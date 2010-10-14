#!/usr/bin/env python
from django.core.management import execute_manager
import settings # Assumed to be in the same directory.
from django.core.management import setup_environ
setup_environ(settings)

if __name__ == "__main__":
    execute_manager(settings)
