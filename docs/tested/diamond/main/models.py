from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255)


class Bar(Restaurant):
    min_age = models.IntegerField()


class Pizzeria(Restaurant):
    specialty = models.CharField(max_length=255)


class PizzeriaBar(Bar, Pizzeria):
    pizza_bar_specific_field = models.CharField(max_length=255)
