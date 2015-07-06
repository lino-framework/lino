.. _eidreader:

====================
The EIDReader applet
====================

**International eID card reader**

EIDReader is an applet to read the public information on electronic ID
cards of different countries and make them accessible to the
Javascript code of a web page.

This is useful in web applications which read the public info (name,
national id, birth date,...) from an id card inserted into the
client's card reader and send this info to the application server.
For example in an Estonian pharmacy it is normal that the salesman
inserts the customer's id card instead of asking for their name or
national id.

Currently supported countries are Estonia and Belgium.  The applet is
designed to read also other countries, but we would need voluntary
contributors to add support for more countires.

The Belgian reader even reads the photo (a feature not supported by
the Estonian reader because in Estonia this requires previous
authentication).

**How to get it**

- The EIDReader **code** is hosted at
  https://github.com/lsaffre/eidreader

- This documentation is currently part of the Lino project and visible
  at http://lino-framework.org/eidreader

- An online demo is available at
  http://test-eidreader.lino-framework.org/

**Relation with other projects**

- This applet is "underground work" and not yet officially 
  supported by any of the national software frameworks for
  `Estonia <http://www.id.ee/index.php?id=36143>`_
  and `Belgium  <http://www.fedict.belgium.be/en/>`_ 

- Other than the official Belgian `eid-applet
  <https://code.google.com/p/eid-applet>`_, EIDReader does *not* ask
  for a PIN and does *not* authenticate the id card's holder.
  Authentication and security is responsibility of the application
  which uses the applet.

- EIDReader is functionally comparable to the Estonian `eidenv
  <http://www.id.ee/index.php?id=35798>`_ command-line tool, but (1)
  it works also for Belgian cards and (2) does not require any special
  software except Java on the client machine.

**Status**

- I'd love to find a partner for this project, somebody who has some
  experience with Java, who would give me advise and help me to learn
  about packaging, signing and deploying the applet.  Or even (if you
  prefer) somebody who fully takes the project maintenance.

**Pages referring to this**

.. refstothis:: eidreader


**Sitemap**

.. toctree::
    :maxdepth: 1

    intro
    countries
    install
    applets
    issues
    

