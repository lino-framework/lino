Java Howto
==========

update-java-alternatives
------------------------

::

  $ sudo update-alternatives --config java

  $ update-java-alternatives -l



  $ update-java-alternatives -l
  java-1.6.0-openjdk-i386 1061 /usr/lib/jvm/java-1.6.0-openjdk-i386
  java-1.7.0-openjdk-i386 1071 /usr/lib/jvm/java-1.7.0-openjdk-i386
  java-7-oracle 1073 /usr/lib/jvm/java-7-oracle
  $ sudo update-java-alternatives -s java-1.7.0-openjdk-i386
  update-alternatives: error: no alternatives for apt

How can I see which Java version I am using?
--------------------------------------------

::

    $ java -version
    java version "1.7.0_25"
    OpenJDK Runtime Environment (IcedTea 2.3.10) (7u25-2.3.10-1ubuntu0.13.04.2)
    OpenJDK Server VM (build 23.7-b01, mixed mode)

