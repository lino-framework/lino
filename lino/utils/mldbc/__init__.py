"""

Generic support for :ref:`mldbc`.

This includes definition of *babel fields* in your Django Models as
well as methods to access these fields.

Babel fields are fields defined using :class:`BabelCharField` or
:class:`BabelTextField`.

Each babel field generates a series of normal CharFields (or
TextFields) depending on your :setting:`languages` setting.

Example::

  class Foo(models.Model):
      name = BabelCharField(_("Foo"), max_length=200)
      

Multilingual database content:

- :class:`BabelNamed <lino.utils.mldbc.mixins.BabelNamed>`
- :class:`BabelCharField <lino.utils.mldbc.fields.BabelCharField>`
- :class:`BabelTextField <lino.utils.mldbc.BabelTextField>`
- :class:`LanguageField <lino.utils.mldbc.fields.LanguageField>`
- :meth:`babelkw <ad.Site.babelkw>`
- :meth:`babelattr <ad.Site.babelattr>`


"""

