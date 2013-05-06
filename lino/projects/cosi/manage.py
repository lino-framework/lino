#!/usr/bin/env python
if __name__ == "__main__":

    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.cosi.settings'

    import settings

    from django.core.management import execute_manager

    execute_manager(settings)







