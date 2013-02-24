==============
Lino pour CPAS
==============

(no longer maintained)

Ceci est la page où je collectionnaise, en français, 
les idées et plans pour le déceloppement futur de Lino pour CPAS.

Lino pour CPAS est une application Lino, 
la première application Lino réellement utilisée,
dont je compte déléguer la maintenance à une organisation 
indépendante.

Aperçu code source
------------------

Au niveau du code source, Lino pour CPAS consiste en 
l'application proprement dite :mod:`lino_welfare.modlib.pcsw` 
et de certains modules  que l'on peut considérer spécifiques 
aux CPAS:

- :mod:`lino.modlib.jobs` (Art 60/7)
- :mod:`lino.modlib.isip`  (Projets PIIS)
- :mod:`lino.modlib.cv` (Curriculums vitae des clients)
- :mod:`lino.modlib.newcomers` (Nouveaux clients)
- :mod:`lino.modlib.cbss` Connexion BCSS
- :mod:`lino.modlib.households` (Ménages)
- :mod:`lino.modlib.debts` (Médiation de dettes)

Les modules suivants sont utilisés dans Lino pour CPAS, 
mais plutôt d'intérêt général et leur maintenance resterait 
idéalement plutôt dans le cadre général du framework:

- :mod:`lino.modlib.contacts`
- :mod:`lino.modlib.cal`
- :mod:`lino.modlib.outbox`
- :mod:`lino.modlib.postings`
- :mod:`lino.modlib.notes`

Données signalétiques spécifiques aux CPAS
------------------------------------------

