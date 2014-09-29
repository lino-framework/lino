=================
The `lino` plugin
=================

.. module:: ml.lino

The :mod:`lino` package is a Django app which gets automatically
installed.  It does not define any models but some choicelists which
are available in :mod:`dd`.

.. currentmodule:: dd


Choicelists
===========

.. class:: Genders(dd.ChoiceList)

    Defines the two possible choices "male" and "female"
    for the gender of a person.
    See :ref:`lino.tutorial.human` for examples.

    .. django2rst:: 

            rt.show(lino.Genders)


.. class:: YesNo(dd.ChoiceList)

    Used to define parameter panel fields for BooleanFields::
    
      foo = dd.YesNo.field(_("Foo"), blank=True)
      
    .. django2rst:: 

            rt.show(lino.YesNo)


.. class:: PeriodEvents(dd.ChoiceList):

    List of things you can observe on a :class:`dd.DatePeriod`. The
    default list has the following choices:

    .. django2rst::

      rt.show(lino.PeriodEvents)

