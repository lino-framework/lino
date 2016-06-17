# -*- coding: UTF-8 -*-
# Copyright 2009-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Defines the :class:`ExtRenderer` class.
"""

from __future__ import unicode_literals
from __future__ import print_function
from builtins import str
from past.builtins import basestring

import logging
logger = logging.getLogger(__name__)

import os
import cgi
import time
import jinja2

from django.conf import settings
from django.db import models
from django.utils import translation
from django.utils.encoding import force_text

from django.utils.translation import ugettext as _

from lino.core.gfks import ContentType

import lino
from lino.core import constants
from lino.core.renderer import HtmlRenderer

from lino.api.ad import Plugin

from lino.core.actions import (ShowEmptyTable, ShowDetailAction,
                               InsertRow, GridEdit, SubmitDetail,
                               SubmitInsert)
from lino.core import dbtables
from lino.core import tables

from lino.utils import AttrDict
from lino.core import choicelists
from lino.core import menus
from lino.core import auth
from lino.utils import jsgen
from lino.utils.jsgen import py2js, js_code
from lino.utils.xmlgen.html import E

from lino.core.roles import SiteUser, Supervisor

if False:
    from lino.utils.jscompressor import JSCompressor
    jscompress = JSCompressor().compress
else:
    def jscompress(s):
        return s

from . import elems as ext_elems

from lino.modlib.users.choicelists import UserProfiles

if settings.SITE.user_model:
    from lino.modlib.users import models as users


def prepare_label(mi):
    return mi.label
    """
    The original idea doesn't work any more with lazy translation.
    See `/blog/2011/1112`
    """
    # ~ label = unicode(mi.label) # trigger translation
    #~ n = label.find(mi.HOTKEY_MARKER)
    #~ if n != -1:
        #~ label = label.replace(mi.HOTKEY_MARKER,'')
        # ~ #label=label[:n] + '<u>' + label[n] + '</u>' + label[n+1:]
    #~ return label


class ExtRenderer(HtmlRenderer):
    """An HTML renderer that uses the ExtJS Javascript toolkit.

    """
    is_interactive = True
    # is_prepared = False

    def __init__(self, plugin):
        HtmlRenderer.__init__(self, plugin)
        jsgen.register_converter(self.py2js_converter)

        for s in 'green blue red yellow'.split():
            self.row_classes_map[s] = 'x-grid3-row-%s' % s

        self.prepare_layouts()

    def pk2url(self, ar, pk, **kw):
        return None

    def href_to(self, ar, obj, text=None):
        h = self.instance_handler(ar, obj)
        if h is None:
            return cgi.escape(force_text(obj))
        uri = self.js2url(h)
        return self.href(uri, text or force_text(obj))

    def py2js_converter(self, v):
        """
        Additional converting logic for serializing Python values to json.
        """
        if v is settings.SITE.LANGUAGE_CHOICES:
            return js_code('LANGUAGE_CHOICES')
        if isinstance(v, choicelists.Choice):
            """
            This is special. We don't render the text but the value.
            """
            return v.value
        if isinstance(v, models.Model):
            return v.pk
        if isinstance(v, Exception):
            return str(v)
        if isinstance(v, menus.Menu):
            if v.parent is None:
                return v.items
                # kw.update(region='north',height=27,items=v.items)
                # return py2js(kw)
            return dict(text=prepare_label(v), menu=dict(items=v.items))

        if isinstance(v, menus.MenuItem):
            if v.instance is not None:
                h = self.instance_handler(None, v.instance)
                assert h is not None
                js = "function() {%s}" % h
                return self.handler_item(v, js, None)
                #~ handler = "function(){%s}" % self.instance_handler(v.instance)
                #~ return dict(text=prepare_label(v),handler=js_code(handler))

                #~ url = self.get_detail_url(v.instance,an='detail')
                #~ url = self.get_detail_url(v.instance)
            elif v.bound_action is not None:
                if v.params:
                    ar = v.bound_action.request(**v.params)
                    js = self.request_handler(ar)
                else:
                    js = self.action_call(None, v.bound_action, {})
                js = "function() {%s}" % js
                return self.handler_item(v, js, v.help_text)

            elif v.javascript is not None:
                js = "function() {%s}" % v.javascript
                return self.handler_item(v, js, v.help_text)
            elif v.href is not None:
                url = v.href
            #~ elif v.request is not None:
                #~ raise Exception("20120918 request %r still used?" % v.request)
                #~ url = self.get_request_url(v.request)
            else:
                # a separator
                #~ return dict(text=v.label)
                return v.label
                #~ url = self.build_url('api',v.action.actor.app_label,v.action.actor.__name__,fmt=v.action.name)
            if v.parent.parent is None:
                # special case for href items in main menubar
                return dict(
                    xtype='button', text=prepare_label(v),
                    #~ handler=js_code("function() { window.location='%s'; }" % url))
                    handler=js_code("function() { Lino.load_url('%s'); }" % url))
            return dict(text=prepare_label(v), href=url)
        return v

    def get_action_params(self, ar, ba, obj, **kw):
        if ba.action.parameters:
            fv = ba.action.params_layout.params_store.pv2list(
                ar, ar.action_param_values)
            kw[constants.URL_PARAM_FIELD_VALUES] = fv
        return kw

    def get_action_status(self, ar, ba, obj, **kw):
        kw.update(ar.get_status())
        if ba.action.parameters and not ba.action.keep_user_values:
            apv = ar.action_param_values
            if apv is None:
                apv = ba.action.action_param_defaults(ar, obj)
            ps = ba.action.params_layout.params_store
            kw.update(field_values=ps.pv2dict(apv))
        if isinstance(obj, models.Model):
            kw.update(record_id=obj.pk)

        return kw

    def action_button(self, obj, ar, ba, label=None, **kw):
        label = label or ba.get_button_label()
        if ba.action.parameters and not ba.action.no_params_window:
            st = self.get_action_status(ar, ba, obj)
            return self.window_action_button(
                ar, ba, st, label, **kw)
        if ba.action.opens_a_window:
            st = ar.get_status()
            if obj is not None:
                st.update(record_id=obj.pk)
            return self.window_action_button(ar, ba, st, label, **kw)
        return self.row_action_button(obj, ar, ba, label, **kw)

    def window_action_button(
            self, ar, ba, status={},
            label=None, title=None, **kw):
        """Return a HTML chunk for a button that will execute this action
        using a Javascript link to this action.

        """
        label = str(label or ba.get_button_label())
        uri = self.js2url(self.action_call(ar, ba, status))
        return self.href_button_action(
            ba, uri, label, title or ba.action.help_text, **kw)

    def put_button(self, ar, obj, text, data, **kw):

        put_data = dict()
        for k, v in list(data.items()):
            fld = obj._meta.get_field(k)
            fld._lino_atomizer.value2dict(v, put_data, obj)

        js = 'Lino.put(%s,%s,%s)' % (
            py2js(ar.requesting_panel),
            py2js(obj.pk),
            py2js(put_data))
        uri = self.js2url(js)
        return self.href_button(uri, text, **kw)

    def quick_manage_toolbar(self, ar, obj):
        """Returns a HTML chunk that displays a "toolbar" with a series of
        "quick manage buttons": one "Insert" and another to open the
        Table.

        Usage example in :ref:`sunto`.

        """
        sar = ar.actor.insert_action.request_from(ar)
        insert_btn = sar.ar2button(None, _("Insert"))
        # insert_btn = ar.insert_button(_("Insert"))
        # assert insert_btn is not None
        ba = ar.bound_action
        manage_btn = ar.renderer.action_button(
            obj, ar, ba, _("Manage"),
            icon_name='application_form')
        assert manage_btn is not None
        return E.p(insert_btn, manage_btn)

    def unused_insert_button(self, ar, text=None, known_values=None, **options):
        "Called via :meth:`lino.core.requests.ActionRequest.insert_button`."
        # changed 20140812 : known_values now defaults to ar's known_values
        raise Exception("20150218 no longer supported")
        a = ar.actor.insert_action
        if a is None:
            return
        if not a.get_bound_action_permission(ar, ar.master_instance, None):
            return
        if known_values is None:
            known_values = ar.known_values
        else:
            raise Exception("20150218 no longer supported")
        # elem = ar.create_instance(**known_values)
        st = ar.get_status()
        # st.update(data_record=ar.elem2rec_insert(ar.ah, elem))
        return self.window_action_button(ar, a, st, text, **options)

    def action_call_on_instance(
            self, obj, ar, ba, request_kwargs={}, **status):
        """Note that `ba.actor` may differ from `ar.actor` when defined on a
        different actor. Remember e.g. the "Must read eID card" action
        button in eid_info of newcomers.NewClients (20140422).

        :obj:  The database object
        :ar:   The action request
        :ba:  The bound action
        :request_kwargs: keyword arguments to forwarded to the child action request

        Any kwyword other arguments are forwarded to :meth:`ar2js`.

        """
        if ar is None:
            sar = ba.request(**request_kwargs)
        else:
            sar = ar.spawn(ba, **request_kwargs)
        return self.ar2js(sar, obj, **status)

    def ar2js(self, ar, obj, **status):
        """Implements :meth:`lino.core.renderer.HtmlRenderer.ar2js`.

        """
        rp = ar.requesting_panel
        ba = ar.bound_action

        if ba.action.is_window_action():
            # Window actions have been generated by
            # js_render_window_action(), so we just call its `run(`)
            # method:
            status.update(self.get_action_status(ar, ba, obj))
            return "Lino.%s.run(%s,%s)" % (
                ba.full_name(), py2js(rp), py2js(status))

        # It's a custom ajax action generated by
        # js_render_custom_action().

        # 20140429 `ar` is now None, see :ref:`welfare.tested.integ`
        params = self.get_action_params(ar, ba, obj)
        return "Lino.%s(%s,%s,%s)" % (
            ba.full_name(), py2js(rp), py2js(obj.pk), py2js(params))

    def request_handler(self, ar, *args, **kw):
        st = ar.get_status(**kw)
        return self.action_call(ar, ar.bound_action, st)

    def action_call(self, request, bound_action, status):
        a = bound_action.action
        if a.opens_a_window or (a.parameters and not a.no_params_window):
            if request and request.subst_user:
                status[
                    constants.URL_PARAM_SUBST_USER] = request.subst_user
            if isinstance(a, ShowEmptyTable):
                status.update(record_id=-99998)
            if request is None:
                rp = None
            else:
                rp = request.requesting_panel
            if status:
                return "Lino.%s.run(%s,%s)" % (
                    bound_action.full_name(),
                    py2js(rp),
                    py2js(status))
            return "Lino.%s.run(%s)" % (bound_action.full_name(), py2js(rp))
        return "%s()" % self.get_panel_btn_handler(bound_action)

    def get_panel_btn_handler(self, ba):
        if not ba.action.action_name:
            raise Exception(
                "Cannot make handler for nameless action %r" % ba.action)
        if ba.action.js_handler:
            h = ba.action.js_handler % ba.action.__dict__
        else:
            if ba.action.select_rows:
                h = 'Lino.row_action_handler('
            else:
                h = 'Lino.list_action_handler('
                h += "'/%s/%s'," % (ba.actor.app_label, ba.actor.__name__)
            h += "'%s'" % ba.action.action_name
            h += ",'%s'" % ba.action.http_method
            if ba.action.preprocessor:
                h += "," + ba.action.preprocessor
            h += ")"
        return h

    def row_action_handler(self, ba, obj, ar=None):
        if ar is None or ba.get_bound_action_permission(ar, obj, None):
            return self.action_call(None, ba, dict(record_id=obj.pk))

    def instance_handler(self, ar, obj):
        a = obj.get_detail_action(ar)
        
        if a is not None:
            if ar is None:
                return self.action_call(None, a, dict(record_id=obj.pk))
            if a.get_bound_action_permission(ar, obj, None):
                return self.action_call(ar, a, dict(record_id=obj.pk))

    def obj2html(self, ar, obj, text=None, **kw):
        # if not text: # Note that html elements are logical False.
        if text is None:
            text = str(obj)

        h = self.instance_handler(ar, obj)
        uri = self.js2url(h)
        return self.href_button(uri, text, **kw)

    def get_actor_url(self, actor, *args, **kw):
        return self.plugin.build_plain_url(
            "api",
            actor.app_label, actor.__name__, *args, **kw)

    def get_home_url(self, *args, **kw):
        return self.plugin.build_plain_url(*args, **kw)

    def get_request_url(self, ar, *args, **kw):
        """
        Called from ActionRequest.absolute_url() used in `Team.eml.html`

        http://127.0.0.1:8000/api/cal/MyPendingInvitations?base_params=%7B%7D
        http://127.0.0.1:8000/api/cal/MyPendingInvitations

        """

        if ar.actor.__name__ == "Main":
            return self.get_home_url(*args, **kw)

        kw = ar.get_status(**kw)
        if not kw['base_params']:
            del kw['base_params']
        #~ kw = self.request2kw(rr,**kw)
        if ar.bound_action != ar.actor.default_action:
            kw[constants.URL_PARAM_ACTION_NAME] = ar.bound_action.action.action_name
        return self.plugin.build_plain_url(
            'api', ar.actor.app_label, ar.actor.__name__, *args, **kw)

    def get_detail_url(self, obj, *args, **kw):
        return self.plugin.build_plain_url(
            'api', obj._meta.app_label, obj.__class__.__name__, str(obj.pk), *args, **kw)

    # def show_table(
    #         self, ar, stripped=True, nosummary=False, **kw):
    #     """
    #     Returns a HTML element representing this request as a table.
    #     Used by appy_pod renderer.
    #     """
    #     if ar.actor.master is not None and not nosummary:
    #         if ar.actor.slave_grid_format == 'summary':
    #             return ar.actor.get_slave_summary(ar.master_instance, ar)
    #     return ar.table2xhtml(**kw)

    def handler_item(self, mi, handler, help_text):
        #~ handler = "function(){%s}" % handler
        #~ d = dict(text=prepare_label(mi),handler=js_code(handler),tooltip="Foo")
        d = dict(text=prepare_label(mi), handler=js_code(handler))
        if mi.bound_action and mi.bound_action.action.icon_name:
            d.update(iconCls='x-tbar-' + mi.bound_action.action.icon_name)
        if settings.SITE.use_quicktips and help_text:
            d.update(listeners=dict(render=js_code(
                "Lino.quicktip_renderer(%s,%s)" % (py2js('Foo'), py2js(help_text)))
            ))
        return d

    def html_page(self, request, *args, **kw):
        """Return a string with the index page.  Content is mostly in the
        :xfile:`extjs/index.html` template.

        """
        user = request.user
        # print 20150427, user
        if True:  # user.profile.level >= UserLevels.admin:
            if request.subst_user:
                user = request.subst_user

        def getit():
            if not settings.SITE.build_js_cache_on_startup:
                self.build_js_cache(False)

            # Render teplate
            env = settings.SITE.plugins.jinja.renderer.jinja_env
            tpl = env.get_template('extjs/index.html')
            context = {
                'site': settings.SITE,
                'extjs': settings.SITE.plugins.extjs,
                'ext_renderer': self,
                'py2js': py2js,  # TODO: Should be template filter
                'jsgen': jsgen,  # TODO: Should be in filters
                'language': translation.get_language(),
                'request': request,
                'user': user,  # Current user
            }
            context.update(kw)
            return tpl.render(context)
    
        return jsgen.with_user_profile(user.profile, getit)

    def html_page_main_window(self, on_ready, request, site):
        """Called from :srcref:`lino/modlib/extjs/config/extjs/index.html`."""
        dashboard = dict(
            id="dashboard",
            xtype='container',
            autoScroll=True,
        )
        main = dict(
            id="main_area",
            xtype='container',
            region="center",
            #~ autoScroll=True,
            layout='fit',
            items=dashboard,
        )
        if not on_ready:
            dashboard.update(html=site.get_main_html(
                request, extjs=self.plugin))

        win = dict(
            layout='fit',
            #~ maximized=True,
            items=main,
            #~ closable=False,
            bbar=dict(xtype='toolbar', items=js_code('Lino.status_bar')),
            #~ title=self.site.title,
            tbar=js_code('Lino.main_menu'),
        )
        return win

    def html_page_user(self, request, site):

        # TODO: move the following to lino.modlib.users?
        if settings.SITE.user_model is not None:

            if request.user.profile.has_required_roles([SiteUser]):

                if request.subst_user:
                    yield "Lino.set_subst_user(%s,%s);" % (
                        py2js(request.subst_user.id),
                        py2js(str(request.subst_user)))
                    user_text = str(request.user) + \
                        " (" + _("as") + " " + \
                        str(request.subst_user) + ")"
                else:
                    yield "Lino.set_subst_user();"
                    user_text = str(request.user)

                user = request.user

                yield "Lino.user = %s;" % py2js(
                    dict(id=user.id, name=str(user)))

                def usertext(u):
                    return "{0} {1}, {3} ({2})".format(
                        u.last_name, u.first_name, u.username, u.profile)

                if user.profile.has_required_roles([Supervisor]):
                    authorities = [
                        (u.id, usertext(u))
                        for u in settings.SITE.user_model.objects.exclude(
                            profile='').exclude(id=user.id)]
                else:
                    qs = users.Authority.objects.filter(
                        authorized=user).exclude(user__profile='')
                    qs = qs.order_by(
                        'user__last_name', 'user__first_name',
                        'user__username')
                    authorities = [
                        (a.user.id, usertext(a.user)) for a in qs]

                a = users.MySettings.default_action
                handler = self.action_call(None, a, dict(record_id=user.pk))
                handler = "function(){%s}" % handler
                mysettings = dict(text=_("My settings"),
                                  handler=js_code(handler))
                login_menu_items = [mysettings]
                if len(authorities):
                    act_as = [
                        dict(text=t, handler=js_code(
                            "function(){Lino.set_subst_user(%s, %s)}" % (v, py2js(t))))
                        for v, t in authorities]
                            #~ for v,t in user.get_received_mandates()]
                    act_as.insert(0, dict(
                        text=_("Myself"),
                        handler=js_code("function(){Lino.set_subst_user(null)}")))
                    act_as = dict(text=_("Act as..."), menu=dict(items=act_as))

                    login_menu_items.insert(0, act_as)

                if site.remote_user_header is None:
                    login_menu_items.append(
                        dict(text=_("Log out"), handler=js_code('Lino.logout')))
                    if auth.get_auth_middleware().can_change_password(request, request.user):
                        login_menu_items.append(
                            dict(text=_("Change password"), handler=js_code('Lino.change_password')))
                        login_menu_items.append(
                            dict(text=_("Forgot password"), handler=js_code('Lino.forgot_password')))

                login_menu = dict(
                    text=user_text,
                    menu=dict(items=login_menu_items))

                yield "Lino.main_menu = Lino.main_menu.concat(['->',%s]);" % py2js(login_menu)

            else:
                login_buttons = [
                    dict(xtype="button", text=_("Log in"),
                         handler=js_code('Lino.show_login_window')),
                    #~ dict(xtype="button",text="Register",handler=Lino.register),
                ]
                yield "Lino.main_menu = \
                Lino.main_menu.concat(['->',%s]);" % py2js(login_buttons)

    def before_row_edit(self, panel):
        from lino.core.actions import get_view_permission
        #~ l.append("console.log('before_row_edit',record);")
        for e in panel.active_children:
            if not get_view_permission(e):
                continue
            for p in settings.SITE.installed_plugins:
                for ln in p.get_row_edit_lines(e, panel):
                    yield ln
        
    def build_site_cache(self, force=False):
        """Build the site cache files under `/media/cache`, especially the
        :xfile:`lino*.js` files, one per user profile and language.

        """
        # if not self.is_prepared:
        #     self.prepare_layouts()
        #     self.is_prepared = True

        if settings.SITE.never_build_site_cache:
            logger.debug(
                "Not building site cache because `settings.SITE.never_build_site_cache` is True")
            return
        if not os.path.isdir(settings.MEDIA_ROOT):
            logger.debug(
                "Not building site cache because " +
                "directory '%s' (settings.MEDIA_ROOT) does not exist.",
                settings.STATIC_ROOT)
            return

        started = time.time()
        # logger.info("20140401 build_site_cache started")

        settings.SITE.on_each_app('setup_site_cache', force)

        settings.SITE.makedirs_if_missing(
            os.path.join(settings.MEDIA_ROOT, 'upload'))
        settings.SITE.makedirs_if_missing(
            os.path.join(settings.MEDIA_ROOT, 'webdav'))

        if force or settings.SITE.build_js_cache_on_startup:
            count = 0
            for lng in settings.SITE.languages:
                with translation.override(lng.django_code):
                    for profile in UserProfiles.objects():
                        count += jsgen.with_user_profile(
                            profile, self.build_js_cache, force)
            logger.info("%d lino*.js files have been built in %s seconds.",
                        count, time.time() - started)

    def build_js_cache(self, force):
        """Build the :xfile:`lino*.js` file for the current user and the
        current language.  If the file exists and is up to date, don't
        generate it unless `force` is `True`.

        This is called

        - on each request if :attr:`build_js_cache_on_startup
          <lino.core.site.Site.build_js_cache_on_startup>` is `False`.

        - with `force=True` when
          :class:`lino.modlib.lino.models.BuildSiteCache` action is
          run.

        """
        fn = os.path.join(*self.lino_js_parts())

        def write(f):
            self.write_lino_js(f)

        return settings.SITE.kernel.make_cache_file(fn, write, force)
    
    def prepare_layouts(self):
        
        self.actors_list = [
            rpt for rpt in dbtables.master_reports
            + dbtables.slave_reports
            + list(dbtables.generic_slaves.values())
            + dbtables.custom_tables
            + dbtables.frames_list]

        self.actors_list.extend(
            [a for a in list(choicelists.CHOICELISTS.values())
             if settings.SITE.is_installed(a.app_label)])

        # don't generate JS for abstract actors
        self.actors_list = [a for a in self.actors_list
                            if not a.is_abstract()]

        # Layouts

        self.form_panels = set()
        self.param_panels = set()
        self.action_param_panels = set()

        def add(res, collector, fl, formpanel_name):
            # res: an actor
            # collector: one of form_panels, param_panels or
            # action_param_panels
            # fl : a FormLayout
            if fl is None:
                return
            if fl._datasource is None:
                return  # 20130804

            if fl._datasource != res:
                fl._other_datasources.add(res)
                # if str(res).startswith('newcomers.AvailableCoaches'):
                #     logger.info("20150716 %s also needed by %s", fl, res)
                # if str(res) == 'courses.Pupils':
                #     print("20160329 ext_renderer.py {2}: {0} != {1}".format(
                #         fl._datasource, res, fl))

            if False:
                try:
                    lh = fl.get_layout_handle(self.plugin)
                except Exception as e:
                    logger.exception(e)
                    raise Exception("Could not define %s for %r: %s" % (
                        formpanel_name, res, e))

                # lh.main.loosen_requirements(res)
                for e in lh.main.walk():
                    e.loosen_requirements(res)

            if fl not in collector:
                fl._formpanel_name = formpanel_name
                fl._url = res.actor_url()
                collector.add(fl)
                # if str(res) == 'courses.Pupils':
                #     print("20160329 ext_renderer.py collected {}".format(fl))

        for res in self.actors_list:
            add(res, self.form_panels, res.detail_layout,
                "%s.DetailFormPanel" % res)
            add(res, self.form_panels, res.insert_layout,
                "%s.InsertFormPanel" % res)
            add(res, self.param_panels, res.params_layout,
                "%s.ParamsPanel" % res)

            for ba in res.get_actions():
                if ba.action.parameters:
                    add(res, self.action_param_panels,
                        ba.action.params_layout,
                        "%s.%s_ActionFormPanel" % (res, ba.action.action_name))

    def write_lino_js(self, f):

        profile = jsgen.get_user_profile()

        context = dict(
            ext_renderer=self,
            site=settings.SITE,
            settings=settings,
            lino=lino,
            language=translation.get_language(),
            # ext_requests=constants,
            constants=constants,
            extjs=settings.SITE.plugins.extjs,
        )

        context.update(_=_)

        tpl = self.linolib_template()

        #~ f.write(jscompress(unicode(tpl)+'\n'))
        f.write(jscompress(tpl.render(**context) + '\n'))

        env = settings.SITE.plugins.jinja.renderer.jinja_env
        for p in settings.SITE.installed_plugins:
            if isinstance(p, Plugin):
                for tplname in p.site_js_snippets:
                    tpl = env.get_template(tplname)
                    f.write(jscompress('\n// from %s:%s\n' % (p, tplname)))
                    f.write(jscompress('\n' + tpl.render(**context) + '\n'))

        menu = settings.SITE.get_site_menu(self, profile)
        menu.add_item(
            'home', _("Home"), javascript="Lino.handle_home_button()")
        f.write("Lino.main_menu = %s;\n" % py2js(menu))

        """Call Ext.namespace for *all* actors because
        e.g. outbox.Mails.FormPanel is defined in ns outbox.Mails
        which is not directly used by non-expert users.

        """
        for a in self.actors_list:
            f.write("Ext.namespace('Lino.%s')\n" % a)

        # actors with their own `get_handle_name` don't have a js
        # implementation
        actors_list = [
            a for a in self.actors_list if a.get_handle_name is None]

        # generate only actors whose default_action is visible
        actors_list = [
            a for a in actors_list
            if a.default_action.get_view_permission(profile)]

        # Define every choicelist as a JS array:
        f.write("\n// ChoiceLists: \n")
        for a in list(choicelists.CHOICELISTS.values()):
            if settings.SITE.is_installed(a.app_label):
                f.write("Lino.%s = %s;\n" %
                        (a.actor_id, py2js(a.get_choices())))

        #~ logger.info('20120120 dbtables.all_details:\n%s',
            #~ '\n'.join([str(d) for d in dbtables.all_details]))

        assert profile == jsgen.get_user_profile()

        def must_render(lh, profile):
            """Return True if the given form layout `fl` is needed for
            profile."""
            if not lh.main.get_view_permission(profile):
                return False
            if lh.layout._datasource.get_view_permission(profile):
                return True
            for ds in lh.layout._other_datasources:
                if ds.get_view_permission(profile):
                    return True
            return False

        #~ f.write('\n/* Application FormPanel subclasses */\n')
        for fl in self.param_panels:
            lh = fl.get_layout_handle(self.plugin)
            if must_render(lh, profile):
                for ln in self.js_render_ParamsPanelSubclass(lh):
                    f.write(ln + '\n')

        for fl in self.action_param_panels:
            lh = fl.get_layout_handle(self.plugin)
            if must_render(lh, profile):
                for ln in self.js_render_ActionFormPanelSubclass(lh):
                    f.write(ln + '\n')

        assert profile == jsgen.get_user_profile()

        for fl in self.form_panels:
            lh = fl.get_layout_handle(self.plugin)
            if must_render(lh, profile):
                for ln in self.js_render_FormPanelSubclass(lh):
                    f.write(ln + '\n')

        actions_written = set()
        for rpt in actors_list:
            rh = rpt.get_handle()
            for ba in rpt.get_actions():
                if ba.action.parameters:
                    if ba.action not in actions_written:
                        actions_written.add(ba.action)
                        for ln in self.js_render_window_action(
                                rh, ba, profile):
                            f.write(ln + '\n')

        for rpt in actors_list:
            rh = rpt.get_handle()
            if isinstance(rpt, type) and issubclass(rpt, (
                    tables.AbstractTable, choicelists.ChoiceList)):
                for ln in self.js_render_GridPanel_class(rh):
                    f.write(ln + '\n')

            for ba in rpt.get_actions():
                if ba.action.parameters and not ba.action.no_params_window:
                    pass
                elif ba.action.opens_a_window:
                    if isinstance(ba.action, (ShowDetailAction,
                                              InsertRow)):
                        for ln in self.js_render_detail_action_FormPanel(
                                rh, ba):
                            f.write(ln + '\n')
                    for ln in self.js_render_window_action(rh, ba, profile):
                        f.write(ln + '\n')
                elif ba.action.action_name:
                    for ln in self.js_render_custom_action(rh, ba):
                        f.write(ln + '\n')

        if profile != jsgen.get_user_profile():
            logger.warning(
                "Oops, profile %s != jsgen.get_user_profile() %s",
                profile, jsgen.get_user_profile())

        return 1

    def lino_js_parts(self):
        profile = jsgen.get_user_profile()
        # return ('genjs',
        return ('cache', 'js',
                'lino_' + profile.value + '_'
                + translation.get_language() + '.js')

    def linolib_template(self):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(
            os.path.dirname(__file__)))
        return env.get_template('linoweb.js')

    def create_layout_element(self, *args, **kw):
        return ext_elems.create_layout_element(*args, **kw)

    def create_layout_panel(self, *args, **kw):
        return ext_elems.create_layout_panel(*args, **kw)

    def toolbar(self, action_list):
        """
        This also manages action groups
        """
        profile = jsgen.get_user_profile()
        buttons = []
        combo_map = dict()
        for ba in action_list:

            # if ba.actor.__name__ == 'AttestationsByProject':
            #     logger.info("20140401 toolbar() %r", ba.action)
            
            if ba.action.show_in_bbar and ba.get_view_permission(profile):
                if ba.action.combo_group is None:
                    buttons.append(self.a2btn(ba))
                else:
                    k = ba.action.combo_group
                    combo = combo_map.get(k, None)
                    if combo is None:
                        parent = self.a2btn(ba)
                        menu = [parent]
                        combo = AttrDict(menu=menu)
                        combo.update(iconCls=parent.get('iconCls'))
                        combo.update(
                            menu_item_text=parent.get('menu_item_text'))
                        combo.update(text=parent.get('text'))
                        buttons.append(combo)
                        combo_map[k] = combo
                    else:
                        #~ menu = parent.get('menu',None)
                        #~ if menu is None:
                            #~ id_map[k] = menu_btn
                        combo['menu'].append(self.a2btn(ba))
        reduced_buttons = []
        for b in buttons:
            menu = b.get('menu', None)
            if menu is None:
                reduced_buttons.append(b)
            elif len(menu) == 1:
                # logger.info("20140520 reduced %s", menu)
                reduced_buttons.append(menu[0])
            else:
                b.update(xtype='splitbutton')
                b.update(panel_btn_handler=menu[0]['panel_btn_handler'])
                for a in menu:
                    a['text'] = a['menu_item_text']
                    if a.get('iconCls', 1) == b.get('iconCls', 2):
                        del a['iconCls']

                reduced_buttons.append(b)
        return reduced_buttons

    def a2btn(self, ba, **kw):
        a = ba.action
        if a.parameters and not a.no_params_window:
            kw.update(panel_btn_handler=js_code(
                "Lino.param_action_handler(Lino.%s)" % ba.full_name()))
        elif isinstance(a, SubmitInsert):
            js = 'function(panel){panel.save()}'
            kw.update(panel_btn_handler=js_code(js))
        elif isinstance(a, SubmitDetail):
            js = 'function(panel){panel.save()}'
            kw.update(panel_btn_handler=js_code(js))
        elif isinstance(a, ShowDetailAction):
            kw.update(panel_btn_handler=js_code('Lino.show_detail'))
        elif isinstance(a, InsertRow):
            kw.update(panel_btn_handler=js_code('Lino.show_insert'))
        else:
            kw.update(
                panel_btn_handler=js_code(self.get_panel_btn_handler(ba)))

        if a.icon_name:
            kw.update(iconCls='x-tbar-' + a.icon_name)
        else:
            kw.update(text=a.button_text or a.label)
        kw.update(
            #~ name=a.name,
            menu_item_text=a.label,
            overflowText=a.label,
            auto_save=a.auto_save,
            itemId=a.action_name,
            #~ text=unicode(a.label),
        )
        if a.key:
            kw.update(keycode=a.key.keycode)
        if a.help_text:
            kw.update(tooltip=a.help_text)
        elif a.icon_name:
            kw.update(tooltip=a.label)
        return kw

    def build_on_render(self, main):
        "dh is a FormLayout or a ColumnsLayout"
        profile = jsgen.get_user_profile()
        on_render = []
        elems_by_field = {}
        field_elems = []
        for e in main.active_children:
            if isinstance(e, ext_elems.FieldElement):
                if e.get_view_permission(profile):
                    field_elems.append(e)
                    l = elems_by_field.get(e.field.name, None)
                    if l is None:
                        l = []
                        elems_by_field[e.field.name] = l
                    l.append(e)

        for e in field_elems:
            #~ if isinstance(e,FileFieldElement):
                #~ kw.update(fileUpload=True)
            holder = main.layout_handle.layout.get_chooser_holder()
            chooser = holder.get_chooser_for_field(e.field.name)
            if chooser:
                #~ logger.debug("20100615 %s.%s has chooser", self.lh.layout, e.field.name)
                for f in chooser.context_fields:
                    for el in elems_by_field.get(f.name, []):
                        #~ if main.has_field(f):
                        #~ varname = varname_field(f)
                        #~ on_render.append("%s.on('change',Lino.chooser_handler(%s,%r));" % (varname,e.ext_name,f.name))
                        on_render.append(
                            "%s.on('change',Lino.chooser_handler(%s,%r));" % (
                                el.as_ext(), e.as_ext(), f.name))
        return on_render

    SUPPRESSED = set(('items', 'layout'))

    def js_render_ParamsPanelSubclass(self, dh):

        yield ""
        yield "Lino.%s = Ext.extend(Ext.form.FormPanel, {" % \
            dh.layout._formpanel_name
        for k, v in list(dh.main.ext_options().items()):
            #~ if k != 'items':
            if not k in self.SUPPRESSED:
                yield "  %s: %s," % (k, py2js(v))
        #~ yield "  collapsible: true,"
        if dh.main.value['layout'] == 'hbox':
            yield "  layout: 'hbox',"
        else:
            yield "  layout: 'form',"
        yield "  autoHeight: true,"
        #~ if dh.layout.window_size and dh.layout.window_size[1] == 'auto':
            #~ yield "  autoHeight: true,"
        yield "  initComponent : function() {"
        # 20140503 yield "    var containing_panel = this;"
        lc = 0
        for ln in jsgen.declare_vars(dh.main.elements):
            yield "    " + ln
            lc += 1
        if lc == 0:
            # print 20150626, dh.main.elements[0].required_roles
            # print 20150626, jsgen._for_user_profile.__class__
            msg = "%r of %s has no variables" % (dh.main, dh)
            msg += ", datasource: %r, other datasources: %r" % (
                dh.layout._datasource, dh.layout._other_datasources)
            msg += ", main elements: %r" % dh.main.elements
            # raise Exception(msg)
            print((20150717, msg))
        yield "    this.items = %s;" % py2js(dh.main.elements)
        yield "    this.fields = %s;" % py2js(
            [e for e in dh.main.walk()
             if isinstance(e, ext_elems.FieldElement)])
        yield "    Lino.%s.superclass.initComponent.call(this);" % \
            dh.layout._formpanel_name
        yield "  }"
        yield "});"
        yield ""

    def js_render_ActionFormPanelSubclass(self, dh):
        tbl = dh.layout._datasource
        yield ""
        yield "Lino.%s = Ext.extend(Lino.ActionFormPanel,{" % \
            dh.layout._formpanel_name
        for k, v in list(dh.main.ext_options().items()):
            if k != 'items':
                yield "  %s: %s," % (k, py2js(v))
        assert tbl.action_name is not None
            #~ raise Exception("20121009 action_name of %r is None" % tbl)
        yield "  action_name: '%s'," % tbl.action_name
        yield "  ls_url: %s," % py2js(dh.layout._url)
        yield "  window_title: %s," % py2js(tbl.label)

        yield "  before_row_edit : function(record) {"
        for ln in self.before_row_edit(dh.main):
            yield "    " + ln
        yield "  },"

        #~ yield "  layout: 'fit',"
        #~ yield "  auto_save: true,"
        if dh.layout.window_size and dh.layout.window_size[1] == 'auto':
            yield "  autoHeight: true,"
        yield "  initComponent : function() {"
        # 20140503 yield "    var containing_panel = this;"
        lc = 0
        for ln in jsgen.declare_vars(dh.main.elements):
            yield "    " + ln
            lc += 1
        yield "    this.items = %s;" % py2js(dh.main.elements)
        yield "    this.fields = %s;" % py2js(
            [e for e in dh.main.walk()
             if isinstance(e, ext_elems.FieldElement)])
        yield "    Lino.%s.superclass.initComponent.call(this);" % \
            dh.layout._formpanel_name
        yield "  }"
        yield "});"
        yield ""

    def js_render_FormPanelSubclass(self, dh):

        tbl = dh.layout._datasource
        if not dh.main.get_view_permission(jsgen.get_user_profile()):
            msg = "No view permission for main panel of %s :" % \
                  dh.layout._formpanel_name
            msg += " main requires %s (actor %s requires %s)" % (
                dh.main.required_roles,
                tbl, tbl.required_roles)
            #~ raise Exception(msg)
            logger.warning(msg)
            print(20150717, msg)
            return

        yield ""
        yield "Lino.%s = Ext.extend(Lino.FormPanel,{" % \
            dh.layout._formpanel_name
        yield "  layout: 'fit',"
        yield "  auto_save: true,"
        if dh.layout.window_size and dh.layout.window_size[1] == 'auto':
            yield "  autoHeight: true,"
        if settings.SITE.is_installed('contenttypes') and issubclass(tbl, dbtables.Table):
            yield "  content_type: %s," % py2js(ContentType.objects.get_for_model(tbl.model).pk)
        if not tbl.editable:
            yield "  disable_editing: true,"
        yield "  initComponent : function() {"
        # 20140503 yield "    var containing_panel = this;"
        # yield "// user profile: %s" % jsgen._for_user_profile
        lc = 0
        for ln in jsgen.declare_vars(dh.main):
            yield "    " + ln
            lc += 1
        if lc == 0:
            raise Exception("%r of %s has no variables" % (dh.main, dh))
        yield "    this.items = %s;" % dh.main.as_ext()
        #~ if issubclass(tbl,tables.AbstractTable):
        if True:
            yield "    this.before_row_edit = function(record) {"
            for ln in self.before_row_edit(dh.main):
                yield "      " + ln
            yield "    }"
        on_render = self.build_on_render(dh.main)
        if on_render:
            yield "    this.onRender = function(ct, position) {"
            for ln in on_render:
                yield "      " + ln
            yield "      Lino.%s.superclass.onRender.call(this, ct, position);" % \
                dh.layout._formpanel_name
            yield "    }"

        yield "    Lino.%s.superclass.initComponent.call(this);" % \
            dh.layout._formpanel_name

        # Seems that checkboxes don't emit a change event
        # when they are changed:
        # http://www.sencha.com/forum/showthread.php?43350-2.1-gt-2.2-OPEN-Checkbox-missing-the-change-event

        if dh.layout._formpanel_name.endswith('.DetailFormPanel'):
            if tbl.active_fields:
                yield '    // active_fields:'
                for name in tbl.active_fields:
                    e = dh.main.find_by_name(name)
                    if e is not None:
                        if True:  # see actions.ValidateForm
                            f = 'function(){ this.save() }'
                        else:
                            f = 'function(){ this.validate_form() }'
                        yield '    %s.on("%s", %s, this);' % (
                            py2js(e), e.active_change_event, f)
        yield "  }"
        yield "});"
        yield ""

    def js_render_detail_action_FormPanel(self, rh, action):
        rpt = rh.actor
        #~ logger.info('20121005 js_render_detail_action_FormPanel(%s,%s)',rpt,action.full_name(rpt))
        yield ""
        #~ yield "// js_render_detail_action_FormPanel %s" % action
        dtl = action.get_window_layout()
        if dtl is None:
            raise Exception("action %s without detail?" % action.full_name())
        yield "Lino.%sPanel = Ext.extend(Lino.%s,{" % (
            action.full_name(), dtl._formpanel_name)
        yield "  empty_title: %s," % py2js(action.get_button_label())
        if action.action.hide_navigator:
            yield "  hide_navigator: true,"

        if rh.actor.params_panel_hidden:
            yield "  params_panel_hidden: true,"

        if action.action.save_action_name is not None:
            yield "  save_action_name: %s," % py2js(
                action.action.save_action_name)
        yield "  ls_bbar_actions: %s," % py2js(
            self.toolbar(rpt.get_toolbar_actions(action.action)))
        yield "  ls_url: %s," % py2js(rpt.actor_url())
        if action.action != rpt.default_action.action:
            yield "  action_name: %s," % py2js(action.action.action_name)
        yield "  initComponent : function() {"
        a = rpt.detail_action
        if a:
            yield "    this.ls_detail_handler = Lino.%s;" % a.full_name()
        a = rpt.insert_action
        if a:
            yield "    this.ls_insert_handler = Lino.%s;" % a.full_name()

        yield "    Lino.%sPanel.superclass.initComponent.call(this);" \
            % action.full_name()
        yield "  }"
        yield "});"
        yield ""

    def js_render_GridPanel_class(self, rh):

        yield ""
        yield "// js_render_GridPanel_class %s" % rh.actor
        yield "Lino.%s.GridPanel = Ext.extend(Lino.GridPanel,{" % rh.actor

        kw = dict()
        #~ kw.update(empty_title=%s,rh.actor.get_button_label()
        kw.update(ls_url=rh.actor.actor_url())
        kw.update(ls_store_fields=[js_code(f.as_js(f.name))
                  for f in rh.store.list_fields])
        if rh.store.pk is not None:
            kw.update(ls_id_property=rh.store.pk.name)
            kw.update(pk_index=rh.store.pk_index)
            if settings.SITE.is_installed('contenttypes'):
                m = getattr(rh.store.pk, 'model', None)
                # e.g. pk may be the VALUE_FIELD of a choicelist which
                # has no model
                if m is not None:
                    ct = ContentType.objects.get_for_model(m).pk
                    kw.update(content_type=ct)

        kw.update(cell_edit=rh.actor.cell_edit)
        kw.update(ls_bbar_actions=self.toolbar(
            rh.actor.get_toolbar_actions(rh.actor.default_action.action)))
        kw.update(ls_grid_configs=[gc.data for gc in rh.actor.grid_configs])
        kw.update(gc_name=constants.DEFAULT_GC_NAME)
        #~ if action != rh.actor.default_action:
            #~ kw.update(action_name=action.name)
        #~ kw.update(content_type=rh.report.content_type)

        vc = dict(emptyText=_("No data to display."))
        if rh.actor.editable:
            vc.update(getRowClass=js_code('Lino.getRowClass'))
        if rh.actor.auto_fit_column_widths:
            vc.update(forceFit=True)
        if rh.actor.variable_row_height:
            vc.update(cellTpl=js_code("Lino.auto_height_cell_template"))
        if rh.actor.row_height != 1:
            kw.update(row_height=rh.actor.row_height)
            tpl = """new Ext.Template(
'<td class="x-grid3-col x-grid3-cell x-grid3-td-{id} {css}" style="{style}" tabIndex="0" {cellAttr}>',
'<div class="x-grid3-cell-inner x-grid3-col-{id}" unselectable="on" style="height:%dpx" {attr}>{value}</div>',
'</td>')""" % (rh.actor.row_height * 11)
            vc.update(cellTpl=js_code(tpl))

        kw.update(viewConfig=vc)

        if not rh.actor.editable:
            kw.update(disable_editing=True)
        if rh.actor.params_panel_hidden:
            kw.update(params_panel_hidden=True)

        if rh.actor.start_at_bottom:
            kw.update(start_at_bottom=True)
        kw.update(page_length=rh.actor.page_length)
        kw.update(stripeRows=True)

        #~ if rh.actor.master:
        kw.update(title=rh.actor.label)
        kw.update(
            disabled_actions_index=rh.store.column_index('disabled_actions'))

        for k, v in list(kw.items()):
            yield "  %s : %s," % (k, py2js(v))

        yield "  initComponent : function() {"

        a = rh.actor.detail_action
        if a:
            yield "    this.ls_detail_handler = Lino.%s;" % a.full_name()
        a = rh.actor.insert_action
        if a:
            yield "    this.ls_insert_handler = Lino.%s;" % a.full_name()

        yield "    var ww = this.containing_window;"
        for ln in jsgen.declare_vars(rh.list_layout.main.columns):
            yield "    " + ln

        yield "    this.before_row_edit = function(record) {"
        for ln in self.before_row_edit(rh.list_layout.main):
            yield "      " + ln
        yield "    };"

        on_render = self.build_on_render(rh.list_layout.main)
        if on_render:
            yield "    this.onRender = function(ct, position) {"
            for ln in on_render:
                yield "      " + ln
            yield "      Lino.%s.GridPanel.superclass.onRender.call(this, ct, position);" % rh.actor
            yield "    }"

        yield "    this.ls_columns = %s;" % py2js([
            ext_elems.GridColumn(rh.list_layout, i, e) for i, e
            in enumerate(rh.list_layout.main.columns)])

        yield "    Lino.%s.GridPanel.superclass.initComponent.call(this);" \
            % rh.actor
        yield "  }"
        yield "});"
        yield ""

    def js_render_custom_action(self, rh, action):
        """Defines the non-window action handler used by
        :meth:`row_action_button`
        """
        yield "Lino.%s = function(rp, pk, params) { " % action.full_name()
        yield "  var h = function() { "
        uri = rh.actor.actor_url()
        yield "    Lino.run_row_action(rp, %s, %s, pk, %s, params, %s);" % (
            py2js(uri), py2js(action.action.http_method),
            py2js(action.action.action_name),
            action.action.preprocessor)
        yield "  };"
        yield "  var panel = Ext.getCmp(rp);"
        yield "  if(panel) panel.do_when_clean(true, h); else h();"
        yield "};"

    def js_render_window_action(self, rh, ba, unused_profile):
        # x = str(rh)
        # if x.startswith('clocking'):
        #     print "20150421 {0}".format(x)
        # profile = jsgen.get_user_profile()
        rpt = rh.actor

        if rpt.parameters and ba.action.use_param_panel:
            params_panel = rh.params_layout_handle
        else:
            params_panel = None

        if isinstance(ba.action, ShowDetailAction):
            mainPanelClass = "Lino.%sPanel" % ba.full_name()
        elif isinstance(ba.action, InsertRow):
            mainPanelClass = "Lino.%sPanel" % ba.full_name()
        elif isinstance(ba.action, GridEdit):
            mainPanelClass = "Lino.%s.GridPanel" % rpt
        elif ba.action.parameters and not ba.action.no_params_window:
            params_panel = ba.action.make_params_layout_handle(
                settings.SITE.plugins.extjs)
        elif ba.action.extjs_main_panel:
            pass
        else:
            # print "20150421 {0}".format(rh)
            return

        windowConfig = dict()
        wl = ba.get_window_layout()
        ws = ba.get_window_size()
        #~ if wl is not None:
            #~ ws = wl.window_size
        if True:
            if ws:
                windowConfig.update(
                    maximized=False,
                    draggable=True,
                    maximizable=True,
                    modal=True)
                # if isinstance(ws[0], basestring) and ws[0].endswith("%"):
                #     windowConfig.update(
                #         width=js_code('Lino.perc2width(%s)' % ws[0][:-1]))
                if isinstance(ws[0], basestring):
                    windowConfig.update(width=ws[0])
                else:
                    windowConfig.update(
                        width=js_code('Lino.chars2width(%d)' % ws[0]))
                if ws[1] == 'auto':
                    windowConfig.update(autoHeight=True)
                elif isinstance(ws[1], int):
                    #~ windowConfig.update(height=ws[1])
                    windowConfig.update(
                        height=js_code('Lino.rows2height(%d)' % ws[1]))
                else:
                    raise ValueError("height")
                #~ print 20120629, action, windowConfig

        yield "Lino.%s = new Lino.WindowAction(%s, function(){" % (
            ba.full_name(), py2js(windowConfig))
        #~ yield "  console.log('20120625 fn');"
        if ba.action.extjs_main_panel:
            yield "  return %s;" % ba.action.extjs_main_panel
        else:
            p = dict()
            # if ba.action is settings.SITE.get_main_action(profile):
            #     p.update(is_home_page=True)
            if ba.action.hide_top_toolbar or ba.actor.hide_top_toolbar or ba.action.parameters:
                p.update(hide_top_toolbar=True)
            if rpt.hide_window_title:
                p.update(hide_window_title=True)

            p.update(is_main_window=True)  # workaround for problem 20111206
            yield "  var p = %s;" % py2js(p)
            if params_panel:
                if ba.action.parameters:
                    yield "  return new Lino.%s({});" % wl._formpanel_name
                else:
                    yield "  p.params_panel = new Lino.%s({});" % params_panel.layout._formpanel_name
                    yield "  return new %s(p);" % mainPanelClass
            else:
                yield "  return new %s(p);" % mainPanelClass
        yield "});"

    def linolib_intro(self):
        """
        Called from :xfile:`linolib.js`.
        """

        extjs = settings.SITE.plugins.extjs

        def fn():
            yield "// lino.js --- generated %s by %s for %s." % (
                time.ctime(), cgi.escape(settings.SITE.site_version()),
                jsgen.get_user_profile())
            # lino.__version__)
            #~ // $site.title ($lino.welcome_text())
            yield "Ext.BLANK_IMAGE_URL = '%s';" % extjs.build_lib_url(
                'resources/images/default/s.gif')
            yield "LANGUAGE_CHOICES = %s;" % py2js(
                list(settings.SITE.LANGUAGE_CHOICES))
            yield "MEDIA_URL = %s;" % py2js(settings.SITE.build_media_url())

        return '\n'.join(fn())
