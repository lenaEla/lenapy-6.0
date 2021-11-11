from classes import *
import random,copy

def uniqueEmoji(emoji):
    return [[emoji,emoji],[emoji,emoji],[emoji,emoji]]

def sameSpeciesEmoji(team1,team2):
    return [[team1,team2],[team1,team2],[team1,team2]]

dangerEm = sameSpeciesEmoji('<a:dangerB:898372745023336448>','<a:dangerR:898372723150041139>')
untargetableEmoji = uniqueEmoji('<:untargetable:899610264998125589>')
intargetable = effect("Inciblable","untargetable",untargetable=True,emoji=uniqueEmoji('<:untargetable:899610264998125589>'),description="Cet entité deviens inciblable directement")

print("")
# Weapon
splattershot = weapon("Liquidateur","ab",RANGE_DIST,AREA_CIRCLE_3,40,50,280,precision=10,strength=10,repetition=3,emoji = emoji.splatShot,affinity=ELEMENT_NEUTRAL)
roller = weapon("Rouleau","ac",RANGE_MELEE,AREA_CIRCLE_1,70,70,340,strength=15,endurance=5,resistance=5,agility=-5,emoji = emoji.roller,needRotate=False,affinity=ELEMENT_AIR,area=AREA_CONE_2,damageOnArmor=0.8)
splatcharger = weapon("Fusil de précision anti-matériel","ad",RANGE_LONG,AREA_CIRCLE_5,83,60,482,agility=-5,precision=25,emoji = '<:sniperRifle:903115499204923402>',damageOnArmor=2,affinity=ELEMENT_WATER)
miniBrush = weapon("Epinceau","ae",RANGE_MELEE,AREA_CIRCLE_1,31,45,224,agility=10,charisma=10,repetition=5,emoji='<:inkBrush:866463573580578816>',needRotate=False)
inkbrella = weapon("Para-Encre","ag",RANGE_MELEE,AREA_CIRCLE_1,41,45,price=472,endurance=10,resistance=10,precision=-10,repetition=3,effect='lp',emoji='<:splatbrella:866464991255199834>',needRotate=False)
blaster = weapon("Eclatblasteur","ah",RANGE_DIST,AREA_CIRCLE_3,84,50,150,agility=10,strength=10,percing=10,precision=-10,area=AREA_CIRCLE_1,emoji='<:blaster:866463931304378418>')
jetSkelcher = weapon("Nettoyeur XL","ai",RANGE_LONG,AREA_CIRCLE_5,31,40,200,10,precision=10,repetition=4,emoji='<:squelsher:866464376319115281>',affinity=ELEMENT_WATER)
dualies = weapon("Double Encreur","aj",RANGE_DIST,AREA_CIRCLE_3,42,35,150,agility=20,repetition=4,emoji='<:splatDualies:866465264434806815>',needRotate=False,affinity=ELEMENT_AIR)
kcharger = weapon("Concentraceur alt.","ak",RANGE_MELEE,AREA_CIRCLE_1,38,60,200,15,agility=15,magie=-10,repetition=3,emoji='<:kcharger:870870886939508737>',message="{0} frappe {1} avec son arme :",use=STRENGTH)
HunterRiffle = weapon("Fusil de chasseur","al",RANGE_DIST,AREA_CIRCLE_4,67,65,250,precision=10,effect="ls",emoji="<:hunterRifle:872034208095297597>",affinity=ELEMENT_NEUTRAL)
firework = weapon("Arbalette avec feu d'artifice","am",RANGE_LONG,AREA_CIRCLE_4,76,50,150,10,precision=10,emoji='<:crossbow:871746122899664976>',area=AREA_CONE_2)
plume = weapon("Plumes tranchantes","ao",RANGE_DIST,AREA_CIRCLE_4,60,50,250,precision=10,percing=10,repetition=1,emoji='<:plume:871893045296128030>',area=AREA_CONE_2,needRotate=False,affinity=ELEMENT_AIR,effectOnUse=incur[2])
hourglass1Weap = weapon("Sablier intemporel I","ap",RANGE_DIST,AREA_CIRCLE_3,35,100,250,endurance=10,resistance=10,target=ALLIES,affinity=ELEMENT_TIME,type=TYPE_HEAL,effectOnUse="lx",emoji='<:hourglass1:872181735062908978>',use=CHARISMA)
clashBlaster = weapon("Rafa-Blasteur","aq",RANGE_MELEE,AREA_CIRCLE_2,28,40,250,endurance=10,agility=10,precision=-10,percing=10,emoji='<:clashBlaster:877666681869176853>',area=AREA_CIRCLE_1,repetition=4)
dualies = weapon("Double Encreur","ar",RANGE_DIST,AREA_CIRCLE_4,34,40,150,agility=15,precision=15,resistance=-10,repetition=4,emoji='<:splatDualies:866465264434806815>')
splatling = weapon("Badigeonneur","as",RANGE_LONG,AREA_CIRCLE_5,33,30,300,precision=10,strength=10,repetition=5,emoji='<:splatling:877666764736061490>')
flexi = weapon("Flexi-Rouleau","at",RANGE_DIST,AREA_CIRCLE_3,85,70,300,25,endurance=-10,critical=5,emoji='<:flexaRoller:877666714760925275>',needRotate=False)
squiffer = weapon("Décap' Express","au",RANGE_DIST,AREA_CIRCLE_4,78,70,300,10,agility=15,precision=10,resistance=-5,endurance=-10,emoji='<:skiffer:877666730225328138>')
dualJetSkelcher = weapon("Nettoyeur Duo","av",RANGE_LONG,AREA_CIRCLE_5,25,50,200,10,magie=10,agility=-10,precision=10,repetition=4,emoji='<:DualSkelcher:877666662801883237>',damageOnArmor=1.33)
butterfly = weapon("Papillon Blanc","aw",RANGE_LONG,AREA_CIRCLE_5,35,80,150,-5,-5,20,use=CHARISMA,intelligence=10,emoji='<:butterflyB:883627125561786428>',target=ALLIES,type=TYPE_HEAL,needRotate=False,message="{0} demande à son papillon de soigner {1} :")
mic = weapon("Micro mignon","ax",RANGE_LONG,AREA_CIRCLE_3,64,75,300,-10,charisma=30,emoji='<:pinkMic:878723391450927195>',needRotate=False,use=CHARISMA,message="{0} pousse la chansonnette !")
spellBook = weapon("Grimoire de feu","ay",RANGE_DIST,AREA_CIRCLE_4,40,75,200,-10,-10,15,magie=20,percing=5,emoji='<:spellBook:878723144326725744>',needRotate=False,use=MAGIE,area=AREA_CIRCLE_1,affinity=ELEMENT_FIRE,message="{0} lance une boule de feu sur {1}")
legendarySword=weapon("Épée et Bouclier de Légende","az",RANGE_MELEE,AREA_CIRCLE_1,82,85,300,10,10,resistance=10,intelligence=-10,emoji='<:masterSword:880008948445478962>',affinity=ELEMENT_LIGHT)
depha = weapon("Lame Dimensionnelle","ba",RANGE_MELEE,AREA_CIRCLE_1,77,90,300,20,10,-10,intelligence=-10,resistance=10,emoji='<:LameDimensionnelle:881595204484890705>')
butterflyR = weapon("Papillon Rose","bb",RANGE_LONG,AREA_CIRCLE_5,50,80,150,-5,-5,20,intelligence=10,emoji='<:butterflyR:883627168406577172>',use=CHARISMA,needRotate=False,message="{0} demande à son papillon d'attaquer {1} :")
butterflyP = weapon("Papillon Violet","bc",RANGE_LONG,AREA_CIRCLE_5,32,100,250,strength=-10,magie=30,effectOnUse="me",needRotate=False,emoji='<:butterflyV:883627142615805962>',type=TYPE_DAMAGE,message="{0} demande à son papillon d'empoisonner {1} :",use=MAGIE)
dtsword = weapon("Épée de Détermination","bd",RANGE_MELEE,AREA_CIRCLE_1,65,85,500,25,endurance=10,charisma=-10,intelligence=-15,resistance=10,emoji='<:dtSword:884802145239588884>',affinity=ELEMENT_NEUTRAL,effectOnUse=incur[2])
magicSword = weapon("Épée de MagicalGirl","be",RANGE_MELEE,AREA_CIRCLE_1,80,70,200,-10,endurance=10,charisma=20,resistance=10,precision=-10,emoji="<:magicSword:885241611682975744>",use=CHARISMA)
lunarBonk = weapon("Bâton Lunaire","bf",RANGE_MELEE,AREA_CIRCLE_1,65,85,250,-20,20,0,0,-10,20,10,emoji="<:lunarBonk:887347614448746516>",use=MAGIE,affinity=ELEMENT_LIGHT)
rapiere = weapon("Rapière en argent","bg",RANGE_DIST,AREA_CIRCLE_3,63,60,0,magie=30,precision=-10,strength=20,endurance=-15,percing=10,resistance=-15,use=MAGIE,emoji='<:bloodyRap:887328737614524496>',effectOnUse="mx")
fauc = weapon("Faux Tourmentée","bh",RANGE_MELEE,AREA_CIRCLE_2,69,75,0,40,10,percing=10,agility=-20,charisma=-20,emoji='<a:akifauxgif:887335929650507776>',affinity=ELEMENT_DARKNESS,effectOnUse=incur[2])
serringue = weapon("Serringue","bi",RANGE_DIST,AREA_CIRCLE_3,35,100,350,0,0,20,0,0,10,10,-20,emoji='<:seringue:887402558665142343>',target=ALLIES,type=TYPE_HEAL,use=CHARISMA,affinity=ELEMENT_LIGHT,message="{0} fait une perfusion à {1}")
bigshot = weapon("[[Big shot](https://www.youtube.com/watch?v=-8p8VowCmgE)]","bj",RANGE_DIST,AREA_CIRCLE_4,63,60,1997,20,-20,0,0,0,10,0,10,emoji='<:bigshot:892756699277037569>',message="{0} PROPOSE UN [[Big shot](https://www.youtube.com/watch?v=-8p8VowCmgE)] À {1} :",area=AREA_LINE_2)
nemefaux = weapon("Faux vangeresse","bk",RANGE_MELEE,AREA_CIRCLE_2,64,70,500,20,10,-10,0,-5,0,5,0,0,0,emoji='<:avengerScythe:893227827942522951>',area=AREA_ARC_1)
waterspell = weapon("Grimoire de l'eau","bl",RANGE_LONG,AREA_CIRCLE_4,73,60,350,-20,-10,10,0,20,20,emoji='<:waterspellbook:892963508248002590>',affinity=ELEMENT_WATER,message="{0} projète un éclat de glace sur {1} :",use=MAGIE)
earthspell = weapon("Grimoire des terres","bm",RANGE_MELEE,AREA_CIRCLE_2,86,60,350,-20,20,0,-10,0,15,15,emoji='<:earthspellbook:892963483665174578>',affinity=ELEMENT_EARTH,use=MAGIE,message="{0} fait apparaitre des pics rocheux sous {1} :")
airspell = weapon("Grimoire des vents","bn",RANGE_MELEE,AREA_CIRCLE_2,17,70,350,-20,20,0,-10,0,15,15,emoji='<:airspellbook:892963551159922718>',affinity=ELEMENT_AIR,use=MAGIE,area=AREA_ARC_1,message="{0} forme des vents violents autour de {1}",repetition=3)
airsword = weapon("Épée des vents","bo",RANGE_MELEE,AREA_CIRCLE_1,70,70,350,-20,0,0,30,20,-10,emoji='<:airsword:892963581031772170>',repetition=1,affinity=ELEMENT_AIR,area=AREA_ARC_2,use=STRENGTH,message="{0} file comme le vent !")
armilame = weapon("Épée empoisonnée","bp",RANGE_MELEE,AREA_CIRCLE_1,58,75,350,-20,15,magie=20,resistance=15,charisma=-10,emoji='<:amirlame:894643896120918107>',effectOnUse="me",use=MAGIE)
shehisa = weapon("Faux des ombres","bq",RANGE_MELEE,AREA_CIRCLE_1,74,75,350,30,10,-20,intelligence=-10,magie=10,emoji='<:shefaux:896924311221305395>',effectOnUse='mx')
machinist = weapon("Canon du machiniste fantaisiste","br",RANGE_LONG,AREA_CIRCLE_4,63,60,350,strength=20,magie=-30,resistance=-10,precision=20,agility=10,percing=10,area=AREA_LINE_2,emoji='<:mach:896924290170093580>')
ironSword = weapon("Épée en fer","bs",RANGE_MELEE,AREA_CIRCLE_1,81,60,350,strength=20,endurance=20,resistance=10,agility=-20,precision=-20,critical=10,emoji='<:ironSword:899994609504092171>',area=AREA_ARC_1)
darkSpellBook = weapon("Grimoire des ténèbres","bt",RANGE_DIST,AREA_CIRCLE_4,35,100,350,magie=30,strength=-20,endurance=-10,intelligence=20,effectOnUse="mw",affinity=ELEMENT_DARKNESS,use=MAGIE,emoji='<:darkspellbook:892963455773048914>')
lightSpellBook = weapon("Grimoire de la lumière","bu",RANGE_DIST,AREA_CIRCLE_4,35,100,350,charisma=30,intelligence=20,strength=-20,precision=-20,magie=10,effectOnUse="mt",type=TYPE_HEAL,use=CHARISMA,target=ALLIES,emoji='<:lightspellbook:892963432222036018>',affinity=ELEMENT_LIGHT)
musical = weapon("Détubeur Musical",'bv',RANGE_LONG,AREA_CIRCLE_5,26,50,1,strength=-15,intelligence=35,repetition=3,use=INTELLIGENCE,emoji='<:musicalGoo:901851887291215933>')
gwenCoupe = weapon("Ciseaux de la poupée","bw",RANGE_MELEE,AREA_CIRCLE_1,10,60,price=1,repetition=5,area=AREA_CONE_2,magie=30,resistance=20,charisma=-10,endurance=20,negativeIndirect=20,strength=-30,emoji='<:gwencoupecoupe:902912449261473875>',effect="ob",use=MAGIE)
inkbrella2 = weapon("Para-Encre alt.","bx",RANGE_MELEE,AREA_CIRCLE_1,32,45,price=472,endurance=20,resistance=15,strength=-25,precision=-20,intelligence=20,repetition=3,use=INTELLIGENCE,effect='ok',emoji='<:heroInkBrella:905282148917993513>',needRotate=False)
concentraceurZoom = weapon("Concentraceur Zoom","bz",RANGE_LONG,AREA_CIRCLE_6,51,60,1,strength=20,endurance=-20,precision=30,agility=-10,area=AREA_LINE_2,emoji='<:splatterscope:905283725036757002>')
klikliSword = weapon("Épée vengeresse","ca",RANGE_MELEE,AREA_CIRCLE_1,53,65,1,repetition=2,emoji='<:KlikliSword:907300288531169340>',strength=30,endurance=20,resistance=20,magie=-30,charisma=-10,intelligence=-10)

weapons = [musical,gwenCoupe,inkbrella2,concentraceurZoom,klikliSword,
    darkSpellBook,lightSpellBook,ironSword,machinist,shehisa,armilame,airsword,waterspell,earthspell,airspell,nemefaux,bigshot,serringue,fauc,rapiere,lunarBonk,magicSword,dtsword,butterflyP,butterflyR,depha,legendarySword,spellBook,mic,butterfly,dualJetSkelcher,squiffer,flexi,splatling,dualies,clashBlaster,hourglass1Weap,plume,mainLibre,splattershotJR,splattershot,roller,splatcharger,miniBrush,inkbrella,blaster,jetSkelcher,kcharger,HunterRiffle,firework]

