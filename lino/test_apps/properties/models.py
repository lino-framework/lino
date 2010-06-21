"""
Module `lino.modlib.properties`
-------------------------------

Imagine that we are doing a study about alimentary habits. We observe a 
defined series of properties on the people who participate in our study.
Here are the properties that we are going to observe::


  >>> weight = properties.INT.create_property(name='weight')
  >>> weight.save()
  
  >>> married = properties.BOOL.create_property(name='married')
  >>> married.save()
  
  >>> favdish = properties.CHAR.create_property(name='favdish',label='favorite dish')
  >>> favdish.save()
  >>> favdish.create_value("Cookies").save()
  >>> v = favdish.create_value("Fish").save()
  >>> favdish.create_value("Meat").save()
  >>> favdish.create_value("Vegetables").save()

  
Now we have setup the properties. Let's have a look at this metadata::
  
  >>> print favdish.choices_list()
  [u'Cookies', u'Fish', u'Meat', u'Vegetables']
  >>> qs = properties.Property.objects.all()
  >>> ["%s (%s)" % (p.name,','.join(map(unicode,p.choices_list()))) for p in qs]
  [u'weight ()', u'married (True,False)', u'favdish (Cookies,Fish,Meat,Vegetables)']
  
PropValuesByOwner is a report that cannot be rendered into a normal grid because the 'value' column has variable data type, but it's render_to_dict() method is used to fill an `Ext.grid.PropertyGrid`:

  >>> properties.PropValuesByOwner().request(master=Person).render_to_dict()
  {'count': 3, 'rows': [{'name': u'favdish', 'value': ''}, {'name': u'married', 'value': None}, {'name': u'weight', 'value': None}], 'title': u'Properties for persons'}
  
 
Here are the people we are going to analyze::

  >>> chris = Person(name='Chris')
  >>> chris.save()
  >>> fred = Person(name='Fred')
  >>> fred.save()
  >>> vera = Person(name='Vera')
  >>> vera.save()
  >>> mary = Person(name='Mary')
  >>> mary.save()
  
Now we are ready to fill in some real data. Chris, Fred and Vera 
answered together to each question. First we asked them "What's 
your weight?", and they answered:
  
  >>> weight.set_value_for(chris,70)
  >>> weight.set_value_for(fred,110)
  >>> weight.set_value_for(vera,60)
  
When asked whether they were married, they answered:
  
  >>> married.set_value_for(chris,True)
  >>> married.set_value_for(fred,False)
  >>> married.set_value_for(vera,True)

And about their favourite dish they answered:
  
  >>> favdish.set_value_for(chris,'Cookies')
  >>> favdish.set_value_for(fred,'Fish')
  >>> favdish.set_value_for(vera,'Vegetables')

Mary came later. She answered all questions at once, which we can enter 
in one line of code:
  
  >>> properties.set_value_for(mary,married=True,favdish='Meat')
  
Note that Mary didn't know her weight.

To see the property values of a person, we can use a manual query...

  >>> qs = properties.PropValue.objects.filter(owner_id=fred.pk).order_by('prop__name')
  >>> [v.by_owner() for v in qs]
  [u'favdish: Fish', u'married: False', u'weight: 110']
  
... or use the `PropValuesByOwner` report:

  >>> properties.PropValuesByOwner().request(master_instance=fred).render_to_dict()
  {'count': 3, 'rows': [{'name': u'favdish', 'value': u'Fish'}, {'name': u'married', 'value': False}, {'name': u'weight', 'value': 110}], 'title': u'Properties for Fred'}
  
Note how properties.PropValuesByOwner also returns 3 rows for Mary although we don't know her weight:
  
  >>> properties.PropValuesByOwner().request(master_instance=mary).render_to_dict()
  {'count': 3, 'rows': [{'name': u'favdish', 'value': u'Meat'}, {'name': u'married', 'value': True}, {'name': u'weight', 'value': None}], 'title': u'Properties for Mary'}
  
Query by property:

  >>> qs = properties.PropValue.objects.filter(prop=weight) 
  >>> [v.by_property() for v in qs]
  [u'Chris: 70', u'Fred: 110', u'Vera: 60']
  
  >>> qs = weight.values_query().order_by('value')
  >>> [v.by_property() for v in qs]
  [u'Vera: 60', u'Chris: 70', u'Fred: 110']
  
  
`Report.as_text()`, is currently broken:

  >>> #properties.PropValuesByOwner().as_text(fred)


"""


from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from lino.modlib.properties import models as properties 
    
class Person(models.Model):
    name = models.CharField(max_length=20)
    properties = generic.GenericRelation(properties.Property)
    
    def __unicode__(self):
        return self.name
        
