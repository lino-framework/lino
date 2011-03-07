====
lino
====



.. currentmodule:: lino

Defined in :srcref:`/lino/models.py`




.. index::
   pair: model; SiteConfig
   single: field;id
   single: field;default_build_method
   single: field;site_company
   single: field;next_partner_id
   single: field;propgroup_skills
   single: field;propgroup_softskills
   single: field;propgroup_obstacles
   single: field;job_office

.. _dsbe.lino.SiteConfig:

--------------------
Model ``SiteConfig``
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


