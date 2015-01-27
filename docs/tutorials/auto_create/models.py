from django.db import models
from lino.api import dd, rt

class Tag(dd.Model):
  
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name
    
