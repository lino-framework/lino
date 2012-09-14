"""
Run using::

  python manage.py run 0914.py
  
"""

if False: # TIMTOWTDI: the following is equivalent  
    from django.conf import settings
    settings.LINO.startup()
    root = settings.LINO.user_model.objects.get(username='root')
    ar = settings.LINO.modules.pcsw.UsersWithClients.request(user=root)
    print ar.to_rst()
else:
    from lino import dd
    pcsw = dd.resolve_app('pcsw')
    User = dd.resolve_model('users.User')
    root = User.objects.get(username='root')
    print pcsw.UsersWithClients.request(user=root).to_rst()
