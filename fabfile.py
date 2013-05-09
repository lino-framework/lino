from atelier.fablib import *
setup_from_project('lino')  

env.languages = "de fr et nl".split()
env.tolerate_sphinx_warnings = True

env.demo_databases.append('lino.projects.cosi.settings')
env.demo_databases.append('lino.projects.presto.settings')
