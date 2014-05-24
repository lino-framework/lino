========
Contacts
========

.. module:: ml.contacts

The :mod:`lino.modlib.contacts` package 
provides data definitions for "Contact management".

This app is being extended by :ref:`welfare` in
:mod:`lino_welfare.modlib.contacts` or by :ref:`faggio` in
:mod:`lino_faggio.modlib.contacts`.

.. note:: 

  This is a tested document. You can test it using::

    $ python setup.py test -s tests.DocsTests.test_docs



.. 
  >>> import os
  >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
  ...   'lino.projects.docs.settings'
  >>> from lino import dd
  >>> dd.startup()
  >>> globals().update(dd.modules)

Mixins
======

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



Models
======

- The :class:`Partner` model (and its two subclasses
  :class:`Person` and :class:`Company`)

- A :class:`CompanyType` model can be used to classify companies.

- The :class:`Role` and :class:`RoleType` models store "who is who"
  information.


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

.. class:: CompanyType

    Represents a possible choice for the :attr:`Company.type`
    field. The :mod:`std <ml.contacts.std>` fixture fills this with
    the following data (5 first rows only):

    .. lino2rst::

       dd.login('robin').show(contacts.CompanyTypes, limit=5)


Tables and Layouts
==================

.. class:: CompanyDetail

    The :class:`dd.Layout` of the :term:`detail window` of a :class:`Company`.

.. class:: PersonDetail

    The :class:`dd.Layout` of the :term:`detail window` of a :class:`Person`.




Settings
========

.. class:: Plugin

  See also :doc:`/admin/settings` and :doc:`/dev/ad`.

  .. attribute:: hide_region

    Whether to hide the `region` field in postal addresses.  Set this
    to `True` if you live in a country like Belgium.  Belgium
    is --despite their constant language disputes-- obviously a very
    united country since they don't need a `region` field when
    entering a postal address.  In many other countries such a field
    is required.

    Example code in a local :xfile:`settings.py` file::

      dd.configure_plugin('contacts', hide_region=True)


