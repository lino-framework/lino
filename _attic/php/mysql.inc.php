<?php

class UpdateStmt {
  var $colName;
  var $colType;
  var $newValue;
  function UpdateStmt($colName,$colType,$newValue) {
    $this->colName = $colName;
    $this->colType = $colType;
    $this->newValue = $newValue;
  }
}

class MySQLDriver {

  function sql_select($sql) {
    $result = mysql_query($sql) 
      or trigger_error('sql_select: ' . $sql
                       . ':' . mysql_error()
                       . ' (' . mysql_errno() . ')',
                       E_USER_ERROR);
    ToDebug($sql . ' (' . mysql_num_rows($result) . ' rows)');
    return $result;
  }

  function sql_exec($sql) {
    $result = mysql_query($sql) 
      or trigger_error('sql_exec: ' . $sql
                       . ':' . mysql_error()
                       . ' (' . mysql_errno() . ')',
                       E_USER_ERROR);
    return $result;
  }

  function sql_peek($tables,$where,$columns='*') {
    $sql = "select $columns from $tables WHERE $where";
    $result = $this->sql_select($sql);
    if ( mysql_num_rows($result)!=1 )
      return NULL;
    //      trigger_error($sql.' returned '
    //                    .mysql_num_rows($result).' rows',
    //                    E_USER_ERROR);
    return mysql_fetch_array($result,MYSQL_ASSOC);
  }


  function sql_update($tableName,$where,$newValues) {
    $sql = 'UPDATE '. $tableName . ' sET ';
    $sep = '';
    foreach($newValues as $col => $value) {
      $sql .= $sep . $col . ' = ' . $value;
      $sep = ',';
    }
    
    if (mysql_query($sql))
      return TRUE;
    ToUserLog('sql_update: ' . $sql
              . ':' . mysql_error()
              . ' (' . mysql_errno() . ')');
    return FALSE;
  }


  function sql_create_table($table) {
    // $table =& Table::GetInstance($tableName);
    $sql = "DROP TABLE IF EXISTS " . $table->name;
    $this->sql_exec($sql);
    $sql = 'CREATE TABLE ' . $table->name . " (";
    $sep = '';
    foreach($table->fields as $name => $field) {
      //echo '<br>is ' . $name . ' in ';
      //print_r($table->GetPrimaryKey());
      //echo '?';
      $isPrimary = in_array( $name,
                             $table->GetPrimaryKey());
      $sql .= $sep . $name . ' '
        . $this->sql_typespec($field,$isPrimary);
      //      if ($isPrimary && count($table->GetPrimaryKey()) == 1)
      //        $sql .= ' PRIMARY KEY';
      $sep = ',';
    }
    // if ( count($table->GetPrimaryKey()) > 1) {
    $sql .= ', PRIMARY KEY (';
    $sep = '';
    foreach($table->GetPrimaryKey() as $i => $pk) {
      $sql .= $sep . $pk;
      $sep = ',';
    }
    $sql .= ")";
    foreach($table->indexes as $ndx) {
      $sql .= ', ' . $ndx;
    }
    // }
    $sql .= ')';
    $this->sql_exec($sql);

  }

  function sql_typespec($field,$isPrimary) {
    switch(get_class($field->type)) {
    case 'inttype':
      $s = 'BIGINT';
      if ($isPrimary) $s .= ' NOT NULL';
      return $s;
    case 'autoinctype':
      $s = 'BIGINT';
      if (! is_a($field,'joinfield'))
        $s .= ' AUTO_INCREMENT';
      if ($isPrimary) $s .= ' NOT NULL';
      return $s;
    case 'booltype':
      $s = 'INT';
      if ($isPrimary) $s .= ' NOT NULL';
      return $s;
    case 'datetype':
      $s = 'DATE';
      if ($isPrimary) $s .= ' NOT NULL';
      return $s;
    case 'texttype':
      if ($isPrimary)
        return 'CHAR('.$field->format[0].') NOT NULL';
      return 'VARCHAR('.$field->format[0].')';
    case 'memotype':
      $s = 'TEXT';
      if ($isPrimary)
        trigger_error('MemoType not allowed for primary key');
      return $s;
    }
  }


  function sql_commit_row($table,$row) {
    if ($row['_new']) {
      $sql = 'INSERT INTO '
        . $table->name
        . '(';
      $sep = '';
      foreach($table->fields as $name => $field) {
        $sql .= $sep . $name; // $col->GetSqlName();
        $sep = ', ';
      }
      $sql .=  ')'
        . ' VALUES (';
    } else {
      $sql = 'UPDATE ' . $table->name . ' SET ';
    }
    $sep = '';
    foreach($table->fields as $name => $field) {
      $type = $field->GetType();
      $value = $row[$name];
      if ($row['_new']) {
        $sql .= $sep . $type->to_sql($value);
      } else {
        $sql .= $sep . $name 
          . ' = '
          . $type->to_sql($value);
      }
      $sep = ', ';
    }
    if ($row['_new']) {
      $sql .= ')';
    } else {
      $sql .= ' WHERE ';
      $sep = '';
      foreach($table->GetPrimaryKey() as $pk) {
        $type = $table->fields[$pk]->GetType();
        $sql .= $sep . $pk . ' = '
          . $type->to_sql($row[$pk]);
        $sep = ' AND ';
      }
    }
    $this->sql_exec($sql);
  }

