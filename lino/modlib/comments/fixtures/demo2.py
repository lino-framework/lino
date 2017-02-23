# Copyright 2016-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Fixure for commnts

creates test comments for each user on each object owned by them which is a commentable_model


some comments are rich-text
some commetns are plain-text
some comments are private
some comments are tables
some comments are long
"""
from lino.utils import Cycler
from lino.api import rt, dd

styled = """<h1 style="color: #5e9ca0;">Styled comment <span style="color: #2b2301;">pasted from word!</span> </h1>"""
table = """<table class="editorDemoTable"><thead>
<tr><td>Who</td><td>What</td><td>Done?</td></tr></thead><tbody><tr><td>Him</td><td>Bar</td><td>&nbsp;</td></tr><tr><td>Her</td><td>Foo the Bar</td><td><strong style="font-size: 17px; color: #2b2301;">x</strong></td></tr><tr><td>Them</td><td><span id="demoId">Floop the pig<br /></span></td><td>x</td></tr></tbody></table>"""
lorem = """<p>Lorem ipsum<strong> dolor sit amet</strong>, consectetur adipiscing elit. Nunc cursus felis nisi, eu pellentesque lorem lobortis non. Aenean non sodales neque, vitae venenatis lectus. In eros dui, gravida et dolor at, pellentesque hendrerit magna. Quisque vel lectus dictum, rhoncus massa feugiat, condimentum sem. Donec elit nisl, placerat vitae imperdiet eget, hendrerit nec quam. Ut elementum ligula vitae odio efficitur rhoncus. Duis in blandit neque. Sed dictum mollis volutpat. Morbi at est et nisi euismod viverra. Nulla quis lacus vitae ante sollicitudin tincidunt. Donec nec enim in leo vulputate ultrices. Suspendisse potenti. Ut elit nibh, porta ut enim ac, convallis molestie risus. Praesent consectetur lacus lacus, in faucibus justo fringilla vel.</p>
<p>Donec fermentum enim et maximus vestibulum. Sed mollis lacus quis dictum fermentum. Maecenas libero tellus, hendrerit cursus pretium et, hendrerit quis lectus. Nunc bibendum nunc nunc, ac commodo sem interdum ut. Quisque vitae turpis lectus. Nullam efficitur scelerisque hendrerit. Fusce feugiat ullamcorper nulla. Suspendisse quis placerat ligula. Etiam ullamcorper elementum consectetur. Aenean et diam ullamcorper, posuere turpis eget, egestas nibh. Quisque condimentum arcu ac metus sodales placerat. Quisque placerat, quam nec tincidunt pharetra, urna justo scelerisque urna, et vulputate ipsum lacus at ligula.</p>"""
short_lorem = """<p>Lorem ipsum <strong> dolor sit amet</strong>, consectetur adipiscing elit. Donec interdum dictum erat. Fusce condimentum erat a pulvinar ultricies.</p>
<p>Phasellus gravida ullamcorper eros, sit amet blandit sapien laoreet quis.</p>
<p>Donec accumsan mauris at risus lobortis, nec pretium tortor aliquam. Nulla vel enim vel eros venenatis congue.</p>"""

def objects():
    TXT = Cycler([styled, table, lorem, short_lorem])

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

                txt = "<p>Very confidential comment</p>"
            else:
                txt = TXT.pop()# txt = "Hackerish comment"
            yield Comment(
                user=u, owner=owner,
                short_text=txt,
                more_text='<p><!--[if gte foo 123]>A conditional '
                          'comment<![endif]--></p>\n<p>Hello</p>')
