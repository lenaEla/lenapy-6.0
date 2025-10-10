"""
Constants module.
Here stand the first brick of the bot
"""
import os, json, requests, math, random, shutil
from datetime import timedelta, datetime
import pytz
from interactions import *
from typing import Union, List

MAXLEVEL, PRESTIGEXPBOOST, XPBOOSTVALUE = 100, 70, 150

emLoading = '<a:loading:862459118912667678>'

try: parisTimeZone = pytz.timezone("Europe/Paris")
except: print(pytz.all_timezones)

defaultDate = datetime(year=2001,month=1,day=19,hour=19,minute=26,second=57,tzinfo=parisTimeZone)

FROM_LEFT, FROM_RIGHT, FROM_UP, FROM_DOWN, FROM_POINT = 0,1,2,3,4
STAT_UP_EM = "<a:statUp:1395096480129220718>"
STAT_DOWN_EM = "<a:statDown:1395096499108577310>"
STAT_NEUTRAL_EM = "<:statNeutral:1395100322699018410>"


def clamp(val:int, minv:int=0, maxv:int=1):
	return minv if val < minv else maxv if val > maxv else val

def between(val: int, limitMax: int, limitMin:int):return min(max(val,limitMin),limitMax)

# Constantes :
# Area of effects
AREA_MONO = 0  # Caster only
AREA_CIRCLE_1 = 1  # Circles (target include)
AREA_CIRCLE_2 = 2
AREA_CIRCLE_3 = 3
AREA_CIRCLE_4 = 4
AREA_CIRCLE_5 = 5
AREA_CIRCLE_6 = 6
AREA_CIRCLE_7 = 7
AREA_ALL_ALLIES = 8  # All allies
AREA_ALL_ENEMIES = 9  # All ennemies
AREA_ALL_ENTITES = 10  # All
AREA_CONE_2 = 11  # Cones
AREA_CONE_3 = 12
AREA_CONE_4 = 13
AREA_CONE_5 = 14
AREA_CONE_6 = 15
AREA_CONE_7 = 16
AREA_LINE_2 = 17  # Lines from target
AREA_LINE_3 = 18
AREA_LINE_4 = 19
AREA_LINE_5 = 20
AREA_LINE_6 = 21
AREA_DONUT_1 = 22  # Circles (target exclude)
AREA_DONUT_2 = 23
AREA_DONUT_3 = 24
AREA_DONUT_4 = 25
AREA_DONUT_5 = 26
AREA_DONUT_6 = 27
AREA_DONUT_7 = 28
AREA_DIST_3 = 29  # Circles (Must be > 2)
AREA_DIST_4 = 30
AREA_DIST_5 = 31
AREA_DIST_6 = 32
AREA_DIST_7 = 33
AREA_ARC_1 = 34  # Arc
AREA_ARC_2 = 35
AREA_ARC_3 = 36
AREA_RANDOMENNEMI_1 = 37
AREA_RANDOMENNEMI_2 = 38
AREA_RANDOMENNEMI_3 = 39
AREA_RANDOMENNEMI_4 = 40
AREA_RANDOMENNEMI_5 = 41
AREA_INLINE_2 = 42
AREA_INLINE_3 = 43
AREA_INLINE_4 = 44
AREA_INLINE_5 = 45
AREA_BOMB_5 = 46
AREA_BOMB_6 = 47
AREA_BOMB_7 = 48
AREA_LOWEST_HP_ALLIE = 49
AREA_SUMMONS = 50
AREA_RANDOMALLIE_1 = 51
AREA_RANDOMALLIE_2 = 52
AREA_RANDOMALLIE_3 = 53
AREA_RANDOMALLIE_4 = 54
AREA_RANDOMALLIE_5 = 55
AREA_SUMMONER = 56
AREA_BIGDONUT = 57
AREA_LOWEST_HP_ENEMY = 58
AREA_HIGHEST_DAMAGE_ENEMY = 59

areaMelee = [AREA_MONO,AREA_CIRCLE_1,AREA_CIRCLE_2,AREA_CIRCLE_3,AREA_CONE_2,AREA_CONE_3,AREA_LINE_2,AREA_LINE_3,AREA_DONUT_1,AREA_DONUT_2,AREA_DONUT_3,AREA_INLINE_2,AREA_INLINE_3,AREA_BIGDONUT]
areaDist = [AREA_DIST_3,AREA_DIST_4,AREA_DIST_5,AREA_DIST_6,AREA_DIST_7,AREA_BOMB_5,AREA_BOMB_6,AREA_BOMB_7]
areaMixte = []
notOrientedAreas = [AREA_CIRCLE_1,AREA_CIRCLE_2,AREA_CIRCLE_3,AREA_CIRCLE_4,AREA_CIRCLE_5,AREA_CIRCLE_6,AREA_CIRCLE_7,AREA_DONUT_1,AREA_DONUT_2,AREA_DONUT_3,AREA_DONUT_4,AREA_DONUT_5,AREA_DONUT_6,AREA_DONUT_7,AREA_INLINE_2,AREA_INLINE_3,AREA_INLINE_4,AREA_INLINE_5,AREA_DIST_3,AREA_DIST_4,AREA_DIST_5,AREA_DIST_6,AREA_DIST_7,AREA_BOMB_5,AREA_BOMB_6,AREA_BOMB_7,AREA_LOWEST_HP_ALLIE,AREA_SUMMONS, AREA_HIGHEST_DAMAGE_ENEMY]
areaRandom = [AREA_RANDOMENNEMI_1, AREA_RANDOMENNEMI_2, AREA_RANDOMENNEMI_3, AREA_RANDOMENNEMI_4, AREA_RANDOMENNEMI_5, AREA_RANDOMALLIE_1, AREA_RANDOMALLIE_2, AREA_RANDOMALLIE_3, AREA_RANDOMALLIE_4, AREA_RANDOMALLIE_5]

areaShortRange = [
	AREA_MONO,
	AREA_CIRCLE_1,
	AREA_CIRCLE_2,
	AREA_DONUT_1,
	AREA_DONUT_2,
	AREA_ARC_1,
	AREA_ARC_2,
	AREA_INLINE_2
]

areaMidRange = [
	AREA_CIRCLE_3,
	AREA_CIRCLE_4,
	AREA_DONUT_3,
	AREA_DONUT_4,
	AREA_DIST_3,
	AREA_DIST_4,
	AREA_ARC_3,
	AREA_INLINE_3,
	AREA_INLINE_4,
	AREA_BIGDONUT
]

areaLongRange = [
	AREA_CIRCLE_5,
	AREA_CIRCLE_6,
	AREA_CIRCLE_7,
	AREA_DONUT_5,
	AREA_DONUT_6,
	AREA_DONUT_7,
	AREA_DIST_5,
	AREA_DIST_6,
	AREA_DIST_7,
	AREA_INLINE_5,
	AREA_BOMB_5,
	AREA_BOMB_6,
	AREA_BOMB_7
]

EmIcon = [None,['<:ikaRed:1362015771055886528>','<:ikaOrange:1362015710972219452>','<:ikaYellow:866459268520607775>','<:ikaGreen:1362015674326712421>','<:ikaLBlue:1362015691049533450>','<:ikaBlue:1362015656639201422>','<:ikaPurple:1362015753124970566>','<:ikaPink:1362015735303377027>','<:ikaWhite:871149538554044466>','<:ikaBlack:1362015633788895322>'],['<:takoRed:866459004439756810>','<:takoOrange:866459027562954762>','<:takoYellow:866459052132532275>','<:takoGreen:866459073910145025>','<:takoLBlue:866459095875190804>','<:takoBlue:866459141077860352>','<:takoPurple:866459162716536892>','<:takoPink:866459203949166593>','<:takoWhite:871149576965455933>','<:takoBlack:871151069193969714>'],['<:octarian:866461984018137138>'],['<:baseIka:913847108640047174>',"<:baseTako:913847092835930172>","<:empty_squid:913911277548601344>","<:empty_octo:913911290299289632>",'<:littleStar:925860806602682369>','<:ikaCatLine:930383582898315284>','<:ikaCatBody:930383603026776064>','<:takoCatLine:930383560630734848>','<:takoCatBody:930397525888880711>','<:komoriLine:930804436861857872>','<:komoriBody:930798973386641448>','<:birdLine:930906003967443034>','<:birdColor:930908372969095248>','<:skeletonLine:930910501691588658>','<:skeletonColor:931190496427139112>','<:fairyLine:935335398094274621>','<:fairyColor:935335413005037600>','<:fairy2Line:935336370774351902>','<:fairy2Color:935336353284096040>']]
EmCount = ('0️⃣','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🇦','🇧','🇨','🇩','🇪','🇫')

for cmpt in range(AREA_INLINE_5+1):
	if cmpt not in [AREA_RANDOMENNEMI_1,AREA_RANDOMENNEMI_2,AREA_RANDOMENNEMI_3,AREA_RANDOMENNEMI_4,AREA_RANDOMENNEMI_5,AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES] + areaMelee + areaDist:
		areaMixte.append(cmpt)

areaNames = ["Monocible", "Cercle de rayon 1", "Cercle de rayon 2", "Cercle de rayon 3", "Cercle de rayon 4", "Cercle de rayon 5", "Cercle de rayon 6", "Cercle de rayon 7", "Tous les alliés", "Tous les ennemis", "Tous les combattants", "Cone simple", "Cone Large", "Cone Large", "Cone Large", "Cone Large", "Cone Large", "Ligne de 2 de longueur", "Ligne de 3 de longueur", "Ligne de 4 de longueur", "Ligne de 5 de longueur", "Ligne de 6 de longueur", "Donut de 1 de rayon", "Donut de 2 de rayon", "Donut de 3 de rayon", "Donut de 4 de rayon","Donut de 5 de rayon", "Donut de 6 de rayon", "Donut de 7 de rayon", "Anneau Distance de 1 de largeur", "Anneau Distance de 2 de largeur", "Anneau Distance de 3 de largeur", "Anneau Distance de 4 de largeur", "Anneau Distance de 5 de largeur", "Arc de Cercle de 1 de rayon", "Arc de Cercle de 2 de rayon", "Arc de Cercle de 3 de rayon", "1 ennemi aléatoire", "2 ennemis aléatoires", "3 ennemis aléatoires", "4 ennemis aléatoires", "5 ennemis aléatoires", "Croix de 2 cases", "Croix de 3 cases", "Croix de 4 cases", "Crois de 5 cases","Lobbée de 5 cases","Lobbée de 6 cases","Lobbée de 7 cases","Allié le plus blessé","Invocations","1 allié aléatoire","2 alliés aléatoires","3 alliés aléatoires","4 alliés aléatoires","5 alliés aléatoires","Invocateur","Anneau","Ennemi le plus blessé", "Ennemi ayant infligé le plus de dégâts"]
allArea = range(0, AREA_BOMB_7)
listNumberEmoji = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟","▶️","⏸️","⏯️","⏹️","⏺️","⏭️","⏮️","⏩","⏪","⏫","⏬","◀️","🔼","🔽","➡️","⬅️","⬆️","⬇️","↗️","↘️","↙️","↖️","↕️","↔️"]

rangeAreaEmojis = ["<:rangeMono:1032293272783179796>", "<:rangeCircle:1032293347869593691>(1)", "<:rangeCircle:1032293347869593691>(2)", "<:rangeCircle:1032293347869593691>(3)", "<:rangeCircle:1032293347869593691>(4)", "<:rangeCircle:1032293347869593691>(5)", "<:rangeCircle:1032293347869593691>(6)", "<:rangeCircle:1032293347869593691>(7)", "<:rangeAllAllies:1032512884351172668>", "<:rangeAllEnemies:1032512939992809502>", "<:rangeAllEntities:1032512991859576933>", "<:rangeCone:1032293500093480970>(1)", "<:rangeCone:1032293500093480970>(2)", "<:rangeCone:1032293500093480970>(3)", "<:rangeCone:1032293500093480970>(4)", "<:rangeCone:1032293500093480970>(5)", "<:rangeCone:1032293500093480970>(6)", "<:rangeLine:1032293431298494595>(2)", "<:rangeLine:1032293431298494595>(3)", "<:rangeLine:1032293431298494595>(4)", "<:rangeLine:1032293431298494595>(5)", "<:rangeLine:1032293431298494595>(6)", "<:rangeDonut:1032294133219459103>(1)", "<:rangeDonut:1032294133219459103>(2)", "<:rangeDonut:1032294133219459103>(3)", "<:rangeDonut:1032294133219459103>(4)","<:rangeDonut:1032294133219459103>(5)", "<:rangeDonut:1032294133219459103>(6)", "<:rangeDonut:1032294133219459103>(7)", "<:rangeDist:1032294217415921726>(1)", "<:rangeDist:1032294217415921726>(2)", "<:rangeDist:1032294217415921726>(3)", "<:rangeDist:1032294217415921726>(4)", "<:rangeDist:1032294217415921726>(5)", "<:rangeArc:1033268272285614080>(1)", "<:rangeArc:1033268272285614080>(2)", "<:rangeArc:1033268272285614080>(3)", "<:rangeRdmEnemie:1032513037351010335>(1)", "<:rangeRdmEnemie:1032513037351010335>(2)", "<:rangeRdmEnemie:1032513037351010335>(3)", "<:rangeRdmEnemie:1032513037351010335>(4)", "<:rangeRdmEnemie:1032513037351010335>(5)", "<:rangeCross:1032294049027194940>(2)", "<:rangeCross:1032294049027194940>(3)", "<:rangeCross:1032294049027194940>(4)", "<:rangeCross:1032294049027194940>(5)","<:rangeLob:1032294266988408833>(5)","<:rangeLob:1032294266988408833>(6)","<:rangeLob:1032294266988408833>(7)","<:INeedHealing:881587796287057951>","<:sprink1:887747751339757599>","<:rangeRdmEnemie:1032513037351010335>","<:rangeRdmEnemie:1032513037351010335>","<:rangeRdmEnemie:1032513037351010335>","<:rangeRdmEnemie:1032513037351010335>","<:rangeRdmEnemie:1032513037351010335>","<:rangeDist:1032294217415921726>"]
rangeAreaEmojis += rangeAreaEmojis[AREA_RANDOMENNEMI_1:AREA_RANDOMENNEMI_5+1] + ["","", "<:blue:950231849337233448>"]
areaEmojis = ["<:areaMono:1032293314130616400>", "<:areaCircle:1032293380379656192>(1)", "<:areaCircle:1032293380379656192>(2)", "<:areaCircle:1032293380379656192>(3)", "<:areaCircle:1032293380379656192>(4)", "<:areaCircle:1032293380379656192>(5)", "<:areaCircle:1032293380379656192>(6)", "<:areaCircle:1032293380379656192>(7)", "<:areaAllAllies:1032512909982564443>", "<:areaAllEnemies:1032512965850710026>", "<:areaAllEntities:1032513013879681095>", "<:areaCone:1032293578858307624>(1)", "<:areaCone:1032293578858307624>(2)", "<:areaCone:1032293578858307624>(3)", "<:areaCone:1032293578858307624>(4)", "<:areaCone:1032293578858307624>(5)", "<:areaCone:1032293578858307624>(6)", "<:areaLine:1032293461803675708>(2)", "<:areaLine:1032293461803675708>(3)", "<:areaLine:1032293461803675708>(4)", "<:areaLine:1032293461803675708>(5)", "<:areaLine:1032293461803675708>(6)", "<:areaDonut:1032294180451520552>(1)", "<:areaDonut:1032294180451520552>(2)", "<:areaDonut:1032294180451520552>(3)", "<:areaDonut:1032294180451520552>(4)","<:areaDonut:1032294180451520552>(5)", "<:areaDonut:1032294180451520552>(6)", "<:areaDonut:1032294180451520552>(7)", "<:areaDist:1032294242783080518>(1)", "<:areaDist:1032294242783080518>(2)", "<:areaDist:1032294242783080518>(3)", "<:areaDist:1032294242783080518>(4)", "<:areaDist:1032294242783080518>(5)", "<:areaArc:1033268300412616747>(1)", "<:areaArc:1033268300412616747>(2)", "<:areaArc:1033268300412616747>(3)", "<:areaRdmEnemie:1032513060524539904>(1)", "<:areaRdmEnemie:1032513060524539904>(2)", "<:areaRdmEnemie:1032513060524539904>(3)", "<:areaRdmEnemie:1032513060524539904>(4)", "<:areaRdmEnemie:1032513060524539904>(5)", "<:areaCross:1032294077653328004>(2)", "<:areaCross:1032294077653328004>(3)", "<:areaCross:1032294077653328004>(4)", "<:areaCross:1032294077653328004>(5)","<:areaLob:1032294287657934910>(5)","<:areaLob:1032294287657934910>(6)","<:areaLob:1032294287657934910>(7)","<:INeedHealing:881587796287057951>","<:sprink1:887747751339757599>","<:areaRdmEnemie:1032513060524539904>","<:areaRdmEnemie:1032513060524539904>","<:areaRdmEnemie:1032513060524539904>","<:areaRdmEnemie:1032513060524539904>","<:areaRdmEnemie:1032513060524539904>","<:areaDist:1032294242783080518>"]
areaEmojis += areaEmojis[AREA_RANDOMALLIE_1:AREA_RANDOMALLIE_5+1] + ["","", "<:blue:950231849337233448>"]

