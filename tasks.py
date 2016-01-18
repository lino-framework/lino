from atelier.tasks import *
# env = Atelier(globals(), "atelier")
env.setup_from_tasks(globals(), "lino")
env.revision_control_system = 'git'
