# -*- coding: UTF-8 -*-
# Copyright 2012-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Defines some utilities to inspect the running Python code.

"""
from builtins import str
from builtins import object

import logging
logger = logging.getLogger(__name__)

import os
import sys
import time
import fnmatch
import rstgen


def codefiles(pattern='*'):
    """
    Yield a list of the source files corresponding to the currently
    imported modules that match the given pattern
    """
    #~ exp = re.compile(pattern, flags)

    for name, mod in list(sys.modules.items()):
        #~ if name == 'lino.extjs' and pattern == '*':
            #~ logger.info("20130801 %r -> %r", name,mod.__file__)
        if fnmatch.fnmatch(name, pattern):
        #~ if exp.match(name):
            filename = getattr(mod, "__file__", None)
            if filename is not None:
                if filename.endswith(".pyc") or filename.endswith(".pyo"):
                    filename = filename[:-1]
                if filename.endswith("$py.class"):
                    filename = filename[:-9] + ".py"
                # File might be in an egg, so there's no source available
                if os.path.exists(filename):
                    yield name, filename


def codetime(*args, **kw):
    """Return the modification time of the youngest source code in memory.

    Used by :mod:`lino.modlib.extjs` to avoid generating .js files if
    not necessary.

    Inspired by the code_changed() function in `django.utils.autoreload`.

    """
    code_mtime = None
    pivot = None
    for name, filename in codefiles(*args, **kw):
        stat = os.stat(filename)
        mtime = stat.st_mtime
        if code_mtime is None or code_mtime < mtime:
            # print 20130204, filename, time.ctime(mtime)
            code_mtime = mtime
            pivot = filename
    # print '20130204 codetime:', time.ctime(code_mtime), pivot
    return code_mtime


def is_start_of_docstring(line):
    for delim in '"""', "'''":
        if line.startswith(delim) or line.startswith('u' + delim) \
           or line.startswith('r' + delim) \
           or line.startswith('ru' + delim):
            return delim


class SourceFile(object):

    """
    Counts the number of code lines in a given Python source file.
    """

    def __init__(self, modulename, filename):
        self.modulename = modulename
        self.filename = filename
        self.analyze()

    def analyze(self):
        self.count_code, self.count_total, self.count_blank, self.count_doc = 0, 0, 0, 0
        self.count_comment = 0
        #~ count_code, count_total, count_blank, count_doc = 0, 0, 0, 0
        skip_until = None
        for line in open(self.filename).readlines():
            self.count_total += 1
            line = line.strip()
            if not line:
                self.count_blank += 1
            else:
                if line.startswith('#'):
                    self.count_comment += 1
                    continue
                if skip_until is None:
                    skip_until = is_start_of_docstring(line)
                    if skip_until is not None:
                        self.count_doc += 1
                        #~ skip_until = '"""'
                        continue
                    #~ if line.startswith('"""') or line.startswith('u"""'):
                        #~ count_doc += 1
                        #~ skip_until = '"""'
                        #~ continue
                    #~ if line.startswith("'''") or line.startswith("u'''"):
                        #~ count_doc += 1
                        #~ skip_until = "'''"
                        #~ continue
                    self.count_code += 1
                else:
                    self.count_doc += 1
                    #~ if line.startswith(skip_until):
                    if skip_until in line:
                        skip_until = None

        #~ self.count_code, count_total, count_blank, count_doc


def analyze_rst(*packages):
    """
    Example:
    
    >>> from lino.utils.code import analyze_rst
    >>> print analyze_rst('lino')
      
    """
    fields = 'count_code count_doc count_comment count_total'.split()
    headers = ["name", "code lines", "doc lines",
               "comment lines", "total lines"]
    rows = []

    def fmt(n):
        return "{}k".format(round(n/1000.0, 1))

    total_sums = [0] * len(fields)
    for package in packages:
        sums = [0] * len(fields)
        for name, filename in codefiles(package + '*'):
            sf = SourceFile(name, filename)
            for i, k in enumerate(fields):
                sums[i] += getattr(sf, k)
        rows.append([package] + [fmt(n) for n in sums])
        for i, k in enumerate(fields):
            total_sums[i] += sums[i]
    rows.append(['total'] + [fmt(n) for n in total_sums])
    return rstgen.table(headers, rows)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
