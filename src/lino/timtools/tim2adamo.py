from lino.adamo.database import Database
from lino.adamo.table import Table
from lino.agui.ui import UI
from lino.adamo.datatypes import *

class TimDatabase(Database):
	
	def initDatabase(self):
		# not yet usable
		conn = self.getConnection()
		csr = conn.sql_exec("""\
		SELECT * FROM sqlite_master
			WHERE type='table'
		UNION ALL
		SELECT * FROM sqlite_temp_master
		WHERE type='table' 
		ORDER BY name;
		""")
		for row in csr.fetchall():
			self.addTable(row[1], TimRow)
		
	def initUI(self,ui):
		ui.clearMenus()

		mb = ui.addMenuBar("user","&User Menu")
		m = mb.addMenu("&Master data")
		m.addItem("&Partners", ui.showReport,"PAR")
		m.addItem("&Pages", ui.showReport,"MSX")
		m.addItem("&News", ui.showReport,"NEW")

		m = self.addSystemMenu(ui,mb)
		m.addItem("Ad&min menu",ui.setMainMenu,'admin')
		
		
		mb = ui.addMenuBar("admin","&Admin Menu")
		m = mb.addMenu("&Tables")
		for (name,table) in self.tables.items():
			m.addItem("&"+table.getLabel(),
						 ui.showReport,
						 name)
		m = mb.addMenu("T&ests")
		m.addItem("&Decide",ui.test_decide)
		m = self.addSystemMenu(ui,mb)
		m.addItem("&User menu",ui.setMainMenu,'user')
		
	def addSystemMenu(self,ui,mb):
		m = mb.addMenu("&System")
		m.addItem("&Exit",ui.exit)
		m.addItem("&About",ui.showAbout)
		#m.addItem("~Main menu",self.getMainMenu)
		return m

## class TimTable(Table):
## 	def init(self):
## 		pass

class TimRow:
 	""
 	def init(self,table):
		conn = table.getConnection()
		sql = "SELECT * FROM %s;" % table.getName()
		csr = conn.sql_exec(sql)
		pk = ''
		for desc in csr.description:
			# print desc[0]
			table.addField(desc[0],STRING)
			
		sql = "SELECT sql FROM sqlite_master where tbl_name='%s' AND type='table';" \
				% table.getName()
		csr = conn.sql_exec(sql)
		if csr.rowcount != 1:
			raise '"%s" returned %d' % (sql,csr.rowcount)
		row = csr.fetchone()
		a = row[0].split('PRIMARY KEY')
		if len(a) == 2:
			print a[1]
		table.setPrimaryKey(tuple())
	

class TimUI(UI):
	pass

def getDB(filename):
	"filename is the name of an sqlite database file"
	from lino.adamo.dbds.sqlite_dbd import Connection
	conn = Connection(filename)
	db = TimDatabase(conn,label="TIM database")
	db.startup()
	return db
	
