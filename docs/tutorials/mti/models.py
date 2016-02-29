from __future__ import unicode_literals
from django.db import models
from lino.mixins.polymorphic import Polymorphic
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Person(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Place(Polymorphic):
    name = models.CharField(max_length=50)
    owners = models.ManyToManyField(Person)

    def __str__(self):
        return "#%s (name=%s, owners=%s)" % (
            self.pk, self.name,
            ', '.join([unicode(o) for o in self.owners.all()]))


@python_2_unicode_compatible
class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    cooks = models.ManyToManyField(Person)

    def __str__(self):
        return "#%d (name=%s, owners=%s, cooks=%s)" % (
            self.pk, self.name,
            ', '.join([unicode(o) for o in self.owners.all()]),
            ', '.join([unicode(o) for o in self.cooks.all()]))


@python_2_unicode_compatible
class Visit(models.Model):
    allow_cascaded_delete = ['place']
    person = models.ForeignKey(Person)
    place = models.ForeignKey(Place)
    purpose = models.CharField(max_length=50)

    def __str__(self):
        return "%s visit by %s at %s" % (
            self.purpose, self.person, self.place.name)


@python_2_unicode_compatible
class Meal(models.Model):
    allow_cascaded_delete = ['restaurant']
    person = models.ForeignKey(Person)
    restaurant = models.ForeignKey(Restaurant)
    what = models.CharField(max_length=50)

    def __str__(self):
        return "%s eats %s at %s" % (
            self.person, self.what, self.restaurant.name)


from .tables import *
