Special model methods
---------------------

.. modmeth:: allow_cascaded_delete

    Set this to `True` on models whose objects should get automatically 
    deleted if a related object gets deleted. 
    Example: Lino should not refuse to delete 
    a Mail just because it has some 
    Recipient. 
    When deleting a Mail, Lino should also delete its Recipients.
    That's why :class:`lino.modlib.mails.models.Recipient` 
    has ``allow_cascaded_delete = True``.
    
.. modmeth:: disabled_fields

    return a list of names of fields that should be disabled (not editable) 
    for this record.
    
    Example::
    
      def disabled_fields(self,request):
          if self.user == request.user: return []
          df = ['field1']
          if self.foo:
            df.append('field2')
          return df
        
.. modmeth:: disable_delete

    Hook to decide whether a given record may be deleted.
    Return a non-empty string with a message that explains why this record cannot be deleted.
    
    Example::
    
      def disable_delete(self,request):
          if self.is_imported:
              return _("Cannot delete imported records.")
            
    
        
.. modmeth:: disable_editing

  ``disable_editing(self,request)``
      Return `True` if the whole record should be read-only.


.. modmeth:: FOO_choices

  Return a queryset or list of allowed choices for field FOO.
  Must be decorated by a :func:`lino.utils.choosers.chooser`.
  Example of a context-sensitive chooser method::
  
      
      country = models.ForeignKey("countries.Country",blank=True,null=True,
          verbose_name=_("Country"))
      city = models.ForeignKey('countries.City',blank=True,null=True,
          verbose_name=_('City'))
          
      @chooser()
      def city_choices(cls,country):
          if country is not None:
              return country.city_set.order_by('name')
          return cls.city.field.rel.to.objects.order_by('name')
      
  

.. modmeth:: FOO_changed

    Called when field FOO of an instance of this model has been modified through the user interface.
    Example::
    
      def city_changed(self,oldvalue):
          print "City changed from %s to %s!" % (oldvalue,self.city)

    
.. modmeth:: get_queryset

    Return a customized default queryset
    
    Example::

      def get_queryset(self):
          return self.model.objects.select_related('country','city','coach1','coach2','nationality')


.. modmeth:: data_control

  Used by :class:`lino.models.DataControlListing`.
    
  Example::

      def data_control(self):


.. modmeth:: on_user_change

  Called when a record has been modified through the user interface.
    
  Example::
  
    def on_user_change(self,request):


.. modmeth:: save_auto_tasks

  Example::
  
    def save_auto_tasks(self):


.. modmeth:: setup_report

  Example::

      @classmethod
      def setup_report(model,rpt):

.. modmeth:: summary_row

  Return a HTML fragment that describes this record in a summary
  
  Example::
  
    def summary_row(self,ui,rr,**kw):
        s = ui.href_to(self)
        if settings.LINO.projects_model:
            if self.project and not reports.has_fk(rr,'project'):
                s += " (" + ui.href_to(self.project) + ")"
        return s
  


.. modmeth:: update_owned_task

  Example::
  
    def update_owned_task(self,task):
        task.person = self


