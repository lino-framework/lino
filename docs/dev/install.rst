.. _lino.dev.install:

=====================================
Installing Lino (development version)
=====================================

This document describes how you should install Lino if you want
to use Lino's newest features even before they get officially 
released on PyPI, or if you possibly want to contribute to 
one of the involved software projects. If the instructions here sound 
too complicated, you might prefer the simple installation as 
described in :ref:`lino.tutorial.quickstart`

We assume you have `pip <http://www.pip-installer.org/en/latest/>`_ 
installed and your `virtualenv <https://pypi.python.org/pypi/virtualenv>`_ 
activated.

If you had previously installed Lino using `pip install lino` as described in 
:ref:`lino.tutorial.quickstart`, then you should first uninstall it using 
`pip uninstall lino`.

Create a directory (e.g. :file:`~/repositories`) meant to hold your 
working copies of version-controlled software projects,
`cd` to that directory and and do::

  $ git clone https://github.com/lsaffre/atelier.git
  $ git clone https://github.com/lsaffre/djangosite.git
  $ git clone https://github.com/lsaffre/north.git
  $ git clone https://github.com/lsaffre/lino.git
  
Then install these projects *as editable packages*::

  $ pip install -e atelier
  $ pip install -e djangosite
  $ pip install -e north
  $ pip install -e lino
  
Some commands you might want to run now:

Run Lino's test suite
---------------------

::

  $ cd ~/repositories/lino
  $ fab test
  
  
Updating your copy of the repository
------------------------------------

To update your copy of the repositories, go to 
your :file:`~/repositories` directory and type::

  $ git pull atelier
  $ git pull djangosite
  $ git pull north
  $ git pull lino
  
