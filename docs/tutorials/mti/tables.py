from lino.api import dd


class Persons(dd.Table):
    model = 'mti.Person'
    column_names = 'name *'
    detail_layout = """
    id name
    VisitsByPerson
    MealsByPerson
    """


class Places(dd.Table):
    model = 'mti.Place'
    detail_layout = """
    id name mti_navigator
    owners
    VisitsByPlace
    """


class Restaurants(dd.Table):
    model = 'mti.Restaurant'
    detail_layout = """
    id name serves_hot_dogs mti_navigator
    owners cooks
    VisitsByPlace
    MealsByRestaurant
    """


class VisitsByPlace(dd.Table):
    model = 'mti.Visit'
    master_key = 'place'
    column_names = 'person purpose'


class VisitsByPerson(dd.Table):
    model = 'mti.Visit'
    master_key = 'person'
    column_names = 'place purpose'


class MealsByRestaurant(dd.Table):
    model = 'mti.Meal'
    master_key = 'restaurant'
    column_names = 'person what'


class MealsByPerson(dd.Table):
    model = 'mti.Meal'
    master_key = 'person'
    column_names = 'restaurant what'


