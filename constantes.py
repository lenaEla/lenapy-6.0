"""
Constants module.
Here stand the first brick of the bot
"""
from datetime import timedelta, datetime
import os
from sre_constants import IN
from index import *
from discord_slash.utils.manage_components import *

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

areaNames = ["Monocible", "Cercle de rayon 1", "Cercle de rayon 2", "Cercle de rayon 3", "Cercle de rayon 4", "Cercle de rayon 5", "Cercle de rayon 6", "Cercle de rayon 7", "Tous les alliés", "Tous les ennemis", "Tous les combattants", "Cone simple", "Cone Large", "Cone Large", "Cone Large", "Cone Large", "Cone Large", "Ligne de 2 de longueur", "Ligne de 3 de longueur", "Ligne de 4 de longueur", "Ligne de 5 de longueur", "Ligne de 6 de longueur", "Donut de 1 de rayon", "Donut de 2 de rayon", "Donut de 3 de rayon", "Donut de 4 de rayon",
             "Donut de 5 de rayon", "Donut de 6 de rayon", "Donut de 7 de rayon", "Anneau Distance de 1 de largeur", "Anneau Distance de 2 de largeur", "Anneau Distance de 3 de largeur", "Anneau Distance de 4 de largeur", "Anneau Distance de 5 de largeur", "Arc de Cercle de 1 de rayon", "Arc de Cercle de 2 de rayon", "Arc de Cercle de 3 de rayon", "1 ennemi aléatoire", "2 ennemis aléatoires", "3 ennemis aléatoires", "4 ennemis aléatoires", "5 ennemis aléatoires", "Croix de 2 cases", "Croix de 3 cases", "Croix de 4 cases", "Crois de 5 cases"]
allArea = range(0, 46)

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

allTriggers = [TRIGGER_PASSIVE, TRIGGER_DAMAGE, TRIGGER_END_OF_TURN, TRIGGER_DEATH,
               TRIGGER_DEALS_DAMAGE, TRIGGER_INSTANT, TRIGGER_START_OF_TURN, TRIGGER_ON_REMOVE, TRIGGER_AFTER_DAMAGE]

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

tablTypeStr = ["Armure", "Dégâts indirects", "Soins Indirects", "Résurection indirecte",
               "Boost", "Resurection", "Dégâts", "Malus", "Soins", "Unique", "Invocation", "Passif"]
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


AUTO_POWER = "autoPower"
nameStats, nameStats2 = ["Force", "Endurance", "Charisme", "Agilité","Précision", "Intelligence", "Magie"], ["Résistance", "Pénétration", "Critique"]
allStatsNames = nameStats+nameStats2

# Status for entities
STATUS_ALIVE, STATUS_DEAD, STATUS_RESURECTED, STATUS_TRUE_DEATH = 0, 1, 2, 3

# Aspirations
BERSERK, OBSERVATEUR, POIDS_PLUME, IDOLE, PREVOYANT, TETE_BRULE, MAGE, ALTRUISTE, ENCHANTEUR, PROTECTEUR, VIGILANT, SORCELER, INOVATEUR, ATTENTIF, ASPI_NEUTRAL = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14
inspi = ["Berserkeur", "Observateur", "Poids plume", "Idole", "Prévoyant", "Tête brulée", "Mage","Altruiste", "Enchanteur", "Protecteur", "Vigilant", "Sorcier", "Inovateur", "Attentif", "Neutre"]
aspiEmoji = ['<:berk:915376153580167209>', '<:obs:903136012975357952>', '<:poi:909548928045842462>', '<:ido:909549029027880992>', '<:pre:910185501535903775>', '<:tet:903136049834889317>','<:mag:909549699160219659>', '<:alt:909549006680653824>', '<:enc:903136097553506314>', '<:pro:909549059059122176>', '<:vigil:939209910019829810>', '<:sorc:939209891510378598>']
lbNames = ["Lames de l'Ombre","Laser Ultra-Nucléïque","Poussé du Mystral Gagnat","Apothéose planétaire","Armure Galactique","Fracture Dimentionnelle","Colère de Nacialisla","Don de Vie","Zone Magiconucléïque","Pousée d'Espoir","Résiliance Infernale","Cataclysme Céleste","Avenir Prometeur","Tir Ultime"]
lbDesc = ["Inflige des dégâts à l'ennemi ciblé et vous soigne d'une partie des dégâts infligés","Inflige des dégâts monocibles en direction de l'ennemi ciblé et augmente temporairement vos statistiques","Inflige des dégâts à l'ennemi ciblé et le repousse violament","Augmente les statistiques des alliés pendant un certain temps et réanime ceux qui sont vaincus","Donne un grand montant d'armure aux alliés à portée et augmente temporairement leurs statistiques offensives","Inflige des dégâts à l'ennemi ciblé et réduit ses PV max d'une partie des dégâts infligés","Inflige d'importants dégâts dans une large zone autour de l'ennemi ciblé","Soigne les alliés à portée et leur donne un effet de régénération tout en réanimant ceux qui étaient vaincus","Inflige des dégâts dans une large zone autour de l'ennemi ciblé et vous octroit une armure","Donne une importante armure aux alliés à portée et augmente temporairement leurs statistiques défensives","Soigne les alliés à portée et réanime puissament les alliés vaincus qu'importe leur position","Inflige des dégâts dans une large zone autour de l'ennemi ciblé et lui octroit un effet de dégâts indirects multi-cibles supplémentaire","Augmente les statistiques des alliés à portée durant un certain temps et réduit leurs dégâts subis pendant la même durée","Inflige des dégâts en ligne droite sur l'ennemi ciblé et augmente temporairement vos statistiques"]
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
    [STRENGTH, PRECISION],
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
    [STRENGTH, PRECISION, CRITICAL],
    [STRENGTH, MAGIE, ACT_DIRECT_FULL]
]


while len(aspiEmoji) < len(inspi):
    aspiEmoji.append('<a:menacing:917007335220711434>')

