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

import collections
LanguageInfo = collections.namedtuple(
    'LanguageInfo', ('django_code', 'name', 'index', 'suffix'))


def to_locale(language):
    """Simplified copy of `django.utils.translation.to_locale`, but we
    need it while the `settings` module is being loaded, i.e. we
    cannot yet import django.utils.translation.  Also we don't need
    the to_lower argument.

    """
    p = language.find('-')
    if p >= 0:
        # Get correct locale for sr-latn
        if len(language[p + 1:]) > 2:
            return language[:p].lower() + '_' \
                + language[p + 1].upper() + language[p + 2:].lower()
        return language[:p].lower() + '_' + language[p + 1:].upper()
    else:
        return language.lower()


