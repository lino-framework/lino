<HTML>
<HEAD>
<TITLE><?=$GLOBALS['pageTitle']?></TITLE>
<link rel=stylesheet type="text/css" href="www.css">
<meta http-equiv="Content-Type"
      content="text/html; charset=ISO-8859-1">
<script language="JavaScript">
<!--
function check() {
  alert(document.forms[0].fieldname[0]);
  document.forms[0].submit();
}
//-->
</script>
</HEAD>
<BODY>
<TABLE class="main" WIDTH="100%">

<tr>

<td class="left" width="20%" valign="top">

<?php

global $showJoinFields;

//  if (isset($HTTP_GET_VARS['debug'])) {
//    $debug = $HTTP_GET_VARS['debug'];
//  }

//  if (isset($HTTP_SESSION_VARS['query'])) {
//    // $query = $HTTP_SESSION_VARS['query'];
//    // if (isset($query->caller)) {
//    echo '<a href="close.php">';
//    echo '<img src="images/close.jpg" alt="Close" border=0>';
//    echo '</a>';
//    // }
//    echo '<a href="this.php">';
//    echo '<img src="images/refresh.jpg" alt="Refresh" border=0>';
//    echo '</a>';

//    if ($showJoinFields) {
//      $HTTP_SESSION_VARS['query']->ShowInspectorRef();
//    }
//  }
?>


<br><a href="index.php">Home</a>
<br><a href="index.php?meth=reset">Restart</a>
<br><a href="status.php">Status</a>
<br><a href="tests.php">Tests</a>
<hr>

<?php

global $HTTP_SERVER_VARS;

$self = $HTTP_SERVER_VARS['SCRIPT_NAME'];

echo '<br><a href="source.php?file=' . $self . '">'
.'show source</a>';


global $verbose;
echo '<br>$verbose : ';


if($verbose == 0) {
  echo ' 0 ';
} else {
  // echo ' <a href="'.$HTTP_SERVER_VARS['PHP_SELF'].'?verbose=0"';
  echo ' <a href="'.$self.'?verbose=0"';
  echo 'title="show messages only in View Log page">0</a>';
}

if($verbose == 1) {
  echo ' 1 ';
} else {
  echo ' <a href="'.$self.'?verbose=1"';
  echo 'title="show a link to message inside page body">1</a>';
}

if($verbose == 2) {
  echo ' 3 ';
} else {
  echo ' <a href="'.$self.'?verbose=2"';
  echo 'title="write full message into page body">2</a>';
}

global $debug;
echo '<br>$debug : ';

if($debug == 0) {
  echo ' 0 ';
} else {
  echo ' <a href="'.$self.'?debug=0"';
  echo 'title="ignore debug messages">0</a>';
}

if($debug == 1) {
  echo ' 1 ';
} else {
  echo ' <a href="'.$self.'?debug=1"';
  // echo ' <a href="this.php?debug=1"';
  echo 'title="log all debug messages">1</a>';
}


echo '<br>$showJoinFields : ';

if($showJoinFields == 0) {
  echo ' 0 ';
} else {
  echo ' <a href="this.php?showJoinFields=0"';
  echo 'title="dont show joined fields">0</a>';
}
if($showJoinFields == 1) {
  echo ' 1 ';
} else {
  echo ' <a href="this.php?showJoinFields=1"';
  echo 'title="show joined fields">1</a>';
}



//  echo $GLOBALS['PHP_AUTH_USER'];
//  echo $GLOBALS['PHP_AUTH_PW'];
//  echo $GLOBALS['PHP_AUTH_TYPE'];




//  $num = count($HTTP_SESSION_VARS['queries']);
//  if ($num > 0) {
//    echo 'Query Stack:';
//    foreach($HTTP_SESSION_VARS['queries'] as $q) {
//      $num--;
//      echo '<br><a href="close.php?num=' . $num
//        . '">'
//        . $q->GetLabel()
//        . '</a>';
//    }
//  }

echo '<hr>';
echo 'Client: ' . $HTTP_SERVER_VARS['REMOTE_ADDR']
      . ':' . $HTTP_SERVER_VARS['REMOTE_PORT'];
echo '<br>Server: ' . $HTTP_SERVER_VARS['SERVER_PORT'];
global $db;
echo '<br>Database: ' . $db;

// echo ':' . $_SERVER['HTTP_REFERER'];

?>
<hr>


<td width="80%" valign="top">

<?php
/**********************
<table class="navbar">
<tr>
<td>
<form name="searchForm" method=get action="search.php">
Search:
<input class="formtext" name="searchStr" type="text" size=8
style="width:150;" value="">
<select name="searchType">
  <option value=0 selected>Local</option>
  <option value=1>Google</option>
</select>
<input type="image" src="images/go.gif"
width=22 height=14 alt="Go" border="0">
</form>
</td>
<td>
<form name="jumpToForm" action="jumpTo.php" method=get>
<select
name="jumpTo"
onchange="if (this.options[this.selectedIndex].value)
window.location.href = this.options[this.selectedIndex].value;"
size=1>
<option disabled>--- Jump To ---
<option value="index">Front Page
<option value="show.php?query=PAR">Partners
</select>
<input type="image" src="images/go.gif" width=22 height=14
alt="Go" border="0">
</form>
</td>
</tr>
</table>
***************************/
?>
