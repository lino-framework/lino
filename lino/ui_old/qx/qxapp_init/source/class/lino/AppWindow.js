/* ************************************************************************

#asset(lino/*)

************************************************************************ */

qx.Class.define("lino.AppWindow",
{
  extend : qx.ui.window.Window,
  //~ construct : function(app, caption) {
  construct : function(app) {
      //~ console.log('lino.TableWindow.construct()',this,app);
      this.base(arguments);
      //~ this.base(arguments, caption);
      //~ console.log('lino.TableWindow.construct.base ok');
      this.__app = app;
  },
          
  members : {
      __app : null,
      showWindow : function(win) { 
        this.__app.showWindow(win); 
      }
  },
  events : {
    //~ "reload" : "qx.event.type.Event",
    //~ "post"   : "qx.event.type.Data"
  }
  
});