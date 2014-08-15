from atelier.fablib import *
setup_from_project('lino')

env.languages = "en de fr et nl pt-br es".split()
env.tolerate_sphinx_warnings = True

env.demo_databases.append('lino.projects.docs.settings')
env.demo_databases.append('lino.projects.belref.settings.demo')
env.demo_databases.append('lino.projects.polly.settings.demo')
# env.demo_databases.append('lino.projects.cosi.settings.demo')
env.demo_databases.append('lino.projects.presto.settings.demo')
env.demo_databases.append('lino.projects.min1.settings')
env.demo_databases.append('lino.projects.i18n.settings')
env.demo_databases.append('lino.projects.events.settings')

env.use_mercurial = False
