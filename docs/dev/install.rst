.. _lino.dev.install:

===============
Installing Lino
===============

.. _pip: http://www.pip-installer.org/en/latest/
.. _virtualenv: https://pypi.python.org/pypi/virtualenv
.. _fabric: http://www.fabfile.org/
.. _atelier: http://atelier.lino-framework.org/
.. _git: http://git-scm.com/downloads

This document describes how to install Lino.  It is meant for people
who plan to write their own Lino application.  Alternativaly you might
prefer to install one of the existing Lino applications, e.g.  `Lino
Così <http://cosi.lino-framework.org/install/index.html>`__ of `Lino
Welfare <http://welfare.lino-framework.org/admin/install.html>`__.

System requirements
-------------------

- Lino still requires **Django 1.6**, we just did not yet take the
  time to make it work with newer versions. Any contribution is
  welcome.

- Lino requires **Python 2**.  Also here: we just did not yet take the
  time to make it work with Python 3. Any contribution is welcome.

- We assume you have pip_ installed. `pip` is not automatically
  bundled with Python 2, but it has become the de-facto standard.

- We recommend to use virtualenv_ (`pip install virtualenv`) and to
  activate a new environment. Something like this::

    $ virtualenv tmp
    $ . tmp/bin/activate

- You will need to install git_ on your computer to get the source
  files.


Get the sources
---------------

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
------------

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
-------------------------

When you want to see which version you have, you can say "hello" to
Lino:


.. py2rst::

    self.shell_block(["python", "-m", "lino.hello"])


The above launches Python with the `-m
<https://docs.python.org/2/using/cmdline.html#cmdoption-m>`_
command-line switch which basically instructs it to just import the
specified module :mod:`lino.hello`.

Run Lino's test suite
---------------------

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
