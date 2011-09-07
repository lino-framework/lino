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
    
  
======= ============== ==========================
name    type           verbose name              
======= ============== ==========================
name    BabelCharField Designation (Beschreibung)
id      CharField      id                        
days    IntegerField   days                      
months  IntegerField   months                    
name_de CharField      Designation (de)          
name_fr CharField      Designation (fr)          
name_nl CharField      Designation (nl)          
name_et CharField      Designation (et)          
======= ============== ==========================

    
Defined in :srcref:`/lino/modlib/sales/models.py`

Referenced from
`lino.sales.SalesRule.payment_term`_, `lino.sales.Customer.payment_term`_, `lino.sales.Order.payment_term`_, `lino.sales.Invoice.payment_term`_



.. index::
   single: field;name
   
.. _lino.sales.PaymentTerm.name:

Field **PaymentTerm.name**
==========================





Type: BabelCharField

   
.. index::
   single: field;id
   
.. _lino.sales.PaymentTerm.id:

Field **PaymentTerm.id**
========================





Type: CharField

   
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
name         BabelCharField  Designation (Beschreibung)                                 
build_method CharField       Build method (Konstruktionsmethode,Méthode de construction)
template     CharField       Template (Vorlage,Modèle)                                  
id           CharField       id                                                         
journal      ForeignKey      journal                                                    
price        PriceField      price                                                      
channel      ChoiceListField Channel                                                    
advance_days IntegerField    advance days                                               
name_de      CharField       Designation (de)                                           
name_fr      CharField       Designation (fr)                                           
name_nl      CharField       Designation (nl)                                           
name_et      CharField       Designation (et)                                           
============ =============== ===========================================================

    
Defined in :srcref:`/lino/modlib/sales/models.py`

Referenced from
`lino.sales.SalesRule.imode`_, `lino.sales.Order.imode`_, `lino.sales.Invoice.imode`_



.. index::
   single: field;name
   
.. _lino.sales.InvoicingMode.name:

Field **InvoicingMode.name**
============================





Type: BabelCharField

   
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



ShippingMode(name, id, price, name_de, name_fr, name_nl, name_et)
  
======= ============== ==========================
name    type           verbose name              
======= ============== ==========================
name    BabelCharField Designation (Beschreibung)
id      CharField      id                        
price   PriceField     price                     
name_de CharField      Designation (de)          
name_fr CharField      Designation (fr)          
name_nl CharField      Designation (nl)          
name_et CharField      Designation (et)          
======= ============== ==========================

    
Defined in :srcref:`/lino/modlib/sales/models.py`

Referenced from
`lino.sales.SalesRule.shipping_mode`_, `lino.sales.Order.shipping_mode`_, `lino.sales.Invoice.shipping_mode`_



.. index::
   single: field;name
   
.. _lino.sales.ShippingMode.name:

Field **ShippingMode.name**
===========================





Type: BabelCharField

   
.. index::
   single: field;id
   
.. _lino.sales.ShippingMode.id:

Field **ShippingMode.id**
=========================





Type: CharField

   
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
    
  
============= ========== ==============
name          type       verbose name  
============= ========== ==============
id            AutoField  ID            
journal       ForeignKey journal       
imode         ForeignKey Invoicing Mode
shipping_mode ForeignKey shipping mode 
payment_term  ForeignKey Payment Term  
============= ========== ==============

    
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
   pair: model; Customer

.. _lino.sales.Customer:

------------------
Model **Customer**
------------------




A Customer is a Contact that can receive sales invoices.

  
============= ============= ==========================================================================================================
name          type          verbose name                                                                                              
============= ============= ==========================================================================================================
id            AutoField     ID                                                                                                        
country       ForeignKey    Country (Land)                                                                                            
city          ForeignKey    City (Stadt)                                                                                              
name          CharField     Name (Nom,Nimi)                                                                                           
addr1         CharField     Address line before street (Adresszeile vor Straße,Ligne avant le nom de rue,Addressi lisatext enne tänav)
street_prefix CharField     Street prefix (Präfix Straße,Préfixe rue)                                                                 
street        CharField     Street (Straße,Rue,Tänav)                                                                                 
street_no     CharField     No. (Nr.,N°,Nr.)                                                                                          
street_box    CharField     Box (boîte,PK/krt)                                                                                        
addr2         CharField     Address line after street (Adresszeile nach Straße,Ligne après le nom de rue,Aadressilisa pärast tänav)   
zip_code      CharField     Zip code (Postleitzahl,Code postal,Sihtnumber)                                                            
region        CharField     Region (Région,Maakond)                                                                                   
language      LanguageField Language (Sprache,Langue)                                                                                 
email         EmailField    E-Mail (E-mail)                                                                                           
url           URLField      URL                                                                                                       
phone         CharField     Phone (Telefon,Téléphone,Telefon)                                                                         
gsm           CharField     GSM                                                                                                       
fax           CharField     Fax                                                                                                       
remarks       TextField     Remarks (Bemerkungen,Remarques,Märkused)                                                                  
contact_ptr   OneToOneField Contact (Kontakt)                                                                                         
payment_term  ForeignKey    Payment Term                                                                                              
vat_exempt    BooleanField  vat exempt                                                                                                
item_vat      BooleanField  item vat                                                                                                  
============= ============= ==========================================================================================================

    
Defined in :srcref:`/lino/modlib/sales/models.py`

