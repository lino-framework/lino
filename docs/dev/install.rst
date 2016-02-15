.. _lino.dev.install:

===============
Installing Lino
===============

.. _pip: http://www.pip-installer.org/en/latest/
.. _virtualenv: https://pypi.python.org/pypi/virtualenv
.. _fabric: http://www.fabfile.org/
.. _pycrypto: https://pypi.python.org/pypi/pycrypto
.. _atelier: http://atelier.lino-framework.org/
.. _git: http://git-scm.com/downloads
.. _lxml: http://lxml.de/

This document describes how to install Lino.  It is meant for people
who plan to write their own Lino application.  Alternativaly you might
prefer to install one of the existing Lino applications, e.g.  `Lino
Così <http://cosi.lino-framework.org/install/index.html>`__ of `Lino
Welfare <http://welfare.lino-framework.org/admin/install.html>`__.

This tutorial assumes you are familiar with the Linux shell at least
for basic file operations like :cmd:`ls`, :cmd:`cp`, :cmd:`mkdir`,
:cmd:`rmdir`, file permissions, environment variables etc. Otherwise
we suggest to keep Mendel Cooper's `Advanced Bash-Scripting Guide
<http://tldp.org/LDP/abs/html/>`_ under your pillow.

.. contents::
    :depth: 1
    :local:


System requirements
===================

#.  Lino requires **Python 2**.  We just did not yet take the time to
    make it work with Python 3. Any contribution is welcome.

#.  We assume you have pip_ installed. `pip` is not automatically
    bundled with Python 2, but it has become the de-facto standard.

#.  We recommend to use virtualenv_ and to activate a new environment.
    On a Debian system this means something like::

        $ sudo pip install virtualenv
        $ mkdir ~/virtualenvs
        $ virtualenv ~/virtualenvs/a
        $ . ~/virtualenvs/a/bin/activate

    Note that the `--no-site-packages
    <https://virtualenv.pypa.io/en/latest/reference.html?highlight=site-packages#cmdoption--no-site-packages>`__
    option is needed only if your virtualenv is older than X.
    
#.  You will need the **Python header files** on your system because
    Lino requires fabric_ which in turn requires pycrypto_ which is an
    `extension module <https://docs.python.org/2/c-api/intro.html>`_. On a
    Debian system this means something like::

        $ sudo apt-get install python-dev

#.  You will need to install git_ on your computer to get the source
    files.

#.  Lino requires lxml_, which has some extra requirements::

      sudo apt-get build-dep lxml


Get the sources
===============

You might theoretically install Lino using ``pip install lino``, but
this method isn't currently being tested very thoroughly. So in most
cases we currently recommend to use the development version because
you will probably want to use Lino's newest features before they get
officially released on PyPI.

Create a directory (e.g. :file:`~/repositories`) meant to hold your
working copies of version-controlled software projects, `cd` to that
directory and and do::

  $ mkdir ~/repositories
  $ cd ~/repositories
  $ git clone https://github.com/lsaffre/lino.git

You should now have a directory called `~/repositories/lino`, which
contains a file :xfile:`setup.py`, a file :xfile:`README.rst` and a
whole tree of other files and directories.

Installation
============

Now you are ready to "install" Lino, i.e. to tell your Python
interpreter where the source file are, so that you can import them
from within any Python program.

Commands::

  $ pip install -e lino

Notes:

- The `-e
  <https://pip.pypa.io/en/latest/reference/pip_install.html#cmdoption-e>`_
  command-line switch for :command:`pip` causes it to use the "development"
  mode.  Development mode means that these modules run "directly from
  source".  `pip` does not *copy* the sources to your Python
  `site_packages`, but instead adds a link to them.  The first
  argument after ``-e`` is not a *project name* but a *directory*.

- Alternatively (without pip_) you could have done::

      $ cd lino ; python setup.py develop ; cd ..


Telling your Lino version
=========================

A quick test when you want to see whether Lino is installed is to say
"hello" to Lino:

.. py2rst::

    self.shell_block(["python", "-m", "lino.hello"])

