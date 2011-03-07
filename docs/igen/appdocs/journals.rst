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




.. index::
   pair: model; Journal
   single: field;id
   single: field;name
   single: field;doctype
   single: field;force_sequence
   single: field;account
   single: field;pos
   single: field;printed_name
   single: field;printed_name_de
   single: field;printed_name_fr
   single: field;printed_name_nl
   single: field;printed_name_et

.. _igen.journals.Journal:

-----------------
Model ``Journal``
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


