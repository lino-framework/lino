# -*- coding: UTF-8 -*-
# Copyright 2016-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""

See :doc:`docs/specs/memo`.

"""

from bs4 import BeautifulSoup

from django.conf import settings

from lino.core.model import Model
from lino.core.requests import BaseRequest
from lino.core.fields import fields_list, RichTextField
from lino.utils.restify import restify
from lino.core.exceptions import ChangedAPI
from etgen.html import E, tostring
from lino.api import _

from lxml import html as lxml_html


def truncate_comment(html_str, max_p_len=None):
    """
    Return a shortened preview of a html string, containing at most one
    paragraph with at most `max_p_len` characters.

    :html_str: the raw string of html
    :max_p_len: max number of characters in the paragraph.

    See usage examples in :doc:`/specs/comments`.

    """
    html_str = html_str.strip()  # remove leading or trailing newlines
    if not html_str.startswith('<'):
        # it's plain text without html tags
        ps = html_str.split('\n\n', 1)
        txt = ps[0]
        if max_p_len is not None and len(txt) > max_p_len:
            txt = txt[:max_p_len] + "..."
        elif len(ps) > 1:
            txt = txt + " (...)"
        return txt
    soup = BeautifulSoup(html_str, "html.parser")
    ps = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9"])
    if len(ps) > 0:
        txt = ps[0].text
        if max_p_len is not None and len(txt) > max_p_len:
            txt = txt[:max_p_len] + "..."
        elif len(ps) > 1:
            txt = txt + " (...)"
        return txt
        # ps[0].string = (txt)
        # return six.text_type(ps[0])
    return html_str


def rich_text_to_elems(ar, description):
    """
    A RichTextField can contain HTML markup or plain text.
    """
    if description.startswith("<"):
        # desc = E.raw('<div>%s</div>' % self.description)
        desc = lxml_html.fragments_fromstring(ar.parse_memo(description))
        return desc
    # desc = E.raw('<div>%s</div>' % self.description)
    html = restify(ar.parse_memo(description))
    # logger.info(u"20180320 restify %s --> %s", description, html)
    # html = html.strip()
    try:
        desc = lxml_html.fragments_fromstring(html)
    except Exception as e:
        raise Exception(
            "Could not parse {!r} : {}".format(html, e))
    # logger.info(
    #     "20160704c parsed --> %s", tostring(desc))
    return desc
    # if desc.tag == 'body':
    #     # happens if it contains more than one paragraph
    #     return list(desc)  # .children
    # return [desc]

def body_subject_to_elems(ar, title, description):
    """
    Convert the given `title` and `description` to a list of HTML
    elements.

    Used by :mod:`lino.modlib.notify` and by :mod:`lino_xl.lib.sales`
    """
    if description:
        elems = [E.p(E.b(title), E.br())]
        elems += rich_text_to_elems(ar, description)
        
    else:
        elems = [E.b(title)]
        # return E.span(self.title)
    return elems



class Previewable(Model):

    class Meta:
        abstract = True

    body = RichTextField(_("Body"), blank=True, format='html', bleached=True)
    short_preview = RichTextField(_("Preview"), blank=True, editable=False)
    full_preview = RichTextField(_("Preview (full)"), blank=True, editable=False)

    def before_ui_save(self, ar):
        """Fills the preview fields.

        """
        front_end = settings.SITE.plugins.memo.front_end
        if front_end is not None:
            if ar is None or ar.renderer.front_end is not front_end:
                # ar = ar.spawn_request(renderer=front_end.renderer)
                ar = BaseRequest(renderer=front_end.renderer)

        # super(BleachedPreviewBody, self).full_clean(*args, **kwargs)
        super(Previewable, self).before_ui_save(ar)
        parse = settings.SITE.plugins.memo.parser.parse
        self.short_preview = parse(truncate_comment(self.body), ar)
        self.full_preview = parse(self.body, ar)


   
