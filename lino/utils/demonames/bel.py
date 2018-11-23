# -*- coding: UTF-8 -*-
# Copyright 2012-2016 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

# $ python setup.py test -s tests.UtilsTests.test_demonames

"""
Example usage:

The first five Belgians:

>>> for i in range(5):
...     print(LAST_NAMES_BELGIUM.pop())
Adam
Adami
Adriaen
Adriaensen
Aelter

>>> from lino.utils.demonames import LAST_NAMES_RUSSIA

Next comes a group of five Russians:

>>> for i in range(5):
...     print(LAST_NAMES_RUSSIA.pop())
Abezgauz
Aleksandrov
Altukhov
Alvang
Ankundinov

Or here is a mixture of nationalities, for each Belgian comes one foreigner:

>>> from lino.utils.demonames import LAST_NAMES_MUSLIM
>>> LAST_NAMES = Cycler(LAST_NAMES_BELGIUM,
...     LAST_NAMES_RUSSIA, LAST_NAMES_BELGIUM, LAST_NAMES_MUSLIM)

>>> for i in range(10):
...     print(LAST_NAMES.pop())
Aelters
Arent
Aelterman
Abad
Aerens
Arnold
Aerts
Abbas
Aertsens
Arshan

Sources:

The raw data was originally copied from:

- Belgian last names from http://www.lavoute.org/debuter/Belgique.htm
- French last names from http://www.nom-famille.com/noms-les-plus-portes-en-france.html
- Russian last names from http://www.meetmylastname.com/prd/articles/24
- French first names from
  http://meilleursprenoms.com/site/LesClassiques/LesClassiques.htm
- African, Muslim and Russian names from
  http://www.babynames.org.uk
  and http://genealogy.familyeducation.com
  
- Streets of Liège (STREETS_OF_LIEGE) are from
  http://fr.wikipedia.org/wiki/Liste_des_rues_de_Li%C3%A8ge
  

"""

from __future__ import print_function
from __future__ import unicode_literals

import re
STREET_RE = re.compile(r"\*\s*\[\[(.+)\]\]\s*$")

from lino.utils import Cycler


def splitter1(s):
    for ln in s.splitlines():
        ln = ln.strip()
        if len(ln) > 1 and ln[0] != '#':
            yield ln


def splitter2(s):
    return [name.strip() for name in s.split(',')]


def splitter3(s):
    for ln in s.splitlines():
        ln = ln.strip()
        if len(ln) > 1 and ln[0] != '#':
            a = ln.split()
            name = a[0]
            yield name


