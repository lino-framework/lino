from lino.modlib.voc import models
from django.contrib import admin, databrowse

admin.site.register(models.Unit)
admin.site.register(models.Entry)

databrowse.site.register(models.Unit)
databrowse.site.register(models.Entry)