print(len(areaEmojis))

if len(areaEmojis) != len(rangeAreaEmojis):
	print(len(areaEmojis),len(rangeAreaEmojis),len(areaNames))
	printy = ""
	for cmpt in range(len(areaNames)):
		try:
			printy+="{0} {1} {2}\n".format(areaNames[cmpt],rangeAreaEmojis[cmpt],areaEmojis[cmpt])
		except:
			print(areaNames[cmpt])
	print(printy)

# Weapon's range
RANGE_MELEE = 0
RANGE_DIST = 1
RANGE_LONG = 2

# Triggers for the effects
TRIGGER_PASSIVE = 0
TRIGGER_DAMAGE = 1
TRIGGER_END_OF_TURN = 2
TRIGGER_DEATH = 3
TRIGGER_DEALS_DAMAGE = 4
TRIGGER_INSTANT = 5
TRIGGER_START_OF_TURN = 6
TRIGGER_ON_REMOVE = 7
TRIGGER_AFTER_DAMAGE = 8
TRIGGER_HP_UNDER_70 = 9
TRIGGER_WEAPON_USE = 10
TRIGGER_HP_UNDER_50 = 11
TRIGGER_HP_UNDER_25 = 12
TRIGGER_ON_MOVE = 13

allTriggers = [TRIGGER_PASSIVE, TRIGGER_DAMAGE, TRIGGER_END_OF_TURN, TRIGGER_DEATH,TRIGGER_DEALS_DAMAGE, TRIGGER_INSTANT, TRIGGER_START_OF_TURN, TRIGGER_ON_REMOVE, TRIGGER_AFTER_DAMAGE,TRIGGER_HP_UNDER_70, TRIGGER_WEAPON_USE,TRIGGER_HP_UNDER_50,TRIGGER_HP_UNDER_25,TRIGGER_ON_MOVE]
triggersTxt = [
	"passivement",
	"lorsque le porteur reçoit des dégâts directs",
	"à la fin du tour du porteur",
	"à la mort du porteur",
	"lorsque le porteur inflige des dégâts directs",
	"lors de la pose de cet effet",
	"au début du tour du porteur",
	"lors du retrait de cet effet",
	"après que le porteur ai infligé des dégâts directs",
	"lorsque les PV du porteur tombent en dessous de 70%",
	"lors de l'utilisation de l'arme principale",
	"lorsque les PV du porteur tombent en dessous de 50%",
	"lorsque les PV du porteur tombent en dessous de 25%",
	"lorsque la cible se déplace ou est déplacée"
]

triggerUnderHp = {
	TRIGGER_HP_UNDER_70:0.7,TRIGGER_HP_UNDER_50:0.5,TRIGGER_HP_UNDER_25:0.25
}

BASEDAMAGEMUL = 0.8
DMGBONUSATLVL50, HEALBONUSATLVL50, ARMORBONUSATLVL50, ARMORMALUSATLVL0 = 50, 25, 25, 20
DMGBONUSPERLEVEL, HEALBONUSPERLEVEL, ARMORLBONUSPERLEVEL = DMGBONUSATLVL50/50/100, HEALBONUSATLVL50/50/100, ARMORBONUSATLVL50/50/100
SUDDENDEATHDMG = 10

# Skills and effects types
TYPE_ARMOR = 0
TYPE_INDIRECT_DAMAGE = 1
TYPE_INDIRECT_HEAL = 2
TYPE_BOOST = 3
TYPE_RESURECTION = 4
TYPE_DAMAGE = 5
TYPE_MALUS = 6
TYPE_HEAL = 7
TYPE_UNIQUE = 8
TYPE_SUMMON = 9
TYPE_PASSIVE = 10
TYPE_DEPL = 11

allTypeNames = ["Armure", "Dégâts indirects", "Soins Indirects" ,"Boost", "Resurection", "Dégâts", "Malus", "Soins", "Unique", "Invocation", "Passif", "Déployable"]
friendlyTypes, hostileTypes = [TYPE_ARMOR, TYPE_INDIRECT_HEAL, TYPE_HEAL, TYPE_BOOST, TYPE_RESURECTION], [TYPE_INDIRECT_DAMAGE, TYPE_DAMAGE, TYPE_MALUS]
allTypes = range(0, TYPE_DEPL+1)
typeEmojis = ["<:armor:1137364335581212682>", "<:indirect:1137364330237673542>", "<:indheal:1409379254814113814>", "<:buff:1409379273042690131>", "<:raise:1409379312896839690>", "<:direct:1137364333526007880>", "<:debuff:1409379294370861066>", "<:directheal:1409379234115485876>", "<:littleStar:925860806602682369>", "<:sprink1:887747751339757599>", "<:littleStar:925860806602682369>", "<:inkStorm:1014240016328835083>"]

EXCLUSIVE, BECOME = 0, 1
WEAPON, ASPIRATION, ELEMENT = 0,1,2

# Stats
STRENGTH = 0
ENDURANCE = 1
CHARISMA = 2
AGILITY = 3
PRECISION = 4
INTELLIGENCE = 5
MAGIE = 6
RESISTANCE = 7
PERCING = 8
CRITICAL = 9
ACT_HEAL_FULL = 10
ACT_BOOST_FULL = 11
ACT_SHIELD_FULL = 12
ACT_DIRECT_FULL = 13
ACT_INDIRECT_FULL = 14
PURCENTAGE = 20
FIXE = 21
HARMONIE = 22
MISSING_HP = 23

ACT_HEAL = 0
ACT_BOOST = 1
ACT_SHIELD = 2
ACT_DIRECT = 3
ACT_INDIRECT = 4

BONUSPOINTPERLEVEL, MAXBONUSPERSTAT, MAJORBONUS = 2, 85, 75

nameStats, nameStats2 = ["Force", "Endurance", "Charisme", "Agilité","Précision", "Intelligence", "Magie"], ["Résistance", "Pénétration", "Critique"]
allStatsNames = nameStats+nameStats2+["Soins","Boosts","Armures","Dégâts Directs","Dégâts Indirects"]
extraallStatNames = allStatsNames + ["?"]*5 +["Pourcentage", "Fixe", "Harmonie", "PVs Manquants"]
statEmojis = ["<:strength:1137363979950375022>","<:stamina:1137363976934674462>","<:charisma:1137363972606152745>","<:agility:1137363969464619079>","<:precision:1137363966981574716>","<:intelligence:1137364357823602749>","<:magie:1137363963257028688>","<:resistance:1137364355537715280>","<:percing:1137364352266149908>","<:critical:1137364347308494849>","<:healing:1137364338374623333>","<:boost:1137364341591638126>","<:armor:1137364335581212682>","<:direct:1137364333526007880>","<:indirect:1137364330237673542>"]
extraStatEmojis = statEmojis + ["?"]*5 + ["% PV Max", "-", "<:littleStar:925860806602682369>", "% PV Manquants"]

# Status for entities
STATUS_ALIVE, STATUS_DEAD, STATUS_RESURECTED, STATUS_TRUE_DEATH = 0, 1, 2, 3

DANGERUPPERSTAR = 5

# Aspirations
BERSERK, OBSERVATEUR, POIDS_PLUME, IDOLE, PREVOYANT, TETE_BRULEE, MAGE, ALTRUISTE, ENCHANTEUR, PROTECTEUR, VIGILANT, SORCELER, INOVATEUR, ATTENTIF, MASCOTTE, ASPI_NEUTRAL = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
aspiNames = ["Berserkeur", "Observateur", "Poids plume", "Idole", "Prévoyant", "Tête brulée", "Mage","Altruiste", "Enchanteur", "Protecteur", "Vigilant", "Sorcier", "Inovateur", "Attentif", "Mascotte", "Neutre"]
aspiEmoji = ["<:ber:985007311997263932>","<:obs:985007736360165407>","<:pplume:985007345648148541>","<:ido:985007596656275476>","<:pre:985007771613274133>","<:tbrule:985007436538740766>","<:ma:985010178900500561>","<:alt:985007803322224720>","<:enc:985007558156755004>","<:pro:985009037546487850>","<:vig:985009013097910302>","<:sor:985007632639205458>","<:inov:985007247656632360>","<:att:985007703707500555>","<:masc:1009814577262895224>","<:neutral:985011113458536538>"]
lbNames = ["Lames de l'Ombre","Odre de Tir : Drône 3.4.8 Alpha","Frappe de Silicia","Apothéose planétaire","Armure Galactique","Fracture Dimentionnelle","Colère de Nacialisla","Bénédiction de Nacialisla","Desctruction Silicienne","Pousée d'Espoir","Grandeur de Nacialisla","Cataclysme Powehien","Avenir Prometeur","Chef d'Oeuvre Balistique","Bénédiction Fleurale"]
lbDesc = ["Inflige des dégâts à l'ennemi ciblé et vous soigne d'une partie des dégâts infligés","Inflige des dégâts à l'ennemi ciblé et augmente vos statistiques","Inflige des dégâts à l'ennemi ciblé et le repousse violament","Augmente les statistiques des alliés à portée et réanime ceux qui sont vaincus","Octroie une armure aux alliés à portée et augmente leurs statistiques offensives","Inflige des dégâts à l'ennemi ciblé et réduit ses PV max","Inflige dégâts dans une large zone autour de l'ennemi ciblé","Soigne les alliés à portée et leur donne un effet de régénération tout en réanimant ceux qui étaient vaincus","Inflige des dégâts dans une large zone autour de l'ennemi ciblé et vous octroit une armure","Octroie une armure aux alliés à portée et augmente leurs statistiques défensives","Soigne les alliés à portée en réanimant ceux vaincus tout en réduisant vos dégâts subis","Inflige des dégâts dans une large zone autour de l'ennemi ciblé et lui inflige un effet de dégâts indirects multi-cibles","Augmente les statistiques des alliés à portée et réduit leurs dégâts subis pendant la même durée","Inflige des dégâts en ligne droite sur l'ennemi ciblé et augmente vos statistiques","Augmente les statistiques des alliés alentours et réduits la défense des ennemis à portée"]
recommandedStat = [
	[STRENGTH, ENDURANCE, AGILITY],
	[STRENGTH, PRECISION, ENDURANCE],
	[AGILITY, PRECISION, ENDURANCE],
	[CHARISMA, INTELLIGENCE, ENDURANCE],
	[INTELLIGENCE, PRECISION, ENDURANCE],
	[STRENGTH, PRECISION, ENDURANCE],
	[MAGIE, PRECISION, ENDURANCE],
	[CHARISMA, PRECISION, ENDURANCE],
	[MAGIE, ENDURANCE, AGILITY],
	[INTELLIGENCE, ENDURANCE, AGILITY],
	[CHARISMA, ENDURANCE, AGILITY],
	[MAGIE, INTELLIGENCE, ENDURANCE],
	[INTELLIGENCE, CHARISMA, ENDURANCE],
	[STRENGTH, INTELLIGENCE, ENDURANCE],
	[ENDURANCE, INTELLIGENCE, ENDURANCE],
	[STRENGTH, MAGIE, ENDURANCE]
]
recommandedStuffStat = [
	[STRENGTH, RESISTANCE, ENDURANCE, ACT_DIRECT_FULL, PERCING, CRITICAL],	# BERK
	[STRENGTH, PRECISION, ACT_DIRECT_FULL, PERCING, CRITICAL],	# OBS
	[AGILITY, PRECISION, RESISTANCE, STRENGTH, MAGIE, ACT_DIRECT_FULL, CRITICAL, PERCING],	# PLUME
	[CHARISMA, ACT_BOOST_FULL, INTELLIGENCE],	# IDOL
	[INTELLIGENCE, ACT_SHIELD_FULL, PRECISION, CRITICAL],	# PRE
	[STRENGTH, PRECISION, CRITICAL, PERCING, ENDURANCE, MAGIE, AGILITY],	# TETE
	[MAGIE, PRECISION, ACT_DIRECT_FULL, CRITICAL, PERCING],	# MAG
	[CHARISMA, ACT_HEAL_FULL, PRECISION, CRITICAL, PRECISION],	# ALT
	[MAGIE, ENDURANCE, RESISTANCE, ACT_DIRECT_FULL, AGILITY, CRITICAL, PERCING],	#ENCH
	[INTELLIGENCE, ENDURANCE, RESISTANCE, ENDURANCE, CRITICAL, ACT_SHIELD_FULL],	# PRO
	[CHARISMA, ENDURANCE, RESISTANCE, CRITICAL, ACT_HEAL_FULL],	# VIGI
	[MAGIE, INTELLIGENCE, ACT_INDIRECT_FULL, CRITICAL, PERCING],	# SORC
	[INTELLIGENCE, ACT_BOOST_FULL, CHARISMA],	# INO
	[STRENGTH, INTELLIGENCE, CRITICAL, ACT_INDIRECT_FULL, PERCING],	# ATT
	[ENDURANCE, ACT_BOOST_FULL, RESISTANCE],	# MASCO
	[STRENGTH, MAGIE, ACT_DIRECT_FULL]
]
recommandedMajorPoints = [
	[STRENGTH,ENDURANCE,RESISTANCE,ACT_DIRECT_FULL,CRITICAL],
	[PRECISION,PERCING,STRENGTH,CRITICAL,ACT_DIRECT_FULL],
	[AGILITY,STRENGTH,RESISTANCE,CRITICAL,ENDURANCE,ACT_DIRECT_FULL],
	[CHARISMA,ACT_BOOST_FULL,INTELLIGENCE,ACT_HEAL_FULL,RESISTANCE],
	[INTELLIGENCE,ACT_SHIELD_FULL,PRECISION,CRITICAL,RESISTANCE],
	[STRENGTH,ENDURANCE,RESISTANCE,ACT_DIRECT_FULL,PERCING],
	[MAGIE,PRECISION,CRITICAL,ACT_DIRECT_FULL,PERCING],
	[CHARISMA,ACT_HEAL_FULL,PRECISION,CRITICAL,RESISTANCE],
	[MAGIE,ENDURANCE,RESISTANCE,ACT_DIRECT_FULL,CRITICAL],
	[INTELLIGENCE,ENDURANCE,RESISTANCE,ACT_SHIELD_FULL,CRITICAL],
	[CHARISMA,ENDURANCE,RESISTANCE,ACT_HEAL_FULL,CRITICAL],
	[MAGIE,ACT_INDIRECT_FULL,INTELLIGENCE,CRITICAL,PERCING],
	[INTELLIGENCE,ACT_BOOST_FULL,CHARISMA,ACT_SHIELD_FULL,RESISTANCE],
	[ENDURANCE,ACT_BOOST_FULL,RESISTANCE,CHARISMA,INTELLIGENCE],
	[STRENGTH,ACT_INDIRECT_FULL,INTELLIGENCE,CRITICAL,PERCING]
]
while len(aspiEmoji) < len(aspiNames):
	aspiEmoji.append('<a:menacing:917007335220711434>')

