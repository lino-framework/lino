# -*- coding: UTF-8 -*-
# Copyright 2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Adds authentication via third-party providers using
`Python Social Auth <https://github.com/python-social-auth>`__

Sites which use this plugins must also install::

  $ pip install social-auth-app-django

And then define a backend and credentials in your local
:xfile:`settings.py` file, e.g.::

  SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = \
    '1234567890-a1b2c3d4e5.apps.googleusercontent.com'
  SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'SH6da...'
  AUTHENTICATION_BACKENDS.insert(
    0, 'social_core.backends.google.GooglePlusAuth')

"""

from __future__ import unicode_literals
from __future__ import print_function

from lino.api import ad, _


class Plugin(ad.Plugin):
    needs_plugins = ['lino.modlib.users', 'social_django']

    ui_label = _("Social Authentication")

    def get_used_libs(self, html=None):
        try:
            import social_django
            version = social_django.__version__
        except ImportError:
            version = self.site.not_found_msg
        name = "social-django"

        yield (name, version, "https://github.com/python-social-auth")

    def on_init(self):
        raise Exception("No longer used. See Site.social_auth_backends.")

        # self.needs_plugins.append()
        ds = self.site.django_settings
        if False:
            ds['SOCIAL_AUTH_PIPELINE'] = (
                'social_core.pipeline.social_auth.social_details',
                'social_core.pipeline.social_auth.social_uid',
                'social_core.pipeline.social_auth.social_user',
                'social_core.pipeline.user.get_username',
                'social_core.pipeline.user.create_user',
                'social_core.pipeline.social_auth.associate_user',
                'social_core.pipeline.social_auth.load_extra_data',
                'social_core.pipeline.user.user_details',
                'social_core.pipeline.social_auth.associate_by_email')        

    def get_patterns(self):
        from django.conf.urls import url, include  # patterns
        urlpatterns = [
            url('', include('social_django.urls', namespace='social'))
            ]
        return urlpatterns
        
    # def get_js_includes(self, settings, language):
    #     yield settings.SITE.build_static_url(
    #         "social_auth", "google_plus.js")

    def get_head_lines(self, site, request):
        from django.conf import settings
        # yield request.render_jinja()
        context = dict(settings=settings)
        yield site.plugins.jinja.render_from_request(
            request, 'social_auth/google_plus.html', **context)
