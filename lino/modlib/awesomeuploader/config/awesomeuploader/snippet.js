/* */

Lino.AwesomeUploaderPanel = Ext.extend(AwesomeUploader,Lino.MainPanel);
Lino.AwesomeUploaderPanel = Ext.extend(
    Lino.AwesomeUploaderPanel, Lino.PanelMixin);

Lino.unused_AwesomeUploaderPanel = Ext.extend(Lino.AwesomeUploaderPanel, {
  app_instance : null
  ,layout: 'fit'
  ,empty_title : "{{site.modules.awesomeuploader.UploaderPanel.label}}"
  ,ls_url: '/awesomeuploader/UploaderPanel'
  ,set_status : function(status,rp) { 
      // console.log('20140402 CalendarAppPanel.set_status()', status);
      this.requesting_panel = Ext.getCmp(rp);
      this.clear_base_params();
      if (status == undefined) status = {};
      //~ if (status.param_values) 
      //~ this.set_field_values(status.field_values);
      if (status.base_params) this.set_base_params(status.base_params);
      this.refresh();
      }
  ,get_base_params : function() {
    // console.log('20140402 getbase_params has', this.base_params);
    var p = Ext.apply({}, this.base_params);
    Lino.insert_subst_user(p);
    // console.log('20140402 getbase_params returns', p);
    return p;
  }
  ,set_base_params : function(p) {
    this.base_params = Ext.apply(this.app_instance.event_store.baseParams,p);
    this.app_instance.event_store.baseParams = this.base_params;
    // console.log('20140402 this.base_params is', this.base_params);
  }
  ,clear_base_params : function() {
      this.base_params = {};
      Lino.insert_subst_user(this.base_params);
  }
  ,set_base_param : function(k,v) {
      if (!this.base_params) this.base_params = {};
      this.base_params[k] = v;
  }
});



Lino.AwesomeUploader = function() {

    return new Lino.AwesomeUploaderPanel({
		title:'Awesome Uploader for Lino'
		,frame:true
		,width:500
		,height:300
		,awesomeUploaderRoot:'/media/awesomeuploader/'
	});
};