ASPI_DPT = [BERSERK, OBSERVATEUR, POIDS_PLUME, TETE_BRULEE, MAGE, ENCHANTEUR, SORCELER, ATTENTIF]
ASPI_HEAL = [VIGILANT, ALTRUISTE]
ASPI_SHIELD = [PRECISION, PROTECTEUR]
ASPI_BOOST = [IDOLE, INOVATEUR, MASCOTTE]

BERS_LIFE_STEAL = 35
MASC_MAX_BOOST = 15
MASC_MIN_BOOST = 1
MASC_LVL_CONVERT = 5

dptAspi = [BERSERK,POIDS_PLUME,TETE_BRULEE,ENCHANTEUR,OBSERVATEUR,ATTENTIF,MAGE,SORCELER]
healAspi = [ALTRUISTE,VIGILANT]
armorAspi = [PREVOYANT,PROTECTEUR]
boostAspi = [IDOLE,INOVATEUR,MASCOTTE]
meleeAspi = [BERSERK,POIDS_PLUME,TETE_BRULEE,ENCHANTEUR,VIGILANT,MASCOTTE,ASPI_NEUTRAL,PROTECTEUR]

# "Target" values
ALL, TEAM1, TEAM2, ALLIES, ENEMIES = 0, 1, 2, 3, 4

# Selected options for fight
OPTION_WEAPON, OPTION_SKILL, OPTION_MOVE, OPTION_SKIP = 0, 1, 2, 3

# Genders. 2 for default
GENDER_MALE, GENDER_FEMALE, GENDER_OTHER = 0, 1, 2

# Color constants
red, light_blue, yellow, green, blue, purple, pink, orange, white, black, aliceColor = 0xED0000, 0x94d4e4, 0xFCED12, 0x1ED311, 0x0035E4, 0x6100E4, 0xFB2DDB, 0xEF7C00, 0xffffff, 0x000000, 0xffc3ff
colorId = [red, orange, yellow, green,light_blue, blue, purple, pink, white, black]
colorChoice = ["Rouge", "Orange", "Jaune", "Vert","Bleu Clair", "Bleu", "Violet", "Rose", "Blanc", "Noir"]

# Aspiration's max stats
# Refert to Aspiration's constants value
aspiStats = [
	# Berserk
	[70, 60, 30, 35, 35, 25, 20],
	# Observateur
	[70, 10, 45, 35, 60, 20, 35],
	# Poids Plume
	[50, 35, 20, 75, 35, 10, 50],
	# Idole
	[25, 25, 70, 40, 35, 40, 40],
	# Prévoyant
	[25, 35, 35, 35, 35, 75, 35],
	# Tête Brulée
	[55, 45, 25, 35, 25, 35, 55],
	# Mage
	[25, 15, 40, 20, 50, 40, 85],
	# Altruise
	[15, 40, 85, 45, 20, 45, 25],
	# Enchanteur
	[25, 60, 30, 50, 25, 10, 75],
	# Protecteur
	[15, 60, 45, 35, 15, 75, 30],
	# Vigilant
	[15, 60, 70, 35, 35, 35, 25],
	# Sorcier
	[20, 35, 35, 35, 20, 50, 80],
	# Inovateur
	[20, 35, 40, 35, 35, 70, 40],
	# Attentif
	[60, 25, 30, 25, 60, 40, 35],
	# Mascotte
	[20, 60, 50, 35, 30, 50, 30],
	# Neutre
	[40, 39, 39, 39, 39, 40, 39]
]

for a in range(0, len(aspiNames)):						   # Aspi base stats verification
	summation = 0
	for b in range(7):
		try:
			summation += aspiStats[a][b]
		except:
			pass

	if summation != 275:
		print("{0} n'a pas le bon cumul de stats : {1}".format(
			aspiNames[a], summation))

# Const Stuff Drop
constStuffDrop = {0:80,10:80,20:70,30:60,40:50,50:45,60:40,70:35,80:30,90:20,100:10}
constLooseStuffDrop = [50,35,15,5]
# Const Skill Drop
constSkillDrop = {0:100,10:90,20:80,30:70,40:60,50:50,60:40,70:35,80:30,90:20,100:10}

# Constants for "orientation" field for skills
TANK, DISTANCE, LONG_DIST = "Tank", "Distance", "Longue Distance"
DPT_PHYS, HEALER, BOOSTER, DPT_MAGIC, SHIELDER = "Bers, Obs, P.Plu, T.Bru, Att.", "Vig., Alt", "Ido, Inv, Masc.", "Enc, Mag, Sor.", "Pro., Pré."

# Elementals ----------------------------------------------------------------------------------------------------------
ELEMENT_NEUTRAL = 0
ELEMENT_FIRE = 1
ELEMENT_WATER = 2
ELEMENT_AIR = 3
ELEMENT_EARTH = 4
ELEMENT_LIGHT = 5
ELEMENT_DARKNESS = 6
ELEMENT_SPACE = 7
ELEMENT_TIME = 8
ELEMENT_UNIVERSALIS = 9

DISTDMGBUFF, AREADMGBUFF, DARKDMGBUFF = 5, 5, 5
LIGHTHEALBUFF = 5
TIMEHEALBUFF = TIMEDMGBUFF = 10
SPACEBONUSBUFF = 10

FIREINCURVALUE, WATERRETURNVALUE, AIRPUSHDMG, EARTHBOOST, LIGHTDMGBUFF, DARKDEBUFF, SPACESHIELD, TIMELIFESTEAL = 10, 10, 15, 5, 10, 10, 10, 10

elemEmojis = ["<:neutral:1137367688793042954>","<:fire:1137367710947356764>","<:water:1137367705972920441>","<:air:1137367703380828201>","<:earth:1137367700348354621>","<:light:1137367698037280818>","<:darkness:1137367695336165498>","<:space:1137367690332348577>","<:time:1137367693255786606>","<:univ:1137367685995438100>"]
secElemEmojis = ["<:em:866459463568850954>", "<:secFeu:932941340612894760>", "<:secEau:932941360858820618>", "<:secAir:932941299559063573>","<:secTerre:932941317804273734>", "<:secLum:932941251597201438>", "<:secTen:932941234501222410>","<:secAst:932941221331075092>","<:secTempo:932941280785338389>","<:univ:1137367685995438100>"]
elemDesc = [
	"L'élément Neutre ({0}) est l'élément le plus apprécié des nouvelles recrues.\nSans spécialisations particulière, cet élément permet de tout faire sans trop se casser la tête".format(elemEmojis[0]),
	"L'élément Feu ({0}) est en général préféré par ceux qui aiment tirer sans distinction et faire carnage sans pareil.\nLes dissicles de l'élément Feu infligent un peu plus de dégâts avec les armes et capacité de zone en distance.".format(elemEmojis[1]),
	"L'élément Eau ({0}) est plus propice à la concentration et la sérénité.\nLes adeptes de cet élément inflige plus de dégâts avec les armes ou capacités monocible à distance.".format(elemEmojis[2]),
	"L'élément Air ({0}) a pour réputation d'être assez capricieu et imprévisible.\nC'est pour cela que ses partisants filent tel le vent pour frapper plusieurs ennemis simultanément.".format(elemEmojis[3]),
	"L'élément Terre ({0}) permet de ressentir la puissance des courants d'énergie télurique et d'en tirer le meilleur parti.\nLes habitués de cet élément infligent des dégâts monocibles en mêlée plus conséquents.".format(elemEmojis[4]),
	"L'élément Lumière ({0}) permet d'entrevoir l'espoir là où les autres ne voit que les ombres.\nLes soins et armures de ces illuminés sont plus conséquents que ceux de leurs congénaires.".format(elemEmojis[5]),
	"L'élément Ténèbre ({0}) n'a pas son pareil pour exploiter les zones d'ombres de leurs adversaires.\nLes dégâts indirects de ces individues sont plus conséquents que ceux de leurs congénères.".format(elemEmojis[6]),
	"L'élément Astral ({0}) utilise la puissance cosmique à son aventage. Car rien ne se perd, rien ne se créait, tout se transforme.".format(elemEmojis[7]),
	"L'élément Temporel ({0}) permet de prévoire les coups, car avoir une longueur d'avance est toujours bienvenue.".format(elemEmojis[8])
]
elemNames = ["Neutre", "Feu", "Eau", "Air", "Terre", "Lumière","Ténèbre", "Astral", "Temporel", "Universalis Premera"]
elemMainPassifDesc = [
	"Aucun passif principal",
	"{3} Pénétration : + 5\n- Augmente de **{0}%** les dégâts directs infligés à distance\n- Augmente de **{1}%** les dégâts directs de zones infligés\n- Augmente de **{2}%** les dégâts indirects infligés".format(DISTDMGBUFF, AREADMGBUFF, AREADMGBUFF, statEmojis[PERCING]),
	"{3} Précision : + 10\n- Augmente de **{0}%** les dégâts directs infligés à distance\n- Augmente de **{1}%** les dégâts directs monocibles infligés\n- Augmente de **{2}%** les soins réalisés".format(DISTDMGBUFF, AREADMGBUFF, AREADMGBUFF, statEmojis[PRECISION]),
	"{3} Agilité : + 10\n- Augmente de **{0}%** les dégâts directs infligés en mêlée\n- Augmente de **{1}%** les dégâts directs de zones infligés\n- Augmente de **{2}%** les dégâts indirects infligés".format(DISTDMGBUFF, AREADMGBUFF, AREADMGBUFF, statEmojis[AGILITY]),
	"{3} Résistance : + 5\n- Augmente de **{0}%** les dégâts directs infligés en mêlée\n- Augmente de **{1}%** les dégâts directs de monocibles\n- Augmente de **{2}%** les armures donnés".format(DISTDMGBUFF, AREADMGBUFF, AREADMGBUFF,statEmojis[RESISTANCE]),
	"- Augmente de **{0}%** les soins réalisés\n- Augmente de **{0}%** les armures donnés\n- Vous soigne de **{0}%** de vos PVs manquant en début de tour".format(LIGHTHEALBUFF),
	"- Augmente de **{0}%** tous les dégâts infligés\n- Augmente de **{1}%** les dégâts indirects infligés\n- Augmente de **{2}%** les dégâts infligés contre l'armure".format(DARKDMGBUFF,DARKDMGBUFF,DARKDMGBUFF),
	"- Augmente de **{0}%** les dégâts directs de zone infligés\n- Augmente de **{1}%** les bonus de statistiques réalisés".format(AREADMGBUFF,SPACEBONUSBUFF),
	"- Augmente de **{0}%** les dégâts indirects infligés\n- Augmente de **{1}%** les soins indirects réalisés".format(TIMEDMGBUFF,TIMEHEALBUFF)
]
elemSecPassifDesc = [
	"Aucun passif secondaire",
	"- Les effets de dégâts indirects infligés réduisent les soins reçus par la cible de **{0}%** (max 30%)".format(FIREINCURVALUE),
	"- Vous absorbez **{0}%** des soins directs effectués sur vos alliés".format(WATERRETURNVALUE),
	"- Augmente de **{0}%** les dégâts de colisions infligés".format(AIRPUSHDMG),
	"- Vous octroie **{0}%** de vol d'armure et **{0}%** de convertion de dégâts infligés en armure".format(EARTHBOOST),
	"- Augmente de **{0}%** la puissance des compétences de dégâts ayant pour effet secondaire d'octroyer des soins ou de l'armure à vous ou aux alliés (vol de vie / convertion inclus)".format(LIGHTDMGBUFF),
	"- Les effets de dégâts indirects infligés réduisent de **{0}%** les statistiques de la cible".format(DARKDEBUFF),
	"- En début de tour, octroie une armure équivalente à **{0}%** de vos PVs Manquants".format(SPACESHIELD),
	"- Les effets de dégâts indirects obtiennent **{0}%** de vol de vie".format(TIMELIFESTEAL)
]

