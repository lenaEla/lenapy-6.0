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
TRIGGER_AFTER_DAMAGE = 8

allTriggers = [TRIGGER_PASSIVE,TRIGGER_DAMAGE,TRIGGER_END_OF_TURN,TRIGGER_DEATH,TRIGGER_DEALS_DAMAGE,TRIGGER_INSTANT,TRIGGER_START_OF_TURN,TRIGGER_ON_REMOVE,TRIGGER_AFTER_DAMAGE]

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
TYPE_PASSIVE = 11

tablTypeStr = ["Armure","Dégâts indirects","Soins Indirects","Résurection indirecte","Boost","Resurection","Dégâts","Malus","Soins","Unique","Invocation","Passif"]

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
PURCENTAGE = 11
FIXE = 12
HARMONIE = 13

nameStats,nameStats2 = ["Force","Endurance","Charisme","Agilité","Précision","Intelligence","Magie"],["Résistance","Pénétration","Critique"]
allStatsNames = nameStats+nameStats2

# Status for entities
STATUS_ALIVE, STATUS_DEAD, STATUS_RESURECTED,STATUS_TRUE_DEATH = 0,1,2,3

# Aspirations
BERSERK, OBSERVATEUR, POIDS_PLUME, IDOLE, PREVOYANT, TETE_BRULE, MAGE, ALTRUISTE, INVOCATEUR, ENCHANTEUR, PROTECTEUR = 0,1,2,3,4,5,6,7,8,9,10
inspi = ["Berserkeur","Observateur","Poids plume","Idole","Prévoyant","Tête brulée","Mage","Altruiste","Invocateur","Enchanteur","Protecteur"]
aspiEmoji = ['<:berk:915376153580167209>','<:obs:903136012975357952>','<:poi:909548928045842462>','<:ido:909549029027880992>','<:pre:910185501535903775>','<:tet:903136049834889317>','<:mag:909549699160219659>','<:alt:909549006680653824>','<:inv:903136277380087850>','<:enc:903136097553506314>','<:pro:909549059059122176>']

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
red,light_blue,yellow,green,blue,purple,pink,orange,white,black,aliceColor = 0xED0000, 0x94d4e4, 0xFCED12, 0x1ED311, 0x0035E4, 0x6100E4, 0xFB2DDB,0xEF7C00,0xffffff,0x000000,0xFF83FF
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
    25, # Mag
    15, # Alt
    35, # Ave
    25, # Enc
    15  # Pro
]

maxEndur = [
    60, # Ber
    20, # Obs
    20, # Poi
    15, # Ido
    30, # Eru
    45, # Tet
    15, # Mag
    45, # Alt
    30, # Ave
    50, # Enc
    50  # Pro
]

maxChar = [
    30, # Ber
    35, # Obs
    25, # Poi
    55, # Ido
    35, # Eru
    25, # Tet
    40, # Mag
    55, # Alt
    30, # Ave
    30, # Enc
    45  # Pro
]

maxAgi = [
    25, # Ber
    25, # Obs
    65, # Poi
    30, # Ido
    25, # Eru
    30, # Tet
    20, # Mag
    35, # Alt
    35, # Ave
    35, # Enc
    35  # Pro
]

maxPreci = [
    30, # Ber
    40, # Obs
    35, # Poi
    30, # Ido
    35, # Eru
    25, # Tet
    35, # Mag
    20, # Alt
    30, # Ave
    25, # Enc
    15  # Pro
]

maxIntel = [
    15, # Ber
    15, # Obs
    20, # Poi
    55, # Ido
    50, # Eru
    35, # Tet
    20, # Mag
    30, # Alt
    30, # Ave
    10, # Enc
    45  # Pro
]

maxMagie = [
    10, # Ber
    35, # Obs
    25, # Poi
    20, # Ido
    20, # Eru
    15, # Tet
    65, # Mag
    20, # Alt
    30, # Ave
    45, # Enc
    15  # Pro
]

for a in range(0,len(inspi)):
    summation = 0
    for b in (maxStrength,maxEndur,maxChar,maxAgi,maxPreci,maxIntel,maxMagie):
        try:
            summation += b[a]
        except:
            pass

    if summation != 220:
        print("{0} n'a pas le bon cumul de stats : {1}".format(inspi[a],summation))

# Constants for "orientation" field for skills
TANK,DISTANCE,LONG_DIST = "Tank","Distance","Longue Distance"
DPT,HEALER,BOOSTER,MAGIC,SHIELDER = "Bers, Obs, P.Plu, T.Bru","Ido, Pro, Alt","Ido, Pro","Enc, Mag","Ido, Pro, Pre"

# Elementals
ELEMENT_NEUTRAL = 0
ELEMENT_FIRE = 1
ELEMENT_WATER = 2
ELEMENT_AIR = 3
ELEMENT_EARTH = 4
ELEMENT_LIGHT = 5
ELEMENT_DARKNESS = 6
ELEMENT_SPACE = 7
ELEMENT_TIME = 8

