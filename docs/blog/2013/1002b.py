"""
How to add users to your Lino database::

  $ python manage.py run /path/to/lino/blog/2013/1002b.py

"""


from lino import dd
from django.conf import settings

User = settings.SITE.user_model
u = User(username="rolf",profile=dd.UserProfiles.admin)
u.save()
u.set_password('1234')
                    
                    
