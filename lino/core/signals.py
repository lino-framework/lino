# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
This defines Lino's standard system signals.
"""

from django.dispatch import Signal, receiver

pre_startup = Signal()
post_startup = Signal()
"""
Sent exactly once per process at site startup,
just before any application-specific startup actions.

sender:
  the Site instance
  
"""

testcase_setup = Signal()
"""
Emitted each time `lino.core.utils.TestCase.setUp` is called.
lino.ui.Site uses this signal to reset its SiteConfig cache.
It is necessary because (afaics) the Django test runner doesn't 
send a 'connected' signal when it restores the database to a 
virgin state before running a new test case.
"""

database_ready = Signal()


pre_analyze = Signal(['models_list'])
"""
Sent exactly once per process at site startup, 
just before Lino analyzes the models.

sender: 
  the Site instance
  
models_list:
  list of models 
  
"""

post_analyze = Signal(['models_list'])
"""
Sent exactly once per process at site startup, 
just after Site has finished to analyze the models.
"""


auto_create = Signal(["field", "value"])
"""
The :attr:`auto_create` signal is sent when 
:func:`lookup_or_create <>` silently created a model instance.

Arguments sent with this signal:

``sender``
    The model instance that has been created. 
    
``field``
    The database field 

``known_values``
    The specified known values

"""


pre_merge = Signal(['request'])
"""
Sent when a model instance is being merged into another instance.
"""

pre_remove_child = Signal(['request', 'child'])
pre_add_child = Signal(['request'])
"""
Sent when an EnableChild field has been checked. Arguments to the handler are:
- `sender` : the parent (a database object instance)
- `request` : the HttpRequest which asks to create an MTI child
- `child` : the child model (a class object)
"""

# on_add_child = Signal(['child'])
# """Sent when insert_child has created and saved a new child
# - `sender` : the database object instance which was parent
# - `child` : the new child object
# """

on_ui_created = Signal(['request'])
"""
Sent when a new model instance has been created and saved.
"""


on_ui_updated = Signal(['request'])
"""Sent when a model instance has been modified and saved.  This will
be called each time some database object has been updated.

Unlike Django's `post_save` signal, the `sender` is a
:class:`lino.core.utils.ChangeWatcher` instance, and the HttpRequest
will be passed to the receiver.

"""

pre_ui_delete = Signal(['request'])
"""Sent just before a model instance is being deleted using the user
interface.

``request``:
  The HttpRequest object

"""

pre_ui_build = Signal()
post_ui_build = Signal()

database_connected = Signal()

#~ database_ready = Signal()