# AoE stuff
AOEDAMAGEREDUCTION = 0.2
AOEMINDAMAGE = 0.4

def uniqueEmoji(emoji) -> List[List[str]]:
	return [[emoji, emoji], [emoji, emoji], [emoji, emoji]]

def sameSpeciesEmoji(team1, team2):
	return [[team1, team2], [team1, team2], [team1, team2]]

dangerEm = sameSpeciesEmoji('<a:dangerB:898372745023336448>', '<a:dangerR:898372723150041139>')
untargetableEmoji = uniqueEmoji('<:untargetable:899610264998125589>')

# List of guild ids for the bots
ShushyCustomIcons = [881900244487516180]
LenaCustomIcons = [881632520830087218, 881633183425253396]

stuffIconGuilds = [866782432997015613, 878720670006132787, 887756868787769434, 887846876114739261, 904164080204513331,908551466988486667, 914608569284964392, 922684334010433547, 928202839136825344, 933783830341484624, 953212496930562098, 1006418791669956698, 1025301457458704385,1102510147848380427,1189893832133840966]
weaponIconGuilds = [866363139931242506, 878720670006132787, 887756868787769434, 938379180851212310, 887846876114739261, 916120008948600872, 911731670972002374, 989526511285571614, 938379180851212310]

# For some time related stuff. Time from server != time from France


# Are we on the livebot or the test bot ?
isLenapy = not(os.path.exists("../Kawi"))

# Level to unlock skill slot
lvlToUnlockSkill = [0, 0, 0, 5, 15, 25, 35]

SKILL_GROUP_NEUTRAL, SKILL_GROUP_HOLY, SKILL_GROUP_DEMON = 0, 1, 2
skillGroupNames = ["neutre", "divine", "démoniaque"]

COUNTERPOWER = 35

SHOP_REPATITION = [4, 5, 8, 3]				 # Shop's item category length

# Same, but for the roll command
rollMessage = [
	"Selon toute vraisemblance ce sera un **{0}**", "Puisse la chance être avec toi... **{0}** !", "Alors Alice tu as obtenu combien ? **{0}** ? **{0}** alors","Sur 100, les chances que la relation Akrisk tienne debout ? Hum... **{0}**", "Le nombre de lances que tu va avoir à esquiver est... **{0}**"]

randomEmojiFight = [
	'<:ffsad:896113677550366740>',
	'<:ffboude:875347226170384454>',
	'<:ffshrug:895280749366878258>',
	'<:ffbored:889900326902186045>'
]

lenRdmEmojiFight = len(randomEmojiFight)
mauvaisePerdante = "\n\nUnexpected situation: The enemy has won"

tablCat = ["Début du combat", "Compétence ultime", "Transcendance", "En éliminant un ennemi", "À la mort", "En étant ressucité", "Victoire (Bleu) en étant en vie", "Victoire (Bleu) en étant mort", "Défaite (Bleu)", "Victoire (Rouge) en étant en vie", "Victoire (Rouge) en étant mort","Défaite (Rouge)", "Bloquer une grosse attaque", "Réaction à la réanimation de plusieurs alliés", "Réaction à la réanimation de plusieurs ennemis", "Réanimer plusieurs allier en même temps", "Réaction à l'élimination d'un ennemi", "Réaction à l'élimination d'un allié"]

# ==== Tmp Allies Quotes ======
tablSaysDictCat = ["start","ultimate","limiteBreak","onKill","onDeath","onResurect","blueWinAlive","blueWinDead","blueLoose","redWinAlive","redWinDead","redLoose","blockBigAttack","reactBigRaiseAllie","reactBigRaiseEnnemy","bigRaise","reactEnnemyKilled","reactAllyKilled"]
iconSetCatNames = ["hand","affElem","affAcc","affWeap"]

class says:
	"""A class for storing the says message from a entity"""
	def __init__(self, start=None, ultimate=None, limiteBreak=None, onKill=None, onDeath=None, onResurect=None, blueWinAlive=None, blueWinDead=None, blueLoose=None, redWinAlive=None, redWinDead=None, redLoose=None, blockBigAttack=None, reactBigRaiseAllie=None, reactBigRaiseEnnemy=None, bigRaise=None, reactEnnemyKilled=None, reactAllyKilled=None, reactAllyLb=None, reactEnemyLb=None, onHit=None, onMiss=None, takeHit=None, dodge=None, getHealed = None, specKill={}, specDeath={}, specReact={}):
		self.start = start
		self.ultimate = ultimate
		self.limiteBreak = limiteBreak
		self.onKill = onKill
		self.onDeath = onDeath
		self.onResurect = onResurect
		self.blueWinAlive = blueWinAlive
		self.blueWinDead = blueWinDead
		self.blueLoose = blueLoose
		self.redWinAlive = redWinAlive
		self.redWinDead = redWinDead
		self.redLoose = redLoose
		self.blockBigAttack = blockBigAttack
		self.reactBigRaiseAllie = reactBigRaiseAllie
		self.reactBigRaiseEnnemy = reactBigRaiseEnnemy
		self.bigRaise = bigRaise
		self.reactEnnemyKilled = reactEnnemyKilled
		self.reactAllyKilled = reactAllyKilled
		self.reactAllyLb = reactAllyLb
		self.reactEnemyLb = reactEnemyLb
		self.onHit = onHit
		self.onMiss = onMiss
		self.takeHit = takeHit
		self.dodge = dodge
		self.getHealed = getHealed
		self.specKill, self.specDeath, self.specReact = specKill, specDeath, specReact

	def tabl(self):
		return [
			self.start,
			self.ultimate,
			self.limiteBreak,
			self.onKill,
			self.onDeath,
			self.onResurect,
			self.blueWinAlive,
			self.blueWinDead,
			self.blueLoose,
			self.reactBigRaiseAllie,
			self.reactBigRaiseEnnemy,
			self.bigRaise,
			self.reactEnnemyKilled,
			self.reactAllyKilled
		]

	def fromTabl(self, tabl: list):
		self.__init__()
	
		for cmpt in range(len(tabl)):
			if type(tabl[cmpt]) == str: tabl[cmpt] = tabl[cmpt].replace("\\","")

		self.start = tabl[0]
		self.ultimate = tabl[1]
		self.limiteBreak = tabl[2]
		self.onKill = tabl[3]
		self.onDeath = tabl[4]
		self.onResurect = tabl[5]
		self.blueWinAlive = tabl[6]
		self.blueWinDead = tabl[7]
		self.blueLoose = tabl[8]
		self.reactBigRaiseAllie = tabl[9]
		self.reactBigRaiseEnnemy = tabl[10]
		self.bigRaise = tabl[11]
		self.reactEnnemyKilled = tabl[12]
		self.reactAllyKilled = tabl[13]

		return self

lenaSays = says(
	start="Lena, parée à faire feu.",
	ultimate="Area denied !",
	limiteBreak="C'est mainteant ou jamais !",
	onDeath="Tps.",
	onResurect="J'te revaudrais ça {target}",
	blueWinAlive="Bien joué",
	redWinAlive="Va falloir faire mieux que ça, là prochaine fois.",
	redWinDead="Pas mal. Mais pas suffisant",
	redLoose="Ahah, pas trop mal cette fois-ci. Mais ce n'était qu'un entrainement",
	reactBigRaiseAllie="Bien joué {caster}",
	reactBigRaiseEnnemy="Pas trop mal, mais on va pas vous laisser faire pour autant",
	reactEnnemyKilled="Pas trop mal {killer}",
	reactAllyKilled="T'en fais pas {downed}, je m'en charge.",
	blockBigAttack="Hé Luna ! Un brisage de l'Espace Temps ça te dis ?\"*\n<:luna:909047362868105227> : \*\"C'est pas déjà ce que l'on était en train de faire ?",
	reactEnemyLb="`Ricane` Si ça vous chante",reactAllyLb="Belle {skill}, {caster}",
	onHit = ["On va bien voir comment tu prendras la prochaine.","Tu prendras pas toutes te les prendre sans broncher.","La prochaine portera ton nom, {target}."],
	onMiss = ["T'en fais pas je te raterais pas la prochaine fois.","Pas la peine de prendre la grosse tête, {target}.","Juste un coup de chance."]
)

aliceSays = says(
	start="Ok, je vais faire de mon mieux, vous allez voir ☆⌒(ゝ。∂) !",
	onDeath="Kya ☆⌒(>。<) !",
	redWinAlive="Viii (≧▽≦) !",
	redWinDead="｡･ﾟ(ﾟ><ﾟ)ﾟ･｡",
	ultimate="Aller tous avec moi ! {skill} !",
	blueWinAlive="Alors, vous en avez dit quoi (≧▽≦) ?",
	onKill="J'aime pas la méthode direct (〃▽〃)...",
	onResurect="Prête pour le rappel ☆⌒(ゝ。∂)!",
	reactBigRaiseEnnemy="Je peux le faire aussi {caster}... Pas de quoi s'en venter...",
	bigRaise="Alors alors (〃▽〃)?",
	reactEnnemyKilled="En voilà un qui sera pas là pour mon final",
	reactAllyKilled="T'en fais pas {downed} !",
	reactAllyLb="Mow, je voulais terminer en apothéose moi :(",
	reactEnemyLb="Pff, tu appelles ça une démonstration, {caster} ?",
	limiteBreak="C'est l'heure de terminer en apothéose !",
	specReact={"Stella":"J'ai même pas envie d'exprimer une once d'empatie.","Bénédicte":"You go down just like Holy Mary...\"*\n{alice} : *\"Mary on a, Mary on a cross...".format(alice="<:alice:1069700207345946715>"),"Liu":"Comment je vais expliquer ça à Pénélope moi...","Sixtine":"Oh heu...","Félicité":"J'en connais une qui aura besoin d'un câlin ce soir..."},
	specDeath={"Nacialisla":["Ça c'est pour toutes les fourmilières que tu as éradiqué.","À ton tour d'être écrasée comme une fulgaire fourmis."]}
)

stellaSays = says(
	specReact={
		"Alice":"Et bah alors c'est tout ?",
		"Powehi":"Tu l'a un peu cherché non ?"
		},
	start="J'espère que vous avez prévu des lunettes parceque ça va chauffer !",
	reactEnnemyKilled="Et c'est pas fini !",
	reactEnemyLb="Ow on a envie de briller ?",
)

serenaSays = says(
	specReact={"Lohica":"J'espère que tu passeras bien le restant de tes jours à croupir aux enfers."}
)

clemSays = says(
	start="`Ferme son livre` Ok allons-y",
	ultimate="J'espère que tu es prêt pour te prendre un {skill} dans la face, {target} !",
	onDeath="Je t'ai sous estimé manifestement...",
	onResurect="Merci du coup de main",
	redWinAlive="Et bah alors, on abandonne déjà ?",
	blueWinAlive="Ça sera tout pour moi",
	reactEnnemyKilled="T'emballe pas trop {killer}",
	redLoose="Pas la peine de prendre la grosse tête.",
	limiteBreak="Vous commencez sérieusement à m'ennuyer.",
	reactAllyLb="J'aurais pû le faire moi-même {caster}.",
	getHealed="Merci",
	specDeath={"John":"Clémence !","Alice":"Voilà un combat que tu n'as pas sû gagner","Ruby":"Tu aurais pas oublié quelques principes de ta formation ?","Félicité":"Huh, ça va aller Clémence ?","Bénédicte":"À moitié surprise..."}
)

ailillSays = says(
	start="Tss, encore vous ?",
	onKill="Venez autant que vous êtes, ça changera rien",
	onDeath="Tu... paie rien pour attendre...",
	redWinAlive="Vous appelez ça un combat ?",
	reactBigRaiseEnnemy="Parceque vous pensez que ça changera quelque chose ?",
	reactEnemyLb="Juste une égratinure..."
)

jevilSays = says(
	start="Let's play a number game ! If you're HP drop to 0, I win !",
	onDeath="THIS BODY CANNOT BE KILLED !",
	redWinAlive="SUCH FUN !",
	redLoose="Such fun ! I'm exausted !"
)

lunaBossSays = says(
	start="Vous tenez tant que ça à vous mettre en travers de mon chemin ?\nSoit. Je vais vous montrer qu'un prêtresse des Ténèbres peut faire !",
	onKill="Disparait dans les ombres.",
	onDeath="Aha-",
	redWinAlive="Vous n'êtes pas les premiers. Et certainement pas les derniers.",
	redLoose="Mhf... Quand cesserez vous de suivre aveuglément cette Lumière corruptrice...",
	reactBigRaiseEnnemy="Vous devez en venir à là ? Soit !"
)

lunaDesc = """Luna est la conscience qu'ont aquis les Ténèbres injectés dans Lena par Gaster, dans leur dimension origielle (à Gaster et Luna, pas à Lena vu qu'elle vient d'ailleurs)

Dans cette dimension, les rapports entre la Lumière et les Ténèbres étaient inversés. C'était ces derniers qui permettaient aux habitants de voir et vitre, tandis que la Lumière représentait ce que nous apellons \"Obscurité\"
Luna a hérité du désir de destruction du monde corrompu qu'était le leur de Gaster lorsque celui-ci a utilisée Lena comme moyen de sortir de cette boucle génocidaire engagée par Chara, et le moins qu'on puisse dire c'est qu'elle y ai parvenu

Avec une puissance dépassant toutes les simulations de Gaster (qui n'avait pas prit en compte le status de personnage principal de Lena mais ça il pouvait pas savoir), Luna a effectivement brisé l'emprise que portait Le Premier Humain sur la dimention, mais a énormément déséquilibré l'équilibre entre les Ténèbres et la Lumière de cette dernière, ce qui causa plusieurs perturbations dans l'Espace Temps lui-même qui déchirèrent la dimension.
Cependant, puisqu'elle n'avait été crée que dans un seul but, la réalisation de celui-ci n'arrêta pas du tout Luna, qui commença à voir la Lumière et dimensions qui l'idolait comme une corruption de l'équilibre du multi-verse, qu'elle estime être son devoir en temps que Prêtresse des Ténèbres de supprimer.

Bien que Lena soit parcevenu à reprendre le contrôle, Luna n'en a pas abandonné des dessins pour autant, et son manque de consistance ainsi que son caractère têtu et compulsif l'empêche de vraiment se concentrer très longtemps sur autre chose, au dame de sa propre fille"""

