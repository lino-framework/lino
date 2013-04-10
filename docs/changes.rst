.. _lino.changes: 

===============
Changes in Lino
===============

See the author's :ref:`Developer Blog <blog>`
to get detailed news.
The final truth about what's going on is only 
`The Source Code <http://code.google.com/p/lino/source/list>`_.


Version 1.6.5 (in development)
==============================

- Exceptions "Using remote authentication, but no user credentials 
  found." and "Unknown or inactive username %r. Please contact your 
  system administrator."
  raised by :class:`lino.utils.auth.RemoteUserMiddleware`
  no longer is a PermissionDenied but a simple Exception.
  See :blogref:`20130409`.

- :class:`lino.core.fields.IncompleteDateField` now has a 
  default `help_text` (adapted from `birth_date` field 
  in :class:`lino.mixins.human.Born`)

- The new method :meth:`lino.core.model.Model.subclasses_graph`
  generates a graphviz directive which shows this model and the 
  submodels.
  the one and only usage example is visible in the 
  `Lino-Welfare user manual
  <http://welfare-user.lino-framework.org/fr/clients.html#partenaire>`_
  See :blogref:`20130401`.


Older releases
==============

.. toctree::
   :maxdepth: 1
   
   /releases/index
