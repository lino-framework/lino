=====
sales
=====



.. currentmodule:: sales

Defined in :srcref:`/lino/modlib/sales/models.py`





.. contents:: Table of Contents



.. index::
   pair: model; PaymentTerm

.. _igen.sales.PaymentTerm:

---------------------
Model **PaymentTerm**
---------------------



Represents a convention on how an Invoice should be paid. 
    
  
======= ============== ===============
name    type           verbose name   
======= ============== ===============
id      CharField      id             
name    BabelCharField name           
days    IntegerField   days (Tage)    
months  IntegerField   months (Monate)
name_de CharField      name (de)      
name_fr CharField      name (fr)      
name_nl CharField      name (nl)      
name_et CharField      name (et)      
======= ============== ===============

    
Defined in :srcref:`/lino/modlib/sales/models.py`

.. index::
   single: field;id
   
.. _igen.sales.PaymentTerm.id:

Field **PaymentTerm.id**
========================





Type: CharField

   
.. index::
   single: field;name
   
.. _igen.sales.PaymentTerm.name:

Field **PaymentTerm.name**
==========================





Type: BabelCharField

   
.. index::
   single: field;days
   
.. _igen.sales.PaymentTerm.days:

Field **PaymentTerm.days**
==========================





Type: IntegerField

   
.. index::
   single: field;months
   
.. _igen.sales.PaymentTerm.months:

Field **PaymentTerm.months**
============================





Type: IntegerField

   
.. index::
   single: field;name_de
   
.. _igen.sales.PaymentTerm.name_de:

Field **PaymentTerm.name_de**
=============================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _igen.sales.PaymentTerm.name_fr:

Field **PaymentTerm.name_fr**
=============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _igen.sales.PaymentTerm.name_nl:

Field **PaymentTerm.name_nl**
=============================





Type: CharField

   
.. index::
   single: field;name_et
   
.. _igen.sales.PaymentTerm.name_et:

Field **PaymentTerm.name_et**
=============================





Type: CharField

   


.. index::
   pair: model; InvoicingMode

.. _igen.sales.InvoicingMode:

-----------------------
Model **InvoicingMode**
-----------------------



Represents a method of issuing/sending invoices.
    
  
============ =============== ===================================
name         type            verbose name                       
============ =============== ===================================
build_method CharField       Build method (Konstruktionsmethode)
template     CharField       Template (Vorlage)                 
id           CharField       id                                 
journal      ForeignKey      journal                            
name         BabelCharField  name                               
price        PriceField      price                              
channel      ChoiceListField channel                            
advance_days IntegerField    advance days                       
name_de      CharField       name (de)                          
name_fr      CharField       name (fr)                          
name_nl      CharField       name (nl)                          
name_et      CharField       name (et)                          
============ =============== ===================================

    
Defined in :srcref:`/lino/modlib/sales/models.py`

.. index::
   single: field;build_method
   
.. _igen.sales.InvoicingMode.build_method:

Field **InvoicingMode.build_method**
====================================





Type: CharField

   
.. index::
   single: field;template
   
.. _igen.sales.InvoicingMode.template:

Field **InvoicingMode.template**
================================





Type: CharField

   
.. index::
   single: field;id
   
.. _igen.sales.InvoicingMode.id:

Field **InvoicingMode.id**
==========================





Type: CharField

   
.. index::
   single: field;journal
   
.. _igen.sales.InvoicingMode.journal:

Field **InvoicingMode.journal**
===============================





Type: ForeignKey

   
.. index::
   single: field;name
   
.. _igen.sales.InvoicingMode.name:

Field **InvoicingMode.name**
============================





Type: BabelCharField

   
.. index::
   single: field;price
   
.. _igen.sales.InvoicingMode.price:

Field **InvoicingMode.price**
=============================





Type: PriceField

   
.. index::
   single: field;channel
   
.. _igen.sales.InvoicingMode.channel:

