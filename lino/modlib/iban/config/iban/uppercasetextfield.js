Lino.UppercaseTextField = Ext.extend(Ext.form.TextField,{
  style: 'text-transform:uppercase;',
  listeners:{
    change: function(field, newValue, oldValue){
      // console.log("20140403 UppercaseTextField",newValue, newValue.toUpperCase());
      field.setRawValue(newValue.toUpperCase());
    }
  }
});


Lino.iban_renderer = function(
    value, metaData, record, rowIndex, colIndex, store) 
{
    var reg = new RegExp(".{4}", "g");
    if(value) {
        return value.replace(reg, function (a) { return a + ' '; });
    }
    return value;
}



