from __future__ import unicode_literals

from django.db import models
from lino.api import dd


@dd.python_2_unicode_compatible
class Person(dd.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


@ddpython_2_unicode_compatible
class Place(dd.Model):
    name = models.CharField(max_length=50)
    owners = models.ManyToManyField(Person, related_name="owned_places")
    ceo = models.ForeignKey(Person, related_name="managed_places")

    def __str__(self):
        if self.get_restaurant():
            if self.get_bar():
                what = "Restaurant & Bar "
            else:
                what = "Restaurant "
        elif self.get_bar():
            what = "Bar "
        else:
            what = ''
        return "%s %s(ceo=%s,owners=%s)" % (
            self.name, what, self.ceo,
            ','.join([unicode(o) for o in self.owners.all()]))

    def get_restaurant(self):
        try:
            return self.restaurant
        except Restaurant.DoesNotExist:
            return None

    def get_bar(self):
        try:
            return self.bar
        except Bar.DoesNotExist:
            return None


@dd.python_2_unicode_compatible
class Bar(dd.Model):
    place = models.OneToOneField(Place)
    serves_alcohol = models.BooleanField(default=True)

    def __str__(self):
        if self.serves_alcohol:
            return self.place.name
        return "%s (no alcohol)" % self.place.name


@dd.python_2_unicode_compatible
class Restaurant(dd.Model):
    place = models.OneToOneField(Place)
    serves_hot_dogs = models.BooleanField(default=False)
    cooks = models.ManyToManyField(Person)

    def __str__(self):
        return "%s (cooks=%s)" % (
            self.place.name,
            ','.join([unicode(o) for o in self.cooks.all()]))
