# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

from django.utils.translation import ugettext_lazy as _
from lino.api import dd, rt


class DependencyTypes(dd.ChoiceList):
    verbose_name = _("Dependency type")
add = DependencyTypes.add_item
add('10', _("Requires"), 'requires')
add('20', _("Callback"), 'callback')
add('30', _("Duplicate"), 'duplicate')

    
