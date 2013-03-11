from lino.ui import base
from lino.core import layouts

class Panel(object):
    def __init__(self,lh,name,vertical,*elems,**pkw):
        self.lh = lh
        self.name = name
        self.vertical = vertical
        self.elems = elems
        for k,v in pkw.items():
            setattr(self,k,v)
        #~ self.options = pkw
        
    def __html__(self,ar):
        if isinstance(self.lh.layout,layouts.ListLayout):
            return 'ext_elems.GridElement(lh,name,lh.layout._table,*elems,**pkw)'
        if isinstance(self.lh.layout,layouts.ParamsLayout) : 
            return 'ext_elems.ParamsPanel(lh,name,vertical,*elems,**pkw)'
        if isinstance(self.lh.layout,layouts.FormLayout): 
            if len(self.elems) == 1 or self.vertical:
                return 'ext_elems.DetailMainPanel(lh,name,vertical,*elems,**pkw)'
            else:
                return 'ext_elems.TabPanel(lh,name,*elems,**pkw)'
        raise Exception("No element class for layout %r" % self.lh.layout)
      
        
class UI(base.UI):
    """The central instance of Lino's ExtJS3 User Interface.
    """
    _handle_attr_name = '_groph_handle'
    #~ _response = None
    name = 'groph'
    verbose_name = "groph"
    
    def create_layout_element(self,lh,name,**kw):
        try:
            de = lh.get_data_elem(name)
            return de
        except Exception, e:
            de = None
            name += " (" + str(e) + ")"
            
        if hasattr(lh,'rh'):
            msg = "Unknown element %r referred in layout %s of %s." % (
                name,lh.layout,lh.rh.actor)
            l = [de.name for de in lh.rh.actor.wildcard_data_elems()]
            model = getattr(lh.rh.actor,'model',None) # VirtualTables don't have a model
            if getattr(model,'_lino_slaves',None):
                l += [str(rpt) for rpt in model._lino_slaves.values()]
            msg += " Possible names are %s." % ', '.join(l)
        else:
            msg = "Unknown element %r referred in layout %s." % (
                name,lh.layout)
            msg += "Cannot handle %r" % de
        raise KeyError(msg)


    def create_layout_panel(self,lh,name,vertical,elems,**kw):
        pkw = dict()
        pkw.update(labelAlign=kw.pop('label_align','top'))
        pkw.update(hideCheckBoxLabels=kw.pop('hideCheckBoxLabels',True))
        pkw.update(label=kw.pop('label',None))
        pkw.update(width=kw.pop('width',None))
        pkw.update(height=kw.pop('height',None))
        if kw:
            raise Exception("Unknown panel attributes %r" % kw)
        return Panel(lh,name,vertical,*elems,**pkw)


