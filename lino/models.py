#~ from django.db.models import loading
#~ if len(loading.cache.postponed) > 0:
    #~ raise ImportError("Waiting for postponed apps (%s) to import" % 
        #~ loading.cache.postponed)
from django.conf import settings
#~ print settings.INSTALLED_APPS
settings.LINO.startup()
#~ settings.LINO.analyze_models()
