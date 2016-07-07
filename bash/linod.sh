#!/bin/bash
#
# Lino daemon startup script
#
# Author: Luc Saffre
# Create adapted copy of this in your /etc/init.d
#

PROJECT="myproject"
PROJECT_DIR="/path/to/$PROJECT"
EXEC="$PROJECT_DIR/linod/run_linod.sh"
PID="$PROJECT_DIR/linod/pid"

set -e

start() {
    if start-stop-daemon --start --verbose --pidfile $PID --exec $EXEC; then
        echo "Done."
        return 0
    else
        echo "Failed."
        return 1
    fi
}

stop() {
    if start-stop-daemon --stop --verbose --pidfile $PID; then
        echo "Done."
        return 0
    else
        echo "Failed."
        return 1
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        [ "$?" == 0 ] && start
        ;;
    *)
        echo "usage: `basename $0` (start|stop|restart|help)"
        exit 1
        ;;
esac
exit 0
