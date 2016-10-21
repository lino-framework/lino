# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Installs some comments which contain "hackerish" HTML, as can
happen when pasting text from certain Microsoft products.

"""

from lino.api import rt


def objects():
    Comment = rt.models.comments.Comment
    User = rt.models.users.User
    for u in User.objects.all():
        yield Comment(user=u,
                      short_text="Hackerish comment",
                      more_text='<p><!--[if gte foo 123]>A conditional '
                      'comment<![endif]--></p>\n<p>Hello</p>')
