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
:file:`/home/lsaffre/mypy` 
(:file:`C:\\mypy` under Windows)
where you will hold your local Python projects.
You may choose some other location, but it should be 
a name without spaces and non-ascii characters.

Then you add this directory to you Python Path by saying::

  export PYTHONPATH = /home/lsaffre/mypy
  
(or under Windows by clicking around to find the place 
where you can define environment variables and defining 
a variable `PYTHONPATH` with the value ``C:\\mypy``).
 
In your :xfile:`mypy` directory, create a file :xfile:`local.pth`, 
a plain txt file that contains simply a list of directories 
which Python should also add to its path.

Under Debian, this file should look like this::

  /home/lsaffre/snapshots/lino
  /home/lsaffre/snapshots/django-dev
  /home/lsaffre/snapshots/appy
  
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

