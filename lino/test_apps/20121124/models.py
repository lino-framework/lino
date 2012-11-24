"""
Is it allowed to annotate the Sum of a TimeField?
==================================================

Let's create two tickets:

>>> t1 = Ticket(name="Ticket #1")
>>> t1.save()
>>> t2 = Ticket(name="Ticket #2")
>>> t2.save()
>>> print Ticket.objects.all()
[<Ticket: Ticket #1>, <Ticket: Ticket #2>]

and some sessions:

>>> Session(ticket=t1,time="0:45").save()
>>> Session(ticket=t1,time="1:30").save()
>>> print Session.objects.all()
[<Session: at 00:45:00>, <Session: at 01:30:00>]

>>> qs = Ticket.objects.annotate(time=models.Sum('sessions__time'))
>>> print [t.time for t in qs]

"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

    
class Ticket(models.Model):  
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class Session(models.Model):  
    ticket = models.ForeignKey(Ticket,related_name="sessions")
    time = models.TimeField()
    def __unicode__(self):
        return "at %s" % self.time

