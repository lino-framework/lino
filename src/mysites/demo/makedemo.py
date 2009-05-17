## Copyright 2008-2009 Luc Saffre 

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import os
import settings
from django.core.management import setup_environ
setup_environ(settings)
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.management.color import no_style
from django.db import models, connection, transaction
from django.db.models import loading
from django.core.management.sql import sql_flush, emit_post_sync_signal
from django.core.management import call_command


from lino.console import syscon

from lino.django.utils.sites import site as lino_site

def db_apps():
    for app_name in settings.INSTALLED_APPS:
        app_label = app_name.split('.')[-1]
        if loading.get_app(app_label,emptyOK=True):
            yield app_label

        
def main():
    for name,url,version in lino_site.thanks_to():
        print name,version, "<%s>" % url
        
    app_labels = [n for n in db_apps()]

    #appnames = [m.__name__ for m in models.get_apps()]
    print "makedemo.py", app_labels
    options = dict(interactive=False)
    if not syscon.confirm("Gonna reset database %s. Are you sure?" 
        % settings.DATABASE_NAME):
        return
    call_command('reset',*app_labels,**options)
    #call_command('reset','songs','auth',interactive=False)
    call_command('syncdb',**options)
    #call_command('flush',interactive=False)
    call_command('loaddata','demo')
    User.objects.create_superuser('root','luc.saffre@gmx.net','1234')
    User.objects.create_user('user','luc.saffre@gmx.net','1234')
    Site(id=1,domain="http://igen.saffre-rumma.ee",name="lino.django.utils demo").save()
        

if __name__ == "__main__":
    main()
