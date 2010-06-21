"""

Django raises DoesNotExist when consulting an empty ForeignKey field
Django Ticket#12708 (http://code.djangoproject.com/ticket/12708)

We create an Order without a Journal:
  
  >>> o = Order()
  >>> print o.journal
  None
  >>> o.save()
 
This works only because `Order.journal` has `null=True`.
In fact I want the `save()` method to complain if `journal` is empty,
so I remove `null=True` from the field definition.

  >>> o = Order2()
  >>> print o.journal
  Traceback (most recent call last):  
  ...
  DoesNotExist
  
The above line raises a DoesNotExist exception. Django should raise 
an exception only when I try to save the instance, not already when 
I want to see the value of `journal`!

"""

from django.db import models
   
class Journal(models.Model):
    pass

class Order(models.Model):
    journal = models.ForeignKey(Journal,null=True)

class Order2(models.Model):
    journal = models.ForeignKey(Journal)

