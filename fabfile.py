from atelier.fablib import *
setup_from_fabfile(globals(), 'lino')

env.locale_dir = 'lino/modlib/lino/locale'
env.languages = "en de fr et nl pt-br es".split()
env.tolerate_sphinx_warnings = True

add_demo_project('lino.projects.docs.settings.demo')
add_demo_project('lino.projects.min1.settings.demo')
add_demo_project('lino.projects.min2.settings.demo')
add_demo_project('lino.projects.belref.settings.demo')
add_demo_project('lino.projects.polly.settings.demo')
add_demo_project('lino.projects.presto.settings.demo')
add_demo_project('lino.projects.i18n.settings')
add_demo_project('lino.projects.events.settings')

env.revision_control_system = 'git'

env.cleanable_files = ['docs/api/lino.*']
