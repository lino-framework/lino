# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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
This is a "reloadable" fixture. If you say::

  python manage.py loaddata web
  
it will overwrite existing web pages.

"""

from __future__ import unicode_literals

from django.conf import settings

from lino.modlib.pages.builder import Page, objects    

    
class Index(Page):
    """
    Welcome to the **{{LINO.title}}** site.
    We are running 
    `{{LINO.short_name}} <{{LINO.url}}>`__
    version {{LINO.version}}, {{LINO.description}}
    
    {% if settings.LINO.admin_url %}
    
    You are currently seeing the **web content** section,
    which contains just this default index page 
    because this site hasn't been configured to show something else here.
    
    To see what Lino really adds to a Django site, 
    you should go to the **Admin** section.
    
    {% endif %}
    """
    language = 'en'
    
    

class Index(Page):
    """
    Bienvenue sur **{{LINO.title}}**.
    Ce site est une démonstration en ligne de
    `{{LINO.short_name}} <{{LINO.url}}>`__
    version {{LINO.version}}, {{LINO.description}}
    
    {% if settings.LINO.admin_url %}
    
    Ceci est la section "web public" qui ne contient que cette page bidon
    parce que ce site n'a pas été configuré pour montrer plus d'information ici.
    
    Pour voir ce que Lino ajoute à Django, vous devriez maintenant aller 
    dans la section Admin.
    
    {% endif %}
    """
    language = 'fr'
    #~ raw_html = True
    

class Index(Page):
    """
    Willkommen auf {{LINO.title}}.
    Diese Site ist eine Online-Demo von
    `{{LINO.short_name}} <{{LINO.url}}>`__
    version {{LINO.version}}, {{LINO.description}}
    
    {% if settings.LINO.admin_url %}
    
    Dies hier ist der öffentliche Bereich mit frei konfigurierbarem Webinhalt.
    Um das Besondere an Lino zu sehen, sollten Sie nun auf den 
    Link **Admin** oben rechts klicken.
   
    {% endif %}
    
    """
    language = 'de'
    
    
class About(Page):
    """
    This website is a life demonstration of 
    <a href="{{LINO.url}}">{{LINO.short_name}}</a> 
    version {{LINO.version}}, {{LINO.description}}.
    """
    title = "About"
    #~ raw_html = True
    language = 'en'
    
    
class Admin(Page):
    """
    You have entered the **admin** section.
    Unlike the `web content section </>`__ there is now a GUI menu 
    bar in the upper part of the screen.
    
    You will now probably want to 
    use the :guilabel:`Log in` button in the upper right corner 
    and log in. 
    
    This demo site has 
    {{LINO.modules.users.UsersOverview.request().get_total_count()}}
    users configured, they all have "1234" as password:
    
    {{as_ul('users.UsersOverview')}}
    
    
    Enjoy!
    Your feedback is welcome to lino-users@googlegroups.com
    or directly to the person who invited you.
    
    """
    special = True
    
class Admin(Page):
    """
    Sie sind im Verwaltungsbereich ("admin").
    Bitte klicken Sie jetzt auf :guilabel:`Anmelden` in der oberen rechten 
    Bildschirmecke, um sich anzumelden.
    
    Auf dieser Demo-Site gibt es
    {{LINO.modules.users.UsersOverview.request().get_total_count()}}
    Benutzer, die alle "1234" als Passwort haben:
    
    {{as_ul('users.UsersOverview')}}
    
    Viel Spaß!
    Reaktionen und Kommentare sind willkommen an lino-users@googlegroups.com
    oder direkt die Person, die Sie eingeladen hat.
    
    
    """
    language = 'de'
    special = True

class Admin(Page):
    """
    Veuillez cliquer maintenant sur le bouton :guilabel:`Log in`
    dans le coin supérieur droit de l'écran.
    
    Sur ce site démo il y a 
    {{LINO.modules.users.UsersOverview.request().get_total_count()}} 
    utilisateurs, tous avec "1234" comme mot de passe:
    
    {{as_ul('users.UsersOverview')}}
    
    Vos commentaires sont les bienvenus sur lino-users@googlegroups.com
    oubien directement à la personne qui vous a invitée.
    """
    language = 'fr'
    special = True
    

def unused_objects():
    #~ yield pages.page("hello","Hello","""\
