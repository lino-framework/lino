/* ************************************************************************

  initially copied from demobrowser.demo.table.RemoteTableModel


************************************************************************ */
/* ************************************************************************

#asset(lino/*)

************************************************************************ */

qx.Class.define('lino.RemoteTableModel', {

  extend : qx.ui.table.model.Remote,

  construct : function(window,url,columnIds) {
    this.base(arguments);
    this.__url = url;
    this.__window = window;
    this.setColumnIds(columnIds); 
  },

  members : {
    __url : null,
    __window : null,

    // overloaded - called whenever the table requests the row count
    _loadRowCount : function()
    {
      var url = this.__url + "?fmt=json&offset=0&limit=0";
      this.__call(url, function(e) {
        var response = e.getContent();
        if (response) {
          //~ console.log('loadRowCount got',response.count, 
            //~ ', this is',this,
            //~ ', this._onRowCountLoaded is',this._onRowCountLoaded);
          //~ this._onRowCountLoaded(parseInt(data));
          this._onRowCountLoaded(response.count);
          this.__window.setCaption(response.title);
        } 
        //~ else {console.log('loadRowCount got null response')}
      });
    },


    _loadRowData : function(firstRow, lastRow)
    {
      var url = this.__url + "?fmt=json&offset="+firstRow+"&limit="+(lastRow-firstRow);
      this.__call(url, function(e) {
        var response = e.getContent();
        this.debug('lino.RemoteTableModel._loadRowData() got',response);
        //~ console.log('lino.RemoteTableModel._loadRowData() got',response);
        //~ this._onRowCountLoaded(parseInt(data));
        this._onRowDataLoaded(response.rows)
      });
    },
    
    
    __call : function(url, callback) {
      //~ console.log('lino.RemoteTableModel.__call',url);
      var req = new qx.io.remote.Request(url, "GET", "application/json");
      // Function.createDelegate()
      //~ req.addListener("completed", function(e) { callback(e.getContent()); }, this);
      req.addListener("completed", callback, this);
      req.send();
    }

  }
});
