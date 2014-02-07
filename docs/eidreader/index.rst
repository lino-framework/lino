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

**TODO**

- I'd like to set up a public demo/test page, but is it allowed to 
  sign a third-party `.jar` file and to distribute it together with 
  my .jar file?
  Concretely I speak about the following libraries:

  - `eid-applet-services.jar` from the
    `eid-applet <https://code.google.com/p/eid-applet/>`_
    project (LGPL)
  - `commons-logging.jar` from the
    `commons-logging <http://commons.apache.org/proper/commons-logging/>`_
    project.
  - `commons-codec.jar` from the
    `commons-codec <http://commons.apache.org/proper/commons-codec/>`_
    project.

**Status**


- I need help with packaging, signing and deploying the applet.
  I have at least one concrete problem described 
  in :blogref:`20131220`. 
  Hints on how to get that working are welcome.


**Pages referring to this**

.. refstothis:: eidreader


**Sitemap**

.. toctree::
    :maxdepth: 1

    intro
    countries
    install
    applets
    

