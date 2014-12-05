# -*- coding: UTF-8 -*-
# Copyright 2012-2013 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Defines the :class:`Page` model, the base of Lino's out-of-the-box CMS.

"""

import logging
logger = logging.getLogger(__name__)

import os
import sys
import cgi
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.utils.translation import get_language

from lino import dd, rt
from lino.utils.xmlgen import html as xghtml
E = xghtml.E

from lino import mixins
from django.conf import settings

PAGES = settings.SITE.plugins.pages

#~ class PageType(dbutils.BabelNamed,mixins.PrintableType,outbox.MailableType):

    #~ templates_group = 'pages/Page'

    #~ class Meta:
        #~ verbose_name = _("Page Type")
        #~ verbose_name_plural = _("Page Types")

    #~ remark = models.TextField(verbose_name=_("Remark"),blank=True)

    #~ def __unicode__(self):
        #~ return self.name


#~ class PageTypes(dd.Table):
    #~ """
    #~ Displays all rows of :class:`PageType`.
    #~ """
    #~ model = 'pages.PageType'
    #~ column_names = 'name build_method template *'
    #~ order_by = ["name"]

    #~ detail_layout = """
    #~ id name
    #~ build_method template email_template attach_to_email
    #~ remark:60x5
    #~ pages.PagesByType
    #~ """


#~ class Page(mixins.TypedPrintable,
      #~ mixins.AutoUser,
      #~ mixins.Controllable,
      #~ mixins.CreatedModified,
      #~ mixins.ProjectRelated,
      #~ outbox.Mailable,
      #~ postings.Postable,
      #~ ):

#~ class Page(dd.Model):
class Page(mixins.Referrable, mixins.Hierarizable):

    """
    Deserves more documentation.
    """

    class Meta:
        #~ abstract = True
        verbose_name = _("Node")
        verbose_name_plural = _("Nodes")
        #~ unique_together = ['ref','language']

    # ~ ref = dd.NullCharField(_("Reference"),blank=True,max_length=100) # ,unique=True)
    #~ ref = models.CharField(_("Reference"),max_length=100,blank=True,unique=True)
    #~ language = dbutils.LanguageField(default=dbutils.get_language,blank=True)
    #~ language = dbutils.LanguageField(blank=True)

    #~ type = models.ForeignKey(PageType,blank=True,null=True)
    # ,null=True)
    title = dd.BabelCharField(_("Title"), max_length=200, blank=True)
    #~ abstract = dd.RichTextField(_("Abstract"),blank=True,format='html')
    body = dd.BabelTextField(_("Body"), blank=True, format='plain')

    #~ special = models.BooleanField(_("Special"),default=False)
    raw_html = models.BooleanField(_("raw html"), default=False)

    #~ def __unicode__(self):
        #~ return "%s -> %s (%s)" % (self.ref,self.title,self.language)
        #~ return "%s -> %s (%s)" % (self.ref,self.title,self.language)
        #~ return u'%s %s' % (self._meta.verbose_name,self.ref)
    #~ def get_mailable_type(self):
        #~ return self.type

    def get_absolute_url(self):
        if self.ref:
            if self.ref != 'index':
                return PAGES.build_plain_url(self.ref)
        return PAGES.build_plain_url()

    def get_sidebar_caption(self):
        if self.title:
            return dd.babelattr(self, 'title')
        if self.ref == 'index':
            return unicode(_('Home'))
        if self.ref:
            return self.ref
        return str(self.id)

        #~ if self.ref or self.parent:
            #~ return self.ref
        #~ return unicode(_('Home'))

    def get_sidebar_item(self, request, other):
        a = E.a(self.get_sidebar_caption(), href=self.get_absolute_url())
        if self == other:
            return E.li(a, class_='active')
        return E.li(a)

    def get_sidebar_html(self, request):
        items = []
        #~ loop over top-level nodes
        for n in Page.objects.filter(parent__isnull=True).order_by('seqno'):
            #~ items += [li for li in n.get_sidebar_items(request,self)]
            items.append(n.get_sidebar_item(request, self))
            if self.is_parented(n):
                children = []
                for ch in n.children.order_by('seqno'):
                    children.append(ch.get_sidebar_item(request, self))
                if len(children):
                    items.append(E.ul(*children, class_='nav nav-list'))

        e = E.ul(*items, class_='nav nav-list')
        return E.tostring_pretty(e)

    def get_sidebar_menu(self, request):
        #~ qs = self.get_siblings()
        qs = Page.objects.filter(parent__isnull=True)
        #~ qs = self.children.all()
        yield ('/', 'index', unicode(_('Home')))
            #~ yield ('/downloads/', 'downloads', 'Downloads')
        #~ yield ('/about', 'about', 'About')
        #~ if qs is not None:
        for obj in qs:
            if obj.ref and obj.title:
                yield ('/' + obj.ref, obj.ref, dd.babelattr(obj, 'title'))
            #~ else:
                #~ yield ('/','index',obj.title)


#~ class PageDetail(dd.FormLayout):
    #~ main = """
    #~ ref title type:25
    #~ project id user:10 language:8 build_time
    #~ left right
    #~ """
    #~ left = """
    # ~ # abstract:60x5
    #~ body:60x20
    #~ """
    #~ right="""
    #~ outbox.MailsByController
    #~ postings.PostingsByController
    #~ """
class PageDetail(dd.FormLayout):
    main = """
    ref parent seqno
    title
    body
    """


class Pages(dd.Table):
    model = 'pages.Page'
    detail_layout = PageDetail()
    column_names = "ref title *"
    #~ column_names = "ref language title user type project *"
    order_by = ["ref"]


#~ class MyPages(mixins.ByUser,Pages):
    #~ required = dict(user_groups='office')
    #~ column_names = "modified title type project *"
    #~ label = _("My pages")
    #~ order_by = ["-modified"]


#~ class PagesByType(Pages):
    #~ master_key = 'type'
    #~ column_names = "title user *"
    #~ order_by = ["-modified"]
#~ if settings.SITE.project_model:
    #~ class PagesByProject(Pages):
        #~ master_key = 'project'
        #~ column_names = "type title user *"
        #~ order_by = ["-modified"]
def create_page(**kw):
    #~ logger.info("20121219 create_page(%r)",kw['ref'])
    return Page(**kw)


def lookup(ref, *args, **kw):
    #~ if ref == '':
        #~ ref = None
    return Page.get_by_ref(ref, *args, **kw)
    #~ try:
        #~ return Page.objects.get_by_ref(ref)
    #~ except Page.DoesNotExist:
        #~ pass

from lino.modlib.pages.dummy import render_node


def setup_main_menu(site, ui, profile, m):
    m = m.add_menu('pages', settings.SITE.plugins.pages.verbose_name)
    m.add_action('pages.Pages')

system = dd.resolve_app('system')


# def setup_config_menu(site, ui, profile, m):
    # m = m.add_menu('pages', settings.SITE.plugins.pages.verbose_name)
    # m.add_action('pages.Pages')
    #~ m.add_action(PageTypes)

#~ def setup_explorer_menu(site,ui,profile,m):
    #~ m  = m.add_menu("office",system.OFFICE_MODULE_LABEL)
    #~ m.add_action(Pages)


def get_all_pages():
    return Page.objects.all()
