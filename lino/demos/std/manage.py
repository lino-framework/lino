#!/usr/bin/env python
from django.core.management import execute_manager
import settings # Assumed to be in the same directory.
from django.core.management import setup_environ
setup_environ(settings)

#~ from lino import diag
#~ diag.welcome()

if __name__ == "__main__":
    execute_manager(settings)
