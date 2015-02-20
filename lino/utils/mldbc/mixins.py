# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines the model mixin :class:`BabelNamed`.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.conf import settings

from django.utils.translation import ugettext_lazy as _

from lino.core import model

from .fields import BabelCharField


class BabelNamed(model.Model):

    """Mixin for models that have a babel field `name` (labelled
    "Description" by default) for each language.
    
    """

    class Meta:
        abstract = True

    name = BabelCharField(max_length=200, verbose_name=_("Designation"))

    def __unicode__(self):
        return settings.SITE.babelattr(self, 'name')


