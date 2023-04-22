"""
Constants module.
Here stand the first brick of the bot
"""
import os, shopMessageDownloader
from datetime import timedelta, datetime
from interactions import *
from interactions.ext.wait_for import setup
from typing import Union, List
from shopMsg import *

emLoading = '<a:loading:862459118912667678>'

FROM_LEFT, FROM_RIGHT, FROM_UP, FROM_DOWN, FROM_POINT = 0,1,2,3,4

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

areaMelee = [AREA_MONO,AREA_CIRCLE_1,AREA_CIRCLE_2,AREA_CIRCLE_3,AREA_CONE_2,AREA_CONE_3,AREA_LINE_2,AREA_LINE_3,AREA_DONUT_1,AREA_DONUT_2,AREA_DONUT_3,AREA_INLINE_2,AREA_INLINE_3]
areaDist = [AREA_DIST_3,AREA_DIST_4,AREA_DIST_5,AREA_DIST_6,AREA_DIST_7,AREA_BOMB_5,AREA_BOMB_6,AREA_BOMB_7]
areaMixte = []
notOrientedAreas = [AREA_CIRCLE_1,AREA_CIRCLE_2,AREA_CIRCLE_3,AREA_CIRCLE_4,AREA_CIRCLE_5,AREA_CIRCLE_6,AREA_CIRCLE_7,AREA_DONUT_1,AREA_DONUT_2,AREA_DONUT_3,AREA_DONUT_4,AREA_DONUT_5,AREA_DONUT_6,AREA_DONUT_7,AREA_INLINE_2,AREA_INLINE_3,AREA_INLINE_4,AREA_INLINE_5,AREA_DIST_3,AREA_DIST_4,AREA_DIST_5,AREA_DIST_6,AREA_DIST_7,AREA_BOMB_5,AREA_BOMB_6,AREA_BOMB_7,AREA_LOWEST_HP_ALLIE]

EmIcon = [None,['<:ikaRed:866459224664702977>','<:ikaOrange:866459241886646272>','<:ikaYellow:866459268520607775>','<:ikaGreen:866459285982937108>','<:ikaLBlue:866459302319226910>','<:ikaBlue:866459319049650206>','<:ikaPurple:866459331254550558>','<:ikaPink:866459344173137930>','<:ikaWhite:871149538554044466>','<:ikaBlack:871149560284741632>'],['<:takoRed:866459004439756810>','<:takoOrange:866459027562954762>','<:takoYellow:866459052132532275>','<:takoGreen:866459073910145025>','<:takoLBlue:866459095875190804>','<:takoBlue:866459141077860352>','<:takoPurple:866459162716536892>','<:takoPink:866459203949166593>','<:takoWhite:871149576965455933>','<:takoBlack:871151069193969714>'],['<:octarian:866461984018137138>'],['<:baseIka:913847108640047174>',"<:baseTako:913847092835930172>","<:empty_squid:913911277548601344>","<:empty_octo:913911290299289632>",'<:littleStar:925860806602682369>','<:ikaCatLine:930383582898315284>','<:ikaCatBody:930383603026776064>','<:takoCatLine:930383560630734848>','<:takoCatBody:930397525888880711>','<:komoriLine:930804436861857872>','<:komoriBody:930798973386641448>','<:birdLine:930906003967443034>','<:birdColor:930908372969095248>','<:skeletonLine:930910501691588658>','<:skeletonColor:931190496427139112>','<:fairyLine:935335398094274621>','<:fairyColor:935335413005037600>','<:fairy2Line:935336370774351902>','<:fairy2Color:935336353284096040>']]
EmCount = ('0️⃣','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🇦','🇧','🇨','🇩','🇪','🇫')

for cmpt in range(AREA_INLINE_5+1):
    if cmpt not in [AREA_RANDOMENNEMI_1,AREA_RANDOMENNEMI_2,AREA_RANDOMENNEMI_3,AREA_RANDOMENNEMI_4,AREA_RANDOMENNEMI_5,AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES] + areaMelee + areaDist:
        areaMixte.append(cmpt)

