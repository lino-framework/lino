=====
sales
=====



.. currentmodule:: sales

Defined in :srcref:`/lino/modlib/sales/models.py`





.. contents:: Table of Contents



.. index::
   pair: model; PaymentTerm

.. _lino.sales.PaymentTerm:

---------------------
Model **PaymentTerm**
---------------------



Represents a convention on how an Invoice should be paid. 
    
  
======= ============== ====================
name    type           verbose name        
======= ============== ====================
id      CharField      id                  
name    BabelCharField name                
days    IntegerField   days (Tage,jours)   
months  IntegerField   months (Monate,mois)
name_de CharField      name (de)           
name_fr CharField      name (fr)           
name_nl CharField      name (nl)           
name_et CharField      name (et)           
======= ============== ====================

    
Defined in :srcref:`/lino/modlib/sales/models.py`

Referenced from
`lino.contacts.Contact.payment_term`_, `lino.sales.SalesRule.payment_term`_, `lino.sales.SalesDocument.payment_term`_, `lino.sales.Order.payment_term`_, `lino.sales.Invoice.payment_term`_



.. index::
   single: field;id
   
.. _lino.sales.PaymentTerm.id:

Field **PaymentTerm.id**
========================





Type: CharField

   
.. index::
   single: field;name
   
.. _lino.sales.PaymentTerm.name:

Field **PaymentTerm.name**
==========================





Type: BabelCharField

   
.. index::
   single: field;days
   
.. _lino.sales.PaymentTerm.days:

Field **PaymentTerm.days**
==========================





Type: IntegerField

   
.. index::
   single: field;months
   
.. _lino.sales.PaymentTerm.months:

Field **PaymentTerm.months**
============================





Type: IntegerField

   
.. index::
   single: field;name_de
   
.. _lino.sales.PaymentTerm.name_de:

Field **PaymentTerm.name_de**
=============================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _lino.sales.PaymentTerm.name_fr:

Field **PaymentTerm.name_fr**
=============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.sales.PaymentTerm.name_nl:

Field **PaymentTerm.name_nl**
=============================





Type: CharField

   
.. index::
   single: field;name_et
   
.. _lino.sales.PaymentTerm.name_et:

Field **PaymentTerm.name_et**
=============================





Type: CharField

   


.. index::
   pair: model; InvoicingMode

.. _lino.sales.InvoicingMode:

-----------------------
Model **InvoicingMode**
-----------------------



Represents a method of issuing/sending invoices.
    
  
============ =============== ===========================================================
name         type            verbose name                                               
============ =============== ===========================================================
build_method CharField       Build method (Konstruktionsmethode,Méthode de construction)
template     CharField       Template (Vorlage,Modèle)                                  
id           CharField       id                                                         
journal      ForeignKey      journal                                                    
name         BabelCharField  name                                                       
price        PriceField      price                                                      
channel      ChoiceListField Channel                                                    
advance_days IntegerField    advance days                                               
name_de      CharField       name (de)                                                  
name_fr      CharField       name (fr)                                                  
name_nl      CharField       name (nl)                                                  
name_et      CharField       name (et)                                                  
============ =============== ===========================================================

    
Defined in :srcref:`/lino/modlib/sales/models.py`

Referenced from
`lino.sales.SalesRule.imode`_, `lino.sales.SalesDocument.imode`_, `lino.sales.Order.imode`_, `lino.sales.Invoice.imode`_



.. index::
   single: field;build_method
   
.. _lino.sales.InvoicingMode.build_method:

Field **InvoicingMode.build_method**
====================================





Type: CharField

   
.. index::
   single: field;template
   
.. _lino.sales.InvoicingMode.template:

Field **InvoicingMode.template**
================================





Type: CharField

   
.. index::
   single: field;id
   
.. _lino.sales.InvoicingMode.id:

Field **InvoicingMode.id**
==========================





Type: CharField

   
.. index::
   single: field;journal
   
.. _lino.sales.InvoicingMode.journal:

Field **InvoicingMode.journal**
===============================





Type: ForeignKey

   
.. index::
   single: field;name
   
.. _lino.sales.InvoicingMode.name:

Field **InvoicingMode.name**
============================





