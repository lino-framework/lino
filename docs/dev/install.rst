.. _lino.dev.install:

================================
Installing Lino (for developers)
================================

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

- Lino requires Python 2. It is not yet converted to Python 3.
  See :ticket:`36` if you want to discuss this.

- We assume you have pip_ installed. `pip` is not automatically
  bundled with Python 2, but it has become the de-facto standard.

- We recommend to use virtualenv_ (`pip install virtualenv`) and to
  activate a new environment. Something like this::

    $ virtualenv tmp
    $ . tmp/bin/activate


Using the latest released version
---------------------------------

That said, installing Lino is easy:

.. code-block:: bash

  $ pip install lino
  Downloading/unpacking lino
  ...
  Successfully installed lino django Sphinx atelier unipath python-dateutil Babel odfpy jinja2 appy pytidylib PyYAML django-iban xlwt xlrd Pygments docutils fabric six pytz markupsafe django-countries paramiko pycrypto ecdsa
  Cleaning up...


This might take some time since it will install all dependencies.

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


Using the development version
-----------------------------

You should install the development version if you want to use Lino's
newest features before they get officially released on PyPI, or if you
possibly want to contribute to the project.



Get the sources
---------------

You will need git_ to get the source files.

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

Congratulations if you got the test suite to pass. 


