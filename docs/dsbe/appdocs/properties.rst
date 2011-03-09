==========
properties
==========



.. currentmodule:: properties

Defined in :srcref:`/lino/modlib/properties/models.py`



Todo:

Property.type should not be a ForeignKey to PropType, 
but a simple reference to a PropertyType instance.
There should be a list of PropertyType objects, 
some of them not stored (like YesNo and 
and only 



.. contents:: Table of Contents



.. index::
   pair: model; PropType

.. _dsbe.properties.PropType:

------------------
Model **PropType**
------------------




The type of the values that a property accepts.
Each PropType may (or may not) imply a list of choices.

Examples: of property types:
- Knowledge (Choices: "merely", "acceptable", "good", "very good",...)
- YesNo (no choices)


  
================ ============== ==========================================
name             type           verbose name                              
================ ============== ==========================================
id               AutoField      ID                                        
name             BabelCharField Designation (Beschreibung)                
choicelist       CharField      Choices List                              
default_value    CharField      default value                             
limit_to_choices BooleanField   Limit to choices (Beschränken auf Auswahl)
multiple_choices BooleanField   Multiple choices                          
name_fr          CharField      Designation (fr)                          
name_nl          CharField      Designation (nl)                          
name_en          CharField      Designation (en)                          
================ ============== ==========================================

    
Defined in :srcref:`/lino/modlib/properties/models.py`

.. index::
   single: field;id
   
.. _dsbe.properties.PropType.id:

Field **PropType.id**
=====================





Type: AutoField

   
.. index::
   single: field;name
   
.. _dsbe.properties.PropType.name:

Field **PropType.name**
=======================





Type: BabelCharField

   
.. index::
   single: field;choicelist
   
.. _dsbe.properties.PropType.choicelist:

Field **PropType.choicelist**
=============================





Type: CharField

   
.. index::
   single: field;default_value
   
.. _dsbe.properties.PropType.default_value:

Field **PropType.default_value**
================================





Type: CharField

   
.. index::
   single: field;limit_to_choices
   
.. _dsbe.properties.PropType.limit_to_choices:

Field **PropType.limit_to_choices**
===================================





Type: BooleanField

   
.. index::
   single: field;multiple_choices
   
.. _dsbe.properties.PropType.multiple_choices:

Field **PropType.multiple_choices**
===================================





Type: BooleanField

   
.. index::
   single: field;name_fr
   
.. _dsbe.properties.PropType.name_fr:

Field **PropType.name_fr**
==========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _dsbe.properties.PropType.name_nl:

Field **PropType.name_nl**
==========================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _dsbe.properties.PropType.name_en:

Field **PropType.name_en**
==========================





Type: CharField

   


.. index::
   pair: model; PropChoice

.. _dsbe.properties.PropChoice:

--------------------
Model **PropChoice**
--------------------




A Choice for this PropType.
`value` is the value to be stored in :attr:`PropValue.value`.
`text` is the text to be displayed in combo boxes.

  
======= ============== ===============================
name    type           verbose name                   
======= ============== ===============================
id      AutoField      ID                             
type    ForeignKey     Property Type (Eigenschaftsart)
value   CharField      Value (Wert)                   
text    BabelCharField Designation (Beschreibung)     
text_fr CharField      Designation (fr)               
text_nl CharField      Designation (nl)               
text_en CharField      Designation (en)               
======= ============== ===============================

    
Defined in :srcref:`/lino/modlib/properties/models.py`

.. index::
   single: field;id
   
.. _dsbe.properties.PropChoice.id:

Field **PropChoice.id**
=======================





Type: AutoField

   
.. index::
   single: field;type
   
.. _dsbe.properties.PropChoice.type:

Field **PropChoice.type**
=========================





Type: ForeignKey

   
.. index::
   single: field;value
   
.. _dsbe.properties.PropChoice.value:

Field **PropChoice.value**
==========================





Type: CharField

   
.. index::
   single: field;text
   
.. _dsbe.properties.PropChoice.text:

Field **PropChoice.text**
=========================





Type: BabelCharField

   
.. index::
   single: field;text_fr
   
.. _dsbe.properties.PropChoice.text_fr:

Field **PropChoice.text_fr**
============================





Type: CharField

   
.. index::
   single: field;text_nl
   
.. _dsbe.properties.PropChoice.text_nl:

Field **PropChoice.text_nl**
============================





Type: CharField

   
.. index::
   single: field;text_en
   
.. _dsbe.properties.PropChoice.text_en:

Field **PropChoice.text_en**
============================





Type: CharField

   


.. index::
   pair: model; PropGroup

.. _dsbe.properties.PropGroup:

-------------------
Model **PropGroup**
-------------------




A Property Group defines a list of Properties that fit together under a common name.
Examples of Property Groups: Skills, Soft Skills, Obstacles
There will be one menu entry per Group.

  
======= ============== ==========================
name    type           verbose name              
======= ============== ==========================
id      AutoField      ID                        
name    BabelCharField Designation (Beschreibung)
name_fr CharField      Designation (fr)          
name_nl CharField      Designation (nl)          
name_en CharField      Designation (en)          
======= ============== ==========================

    
Defined in :srcref:`/lino/modlib/properties/models.py`

.. index::
   single: field;id
   
.. _dsbe.properties.PropGroup.id:

Field **PropGroup.id**
======================





Type: AutoField

   
.. index::
   single: field;name
   
.. _dsbe.properties.PropGroup.name:

Field **PropGroup.name**
========================





Type: BabelCharField

   
.. index::
   single: field;name_fr
   
.. _dsbe.properties.PropGroup.name_fr:

Field **PropGroup.name_fr**
===========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _dsbe.properties.PropGroup.name_nl:

Field **PropGroup.name_nl**
===========================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _dsbe.properties.PropGroup.name_en:

Field **PropGroup.name_en**
===========================





Type: CharField

   


.. index::
   pair: model; Property

.. _dsbe.properties.Property:

------------------
Model **Property**
------------------



Property(id, name, group_id, type_id, name_fr, name_nl, name_en)
  
======= ============== ===================================
name    type           verbose name                       
======= ============== ===================================
id      AutoField      ID                                 
name    BabelCharField Designation (Beschreibung)         
group   ForeignKey     Property Group (Eigenschaftsgruppe)
type    ForeignKey     Property Type (Eigenschaftsart)    
name_fr CharField      Designation (fr)                   
name_nl CharField      Designation (nl)                   
name_en CharField      Designation (en)                   
======= ============== ===================================

    
Defined in :srcref:`/lino/modlib/properties/models.py`

.. index::
   single: field;id
   
.. _dsbe.properties.Property.id:

Field **Property.id**
=====================





Type: AutoField

   
.. index::
   single: field;name
   
.. _dsbe.properties.Property.name:

Field **Property.name**
=======================





Type: BabelCharField

   
.. index::
   single: field;group
   
.. _dsbe.properties.Property.group:

Field **Property.group**
========================





Type: ForeignKey

   
.. index::
   single: field;type
   
.. _dsbe.properties.Property.type:

Field **Property.type**
=======================





Type: ForeignKey

   
.. index::
   single: field;name_fr
   
.. _dsbe.properties.Property.name_fr:

Field **Property.name_fr**
==========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _dsbe.properties.Property.name_nl:

Field **Property.name_nl**
==========================





Type: CharField

   
.. index::
   single: field;name_en
   
.. _dsbe.properties.Property.name_en:

Field **Property.name_en**
==========================





Type: CharField

   


.. index::
   pair: model; PersonProperty

.. _dsbe.properties.PersonProperty:

------------------------
Model **PersonProperty**
------------------------



PersonProperty(id, group_id, property_id, value, person_id, remark)
  
======== ========== ===================================
name     type       verbose name                       
======== ========== ===================================
id       AutoField  ID                                 
group    ForeignKey Property group (Eigenschaftsgruppe)
property ForeignKey Property (Eigenschaft)             
value    CharField  Value (Wert)                       
person   ForeignKey person (Person)                    
remark   CharField  Remark (Bemerkung)                 
======== ========== ===================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.properties.PersonProperty.id:

Field **PersonProperty.id**
===========================





Type: AutoField

   
.. index::
   single: field;group
   
.. _dsbe.properties.PersonProperty.group:

Field **PersonProperty.group**
==============================





Type: ForeignKey

   
.. index::
   single: field;property
   
.. _dsbe.properties.PersonProperty.property:

Field **PersonProperty.property**
=================================





Type: ForeignKey

   
.. index::
   single: field;value
   
.. _dsbe.properties.PersonProperty.value:

Field **PersonProperty.value**
==============================





Type: CharField

   
.. index::
   single: field;person
   
.. _dsbe.properties.PersonProperty.person:

Field **PersonProperty.person**
===============================





Type: ForeignKey

   
.. index::
   single: field;remark
   
.. _dsbe.properties.PersonProperty.remark:

Field **PersonProperty.remark**
===============================





Type: CharField

   


.. index::
   pair: model; WantedSkill

.. _dsbe.properties.WantedSkill:

---------------------
Model **WantedSkill**
---------------------



WantedSkill(id, group_id, property_id, value, search_id)
  
======== ========== ===================================
name     type       verbose name                       
======== ========== ===================================
id       AutoField  ID                                 
group    ForeignKey Property group (Eigenschaftsgruppe)
property ForeignKey Property (Eigenschaft)             
value    CharField  Value (Wert)                       
search   ForeignKey search                             
======== ========== ===================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.properties.WantedSkill.id:

Field **WantedSkill.id**
========================





Type: AutoField

   
.. index::
   single: field;group
   
.. _dsbe.properties.WantedSkill.group:

Field **WantedSkill.group**
===========================





Type: ForeignKey

   
.. index::
   single: field;property
   
.. _dsbe.properties.WantedSkill.property:

Field **WantedSkill.property**
==============================





Type: ForeignKey

   
.. index::
   single: field;value
   
.. _dsbe.properties.WantedSkill.value:

Field **WantedSkill.value**
===========================





Type: CharField

   
.. index::
   single: field;search
   
.. _dsbe.properties.WantedSkill.search:

Field **WantedSkill.search**
============================





Type: ForeignKey

   


.. index::
   pair: model; UnwantedSkill

.. _dsbe.properties.UnwantedSkill:

-----------------------
Model **UnwantedSkill**
-----------------------



UnwantedSkill(id, group_id, property_id, value, search_id)
  
======== ========== ===================================
name     type       verbose name                       
======== ========== ===================================
id       AutoField  ID                                 
group    ForeignKey Property group (Eigenschaftsgruppe)
property ForeignKey Property (Eigenschaft)             
value    CharField  Value (Wert)                       
search   ForeignKey search                             
======== ========== ===================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

.. index::
   single: field;id
   
.. _dsbe.properties.UnwantedSkill.id:

Field **UnwantedSkill.id**
==========================





Type: AutoField

   
.. index::
   single: field;group
   
.. _dsbe.properties.UnwantedSkill.group:

Field **UnwantedSkill.group**
=============================





Type: ForeignKey

   
.. index::
   single: field;property
   
.. _dsbe.properties.UnwantedSkill.property:

Field **UnwantedSkill.property**
================================





Type: ForeignKey

   
.. index::
   single: field;value
   
.. _dsbe.properties.UnwantedSkill.value:

Field **UnwantedSkill.value**
=============================





Type: CharField

   
.. index::
   single: field;search
   
.. _dsbe.properties.UnwantedSkill.search:

Field **UnwantedSkill.search**
==============================





Type: ForeignKey

   


