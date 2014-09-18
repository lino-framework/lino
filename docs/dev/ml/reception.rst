=========
Reception
=========

.. module:: ml.reception

The :mod:`lino.modlib.reception` package provides functionality for
running a reception desk. It depends on :mod:`ml.cal`. It does not
aadd any model, but adds some workflow states, actions and tables.

.. contents:: 
   :local:
   :depth: 2


Tables
======

.. class:: AppointmentsByPartner
.. class:: ExpectedGuests
.. class:: Visitors
.. class:: MyVisitors
.. class:: BusyVisitors
.. class:: WaitingVisitors
.. class:: GoneVisitors


Actions
=======

.. class:: CheckinVisitor
.. class:: ReceiveVisitor
.. class:: CheckoutVisitor
