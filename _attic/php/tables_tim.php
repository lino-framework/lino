<?php

class PAR extends Table {

  function SetupFields() {
$this = new Table("PAR");
$this->AddIntField("IdPar","ID");
$this->AddStringField("Name","Name");
$this->AddStringField("Vorname","First Name");
$this->AddStringField("Allo","Anrede");
$this->AddStringField("Phone","Phone");
$this->AddStringField("Fax","Fax");
$this->AddStringField("EMail","E-Mail","mailto:");
$this->SetLabel( "Partners");
    $this->AddAction('viewform','Form View');
// $this->AddAction(new FormAction());
// $this->AddAction(new DetailAction('DocByPar'));
}
}


class ART extends Table {

  function SetupFields() {

$this->AddStringField("IdArt","ID");
$this->AddStringField("Name1","Description");
$this->AddStringField("Prix1","Price");
$this->AddStringField("Memo1","Memo (de)");
$this->AddStringField("Memo2","Memo (fr)");
$this->SetLabel("Products");
}
}


class CITIES extends Table {

  function SetupFields() {

$this->AddIntField("ID","ID");
$this->AddStringField("Name","Name");
$this->AddStringField("Country","Country");
$this->AddStringField("Zip","Zip");
$this->AddStringField("Format","Prefix");
}}


class COUNTRIES extends Table {

  function SetupFields() {

$this->AddIntField("ID","ID");
$this->AddStringField("Name","Name");
$this->AddStringField("IdLng","Lang");
$this->AddStringField("IdDev","Ccy");
$this->AddStringField("TelPrefix","Prefix");
$this->SetLabel( "Countries");
}}


class MSX extends Table {

  function SetupFields() {

$this->AddIntField("IdMsx","ID");
$this->AddStringField("Title_en","Title (en)");
$this->AddStringField("Title_de","Title (de)");
$this->AddStringField("Title_ee","Title (ee)");
$this->AddStringField("Title_fr","Title (fr)");
$this->AddMemoField("Body_en","Body (en)");
$this->AddMemoField("Body_de","Body (de)");
$this->AddMemoField("Body_fr","Body (fr)");
$this->SetLabel( "Entries");
}}


?>