elemEmojis = ["<:neutral:887847377917050930>","<:fire:887847475203932261>","<:water:887847459211079760>","<:air:887847440932290560>","<:earth:887847425459503114>","<:light:887847410141921362>","<:darkness:887847395067568128>",'<:astral:907467653147410475>','<:temporel:907467620930973707>']
elemDesc = [
    "L'élément Neutre (<:neutral:887847377917050930>) est l'élément le plus apprécié des nouvelles recrues.\nSans spécialisations particulière, cet élément permet de tout faire sans trop se casser la tête",
    "L'élément Feu (<:fire:887847475203932261>) est en général préféré par ceux qui aiment tirer sans distinction et faire carnage sans pareil.\nLes dissicles de l'élément Feu infligent un peu plus de dégâts avec les armes et capacité de zone en distance.\n\nPénétration : + 5\nDégâts zones et distance simultanément : +10%",
    "L'élément Eau (<:water:887847459211079760>) est plus propice à la concentration et la sérénité.\nLes adeptes de cet élément inflige plus de dégâts avec les armes ou capacités monocible à distance.\n\nPrécision : + 10\nDégâts monocible et distance simultanément : +10%",
    "L'élément Air (<:air:887847440932290560>) a pour réputation d'être assez capricieu et imprévisible.\nC'est pour cela que ses partisants filent tel le vent pour frapper plusieurs ennemis simultanément.\n\nAgilité : + 10\nDégâts zones et mêlée simultanément : +10%",
    "L'élément Terre (<:earth:887847425459503114>) permet de ressentir la puissance des courants d'énergie télurique et d'en tirer le meilleur parti.\nLes habitués de cet élément infligent des dégâts monocibles en mêlée plus conséquents.\n\nRésistance : + 5\nDégâts monocible et mêlée simultanément : +10%",
    "L'élément Lumière (<:light:887847410141921362>) permet d'entrevoir l'espoir là où les autres ne voit que les ombres.\nLes soins et armures de ces illuminés sont plus conséquents que ceux de leurs congénaires.\n\nSoins et armures : +10%",
    "L'élément Ténèbre (<:darkness:887847395067568128>) n'a pas son pareil pour exploiter les zones d'ombres de leurs adversaires.\nLes dégâts indirects de ces individues sont plus conséquents que ceux de leurs congénères.\n\nDégâts indirects : + 10%",
    "L'élément Astral (<:astral:907467653147410475>) utilise la puissance cosmique à son aventage. Car rien ne se perd, rien ne se créait, tout se transforme\n\n10% des dégâts reçu sont reconverties en <:astralShield:907467906483367936> Armure Astrale (après les dégâts)\n\n__<:astralShield:907467906483367936> Armure Astrale :__\nDurée infinie. Cette armure n'absorbe pas de dégâts supplémentaires lors de sa destruction",
    "L'élément Temporel (<:temporel:907467620930973707>) permet de prévoire les coups, car avoir une longueur d'avance est toujours bienvenue\n\n10% des soins et armures donnés à autruit vous sont restitués en temps qu'__<:tempoShield:907467936975945758> Armure Temporelle__ (La valeur des soins et armures n'est pas modifiée)\n\n__<:tempoShield:907467936975945758> Armure Temporelle :__\nDurée infinie. Cette armure n'absorbe pas de dégâts supplémentaires lors de sa destruction"
]
elemNames = ["Neutre","Feu","Eau","Air","Terre","Lumière","Ténèbre","Astral","Temporel"]


def uniqueEmoji(emoji):
    return [[emoji,emoji],[emoji,emoji],[emoji,emoji]]

def sameSpeciesEmoji(team1,team2):
    return [[team1,team2],[team1,team2],[team1,team2]]

dangerEm = sameSpeciesEmoji('<a:dangerB:898372745023336448>','<a:dangerR:898372723150041139>')
untargetableEmoji = uniqueEmoji('<:untargetable:899610264998125589>')
hourglassEmoji = [['<:hourglass1:872181651801772052>','<:hourglass2:872181632801603644>'],['<:hourglass1:872181651801772052>','<:hourglass2:872181632801603644>'],['<:hourglass1:872181651801772052>','<:hourglass2:872181632801603644>']]

# List of guild ids for the bots
ShushyCustomIcons = [881900244487516180]
LenaCustomIcons = [881632520830087218,881633183425253396]

stuffIconGuilds = [866782432997015613,878720670006132787,887756868787769434,887846876114739261,904164080204513331,908551466988486667,914608569284964392]
weaponIconGuilds = [866363139931242506,878720670006132787,887756868787769434,887846876114739261,916120008948600872]

# For some time related stuff. Time from server != time from France
if not(os.path.exists("../Kawi")):
    horaire = timedelta(hours=1)
else:
    horaire = timedelta(hours=0)
    
# Are we on the livebot or the test bot ?
isLenapy = not(os.path.exists("../Kawi"))

