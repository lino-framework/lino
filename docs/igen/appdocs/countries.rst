=========
countries
=========



.. currentmodule:: countries

Defined in :srcref:`/lino/modlib/countries/models.py`



.. contents:: Table of Contents



.. index::
   pair: model; Language

.. _igen.countries.Language:

------------------
Model **Language**
------------------



Language(id, name, iso2)
  
======= ========= =================================
name    type      verbose name                     
======= ========= =================================
id      CharField id                               
name    CharField Designation (Bezeichnung,Nimetus)
iso2    CharField iso2                             
name_de CharField Designation (de)                 
name_fr CharField Designation (fr)                 
name_nl CharField Designation (nl)                 
name_et CharField Designation (et)                 
======= ========= =================================

    
Defined in :srcref:`/lino/modlib/countries/models.py`

.. index::
   single: field;id
   
.. _igen.countries.Language.id:

Field **Language.id**
=====================





Type: CharField

   
.. index::
   single: field;name
   
.. _igen.countries.Language.name:

Field **Language.name**
=======================





Type: CharField

   
.. index::
   single: field;iso2
   
.. _igen.countries.Language.iso2:

Field **Language.iso2**
=======================





Type: CharField

   
.. index::
   single: field;name_de
   
.. _igen.countries.Language.name_de:

Field **Language.name_de**
==========================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _igen.countries.Language.name_fr:

Field **Language.name_fr**
==========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _igen.countries.Language.name_nl:

Field **Language.name_nl**
==========================





Type: CharField

   
.. index::
   single: field;name_et
   
.. _igen.countries.Language.name_et:

Field **Language.name_et**
==========================





Type: CharField

   


.. index::
   pair: model; Country

.. _igen.countries.Country:

-----------------
Model **Country**
-----------------




Implements the :class:`countries.Country` convention.

  
========== ========= ============
name       type      verbose name
========== ========= ============
isocode    CharField isocode     
name       CharField name        
short_code CharField short code  
iso3       CharField iso3        
name_de    CharField name (de)   
name_fr    CharField name (fr)   
name_nl    CharField name (nl)   
name_et    CharField name (et)   
========== ========= ============

    
Defined in :srcref:`/lino/modlib/countries/models.py`

.. index::
   single: field;isocode
   
.. _igen.countries.Country.isocode:

Field **Country.isocode**
=========================





Type: CharField

   
.. index::
   single: field;name
   
.. _igen.countries.Country.name:

Field **Country.name**
======================





Type: CharField

   
.. index::
   single: field;short_code
   
.. _igen.countries.Country.short_code:

Field **Country.short_code**
============================





Type: CharField

   
.. index::
   single: field;iso3
   
.. _igen.countries.Country.iso3:

Field **Country.iso3**
======================





Type: CharField

   
.. index::
   single: field;name_de
   
.. _igen.countries.Country.name_de:

Field **Country.name_de**
=========================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _igen.countries.Country.name_fr:

Field **Country.name_fr**
=========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _igen.countries.Country.name_nl:

Field **Country.name_nl**
=========================





Type: CharField

   
.. index::
   single: field;name_et
   
.. _igen.countries.Country.name_et:

Field **Country.name_et**
=========================





Type: CharField

   


.. index::
   pair: model; City

.. _igen.countries.City:

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

.. index::
   single: field;id
   
.. _igen.countries.City.id:

Field **City.id**
=================





Type: AutoField

   
.. index::
   single: field;name
   
.. _igen.countries.City.name:

Field **City.name**
===================





Type: CharField

   
.. index::
   single: field;country
   
.. _igen.countries.City.country:

Field **City.country**
======================





Type: ForeignKey

   
.. index::
   single: field;zip_code
   
.. _igen.countries.City.zip_code:

Field **City.zip_code**
=======================





Type: CharField

   


