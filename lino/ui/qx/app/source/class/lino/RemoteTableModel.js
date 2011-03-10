/* ************************************************************************

  initially copied from demobrowser.demo.table.RemoteTableModel


************************************************************************ */
/* ************************************************************************

#asset(lino/*)

************************************************************************ */

qx.Class.define('lino.RemoteTableModel', {

  extend : qx.ui.table.model.Remote,

  //~ construct : function(url,columns) {
  construct : function(url) {
    //~ columns = [ [name,header,sortable,editable] ]
    this.base();
    this.__url = url;
    //~ this.__columns = columns;
    //~ var headers = [], names = [];
    //~ for (var i = 0; i < columns.length; i++) {
       //~ names.push(columns[i][0]);
       //~ headers.push(columns[i][1]);
    //~ }
    //~ this.setColumns(headers,names);
  },

  members : {
    //~ __columns : null,
    __url : null,

     // overloaded - called whenever the table requests the row count
    _loadRowCount : function()
    {
      var url = this.__url + "?fmt=json&offset=0&limit=0";
      //~ var url = this.__url + "?fmt=count";
      this.__call(url, function(response) {
        console.log('got',response);
        //~ this._onRowCountLoaded(parseInt(data));
        this._onRowCountLoaded(response.count);
      });
    },


    _loadRowData : function(firstRow, lastRow)
    {
      var url = this.__url + "?fmt=json&offset="+firstRow+"&limit="+(lastRow-firstRow);
      this.__call(url, function(response) {
        console.log('got',response);
        //~ this._onRowCountLoaded(parseInt(data));
        this._onRowDataLoaded(response.rows)
      });
    },
    
    
    __call : function(url, callback) {
      var req = new qx.io.remote.Request(url, "GET", "application/json");
      req.addListener("completed", function(e) { callback(e.getContent()); }, this);
      req.send();
    }


    // Fake the server localy
    
    //~ __rowDataLoadded : function(firstRow, lastRow) {
      //~ var self = this;
      //~ window.setTimeout(function() {
        //~ var data = [];
        //~ for (var i=firstRow;i<=lastRow;i++){
          //~ data.push({id:i,text:'Hello '+i+' Generated on:'+(new Date())});
        //~ }
        //~ self._onRowDataLoaded(data);
      //~ }, 0);
    //~ }
  }
});
