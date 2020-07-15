# -*- coding: UTF-8 -*-
# Copyright 2002-2020 Rumma & Ko Ltd
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

import sys
from sphinx.ext import autosummary
from typing import Any, Dict, List, Tuple
from sphinx.ext.autodoc.importer import import_module
from sphinx.util import logging ; logger = logging.getLogger(__name__)


# patch for autosummary. This version of import_by_name doesn't swallow the traceback
# and imports only the first item prefixes
# def my_import_by_name(name: str, prefixes: List[str] = [None]) -> Tuple[str, Any, Any, str]:
#     """Import a Python object that has the given *name*, under one of the
#     *prefixes*.  The first name that succeeds is used.
#     """
#     for prefix in prefixes:
#         if prefix:
#             prefixed_name = '.'.join([prefix, name])
#         else:
#             prefixed_name = name
#         obj, parent, modname = _import_by_name(prefixed_name)
#         return prefixed_name, obj, parent, modname

# temporary patch reports failed imports
def _import_by_name(name: str) -> Tuple[Any, Any, str]:
    """Import a Python object given its full name."""

    try:
        name_parts = name.split('.')

        # # 20200429 first try whether it is a full module name
        # try:
        #     mod = import_module(name)
        #     parent_name = '.'.join(name_parts[:-1])
        #     if parent_name:
        #         parent = import_module(parent_name)
        #     else:
        #         parent = None
        #     return parent, mod, name
        # except ImportError:
        #     pass

        # try first interpret `name` as MODNAME.OBJ
        modname = '.'.join(name_parts[:-1])
        if modname:
            try:
                mod = import_module(modname)
                return getattr(mod, name_parts[-1]), mod, modname
            except (ImportError, IndexError, AttributeError):
                pass

        # ... then as MODNAME, MODNAME.OBJ1, MODNAME.OBJ1.OBJ2, ...
        last_j = 0
        modname = None
        for j in reversed(range(1, len(name_parts) + 1)):
            last_j = j
            modname = '.'.join(name_parts[:j])
            try:
                import_module(modname)
            except ImportError as e:
                logger.info("Failed to import %s : %s", modname, e)
                continue

            if modname in sys.modules:
                break

        if last_j < len(name_parts):
            parent = None
            obj = sys.modules[modname]
            for obj_name in name_parts[last_j:]:
                parent = obj
                obj = getattr(obj, obj_name)
            return obj, parent, modname
        else:
            return sys.modules[modname], None, modname
    except (ValueError, ImportError, AttributeError, KeyError) as e:
        raise ImportError(*e.args)

# autosummary.import_by_name = my_import_by_name
autosummary._import_by_name = _import_by_name


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
        print("Django started with DJANGO_SETTINGS_MODULE={}.".format(settings_module_name))
        from django.conf import settings
        print(settings.SITE.welcome_text())
        # print(settings.SITE.diagnostic_report_rst())

        # os.environ['DJANGO_SETTINGS_MODULE'] = settings_module_name

        # # Trigger loading of Djangos model cache in order to avoid
        # # side effects that would occur when this happens later while
        # # importing one of the models modules.
        # from django.conf import settings
        # settings.SITE.startup()

        # globals_dict.update(
        #     template_bridge=str('lino.sphinxcontrib.DjangoTemplateBridge'))

    intersphinx_mapping = globals_dict.setdefault('intersphinx_mapping', dict())
    intersphinx_mapping['cg'] = ('https://community.lino-framework.org/', None)
    intersphinx_mapping['book'] = ('https://www.lino-framework.org/', None)
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
