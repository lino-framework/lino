# -*- coding: UTF-8 -*-
# Copyright 2012-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Defines the model mixin :class:`BabelNamed`.

"""

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from lino.core import model

from .fields import BabelCharField



class BabelNamed(model.Model):

    """
    Mixin for models that have a babel field `name` (labelled
    "Designation" by default) for each language.

    This mixin is deprecated (but without any planned expiry date so
    far). For new applications we recommend to use
    :class:`BabelDesignated` instead.
    """

    class Meta(object):
        abstract = True

    name = BabelCharField(max_length=200, verbose_name=_("Designation"))

    def __str__(self):
        return self.get_designation()

    def get_designation(self):
        return settings.SITE.babelattr(self, 'name')



class BabelDesignated(model.Model):

    """
    Mixin for models that have a babel field "Designation" (i.e. one
    designation for each language defined in the site's
    :attr:`languages <lino.core.site.Site.languages>`.

    This is the same as :class:`BabelNamed` but the internal field
    name matches the label.
    """

    class Meta(object):
        abstract = True

    designation = BabelCharField(
        max_length=200, verbose_name=_("Designation"))

    def __str__(self):
        return self.get_designation()

    def get_designation(self):
        return settings.SITE.babelattr(self, 'designation')
