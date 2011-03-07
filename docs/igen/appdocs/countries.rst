=========
countries
=========



.. currentmodule:: countries

Defined in :srcref:`/lino/modlib/countries/models.py`




.. index::
   pair: model; Language
   single: field;id
   single: field;name
   single: field;iso2
   single: field;name_de
   single: field;name_fr
   single: field;name_nl
   single: field;name_et

.. _igen.countries.Language:

------------------
Model ``Language``
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
   pair: model; Country
   single: field;isocode
   single: field;name
   single: field;short_code
   single: field;iso3
   single: field;name_de
   single: field;name_fr
   single: field;name_nl
   single: field;name_et

.. _igen.countries.Country:

-----------------
Model ``Country``
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
   pair: model; City
   single: field;id
   single: field;name
   single: field;country
   single: field;zip_code

.. _igen.countries.City:

--------------
Model ``City``
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


