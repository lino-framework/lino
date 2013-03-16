#!/usr/bin/env python
"""
To call it on the default settings of this doctree::

  python manage.py test 
  
To call it for some other settings file defined in this doctree::

  python manage.py --settings=tutorials.de_BE.settings test 
  
"""

import sys

has_settings = False

for a in sys.argv:
    if a.startswith('--settings'):
        has_settings = True
    
if not has_settings:
  
    import conf

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
  
