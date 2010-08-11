=================================
:mod:`lino.modlib` user reference
=================================

Overview
========

This section is the central user reference documentation for the modules in :mod:`lino.modlib`. 


================= ==========================================
Name              Tables
================= ==========================================
:mod:`contacts`   :class:`contacts.Person`, :class:`contacts.Company`
:mod:`countries`  :class:`countries.Country`, :class:`countries.City`
:mod:`notes`      :class:`notes.Note`, :class:`notes.NoteType`
:mod:`projects`
:mod:`system`
:mod:`products`
:mod:`sales`
:mod:`journals`
:mod:`finan`
:mod:`ledger`
================= ==========================================


How it works
------------

The `lino.modlib` modules are ready-to-use Django applications that may be 
included in your :setting:`INSTALLED_APPS`::

  INSTALLED_APPS = (
  
    # manatory django.contrib applications needed by Lino
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    
    # your selection of lino.modlib applications:
    
    'lino.modlib.system',
    'lino.modlib.countries',
    'lino.modlib.contacts',
    'lino.modlib.projects',
    'lino.modlib.notes',
    
    # optionally you may write your own Django application that adds new models or reimplements models from lino.modlib.
    'myapp',  
  )

Django identifies models and SQL tables using a string of format `app_label.model_name`. 
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


Overriding modlib models
------------------------

Optionally you may write your own Django application that adds new models or reimplements models from lino.modlib.

For example if you have a Django application `myapp` and want to extend :class:`contacts.Person`, then in :file:`myapp/models.py` you write::

  from lino.modlibe.contacts import models as contacts
  class Person(contacts.Person):

      class Meta:
          app_label = 'contacts'
          
      my_field = models.CharField(...)
      ...

The important thing is to manually specify `Meta.app_label` because otherwise your model would be called `myapp.Person`.



.. module:: contacts

contacts
========

contacts.Contact
----------------

.. class:: Contact

  Anything that has contact information (postal address, email, phone,...).
  Base class for :class:`Company` and :class:`Person`.
  
  .. attribute:: address
  
  The postal address, formatted according to the local rules in this country. Virtual field. 



contacts.Company
----------------

.. class:: Company
.. report:: contacts.Companies

  Used to store organisations of any kind. Also non-formal groups of persons.
  


contacts.Person
---------------

.. class:: Person
.. report:: contacts.Persons

  Used to store physical persons.
  

.. module:: countries

countries
=========

lino.modlib.countries.models

countries.Country
-----------------

.. class:: Country
.. report:: countries.Countries

  .. attribute:: isocode
  
  .. attribute:: name
  
  .. attribute:: short_code


notes
=====

lino.modlib.notes.models

notes.Note
----------

.. class:: Note

  .. attribute:: isocode
  
notes.NoteType
--------------

.. class:: NoteType
