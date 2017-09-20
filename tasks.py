# from atelier.invlib import add_demo_project
from atelier.invlib.ns import ns

ns.setup_from_tasks(
    globals(), "lino",
    languages="en de fr et nl pt-br es".split(),
    # tolerate_sphinx_warnings=True,
    blogref_url = 'http://luc.lino-framework.org',
    revision_control_system='git',
    locale_dir='lino/modlib/lino_startup/locale',
    doc_trees=[])
