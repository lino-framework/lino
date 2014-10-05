========
Contacts
========

.. module:: ml.contacts

The :mod:`lino.modlib.contacts` package 
provides data definitions for "Contact management".

This app is being extended by :ref:`welfare` in
:mod:`lino_welfare.modlib.contacts` or by :ref:`faggio` in
:mod:`lino_faggio.modlib.contacts`.

.. contents:: 
   :local:
   :depth: 2


.. note:: 

  This is a tested document. You can test it using::

    $ python setup.py test -s tests.DocsTests.test_docs

.. 
  >>> import os
  >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
  ...   'lino.projects.docs.settings'
  >>> from lino.runtime import *

Models
======

- The :class:`Partner` model (and its two subclasses
  :class:`Person` and :class:`Company`)

- A :class:`CompanyType` model can be used to classify companies.

- The :class:`Role` and :class:`RoleType` models store "who is who"
  information.

Partner
-------

.. class:: Partner(AddressLocation)

    A Partner is any physical or moral person for which you want to
    keep contact data (address, phone numbers, ...).

    A :class:`Partner` can act as the recipient of a sales invoice, as
    the sender of an incoming purchases invoice, ...

    A Partner has at least a name and usually also an "official" address.

    Predefined subclasses of Partners are :class:`Person` for physical
    persons and :class:`Company` for companies, organisations and any
    kind of non-formal Partners.

    Lino differentiates the following subclasses of Partner:

    .. django2rst:: contacts.Partner.print_subclasses_graph()



  .. attribute:: name

    The full name of this partner. Used for alphabetic
    sorting. Subclasses may fill this field automatically, e.g. saving
    a :class:`Person` will automatically set her `name` field to
    "last_name, first_name".

  .. attribute:: email

    The primary email address.

Person
------

.. class:: Person

    Represents a physical person and an individual human being.
    See :ref:`lino.tutorial.human`.

Company
-------

.. class:: Company

    Represents an organisation.  The internal name is "Company" for
    historical reasons and because that's easier to type.

    See also :doc:`/tickets/14`.

  .. attribute:: type
    
    Pointer to the :class:`CompanyType`. 

CompanyType
-----------

.. class:: CompanyType

    Represents a possible choice for the :attr:`Company.type`
    field. The :mod:`std <ml.contacts.std>` fixture fills this with
    the following data (5 first rows only):

    .. django2rst:: rt.show(contacts.CompanyTypes, limit=5)

Role
----

.. class:: Role

    A Role is when a given :class:`Person` plays a given
    :class:`RoleType` in a given :class:`Company`.

RoleType
--------

.. class:: RoleType

    A :class:`RoleType` is "what a given :class:`Person` can be for a
    given :class:`Company`".

    The default database comes with the following list of 
    :class:`RoleType`:
    
    .. django2rst:: rt.show(contacts.RoleTypes)
    


Mixins
======

AddressLocation
---------------

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



ContactRelated
--------------

.. class:: ContactRelated

    Model mixin for things that relate to a *company*, potentially
    represented by a *contact person* having a given *role*.

    Adds 3 fields `company`, `contact_person` and `contact_role`.

    .. attribute:: company

    Pointer to :class:`Company`.

    .. attribute:: contact_person

    Pointer to :class:`Person`.

    .. attribute:: contact_role

    Pointer to :class:`RoleType`.




Tables and Layouts
==================

.. class:: CompanyDetail

    The :class:`dd.Layout` of the :term:`detail window` of a :class:`Company`.

.. class:: PersonDetail

    The :class:`dd.Layout` of the :term:`detail window` of a :class:`Person`.




Configuration
=============

.. class:: Plugin

  Extends :class:`ad.Plugin`. See also :doc:`/dev/ad`.

  .. attribute:: hide_region

    Whether to hide the `region` field in postal addresses.  Set this
    to `True` if you live in a country like Belgium.  Belgium
    is --despite their constant language disputes-- obviously a very
    united country since they don't need a `region` field when
    entering a postal address.  In many other countries such a field
    is required.