# Skill
soupledown = skill("Choc Ténébreux","zz",TYPE_DAMAGE,500,140,range = AREA_CIRCLE_1,conditionType=["exclusive","aspiration",POIDS_PLUME],area = AREA_CIRCLE_2,sussess=70,ultimate=True,cooldown=4,emoji='<:darkdown:892350717384347648>',use=STRENGTH)
inkarmor = skill("Armure d'Encre","zy",TYPE_ARMOR,250,ultimate=True,effect="la",emoji = '<:inkArmor:866829950463246346>',area=AREA_ALL_ALLIES,cooldown=4,range=AREA_MONO)
coffeeSkill = skill("Suprématie du café","zx",TYPE_BOOST,500,effect=["lb","mc"],use=CHARISMA,conditionType=["reject","skill","zw"],area=AREA_ALL_ALLIES,emoji='<:coffee:867538582846963753>',cooldown=4,message="{0} prend le café avec ses alliés :")
theSkill = skill("Liberté du thé","zw",TYPE_BOOST,500,effect=["lc","mc"],use=CHARISMA,conditionType=["reject","skill","zx"],area=AREA_ALL_ALLIES,emoji='<:the:867538602644602931>',cooldown=4,message="{0} prend le thé avec ses alliés :")
gpotion = skill("Potion tonifiante","zv",TYPE_BOOST,200,emoji="<:bpotion:867165268911849522>",use=INTELLIGENCE,cooldown=3,effect="le",area=AREA_MONO,range=AREA_MONO)
bpotion = skill("Potion étrange","zu",TYPE_MALUS,200,cooldown=3,effect="lf",emoji="<:dpotion:867165281617182760>",use=INTELLIGENCE,area=AREA_CIRCLE_1,message="{0} lance une {1} sur {2}")
zelian = skill("R","zt",TYPE_INDIRECT_REZ,250,cooldown=5,effect="lj",emoji='<:chronoshift:867872479719456799>',use=None)
courage = skill("Motivation","zs",TYPE_BOOST,500,emoji ='<:charge:866832551112081419>',area=AREA_CIRCLE_2,use=CHARISMA,effect="lk",cooldown=3,range=AREA_MONO)
nostalgia = skill("Nostalgie","zr",TYPE_MALUS,500,emoji='<:nostalgia:867162802783649802>',effect="lm",cooldown=3,use=INTELLIGENCE)
draw25 = skill("Stop attacking or draw 25","zq",TYPE_MALUS,300,25,emoji="<:draw25:869982277701103616>",use=None,effect="lq",cooldown = 3,area=AREA_ALL_ENNEMIES,range=AREA_MONO,ultimate=True,conditionType=["exclusive","aspiration",PREVOYANT],message="{0} utilise sa carte joker !")
siropMenthe = skill("Neutralité du Sirop de Menthe","zp",TYPE_BOOST,500,effect=["lu","mc"],use=CHARISMA,area=AREA_ALL_ALLIES,emoji='<:menthe:867538622797054042>',cooldown=2,message="{0} prend un sirop de menthe avec ses alliés :")
unHolly = skill("Truc pas catho","zo",TYPE_MALUS,69,emoji='<:bravotakei:877202258348113960>',effect="lw",use=CHARISMA,message="{0} ||fait des trucs pas catho à destination de|| {2} :")
chaos = skill("Chaos Chaos !","zn",TYPE_UNIQUE,1000,range=AREA_MONO,area=AREA_ALL_ENTITES,sussess=200,emoji='<a:CHAOS:762276118224961556>',cooldown=5,ultimate=True,use=None,message="PLEASE ! JUST A SIMPLE CHAOS !")
contrecoup = skill("Contre-coup","zm",TYPE_INDIRECT_DAMAGE,250,effect="ln",cooldown=2,emoji='<:aftershock:882889694269038592>',use=MAGIE)
boom = skill("Réaction en chaîne","zl",TYPE_INDIRECT_DAMAGE,250,effect="lv",cooldown=2,emoji='<:bimbamboum:873698494874017812>',use=MAGIE)
balayette = skill("Baleyette","zk",TYPE_DAMAGE,100,90,range=AREA_MONO,area=AREA_CIRCLE_1,emoji='<:baleyette:873924668963291147>',cooldown=2)
firstheal = skill("Premiers secours","zj",TYPE_HEAL,100,35,emoji="<:bandage:873542442484396073>")
cure = skill("Guérison","zi",TYPE_HEAL,250,80,cooldown=5,emoji='<:cure:873542385731244122>')
lightAura = skill("Aura de Lumière I","zh",TYPE_PASSIVE,250,effectOnSelf="ly",emoji="<:AdL:873548073769533470>")
splatbomb = skill("Bombe splash","zg",TYPE_DAMAGE,100,cooldown=2,area=AREA_CIRCLE_1,power=55,emoji='<:splatbomb:873527088286687272>',message="{0} lance une {1} sur {2} :")
explosion = skill("Explosion","zf",TYPE_DAMAGE,1000,power=300,ultimate=True,cooldown=7,area=AREA_CIRCLE_2,sussess=80,effectOnSelf="mb",use=MAGIE,emoji='<a:explosion:882627170944573471>')
explosion2 = skill("Explosion","zf",TYPE_DAMAGE,1000,0,ultimate=True,cooldown=7,area=AREA_CIRCLE_2,sussess=500,effectOnSelf="na",use=MAGIE,emoji='<a:explosion:882627170944573471>',message="{0} rassemble son mana...")
protect = skill("Orbe défensif","ze",TYPE_ARMOR,200,emoji='<:orbeDef:873725544427053076>',effect="md",cooldown=3)
poisonus = skill("Vent empoisonné","zd",TYPE_INDIRECT_DAMAGE,500,emoji='<:estabistia:883123793730609172>',effect="me",cooldown=5,area=AREA_CIRCLE_1,use=MAGIE,message="{0} propage un {1} autour de {2} :")
invocBat = skill("Invocation - Chauve-souris","zc",TYPE_INVOC,500,invocation="Chauve-Souris",emoji="<:cutybat:884899538685530163>",shareCooldown=True,use=AGILITY)
multiMissiles = skill("Multi-Missiles","zb",TYPE_INDIRECT_DAMAGE,750,range=AREA_MONO,ultimate=True,emoji='<:tentamissile:884757344397951026>',effect="mf",cooldown=3,area=AREA_ALL_ENNEMIES)
monoMissiles = skill("Mono-Missiles","za",TYPE_INDIRECT_DAMAGE,250,range=AREA_CIRCLE_7,emoji='<:monomissile:884757360193708052>',effect="mf",cooldown=2)
splashdown = skill("Choc Chromatique","yz",TYPE_DAMAGE,500,140,AREA_MONO,ultimate=True,emoji='<:splashdown:884803808402735164>',cooldown=5,area=AREA_CIRCLE_2,damageOnArmor=5)
invocCarbE = skill("Invocation - Carbuncle Emeraude","yy",TYPE_INVOC,500,invocation="Carbuncle Emeraude",emoji="<:carbuncleE:884899235332522016>",cooldown=4,range=AREA_CIRCLE_3,shareCooldown=True,use=MAGIE)
invocCarbT = skill("Invocation - Carbuncle Topaze","yx",TYPE_INVOC,500,invocation="Carbuncle Topaze",emoji="<:carbuncleT:884899263459500053>",cooldown=4,range=AREA_CIRCLE_3,shareCooldown=True,use=ENDURANCE)
invocFee = skill("Invocation - Fée Soignante","yw",TYPE_INVOC,500,0,AREA_CIRCLE_3,cooldown=4,invocation="Fée soignante",emoji="<:selene:885077160862318602>",shareCooldown=True,use=CHARISMA)
thinkSkill = skill("Réfléchis !","yv",TYPE_BOOST,250,0,emoji="<:think:885240853696765963>",effect="mh",use=CHARISMA,cooldown = 3)
descart = skill("Je pense donc je suis","yu",TYPE_BOOST,250,range=AREA_MONO,emoji="<:descartes:885240392860188672>",effect='mi',cooldown=4,use=None,message="{0} a trouvé le sens de la vie !")
trans = skill("Transcendance","yt",TYPE_UNIQUE,0,initCooldown=3,cooldown=5,emoji="<:limiteBreak:886657642553032824>",description="Un sort particulier qui a un effet différent en fonction de l'aspiration du lanceur\n\nUtiliser Transcendance vous empêche d'utiliser une compétence ultime lors du prochain tour",use=HARMONIE,shareCooldown=True)
burst = skill("Bombe ballon","ys",TYPE_DAMAGE,0,35,area=AREA_CIRCLE_1,sussess=60,emoji='<:burstBomb:887328853683474444>',use=HARMONIE)
lapSkill = skill("Invocation - Lapino","yr",TYPE_INVOC,0,invocation="Lapino",cooldown=4,shareCooldown=True,emoji='<:lapino:885899196836757527>',use=CHARISMA)
adrenaline = skill("Adrénaline","yq",TYPE_HEAL,250,cure.power,cooldown=5,emoji='<:adrenaline:887403480933863475>',use=INTELLIGENCE)
blindage = skill("Blindage","yp",TYPE_BOOST,350,0,AREA_MONO,effect="mj",cooldown=3,use=None,emoji="<:blindage:897635682367971338>")
secondWind = skill("Second Souffle","yo",TYPE_HEAL,350,150,AREA_MONO,emoji='<:secondWind:897634132639756310>',cooldown=99,use=ENDURANCE)
isolement = skill("Isolement","yn",TYPE_ARMOR,500,0,AREA_MONO,emoji='<:selfProtect:887743151027126302>',cooldown=5,effect="ml")
bombRobot = skill("Invocation - Bombe Robot","ym",TYPE_INVOC,500,0,AREA_CIRCLE_3,invocation="Bombe Robot",cooldown=2,shareCooldown=True,emoji='<:autobomb:887747538994745394>',use=STRENGTH)
linx = skill("Œuil de Linx","yl",TYPE_BOOST,500,range=AREA_MONO,area=AREA_CIRCLE_2,emoji='<:noeuil:887743235131322398>',effect="mm",cooldown=4)
stalactic = skill("Stalactite","yk",TYPE_DAMAGE,300,60,emoji='<:stalactit:889089667088142346>',cooldown=3,sussess=60,range=AREA_DIST_5)
uppercut = skill("Uppercut","yj",TYPE_DAMAGE,200,70,AREA_CIRCLE_1,emoji='<:uppercut:889091033718194196>',cooldown=2,message="{0} donne un {1} à {2} :")
oneforall = skill("Un pour tous","yi",TYPE_BOOST,500,range=AREA_MONO,area=AREA_DONUT_2,cooldown=5,use=CHARISMA,effect="mo",effectOnSelf="mp",description="Une compétence qui permet d'augmenter les résistances de ses alliés au détriment des siennes",conditionType=["exclusive","aspiration",ALTRUISTE],emoji='<:oneforall:893295824761663488>')
secondSun = skill("Le second Soleil","yh",TYPE_MALUS,350,0,AREA_MONO,area=AREA_ALL_ENNEMIES,cooldown=5,effect="mq",emoji='<:iwanttosleeppls:893241882484817920>',use=CHARISMA,conditionType=["exclusive","element",ELEMENT_LIGHT])
kiss = skill("Baisé divin","yg",TYPE_HEAL,69,55,AREA_DONUT_2,emoji='<:welp:893251469439008809>',message="{0} fait un gros bisou à {2} :")
onstage = skill("En scène !","yf",TYPE_BOOST,750,0,AREA_MONO,["exclusive","aspiration",IDOLE],True,effect="mr",emoji='<:alice:893463608716062760>',area=AREA_DONUT_7,use=CHARISMA,cooldown=5,message="{0} éléctrise l'ambience !")
icelance = skill("Lame glacée","ye",TYPE_DAMAGE,500,120,AREA_DIST_6,["exclusive","element",ELEMENT_WATER],True,emoji='<:emoji_47:893471252537298954>',cooldown=5,message="{0} fait appaître une lame de glace géante sous {2} :")
rocklance = skill("Lame rocheuse","yd",TYPE_DAMAGE,500,120,AREA_CIRCLE_3,["exclusive","element",ELEMENT_EARTH],True,emoji='<:emoji_46:893471231641276496>',cooldown=5,message="{0} fait appaître une lame de roche géante sous {2} :",use=MAGIE)
infinitFire = skill("Brasier","yc",TYPE_DAMAGE,500,90,AREA_DIST_5,["exclusive","element",ELEMENT_FIRE],True,emoji='<:emoji_44:893471208065101924>',cooldown=5,message="{0} déclanche un brasier autour de {2} :",area=AREA_LINE_3,use=MAGIE)
storm = skill("Ouragan","yb",TYPE_DAMAGE,500,90,AREA_CIRCLE_2,["exclusive","element",ELEMENT_AIR],True,emoji='<:emoji_44:893471179023732809>',cooldown=5,message="{0} déclanche un ouragan autour de {2} :",area=AREA_CIRCLE_2,use=MAGIE)
innerdarkness = skill("Ténèbres intérieurs","ya",TYPE_INDIRECT_DAMAGE,500,0,conditionType=["exclusive","element",ELEMENT_DARKNESS],ultimate=True,emoji='<:emoji_48:893471268957990982>',cooldown=5,effect="ms",use=MAGIE,area=AREA_CIRCLE_1)
divineLight = skill("Lumière divine",'xz',TYPE_INDIRECT_HEAL,500,conditionType=["exclusive","element",ELEMENT_LIGHT],ultimate=True,emoji='<:emoji_49:893471282815963156>',cooldown=5,effect=["mu","mv"],use=CHARISMA,area=AREA_CIRCLE_1)
swordDance = skill("Dance des sabres","xy",TYPE_DAMAGE,350,power=70,use=STRENGTH,emoji='<:sworddance:894544710952173609>',cooldown=3,area=AREA_CIRCLE_1)
shot = skill("Tir net","xx",TYPE_DAMAGE,350,75,AREA_CIRCLE_6,emoji='<:shot:894544804321558608>',cooldown=3,use=STRENGTH,damageOnArmor=1.5)
percingLance = skill("Lance Perçante","xw",TYPE_DAMAGE,350,power=70,emoji='<:percing:894544752668708884>',cooldown=3,area=AREA_LINE_2,range=AREA_CIRCLE_2)
percingArrow = skill("Flèche Perçante","wv",TYPE_DAMAGE,350,power=60,emoji='<:percingarrow:887745340915191829>',cooldown=3,area=AREA_LINE_2,range=AREA_DIST_5)
highkick = skill("HighKick","wu",TYPE_DAMAGE,350,power=100,range=AREA_CIRCLE_1,emoji='<:highkick:894544734759030825>',cooldown=3)
multishot = skill("Tir Multiple","wt",TYPE_DAMAGE,350,power=60,range=AREA_DIST_4,emoji='<:name:894544834780622868>',cooldown=3,area=AREA_CONE_2)
bleedingArrow = skill("Flèche Hémoragique","ws",TYPE_DAMAGE,350,35,AREA_DIST_5,effect='mx',emoji='<:bleedingarrow:894544820071178292>')
bleedingDague = skill("Dague Hémoragique","wr",TYPE_DAMAGE,350,45,AREA_CIRCLE_2,effect='mx',emoji='<:bleedingdague:894552391444234242>')
affaiblissement = skill("Affaiblissement","wq",TYPE_MALUS,350,effect="my",cooldown=3,use=INTELLIGENCE,emoji='<:affaiblissement:894544690400071750>')
provo = skill("Provocation","wp",TYPE_MALUS,350,emoji='<:supportnt:894544669793476688>',effect='mz',cooldown=3,use=INTELLIGENCE)
flameche = skill("Flamèche","wo",TYPE_DAMAGE,100,35,area=AREA_CONE_2,use=MAGIE,conditionType=["exclusive","element",ELEMENT_FIRE],emoji='<:flame1:897811975675969556>')
flame = skill("Flamme","wn",TYPE_DAMAGE,250,55,area=AREA_CONE_2,use=MAGIE,conditionType=["exclusive","element",ELEMENT_FIRE],cooldown=3,emoji='<:flame2:897812264185376798>')
pyro = skill("Pyrotechnie","wm",TYPE_DAMAGE,500,75,area=AREA_CONE_2,use=MAGIE,conditionType=["exclusive","element",ELEMENT_FIRE],cooldown=5,emoji='<:flame3:897812061139140651>')
ecume = skill("Ecume","wl",TYPE_DAMAGE,100,40,use=MAGIE,conditionType=["exclusive","element",ELEMENT_WATER],emoji='<:splash1:897844189184811078>')
courant = skill("Courant","wk",TYPE_DAMAGE,250,60,use=MAGIE,conditionType=["exclusive","element",ELEMENT_WATER],cooldown=3,emoji='<:splash2:897844205198659594>')
torant = skill("Torrant","wd",TYPE_DAMAGE,500,80,use=MAGIE,conditionType=["exclusive","element",ELEMENT_WATER],cooldown=5,emoji='<:splash3:897844380491202581>')
brise = skill("Brise","wj",TYPE_DAMAGE,100,35,use=MAGIE,conditionType=["exclusive","element",ELEMENT_AIR],area=AREA_CIRCLE_1,emoji='<:wind1:897845097775915038>')
storm2 = skill("Tempête","wi",TYPE_DAMAGE,250,55,use=MAGIE,conditionType=["exclusive","element",ELEMENT_AIR],area=AREA_CIRCLE_1,cooldown=3,emoji='<:wind2:897845144299110441>')
tornado = skill("Tornade","wh",TYPE_DAMAGE,500,75,use=MAGIE,conditionType=["exclusive","element",ELEMENT_AIR],area=AREA_CIRCLE_1,cooldown=5,emoji='<:wind3:897845187940868156>')
stone = skill("Caillou","wg",TYPE_DAMAGE,100,40,use=MAGIE,conditionType=["exclusive","element",ELEMENT_EARTH],emoji='<:rock1:897846015552532531>')
rock = skill("Rocher","wf",TYPE_DAMAGE,250,60,use=MAGIE,conditionType=["exclusive","element",ELEMENT_EARTH],cooldown=3,emoji="<:rock2:897846028512944138>")
mont = skill("Montagne","we",TYPE_DAMAGE,500,80,use=MAGIE,conditionType=["exclusive","element",ELEMENT_EARTH],cooldown=5,emoji='<:rock3:897846042576420874>')
stingray2 = skill("Pigmalance","wd",TYPE_DAMAGE,500,70,AREA_CIRCLE_7,ultimate=True,emoji='<:stingray:899243721378390036>',cooldown=5,area=AREA_LINE_6,sussess=70,description="Cette compétence dure **2** tours")
stingray = skill("Pigmalance","wc",TYPE_DAMAGE,500,70,AREA_CIRCLE_7,ultimate=True,emoji='<:stingray:899243721378390036>',cooldown=5,area=AREA_LINE_6,sussess=70,effectOnSelf="nb")
dark1 = skill("Cécité","wb",TYPE_DAMAGE,100,40,use=MAGIE,conditionType=["exclusive","element",ELEMENT_DARKNESS],emoji='<:dark1:899599162566410280>')
dark2 = skill("Obscurité","wa",TYPE_DAMAGE,250,60,use=MAGIE,conditionType=["exclusive","element",ELEMENT_DARKNESS],cooldown=3,emoji='<:dark2:899599147399807006>')
dark3 = skill("Pénombre","vz",TYPE_DAMAGE,500,80,use=MAGIE,conditionType=["exclusive","element",ELEMENT_DARKNESS],cooldown=5,emoji='<:dark3:899598969930399765>')
light1 = skill("Lueur","vy",TYPE_DAMAGE,100,35,use=MAGIE,conditionType=["exclusive","element",ELEMENT_LIGHT],area=AREA_CIRCLE_1,emoji='<:light1:899598879576690689>')
light2 = skill("Éclat","vx",TYPE_DAMAGE,250,55,use=MAGIE,conditionType=["exclusive","element",ELEMENT_LIGHT],area=AREA_CIRCLE_1,cooldown=3,emoji='<:light2:899598896613969970>')
light3 = skill("Éblouissement","vw",TYPE_DAMAGE,500,75,use=MAGIE,conditionType=["exclusive","element",ELEMENT_LIGHT],area=AREA_CIRCLE_1,cooldown=5,emoji='<:light3:899599232628043787>')
derobade = skill("Dérobade","vv",TYPE_BOOST,350,0,AREA_DONUT_3,cooldown=4,effectOnSelf="nd",effect="nc",emoji='<:derobade:899788297868558337>',use=INTELLIGENCE)
ferocite = skill("Férocité","vu",TYPE_PASSIVE,200,0,emoji='<:ferocite:899790356315512852>',effectOnSelf="ne",use=None)
ironWillSkill = skill("Volontée de Fer","vt",TYPE_PASSIVE,200,0,emoji='<:ironwill:899793931762565251>',effectOnSelf="nh",use=None)
royaleGardeSkill = skill("Garde Royale","vs",TYPE_PASSIVE,200,0,emoji='<:gardeRoyale:899793954315321405>',effectOnSelf="ng",use=None)
defi = skill("Défi","vr",TYPE_PASSIVE,200,0,emoji='<:defi:899793973873360977>',effectOnSelf="nf",use=None)
dissimulation = skill("Dissimulation","vq",TYPE_PASSIVE,0,effectOnSelf="nj",use=None,emoji="<:dissimulation:900083085708771349>")
bleedingTrap = skill("Piège de lacération","vp",TYPE_INDIRECT_DAMAGE,500,effect="mx",cooldown=5,area=AREA_CIRCLE_1,use=STRENGTH,message="{0} place et déclanche un {1} autour de {2} :",emoji='<:lacerTrap:900076484230774807>')
# vn already taken (Prévention)
convert = skill("Convertion","vm",TYPE_ARMOR,350,range=AREA_DONUT_5,effect="nk",cooldown=3,emoji='<:convertion:900311843938115614>')
vampirisme = skill("Vampirisme","vl",TYPE_INDIRECT_HEAL,350,range=AREA_DONUT_5,effect="no",cooldown=3,emoji='<:vampire:900312789686571018>')
heriteEstialba = skill("Héritage - Fée d'Estialba","vk",TYPE_PASSIVE,0,effectOnSelf='np',emoji='<:heriteEstialba:900318953262432306>',use=MAGIE)
heriteLesath = skill("Héritage - Famille Lesath","vj",TYPE_PASSIVE,0,effectOnSelf='ns',emoji='<:hertiteLesath:900322590168608779>')
focal = skill("Focalisation","vi",TYPE_INDIRECT_DAMAGE,1000,range=AREA_CIRCLE_3,cooldown=7,effect=["me","me","me"],effectOnSelf="me",emoji='<:focal:901852405338099793>',shareCooldown=True,use=MAGIE,description="Applique 3 effets Poison d'Estialba à la cible, mais vous en donne un également")
suppr = skill("Suppression","vh",TYPE_DAMAGE,650,100,emoji='<:suppression:889090900326744085>',cooldown=5,use=MAGIE,damageOnArmor=3,sussess=70)
revitalisation = skill("Mot revitalisant","vg",TYPE_HEAL,300,45,area=AREA_CIRCLE_1,emoji="<:revita:902525429183811655>",cooldown=2)
onde = skill("Onde","vf",TYPE_ARMOR,500,effect="nv",cooldown=4,area=AREA_CIRCLE_1,emoji='<:onde:902526595842072616>')
eting = skill("Marque Eting","ve",TYPE_INDIRECT_HEAL,350,effect="nw",emoji='<:eting:902525771074109462>')
renforce = skill("Renforcement","vd",TYPE_BOOST,500,range=AREA_DONUT_5,effect="nx",cooldown=5,description="Une compétence qui augmente la résistance d'un allié. L'effet diminue avec les tours qui passent",use=INTELLIGENCE)
steroide = skill("Stéroïdes","vc",TYPE_BOOST,500,range=AREA_DONUT_5,effect="oa",cooldown=3,area=AREA_CIRCLE_1,use=INTELLIGENCE)
renisurection = skill("Résurrection","vb",TYPE_RESURECTION,500,100,emoji='<:respls:906314646007468062>',cooldown=4,shareCooldown=True,description="Permet de ressuciter un allié (en théorie, vous vous doutez bien que c'est compliqué à tester)",use=CHARISMA)
demolish = skill("Démolition","va",TYPE_DAMAGE,650,150,AREA_CIRCLE_2,ultimate=True,cooldown=4,effect=incur[5],damageOnArmor=3,emoji='<:destruc:905051623108280330>')
contrainte = skill("Contrainte","uz",TYPE_MALUS,500,range=AREA_CIRCLE_6,effect=[incur[3],"oc"],cooldown=4,use=INTELLIGENCE)
trouble = skill("Trouble","uy",TYPE_MALUS,500,range=AREA_CIRCLE_6,effect=[incur[3],"od"],use=CHARISMA,emoji='<:trouble:904164471109468200>')
epidemic = skill("Infirmitée","ux",TYPE_MALUS,500,area=AREA_CIRCLE_5,effect=incur[2],cooldown=4,use=None,emoji='<:infirm:904164428545683457>')
croissance = skill("Croissance","uw",TYPE_BOOST,500,effect="oe",cooldown=5,description="Une compétence dont les bonus se renforce avec les tours qui passent",use=CHARISMA,range=AREA_DONUT_5,emoji='<:croissance:904164385952505886>')
destruction = skill("Météore","uu",TYPE_DAMAGE,1000,power=int(explosion.power * 1.33),ultimate=True,cooldown=7,effectOnSelf="mb",use=MAGIE,emoji='<:meteor:904164411990749194>',damageOnArmor=explosion.onArmor)
castDest = effect("Cast - Météore","nnnn",turnInit=2,silent=True,emoji=dangerEm,replique=destruction)
destruction2 = skill("Météore","uv",TYPE_DAMAGE,1000,power=0,ultimate=True,cooldown=7,effectOnSelf=castDest,use=MAGIE,emoji=destruction.emoji,message="Une ombre plane au dessus de {2}...")
infectFiole = skill("Fiole d'infection","ut",TYPE_INDIRECT_DAMAGE,350,0,effect=["oh","oi"],cooldown=3,use=INTELLIGENCE,message="{0} lance une {1} sur {2}",emoji='<:fioleInfect:904164736407597087>')
bigLaser = skill("Lasers chromanergiques - Configuration Ligne","us",TYPE_DAMAGE,0,200,emoji='<:uLaserLine:906027231128715344>',area=AREA_LINE_6,sussess=95,damageOnArmor=1.33,ultimate=True,cooldown=5,description="Après un tour de chargement, déployez des drones énergétiques qui tirent un puissant rayon coloré en ligne droite")
bigLaserRep = effect("Cast - {0}".format(bigLaser.name),"bigLaserEff",turnInit=2,silent=True,emoji=dangerEm,replique=bigLaser)
bigLaser2 = skill(bigLaser.name,"ur",bigLaser.type,750,0,area=bigLaser.area,emoji=bigLaser.emoji,effectOnSelf=bigLaserRep,ultimate=bigLaser.ultimate,cooldown=bigLaser.cooldown,message="{0} charge ses drones")
bigMonoLaser = skill("Lasers chromanergiques - Configuration Mono","uq",TYPE_DAMAGE,0,230,emoji='<:uLaserMono:906027216989716480>',area=AREA_MONO,sussess=100,damageOnArmor=1.33,ultimate=True,cooldown=5,description="Après un tour de chargement, déployez des drones énergétiques qui tirent un puissant rayon coloré sur un adversaire depuis le ciel")
bigMonoLaserRep = effect("Cast - {0}".format(bigMonoLaser.name),"bigMonoLaserEff",turnInit=2,silent=True,emoji=dangerEm,replique=bigMonoLaser)
bigMonoLaser2 = skill(bigMonoLaser.name,"up",bigMonoLaser.type,750,0,area=bigMonoLaser.area,emoji=bigMonoLaser.emoji,effectOnSelf=bigMonoLaserRep,ultimate=bigMonoLaser.ultimate,cooldown=bigMonoLaser.cooldown,message="Les drones de {0} s'envolent")
invocBat2 = skill("Invocation - Chauve-souris II","uo",TYPE_INVOC,500,invocation="Chauve-Souris II",emoji="<:cuttybat2:904369379762925608>",shareCooldown=True,use=CHARISMA,cooldown=3)
invocCarbunR = skill("Invocation - Carbuncle Rubis","un",TYPE_INVOC,500,invocation="Carbuncle Rubis",emoji="<:carbunR:904367955507314731>",shareCooldown=True,use=MAGIE,cooldown=5)
concen = skill("Concentration","um",TYPE_BOOST,price=350,effect="oj",range=AREA_MONO,area=AREA_DONUT_2,cooldown=4,use=None)
memAlice = skill("Memento - Voie de l'Ange","memAlice",TYPE_HEAL,1000,80,AREA_MONO,area=AREA_DONUT_4,cooldown=99,ultimate=True,use=CHARISMA)
memAliceCast = effect("Cast - {0}".format(memAlice.name),"aliceMementoCast",replique=memAlice,turnInit=2,silent=True)
memAlice2 = copy.deepcopy(memAlice)
memAlice2.id, memAlice2.power, memAlice2.effectOnSelf, memAlice2.message = "ul",0,memAliceCast,"{0} rassemble ses souvenirs..."
blackHole = skill("Trou noir","uk",TYPE_PASSIVE,ironWillSkill.price,effectOnSelf="ol",use=None,emoji='<:blackHole:906195944406679612>')
blackHole2 = skill("Trou noir II","uj",TYPE_BOOST,0,use=None,effect=[intargetable,"on"],effectOnSelf="om",emoji='<:blackHole2:906195979332640828>',cooldown=7,initCooldown=2,description="Augmente sensiblement les chances d'être pris pour cible par l'adversaire, tout en rendant vos alliés aux corps à corps **Inciblable** et en redirigeant une partie de leurs dégâts sur vous",area=AREA_DONUT_1,range=AREA_MONO)
fireCircle = skill("Cercle de feu","ui",TYPE_DAMAGE,350,50,AREA_DIST_5,["exclusive","element",ELEMENT_FIRE],effect='oo',area=AREA_DONUT_1,cooldown=3,use=MAGIE,emoji='<:fireCircle:906219518760747159>')
waterCircle = skill("Cercle d'eau","uh",TYPE_DAMAGE,350,35,AREA_DIST_5,["exclusive","element",ELEMENT_WATER],effect='op',area=AREA_DONUT_1,cooldown=3,use=MAGIE,emoji='<:waterCircle:906219492135276594>')
airCircle = skill("Cercle d'air","ug",TYPE_DAMAGE,350,50,AREA_CIRCLE_2,["exclusive","element",ELEMENT_AIR],effect='oq',area=AREA_DONUT_1,cooldown=3,use=MAGIE,emoji='<:airCircle:906219469200842752>')
earthCircle = skill("Cercle de terre","uf",TYPE_DAMAGE,350,35,AREA_DIST_5,["exclusive","element",ELEMENT_EARTH],effect='or',area=AREA_DONUT_1,cooldown=3,use=MAGIE,emoji='<:earthCircle:906219450129317908>')
fireShot = skill("Tir Feu","ue",TYPE_DAMAGE,350,45,area=AREA_CONE_2,cooldown=3,conditionType=["exclusive","element",ELEMENT_FIRE],range=AREA_DIST_5,emoji='<:fireShot:906219594639876116>')
waterShot = skill("Tir Eau","ud",TYPE_DAMAGE,350,60,cooldown=3,conditionType=["exclusive","element",ELEMENT_WATER],range=AREA_DIST_5,emoji='<:waterShot:906219607856119868>')
airStrike = skill("Frappe Air","uc",TYPE_DAMAGE,350,45,area=AREA_CONE_2,cooldown=3,conditionType=["exclusive","element",ELEMENT_AIR],range=AREA_CIRCLE_2,emoji='<:airStrike:906219547873386526>')
earthStrike = skill("Frappe Terre","ub",TYPE_DAMAGE,350,60,cooldown=3,conditionType=["exclusive","element",ELEMENT_EARTH],range=AREA_CIRCLE_2,emoji='<:earthStrike:906219563832709142>')
space1 = skill("Naine Blanche","ua",TYPE_DAMAGE,100,35,use=MAGIE,conditionType=["exclusive","element",ELEMENT_SPACE],area=AREA_CIRCLE_1,emoji='<:ast1:907470821679824896>')
space2 = skill("Constelation","tz",TYPE_DAMAGE,250,55,use=MAGIE,conditionType=["exclusive","element",ELEMENT_SPACE],area=AREA_CIRCLE_1,cooldown=3,emoji='<:ast2:907470855402033153>')
space3 = skill("Nébuluse","ty",TYPE_DAMAGE,500,75,use=MAGIE,conditionType=["exclusive","element",ELEMENT_SPACE],area=AREA_CIRCLE_1,cooldown=5,emoji='<:ast3:907470880676917309>')
time1 = skill("Seconde","tx",TYPE_DAMAGE,100,40,use=MAGIE,conditionType=["exclusive","element",ELEMENT_TIME],emoji='<:time1:907474383034023977>')
time2 = skill("Minute","tw",TYPE_DAMAGE,250,60,use=MAGIE,conditionType=["exclusive","element",ELEMENT_TIME],cooldown=3,emoji='<:time2:907474439854235668>')
time3 = skill("Heure","tv",TYPE_DAMAGE,500,80,use=MAGIE,conditionType=["exclusive","element",ELEMENT_TIME],cooldown=5,emoji='<:time3:907474471240216658>')
timeSp = skill("Rembobinage","tu",TYPE_HEAL,500,70,use=CHARISMA,range=AREA_MONO,area=AREA_DONUT_3,conditionType=["exclusive","element",ELEMENT_TIME],cooldown=5,ultimate=True,emoji='<:rollback:907687694476378112>')
spaceSp = skill("Pluie d'étoiles","tt",TYPE_DAMAGE,500,100,use=MAGIE,conditionType=["exclusive","element",ELEMENT_SPACE],cooldown=5,area=AREA_CIRCLE_2,ultimate=True,emoji='<:starFall:907687023140302908>')

