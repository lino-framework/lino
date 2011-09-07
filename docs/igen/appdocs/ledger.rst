======
ledger
======



.. currentmodule:: ledger

Defined in :srcref:`/lino/modlib/ledger/models.py`



.. contents:: Table of Contents



.. index::
   pair: model; Account

.. _lino.ledger.Account:

-----------------
Model **Account**
-----------------



Account(id, match, name)
  
===== ========= ============
name  type      verbose name
===== ========= ============
id    AutoField ID          
match CharField match       
name  CharField name        
===== ========= ============

    
Defined in :srcref:`/lino/modlib/ledger/models.py`

Referenced from
`lino.ledger.Booking.account`_, `lino.lino.SiteConfig.sales_base_account`_, `lino.lino.SiteConfig.sales_vat_account`_, `lino.journals.Journal.account`_, `lino.finan.DocItem.account`_



.. index::
   single: field;id
   
.. _lino.ledger.Account.id:

Field **Account.id**
====================





Type: AutoField

   
.. index::
   single: field;match
   
.. _lino.ledger.Account.match:

Field **Account.match**
=======================





Type: CharField

   
.. index::
   single: field;name
   
.. _lino.ledger.Account.name:

Field **Account.name**
======================





Type: CharField

   


.. index::
   pair: model; Booking

.. _lino.ledger.Booking:

-----------------
Model **Booking**
-----------------



Booking(id, journal_id, number, pos, date, account_id, contact_id, debit, credit)
  
======= ============ =================
name    type         verbose name     
======= ============ =================
id      AutoField    ID               
journal ForeignKey   journal          
number  IntegerField number           
pos     IntegerField Position         
date    DateField    date             
account ForeignKey   account          
contact ForeignKey   Contact (Kontakt)
debit   PriceField   debit            
credit  PriceField   credit           
======= ============ =================

    
Defined in :srcref:`/lino/modlib/ledger/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.ledger.Booking.id:

Field **Booking.id**
====================





Type: AutoField

   
.. index::
   single: field;journal
   
.. _lino.ledger.Booking.journal:

Field **Booking.journal**
=========================





Type: ForeignKey

   
.. index::
   single: field;number
   
.. _lino.ledger.Booking.number:

Field **Booking.number**
========================





Type: IntegerField

   
.. index::
   single: field;pos
   
.. _lino.ledger.Booking.pos:

Field **Booking.pos**
=====================





Type: IntegerField

   
.. index::
   single: field;date
   
.. _lino.ledger.Booking.date:

Field **Booking.date**
======================





Type: DateField

   
.. index::
   single: field;account
   
.. _lino.ledger.Booking.account:

Field **Booking.account**
=========================





Type: ForeignKey

   
.. index::
   single: field;contact
   
.. _lino.ledger.Booking.contact:

Field **Booking.contact**
=========================





Type: ForeignKey

   
.. index::
   single: field;debit
   
.. _lino.ledger.Booking.debit:

Field **Booking.debit**
=======================





Type: PriceField

   
.. index::
   single: field;credit
   
.. _lino.ledger.Booking.credit:

Field **Booking.credit**
========================





Type: PriceField

   


