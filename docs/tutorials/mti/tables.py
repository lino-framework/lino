from lino import dd


class Persons(dd.Table):
    model = 'mti.Person'


class Places(dd.Table):
    model = 'mti.Place'


class Restaurants(dd.Table):
    model = 'mti.Restaurant'


def setup_main_menu(site, ui, profile, m):
    m = m.add_menu("contacts", "Contacts")
    m.add_action(Persons)
    m.add_action(Places)
    m.add_action(Restaurants)
