"""
Constants module.
Here stand the first brick of the bot
"""
from datetime import timedelta, datetime
import os
from sre_constants import IN
from index import *
from discord_slash.utils.manage_components import *


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

areaMelee = [AREA_MONO,AREA_CIRCLE_1,AREA_CIRCLE_2,AREA_CIRCLE_3,AREA_CONE_2,AREA_CONE_3,AREA_LINE_2,AREA_LINE_3,AREA_DONUT_1,AREA_DONUT_2,AREA_DONUT_3,AREA_INLINE_2,AREA_INLINE_3]
areaDist = [AREA_DIST_3,AREA_DIST_4,AREA_DIST_5,AREA_DIST_6,AREA_DIST_7]
areaMixte = []
notOrientedAreas = [AREA_CIRCLE_1,AREA_CIRCLE_2,AREA_CIRCLE_3,AREA_CIRCLE_4,AREA_CIRCLE_5,AREA_CIRCLE_6,AREA_CIRCLE_7,AREA_DONUT_1,AREA_DONUT_2,AREA_DONUT_3,AREA_DONUT_4,AREA_DONUT_5,AREA_DONUT_6,AREA_DONUT_7,AREA_INLINE_2,AREA_INLINE_3,AREA_INLINE_4,AREA_INLINE_5,AREA_DIST_3,AREA_DIST_4,AREA_DIST_5,AREA_DIST_6,AREA_DIST_7]

for cmpt in range(AREA_INLINE_5+1):
    if cmpt not in [AREA_RANDOMENNEMI_1,AREA_RANDOMENNEMI_2,AREA_RANDOMENNEMI_3,AREA_RANDOMENNEMI_4,AREA_RANDOMENNEMI_5,AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES] + areaMelee + areaDist:
        areaMixte.append(cmpt)

areaNames = ["Monocible", "Cercle de rayon 1", "Cercle de rayon 2", "Cercle de rayon 3", "Cercle de rayon 4", "Cercle de rayon 5", "Cercle de rayon 6", "Cercle de rayon 7", "Tous les alliés", "Tous les ennemis", "Tous les combattants", "Cone simple", "Cone Large", "Cone Large", "Cone Large", "Cone Large", "Cone Large", "Ligne de 2 de longueur", "Ligne de 3 de longueur", "Ligne de 4 de longueur", "Ligne de 5 de longueur", "Ligne de 6 de longueur", "Donut de 1 de rayon", "Donut de 2 de rayon", "Donut de 3 de rayon", "Donut de 4 de rayon","Donut de 5 de rayon", "Donut de 6 de rayon", "Donut de 7 de rayon", "Anneau Distance de 1 de largeur", "Anneau Distance de 2 de largeur", "Anneau Distance de 3 de largeur", "Anneau Distance de 4 de largeur", "Anneau Distance de 5 de largeur", "Arc de Cercle de 1 de rayon", "Arc de Cercle de 2 de rayon", "Arc de Cercle de 3 de rayon", "1 ennemi aléatoire", "2 ennemis aléatoires", "3 ennemis aléatoires", "4 ennemis aléatoires", "5 ennemis aléatoires", "Croix de 2 cases", "Croix de 3 cases", "Croix de 4 cases", "Crois de 5 cases"]
allArea = range(0, 46)
listNumberEmoji = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟","▶️","⏸️","⏯️","⏹️","⏺️","⏭️","⏮️","⏩","⏪","⏫","⏬","◀️","🔼","🔽","➡️","⬅️","⬆️","⬇️","↗️","↘️","↙️","↖️","↕️","↔️"]
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

allTriggers = [TRIGGER_PASSIVE, TRIGGER_DAMAGE, TRIGGER_END_OF_TURN, TRIGGER_DEATH,TRIGGER_DEALS_DAMAGE, TRIGGER_INSTANT, TRIGGER_START_OF_TURN, TRIGGER_ON_REMOVE, TRIGGER_AFTER_DAMAGE]
triggersTxt = [
    "passivement",
    "lorsque le porteur reçoit des dégâts directs",
    "à la fin du tour du porteur",
    "à la mort du porteur",
    "lorsque le porteur inflige des dégâts directs",
    "lors de la pose de cet effet",
    "au début du tour du porteur",
    "lors du retrait de cet effet",
    "après que le porteur ai infligé des dégâts directs"
]

DMGBONUSATLVL50, HEALBONUSATLVL50, ARMORBONUSATLVL50, ARMORMALUSATLVL0 = 65, 15, 30, 20
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

tablTypeStr = ["Armure", "Dégâts indirects", "Soins Indirects", "Résurection indirecte","Boost", "Resurection", "Dégâts", "Malus", "Soins", "Unique", "Invocation", "Passif"]
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

nameStats, nameStats2 = ["Force", "Endurance", "Charisme", "Agilité","Précision", "Intelligence", "Magie"], ["Résistance", "Pénétration", "Critique"]
allStatsNames = nameStats+nameStats2+["Soins","Boosts","Armures","Dégâts Directs","Dégâts Indirects"]
statsEmojis = ["<:str:1012308654780850267>","<:sta:1012308718140002374>","<:cha:1012308755121188905>","<:agi:1012308798494482482>","<:pre:1012308901498208286>","<:int:1012308834661961748>","<:mag:1012308871525699604>","<:res:1012308953721487392>","<:per:1012309032867991613>","<:cri:1012309064824406116>","<:heal:1012309125083959306>","<:bost:1012309093509238814>","<:arm:1012309148802748456>","<:dir:1012309179245019177>","<:idir:1012309203249004614>"]

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
    [STRENGTH, ENDURANCE],
    [STRENGTH, PRECISION],
    [AGILITY, STRENGTH],
    [CHARISMA, INTELLIGENCE],
    [INTELLIGENCE, PRECISION],
    [STRENGTH, PRECISION],
    [MAGIE, PRECISION],
    [CHARISMA, PRECISION],
    [MAGIE, ENDURANCE],
    [INTELLIGENCE, ENDURANCE],
    [CHARISMA, ENDURANCE],
    [MAGIE, INTELLIGENCE],
    [INTELLIGENCE, CHARISMA],
    [STRENGTH, INTELLIGENCE],
    [ENDURANCE, INTELLIGENCE],
    [STRENGTH, MAGIE]
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
DPT_PHYS, HEALER, BOOSTER, DPT_MAGIC, SHIELDER = "Bers, Obs, P.Plu, T.Bru, Att.", "Vig., Alt", "Ido, Inv.", "Enc, Mag, Sor.", "Pro., Pré."

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

elemEmojis = ["<:neutral:921127224596385802>", "<:fire:918212781168275456>", "<:water:918212797320536124>", "<:air:918592529480446002>", "<:earth:918212824805801984>","<:light:918212861757653053>", "<:darkness:918212877419175946>", '<:space:918212897967075329>', '<:time:918212912408051814>', "<:univ:936302039456165898>"]
secElemEmojis = ["<:empty:866459463568850954>", "<:secFeu:932941340612894760>", "<:secEau:932941360858820618>", "<:secAir:932941299559063573>","<:secTerre:932941317804273734>", "<:secLum:932941251597201438>", "<:secTen:932941234501222410>", "<:secTempo:932941280785338389>", "<:secAst:932941221331075092>"]
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
    "Pénétration : + 5\nDégâts zones et distance simultanément : +10%",
    "Précision : + 10\nDégâts monocible et distance simultanément : +10%",
    "Agilité : + 10\nDégâts zones et mêlée simultanément : +10%",
    "Résistance : + 5\nDégâts monocible et mêlée simultanément : +10%",
    "Soins et armures : +10%",
    "Dégâts indirects : + 10%",
    "Puissance des boosts et malus donnés : +10%\nPuissance des boost reçu d'autrui : +5%\nPuissance des malus reçus d'autrui : -5%",
    "Puissance des effets de soins indirects : +20%"
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
AOEDAMAGEREDUCTION = 0.25
AOEMINDAMAGE = 0.2

def uniqueEmoji(emoji):
    return [[emoji, emoji], [emoji, emoji], [emoji, emoji]]

def sameSpeciesEmoji(team1, team2):
    return [[team1, team2], [team1, team2], [team1, team2]]

dangerEm = sameSpeciesEmoji('<a:dangerB:898372745023336448>', '<a:dangerR:898372723150041139>')
untargetableEmoji = uniqueEmoji('<:untargetable:899610264998125589>')

# List of guild ids for the bots
ShushyCustomIcons = [881900244487516180]
LenaCustomIcons = [881632520830087218, 881633183425253396]

stuffIconGuilds = [866782432997015613, 878720670006132787, 887756868787769434, 887846876114739261, 904164080204513331,908551466988486667, 914608569284964392, 922684334010433547, 928202839136825344, 933783830341484624, 953212496930562098, 1006418791669956698]
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

