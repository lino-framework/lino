# -*- coding: UTF-8 -*-
## Copyright 2009-2011 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

u"""
The Lino process creates a list config_dirs of all 
configuration directories on server startup
by looping through :setting:`INSTALLED_APPS` that have a :xfile:`config` 
subdir.

Die Reihenfolge in :setting:`INSTALLED_APPS` sollte sein: zuerst 
`django.contrib.*`, dann ``lino``, dann `lino.modlib.*` und dann `lino.apps.dsbe`. 
Also vom Allgemeineren zum Spezifischeren. Und bei den config-Dirs soll diese 
Liste umgekehrt abgeklappert werden (und die Suche beim 
ersten Treffer aufhören): zuerst das eventuelle lokale `config_dir`, 
dann `lino.apps.dsbe`, dann die diversen `lino.modlib.*` usw. 

"""

import logging
logger = logging.getLogger(__name__)

import os
import sys
import codecs

from fnmatch import fnmatch

from django.conf import settings
from django.utils.importlib import import_module

from lino.tools import makedirs_if_missing
from lino.utils import iif

class ConfigDir:
    """
    A configuration directory is a directory that may contain configuration files.
    
    """
    def __init__(self,name,writeable):
        self.name = name
        self.writeable = writeable
        
    def __repr__(self):
        return "ConfigDir %s" % self.name + iif(self.writeable," (writeable)","")
        

# similar logic as in django.template.loaders.app_directories
fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
config_dirs = []
for app in settings.INSTALLED_APPS:
    mod = import_module(app)
    dirname = os.path.join(os.path.dirname(mod.__file__), 'config')
    if os.path.isdir(dirname):
        config_dirs.append(ConfigDir(dirname.decode(fs_encoding),False))

LOCAL_CONFIG_DIR = None

if settings.LINO.project_dir != settings.LINO.source_dir:
    """
    When called by makedocs, there is no local config dir.
    """
    dirname = os.path.join(settings.LINO.project_dir,'config')
    if os.path.isdir(dirname):
        LOCAL_CONFIG_DIR = ConfigDir(dirname,True)
        config_dirs.append(LOCAL_CONFIG_DIR)

config_dirs.reverse()
config_dirs = tuple(config_dirs)

#~ logger.debug('config_dirs:\n%s', '\n'.join([repr(cd) for cd in config_dirs]))

#~ for app_name in settings.INSTALLED_APPS:
    #~ app = import_module(app_name)
    #~ fn = getattr(app,'__file__',None)
    #~ if fn is not None:
        #~ dirname = os.path.join(os.path.dirname(fn),'config')
        #~ if os.path.isdir(dirname):
            #~ config_dirs.append(ConfigDir(dirname,False))
    #~ LOCAL_CONFIG_DIR = ConfigDir(os.path.join(settings.PROJECT_DIR,'config'),True)
    #~ config_dirs.append(LOCAL_CONFIG_DIR)

def find_config_file(fn,group=''):
    if os.path.isabs(fn):
        return fn
    if group:
        prefix = os.path.join(*(group.split('/')))
    else:
        prefix = ''
    for cd in config_dirs:
        ffn = os.path.join(cd.name,prefix,fn)
        if os.path.exists(ffn):
            return ffn


def find_config_files(pattern,group=''):
    """
    Returns a dict of filename -> config_dir entries for 
    each config file on this site that matches the pattern.
    Loops through `config_dirs` and collects matching files. 
    When more than one file of the same name exists in different 
    applications it gets overridden by later apps.
    
    `group` is e.g. '','foo', 'foo/bar',...
    
    """
    if group:
        prefix = os.path.sep + os.path.join(*(group.split('/')))
        #~ if not group.endswith('/'):
            #~ group += '/'
    else:
        prefix = ''
    files = {}
    for cd in config_dirs:
        #~ print 'find_config_files() discover', dirname, pattern
        dirname = cd.name + prefix
        if os.path.exists(dirname):
            for fn in os.listdir(dirname):
                if fnmatch(fn,pattern):
                    files.setdefault(fn,cd)
                    #~ if not files.has_key(fn):
                        #~ files[fn] = cd
        #~ else:
            #~ print 'find_config_files() not a directory:', dirname
    return files

