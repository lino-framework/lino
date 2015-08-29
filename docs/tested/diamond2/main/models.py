from django.db import models


class Addressable(models.Model):
    class Meta:
        abstract = True
    street = models.CharField(max_length=255, blank=True)
        

class Restaurant(Addressable):
    class Meta:
        abstract = True

    name = models.CharField(max_length=255)
    

class Bar(Restaurant):
    class Meta:
        abstract = True

    min_age = models.IntegerField()
    

class Pizzeria(Restaurant):

    specialty = models.CharField(max_length=255)

    
class PizzeriaBar(Bar, Pizzeria):
    pizza_bar_specific_field = models.CharField(max_length=255)

