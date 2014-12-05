# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines the fields :class:`LanguageField`, :class:`BabelCharField`
and :class:`BabelTextField`, and the model mixin :class:`BabelNamed`.

See usage example in :ref:`mldbc_tutorial`.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

from lino.core.fields import RichTextField

LANGUAGE_CODE_MAX_LENGTH = 5


def contribute_to_class(field, cls, fieldclass, **kw):
    "Used by both :class:`BabelCharField` and :class:`BabelTextField` "
    if cls._meta.abstract:
        return
    kw.update(blank=True)
    for lang in settings.SITE.BABEL_LANGS:
        kw.update(verbose_name=string_concat(
            field.verbose_name, ' (' + lang.django_code + ')'))
        newfield = fieldclass(**kw)
        #~ newfield._lino_babel_field = True
        # used by dbtools.get_data_elems
        newfield._lino_babel_field = field.name
        newfield._babel_language = lang
        cls.add_to_class(field.name + '_' + lang.name, newfield)


class BabelCharField(models.CharField):

    """Define a variable number of `CharField` database fields, one for
    each language of your :attr:`ad.Site.languages`.  See
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
    babel languages.

    """

    def __init__(self, *args, **kw):
        defaults = dict(
            verbose_name=_("Language"),
            choices=iter(settings.SITE.LANGUAGE_CHOICES),
            default=settings.SITE.get_default_language,
            #~ default=get_language,
            max_length=LANGUAGE_CODE_MAX_LENGTH,
        )
        defaults.update(kw)
        models.CharField.__init__(self, *args, **defaults)


