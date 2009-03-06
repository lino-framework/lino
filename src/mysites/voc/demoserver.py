"""
pkkserver.py does almost the same as would do 
``python manage.py testserver pkk``, with one difference:
the above command won't execute any custom before_save() and after_save() when commiting the fixtures to the database.

But pkk.yaml is a hand-written fixture, and we need to run the
Unit.before_save() in order to set the Unit.seq fields and to 
fill the Entry table with data found in Unit.vocabulary.


"""
from django.core.management import setup_environ, call_command
import settings 
setup_environ(settings)

from django.db import connection
from lino.django.voc.models import Unit


verbosity = 2
addrport = "8000"

# Create a test database.
db_name = connection.creation.create_test_db(verbosity=verbosity)

# Import the fixture data into the test database.
call_command('loaddata', 'demo', verbosity=verbosity)

#for u in Unit.objects.all():
#    u.save()


# Run the development server. Turn off auto-reloading because it causes
# a strange error -- it causes this handle() method to be called
# multiple times.
shutdown_message = '\nServer stopped.\nNote that the test database, %r, has not been deleted. You can explore it on your own.' % db_name
call_command('runserver', addrport=addrport, shutdown_message=shutdown_message, use_reloader=False)
