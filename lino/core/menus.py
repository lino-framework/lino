# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Defines the classes :class:`MenuItem`
"""

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.db import models

from atelier import rstgen
from lino.core.dbutils import obj2str


from lino.core import actors
from lino.core import actions
from lino.utils.xmlgen import html as xghtml
E = xghtml.E


class MenuItem:

    """
    Represents a menu item
    """
    HOTKEY_MARKER = '~'

    name = None
    parent = None

    def __init__(self,
                 name=None, label=None, doc=None, enabled=True,
                 action=None,
                 #~ can_view=None,
                 hotkey=None,
                 params={},
                 help_text=None,
                 #~ request=None,
                 instance=None,
                 javascript=None,
                 href=None):
        if action is None:
            pass
            #~ if instance is not None:
                #~ action = instance.get_default_table().default_action
        elif not isinstance(action, actors.BoundAction):
            raise Exception("20121003 not a BoundAction: %r" % action)
        if instance is not None:
            if action is None:
                raise Exception("20130610")
            instance._detail_action = action
        self.bound_action = action
        self.params = params
        self.href = href
        #~ self.request = request
        self.instance = instance
        self.javascript = javascript
        self.help_text = help_text

        if label is None:
            if instance is not None:
                label = unicode(instance)
            elif action is not None:
                label = action.get_button_label()

        if name is not None:
            self.name = name
        self.doc = doc
        self.enabled = enabled
        self.hotkey = hotkey

        if label:
            label = label.replace('~', '')
        self.label = label

        #~ if self.label is None:
            #~ raise Exception("20130907 %r has no label" % self)

    def compress(self):
        pass

    def getLabel(self):
        return self.label

    def getDoc(self):
        return self.doc

    def walk_items(self):
        yield self

    def __repr__(self):
        s = self.__class__.__name__ + "("
        attrs = []
        for k in 'label instance bound_action href params name'.split():
            v = getattr(self, k)
            if v is not None:
                attrs.append(k + "=" + obj2str(v))
        s += ', '.join(attrs)
        return s + ")"

    #~ def interesting(self,**kw):
        #~ l = []
        #~ if self.label is not None:
            #~ l.append(('label',self.label.strip()))
        #~ if not self.enabled:
            #~ l.append( ('enabled',self.enabled))
        #~ return l

    #~ def parents(self):
        #~ l = []
        #~ p = self.parent
        #~ while p is not None:
            #~ l.append(p)
            #~ p = p.parent
        #~ return l

    def get_url_path(self):
        if self.action:
            return str(self.action)
        if self.parent:
            s = self.parent.get_url_path()
            if len(s) and not s.endswith("/"):
                s += "/"
        else:
            s = '/'
        if self.name:
            return s + self.name
        return s

    def as_bootstrap_html(self, renderer, request, level=None):
        if self.bound_action:
            assert renderer is not None
            sr = self.bound_action.actor.request(
                action=self.bound_action,
                user=request.user, subst_user=request.subst_user,
                requesting_panel=request.requesting_panel,
                renderer=renderer, **self.params)

            url = sr.get_request_url()
        else:
            url = self.href
        assert self.label is not None
        if url is None:
            return E.p()  # spacer
        return E.li(E.a(self.label, href=url, tabindex="-1"))

    def as_rst(self, ar, level=None):
        """
        Render this menu item as an rst string.
        Currently used only for writing test cases.
        """
        #~ if self.bound_action:
            #~ sr = self.bound_action.actor.request(
                #~ action=self.bound_action,
                #~ user=request.user,subst_user=request.subst_user,
                #~ requesting_panel=request.requesting_panel,
                #~ renderer=ui.plain_renderer,**self.params)
          #~
            #~ url = sr.get_request_url()
        #~ else:
            #~ url = self.href
        #~ assert self.label is not None
        #~ if url is None:
            # ~ return E.p() # spacer
        #~ return E.li(E.a(self.label,href=url,tabindex="-1"))
        return unicode(self.label)


def has_items(menu):
    for i in menu.items:
        if i.label is None:
            raise Exception("20130907 %r has no label" % i)
        if not i.label.startswith('-'):
            return True
    return False


def create_item(spec, action=None, help_text=None, **kw):
    """
    """
    givenspec = spec
    if isinstance(spec, basestring):
        spec = settings.SITE.modules.resolve(spec)
        #~ if a is None:
            #~ raise Exception("Could not resolve action specifier %r" % spec)
    if isinstance(spec, actors.BoundAction):
        a = spec
    else:
        if isinstance(spec, type) and issubclass(spec, models.Model):
            spec = spec.get_default_table()
            assert spec is not None

        if isinstance(spec, type) and issubclass(spec, actors.Actor):
            if action:
                a = spec.get_url_action(action)
                #~ print 20121210, a
                if a is None:
                    raise Exception("add_action(%r,%r,%r) found None" %
                                    (spec, action, kw))
            else:
                a = spec.default_action
                if a is None:
                    raise Exception("%r default_action is None?!" % spec)
        else:
            raise Exception("Action spec %r returned invalid object %r" %
                            (givenspec, spec))

    #~ if kw.has_key('params'):
        #~ if a.actor.__name__ == 'Contacts':
          #~ raise Exception("20120103")
    if help_text is None:
        if a == a.actor.default_action:
            help_text = a.actor.help_text or a.action.help_text
        else:
            help_text = a.action.help_text
    if help_text is not None:
        kw.update(help_text=help_text)
    kw.update(action=a)
    return MenuItem(**kw)


class Menu(MenuItem):

    """
    Represents a menu. A menu is conceptually a :class:`MenuItem` 
    which contains other menu items.
    """

    avoid_lonely_items = False
    """
    If set to True, avoid lonely menu items by lifting them up one level.
    This is not done for top-level menus
    
    For example the following menu::
        
        Foo           Bar         Baz
        |Foobar       |BarBaz
         |Copy
         |Paste
        |FooBarBaz
         | Insert
         
    would become::
         
        Foo           BarBaz        Baz
        |Foobar       
         |Copy
         |Paste
        |Insert
         
    
    """

    def __init__(self, user_profile, name, label=None, parent=None, **kw):
        MenuItem.__init__(self, name, label, **kw)
        self.parent = parent
        self.user_profile = user_profile
        self.clear()

    def clear(self):
        self.items = []
        self.items_dict = {}

    def compress(self):
        """
        Dynamically removes empty menu entries.
        Collapses menu with only one item into their parent.
        """
        for mi in self.items:
            mi.compress()

        newitems = []

        for mi in self.items:
            if isinstance(mi, Menu):
                if has_items(mi):
                    if not self.avoid_lonely_items:
                        newitems.append(mi)
                    elif len(mi.items) == 1:
                        if not mi.items[0].label.startswith('-'):
                            if self.parent is None:
                                newitems.append(mi)
                            else:
                                newitems.append(mi.items[0])
                    elif len(mi.items) > 1:
                        newitems.append(mi)
            else:
                newitems.append(mi)

        self.items = newitems

    def add_action(self, *args, **kw):
        mi = create_item(*args, **kw)
        return self.add_item_instance(mi)

    #~ def add_action_(self,action,**kw):
        #~ return self.add_item_instance(MenuItem(self,action,**kw))

    #~ def add_item(self,**kw):
        #~ return self.add_item_instance(Action(self,**kw))

    #~ def add_request_action(self,ar,**kw):
        #~ kw.update(request=ar)
        #~ return self.add_item_instance(MenuItem(self,ar.action,**kw))

    def add_instance_action(self, obj, **kw):
        """
        Add an action which displays the given object (a Django model instance)
        in a detail form for editing.
        Used e.g. for the SiteConfig object.
        """
        kw.update(instance=obj)
        da = kw.get('action', None)
        if da is None:
            da = obj.get_default_table().detail_action
            kw.update(action=da)
        #~ obj._detail_action = da
        return self.add_item_instance(MenuItem(**kw))

    def add_item(self, name, label, **kw):
        return self.add_item_instance(MenuItem(name, label, **kw))

    def add_separator(self, label='-', **kw):
        if len(self.items) > 0 and not self.items[-1].label.startswith('-'):
            return self.add_item_instance(MenuItem(None, label, **kw))

    def add_menu(self, name, label, **kw):
        return self.add_item_instance(Menu(
            self.user_profile, name, label, self, **kw))

    def get_item(self, name):
        return self.items_dict[name]

    #~ def add_url_button(self,url,label):
    def add_url_button(self, url, **kw):
        kw.update(href=url)
        return self.add_item_instance(MenuItem(**kw))
        #~ self.items.append(dict(
          #~ xtype='button',text=label,
          #~ handler=js_code("function() {window.location='%s';}" % url)))

    def add_item_instance(self, mi):
        """
        Adds the specified MenuItem to this menu after checking whether
        it has view permission.
        """
        assert isinstance(mi, MenuItem)
        mi.parent = self
        if mi.bound_action is not None:
            #~ if not mi.bound_action.actor.get_view_permission(self.user):
            if not mi.bound_action.get_view_permission(self.user_profile):
                return
            #~ logger.info("20130129 _add_item %s for %s",mi.label,self.user_profile)
        if mi.name is not None:
            old = self.items_dict.get(mi.name)
            if old is not None:
                if mi.label != old.label:
                    raise Exception(
                        "Menu item %r labelled %s cannot override existing label %s" %
                        (mi.name, mi.label, old.label))
                return old
            self.items_dict[mi.name] = mi
        self.items.append(mi)
        return mi

    #~ def get(self,name):
        #~ return self.items_dict.get(name)

    def walk_items(self):
        yield self
        for mi in self.items:
            for i in mi.walk_items():
                yield i

    #~ def unused_sort_items(self,front=None,back=None):
        #~ new_items = []
        #~ if front:
            #~ for name in front.split():
                #~ new_items.append(self.findItem(name))
        #~ back_items = []
        #~ if back:
            #~ for name in back.split():
                #~ back_items.append(self.findItem(name))
        #~ for i in self.get_items():
            #~ if not i in new_items + back_items:
                #~ new_items.append(i)
        #~ self.items = new_items + back_items
        #~ self.items_dict = {}
        #~ for i in self.items:
            #~ self.items_dict[i.name] = i

    def as_bootstrap_html(self, renderer, request, level=1):
        items = [mi.as_bootstrap_html(renderer, request, level + 1)
                 for mi in self.items]
        #~ print 20120901, items
        if level == 1:
            return E.ul(*items, class_='nav navbar-nav')
        if self.label is None:
            raise Exception("%s has no label" % self)
        if level == 2:
            cl = 'dropdown'
            menu_title = E.a(
                unicode(self.label), E.b(' ', class_="caret"), href="#",
                class_='dropdown-toggle', data_toggle="dropdown")
        elif level == 3:
            menu_title = E.a(unicode(self.label), href="#")
            cl = 'dropdown-submenu'
        else:
            raise Exception("Menu with more than three levels")
        return E.li(
            menu_title,
            E.ul(*items, class_='dropdown-menu'),
            class_=cl)

    def as_rst(self, ar, level=1):
        """
        Render this menu as an rst string.
        Currently used only for writing test cases.
        """
        has_submenus = False
        for i in self.items:
            if isinstance(i, Menu):
                has_submenus = True
        items = [mi.as_rst(ar, level + 1) for mi in self.items]
        if has_submenus:
            s = rstgen.ul(items).strip() + '\n'
            if self.label is not None:
                s = unicode(self.label) + ' :\n\n' + s
        else:
            s = ', '.join(items)
            if self.label is not None:
                s = unicode(self.label) + ' : ' + s
        return s


class Toolbar(Menu):

    """
    A Toolbar is a top-level :class:`Menu`.
    """
    pass


def find_menu_item(spec):
    from django.conf import settings
    from lino import dd
    profile = dd.modules.users.UserProfiles.get_by_value('900')
    menu = settings.SITE.get_site_menu(settings.SITE.ui, profile)
    for mi in menu.walk_items():
        if mi.bound_action == spec:
            return mi
    return None
