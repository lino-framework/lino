import os
import sys    
def prettyfy(fn):
    a,b = os.path.split(fn)
    outfile = os.path.join(a,'pretty-'+b)
    file(outfile,"w").write(file(fn).read().replace('><','>\n<'))
prettyfy(sys.argv[1])