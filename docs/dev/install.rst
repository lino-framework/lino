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

This document describes how to install Lino.  It is meant for people
who plan to write their own Lino application.  Alternativaly you might
prefer to install one of the existing Lino applications, e.g.  `Lino
Così <http://cosi.lino-framework.org/install/index.html>`__ of `Lino
Welfare <http://welfare.lino-framework.org/admin/install.html>`__.


.. contents::
    :depth: 1
    :local:

System requirements
===================

#.  Lino still requires **Django 1.6**, we just did not yet take the
    time to make it work with newer versions. Any contribution is
    welcome.

#.  Lino requires **Python 2**.  Also here: we just did not yet take the
    time to make it work with Python 3. Any contribution is welcome.

#.  We assume you have pip_ installed. `pip` is not automatically
    bundled with Python 2, but it has become the de-facto standard.

#.  We recommend to use virtualenv_ and to activate a new environment.
    On a Debian system this means something like::

        $ pip install python-virtualenv
        $ virtualenv myenv
        $ . myenv/bin/activate

#.  You will need the **Python header files** on your system because
    Lino requires fabric_ which in turn requires pycrypto_ which is an
    `extension module <https://docs.python.org/2/c-api/intro.html>`_. On a
    Debian system this means something like::

        $ sudo apt-get install python-dev

#.  You will need to install git_ on your computer to get the source
    files.


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

When you want to see which version you have, you can say "hello" to
Lino:


.. py2rst::

    self.shell_block(["python", "-m", "lino.hello"])


The above launches Python with the `-m
<https://docs.python.org/2/using/cmdline.html#cmdoption-m>`_
command-line switch which basically instructs it to just import the
specified module :mod:`lino.hello`.

Defining a cache directory for Lino
===================================

Before going on, you should prepare a place where Lino can store
temporary files like the SQLite database file, static files and
dynamically generated files of miscellaneous types like `.js`, `.pdf`,
`.xls`.

You do this by creating an empty directory where you have write
permission, and then set the :envvar:`LINO_CACHE_ROOT` environment
variable to point to it.

For example on a Debian system you might add the following line to
your :xfile:`.bashrc` file::

    export LINO_CACHE_ROOT=/home/myname/tmp/lino_cache

Don't forget to open a new terminal window after editing the file in
order to activate these changes.  You can verify whether the variable
is set using this command::

    $ set | grep LINO

More about this in :doc:`cache`.


Collecting static files
=======================

One part of your cache directory are the static files.  When your
:envvar:`LINO_CACHE_ROOT` is set, you should run Django's
:manage:`collectstatic` command::

    $ python manage.py collectstatic

The output should be something like this::

    You have requested to collect static files at the destination
    location as specified in your settings:

        /home/myname/tmp/lino_cache/collectstatic

    This will overwrite existing files!
    Are you sure you want to do this?

    Type 'yes' to continue, or 'no' to cancel: yes

    4688 static files copied to '/home/myname/tmp/lino_cache/collectstatic', 0 unmodified.


You need to do this only for your first local Lino project because
static files are the same for every Lino application.  There are
exceptions to this rule, but we can ignore them for the moment.


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
    Ran 69 tests in 52.712s
    OK
    Done.


Congratulations if you got the test suite to pass.

As your next step, we now suggest to :doc:`/tutorials/hello/index`.


Install LibreOffice if necessary
================================

Most Lino applications (:ref:`cosi`, :ref:`noi`, :ref:`welfare` use
:mod:`lino.modlib.appypod` for printing and therefore require
:ref:`admin.oood`.
