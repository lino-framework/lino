Playing with the minimal applications
=====================================

See the files in :srcref:`/lino/tutorials/mini`.

They are designed to run directly from the Lino source code,
but if you work on them (which is what you should do in a tutorial),
your local modifications will get lost when 
you upgrade your copy of Lino (which you should do often).

If you don't want to loose the traces of your learning, 
you can copy them to some other place before editing them.
But in that case you'll need to take care about the 
Python Path and the value of DJANGO_SETTINGS_MODULE 
(the latter fortunately occurs only once, in 
:srcref:`/lino/tutorials/mini/manage.py`).

Note also that

- each time you make some change in 
  `settings.py`, you must re-run `initdb_demo`.
  
- invoking `runserver` will create `media` directory tree.