areaNames = ["Monocible", "Cercle de rayon 1", "Cercle de rayon 2", "Cercle de rayon 3", "Cercle de rayon 4", "Cercle de rayon 5", "Cercle de rayon 6", "Cercle de rayon 7", "Tous les alliés", "Tous les ennemis", "Tous les combattants", "Cone simple", "Cone Large", "Cone Large", "Cone Large", "Cone Large", "Cone Large", "Ligne de 2 de longueur", "Ligne de 3 de longueur", "Ligne de 4 de longueur", "Ligne de 5 de longueur", "Ligne de 6 de longueur", "Donut de 1 de rayon", "Donut de 2 de rayon", "Donut de 3 de rayon", "Donut de 4 de rayon","Donut de 5 de rayon", "Donut de 6 de rayon", "Donut de 7 de rayon", "Anneau Distance de 1 de largeur", "Anneau Distance de 2 de largeur", "Anneau Distance de 3 de largeur", "Anneau Distance de 4 de largeur", "Anneau Distance de 5 de largeur", "Arc de Cercle de 1 de rayon", "Arc de Cercle de 2 de rayon", "Arc de Cercle de 3 de rayon", "1 ennemi aléatoire", "2 ennemis aléatoires", "3 ennemis aléatoires", "4 ennemis aléatoires", "5 ennemis aléatoires", "Croix de 2 cases", "Croix de 3 cases", "Croix de 4 cases", "Crois de 5 cases","Lobbée de 5 cases","Lobbée de 6 cases","Lobbée de 7 cases","Allié le plus blessé"]
allArea = range(0, AREA_BOMB_7)
listNumberEmoji = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟","▶️","⏸️","⏯️","⏹️","⏺️","⏭️","⏮️","⏩","⏪","⏫","⏬","◀️","🔼","🔽","➡️","⬅️","⬆️","⬇️","↗️","↘️","↙️","↖️","↕️","↔️"]

rangeAreaEmojis = ["<:rangeMono:1032293272783179796>", "<:rangeCircle:1032293347869593691>(1)", "<:rangeCircle:1032293347869593691>(2)", "<:rangeCircle:1032293347869593691>(3)", "<:rangeCircle:1032293347869593691>(4)", "<:rangeCircle:1032293347869593691>(5)", "<:rangeCircle:1032293347869593691>(6)", "<:rangeCircle:1032293347869593691>(7)", "<:rangeAllAllies:1032512884351172668>", "<:rangeAllEnemies:1032512939992809502>", "<:rangeAllEntities:1032512991859576933>", "<:rangeCone:1032293500093480970>(1)", "<:rangeCone:1032293500093480970>(2)", "<:rangeCone:1032293500093480970>(2)", "<:rangeCone:1032293500093480970>(3)", "<:rangeCone:1032293500093480970>(4)", "<:rangeCone:1032293500093480970>(5)", "<:rangeLine:1032293431298494595>(2)", "<:rangeLine:1032293431298494595>(3)", "<:rangeLine:1032293431298494595>(4)", "<:rangeLine:1032293431298494595>(5)", "<:rangeLine:1032293431298494595>(6)", "<:rangeDonut:1032294133219459103>(1)", "<:rangeDonut:1032294133219459103>(2)", "<:rangeDonut:1032294133219459103>(3)", "<:rangeDonut:1032294133219459103>(4)","<:rangeDonut:1032294133219459103>(5)", "<:rangeDonut:1032294133219459103>(6)", "<:rangeDonut:1032294133219459103>(7)", "<:rangeDist:1032294217415921726>(1)", "<:rangeDist:1032294217415921726>(2)", "<:rangeDist:1032294217415921726>(3)", "<:rangeDist:1032294217415921726>(4)", "<:rangeDist:1032294217415921726>(5)", "<:rangeArc:1033268272285614080>(1)", "<:rangeArc:1033268272285614080>(2)", "<:rangeArc:1033268272285614080>(3)", "<:rangeRdmEnemie:1032513037351010335>(1)", "<:rangeRdmEnemie:1032513037351010335>(2)", "<:rangeRdmEnemie:1032513037351010335>(3)", "<:rangeRdmEnemie:1032513037351010335>(4)", "<:rangeRdmEnemie:1032513037351010335>(5)", "<:rangeCross:1032294049027194940>(2)", "<:rangeCross:1032294049027194940>(3)", "<:rangeCross:1032294049027194940>(4)", "<:rangeCross:1032294049027194940>(5)","<:rangeLob:1032294266988408833>(5)","<:rangeLob:1032294266988408833>(6)","<:rangeLob:1032294266988408833>(7)","<:INeedHealing:881587796287057951>"]
areaEmojis = ["<:areaMono:1032293314130616400>", "<:areaCircle:1032293380379656192>(1)", "<:areaCircle:1032293380379656192>(2)", "<:areaCircle:1032293380379656192>(3)", "<:areaCircle:1032293380379656192>(4)", "<:areaCircle:1032293380379656192>(5)", "<:areaCircle:1032293380379656192>(6)", "<:areaCircle:1032293380379656192>(7)", "<:areaAllAllies:1032512909982564443>", "<:areaAllEnemies:1032512965850710026>", "<:areaAllEntities:1032513013879681095>", "<:areaCone:1032293578858307624>(1)", "<:areaCone:1032293578858307624>(2)", "<:areaCone:1032293578858307624>(3)", "<:areaCone:1032293578858307624>(4)", "<:areaCone:1032293578858307624>(5)", "<:areaCone:1032293578858307624>(6)", "<:areaLine:1032293461803675708>(2)", "<:areaLine:1032293461803675708>(3)", "<:areaLine:1032293461803675708>(4)", "<:areaLine:1032293461803675708>(5)", "<:areaLine:1032293461803675708>(6)", "<:areaDonut:1032294180451520552>(1)", "<:areaDonut:1032294180451520552>(2)", "<:areaDonut:1032294180451520552>(3)", "<:areaDonut:1032294180451520552>(4)","<:areaDonut:1032294180451520552>(5)", "<:areaDonut:1032294180451520552>(6)", "<:areaDonut:1032294180451520552>(7)", "<:areaDist:1032294242783080518>(1)", "<:areaDist:1032294242783080518>(2)", "<:areaDist:1032294242783080518>(3)", "<:areaDist:1032294242783080518>(4)", "<:areaDist:1032294242783080518>(5)", "<:areaArc:1033268300412616747>(1)", "<:areaArc:1033268300412616747>(2)", "<:areaArc:1033268300412616747>(3)", "<:areaRdmEnemie:1032513060524539904>(1)", "<:areaRdmEnemie:1032513060524539904>(2)", "<:areaRdmEnemie:1032513060524539904>(3)", "<:areaRdmEnemie:1032513060524539904>(4)", "<:areaRdmEnemie:1032513060524539904>(5)", "<:areaCross:1032294077653328004>(2)", "<:areaCross:1032294077653328004>(3)", "<:areaCross:1032294077653328004>(4)", "<:areaCross:1032294077653328004>(5)","<:areaLob:1032294287657934910>(5)","<:areaLob:1032294287657934910>(6)","<:areaLob:1032294287657934910>(7)","<:INeedHealing:881587796287057951>"]

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
TRIGGER_HP_ENDER_70 = 9

