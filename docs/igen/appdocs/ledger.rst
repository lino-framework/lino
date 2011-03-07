======
ledger
======



.. currentmodule:: ledger

Defined in :srcref:`/lino/modlib/ledger/models.py`




.. index::
   pair: model; Account
   single: field;id
   single: field;match
   single: field;name

.. _igen.ledger.Account:

-----------------
Model ``Account``
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
   pair: model; Booking
   single: field;id
   single: field;journal
   single: field;number
   single: field;pos
   single: field;date
   single: field;account
   single: field;person
   single: field;company
   single: field;debit
   single: field;credit

.. _igen.ledger.Booking:

-----------------
Model ``Booking``
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


