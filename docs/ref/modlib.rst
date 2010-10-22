=========================
Model Library Conventions
=========================

Lino comes with a library of reusable models in the 
:mod:`lino.modlib` package.
There may come other such packages, developed by other authors. 
In order to be useable in Lino, 
they should adhere to Lino's 
Model Library Conventions.

Lino relies on Django's system of 'applications' and 'models'.

.. contents::
  :depth: 2
  :local:



The ``countries`` application label
-----------------------------------

.. module:: countries

Implemented in :mod:`lino.modlib.countries`

.. class:: Country

  Implemented in :class:`lino.modlib.countries.models.Country`


.. class:: City

  Implemented in :class:`lino.modlib.countries.models.City`



The ``contacts`` application label
----------------------------------

.. module:: contacts

Depends on :mod:`countries`.

A :class:`Contact` is anything that may be contacted using a postal or email address or phone numbers. 

:class:`Contact` is the abstract base class 
for :class:`Person` (physical persons) 
and :class:`Company` (companies, organisations of any kind, non-formal groups of persons). 
  
:attr:`Company.type` is a pointer to this 
company's :class:`CompanyType`. 
:class:`CompanyTypes`
  

.. class:: Contact

  Abstract base class for :class:`Company` and :class:`Person`.
  Anything that has contact information (postal address, email, phone,...).

  .. attribute:: country
  
      A pointer to :class:`countries.Country`. The country where this contact is located.
    
  .. attribute:: city
  
      A pointer to :class:`countries.City`. The city where this contact is located.
      The list of choices for this field is context-sensitive, it depends on the :attr:`country`.
    
  .. method:: address
  
      The plain text postal address, layd out according to the local rules in 
      this Contact's :country. 
      Virtual field. 

.. class:: Person

  Abstract implementation in 
  :class:`lino.modlib.contacts.models.Person`
  
  Concrete implementations in 
  :class:`dsbe <lino.modlib.dsbe.models.Person>`
  and :class:`igen <lino.modlib.igen.models.Person>`


.. class:: Company

  Abstract implementation in 
  :class:`lino.modlib.contacts.models.Company`
  
  Concrete implementations in 
  :class:`dsbe <lino.modlib.dsbe.models.Company>`
  and :class:`igen <lino.modlib.igen.models.Company>`

.. class:: CompanyType

  Implemented in :class:`lino.modlib.contacts.models.CompanyType`
