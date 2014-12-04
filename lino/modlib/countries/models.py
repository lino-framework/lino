# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Defines models
:class:`Country` and
:class:`Place`.

"""
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings

from lino import dd, rt, mixins
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.core.exceptions import ValidationError

from lino.utils import join_words

menu_root = dd.plugins.countries
config = dd.plugins.countries


class PlaceType(dd.Choice):

    def find(self, name):
        M = rt.modules.countries.Place
        try:
            return M.objects.get(type=self, name=name)
        except M.DoesNotExist:
            raise Exception("No %s named %s" % (self, name))


class PlaceTypes(dd.ChoiceList):

    """
    Sources used:

    - http://en.wikipedia.org/wiki/List_of_subnational_entities

    """
    verbose_name = _("Place Type")
    item_class = PlaceType

add = PlaceTypes.add_item
# ~ add('10', pgettext_lazy(u'countries','State'))             # de:Bundesland
add('10', _('Member State'))      # de:Bundesland
add('11', _('Division'))
add('12', _('Region'))
add('13', _('Community'))            # fr:Communauté de: Gemeinschaft
add('14', _('Territory'))
# ~ add('15', _('City-state'))        # et:Linnriik  de:Stadtstaat  fr:Cité-État

add('20', _('County'), 'county')      # et:maakond   de:Regierungsbezirk
add('21', _('Province'), 'province')
add('22', _('Shire'))
add('23', _('Subregion'))
add('24', _('Department'))
add('25', _('Arrondissement'))
add('26', _('Prefecture'))
add('27', _('District'), 'district')
add('28', _('Sector'))                      # de:Kreis

add('50', _('City'), 'city')              # et:suurlinn  de:Stadt
add('51', _('Town'), 'town')              # et:linn      de:Kleinstadt
add('52', _('Municipality'), 'municipality')  # et:vald de:Gemeinde fr:Commune
add('54', _('Parish'), 'parish')           # de:Pfarre fr:Paroisse
add('55', _('Township'), 'township')       # de:Stadtteil fr:?, et: linnaosa
add('56', _('Quarter'), 'quarter')           # de:Viertel fr:Quartier

add('61', _('Borough'), 'borough')           # et:alev
add('62', _('Small borough'), 'smallborough')     # et:alevik

add('70', _('Village'), 'village')           # et:küla

#~ REGION_TYPES = '10 11 12 13 14 15 20 21 22 23 24 25 26 27 28'
#~ REGION_TYPES = [PlaceTypes.get_by_value(v) for v in REGION_TYPES.split()]


class AddressFormatter(object):

    """
    Format used in BE, DE, FR, NL...
    """
    def get_city_lines(me, self):
        if self.city is not None:
            s = join_words(self.zip_code or self.city.zip_code, self.city)
            if s:
                yield s

    def get_street_lines(me, self):
        if self.street:
            s = join_words(
                self.street_prefix, self.street,
                self.street_no)
            if self.street_box:
                if self.street_box[0] in '/-':
                    s += self.street_box
                else:
                    s += ' ' + self.street_box
            yield s


class EstonianAddressFormatter(AddressFormatter):

    """
    Format used in Estonia.
    """
    
    def format_place(self, p):
        if p.type == PlaceTypes.municipality:
            return "%s vald" % p
        elif p.type == PlaceTypes.village:
            return "%s küla" % p
        elif p.type == PlaceTypes.county:
            return "%s maakond" % p
        return unicode(p)

    def get_city_lines(me, self):
        lines = []
        if self.city:
            city = self.city
            zip_code = self.zip_code or self.city.zip_code
            # Tallinna linnaosade asemel kirjutakse "Tallinn"
            if city.type == PlaceTypes.township and city.parent:
                city = city.parent
            # linna puhul pole vaja maakonda
            if city.type in (PlaceTypes.town, PlaceTypes.city):
                s = join_words(zip_code, city)
            else:
                lines.append(me.format_place(city))
                p = city.parent
                while p and not CountryDrivers.EE.is_region(p):
                    lines.append(me.format_place(p))
                    p = p.parent
                if self.region:
                    s = join_words(zip_code, self.region)
                elif p:
                    s = join_words(zip_code, me.format_place(p))
                elif len(lines) and zip_code:
                    lines[-1] = zip_code + ' ' + lines[-1]
                    s = ''
                else:
                    s = zip_code
        else:
            s = join_words(self.zip_code, self.region)
        if s:
            lines.append(s)
        return lines


ADDRESS_FORMATTERS = dict()
ADDRESS_FORMATTERS[None] = AddressFormatter()
ADDRESS_FORMATTERS['EE'] = EstonianAddressFormatter()


def get_address_formatter(country):
    if country and country.isocode:
        af = ADDRESS_FORMATTERS.get(country.isocode, None)
        if af is not None:
            return af
    return ADDRESS_FORMATTERS.get(None)


class CountryDriver(object):

    def __init__(self, region_types, city_types):
        self.region_types = [PlaceTypes.get_by_value(v)
                             for v in region_types.split()]
        self.city_types = [PlaceTypes.get_by_value(v)
                           for v in city_types.split()]

    def is_region(self, p):
        return p and p.type and p.type in self.region_types


class CountryDrivers:
    BE = CountryDriver('21', '50 70')
    EE = CountryDriver('20', '50 51 52 55 61 62 70')
    DE = CountryDriver('10', '50 51 52 70')
    FR = CountryDriver('24', '50 51 52 70')


class Country(mixins.BabelNamed):

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    isocode = models.CharField(
        max_length=4, primary_key=True,
        verbose_name=_("ISO code"),
        help_text=_("""\
        The two-letter code for this country as defined by ISO 3166-1.
        For countries that no longer exist it may be a 4-letter code."""))
    #~ name = models.CharField(max_length=200)
    #~ name = d.BabelCharField(max_length=200,verbose_name=_("Designation"))

    short_code = models.CharField(
        max_length=4, blank=True,
        verbose_name=_("Short code"),
        help_text=_("""A short abbreviation for regional usage. Obsolete."""))

    iso3 = models.CharField(
        max_length=3, blank=True,
        verbose_name=_("ISO-3 code"),
        help_text=_("The three-letter code for this country "
                    "as defined by ISO 3166-1."))

    def allowed_city_types(self):
        cd = getattr(CountryDrivers, self.isocode, None)
        if cd is not None:
            return cd.region_types + cd.city_types
        return PlaceTypes.items()


#~ add_babel_field(Country,'name')

class Countries(dd.Table):
    help_text = _("""
    A country is a geographic entity considered a "nation".
    """)
    #~ label = _("Countries")
    model = 'countries.Country'
    required = dd.Required(user_groups='office')
    order_by = ["name", "isocode"]
    column_names = "name isocode *"
    detail_layout = """
    isocode name short_code
    countries.PlacesByCountry
    """


FREQUENT_COUNTRIES = ['BE', 'NL', 'DE', 'FR', 'LU']


class Place(mixins.BabelNamed):

    class Meta:
        verbose_name = _("Place")
        verbose_name_plural = _("Places")
        if not settings.SITE.allow_duplicate_cities:
            unique_together = (
                'country', 'parent', 'name', 'type', 'zip_code')

    country = models.ForeignKey('countries.Country')
    zip_code = models.CharField(max_length=8, blank=True)
    type = PlaceTypes.field(blank=True)
    parent = models.ForeignKey(
        'self',
        blank=True, null=True,
        verbose_name=_("Part of"),
        help_text=_("The superordinate geographic place \
        of which this place is a part."))

    #~ def __unicode__(self):
        #~ return self.name

    def get_parents(self, *grandparents):
        if self.parent_id:
            return self.parent.get_parents(self, *grandparents)
        return [self] + list(grandparents)

    @dd.chooser()
    def type_choices(cls, country):
        if country is not None:
            allowed = country.allowed_city_types()
            return [(i, t) for i, t in PlaceTypes.choices if i in allowed]
        return PlaceTypes.choices

    # def __unicode__(self):
    def get_choices_text(self, request, actor, field):
        """
        Extends the default behaviour (which would simply diplay this
        city in the current language) by also adding the name in other
        languages and the type between parentheses.
        """
        names = [self.name]
        for lng in settings.SITE.BABEL_LANGS:
            #~ n = getattr(self,'name_'+lng)
            n = getattr(self, 'name' + lng.suffix)
            if n and not n in names:
                names.append(n)
                #~ s += ' / ' + n
        if len(names) == 1:
            s = names[0]
        else:
            s = ' / '.join(names)
            # s = "%s (%s)" % (names[0], ', '.join(names[1:]))
        if True:  # TODO: attribute per type?
            s += " (%s)" % unicode(self.type)
        return s
        #~ return unicode(self)

    @classmethod
    def get_cities(cls, country):
        if country is None:
            cd = None
            flt = models.Q()
        else:
            cd = getattr(CountryDrivers, country.isocode, None)
            flt = models.Q(country=country)

        #~ types = [PlaceTypes.blank_item] 20120829
        types = [None]
        if cd:
            types += cd.city_types
            #~ flt = flt & models.Q(type__in=cd.city_types)
        else:
            types += [v for v in PlaceTypes.items() if v.value >= '50']
            #~ flt = flt & models.Q(type__gte=PlaceTypes.get_by_value('50'))
        flt = flt & models.Q(type__in=types)
        #~ flt = flt | models.Q(type=PlaceTypes.blank_item)
        return cls.objects.filter(flt).order_by('name')

        #~ if country is not None:
            #~ cd = getattr(CountryDrivers,country.isocode,None)
            #~ if cd:
                #~ return Place.objects.filter(
                    #~ country=country,
                    #~ type__in=cd.city_types).order_by('name')
            #~ return country.place_set.order_by('name')
        #~ return cls.city.field.rel.to.objects.order_by('name')


class Places(dd.Table):
    help_text = _("""
    The table of known geographical places.
    A geographical place can be a city, a town, a suburb,
    a province, a lake... any named geographic entity,
    except for countries because these have their own table.
    """)

    model = 'countries.Place'
    required = dd.Required(user_level='admin', user_groups='office')
    order_by = "country name".split()
    column_names = "country name type zip_code parent *"
    detail_layout = """
    name country
    type parent zip_code id
    PlacesByPlace
    """


class PlacesByPlace(Places):
    label = _("Subdivisions")
    master_key = 'parent'
    column_names = "name type zip_code *"
    # required = dd.Required(user_groups='office')


class PlacesByCountry(Places):
    master_key = 'country'
    column_names = "name type zip_code *"
    required = dd.Required()
    details_of_master_template = _("%(details)s in %(master)s")


class CountryCity(dd.Model):

    """Model mixin that adds two fields `country` and `city` and defines
    a context-sensitive chooser for `city`, a `create_city_choice`
    method, ...

    """
    class Meta:
        abstract = True

    country = dd.ForeignKey(
        "countries.Country", blank=True, null=True)
    city = dd.ForeignKey(
        'countries.Place',
        verbose_name=_('City'),
        blank=True, null=True)
    zip_code = models.CharField(_("Zip code"), max_length=10, blank=True)

    active_fields = 'city zip_code'
    # active fields cannot be used in insert_layout

    @dd.chooser()
    def city_choices(cls, country):
        return Place.get_cities(country)

    def create_city_choice(self, text):
        """
        Called when an unknown city name was given.
        Try to auto-create it.
        """
        if self.country is not None:
            return Place.lookup_or_create('name', text, country=self.country)

        raise ValidationError(
            "Cannot auto-create city %r if country is empty", text)

    def country_changed(self, ar):
        """
        If user changes the `country`, then the `city` gets lost.
        """
        if self.city is not None and self.country != self.city.country:
            self.city = None

    def zip_code_changed(self, ar):
        if self.country and self.zip_code:
            qs = Place.objects.filter(
                country=self.country, zip_code=self.zip_code)
            if qs.count() > 0:
                self.city = qs[0]

    def full_clean(self, *args, **kw):
        city = self.city
        if city is None:
            self.zip_code_changed(None)
        else:
            if city.country is not None and self.country != city.country:
                self.country = city.country
            if city.zip_code:
                self.zip_code = city.zip_code
        super(CountryCity, self).full_clean(*args, **kw)


class CountryRegionCity(CountryCity):
    region = models.ForeignKey(
        'countries.Place',
        blank=True, null=True,
        verbose_name=config.region_label,
        related_name="%(app_label)s_%(class)s_set_by_region")
        #~ related_name='regions')

    class Meta:
        abstract = True

    @dd.chooser()
    def region_choices(cls, country):
        if country is not None:
            cd = getattr(CountryDrivers, country.isocode, None)
            if cd:
                flt = models.Q(type__in=cd.region_types)
            else:
                flt = models.Q(type__lt=PlaceTypes.get_by_value('50'))
            #~ flt = flt | models.Q(type=PlaceTypes.blank_item)
            flt = flt & models.Q(country=country)
            return Place.objects.filter(flt).order_by('name')
            #~ return Place.filter(flt).order_by('name')
        else:
            flt = models.Q(type__lt=PlaceTypes.get_by_value('50'))
            return Place.objects.filter(flt).order_by('name')

    def create_city_choice(self, text):
        # if a Place is created by super, then we add our region
        obj = super(CountryRegionCity, self).create_city_choice(text)
        obj.region = self.region
        return obj

    @dd.chooser()
    def city_choices(cls, country, region):
        qs = super(CountryRegionCity, cls).city_choices(country)

        if region is not None:
            parent_list = [p.pk for p in region.get_parents()] + [None]
            #~ print 20120822, region,region.get_parents(), parent_list
            qs = qs.filter(parent__id__in=parent_list)
            #~ print flt

        return qs

            #~ return country.place_set.filter(flt).order_by('name')
        #~ return cls.city.field.rel.to.objects.order_by('name')


class AddressLocation(CountryRegionCity):
    "See :class:`ml.contacts.AddressLocation`."
    class Meta:
        abstract = True

    addr1 = models.CharField(
        _("Address line before street"),
        max_length=200, blank=True,
        help_text=_("Address line before street"))

    street_prefix = models.CharField(
        _("Street prefix"), max_length=200, blank=True,
        help_text=_("Text to print before name of street, "
                    "but to ignore for sorting."))

    street = models.CharField(
        _("Street"), max_length=200, blank=True,
        help_text=_("Name of street, without house number."))

    street_no = models.CharField(
        _("No."), max_length=10, blank=True,
        help_text=_("House number."))

    street_box = models.CharField(
        _("Box"), max_length=10, blank=True,
        help_text=_("Text to print after street nuber on the same line."))

    addr2 = models.CharField(
        _("Address line after street"),
        max_length=200, blank=True,
        help_text=_("Address line to print below street line."))

    def on_create(self, ar):
        sc = settings.SITE.site_config.site_company
        if sc and sc.country:
            self.country = sc.country
        super(AddressLocation, self).on_create(ar)

    def address_location_lines(self):
        #~ lines = []
        #~ lines = [self.name]
        af = get_address_formatter(self.country)

        if self.addr1:
            yield self.addr1
        for ln in af.get_street_lines(self):
            yield ln
        if self.addr2:
            yield self.addr2

        for ln in af.get_city_lines(self):
            yield ln

        if self.country is not None:
            sc = settings.SITE.site_config  # get_site_config()
            #~ print 20130228, sc.site_company_id
            if sc.site_company is None or self.country != sc.site_company.country:
                # (if self.country != sender's country)
                yield unicode(self.country)

        #~ logger.debug('%s : as_address() -> %r',self,lines)

    def address_location(self, linesep="\n"):
        return linesep.join(self.address_location_lines())

    @dd.displayfield(_("Address"))
    def address_column(self, request):
        return self.address_location(', ')



def setup_config_menu(site, ui, profile, m):
    m = m.add_menu(menu_root.app_label, menu_root.verbose_name)
    m.add_action(Countries)
    m.add_action(Places)

#~ def setup_explorer_menu(site,ui,profile,m):
    #~ m = m.add_menu("contacts",Plugin.verbose_name)
    #~ m.add_action(Places)
