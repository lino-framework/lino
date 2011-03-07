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
   single: field;sales_base_account
   single: field;sales_vat_account

.. _igen.lino.SiteConfig:

--------------------
Model ``SiteConfig``
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


