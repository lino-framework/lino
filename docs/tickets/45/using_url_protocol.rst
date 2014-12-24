Using a custom URL protocol
---------------------------

- `We need a webdav:// URL scheme!
  <http://kartik-log.blogspot.com/2006/01/we-need-webdav-url-scheme.html>`_ 
  (Kartick's Log, January 2006)

- `Registering an Application to a URL Protocol
  <http://msdn.microsoft.com/en-us/library/aa767914.aspx>`_
  
- Freeware `viewer <http://www.nirsoft.net/utils/url_protocol_view.html>`_ 
  for URL protocols.

Here is a simple `.reg` file that installs LibreOffice 
as handler for ``webdav:`` URLs:

.. literalinclude:: webdav.reg

To try it: download :srcref:`docs/tickets/45/webdav.reg` and doubleclick on it.

Here is a similar file for MS Office:
:srcref:`docs/tickets/45/webdav_mso.reg`.

Problem: The specified URL protocol handler then receives 
``webdav://host/path.rtf`` 
as command line argument, 
but the argumentneeds first to be converted 
to ``https://host/path.rtf``.

LibreOffice solves this using the magic protocol name 
``vnd.sun.star.webdav`` 
instead of
``webdav``.
This activates the 
`WebDAV Content Provider
<http://wiki.services.openoffice.org/wiki/Documentation/DevGuide/AppendixC/The_WebDAV_Content_Provider>`_ 
who does the conversion.
This works, but only when the WebDAV server is on 
``http``, not on ``https``.




http://msdn.microsoft.com/en-us/library/aa767914%28v=vs.85%29.aspx

