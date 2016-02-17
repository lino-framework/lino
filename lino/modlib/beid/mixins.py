# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Actions and Choicelists used to read Belgian eID cards.

See unit tests in :mod:`lino_welfare.tests.test_beid`.

.. autosummary::

"""
from builtins import str
from past.builtins import basestring
from builtins import object

import logging
logger = logging.getLogger(__name__)

import os
import yaml
import base64

from unipath import Path

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.exceptions import ValidationError

from lino.core.utils import get_field

from lino.core.utils import ChangeWatcher

from lino.utils.xmlgen.html import E
from lino.utils import AttrDict

from lino.api import dd, rt


from lino.utils import ssin
from lino.utils import join_words
from lino.utils import IncompleteDate
from lino.modlib.contacts.utils import street2kw
from lino.modlib.plausibility.choicelists import Checker
from .roles import BeIdUser

config = dd.plugins.beid

from .choicelists import BeIdCardTypes

MALE = Path(__file__).parent.child('luc.jpg')
FEMALE = Path(__file__).parent.child('ly.jpg')


def get_image_parts(card_number):
    return ("beid", card_number + ".jpg")


def get_image_path(card_number):
    """Return the full path of the image file on the server. This may be
    used by printable templates.

    """
    if card_number:
        parts = get_image_parts(card_number)
        # return os.path.join(settings.MEDIA_ROOT, *parts)
        return Path(settings.MEDIA_ROOT).child(*parts)
    return Path(settings.STATIC_ROOT).child("contacts.Person.jpg")


def simulate_wrap(msg):
    if config.read_only_simulate:
        msg = "(%s:) %s" % (str(_("Simulation")), msg)
    return msg


class BaseBeIdReadCardAction(dd.Action):
    """Common base for all "Read eID card" actions
    (:class:FindByBeIdAction and :class:`BeIdReadCardAction`).

    """
    label = _("Read eID card")
    required_roles = dd.required(BeIdUser)
    preprocessor = 'Lino.beid_read_card_processor'
    http_method = 'POST'
    sorry_msg = _("Sorry, I cannot handle that case: %s")

    def get_view_permission(self, profile):
        """Make invisible when :attr:`lino.core.site.Site.use_java` is
`False`."""
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
        """Convert the data coming from the card into database fields to be
        stored in the card holder.

        """
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
            if not card_number:
                raise Exception("20150730 photo data but no card_number ")
            fn = get_image_path(card_number)
            if fn.exists():
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
        watcher = ChangeWatcher(obj)
        objects, diffs = obj.get_beid_diffs(attrs)

        if len(diffs) == 0:
            return self.goto_client_response(
                ar, obj, _("Client %s is up-to-date") % str(obj))

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

    def goto_client_response(self, ar, obj, msg=None, **kw):
        """Called from different places but always the same result.  Calls
