====================
Supported countries
====================

Currently supported countries are Estonia_ and Belgium_.
Contributions for other countries are welcome
(please contact :ref:`luc` before doing a lot of work).

Estonia
-------

The original version was largely inspired by 
a `blog post by Revo at Codeborne 
<http://blog.codeborne.com/2010/10/javaxsmartcardio-and-esteid.html>`_.

Belgium
-------

Other than the official 
`eid-applet <https://code.google.com/p/eid-applet>`_,
the basic idea of EIDReader is to not worry about 
verifying the certificates and asking privacy questions like "Are you 
sure you want to display the information on this card to your screen?"

So EIDReader has an will always have some limitations. 
For example is doesn't validate the data on a given card
and will happily display information even from invalid cards.
Use the official Belgian eID software if you want to do that.

EIDReader imports and uses three classes from 
`eid-applet <https://code.google.com/p/eid-applet>`_
because the mere parsing of the information found on Belgian eID cards 
is very complex.

