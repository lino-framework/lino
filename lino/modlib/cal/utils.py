# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
This module deserves more documentation.

"""

from django.utils.translation import ugettext_lazy as _

from lino.utils.choicelists import ChoiceList

class EventStatus(ChoiceList):
    """A list of possible values for the `status` field of an :class:`Event`.
    """
    label = _("Event status")
    
add = EventStatus.add_item
add('0',en=u"tentative",de=u"Vorschlag",   fr=u"proposition")
add('1',en=u"confirmed",de=u"bestätigt",   fr=u"confirmé")
add('2',en=u"cancelled",de=u"storniert",   fr=u"annulé")

class TaskStatus(ChoiceList):
    """A list of possible values for the `status` field of a :class:`Task`.
    """
    label = _("Taskstatus")
    
add = TaskStatus.add_item
add('0',en=u"needs action",de=u"zu erledigen",   fr=u"à traîter")
add('1',en=u"in process",de=u"begonnen",   fr=u"commencée")
add('2',en=u"completed",de=u"erledigt",   fr=u"complétée")
add('3',en=u"cancelled",de=u"storniert",   fr=u"annulée")


class DurationUnit(ChoiceList):
    """A list of possible values for the `duration_unit` field of an :class:`Event`.
    """
    label = _("Duration unit")
    
add = DurationUnit.add_item
add('s','seconds',en=u"seconds",de=u"Sekunden",   fr=u"secondes")
add('m','minutes',en=u"minutes",de=u"Minuten",   fr=u"minutes")
add('h','hours',en=u"hours",de=u"Stunden",   fr=u"heures")
add('D','days',en=u"days",de=u"Tage",   fr=u"jours")
add('W','weeks',en=u"weeks",de=u"Wochen",   fr=u"semaines")
add('M','months',en=u"months",de=u"Monate",   fr=u"mois")
add('Y','years',en=u"years",de=u"Jahre",   fr=u"années")



class Priority(ChoiceList):
    """
    A list of possible values for the `CLASS` 
    property of a calendar component.
    """
    label = _("Access class")
    
add = Priority.add_item
add('0',en=u"undefined",de=u"nicht angegeben",   fr=u"non spécifiée")
add('1',en=u"high",de=u"hoch",   fr=u"élevée")
add('5',en=u"normal",de=u"normal",   fr=u"normale")
add('9',en=u"low",de=u"niedrig",   fr=u"basse")

#~ add('1',en=u"very urgent",de=u"sehr dringend",   fr=u"très urgent")
#~ add('2',en=u"quite urgent",de=u"recht dringend",   fr=u"relativement urgent")
#~ add('3',en=u"relatively urgent",de=u"ziemlich dringend",   fr=u"relativement urgent")
#~ add('4',en=u"relatively urgent",de=u"ziemlich dringend",   fr=u"relativement urgent")
#~ add('5',en=u"normal",de=u"normal",   fr=u"normal")
#~ add('6',en=u"not very urgent",de=u"nicht sehr niedrig",   fr=u"pas très urgent")
#~ add('7',en=u"not urgent",de=u"nicht dringend",   fr=u"pas urgent")
#~ add('8',en=u"not urgent",de=u"nicht dringend",   fr=u"pas urgent")
#~ add('9',en=u"not urgent at all",de=u"überhaupt nicht dringend",   fr=u"pas urgent du tout")

class AccessClass(ChoiceList):
    """
    A list of possible values for the `CLASS` 
    property of a calendar component.
    """
    label = _("Access class")
    
add = AccessClass.add_item
add('0',en=u"Public",de=u"Öffentlich",   fr=u"Public")
add('1',en=u"Private",de=u"Privat",   fr=u"Privé")
add('2',en=u"Confidential",de=u"Vertraulich",   fr=u"Confidentiel")


