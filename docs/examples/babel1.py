from lino.apps.ledger import demo, tables

sess=demo.startup(langs="en fr")

qry=sess.query(tables.Currency)

ccy=qry.peek("EEK")

#sess.setBabelLangs("en")
print "Your currency: %s (%s)" % (ccy.name,ccy.id)
sess.showQuery(qry)

print
sess.setBabelLangs("fr")
print "Votre monnaie: %s (%s)" % (ccy.name,ccy.id)
sess.showQuery(qry)


