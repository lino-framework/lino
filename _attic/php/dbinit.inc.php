<?php

include('lino.inc.php');

BeginSection("Initialize Database");

if (isset($HTTP_GET_VARS['ok'])) {
  if ($HTTP_GET_VARS['ok'] == 'yes' ) {
    foreach($HTTP_SESSION_VARS['app']->tables as $table) {
      $table->dbd->sql_create_table($table);
    }
    include('lino.init.php');
    echo ('Database has been initialized.');
  }
} else {

  echo ( '<p>Initialize the database?');
  echo ( '[<a href="dbinit.php?ok=yes">yes</a>]');
  echo ( '[<a href="dbinit.php?ok=no">no</a>]');
  echo ( '[<a href="index.php">cancel</a>]');
}

EndSection();
?>
