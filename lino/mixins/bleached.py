# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
Remove all tags except some when saving the content of a
:class:`RichHtmlField <lino.core.fields.RichHtmlField>`.

When copying rich text from other applications into Lino, the text can
contain styles and other things which can cause side effects when
displaying or printing them.

A possible strategy for avoiding such problems is to bleach any
content, i.e. allow only simple plain HTML formatting.

If you use this in your application, then your application must add
`bleach <http://bleach.readthedocs.org/en/latest/>`_ to its
:ref:`install_requires`.

Usage example (excerpt from
:class:`lino.modlib.comments.models.Comment`)::

  from lino.mixins.bleached import Bleached
  from lino.api import dd

  class MyModel(Bleached):

      short_text = dd.RichTextField(_("Short text"), blank=True)
      more_text = dd.RichTextField(_("More text"), blank=True)

      bleached_fields = "short_text more_text"

Note that `bleach` until 20170225 required html5lib` version
`0.9999999` (7*"9") while the current version is `0.999999999`
(9*"9"). Which means that you might inadvertedly break `bleach` when
you ask to update `html5lib`::

    $ pip install -U html5lib
    ...
    Successfully installed html5lib-0.999999999
    $ python -m bleach
    Traceback (most recent call last):
      File "/usr/lib/python2.7/runpy.py", line 163, in _run_module_as_main
        mod_name, _Error)
      File "/usr/lib/python2.7/runpy.py", line 111, in _get_module_details
        __import__(mod_name)  # Do not catch exceptions initializing package
      File "/site-packages/bleach/__init__.py", line 14, in <module>
        from html5lib.sanitizer import HTMLSanitizer
    ImportError: No module named sanitizer
"""
import six

try:
    import bleach
except ImportError:
    bleach = None

import logging
logger = logging.getLogger(__name__)

from lino.core.model import Model
from lino.core.fields import fields_list, RichTextField
from lino.utils.restify import restify
from lino.utils.soup import truncate_comment
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


class Bleached(Model):
    """
    Mixin for models that have at least one text field which might
    contain HTML.

    When using this, you should specify :attr:`bleached_fields`.

    .. attribute:: bleached_fields

        A list of strings with the names of the fields that are
        to be bleached.

    .. attribute:: allowed_tags

        A list of tag names which are to *remain* in HTML comments if
        bleaching is active.
    """
    
    allowed_tags = ['a', 'b', 'i', 'em', 'ul', 'ol', 'li', 'strong',
                    'p', 'br', 'span', 'pre', 'def', 'table', 'th', 'tr',
                    'td', 'thead', 'tfoot', 'tbody']

    bleached_fields = []

    class Meta(object):
        abstract = True

    @classmethod
    def on_analyze(cls, site):
        super(Bleached, cls).on_analyze(site)
        if cls.bleached_fields is None:
            return
        if isinstance(cls.bleached_fields, six.string_types):
            cls.bleached_fields = fields_list(cls, cls.bleached_fields)
        if not bleach:
            # site.logger.debug(
            #     "%s not being bleached because `bleach` is broken "
            #     "or not installed.", cls)
            raise Exception(
                "{} has bleached fields but `bleach` is not installed.".format(
                    cls))

    # def full_clean(self, *args, **kwargs):
    def before_ui_save(self, ar):
        """This does the actual bleaching work.
        
        TODO: Lino should log at least a bit of bleach's "activity",
        for example an info message saying "Removed tags x, y, z from
        short_text"

        """
        if bleach and self.bleached_fields:
            for k in self.bleached_fields:
                old = getattr(self, k)
                if old is None:
                    continue
                try:
                    new = bleach.clean(
                        old, tags=self.allowed_tags, strip=True)
                except TypeError as e:
                    logger.warning(
                        "Could not bleach %r : %s (%s)", old, e, self)
                    continue
                if old != new:
                    logger.debug(
                        "Bleaching %s from %r to %r", k, old, new)
                setattr(self, k, new)
        # super(Bleached, self).full_clean(*args, **kwargs)
        super(Bleached, self).before_ui_save(ar)


class BleachedPreviewBody(Bleached):

    class Meta:
        abstract = True

    bleached_fields = 'body'

    body = RichTextField(_("Body"), blank=True, format='html')
    body_preview = RichTextField(
        _("Preview"), blank=True, editable=False)

    # def full_clean(self, *args, **kwargs):
    def before_ui_save(self, ar):
        """Fills the body_preview field.

        """
        # super(BleachedPreviewBody, self).full_clean(*args, **kwargs)
        super(BleachedPreviewBody, self).before_ui_save(ar)
        self.body_preview = truncate_comment(self.body)


   
