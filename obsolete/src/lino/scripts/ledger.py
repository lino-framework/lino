from lino.apps.ledger.ledger_demo import startup
from lino.apps.ledger.ledger_forms import Ledger

dbsess=startup() # filename="ledger.db")
Ledger(dbsess).main()


