.. _dev.actors: 

======
Actors
======

Note: this is intended to be a rather dry but complete document for
reference purposes.  See also some tutorials:

- :doc:`/tutorials/vtables/index`
- :doc:`/tutorials/tables/index`
- :doc:`/tutorials/actors/index`


Overview
--------

An :class:`Actor <lino.core.actors.Actor>` is a globally known unique
thing that offers :ref:`actions <dev.actions>`.  An alternative name for
"Actor" might be "Resource" or "View", but these words are already
being used very often, so in this section we talk about actors.

Each actor has a list of :doc:`actions <actions>`.  Almost every
incoming web request in a Lino application is a given *user* who
requests execution of a given *action* on a given *actor*.

Each subclass of an actor is a new actor.


The global namespace
--------------------

When we say "a globally known unique thing", then we refer to the
global namespace.


Actors are classes, not instances
---------------------------------

Actors are never instantiated, we use only the class objects.

The main reason for this design choice was that it leads to more
readable application code. This is not an absolute decision,
however. We might decide one day that Lino creates an automatic
singleton instance for each Actor at startup. That would avoid us to
write all those `@classmethod` decorators.


.. _dev.tables: 

Tables
------

The most common type of actors are tables. A Table is an Actor which
displays some data in a tabular way, i.e. interactively as a GridPanel
or on a printable document as a table.

There are VirtualTable and "normal" (model-based) tables. And then
there is a third kind of table is special: the EmptyTable.

The **columns** of a table are defined by attributes like 
`column_names`.

.. autoattribute:: lino.core.tables.AbstractTable.column_names

The **rows** of a table are defined using a multitude of 

In a virtual table theyr are defined by a method `get_data_rows`.
The rows of a model-based table are indirectly defined by its `model`..

