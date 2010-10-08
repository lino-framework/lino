"""
This package is meant for internal use. 
Should not be imported in your `models` 
modules because they need the LinoSite to be set up.
"""

from django.utils.translation import ugettext_lazy as _

boolean_texts = (_('Yes'),_('No'),' ')
