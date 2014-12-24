====================================
ExtJS - User Interface using ExtJS 3
====================================

.. module:: ml.extjs

This page documents the :mod:`lino.modlib.extjs` app.

It is being automatically included by every Lino application unless
you specify ``extjs`` in :meth:`lino.core.site_def.Site.get_apps_modifiers` (or
override your :meth:`lino.core.site_def.Site.get_installed_apps` method).

When your Lino application uses the ExtJS user interface, then you may
need a commercial license from Sencha if your site is (1) your
application is not available under the GPL **and** (2) used by other
people than the empoyees of the company who wrote the application. 

.. contents:: 
   :local:
   :depth: 2


Configuration
=============

.. class:: Plugin

  Extends :class:`lino.core.plugin.Plugin`. See also :doc:`/dev/ad`.

  .. attribute:: use_statusbar

    Whether to use a status bar to display certain messages to the user.
    Default is `False` since currently this is not really useful.

  .. attribute:: media_base_url

    The URL from where to include the ExtJS library files.
    
    The default value points to the `extjs-public
    <http://code.google.com/p/extjs-public/>`_ repository and thus
    requires the clients to have an internet connection.  This
    relieves newcomers from the burden of having to specify a download
    location in their :xfile:`settings.py`.
    
    On a production site you'll probably want to download and serve
    these files yourself by setting this to `None` and setting
    :attr:`extjs_root` (or a symbolic link "extjs" in your
    :xfile:`media` directory) to point to the local directory where
    ExtJS 3.3.1 is installed).

  .. attribute:: media_root

    Path to the ExtJS root directory.  Only used when
    :attr:`media_base_url` is None, and when the `media` directory has
    no symbolic link named `extjs` pointing to the ExtJS root
    directory.

