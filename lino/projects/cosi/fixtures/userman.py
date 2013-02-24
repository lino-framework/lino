# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
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
The Lino Così User Manual

"""

from __future__ import unicode_literals

from django.conf import settings

from lino.modlib.pages.builder import page, objects

page('userman','de','Lino Così Benutzerhandbuch',"""

""")
    
page('contacts','de','Kontakte verwalten',"""

Im Menü :menuselection:`Kontakte`
haben wir drei Befehle:
:menuselection:`Kontakte --> Personen`,
:menuselection:`Kontakte --> Organisationen`
und
:menuselection:`Kontakte --> Partner`.

In Lino Così müssen Empfänger von Verkaufsrechnungen und Absender 
von Einkaufsrechnungen *zumindest* als "Partner" erfasst werden. 
Ein Partner ist normalerweise entweder eine Organisation 
(Firma, Institution,...) oder eine Person.
Theoretisch kann er auch beides zugleich sein:
Zum Beispiel kann ein befreundeter selbstständiger 
Schreiner zugleich Person und Organisation (Einzelunternehmen) sein.

Ein Partner kann (noch theoretischer) auch weder Person noch Organisation 
sein: zum Beispiel eine Verteilerliste.

""",parent='userman')
    
page('products','de','Produkte verwalten',"""
Produkte sind alle Dinge, die Sie verkaufen wollen.
Also das können auch Dienstleistungen sein. 
Ein Produkt hat eine Bezeichnung und einen Stückpreis.

Wenn Sie viele Produkte haben, können Sie diese 
optional in Kategorien ordnen.
""",parent='userman')
    
page('orders','de','Aufträge',"""
""",parent='userman')
    
page('sales_invoices','de','Verkaufsrechnungen',"""
""",parent='userman')
    
page('purchases','de','Einkaufsrechnungen',"""
""",parent='userman')
    
page('vat','de','MWSt-Erklärung',"""
""",parent='userman')
    
page('bank','de','Kasse und Bankkonten',"""
""",parent='userman')
    
    
