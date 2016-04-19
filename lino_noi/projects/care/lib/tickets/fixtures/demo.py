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

from lino.api import rt
from lino.utils.cycler import Cycler
from lino_noi.lib.tickets.choicelists import TicketStates

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


def T(reporter, summary, **kw):
    kw.update(
        summary=summary,
        reporter=rt.modules.users.User.objects.get(username=reporter))
    kw.update(state=STATES.pop())
    return rt.modules.tickets.Ticket(**kw)


def objects():
    yield U("anna")
    yield U("berta")
    yield U("christina")
    yield U("dora")
    yield S("Bei mir zu Hause")
    yield S("AZ Ephata")
    yield S("Eupen")

    yield F("Französischunterricht", "Cours de francais")
    yield F("Deutschunterricht", "Cours d'allemand")
    yield F("Matheunterricht", "Cours de maths")
    yield F("Gitarrenunterricht", "Cours de guitare")
    yield F("Nähen", "Couture")
    yield F("Friseur", "Coiffure")
    yield F("Gartenarbeiten", "Travaux de jardin")
    yield F("Fahrdienst", "Voiture")
    yield F("Botengänge", "Commissions")
    yield F("Babysitting", "Garde enfant")
    yield F("Gesellschafter für Senioren", "Rencontres personnes agées")
    yield F("Hunde spazierenführen", "Chiens")
    yield F("Übersetzungsarbeiten", "Traductions")
    yield F("Briefe beantworten", "Répondre au courrier")

    yield T("berta", "Mein Wasserhahn tropft, wer kann mir helfen?")
    yield T("christina",
            "Mein Rasen muss gemäht werden. Donnerstags oder Samstags")
    yield T("dora",
            "Wer kommt meinem Sohn Klavierunterricht geben?")
    yield T("berta",
            "Wer hilft meinem Sohn sich auf die Mathearbeit am "
            "21.05. vorzubereiten? 5. Schuljahr PDS.")
    yield T("dora",
            "Wer kann meine Abschlussarbeit korrekturlesen?",
            description="Für 5. Jahr RSI zum Thema \"Das "
            "Liebesleben der Kängurus\"  "
            "Muss am 21.05. eingereicht "
            "werden.")
    yield T("anna",
            "Wer fährt für mich nach Aachen Pampers kaufen?",
            description="Ich darf selber nicht über die Grenze.")

