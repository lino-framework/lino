========
Glossary
========


.. glossary::

  Tups
     The machine that is serving saffre-rumma.ee

  DSBE
     "Dienst für Sozial-Berufliche Eingliederung"     
     A public service in Eupen (Belgium) who will probably be the first user of a Lino application.
     
  LinksByOwner   
    http://code.google.com/p/lino/source/browse/src/lino/modlib/links/models.py
    
  ExtJS
    http://www.sencha.com/products/js/


Settings
--------

.. setting:: MEDIA_ROOT

   Used by FileSystemStorage


.. setting:: PROJECT_DIR

  Directory where local configuration files are stored.
  I always set this variable to the absolute path of the :envvar:`DJANGO_SETTINGS_MODULE`.
  Local configuration files are:
  - settings.py
  - manage.py
  - lino_settings.py
  - fill.py & load_tim.py (which should once become commands for manage.py)
  

.. setting:: DATA_DIR

   Directory where local data gets stored. 
   On a Unix production system I suggest to set it to `/usr/local/lino`. 
   The development and demo configrations set it to ``os.path.join(PROJECT_DIR,'data')``.
   
.. setting:: MODEL_DEBUG

  If this is `True`, Lino will write more debugging info about the models and reports.

.. setting:: REMOTE_USER
  
  To be used only for development server. Simulates 
  
.. setting:: BYPASS_PERMS

   If this is `True`, Lino won't apply any user permission checks.
   
   
.. setting:: USER_INTERFACES
  
   Lino-specific setting. See :doc:`/blog/2010/20100624`.
   

.. default-domain:: py

  
Modules
-------

.. module:: lino.reports
    :synopsis: Report and ReportHandle
    
.. class:: Report

  .. method:: do_setup()
  
    Sets up the report. Called once for each UI when web server starts up.
  
  

.. module:: lino.ui.extjsw
    :synopsis: UI using windowed ExtJS

.. module:: lino.ui.extjsu
    :synopsis: UI using non-windowed ExtJS and URL

.. module:: lino.utils.mixins

.. js:function:: Lino.notes.NoteTypes.grid()

    See :doc:`blog/2010/20100706`
   

.. module:: lino.modlib.notes.models

``lino.modlib.notes``
---------------------

.. class:: NoteType

  .. attribute:: print_method
  
    The print method to be used.
    
  .. attribute:: template
    
    The template to be used.
    
.. class:: Note

  .. attribute:: language    
    

.. module:: lino.modlib.countries.models

``lino.modlib.countries``
-------------------------

Source :srcref:`/lino/modlib/countries/models.py`.
  
Models
======

.. model:: countries.Country

  One entry per country.
  
.. model:: countries.City

  One entry per city.
  
    