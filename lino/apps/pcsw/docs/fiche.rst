Fiche technique
===============

Lino est un framework (librarie de construction d’applications), et « Lino pour CPAS » est
une des applications principales développées également par l’auteur du framework.

Charactéristiques du framework
------------------------------

- Lino utilise les technologies Python, Django et ExtJS pour délivrer 
  des Rich Internet Applications (RIA) au look « desktop ».
- Une application Lino fonctionne indépendamment du système d’exploitation et de l’endroit géographique
- Lino tourne sur n’importe quel serveur qui offre Apache/mod_wsgi (ou un autre serveur web compatible WSGI) et une des bases de données MySQL, PostgreSQL, SQLite, Oracle. En pratique nous recommendons Debian ou Ubuntu.
- Plusieures instances par serveur possible (par exemple pour différentes applications/services et/ou environnement de test)
- Multilingue à trois niveaux : (1) interface utilisateur (2) désignations des codes et (3) destinataire d’un document
- Génération automatique de documents de type PDF, MS-Word, OpenOffice et autres se basant sur des templates (modèles, gabarits)
- WebDAV automatique intégré afin de pouvoir éditer des documents générés et stockés sur le serveur sans que l’utilisateur doive intervenir.
- Export des données vers des tableurs
- Filtres et fonctions de recherche intuitifs et avancés
- Authentication annuaire LDAP
- Customisation facile
- Système sophistiqué pour définir et modifier les workflows Fonctionnalités générales secrétariat
- Gestion des contacts avec personnes et organisations.
- Calendrier
- Messagerie électronique
- Gestion des envois (courriers, mails, SMS, ...) Fonctionnalités spécifiques aux CPAS 

Signalétiques
-------------

- Les signalétiques spécifiques aux CPAS (Clients, Ménages,...) sont intégrées de 
  manière transparente dans la gestion générale des contacts.
  

Historique client
-----------------

- Gestion des documents scannés (permis de conduire, de résidence, de travail,...).
  Rappel optionnel si la date de fin de validité approche.
  
- Les travailleurs sociaux notent chaque événement. 
  Traçabilité par exemple des appels téléphoniques, des contacts internes et externe avec clients, 
  collègues ou partenaires, courriers, ...
  
Service d’insertion socio-professionnelle
-----------------------------------------

- Gestion des données relatives au CV (formations, expériences professionnelles, 
  connaissances des langues, compétences, ...)  
  Possibilité de recherche avancée sur base de ces critères.
  
- Gestion des PIIS (VSE): saisie, création automatique et impression du contrat papier, 
  consultation, analyse statistique, rappels automatique des évaluations intermédiaires 
  à prévoir
  
- Gestion des projets de mise au travail (Art. 60§7): saisie, création automatique et impression de la convention papier, consultation, analyse statistique, rappels automatique des évaluations intermédiaires à prévoir

- Gestion des partenaires Art60§7

- Gestions des offres d’emploi vacants 

Gestion des cours de langues
----------------------------

- Gestion des organisations externes organisant des cours de langue
- Par client saisir des demandes de cours
- Par organisation une liste des candidats
- Gestion de l’offre et de la demande

Gestion des nouvelles demandes/clients
--------------------------------------

- Gestion des spécialités attribuées aux travailleurs sociaux.
- Proposition automatique des travailleurs sociaux compétents selon les spécificités de la demande et attribution selon la disponibilité

Médiation de dettes
-------------------

Interface d’encodage des données (dépenses, revenus, obligations, répartition au marc-lefranc)
et création automatique d’un budget mensuel individuel ou par ménage.

Connexion BCSS (nouvelle technologie SOAP/XML)
----------------------------------------------

- Données légales RN (IdentifyPerson)
- Intégration (ManageAccess)
- Registre National avec historique (Tx25)

