/* ************************************************************************

   Copyright:

   License:

   Authors:

************************************************************************ */

/* ************************************************************************

#asset(lino/*)

************************************************************************ */

/**
 * This is the main application class of your custom application "lino"
 */
qx.Class.define("lino.CountriesCitiesTable",
{
  extend : lino.TableWindow,
  //~ construct : function() {
    //~ console.log('lino.CountriesCitiesTable.construct()',arguments);
    //~ this.base(arguments);
  //~ },

  members : {
    caption : 'Städte',
    content_type : 9,
    before_row_edit : function(record){}, 
    createTableModel : function() {
      var tm = new lino.RemoteTableModel('/countries/Cities');
      tm.setColumns(
        ["country",'name','zip_code','id'],
        ["Land",'Name','PLZ','ID']
      ); // columnNameArr, columnIdArr
      tm.setColumnSortable(0,true);
      tm.setColumnEditable(0,true);
      // todo:
      // filter ? 
      // width ?
      // renderer
      // editor
      // hidden
      // lino.CountriesCitiesInsert
    },
    setupToolbar: function(bar)
    {
      var btn = new qx.ui.toolbar.Button('Detail');
      btn.addListener('execute',function(){
        //~ this.showWindow(lino.CountriesCitiesDetail);
        alert("TODO : how to referencethe app? want to open new window...");
      }, this);
      bar.add(btn);
    //~ "ls_bbar_actions": [ 
      //~ { "text": "Detail", "panel_btn_handler": Lino.show_detail_handler }, 
      //~ { "text": "Einf\u00fcgen", "must_save": true, "panel_btn_handler": function(panel){Lino.show_insert(panel)} }, 
      //~ { "text": "L\u00f6schen", "panel_btn_handler": Lino.delete_selected } 
    //~ ], 

    }
  }
});