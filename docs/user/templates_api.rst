=====================
Template designer API
=====================

TODO: This is just a start and far from being complete...


Global names:

:iif: :func:`iif <lino.utils.iif>`
:tr: :func:`tr <lino.utils.iif>`
:_: gettext
:E: refers to :func:`lino.utils.xmlgen.html.E`
:unicode: the builtin Python :func:`unicode` function
:len: the builtin Python :func:`len` function

:settings:  The Django settings module
:site: shortcut for `settings.SITE`
:dtos: :func:`north.dbutils.dtos`
:dtosl: :func:`north.dbutils.dtosl`



Available in :xfile:`admin_main.html`
(rendered by :meth:`get_main_html <lino.ui.Site.get_main_html>`,
which calls :func:`lino.core.web.render_from_request`):

:request: the Django HttpRequest instance
:ar: a Lino :class:`lino.core.requests.BaseRequest` instance





