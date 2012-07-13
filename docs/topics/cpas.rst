==============
Lino pour CPAS
==============

Ceci est la page où je collectione, en français, les idées et plans pour le déceloppement futur de Lino pour CPAS.

Lino pour CPAS est une application Lino, 
la première application Lino réellement utilisée,
dont je compte déléguer la maintenance à une organisation 
indépendante.

Aperçu code source
------------------

Au niveau du code source, Lino pour CPAS consiste en 
l'application proprement dite :mod:`lino.apps.pcsw` 
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

Différencier Clients et Personnes
---------------------------------

Un changement qui est quasi clair (mais pas encore implémenté):

- Quand Lino parle de "Personnes", il faudra bientôt différencier 
  entre "Personnes" simples et "Clients". 
  Ces derniers étant des personnes spéciales pour lesquelles 
  Lino gère plus d'information que pour des simples personnes de contact.

- En plus Lino devra connaître le notion de Centre (une table contenant un 
  record pour chaque CPAS "connu")

- Plusieurs CPAS doivent pouvoir travailler dans une même base de données.
  Ce scénario deviendra réel dès que le module Médiation des Dettes 
  entre en production.

Imaginons le cas d'un client du CPAS d'Eupen 
qui déménage à Raeren (un autre centre géré par Lino), 
puis à Verviers (centre qui ne travaille pas encore avec Lino), 
puis revient à Eupen.

La personne physique reste la même, 
son n° au Régistre National ne change pas.
La BCSS (service ManageAccess) parle dans ce cas d´"intégration": 
la même personne est *intégrée* 
au cours du temps dans différents centres, 
chaque fois pour une période déterminée.

Implémentation
--------------

Voici une première idée pour structurer cela::

  class Centre(dd.Model):
      company = models.ForeignKey('contacts.Company')
      code_cbss = models.CharField(unique=True)
      president = models.ForeignKey('contacts.Person')
      secretary  = models.ForeignKey('contacts.Person')
      
  class Client(dd.Model):
      person = models.ForeignKey('contacts.Person')
      centre = models.ForeignKey(Centre)
      start_date = models.DateField()
      end_date = models.DateField()
      integ_agent = models.ForeignKey('users.User',verbose_name="Assistant d'insertion")
      social_agent = models.ForeignKey('users.User',verbose_name="Assistant social")
      debts_agent = models.ForeignKey('users.User',verbose_name="Conseiller Dettes")
    
Vérifions cette idee en imaginant le cas suivant:

Quand un employé d'un CPAS quitte la place, ses collègues 
prendront en charge les clients qu'il a accompagné. 

- Il faudra bien-sûr changer les champs 
  `integ_agent`, `social_agent` et/ou `debts_agent`
  de tous les clients concernés. 

- L'aide sociale octroyée et intégration à la BCSS 
  ne sont pas influencées.
  Il n'y a donc aucune raison d'informer la BCSS, 
  pas besoin de faire une déclaration
  :class:`ManageAccess <lino.modlib.cbss.models.ManageAccessRequest>.

Mais chaque CPAS est libre de décider pour soi s'il crée dans ce 
cas un nouveau Client pour chaque personne concernée, 
ou s'il change simplement les champs `integ_agent`, `social_agent` etc. 
des Clients existant. 
Les petits centres ne sont peut-être pas intéressés d'avoir un historique 
de ces données.

Données signalétiques spécifiques aux CPAS
------------------------------------------

Pour leurs Clients, les CPAS retiennent 
toute une série de données signalétiques 
spécifiques (non définies dans lino.modlib.contacts)
tels que `id_card_no` (n° de carte d'identité) 
et `birth_place` (lieu de naissance).
En réalité il y en a beaucoup plus, 
nous prenons ces deux comme exemples.

Où va-t-on mettre ces champs: dans `Person` ou dans `Client`?
(Pour Lino c'est du pif au même, la question est: que voulons-nous?

Un désavantage de cette structure est que les données `id_card_no` et 
`birth_place` se voient dupliquées inutilement.


- Si une personne reçoit une nouvelle carte d'identité, je suppose 
  que le CPAS modifiera simplement le champ `id_card_no` sans créer 
  un nouveau Client: un CPAS ne s'intéresse pas aux cartes d'identité périmées.
  Mais ce n'est pas certain. Quelle est la probabilité qu'un CPAS donné voudrait 
  garder (de manière accessible) les données historiques sur les cartes d'identité?

- Pour le champ `birth_place` par contre il est 
  certainement inutile de maintenir un historique de manière accessible.

- Je dis "historique de manière accessible" parce qu'il y a toujours la possibilité 
  de consulter le system log pour voir qand la valeur d'un champ a été modifiée 
  et par qui. Ce changelog (qui pour l'instant est encore primitif) deviendra en 
  plus plus facilement consultable dans le futur quand Lino aura la possibilité 
  d'un historique général des changements. 
  "Accessible" veut donc dire "relativement visible pour l'utilisateur".
  
  
À propos du champ `code_cbss` d'un Centre: 

- Quand on fait une demande ManageAccess LIST, 
  Lino pourrait convertir la réponse en une suite de Clients.
  Le centre de Verviers, même s'il n'utilise pas Lino, 
  pourrait se trouver dans notre base de données.
  Le `code_cbss` sert à l'identifier quand nous communiqons avec la BCSS.


Alternativement Lino pourrait différencier d'avantage et faire un 
Client par "Accompagnement". Càd au lieu d'avoir trois champs
`integ_agent`, `social_agent` et/ou `debts_agent`, nous aurions::

  class Service(dd.BabelNamed):
      pass
      (une table avec trois Services: Intégration, Social et Dettes)
    
  class Client(dd.Model):
      person = models.ForeignKey('contacts.Person')
      centre = models.ForeignKey(Centre)
      service = models.ForeignKey(Service)
      start_date = models.DateField()
      end_date = models.DateField()
      agent = models.ForeignKey('users.User',verbose_name="Assistant responsable")
      id_card_no = ... 
      birth_place = ...
    
Oubien en utilisant MTI::

  class Client(dd.Model):
      class Meta:
        abstract = True
      person = models.ForeignKey('contacts.Person')
      centre = models.ForeignKey(Centre)
      start_date = models.DateField()
      end_date = models.DateField()
      id_card_no = ... 

  class SocialClient(Client):
      social_agent = models.ForeignKey('users.User',verbose_name="Assistant social")
  class IntegrationClient(Client):
      integ_agent = models.ForeignKey('users.User',verbose_name="Assistant d'insertion")
  class DebtsClient(Client):
      debts_agent = models.ForeignKey('users.User',verbose_name="Conseiller Dettes")

Un argument important contre l'utilisation de MTI est que nous voudrons 
probablement avoir une table `ClientsByPerson` qui montre les trois 
types de Client dans l'ordre chronologique.


Autre question: Un contrat PIIS: est-il lié à la Persone ou au Client?
