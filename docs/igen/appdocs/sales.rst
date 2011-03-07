=====
sales
=====



.. currentmodule:: sales

Defined in :srcref:`/lino/modlib/sales/models.py`






.. index::
   pair: model; PaymentTerm
   single: field;id
   single: field;name
   single: field;days
   single: field;months
   single: field;name_de
   single: field;name_fr
   single: field;name_nl
   single: field;name_et

.. _igen.sales.PaymentTerm:

---------------------
Model ``PaymentTerm``
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
   pair: model; InvoicingMode
   single: field;build_method
   single: field;template
   single: field;id
   single: field;journal
   single: field;name
   single: field;price
   single: field;channel
   single: field;advance_days
   single: field;name_de
   single: field;name_fr
   single: field;name_nl
   single: field;name_et

.. _igen.sales.InvoicingMode:

-----------------------
Model ``InvoicingMode``
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
   pair: model; ShippingMode
   single: field;id
   single: field;name
   single: field;price
   single: field;name_de
   single: field;name_fr
   single: field;name_nl
   single: field;name_et

.. _igen.sales.ShippingMode:

----------------------
Model ``ShippingMode``
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
   pair: model; SalesRule
   single: field;id
   single: field;journal
   single: field;imode
   single: field;shipping_mode
   single: field;payment_term

.. _igen.sales.SalesRule:

-------------------
Model ``SalesRule``
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
   pair: model; SalesDocument
   single: field;id
   single: field;must_build
   single: field;person
   single: field;company
   single: field;contact
   single: field;language
   single: field;journal
   single: field;number
   single: field;sent_time
   single: field;creation_date
   single: field;your_ref
   single: field;imode
   single: field;shipping_mode
   single: field;payment_term
   single: field;sales_remark
   single: field;subject
   single: field;vat_exempt
   single: field;item_vat
   single: field;total_excl
   single: field;total_vat
   single: field;intro
   single: field;user

.. _igen.sales.SalesDocument:

-----------------------
Model ``SalesDocument``
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
   pair: model; Order
   single: field;id
   single: field;must_build
   single: field;person
   single: field;company
   single: field;contact
   single: field;language
   single: field;journal
   single: field;number
   single: field;sent_time
   single: field;creation_date
   single: field;your_ref
   single: field;imode
   single: field;shipping_mode
   single: field;payment_term
   single: field;sales_remark
   single: field;subject
   single: field;vat_exempt
   single: field;item_vat
   single: field;total_excl
   single: field;total_vat
   single: field;intro
   single: field;user
   single: field;salesdocument_ptr
   single: field;cycle
   single: field;start_date
   single: field;covered_until

.. _igen.sales.Order:

---------------
Model ``Order``
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
   pair: model; Invoice
   single: field;id
   single: field;must_build
   single: field;person
   single: field;company
   single: field;contact
   single: field;language
   single: field;journal
   single: field;number
   single: field;sent_time
   single: field;creation_date
   single: field;your_ref
   single: field;imode
   single: field;shipping_mode
   single: field;payment_term
   single: field;sales_remark
   single: field;subject
   single: field;vat_exempt
   single: field;item_vat
   single: field;total_excl
   single: field;total_vat
   single: field;intro
   single: field;user
   single: field;salesdocument_ptr
   single: field;journal
   single: field;number
   single: field;value_date
   single: field;ledger_remark
   single: field;booked
   single: field;due_date
   single: field;order

.. _igen.sales.Invoice:

-----------------
Model ``Invoice``
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
   pair: model; DocItem
   single: field;id
   single: field;document
   single: field;pos
   single: field;product
   single: field;title
   single: field;description
   single: field;discount
   single: field;unit_price
   single: field;qty
   single: field;total

.. _igen.sales.DocItem:

-----------------
Model ``DocItem``
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


