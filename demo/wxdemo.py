"""
starts a GUI application with an adamo database.
Just a proof of concept, far from being usable.
"""

if __name__ == "__main__":
	
	from lino.adamo import center 
	center.start(verbose=True)

	from lino.schemas.sprl import demo
	sess = demo.beginSession()
	
	from lino.wxgui.main import WxApp
	app = WxApp(sess)
	app.MainLoop()
