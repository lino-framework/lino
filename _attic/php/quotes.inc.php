<?php

class QUOTES extends MemoTable {
  function SetupFields() {
    parent::SetupFields();
    $this->AddAutoIncField('id','ID');
    $this->AddStringField('pubRef','ref in publication');
    
    $this->SetLabel('Quotes');
  }

  function SetupMainQuery(&$query) {
    // echo 'DBITEMS';
    // parent::SetupMainQuery($query);
    $query->SetLabel('Quotes');
    $query->SetDepth(DEPTH_LIST);
    $query->order = 'superSeq';
  }

  function ShowInList($query)
  {
    BeginSequence(SEQ_SENTENCES,$query->row['title'],FALSE);
//      echo ( '<b>');
//      $query->ShowCell('title');
//      echo ( '</b>. ');
    $query->ShowCell('abstract');
    echo ( ' (');
    $query->ShowCell('author');
    echo ( ')');
    $query->ShowMore();
    EndSequence();
  }
  function ShowInPage($query,$first) {
    parent::ShowInPage($query,$first);
    $query->ShowCell('author');
  }
}


class PUBLICATIONS extends SuperMemoTable {
  function SetupFields() {
    parent::SetupFields();
    $this->AddIntField('id','ID');
    // $this->AddStringField('type_id','type');
    $this->AddStringField('subtitle','subtitle');
    $this->AddStringField('typeRef','type specific ref');
    $this->AddIntField('year','year');

    $this->SetLabel('Publications');
  }
  
  function GetRowLabel($row) {
    $s = '';
//      if (!is_null($row['author_id']))
//        $s .= $this->joins['author']->
    $s .= $row['title'];
    if (!is_null($row['year']))
      $s .= ' (' . $row['year'] . ')';
    return $s;
  }

  function ShowInList($query)
  {
    BeginSequence(SEQ_SENTENCES,$query->row['title'],FALSE);
//      echo ( '<b>');
//      $query->ShowCell('title');
//      echo ( '</b> : ');
    $query->ShowCell('subtitle');
    $query->ShowCell('authors');
    $query->ShowCell('year');
    EndSequence();
    BeginSequence(SEQ_BR,NULL,FALSE);
    $query->ShowCell('abstract');
    $query->ShowMore();
    EndSequence();
  }

  function ShowInPage($query,$first) {
    BeginSequence(SEQ_FORM);
    $query->ShowCell('id');
    $query->ShowCell('title');
    $query->ShowCell('subtitle');
    $query->ShowCell('authors',DEPTH_SHORTLIST);
    EndSequence();
    parent::ShowInPage($query,$first);
  }
  
}

class PUBTYPES extends Table {
  function SetupFields() {
    $this->AddStringField('id','ID');
    $this->AddStringField('name_en','');
    $this->AddStringField('typeRefPrefix','typeRef prefix');
    $this->AddStringField('pubRefLabel','pubRef label');

    $this->SetLabel('Publication Types');
  }

  function GetRowLabel($row) {
    return $row['name_en'];
  }
}


  
class QuotesModule extends Module {
  
  function SetupTables() {
    $this->DeclareTable('QUOTES',new QUOTES());
    $this->DeclareTable('PUBLICATIONS',new PUBLICATIONS());
    $this->DeclareTable('PUBTYPES',new PUBTYPES());
    
    $this->DeclareTable('PUB2PERS',
                        new LinkTable('PUBLICATIONS','authors',
                                      'PERSONS','publications'));
  }
  
  function SetupLinks() {
    $this->AddLink('QUOTES','author','Author',
                   'PERSONS','quotes','Quotes'); 
    $this->AddLink('QUOTES','pub','Publication',
                   'PUBLICATIONS','quotes','Quotes'); 
    $this->AddLink('PUBLICATIONS','type','Publication Type',
                   'PUBTYPES','publications','Publications by Type'); 
  }
}


?>
