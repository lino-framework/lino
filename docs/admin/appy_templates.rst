.. _lino.admin.appy_templates:

========================
Appy POD template syntax
========================

When a printable document is being generated using the
:class:`AppyBuildMethod <lino.modlib.printing.choicelists.AppyBuildMethod>` build method, 
Lino uses `appy.pod <http://appyframework.org/pod.html>`__
a library 


uses a special approach:
  the templates are themselves `.odt` files.
  See :doc:`appy_templates`

  it marks template commands 
  using OOo's "change records" and "comments" features. 
  Appy/Pod also handles transparently 
  the fact that .odt files are in fact .zip files containing a set of .xml files.

Weblinks
========

.. glossary::

  appy_pod
    http://appyframework.org/pod.html


.. currentmodule:: lino.utils.appy_pod


installs additional
functions to be used in `do text|section|table from
<http://appyframework.org/podWritingAdvancedTemplates.html>`__
statements.

.. function:: jinja(template_name)

  Render the template named `template_name` using Jinja.
  I `template_name` contains no dot, then the default filename
  extension `.body.html` is added.
  The template is supposed to contain HTML.

- `restify(s)`:
  Render a string `s` which contains reStructuredText markup.
  The string is first passed to
  :func:`lino.utils.restify.restify` to convert it to XHTML,
  then to `appy.pod`'s built in `xhtml` function.
  Without this, users would have to write each time something like::

    do text
    from xhtml(restify(self.body).encode('utf-8'))

- `html(s)` :
  Render a string that is in HTML (not XHTML).

- `ehtml(e)` :
  Render an ElementTree HTML object
  (generated using :mod:`lino.utils.xmlgen.html`)
  by passing it to :mod:`lino.utils.html2odf`.

- `table(ar, column_names=None)` : render an
  :class:`lino.core.tables.TableRequest` as a table. Example::

    do text
    from table(ar.spawn('users.UsersOverview'))


