======================
Server startup signals
======================

Lino provides a solution for Django's old problem of not 
providing an "application server startup signal", 
a signal to be emitted when the models cache has been populated.

In March 2010, wojteks suggested to call it "server_initialized"
in his :djangoticket:`13024` ("Signal sent on application startup").
This ticket has been closed because it was 
"fixed in a branch which needs review. See #3591."

:djangoticket:`3591` ("add support for custom app_label and verbose_name") 
seems truly very interesting and truly very complex,
but didn't get into 1.5.
Obviously it's not easy to find a good solution.

In `Entry point hook for Django projects
<http://eldarion.com/blog/2013/02/14/entry-point-hook-django-projects/>`__
(2013-02-14), 
Brian Rosner describes a method for "running code when Django starts",
but this is not the same problem, 
it is rather what I describe in :doc:`/admin/lino_local`.
We don't want to run code *when* Django starts, 
but *after* Django has finished to start.
The difference is important if you want to analyze all installed models.

Ross McFarland describes an aproach which simply sends the signal
"at the end of your last app's models.py file":
`Sun 24 June 2012 by Ross McFarland
<http://www.xormedia.com/django-startup-signal/>`_
This is the base for Lino's current solution.