# Tabl of random messages for the shop
shopRandomMsg = [
    '<:lena:909047343876288552> : "Si j\'en crois la loi, je suis sensée vous rappeller que vous acceptez d\'utiliser vos armes à vos risques et périls.\nJe suis en aucun cas responsable si elle vous explose dans les mains et que vous la passez à gauche"',
    '<:lena:909047343876288552> : "Si quelqu\'un vois l\'autre fanatique des fleurs roses, vous pourrez lui dire qu\'il y en a une qui a poussée dans mon shop ?"',
    '<:lena:909047343876288552> : "Hônnetement, ça fait un moment que j\'ai arrêté de compter le nombre de canettes de Coca que me dois Léna"',
    '<:lena:909047343876288552> : "Des fleurs roses, blues, jaunes... Je dois vous rappeler que vous partez pas en mission jardinage ?"',
    "<:lena:909047343876288552> : \"Faites attention si Alice vous rejoint pour un combat. Il est fort probable qu'elle cherche à obtenir des infos sur vous plutôt que de vaincre vos ennemis\"",
    "<:alice:908902054959939664> : \"J'aime bien les vêtements que tu proposes, mais ça manque de rose...\"\n<:lena:909047343876288552> : \"C'est une blague j'espère\"",
    "<:ikaBlue:866459319049650206> : `Sit down and eat pop-corns`",
    "<:ikaBlue:866459319049650206> : `Sit down and eat pop-corns`\n<:shushi:909047653524963328> : `Regarde les pop-corns avec un air interresée`",
    "<:ikaPink:866459344173137930> : \"Flum POWA !\"",
    "<:ikaPink:866459344173137930> : \"Flum POWA !\"\n<:clemence:908902579554111549> : \"Les coquelicots c'est mieux je trouve\"\n<:alice:908902054959939664> : \"N'importe quoi ! Ce sont les roses les plus jolies !\"\n<:lena:909047343876288552> : \"Vous trois, vous pourriez arrêter de débattre dans mon shop, s'il vous plait ?\"",
    "<:lena:909047343876288552> : \"Tiens, Clémence, j'ai trouvé un drôle de livre ces derniers temps et vu que tu t'y connais un peu en runes et magie, je me demandais si tu pouvais essayer de m'apprendre un peu comment m'en servir...\"\n<:clemence:908902579554111549> : \"Heu... ok\"",
    "<:clemence:908902579554111549> : \"Ah, Lena. J'ai jeté un coup d'œil à ton livre et heu... Tu as au moins une idée de ce qu'est un Carbuncle ?\"\n<:lena:909047343876288552> : \"Absolument pas\"\n<:clemence:908902579554111549> : \"... Ça va être long...\"",
    '<:lena:909047343876288552> : "Si quelqu\'un vois Ly, vous pourrez lui dire que ma proposition tiens toujours ?"',
    '<:clemence:908902579554111549> : "Hum... j\'ai trouvé des trucs qui pourrait t\'interresser lors de ma dernière escapade dans les ruines d\'Elidyn, Lena"\n<:lena:909047343876288552> : "Ow ? Montre pour voir ?"',
    '<:luna:909047362868105227> : "On a tous une part sombre en nous. Si vous voulez je peux vous aider à la trouver"',
    '<:shihu:909047672541945927> : "Ti miman a un pobem"\n<:shushi:909047653524963328> : "Gomment za ?"\n<:shihu:909047672541945927> : "Mi miman commenze a en awoir marre de fire la zentille fifille"\n<:shushi:909047653524963328> : "..."',
    '<:alice:908902054959939664> : "Mooow tu sais que tu es trop mignone toi ?"\n<:shushi:909047653524963328> : "Heu... gwa ?"',
    '<:clemence:908902579554111549> : "Je me doute déjà de la réponse mais... Alice, pourquoi tu es quasiment toujours là où se trouve Hélène en ce moment ?"\n<:alice:908902054959939664> : "... Pour rien ^^"\n<:clemence:908902579554111549> : "Je suis pas vraiment convaincue..."',
    '<:shihu:909047672541945927> : "Ti en penze gwa de zette coupe de tentacule ?"\n<:shushi:909047653524963328> : "Hum... Pas viment convaincue..."\n<:shihu:909047672541945927> : "Oh..."\n<:shushi:909047653524963328> : "Mi apès, ze peux touzour en fire un queue de zeval regawde !\n<:shihu:909047672541945927> : :0',
    '<:felicite:899695897900879902> : "Hé Clémence ! Je peux t\'accompagner pour ta prochaine aventure ? Je te promet que je te gênerais pas !"\n<:clemence:908902579554111549> : "Alala... Soit"\n<:felicite:899695897900879902> : :D',
    '<:akira:909048455828238347> : ...\n<:shihu:909047672541945927> : ...\n<:akira:909048455828238347> <:shihu:909047672541945927> : ^^\n\n<:lena:909047343876288552> : <:LenaWhat:760884455727955978>',
    '<:lena:909047343876288552> : "\"Fini de jouer\" ? Tu as pas mieux comme phrase d\'accroche ?"\n<:luna:909047362868105227> : "Est-ce que je critique tes \"It\'s now or never\" moi ?"\n<:lena:909047343876288552> : "Roh, je suis sûre que tu l\'aime bien aussi cette chanson"\n<:luna:909047362868105227> : "Tss. Uniquement l\'originale."',
    '<:helene:906303162854543390> : "Tu es au courant que mourir par hémorragie est tout sauf une mort agréable hein ?"\n<:shehisa:901555930066473000> : "Je vois pas où est la différence avec les infections que tu donnes à tes adversaires. Je suis peut-être pas une soigneuse, mais Papa m\'a suffisament initiée pour savoir que les maladies que tu leur refile sont tous sauf agréable"',
    '<:shehisa:901555930066473000> : "Tu me reproche d\'avoir suivi la voie de Maman, mais tu devrais voir comment tu te comporte face à un ennemi quand tu veux lui faire avaler la pilule"\n<:helene:906303162854543390> : "Qu\'est-ce que tu insinue par là ?"\n<:shehisa:901555930066473000> : "Que je suis pas la seule à avoir héritée des talents de Maman"',
    '<:shehisa:901555930066473000> : "Toujours rassurant de te savoir dans les parages, Icealia"\n<:icealia:909065559516250112> : "Oh, je n\'arrive pas au niveau de ta soeur en terme de soutiens quand même..."',
    '<:shehisa:901555930066473000> : "Toujours rassurant de te savoir dans les parages, Icealia"\n<:icealia:909065559516250112> : "Et moi je suis toujours rasurée de te savoir dans mon camp..."',
    '<:determination:867894180851482644> : "Laisse tomber Lena. De toutes façons il me considre même pas comme un de ses OCs"\n<:lena:909047343876288552> : "Tu vas pas rester dans le retrait et dans l\'oublie quand même ! Tu es presque aussi vielle que moi !"\n<:determination:867894180851482644> : "Undertale est plus vieux que toi"\n<:lena:909047343876288552> : "Si tu veux jouer à qui a la plus grosse je pense que je t\'explose"\n<:determination:867894180851482644> : "Oh ça dépend de la catégorie. En combat, tu m\'as jamais vaincue"\n<:luna:909047362868105227> : "Mais moi si"',
    'Les anges c\'est surc-\n<:lena:909047343876288552> : .',
    '<:determination:867894180851482644> : "Alors Féli, tu as fais des progrès sur ta maitrise de la Détermination ?"\n<:felicite:899695897900879902> : "Ouais :D ! Regarde ça !"',
    '<:takoRed:866459004439756810> : "Clémence, ça va mieux avec ta cicatrice en ce moment ?"\n<:clemence:908902579554111549> : "À part qu\'elle me brûle quand j\'utilise trop mes pouvoirs vampiriques ou quand il y a un Alpha dans le coin, rien à déclarer"\n<:takoRed:866459004439756810> : "Tss. Ces loups garoux..."\n<:clemence:908902579554111549> : "Pas la peine de prendre ce regard assassin Madame Ruby. J\'ai appris à faire avec maintenant"',
    '`Alice surgit au coins du couloir en courant et vous rentre dedans, ne vous ayant pas vu`\n\n<:alice:908902054959939664> : "Dé-désolée !"\n\n`Elle ramasse rapidement les cahiers qu\'elle portait dans ses bras et repart aussi vite qu\'elle est venue.\nVous constatez qu\'elle a oublié une feuille, qui a du se retrouver sous elle quand elle est tombée`\n\n📄 [Devoir d\'astronomie sur les trous noirs](https://bit.ly/3kh8xP3)',
    '<:alice:908902054959939664> : "Maraiiiiiiiiine ?"\n<:lena:909047343876288552> : "Il y a un peu trop de "i" pour moi..."\n<:alice:908902054959939664> : "C\'est quoi ça."\n\n`Elle sortie son téléphone et le mit directement devant le visage de Lena`\n\n📱 [Photographie d\'une feuille de papier](https://bit.ly/3o74aal)\n\n<:lena:909047343876288552> : "... Merde. Et comment ça, tu es allé fouiller dans ma chambre !?"',
    '<:alice:908902054959939664> : "Altyyy ?"\n<:alty:906303048542990347> : "Hum ^^ ?"\n<:alice:908902054959939664> : "Tu peux m\'apprend à faire des begnets de calamars (ᵔ◡ᵔ) ?"\n<:alty:906303048542990347> : "Heu... ok mais seulement si c\'est moi qui apporte le calamar ^^\'"\n<:alice:908902054959939664> : "Bah pourquoi tu dis ça (o^ ^o) ?"\n<:shushi:909047653524963328> : "Quiqu\'un awais vu Miman ?"',
    '<:lena:909047343876288552> : "Tu sais que tu va finir par traumatiser des gens avec tes \"Boum boum\" toi ?"\n<:shihu:909047672541945927> : "Mi z\'est drole les Boum Boum..."',
    '<:clemence:908902579554111549> : "Hé Powehi, je me suis retrouvée avec plein de Rotten Flesh lors de ma dernière expédition, tu veux que je te les passes ?"\n<:powehi:909048473666596905> : "Oh que oui !"',
    '<:gweny:906303014665617478> : "Toujours à regarder les étoiles ?"\n<:powehi:909048473666596905> : "J\'ai une question Gwendoline... Tu réagirais comment si tu étais bloquée dans ce monde après ta mort et ne pouvais que regarder les autres être vivant te fuir dès que tu t\'approches trop d\'eux ?"\n<:gweny:906303014665617478> : "Oh heu... Je sais pas vraiment désolée. Compliqué de se mettre à ta place, j\'en ai bien peur"\n<:powehi:909048473666596905> : "C\'est pas grave, merci quand même..."',
    '`En entrant dans une pièce présumée vide, vous êtes surpris de voir des reflets lumineux dans un coin. En allant l\'examiner, vous découvrez Shushi et Sixtine qui dorment l\'une contre l\'autre. Au sol se trouve un lecteur de musique`\n\n📱 [Liste de musique en file d\'attente](https://bit.ly/3D6Ltdh)',
    "<:lena:909047343876288552> : \"Qu'est-ce que l'EEv3 ? J'aurais peut-être dû te dire ça avant de t'envoyer taper les octariens à tout bout de champ...\"\n\n`Elle s'adossa à un mur, en réfléchissant à comment elle pourrait expliquer ça sans dépasser la limite de caractère`\n\n<:lena:909047343876288552> : \"Pour commencer, l'Escadron Espadon (premier du nom) était le nom de l'armée de mon peuple, les Inklings, lors de la Grande Guerre de Territoire. Déjà si tu en est arrivé à là j'en déduis que tu es pas Flora. Je te passe les détails, mais on l'a gagné.\nUn siècle plus tard, les Octariens ont relancé une offensive contre Chromapolis, mais qui fût repoussé par l'Escadron Espadon Nouvelle Version, nouvellement reformé à l'occasion. Oh ça n'a pas empêché les Octariens de lancer d'autres offensives, et c'est au cours de l'une d'elle que j'ai rejoins les rangs.\n\nLe temps à passé, et au final je me suis retrouvé à la tête de l'Escadron. C'est à ce moment là que j'ai décidé d'en faire une société un peu moins secrète et fait batir ce QG tout en changeant le nom de l'Escadron une nouvelle fois pour Escadron Espadon 3e Version.\nNotre role premier consiste évidamment à protéger Chromapolis contre les agressions, mais ces derniers temps, plusieurs failles dimentionnels sont apparues menacent la notre.\n\nC'est là que tu rentre en jeu {0}. Ouais bon, je vais continuer de t'appeller {1} enfaite. Plus court. Donc bref, comme tu peux t'en douter, tu, et ton équipe, viens de l'une de ses failles des dimensions de l'imaginaire et avec votre aide j'aimerais bien tirer au clair toute cette histoire. Comme tu aura pu le remarquer, les Octariens aussi ont saisi cette occasion pour renforcer leurs rangs, et poussent leurs assauts à un autre niveau que précédamment, mais tant que les équipes d'interventions comme vous seront là, j'ai pas vraiment de soucis à me faire.\"",
    "<:lena:909047343876288552> : \"La plupart des armes que tu trouveras dans cet arsenal viennent de d'autres dimensions tu t'en doute. Mais elles ont toutes été vérifiées par notre expert qui les as toutes certifiées avec un \"Dans les conditions normales d'utilisation, sans danger pour l'utilisateur\". Va savoir ce qui se passe dans des conditions anormales, par contre.\"",
    "<:lena:909047343876288552> : \"À quoi sert mon équipe des \"Temp's\" ? Basiquement on remplie la tienne si elle contient pas assez de membre pour partir en mission, mais de temps en temps on organise des combats d'entrainement contre des équipes d'intervention, histoire de tester des armes et compétences. Et puis ça vous change de vos adversaires habituels.\"",
    "<:john:908887592756449311> : \"A-Alice, toi qui la connais bien tu... saurais ce que je pourrais faire pour... qu'elle me voit comme autre chose qu'un... ami ?\"\n<:alice:908902054959939664> : \"Commence par être un peu plus sûr de toi. Là, elle continue de voir le louvetau naïf qui essayait de se coucher à ses pieds au lieu de fuir\"\n<:john:908887592756449311> : \"Mais je-\"\n<:alice:908902054959939664> : \"Passe ton temps avec elle sous ta forme de loup à être couché à ses pieds. Si tu veux qu'elle te vois comme autre chose qu'un chien de compagnie, va falloir que tu arrête de te comporter tel quel.\"",
    "<:lio:908754690769043546> : \"H-hm !? Oh c'est toi...\"\n<:felicite:909048027644317706> : \"Tiens tu es là toi aussi ?\"\n<:lio:908754690769043546> : \"J'ai pas trouvé d'autres points d'eau dans le coin donc oui... je suppose...\"",
    "<:gweny:906303014665617478> : \"Eh bien... On... fatigue déjà... Liu... ?\"\n<:liu:908754674449018890> : \"Cer... Certainement pas... Je... pourrais courir... comme ça... pendant encore des kilomètres...\"",
    "<:lia:908754741226520656> : \"Hé Alice ! Tu penses quoi de ces fleurs là ?\"\n<:alice:908902054959939664> : \"Hum... un peu trop jaune à mon goût...\"",
    "<:shushi:909047653524963328> : \"Hé hé Midame des neizes ! Z'est touvé za part terre, y a maqué quoi dezu ?\"\n<:icealia:909065559516250112> : \"Montre moi pour voir ^^ ?\"\n\n📃 [Page de papier à l'encre rose](https://bit.ly/3DgXk8v)",
    "<:lena:909047343876288552> : \"...\"\n<:luna:909047362868105227> : \"Tu commencerais pas à nous faire une crise de jalousie toi ?\"<:lena:909047343876288552> : \"Je vois pas de quoi tu parles.\"\n<:luna:909047362868105227> : \"J'en pris, je suis mieux placée que qui-conque pour voir comment tu regardes Clémence depuis qu'elle a sa version boss\"\n<:lena:909047343876288552> : \"...\"\n<:luna:909047362868105227> : \"En même temps tu passes ton temps à lui montrer que tu peux te débrouiller toute seule, tu vas pas lui reprocher de s'occuper de ses autres OCs de temps en temps, si ?\"<:lena:909047343876288552> : \"Non évidament...\""
]

