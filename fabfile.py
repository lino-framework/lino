from atelier.fablib import *
setup_from_fabfile(globals(), 'lino')

env.languages = "en de fr et nl pt-br es".split()
# env.tolerate_sphinx_warnings = True

add_demo_project('lino/projects/docs')
add_demo_project('lino/projects/min1')
add_demo_project('lino/projects/min2')
add_demo_project('lino/projects/belref')
add_demo_project('lino/projects/polly')
add_demo_project('lino/projects/presto')
add_demo_project('lino/projects/i18n')
add_demo_project('lino/projects/events')

env.revision_control_system = 'git'

# env.apidoc_exclude_pathnames = ['lino/projects']
