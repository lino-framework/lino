# -*- coding: UTF-8 -*-
# Copyright 2010-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
"""

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _

from lino import dd


class Shortcut(dd.Choice):
    model_spec = None

    def __init__(self, model_spec, name, verbose_name):
        self.model_spec = model_spec
        value = model_spec + "." + name
        super(Shortcut, self).__init__(value, verbose_name, name)


class Shortcuts(dd.ChoiceList):
    """Choices are added e.g. in
:mod:`lino_welfare.modlib.pcsw.models`."""
    verbose_name = _("Upload shortcut")
    verbose_name_plural = _("Upload shortcuts")
    item_class = Shortcut
    max_length = 50  # fields get created before the values are known


class UploadAreas(dd.ChoiceList):
    verbose_name = _("Upload Area")
    verbose_name_plural = _("Upload Areas")
add = UploadAreas.add_item
add('90', _("Uploads"), 'general')


