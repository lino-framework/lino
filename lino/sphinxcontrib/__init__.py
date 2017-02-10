# -*- coding: UTF-8 -*-
# Copyright 2002-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Some extensions for Sphinx.

.. autosummary::
   :toctree:

   logo
   actordoc
   help_texts_extractor

"""

from atelier import sphinxconf

def configure(globals_dict, settings_module_name=None):
    """Same as :func:`atelier.sphinxconf.configure` but with an additional
    positional parameter `settings_module_name`.  If this is
    specified, call lino startup on it.

    """
    if settings_module_name is not None:
        from lino import startup
        startup(settings_module_name)

        # os.environ['DJANGO_SETTINGS_MODULE'] = settings_module_name

        # # Trigger loading of Djangos model cache in order to avoid
        # # side effects that would occur when this happens later while
        # # importing one of the models modules.
        # from django.conf import settings
        # settings.SITE.startup()

        globals_dict.update(
            template_bridge=str('atelier.sphinxconf.DjangoTemplateBridge'))
    return sphinxconf.configure(globals_dict)

    

