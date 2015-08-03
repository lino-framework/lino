from lino.modlib.bootstrap3.renderer import Renderer

from lino.modlib.tickets.models import Ticket


class Renderer(Renderer):
    
    def get_detail_url(self, obj, *args, **kw):
        if isinstance(obj, Ticket):
            return self.plugin.build_plain_url(
                'ticket', str(obj.id), *args, **kw)

        return self.plugin.build_plain_url(
            obj._meta.app_label,
            obj.__class__.__name__,
            str(obj.pk), *args, **kw)


