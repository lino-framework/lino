==========
Households
==========

.. module:: ml.households


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



Models
======

.. class:: Household

  A Household is a subclass of :class:`ml.contacts.Partner`.

.. class:: HouseholdType

.. class:: Member

  Represents a membership, i.e. the fact that a given person is part
  of a given household.

  .. attribute:: start_date

    Since when this membership exists. This is usually empty.

  .. attribute:: end_date

    Until when this membership exists.


Tables
======

.. class:: SiblingsByPerson

  Displays the siblings of a given person in that person's active
  household.

  The active household is determined as follows:

  - If the person has only one household, use this.
  - Otherwise, if one household is marked as primary, use this.
  - Otherwise, if there is exactly one membership whose end_date is
    either empty or in the future, take this.

  If no active household can be determined, the panel just displays an
  apporpriate message.
