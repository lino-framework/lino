.. _eidreader:

====================
The EIDReader applet
====================

**International eID card reader**

EIDReader is an applet to read the publicly available information
(name, birth date, national id,...)  on electronic ID cards of
different countries and make them accessible to the Javascript code of
a web page.

This is useful in web applications which read the public info (name,
national id, birth date,...) from an id card inserted into the
client's card reader and send this info to the application server.

For example in an Estonian pharmacy the salesman inserts the
customer's id card instead of asking for their name or national id.

Other than the official eid card frameworks 
for `Belgium <https://code.google.com/p/eid-applet>`_ 
and `Estonia <http://www.id.ee/index.php?id=36143>`_,
EIDReader does *not* ask for a PIN and does *not*  
authenticate the id card's holder.
Authentication and security is responsibility of the application 
which uses the applet.


**Status**

- Currently supported countries are Estonia and Belgium.

- The Estonian reader does not yet import the photo
  (hints on how to implement this are welcome).

- The applet works perfectly on a client with IcedTea (OpenJDK) 
  RTE, but *not* when using a Sun Java client. 
  (hints on how to get that working are welcome).


Note: 
The EIDReader **code** has been moved to its own repository at
https://github.com/lsaffre/eidreader,
the documentation is still here until I learned how to manage docs 
on github.



.. toctree::
    :maxdepth: 1

    countries
    install
    intro
    