Field **InvoicingMode.channel**
===============================




        Method used to send the invoice.

Type: ChoiceListField

   
.. index::
   single: field;advance_days
   
.. _igen.sales.InvoicingMode.advance_days:

Field **InvoicingMode.advance_days**
====================================




    Invoices must be sent out X days in advance so that the customer
    has a chance to pay them in time. 
    

Type: IntegerField

   
.. index::
   single: field;name_de
   
.. _igen.sales.InvoicingMode.name_de:

Field **InvoicingMode.name_de**
===============================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _igen.sales.InvoicingMode.name_fr:

Field **InvoicingMode.name_fr**
===============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _igen.sales.InvoicingMode.name_nl:

Field **InvoicingMode.name_nl**
===============================





Type: CharField

   
.. index::
   single: field;name_et
   
.. _igen.sales.InvoicingMode.name_et:

Field **InvoicingMode.name_et**
===============================





Type: CharField

   


.. index::
   pair: model; ShippingMode

.. _igen.sales.ShippingMode:

----------------------
Model **ShippingMode**
----------------------



ShippingMode(id, name, price, name_de, name_fr, name_nl, name_et)
  
======= ============== ============
name    type           verbose name
======= ============== ============
id      CharField      id          
name    BabelCharField name        
price   PriceField     price       
name_de CharField      name (de)   
name_fr CharField      name (fr)   
name_nl CharField      name (nl)   
name_et CharField      name (et)   
======= ============== ============

    
Defined in :srcref:`/lino/modlib/sales/models.py`

.. index::
   single: field;id
   
.. _igen.sales.ShippingMode.id:

Field **ShippingMode.id**
=========================





Type: CharField

   
.. index::
   single: field;name
   
.. _igen.sales.ShippingMode.name:

Field **ShippingMode.name**
===========================





Type: BabelCharField

   
.. index::
   single: field;price
   
.. _igen.sales.ShippingMode.price:

Field **ShippingMode.price**
============================





Type: PriceField

   
.. index::
   single: field;name_de
   
.. _igen.sales.ShippingMode.name_de:

Field **ShippingMode.name_de**
==============================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _igen.sales.ShippingMode.name_fr:

Field **ShippingMode.name_fr**
==============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _igen.sales.ShippingMode.name_nl:

Field **ShippingMode.name_nl**
==============================





Type: CharField

   
.. index::
   single: field;name_et
   
.. _igen.sales.ShippingMode.name_et:

Field **ShippingMode.name_et**
==============================





Type: CharField

   


.. index::
   pair: model; SalesRule

.. _igen.sales.SalesRule:

-------------------
Model **SalesRule**
-------------------



Represents a group of default values for certain parameters of a SalesDocument.
    
  
============= ========== ================================
name          type       verbose name                    
============= ========== ================================
id            AutoField  ID                              
journal       ForeignKey journal                         
imode         ForeignKey imode                           
shipping_mode ForeignKey shipping mode                   
payment_term  ForeignKey payment term (Tasumistingimused)
============= ========== ================================

    
Defined in :srcref:`/lino/modlib/sales/models.py`

.. index::
   single: field;id
   
.. _igen.sales.SalesRule.id:

Field **SalesRule.id**
======================





Type: AutoField

   
.. index::
   single: field;journal
   
.. _igen.sales.SalesRule.journal:

Field **SalesRule.journal**
===========================





Type: ForeignKey

   
.. index::
   single: field;imode
   
.. _igen.sales.SalesRule.imode:

Field **SalesRule.imode**
=========================





Type: ForeignKey

   
.. index::
   single: field;shipping_mode
   
.. _igen.sales.SalesRule.shipping_mode:

Field **SalesRule.shipping_mode**
=================================





Type: ForeignKey

   
.. index::
   single: field;payment_term
   
.. _igen.sales.SalesRule.payment_term:

Field **SalesRule.payment_term**
================================





