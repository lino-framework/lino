# -*- coding: UTF-8 -*-
## Copyright 2009-2013 Luc Saffre
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

"""
This creates a list `config_dirs` of all 
configuration directories by looping through :setting:`INSTALLED_APPS` 
and taking those whose source directory has a :xfile:`config` subdir.

..

  DO NOT import this module at the global level of a models module
  because importing it will fill the config dirs, i.e. will try to import 
  every installed `models` module.

The mechanism in this module emulates the behaviour of Django's 
(or Jinja's) template loaders. 
It was written before I discovered Jinja and became less used afterwards.
But we still need it to find the `.odt` files for 
:class:`AppyBuildMethod <lino.mixins.printable.AppyBuildMethod>`.
This task cannot be done using Jinja because
Jinja's `get_template` method returns a `Template`, 
and Jinja templates don't know their filename,
the only thing needed by 
:class:`AppyBuildMethod <lino.mixins.printable.AppyBuildMethod>`.

One possibility might be to write a special Jinja Template class...

Die Reihenfolge in :setting:`INSTALLED_APPS` sollte sein: zuerst 
`django.contrib.*`, dann ``lino``, dann `lino.modlib.*` 
und dann `lino.projects.pcsw`. 
Also vom Allgemeineren zum Spezifischeren. Und bei den config-Dirs soll diese 
Liste umgekehrt abgeklappert werden (und die Suche beim 
ersten Treffer aufhören): zuerst das eventuelle lokale `config_dir`, 
dann `lino.projects.pcsw`, dann die diversen `lino.modlib.*` usw. 

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import os
from os.path import join, abspath, dirname, normpath, isdir

import sys
import codecs
import glob

from fnmatch import fnmatch

from django.utils.importlib import import_module
from django.conf import settings

from lino import ad
from lino.utils import iif

SUBDIR_NAME = 'config' # we might change this to "templates" 

class ConfigDir:
    """
    A configuration directory is a directory that may contain configuration files.
    
    """
    def __init__(self,name,writeable):
        self.name = os.path.abspath(name)
        self.writeable = writeable
        
    def __repr__(self):
        return "ConfigDir %s" % self.name + iif(self.writeable," (writeable)","")
        

fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
config_dirs = []

for pth in settings.SITE.get_settings_subdirs(SUBDIR_NAME):
    config_dirs.append(ConfigDir(pth.decode(fs_encoding),False))

def add_config_dir(name,mod):
    pth = join(dirname(mod.__file__),SUBDIR_NAME)    
    if isdir(pth):
        config_dirs.append(ConfigDir(pth.decode(fs_encoding),False))
        
settings.SITE.for_each_app(add_config_dir)

#~ for app in settings.INSTALLED_APPS:
    #~ app_mod = import_module(app)
    #~ app = getattr(app_mod,'App',None)
    #~ if isinstance(app,ad.App) and app.extends:
        #~ parent = import_module(app.extends)
        #~ add_config_dir(parent)
    #~ add_config_dir(app_mod)
    
LOCAL_CONFIG_DIR = None

#~ if settings.SITE.project_dir != settings.SITE.source_dir:
if settings.SITE.is_local_project_dir:
    p = join(settings.SITE.project_dir,SUBDIR_NAME)
    if isdir(p):
        LOCAL_CONFIG_DIR = ConfigDir(p,True)
        config_dirs.append(LOCAL_CONFIG_DIR)

config_dirs.reverse()
config_dirs = tuple(config_dirs)

#~ logger.debug('config_dirs:\n%s', '\n'.join([repr(cd) for cd in config_dirs]))

#~ for app_name in settings.INSTALLED_APPS:
    #~ app = import_module(app_name)
    #~ fn = getattr(app,'__file__',None)
    #~ if fn is not None:
        #~ pth = join(dirname(fn),'config')
        #~ if isdir(pth):
            #~ config_dirs.append(ConfigDir(pth,False))
    #~ LOCAL_CONFIG_DIR = ConfigDir(join(settings.PROJECT_DIR,'config'),True)
    #~ config_dirs.append(LOCAL_CONFIG_DIR)

  
def find_config_file(fn,group=''):
    if os.path.isabs(fn):
        return fn
    if group:
        prefix = join(*(group.split('/')))
    else:
        prefix = ''
    for cd in config_dirs:
        ffn = join(cd.name,prefix,fn)
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
        prefix = os.path.sep + join(*(group.split('/')))
        #~ if not group.endswith('/'):
            #~ group += '/'
    else:
        prefix = ''
    files = {}
    for cd in config_dirs:
        pth = cd.name + prefix
        #~ print 'find_config_files() discover', pth, pattern
        if isdir(pth):
            for fn in os.listdir(pth):
                if fnmatch(fn,pattern):
                    files.setdefault(fn,cd)
                    #~ if not files.has_key(fn):
                        #~ files[fn] = cd
        #~ else:
            #~ print 'find_config_files() not a directory:', pth
    return files
    
def find_template_config_files(template_ext,templates_group):
    """
    find_config_files and ignore babel variants:
    e.g. ignore "foo_fr.html" if "foo.html" exists 
    but don't ignore "my_template.html"
    """
    files = find_config_files('*' + template_ext,templates_group)
    l = []
    template_ext
    for name in files.keys():
        basename = name[:-len(template_ext)]
        chunks = basename.split('_')
        if len(chunks) > 1:
            basename = '_'.join(chunks[:-1])
            if files.has_key(basename + template_ext):
                continue
        l.append(name)
    l.sort()
    if not l:
        logger.warning("email_template_choices() : no matches for (%r,%r)",
          '*' + template_ext,templates_group)
    return l
        
    

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
        filename = join(prefix,filename)
        ffn = join(cd.name,filename)
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
            raise IOError("Cannot save because there is no local config directory")
            
        if not self.cd.writeable:
            #~ print self.cd, "is not writable", self.filename
            self.cd = LOCAL_CONFIG_DIR
        fn = join(self.cd.name,self.filename)
        pth = dirname(fn)
        settings.SITE.makedirs_if_missing(pth)
        #~ if not os.path.exists(pth):
            #~ os.makedirs(pth)
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
        fn = join(self.cd.name,self.filename)
        if self.cd.writeable: 
            logger.info("Not writing %s because %s is writeable",
                self.filename,self.cd.name)
            return
        #~ if self.messages: 
        """
        if there are no messages, we still write a 
        new file to remove messages from pervious versions.
        """
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
    Write a dummy `.py` source file containing 
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
  
