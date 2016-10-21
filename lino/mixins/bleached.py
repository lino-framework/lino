# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""
If `bleach
<http://bleach.readthedocs.org/en/latest/>`_ is installed, all
tags except some will be removed when

"""
try:
    import bleach
except ImportError:
    bleach = None

from lino.core.model import Model
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


class Bleached(Model):
    """Mixin for models which have at least one text field which might
    contain HTML.

    When using this, you should specify :attr:`bleached_fields`.

    .. attribute:: bleached_fields

        A list of strings with the names of the fields that are bleached.

    .. attribute:: ALLOWED_TAGS

        A list of tag names which are to *remain* in HTML comments if
        bleaching is active.

    """
    
    ALLOWED_TAGS = ['a', 'b', 'i', 'em', 'ul', 'ol', 'li', 'strong', 'p',
                    'br', 'span', 'pre', 'def']

    bleached_fields = []

    class Meta(object):
        abstract = True

    def save(self, *args, **kwargs):
        if bleach:
            for k in self.bleached_fields:
                setattr(self, k, bleach.clean(
                    getattr(self, k),
                    tags=self.ALLOWED_TAGS, strip=True))
        super(Bleached, self).save(*args, **kwargs)


