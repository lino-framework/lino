======
thirds
======



.. currentmodule:: thirds

Defined in :srcref:`/lino/modlib/thirds/models.py`




.. contents:: Table of Contents



.. index::
   pair: model; Third

.. _std.thirds.Third:

---------------
Model **Third**
---------------



Third(id, seqno, owner_type_id, owner_id, person_id, company_id, remark)
  
========== ==================== =================================================
name       type                 verbose name                                     
========== ==================== =================================================
id         AutoField            ID                                               
seqno      IntegerField         Seq.No. (Seq.-Nr.,Sequence N°)                   
owner_type ForeignKey           Owner type (Besitzertabelle,type de propriétaire)
owner_id   PositiveIntegerField Owner (Besitzer,Propriétaire)                    
person     ForeignKey           Person (Personne)                                
company    ForeignKey           Company (Firma)                                  
remark     TextField            Remark (Bemerkung,Remarque)                      
========== ==================== =================================================

    
Defined in :srcref:`/lino/modlib/thirds/models.py`

.. index::
   single: field;id
   
.. _std.thirds.Third.id:

Field **Third.id**
==================





Type: AutoField

   
.. index::
   single: field;seqno
   
.. _std.thirds.Third.seqno:

Field **Third.seqno**
=====================





Type: IntegerField

   
.. index::
   single: field;owner_type
   
.. _std.thirds.Third.owner_type:

Field **Third.owner_type**
==========================





Type: ForeignKey

   
.. index::
   single: field;owner_id
   
.. _std.thirds.Third.owner_id:

Field **Third.owner_id**
========================





Type: PositiveIntegerField

   
.. index::
   single: field;person
   
.. _std.thirds.Third.person:

Field **Third.person**
======================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _std.thirds.Third.company:

Field **Third.company**
=======================





Type: ForeignKey

   
.. index::
   single: field;remark
   
.. _std.thirds.Third.remark:

Field **Third.remark**
======================





Type: TextField

   


