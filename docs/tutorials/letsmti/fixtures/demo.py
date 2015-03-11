from lino.api import rt
from lino.utils import mti


def findbyname(model, name):
    """
    Utility function.
    """
    return model.objects.get(name=name)


def objects():
    """This will be called by the :ref:`dpy` deserializer during
    :manage:`initdb_demo` and must yield a list of object instances to
    be saved.

    """
    Place = rt.modules.letsmti.Place
    Member = rt.modules.letsmti.Member
    Customer = rt.modules.letsmti.Customer
    Supplier = rt.modules.letsmti.Supplier
    Product = rt.modules.letsmti.Product

    def offer(what, who):
        return rt.modules.letsmti.Offer(
            product=findbyname(Product, what),
            supplier=findbyname(Supplier, who))

    def demand(what, who):
        return rt.modules.letsmti.Demand(
            product=findbyname(Product, what),
            customer=findbyname(Customer, who))

    def member(name, place, email=''):
        return Member(
            name=name, email=email,
            place=findbyname(Place, place))

    def customer(name, place, email=''):
        return Customer(
            name=name, email=email,
            place=findbyname(Place, place))

    def supplier(name, place, email=''):
        return Supplier(
            name=name, email=email,
            place=findbyname(Place, place))

    def customer_supplier(name, place, email=''):
        m = Member(
            name=name, email=email,
            place=findbyname(Place, place))
        m.save()
        mti.insert_child(m, Customer)
        mti.insert_child(m, Supplier)
        # return (m, c, s)
        return m

    yield Place(name="Tallinn")
    yield Place(name="Tartu")
    yield Place(name="Vigala")
    yield Place(name="Haapsalu")

    yield Product(name="Bread")
    yield Product(name="Buckwheat")
    yield Product(name="Eggs")
    yield Product(name="Sanitary repair work")
    yield Product(name="Building repair work")
    yield Product(name="Electricity repair work")

    yield supplier("Fred", "Tallinn", 'fred@example.com')
    yield supplier("Argo", "Haapsalu", 'argo@example.com')
    yield member("Peter", "Vigala", 'peter@example.com')
    yield supplier("Anne", "Tallinn", 'anne@example.com')
    yield member("Jaanika", "Tallinn", 'jaanika@example.com')

    yield customer_supplier("Henri", "Tallinn", 'henri@example.com')
    yield customer_supplier("Mari", "Tartu", 'mari@example.com')
    yield customer_supplier("Katrin", "Vigala", 'katrin@example.com')

    yield offer("Bread", "Fred")
    yield offer("Buckwheat", "Fred")
    yield offer("Buckwheat", "Anne")
    yield offer("Electricity repair work", "Henri")
    yield offer("Electricity repair work", "Argo")

    yield demand("Buckwheat", "Henri")
    yield demand("Eggs", "Henri")
    yield demand("Eggs", "Mari")

