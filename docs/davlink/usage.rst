How to use DavLink
==================

This document is for people who want to use the :ref:`davlink` applet
**without Lino**.  A Lino application will automatically do everything
described here when you set :attr:`use_davlink <ad.Site.use_davlink>`
to `True` in your :xfile:`settings.py`.

Trying it using a self-signed certificate
-----------------------------------------

Basically you need to:

- Download `DavLink.jar
  <https://github.com/lsaffre/davlink/blob/master/example/DavLink.jar?raw=true>`_
  and make it available on your web server.
  
- Include the applet in your web page, using some code like::

    <applet name="DavLink" code="davlink.DavLink.class"
            archive="url/to/DavLink.jar"
            width="1" height="1"></applet>

- Launch the applet using JavaScript code like::

     document.applets.DavLink.open("http://example.com/davlink/test.odt");

- :doc:`client`

- Set up a web server with WebDAV enabled.


Compile the `.java` file into a signed `.jar` file
--------------------------------------------------

The :file:`DavLink.jar` file from the previous section is a
self-signed archive which expires after 6 months.  In a production
environment you must build and sign the `.jar` file yourself.

You can re-build it using your own self-signed `.jar` file.

On a Debian machine::

    $ cd ~/repositories/davlink
    $ make jars_mykey

The output should be something like::

    jar cvmf Manifest.txt example/DavLink.jar davlink
    added manifest
    adding: davlink/(in = 0) (out= 0)(stored 0%)
    adding: davlink/DavLink.class(in = 4500) (out= 2343)(deflated 47%)
    adding: davlink/DavLink$2.class(in = 3866) (out= 2215)(deflated 42%)
    adding: davlink/DavLink.java(in = 15036) (out= 3997)(deflated 73%)
    adding: davlink/DavLink$1.class(in = 647) (out= 428)(deflated 33%)
    adding: davlink/DavLink$3.class(in = 1406) (out= 777)(deflated 44%)
    adding: davlink/Launcher.class(in = 295) (out= 229)(deflated 22%)
    adding: davlink/Searcher.class(in = 1780) (out= 1014)(deflated 43%)
    adding: davlink/DocType.class(in = 605) (out= 381)(deflated 37%)
    adding: davlink/DavLink.java~(in = 15032) (out= 4004)(deflated 73%)
    jarsigner example/DavLink.jar mykey
    Enter Passphrase for keystore: 
    jar signed.

    Warning: 
    The signer certificate will expire within six months.
    No -tsa or -tsacert is provided and this jar is not
    timestamped. Without a timestamp, users may not be able to
    validate this jar after the signer certificate's expiration date
    (2014-08-25) or after any future revocation date.

This requires a key named "mykey" in your keystore, and will ask you
for the passphrase of that key.  So you'll have to create that key on
your machine before you do the above for the first time.  Here is a
short cheat sheet for working with keytool::

  $ keytool -list
  $ keytool -genkey
  $ keytool -selfcert
  $ keytool -delete -alias mykey

If you don't have any ``keytool`` command, then you probably just need
some Java SDK.  The easiest way to install one is::
  
  $ sudo aptitude install default-jdk
  

