__all__ = []

__docformat__ = 'reStructuredText'


def run(sess):
	#from wxui import wxUI
	from main import MyApp
	#ui = wxUI(sess)
	#print sess.forms._values
	app = MyApp(sess)
	app.MainLoop()
	