  /*
    Query.GetSqlSelect()
   */
  function GetSqlSelect($query) {

    $s = 'SELECT ';
    $sep = '';
    foreach($query->leader->fields as $field) {
      $s .= $sep . $query->leader->name . '.' . $field->name;
      $sep = ',';
    }
    foreach($query->leader->joins as $join) {
      foreach($join->toTable->fields as $field) {
        $s .= $sep . $join->alias . '.' . $field->name
          . ' AS ' . $join->alias . '_' . $field->name;
        $sep = ',';
      }
    }

    $s .= ' FROM ' . $query->leader->name;
    $sep = ',';
    foreach ($query->leader->joins as $join) {
      $s .= ' LEFT JOIN '
        . $join->toTable->name;
      // if ($join->alias != $join->toTable->name) {
      $s .= ' AS ' . $join->alias;
      // }
      $rpk = $join->toTable->GetPrimaryKey();
      $s .= ' ON (';
      // $i = 0;
      $sep = '';
      foreach($join->fields as $i => $field) {
        $s .= $sep
          . $query->leader->name . '.' . $field->name
          . ' = '
          . $join->alias . '.' . $rpk[$i];
        // $i++;
        $sep = ' AND ';
      }    
      $s .= ')';
    }

    $where = '';
    $sep = ' WHERE ';

    // $i = 0;
    foreach ($query->slices as $k => $v) {
      // $type = $k->GetType();
      $col = $query->view->columns[$k];
      $where = $where . $sep
        . $col->sql_where(
                          $query->leader->name . '.' . $k,
                          ' = ',
                          $v);
      // . $fld->type->to_sql($v) ;
      $sep = ' AND ';
      // $i++;
    }

    if (!is_null($query->filter)) {
      $where .= $sep . '(' . $query->filter . ')';
      $sep = ' AND ';
    }
    
    if (!is_null($query->qfilter)) {
      $where .= $sep . ' ( ';
      // $sep = ' AND (';
      $sep = '';
      $first = TRUE;
      foreach($query->view->columns as $col) {
        if ($col->IsQuickFilter()) {
          $where .= $sep . $col->GetSqlName() 
            . ' LIKE "' . $query->qfilter . '%"';
          $sep = ' OR ';
        }
      }
      $where .= ' ) ';
      $sep = ' AND ';
    }

    if (isset($query->view->filter)) {
      $where .= $sep . ' (' . $query->view->filter . ')';
    }

    /***********
    $s = 'SELECT COUNT(*), '
      . $query->view->SqlSelectColumns()
      . ' ' . $query->view->SqlSelectFrom()
      . $where;

    $result = sql_query($s);
    // $q = mysql_query($s) or print('Invalid query:' . $s);
    
    $query->rowcount = mysql_result($result,0,0);
    *******/

    $s .= $where;
    
    
//      $s .= ' ' . $query->leader->SqlSelectFrom()
//        . $where;
    
    if (! is_null($query->orderby)) {
      $s = $s . ' ORDER BY ' . $query->orderby;
    }
    // echo $s;
    // echo ( $s);
    return $s;
  }

  function Peek($table,$id,$columns='*') {
    ToDebug('MySQLDriver.Peek()');
    assert('is_array($id)||inspect($id)');
    // print_r($id);
    // print_r($id);
    $sql = 'SELECT ';
    $sep = '';
    foreach($table->fields as $fld) {
      $sql = $sql . $sep
        . $table->name . '.' . $fld->name;
      // . ' AS ' . $this->name . '_' . $fld->name;
      $sep = ',';
    }
    $sql = $sql . ' FROM ' . $table->name;
    $pkeys = $table->GetPrimaryKey();
    $sep = ' WHERE ';
    $i = 0;
    foreach($pkeys as $pk) {
      $type = $table->fields[$pk]->type;
      $sql .= $sep . $pk . '=' . $type->to_sql($id[$i]);
      $sep = ' AND ';
      $i+=1;;
    }
    $result = $this->sql_select($sql);
    if ( mysql_num_rows($result)!=1 )
      return NULL;
//        trigger_error($sql.' returned '
//                      .mysql_num_rows($result).' rows',
//                      E_USER_ERROR);
    return mysql_fetch_array($result,MYSQL_ASSOC);
  }


  
  function OpenQuery($query) {
    $sql = $this->GetSqlSelect($query);
    $result = new Result();
    $result->handle = $this->sql_select($sql);
    $result->rowcount = mysql_num_rows($result->handle);
    
    if ($query->page != 0) {
      $start = $query->GetPageLength() * ($query->page-1);
      $sql .= " LIMIT $start , " . $query->GetPageLength();
      $result->handle = $this->sql_select($sql);
    }
    if ($query->page == 0) {
      $result->recno = 0;
    } else {
      $result->recno = ($query->page-1) * $query->GetPageLength();
    }
    return $result;
  }


  /**
     Query.fetch_row()
   */
  function fetch_row(&$query,&$result) {
    $row = mysql_fetch_row($query->result->handle);
    if (! $row) return FALSE;
    $query->result->recno++;
    $i = 0;
    $query->row = array();
    $query->row['_new'] = FALSE;
    foreach($query->leader->fields as $field) {
      $query->row[$field->name] = $row[$i];
      $i++;
    }
    foreach($query->leader->joins as $join) {
      $joinRow = array();
      $empty = TRUE;
      foreach($join->toTable->fields as $field) {
        $value = $field->type->str2value($row[$i]);
        $joinRow[$field->name] = $value;
        $i++;
        if (!is_null($value)) $empty = FALSE;
      }
      if ($empty) $joinRow = NULL;
      $query->row[$join->alias] = $joinRow;
    }
    return TRUE;
  }

}

$dbd = new MySQLDriver();

$con = mysql_pconnect($host, $user, $pass)
   or die ("Unable to connect!");
mysql_select_db($db,$con)
  or die ("Unable to select database $db!");


?>
