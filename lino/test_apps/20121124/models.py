"""
Is it allowed to annotate the Sum of a TimeField?
==================================================

Answer: Not under sqlite. See :djangoticket:`19360`.


Let's create two tickets:

>>> t1 = Ticket(name="Ticket #1")
>>> t1.save()
>>> t2 = Ticket(name="Ticket #2")
>>> t2.save()
>>> print Ticket.objects.all()
[<Ticket: Ticket #1>, <Ticket: Ticket #2>]

and some sessions:

>>> Session(ticket=t1,time="0:45",price="0.75").save()
>>> Session(ticket=t1,time="1:30",price="1.50").save()
>>> print Session.objects.all()
[<Session: at 00:45:00>, <Session: at 01:30:00>]

Get the sum of the prices of all sessions for each ticket:

>>> qs = Ticket.objects.annotate(pricesum=models.Sum('sessions__price'))
>>> print [t.pricesum for t in qs]
[Decimal('2.25'), None]


Now the same with a timefield:

>>> qs = Ticket.objects.annotate(timesum=models.Sum('sessions__time'))
>>> print [unicode(t.timesum) for t in qs]
['02:15:00','']

The above example raises the following Exeption::

  Traceback (most recent call last):
    File "l:\snapshots\Django-1.4.2\django\test\_doctest.py", line 1235, in __run
      compileflags, 1) in test.globs
    File "<doctest lino.test_apps.20121124.models[10]>", line 1, in <module>
      print [unicode(t.timesum) for t in qs]
    File "l:\snapshots\Django-1.4.2\django\db\models\query.py", line 118, in _result_iter
      self._fill_cache()
    File "l:\snapshots\Django-1.4.2\django\db\models\query.py", line 892, in _fill_cache
      self._result_cache.append(self._iter.next())
    File "l:\snapshots\Django-1.4.2\django\db\models\query.py", line 291, in iterator
      for row in compiler.results_iter():
    File "l:\snapshots\Django-1.4.2\django\db\models\sql\compiler.py", line 790, in results_iter
      ]) + tuple(row[aggregate_end:])
    File "l:\snapshots\Django-1.4.2\django\db\models\sql\query.py", line 338, in resolve_aggregate
      return self.convert_values(value, aggregate.field, connection)
    File "l:\snapshots\Django-1.4.2\django\db\models\sql\query.py", line 316, in convert_values
      return connection.ops.convert_values(value, field)
    File "l:\snapshots\Django-1.4.2\django\db\backends\sqlite3\base.py", line 208, in convert_values
      return parse_time(value)
    File "l:\snapshots\Django-1.4.2\django\utils\dateparse.py", line 51, in parse_time
      match = time_re.match(value)
  TypeError: expected string or buffer

The same exception comes when I use Django development trunk revision 17942.


- `Value conversions of aggregate return values -- is float conversion really required? 
  <https://groups.google.com/forum/?fromgroups=#!topic/django-developers/6HQlh2t1j4M>`_

"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Ticket(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


@dd.python_2_unicode_compatible
class Session(models.Model):
    ticket = models.ForeignKey(Ticket, related_name="sessions")
    time = models.TimeField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return "at %s" % self.time
