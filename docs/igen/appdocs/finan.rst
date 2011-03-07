=====
finan
=====



.. currentmodule:: finan

Defined in :srcref:`/lino/modlib/finan/models.py`




.. index::
   pair: model; BankStatement
   single: field;id
   single: field;journal
   single: field;number
   single: field;value_date
   single: field;ledger_remark
   single: field;booked
   single: field;date
   single: field;balance1
   single: field;balance2

.. _igen.finan.BankStatement:

-----------------------
Model ``BankStatement``
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
   pair: model; DocItem
   single: field;id
   single: field;document
   single: field;pos
   single: field;date
   single: field;debit
   single: field;credit
   single: field;remark
   single: field;account
   single: field;person
   single: field;company

.. _igen.finan.DocItem:

-----------------
Model ``DocItem``
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


