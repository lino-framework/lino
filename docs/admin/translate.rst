=============================
Instructions pour traducteurs
=============================

En principe c'est facile: 

- Tu édites une série de fichiers `.po` (voir plus bas)
  soit à la main, soit en utilisant un éditeur po comme 
  `poEdit <http://www.poedit.net/>`_
  
- Tu m'envoyes les fichiers édités pour que je les mette dans 
  le répertoire googlecode. Soit un fichier à la fois par e-mail.
  Et puis tu feras un 'pull' (:doc:`/admin/upgrade`) 
  et optionellement un nouveau 'initdb' pour voir les résultats sur ton serveur.
  
- Une alternative plus efficace serait de directement travailler sur ta copie 
  du code source et de m'envoyer un patch.
  
Voici la liste des fichiers `.po`:

- lino.apps.dsbe :
  `fr <http://lino.googlecode.com/hg/lino/apps/dsbe/locale/fr/LC_MESSAGES/django.po>`__
  `nl <http://lino.googlecode.com/hg/lino/apps/dsbe/locale/nl/LC_MESSAGES/django.po>`__
  
- `lino.modlib.notes`:
  `fr <http://lino.googlecode.com/hg/lino/modlib/notes/locale/fr/LC_MESSAGES/django.po>`__
  `nl <http://lino.googlecode.com/hg/lino/modlib/notes/locale/nl/LC_MESSAGES/django.po>`__

- `lino.modlib.contacts`:
  `fr <http://lino.googlecode.com/hg/lino/modlib/contacts/locale/fr/LC_MESSAGES/django.po>`__
  `nl <http://lino.googlecode.com/hg/lino/modlib/contacts/locale/nl/LC_MESSAGES/django.po>`__

- `lino.modlib.uploads`:
  `fr <http://lino.googlecode.com/hg/lino/modlib/uploads/locale/fr/LC_MESSAGES/django.po>`__
  `nl <http://lino.googlecode.com/hg/lino/modlib/uploads/locale/nl/LC_MESSAGES/django.po>`__

- `lino.modlib.links`:
  `fr <http://lino.googlecode.com/hg/lino/modlib/links/locale/fr/LC_MESSAGES/django.po>`__
  `nl <http://lino.googlecode.com/hg/lino/modlib/links/locale/nl/LC_MESSAGES/django.po>`__

- `lino.modlib.thirds`:
  `fr <http://lino.googlecode.com/hg/lino/modlib/thirds/locale/fr/LC_MESSAGES/django.po>`__
  `nl <http://lino.googlecode.com/hg/lino/modlib/thirds/locale/nl/LC_MESSAGES/django.po>`__

- `lino.modlib.properties`:
  `fr <http://lino.googlecode.com/hg/lino/modlib/properties/locale/fr/LC_MESSAGES/django.po>`__
  `nl <http://lino.googlecode.com/hg/lino/modlib/properties/locale/nl/LC_MESSAGES/django.po>`__


Trucs et astuces
----------------

Voici un pitfall: la traduction du string suivant::

  msgid "%(person)s has been unregistered from %(course)s"
  
ne doit pas être::

  msgstr "%(personne)s a été désinscrit du %(cours)"

mais bien::

  msgstr "%(person)s a été désinscrit du %(course)s"

C.-à-d. les mots-clés entre parenthèses sont des variables, 
et il *ne faut pas* les modifier.

À noter également que le ``s`` derrière la parenthèse ne sera pas 
imprimé mais est obligatoire 
(il indique à Python qu'il s'agit d'un remplacement de type `string`).
