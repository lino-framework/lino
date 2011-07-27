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



Language(id, name, iso2, name_fr, name_nl, name_en)
  
======= ============== ======================================
name    type           verbose name                          
======= ============== ======================================
id      CharField      id                                    
name    BabelCharField Designation (Beschreibung,Désignation)
iso2    CharField      iso2                                  
name_fr CharField      Designation (fr)                      
name_nl CharField      Designation (nl)                      
name_en CharField      Designation (en)                      
======= ============== ======================================

    
Defined in :srcref:`/lino/modlib/countries/models.py`

Referenced from
`lino.dsbe.Study.language`_, `lino.dsbe.LanguageKnowledge.language`_, `lino.dsbe.WantedLanguageKnowledge.language`_



.. index::
   single: field;id
   
.. _lino.countries.Language.id:

Field **Language.id**
=====================





Type: CharField

   
.. index::
   single: field;name
   
.. _lino.countries.Language.name:

Field **Language.name**
=======================





Type: BabelCharField

   
.. index::
   single: field;iso2
   
.. _lino.countries.Language.iso2:

Field **Language.iso2**
=======================





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
   single: field;name_en
   
.. _lino.countries.Language.name_en:

Field **Language.name_en**
==========================





Type: CharField

   


.. index::
   pair: model; Country

.. _lino.countries.Country:

-----------------
Model **Country**
-----------------




Implements the :class:`countries.Country` convention.

  
========== ============== ======================================
name       type           verbose name                          
========== ============== ======================================
isocode    CharField      isocode                               
name       BabelCharField Designation (Beschreibung,Désignation)
short_code CharField      short code                            
iso3       CharField      iso3                                  
name_fr    CharField      Designation (fr)                      
name_nl    CharField      Designation (nl)                      
name_en    CharField      Designation (en)                      
========== ============== ======================================

    
Defined in :srcref:`/lino/modlib/countries/models.py`

Referenced from
`lino.jobs.JobProvider.country`_, `lino.contacts.Person.country`_, `lino.contacts.Person.birth_country`_, `lino.contacts.Person.nationality`_, `lino.contacts.Company.country`_, `lino.dsbe.Study.country`_, `lino.dsbe.JobExperience.country`_, `lino.dsbe.CourseProvider.country`_, `lino.countries.City.country`_



.. index::
   single: field;isocode
   
.. _lino.countries.Country.isocode:

Field **Country.isocode**
=========================





Type: CharField

   
.. index::
   single: field;name
   
.. _lino.countries.Country.name:

Field **Country.name**
======================





Type: BabelCharField

   
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
   single: field;name_en
   
.. _lino.countries.Country.name_en:

Field **Country.name_en**
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
`lino.jobs.JobProvider.city`_, `lino.contacts.Person.city`_, `lino.contacts.Company.city`_, `lino.dsbe.Study.city`_, `lino.dsbe.CourseProvider.city`_



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

   


