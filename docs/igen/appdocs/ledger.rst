======
ledger
======



.. currentmodule:: ledger

Defined in :srcref:`/lino/modlib/ledger/models.py`



.. contents:: Table of Contents



.. index::
   pair: model; Account

.. _igen.ledger.Account:

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
   
.. _igen.ledger.Account.id:

Field **Account.id**
====================





Type: AutoField

   
.. index::
   single: field;match
   
.. _igen.ledger.Account.match:

Field **Account.match**
=======================





Type: CharField

   
.. index::
   single: field;name
   
.. _igen.ledger.Account.name:

Field **Account.name**
======================





Type: CharField

   


.. index::
   pair: model; Booking

.. _igen.ledger.Booking:

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
   
.. _igen.ledger.Booking.id:

Field **Booking.id**
====================





Type: AutoField

   
.. index::
   single: field;journal
   
.. _igen.ledger.Booking.journal:

Field **Booking.journal**
=========================





Type: ForeignKey

   
.. index::
   single: field;number
   
.. _igen.ledger.Booking.number:

Field **Booking.number**
========================





Type: IntegerField

   
.. index::
   single: field;pos
   
.. _igen.ledger.Booking.pos:

Field **Booking.pos**
=====================





Type: IntegerField

   
.. index::
   single: field;date
   
.. _igen.ledger.Booking.date:

Field **Booking.date**
======================





Type: DateField

   
.. index::
   single: field;account
   
.. _igen.ledger.Booking.account:

Field **Booking.account**
=========================





Type: ForeignKey

   
.. index::
   single: field;person
   
.. _igen.ledger.Booking.person:

Field **Booking.person**
========================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _igen.ledger.Booking.company:

Field **Booking.company**
=========================





Type: ForeignKey

   
.. index::
   single: field;debit
   
.. _igen.ledger.Booking.debit:

Field **Booking.debit**
=======================





Type: PriceField

   
.. index::
   single: field;credit
   
.. _igen.ledger.Booking.credit:

Field **Booking.credit**
========================





Type: PriceField

   


