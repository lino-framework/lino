# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Adds actions to read Belgian eID card.
See unit tests in :mod:`lino_welfare.tests.test_beid`.

"""

import logging
logger = logging.getLogger(__name__)

import os
import yaml
import base64

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from lino.core.dbutils import get_field

from lino.utils.xmlgen.html import E
from lino.utils import AttrDict

from lino import dd, rt, mixins


from lino.utils import ssin
from lino.utils import join_words
from lino.utils import IncompleteDate
from lino.modlib.contacts.utils import street2kw

config = dd.plugins.beid

dd.add_user_group('beid', config.verbose_name)


def simulate_wrap(msg):
    if config.read_only_simulate:
        msg = "(%s:) %s" % (unicode(_("Simulation")), msg)
    return msg


class BeIdCardTypes(dd.ChoiceList):
    "See :class:`ml.beid.BeIdCardTypes`."

    # app_label = 'lino'
    required = dd.required(user_level='admin')
    verbose_name = _("eID card type")
    verbose_name_plural = _("eID card types")

add = BeIdCardTypes.add_item
add('1', _("Belgian citizen"), "belgian_citizen")
# ,de=u"Belgischer Staatsbürger",fr=u"Citoyen belge"),
add('6', _("Kids card (< 12 year)"), "kids_card")
#,de=u"Kind unter 12 Jahren"),

#~ add('8', _("Habilitation"))
#,fr=u"Habilitation",nl=u"Machtiging")

add('11', _("Foreigner card A"), "foreigner_a")
        #~ nl=u"Bewijs van inschrijving in het vreemdelingenregister - Tijdelijk verblijf",
        #~ fr=u"Certificat d'inscription au registre des étrangers - Séjour temporaire",
        #~ de=u"Ausländerkarte A Bescheinigung der Eintragung im Ausländerregister - Vorübergehender Aufenthalt",
add('12', _("Foreigner card B"), "foreigner_b")
        #~ nl=u"Bewijs van inschrijving in het vreemdelingenregister",
        #~ fr=u"Certificat d'inscription au registre des étrangers",
        #~ de=u"Ausländerkarte B (Bescheinigung der Eintragung im Ausländerregister)",
add('13', _("Foreigner card C"), "foreigner_c")
        #~ nl=u"Identiteitskaart voor vreemdeling",
        #~ fr=u"Carte d'identité d'étranger",
        #~ de=u"C (Personalausweis für Ausländer)",
add('14', _("Foreigner card D"), "foreigner_d")
        #~ nl=u"EG - langdurig ingezetene",
        #~ fr=u"Résident de longue durée - CE",
        #~ de=u"Daueraufenthalt - EG",
add('15', _("Foreigner card E"), "foreigner_e")
        #~ nl=u"Verklaring van inschrijving",
        #~ fr=u"Attestation d’enregistrement",
        #~ de=u"Anmeldebescheinigung",
add('16', _("Foreigner card E+"), "foreigner_e_plus")
        # Document ter staving van duurzaam verblijf van een EU onderdaan
add('17', _("Foreigner card F"), "foreigner_f")
        #~ nl=u"Verblijfskaart van een familielid van een burger van de Unie",
        #~ fr=u"Carte de séjour de membre de la famille d’un citoyen de l’Union",
        #~ de=u"Aufenthaltskarte für Familienangehörige eines Unionsbürgers",
add('18', _("Foreigner card F+"), "foreigner_f_plus")


class BaseBeIdReadCardAction(dd.Action):
    "See :class:`ml.beid.BaseBeIdReadCardAction`."
    label = _("Read eID card")
    required = dd.Required(user_groups='beid')
    preprocessor = 'Lino.beid_read_card_processor'
    http_method = 'POST'
    sorry_msg = _("Sorry, I cannot handle that case: %s")

    def get_view_permission(self, profile):
        if not settings.SITE.use_java:
            return False
        return super(BaseBeIdReadCardAction, self).get_view_permission(profile)

    def get_button_label(self, actor):
        return self.label

    def attach_to_actor(self, actor, name):
        """
        Don't add this action when `beid` app is not installed.
        """
        if config is None:
            return False

        return super(
            BaseBeIdReadCardAction, self).attach_to_actor(actor, name)

    def card2client(self, data):
        countries = dd.resolve_app('countries', strict=True)

        kw = dict()
        raw_data = data['card_data']
        if not '\n' in raw_data:
            # a one-line string means that some error occured (e.g. no
            # card in reader). of course we want to show this to the
            # user.
            raise Warning(raw_data)

        #~ print cd
        data = AttrDict(yaml.load(raw_data))
        #~ raise Exception("20131108 cool: %s" % cd)

        kw.update(national_id=ssin.format_ssin(str(data.nationalNumber)))
        kw.update(first_name=data.firstName or '')
        kw.update(middle_name=data.middleName or '')
        kw.update(last_name=data.name or '')

        card_number = str(data.cardNumber)

        if data.photo:
            fn = config.card_number_to_picture_file(card_number)
            if os.path.exists(fn):
                logger.warning("Overwriting existing image file %s.", fn)
            try:
                fp = file(fn, 'wb')
                fp.write(base64.b64decode(data.photo))
                fp.close()
            except IOError as e:
                logger.warning("Failed to store image file %s : %s", fn, e)
                
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
        if data.streetAndNumber:
            # kw.update(street=data.streetAndNumber)
            kw = street2kw(data.streetAndNumber, **kw)
        if data.zip:
            kw.update(zip_code=str(data.zip))
        if data.placeOfBirth:
            kw.update(birth_place=data.placeOfBirth)
        pk = data.reader.upper()

        msg1 = "BeIdReadCardToClientAction %s" % kw.get('national_id')

        country = countries.Country.objects.get(isocode=pk)
        kw.update(country=country)
        if data.municipality:
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
            # logger.info("20130103 documentType %r --> %r", dt, rv)
            return rv
        kw.update(card_type=doctype2cardtype(data.documentType))

        if config.data_collector_dir:
            logger.info("Gonna write raw eid card data: %r", raw_data)
            fn = os.path.join(
                config.data_collector_dir,
                card_number + '.txt')
            file(fn, "w").write(raw_data.encode('utf-8'))
            logger.info("Wrote eid card data to file %s", fn)

        return kw

    def process_row(self, ar, obj, attrs):
        """Generate a confirmation which asks to update the given data row
        `obj` using the data read from the eid card (given in `attr`).

        """
        oldobj = obj
        watcher = dd.ChangeWatcher(obj)
        objects, diffs = obj.get_beid_diffs(attrs)

        if len(diffs) == 0:
            return self.goto_client_response(
                ar, obj, _("Client %s is up-to-date") % unicode(obj))

        msg = _("Click OK to apply the following changes for %s") % obj
        msg = simulate_wrap(msg)
        msg += ' :<br/>'
        msg += '\n<br/>'.join(diffs)

        def yes(ar2):
            msg = _("%s has been saved.") % dd.obj2unicode(obj)
            if not config.read_only_simulate:
                for o in objects:
                    o.full_clean()
                    o.save()
                watcher.send_update(ar2.request)
            msg = simulate_wrap(msg)
            return self.goto_client_response(ar2, obj, msg)

        def no(ar2):
            return self.goto_client_response(ar2, oldobj)
        #~ print 20131108, msg
        cb = ar.add_callback(msg)
        cb.add_choice('yes', yes, _("Yes"))
        cb.add_choice('no', no, _("No"))
        ar.set_callback(cb)
        #~ cb.add_choice('cancel',no,_("Don't apply"))
        #~ return cb

    def goto_client_response(self, ar, obj, msg=None, **kw):
        """Called from different places but always the same result.  Calls
