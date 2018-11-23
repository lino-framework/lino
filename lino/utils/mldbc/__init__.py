# Copyright 2010-2015 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Generic support for :ref:`mldbc`.

See usage example in :ref:`mldbc_tutorial`.

This includes definition of *babel fields* in your Django Models as
well as methods to access these fields.

Multilingual database content:

- :class:`BabelNamed <lino.utils.mldbc.mixins.BabelNamed>`
- :class:`BabelCharField <lino.utils.mldbc.fields.BabelCharField>`
- :class:`BabelTextField <lino.utils.mldbc.BabelTextField>`
- :class:`LanguageField <lino.utils.mldbc.fields.LanguageField>`
- :meth:`babelkw <ad.Site.babelkw>`
- :meth:`babelattr <ad.Site.babelattr>`


.. autosummary::
   :toctree:

    fields
    mixins

"""

from django.conf import settings

def babel_named(model, name, **kwargs):
    """Instantiate the given subclass of BabelNamed"""
    kwargs = settings.SITE.str2kw('name', name, **kwargs)
    return model(**kwargs)


def babeld(model, desig, **kwargs):
    """Instantiate the given subclass of BabelDesignated"""
    kwargs = settings.SITE.str2kw('designation', desig, **kwargs)
    return model(**kwargs)