Type: ForeignKey

   


.. index::
   pair: model; SalesDocument

.. _igen.sales.SalesDocument:

-----------------------
Model **SalesDocument**
-----------------------



Common base class for :class:`Order` and :class:`Invoice`.
    
  
============= ============= ==================================
name          type          verbose name                      
============= ============= ==================================
id            AutoField     ID                                
must_build    BooleanField  must build (muss generiert werden)
person        ForeignKey    Person (Isik)                     
company       ForeignKey    Company (Firma)                   
contact       ForeignKey    represented by                    
language      LanguageField Language (Sprache)                
journal       ForeignKey    journal                           
number        IntegerField  number                            
sent_time     DateTimeField sent time                         
creation_date DateField     creation date                     
your_ref      CharField     your ref                          
imode         ForeignKey    imode                             
shipping_mode ForeignKey    shipping mode                     
payment_term  ForeignKey    payment term (Tasumistingimused)  
sales_remark  CharField     Remark for sales                  
subject       CharField     Subject line                      
vat_exempt    BooleanField  vat exempt                        
item_vat      BooleanField  item vat                          
total_excl    PriceField    total excl                        
total_vat     PriceField    total vat                         
intro         TextField     Introductive Text                 
user          ForeignKey    user (Benutzer)                   
============= ============= ==================================

    
Defined in :srcref:`/lino/modlib/sales/models.py`

.. index::
   single: field;id
   
.. _igen.sales.SalesDocument.id:

Field **SalesDocument.id**
==========================





Type: AutoField

   
.. index::
   single: field;must_build
   
.. _igen.sales.SalesDocument.must_build:

Field **SalesDocument.must_build**
==================================





Type: BooleanField

   
.. index::
   single: field;person
   
.. _igen.sales.SalesDocument.person:

Field **SalesDocument.person**
==============================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _igen.sales.SalesDocument.company:

Field **SalesDocument.company**
===============================





Type: ForeignKey

   
.. index::
   single: field;contact
   
.. _igen.sales.SalesDocument.contact:

Field **SalesDocument.contact**
===============================





Type: ForeignKey

   
.. index::
   single: field;language
   
.. _igen.sales.SalesDocument.language:

Field **SalesDocument.language**
================================





Type: LanguageField

   
.. index::
   single: field;journal
   
.. _igen.sales.SalesDocument.journal:

Field **SalesDocument.journal**
===============================





Type: ForeignKey

   
.. index::
   single: field;number
   
.. _igen.sales.SalesDocument.number:

Field **SalesDocument.number**
==============================





Type: IntegerField

   
.. index::
   single: field;sent_time
   
.. _igen.sales.SalesDocument.sent_time:

Field **SalesDocument.sent_time**
=================================





Type: DateTimeField

   
.. index::
   single: field;creation_date
   
.. _igen.sales.SalesDocument.creation_date:

Field **SalesDocument.creation_date**
=====================================





Type: DateField

   
.. index::
   single: field;your_ref
   
.. _igen.sales.SalesDocument.your_ref:

Field **SalesDocument.your_ref**
================================





Type: CharField

   
.. index::
   single: field;imode
   
.. _igen.sales.SalesDocument.imode:

Field **SalesDocument.imode**
=============================





Type: ForeignKey

   
.. index::
   single: field;shipping_mode
   
.. _igen.sales.SalesDocument.shipping_mode:

Field **SalesDocument.shipping_mode**
=====================================





Type: ForeignKey

   
.. index::
   single: field;payment_term
   
.. _igen.sales.SalesDocument.payment_term:

Field **SalesDocument.payment_term**
====================================





Type: ForeignKey

   
.. index::
   single: field;sales_remark
   
.. _igen.sales.SalesDocument.sales_remark:

Field **SalesDocument.sales_remark**
====================================





Type: CharField

   
.. index::
   single: field;subject
   