:meth:`ar.goto_instance <rt.ActionRequest.goto_instance>`.

        """
        ar.goto_instance(obj)
        if msg:
            return ar.success(msg, _("Success"), **kw)
        return ar.success(msg, **kw)

NAMES = tuple('last_name middle_name first_name'.split())


class FindByBeIdAction(BaseBeIdReadCardAction):
    """Read an eID card without being on a precise holder. Either show the
    holder or ask to create a new holder.

    This is a list action, usually called from a quicklink or a main
    menu item.

    """

    help_text = _("Find or create card holder from eID card")
    icon_name = 'vcard_add'
    select_rows = False
    # show_in_bbar = False
    sort_index = 91
    # debug_permissions = "20150129"

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
                    obj.full_clean()
                    obj.save()
                    objects, diffs = obj.get_beid_diffs(attrs)
                    for o in objects:
                        o.full_clean()
                        o.save()
                    #~ changes.log_create(ar.request,obj)
                    dd.on_ui_created.send(obj, request=ar2.request)
                    msg = _("New client %s has been created") % obj
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
    """Read eId card and store the data on the selected holder.

    This is a row action (called on a given holder).

    When the selected holder has an empty `national_id`, and when
    there is no holder yet with that `national_id` in the database,
    then we want to update the existing holder from the card.

    """
    sort_index = 90
    icon_name = 'vcard'
    help_text = _("Update card holder data from eID card")

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
    """Mixin for models which represent an eid card holder.
    Currently only Belgian eid cards are tested.
    Concrete subclasses must also inherit from :mod:`lino.mixins.Born`.

    .. attribute:: national_id

        The SSIN. It is a *nullable char field* declared *unique*. It
        is not validated directly because that would cause problems
        with legacy data where SSINs need manual control. See also
        :class:`BeIdCardHolderChecker`.

    .. attribute:: nationality

        The nationality. This is a pointer to
        :class:`countries.Country
        <lino.modlib.statbel.countries.models.Country>` which should
        contain also entries for refugee statuses.

        Note that the nationality is *not* being read from eID card
        because it is stored there as a language and gender specific
        plain text.

    .. attribute:: image

        Virtual field which displays the picture.

    """
    class Meta(object):
        abstract = True

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
    "The administration who issued this ID card."

    read_beid = BeIdReadCardAction()
    find_by_beid = FindByBeIdAction()

    noble_condition = models.CharField(
        max_length=50,
        blank=True,  # null=True,
        verbose_name=_("noble condition"),
        help_text=_("The eventual noble condition of this person."))

    beid_readonly_fields = set(
        'noble_condition card_valid_from card_valid_until \
        card_issuer card_number card_type'.split())

    def disabled_fields(self, ar):
        rv = super(BeIdCardHolder, self).disabled_fields(ar)
        if not isinstance(ar.get_user().profile.role, dd.SiteStaff):
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
        attrs = dict(class_="lino-info")
        if ar is None:
            return E.div(**attrs)
        must_read = False
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
        for fldname, new in list(attrs.items()):
            fld = get_field(model, fldname)
            old = getattr(obj, fldname)
            if old != new:
                diffs.append(
                    "%s : %s -> %s" % (
                        str(fld.verbose_name), dd.obj2str(old),
                        dd.obj2str(new)))
                setattr(obj, fld.name, new)
        return objects, diffs

    @dd.htmlbox()
    def image(self, ar):
        url = self.get_image_url(ar)
        return E.a(E.img(src=url, width="100%"), href=url, target="_blank")
        # s = '<img src="%s" width="100%%"/>' % url
        # s = '<a href="%s" target="_blank">%s</a>' % (url, s)
        # return s

    def get_image_url(self, ar):
        if self.card_number:
            parts = get_image_parts(self.card_number)
            return settings.SITE.build_media_url(*parts)
        return settings.SITE.build_static_url("contacts.Person.jpg")

    def get_image_path(self):
        return get_image_path(self.card_number)

    def make_demo_picture(self):
        """Create a demo picture for this card holder. """
        if not self.card_number:
            raise Exception("20150730")
        src = self.mf(MALE, FEMALE)
        dst = self.get_image_path()
        # dst = settings.SITE.cache_dir.child(
        #     'media', 'beid', self.card_number + '.jpg')
        if dst.needs_update([src]):
            logger.info("Create demo picture %s", dst)
            settings.SITE.makedirs_if_missing(dst.parent)
            src.copy(dst)
        else:
            logger.info("Demo picture %s is up-to-date", dst)


class BeIdCardHolderChecker(Checker):
    """Invalid NISSes are not refused à priori using a ValidationError
    (see :attr:`BeIdCardHolder.national_id`), but this checker reports
    them.

    Belgian NISSes are stored including the formatting characters (see
    :mod:`lino.utils.ssin`) in order to guarantee uniqueness.

    """
    model = BeIdCardHolder
    verbose_name = _("Check for invalid SSINs")
    
    def get_plausibility_problems(self, obj, fix=False):
        if obj.national_id:
            try:
                expected = ssin.parse_ssin(obj.national_id)
            except ValidationError as e:
                yield (False, _("Cannot fix invalid SSIN ({0})").format(e))
            else:
                got = obj.national_id
                if got != expected:
                    msg = _("Malformed SSIN '{got}' must be '{expected}'.")
                    params = dict(expected=expected, got=got, obj=obj)
                    yield (True, msg.format(**params))
                    if fix:
                        obj.national_id = expected
                        try:
                            obj.full_clean()
                        except ValidationError as e:
                            msg = _("Failed to fix malformed "
                                    "SSIN '{got}' of '{obj}'.")
                            msg = msg.format(**params)
                            raise Warning(msg)
                        obj.save()

BeIdCardHolderChecker.activate()


def holder_model():
    cmc = list(rt.models_by_base(BeIdCardHolder))
    if len(cmc) != 1:
        raise Exception(
            "There must be exactly one BeIdCardHolder model in your Site!")
    return cmc[0]

