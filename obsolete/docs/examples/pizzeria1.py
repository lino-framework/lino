from lino.apps.pizzeria.pizzeria import Pizzeria, populate, Order

app = Pizzeria() 

dbc = app.createContext()
    
populate(dbc)

orders = dbc.query(Order,"customer totalPrice")

for o in orders:
    print "%s must pay %d EUR" % (o.customer.name, o.totalPrice)

del app, dbc, orders, o
