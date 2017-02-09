# Copyright 2016-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Installs some comments which contain "hackerish" HTML, as can
happen when pasting text from certain Microsoft products.

"""
from lino.utils import Cycler
from lino.api import rt, dd


def objects():
    if dd.plugins.comments.commentable_model is None:
        return
    OWNERS = Cycler(dd.plugins.comments.commentable_model.objects.all())
    if len(OWNERS) == 0:
        return
    Comment = rt.models.comments.Comment
    User = rt.models.users.User
    for i in range(2):
        for u in User.objects.all():
            owner = OWNERS.pop()
            if owner.private:
                txt = "Very confidential comment"
            else:
                txt = "Hackerish comment"
            yield Comment(
                user=u, owner=owner,
                short_text=txt,
                more_text='<p><!--[if gte foo 123]>A conditional '
                          'comment<![endif]--></p>\n<p>Hello</p>')
