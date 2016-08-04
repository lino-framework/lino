# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.utils.restify import restify
from lino.utils.xmlgen.html import E

def rich_text_to_elems(ar, description):
    """A RichTextField can contain HTML markup or plain text."""
    if description.startswith("<"):
        # desc = E.raw('<div>%s</div>' % self.description)
        desc = E.raw(ar.parse_memo(description))
        return [desc]
    # desc = E.raw('<div>%s</div>' % self.description)
    html = restify(ar.parse_memo(description))
    # dd.logger.info("20160704b restified --> %s", html)
    desc = E.raw(html)
    # dd.logger.info(
    #     "20160704c parsed --> %s", E.tostring(desc))
    if desc.tag == 'body':
        # happens if it contains more than one paragraph
        return list(desc)  # .children
    return [desc]

def body_subject_to_elems(ar, title, description):
    """Convert the given `title` and `description` to a list of HTML
    elements.

    Used by :mod:`lino.modlib.notify` and by :mod:`lino_cosi.lib.sales`

    """
    if description:
        elems = [E.p(E.b(title), E.br())]
        elems += rich_text_to_elems(ar, description)
        
    else:
        elems = [E.b(title)]
        # return E.span(self.title)
    return elems

