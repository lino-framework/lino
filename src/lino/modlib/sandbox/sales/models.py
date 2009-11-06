"""

>>> luc = contacts.Contact(first_name="Luc",last_name="Saffre")
>>> luc.save()
>>> luc
<Contact: Luc Saffre>

>>> cust = Customer(contact=luc)
>>> cust.save()
>>> cust.last_name
Saffre

# the following fails because of ticket #7626
# http://code.djangoproject.com/ticket/7623

"""

from django.db import models
from lino.apps.sandbox.contacts import models as contacts

# extends Contact

class Customer(contacts.Contact):
    contact = models.OneToOneField(contacts.Contact,parent_link=True)
    payment_term = models.IntegerField(blank=True,null=True)
    
