========
Courses
========

.. module:: ml.courses

The :mod:`lino.modlib.courses` package provides data definitions for
managing "Courses".


.. contents:: 
   :local:
   :depth: 2

Models
======

.. class:: Pupil
.. class:: Teacher

.. class:: Course

    Notes about automatic event generation:
    
    - When an automatically generated event is to be moved to another
      date, e.g. because it falls into a vacation period, then you
      simply change it's date.  Lino will automatically adapt all
      subsequent events.
      
    - Marking an automatically generated event as "Cancelled" will not
      create a replacement event.


.. class:: Line

    A line (of Courses) is a series which groups
    courses into a configurable list of categories. 


