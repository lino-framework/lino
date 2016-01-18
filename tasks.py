from atelier.tasks import *
env.setup_from_tasks(globals(), "lino")

env.locale_dir = 'lino/modlib/lino_startup/locale'
env.languages = "en de fr et nl pt-br es".split()
# env.tolerate_sphinx_warnings = True

env.add_demo_project('lino.projects.docs.settings.demo')
env.add_demo_project('lino.projects.min1.settings.demo')
env.add_demo_project('lino.projects.min2.settings.demo')
env.add_demo_project('lino.projects.belref.settings.demo')
env.add_demo_project('lino.projects.polly.settings.demo')
env.add_demo_project('lino.projects.i18n.settings')
env.add_demo_project('lino.projects.events.settings')
env.add_demo_project('lino.projects.cms.settings')

env.revision_control_system = 'git'

env.cleanable_files = ['docs/api/lino.*']
