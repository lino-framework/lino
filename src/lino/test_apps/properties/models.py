"""

  >>> CHAR = ContentType.objects.get_for_model(properties.CharPropValue)
  >>> INT = ContentType.objects.get_for_model(properties.IntegerPropValue)
  >>> BOOL = ContentType.objects.get_for_model(properties.BooleanPropValue)
  
Imagine that we are doing a study about alimentary habits. We observe a 
defined series of properties on the people who participate in our study.
Here are the properties that we are going to observe:

  >>> weight = properties.Property(name='weight',value_type=INT)
  >>> weight.save()
  
  >>> married = properties.Property(name='married',value_type=BOOL)
  >>> married.save()
  
  >>> favdish = properties.Property(name='favdish',value_type=CHAR,label='favorite dish')
  >>> favdish.save()
  >>> favdish.create_value("Cookies")
  <CharPropValue: One choice for 'favorite dish' is Cookies>
  >>> favdish.create_value("Fish")
  <CharPropValue: One choice for 'favorite dish' is Fish>
  >>> favdish.create_value("Meat")
  <CharPropValue: One choice for 'favorite dish' is Meat>
  >>> favdish.create_value("Vegetables")
  <CharPropValue: One choice for 'favorite dish' is Vegetables>
  
Now we have setup the properties. Let's have a look at this metadata:
  
  >>> print [v.value for v in favdish.choices_list()]
  [u'Cookies', u'Fish', u'Meat', u'Vegetables']
  >>> qs = properties.Property.objects.all()
  >>> ["%s (%s)" % (p.name,','.join([pv.value for pv in p.choices_list()])) for p in qs]
  [u'weight ()', u'married ()', u'favdish (Cookies,Fish,Meat,Vegetables)']
  
  
  
Here are the people we are going to analyze:  

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
  >>> weight.set_value_for(fred,80)
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
  
Note that she didn't know her weight.

To see the property values of a person, we can use the 
`PropValuesByOwner` report:

  >>> qs = properties.PropValuesByOwner().get_queryset(fred)
  >>> [v.by_owner() for v in qs]
  [u'favdish: Fish', u'married: False', u'weight: 80']
  
The following wouldn't work because owner is a GenericForeignKey:

  >>> # qs = properties.PropValue.objects.filter(owner=fred)
  
Query by property:

  >>> qs = properties.PropValue.objects.filter(prop=weight) 
  >>> [v.by_property() for v in qs]
  [u'Person object: 70', u'Person object: 80', u'Person object: 60']
  
  >>> qs = properties.PropValue.objects.filter(prop=weight).order_by('value_text')
  >>> [v.by_property() for v in qs]
  [u'Person object: 60', u'Person object: 70', u'Person object: 80']
  
  
`Report.as_text()`, is currently broken:

  >>> #properties.PropValuesByOwner().as_text(fred)


"""


from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from lino.modlib.properties import models as properties 
    
class Person(models.Model):
    name = models.CharField(max_length=20,blank=True,null=True)
    properties = generic.GenericRelation(properties.Property)
