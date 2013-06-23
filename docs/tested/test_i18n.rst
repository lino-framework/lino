.. _lino.tested.i18n:

===================================================
Code snippets for testing Lino's i18n
===================================================

General stuff:

>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.i18n.settings'
>>> from lino.runtime import *
>>> from django.test import Client
>>> client = Client()
>>> ses = settings.SITE.login('robin')

Users Overview in different languages
=====================================

We use the `users.UsersOverview` table for testing some 
basic i18n functionality.
Since we are interested only in the column headers and not to see 
all users, we add a filter:

>>> kw = dict(known_values=dict(username='robin'))

The non-translated result is:

>>> ses.show('users.UsersOverview',language='en',**kw)
========== =============== ==========
 Username   User Profile    Language
---------- --------------- ----------
 robin      Administrator   en
========== =============== ==========
<BLANKLINE>

Now we look at this table in different languages:

>>> ses.show('users.UsersOverview',language='de',**kw)
============== ================ =========
 Benutzername   Benutzerprofil   Sprache
-------------- ---------------- ---------
 robin          Verwalter        en
============== ================ =========
<BLANKLINE>


>>> ses.show('users.UsersOverview',language='fr',**kw)
=================== ====================== ========
 Nom d'utilisateur   Profil d'utilisateur   Langue
------------------- ---------------------- --------
 robin               Administrateur         en
=================== ====================== ========
<BLANKLINE>

>>> ses.show('users.UsersOverview',language='et',**kw)
============== ================= ======
 Kasutajanimi   Kasutajaprofiil   Keel
-------------- ----------------- ------
 robin          Administrator     en
============== ================= ======
<BLANKLINE>


>>> ses.show('users.UsersOverview',language='pt',**kw)
================= =================== ========
 Nome de usuário   Perfil do usuário   Idioma
----------------- ------------------- --------
 robin             Administrador       en
================= =================== ========
<BLANKLINE>

>>> ses.show('users.UsersOverview',language='pt-br',**kw)
================= =================== ========
 Nome de usuário   Perfil do usuário   Idioma
----------------- ------------------- --------
 robin             Administrador       en
================= =================== ========
<BLANKLINE>