LAST_NAMES_BELGIUM = u"""
 
A

Adam

Adami

#Adriaenssens

Adriaen

Adriaensen

#Adriaenssen

#Adriencense

#Adriensence

#Adrienssens

Aelter

Aelters

Aelterman

Aerens

Aerts

Aertsens 

Albumazard

Alloo

Alsteen

Andersson

André

Andries

Andriessen

Anthon

Antoine

Appelbaum

Applaer

Arimont

Arquin

Arteman

B

Baert

Bartholomeeus

Bastien 

Bastin

Baugnet

Baugniet

Baugniez

Bauwens

Beauve

Beck

Beckers

Bernard

Bertrand

Bietmé

Blaas

Blankaert

Blanquaert

Blondeel

Blondeeuw

Blondoo

Bodart

Bodson

Boeck

Boesmans

Bogaert

Bogaerts

Bogemans

Booghmans

Borremans

Borsu

Borsus 

Borsut 

Bosmans

Bouch

Bouchhout

Bouillère

Bouillet

Boulanger

Bourton

Bouxin

Brasseur

Brouck

Broucke

Broucq

Broucque

Brouhier

Brug

Bruggesman

Bruynseel 

Bruynseels

Burger

Burghgraeve

Burgmeester

Burton

Burtont

Buyle

C

Calbert 

Callebaut

Callebert 

Callebout

Camby

Cappelaere

Cappelaire 

Cappelier 

Cappeliez 

Cappellier 

Carbonez

Carbonnez

Carlier

Casteau

Castel

Castiaux

Cauderlier

Caudron

Cauvel

Cauvet

Cauvin

Cavard

Ceulemans

Chantry

Charlier

Chêneboit

Chestay

Chestia

Chrispeels

Christiaens

Christoffel

Claes

Claessens

Claeys

Claus

Cléban

Clébant

Clerx

Colinus

Collard

Colleye
Collignon
Collin
Colson
Cool
Cools
Coppens
Corain
Corijn
Corin
Cornelis
Cornet
Corrin
Corring
Corringer
Coryn
Coudyser
Couhysder
Coutijser 
Coutiser 
Crab 
Crabbe
Crama

Crépez

Crespel

Crevisse

Crevits

Crispeel

Crispeels

Crispel

Crispiels

Cuvelier

Cuypers

D

Daan

Daels

Daems

Dalmans

Damard 

Damart

Danis

Dany 

Danys 

Dapvril

Daufresne

Dawance

De Backer

De Bisschop

De Bloedt

De Blonde

De Boeck

De Bosscher

De Bosschere

De Bruyn

De Busschere

De Buyle

De Clercq

De Cock

De Coninck

De Conninck

De Coster

De Cruyenaere

De Cuyper

De Decker

De Doncker

De Draier

De Flandre

De Frankrijker

De Greef

De Griek

De Groot

De Groote

De Guchteneere

De Haese

De Hert

De Hertog

De Hoorne

De Kimpe

De Markgraef

De Meester

De Meulenaer

De Meyer

De Molder

De Munck

De Muynck

De Muyncke

 De Muynek

 De Muynke

De Naeyer

De Nayer 

 De Pannemacker

De Pannemaecker

De Pauss

De Pauw

De Pelsemaeker

De Pester 

De Potter

De Praeter

De Prester

De Ridder

De Ridere

De Rovéréaz

De Rudere

De Sachte

De Saedeleer

De Saert

De Schepper

De Schoone

De Smedt

De Smet

De Smeytere

De Smidt

De Smit 

 De Smyter

De Stracke

De Sueter

De Vette

De Voghels

De Vos

De Vrient

De Wilde

De Winter

Debacker

Debaere

Debakker

Debaut

Debecker

Debekker

Debled

Deboschere

Deboscker

Deboskre

Debosscher

Debosschere

Debusschere

Debuyst

Declerck

Declercq

Decock

Decocq

Decrucq

Decruyenaere

Defaux

Defawe

Degroote

Dehoorne

Dehorne

Dehornes

Deilgat

Dejong

Dejonghe

Dekale

Dekimpe 

Dekoch

Dekuiper

Dekyndt

Delacuvellerie

Delafosse 

Delahaye 

Delahayes 

Delbouille

Delboulle

Delcorps

Delflache

Delfosse

Delgat 

Delhaye

Delhoste 

Delhotte

Delmare

Delmer

Delobbe

Delobe 

Delobes 

Delplace

Delvaux

Demain

Demeiere

Demeyer

Demoor

Demoore

 Demunck

Demunck

Demuynck

Den Ouste

Denaeyer

Denayer

Deneyer

Denis

Denoor

Depannemaecker

Depelsemacker

Depelsemaeker

Depelsenaire 

Depelseneer 

Depercenaire 

Depester 

Depiéreux 

Depierreux 

Depireux 

Depoorter

Depoortere 

Depooter 

Depootere 

Deporter 

Deportere 

Depoterre

Deprez

Deramaix

Deroosse

Desandrouins

Descamps

Deschepper

Desmedt

Desmet

Desmets

Desmeytere

Desmidt

Desmidts 

Desmit

Desmyter

Desmytter

Desmyttere

 Despineto

Després 

Despret 

Desprets 

Despretz 

Desprey 

Desprez 

Destoute

Deswart

Deswarte

Dethier

Deur

Deurwaerder

Devis

Devloo

Devos

Devriend

Dewever

Dewit

Dewitte

Dewyse

D'Haeyer

Dhaeyer

D'Hoeraen

Dhoeraen

D'hoolaege

Dierckx

Dierik

Doeraene

Dolhaeghe

Domiens

Dominicus

Dondaine

Dondeine 

Dondenne 

Dondeyne 

Doolaeg(h)e

Doolaegue

Doolage

Doorn

Doorne

Doorneman

Draier

Dresselaers

Dubled

Dubois

Dumont

Dupont

Duquesnay

Duquesne

Duquesnoy

E

Ebrard

Eeckeman

Eerkens

Erckens

Erk

Erken

Erkens

Etienne

Euvrard

Evert

Evrard

Evras

Evrat

Eyck

Eysermans

F

Fawat

Faweux

Fee

Felix

Flamenck

Floche

Floquet

Fontaine

Fonteyne

Fraigany

Fraigneux

Francoeur

François

Francon

Frankel

Franken

Frankeur

Frans

Fransman

Fransolet

Franzman

Frijer

G

Gabriels

Gadisseur

Gadisseux

Gasthuys

Gaudisseu

Geerts

Gehucht

Geiregat

Geeregat 

Gendebien

Genot

Georges

Gérard

Gerlache

Gerlaxhe 

Germay

Germéa

Germeau

Ghiste

Gilles

Gillet

Gilson

Gits

Giets

Gidts

Geets

Geerts

Glaze

Glazeman

Goethals

Goffin

Gomaert

Gomardt

Goor

Goossens

Goud

Goudman

Goudsmith

Gourdet

Gousson

Graas

Greggs

Gregh

Grégoire

Gregoor

Grewis

Groot

Groote

Grotaers

Guillaume

Guyaux

H

Haesen

Haesevoets

Halasi

Halazy

Hamers

Hanssens

Hardas 

Hardat

Hardy

Heerbrant

Hendrick

Hendrickx

Hendriks

Henry

Herbrand 

Herbrandt 

Herbrant 

Herman

Hermann 

Hermans

Herten

Hertogs

Hertogue

Heylen

Heymans

Heynemans

Heyrman

Hinck

Hinckel

Hincker

Hinkel

Hinkels

Hinkens

Hinker

Hinkle

Hoefnagel 

Hoefnagels 

Holemans

Honnay

Horlin

Houvenaghel

Hoyois

Hubert

Huig

I

Ickx

Istace 

Istasse 

J

Jaak

Jaap

Jacob

Jacobs

Jacques

Jacquet

Jan

Janhes

Jansen

Janssen

Janssens

Jef

Jenot

Jeuniaux

Joire

Jone

Joneau

Jonet

Jongers

Jonné

Jonet

Jonnet

Jordaens

Jorez

Joris

Jorissen

Jozef

Julianus

Julius

Jurgen

K

Kaalman

Kaisin

Keetels

Kenens 

Kenes 

Kenis 

Kennens 

Kennes 

Kennis 

Kesteloot

Ketel

Ketelsmit

Kiecken

Kimpe 

Kinnen 

Klein 

Kleineman

Kleiner 

Kleinerman

Kleinman 

Klerk

Kleynen

Klingeleers

Kobus

Koeck

Konninckx

Koolman

Korring

Kramers

Kreemers

Kuipers

L

Labbez

Lacroix

Laenen 

Laenens 

Lafontaine 

Lambert

Lambrechts

Lanen 

Lanens 

Langlez

Lapayre

Laseur

Laseure

Lauffer

Laurent

Lauwers

Le Mayeur

Le Provost

Leboutte

Lebrun

Leclerc

Leclercq

Lecocq

Lecomte

Ledecq

Leenhard

Leenhart

Lefebvre

Lefèvre

Legrand

Lejeune

Lemaire

Lemmens

Lemonnier

Lemounie

Lenaerts

Lénel 

Lénelle

Lennel 

Léonard

Lepoutre

Leprette

Lepropre

Leroy

Lescohy

Lesoil

Lesoile 

Lesoille 

Levecq

Lewek

Libert

Liens

Liephoudt

Liepot

Liepout

Lieseborghs

Liesenborghs

Lietaer

Lietaert

Lietar

Liétar

Liétard

Liétart

Lievens

Lievesoons 

Lievevrouw 

Lievrouw

Liévrouw

Lievrow 

Linglay

Linglet

Liphout

Lisenborgh

Lisenborgs

Locreille 

Locrel

Locrelle 

Lode

Loo

Lorfèvre

Lorphêvre

Losseau

Losset

Louis

Louzeau

Lowie

Ludovicus

Lugen

Lugens 

Lust

Lustig

Luyer

Luyrik

Luyten

Lyphoudt 

Lyphout

M

Maca

Maertens

Maes

Maessen

Mahieu

Maka

Malchamp 

Malchamps 

Malmedier

Malmedy

Malmendier

Mangon

Maqua

Marchal

Marckx

Marcus

Mardaga

Maréchal

Maria

Mark

Markgraff

Martens

Martin

Martins

Massart

Masson

Mathieu

Mathissen

Mathy

Matthys

Mauchamp 

Mauchamps 

Maurichon

Maurissen

Maurits

Mayeur

Mayeux

Mechelaere

Meert

Meertens

Meester

Meeus

Melaerts 

Mellaerts

Merchié

Merchier

Mergeai

Mergeay

Merjai

Merjay

Mertens

Mertes

Merts 

Mertz 

Meulemans

Meulemeesters

Meunier

Meurice

Mewis

Mewissen

Michaël

Michaux

Michel

Michiels

Mixhel

Mochamps

Moens

Moeyaert 

Moiling

Moinil

Molemans

Molenaers

Monceau

Moncia

Monciaux

Monsay

Monteyne

Moreau

Mouyart

Moyaert 

Mullenders

Munck

Muynck

N

Nachtegael

Nagelmaekers

Nagels

Natus

Neel

Neels

Neuray

Neureau

Neuret

Neurot

Neuts 

Neuven

Neven

Nguyen

Nicolas

Nicolaus

Nicolus

Nijs

Niklaas

Noël

Nuts 

Nuttin

O

Ochin

Olivier

Olyff

P

Paindavaine

Pannaye

Parmentier

Pas

Pauss

Pauwels

Peeters

Pelser

Pelsmaeker

Peschon

Peschoniez

Pester

Petersen

Petit

Pierre

Piet

Pieters

Pietersen

Piette

Pirard

Piron

Pirotte

Plaats

Poels

Poelsmans

Poncelet

Pools

Posson

Potstainer

Potter

Pottiaux

Pottié

Potty

Poyon

Praat

Premereur 

Premmereur

Prevostel

Priesse

Prisse

Proost

Prost

Proust

Putmans

Putmans

Puttemans

Puttemans

Putman 

Q

Quaisin

Quesnay

Quesne

Quesneau

Quesnel

Quesney

Quesnoy

Queval

R

Raes

Ramael

Raucent

Rauscent

Rausin 

Raussain

Raussent

Raussin 

Raveydts

Ravignat

Remy

Renard

Retelet

Ricaart

Ricaert

Ricard

Robaert

Robbert

Robert

Roels

Roland

Rooseels

Roosengardt

Rosseel

Rousseau

S

Saintmaux 

Saint-Maux

Sanctorum

Santilman

Schmitz

Schnock

Schoenmakers

Schoenman

Schoone

Scorier

Scuvie

Scuvie

Segers

Seghers

Seppen

Servais

Shoen

Sijmen

Simoens

Simon

Simons

Sinnesaël

Sinnesal 

Slagmolder

Slagmulder

Slamulder

Smal

Smeets

Smet

Smets

Smit

Smolders

Smulders

Somers

Sottiaux

Spinette

Sprecher

Stas

Stass 

Stassaert 

Stassar 

Stassard 

Stassart 

Stasse 

Stassiaux 

Stassin 

Stassinet 

Statius 

Steculorum

Stefaans

Stercken

Sterckmans

Sterckx

Stevens

Stier

Stiers

Stievens

Stine

Stoffel

Stordair

Stordeur

Stoutmans

Swart

Swarte

T

Tack

Taverner

Teissant

Terreur

Thijs

Thiry

Thissen

Thomas

Thonnisen

Thuiliau

Thuiliaux

Thuiliet

Thys

Tibaut

Timmerman

Timmermans

T'Jampens

Tjampens

Toussaint

Trausch

Tuiliau

Tuiliaux

Tuilliet

Tuin

Tumson

Tweelinckx

U

Urbain

Urting

V

Van Acker

Van Aelter

Van Belle

Van Berckel

Van Bergh

Van Caenegem

Van Caeneghem

Van Daele

Van Damme

Van de Loo

Van de Pas 

Van de Poel

Van de Slijke

Van de Slycke

Van de Veld

Van de Velde

Van den Bergh

Van den Bogaerde

Van den Borne

Van den Bossche

Van den Broeck

Van den Broecke

Van den Camp

Van den Castele

Van den Dael

Van den Dorpe

Van den Tuin

Van Den

Van der Brug

Van der Gucht

Van der Pas 

Van der Slijke

Van der Slikke

Van der Slycke

Van der Vleuten 

Van Doren

Van Dorp

Van Dorpe

Van Dovlaeghe

Van Dyck

Van Engeland

Van Esch

Van Escht

Van Eyck

Van Hecke

Van Hoof

Van Hoorebeke

Van Hoorenbeeck

Van Horenbeck

Van Horenbeeck

 Van Lierde

Van Noye

Van Noÿe

Van Pé

Van Pede

Van Pée

Van Roy

Van Sinaey

Van Slijke

Van Slycke

Van Steerteghem

Van Steerteghen

Van Steirteghem

Van Vleuten 

Vanbattel

Vanbergh

Vandamme

Vandenberghe

Vandenbossche 

Vandenbussche

Vandendorpe

Vandeputte

Vanderhorst

Vanderlinden

Vanderplaetsen

Vandevelde

Vandoolaeghe

Vandorpe

Vanlierde

Vanpé

Vanpede

Vanpée

Vansteertegem

Vecq

Veld

Veldmann

Vellemans

Veraghe

Veraghen

Verbeeck

Verbeke

Verbruggen

Vercammen

Vercheval

Verdoolaeg(h)e

Verhaege

Verhaegen

Verhaeghe

Verhaeghen

Verhaegue

Verhage

Verhagen

Verhaghe

Verhelst

Verheyen

Verhoeven

Verlinden

Vermeer 

Vermeersch

Vermeiren

Vermeren 

Vermeulen

Vermotte 

Verplaetse

Verplancke

Verplancken

Verschueren

Verslijke

Verslycke

Verstraete

Verstraeten

Vervoort

Vet

Vette

Viatour

 Vieutemps 

Vieutems 

Vieuxtemps

Vilain 

Vincent 

Vinchent

Visje

Vlaamsche

Vlaeminck

Vlaemynck

Vlaminck

Vlamynck

Vlemincks

Vleminckx

Vleminx

Vlemynckx

Vogels

Volckaert

Volkaert

Volkaerts

Volkart

Volkert

Voller

Vos

Vossen

Vrank

Vrindt

Vrolijt

Vrolyck

Vullers

W

Wagemans

Wagenmann 

Waghon 

Wagon

Walle

Wastiaux 

Watrigant 

Watriquant 

Watteau 

Watteau

Watteaux 

Watteaux

Wattecamp 

Wattecamps

Wattecant 

Watteel

Wattel

Wattelle

Wattiau 

Wattiaux 

Wattieaux 

Wauters

Weers 

Weerts

Wek

Wevers

Weynen

Wilbaert

Wilfart

Willems

Willock

Willocq

Wilock

Wintgens

Wouter

Wouters

Wuyts

Wylock
Wylocke

Y

Yildirim
Yilmaz

Z

Zadelaar
Zegers
Zeggers
Zègres
"""