allTriggers = [TRIGGER_PASSIVE, TRIGGER_DAMAGE, TRIGGER_END_OF_TURN, TRIGGER_DEATH,TRIGGER_DEALS_DAMAGE, TRIGGER_INSTANT, TRIGGER_START_OF_TURN, TRIGGER_ON_REMOVE, TRIGGER_AFTER_DAMAGE,TRIGGER_HP_ENDER_70]
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
    "lorsque les PV du porteur tombent en dessous de 70%"
]

DMGBONUSATLVL50, HEALBONUSATLVL50, ARMORBONUSATLVL50, ARMORMALUSATLVL0 = 50, 15, 15, 20
DMGBONUSPERLEVEL, HEALBONUSPERLEVEL, ARMORLBONUSPERLEVEL = DMGBONUSATLVL50/50/100, HEALBONUSATLVL50/50/100, ARMORBONUSATLVL50/50/100
SUDDENDEATHDMG = 20

# Skills and effects types
TYPE_ARMOR = 0
TYPE_INDIRECT_DAMAGE = 1
TYPE_INDIRECT_HEAL = 2
TYPE_INDIRECT_REZ = 3
TYPE_BOOST = 4
TYPE_RESURECTION = 5
TYPE_DAMAGE = 6
TYPE_MALUS = 7
TYPE_HEAL = 8
TYPE_UNIQUE = 9
TYPE_SUMMON = 10
TYPE_PASSIVE = 11
TYPE_DEPL = 12

allTypeNames = ["Armure", "Dégâts indirects", "Soins Indirects", "Résurection indirecte","Boost", "Resurection", "Dégâts", "Malus", "Soins", "Unique", "Invocation", "Passif", "Déployable"]
friendlyTypes, hostilesTypes = [TYPE_ARMOR,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ,TYPE_HEAL,TYPE_BOOST,TYPE_RESURECTION], [TYPE_INDIRECT_DAMAGE,TYPE_DAMAGE,TYPE_MALUS]
allTypes = range(0, 12)

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
PURCENTAGE = 11
FIXE = 12
HARMONIE = 13

