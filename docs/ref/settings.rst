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

.. setting:: ROOT_URL

Lino sets this automatically to :mod:`lino.core.urls`.
You might specify your own :setting:`ROOT_URLS` on a Lino site.

See http://docs.djangoproject.com/en/dev/ref/settings/#root-url

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

You'll set this to :mod:`lino.ui.extjs3.urls` and don't need to write 
any local html nor css.

We are also working on alternative user interfaces 
:mod:`lino.ui.extjs4.urls` and
:mod:`lino.ui.qx.urls`.


.. setting:: INSTALLED_APPS

Lino sets this automatically from the values returned by the
:setting:`get_installed_apps` method.  In order to modify your
:setting:`INSTALLED_APPS`, you usually override this method.  The only
exception is in very small code snippets where you can specify them as
positional arguments when instantiating the :class:`Site
<lino.core.site.Site>`.

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
<https://docs.djangoproject.com/en/1.6/ref/settings/#serialization-modules>`_.

.. setting:: FIXTURE_DIRS

