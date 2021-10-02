"""
Constants module.
Here stand the first brick of the bot
"""
from datetime import timedelta
import os


#Constantes :
# Area of effects
AREA_MONO = 0 # Caster only
AREA_CIRCLE_1 = 1 # Circles (target include)
AREA_CIRCLE_2 = 2
AREA_CIRCLE_3 = 3
AREA_CIRCLE_4 = 4
AREA_CIRCLE_5 = 5
AREA_CIRCLE_6 = 6
AREA_CIRCLE_7 = 7
AREA_ALL_ALLIES = 8 # All allies
AREA_ALL_ENNEMIES = 9 # All ennemies
AREA_ALL_ENTITES = 10 # All
AREA_CONE_2 = 11 # Cones
AREA_CONE_3 = 12
AREA_CONE_4 = 13
AREA_CONE_5 = 14
AREA_CONE_6 = 15
AREA_CONE_7 = 16
AREA_LINE_2 = 17 # Lines from target
AREA_LINE_3 = 18
AREA_LINE_4 = 19
AREA_LINE_5 = 20
AREA_LINE_6 = 21
AREA_DONUT_1 = 22 # Circles (target exclude)
AREA_DONUT_2 = 23
AREA_DONUT_3 = 24
AREA_DONUT_4 = 25
AREA_DONUT_5 = 26
AREA_DONUT_6 = 27
AREA_DONUT_7 = 28
AREA_DIST_3 = 29 # Circles (Must be > 2)
AREA_DIST_4 = 30
AREA_DIST_5 = 31
AREA_DIST_6 = 32
AREA_DIST_7 = 33
AREA_ARC_1 = 34 # Arc
AREA_ARC_2 = 35
AREA_ARC_3 = 36

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

allTriggers = [TRIGGER_PASSIVE,TRIGGER_DAMAGE,TRIGGER_END_OF_TURN,TRIGGER_DEATH,TRIGGER_DEALS_DAMAGE,TRIGGER_INSTANT,TRIGGER_START_OF_TURN,TRIGGER_ON_REMOVE]

# Useless stuff
DAMAGE = 0
DAMAGE_IRRECTIBLE = 1
DAMAGE_TRUE = 2
DAMAGE_FIXE = 3

HEAL = 0
HEAL_FIXE = 0

REZ = 0
REZ_POURCENTAGE = 1
REZ_FIXE = 2

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
TYPE_INVOC = 10

tablTypeStr = ["Armure","Dégâts indirects","Soins Indirects","Résurection indirecte","Boost","Resurection","Dégâts","Malus","Soins","Unique","Invocation"]

# Stats
STRENGTH = 0
ENDURANCE = 1
CHARISMA = 2
AGILITY = 3
PRECISION = 4
INTELLIGENCE = 5
PURCENTAGE = 6
FIXE = 7
HARMONIE = 8

nameStats,nameStats2 = ["Force","Endurance","Charisme","Agilité","Précision","Intelligence"],["Résistance","Pénétration","Critique"]
allNameStats = nameStats+nameStats2

# Status for entities
STATUS_ALIVE, STATUS_DEAD, STATUS_RESURECTED,STATUS_TRUE_DEATH = 0,1,2,3

# Aspirations
BERSERK, OBSERVATEUR, POIDS_PLUME, IDOLE, ERUDIT, TETE_BRULE, STRATEGE, ALTRUISTE, AVENTURIER = 0,1,2,3,4,5,6,7,8
inspi = ["Berserkeur","Observateur","Poids plume","Idole","Erudit","Tête brulée","Stratège","Altruiste","Aventurier"]

# "Target" values
ALL, TEAM1, TEAM2, ALLIES, ENNEMIS = 0,1,2,3,4

# Selected options for fight
OPTION_WEAPON,OPTION_SKILL,OPTION_MOVE,OPTION_SKIP = 0,1,2,3

# Genders. 2 for default
GENDER_MALE, GENDER_FEMALE, GENDER_OTHER = 0,1,2

# Do I use those ? I dunno
allDamages = [DAMAGE,DAMAGE_IRRECTIBLE,DAMAGE_TRUE,DAMAGE_FIXE]
allHeals = [HEAL,HEAL_FIXE]
allRez = [REZ,REZ_POURCENTAGE,REZ_FIXE]

