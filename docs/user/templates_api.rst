=====================
Template designer API
=====================

TODO: This is just a start and far from being complete...


Global names:

:iif: :func:`iif <atelier.utils.iif>`
:tr: :func:`tr <lino.utils.iif>`
:_: gettext
:E: HTML tag generator, see :mod:`lino.utils.xmlgen.html`
:unicode: the builtin Python :func:`unicode` function
:len: the builtin Python :func:`len` function

:settings:  The Django :xfile:`settings.py` module

:site: shortcut for `settings.SITE`
:dtos: :func:`north.dbutils.dtos`
:dtosl: :func:`north.dbutils.dtosl`



Available in :xfile:`admin_main.html`
(rendered by :meth:`get_main_html <lino.ui.Site.get_main_html>`,
which calls :func:`lino.core.web.render_from_request`):

:request: the Django HttpRequest instance
:ar: a Lino :class:`lino.core.requests.BaseRequest` instance





