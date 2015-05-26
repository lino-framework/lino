============
Settings API
============

This section describes Lino-specific considerations about certain
Django settings.  For introductive texts see :doc:`/dev/settings`,
:doc:`/dev/application`.


.. setting:: LOGGING
.. setting:: LOGGING_CONFIG

Lino sets :setting:`LOGGING_CONFIG` to :func:`lino.utils.log.configure` 
which is our suggetion for a lightweight flexible 
logging configuration method. If you leave :setting:`LOGGING_CONFIG` 
unchanged, you can configure your logging preferences using the 
:setting:`LOGGING` setting. Some examples::

    LOGGING = dict(filename='/var/log/lino/system.log'), level='DEBUG')
    LOGGING = dict(filename=join(SITE.project_dir, 'log', 'system.log'), level='DEBUG')
    LOGGING = dict(filename=None, level='DEBUG')

You don't *need* to use Lino's logging config. In that case, refer to
https://docs.djangoproject.com/en/dev/ref/settings/#logging-config


.. setting:: USE_L10N

Lino sets this automatically when
:attr:`lino.core.site.Site.languages` is not `None`.

See http://docs.djangoproject.com/en/dev/ref/settings/#use-l10n

.. setting:: LANGUAGE_CODE

Lino sets this automatically when
:attr:`lino.core.site.Site.languages` is not `None`.

See http://docs.djangoproject.com/en/dev/ref/settings/#language-code

.. setting:: DATABASES

Lino sets this to `SQLite` on a file `default.db` in your 
:attr:`project_dir <lino.core.site.Site.project_dir>`.

See http://docs.djangoproject.com/en/dev/ref/settings/#databases
  
.. setting:: MIDDLEWARE_CLASSES

  See http://docs.djangoproject.com/en/dev/ref/settings/#middleware_classes
  
.. setting:: LANGUAGES

Lino sets this automatically when your :attr:`SITE.languages
<lino.core.site.Site.languages>` is not `None`.

Used by :class:`lino.modlib.fields.LanguageField`.

See http://docs.djangoproject.com/en/dev/ref/settings/#languages

.. setting:: ROOT_URLCONF

This is set to the value of your :class:`Site <lino.core.site.Site>`\
's :attr:`root_urlconf <lino.core.site.Site.root_urlconf>` attribute
(which itself defaults to :mod:`lino.core.urls`).

See `URL dispatcher
<https://docs.djangoproject.com/en/dev/topics/http/urls/>`_ section of
the Django documentation.


.. setting:: INSTALLED_APPS

In a Lino application you usually set your :setting:`INSTALLED_APPS`
by overriding the :meth:`get_installed_apps
<lino.core.site.Site.get_installed_apps>` method.  Alternatively, in
very small projects (such as the projects in :doc:`/tutorials/index`)
you might prefer to specify them as positional arguments when
instantiating the :class:`Site <lino.core.site.Site>`.

.. setting:: MEDIA_ROOT

The root directory of the media files used on this site.  If the
directory specified by :setting:`MEDIA_ROOT` does not exist, then Lino
does not create any cache files. Which means that the web interface
won't work.

Used e.g. by :mod:`lino.utils.media` :mod:`lino.modlib.extjs` and
:mod:`lino.mixins.printable`.

.. setting:: DEBUG

See :blogref:`20100716`
  
.. setting:: SERIALIZATION_MODULES

    See `Django doc
    <https://docs.djangoproject.com/en/1.6/ref/settings/#serialization-modules>`__.

.. setting:: FIXTURE_DIRS

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

