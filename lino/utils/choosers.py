# Copyright 2009-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Extends the possibilities for defining choices for fields of a
Django model.

- Context-sensitive choices (see :ref:`lino.dev.combo`)
- Non-limiting choices (`force_selection` False) :
  specify a pick list of suggestions but leave the possibility
  to store manually entered values
- :ref:`learning_combos`


"""
from builtins import object
from builtins import str

from lino.api import rt
from lino.core import constants
from lino.core.utils import getrqdata
from lino.utils.instantiator import make_converter


class BaseChooser(object):
    pass


class FieldChooser(BaseChooser):

    def __init__(self, field):
        self.field = field


class ChoicesChooser(FieldChooser):

    def __init__(self, field):
        FieldChooser.__init__(self, field)
        self.simple_values = type(field.choices[0])


class Chooser(FieldChooser):
    """A **chooser** holds information about the possible choices of a
    field.

    """
    #~ stored_name = None
    simple_values = False
    instance_values = True
    force_selection = True
    choice_display_method = None  # not yet used.
    can_create_choice = False

    def __init__(self, model, field, meth):
        FieldChooser.__init__(self, field)
        self.model = model
        #~ self.field = model._meta.get_field(fldname)
        self.meth = meth
        from lino.core.gfks import is_foreignkey
        from lino.core.choicelists import ChoiceListField
        if isinstance(field, ChoiceListField):
            self.simple_values = getattr(meth, 'simple_values', False)
            self.instance_values = getattr(meth, 'instance_values', True)
            self.force_selection = getattr(
                meth, 'force_selection', self.force_selection)
        elif not is_foreignkey(field):
            self.simple_values = getattr(meth, 'simple_values', False)
            self.instance_values = getattr(meth, 'instance_values', False)
            self.force_selection = getattr(
                meth, 'force_selection', self.force_selection)
        #~ self.context_params = meth.func_code.co_varnames[1:meth.func_code.co_argcount]
        self.context_params = meth.context_params
        #~ self.multiple = meth.multiple
        #~ self.context_params = meth.func_code.co_varnames[:meth.func_code.co_argcount]
        #~ print '20100724', meth, self.context_params
        #~ logger.warning("20100527 %s %s",self.context_params,meth)
        self.context_values = []
        self.context_fields = []
        for name in self.context_params:
            if name == "ar":
                continue
            f = self.get_data_elem(name)

            if f is None:
                raise Exception(
                    "No data element '%s' in %s "
                    "(method %s_choices)" % (
                        name, self.model, field.name))
            #~ if name == 'p_book':
                #~ print 20131012, f
            self.context_fields.append(f)
            self.context_values.append(name + "Hidden")
            #~ if isinstance(f,models.ForeignKey):
                #~ self.context_values.append(name+"Hidden")
            #~ else:
                #~ self.context_values.append(name)
        self.converters = []
        #~ try:
        for f in self.context_fields:
            cv = make_converter(f)
            if cv is not None:
                self.converters.append(cv)
        #~ except models.FieldDoesNotExist,e:
            #~ print e

        if hasattr(model, "create_%s_choice" % field.name):
            self.can_create_choice = True

        m = getattr(model, "%s_choice_display" % field.name, None)
        if m is not None:
            self.choice_display_method = m

    def __str__(self):
        return "Chooser(%s.%s,%s)" % (
            self.model.__name__, self.field.name,
            self.context_params)

    def create_choice(self, obj, text):
        m = getattr(obj, "create_%s_choice" % self.field.name)
        return m(text)

    def get_data_elem(self, name):
        """Calls :meth:`dd.Actor.get_data_elem` or
        :meth:`dd.Model.get_data_elem` or
        :meth:`dd.Action.get_data_elem`.

        """
        de = self.model.get_data_elem(name)
        if de is None:
            return self.model.get_param_elem(name)
        return de

    def __call__(self, *args, **kw):
        for i, v in enumerate(args):
            kw[self.context_fields[i]] = v
        return self.get_choices(**kw)

    def get_choices(self, **context):
        """Return a list of choices for this chooser, using keyword parameters
        as context.

        """
        args = []
        for varname in self.context_params:
            args.append(context.get(varname, None))
        return self.meth(*args)

    def get_request_choices(self, ar, tbl):
        """
        Return a list of choices for this chooser,
        using a HttpRequest to build the context.
        """
        kw = {
            "ar": ar,
        }
        # kw = {}

        # ba = tbl.get_url_action(tbl.default_elem_action_name)
        # 20120202
        if tbl.master_field is not None:
            rqdata = getrqdata(ar.request)
            if tbl.master is not None:
                master = tbl.master
            else:
                mt = rqdata.get(constants.URL_PARAM_MASTER_TYPE)
                ContentType = rt.models.contenttypes.ContentType
                try:
                    master = ContentType.objects.get(pk=mt).model_class()
                except ContentType.DoesNotExist:
                    master = None

            pk = rqdata.get(constants.URL_PARAM_MASTER_PK, None)
            if pk and master:
                try:
                    kw[tbl.master_field.name] = master.objects.get(pk=pk)
                except ValueError:
                    raise Exception(
                        "Invalid primary key %r for %s", pk, master.__name__)
                except master.DoesNotExist:
                    raise Exception("There's no %s with primary key %r" %
                                    (master.__name__, pk))

        for k, v in list(ar.request.GET.items()):
            kw[str(k)] = v

        # logger.info(
        #     "20130513 get_request_choices(%r) -> %r",
        #     tbl, kw)

        for cv in self.converters:
            kw = cv.convert(**kw)

        if tbl.known_values:
            kw.update(tbl.known_values)

        if False:  # removed 20120815 #1114
            #~ ar = tbl.request(ui,request,tbl.default_action)
            if ar.create_kw:
                kw.update(ar.create_kw)
            if ar.known_values:
                kw.update(ar.known_values)
            if tbl.master_key:
                kw[tbl.master_key] = ar.master_instance
            #~ if tbl.known_values:
                #~ kw.update(tbl.known_values)
        return self.get_choices(**kw)  # 20120918b

    def get_text_for_value(self, value, obj):
        m = getattr(self.field, 'get_text_for_value', None)
        if m is not None:  # e.g. lino.utils.choicelist.ChoiceListField
            return m(value)
        #~ raise NotImplementedError
        #~ assert not self.simple_values
        m = getattr(obj, "get_" + self.field.name + "_display", str)
        #~ if m is None:
            #~ raise Exception("")
        return m(value)
        #~ raise NotImplementedError("%s : Cannot get text for value %r" % (self.meth,value))


def uses_simple_values(holder, fld):
    "used by :class:`lino.core.store`"
    from lino.core.gfks import is_foreignkey
    if is_foreignkey(fld):
        return False
    # if isinstance(fld, models.OneToOneRel):
    #     return False
    if holder is not None:
        ch = holder.get_chooser_for_field(fld.name)
        if ch is not None:
            return ch.simple_values
    choices = list(fld.choices)
    if len(choices) == 0:
        return True
    if type(choices[0]) in (list, tuple):
        return False
    return True


def _chooser(make, **options):
    #~ options.setdefault('quick_insert_field',None)
    def chooser_decorator(fn):
        def wrapped(*args):
            return fn(*args)
        cp = options.pop(
            'context_params',
            fn.__code__.co_varnames[1:fn.__code__.co_argcount])
        wrapped.context_params = cp
        for k, v in list(options.items()):
            setattr(wrapped, k, v)
        return make(wrapped)
        # return classmethod(wrapped)
        # A chooser on an action must not turn it into a classmethod
    return chooser_decorator


def chooser(**options):
    "Decorator which turns the method into a chooser."
    return _chooser(classmethod, **options)


def noop(x):
    return x


def action_chooser(**options):
    return _chooser(noop, **options)
