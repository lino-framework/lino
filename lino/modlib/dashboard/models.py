# -*- coding: UTF-8 -*-
# Copyright 2011-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Database models for this plugin.


"""
from builtins import object

from django.db import models
from django.conf import settings

from lino.api import dd, rt, _
from lino.core.roles import SiteAdmin
from lino.core.userprefs import get_available_items

from lino.mixins import Sequenced

from lino.modlib.users.mixins import UserAuthored


class UpdateWidgets(dd.Action):
    """Create or update the dashboard widgets for this user.

    This is installed as :attr:`update_widgets` on :class:`Widget`.

    """
    label = _('Update widgets')
    button_text = ' ⚡ '  # 26A1
    # icon_name = 'lightning'

    def get_action_permission(self, ar, obj, state):
        me = ar.get_user()
        if not me.user_type.has_required_roles([SiteAdmin]):
            if obj != me:
                return False
        return super(UpdateWidgets, self).get_action_permission(
            ar, obj, state)

    def run_from_ui(self, ar):
        for obj in ar.selected_rows:
            update_widgets_for(ar, obj)

dd.inject_action('users.User', update_widgets=UpdateWidgets())



class Widget(UserAuthored, Sequenced):
    """
    """

    move_action_names = ('move_up', 'move_down')
    
    class Meta(object):
        app_label = 'dashboard'
        verbose_name = _("Widget")
        verbose_name_plural = _("Widgets")

    item_name = models.CharField(_("Resource"), max_length=200)
    visible = models.BooleanField(_("Visible"), default=True)

    
    @dd.chooser(simple_values=True)
    def item_name_choices(cls, user):
        return [i.name for i in
                settings.SITE.get_dashboard_items(user)]

    def __str__(self):
        return self.item_name

    def get_siblings(self):
        qs = super(Widget, self).get_siblings()
        return qs.filter(user=self.user)
    
    @dd.displayfield(_("Label"))
    def title(self, ar):
        a = settings.SITE.models.resolve(self.item_name)
        # might be invalid e.g. if the widget was created by a
        # previous version.
        if a is None:
            return _("Invalid item_name {} in {}").format(
                self.item_name, self._meta.verbose_name)
        return a.label
    

class Widgets(dd.Table):
    model = 'dashboard.Widget'

class AllWidgets(Widgets):
    label = _("All dashboard widgets")
    required_roles = dd.login_required(SiteAdmin)
    column_names = 'id user seqno move_buttons title visible *'
    order_by = ['id']
        
class WidgetsByUser(Widgets):
    label = _("Dashboard")
    master_key = 'user'
    column_names = 'seqno move_buttons title visible *'
    order_by = ['seqno']

    
def update_widgets_for(ar, user):
    
    available = set([i.name for i in get_available_items(user)])
    
    Widget = rt.models.dashboard.Widget
    qs = Widget.objects.filter(user=user).order_by('seqno')
    
    seqno = 0
    for w in qs:
        if w.item_name in available:
            available.remove(w.item_name)
            seqno = max(seqno, w.seqno)
        else:
            w.delete()
    up = user.get_preferences()
    for name in available:
        seqno += 1
        obj = Widget(user=user, item_name=name, seqno=seqno)
        obj.full_clean()
        obj.save()
        # print(20161128, "created item", obj)

    up.invalidate()
    ar.set_response(refresh=True)

