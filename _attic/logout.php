<?php
ob_start();  // hold back all eventual output during initialization
include('console.inc.php');
include('html.inc.php');
session_start();
setcookie(session_name(),"",0,"/");

// $con = $HTTP_SESSION_VARS['connection'];

session_destroy();
// mysql_close($con);

global $debug,$verbose;

$savedebug = $debug;
$saveverbose = $verbose;
$save = $verbose;

$HTTP_SESSION_VARS = array();

init_option('debug',$savedebug);
init_option('verbose',$saveverbose);
init_option('showJoinFields',FALSE);

ob_end_clean();
RedirectTo('index.php'); // LocationIndex();

?>

