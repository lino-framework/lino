# -*- coding: UTF-8 -*-
# Copyright 2002-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Some extensions for Sphinx.

.. autosummary::
   :toctree:

   base
   logo
   actordoc
   help_texts_extractor

"""

from atelier import sphinxconf

def configure(globals_dict, settings_module_name=None):
    """
    Same as :func:`atelier.sphinxconf.configure` but with an
    additional positional argument `settings_module_name` (the name of
    a Django settings module).  If this argument is specified, call
    :meth:`lino.startup` with it.
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

        # globals_dict.update(
        #     template_bridge=str('lino.sphinxcontrib.DjangoTemplateBridge'))
    return sphinxconf.configure(globals_dict)

    

# from sphinx.jinja2glue import BuiltinTemplateLoader


# class DjangoTemplateBridge(BuiltinTemplateLoader):

#     """The :meth:`configure` method installs this as `template_bridge
#     <http://sphinx-doc.org/config.html#confval-template_bridge>`_ for
#     Sphinx.  It causes a template variable ``settings`` to be added
#     the Sphinx template context. This cannot be done using
#     `html_context
#     <http://sphinx-doc.org/config.html#confval-html_context>`_ because
#     Django settings are not pickleable.

#     """

#     def render(self, template, context):
#         from django.conf import settings
#         context.update(settings=settings)
#         return super(DjangoTemplateBridge, self).render(template, context)

#     def render_string(self, source, context):
#         from django.conf import settings
#         context.update(settings=settings)
#         return super(DjangoTemplateBridge, self).render_string(source, context)


