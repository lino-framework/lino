# a work-around for ticket 7623
# http://code.djangoproject.com/ticket/7623
# inspired by Tom Tobin's patch suggestion 
# http://bazaar.launchpad.net/~theonion/django/makechild/revision/5060

def child_from_parent(model, *parents,**kw):
    model_parents = tuple(model._meta.parents.keys())
    if not model_parents:
        raise ValueError("%r is not a child model; it has no parents" % model)
    attrs = {}
    for parent in parents:
        if not isinstance(parent, model_parents):
            raise ValueError("%r is not a parent instance of %r" % (parent, model))
        for field in parent._meta.fields:
            if field.name not in attrs:
                attrs[field.name] = getattr(parent, field.name)

        attrs[model._meta.parents[parent.__class__].name] = parent
    attrs.update(kw)
    return model(**attrs)

