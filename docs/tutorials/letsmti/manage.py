#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":

    # this is a single-dir Django project. we add ".." to PYTHONPATH
    # and prefix '.settings' with name of this directory.
    sys.path.insert(0,  os.path.abspath('..'))
    name = os.path.split(os.path.abspath(os.path.dirname(__file__)))[1]
    os.environ["DJANGO_SETTINGS_MODULE"] = name + ".settings"

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
