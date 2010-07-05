Patches that I suggest for Django
=================================

Files in :srcref:`/patches`:

10808b.diff : 
    My suggestion for fixing `Django ticket #10808 <http://code.djangoproject.com/ticket/10808>`_ (Multiple inheritance (model-based) broken for __init__ of common fields in diamond inheritance).
    In Django revision 12394 this wasn't yet included.
    This patch is necessary to run Lino, otherwise you'll get a traceback that ends like this::

        File "/var/snapshots/django/django/forms/models.py", line 821, in _get_foreign_key
          return fk
      UnboundLocalError: local variable 'fk' referenced before assignment


20091107.diff : 

    My suggestion for fixing `Django ticket #11696 <http://code.djangoproject.com/ticket/11696>`_ (validate command in 1.1 hides errors in models that used to be shown)
    In Django revision 12394 this wasn't yet included.
    This patch is not necessary to run Lino.


How to install these patches:

  * We suppose you have done HowToInstall.

  * Execute the following::
  
      $ cd /var/snapshots/django
      $ patch -p0 < /var/snapshots/lino/patches/10808b.diff
      $ patch -p0 < /var/snapshots/lino/patches/20091107.diff
  
How to uninstall these patches:

    $ cd /var/snapshots/django
    $ svn revert . -R
