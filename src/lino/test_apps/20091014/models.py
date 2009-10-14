"""

It is okay to assign integer values to DecimalFields::

  >>> a = A(price=10,qty=2)
  >>> a.total()
  20.00
  >>> a.save()

Don't assign float values to a DecimalField because 
although Django doesn't complain, and although the 
values get stored in the instance object, you'll get 
a TypeError when you try to save the object::

  >>> a = A(price=2.50,qty=8.0)
  >>> a.total()
  20.00
  >>> a.save()
Exception raised:
    Traceback (most recent call last):
    ...
    TypeError: Cannot convert float to Decimal.  First convert the float to a string  
    
To assign non-integer values to a DecimalField, you 
should convert the value to a string first::

  >>> a = A(price='2.50',qty='8')
  >>> a.total()
  20.00
  >>> a.save()
  
Even this works::

  >>> a = A(price='',qty='')
  >>> a.total()
  0.00
  >>> a.save()
  

  >>> b = B(price=10,qty=2)
  >>> b.total()
  20.00
  >>> b.save()


  >>> b = B(price='2.50',qty='8')
  >>> b.total()
  20.00
  >>> b.save()
  

"""

from django.db import models

class A(models.Model):
    price = models.DecimalField(max_digits=10,decimal_places=2)
    qty = models.DecimalField(max_digits=5,decimal_places=2)
    
    def total(self):
        return self.price * self.qty


class PriceField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        defaults = dict(
            max_length=10,
            max_digits=10,
            decimal_places=2,
            )
        defaults.update(kwargs)
        super(PriceField, self).__init__(*args, **defaults)
        
class QuantityField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        defaults = dict(
            max_length=5,
            max_digits=5,
            decimal_places=0,
            )
        defaults.update(kwargs)
        super(QuantityField, self).__init__(*args, **defaults)
        
        
class B(models.Model):
    price = PriceField()
    qty = QuantityField()
    
    def total(self):
        return self.price * self.qty

