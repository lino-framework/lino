<?php
/**
 ** Server-specific module list
 **
 ** Includes all modules which are available on this server.
 **
 ** Note that modules become active for a specific application only if
 ** they are declared in appinit.inc.php
 **
 ** This file is necessary because Lino must know all possible classes
 ** before doing session_start()
 **
 **/
include('mysql.inc.php');

include('sys.inc.php'); 
include('crm.inc.php'); 
include('community.inc.php'); 
include('sdk.inc.php'); 
include('docbook.inc.php'); 
include('quotes.inc.php'); 
//include('addrbook.php');
//include('agenda.php');



?>
