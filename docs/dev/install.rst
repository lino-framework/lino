.. _lino.dev.install:

=====================================
Installing Lino (development version)
=====================================

This document describes how you should install Lino if you want
to use Lino's newest features even before they get officially 
released on PyPI, or if you possibly want to contribute to 
one of the involved software projects.

We assume you have `pip <http://www.pip-installer.org/en/latest/>`_ 
installed and your `virtualenv <https://pypi.python.org/pypi/virtualenv>`_ 
activated.

If you had previously installed Lino using `pip install lino` as described in 
:ref:`lino.tutorial.quickstart`, then you should first uninstall it using 
`pip uninstall lino`.

Create a directory (e.g. :file:`~/hgwork`) meant to hold your 
working copies of version-controlled software projects,
`cd` to that directory and and do::

  $ hg clone https://lino.googlecode.com/hg/ lino
  $ hg clone https://django-north.googlecode.com/hg/ django-north
  $ hg clone https://django-site.googlecode.com/hg/ django-site
  
(The ``hg`` command is from `Mercurial
<http://mercurial.selenic.com/wiki/QuickStart>`_. 
Run `sudo aptitude install mercurial`  if necessary.)
  
Then install these projects *as editable packages*::

  $ pip install -e lino
  $ pip install -e north
  $ pip install -e django-site
  
You will also need some other dependencies for 
which the regular pip installation will work::

  $ pip install Django Unipath Sphinx Jinja2 Babel
  
You should also install `Fabric <http://docs.fabfile.org>`_:

  $ pip install fabric 
  
Some commands you might want to run now:

Run Lino's test suite
---------------------

::

  $ cd ~/hgwork/lino
  $ fab test
  
  


