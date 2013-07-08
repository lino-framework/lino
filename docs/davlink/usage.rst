How to use DavLink
==================

This document is for people who want to use the 
:doc:`DavLink <index>` applet **without Lino**.

A Lino application will automatically do everything described here
when you set :attr:`use_davlink <lino.ui.Site.use_davlink>` 
to `True` in your :file:`settings.py`.

Basically you need to:

- Download `DavLink.jar
  <http://lino.googlecode.com/hg/lino/media/applets/DavLink.jar>` 
  and make it available on your web server.
  
- Include the applet in your web page, using some code like::

            <applet name="DavLink" code="davlink.DavLink.class"
                    archive="url/to/DavLink.jar"
                    width="1" height="1"></applet>

- Launch the applet using JavaScript code like::

     document.applets.DavLink.open(webdavURL);

- :doc:` client`


Compile the `.java` file into a signed `.jar` file
--------------------------------------------------

`DavLink.jar
  <http://lino.googlecode.com/hg/lino/media/applets/DavLink.jar>` 
is a self-signed archive which expires after 6 months. 
In case you use some Lino version for more than 6 months, 
you can re-build it yourself a new self-signed .jar file.

On a Debian machine::

  $ cd ~/hgwork/lino/java
  $ make 
  
This requires a key named "mykey" in your keystore, and will 
ask you for the passphrase of that key.
So you'll have to create that key on your machine before you 
do the above for the first time::

  $ keytool -list
  $ keytool -genkey
  $ keytool -selfcert
  $ keytool -list
  
You also need some Java SDK. 
The easiest way to install one is::
  
  $ sudo aptitude install default-jdk
  

