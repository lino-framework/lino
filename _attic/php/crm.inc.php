<?php

class ORG extends Table {

  function SetupFields() {
    $this->AddAutoIncField('id','ID');
    $this->AddStringField('name','Name');
    $this->SetLabel( 'Organisations');
  }

  
  function GetRowLabel($row) {
    return $row['name'];
  }

//    function SetupDetailQuery($master,&$detailQuery) {
//      $detailQuery->SetFormat(QRYFORMAT_COMMALIST);
//    }
}


class PERSONS extends Table {

  function SetupFields() {

    $this->AddAutoIncField("id","ID");
    $this->AddStringField("name","Name");
    $this->AddStringField("fname","First Name");
    $this->AddStringField("title","Title");
    $this->AddDateField("born","Born");
    $this->AddDateField("died","Died");
    
    $this->SetLabel( "Persons");

  }

  function GetRowLabel($row) {
    return $row['fname'] . ' ' . $row['name'];
  }

  function ShowInPage($query,$first) {
    BeginSequence(SEQ_FORM);
    $query->ShowCell('id');
    $query->ShowCell('title');
    $query->ShowCell('fname');
    $query->ShowCell('name');
    $query->ShowCell('addresses',DEPTH_SHORTLIST);
    $query->ShowCell('slots',DEPTH_SHORTLIST);
    $query->ShowCell('news',DEPTH_REF);
    $query->ShowCell('projects',DEPTH_REF);
    $query->ShowCell('changes',DEPTH_REF);
    EndSequence();
  }
//    function SetupDetailQuery($master,&$detailQuery) {
//      $detailQuery->SetFormat(QRYFORMAT_COMMALIST);
//    }

}


class SLOTS extends Table {

  function SetupFields() {
    $this->AddAutoIncField('id','ID');

    $this->AddStringField('type','Type');
    $this->AddStringField('slot','Slot');

    $this->SetLabel('Slots');

  }
  
  function GetRowLabel($row) {
    $s = '';
    $s .= $row['type'];
    $s .= ' ' . $row['slot'];
    return $s;
  }
  
//    function SetupDetailQuery($master,&$detailQuery) {
//      $detailQuery->SetFormat(QRYFORMAT_COMMALIST);
//    }
}

class ADDR extends Table {

  function SetupFields() {
    $this->AddAutoIncField('id','ID');

    // $this->AddStringField('email','E-Mail');

    $this->AddStringField('zip','Zip Code');
    $this->AddStringField('street','Street');
    $this->AddIntField('house','#');
    $this->AddStringField('box','box');
    // $this->AddStringField('tel','Phone');
    // $this->AddStringField('fax','Fax');

    $this->SetLabel('Addresses');

  }
  
  function GetRowLabel($row) {
    $s = '';
    $s .= $row['street'];
    $s .= ' ' . $row['house'];
    $s .= $row['box'];
    // $email = $query->row[$alias.'email'];
    $s .= ', ' . $row['zip'];
    $s .= ' (todo:city)' ;
    // $s .= $query->row['city_name'];
    // $city = $CRM->CITIES->Peek($query->row[$alias.'city'];);
    return $s;
  }
  
//    function SetupDetailQuery($master,&$detailQuery) {
//      $detailQuery->SetFormat(QRYFORMAT_COMMALIST);
//    }
}


class NATIONS extends Table {

  function SetupFields() {

    $this->AddStringField('id','ID',3);
    $this->AddStringField('name_en','Name');
    $this->AddStringField('name_de','Name');
    $this->AddStringField('name_fr','Name');
    $this->AddStringField('name_ee','Name');
    
//      $this->AddDetail('cities',
//                       'CITIES','nation',
//                       'Cities');
    
    $this->SetLabel( 'Nations');
  }

  function GetRowLabel($row) {
    return $row['name_en'];
  }
//    function SetupDetailQuery($master,&$detailQuery) {
//      $detailQuery->SetFormat(QRYFORMAT_COMMALIST);
//    }
}


class CITIES extends Table {

  function SetupFields() {

    $this->AddAutoIncField('id','ID');
    $this->AddStringField('name','Name');
    // $this->AddJoinField('nation','Country','NATIONS','cities');
    
    $this->SetLabel('Cities');
  }
  
  function GetRowLabel($row) {
    return $row['name'];
  }

}

class TALKS extends Table {
  function SetupFields() {
    $this->AddAutoIncField('id','ID');

    $this->AddDateField('date','Date');
    $this->AddStringField('time','Time');
    $this->AddStringField('type','Title');
    $this->AddStringField('title','Title');
    
    $this->AddMemoField('notes','Notes');
    $this->SetLabel('Talks');
  }
  
