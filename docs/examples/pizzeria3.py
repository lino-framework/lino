from lino.apps.pizzeria.pizzeria import Products, OrderLines
from lino.apps.pizzeria.services import \
     ServicePizzeria, populate

app = ServicePizzeria()
sess = app.quickStartup()
populate(sess)

p=sess.query(Products).peek(1)

title="Who bought %s (product# %s)?" % (p.name, p.id)

qry = sess.query(OrderLines,"ordr.date ordr.customer",
                 product=p)
sess.showQuery(qry,columnWidths="10 13",label=title)

