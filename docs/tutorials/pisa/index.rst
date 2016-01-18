.. _lino.tutorial.pisa:

Printing using Pisa
-------------------

Continued from :ref:`lino.tutorial.human` 

We have Person model inherit from :class:`lino.mixins.printable.Printable`:

.. literalinclude:: models.py


We create a template:
:srcref:`Default.pisa.html </docs/tutorials/pisa/config/pisa/Person/Default.pisa.html>`

.. literalinclude:: config/pisa/Person/Default.pisa.html

That's basically all. 

:srcref:`docs/tutorials/pisa/pisa.Person-1.pdf`
shows what you would see when clicking on 
the Print button of a Person.

The following code snippets are to 
verify that our example actually works and to show how you can do 
such things using scripts.

Note that you need to manually add `pip install pisa`.

>>> from __future__ import print_function 
>>> from lino.api.doctest import *
>>> from pisa.models import Person

Must set `default_build_method` to ``"pisa"`` because otherwise Lino would 
use ``"appyodt"``

>>> settings.SITE.site_config.update(default_build_method='pisa')

Let's install our well-known demo root users from
:mod:`lino.modlib.users.fixtures.demo`:

>>> from lino.modlib.users.fixtures.demo import objects
>>> for obj in objects(): 
...     obj.save()

Or here is another demo user:

>>> anna = users.User(username='anna', profile='100', first_name="Anna", last_name="Andante")
>>> anna.save()

Create a Person:

>>> pisa.Person(first_name="Jean", last_name="Dupont").save()

Start a scripting session as `robin`

>>> ses = settings.SITE.login('robin', subst_user=anna)

Get our Person:

>>> obj = pisa.Person.objects.get(pk=1)

Run the Print action:

>>> rv = ses.run(obj.do_print)

Check the result:

>>> rv['success']
True

>>> print(rv['open_url'])
/media/cache/pisa/pisa.Person-1.pdf

>>> print(rv['message'])  #doctest: +NORMALIZE_WHITESPACE
Your printable document (filename pisa.Person-1.pdf) should now 
open in a new browser window. If it doesn't, please consult 
<a href="http://www.lino-framework.org/help/print.html" 
target="_blank">the documentation</a> 
or ask your system administrator.

The message contains a link to the page :doc:`/help/print`.  You can
override :attr:`lino.core.site.Site.help_url` if you want to invite users to your
own help system.

Since the `media/cache` directory is not part of the Lino repository,
we copy the resulting file to a public place:

>>> p = settings.SITE.cache_dir.child('media', 'cache', 'pisa',
...     'pisa.Person-1.pdf')
>>> import shutil
>>> shutil.copyfile(p, 'pisa.Person-1.pdf')


