Other Software used by Lino
===========================

Lino uses a series of other free Python packages which you may have to
install on your system.  Install them only if you get any related
error messages, because the following list may not be perfectly
up-to-date.

.. module:: django

- :mod:`django` means `Django <http://www.djangoproject.com/>`_

  
  
- Dirk Holtwick's `xhtml2pdf <http://www.xhtml2pdf.com/>`_ module.

- `Reportlab Toolkit <http://www.reportlab.org/>`_

- `Python Imaging Library <http://www.pythonware.com/products/pil/>`_

- `docutils <http://docutils.sourceforge.net/>`_

.. module:: win32

- :mod:`win32` means 
  Mark Hammond's 
  `Python Extensions for Windows
  <http://starship.python.net/crew/mhammond/>`_

The following are probably not necessary:

- `PySQLite <http://pysqlite.sourceforge.net/>`_
  
- `Twisted <http://www.twistedmatrix.com/>`_

- `wxPython <http://www.wxpython.org/>`_

- `Medusa <http://www.amk.ca/python/code/medusa.html>`_ web server.

- `Quixote <http://www.mems-exchange.org/software/quixote/>`_


Test whether it worked
----------------------

To test whether Lino is functional, `cd` 
to your :srcref:`src/mysites/demo` directory and run::

  python manage.py test 
  

Create a `lino` script
----------------------

If you are going to use one of the command-line tools, then you should
create somewhere on your system a shell script :xfile:`lino` with just
one line::

  @python -c "from lino import runscript" %*










