# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
This defines the :class:`Certifiable` model mixin.

"""

from __future__ import unicode_literals
from __future__ import print_function

from django.utils.translation import ugettext_lazy as _
from django.contrib.humanize.templatetags.humanize import naturaltime

from lino.api import dd


class Certifiable(dd.Model):
    """
    Any model which inherits from this mixin becomes "certifiable".
    That is:

      - it has a `printed_by` field and a corresponding virtual field
        `printed` which point to the excerpt that is the "definitive"
        ("Certifying") printout of this object.

      - It may define a list of "certifiable" fields. 
        See :meth:`get_certifiable_fields`.

    Usage example::

        from lino.modlib.excerpts.mixins import Certifiable

        class MyModel(dd.UserAuthored, Certifiable, dd.Duplicable):
            ...

    The :mod:`lino.modlib.excerpts.fixtures.std` fixture automatically
    creates a certifying :class:`ExcerptType` instance for every model
    which inherits from :class:`Certifiable`.


    .. attribute:: printed

      Displays information about when this certifiable has been printed.
      Clicking on it will display the excerpt pointed to by
      :attr:`printed_by`.

    .. attribute:: printed_by

      ForeignKey to the :class:`Excerpt` which certifies this instance.

      A :class:`Certifiable` is considered "certified" when this this is
      not `None`.

    .. method:: get_certifiable_fields()

      Expected to return a string with a space-separated list of field
      names.  These files will automaticaly become disabled (readonly)
      when the document is "certified". The default implementation
      returns an empty string, which means that no field will become
      disabled when the row is "certified".

      Example::

          @classmethod
          def get_certifiable_fields(cls):
              return 'date user title'


    """
    class Meta:
        abstract = True

    printed_by = dd.ForeignKey(
        'excerpts.Excerpt',
        verbose_name=_("Printed"),
        editable=False,
        related_name="%(app_label)s_%(class)s_set_as_printed",
        blank=True, null=True,
    )

    def disabled_fields(self, ar):
        if self.printed_by_id is None:
            return set()
        return self.CERTIFIED_FIELDS

    @classmethod
    def on_analyze(cls, site):
        # Contract.user.verbose_name = _("responsible (DSBE)")
        cls.CERTIFIED_FIELDS = dd.fields_list(
            cls,
            cls.get_certifiable_fields())
        super(Certifiable, cls).on_analyze(site)

    @classmethod
    def get_certifiable_fields(cls):
        return ''

    @dd.displayfield(_("Printed"))
    def printed(self, ar):
        ex = self.printed_by
        if ex is None:
            return ''
        return ar.obj2html(ex, naturaltime(ex.build_time))

    def clear_cache(self):
        obj = self.printed_by
        if obj is not None:
            self.printed_by = None
            self.full_clean()
            self.save()
            obj.delete()

    def get_excerpt_title(self):
        """A string to be used in templates as the title of the certifying
        document.

        """
        return unicode(self)

