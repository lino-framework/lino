<html>
<p>The following articles taught me that PHP knows class methods:

http://zend.com/zend/trick/tricks-dec-2001.php
http://zend.com/zend/trick/tricks-app-patt-php.php

<p>Here is the test:
<p>

<?php

$tables = array();

class Table {

  var $fields = array();

  function &GetInstance($name) {
    global $tables;
    if (isset($tables[$name])) {
      return $tables[$name];
    }
    $x = 'return new ' . $name . '(\'' . $name . '\');';
    $table = eval($x); // new $$name($name);
    $tables[$name] =& $table;
    $table->SetupFields();
    return $table;
  }

  function SetupFields() {
    echo 'Table->init() never called';
  }
  
  function foo() {
    echo '<br>'. get_class($this) . '->foo()';
    echo '<br>I have now '. count($this->fields) . ' field(s)';
  }
  
}

class PERSONS extends Table {
  function SetupFields() {
    echo 'PERSONS:init()';
    $this->fields[] = 'field1';
  }

}


$p =& Table::GetInstance('PERSONS');
$p->foo();
$p->fields[] = 'field2';

$q =& Table::GetInstance('PERSONS');
$q->foo();



?>
</html>