skills = [fireCircle,waterCircle,airCircle,earthCircle,fireShot,waterShot,airStrike,earthStrike,space1,space2,space3,spaceSp,time1,time2,time3,timeSp,
    renisurection,demolish,contrainte,trouble,epidemic,croissance,destruction2,infectFiole,bigLaser2,bigMonoLaser2,invocBat2,invocCarbunR,concen,memAlice2,blackHole,blackHole2,
    renforce,steroide,focal,suppr,revitalisation,onde,eting,stingray,dark1,dark2,dark3,light1,light2,light3,derobade,ferocite,ironWillSkill,royaleGardeSkill,defi,dissimulation,bleedingTrap,convert,vampirisme,heriteEstialba,heriteLesath,flameche,flame,pyro,ecume,courant,torant,brise,storm2,tornado,stone,rock,mont,bleedingArrow,bleedingDague,swordDance,shot,percingArrow,percingLance,highkick,multishot,rocklance,infinitFire,storm,innerdarkness,divineLight,icelance,onstage,kiss,secondSun,oneforall,uppercut,stalactic,linx,bombRobot,isolement,secondWind,blindage,adrenaline,lapSkill,burst,trans,descart,thinkSkill,invocFee,invocCarbT,invocCarbE,splashdown,multiMissiles,monoMissiles,invocBat,poisonus,protect,explosion2,splatbomb,lightAura,cure,firstheal,balayette,contrecoup,boom,chaos,unHolly,soupledown,inkarmor,coffeeSkill,theSkill,gpotion,bpotion,zelian,courage,nostalgia,draw25,siropMenthe
]


# Invocations ----------------------------------
batWeap = weapon("Griffe","aaa",RANGE_MELEE,AREA_CIRCLE_1,56,100,0,emoji='<:griffe:884889931359596664>',use=AGILITY)
carbunTWeap = weapon("Griffe","aaa",RANGE_MELEE,AREA_CIRCLE_1,56,100,0,emoji='<:griffe:884889931359596664>',use=ENDURANCE)
carbunE = weapon("Coup de vent","aab",RANGE_LONG,AREA_CIRCLE_5,40,70,0,emoji='<:vent:884889843681853460>',area=AREA_CIRCLE_1,use=MAGIE)
carbunSkill = skill("Rafale","aac",TYPE_DAMAGE,0,100,area=AREA_CIRCLE_2,sussess=55,emoji='<:rafale:884889889445912577>',use=MAGIE,cooldown=4)
carbunTSKill = skill("Eclat de Topaze","aad",TYPE_DAMAGE,0,100,AREA_MONO,area=AREA_CIRCLE_2,sussess=80,cooldown=4,emoji="<:eclattopaze:884889967397056512>",use=ENDURANCE)
feeWeap = weapon("Embrassement","aae",RANGE_DIST,AREA_CIRCLE_4,30,100,0,type=TYPE_HEAL,use=CHARISMA,emoji="<:feerie:885076995522834442>",target=ALLIES,area=AREA_CIRCLE_1)
feeEffect = effect("Murmure de l'aurore","aaf",CHARISMA,type=TYPE_INDIRECT_HEAL,power=15,emoji=uniqueEmoji('<:feerie:885076995522834442>'),trigger=TRIGGER_START_OF_TURN,turnInit=2,stackable=True)
feeSkill = skill("Murmure de l'aurore","aag",TYPE_INDIRECT_HEAL,0,0,AREA_MONO,cooldown=3,area=AREA_CIRCLE_3,emoji="<:feerie:885076995522834442>",effect=feeEffect)
titWeap = weapon("Magical Bonk","aah",RANGE_MELEE,AREA_CIRCLE_3,20,70,0,0,0,0,0,0,0,0,0,0,0,repetition=3,emoji='<:magicalBonk:886669168408137749>',area=AREA_CONE_2) 
lapinoWeap = weapon("Murmure de guérison","aai",RANGE_DIST,AREA_CIRCLE_3,25,100,0,0,0,0,0,0,0,0,0,0,0,'<:defHeal:885899034563313684>',use=CHARISMA,type=TYPE_HEAL,target=ALLIES,message="{0} encourage doucement {1} :")
lapinoSkill = skill("Murmure de dévoument","aaj",TYPE_HEAL,0,50,emoji='<:defHeal:885899034563313684>',cooldown=4)
batSkill = skill("Cru-aile","aak",TYPE_DAMAGE,0,50,AREA_CIRCLE_2,emoji='<:defDamage:885899060488339456>',use=AGILITY)
autoWeap = weapon("NoneWeap","aal",RANGE_MELEE,AREA_CIRCLE_1,0,0,0,emoji="<:empty:866459463568850954>")
autoEff = effect("Explosé","aam",trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,power=9999,emoji=emojiMalus,silent=True)
autoSkill = skill("Explosion","aan",TYPE_DAMAGE,0,75,AREA_MONO,emoji='<:defDamage:885899060488339456>',area=AREA_CIRCLE_1,effectOnSelf=autoEff)
cutyBatSkill1Eff = effect("Motivé Bis","batMotivEff",stat=CHARISMA,strength=10,magie=10,charisma=10,intelligence=10)
cutyBatSkill1 = skill("Motivation de la Chauve-Souris","batMotiv",TYPE_BOOST,0,0,AREA_MONO,area=AREA_DONUT_2,use=CHARISMA,cooldown=4,effect=cutyBatSkill1Eff)
cutyBatSkill2Eff = effect("Renforcement Bis","batRenforceEff",stat=INTELLIGENCE,endurance=10,resistance=10,emoji=uniqueEmoji('<:egide:887743268337619005>'))
cutyBatSkill2 = skill("Renforcement de la Chauve-Souris","batRenforce",TYPE_BOOST,0,0,range=AREA_DONUT_5,cooldown=3,emoji='<:egide:887743268337619005>',effect=cutyBatSkill2Eff)
cutyBatSkill3Eff = effect("Echolocalisé","batEchoEff",CHARISMA,agility=-10,type=TYPE_MALUS)
cutyBatSkill3 = skill("Echolocalisation","batEcho",TYPE_MALUS,0,0,AREA_MONO,area=AREA_DONUT_5,effect=cutyBatSkill3Eff,cooldown=3)
cutyBatWeap = weapon("Onde sonore","batWeap",RANGE_DIST,AREA_CIRCLE_5,32,100,effectOnUse=incur[1],use=CHARISMA)
carbunRWeap = weapon("Griffe enflammé","rubyWeap",RANGE_MELEE,AREA_CIRCLE_1,56,100,use=MAGIE,emoji=batWeap.emoji)
carbunRSkill1 = skill("Pyrotechnie du Carbuncle","rubySkill",TYPE_DAMAGE,0,70,AREA_CIRCLE_2,cooldown=3,use=MAGIE)
curbunRSkill2Eff = effect("Flamme éternelle","fire",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=25,lvl=2,turnInit=2)
carbunRSkill2 = skill("Flammes éternelles","rubySkill2",TYPE_DAMAGE,0,50,AREA_CIRCLE_3,effect=curbunRSkill2Eff,cooldown=3)

batInvoc = invoc("Chauve-Souris",aspiration=TETE_BRULE,strength=[PURCENTAGE,0.5],endurance=[PURCENTAGE,0.3],charisma=[PURCENTAGE,0.5],agility=[PURCENTAGE,0.7],precision=[PURCENTAGE,0.7],intelligence=[PURCENTAGE,0.5],magie=[PURCENTAGE,0.5],resistance=20,percing=0,critical=30,icon=["<:bat1:884519906819862568>","<:bat2:884519927208357968>"],gender=GENDER_FEMALE,weapon=batWeap,description="Une invocation de mêlée peu resistante, mais sans temps de rechargement",skill=[batSkill],element=ELEMENT_AIR)
carbuncleE = invoc("Carbuncle Emeraude",[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.7],20,10,[PURCENTAGE,2],TETE_BRULE,["<:ce1:884889724114841610>","<:ce2:884889693374775357>"],carbunE,[carbunSkill],description="Une invocation utilisant des compétences de zone pour vaincre des groupes d'ennemis de loin",element=ELEMENT_AIR)
carbuncleT = invoc("Carbuncle Topaze",[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.1],0,10,PROTECTEUR,["<:ct1:884889748274028666>","<:ct2:884889807111749662>"],carbunTWeap,[carbunTSKill],description="Une invocation résistante qui n'a pas froid au yeux et viendra sauter dans la mêlée",element=ELEMENT_EARTH)
feeInv = invoc("Fée soignante",[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.7],10,0,0,ALTRUISTE,["<:fee1:885076945333805086>","<:fee2:885076961695760386>"],feeWeap,[feeSkill],gender=GENDER_FEMALE,description="Une fée qui soigne ses alliés grace à sa magie curative",element=ELEMENT_LIGHT)
titania = invoc("Titania",[HARMONIE],[HARMONIE],[PURCENTAGE,1],[PURCENTAGE,1],[PURCENTAGE,1],[PURCENTAGE,1],[PURCENTAGE,0.5],25,10,25,OBSERVATEUR,["<:tita1:886663550796431390>","<:tita2:886663565220651028>"],titWeap,[],GENDER_FEMALE,ELEMENT_AIR)
lapino = invoc("Lapino",[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.3],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.5],10,0,0,ALTRUISTE,['<:lapino1:885899366966112266>','<:lapino2:885899382539571221>'],lapinoWeap,[lapinoSkill,eting],description="Fidèle Lapino d'Hélène, il la suit partout là où elle aura besoin de lui",element=ELEMENT_LIGHT)
autoBomb = invoc("Bombe Robot",[PURCENTAGE,0.8],50,0,0,0,0,0,20,0,0,INVOCATEUR,["<:auto1:887747795497394267>","<:auto2:887747819866312735>"],autoWeap,[autoSkill])
darkness = invoc("Conviction des Ténèbres",0,-25,0,0,0,0,0,0,0,0,INVOCATEUR,['<:infiniteDarkness:898497770531455008>','<:infiniteDarkness:898497770531455008>'],autoWeap,gender=GENDER_FEMALE,element=ELEMENT_DARKNESS)
cutyBat = invoc("Chauve-Souris II",strength=[PURCENTAGE,0.5],endurance=[PURCENTAGE,0.3],charisma=[PURCENTAGE,0.7],agility=[PURCENTAGE,0.7],precision=[PURCENTAGE,0.5],intelligence=[PURCENTAGE,0.7],magie=[PURCENTAGE,0.5],resistance=[PURCENTAGE,1],percing=0,critical=0,aspiration=IDOLE,icon=['<:bat2B:904368975952085012>','<:bat2R:904368991710101515>'],weapon=cutyBatWeap,skill=[cutyBatSkill1,cutyBatSkill2,cutyBatSkill3],gender=GENDER_FEMALE,description="Une chauve-souris spécialisée dans le soutiens")
carbunR = invoc("Carbuncle Rubis",strength=[PURCENTAGE,0.5],endurance=[PURCENTAGE,0.7],charisma=[PURCENTAGE,0.5],agility=[PURCENTAGE,0.7],precision=[PURCENTAGE,0.7],intelligence=[PURCENTAGE,0.5],magie=[PURCENTAGE,0.7],resistance=[PURCENTAGE,1],percing=[PURCENTAGE,1],critical=25,aspiration=POIDS_PLUME,icon=['<:carbunRB:904368034200834089>','<:carbunRR:904368049547776010>'],weapon=carbunRWeap,skill=[carbunRSkill1,carbunRSkill2],description="Un carbuncle de mêlée",element=ELEMENT_FIRE)

invocTabl = [darkness,autoBomb,lapino,titania,feeInv,carbuncleT,carbuncleE,batInvoc,cutyBat,carbunR]

