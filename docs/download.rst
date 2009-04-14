=============
Download Lino
=============


The only possibly useful thing to download here is the TIM Tools installer for Win32.
There are `Installation instructions <http://tim.saffre-rumma.ee/timtools.html>`_ 
in German for the TIM Tools.

If you want to discover what Lino is, then we rather recommended to 
get an SVN snapshot.


Install a SVN client
--------------------

You'll need an SVN client on your computer. 
For most Windows user I recommend 
`TortoiseCVS <http://tortoisecvs.sourceforge.net/>`_.

If you want to know more about accessing a CVS repository, see the
general SourceForge documentation:
http://sourceforge.net/cvs/?group_id=87016

More about SVN

- Subversion project homepage::
  http://subversion.tigris.org/

- Article "The Subversion Project: Building a Better CVS"
  http://www.linuxjournal.com/article.php?sid=4768
  
- Online book "Version Control with Subversion":
  http://svnbook.red-bean.com/


Get an SVN snapshot
-------------------

Once Lino is installed, you can always download the latest snapshot to get the latest fixes. This is currently the only method since it is too early to work with official releases.

First-time installation

   1. Checkout from anonymous SVN
   
      For example on a Linux system to :file:`/var/snapshots/lino`::

        mkdir /var/snapshots
        mkdir /var/snapshots/lino
        cd /var/snapshots/lino
        svn checkout svn://svn.berlios.de/lino/trunk

   2. Add lino to your Python path.

      For example on a Linux system, edit your file
      :file:`/usr/local/lib/python2.x/site-packages/sitecustomize.py`:

      import site
      site.addsitedir("/var/snapshots/lino/trunk/src")
      #from lino.console import sitecustomize

   3. Create the 'lino' launcher script::

      echo 'python -c "import lino.runscript" $*' > /usr/local/bin/lino
      chmod a+x /usr/local/bin/lino

   4. run the test suite::

      cd /var/snapshots/lino/trunk/tests
      lino runtests

Updating your Lino to the most recent version
---------------------------------------------

Go to the directory containing your local copy and type the command::

  cd /var/snapshots/lino/trunk
  svn update 

Configuring your SVN client on Windows
--------------------------------------

Because your Python will probably create :file:`*.pyc` files in your local 
work copy, you should tell SVN to ignore them. Here is how to do it::

  cd %APPDATA%\Subversion
  edit config

  [miscellany]
  ### Set global-ignores to a set of whitespace-delimited globs
  ### which Subversion will ignore in its 'status' output, and
  ### while importing or adding files and directories.
  global-ignores = *.o *.lo *.la #*# .*.rej *.rej .*~*~.#* .DS_Store *.pyc









