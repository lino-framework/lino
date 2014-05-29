.. _lino.dev.install:

=====================================
Installing Lino (development version)
=====================================

.. _pip: http://www.pip-installer.org/en/latest/
.. _virtualenv: https://pypi.python.org/pypi/virtualenv
.. _fabric: http://www.fabfile.org/
.. _git: http://git-scm.com/downloads

This document describes how you should install Lino if you want
to use Lino's newest features even before they get officially 
released on PyPI, or if you possibly want to contribute to 
one of the involved software projects. If the instructions here sound 
too complicated, you might prefer the simple installation as 
described in :ref:`lino.tutorial.quickstart`

Preliminaries
-------------

- You will need git_ to get the source files.

- We assume you have pip_  installed.

- If you had previously installed Lino using `pip install lino` as described in 
  :ref:`lino.tutorial.quickstart`, then you should first uninstall it using 
  `pip uninstall lino`.

- We recommend to install fabric_, a command-line tool systems to
  streamline administration tasks. It's easy to install it::

     $ pip install fabric


Create a virtual Python environment
-----------------------------------

We recommend to use virtualenv_ and to activate a new
environment. Something like this::

  $ virtualenv tmp
  $ . tmp/bin/activate


Get the sources
---------------

Create a directory (e.g. :file:`~/repositories`) meant to hold your 
working copies of version-controlled software projects,
`cd` to that directory and and do::

  $ git clone https://github.com/lsaffre/atelier.git
  $ git clone https://github.com/lsaffre/djangosite.git site
  $ git clone https://github.com/lsaffre/north.git
  $ git clone https://github.com/lsaffre/lino.git
  $ git clone https://github.com/lsaffre/lino-cosi.git cosi

The second and the last lines are example for having a project whose
**local name** differs from its **public name**.  We recommend to keep
your local project names short.

You should now have 5 subdirectories called `atelier`, `site`,
`north`, `lino` and `cosi`. Each of them should contain a file
`setup.py`, a file `README.rst`, a sub-directory `docs`, and other
files and directories.


The last line installed :ref:`cosi`, one of the existing free Lino
applications. This project will serve as an example for your own Lino
application.  Alternatively or additionally to :ref:`cosi` you might
want to do the same for one or several of the out-of-the-box Lino
applications: :ref:`faggio` :ref:`welfare` :ref:`logos`

Installation
------------

Now you are ready to "install" these projects.

Commands::

  $ pip install -e atelier
  $ pip install -e site 
  $ pip install -e north
  $ pip install -e lino
  $ pip install -e cosi

Notes:

- The ``-e`` command-line switch for `pip` causes it to use the
  "development" mode.  The first argument after ``-e`` is not a
  *project name* but a *directory*.  Development mode means that these
  modules run "directly from source".  `pip` does not *copy* the
  sources to your Python `site_packages`, but instead adds a link to
  them.

- Alternatively (without pip_) you could have done::

      $ cd atelier ; python setup.py develop ; cd ..
      $ cd site ; python setup.py develop ; cd ..
      ...


Run Lino's test suite
---------------------

The following commands are not strictly necessary, but they are a
useful check to see whether everything worked well.

- First we install some more recommended Python modules::

     $ pip install reportlab
     $ pip install pisa

- And here we go for the test suite::

    $ cd ~/repositories/lino
    $ fab initdb
    $ fab test

- The :fab:`initdb` command initializes the demo databases. These are
  used by the test suite which would fail if these demo databases were
  missing.
- The :fab:`test` command simply runs the test suite, it is a short
  for ``python setup.py test``


Continue here: :ref:`lino.tutorial.quickstart`
