======================================
Everything about cached temporary data
======================================

In :doc:`/dev/install` we told you to set up an environment variable
:envvar:`LINO_CACHE_ROOT` which points to a directory where Lino can
store temporary files like the SQLite database file, static files and
dynamically generated files of miscellaneous types like `.js`, `.pdf`,
`.xls`.


.. envvar:: LINO_CACHE_ROOT

If an environment variable :envvar:`LINO_CACHE_ROOT` is set, then the
cached data of demo projects (the :xfile:`default.db` files and the
:xfile:`media` directories) are not written into the file tree of the
source code repository but below the given directory.  See
:attr:`atelier.fablib.env.demo_projects`.

For example you can add the following line to your :file:`.bashrc`
file::

  export LINO_CACHE_ROOT=/home/luc/tmp/cache

Note that the path should be absolute and without a ``~``.


When to update your static files
================================

Lino comes with over 4000 static files, and together they take about
50 MB of hard disk storage. To manage them, it uses Django's
`staticfiles
<https://docs.djangoproject.com/en/1.6/ref/contrib/staticfiles/>`_ app
which provides the :manage:`collectstatic` command.

.. management_command :: collectstatic

    The :manage:`collectstatic` command copies miscellaneous static
    files to a central place where the web server will find them.
    This is standard Django know-how.  See the documentation about the
    `staticfiles
    <https://docs.djangoproject.com/en/1.6/ref/contrib/staticfiles/>`_
    app.

Django applications expect static files to be stored in a central
directory pointed to by :setting:`STATIC_ROOT`. And the development
server automatically serves them at the location defined in
:setting:`STATIC_URL`.

Lino automatically sets :setting:`STATIC_ROOT` to a directory named
:file:`collectstatic` under your :envvar:`LINO_CACHE_ROOT`.

As we said in :doc:`/tutorials/hello/index`, before you can see your
first Lino application running in a web server on your machine, you
must run Django's :manage:`collectstatic` command::

    $ python manage.py collectstatic

Theoretically you need to do this only for your first local Lino
project, but you should run :manage:`collectstatic` again:

- after a Lino upgrade 
- when you changed your :envvar:`LINO_CACHE_ROOT`
- if you use a plugin with static files for the first time

The following built-in plugins have static files:

- :mod:`lino.modlib.lino`
- :mod:`lino.modlib.extjs`
- :mod:`lino.modlib.extensible`
- :mod:`lino.modlib.bootstrap3`
- :mod:`lino.modlib.davlink`
- :mod:`lino.modlib.beid`
- :mod:`lino.modlib.tinymce`

You can run the :manage:`collectstatic` command as often as you want.
So if you are in doubt, just run it again.



Site settings
=============

Some attributes of your :class:`Site <lino.core.site.Site>` instance
which are related to this topic:

.. currentmodule:: lino.core.site

- :attr:`never_build_site_cache <Site.never_build_site_cache>`
- :attr:`build_js_cache_on_startup <Site.build_js_cache_on_startup>`
- :attr:`keep_erroneous_cache_files <Site.keep_erroneous_cache_files>`



Django settings
===============

Some Django settings related to this topic:

.. setting:: STATIC_ROOT

    The root directory where static files are to be collected when the
    `collectstatic` command is run.  See `Django doc
    <https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-STATIC_ROOT>`__.

    This is not needed as long as you work on a development server
    because the developement server serves static files automagically.

    If this is not set, Lino sets an intelligent default value for it
    as follows.

    When :envvar:`LINO_CACHE_ROOT` is set, the default value for
    :setting:`STATIC_ROOT` is a subdir named :file:`collectstatic` of
    :envvar:`LINO_CACHE_ROOT`.  Otherwise it is set to a subdir named
    :file:`static` of the :attr:`cache_dir
    <lino.core.site.Site.cache_dir>`.


.. setting:: MEDIA_ROOT

    The root directory of the media files used on this site.  If the
    directory specified by :setting:`MEDIA_ROOT` does not exist, then Lino
    does not create any cache files. Which means that the web interface
    won't work.

    Used e.g. by :mod:`lino.utils.media` :mod:`lino.modlib.extjs` and
    :mod:`lino.mixins.printable`.

