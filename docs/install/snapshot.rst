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


Add the Lino snapshot to your Python path
-----------------------------------------

For example on a Linux system, you can add a 
path configuration file :file:`snapshots.pth` 
to a directory that’s already on `Python’s path <http://www.python.org/doc/current/install/index.html>`_.

Here is how :file:`snapshots.pth` might look on a Debian lenny::

  # cat /usr/local/lib/python2.5/site-packages/snapshots.pth
  /var/snapshots/lino/trunk/src
  /var/snapshots/django_src  


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










