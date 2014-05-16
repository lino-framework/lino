====================
Javascript functions
====================

.. default-domain:: js


The ``linoweb.js`` file
=======================

.. xfile:: linoweb.js

The :srcref:`lino/modlib/extjs/linoweb.js` template is used to
generate a huge monolythic javascript file which contains
Lino-specific Javascript functions.


General functions
------------------

.. function:: Lino.id_renderer()
.. function:: Lino.logout(id, name)

Action calls
------------

Functions which have to do with AJAX calls:

- :func:`Lino.row_action_handler`
- :func:`Lino.list_action_handler` 
- :func:`Lino.run_row_action`
- :func:`Lino.logout`

- :func:`Lino.call_ajax_action`

- :func:`Lino.put`
- :func:`Lino.action_handler`
- :func:`Lino.handle_action_result`
- :func:`Lino.FormPanel.load_record_id`

- :func:`Lino.FormPanel.save`
- :func:`Lino.ActionFormPanel.on_ok`
- :func:`Lino.GridPanel.on_afteredit`


.. graphviz:: 

   digraph "Who's who in :xfile:`linoweb.js`" {

    row_action_handler -> call_ajax_action;
    list_action_handler -> call_ajax_action;
    run_row_action -> call_ajax_action;
    logout -> call_ajax_action;
    
    put -> action_handler;
    on_afteredit -> action_handler;
    
    "ActionFormPanel.on_ok" -> call_ajax_action;
    call_ajax_action -> action_handler;
    action_handler -> handle_action_result;

    "FormPanel.save"  -> handle_action_result;
    
    handle_action_result -> action_handler;
   }

TODO:

- Convert :func:`Lino.FormPanel.load_record_id`  to use 
  :func:`Lino.action_handler` instead of doing it herself.


.. function:: Lino.row_action_handler(actionName, hm, pp)

.. function:: Lino.list_action_handler(ls_url, actionName, hm, pp)

.. function:: Lino.run_row_action(requesting_panel, url, meth, pk, actionName, preprocessor)

.. function:: Lino.put = function(requesting_panel, pk, data)

.. function:: Lino.call_ajax_action(panel, method, url, p, actionName, step, on_confirm, on_success)

.. function:: Lino.action_handler(panel, on_success, on_confirm)

.. function:: Lino.handle_action_result(panel, result, on_success, on_confirm)




Classes
-------

.. class:: Lino.WindowWrapper

  See :blogref:`20100716`
  
  .. function:: Lino.WindowWrapper.load_master_record(record)
  
    Loads the specified record into this window.
  
  .. function:: Lino.WindowWrapper.show()
  
    Display this window.

  
.. class:: Lino.FormPanel

  .. attribute:: Lino.FormPanel.ls_data_url
  
    The base URI of the report.
  
  .. attribute:: Lino.FormPanel.data_record
  
    An object that should have at least these attributes:
    - title
    - values
  
    See :blogref:`20100714`
  
  .. function:: Lino.FormPanel.load_master_record

  .. function:: Lino.FormPanel.save()
  .. function:: Lino.FormPanel.load_record_id(record_id,after)

  
  
    
.. class:: Lino.GridPanel

  .. function:: Lino.GridPanel.load_slavegrid()
  
  .. attribute:: Lino.GridPanel.ls_data_url
  
    The base URI of the report.
  
    See :blogref:`20100714`
  

.. function:: Lino.GridPanel.on_afteredit(e)


.. class:: Lino.ActionFormPanel

  The window that opens when the user invokes an action that has
  parameters.

.. function:: Lino.ActionFormPanel.on_ok()




Defined in site.js
------------------

.. function:: Lino.notes.NoteTypes.grid(params)

  :param object params: Parameters to override default config values.
  :returns: null
   
  See :blogref:`20100706`
   

Names from external libraries
-----------------------------

.. class:: Ext.ux.grid.GridFilters