LAST_NAMES_FRANCE = u"""
Martin	236 172
Bernard	131 901
Thomas	119 078
Dubois	114 001
Durand	111 510
Robert	106 161
Moreau	103 056
Petit	95 876
Simon	95 733
Michel	93 581
Leroy	88 722
Laurent	85 243
Lefebvre	82 670
Bertrand	75 030
Roux	74 955
David	73 150
Garnier	67 829
Legrand	67 475
Garcia	67 162
Bonnet	66 124
Lambert	65 724
Girard	65 228
Morel	64 537
Andre	64 301
Dupont	63 520
Guerin	62 971
Fournier	61 770
Lefevre	61 662
Rousseau	58 884
Francois	58 409
Fontaine	57 783
Mercier	56 702
Roussel	56 300
Boyer	56 024
Blanc	54 714
Henry	54 212
Chevalier	53 741
Masson	52 966
Clement	51 177
Perrin	50 834
Lemaire	50 038
Dumont	49 834
Meyer	48 796
Marchand	47 763
Joly	47 337
Gauthier	47 218
Mathieu	47 178
Nicolas	46 761
Nguyen	46 605
Robin	46 329
Barbier	45 635
Lucas	44 369
Schmitt	44 128
Duval	44 075
Gerard	43 762
Noel	43 263
Gautier	42 411
Dufour	42 209
Meunier	41 833
Brunet	41 807
Blanchard	41 477
Leroux	41 162
Caron	40 845
Lopez	40 431
Giraud	39 896
Fabre	39 592
Pierre	39 469
Gaillard	39 260
Sanchez	39 133
Riviere	39 018
Renard	37 607
Perez	37 371
Renaud	37 274
Lemoine	37 222
Arnaud	37 173
Jean	36 901
Colin	36 289
Brun	36 159
Philippe	35 922
Picard	35 912
Rolland	35 870
Olivier	35 384
Vidal	34 737
Leclercq	34 630
Aubert	34 477
Hubert	34 429
Bourgeois	34 380
Roy	33 798
Guillaume	33 518
Adam	32 624
Dupuy	31 895
Louis	31 785
Maillard	31 752
Aubry	31 184
Charpentier	30 139
Benoit	30 055
Berger	29 640
Royer	29 425
Poirier	29 345
Dupuis	29 339
Rodriguez	29 330
Jacquet	29 274
Moulin	29 065
Charles	29 041
Lecomte	28 980
Deschamps	28 823
Fernandez	28 547
Guillot	28 526
Collet	28 333
Prevost	28 129
Germain	27 664
Bailly	27 588
Guyot	27 419
Perrot	27 293
Le gall	27 140
Renault	27 138
Le roux	26 551
Vasseur	26 431
Herve	26 272
Gonzalez	26 182
Barre	26 084
Breton	26 057
Huet	25 961
Bertin	25 960
Carpentier	25 809
Lebrun	25 749
Carre	25 435
Boucher	25 365
Menard	25 135
Rey	24 943
Klein	24 750
Weber	24 727
Collin	24 553
Cousin	24 314
Millet	24 310
Tessier	23 978
Leveque	23 737
Le goff	23 704
Lesage	23 599
Marchal	23 525
Leblanc	23 492
Bouchet	23 442
Etienne	23 413
Jacob	23 328
Humbert	23 315
Bouvier	23 290
Leger	23 273
Perrier	23 182
Pelletier	22 952
Remy	22 824
"""


FEMALE_FIRST_NAMES_FRANCE = u"""
Adélaïde, Adèle, Agnès, Alix, Béatrice, Beatrix, Elizabeth, Hélène, Héloïse, Isabeau, Iseult, Irène, Mahaut, Margot, Mathilde, Mélissende, Pétronille, Yolande,
Adèle, Aimée, Alice, Appoline, Augustine, Céleste, Célie, Emma, Élise, Églantine, Eugénie, Irène, Jeanne, Joséphine, Léopoldine, Léontine, Lucie, Louise, Madeleine, Mathilde, Ophélie, Pauline, Rose, Zoé,
Albanie, Alexine, Aglaé, Alina, Alma, Angèle, Appoline, Armance, Arthémise, Augustine, Blanche, Célestine, Colombe, Dina, Elia, Émerence, Eulalie, Eugénie, Félicie, Fleurine, Gracianne, Honorine, Jeanne, Léona, Léonie, Léontine, Lilly, Louise, Matilde, Noémi, Pétronille, Philomène, Rose, Salomée, Sidonie, Victoire, Victorine Zélie
"""

MALE_FIRST_NAMES_FRANCE = u"""
Ambroise, Amédée, Anastase, Arthur, Augustin, Aymeric, Béranger, Geoffroy, Grégoire, Guillaume, Léon, Louis, Théodore, Thibaut, Tristan,
Alfred, Alphonse, Amédée, Aristide, Augustin, Barthélémy, Cyprien, Eugène, Ferdinand, Félix, Gustave, Jules, Justin, Léon, Théophile, Victor, Virgile,
Abel, Achille, Aimé, Anatole, Anthime, Auguste, Augustin, Célestin, Edgar, Emile, Ernest, Faustin, Félix, Gaston, Gustave, Jules, Léon, Léopold, Louis, Marceau, Marius, Max, Melchior, Oscar, Philémon, Rubens, Sully, Théodore, Théophile, Victor, Victorin, Wilhem
"""

