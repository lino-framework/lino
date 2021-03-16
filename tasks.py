from atelier.invlib import setup_from_tasks

ns = setup_from_tasks(
    globals(), "lino",
    # tolerate_sphinx_warnings=True,
    languages="en de fr et nl pt-br es zh-hant bn".split(),
    doc_trees=[],
    blogref_url='https://luc.lino-framework.org',
    revision_control_system='git',
    locale_dir='lino/locale')
