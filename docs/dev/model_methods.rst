Special model methods
---------------------


def summary_row

@chooser
def FOO_choices(cls)
    "Return a queryset or list of allowed choices for field FOO."

def FOO_changed(self,old_value)
    "Called when field FOO of an instance of this model has been modified through the user interface."
    
def disable_delete(self,request):
    Hook to decide whether a given record may be deleted.
    Return a non-empty string with a message that explains why this record cannot be deleted.
        
def disabled_fields(self,request):
    return a list of names of fields that should be disabled (not editable) 
    for this record.
        

def get_queryset(self):
    return a customized default queryset


@classmethod
def setup_report(model,rpt):

def data_control(self):
    "Used by :class:`lino.models.DataControlListing`."

def save_auto_tasks(self):


def update_owned_task(self,task):
    task.person = self


def on_user_change(self,request):
    "Called when a record has been modified through the user interface."