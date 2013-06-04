.. _cosi.tested:

===================================================
Tested code snippets on the Lino Così demo database
===================================================

General stuff:

>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.cosi.settings.test'
>>> from lino.runtime import *
>>> from django.test import Client
>>> client = Client()
>>> ses = settings.SITE.login('rolf')


Person #115 is not a Partner
----------------------------

Person #115 (u'Altenberg Hans') is not a Partner (master_key 
is <django.db.models.fields.related.ForeignKey: partner>)

>>> url = '/plain/contacts/Person/115'
>>> res = client.get(url,REMOTE_USER='robin')
>>> print res.status_code
200

