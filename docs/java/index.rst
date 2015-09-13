.. _lino.java:

=============
Lino and Java
=============

Some Lino applications (e.g. :ref:`welfare`) uses plugins
that require two Java applets:

- :mod:`lino.modlib.beid` is for reading Belgian eId cards
- :mod:`lino.modlib.davlink` is to provide possibility to edit
  printable documents on a server with :doc:`/admin/webdav`.

You can easily disable these functionalities by setting
:attr:`use_java <lino.core.site.Site.use_java>` to `False` in your
:xfile:`djangosite_local.py`.

Java cheat sheet
================

When using Java applets, you might encounter problems due to Java's
security system.

.. note:: 

   Warning: This is just a cheat sheet! 
   Don't use it without understanding what a command does. 

update-java-alternatives
------------------------

::

  $ sudo update-alternatives --config java

  $ update-java-alternatives -l
  java-1.6.0-openjdk-i386 1061 /usr/lib/jvm/java-1.6.0-openjdk-i386
  java-1.7.0-openjdk-i386 1071 /usr/lib/jvm/java-1.7.0-openjdk-i386
  java-7-oracle 1073 /usr/lib/jvm/java-7-oracle

  $ sudo update-java-alternatives -s java-1.7.0-openjdk-i386
  update-alternatives: error: no alternatives for apt

How can I see which Java version I am using?
--------------------------------------------

Simply run it::

    $ java -version

OpenJDK Java will answer::

    java version "1.7.0_25"
    OpenJDK Runtime Environment (IcedTea 2.3.10) (7u25-2.3.10-1ubuntu0.13.04.2)
    OpenJDK Server VM (build 23.7-b01, mixed mode)

Oracle Java will answer::

    java version "1.7.0_45"
    Java(TM) SE Runtime Environment (build 1.7.0_45-b18)
    Java HotSpot(TM) Server VM (build 24.45-b08, mixed mode)



How to generate a self-signed key
---------------------------------

::

 $ keytool -genkey
 $ keytool -selfcert
 $ keytool -list



How to get rid of "update-alternatives: error: no alternatives for apt"
-----------------------------------------------------------------------

This error can have multiple explanations.
On :blogref:`20140211` I solved this by removing and reinstalling Java...


.. _java.flush:

How to flush the Java cache?
----------------------------

- On Debian/Ubuntu, simply do::

      $ javaws -Xclearcache
  
  You can also launch the IcedTea Web Control Panel and inspect your
  cache, disable caching alltogether and other thing. But I didn't
  manage to delete individual entries (Ubuntu 13.10).
