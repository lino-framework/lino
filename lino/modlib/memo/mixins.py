# -*- coding: UTF-8 -*-
# Copyright 2016-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from bs4 import BeautifulSoup

from django.conf import settings

from lino.core.model import Model
from lino.core.requests import BaseRequest
from lino.core.fields import fields_list, RichTextField
from lino.utils.restify import restify
from lino.core.exceptions import ChangedAPI
from lino.modlib.checkdata.choicelists import Checker
from etgen.html import E, tostring
from lino.api import _

from lxml import html as lxml_html


def truncate_comment(html_str, max_p_len=None):
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

    def get_previews(self, ar=None):
        front_end = settings.SITE.plugins.memo.front_end or settings.SITE.default_ui
        if ar is None or ar.renderer.front_end is not front_end:
            ar = BaseRequest(renderer=front_end.renderer)
            # print("20190926 using BaseRequest with front end {}".format(front_end))

        parse = settings.SITE.plugins.memo.parser.parse
        short = parse(truncate_comment(self.body), ar)
        full = parse(self.body, ar)
        return (short, full)

    def before_ui_save(self, ar):
        """Fills the preview fields.

        """
        super(Previewable, self).before_ui_save(ar)
        self.short_preview, self.full_preview = self.get_previews(ar)


class PreviewableChecker(Checker):
    verbose_name = _("Check for previewables needing update")
    model = Previewable

    def get_checkdata_problems(self, obj, fix=False):
        short, full = obj.get_previews()
        if obj.short_preview != short or obj.full_preview != full:
            if fix:
                obj.short_preview = short
                obj.full_preview = full
            else:
                yield (True, _("Preview needs update"))

PreviewableChecker.activate()
