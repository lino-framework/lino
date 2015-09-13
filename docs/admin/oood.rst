.. _admin.oood:

==============================
Installing LibreOffice and UNO
==============================

When your Lino applicaton uses :mod:`lino.modlib.appypod`, then you
need to have a LibreOffice server running so that the users of your
site can print documents.

:mod:`lino.modlib.appypod` uses `appy.pod
<http://appyframework.org/pod.html>`_ which in turn uses `python3-uno
<https://packages.debian.org/de/sid/python3-uno>`__ to connect to a
`LibreOffice` server.

`appy.pod` is a Python package and was automatically installed
together with Lino into your Python environment.  But `libreoffice`
and `python3-uno` must be installed by the system administrator using
something like this::

  $ sudo aptitude install libreoffice python3-uno

Starting the LibreOffice server
===============================

Then you need to run a LO server. For occasional or experimental use
you can fire it up using something like this::

  $ libreoffice '--accept=socket,host=127.0.0.1,port=8100;urp;' &

For regular usage you will want to use a startup script.  Vic
Vijayakumar has written such a script, and for convenience the Lino
repository contains a copy of it :file:`/bash/openoffice-headless`.

- Install the startup script::

    $ sudo cp ~/repositories/lino/bash/openoffice-headless /etc/init.d
    $ sudo chmod 755 /etc/init.d/openoffice-headless
    $ sudo nano /etc/init.d/openoffice-headless
    
- Check the value of the `OFFICE_PATH` environment variable::
  
    OFFICE_PATH=/usr/lib/libreoffice
    OFFICE_PATH=/usr/lib/openoffice/program/soffice  
  
- Finally, run ``update-rc.d`` to have the daemon 
  automatically start when the server boots::

    $ sudo update-rc.d openoffice-headless defaults
    

Setting ``appy_params``
=======================

And then you must set your :attr:`appy_params
<lino.core.site.Site.appy_params>` to point to your `python3`
executable, e.g. by specifying in your :xfile:`settings.py`::

  SITE.appy_params.update(pythonWithUnoPath='/usr/bin/python3')

This is because Lino needs Python **2** while `python-uno` needs
Python **3**.  To resolve that conflict, `appy.pod` has this
configuration option which causes it to run its UNO call in a
subprocess with Python 3.

If you don't want to do this again and again for every Lino site on
your machine, then you should put this to your
:xfile:`djangosite_local.py` file



.. rubric:: The following is probably obsolete


See also :srcref:`/docs/blog/2010/1116`. But basically:

- Install a headless version > 2.3 of openoffice or libreoffice::
    
    # aptitude install openoffice.org-headless openoffice.org-writer python-openoffice
    # aptitude install openoffice.org-java-common java-virtual-machine
    
  Check whether everything is correct:
  
    $ python /usr/share/doc/python-openoffice/examples/check-installation
    
  This should output something like::
  
    Starting OOo for listening on pipe,name=uno387349758964
    Will use command ('/usr/lib/openoffice/program/soffice', '-headless', '-norestore', '-accept=pipe,name=uno387349758964;urp;')
    Started OOo with process id 5216

    Now trying to connect to OOo.
    Connecting with context pyuno object (com.sun.star.uno.XInterface)0xa36b354{, supportedInterfaces={com.sun.star.uno.XComponentContext,com.sun.star.container.XNameContainer,com.sun.star.lang.XTypeProvider,com.sun.star.uno.XWeak,com.sun.star.lang.XComponent}}

    Looks good.  

   
