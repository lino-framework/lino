"""
Usage: openurl URL

Starts the default browser on your system to display the specified URL.

"""

import sys
import webbrowser

from lino.ui import console 

def main(argv):
    console.copyleft(name="Lino openurl",
                     years='2002-2005',
                     author='Luc Saffre')
    for url in argv:
        # webbrowser.open(url,new=1)
        webbrowser.open_new(url)

if __name__ == "__main__":
    
    main(sys.argv[1:])

