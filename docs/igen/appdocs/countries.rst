=========
countries
=========



.. currentmodule:: countries

Defined in :srcref:`/lino/modlib/countries/models.py`


Defines models 
:class:`Language`,
:class:`Country` and
:class:`City`.



.. contents:: Table of Contents



.. index::
   pair: model; Language

.. _lino.countries.Language:

------------------
Model **Language**
------------------



Language(name, id, iso2, name_de, name_fr, name_nl, name_et)
  
======= ============== ==========================
name    type           verbose name              
======= ============== ==========================
name    BabelCharField Designation (Beschreibung)
id      CharField      id                        
iso2    CharField      iso2                      
name_de CharField      Designation (de)          
name_fr CharField      Designation (fr)          
name_nl CharField      Designation (nl)          
name_et CharField      Designation (et)          
======= ============== ==========================

    
Defined in :srcref:`/lino/modlib/countries/models.py`

Referenced from




.. index::
   single: field;name
   
.. _lino.countries.Language.name:

Field **Language.name**
=======================





Type: BabelCharField

   
.. index::
   single: field;id
   
.. _lino.countries.Language.id:

Field **Language.id**
=====================





Type: CharField

   
.. index::
   single: field;iso2
   
.. _lino.countries.Language.iso2:

Field **Language.iso2**
=======================





Type: CharField

   
.. index::
   single: field;name_de
   
.. _lino.countries.Language.name_de:

Field **Language.name_de**
==========================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _lino.countries.Language.name_fr:

Field **Language.name_fr**
==========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.countries.Language.name_nl:

Field **Language.name_nl**
==========================





Type: CharField

   
.. index::
   single: field;name_et
   
.. _lino.countries.Language.name_et:

Field **Language.name_et**
==========================





Type: CharField

   


.. index::
   pair: model; Country

.. _lino.countries.Country:

-----------------
Model **Country**
-----------------




Implements the :class:`countries.Country` convention.

  
========== ============== ==========================
name       type           verbose name              
========== ============== ==========================
name       BabelCharField Designation (Beschreibung)
isocode    CharField      isocode                   
short_code CharField      short code                
iso3       CharField      iso3                      
name_de    CharField      Designation (de)          
name_fr    CharField      Designation (fr)          
name_nl    CharField      Designation (nl)          
name_et    CharField      Designation (et)          
========== ============== ==========================

    
Defined in :srcref:`/lino/modlib/countries/models.py`

Referenced from
`lino.users.User.country`_, `lino.contacts.Contact.country`_, `lino.contacts.Person.country`_, `lino.contacts.Company.country`_, `lino.countries.City.country`_



.. index::
   single: field;name
   
.. _lino.countries.Country.name:

Field **Country.name**
======================





Type: BabelCharField

   
.. index::
   single: field;isocode
   
.. _lino.countries.Country.isocode:

Field **Country.isocode**
=========================





Type: CharField

   
.. index::
   single: field;short_code
   
.. _lino.countries.Country.short_code:

Field **Country.short_code**
============================





Type: CharField

   
.. index::
   single: field;iso3
   
.. _lino.countries.Country.iso3:

Field **Country.iso3**
======================





Type: CharField

   
.. index::
   single: field;name_de
   
.. _lino.countries.Country.name_de:

Field **Country.name_de**
=========================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _lino.countries.Country.name_fr:

Field **Country.name_fr**
=========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.countries.Country.name_nl:

Field **Country.name_nl**
=========================





Type: CharField

   
.. index::
   single: field;name_et
   
.. _lino.countries.Country.name_et:

Field **Country.name_et**
=========================





Type: CharField

   


.. index::
   pair: model; City

.. _lino.countries.City:

--------------
Model **City**
--------------




Implements the :class:`countries.City` convention.

  
======== ========== ==============
name     type       verbose name  
======== ========== ==============
id       AutoField  ID            
name     CharField  name          
country  ForeignKey country (Land)
zip_code CharField  zip code      
======== ========== ==============

    
Defined in :srcref:`/lino/modlib/countries/models.py`

Referenced from
`lino.users.User.city`_, `lino.contacts.Contact.city`_, `lino.contacts.Person.city`_, `lino.contacts.Company.city`_



.. index::
   single: field;id
   
.. _lino.countries.City.id:

Field **City.id**
=================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.countries.City.name:

Field **City.name**
===================





Type: CharField

   
.. index::
   single: field;country
   
.. _lino.countries.City.country:

Field **City.country**
======================





Type: ForeignKey

   
.. index::
   single: field;zip_code
   
.. _lino.countries.City.zip_code:

Field **City.zip_code**
=======================





Type: CharField

   


