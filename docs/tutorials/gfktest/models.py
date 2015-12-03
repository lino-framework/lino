from django.db import models
from django.contrib.contenttypes.models import ContentType
from lino.api import dd
from lino.core.gfks import GenericForeignKey


class Member(dd.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name


class Comment(dd.Model):
    allow_cascaded_delete = ['owner']
    owner_type = dd.ForeignKey(ContentType)
    owner_id = models.PositiveIntegerField()
    owner = GenericForeignKey('owner_type', 'owner_id')
    
    text = models.CharField(max_length=200)


class Note(dd.Model):
    owner_type = dd.ForeignKey(ContentType)
    owner_id = models.PositiveIntegerField()
    owner = GenericForeignKey('owner_type', 'owner_id')
    
    text = models.CharField(max_length=200)


class Memo(dd.Model):
    owner_type = dd.ForeignKey(ContentType, blank=True, null=True)
    owner_id = models.PositiveIntegerField(blank=True, null=True)
    owner = GenericForeignKey('owner_type', 'owner_id')
    
    text = models.CharField(max_length=200)