# Color constants
red,light_blue,yellow,green,blue,purple,pink,orange,white,black = 0xED0000, 0x94d4e4, 0xFCED12, 0x1ED311, 0x0035E4, 0x6100E4, 0xFB2DDB,0xEF7C00,0xffffff,0x000000
colorId = [red,orange,yellow,green,light_blue,blue,purple,pink,white,black]
colorChoice = ["Rouge","Orange","Jaune","Vert","Bleu Clair","Bleu","Violet","Rose","Blanc","Noir"]

# Aspiration's max stats
# Refert to Aspiration's constants value
maxStrength = [
    50, # Ber
    50, # Obs
    30, # Poi
    15, # Ido
    25, # Eru
    45, # Tet
    25, # Omae wa mou shinderu
    15, # Alt
    35  # Ave
]

maxEndur = [
    60, # Ber
    20, # Obs
    20, # Poi
    15, # Ido
    30, # Eru
    45, # Tet
    35, # Nani
    45, # Alt
    30  # Ave
]

maxChar = [
    30, # Ber
    35, # Obs
    25, # Poi
    55, # Ido
    35, # Eru
    25, # Tet
    30, # Ohoh
    55, # Alt
    30  # Ave
]

maxAgi = [
    15, # Ber
    25, # Obs
    65, # Poi
    30, # Ido
    25, # Eru
    25, # Tet
    30, # You dare approche me
    35, # Alt
    35  # Ave
]

maxPreci = [
    30, # Ber
    35, # Obs
    35, # Poi
    30, # Ido
    35, # Eru
    25, # Tet
    25, # Insted of running away form me
    20, # Alt
    35  # Ave
]

maxIntel = [
    15,  # Ber
    35, # Obs
    30, # Poi
    50, # Ido
    50, # Eru
    35, # Tet
    35, # I can't beet yout shit without be any closer
    30, # Alt
    35  # Ave
]

# Constants for "orientation" field for skills
TANK,DISTANCE,LONG_DIST = "Tank","Distance","Longue Distance"
DPT,HEALER,BOOSTER,MAGIC = "Bers, Obs, P.Plu, T.Bru","Ido,Alt","Ido, Eru","T.Bru, Obs, Eru"

# Elementals
ELEMENT_NEUTRAL = 0
ELEMENT_FIRE = 1
ELEMENT_WATER = 2
ELEMENT_AIR = 3
ELEMENT_EARTH = 4
ELEMENT_LIGHT = 5
ELEMENT_DARKNESS = 6

elemEmojis = ["<:neutral:887847377917050930>","<:fire:887847475203932261>","<:water:887847459211079760>","<:air:887847440932290560>","<:earth:887847425459503114>","<:light:887847410141921362>","<:darkness:887847395067568128>"]
elemDesc = [
    "L'élément Neutre (<:neutral:887847377917050930>) est l'élément le plus apprécié des nouvelles recrues.\nSans spécialisations particulière, cet élément permet de tout faire sans trop se casser la tête",
    "L'élément Feu (<:fire:887847475203932261>) est en général préféré par ceux qui aiment tirer sans distinction et faire carnage sans pareil.\nLes dissicles de l'élément Feu infligent un peu plus de dégâts avec les armes et capacité de zone en distance.\n\nPénétration : + 5\nDégâts zones et distance simultanément : +10%",
    "L'élément Eau (<:water:887847459211079760>) est plus propice à la concentration et la sérénité.\nLes adeptes de cet élément inflige plus de dégâts avec les armes ou capacités monocible à distance.\n\nPrécision : + 10\nDégâts monocible et distance simultanément : +10%",
    "L'élément Air (<:air:887847440932290560>) a pour réputation d'être assez capricieu et imprévisible.\nC'est pour cela que ses partisants filent tel le vent pour frapper plusieurs ennemis simultanément.\n\nAgilité : + 10\nDégâts zones et mêlée simultanément : +10%",
    "L'élément Terre (<:earth:887847425459503114>) permet de ressentir la puissance des courants d'énergie télurique et d'en tirer le meilleur parti.\nLes habitués de cet élément infligent des dégâts monocibles en mêlée plus conséquents.\n\nRésistance : + 5\nDégâts monocible et mêlée simultanément : +10%",
    "L'élément Lumière (<:light:887847410141921362>) permet d'entrevoir l'espoir là où les autres ne voit que les ombres.\nLes soins et armures de ces illuminés sont plus conséquents que ceux de leurs congénaires.\n\nSoins et armures : +10%",
    "L'élément Ténèbre (<:darkness:887847395067568128>) n'a pas son pareil pour exploiter les zones d'ombres de leurs adversaires.\nLes dégâts indirects de ces individues sont plus conséquents que ceux de leurs congénères.\n\nDégâts indirects : + 10%"]
