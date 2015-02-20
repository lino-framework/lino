# Copyright 2010-2015 Luc Saffre
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

