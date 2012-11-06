import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_welfare.demo.settings'
from django.conf import settings
settings.LINO.startup()
from lino import dd
pcsw = dd.resolve_app('pcsw')
User = dd.resolve_model('users.User')
root = User.objects.get(username='root')
print pcsw.UsersWithClients.request(user=root).to_rst()
