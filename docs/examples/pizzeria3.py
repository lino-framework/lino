from lino.apps.pizzeria.pizzeria import Product, OrderLine
from lino.apps.pizzeria.services import \
     ServicePizzeria, populate

app = ServicePizzeria()
sess = app.quickStartup()
populate(sess)

p=sess.query(Product).peek(1)

qry = sess.query(OrderLine,"order.date order.customer",
                 product=p)
sess.showQuery(
    qry,columnWidths="10 13",
    title="Who bought %s (product# %s)?" % (p.name, p.id))

print
print qry.getSqlSelect()

