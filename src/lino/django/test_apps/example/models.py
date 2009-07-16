"""

Small example for the problem described in ticket #7623
(http://code.djangoproject.com/ticket/7623)

With revision 11066, the following doctest fails::

    Failed example:
        r
    Expected:
        <Restaurant: Demon Dogs>
    Got:
        <Restaurant: >


>>> p1 = Place(name='Demon Dogs')
>>> p1.save()

# Create a Restaurant from this Place. 
>>> r = Restaurant(place=p1, serves_hot_dogs=True)
>>> r.save()
>>> r
<Restaurant: Demon Dogs>

"""

from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Restaurant(Place):
  
    serves_hot_dogs = models.BooleanField()
    
    # the following explicit parent_link should not be necessary according to 
    # http://docs.djangoproject.com/en/dev/topics/db/models/#specifying-the-parent-link-field
    place = models.OneToOneField(Place,parent_link=True)