.. _igen.sales.SalesDocument.subject:

Field **SalesDocument.subject**
===============================





Type: CharField

   
.. index::
   single: field;vat_exempt
   
.. _igen.sales.SalesDocument.vat_exempt:

Field **SalesDocument.vat_exempt**
==================================





Type: BooleanField

   
.. index::
   single: field;item_vat
   
.. _igen.sales.SalesDocument.item_vat:

Field **SalesDocument.item_vat**
================================





Type: BooleanField

   
.. index::
   single: field;total_excl
   
.. _igen.sales.SalesDocument.total_excl:

Field **SalesDocument.total_excl**
==================================





Type: PriceField

   
.. index::
   single: field;total_vat
   
.. _igen.sales.SalesDocument.total_vat:

Field **SalesDocument.total_vat**
=================================





Type: PriceField

   
.. index::
   single: field;intro
   
.. _igen.sales.SalesDocument.intro:

Field **SalesDocument.intro**
=============================





Type: TextField

   
.. index::
   single: field;user
   
.. _igen.sales.SalesDocument.user:

Field **SalesDocument.user**
============================





Type: ForeignKey

   


.. index::
   pair: model; Order

.. _igen.sales.Order:

---------------
Model **Order**
---------------



Order(id, must_build, person_id, company_id, contact_id, language, journal_id, number, sent_time, creation_date, your_ref, imode_id, shipping_mode_id, payment_term_id, sales_remark, subject, vat_exempt, item_vat, total_excl, total_vat, intro, user_id, salesdocument_ptr_id, cycle, start_date, covered_until)
  
================= ============= ==================================
name              type          verbose name                      
================= ============= ==================================
id                AutoField     ID                                
must_build        BooleanField  must build (muss generiert werden)
person            ForeignKey    Person (Isik)                     
company           ForeignKey    Company (Firma)                   
contact           ForeignKey    represented by                    
language          LanguageField Language (Sprache)                
journal           ForeignKey    journal                           
number            IntegerField  number                            
sent_time         DateTimeField sent time                         
creation_date     DateField     creation date                     
your_ref          CharField     your ref                          
imode             ForeignKey    imode                             
shipping_mode     ForeignKey    shipping mode                     
payment_term      ForeignKey    payment term (Tasumistingimused)  
sales_remark      CharField     Remark for sales                  
subject           CharField     Subject line                      
vat_exempt        BooleanField  vat exempt                        
item_vat          BooleanField  item vat                          
total_excl        PriceField    total excl                        
total_vat         PriceField    total vat                         
intro             TextField     Introductive Text                 
user              ForeignKey    user (Benutzer)                   
salesdocument_ptr OneToOneField salesdocument ptr                 
cycle             CharField     cycle                             
start_date        MyDateField   start date                        
covered_until     MyDateField   covered until                     
================= ============= ==================================

    
Defined in :srcref:`/lino/modlib/sales/models.py`

.. index::
   single: field;id
   
.. _igen.sales.Order.id:

Field **Order.id**
==================





Type: AutoField

   
.. index::
   single: field;must_build
   
.. _igen.sales.Order.must_build:

Field **Order.must_build**
==========================





Type: BooleanField

   
.. index::
   single: field;person
   
.. _igen.sales.Order.person:

Field **Order.person**
======================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _igen.sales.Order.company:

Field **Order.company**
=======================





Type: ForeignKey

   
.. index::
   single: field;contact
   
.. _igen.sales.Order.contact:

Field **Order.contact**
=======================





Type: ForeignKey

   
.. index::
   single: field;language
   
.. _igen.sales.Order.language:

Field **Order.language**
========================





Type: LanguageField

   
.. index::
   single: field;journal
   
.. _igen.sales.Order.journal:

Field **Order.journal**
=======================





Type: ForeignKey

   
.. index::
   single: field;number
   
.. _igen.sales.Order.number:

Field **Order.number**
======================