# Stuff
uniform = stuff("Uniforme Scolaire","hd",1,100,intelligence=5,magie=5,charisma=10,emoji='<:uniform:866830066008981534>',orientation=[None,BOOSTER],affinity=ELEMENT_WATER)
blueSnekers = stuff("Tennis Montantes Bleues","he",2,100,agility=10,endurance=5,charisma=5,emoji='<:blueHotTop:866795241721954314>')
redSnekers = stuff("Tennis Montantes Rouge","hg",2,100,strength=10,endurance=5,resistance=5,emoji='<:redHopTop:866782609464098887>')
encrifuge = stuff("Tenue Encrifugée","hh",1,350,endurance=20,resistance=15,charisma=-10,intelligence=-15,effect="ni",emoji='<:encrifuge:871878276061212762>',orientation=[TANK])
pinkFlat = stuff("Ballerines roses","hi",2,150,charisma=20,emoji='<:pinkFlat:867158156139692042>',orientation=[DISTANCE,HEALER])
blackFlat = stuff("Ballerines noires","hj",2,150,strength=5,endurance=5,charisma=10,resistance=10,agility=-10,emoji="<:blackflat:867175685768347688>",orientation=[TANK,HEALER])
batEarRings = stuff("Clous d'oreilles chauve-souris","hk",0,150,charisma=10,percing=10,emoji="<:batearrings:867159399395098634>",orientation=[DISTANCE,DPT],position=1,affinity=ELEMENT_NEUTRAL)
ironHelmet = stuff("Casque en fer","hl",0,200,endurance=10,resistance=10,emoji="<:helmet:867158650488225792>",orientation=[TANK])
determination = stuff("Détermination","hm",0,500,10,effect="lg",emoji='<:determination:867894180851482644>',position=2,affinity=ELEMENT_NEUTRAL)
pinkDress = stuff("Robe rose","ho",1,200,charisma=15,agility=10,strength=-5,emoji='<:pinkDress:867533070940766228>',orientation=[DISTANCE,HEALER])
oldBooks = stuff("Vieux livres","hp",0,200,intelligence=15,magie=10,agility=-15,strength=10,emoji='<:oldbooks:867533718485598208>',orientation=[DISTANCE,BOOSTER])
jeanJacket = stuff("Veste en jean","hq",1,150,5,5,5,5,emoji='<:jeanjacket:867813124697620510>',affinity=ELEMENT_NEUTRAL)
blackJeanJacket = stuff("Veste en jean noire","hr",1,150,10,10,-5,magie=-5,percing=10,emoji='<:blackjacket:867542491666579467>',orientation=[None,DPT],affinity=ELEMENT_EARTH)
whiteSneakers = stuff("Baskets Blanches","hs",2,100,agility=10,magie=10,emoji='<:whiteSneakers:867543508496023592>',orientation=[None,BOOSTER])
amethystEarRings = stuff("Boucles d'oreilles en améthyste","hw",0,200,strength=45,endurance=10,negativeDirect=-15,precision=30,percing=10,resistance=-10,negativeBoost=35,negativeHeal=35,critical=-10,emoji='<:amethystEarRings:870391874081419345>',position=1,orientation=[LONG_DIST,DPT])
anakiMask = stuff("Masque Annaki","hx",0,150,endurance=10,charisma=5,precision=10,resistance=-5,emoji='<:anakiMask:870806374009954345>',position=5)
whiteBoots = stuff("Bottines Blanches","hy",2,200,endurance=10,agility=10,resistance=5,strength=-5,emoji='<:bottinesPunkBlanche:870807353044393994>',orientation=[TANK])
mustangBoots = stuff("Bottines à lacets","hz",2,150,strength=5,agility=5,charisma=5,precision=5,emoji='<:mustangboots:870808390081851423>')
pullBrown = stuff("Pull Brun","ia",1,200,10,agility=10,resistance=5,percing=5,charisma=-10,emoji='<:pullMaron:871878275922800681>')
blackShirt = stuff("T-Shirt Noir","ib",1,50,precision=10,resistance=5,magie=5,emoji='<:tshirtNoir:871878276103159848>')
pullCamo = stuff("Pull Camouflage","ic",1,150,agility=20,resistance=10,percing=10,precision=-5,critical=-5,endurance=-10,emoji='<:pullCam:871878276090593321>',orientation=[TANK,DPT])
woodenSandals = stuff("Sandales en bois","ie",2,200,10,agility=10,resistance=5,endurance=-5,emoji="<:sandaleBois:871880746070056991>")
schoolShoes = stuff("Mocassins Scolaires","if",2,100,charisma=5,intelligence=5,magie=5,resistance=5,emoji='<:schoolShoe:871880746426593331>',orientation=[None,BOOSTER])
blackSnelers = stuff("Tennis Montantes Noires","ig",2,100,5,endurance=5,resistance=10,emoji='<:BlackHotTop:871880746422394970>',orientation=[TANK,DPT])
heartLocket = stuff("Heart Locket","ih",0,300,resistance=20,emoji='<:heartLocket:871886518753570836>',orientation=[TANK],position=2)
catEars = stuff("Oreilles de chat","ii",0,150,charisma=10,agility=10,emoji='<:catEars:871886070025957388>',orientation=[None,HEALER],affinity=ELEMENT_AIR)
batPendant = stuff("Pendantif Chauve-Souris","ij",0,200,5,5,magie=10,emoji='<:batPendant:871887272469995560>',position=2)
bikini = stuff("Tenue Provocante","ik",1,69,endurance=-15,charisma=40,resistance=-10,percing=5,emoji='<:tenueProvoquante:871889591127388201>',orientation=[LONG_DIST,HEALER])
headSG = stuff("Chapeau Squid Girl","il",0,200,strength=5,agility=10,precision=10,endurance=-5,emoji='<:headSG:874266872340680785>',orientation=[DISTANCE,DPT])
bodySG = stuff("Tunique Squid Girl","im",1,200,10,resistance=10,emoji="<:tuniqueSG:874266874299437126>",orientation=[DISTANCE,DPT])
shoeSG = stuff("Chaussures Squid Girl","in",2,200,5,agility=10,critical=5,emoji="<:shoeSG:874266873099857930>",orientation=[DISTANCE,DPT])
flum = stuff("Fleur lumineuse","io",0,150,charisma=10,effect="lz",emoji='<:flum:876079513954557952>',orientation=[None,HEALER],position=3,affinity=ELEMENT_LIGHT)
pinkShirt = stuff("Veste et jupe rose","ip",1,300,-20,charisma=25,agility=10,critical=5,emoji='<:VesteEtJupeRose:877658944045219871>',orientation=[None,HEALER])
redDress = stuff("Robe rouge et noire","iq",1,300,20,endurance=-10,percing=5,critical=5,emoji='<:gothicRednBlackDress:877665554033414217>',orientation=[DISTANCE,DPT])
pataarmor = stuff("Armure patapoulpe","ir",1,300,-10,20,-5,resistance=15,emoji='<:octoArmor:876783724237303829>',orientation=[TANK])
barrette = stuff("Barette Seiche","is",0,100,charisma=10,precision=10,emoji='<:squidBar:878718467434491934>',position=3)
squidEarRings = stuff("Boucles d'oreilles Seiche","it",0,150,charisma=15,intelligence=10,precision=-5,emoji='<:squidEarRings:878718445171126313>',orientation=[None,BOOSTER],position=1,affinity=ELEMENT_NEUTRAL)
maidDress = stuff("Robe de soubrette","iu",1,300,-10,15,10,agility=-10,resistance=15,emoji='<:maidDress:878716791789080637>',orientation=[TANK,HEALER])
maidHeels = stuff("Escarpins de soubrette","iv",2,300,charisma=20,endurance=10,agility=-20,resistance=10,emoji='<:maidHeels:878716728346050600>',orientation=[TANK,HEALER])
maidHat = stuff("Coiffe de soubrette","iw",0,200,charisma=15,endurance=10,resistance=10,strength=-10,precision=-5,emoji='<:maidHat:878716744305356812>',orientation=[TANK,HEALER])
pinkRuban = stuff("Ruban Rose","ix",0,100,charisma=20,emoji='<:pinkRuban:878718698469335060>',orientation=[DISTANCE,HEALER],position=3)
pinkSneakers = stuff("Tennis Montantes Roses","iy",2,300,charisma=20,agility=10,intelligence=10,endurance=-10,precision=-10,emoji='<:PinkHotTop:877664496737472602>',orientation=[DISTANCE,HEALER])
abobination = stuff("Claquettes chaussettes","iz",2,1,1,1,-100,1,1,1,1,1,1,1,'<:claquetteChaussette:871880745998770258>')
legendaryTunic = stuff("Tunique de Légende","ja",1,300,15,10,resistance=10,precision=-10,agility=-5,emoji='<:LegendaryTunic:880008983618912277>',orientation=[TANK,DPT],affinity=ELEMENT_LIGHT)
legendaryBoots = stuff("Bottes de Légende","jb",2,300,endurance=10,resistance=10,strength=5,agility=-5,emoji='<:LegendaryBoots:880008962852917313>',orientation=[TANK,DPT])
purpleBasket = stuff("Baskets Violettes","jc",2,50,10,10,emoji='<:BasketViolette:871880746535620618>',orientation=[TANK,DPT])
camoHat = stuff("Casquette Camouflage","jd",0,50,15,precision=25,resistance=-10,magie=-10,emoji='<:camohat:878721916570058754>',orientation=[LONG_DIST,DPT])
blueFlat = stuff("Ballerines Blues","je",2,100,magie=25,resistance=-5,emoji='<:blueflat:881209954902638602>',orientation=[DISTANCE,MAGIC])
redFlat = stuff("Ballerines Rouges","jf",2,100,20,resistance=-5,percing=5,emoji='<:redflat:881209970568364173>',orientation=[DISTANCE,DPT])
redHeels = stuff("Escarpins Rouges","jg",2,150,strength=20,resistance=-10,percing=10,emoji='<:heelsRed:881339121795215410>',orientation=[DISTANCE,DPT])
whiteHeels = stuff("Escarpins Blancs","jh",2,150,charisma=15,intelligence=15,resistance=-10,emoji='<:heelsWhite:881339137410609162>',orientation=[DISTANCE,BOOSTER])
blackHeels = stuff("Escarpins Noirs","ji",2,150,10,percing=10,endurance=10,resistance=10,agility=-20,emoji='<:heelsBlack:881339167357935616>',orientation=[TANK,DPT])
heroHead = stuff("Casque Héroïque","jj",0,250,20,-10,percing=10,emoji='<:heroicheadset:881326928802496562>',orientation=[DISTANCE,DPT])
heroBody = stuff("Veste Héroïque","jk",1,250,10,10,precision=10,magie=-10,emoji='<:herojacket:881326964328255508>',orientation=[DISTANCE,DPT])
heroShoe = stuff("Baskets Héroïques","jl",2,250,strength=10,critical=5,percing=5,emoji='<:heroshoe:881326998511833098>',orientation=[DISTANCE,DPT])
intemCharpe = stuff("Echarpe Intemporelle","jm",0,250,charisma=25,precision=-5,emoji='<:intemcharpe:882006603350568960>',orientation=[None,HEALER],position=2,affinity=ELEMENT_TIME)
intemNorak = stuff("Anorack Intemporel","jn",1,250,charisma=20,resistance=10,strength=-5,percing=-5,emoji='<:intemnorak:882006589870075944>',orientation=[DISTANCE,HEALER],affinity=ELEMENT_TIME)
intemShoe = stuff("Tennis Montantes Intemporelles","jo",2,250,charisma=30,resistance=5,percing=-15,emoji='<:intemtennis:882006616961073253>',orientation=[DISTANCE,HEALER],affinity=ELEMENT_TIME)
patacasque = stuff("Casque Patapoutre","jp",0,200,resistance=10,endurance=10,orientation=[TANK,None],emoji='<:patacasque:881334720732991529>')
patabottes = stuff("Bottes Patapoutres","jq",2,200,resistance=15,endurance=5,orientation=[TANK,None],emoji='<:pataboots:881334739183730689>')
lunettesOv = stuff("Lunettes ovales","jr",0,100,strength=10,precision=10,emoji='<:lunettesovales:881965054830997534>',orientation=[None,DPT])
masqueTub = stuff("Masque et tuba","js",0,100,resistance=10,precision=10,emoji='<:masqieTubas:881965193100406785>',orientation=[TANK,None])
casqueColor = stuff("Casque coloré","jt",0,150,charisma=15,intelligence=15,agility=-5,precision=-5,emoji="<:colorheadset:881326908149727253>",orientation=[None,BOOSTER])
blingbling = stuff("Lunettes 18 karas","ju",0,100,5,5,5,5,-5,-5,5,5,emoji='<:lunettes18kara:881965006483251263>')
legendaryHat = stuff("Exelo","jw",0,300,endurance=10,resistance=5,strength=10,agility=-5,emoji='<:excelot:882727033782812702>',orientation=[TANK,DPT])
robeDrac = stuff("Robe draconique","jv",1,250,strength=-30,endurance=15,intelligence=20,resistance=15,emoji='<:robedraco:878572815807287297>',orientation=[TANK,DPT])
robeLoliBlue = stuff("Robe Lolita Bleue","jx",1,300,-10,0,10,0,0,0,40,negativeDirect=20,emoji="<:blueLolita:884212751881363467>",orientation=[DISTANCE,MAGIC])
old = stuff("Vieux porte-clefs","jy",0,200,magie=35,negativeDirect=15,emoji='<:old:885086171754012702>',affinity=ELEMENT_WATER,position=4)
batRuban = stuff("Noeud Chauve-Souris","jz",0,0,charisma=40,intelligence=20,strength=-20,resistance=-10,percing=-10,orientation=[LONG_DIST,HEALER],emoji='<:batRuban:887328511222763593>',position=3)
FIACNf = stuff("Robe du FIACN","ka",1,0,40,10,resistance=15,agility=-20,precision=-15,magie=-10,emoji='<:FIACNF:887328531774836736>',orientation=[TANK,DPT])
FIACNh = stuff("Gilet du FIACN","kb",1,0,40,10,resistance=15,agility=-20,precision=-15,magie=-10,emoji='<:FIACNH:887328549437059172>',orientation=[TANK,DPT])
heleneDress = stuff("Robe bleue d'Hélène","kc",1,0,charisma=25,intelligence=20,strength=-20,endurance=-15,emoji='<:heleneDress:888745359365525535>',effect='mk',affinity=ELEMENT_LIGHT,orientation=[DISTANCE,HEALER])
heleneShoe = stuff("Babies bleues d'Hélène","kd",2,0,strength=-10,charisma=25,intelligence=5,emoji='<:blueBabie:887857026477207592>',orientation=[DISTANCE,HEALER])
corset = stuff("Corset d'Ordin","ke",1,500,10,0,-5,0,25,-10,emoji="<:corsetordin:887757308157886465>",orientation=[DISTANCE,None])
ggshield = stuff("Bouclier GG","kf",0,500,endurance=20,resistance=15,agility=-15,emoji='<:emoji_8:887757446658023496>',orientation=[TANK,None],position=4)
fecaShield = stuff("Bouclier Feca","kg",0,1000,-15,15,resistance=20,emoji='<:fecashield:887757399736348722>',affinity=ELEMENT_EARTH,orientation=[TANK,None],position=4)
kanisand = stuff("Sandales Kannivore","kh",2,250,agility=20,emoji="<:sandaleskannivores:887755801161240577>",affinity=ELEMENT_AIR)
tsarine = stuff("Starine","ki",0,500,resistance=15,intelligence=10,endurance=10,precision=-15,charisma=-10,effect="mk",emoji='<:tsarine:887755891913396245>',orientation=[TANK,None])
dracBoot = stuff("Bottes Draconiques","kj",2,500,-10,20,resistance=10,intelligence=10,agility=-10,emoji='<:bottesdraco:885080377234968608>',orientation=[TANK,None])
darkMaidFlats = stuff("Ballerines de soubrette des Ténèbres","kk",2,500,10,10,agility=25,resistance=10,charisma=-15,precision=-10,magie=-10,emoji='<:linaflats:890598400624586763>',orientation=[TANK,DPT],affinity=ELEMENT_DARKNESS)
darkMaidDress = stuff("Robe de soubrette des Ténèbres","kl",1,500,15,10,agility=15,resistance=15,precision=-5,charisma=-20,magie=-10,emoji="<:linadress:890598423152185364>",orientation=[TANK,DPT],affinity=ELEMENT_DARKNESS)
darkMaidPendants = stuff("Boucles d'oreilles de soubrette des Ténèbres","km",0,500,10,10,-10,25,-10,-10,resistance=5,emoji='<:linapendant:890599104902754326>',orientation=[TANK,DPT],affinity=ELEMENT_DARKNESS,position=1)
darkbabie = stuff("Babies noires","kn",2,250,20,-20,precision=20,emoji='<:bbabies:892351703230320670>',affinity=ELEMENT_DARKNESS,orientation=[DISTANCE,DPT])
krysCorn = stuff("Serre-Tête en KrysTal","ko",0,250,endurance=15,resistance=10,agility=-5,emoji='<:krysCorn:892350678620586004>',affinity=ELEMENT_EARTH)
shihuDress = stuff("Robe de matelot noire d'encre","kp",1,750,-10,0,magie=45,critical=5,negativeIndirect=20,emoji='<:shihudress:896916995948302336>',orientation=[DISTANCE,MAGIC])
shihuShoe = stuff("Babies noire d'encre","kq",2,750,-10,magie=35,critical=5,negativeIndirect=10,emoji='<:shihubabies:896914810225188895>',orientation=[DISTANCE,MAGIC])
mageDress = stuff("Coule du mage noir","kr",1,500,-20,agility=10,precision=10,magie=25,resistance=-5,emoji='<:bmage:896912954744795177>',orientation=[LONG_DIST,MAGIC])
mageShoe = stuff("Bottines de mage noir",'ks',2,500,-10,endurance=-10,magie=25,precision=15,emoji='<:bmageshoe:896913235884802090>',orientation=[LONG_DIST,MAGIC])
tankmage1 = stuff("Armure du mage de combat",'kt',1,500,-30,20,resistance=10,magie=20,emoji='<:battlemagedress:898203453824852029>',orientation=[TANK,MAGIC])
tankmage2 = stuff("Bottes du mage de combat",'ku',2,500,charisma=-20,agility=20,resistance=15,magie=15,intelligence=-10,emoji='<:battlemageboot:898203467800277032>',orientation=[TANK,MAGIC])
tankmage3 = stuff("Chapeau du mage de combat",'kv',0,500,-20,20,resistance=10,magie=10,emoji='<:battlemagehat:899698677059305482>',orientation=[TANK,MAGIC])
shihuHat = stuff("Berêt de matelot noir d'encre",'kw',0,750,magie=35,negativeIndirect=15,emoji='<:shihuhat:898231015384944640>',orientation=[DISTANCE,MAGIC])
indeci1 = stuff("Fleur du mage indécis",'kx',0,750,strength=15,magie=15,intelligence=-5,charisma=-5,emoji='<:rmhat:898206952952332299>',position=barrette.position)
indeci2 = stuff("Veste du mage indécis",'ky',1,750,strength=15,magie=15,precision=-5,agility=-5,emoji='<:rmjakect:897631127760691240>')
indeci3 = stuff("Bottes du mage indécis",'k7',2,750,strength=15,magie=15,charisma=-5,agility=-5,emoji='<:rmboots:897631140557516840>')
hyperlink = stuff("[[Hyperlink blocked]]",'kz',2,1997,35,intelligence=35,charisma=-25,magie=-25,emoji='<:blocked:897631107602841600>')
heartSphapeObject = stuff("[[Heart Shaped Object](https://deltarune.fandom.com/wiki/SOUL)]","la",1,1997,20,20,-20,0,0,20,-20,20,critical=-20,emoji=determination.emoji,affinity=ELEMENT_TIME)
vigilant1 = stuff("Echarpe Temporelle","lb",0,500,intelligence=35,charisma=-15,orientation=[None,BOOSTER],emoji='<:tempoCharpe:900148919248502894>',position=intemCharpe.position,affinity=ELEMENT_TIME)
vigilant2 = stuff("Veste Temporelle","lc",1,500,intelligence=35,strength=-15,orientation=[None,BOOSTER],emoji='<:tempoVeste:900148936088625152>',affinity=ELEMENT_TIME)
vigilant3 = stuff("Tennis Montantes Temporelles","ld",2,500,intelligence=35,magie=-15,orientation=[None,BOOSTER],emoji='<:tempoBoots:900148968808402997>')
vigilant4 = stuff("Heaume du vigilant","le",0,750,strength=-10,endurance=20,intelligence=20,magie=-20,resistance=15,charisma=-5,orientation=[TANK,BOOSTER],emoji='<:prevHead:904171171300384838>')
vigilant5 = stuff("Armure du vigilant","lf",1,750,strength=-30,endurance=30,intelligence=30,magie=-20,resistance=25,charisma=-15,orientation=[TANK,BOOSTER],emoji='<:prevArmor:904171199108628492>')
vigilant6 = stuff("Soleret du vigilant","lp",2,750,strength=-15,endurance=20,intelligence=20,magie=-15,resistance=15,charisma=-5,orientation=[TANK,BOOSTER],emoji='<:prevShoe:904171185191915590>')
lunetteDeVisee = stuff("Lunette de visée","lg",0,500,strength=25,precision=25,resistance=-10,endurance=-20,orientation=[LONG_DIST,DPT],emoji='<:emoji_47:905277620055330846>',position=fecaShield.position)
magicHeal1 = stuff("Fleur du mage blanc","lh",0,500,strength=-15,charisma=30,magie=20,intelligence=-15,affinity=ELEMENT_LIGHT,position=barrette.position)
magicHeal2 = stuff("Robe du mage blanc","li",1,500,endurance=-15,charisma=35,magie=25,resistance=-10,precision=-15,affinity=ELEMENT_LIGHT,orientation=[LONG_DIST,None])
magicHeal3 = stuff("Souliers du mage blanc","lj",2,500,strength=-15,charisma=30,magie=20,intelligence=-15,affinity=ELEMENT_LIGHT)
shehisaBody = stuff("Tenue de la tiseuse","lk",1,500,strength=35,endurance=10,resistance=10,magie=-20,critical=-5,negativeDirect=10,orientation=[TANK,DPT])
shehisaBoots = stuff("Bottes de la tiseuse","ll",2,500,strength=45,resistance=5,agility=10,critical=-10,magie=-10,negativeDirect=20)
shehisaMask = stuff("Masque de la tiseuse","lo",0,500,strength=35,intelligence=10,resistance=5,agility=-10,magie=-10,emoji='<:shiMask:901850537132171334>',negativeDirect=10,position=barrette.position)
# LP alreay taken
darkFlum = stuff("Fleur ténèbreuse","lm",0,150,magie=10,effect="nt",emoji='<:darkFlum:901849622685814814>',orientation=[None,MAGIC],position=3,affinity=ELEMENT_DARKNESS)
hockey = stuff("Masque de hockey","ln",0,250,strength=30,magie=-10,charisma=-10,percing=10,emoji='<:hockeymask:881326947597164564>',orientation=[None,DPT],position=3)
laurier = stuff("Lauriers","lq",0,650,charisma=20,strength=20,magie=-10,intelligence=-10,emoji='<:laurier:887755867271888898>')
lentille = stuff("Lentilles sans corrections","lr",0,350,intelligence=20,magie=20,emoji='<:lentilles:881965103438770176>',negativeIndirect=20)
kaviboots = stuff("Bottes Kannivore","ls",2,350,strength=20,agility=25,endurance=15,resistance=15,magie=-30,intelligence=-25,emoji='<:bottinscanivore:887755841535639562>')
purpleGlass = stuff("Monture Violette","lt",0,350,magie=20,emoji='<:monturesViolettes:881965147990663188>')
legolass = stuff("Les Lego'Lasses","lu",2,350,precision=20,strength=20,endurance=-20,emoji='<:legolasse:887755747683889234>',orientation=[DISTANCE,None])
aliceDress = stuff("Robe de scène","lv",1,1,charisma=60,intelligence=30,negativeHeal=30,negativeDirect=20,negativeShield=20,emoji='<:aliceDress:902282155474964540>',orientation="Distance - Idole")
yellowpull = stuff("Pull Jaune","lw",1,1,endurance=20,charisma=40,intelligence=20,resistance=20,strength=-30,magie=-30,negativeDirect=10,negativeIndirect=10,emoji='<:yellowPull:903595209802272798>')
blackGhoticDress = stuff("Robe Gothique Noire",'lx',1,1,magie=40,resistance=-20,negativeDirect=20,negativeIndirect=-20,emoji='<:emoji_33:903616825810636830>')
aliceShoes = stuff("Chaussures de scène","ly",2,1,charisma=40,intelligence=25,negativeIndirect=-5,negativeHeal=25,negativeShield=25,emoji='<:aliceShoe:904164849708331098>')
lightBlueFlats = stuff("Ballerines azurées","lz",2,1,strength=30,precision=35,negativeIndirect=65,negativeDirect=-45,agility=-25,orientation=[LONG_DIST,DPT],emoji='<:lbflats:905047434462396446>')
rangers = copy.deepcopy(lightBlueFlats)
rangers.name, rangers.id, rangers.emoji = "Rangers Octaling","ma","<:octoRangers:905048480861548544>"
lightBlueJacket = stuff("Veste Azurée","mb",1,1,strength=30,precision=30,endurance=10,negativeDirect=-45,negativeIndirect=75,agility=-20,orientation=[LONG_DIST,DPT],emoji='<:lbjacket:905047464820752404>')
encrifugeBoots = stuff("Bottes encrifugées","mc",2,350,endurance=25,resistance=15,negativeDirect=10,negativeIndirect=10,emoji='<:armoredBoots:905048503275892766>')

