#----------------------------------------------------------------------
# startup.py
# This file is part of the Lino project
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

import sys, os

from lino import copyleft
from lino.ui import console

import datetime

editorCommand = r's:\gnuserv\gnuclientw -F %s'
#actions = ('lino','debian','windows', 'priv')
actions = ('lino','work', 'priv')
blogDir = r't:\data\luc\blogs'
filenames = []
today = datetime.date.today()
year,week,weekday = today.isocalendar()

chunk = "%d-%02d" % (year,week)
title = "Week %d/%d (started on %s)" % (year,week,str(today))

def main(argv):

    parser = console.getOptionParser(
        usage="usage: %prog [options]",
        )
    
    (options, args) = parser.parse_args(argv)

    for a in actions:
        fn = os.path.join(blogDir,a,a+"-"+chunk+".txt")
        if not os.path.exists(fn):
            f = file(fn,'w')
            f.write("="*len(title)+"\n")
            f.write(title+"\n")
            f.write("="*len(title)+"\n")
            f.close()
        filenames.append(fn)

    os.system(editorCommand % " ".join(filenames))


if __name__ == '__main__':
    print copyleft(name="Lino/startup", year='2004')
    main(sys.argv[1:])
    
