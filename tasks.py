# from atelier.invlib import add_demo_project
from atelier.tasks import ns

ns.setup_from_tasks(globals(), "lino")

ns.configure(dict(languages="en de fr et nl pt-br es".split()))

