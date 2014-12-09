# Copyright 2013-2014 Luc Saffre
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
pre_ui_create = Signal(['request'])
"""
Sent when a new model instance has been created and saved.
"""
pre_ui_update = Signal(['request'])

pre_ui_delete = Signal(['request'])
"""
Sent just before a model instance is being deleted using 
the user interface.

``request``:
  The HttpRequest object
  
"""

pre_ui_build = Signal()
post_ui_build = Signal()

database_connected = Signal()

#~ database_ready = Signal()



