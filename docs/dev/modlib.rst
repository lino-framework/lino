===============================
The standard library ``modlib``
===============================

The :mod:`lino.modlib` modules are ready-to-use "apps" (as Django
calls them) which may be used by your Lino applications.

.. 
  >>> import os
  >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
  ...   'lino.projects.docs.settings'
  >>> from lino import dd
  >>> dd.startup()
  >>> globals().update(dd.modules)

.. contents::


.. toctree::
   :maxdepth: 2

   humanlinks



Users
=====

.. module:: ml.users

Countries (Geographic places)
=============================

.. module:: ml.countries

.. class:: Country

.. class:: Place


.. class:: CountryCity

  .. attribute:: zip_code
  .. attribute:: city

    Pointer to :class:`Place`

  .. method:: full_clean

    Fills my :attr:`zip_code` from my :attr:`city`,

    If my `zip_code` is not empty and differs from that of the city.


.. class:: CountryRegionCity

    Adds a `region` field to a :class:`CountryCity`.

  

Addresses
=========

.. module:: ml.addresses

Adds multiple addresses per Partner.

.. class:: Address

  Inherits fields from 
  :class:`ml.countries.CountryRegionCity` (country, region, city. zip_code)
  and
  :class:`ml.contacts.AddresssLocation` (street, street_no, ...)

  .. attribute:: partner

  


Contacts
========


.. module:: ml.contacts

The :mod:`lino.modlib.contacts` package 
(or some extension of it like
:mod:`lino_welfare.modlib.contacts` or 
:mod:`lino_faggio.modlib.contacts`)
provides data definitions for "Contact management":

**Models**

- The :class:`Partner` model (and its two subclasses
  :class:`Person` and :class:`Company`)

- A :class:`CompanyType` model can be used to classify companies.

- The :class:`Role` and :class:`RoleType` models store "who is who"
  information.

.. class:: AddressLocation

  .. attribute:: addr1
  .. attribute:: street_prefix
  .. attribute:: street
  .. attribute:: street_no
  .. attribute:: street_box
  .. attribute:: addr2

  .. method:: address_column(self, ar)

    Virtual field which returns the location as a comma-separated
    one-line string.


  .. method:: address_location(self, linesep="\n")

    Return the plain text postal address location part. 
    Lines are separated by `linesep` which defaults to ``"\n"``.

    The following example creates a Partner, then calls its
    :meth:`address_location` method:

    >>> BE = countries.Country.objects.get(pk='BE')
    >>> p = contacts.Partner(
    ...   name="Foo",
    ...   street_prefix="Rue de l'", street="Abattoir", 
    ...   street_no=5, country=BE, zip_code="4000")
    >>> p.full_clean()
    >>> p.save()
    >>> print(p.address_location())
    Rue de l' Abattoir 5
    4000 Liège
    Belgium



.. class:: Partner(AddressLocation)

    A :class:`Partner` is anything that can act as a business partner.
    A Partner has at least a name and usually also one "official" address.
    Predefined subclasses of Partners are
    :class:`Person` for physical persons and
    :class:`Company` for companies, organisations and any kind of
    non-formal Partners.

    Base class for anything that has contact information
    (postal address, email, phone,...).

  .. attribute:: name

    The full name of this partner. Used for alphabetic
    sorting. Subclasses may fill this field automatically, e.g. saving
    a :class:`Person` will automatically set her `name` field to
    "last_name, first_name".

  .. attribute:: email

    The primary email address.

.. class:: Person

    Represents a physical person.
    See :ref:`lino.tutorial.human`.

.. class:: Company

    Represents an organisation.  The internal name is "Company" for
    historical reasons and because that's easier to type.

    See also :doc:`/tickets/14`.

  .. attribute:: type
    
    Pointer to the :class:`CompanyType`. 

.. class:: CompanyDetail

    The :class:`dd.Layout` of the detail Window of a :class:`Company`.



.. class:: CompanyDetail



.. class:: CompanyType

    Represents a possible choice for the :attr:`Company.type`
    field. The :mod:`std <ml.contacts.std>` fixture fills this with
    the following data (5 first rows only):

    .. lino2rst::

       dd.login('robin').show(contacts.CompanyTypes, limit=5)



**Settings**

.. class:: Plugin

  See also :class:`ad.Plugin`.

  .. attribute:: hide_region

    Whether to hide the `region` field in postal addresses.  Set this
    to `True` if you live in a country like Belgium.  Belgium
    is --despite their constant language disputes-- obviously a very
    united country since they don't need a `region` field when
    entering a postal address.  In many other countries such a field
    is required.

    Example code in a local :xfile:`settings.py` file::

      SITE.configure_plugin('contacts', hide_region=True)




Using the modlib
================


Overriding `modlib` apps
------------------------

Optionally you may write your own Django application that adds new
models or reimplements models from lino.modlib.

For example if you have a Django application `myapp` and want to
extend :class:`contacts.Person`, then in :file:`myapp/models.py` you
write::

  from lino.modlib.contacts import models as contacts
  class Person(contacts.Person):

      class Meta:
          app_label = 'contacts'
          
      my_field = models.CharField(...)
      ...

The important thing is to manually specify `Meta.app_label` because
otherwise your model would be called `myapp.Person`.


  
