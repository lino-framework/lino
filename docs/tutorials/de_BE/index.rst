==============
Ostbelgizismen
==============

I wrote this article to test and document the new support 
for :ref:`mldbc` with different variants of a same language 
on a same Site.


In our `settings.py` you can see that we have 
two variants of German in 
:attr:`languages <north.Site.languages>`: 
normal German ('de') and belgian German ('de_BE'):

.. literalinclude:: settings.py

This example site is going to show a list of differences between 
those two languages.

The site uses a single model, which is a :class:`BabelNamed 
<north.dbutils.BabelNamed>`:

.. literalinclude:: models.py

..
  >>> # encoding: utf-8
  >>> from tutorials.de_BE.models import *


Populate the database
----------------------

Now we wrote a Python fixture with some data:

.. literalinclude:: fixtures/demo.py
   :lines: 1-14

We load this fixture using Django's standard loaddata command:

>>> from django.core.management import call_command
>>> call_command('initdb_demo',interactive=False)
Creating tables ...
Creating table de_BE_expression
Installing custom SQL ...
Installing indexes ...
Installed 3 object(s) from 1 fixture(s)


Here is the result:

>>> Expressions.show()
==== ============== ================== =====================
 ID   Designation    Designation (de)   Designation (de-be)
---- -------------- ------------------ ---------------------
 1    the workshop   die Werkstatt      das Atelier
 2    the lorry      der Lastwagen      der Camion
 3    the folder     der Ordner         die Farde
==== ============== ================== =====================
<BLANKLINE>


See also

- :attr:`north.Site.languages`
- :meth:`north.Site.get_language_info`