Type: IntegerField

   
.. index::
   single: field;sent_time
   
.. _igen.sales.Order.sent_time:

Field **Order.sent_time**
=========================





Type: DateTimeField

   
.. index::
   single: field;creation_date
   
.. _igen.sales.Order.creation_date:

Field **Order.creation_date**
=============================





Type: DateField

   
.. index::
   single: field;your_ref
   
.. _igen.sales.Order.your_ref:

Field **Order.your_ref**
========================





Type: CharField

   
.. index::
   single: field;imode
   
.. _igen.sales.Order.imode:

Field **Order.imode**
=====================





Type: ForeignKey

   
.. index::
   single: field;shipping_mode
   
.. _igen.sales.Order.shipping_mode:

Field **Order.shipping_mode**
=============================





Type: ForeignKey

   
.. index::
   single: field;payment_term
   
.. _igen.sales.Order.payment_term:

Field **Order.payment_term**
============================





Type: ForeignKey

   
.. index::
   single: field;sales_remark
   
.. _igen.sales.Order.sales_remark:

Field **Order.sales_remark**
============================





Type: CharField

   
.. index::
   single: field;subject
   
.. _igen.sales.Order.subject:

Field **Order.subject**
=======================





Type: CharField

   
.. index::
   single: field;vat_exempt
   
.. _igen.sales.Order.vat_exempt:

Field **Order.vat_exempt**
==========================





Type: BooleanField

   
.. index::
   single: field;item_vat
   
.. _igen.sales.Order.item_vat:

Field **Order.item_vat**
========================





Type: BooleanField

   
.. index::
   single: field;total_excl
   
.. _igen.sales.Order.total_excl:

Field **Order.total_excl**
==========================





Type: PriceField

   
.. index::
   single: field;total_vat
   
.. _igen.sales.Order.total_vat:

Field **Order.total_vat**
=========================





Type: PriceField

   
.. index::
   single: field;intro
   
.. _igen.sales.Order.intro:

Field **Order.intro**
=====================





Type: TextField

   
.. index::
   single: field;user
   
.. _igen.sales.Order.user:

Field **Order.user**
====================





Type: ForeignKey

   
.. index::
   single: field;salesdocument_ptr
   
.. _igen.sales.Order.salesdocument_ptr:

Field **Order.salesdocument_ptr**
=================================





Type: OneToOneField

   
.. index::
   single: field;cycle
   
.. _igen.sales.Order.cycle:

Field **Order.cycle**
=====================





Type: CharField

   
.. index::
   single: field;start_date
   
.. _igen.sales.Order.start_date:

Field **Order.start_date**
==========================



Beginning of payable period. 
      Set to blank if no bill should be generated

Type: MyDateField

   
.. index::
   single: field;covered_until
   
.. _igen.sales.Order.covered_until:

Field **Order.covered_until**
=============================





Type: MyDateField

   


.. index::
   pair: model; Invoice

.. _igen.sales.Invoice:

-----------------
Model **Invoice**
-----------------



Invoice(id, must_build, person_id, company_id, contact_id, language, journal_id, number, sent_time, creation_date, your_ref, imode_id, shipping_mode_id, payment_term_id, sales_remark, subject, vat_exempt, item_vat, total_excl, total_vat, intro, user_id, salesdocument_ptr_id, journal_id, number, value_date, ledger_remark, booked, due_date, order_id)
  