BERS_LIFE_STEAL = 20

# "Target" values
ALL, TEAM1, TEAM2, ALLIES, ENNEMIS = 0, 1, 2, 3, 4

# Selected options for fight
OPTION_WEAPON, OPTION_SKILL, OPTION_MOVE, OPTION_SKIP = 0, 1, 2, 3

# Genders. 2 for default
GENDER_MALE, GENDER_FEMALE, GENDER_OTHER = 0, 1, 2

# Color constants
red, light_blue, yellow, green, blue, purple, pink, orange, white, black, aliceColor = 0xED0000, 0x94d4e4, 0xFCED12, 0x1ED311, 0x0035E4, 0x6100E4, 0xFB2DDB, 0xEF7C00, 0xffffff, 0x000000, 0xffc3ff
colorId = [red, orange, yellow, green,
           light_blue, blue, purple, pink, white, black]
colorChoice = ["Rouge", "Orange", "Jaune", "Vert",
               "Bleu Clair", "Bleu", "Violet", "Rose", "Blanc", "Noir"]

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

# Constants for "orientation" field for skills
TANK, DISTANCE, LONG_DIST = "Tank", "Distance", "Longue Distance"
DPT_PHYS, HEALER, BOOSTER, DPT_MAGIC, SHIELDER = "Bers, Obs, P.Plu, T.Bru", "Ido, Pro, Alt", "Ido, Pro", "Enc, Mag", "Ido, Pro, Pre"

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
ELEMENT_UNIVERSALIS_PREMO = 9

elemEmojis = ["<:neutral:921127224596385802>", "<:fire:918212781168275456>", "<:water:918212797320536124>", "<:air:918592529480446002>", "<:earth:918212824805801984>",
              "<:light:918212861757653053>", "<:darkness:918212877419175946>", '<:space:918212897967075329>', '<:time:918212912408051814>', "<:univ:936302039456165898>"]
secElemEmojis = ["<:empty:866459463568850954>", "<:secFeu:932941340612894760>", "<:secEau:932941360858820618>", "<:secAir:932941299559063573>",
                 "<:secTerre:932941317804273734>", "<:secLum:932941251597201438>", "<:secTen:932941234501222410>", "<:secTempo:932941280785338389>", "<:secAst:932941221331075092>"]
elemDesc = [
    "L'élément Neutre ({0}) est l'élément le plus apprécié des nouvelles recrues.\nSans spécialisations particulière, cet élément permet de tout faire sans trop se casser la tête".format(
        elemEmojis[0]),
    "L'élément Feu ({0}) est en général préféré par ceux qui aiment tirer sans distinction et faire carnage sans pareil.\nLes dissicles de l'élément Feu infligent un peu plus de dégâts avec les armes et capacité de zone en distance.".format(
        elemEmojis[1]),
    "L'élément Eau ({0}) est plus propice à la concentration et la sérénité.\nLes adeptes de cet élément inflige plus de dégâts avec les armes ou capacités monocible à distance.".format(
        elemEmojis[2]),
    "L'élément Air ({0}) a pour réputation d'être assez capricieu et imprévisible.\nC'est pour cela que ses partisants filent tel le vent pour frapper plusieurs ennemis simultanément.".format(
        elemEmojis[3]),
    "L'élément Terre ({0}) permet de ressentir la puissance des courants d'énergie télurique et d'en tirer le meilleur parti.\nLes habitués de cet élément infligent des dégâts monocibles en mêlée plus conséquents.".format(
        elemEmojis[4]),
    "L'élément Lumière ({0}) permet d'entrevoir l'espoir là où les autres ne voit que les ombres.\nLes soins et armures de ces illuminés sont plus conséquents que ceux de leurs congénaires.".format(
        elemEmojis[5]),
    "L'élément Ténèbre ({0}) n'a pas son pareil pour exploiter les zones d'ombres de leurs adversaires.\nLes dégâts indirects de ces individues sont plus conséquents que ceux de leurs congénères.".format(
        elemEmojis[6]),
    "L'élément Astral ({0}) utilise la puissance cosmique à son aventage. Car rien ne se perd, rien ne se créait, tout se transforme.".format(
        elemEmojis[7]),
    "L'élément Temporel ({0}) permet de prévoire les coups, car avoir une longueur d'avance est toujours bienvenue.".format(
        elemEmojis[8])
]
elemNames = ["Neutre", "Feu", "Eau", "Air", "Terre", "Lumière",
             "Ténèbre", "Astral", "Temporel", "Universalis Premera"]

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
AOEDAMAGEREDUCTION = 0.35
AOEMINDAMAGE = 0.2


def uniqueEmoji(emoji):
    return [[emoji, emoji], [emoji, emoji], [emoji, emoji]]

def sameSpeciesEmoji(team1, team2):
    return [[team1, team2], [team1, team2], [team1, team2]]

dangerEm = sameSpeciesEmoji(
    '<a:dangerB:898372745023336448>', '<a:dangerR:898372723150041139>')
untargetableEmoji = uniqueEmoji('<:untargetable:899610264998125589>')

# List of guild ids for the bots
ShushyCustomIcons = [881900244487516180]
LenaCustomIcons = [881632520830087218, 881633183425253396]

stuffIconGuilds = [866782432997015613, 878720670006132787, 887756868787769434, 887846876114739261, 904164080204513331,
                   908551466988486667, 914608569284964392, 922684334010433547, 928202839136825344, 933783830341484624, 953212496930562098]
weaponIconGuilds = [866363139931242506, 878720670006132787, 887756868787769434,
                    938379180851212310, 887846876114739261, 916120008948600872, 911731670972002374]

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

