==============================
The Ext.ensible Calendar Panel
==============================

.. module:: ml.extensible

This page documents the :mod:`lino.modlib.extensible` app, an
extension to :mod:`ml.cal` which uses the `Extensible
<http://ext.ensible.com>`_ calendar library to adds a special
"Calendar Panel" view of your calendar events.

.. contents:: 
   :local:
   :depth: 2


The ``CalendarPanel`` class
===========================

.. class:: CalendarPanel(dd.Frame)

    Opens the "Calendar View" (a special window with the
    Ext.ensible CalendarAppPanel).

Configuration
=============

.. class:: Plugin

  Extends :class:`lino.core.plugin.Plugin`. See also :doc:`/dev/ad`.

  .. attribute:: calendar_start_hour

  The time at which the CalendarPanel's daily view starts.

  .. attribute:: calendar_end_hour

  The time at which the CalendarPanel's daily view ends.

  .. attribute:: media_base_url