  function GetRowLabel($row) {
    return $row['date']
      . ' (' . $row['title'] . ')';
  }
}

class MEETINGS extends TALKS {
  function SetupFields() {
    parent::SetupFields();
    $this->SetLabel( 'Meetings');
  }
}

//  class ARTICLES extends Table {
//    function SetupFields() {
//      $this->AddIntField('id','ID');

//      $this->AddStringField('title','Title');
    
//      $this->AddMemoField('abstract','Abstract');
//      $this->AddMemoField('body','Body');
    
//      $this->label = 'Articles';
//    }

//    function GetRowLabel($row) {
//      if (strlen($row['title']) > 0) 
//        return $row['title'];
//      return $row['date'];
//    }
  
//    function ShowInList($query)
//    {
//      echo '<b>';
//      $query->ShowCell('title');
//      echo '</b>. ';
//      $query->ShowCell('abstract');
//      $query->ShowMore();
//    }

//    function ShowInPage($query,$first) {
//      $query->ShowCell('abstract');
//      echo '<p>';
//      $query->ShowCell('body');
//    }
//  }


class ORG2ORG extends LinkTable {
  
  function ORG2ORG() {
    $this->LinkTable('ORG','superOrgs','ORG','subOrgs');
  }
}

class ORG2PERS extends LinkTable {
  function ORG2PERS() {
    $this->LinkTable('ORG','contacts',
                     'PERSONS','isContactFor');
  }
  
  function SetupFields() {
    
    $this->AddStringField('note','Note');
    $this->SetLabel('Contact persons');
  }
  
  function ShowPageRef($query,$label=NULL,$alias='') {
    parent::ShowPageRef($query,$label,$alias);
    echo ' (';
    $query->row['note'];
    echo ')';
  }
}

class MEET2PERS extends LinkTable {
  function MEET2PERS() {
    $this->LinkTable('MEETINGS','participants',
                     'PERSONS','participatesIn');
  }
  function SetupFields() {
    $this->AddStringField('note','Note');
    $this->SetLabel( 'Participants');
  }
  
//    function ShowPageRef($query,$label=NULL,$alias='') {
//      parent::ShowPageRef($query,$label,$alias);
//  //      echo ' (';
//  //      $query->ShowCell('note');
//  //      echo ')';
//    }

}



class ADDRBOOK extends Module {
  
  function SetupTables() {

    $this->DeclareTable('PERSONS',new PERSONS());
    $this->DeclareTable('ORG',new ORG());
    $this->DeclareTable('CITIES',new CITIES());
    $this->DeclareTable('NATIONS',new NATIONS());
    $this->DeclareTable('ADDR',new ADDR());
    $this->DeclareTable('SLOTS',new SLOTS());
           
    $this->DeclareTable('ORG2ORG',new ORG2ORG());
    $this->DeclareTable('ORG2PERS',new ORG2PERS());

  }

  function SetupLinks() {

    $this->AddLink('ADDR','pers','Person',
            'PERSONS','addresses','Addresses');
    $this->AddLink('ADDR','org','Organisation',
            'ORG','addresses','Addresses');
    
    $this->AddLink('SLOTS','pers','Person',
            'PERSONS','slots','Slots');
    $this->AddLink('SLOTS','org','Organisation',
            'ORG','slots','Slots');
    
    /* ADDR->nation is declared without 4th parameter toDetail which
     means that there is no detail in NATIONS to show all ADDR in this
     country */
    
    $this->AddLink('ADDR','nation','Country',
            'NATIONS');
    
    $this->AddLink('ADDR','city','City',
            'CITIES', 'addresses','Addresses');    
    $this->AddLink('CITIES','nation','Country',
            'NATIONS','cities','Cities');

  }
}


class AGENDA extends Module {
  function SetupTables() {
    $this->DeclareTable('TALKS',new TALKS());
    $this->DeclareTable('MEETINGS', new MEETINGS());
    $this->DeclareTable('MEET2PERS', new MEET2PERS());
  }
  
  function SetupLinks() {
    
    $this->AddLink('TALKS','ipers','Responsible',
                   'PERSONS','icontacts','Contacts(i)'); // ,DETAIL_REF);
    $this->AddLink('TALKS','epers','Partner',
                   'PERSONS','econtacts','Contacts(e)'); // ,DETAIL_REF);
    
    $this->AddLink('MEETINGS','org','Organisation',
                   'ORG','meetings','Meetings by this Org');
    $this->AddLink('MEETINGS','addr','Address',
                   'ADDR','meetings','Meetings at this address');
    
  }
}


?>
