=========
countries
=========



.. currentmodule:: countries

Defined in :srcref:`/lino/modlib/countries/models.py`



.. contents:: Table of Contents



.. index::
   pair: model; Language

.. _dsbe.countries.Language:

------------------
Model **Language**
------------------



Language(id, name, iso2)
  
======= ========= ==========================
name    type      verbose name              
======= ========= ==========================
id      CharField id                        
name    CharField Designation (Beschreibung)
iso2    CharField iso2                      
name_fr CharField Designation (fr)          
name_nl CharField Designation (nl)          
name_en CharField Designation (en)          
======= ========= ==========================

    
Defined in :srcref:`/lino/modlib/countries/models.py`

.. index::
   single: field;id
   
.. _dsbe.countries.Language.id:

Field **Language.id**
=====================





Type: CharField

   
.. index::
   single: field;name
   
.. _dsbe.countries.Language.name:

Field **Language.name**
=======================





Type: CharField

   
.. index::
   single: field;iso2
   
.. _dsbe.countries.Language.iso2:

Field **Language.iso2**
=======================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _dsbe.countries.Language.name_fr:

Field **Language.name_fr**
==========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _dsbe.countries.Language.name_nl:

Field **Language.name_nl**
==========================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _dsbe.countries.Language.name_en:

Field **Language.name_en**
==========================





Type: CharField

   


.. index::
   pair: model; Country

.. _dsbe.countries.Country:

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
name_fr    CharField name (fr)   
name_nl    CharField name (nl)   
name_en    CharField name (en)   
========== ========= ============

    
Defined in :srcref:`/lino/modlib/countries/models.py`

.. index::
   single: field;isocode
   
.. _dsbe.countries.Country.isocode:

Field **Country.isocode**
=========================





Type: CharField

   
.. index::
   single: field;name
   
.. _dsbe.countries.Country.name:

Field **Country.name**
======================





Type: CharField

   
.. index::
   single: field;short_code
   
.. _dsbe.countries.Country.short_code:

Field **Country.short_code**
============================





Type: CharField

   
.. index::
   single: field;iso3
   
.. _dsbe.countries.Country.iso3:

Field **Country.iso3**
======================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _dsbe.countries.Country.name_fr:

Field **Country.name_fr**
=========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _dsbe.countries.Country.name_nl:

Field **Country.name_nl**
=========================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _dsbe.countries.Country.name_en:

Field **Country.name_en**
=========================





Type: CharField

   


.. index::
   pair: model; City

.. _dsbe.countries.City:

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
   
.. _dsbe.countries.City.id:

Field **City.id**
=================





Type: AutoField

   
.. index::
   single: field;name
   
.. _dsbe.countries.City.name:

Field **City.name**
===================





Type: CharField

   
.. index::
   single: field;country
   
.. _dsbe.countries.City.country:

Field **City.country**
======================





Type: ForeignKey

   
.. index::
   single: field;zip_code
   
.. _dsbe.countries.City.zip_code:

Field **City.zip_code**
=======================





Type: CharField

   


