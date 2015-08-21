from django.db import models

# import lino.core.inject


class Addressable(models.Model):
    class Meta:
        abstract = True

    a = models.CharField(max_length=255)


class AbstractPartner(Addressable):
    class Meta:
        abstract = True

    b = models.CharField(max_length=255)
    

class AbstractPerson(AbstractPartner):
    class Meta:
        abstract = True

    c = models.CharField(max_length=255)
    

class Partner(AbstractPartner):

    d = models.CharField(max_length=255)
    

class Person(Partner, AbstractPerson):

    e = models.CharField(max_length=255)