# Tabl of random messages for the shop
shopRandomMsg = [
    "<:ikaBlue:866459319049650206> : `Sit down and eat pop-corns`\n{shushi} : `Regarde les pop-corns avec un air interresée`",
    "<:soria:977183253255557140> : \"Flum POWA !\"\n{clemence} : \"Les coquelicots c'est mieux je trouve\"\n{alice} : \"N'importe quoi ! Ce sont les roses les plus jolies !\"\n{lena} : \"Vous trois, vous pourriez arrêter de débattre dans mon shop, s'il vous plait ?\"",
    '{shihu} : "Tu en pense qwa de cette coupe de cheveux ?"\n{shushi} : "Hum... Pi vraiment convaincue..."\n{shihu} : "Oh..."\n{shushi} : "Mais après, je peux toujours en faire un queue de cheval regarde !\n{shihu} : :0',
    '<:akira:909048455828238347> : ...\n{shihu} : ...\n<:akira:909048455828238347> {shihu} : ^^\n\n{lena} : <:LenaWhat:760884455727955978>',
    '{shehisa} : "Toujours rassurant de te savoir dans les parages, Icealia"\n{icelia} : "Et moi je suis toujours rasurée de te savoir dans mon camp..."',
    '<:determination:867894180851482644> : "Alors Féli, tu as fais des progrès sur ta maitrise de la Détermination ?"\n{feli} : "Ouais :D ! Regarde ça !"',
    '`Alice surgit au coins du couloir en courant et vous rentre dedans, ne vous ayant pas vu`\n\n{alice} : "Dé-désolée !"\n\n`Elle ramasse rapidement les cahiers qu\'elle portait dans ses bras et repart aussi vite qu\'elle est venue.\nVous constatez qu\'elle a oublié une feuille, qui a du se retrouver sous elle quand elle est tombée`\n\n📄 [Devoir d\'astronomie sur les trous noirs](https://bit.ly/3kh8xP3)',
    '{alice} : "Maraiiiiiiiiine ?"\n{lena} : "Il y a un peu trop de "i" pour moi..."\n{alice} : "C\'est quoi ça."\n\n`Elle sortie son téléphone et le mit directement devant le visage de Lena`\n\n📱 [Photographie d\'une feuille de papier](https://bit.ly/3o74aal)\n\n{lena} : "... Merde. Et comment ça, tu es allé fouiller dans ma chambre !?"',
    '`En entrant dans une pièce présumée vide, vous êtes surpris de voir des reflets lumineux dans un coin. En allant l\'examiner, vous découvrez Shushi et Sixtine qui dorment l\'une contre l\'autre. Au sol se trouve un lecteur de musique`\n\n📱 [Liste de musique en file d\'attente](https://bit.ly/3D6Ltdh)',
    "{shushi} : \"Hé hé Madame des neiges ! J'ai touvé ça part terre, y a maqué quoi deçu ?\"\n{icelia} : \"Montre moi pour voir ^^ ?\"\n\n📃 [Page de papier à l'encre rose](https://bit.ly/3DgXk8v)",
    "{sixtine} : \"...\"\n<:krys:916118008991215726> : ?\"\n{sixtine} : \"...\"\n<:krys:916118008991215726> : \"?.? Je peux t'aider ?\"\n{sixtine} : \"Oh heu... Je me demandais juste si tu avais un coeur de pierre...\"\n<:krys:916118008991215726> : \"??.??\"",
    "{feli} : \"Dit Maraine, tu peux jouer ça au violon ?\"\n{lena} : \"Hum laisse moi voir ? Si Do# Mi Fa# Mi Ré# Do# Si Fa#... Oh. Je vois où tu veux en venir\"",
    "{shushi} : \"Maman tu fais quoi ?\"\n{lena} : \"Hum ? Oh rien d'important\" `Glisse une feuille de papier derrière elle`\n{shushi} : \"Tu peux m'aider pour mes devoirs :< ? J'y arrive pas\"\n{lena} : \"Oh oui bien sûr ^^\"\n\n`Les deux quittèrent la pièce en laissant la dite feuille sur le bureau`\n\n:page_with_curl: [Feuille de papier](https://docs.google.com/spreadsheets/d/1l6csj2GjnaHMPYhPgqaji6Hs7bU68eb4XC_Ss2oxT-4/edit?usp=drivesdk)",
    "{alty} : \"Et voilà ^^ Et évite de courir trop vite la prochaine fois sinon tu vas retomber\"\n{shushi} : \":< Je veux un bisou magique !\"\n{alty} : \"Oh. `Fait un bisou sur le genou de Shushi` Et voilà ^^\"\n{shushi} : \"Viiii :D\"",
    "<:stella:958786101940736061> : \"Oh Nacia' ! Tu te débrouilles avec ton réchauffement atmosphérique en ce moment ?\"\n<:nacialisla:985933665534103564> : \"On peut pas vraiment dire que tu m'aide Stella...\"",
    "<:kitsune:935552850686255195> : \"Oh c'est toi. Ta vandetta est toujours dans tes projets ? Il me semble que la population d'humains à quand même sacrément diminuée ces dernières années. Enfin... pas que les humains.\"\n<:nacialisla:985933665534103564> : \"On fait pas d'omelette sans casser des oeufs. Et pour répondre à ta question, j'ai tout de même prévu de leur faire quelques piqûres de rappels de temps en temps\"\n<:kitsune:935552850686255195> : \"J'aimerais juste que tu te souvienne qu'il y a pas que ces primates qui souffres de tes crises.\"\n<:nacialisla:985933665534103564> : \"Et je te rappelle que le génocide de tes décendantes n'a rien à voir avec moi.\"\n<:kitsune:935552850686255195> : \"Oh je ne parlais pas que pour mon \"espèce\" tu sais.\"",
    "{catili} : `Déprime sous un lit en repensant à sa dimension d'origine`\n{luna} : \"Ah bah te voilà. Tu es pas en train de te cacher pour creuver seule dans un coin tout de même ?\"\n{catili} : `Se tourne vers le mur pour pas la regarder` \"Dit Luna... Pourquoi tu as arrêté de me tuer après notre troisième affrontement ? Dans ma dimension tu avais pas hésité à m'achever, mais ensuite tu as hésité jusqu'à m'épargner à partir de ma 4e défaite...\"\n{luna} : \"... `S'assoit dos contre le lit et regarde la lampe au plafond en réflichissant` Disons que la première fois, je voyais tous les servants de la Lumière comme des parasites qui ne méritaient que de se faire écraser sur mon chemin. Mais lorsque tu es revenue me faire face quelques mois plus tard alors que tu avais tout perdu, j'ai commencé à ressortir une pointe de compassion à ton égart, que j'ai préférer ignorer. Puis tu es revenue une troisème fois, avec la rage au ventre et cette détermination toujours aussi inébranlable pour me suivre aux travers de dimensions quasiment similaires à la tienne qui subissaient un sort tout aussi similaire. Disons que j'avais de plus en plus de mal à porter le coup fatal on va dire...\"\n{catili} : `Fouette doucement le bras de Luna avec sa queue` \"Je l'ai fait parceque c'était la dernière chose que je pouvais faire en tant de pretresse de la Lumière, tout tenter pour t'arrêter quitte à y laisser mes neufs vies... `Sort de sous le lit et se colle à la jambe de Luna toujours sans la regarder` J-J'ai gagné non... ? Alors... Pourquoi je suis obligée de vivre comme un vulgaire animal de compagnie Luna... ? Tu m'as déjà pris tous ceux que j'aimais et ton alter ego m'a prit le peu de dignité qu'il me restait... C-C'est en grande partie grâce à moi que tu ne l'a pas effacé ou que vous avez pas de problème avec les autres Servants de la Lumières qui veulent votre peau à cause de tes conneries ! Alors... alors pourquoi c'est moi qui douille le plus dans cette histoire... ?\n\"{luna} : \"...\"",
    ]

shopEventEndYears = [
    "{lena} : \"Alors Shu' tu as des résolutions pour l'année à venir ^^ ?\"\n{shushi} : \"Ré...so...lu... quoi ?\"",
    "{clemence} : \"Tu t'es surpassée pour ta robe de noël cette année Alice\"\n{alice} : \"Tu trouves ^^ ?\"\n{clemence} : \"Puisque je te le dis x)\"",
    "{feli} : `Fait des calins à tous le monde` \"Bonne année ^°^ !\"",
    "{shihu} : \"Mmg pourquoi il y a tout qui brille en ce moment... j'y vois rien...\"",
    "{icelia} : \"Vous avez prévu un truc pour cette fin d'année, vous ?\"\n{shehisa} : \"Oh on comptait juste aller voir nos parents, ça fais un moment qu'on n'est pas allé leur faire un coucou",
    "{sixtine} : \"Mais puisque je te dis que ce pull me va très bien...\"\n{alice} : \"Alleeeeez :<\"",
    "{alice} : `Regarde les babies roses à ruban que lui a offert Iliana` ...\n{sixtine} : \"Elle veut juste devenir ton amie... tu sais...",
]

shopEventOneDay = [
    {"date": (19, 1),
     "tabl": [
        "{shushi} : \"Joyeux naniversaire Miman !\" `Lui donne un joli dessin fait avec Sixtine`\n{lena} : \"Oh ^^ Merci Shu'\"",
        "{lena} : \"Hé Léna ! J'ai le droit à un jour de congé pour mon anniversaire ?\"\nC'est pas comme si tu étais un OC super occupée...",
        "{feli} : \"Joyeux anniversaire Maraine ^°^\"\n{lena} : \"Merci Féli ^^\"",
        "{lena} : \"Le temps passe mine de rien... Et c'est pas parceque je n'ai pas de forme physique que je ne le ressent pas\"\nSi je peux me permettre, tu as quand même grandit depuis ton premier chara-desing\n{lena} : \"Tu me fais toujours de la même taille qu'Alice par contre.\"",
        "{lena} : `Regarde Shushi courir après des ballons de baudruche` \"Parfois je me demande à quoi ressemble une vraie enfance...\"\nTu n'en a pas eu une super désagréable pourtant\n{lena} : `Soupir` \"Tu sais très bien que la seule enfance que j'ai ce sont les souvenirs que tu m'en a donné\"",
        "{lena} : \"J'aurais pensé que tu te ferais plus présente aujourd'hui tout de même. Techniquement, c'est ton anniversaie aussi\"\n{luna} : \"Je comprend pas vraiment ce délire des \"anniversaires\"\""
    ]
    },
    {"date": (14, 2),
     "tabl": [
        "{lena} : `Soupir` \"Je dirais pas non à un petit chocolat chaud aujourd'hui...\"",
        "{clemence} : \"Alors Alice, prête à être la boureau des coeurs du colège ?\"\n{alice} : \"Si tu crois que ça m'amuse...\"",
        "{lena} : `Regarde Ly dormir sous un arbre à l'aurée de la forêt` Je sais pas pourquoi je l'aurais pensé plus active aujourd'hui...",
        "<:john:908887592756449311> : \"Hum... Clémence ? J'ai... des chocolats pour toi...\"\n{clemence} : \"Hum, désolée, mais je dirgère pas trop les chocolats ^^'\"\n{alice} : `Facepalm derrière le dos de la vampire`"
    ]
    },
    {"date": (17, 4),
     "tabl": [
        "{alice} : \"Hé Clémence :D Regarde tous les oeufs que j'ai trouvés !\"\n{clemence} : \"Effectivement c'est beaucoup\"",
        "{sixtine} : \"Clémence... ? Hum... Tu veux partager un oeuf en chocolat... ?\"\n{clemence} : \"Désolée Sixtine... tu sais bien que je digère pas le chocolat...\"",
        "{lena} : \"J'ai jamais compris pourquoi les gens cachent des oeufs en chocolat pour Pâques\"\n{luna} : \"Ça ne t'empêches pas de le faire quand même\"\n{lena} : \"En même temps, même toi tu ne peux pas être insensibles à toutes leurs bouilles heureuses\"\n{luna} : \"Évite de parler en mon nom s'il te plaît... Mais oui\"",
        "{feli} : \"Aller Clémence viens chercher avec nous !\"\n{clemence} : \"Avec une main ça va être compliqué\"\n{feli} : '^' \"Tu n'as qu'à porter le panier !\""
    ]
    }
]

