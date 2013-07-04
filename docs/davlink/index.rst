DavLink
=======

DavLink is an applet that 
launches the client's desktop's office application,
passing it the URL of a webdav file 
as command line argument.

It is actively being used since 2011 as a solution for 
:doc:`/tickets/45`.

It is published and maintained by the author 
as a part of the Lino project.

Supported Office suites: Microsoft, OpenOffice, LibreOffice

Supported client platforms: Windows, Unix

.. toctree::
   :maxdepth: 2

   usage
   client

  
Thanks to 
---------
  
- `FilenameFilter
  <http://bruce-eckel.developpez.com/livres/java/traduction/tij2/?chap=12&page=0>`_
  
- `Inspiration for traversal()
  <http://vafer.org/blog/20071112204524/>`_
  
  Methods with variable arguments:
  http://today.java.net/pub/a/today/2004/04/19/varargs.html
  
  List all the drives ("roots paths") on Windows:
  http://msdn.microsoft.com/en-us/library/aa988512(v=vs.80).aspx
  
  Recursive file listing
  http://www.javapractices.com/topic/TopicAction.do?Id=68

  Preferences API
  http://download.oracle.com/javase/1.5.0/docs/api/java/util/prefs/Preferences.html
  
  API for Java SE:
  http://download.oracle.com/javase/6/docs/api/
  
Alternatives
------------

- Element IT's `OfficeOpen control
  <http://www.element-it.com/online-edit-in-openoffice-and-microsoft-office.aspx>`_
  
- WebDAV Launcher

.. image:: WebDAV_Launcher.jpg
  :scale: 80
  



