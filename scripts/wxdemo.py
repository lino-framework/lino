"""
starts a GUI application with an adamo database.
Just a proof of concept, far from being usable.
"""

if __name__ == "__main__":
	
	from lino import wxgui
	from lino.schemas.sprl import demo

	if True:

		db = demo.startup(verbose=True)
		wxgui.run(db)

	else:
	
		from lino.sprl.database import SprlDatabase
		from lino.adamo.dbds.sqlite_dbd import Connection

		conn = Connection("demo.db")

		db = SprlDatabase(conn,"My demo database")
		db.startup(verbose=True)
		db.createTables()
		demo.populateDemo(db)

		wxgui.run(db)
