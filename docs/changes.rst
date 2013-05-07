.. _lino.changes: 

===============
Changes in Lino
===============

See the author's :ref:`Developer Blog <blog>`
to get detailed news.
The final truth about what's going on is only 
`The Source Code <http://code.google.com/p/lino/source/list>`_.


Version 1.6.7 (in development)
============================================

- Optimization: 
  virtual fields to a foreignkey 
  (e.g. the new `bailiff` field in :ref:`welfare.debts.PrintLiabilitiesByBudget`)
  might cause a "unicode object has no attribute '_meta'" traceback.

  

Version 1.6.6 (released :blogref:`20130505`)
============================================

- :mod:`lino.utils.html2odf` now converts the text formats `<i>` 
  and `<em>` to a style "Emphasis".
  `<b>` is no longer converted to "Bold Text" but 
  to "Strong Emphasis".

- Lino now supports 
  :class:`lino.core.fields.RemoteField` to a 
  :class:`lino.core.fields.VirtualField`.
  See :blogref:`20130422`

- :mod:`lino.utils.auth` forgot to set `request.subst_user` to `None`
  for html HEAD requests.
  (:blogref:`20130423`)
  
- Readable user message when contract type empty
  (:blogref:`20130423`)

Version 1.6.5 (released :blogref:`20130422`)
============================================

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
