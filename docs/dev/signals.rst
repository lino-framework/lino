.. _lino.signals:

Signals overview
================

Work in progress.
Far from being finished.
Still experimenting with how to organize the docstrings.


database_connected
------------------

Database connection is opened.
The database is not guaranteed to be initialized.

database_ready
--------------


testcase_setup
--------------

:attr:`testcase_setup <djangosite.utils.testcase_setup>`

Fired in :meth:`djangosite.utils.djangotest.TestCase.setUp`,
i.e. at the beginning of each test case.



post_syncdb
-----------



:mod:`lino.ui.models` also defines a handler which will fire 
the `database_connected` signal 
and call the :func:`lino.ui.site.clear_site_config` 
method on each of the following signals:

- testcase_setup
- connection_created
- post_syncdb
