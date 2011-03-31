Lino and Qooxdoo
================

How to use it
-------------

- The :setting:`ROOT_URLCONF` in your :xfile:`settings.py` 
  decides whether your site uses ExtJS or Qooxdoo. 
  You can set it either to
  
  ::

    ROOT_URLCONF = 'lino.ui.qx.urls'
   
  or to
  
  ::
  
    ROOT_URLCONF = 'lino.ui.extjs.urls'
   
- Each time you changed something in your :xfile:`settings.py` 
  you also need to run the :term:`makeui` command.
  (This is currently required only when using Qooxdoo, but 
  we'll probably adapt the ExtJS version, see ticket :doc:`/tickets/35`)

- Now you can invoke :command:`python manage.py runserver` 
  and point your browser to one of the following URIs:
  
  - build : http://127.0.0.1:8000/
  - source : http://127.0.0.1:8000/media/qooxdoo/lino_apps/MYPROJECT/source/index.html
  
- You don't need to restart the web server after makeui, 
  it is enough to reload the browser page.
  
- The source version is very slow because each resource is 
  requested by a GET and served by Django's `django.views.static`.

The :term:`makeui` command
--------------------------

You invoke the :term:`makeui` command by executing 
the following shell command in your local project directory::

  python manage.py makeui
  
This generates a complete Qooxdoo application 
into the :xfile:`lino_apps` directory of your project.

This job consists of two parts:

- writing all the files that make up a Qooxdoo application
  (`config.json`, class files, etc.) 
- runs Qooxdoo's ``generate.py source build`` command .


The :xfile:`lino_apps` directory
--------------------------------

The :xfile:`lino_apps` directory is 
`QOOXDOO_PATH/lino_apps/MYPROJECT`,
where 
- QOOXDOO_PATH is usually something like `/var/snapshots/qooxdoo-1.3-sdk`
- MYPROJECT is the local name you chose for your project
- `lino_apps` is a hard-coded string that is currently not configurable.

It's actually not very polite that Lino writes 
into the source tree of your Qooxdoo SDK.
But we didn't yet find a better solution.
See :doc:`/tickets/30`

