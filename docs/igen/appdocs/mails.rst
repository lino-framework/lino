=====
mails
=====



.. currentmodule:: mails

Defined in :srcref:`/lino/modlib/mails/models.py`


Defines models for :mod:`lino.modlib.mails`.


.. contents:: Table of Contents



.. index::
   pair: model; Recipient

.. _lino.mails.Recipient:

-------------------
Model **Recipient**
-------------------



Recipient(id, mail_id, contact_id, type, address, name)
  
======= =============== ================================
name    type            verbose name                    
======= =============== ================================
id      AutoField       ID                              
mail    ForeignKey      mail                            
contact ForeignKey      Contact (Kontakt)               
type    ChoiceListField Recipient Type (Empfängerart)   
address EmailField      Address (Adresse,Adresse,Adress)
name    CharField       Name (Nom,Nimi)                 
======= =============== ================================

    
Defined in :srcref:`/lino/modlib/mails/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.mails.Recipient.id:

Field **Recipient.id**
======================





Type: AutoField

   
.. index::
   single: field;mail
   
.. _lino.mails.Recipient.mail:

Field **Recipient.mail**
========================





Type: ForeignKey

   
.. index::
   single: field;contact
   
.. _lino.mails.Recipient.contact:

Field **Recipient.contact**
===========================





Type: ForeignKey

   
.. index::
   single: field;type
   
.. _lino.mails.Recipient.type:

Field **Recipient.type**
========================





Type: ChoiceListField

   
.. index::
   single: field;address
   
.. _lino.mails.Recipient.address:

Field **Recipient.address**
===========================





Type: EmailField

   
.. index::
   single: field;name
   
.. _lino.mails.Recipient.name:

Field **Recipient.name**
========================





Type: CharField

   


.. index::
   pair: model; Mail

.. _lino.mails.Mail:

--------------
Model **Mail**
--------------




Deserves more documentation.

  
======= ============= =======================
name    type          verbose name           
======= ============= =======================
id      AutoField     ID                     
subject CharField     Subject (Betreff,Objet)
body    RichTextField Body (Inhalt,Corps)    
======= ============= =======================

    
Defined in :srcref:`/lino/modlib/mails/models.py`

Referenced from
`lino.mails.Recipient.mail`_, `lino.mails.InMail.mail_ptr`_, `lino.mails.OutMail.mail_ptr`_



.. index::
   single: field;id
   
.. _lino.mails.Mail.id:

Field **Mail.id**
=================





Type: AutoField

   
.. index::
   single: field;subject
   
.. _lino.mails.Mail.subject:

Field **Mail.subject**
======================





Type: CharField

   
.. index::
   single: field;body
   
.. _lino.mails.Mail.body:

Field **Mail.body**
===================





Type: RichTextField

   


.. index::
   pair: model; InMail

.. _lino.mails.InMail:

----------------
Model **InMail**
----------------



Incoming Mail
  
=========== ==================== ==============================================================
name        type                 verbose name                                                  
=========== ==================== ==============================================================
id          AutoField            ID                                                            
subject     CharField            Subject (Betreff,Objet)                                       
body        RichTextField        Body (Inhalt,Corps)                                           
mail_ptr    OneToOneField        mail                                                          
sender_type ForeignKey           content type (Inhaltstyp,type de contenu,inhoudstype,sisutüüp)
sender_id   PositiveIntegerField sender id                                                     
received    DateTimeField        received                                                      
=========== ==================== ==============================================================

    
Defined in :srcref:`/lino/modlib/mails/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.mails.InMail.id:

Field **InMail.id**
===================





Type: AutoField

   
.. index::
   single: field;subject
   
.. _lino.mails.InMail.subject:

Field **InMail.subject**
========================





Type: CharField

   
.. index::
   single: field;body
   
.. _lino.mails.InMail.body:

Field **InMail.body**
=====================





Type: RichTextField

   
.. index::
   single: field;mail_ptr
   
.. _lino.mails.InMail.mail_ptr:

Field **InMail.mail_ptr**
=========================





Type: OneToOneField

   
.. index::
   single: field;sender_type
   
.. _lino.mails.InMail.sender_type:

Field **InMail.sender_type**
============================





Type: ForeignKey

   
.. index::
   single: field;sender_id
   
.. _lino.mails.InMail.sender_id:

Field **InMail.sender_id**
==========================





Type: PositiveIntegerField

   
.. index::
   single: field;received
   
.. _lino.mails.InMail.received:

Field **InMail.received**
=========================





Type: DateTimeField

   


.. index::
   pair: model; OutMail

.. _lino.mails.OutMail:

-----------------
Model **OutMail**
-----------------



Outgoing Mail
  
======== ============= =======================
name     type          verbose name           
======== ============= =======================
id       AutoField     ID                     
subject  CharField     Subject (Betreff,Objet)
body     RichTextField Body (Inhalt,Corps)    
mail_ptr OneToOneField mail                   
user     ForeignKey    User                   
sent     DateTimeField sent                   
======== ============= =======================

    
Defined in :srcref:`/lino/modlib/mails/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.mails.OutMail.id:

Field **OutMail.id**
====================





Type: AutoField

   
.. index::
   single: field;subject
   
.. _lino.mails.OutMail.subject:

Field **OutMail.subject**
=========================





Type: CharField

   
.. index::
   single: field;body
   
.. _lino.mails.OutMail.body:

Field **OutMail.body**
======================





Type: RichTextField

   
.. index::
   single: field;mail_ptr
   
.. _lino.mails.OutMail.mail_ptr:

Field **OutMail.mail_ptr**
==========================





Type: OneToOneField

   
.. index::
   single: field;user
   
.. _lino.mails.OutMail.user:

Field **OutMail.user**
======================





Type: ForeignKey

   
.. index::
   single: field;sent
   
.. _lino.mails.OutMail.sent:

Field **OutMail.sent**
======================





Type: DateTimeField

   


