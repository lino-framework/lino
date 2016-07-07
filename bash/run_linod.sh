#!/bin/bash
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
#
# Invokes ``python manage.py linod`` with the proper command-line
# arguments for this project.
#
# This is not meant to be used as-is but as template for a script to
# be adapted to your system.  This script should be in a subdirectory
# `linod` of your project directory.
#

set -e  # exit on error

PROJECT=myproject
PROJECT_DIR="/path/to/$PROJECT"
PID="$PROJECT_DIR/linod/pid"
STDERR="$PROJECT_DIR/linod/error.log"
STDOUT="$PROJECT_DIR/linod/stdout.log"
DJANGO_SETTINGS_MODULE=$PROJECT.settings
. $PROJECT_DIR/env/bin/activate
python $PROJECT_DIR/manage.py linod \
  --traceback \
  --pidfile $PID \
  --stdout $STDOUT \
  --stderr $STDERR

