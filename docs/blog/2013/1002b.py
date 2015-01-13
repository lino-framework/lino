"""
How to add users to your Lino database::

  $ python manage.py run /path/to/lino/blog/2013/1002b.py

"""


from django.conf import settings
from lino.modlib.users.choicelists import UserProfiles

User = settings.SITE.user_model
u = User(username="rolf", profile=UserProfiles.admin)
u.save()
u.set_password('1234')
                    
                    
