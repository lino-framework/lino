Lino.UppercaseTextField = Ext.extend(Ext.form.TextField,{
  style: 'text-transform:uppercase;',
  listeners:{
    change: function(field, newValue, oldValue){
      console.log("20140403 UppercaseTextField",newValue, newValue.toUpperCase());
      field.setRawValue(newValue.toUpperCase());
    }
  }
});

