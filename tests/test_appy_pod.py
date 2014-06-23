# -*- coding: UTF-8 -*-
"""Verify whether the following bug is fixed:

    Bug Description

    When I run appy_pod.Renderer on a template which contains buggy
    instructions, then the resulting file contains the tracebacks as
    comments. Very well. But sometimes I'd prefer appy.pod to not catch
    such exceptions. E.g. when I run it within a unit test suite.

    https://bugs.launchpad.net/appy/+bug/1169217

Note: this test case is in fact always skipped because the current
development version of appy `has no `setup.py` file
<https://bugs.launchpad.net/appy/+bug/1048963>`_ and thus cannot be
installed using pip (the PYTHONPATH trick doesn't seem work with
`setup.py test`).

"""
import os
import os.path
from os.path import join, dirname, abspath, exists
import sys

import unittest

from appy.pod.renderer import Renderer
from appy import version

PARAMS = dict(pythonWithUnoPath='/usr/bin/python3')
PARAMS.update(raiseOnError=True)

MYDIR = abspath(dirname(__file__))

from distutils.version import StrictVersion as V


class RaiseExceptionTest(unittest.TestCase):

    @unittest.skipIf(V(version.short) < V('0.9.0'),
                     "not supported with appy version %s" % version.short)
    def test_01(self):

        tpl = join(MYDIR, 'appy', 'template.odt')
        context = dict()
        context.update(
            appy_version=version.verbose,
            python_version=sys.version,
            platform=sys.platform,
        )
        target = join(MYDIR, '..', 'tmp', 'result.odt')
        if exists(target):
            os.remove(target)
        renderer = Renderer(tpl, context, target, **PARAMS)
        try:
            renderer.run()
        except Exception as e:
            self.assertEqual(str(e), (
                'Error while evaluating expression "foo".'
                " name 'foo' is not defined"))
