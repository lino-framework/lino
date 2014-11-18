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
one of the involved software projects. 


Preliminaries
-------------

- Lino requires Python 2. It is not yet converted to Python 3.  See
  :doc:`/tickets/117` if you want to discuss this.

- You will need git_ to get the source files.

- We assume you have pip_ installed.

- We recommend to use virtualenv_ and to activate a new
  environment. Something like this::

    $ virtualenv tmp
    $ . tmp/bin/activate

Get the sources
---------------

Create a directory (e.g. :file:`~/repositories`) meant to hold your 
working copies of version-controlled software projects,
`cd` to that directory and and do::

  $ git clone https://github.com/lsaffre/atelier.git
  $ git clone https://github.com/lsaffre/djangosite.git
  $ git clone https://github.com/lsaffre/north.git
  $ git clone https://github.com/lsaffre/lino.git

You should now have 4 subdirectories called `atelier`, `djangosite`,
`north`, `lino`. Each of them should contain a file :xfile:`setup.py`,
a file :xfile:`README.rst` and a whole tree of other files and
directories.

Installation
------------

Now you are ready to "install" these projects, i.e. to tell your
Python interpreter where they are, so that you can import them from
within any Python program.

Commands::

  $ pip install -e atelier
  $ pip install -e djangosite 
  $ pip install -e north
  $ pip install -e lino

Notes:

- The ``-e`` command-line switch for `pip` causes it to use the
  "development" mode.  The first argument after ``-e`` is not a
  *project name* but a *directory*.  Development mode means that these
  modules run "directly from source".  `pip` does not *copy* the
  sources to your Python `site_packages`, but instead adds a link to
  them.

- Alternatively (without pip_) you could have done::

      $ cd atelier ; python setup.py develop ; cd ..
      $ cd djangosite ; python setup.py develop ; cd ..
      ...


Run Lino's test suite
---------------------

The following commands are a recommended check to see whether
everything worked well.

- First we install some more Python modules needed by the test suite::

     $ pip install fabric
     $ pip install html5lib
     $ pip install 'reportlab==2.7'
     $ pip install pisa
     $ pip install django-iban
     $ pip install pytidylib

  fabric_ is a command-line tool systems to streamline administration tasks. 

  pisa complains that "Reportlab Version 2.1+ is needed!" with
  reportlab 3, so we install 2.7 (the latest 2.x version)

- And here we go for the test suite::

    $ cd ~/repositories/lino
    $ fab initdb
    $ fab test

- The :cmd:`fab initdb` command initializes the demo databases. These
  are used by the test suite which would fail if these demo databases
  were missing.

- The :cmd:`fab test` command simply runs the test suite, it is a short
  for ``python setup.py test``


Where to go from here 
---------------------

- :ref:`lino.tutorial.hello`

- :ref:`Lino Polls tutorial <lino.tutorial.polls>` 

- Install one or several of the out-of-the-box Lino
  applications: :ref:`cosi`, :ref:`faggio`, :ref:`welfare` or
  :ref:`logos`