# copied from
# http://fr.wikipedia.org/w/index.php?title=Liste_des_rues_de_Li%C3%A8ge&action=edit
STREETS_OF_LIEGE = u"""
{{ébauche|Liège}}
Cet article dresse une liste (incomplète) des voies ([[voirie]]s et [[Place (voie)|places]]) de la [[Ville de Belgique|ville]] de [[Liège]] en [[Belgique]].

{{SommaireCompact}}

==2==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
*[[Place du 20-Août]]
</div>

==A==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">

* [[Rue de l'Abattoir]]
* [[Rue des Abeilles (Liège)|Rue des Abeilles]]
* [[Rue des Acacias (Liège)|Rue des Acacias]]
* [[Rue de l'Académie]]
* [[Avenue Albert Mahiels]]
* [[Rue Ambiorix]]
* [[Rue d'Amercoeur]]
* [[rue des Anglais (Liège)|Rue des Anglais]]
* [[Rue d'Ans]]
* [[Quai des Ardennes]]
* [[Rue Armand Stouls]]
* [[Rue Auguste Hock]]
* [[Rue des Augustins (Liège)|Rue des Augustins]]
* [[Impasse de l'Avenir]]
* [[Boulevard d'Avroy]]
* [[Rue d'Awans]]

</div>

==B==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[La Batte]]<ref>Batte signifiant ''quai'' en [[wallon]], on ne doit donc pas dire quai de la Batte</ref>
* [[Rue Basse-Wez]]
* [[Rue Beauregard (Liège)|Rue Beauregard]]
* [[Place des Béguinages]]
* [[Rue Bernimolin]]
* [[Rue Bidaut]]
* [[Avenue Blonden]]
* [[Rue Bois Gotha]]
* [[Quai Bonaparte]]
* [[Rue Bonne-Fortune]]
* [[Rue Bonne-Nouvelle]]
* [[Rue des Bons Enfants (Liège)|Rue des Bons Enfants]]
* [[Rue du Bosquet (Liège)|Rue du Bosquet]]
* [[Rue de la Boucherie (Liège)]]
* [[Quai de la Boverie]]
* [[Rue de Bruxelles (Liège)|Rue de Bruxelles]]
* [[Montagne de Bueren]]

</div>

==C==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Rue de Campine]]
* [[Rue des Carmes (Liège)|Rue des Carmes]]
* [[Place des Carmes]]
* [[Rue de la Casquette]]
* [[Place de la Cathédrale]]
* [[Rue de la Cathédrale]]
* [[Boulevard César Thomson]]
* [[Rue des Champs]]
* [[Rue Charles Bartholomez]]
* [[Rue Charles Magnette]]
* [[Avenue Rogier (Liège)|Avenue Charles Rogier]]
* [[Thier de la Chartreuse]]
* [[Rue de Chaudfontaine]]
* [[Rue Chauve-Souris (Liège)|Rue Chauve-Souris]]
* [[Rue de la Cité (Liège)|Rue de la Cité]]
* [[Rue des Clarisses]]
* [[Boulevard de la Constitution]]
* [[Rue du Coq]]
* [[Rue Counotte]]
* [[Rue Cour Petit]]
* [[Place Crèvecœur]]
* [[Rue des Croisiers]]
* [[Rue des Croix-de-Guerre]]
</div>

==D==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Rue Darchis]]
* [[Rue Dartois]]
* [[Rue Dehin]]
* [[Rue Denis Sotiau]]
* [[Rue Dony]]
* [[Rue Douffet]]
</div>

==E==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Boulevard Émile de Laveleye]]
* [[Avenue Émile Digneffe]]
* [[Rue Émile Gérard]]
* [[Rue Émile Vandervelde (Liège)|Rue Émile Vandervelde]]
* [[Rue En Bois]]
* [[Rue Ernest de Bavière]]
* [[Rue Ernest Solvay (Liège)|Rue Ernest Solvay]]
* [[Rue Éracle]]
* [[Rue Eugène Houdret]]
* [[Rue de l'Étuve (Liège)|Rue de l'Étuve]]
</div>

==F==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Féronstrée]]
* [[Rue de Fétinne]]
* [[Rue Fond Saint-Servais]]
* [[Rue fond des Tawes]]
* [[Rue des Fontaines-Roland]]
* [[Rue des Fossés]]
* [[Rue de Fragnée]]
* [[Place des Franchises]]
* [[Boulevard Frankignoul]]
* [[Ernest-Frédéric Nyst|Rue Frédéric Nyst]]
* [[Rue aux Frênes]]
* [[Boulevard Frère-Orban]]
</div>

==G==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Rue Gaston Laboulle]]
* [[Rue Gaucet]]
* [[Quai de Gaulle]]
* [[Rue du Général de Gaulle]]
* [[Rue du Général Bertrand]]
* [[Place du Général Leman]]
* [[Rue Georges Simenon]]
* [[Quai Godefroid Kurth]]
* [[Quai de la Goffe]]
* [[Rue de la Goffe]]
* [[Impasse Graindor]]
* [[Rue Gramme (Liège)|Rue Gramme]]
* [[Rue Grande Bêche]]
* [[Rue des Gravillons]]
* [[Rue Grétry (Liège)|Rue Grétry]]
* [[Rue du Gros Gland]]
* [[Place des Guillemins]]
* [[Rue des Guillemins]]
</div>

==H==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Rue de la Halle]]
* [[Rue de Harlez]]
* [[Rue d'Harscamp]]
* [[Rue du Haut-Pré]]
* [[Place du Haut-Pré]]
* [[Rue Hazinelle]]
* [[Rue Henri Baron]]
* [[Rue Henri Koch (Liège)|Rue Henri Koch]]
* [[Rue Henri Maus (Liège)|Rue Henri Maus]]
* [[Rue Herman Reuleaux]]
* [[Rue de Hesbaye]]
* [[Rue Hocheporte]]
* [[Rue Hors-Château]]
* [[Rue des Houblonnières]]
* [[Rue Hullos]]
</div>

==I==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Place d'Italie (Liège)|Place d'Italie]]
* [[Rue des Ixellois]]
</div>

==J==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Rue Jambe de Bois]]
* [[Rue du Jardin Botanique]]
* [[Rue Jean Bury]]
* [[Rue Jean d'Outremeuse]]
* [[Rue Jean Haust]]
* [[Rue Joffre]]
* [[Rue de Joie]]
* [[Rue Jonckeu]]
* [[Rue Jondry]]
* [[Rue des Jonquilles (Liège)|Rue des Jonquilles]]
* [[Place Joseph de Bronckart]]
* [[Rue Joseph Demoulin]]
* [[Rue Joseph Henrion]]
* [[Rue Joseph Lacroix]]
* [[Rue Joseph Wauters (Liège) |Rue Joseph Wauters]]

</div>

==L==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Rue Lairesse]]
* [[Rue de Lantin]]
* [[Rue du Laveu (Liège)|Rue du Laveu]]
* [[Rue de la Légia]]
* [[Rue Lemille]]
* [[Passage Lemonnier]]
* [[Rue Léon Mignon (Liège)|Rue Léon Mignon]] 
* [[Rue Léopold]]
* [[Rue Libotte]]
* [[Rue de Londres (Liège)|Rue de Londres]]
* [[Quai de Longdoz]]
* [[Rue Louis Abry]]
* [[Rue Louis Fraigneux]]
* [[Rue Louvrex]]
* [[Avenue du Luxembourg]]
</div>

==M==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Quai de Maestricht]]
* [[Rue des Maraîchers (Liège)|Rue des Maraîchers]]
* [[Place du Marché (Liège)|Place du Marché]]
* [[Quai Marcellis]]
* [[Quai Mativa]]
* [[Avenue Maurice Destenay]]
* [[Rue Méan]]
* [[Quai sur Meuse]]
* [[Rue Mississippi]] 
* [[Rue du Mont Saint-Martin]]
* [[Rue Montagne Sainte-Walburge]]
</div>

==N==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Rue de Namur]]
* [[Rue Naniot]]
* [[Rue Natalis]]
* [[Place des Nations-Unies (Liège)|Place des Nations-Unies]]
* [[En Neuvice]]
</div>

==O==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Place de l'Opéra (Liège)|Place de l'Opéra]]
* [[Quai Orban]]
* [[Rue Oscar Rémy]]
* [[Quai de l'Ourthe]]
</div>

==P==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Rue Paradis (Liège)|Rue Paradis]]
* [[Rue du Parc]]
* [[Rue du Palais (Liège)|Rue du Palais]]
* [[Rue de Paris (Liège)|Rue de Paris]]
* [[Au Péri]]
* [[Boulevard Piercot]]
* [[Rue Pierreuse]]
* [[Rue du Plan Incliné]]
* [[Rue Plumier]]
* [[Rue Pont-d'Avroy]]
* [[Rue Pont-d'Ile]]
* [[Rue du Pot d'Or]]
* [[Potiérue]]
* [[Rue des Prébendiers]]
* [[Rue Publémont]]
* [[Rue Puits-en-Sock]]
* [[Rue du Puits]]
</div>

==R==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Rue des Récollets (Liège)|Rue des Récollets]]
* [[Rue de la Régence (Liège)|Rue de la Régence]]
* [[Rue Regnier-Poncelet (Liège)|Rue Regnier-Poncelet]]
* [[Avenue Reine Elisabeth]]
* [[Rue des Remparts]]
* [[Place de la République française]]
* [[Rue de la Résistance]]
* [[Quai de la Ribuée]]
* [[Rue des Rivageois]]
* [[Rue Robertson]]
* [[Quai de Rome]]
* [[Quai Roosevelt]]
* [[Rue Roture]]
</div>

==S==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Place Saint-Barthélemy]]
* [[Place Saint-Denis]]
* [[Rue Saint-Gilles (Liège)|Rue Saint-Gilles]]
* [[Place Saint-Jacques (Liège)|Place Saint-Jacques]]
* [[Place Saint-Lambert (Liège)|Place Saint-Lambert]]
* [[Rue Saint-Laurent (Liège)|Rue Saint-Laurent]]
* [[Esplanade Saint-Léonard (Liège)|Esplanade Saint-Léonard]]
* [[Rue Saint-Léonard]]
* [[Rue Sainte-Marie (Liège)|Rue Sainte-Marie]]
* [[Rue Saint-Martin-en-Île]]
* [[Place Saint-Michel (Liège)|Place Saint-Michel]]
* [[Rue Saint-Michel (Liège)|Rue Saint-Michel]]
* [[Place Saint-Paul (Liège)|Place Saint-Paul]]
* [[Rue Saint-Paul (Liège)|Rue Saint-Paul]]
* [[Rue Saint-Pierre (Liège)|Rue Saint-Pierre]]
* [[Rue Saint-Remacle]]
* [[Rue Saint-Remy]]
* [[Rue Saint-Séverin (Liège)|Rue Saint-Séverin]]
* [[Rue Sainte-Croix]]
* [[Rue Sainte-Marguerite (Liège)|Rue Sainte-Marguerite]]
* [[Place Sainte-Véronique]]
* [[Rue Sainte-Véronique]]
* [[Rue Sainte-Walburge]]
* [[Boulevard Saucy]]
* [[Boulevard de la Sauvenière]]
* [[Rue de Sclessin]]
* [[Rue de Seraing]]
* [[Rue de la Sirène]]
* [[Rue Soubre]]
* [[Rue Sous l'Eau]]
* [[Rue de Spa (Liège)|Rue de Spa]]
* [[Rue Stappers]]
* [[Rue de Stavelot]]
* [[Rue Suavius]]
</div>

==T==
<div style="-moz-column-count:3; column-count:3; -webkit-column-count:3;">
* [[Quai des Tanneurs]]
* [[Rue des Tanneurs (Liège)|Rue des Tanneurs]]
* [[Rue des Tawes]]
* [[Rue du Terris (Liège)|Rue du Terris]]
* [[Place du Tertre (Liège)|Place du Tertre]]
* [[Rue du Thier-à-Liège]]
* [[Chaussée de Tongres]]
* [[Rue Tournant Saint-Paul]]
* [[Rue Toussaint Beaujean]]
</div>

* [[Rue de l'Université (Liège)|Rue de l'Université]]
* [[Rue des Urbanistes]]
* [[Impasse des Ursulines (Liège)|Impasse des Ursulines]]

* [[Rue Valdor]]
* [[Quai Édouard van Beneden]]
* [[Rue Varin]]
* [[Rue des Vennes]]
* [[Rue du Vertbois (Liège)|Rue du Vertbois]]
* [[Rue du Vieux Mayeur]]
* [[Impasse du Vieux Pont des Arches]]
* [[Rue Villette]]
* [[Vinâve d'Île]]<ref>Vinâve signifiant ''artère principale'' en [[wallon]], on ne doit donc pas dire rue du Vinâve d'Île</ref>
* [[Rue Volière (Liège)|Rue Volière]]

* [[Rue des Wallons (Liège)|Rue des Wallons]]
* [[Rue de Waroux]]
* [[Rue de Wazon]]
* [[Rue de Wetzlar]]
* [[Rue Wiertz (Liège)|Rue Wiertz]]

* [[Place Xavier Neujean]]


"""

