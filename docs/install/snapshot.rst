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


About SVN: see :doc:`../topics/svn`.


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