def load_config_files(loader,pattern,group=''):
    """
    Naming conventions for :xfile:`*.dtl` files are:
    
    - the first detail is called appname.Model.dtl
    - If there are more Details, then they are called 
      appname.Model.2.dtl, appname.Model.3.dtl etc.
    
    The `sort()` below must remove the filename extension (".dtl") 
    because otherwise the frist Detail would come last.
    """
    files = find_config_files(pattern,group).items()
    def fcmp(a,b):
        return cmp(a[0][:-4],b[0][:-4])
    files.sort(fcmp)
    prefix = group.replace("/",os.sep)
    for filename,cd in files:
        filename = os.path.join(prefix,filename)
        ffn = os.path.join(cd.name,filename)
        logger.debug("Loading %s...",ffn)
        s = codecs.open(ffn,encoding='utf-8').read()
        loader(s,cd,filename)
        

class Configured(object):
  
    #~ filename = None
    #~ cd = None # ConfigDir
    
    def __init__(self,filename=None,cd=None):
        if filename is not None:
            assert not os.pardir in filename
            #~ assert not os.sep in filename
            if cd is None:
                cd = LOCAL_CONFIG_DIR
        self.filename = filename
        self.cd = cd
        self.messages = set()

    def save_config(self):
        if not self.filename:
            raise IOError('Cannot save unnamed %s' % self)
        if self.cd is None:
            raise IOError("Cannot save because there is no LOCAL_CONFIG_DIR")
            
        if not self.cd.writeable:
            #~ print self.cd, "is not writable", self.filename
            self.cd = LOCAL_CONFIG_DIR
        fn = os.path.join(self.cd.name,self.filename)
        dirname = os.path.dirname(fn)
        makedirs_if_missing(dirname)
        #~ if not os.path.exists(dirname):
            #~ os.makedirs(dirname)
        f = codecs.open(fn,'w',encoding='utf-8')
        self.write_content(f)
        f.close()
        msg = "%s has been saved to %s" % (self.__class__.__name__,fn)
        logger.info(msg)
        return msg
        
    def make_dummy_messages_file(self):
        """
        Make dummy messages file for this Configurable.
        Calls the global :func:`make_dummy_messages_file`
        """
        if not self.filename: return
        if self.cd is None: return
        fn = os.path.join(self.cd.name,self.filename)
        if self.cd.writeable: 
            logger.info("Not writing %s because %s is writeable",
                self.filename,self.cd.name)
            return
        if self.messages:
            make_dummy_messages_file(fn,self.messages)
        
        
    def add_dummy_message(self,msg):
        self.messages.add(msg)
            
    def write_content(self,f):
        raise NotImplementedError
        
    def __str__(self):
        if self.filename:
            return u"%s (from %s)" % (self.filename,self.cd)
        return "Dynamic " + super(Configured,self).__str__()
        # "%s(%r)" % (self.__class__.__name__,self._desc)
        

        
IGNORE_TIMES = False
MODIFY_WINDOW = 2

def must_make(src,target):
    "returns True if src is newer than target"
    try:
        src_st = os.stat(src)
        src_mt = src_st.st_mtime
    except OSError,e:
        # self.error("os.stat() failed: ",e)
        return False

    try:
        target_st = os.stat(target)
        target_mt = target_st.st_mtime
    except OSError,e:
        # self.error("os.stat() failed: %s",e)
        return True

    if src_mt - target_mt > MODIFY_WINDOW:
        return True
    return False
        

def make_dummy_messages_file(src_fn,messages):
    """
    Write a dummy `.py`source file containing 
    translatable messages that getmessages will find. 
    """
    target_fn = src_fn + '.py'
    if not must_make(src_fn,target_fn):
        logger.debug("%s is up-to-date.", target_fn)
        return
    try:
        f = file(target_fn,'w')
    except IOError,e:
        logger.warning("Could not write file %s : %s", target_fn, e)
        return 
    f.write("# this file is generated by Lino\n")
    f.write("from django.utils.translation import ugettext\n")
    for m in messages:
        f.write("ugettext(%r)\n" % m)
    f.close()
    logger.info("Wrote %d dummy messages to %s.", len(messages),target_fn)
  