ACT_HEAL = 0
ACT_BOOST = 1
ACT_SHIELD = 2
ACT_DIRECT = 3
ACT_INDIRECT = 4

BONUSPOINTPERLEVEL, MAXBONUSPERSTAT, MAJORBONUS = 2, 55, 50

nameStats, nameStats2 = ["Force", "Endurance", "Charisme", "Agilité","Précision", "Intelligence", "Magie"], ["Résistance", "Pénétration", "Critique"]
allStatsNames = nameStats+nameStats2+["Soins","Boosts","Armures","Dégâts Directs","Dégâts Indirects"]
statsEmojis = ["<:str:1012308654780850267>","<:sta:1012308718140002374>","<:cha:1012308755121188905>","<:agi:1012308798494482482>","<:pre:1012308901498208286>","<:int:1012308834661961748>","<:mag:1012308871525699604>","<:res:1012308953721487392>","<:per:1012309032867991613>","<:cri:1012309064824406116>","<:heal:1012309125083959306>","<:bost:1012309093509238814>","<:arm:1012309148802748456>","<:dir:1012309179245019177>","<:idir:1012309203249004614>"] + list(range(99))

# Status for entities
STATUS_ALIVE, STATUS_DEAD, STATUS_RESURECTED, STATUS_TRUE_DEATH = 0, 1, 2, 3

DANGERUPPERSTAR = 5

