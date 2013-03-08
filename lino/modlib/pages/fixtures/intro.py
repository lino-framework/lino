# -*- coding: UTF-8 -*-
## Copyright 2012-2013 Luc Saffre
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
This fixture defines pages `/`, `/admin` and `/about`,
with automatically generated introductory content.

Currently in English, German and French.

This is no longer a "reloadable" fixture. If you say::

  python manage.py loaddata intro
  
it will overwrite existing web pages.

"""

from __future__ import unicode_literals

from django.conf import settings

from lino.modlib.pages.builder import page, objects

page('index','en','',"""
Welcome to the **{{site.title}}** site.
{% if site.verbose_name %}
This is an online demo of `{{site.verbose_name}} <{{site.url}}>`__
version {{site.version}}.
{% endif %}

{% if site.admin_prefix %}

You are currently seeing the **web content** section,
whose content and layout are configurable using 
the normal Django techniques.

To see what Lino really adds to a Django site, 
you should go to the `Admin <{{site.admin_prefix}}/>`__ section.

{% endif %}
""")
    
    

page('index','fr','',"""
Bienvenue sur **{{site.title}}**.
{% if site.verbose_name %}
Ce site est une démonstration en ligne de
`{{site.verbose_name}} <{{site.url}}>`__
version {{site.version}}.
{% endif %}

{% if site.admin_prefix %}

Ceci est la section publique dont le layout et le contenu sont configurables
selon les techniques habituelles de Django.

Pour voir ce que Lino ajoute à Django, vous devriez maintenant aller 
dans la `section administrative <{{site.admin_prefix}}/>`__.


{% endif %}
""")
    
page('index','de','',"""
Willkommen auf {{site.title}}.
{% if site.verbose_name %}
Diese Site ist eine Online-Demo von
`{{site.verbose_name}} <{{site.url}}>`__
version {{site.version}}.
{% endif %}

{% if site.admin_prefix %}

Dies ist der öffentliche Bereich, dessen Layout 
und Inhalt frei konfigurierbar sind wie bei jeder Django-Site.

Um das Besondere an Lino zu sehen, sollten Sie nun 
in den `Verwaltungsbereich <{{site.admin_prefix}}/>`__ gehen.

{% endif %}
""")
    
    
page('about','en','About',"""
This website is a life demonstration of 
`{{site.verbose_name}} <{{site.url}}>`__.    
""")
    
page('about','fr','À propos',"""
Ce site est une démonstration en ligne de 
`{{site.verbose_name}} <{{site.url}}>`__.
""")
    
page('about','de','Info',"""
Diese Site ist eine online-Demo von `{{site.verbose_name}} <{{site.url}}>`__.
""")
    
if False:
  
    page('admin','en','',"""

    {% if not site.admin_prefix %}

    Welcome to the **{{site.title}}** site.
    We are running 
    `{{site.verbose_name}} <{{site.url}}>`__
    version {{site.version}}.

    {% endif %}

    You have entered the **admin** section.
    Unlike the `web content section </>`__ there is now a GUI menu 
    bar in the upper part of the screen.

    You will now probably want to 
    use the :guilabel:`Log in` button in the upper right corner 
    and log in. 

    This demo site has 
    {{site.modules.users.UsersOverview.request().get_total_count()}}
    users configured, they all have "1234" as password:

    {{as_ul('users.UsersOverview')}}

    Enjoy!
    Your feedback is welcome to lino-users@googlegroups.com
    or directly to the person who invited you.

    """,special = True)
        
    page('admin','de','',"""

    {% if not site.admin_prefix %}
    Willkommen auf {{site.title}}.
    Diese Site ist eine Online-Demo von
    `{{site.verbose_name}} <{{site.url}}>`__
    version {{site.version}}.
    {% endif %}

    Sie sind im Verwaltungsbereich.
    Anders als im `öffentlichen Bereich </>`__ 
    sehen Sie hier ein Menü am oberen Bildschirmrand.

    Bitte klicken Sie jetzt auf :guilabel:`Anmelden` in der oberen rechten Bildschirmecke, um sich anzumelden.

    Auf dieser Demo-Site gibt es
    {{site.modules.users.UsersOverview.request().get_total_count()}}
    Benutzer, die alle "1234" als Passwort haben:

    {{as_ul('users.UsersOverview')}}

    Viel Spaß!
    Reaktionen und Kommentare sind willkommen an lino-users@googlegroups.com oder direkt die Person, die Sie eingeladen hat.

    """,special = True)

    page('admin','fr','',"""
    {% if not site.admin_prefix %}
    Bienvenue sur **{{site.title}}**.
    Ce site est une démonstration en ligne de
    `{{site.verbose_name}} <{{site.url}}>`__
    version {{site.version}}.
    {% endif %}

    Vous êtes dans la section administrative qui,
    autrement que la `section publique </>`__ a un menu déroulant.

    Ce menu est relativement vide tant que vous ne vous êtes pas identifié.

    Veuillez vous identifier maintenant en cliquant 
    sur le bouton :guilabel:`Log in`
    dans le coin supérieur droit de l'écran.

    Sur ce site démo il y a 
    {{site.modules.users.UsersOverview.request().get_total_count()}} 
    utilisateurs, tous avec "1234" comme mot de passe:

    {{as_ul('users.UsersOverview')}}

    Vos commentaires sont les bienvenus sur lino-users@googlegroups.com
    oubien directement à la personne qui vous a invitée.
    """,special = True)
        
#~ print 20121227, __file__