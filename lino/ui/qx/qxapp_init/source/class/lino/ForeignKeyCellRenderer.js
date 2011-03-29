/* ************************************************************************

************************************************************************ */

/**
 * The string data cell renderer. All it does is escape the incoming String
 * values.
 */
qx.Class.define("lino.ForeignKeyCellRenderer",
{
  extend : qx.ui.table.cellrenderer.String,

  /*
  *****************************************************************************
     MEMBERS
  *****************************************************************************
  */
  
  construct : function(colIndex)
  {
    this.base(arguments);
    this.__colIndex = colIndex;
  },
  

  members :
  {
    __colIndex : null,
    // overridden
    _getContentHtml : function(cellInfo) {
        this.debug('ForeignKeyCellRenderer',cellInfo);
        //~ console.log('ForeignKeyCellRenderer',cellInfo);
        if (cellInfo.rowData) {
            //~ console.log('ForeignKeyCellRenderer',cellInfo,'->',cellInfo.rowData[this.__colIndex]);
            var s = cellInfo.rowData[this.__colIndex];
            if (s) return qx.bom.String.escape(s);
            //~ return qx.bom.String.escape(s);
        }
        //~ console.log('ForeignKeyCellRenderer empty: ',cellInfo.rowData);
        return "";
    }
  }
});