Referenced from
`lino.sales.Order.customer`_, `lino.sales.Invoice.customer`_



.. index::
   single: field;id
   
.. _lino.sales.Customer.id:

Field **Customer.id**
=====================





Type: AutoField

   
.. index::
   single: field;country
   
.. _lino.sales.Customer.country:

Field **Customer.country**
==========================





Type: ForeignKey

   
.. index::
   single: field;city
   
.. _lino.sales.Customer.city:

Field **Customer.city**
=======================





Type: ForeignKey

   
.. index::
   single: field;name
   
.. _lino.sales.Customer.name:

Field **Customer.name**
=======================





Type: CharField

   
.. index::
   single: field;addr1
   
.. _lino.sales.Customer.addr1:

Field **Customer.addr1**
========================



Address line before street

Type: CharField

   
.. index::
   single: field;street_prefix
   
.. _lino.sales.Customer.street_prefix:

Field **Customer.street_prefix**
================================



Text to print before name of street, but to ignore for sorting.

Type: CharField

   
.. index::
   single: field;street
   
.. _lino.sales.Customer.street:

Field **Customer.street**
=========================



Name of street. Without house number.

Type: CharField

   
.. index::
   single: field;street_no
   
.. _lino.sales.Customer.street_no:

Field **Customer.street_no**
============================



House number

Type: CharField

   
.. index::
   single: field;street_box
   
.. _lino.sales.Customer.street_box:

Field **Customer.street_box**
=============================



Text to print after :attr:`steet_no` on the same line

Type: CharField

   
.. index::
   single: field;addr2
   
.. _lino.sales.Customer.addr2:

Field **Customer.addr2**
========================



Address line to print below street line

Type: CharField

   
.. index::
   single: field;zip_code
   
.. _lino.sales.Customer.zip_code:

Field **Customer.zip_code**
===========================





Type: CharField

   
.. index::
   single: field;region
   
.. _lino.sales.Customer.region:

Field **Customer.region**
=========================





Type: CharField

   
.. index::
   single: field;language
   
.. _lino.sales.Customer.language:

Field **Customer.language**
===========================





Type: LanguageField

   
.. index::
   single: field;email
   
.. _lino.sales.Customer.email:

Field **Customer.email**
========================





Type: EmailField

   
.. index::
   single: field;url
   
.. _lino.sales.Customer.url:

Field **Customer.url**
======================





Type: URLField

   
.. index::
   single: field;phone
   
.. _lino.sales.Customer.phone:

Field **Customer.phone**
========================





Type: CharField

   
.. index::
   single: field;gsm
   
.. _lino.sales.Customer.gsm:

Field **Customer.gsm**
======================





Type: CharField

   
.. index::
   single: field;fax
   
.. _lino.sales.Customer.fax:

Field **Customer.fax**
======================





Type: CharField

   
.. index::
   single: field;remarks
   
.. _lino.sales.Customer.remarks:

Field **Customer.remarks**
==========================





Type: TextField

   
.. index::
   single: field;contact_ptr
   
.. _lino.sales.Customer.contact_ptr:

Field **Customer.contact_ptr**
==============================





Type: OneToOneField

   
.. index::
   single: field;payment_term
   
.. _lino.sales.Customer.payment_term:

Field **Customer.payment_term**
===============================





Type: ForeignKey

   
.. index::
   single: field;vat_exempt
   
.. _lino.sales.Customer.vat_exempt:

Field **Customer.vat_exempt**
=============================





Type: BooleanField

   
.. index::
   single: field;item_vat
   
.. _lino.sales.Customer.item_vat:

Field **Customer.item_vat**
===========================





Type: BooleanField

   


.. index::
   pair: model; Order

.. _lino.sales.Order:

---------------
Model **Order**
---------------




