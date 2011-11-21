from jobs1 import work

from lino.ui import console
from lino.forms import gui

if __name__ == "__main__":
    print "This example currently broken."
    if False:
        gui.parse_args()
        frm = gui.form("Demonstrating Job")
        frm.addButton("with").setHandler(work,True)
        frm.addButton("without").setHandler(work,False)
        frm.show()
    
