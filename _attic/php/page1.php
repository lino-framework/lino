<?php
session_start();
if (isset($HTTP_SESSION_VARS['count'])) {
   $HTTP_SESSION_VARS['count']++;
   echo 'count:' . $HTTP_SESSION_VARS['count'];
} else {
   $HTTP_SESSION_VARS['count'] = 1;
   echo "(first time you called this page)";
}
?>
<HTML>
<BODY>
<br>count = <?= $HTTP_SESSION_VARS['count']?>
<br>session_save_path() = <?= session_save_path();?>
</body>
</html>


Apache/1.3.20 (Win32) PHP/4.1.3-dev running...