shopRepatition = [4,7,10,2]                 # Répartition des objets du shop

# Same, but for the roll command
rollMessage = ["Selon toute vraisemblance ce sera un **{0}**","Puisse la chance être avec toi... **{0}** !","Alors Alice tu as obtenu combien ? **{0}** ? **{0}** alors","Sur 100, les chances que la relation Akrisk tienne debout ? Hum... **{0}**","Le nombre de lances que tu va avoir à esquiver est... **{0}**"]

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

class says:
    """A class for storing the says message from a entity"""
    def __init__(self,start=None,ultimate=None,limiteBreak=None,onKill=None,onDeath=None,onResurect=None,blueWinAlive=None,blueWinDead=None,blueLoose=None,redWinAlive=None,redWinDead=None,redLoose=None):
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
            self.redLoose
            ]

    def fromTabl(self,tabl : list):
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

        return self

lenaSays = says(
    start= "Ok, voyons voir ce que vous avez dans le ventre",
    ultimate= "Qu'est-ce que vous dîtes de ça ?",
    limiteBreak= "It's now or never !",
    onDeath= "Tps.",
    onResurect= "J'te revaudrais ça",
    blueWinAlive= "Une victoire en bonne uniforme",
    redWinAlive= "Vous avez encore des progrès à faire",
    redWinDead="Pas mal. Mais pas suffisant",
    redLoose="Vous commencez à bien vous débrouiller"
)

