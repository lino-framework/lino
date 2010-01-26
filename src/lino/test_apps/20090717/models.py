"""

Diamond inheritance
===================

To try this test, save the body of this mail as a file models.py together with an empty __init__.py in some new directory on your PYTHONPATH, add this to your INSTALLED_APPS and then run "manage.py test".

This test needs issue #10808 to be solved.
http://code.djangoproject.com/ticket/10808

If you apply patch 10808.diff, then the following code won't fail anymore::

  >>> p = PizzeriaBar(name="Mike's", pizza_bar_specific_field="Doodle")
  >>> p.name == "Mike's"
  True
  >>> p.pizza_bar_specific_field == "Doodle"
  True

But patch 10808.diff fixes only one symptom, not the real problem. 
The real problem is that in case of diamond inheritance there are duplicate field definitions:

  >>> print ' '.join([f.name for f in p._meta.fields])
  id name owner foodplace_ptr id name owner foodplace_ptr pizzeria_ptr bar_ptr pizza_bar_specific_field
  
The first 4 fields occur twice.

My patch won't fix the real problem, but another symptom: when the top-level model of your diamond structure contains a ForeignKey, then you get problems when trying to create inline formsets. This is why I added a "Owner" class to SmileyChris's diamond inheritance test.

  >>> from django.forms.models import inlineformset_factory
  >>> f = inlineformset_factory(Owner,PizzeriaBar)
  Traceback (most recent call last):
    ...
  Exception: <class '...PizzeriaBar'> has more than 1 ForeignKey to <class '....Owner'>
  
The workaround I suggest for this problem is to specify the fk_name explicitly:

  >>> from django.forms.models import inlineformset_factory
  >>> f = inlineformset_factory(Owner,PizzeriaBar,fk_name='owner')
  
Unfortunately this workaround needs another patch because inlineformset_factory() just can't imagine that a model can have two fields with the same name.

The patch 10808b.diff contains 10808.diff + my suggestion.


"""

from django.db import models


#
# Extended Diamond inheritance test
# 

class Owner(models.Model):
    name = models.CharField(max_length=255)
    
class FoodPlace(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Owner,blank=True,null=True)

class Bar(FoodPlace):
    pass

class Pizzeria(FoodPlace):
    pass

class PizzeriaBar(Bar, Pizzeria):
    pizza_bar_specific_field = models.CharField(max_length=255)
