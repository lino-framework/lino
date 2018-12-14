# -*- coding: UTF-8 -*-
# Copyright 2008-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from builtins import str

from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey \
    as DjangoGenericForeignKey

from lino.utils.choosers import chooser
from lino.core.utils import full_model_name


class GenericForeignKey(DjangoGenericForeignKey):

    def __init__(self, ct_field="content_type", fk_field="object_id",
                 verbose_name=None, help_text=None, dont_merge=False):
        self.verbose_name = verbose_name
        self.help_text = help_text
        self.dont_merge = dont_merge
        DjangoGenericForeignKey.__init__(self, ct_field, fk_field)

    def contribute_to_class(self, cls, name):
        # Automatically setup chooser and display field for ID field of
        # generic foreign key.

        super(GenericForeignKey, self).contribute_to_class(cls, name)

        # Chooser
        fk_choices_name = "{fk_field}_choices".format(fk_field=self.fk_field)
        if not hasattr(cls, fk_choices_name):
            def fk_choices(obj, *args):
                # print 20160830, obj, args
                object_type = args[0]
                if object_type:
                    return object_type.model_class().objects.all()
                return []
            field = chooser(
                instance_values=True,
                context_params=[self.ct_field])(fk_choices)
            # field.context_params = [self.fk_field]
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


