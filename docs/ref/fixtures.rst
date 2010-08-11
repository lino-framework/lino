Fixtures
========

The following packages contain fixtures to be used by Django.

- :mod:`lino.modlib.ledger`
- :mod:`lino.modlib.notes`
- :mod:`lino.modlib.contacts`
- :mod:`dsbe`


Most fixtures are written in dpy format, so you need the following in 
your :xfile:`settings.py`::

  SERIALIZATION_MODULES = {
       "dpy" : "lino.utils.dpyserializer",
  }



- initial_data
- demo
- demo_ee
- be
- et
- iso3166 : in :mod:`lino.modlib.countries` populates all countries to :class:`countries.Country` 

