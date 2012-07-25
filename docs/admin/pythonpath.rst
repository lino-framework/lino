The Python Path
===============

A collection of things to know when setting up the 
`Python Path <http://www.python.org/doc/current/install/index.html>`_
or diagnosing problems that might be related.

See your default Python Path
----------------------------

python -c 'import sys; print sys.path'


The :xfile:`mypy` directory
---------------------------

We recommend to create directory 
:file:`~/mypy` 
(or :file:`C:\\mypy` under Windows)
where you will hold your local Python projects.
You may choose some other location, but it should be 
a name without spaces and non-ascii characters.

Then you add this directory to you Python Path by saying in 
your `.bashrc` (or whatever login script y use)::

  export PYTHONPATH = ~/mypy
  
(Under Windows you click around to find the place 
where you can define *environment variables* and define
a variable `PYTHONPATH` with the value ``C:\\mypy``).

The result is that any Python script in or below this directory 
is now available as an importable Python module. 

For example 
if you create a file :file:`~/mypy/foo.py` with the following content...

::

  def hello():
      print "Hello, world!"
      
... then you can import a module ``foo`` from any Python process, 
independently of the current directory::

  $ python
  Python 2.7.1 (r271:86832, Nov 27 2010, 18:30:46) ...
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import foo
  >>> foo.hello()
  Hello, world!
  >>> from foo import hello
  >>> hello()
  Hello, world!
  >>>

The :xfile:`local.pth` file
---------------------------
 
In your :xfile:`mypy` directory, create a file :xfile:`local.pth`, 
a plain txt file that contains a list of directories 
which Python should also add to its path.

Under Debian, this file should look like this::

  ~/snapshots/lino
  ~/snapshots/django-dev
  ~/snapshots/appy
  
Under Windows it should have the following content::

  c:\snapshots\lino
  c:\snapshots\python-dateutil
  c:\snapshots\appy
  c:\snapshots\Cheetah-2.4.4
  c:\snapshots\PyYAML-3.10\lib
  

Set the system-wide Python Path
-------------------------------

The following approach can be useful if you want to provide system users 
with a development version of Django or some other Python package.
It requires you to have root permission.

To modify the system-wide Python Path,
add the file :xfile:`local.pth` to a directory that's already on 
your Python Path:
 
=============== ==============================================
OS              Recommended directory
=============== ==============================================
Debian Lenny    :file:`/usr/local/lib/python2.5/site-packages`
Debian Squeeze  :file:`/usr/local/lib/python2.6/dist-packages`
=============== ==============================================

