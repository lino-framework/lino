# -*- coding: UTF-8 -*-
# Copyright 2012-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Defines the babel field classes (:class:`BabelCharField` and
:class:`BabelTextField`) and the :class:`LanguageField` class.

**Babel fields** are fields which "generate" in the Django model a
series of normal CharFields (or TextFields), one for each
:attr:`lino.core.site.Site.language`.

Example::

  class Foo(models.Model):
      name = BabelCharField(_("Foo"), max_length=200)
      

.. autosummary::

"""

from __future__ import unicode_literals
import six

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.text import format_lazy

from lino.core.fields import RichTextField

LANGUAGE_CODE_MAX_LENGTH = 5


def contribute_to_class(field, cls, fieldclass, **kw):
    "Used by both :class:`BabelCharField` and :class:`BabelTextField` "
    if cls._meta.abstract:
        return
    kw.update(blank=True)
    if "__fake__" in repr(cls):
        # Used to test if we're creating a migration, in that case we don't want to add new fields,
        # As they're already detected during site startup.
        return
    for lang in settings.SITE.BABEL_LANGS:
        kw.update(verbose_name=format_lazy(u"{}{}",
            field.verbose_name, ' (' + lang.django_code + ')'))
        newfield = fieldclass(**kw)
        #~ newfield._lino_babel_field = True
        # used by dbtools.get_data_elems
        newfield._lino_babel_field = field.name
        newfield._babel_language = lang
        cls.add_to_class(six.text_type(field.name + '_' + lang.name), newfield)
        # we must convert the field name to six.text_type because lang.name is a newstr, and Django can raise a
        # TypeError: unorderable types: str() and <type 'str'>
        # when a model contains both Babelfields and fields with plain Py2 str names.


class BabelCharField(models.CharField):

    """Define a variable number of `CharField` database fields, one for
    each language of your :attr:`lino.core.site.Site.languages`.  See
    :ref:`mldbc`.

    """

    def contribute_to_class(self, cls, name):
        super(BabelCharField, self).contribute_to_class(cls, name)
        contribute_to_class(self, cls, models.CharField,
                            max_length=self.max_length)


class BabelTextField(RichTextField):

    """
    Define a variable number of clones of the "master" field,
    one for each language .
    See :ref:`mldbc`.
    """

    def contribute_to_class(self, cls, name):
        super(BabelTextField, self).contribute_to_class(cls, name)
        contribute_to_class(self, cls, RichTextField,
                            format=self.textfield_format)


class LanguageField(models.CharField):
    """A field that lets the user select a language from the available
    :attr:`lino.core.site.Site.languages`.

    See also :meth:`lino.core.model.Model.get_print_language`.

    """

    def __init__(self, *args, **kw):
        defaults = dict(
            verbose_name=_("Language"),
            # choices=list(settings.SITE.LANGUAGE_CHOICES),
            choices=settings.SITE.LANGUAGE_CHOICES,
            blank=True,
            # default=settings.SITE.get_default_language,
            #~ default=get_language,
            max_length=LANGUAGE_CODE_MAX_LENGTH,
        )
        defaults.update(kw)
        models.CharField.__init__(self, *args, **defaults)


