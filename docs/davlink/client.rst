=========================================
Configuring your client for using DavLink
=========================================

:ref:`davlink` launches an executable application program on your 
computer. For security reasons it is normal that the Java Runtime on 
your computer refuses this without your prior explicit permission.

The problem is that it is not always easy to give this permission.

Note that the :ref:`demos` have their 
:ref:`davlink` functionality switched off 
for security reasons (they have :attr:`use_davlink <lino.site.Site.use_davlink>` 
set to False).


Debian
======

#.  To enable Java in your browser, 
    you need to install the `icedtea-plugin` package.

#.  And then you must tell icedtea that you grant permission for 
    the DavLink applet to launch a program.    
    
    For this you must invoke `policytool
    <http://docs.oracle.com/javase/tutorial/security/tour1/wstep1.html>`_
    and add a policy entry:
    
    - codeBase: URL of the applet. 
      For example
      http://welfare-demo.lino-framework.org/media/lino/applets/DavLink.jar
      
    - add a "FilePermission" for the "<<ALL FILES>>" target and 
      the "read" action.
      
    Then save it into your "user java policy file".
    This file must be named :xfile:`.java.policy` and must be in your 
    home directory.
    If you have never used the policitool before, then you must
    type that name yourself.
    
    When done, your :xfile:`.java.policy` file should look similar to this::
    
        grant codeBase "http://welfare-demo.lino-framework.org/media/lino/applets/DavLink.jar" {
          permission java.io.FilePermission "<<ALL FILES>>", "read";
        };


If any other problems arise, 
watch your console to see what the applet wants to do.


How to see the java console of an applet
----------------------------------------

To see the Java console output, simply close all browser windows, then 
launch your browser from a command shell::

  $ firefox
  $ chromium-browser
  
Then use your browser as usual, and watch the Java console output in 
your terminal window.
 


Allowing DavLink applet to store preferences
--------------------------------------------

Currently just some notes of problems I saw and how I solved them.

The console says::

    WARNING: Couldn't flush system prefs: java.util.prefs.BackingStoreException: /etc/.java/.systemPrefs/lino create failed.
    
Reaction::    

    $ sudo mkdir /etc/.java/.systemPrefs/lino
    
Now it says::    

    WARNING: Couldn't flush system prefs: java.util.prefs.BackingStoreException: java.io.FileNotFoundException: /etc/.java/.systemPrefs/lino/prefs.tmp (Permission denied)
    
Reaction::    

    $ sudo chgrp www-data /etc/.java/.systemPrefs/lino
    $ sudo chmod g+ws /etc/.java/.systemPrefs/lino

Now that part works.    
To see what the applet wrote to your preferences::

    $ less /etc/.java/.systemPrefs/lino/davlink/prefs.xml 

Next problem is (when I try to open an URL ending with `.odt`) 
that it still says::

  java.lang.RuntimeException: No launcher defined for extension 'odt'
  
Theoretically it should find `libreoffice` automatically.

(EDIT: I don't remember for sure how I solved this. 
Maybe this was simply a bug in DavLink which is now fixed.)


Why are there infinitely many x11 subdirectories in /usr/bin/x11?
-----------------------------------------------------------------

When DavLink starts scanning a Linux client for installed launchers, 
then you see something funny::

    Searching /usr/bin
      Found /usr/bin/libreoffice
    Searching /usr/bin/X11
    Searching /usr/bin/X11/X11
    Searching /usr/bin/X11/X11/X11
    Searching /usr/bin/X11/X11/X11/X11
    Searching /usr/bin/X11/X11/X11/X11/X11
    Searching /usr/bin/X11/X11/X11/X11/X11/X11
    Searching /usr/bin/X11/X11/X11/X11/X11/X11/X11
    Searching /usr/bin/X11/X11/X11/X11/X11/X11/X11/X11
    Searching /usr/bin/X11/X11/X11/X11/X11/X11/X11/X11/X11

... and so on until about 40 occurences of the X11 subdir. 
That's surprising but does no harm. 
Explanation is here:
http://askubuntu.com/questions/191654/why-are-there-infinitely-many-x11-subdirectories-in-usr-bin-x11


How to have DavLink re-scan your system for launchers
-----------------------------------------------------

Using brute force::

  $ rm /etc/.java/.systemPrefs/lino/davlink/prefs.xml

This will later cause a warning "Prefs file removed in background 
/etc/.java/.systemPrefs/lino/davlink/prefs.xml". 


How to configure Java security policy on each client
----------------------------------------------------

(This section is obsolete)

This is rather complex. 

The following message may come on the clients when they enter 
to a Lino site which uses DavLink.
  
.. image:: not_verified.jpg
  :scale: 80
  
TODO:
Self-signed certificate: 
`Saffre-Rumma.cer <http://lino.googlecode.com/hg/docs/davlink/Saffre-Rumma.cer>`__.


Enable Java logging
-------------------

If for some reason you cannot launch your browser from command line 
to see the java console of an applet, 
then try to enable "logging" in the `IcedTea Web Control 
Panel`:

.. image:: icedtea_enable_logging.png
  :scale: 80
  
And then watch the log files::

  $ tail -f ~/.icedtea/log/java.stderr 
  $ tail -f ~/.icedtea/log/java.stdout
  $ tail -f ~/.icedtea/log/java.stderr ~/.icedtea/log/java.stdout
  $ multitail ~/.icedtea/log/java.stderr ~/.icedtea/log/java.stdout

