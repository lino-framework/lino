raise "no longer used"
# this script is imported by lino.spec who will check that both
# versions correspond

version = None
notes = None

def release(ver,date,_notes):
	pass
	global version
	global notes
	assert ver > version, "Version number cannot go back."
	version = ver
	notes = _notes

release('0.5.2','20030415',"""
pds2pdf being actively used by a first customer who generates a Wochenplan with TIM.
""")

release('0.5.3','20030417',"""
first bugs in pds2pdf solved...
""")


release('0.6.0','20030603', """pds2pdf can now print barcodes.
HTML rendering works (although very early stage).
Internal redesign. The previous
internals were too close to the reportlab data model and had problems
to render HTML.
""")

release('0.6.1','20031029', """Release is for a customer who starts to
use TIM tools.""")

