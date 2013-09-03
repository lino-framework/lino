.. _lino.tutorial.pisa:

Printing using Pisa
-------------------

Continued from :ref:`lino.tutorial.human` 

We have Person model inherit from `dd.Printable`:

.. literalinclude:: models.py


We create a template:
:srcref:`/docs/tutorials/pisa/config/Default.pisa.html`

That's basically all. 

:srcref:`/docs/tutorials/pisa/pisa.Person-1.pdf`
shows what you would see when clicking on 
the Print button of a Person.

The following code snippets are to 
verify that our example actually works and to show how you can do 
such things using scripts.

Note that you need to manually add `pip install pisa`.


>>> from __future__ import print_function 
>>> from lino.runtime import *
>>> from django.test import Client
>>> from tutorials.pisa.models import Person

Must set default_build_method to pisa because otherwise Lino would 
use `appyodt`

>>> settings.SITE.site_config.update(default_build_method = 'pisa')

Let's install our well-known demo root users:

>>> from lino.modlib.system.fixtures.demo import objects
>>> for obj in objects(): 
...     obj.save()

Or here is another demo user:

>>> anna = users.User(username='anna',profile='100',first_name="Anna",last_name="Andante")
>>> anna.save()

Create a Person:

>>> pisa.Person(first_name="Jean",last_name="Dupont").save()

Start a scripting session as `robin`

>>> ses = settings.SITE.login('robin',subst_user=anna)

Get our Person:

>>> obj = pisa.Person.objects.get(pk=1)

Run the Print action:

>>> rv = ses.run(obj.do_print)

Check the result:

>>> print(rv) #doctest: +NORMALIZE_WHITESPACE
{'open_url': u'/media/cache/pisa/pisa.Person-1.pdf', 'success': True}


Since the media/cache directory is not part of the Lino repository, 
we add the following code to copies the resulting file to a public place:

>>> import shutil
>>> base = 'docs/tutorials/pisa/'
>>> shutil.copyfile(
...    base + 'media/cache/pisa/pisa.Person-1.pdf',
...    base + 'pisa.Person-1.pdf')


