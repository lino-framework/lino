from lino.timtools import console_targets
from lino.console.syscon import confirm
from lino.misc.tsttools import trycmd

if confirm("Are you sure?"):
    for ct in console_targets():
        cmd="lino %s --help > %s.help.txt" % (ct,ct)
        print cmd
        trycmd(cmd)
    
