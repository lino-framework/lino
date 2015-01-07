#!/usr/bin/env python
import os
import sys

# we add ".." to PYTHONPATH because this is a single-dir Django project
sys.path.insert(0,  os.path.abspath('..'))

if __name__ == "__main__":

    import os
    from django.core.management import execute_from_command_line

    os.environ["DJANGO_SETTINGS_MODULE"] = "watch_tutorial.settings"
    execute_from_command_line(sys.argv)