# Tabl of random messages for the shop
shopRandomMsg = [
    "{alice} : \"J'aime bien les vêtements que tu proposes, mais ça manque de rose...\"\n{lena} : \"C'est une blague j'espère\"",
    "<:ikaBlue:866459319049650206> : `Sit down and eat pop-corns`\n{shushi} : `Regarde les pop-corns avec un air interresée`",
    "<:ikaPink:866459344173137930> : \"Flum POWA !\"\n{clemence} : \"Les coquelicots c'est mieux je trouve\"\n{alice} : \"N'importe quoi ! Ce sont les roses les plus jolies !\"\n{lena} : \"Vous trois, vous pourriez arrêter de débattre dans mon shop, s'il vous plait ?\"",
    "{lena} : \"Tiens, Clémence, j'ai trouvé un drôle de livre ces derniers temps et vu que tu t'y connais un peu en runes et magie, je me demandais si tu pouvais essayer de m'apprendre un peu comment m'en servir...\"\n{clemence} : \"Heu... ok\"",
    "{clemence} : \"Ah, Lena. J'ai jeté un coup d'œil à ton livre et heu... Tu as au moins une idée de ce qu'est un Carbuncle ?\"\n{lena} : \"Absolument pas\"\n{clemence} : \"... Ça va être long...\"",
    '{clemence} : "Hum... j\'ai trouvé des trucs qui pourrait t\'interresser lors de ma dernière escapade dans les ruines d\'Elidyn, Lena"\n{lena} : "Ow ? Montre pour voir ?"',
    '{shihu} : "Ti miman a un pobem"\n{shushi} : "Gomment za ?"\n{shihu} : "Mi miman commenze a en awoir marre de fire la zentille fifille"\n{shushi} : "..."',
    '{alice} : "Mooow tu sais que tu es trop mignone toi ?"\n{shushi} : "Heu... gwa ?"',
    '{clemence} : "Je me doute déjà de la réponse mais... Alice, pourquoi tu es quasiment toujours là où se trouve Hélène en ce moment ?"\n{alice} : "... Pour rien ^^"\n{clemence} : "Je suis pas vraiment convaincue..."',
    '{shihu} : "Ti en penze gwa de zette coupe de cheveux ?"\n{shushi} : "Hum... Pas viment convaincue..."\n{shihu} : "Oh..."\n{shushi} : "Mi apès, ze peux touzour en fire un queue de zeval regawde !\n{shihu} : :0',
    '{feli} : "Hé Clémence ! Je peux t\'accompagner pour ta prochaine aventure ? Je te promet que je te gênerais pas !"\n{clemence} : "Alala... Soit"\n{feli} : :D',
    '<:akira:909048455828238347> : ...\n{shihu} : ...\n<:akira:909048455828238347> {shihu} : ^^\n\n{lena} : <:LenaWhat:760884455727955978>',
    '{lena} : "\"Fini de jouer\" ? Tu as pas mieux comme phrase d\'accroche ?"\n{luna} : "Est-ce que je critique tes \"It\'s now or never\" moi ?"\n{lena} : "Roh, je suis sûre que tu l\'aime bien aussi cette chanson"\n{luna} : "Tss. Uniquement l\'originale."',
    '<:helene:906303162854543390> : "Tu es au courant que mourir par hémorragie est tout sauf une mort agréable hein ?"\n{shehisa} : "Je vois pas où est la différence avec les infections que tu donnes à tes adversaires. Je suis peut-être pas une soigneuse, mais Papa m\'a suffisament initiée pour savoir que les maladies que tu leur refile sont tous sauf agréable"',
    '{shehisa} : "Tu me reproche d\'avoir suivi la voie de Maman, mais tu devrais voir comment tu te comporte face à un ennemi quand tu veux lui faire avaler la pilule"\n<:helene:906303162854543390> : "Qu\'est-ce que tu insinue par là ?"\n{shehisa} : "Que je suis pas la seule à avoir héritée des talents de Maman"',
    '{shehisa} : "Toujours rassurant de te savoir dans les parages, Icealia"\n{icelia} : "Et moi je suis toujours rasurée de te savoir dans mon camp..."',
    '<:determination:867894180851482644> : "Alors Féli, tu as fais des progrès sur ta maitrise de la Détermination ?"\n{feli} : "Ouais :D ! Regarde ça !"',
    '<:ruby:958786374759251988> : "Clémence, ça va mieux avec ta cicatrice en ce moment ?"\n{clemence} : "À part qu\'elle me brûle quand j\'utilise trop mes pouvoirs vampiriques ou quand il y a un Alpha dans le coin, rien à déclarer"\n<:ruby:958786374759251988> : "Tss. Ces loups garoux..."\n{clemence} : "Pas la peine de prendre ce regard assassin Madame Ruby. J\'ai appris à faire avec maintenant"',
    '`Alice surgit au coins du couloir en courant et vous rentre dedans, ne vous ayant pas vu`\n\n{alice} : "Dé-désolée !"\n\n`Elle ramasse rapidement les cahiers qu\'elle portait dans ses bras et repart aussi vite qu\'elle est venue.\nVous constatez qu\'elle a oublié une feuille, qui a du se retrouver sous elle quand elle est tombée`\n\n📄 [Devoir d\'astronomie sur les trous noirs](https://bit.ly/3kh8xP3)',
    '{alice} : "Maraiiiiiiiiine ?"\n{lena} : "Il y a un peu trop de "i" pour moi..."\n{alice} : "C\'est quoi ça."\n\n`Elle sortie son téléphone et le mit directement devant le visage de Lena`\n\n📱 [Photographie d\'une feuille de papier](https://bit.ly/3o74aal)\n\n{lena} : "... Merde. Et comment ça, tu es allé fouiller dans ma chambre !?"',
    '{lena} : "Tu sais que tu va finir par traumatiser des gens avec tes \"Boum boum\" toi ?"\n{shihu} : "Mi z\'est drole les Boum Boum..."',
    '{clemence} : "Hé Powehi, je me suis retrouvée avec plein de Rotten Flesh lors de ma dernière expédition, tu veux que je te les passes ?"\n<:powehi:909048473666596905> : "Oh que oui !"',
    '<:gweny:906303014665617478> : "Toujours à regarder les étoiles ?"\n<:powehi:909048473666596905> : "J\'ai une question Gwendoline... Tu réagirais comment si tu étais bloquée dans ce monde après ta mort et ne pouvais que regarder les autres être vivant te fuir dès que tu t\'approches trop d\'eux ?"\n<:gweny:906303014665617478> : "Oh heu... Je sais pas vraiment désolée. Compliqué de se mettre à ta place, j\'en ai bien peur"\n<:powehi:909048473666596905> : "C\'est pas grave, merci quand même..."',
    '`En entrant dans une pièce présumée vide, vous êtes surpris de voir des reflets lumineux dans un coin. En allant l\'examiner, vous découvrez Shushi et Sixtine qui dorment l\'une contre l\'autre. Au sol se trouve un lecteur de musique`\n\n📱 [Liste de musique en file d\'attente](https://bit.ly/3D6Ltdh)',
    "<:john:908887592756449311> : \"A-Alice, toi qui la connais bien tu... saurais ce que je pourrais faire pour... qu'elle me voit comme autre chose qu'un... ami ?\"\n{alice} : \"Commence par être un peu plus sûr de toi. Là, elle continue de voir le louvetau naïf qui essayait de se coucher à ses pieds au lieu de fuir\"\n<:john:908887592756449311> : \"Mais je-\"\n{alice} : \"Passe ton temps avec elle sous ta forme de loup à être couché à ses pieds. Si tu veux qu'elle te vois comme autre chose qu'un chien de compagnie, va falloir que tu arrête de te comporter tel quel.\"",
    "<:lio:908754690769043546> : \"H-hm !? Oh c'est toi...\"\n{feli} : \"Tiens tu es là toi aussi ?\"\n<:lio:908754690769043546> : \"J'ai pas trouvé d'autres points d'eau dans le coin donc oui... je suppose...\"",
    "<:gweny:906303014665617478> : \"Eh bien... On... fatigue déjà... Liu... ?\"\n<:liu:908754674449018890> : \"Cer... Certainement pas... Je... pourrais courir... comme ça... pendant encore des kilomètres...\"",
    "<:lia:908754741226520656> : \"Hé Alice ! Tu penses quoi de ces fleurs là ?\"\n{alice} : \"Hum... un peu trop jaune à mon goût...\"",
    "{shushi} : \"Hé hé Midame des neizes ! Z'est touvé za part terre, y a maqué quoi dezu ?\"\n{icelia} : \"Montre moi pour voir ^^ ?\"\n\n📃 [Page de papier à l'encre rose](https://bit.ly/3DgXk8v)",
    "{lena} : \"La vache c'est bien plus compliqué que je le pensais de lancer ces plumes enfaites...\"\n<:hina:908820821185810454> : \"C'est qu'une question d'habitude ^^ Hônnetement... J'arriverai même pas à tenir un de tes fusils donc bon ^^'\"",
    "{sixtine} : \"...\"\n<:krys:916118008991215726> : ?\"\n{sixtine} : \"...\"\n<:krys:916118008991215726> : \"?.? Je peux t'aider ?\"\n{sixtine} : \"Oh heu... Je me demandais juste si tu avais un coeur de pierre...\"\n<:krys:916118008991215726> : \"??.??\"",
    "{iliana} : \"Cl-Clméence... ? Hum... tu sais pourquoi ta soeur m'évite toi... ?\"\n{clemence} : \"Si tu parles d'Alice, elle a eu quelques porblèmes avec un chat quand elle était plus jeune donc elle en est un peu traumatisée\"\n{iliana} : \"Oh... la pauvre...\"",
    "{iliana} : \"Je... C'est ton droit de me détester mais... Je pourrais au moins savoir pourquoi... ?\"\n{iliana} : \"Lena... qu'est-ce que j'ai mal fait... ?\"\n{iliana} : \"L-Lena... m'ignore pas s'il te plaît...\"\n{iliana}  : \"... Désolée...\"",
    "{sixtine} : \"Par curiosité Alice... tu as quoi comme info sur Iliana ?\"\n{alice} : \"Hum... Laisse moi voir... Tiens voilà\"\n\n[Feuille de papier froisée](https://docs.google.com/document/d/1SUVmdch_lQ-Ub_zoTJKOtxTkwZMqyLD8xrbCq8CTcDQ/edit?usp=drivesdk)\n\n{sixtine} : \"Même sur ça tu as fais d'efforts... ?\"\n{alice} : S-Sixtine ! Tu sais bien que je peux juste... pas...",
    "{luna} : \"Hum... Iliana ? Je peux te demander pourquoi tu restes toujours avec moi enfaite... ? Enfin... On représente chacune des éléments totalement opposés, j'ai détruit ta dimension native et passe mon temps à te rabaisser. Tu as toutes les raisons du monde pour me détester...\"\n{iliana} : `Saute des genoux de Luna en reprenant sa forme humaine puis se tourne face à elle` \"Il est vrai que je pourrais totalement te détester comme ton alter ego me déteste, mais honnements je crois que je suis trop stupide pour ça ^^ Et puis va pas me dire que tu me déteste aussi, sinon ça ferai un moment que je me serais prise des murs quand je monte sur tes genoux et tu me carresserais pas la tête quand je le fais. Et toi, pourquoi tu me déteste pas ?\"\n{luna} : \"Je heu... Bonne question...\"",
    "`Gwen descendit dans le séjour pour aller préparer le petit déjeuné quand elle vit Lena en train de dormir sur le canapé. Sur la table se trouve plusieurs pièces de ce qu'elle devina être un nouveau fusil longue portée et en déduit que l'inkling a encore veillé jusqu'à point d'heure pour mettre au point un nouveau joujou\nEn approchant, elle vit Shushi assise à côté de sa mère en train d'essayer de résoudre un Rubik's cube silencieusement. En la voyant arriver, celle-ci mit doucement un doigt sur ses lèvres. Gwen lui sourit gentiment puis alla dans la cuisine`",
    "{clemence} : `Attend le trio de soeur en lisant assise (à l'ombre) à la terrasse d'un café tout en discutant avec Gwen, quand elle vit Sixitine venir seule` \"Comment ça tu es toute seule Sixtine ? Où sont Féli et Alice ?\"\n{sixtine} : \"Féli a dit qu'elle voulait aller voir la dernière expédition sur les dieux de la Grèce Antique et Alice a... dit un truc à propos de l'Eglise je crois...\"\n{clemence} : \"... Gweny, tu veux bien t'occuper d'aller chercher Alice et je me charge de Féli ?\"\n<:gweny:906303014665617478> : \"Je suis pas vraiment la bienvenue dans les églises catholiques aussi tu sais ?\"\n{clemence} : \"Déjà moins que moi...\"\n{sixtine} : \"Je peux y aller moi si vous voulez... Je suis qu'humaine...\"",
    "{sixtine} : `Regarde le crusifix et le livre religieux à côté du lit d'Alice` \"Comment tu arrives à dormir à côté de ça... Clémence ne supporte même pas d'être à proximité d'une croix...\"\n{alice} : `Fait une petite moue`\" C'est elle qui s'est définie en temps qu'ennemi du divin souss prétexte que c'est sa nature. Mais ce genre de discipline tiens sa puissance en la Foi. Tant que tu l'as, qu'importe que ce tu es",
    "{clemence} : \"... Je sais que tu as la manie de dormir partout Sixtine... Mais dans mon cercueil tout en étant claustrophobe ?\"\n{sixtine} : `Dort à point fermé`",
    "{lena} : \"Contente que tu ai changé d'avis\"\n<:ly:943444713212641310> : \"J'avais besoin de changer d'horison\"",
    "<:edelweiss:918451422939451412> : \"... Je peux t'aider ? On le dirait pas comme ça mais je me débrouille plutôt bien en soins\"\n<:lohica:919863918166417448> : \"Tu me rappelle juste quelqu'un, c'est tout... Et ton truc c'est pas plutôt la protection ?\"\n<:edelweiss:918451422939451412> : `Hausse les épaules` \"Je le fais parcequ'il y a déjà pas mal de personnes qui soignent ici, c'est tout\"",
    "{sixtine} : `Regarde les étoiles dans une prairie, puis remarque qu'elle n'est pas seule` \"... toi aussi tu brillais autant à l'époque où tu étais une étoile aussi... ?\"\n<:powehi:909048473666596905> : \"Et comment ! J'étais la plus grande, la plus chaude et la plus brillante de ma région...\"\n{sixtine} : \"Tu avais un système planétaire aussi ?\"\n<:powehi:909048473666596905> : \"Trois. Elles étaient plutôt sympatiques, et l'une d'entre elle abritait même la vie mais... `Soupir` Elles...\"\n{sixtine} : \"... Au moins je suis sûre qu'elles ont bien aimée ta supernova...\"\n<:powehi:909048473666596905> : \"Je... je pense... Leurs représentations se tenaient les mains sans vraiment avoir l'air effrayées...\"",
    "{feli} : \"Dit Maraine, tu peux jouer ça au violon ?\"\n{lena} : \"Hum laisse moi voir ? Si Do# Mi Fa# Mi Ré# Do# Si Fa#... Oh. Je vois où tu veux en venir\"",
    "{lena} : \"Merci du coup de main Lio. Bon maintenant Shihu. Qu'est-ce que j'ai dit à propos de l'utilisation de la magie à la maison ?\"\n{shihu} : \"De... Pas utiliser la magie à la maison...\"\n{lena} : \"Et donc pourquoi on a du s'y mettre à trois pour éteindre les flammes noires dans votre chambre ?\"\n{shihu} : \"Mais il y avait un moustique...\"\n{lena} : \"Et tu penses sérieusement que risquer de réduire la maison en cendre pour un moustique est une bonne idée ?\"\n{shihu} : \"... au moins je l'ai eu...\"\n{lena} : \"... Vous êtes toutes les deux privées de dessins animés et de dessert pour une semaine.\"\n{shushi} : \"Mais j'ai rien fait moi !\"\n{lena} : \"Justement.\"",
    "{shihu} : \"Lena ne va pas du tout être contente quand elle vera que tu as pris un de ses pistolets d'airsoft...\"\n{shushi} : \"Elle n'en saura rien !\"\n{shihu} : \"Tu as même pas pris de protections..\"\n\n`Shushi visa une canette vide et tira, sans grand succès. La bille rebondit cependant sur le mur derrière et explosa contre un bouclier lumineux qui s'était formée devant la petite fille avant qu'elle n'ai eu le temps de bouger. Cette dernière regarda un peu confuse autour d'elle puis elle remarqua la chatte blanche assise à côté d'elle qui la regardait fixement`\n\n{shushi} : \"... s'il te plait le dis pas à Miman...\"\n{iliana} : \"Si tu ranges ça, peut-être\"\n{shihu} : \"(Pff, elle fait juste ça pour pas que Lena la tienne responsable également)\"",
    "{alice} : `Carresse très lentement Iliana en étant relativement tendue`\n{iliana} : `Se contente de ronronner sans bouger pour éviter de l'effrayer. Et puis elle aime bien les caresses`\n{alice} : `Se met à lui caresser le ventre en voyant qu'elle s'est mise sur le dos`\n{iliana} : `Essaye le plus possible d'ignorer son instinct de félin qui lui hurle d'essayer de mordiller cette main qui se balade sur son ventre, parcequ'elle n'a pas envie que cette même main la projette contre un mur dans un mouvement brusque avec toute la force d'une jeune vampire paniquée. Quelque chose lui dit que plusieurs de ses os ne l'appréciraient pas trop`",
    "{shushi} : \"Maman tu fais quoi ?\"\n{lena} : \"Hum ? Oh rien d'important\" `Glisse une feuille de papier derrière elle`\n{shushi} : \"Tu peux m'aider pour mes devoirs :< ? J'y arrive pas\"\n{lena} : \"Oh oui bien sûr ^^\"\n\n`Les deux quittèrent la pièce en laissant la dite feuille sur le bureau`\n\n:page_with_curl: [Feuille de papier](https://docs.google.com/spreadsheets/d/1l6csj2GjnaHMPYhPgqaji6Hs7bU68eb4XC_Ss2oxT-4/edit?usp=drivesdk)"
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
        "{lena} : \"J'ai jamais compris pourquoi les gens cachent des oeufs en chocolat pour Pâques\"\n{luna} : \"Ça ne t'empêches pas de le faire quand même\"\n{lena} : \"En même temps, même toi tu ne peux pas être insensibles à toutes leurs bouilles heureuses\"\n{luna} : \"Évite de parler en mon nom s'il te plaît\""
    ]
    }
]