aliceSays = says(
    start= "Ok, je vais faire de mon mieux, vous allez voir ☆⌒(ゝ。∂) !",
    onDeath="Kya ☆⌒(>。<) !",
    redWinAlive="Viii (≧▽≦) !",
    redWinDead="｡･ﾟ(ﾟ><ﾟ)ﾟ･｡",
    blueWinAlive="Alors, vous en avez dit quoi (≧▽≦) ?",
    onKill = "J'aime pas la méthode direct (〃▽〃)...",
    onResurect= "Prête pour le rappel ☆⌒(ゝ。∂)!"
)

clemSays = says(
    start = "Parée !",
    ultimate = "Ok, c'est parti !",
    onDeath = "Je t'ai sous estimé manifestement...",
    onResurect = "Merci du coup de main !",
    redWinAlive = "Et bah alors, on abandonne déjà ?",
    blueWinAlive = "Simple. Basique."
)

ailillSays = says(
    start="Tss, encore toi ?",
    onKill="Déjà cassé ?",
    onDeath="Tu... payes rien pour attendre...",
    redWinAlive="Vous appelez ça un combat ?"
)

jevilSays = says(
    start="Let's play a number game ! If you're HP drop to 0, I win !",
    onDeath="THIS BODY CANNOT BE KILLED !",
    redWinAlive="SUCH FUN !",
    redLoose="Such fun ! I'm exausted !"
)

