=====================
Lino Standard Library
=====================

.. _lino.lib.users:

Users module
------------

.. _lino.lib.users.User:

User
----

A User means somebody who can log into the application.



.. _lino.lib.users.Group:

Group
-----

The permissions do not depend on the user group, they depend on the :ref:`lib.users.UserProfiles`.
Belonging to a user group or not user group has no influence on access permissions




.. _lino.lib.users.Membership:

Membership
----------

A membership is when a given :ref:`lino.lib.users.User` 
belongs to a given :ref:`lino.lib.users.Group`.



.. _lino.lib.cal:

Calendar module
---------------

If you have a `Calendar` item in your main menu, then you 
probably have Lino's calendar module.

.. _lino.lib.cal.Event:

Event
-----

A calendar event is when something happens.



.. _lino.lib.countries.City:

City
----

A better name would be "geographical place" because 
a City, in Lino, can also be a suburb, a town, 
a province, a lake... any geographic entity 
(except a :ref:`lino.lib.countries.Country` 
because these have their own table).

.. _lino.lib.countries.Country:

Country
-------

Many Lino applications have a table of countries.