jeanCas = stuff("Casquette en jean","md",0,1,magie=10,negativeDirect=-10,emoji='<:CascJean:907386971276587018>')
pullPol = stuff("Pull polaire","me",1,1,endurance=20,charisma=20,negativeShield=20,emoji='<:NHChandail_neige1:907386973294047312>',orientation=[TANK,HEALER])
heartBask = stuff("Paire de baskets à coeur","mf",2,1,charisma=10,intelligence=10,strength=10,magie=10,critical=-20,emoji='<:NHPaire_de_baskets_c3Fur0:907386973260505109>')
mocas = stuff("Paire de mocassins","mg",2,1,strength=10,magie=10,emoji='<:NHPaire_de_mocassins1:907386974246174790>')
sandPlage = stuff("Paire de sandales de plages","mh",2,1,endurance=15,magie=15,resistance=10,strength=-10,intelligence=-10,emoji='<:NHPaire_sandalettes_de_plage1:907386973277282334>',orientation=[TANK,MAGIC])
pullHeart = stuff("Pull coeur","mi",1,1,charisma=20,intelligence=20,percing=-20,emoji='<:NHPull_c3Fur0:907386973629595729>',orientation=[None,BOOSTER])
pullJoliReve = stuff("Pull joli rêve","mj",1,1,endurance=10,agility=10,emoji='<:NHPull_joli_r3Fve1:907386973839319141>')
surveste = stuff("Surveste",'mk',1,1,precision=10,strength=10,emoji='<:NHSurveste0:907386974409732136>')
tshirMatelot = stuff("T-shirt matelot",'ml',1,1,magie=20,resistance=15,endurance=10,precision=-10,critical=-5,strength=-10,emoji='<:NHTshirt_matelot2:907386972983664661>',orientation=[TANK,MAGIC])
tshirtNoue = stuff("T-shirt noué",'mm',1,1,strength=15,resistance=10,endurance=10,magie=-15,emoji='<:NHTshirt_nou3F_devant0:907386974363615262>',orientation=[TANK,DPT])
tshirtSport = stuff("T-shirt de sport",'mn',1,1,agility=20,emoji='<:NHTshirt_sport1:907386974434893855>')
motarVeste = stuff("Veste de motard","mo",1,1,strength=25,endurance=10,resistance=10,magie=-15,agility=-10,emoji='<:NHVeste_de_motard0:907386974543945728>',orientation=[TANK,DPT])
babiesRose = stuff("Babies à ruban roses","mp",2,1,charisma=10,intelligence=10,negativeHeal=-20,negativeBoost=20,emoji='<:babieRubR:907386970966196254>',orientation=[None,HEALER])
babiesVert = stuff("Babies verts","mq",2,1,agility=15,precision=15,negativeDirect=10,emoji='<:babiesV:907386972455198750>')
carid = stuff("Casdigan","mr",1,1,endurance=10,critical=10,emoji='<:cardigan:907386965232586772>')
chemLB = stuff("Chemise azurée","ms",1,1,strength=15,precision=15,agility=-10,emoji='<:chemB:907386970668425216>')
chemV = stuff("Chemise verte","mt",1,1,strength=15,agility=15,magie=-10,emoji='<:chemCrant:907386970894893096>')
chemB = stuff("Chemise bleue","mu",1,1,magie=25,resistance=-5,emoji='<:chemFlan:907386970827788368>')
chemN = stuff("Chemise noire","mv",1,1,strength=25,endurance=20,resistance=15,agility=-20,negativeIndirect=20,emoji='<:chemN:907386972161572896>',orientation=[TANK,DPT])
chemR = stuff("Chemise rose",'mw',1,1,negativeHeal=-30,negativeDirect=10,emoji='<:chemR:907386968046985226>',orientation=[None,HEALER])
coiffeInfirmR = stuff("Coiffe d'infirmier rose","mx",0,1,negativeHeal=-20,emoji='<:coiffeInfirmR:907386964888653824>',orientation=[None,HEALER])
coiffeInfirmB = stuff("Coiffe d'infirmier bleu","my",0,1,negativeShield=-20,emoji='<:coiffeInfirmB:907386964288868373>',orientation=[None,BOOSTER])
blueNoeud = stuff("Noeud bleu",'mz',0,1,intelligence=30,negativeHeal=10,emoji='<:noeudB:907386968013418497>',orientation=[None,BOOSTER])
whiteNoeud = stuff("Noeud blanc",'na',0,1,negativeHeal=-30,negativeBoost=5,negativeShield=5,emoji='<:noeudBl:907386972505522178>',orientation=[None,HEALER])
giletShirt = stuff("Gilet avec T-shirt",'nb',1,1,endurance=10,resistance=10,magie=10,negativeIndirect=10,emoji='<:giletTshirt:907386967472365618>',orientation=[TANK,MAGIC])
LBBerer = stuff("Bêret azuré",'nc',0,1,precision=20,negativeDirect=-20,negativeIndirect=20,emoji='<:beretBleu:907386673166426187>')
starBoots = stuff("Cuissardes nébuleuse","nd",2,1,endurance=20,resistance=20,magie=35,agility=20,intelligence=5,negativeDirect=30,negativeIndirect=30,precision=-20,emoji='<:startBoots:907799882776076318>',orientation=[TANK,MAGIC])
starPull = stuff("Pull nébuleuse","ne",1,1,endurance=30,resistance=25,magie=35,charisma=12,intelligence=5,negativeHeal=25,negativeShield=25,negativeBoost=25,strength=-12,emoji='<:starsPull:907778034738811000>',orientation=[TANK,MAGIC])
starBar = stuff("Barette étoilée","nf",0,1,endurance=20,resistance=10,magie=30,precision=20,critical=5,intelligence=10,negativeHeal=40,negativeShield=35,emoji='<:startBar:907779307630391307>',orientation=[None,MAGIC])
starDress = stuff("Robe nébuleuse","ng",1,1,endurance=10,resistance=10,magie=35,negativeDirect=-35,strength=-40,negativeBoost=30,emoji='<:starDress:907799795228352544>',orientation=[None,MAGIC])
starFlats = stuff("Ballerines nébuleuses","nh",2,1,endurance=10,resistance=5,magie=20,negativeIndirect=-35,negativeDirect=-18,negativeHeal=35,negativeShield=33,emoji='<:startFlats:907778001897414766>',orientation=[None,MAGIC])
celestBronzeHat = stuff("Casque en bronze céleste","ni",0,1,strength=40,endurance=35,resistance=15,negativeDirect=-15,precision=-25,negativeHeal=35,magie=-25,orientation=[TANK,DPT])
celestBronzeArmor = stuff("Armure en bronze céleste",'nj',1,1,strength=30,endurance=35,resistance=25,negativeDirect=-20,agility=-30,negativeIndirect=30,negativeBoost=30,orientation=[TANK,DPT])
celestBronzeBoots = stuff("Bottes en bronze céleste",'nk',2,1,strength=40,endurance=35,resistance=15,negativeDirect=-15,precision=-25,negativeHeal=35,magie=-25,orientation=[TANK,DPT])
armyBoots = stuff("Bottes de l'EEv2",'nl',2,1,strength=40,endurance=10,precision=25,negativeDirect=-15,negativeIndirect=30,charisma=-15,intelligence=-25,orientation=[LONG_DIST,DPT])
armyArmor = stuff("Uniforme de l'EEv2",'nm',1,1,strength=35,endurance=15,precision=25,negativeDirect=-15,negativeIndirect=30,charisma=-15,intelligence=-25,orientation=[LONG_DIST,DPT])

stuffs = [celestBronzeHat,celestBronzeArmor,celestBronzeBoots,armyBoots,armyArmor,
    starDress,starFlats,starBar,starPull,starBoots,jeanCas,pullPol,heartBask,mocas,sandPlage,pullHeart,pullJoliReve,surveste,tshirMatelot,tshirtNoue,motarVeste,babiesRose,babiesVert,carid,chemLB,chemV,chemB,chemN,chemR,coiffeInfirmR,coiffeInfirmB,blueNoeud,whiteNoeud,giletShirt,LBBerer,
    aliceShoes,lightBlueFlats,rangers,lightBlueJacket,encrifugeBoots,lunetteDeVisee,magicHeal1,magicHeal2,magicHeal3,shehisaBody,shehisaBoots,shehisaMask,darkFlum,hockey,laurier,lentille,kaviboots,purpleGlass,legolass,aliceDress,yellowpull,blackGhoticDress,vigilant4,vigilant5,vigilant6,vigilant1,vigilant2,vigilant3,heartSphapeObject,shihuDress,shihuShoe,mageDress,mageShoe,tankmage1,tankmage2,tankmage3,shihuHat,indeci1,indeci2,indeci3,hyperlink,darkbabie,krysCorn,darkMaidDress,darkMaidFlats,darkMaidPendants,dracBoot,tsarine,kanisand,fecaShield,ggshield,corset,heleneShoe,heleneDress,FIACNf,FIACNh,batRuban,old,robeLoliBlue,legendaryHat,robeDrac,blingbling,lunettesOv,masqueTub,casqueColor,patacasque,patabottes,intemNorak,intemShoe,intemCharpe,heroHead,heroBody,heroShoe,blackHeels,whiteHeels,redHeels,redFlat,blueFlat,camoHat,purpleBasket,amethystEarRings,legendaryBoots,legendaryTunic,pinkSneakers,pinkRuban,maidHat,maidHeels,maidDress,squidEarRings,barrette,pataarmor,redDress,pinkShirt,flum,headSG,bodySG,shoeSG,bikini,batPendant,catEars,heartLocket,blackSnelers,schoolShoes,woodenSandals,abobination,pullCamo,blackShirt,pullBrown,bbandeau,bshirt,bshoes,uniform,blueSnekers,redSnekers,encrifuge,pinkFlat,blackFlat,batEarRings,ironHelmet,determination,pinkDress,oldBooks,jeanJacket,blackJeanJacket,whiteSneakers,anakiMask,whiteBoots,mustangBoots]

octoEmpty1 = stuff("placeolder","ht",0,0)
octoEmpty2 = stuff("placeolder","hu",0,0)
octoEmpty3 = stuff("placeolder","hv",0,0)

hourglassEmoji = [['<:hourglass1:872181651801772052>','<:hourglass2:872181632801603644>'],['<:hourglass1:872181651801772052>','<:hourglass2:872181632801603644>'],['<:hourglass1:872181651801772052>','<:hourglass2:872181632801603644>']]

