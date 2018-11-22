# Copyright 2013-2015 by Rumma & Ko Ltd.
# License: BSD, see LICENSE for more details.

"""An extended :class:`TestCase` for the plain python tests of a Lino
project.

"""
import os
import sys
import doctest
import warnings

from atelier.test import TestCase


class TestCase(TestCase):
    """An extended :class:`atelier.test.TestCase` to be run using
    :xfile:`setup.py` in the root of a project which may contain
    several Django projects.

    This is different from the classes in :mod:`lino.utils.djangotest`
    which are designed for unit tests to be run using `djange-admin
    test` within a particular Django project.

    """

    django_settings_module = None
    """The :setting:`DJANGO_SETTINGS_MODULE` to set for each subprocess
    launched by this test case.

    """

    def build_environment(self):
        env = super(TestCase, self).build_environment()
        if self.django_settings_module:
            env.update(DJANGO_SETTINGS_MODULE=self.django_settings_module)
        return env

    def setUp(self):

        if self.django_settings_module:
            from lino.core.signals import testcase_setup
            testcase_setup.send(self)
        super(TestCase, self).setUp()

    def run_docs_django_tests(self, n, **kw):
        warnings.warn("run_docs_django_tests is deprecated")
        args = ["django-admin.py"]
        args += ["test"]
        args += ["--settings=%s" % n]
        args += ["--failfast"]
        args += ["--traceback"]
        args += ["--verbosity=0"]
        args += ["--pythonpath=%s" % self.project_root.child('docs')]
        self.run_subprocess(args, **kw)

    def run_django_manage_test(self, cwd=None, **kw):
        """Run `python manage.py test` command in the given directory."""
        args = ["python", "manage.py"]
        args += ["test"]
        if cwd is not None:
            args += ["--top-level-directory=" + os.path.abspath(cwd)]
            # args += [os.path.realpath(cwd)]  # see 20150730
            kw.update(cwd=cwd)
        args += ["--noinput"]
        # args += ["-v3"]  # temporary 20180502
        args += ["--failfast"]
        self.run_subprocess(args, **kw)

    def run_django_admin_test_cd(self, cwd, **kw):
        """Run `django-admin.py test` in the given directory."""
        kw.update(cwd=cwd)
        args = ["django-admin.py"]
        args += ["test"]
        args += ["--settings=settings"]
        args += ["--pythonpath=."]
        args += ["--verbosity=0"]
        args += ["--noinput"]
        args += ["--failfast"]
        args += ["--traceback"]
        self.run_subprocess(args, **kw)

    # def run_django_admin_test(self, settings_module, *args, **kw):
    #     warnings.warn("run_django_admin_test is deprecated")
    #     parts = settings_module.split('.')
    #     assert parts[-1] == "settings"
    #     cwd = '/'.join(parts[:-1])
    #     return self.run_django_admin_test_cd(cwd, *args, **kw)

    def run_django_admin_command(self, settings_module, *cmdargs, **kw):
        args = ["django-admin.py"]
        args += cmdargs
        args += ["--settings=%s" % settings_module]
        self.run_subprocess(args, **kw)

    def run_django_admin_command_cd(self, cwd, *cmdargs, **kw):
        """Run `django-admin.py CMD` in the given directory.
        """
        kw.update(cwd=cwd)
        args = ["python", "manage.py"]
        args += cmdargs
        # args += ["--settings=settings"]
        # args += ["--pythonpath=."]
        self.run_subprocess(args, **kw)

    def run_docs_doctests(self, filename):
        """Run a simple doctest for specified file after importing the docs
        `conf.py` (which causes the demo database to be activated).
        
        This is used e.g. for testing pages like those below
        :doc:`/tested/index`.
        
        
        http://docs.python.org/2/library/doctest.html#doctest.REPORT_ONLY_FIRST_FAILURE
        
        These tests may fail for the simple reason that the demo database
        has not been initialized (in that case, run `fab initdb`).

        """
        filename = 'docs/' + filename
        sys.path.insert(0,  os.path.abspath('docs'))
        import conf  # import Sphinx conf.py which possibly triggers
                     # Django startup

        self.check_doctest(filename)
        # res = doctest.testfile(filename, module_relative=False,
        #                        encoding='utf-8',
        #                        optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

        del sys.path[0]
        #~ os.chdir(oldcwd)

        # if res.failed:
        #     self.fail("doctest.testfile() failed. See earlier messages.")

    def check_doctest(self, n):
        res = doctest.testfile(
            n, module_relative=False,
            encoding='utf-8',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
        if res.failed:
            self.fail("doctest {0} failed.".format(n))
