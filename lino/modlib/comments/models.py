# -*- coding: UTF-8 -*-
# Copyright 2013-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from builtins import object

from django.db import models

from lino.api import dd, rt, _
    
from lino.mixins import CreatedModified, BabelNamed
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.notify.mixins import ChangeNotifier
from lino.modlib.gfks.mixins import Controllable
from lino.mixins.bleached import BleachedPreviewBody
from .choicelists import CommentEvents
# from .choicelists import PublishAllComments, PublishComment



if dd.is_installed("inbox"):
    from lino_xl.lib.inbox.models import comment_email

class CommentType(BabelNamed):
    class Meta(object):
        abstract = dd.is_abstract_model(__name__, 'CommentType')
        verbose_name = _("Comment Type")
        verbose_name_plural = _("Comment Types")

    
@dd.python_2_unicode_compatible
class Comment(CreatedModified, UserAuthored, Controllable,
              ChangeNotifier, BleachedPreviewBody):
    class Meta(object):
        app_label = 'comments'
        abstract = dd.is_abstract_model(__name__, 'Comment')
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    # ALLOWED_TAGS = ['a', 'b', 'i', 'em', 'ul', 'ol', 'li']
    # bleached_fields = 'short_text more_text'
    # bleached_fields = 'body'

    # if dd.plugins.comments.user_must_publish:
    #     # e.g. in amici we don't have notify
    #     publish_this = PublishComment()
    #     publish_all = PublishAllComments()

    # short_text = dd.RichTextField(_("Short text"))
    # owner = dd.ForeignKey(commentable_model, blank=True, null=True)

    reply_to = dd.ForeignKey(
        'self', blank=True, null=True, verbose_name=_("Reply to"))
    # more_text = dd.RichTextField(_("More text"), blank=True)
    # private = models.BooleanField(_("Private"), default=False)
    comment_type = dd.ForeignKey(
        'comments.CommentType', blank=True, null=True)
    # published = models.DateTimeField(
    #     _("Published"), blank=True, null=True)

    def __str__(self):
        return u'%s #%s' % (self._meta.verbose_name, self.pk)
        # return _('{user} {time}').format(
        #     user=self.user, obj=self.owner,
        #     time=naturaltime(self.modified))

    # @classmethod
    # def get_request_queryset(cls, ar, **filter):
    #     # if commentable_model is None:
    #     #     return cls.objects.all()
    #     # if ar.get_user().user_type.has_required_roles([SiteUser]):
    #     if ar.get_user().authenticated:
    #         return cls.objects.all()
    #     return super(Comment, cls).get_request_queryset(ar, **filter)

    #     # else:
    #     #     return cls.objects.exclude(owner__private=True)
        
    def after_ui_save(self, ar, cw):
        super(Comment, self).after_ui_save(ar, cw)
        if self.owner_id:
            self.owner.on_commented(self, ar, cw)
        
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
        fields.update(
            start_date=models.DateField(
                _("Period from"), blank=True, null=True,
                help_text=_("Start date of observed period")))
        fields.update(
            end_date=models.DateField(
                _("until"),
                blank=True, null=True,
                help_text=_("End date of observed period")))
        # fields.update(
        #     show_published=dd.YesNo.field(_("Published"), blank=True))
        super(Comment, cls).setup_parameters(fields)

    @classmethod
    def get_request_queryset(cls, ar, **filter):
        qs = super(Comment, cls).get_request_queryset(ar, **filter)
        pv = ar.param_values
        if pv.observed_event:
            qs = pv.observed_event.add_filter(qs, pv)
        # if pv.show_published == dd.YesNo.yes:
        #     qs = qs.filter(published__isnull=False)
        # elif pv.show_published == dd.YesNo.no:
        #     qs = qs.filter(published__isnull=True)
        return qs

dd.update_field(Comment, 'user', editable=False)


from .ui import *