shushiAltSays = says(
	start="Désolé Miman... Mais on peut pa ti laizer fire.",
	onKill="Zi te plait...",
	onDeath="D-Dézolée !",
	blueLoose="Ze ferais miheu... la prozaine fois...",
	blueWinAlive="Wiiii !",
	reactBigRaiseAllie="Bien joué {caster}"
)

shushiSays = says(
	start="Je vais te montrer ce que je peux faire Miman !",
	ultimate="C'est maintenant ou jamais !",
	onKill="Tu m'en voudras pas hein ? ?",
	onDeath="Miman !",
	onResurect="Ze veux encore dodo...",
	blueWinAlive="`Petite danse de la victoire et s'arrête brusquement lorsqu'elle remarque qu'on la regarde`  Heh !?",
	blueWinDead="Bien zoué !",
	blueLoose="Je vais devoir faire mieux la prochaine fois !",
	redWinAlive="Alors alors ?",
	redWinDead="Peux mieux faire !",
	redLoose="Oh...",
	getHealed="Merciiiii",
	takeHit="Mhf...",
	specDeath={"Lena":"Shushi !","Félicité":"Lena va pas être contente...","Iliana":"Huh, tiens bon calamar !","Alice":"Mow, qui a osé mettre K.O. une enfant cute comme Shuhsi ?"}
)

lunaSays = says(
	start="Ok, on va bien voir si vous continuez de faire les malins",
	ultimate="Ça va être tout noiiiiiire !",
	onKill="J'ai vu des brindilles plus solides que toi...",
	onDeath="Je retiens.",
	blueWinAlive="Et sans bavures !",
	redWinAlive="C'est eux que tu comptes recruter Lena ? Ne me fais pas rire"
)

shihuSays = says(
	start="J'essayerai de pas tout casser !",
	redWinAlive="Boum Boum",
	ultimate="Préparez vous à ressentir le pouvoir des Ténèbes !",
	onKill="Tu risques de broyer du noir pendant un moment, dézolée !",
	blueWinAlive="Haha ! C'était marrant ^^ On remet ça quand vous voulez !",
	specDeath={"Lena":"Shihu !","Félicité":"Lena va pas être contente...","Iliana":"Huh, tiens Shihu !"}
)

temSays = says(
	start="HoIIII !",
	onDeath="Ayayaya !",
	specDeath={"Lena":"Du miel pour les oreilles..."},
	specKill={"Lena":"C'est ça, la ferme."}
)

spamtonSays = says(
	start="HEY EVERY	   ! IT'S ME, SPAMTON G. SPAMTON!",
	redWinAlive="DON'T FORGET TO [[Like and Subscribe](https://gfycat.com/fr/gifs/search/youtube+subscribe+button+green+screen)] FOR MORE [[Hyperlink Blocked]]!",
	redLoose="THIS IS [[One Purchase](https://www.m6boutique.com/?adlgid=c|g||383715070314|b&gclid=Cj0KCQjwlOmLBhCHARIsAGiJg7lgxkpj8jJSOEZZ_q1URCeEWFW_SmyGcVeiKz8wUmO0-LCAE9Sz4SsaAgsvEALw_wcB)] YOU WILL [[Regret](https://www.youtube.com/watch?v=u617RilV5wU)] FOR THE REST OF YOUR LIFE!",
	onKill="HOW'S AN INNOCENT GUY LIKE ME SUPPOSED TO [[Rip People Off](https://www.youtube.com/watch?v=nIxMX6uyuAI)] WHEN KIDS LIKE YOU ARE [[Beating People Up](https://www.youtube.com/watch?v=4c_eEd-ReiY)]",
	reactEnemyLb="DON'T YOU WANNA BE A [[Big shot](https://www.youtube.com/watch?v=-8p8VowCmgE)]!?"
)

powehiSays = says(
	start="Un nouveau cycle commence...",
	limiteBreak="Qui vous a dit que je vous laisserais faire ?",
	onDeath="Kya !",
	onResurect="Mourir, c'est toujours pas drôle",
	reactBigRaiseAllie="On peut dire que tu sais y faire {caster}",
	reactEnemyLb="C'est beau de s'acharner inutilement...",
	getHealed="Merci bien",
	specDeath={"Stella":"Et bien on a eu du mal à tout absorber cette fois ?"},
	specKill={"Nacialisla":"Tiens donc, tu décide de laisser tomber ?"}
)

randomWaitingMsg = [
	"<a:bastuno:720237296322084905> Baston inkoming !",
	"<a:explosion:882627170944573471> Simulation de l'anéantissement à venir...",
	"<:invisible:899788326691823656> Erreur 404 : Blague non trouvée",
	"{alice} \"Conseil gratuit : Les OctoBooms font mal\"",
	"<a:giveup:902383022354079814>",
	"<a:Braum:760825014836002826> I am faster than you~"
]

johnSays = says(
	start="(Courage John. Montre lui que tu as appris à devenir un combattant.)",
	specDeath={"Clémence":"Hé ! Qui s'est permis de mettre mon John à terre !?"}
)

liaSays = says(
	start="Ça vous dirait de danser avec moi ?",
	onKill="Oh déjà... ?",
	onDeath="Hii ! Compris compris !",
	redWinAlive="C'était marrant !",
	redLoose="Vous savez pas rire...",
	reactBigRaiseAllie="Toujours aussi jouissif {caster}",
	reactEnemyLb="Mow, je crois qu'ils sont un peu en colère",
	dodge=["T'es sûr d'avoir les yeux en face des trous {caster} ?","Bien essayé","Pas cette fois !","Huh, ça devait être le vent..."],
	getHealed=["Arigatō","Domo","Merci {caster}"],
	specDeath={"Liu":"Hé bah on l'a pas esquivé celle-là","Liz":"Ça te ressemble pas d'abandonner comme ça Lia"}
)

liuSays = says(
	start="Hé ! Une course d'endurance vous en pensez quoi ?",
	onKill="Va falloir mieux gérer ta fatigue la prochaine fois",
	onResurect="Une seconde course ?",
	redLoose="Hé bah... Finalement c'est moi qui ai mordu la poussière",
	limiteBreak="Pas si vite !",
	reactEnemyLb="C'est bon tu as fini {caster} ?",
	getHealed="Go kyōryoku itadaki arigatōgozaimasu",
	takeHit=["C'est tout ce que tu peux faire {caster} ?","Va falloir taper plus fort que ça"],
	specDeath={"Lia":"Et bah alors, on dirais que tu as atteint ta limite Liu"}
)

lioSays = says(
	start="Oh... Heu... Bonjour...",
	onKill="J- J'y suis allé trop fort ?",
	onResurect="Merci...",
	onDeath="Humf ! J'aurais du rester dans la forêt...",
	redWinAlive="Le monde des humains est... perturbant...",
	bigRaise="On lache rien...",
	reactBigRaiseEnnemy="Je peux faire ça aussi, tu sais...",
	reactAllyKilled="Vous commencez à me taper sur les nerfs...",
	getHealed="Arigato gozaimasu...",
	specDeath={"Lia":"Huh, ça va être compliqué...","Liu":"Hé Lio c'est pas trop trop le moment de faire la sieste là !","Liz":"Lio !"}
)

lizSays = says(
	start="Tiens donc, des nouvelles braises",
	ultimate="Allez quoi, déclarez moi votre flamme !",
	onKill="Woops, j'y suis allé trop fort manifestement",
	onDeath="Pff, vous êtes pas drôle",
	redLoose="Waw, je me suis jamais faite autant refroidir rapidement...",
	reactEnemyLb="T'enflamme pas trop vite {caster}.",
	redWinAlive="Va falloir apprendre à pas trop vous consummer trop vite, vous savez ?",
	onHit="Oh je viens qu'on tiens plutôt bien debout",
	onMiss="Ne tente pas trop ta chance...",
	specDeath={"Lia":"Waw, quelqu'un a réussi à calmer tes ardeurs ?"}
)

julieSays = says(
	start="J'ai pas le temps pour ça ! Je dois encore faire la cuisine, nettoyer le hall, faire tourner une machine à laver et repasser les robes de Madame !",
	ultimate="Pas le choix...",
	limiteBreak="Courage vous autre !",
	onDeath="M-Madame... désolée...",
	onResurect="E-elle en saura rien, hein ?",
	bigRaise="Le temps joue contre nous ! Foncez !"
)

sixtineSays = says(
	start="`Baille en s'étirant`",
	ultimate="Soit...",
	redWinAlive="Je retourne dessiner maintenant...",
	redLoose="Zzz...",
	reactBigRaiseAllie="Waw...",
	reactAllyLb="C'était joli à regarder...",
	getHealed="Merci {caster}...",
	takeHit="Mfh !",
	specDeath={"Alice":"Hé !","Félicité":"Huh, ça va aller Sixtine ?"}
)

clemPosSays = says(
	start="J'en ai ma claque des gens de votre genre.",
	onKill="Un de plus, un de moins. Quelle importance",
	redWinAlive="Restez à votre place.",
	redLoose="Que...",
	takeHit=["Si tu crois que je vais laisser tomber pour si peu {caster}, tu te met le doigts dans l'oeuil.","Rassure moi, tu appelles pas ça une attaque quand même ?","C'était sensé faire quelque chose ?","{caster} utilise Trempette. Mais rien ne se passe."]
)

aliceExSays = says(
	start="Clémence...",
	onKill="...",
	onResurect="Merci...",
	blueWinAlive="Ça... Ça va mieux ?",
	bigRaise="Je y arriver probablement pas... S'il vous plaît..."
)

lilySays = says(
	start="Il faut toujours pourchasser ses rêves !",
	ultimate="Toujours suivre ses rêves !",
	limiteBreak="Que nos rêves deviennent réalité !",
	onDeath="Dites-moi que je rêve...",
	blueWinAlive="Faites de beaux rêves !",
	redLoose="C'est pas vrai, ça a encore viré au cauchemar...",
	reactAllyKilled="Ça commence à virer au cauchemar...",
	reactAllyLb="Faisons que cette réalité un doux rêve !",
	onKill="Heu... Je... je crois que j'y suis allé trop fort, désolée !",
	getHealed="Merci, je risque d'en avoir besoin..."
)

ilianaSaysNormal = says(
	start="Puisse ce combat être bénéfique pour tous !",
	ultimate="Qu'est-ce que vous pensez du pouvoir de la Lumière ?",
	limiteBreak="Que la Lumière nous protège !",
	onKill="Je décline toute responsabilité en cas de tache blanche incrustée dans ta rénite",
	onDeath="Humf !",
	reactAllyKilled="J'aurais du faire plus attention, désolée",
	reactBigRaiseAllie="On reprend ses esprits et on y retourne",
	takeHit=["C'est tout ce que tu as {caster} ?","Tu peux mieux faire quand même {caster}, non ?","Toujours debout !"],
	specDeath={"Luna":"Hé chaton, c'est pas le moment de faire la sieste !"}
)

ilianaSaysVsLuna = says(
	start="Tu nous fais encore une crise ?",
	ultimate="On tiens le bon bou, lachez rien !",
	onKill="T'en fait pas Luna !",
	onDeath="Ish...",
	onResurect="Merci bien",
	blueWinAlive="`S'assoit à côté de Luna, qui est trop fatiguée pour bouger, lui met la tête sur ses genoux puis caresse cette dernière en ronronnant`\"\n<:luna:909047362868105227> : \"Ili'...\"\n<:Iliana:926425844056985640> : \"Tu ferais la même chose si c'était moi, et tu t'es faite battre à plate couture, tu es pas en droit de contester\"\n<:luna:909047362868105227> : \"... `Ferme les yeux et s'endort peut de temps après`",
	blockBigAttack="Si tu crois que tu va m'avoir avec ça !",
	reactBigRaiseAllie="Je m'occupe des Ténèbres qui paralyse votre âme vous en faites pas !"
)

kitsuneSays = says(
	start="Mais c'est que vous êtes bien nombreux dites donc ^^",
	onKill="C'était trop intense pour toi ? Mais on a même pas encore commencé !",
	redWinAlive="C'était amusant, vous trouvez pas ?",
	reactBigRaiseEnnemy="Vos âmes m'appartiennent déjà, pourquoi résister ?",
	takeHit=["Tu essayes vraiment là ?","`Soupire` C'est vraiment tout ce que tu peux faire... ?"],
	onHit=["Pourquoi résister ?","Ahah, j'ai pas encore révélé tout l'étendu de mon pouvoir !"],
	dodge="Hum... Rater un adversaire de mon gabari quand même..."
)

lySays = says(
	start="Arf, mon truc c'est plutôt les squelettes et les zombies, vous savez ?",
	ultimate="Prêts pour le feu d'artifice ?",
	onDeath="Je suis pas assez bien payée pour ce genre de trucs...",
	onResurect="Je savais que j'aurais du prendre un totem de résurection... Mais merci",
	blueWinAlive="J'ai le droit de garder le loot ?",
	redWinAlive="Vous avez un lit qui vous attend",
	reactBigRaiseAllie="Si on doit en arriver à cette extremité, ça n'a pas vraiment l'air d'être bien parti...",
	reactBigRaiseEnnemy="Je doute que ça suffira à inverser la tendance !",
	reactEnnemyKilled="Tu as oublié ton totem de résurrection, {downed} ?"
)

