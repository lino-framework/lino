# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

from django.utils.translation import ugettext_lazy as _

from lino import dd


class AddressType(dd.Choice):
    living_text = _("living at")


class AddressTypes(dd.ChoiceList):
    verbose_name = _("Address type")
    verbose_name_plural = _("Address types")
    item_class = AddressType

add = AddressTypes.add_item
add('01', _("Official address"), 'official')  # IT020
add('02', _("Unverified address"), 'unverified')  # IT042
add('03', _("Declared address"), 'declared')  # IT214
add('04', _("Reference address"), 'reference')


class DataSources(dd.ChoiceList):
    verbose_name = _("Data source")
    verbose_name_plural = _("Data sources")

add = DataSources.add_item
add('01', _("Manually entered"), 'manually')
add('02', _("Read from eID"), 'eid')