# Aspirations
BERSERK, OBSERVATEUR, POIDS_PLUME, IDOLE, PREVOYANT, TETE_BRULE, MAGE, ALTRUISTE, ENCHANTEUR, PROTECTEUR, VIGILANT, SORCELER, INOVATEUR, ATTENTIF, MASCOTTE, ASPI_NEUTRAL = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
inspi = ["Berserkeur", "Observateur", "Poids plume", "Idole", "Prévoyant", "Tête brulée", "Mage","Altruiste", "Enchanteur", "Protecteur", "Vigilant", "Sorcier", "Inovateur", "Attentif", "Mascotte", "Neutre"]
aspiEmoji = ["<:ber:985007311997263932>","<:obs:985007736360165407>","<:pplume:985007345648148541>","<:ido:985007596656275476>","<:pre:985007771613274133>","<:tbrule:985007436538740766>","<:ma:985010178900500561>","<:alt:985007803322224720>","<:enc:985007558156755004>","<:pro:985009037546487850>","<:vig:985009013097910302>","<:sor:985007632639205458>","<:inov:985007247656632360>","<:att:985007703707500555>","<:masc:1009814577262895224>","<:neutral:985011113458536538>"]
lbNames = ["Lames de l'Ombre","Odre de Tir : Drône 3.4.8 Alpha","Frappe de Silicia","Apothéose planétaire","Armure Galactique","Fracture Dimentionnelle","Colère de Nacialisla","Bénédiction de Nacialisla","Desctruction Silicienne","Pousée d'Espoir","Grandeur de Nacialisla","Cataclysme Powehien","Avenir Prometeur","Chef d'Oeuvre Balistique","Bénédiction Fleurale"]
lbDesc = ["Inflige des dégâts à l'ennemi ciblé et vous soigne d'une partie des dégâts infligés","Inflige des dégâts à l'ennemi ciblé et augmente vos statistiques","Inflige des dégâts à l'ennemi ciblé et le repousse violament","Augmente les statistiques des alliés à portée et réanime ceux qui sont vaincus","Octroi une armure aux alliés à portée et augmente leurs statistiques offensives","Inflige des dégâts à l'ennemi ciblé et réduit ses PV max","Inflige dégâts dans une large zone autour de l'ennemi ciblé","Soigne les alliés à portée et leur donne un effet de régénération tout en réanimant ceux qui étaient vaincus","Inflige des dégâts dans une large zone autour de l'ennemi ciblé et vous octroit une armure","Octroi une armure aux alliés à portée et augmente leurs statistiques défensives","Soigne les alliés à portée en réanimant ceux vaincus tout en réduisant vos dégâts subis","Inflige des dégâts dans une large zone autour de l'ennemi ciblé et lui inflige un effet de dégâts indirects multi-cibles","Augmente les statistiques des alliés à portée et réduit leurs dégâts subis pendant la même durée","Inflige des dégâts en ligne droite sur l'ennemi ciblé et augmente vos statistiques","Augmente les statistiques des alliés alentours et réduits la défense des ennemis à portée"]
recommandedStat = [
    [STRENGTH, ENDURANCE, AGILITY],
    [STRENGTH, PRECISION, ENDURANCE],
    [AGILITY, STRENGTH, ENDURANCE],
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
    [STRENGTH, RESISTANCE, ENDURANCE],
    [STRENGTH, PRECISION, ACT_DIRECT_FULL],
    [AGILITY, STRENGTH, RESISTANCE],
    [CHARISMA, ACT_BOOST_FULL, INTELLIGENCE],
    [INTELLIGENCE, ACT_SHIELD_FULL, PRECISION],
    [STRENGTH, PRECISION, CRITICAL],
    [MAGIE, PRECISION, ACT_DIRECT_FULL],
    [CHARISMA,ACT_HEAL_FULL, PRECISION],
    [MAGIE, ENDURANCE, RESISTANCE],
    [INTELLIGENCE, ENDURANCE, RESISTANCE],
    [CHARISMA, ENDURANCE, RESISTANCE],
    [MAGIE, INTELLIGENCE, ACT_INDIRECT_FULL],
    [INTELLIGENCE, ACT_SHIELD_FULL, CHARISMA],
    [STRENGTH, INTELLIGENCE, CRITICAL],
    [ENDURANCE, ACT_BOOST_FULL, RESISTANCE],
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
while len(aspiEmoji) < len(inspi):
    aspiEmoji.append('<a:menacing:917007335220711434>')

BERS_LIFE_STEAL = 35
MASC_MAX_BOOST = 25
MASC_MIN_BOOST = 1
MASC_LVL_CONVERT = 10

dptAspi = [BERSERK,POIDS_PLUME,TETE_BRULE,ENCHANTEUR,OBSERVATEUR,ATTENTIF,MAGE,SORCELER]
healAspi = [ALTRUISTE,VIGILANT]
armorAspi = [PREVOYANT,PROTECTEUR]
boostAspi = [IDOLE,INOVATEUR,MASCOTTE]

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
    [50, 40, 25, 75, 35, 10, 40],
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

for a in range(0, len(inspi)):                           # Aspi base stats verification
    summation = 0
    for b in range(7):
        try:
            summation += aspiStats[a][b]
        except:
            pass

    if summation != 275:
        print("{0} n'a pas le bon cumul de stats : {1}".format(
            inspi[a], summation))

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
ELEMENT_UNIVERSALIS_PREMO = 9

FIREDMGBUFF = WATERDMGBUFF = EARTHDMGBUFF = AIRDMGBUFF = DARKNESSDMGBUFF = 5
LIGHTHEALBUFF = 10
TIMEHEALBUFF = TIMEDMGBUFF = 10
TIMESHIELDABS = 50
SPACEBONUSBUFF, SPACEMALUSRESIST = 10, 5

elemEmojis = ["<:neutral:921127224596385802>", "<:fire:918212781168275456>", "<:water:918212797320536124>", "<:air:918592529480446002>", "<:earth:918212824805801984>","<:light:918212861757653053>", "<:darkness:918212877419175946>", '<:space:918212897967075329>', '<:time:918212912408051814>', "<:univ:936302039456165898>"]
secElemEmojis = ["<:em:866459463568850954>", "<:secFeu:932941340612894760>", "<:secEau:932941360858820618>", "<:secAir:932941299559063573>","<:secTerre:932941317804273734>", "<:secLum:932941251597201438>", "<:secTen:932941234501222410>", "<:secTempo:932941280785338389>", "<:secAst:932941221331075092>"]
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
    "{1} Pénétration : + 5\nAugmente de **{0}%** les **dégâts de zones** et les **dégâts à distances** infligés (Cumulable)".format(FIREDMGBUFF,statsEmojis[PERCING]),
    "{1} Précision : + 10\nAugmente de **{0}%** les **dégâts monocibles** et les **dégâts à distances** infligés (Cumulable)".format(WATERDMGBUFF,statsEmojis[PRECISION]),
    "{1} Agilité : + 10\nAugmente de **{0}%** les **dégâts de zones** et les **dégâts en mêlée** infligés (Cumulable)".format(AIRDMGBUFF,statsEmojis[AGILITY]),
    "{1} Résistance : + 5\nAugmente de **{0}%** les **dégâts monocibles** et les **dégâts en mêlée** infligés (Cumulable)".format(EARTHDMGBUFF,statsEmojis[RESISTANCE]),
    "Augmente de **{0}%** la puissance des **compétences** de **soins** et de **réanimation**, la puissance des effets secondaires soignants de vos compétences ainsi que la puissance des **armures données**".format(LIGHTHEALBUFF),
    "Augmente de **{0}%** tous les **dégâts infligés** ainsi que la puissance des effets de **dégâts indirects** se déclanchant en **début ou en fin de tour** (Cumulable)".format(DARKNESSDMGBUFF),
    "Augmente de **{0}%** la puissance des **bonus donnés ou reçus** (Non Cumulable) et réduit de **{1}%** la puissance des **malus reçus**".format(SPACEBONUSBUFF,SPACEMALUSRESIST),
    "Augmente de **{0}%** la puissance des effets de **soins indirects** et des effets de **dégâts indirects** se déclanchant lors de **leur retrait** octroyés, et augmente de **{1}%** la quantié de **dégâts** supplémentaires **absorbés** par vos **effets d'armures**".format(TIMEHEALBUFF,TIMESHIELDABS)
]
elemSecPassifDesc = [
    "Aucun passif secondaire",
    "Soins donnés et reçus : +5%\nArmures données et reçues : -5%",
    "Armures données et reçues : +5%\nSoins données et reçus : -5%",
    "Puissance des bonus et malus données et reçus : +5%",
    "Dégâts sur Armure infligés et reçus : +5%",
    "Dégâts directs infligés et reçus : +5%",
    "Dégâts directs infligés et reçus : -5%",
    "Dégâts directs de zone infligées et reçus : +5%",
    "Dégâts directs monocibles infligés et reçus : +5%"
]

