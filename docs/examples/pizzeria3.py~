from lino.apps.pizzeria.pizzeria import Product, OrderLine
from lino.apps.pizzeria.services import \
     MyPizzeria, populate

app = MyPizzeria()
sess = app.createContext()
populate(sess)

p=sess.query(Product).peek(1)

qry = sess.query(OrderLine,"order.date order.customer",
                 product=p)
qry.show(
    columnWidths="10 13",
    title="Who bought %s (product# %s)?" % (p.name, p.id))

print
print qry.getSqlSelect()

