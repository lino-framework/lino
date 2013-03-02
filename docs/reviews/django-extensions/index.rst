=================
Django-Extensions
=================

To use `django-extensions <https://github.com/django-extensions>`_
on a Lino site:

- In your settings.py (after the :setting:`LINO` instantiation), add a line::

    INSTALLED_APPS = INSTALLED_APPS  + ('django_extensions',)
  
- In your manage.py you must add a line::
 
    import lino.runtime
    
The remainder of this article is just my personal and not very 
elaborated first impression.

Es hat einen Befehl "dumpscript", der ähnlich wie mein 
:mod:`lino.utils.dumpy` den Inhalt der Datenbank in ein 
Python-Skript schreibt, das ebendiesen Inhalt wiederherstellt.
Es ist aber klar, dass "dumpscript" eher primitiv ist und 
sich nicht für Datenbank-Migrationen eignet.
Hat sich nicht gelohnt.

Interessanter war ein anderer Befehl ``graph_models``
in dieser Bibliothek.
Hier ein paar Resultate.
Sehen schön aus, aber ehrlich gesagt 
besteht dafür jetzt auch nicht gerade 
ein dringender Bedarf...


.. graphviz:: contacts.dot

.. graphviz:: cal.dot

.. graphviz:: outbox.dot

.. graphviz:: courses.dot

The cbss module with and without ``-d``
---------------------------------------

.. graphviz:: cbss.dot

.. graphviz:: cbssd.dot

The debts module with and without ``-d``
----------------------------------------

.. graphviz:: debts.dot

.. graphviz:: debtsd.dot

The :mod:`lino.projects.cms` application
----------------------------------------

.. graphviz:: cms.dot

Um den Befehl laufen zu lassen:
Zunächst das neue Attribut :attr:`replace_django_templates 
<lino.Lino.replace_django_templates>` kurzfristig auf 
False setzen.
Denn graph_models arbeitet mit Django_Templates.
Dann die .dot-Dateien generieren::
  
  python manage.py graph_models outbox -g > outbox.dot
  
Anschließend :attr:`replace_django_templates 
<lino.Lino.replace_django_templates>` wieder zurücksetzen.

Und hier im Blog die Dateien dann mit 
`graphviz <http://sphinx-doc.org/ext/graphviz.html>`_
einbauen.

