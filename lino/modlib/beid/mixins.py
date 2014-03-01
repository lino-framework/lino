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

"""
Actions to read Belgian eID card.

TODO: 
- make it an independant app 
- make the `linoweb.js` fragmented...

"""

import logging
logger = logging.getLogger(__name__)

import datetime


from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
#~ from django.utils.translation import ugettext as __
from django.utils.translation import ugettext
from lino.core.dbutils import get_field

from lino.utils.xmlgen.html import E

from lino import dd

countries = dd.resolve_app('countries', strict=True)
config = dd.apps.get('beid', None)


class BeIdCardTypes(dd.ChoiceList):

    """List of Belgian Identification Card Types.
    
    Didn't yet find any official reference document.
    
    The eID applet returns a field `documentType` which contains a
    numeric code.  For example 1 is for "Belgian citizen", 6 for "Kids
    card",...
    
    The eID viewer, when saving a card as xml file, doesn't save these
    values nowhere, it saves a string equivalent (1 becomes
    "belgian_citizen", 6 becomes "kids_card", 17 becomes
    "foreigner_f", 16 becomes "foreigner_e_plus",...
    
    Sources:
    | [1] https://securehomes.esat.kuleuven.be/~decockd/wiki/bin/view.cgi/EidForums/ForumEidCards0073
    | [2] `Enum be.fedict.commons.eid.consumer.DocumentType <http://code.google.com/p/eid-applet/source/browse/trunk/eid-applet-service/src/main/java/be/fedict/eid/applet/service/DocumentType.java>`_

    """
    app_label = 'lino'
    required = dd.required(user_level='admin')
    verbose_name = _("eID card type")
    verbose_name_plural = _("eID card types")

add = BeIdCardTypes.add_item
add('1', _("Belgian citizen"), "belgian_citizen")
# ,de=u"Belgischer Staatsbürger",fr=u"Citoyen belge"),
add('6', _("Kids card (< 12 year)"), "kids_card")
#,de=u"Kind unter 12 Jahren"),

"""
from [1]: 
Johan: A document type of 7 is used for bootstrap cards ? What is a bootstrap card (maybe some kind of test card?) 
Danny: A bootstrap card was an eID card that was used in the early start of the eID card introduction to bootstrap 
the computers at the administration. This type is no longer issued. 
"""

#~ add('8', _("Habilitation"))
#,fr=u"Habilitation",nl=u"Machtiging")
"""
from [1]: 
Johan: A document type of 8 is used for a “habilitation/machtigings” card ? Is this for refugees or asylum seekers? 
Danny: A habilitation/machtigings card was aimed at civil servants. This type is also no longer used. 
"""

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
    """Common base for all "Read eID card" actions.
    """
    label = _("Read eID card")
    required = dd.Required(user_groups='reception')
    preprocessor = 'Lino.beid_read_card_processor'
    http_method = 'POST'
    sorry_msg = _("Sorry, I cannot handle that case: %s")

    def get_button_label(self, actor):
        return self.label

    def attach_to_actor(self, actor, name):
        """
        Don't add this action when `beid` app is not installed.
        """
        if config is None:
            return False

        cmc = list(dd.models_by_base(BeIdCardHolder))
        if len(cmc) != 1:
            raise Exception(
                "There must be exactly one BeIdCardHolder model in your Site!")
        self.client_model = cmc[0]

        return super(
            BaseBeIdReadCardAction, self).attach_to_actor(actor, name)


class FindByBeIdAction(BaseBeIdReadCardAction):
    """Read an eID card without being on a Client and either show the
Client or ask to create a new client.

    This is a list action (usually called from a quicklink or a main
    menu item).

    """

    select_rows = False

    def run_from_ui(self, ar, **kw):
        attrs = config.card2client(ar.request.POST)
        settings.SITE.logger.info("20140301 %s", attrs)