shopSeasonWinter = [
    "{clemence} : `Lit un grimoire en étant assise sur un fauteuil devant la cheminée`",
    "{lena} : \"Féli, si tu pouvais arrêter de dormir dans le feu ça m'arrangerais pas mal\"\n{feli} : \"Bah pourquoi :< ?\"\n{lena} : \"Parceque après tes soeurs et Shushi veulent faire la même chose. Et elles, elles ne sont pas fireproof.\"\n{feli} : \"Oh\"",
    "{alice} : `Boit un chocolat chaud en étant assise sur un fauteuil devant la cheminée`\n{sixtine} : `Arrive dans le salon avec sa couette sur les épaules et monte dans le fauteuil pour se blottir contre Alice`\n{alice} : \"ça va pas ?\"\n{sixtine} : \"Juste un cauchemar...\"\n{alice} : `patpat`",
    "{clemence} : `Regarde Félicité de haut en bas` \"Toi tu as encore dormi dans la cheminée\"\n{feli} : \"D: Non c'est faux !\"\n{clemence} : \"Tu es pleine de cendres, s'il te plaît x)\"",
    "{lena} : `Descend dans le salon à 3h du matin pour prendre un verre d'eau et voit une boule de poils blancs devant la cheminée` \"C'est pour ça qu'on porte des vêtements, Lio\"\n<:lio:908754690769043546> : `Eternue dans son sommeil`\n{lena} : `Soupir, remet une buche dans la cheminée puis pose une couverture sur la grosse boule de poils`"
]

