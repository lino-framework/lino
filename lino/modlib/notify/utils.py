# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.utils.restify import restify
from lino.utils.xmlgen.html import E


def body_subject_to_elems(ar, title, description):
    """Convert the given `title` and `description` to a list of HTML
    elements.

    Used by `lino.modlib.notify` and by `lino_cosi.lib.sales`

    """
    if description:
        elems = [E.p(E.b(title), E.br())]
        if description.startswith("<"):
            # desc = E.raw('<div>%s</div>' % self.description)
            desc = E.raw(ar.parse_memo(description))
            elems.append(desc)
        else:
            # desc = E.raw('<div>%s</div>' % self.description)
            html = restify(ar.parse_memo(description))
            # dd.logger.info("20160704b restified --> %s", html)
            desc = E.raw(html)
            if desc.tag == 'body':
                # happens if it contains more than one paragraph
                desc = list(desc)  # .children
                elems.extend(desc)
            else:
                elems.append(desc)
            # dd.logger.info(
            #     "20160704c parsed --> %s", E.tostring(desc))
    else:
        elems = [E.b(title)]
        # return E.span(self.title)
    return elems