# AoE stuff
AOEDAMAGEREDUCTION = 0.35
AOEMINDAMAGE = 0.2

def uniqueEmoji(emoji) -> List[List[str]]:
    return [[emoji, emoji], [emoji, emoji], [emoji, emoji]]

def sameSpeciesEmoji(team1, team2):
    return [[team1, team2], [team1, team2], [team1, team2]]

dangerEm = sameSpeciesEmoji('<a:dangerB:898372745023336448>', '<a:dangerR:898372723150041139>')
untargetableEmoji = uniqueEmoji('<:untargetable:899610264998125589>')

# List of guild ids for the bots
ShushyCustomIcons = [881900244487516180]
LenaCustomIcons = [881632520830087218, 881633183425253396]

stuffIconGuilds = [866782432997015613, 878720670006132787, 887756868787769434, 887846876114739261, 904164080204513331,908551466988486667, 914608569284964392, 922684334010433547, 928202839136825344, 933783830341484624, 953212496930562098, 1006418791669956698, 1025301457458704385]
weaponIconGuilds = [866363139931242506, 878720670006132787, 887756868787769434,938379180851212310, 887846876114739261, 916120008948600872, 911731670972002374, 989526511285571614]

# For some time related stuff. Time from server != time from France
if not(os.path.exists("../Kawi")):
    horaire = timedelta(hours=2)
else:
    horaire = timedelta(hours=0)

# Are we on the livebot or the test bot ?
isLenapy = not(os.path.exists("../Kawi"))

# Level to unlock skill slot
lvlToUnlockSkill = [0, 0, 0, 5, 15, 25, 35]

SKILL_GROUP_NEUTRAL, SKILL_GROUP_HOLY, SKILL_GROUP_DEMON = 0, 1, 2
skillGroupNames = ["neutre", "divine", "démoniaque"]

COUNTERPOWER = 35

shopRepatition = [4, 5, 8, 3]                 # Shop's item category length
if datetime.now().month == 9:
    cpShopRandomMsg = shopRandomMsg[:]
    for cmpt in range(len(cpShopRandomMsg)):
        if "{feli}" in cpShopRandomMsg[cmpt]:
            try:
                shopRandomMsg.remove(cpShopRandomMsg[cmpt])
            except:
                pass

# Same, but for the roll command
rollMessage = ["Selon toute vraisemblance ce sera un **{0}**", "Puisse la chance être avec toi... **{0}** !", "Alors Alice tu as obtenu combien ? **{0}** ? **{0}** alors","Sur 100, les chances que la relation Akrisk tienne debout ? Hum... **{0}**", "Le nombre de lances que tu va avoir à esquiver est... **{0}**"]

randomEmojiFight = [
    '<:ffsad:896113677550366740>',
    '<:ffboude:875347226170384454>',
    '<:ffshrug:895280749366878258>',
    '<:ffbored:889900326902186045>'
]

