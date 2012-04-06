# -*- coding: UTF-8 -*-
from lino.tools import resolve_model

def findbyname(model,name):
    """
    Utility function.
    """
    return model.objects.get(name=name)
    
def objects():
    """
    This will be called by the :term:`dumpy` deserializer and 
    must yield a list of object instances to be saved.
    """
    Place = resolve_model('lets.Place')
    Provider = resolve_model('lets.Provider')
    Customer = resolve_model('lets.Customer')
    Product = resolve_model('lets.Product')
    Offer = resolve_model('lets.Offer')
    Demand = resolve_model('lets.Demand')
    
    yield Place(name="Tallinn")
    yield Place(name="Tartu")
    yield Place(name="Vigala")
    yield Place(name="Haapsalu")
    
    yield Provider(name="Priit",place=findbyname(Place,"Tallinn"))
    yield Provider(name="Argo",place=findbyname(Place,"Haapsalu"))
    yield Provider(name=u"Tõnis",place=findbyname(Place,"Vigala"))
    yield Provider(name="Anne",place=findbyname(Place,"Tallinn"))
    yield Provider(name="Jaanika",place=findbyname(Place,"Tallinn"))
    
    yield Customer(name="Henri",place=findbyname(Place,"Tallinn"))
    yield Customer(name="Mare",place=findbyname(Place,"Tartu"))
    yield Customer(name=u"Külliki",place=findbyname(Place,"Vigala"))

    yield Product(name="Leib")
    yield Product(name="Tatar")
    yield Product(name="Kanamunad")

    yield Offer(product=findbyname(Product,"Leib"),provider=findbyname(Provider,"Priit"))
    yield Offer(product=findbyname(Product,"Tatar"),provider=findbyname(Provider,"Priit"))
    yield Offer(product=findbyname(Product,"Tatar"),provider=findbyname(Provider,"Anne"))
    
    yield Demand(product=findbyname(Product,"Tatar"),customer=findbyname(Customer,"Henri"))
    yield Demand(product=findbyname(Product,"Kanamunad"),customer=findbyname(Customer,"Henri"))
    yield Demand(product=findbyname(Product,"Kanamunad"),customer=findbyname(Customer,"Mare"))
      
