<?php
include('html.inc.php');
$url = $HTTP_GET_VARS['file'];

// $dir = dirname($url);

//  if ($dir && $legal_dir) {
//      $page_name = $DOCUMENT_ROOT . $url;
//  } else {
//      $page_name = basename($url);
//  }

$page_name = basename($url);

echo "<!-- ", htmlentities($page_name), " -->\n";

BeginSection('Source: ' . $page_name);

if (substr($page_name,strlen($page_name)-4) != '.php') {
  echo 'refused';
} else // if (file_exists($page_name) && !is_dir($page_name)) {
    show_source($page_name);
//  } else if (@is_dir($page_name)) {
//      echo "<p>No file specified.  Can't show source for a directory.</p>\n";
//  }
//  else {
//      echo "<p>This file does not exist.</p>\n";
//  }

// show_source($file);

EndSection();
// ShowFooter();
?>
