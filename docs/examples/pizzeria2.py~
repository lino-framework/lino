from lino.apps.pizzeria.services import makeSchema, populate, Orders

schema = makeSchema(label="Luc's Pizza Service")

sess = schema.quickStartup()
    
populate(sess)

orders = sess.query(Orders)

o = orders.peek(3)

print "Order #:", o.id
print "Date:", o.date
print "Customer:", o.customer.name
print "-" * 40
for line in o.lines:
    print "%-20s %3d %5d" % (line.product.name,
                             line.qty,
                             line.product.price*line.qty)
print "-" * 40
print "Total: ", o.totalPrice

