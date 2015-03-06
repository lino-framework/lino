.. _startup:

=================================
When a Lino application starts up
=================================

There are three phases in the lifecycle of a Lino process:

- while Django settings are being loaded (:mod:`lino.api.ad`)
- while Django models are being loaded (:mod:`lino.api.dd`)
- normal runtime (:mod:`lino.api.rt`)


A server startup signal for Django
==================================

This section is for Django before 1.7.

Lino provides a solution for Django's old problem of not having an
"application server startup signal", a signal to be emitted when the
models cache has been populated.

About the problem
-----------------

The problem is old:

- In March 2010, wojteks suggested to call it "server_initialized"
  in his :djangoticket:`13024` ("Signal sent on application startup").
  This ticket has been closed because it was 
  "fixed in a branch which needs review. See #3591."

- :djangoticket:`3591` ("add support for custom app_label and verbose_name") 
  seems truly very interesting and truly very complex,
  but didn't get into 1.5.
  Obviously it's not easy to find a good solution.

Note that this is *not* the same problem as
in `Entry point hook for Django projects
<http://eldarion.com/blog/2013/02/14/entry-point-hook-django-projects/>`__
(2013-02-14) where 
Brian Rosner 
describes a method for "running code when Django starts".
We don't want to run code *when* Django starts, 
but *after* Django has finished to start.
The difference is important e.g. if you want to analyze all installed models.


How Lino solves it
------------------

The basic trick is to simply send the signal "at the end of your last
app's models.py file" as described by `Ross McFarland on Sun 24 June
2012 <http://www.xormedia.com/django-startup-signal/>`_.

That's why :mod:`lino`  must be the *last* item of your
:setting:`INSTALLED_APPS`.

.. currentmodule:: lino.core.site

Although :mod:`lino` doesn't have any model of its own, it
does have a `models` module which invokes
the :meth:`startup <Site.startup>` method.
The :meth:`startup <Site.startup>` method
then emits a :attr:`startup <djangosite.signals.startup>`
signal.

Result is that you can now write code like the following in any
`models` or `admin` module of your existing project::

  from djangosite.signals import startup, receiver
  
  @receiver(startup)
  def my_handler(sender,**kw):
      # code to run exactly once per process at startup
      print sender.welcome_text()
        
