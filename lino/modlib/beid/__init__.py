# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""Add this to your :setting:`get_installed_apps`
if your Site should feature actions for reading electronic ID
smartcards.

When this app is installed, then you must also add the `.jar` files
required by :ref:`eidreader` into your media directory, in a
subdirectory named "eidreader".

Alternatively there is :mod:`lino.modlib.eid_jslib.beid` which overrides
:mod:`lino.modlib.beid` and does the same except that it uses
:ref:`eid_jslib` instead of :ref:`eidreader`

This app makes sense only if there is exactly one subclass of
:class:`BeIdCardHolder` among your Site's models.

"""

import logging
logger = logging.getLogger(__name__)

import os
import yaml
import base64

from lino import ad
from lino.utils import AttrDict


class Plugin(ad.Plugin):  # was: use_eidreader

    site_js_snippets = ['beid/eidreader.js']
    media_name = 'eidreader'

    def get_head_lines(self, site, request):
        if not site.use_java:
            return
        # p = self.build_media_url('EIDReader.jar')
        # p = self.build_media_url('eidreader.jnlp')
        p = self.build_media_url()
        p = request.build_absolute_uri(p)
        yield '<applet name="EIDReader" code="src.eidreader.EIDReader.class"'
        # yield '        archive="%s"' % p
        yield '        codebase="%s">' % p
        # seems that you may not use another size than
        # yield '        width="0" height="0">'
        # ~ yield '<param name="separate_jvm" value="true">' # 20130913
        yield '<param name="permissions" value="all-permissions">'
        # yield '<param name="jnlp_href" value="%s">' % p
        yield '<param name="jnlp_href" value="eidreader.jnlp">'
        yield '</applet>'

    def card_number_to_picture_file(self, card_number):
        #~ TODO: handle configurability of card_number_to_picture_file
        from django.conf import settings
        return os.path.join(settings.MEDIA_ROOT, 'beid',
                            card_number + '.jpg')

    def card2client(cls, data):
        "does the actual conversion"

        self = cls

        from lino.utils import ssin
        from lino import dd
        from .mixins import BeIdCardTypes
        from lino.utils import join_words
        from lino.utils import IncompleteDate
        from lino.modlib.contacts.utils import street2kw

        countries = dd.resolve_app('countries', strict=True)

        kw = dict()
        #~ assert not settings.SITE.use_eid_jslib
        #~ assert not settings.SITE.has_plugin(BeIdJsLibPlugin):
        data = data['card_data']
        if not '\n' in data:
            raise Warning(data)
        #~ print cd
        data = AttrDict(yaml.load(data))
        #~ raise Exception("20131108 cool: %s" % cd)

        kw.update(national_id=ssin.format_ssin(str(data.nationalNumber)))
        kw.update(first_name=join_words(
            data.firstName,
            data.middleName))
        kw.update(last_name=data.name)

        card_number = str(data.cardNumber)

        if data.photo:
            fn = self.card_number_to_picture_file(card_number)
            if os.path.exists(fn):
                logger.warning("Overwriting existing image file %s.", fn)
            fp = file(fn, 'wb')
            fp.write(base64.b64decode(data.photo))
            fp.close()
            #~ print 20121117, repr(data['picture'])
            #~ kw.update(picture_data_encoded=data['picture'])

        if isinstance(data.dateOfBirth, basestring):
            data.dateOfBirth = IncompleteDate(*data.dateOfBirth.split('-'))
        kw.update(birth_date=data.dateOfBirth)
        kw.update(card_valid_from=data.cardValidityDateBegin)
        kw.update(card_valid_until=data.cardValidityDateEnd)

        kw.update(card_number=card_number)
        kw.update(card_issuer=data.cardDeliveryMunicipality)
        if data.nobleCondition:
            kw.update(noble_condition=data.nobleCondition)
        kw.update(street=data.streetAndNumber)
        #~ kw.update(street_no=data['streetNumber'])
        #~ kw.update(street_box=data['boxNumber'])
        if True:  # kw['street'] and not (kw['street_no'] or kw['street_box']):
            kw = street2kw(kw['street'], **kw)
        kw.update(zip_code=str(data.zip))
        if data.placeOfBirth:
            kw.update(birth_place=data.placeOfBirth)
        pk = data.reader.upper()

        msg1 = "BeIdReadCardToClientAction %s" % kw.get('national_id')

        #~ try:
        country = countries.Country.objects.get(isocode=pk)
        kw.update(country=country)
        #~ except countries.Country.DoesNotExist,e:
        #~ except Exception,e:
            #~ logger.warning("%s : no country with code %r",msg1,pk)
        #~ BE = countries.Country.objects.get(isocode='BE')
        #~ fld = countries.Place._meta.get_field()
        kw.update(city=countries.Place.lookup_or_create(
            'name', data.municipality, country=country))

        def sex2gender(sex):
            if sex == 'MALE':
                return dd.Genders.male
            if sex == 'FEMALE':
                return dd.Genders.female
            logger.warning("%s : invalid gender code %r", msg1, sex)
        kw.update(gender=sex2gender(data.gender))

        def doctype2cardtype(dt):
            #~ if dt == 1: return BeIdCardTypes.get_by_value("1")
            rv = BeIdCardTypes.get_by_value(str(dt))
            logger.info("20130103 documentType %r --> %r", dt, rv)
            return rv
        kw.update(card_type=doctype2cardtype(data.documentType))
        return kw


