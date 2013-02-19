from django.db.models import loading
if len(loading.cache.postponed) > 0:
    raise Exception("Waiting for postponed apps (%s) to import" % 
        loading.cache.postponed)
from django.conf import settings
settings.LINO.startup()
#~ settings.LINO.analyze_models()
#~ print 20130219, __file__, settings.INSTALLED_APPS
