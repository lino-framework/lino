# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Defines models for :mod:`lino.modlib.postings`.
"""
from builtins import object

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from lino.core import actions

from lino.api import dd, rt


class CreatePostings(dd.Action):

    """
    Creates a series of new Postings from this Postable. 
    The Postable gives the list of recipients, and there will 
    be one Posting for each recipient.
    
    Author of each Posting will be the user who issued the action request,
    even if that user is acting as someone else.
    You cannot create a Posting in someone else's name.
    
    """

    url_action_name = 'post'
    #~ label = _('Create email')
    label = _('Create posting')
    help_text = _('Create classical mail postings from this')
    icon_name = 'script_add'

    callable_from = (actions.GridEdit,
                     actions.ShowDetailAction)  # but not from InsertRow

    def run_from_ui(self, ar, **kw):

        Posting = rt.modules.postings.Posting
        PostingStates = rt.modules.postings.PostingStates

        elem = ar.selected_rows[0]
        recs = tuple(elem.get_postable_recipients())

        def ok(ar):
            for rec in recs:
                p = Posting(
                    user=ar.user, owner=elem,
                    partner=rec,
                    date=dd.today(),
                    state=PostingStates.ready)
                p.full_clean()
                p.save()
            kw.update(refresh=True)
            ar.success(**kw)

        msg = _("Going to create %(num)d postings for %(elem)s") % dict(
            num=len(recs), elem=elem)
        ar.confirm(ok, msg)


class Postable(dd.Model):
    """
    Mixin for models that provide a "Post" button.
    """

    class Meta(object):
        abstract = True

    create_postings = CreatePostings()

    #~ def print_from_posting(self,posting,ar,**kw):
        #~ return ar.error("Not implemented")

    def get_postable_recipients(self):
        return []

    def get_recipients(self):
        Posting = rt.modules.postings.Posting
        qs = Posting.objects.filter(
            owner_id=self.pk, owner_type=ContentType.get_for_model(self.__class__))
        return qs.values('partner')
        #~ state=PostingStates.ready)


