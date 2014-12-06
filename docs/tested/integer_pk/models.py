from django.db import models
from django.utils.translation import ugettext_lazy as _

   
class Person(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class AutoPerson(models.Model):
    id = models.AutoField(primary_key=True, verbose_name=_("ID"))
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class IntegerPerson(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name=_("ID"))
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class CharPerson(models.Model):
    id = models.CharField(_("ID"), primary_key=True, max_length=10)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