MALE_FIRST_NAMES_MUSLIM = u"""
Aabdeen
Aabid
Aadam
Aadil
Aaish
Aakif
Aamir
Aaqil
Aarif
Aasim
Aatif
Aayid
Abbaad
Abbaas
Abdul Azeez
Abdul Baari
Abdul Baasid
Abdul Fattaah
Abdul Ghafoor
Abdul Ghani
Abdul Haadi
Abdul Hai
Abdul Hakeem
Abdul Haleem
Abdul Hameed
Abdul Jabbaar
Abdul Jaleel
Abdul Kader
Abdul Kareem
Abdul Khaliq
Abdul Lateef
Abdul Maalik
Abdul Majeed
Abdul Noor
Abdul Qayyoom
Abdul Quddoos
Abdul Rauf
Abdul Waahid
Abdul Wadood
Abdul Wahaab
Abdullah
Abdur Raheem
Abdur Rahmaan
Abdur Raqeeb
Abdur Rasheed
Abdur Razzaaq
Abdus Salam
Abdus Samad
Abdut Tawwab
Abood
Abyad
Adeeb
Adham
Adnaan
Afeef
Ahmed
Aiman
Akram
Alawi
Ali
Amaan
Amaanullah
Ameen
Ameer
Amjad
Ammaar
Amru
Anas
Annnees
Anwar
Aqeel
Arafaat
Arhab
Arkaan
Arshad
Asad
Aseel
Asghar
Ashqar
Ashraf
Aslam
Asmar
Awad
Awf
Awn
Awni
Ayyoob
Azhaar
Azmi
Azzaam
Baahir
Baaqir
Baasim
Badr
Badraan
Badri
Badruddeen
Baheej
Bakar
Bandar
Basheer
Bassaam
Bassil
Bilaal
Bishr
Burhaan
Daamir
Daawood
Daif
Daifallah
Daleel
Dhaafir
Dhaahir
Dhaakir
Dhaki
Dhareef
Faadi
Faadil
Faai Z
Faaid
Faaiq
Faalih
Faaris
Faarooq
Faatih
Faatin
Fahd
Faheem
Fahmi
Faisal
Faraj
Farajallah
Fareed
Farhaan
Fateen
Fat'hi
Fawwaaz
Fawz
Fawzi
Fayyaad
Fikri
Fuaad
Furqaan
Ghaali
Ghaalib
Ghaamid
Ghaazi
Ghassaan
Haafil
Haajid
Haamid
Haani
Haarith
Haaroon
Haashid
Haashim
Haatim
Haazim
Haitham
Hakam
Hamad
Hamdaan
Hamdi
Hamood
Hamza
Haneef
Hanlala
Hasan
Hazm
Hibbaan
Hilaal
Hilmi
Hishaam
Hudhaifa
Humaid
Humaidaan
Huraira
Husaam
Husain
Husni
Ibrahim
Idrees
Ihaab
Ikram
Ilyaas
Imaad
Imraan
Irfaan
Isaam
Ishaaq
Ismad
Ismaeel
Iyaad
Izzaddeen
Izzat
Jaabir
Jaad
Jaadallah
Jaarallah
Jaasim
Jaasir
Jafar
Jalaal
Jam,Aan
Jamaal
Jameel
Jareer
Jasoor
Jawaad
Jawhar
Jihaad
Jiyaad
Jubair
Jumail
Junaid
Kaalim
Kaamil
Kaarim
Kabeer
Kaleem
Kamaal
Kamaaluddeen
Kameel
Kanaan
Katheer
Khaalid
Khairi
Khaleefa
Khaleel
Labeeb
Labeeb
Luqmaan
Lutfi
Luwai
Ma,Roof
Maahir
Maaiz
Maa'iz
Maajid
Maazin
Mahboob
Mahdi
Mahfooz
Mahmood
Mahuroos
Maisara
Maisoon
Majdi
Mamdooh
Mamoon
Mansoor
Marwaan
Marzooq
Mashal
Masood
Mastoor
Mawdood
Mazeed
Miqdaad
Miqdaam
Misfar
Mishaari
Moosha
Mu,Aawiya
Muaaid
Muammar
Mubarak
Mubashshir
Mudrik
Mufeed
Muhaajir
Muhammad
Muhsin
Muhyddeen
Mujahid
Mukarram
Mukhtaar
Mundhir
Muneeb
Muneef
Muneer
Munjid
Munsif
Muntasir
Murshid
Musaaid
Mus'ab
Musaddiq
Musheer
Mushtaaq
Muslih
Muslim
Mustaba
Mutammam
Mutasim
Mu'taz
Muthanna
Mutlaq
Muzammil
Naadir
Naaif
Naaji
Naasif
Naasiruddeen
Naazil
Naazim
Nabeeh
Nabeel
Nadeem
Nadheer
Najeeb
Najeem
Naseem
Naseer
Nashat
Nassaar
Nawaar
Nawf
Nawfal
Nazmi
Neeshaan
Nizaam
Nizaar
Noori
Nu'maan
Numair
Qaaid
Qaasim
Qais
Quraish
Qutb
Raadi
Raafi
Raaid
Raaji
Raakaan
Raamiz
Raashid
Rabi
Rafeeq
Raihaan
Rajaa
Rajab
Ramalaan
Ramzi
Rashaad
Rasheeq
Rayyaan
Razeen
Rida
Ridwaan
Rifaah
Rifat
Riyaal
Rushdi
Rushdi
Ruwaid
Saabiq
Saabir
Saadiq
Saahir
Saajid
Saalih
Saalim
Saami
Saamir
Sabaah
Sabri
Sad
Sadi
Sadoon
Saeed
Safar
Safwaan
Sahl
Saif
Sakeen
Salaah
Saleel
Saleem
Saleet
Salmaan
Samir
Saood
Saqr
Shaafi
Shaaheen
Shaahir
Shaakir
Shaamikh
Shaamil
Shabaan
Shaddaad
Shafeeq
Shaheed
Shaheed
Shaheer
Shakeel
Shameem
Shaqeeq
Sharaf
Sharaf
Shawqi
Shihaab
Shuaib
Shujaa
Shukri
Shuraih
Siddeeqi
Sidqi
Silmi
Siraaj
Sirajuddeen
Subhi
Sufyaan
Suhaib
Suhail
Sulaimaan
Sultan
Suwailim
Taaha
Taahir
Taaj
Taajuddeen
Taalib
Taamir
Taariq
Taiseer
Talaal
Talha
Tameem
Tammaam
Taqi
Tareef
Tawfeeq
Tawheed
Tayyib
Thaamir
Thaaqib
Tufail
Turki
Ubaida
Umair
Umar
Unais
Uqbah
Usaama
Uthmaa N
Uwais
Waail
Waatiq
Waddaah
Wajdi
Wajeeb
Wajeeh
Waleed
Waseef
Waseem
Wisaam
Yaasir
Ya'eesh
Yahya
Ya'qoob
Yoonus
Yoosuf
Yusri
Zaahid
Zaahir
Zaaid
Zaamil
Zaghlool
Zaid
Zaidaan
Zain
Zainuddeen
Zakariyya
Zaki
Zameel
Zayyaan
Ziyaad
Zubair
Zufar
Zuhair
Zuraara
"""

