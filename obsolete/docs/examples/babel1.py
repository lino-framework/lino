from lino.apps.ledger.ledger_demo import startup
from lino.apps.ledger.ledger_tables import Currency

sess=startup(langs="en fr")
qry=sess.query(Currency,"id name")
# show in default language:
qry.show()
print
# switch to FR and show again:
sess.setBabelLangs("fr")
qry.show()
sess.shutdown()

