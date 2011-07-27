==========
properties
==========



.. currentmodule:: properties

Defined in :srcref:`/lino/modlib/properties/models.py`



:class:`PropType`
:class:`PropChoice`
:class:`PropGroup`
A :class:`PropOccurence` is when a certain "property owner" 
has a certain :class:`Property`. 
"Property owner" can be anything: 
a person, a company, a product, an upload, 
it depends on the implentation of :class:`PropOccurence`.
For example :mod:`lino.apps.dsbe.models.PersonProperty`.

A :class:`Property` defines the configuration of a property.

This module would deserve more documentation.




.. contents:: Table of Contents



.. index::
   pair: model; PropType

.. _lino.properties.PropType:

------------------
Model **PropType**
------------------




The type of the values that a property accepts.
Each PropType may (or may not) imply a list of choices.

Examples: of property types:
- Knowledge (Choices: "merely", "acceptable", "good", "very good",...)
- YesNo (no choices)


  
================ ============== ===========================================================
name             type           verbose name                                               
================ ============== ===========================================================
id               AutoField      ID                                                         
name             BabelCharField Designation (Beschreibung,Désignation)                     
choicelist       CharField      Choices List (Auswahliste,Liste de choix)                  
default_value    CharField      default value (Standardwert,valeur par défault)            
limit_to_choices BooleanField   Limit to choices (Beschränken auf Auswahl,Limite aux choix)
multiple_choices BooleanField   Multiple choices (Mehrfachauswahl,Choix multiples)         
name_fr          CharField      Designation (fr)                                           
name_nl          CharField      Designation (nl)                                           
name_en          CharField      Designation (en)                                           
================ ============== ===========================================================

    
Defined in :srcref:`/lino/modlib/properties/models.py`

Referenced from
`lino.properties.PropChoice.type`_, `lino.properties.Property.type`_



.. index::
   single: field;id
   
.. _lino.properties.PropType.id:

Field **PropType.id**
=====================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.properties.PropType.name:

Field **PropType.name**
=======================





Type: BabelCharField

   
.. index::
   single: field;choicelist
   
.. _lino.properties.PropType.choicelist:

Field **PropType.choicelist**
=============================





Type: CharField

   
.. index::
   single: field;default_value
   
.. _lino.properties.PropType.default_value:

Field **PropType.default_value**
================================





Type: CharField

   
.. index::
   single: field;limit_to_choices
   
.. _lino.properties.PropType.limit_to_choices:

Field **PropType.limit_to_choices**
===================================





Type: BooleanField

   
.. index::
   single: field;multiple_choices
   
.. _lino.properties.PropType.multiple_choices:

Field **PropType.multiple_choices**
===================================





Type: BooleanField

   
.. index::
   single: field;name_fr
   
.. _lino.properties.PropType.name_fr:

Field **PropType.name_fr**
==========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.properties.PropType.name_nl:

Field **PropType.name_nl**
==========================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _lino.properties.PropType.name_en:

Field **PropType.name_en**
==========================





Type: CharField

   


.. index::
   pair: model; PropChoice

.. _lino.properties.PropChoice:

--------------------
Model **PropChoice**
--------------------




A Choice for this PropType.
`text` is the text to be displayed in combo boxes.

`value` is the value to be stored in :attr:`PropValue.value`, 
it must be unique for all PropChoices of a given PropType.

Choices for a given PropType will be sorted on `value`
(we might make this more customizable if necessary by adding a new field `sort_text` 
and/or an option to sort on text instead of value) 

