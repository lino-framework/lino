import settings
from django.core.management import setup_environ
setup_environ(settings)

from lino.django.apps.sales.utils import make_invoices
make_invoices()