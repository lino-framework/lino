from lino.apps.pizzeria.pizzeria import Pizzeria, populate, Orders

app = Pizzeria() #label="Luc's Pizza Restaurant")

sess = app.quickStartup()
    
populate(sess)

orders = sess.query(Orders,"customer totalPrice")

for o in orders:
    print "%s must pay %d EUR" % (o.customer.name, o.totalPrice)