#Effect
armor = effect("Armure d'Encre","la",INTELLIGENCE,overhealth=70,emoji=sameSpeciesEmoji('<:armor1:866828463751036929>','<:armor2:866828487038205962>'),description="Donne de l'armure à tous les alliés",trigger=TRIGGER_DAMAGE)
coffee = effect("Caféiné","lb",2,strength=10,endurance=10,reject=["mc"],description="Boost la force et l'endurance de tous les alliés",emoji=uniqueEmoji("<:coffee:867538582846963753>"))
the = effect("Théiné","lc",2,intelligence=10,magie=10,reject=["mc"],description="Boost l'agilité et la précision de tous les alliés",emoji=uniqueEmoji('<:the:867538602644602931>'))
encrifugeEff = effect("Tenue encrifugée - Armure","ld",emoji=uniqueEmoji(encrifuge.emoji), overhealth=1,turnInit=2,trigger=TRIGGER_DAMAGE)
gpEffect = effect("Potion tonifiante","le",5,5,5,5,5,5,0,5,5,5,turnInit=2,description="Vos connaissances en alchimie vous permettent de booster toutes vos statistiques pour le prochain tour")
bpEffect = effect("Potion étrange","lf",5,-5,-5,-5,-5,-5,-5,-5,-5,-5,turnInit=1,description="Vos connaissances en alchimie vous permettent de baisser toutes les statistiques d'un adversaire pendant un tour",emoji = emojiMalus)
deterEff1 = effect("Détermination","lg",emoji=uniqueEmoji(determination.emoji),turnInit=-1,description="Sur le points de mourir, votre volonté vous permet de tenir jusqu'à votre prochain tour",trigger=TRIGGER_DEATH,callOnTrigger="lh",power=1,type=TYPE_INDIRECT_REZ)
undying = effect("Undying","lh",reject=["li","lj"],turnInit=2,trigger=TRIGGER_END_OF_TURN,onTrigger=[0,9999,DAMAGE_FIXE],immunity=True,description="Vos dernières forces pour rendent insensible à toutes attaques.\nMais à la fin de votre tour, vous mourrerez, pour de bon.",callOnTrigger="li",type=TYPE_INDIRECT_DAMAGE,power=9999,ignoreImmunity=True)
onceButNotTwice = effect("Une fois mais pas deux","li",emoji=uniqueEmoji('<:notTwice:867536068110057483>'),description="La mort ne vous laissera pas filer une seconde fois",turnInit=-1,silent=True)
zelianR = effect("Chronoshift","lj",PURCENTAGE,trigger=TRIGGER_DEATH,description = "Si le porteur venait à mourir tant qu'il porte cet effet, il est réssucité avec la moitié de sa vie",emoji=[['<:chronoshift1:867877564864790538>','<:chronoshift2:867877584518905906>'],['<:chronoshift1:867877564864790538>','<:chronoshift2:867877584518905906>']],reject=["lh","li"],type=TYPE_INDIRECT_REZ,power=50)
courageE = effect("Motivé","lk",2,15,emoji=sameSpeciesEmoji('<:charge1:866832660739653632>','<:charge2:866832677512282154>'))
nostalgiaE = effect("Nostalgie","lm",5,-10,resistance=-10,emoji=emojiMalus)
afterShockDmg = effect("Contre coup","ln",MAGIE,turnInit=1,power=25,aggro=10,lvl=3,trigger=TRIGGER_DAMAGE,type=TYPE_INDIRECT_DAMAGE,emoji=sameSpeciesEmoji('<:aftershock1:882889524122898452>','<:aftershock2:882889538886852650>'))
octoshield = effect("Bouclier Octarien","lo",agility=-100,overhealth=200,emoji=armor.emoji,turnInit=-1,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR)
inkBrellaEff = effect("Toile du para-encre","lp",None,-10,agility=-10,overhealth=100,turnInit=-1,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji('<:splatbrellareverse:876079630749147196>'),description="Commencez le combat avec un peu d'armure !\nCependant, vous subirez un malus d'agilité et de force tant que celle-ci est active")
stopAttacking = effect("Stop attacking or draw 25","lq",None,trigger=TRIGGER_DEALS_DAMAGE,type=TYPE_INDIRECT_DAMAGE,power=25,emoji=emojiMalus,description="Vous jouez votre jocker !\nSi le porteur de l'état attaque, il subit 25 dégâts fixe")
poidPlumeEff = effect("Poids Plume","lr",None,trigger=TRIGGER_END_OF_TURN,silent=True,lvl=0,type=TYPE_UNIQUE,unclearable=True,turnInit=-1,emoji=uniqueEmoji(aspiEmoji[POIDS_PLUME]))
hunter = effect("Chasseur","ls",None,emoji=uniqueEmoji('<:chasseur:871097673334276096>'),trigger=TRIGGER_DEATH,type=TYPE_UNIQUE,description="Un chasseur sachant chasser sans son chien a toujours une dernière carte à jouer",turnInit=-1)
hunterBuff = effect("Hunterbuff","lt",None,critical=100,precision=500,silent=True)
menthe = effect("Mentiné","lu",INTELLIGENCE,percing=5,resistance=5,critical=10,reject=["mc"],description="Boost la résistance, la pénétration et le critique de vos alliés",emoji=uniqueEmoji('<:menthe:867538622797054042>'))
badaboum = effect("Ça fait bim bam boum","lv",MAGIE,emoji=emojiMalus,aggro=10,turnInit=2,trigger=TRIGGER_DEATH,power=100,type=TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_2)
charme = effect("Sous le charme","lw",CHARISMA,-10,resistance=-10,magie=-10,emoji=emojiMalus,description="Heu peut-être plus tard la description",type=TYPE_MALUS)
jetlag = effect("Jetlag",'jetLag',None,emoji=uniqueEmoji('<:jetlag:872181671372402759>'),silent=True,description="Le porteur de cet effet est insenssible aux sorts/armes de type \"Sablier\"")
hourglass1 = effect("Rollback","lx",None,trigger=TRIGGER_ON_REMOVE,type=TYPE_UNIQUE,emoji=hourglassEmoji,description="Lorsque l'initiateur de cet effet commence son prochain tour, le porteur récupèrera 75% des PV perdues depuis que cet effet est actif",reject=[jetlag])
lightAuraEffect = effect("Aura de Lumière I","ly",CHARISMA,turnInit=-1,power=10,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_END_OF_TURN,emoji=sameSpeciesEmoji("<:AdL1:873549174052892672>","<:AdL2:873549232601182249>"),description="Bénissez vos alliés proches et offrez leur des soins sur plusieurs tours",area=AREA_CIRCLE_2)
flumEffect = effect("Douce lueur","lz",None,power=10,turnInit=-1,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji=uniqueEmoji(flum.emoji))
dephased = effect("Déphasée","ma",None,emoji=uniqueEmoji('<a:dephasee:882042949494525973>'),description="Ailill n'aime pas affronter trop d'ennemi à la fois, ni ceux qui essaye de l'avoir de loin",type=TYPE_UNIQUE,turnInit=-1)
stuned = effect("Etourdi","mb",emoji=uniqueEmoji('<:stun:882597448898474024>'),turnInit=2,stun=True,description="L'utilisation d'un gros sort magique vous a vidé de votre énergie")
defensive = effect("Orbe défensif","md",emoji=sameSpeciesEmoji('<:orbe1:873725384359837776>','<:orbe2:873725400730202123>'),overhealth=50,description='Donne de l\'armure à un allié',stat=INTELLIGENCE,trigger=TRIGGER_DAMAGE,turnInit=1)
cafeine = effect("Désaltéré","mc",emoji=uniqueEmoji('<:cafeine:883253781024870401>'),turnInit = 4, description = "L'abus de caféine (ou théine c' est la même chose) est dangereureux pout la santé",silent=True)
estal = effect("Poison d'Estialba","me",emoji=uniqueEmoji('<:estialba:884223390804766740>'),turnInit=3,stat=MAGIE,description="Un virulant poison, faisant la sinistre renommée des fées de cette île",trigger=TRIGGER_START_OF_TURN,stackable=True,power=25,type=TYPE_INDIRECT_DAMAGE,lvl=3)
missiles = effect("Ciblé","mf",emoji=uniqueEmoji('<:tentamissile:884757344397951026>'),stat=STRENGTH,description="Au début de son tour, le ciel tombera sur la tête du Ciblé et ses alliés proches !",trigger=TRIGGER_START_OF_TURN,power=25,type=TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_1,stackable=True)
octoboum = effect("Explosion à venir !!","mg",emoji=uniqueEmoji(explosion.emoji),turnInit=3,aggro=20)
think = effect("REFLECHIS !","mh",CHARISMA,intelligence=10)
iThink = effect("Philosophé","mi",intelligence=15,magie=15,turnInit=3)
blinde = effect("Blindé","mj",resistance=35,description="Réduit les degâts subis de 35% jusqu'à votre prochain tour")
const = effect("Constitution","mk",emoji=uniqueEmoji('<:constitution:888746214999339068>'),description="Augmente de 20 les PV max de base de toute votre équipe",turnInit = -1)
isoled = effect("Isolé","ml",emoji=uniqueEmoji('<:selfProtect:887743151027126302>'),description="S'isoler mentalement pôur ne pas faire attention au dégâts",overhealth=100,stat=INTELLIGENCE,trigger=TRIGGER_DAMAGE)
nouil = effect("Œuil de Linx","mm",emoji=uniqueEmoji('<:noeuil:887743235131322398>'),precision=30,critical=10)
lostSoul = effect("Âme en peine","mn",emoji=uniqueEmoji('<:lostSoul:887853918665707621>'),turnInit=3,trigger=TRIGGER_ON_REMOVE,silent=True,type=TYPE_UNIQUE)
oneforallbuff = effect("Un pour tous - Bonus","mo",resistance=10,stat=CHARISMA,description="Vos capacités défensives sont augmentées au détriment de celle du lanceur de cette compétence",emoji=sameSpeciesEmoji('<:one4allB:905243401157476423>','<:one4allR:905243417846636555>'))
oneforalldebuff = effect("Un pour tous - Malus","mp",resistance=-33,type=TYPE_MALUS,emoji=emojiMalus,description="Vos capacités défenses sont dimunuées pour augmenter celles de vos alliés")
secondSuneff = effect("Insomnie","mq",CHARISMA,agility=-10,precision=-10,type=TYPE_MALUS,emoji=uniqueEmoji('<:MyEyes:784226383018328115>'),description="Vous êtes en train d'expérimenter la joie d'avoir un lampadaire devant une fênetre sans rideau")
onstageeff = effect("Euphorie","mr",CHARISMA,10,10,10,10,10,10,10,5,3,3,description="C'est le moment de tout donner !",emoji=uniqueEmoji(onstage.emoji))
innerdarknessEff = effect("Ténèbres intérieurs","ms",MAGIE,power=65,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:innerdarkness:902008902776938628>'))
lightspellshield = effect("Bouclier de lumière","mt",INTELLIGENCE,overhealth=10,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji(lightSpellBook.emoji))
lighteff = effect("Illuminé","mu",INTELLIGENCE,overhealth=50,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji('<:illumi1:902008944887746611>'))
lightHealeff = effect("Illuminé","mv",CHARISMA,power=50,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:illumi2:902008962134712380>'))
darkspellbookeff = effect("Eclair sombre","mw",MAGIE,power=50,area=AREA_CIRCLE_1,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji=uniqueEmoji(darkSpellBook.emoji))
hemoragie = effect("Hémoragie","mx",STRENGTH,power=25,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,turnInit=3,stackable=True,lvl=3,emoji=uniqueEmoji('<:bleeding:887743186095730708>'))
affaiEffect = effect("Affaiblissement","my",INTELLIGENCE,-10,endurance=-10,resistance=-5,type=TYPE_MALUS,emoji=emojiMalus)
stupid = effect("Provoqué","mz",INTELLIGENCE,charisma=-20,intelligence=-20,type=TYPE_MALUS,emoji=emojiMalus)
castExplo = effect("Cast - Explosion","na",turnInit=2,silent=True,emoji=dangerEm,replique=explosion)
pigmaCast = effect("Cast - Pigmalance","nb",turnInit=2,silent=True,emoji=uniqueEmoji('<:castStingray:899243733835456553>'),replique=stingray2)
derobadeBonus = effect("Dérobade - Bonus","nc",ENDURANCE,resistance=5,aggro=20,description="Un de vos alliés vous a gentiment inviter à prendre les coups à sa place",turnInit=2)
derobadeMalus = effect("Dérobade - Malus","nd",ENDURANCE,aggro=-20,description="Vous avez fuis vos responsabilitées",type=TYPE_MALUS,turnInit=2)
ferociteEff = effect("Férocité","ne",magie=10,aggro=15,resistance=10,turnInit=-1,emoji=uniqueEmoji('<:ferocite:899790356315512852>'),description="Vos grands airs augmentent les chances d'être attaqué par les ennemis",unclearable=True,reject=["nf","ng","nh","ol"])
defiEff = effect("Défi","nf",strength=10,aggro=15,resistance=10,turnInit=-1,emoji=uniqueEmoji('<:defi:899793973873360977>'),description="Vos grands airs augmentent les chances d'être attaqué par les ennemis",unclearable=True,reject=["ne","ng","nh","ol"])
royaleGarde = effect("Garde Royale","ng",intelligence=10,aggro=15,resistance=10,turnInit=-1,emoji=uniqueEmoji('<:gardeRoyale:899793954315321405>'),description="Vos grands airs augmentent les chances d'être attaqué par les ennemis",unclearable=True,reject=["nf","ne","nh","ol"])
ironWill = effect("Volontée de Fer","nh",charisma=10,aggro=15,resistance=10,turnInit=-1,emoji=uniqueEmoji('<:ironwill:899793931762565251>'),description="Vos grands airs augmentent les chances d'être attaqué par les ennemis",unclearable=True,reject=["nf","ng","ne","ol"])
encrifugeEff2 = effect("Tenue Encrifugée","ni",callOnTrigger="ld",emoji=uniqueEmoji(encrifuge.emoji),trigger=TRIGGER_START_OF_TURN,turnInit=-1,lvl=99,description="Une fois par tour, vous protège de 50 dégâts")
dissimulationEff = effect("Dissimulé","nj",strength=-15,charisma=-15,intelligence=-15,magie=-15,aggro=-10,turnInit=-1,unclearable=True,description="Vous permet de réduire les chances d'être attaqué, mais réduit vos statistiques offensives et supports",emoji=sameSpeciesEmoji("<:dissiB:900130199826497536>","<:dissiR:900130215806779433>"))
convertEff = effect("Convertion","nk",power=50,type=TYPE_BOOST,trigger=TRIGGER_AFTER_DAMAGE,stat=INTELLIGENCE,description="Lorsque le porteur de l'effet inflige des dégâts directs, **{0}**% de ces dégâts lui sont rendue en Armure\nL'Intelligence du lanceur de la compétence influ sur le pourcentage de convertion",emoji=uniqueEmoji('<:convertion:900311843938115614>'))
convertArmor = effect("Convertion - Armure","nl",type=TYPE_ARMOR,turnInit=3,emoji=uniqueEmoji('<:converted:902527031663788032>'),trigger=TRIGGER_DAMAGE)
vampirismeEff = effect("Vampirisme","no",power=66,type=TYPE_HEAL,stat=CHARISMA,trigger=TRIGGER_AFTER_DAMAGE,description="Lorsque le porteur de l'effet inflige des dégâts directs, **{0}**M de ces dégâts lui sont rendue en PV\nLe Charisme du lanceur de la compétence influ sur le pourcentage de convertion",emoji=sameSpeciesEmoji('<:vampireB:900313575913062442>','<:vampireR:900313598130282496>'))
heriteEstialbaEff = effect("Héritage - Estialba","np",turnInit=-1,unclearable=True,description="Grâce aux enseignements de Lohica, vous êtes de plus en plus rodé en terme de poison\n\nLorsque vous donnez l'effet __<:estialba:884223390804766740> Poison d'Estialba__ à un ennemi, lui confère également l'effet __<:estialba2:900329155974008863> Poison d'Estialba II__\n\n__<:estialba2:900329155974008863> Poison d'Estialba II :__ Dégâts indirects, 33% de la puissance de __<:estialba:884223390804766740> Poison d'Estialba__, ne dure qu'un tour",emoji=sameSpeciesEmoji('<:heriteEstialbaB:900318783661559858>','<:heriteEstialbaR:900318753156390962>'),reject=["ns"])
estal2 = effect("Poison d'Estialba II","nq",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=int(estal.power/3),emoji=uniqueEmoji('<:estialba2:900329155974008863>'),stackable=True)
hemoragie2 = effect("Hémoragie II","nr",STRENGTH,power=int(hemoragie.power/3),type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,stackable=True,emoji=uniqueEmoji('<:bleeding2:900329311955984456>'))
heriteLesathEff = effect("Héritage - Lesath","ns",turnInit=-1,unclearable=True,description="Grâce aux enseignements de Shehisa, vous en connaissez un peu plus sur les points faibles de vos adversaires\n\nLorsque vous donnez l'effet __<:bleeding:887743186095730708> Hémorragie__ à un ennemi, lui confère également l'effet __<:bleeding2:900329311955984456> Hémorragie II__\n\n____<:bleeding2:900329311955984456> Hémorragie II :__ Dégâts indirects, 33% de la puissance de __<:bleeding:887743186095730708> Hémorragie__, ne dure qu'un tour",emoji=sameSpeciesEmoji('<:hetiteLesathB:900322804124229642>','<:heriteLesathR:900322774202089512>'),reject=["np"])
darkFlumEff = effect("Fleur ténèbreuse","nt",turnInit=-1,description="En subissant des dégâts, applique l'effet \"Ténèbres floraux\" sur l'attaquant",emoji=uniqueEmoji(darkFlum.emoji),callOnTrigger="nu",trigger=TRIGGER_DAMAGE)
darkFlumPoi = effect("Ténèbres floraux","nu",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=darkFlumEff.emoji,power=5,stackable=True,turnInit=2,lvl=1)
ondeEff = effect("Onde","nv",INTELLIGENCE,type=TYPE_ARMOR,overhealth=35,turnInit=5,emoji=uniqueEmoji('<:onde:902526595842072616>'),trigger=TRIGGER_DAMAGE)
etingEff = effect("Marque Eting","nw",CHARISMA,power=20,turnInit=3,stackable=True,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:eting:902525771074109462>'),type=TYPE_INDIRECT_HEAL)
renforceEff = effect("Renforcé","nx",INTELLIGENCE,resistance=15,endurance=15,trigger=TRIGGER_ON_REMOVE,callOnTrigger="ny")
renforceEff2 = effect("Renforcé II","ny",INTELLIGENCE,resistance=10,endurance=10,trigger=TRIGGER_ON_REMOVE,callOnTrigger="nz")
renforceEff3 = effect("Renforcé III","nz",INTELLIGENCE,resistance=5,endurance=5)
steroideEff = effect("Stéroïde","oa",INTELLIGENCE,strength=10,magie=10)
gwenCoupeEff = effect("Brûme sacrée","ob",emoji=uniqueEmoji('<:gwenZ:902913176562176020>'),turnInit=-1,unclearable=True,description="Vous confère 15% de chance d'obtenir l'effet **Inciblable** pendant 1 tour lorsque vous commencez votre tour")
contrainteEff = effect("Contrain","oc",INTELLIGENCE,agility=-15,precision=-15,type=TYPE_MALUS)
troubleEff = effect("Troublé","od",CHARISMA,charisma=-15,intelligence=-15,type=TYPE_MALUS)
croissanceEff = effect("Bourgeon","oe",CHARISMA,strength=10,magie=10,resistance=5,trigger=TRIGGER_ON_REMOVE,callOnTrigger="of",emoji=uniqueEmoji('<:crois1:903976740869795910>'))
croissanceEff2 = effect("Jeune pousse","of",CHARISMA,strength=15,magie=15,resistance=10,trigger=TRIGGER_ON_REMOVE,callOnTrigger="og",emoji=uniqueEmoji('<:crois2:903976762726289520>'))
croissanceEff3 = effect("Joli plante","og",CHARISMA,strength=20,magie=20,resistance=15,emoji=uniqueEmoji('<:crois3:903976790530326578>'))
infection = effect("Infection","oh",INTELLIGENCE,power=15,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,lvl=2,reject=["oi"],description="Un effet infligeant des dégâts indirects\n\nL'infection se propage sur les ennemis autour du porteur lorsque l'effet se déclanche",emoji=uniqueEmoji("<:infect:904164445268369428>"),turnInit=2)
infectRej = effect("Guérison récente","oi",silent=True,turnInit=3,description="Une guérison récente empêche une nouvelle infection")
ConcenEff = effect("Concentration",'oj',redirection=35,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji('<:redirectB:905245642643877889>','<:redirectR:905245726253142106>'),turnInit=1,description="Une partie des dégâts directs reçu par le porteur de l'effet sont redirigé vers le combattant qui a donné l'effet")
inkBrella2Eff = copy.deepcopy(inkBrellaEff)
inkBrella2Eff.id, inkBrella2Eff.emoji = "ok",uniqueEmoji("<:inkBrellaAltShield:905283041155514379>")
blackHoleEff = effect("Singularité","ol",aggro=35,turnInit=-1,unclearable=True,reject=["nf","ng","ne","nh"],description="Augmente considérablement les chances d'être pris pour cible par l'adversaire",emoji='<:blackHole:906195944406679612>')
blackHoleEff2 = effect("Singularité II","om",aggro=15,reject=["ol"],description="Les chances d'être la cible des adversaires sont augmentés",emoji='<:blackHole2:906195979332640828>')
blackHoleEff3 = effect("Horizon des événements","on",redirection=50,description="Quelqu'un attire les dégâts sur lui")
fireCircleEff = effect("Foyer","oo",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=35,emoji=fireCircle.emoji)
waterCircleEff = effect("Syphon","op",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=50,emoji=waterCircle.emoji)
airCircleEff = effect("Oeuil de la tempête","oq",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=35,emoji=airCircle.emoji)
earthCircleEff = effect("Epicentre","or",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=50,emoji=earthCircle.emoji)

enchant = effect("Enchanté","na",None,turnInit=-1,silent=True,type=TYPE_UNIQUE,unclearable=True,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji(aspiEmoji[ENCHANTEUR]))
proMalus = effect("Protecteur - Malus","nb",None,strength=-20,magie=-20,type=TYPE_MALUS,silent=True,stackable=True,emoji=uniqueEmoji('<:proMalus:903137298001047573>'))
astralShield = effect("Armure Astrale","astShield",type=TYPE_ARMOR,turnInit=99,emoji=uniqueEmoji('<:astralShield:907467906483367936>'),trigger=TRIGGER_DAMAGE)
timeShield = effect("Armure Temporelle","timeShield",type=TYPE_ARMOR,turnInit=99,emoji=uniqueEmoji('<:tempoShield:907467936975945758>'),trigger=TRIGGER_DAMAGE)

effTB2 = [effect("Tête Brûlée","effTB",None,turnInit=-1,silent=True,type=TYPE_UNIQUE,unclearable=True,emoji=uniqueEmoji(aspiEmoji[TETE_BRULE]))]
effMag2 = [effect("Mage","effMage",None,turnInit=-1,silent=True,type=TYPE_UNIQUE,unclearable=True,emoji=uniqueEmoji(aspiEmoji[MAGE]))]
chaosEff = effect("Boîte à malice","chaosed",STRENGTH,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:surprise:904916065778274304>'))

effTransShield = effect("Transcendance - Armure","transArm",INTELLIGENCE,overhealth=100,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji("<a:transArmorB:900037831257358378>","<a:transArmorR:900037817449717800>"),turnInit=3)

chaosProhib = [undying,deterEff1,poidPlumeEff,dephased,cafeine,octoboum,const,lostSoul,onceButNotTwice,zelianR,octoshield]

effects = [fireCircleEff,waterCircleEff,airCircleEff,earthCircleEff,renforceEff,renforceEff2,renforceEff3,steroideEff,gwenCoupeEff,contrainteEff,troubleEff,croissanceEff,croissanceEff2,croissanceEff3,infection,infectRej,ConcenEff,inkBrella2Eff,blackHoleEff,blackHoleEff2,blackHoleEff3,convertEff,vampirismeEff,heriteEstialbaEff,estal2,hemoragie2,heriteLesathEff,darkFlumEff,darkFlumPoi,ondeEff,etingEff,encrifugeEff2,ferociteEff,defiEff,royaleGarde,ironWill,dissimulationEff,pigmaCast,derobadeBonus,derobadeMalus,castExplo,affaiEffect,stupid,hemoragie,innerdarknessEff,darkspellbookeff,lighteff,lightHealeff,lightspellshield,onstageeff,secondSuneff,oneforallbuff,oneforalldebuff,lostSoul,nouil,isoled,const,blinde,iThink,think,octoboum,missiles,estal,cafeine,defensive,stuned,flumEffect,lightAuraEffect,hourglass1,jetlag,charme,armor,coffee,the,encrifugeEff,gpEffect,bpEffect,deterEff1,undying,onceButNotTwice,zelianR,afterShockDmg,octoshield,nostalgiaE,inkBrellaEff,stopAttacking,poidPlumeEff,hunter,hunterBuff,menthe,badaboum,courageE]
hourglassEffects = [hourglass1]

#Other
changeAspi = other("Changement d'aspiration","qa",description="Vous permet de changer d'aspiration",emoji='<:changeaspi:868831004545138718>')
changeAppa = other("Changement d'apparence","qb",description="Vous permet de changeer votre genre, couleur et espèce",emoji='<:changeAppa:872174182773977108>',price=500)
changeName = other("Changement de nom","qc",description="Vous permet de changer le nom de votre personnage",emoji='<:changeName:872174155485810718>',price=500)
restat = other("Rénitialisation des points bonus","qd",description="Vous permet de redistribuer vos points bonus",emoji='<:restats:872174136913461348>',price=500)
elementalCristal = other("Cristal élémentaire","qe",500,description="Ces cristaux vous permettent de changer l'élément de votre personnage dans /inventory element (lvl 10)\n\nCe cristal permet de sélectionner les éléments suivants :\n<:fire:887847475203932261> Feu\n<:water:887847459211079760> Eau\n<:air:887847440932290560> Air\n<:earth:887847425459503114> Terre",emoji="<:krysTal:888070310472073257>")
customColor = other("Couleur personnalisée","qf",500,description="Vous permet de rentrer une couleur personnalisée pour votre personnage",emoji='<:changeColor:892350738322300958>')
seeshell = other("Super Coquillage","qd",500,description="Ce coquillage permet de changer son bonus iné dans /inventory bonus (lvl 25)")
blablator = other("Blablator","qg",500,description="Permet de définir des messages que votre personnages dira lors de certains événements")
dimentioCristal = other("Cristal dimentionel",'qh',500,'<:krysTal2:907638077307097088>',"Ces cristaux vous permettent de changer l'élément de votre personnage dans /inventory element (lvl 20)\n\nCe cristal permet de choisir les éléments suivants :\n<:light:887847410141921362> Lumière\n<:darkness:887847395067568128> Ténèbre\n<:astral:907467653147410475> Astral\n<:temporel:907467620930973707> Temporel")
others = [elementalCristal,customColor,changeAspi,changeAppa,changeName,restat,blablator,dimentioCristal]

tablAllOcta,tablAllAllies = [],[]

# Bonus iné
inkResis = effect("Pied au sec",1,emoji=uniqueEmoji('<:piedAuSec:810918749196648459>'),silent=True,turnInit=-1,description="Réduit les dégâts indirects de 20%",unclearable=True)
respawnPunish = effect("Retour Perdant",2,emoji=uniqueEmoji('<:retourPerdant:810918739637567489>'),silent=True,turnInit=-1,description="Augmente de 20% les dégâts infligés, mais augmente de 35% les dégâts reçu",unclearable=True)
speedup = effect("Course à Pied",3,emoji=uniqueEmoji('<:course:810918753197752401>'),silent=True,turnInit=-1,description="Lorsque vous êtes attaqué réduit la précision de base de l'arme de votre attaquant de 20% (Attaque en cours uniquement)",unclearable=True)
bombDefense = effect("Philtre à Explosion",4,emoji=uniqueEmoji('<:BDDX:810918653322330112>'),silent=True,turnInit=-1,description="Réduit les dégâts de zone subis sans être la cible principale de 20%",unclearable=True)
demolished = effect("Démolition",5,emoji=uniqueEmoji('<:demolition:810918751703793665>'),silent=True,turnInit=-1,description="Les dégâts infligés à l'armure sont augmentés de 20%",unclearable=True)
mpu = effect("Arme Principale +",6,emoji=uniqueEmoji('<:mainpowerup:895025631023210638>'),silent=True,turnInit=-1,description="La puissance de votre arme principale augmente de 10%",unclearable=True)
secondpu = effect("Arme Secondaire +",7,emoji=uniqueEmoji('<:subpowerup:895025042679820378>'),silent=True,turnInit=-1,description="La puissance de vos compétences directes non ultime augmente de 10%",unclearable=True)
specialpu = effect("Arme Spéciale +",8,emoji=uniqueEmoji('<:specialpowerup:895025042361049089>'),silent=True,turnInit=-1,description="La puissance de votre compétence ultime augmente de 10%",unclearable=True)
subsaver = effect("Encrémenteur Secondaire",9,emoji=uniqueEmoji('<:subinksaver:895025042042265690>'),silent=True,turnInit=-1,description="Le temps de rechargement de vos compétences non ultime est réduit de 20%",unclearable=True)
spesaver = effect("Jauge Spéciale +",10,emoji=uniqueEmoji('<:abilitycharge:895025042927259678>'),silent=True,turnInit=-1,description="Le temps de rechargement de votre compétence ultime est réduit de 25%",unclearable=True)

# Octarien
octoEm = '<:splatted1:727586364618702898>'
octoShieldWeap = weapon("Bouclier Octarien","aaa",0,AREA_CIRCLE_2,52,sussess=100,price=0,endurance=20,strength=-50,effect="lo",emoji=octoEm)
octoBallWeap = weapon("Balles rebondissantes","aaa",1,AREA_CIRCLE_3,66,30,0,repetition=3,strength=10,agility=10,emoji=octoEm)
octoSnipeWeap = weapon("Snipeur Octarien","aaa",2,AREA_CIRCLE_6,52,85,0,strength=20,emoji=octoEm)
octoFly = weapon("Machinerie volante","aaa",RANGE_DIST,AREA_CIRCLE_3,80,75,-20,10,emoji=octoEm)
octoHeal = weapon("Octo heal","aaa",1,AREA_CIRCLE_3,35,50,0,use=CHARISMA,type=TYPE_HEAL,target=ALLIES,emoji='<:medic:882890887120699444>')
octoDef = weapon('OctoDef',"aaa",1,AREA_CIRCLE_3,10,100,0,effectOnUse="md",use=INTELLIGENCE,target=ALLIES,type=TYPE_HEAL,intelligence=20)
flyfishweap = weapon("Flyfish","ffweap",2,AREA_CIRCLE_7,0,100,0,effectOnUse="mf",type=TYPE_INDIRECT_DAMAGE,strength=30)
octoBoumWeap = weapon("noneWeap","aaa",1,AREA_CIRCLE_1,0,0,0,effect="mg") 
ruddinweap = weapon("Carreaux","aaa",RANGE_DIST,AREA_CIRCLE_3,28,70,0,0,0,0,0,0,0,0,repetition=3,emoji='<:chaos:892857755143127090>')
ruddinweap2 = weapon("Carreaux","aaa",RANGE_MELEE,AREA_CIRCLE_3,28,70,0,0,0,0,0,0,0,0,repetition=3,emoji='<:chaos:892857755143127090>')
malusWeaponEff = effect("Embrouillement","aaa",INTELLIGENCE,strength=-5,magie=-5,critical=-2,type=TYPE_MALUS)
malusWeapon = weapon("Magie sombre","aaa",RANGE_DIST,AREA_CIRCLE_5,45,70,0,effectOnUse=malusWeaponEff,use=MAGIE)
malusSkill1Eff = effect("Malussé","mal",INTELLIGENCE,-15,magie=-15,resistance=-5,type=TYPE_MALUS)
malusSkill1 = skill("Abrutissement","aaa",TYPE_MALUS,0,area=AREA_CIRCLE_2,effect=malusSkill1Eff,cooldown=5,initCooldown=2)
malusSkill2 = skill("Eclair","aaa",TYPE_DAMAGE,0,50,cooldown=2,sussess=65,use=MAGIE)
kralamWeap = weapon("Décharge motivante","aaa",RANGE_DIST,AREA_DONUT_4,35,100,0,type=TYPE_HEAL,target=ALLIES,use=CHARISMA)
kralamSkillEff2 = effect("This is, my No No Square","nono",INTELLIGENCE,resistance=20,overhealth=100,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,turnInit=3)
kralamSkillEff1 = effect("No no, don't touch me there","squaez",trigger=TRIGGER_DAMAGE,callOnTrigger=kralamSkillEff2,lvl=1)
kralamSkill = skill("Prévention","vn",TYPE_BOOST,0,0,AREA_DONUT_6,cooldown=3,effect=kralamSkillEff1,emoji='<:egide:887743268337619005>')
temNativTriggered = effect("Promue",'tem',magie=0,turnInit=-1,unclearable=True,emoji=uniqueEmoji('<:colegue:895440308257558529>'))
temNativ = effect("College",'tem1',trigger=TRIGGER_ON_REMOVE,turnInit=3,unclearable=True,callOnTrigger=temNativTriggered)
temWeap = weapon("Tem life saves","aaa",RANGE_DIST,AREA_CIRCLE_5,42,75,0,use=MAGIE,effect=temNativ)
temSkill1 = skill("Alergies","aaa",TYPE_DAMAGE,0,50,use=MAGIE,initCooldown=3)
octoMageWeap = weapon("noneWeap","aaa",1,AREA_CIRCLE_1,0,0,0) 
chargeShot = skill('Tir chargé',"aaa",TYPE_DAMAGE,0,50,emoji=shot.emoji,cooldown=3,initCooldown=2)
octobomberWeap = weapon("Lance Bombe Splash",0,RANGE_LONG,AREA_CIRCLE_5,int(splatbomb.power*0.66),int(splatbomb.sussess*0.9),area=splatbomb.area,emoji=splatbomb.emoji)
tentaWeap = weapon("Double canon",0,RANGE_MELEE,AREA_CIRCLE_3,42,35,repetition=4,emoji=octoEm)
octoTour = weapon("noneWeap","aaa",RANGE_LONG,AREA_CIRCLE_1,0,0,0,resistance=500)
octoTourEff1 = effect("Grand protecteur","octTourEff1",turnInit=-1,emoji=uniqueEmoji('<:tower:905169617163538442>'),unclearable=True,description="L'octo tour protège ses alliés\nTant qu'il est en vie, celui-ci subis les dégâts directs de ses alliés à leur place")
octoTourEff2 = effect("Protection magique","octTourEff2",redirection=100,turnInit=-1,emoji=uniqueEmoji('<:tower:905169617163538442>'))
octoTourSkill = skill("Grand protecteur","octoTourSkill",TYPE_PASSIVE,0,effectOnSelf=octoTourEff1,use=None,emoji='<:tower:905169617163538442>')
veterHealSkill1 = skill("Here we go again","octoHealVet1",TYPE_RESURECTION,0,50,cooldown=4,use=CHARISMA)
veterHealSkill2 = skill("Renouvellement","octaHealVet2",TYPE_HEAL,0,80,use=CHARISMA,cooldown=4,initCooldown=2)
veterHealSkill3 = skill("I'm a healer but...","octaHealVet3",TYPE_MALUS,0,area=AREA_CIRCLE_1,effect=incur[3],cooldown=5,emoji=incur[3].emoji[0][0])
veterHealSkill4 = skill("Théorie du complot","octaHealVet4",TYPE_DAMAGE,0,50,use=CHARISMA,cooldown=2)
veterHealWeap = copy.deepcopy(octoHeal)
veterHealWeap.negativeHeal = -20

skills.append(kralamSkill)
effects.append(kralamSkillEff1)
effects.append(kralamSkillEff2)

octaStransEff = effect('Multi-Bras',"ocSt",aggro=15,resistance=10,turnInit = -1,unclearable=True,emoji=uniqueEmoji('<:octoStrans:900084603140853760>'))
octaStrans = skill("Multi-Bras","octaStrans",TYPE_PASSIVE,0,effectOnSelf=octaStransEff,emoji='<:multibras:900084714675785759>')

class octarien:
    def __init__(self,name,maxStrength,maxEndurance,maxCharisma,maxAgility,maxPrecision,maxIntelligence,maxMagie,resistance,percing,critical,weapon,exp,icon,skill=["0","0","0","0","0"],aspiration=INVOCATEUR,gender=GENDER_OTHER,description="",deadIcon=None,oneVAll = False,say=says(),baseLvl = 1):
        self.name = name
        self.species = 3
        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie = maxStrength,maxEndurance,maxCharisma,maxAgility,maxPrecision,maxIntelligence,maxMagie
        self.resistance,self.percing,self.critical = resistance,percing,critical
        self.aspiration = aspiration
        self.weapon = weapon
        self.skills = skill
        while len(self.skills) < 5:
            self.skills+=["0"]

        self.skillsInventory = []
        self.color = red
        self.level = 1
        self.stuff = [octoEmpty1,octoEmpty2,octoEmpty3]
        self.exp = exp
        self.icon = icon
        self.gender = gender
        self.description = description
        self.element = ELEMENT_NEUTRAL
        self.deadIcon = deadIcon
        self.oneVAll = oneVAll
        self.says = say
        self.baseLvl = baseLvl

    def allStats(self):
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

class tmpAllie:
    def __init__(self,name,species,color,aspiration,weapon,stuff,gender,skill=[],description="Pas de description",url="",element=ELEMENT_NEUTRAL,variant = False,deadIcon=None,icon = None,bonusPoints = [None,None],say=says()):
        self.name = name
        self.species = species
        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie = 0,0,0,0,0,0,0
        self.resistance,self.percing,self.critical = 0,0,0
        self.aspiration = aspiration
        self.weapon = weapon
        self.skills = ["0","0","0","0","0"]
        for a in range(0,len(skill)):
            self.skills[a] = skill[a]
        self.skillsInventory = []
        self.color = color
        self.level = 1
        self.stuff = stuff
        self.gender = gender
        if icon == None:
            self.icon = emoji.icon[species][getColorId(self)]
        else:
            self.icon = icon
        self.description=description
        self.url = url
        self.element = element
        self.variant = variant
        self.deadIcon = deadIcon
        self.bonusPoints = bonusPoints
        self.says = say

    def changeLevel(self,level=1):
        self.level = level
        stats = self.allStats()
        allMax = [maxStrength,maxEndur,maxChar,maxAgi,maxPreci,maxIntel,maxMagie]
        for a in range(0,len(stats)):
            stats[a] = round(allMax[a][self.aspiration]*0.1+allMax[a][self.aspiration]*0.9*self.level/50)

        bPoints = level
        for a in self.bonusPoints:
            if a != None:
                distribute = min(30,bPoints)
                bPoints -= distribute
                stats[a] += distribute

        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie = stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],stats[6]

    def allStats(self):
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

for a in [0,1]: # Octo shield
    tablAllOcta += [octarien("OctoShield",40,150,20,30,30,10,0,35,0,0,octoShieldWeap,5,'<:OctoShield:881587820530139136>',[octaStrans,blindage,isolement],description="Un octarien qui se cache derrière un gros et lourd bouclier")]

for a in [0,1,2]: # Octo shoot
    tablAllOcta += [octarien("OctoShooter",60,35,30,75,55,35,0,20,0,0,octoBallWeap,3,'<:octoshooter:880151608791539742>',[chargeShot],description="Un tireur sans plus ni moins")]

for a in [0,1]: # Octo heal
    tablAllOcta += [octarien("OctoHealer",10,30,155,25,15,15,10,15,0,30,octoHeal,4,"<:octohealer:880151652710092901>",[lightAura,cure,firstheal],aspiration=ALTRUISTE,description="Un octarien qui se spcésialise dans ~~passer son tour~~ soigner ses alliés")]

for a in [0,1,2]: # Rudinn
    tablAllOcta += [octarien("Rudinn",120,50,20,20,20,35,35,0,0,15,ruddinweap,6,"<a:rudinn:893246033226760232>",aspiration=TETE_BRULE,deadIcon='<:defeatrudeen:893246353415757824>',baseLvl=10)]

for a in [0,1]: # Rudinn Ranger
    tablAllOcta += [octarien("Rudinn Ranger",135,50,20,30,30,25,25,0,0,15,ruddinweap2,8,"<a:rudinnRanger:893248570742956072>",aspiration=POIDS_PLUME,deadIcon='<:defeatrudeen:893246353415757824>',skill=[octaStrans],baseLvl=10)]

for a in [0,1,2]: # Flyfish
    tablAllOcta += [octarien("Aéro-benne",150,20,25,50,35,35,0,10,0,0,flyfishweap,5,'<:flyfish:884757237522907236>',description="Un Salmioche qui s'est passionné pour l'aviation",deadIcon='<:salmonnt:894551663950573639>',aspiration=OBSERVATEUR,baseLvl=10)]

for a in [0,1]: # Mallus
    tablAllOcta += [octarien("Mallus",25,30,20,20,25,80,100,10,0,15,malusWeapon,6,'<:mallus:895824636716130308>',skill=[malusSkill1,malusSkill2],aspiration=PREVOYANT,baseLvl=15)]

for a in [0,1]: # Kralamour
    tablAllOcta += [octarien("Kralamour",10,50,80,30,30,80,30,20,0,0,kralamWeap,5,'<:kralamour:895443866189176842>',[kralamSkill],PREVOYANT,baseLvl=15)]

for a in [0,1,2]: # Temmie
    tablAllOcta += [octarien("Temmie",50,25,35,35,35,30,35,30,15,15,temWeap,4,'<:temmie:894546348324552724>',[temSkill1],deadIcon='<:temmient:894545999996014663>',aspiration=TETE_BRULE,say=temSays,baseLvl=15)]

for a in [0,1,2]: # Octo Mage
    tablAllOcta += [octarien("Octo Mage",50,20,30,30,30,20,100,20,10,15,octoMageWeap,5,'<:octomage:897910662758543422>',[flame,courant,rock,storm2],MAGE,baseLvl=20)]

for a in [0,1,2]: # Armored Zombie
    tablAllOcta += [octarien("Zombie",100,80,0,50,30,0,0,35,0,10,ironSword,6,'<:armoredZombie:899993449443491860>',[defi,gpotion],BERSERK,baseLvl=20)]

for a in [0,1,2]: # OctoBomber
    tablAllOcta.append(octarien("Octo Bomber",150,50,20,10,50,20,0,0,10,0,octobomberWeap,6,'<:octobomber:902013837123919924>',aspiration=OBSERVATEUR,baseLvl=20))

for a in [0,1,2]: # Tentassin
    tablAllOcta.append(octarien("Tentassin",115,55,20,35,30,20,20,20,0,10,tentaWeap,6,'<:octoshoter2:902013858602967052>',aspiration=BERSERK,skill=[octaStrans],baseLvl=15))

# Octo Protecteur
tablAllOcta += [octarien("OctoProtecteur",0,45,50,50,30,100,20,20,0,0,octoDef,5,"<:octoProtect:883303222255706142>",[inkarmor],aspiration=PREVOYANT,description="Un octarien qui pense que les boucliers sont la meilleure défense",baseLvl=5)]

# OctoBOUM
tablAllOcta += [octarien("OctoBOUM",100,-30,10,0,0,0,250,-10,0,0,octoBoumWeap,5,'<:octoboom:884810545457418271>',[explosion2],MAGE,description="Un octarien qui a placé tous ses points dans ses envies pirotechniques",baseLvl=25)]

for a in [0,1,2]: # Octaling
    tablAllOcta += [octarien("Octaling",55,35,35,35,35,35,55,20,0,20,weapons[random.randint(0,len(weapons)-1)],5,'<:Octaling:866461984018137138>',[skills[random.randint(0,len(skills)-1)],skills[random.randint(0,len(skills)-1)],skills[random.randint(0,len(skills)-1)]],baseLvl=10)]

for a in [0,1]: # OctoFly
    tablAllOcta += [octarien("Octarien Volant",100,35,35,50,50,20,0,10,0,35,octoFly,4,'<:octovolant:880151493171363861>')]

for a in [0,1,2]: # OctoHeal 2
    tablAllOcta.append(octarien("OctoHealer Vétéran",0,25,150,35,40,35,0,20,0,0,veterHealWeap,7,'<:octoHealVet:906302110403010581>',[veterHealSkill1,veterHealSkill2,veterHealSkill3,veterHealSkill4],ALTRUISTE,baseLvl=30))

for a in [0,1,2]: # OctoMoine
    tablAllOcta.append(octarien("OctoMoine",100,75,30,35,40,25,50,30,0,0,mainLibre,5,'<:octoMonk:907723929882337311>',[airStrike,earthStrike],BERSERK,baseLvl=15))

for a in [0,1,2]: # OctoMage2
    tablAllOcta.append(octarien("Octo Mage II",50,20,30,30,30,20,100,20,10,15,octoMageWeap,5,'<:octoMage2:907712297013751838>',[fireCircle,waterCircle,earthCircle,airCircle],MAGE,baseLvl=20))

# OctoSnipe
tablAllOcta += [octarien("OctoSniper",150,30,20,0,75,20,15,15,0,0,octoSnipeWeap,7,'<:octotSniper:873118129398624287>',aspiration=OBSERVATEUR,description="Un octarien qui a passé des années à s'entrainer pour rivaliser avec une inkling qui faisait des ravages conséquents parmis les siens",baseLvl=15)]

# Boss special skills ----------------------------------------------------------------
spamSkill1 = skill("A Call For You","aaa",TYPE_DAMAGE,0,70,area=AREA_CONE_3,sussess=50,emoji='<:call:892757436203671572>',cooldown=3,message="HOT {0} IN YOUR AREA HAVE A [[Message](https://fr.wikipedia.org/wiki/Message)] FOR [{2}] :")
spamSkill2 = skill("BIG SHOT","aaa",TYPE_DAMAGE,0,130,area=AREA_LINE_5,sussess=70,ultimate=True,cooldown=5,message="[[Press F1](https://forums.commentcamarche.net/forum/affich-19023080-press-f1-to-continue-del-to-enter-setup)] FOR HELP :",emoji='<:bigshot:892757453442277417>')
serenaSpe = skill("Libération","aaa",TYPE_UNIQUE,0,35,AREA_MONO,ultimate=True,cooldown=5,area=AREA_ALL_ENNEMIES,description="Serena fait imploser toutes les poudres de fées d'Estialba, infligeant des dégâts en fonction du nombre d'effets \"Poison d'Estialba\" et de leurs durées restantes",emoji=estal.emoji[0][0])
serenaSkill = skill("Propagation","aaa",TYPE_INDIRECT_DAMAGE,0,0,AREA_MONO,area=AREA_ALL_ENNEMIES,cooldown=3,effect=[estal],emoji=estal.emoji[0][0])

jevilWeap = weapon("Trèfle","aaa",RANGE_DIST,AREA_CIRCLE_4,76,50,0,area=AREA_CONE_2,say="CHAOS, CHAOS, CATCH ME IF YOU CAN!",emoji='<:chaos:892857755143127090>',damageOnArmor=1.5)
jevilSkill1 = skill("Pics","aaa",TYPE_DAMAGE,0,70,area=AREA_CONE_3,range=AREA_DIST_5,sussess=60,emoji='<a:card:892855854712385637>',say="NU-HA!! I NEVER HAD SUCH FUN, FUN!!",cooldown=2,damageOnArmor=1.5)
jevilSkill2 = skill("Final Chaos","aaa",TYPE_DAMAGE,0,120,AREA_MONO,area=AREA_ALL_ENNEMIES,say="KIDDING ! HERE'S MY FINAL CHAOS !",initCooldown=5,cooldown=10,emoji="<:devilknife:892855875600023592>",damageOnArmor=2)
ailillSkill = skill("Décapitage","aaa",TYPE_DAMAGE,0,1000,AREA_CIRCLE_1,initCooldown=5,cooldown=5,damageOnArmor=500,message="{0} a assez vu {2} :",emoji='<:decapitage:897846515979149322>',say="J'en ai assez de ta tête.")
lunaSpe = skill("Ténèbres Éternels","InfDarkLaunch",TYPE_DAMAGE,0,100,AREA_MONO,area=AREA_CIRCLE_7,emoji='<a:darkExplosion:899451335269822475>',say="Voyons voir comment vous allez résister à ça !",description="\n\nInvoque X **Convictions des Ténèbres**, X étant la taille de l'équipe bleue au début du combat.\nAprès 3 tours de chargement, Luna enveloppe le terrain de Ténèbres, infligeant des dégâts massifs à toute l'équipe en fonction du nombre de **Convictions des Ténèbres** présent sur le terrain\n\nDurant la période de chargement, Luna est **Invisible**, **Inciblable** et **Imunisée**",cooldown=99,initCooldown=10,damageOnArmor=1.66)
lunaRepEffect = effect("Cast - Ténèbres Éternels","darkerYetDarker3",replique=lunaSpe,turnInit=2,silent=True,emoji=dangerEm,immunity=True,translucide=True,untargetable=True)
lunaSpe2 = skill("Ténèbres Éternels","aab",TYPE_DAMAGE,0,0,AREA_MONO,area=AREA_DONUT_7,effectOnSelf=lunaRepEffect,say="On s'accroche toujours hein ?",message="Luna concentre les Ténèbres environants...",emoji='<:infiniteDarkness:898497770531455008>')
lunaWeap = weapon("Concentraceur K","aaa",RANGE_MELEE,AREA_CIRCLE_1,35,40,0,0,0,0,0,0,0,0,0,0,0,5,kcharger.emoji,message="{0} frappe {1} avec son arme :",damageOnArmor=1.2)
lenaRepEffect2 = effect("Cast - Ténèbres Éternels","darkerYetDarker2",replique=lunaSpe2,turnInit=3,silent=True,emoji=uniqueEmoji('<:longCast:898555354462441572>'),immunity=True,translucide=True,untargetable=True)
lunaSpe3 = skill("Ténèbres Éternels","aac",TYPE_DAMAGE,0,0,AREA_MONO,area=AREA_DONUT_7,effectOnSelf=lenaRepEffect2,message="Luna concentre les Ténèbres environants...",emoji='<:infiniteDarkness:898497770531455008>')
lenaRepEffect3 = effect("Cast - Ténèbres Éternels","darkerYetDarker1",replique=lunaSpe3,turnInit=4,silent=True,emoji=uniqueEmoji('<:longCast:898555354462441572>'),immunity=True,translucide=True,untargetable=True)
lunaSpe4 = skill("Ténèbres Éternels","InfiniteDarkness",TYPE_DAMAGE,0,0,AREA_MONO,cooldown=99,initCooldown=8,area=AREA_DONUT_7,effectOnSelf=lenaRepEffect3,emoji='<:infiniteDarkness:898497770531455008>',say='OK ! FINI DE JOUER !')
lunaSkill = copy.deepcopy(soupledown)
lunaSkill.power = 120
lunaSkill2 = skill("Tank Burst","aaa",TYPE_DAMAGE,0,300,AREA_CIRCLE_2,cooldown=5,initCooldown=2,emoji='<a:lunaTB:899456356036251658>')
lunaSkill4Eff = copy.deepcopy(innerdarknessEff)
lunaSkill4Eff.stat = STRENGTH
lunaSkill4Eff.power = 55
lunaSkill4 = skill("Déchirment","aaa",TYPE_INDIRECT_DAMAGE,0,range=AREA_MONO,area=AREA_DIST_7,effect=lunaSkill4Eff,cooldown=5,use=MAGIC,say="Ne sentez vous pas les ténèbres de votre âme s'agiter ?",emoji=innerdarkness.emoji)
lunaSkill5 = skill("Assombrissement","lunaSkill5",TYPE_DAMAGE,0,100,AREA_MONO,cooldown=4,emoji='<:lunaSkill5:905401258658115615>',area=AREA_CIRCLE_2,say="Je comprend pas pourquoi vous tenez tant à vous mettre en travers de mon chemin")
jevilEff = effect("Confusion","giveup",silent=True,emoji=uniqueEmoji('<a:giveup:902383022354079814>'),turnInit=3,description="Confuse confusing confusion")
jevilSkill3 = skill("Confusion","aaa",TYPE_MALUS,0,range=AREA_MONO,area=AREA_ALL_ENTITES,effect=jevilEff,cooldown=5,emoji='<a:giveup:902383022354079814>',say='I CAN DO ANYTHING !')

tablBoss = [
    octarien("Ailill",80,50,0,30,50,50,50,10,10,0,depha,10,'<a:Ailill:882040705814503434>',[balayette,uppercut,ailillSkill],BERSERK,GENDER_FEMALE,description="Une humaine à qui la vie n'a pas vraiment souris. Du coup elle passe ses nerfs sur les autres.\nEnfin les autres plus faibles qu'elle évidamment\n\nSi il y a 5 combattants ou plus dans une équipe, les dégâts infligés à Ailill sont réduits si l'attaquant est trop éloigné",say=ailillSays),
    octarien("[[Spamton Neo](https://deltarune.fandom.com/wiki/Spamton)]",250,1250,100,45,45,200,200,30,10,15,bigshot,45,'<a:spamton:892749040205316138>',skill=[spamSkill1,spamSkill2],description="NOW IT'S YOUR CHANCE TO BE A [Big shot] !",deadIcon='<:spamblocked:892750635315912746>',oneVAll=True,say=spamtonSays),
    octarien("Jevil",250,1500,100,60,75,120,120,10,0,15,jevilWeap,50,'<a:CHAOS:762276118224961556>',[chaos,jevilSkill1,jevilSkill2,jevilSkill3],description="I CAN DO ANYTHING !",deadIcon='<:chaosnt:892857736642064455>',oneVAll=True,say=jevilSays),
    octarien("Serena",50,65,-50,70,50,50,150,25,5,15,armilame,10,'<:serena:897912402354511894>',[poisonus,serenaSkill,serenaSpe],ENCHANTEUR,GENDER_FEMALE,deadIcon='<:flowernt:894550324705120266>'),
    octarien("Luna",275,1150,100,75,50,100,0,25,0,25,lunaWeap,50,'<:luna:899120831152680971>',[lunaSpe4,lunaSkill,lunaSkill5,lunaSkill2,lunaSkill4],POIDS_PLUME,GENDER_FEMALE,"Il viendra toujours un moment où vous allez devoir affronter votre côté sombre",'<:spIka:866465882540605470>',True,say=lunaBossSays),
    octarien("Octo Tour",0,650,0,0,0,0,0,50,0,0,octoTour,12,'<:tower:905169617163538442>',[octoTourSkill],PROTECTEUR,description="Une tour de siège. Tant qu'elle est en vie, tous les dégâts directs reçu par ses alliés lui sont redirigés")
]

clemInnerDark = copy.deepcopy(innerdarkness)
aliceOnStage = copy.deepcopy(onstage)
aliceOnStage.say = "Hé ! Hé ! J'ai une avant première pour vous tous, vous en pensez quoi ?"
lohicaFocal = copy.deepcopy(focal)
lohicaFocal.say = "Vous commencez sérieusement à me tapez sur les nerfs..."
feliSplash = copy.deepcopy(splashdown)
feliSplash.say = "Vous m'en direz des nouvelles !"

# Alliés temporaires
tablAllAllies = [
    tmpAllie("Lena",1,light_blue,OBSERVATEUR,splatcharger,[amethystEarRings,lightBlueJacket,lightBlueFlats],GENDER_FEMALE,[splatbomb,bigMonoLaser2,trans,shot,multishot],"Une inkling qui en a vu des vertes et des pas murs.\nPréfère rester loin de la mêlée et abattre ses ennemis à bonne distance","https://cdn.discordapp.com/emojis/899120815205929010.png",ELEMENT_WATER,icon='<:lena:899120815205929010>',bonusPoints=[STRENGTH,PRECISION],say=lenaSays),
    tmpAllie("Gwendoline",2,yellow,POIDS_PLUME,roller,[anakiMask,FIACNf,blackFlat],GENDER_FEMALE,[defi,splashdown,balayette,airStrike],"Bien qu'elle essaye de l'éviter, cette jeune femme se retrouve toujours à devoir en venir aux mains pour se débarraser des gros lourds de la première ligne ennemie.\nIl est vrai aussi qu'elle n'est pas toute seule dans sa tête","https://cdn.discordapp.com/emojis/906303014665617478.png",ELEMENT_AIR,bonusPoints=[STRENGTH,ENDURANCE],icon='<:gweny:906303014665617478>'),
    tmpAllie("Clémence",2,red,MAGE,rapiere,[indeci1,indeci2,indeci3],GENDER_FEMALE,[bleedingArrow,poisonus,bleedingDague,clemInnerDark,invocCarbunR],"Une vampire qui a décidé de léguer sa jeunesse éternelle à l'étude des runes et la magie","https://cdn.discordapp.com/emojis/899117538519154758.png",ELEMENT_DARKNESS,icon='<:clemence:899117538519154758>',bonusPoints=[MAGIE,STRENGTH],say=clemSays),
    tmpAllie("Alice",1,pink,IDOLE,mic,[batRuban,aliceDress,aliceShoes],GENDER_FEMALE,[invocBat2,vampirisme,theSkill,croissance,aliceOnStage],"Une petite fille vampirique qui veut toujours avoir l'attention sur elle. Faisant preuve d'une grande volontée, il faudrait mieux ne pas trop rester dans le coin si elle décide que vous lui faites de l'ombre","https://cdn.discordapp.com/emojis/899117566683934770.png",ELEMENT_LIGHT,icon='<:alice:899117566683934770>',bonusPoints=[CHARISMA,INTELLIGENCE],say=aliceSays),
    tmpAllie("Shushi",1,blue,ENCHANTEUR,airspell,[tankmage3,tankmage2,tankmage1],GENDER_FEMALE,[ferocite,invocCarbT,storm2,storm,suppr],"Jeune inkling pas très douée pour le combat, à la place elle essaye de gagner du temps pour permettre à ses alliés d'éliminer l'équipe adverse","https://cdn.discordapp.com/emojis/899117520211042334.png",ELEMENT_AIR,icon='<:shushi:899117520211042334>',bonusPoints=[MAGIE,ENDURANCE],say=shushiSays),
    tmpAllie("Lohica",1,purple,MAGE,butterflyP,[old,robeLoliBlue,blueFlat],GENDER_FEMALE,[lohicaFocal,poisonus,heriteEstialba,dark2],"Une fée à l'histoire bien mouvementée. Spécialisée dans les poisons","https://cdn.discordapp.com/emojis/899694452334022706.png",ELEMENT_DARKNESS,bonusPoints=[MAGIE,STRENGTH],icon='<a:lohicaGif:900378281877057658>',deadIcon='<:flowernt:894550324705120266>'),
    tmpAllie("Hélène",2,white,ALTRUISTE,serringue,[barrette,heleneDress,heleneShoe],GENDER_FEMALE,[cure,lapSkill,memAlice2,eting,revitalisation],"Une fée qui estime qu'essayer de sauver la vie de ses alliés est plus efficace que si elle esseyait de terminer le combat elle-même","https://cdn.discordapp.com/emojis/906303162854543390.png",ELEMENT_LIGHT,bonusPoints=[CHARISMA,INTELLIGENCE],icon='<:helene:906303162854543390>'),
    tmpAllie("Félicité",1,red,TETE_BRULE,dtsword,[celestBronzeHat,celestBronzeArmor,celestBronzeBoots],GENDER_FEMALE,[defi,uppercut,feliSplash,splatbomb,highkick],"Une grande pré-ado qui veut toujours tout faire, mais qui n'y arrive pas tout à fait non plus","https://cdn.discordapp.com/emojis/899695897900879902.png",bonusPoints=[ENDURANCE,STRENGTH],icon='<:felicite:899695897900879902>'),
    tmpAllie("Akira",2,black,TETE_BRULE,fauc,[anakiMask,heartSphapeObject,blackSnelers],GENDER_MALE,[defi,balayette,splashdown,bleedingDague,demolish],"Flora si tu as une description je veux bien","https://cdn.discordapp.com/emojis/899693936199753779.png",ELEMENT_DARKNESS,bonusPoints=[ENDURANCE,STRENGTH],icon='<:akiki:899693936199753779>'),
    tmpAllie("Icealia",2,light_blue,PREVOYANT,waterspell,[vigilant1,vigilant2,vigilant3],GENDER_FEMALE,[protect,inkarmor,kralamSkill,convert,onde],"Une érudite qui préfère protéger ses compagnons",element=ELEMENT_LIGHT,bonusPoints=[INTELLIGENCE,ENDURANCE]),
    tmpAllie("Powehi",2,black,PROTECTEUR,inkbrella2,[starBar,starPull,starBoots],GENDER_FEMALE,[blackHole,trans,blindage,secondWind,blackHole2],"Une manifestation cosmique d'un trou noir. Si vous vous sentez attiré par elle, c'est probablement à raison\nNe lui demandez pas de vous marchez dessus par contre, si vous voulez un conseil. Elle a beau paraître avoir un petit gabarie, ce n'est pas pour rien qu'elle évite de marcher sur le sol",element=ELEMENT_SPACE,bonusPoints=[ENDURANCE,INTELLIGENCE],icon='<:powehi:906202079213797448>',deadIcon = '<:powehiDisiped:907326521641955399>',say=powehiSays),
    tmpAllie("Shehisa",1,purple,TETE_BRULE,shehisa,[shehisaMask,shehisaBody,shehisaBoots],GENDER_FEMALE,[dissimulation,bleedingDague,bleedingArrow,bleedingTrap,heriteLesath],"Soeur d'Hélène, elle a cependant préférer suivre un chemin beaucoup moins altruiste",element=ELEMENT_NEUTRAL,bonusPoints=[STRENGTH,ENDURANCE],icon='<:shehisa:901555930066473000>'),
    tmpAllie("Rasalhague",1,light_blue,MAGE,spellBook,[lentille,chemB,mocas],GENDER_MALE,[space1,space2,space3,spaceSp],element=ELEMENT_SPACE,icon='<:rasalhague:907689992745271376>',bonusPoints=[MAGIE]),
    tmpAllie("Sixtine",1,blue,PREVOYANT,lightSpellBook,[blueNoeud,pullHeart,heartBask],skill=[bpotion,affaiblissement,nostalgia,provo],gender=GENDER_FEMALE,element=ELEMENT_NEUTRAL,bonusPoints=[INTELLIGENCE,ENDURANCE],description="Grande rêveuse, Sixtine préfère rester seule dans son coin à dessiner pendant que ses soeurs partent en vadrouille")
]

# Shushi alt spells
shushiSkill1 = skill("Frappe lumineuse","aaa",TYPE_DAMAGE,0,80,cooldown=3,use=MAGIE,emoji='<a:ShushiLF:900088862871781427>')
shushiSkill2Eff = effect("Armure de Lumière","shuArmor",overhealth=50,stat=MAGIE,turnInit=3,type=TYPE_ARMOR,emoji=uniqueEmoji('<a:shushiLA:900089758494097450>'))
shushiSkill2 = skill("Armure de Lumière","aaa",TYPE_ARMOR,0,range=AREA_MONO,area=AREA_ALL_ALLIES,cooldown=7,initCooldown=5,effect=shushiSkill2Eff,say='On peut pas ahandonner mitenant !',emoji='<a:shushiLA:900089758494097450>')
shushiSkill3Eff = effect("Jeu de lumière","diff",untargetable=True,description="Un habile jeu de lumière permet de vous cacher de vos ennemis",emoji=untargetableEmoji)
shushiSkill3 = skill("Diffraction","aaa",TYPE_ARMOR,0,0,AREA_CIRCLE_6,effect=shushiSkill3Eff,cooldown=5,initCooldown=2,use=None,emoji='<:untargetable:899610264998125589>')
shushiSkill4Eff = effect("Assimilation","assimil",MAGIE,strength=20,charisma=20,intelligence=20,magie=20,resistance=5,critical=5,description="Grâce à Shihu, vous avez réussi à utiliser les Ténèbres environant à votre avantage")
shushiSkill4 = skill("Assimilation","aaa",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_4,cooldown=10,initCooldown=2,effect=shushiSkill4Eff,say='On peut y awiver !',use=MAGIE)
shushiWeapEff = effect("Lueur Ténébreuse","darkLight",MAGIE,resistance=5,overhealth=15,type=TYPE_ARMOR,emoji=uniqueEmoji('<:dualMagie:899628510463803393>'))
shushiWeap = weapon("Magie trancendante","dualMagie",RANGE_LONG,AREA_DONUT_5,35,100,0,strength=-20,endurance=10,charisma=20,intelligence=20,magie=35,type=TYPE_HEAL,target=ALLIES,use=MAGIE,effectOnUse=shushiWeapEff,affinity=ELEMENT_LIGHT,emoji='<:dualMagie:899628510463803393>')
shushiHat = stuff("Barrête de la cohabitation","dualHat",0,0,strength=-20,endurance=15,charisma=20,agility=10,precision=10,intelligence=20,magie=45,affinity=ELEMENT_LIGHT)
shushiDress = stuff("Robe de la cohabitation","dualDress",1,0,strength=-10,endurance=35,charisma=20,agility=0,precision=10,intelligence=10,magie=60,resistance=20,affinity=ELEMENT_LIGHT)
shushiBoots = stuff("Bottines de la cohabitation","dualBoost",2,0,strength=-10,endurance=15,charisma=0,agility=20,precision=10,magie=40,intelligence=10,affinity=ELEMENT_LIGHT)
shushiSkill5 = skill("Lumière éternelle","LumEt",TYPE_RESURECTION,0,100,emoji='<:renisurection:873723658315644938>',cooldown=2,description="Permet de ressuciter un allié (en théorie, vous vous doutez bien que c'est compliqué à tester)",use=MAGIE,range=AREA_DONUT_7)

shihuDarkBoom1 = copy.deepcopy(explosion)
shihuDarkBoom2 = copy.deepcopy(explosion2)
shihuDarkBoomEff = copy.deepcopy(castExplo)

shihuDarkBoom2.effectOnSelf, shihuDarkBoom2.name,shihuDarkBoom2.emoji = shihuDarkBoomEff,"Explosion Noire",'<a:darkExplosion:899451335269822475>'
shihuDarkBoom2.id, shihuDarkBoom1.name, shihuDarkBoom1.repetition, shihuDarkBoom1.power = "ShihuDarkBoom","Explosion Noire",2,int(explosion.power * 0.45)
shihuDarkBoomEff.replica = shihuDarkBoom1
shihuDarkBoomEff.id = "ShihuDarkBoomEff"
shihuDarkBoom1.emoji= '<a:darkExplosion:899451335269822475>'
shihuDarkBoom1.id = "ShihuDarkBoomLaunch"
shihuDarkBoom1.say = "Za va fire Boum Boum !"

tablVarAllies = [
    tmpAllie("Luna",1,black,POIDS_PLUME,kcharger,[darkMaidPendants,darkMaidDress,darkMaidFlats],GENDER_FEMALE,[defi,splatbomb,balayette,soupledown,highkick],"Là où se trouve la Lumière se trouvent les Ténèbres","https://cdn.discordapp.com/emojis/899120831152680971.png?size=96",ELEMENT_DARKNESS,variant=True,icon='<:luna:899120831152680971>',bonusPoints=[STRENGTH,ENDURANCE],say=lunaSays),
    tmpAllie("Altikia",2,yellow,PROTECTEUR,inkbrella,[maidHat,yellowpull,maidHeels],GENDER_FEMALE,[ironWillSkill,lightAura,inkarmor,renisurection,concen],"Une personnalité de Gwen qui préfère se concentrer sur ses alliés","https://cdn.discordapp.com/emojis/906303048542990347.png",ELEMENT_LIGHT,variant=True,bonusPoints=[ENDURANCE,CHARISMA],icon='<:alty:906303048542990347>'),
    tmpAllie("Klironovia",2,yellow,BERSERK,klikliSword,[darkMaidPendants,FIACNf,blackFlat],GENDER_FEMALE,[defi,demolish,earthStrike,trans,highkick],"Une personnalité de Gwen bien plus violente que les deux autres","https://cdn.discordapp.com/emojis/906303031837073429.png",ELEMENT_EARTH,variant=True,bonusPoints=[STRENGTH,AGILITY],icon='<:klikli:906303031837073429>'),
    tmpAllie("Shihu",1,black,MAGE,darkSpellBook,[shihuHat,shihuDress,shihuShoe],GENDER_FEMALE,[dark2,dark3,shihuDarkBoom1,suppr],"\"Eye veut zuste un pi d'attenchions...\" - Shushi","https://cdn.discordapp.com/emojis/899117502800461824.png?size=96",ELEMENT_DARKNESS,variant=True,icon='<:shihu:899117502800461824>',bonusPoints=[MAGIE,STRENGTH],say=shihuSays),
    tmpAllie("Shushi (Alt.)",1,blue,PREVOYANT,shushiWeap,[shushiHat,shushiDress,shushiBoots],GENDER_FEMALE,[shushiSkill1,shushiSkill2,shushiSkill3,shushiSkill4,shushiSkill5],"S'étant comprise l'une et l'autre, Shushi et Shihu ont décidé de se liguer contre la mère de cette dernière.\nCette allié temporaire n'apparait que contre le boss \"Luna\"","https://cdn.discordapp.com/emojis/899608664770506783.png?size=96",ELEMENT_LIGHT,True,icon='<:shushiAlt:899608664770506783>',bonusPoints=[MAGIE,AGILITY])
]

print("\nVérification de l'équilibrage des stuffs...")
allstats = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for a in stuffs+weapons:
    ballerine = a.allStats()+[a.resistance,a.percing,a.critical]
    babie = [a.negativeHeal,a.negativeBoost,a.negativeShield,a.negativeDirect,a.negativeIndirect]
    sumation = 0
    for b in range(0,len(ballerine)):
        sumation += ballerine[b]
        allstats[b] += ballerine[b]

    for b in babie:
        sumation -= b

    if sumation != 20 and a.effect == None and a.name != "Claquettes chaussettes":
        print("{0} n'a pas le bon cumul de stats : {1}".format(a.name,sumation))

    elif sumation != 10 and a.effect != None:
        print("{0} n'a pas le bon cumul de stats : {1}".format(a.name,sumation))

temp = "\nDistribution des statistiques :\n"
total = 0
for a in allstats:
    total += a

for a in range(0,len(allStatsNames)):
    temp += "{0} : {1}% ({2})\n".format(allStatsNames[a],round(allstats[a]/total*100,2),allstats[a])
print(temp)

lvlTabl = [{"level":0,"nombre":0}]
for equip in stuffs:
    find = False
    for temp in lvlTabl:
        if temp["level"] == equip.minLvl:
            temp["nombre"]+=1
            find = True
            break

    if not(find):
        lvlTabl.append({"level":equip.minLvl,"nombre":1})

lenStuff = len(stuffs)
lvlTabl.sort(key=lambda ballerine: ballerine["level"])

for temp in lvlTabl:
    print("Objets de niveau {0} : {1} ({2})%, statsAttendues : {3}".format(temp["level"],temp["nombre"],round(temp["nombre"]/lenStuff*100,2),20 + (temp["level"] * 2)))

tabl = copy.deepcopy(tablAllAllies)
tablTank = []
tablMid = []
tablBack = []

for allie in tabl:
    [tablTank,tablMid,tablBack][allie.weapon.range].append(allie)

print("")
for num in range(3):
    print("Nombre de Temp's en {0} : {1}".format(["mêlée","distance","backline"][num],len([tablTank,tablMid,tablBack][num])))

tabl = copy.deepcopy(tablAllOcta)
alReadySeen = []
tablTank = []
tablMid = []
tablBack = []

for ennemi in tabl:
    if ennemi.name not in alReadySeen:
        [tablTank,tablMid,tablBack][ennemi.weapon.range].append(ennemi)
        alReadySeen.append(ennemi.name)
        stat = ennemi.allStats()+[ennemi.resistance,ennemi.percing,ennemi.critical]
        summ = 0
        for a in stat:
            summ += a

        awaited = int((230+80*3)*0.65)
        if summ < awaited or summ > awaited*1.1:
            print("{0} n'a pas le bon cumul de stats : {1} ({2})".format(ennemi.name,summ,awaited))

print("")
for num in range(3):
    print("Nombre d'ennemis en {0} : {1}".format(["mêlée","distance","backline"][num],len([tablTank,tablMid,tablBack][num])))

print("\nVérification de l'équilibrage des stuffs terminée")


def findWeapon(WeaponId) -> weapon:
    typi = type(WeaponId)
    if typi == weapon:
        return WeaponId

    elif type(WeaponId) != str:
        return None
    else:
        rep,id = None,WeaponId

        if WeaponId.startswith("\n"):
            id = WeaponId[-2:]
        for a in weapons:
            if a.id == id or a.name.lower() == id.lower():
                rep = a
                break
    
        return rep

def findSkill(skillId) -> skill:
    """Renvoie une compétence Skill, si trouvé"""
    typi = type(skillId)
    if typi == skill:
        return skillId

    elif type(skillId) != str or skillId == "0":
        return None
    else:
        if skillId.startswith("\n"):
            skillId = skillId[-2:]
        for a in skills:
            if a.id == skillId or a.name.lower() == skillId.lower():
                return a

        #print("ID non trouvée : ",skillId)
        return None

def findStuff(stuffId) -> stuff:
    """Renvoie un équipement Stuff, si trouvé"""
    typi = type(stuffId)
    if typi == stuff:
        return stuffId

    elif type(stuffId) != str:
        return None
    else:
        rep,id = None,stuffId
        if stuffId.startswith("\n"):
            id = stuffId[-2:]
        for a in stuffs:
            if a.id == id or a.name.lower() == id.lower():
                rep = a
                break

        return rep

def findEffect(effectId) -> effect:
    if type(effectId) == effect:
        return effectId
    elif type(effectId) != str:
        return None
    else:
        rep,id = None,effectId
        if effectId.startswith("\n"):
            id = effectId[-2:]
        for a in effects:
            if a.id == id or a.name.lower() == id.lower():
                rep = a
                break
    
        return rep

def findOther(otherId) -> other:
    if type(otherId) == other:
        return otherId
    else:
        rep,id = None,otherId
        if otherId.startswith("\n"):
            id = otherId[-2:]
        for a in others:
            if a.id == id or a.name.lower() == id.lower():
                rep = a
    
    return rep

def findInvoc(name) -> invoc:
    for a in invocTabl:
        if a.name == name:
            return a

    return None

def findAllie(name) -> tmpAllie:
    for a in tablAllAllies+tablVarAllies:
        if a.name == name:
            return a
    return None

def findEnnemi(name) -> octarien:
    for a in tablAllOcta+tablBoss:
        if a.name == name:
            return a
    return None

listAllBuyableShop = []
for a in weapons+skills+stuffs:
    if a.price > 0:
        listAllBuyableShop.append(a)

def userShopPurcent(user : char):
    totalShop = len(listAllBuyableShop)
    tablToSee = listAllBuyableShop[:]
    for a in listAllBuyableShop:
        if user.have(a):
            tablToSee.remove(a)

    return 100-(len(tablToSee)/totalShop*100)

print("\nVérification des identifiants...")
allReadySeen = []
for obj in stuffs+weapons+skills+others:
    if obj.id not in allReadySeen:
        allReadySeen.append(obj.id)
    else:
        what = ""
        for whaty in stuffs+weapons+skills+others:
            if whaty.id == obj.id:
                what += whaty.name + ", "
        print("Identifiant doublon : {1}".format(obj.name,what))
print("\nVérification des identifiants terminée")

transMelee = copy.deepcopy(trans)
transMelee.type,transMelee.power, transMelee.name = TYPE_DAMAGE,200, transMelee.name + " - Lasers Chromanergiques Prompts, Monocible"

transLine = copy.deepcopy(trans)
transLine.type,transLine.power,transLine.area, transLine.name = TYPE_DAMAGE,180,AREA_LINE_6, transLine.name + " - Lasers Chromanergiques Prompts, Ligne"

transCircle = copy.deepcopy(trans)
transCircle.type,transCircle.power,transCircle.area,transCircle.name = TYPE_DAMAGE,160,AREA_CIRCLE_2, transCircle.name + " - Explosion Prompte"

transHeal = copy.deepcopy(trans)
transHeal.type,transHeal.power,transHeal.area,transHeal.range, transHeal.name = TYPE_HEAL,100,AREA_ALL_ALLIES,AREA_MONO, transHeal.name + " - Voie de l'Ange Prompte"

transInvoc = copy.deepcopy(trans)
transInvoc.type, transInvoc.invocation, transInvoc.name  = TYPE_INVOC,"Titania", transInvoc.name + " - La lumière brille brille brille"

transShield = copy.deepcopy(trans)
transShield.type,transShield.area,transShield.range,transShield.effect,transShield.name = TYPE_ARMOR,AREA_ALL_ALLIES,AREA_MONO,[effTransShield],transShield.name + " - Extra Armure d'Encre"