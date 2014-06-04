========
Debts
========

.. module:: ml.debts

Models
======

.. class:: Budget

A document which expresses the financial situation of a partner at a
given date.

.. class:: Entry(dd.Model)

  .. attribute:: budget

    ForeignKey to the :class:`Budget`.

.. class:: Actor(dd.Model)

  .. attribute:: budget

    ForeignKey to the :class:`Budget`.




Tables
======

.. class:: Clients(dd.Table)

