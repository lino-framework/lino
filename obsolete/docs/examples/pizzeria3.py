from lino.apps.pizzeria.pizzeria import Product, OrderLine
from lino.apps.pizzeria.services import \
     MyPizzeria, populate

app = MyPizzeria()
dbc = app.createContext()
populate(dbc)

p=dbc.query(Product).peek(1)

qry = dbc.query(OrderLine,"order.date order.customer",
                 product=p)
qry.show(
    columnWidths="10 13",
    title="Who bought %s (product# %s)?" % (p.name, p.id))

print
print qry.getSqlSelect()

#del qry, dbc, app

dbc.shutdown()
