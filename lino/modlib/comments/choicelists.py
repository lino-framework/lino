# -*- coding: UTF-8 -*-
# Copyright 2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, rt, _
from datetime import datetime
import pytz
from lino.modlib.system.choicelists import ObservedEvent
# from .roles import CommentsUser


class Emotions(dd.ChoiceList):
    verbose_name = _("Emotion")
    verbose_name_plural = _("Emotions")
    column_names = "value name text button_text"

# ⁈:2048  👍:1F44D  👎:1F44E  ✅:2705  ❎:274e  😠:1F620 😀:1F600 😐:1f610
add = Emotions.add_item
if dd.plugins.comments.emotion_range == "business":
    add('ok', _("Okay"), 'ok')
    # add('but', _("But"), 'but', button_text="⁈")
    add('agree', _("Agree"), 'agree', button_text="✅")
    add('disagree', _("Disagree"), 'disagree', button_text="❎")
elif dd.plugins.comments.emotion_range == "social":
    add('ok', _("Like"), 'ok', button_text="👍")
    add('dislike', _("Dislike"), 'dislike', button_text="👎")
    add('happy', _("Happy"), 'happy', button_text="😀")
    add('angry', _("Angry"), 'angry', button_text="😠")
    add('skeptical', _("Skeptical"), 'skeptical', button_text="😐")


class ObservedTime(ObservedEvent):

    def __init__(self, value, name, text):
        super(ObservedTime, self).__init__(value, text=text, name=name)

    def add_filter(self, qs, pv):
        if pv.start_date:
            start_datetime = datetime.combine(pv.start_date, datetime.min.time()).replace(tzinfo=pytz.UTC)
            qs = qs.filter(**{
                self.name + '__gte': start_datetime,
                self.name + '__isnull': False})
        if pv.end_date:
            end_datetime = datetime.combine(pv.end_date, datetime.max.time()).replace(tzinfo=pytz.UTC)
            qs = qs.filter(**{
                self.name + '__lte': end_datetime,
                self.name + '__isnull': False})
        return qs

class CommentEvents(dd.ChoiceList):
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")

def add(*args):
    CommentEvents.add_item_instance(ObservedTime(*args))
add('10', 'created', _("Created"))
add('20', 'modified', _("Modified"))
#add('30', 'published', _("Published"))



# class PublishComment(dd.Action):
#     sort_index = 100
#     label = _("Publish")
#     show_in_workflow = True
#     show_in_bbar = False
#     required_roles = dd.login_required(CommentsUser)


#     def run_from_ui(self, ar, **kw):
#         for obj in ar.selected_rows:
#             obj.do_publish(ar)
#         ar.success(
#             _("{0} comments published.").format(
#                 len(ar.selected_rows)), refresh_all=True)

# class PublishAllComments(PublishComment):
#     label = _("Publish all")
#     show_in_workflow = False
#     show_in_bbar = True
#     select_rows = False
#     default_format = 'ajax'

#     def run_from_ui(self, ar, **kw):
#         n = ar.get_total_count()
#         def ok(ar):
#             for obj in ar:
#                 obj.do_publish(ar)
#             ar.success(
#                 _("{0} comments published.").format(n), refresh_all=True)

#         ar.confirm(
#             ok, _("This will publish {} comments.").format(n),
#             _("Are you sure?"))
