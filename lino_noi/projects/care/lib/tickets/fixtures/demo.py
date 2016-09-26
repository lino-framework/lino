# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
#
# This file is part of Lino Noi.
#
# Lino Noi is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Noi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Noi.  If not, see
# <http://www.gnu.org/licenses/>.


from __future__ import unicode_literals

from lino.api import rt, _
from lino.utils.cycler import Cycler
from lino_noi.lib.tickets.choicelists import TicketStates

from lino.api.dd import str2kw

STATES = Cycler(TicketStates.objects())


def U(username, **kw):
    kw.update(username=username,
              profile=rt.modules.users.UserProfiles.user)
    return rt.modules.users.User(**kw)


def F(name, name_fr, **kw):
    kw.update(name=name, name_fr=name_fr)
    return rt.modules.faculties.Faculty(**kw)


def S(name, **kw):
    kw.update(name=name)
    return rt.modules.tickets.Site(**kw)


def Topic(name, **kw):
    kw.update(**str2kw('name', name))
    return rt.modules.topics.Topic(**kw)


def T(reporter, summary, **kw):
    kw.update(
        summary=summary,
        reporter=rt.modules.users.User.objects.get(username=reporter))
    kw.update(state=STATES.pop())
    return rt.modules.tickets.Ticket(**kw)


def competence(user, faculty, **kw):
    kw.update(
        user=rt.modules.users.User.objects.get(username=user))
    kw.update(faculty=faculty)
    return rt.modules.faculties.Competence(**kw)


def objects():
    yield U("axel")
    yield U("berta")
    yield U("christa")
    yield U("dora")
    yield U("eric")

    yield S("Bei mir zu Hause")
    yield S("AZ Ephata")
    yield S("Eupen")

    TopicGroup = rt.modules.topics.TopicGroup
    lng = TopicGroup(**str2kw('name', _("Languages")))
    yield lng
    fr = Topic(_("French"), topic_group=lng)
    yield fr
    de = Topic(_("German"), topic_group=lng)
    yield de
    yield Topic(_("English"), topic_group=lng)

    # music = TopicGroup(**str2kw('name', _("Music")))
    # yield music
    # piano = Topic(_("Piano"), topic_group=music)
    # yield piano
    # guitar = Topic(_("Guitar"), topic_group=music)
    # yield guitar

    edu = F("Unterricht", "Cours")
    yield edu
    yield F("Französischunterricht", "Cours de francais", parent=edu)
    yield F("Deutschunterricht", "Cours d'allemand", parent=edu)
    math = F("Matheunterricht", "Cours de maths", parent=edu)
    yield math
    
    music = F("Musik", "Musique")
    yield music
    guitar = F("Gitarrenunterricht", "Cours de guitare", parent=music)
    yield guitar
    piano = F("Klavierunterricht", "Cours de piano", parent=music)
    yield piano

    home = F("Haus und Garten", "Maison et jardin")
    yield home

    yield F("Nähen", "Couture", parent=home)
    garden = F("Gartenarbeiten", "Travaux de jardin", parent=home)
    yield garden
    handwerk = F("Handwerksarbeiten", "Travaux de réparation", parent=home)
    yield handwerk

    yield F("Fahrdienst", "Voiture")
    commissions = F("Botengänge", "Commissions")
    yield commissions
    yield F("Friseur", "Coiffure")
    yield F("Babysitting", "Garde enfant")
    yield F("Gesellschafter für Senioren",
            "Rencontres personnes agées")
    yield F("Hunde spazierenführen", "Chiens")
    traduire = F("Übersetzungsarbeiten", "Traductions", topic_group=lng)
    yield traduire
    yield F("Briefe beantworten", "Répondre au courrier")

    yield T("berta", "Mein Wasserhahn tropft, wer kann mir helfen?",
            faculty=handwerk)
    yield T("christa",
            "Mein Rasen muss gemäht werden. Donnerstags oder Samstags")
    yield T("dora",
            "Wer kann meinem Sohn Klavierunterricht geben?",
            faculty=piano)
    yield T("axel",
            "Wer kann meiner Tochter Gitarreunterricht geben?",
            faculty=guitar)
    yield T("axel",
            "Wer macht Musik auf meinem Geburtstag am 12.12.2012 ?",
            faculty=music)
    yield T("berta",
            "Wer hilft meinem Sohn sich auf die Mathearbeit am "
            "21.05. vorzubereiten? 5. Schuljahr PDS.", faculty=math)
    yield T("dora",
            "Wer kann meine Abschlussarbeit korrekturlesen?",
            description="Für 5. Jahr RSI zum Thema \"Das "
            "Liebesleben der Kängurus\"  "
            "Muss am 21.05. eingereicht "
            "werden.")
    yield T("axel",
            "Wer fährt für mich nach Aachen Pampers kaufen?",
            description="Ich darf selber nicht über die Grenze.",
            faculty=commissions)

    yield competence('axel', traduire, topic=fr)
    yield competence('berta', traduire, topic=fr)
    yield competence('berta', traduire, topic=de)
    yield competence('axel', commissions)
    yield competence('axel', handwerk)
    yield competence('christa', piano)
    yield competence('eric', guitar)

