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




.. index::
   pair: model; PropType
   single: field;id
   single: field;name
   single: field;choicelist
   single: field;default_value
   single: field;limit_to_choices
   single: field;multiple_choices
   single: field;name_fr
   single: field;name_nl
   single: field;name_en

.. _dsbe.properties.PropType:

------------------
Model ``PropType``
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
   pair: model; PropChoice
   single: field;id
   single: field;type
   single: field;value
   single: field;text
   single: field;text_fr
   single: field;text_nl
   single: field;text_en

.. _dsbe.properties.PropChoice:

--------------------
Model ``PropChoice``
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
   pair: model; PropGroup
   single: field;id
   single: field;name
   single: field;name_fr
   single: field;name_nl
   single: field;name_en

.. _dsbe.properties.PropGroup:

-------------------
Model ``PropGroup``
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
   pair: model; Property
   single: field;id
   single: field;name
   single: field;group
   single: field;type
   single: field;name_fr
   single: field;name_nl
   single: field;name_en

.. _dsbe.properties.Property:

------------------
Model ``Property``
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
   pair: model; PersonProperty
   single: field;id
   single: field;group
   single: field;property
   single: field;value
   single: field;person
   single: field;remark

.. _dsbe.properties.PersonProperty:

------------------------
Model ``PersonProperty``
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

    
Defined in :srcref:`/lino/sites/dsbe/models.py`


.. index::
   pair: model; WantedSkill
   single: field;id
   single: field;group
   single: field;property
   single: field;value
   single: field;search

.. _dsbe.properties.WantedSkill:

---------------------
Model ``WantedSkill``
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

    
Defined in :srcref:`/lino/sites/dsbe/models.py`


.. index::
   pair: model; UnwantedSkill
   single: field;id
   single: field;group
   single: field;property
   single: field;value
   single: field;search

.. _dsbe.properties.UnwantedSkill:

-----------------------
Model ``UnwantedSkill``
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

    
Defined in :srcref:`/lino/sites/dsbe/models.py`


