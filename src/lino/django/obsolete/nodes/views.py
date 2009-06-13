## Copyright 2007 Luc Saffre.
## This file is part of the Lino project. 

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


from lino.django.nodes.models import Node
from lino.htgen import Document
#from django.shortcuts import get_object_or_404
from django.shortcuts import _get_queryset
from django.http import HttpResponse, Http404

#from django.shortcuts import render_to_response, get_object_or_404
#from stools import nations


def get_object_or_404(klass, *args, **kwargs):
    """ modified copy of django.shortcuts.get_object_or_404
    shows the query's parameters if DoesNotExist.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise Http404('No %s matches the query (%r,%r).' % 
        (queryset.model._meta.object_name,args,kwargs))




def index(request):
    name=request.META["PATH_INFO"]
    if name == "/" or name == "":
        name='index'
    return detail_by_name(request,name)

def latest_nodes():
    return Node.objects.all().order_by('-published')[:5]



def detail(request, node_id):
    n = get_object_or_404(Node,pk=node_id)
    return render_node(request,n)
    #return render_to_response('cms/detail.html', {'node': n})

def detail_by_name(request, name):
    n=None
    for part in name.split('/'):
        if len(part) != 0:
          if n is None:
            n = get_object_or_404(Node,name=part,
                                  parent__isnull=True)
          else:
            n = get_object_or_404(Node,name=part,parent=n)
    return render_node(request,n)
    # return render_to_response('cms/detail.html', {'node': n})


def render_node(request, node):
    d=Document(node.title)
    d.h1(d.title)
    d.memo(node.abstract)
    d.memo(node.body)
    return HttpResponse(d.toxml())

#def edit(request, node_id):
#    n = get_object_or_404(Node,pk=node_id)
#    return render_to_response('cms/edit.html', {'node': n})
#    return HttpResponse(t.render(c))

#def test1(request):
    

## from django.core.exceptions import ObjectDoesNotExist
## from django.template import Context, RequestContext, loader
## from django.contrib.contenttypes.models import ContentType
## from django.contrib.sites.models import Site
## from django import http

## def shortcut(request, content_type_id, object_id):
##     "Redirect to an object's page based on a content-type ID and an object ID."
##     # Look up the object, making sure it's got a get_absolute_url() function.
##     try:
##         content_type = ContentType.objects.get(pk=content_type_id)
##         obj = content_type.get_object_for_this_type(pk=object_id)
##     except ObjectDoesNotExist:
##         raise http.Http404, "Content type %s object %s doesn't exist" % (content_type_id, object_id)
##     try:
##         absurl = obj.get_absolute_url()
##     except AttributeError:
##         raise http.Http404, "%s objects don't have get_absolute_url() methods" % content_type.name

##     # Try to figure out the object's domain, so we can do a cross-site redirect
##     # if necessary.

##     # If the object actually defines a domain, we're done.
##     if absurl.startswith('http://') or absurl.startswith('https://'):
##         return http.HttpResponseRedirect(absurl)

##     object_domain = None

##     # Otherwise, we need to introspect the object's relationships for a
##     # relation to the Site object
##     opts = obj._meta

##     # First, look for an many-to-many relationship to sites
##     for field in opts.many_to_many:
##         if field.rel.to is Site:
##             try:
##                 object_domain = getattr(obj, field.name).all()[0].domain
##             except IndexError:
##                 pass
##             if object_domain is not None:
##                 break

##     # Next look for a many-to-one relationship to site
##     if object_domain is None:
##         for field in obj._meta.fields:
##             if field.rel and field.rel.to is Site:
##                 try:
##                     object_domain = getattr(obj, field.name).domain
##                 except Site.DoesNotExist:
##                     pass
##                 if object_domain is not None:
##                     break

##     # Fall back to the current site (if possible)
##     if object_domain is None:
##         try:
##             object_domain = Site.objects.get_current().domain
##         except Site.DoesNotExist:
##             pass

##     # If all that malarkey found an object domain, use it; otherwise fall back
##     # to whatever get_absolute_url() returned.
##     if object_domain is not None:
##         protocol = request.is_secure() and 'https' or 'http'
##         return http.HttpResponseRedirect('%s://%s%s' % (protocol, object_domain, absurl))
##     else:
##         return http.HttpResponseRedirect(absurl)

