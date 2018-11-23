# -*- coding: UTF-8 -*-
# Copyright 2009-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""This defines the :class:`ConfigDirCache` which Lino instantiates
and installs as :attr:`SITE.confdirs
<lino.core.site.Site.confdirs>`.

It creates a list `config_dirs` of all configuration directories by
looping through :attr:`lino.core.site.Site.installed_plugins` and taking those
whose source directory has a :xfile:`config` subdir.

The mechanism in this module emulates the behaviour of Django's and
Jinja's template loaders.

We cannot use the Jinja loader because Jinja's `get_template` method
returns a `Template`, and Jinja templates don't know their filename.
One possibility might be to write a special Jinja Template class...

"""

from __future__ import unicode_literals
from builtins import object

import logging
logger = logging.getLogger(__name__)

import os
from os.path import join, abspath, dirname, isdir
import sys
import codecs
from fnmatch import fnmatch
import six

fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()

from lino.utils import iif

SUBDIR_NAME = 'config'  # we might change this to "templates"


class ConfigDir(object):

    """A directory that may contain configuration files.

    """

    def __init__(self, name, writeable):
        self.name = abspath(name)
        self.writeable = writeable

    def __repr__(self):
        return "ConfigDir %s" % self.name + iif(
            self.writeable, " (writeable)", "")


class ConfigDirCache(object):
    _init = False

    def __init__(self, site):
        if self._init:
            raise Exception("Oops, ConfigDirCache was already instantiated!")
        self._init = True
        self.site = site
        self.scan_config_dirs()
        
    def scan_config_dirs(self):
        """Scan the file system and populate :attr:`config_dirs`."""
        config_dirs = []

        for pth in self.site.get_settings_subdirs(SUBDIR_NAME):
            if six.PY2:
                pth = pth.decode(fs_encoding)
            config_dirs.append(ConfigDir(pth, False))

        def add_config_dir(name, mod):
            pth = join(dirname(mod.__file__), SUBDIR_NAME)
            if isdir(pth):
                # logger.info("add_config_dir %s %s", name, pth)
                # config_dirs.append(ConfigDir(pth.decode(fs_encoding), False))
                config_dirs.append(ConfigDir(pth, False))

        self.site.for_each_app(add_config_dir)

        self.LOCAL_CONFIG_DIR = None

        p = self.site.cache_dir.child(SUBDIR_NAME)
        if isdir(p):
            self.LOCAL_CONFIG_DIR = ConfigDir(p, True)
            config_dirs.append(self.LOCAL_CONFIG_DIR)

        config_dirs.reverse()
        self.config_dirs = tuple(config_dirs)

        # logger.info('config_dirs:\n%s', '\n'.join([
        #     repr(cd) for cd in config_dirs]))

    def find_config_file(self, fn, *groups):
        """
        Return the full path of the first occurence within the
        :class:`lino.utils.config.ConfigDirCache` of a file named
        `filename`

        """
        if os.path.isabs(fn):
            return fn
        if len(groups) == 0:
            groups = ['']
        for group in groups:
            if group:
                prefix = join(*(group.split('/')))
            else:
                prefix = ''
            for cd in self.config_dirs:
                ffn = join(cd.name, prefix, fn)
                if os.path.exists(ffn):
                    return ffn

    def find_config_files(self, pattern, *groups):
        """
        Returns a dict of `filename` -> `config_dir` entries for each config
        file on this site that matches the pattern.  Loops through
        `config_dirs` and collects matching files.  When a filename is
        provided by more than one app, then the latest app gets it.

        `groups` is a tuple of strings, e.g. '', 'foo', 'foo/bar', ...

        """
        files = {}
        for group in groups:
            if group:
                prefix = os.path.sep + join(*(group.split('/')))
            else:
                prefix = ''
            for cd in self.config_dirs:
                pth = cd.name + prefix
                if isdir(pth):
                    for fn in os.listdir(pth):
                        if fnmatch(fn, pattern):
                            files.setdefault(fn, cd)
        return files

    def find_template_config_files(self, template_ext, *groups):
        """
        Like :func:`find_config_files`, but ignore babel variants:
        e.g. ignore "foo_fr.html" if "foo.html" exists.
        Note: but don't ignore "my_template.html"
        """
        files = self.find_config_files('*' + template_ext, *groups)
        l = []
        template_ext
        for name in list(files.keys()):
            basename = name[:-len(template_ext)]
            chunks = basename.split('_')
            if len(chunks) > 1:
                basename = '_'.join(chunks[:-1])
                if basename + template_ext in files:
                    continue
            l.append(name)
        l.sort()
        if not l:
            logger.warning(
                "find_template_config_files() : no matches for (%r, %r)",
                '*' + template_ext, groups)
        return l

    def load_config_files(self, loader, pattern, *groups):
        """
        Currently not used.
        Naming conventions for :xfile:`*.dtl` files are:

        - the first detail is called appname.Model.dtl
        - If there are more Details, then they are called
          appname.Model.2.dtl, appname.Model.3.dtl etc.

        The `sort()` below must remove the filename extension (".dtl")
        because otherwise the frist Detail would come last.
        """
        files = list(self.find_config_files(pattern, *groups).items())

        def fcmp(a):
            return a[0][:-4]
        files.sort(key=fcmp)
        for group in groups:
            prefix = group.replace("/", os.sep)
            for filename, cd in files:
                filename = join(prefix, filename)
                ffn = join(cd.name, filename)
                logger.debug("Loading %s...", ffn)
                s = codecs.open(ffn, encoding='utf-8').read()
                loader(s, cd, filename)


IGNORE_TIMES = False
MODIFY_WINDOW = 2


def must_make(src, target):
    "returns True if src is newer than target"
    try:
        src_st = os.stat(src)
        src_mt = src_st.st_mtime
    except OSError:
        # self.error("os.stat() failed: ",e)
        return False

    try:
        target_st = os.stat(target)
        target_mt = target_st.st_mtime
    except OSError:
        # self.error("os.stat() failed: %s", e)
        return True

    if src_mt - target_mt > MODIFY_WINDOW:
        return True
    return False


def make_dummy_messages_file(src_fn, messages):
    """
    Write a dummy `.py` source file containing
    translatable messages that getmessages will find.
    """
    raise Exception("Never used")
    target_fn = src_fn + '.py'
    if not must_make(src_fn, target_fn):
        logger.debug("%s is up-to-date.", target_fn)
        return
    try:
        f = file(target_fn, 'w')
    except IOError as e:
        logger.warning("Could not write file %s : %s", target_fn, e)
        return
    f.write("# this file is generated by Lino\n")
    f.write("from django.utils.translation import ugettext\n")
    for m in messages:
        f.write("ugettext(%r)\n" % m)
    f.close()
    logger.info("Wrote %d dummy messages to %s.", len(messages), target_fn)
