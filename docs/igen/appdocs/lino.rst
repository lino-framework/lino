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
  
==================== ============ ====================================================
name                 type         verbose name                                        
==================== ============ ====================================================
id                   AutoField    ID                                                  
default_build_method CharField    Default build method (Standard-Konstruktionsmethode)
site_company         ForeignKey   The company that runs this site                     
next_partner_id      IntegerField The next automatic id for Person or Company         
sales_base_account   ForeignKey   Sales base account                                  
sales_vat_account    ForeignKey   Sales VAT account                                   
==================== ============ ====================================================

    
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
   single: field;sales_base_account
   
.. _std.lino.SiteConfig.sales_base_account:

Field **SiteConfig.sales_base_account**
=======================================





Type: ForeignKey

   
.. index::
   single: field;sales_vat_account
   
.. _std.lino.SiteConfig.sales_vat_account:

Field **SiteConfig.sales_vat_account**
======================================





Type: ForeignKey

   


