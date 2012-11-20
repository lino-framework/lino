===================================
Reading data from Belgian eID cards
===================================


For system managers
-------------------

When :attr:`lino.Lino.use_eid_jslib` is `True`, then 
you as the system administrator are responsible for installing 
Johan De Schutter's 
`eid-javascript-lib <http://code.google.com/p/eid-javascript-lib/>`_
and creating in your project's `media` directory, a symlink 
named `ext-jslib` which points to the installation directory.

Yes, this is currently a bit tricky.

The installation directory must probably contain 
the following files::

  Applet-Launcher License.rtf
  BEID_Applet.jar
  applet-launcher.jar
  be_belgium_eid.js
  beid.jnlp
  beid35JavaWrapper-linux.jar
  beid35JavaWrapper-mac.jar
  beid35JavaWrapper-win.jar
  beid35libJava.jar
  beid_java_plugin.jnlp
  hellerim_base64.js
  license.txt
  readme.txt
  
as explained in Johan's 
`readme.txt <http://code.google.com/p/eid-javascript-lib/source/browse/trunk/readme.txt>`_,
and `hellerim_base64.js` 
is Dr. Heller's base64 implementation with Johan's modifications as 
explained in 
`example_picture.html 
<http://code.google.com/p/eid-javascript-lib/source/browse/trunk/examples/example_picture.html>`_.





For applciation developers
---------------------------

When :attr:`lino.Lino.use_eid_jslib` is `True`, then the `lino*.js` 
fill define a function `Lino.beid_read_card_handler` which you can 
use in your application by subclassing 
:class:`lino.actions.BeIdReadCardAction`.
See :mod:`lino_welfare.modlib.pcsw.models` for a usage example. b