An Order is when a :class:`Customer` asks us to "deliver" a 
given set of "products".

  
============= ============= ======================================================
name          type          verbose name                                          
============= ============= ======================================================
id            AutoField     ID                                                    
user          ForeignKey    User                                                  
must_build    BooleanField  must build (muss generiert werden,doit être construit)
journal       ForeignKey    journal                                               
number        IntegerField  number                                                
sent_time     DateTimeField sent time                                             
customer      ForeignKey    Customer                                              
language      LanguageField Language (Sprache,Langue)                             
creation_date DateField     creation date                                         
your_ref      CharField     your ref                                              
imode         ForeignKey    Invoicing Mode                                        
shipping_mode ForeignKey    shipping mode                                         
payment_term  ForeignKey    Payment Term                                          
sales_remark  CharField     Remark for sales                                      
subject       CharField     Subject line                                          
vat_exempt    BooleanField  vat exempt                                            
item_vat      BooleanField  item vat                                              
total_excl    PriceField    total excl                                            
total_vat     PriceField    total vat                                             
intro         TextField     Introductive Text                                     
cycle         CharField     cycle                                                 
start_date    MyDateField   start date                                            
covered_until MyDateField   covered until                                         
============= ============= ======================================================

    
Defined in :srcref:`/lino/modlib/sales/models.py`

Referenced from
`lino.sales.Invoice.order`_, `lino.sales.OrderItem.document`_



.. index::
   single: field;id
   
.. _lino.sales.Order.id:

Field **Order.id**
==================





Type: AutoField

   
.. index::
   single: field;user
   
.. _lino.sales.Order.user:

Field **Order.user**
====================





Type: ForeignKey

   
.. index::
   single: field;must_build
   
.. _lino.sales.Order.must_build:

Field **Order.must_build**
==========================





Type: BooleanField

   
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
   single: field;customer
   
.. _lino.sales.Order.customer:

Field **Order.customer**
========================





Type: ForeignKey

   
.. index::
   single: field;language
   
.. _lino.sales.Order.language:

Field **Order.language**
========================





Type: LanguageField

   
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



Invoice(id, user_id, must_build, journal_id, number, sent_time, value_date, ledger_remark, booked, customer_id, language, creation_date, your_ref, imode_id, shipping_mode_id, payment_term_id, sales_remark, subject, vat_exempt, item_vat, total_excl, total_vat, intro, due_date, order_id)
  
============= ============= ======================================================
name          type          verbose name                                          
============= ============= ======================================================
id            AutoField     ID                                                    
user          ForeignKey    User                                                  
must_build    BooleanField  must build (muss generiert werden,doit être construit)
journal       ForeignKey    journal                                               
number        IntegerField  number                                                
sent_time     DateTimeField sent time                                             
value_date    DateField     value date                                            
ledger_remark CharField     Remark for ledger                                     
booked        BooleanField  booked                                                
customer      ForeignKey    Customer                                              
language      LanguageField Language (Sprache,Langue)                             
creation_date DateField     creation date                                         
your_ref      CharField     your ref                                              
imode         ForeignKey    Invoicing Mode                                        
shipping_mode ForeignKey    shipping mode                                         
payment_term  ForeignKey    Payment Term                                          
sales_remark  CharField     Remark for sales                                      
subject       CharField     Subject line                                          
vat_exempt    BooleanField  vat exempt                                            
item_vat      BooleanField  item vat                                              
total_excl    PriceField    total excl                                            
total_vat     PriceField    total vat                                             
intro         TextField     Introductive Text                                     
due_date      DateField     Payable until                                         
order         ForeignKey    order                                                 
============= ============= ======================================================

    
Defined in :srcref:`/lino/modlib/sales/models.py`

Referenced from
`lino.sales.InvoiceItem.document`_



.. index::
   single: field;id
   
.. _lino.sales.Invoice.id:

Field **Invoice.id**
====================





Type: AutoField

   
.. index::
   single: field;user
   
.. _lino.sales.Invoice.user:

Field **Invoice.user**
======================





Type: ForeignKey

   
.. index::
   single: field;must_build
   
.. _lino.sales.Invoice.must_build:

Field **Invoice.must_build**
============================





Type: BooleanField

   
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
   single: field;customer
   
.. _lino.sales.Invoice.customer:

Field **Invoice.customer**
==========================





Type: ForeignKey

   
.. index::
   single: field;language
   
.. _lino.sales.Invoice.language:

Field **Invoice.language**
==========================





Type: LanguageField

   
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
   single: field;due_date
   
.. _lino.sales.Invoice.due_date:

Field **Invoice.due_date**
==========================





Type: DateField

   
.. index::
   single: field;order
   
.. _lino.sales.Invoice.order:

