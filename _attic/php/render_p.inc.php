<?php
include('lino.inc.php');

if (!isset($HTTP_SESSION_VARS['renderedQuery'])) {
  trigger_error('your session data is invalid');
}

$query =& $HTTP_SESSION_VARS['renderedQuery'];

foreach($HTTP_POST_VARS as $key => $value) {
  switch ($key) {
  case 'qfilter':
    $query->qfilter = $value;
    break;
  default:
  }
}

$query->Render();

?>