Pour leurs Clients, les CPAS retiennent 
toute une série de données signalétiques 
spécifiques (non définies dans :mod:`lino.modlib.contacts`)
tels que 
`id_card_no` (n° de carte d'identité),
`national_id` (NISS) 
`civil_state` (Etat civil) 
et `birth_place` (lieu de naissance).

(Liste complète: 
activity    
bank_account1        
bank_account2
remarks2
gesdos_id
is_cpas
is_senior
group
birth_place
birth_country
civil_state
national_id
health_insurance
pharmacy
nationality
card_number
card_valid_from
card_valid_until
card_type
card_issuer
noble_condition
residence_type
in_belgium_since
unemployed_since
needs_residence_permit
needs_work_permit
work_permit_suspended_until
aid_type
income_ag    
income_wg    
income_kg    
income_rente 
income_misc  
is_seeking
unavailable_until
unavailable_why
obstacles
skills
job_agents    
job_office_contact)
   

Où va-t-on mettre ces champs: les garder dans `Person` 
ou ajouter une nouvelle table `Client`?
On pourrait différencier entre "Personnes" simples et "Clients". 
Ces derniers étant des personnes spéciales pour lesquelles 
Lino gère plus d'information que pour des simples personnes de contact.
Une simple personne de contact est p.ex. le directeur d'une société employante,
pour lequel Lino requiert une entrée dans le signalétique "Person" 
car il figure en tant que représentant pour une série de contrats.

Observations:

- Pour le champ `birth_place` il est 
  inutile de maintenir un historique de manière accessible.
  Le lieu de naissance d'une personne ne change jamais 
  (sauf correction d'erreeer d'encodage)

  Je dis "historique accessible" parce qu'il y a toujours la possibilité 
  de consulter le system log pour voir qand la valeur d'un champ a été modifiée 
  et par qui. Ce changelog (qui pour l'instant est encore primitif) deviendra en 
  plus plus facilement consultable dans le futur quand Lino aura la possibilité 
  d'un historique général des changements. 
  Mais il restera toujours en arrière-plan.
  "Historique accessible" par contre veut dire 
  "relativement visible pour l'utilisateur".
  
- Si une personne reçoit une nouvelle carte d'identité, 
  le CPAS modifiera simplement le champ `id_card_no` sans 
  garder l'ancien numéro (dans un historique accessible) : 
  un CPAS ne s'intéresse pas aux cartes d'identité périmées.

- Il ne faudrait pas que ces données se voient dupliquées 
  inutilement p.ex. quand la personne change d'un centre vers un autre.
  
- Le NISS est obligatoire pour devenir Client.

- Lino doit refuser de créer plusieurs Personnes avec le même NISS.

Ces deux derniers points sont décisifs: 
**il faut une table séparée pour les Clients**.

Ce qui veut dire qu'il y aura un réarrangement au niveau 
de la table "Personnes".

.. 

  Ce qui veut dire que même pour le directeur d'une société employante
  (pour lequel Lino requiert une entrée dans le signalétique "Person" 
  car il figure en tant que représentant pour une série de contrats)
  nous avons la possiblité d'encoder ces données.



Accompagnements
---------------

Les champs `coached_from`, `coached_until`, `coach1` et `coach2`
doivent passer de Person vers une nouvelle table 
`Coaching` ("Accompagnements").

En plus Lino devra connaître le notion de Centre (une table contenant un 
record pour chaque CPAS "connu")

Plusieurs CPAS doivent pouvoir travailler dans une même base de données.
Ce scénario deviendra réel dès que le module Médiation des Dettes 
entre en production.
 
  
Voici la nouvelle structure (code simplifié)::

  class Centre(dd.Model):
      company = models.ForeignKey('contacts.Company')
      code_cbss = models.CharField(unique=True)
      president = models.ForeignKey('contacts.Person')
      secretary  = models.ForeignKey('contacts.Person')
      
  #class Service(dd.BabelNamed):
  #    centre = models.ForeignKey(Centre)
  #    (une table avec trois Services: Intégration, Social et Dettes)
    
  class Coaching(dd.Model):
      client = models.ForeignKey('pcsw.Client')
      # service = models.ForeignKey(Service)
      start_date = models.DateField()
      end_date = models.DateField()
      agent = models.ForeignKey('users.User',verbose_name="Assistant responsable")
    
À propos du champ `code_cbss` d'un Centre: 
Quand on fait une demande ManageAccess LIST, 
Lino pourrait convertir la réponse en une suite de Coachings.
Le centre de Verviers, même si celui-ci n'utilise pas Lino, 
pourrait se trouver dans notre base de données.
Le `code_cbss` sert à l'identifier quand nous communiqons avec la BCSS.

Regardons quelques cas limites:

- Un client du CPAS d'Eupen 
  déménage à Raeren (un autre centre géré par Lino), 
  puis à Verviers (centre qui ne travaille pas encore avec Lino), 
  puis revient à Eupen.

  La personne physique reste la même, son n° au Régistre National ne change pas.
  
  La BCSS (service ManageAccess) parle dans ce cas d´"intégration": 
  la même personne est *intégrée* 
  au cours du temps dans différents Centres, 
  chaque fois pour une période déterminée.
  
  Pour chaque changement d'adresse 
  il y aura un nouveau "Client" dans Lino,
  et chaque fois il y aura deux déclarations 
  :class:`ManageAccess <lino.modlib.cbss.models.ManageAccessRequest>`.


- Un assistant social meurt ou quitte définitivement son endroit de travail. 
  Ses collègues prennent en charge les Clients qu'il a accompagné. 
  
  Pour faciliter la réattribution des clients, Lino aura une table 
  `CoachingsByAgent`.

  L'aide sociale octroyée des clients et intégration à la BCSS 
  ne sont pas influencées.
  Il n'y a donc aucune raison d'informer la BCSS, 
  pas besoin de faire une déclaration
  :class:`ManageAccess <lino.modlib.cbss.models.ManageAccessRequest>`.



  Chaque CPAS est libre de décider pour soi s'il crée dans ce 
  cas un nouveau Coaching pour chaque personne concernée, 
  ou s'il change simplement les champs `agent` des Coachings existants. 
  Les petits centres ne sont peut-être pas intéressés d'avoir un historique 
  de ces données.
  
Intégrations
------------

Est-ce que les "intégrations" de la BCSS peuvent entrer dans 
notre table Coachings? 
Oubien faut-il une table supplémentaire pour les stocker?
Oubien suffit-il de dire quil faut consulter la dernière requête
ManageAccess?

Exemples fictifs:

- Personne qui n'a jamais été client autrepart que chez nous. 
  C'est d'abord Caroline qui l'accueuille pour décider qui 
  accompagnera cette personne. Elle fait les formalités 
  d'identification et crée le Client dans Lino. 
  Puis elle décide avec ses collègues de passer la 
  personne à Roger pour le service social général (SS) 
  et Alicia pour le service d'intégration (SI).
  Un mois plus tard le SI décide qu'Alicia passe son client à Hubert.
  

    Coachings:                          Intégrations:
  
    début    fin      Agent  Service    début    fin      Qualité Centre
    -------- -------- -------- -----    -------- -------- ------- ------
    20.02.05 01.03.05 Caroline  SA      01.04.05   .  .   1       Eupen
    01.03.05   .  .   Roger     SS
    01.03.05 31.03.05 Alicia    SI
    01.04.05   .  .   Hubert    SI
  
    début    fin      Agent  Service    début    fin      Qualité Centre
    -------- -------- -------- -----    -------- -------- ------- ------
    01.02.05   .  .   Caroline  SS      01.04.05   .  .   1       Eupen
    01.03.05 31.03.05 Alicia    SI
    01.04.05   .  .   Hubert    SI
  
- Personne qui a traversé d'autres Centres avant d'avoir abouti chez nous:

    Coachings:                          Intégrations:
  
    début    fin      Agent  Service    début    fin      Qualité Centre
    -------- -------- -------- -----    -------- -------- ------- ------
    01.02.05   .  .   Caroline  SS      01.04.05   .  .   1       Eupen
    01.03.05 31.03.05 Alicia    SI
    01.04.05   .  .   Hubert    SI


  
Poubelle
--------

Une autre idée étatit d'utiliser MTI::

    class Client(dd.Model):
        class Meta:
          abstract = True
        person = models.ForeignKey('contacts.Person')
        centre = models.ForeignKey(Centre)
        start_date = models.DateField()
        end_date = models.DateField()

    class SocialClient(Client):
        social_agent = models.ForeignKey('users.User',verbose_name="Assistant social")
    class IntegrationClient(Client):
        integ_agent = models.ForeignKey('users.User',verbose_name="Assistant d'insertion")
    class DebtsClient(Client):
        debts_agent = models.ForeignKey('users.User',verbose_name="Conseiller Dettes")

  Un argument important contre l'utilisation de MTI est que nous voudrons 
  probablement avoir une table `ClientsByPerson` qui montre les trois 
  types de Client dans l'ordre chronologique.


Questions ouvertes
------------------

- Un contrat PIIS: est-il lié à la Persone ou au Client/Coaching?
- Comment intégrér le workflow des nouveaux clients dans tout cela?

- Un AI décide, après avoir accompagné un client pendant quelques mois, 
  qu'il vaut mieux passer ce client à un autre AI.
  
- Dans la variante "Coaching", le champ `job_office_contact` 
  ("Personne de contact ONE") pourrait être remplacé 
  par un quatrième service, cette fois-ci un "service externe".
  Dans ce cas le champ `Coaching.agent` serait FK vers Person (au lieu de User).
  
- Est-ce vrai
  que les CPAS ne s'intéressent pas aux cartes d'identité périmées?
  


Demandes d'aide
---------------

Il y aura une nouvelle 
Table "Dossiers" ("Dossiers sociaux").
Un Dossier représente le fait qu'une Personne a introduit une demande d'aide.

- client
- centre
- date de début

DossiersByPerson: Historique des demandes d'aide





