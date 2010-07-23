==============
Python Modules
==============

``lino.reports``
----------------

.. module:: lino.reports
    :synopsis: Report and ReportHandle
    
.. class:: Report

  .. method:: do_setup()
  
    Sets up the report. Called once for each UI when web server starts up.
  
  

``lino.ui.extjsw``
------------------

.. module:: lino.ui.extjsw
    :synopsis: UI using windowed ExtJS

``lino.ui.extjsu``
------------------

.. module:: lino.ui.extjsu
    :synopsis: UI using non-windowed ExtJS and URL


``lino.utils.mixins``
---------------------

.. module:: lino.utils.mixins


``lino.modlib.notes``
---------------------
.. module:: lino.modlib.notes.models
.. class:: NoteType

  .. attribute:: print_method
  
    The print method to be used.
    
  .. attribute:: template
    
    The template to be used.
    
  .. method:: template_type
    
    Implements
    
.. class:: Note

  .. attribute:: language    
    

``lino.modlib.countries``
-------------------------

.. module:: lino.modlib.countries.models

``lino.modlib.countries``
-------------------------

Source :srcref:`/lino/modlib/countries/models.py`.
  
.. class:: countries.Country(django.db.models.Model)

  One entry per country.
  
.. class:: countries.Countries(django.db.models.Model)

  Report for :class:`Country`
  
  
.. class:: countries.City(django.db.models.Model)

  One entry per city.
  
    
    
