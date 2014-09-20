from django.db import models
from lino import dd, rt

class Tag(dd.Model):
  
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name
    