:meth:`ar.goto_instance <rt.ActionRequest.goto_instance>`.

        """
        # kw.update(goto_record_id=obj.pk)
        ar.goto_instance(obj)
        #~ ba = self.defining_actor.detail_action
        #~ kw.update(eval_js=ar.row_action_handler(ba,obj,ar))
        #~ kw.update(eval_js=ar.instance_handler(obj))
        #~ kw.update(refresh=True)
        if msg:
            return ar.success(msg, _("Success"), **kw)
        return ar.success(msg, **kw)

NAMES = tuple('last_name middle_name first_name'.split())


class FindByBeIdAction(BaseBeIdReadCardAction):
    "See :class:`ml.beid.FindByBeIdAction`."

    select_rows = False
    show_in_bbar = False

    def run_from_ui(self, ar, **kw):
        attrs = self.card2client(ar.request.POST)
        qs = holder_model().objects.filter(national_id=attrs['national_id'])
        if qs.count() > 1:
            msg = self.sorry_msg % (
                _("There is more than one client with national "
                  "id %(national_id)s in our database.") % attrs)

            raise Exception(msg)  # this is impossible because
                                  # national_id is unique
            return ar.error(msg)
        if qs.count() == 0:
            fkw = dict()
            for k in NAMES:
                v = attrs[k]
                if v:
                    fkw[k+'__iexact'] = v
            # fkw = dict(last_name__iexact=attrs['last_name'],
            #            middle_name__iexact=attrs['middle_name'],
            #            first_name__iexact=attrs['first_name'])

            full_name = join_words(
                attrs['first_name'],
                attrs['middle_name'],
                attrs['last_name'])

            # If a Person with same full_name exists, the user cannot
            # (automatically) create a new Client from eid card.

            #~ fkw.update(national_id__isnull=True)
            contacts = rt.modules.contacts
            pqs = contacts.Person.objects.filter(**fkw)
            if pqs.count() == 0:
                def yes(ar2):
                    obj = holder_model()(**attrs)
                    msg = _("New client %s has been created") % obj
                    if config.read_only_simulate:
                        msg = simulate_wrap(msg)
                        return ar2.warning(msg)
                    else:
                        obj.full_clean()
                        obj.save()
                        objects, diffs = obj.get_beid_diffs(attrs)
                        for o in objects:
                            o.full_clean()
                            o.save()
                        #~ changes.log_create(ar.request,obj)
                        dd.pre_ui_create.send(obj, request=ar2.request)
                        return self.goto_client_response(ar2, obj, msg)
                msg = _("Create new client %s : Are you sure?") % full_name
                msg = simulate_wrap(msg)
                return ar.confirm(yes, msg)
            elif pqs.count() == 1:
                return ar.error(
                    self.sorry_msg % _(
                        "Cannot create new client because "
                        "there is already a person named "
                        "%s in our database.")
                    % full_name, alert=_("Oops!"))
            else:
                return ar.error(
                    self.sorry_msg % _(
                        "Cannot create new client because "
                        "there is more than one person named "
                        "%s in our database.")
                    % full_name, alert=_("Oops!"))

        assert qs.count() == 1
        row = qs[0]
        return self.process_row(ar, row, attrs)


class BeIdReadCardAction(BaseBeIdReadCardAction):
    sort_index = 90
    icon_name = 'vcard'

    def run_from_ui(self, ar, **kw):
        attrs = self.card2client(ar.request.POST)
        row = ar.selected_rows[0]
        qs = holder_model().objects.filter(
            national_id=attrs['national_id'])
        if not row.national_id and qs.count() == 0:
            row.national_id = attrs['national_id']
            row.full_clean()
            row.save()
            # don't return, continue below

        elif row.national_id != attrs['national_id']:
            return ar.error(
                self.sorry_msg %
                _("National IDs %s and %s don't match ") % (
                    row.national_id, attrs['national_id']))
        return self.process_row(ar, row, attrs)


class BeIdCardHolder(dd.Model):
    class Meta:
        abstract = True

    #~ national_id = models.CharField(max_length=200,
    national_id = dd.NullCharField(
        max_length=200,
        unique=True,
        verbose_name=_("National ID")
        #~ blank=True,verbose_name=_("National ID")
        # ~ ,validators=[ssin.ssin_validator] # 20121108
    )

    nationality = dd.ForeignKey('countries.Country',
                                blank=True, null=True,
                                related_name='by_nationality',
                                verbose_name=_("Nationality"))
    card_number = models.CharField(max_length=20,
                                   blank=True,  # null=True,
                                   verbose_name=_("eID card number"))
    card_valid_from = models.DateField(
        blank=True, null=True,
        verbose_name=_("ID card valid from"))
    card_valid_until = models.DateField(
        blank=True, null=True,
        verbose_name=_("until"))

    card_type = BeIdCardTypes.field(blank=True)

    card_issuer = models.CharField(max_length=50,
                                   blank=True,  # null=True,
                                   verbose_name=_("eID card issuer"))
    "The administration who issued this ID card. Imported from TIM."

    read_beid = BeIdReadCardAction()
    find_by_beid = FindByBeIdAction()

    noble_condition = models.CharField(
        max_length=50,
        blank=True,  # null=True,
        verbose_name=_("noble condition"),
        help_text=_("The eventual noble condition of this person."))

    if False:  # see 20140210
        print_eid_content = dd.DirectPrintAction(
            _("eID sheet"), 'eid-content', icon_name='vcard')

    beid_readonly_fields = set(
        'noble_condition card_valid_from card_valid_until \
        card_issuer card_number card_type'.split())

    def disabled_fields(self, ar):
        rv = super(BeIdCardHolder, self).disabled_fields(ar)
        if ar.get_user().profile.level < dd.UserLevels.admin:
            rv |= self.beid_readonly_fields
        #~ logger.info("20130808 beid %s", rv)
        return rv

    def has_valid_card_data(self, today=None):
        if not self.card_number:
            return False
        if self.card_valid_until < (today or dd.today()):
            return False
        return True

    @dd.displayfield(_("eID card"), default='<br/><br/><br/><br/>')
    def eid_info(self, ar):
        "Display some information about the eID card."
        must_read = False
        attrs = dict(class_="lino-info")
        elems = []
        if self.card_number:
            elems += ["%s %s (%s)" %
                      (ugettext("Card no."), self.card_number, self.card_type)]
            if self.card_issuer:
                elems.append(", %s %s" %
                             (ugettext("issued by"), self.card_issuer))
                #~ card_issuer = _("issued by"),
            if self.card_valid_until is not None:
                valid = ", %s %s %s %s" % (
                    ugettext("valid from"), dd.dtos(self.card_valid_from),
                    ugettext("until"), dd.dtos(self.card_valid_until))
                if self.card_valid_until < dd.today():
                    must_read = True
                    elems.append(E.b(valid))
                    elems.append(E.br())
                else:
                    elems.append(valid)

            else:
                must_read = True
        else:
            must_read = True
        if must_read:
            msg = _("Must read eID card!")
            if config:
                elems.append(ar.instance_action_button(
                    self.read_beid, msg, icon_name=None))
            else:
                elems.append(msg)
            # same red as in lino.css for .x-grid3-row-red td
            # ~ attrs.update(style="background-color:#FA7F7F; padding:3pt;")
            attrs.update(class_="lino-info-red")
        return E.div(*elems, **attrs)

    def get_beid_diffs(obj, attrs):
        """Return two lists, one with the objects to save, and another with
        text lines to build a confirmation message explaining which
        changes are going to be applied after confirmation.

        The default implemantion is for the simple case where the
        holder is also a contacts.AddressLocation and the address is
        within the same database row.

        """
        raise Exception("not tested")
        diffs = []
        objects = []
        # model = holder_model()
        model = obj.__class__  # the holder
        for fldname, new in attrs.items():
            fld = get_field(model, fldname)
            old = getattr(obj, fldname)
            if old != new:
                diffs.append(
                    "%s : %s -> %s" % (
                        unicode(fld.verbose_name), dd.obj2str(old),
                        dd.obj2str(new)))
                setattr(obj, fld.name, new)
        return objects, diffs


def holder_model():
    cmc = list(rt.models_by_base(BeIdCardHolder))
    if len(cmc) != 1:
        raise Exception(
            "There must be exactly one BeIdCardHolder model in your Site!")
    return cmc[0]