shopMonthlyMsg = [
    [# January
        "{lena} : \"Féli, si tu pouvais arrêter de dormir dans le feu ça m'arrangerais pas mal\"\n{feli} : \"Bah pourquoi :< ?\"\n{lena} : \"Parceque après tes soeurs et Shushi veulent faire la même chose. Et elles, elles ne sont pas fireproof.\"\n{feli} : \"Oh\"",
        "{lena} : `Descend dans le salon à 3h du matin pour prendre un verre d'eau et voit une boule de poils blancs devant la cheminée` \"C'est pour ça qu'on porte des vêtements, Lio\"\n{lio} : `Eternue dans son sommeil`\n{lena} : `Soupir, remet une buche dans la cheminée puis pose une couverture sur la grosse boule de poils`",
        "{lena} : \"`Aide Altikia à ranger les courses` Dit-moi... elles t'ont fait un truc les vampirettes ou comment ça se passe ?\"\n{alty} : \"Hum ? Oh tu parles des gouses d'ails ? Bah Alice dort chez une amie et Clémence a dit qu'elle passerait la nuit à la bibliothèque donc je me suis dit que c'était l'occasion de changer un peu le menu ^^\"\n{lena} : \"Il va falloir passer un sacré coup de déodorisant...\"",
        "{shihu} : \"Lena ne va pas du tout être contente quand elle vera que tu as pris un de ses pistolets d'airsoft...\"\n{shushi} : \"Elle n'en saura rien !\"\n{shihu} : \"Tu as même pas pris de protections..\"\n\n`Shushi visa une canette vide et tira, sans grand succès. La bille rebondit cependant sur le mur derrière et explosa contre un bouclier lumineux qui s'était formée devant la petite fille avant qu'elle n'ai eu le temps de bouger. Cette dernière regarda un peu confuse autour d'elle puis elle remarqua la chatte blanche assise à côté d'elle qui la regardait fixement`\n\n{shushi} : \"... s'il te plait le dis pas à Miman...\"\n{catili} : \"Si tu ranges ça, peut-être\"\n{shihu} : \"(Pff, elle fait juste ça pour pas que Lena la tienne responsable également)\"",
    ],
    [# Febuary
        "{clemence} : `Regarde Félicité de haut en bas` \"Toi tu as encore dormi dans la cheminée\"\n{feli} : \"D: Non c'est faux !\"\n{clemence} : \"Tu es pleine de cendres, s'il te plaît x)\"",
        "{gweny} : \"Ta mère ne va pas être contente si elle te choppe en train de fouiller dans son atelier\"\n{shushi} : \"Gwen, tu sais pourquoi Miman a autant de balles incendiaires ? Son élément c'est plutôt la glace, non ?\"\n{gweny} : \"Détourne pas le sujet. Mais pour répondre à ta question, je pense que ça remonte à l'époque où j'était encore flic à la ville. L'une des membres de la mafia locale était d'élément Métal Pur et il me semble que ta mère et elle se connaissaient personnellement. Et c'était pas l'amour fou entre les deux. Il me semble même que c'est la seule personne que Lena craind encore aujourd'hui, même si ça fait des années qu'elle n'a pas donné signe de vie. Et tu connais ta mère, quand quelque chose la contrari elle préfère contre attaquer, d'où le fait qu'elle ai passé pas mal de temps à mettre au point ces balles\"\n\n`Gwendoline se pencha pour prendre l'une des balles et l'observa attentivement pendant quelques secondes`\n\n{gweny} : \"Si je n'abuse, celle-là est prévu pour pénétrer un blindage ultra-épais et exploser à l'intérieur en libérant des sharpels explosifs. De quoi te descendre un élicoptère blindé d'une balle au vu de la puissance du fusil de Lena, si tu veux mon avis\"\n{shushi} : \"Wow...\"\n{shihu} : \"Je comprend mieux pourquoi elle veut pas nous voir jouer ici...\"",
        "{lena} : \"FM comes in different colors, I believe... In the sewing machine, I've lost myself... Memories inside my heart are there to grieve... Color-coded by the love she gave to me...\"\n{luna} : \"Nostalgique ?\"\n{lena} : \"En quelques sortes, je suppose...\"",
        "{sixtine} : `Regarde le crusifix et le livre religieux à côté du lit d'Alice` \"Comment tu arrives à dormir à côté de ça... Clémence ne supporte même pas d'être à proximité d'une croix...\"\n{alice} : `Fait une petite moue`\" C'est elle qui s'est définie en temps qu'ennemi du divin souss prétexte que c'est sa nature. Mais ce genre de discipline tiens sa puissance en la Foi. Tant que tu l'as, qu'importe que ce tu es",
        "{alice} : `Carresse très lentement Iliana en étant relativement tendue`\n{catili} : `Se contente de ronronner sans bouger pour éviter de l'effrayer. Et puis elle aime bien les caresses`\n{alice} : `Se met à lui caresser le ventre en voyant qu'elle s'est mise sur le dos`\n{catili} : `Essaye le plus possible d'ignorer son instinct de félin qui lui hurle d'essayer de mordiller cette main qui se balade sur son ventre, parcequ'elle n'a pas envie que cette même main la projette contre un mur dans un mouvement brusque avec toute la force d'une jeune vampire paniquée. Quelque chose lui dit que plusieurs de ses os ne l'appréciraient pas trop`",

    ],
    [# March
        "{alice} : `Est assise sur une commode devant une fênetre et regarde la pluie arroser ses fleurs`",
        "{alice} : `Plante des fleurs dans le jardins tandis que Sixtine regarde les nuages`",
        "{lena} : \"Surtout tu oublie pas ton parapluie !\"\n{shushi} : \"Mais il fait grand soleil !\"\n{lena} : \"Il peut très rapidement se mettre à pleuvoir à cette saison, Shu'\"",
        "{lena} : \"Oh est surtout, évitez de traîner trop avec Lia s'il vous plaît. Le printemps est sa saison de prédilection\"",
        "{lena} : \"La vache c'est bien plus compliqué que je le pensais de lancer ces plumes enfaites...\"\n<:hina:908820821185810454> : \"C'est qu'une question d'habitude ^^ Hônnetement... J'arriverai même pas à tenir un de tes fusils donc bon ^^'\"",

    ],
    [# April
        "{clemence} : `Attend le trio de soeur en lisant assise (à l'ombre) à la terrasse d'un café tout en discutant avec Gwen, quand elle vit Sixitine venir seule` \"Comment ça tu es toute seule Sixtine ? Où sont Féli et Alice ?\"\n{sixtine} : \"Féli a dit qu'elle voulait aller voir la dernière expédition sur les dieux de la Grèce Antique et Alice a... dit un truc à propos de l'Eglise je crois...\"\n{clemence} : \"... Gweny, tu veux bien t'occuper d'aller chercher Alice et je me charge de Féli ?\"\n{gweny} : \"Je suis pas vraiment la bienvenue dans les églises catholiques aussi tu sais ?\"\n{clemence} : \"Déjà moins que moi...\"\n{sixtine} : \"Je peux y aller moi si vous voulez... Je suis qu'humaine...\"",    
        "{luna} : \"Dans notre ancien chez nous les fleurs mourraient si elles avaient trop de Lumière\"\n{catili} : \"Vraiment toutes ? Même ici il y a des fleurs qui vivent dans l'ombre\"\n{luna} : \"À quelques exeptions près, effectivement\"",
        "{sixtine} : `Regarde les étoiles dans une prairie, puis remarque qu'elle n'est pas seule` \"... toi aussi tu brillais autant à l'époque où tu étais une étoile aussi... ?\"\n<:powehi:909048473666596905> : \"Et comment ! J'étais la plus grande, la plus chaude et la plus brillante de ma région...\"\n{sixtine} : \"Tu avais un système planétaire aussi ?\"\n<:powehi:909048473666596905> : \"Trois. Elles étaient plutôt sympatiques, et l'une d'entre elle abritait même la vie mais... `Soupir` Elles...\"\n{sixtine} : \"... Au moins je suis sûre qu'elles ont bien aimée ta supernova...\"\n<:powehi:909048473666596905> : \"Je... je pense... Leurs représentations se tenaient les mains sans vraiment avoir l'air effrayées...\""
        '{alice} : "Mooow tu sais que tu es trop mignone toi ?"\n{shushi} : "Heu... gwa ?"',
        "<:rdmEvilGuy:866459027562954762> : \"Rien ni personne ne pourra m'arrêter ! Mon plan est parfait et j'ai anticipé toutes les possibilités ! Lorsque j'aurais assujeti le monde, personne ne remettra mes idées en question et je serais enfin reconnu pour mon génie ! Puis je le détruirais après avoir terminé mon vaiseau galactique et j'ira asurjetir la galaxie ! Et lorsque ça sera fait, je la détruirais également parceque je le peux et que j'en ai les moyens ! Mon armée de robot est invincible et vous allez toutes mourirs dans d'affreuses souf-ARG !\"\n<:helene:906303162854543390> : \"Shehisa !\"\n<:shehisa:919863933320454165> : \"Oh vous comptiez écouter son discourt pendant encore longtemps ? Vous savez pas comment c'est stressant de rester invisible derrière les gens en attendant le moment parfait pour les planter une dague dans la nuque...\"\n<:icealia:909065559516250112> : \"Oh non tu as bien fais je commençais à en avoir marre aussi\"",
        "<:john:908887592756449311> : \"A-Alice, toi qui la connais bien tu... saurais ce que je pourrais faire pour... qu'elle me voit comme autre chose qu'un... ami ?\"\n{alice} : \"Commence par être un peu plus sûr de toi. Là, elle continue de voir le louvetau naïf qui essayait de se coucher à ses pieds au lieu de fuir\"\n<:john:908887592756449311> : \"Mais je-\"\n{alice} : \"Passe ton temps avec elle sous ta forme de loup à être couché à ses pieds. Si tu veux qu'elle te vois comme autre chose qu'un chien de compagnie, va falloir que tu arrête de te comporter tel quel.\"",

    ],
    [# May
        "<:anna:943444730430246933> : \"Hé Alice, tu en penses quoi de cet ensemble... ?\"\n{alice} : \"Un peu viellot, mais ça te va bien\"",
        "<:determination:867894180851482644> :\"`S'étire` C'est un chouette printemps que nous avons là\"\n{alice} : \"Dis Chara... tu avais promis de m'aider avec mes fleurs :<\"\n<:determination:867894180851482644> : \"Oh mais je l'ai fais, pourquoi crois-tu qu'il y a une golden flower au milieu ?\"\n{alice} : \"Oh heu... c'est pas vraiment ce que je voulais dire par là mais... merci quand même\"\n<:determination:867894180851482644> : \"`Facepalm` Ah tu demandais des conseils en jardinage normal, c'est ça ?\"\n{alice} : `Hoche la tête`",
        "{luna} : `Regarde Shushi et Shihu faire de la calligraphie, en controlant chacune leur main dominante respective`\n{lena} : \"Tu sais, si tu veux passer du temps avec elle il suffit de le dire hein\"\n{luna} : `Soupir` À quoi bon. Elle me considère sûrment même plus comme sa mère, et je suis nulle pour essayer de l'être\"\n{lena} : \"Tu te trompes. Quoi qu'il arrive, tu seras toujours sa mère. Elle s'est juste faite à l'idée qu'elle ne pourra pas avoir une relation \"normale\" de file-mère avec toi, et elle essaye de l'avoir avec moi à la place\"\n{luna} : \"Ça me motive encore moins à essayer, ça Lena\"\n{lena} : \"Ce que je veux dire, c'est que ce n'est pas en restant cacher au fond de notre âme que ça va changer les choses, Luna\"",
        "{lia} : \"Pourquoi c'est moi qui doit garder mes petits frères et soeurs !?\"\n<:kitsune:935552850686255195> : \"Parceque Lio est occupée. Tu verras ils sont pas méchants, par contre cette portée là-\"\n{lia} : \"Laisse moi deviner, adores jouer dans les queues de leur mère ?\"\n<:kitsune:935552850686255195> : \"Pourquoi tu dis ça sur ce ton là ? Toi aussi tu aimais bien le faire à leur âge ?\"\n{lia} : \"Sauf que tu as trois fois plus de queues que moi Maman >< ! On pouvait chacun avoir la notre pour s'amuser, là ils sont presque à deux à me tirer sur chaqu'une d'entre elles !\"\n<:kitsune:935552850686255195> : `Ricane` \"Commence par t'assoir comme ça tu risques pas de leur tomber dessus si ils tirent trop fort. Et c'est pas tout mais je vais devoir y aller moi, bon courage. Oh et hésite pas à leurs montrer quelques tours. Même si ce sont de renardaux ordinaires, ils restent plutôt sensible à la magie. Ta soeur qui est actuellement en train de se frotter à tes jambes semble avoir une affinité avec le vent d'ailleurs, vous devriez bien vous entendre. `Avec un ton plus bas, sans vraiment s'adresser à Lia` J'aimerais bien que vous passiez plus de temps avec vos frères et soeurs \"ordinaires\" vous savez...\"",
        "{sixtine} : `Arrête de dessiner` Hum... Enfaite Anna... heu... comme tu est une fantôme tu peux posséder des gens ?\"\n<:anna:943444730430246933> : \"À vrai dire, pas vraiment... par contre Belle...\"\n`Les deux se tournèrent vers le miroir le plus proche où le reflet de Sixtine n'était absolument pas là où il devrait être, mais en train de fouiller dans le reflet de la boîte à bijoux d'Alice`\n{sixtine} : \"... C'est bien ce qu'il me semblait...\"",
        "{gweny} : \"Hey Clémence ! Tu veux faire une partie de paintball avec moi ce soir ?\"\n{clemence} : \"Pourquoi pas, mais il y aura Lena ?\"\n{gweny} : \"Hum...\"\n{clemence} : \"...\"\n{gweny} : \"...\"\n{clemence} : \"Je vais mettre plusieurs couches de tee-shirts\"\n{gweny} : \"Bonne idée, je vais faire de même\"",
        '<:ruby:958786374759251988> : "Clémence, ça va mieux avec ta cicatrice en ce moment ?"\n{clemence} : "À part qu\'elle me brûle quand j\'utilise trop mes pouvoirs vampiriques ou quand il y a un Alpha dans le coin, rien à déclarer"\n<:ruby:958786374759251988> : "Tss. Ces loups garoux..."\n{clemence} : "Pas la peine de prendre ce regard assassin Madame Ruby. J\'ai appris à faire avec maintenant"',

    ],
    [# June
        "{alice} : \"J'ai hate que l'été arrive ! Tu viendras avec nous à la plage Clémence :D ?\"\n{clemence} : \"Hum, tu veux dire sous un soleil de plomb en maillot de bain avec la mer qui fait ses remous juste à côté alors que je déteste l'eau et arrive à me chopper des coups de soleil en hiver et sans reflets sur la neige ?\"\n{alice} : \"... Désolée c'était stupide...\"",
        "<a:Ailill:882040705814503434> : \"Est-ce que tu t'es déjà demandée quel goût avait le sang ?\"\n{lena} : \"Non merci, et si vraiment j'ai envie de savoir, je préfère demander aux vampirettes plutôt qu'à toi.\"\n<a:Ailill:882040705814503434> : \"Tu es pas drôle tu sais\"",
        "{alty} : \"Tu devrais aller dormir, Lena\"\n{lena} : \"C'est pas parceque tu fait deux têtes de plus que moi que tu es sensé agir comme ma mère Altikia\"\n{alty} : \"Lena... Tu as dormis que 3h en deux jours... Et regarde moi ce nombre de canettes de Coca... Je sais pas ce que tu fais, mais je suis sûre que ça peut attendre une bonne nuit de sommeil\"\n{lena} : \"Ça va, t'en fais pas\"\n{alty} : \"Ça fait deux fois que tu dévise et revise la même vis dans le même trou depuis qu'on parle\"\n{lena} : \"Peut-être qui si tu arrêtais de me parler je serais plus concentrée, effectivement.\"\n{alty} : \"`Soupir` Tu es en train de te défoncer la santé et je doute fortement que le jeu en vale la chandelle. Maintenant tu va aller te coucher ou sinon tu va voir que mes deux têtes supplémentaire vont faire une bonne différence quand je vais te forcer à y aller.\"\n{lena} : \"`Se lève d'un coup pour aller confrontrer Altikia, ce qui fût une erreur puisque qu'elle fût immédiatement prise de vertige et ses jambes se dérobèrent sous elle. Puis elle soupira` Tu as peut-être pas tord au fond...\"\n{alty} : \"Tu vois ?\"",
        "{gweny} : `S'écroule dans son lit` \"J'en peut plus de ces canicules je dois changer de tee-shirts trois fois par jours...\"\n{karai} : `Ricane depuis l'étagère` \"Tu as toujours eu ce genre de problème Gweny\"\n{gweny} : \"Ça m'aide pas vraiment ça Karaï...\"",
        "{alice} : \"Tu devrais essayer de te dégager un peu la mèche de temps en temps tu sais ? Je pense que ça t'irais pas trop mal\"\n<:akira:909048455828238347> : \"Est-ce que je t'ai demandé ton avis ?\"",
        "<:benedict:958786319776112690> : \"Alice, même si je le conçois tu chantes très bien, est-ce que tu pourrais essayer de ne pas couvrir les autres à la chorale ? C'est un coeur, pas un solo\"\n{alice} : \"D-Désolée je m'en rend pas compte...\"",

    ],
    [# July
        "{alice} : \"Clémeeeence ? Tu peux venir nous surveiller pendant qu'on se baigne dans le lac s'il te plaît :< ? On voudrait apprendre à Shushi à nager\"\n{clemence} : \"Hum... Tu me demande ça à moi alors qu'il n'y a pas un nuage dans le ciel ?\"\n{alice} : \"Tu te doute bien que si je le fais c'est qu'il n'y a pas d'autres options... Gwen et Lena sont en ville aujourd'hui\"\n{clemence} : \"`Soupir` Je vais chercher des lunettes de soleils et le plus grand parasol de que je peux trouver alors... Mais si il arrive quoi que ce soit dans l'eau, c'est Féli qui s'en charge.\"\n{feli} : \"Capiche !\"\n{alice} : \"Viiii ^°^ Merci Clémence\"",
        "{lena} : \"Arrêtez de vous plaindre ça fait à peine une heure qu'on est en randonné. Et est-ce que Clémence s'est plainte elle ? `Se retourne vers le groupe` Huh\"\n{sixtine} : \"`Soulève sa casquette humide pour révéler la chauve-souris en train de faire l'étoile de mer dans ses cheveux` Elle a fait une insolation dès les dix premières minutes...\"\n{lena} : `Soupir`\n<:edelweiss:918451422939451412> : \"Si vous voulez il y a un lac ombragé pas trop loin pas trop loin\"\n{lena} : \"Oh bonjour Edelweiss. Et je pense que c'est un bon endroit pour faire une pause effectivement...\"",
        "{lio} : `Regarde Alice et Sixtine essayer d'apprendre à nager à Shushi depuis le fond de son lac`\n{feli} : \"Coucou !\"\n{lio} : `Sursaute (peut-être vraiment parler de sursaut quand on flotte dans l'eau ?)` \"Oh c'est toi... J'oublie toujours que tu peux respirer sous l'eau aussi...\"\n{feli} : \"Ça t'arrive jamais de sortir de ton lac de temps en temps ? Enfin à part pour ralonger nos combats\"\n{lio} : \"Mais j'aime bien mon lac moi... et puis il y a trop de problèmes là haut... Et pour ton deuxième point, les combats sont plus interressant contre vous qu'avec. C'est toujours trop rapide avec vous...\"\n{feli} : \"Oula, à ne pas sortir du contexte celle-là\"\n{lio} : \"Oh hum... désolée...\"",
        "`C'est l'heure du beach épisode ! Dans l'eau en face de vous vous pouvez observer le trio de soeurs et Shihu en train de jouer avec un ballon de plage dans la mer\nUn peu plus sur le côté vous pouvez voir Lia et Liz qui louchent pas mal sur un groupe de surfeur en étant à moitié jalouses du fait que Liu est parmis eux alors qu'elle ne semble pas vraiment être affectuée par la chad attitude qu'ils libèrent\nCeux qui font de la plongée sous-marine peuvent voir Lio en bikini (pour une fois) en train de récupérer les objets perdus par les nageurs et constater que quelques familles auront du mal à prendre leurs voitures sans leurs clés, et vous dites que voir une kitsune sortir de l'eau pour les leur rendre fait très fée sortant du lac et qui propose une version d'or ou d'argent d'un objet perdu\nAssise sur un rocher, vous pouvez retrouver Lena en train de lire les pieds dans l'eau tout en surveillant Gwen qui nage dangereusement près en lui lançant des regards malicieux de temps en temps pour vérifier si la jeune femme aux cheveux bleus fait attention à elle ou non\nEt enfin, collées l'une à l'autre, vous pouvez retrouver Clémence et Iliana qui, bien que toutes les deux en maillot de bain, ne veulent quitter l'ombre du parasol pour rien au monde`",
        "<:benedict:958786319776112690> : `Viens à la rencontre de Clémence qui attendait à la sortie de l'église` \"Tu es la soeur d'Alice, c'est cela ?\"\n{clemence} : \"C'est si compliqué à deviner ?\"\n<:benedict:958786319776112690> : `Croise les bras en faisant la moue` \"Il n'y a pas beaucoup de vampires qui attendrait pendant une dizaine de minutes devant un église d'autant plus qu'il ne fait pas encore nuit. D'autant plus qu'Alice nous avait dit que tu viendrais la chercher après le Chemin de Croix.\"\n{clemence} : \"Et je suppose que si ce n'est pas elle qui vient directement c'est parcequ'il s'est passé quelque chose ?\"\n<:benedict:958786319776112690> : \"Elle a perdu connaissance en milieu d'après-midi et ne s'est toujours pas réveillé depuis. Je pense que le soleil de plomb et la symbolique du chemin n'a pas fait du bien à ses... origines, aussi... résistante soit-elle. Peut-être que toi qui t'y connais un peu mieux sur ce sujet pourrait la réveiller. Si c'est le cas, je t'autorise à rentrer dans l'église pour aller la voir.\"\n{clemence} : `Soupir` \"Si un jour on m'aurait dit qu'on m'inviterais à rentrer dans une église...\"",
        "{lena} : \"Au fait Krys, je dois te rajouter au club des hydrophobes ? T'en fais pas on mord pas. Enfin peut-être Iliana mais premièrement elle le fait que si elle est vraiment énervée et de deux je pense qu'elle s'y casserais les dents avec toi.\"\n<:krys:916118008991215726> : \"Le club des quoi ?\"",
        "{klikli} : \"Hé Lena je peux t'emprunter ta moto ?\"\n{lena} : \"Tant que tu la met à charger en rentrant oui. Tu va faire quoi ?\"\n{klikli} : \"Je dois aller chercher un truc à l'autre bout de la ville pour Lighting\"",
        "<:edelweiss:918451422939451412> : \"... Je peux t'aider ? On le dirait pas comme ça mais je me débrouille plutôt bien en soins\"\n<:lohica:919863918166417448> : \"Tu me rappelle juste quelqu'un, c'est tout... Et ton truc c'est pas plutôt la protection ?\"\n<:edelweiss:918451422939451412> : `Hausse les épaules` \"Je le fais parcequ'il y a déjà pas mal de personnes qui soignent ici, c'est tout\"",
        "{lena} : \"Merci du coup de main Lio. Bon maintenant Shihu. Qu'est-ce que j'ai dit à propos de l'utilisation de la magie à la maison ?\"\n{shihu} : \"De... Pas utiliser la magie à la maison...\"\n{lena} : \"Et donc pourquoi on a du s'y mettre à trois pour éteindre les flammes noires dans votre chambre ?\"\n{shihu} : \"Mais il y avait un moustique...\"\n{lena} : \"Et tu penses sérieusement que risquer de réduire la maison en cendre pour un moustique est une bonne idée ?\"\n{shihu} : \"... au moins je l'ai eu...\"\n{lena} : \"... Vous êtes toutes les deux privées de dessins animés et de dessert pour une semaine.\"\n{shushi} : \"Mais j'ai rien fait moi !\"\n{lena} : \"Justement.\"",
        "{lena} : \"Au faite Gwen tu met quoi lorsque tu prend ma moto ?\"\n{gweny} : \"Alors hum... moi je met juste un casque et des gants, Alty rajoute une veste et pentalon renforcé et Klironovia ne prend rien du tout, je crois.\"\n{lena} : \"... Il y en a qu'une seule qi a compris à quel point on peut être vulnérable sur un deux roues ?\"\n{gweny} : \"Roh ça va il y a quand même beaucoup moins de gens sur les routes maintenants. Et puis tout le monde ne peut pas changer de tenue en un claquement de doigts, Lena.\"",
        "{feli} : \"Pourquoi on fait jamais de combats sous l'eau enfaite ?\"\n{sixtine} : \"Parceque ça reviendrai à un duel entre toi et Lio...\"\n{feli} : \"Oh\"",
        "{iliana} : `Essaye de voir quelle robe lui irait le mieux`\n{alice} : \"... Hônnetement je pense qu'une chemise nouée et un short t'irai mieux Iliana...\"\n{iliana} : \"Tu trouves ? Et pour la couleur ? Je dois avouer que j'en ai marre d'être toujours en blanc...\"\n{alice} : \"Hum... une chemise vichy rouge peut-être...\""
    ],
    [# August
        "{clemence} : \"Hum... Où est Alice ?\"\n{feli} : \"Elle était avec nous non ?\"\n<:anna:943444730430246933> : \"Je croyais qu'elle t'avais rejoint après le Palais des Glaces Clémence !\"\n{clemence} : \"... Attendez... Vous avez emmené Alice, qui n'a aucun sens de l'orientation ni reflet dans un Palais des Glaces au beau milieu d'une fête foraine tellement bruyante que j'ai du mal à ne pas me cogner contre un mur si je me fit qu'à mes oreilles alors que je suis bien plus expérimenté qu'elle en echolocalisation et ne l'avez même pas attendue ou aidé !?\"\n{feli} : \"Elle mettait tellement longtemps on a pensé qu'elle était déjà sortie '^' !\"\n{clemence} : `Facepalm`\n<:anna:943444730430246933> : `Regarde ses pieds pas très fière d'elle et jette un coup d'oeuil à la vitrine la plus proche`\n<:belle:943444751288528957> : `Roule des yeux et sort du cadre de la vitrine`",
        "<:kitsune:935552850686255195> : \"Hmm... C'est moi Lio où je constate une forte abondance de magie curative récente au niveau de tes joues ? Me dit pas que tu continues de mordre bêtement aux hammeçons ?\"\n{lio} : \"`Est soudainement prise d'une envie de caresser ses queues` Ils sont bons les poissons qu'ils utilisent comme appât quand même... On les trouvent pas dans le coin...",
        "{alice} : \"C'est qu'il te va plutôt bien ce maillot, ça change de tes tenues en cuir !\"\n<:lohica:919863918166417448> : \"Merci je suppose. Pas besoin de te dire que ton maillot te va très bien, tu le sais déjà je pense.\"",
        "`Gwen était assise sur son lit en étant en train de surfer en ligne avec son ordinateur portable quand un mouvement dans le coin de la chambre attira son attention`\n{karai} : \"... Bonsoir Klironovia...\"\n{klikli} : \"Tiens, Karaï, ma poupée préférée `Elle prit la poupée et la plaça sur ses jambes tout en continuant sa navigation` Qu'est-ce qui t'amène donc ?\"\n{karai} : \"Oh hum... je voulais savoir si je pouvait dormir avec vous ce soir... Si ça vous dérange pas...\"\n{klikli} : \"Moi ça me va, et je pense pas que ça dérange les autres non plus. Mais je décline toute responsabilité au cas ou tu te retrouve sous moi durant la nuit\"\n{karai} : \"C'est un risque que je suis prête à prendre...\"",
        "{alice} : \"Sixtine, tu penses que c'est quel maillot qui m'irai le mieux ?\"\n{sixtine} : \"J-Je sais pas Alice... le rose ?\"\n{alice} : `Regarde les deux maillots qui était tout les deux roses`",
        "{shihu} : \"Lena, je comprend pas l'interêt de ce truc...\"\n{lena} : \"Montre ? Oh c'est tout simplement pour apprendre aux enfants les formes. D'ailleurs c'était le votre non ?\"\n{shihu} : \"Mais... tout rentre par le trou carré...\"",
        "{alice} : \"C'est un gros monstre qui est là... Hum...\"\n{feli} : \"Vous en faites pas, j'ai déjà trouvé la technique imparable !\"\n{alice} : \"Déjà ?\"\n{sixtine} : \"...\"\n{feli} : \"Ouaip ! regardez comme il a du mal à avncer ! Je pense donc que je vais utiliser mes jambes !\"\n{alice} : \⭐o\⭐\n{feli} : \"Vous êtes prêtes ? ça va être le moment de montrer ma technique secrète !\"\n{sixtine} : \"...\"\n{feli} : `Fait demi-tour et par en courant` \"Nigerundayo !!\"\n{sixtine} : \"Prévisible...\"\n{alice} : '-'",
        "{lio} : `Est assise sur un rocher en fixant la mer tandis qu'Hélène, Shehisa et Icelia pèchent à côté` \"Icealia, vous devriez essayer de lancer votre bouchon un peu plus sur la droite. Là où il est il risque d'attirer aucun poisson, entre ces rochers.\"\n{icelia} : \"Vous arrivez à voir le fond de l'eau de là ?\"\n{lio} : \"Hum ? Oh hum... je vois aussi bien dans l'eau que dans l'air donc mui, je vois le fond.\"",
        "{clemence} : \"Iliana, j'ai prévu d'aller chercher une gemme magique dans une grotte ce soir mais je suis presque sûre qu'elle regorge de monstres puissant et je serais plus rassurée si tu pouvais attirer leur attention pour qu'ils me foutent la paix pendant que je caste mes sorts\"\n{iliana} : \"Moi ? Mais... Tu aimes pas vraiment la lumière non... ? Gwen serait plus adaptée...\"\n{clemence} : \"C'est à toi que je demande, pas à Gwen. Et ne va pas me dire que tu as pas envie de te défouler un peu tu tournes en rond comme un lion en cage en ce moment\"\n{iliana} : \"Oh hum... Je veux bien venir mui ^^\"",
        "{liz} : \"Pas trop mal. Mais laisse moi te montrer ce qu'est qu'un vrai brasier\"\n{shihu} : \"... Est-ce que... Son niveau de puissance dépassait les 9 000 ?\"\n{liz} : \"Yep\"",
        "{lena} : \"Hum... Ptdr t ki toi ?\"\n<:vampHunter1:1003027064112287764> : \"Tu m'a tiré une balle dans le ventre qui m'a défoncé la colonne vertébrale !\"\n{lena} : \"Est-ce que tu te rend compte d'à quel point ça diminue peu la liste ?\"\n<:vampHunter1:1003027064112287764> : \"Je suis devenu paralisé à vie ! Tu m'as tout pris !\"\n{lena} : \"Mais je ne sais même pas qui tu es\"",
        "{liz} : \"Tu devrais venir te balader sur les plages plus souvent, il y a plein de beaux garçons avec des tablettes de chocolat, peut-être que tu auras un coup de foudre ^^\"\n{lio} : \"Je suis pas interressée tu le sais très bien...\"",
        "{lio} : \"Tu pourrais plutôt facilement apprendre la magie des sirènes toi tu sais ?\"\n{alice} : \"Tu penses vraiments ?\"\n{lio} : \"Si je te le dis ^^\"",
        "{gweny} : \"Une mini-moto ?\"\n{shushi} : \"Ouaip :D Comme Maman !\"\n{gweny} : \"Tu as l'air d'y tenir à ta mère x)\"\n{shushi} : \"Vi ^°^ C'est la meilleure !\"\n{gweny} : \"Ça dépend des domaines mais mui elle s'en sort bien\"\n{liz} : \"Pour te foutre des balles dans le coeur mui elle s'en sort bien...\"",
        "{feli} : \"Shushi qu'est-ce que tu fais avec la carabine de ta mère '-' ? Elle est plus grande que toi quasiment\"\n{shushi} : \"Bah tu as dis qu'on allait manquer de puissance de feu\"\n{feli} : \"`Facepalm` Je parlais de magie de feu, pas d'arme à feu.\"\n{shushi} : '°'\n{feli} : \"Va ranger ça avant que Lena s'en rende compte.\"",
        "{catili} : \"Qu'est-ce que tu fais avec ce pointeur laser toi '^' ? N'y pense même pas !\"\n{klikli} : :3 `Agite le point lumineux entre les pieds de la neko`\n{catili} : \"'^'... ... `Abandonne et se jete sur le point pour essayer de l'attraper. Puis fini par en avoir marre et l'attrape réellement`\"\n{klikli} : \"Hé comment t'as fais ça ?\"\n{catili} : \"Je suis littéralement une divinité mineure de la Lumière '^'\"",
        "{alice} : `Prend une photo d'Iliana pendant qu'elle somnole`\n{catili} : \"`Baille en ouvrant un oeuil une fois qu'elle a fini` Tu me dirais si j'ai eu beaucoup de Like...\"\n{alice} : \"Bien sûr x)\"",
        "{feli} : \"`Regarde Alice prendre des selfies en maillot de bain devant la mer` Tu sais que tu devrais faire attention avec les photos que tu postes sur les réseaux...\"",
        "{liz} : \"Hé Liu je me disais que tu pourrais quand même charmer pas mal de mec si tu le voulais. Tu ignores totalement le nombre d'entre eux qui sont interressés par une fille sportive comme toi\"\n{liu} : \"Je l'ignore autant que tu sais que je suis pas interressée\"\n{liz} : \"Je sais je sais malheureusement. Un conseil, évite Lia aujourd'hui, même moi j'ai commencé à être affectée par son aura\"\n{liu} : \"Noté\"",
        "{lia} : `Somnole en faisant la planche dans le lac`",
        "{lena} : \"Clémence, Iliana, pourquoi vous êtes en maillot de bain tout en restant collées au parasole ? Je veux dire, que vous vouliez pas aller dans l'eau c'est une chose - Et je vais pas vous blammer je fais de même - mais vous prenez même pas de bain de soleil là. Autant l'une c'est compréhensible autant j'aurais pensé que la lumire c'était ton truc, Iliana\"\n{iliana} : \"Ça l'est ! Mais partir de sous le parasol signifirait se rapprocher de l'eau '^' !\"\n{lena} : \"`Soupir` C'est pas deux trois goûtes qui vont te tuer\"\n{clemence} : \"Toi aussi Lena, alors pourquoi toi tu va pas dans l'eau ? Certes tu sais pas nager mais la mer n'est pas très profonde sur des dizaines de mètres quand même. Regarde ta fille elle s'amuse bien elle\"\n{lena} : \"`Fait la moue` J'essaye juste de savoir pourquoi vous êtes venus si c'est pour absolument rien faire\"\n{clemence} : \"Pour ma part j'ai pas eu le choix, c'est Alice qui m'a embarqué dans sa poche pendant que je dormais\"",
        "{lio} : `Surveille des petits frères et soeurs qui jouent dans le lac`\"\n{liz} : \"Eh bah il y a du monde ici ma parole !\"\n{lio} : \"Comme si tu étais surpise de me voir ici...\"\n{liz} : \"C'est pas faux `Se déshabille et va les rejoindre dans l'eau peu profonde`\"\n{lio} : \"... C'est rare de te voir faire trempette... Je veux dire... tu crainds pas la chaleur de l'été, l'eau est ton élément némésis et manifestement tu es même pas là pour me montrer ton maillot de bain puisque tu en as pas...\"\n{liz} : \"J'ai pas le droit de vouloir passer un peu de temps avec ma petite soeur ? C'est pas parcequ'on a des éléments opposés qu'on doit se voir le moins possible non, regarde nos ainées. Tu ne m'aimes pas :< ?\"\n{lio} : \"J'ai pas dit ça... mais je ne t'aimes pas autant que s'aiment nos fameuses ainées en tout cas\"\n{liz} : \"Et bien heureusement...\"\n{lio} : \"J'aurais pas pensé que ça te repousse tant que ça vu à quel point tu es... à fond là dessus\"\n{liz} : \"C'est pas pareil avec des femmes, j'y prend pas de plaisir\"",
        "{liz} : \"Hé Lio, tu as déjà pris des bains dans des sources chaudes ?\"\n{lio} : \"Hum... pas vraiment pourquoi... ?\"\n{liz} : \"Il faudrait que je t'emmène un jour, tu verras c'est super relaxant\"",
        "{gweny} : \"Au fait Iliana, pourquoi tu as des talons aiguilles sur tes sorolets ? ça doit pas vraiment être pratique quand tu cours à la vitesse de la lumière\"\n{iliana} : \"Hum c'est pour ne pas vraiment avoir de problème lorsque j'interverti avec ma forme féline en combat. Les chats marchent constaments sur la pointe des pieds, tu sais\"\n{gweny} : \"Compréhensible effectivement. J'avoue que je suis plutôt team chien donc j'ai pas fait le rapprochement tout de suite\"",
        "{shihu} : \"Hé Shushi, tu vas dormir ?\"\n{shushi} : \"Oui, stfu.\"\n{shihu} : \"Mourir de veillesse est juste mourir de Pas mourir\"\n{shushi} : \"O.O\"",
        "`Gwendoline se trouvait assise au bord d'une rivière les pieds dans l'eau à regarder les tumultes causées par le courant`\n<:kitsune:935552850686255195> : \"Tiens donc, ne seraisse pas cette triple déeesse junior ?\"\n{gweny} : \"Vous savez bien que je déteste que l'on m'appelle comme ça...\"\n<:kitsune:935552850686255195> : \"Et je n'ai aucune intention d'arrêter\"\n`La renarde vint se coucher à côté d'elle en regardant l'eau également`\n<:kitsune:935552850686255195> : \"Je te sens plus faible mentalement qu'à l'accoutumée, quelque chose te tracasserait-il ?\"\n`La jeune fille lui jeta un regard en coin en se demandant si elle pouvait vraiment lui parler de ses problèmes. Puis elle se coucha dans l'herbe en regardant les nuages`\n{gweny} : \"Je me demande juste à quoi je sers, à côté des deux autres. Klironovia est une superbe combattante qui n'a besoin de personne pour briller. Altikia est excellente en combat en équipe ainsi qu'en stratégie. Et moi je sert à quoi là dedans ? Je suis sensé être un mélange des deux ? Personne ne veut d'un Juste au milieu\"\n<:kitsune:935552850686255195> : \"Je pense effectivement que tu es un Juste au Milieu. Mais ne sous-estime pas l'importance de ce role. Tes deux autres personnalités ne sont pas faites pour s'entendre. Elles sont les némésis de l'autre. Cependant tu n'es pas en guerre perpétuelle contre toi-même, et je vais te dire pourquoi. Altikia préfère faire profile bas car elle estime que c'est ce qui est mieux pour toi. Klironovia se contente de laisser les choses se dérouler car elle sait que tu sais les gêrer. J'ai souvenance de ces deux là lors de leur dernière incarnation. Je peux te dire qu'elles paissaient plus de temps à s'entre-tuer mentalement qu'autre chose. Tu n'as peut-être pas la force d'une déesse, mais tu es celle qui rend tes alter-ego plus humaines\"",
        "{alice} : \"Lenaaaaa, est-ce que je peux aller avec Lio à la plage aujourd'hui :< ?\"\n{lio} : \"Je vous promet qu'il n'y aura pas de dérives :<\"\n{lena} : \"... Vous êtes térifiantes toutes les deux quand vous essayez de m'enjôler tout en sachant que ça marche pas sur moi...\"\n{alice} : \"Est-ce que tu pourrais faire semblant d'être affectée pour récompenser nos efforts :< ?\"\n{lena} : \"`Soupir` Soit amusez-vous bien. Parcontre je veux que vous preniez Shushi avec vous. Vous y êtes tellement allé fort que vous avez réussi à la convaincre qu'elle voulais aller à la plage alors que c'est pas son truc.\"\n{shushi} : `Regarde fixement Lio en tenant les queues de cette dernières comme des doudoux`\n{lio} : \"Je n'y vois pas de problème ^^ J'ai l'habitude des enfants\"",
        "{lily} : \"`Se matérialise dans la chambre des filles et carresse doucement le front d'Alice qui faisait manifestement un cauchemar en murmurant` Tu sais que tu nous poses beaucoup de problèmes toi... ? ... Parfois je me demande si tu fais pas exprès... À l'école ils nous disent souvent que les vampires sont bien plus conscient dans leurs rêves que les humains... Et Sixtine me dit toujours que tu veux connaître et être amie avec tout le monde... Est-ce que tu reconnais ta soeur lorsqu'elle viens t'aider avec tes cauchemars et que tu veux juste apprendre à connaître cette autre facette d'elle... ?",
        "{iliana} : `Est assise sur la table en regardant son téléphone`\n{lena} : \"Iliana, est-ce que tu pourrais éviter de t'assoir sur la table, encore plus si il y a des verres dessus ?\"\n{iliana} : `Sursaute car elle ne l'avait pas entendu arriver et fait tomber un verre sans faire exprès avec sa queue` \"... désolée...\"\n{lena} : \"`Facepalm` Est-ce que tu pourrais nettoyer ça toute seule ou je dois sortir le Pshit Pshit ?\"\n{iliana} : \"Pas le Pshit Pshit :< !\"",
        "{lia} : \"`Se laisse tomber dans l'herbe` J'en peux plus de ces séances d'entrainement avec Maman, pourquoi il y a que moi qui y ai le droit ?\"\n{liu} : \"Tu sais très bien pourquoi...\"\n{lia} : \"Je sais je sais... elle veut que je ressemble à peu plus à nos demi-soeurs japonaise... Que je reprenne le flambeau des démonnes renardes à neufs queues... mais pourquoi moi particulièrement ?\"\n{liu} : \"Hum... Il est vrai que de nous quatres tu es celle qui a le plus de pouvoirs, et en plus tu es l'ainée. Peut-être qu'elle veut que tu montre l'exemple ?",
        "{shushi} : \"`Mange son sandwich assise dans l'herbe devant la maison et entend un bourdonnement singulier près de son oreille, suivi d'un sursaut d'attention de Shihu` N'y pense même pas\"\n{shihu} : \"Mais le moustique '^' !\"\n{shushi} : \"On se fait toujours punir à chaque fois que tu utilises ta magie pour des moustiques. J'ai envie d'avoir des desserts moi !\"\n{shihu} : \"Mgmgm même juste une petite flamme ?\"\n{shushi} : \"Ta dernière \"Petite Flamme\" a failli mettre le feu au salon...\"\n{shihu} : \"Hé ! C'est pas ma faute si il s'était posé sur un rideau '^' !\""
    ],
    [# September
        "{lia} : `Est couchée dans l'herbe avec ses soeurs à regarder les nuages` \"Dites... Vous pensez qu'on a combien de soeurs, nièces, petites nièces etceteras... ?\"\n{liz} : \"Hum... Tu connais très bien la réponse Lia...\"\n{lia} : `Lève un bras au ciel comme pour essayer d'attraper les étoiles en soupirant` \"Je reformule... Vous pensez qu'elles sont combien là haut ?\"\n{lio} : \"... J'aurais voulu les connaîtres aussi...\"\n{liz} : `Se redresse en regardant ses soeurs` \"Ça ne sert à rien de s'apitoyer sur leurs sorts. Oui plus d'un millier d'années nous sépare de la mort de la dernière représentante de notre espèce, mais le fait est que Maman a réussi à se libérer et que nous as donné naissance. On est peut-être les kitsunes les plus jeunes à l'heure actuelle, mais de nous a le potenciel pour augmenter dragstiquement notre démographie\"\n{liu} : \"Ça me fait bizarre de penser qu'on est en même temps tout en bas de l'arbre généalogique mais en même temps tout en haut...\"\n{liz} : `Secoue la tête` \"On est ni en bas ni en haut. On est une nouvelle branche à part entière\"",
        "{karai} : \"Ainsi donc avec Clara tu es devenue une soigneuse Alty...\"\n{alty} : \"Ça pose un problème particulier ?\"\n{karai} : \"Oh heu non évidammant ! C'est juste que... dans ma timeline tu était plutôt du genre shinobi... Ça me fait bizarre c'est tout...\"\n{alty} : \"Si j'en crois que ce les autres m'ont dit ce changement est plus ou moins... logique\"",

    ],
    [# October
        "{lena} : \"Hé Iliana, tu pourrais me rendre un service ?\"\n{catili} : \"Mui ?\"\n{lena} : \"Tu as déjà entendu parler d'un certain Schrödinger ?\"\n{iliana} : \"... Oh zut j'ai totalement oublié ! Alice m'avait proposé de les accompagner à la plage, il faut que je me trouve un maillot de bain !\"",
        "{clemence} : \"... Je sais que tu as la manie de dormir partout Sixtine... Mais dans mon cercueil tout en étant claustrophobe ?\"\n{sixtine} : `Dort à point fermé`",
        "{shehisa} : \"Tiens ça me fait penser, mais tu avais pas dit que tu libérais tes morts-vivants si ils était plus en état de se déplacer correctement ?\"\n<:kiku:962082466368213043> : \"C'est le cas\"\n{shehisa} : \"Bah heu... \" `Jette un oeuil à une goule qui n'avait plus qu'un tron`\n<:kiku:962082466368213043> : \"C'est pas ce que tu crois. C'est lui qui veut pas que je le libère\"",
        "{gweny} : \"Tiens Karaï ça faisait un moment\"\n`La poupée vint hug la jambe de Gwen sans rien dire`\n{gweny} : \"Ah. Je vois `Gwendoline prit la poupée des ses bras en lui caressant doucement la tête` Vas-y je t'écoute...\"\n{karai} : \"Pourquoi est-ce que je dois endurer tout ça... 300 ans à attendre pour qu'au final ma place soit prise par une autre version de moi-même... Et par dessus ça je peux même pas en finir...\"\n{gweny} : \"... Je n'ai pas de réponse à t'apporter malheureusement...\"\n\n{karai} : \"Prend soins de ton père pour moi s'il te plaît...\"\n{gweny} : \"Honnêtement je ne pense pas qu'il ai vraiment besoin que je veille sur lui mais j'y penserais\"\n{karai} : \"Merci...\"",
        "{alice} : \"Madame Ruby ? ça va être l'anniversaire de Clémence à la fin du mois mais je sais pas quoi lui offrir... Elle a tellement de truc plus puissant les uns que les autres et je pense pas qu'une quelconque relique que je serais capable de lui trouver puisse rivaliser...\"\n<:ruby:958786374759251988> : \"Je pense que tu te prend trop la tête. Je suis persuadé que qu'importe ce que tu lui offre, elle le trouvera incomparable si tu y a mis du tiens, même si elle le dira pas directement\""
    ],
    [#November
        "{sixtine} : \"`Fixe le plafond en arrivant pas à dormir lorsqu'elle entendit un bâtement d'ailes et senti une chauve-souris se blotir contre sa tête` Un cauchemar ?\"\n{alice} : `Répond par un petit couinement affirmatif`\n{sixtine} : `La prend doucement dans ses mains et la place contre sa poitrine en lui carressant la tête avec son pouce`\n{alice} : `Finit par se rendormir bercée par les bâtements de coeurs de sa soeur et ses caresses`",
        '{helene} : "Tu es au courant que mourir par hémorragie est tout sauf une mort agréable hein ?"\n{shehisa} : "Je vois pas où est la différence avec les infections que tu donnes à tes adversaires. Je suis peut-être pas une soigneuse, mais Papa m\'a suffisament initiée pour savoir que les maladies que tu leur refile sont tous sauf agréable"',
        '{shehisa} : "Tu me reproche d\'avoir suivi la voie de Maman, mais tu devrais voir comment tu te comporte face à un ennemi quand tu veux lui faire avaler la pilule"\n<:helene:906303162854543390> : "Qu\'est-ce que tu insinue par là ?"\n{shehisa} : "Que je suis pas la seule à avoir héritée des talents de Maman"',
        "<:benedict:958786319776112690> : \"Bon j'ai fais ce que tu m'as demandé et selon mon correspondant, effectivement il a bien constaté qu'une âme incomplete est coincée au purgatoire depuis plusieurs décinies\"\n{shehisa} : \"Merci\"\n<:benedict:958786319776112690> : \"Juste merci :< ?\"\n{shehisa} : \"Merci Bénédicte d'avoir fait jouer tes relations surnaturelles afin de répondre à ma question\"\n<:benedict:958786319776112690> : \":< ça ira je suppose...\"",
        "{shihu} : \"Il me faut des cristaux magiques sinon je vais jamais y arriver...\"\n{shushi} : \"Tu en fais trop Shihu... Tu t'épuises pour rien, c'est pas grave si on y arrive pas...\"\n{shihu} : \"On doit y arriver sans l'aide de personne... On en peut plus de se faire rabaissée par Clémence dès qu'elle en a l'occasion, je veux lui montrer qu'on est capacle de réussir là où elle a échoué et lui rabatre le clapet... Pour une fois...\"\n{shushi} : \"Clémence a plus de quatre fois notre âge... On peut pas rivaliser !\"\n{shihu} : \"Mais on a quelque chose qu'elle n'a pas : Une réserve presque infinie de l'une des quatres énergies qui régient l'univers.\"\n{shushi} : \"T-Tu va finir par disparaitre si tu continue comme ça... J'ai... j'ai pas envie de me retrouver seule...\"\n{shihu} : \"... Ça serait peut-être mieux ainsi... Ma simple existance a débilement compliqué la tienne...\"\n{shushi} : `Prend spontanément le controle de sa main droite pour se gifler elle-même` \"Je t'interdis de penser ce genre de truc tu m'entends !?\"",

    ],
    [# December
        "{helene} : \"Ah Shi' ! Je t'ai fait une nouvelle tenue en fourure tu en pense quoi ?\"\n{shehisa} : `Prend la tenue et va se changer, puis se regarde dans un miroir` \"Hum... elle me plait bien. Et c'est vrai que je me sensait un peu... sous-vêtue ces derniers temps\"\n{helene} : \"Quelle idée de porter des trucs aussi cours en hiver aussi...\"",
        "{alice} : `Boit un chocolat chaud en étant assise sur un fauteuil devant la cheminée`\n{sixtine} : `Arrive dans le salon avec sa couette sur les épaules et monte dans le fauteuil pour se blottir contre Alice`\n{alice} : \"Ça va pas ?\"\n{sixtine} : \"Juste un cauchemar...\"\n{alice} : `patpat`",
        "{clemence} : `Lit un grimoire en étant assise sur un fauteuil devant la cheminée`",
        "`Gwen descendit dans le séjour pour aller préparer le petit déjeuné quand elle vit Lena en train de dormir sur le canapé. Sur la table se trouve plusieurs pièces de ce qu'elle devina être un nouveau fusil longue portée et en déduit que l'inkling a encore veillé jusqu'à point d'heure pour mettre au point un nouveau joujou\nEn approchant, elle vit Shushi assise à côté de sa mère en train d'essayer de résoudre un Rubik's cube silencieusement. En la voyant arriver, celle-ci mit doucement un doigt sur ses lèvres. Gwen lui sourit gentiment puis alla dans la cuisine`",
        "<:benedict:958786319776112690> : \"Même si cette idée me plaît toujours pas, je dois avouer que tu fais une bonne enfant de coeur, tu as une plutôt bonne bouille quand tu as pas la bouche grande ouverte\"\n{alice} : M-merci ma Soeur, je suppose...\"",
        "{shushi} : \"Dit Shihu...\"\n{shihu} : \"Vi ?\"\n{shushi} : \"Tu as une idée de cadeau pour miman ? Son anniversaire arrive bientôt...\"\n{shihu} : \"Hum... J'avais pensé qu'on pouvait peut-être lui trouver un nouveau mortier ? Le sien commence à dater...\"\n{shushi} : \"Lequel ? Celui pour ses plantes ou celui avec lequel elle bombarbe les monstres ?\"\n{shihu} : \"... Je pense qu'il y en a un qui est plus à notre portée...\"\n{shushi} : \"... C'est pas faux...\""
    ]
]

