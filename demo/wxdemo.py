"""
starts a GUI application with an adamo database.
Just a proof of concept, far from being usable.
"""

if __name__ == "__main__":
	
	from lino import wxgui
	from lino.schemas.sprl import demo

	sess = demo.beginSession(verbose=True)
	wxgui.run(sess)