elemNames = ["Neutre","Feu","Eau","Air","Terre","Lumière","Ténèbre"]

# List of guild ids for the bots
ShushyCustomIcons = [881900244487516180]
LenaCustomIcons = [881632520830087218,881633183425253396]

stuffIconGuilds = [866782432997015613,878720670006132787,887756868787769434,887846876114739261]
weaponIconGuilds = [866363139931242506,878720670006132787,887756868787769434,887846876114739261]

# For some time related stuff. Time from server != time from France
if not(os.path.exists("../Kawi")):
    horaire = timedelta(hours=2)
else:
    horaire = timedelta(hours=0)
    
# Are we on the livebot or the test bot ?
isLenapy = not(os.path.exists("../Kawi"))

# Tabl of random messages for the shop
shopRandomMsg,rollMessage = [],[]
shopRandomMsg += ['<:ikaLBlue:866459302319226910> : "Si j\'en crois la loi, je suis sensée vous rappeller que vous acceptez d\'utiliser vos armes à vos risques et périls.\nJe suis en aucun cas responsable si elle vous explose dans les mains et que vous la passez à gauche"']
shopRandomMsg += ['<:ikaLBlue:866459302319226910> : "Si quelqu\'un vois l\'autre fanatique des fleurs roses, vous pourrez lui dire qu\'il y en a une qui a poussée dans mon shop ?"']
shopRandomMsg += ['<:ikaLBlue:866459302319226910> : "Hônnetement, ça fait un moment que j\'ai arrêté de compter le nombre de canettes de Coca que me dois Léna"']
shopRandomMsg += ['<:ikaLBlue:866459302319226910> : "Des fleurs roses, blues, jaunes... Je dois vous rappeler que vous partez pas en mission jardinage ?"']
shopRandomMsg += ["<:ikaLBlue:866459302319226910> : \"Faites attention si Alice vous rejoint pour un combat. Il est fort probable qu'elle cherche à obtenir des infos sur vous plutôt que de vaincre vos ennemis\""]
shopRandomMsg += ["<:ikaPink:866459344173137930> : \"J'aime bien les vêtements que tu proposes, mais ça manque de rose...\"\n<:ikaLBlue:866459302319226910> : \"C'est une blague j'espère\""]
shopRandomMsg += ["<a:Ailill:882040705814503434> : \"ReeaperrDusst ? ... Je ssuis prêêtee à pariier ma têtee qu'iil a jammais été oriiginal de saa vie\""]
shopRandomMsg += ["<:ikaBlue:866459319049650206> : `Sit down and eat pop-corns`"]
shopRandomMsg += ["<:ikaBlue:866459319049650206> : `Sit down and eat pop-corns`\n<:ikaBlue:866459319049650206> : `Regarde les pop-corns avec un air interresée`"]
shopRandomMsg += ["<:ikaPink:866459344173137930> : \"Flum POWA !\""]
shopRandomMsg += ["<:ikaPink:866459344173137930> : \"Flum POWA !\"\n<:takoRed:866459004439756810> : \"Les coquelicots c'est mieux je trouve\"\n<:ikaPink:866459344173137930> : \"N'importe quoi ! Ce sont les roses les plus jolies !\"\n<:ikaLBlue:866459302319226910> : \"Vous trois, vous pourriez arrêter de débattre dans mon shop, s'il vous plait ?\""]
shopRandomMsg += ["<:ikaLBlue:866459302319226910> : \"Tiens, Clémence, j'ai trouvé un drôle de livre ces derniers temps et vu que tu t'y connais un peu en runes et magie, je me demandais si tu pouvais essayer de m'apprendre un peu comment m'en servir...\"\n<:takoRed:866459004439756810> : \"Heu... ok\""]
shopRandomMsg += ["<:takoRed:866459004439756810> : \"Ah, Lena. J'ai jeté un coup d'œil à ton livre et heu... Tu as au moins une idée de ce qu'est un Carbuncle ?\"\n<:ikaLBlue:866459302319226910> : \"Absolument pas\"\n<:takoRed:866459004439756810> : \"... Ça va être long...\""]

# Same, but for the roll command
rollMessage += ["Selon toute vraisemblance ce sera un **{0}**","Puisse la chance être avec toi... **{0}** !","Alors Alice tu as obtenu combien ? **{0}** ? **{0}** alors","Sur 100, les chances que la relation Akrisk tienne debout ? Hum... **{0}**","Le nombre de lances que tu va avoir à esquiver est... **{0}**"]