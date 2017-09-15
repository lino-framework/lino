# -*- coding: UTF-8 -*-
# Copyright 2013-2017 by Luc Saffre & Hamza Khchine.
# License: BSD, see LICENSE for more details.

from atelier.invlib.tasks import *

from importlib import import_module

def run_in_demo_projects(ctx, admin_cmd, *more, **kwargs):
    """Run the given shell command in each demo project (see
    :attr:`ctx.demo_projects`).

    """
    cov = kwargs.pop('cov', False)
    for mod in ctx.demo_projects:
        # print("-" * 80)
        # print("In demo project {0}:".format(mod))
        m = import_module(mod)
        # 20160710 p = m.SITE.cache_dir or m.SITE.project_dir
        p = m.SITE.project_dir
        with cd(p):
            # m = import_module(mod)
            if cov:
                args = ["coverage"]
                args += ["run --append"]
                args += ["`which django-admin.py`"]
                datacovfile = ctx.root_dir.child('.coverage')
                if not datacovfile.exists():
                    print('No .coverage file in {0}'.format(ctx.project_name))
                os.environ['COVERAGE_FILE'] = datacovfile
            else:
                args = ["django-admin.py"]
            args += [admin_cmd]
            args += more
            args += ["--settings=" + mod]
            cmd = " ".join(args)
            print("-" * 80)
            print("Run in demo project {0}\n$ {1} :".format(p, cmd))
            ctx.run(cmd, pty=True)


@task(name='prep')
def prep(ctx, cov=False):
    """Run `manage.py prep` on every demo project."""
    if cov:
        covfile = ctx.root_dir.child('.coveragerc')
        if not covfile.exists():
            raise Exception('No .coveragerc file in {0}'.format(
                ctx.project_name))
        # os.environ['COVERAGE_PROCESS_START'] = covfile
        ctx.run('coverage erase', pty=True)
        
    run_in_demo_projects(ctx, 'prep', "--noinput", '--traceback', cov=cov)


@task(name='cov', pre=[tasks.call(prep, cov=True)])
def run_tests_coverage(ctx, html=True, html_cov_dir='htmlcov'):
    """Run all tests and create a coverage report.

    If there a directory named :xfile:`htmlcov` in your project's
    `root_dir`, then it will write a html report into this directory
    (overwriting any files without confirmation).

    """
    covfile = ctx.root_dir.child('.coveragerc')
    if not covfile.exists():
        print('No .coveragerc file in {0}'.format(ctx.project_name))
        return
    if ctx.root_dir.child('pytest.ini').exists():
        ctx.run('coverage combine', pty=True)
        print("Running pytest in {1} within coverage...".format(
            ctx.coverage_command, ctx.project_name))
        with cd(ctx.root_dir):
            ctx.run('py.test --cov=lino --cov-append', pty=True)
        html = False
    else:
        os.environ['COVERAGE_PROCESS_START'] = covfile
        ctx.run('coverage erase', pty=True)
        print("Running {0} in {1} within coverage...".format(
            ctx.coverage_command, ctx.project_name))
        ctx.run('coverage run {}'.format(ctx.coverage_command), pty=True)
    ctx.run('coverage combine', pty=True)
    ctx.run('coverage report', pty=True)
    if html:
        pth = ctx.root_dir.child(html_cov_dir)
        print("Writing html report to {}".format(pth))
        ctx.run('coverage html -d {}'.format(pth), pty=True)
        if False:
            ctx.run('open {}/index.html'.format(pth), pty=True)
        print('html report is ready.')
    ctx.run('coverage erase', pty=True)