gwenySays = says(start="Tachons de faire ça rapidement, ça vous vas ?",ultimate="Ok ça suffit là !",limiteBreak="Ok là vous m'avez énervée !",reactAllyLb="Espéront que ça changera la donne",reactAllyKilled="Je suppose que j'ai une nouvelle cible maintenant",reactBigRaiseEnnemy="En quoi c'est juste ça Lena !?\"*\n<:lena:909047343876288552> : \"*Vous pouvez le faire aussi, arrête de te plaindre",onKill="Tu m'en diras des nouvelles.",redWinAlive="Vous en revoulez ?")
klikliSays = says(start="Ok. Je vais m'en occuper rapidement",limiteBreak="OK, VOILÀ POUR VOUS !",onKill="Si tu veux revenir, j't'ai pas encore montrer tout ce dont je suis capable.",reactEnnemyKilled="Pff, j'peux le faire toute seule tu sais ?",ultimate="J'espère que tu as les yeux grands ouverts {target} !",redWinAlive="J'espère que vous en avez pris de la graine.",onHit="Et ce n'était qu'un début !",reactBigRaiseEnnemy="Vous en voulez encore ?")
altySays = says(start="'K, je vais faire de mon mieux",onKill="Désolée...",onResurect="Ok, second round !",reactAllyKilled="{downed} !",redWinAlive="Oulà, ça va aller ? Je crois qu'on y est allé un peu fort...",redWinDead="`Rigole` Bien joué tout le monde !",takeHit="Quoi c'est tout ?",bigRaise="On n'a pas encore dit notre dernier mot !")

shehisaSays = says(
	start="Ok, si on suit le plan, tout se passera bien",
	onKill=["Tu aurais pu attendre que je soit partie avant de creuver quand même.","Ça, c'est fait","Parfait, ça c'est bon"],
	onDeath="Humf, c'était pas prévu ça...",
	reactAllyKilled=["On lache rien !","On se relache pas !"],
	reactBigRaiseEnnemy=["C'était trop beau pour être vrai","Tps. On se reprend et on y retourne."],
	reactAllyLb=["Wowowo tu nous as fait quoi là {caster} ?", "C'était pas prévu ça. Mais bienvenue quand même"],
	blueWinAlive="Tout s'est déroulé comme prévu",
	redWinAlive="Tout s'est déroulé selon le plan",
	getHealed=["Merci {caster}","Merci. Tâcherais de faire un peu plus gaffe"],
	onHit=["Urf, j'aurais préféré terminer ça en un coup."])

churiSays = says(
	start="Ça n'a rien de personnel mais... Je dois devenir plus forte.",
	ultimate="À moi Hinoro !",
	limiteBreak="Je dois y arriver !",
	onKill = "T'en fais pas, je t'assure que l'au-delà n'est pas si terrible qu'il n'y parait",
	onResurect="Si c'est pas ironique...",
	bigRaise="Merci du coup de main Hinoro",
	reactAllyKilled="Ça se complique...",
	reactAllyLb="Pas trop mal"
)

lunaPreSays = says(
	start="C'est votre dernière chance de prendre la poudre d'escampette.",
	onKill="Quoi tu es surpris ? C'est pas faute d'avoir prévenu pourtant.",
	blueWinAlive="Pas la peine de revenir me faire chier, le résulta sera le même",
	reactBigRaiseEnnemy="Vous me faites une fleur vous savez, que vais pouvoir vous maraver la gueule une seconde fois sans ménagement",
	blockBigAttack="Chaton, c'est pas à toi de le faire d'habitude ?"
)

ilianaPreSays = says(
	start="J'espère que tu es en forme Luna...\"\n<:luna:909047362868105227> : \"Je suis toujours prête pour ce genre de trucs",
	ultimate="Oh on en a pas encore terminé !",
	reactEnnemyKilled="On a pas encore fini",
	blueWinAlive="`S'étire` Ce genre d'informités deviens de plus en plus récurrent...\"\n<:luna:909047362868105227> : \"Ca ne présage rien de bon..."
)

feliSays = says(
	start="Hoi !",
	ultimate="Prend toi donc ça {target} !",
	limiteBreak="Tu tomberas avant moi {target} !!",
	onKill="Wesh alors ?",
	blueWinAlive="`Sourit en faisant un V avec sa main gauche`",
	redWinAlive="Wesh alors ? C'est tout ?",
	onHit="Et ce n'est que le début {target} !",
	specDeath={"Alice":'Féli ! On se retrouve à la maison !'}
)

hinaSays = says(
	specDeath={"Lohica":[
		"Tss, encore par terre toi ?",
		"Un jour il va falloir que tu apprenne à voler de tes propres ailes tu sais ?",
		"À trop vouloir toucher le ciel on fini par se brûler les ailes."
		]}
)

edelweissSays = says(
	specDeath={"Lohica":"Am-"}
)

lohicaSays=says(
	specReact={"Séréna":"T'en fais pas, je me rappellerais de comment tu as vainnement essayé de me tenir tête quand je consulterais ta fleur déséchée dans mon herbier"}
)

def createTmpChangeDict(level: int, changeWhat: int, change: list, to: list, proba=100):
	"""ChangeWhat : 0 == skills"""
	if len(change) != len(to):
		raise AttributeError(
			"Change list and To list don't have the same length")
	if proba > 100:
		raise AttributeError("Proba > 100")
	elif proba < 1:
		raise AttributeError("Proba < 1")

	return {"level": level, "changeWhat": changeWhat, "change": change, "to": to, "proba": proba}

# ["Berserkeur", "Observateur", "Poids plume", "Idole", "Prévoyant", "Tête brulée", "Mage","Altruiste", "Enchanteur", "Protecteur", "Vigilant", "Sorcier", "Inovateur", "Attentif", "Neutre"]
limitBeakGif = [
	'https://cdn.discordapp.com/attachments/927195778517184534/932778559150391366/20220118_002840.gif',  # Ber
	'https://cdn.discordapp.com/attachments/927195778517184534/932775385043709952/20220118_001608.gif',  # Obs
	'https://cdn.discordapp.com/attachments/927195778517184534/932774912391782490/20220118_001411.gif',  # PPlu
	'https://cdn.discordapp.com/attachments/927195778517184534/932776578058965102/20220118_002049.gif',  # Ido
	'https://cdn.discordapp.com/attachments/927195778517184534/932778559502700594/20220118_002719.gif',  # Pré
	'https://media.discordapp.net/attachments/935769576808013837/938175773137862756/20220201_214401.gif', # Tbru
	'https://cdn.discordapp.com/attachments/933783831272628356/934069125628690482/20220121_135643.gif',  # Mage
	'https://cdn.discordapp.com/attachments/927195778517184534/932773655342104606/20220118_000858.gif',  # Alt
	'https://cdn.discordapp.com/attachments/927195778517184534/932773655732158525/20220118_000607.gif',  # Enc
	'https://cdn.discordapp.com/attachments/927195778517184534/932777330978488391/20220118_002225.gif',  # Pro
	'https://cdn.discordapp.com/attachments/927195778517184534/934968488550871140/20220124_012750.gif', # Vig
	'https://cdn.discordapp.com/attachments/927195778517184534/932773655732158525/20220118_000607.gif', # Sor
	'https://media.discordapp.net/attachments/935769576808013837/938175769253904414/20220201_214905.gif', # Ino
	'https://cdn.discordapp.com/attachments/927195778517184534/932777330605178920/20220118_002344.gif',  # Att
]

# ============ Procur Temp stuff =============

alphaTabl=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
def getAutoId(id:str,reverse=False):
	if type(id) != str:
		id = id.id
	idTabl = []
	for letter in id:
		idTabl.append(letter)
	for cmpt in range(len(idTabl)).__reversed__():
		if not(reverse):
			if idTabl[cmpt] == alphaTabl[-1]:
				idTabl[cmpt] = alphaTabl[0]
			else:
				for cmpt2 in range(len(alphaTabl)):
					if idTabl[cmpt] == alphaTabl[cmpt2]:
						idTabl[cmpt] = alphaTabl[cmpt2+1]
						break
				break
		else:
			if idTabl[cmpt] == alphaTabl[0]:
				idTabl[cmpt] = alphaTabl[-1]
			else:
				for cmpt2 in range(len(alphaTabl)):
					if idTabl[cmpt] == alphaTabl[cmpt2]:
						idTabl[cmpt] = alphaTabl[cmpt2-1]
						break
				break
	toReturn = ""
	for letter in idTabl:
		toReturn += letter
	return toReturn

def getArrayAutoId(start:str,iteration:int,reverse=False):
	"""Return a tuple of auto generated ids for stuffs and skills"""
	toReturn, cmpt = [], 0
	while cmpt < iteration:
		tempId = getAutoId(start,reverse)
		toReturn.append(tempId)
		start=tempId
		cmpt += 1
	return tuple(toReturn)

# ====== Stats Msg =======
randomMaxDmg = [
	"Apparament, {icon} __{name}__ aurait réussi à infligé **{value}** dégâts en un seul combat, ce mois-ci ╮(︶▽︶)╭",
	"Hé tu sais quoi {icon} __{name}__ ? Ton record de dégâts mensuel en un seul combat est de **{value}**",
	"Hum... le record de dégâts de {icon} __{name}__ est que de **{value}** ce mois-ci ? Pas ouf",
	"Voyons voir... Ce mois-ci, {icon} __{name}__ a fait au maximum **{value}** en un combat",
	"Une à droite et une à gauche ! {icon} __{name}__ a réussi à faire **{value}** dégâts avec des beignes bien placées ce mois-ci !",
	"Il faudrait peut-être que j'écrive une chanson sur la façon dont {icon} __{name}__ a infligé jusqu'à **{value}** dégâts ce mois-ci"
]

randomTotalDmg = [
	"Hé {icon} __{name}__ ! Tu veux savoir combien de dégâts tu as fait au total ? **{value}**",
	"Aufaite, tu voulais savoir combien de dégâts tu a fait {icon} __{name}__ au total ? **{value}**",
	"Tu veux savoir combien de dégâts tu as fait {icon} __{name}__ ? Hum... **{value}** ╮(︶▽︶)╭",
	"Pour {icon} __{name}__, j'ai ressencé **{value}** dégâts infligés jusqu'à présent"
]

randomMaxHeal = [
	"Alors voyons voir si {icon} __{name}__ est un bon healer... Son record de soins est de **{value}**, ce mois-ci",
	"Au maximum, tu as soigné **{value}** PV en un combat {icon} __{name}__ ce mois-ci",
	"Apparament, le record personnel de soins mensuel de {icon} __{name}__ est de **{value}**, ni plus ni moins ╮(︶▽︶)╭",
	"Savoir s'adapter à toutes les situations est crucial. Et {icon} __{name}__ a du avoir de bon réflexe pour avoir soigné **{value}** points de vie ce mois-ci",
]

randomTotalHeal = [
	"Au total, tu as soigné **{value}** PV {icon} __{name}__",
	"Tu as réussi à annuler **{value}** dégâts subis par tes alliés {icon} __{name}__, c'est pas trop mal (〃▽〃)! ",
	"Si j'en crois mes observations, {icon} __{name}__ aurait soigné un total de **{value}** PV... J'ai du mal regarder (ᓀ ᓀ)",
	"Tu n'aimes pas les barres de vies qui frittent avec le 0, n'est-ce pas {icon} __{name}__ ? Tu en est à **{value}** PV soignés, actuellement"
]

randomMaxRes = [
	"En un seul combat ce mois-ci, {icon} __{name}__ a réussi à ressuciter jusqu'à **{value}** alliés, quel ange gardien (ᓀ ᓀ)",
	"La mort c'est surcôté tu trouves pas {icon} __{name}__ ^^ ? Tu as ressucité jusqu'à **{value}** alliés en un seul combat durant le courant du mois"
]

randomTotalRes = [
	"La mort c'est juste une mauvaise grippe ☆⌒(ゝ。∂). Que {icon} __{name}__ a soigné **{value}** fois",
	"(－.－)…zzz {icon} __{name}__... résu... **{value}** fois...",
	"{icon} __{name}__ à l'air de bien maitriser les gestes de premiers secours, {il} a réanimé **{value}** fois un allié"
]

randomMaxTank = [
	"Hé bah ! {icon} __{name}__ a subis un maximum de **{value}** dégâts en un combat ce mois-ci ? J'espère que ses supports ont suivi (〃▽〃)",
	"{icon} __{name}__ préfère voir les ennemis dans le blanc des yeux apparament. En tous cas, c'est pas ses **{value}** dégâts subis en un combat qui le contesteront",
	"Je me demande ce qu'il y a dans la tête de {icon} __{name}__ pour s'être exposé à **{value}** dégâts ce mois-ci... A-t-{il} encore sa tête au moins ?"
]

randomTotalTank = [
	"Tiens donc ? {icon} __{name}__ aurait subi un total de **{value}** ? Ça fait pas mal quand même, je compatis pour ses soigneurs (￣ ￣|||)",
	"{icon} __{name}__, tu serais pas un peu mazo par hasard (￣ ￣|||) ? Tu es quand même à **{value}** dégâts totaux subis là..."
]

randomMaxArmor = [
	"L'important c'est de savoir quand utiliser ses capacités ☆⌒(ゝ。∂).\nRegardez {icon} __{name}__ : Son record d'armure donnée mensuel est à **{value}**",
	"Je suis plus partisante du \"Ils peuvent pas nous taper si ils sont morts\", mais bon au cas où je pourrais compter sur {icon} __{name}__.\nSon record d'armure donnée ce mois-ci est à **{value}** ╮(︶▽︶)╭",
	"{icon} __{name}__ n'aime pas vous voir subir des dégâts il faut croire. Ce mois-ci, {il} a donné au maximum **{value}** points d'armure en un combat"
]

randomTotalArmor = [
	"Il semblerais que {icon} __{name}__ préfère prévenir que guérir... Son total d'armure donné s'élève à **{value}**",
	"Le total d'armure donnée par {icon} __{name}__ s'élève à **{value}**, sans plus ni moins ╮(︶▽︶)╭",
	"Hé bah ! On peut dire que {icon} __{name}__ s'y connais en armure, {il} en a donné **{value}** points jusqu'à présent",
	"Je ne penses pas connaître de chanson qui racconterais comment {icon} __{name}__ a réussi à donner **{value}** points d'armures jusqu'à présent"
]

randomMaxKill = [
	"{icon} __{name}__ est une veritable terreur avec son record mensuel de **{value}** éliminations en un combat (･_├┬┴┬┴",
	"Va falloir que je me souvienne d'être particulirement prudente avec {icon} __{name}__ ( . .)φ...\nSon record d'élimination est de **{value}**...",
	"Toujours droit au but n'est-ce pas {icon} __{name}__ ? Tu as éliminé au maximum **{value}** ennemis ce mois-ci"
]

