===============
Generating HTML
===============

Although Lino is made to *avoid* writing HTML, CSS and Javascript,
there are cases where even the most user-interface agnostic framework
must give some API for writing "rich" or "formatted" text.

For example the return value of a :class:`DisplayField
<lino.core.fields.DisplayField>` or a :class:`HtmlBox
<lino.core.fields.HtmlBox>`, or the :meth:`get_slave_summary
<lino.core.actors.Actor.get_slave_summary>` method are places where
the application developer is expected to write "rich text" which
contains formatting, hyperlinks, widgets.

And the most natural and best known API for writing rich text remains
HTML.

In Lino we recommend a pythonic method to generate HTML using the
:mod:`lino.utils.xmlgen.html` module.

