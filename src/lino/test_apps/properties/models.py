"""

  >>> CHAR = ContentType.objects.get_for_model(properties.CharPropValue)
  >>> INT = ContentType.objects.get_for_model(properties.IntegerPropValue)
  >>> BOOL = ContentType.objects.get_for_model(properties.BooleanPropValue)

  >>> weight = properties.Property(name='weight',value_type=INT)
  >>> weight.save()
  >>> favdish = properties.Property(name='favorite dish',value_type=CHAR)
  >>> favdish.save()
  >>> favdish.create_value("Cookies")
  <CharPropValue: favorite dish: Cookies>
  >>> favdish.create_value("Fish")
  <CharPropValue: favorite dish: Fish>
  >>> favdish.create_value("Meat")
  <CharPropValue: favorite dish: Meat>
  >>> favdish.create_value("Vegetables")
  <CharPropValue: favorite dish: Vegetables>
  
  >>> print [v.value for v in favdish.choices_list()]
  [u'Cookies', u'Fish', u'Meat', u'Vegetables']

  >>> chris = Person(name='Chris')
  >>> fred = Person(name='Fred')
  >>> vera = Person(name='Vera')
  >>> mary = Person(name='Mary')
  
How to set a property value:  
  
  >>> weight.set_value_for(chris,70)
  >>> weight.set_value_for(fred,80)
  >>> weight.set_value_for(vera,60)
  >>> weight.set_value_for(mary,50)
  
  >>> favdish.set_value_for(chris,'Cookies')
  >>> favdish.set_value_for(fred,'Fish')
  >>> favdish.set_value_for(vera,'Vegetables')
  >>> favdish.set_value_for(mary,'Meat')
  
  >>> properties.PropValuesByOwner().as_text(fred)



"""


from django.db import models
from django.contrib.contenttypes.models import ContentType
from lino.modlib.properties import models as properties 
    
class Person(models.Model):
    name = models.CharField(max_length=20,blank=True,null=True)
    
