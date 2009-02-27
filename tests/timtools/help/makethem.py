from lino.timtools import CONSOLE_TARGETS
from lino.console.syscon import confirm
from lino.misc.tsttools import trycmd

if confirm("Are you sure?"):
    for ct in CONSOLE_TARGETS:
        cmd="lino %s --help > %s.help.txt" % (ct,ct)
        print cmd
        trycmd(cmd)
    
