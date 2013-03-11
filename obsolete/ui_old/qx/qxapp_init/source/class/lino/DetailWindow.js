/* ************************************************************************

#asset(lino/*)

************************************************************************ */

qx.Class.define("lino.DetailWindow",
{
  extend : lino.AppWindow,
  //~ construct : function(app, caption) {
  construct : function(app) {
      //~ console.log('lino.TableWindow.construct()',this,app);
      this.base(arguments);
      //~ this.base(arguments, caption);
      //~ console.log('lino.TableWindow.construct.base ok');
      //~ var tm = this.createTableModel();
      //~ this.__table = new qx.ui.table.Table(tm);
      this.__main = this.createMain();
      
      var toolbar = new qx.ui.toolbar.ToolBar();
      var part = new qx.ui.toolbar.Part();
      toolbar.add(part);
      var reload = new qx.ui.toolbar.Button('Reload');
      reload.addListener('execute',function(){
        console.log("Reload not yet implemented");
      }, this);
      part.add(reload);
      this.setupToolbar(part);
      
      this.set({
        width: 600,
        height: 400,
        contentPadding : [ 0, 0, 0, 0 ],
        //~ allowClose: true
        showClose: true
        //~ showMinimize: false
      });
      this.setLayout(new qx.ui.layout.VBox());
      this.add(toolbar);
      this.add(this.__main, {flex: 1});
      
  },
          
  members : {
      __table : null,
      createMain : function() {
        throw new Error("createMain is abstract");
      },
      setupToolbar: function(bar) { 
      }
  },
  events : {
    //~ "reload" : "qx.event.type.Event",
    //~ "post"   : "qx.event.type.Data"
  }
  
});