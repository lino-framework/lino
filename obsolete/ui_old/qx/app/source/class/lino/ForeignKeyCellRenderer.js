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
        //~ console.log('ForeignKeyCellRenderer',cellInfo);
        if (cellInfo.rowData) {
            return qx.bom.String.escape(cellInfo.rowData[this.__colIndex]);
        }
        return "";
    }
  }
});
