========
Settings
========

Lino and the Django `settings.py` file
--------------------------------------

This section describes Lino-specific entries of the Django :xfile:`settings.py`.

.. setting:: USE_GRIDFILTERS

If True, the generated JavaScript uses the :extjs:`Ext.ux.grid.GridFilters` extension.


.. setting:: USE_FIREBUG

  If True, the generated JavaScript contains instructions that use the FireBug console. 
  This is useful for profiling and debugging, but the client then needs FireBug installed and active.

.. setting:: MEDIA_ROOT

  Used by FileSystemStorage.
  Used by :meth:`lino.ui.extjs.ext_ui.ExtUI.build_site_js` 
  and Printable to determine the location of the cache.


.. setting:: LANGUAGES

  Used by :class:`lino.modlib.fields.LanguageField`.
  See http://docs.djangoproject.com/en/dev/ref/settings/#languages

.. setting:: PROJECT_DIR

  Directory where local configuration files are stored.
  I always set this variable to the absolute path of the :envvar:`DJANGO_SETTINGS_MODULE`.
  Local configuration files are:
  
  - :xfile:`settings.py`, :xfile:`manage.py` and :xfile:`urls.py`
  - :xfile:`lino_settings.py`
  

.. setting:: DATA_DIR

   Directory where local data gets stored. 
   On a Unix production system I suggest to set it to `/usr/local/lino`. 
   The development and demo configurations set it to ``os.path.join(PROJECT_DIR,'data')``.
   
.. setting:: MODEL_DEBUG

  If this is `True`, Lino will write more debugging info about the models and reports.

.. setting:: BYPASS_PERMS

   If this is `True`, Lino won't apply any user permission checks.
   
   
.. setting:: DEBUG

  See :doc:`/blog/2010/0716`
  
.. setting:: USER_INTERFACES
  
   Lino-specific setting. See :doc:`/blog/2010/0624`.
   
   
Environment variables
---------------------

.. envvar:: REMOTE_USER
  
  If :class:`lino.utils.simulate_remote.SimulateRemoteUserMiddleware` is active, this development server 
  will simulate HTTP authentication and set the `REMOTE_USER` meta attribute of every request to this name. 
  Without SimulateRemoteUserMiddleware active, this environment variable is not consulted.
  
  

The `lino_settings.py` file
---------------------------

This contains settings that have no influence on the Django machinery.