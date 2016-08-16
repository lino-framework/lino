from atelier.tasks import ns
ns.setup_from_tasks(
    globals(), "lino_noi",
    languages="en de fr et".split(),
    tolerate_sphinx_warnings=False,
    blogref_url='http://luc.lino-framework.org',
    revision_control_system='git',
    locale_dir='lino_noi/lib/noi/locale',
    cleanable_files=['docs/api/lino_noi.*'],
    demo_projects=[
        'lino_noi.projects.team.settings.demo',
        'lino_noi.projects.care.settings.demo'])

# The following demo databases use the database file of team, so there is no
# need initialize them:
#    - lino_noi.projects.public.settings.demo
#    - lino_noi.projects.bs3.settings.demo
