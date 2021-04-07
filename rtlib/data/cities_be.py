# Copyright 2003-2010 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import csv
import os
import codecs

if __name__ == "__main__":
    print "zip_code name"
    f = codecs.open('belgzip.csv','r',"cp850")
    r = csv.reader(f)
    r.next()
    for (name,zip) in r:
        print zip, " ", name
    f.close()
