# -*- coding: UTF-8 -*-
# Copyright 2009-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Defines the :class:`ExtRenderer` class.
"""

import logging ; logger = logging.getLogger(__name__)

from html import escape
import time

from django.conf import settings
from django.db import models
from django.utils import translation
from django.utils.translation import ugettext as _

from etgen.html import E, iselement

import lino
from lino.core import constants
from lino.core.renderer import JsRenderer
from lino.core.renderer_mixins import JsCacheRenderer
from lino.core.gfks import ContentType

from lino.core.actions import (ShowEmptyTable, ShowDetail,
                               ShowInsert, ShowTable, SubmitDetail,
                               SubmitInsert)
from lino.core import dbtables
from lino.core import kernel
from lino.core import tables

from lino.utils import AttrDict
from lino.core import choicelists
from lino.core import menus
# from lino.core import auth
from lino.utils import jsgen
from lino.utils.jsgen import py2js, js_code
from lino.api import rt
from lino.api.ad import Plugin

from lino.modlib.users.utils import get_user_profile, with_user_profile

if False:
    from lino.utils.jscompressor import JSCompressor
    jscompress = JSCompressor().compress
else:
    def jscompress(s):
        return s

from lino.core import elems as ext_elems


# if settings.SITE.user_model:
#     from lino.modlib.users import models as users

# ONE_CHAR_LABEL = "\u00A0{}\u00A0"
# ONE_CHAR_LABEL = "<font size=\"4\">\u00A0{}\u00A0</font>"
ONE_CHAR_LABEL = " <font size=\"4\">{}</font>"

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



class ExtRenderer(JsRenderer, JsCacheRenderer):
    """An HTML renderer that uses the ExtJS Javascript toolkit.

    """
    is_interactive = True
    # is_prepared = False

    extjs_version = 3

    def __init__(self, plugin):
        super(ExtRenderer, self).__init__(plugin)
        JsCacheRenderer.__init__(self)
        jsgen.register_converter(self.py2js_converter)

        for s in 'green blue red yellow'.split():
            self.row_classes_map[s] = 'x-grid3-row-%s' % s

        self.prepare_layouts()

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
                # h = self.instance_handler(None, v.instance, None)
                h = self.instance_handler(None, v.instance, v.bound_action)
                # 20190501 not passing the v.bound_action seems an obvious bug,
                # though there is probably no use case where the bug was visible

                assert h is not None
                # print(20190430, h)
                js = "function() {%s}" % h
                return self.handler_item(v, js, None)
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

    def action_button(self, obj, ar, ba, label=None, **kw):
        label = label or ba.get_button_label()
        if len(label) == 1:
            label = "\u00A0{}\u00A0".format(label)
            # label = ONE_CHAR_LABEL.format(label)
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

    def is_custom_action(self, a):
        if a.parameters and not a.no_params_window:
            return False
        if a.opens_a_window:
            return False
        if not a.action_name:
            return False
        return True

    @staticmethod
    def actions_hotkeys2js(actions_hotkeys):

        for action_hotkeys in actions_hotkeys:
            js_action = """Lino.row_action_handler('{}', 'GET', null)""".format(action_hotkeys.get('ba'))
            action_hotkeys.update({
                'ba':js_action
            })
        return actions_hotkeys


    def window_action_button(
            self, ar, ba, status=None,
            label=None, title=None, **kw):
        """Return a HTML chunk for a button that will execute this action
        using a Javascript link to this action.

        """
        label = str(label or ba.get_button_label())
        uri = self.js2url(self.action_call(ar, ba, status or {}))
        return self.href_button_action(
            ba, uri, label, title or ba.action.help_text, **kw)

    def quick_manage_toolbar(self, ar, obj):
        """Returns a HTML chunk that displays a "toolbar" with a series of
        "quick manage buttons": one "Insert" and another to open the
        table.

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

        Any other keyword arguments are forwarded to :meth:`ar2js`.

        """
        if ar is None:
            sar = ba.request(**request_kwargs)
        else:

            sar = ar.spawn(ba, **request_kwargs)
        return self.ar2js(sar, obj, **status)

    def request_handler(self, ar, *args, **kw):
        st = ar.get_status(**kw)
        return self.action_call(ar, ar.bound_action, st)

    def action_call(self, ar, bound_action, status):
        a = bound_action.action
        if a.opens_a_window or (a.parameters and not a.no_params_window):
            if ar and ar.subst_user:
                status[constants.URL_PARAM_SUBST_USER] = ar.subst_user
            if isinstance(a, ShowEmptyTable):
                status.update(record_id=-99998)
            if ar is None:
                rp = None
            else:
                rp = ar.requesting_panel
            if status:
                return "Lino.%s.run(%s,%s)" % (
                    bound_action.full_name(),
                    py2js(rp),
                    py2js(status))
            return "Lino.%s.run(%s)" % (bound_action.full_name(), py2js(rp))
        # raise Exception("20180620 {}".format(bound_action))

        # used e.g. the invoicing.StartInvoicing action (visible in
        # roger or lydia).
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

    def get_actor_url(self, actor, *args, **kw):
        return self.front_end.build_plain_url(
            "api",
            actor.app_label, actor.__name__, *args, **kw)

    def get_home_url(self, *args, **kw):
        return self.front_end.build_plain_url(*args, **kw)

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
        return self.front_end.build_plain_url(
            'api', ar.actor.app_label, ar.actor.__name__, *args, **kw)

    # def show_table(
    #         self, ar, stripped=True, nosummary=False, **kw):
    #     """
    #     Returns a HTML element representing this request as a table.
    #     Used by appy_pod renderer.
    #     """
    #     if ar.actor.master is not None and not nosummary:
    #         if ar.actor.display_mode == 'summary':
    #             return ar.actor.get_table_summary(ar.master_instance, ar)
    #     return ar.table2xhtml(**kw)

    def handler_item(self, mi, handler, help_text):
        #~ handler = "function(){%s}" % handler
        #~ d = dict(text=prepare_label(mi),handler=js_code(handler),tooltip="Foo")
        d = dict(text=prepare_label(mi), handler=js_code(handler))
        if mi.bound_action and mi.bound_action.action.icon_name:
            d.update(iconCls='x-tbar-' + mi.bound_action.action.icon_name)
        # if help_text:
        #     d.update(tooltip=help_text, tooltipType='title')
        # 20200429 seems that tooltipType 'title' doesn't work on menu items
        if settings.SITE.use_quicktips and help_text:
            d.update(listeners=dict(render=js_code(
                "Lino.quicktip_renderer(%s,%s)" % (
                    py2js('Foo'), py2js(help_text)))
            ))
        return d

    def html_text(self, html):
        """
        Wrap the given html fragment into a ``<div class="htmlText">``
        which specifies that this fragment contains simple html text
        inside an ExtJS component.  This is required because ExtJS
        does a lot of CSS magic which neutralizes the "usual" effects
        of most html tags.
        """
        if isinstance(html, str):
            return '<div class="htmlText">{0}</div>'.format(html)
        if not iselement(html):
            raise Exception("{!r} is not an element".format(html))
        if html.tag in ('div', 'span'):
            html.set('class', 'htmlText')
            return html
        return E.div(html, **{'class': 'htmlText'})
        # # is a list or tuple of ET elements
        # return E.div(*html, class_='htmlText')

    def html_page(self, request, *args, **kw):
        """Return a string with the index page.  Content is mostly in the
        :xfile:`extjs/index.html` template.

        """
        user = request.user
        # print 20150427, user
        if True:  # user.user_type.level >= UserLevels.admin:
            if request.subst_user:
                user = request.subst_user

        def getit():
            if not settings.SITE.build_js_cache_on_startup:
                self.build_js_cache(False)

            # Render template
            env = settings.SITE.plugins.jinja.renderer.jinja_env
            tpl = env.get_template('extjs/index.html')
            context = {
                'site': settings.SITE,
                'extjs': self.front_end,
                'ext_renderer': self,
                'py2js': py2js,  # TODO: Should be template filter
                'jsgen': jsgen,  # TODO: Should be in filters
                'language': translation.get_language(),
                'request': request,
                'user': user,  # Current user
            }
            context.update(kw)
            return tpl.render(context)

        return with_user_profile(user.user_type, getit)

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
            html = site.get_main_html(request, extjs=self.front_end)
            html = self.html_text(html)
            dashboard.update(html=html)

        win = dict(
            layout='fit',
            #~ maximized=True,
            items=main,
            #~ closable=False,
            bbar=dict(xtype='toolbar', items=js_code('Lino.status_bar')),
            #~ title=self.site.title,
            tbar=js_code('Lino.main_menu'),
            tbarCfg={"cls": "l-mainmenu"}
        )
        return win

    def html_page_user(self, request, site):
        """Build the "user menu", i.e. the menu in the top right corner.
        """
        if settings.SITE.user_model is not None:
            if request.user.is_authenticated:
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

                a = rt.models.users.MySettings.default_action
                handler = self.action_call(None, a, dict(record_id=user.pk))
                handler = "function(){%s}" % handler
                mysettings = dict(text=_("My settings"),
                                  handler=js_code(handler))
                login_menu_items = [mysettings]

                authorities = user.get_authorities()
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
                    # 20170921
                    a = rt.models.users.MySettings.get_action_by_name('sign_out')
                    # a = user.sign_out.bound_action
                    js = self.action_call(None, a, {})
                    js = "function(){%s}" % js
                    login_menu_items.append(
                        dict(text=a.get_button_label(), handler=js_code(js)))
                # the following was never used
                #     if auth.get_auth_middleware().can_change_password(request, request.user):
                #         login_menu_items.append(
                #             dict(text=_("Change password"), handler=js_code('Lino.change_password')))
                #         login_menu_items.append(
                #             dict(text=_("Forgot password"), handler=js_code('Lino.forgot_password')))

                login_menu = dict(
                    text=user_text,
                    menu=dict(items=login_menu_items))

                yield "Lino.main_menu = Lino.main_menu.concat(['->',%s]);" % py2js(login_menu)

            else:
                ba = rt.models.users.UsersOverview.get_action_by_name('sign_in')
                js = self.action_call(None, ba, {})
                js = "function(){%s}" % js
                login_buttons = [ dict(
                    xtype="button", text=ba.get_button_label(),
                    handler=js_code(js)) ]
                # login_buttons = [
                #     dict(xtype="button", text=_("Log in"),
                #          handler=js_code('Lino.show_login_window')),
                #     #~ dict(xtype="button",text="Register",handler=Lino.register),
                # ]
                yield "Lino.main_menu = \
                Lino.main_menu.concat(['->', %s]);" % py2js(login_buttons)

    def before_row_edit(self, panel):
        from lino.core.actions import get_view_permission
        #~ l.append("console.log('before_row_edit',record);")
        for e in panel.active_children:
            if not get_view_permission(e):
                continue
            for p in settings.SITE.installed_plugins:
                for ln in p.get_row_edit_lines(e, panel):
                    yield ln

    def write_lino_js(self, f):

        user_type = get_user_profile()

        context = dict(
            ext_renderer=self,
            site=settings.SITE,
            settings=settings,
            lino=lino,
            language=translation.get_language(),
            # ext_requests=constants,
            constants=constants,
            extjs=self.front_end,  # 20171227
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

        menu = settings.SITE.get_site_menu(user_type)
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
            if a.default_action.get_view_permission(user_type)]

        # Define every choicelist as a JS array:
        f.write("\n// ChoiceLists: \n")
        for a in kernel.CHOICELISTS.values():
            # if settings.SITE.is_installed(a.app_label):
            f.write("Lino.%s = %s;\n" %
                    (a.actor_id, py2js(a.get_choices())))

        #~ logger.info('20120120 dbtables.all_details:\n%s',
            #~ '\n'.join([str(d) for d in dbtables.all_details]))

        assert user_type == get_user_profile()

        def must_render(lh, user_type):
            """
            Return True if the given form layout `fl` is needed for
            user_type.
            """
            if not lh.main.get_view_permission(user_type):
                return False
            if lh.layout._datasource.get_view_permission(user_type):
                return True
            for ds in lh.layout._other_datasources:
                if ds.get_view_permission(user_type):
                    return True
            return False

        #~ f.write('\n/* Application FormPanel subclasses */\n')
        for fl in self.param_panels:
            lh = fl.get_layout_handle(self.front_end)
            if must_render(lh, user_type):
                for ln in self.js_render_ParamsPanelSubclass(lh):
                    f.write(ln + '\n')

        for fl in self.action_param_panels:
            lh = fl.get_layout_handle(self.front_end)
            if must_render(lh, user_type):
                for ln in self.js_render_ActionFormPanelSubclass(lh):
                    f.write(ln + '\n')

        assert user_type == get_user_profile()

        for fl in self.form_panels:
            lh = fl.get_layout_handle(self.front_end)
            if must_render(lh, user_type):
                for ln in self.js_render_FormPanelSubclass(lh):
                    f.write(ln + '\n')

        actions_written = set()
        for rpt in actors_list:
            rh = rpt.get_handle()
            for ba in rpt.get_actions():
                if ba.action.parameters:
                    if ba.action not in actions_written:
                        actions_written.add(ba.action)
                        for ln in self.js_render_window_action(rh, ba):
                            f.write(ln + '\n')

        for rpt in actors_list:
            # x = str(rpt)
            # if x == 'working.WorkedHours':
            #     raise Exception("20180803 {0}".format(x))

            rh = rpt.get_handle()
            if isinstance(rpt, type) and issubclass(rpt, (
                    tables.AbstractTable, choicelists.ChoiceList)):
                for ln in self.js_render_GridPanel_class(rh):
                    f.write(ln + '\n')

                # 20180518 There is more useless JS code in the
                # :file:`lino_XXX_yy.js` file : for example (in team)
                # it generates a GridPanel and related functions for
                # `Lino.countries.PlaceTypes`.  This table is never
                # used because there is no menu item for it.  We might
                # extend the code which decides whether
                # :meth:`js_render_GridPanel_class` must be called or
                # not.  The condition would be: if it is a master
                # table but does not have any menu item.  But that
                # might be dangerous (cause uncovered regressions), so
                # I prefer to leave this for another time.

            window_actions = [ba.action for ba in rpt.get_actions() if
                              ba.action.opens_a_window]
            for ba in rpt.get_actions():
                if ba.action.parameters and not ba.action.no_params_window:
                    pass
                elif ba.action.opens_a_window:
                    if isinstance(ba.action, (ShowDetail,
                                              ShowInsert)):
                        for ln in self.js_render_detail_action_FormPanel(
                                rh, ba):
                            f.write(ln + '\n')
                    for ln in self.js_render_window_action(rh, ba):
                        f.write(ln + '\n')
                # elif self.is_custom_action(ba.action):
                elif ba.action.action_name:
                    is_custom = False
                    for parent in window_actions:
                        if ba.action.is_callable_from(parent):
                            is_custom = True
                            break
                    if is_custom:
                        for ln in self.js_render_custom_action(rh, ba):
                            f.write(ln + '\n')

        if user_type != get_user_profile():
            logger.warning(
                "Oops, user_type %s != get_user_profile() %s",
                user_type, get_user_profile())

        return 1

    def toolbar(self, action_list):
        """
        This also manages action groups
        """
        user_type = get_user_profile()
        buttons = []
        combo_map = dict()
        for ba in action_list:

            if ba.action.show_in_bbar and ba.get_view_permission(user_type):
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
        elif isinstance(a, ShowDetail):
            kw.update(panel_btn_handler=js_code('Lino.show_detail'))
        elif isinstance(a, ShowInsert):
            kw.update(panel_btn_handler=js_code('Lino.show_insert'))
        else:
            kw.update(
                panel_btn_handler=js_code(self.get_panel_btn_handler(ba)))

        if a.icon_name:
            kw.update(iconCls='x-tbar-' + a.icon_name)
        else:
            txt = a.button_text or a.get_label()
            if len(txt) == 1:
                txt = ONE_CHAR_LABEL.format(txt)

            kw.update(text=txt)
        kw.update(
            #~ name=a.name,
            menu_item_text=a.get_label(),
            overflowText=a.get_label(),
            auto_save=a.auto_save,
            itemId=a.action_name,
            #~ text=unicode(a.label),
        )
        if a.key:
            kw.update(keycode=a.key.keycode)

        if a.help_text:
            # if a.__class__.__name__ in ('ChangePassword', 'SubmitDetail'):
            #     logger.info("20160829 a2btn() %r %r", a, str(a.help_text))

            # A tooltip becomes visible only on buttons with an
            # iconCls. On a button which has only text we must use
            # Lino.quicktip_renderer. But I didn't find out why this
                # doesn't seem to work.
            kw.update(tooltip=a.help_text, tooltipType='title')
            # if not a.icon_name:
            #     kw.update(tooltipType='title')
            #    kw.update(listen   ers=dict(render=js_code(
            #        "Lino.quicktip_renderer('a2btn',%s)" %
            #        py2js(a.help_text))
            #    ))
        elif a.icon_name:
            kw.update(tooltip=a.get_label(), tooltipType='title')
        return kw

    def build_on_render(self, main):
        "dh is a FormLayout or a ColumnsLayout"
        user_type = get_user_profile()
        on_render = []
        elems_by_field = {}
        field_elems = []
        for e in main.active_children:
            if isinstance(e, ext_elems.FieldElement):
                if e.get_view_permission(user_type):
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
                            "typeof %s !== 'undefined' && %s.on('change',Lino.chooser_handler(%s,'%s'));" % (
                                el.as_ext(), el.as_ext(), e.as_ext(), f.name))
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
        # 20191121 yield "  ls_url: %s," % py2js(dh.layout._url)
        yield "  window_title: %s," % py2js(tbl.label)
        # if not tbl.select_rows:
        #     yield "  default_record_id: -99999,"

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
        yield "    this.http_method = %s" % py2js(tbl.http_method)
        yield "    Lino.%s.superclass.initComponent.call(this);" % \
            dh.layout._formpanel_name
        yield "  }"
        yield "});"
        yield ""

    def js_render_FormPanelSubclass(self, dh):

        tbl = dh.layout._datasource
        if not dh.main.get_view_permission(get_user_profile()):
            msg = "No view permission for main panel of %s :" % \
                  dh.layout._formpanel_name
            msg += " main requires %s (actor %s requires %s)" % (
                dh.main.required_roles,
                tbl, tbl.required_roles)
            #~ raise Exception(msg)
            logger.warning(msg)
            # print(20150717, msg)
            return

        yield ""
        yield "Lino.%s = Ext.extend(Lino.FormPanel,{" % \
              dh.layout._formpanel_name

        if dh.layout._formpanel_name.endswith('.DetailFormPanel'):
            yield "cls: %s," % py2js("l-DetailFormPanel " + tbl.actor_id.replace(".", "-"))
        if dh.layout._formpanel_name.endswith('.InsertFormPanel'):
            yield "cls: %s," % py2js("l-InsertFormPanel " + tbl.actor_id.replace(".", "-"))
        if dh.layout._formpanel_name.endswith('.ParamsPanel'):
            yield "cls: %s," % py2js("l-ParamsPanel " + tbl.actor_id.replace(".", "-"))
        if dh.layout._formpanel_name.endswith('_ActionFormPanel'):
            yield "cls: %s," % py2js("l-ActionFormPanel " + tbl.actor_id.replace(".", "-"))

        yield "  layout: 'fit',"
        yield "  auto_save: true,"
        hotkeys = tbl.get_actions_hotkeys()
        if hotkeys:
            yield "  actions_hotkeys: %s," % py2js(self.actions_hotkeys2js(hotkeys))
        if dh.layout.window_size and dh.layout.window_size[1] == 'auto':
            yield "  autoHeight: true,"
        if settings.SITE.is_installed('contenttypes') and issubclass(tbl, dbtables.Table):
            yield "  content_type: %s," % py2js(ContentType.objects.get_for_model(tbl.model).pk)
        if not tbl.editable:
            yield "  disable_editing: true,"
        if not tbl.auto_apply_params:
            yield "  auto_apply_params: false,"
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
        if isinstance(action.action, ShowInsert):
            yield "  default_record_id: -99999,"

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
        if getattr(rh.actor,'use_detail_params_value',None):
            kw.update(use_detail_params_value=True)
        kw.update(ls_url=rh.actor.actor_url())
        if not hasattr(rh, 'store'):
            raise AttributeError("20200128 {} has no store".format(rh))
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
        kw.update(focus_on_quick_search=rh.actor.focus_on_quick_search)
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
        if rh.actor.editable:
            kw.update(
                disabled_fields_index=rh.store.column_index('disabled_fields'))

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
        if not hasattr(rh, 'list_layout'):
            raise AttributeError("20200128 {} has no list_layout".format(rh))
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
        yield "Lino.%s = function(rp, is_main, pk, params) { " % action.full_name()
        yield "  var h = function() { "
        uri = rh.actor.actor_url()
        yield "    Lino.run_row_action(rp, is_main, %s, %s, pk, %s, params, %s);" % (
            py2js(uri), py2js(action.action.http_method),
            py2js(action.action.action_name),
            action.action.preprocessor)
        yield "  };"
        yield "  var panel = Ext.getCmp(rp);"
        yield "  if(panel && !params.rqdata) panel.do_when_clean(true, h); else h();"
        yield "};"

    def js_render_window_action(self, rh, ba):
        rpt = rh.actor
        # x = str(rpt)
        # if x == 'working.WorkedHours':
        #     raise Exception("20180803 {0}".format(x))

        if rpt.parameters and ba.action.use_param_panel:
            params_panel = rh.params_layout_handle
        else:
            params_panel = None

        if isinstance(ba.action, ShowDetail):
            mainPanelClass = "Lino.%sPanel" % ba.full_name()
        elif isinstance(ba.action, ShowInsert):
            mainPanelClass = "Lino.%sPanel" % ba.full_name()
        elif isinstance(ba.action, ShowTable):
            mainPanelClass = "Lino.%s.GridPanel" % rpt
        elif ba.action.parameters and not ba.action.no_params_window:
            params_panel = ba.action.make_params_layout_handle()
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
                if isinstance(ws[0], str):
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
            p.update(ls_url=ba.actor.actor_url())  # 20191121
            yield "  var p = %s;" % py2js(p)
            if params_panel:
                if ba.action.parameters:
                    yield "  return new Lino.%s(p);" % wl._formpanel_name
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

        # extjs = settings.SITE.plugins.extjs
        extjs = self.front_end

        def fn():
            yield "// lino.js --- generated %s by %s for %s." % (
                time.ctime(), escape(settings.SITE.site_version()),
                get_user_profile())
            # lino.__version__)
            #~ // $site.title ($lino.welcome_text())
            if self.extjs_version == 3:
                yield "Ext.BLANK_IMAGE_URL = '%s';" % extjs.build_lib_url(
                    'resources/images/default/s.gif')
            yield "LANGUAGE_CHOICES = %s;" % py2js(
                list(settings.SITE.LANGUAGE_CHOICES))
            yield "MEDIA_URL = %s;" % py2js(settings.SITE.build_media_url())
            yield "GEN_TIMESTAMP = %s;" % py2js(rt.settings.SITE.kernel.code_mtime)

        return '\n'.join(fn())