When configuring your property choices, be aware of the fact tht existing 
property occurences will *not* change when you change the `value` 
of a property choice.



  
======= ============== =======================================================
name    type           verbose name                                           
======= ============== =======================================================
id      AutoField      ID                                                     
type    ForeignKey     Property Type (Eigenschafts-Datentyp,Type de propriété)
value   CharField      Value (Wert,Valeur)                                    
text    BabelCharField Designation (Beschreibung,Désignation)                 
text_fr CharField      Designation (fr)                                       
text_nl CharField      Designation (nl)                                       
text_en CharField      Designation (en)                                       
======= ============== =======================================================

    
Defined in :srcref:`/lino/modlib/properties/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.properties.PropChoice.id:

Field **PropChoice.id**
=======================





Type: AutoField

   
.. index::
   single: field;type
   
.. _lino.properties.PropChoice.type:

Field **PropChoice.type**
=========================





Type: ForeignKey

   
.. index::
   single: field;value
   
.. _lino.properties.PropChoice.value:

Field **PropChoice.value**
==========================





Type: CharField

   
.. index::
   single: field;text
   
.. _lino.properties.PropChoice.text:

Field **PropChoice.text**
=========================





Type: BabelCharField

   
.. index::
   single: field;text_fr
   
.. _lino.properties.PropChoice.text_fr:

Field **PropChoice.text_fr**
============================





Type: CharField

   
.. index::
   single: field;text_nl
   
.. _lino.properties.PropChoice.text_nl:

Field **PropChoice.text_nl**
============================





Type: CharField

   
.. index::
   single: field;text_en
   
.. _lino.properties.PropChoice.text_en:

Field **PropChoice.text_en**
============================





Type: CharField

   


.. index::
   pair: model; PropGroup

.. _lino.properties.PropGroup:

-------------------
Model **PropGroup**
-------------------




A Property Group defines a list of Properties that fit together under a common name.
Examples of Property Groups: Skills, Soft Skills, Obstacles
There will be one menu entry per Group.

  
======= ============== ======================================
name    type           verbose name                          
======= ============== ======================================
id      AutoField      ID                                    
name    BabelCharField Designation (Beschreibung,Désignation)
name_fr CharField      Designation (fr)                      
name_nl CharField      Designation (nl)                      
name_en CharField      Designation (en)                      
======= ============== ======================================

    
Defined in :srcref:`/lino/modlib/properties/models.py`

Referenced from
`lino.lino.SiteConfig.propgroup_skills`_, `lino.lino.SiteConfig.propgroup_softskills`_, `lino.lino.SiteConfig.propgroup_obstacles`_, `lino.properties.Property.group`_, `lino.properties.PersonProperty.group`_, `lino.properties.WantedSkill.group`_, `lino.properties.UnwantedSkill.group`_



.. index::
   single: field;id
   
.. _lino.properties.PropGroup.id:

Field **PropGroup.id**
======================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.properties.PropGroup.name:

Field **PropGroup.name**
========================





Type: BabelCharField

   
.. index::
   single: field;name_fr
   
.. _lino.properties.PropGroup.name_fr:

Field **PropGroup.name_fr**
===========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.properties.PropGroup.name_nl:

Field **PropGroup.name_nl**
===========================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _lino.properties.PropGroup.name_en:

Field **PropGroup.name_en**
===========================





Type: CharField

   


.. index::
   pair: model; Property

.. _lino.properties.Property:

------------------
Model **Property**
------------------



Property(id, name, group_id, type_id, name_fr, name_nl, name_en)
  
======= ============== ========================================================
name    type           verbose name                                            
======= ============== ========================================================
id      AutoField      ID                                                      
name    BabelCharField Designation (Beschreibung,Désignation)                  
group   ForeignKey     Property Group (Eigenschaftsgruppe,Groupe de propriétés)
type    ForeignKey     Property Type (Eigenschafts-Datentyp,Type de propriété) 
name_fr CharField      Designation (fr)                                        
name_nl CharField      Designation (nl)                                        
name_en CharField      Designation (en)                                        
======= ============== ========================================================

    
Defined in :srcref:`/lino/modlib/properties/models.py`

Referenced from
`lino.properties.PersonProperty.property`_, `lino.properties.WantedSkill.property`_, `lino.properties.UnwantedSkill.property`_



.. index::
   single: field;id
   
.. _lino.properties.Property.id:

Field **Property.id**
=====================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.properties.Property.name:

Field **Property.name**
=======================





Type: BabelCharField

   
.. index::
   single: field;group
   
.. _lino.properties.Property.group:

Field **Property.group**
========================





Type: ForeignKey

   
.. index::
   single: field;type
   
.. _lino.properties.Property.type:

Field **Property.type**
=======================





Type: ForeignKey

   
.. index::
   single: field;name_fr
   
.. _lino.properties.Property.name_fr:

Field **Property.name_fr**
==========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _lino.properties.Property.name_nl:

Field **Property.name_nl**
==========================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _lino.properties.Property.name_en:

Field **Property.name_en**
==========================





Type: CharField

   


.. index::
   pair: model; PersonProperty

.. _lino.properties.PersonProperty:

------------------------
Model **PersonProperty**
------------------------



A certain property defined for a certain person. 
    See :mod:`lino.modlib.properties`.
  
======== ========== ========================================================
name     type       verbose name                                            
======== ========== ========================================================
id       AutoField  ID                                                      
group    ForeignKey Property group (Eigenschaftsgruppe,Groupe de propriétés)
property ForeignKey Property (Eigenschaft,Propriété)                        
value    CharField  Value (Wert,Valeur)                                     
person   ForeignKey person (Person,Personne)                                
remark   CharField  Remark (Bemerkung,Remarque)                             
======== ========== ========================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.properties.PersonProperty.id:

Field **PersonProperty.id**
===========================





Type: AutoField

   
.. index::
   single: field;group
   
.. _lino.properties.PersonProperty.group:

Field **PersonProperty.group**
==============================





Type: ForeignKey

   
.. index::
   single: field;property
   
.. _lino.properties.PersonProperty.property:

Field **PersonProperty.property**
=================================





Type: ForeignKey

   
.. index::
   single: field;value
   
.. _lino.properties.PersonProperty.value:

Field **PersonProperty.value**
==============================





Type: CharField

   
.. index::
   single: field;person
   
.. _lino.properties.PersonProperty.person:

Field **PersonProperty.person**
===============================





Type: ForeignKey

   
.. index::
   single: field;remark
   
.. _lino.properties.PersonProperty.remark:

Field **PersonProperty.remark**
===============================





Type: CharField

   


.. index::
   pair: model; WantedSkill

.. _lino.properties.WantedSkill:

---------------------
Model **WantedSkill**
---------------------



WantedSkill(id, group_id, property_id, value, search_id)
  
======== ========== ========================================================
name     type       verbose name                                            
======== ========== ========================================================
id       AutoField  ID                                                      
group    ForeignKey Property group (Eigenschaftsgruppe,Groupe de propriétés)
property ForeignKey Property (Eigenschaft,Propriété)                        
value    CharField  Value (Wert,Valeur)                                     
search   ForeignKey search                                                  
======== ========== ========================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.properties.WantedSkill.id:

Field **WantedSkill.id**
========================





Type: AutoField

   
.. index::
   single: field;group
   
.. _lino.properties.WantedSkill.group:

Field **WantedSkill.group**
===========================





Type: ForeignKey

   
.. index::
   single: field;property
   
.. _lino.properties.WantedSkill.property:

Field **WantedSkill.property**
==============================





Type: ForeignKey

   
.. index::
   single: field;value
   
.. _lino.properties.WantedSkill.value:

Field **WantedSkill.value**
===========================





Type: CharField

   
.. index::
   single: field;search
   
.. _lino.properties.WantedSkill.search:

Field **WantedSkill.search**
============================





Type: ForeignKey

   


.. index::
   pair: model; UnwantedSkill

.. _lino.properties.UnwantedSkill:

-----------------------
Model **UnwantedSkill**
-----------------------



UnwantedSkill(id, group_id, property_id, value, search_id)
  
======== ========== ========================================================
name     type       verbose name                                            
======== ========== ========================================================
id       AutoField  ID                                                      
group    ForeignKey Property group (Eigenschaftsgruppe,Groupe de propriétés)
property ForeignKey Property (Eigenschaft,Propriété)                        
value    CharField  Value (Wert,Valeur)                                     
search   ForeignKey search                                                  
======== ========== ========================================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.properties.UnwantedSkill.id:

Field **UnwantedSkill.id**
==========================





Type: AutoField

   
.. index::
   single: field;group
   
.. _lino.properties.UnwantedSkill.group:

Field **UnwantedSkill.group**
=============================





Type: ForeignKey

   
.. index::
   single: field;property
   
.. _lino.properties.UnwantedSkill.property:

Field **UnwantedSkill.property**
================================





Type: ForeignKey

   
.. index::
   single: field;value
   
.. _lino.properties.UnwantedSkill.value:

Field **UnwantedSkill.value**
=============================





Type: CharField

   
.. index::
   single: field;search
   
.. _lino.properties.UnwantedSkill.search:

Field **UnwantedSkill.search**
==============================





Type: ForeignKey

   


