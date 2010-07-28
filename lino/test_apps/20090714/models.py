"""
(Note: this test is useless since this is being tested in the django trunk.)

This test verifies whether issue #10808 "Multiple inheritance (model-based) broken for __init__ of common fields in diamond inheritance" has been solved. http://code.djangoproject.com/ticket/10808

To try this test, save the body of this mail as a file models.py together with an empty __init__.py in some new directory on your PYTHONPATH, add this to your INSTALLED_APPS and then run "manage.py test".

Here is the test code::

  >>> i1 = D(a='D')
  >>> i1.a
  'D'

  >>> i2 = E(a='E')
  >>> i2.a
  'E'
  
If the above code fails like this::

  Failed example:
      i2.a
  Expected:
      'E'
  Got:
      ''      

then you don't have the bug fixed. You can apply the patch
by savig the file 10808.diff into you Django working copy and issuing::

  patch -p0 10808.diff
  
Which should output::

  patching file django/db/models/base.py                    
  patching file tests/modeltests/model_inheritance/models.py

"""

from django.db import models

class A(models.Model):
    a = models.CharField(max_length=100)
    class Meta:
        abstract = True

class B(A): 
    b = models.CharField(max_length=100)
class C(A):
    c = models.CharField(max_length=100)
  
class D(B): 
    dd = models.CharField(max_length=100)
class E(B,C): 
    ee = models.CharField(max_length=100)


