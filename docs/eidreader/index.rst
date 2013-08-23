.. _eidreader:

====================
The EIDReader applet
====================

An applet to read the publicly available information 
(name, birth date, national id,...) 
on electronic ID cards of different countries and make them accessible 
to Javascript code. 

Currently supported countries are Estonia and Belgium.

- Source code: :srcref:`EIDReader </java/lino/eid/EIDReader.java>`
- Makefile: :srcref:`EIDReader </java/lino/Makefile>`



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
For example is doesn't validate the data on a given card.
It will happily display information even from invalid cards.
Use the official Belgian eID software if you want to do that.

EIDReader imports and uses three classes from 
`eid-applet <https://code.google.com/p/eid-applet>`_
because the mere parsing of the information found on Belgian eID cards 
is very complex.

 
