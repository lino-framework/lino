# -*- coding: UTF-8 -*-

from lino import rt


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
    Place = rt.modules.lets.Place
    Member = rt.modules.lets.Member
    Product = rt.modules.lets.Product

    def offer(what, who):
        return rt.modules.lets.Offer(
            product=findbyname(Product, what),
            provider=findbyname(Member, who))

    def demand(what, who):
        return rt.modules.lets.Demand(
            product=findbyname(Product, what),
            customer=findbyname(Member, who))

    yield Place(name="Tallinn")
    yield Place(name="Tartu")
    yield Place(name="Vigala")
    yield Place(name="Haapsalu")

    yield Member(name="Fred", place=findbyname(Place, "Tallinn"))
    yield Member(name="Argo", place=findbyname(Place, "Haapsalu"))
    yield Member(name="Peter", place=findbyname(Place, "Vigala"))
    yield Member(name="Anne", place=findbyname(Place, "Tallinn"))
    yield Member(name="Jaanika", place=findbyname(Place, "Tallinn"))

    yield Member(name="Henri", place=findbyname(Place, "Tallinn"))
    yield Member(name="Mare", place=findbyname(Place, "Tartu"))
    yield Member(name="Katrin", place=findbyname(Place, "Vigala"))

    yield Product(name="Bread")
    yield Product(name="Buckwheat")
    yield Product(name="Eggs")

    yield offer("Bread", "Fred")
    yield offer("Buckwheat", "Fred")
    yield offer("Buckwheat", "Anne")

    yield demand("Buckwheat", "Henri")
    yield demand("Eggs", "Henri")
    yield demand("Eggs", "Mare")