shopRepatition = [4, 5, 8, 3]                 # Shop's item category length

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
class says:
    """A class for storing the says message from a entity"""
    def __init__(self, start=None, ultimate=None, limiteBreak=None, onKill=None, onDeath=None, onResurect=None, blueWinAlive=None, blueWinDead=None, blueLoose=None, redWinAlive=None, redWinDead=None, redLoose=None, blockBigAttack=None, reactBigRaiseAllie=None, reactBigRaiseEnnemy=None, bigRaise=None, reactEnnemyKilled=None, reactAllyKilled=None, reactAllyLb=None, reactEnemyLb=None):
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
    blueWinAlive="Une victoire en bonne uniforme",
    redWinAlive="Va falloir faire mieux que ça, là prochaine fois.",
    redWinDead="Pas mal. Mais pas suffisant",
    redLoose="Ahah, pas trop mal cette fois-ci. Mais ce n'était qu'un entrainement",
    reactBigRaiseAllie="Bien joué {caster}",
    reactBigRaiseEnnemy="Pas trop mal, mais on va pas vous laisser faire pour autant",
    reactEnnemyKilled="Pas trop mal {killer}",
    reactAllyKilled="T'en fais pas {downed}, je m'en charge.",
    blockBigAttack="Hé Luna ! Un brisage de l'Espace Temps ça te dis ?\"*\n<:luna:909047362868105227> : \*\"C'est pas déjà ce que l'on était en train de faire ?",
    reactEnemyLb="`Ricane` Si ça vous chante",reactAllyLb="Belle {skill}, {caster}"
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
    reactAllyLb="Mow, je voulais terminer en apothéose moi :<",
    reactEnemyLb="Pff, tu appelles ça une démonstration, {caster} ?",
    limiteBreak="C'est l'heure de terminer en apothéose !"
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
    reactAllyLb="J'aurais pû le faire moi-même {caster}."
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
    start="Dézolé Miman... Mais on peut pa ti laizer fire.",
    onKill="Zi te plait...",
    onDeath="D-Dézolée !",
    blueLoose="Ze ferais miheu... la prozaine fois...",
    blueWinAlive="Wiiii !",
    reactBigRaiseAllie="Bien zoué {caster}"
)

