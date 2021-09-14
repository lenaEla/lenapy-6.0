"""
Constants module.
Here stand the first brick of the bot
"""
from datetime import timedelta
import os


#Constantes :
# Area of effects
AREA_MONO = 0
AREA_CIRCLE_1 = 1
AREA_CIRCLE_2 = 2
AREA_CIRCLE_3 = 3
AREA_CIRCLE_4 = 4
AREA_CIRCLE_5 = 5
AREA_CIRCLE_6 = 6
AREA_CIRCLE_7 = 7
AREA_ALL_ALLIES = 8
AREA_ALL_ENNEMIES = 9
AREA_ALL_ENTITES = 10
AREA_CONE_2 = 11
AREA_CONE_3 = 12
AREA_CONE_4 = 13
AREA_CONE_5 = 14
AREA_CONE_6 = 15
AREA_CONE_7 = 16
AREA_LINE_2 = 17
AREA_LINE_3 = 18
AREA_LINE_4 = 19
AREA_LINE_5 = 20
AREA_LINE_6 = 21

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
OPTION_SKIP,OPTION_WEAPON,OPTION_MOVE,OPTION_SKILL = 0,1,2,3

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
maxStrength,maxEndur,maxChar,maxAgi,maxPreci,maxIntel = [50,40,10,15,25,35,25,15,30],[60,20,15,15,30,35,35,35,30],[30,25,25,55,20,25,30,45,30],[15,25,65,25,20,30,30,35,30],[20,35,35,30,35,35,25,20,30],[5,35,30,40,50,20,35,30,30]

# Constants for "orientation" field for skills
TANK,DISTANCE,LONG_DIST = "Tank","Distance","Longue Distance"
DPT,HEALER,BOOSTER,MAGIC = "Bers, Obs, P.Plu, T.Bru","Ido,Alt","Ido, Eru","T.Bru, Obs, Eru"

# List of guild ids for the bots
ShushyCustomIcons = [881900244487516180]
LenaCustomIcons = [881632520830087218,881633183425253396]

stuffIconGuilds = [866782432997015613,878720670006132787]
weaponIconGuilds = [866363139931242506,878720670006132787]

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