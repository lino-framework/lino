.. _lino.dev.install:

=====================================
Installing Lino (development version)
=====================================

.. _pip: http://www.pip-installer.org/en/latest/
.. _virtualenv: https://pypi.python.org/pypi/virtualenv
.. _fabric: http://www.fabfile.org/
.. _atelier: http://atelier.lino-framework.org/
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

- We assume you have pip_ installed. `pip` is not automatically
  bundled with Python 2, but it has become the de-facto standard.

- We recommend to use virtualenv_ (`pip install virtualenv`) and to
  activate a new environment. Something like this::

    $ virtualenv tmp
    $ . tmp/bin/activate


Get the sources
---------------

Create a directory (e.g. :file:`~/repositories`) meant to hold your
working copies of version-controlled software projects, `cd` to that
directory and and do::

  $ git clone https://github.com/lsaffre/lino.git

You should now have a subdirectory called `lino`, which contains a
file :xfile:`setup.py`, a file :xfile:`README.rst` and a whole tree of
other files and directories.

Installation
------------

Now you are ready to "install" Lino, i.e. to tell your Python
interpreter where the source file are, so that you can import them
from within any Python program.

Commands::

  $ pip install -e lino

Notes:

- The ``-e`` command-line switch for `pip` causes it to use the
  "development" mode.  Development mode means that these modules run
  "directly from source".  `pip` does not *copy* the sources to your
  Python `site_packages`, but instead adds a link to them.  The first
  argument after ``-e`` is not a *project name* but a *directory*.

- Alternatively (without pip_) you could have done::

      $ cd lino ; python setup.py develop ; cd ..


Run Lino's test suite
---------------------

In order to check to see whether everything worked well, we are now
going to run the test suite.  

And before running the test suite, we must initialize the **demo
databases** because the test suite has many test cases which would
fail if these demo databases were missing or not in their virgin
state.

The easiest way to initialize the demo databases is to run the
:cmd:`fab initdb` command.  Which requires atelier_ (my personal
collection of general Pyton utilities).

So we must do::

    $ pip install atelier
    $ cd ~/repositories/lino
    $ fab initdb

And here we go for the test suite itself::

    $ cd ~/repositories/lino
    $ fab test

  The :cmd:`fab test` command simply runs the test suite, it is a short
  for ``python setup.py test``


Where to go from here 
---------------------

Congratulations if you got the test suite to pass. Here are some more
*suggestions du chef* for getting acquaintaned with Lino:

- :ref:`lino.tutorial.hello`

- :ref:`Lino Polls tutorial <lino.tutorial.polls>` 

- Install one or several of the out-of-the-box Lino
  applications: :ref:`cosi`, :ref:`faggio`, :ref:`welfare` or
  :ref:`logos`

