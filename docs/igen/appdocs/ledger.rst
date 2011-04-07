======
ledger
======



.. currentmodule:: ledger

Defined in :srcref:`/lino/modlib/ledger/models.py`



.. contents:: Table of Contents



.. index::
   pair: model; Account

.. _std.ledger.Account:

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

.. index::
   single: field;id
   
.. _std.ledger.Account.id:

Field **Account.id**
====================





Type: AutoField

   
.. index::
   single: field;match
   
.. _std.ledger.Account.match:

Field **Account.match**
=======================





Type: CharField

   
.. index::
   single: field;name
   
.. _std.ledger.Account.name:

Field **Account.name**
======================





Type: CharField

   


.. index::
   pair: model; Booking

.. _std.ledger.Booking:

-----------------
Model **Booking**
-----------------



Booking(id, journal_id, number, pos, date, account_id, person_id, company_id, debit, credit)
  
======= ============ =====================
name    type         verbose name         
======= ============ =====================
id      AutoField    ID                   
journal ForeignKey   journal              
number  IntegerField number               
pos     IntegerField Position             
date    DateField    date                 
account ForeignKey   account              
person  ForeignKey   person (Person,isik) 
company ForeignKey   company (Firma,firma)
debit   PriceField   debit                
credit  PriceField   credit               
======= ============ =====================

    
Defined in :srcref:`/lino/modlib/ledger/models.py`

.. index::
   single: field;id
   
.. _std.ledger.Booking.id:

Field **Booking.id**
====================





Type: AutoField

   
.. index::
   single: field;journal
   
.. _std.ledger.Booking.journal:

Field **Booking.journal**
=========================





Type: ForeignKey

   
.. index::
   single: field;number
   
.. _std.ledger.Booking.number:

Field **Booking.number**
========================





Type: IntegerField

   
.. index::
   single: field;pos
   
.. _std.ledger.Booking.pos:

Field **Booking.pos**
=====================





Type: IntegerField

   
.. index::
   single: field;date
   
.. _std.ledger.Booking.date:

Field **Booking.date**
======================





Type: DateField

   
.. index::
   single: field;account
   
.. _std.ledger.Booking.account:

Field **Booking.account**
=========================





Type: ForeignKey

   
.. index::
   single: field;person
   
.. _std.ledger.Booking.person:

Field **Booking.person**
========================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _std.ledger.Booking.company:

Field **Booking.company**
=========================





Type: ForeignKey

   
.. index::
   single: field;debit
   
.. _std.ledger.Booking.debit:

Field **Booking.debit**
=======================





Type: PriceField

   
.. index::
   single: field;credit
   
.. _std.ledger.Booking.credit:

Field **Booking.credit**
========================





Type: PriceField

   