lunaBossSays = says(
    start="`Soupir` Je pensais pas te voir parmis eux, Shihu",
    onKill="Laisse les Ténèbres de ton âme prendre le dessus",
    redWinAlive="Je vous souhaite une bonne nuit. Une nuit éternelle !",
    redLoose="Tsp. Vous ne faites que repousser l'inévitable"
)

shushiAltSays = says(
    start="Dézolé Miman... Mais on peut pa ti laizer fire.",
    onKill="Zi te plait...",
    onDeath="D-Dézolée !",
    blueLoose="Ze ferais miheu... la prozaine fois...",
    blueWinAlive="Wiiii !"
)

shushiSays = says(
    start="Ze te rendrais fi-ère Miman !",
    ultimate="Mintenant !",
    onKill="Purgwa y bouze pu ?",
    onDeath="Miman !",
    onResurect="Ze veux encore dodo...",
    blueWinAlive="On a réuzi ?",
    blueWinDead="Bien zoué !",
    blueLoose="Ze vais dewoir fire mieux la pozaine fois !",
    redWinAlive="Alors alors ?",
    redWinDead="Pi mieux fire !",
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
    start="Ti le regetera pas, Zuzi !",
    redWinAlive="Boum Boum"
)

temSays = says(
    start="HoIIII !",
    onDeath="Ayayaya !"
)

