from django.db import models

from lino.modlib.countries.mixins import AddressLocation


class Company(AddressLocation):
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    name = models.CharField("Name", max_length=50)

    def __unicode__(self):
        return self.name


from .ui import *
