====
lino
====



.. currentmodule:: lino

Defined in :srcref:`/lino/models.py`



.. contents:: Table of Contents



.. index::
   pair: model; SiteConfig

.. _std.lino.SiteConfig:

--------------------
Model **SiteConfig**
--------------------



SiteConfig(id, default_build_method)
  
==================== ============ ===================================================================
name                 type         verbose name                                                       
==================== ============ ===================================================================
id                   AutoField    ID                                                                 
default_build_method CharField    Default build method (Standard-Konstruktionsmethode)               
site_company         ForeignKey   The company that runs this site                                    
next_partner_id      IntegerField The next automatic id for Person or Company                        
propgroup_skills     ForeignKey   Skills Property Group (Eigenschaftsgruppe "Fachkompetenzen")       
propgroup_softskills ForeignKey   Soft Skills Property Group (Eigenschaftsgruppe "Sozialkompetenzen")
propgroup_obstacles  ForeignKey   Obstacles Property Group (Eigenschaftsgruppe "Hindernisse")        
job_office           ForeignKey   Local job office (Lokales Arbeitsamt)                              
==================== ============ ===================================================================

    
Defined in :srcref:`/lino/models.py`

.. index::
   single: field;id
   
.. _std.lino.SiteConfig.id:

Field **SiteConfig.id**
=======================





Type: AutoField

   
.. index::
   single: field;default_build_method
   
.. _std.lino.SiteConfig.default_build_method:

Field **SiteConfig.default_build_method**
=========================================





Type: CharField

   
.. index::
   single: field;site_company
   
.. _std.lino.SiteConfig.site_company:

Field **SiteConfig.site_company**
=================================





Type: ForeignKey

   
.. index::
   single: field;next_partner_id
   
.. _std.lino.SiteConfig.next_partner_id:

Field **SiteConfig.next_partner_id**
====================================





Type: IntegerField

   
.. index::
   single: field;propgroup_skills
   
.. _std.lino.SiteConfig.propgroup_skills:

Field **SiteConfig.propgroup_skills**
=====================================





Type: ForeignKey

   
.. index::
   single: field;propgroup_softskills
   
.. _std.lino.SiteConfig.propgroup_softskills:

Field **SiteConfig.propgroup_softskills**
=========================================





Type: ForeignKey

   
.. index::
   single: field;propgroup_obstacles
   
.. _std.lino.SiteConfig.propgroup_obstacles:

Field **SiteConfig.propgroup_obstacles**
========================================





Type: ForeignKey

   
.. index::
   single: field;job_office
   
.. _std.lino.SiteConfig.job_office:

Field **SiteConfig.job_office**
===============================





Type: ForeignKey

   


