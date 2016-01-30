from atelier.invlib import add_demo_project
from atelier.tasks import ns, setup_from_tasks

ctx = setup_from_tasks(globals(), "lino")

locale_dir = 'lino/modlib/lino_startup/locale'
languages = "en de fr et nl pt-br es".split()
# env.tolerate_sphinx_warnings = True

add_demo_project(ctx, 'lino.projects.docs.settings.demo')
add_demo_project(ctx, 'lino.projects.min1.settings.demo')
add_demo_project(ctx, 'lino.projects.min2.settings.demo')
add_demo_project(ctx, 'lino.projects.belref.settings.demo')
add_demo_project(ctx, 'lino.projects.polly.settings.demo')
add_demo_project(ctx, 'lino.projects.i18n.settings')
add_demo_project(ctx, 'lino.projects.events.settings')
add_demo_project(ctx, 'lino.projects.cms.settings')

ns.configure({'revision_control_system': 'git',
              'cleanable_files': ['docs/api/lino.*']})
