Install OpenOffice.org server
=============================

.. rubric:: Cheat sheet

You must install `python3-uno` package::

  $ sudo aptitude install python3-uno

and then set your :attr:`appy_params
<lino.core.site.Site.appy_params>` to point to your `python3`
executable, e.g. by specifying in your :xfile:`settings.py`::

  SITE.appy_params.update(pythonWithUnoPath='/usr/bin/python3')


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

   
- Install the startup script::

    $ sudo cp /var/snapshots/lino/bash/openoffice-headless /etc/init.d
    $ sudo chmod 755 /etc/init.d/openoffice-headless
    $ sudo nano /etc/init.d/openoffice-headless
    
  Check the value of the `OFFICE_PATH` environment variable::
  
    OFFICE_PATH=/usr/lib/libreoffice
    OFFICE_PATH=/usr/lib/openoffice/program/soffice  
  
- Finally, run ``update-rc.d`` to have the daemon 
  automatically start when the server boots::

    $ sudo update-rc.d openoffice-headless defaults
    
    


