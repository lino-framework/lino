===================
Get a Lino snapshot
===================

Short instructions:

- Create a new directory (e.g. :file:`/var/snapshots/lino/`) 

- In a command shell, run::

     svn checkout svn://svn.berlios.de/lino/trunk
  
- Don't run :file:`setup.py`, it is not necessary and doesn't work.  

- Add :file:`/var/snapshots/lino/trunk/src` to your Python path.
  

If that was too short, then here is a longer version.
And don't hesitate to contact me if you get stucked.


About SVN: see :doc:`topics/svn`.


Add lino to your Python path
----------------------------

For example on a Linux system, edit your :file:`sitecustomize.py`::

  import site
  site.addsitedir("/var/snapshots/lino/trunk/src")


Updating your Lino to the newest version
----------------------------------------

Go to the directory containing your local copy and type the command::

  cd /var/snapshots/lino/trunk
  svn update 


Install other Python packages
-----------------------------

Lino uses a series of other free Python packages which you may have to
install on your system.  Install them only if you get any related
error messages, because the following list may not be perfectly
up-to-date.

- `Django <http://www.djangoproject.com/>`_
  
- Dirk Holtwick's `xhtml2pdf <http://www.xhtml2pdf.com/>`_ module.

- `Reportlab Toolkit <http://www.reportlab.org/>`_

- `Python Imaging Library <http://www.pythonware.com/products/pil/>`_

- `docutils <http://docutils.sourceforge.net/>`_

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










