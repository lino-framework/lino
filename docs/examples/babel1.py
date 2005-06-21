from lino.schemas.sprl import demo, Currencies

sess=demo.startup(langs="en fr")

qry=sess.query(Currencies)

ccy=qry.peek("EEK")

#sess.setBabelLangs("en")
print "Your currency: %s (%s)" % (ccy.name,ccy.id)
sess.showQuery(qry)

print
sess.setBabelLangs("fr")
print "Votre monnaie: %s (%s)" % (ccy.name,ccy.id)
sess.showQuery(qry)