lenRdmEmojiFight = len(randomEmojiFight)
mauvaisePerdante = "\n\nUnexpected situation: The enemy has won"

randChooseMsg = [
    "À quoi bon, de toutes façons tu vas choisir ce qui t'interresse vraiment\nMais bon voilà",
    "Je doute que tu tiennes compte de mon avis mais j'ai choisi",
    "Selon l'allignement des étoiles, tu va devoir prendre",
    "D'après les résidus de thé dans ma tasse...",
]

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
            self.redWinAlive,
            self.redWinDead,
            self.redLoose,
            self.blockBigAttack,
            self.reactBigRaiseAllie,
            self.reactBigRaiseEnnemy,
            self.bigRaise,
            self.reactEnnemyKilled,
            self.reactAllyKilled
        ]

    def fromTabl(self, tabl: list):
        for cmpt in range(len(tabl)):
            if type(tabl[cmpt]) == str:
                tabl[cmpt] = tabl[cmpt].replace("\\","")

        self.start = tabl[0]
        self.ultimate = tabl[1]
        self.limiteBreak = tabl[2]
        self.onKill = tabl[3]
        self.onDeath = tabl[4]
        self.onResurect = tabl[5]
        self.blueWinAlive = tabl[6]
        self.blueWinDead = tabl[7]
        self.blueLoose = tabl[8]
        self.redWinAlive = tabl[9]
        self.redWinDead = tabl[10]
        self.redLoose = tabl[11]
        self.blockBigAttack = tabl[12]
        self.reactBigRaiseAllie = tabl[13]
        self.reactBigRaiseEnnemy = tabl[14]
        self.bigRaise = tabl[15]
        self.reactEnnemyKilled = tabl[16]
        self.reactAllyKilled = tabl[17]

        return self

