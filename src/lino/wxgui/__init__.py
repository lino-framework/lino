__all__ = []

__docformat__ = 'reStructuredText'


def run(sess):
	from main import WxApp
	wxapp = WxApp(sess)
	wxapp.MainLoop()
	
