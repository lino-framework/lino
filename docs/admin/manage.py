#!/usr/bin/env python
import os
import sys
if __name__ == "__main__":
    prj = os.path.split(os.path.dirname(os.path.abspath(__file__)))[-1]
    os.environ['DJANGO_SETTINGS_MODULE'] = prj + '.settings'
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