shopSeasonSpring = [
    "{alice} : `Est assise sur une commode devant une fênetre et regarde la pluie arroser ses fleurs`",
    "{alice} : `Plante des fleurs dans le jardins tandis que Sixtine regarde les nuages`",
    "{luna} : \"Dans notre ancien chez nous les fleurs mourraient si elles avaient trop de Lumière\"\n{iliana} : \"Vraiment toutes ? Même ici il y a des fleurs qui vivent dans l'ombre\"\n{luna} : \"À quelques exeptions près, effectivement\"",
    "{lena} : \"Surtout tu oublie pas ton parapluie !\"\n{shushi} : \"Mi il fait grand soleil !\"\n{lena} : \"Il peut très rapidement se mettre à pleuvoir à cette saison, Shu'\"",
    "{alice} : \"J'ai hate que l'été arrive ! Tu viendras avec nous à la plage Clémence :D ?\"\n{clemence} : \"Hum, tu veux dire sous un soleil de plomb en maillot de bain avec la mer qui fait ses remous juste à côté alors que je déteste l'eau et arrive à me chopper des coups de soleil en hiver et sans reflets sur la neige ?\"\n{alice} : \"... Désolée c'était stupide...\"",
    "<:anna:943444730430246933> : \"Hé Alice, tu en penses quoi de cet ensemble... ?\"\n{alice} : \"Un peu viellot, mais ça te va bien\"",
    "{lena} : \"On est surtout, évitez de traîner trop avec Lia s'il vous plaît. Le printemps est sa saison de prédilection\""
]

