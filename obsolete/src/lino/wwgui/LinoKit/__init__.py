#coding:latin1
#----------------------------------------------------------------------
# $Id: __init__.py,v 1.1 2004/03/04 12:23:21 lsaffre Exp $
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

from lino.wwgui.webware_ui import UI
#from lino.agui.ui import UI
from lino.schemas.sprl.sprl import Schema
from lino.adamo.dbds.sqlite_dbd import Connection


def InstallInWebKit(appServer):
	
	ui = UI(verbose=True)

 	schema = Schema()
 	schema.startup(ui)
	
 	ui.addDatabase(name="luc",
						conn=Connection("luc.db"),
						schema=schema,
						label="Lucs Heimatseite")
						

	
	app = appServer.application()
	app.lino_ui = ui
	app.addShutDownHandler(ui.shutdown)

	 	

 
