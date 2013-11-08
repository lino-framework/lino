.. _eidreader.install:

Installation
-------------

Get a local copy of the repository from github, e.g. using::

  $ git clone https://github.com/lsaffre/eidreader.git
  
Download an appropriate version of :file:`eid-applet-sdk-VERSION.zip`
from the `eid-applet downloads page 
<http://code.google.com/p/eid-applet/downloads/list>`_
and extract :file:`eid-applet-service-VERSION.jar`
into a file :file:`eid-applet-service.jar` in your 
:file:`applets` directory.
For example something like::

    $ cd eidreader/applets
    $ wget http://eid-applet.googlecode.com/files/eid-applet-sdk-1.1.0.GA.zip
    $ unzip eid-applet-sdk-1.1.0.GA.zip
    $ mv eid-applet-sdk-1.1.0.GA/eid-applet-service-1.1.0.GA.jar eid-applet-service.jar
    $ rm -R eid-applet-sdk-1.1.0.GA
    

Download an appropriate version of     
`LogFactory
<http://commons.apache.org/proper/commons-logging/apidocs/org/apache/commons/logging/LogFactory.html>`_
from 
`commons.apache.org <http://commons.apache.org/proper/commons-logging/download_logging.cgi>`_
and extract a file `commons-logging.jar` from it to your `applets` directory.
For example something like::

    $ wget http://servingzone.com/mirrors/apache//commons/logging/binaries/commons-logging-1.1.3-bin.tar.gz
    $ tar -xvzf commons-logging-1.1.3-bin.tar.gz 
    $ mv commons-logging-1.1.3/commons-logging-1.1.3.jar commons-logging.jar
    $ rm -R commons-logging-1.1.3

    
Download an appropriate version of     
`commons-codec
<http://commons.apache.org/proper/commons-codec/>`_
and extract a file `commons-codec.jar` from it to your `applets` directory.


    $ wget http://servingzone.com/mirrors/apache//commons/codec/binaries/commons-codec-1.8-bin.tar.gz
    $ tar -xvzf commons-codec-1.8-bin.tar.gz 
    $ mv commons-codec-1.8/commons-codec-1.8.jar commons-codec.jar
    $ rm -R commons-codec-1.8