shopRepatition = [4, 5, 8, 3]                 # Shop's item category length

# Same, but for the roll command
rollMessage = ["Selon toute vraisemblance ce sera un **{0}**", "Puisse la chance être avec toi... **{0}** !", "Alors Alice tu as obtenu combien ? **{0}** ? **{0}** alors",
               "Sur 100, les chances que la relation Akrisk tienne debout ? Hum... **{0}**", "Le nombre de lances que tu va avoir à esquiver est... **{0}**"]

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

tablCat = ["Début du combat", "Compétence ultime", "Transcendance", "En éliminant un ennemi", "À la mort", "En étant ressucité", "Victoire (Bleu) en étant en vie", "Victoire (Bleu) en étant mort", "Défaite (Bleu)", "Victoire (Rouge) en étant en vie", "Victoire (Rouge) en étant mort",
           "Défaite (Rouge)", "Bloquer une grosse attaque", "Réaction à la réanimation de plusieurs alliés", "Réaction à la réanimation de plusieurs ennemis", "Réanimer plusieurs allier en même temps", "Réaction à l'élimination d'un ennemi", "Réaction à l'élimination d'un allié"]

class says:
    """A class for storing the says message from a entity"""

    def __init__(self, start=None, ultimate=None, limiteBreak=None, onKill=None, onDeath=None, onResurect=None, blueWinAlive=None, blueWinDead=None, blueLoose=None, redWinAlive=None, redWinDead=None, redLoose=None, blockBigAttack=None, reactBigRaiseAllie=None, reactBigRaiseEnnemy=None, bigRaise=None, reactEnnemyKilled=None, reactAllyKilled=None):
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
    limiteBreak="It's now or never ! {skill} !",
    onDeath="Tps.",
    onResurect="J'te revaudrais ça {target}",
    blueWinAlive="Une victoire en bonne uniforme",
    redWinAlive="Vous avez encore des progrès à faire",
    redWinDead="Pas mal. Mais pas suffisant",
    redLoose="Ahah, pas trop mal cette fois-ci. Mais ce n'était qu'un entrainement",
    reactBigRaiseAllie="Bien joué {caster}",
    reactBigRaiseEnnemy="Je dois avouer qu'il était pas mal celui-là. Je suppose que j'ai qu'à donner le meilleur de moi-même de nouveau",
    reactEnnemyKilled="Pas trop mal {killer}",
    reactAllyKilled="T'en fais pas {downed}, je m'en charge.",
    blockBigAttack="Hé Luna ! Un brisage de l'Espace Temps ça te dis ?\"*\n<:luna:909047362868105227> : \*\"C'est pas déjà ce que l'on était en train de faire ?"
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
    reactAllyKilled="T'en fais pas {downed} !"
)

