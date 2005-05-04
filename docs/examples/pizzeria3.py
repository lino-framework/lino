from lino.apps.pizzeria.services import \
     makeSchema, populate, Products, OrderLines

schema = makeSchema()
sess = schema.quickStartup()
populate(sess)

p=sess.query(Products).peek(1)

title="Who bought %s (product# %s)?" % (p.name, p.id)

qry = sess.query(OrderLines,"ordr.date ordr.customer",
                 product=p)
qry.report(columnWidths="10 13",
           label=title)

