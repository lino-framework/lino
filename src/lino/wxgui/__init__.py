__all__ = []

__docformat__ = 'reStructuredText'


def run(db):
	from wxui import wxUI
	from main import MyApp
	ui = wxUI(db)
	app = MyApp(ui)
	app.MainLoop()
	