lenaSays = says(
    start="Lena, parée à faire feu.",
    ultimate="Hey {target} ! J'ai un {skill} avec ton nom dessus !",
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
    reactEnnemyKilled="Pas trop {killer}",
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
    start="HEY EVERY       ! IT'S ME, SPAMTON G. SPAMTON!",
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
    dodge=["T'es sûr d'avoir les yeux en face des trous {caster} ?","Bien essayé","Pas cette fois !"],
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
    ultimate="Les rêves sont plus réels que vous pensez !",
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
klikliSays = says(start="Ok. Je vais m'en occuper rapidement",limiteBreak="OK, VOILÀ POUR VOUS !",onKill="Si tu veux revenir, j't'ai pas encore montrer tout ce dont je suis capable.",reactEnnemyKilled="Pff, j'peux le faire toute seule tu sais ?",ultimate="J'espère que tu as les yeux grands ouverts {target} !",redWinAlive="J'espère que vous en avez pris de la graine.")
altySays = says(start="'K, je vais faire de mon mieux",onKill="Désolée...",onResurect="Ok, second round !",reactAllyKilled="{downed} !",redWinAlive="Oulà, ça va aller ? Je crois qu'on y est allé un peu fort...",redWinDead="`Rigole` Bien joué tout le monde !")

shehisaSays = says(start="Ok, si on suit le plan, tout se passera bien",onKill="Tu aurais pu attendre que je soit partie avant de creuver quand même.",onDeath="Humf, c'était pas prévu ça...",reactAllyKilled="On lache rien !",reactBigRaiseEnnemy="C'était trop beau pour être vrai",reactAllyLb="Wowowo tu nous as fait quoi là {caster} ?",blueWinAlive="Tout s'est déroulé comme prévu",redWinAlive="Tout s'est déroulé selon le plan")

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
procurTempStuff = {
    "Shushi Cohabitée":[0,
        ["Barrête de la cohabitation","dualHat","<:coaBar:911659734812229662>"],
        ["Robe de la cohabitation","dualDress",'<:coaDress:911659797076660294>'],
        ["Bottines de la cohabitation","dualBoost",'<:coaBoots:911659778995007528>'],
        [[0,0],[5,0.2],[2,0.3],[0.5,1],[0.5,1],[2,0.8],[2,0.8],[1,0.2],[0.5,0.3],[0.8,0.2]]
    ],
    "Luna prê.":[250,
        ["Boucle d'oreille ombrale",'lunaDarkPendant','<:linapendant:890599104902754326>'],
        ["Robe de soubrette ombrale ",'lunaDarkMaidDress','<:linadress:890598423152185364>'],
        ["Ballerines ombrales",'lunaDarkFlats','<:linaflats:890598400624586763>'],
        [[1.2,2.55],[1.15,0.4],[0.8,0.5],[1,1.2],[1,0.6],[0.2,0.3],[0,0],[0.25,0.35],[0.25,0.35],[0,0]]
    ],
    "Iliana prê.":[350,
        ["Casque de la neko de la lueur ultime", 'ilianaPreHead','<:zenithHead:913170464581484554>'],
        ["Armure de la neko de la lueur ultime", 'ilianaPreArmor','<:zenithArmor:913170492452646922>'],
        ["Sorolets de la neko de la lueur ultime", 'ilianaPreBoots','<:zenithBoots:913170512564334623>'],
        [[0.2,0.1],[1,2.5],[1,3],[0.5,0.9],[1.2,0.7],[3,0.05],[5,0.05],[1.0,0.15],[1,0.03],[1,0]]
    ],
    "Clémence Exaltée":[500,
        ["Boucles d'oreilles runiques","clemRune",'<:clemEarRings:920297359848636458>'],
        ["Veste sanguine",'clemRune','<:clemVeste:920300283068833874>'],
        ["Bottes sanguines","clemRune","<:clemBoots:920297554330157056>"],
        [[0.6,0.2],[2,1],[0.5,0.5],[2,.05],[1,0.3],[1.2,0.8],[1.7,1],[0.5,0.25],[1,0.031],[1,0.0005]]
    ],
    "Alice Exaltée":[0,
        ["Noeud en ruban chauve-souris","aliceExHat","<:batRuban:887328511222763593>"],
        ["Veste et jupe rose pâle","aliceExDress",'<:VesteEtJupeRose:877658944045219871>'],
        ["Ballerines roses pâles","aliceExShoes",'<:pinkFlat:867158156139692042>'],
        [[0.1,0.05],[0.5,0.4],[1.1,1.5],[0.8,0.25],[0.65,0.2],[1,1.35],[0.6,0.4],[1.2,0.15],[0.5,0.1],[1,0.1]]
    ],
    "Lia Ex":[150,
        ["Masque de démon renard","liaExHat",'<:liaMask:1012669701068968026>'],
        ["Robe des vents",'liaExDress','<:vert:928200434278100992>'],
        ["Sandales des vents","liaExShoes",'<:sandalGreen:928203305052696616>'],
        [[0.1,0.01],[0.7,0.5],[1,1.2],[2,1.2],[1,1.2],[0.5,1],[1,1.15],[0.2,0.35],[0.1,0.3],[0,0]]
    ]
}

alphaTabl=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
def getAutoId(id:str,reverse=False):
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
    3: createCapSkillDict("Shehisa","<:shehisa:919863933320454165>","Réduit la progression des malus d'agression en fonction des actions des équipiers de **__{0}%__**\nDe plus, octroi aux équipiers **__{1}%__** de chances d'effectuer une *Contre-Attaque* lorsqu'ils esquivent une attaque",[15,20,25],[5,10,15],"Ils peuvent pas nous toucher si nous sommes pas là"),
    4: createCapSkillDict("Liu","<:liu:908754674449018890>","Augmente de **__{0}%__** la probabilité de tous les équipiers d'effectuer une *Parade* lorsqu'il est attaqué\nDe plus, octroi aux équipiers **__{1}%__** de chances d'effectuer une *Contre-Attaque* lorsqu'ils parent une attaque",[10,15,20],[15,20,25],"Il suffit de garder la forme"),
    5: createCapSkillDict("Edelweiss","<:edelweiss:918451422939451412>","En début de tour de table, octroi aux **__{0}__** équipiers ayant le moins de PV une armure équivalante à **__{1}%__** des PV maximums de l'équipier qui en possède le plus",[1,2,3],[5,7.5,10],"Je vous ferais pas faux-bond..."),
    6: createCapSkillDict("Elina","<:elina:950542889623117824>","En début de tour de table, l'équipier ayant le moins de PV récupère **__{0}%__** de ses PV manquants et reçois des dégâts réduits de __**{1}%**__ pour le tour en cour",[10,12.5,15],[5,7.5,10],"Huh ?"),
    7: createCapSkillDict("Icealia","<:icealia:909065559516250112>","Lorsqu'un équipier passe en dessous de __**{0}%**__ de ses PV maximums, il reçoit une armure équivalante à __**{1}%**__ de ses PV maximus pendant 3 tours (une fois par combat)",[10,12.5,15],[10,15,20],"Je vais faire de mon mieux")
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

def reducedEmojiNames(string:str) -> str:
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
