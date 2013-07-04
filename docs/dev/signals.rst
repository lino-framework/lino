.. _lino.signals:

Signals overview
================

Startup signals:

- :attr:`post_syncdb <django.signals.post_syncdb>`
- :attr:`pre_analyze <lino.core.signals.pre_analyze>`
- :attr:`post_analyze <lino.core.signals.post_analyze>`
- :attr:`pre_startup <djangosite.signals.pre_startup>`
- :attr:`post_startup <djangosite.signals.post_startup>`

- :attr:`database_connected <lino.core.signals.database_connected>`
  Database connection is opened.
  The database is not guaranteed to be initialized.
  
- :attr:`database_ready <djangosite.signals.database_ready>`:
  Fired when database initialized and all fixtures have been loaded.

- :attr:`pre_ui_build <lino.core.signals.pre_ui_build>`
- :attr:`post_ui_build <lino.core.signals.post_ui_build>`

Test-specific signals:  

- :attr:`testcase_setup <djangosite.signals.testcase_setup>`
  Fired in :meth:`djangosite.utils.djangotest.TestCase.setUp`,
  i.e. at the beginning of each test case.
  
Runtime signals:
  
- :attr:`auto_create <lino.core.signals.auto_create>`
- :attr:`pre_add_child <lino.core.signals.pre_add_child>`
- :attr:`pre_remove_child <lino.core.signals.pre_remove_child>`
- :attr:`pre_merge <lino.core.signals.pre_merge>`
- :attr:`pre_ui_create <lino.core.signals.pre_ui_create>`
- :attr:`pre_ui_update <lino.core.signals.pre_ui_update>`
- :attr:`pre_ui_delete <lino.core.signals.pre_ui_delete>`


Utilities:

- :attr:`ChangeWatcher <lino.core.signals.ChangeWatcher>`
- :attr:`receiver <django.dispatch.receiver>` : the standard Django receiver decorator





:mod:`lino.ui.models` also defines a handler which will fire 
the `database_connected` signal 
and call the :func:`lino.ui.site.clear_site_config` 
method on each of the following signals:

- testcase_setup
- connection_created
- post_syncdb