Type: BabelCharField

   
.. index::
   single: field;price
   
.. _lino.sales.InvoicingMode.price:

Field **InvoicingMode.price**
=============================





Type: PriceField

   
.. index::
   single: field;channel
   
.. _lino.sales.InvoicingMode.channel:

Field **InvoicingMode.channel**
===============================




        Method used to send the invoice.

Type: ChoiceListField

   
.. index::
   single: field;advance_days
   
.. _lino.sales.InvoicingMode.advance_days:

Field **InvoicingMode.advance_days**
====================================




    Invoices must be sent out X days in advance so that the customer
    has a chance to pay them in time. 
    

Type: IntegerField

   
.. index::
   single: field;name_de
   
.. _lino.sales.InvoicingMode.name_de:

Field **InvoicingMode.name_de**
===============================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _lino.sales.InvoicingMode.name_fr:

Field **InvoicingMode.name_fr**
===============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.sales.InvoicingMode.name_nl:

Field **InvoicingMode.name_nl**
===============================





Type: CharField

   
.. index::
   single: field;name_et
   
.. _lino.sales.InvoicingMode.name_et:

Field **InvoicingMode.name_et**
===============================





Type: CharField

   


.. index::
   pair: model; ShippingMode

.. _lino.sales.ShippingMode:

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

Referenced from
`lino.sales.SalesRule.shipping_mode`_, `lino.sales.SalesDocument.shipping_mode`_, `lino.sales.Order.shipping_mode`_, `lino.sales.Invoice.shipping_mode`_



.. index::
   single: field;id
   
.. _lino.sales.ShippingMode.id:

Field **ShippingMode.id**
=========================





Type: CharField

   
.. index::
   single: field;name
   
.. _lino.sales.ShippingMode.name:

Field **ShippingMode.name**
===========================





Type: BabelCharField

   
.. index::
   single: field;price
   
.. _lino.sales.ShippingMode.price:

Field **ShippingMode.price**
============================





Type: PriceField

   
.. index::
   single: field;name_de
   
.. _lino.sales.ShippingMode.name_de:

Field **ShippingMode.name_de**
==============================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _lino.sales.ShippingMode.name_fr:

Field **ShippingMode.name_fr**
==============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.sales.ShippingMode.name_nl:

Field **ShippingMode.name_nl**
==============================





Type: CharField

   
.. index::
   single: field;name_et
   
.. _lino.sales.ShippingMode.name_et:

Field **ShippingMode.name_et**
==============================





Type: CharField

   


.. index::
   pair: model; SalesRule

.. _lino.sales.SalesRule:

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

Referenced from




.. index::
   single: field;id
   
.. _lino.sales.SalesRule.id:

Field **SalesRule.id**
======================





Type: AutoField

   
.. index::
   single: field;journal
   
.. _lino.sales.SalesRule.journal:

Field **SalesRule.journal**
===========================





Type: ForeignKey

   
.. index::
   single: field;imode
   
.. _lino.sales.SalesRule.imode:

Field **SalesRule.imode**
=========================





Type: ForeignKey

   
.. index::
   single: field;shipping_mode
   
.. _lino.sales.SalesRule.shipping_mode:

Field **SalesRule.shipping_mode**
=================================





Type: ForeignKey

   
.. index::
   single: field;payment_term
   
.. _lino.sales.SalesRule.payment_term:

Field **SalesRule.payment_term**
================================





Type: ForeignKey

   


.. index::
   pair: model; SalesDocument

.. _lino.sales.SalesDocument:

-----------------------
Model **SalesDocument**
-----------------------



Common base class for :class:`Order` and :class:`Invoice`.
    
  
============= ============= ======================================================
name          type          verbose name                                          
============= ============= ======================================================
id            AutoField     ID                                                    
must_build    BooleanField  must build (muss generiert werden,doit être construit)
person        ForeignKey    Person (Personne,Isik)                                
company       ForeignKey    Company (Firma,Société,Firma)                         
contact       ForeignKey    represented by (Vertreten durch,représenté par)       
language      LanguageField Language (Sprache,Langue)                             
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
user          ForeignKey    user (Benutzer,utilisateur)                           
============= ============= ======================================================

    
Defined in :srcref:`/lino/modlib/sales/models.py`

