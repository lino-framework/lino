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




.. toctree::
    :maxdepth: 2

    properties.PropType
    properties.PropChoice
    properties.PropGroup
    properties.Property
    properties.PersonProperty
    properties.WantedSkill
    properties.UnwantedSkill


