The `djangosite_local` module
=============================

When hosting multiple Lino sites on a same host we suggest 
to create a file :file:`djangosite_local.py` 
somewhere in your :doc:`Python Path </admin/pythonpath>`.

This file might then have the following content (adapt to your needs, 
this is just to fire up your imagination):

.. code-block:: python

    # file /home/luc/mypy/djangosite_local.py
    import os, sys
    from os.path import join, split, dirname, abspath
    
    MEMORY_DB = False
    
    LOCAL_PREFIX = split(dirname(abspath(__file__)))[-1] + '.'
    # e.g. LOCAL_PREFIX will be "lino_local." 
        
    def setup_site(self):
        """
        Local settings to be applied to every Lino instance on this server.
        """
        
        self.update_settings(ADMINS=[("Robin Rood","robin@example.com")])
        self.django_settings.update(SECRET_KEY='?~hdakl123ASD%#¤/&¤')

        self.extjs_root = '/home/luc/snapshots/ext-3.3.1'
        self.eid_jslib_root = '/home/luc/mypy/lino_local/dsbe/media/beid-jslib'
        self.extensible_root  = '/home/luc/snapshots/extensible-1.0.1'
        self.bootstrap_root = '/home/luc/snapshots/bootstrap'
        
        self.use_jasmine = False

Note this line::

    self.django_settings.update(SECRET_KEY='?~hdakl123ASD%#¤/&¤')
    
It will set the same SECRET_KEY for all projects on that server.

If you prefer to use environment variables::

    import os
    def setup_site(self):
        self.django_settings.update(SECRET_KEY=os.environ.get('DJANGO_SECRET_KEY'))
