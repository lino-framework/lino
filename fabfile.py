from atelier.fablib import *
setup_from_project('lino')

env.languages = "en de fr et nl pt-br es".split()
env.tolerate_sphinx_warnings = True

add_demo_database('lino.projects.docs.settings.demo')
add_demo_database('lino.projects.min1.settings.demo')
add_demo_database('lino.projects.min2.settings.demo')
add_demo_database('lino.projects.belref.settings.demo')
add_demo_database('lino.projects.polly.settings.demo')
add_demo_database('lino.projects.presto.settings.demo')
add_demo_database('lino.projects.i18n.settings')
add_demo_database('lino.projects.events.settings')

env.revision_control_system = 'git'

env.apidoc_exclude_pathnames = ['lino/projects']
