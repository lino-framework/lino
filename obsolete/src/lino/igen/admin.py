from lino.django.igen import models
from django.contrib import admin

class ContactAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Person data", dict(fields=['title','firstName','lastName'])),
        ("Company data", dict(fields=['companyName','nationalId','vatId'])),
        ('Postal address', dict(fields=['addr1','addr2','city','zipCode','region',"country"])),
        ('Contact', dict(fields=['email','phone','gsm'])),
        ('Invoicing', dict(fields=['paymentTerm','vatExempt','itemVat'], 
          classes=['collapse'])),
        ('Other', dict(fields=['remarks','language'])),
    ]
    list_display = ('__unicode__', "companyName","lastName",
        "firstName", 'as_address')
    list_filter = ['firstName','lastName','companyName']
    search_fields = ['firstName','lastName','companyName']
    ordering=("companyName","lastName","firstName")
    
    
    
admin.site.register(models.Contact, ContactAdmin)
admin.site.register(models.Product)
admin.site.register(models.ProductCat)
#admin.site.register(models.Country)
#admin.site.register(models.Language)
admin.site.register(models.PaymentTerm)
admin.site.register(models.ShippingMode)
admin.site.register(models.SalesDocument)
admin.site.register(models.Invoice)
admin.site.register(models.Order)
admin.site.register(models.DocItem)
