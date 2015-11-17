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
from django.db import models

from lino.utils.mldbc.mixins import BabelNamed

from lino.api import dd


class ClearPrinted(dd.Action):
    """Action to clear the print cache (i.e. the generated printable
document)."""
    sort_index = 51
    label = _('Clear print cache')
    icon_name = 'printer_delete'
    help_text = _("Mark this object as not printed. A subsequent "
                  "call to print will generate a new cache file.")

    def get_action_permission(self, ar, obj, state):
        if obj.printed_by_id is None:
            return False
        return super(ClearPrinted, self).get_action_permission(
            ar, obj, state)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        if obj.printed_by is None:
            ar.error(_("Oops, the print cache was already cleared."))
            return

        def ok(ar2):
            obj.clear_cache()
            ar2.success(_("Print cache file has been cleared."), refresh=True)
        if False:
            ar.confirm(
                ok,
                _("Going to clear the print cache file of %s") %
                dd.obj2unicode(obj))
        else:
            ok(ar)


class Certifiable(dd.Model):
    """Any model which inherits from this mixin becomes "certifiable".
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

      Note that this field is a nullable ForeignKey with `on_delete
      <https://docs.djangoproject.com/en/1.8/ref/models/fields/#django.db.models.ForeignKey.on_delete>`__
      set to ``SET_NULL``.

    """
    class Meta:
        abstract = True

    printed_by = dd.ForeignKey(
        'excerpts.Excerpt',
        verbose_name=_("Printed"),
        editable=False,
        related_name="%(app_label)s_%(class)s_set_as_printed",
        blank=True, null=True, on_delete=models.SET_NULL)

    clear_printed = ClearPrinted()

    def disabled_fields(self, ar):
        if self.printed_by_id is None:
            return set()
        return self.CERTIFIED_FIELDS

    def on_duplicate(self, ar, master):
        """After duplicating e.g. a budget which had been printed, we don't
        want the duplicate point to the same
        excerpt. :meth:`lino.mixins.duplicable.Duplicable.on_duplicate`.

        """
        super(Certifiable, self).on_duplicate(ar, master)
        self.printed_by = None

    @classmethod
    def on_analyze(cls, site):
        # Contract.user.verbose_name = _("responsible (DSBE)")
        cls.CERTIFIED_FIELDS = dd.fields_list(
            cls,
            cls.get_certifiable_fields())
        super(Certifiable, cls).on_analyze(site)

    @classmethod
    def get_printable_demo_objects(cls, excerpt_type):
        """Return an iterable of database objects for which Lino should
        generate a printable excerpt.

        This is being called by
        :mod:`lino.modlib.excerpts.fixtures.demo2`.

        """

        qs = cls.objects.all()
        if qs.count() > 0:
            yield qs[0]

    @classmethod
    def get_certifiable_fields(cls):
        """
        Expected to return a string with a space-separated list of field
        names.  These files will automaticaly become disabled (readonly)
        when the document is "certified". The default implementation
        returns an empty string, which means that no field will become
        disabled when the row is "certified".

        For example::

          @classmethod
          def get_certifiable_fields(cls):
              return 'date user title'

        """
        return ''

    @dd.displayfield(_("Printed"))
    def printed(self, ar):
        if ar is None:
            return ''
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

    def get_excerpt_templates(self, bm):
        """Return either None or a list of template names."""
        return None


class ExcerptTitle(BabelNamed):
    """Mixin for models like
    :class:`lino_welfare.modlib.aids.models.AidType` and
    :class:`lino.modlib.courses.models.Line`.

    .. attribute:: name

        The designation of this row as seen by the user e.g. when
        selecting an instance of this model.

        One field for every :attr:`language <lino.core.site.Site.language>`.

    .. attribute:: excerpt_title

        The text to print as title in confirmations.
        One field for every :attr:`language <lino.core.site.Site.language>`.
        If this is empty, then :attr:`name` is used.

    """
    class Meta:
        abstract = True

    excerpt_title = dd.BabelCharField(
        _("Excerpt title"),
        max_length=200,
        blank=True,
        help_text=_(
            "The title to be used when printing an excerpt."))

    def get_excerpt_title(self):
        return dd.babelattr(self, 'excerpt_title') or unicode(self)

