"""
Example which I used for post to django-developers:
http://groups.google.com/group/django-developers/browse_thread/thread/89787edc279d74d2?hl=en

>>> a = Animal()
>>> print a.owner
None
>>> a.save() 

>>> t = Thing()
>>> print t.owner_id
None

>>> t.save()
Traceback (most recent call last):
...
IntegrityError: 20100212_thing.owner_id may not be NULL

"""

from django.db import models

class Owner(models.Model):
    pass
    
class Animal(models.Model):  # nullable owner
    owner = models.ForeignKey(Owner,blank=True,null=True)

class Thing(models.Model):   # non-nullable owner
    owner = models.ForeignKey(Owner) 

