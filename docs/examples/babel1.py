from lino.apps.ledger import demo, tables

sess=demo.startup(langs="en fr")
qry=sess.query(tables.Currency,"id name")
# show in default language:
sess.showQuery(qry)
print
# switch to FR and show again:
sess.setBabelLangs("fr")
sess.showQuery(qry)


