.. _tutorials.de_BE:

==============
Ostbelgizismen
==============

.. How to run only this test:

  $ python setup.py test -s tests.DocsTests.test_de_BE


I wrote this article to test and document the new support 
for :ref:`mldbc` with different variants of a same language 
on a same Site.


In our :xfile:`settings.py` you can see that we have two variants of
German in :attr:`languages <lino.core.site.Site.languages>`: "normal"
('de') and "Belgian" ('de_BE'):

.. literalinclude:: settings.py

The :xfile:`models.py` file defines a single model:

.. literalinclude:: models.py

The model inherits from :class:`BabelNamed
<lino.utils.mldbc.mixins.BabelNamed>`.


This example site is going to show a list of differences between 
those two languages.


Populate the database
----------------------

Now we wrote a Python fixture with some data:

.. literalinclude:: fixtures/demo.py
   :lines: 1-14


We load this fixture using Django's standard loaddata command:

>>> from django.core.management import call_command
>>> call_command('initdb_demo', interactive=False, verbosity=0)

Here is the result:

>>> from lino.api import rt
>>> from de_BE.models import Expressions
>>> rt.show(Expressions)
==== ============== ================== =====================
 ID   Designation    Designation (de)   Designation (de-be)
---- -------------- ------------------ ---------------------
 1    the workshop   die Werkstatt      das Atelier
 2    the lorry      der Lastwagen      der Camion
 3    the folder     der Ordner         die Farde
==== ============== ================== =====================
<BLANKLINE>

See also

- :meth:`lino.core.site.Site.get_language_info`
