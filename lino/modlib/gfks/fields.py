# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Extended fields for use with `lino.modlib.gfks`.
"""
from builtins import str

from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey \
    as DjangoGenericForeignKey

from lino.utils.choosers import chooser
from lino.core.utils import full_model_name


class GenericForeignKey(DjangoGenericForeignKey):

    """Add verbose_name and help_text to Django's GFK.

    Used by
    :class:`lino.modlib.gfks.mixins.Controllable`.

    """

    def __init__(self, ct_field="content_type", fk_field="object_id",
                 verbose_name=None, help_text=None, dont_merge=False):
        self.verbose_name = verbose_name
        self.help_text = help_text
        self.dont_merge = dont_merge
        DjangoGenericForeignKey.__init__(self, ct_field, fk_field)

    def contribute_to_class(self, cls, name):
        """Automatically setup chooser and display field for ID field of
        generic foreign key.

        """

        super(GenericForeignKey, self).contribute_to_class(cls, name)

        # Chooser
        fk_choices_name = "{fk_field}_choices".format(fk_field=self.fk_field)
        if not hasattr(cls, fk_choices_name):
            def fk_choices(obj, **kwargs):
                object_type = kwargs[self.ct_field]
                if object_type:
                    return object_type.model_class().objects.all()
                return []
            field = chooser(instance_values=True)(fk_choices)
            setattr(cls, fk_choices_name, field)

        # Display
        fk_display_name = "get_{fk_field}_display".format(
            fk_field=self.fk_field)
        if not hasattr(cls, fk_display_name):
            def fk_display(obj, value):
                ct = getattr(obj, self.ct_field)
                if ct:
                    try:
                        return str(ct.get_object_for_this_type(pk=value))
                    except ct.model_class().DoesNotExist:
                        return "%s with pk %r does not exist" % (
                            full_model_name(ct.model_class()), value)
            setattr(cls, fk_display_name, fk_display)


class GenericForeignKeyIdField(models.PositiveIntegerField):

    """Use this instead of `models.PositiveIntegerField` for fields that
    are part of a :term:`GFK` and you want Lino to render them using a
    Combobox.

    Used by :class:`lino.modlib.gfks.mixins.Controllable`.

    Note: `type_field` is a mandatory argument, but you can specify
    anything because it is being ignored.

    """

    def __init__(self, type_field, *args, **kw):
        self.type_field = type_field
        models.PositiveIntegerField.__init__(self, *args, **kw)

    def deconstruct(self):
        # needed for Django 1.7
        # https://docs.djangoproject.com/en/dev/howto/custom-model-fields/#custom-field-deconstruct-method

        name, path, args, kwargs = super(
            GenericForeignKeyIdField, self).deconstruct()
        args = [self.type_field]
        return name, path, args, kwargs


