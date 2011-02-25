Patches that I suggest for Django
=================================

Files in :srcref:`/patches`:

:file:`10808b-r14404.diff` (`10808*.diff`) : 
    My suggestion for fixing 
    :djangoticket:`10808`
    (Multiple inheritance (model-based) broken for __init__ of common fields in diamond inheritance).
    In Django revision 14404 this wasn't yet included.
    This patch is necessary to run :mod:`lino.sites.igen`, otherwise you'll get a case of :doc:`/tickets/11`.
    This patch currently fails to patch the tests (which isn't a major problem for Lino).
    See :doc:`/blog/2011/0225`


:file:`20091107.diff` : 

    This patch is not necessary to run Lino, but I find it useful when developing Django applications.
    My suggestion for fixing `Django ticket #11696 <http://code.djangoproject.com/ticket/11696>`_ (validate command in 1.1 hides errors in models that used to be shown)
    In Django revision 12394 this wasn't yet included.

:srcref:`/patches/extjs_checkboxes.diff` :

    Not necessary to run Lino.  See :doc:`/blog/2011/0225`


How to install these patches:

  * We suppose you have followind the instructions in :doc:`/admin/install`.

  * Execute the following::
  
      $ cd /var/snapshots/django
      $ patch -p0 < /var/snapshots/lino/patches/10808b.diff
      $ patch -p0 < /var/snapshots/lino/patches/20091107.diff
  
How to uninstall these patches:

    $ cd /var/snapshots/django
    $ svn revert . -R
