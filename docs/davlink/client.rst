=========================================
Configuring your client for using DavLink
=========================================

:ref:`davlink` launches an executable application program on your 
computer.For security reasons it is normal that the Java Runtime on 
your computer refuses this without your prior explicit permission.

The only problem is that it is not always easy to give this permission.

Debian
======


How to see the java console of an applet
----------------------------------------

So the simple answer is *one of the following*::

  $ tail -f ~/.icedtea/log/java.stderr 
  $ tail -f ~/.icedtea/log/java.stdout
  $ tail -f ~/.icedtea/log/java.stderr ~/.icedtea/log/java.stdout
  $ multitail ~/.icedtea/log/java.stderr ~/.icedtea/log/java.stdout
  
  
How to have DavLink re-scan your system for launchers
-----------------------------------------------------

Using brute force::

  $ rm /etc/.java/.systemPrefs/lino/davlink/prefs.xml

This will later cause a warning "Prefs file removed in background 
/etc/.java/.systemPrefs/lino/davlink/prefs.xml". 


Why are there infinitely many x11 subdirectories in /usr/bin/x11?
-----------------------------------------------------------------

When scanning a Linux client for installed launchers, you see something funny::

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

... and so on until about 40 occurences the X11 subdir. 
That's surprising but does no harm. 
Explanation is here:
http://askubuntu.com/questions/191654/why-are-there-infinitely-many-x11-subdirectories-in-usr-bin-x11


Allowing DavLink applet to store preferences
--------------------------------------------

Now that I can finally read the Java console, I can start with 
some real problem: DavLink obviously doesn't yet work when it 
is being used from a Linux client.
Let's get that running.

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
that it still says "java.lang.RuntimeException: 
No launcher defined for extension 'odt'".
Theoretically it should find `libreoffice` automatically.




How to configure Java security policy on each client
----------------------------------------------------

This is rather complex. 

The following message may come on the clients when they enter 
to a Lino site which uses DavLink.
  
.. image:: not_verified.jpg
  :scale: 80
  
TODO:
Self-signed certificate: 
`Saffre-Rumma.cer <http://lino.googlecode.com/hg/docs/davlink/Saffre-Rumma.cer>`__.



