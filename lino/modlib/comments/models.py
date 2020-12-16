# -*- coding: UTF-8 -*-
# Copyright 2013-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from django.db import models
from django.db.models import Q
from django.core import validators
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from etgen.html import E, tostring

from lino.api import dd, rt, _

from lino.mixins import CreatedModified, BabelNamed
from lino.mixins.periods import DateRangeObservable
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.notify.mixins import ChangeNotifier
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.memo.mixins import Previewable
from lino.modlib.publisher.mixins import Publishable
from .choicelists import CommentEvents, Emotions
from .mixins import Commentable
from .fields import MyEmotionField
# from .choicelists import PublishAllComments, PublishComment

if dd.is_installed("inbox"):
    from lino_xl.lib.inbox.models import comment_email


class CommentType(BabelNamed):
    class Meta(object):
        abstract = dd.is_abstract_model(__name__, 'CommentType')
        verbose_name = _("Comment Type")
        verbose_name_plural = _("Comment Types")



class Comment(CreatedModified, UserAuthored, Controllable,
              ChangeNotifier, Previewable, Publishable, DateRangeObservable):
    class Meta(object):
        app_label = 'comments'
        abstract = dd.is_abstract_model(__name__, 'Comment')
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    publisher_location = "c"

    reply_to = dd.ForeignKey(
        'self', blank=True, null=True, verbose_name=_("Reply to"),
        related_name="replies_to_this")
    # more_text = dd.RichTextField(_("More text"), blank=True)

    private = models.BooleanField(
        _("Private"), default=dd.plugins.comments.private_default)

    comment_type = dd.ForeignKey('comments.CommentType', blank=True, null=True)
    # reply_vote = models.BooleanField(_("Upvote"), null=True, blank=True)
    # reply_vote = models.SmallIntegerField(_("Vote"), default=0,
    #     validators=[validators.MinValueValidator(-1),
    #         validators.MaxValueValidator(1)])

    my_emotion = MyEmotionField()

    def get_my_emotion(self, ar):
        if ar is None:
            return
        mr = rt.models.comments.Reaction.objects.filter(user=ar.get_user(), comment=self).first()
        if mr:
            return mr.emotion

    def __str__(self):
        return '{} #{}'.format(self._meta.verbose_name, self.pk)
        # return _('{user} {time}').format(
        #     user=self.user, obj=self.owner,
        #     time=naturaltime(self.modified))

    # def disabled_fields(self, ar):
    #     rv = super(Comment, self).disabled_fields(ar)
    #     if not self.reply_to_id:
    #         # rv.add("do_pick_reply_emotion")
    #         # rv.add("pick_reply_emotion")
    #         rv.add("reply_emotion")
    #         rv.add("reply_vote")
    #     return rv

    @classmethod
    def get_user_queryset(cls, user):
        qs = super(Comment, cls).get_user_queryset(user)

        if not user.user_type.has_required_roles([CommentsReader]):
            return qs.none()

        filters = []
        for m in rt.models_by_base(Commentable):
            flt = m.get_comments_filter(user)
            if flt is not None:
                ct = rt.models.contenttypes.ContentType.objects.get_for_model(m)
                filters.append(flt | ~Q(owner_type=ct))
        if len(filters):
            qs = qs.filter(*filters)
        return qs.distinct()  # add distinct because filter might be on a join

    # def after_ui_create(self, ar):
    #     super(Comment, self).after_ui_create(ar)
    #     if self.owner_id:
    #         self.private = self.owner.is_comment_private(self, ar)

    def on_create(self, ar):
        super(Comment, self).on_create(ar)
        if self.owner_id:
            self.private = self.owner.is_comment_private(self, ar)

    def after_ui_save(self, ar, cw):
        super(Comment, self).after_ui_save(ar, cw)
        if self.owner_id:
            self.owner.on_commented(self, ar, cw)
        if dd.is_installed("memo"):
            ref_objects = settings.SITE.plugins.memo.parser.get_referred_objects(self.body)
            for ref_object in ref_objects:
                created_mention = Mention(comment=self,
                        owner_id=ref_object.pk,
                        owner_type=ContentType.objects.get_for_model(ref_object.__class__))
                created_mention.touch()
                created_mention.save()

    # def full_clean(self):
    #     super(Comment, self).full_clean()
    #     self.owner.setup_comment(self)

    def get_change_owner(self):
        return self.owner or self

    # def get_change_message_type(self, ar):
    #     if self.published is None:
    #         return None
    #     return super(Comment, self).get_change_message_type(ar)

    def get_change_observers(self, ar=None):
        if isinstance(self.owner, ChangeNotifier):
            obs = self.owner
        else:
            obs = super(Comment, self)
        for u in obs.get_change_observers(ar):
            yield u

    def get_change_subject(self, ar, cw):
        if cw is None:
            s = _("{user} commented on {obj}")
        else:
            s = _("{user} modified comment on {obj}")
        return s.format(user=ar.get_user(), obj=self.owner)

    def get_change_body(self, ar, cw):
        if cw is None:
            s = _("{user} commented on {obj}")
        else:
            s = _("{user} modified comment on {obj}")
        user = ar.get_user()
        s = s.format(
            user=user, obj=ar.obj2memo(self.owner))
        if dd.is_installed("inbox"):
            #mailto:ADDR@HOST.com?subject=SUBJECT&body=Filling%20in%20the%20Body!%0D%0Afoo%0D%0Abar
            s += ' <a href="{href}">{reply}</a>'.format(
                href=comment_email.gen_href(self, user),
                reply=_("Reply"))

        s += ':<br>' + self.body
        # if False:
        #     s += '\n<p>\n' + self.more_text
        return s

    @classmethod
    def setup_parameters(cls, fields):
        fields.update(
            observed_event=CommentEvents.field(blank=True))
        # fields.update(
        #     start_date=models.DateField(
        #         _("Period from"), blank=True, null=True,
        #         help_text=_("Start date of observed period")))
        # fields.update(
        #     end_date=models.DateField(
        #         _("until"),
        #         blank=True, null=True,
        #         help_text=_("End date of observed period")))
        # fields.update(
        #     show_published=dd.YesNo.field(_("Published"), blank=True))
        super(Comment, cls).setup_parameters(fields)

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        qs = super(Comment, cls).get_request_queryset(ar, **filter)
        pv = ar.param_values
        if pv.observed_event:
            qs = pv.observed_event.add_filter(qs, pv)
        return qs

    @dd.htmlbox()
    def card_summary(self, ar):
        if not ar:
            return ""
        # header = ar.actor.get_comment_header(self, ar) if ar else ""
        body = ar.parse_memo(self.body)
        # for e in lxml.html.fragments_fromstring(self.short_preview):  # , parser=cls.html_parser)
        #     html += tostring(e)

        return "<div><p>{}</p></div>".format(
            # header,
            body)

    # def summary_row(o, ar):



dd.update_field(Comment, 'user', editable=False)
Comment.update_controller_field(verbose_name=_('Topic'))
Comment.add_picker('my_emotion')

class Mention(CreatedModified, Controllable, UserAuthored):

    class Meta(object):
        app_label = 'comments'
        abstract = dd.is_abstract_model(__name__, 'Mention')
        verbose_name = _("Mention")
        verbose_name_plural = _("Mentions")

    comment = dd.ForeignKey('comments.Comment', blank=True, null=True)


class Reaction(CreatedModified, UserAuthored, DateRangeObservable):

    class Meta(object):
        app_label = 'comments'
        abstract = dd.is_abstract_model(__name__, 'Reaction')
        verbose_name = _("Reaction")
        verbose_name_plural = _("Reactions")

    allow_cascaded_delete = 'user comment'

    comment = dd.ForeignKey('comments.Comment', related_name="reactions_to_this")
    emotion = Emotions.field(default="ok")


from .ui import *
