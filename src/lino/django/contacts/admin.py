from lino.django.contacts.models import Person, Organisation, Contact, Country, City
from django.contrib import admin

class PersonAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               dict(fields=['title','firstname','name'])),
        ('Date information', dict(fields=['birthdate'], 
          classes=['collapse'])),
    ]
    list_display = ('name', 'firstname', 'title', 'birthdate', 'age')
    list_filter = ['name','firstname']
    search_fields = ['name','firstname']
    
    
admin.site.register(Person, PersonAdmin)
admin.site.register(Organisation)
admin.site.register(Contact)
admin.site.register(Country)
admin.site.register(City)