randomTotalKill = [
	"Le nombre de victimes de {icon} __{name}__ est de **{value}**.\n\nNon j'ai pas de commentaire à faire (＃￣0￣)",
	"Le nombre de victimes de {icon} __{name}__ est de **{value}**.",
	"Si j'ai bien compté, le nombre total d'élimiation par {icon} __{name}__ est à **{value}** (ᓀ ᓀ)\nFaites ce que vous voulez de cette information",
	"{icon} __{name}__ a éliminé au total **{value}** adversaires. J'espère qu'{il} garde en tête qu'{il} n'y est pas arrivé seul{e}"
]

randomRecordMsg = [
	"C'est cependant loin du record mensuel qui est de **{value}**, détenu par {icon} __{name}__",
	"Va falloir mieux faire si tu veux dépasser {icon} __{name}__, le sien est à **{value}** ☆⌒(ゝ。∂)",
	"Allez courage ! {icon} __{name}__ n'est qu'à **{value}** (^.~)☆",
	"Si tu veux viser les étoiles, sache que {icon} __{name}__ est à **{value}** ┐( ˘ ､ ˘ )┌",
	"Tu veux pas essayer de prendre le record ? Pour le moment c'est {icon} __{name}__ qui le détient avec **{value}**",
	"La concurence est dure par contre. Si tu cherches le haut du podium, il va falloir faire mieux que {icon} __{name}__ et ses **{value}**",
	"Par contre c'est {icon} __{name}__ qui brise tous les records en ce moment, avec ses **{value}** points"
]

randomPurcenMsg = [
	"Ça fait quoi... **{purcent}** % du total de son équipe ?",
	"Hum... Je crois que ça doit faire... **{purcent}** % du total de son équipe ?",
	"D'après ma calculatrice, ça fait **{purcent}**% du total de son équipe",
	"D'après Lena ça fait **{purcent}%** de son équipe"
]

randomTotalSupp = [
	"Qu'est-ce que ferais ton équipe sans toi {icon} __{name}__ ? Ton score de Soutien est à **{value}**",
	"Tiens donc, il semblerait que le score de Soutien de {icon} __{name}__ soit à **{value}**"
]

randomMaxSupp = [
	"On ne ménage pas ses efforts à ce que je vois {icon} __{name}__ ! En un combat, tu as réussi à obtenir un maximum de **{value}** points de Soutien durant ce mois",
	"Taper c'est bien beau, mais sans {icon} __{name}__, vous n'auriez pas tapé énormément. Son record de Soutien mensuel est de **{value}**"
]

aliceStatsNothingToShow = [
	["Hum... Il semblerait que personna dans ton équipe a fait de dégâts jusqu'à présent ?"],
	["Hé bah, ça vole pas haut niveau élimiation chez vous..."],
	["On a qu'une seule vie comme on dit. Enfin particulièrement chez vous, où personne a réanimé personne","Conseil d'amie : Vous feriez mieux d'avoir quelqu'un qui puisse réanimer dans votre équipe, et pas toujours vous reposer sur nous pour vous sauver le postérieur"],
	["Vous avez vraiment réussi à subir aucuns dégâts jusqu'à là ?"],
	["Faut croire que vous aimer vous faire maraver la figure, personne a soigné personne dans votre équipe"],
	["Vous savez qu'avoir un peu d'armure peu pas vous faire de mal, hein ?"],
	["Je sais que le role de Support n'est pas particulièrement attractif, mais bon il reste quand même utile d'en avoir un","Avoir un support est en général une bonne idée pour augmenter encore plus les dégâts ou les soins de votre équipe"]
]

# ============ Breaking the limits ===================
RANGELB1 = range(5,15+1)
RANGELB2 = range(4,10+1)
RANGELB3 = range(1,5+1)
RANGELB4 = range(1,3+1)

tablRangeLB = [RANGELB1,RANGELB2,RANGELB3, RANGELB4]

tablBreakingTheLimits = []
for cmpt in range(MAGIE+1):
	tablBreakingTheLimits.append([cmpt])
for cmpt in range(MAGIE+1):
	for cmpt2 in range(MAGIE):
		if cmpt2 != cmpt:
			tablBreakingTheLimits.append([cmpt,cmpt2])
for cmpt in range(MAGIE+1):
	for cmpt2 in range(MAGIE):
		if cmpt2 != cmpt:
			for cmpt3 in range(MAGIE):
				if cmpt3 not in [cmpt,cmpt2]:
					tablBreakingTheLimits.append([cmpt,cmpt2,cmpt3])
for cmpt in range(MAGIE+1):
	for cmpt2 in range(MAGIE):
		if cmpt2 != cmpt:
			for cmpt3 in range(MAGIE):
				if cmpt3 not in [cmpt,cmpt2]:
					for cmpt4 in range(MAGIE):
						if cmpt4 not in [cmpt,cmpt2,cmpt3]:
							tablBreakingTheLimits.append([cmpt,cmpt2,cmpt3,cmpt4])

for cmpt in range(len(tablBreakingTheLimits)):
	tablBreakingTheLimits[cmpt].sort()

# Captain Skills ---------------------------------------
CAP_EXP_LVL2, CAP_EXP_LVL3 = 100, 500
CAP_EXP_LOST, CAP_EXP_WIN = 5, 10

def createCapSkillDict(name:str,icon:str,desc:str,lvlValue1:List[int],lvlValue2:List[int],selectedTxt="")->dict:
	return {"name": name,"icon": icon,"desc": desc,"lvlValue1": lvlValue1,"lvlValue2": lvlValue2, "selectedTxt":selectedTxt}

capSkills = {
	0: createCapSkillDict("Lena","<:lena:909047343876288552>","En début de tour de table, inflige des dégâts aux **3** ennemis ayant le plus de PAr\nPuissance : **__{0}__** (x**__{1}__** sur l'armure)",[20,22.5,25],[4,4.5,5],"Prête à tirer"),
	1: createCapSkillDict("Clémence","<:clemence:908902579554111549>","En début de tour de table, marque les **__{0}__** ennemi(s) ayant le moins de PV\nLorsque le ou les ennemis marqués recevront des soins, ceux-ci seront réduit de **__{1}__** et votre équipié ayant le moins de PV sera soigné de cette même valeur",[1,2,3],[5,7.5,10],"Si vous y tenez"),
	2: createCapSkillDict("Hélène","<:helene:906303162854543390>","Augmente les PV maximums et les soins reçus par les équipiers de **__{0}%__**",[10,12.5,15],[0,0,0],"Je vous laisserais pas tomber"),
	3: createCapSkillDict("Shehisa","<:shehisa:919863933320454165>","Réduit la progression des malus d'agression en fonction des actions des équipiers de **__{0}%__**\nDe plus, octroie aux équipiers **__{1}%__** de chances d'effectuer une *Contre-Attaque* lorsqu'ils esquivent une attaque",[15,20,25],[5,10,15],"Ils peuvent pas nous toucher si nous sommes pas là"),
	4: createCapSkillDict("Liu","<:liu:908754674449018890>","Augmente de **__{0}%__** la probabilité de tous les équipiers d'effectuer une *Parade* lorsqu'il est attaqué\nDe plus, octroie aux équipiers **__{1}%__** de chances d'effectuer une *Contre-Attaque* lorsqu'ils parent une attaque",[10,15,20],[15,20,25],"Il suffit de garder la forme"),
	5: createCapSkillDict("Edelweiss","<:edelweiss:918451422939451412>","En début de tour de table, octroie aux **__{0}__** équipiers ayant le moins de PV une armure équivalante à **__{1}%__** des PV maximums de l'équipier qui en possède le plus",[1,2,3],[5,7.5,10],"Je vous ferais pas faux-bond..."),
	6: createCapSkillDict("Elina","<:elina:950542889623117824>","En début de tour de table, l'équipier ayant le moins de PV récupère **__{0}%__** de ses PV manquants et reçois des dégâts réduits de __**{1}%**__ pour le tour en cour",[10,12.5,15],[5,7.5,10],"Huh ?"),
	7: createCapSkillDict("Icealia","<:icealia:1308103151643136020>","Lorsqu'un équipier passe en dessous de __**{0}%**__ de ses PV maximums, il reçoit une armure équivalante à __**{1}%**__ de ses PV maximus pendant 3 tours (une fois par combat)",[10,12.5,15],[10,15,20],"Je vais faire de mon mieux")
}

# Team Settings ---------------------------------------
TEAM_SET_ALLY_ICON_DEFAULT, TEAM_SET_ALLY_ICON_WEAPON, TEAM_SET_ALLY_ICON_ASPIRATION = 0,1,2
TEAM_SET_ENEMY_ICON_DEFAULT, TEAM_SET_ENEMY_ICON_CLASSICAL = 0,1

def createTeamSettingsDict(teamLeader=0,settingsAllyIcon=0,settingsEnemyIcon=0,teamName="",teamCaptain=None,teamCapLenaExp=-1,teamCapClemenceExp=-1,teamCapHeleneExp=-1,teamCapShehisaExp=-1,teamCapLiuExp=-1,teamCapEdelweissExp=-1,teamCapElinaExp=-1,teamCapIcealiaExp=-1) -> dict:
	return {
		"teamLeader":teamLeader,
		"settingsAllyIcon":settingsAllyIcon,
		"settingsEnemyIcon":TEAM_SET_ENEMY_ICON_DEFAULT,
		"teamName":teamName,
		"teamCaptain":teamCaptain,
		"teamCapLenaExp":teamCapLenaExp,
		"teamCapClemenceExp":teamCapClemenceExp,
		"teamCapHeleneExp":teamCapHeleneExp,
		"teamCapShehisaExp":teamCapShehisaExp,
		"teamCapLiuExp":teamCapLiuExp,
		"teamCapEdelweissExp":teamCapEdelweissExp,
		"teamCapElinaExp":teamCapElinaExp,
		"teamCapIcealiaExp":teamCapIcealiaExp
	}

teamFirstName = [
	["Chauve-souris",1],
	["Oiseaux",0],
	["Flammes",1],
	["Torrents",0],
	["Vents",0],
	["Terres",1],
	["Lumières",1],
	["Ombres",1],
	["Supernovas",1],
	["Voyageurs",0],
	["Dragons",0],
	["Agresseurs",0],
	["Guerriers",0],
	["Stars",1],
	["Faucheurs",0],
	["Jardiniers",0],
	["Archéologues",0]
]

teamSecondName = [
	["espiègles","espiègles"],
	["de feu","de feu"],
	["divins","divines"],
	["insurmercibles","insurmercibles"],
	["insurmontables","insurmontables"],
	["immaculés","immaculées"],
	["intenses","intenses"],
	["éternels","éternelles"],
	["explosifs","explosives"],
	["intemporels","intemporelles"],
	["célestes","célestes"],
	["infatigables","infatigables"],
	["protecteurs","protectrices"],
	["nationnaux","nationnaux"],
	["paysans","paysannes"],
	["en herbe","en herbe"],
	["amateurs","amatrices"]
]

# Char Settings ------------------------------------------------
CHARSET_WEAPON_USE_LOW, CHARSET_WEAPON_USE_DEFAULT, CHARSET_WEAPON_USE_HIGH = 0,1,2
CHARSET_DMGSKILL_LOW, CHARSET_DMGSKILL_DEFAULT, CHARSET_DMGSKILL_HIGH = 0,1,2
CHARSET_HEALSKILL_LOW, CHARSET_HEALSKILL_DEFAULT, CHARSET_HEALSKILL_HIGH = 0,1,2
CHARSET_ARMORSKILL_LOW, CHARSET_ARMORSKILL_DEFAULT, CHARSET_ARMORSKILL_HIGH = 0,1,2
CHARSET_BOOSTSKILLL_LOW, CHARSET_BOOSTSKILLL_DEFAULT, CHARSET_BOOSTSKILL_HIGH = 0,1,2
CHARSET_DEBUFFSKILL_LOW, CHARSET_DEBUFFSKILL_DEFAULT, CHARSET_DEBUFFSKILL_HIGH = 0,1,2
CHARSET_SUMMONSKILL_LOW, CHARSET_SUMMONSKILL_DEFAULT, CHARSET_SUMMONSKILL_HIGH = 0,1,2
skillProbTxt = ["Rare","Normal","Beaucoup"]

CHARSET_OFFTARGET_DEFAULT, CHARSET_OFFTARGET_DMG, CHARSET_OFFTARGET_HEAL, CHARSET_OFFTARGET_BUFF = 0,1,2,3
charsetOffTargetTxt = ["Défaut","Attaquants","Récupérateurs","Supports"]
CHARSET_HEALTARGET_DEFAULT, CHARSET_HEALTARGET_DPT, CHARSET_HEALTARGET_HEAL, CHARSET_HEALTARGET_BUFF, CHARSET_HEALTARGET_MELEE = 0,1,2,3,4
charsetHealTargetTxt = ["Défaut","Attaquants","Récupérateurs","Supports","Mêlée"]
CHARSET_ARMORTARGET_DEFAULT, CHARSET_ARMORTARGET_DPT, CHARSET_ARMORTARGET_HEAL, CHARSET_ARMORTARGET_BUFF, CHARSET_ARMORTARGET_MELEE = 0,1,2,3,4
CHARSET_BUFFTARGET_DEFAULT, CHARSET_BUFFTARGET_LOWDPT, CHARSET_BUFFTARGET_HIGHDPT, CHARSET_BUFFTARGET_HASULT = 0,1,2,3
charsetBuffTargetTxt = ["Défaut","Attaquants à la traîne","Meilleurs Attaquants","Attaquants Préparés"]
CHARSET_RAISETARGET_DEFAULT, CHARSET_RAISETARGET_DMG, CHARSET_RAISETARGET_HEAL, CHARSET_RAISETARGET_BUFF = 0,1,2,3
charsetRaiseTargetTxt = ["Défaut","Attaquants","Récupérateurs","Supports"]

charsetCatNamesUse = ["Arme","Comp. Offensives","Comp. Soins","Comp. Armures","Comp. Bonus","Comp. Malus","Comp. Invocations"]
charsetCatNamesTarget = ["En attaque","À soigner","À protéger","À booster","À réanimer"]
charsetTargetOptions = [charsetOffTargetTxt,charsetHealTargetTxt,charsetHealTargetTxt,charsetBuffTargetTxt,charsetRaiseTargetTxt]
charsetUseNames = ["weaponUse","dmgSkillUse","healSkillUse","armorSkillUse","buffSkillUse","debuffSkillUse","summonSkillUse"]
charsetTargetsNames = ["offTarget","healTarget","armorTarget","buffTarget","raiseTarget"]

