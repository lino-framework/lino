from djangosite.utils.fablib import *
setup_from_project()  

env.django_doctests.append('tutorials.fixtures1.settings')
env.django_doctests.append('tutorials.auto_create.settings')
env.django_doctests.append('tutorials.human.settings')

env.django_admin_tests += [
      "lino.projects.cosi.settings",
      "lino.projects.events.settings",
      "lino.test_apps.nomti.settings",
      "lino.test_apps.20100212.settings",
      "lino.test_apps.quantityfield.settings",
      #~ "lino.test_apps.human.settings",
      "lino.projects.cosi.settings",
      "lino.projects.presto.settings", 
      "lino.projects.babel_tutorial.settings",
      "lino.projects.polls_tutorial.settings",
      "lino.projects.belref.settings",
      "lino.projects.events.settings",
      "lino.projects.homeworkschool.settings",
      "lino.projects.min1.settings",
      "lino.projects.min2.settings",
]