In case you didn't know: Python's `-m
<https://docs.python.org/2/using/cmdline.html#cmdoption-m>`_
command-line switch instructs it to just *import* the specified module
(here :mod:`lino.hello`) and then to return to the command line.

Updating your copy of the Lino sources
======================================

Actually the Lino version is not enough when using a developer
installation of Lino.  The Lino codebase repository changes almost
every day, but the version is incremented only when we do an official
release to PyPI.

as a developer you will simply update your copy of the code repository
often. In order to get the latest version, you just need to run::

  $ cd ~/repositories/lino
  $ git pull

You don't need to reinstall it in Python after such an upgrade since
you used the ``-e`` option of `pip install` above. The new version
will automatically become active.

See the documentation of `git pull
<https://git-scm.com/docs/git-pull>`_ for more information.



Defining a cache directory for Lino
===================================

Before going on, you should prepare a place where Lino can store
temporary files like the SQLite database file, static files and
dynamically generated files of miscellaneous types like `.js`, `.pdf`,
`.xls`.

You do this by creating an empty directory where you have write
permission, and then set the :envvar:`LINO_CACHE_ROOT` environment
variable to point to it.

We recommend to create this directory below your virtual environment::

  $ cd ~/virtualenvs/a
  $ mkdir lino_cache

And then to add the following line to your
:file:`~/virtualenvs/a/bin/activate` script

   export LINO_CACHE_ROOT=$VIRTUAL_ENV/lino_cache

Don't forget to re-run the script in order to activate these changes.
You can verify whether the variable is set using this command::

    $ set | grep LINO

More about this in :doc:`cache`.


Collecting static files
=======================

One part of your cache directory are the static files.  When your
:envvar:`LINO_CACHE_ROOT` is set, you should run Django's
:manage:`collectstatic` command::

    $ cd lino/projects/min1
    $ python manage.py collectstatic

The output should be something like this::

    You have requested to collect static files at the destination
    location as specified in your settings:

        /home/myname/virtualenvs/a/lino_cache/collectstatic

    This will overwrite existing files!
    Are you sure you want to do this?

    Type 'yes' to continue, or 'no' to cancel: yes

    4688 static files copied to '/home/myname/virtualenvs/a/lino_cache/collectstatic', 0 unmodified.

Note that you can chose an arbitrary project directory for running
:manage:`collectstatic`, it does not need to be :mod:`min1
<lino.projects.min1>`. That's because all Lino applications have the
same set of staticfiles.

You need to do this only for your first local Lino project because
static files are the same for every Lino application.  (There are
exceptions to this rule, but we can ignore them for the moment.)


Run Lino's test suite
=====================

In order to check to see whether everything worked well, we are now
going to run the test suite.

And before running the test suite, we must initialize the **demo
databases** because the test suite has many test cases which would
fail if these demo databases were missing or not in their virgin
state.

The easiest way to initialize the demo databases is to run the
:cmd:`fab initdb` command::

    $ cd ~/repositories/lino
    $ fab initdb

The ``fab`` command has been installed on your system (more precisely:
into your Python environment) by the fabric_ package, which itself has
been required by atelier_, which is another Python package developed
by :ref:`luc`.

The ``fab`` command is a kind of Make tool which works by looking for
a file named :xfile:`fabfile.py`. The Lino repository contains such a
file, and this file uses :mod:`atelier.fablib`, which defines a whole
series of tasks like `initdb` and `test`.

And here we go for the test suite itself::

    $ fab test

The :cmd:`fab test` command is a short for ``python setup.py test``
which simply runs the test suite.  The output should be something like
this::

    [localhost] local: python setup.py -q test
    .....................................................................
    ----------------------------------------------------------------------
    Ran 74 tests in 52.712s
    OK
    Done.


Congratulations if you got the test suite to pass.

As your next step, we now suggest to :doc:`/tutorials/hello/index`.


Install LibreOffice if necessary
================================

Most Lino applications (:ref:`cosi`, :ref:`noi`, :ref:`welfare` use
:mod:`lino.modlib.appypod` for printing and therefore require
:ref:`admin.oood`.