FEMALE_FIRST_NAMES_MUSLIM = u"""
Aadila
Aaida
Aaisha
Aamina
Aanisa
Aarifa
Aasima
Aasiya
Aatifa
Aatika
Aayaat
Abeer
Adeeba
Adhraaa
Afaaf
Afeefa
Afnaan
Afraah
Ahlaam
Aliyya
Almaasa
Amaani
Amal
Amatullah
Ameena
Ameera
Amniyya
Anbara
Aneesa
Aqeela
Ariyya
Arwa
Aseela
Asmaa
Atheer
Atiyya
Awaatif
Awda
Azeema
Azeeza
Azza
Fakeeha
Faraah
Fareeda
Farha
Farhaana
Farhat
Faseeha
Fateena
Fat'hiyaa
Fawqiyya
Fawzaana
Fawzia
Fidda
Fikra
Fikriyya
Firdaus
Fuaada
Gaitha
Ghaada
Ghaaliba
Ghaaliya
Ghaaziya
Ghaidaa
Ghazaala
Ghuzaila
Haafiza
Haajara
Haakima
Haala
Haamida
Haaniya
Haaritha
Haazima
Habeeba
Hadbaaa
Hadeel
Hadiyya
Hafsa
Haibaa
Haifaaa
Hakeema
Haleema
Hamaama
Hamda
Hamdoona
Hameeda
Hamna
Hamsa
Hanaaa
Hanaan
Haniyya
Hanoona
Hasana
Haseena
Hasnaa
Hawraa
Hazeela
Hiba
Hikma
Hilmiyya
Himma
Hishma
Hissa
Hiwaaya
Huda
Hujja
Humaina
Humaira
Husniyya
Huwaida
Ibtisaama
Iffat
Ilhaam
Imtinaan
Inaaya
Insaaf
Intisaar
Israa
Izza
Jadeeda
Jaleela
Jameela
Jannat
Jasra
Jawhara
Jeelaan
Juhaina
Jumaana
Jumaima
Juwairiya
Kaatima
Kaazima
Kabeera
Kameela
Kareema
Kawkab
Kawthar
Khaalida
Khadeeja
Khaira
Khairiya
Khaleela
Khawla
Khulood
Kifaaya
Kinaana
Kulthum
Laaiqa
Labeeba
Laila
Lateefa
Layaali
Lubaaba
Lubna
Lutfiyya
Maajida
Maariya
Maazina
Madeeha
Mahaa
Mahbooba
Mahdeeya
Mahdhoodha
Mahfoodha
Mahmooda
Maimoona
Maisara
Majdiyya
Majeeda
Maleeha
Maleeka
Manaahil
Manaal
Manaara
Mardiyya
Marjaana
Marwa
Marzooqa
Mas'ooda
Masroora
Mastoora
Mawhiba
Mawzoona
Mayyaada
Mazeeda
Minnah
Misbaah
Miska
Mubaaraka
Mubeena
Mudrika
Mufeeda
Mufliha
Muhjar
Mu'hsina
Mujaahida
Mumina
Mu'mina
Mumtaaza
Muna
Muneefa
Muneera
Munisa
Muntaha
Musfira
Musheera
Mushtaaqa
Mutee'a
Muzaina
Muzna
Naadiya
Naafoora
Naaifa
Naaila
Nabeeha
Nabeela
Nada
Nadeera
Nadheera
Nadiyya
Nafeesa
Nahla
Najaat
Najeeba
Najeema
Najiyya
Najlaa
Najma
Najwa
Nakheel
Nameera
Naqaa
Naqiyya
Naseeba
Naseefa
Naseema
Naseera
Nasreen
Nawaal
Nawaar
Nawfa
Nawwaara
Nazeeha
Nazeema
Nazmiyya
Nisma
Noora
Nooriyya
Nuha
Nu'ma
Nusaiba
Nuzha
Qaaida
Qamraaa
Qisma
Raabia
Raabiya
Raadiya
Raafida
Raaida
Raaniya
Rabdaa
Radiyya
Radwa
Rafeeda
Rafeeqa
Raheema
Rahma
Raihaana
Raita
Ramla
Ramza
Ramziyya
Randa
Rashaa
Rasheeda
Rasheeqa
Rawda
Rayyana
Razeena
Reema
Rif'a
Rifqa
Rihaab
Rumaana
Ruqayya
Rutaiba
Ruwaida
Saabiqa
Saabira
Saafiyya
Saahira
Saajida
Saaliha
Saalima
Saamiqa
Saamyya
Saara
Sabaaha
Sabeeha
Sabeeka
Sabiyya
Sabreen
Sabriyya
Sadeeda
Sadeeqa
Safaaa
Safiyya
Safwa
Sahar
Sahheeda
Sahla
Sajaa
Sajiyya
Sakeena
Saleema
Salma
Salwa
Sameeha
Sameera
Samraa
Sanaaa
Sanad
Sawada
Shaafia
Shaahida
Shaahira
Shaakira
Shaamila
Shabeeba
Shadhaa
Shafaaa
Shafee'a
Shafeeqa
Shahaada
Shahaama
Shaheera
Shahla
Shaimaaa
Shajee'a
Shakeela
Shakoora
Sham'a
Shamaail
Shameema
Shaqeeqa
Shareefa
Shukriyya
Siddeeqa
Sireen
Sitaara
Suhaa
Suhaad
Suhaila
Sukaina
Sulama
Sultana
Sumaita
Sumayya
Sumbula
Sundus
Taaliba
Taamira
Tahaani
Tahiyya
Tahleela
Tamanna
Tameema
Taqiyya
Tareefa
Tasneem
Tawfeeqa
Tawheeda
Tayyiba
Thaabita
Thaamira
Thamra
Thanaa
Tharwa
Tuhfa
Tulaiha
Turfa
Ulyaa
Umaima
Umaira
Ummu Kulthoom
Urwa
Waajida
Wadee'a
Wadha
Wafaaa
Waheeba
Waheeda
Wajdiyya
Wajeeha
Waleeda
Waliyya
Waneesa
Warda
Wardiyya
Waseema
Wasmaaa
Widdad
Yaasmeen
Yaasmeena
Zaahira
Zaaida
Zahra
Zahraaa
Zainab
Zaitoona
Zakiyya
Zarqaa
Zeena
Zubaida
Zuhaira
Zuhra
Zuhriyaa
Zulfa
Zumruda
"""

