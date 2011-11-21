from lino.django.contacts.models import Person, Organisation, Contact, Country, City, Place
from django.contrib import admin

class PersonAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               dict(fields=['title','firstname','name'])),
        ('Date information', dict(fields=['birthdate'], 
          classes=['collapse'])),
    ]
    list_display = ('name', 'firstname', 'contacts', 'birthdate', 'age')
    list_filter = ['name','firstname']
    search_fields = ['name','firstname']
    
class CityInline(admin.TabularInline):
    model=City

class PlaceCityInline(admin.TabularInline):
    "to display the places of a City"
    model=Place
    
class CountryAdmin(admin.ModelAdmin):
    inlines = [ CityInline ]

class CityAdmin(admin.ModelAdmin):
    #~ fieldsets = [
        #~ (None,               dict(fields=['name','country'])),
        #~ ('Contacts', dict(fields=['contacts'], 
          #~ classes=['collapse'])),
    #~ ]
    list_display = ('name', 'country', 'contacts')
    
    
    
admin.site.register(Person, PersonAdmin)
admin.site.register(Organisation)
admin.site.register(Place)
admin.site.register(Contact)
admin.site.register(Country,CountryAdmin)
admin.site.register(City,CityAdmin)


