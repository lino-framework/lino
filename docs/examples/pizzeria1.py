from lino.apps.pizzeria.pizzeria import makeSchema, populate, Orders

schema = makeSchema(label="Luc's Pizza Restaurant")

sess = schema.quickStartup()
    
populate(sess)

orders = sess.query(Orders,"customer totalPrice")

for o in orders:
    print "%s must pay %d EUR" % (o.customer.name, o.totalPrice)