LAST_NAMES_AFRICAN = u"""
Ba
Bah
Ballo
Chahine
Cisse
Congo
Contee
Conteh
Dia
Diallo
Diop
Fall
Fofana
Gueye
Jalloh
Keita
Kone
Maalouf
Mensah
Ndiaye
Nwosu
Okafor
Okeke
Okoro
Osei
Owusu
Sall
Sane
Sarr
Sesay
Sow
Sy
Sylla
Toure
Traore
Turay
Yeboah
"""

LAST_NAMES_MUSLIM = u"""
Abad
Abbas
Abbasi
Abdalla
Abdallah
Abdella
Abdelnour
Abdelrahman
Abdi
Abdo
Abdoo
Abdou
Abdul
Abdulla
Abdullah
Abed
Abid
Abood
Aboud
Abraham
Abu
Adel
Afzal
Agha
Ahmad
Ahmadi
Ahmed
Ahsan
Akbar
Akbari
Akel
Akhtar
Akhter
Akram
Alam
Ali
Allam
Allee
Alli
Ally
Aly
Aman
Amara
Amber
Ameen
Amen
Amer
Amin
Amini
Amir
Amiri
Ammar
Ansari
Anwar
Arafat
Arif
Arshad
Asad
Ashraf
Aslam
Asmar
Assad
Assaf
Atallah
Attar
Awan
Aydin
Ayoob
Ayoub
Ayub
Azad
Azam
Azer
Azimi
Aziz
Azizi
Azzam
Azzi
Bacchus
Baccus
Bacho
Baddour
Badie
Badour
Bagheri
Bahri
Baig
Baksh
Baluch
Bangura
Barakat
Bari
Basa
Basha
Bashara
Basher
Bashir
Baten
Begum
Ben
Beshara
Bey
Beydoun
Bilal
Bina
Burki
Can
Chahine
Dada
Dajani
Dallal
Daoud
Dar
Darwish
Dawood
Demian
Dia
Diab
Dib
Din
Doud
Ebrahim
Ebrahimi
Edris
Eid
Elamin
Elbaz
El-Sayed
Emami
Fadel
Fahmy
Fahs
Farag
Farah
Faraj
Fares
Farha
Farhat
Farid
Faris
Farman
Farooq
Farooqui
Farra
Farrah
Farran
Fawaz
Fayad
Firman
Gaber
Gad
Galla
Ghaffari
Ghanem
Ghani
Ghattas
Ghazal
Ghazi
Greiss
Guler
Habeeb
Habib
Habibi
Hadi
Hafeez
Hai
Haidar
Haider
Hakeem
Hakim
Halaby
Halim
Hallal
Hamad
Hamady
Hamdan
Hamed
Hameed
Hamid
Hamidi
Hammad
Hammoud
Hana
Hanif
Hannan
Haq
Haque
Hares
Hariri
Harron
Harroun
Hasan
Hasen
Hashem
Hashemi
Hashim
Hashmi
Hassan
Hassen
Hatem
Hoda
Hoque
Hosein
Hossain
Hosseini
Huda
Huq
Husain
Hussain
Hussein
Ibrahim
Idris
Imam
Iman
Iqbal
Irani
Ishak
Ishmael
Islam
Ismael
Ismail
Jabara
Jabbar
Jabbour
Jaber
Jabour
Jafari
Jaffer
Jafri
Jalali
Jalil
Jama
Jamail
Jamal
Jamil
Jan
Javed
Javid
Kaba
Kaber
Kabir
Kader
Kaiser
Kaleel
Kalil
Kamal
Kamali
Kamara
Kamel
Kanan
Karam
Karim
Karimi
Kassem
Kazemi
Kazi
Kazmi
Khalaf
Khalid
Khalifa
Khalil
Khalili
Khan
Khatib
Khawaja
Koroma
Laham
Latif
Lodi
Lone
Madani
Mady
Mahdavi
Mahdi
Mahfouz
Mahmood
Mahmoud
Mahmud
Majeed
Majid
Malak
Malek
Malik
Mannan
Mansoor
Mansour
Mansouri
Mansur
Maroun
Masih
Masood
Masri
Massoud
Matar
Matin
Mattar
Meer
Meskin
Miah
Mian

Mina
Minhas
Mir
Mirza
Mitri
Moghaddam
Mohamad
Mohamed
Mohammad
Mohammadi
Mohammed
Mohiuddin
Molla
Momin
Mona
Morad
Moradi
Mostafa
Mourad
Mousa
Moussa
Moustafa
Mowad
Muhammad
Muhammed
Munir
Murad
Musa
Mussa
Mustafa
Naderi
Nagi
Naim
Naqvi
Nasir
Nasr
Nasrallah
Nasser
Nassif
Nawaz
Nazar
Nazir
Neman
Niazi
Noor
Noorani
Noori
Nour
Nouri
Obeid
Odeh
Omar
Omer
Othman
Ozer
Parsa
Pasha
Pashia
Pirani
Popal
Pour
Qadir
Qasim
Qazi
Quadri
Raad
Rabbani
Rad
Radi
Radwan
Rafiq
Rahaim
Rahaman
Rahim
Rahimi
Rahman
Rahmani
Rais
Ramadan
Ramin
Rashed
Rasheed
Rashid
Rassi
Rasul
Rauf
Rayes
Rehman
Rehmann
Reza
Riaz
Rizk
Saab
Saad
Saade
Saadeh
Saah
Saba
Saber
Sabet
Sabir
Sadek
Sader
Sadiq
Sadri
Saeed
Safar
Safi
Sahli
Saidi
Sala
Salaam
Saladin
Salah
Salahuddin
Salam
Salama
Salame
Salameh
Saleem
Saleh
Salehi
Salek
Salem
Salih
Salik
Salim
Salloum
Salman
Samaan
Samad
Samara
Sami
Samra
Sani
Sarah
Sarwar
Sattar
Satter
Sawaya
Sayed
Selim
Semaan
Sesay
Shaban
Shabazz
Shad
Shaer
Shafi
Shah
Shahan
Shaheed
Shaheen
Shahid
Shahidi
Shahin
Shaikh
Shaker
Shakir
Shakoor
Sham
Shams
Sharaf
Shareef
Sharif
Shariff
Sharifi
Shehadeh
Shehata
Sheikh
Siddiqi
Siddique
Siddiqui
Sinai
Soliman
Soltani
Srour
Sulaiman
Suleiman
Sultan
Sultana
Syed
Sylla
Tabatabai
Tabet
Taha
Taheri
Tahir
Tamer
Tariq
Tawil
Toure
Turay
Uddin
Ullah
Usman
Vaziri
Vohra
Wahab
Wahba
Waheed
Wakim
Wali
Yacoub
Yamin
Yasin
Yassin
Younan
Younes
Younis
Yousef
Yousif
Youssef
Yousuf
Yusuf
Zadeh
Zafar
Zaher
Zahra
Zaidi
Zakaria
Zaki
Zaman
Zamani
Zia

"""

