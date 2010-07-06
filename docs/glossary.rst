Glossary
========


.. glossary::

  Tups
     The machine that is serving saffre-rumma.ee

  DSBE
     "Dienst für Sozial-Berufliche Eingliederung"     
     A public service in Eupen (Belgium) who will probably be the first user of a Lino application.


Settings
--------

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
----------------------

.. class:: NoteType

  .. attribute:: print_method
  
    The print method to be used.
    
  .. attribute:: template
    
    The template to be used.
    
.. class:: Note

  .. attribute:: language    
    
