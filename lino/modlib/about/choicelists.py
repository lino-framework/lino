# Copyright 2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

import six
import pytz

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.core.choicelists import ChoiceList, Choice

class TimeZone(Choice):
    def __init__(self, *args, **kwargs):
        super(TimeZone, self).__init__(*args, **kwargs)
        self.tzinfo = pytz.timezone(six.text_type(self.text))
        
class TimeZones(ChoiceList):
    verbose_name = _("Time zone")
    verbose_name_plural = _("Time zones")
    item_class = TimeZone

add = TimeZones.add_item
add('01', settings.TIME_ZONE or 'UTC', 'default')


