<?php
class Foo {
  var $fo;
  var $fi;
  function Foo() {
    $this->fo = 'foo';
    $this->fi = 'bar';
  }

  function Show() {
    echo 'Foo';
  }
}

session_start();
// setcookie(session_name(),"",0,"/");
?>
<html>
<body>

<ul>
<li>Session ID = <?=session_id();?></li>
<li>

<?php
// $HTTP_SESSION_VARS = array();
if (isset($HTTP_SESSION_VARS['count'])) {
  echo 'count = ' . $HTTP_SESSION_VARS['count'];
  $HTTP_SESSION_VARS['count'] = $HTTP_SESSION_VARS['count'] + 1;
  echo '<li>';
  print_r($HTTP_SESSION_VARS['foo']);
  $HTTP_SESSION_VARS['foo']->Show();
} else {
  $HTTP_SESSION_VARS['count'] = 1;
  $HTTP_SESSION_VARS['foo'] = new Foo();
  echo 'First time';
}
?>
</li>
</ul>
</body>
</html>