clemSays = says(
    start="`Ferme son livre` Ok allons-y",
    ultimate="J'espère que tu es prêt pour te prendre un {skill} dans la face, {target} !",
    onDeath="Je t'ai sous estimé manifestement...",
    onResurect="Merci du coup de main",
    redWinAlive="Et bah alors, on abandonne déjà ?",
    blueWinAlive="Simple. Basique.",
    reactEnnemyKilled="Pas mal celle-là {killer}"
)

ailillSays = says(
    start="Tss, encore vous ?",
    onKill="Venez autant que vous êtes, ça changera rien",
    onDeath="Tu... paie rien pour attendre...",
    redWinAlive="Vous appelez ça un combat ?",
    reactBigRaiseEnnemy="Parceque vous pensez que ça changera quelque chose ?"
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
    redLoose="Vous savez pas rire..."
)

liuSays = says(
    start="Hé ! Une course d'endurance vous en pensez quoi ?",
    onKill="Va falloir mieux gérer ta fatigue la prochaine fois",
    onResurect="Une seconde course ?",
    redLoose="Hé bah... Finalement c'est moi qui ai mordu la poussière",
    limiteBreak="Pas si vite !"
)

lioSays = says(
    start="Oh... Heu... Bonjour...",
    onKill="J- J'y suis allé trop fort ?",
    onResurect="Merci...",
    onDeath="Humf ! J'aurais du rester dans la forêt...",
    redWinAlive="Le monde des humains est... perturbant...",
    bigRaise="On lache rien...",
    reactBigRaiseEnnemy="Je peux faire ça aussi, tu sais...",
    reactAllyKilled="Vous commencez à me taper sur les nerfs..."
)

lizSays = says(
    start="Tiens donc, des nouvelles braises",
    ultimate="Allez quoi, déclarez moi votre flamme !",
    onKill="Woops, j'y suis allé trop fort manifestement",
    onDeath="Pff, vous êtes pas drôle",
    redLoose="Waw, je me suis jamais faite autant refroidir rapidement..."
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
    redLoose="Zzz..."
)

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
    ["On a qu'une seule vie comme on dit. Enfin particulièrement chez vous, où personne a réanimé personne",
        "Conseil d'amie : Vous feriez mieux d'avoir quelqu'un qui puisse réanimer dans votre équipe, et pas toujours vous reposer sur nous pour vous sauver le postérieur"],
    ["Vous avez vraiment réussi à subir aucuns dégâts jusqu'à là ?"],
    ["Faut croire que vous aimer vous faire maraver la figure, personne a soigné personne dans votre équipe"],
    ["Vous savez qu'avoir un peu d'armure peu pas vous faire de mal, hein ?"],
    ["Je sais que le role de Support n'est pas particulièrement attractif, mais bon il reste quand même utile d'en avoir un"]
]

clemPosSays = says(
    start="Encore des chasseurs de vamires ? J'en ai ma claque des gens de votre genre.",
    onKill="Un de plus, un de moins. Quelle importance",
    redWinAlive="Restez à votre place.",
    redLoose="Que..."
)

