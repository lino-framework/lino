# -*- coding: UTF-8 -*-
# Copyright 2012-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines the model mixin :class:`BabelNamed`.

"""

from __future__ import unicode_literals
from builtins import object

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from lino.core import model

from .fields import BabelCharField


@python_2_unicode_compatible
class BabelNamed(model.Model):

    """Mixin for models that have a babel field `name` (labelled
    "Description" by default) for each language.
    
    """

    class Meta(object):
        abstract = True

    name = BabelCharField(max_length=200, verbose_name=_("Designation"))

    def __str__(self):
        return settings.SITE.babelattr(self, 'name')