spamtonSays = says(
    start="HEY EVERY       ! IT'S ME, SPAMTON G. SPAMTON!",
    redWinAlive="DON'T FORGET TO [[Like and Subscribe](https://gfycat.com/fr/gifs/search/youtube+subscribe+button+green+screen)] FOR MORE [[Hyperlink Blocked]]!",
    redLoose="THIS IS [[One Purchase](https://www.m6boutique.com/?adlgid=c|g||383715070314|b&gclid=Cj0KCQjwlOmLBhCHARIsAGiJg7lgxkpj8jJSOEZZ_q1URCeEWFW_SmyGcVeiKz8wUmO0-LCAE9Sz4SsaAgsvEALw_wcB)] YOU WILL [[Regret](https://www.youtube.com/watch?v=u617RilV5wU)] FOR THE REST OF YOUR LIFE!",
    onKill="HOW'S AN INNOCENT GUY LIKE ME SUPPOSED TO [[Rip People Off](https://www.youtube.com/watch?v=nIxMX6uyuAI)] WHEN KIDS LIKE YOU ARE [[Beating People Up](https://www.youtube.com/watch?v=4c_eEd-ReiY)],"
)

powehiSays = says(
    start="Un nouveau cycle commence...",
    limiteBreak="Qui vous a dit que je vous laisserais faire ?",
    onDeath="Kya !",
    onResurect="Mourir, c'est toujours pas drôle"
)

randomWaitingMsg = [
    "<a:bastuno:720237296322084905> Baston inkoming !",
    "<a:explosion:882627170944573471> Simulation de l'anéantissement à venir...",
    "<:invisible:899788326691823656> Erreur 404 : Blague non trouvée",
    "<:alice:908902054959939664> \"Conseil gratuit : Les OctoBooms font mal\"",
    "<a:giveup:902383022354079814>",
    "<a:Braum:760825014836002826> I am faster than you~"
]

johnSays = says(
    start = "(Courage John. Montre lui que tu as appris à devenir un combattant.)"
)

liaSays = says(
    start="Ça vous dirait de danser avec moi ?",
    onKill = "Oh déjà... ?",
    onDeath = "Hii ! Compris compris !",
    redWinAlive = "C'était marrant !",
    redLoose = "Vous savez pas rire..."
)

liuSays = says(
    start = "Hé ! Une course d'endurance vous en pensez quoi ?",
    onKill = "Va falloir mieux gérer ta fatigue la prochaine fois",
    onResurect = "Une seconde course ?",
    redLoose = "Hé bah... Finalement c'est moi qui ai mordu la poussière"
)

lioSays = says(
    start = "Oh... Heu... Bonjour...",
    onKill = "J- J'y suis allé trop fort ?",
    onResurect = "Merci...",
    onDeath= "Humf ! J'aurais du rester dans la forêt...",
    redWinAlive= "Le monde des humains est... perturbant..."
)

lizSays = says(
    start = "Tiens donc, des nouvelles braises",
    ultimate = "Allez quoi, déclarez moi votre flamme !",
    onKill = "Woops, j'y suis allé trop fort manifestement",
    onDeath = "Pff, vous êtes pas drôle",
    redLoose = "Waw, je me suis jamais faite autant refroidir rapidement..."
)

randomMaxDmg = [
    "Apparament, {icon} __{name}__ aurait réussi à infligé **{value}** dégâts en un seul combat ╮(︶▽︶)╭",
    "Hé tu sais quoi {icon} __{name}__ ? Ton record de dégâts en un seul combat est de **{value}**",
    "Hum... le record de dégâts de {icon} __{name}__ est que de **{value}** ?"
]

randomTotalDmg = [
    "Hé {icon} __{name}__ ! Tu veux savoir combien de dégâts tu as fait au total ? **{value}**",
    "Aufaite Lena, tu voulais savoir combien de dégâts a fait {icon} __{name}__ au total ? **{value}**",
    "Tu veux savoir combien de dégâts tu as fait {icon} __{name}__ ? Hum... **{value}** ╮(︶▽︶)╭"
]

randomMaxHeal = [
    "Alors voyons voir si {icon} __{name}__ est un bon healer... Son record de soins est de **{value}**",
    "Au maximum, tu as soigné **{value}** PV en un combat {icon} __{name}__",
    "Apparament, le record personnel de soins de {icon} __{name}__ est de **{value}**, ni plus ni moins ╮(︶▽︶)╭"
]

