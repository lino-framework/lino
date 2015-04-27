<?php
	error_reporting(E_ALL&~E_NOTICE);
	include('db.php');
	
	/**
	 * Gets Atricals from the com_extensiondemo_content table by filtering them accroding to $filter option
	 *
	 * @param $filter  as array ('name'=>"John", "name_filterOption"=>'startwith', 'email'=>'@yahoo.com', "email_filterOption"=>'endwith')
	 *
	 * @access public
	 * @return records found
	 */
	function filteredMembers( $filter ="" ){
		$where 	= " WHERE ";
		$where .= buildFilterCondition($filter);				
		
		$sql = "SELECT *, DATE_FORMAT(created, '%b %e, %Y') as created_date FROM com_extensiondemo_content  ".$where;
		if( $offset > 0 ){
			$sql .= " LIMIT ".intval($start).",".intval($offset);
		}
        		
		$return  = loadObjectlist($sql);
		return  $return;
	}
	
	/**
	 * build the filter condition for query
	 *
	 * @param $filter  as array ('name'=>"John", "name_filterOption"=>'startwith', 'email'=>'@yahoo.com', "email_filterOption"=>'endwith')
	 *
	 * @access public
	 * @return filter as string 
	 */
	function buildFilterCondition($filter){
		$where	= ' 1=1 ';
		if( $filter && is_array($filter) && count($filter) ){
			foreach($filter as $fieldIndex=>$val){
				if( substr($fieldIndex, -12 ) == 'filterOption' ){
					$fieldName 	= str_replace('_filterOption', '', $fieldIndex);
					$fieldValue = $filter[$fieldName];
					if($fieldValue===''){
						continue;
					}
					
					switch($val){
						case 'startwith':
							$where .= " AND {$fieldName} like '{$fieldValue}%' ";
						break;
						case 'endwith':
							$where .= " AND {$fieldName} like '%{$fieldValue}' ";
						break;
						case 'doesnotcontain':
							$where .= " AND {$fieldName} NOT like '%{$fieldValue}%' ";
						break;
						case 'equal':
							$where .= " AND {$fieldName} = '{$fieldValue}' ";
						break;
						case 'notequal':
							$where .= " AND {$fieldName} <> '{$fieldValue}' ";
						break;
						case 'before':
							$where .= " AND {$fieldName} < '{$fieldValue}' ";
						break;
						case 'after':
							$where .= " AND {$fieldName} > '{$fieldValue}' ";
						break;
						case 'NoFilter':
						break;
						default:
						case 'contain':
							$where .= " AND {$fieldName} like '%{$fieldValue}%' ";
						break;
					}
				}
			} 
		}		
		return $where;
	}
	
	
	$filter				= $_REQUEST['filter'];
	$rows				= filteredMembers($filter);
	$result 			= new stdClass();
	$result->data		= $rows;
	$result->total		= count($rows);
	$result->success	= true;
	echo $json 			=  json_encode($result);	

?>