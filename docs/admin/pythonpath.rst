The Python Path
===============

A collection of things to know when setting up the 
`Python Path <http://www.python.org/doc/current/install/index.html>`_
or diagnosing problems that might be related.

See your default Python Path
----------------------------

python -c 'import sys; print sys.path'

Set the system-wide Python Path
-------------------------------

The following approach can be useful if you want to provide system users 
with a development version of Django or some other Python package.
It requires you to have root permission.

Add a path configuration file :xfile:`local.pth` 
Python Pathto a directory that's already on your 
. 
 
=============== ==============================================
OS              Recommended directory
=============== ==============================================
Debian Lenny    :file:`/usr/local/lib/python2.5/site-packages`
Debian Squeeze  :file:`/usr/local/lib/python2.6/dist-packages`
=============== ==============================================

The file :xfile:`local.pth` itself should contain a list of directories 
to add to the system-wide Python Path, e.g.::

  /var/snapshots/django-dev
  /var/snapshots/appy
  /usr/local/django  
  

