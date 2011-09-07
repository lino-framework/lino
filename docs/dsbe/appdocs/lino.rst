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
  
============================ ============ ======================================================================================================
name                         type         verbose name                                                                                          
============================ ============ ======================================================================================================
id                           AutoField    ID                                                                                                    
default_build_method         CharField    Default build method (Standard-Konstruktionsmethode,Méthode de constuction par défault)               
next_partner_id              IntegerField The next automatic id for Person or Company (Nächste Partnernummer)                                   
site_company                 ForeignKey   The company that runs this site (Firma, die diesen Site betreibt,La société ou tourne ce site)        
job_office                   ForeignKey   Local job office (Lokales Arbeitsamt,Agence locale pour l'emploi ?)                                   
propgroup_skills             ForeignKey   Skills Property Group (Eigenschaftsgruppe Fähigkeiten,Groupe de propriétés 'Skills')                  
propgroup_softskills         ForeignKey   Soft Skills Property Group (Eigenschaftsgruppe Sozialkompetenzen,Groupe de propriétés 'Soft Skills')  
propgroup_obstacles          ForeignKey   Obstacles Property Group (Eigenschaftsgruppe Hindernisse,Groupe de propriétés 'Obstacles')            
residence_permit_upload_type ForeignKey   Upload Type for residence permit (Upload-Art Aufenthaltserlaubnis,Type d'upload "permis de résidence")
work_permit_upload_type      ForeignKey   Upload Type for work permit (Upload-Art Arbeitserlaubnis,Type d'upload "permis de travail")           
driving_licence_upload_type  ForeignKey   Upload Type for driving licence (Upload-Art Führerschein,Type d'upload "permis de conduire")          
============================ ============ ======================================================================================================

    
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
   single: field;next_partner_id
   
.. _lino.lino.SiteConfig.next_partner_id:

Field **SiteConfig.next_partner_id**
====================================





Type: IntegerField

   
.. index::
   single: field;site_company
   
.. _lino.lino.SiteConfig.site_company:

Field **SiteConfig.site_company**
=================================





Type: ForeignKey

   
.. index::
   single: field;job_office
   
.. _lino.lino.SiteConfig.job_office:

Field **SiteConfig.job_office**
===============================





Type: ForeignKey

   
.. index::
   single: field;propgroup_skills
   
.. _lino.lino.SiteConfig.propgroup_skills:

Field **SiteConfig.propgroup_skills**
=====================================





Type: ForeignKey

   
.. index::
   single: field;propgroup_softskills
   
.. _lino.lino.SiteConfig.propgroup_softskills:

Field **SiteConfig.propgroup_softskills**
=========================================





Type: ForeignKey

   
.. index::
   single: field;propgroup_obstacles
   
.. _lino.lino.SiteConfig.propgroup_obstacles:

Field **SiteConfig.propgroup_obstacles**
========================================





Type: ForeignKey

   
.. index::
   single: field;residence_permit_upload_type
   
.. _lino.lino.SiteConfig.residence_permit_upload_type:

Field **SiteConfig.residence_permit_upload_type**
=================================================





Type: ForeignKey

   
.. index::
   single: field;work_permit_upload_type
   
.. _lino.lino.SiteConfig.work_permit_upload_type:

Field **SiteConfig.work_permit_upload_type**
============================================





Type: ForeignKey

   
.. index::
   single: field;driving_licence_upload_type
   
.. _lino.lino.SiteConfig.driving_licence_upload_type:

Field **SiteConfig.driving_licence_upload_type**
================================================





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
    
  
=========== ============= ======================================
name        type          verbose name                          
=========== ============= ======================================
id          AutoField     ID                                    
user        ForeignKey    User (Benutzer,Utilisateur)           
name        CharField     Designation (Beschreibung,Désignation)
description RichTextField Description (Beschreibung)            
text        RichTextField Template Text (Vorlagentext)          
=========== ============= ======================================

    
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

   


