# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals


import logging
logger = logging.getLogger(__name__)

import pprint

from django.db.utils import IntegrityError
from django.conf import settings
from django.utils.encoding import force_text
from django.utils import translation
from django.core.exceptions import ValidationError
from django.utils import translation

#~ from django.utils import unittest
#~ from django.test.client import Client
#from lino.igen import models
#from lino.modlib.contacts.models import Contact, Companies
#from lino.modlib.countries.models import Country

from lino.api import dd, rt
from lino.utils import i2d
from lino.utils.djangotest import TestCase


class DemoTest(TestCase):
    #~ fixtures = [ 'std','demo' ]
    fixtures = settings.SITE.demo_fixtures
    never_build_site_cache = True
    maxDiff = None

    def test_01(self):
        etypes = settings.SITE.modules.events.Type.objects.order_by('id')
        #~ dbutils.set_language('de')
        with translation.override('de'):
            lst = [unicode(obj) for obj in etypes]
            expected = ['Breitensport',
                        'Radrennen Stra\xdfe',
                        'MTB Rennen \u2265 15-j\xe4hrige',
                        'Mountainbike Rennsport -- Kids Trophy O2 Biker/V.O.R.-Lotto']
            self.assertEqual(lst, expected)

            s = etypes[0].EventsByType().to_rst()
            #~ print s
            expected = """\
+------------------------------+--------------------------------------------------+---------------------------------------+
| Wann                         | Was                                              | Wo                                    |
+==============================+==================================================+=======================================+
| Sonntag, 24. März 2013       | **18\. Bike-Day  IRMEP-RSK Eupen** |br|          | IRMEP-Kaserne **Eupen**               |
|                              | Mountain-Bike-Ausfahrt, Volksradfahren           |                                       |
+------------------------------+--------------------------------------------------+---------------------------------------+
| Sonntag, 5. Mai 2013         | **24\. Eifel-Biker event** |br|                  | Zur Domäne **Bütgenbach**             |
|                              | Mountain-Bike-Ausfahrt, Volksradfahren           |                                       |
+------------------------------+--------------------------------------------------+---------------------------------------+
| Samstag, 6. Juli 2013        | **Internationale 3 Länderfahrt** |br|            | Triangel **Sankt Vith**               |
|                              | Volksradfahren, Straße- und Mountain Bike Touren |                                       |
+------------------------------+--------------------------------------------------+---------------------------------------+
| `Sonntag,                    | **Radtag der DG** |br|                           | Galmeiplatz (Koul-Gelände) **Kelmis** |
| 1.                           | Volksradfahren, Straße- und Mountain Bike Touren |                                       |
| September                    |                                                  |                                       |
| 2013 <http://www.vclc.be>`__ |                                                  |                                       |
+------------------------------+--------------------------------------------------+---------------------------------------+
"""
            self.assertEqual(s, expected)