FEMALE_FIRST_NAMES_AFRICAN = u"""
Aba
Abeni
Abiba
Abmaba
Aissa
Ajua
Akosua
Armani
Arziki
Asha
Ashanti
Ayana
Baako
Beyonce
Bisa
Cacey
Cassietta
Catava
Chipo
Cleotha
Deiondre
Deka
Delu
Dericia
Diara
Doli
Dumi
Ebere
Ekua
Faizah
Fola
Gaynelle
Habika
Hawa
Isoke
Jendayi
Jira
Kabibe
Kabira
Kacela
Kacondra
Kadija
Kainda
Kambo
Kande
Kanene
Kanesha
Kanoni
Kapera
Kapuki
Karasi
Karimah
Karna
Kasinda
Keeya
Keilantra
Keisha
Keishla
Kendis
Kenyatta
Keshia
Keshon
Kesia
Keyah
Kia
Kianga
Kiden
Kiho
Kijana
Kinfe
Kione
Kirabo
Kiros
Kumani
Kuron
Kwashi
Kya
Lachelle
Lakin
Lanelle
Laquanna
Laqueta
Laquinta
Laquita
Lashawn
Latanya
Lateefah
Latifah
Latonya
Latoya
Layla
Lehana
Lewa
Lilovarti
Limber
Lisimba
Loba
Lolovivi
Lulu
Maha
Mahari
Mahdi
Maisha
Maizah
Malaika
Malkia
Mandisa
Manyara
Marjani
Mekell
Messina
Moesha
Muncel
Nafuna
Nailah
Naja
Najwa
Nakeisha
Nala
Narkaesha
Nasha
Nashaly
Nichelle
Niesha
Nimeesha
Nyeki
Okal
Okapi
Onaedo
Ontibile
Paka
Panya
Pasua
Pedzi
Pemba
Penda
Pita
Quanella
Quanesha
Quisha
Raimy
Ranielle
Rashida
Raziya
Ronnell
Safara
Safiya
Saidah
Salihah
Sekai
Semira
Serwa
Sesen
Shakila
Shakina
Shandra
Shaquana
Shasa
Shasmecka
Shateque
Sibongile
Sidone
Sika
Sima
Sitembile
Siyanda
Sukutai
Taifa
Taja
Takala
Takiyah
Talaitha
Tale
Talisa
Talisha
Tamasha
Tamika
Tamira
Tamyra
Tanasha
Tandice
Tanesha
Tanginika
Taniel
Tanisha
Tapanga
Tarana
Tariana
Tarisai
Tazara
Temima
Tendai
Terehasa
Thandiwe
Thema
Tiaret
Timberly
Tineka-Jawana
Tiombe
Tyesha
Tyrell
Tyrina
Tyronica
Uchenna
Ulu
Urbi
Uwimana
Velinda
Wangari
Waseme
Wyetta
Yaa
Yetty
Zabia
Zaci
Zahwa
Zaila
Zaire
Zakiya
Zalika
Zanta
Zarina
Zasu
Zawadi
Zilli
Zina
Zoila
"""

MALE_FIRST_NAMES_AFRICAN = u"""
Afram
Arali
Armani
Banji
Chata
Chiamaka
Chike
Dakarai
Deion
Deiondre
Dele
Dembe
Denzel
Dewayne
Diallo
Dikembe
Duante
Dume
Ebi
Essien
Faraji
Ibeamaka
Jamar
Jayvyn
Jevonte
Kabonero
Kabonesa
Kadeem
Kaleb
Kasi
Kendis
Kentay
Keshawn
Khalon
Kofi
Kwamin
Kwau
Kyan
Kyrone
Lado
Laken
Lakista
Lamech
Lavaughn
La Vonn
LeBron
Lisimba
Ludacris
Lugono
Luister
Lukman
Mablevi
Mahdi
Makalo
Manu
Marques
Mashawn
Montraie
Mykelti
Nabulung
Naeem
Naftali
Napoleon
Nuru
Nwa
Obiajulu
Oja
Okal
Okapi
Okoth
Onaedo
Ontibile
Oringo
Orma
Otieno
Paulo
Peabo
Penda
Phornello
Polo
Quaashie
Quaddus
Quadrees
Quannell
Quarren
Quashawn
Quintavius
Quoitrel
Raimy
Rashon
Razi
Roshaun
Runako
Salim
Shaquille
Shevon
Shontae
Simba
Sulaiman
Tabansi
Tabari
Tamarius
Tavarius
Tavon
Tevaughn
Tevin
Trory
Tyrell
Uba
Ubanwa
Udenwa
Ulan
Uland
Umi
Useni
Usi
Uzoma
Uzondu
Vandwon
Vashon
Veltry
Verlyn
Voshon
Vul
Wasaki
Xayvion
Xhosas
Xyshaun
Yobachi
Zaid
Zareb
Zashawn
"""

STREETS_OF_EUPEN = u"""\
Aachener Straße
Akazienweg
Alter Malmedyer Weg
Am Bahndamm
Am Berg
Am Waisenbüschchen
Auenweg
Auf dem Spitzberg
Auf'm Rain
August-Thonnar-Str.
Bahnhofsgasse
Bahnhofstraße
Bellmerin
Bennetsborn
Bergkapellstraße
Bergstraße
Binsterweg
Brabantstraße
Buchenweg
Edelstraße
Euregiostraße
Favrunpark
Feldstraße
Fränzel
Gewerbestraße
Gospert
Gülcherstraße
Haagenstraße
Haasberg
Haasstraße
Habsburgerweg
Heidberg
Heidgasse
Heidhöhe
Herbesthaler Straße
Hisselsgasse
Hochstraße
Hook
Hostert
Hufengasse
Hugo-Zimmermann-Str.
Hütte
Hütterprivatweg
Im Peschgen
In den Siepen
Industriestraße
Johannesstraße
Judenstraße
Kaperberg
Kaplan-Arnolds-Str.
Karl-Weiß-Str.
Kehrweg
Kirchgasse
Kirchstraße
Klinkeshöfchen
Kügelgasse
Langesthal
Lascheterweg
Limburgerweg
Lindenweg
Lothringerweg
Malmedyer Straße
Maria-Theresia-Straße
Marktplatz
Monschauer Straße
Mühlenweg
Neustraße
Nikolausfeld
Nispert
Noereth
Obere Ibern
Obere Rottergasse
Oestraße
Olengraben
Panorama
Paveestraße
Peter-Becker-Str.
Rosenweg
Rot-Kreuz-Str.
Rotenberg
Rotenbergplatz
Schilsweg
Schlüsselhof
Schnellewindgasse
Schönefeld
Schorberg
Schulstraße
Selterschlag
Simarstraße
Steinroth
Stendrich
Stockbergerweg
Stockem
Theodor-Mooren-Str.
Untere Ibern
Vervierser Straße
Vossengasse
Voulfeld
Werthplatz
Weserstraße
"""


def streets_of_eupen():
    r"""Yield an almost complete list of street names in Eupen.

    >>> for s in list(streets_of_eupen())[:5]:
    ...     print(s)
    Aachener Straße
    Akazienweg
    Alter Malmedyer Weg
    Am Bahndamm
    Am Berg

    """
    for ln in STREETS_OF_EUPEN.splitlines():
        ln = ln.strip()
        if ln:
            yield ln


def streets_of_liege():
    """Yield an almost complete list of street names in Liège.

    >>> for s in list(streets_of_liege())[:5]:
    ...     print(s)
    Place du 20-Août
    Rue de l'Abattoir
    Rue des Abeilles
    Rue des Acacias
    Rue de l'Académie


    """
    for ln in STREETS_OF_LIEGE.splitlines():
        if ln and ln[0] == '*':
            m = re.match(STREET_RE, ln)
            if m:
                s = m.group(1).strip()
                if '|' in s:
                    s = s.split('|')[1]
                yield s
                #~ streets.append(s)


LAST_NAMES_BELGIUM = Cycler(splitter1(LAST_NAMES_BELGIUM))
MALE_FIRST_NAMES_FRANCE = Cycler(splitter2(MALE_FIRST_NAMES_FRANCE))
FEMALE_FIRST_NAMES_FRANCE = Cycler(splitter2(FEMALE_FIRST_NAMES_FRANCE))

LAST_NAMES_AFRICAN = Cycler(splitter1(LAST_NAMES_AFRICAN))
MALE_FIRST_NAMES_AFRICAN = Cycler(splitter1(MALE_FIRST_NAMES_AFRICAN))
FEMALE_FIRST_NAMES_AFRICAN = Cycler(splitter1(FEMALE_FIRST_NAMES_AFRICAN))

LAST_NAMES_MUSLIM = Cycler(splitter1(LAST_NAMES_MUSLIM))
MALE_FIRST_NAMES_MUSLIM = Cycler(splitter1(MALE_FIRST_NAMES_MUSLIM))
FEMALE_FIRST_NAMES_MUSLIM = Cycler(splitter1(FEMALE_FIRST_NAMES_MUSLIM))

if False:
    last_names = []
    for ln in LAST_NAMES_FRANCE.splitlines():
        if ln:
            a = ln.split()
            if len(a) == 3:
                last_names.append(a[0].strip())
            elif len(a) == 4:
                last_names.append(a[0].strip() + ' ' + a[1].strip())


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
