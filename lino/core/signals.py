# Copyright 2013-2015 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""This defines Lino's standard system signals.

.. data:: pre_startup
.. data:: post_startup

    Sent exactly once per process at site startup,
    just before any application-specific startup actions.

    - `sender`:  the Site instance

.. data:: pre_analyze

    Sent exactly once per process at site startup, just before Lino
    analyzes the models.

    - `sender`      the Site instance
    - `models_list` list of models


.. data:: post_analyze

    Sent exactly once per process at site startup, just after Site has
    finished to analyze the models.


.. data:: database_connected

    No longer used.

.. data:: testcase_setup

    Emitted each time `lino.core.utils.TestCase.setUp` is called.
    Lino uses this signal to reset its SiteConfig cache.
    
    It is necessary because (afaics) the Django test runner doesn't
    send a 'connected' signal when it restores the database to a
    virgin state before running a new test case.


.. data:: on_ui_created

    Sent when a new model instance has been created and saved.

.. data:: pre_ui_delete

    Sent just before a model instance is being deleted using the user
    interface.

    - `request`: The HttpRequest object



.. data:: pre_ui_save

    Sent before a database object gets saved using the web user
    interface.
    
    - `sender`   the database model
    - `instance` the database object which is going to be saved.
    - `ar` the action request

.. data:: on_ui_updated

    Sent when a database model instance has been modified and saved
    using the web interface.

    A receiver of this signal gets the following keyword parameters:

    :sender: the database model of the instance which has been updated

    :watcher: the :class:`ChangeWatcher
              <lino.core.utils.ChangeWatcher>` object (which contains
              the model instance and information about the changes)

    :request: the BaseRequest object
    
.. data:: pre_merge
    
    Sent when a model instance is being merged into another instance.
    
.. data:: auto_create
    
    The :attr:`auto_create` signal is sent when
    :func:`lookup_or_create <>` silently created a model instance.

    Arguments sent with this signal:

    - ``sender`` : The model instance that has been created.
    - ``field`` : The database field
    - ``known_values`` : The specified known values
    
.. data:: pre_remove_child
.. data:: pre_add_child
    
    Sent when an MTI child has been added. Arguments to the handler are:
    
    - `sender` : the parent (a database object instance)
    - `request` : the HttpRequest which asks to create an MTI child
    - `child` : the child model (a class object)

"""

from django.dispatch import Signal, receiver

pre_startup = Signal()
post_startup = Signal()
testcase_setup = Signal()
pre_analyze = Signal(['models_list'])
post_analyze = Signal(['models_list'])
auto_create = Signal(["field", "value"])
pre_merge = Signal(['request'])
pre_remove_child = Signal(['request', 'child'])
pre_add_child = Signal(['request'])
on_ui_created = Signal(['request'])
on_ui_updated = Signal(['request', 'watcher'])
pre_ui_save = Signal(['instance', 'ar'])
pre_ui_delete = Signal(['request'])
pre_ui_build = Signal()
post_ui_build = Signal()
# database_connected = Signal()

