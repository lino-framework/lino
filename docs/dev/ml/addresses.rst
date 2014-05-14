=========
Addresses
=========

.. module:: ml.addresses

Adds functionality and models to handle multiple addresses per
:class:`ml.contacts.Partner`. When this module is installed, your
application usually has a "Manage addresses" button per partner.

.. class:: AddressOwner

    Base class for the "addressee" of any address.

.. class:: DataSources

  The choicelist with the possible values of :attr:`Address.data_source`.

.. class:: AddressTypes

  The choicelist with the possible values of :attr:`Address.address_type`.


.. class:: Address

  Inherits fields from 
  :class:`ml.countries.CountryRegionCity` (country, region, city. zip_code)
  and
  :class:`ml.contacts.AddresssLocation` (street, street_no, ...)

  .. attribute:: partner

  .. attribute:: address_type

  .. attribute:: data_source

    Specifies how this information entered into our database.
  
  .. attribute:: primary

    Setting this field will automatically uncheck any previousl
    primary addresses and update the partner's address fields.
