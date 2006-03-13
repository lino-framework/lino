from lino.apps.ledger import demo
from lino.apps.ledger.ledger import Ledger

dbsess=demo.startup() # filename="ledger.db")
Ledger(dbsess).main()