randomTotalHeal = [
    "Au total, tu as soigné **{value}** PV {icon} __{name}__",
    "Tu as réussi à annuler **{value}** dégâts subis par tes alliés {icon} __{name}__, c'est pas trop mal (〃▽〃)! ",
    "Si j'en crois mes observations, {icon} __{name}__ aurait soigné un total de **{value}** PV... J'ai du mal regarder (ᓀ ᓀ)"
]

randomMaxRes = [
    "En un seul combat, {icon} __{name}__ a réussi à ressuciter jusqu'à **{value}** alliés, quel ange gardien (ᓀ ᓀ)",
    "La mort c'est surcôté tu trouves pas {icon} __{name}__ ^^ ? Tu as ressucité jusqu'à **{value}** alliés en un seul combat"
]

randomTotalRes = [
    "La mort c'est juste une mauvaise grippe ☆⌒(ゝ。∂). Que {icon} __{name}__ a soigné **{value}** fois",
    "(－.－)…zzz {icon} __{name}__... résu... **{value}** fois..."
]

randomMaxTank = [
    "Hé bah ! {icon} __{name}__ a subis un maximum de **{value}** dégâts en un combat ? J'espère que ses supports ont suivi (〃▽〃)",
    "Hé bah ! {icon} __{name}__ a subis un maximum de **{value}** dégâts en un combat ? Ça doit être son kiff je présume (¯.¯;) ..."
]

randomTotalTank = [
    "Tiens donc ? {icon} __{name}__ aurait subi un total de **{value}** ? Ça fait pas mal quand même, je plaind ses soutiens (￣ ￣|||)",
    "{icon} __{name}__, tu serais pas un peu mazo par hasard (￣ ￣|||) ? Tu es quand même à **{value}** dégâts totaux subis là..."
]

randomMaxArmor = [
    "L'important c'est de savoir quand utiliser ses capacités ☆⌒(ゝ。∂).\nRegardez {icon} __{name}__ : Son record d'armure donnée est à **{value}**",
    "Je suis plus partisante du \"Ils peuvent pas nous taper si ils sont morts\", mais bon au cas où je pourrais compter sur {icon} __{name}__.\nSon record d'armure donnée est à **{value}** ╮(︶▽︶)╭"
]

randomTotalArmor = [
    "Il semblerais que {icon} __{name}__ préfère prévenir que guérir... Son total d'armure donné s'élève à **{value}**",
    "Le total d'armure donnée par {icon} __{name}__ s'élève à **{value}**, sans plus ni moins ╮(︶▽︶)╭",
    "Hé bah ! On peut dire que {icon} __{name}__ s'y connais en armure. Il en a donné **{value}** points jusqu'à présent"
]

randomMaxKill = [
    "{icon} __{name}__ est une veritable terreur avec son record personnel de **{value}** éliminations en un combat (･_├┬┴┬┴",
    "Va falloir que je me souvienne d'être particulirement prudente avec {icon} __{name}__ ( . .)φ...\nSon record d'élimination est de **{value}**..."
]

randomTotalKill = [
    "Le nombre de victimes de {icon} __{name}__ est de **{value}**.\n\nNon j'ai pas de commentaire à faire (＃￣0￣)",
    "Le nombre de victimes de {icon} __{name}__ est de **{value}**."
    "Si j'ai bien compté, le nombre total d'élimiation par {icon} __{name}__ est à **{value}** (ᓀ ᓀ)\nFaites ce que vous voulez de cette information"
]

randomRecordMsg = [
    "C'est cependant loin du record qui est de **{value}**, détenu par {icon} __{name}__",
    "Va falloir mieux faire si tu veux dépasser {icon} __{name}__, le sien est à **{value}** ☆⌒(ゝ。∂)",
    "Allez courage ! {icon} __{name}__ n'est qu'à **{value}** (^.~)☆",
    "Si tu veux viser les étoiles, sache que {icon} __{name}__ est à **{value}** ┐( ˘ ､ ˘ )┌"
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
    "On ne ménage pas ses efforts à ce que je vois {icon} __{name}__ ! En un combat, tu as réussi à obtenir un maximum de **{value}** points de Soutien",
    "Taper c'est bien beau, mais sans {icon} __{name}__, vous n'auriez pas tapé énormément. Son record de Soutien est de **{value}**"
]

clemPosSays = says(
    start = "Encore des chasseurs de vamires ? J'en ai ma claque des gens de votre genre.",
    onKill = "Un de plus, un de moins. Quelle importance",
    redWinAlive = "Restez à votre place.",
    redLoose = "Que..."
)

aliceExSays = says(
    start = "Clémence...",
    onKill = "...",
    onResurect= "Merci...",
    blueWinAlive= "ça... ça va mieux ?"
)

def createTpmChangeDict(level : int, changeWhat : int, change : list, to : list, proba = 100):
    """ChangeWhat : 0 == skills"""
    if len(change) != len(to):
        raise AttributeError("Change list and To list don't have the same length")
    if proba > 100:
        raise AttributeError("Proba > 100")
    elif proba < 1:
        raise AttributeError("Proba < 1")

    return {"level":level,"changeWhat":changeWhat,"change":change,"to":to,"proba":proba}
