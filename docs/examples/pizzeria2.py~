from lino.apps.pizzeria.pizzeria import Order
from lino.apps.pizzeria.services import ServicePizzeria, populate

app = ServicePizzeria() # label="Luc's Pizza Service")

sess = app.quickStartup()
    
populate(sess)

orders = sess.query(Order)

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

