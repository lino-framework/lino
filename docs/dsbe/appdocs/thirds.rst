======
thirds
======



.. currentmodule:: thirds

Defined in :srcref:`/lino/modlib/thirds/models.py`

Deserves more documentation.


.. contents:: Table of Contents



.. index::
   pair: model; Third

.. _lino.thirds.Third:

---------------
Model **Third**
---------------



Third(id, seqno, owner_type_id, owner_id, person_id, company_id, remark)
  
========== ======================== =================================================
name       type                     verbose name                                     
========== ======================== =================================================
id         AutoField                ID                                               
seqno      IntegerField             Seq.No. (Seq.-Nr.,N° de séq)                     
owner_type ForeignKey               Owner type (Besitzertabelle,type de propriétaire)
owner_id   GenericForeignKeyIdField Owner (Besitzer,Propriétaire)                    
person     ForeignKey               Person (Personne)                                
company    ForeignKey               Company (Firma,Société)                          
remark     TextField                Remark (Bemerkung,Remarque)                      
========== ======================== =================================================

    
Defined in :srcref:`/lino/modlib/thirds/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.thirds.Third.id:

Field **Third.id**
==================





Type: AutoField

   
.. index::
   single: field;seqno
   
.. _lino.thirds.Third.seqno:

Field **Third.seqno**
=====================





Type: IntegerField

   
.. index::
   single: field;owner_type
   
.. _lino.thirds.Third.owner_type:

Field **Third.owner_type**
==========================





Type: ForeignKey

   
.. index::
   single: field;owner_id
   
.. _lino.thirds.Third.owner_id:

Field **Third.owner_id**
========================





Type: GenericForeignKeyIdField

   
.. index::
   single: field;person
   
.. _lino.thirds.Third.person:

Field **Third.person**
======================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _lino.thirds.Third.company:

Field **Third.company**
=======================





Type: ForeignKey

   
.. index::
   single: field;remark
   
.. _lino.thirds.Third.remark:

Field **Third.remark**
======================





Type: TextField

   


