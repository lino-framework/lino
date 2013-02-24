============================
Instructions for translators
============================

Here is how your can help translating Lino into your own language.

Basically it's easy: 

- you edit a series of :xfile:`.po` files, 
  (see below) using either your preferred plain text editor 
  or a tool like `Poedit <http://www.poedit.net>`_.

- Tu m'envoyes les fichiers édités pour que je les mette dans 
  le répertoire googlecode. Soit un fichier à la fois par e-mail.
  Et puis tu feras un 'pull' (:doc:`/admin/upgrade`) 
  et optionellement un nouveau 'initdb' pour voir les résultats sur ton serveur.
  
- Une alternative plus efficace serait de directement travailler sur ta copie 
  du code source et de m'envoyer un patch.
  
Which files to edit?
--------------------

(TODO: how to easily publish a list of all `.po` files used by a project)


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