aliceExSays = says(
    start="Clémence...",
    onKill="...",
    onResurect="Merci...",
    blueWinAlive="ça... ça va mieux ?",
    bigRaise="Je y arriver probablement pas... S'il vous plaît..."
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

# ["Berserkeur","Observateur","Poids plume","Idole","Prévoyant","Tête brulée","Mage","Altruiste","Invocateur","Enchanteur","Protecteur"]
limitBeakGif = [
    'https://cdn.discordapp.com/attachments/927195778517184534/932778559150391366/20220118_002840.gif',  # Ber
    'https://cdn.discordapp.com/attachments/927195778517184534/932775385043709952/20220118_001608.gif',  # Obs
    'https://cdn.discordapp.com/attachments/927195778517184534/932774912391782490/20220118_001411.gif',  # PPlu
    'https://cdn.discordapp.com/attachments/927195778517184534/932776578058965102/20220118_002049.gif',  # Ido
    'https://cdn.discordapp.com/attachments/927195778517184534/932778559502700594/20220118_002719.gif',  # Pré
    'https://cdn.discordapp.com/attachments/927195778517184534/932777330605178920/20220118_002344.gif',  # TBru
    'https://cdn.discordapp.com/attachments/927195778517184534/932773655732158525/20220118_000607.gif',  # Mage
    'https://cdn.discordapp.com/attachments/927195778517184534/932773655342104606/20220118_000858.gif',  # Alt
    'https://cdn.discordapp.com/attachments/927195778517184534/932773655732158525/20220118_000607.gif',  # Enc
    'https://cdn.discordapp.com/attachments/927195778517184534/932777330978488391/20220118_002225.gif'  # Pro
]

lenaTipsMsgTabl = [
    "Est-ce que quelqu'un lit vraiment ça ?",
    "Si vous réalisez la commande /fight normal alors qu'il vous reste moins de 10 minutes de repos, votre combat sera mis en file d'attente et se lancera automatiquement une fois le décompte écoulé",
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
    "Chaque réanimation accorde une armure absolue équivalente à 20% des PVs maximums du réanimé à ce dernier",
    "Les armures absolues protègent de tous types de dégâts à l'exeption de la Mort Subite et des coûts en PV des compétences démoniques",
    "Les armures absolues et normales absorbent des dégâts supplémentaires lorsqu'elles sont détruites. Par défaut, cette valeur est égale à votre niveau, mais certaines compétences peuvent influer dessus",
    "Donner une armure normale ou légère à un combattant qui possède déjà une armure normale ou absolue réduit la valeur de cette nouvelle armure. Par défaut, la réduction est de 50%, mais certaines compétences peuvent influer dessus",
    "Kiku commence tous ses combats avec le status \"Réanimée\"",
    "Certains ennemis comme l'OctoBOOM ne peuvent pas être réanimés",
    "Les Berserkeur ont besoin de pouvoir infliger des dégâts pour être des tanks efficace. Par conséquent leur donner un autre second role que DPT est pas vraiment une bonne idée",
    "Les statistiques des Idoles leur permettent de pouvoir se spécialiser dans tous les roles de support, de soins ou de protection, sauf Tank",
    "Les statistiques des Altruistes ainsi que leurs compétences propres en fond de très bon soigneur, mais avec les bons équipements ils peuvent aussi être de bon booster d'équipe",
    "Les Mages bénificent principalement de l'utilisation de compétence ultime, mais comme leur bonus dure 2 tours, ils peuvent le cumuler avec les compétences avec un tour de chargement",
    "Les Poids Plumes ont naturellement une endurance et une force relativement faible, mais cela est compensé par leur grande agilité qui leur permet d'esquiver ou d'infliger des coups critiques plus souvent que ses concurants de mêlée\nDe plus, à l'instar des Observateurs, leurs coups critiques infligent plus de dégâts",
    "Le taux d'esquive est calculé en fonction de la différence entre la précision de l'attaquant et l'agilité de l'attaqué.\nSi l'attaqué est plus agile, le taux de réussite de l'attaque est diminuée jusqu'au maximum la moitié de sa valeur\nÀ contratio, une précision plus élevée de l'attaquant peut lui donner jusqu'à deux fois plus de chances de toucher",
    "Le 19 de chaques mois, les records mensuels sont rénitialisés",
    "Il se peut que vous obtenez une récompense si vous possédez un certain pourcentage des objets obtenables dans le magasin ou en butin",
    "Ailill impose une icone mortuaire aux cibles qu'elle élimine, qu'importe la manière. Mais subir sa compétence signature donne un succès...",
    "Lors d'un raid, vous êtes associé à une équipe dont le niveau moyen est similaire à celle de la votre. Cependant, cette équipe tierce n'obtient aucune récompense",
    "Vous vous souvenez de l'aspiration \"Stratège\" ? Ouais moi non plus",
    "Funfact : Tout à commencé sur une aire d'autoroute pendant que Lénaïc s'ennuyait à attendre que sa famille revienne de sa pause pipi",
    "Les sorciers créent de petites détonnations quand ils éliminent un ennemi. Celles-ci prennent en compte les statistiques de Magie et de Dégâts indirects",
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
    "Alice n'aime pas vraiment que quelqu'un monte sur scène en sa présence"
]

ilianaSaysNormal = says(
    start="Puisse ce combat être miawtastique !",
    ultimate="Nynme de la Lumière Infinie !",
    limiteBreak="Que la Lumière nous protège !",
    onKill="Nyan. Désolée",
    onDeath="Miaw !!",
    reactAllyKilled="Nyan !",
    reactBigRaiseAllie="Miawtastique"
)

ilianaSaysVsLuna = says(
    start="Tu nous fais encore une crise ?",
    ultimate="Courraw tout le monde !",
    onKill="T'enw fait pas Luna !",
    onDeath="Miaw...",
    onResurect="Miawzi bien",
    blueWinAlive="`S'assoit à côté de Luna, qui est trop fatiguée pour bouger, lui met la tête sur ses genoux puis caresse cette dernière en ronronnant`\"\n<:luna:909047362868105227> : \"Ili'...\"\n<:Iliana:926425844056985640> : \"Niow Niow. Tu ferais la même chose si c'était moiw, et tu t'es faite battre à plate couture, tu ees paw en droit de contester\"\n<:luna:909047362868105227> : \"... `Ferme les yeux et s'endort peut de temps après`",
    blockBigAttack="Si tu crois que tu va m'awvoir avec ça !",
    reactBigRaiseAllie="Je m'owcupe des Ténèbres qui paralyse votre âme, et on y retourwn !"
)

kitsuneSays = says(
    start="Mais c'est que vous êtes bien nombreux dites donc ^^",
    onKill="Je suppose que s'en était trop pour toi",
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

gwenySays = says(start="Tachons de faire ça rapidement, ça vous vas ?",ultimate="Ok ça suffit là !",limiteBreak="Ok là vous m'avez énervée !",reactAllyKilled="Je suppose que j'ai une nouvelle cible maintenant",reactBigRaiseEnnemy="En quoi c'est juste ça Lena !?\"*\n<:lena:909047343876288552> : \"*Vous pouvez le faire aussi, arrête de te plaindre")
klikliSays = says(start="Ok. Je vais m'en occuper rapidement",limiteBreak="OK, VOILÀ POUR VOUS !",onKill="Si tu veux revenir, j't'ai pas encore montrer tout ce dont je suis capable.",reactEnnemyKilled="Pff, j'peux le faire toute seule tu sais ?")
altySays = says(start="'K, je vais faire de mon mieux",onKill="Désolée...",onResurect="Ok, second round !",reactAllyKilled="{killed} !")

shehisaSays = says(start="Ok, si on suit le plan, tout se passera bien",onKill="Tu aurais pu attendre que je soit partie avant de creuver quand même.",onDeath="Humf, c'était pas prévu ça...",reactAllyKilled="On lache rien !",reactBigRaiseEnnemy="C'était trop beau pour être vrai",blueWinAlive="Tout s'est déroulé comme prévu",redWinAlive="Tout s'est déroulé selon le plan")
