Special model attributes used by Lino
=====================================

allow_cascaded_delete
=====================

If a Model has this attribute defined with 
a value of `True`, Lino will consider this data as "relatively worthless", 
meaning that they get deleted if an object to which they refer is being 
deleted.

Lino by default forbids to delete an object that is 
referenced by other objects.

Examples of such models are 
:class:`lino.apps.dsbe.models.PersonProperty`
and
:class:`lino.apps.dsbe.models.LanguageKnowledge`.


disable_delete
==============

disabled_fields
===============


disable_editing
===============

