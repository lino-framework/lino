# Copyright 2012-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

import re
from html import escape
import datetime

# from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext
from django.conf import settings


from lino.utils.report import EmptyTable
from lino.core.utils import get_models

from lino.utils.code import codetime
from lino.utils.diag import analyzer
from etgen.html import E

from lino.api import rt, dd
from .roles import SiteSearcher
from .choicelists import TimeZones

def dtfmt(dt):
    if isinstance(dt, float):
        # assert dt
        dt = datetime.datetime.fromtimestamp(dt)
        # raise ValueError("Expected float, go %r" % dt)
    return gettext("%(date)s at %(time)s") % dict(
        date=dd.fds(dt.date()),
        time=settings.SITE.strftime(dt.time()))



class SiteSearch(dd.VirtualTable):
    required_roles = dd.login_required(SiteSearcher)
    label = _("Search")
    column_names = "description matches"
    private_apps = frozenset(['sessions', 'contenttypes', 'users'])


    # _site_search_tables = []
    # @classmethod
    # def register(cls, t):
    #     assert t not in cls._site_search_tables
    #     cls._site_search_tables.append(t)

    # disabled_models = set()
    # @classmethod
    # def disable_model(cls, m):
    #     cls.disabled_models.add(m)

    @classmethod
    def get_data_rows(cls, ar):
        if ar.quick_search is None or len(ar.quick_search) < 2:
            return

        user_type = ar.get_user().user_type
        # for model in rt.models_by_base(Searchable):
        for model in get_models():
            if model._meta.app_label in cls.private_apps:
                continue
            if model.show_in_site_search:
                t = model.get_default_table()
                # for t in cls._site_search_tables:
                if not t.get_view_permission(user_type):
                    continue
                sar = t.request(
                    parent=ar, quick_search=ar.quick_search)
                for obj in sar:
                    if obj.show_in_site_search:  # don't show calview.HeaderRow
                        yield obj

    @dd.displayfield(_("Description"))
    def description(self, obj, ar):
        elems = []
        elems.append(ar.obj2html(obj))
        # elems.append(u" ({})".format(obj._meta.verbose_name))
        elems += (" (", str(obj._meta.verbose_name), ")")
        return E.p(*elems)

    @dd.displayfield(_("Matches"))
    def matches(self, obj, ar):
        # if not obj.__class__.show_in_site_search:
        #     return ""
        def bold(mo):
            return "<b>{}</b>".format(mo.group(0))
        matches = {}
        for w in ar.quick_search.split():
            char_search = True
            lst = None
            if w.startswith("#") and w[1:].isdigit():
                w = w[1:]
                char_search = False
            if w.isdigit():
                i = int(w)
                for de in obj.quick_search_fields_digit:
                    if de.value_from_object(obj) == i:
                    # if getattr(obj, fn) == int(w):
                        matches.setdefault(de, w)
            if char_search:
                for de in obj.quick_search_fields:
                    s = matches.get(de, None)
                    if s is None:
                        s = str(de.value_from_object(obj))
                        s = escape(s, quote=False)
                    r, count = re.subn(w, bold, s, flags=re.IGNORECASE)
                    if count:
                        matches[de] = r

        chunks = []
        for de in obj.quick_search_fields + obj.quick_search_fields_digit:
            lst = matches.get(de, None)
            if lst:
                chunks.append(de.name + ":" + lst)
        from lxml import etree
        s = ', '.join(chunks)
        s = "<span>" + s + "</span>"
        try:
            return etree.fromstring(s)
        except Exception as e:
            raise Exception("{} : {}".format(e, s))
        # return etree.fromstring(', '.join(chunks))
        # return E.raw(', '.join(chunks))


class About(EmptyTable):
    """
    Display information about this web site.  This defines the window
    which opens via the menu command :menuselection:`Site --> About`.
    """
    label = _("About")
    help_text = _("Show information about this site.")
    required_roles = set()
    hide_top_toolbar = True
    detail_layout = dd.DetailLayout("""
    about_html
    # server_status
    """, window_size=(60, 20))

    @dd.constant()
    def about_html(cls):

        body = []

        body.append(settings.SITE.welcome_html())

        if settings.SITE.languages:
            body.append(E.p(str(_("Languages")) + ": " + ', '.join([
                lng.django_code for lng in settings.SITE.languages])))

        # print "20121112 startup_time", settings.SITE.startup_time.date()
        # showing startup time here makes no sense as this is a constant text
        # body.append(E.p(
        #     gettext("Server uptime"), ' : ',
        #     E.b(dtfmt(settings.SITE.startup_time)),
        #     ' ({})'.format(settings.TIME_ZONE)))
        if settings.SITE.is_demo_site:
            body.append(E.p(gettext(_("This is a Lino demo site."))))
        if settings.SITE.the_demo_date:
            s = _("We are running with simulated date set to {0}.").format(
                dd.fdf(settings.SITE.the_demo_date))
            body.append(E.p(s))

        body.append(E.p(str(_("Source timestamps:"))))
        items = []
        times = []
        packages = set(['django'])

        items.append(E.li(gettext("Server timestamp"), ' : ',
            E.b(dtfmt(settings.SITE.kernel.code_mtime))))

        for p in settings.SITE.installed_plugins:
            packages.add(p.app_name.split('.')[0])
        for src in packages:
            label = src
            value = codetime('%s.*' % src)
            if value is not None:
                times.append((label, value))

        times.sort(key=lambda x: x[1])
        for label, value in times:
            items.append(E.li(str(label), ' : ', E.b(dtfmt(value))))
        body.append(E.ul(*items))
        body.append(E.p("{} : {}".format(
            _("Complexity factors"),
            ', '.join(analyzer.get_complexity_factors(dd.today())))))
        return rt.html_text(E.div(*body))

    # @dd.displayfield(_("Server status"))
    # def server_status(cls, obj, ar):
    #     st = settings.SITE.startup_time
    #     return rt.html_text(
    #         E.p(_("Running since {} ({}) ").format(
    #             st, naturaltime(st))))