Referenced from
`lino.sales.Order.salesdocument_ptr`_, `lino.sales.Invoice.salesdocument_ptr`_, `lino.sales.DocItem.document`_



.. index::
   single: field;id
   
.. _lino.sales.SalesDocument.id:

Field **SalesDocument.id**
==========================





Type: AutoField

   
.. index::
   single: field;must_build
   
.. _lino.sales.SalesDocument.must_build:

Field **SalesDocument.must_build**
==================================





Type: BooleanField

   
.. index::
   single: field;person
   
.. _lino.sales.SalesDocument.person:

Field **SalesDocument.person**
==============================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _lino.sales.SalesDocument.company:

Field **SalesDocument.company**
===============================





Type: ForeignKey

   
.. index::
   single: field;contact
   
.. _lino.sales.SalesDocument.contact:

Field **SalesDocument.contact**
===============================





Type: ForeignKey

   
.. index::
   single: field;language
   
.. _lino.sales.SalesDocument.language:

Field **SalesDocument.language**
================================





Type: LanguageField

   
.. index::
   single: field;journal
   
.. _lino.sales.SalesDocument.journal:

Field **SalesDocument.journal**
===============================





Type: ForeignKey

   
.. index::
   single: field;number
   
.. _lino.sales.SalesDocument.number:

Field **SalesDocument.number**
==============================





Type: IntegerField

   
.. index::
   single: field;sent_time
   
.. _lino.sales.SalesDocument.sent_time:

Field **SalesDocument.sent_time**
=================================





Type: DateTimeField

   
.. index::
   single: field;creation_date
   
.. _lino.sales.SalesDocument.creation_date:

Field **SalesDocument.creation_date**
=====================================





Type: DateField

   
.. index::
   single: field;your_ref
   
.. _lino.sales.SalesDocument.your_ref:

Field **SalesDocument.your_ref**
================================





Type: CharField

   
.. index::
   single: field;imode
   
.. _lino.sales.SalesDocument.imode:

Field **SalesDocument.imode**
=============================





Type: ForeignKey

   
.. index::
   single: field;shipping_mode
   
.. _lino.sales.SalesDocument.shipping_mode:

Field **SalesDocument.shipping_mode**
=====================================





Type: ForeignKey

   
.. index::
   single: field;payment_term
   
.. _lino.sales.SalesDocument.payment_term:

Field **SalesDocument.payment_term**
====================================





Type: ForeignKey

   
.. index::
   single: field;sales_remark
   
.. _lino.sales.SalesDocument.sales_remark:

Field **SalesDocument.sales_remark**
====================================





Type: CharField

   
.. index::
   single: field;subject
   
.. _lino.sales.SalesDocument.subject:

Field **SalesDocument.subject**
===============================





Type: CharField

   
.. index::
   single: field;vat_exempt
   
.. _lino.sales.SalesDocument.vat_exempt:

Field **SalesDocument.vat_exempt**
==================================





Type: BooleanField

   
.. index::
   single: field;item_vat
   
.. _lino.sales.SalesDocument.item_vat:

Field **SalesDocument.item_vat**
================================





Type: BooleanField

   
.. index::
   single: field;total_excl
   
.. _lino.sales.SalesDocument.total_excl:

Field **SalesDocument.total_excl**
==================================





Type: PriceField

   
.. index::
   single: field;total_vat
   
.. _lino.sales.SalesDocument.total_vat:

Field **SalesDocument.total_vat**
=================================





Type: PriceField

   
.. index::
   single: field;intro
   
.. _lino.sales.SalesDocument.intro:

Field **SalesDocument.intro**
=============================





Type: TextField

   
.. index::
   single: field;user
   
.. _lino.sales.SalesDocument.user:

Field **SalesDocument.user**
============================





Type: ForeignKey

   


.. index::
   pair: model; Order

.. _lino.sales.Order:

---------------
Model **Order**
---------------



Order(id, must_build, person_id, company_id, contact_id, language, journal_id, number, sent_time, creation_date, your_ref, imode_id, shipping_mode_id, payment_term_id, sales_remark, subject, vat_exempt, item_vat, total_excl, total_vat, intro, user_id, salesdocument_ptr_id, cycle, start_date, covered_until)
  
