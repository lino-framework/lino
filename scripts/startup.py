#coding: latin1

import sys, os

from lino import copyleft
from lino.misc import console

from forum.normalDate import ND
import datetime

editorCommand = r's:\gnuserv\gnuclientw -F %s'
actions = ('lino','debian','windows', 'priv')
blogDir = r't:\data\luc\blogs'

def main(argv):

    parser = console.getOptionParser(
        usage="usage: %prog [options] [ACTIONS]",
        description="""\
where ACTIONS is an optional list of actions to do.
""" )
    
    (options, args) = parser.parse_args(argv)

    if len(args) == 0:
        args = actions
        
    today = datetime.date.today()
    filenames = []
    for a in args:
        fn = os.path.join(blogDir,a,a+"-"+str(today)+".txt")
        if not os.path.exists(fn):
            f = file(fn,'w')
            f.write(str(today)+"\n")
            f.write("==========\n")
            f.close()
        filenames.append(fn)

    os.system(editorCommand % " ".join(filenames))


if __name__ == '__main__':
    print copyleft(name="Lino/startup", year='2004')
    main(sys.argv[1:])
    
