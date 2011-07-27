====
lino
====



.. currentmodule:: lino

Defined in :srcref:`/lino/models.py`



.. contents:: Table of Contents



.. index::
   pair: model; SiteConfig

.. _lino.lino.SiteConfig:

--------------------
Model **SiteConfig**
--------------------



SiteConfig(id, default_build_method)
  
==================== ========== ==============================================================================================
name                 type       verbose name                                                                                  
==================== ========== ==============================================================================================
id                   AutoField  ID                                                                                            
default_build_method CharField  Default build method (Standard-Konstruktionsmethode,Méthode de constuction par défault)       
site_company         ForeignKey The company that runs this site (Firma, die diesen Site betreibt,La société ou tourne ce site)
sales_base_account   ForeignKey Sales base account                                                                            
sales_vat_account    ForeignKey Sales VAT account                                                                             
==================== ========== ==============================================================================================

    
Defined in :srcref:`/lino/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.lino.SiteConfig.id:

Field **SiteConfig.id**
=======================





Type: AutoField

   
.. index::
   single: field;default_build_method
   
.. _lino.lino.SiteConfig.default_build_method:

Field **SiteConfig.default_build_method**
=========================================





Type: CharField

   
.. index::
   single: field;site_company
   
.. _lino.lino.SiteConfig.site_company:

Field **SiteConfig.site_company**
=================================





Type: ForeignKey

   
.. index::
   single: field;sales_base_account
   
.. _lino.lino.SiteConfig.sales_base_account:

Field **SiteConfig.sales_base_account**
=======================================





Type: ForeignKey

   
.. index::
   single: field;sales_vat_account
   
.. _lino.lino.SiteConfig.sales_vat_account:

Field **SiteConfig.sales_vat_account**
======================================





Type: ForeignKey

   


.. index::
   pair: model; DataControlListing

.. _lino.lino.DataControlListing:

----------------------------
Model **DataControlListing**
----------------------------



Performs a "soft integrity test" on the database. 
    Prints 
    
  
========== ============ ======================================================
name       type         verbose name                                          
========== ============ ======================================================
id         AutoField    ID                                                    
must_build BooleanField must build (muss generiert werden,doit être construit)
date       DateField    Date (Datum)                                          
========== ============ ======================================================

    
Defined in :srcref:`/lino/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.lino.DataControlListing.id:

Field **DataControlListing.id**
===============================





Type: AutoField

   
.. index::
   single: field;must_build
   
.. _lino.lino.DataControlListing.must_build:

Field **DataControlListing.must_build**
=======================================





Type: BooleanField

   
.. index::
   single: field;date
   
.. _lino.lino.DataControlListing.date:

Field **DataControlListing.date**
=================================





Type: DateField

   


.. index::
   pair: model; TextFieldTemplate

.. _lino.lino.TextFieldTemplate:

---------------------------
Model **TextFieldTemplate**
---------------------------



A reusable block of text that can be selected from a text editor to be 
    inserted into the text being edited.
    
  
=========== ============= ==============================================
name        type          verbose name                                  
=========== ============= ==============================================
id          AutoField     ID                                            
user        ForeignKey    user (Benutzer,utilisateur)                   
name        CharField     Designation (Beschreibung,Désignation,Nimetus)
description RichTextField Description (Beschreibung)                    
text        RichTextField Template Text (Vorlagentext)                  
=========== ============= ==============================================

    
Defined in :srcref:`/lino/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.lino.TextFieldTemplate.id:

Field **TextFieldTemplate.id**
==============================





Type: AutoField

   
.. index::
   single: field;user
   
.. _lino.lino.TextFieldTemplate.user:

Field **TextFieldTemplate.user**
================================





Type: ForeignKey

   
.. index::
   single: field;name
   
.. _lino.lino.TextFieldTemplate.name:

Field **TextFieldTemplate.name**
================================





Type: CharField

   
.. index::
   single: field;description
   
.. _lino.lino.TextFieldTemplate.description:

Field **TextFieldTemplate.description**
=======================================





Type: RichTextField

   
.. index::
   single: field;text
   
.. _lino.lino.TextFieldTemplate.text:

Field **TextFieldTemplate.text**
================================





Type: RichTextField

   


