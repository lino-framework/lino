# -*- coding: UTF-8 -*-
# Copyright 2008-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from django.utils.translation import ugettext_lazy as _
from lino.core.choicelists import ChoiceList


class YesNo(ChoiceList):

    """
    Used to define parameter panel fields for BooleanFields::
    
      foo = dd.YesNo.field(_("Foo"),blank=True)
      
    """
    # app_label = 'lino'
    verbose_name_plural = _("Yes or no")
add = YesNo.add_item
add('y', _("Yes"), 'yes')
add('n', _("No"), 'no')


class Genders(ChoiceList):

    """
    Defines the two possible choices "male" and "female"
    for the gender of a person.
    See :ref:`lino.tutorial.human` for examples.
    """
    verbose_name = _("Gender")
    # app_label = 'lino'
    #~ item_class = GenderItem

add = Genders.add_item
add('M', _("Male"), 'male')
add('F', _("Female"), 'female')