#~ The hello page.    
    #~ """)

    WEB_INDEX = pages.page("",
        body="""\
    <p>
    Welcome to the <b>[=LINO.title]</b> site.
    We are running <a href="[=LINO.url]">[=LINO.short_name]</a> 
    version [=LINO.version], [=LINO.description]
    </p>
    """)
    ADMIN_INDEX = pages.page("admin",body=WEB_INDEX.body)
        
    if 'fr' in babel.AVAILABLE_LANGUAGES:
        WEB_INDEX_FR = pages.page("",'fr',
            body=u"""\
        <p>
        Bienvenue sur <b>[=LINO.title]</b>.
        Ce site utilise <a href="[=LINO.url]">[=LINO.short_name]</a> 
        version [=LINO.version], [=LINO.description]
        </p>
        """)
        ADMIN_INDEX_FR = pages.page("admin",'fr',body=WEB_INDEX_FR.body)
        
    if 'de' in babel.AVAILABLE_LANGUAGES:
        WEB_INDEX_DE = pages.page("",'de',body=u"""\
        <p>
        Willkommen auf <b>[=LINO.title]</b>.
        Diese Site benutzt <a href="[=LINO.url]">[=LINO.short_name]</a> 
        version [=LINO.version], [=LINO.description]
        </p>
        """)
        ADMIN_INDEX_DE = pages.page("admin",'de',body=WEB_INDEX_DE.body)


    if settings.LINO.admin_url:
      
        if settings.LINO.user_model is None:
            raise Exception("When admin_url is not empty, user_model cannot be None")
            
        WEB_INDEX.body += """
        <p>
        You are currently seeing the <strong>web content</strong> section,
        which contains just this default index page 
        because this site hasn't been configured to show something else here.
        </p>
        <p>
        To see what Lino really adds to a Django site, 
        you should go to the <strong>admin</strong> section.
        </p>
        <p align="center"><button onclick="document.location='/admin/'">admin</button></p>
        """


    if settings.LINO.admin_url:
      
        ADMIN_INDEX.body += """
        <p>
        You have entered the admin section. 
        </p>
        """
        
    ADMIN_INDEX.body += """
    <p>
    You will now probably want to 
    use the <strong>Login</strong> button in the upper right corner 
    and log in. 
    </p><p>
    This demo site has 
    [=LINO.modules.users.UsersOverview.request().get_total_count()] 
    users configured, they all have "1234" as password:
    </p>
    """
    
    users_overview = "[ul users.UsersOverview]"
    #~ users_overview = """
    #~ <ul>
    #~ [="".join(['<li><strong>%s</strong> : %s, %s, <strong>%s</strong></li>' % (\
      #~ u.username, u, u.profile, babel.LANGUAGE_DICT.get(u.language)) \
      #~ for u in LINO.modules.users.UsersOverview.request()])] 
    #~ </ul>
    #~ """
    
    ADMIN_INDEX.body += users_overview
    
    
    if 'de' in babel.AVAILABLE_LANGUAGES:
        ADMIN_INDEX_DE.body += u"""
        <p>
        Bitte klicken Sie jetzt auf <strong>Anmelden</strong> in der oberen rechten 
        Bildschirmecke, um sich anzumelden.
        </p><p>
        Auf dieser Demo-Site gibt es
        [=LINO.modules.users.UsersOverview.request().get_total_count()] 
        Benutzer, die alle "1234" als Passwort haben:
        </p>
        """
        ADMIN_INDEX_DE.body += users_overview

    if 'fr' in babel.AVAILABLE_LANGUAGES:
        ADMIN_INDEX_FR.body += u"""
        <p>
        Veuillez cliquer maintenant sur le bouton <strong>Log in</strong> 
        dans le coin supérieur droit de l'écran.
        </p><p>
        Sur ce site démo il y a 
        [=LINO.modules.users.UsersOverview.request().get_total_count()] 
        utilisateurs, tous avec "1234" comme mot de passe:
        </p>
        """
        ADMIN_INDEX_FR.body += users_overview



    if settings.LINO.admin_url:
      
        ADMIN_INDEX.body += """
        <p>
        Or you might want to return to the <a href="/">web content section</a>.
        </p>
        """

    #~ </p><p>
    #~ [=LINO.modules.users.UsersOverview.to_html()]


    WEB_INDEX.body += """
    <p>
    Enjoy!
    Your feedback is welcome to lino-users@googlegroups.com
    or directly to the person who invited you.
    </p>
    """

    if 'de' in babel.AVAILABLE_LANGUAGES:
        WEB_INDEX_DE.body += u"""
        <p>
        Viel Spaß!
        Reaktionen und Kommentare sind willkommen an lino-users@googlegroups.com
        oder direkt die Person, die Sie eingeladen hat.
        </p>
        """

    if 'fr' in babel.AVAILABLE_LANGUAGES:
        WEB_INDEX_FR.body += """
        <p>
        Enjoy!
        Your feedback is welcome to lino-users@googlegroups.com
        or directly to the person who invited you.
        </p>
        """


    #~ WEB_INDEX.body += """
    #~ <iframe src="https://www.facebook.com/plugins/like.php?href=[=LINO.site_url]"
            #~ scrolling="no" frameborder="0"
            #~ style="border:none; width:450px; height:80px"></iframe>
    #~ """


    yield WEB_INDEX
    yield ADMIN_INDEX
    
    if 'de' in babel.AVAILABLE_LANGUAGES:
        yield WEB_INDEX_DE
        yield ADMIN_INDEX_DE
    if 'fr' in babel.AVAILABLE_LANGUAGES:
        yield WEB_INDEX_FR
        yield ADMIN_INDEX_FR