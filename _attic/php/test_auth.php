<?php
/*
  http://hotwired.lycos.com/webmonkey/00/05/index2a_page2.html?tw=programming */

// File Name: auth01.php
// Check to see if $PHP_AUTH_USER already contains info

if (!isset($_SERVER['PHP_AUTH_USER'])) {
  
  // If empty, send header causing dialog box to appear
  header('WWW-Authenticate: Basic realm="My Private Stuff"');
  header('HTTP/1.0 401 Unauthorized');
  echo 'Authorization Required.';
  exit;
}

// If not empty, display values for variables

else {
  
  echo "<P>You have entered this username: {$_SERVER['PHP_AUTH_USER']}<br>
       You have entered this password: {$_SERVER['PHP_AUTH_PW']}<br>
       The authorization type is: {$_SERVER['PHP_AUTH_TYPE']}</p>
		";
  
}

?>
