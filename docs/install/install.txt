---------------
Installing Lino
---------------

.. include:: ../_header.txt

.. contents:: 


Before installing
-----------------

Lino is in an early development stage.  And especially the release
procedure through Internet is almost untested and will certainly not
work out of the box.  But don't give up, there is hope: you can get
free support from the project's author!  So if you get locked, send me
an e-mail, describing your problem.  I will do my best to help you.


Install Python
--------------

If you don't already have Python on your computer, download and
install the latest official version from

   http://www.python.org/2.3.3/

On Windows you can simply download and execute a binary installer:

   http://www.python.org/ftp/python/2.3.3/Python-2.3.3c1.exe


Download Lino
-------------

See `Downloading Lino <download.html>`_.


Add Lino to your Python path
----------------------------

Basically you just add the `src` directory of your local copy (that is
``c:\snapshot\lino\lino\src``) to your computer's Python path.

For most Windows users it will be easiest to define an environment
variable ``PYTHONPATH`` with the value ``C:\snapshots\lino\lino\src``
(if you checked out Lino to ``c:\snapshots\lino``).


Or, on a Debian system you can create a file
`/usr/lib/site-python/sitecustomize.py` containing the following::

    import site
    site.addsitedir("/opt/lino/src")

Or you just set the PYTHONPATH environment variable to
`/opt/lino/src`.


.. warning:: (If you are used to install Python modules:) Don't run
	the file :fileref:`setup.py` as usual.  It won't work.  And anyway,
	simply adding the Lino source tree to your PYTHONPATH is more
	appropriate to the current development status.



..

  On my Windows computer I use a combination of both: I created
  `sitecustomize.py` in `s:\py-site-packages` which is a directory
  where I install site-specific pure Python packages independently of
  the installed Python version. Now I simply do::

    SET PYTHONPATH=s:/py-site-packages
	 

Install other Python packages
-----------------------------

Lino uses a series of other free Python packages which you may have to
install on your system.  Install them only if you get any related
error messages, because the following list may not be perfectly
up-to-date.

- `ReportLab Toolkit <http://www.reportlab.org>`_

- `Python Imaging Library <http://www.pythonware.com/products/pil/>`_

- `PySQLite <http://pysqlite.sourceforge.net/>`_
  
- `docutils <http://docutils.sourceforge.net/>`_

- `Twisted <http://www.twistedmatrix.com/>`_

- `wxPython <http://www.wxpython.org/>`_

- `Medusa <http://www.amk.ca/python/code/medusa.html>`_ web server.

- `Quixote <http://www.mems-exchange.org/software/quixote/>`_


(Debian) : check that `python-dev` and `python-sqlite`packages are
installed. They contain the `distutils` and `sqlite` modules.

.. 
	- `PyCrypto <http://www.amk.ca/python/code/crypto.html>`_ :
	  Python Cryptography Toolkit 

   - `empy <http://www.alcyone.com/pyos/empy>`_
	- `WebWare <http://webware.sourceforge.net/>`_


	 
Test whether it worked
----------------------

To test whether Lino is functional, `cd` to the directory containing
your local copy and type::

    python make.py


The output of this should be something like::

	Generating docs...
	Loading WebMan module from C:\snapshots\lino\docs...
	Loading WebMan module from C:\snapshots\lino\docs\diary...
	Loading WebMan module from C:\snapshots\lino\docs\pds...
	Processing docs\scripts.html...
	Processing docs\index.html...
	...
	Processing docs\pds\index.html...
	Processing docs\pds\examples.html...
	Running unittest on test/ ...
			  collecting cases in tests\adamo
			  collecting cases in tests\etc
			  collecting cases in tests\reporter
	..................................
	---------------------------------------------------------------
	Ran 35 tests in 33.819s

	OK
	Running doctest on ['lino.adamo', 'lino.sdoc'] ...
	Running doctest on docs/ ...		  


It is probable that many things won't work.  You will probably see
some typical Python error messages, something like::

  Traceback (most recent call last):
	 File "c:\snapshots\lino\src\lino\webman\xdocutils.py", line 58, in exec


This is normal.  Don't give up.  In fact you are very close.  Just
tell me these messages.


Create a `lino` script
----------------------

Currently you must then manually create a file `lino.bat` (on Windows)
somewhere in your PATH, which does something like::

	@echo off
	if x%1 == x goto usage
	python c:\snapshots\lino\lino\scripts\%1.py %2 %3 %4 %5
	if not errorlevel 1 goto ok
	echo Something went wrong...
	pause
	goto ok
	:usage
	echo USAGE : lino CMD params
	echo Where CMD is one of prn2pdf, pds2pdf, sendmail, openurl, ...
	goto ok
	:ok

The basic idea of this approach is that one can execute the Lino
scripts easily from anywhere, without copying them to some other place
on your computer.  The file `lino.bat` (or a similar shell script on a
UNIX system) should be the only connection point.

	 




	 
