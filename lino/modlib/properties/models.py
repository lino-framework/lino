# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.properties`.

This module is deprecated.

A :class:`PropOccurence` is when a given "property owner" has a given
:class:`Property`.  "Property owner" can be anything: a person, a
company, a product, an upload, it depends on the implementation of
:class:`PropOccurence`.  For example
:mod:`lino.projects.pcsw.models.PersonProperty`.

A :class:`Property` defines the configuration of a property.

.. autosummary::

"""

import os
import cgi
import datetime

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode


from lino.core.roles import SiteStaff
from lino.api import dd, rt
from lino import mixins

from lino.core.choicelists import get_choicelist, choicelist_choices

MULTIPLE_VALUES_SEP = ','


class DoYouLike(dd.ChoiceList):
    """A list of possible answers to questions of type "How much do you
    like ...?".

    """
    verbose_name = _("Do you like?")

add = DoYouLike.add_item
add('0', _("certainly not"))
add('1', _("rather not"))
add('2', _("normally"), "default")
add('3', _("quite much"))
add('4', _("very much"))


class HowWell(dd.ChoiceList):

    """A list of possible answers to questions of type "How well ...?":
    "not at all", "a bit", "moderate", "quite well" and "very well"
    
    which are stored in the database as '0' to '4',
    and whose `__unicode__()` returns their translated text.

    """
    verbose_name = _("How well?")

add = HowWell.add_item
add('0', _("not at all"))
add('1', _("a bit"))
add('2', _("moderate"), "default")
add('3', _("quite well"))
add('4', _("very well"))


class PropType(mixins.BabelNamed):

    """
    The type of the values that a property accepts.
    Each PropType may (or may not) imply a list of choices.
    
    Examples: of property types:

    - Knowledge (Choices: "merely", "acceptable", "good", "very good",...)
    - YesNo (no choices)
    
    """
    class Meta:
        verbose_name = _("Property Type")
        verbose_name_plural = _("Property Types")

    #~ name = dd.BabelCharField(max_length=200,verbose_name=_("Designation"))

    choicelist = models.CharField(
        max_length=50, blank=True,
        verbose_name=_("Choices List"),
        choices=choicelist_choices())

    default_value = models.CharField(
        _("default value"),
        max_length=settings.SITE.propvalue_max_length,
        blank=True)
    """
    The default value to set when creating a :class:`PropertyOccurence`.
    This is currently used only in some fixture...
    """

    limit_to_choices = models.BooleanField(
        _("Limit to choices"), default=False)
    """
    not yet supported
    """

    multiple_choices = models.BooleanField(
        _("Multiple choices"), default=False)
    """
    not yet supported
    """

    @dd.chooser()
    def default_value_choices(cls, choicelist):
        if choicelist:
            return get_choicelist(choicelist).get_choices()
        return []

    def get_default_value_display(self, value):
        return self.get_text_for_value(value)

    def get_text_for_value(self, value):
        if not value:
            return ''
        if self.choicelist:
            cl = get_choicelist(self.choicelist)
            return cl.get_text_for_value(value)
        l = []
        for v in value.split(MULTIPLE_VALUES_SEP):
            try:
                pc = PropChoice.objects.get(value=v, type=self)
                v = dd.babelattr(pc, 'text')
            except PropChoice.DoesNotExist:
                pass
            l.append(v)
        return ','.join(l)

    #~ def __unicode__(self):
        #~ return dd.babelattr(self,'name')

    def choices_for(self, property):
        if self.choicelist:
            return get_choicelist(self.choicelist).get_choices()
        return [(pc.value, pc.text) for pc in
                PropChoice.objects.filter(type=self).order_by('value')]


class PropChoice(dd.Model):

    """A Choice for a given PropType.  `text` is the text to be displayed
    in combo boxes.
    
    `value` is the value to be stored in :attr:`PropValue.value`, it
    must be unique for all PropChoices of a given PropType.
    
    Choices for a given PropType will be sorted on `value` (we might
    make this more customizable if necessary by adding a new field
    `sort_text` and/or an option to sort on text instead of value)
    
    When configuring your property choices, be aware of the fact that
    existing property occurences will *not* change when you change the
    `value` of a property choice.

    """
    class Meta:
        verbose_name = _("Property Choice")
        verbose_name_plural = _("Property Choices")
        unique_together = ['type', 'value']

    type = models.ForeignKey(
        PropType, verbose_name=_("Property Type"))
    value = models.CharField(
        max_length=settings.SITE.propvalue_max_length,
        verbose_name=_("Value"))
    text = dd.BabelCharField(
        max_length=200, verbose_name=_("Designation"), blank=True)

    def save(self, *args, **kw):
        if not self.text:
            self.text = self.value
        r = super(PropChoice, self).save(*args, **kw)
        return r

    def __unicode__(self):
        return dd.babelattr(self, 'text')


class PropGroup(mixins.BabelNamed):

    """A Property Group defines a list of Properties that fit together
    under a common name.  Examples of Property Groups: Skills, Soft
    Skills, Obstacles There will be one menu entry per Group.

    """
    class Meta:
        verbose_name = _("Property Group")
        verbose_name_plural = _("Property Groups")


class Property(mixins.BabelNamed):

    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")

    group = models.ForeignKey(PropGroup)
    type = models.ForeignKey(PropType, verbose_name=_("Property Type"))


class PropertyOccurence(dd.Model):

    """A Property Occurence is when a Property occurs, possibly having a
    certain value.
    
    Abstract base class for
    | :class:`lino_welfare.modlib.cv.models.PersonProperty`,
    | :class:`lino_welfare.modlib.cv.models.WantedProperty`,
    | :class:`lino_welfare.modlib.cv.models.AvoidedProperty`,
    | ...

    """

    class Meta:
        abstract = True

    group = models.ForeignKey(PropGroup)
    property = models.ForeignKey('properties.Property')
    value = models.CharField(
        _("Value"),
        max_length=settings.SITE.propvalue_max_length,
        blank=True)

    @dd.chooser()
    def value_choices(cls, property):
        if property is None:
            return []
        return property.type.choices_for(property)

    @dd.chooser()
    def property_choices(cls, group):
        #~ print 20120212, group
        if group is None:
            return []
        return Property.objects.filter(group=group).order_by('name')

    def get_value_display(self, value):
        if self.property_id is None:
            return value
        return self.property.type.get_text_for_value(value)

    def full_clean(self):
        if self.property_id is not None:
            self.group = self.property.group
        super(PropertyOccurence, self).full_clean()

    def __unicode__(self):
        if self.property_id is None:
            return u"Undefined %s" % self.group
        # 20111111 : call unicode() because get_text_for_value returns a
        # Promise
        return unicode(self.property.type.get_text_for_value(self.value))

    #~ def __unicode__(self):
        #~ if self.property_id is None:
            #~ return u"Undefined %s" % self.group
        #~ return u'%s.%s=%s' % (
            #~ self.group,self.property,
            #~ self.property.type.get_text_for_value(self.value))


class PropGroups(dd.Table):
    required_roles = dd.required(dd.SiteStaff)
    model = PropGroup
    detail_layout = """
    id name 
    PropsByGroup
    """


class PropTypes(dd.Table):
    required_roles = dd.required(dd.SiteStaff)
    model = PropType
    detail_layout = """
    id name choicelist default_value
    ChoicesByType
    PropsByType
    """


class Properties(dd.Table):
    required_roles = dd.required(dd.SiteStaff)
    model = Property
    order_by = ['name']
    #~ column_names = "id name"


class PropsByGroup(Properties):
    master_key = 'group'


class PropsByType(Properties):
    master_key = 'type'


class PropChoices(dd.Table):
    model = PropChoice


class ChoicesByType(PropChoices):

    "Lists all PropChoices for a given PropType."
    master_key = 'type'
    order_by = ['value']
    column_names = 'value text *'