def createCharSettingsDict(weaponUse=CHARSET_WEAPON_USE_DEFAULT,dmgSkillUse=CHARSET_DMGSKILL_DEFAULT,healSkillUse=CHARSET_HEALSKILL_DEFAULT,armorSkillUse=CHARSET_ARMORSKILL_DEFAULT,buffSkillUse=CHARSET_BOOSTSKILLL_DEFAULT,debuffSkillUse=CHARSET_DEBUFFSKILL_DEFAULT,summonSkillUse=CHARSET_SUMMONSKILL_DEFAULT,offTarget=CHARSET_OFFTARGET_DEFAULT,healTarget=CHARSET_HEALTARGET_DEFAULT,armorTarget=CHARSET_ARMORTARGET_DEFAULT,buffTarget=CHARSET_BUFFTARGET_DEFAULT,raiseTarget=CHARSET_RAISETARGET_DEFAULT) -> dict:
	return {
		"weaponUse":weaponUse,
		"dmgSkillUse":dmgSkillUse,
		"healSkillUse":healSkillUse,
		"armorSkillUse":armorSkillUse,
		"buffSkillUse":buffSkillUse,
		"debuffSkillUse":debuffSkillUse,
		"summonSkillUse":summonSkillUse,
		"offTarget":offTarget,
		"healTarget":healTarget,
		"armorTarget":armorTarget,
		"buffTarget":buffTarget,
		"raiseTarget":raiseTarget
	}

emptyCharDict = createCharSettingsDict()
preDefCharSet = [
	[dptAspi,[
		["Défaut (DPT)","Votre personnage agira comme a été pensé son aspiration",createCharSettingsDict()],
		["Offensive Constante","Votre personnage utilisera bien plus ses options offensives au détriment de compétences qui pourrait l'aider à rester en vie plus longtemps",createCharSettingsDict(
			weaponUse=CHARSET_WEAPON_USE_HIGH,
			dmgSkillUse=CHARSET_DMGSKILL_HIGH,
			healSkillUse=CHARSET_HEALSKILL_LOW,
			armorSkillUse=CHARSET_ARMORSKILL_LOW,
			summonSkillUse=CHARSET_SUMMONSKILL_LOW
		)],
		["Prudence est mère de Sureté","Votre personnage utilisera plus souvent ses compétences pouvant lui octroyer de l'armure ou le soigner un peu",createCharSettingsDict(
			healSkillUse=CHARSET_HEALSKILL_HIGH,armorSkillUse=CHARSET_ARMORSKILL_HIGH,summonSkillUse=CHARSET_SUMMONSKILL_LOW,healTarget=CHARSET_HEALTARGET_MELEE,armorTarget=CHARSET_ARMORTARGET_MELEE
		)],
		["Soigne donc un autre tour","Votre personnage aura plutôt tendance à attaquer les adversaires qui soignent ou donne beaucoup d'armures à ses leurs coéquipiers",createCharSettingsDict(
			dmgSkillUse=CHARSET_DMGSKILL_HIGH,offTarget=CHARSET_OFFTARGET_HEAL,debuffSkillUse=CHARSET_DEBUFFSKILL_HIGH,weaponUse=CHARSET_WEAPON_USE_HIGH		   
		)]
	]],
	[healAspi+armorAspi,[
		["Défaut (Récup)","Votre personnage agira comme a été pensé son aspiration",createCharSettingsDict()],
		["Je suis un Récupérateur, mais...","Votre personnage délaissera un peu ses obligations pour chercher à attaquer l'ennemi",createCharSettingsDict(
			weaponUse=CHARSET_WEAPON_USE_LOW,dmgSkillUse=CHARSET_DMGSKILL_HIGH,healSkillUse=CHARSET_HEALSKILL_LOW,armorSkillUse=CHARSET_ARMORSKILL_LOW,raiseTarget=CHARSET_RAISETARGET_DMG
		)],
		["La Vie avant tout","Votre personnage priviligera abondammant les compétences de récupération et cherchera à garder le plus possible vos récupérateurs en vie",createCharSettingsDict(
			weaponUse=CHARSET_WEAPON_USE_LOW,healSkillUse=CHARSET_HEALSKILL_HIGH,armorSkillUse=CHARSET_ARMORSKILL_HIGH,healTarget=CHARSET_HEALTARGET_HEAL,armorTarget=CHARSET_ARMORTARGET_HEAL,raiseTarget=CHARSET_RAISETARGET_HEAL
		)]
	]],
	[boostAspi,[
		["Défaut (Récup)","Votre personnage agira comme a été pensé son aspiration",createCharSettingsDict()],
		["Coup de Pouce aux Récupérateurs","Votre personnage utilisera plus souvent ses compétences de soins ou d'armure",createCharSettingsDict(
			weaponUse=CHARSET_WEAPON_USE_LOW,healSkillUse=CHARSET_HEALSKILL_HIGH,armorSkillUse=CHARSET_ARMORSKILL_HIGH,dmgSkillUse=CHARSET_DMGSKILL_LOW,raiseTarget=CHARSET_RAISETARGET_HEAL,buffTarget=CHARSET_BUFFTARGET_HASULT
		)],
		["Offensive poussé","Votre personnage utilisera plus souvent ses compétences offensives et priviligera les alliés qui font le plus de dégâts",createCharSettingsDict(
			weaponUse=CHARSET_WEAPON_USE_HIGH,dmgSkillUse=CHARSET_DMGSKILL_HIGH,debuffSkillUse=CHARSET_DEBUFFSKILL_HIGH,buffTarget=CHARSET_BUFFTARGET_HIGHDPT,raiseTarget=CHARSET_RAISETARGET_DMG
		)]
	]]
]

def reduceEmojiNames(string:str) -> str:
	toReturn, emojiName, tempEmoji, inEmoji, inEmojiName = "","","", False, False
	for a in string:
		if not(inEmoji):
			if a != "<":
				toReturn = toReturn + a
			else:
				inEmoji = True
				tempEmoji = tempEmoji + a
		elif a == ">":
			inEmoji = False
			toReturn = toReturn + tempEmoji + a
			tempEmoji = ""
		elif not(inEmojiName):
			if a == ":":
				inEmojiName = True
			tempEmoji = tempEmoji + a
		else:
			if a == ":":
				inEmojiName = False
				tempEmoji = tempEmoji + a
				emojiName = ""
			elif len(emojiName) < 2:
				tempEmoji = tempEmoji + a
				emojiName = emojiName + a
	return toReturn

NPC_UNDEAD, NPC_FAIRY, NPC_DRYADE, NPC_HOLY, NPC_KITSUNE, NPC_GOLEM, NPC_UNFORM, NPC_DEMON, NPC_MARINE, NPC_SALMON, NPC_OCTARIAN, NPC_GLYPHIQUE, NPC_BOMB, NPC_SPIDER, NPC_ANGEL = tuple(range(15))
npcTeamNames = ["Mort-Vivant","Féérique","Dryade","Divin","Kitsune","Golem","Aformité","Démon","Marine","Salmonoïde","Octarien","Glyphide","Bombe","Araignés","Ange"]
npcTeamEmojis = ["<:squeleton:1034363693724610580>","<:brume:1058843224933933096>","<:gardeSilvestre:1023609768427925594>","<:dvin:1004737746377654383>","","","","<:dmon:1004737763771433130>","","<:smallFry:1127173673162387476>","","<:glyphidGrunt:1127174330216886312>","<:neutralbombR:1155485124142563390>","","<:dvinRegen:1104496736845713440>","","","","","",]
UNDEAD_WEAKNESS, FAIRYMAGICRESIST = 20, 10
ANGELPOWERMALUS = (100-10)/100
npcTeamDesc = [
	"Augmente les dégâts reçus des compétences {0} __Divines__ de **{1}%**".format("<:dvin:1004737746377654383>",UNDEAD_WEAKNESS),
	"Réduit les dégâts {4}{0} __Directs Magiques__ reçus de **{1}%** mais augmente d'autant les dégâts {2}{3} __Indirectes Force__ reçus".format(statEmojis[MAGIE],FAIRYMAGICRESIST,statEmojis[ACT_INDIRECT_FULL],statEmojis[STRENGTH],statEmojis[ACT_DIRECT_FULL]),
	"",
	"Augmente les dégâts reçus des compétences {0} __Démoniaques__ de **{1}%**".format("<:dmon:1004737763771433130>",UNDEAD_WEAKNESS),
	"Vulnérable aux {0} __Faiblesses élémentaires__".format("<:univ:936302039456165898>"),
	"Vulnérable aux {0} __Faiblesses élémentaires__".format("<:univ:936302039456165898>"),
	"",
	"Augmente les dégâts reçus des compétences {0} __Divines__ de **{1}%**".format("<:dvin:1004737746377654383>",UNDEAD_WEAKNESS),
	"",
	"",
	""
	]

WAKFUMAXLEVEL = 230

if not(os.path.exists("./data/database/shopMsg.json")):
	print("shopMsg.json not found")
	os.umask(0)
	f, r = open(os.getcwd() + '/data/database/shopMsg.json',mode="wb"), requests.get("https://raw.githubusercontent.com/lenaEla/LenapyShopMsg/main/shopMsg.json")
	f.write(r.content)
	f.close()
	print("> - Download Complete")

elif not(os.path.exists("../Kawi")) or 0:
	print("Downloading ShopMsg.json...")
	r, f = requests.get("https://raw.githubusercontent.com/lenaEla/LenapyShopMsg/main/shopMsg.json"), open( os.getcwd() + '/data/database/shopMsg.json',mode="wb")
	f.write(r.content)
	f.close()
	print("> - Download Complete")
	
	print("Downloading appEmoji.json...")
	r, f = requests.get("https://raw.githubusercontent.com/lenaEla/LenapyShopMsg/main/appEmoji.json"), open( os.getcwd() + '/data/database/appEmoji.json',mode="wb")
	f.write(r.content)
	f.close()
	print("> - Download Complete")
else:
	shutil.copy("../LenapyShopMsg/shopMsg.json", "./data/database/shopMsg.json")
	shutil.copy("../LenapyShopMsg/appEmoji.json", "./data/database/appEmoji.json")

shomMsgJsonFile = open("./data/database/shopMsg.json","r",encoding="utf8")
shopMsgJson = json.load(shomMsgJsonFile)
shomMsgJsonFile.close()

targetEmJson = open("./data/database/appEmoji.json", "r", encoding="utf8")
targetEmojis = json.load(targetEmJson)
targetEmojis = targetEmojis["targetEmojis"][["shushipy", "lenapy"][isLenapy]]

tmpCounter1, tmpCounter2, tmpCounter3 = 0, 0, 0
for tmpKey in ["shopMonthlyMsg","shopLastMonthlyMsg"]:
	for tmpInt in range(12):
		for tmpTxt in shopMsgJson[tmpKey][tmpInt]:
			tmpCounter1 += 1
			tmpCounter2 += len(tmpTxt[1])
			tmpCounter3 += len(tmpTxt[1].splitlines())

print("Btw, there are currently {0} monthly shop msg (present and past), for a total of {1} characters and {2} lines".format(tmpCounter1,tmpCounter2,tmpCounter3))

shopRandomMsg, shopEventEndYears, shopEventOneDay, shopMonthlyMsg, singingShopMsg, shopLastMonthlyMsg, lenaTipsMsgTabl, pnjDescriptions = shopMsgJson["shopPermaRdmMsg"], shopMsgJson["shopEventEndYears"], shopMsgJson["shopEventOneDay"], shopMsgJson["shopMonthlyMsg"], shopMsgJson["singingShopMsg"], shopMsgJson["shopLastMonthlyMsg"], shopMsgJson["lenaTips"], shopMsgJson["pnjDescriptions"]
shopAliceChristmasSong = shopMsgJson["christmas"]

randRollMsg = shopMsgJson["miscText"]["lena"]["roll"]
randChooseMsg = shopMsgJson["miscText"]["lena"]["choose"]

akiaSays = says(
	"Je suppose qu'il faut quelqu'un pour faire un remplacement.",
	"Désactivation du limiteur.",
	"CPU à 300%. Températeur annormalement élevée, mais conformément aux estimations.",
	"Processus tué avec succès.",
	"Le CPU a cessé de répondre.",
	"Merci.",
	"Résultat du combat : Succès.","Résultat du combat : Succès.","Résultat du combat : Echec.","Résultat du combat : Succès.","Résultat du combat : Succès.","Résultat du combat : Echec.",
	"Activation des programmes d'isolement de la menace.",
	"Score de style de {caster} anormalement élevé.","Réponse du module de réaction : Frustration niveau 2.","Chances de victoires reconsidérées à la hausse.","Un premier pas vers le succes.","Réduction des chances de succès...",
	"Niveau de puissance estimé au dessus du niveau 9000.","Niveau de puissance estimé au dessus du niveau 9000.","Constatation : L'ennemi a encaissé l'attaque","Constatation : Echec de l'attaque","Dégâts détectés...","Maneuvre d'esquive réalisée avec succès.",
	"Merci."
)

amandineSays = says(
	start="Numéro 3, parée",ultimate="C'est l'heure de sortir le grand jeu !",limiteBreak="PREND CA !",onDeath="Mmmmgn...",blueWinAlive="Mission accomplie"
)

global allReadyInWait, allReadyInWaitQuick
allReadyInWait, allReadyInWaitQuick = {}, {}

def randRep(liste : list):
	"""Return a random value from the list"""
	if type(liste) != list: liste = [liste]

	if len(liste) == 1: return liste[0]
	else: return liste[random.randint(0,len(liste)-1)]

ALLIES_EXP_GAIN = 10
ALLIES_EXP_BONUS = 1

toSanitize = ["\\", "#", "*", "_", "-"]
def sanitize(txt: str):
	for toReplace in toSanitize:
		txt = txt.replace(toReplace, "\\"+toReplace)
	
	return txt

returnButton = Button(style=ButtonStyle.SECONDARY, label="Retour",custom_id="return", emoji=PartialEmoji(name="◀️"))

def containerReduceEmojiNames(emb: Union[ContainerComponent, SectionComponent]):
	for indx, contComp in enumerate(emb.components):
		if contComp.type == 9: emb.components[indx] = containerReduceEmojiNames(emb=contComp)
		elif contComp.type == 10: emb.components[indx].content = reduceEmojiNames(contComp.content)
	return emb

def lenContainer(emb: Union[ContainerComponent, SectionComponent], count=0):
	for indx, contComp in enumerate(emb.components):
		if contComp.type == 9: count = lenContainer(contComp, count)
		elif contComp.type == 10: count += len(contComp.content)
	return count