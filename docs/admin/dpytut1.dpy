from lino.tools import resolve_model
User = resolve_model('users.User')

def objects():

    yield User(username='pbommel',
      first_name='Piet',last_name='Bommel',
      email='piet@bommel.be',
      is_staff=True)

    yield User(username='jdupond',
      first_name='Jean',last_name='Dupond',
      email='jean@bommel.be',
      is_staff=True)
      