================= ============= ======================================================
name              type          verbose name                                          
================= ============= ======================================================
id                AutoField     ID                                                    
must_build        BooleanField  must build (muss generiert werden,doit être construit)
person            ForeignKey    Person (Personne,Isik)                                
company           ForeignKey    Company (Firma,Société,Firma)                         
contact           ForeignKey    represented by (Vertreten durch,représenté par)       
language          LanguageField Language (Sprache,Langue)                             
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
user              ForeignKey    user (Benutzer,utilisateur)                           
salesdocument_ptr OneToOneField salesdocument ptr                                     
cycle             CharField     cycle                                                 
start_date        MyDateField   start date                                            
covered_until     MyDateField   covered until                                         
================= ============= ======================================================

    
Defined in :srcref:`/lino/modlib/sales/models.py`

Referenced from
`lino.sales.Invoice.order`_



.. index::
   single: field;id
   
.. _lino.sales.Order.id:

Field **Order.id**
==================





Type: AutoField

   
.. index::
   single: field;must_build
   
.. _lino.sales.Order.must_build:

Field **Order.must_build**
==========================





Type: BooleanField

   
.. index::
   single: field;person
   
.. _lino.sales.Order.person:

Field **Order.person**
======================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _lino.sales.Order.company:

Field **Order.company**
=======================





Type: ForeignKey

   
.. index::
   single: field;contact
   
.. _lino.sales.Order.contact:

Field **Order.contact**
=======================





Type: ForeignKey

   
.. index::
   single: field;language
   
.. _lino.sales.Order.language:

Field **Order.language**
========================





Type: LanguageField

   
.. index::
   single: field;journal
   
.. _lino.sales.Order.journal:

Field **Order.journal**
=======================





Type: ForeignKey

   
.. index::
   single: field;number
   
.. _lino.sales.Order.number:

Field **Order.number**
======================





Type: IntegerField

   
.. index::
   single: field;sent_time
   
.. _lino.sales.Order.sent_time:

Field **Order.sent_time**
=========================





Type: DateTimeField

   
.. index::
   single: field;creation_date
   
.. _lino.sales.Order.creation_date:

Field **Order.creation_date**
=============================





Type: DateField

   
.. index::
   single: field;your_ref
   
.. _lino.sales.Order.your_ref:

Field **Order.your_ref**
========================





Type: CharField

   
.. index::
   single: field;imode
   
.. _lino.sales.Order.imode:

Field **Order.imode**
=====================





Type: ForeignKey

   
.. index::
   single: field;shipping_mode
   
.. _lino.sales.Order.shipping_mode:

Field **Order.shipping_mode**
=============================





Type: ForeignKey

   
.. index::
   single: field;payment_term
   
.. _lino.sales.Order.payment_term:

Field **Order.payment_term**
============================





Type: ForeignKey

   
.. index::
   single: field;sales_remark
   
.. _lino.sales.Order.sales_remark:

Field **Order.sales_remark**
============================





Type: CharField

   
.. index::
   single: field;subject
   
.. _lino.sales.Order.subject:

Field **Order.subject**
=======================





Type: CharField

   
.. index::
   single: field;vat_exempt
   
.. _lino.sales.Order.vat_exempt:

Field **Order.vat_exempt**
==========================





Type: BooleanField

   
.. index::
   single: field;item_vat
   
.. _lino.sales.Order.item_vat:

Field **Order.item_vat**
========================





Type: BooleanField

   
.. index::
   single: field;total_excl
   
.. _lino.sales.Order.total_excl:

Field **Order.total_excl**
==========================





Type: PriceField

   
.. index::
   single: field;total_vat
   
.. _lino.sales.Order.total_vat:

Field **Order.total_vat**
=========================





Type: PriceField

   
.. index::
   single: field;intro
   
.. _lino.sales.Order.intro:

Field **Order.intro**
=====================





Type: TextField

   
.. index::
   single: field;user
   
.. _lino.sales.Order.user:

Field **Order.user**
====================





