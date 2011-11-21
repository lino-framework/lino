Install OpenOffice.org server 
=============================

See also :doc:`/blog/2010/1116`. But basically:

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

    
- Install the startup script::

    # cp /var/snapshots/lino/bash/oood /etc/init.d
    # chmod 755 /etc/init.d/oood
    # nano /etc/init.d/oood
    
    
  Check the value of the `SOFFICE` environment variable::
  
    SOFFICE=/usr/lib/openoffice/program/soffice  
  
  Finally, run ``update-rc.d`` to have the daemon 
  automatically start when the server boots::

    # update-rc.d oood defaults
    
    
- In your local :xfile:`settings.py`::


