"""
starts a GUI application with an adamo database.
Just a proof of concept, far from being usable.
"""

import sys

from lino.misc import console
from lino.schemas.sprl import demo
from lino import wxgui 

if __name__ == "__main__":
    console.parse_args(sys.argv)
    sess = demo.beginSession()
    wxgui.run(sess)
    