class BeIdReadCardAction(BaseBeIdReadCardAction):
    """Read beid card and store the data on the selected Client instance.
    This is a row action (called on a given client).

    """

    sort_index = 90

    icon_name = 'vcard'

    # label = _("Read eID card")
    #~ show_in_workflow = True
    #~ show_in_row_actions = True

    def run_from_ui(self, ar, **kw):
        attrs = config.card2client(ar.request.POST)
        row = ar.selected_rows[0]
        qs = self.client_model.objects.filter(
            national_id=attrs['national_id'])
        if not row.national_id and qs.count() == 0:
            row.national_id = attrs['national_id']
            row.full_clean()
            row.save()

        elif row.national_id != attrs['national_id']:
            if qs.count() > 1:
                return ar.error(
                    self.sorry_msg %
                    _("There is more than one client with national "
                      "id %(national_id)s in our database.") % attrs)
            if qs.count() == 0:
                fkw = dict(last_name__iexact=attrs['last_name'],
                           first_name__iexact=attrs['first_name'])

                # if a client with same last_name and first_name
                # exists, the user cannot (automatically) create a new
                # client from eid card.

                #~ fkw.update(national_id__isnull=True)
                qs = self.client_model.objects.filter(**fkw)
                if qs.count() == 0:
                    def yes(ar):
                        obj = self.client_model(**attrs)
                        obj.full_clean()
                        obj.save()
                        #~ changes.log_create(ar.request,obj)
                        dd.pre_ui_create.send(obj, request=ar.request)
                        return self.goto_client_response(ar, obj,
                                                         _("New client %s has been created") % obj)
                    return ar.confirm(yes,
                                      _("Create new client %(first_name)s %(last_name)s : Are you sure?") % attrs)
                elif qs.count() > 1:
                    return ar.error(self.sorry_msg %
                                    _("There is more than one client named %(first_name)s %(last_name)s in our database.")
                                    % attrs, alert=_("Oops!"))

            assert qs.count() == 1
            row = qs[0]
        return self.process_row(ar, row, attrs)

    def process_row(self, ar, obj, attrs):
        oldobj = obj
        watcher = dd.ChangeWatcher(obj)
        diffs = []
        for fldname, new in attrs.items():
            fld = get_field(self.client_model, fldname)
            old = getattr(obj, fldname)
            if old != new:
                diffs.append("%s : %s -> %s" %
                             (unicode(fld.verbose_name), dd.obj2str(old), dd.obj2str(new)))
                setattr(obj, fld.name, new)

        if len(diffs) == 0:
            #~ return self.no_diffs_response(ar,obj)
            return self.goto_client_response(ar, obj, _("Client %s is up-to-date") % unicode(obj))

        msg = unicode(_("Click OK to apply the following changes for %s") %
                      obj)
        msg += ' :<br/>'
        msg += '\n<br/>'.join(diffs)

        def yes(ar):
            obj.full_clean()
            obj.save()
            watcher.send_update(ar.request)
            #~ return self.saved_diffs_response(ar,obj)
            return self.goto_client_response(ar, obj, _("%s has been saved.") % dd.obj2unicode(obj))

        def no(ar):
            return self.goto_client_response(ar, oldobj)
        #~ print 20131108, msg
        cb = ar.add_callback(msg)
        cb.add_choice('yes', yes, _("Yes"))
        cb.add_choice('no', no, _("No"))
        ar.set_callback(cb)
        #~ cb.add_choice('cancel',no,_("Don't apply"))
        #~ return cb

    def goto_client_response(self, ar, obj, msg=None, **kw):
        kw.update(goto_record_id=obj.pk)
        #~ ba = self.defining_actor.detail_action
        #~ kw.update(eval_js=ar.row_action_handler(ba,obj,ar))
        #~ kw.update(eval_js=ar.instance_handler(obj))
        #~ kw.update(refresh=True)
        if msg:
            return ar.success(msg, _("Success"), **kw)
        return ar.success(msg, **kw)


class BeIdCardHolder(dd.Model):

    """
    Mixin for models which represent an eid card holder.
    Currently only Belgian eid cards are tested.
    Concrete subclasses must also inherit from :mod:`lino.mixins.Born`.
    """
    class Meta:
        abstract = True

    #~ national_id = models.CharField(max_length=200,
    national_id = dd.NullCharField(max_length=200,
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
        if self.card_valid_until < (today or datetime.date.today()):
            return False
        return True

    @dd.displayfield(_("eID card"), default='<br/><br/><br/><br/>')
    def eid_info(self, ar):
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
                if self.card_valid_until < datetime.date.today():
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
            #~ if settings.SITE.use_eid_jslib or settings.SITE.use_eidreader:
            if config:
                #~ ba = cls.get_action_by_name('read_beid')
                #~ elems.append(ar.action_button(ba,self,_("Must read eID card!")))
                elems.append(ar.instance_action_button(
                    self.read_beid, msg, icon_name=None))
            else:
                elems.append(msg)
            # same red as in lino.css for .x-grid3-row-red td
            # ~ attrs.update(style="background-color:#FA7F7F; padding:3pt;")
            attrs.update(class_="lino-info-red")
        return E.div(*elems, **attrs)
