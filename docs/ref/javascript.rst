====================
Javascript functions
====================

.. default-domain:: js


Defined in lino.js
------------------

.. class:: Lino.WindowWrapper

  See :doc:`/blog/2010/20100716`
  
  .. function:: Lino.WindowWrapper.load_master_record(record)
  
    Loads the specified record into this window.
  
  .. function:: Lino.WindowWrapper.show()
  
    Display this window.

  
.. js:class:: Lino.FormPanel

  .. js:attribute:: Lino.FormPanel.ls_data_url
  
    The base URI of the report.
  
  .. js:attribute:: Lino.FormPanel.data_record
  
    An object that should have at least these attributes:
    - title
    - values
  
  See :doc:`/blog/2010/20100714`
  
  .. js:function:: Lino.FormPanel.load_master_record
  
  
    
.. js:class:: Lino.GridPanel

  .. js:function:: Lino.GridPanel.load_slavegrid()
  
  .. js:attribute:: Lino.GridPanel.ls_data_url
  
    The base URI of the report.
  
  See :doc:`/blog/2010/20100714`
  
.. js:function:: Lino.id_renderer()

Defined in site.js
------------------

.. js:function:: Lino.notes.NoteTypes.grid(params)

  :param object params: Parameters to override default config values.
  :returns: null
   
  See :doc:`/blog/2010/20100706`
   

Names from external libraries
-----------------------------

.. js:class:: Ext.ux.grid.GridFilters