================= ============= ==================================
name              type          verbose name                      
================= ============= ==================================
id                AutoField     ID                                
must_build        BooleanField  must build (muss generiert werden)
person            ForeignKey    Person (Isik)                     
company           ForeignKey    Company (Firma)                   
contact           ForeignKey    represented by                    
language          LanguageField Language (Sprache)                
journal           ForeignKey    journal                           
number            IntegerField  number                            
sent_time         DateTimeField sent time                         
creation_date     DateField     creation date                     
your_ref          CharField     your ref                          
imode             ForeignKey    imode                             
shipping_mode     ForeignKey    shipping mode                     
payment_term      ForeignKey    payment term (Tasumistingimused)  
sales_remark      CharField     Remark for sales                  
subject           CharField     Subject line                      
vat_exempt        BooleanField  vat exempt                        
item_vat          BooleanField  item vat                          
total_excl        PriceField    total excl                        
total_vat         PriceField    total vat                         
intro             TextField     Introductive Text                 
user              ForeignKey    user (Benutzer)                   
salesdocument_ptr OneToOneField salesdocument ptr                 
journal           ForeignKey    journal                           
number            IntegerField  number                            
value_date        DateField     value date                        
ledger_remark     CharField     Remark for ledger                 
booked            BooleanField  booked                            
due_date          MyDateField   Payable until                     
order             ForeignKey    order                             
================= ============= ==================================

    
Defined in :srcref:`/lino/modlib/sales/models.py`

.. index::
   single: field;id
   
.. _igen.sales.Invoice.id:

Field **Invoice.id**
====================





Type: AutoField

   
.. index::
   single: field;must_build
   
.. _igen.sales.Invoice.must_build:

Field **Invoice.must_build**
============================





Type: BooleanField

   
.. index::
   single: field;person
   
.. _igen.sales.Invoice.person:

Field **Invoice.person**
========================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _igen.sales.Invoice.company:

Field **Invoice.company**
=========================





Type: ForeignKey

   
.. index::
   single: field;contact
   
.. _igen.sales.Invoice.contact:

Field **Invoice.contact**
=========================





Type: ForeignKey

   
.. index::
   single: field;language
   
.. _igen.sales.Invoice.language:

Field **Invoice.language**
==========================





Type: LanguageField

   
.. index::
   single: field;journal
   
.. _igen.sales.Invoice.journal:

Field **Invoice.journal**
=========================





Type: ForeignKey

   
.. index::
   single: field;number
   
.. _igen.sales.Invoice.number:

Field **Invoice.number**
========================





Type: IntegerField

   
.. index::
   single: field;sent_time
   
.. _igen.sales.Invoice.sent_time:

Field **Invoice.sent_time**
===========================





Type: DateTimeField

   
.. index::
   single: field;creation_date
   
.. _igen.sales.Invoice.creation_date:

Field **Invoice.creation_date**
===============================





Type: DateField

   
.. index::
   single: field;your_ref
   
.. _igen.sales.Invoice.your_ref:

Field **Invoice.your_ref**
==========================





Type: CharField

   
.. index::
   single: field;imode
   
.. _igen.sales.Invoice.imode:

Field **Invoice.imode**
=======================





Type: ForeignKey

   
.. index::
   single: field;shipping_mode
   
.. _igen.sales.Invoice.shipping_mode:

Field **Invoice.shipping_mode**
===============================





Type: ForeignKey

   
.. index::
   single: field;payment_term
   
.. _igen.sales.Invoice.payment_term:

Field **Invoice.payment_term**
==============================





Type: ForeignKey

   
.. index::
   single: field;sales_remark
   
.. _igen.sales.Invoice.sales_remark:

Field **Invoice.sales_remark**
==============================





Type: CharField

   
.. index::
   single: field;subject
   
.. _igen.sales.Invoice.subject:

Field **Invoice.subject**
=========================





Type: CharField

   
.. index::
   single: field;vat_exempt
   
.. _igen.sales.Invoice.vat_exempt:

Field **Invoice.vat_exempt**
============================





Type: BooleanField

   
.. index::
   single: field;item_vat
   
.. _igen.sales.Invoice.item_vat:

Field **Invoice.item_vat**
==========================





Type: BooleanField

   
.. index::
   single: field;total_excl
   
.. _igen.sales.Invoice.total_excl:

Field **Invoice.total_excl**
============================





