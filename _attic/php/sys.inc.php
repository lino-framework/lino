<?php

// ProvidesModule('SYS');


class QUERIES extends Table
{
  function SetupFields() {
    $this->AddStringField('id',"ID");
    $this->AddStringField("master","Master Table");
    $this->AddStringField("label_en","Title");
    $this->AddIntField("pglen",'Page Size');
    $this->AddStringField('filter','Filter');
    // $this->AddStringField("desc_en","Description");
    
//      $this->AddDetail('columns',
//                       'QRYCOLS',
//                       'query',
//                       'Columns');
    
    $this->SetLabel('Views');
  }

//    function SetupQuery($query) {
//      // $QUERIES =& Table::GetInstance('QUERIES');
//      // $this->details['columns']->slave->SetFormat(QRYFORMAT_TABLE);
//    }
}

class QRYCOLS extends Table
{
  function SetupFields() {
    // $this->AddJoinField('query',"Query",'QUERIES','columns');
    $this->AddIntField('seq',"Seq");
    $this->AddStringField('coltype','Column Type');
      $this->f_SetPickList('coltype_list');
    $this->AddStringField("alias","Alias");
      $this->f_SetPickList('table_list');
    $this->AddStringField("fieldname",'Field name');
    $this->AddStringField("label_en","Header");
    // $this->AddStringField("desc_en","Description");    
    // no description for each query. QRYCOLS is for "display" data,
    // not for help.    
    $this->AddStringField("width","Width");
    $this->AddBoolField('qfilter','Filter');
    $this->SetLabel( 'View Columns');
  }

  function GetPrimaryKey() {
    return array('query_id','seq');
  }

  function table_list($row) {
  }
  function coltype_list($row) {
    return array(
      'A' => 'Action',
      'V' => 'Vurt',
      'F' => 'Field'
    );
  }
}

class LANG extends Table {

  function SetupFields() {

    $this->AddStringField('id','ID',3);
    $this->AddStringField('name_en','Name');
    $this->SetLabel( 'Languages');
  }

  function GetRowLabel($row) {
    return $row['id'];
    // $row['name_en'];
  }
  
}



class SYS extends Module {
  
  function SetupTables() {
    ToDebug('SYS.SetupTables()');
    $this->DeclareTable('QUERIES',new QUERIES());
    $this->DeclareTable('QRYCOLS',new QRYCOLS());
    $this->DeclareTable('LANG'   ,new LANG());
    ToDebug('SYS.init() : done');
  }

  function SetupLinks() {
    $this->AddLink('QRYCOLS','query','Query',
                   'QUERIES','columns','Columns');

  }
}


?>
