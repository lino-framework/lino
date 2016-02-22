# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Deprecated.

Add this to your :setting:`get_installed_apps`
if your Site should feature actions for reading electronic ID
smartcards.

Extends :mod:`lino.modlib.eidreader` to use eid_jslib
"""

import logging
logger = logging.getLogger(__name__)

import os
import base64


from lino_xl.lib.beid import Plugin as BeIdPlugin


class Plugin(BeIdPlugin):  # was: use_eid_jslib
    # deprecated, not tested
    site_js_snippets = ['plugins/eid_jslib.js']
    media_name = 'eid-jslib'
    media_base_url = "?"
    media_root = None
    """
    Path to the `eid_jslib` root directory. 
    Only to be used on a development server
    if the `media` directory has no symbolic link to the directory,
    and only if :attr:`use_eid_jslib` is True.
    http://code.google.com/p/eid-javascript-lib/
    """

    def get_js_includes(self, settings, language):
        yield self.build_media_url('be_belgium_eid.js')
        yield self.build_media_url('hellerim_base64.js')

    def get_body_lines(self, site, request):
        p = self.build_media_url()
        p = request.build_absolute_uri(p)
        #~ print p
        yield '<applet code="org.jdesktop.applet.util.JNLPAppletLauncher"'
        yield 'codebase = "%s/"' % p
        yield 'width="1" height="1"'
        yield 'name   = "BEIDAppletLauncher"'
        yield 'id   = "BEIDAppletLauncher"'
        yield 'archive="applet-launcher.jar,beid35libJava.jar,BEID_Applet.jar">'

        yield '<param name="codebase_lookup" value="false">'
        yield '<param name="subapplet.classname" value="be.belgium.beid.BEID_Applet">'
        yield '<param name="progressbar" value="true">'
        yield '<param name="jnlpNumExtensions" value="1">'
        yield '<param name="jnlpExtension1" value= "' + p + '/beid.jnlp">'
        #~ yield '<param name="jnlpExtension1" value= "beid.jnlp">'

        yield '<param name="debug" value="false"/>'
        yield '<param name="Reader" value=""/>'
        yield '<param name="OCSP" value="-1"/>'
        yield '<param name="CRL" value="-1"/>'
        #~ yield '<param name="jnlp_href" value="' + p + '/beid_java_plugin.jnlp" />'
        yield '<param name="jnlp_href" value="beid_java_plugin.jnlp" />'
        yield '<param name="separate_jvm" value="true">'  # 20130913
        yield '</applet>'

    def card2client(cls, data):
        "does the actual conversion"

        self = cls

        from lino.utils import ssin
        from lino.api import dd, rt
        from lino.mixins.beid import BeIdCardTypes
        from lino.utils import join_words
        from lino.utils import IncompleteDate
        from lino.modlib.contacts.utils import street2kw

        countries = dd.resolve_app('countries', strict=True)

        kw = dict()
        #~ def func(fldname,qname):
            #~ kw[fldname] = data[qname]
        kw.update(national_id=ssin.format_ssin(data['nationalNumber']))
        kw.update(first_name=join_words(
            data['firstName1'],
            data['firstName2'],
            data['firstName3']))
        #~ func('first_name','firstName1')
        kw.update(last_name=data['surname'])

        card_number = data['cardNumber']

        if 'picture' in data:
            fn = self.card_number_to_picture_file(card_number)
            if os.path.exists(fn):
                logger.warning("Overwriting existing image file %s.", fn)
            fp = file(fn, 'wb')
            fp.write(base64.b64decode(data['picture']))
            fp.close()
            #~ print 20121117, repr(data['picture'])
            #~ kw.update(picture_data_encoded=data['picture'])

        #~ func('card_valid_from','validityBeginDate')
        #~ func('card_valid_until','validityEndDate')
        #~ func('birth_date','birthDate')
        kw.update(birth_date=IncompleteDate(
            *settings.SITE.parse_date(data['birthDate'])))
        kw.update(card_valid_from=datetime.date(
            *settings.SITE.parse_date(data['validityBeginDate'])))
        kw.update(card_valid_until=datetime.date(
            *settings.SITE.parse_date(data['validityEndDate'])))
        kw.update(card_number=card_number)
        kw.update(card_issuer=data['issuingMunicipality'])
        kw.update(noble_condition=data['nobleCondition'])
        kw.update(street=data['street'])
        kw.update(street_no=data['streetNumber'])
        kw.update(street_box=data['boxNumber'])
        if kw['street'] and not (kw['street_no'] or kw['street_box']):
            kw = street2kw(kw['street'], **kw)
        kw.update(zip_code=data['zipCode'])
        kw.update(birth_place=data['birthLocation'])
        pk = data['country'].upper()

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
            'name', data['municipality'], country=country))

        def sex2gender(sex):
            if sex == 'M':
                return dd.Genders.male
            if sex in 'FVW':
                return dd.Genders.female
            logger.warning("%s : invalid gender code %r", msg1, sex)
        kw.update(gender=sex2gender(data['sex']))

        if False:
            def nationality2country(nationality):
                try:
                    return countries.Country.objects.get(
                        nationalities__icontains=nationality)
                except countries.Country.DoesNotExist, e:
                    logger.warning("%s : no country for nationality %r",
                                   msg1, nationality)
                except MultipleObjectsReturned, e:
                    logger.warning(
                        "%s : found more than one country for nationality %r",
                        msg1, nationality)
            kw.update(nationality=nationality2country(data['nationality']))

        def doctype2cardtype(dt):
            #~ logger.info("20130103 documentType is %r",dt)
            #~ if dt == 1: return BeIdCardTypes.get_by_value("1")
            return BeIdCardTypes.get_by_value(str(dt))
        kw.update(card_type=doctype2cardtype(data['documentType']))

        #~ unused = dict()
        #~ unused.update(country=country)
        #~ kw.update(sex=data['sex'])
        #~ unused.update(documentType=data['documentType'])
        #~ logger.info("Unused data: %r", unused)
        return kw


