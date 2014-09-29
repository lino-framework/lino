=================
The `lino` plugin
=================

.. module:: ml.lino

The :mod:`lino` package is also a Django app which gets automatically
installed. It dos not define any models but some choicelists.


Choicelists
===========

.. class:: Genders(dd.ChoiceList)

    .. django2rst:: 

            rt.show(lino.Genders)


.. class:: YesNo(dd.ChoiceList)

    .. django2rst:: 

            rt.show(lino.YesNo)


