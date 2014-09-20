Human Links
===========

.. module:: ml.humanlinks

Defines "parency links" between two "persons", and a user interface to
manage them.  This module is probably useful in combination with
:mod:`ml.households`.

.. contents:: 
   :local:
   :depth: 2


Configuration
=============

.. class:: Plugin

  Extends :class:`ad.Plugin`. See also :doc:`/dev/ad`.

  .. attribute:: person_model

    A string referring to the model which represents a human in your
    application.  Default value is ``'contacts.Person'`` (referring to
    :class:`ml.contacts.Person`).


Choicelists
===========

.. class:: LinkTypes

    A :class:`dd.ChoiceList` of possible values for the
    :attr:`Link.type` field. The default list contains the following
    data:
    
    .. django2rst::
        
        rt.show(humanlinks.LinkTypes)


Models
======

.. class:: Link

  A link between two persons.

  .. attribute:: parent

    Pointer to the person who is "parent".

  .. attribute:: child

    Pointer to the person who is "child".

  .. attribute:: type

    Pointer to :class:`LinkTypes`.


Tables
======

.. class:: LinksByHuman

    Display all human links of the master, using both the parent and
    the child directions.

    It is a cool usage example for using a
    :meth:`dd.Table.get_request_queryset` method instead of
    :attr:`dd.Table.master_key`.

    It is also a cool usage example for the
    :meth:`dd.Table.get_slave_summary` method.




