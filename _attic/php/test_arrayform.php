<HTML>
<HEAD>
<TITLE>array form</TITLE>
<script language="JavaScript">

<!--
function submit() {

  alert(document.test.fieldname[0]);
  var max = document.test.length-1;
  var retval = true;
  alert("checking..."+max+" inputs.");

  for (i = 0; i < max; i++) {
    //alert(i+","+document.forms[0][i].value);
    if (document.forms[0][i].value == '') {
      //alert(i+" is empty");
      document.all["l"+i].style.border = "1px #FF0000 solid";
      retval = false;
    } else {
       //alert(i+" is not empty");
       document.all["l"+i].style.border = "1px #00FF00 solid";
    }
  }

  if( retval == false ) {
     alert("Missing Required fields. Missing fields are highlighted in red.");
  } else {
     alert("All fields correctly filled out.");
     document.forms[0].submit();         // form is correctly filled out
  }
  return retval;
}

function warn() {
  if (document.sub.name.value == '') {
     document.all["light"].style.border 
      = "5px #FF0000 solid";
  }
}
//-->
</script>
</HEAD>

<BODY>

GET will submit by
http://localhost/phptest/lino/debug.php?fieldname%5B%5D=a&coltype%5B%5D=b&fieldname%5B%5D=c&coltype%5B%5D=d&fieldname%5B%5D=e&coltype%5B%5D=f


<form name="test" action="debug.php" method="GET">
<table>
<tr>
<td>0
<td><input type="text" name="fieldname[]" value="a">
<td><input type="text" name="coltype[]" value="b">
</tr>
<tr>
<td>1
<td><input type="text" name="fieldname[]" value="c">
<td><input type="text" name="coltype[]" value="d">
</tr>
<tr>
<td>2
<td><input type="text" name="fieldname[]" value="e">
<td><input type="text" name="coltype[]" value="f">
</tr>
</table>

<input type="button" value="Submit" onClick="submit()">
</form>
</body>
</html>
