from lino.api import dd
from .choicelists import UploadAreas

class UploadController(dd.Model):
    
    class Meta(object):
        abstract = True
        
    def get_upload_area(self):
        return UploadAreas.general

