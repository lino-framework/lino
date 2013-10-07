.. _cosi.tested:

===================================================
Tested code snippets on the Lino Così demo database
===================================================

General stuff:

>>> import os
>>> import json
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.cosi.settings.test'
>>> from lino.runtime import *
>>> from django.test import Client
>>> client = Client()
>>> ses = settings.SITE.login('rolf')
>>> from __future__ import print_function


Person #115 is not a Partner
----------------------------

Person #115 (u'Altenberg Hans') is not a Partner (master_key 
is <django.db.models.fields.related.ForeignKey: partner>)

>>> url = '/plain/contacts/Person/115'
>>> res = client.get(url,REMOTE_USER='robin')
>>> print(res.status_code)
200


Slave tables with more than 15 rows
-----------------------------------

When you look at the detail window of Belgium in `Lino Così
<http://demo4.lino-framework.org/api/countries/Countries/BE?an=detail>`_
then you see a list of all places in Belgium.
This demo database contains exactly 40 entries:

>>> be = countries.Country.objects.get(isocode="BE")
>>> be.city_set.count()
45

>>> countries.CitiesByCountry.request(be).get_total_count()
45

>>> url = '/api/countries/CitiesByCountry?fmt=json&start=0&mt=10&mk=BE'
>>> res = client.get(url,REMOTE_USER='robin')
>>> print(res.status_code)
200
>>> result = json.loads(res.content)
>>> print(len(result['rows']))
16

The 16 is because Lino has a hard-coded default value of  
returning only 15 rows when no limit has been specified
(there is one extra row for adding new records).

In versions after :blogref:`20130903` you can change that limit 
for a given table by overriding the 
:attr:`preview_limit <lino.core.tables.AbstractTable.preview_limit>`
parameter of your table definition.
Or you can change it globally for all your tables 
by setting the 
:attr:`preview_limit <lino.site.Site.preview_limit>`
Site attribute to either `None` or some bigger value.

This parameter existed before but wasn't tested.
In your code this would simply look like this::

  class CitiesByCountry(Cities):
      preview_limit = 30

Here we override it on the living object:

>>> countries.CitiesByCountry.preview_limit = 25

Same request returns now 26 data rows:

>>> res = client.get(url,REMOTE_USER='robin')
>>> result = json.loads(res.content)
>>> print(len(result['rows']))
26

To remove the limit altogether, you can say:

>>> countries.CitiesByCountry.preview_limit = None

Same request returns now all 45 data rows (44 + the phantom row):

>>> res = client.get(url,REMOTE_USER='robin')
>>> result = json.loads(res.content)
>>> print(len(result['rows']))
46