shushiSays = says(
    start="Je vais te montrer ce que je peux faire Miman !",
    ultimate="C'est maintenant ou jamais !",
    onKill="Tu m'en voudras pas hein ? ?",
    onDeath="Miman !",
    onResurect="Ze veux encore dodo...",
    blueWinAlive="`Petite danse de la victoire` ?",
    blueWinDead="Bien zoué !",
    blueLoose="Je vais devoir faire mieux la prochaine fois !",
    redWinAlive="Alors alors ?",
    redWinDead="Peux mieux faire !",
    redLoose="Oh..."
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
    onKill="Tu risques de broyer du noir pendant un moment, dézolée !"
)

temSays = says(
    start="HoIIII !",
    onDeath="Ayayaya !"
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
    reactEnemyLb="C'est beau de s'acharner inutilement..."
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
    start="(Courage John. Montre lui que tu as appris à devenir un combattant.)"
)

liaSays = says(
    start="Ça vous dirait de danser avec moi ?",
    onKill="Oh déjà... ?",
    onDeath="Hii ! Compris compris !",
    redWinAlive="C'était marrant !",
    redLoose="Vous savez pas rire...",
    reactBigRaiseAllie="Toujours aussi jouissif {caster}",
    reactEnemyLb="Mow, je crois qu'ils sont un peu en colère"
)

