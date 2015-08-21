from django.db import models


class Owner(models.Model):
    name = models.CharField(max_length=255)


class FoodPlace(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Owner, blank=True, null=True)


class Bar(FoodPlace):
    pass


class Pizzeria(FoodPlace):
    pass


class PizzeriaBar(Bar, Pizzeria):
    pizza_bar_specific_field = models.CharField(max_length=255)
