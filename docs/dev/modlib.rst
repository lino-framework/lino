===============================
The standard library ``modlib``
===============================

The :mod:`lino.modlib` modules are ready-to-use "apps" (as Django
calls them) which may be used by your Lino applications.

Contacts
========

.. currentmodule:: ml.contacts

The :mod:`lino.modlib.contacts` package 
(or some extension of it like
:mod:`lino_welfare.modlib.contacts` or 
:mod:`lino_faggio.modlib.contacts`)
provides data definitions for "Contact management":

- The :class:`Partner` Model (and its two standard specializations
  :class:`Person` and :class:`Company`)

- A :class:`CompanyType` model can be used to classify companies.

- The :class:`Role` and :class:`RoleType` models store "who is who"
  information.



.. class:: Partner

    A :class:`Partner` is anything that can act as a business partner.
    A Partner has at least a name and usually also one "official" address.
    Predefined subclasses of Partners are
    :class:`Person` for physical persons and
    :class:`Company` for companies, organisations and any kind of
    non-formal Partners.

    Base class for anything that has contact information
    (postal address, email, phone,...).


.. class:: Person

    Represents a physical person.
    See :ref:`lino.tutorial.human`.

.. class:: Company

    Represents an organisation.  The internal name is "Company" for
    historical reasons and because that's easier to type.

    See also :doc:`/tickets/14`.

.. class:: CompanyDetail

    The :class:`dd.Layout` of the detail Window of a :class:`Company`.


  .. attribute:: type

.. class:: CompanyType

    Represents a possible choice for the :attr:`Company.type` field.


Using the modlib
================


Overriding `modlib` apps
------------------------

Django identifies models and SQL tables using a string of format
`app_label.model_name`.

The `app_label` is usually added automatically by taking the second-last 
part of the full Python module name. 

For example if you define two classes
`foo.sales.models.Invoice` and `bar.sales.models.Invoice` 
(both subclasses of django.db.models.Model) and install them both 
using ``INSTALLED_APPS = ['foo.sales', 'bar.sales']``, 
then `bar.sales.models.Invoice` will "override" 
`foo.sales.models.Invoice`, and 
`sales.Invoice` 
will be implemented by `foo.sales`, not by `bar.sales`.

Lino uses this behaviour to provide a collection of reusable Models, Reports and Menus that 
are not limited to a known implementation of a model will be used.



Optionally you may write your own Django application that adds new models or reimplements models from lino.modlib.

For example if you have a Django application `myapp` and want to extend :class:`contacts.Person`, then in :file:`myapp/models.py` you write::

  from lino.modlib.contacts import models as contacts
  class Person(contacts.Person):

      class Meta:
          app_label = 'contacts'
          
      my_field = models.CharField(...)
      ...

The important thing is to manually specify `Meta.app_label` because otherwise your model would be called `myapp.Person`.


  
