<?php

	include('../../../../../../../../../configuration.php');
	
	$Config	= new JConfig();
	/*************
	*mysql database configuration
	*******************************************/
	$host		=	$Config->host;//mysql database hostname
	$username	=	$Config->user;//mysql database username
	$password	=	$Config->password;//mysql database password
	$database	=   $Config->db;//mysql database name
	
	/**********
	*Connect the mysql database
	********************/
	function connectDatabase($host, $username, $password, $database){
		$link = mysql_connect($host, $username, $password);
		mysql_select_db($database, $link);
	}
	
	/*****
	*Return the mysql table records as object array
	***************/
	function loadObjectlist($query){
		$rows	= array();
		$result = mysql_query($query);
		if($result){
			while( $row = mysql_fetch_object($result) ){
				$rows[] = $row;
			}
		}
		return $rows;
	}
	//connect the databse
	connectDatabase($host, $username, $password, $database);
?>