liuSays = says(
    start="Hé ! Une course d'endurance vous en pensez quoi ?",
    onKill="Va falloir mieux gérer ta fatigue la prochaine fois",
    onResurect="Une seconde course ?",
    redLoose="Hé bah... Finalement c'est moi qui ai mordu la poussière",
    limiteBreak="Pas si vite !",
    reactEnemyLb="C'est bon tu as fini {caster} ?"
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
)

lizSays = says(
    start="Tiens donc, des nouvelles braises",
    ultimate="Allez quoi, déclarez moi votre flamme !",
    onKill="Woops, j'y suis allé trop fort manifestement",
    onDeath="Pff, vous êtes pas drôle",
    redLoose="Waw, je me suis jamais faite autant refroidir rapidement...",
    reactEnemyLb="T'enflamme pas trop vite {caster}."
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
    ultimate="Laissez moi tranquille...",
    redWinAlive="Je retourne dessiner maintenant...",
    redLoose="Zzz...",
    reactBigRaiseAllie="Waw...",
    reactAllyLb="C'était joli à regarder..."
)

clemPosSays = says(
    start="J'en ai ma claque des gens de votre genre.",
    onKill="Un de plus, un de moins. Quelle importance",
    redWinAlive="Restez à votre place.",
    redLoose="Que..."
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
    onKill="Heu... Je... je crois que j'y suis allé trop fort, désolée !"
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

lenaTipsMsgTabl = [
    "Est-ce que quelqu'un lit vraiment ça ?",
    "Si vous réalisez la commande /fight alors qu'il vous reste moins de 10 minutes de repos, votre combat sera mis en file d'attente et se lancera automatiquement une fois le décompte écoulé",
    "Une fois le tour 20 atteint en combat, il est plus possible de réanimer un combattant et tout le monde subis des dégâts en fonction de ses PVs Maximums",
    "Hé vous voulez un conseil de chargement inutile que tout le monde ne lit qu'une fois puis oubli leur existance ? En voilà un",
    "En fin de combat, vous gagnez de l'expérience en fonction des ennemis vaincu. Si un ennemi a été réanimé mais n'a pas été vaincu une seconde fois, il ne donne que la moitié de l'expérience qu'il devait donner",
    "En général, les combattants de dernière ligne font plus de dégâts que leurs camarades en mêlée, mais sont bien plus fragile",
    "Si une entité repoussée rencontre un obstacle, elle subit des dégâts Harmonie d'une puissance de 10 multipliée par le nombre de cases qu'il lui restait à parcourir",
    "Si une entité ne peux pas se téléporter parceque toutes les cases adjacantes à la cible sont occupées, elle s'inflige des dégâts Harmonie d'une puissance de 20",
    "L'Harmonie est une statistique spéciale qui est juste un beau mot pour dire \"Statistique la plus élevée\"",
    "L'Harmonie ne prend pas en compte les statistiques d'actions, mais ceux-ci sont cependant bien rajouté à la statistique d'Harmonie après sa définition",
    "Les Trancendances prennent en compte la statistique principale la plus élevée du lanceur, mais également sa meilleur statistique d'action, indépendamant de l'action en question",
    "Les compétences de réanimations prennent en compte la statistique d'action la plus élevée parmis les Soins, Armures ou Bonus",
    "Chaque réanimation accorde une armure absolue équivalente à 20% des PVs maximums du réanimé à ce dernier, mais cette valeur est augmentée à 50% pour les combattants manuels",
    "Les armures absolues protègent de tous types de dégâts à l'exeption de la Mort Subite et des coûts en PV des compétences démoniques",
    "Les armures absolues et normales absorbent des dégâts supplémentaires lorsqu'elles sont détruites. Par défaut, cette valeur est égale à votre niveau, mais certaines compétences peuvent influer dessus",
    "Kiku et les Zombies commencent tous leurs combats avec le status \"Réanimée\"",
    "Certains ennemis comme l'OctoBOOM ne peuvent pas être réanimés",
    "Les Berserkeur ont besoin de pouvoir infliger des dégâts pour être des tanks efficace. Par conséquent leur donner un autre second role que DPT est pas vraiment une bonne idée",
    "Les statistiques des Idoles leur permettent prendre un role secondaire de soingneur, là où les Innovateurs peuvent se tourner vers l'armure si ils le désirent",
    "Les statistiques des Altruistes ainsi que leurs compétences propres en fond de très bon soigneur, mais avec les bons équipements ils peuvent aussi être de bon booster d'équipe",
    "Les Poids Plumes ont naturellement une endurance et une force relativement faible, mais cela est compensé par leur grande agilité qui leur permet d'esquiver ou d'infliger des coups critiques plus souvent que ses concurants de mêlée\nDe plus, à l'instar des Observateurs, leurs coups critiques infligent plus de dégâts",
    "Le taux d'esquive est calculé en fonction de la différence entre la précision de l'attaquant et l'agilité de l'attaqué.\nSi l'attaqué est plus agile, le taux de réussite de l'attaque est diminuée jusqu'au maximum la moitié de sa valeur\nÀ contratio, une précision plus élevée de l'attaquant peut lui donner jusqu'à deux fois plus de chances de toucher",
    "Le 19 de chaques mois, les records mensuels sont rénitialisés",
    "Lors d'un raid, vous êtes associé à une équipe dont le niveau moyen est similaire à celle de la votre. Cependant, cette équipe tierce n'obtient aucune récompense",
    "Vous vous souvenez de l'aspiration \"Stratège\" ? Ouais moi non plus",
    "Funfact : Tout à commencé sur une aire d'autoroute pendant que Lénaïc s'ennuyait à attendre que sa famille revienne de sa pause pipi",
    "Les Sorciers créent de petites détonnations quand ils éliminent un ennemi. Celles-ci prennent en compte les statistiques de Magie et de Dégâts indirects",
    "Les Têtes Brulées réduisent petit à petit les PV maximums de leurs cibles, ce qui les rends particulièrement efficaces contre les ennemis qui se soignent beaucoup",
    "Utiliser des compétences divines vous fait peu à peu perdre votre prise sur la réalité au fil du combat. Cela est représenté par des pertes de PV maximums lors de l'utilisation de ces dernières",
    "Utiliser des compétences démoniaques requière une quantité d'énergie si importe que vous perdrez une partie de vos PV courrants",
    "En lançant des combats normaux, vous avez une petite chance de revivre un combat passé qu'à vécu un des alliés temporaires\nCes combats sont appelés \"Combat par procuration\"",
    "Certaines compétences comme Mort Vivant ou Bolide peuvent rendre leur utilisateur invulnérable ou impossible à vaincre pendant un cours instant, permettant aux soigneurs d'essayer de leur sauver la mise",
    "Certaines compétences comme quelques transcendance ou Abnégations ont pour effet secondaire de réanimé les alliés vaincus dans la zone d'effet, si ils peuvent encore l'être",
    "Les Protecteurs, Vigilants et Enchanteurs sont trois aspirations qui tirent partie de leur capacités à attirer (et encaisser) les attaques adverses",
    "La Résistance Soin progresse plus rapidement si plusieurs soigneurs sont présents dans la même équipe",
    "Repose en paix, aspiration Invocateur",
    "Une intelligence élevée permet, en plus de pouvoir donner une bonne quantité d'armure, d'avoir une bonne probabilité d'effectuer des dégâts indirects critiques tout en diminuant la probabilité d'en recevoir",
    "Les statistiques de Clémence, Félicité, Sixtine et Alice augmente légèrement si plusieurs d'entre elles sont dans le même combat",
    "Lohica est plutôt mauvaise perdante et infligera __Poison d'Estialba__ à son éliminateur lorsque ses PVs tombent à 0",
    "Les Sorciers infligent des dégâts indirects critiques plus élevés que les autres aspirations",
    "Le Charisme de Liu, Lia, Liz et Lio augmente légèrement si au moins deux d'entre elles sont dans le même combat",
    "Alice n'aime pas vraiment que quelqu'un monte sur scène en sa présence",
    "Les compétences \"Haima\" et \"Pandaima\" ont une très bonne synergie avec l'une des compétences qui augmente le nombre de PAr supplémentaire des armures lorsqu'elles sont détruites. Elles peuvent ainsi déclancher leurs effets 5 fois, résultant en une réduction de dégâts encore plus conséquante",
    "Lors d'un combat normal contre les alliés temporaires, certains ont des malus spécifiques pour diminuer un peu leur efficacité au combat",
    "Par défaut, chaque combattant ne peut voler un nombre de PV supérieur à 45 fois leur niveau avec une même attaque. Cette limite est surtout là pour éviter que certain boss se soigne d'une quantité astronomique de PV lorsqu'ils attaquent.\nCependant, certains ennemis ou alliés temporaires peuvent outre-passer en partie cette limite",
    "Toutes les aspirations de supports, de soins et d'armures voient leur probabilité d'utiliser des options offensives augmenter lorsqu'ils n'ont plus beaucoup de DPT alliés en vie ou que le combat se rapproche du tour 20.",
    "Les dégâts de Mors Subite sont réduits de 90% sur les boss",
    "Les armes runiques, le passif Maitrise Elémentaire ainsi les compétences Convertion Elémentaire et Concentration Elémentaire sont le meilleur moyen de gagner des effets élémentaires.\nCes effets augmentent de 5% la puissance des compétences exclusives à leur élément et certaines compétences les consommes pour obtenir des effets supplémentaires.",
    "Les Sorciers et les Attentifs infligent des dégâts indirects critiques plus élevées que les autres aspirations.",
    "Les effets de dégâts indirects des Attentifs ont pour effet secondaire de réduire les soins reçus par leur cible en fonction de leur puissance.",
    "Les redirections de dégâts ne redirigent que les dégâts directs, à l'exeption des pattes de The Giant Ennemi Spider; bien que rien n'est affiché, cette dernière subit bien l'intégralité des dégâts indirects reçus par ses pattes",
    "Les débuts de combat sont les moments où les Idoles et les Innovateurs octroient des bonus plus puissant qu'à l'accoutumé. Cependant, ceux des Idoles voient leur puissance diminuer au fur et à mesure que leur équipe se fait vaincre tandis que ceux des Innovateurs dépérissent en même temps que l'équipe adverse",
    "À chaque fois que vous prestigez votre personnage, les combats qui s'en suivent seront de plus en plus difficiles",
    "Les alliés temporaires s'addaptent au niveau de prestige de votre équipe, qu'ils soient avec ou contre vous",
    "En combat de raid, il est possible de cumuler jusqu'à 4 charges de Transcendance. La compétence qui en résultes inflige beaucoup de dégâts au boss, mais réanime, soigne et boost également les alliés"
]

ilianaSaysNormal = says(
    start="Puisse ce combat être bénéfique pour tous !",
    ultimate="Qu'est-ce que vous pensez du pouvoir de la Lumière ?",
    limiteBreak="Que la Lumière nous protège !",
    onKill="Je décline toute responsabilité en cas de tache blanche incrustée dans ta rénite",
    onDeath="Humf !",
    reactAllyKilled="J'aurais du faire plus attention, désolée",
    reactBigRaiseAllie="On reprend ses esprits et on y retourne"
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
    reactBigRaiseEnnemy="Vos âmes m'appartiennent déjà, pourquoi résister ?"
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

# ============ Procur Temp stuff =============
procurTempStuff = {
    "Shushi Cohabitée":[0,
        ["Barrête de la cohabitation","dualHat","<:coaBar:911659734812229662>"],
        ["Robe de la cohabitation","dualDress",'<:coaDress:911659797076660294>'],
        ["Bottines de la cohabitation","dualBoost",'<:coaBoots:911659778995007528>'],
        [[0,0],[5,0.2],[2,0.3],[0.5,1],[0.5,1],[3,0.8],[3.6,0.8],[1,0.2],[0.5,0.3],[0.8,0.2]]
    ],
    "Luna prê.":[250,
        ["Boucle d'oreille ombrale",'lunaDarkPendant','<:linapendant:890599104902754326>'],
        ["Robe de soubrette ombrale ",'lunaDarkMaidDress','<:linadress:890598423152185364>'],
        ["Ballerines ombrales",'lunaDarkFlats','<:linaflats:890598400624586763>'],
        [[1.2,2.55],[1.15,0.4],[0.8,0.5],[1,1.2],[1,0.6],[0.2,0.3],[0,0],[0.25,0.35],[0.25,0.35],[0,0]]
    ],
    "Iliana prê.":[250,
        ["Casque de la neko de la lueur ultime", 'ilianaPreHead','<:zenithHead:913170464581484554>'],
        ["Armure de la neko de la lueur ultime", 'ilianaPreArmor','<:zenithArmor:913170492452646922>'],
        ["Sorolets de la neko de la lueur ultime", 'ilianaPreBoots','<:zenithBoots:913170512564334623>'],
        [[0.2,0.1],[1,2.5],[1,3],[0.5,0.9],[1.2,0.3],[3,0.05],[5,0.05],[1.2,0.2],[1,0.05],[1,0.05]]
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
    "Une à droite et une à gauche ! {icon} __{name}__ a réussi à faire **{value}** dégâts avec des beignes bien placées ce mois-ci !"
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
    "Savoir s'adapter à toutes les situations est crucial. Et {icon} __{name}__ a du avoir de bon réflexe pour avoir soigné **{value}** points de vie ce mois-ci"
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
    "Hé bah ! On peut dire que {icon} __{name}__ s'y connais en armure, {il} en a donné **{value}** points jusqu'à présent"
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
    "La concurence est dure par contre. Si tu cherches le haut du podium, il va falloir faire mieux que {icon} __{name}__ et ses **{value}**"
]

randomPurcenMsg = [
    "Ça fait quoi... **{purcent}** % du total de son équipe ?",
    "Hum... Je crois que ça doit faire... **{purcent}** % du total de son équipe ?",
    "D'après ma calculatrice, ça fait **{purcent}**% du total de son équipe"
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
    ["Je sais que le role de Support n'est pas particulièrement attractif, mais bon il reste quand même utile d'en avoir un"]
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

uniqueitems, copyTablBreak = [], tablBreakingTheLimits[:]
for cmpt in range(len(copyTablBreak)):
    if copyTablBreak[cmpt] not in uniqueitems:
        uniqueitems.append(copyTablBreak[cmpt])
    else:
        tablBreakingTheLimits.remove(copyTablBreak[cmpt])

print("Nb bonus différents : {0}".format(len(tablBreakingTheLimits)))

summation = 0
for cmpt in range(len(tablBreakingTheLimits)):
    summation += len(tablRangeLB[len(tablBreakingTheLimits[cmpt])-1])

print("Nb bonus Total : {0}".format(summation))
