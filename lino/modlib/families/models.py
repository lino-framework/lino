# -*- coding: UTF-8 -*-
# Copyright 2013 Luc Saffre
"""
Database models for `lino.modlib.families`.

.. autosummary::

"""


from __future__ import unicode_literals
from builtins import object

from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.db import models


#~ from lino.modlib.families import Plugin
from lino.api import dd, rt


#~ class CoupleTypes(dd.ChoiceList):
    #~ verbose_name = _("Couple type")
    #~
#~ add = CoupleTypes.add_item
#~ add('100', _('Married'),'married')
#~ add('200', _('Wild'),'married')
#~ class LinkTypes(dd.ChoiceList):
    #~ verbose_name = _("Link type")
    #~
#~ add = LinkTypes.add_item
#~ add('100', _('Father'),'father',gender=dd.Genders.male)
#~ add('101', _('Mother'),'mother',gender=dd.Genders.female)

@dd.python_2_unicode_compatible
class Couple(dd.Model):

    class Meta(object):
        app_label = 'families'

    father = dd.ForeignKey('contacts.Person', blank=True,
                           null=True, related_name='couples_as_father')
    mother = dd.ForeignKey('contacts.Person', blank=True,
                           null=True, related_name='couples_as_mother')
    married = models.DateField(_("Married on"), blank=True, null=True)
    married_place = dd.ForeignKey(
        'countries.Place', 
        verbose_name=_("Married in"), blank=True, null=True)
    divorced = models.DateField(_("Divorced"), blank=True, null=True)

    def __str__(self):
        return "%s & %s" % (self.father or "?", self.mother or "?")


class Couples(dd.Table):
    model = Couple
    required_roles = dd.required(dd.SiteStaff)


class CoupleField(dd.VirtualField):

    """
    An editable virtual field that looks like a FK to a contacts.Person
    but is stored as a Couple instance.
    """
    editable = True

    def __init__(self, parents_name, my_attname, other_attname, verbose_name):
        self.parents_name = parents_name
        self.my_attname = my_attname
        self.other_attname = other_attname
        rt = dd.ForeignKey('contacts.Person', blank=True,
                           null=True, verbose_name=verbose_name)
        dd.VirtualField.__init__(self, rt, None)

    def set_value_in_object(self, request, obj, value):
        if value is not None:
            parents = getattr(obj, self.parents_name)
            if parents is None:
                parents = Couple(**{self.my_attname: value})
                parents.save()
                setattr(obj, self.parents_name, parents)
                obj.save()
            else:
                setattr(parents, self.my_attname, value)
                parents.save()
        else:
            parents = getattr(obj, self.parents_name)
            if parents is None:
                raise Exception("Unexpected case")
            elif getattr(parents, self.other_attname) is None:
                setattr(obj, self.parents_name, None)
                obj.save()
                parents.delete()
            else:
                setattr(parents, self.my_attname, None)
                parents.save()

    def value_from_object(self, obj, ar):
        #~ logger.info("20120118 value_from_object() %s",dd.obj2str(obj))
        parents = getattr(obj, self.parents_name)
        if parents is None:
            return None
        return getattr(parents, self.my_attname)


class Child(dd.Model):

    class Meta(object):
        app_label = 'families'
        abstract = True

    #~ parents = dd.ForeignKey(Couple,blank=True,null=True)
    #~ father = CoupleField('parents','father','mother',_("Father"))
    #~ mother = CoupleField('parents','mother','father',_("Mother"))

    father = dd.ForeignKey('contacts.Person', verbose_name=_("Father"),
                           blank=True, null=True,
                           related_name='father_for')

    mother = dd.ForeignKey('contacts.Person', verbose_name=_("Mother"),
                           blank=True, null=True,
                           related_name='mother_for')

    @dd.displayfield(_('Family'))
    def family(self, ar):
        members = []
        if self.father:
            members.append(
                [self.__class__.father.verbose_name, ': ', ar.obj2html(self.father)])
        if self.mother:
            members.append(
                [self.__class__.mother.verbose_name, ': ', ar.obj2html(self.mother)])
        return E.div(*members)
        #~ return "%s & %s" % ar.obj2html(obj) or "?",self.mother or "?")
        #~ return ar.obj2html(self.parents)

    @dd.chooser()
    def father_choices(self):
        return contacts.Person.objects.filter(gender=dd.Genders.male).order_by('last_name', 'first_name')

    @dd.chooser()
    def mother_choices(self):
        return contacts.Person.objects.filter(gender=dd.Genders.female).order_by('last_name', 'first_name')

#~ class Link(dd.Model):
    #~ parent = dd.ForeignKey('contacts.Person')
    #~ child = dd.ForeignKey('contacts.Person')
    #~ type = LinkTypes.field()


