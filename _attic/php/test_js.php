<SCRIPT LANGUAGE="JavaScript">
 <!--
 var supported = (window.Option) ? 1 : 0;

 if (supported) {
   var active;

var ar = new Array();

ar[0] = new Array();
ar[0][0] = new makeOption("Crown,  Tom", "151");
ar[0][1] = new makeOption("Christiansen,  Steve", "221");
ar[0][2] = new makeOption("Berman,  Randal", "321");
ar[0][3] = new makeOption("Turok,  Steve", "341");
ar[0][4] = new makeOption("Cider,  Eric", "361");
ar[0][5] = new makeOption("Bolton,  Liz", "421");
ar[1] = new Array();
ar[1][0] = new makeOption("Crown,  Tom", "152");
ar[1][1] = new makeOption("Christiansen,  Steve", "222");
ar[1][2] = new makeOption("Berman,  Randal", "322");
ar[1][3] = new makeOption("Turok,  Steve", "342");
ar[1][4] = new makeOption("Cider,  Eric", "362");
ar[1][5] = new makeOption("Bolton,  Liz", "422");
ar[1][6] = new makeOption("Tuti,  Berna", "432");
ar[1][7] = new makeOption("Dong,  Enormai ", "442");
ar[2] = new Array();
ar[2][0] = new makeOption("Lindberg,  John", "273");
ar[2][1] = new makeOption("Tuti,  Berna ", "433");
ar[2][2] = new makeOption("Dong,  Enormai", "443");
ar[3] = new Array();
ar[3][0] = new makeOption("Tuti,  Berna ", "434");
ar[4] = new Array();
ar[4][0] = new makeOption("Narsysus,  Thelma", "306");
ar[5] = new Array();
ar[5][0] = new makeOption("Turok,  Steve ", "347");
ar[5][1] = new makeOption("Bolton,  Liz ", "427");

}



function makeOption(text, url) {
   this.text = text;
   this.url = url;
}

 function relate(form) {
   if (!supported) {
     load(form, "industry");
     return;
   }
   var options = form.industry_focus.options;
   for (var i = options.length - 1; i > 0; i--) {
     options[i] = null;
   }
   var curAr = ar[form.industry.selectedIndex];
   for (var j = 0; j < curAr.length; j++) {
     options[j] = new Option(curAr[j].text, curAr[j].url);
   }
   options[0].selected = true;
 }

// The function selectAll and store are for passing multiple select values to a form
// processing script, which will be the focus of an upcoming article.

function selectAll() {
        for (i = 0; i <= document.menu.list2.length; i++){  
        if (document.menu.list2.options[i] != -1){
                        document.menu.list2.options[i].selected = true; 
                validForm = 1;               
                }
        }
}

function store() { 
         allValues=""; 
         allSkills="";
        for(var i=0;i<document.menu.list2.length;i++) { 
        if(document.menu.list2.options[i].selected && document.menu.list2.options[i].value != 0) { 
                user = document.menu.list2.options[i].value.substring(0,2)
                        skill = document.menu.list2.options[i].value.substring(2,3)
                        allValues+=user+","; 
                        allSkills+=skill+",";
        } 
    }
document.menu.hdn.value=allValues; 
document.menu.skill.value=allSkills;
}

 // -->

</SCRIPT>

<SCRIPT LANGUAGE="JavaScript">

<!-- Begin

sortitems = 1;  // Automatically sort items within lists? (1 or 0)

function move(fbox,tbox) {
for(var i=0; i<fbox.options.length; i++) {
if(fbox.options[i].selected && fbox.options[i].value != "") {
var no = new Option();
no.value = fbox.options[i].value;
no.text = fbox.options[i].text;
tbox.options[tbox.options.length] = no;
fbox.options[i].value = "";
fbox.options[i].text = "";
   }
}

BumpUp(fbox);
if (sortitems) SortD(tbox);
}

function BumpUp(box)  {
for(var i=0; i<box.options.length; i++) {
if(box.options[i].value == "")  {
for(var j=i; j<box.options.length-1; j++)  {
box.options[j].value = box.options[j+1].value;
box.options[j].text = box.options[j+1].text;
}
var ln = i;
break;
   }

}

if(ln < box.options.length)  {
box.options.length -= 1;
BumpUp(box);
   }
}



function SortD(box)  {
var temp_opts = new Array();
var temp = new Object();
for(var i=0; i<box.options.length; i++)  {
temp_opts[i] = box.options[i];
}

for(var x=0; x<temp_opts.length-1; x++)  {
for(var y=(x+1); y<temp_opts.length; y++)  {
if(temp_opts[x].text > temp_opts[y].text)  {
temp = temp_opts[x].text;
temp_opts[x].text = temp_opts[y].text;
temp_opts[y].text = temp;
      }
   }
}

for(var i=0; i<box.options.length; i++)  {
box.options[i].value = temp_opts[i].value;
box.options[i].text = temp_opts[i].text;
   }
}

function clear() {
        
}
// End -->
</script>
<br>
We have all seen pages that use JavaScript for better or for worse.  In many cases JavaScript can improve a site's functionality and ease of use.  Unfortunately administrating some of the complicated arrays that JavaScript depends on for things like heirarchichal menus and dynamic forms can be a pain in the rear.  That's why were going to turn the task over to PHP and MySQL.  We can use this combination to load data into the JavaScript for us. This is particularly useful if information contained in the array is likely to change. 
<br><br>
In this exercise we will build a selection component for a resource management system.  The component will tie people and project together based on staffing needs and employee skill.  It will also illustrate how PHP and MySQL can be used to dynamically build JavaScript. The static component code is below. 
<br><br>

<form>
<table width=350>
        <tr><td colspan="3"><font size=-1>Use the drop down menu below to select the skills required for the project.  The list of personnel will change according to skill.  Use the arrows arrows to control the addition or subtraction or people to the project.</font></td></tr>
		<tr>

        <td>

        <SELECT NAME="industry" onChange="relate(this.form)">

        

        <option>HTML<option>JavaScript<option>Vignette<option>Cold Fusion<option>Oracle<option>MySQL 

        

        </SELECT>

        </td>

        </tr>

        <tr>

        <td>

        <select multiple size="5" NAME="industry_focus" onSubmit="load(this.form, 'industry_focus')">
<option value="151">Crown,  Tom
<option value="221">Christiansen,  Steve
<option value="321">Berman,  Randal
<option value="341">Turok,  Steve
<option value="361">Cider,  Eric
<option value="421">Bolton,  Liz
        </select></td>

        <td align="center">

        <input type="button" value="   >>   " onclick="move(this.form.industry_focus,this.form.list2)" name="B1"><br>

        <input type="button" value="   <<   " onclick="move(this.form.list2,this.form.industry_focus)" name="B2">

        </td>

        <td><select multiple size="5" name="list2">

        <option value="0">Project Personnel</option>

        </select></td>

        </tr>

        </table>


<input type="submit" name="submit" onclick="selectAll()">

</form>
