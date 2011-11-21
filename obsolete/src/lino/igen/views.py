# Create your views here.
raise "no longer used"

from django.http import HttpResponse

def root(request):
    return HttpResponse("""\
<html>
<a href="admin">admin</a>
<a href="db">db</a>
</html>
""")


from lino.django.igen.models import Invoice
from django.forms import ModelForm

class InvoiceForm(ModelForm):
    class Meta:
        model=Invoice
        
        
def invoice(request,number):
    
    if request.method == 'POST': # If the form has been submitted...
        form = InvoiceForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            form.save()
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        invoice=Invoice.objects.get(number=number)
        form=InvoiceForm(instance=invoice)
        form=InvoiceForm() # An unbound form

    return render_to_response('igen/invoice.html', {
        'form': form,
    })

