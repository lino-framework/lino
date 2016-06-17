# -*- coding: UTF-8 -*-
# Copyright 2009-2016 Luc Saffre
# License: BSD (see file COPYING for details)

""".. management_command:: garble_persons

Garbles person names in the database so that it may be used for a
demo.

"""

from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from lino.utils import dblogger
from lino.utils import Cycler, join_words

from lino.api import dd, rt

from lino.utils import confirm

from lino.utils import demonames as demo


class Distribution(object):
    def __init__(self):
        self.LAST_NAMES = Cycler(self.get_last_names())
        self.MALES = Cycler(self.get_male_first_names())
        self.FEMALES = Cycler(self.get_female_first_names())

    def before_save(self, obj):
        pass


class BelgianDistribution(Distribution):
    def get_last_names(self):
        yield demo.LAST_NAMES_BELGIUM
        yield demo.LAST_NAMES_MUSLIM
        yield demo.LAST_NAMES_BELGIUM
        yield demo.LAST_NAMES_RUSSIA
        yield demo.LAST_NAMES_BELGIUM
        yield demo.LAST_NAMES_AFRICAN

    def get_male_first_names(self):
        yield demo.MALE_FIRST_NAMES_FRANCE
        yield demo.MALE_FIRST_NAMES_MUSLIM
        yield demo.MALE_FIRST_NAMES_FRANCE
        yield demo.MALE_FIRST_NAMES_RUSSIA
        yield demo.MALE_FIRST_NAMES_FRANCE
        yield demo.MALE_FIRST_NAMES_AFRICAN

    def get_female_first_names(self):
        yield demo.FEMALE_FIRST_NAMES_FRANCE
        yield demo.FEMALE_FIRST_NAMES_MUSLIM
        yield demo.FEMALE_FIRST_NAMES_FRANCE
        yield demo.FEMALE_FIRST_NAMES_RUSSIA
        yield demo.FEMALE_FIRST_NAMES_FRANCE
        yield demo.FEMALE_FIRST_NAMES_AFRICAN


class EstonianDistribution(Distribution):
    def __init__(self):
        super(EstonianDistribution, self).__init__()
        Country = rt.modules.countries.Country
        Place = rt.modules.countries.Place
        PlaceTypes = rt.modules.countries.PlaceTypes
        self.tallinn = Place.objects.get(
            type=PlaceTypes.town, name="Tallinn")
        self.eesti = Country.objects.get(isocode="EE")
        self.streets = Cycler(self.get_streets())

    def get_last_names(self):
        yield demo.LAST_NAMES_ESTONIA

    def get_male_first_names(self):
        yield demo.MALE_FIRST_NAMES_ESTONIA

    def get_female_first_names(self):
        yield demo.FEMALE_FIRST_NAMES_ESTONIA

    def get_streets(self):
        Place = rt.modules.countries.Place
        PlaceTypes = rt.modules.countries.PlaceTypes
        for streetname, linnaosa in demo.streets_of_tallinn():
            t = PlaceTypes.township
            try:
                p = Place.objects.get(type=t, name__iexact=linnaosa)
            except Place.DoesNotExist:
                raise Exception("Unknown %s %r" % (t, linnaosa))
            yield p, streetname

    def before_save(self, obj):
        if obj.country and obj.country.isocode == 'BE':
            obj.country = self.eesti
            p, s = self.streets.pop()
            obj.city = p
            obj.zip_code = p.zip_code
            obj.street = s


class Command(BaseCommand):
    args = '(no arguments)'
    help = "Garbles person names in the database so that it "
    "may be used for a demo."

    def add_arguments(self, parser):
        parser.add_argument('--noinput', action='store_false',
                            dest='interactive', default=True,
                            help='Do not prompt for input of any kind.'),
        parser.add_argument('--distribution', action='store',
                            dest='distribution', default='BE',
                            help='Distribution to use. Available dists are BE and EE.')

    def handle(self, *args, **options):

        dbname = settings.DATABASES['default']['NAME']
        if options.get('interactive'):
            if not confirm("This is going to GARBLE your database (%s).\n"
                           "Are you sure (y/n) ?" % dbname):
                raise CommandError("User abort.")

        def build_dist(k):
            k = k.upper()
            if k == 'BE':
                return BelgianDistribution()
            if k == 'EE':
                return EstonianDistribution()
            raise CommandError("Invalid distribution key %r." % k)

        dist = build_dist(options.get('distribution'))

        User = dd.resolve_model(settings.SITE.user_model)
        Person = rt.modules.contacts.Person

        for p in Person.objects.order_by('id'):
            if User.objects.filter(partner=p).count() > 0:
                # users keep their original name
                pass
            else:
                p.last_name = dist.LAST_NAMES.pop()
                if p.gender == dd.Genders.male:
                    p.first_name = dist.MALES.pop()
                    dist.FEMALES.pop()
                else:
                    p.first_name = dist.FEMALES.pop()
                    dist.MALES.pop()
                p.name = join_words(p.last_name, p.first_name)
                dist.before_save(p)
                p.save()
                dblogger.info(p.get_address(', '))
