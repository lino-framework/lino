======================
The Lino Model Library 
======================

Lino comes with a collection of reusable models 
in the :mod:`lino.modlib` package.

There may come other such collections, developed by other authors. 

Vocabulary: 
:mod:`lino.modlib` is a collection of 
*Django applications* (Lino calls them *modules*)
designed to be used by Lino applications.
There is also collection of Lino *applications* 
(a concept for which Django has no word) 
in :mod:`lino.apps`.
An application is a defined set of modules that have been 
"glued together".


.. contents::
  :depth: 2
  :local:



The ``countries`` label
-----------------------

.. module:: countries

Implemented in :mod:`lino.modlib.countries`

.. class:: Country

Implemented in :class:`lino.modlib.countries.models.Country`


.. class:: City

Implemented in :class:`lino.modlib.countries.models.City`



The ``contacts`` label
----------------------

.. module:: contacts

Depends on :mod:`countries`.

A :class:`Partner` is anything that can act as a business partner.
A Partner has at least a name and usually also one "official" address.
Predefined subclasses of Partners are
:class:`Person` for physical persons and
:class:`Company` for companies, organisations and any kind of 
non-formal Partners.

A :class:`Contact` is a :class:`Person` 
that has a certain role :class:`ContactType` 
in a certain :class:`Company`. 
  
:attr:`Company.type` is a pointer to this company's :class:`CompanyType`.

.. class:: Contact

Abstract base class for :class:`Company` and :class:`Person`.

.. class:: Person

  Abstract implementation in 
  :class:`lino.modlib.contacts.models.Person`
  
  Concrete implementations in 
  :class:`pcsw <lino.apps.pcsw.models.Person>`
  and :class:`igen <lino.modlib.igen.models.Person>`


.. class:: Company

  Abstract implementation in 
  :class:`lino.modlib.contacts.models.Company`
  
  Concrete implementations in 
  :class:`pcsw <lino.apps.pcsw.models.Company>`
  and :class:`igen <lino.apps.igen.models.Company>`

.. class:: ContactType

  .. attribute:: name
  
    the string displayed in comboboxes when selecting a ContactType.
    Also used at "in seiner Eigenschaft als ..." in document templates for contracts.
  
  .. attribute:: name_fr
  
    The optional french version of :attr:`name`.
    See :doc:`/topics/babel`.
  
.. class:: CompanyType

  Implemented in :class:`lino.modlib.contacts.models.CompanyType`
  
  .. attribute:: abbr
  
    The usual abbreviation. Used to build default string representation.
    
  .. attribute:: name
  
    Used to build default string representation.
  
  .. attribute:: contract_type
    
      Only :doc:`/pcsw/index`.
      
      The default ContractType to apply on contracts with a company of this CompanyType.



The ``links`` label
-------------------

.. module:: links

Implemented in :mod:`lino.modlib.links`

.. class:: Link

  Implemented in :class:`lino.modlib.links.models.Link`
  
  A bookmark, made by a certain user at a certain date, usually assigned 
  to a certain "owner" and possibly classified into a certain type.


.. class:: LinkType

  Implemented in :class:`lino.modlib.links.models.LinkType`


The ``jobs`` label
------------------

.. module:: jobs

Implemented by :mod:`lino.modlib.jobs`

.. class::  JobProvider

Implemented by :class:`lino.modlib.jobs.models.JobProvider`
  
.. class::  JobProviders

Implemented by :class:`lino.modlib.jobs.models.JobProviders`