Field **Invoice.order**
=======================





Type: ForeignKey

   


.. index::
   pair: model; OrderItem

.. _lino.sales.OrderItem:

-------------------
Model **OrderItem**
-------------------



OrderItem(id, pos, product_id, title, description, discount, unit_price, qty, total, document_id)
  
=========== ============= ==========================
name        type          verbose name              
=========== ============= ==========================
id          AutoField     ID                        
pos         IntegerField  Position                  
product     ForeignKey    Product (Toode)           
title       CharField     title                     
description RichTextField Description (Beschreibung)
discount    IntegerField  Discount %                
unit_price  PriceField    unit price                
qty         QuantityField qty                       
total       PriceField    total                     
document    ForeignKey    order                     
=========== ============= ==========================

    
Defined in :srcref:`/lino/modlib/sales/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.sales.OrderItem.id:

Field **OrderItem.id**
======================





Type: AutoField

   
.. index::
   single: field;pos
   
.. _lino.sales.OrderItem.pos:

Field **OrderItem.pos**
=======================





Type: IntegerField

   
.. index::
   single: field;product
   
.. _lino.sales.OrderItem.product:

Field **OrderItem.product**
===========================





Type: ForeignKey

   
.. index::
   single: field;title
   
.. _lino.sales.OrderItem.title:

Field **OrderItem.title**
=========================





Type: CharField

   
.. index::
   single: field;description
   
.. _lino.sales.OrderItem.description:

Field **OrderItem.description**
===============================





Type: RichTextField

   
.. index::
   single: field;discount
   
.. _lino.sales.OrderItem.discount:

Field **OrderItem.discount**
============================





Type: IntegerField

   
.. index::
   single: field;unit_price
   
.. _lino.sales.OrderItem.unit_price:

Field **OrderItem.unit_price**
==============================





Type: PriceField

   
.. index::
   single: field;qty
   
.. _lino.sales.OrderItem.qty:

Field **OrderItem.qty**
=======================





Type: QuantityField

   
.. index::
   single: field;total
   
.. _lino.sales.OrderItem.total:

Field **OrderItem.total**
=========================





Type: PriceField

   
.. index::
   single: field;document
   
.. _lino.sales.OrderItem.document:

Field **OrderItem.document**
============================





Type: ForeignKey

   


.. index::
   pair: model; InvoiceItem

.. _lino.sales.InvoiceItem:

---------------------
Model **InvoiceItem**
---------------------



InvoiceItem(id, pos, product_id, title, description, discount, unit_price, qty, total, document_id)
  
=========== ============= ==========================
name        type          verbose name              
=========== ============= ==========================
id          AutoField     ID                        
pos         IntegerField  Position                  
product     ForeignKey    Product (Toode)           
title       CharField     title                     
description RichTextField Description (Beschreibung)
discount    IntegerField  Discount %                
unit_price  PriceField    unit price                
qty         QuantityField qty                       
total       PriceField    total                     
document    ForeignKey    invoice                   
=========== ============= ==========================

    
Defined in :srcref:`/lino/modlib/sales/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.sales.InvoiceItem.id:

Field **InvoiceItem.id**
========================





Type: AutoField

   
.. index::
   single: field;pos
   
.. _lino.sales.InvoiceItem.pos:

Field **InvoiceItem.pos**
=========================





Type: IntegerField

   
.. index::
   single: field;product
   
.. _lino.sales.InvoiceItem.product:

Field **InvoiceItem.product**
=============================





Type: ForeignKey

   
.. index::
   single: field;title
   
.. _lino.sales.InvoiceItem.title:

Field **InvoiceItem.title**
===========================





Type: CharField

   
.. index::
   single: field;description
   
.. _lino.sales.InvoiceItem.description:

Field **InvoiceItem.description**
=================================





Type: RichTextField

   
.. index::
   single: field;discount
   
.. _lino.sales.InvoiceItem.discount:

Field **InvoiceItem.discount**
==============================





Type: IntegerField

   
.. index::
   single: field;unit_price
   
.. _lino.sales.InvoiceItem.unit_price:

Field **InvoiceItem.unit_price**
================================





Type: PriceField

   
.. index::
   single: field;qty
   
.. _lino.sales.InvoiceItem.qty:

Field **InvoiceItem.qty**
=========================





Type: QuantityField

   
.. index::
   single: field;total
   
.. _lino.sales.InvoiceItem.total:

Field **InvoiceItem.total**
===========================





Type: PriceField

   
.. index::
   single: field;document
   
.. _lino.sales.InvoiceItem.document:

Field **InvoiceItem.document**
==============================





Type: ForeignKey

   


