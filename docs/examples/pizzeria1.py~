from lino.apps.pizzeria.pizzeria import Pizzeria, populate, Order

app = Pizzeria() 

sess = app.quickStartup()
    
populate(sess)

orders = sess.query(Order,"customer totalPrice")

for o in orders:
    print "%s must pay %d EUR" % (o.customer.name, o.totalPrice)
