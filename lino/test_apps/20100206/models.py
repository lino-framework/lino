"""
Allow empty non-nullable ForeignKey fields until save()
Django Ticket #12801 (http://code.djangoproject.com/ticket/12801)
Follow-up to Django Ticket #12708 (http://code.djangoproject.com/ticket/12708)

When a model has non-nullable fields (that don't have `null=True`), then Django 
still accepts to instantiate objects of that model where these fields are empty.
An exception is raised only when you try to save such an (invalid) instance.

Unfortunately this is not true for ForeignKey fields. 
If you leave a non-nullable ForeignKey field empty, Django behaves strangely: 
your instance is then like a time bomb, causing an exception when you only consult that field.

We create an Order without a Journal:
  
  >>> o = Order()
  >>> print o.date_field
  None
  >>> print o.char_field
  <BLANKLINE>
  >>> print o.int_field
  None
  >>> print o.decimal_field
  None
  
No problem so far. And of course, if you try to save this, you'll get an exception:

  >>> o.save()
  Traceback (most recent call last):
  ...
  IntegrityError: 20100206_order.date_field may not be NULL
 
But ForeignKey fields are different: you get an exception when you only look at them:

  >>> print o.fk_field
  Traceback (most recent call last):  
  ...
  DoesNotExist
  
This behaviour is not sane.
The line `print o.fk_field` should output `None`, like it does for other field types.

"""

from django.db import models
   
class Journal(models.Model):
    pass

class Order(models.Model):
    date_field = models.DateField()
    char_field = models.CharField(max_length=20)
    int_field = models.IntegerField()
    decimal_field = models.IntegerField()
    fk_field = models.ForeignKey(Journal)