Type: ForeignKey

   
.. index::
   single: field;salesdocument_ptr
   
.. _lino.sales.Order.salesdocument_ptr:

Field **Order.salesdocument_ptr**
=================================





Type: OneToOneField

   
.. index::
   single: field;cycle
   
.. _lino.sales.Order.cycle:

Field **Order.cycle**
=====================





Type: CharField

   
.. index::
   single: field;start_date
   
.. _lino.sales.Order.start_date:

Field **Order.start_date**
==========================



Beginning of payable period. 
      Set to blank if no bill should be generated

Type: MyDateField

   
.. index::
   single: field;covered_until
   
.. _lino.sales.Order.covered_until:

Field **Order.covered_until**
=============================





Type: MyDateField

   


.. index::
   pair: model; Invoice

.. _lino.sales.Invoice:

-----------------
Model **Invoice**
-----------------



Invoice(id, must_build, person_id, company_id, contact_id, language, journal_id, number, sent_time, creation_date, your_ref, imode_id, shipping_mode_id, payment_term_id, sales_remark, subject, vat_exempt, item_vat, total_excl, total_vat, intro, user_id, salesdocument_ptr_id, journal_id, number, value_date, ledger_remark, booked, due_date, order_id)
  
================= ============= ======================================================
name              type          verbose name                                          
================= ============= ======================================================
id                AutoField     ID                                                    
must_build        BooleanField  must build (muss generiert werden,doit être construit)
person            ForeignKey    Person (Personne,Isik)                                
company           ForeignKey    Company (Firma,Société,Firma)                         
contact           ForeignKey    represented by (Vertreten durch,représenté par)       
language          LanguageField Language (Sprache,Langue)                             
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
user              ForeignKey    user (Benutzer,utilisateur)                           
salesdocument_ptr OneToOneField salesdocument ptr                                     
journal           ForeignKey    journal                                               
number            IntegerField  number                                                
value_date        DateField     value date                                            
ledger_remark     CharField     Remark for ledger                                     
booked            BooleanField  booked                                                
due_date          MyDateField   Payable until                                         
order             ForeignKey    order                                                 
================= ============= ======================================================

    
Defined in :srcref:`/lino/modlib/sales/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.sales.Invoice.id:

Field **Invoice.id**
====================





Type: AutoField

   
.. index::
   single: field;must_build
   
.. _lino.sales.Invoice.must_build:

Field **Invoice.must_build**
============================





Type: BooleanField

   
.. index::
   single: field;person
   
.. _lino.sales.Invoice.person:

Field **Invoice.person**
========================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _lino.sales.Invoice.company:

Field **Invoice.company**
=========================





Type: ForeignKey

   
.. index::
   single: field;contact
   
.. _lino.sales.Invoice.contact:

Field **Invoice.contact**
=========================





Type: ForeignKey

   
.. index::
   single: field;language
   
.. _lino.sales.Invoice.language:

Field **Invoice.language**
==========================





Type: LanguageField

   
.. index::
   single: field;journal
   
.. _lino.sales.Invoice.journal:

Field **Invoice.journal**
=========================





Type: ForeignKey

   
.. index::
   single: field;number
   
.. _lino.sales.Invoice.number:

Field **Invoice.number**
========================





Type: IntegerField

   
.. index::
   single: field;sent_time
   
.. _lino.sales.Invoice.sent_time:

Field **Invoice.sent_time**
===========================





Type: DateTimeField

   
.. index::
   single: field;creation_date
   
.. _lino.sales.Invoice.creation_date:

Field **Invoice.creation_date**
===============================





Type: DateField

   
.. index::
   single: field;your_ref
   
.. _lino.sales.Invoice.your_ref:

Field **Invoice.your_ref**
==========================





Type: CharField

   
.. index::
   single: field;imode
   
.. _lino.sales.Invoice.imode:

Field **Invoice.imode**
=======================





Type: ForeignKey

   
.. index::
   single: field;shipping_mode
   
.. _lino.sales.Invoice.shipping_mode:

Field **Invoice.shipping_mode**
===============================





Type: ForeignKey

   
.. index::
   single: field;payment_term
   
.. _lino.sales.Invoice.payment_term:

Field **Invoice.payment_term**
==============================





Type: ForeignKey

   
.. index::
   single: field;sales_remark
   
.. _lino.sales.Invoice.sales_remark:

Field **Invoice.sales_remark**
==============================





Type: CharField

   
.. index::
   single: field;subject
   
.. _lino.sales.Invoice.subject:

Field **Invoice.subject**
=========================





Type: CharField

   
.. index::
   single: field;vat_exempt
   
.. _lino.sales.Invoice.vat_exempt:

Field **Invoice.vat_exempt**
============================





Type: BooleanField

   
.. index::
   single: field;item_vat
   
.. _lino.sales.Invoice.item_vat:

Field **Invoice.item_vat**
==========================





Type: BooleanField

   
.. index::
   single: field;total_excl
   
.. _lino.sales.Invoice.total_excl:

Field **Invoice.total_excl**
============================





Type: PriceField

   
.. index::
   single: field;total_vat
   
.. _lino.sales.Invoice.total_vat:

Field **Invoice.total_vat**
===========================





Type: PriceField

   
.. index::
   single: field;intro
   
.. _lino.sales.Invoice.intro:

Field **Invoice.intro**
=======================





Type: TextField

   
.. index::
   single: field;user
   
.. _lino.sales.Invoice.user:

Field **Invoice.user**
======================





Type: ForeignKey

   
.. index::
   single: field;salesdocument_ptr
   
.. _lino.sales.Invoice.salesdocument_ptr:

Field **Invoice.salesdocument_ptr**
===================================





Type: OneToOneField

   
.. index::
   single: field;journal
   
.. _lino.sales.Invoice.journal:

Field **Invoice.journal**
=========================





Type: ForeignKey

   
.. index::
   single: field;number
   
.. _lino.sales.Invoice.number:

Field **Invoice.number**
========================





Type: IntegerField

   
.. index::
   single: field;value_date
   
.. _lino.sales.Invoice.value_date:

Field **Invoice.value_date**
============================





Type: DateField

   
.. index::
   single: field;ledger_remark
   
.. _lino.sales.Invoice.ledger_remark:

Field **Invoice.ledger_remark**
===============================





Type: CharField

   
.. index::
   single: field;booked
   
.. _lino.sales.Invoice.booked:

Field **Invoice.booked**
========================





Type: BooleanField

   
.. index::
   single: field;due_date
   
.. _lino.sales.Invoice.due_date:

Field **Invoice.due_date**
==========================





Type: MyDateField

   
.. index::
   single: field;order
   
.. _lino.sales.Invoice.order:

Field **Invoice.order**
=======================





Type: ForeignKey

   


.. index::
   pair: model; DocItem

.. _lino.sales.DocItem:

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

Referenced from




.. index::
   single: field;id
   
.. _lino.sales.DocItem.id:

Field **DocItem.id**
====================





Type: AutoField

   
.. index::
   single: field;document
   
.. _lino.sales.DocItem.document:

Field **DocItem.document**
==========================





Type: ForeignKey

   
.. index::
   single: field;pos
   
.. _lino.sales.DocItem.pos:

Field **DocItem.pos**
=====================





Type: IntegerField

   
.. index::
   single: field;product
   
.. _lino.sales.DocItem.product:

Field **DocItem.product**
=========================





Type: ForeignKey

   
.. index::
   single: field;title
   
.. _lino.sales.DocItem.title:

Field **DocItem.title**
=======================





Type: CharField

   
.. index::
   single: field;description
   
.. _lino.sales.DocItem.description:

Field **DocItem.description**
=============================





Type: TextField

   
.. index::
   single: field;discount
   
.. _lino.sales.DocItem.discount:

Field **DocItem.discount**
==========================





Type: IntegerField

   
.. index::
   single: field;unit_price
   
.. _lino.sales.DocItem.unit_price:

Field **DocItem.unit_price**
============================





Type: PriceField

   
.. index::
   single: field;qty
   
.. _lino.sales.DocItem.qty:

Field **DocItem.qty**
=====================





Type: QuantityField

   
.. index::
   single: field;total
   
.. _lino.sales.DocItem.total:

Field **DocItem.total**
=======================





Type: PriceField

   


