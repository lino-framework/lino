"""
>>> luc = Contact(first_name="Luc",last_name="Saffre")
>>> luc.save()
>>> luc
<Contact: Luc Saffre>

"""

from django.db import models

class Contact(models.Model):
  
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.first_name + " " + self.last_name
