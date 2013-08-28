from lino import ad

#~ def _(s): return s
from django.utils.translation import ugettext_lazy as _

class App(ad.App):
    verbose_name = _("Households")

