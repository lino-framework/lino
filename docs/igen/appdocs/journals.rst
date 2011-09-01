========
journals
========



.. currentmodule:: journals

Defined in :srcref:`/lino/modlib/journals/models.py`


This module defines the models Journal and AbstractDocument.

A journal is a sequence of numbered documents.
A Journal instance knows the model used for documents in this journal.
An AbstractDocument instance can look at its journal to find out which subclass it is.

See lino.testapps.journals for more documentation.



.. contents:: Table of Contents



.. index::
   pair: model; Journal

.. _lino.journals.Journal:

-----------------
Model **Journal**
-----------------



Journal(id, name, doctype, force_sequence, account_id, pos, printed_name, printed_name_de, printed_name_fr, printed_name_nl, printed_name_et)
  
=============== ============== =================
name            type           verbose name     
=============== ============== =================
id              CharField      id               
name            CharField      name             
doctype         IntegerField   doctype          
force_sequence  BooleanField   force sequence   
account         ForeignKey     account          
pos             IntegerField   pos              
printed_name    BabelCharField printed name     
printed_name_de CharField      printed name (de)
printed_name_fr CharField      printed name (fr)
printed_name_nl CharField      printed name (nl)
printed_name_et CharField      printed name (et)
=============== ============== =================

    
Defined in :srcref:`/lino/modlib/journals/models.py`

Referenced from
`lino.ledger.Booking.journal`_, `lino.sales.InvoicingMode.journal`_, `lino.sales.SalesRule.journal`_, `lino.sales.Order.journal`_, `lino.sales.Invoice.journal`_, `lino.finan.BankStatement.journal`_



.. index::
   single: field;id
   
.. _lino.journals.Journal.id:

Field **Journal.id**
====================





Type: CharField

   
.. index::
   single: field;name
   
.. _lino.journals.Journal.name:

Field **Journal.name**
======================





Type: CharField

   
.. index::
   single: field;doctype
   
.. _lino.journals.Journal.doctype:

Field **Journal.doctype**
=========================





Type: IntegerField

   
.. index::
   single: field;force_sequence
   
.. _lino.journals.Journal.force_sequence:

Field **Journal.force_sequence**
================================





Type: BooleanField

   
.. index::
   single: field;account
   
.. _lino.journals.Journal.account:

Field **Journal.account**
=========================





Type: ForeignKey

   
.. index::
   single: field;pos
   
.. _lino.journals.Journal.pos:

Field **Journal.pos**
=====================





Type: IntegerField

   
.. index::
   single: field;printed_name
   
.. _lino.journals.Journal.printed_name:

Field **Journal.printed_name**
==============================





Type: BabelCharField

   
.. index::
   single: field;printed_name_de
   
.. _lino.journals.Journal.printed_name_de:

Field **Journal.printed_name_de**
=================================





Type: CharField

   
.. index::
   single: field;printed_name_fr
   
.. _lino.journals.Journal.printed_name_fr:

Field **Journal.printed_name_fr**
=================================





Type: CharField

   
.. index::
   single: field;printed_name_nl
   
.. _lino.journals.Journal.printed_name_nl:

Field **Journal.printed_name_nl**
=================================





Type: CharField

   
.. index::
   single: field;printed_name_et
   
.. _lino.journals.Journal.printed_name_et:

Field **Journal.printed_name_et**
=================================





Type: CharField

   


