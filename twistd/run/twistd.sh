#!/bin/sh
# run Luc's Twisted Web Server

case "$1" in
'start')
        #cd /home/luc/twistd/run
        #twistd -f web.tap
		  cd /mnt/lino/twistd/run
		  twistd -y nevow_webserver.py
        ;;
'stop')
        #cd /home/luc/twistd/run
		  cd /mnt/lino/twistd/run
        kill `cat twistd.pid`
        ;;
*)
        echo "Usage: $0 { start | stop }"
        ;;
esac
exit 0