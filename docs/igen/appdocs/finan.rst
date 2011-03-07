=====
finan
=====



.. currentmodule:: finan

Defined in :srcref:`/lino/modlib/finan/models.py`



.. contents:: Table of Contents



.. index::
   pair: model; BankStatement

.. _igen.finan.BankStatement:

-----------------------
Model **BankStatement**
-----------------------



BankStatement(id, journal_id, number, value_date, ledger_remark, booked, date, balance1, balance2)
  
============= ============ =================
name          type         verbose name     
============= ============ =================
id            AutoField    ID               
journal       ForeignKey   journal          
number        IntegerField number           
value_date    DateField    value date       
ledger_remark CharField    Remark for ledger
booked        BooleanField booked           
date          MyDateField  date             
balance1      PriceField   balance1         
balance2      PriceField   balance2         
============= ============ =================

    
Defined in :srcref:`/lino/modlib/finan/models.py`

.. index::
   single: field;id
   
.. _igen.finan.BankStatement.id:

Field **BankStatement.id**
==========================





Type: AutoField

   
.. index::
   single: field;journal
   
.. _igen.finan.BankStatement.journal:

Field **BankStatement.journal**
===============================





Type: ForeignKey

   
.. index::
   single: field;number
   
.. _igen.finan.BankStatement.number:

Field **BankStatement.number**
==============================





Type: IntegerField

   
.. index::
   single: field;value_date
   
.. _igen.finan.BankStatement.value_date:

Field **BankStatement.value_date**
==================================





Type: DateField

   
.. index::
   single: field;ledger_remark
   
.. _igen.finan.BankStatement.ledger_remark:

Field **BankStatement.ledger_remark**
=====================================





Type: CharField

   
.. index::
   single: field;booked
   
.. _igen.finan.BankStatement.booked:

Field **BankStatement.booked**
==============================





Type: BooleanField

   
.. index::
   single: field;date
   
.. _igen.finan.BankStatement.date:

Field **BankStatement.date**
============================





Type: MyDateField

   
.. index::
   single: field;balance1
   
.. _igen.finan.BankStatement.balance1:

Field **BankStatement.balance1**
================================





Type: PriceField

   
.. index::
   single: field;balance2
   
.. _igen.finan.BankStatement.balance2:

Field **BankStatement.balance2**
================================





Type: PriceField

   


.. index::
   pair: model; DocItem

.. _igen.finan.DocItem:

-----------------
Model **DocItem**
-----------------



DocItem(id, document_id, pos, date, debit, credit, remark, account_id, person_id, company_id)
  
======== ============ =====================
name     type         verbose name         
======== ============ =====================
id       AutoField    ID                   
document ForeignKey   document             
pos      IntegerField Position             
date     MyDateField  date                 
debit    PriceField   debit                
credit   PriceField   credit               
remark   CharField    remark               
account  ForeignKey   account              
person   ForeignKey   person (Person,isik) 
company  ForeignKey   company (Firma,firma)
======== ============ =====================

    
Defined in :srcref:`/lino/modlib/finan/models.py`

.. index::
   single: field;id
   
.. _igen.finan.DocItem.id:

Field **DocItem.id**
====================





Type: AutoField

   
.. index::
   single: field;document
   
.. _igen.finan.DocItem.document:

Field **DocItem.document**
==========================





Type: ForeignKey

   
.. index::
   single: field;pos
   
.. _igen.finan.DocItem.pos:

Field **DocItem.pos**
=====================





Type: IntegerField

   
.. index::
   single: field;date
   
.. _igen.finan.DocItem.date:

Field **DocItem.date**
======================





Type: MyDateField

   
.. index::
   single: field;debit
   
.. _igen.finan.DocItem.debit:

Field **DocItem.debit**
=======================





Type: PriceField

   
.. index::
   single: field;credit
   
.. _igen.finan.DocItem.credit:

Field **DocItem.credit**
========================





Type: PriceField

   
.. index::
   single: field;remark
   
.. _igen.finan.DocItem.remark:

Field **DocItem.remark**
========================





Type: CharField

   
.. index::
   single: field;account
   
.. _igen.finan.DocItem.account:

Field **DocItem.account**
=========================





Type: ForeignKey

   
.. index::
   single: field;person
   
.. _igen.finan.DocItem.person:

Field **DocItem.person**
========================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _igen.finan.DocItem.company:

Field **DocItem.company**
=========================





Type: ForeignKey

   