Type: PriceField

   
.. index::
   single: field;total_vat
   
.. _igen.sales.Invoice.total_vat:

Field **Invoice.total_vat**
===========================





Type: PriceField

   
.. index::
   single: field;intro
   
.. _igen.sales.Invoice.intro:

Field **Invoice.intro**
=======================





Type: TextField

   
.. index::
   single: field;user
   
.. _igen.sales.Invoice.user:

Field **Invoice.user**
======================





Type: ForeignKey

   
.. index::
   single: field;salesdocument_ptr
   
.. _igen.sales.Invoice.salesdocument_ptr:

Field **Invoice.salesdocument_ptr**
===================================





Type: OneToOneField

   
.. index::
   single: field;journal
   
.. _igen.sales.Invoice.journal:

Field **Invoice.journal**
=========================





Type: ForeignKey

   
.. index::
   single: field;number
   
.. _igen.sales.Invoice.number:

Field **Invoice.number**
========================





Type: IntegerField

   
.. index::
   single: field;value_date
   
.. _igen.sales.Invoice.value_date:

Field **Invoice.value_date**
============================





Type: DateField

   
.. index::
   single: field;ledger_remark
   
.. _igen.sales.Invoice.ledger_remark:

Field **Invoice.ledger_remark**
===============================





Type: CharField

   
.. index::
   single: field;booked
   
.. _igen.sales.Invoice.booked:

Field **Invoice.booked**
========================





Type: BooleanField

   
.. index::
   single: field;due_date
   
.. _igen.sales.Invoice.due_date:

Field **Invoice.due_date**
==========================





Type: MyDateField

   
.. index::
   single: field;order
   
.. _igen.sales.Invoice.order:

Field **Invoice.order**
=======================





Type: ForeignKey

   


.. index::
   pair: model; DocItem

.. _igen.sales.DocItem:

-----------------
Model **DocItem**
-----------------



DocItem(id, document_id, pos, product_id, title, description, discount, unit_price, qty, total)
  
=========== ============= ============
name        type          verbose name
=========== ============= ============
id          AutoField     ID          
document    ForeignKey    document    
pos         IntegerField  Position    
product     ForeignKey    product     
title       CharField     title       
description TextField     description 
discount    IntegerField  Discount %  
unit_price  PriceField    unit price  
qty         QuantityField qty         
total       PriceField    total       
=========== ============= ============

    
Defined in :srcref:`/lino/modlib/sales/models.py`

.. index::
   single: field;id
   
.. _igen.sales.DocItem.id:

Field **DocItem.id**
====================





Type: AutoField

   
.. index::
   single: field;document
   
.. _igen.sales.DocItem.document:

Field **DocItem.document**
==========================





Type: ForeignKey

   
.. index::
   single: field;pos
   
.. _igen.sales.DocItem.pos:

Field **DocItem.pos**
=====================





Type: IntegerField

   
.. index::
   single: field;product
   
.. _igen.sales.DocItem.product:

Field **DocItem.product**
=========================





Type: ForeignKey

   
.. index::
   single: field;title
   
.. _igen.sales.DocItem.title:

Field **DocItem.title**
=======================





Type: CharField

   
.. index::
   single: field;description
   
.. _igen.sales.DocItem.description:

Field **DocItem.description**
=============================





Type: TextField

   
.. index::
   single: field;discount
   
.. _igen.sales.DocItem.discount:

Field **DocItem.discount**
==========================





Type: IntegerField

   
.. index::
   single: field;unit_price
   
.. _igen.sales.DocItem.unit_price:

Field **DocItem.unit_price**
============================





Type: PriceField

   
.. index::
   single: field;qty
   
.. _igen.sales.DocItem.qty:

Field **DocItem.qty**
=====================





Type: QuantityField

   
.. index::
   single: field;total
   
.. _igen.sales.DocItem.total:

Field **DocItem.total**
=======================





Type: PriceField

   


