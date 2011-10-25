Using JavaScript
================

This might become a solution for :doc:`/tickets/45`.

Using JavaScript implies that we must use browser-specific methods.


This approach seems the most promising.
The main challenge was that we must find out 
which application to start, that is, 
the application associated 
(on the client's desktop)
with a given file type.
On a Windows client we must consult the registry,
on Linux there might be different methods depending 
on which Window Manager is used. At least KDE and Gnome 
should have the concept of a configured list that maps 
a file extension to the executable to be launched.
The other challenge is to get permission for Lino's Javascript 
to execute local commands without violating the client's 
security.


**Internet Explorer**: 
If Microsoft would rule them all, we could simply do::

  <script type="text/javascript">
  function runShell(cmd) {
    WshShell = new ActiveXObject("WScript.Shell");
    WshShell.Run(cmd); // ,1,true);
  }
  </script>

In fact it's less trivial: the above would still start a browser window 
if `cmd` were a string like `http://webdav.server.tld/path/doc.rtf`. 
It shouldn't be too difficult though to read the registry and get the 
command associated to `.rtf` files and run it on the URL.
But I'm not going to waste unpaid time on proprietary software.


For **Firefox** we got it working.
(Sources:
`1 <https://developer.mozilla.org/en/Code_snippets/Running_applications>`_
`2 <https://developer.mozilla.org/en/XPCOM_Interface_Reference/nsIProcess>`_
`3 <http://forums.mozillazine.org/viewtopic.php?f=19&t=803615&start=0>`_
`4 <http://stackoverflow.com/questions/2017743/how-to-call-a-function-in-firefox-extension-from-a-html-button>`_
`5 <http://stackoverflow.com/questions/1374927/launch-file-from-firefox-chrome>`_)
Here is a proof of concept:

.. literalinclude:: ../blog/2011/0923/startfile.js

This script would be used as follows:

.. literalinclude:: ../blog/2011/0923/startfile.html



Firefox will ask the user "A script from XXX is requesting enhanced 
abilities that are UNSAFE and could be used to comprimise your machine 
or data...":

.. image:: 45/20110921a.jpg
   :scale: 50
  
**Google Chrome** :
we probably need to write an NPAPI extension.
Read
`1 <http://stackoverflow.com/questions/2537772/how-can-i-launch-a-system-command-via-javascript-in-google-chrome>`_
`2 <http://code.google.com/chrome/extensions/getstarted.html>`_
`3 <http://code.google.com/chrome/extensions/devguide.html>`_
`4 <http://code.google.com/chrome/extensions/npapi.html>`_
`5 <https://developer.mozilla.org/en/Plugins>`_
and
`6 <http://www.firebreath.org/display/documentation/FireBreath+Home>`_.




