from django.db import models
from lino.utils.mti import EnableChild
from lino import dd, rt


class Person(dd.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Place(dd.Model):
    name = models.CharField(max_length=50)
    owners = models.ManyToManyField(Person)
    is_restaurant = EnableChild('Restaurant', verbose_name="is a restaurant")

    def __unicode__(self):
        return "#%s (name=%s,owners=%s)" % (
            self.pk, self.name,
            ','.join([unicode(o) for o in self.owners.all()]))


class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    cooks = models.ManyToManyField(Person)

    def __unicode__(self):
        return "#%d (name=%s,owners=%s,cooks=%s)" % (
            self.pk, self.name,
            ','.join([unicode(o) for o in self.owners.all()]),
            ','.join([unicode(o) for o in self.cooks.all()]))


class Visit(dd.Model):
    person = models.ForeignKey(Person)
    place = models.ForeignKey(Place)
    purpose = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s visit by %s at %s" % (
            self.purpose, self.person, self.place.name)


class Meal(dd.Model):
    allow_cascaded_delete = ['restaurant']
    person = models.ForeignKey(Person)
    restaurant = models.ForeignKey(Restaurant)
    what = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s eats %s at %s" % (
            self.person, self.what, self.restaurant.name)
