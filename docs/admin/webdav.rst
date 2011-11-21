WebDAV
======

When WebDAV is correctly set up on your server (see
:doc:`apache_webdav`), there's still a few details 
to check on the client machines.

When you click the "print" button of a Printable, 
and when the ´AppyRtfBuildMethod` is being used, 
then Lino redirects your browser to a location like 
´http://lino/media/webdav/userdocs/appyrtf/notes.Note-473.rtf`.

This will cause IE users to have the file opened within 
the browser window (but having in fact Word control it). 
Saving the file will automatically send it back to the WebDAV server.

Possible problems

The file's rtf content is displayed as plain text
-------------------------------------------------

Note: .rtf content looks something like this::

  {\rtf1\ansi\deff1\adeflang1025
  {\fonttbl{\f0\froman\fprq2\fcharset128 DejaVu Serif;}{\f1\froman\fprq2\fcharset128 Times New Roman;}{\f2\fswiss\fprq2\fcharset128 Arial;}{\f3\fnil\fprq0\fcharset128 StarSymbol{\*\falt Arial Unicode MS};}{\f4\fswiss\fprq0\fcharset128 Tahoma;}{\f5\fnil\fprq2\fcharset128 SimSun;}{\f6\fnil\fprq2\fcharset128 Tahoma;}{\f7\fnil\fprq0\fcharset128 Tahoma;}}
  {\colortbl;\red0\green0\blue0;\red128\green12



- Check whether Apache is correctly configured to return a mime type of ``application/rtf``.  

- Test with different browsers.


The file is correctly opened, but read-only
-------------------------------------------

- Maybe somebody else is just editing the file?

- Office 2003 needs Service Pack 2, otherwise if will open .rtf 
  files as read-only:
  http://support.microsoft.com/kb/884050/en-us
  
  
- LibreOffice users, see
  http://help.libreoffice.org/Common/Opening_a_Document_Using_WebDAV_over_HTTPS
  
  You must manually open the webdav location once, to trigger LO's dialog 
  that asks for username and password.
  
  http://forums.mozillazine.org/viewtopic.php?p=3203256
  http://user.services.openoffice.org/en/forum/viewtopic.php?f=47&t=14017
  http://user.services.openoffice.org/en/forum/viewtopic.php?f=7&t=1614#p32570
  http://extensions.geckozone.org/DownloadWith
  

If your Office suite doesn't support editing of webdav documents
----------------------------------------------------------------

Tell your browser that it is okay to open "local" files

- FF users must install Michael J Gruber's
  `LocalLink add-on <https://addons.mozilla.org/en-US/firefox/addon/locallink/>`_.

- Chrome users must install Leonid Borisenko's
  `LocalLinks add-on <https://chrome.google.com/webstore/detail/jllpkdkcdjndhggodimiphkghogcpida>`_.

- all windows users must map a drive letter (e.g. ``W:`` to the 
  :attr:`lino.Lino.webdav_root` directory on the Lino server.
  
- Set :attr:`lino.Lino.webdav_url` to ``"file://W:/"``


