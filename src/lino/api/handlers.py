from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc, require_mime, require_extended

from blogserver.blog.models import Blogpost

class ReportHandler(BaseHandler):
    model = None
    fields = None

    @classmethod
    def content_length(cls, blogpost):
        return len(blogpost.content)

    @classmethod
    def resource_uri(cls, blogpost):
        return ('blogposts', [ 'json', ])

    def read(self, request, pk=None):
        """
        Returns one instance if `pk` is given,
        otherwise all the instances.
        
        Parameters:
         - `pk`: The primary key of the instance to retrieve.
        """
        if pk:
            return self.lino_rh.queryset.get(pk=pk)
        base = self.model.objects
        
        if title:
            return base.get(title=title)
        else:
            return base.all()

    def create(self, request):
        """
        Creates a new blogpost.
        """
        attrs = self.flatten_dict(request.POST)

        if self.exists(**attrs):
            return rc.DUPLICATE_ENTRY
        else:
            post = Blogpost(title=attrs['title'], 
                            content=attrs['content'],
                            author=request.user)
            post.save()
            
            return post
            
def reporthandler_factory(rh):
    h = ReportHandler()
    h.model = rh.report.model
    h.fields = [f.name for f in rh.list_layout._store_fields]
    h.lino_rh = rh
    return h

            
