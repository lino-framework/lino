from django.conf import settings
settings.SITE.startup()
globals().update(settings.SITE.modules)
