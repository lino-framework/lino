# The is file ui.py of the Lino polls tutorial
from lino.api import dd


class Polls(dd.Table):
    model = 'polls.Poll'
    sort_order = ['pub_date']

    detail_layout = """
    id question
    hidden pub_date
    ChoicesByPoll
    """

    insert_layout = """
    question
    hidden
    """


class Choices(dd.Table):
    model = 'polls.Choice'


class ChoicesByPoll(Choices):
    master_key = 'poll'

