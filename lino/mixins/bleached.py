# -*- coding: UTF-8 -*-
# Copyright 2016-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""

Content moved to :doc:`docs/dev/bleach`.

"""
import six

from django.conf import settings
from lino.core.model import Model
from lino.core.fields import fields_list, RichTextField
from lino.utils.restify import restify
from lino.utils.soup import truncate_comment
from lino.core.exceptions import ChangedAPI
from etgen.html import E, tostring
from lino.api import _

from lxml import html as lxml_html

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



class BleachedPreviewBody(Model):

    class Meta:
        abstract = True

    # bleached_fields = 'body'

    body = RichTextField(_("Body"), blank=True, format='html', bleached=True)
    body_preview = RichTextField(_("Preview"), blank=True, editable=False)

    # def full_clean(self, *args, **kwargs):
    def before_ui_save(self, ar):
        """Fills the body_preview field.

        """
        # super(BleachedPreviewBody, self).full_clean(*args, **kwargs)
        super(BleachedPreviewBody, self).before_ui_save(ar)
        self.body_preview = truncate_comment(self.body)


   
