About SVN
=========

Install an SVN client
---------------------

You'll need an SVN client on your computer. 
For most Windows user I recommend 
`TortoiseCVS <http://tortoisecvs.sourceforge.net/>`_.

If you want to know more about accessing a CVS repository, see the
general SourceForge documentation:
http://sourceforge.net/cvs/?group_id=87016



Configuring your SVN client on Windows
--------------------------------------

Because your Python will probably create :xfile:`*.pyc` files in your local 
work copy, you should tell SVN to ignore them. Here is how to do it::

  cd %APPDATA%\Subversion
  edit config

  [miscellany]
  ### Set global-ignores to a set of whitespace-delimited globs
  ### which Subversion will ignore in its 'status' output, and
  ### while importing or adding files and directories.
  global-ignores = *.o *.lo *.la #*# .*.rej *.rej .*~ *~ .#* .DS_Store *.pyc *.pyo *.dpyc
  
(:xfile:`*.dpyc` files are compiled :xfile:`*.dpy` files and will be created if you use :mod:`lino.django.utils.dpyserializer`.)



More about Subversion
---------------------

- Subversion project homepage::
  http://subversion.tigris.org/

- Article "The Subversion Project: Building a Better CVS"
  http://www.linuxjournal.com/article.php?sid=4768
  
- Online book "Version Control with Subversion":
  http://svnbook.red-bean.com/







