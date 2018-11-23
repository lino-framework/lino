# Copyright 2016-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Lino's :mod:`lino.modlib.restful` plugin is an adapter to the
django-restful framework.

Usage:

- Add ``'lino.modlib.restful'`` to your :meth:`get_installed_apps`.

- Install `djangorestframework` manually in case it is not installed
  automatically::

      $ pip install djangorestframework

- Set your :attr:`root_urlconf` to 'mysite.urls'

- Write your `mysite/urls.py` using lino_noi.projects.team.urls as
  example.

.. autosummary::
   :toctree:

    urls

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :doc:`/dev/plugins`."
    verbose_name = _("Restful")

    needs_plugins = ['rest_framework']

    # def on_init(self):
    #     super(Plugin, self).on_init()
    #     self.site.set_user_model('users.User')

    def on_init(self):
        # if self.site.use_websockets:
        #     self.needs_plugins.append('channels')

        sd = self.site.django_settings
        # the dict which will be
        # used to create settings
        sd.update(REST_FRAMEWORK={
            'DEFAULT_PERMISSION_CLASSES': [
                # 'rest_framework.permissions.AllowAny'
                'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
            # 'EXCEPTION_HANDLER': 'lino_noi.lib.rest.utils.exception_handler',
            'UNAUTHENTICATED_USER': 'lino.core.auth.utils.AnonymousUser'
        })
            
            
