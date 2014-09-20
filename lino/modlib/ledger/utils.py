# -*- coding: UTF-8 -*-
# Copyright 2012-2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""

Defines the :class:`FiscalYears` choicelist.

"""
import datetime

from django.utils.translation import ugettext_lazy as _

#~ from lino.utils.choicelists import Choice,ChoiceList

from lino import dd, rt

from django.conf import settings

#~ class FiscalMonth(dd.Choice):
    #~ pass

#~ class FiscalMonths(dd.ChoiceList):
    #~ item_class = FiscalMonth
    #~ verbose_name = _("Fiscal Month")


class FiscalYear(dd.Choice):
    pass


class FiscalYears(dd.ChoiceList):

    """If the fiscal year of your company is the same as the calendar
    year, then the default entries in this should do.  Otherwise you
    can always override this in your
    :meth:`ad.Site.setup_choicelists`.

    """
    item_class = FiscalYear
    verbose_name = _("Fiscal Year")
    verbose_name_plural = _("Fiscal Years")
    # ~ preferred_width = 4 # would be 2 otherwise

    @classmethod
    def from_int(cls, year):
        return cls.get_by_value(str(year)[2:])

    @classmethod
    def from_date(cls, date):
        return cls.from_int(date.year)

for y in range(settings.SITE.start_year, settings.SITE.today().year + 5):
    s = str(y)
    FiscalYears.add_item(s[2:], s)


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
