.. _ui.renderer:

========================================
Introduction to User Interface Renderers
========================================

One of Lino's design goals is to make your applications user interface
agnostic, i.e. independent of the choice of a user interface.  

Our plan is that one day local system admins can opt to simply replace
:mod:`lino.modlib.extjs` by another user interface (e.g. one with a
less restrictive license).  For example :ref:`belref`
(:mod:`lino.projects.belref`) is a Lino application which runs
entirely on :mod:`lino.modlib.bootstrap3` and without ExtJS. The
drawback of that application is that it is just a proof of concept.
You cannot change any data because the bootstrap ui is read-only.  So
the road is prepared, but we did not yet reach our goal, mostly
because until now everybody is happy with ExtJS.

An important side-effect of our plan is that Lino has (already now)
another "user interface" which writes everything as text formatted in
reStructuredText syntax. This is interface is heavily used for writing
technical specifications that are being automatically tested using
doctest.

A user interface is a special plugin which has its "renderer"
(i.e. :attr:`renderer <lino.core.plugin.Plugin.renderer>` attribute
not `None`).

The default user interface is specified in 
:attr:`lino.core.site.Site.default_ui`.

Lino currently has three "User Interface Renderers" (not to be
confused with e.g. the appy renderer):

- The renderer used by :mod:`lino.modlib.bootstrap3` is defined in
  :class:`lino.modlib.bootstrap3.renderer.HtmlRenderer` and can be
  accessed via ``settings.SITE.plugins.bootstrap3.renderer``.

- The renderer used by :mod:`lino.modlib.extjs` is defined in :class:`lino.modlib.extjs.ext_renderer.ExtRenderer` and can be accessed via
  ``settings.SITE.plugins.extjs.renderer``.

Besides these two pluggable renderers Lino has a third one

- :class:`TextRenderer <lino.core.renderer.TextRenderer>`,
  instantiated in :attr:`settings.SITE.kernel.text_renderer
  <lino.core.kernel.Kernel.text_renderer>`.




Some methods:

- :meth:`ar.show <lino.core.requests.BaseRequest.show>` : show the
  specified resource (a table, a request, a database object, ...)
  using the request's renderer.

- :meth:`lino.core.tablerequest.TableRequest.to_rst` : return that
  table request as a reStructuredText string.

- :meth:`lino.core.tablerequest.TableRequest.table2rst` : shortcut to
  :meth:`text_renderer.show_table
  <lino.core.renderer.TextRenderer.show_table>`.

Internal

- :meth:`lino.core.renderer.HtmlRenderer.show_table`
- :meth:`text_renderer.show_table <lino.core.renderer.TextRenderer.show_table>`
- :meth:`lino.modlib.extjs.ext_renderer.ExtRenderer.show_table`
- :meth:`lino.core.renderer.TextRenderer.show_story`




