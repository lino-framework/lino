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
from django.core.management.color import no_style
from django.db import models, connection, transaction, models
from django.core.management.sql import sql_flush, emit_post_sync_signal
from django.core.management import call_command


from lino.console import syscon
        
def main():
    call_command('syncdb')
    if syscon.confirm("Gonna flush database %s. Are you sure?" 
        % settings.DATABASE_NAME):
        call_command('flush',interactive=False)
    elif not syscon.confirm("Continue filling the existing database?"):
        return
    call_command('loaddata','demo')
    User.objects.create_superuser('root','root@example.com','root')
    User.objects.create_user('user','user@example.com','user')
        

if __name__ == "__main__":
    main()
