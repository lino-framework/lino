__all__ = []

__docformat__ = 'reStructuredText'


def run(adamoApp):
	#from wxui import wxUI
	from main import WxApp
	#ui = wxUI(sess)
	#print sess.forms._values
	wxapp = WxApp(adamoApp)
	wxapp.MainLoop()
	
