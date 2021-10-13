from classes import *
from data.database import *
import random

stuffDB =  dbHandler(database="stuff.db")
customIconDB = dbHandler(database="custom_icon.db")

def uniqueEmoji(emoji):
    return [[emoji,emoji],[emoji,emoji],[emoji,emoji]]

# Weapon
splattershot = weapon("Liquidateur","ab",RANGE_DIST,AREA_CIRCLE_3,30,50,100,precision=10,strength=10,repetition=3,emoji = emoji.splatShot,affinity=ELEMENT_NEUTRAL)
roller = weapon("Rouleau","ac",RANGE_MELEE,AREA_CIRCLE_1,40,70,100,strength=15,endurance=5,resistance=5,agility=-5,emoji = emoji.roller,needRotate=False,affinity=ELEMENT_AIR,area=AREA_CONE_2,damageOnArmor=0.8)
splatcharger = weapon("Concentraceur","ad",RANGE_LONG,AREA_CIRCLE_5,50,60,100,agility=-5,precision=25,emoji = emoji.charger,damageOnArmor=1.5,affinity=ELEMENT_WATER)
miniBrush = weapon("Epinceau","ae",RANGE_MELEE,AREA_CIRCLE_1,30,45,100,agility=10,charisma=10,repetition=5,emoji='<:inkBrush:866463573580578816>',needRotate=False)
inkbrella = weapon("Para-Encre","ag",RANGE_MELEE,AREA_CIRCLE_2,30,45,price=100,endurance=10,resistance=10,precision=-10,repetition=3,effect='lp',emoji='<:splatbrella:866464991255199834>',needRotate=False)
blaster = weapon("Eclatblasteur","ah",RANGE_DIST,AREA_CIRCLE_3,35,50,150,agility=10,strength=10,percing=10,precision=-10,area=AREA_CIRCLE_1,emoji='<:blaster:866463931304378418>')
jetSkelcher = weapon("Nettoyeur XL","ai",RANGE_LONG,AREA_CIRCLE_5,30,40,200,10,precision=10,repetition=4,emoji='<:squelsher:866464376319115281>',affinity=ELEMENT_WATER)
dualies = weapon("Double Encreur","aj",RANGE_DIST,AREA_CIRCLE_3,35,35,150,agility=20,repetition=4,emoji='<:splatDualies:866465264434806815>',needRotate=False,affinity=ELEMENT_AIR)
kcharger = weapon("Concentraceur alt.","ak",RANGE_MELEE,AREA_CIRCLE_1,35,60,200,15,agility=15,magie=-10,repetition=3,emoji='<:kcharger:870870886939508737>',message="{0} frappe {1} avec son arme :",use=STRENGTH)
HunterRiffle = weapon("Fusil de chasseur","al",RANGE_DIST,AREA_CIRCLE_4,50,50,250,precision=10,effect="ls",emoji="<:hunterRifle:872034208095297597>",affinity=ELEMENT_NEUTRAL)
firework = weapon("Arbalette avec feu d'artifice","am",RANGE_LONG,AREA_CIRCLE_4,35,50,150,10,precision=10,emoji='<:crossbow:871746122899664976>',area=AREA_CONE_2)
plume = weapon("Plumes tranchantes","ao",RANGE_DIST,AREA_CIRCLE_4,40,50,250,precision=10,percing=10,repetition=1,emoji='<:plume:871893045296128030>',area=AREA_CONE_2,needRotate=False,affinity=ELEMENT_AIR)
hourglass1Weap = weapon("Sablier intemporel I","ap",RANGE_DIST,AREA_CIRCLE_3,20,100,250,endurance=10,resistance=10,target=ALLIES,type=TYPE_HEAL,effectOnUse="lx",emoji='<:hourglass1:872181735062908978>',use=CHARISMA)
clashBlaster = weapon("Rafa-Blasteur","aq",RANGE_MELEE,AREA_CIRCLE_2,20,40,250,endurance=10,agility=10,precision=-10,percing=10,emoji='<:clashBlaster:877666681869176853>',area=AREA_CIRCLE_1,repetition=4)
dualies = weapon("Double Encreur","ar",RANGE_DIST,AREA_CIRCLE_4,35,40,150,agility=15,precision=15,resistance=-10,repetition=4,emoji='<:splatDualies:866465264434806815>')
splatling = weapon("Badigeonneur","as",RANGE_LONG,AREA_CIRCLE_5,35,30,300,precision=10,strength=10,repetition=5,emoji='<:splatling:877666764736061490>')
flexi = weapon("Flexi-Rouleau","at",RANGE_DIST,AREA_CIRCLE_3,50,70,300,25,endurance=-10,critical=5,emoji='<:flexaRoller:877666714760925275>',needRotate=False)
squiffer = weapon("Décap' Express","au",RANGE_DIST,AREA_CIRCLE_4,45,60,300,10,agility=15,precision=10,resistance=-5,endurance=-10,emoji='<:skiffer:877666730225328138>')
dualJetSkelcher = weapon("Nettoyeur Duo","av",RANGE_LONG,AREA_CIRCLE_5,30,50,200,10,magie=10,agility=-10,precision=10,repetition=4,emoji='<:DualSkelcher:877666662801883237>',damageOnArmor=1.33)
butterfly = weapon("Papillon Blanc","aw",RANGE_LONG,AREA_CIRCLE_5,35,80,150,-5,-5,20,intelligence=10,emoji='<:butterflyB:883627125561786428>',target=ALLIES,type=TYPE_HEAL,needRotate=False,message="{0} demande à son papillon de soigner {1} :")
mic = weapon("Micro mignon","ax",RANGE_LONG,AREA_CIRCLE_3,25,55,300,-10,charisma=30,emoji='<:pinkMic:878723391450927195>',needRotate=False,use=CHARISMA,message="{0} pousse la chansonnette !")
spellBook = weapon("Grimoire de feu","ay",RANGE_DIST,AREA_CIRCLE_4,40,75,200,-10,-10,15,magie=20,percing=5,emoji='<:spellBook:878723144326725744>',needRotate=False,use=MAGIE,area=AREA_CIRCLE_1,affinity=ELEMENT_FIRE,message="{0} lance une boule de feu sur {1}")
legendarySword=weapon("Épée et Bouclier de Légende","az",RANGE_MELEE,AREA_CIRCLE_1,60,70,300,10,10,resistance=10,intelligence=-10,emoji='<:masterSword:880008948445478962>',affinity=ELEMENT_LIGHT)
depha = weapon("Lame Dimensionnelle","ba",RANGE_MELEE,AREA_CIRCLE_1,60,90,300,20,10,-10,intelligence=-10,resistance=10,emoji='<:LameDimensionnelle:881595204484890705>')
butterflyR = weapon("Papillon Rose","bb",RANGE_LONG,AREA_CIRCLE_5,35,80,150,-5,-5,20,intelligence=10,emoji='<:butterflyR:883627168406577172>',use=CHARISMA,needRotate=False,message="{0} demande à son papillon d'attaquer {1} :")
butterflyP = weapon("Papillon Violet","bc",RANGE_LONG,AREA_CIRCLE_5,30,100,250,strength=-10,magie=30,effectOnUse="me",needRotate=False,emoji='<:butterflyV:883627142615805962>',type=TYPE_DAMAGE,message="{0} demande à son papillon d'empoisonner {1} :",use=MAGIE)
dtsword = weapon("Épée de Détermination","bd",RANGE_MELEE,AREA_CIRCLE_1,70,70,500,25,endurance=10,charisma=-10,intelligence=-15,resistance=10,emoji='<:dtSword:884802145239588884>',affinity=ELEMENT_NEUTRAL)
magicSword = weapon("Épée de MagicalGirl","be",RANGE_MELEE,AREA_CIRCLE_1,35,70,200,-10,endurance=10,charisma=20,resistance=10,precision=-10,emoji="<:magicSword:885241611682975744>",use=CHARISMA)
lunarBonk = weapon("Bâton Lunaire","bf",RANGE_MELEE,AREA_CIRCLE_1,40,50,250,-20,20,0,0,-10,20,10,emoji="<:lunarBonk:887347614448746516>",use=MAGIE,affinity=ELEMENT_LIGHT)
rapiere = weapon("Rapière en argent","bg",RANGE_DIST,AREA_CIRCLE_3,45,60,0,magie=30,precision=-10,strength=20,endurance=-15,percing=10,resistance=-15,use=MAGIE,emoji='<:bloodyRap:887328737614524496>',effectOnUse="mx")
fauc = weapon("Faux Tourmentée","bh",RANGE_MELEE,AREA_CIRCLE_2,55,60,0,40,10,percing=10,agility=-20,charisma=-20,emoji='<a:akifauxgif:887335929650507776>',affinity=ELEMENT_DARKNESS)
serringue = weapon("Serringue","bi",RANGE_DIST,AREA_CIRCLE_3,35,100,350,0,0,20,0,0,10,10,-20,emoji='<:seringue:887402558665142343>',target=ALLIES,type=TYPE_HEAL,use=CHARISMA,affinity=ELEMENT_LIGHT,message="{0} fait une perfusion à {1}")
bigshot = weapon("[[Big shot](https://www.youtube.com/watch?v=-8p8VowCmgE)]","bj",RANGE_DIST,AREA_CIRCLE_4,70,60,1997,20,-20,0,0,0,10,0,10,emoji='<:bigshot:892756699277037569>',message="{0} PROPOSE UN [[Big shot](https://www.youtube.com/watch?v=-8p8VowCmgE)] À {1} :",area=AREA_LINE_2)
nemefaux = weapon("Faux vangeresse","bk",RANGE_MELEE,AREA_CIRCLE_2,55,70,500,20,10,-10,0,-5,0,5,0,0,0,emoji='<:avengerScythe:893227827942522951>',area=AREA_ARC_1)
waterspell = weapon("Grimoire de l'eau","bl",RANGE_LONG,AREA_CIRCLE_4,70,60,350,-20,-10,10,0,20,20,emoji='<:waterspellbook:892963508248002590>',affinity=ELEMENT_WATER,message="{0} projète un éclat de glace sur {1} :",use=MAGIE)
earthspell = weapon("Grimoire des terres","bm",RANGE_MELEE,AREA_CIRCLE_2,70,60,350,-20,20,0,-10,0,15,15,emoji='<:earthspellbook:892963483665174578>',affinity=ELEMENT_EARTH,use=MAGIE,message="{0} fait apparaitre des pics rocheux sous {1} :")
airspell = weapon("Grimoire des vents","bn",RANGE_MELEE,AREA_CIRCLE_2,20,70,350,-20,20,0,-10,0,15,15,emoji='<:airspellbook:892963551159922718>',affinity=ELEMENT_AIR,use=MAGIE,area=AREA_ARC_1,message="{0} forme des vents violents autour de {1}",repetition=3)
airsword = weapon("Épée des vents","bo",RANGE_MELEE,AREA_CIRCLE_1,50,70,350,-20,0,0,30,20,-10,emoji='<:airsword:892963581031772170>',repetition=1,affinity=ELEMENT_AIR,area=AREA_ARC_2,use=STRENGTH,message="{0} file comme le vent !")
armilame = weapon("Épée empoisonnée","bp",RANGE_MELEE,AREA_CIRCLE_1,60,65,350,-20,15,magie=20,resistance=15,charisma=-10,emoji='<:amirlame:894643896120918107>',effectOnUse="me",use=MAGIE)
shehisa = weapon("Faux des ombres","bq",RANGE_MELEE,AREA_CIRCLE_1,50,70,350,20,10,-20,intelligence=-20,magie=10,emoji='<:shefaux:896924311221305395>',effectOnUse='mx')
machinist = weapon("Canon du machiniste fantaisiste","br",RANGE_LONG,AREA_CIRCLE_4,45,60,350,strength=20,magie=-30,resistance=-10,precision=20,agility=15,percing=10,area=AREA_LINE_2,emoji='<:mach:896924290170093580>')

weapons = [machinist,shehisa,armilame,airsword,waterspell,earthspell,airspell,nemefaux,bigshot,serringue,fauc,rapiere,lunarBonk,magicSword,dtsword,butterflyP,butterflyR,depha,legendarySword,spellBook,mic,butterfly,dualJetSkelcher,squiffer,flexi,splatling,dualies,clashBlaster,hourglass1Weap,plume,mainLibre,splattershotJR,splattershot,roller,splatcharger,miniBrush,inkbrella,blaster,jetSkelcher,kcharger,HunterRiffle,firework]

def addAllInWeaponData():
    for a in weapons:
        try:
            stuffDB.create_weapon(a)
        except:
            stuffDB.edit_weapon(a)

# Skill
soupledown = skill("Choc Ténébreux","zz",TYPE_DAMAGE,500,140,range = AREA_CIRCLE_1,conditionType=["exclusive","aspiration",POIDS_PLUME],area = AREA_CIRCLE_2,sussess=70,ultimate=True,cooldown=4,emoji='<:darkdown:892350717384347648>',use=STRENGTH)
inkarmor = skill("Armure d'Encre","zy",TYPE_ARMOR,250,ultimate=True,effect="la",emoji = '<:inkArmor:866829950463246346>',area=AREA_ALL_ALLIES,cooldown=3,range=AREA_MONO)
coffeeSkill = skill("Suprématie du café","zx",TYPE_BOOST,500,effect=["lb","mc"],use=CHARISMA,conditionType=["reject","skill","zw"],area=AREA_ALL_ALLIES,emoji='<:coffee:867538582846963753>',cooldown=2,message="{0} prend le café avec ses alliés :")
theSkill = skill("Liberté du thé","zw",TYPE_BOOST,500,effect=["lc","mc"],use=CHARISMA,conditionType=["reject","skill","zx"],area=AREA_ALL_ALLIES,emoji='<:the:867538602644602931>',cooldown=2,message="{0} prend le thé avec ses alliés :")
gpotion = skill("Potion tonifiante","zv",TYPE_BOOST,200,emoji="<:bpotion:867165268911849522>",use=INTELLIGENCE,cooldown=3,effect="le",area=AREA_MONO,range=AREA_MONO)
bpotion = skill("Potion étrange","zu",TYPE_MALUS,200,cooldown=3,effect="lf",emoji="<:dpotion:867165281617182760>",use=INTELLIGENCE,area=AREA_CIRCLE_1,message="{0} lance une {1} sur {2}")
zelian = skill("R","zt",TYPE_INDIRECT_REZ,1000,cooldown=5,effect="lj",emoji='<:chronoshift:867872479719456799>',use=None)
courage = skill("Motivation","zs",TYPE_BOOST,500,emoji ='<:charge:866832551112081419>',area=AREA_CIRCLE_2,use=CHARISMA,effect="lk",cooldown=3,range=AREA_MONO)
nostalgia = skill("Nostalgie","zr",TYPE_MALUS,500,emoji='<:nostalgia:867162802783649802>',effect="lm",cooldown=3,use=INTELLIGENCE)
draw25 = skill("Stop attacking or draw 25","zq",TYPE_MALUS,300,25,emoji="<:draw25:869982277701103616>",use=None,effect="lq",cooldown = 3,area=AREA_ALL_ENNEMIES,range=AREA_MONO,ultimate=True,conditionType=["exclusive","aspiration",PREVOYANT],message="{0} utilise sa carte joker !")
siropMenthe = skill("Neutralité du Sirop de Menthe","zp",TYPE_BOOST,500,effect=["lu","mc"],use=CHARISMA,area=AREA_ALL_ALLIES,emoji='<:menthe:867538622797054042>',cooldown=2,message="{0} prend un sirop de menthe avec ses alliés :")
unHolly = skill("Truc pas catho","zo",TYPE_MALUS,69,emoji='<:bravotakei:877202258348113960>',effect="lw",use=CHARISMA,message="{0} ||fait des trucs pas catho à destination de|| {2} :")
chaos = skill("Chaos Chaos !","zn",TYPE_UNIQUE,1000,range=AREA_MONO,area=AREA_ALL_ENTITES,sussess=200,emoji='<a:CHAOS:762276118224961556>',cooldown=5,ultimate=True,use=None,message="PLEASE ! JUST A SIMPLE CHAOS !")
contrecoup = skill("Contre-coup","zm",TYPE_INDIRECT_DAMAGE,250,effect="ln",cooldown=2,emoji='<:aftershock:882889694269038592>',use=MAGIE)
boom = skill("Réaction en chaîne","zl",TYPE_INDIRECT_DAMAGE,250,effect="lv",cooldown=2,emoji='<:bimbamboum:873698494874017812>',use=MAGIE)
balayette = skill("Baleyette","zk",TYPE_DAMAGE,100,40,range=AREA_MONO,area=AREA_CIRCLE_1,emoji='<:baleyette:873924668963291147>',cooldown=2)
firstheal = skill("Premiers secours","zj",TYPE_HEAL,100,25,emoji="<:bandage:873542442484396073>")
cure = skill("Guérison","zi",TYPE_HEAL,250,60,cooldown=3,emoji='<:cure:873542385731244122>')
healAura = skill("Aura de Lumière","zh",TYPE_INDIRECT_HEAL,250,cooldown=3,range=AREA_MONO,area=AREA_MONO,effect="ly",emoji="<:AdL:873548073769533470>")
splatbomb = skill("Bombe splash","zg",TYPE_DAMAGE,100,cooldown=2,area=AREA_CIRCLE_1,power=45,emoji='<:splatbomb:873527088286687272>',message="{0} lance une {1} sur {2} :")
explosion = skill("Explosion","zf",TYPE_DAMAGE,1000,power=180,ultimate=True,cooldown=10,area=AREA_CIRCLE_2,sussess=80,effectOnSelf="mb",use=MAGIE,emoji='<a:explosion:882627170944573471>')
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
trans = skill("Transcendance","yt",TYPE_UNIQUE,0,initCooldown=3,cooldown=7,emoji="<:limiteBreak:886657642553032824>",description="Un sort particulier qui a un effet différent en fonction de l'aspiration du lanceur\n\n__Berserkeur, Poids Plume :__ Dégâts mono\n__Observateur, Tête Brûlée :__Dégâts en ligne\n__Idole, Altruiste :__ Soins sur toute l'équipe (et resurrection)\n__Mage, Enchanteur :__ Dégâts en cercle\n__Prevoyant, Protecteur :__ Armure sur l'équipe\n__Aventurier :__ Invoque \"Titania\"\n\nCette compétence utilise la statistique la plus élevée du lanceur\n\nUtiliser Transcendance vous empêche d'utiliser une compétence ultime lors du prochain tour",use=HARMONIE,shareCooldown=True)
burst = skill("Bombe ballon","ys",TYPE_DAMAGE,0,20,area=AREA_CIRCLE_1,sussess=60,emoji='<:burstBomb:887328853683474444>',use=HARMONIE)
lapSkill = skill("Invocation - Lapino","yr",TYPE_INVOC,0,invocation="Lapino",cooldown=4,shareCooldown=True,emoji='<:lapino:885899196836757527>',use=CHARISMA)
adrenaline = skill("Adrénaline","yq",TYPE_HEAL,250,60,cooldown=5,emoji='<:adrenaline:887403480933863475>',use=INTELLIGENCE)
blindage = skill("Blindage","yp",TYPE_BOOST,350,0,AREA_MONO,effect="mj",cooldown=3,use=None,emoji="<:blindage:897635682367971338>")
fermete = skill("Second Souffle","yo",TYPE_HEAL,350,80,AREA_MONO,emoji='<:secondWind:897634132639756310>',cooldown=5,use=ENDURANCE)
isolement = skill("Isolement","yn",TYPE_ARMOR,500,70,AREA_MONO,emoji='<:selfProtect:887743151027126302>',cooldown=5,effect="ml")
bombRobot = skill("Invocation - Bombe Robot","ym",TYPE_INVOC,500,0,AREA_CIRCLE_3,invocation="Bombe Robot",cooldown=2,shareCooldown=True,emoji='<:autobomb:887747538994745394>',use=STRENGTH)
linx = skill("Œuil de Linx","yl",TYPE_BOOST,500,range=AREA_MONO,area=AREA_CIRCLE_2,emoji='<:noeuil:887743235131322398>',effect="mm",cooldown=4)
stalactic = skill("Stalactite","yk",TYPE_DAMAGE,300,60,emoji='<:stalactit:889089667088142346>',cooldown=3,sussess=60,range=AREA_DIST_5)
uppercut = skill("Uppercut","yj",TYPE_DAMAGE,200,50,AREA_CIRCLE_1,emoji='<:uppercut:889091033718194196>',cooldown=2,message="{0} donne un {1} à {2} :")
oneforall = skill("Un pour tous","yi",TYPE_BOOST,500,range=AREA_MONO,area=AREA_DONUT_2,cooldown=5,use=CHARISMA,effect="mo",effectOnSelf="mp",description="Une compétence qui permet d'augmenter les résistances de ses alliés au détriment des siennes",conditionType=["exclusive","aspiration",ALTRUISTE],emoji='<:oneforall:893295824761663488>')
secondSun = skill("Le second Soleil","yh",TYPE_MALUS,350,0,AREA_MONO,area=AREA_ALL_ENNEMIES,cooldown=5,effect="mq",emoji='<:iwanttosleeppls:893241882484817920>',use=CHARISMA,conditionType=["exclusive","element",ELEMENT_LIGHT])
kiss = skill("Baisé divin","yg",TYPE_HEAL,69,50,AREA_DONUT_2,emoji='<:welp:893251469439008809>',message="{0} fait un gros bisou à {2} :")
onstage = skill("En scène !","yf",TYPE_BOOST,750,0,AREA_MONO,["exclusive","aspiration",IDOLE],True,effect="mr",emoji='<:alice:893463608716062760>',area=AREA_DONUT_7,use=CHARISMA,cooldown=5,message="{0} éléctrise l'ambience !")
icelance = skill("Lame glacée","ye",TYPE_DAMAGE,500,120,AREA_DIST_6,["exclusive","element",ELEMENT_WATER],True,emoji='<:emoji_47:893471252537298954>',cooldown=5,message="{0} fait appaître une lame de glace géante sous {2} :")
rocklance = skill("Lame rocheuse","yd",TYPE_DAMAGE,500,120,AREA_CIRCLE_3,["exclusive","element",ELEMENT_EARTH],True,emoji='<:emoji_46:893471231641276496>',cooldown=5,message="{0} fait appaître une lame de roche géante sous {2} :",use=MAGIE)
infinitFire = skill("Brasier","yc",TYPE_DAMAGE,500,90,AREA_DIST_5,["exclusive","element",ELEMENT_FIRE],True,emoji='<:emoji_44:893471208065101924>',cooldown=5,message="{0} déclanche un brasier autour de {2} :",area=AREA_LINE_3,use=MAGIE)
storm = skill("Ouragan","yb",TYPE_DAMAGE,500,90,AREA_CIRCLE_2,["exclusive","element",ELEMENT_AIR],True,emoji='<:emoji_44:893471179023732809>',cooldown=5,message="{0} déclanche un ouragan autour de {2} :",area=AREA_CIRCLE_2,use=MAGIE)
innerdarkness = skill("Ténèbres intérieurs","ya",TYPE_INDIRECT_DAMAGE,500,0,conditionType=["exclusive","element",ELEMENT_DARKNESS],ultimate=True,emoji='<:emoji_48:893471268957990982>',cooldown=5,effect="ms",use=MAGIE,area=AREA_CIRCLE_1)
divineLight = skill("Lumière divine",'xz',TYPE_INDIRECT_HEAL,500,conditionType=["exclusive","element",ELEMENT_LIGHT],ultimate=True,emoji='<:emoji_49:893471282815963156>',cooldown=5,effect=["mu","mv"],use=CHARISMA,area=AREA_CIRCLE_1)
swordDance = skill("Dance des sabres","xy",TYPE_DAMAGE,350,power=60,use=STRENGTH,emoji='<:sworddance:894544710952173609>',cooldown=3,area=AREA_CIRCLE_1)
shot = skill("Tir net","xx",TYPE_DAMAGE,350,75,AREA_MONO,emoji='<:shot:894544804321558608>',cooldown=3,use=STRENGTH,damageOnArmor=1.5)
percingLance = skill("Lance Perçante","xw",TYPE_DAMAGE,350,power=65,emoji='<:percing:894544752668708884>',cooldown=3,area=AREA_LINE_2,range=AREA_CIRCLE_2)
percingArrow = skill("Flèche Perçante","wv",TYPE_DAMAGE,350,power=60,emoji='<:percingarrow:887745340915191829>',cooldown=3,area=AREA_LINE_2,range=AREA_DIST_5)
highkick = skill("HighKick","wu",TYPE_DAMAGE,350,power=80,range=AREA_CIRCLE_1,emoji='<:highkick:894544734759030825>',cooldown=3)
multishot = skill("Tir Multiple","wt",TYPE_DAMAGE,350,power=60,range=AREA_DIST_4,emoji='<:name:894544834780622868>',cooldown=3,area=AREA_CONE_2)
bleedingArrow = skill("Flèche Hémoragique","ws",TYPE_DAMAGE,350,25,AREA_DIST_5,effect='mx',emoji='<:bleedingarrow:894544820071178292>')
bleedingDague = skill("Dague Hémoragique","wr",TYPE_DAMAGE,350,35,AREA_CIRCLE_2,effect='mx',emoji='<:bleedingdague:894552391444234242>')
affaiblissement = skill("Affaiblissement","wq",TYPE_MALUS,350,effect="my",cooldown=3,use=INTELLIGENCE,emoji='<:affaiblissement:894544690400071750>')
provo = skill("Provocation","wp",TYPE_MALUS,350,emoji='<:supportnt:894544669793476688>',effect='mz',cooldown=3,use=INTELLIGENCE)
flameche = skill("Flamèche","wo",TYPE_DAMAGE,100,30,area=AREA_CONE_2,use=MAGIE,conditionType=["exclusive","element",ELEMENT_FIRE])
flame = skill("Flme","wn",TYPE_DAMAGE,250,55,area=AREA_CONE_2,use=MAGIE,conditionType=["exclusive","element",ELEMENT_FIRE],cooldown=3)
pyro = skill("Pyrotechnie","wm",TYPE_DAMAGE,500,75,area=AREA_CONE_2,use=MAGIE,conditionType=["exclusive","element",ELEMENT_FIRE],cooldown=5)
ecume = skill("Ecume","wl",TYPE_DAMAGE,100,35,use=MAGIE,conditionType=["exclusive","element",ELEMENT_WATER])
courant = skill("Courant","wk",TYPE_DAMAGE,250,60,use=MAGIE,conditionType=["exclusive","element",ELEMENT_WATER],cooldown=3)
torant = skill("Torant","wk",TYPE_DAMAGE,500,80,use=MAGIE,conditionType=["exclusive","element",ELEMENT_WATER],cooldown=5)
brise = skill("Brise","wj",TYPE_DAMAGE,100,35,use=MAGIE,conditionType=["exclusive","element",ELEMENT_AIR],area=AREA_CIRCLE_1)
storm2 = skill("Tempête","wi",TYPE_DAMAGE,250,55,use=MAGIE,conditionType=["exclusive","element",ELEMENT_AIR],area=AREA_CIRCLE_1,cooldown=3)
tornado = skill("Tornade","wh",TYPE_DAMAGE,500,75,use=MAGIE,conditionType=["exclusive","element",ELEMENT_AIR],area=AREA_CIRCLE_1,cooldown=5)
stone = skill("Caillou","wg",TYPE_DAMAGE,100,35,use=MAGIE,conditionType=["exclusive","element",ELEMENT_EARTH])
rock = skill("Rocher","wf",TYPE_DAMAGE,250,60,use=MAGIE,conditionType=["exclusive","element",ELEMENT_EARTH],cooldown=3)
mont = skill("Montagne","we",TYPE_DAMAGE,500,80,use=MAGIE,conditionType=["exclusive","element",ELEMENT_EARTH],cooldown=5)

skills = [
    flameche,flame,pyro,ecume,courant,torant,brise,storm2,tornado,stone,rock,mont,bleedingArrow,bleedingDague,swordDance,shot,percingArrow,percingLance,highkick,multishot,rocklance,infinitFire,storm,innerdarkness,divineLight,icelance,onstage,kiss,secondSun,oneforall,uppercut,stalactic,linx,bombRobot,isolement,fermete,blindage,adrenaline,lapSkill,burst,trans,descart,thinkSkill,invocFee,invocCarbT,invocCarbE,splashdown,multiMissiles,monoMissiles,invocBat,poisonus,protect,explosion,splatbomb,healAura,cure,firstheal,balayette,contrecoup,boom,chaos,unHolly,soupledown,inkarmor,coffeeSkill,theSkill,gpotion,bpotion,zelian,courage,nostalgia,draw25,siropMenthe
]

def addAllInSkillData():
    for a in skills:
        try:
            stuffDB.create_skill(a)
        except:
            stuffDB.edit_skill(a)

# Invocations
batWeap = weapon("Griffe","aaa",RANGE_MELEE,AREA_CIRCLE_1,25,70,0,emoji='<:griffe:884889931359596664>')
carbunE = weapon("Coup de vent","aab",RANGE_LONG,AREA_CIRCLE_5,20,70,0,emoji='<:vent:884889843681853460>',area=AREA_CIRCLE_1,use=MAGIE)
carbunSkill = skill("Rafale","aac",TYPE_DAMAGE,0,35,area=AREA_CIRCLE_2,sussess=55,emoji='<:rafale:884889889445912577>',use=MAGIE,cooldown=4)
carbunTSKill = skill("Eclat de Topaze","aad",TYPE_DAMAGE,0,35,AREA_MONO,area=AREA_CIRCLE_2,sussess=80,cooldown=4,emoji="<:eclattopaze:884889967397056512>",use=ENDURANCE)
feeWeap = weapon("Embrassement","aae",RANGE_DIST,AREA_CIRCLE_4,15,100,0,type=TYPE_HEAL,use=CHARISMA,emoji="<:feerie:885076995522834442>",target=ALLIES,area=AREA_CIRCLE_1)
feeEffect = effect("Murmure de l'aurore","aaf",CHARISMA,type=TYPE_INDIRECT_HEAL,power=8,emoji=uniqueEmoji('<:feerie:885076995522834442>'),trigger=TRIGGER_START_OF_TURN,turnInit=2,stackable=True)
feeSkill = skill("Murmure de l'aurore","aag",TYPE_INDIRECT_HEAL,0,0,AREA_MONO,cooldown=3,area=AREA_CIRCLE_3,emoji="<:feerie:885076995522834442>",effect=feeEffect)
titWeap = weapon("Arme","aah",RANGE_MELEE,AREA_CIRCLE_2,15,70,0,0,0,0,0,0,0,0,0,0,3,emoji='<:magicalBonk:886669168408137749>',area=AREA_CONE_2) 
lapinoWeap = weapon("Murmure de guérison","aai",RANGE_DIST,AREA_CIRCLE_3,20,100,0,0,0,0,0,0,0,0,0,0,0,'<:defHeal:885899034563313684>',type=TYPE_HEAL,target=ALLIES,message="{0} encourage doucement {1} :")
lapinoSkill = skill("Murmure de dévoument","aaj",TYPE_HEAL,0,30,emoji='<:defHeal:885899034563313684>',cooldown=4)
batSkill = skill("Cru-aile","aak",TYPE_DAMAGE,0,15,AREA_CIRCLE_2,emoji='<:defDamage:885899060488339456>',use=AGILITY)
autoWeap = weapon("NoneWeap","aal",RANGE_MELEE,AREA_CIRCLE_1,0,0,0,emoji="<:empty:866459463568850954>")
autoEff = effect("Explosé","aam",trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,power=9999,emoji=emojiMalus,silent=True)
autoSkill = skill("Explosion","aan",TYPE_DAMAGE,0,75,AREA_MONO,emoji='<:defDamage:885899060488339456>',area=AREA_CIRCLE_1,effectOnSelf=autoEff)

batInvoc = invoc("Chauve-Souris",aspiration=TETE_BRULE,strength=[PURCENTAGE,1],endurance=[PURCENTAGE,0.5],charisma=[PURCENTAGE,0.6],agility=[PURCENTAGE,1],precision=[PURCENTAGE,0.8],intelligence=[PURCENTAGE,0.8],magie=[PURCENTAGE,0.5],resistance=20,percing=0,critical=30,icon=["<:bat1:884519906819862568>","<:bat2:884519927208357968>"],gender=GENDER_FEMALE,weapon=batWeap,description="Une invocation de mêlée peu resistante, mais sans tant de rechargement",skill=[batSkill],element=ELEMENT_AIR)
carbuncleE = invoc("Carbuncle Emeraude",[PURCENTAGE,0.8],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.8],[PURCENTAGE,0.8],[PURCENTAGE,1.1],[PURCENTAGE,0.5],20,10,[PURCENTAGE,2],TETE_BRULE,["<:ce1:884889724114841610>","<:ce2:884889693374775357>"],carbunE,[carbunSkill],description="Une invocation utlisant son **Intelligence** pour vaincre des groupes d'ennemis de loin",element=ELEMENT_FIRE)
carbuncleT = invoc("Carbuncle Topaze",[PURCENTAGE,0.8],[PURCENTAGE,2.5],[PURCENTAGE,0.6],[PURCENTAGE,0.8],[PURCENTAGE,0.8],[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,1],0,10,BERSERK,["<:ct1:884889748274028666>","<:ct2:884889807111749662>"],batWeap,[carbunTSKill],description="Une invocation résistante qui n'a pas froid au yeux et viendra sauter dans la mêlée",element=ELEMENT_AIR)
feeInv = invoc("Fée soignante",[PURCENTAGE,0.5],[PURCENTAGE,0.8],[PURCENTAGE,1],[PURCENTAGE,1],[PURCENTAGE,0.8],[PURCENTAGE,0.8],[PURCENTAGE,0.5],10,0,0,ALTRUISTE,["<:fee1:885076945333805086>","<:fee2:885076961695760386>"],feeWeap,[feeSkill],gender=GENDER_FEMALE,description="Une fée qui soigne ses alliés grace à sa magie curative",element=ELEMENT_LIGHT)
titania = invoc("Titania",[HARMONIE],[HARMONIE],[PURCENTAGE,1],[PURCENTAGE,1],[PURCENTAGE,1],[PURCENTAGE,1],[PURCENTAGE,0.5],25,10,25,OBSERVATEUR,["<:tita1:886663550796431390>","<:tita2:886663565220651028>"],titWeap,[],GENDER_FEMALE,ELEMENT_AIR)
lapino = invoc("Lapino",[PURCENTAGE,0.5],[PURCENTAGE,1],[PURCENTAGE,1],[PURCENTAGE,0.8],[PURCENTAGE,0.8],[PURCENTAGE,0.5],[PURCENTAGE,0.5],10,0,0,ALTRUISTE,['<:lapino1:885899366966112266>','<:lapino2:885899382539571221>'],lapinoWeap,[lapinoSkill],description="Fidèle Lapino d'Hélène, il la suit partout là où elle aura besoin de lui",element=ELEMENT_LIGHT)
autoBomb = invoc("Bombe Robot",[PURCENTAGE,0.8],50,0,0,0,0,0,20,0,0,INVOCATEUR,["<:auto1:887747795497394267>","<:auto2:887747819866312735>"],autoWeap,[autoSkill])

invocTabl = [autoBomb,lapino,titania,feeInv,carbuncleT,carbuncleE,batInvoc]

# Stuff
uniform = stuff("Uniforme Scolaire","hd",1,100,intelligence=5,magie=5,charisma=10,emoji='<:uniform:866830066008981534>',orientation=[None,BOOSTER],affinity=ELEMENT_WATER)
blueSnekers = stuff("Tennis Montantes Bleues","he",2,100,agility=10,endurance=5,charisma=5,emoji='<:blueHotTop:866795241721954314>')
redSnekers = stuff("Tennis Montantes Rouge","hg",2,100,strength=10,endurance=5,resistance=5,emoji='<:redHopTop:866782609464098887>')
encrifuge = stuff("Tenue Encrifugée","hh",1,350,endurance=5,resistance=5,effect="ld",emoji='<:encrifuge:871878276061212762>',orientation=[TANK])
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
amethystEarRings = stuff("Boucles d'oreilles en améthyste","hw",0,200,10,charisma=10,precision=10,percing=10,resistance=-10,critical=-10,emoji='<:amethystEarRings:870391874081419345>',position=1,affinity=ELEMENT_DARKNESS)
anakiMask = stuff("Masque Annaki","hx",0,150,endurance=10,charisma=5,precision=10,resistance=-5,emoji='<:anakiMask:870806374009954345>',position=2)
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
barrette = stuff("Barette Seiche","is",0,100,charisma=10,precision=10,emoji='<:squidBar:878718467434491934>')
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
blueFlat = stuff("Ballerines Blues","je",2,100,magie=15,charisma=10,resistance=-5,emoji='<:blueflat:881209954902638602>',orientation=[DISTANCE,BOOSTER])
redFlat = stuff("Ballerines Rouges","jf",2,100,20,resistance=-5,percing=5,emoji='<:redflat:881209970568364173>',orientation=[DISTANCE,DPT])
redHeels = stuff("Escarpins Rouges","jg",2,150,strength=20,resistance=-10,percing=10,emoji='<:heelsRed:881339121795215410>',orientation=[DISTANCE,DPT])
whiteHeels = stuff("Escarpins Blancs","jh",2,150,charisma=15,intelligence=15,resistance=-10,emoji='<:heelsWhite:881339137410609162>',orientation=[DISTANCE,BOOSTER])
blackHeels = stuff("Escarpins Noirs","ji",2,150,10,percing=10,endurance=10,resistance=10,agility=-20,emoji='<:heelsBlack:881339167357935616>',orientation=[TANK,DPT])
heroHead = stuff("Casque Héroïque","jj",0,250,20,-10,percing=10,emoji='<:heroicheadset:881326928802496562>',orientation=[DISTANCE,DPT])
heroBody = stuff("Veste Héroïque","jk",1,250,10,10,precision=10,magie=-10,emoji='<:herojacket:881326964328255508>',orientation=[DISTANCE,DPT])
heroShoe = stuff("Baskets Héroïques","jl",2,250,strength=10,critical=5,percing=5,emoji='<:heroshoe:881326998511833098>',orientation=[DISTANCE,DPT])
intemCharpe = stuff("Echarpe Intemporelle","jm",0,250,charisma=25,precision=-5,emoji='<:intemcharpe:882006603350568960>',orientation=[None,HEALER],position=2)
intemNorak = stuff("Anorack Intemporel","jn",1,250,charisma=20,resistance=10,strength=-5,percing=-5,emoji='<:intemnorak:882006589870075944>',orientation=[DISTANCE,HEALER])
intemShoe = stuff("Tennis Montantes Intemporelles","jo",2,250,charisma=30,resistance=5,percing=-15,emoji='<:intemtennis:882006616961073253>',orientation=[DISTANCE,HEALER])
patacasque = stuff("Casque Patapoutre","jp",0,200,resistance=10,endurance=10,orientation=[TANK,None],emoji='<:patacasque:881334720732991529>')
patabottes = stuff("Bottes Patapoutres","jq",2,200,resistance=15,endurance=5,orientation=[TANK,None],emoji='<:pataboots:881334739183730689>')
lunettesOv = stuff("Lunettes ovales","jr",0,100,strength=10,precision=10,emoji='<:lunettesovales:881965054830997534>',orientation=[None,DPT])
masqueTub = stuff("Masque et tuba","js",0,100,resistance=10,precision=10,emoji='<:masqieTubas:881965193100406785>',orientation=[TANK,None])
casqueColor = stuff("Casque coloré","jt",0,150,charisma=15,intelligence=15,agility=-5,precision=-5,emoji="<:colorheadset:881326908149727253>",orientation=[None,BOOSTER])
blingbling = stuff("Lunettes 18 karas","ju",0,100,5,5,5,5,-5,-5,5,5,emoji='<:lunettes18kara:881965006483251263>')
legendaryHat = stuff("Exelo","jw",0,300,endurance=10,resistance=5,strength=10,agility=-5,emoji='<:excelot:882727033782812702>',orientation=[TANK,DPT])
robeDrac = stuff("Robe draconique","jv",1,250,strength=-30,endurance=15,intelligence=20,resistance=15,emoji='<:robedraco:878572815807287297>',orientation=[TANK,DPT])
robeLoliBlue = stuff("Robe Lolita Bleue","jx",1,300,-10,0,10,0,0,0,30,-10,emoji="<:blueLolita:884212751881363467>",orientation=[DISTANCE,MAGIC])
old = stuff("Vieux porte-clefs","jy",0,200,intelligence=10,magie=15,agility=-15,strength=10,emoji='<:old:885086171754012702>',affinity=ELEMENT_WATER,position=4)
batRuban = stuff("Noeud Chauve-Souris","jz",0,0,charisma=40,intelligence=20,strength=-20,resistance=-10,percing=-10,orientation=[LONG_DIST,HEALER],emoji='<:batRuban:887328511222763593>',position=3)
FIACNf = stuff("Robe du FIACN","ka",1,0,40,10,resistance=15,agility=-20,precision=-15,magie=-10,emoji='<:FIACNF:887328531774836736>',orientation=[TANK,DPT])
FIACNh = stuff("Gilet du FIACN","kb",1,0,40,10,resistance=15,agility=-20,precision=-15,magie=-10,emoji='<:FIACNH:887328549437059172>',orientation=[TANK,DPT])
heleneDress = stuff("Robe bleue d'Hélène","kc",1,0,charisma=25,intelligence=20,strength=-20,endurance=-15,emoji='<:heleneDress:888745359365525535>',effect='mk',affinity=ELEMENT_LIGHT,orientation=[DISTANCE,HEALER])
heleneShoe = stuff("Babies bleues d'Hélène","kd",2,0,strength=-10,charisma=25,intelligence=5,emoji='<:blueBabie:887857026477207592>',orientation=[DISTANCE,HEALER])
corset = stuff("Corset d'Ordin","ke",1,500,10,0,-5,0,25,-10,emoji="<:corsetordin:887757308157886465>",orientation=[DISTANCE,None])
ggshield = stuff("Bouclier GG","kf",0,500,endurance=20,resistance=15,agility=-15,emoji='<:emoji_8:887757446658023496>',orientation=[TANK,None],position=4)
fecaShield = stuff("Bouclier Feca","kg",0,1000,-20,15,resistance=25,emoji='<:fecashield:887757399736348722>',affinity=ELEMENT_EARTH,orientation=[TANK,None],position=4)
kanisand = stuff("Sandales Kannivore","kh",2,250,agility=20,emoji="<:sandaleskannivores:887755801161240577>",affinity=ELEMENT_AIR)
tsarine = stuff("Starine","ki",0,500,resistance=15,intelligence=10,endurance=10,precision=-15,emoji='<:tsarine:887755891913396245>',orientation=[TANK,None])
dracBoot = stuff("Bottes Draconiques","kj",2,500,-10,20,resistance=10,intelligence=10,agility=-10,emoji='<:bottesdraco:885080377234968608>',orientation=[TANK,None])
darkMaidFlats = stuff("Ballerines de soubrette des Ténèbres","kk",2,500,10,10,agility=25,resistance=10,charisma=-15,precision=-10,magie=-10,emoji='<:linaflats:890598400624586763>',orientation=[TANK,DPT],affinity=ELEMENT_DARKNESS)
darkMaidDress = stuff("Robe de soubrette des Ténèbres","kl",1,500,15,10,agility=15,resistance=15,precision=-5,charisma=-20,magie=-10,emoji="<:linadress:890598423152185364>",orientation=[TANK,DPT],affinity=ELEMENT_DARKNESS)
darkMaidPendants = stuff("Boucles d'oreilles de soubrette des Ténèbres","km",0,500,10,10,-10,25,-10,-10,resistance=5,emoji='<:linapendant:890599104902754326>',orientation=[TANK,DPT],affinity=ELEMENT_DARKNESS,position=1)
darkbabie = stuff("Babies noires","kn",2,250,20,-20,precision=20,emoji='<:bbabies:892351703230320670>',affinity=ELEMENT_DARKNESS)
krysCorn = stuff("Serre-Tête en KrysTal","ko",0,250,endurance=15,resistance=10,agility=-5,emoji='<:krysCorn:892350678620586004>',affinity=ELEMENT_EARTH)
shihuDress = stuff("Robe de matelot noire d'encre","kp",1,750,-20,0,magie=35,critical=5,emoji='<:shihudress:896916995948302336>')
shihuShoe = stuff("Babies noire d'encre","kq",2,750,-20,agility=-10,magie=25,critical=5,emoji='<:shihubabies:896914810225188895>')
mageDress = stuff("Coule du mage noir","kr",1,500,-20,agility=10,precision=10,magie=25,resistance=-5,emoji='<:bmage:896912954744795177>')
mageShoe = stuff("Bottines de mage noir",'ks',2,500,-10,endurance=-10,magie=15,precision=15,emoji='<:bmageshoe:896913235884802090>')
tankmage1 = stuff("Armure du mage de combat",'kt',1,500,-30,20,resistance=10,magie=20)
tankmage2 = stuff("Bottes du mage de combat",'ku',2,500,charisma=-20,agility=20,resistance=15,magie=15,intelligence=-10)
tankmage3 = stuff("Heaume du mage de combat",'kv',0,500,-20,20,resistance=10,magie=10)
shihuHat = stuff("Berêt de matelot noir d'encre",'kw',0,750,magie=25,critical=10,strength=-10,intelligence=-5,emoji='<:shihuhat:897631090557206578>')
indeci1 = stuff("Chapeau du mage indécis",'kx',0,750,strength=15,magie=15,intelligence=-5,charisma=-5)
indeci2 = stuff("Veste du mage indécis",'ky',1,750,strength=15,magie=15,precision=-5,agility=-5,emoji='<:rmjakect:897631127760691240>')
indeci3 = stuff("Bottes du mage indécis",'k7',2,750,strength=15,magie=15,charisma=-5,agility=-5,emoji='<:rmboots:897631140557516840>')
hyperlink = stuff("[[Hyperlink blocked]]",'kz',2,1997,35,intelligence=35,charisma=-25,magie=-25,emoji='<:blocked:897631107602841600>')

stuffs =[shihuDress,shihuShoe,mageDress,mageShoe,tankmage1,tankmage2,tankmage3,shihuHat,indeci1,indeci2,indeci3,hyperlink,darkbabie,krysCorn,darkMaidDress,darkMaidFlats,darkMaidPendants,dracBoot,tsarine,kanisand,fecaShield,ggshield,corset,heleneShoe,heleneDress,FIACNf,FIACNh,batRuban,old,robeLoliBlue,legendaryHat,robeDrac,blingbling,lunettesOv,masqueTub,casqueColor,patacasque,patabottes,intemNorak,intemShoe,intemCharpe,heroHead,heroBody,heroShoe,blackHeels,whiteHeels,redHeels,redFlat,blueFlat,camoHat,purpleBasket,amethystEarRings,legendaryBoots,legendaryTunic,pinkSneakers,pinkRuban,maidHat,maidHeels,maidDress,squidEarRings,barrette,pataarmor,redDress,pinkShirt,flum,headSG,bodySG,shoeSG,bikini,batPendant,catEars,heartLocket,blackSnelers,schoolShoes,woodenSandals,abobination,pullCamo,blackShirt,pullBrown,bbandeau,bshirt,bshoes,uniform,blueSnekers,redSnekers,encrifuge,pinkFlat,blackFlat,batEarRings,ironHelmet,determination,pinkDress,oldBooks,jeanJacket,blackJeanJacket,whiteSneakers,anakiMask,whiteBoots,mustangBoots]

octoEmpty1 = stuff("placeolder","ht",0,0)
octoEmpty2 = stuff("placeolder","hu",0,0)
octoEmpty3 = stuff("placeolder","hv",0,0)

def addAllInStuffData():
    for a in stuffs:
        try:
            stuffDB.create_gear(a)
        except:
            stuffDB.edit_gear(a)

hourglassEmoji = [['<:hourglass1:872181651801772052>','<:hourglass2:872181632801603644>'],['<:hourglass1:872181651801772052>','<:hourglass2:872181632801603644>'],['<:hourglass1:872181651801772052>','<:hourglass2:872181632801603644>']]

def sameSpeciesEmoji(team1,team2):
    return [[team1,team2],[team1,team2],[team1,team2]]

#Effect
armor = effect("Armure d'Encre","la",INTELLIGENCE,overhealth=80,emoji=sameSpeciesEmoji('<:armor1:866828463751036929>','<:armor2:866828487038205962>'),description="Donne de l'armure à tous les alliés",trigger=TRIGGER_DAMAGE)
coffee = effect("Caféiné","lb",2,strength=10,endurance=10,reject=["mc"],description="Boost la force et l'endurance de tous les alliés",emoji=uniqueEmoji("<:coffee:867538582846963753>"))
the = effect("Théiné","lc",2,agility=5,precision=5,intelligence=15,magie=10,reject=["mc"],description="Boost l'agilité et la précision de tous les alliés",emoji=uniqueEmoji('<:the:867538602644602931>'))
encrifugeEff = effect(encrifuge.name,"ld",emoji=uniqueEmoji(encrifuge.emoji), overhealth=1,description="Au début du combat, vous protège du premier coup reçu",turnInit=-1,trigger=TRIGGER_DAMAGE)
gpEffect = effect("Potion tonifiante","le",5,5,5,5,5,5,0,5,5,5,turnInit=2,description="Vos connaissances en alchimie vous permettent de booster toutes vos statistiques pour le prochain tour")
bpEffect = effect("Potion étrange","lf",5,-5,-5,-5,-5,-5,-5,-5,-5,-5,turnInit=1,description="Vos connaissances en alchimie vous permettent de baisser toutes les statistiques d'un adversaire pendant un tour",emoji = emojiMalus)
deterEff1 = effect("Détermination","lg",emoji=uniqueEmoji(determination.emoji),turnInit=-1,description="Sur le points de mourir, votre volonté vous permet de tenir jusqu'à votre prochain tour",trigger=TRIGGER_DEATH,callOnTrigger="lh",power=1,type=TYPE_INDIRECT_REZ)
undying = effect("Undying","lh",reject=["li","lj"],turnInit=2,trigger=TRIGGER_END_OF_TURN,onTrigger=[0,9999,DAMAGE_FIXE],immunity=True,description="Vos dernières forces pour rendent insensible à toutes attaques.\nMais à la fin de votre tour, vous mourrerez, pour de bon.",callOnTrigger="li",type=TYPE_INDIRECT_DAMAGE,power=9999,ignoreImmunity=True)
onceButNotTwice = effect("Une fois mais pas deux","li",emoji=uniqueEmoji('<:notTwice:867536068110057483>'),description="La mort ne vous laissera pas filer une seconde fois",turnInit=-1,silent=True)
zelianR = effect("Chronoshift","lj",PURCENTAGE,trigger=TRIGGER_DEATH,description = "Si le porteur venait à mourir tant qu'il porte cet effet, il est réssucité avec la moitié de sa vie",emoji=[['<:chronoshift1:867877564864790538>','<:chronoshift2:867877584518905906>'],['<:chronoshift1:867877564864790538>','<:chronoshift2:867877584518905906>']],reject=["lh","li"],type=TYPE_INDIRECT_REZ,power=50)
courageE = effect("Motivé","lk",2,15,emoji=sameSpeciesEmoji('<:charge1:866832660739653632>','<:charge2:866832677512282154>'))
nostalgiaE = effect("Nostalgie","lm",5,-10,resistance=-10,emoji=emojiMalus)
afterShockDmg = effect("Contre coup","ln",MAGIE,turnInit=1,power=25,lvl=3,trigger=TRIGGER_DAMAGE,type=TYPE_INDIRECT_DAMAGE,emoji=sameSpeciesEmoji('<:aftershock1:882889524122898452>','<:aftershock2:882889538886852650>'))
octoshield = effect("Bouclier Octarien","lo",agility=-100,overhealth=200,emoji=armor.emoji,turnInit=-1,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR)
inkBrellaEff = effect("Toile du para-encre","lp",None,-10,agility=-10,overhealth=50,turnInit=-1,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji('<:splatbrellareverse:876079630749147196>'),description="Commencez le combat avec un peu d'armure !\nCependant, vous subirez un malus d'agilité et de force tant que celle-ci est active")
stopAttacking = effect("Stop attacking or draw 25","lq",None,trigger=TRIGGER_DEALS_DAMAGE,type=TYPE_INDIRECT_DAMAGE,power=25,emoji=emojiMalus,description="Vous jouez votre jocker !\nSi le porteur de l'état attaque, il subit 25 dégâts fixe")
poidPlumeEff = effect("Poids Plume","lr",None,trigger=TRIGGER_END_OF_TURN,silent=True,lvl=0,type=TYPE_UNIQUE,unclearable=True,turnInit=-1)
hunter = effect("Chasseur","ls",None,emoji=uniqueEmoji('<:chasseur:871097673334276096>'),trigger=TRIGGER_DEATH,type=TYPE_UNIQUE,description="Un chasseur sachant chasser sans son chien a toujours une dernière carte à jouer",turnInit=-1)
hunterBuff = effect("Hunterbuff","lt",None,critical=100,precision=500,silent=True)
menthe = effect("Mentiné","lu",INTELLIGENCE,percing=5,resistance=5,critical=10,reject=["mc"],description="Boost la résistance, la pénétration et le critique de vos alliés",emoji=uniqueEmoji('<:menthe:867538622797054042>'))
badaboum = effect("Ça fait bim bam boum","lv",MAGIE,emoji=emojiMalus,turnInit=2,trigger=TRIGGER_DEATH,power=50,type=TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_2)
charme = effect("Sous le charme","lw",CHARISMA,-10,resistance=-10,magie=-10,emoji=emojiMalus,description="Heu peut-être plus tard la description",type=TYPE_MALUS)
jetlag = effect("Jetlag",'ly',None,emoji=uniqueEmoji('<:jetlag:872181671372402759>'),silent=True,description="Le porteur de cet effet est insenssible aux sorts/armes de type \"Sablier\"")
hourglass1 = effect("Rollback","lx",None,trigger=TRIGGER_ON_REMOVE,type=TYPE_UNIQUE,emoji=hourglassEmoji,description="Lorsque l'initiateur de cet effet commence son prochain tour, le porteur récupèrera 75% des PV perdues depuis que cet effet est actif",reject=[jetlag])
lightAura = effect("Aura de Lumière","ly",CHARISMA,turnInit=3,power=15,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_END_OF_TURN,emoji=sameSpeciesEmoji("<:AdL1:873549174052892672>","<:AdL2:873549232601182249>"),description="Bénissez vos alliés proches et offrez leur des soins sur plusieurs tours",area=AREA_CIRCLE_2)
flumEffect = effect("Douce lueur","lz",None,power=10,turnInit=-1,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji=uniqueEmoji(flum.emoji))
dephased = effect("Déphasée","ma",None,emoji=uniqueEmoji('<a:dephasee:882042949494525973>'),description="Ailill n'aime pas affronter trop d'ennemi à la fois, ni ceux qui essaye de l'avoir de loin",type=TYPE_UNIQUE,turnInit=-1)
stuned = effect("Etourdi","mb",emoji=uniqueEmoji('<:stun:882597448898474024>'),turnInit=4,stun=True)
defensive = effect("Orbe défensif","md",emoji=sameSpeciesEmoji('<:orbe1:873725384359837776>','<:orbe2:873725400730202123>'),overhealth=40,description='Donne de l\'armure à un allié',stat=INTELLIGENCE,trigger=TRIGGER_DAMAGE,turnInit=1)
cafeine = effect("Désaltéré","mc",emoji=uniqueEmoji('<:cafeine:883253781024870401>'),turnInit = 4, description = "L'abus de caféine (ou théine c' est la même chose) est dangereureux pout la santé",silent=True)
estal = effect("Poison d'Estialba","me",emoji=uniqueEmoji('<:estialba:884223390804766740>'),turnInit=3,stat=MAGIE,description="Un virulant poison, faisant la sinistre renommée des fées de cette île",trigger=TRIGGER_START_OF_TURN,stackable=True,power=25,type=TYPE_INDIRECT_DAMAGE,lvl=3)
missiles = effect("Ciblé","mf",emoji=uniqueEmoji('<:tentamissile:884757344397951026>'),stat=STRENGTH,description="Au début de son tour, le ciel tombera sur la tête du Ciblé et ses alliés proches !",trigger=TRIGGER_START_OF_TURN,power=20,type=TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_1)
octoboum = effect("Explosion à venir !!","mg",emoji=uniqueEmoji(explosion.emoji),turnInit=3)
think = effect("REFLECHIS !","mh",CHARISMA,intelligence=10)
iThink = effect("Philosophé","mi",intelligence=10,magie=10,turnInit=3)
blinde = effect("Blindé","mj",resistance=20,description="Réduit les degâts subis de 20% jusqu'à votre prochain tour")
const = effect("Constitution","mk",emoji=uniqueEmoji('<:constitution:888746214999339068>'),description="Augmente de 30 les PV max de base de toute votre équipe",turnInit = -1)
isoled = effect("Isolé","ml",emoji=uniqueEmoji('<:selfProtect:887743151027126302>'),description="S'isoler mentalement pôur ne pas faire attention au dégâts",overhealth=70,stat=INTELLIGENCE)
nouil = effect("Œuil de Linx","mm",emoji=uniqueEmoji('<:noeuil:887743235131322398>'),precision=30)
lostSoul = effect("Âme en peine","mn",emoji=uniqueEmoji('<:lostSoul:887853918665707621>'),turnInit=3,trigger=TRIGGER_ON_REMOVE,silent=True,type=TYPE_UNIQUE)
oneforallbuff = effect("Un pour tous - Bonus","mo",resistance=10,stat=CHARISMA,description="Vos capacités défensives sont augmentées au détriment de celle du lanceur de cette compétence")
oneforalldebuff = effect("Un pour tous - Malus","mp",resistance=-33,type=TYPE_MALUS,emoji=emojiMalus,description="Vos capacités défenses sont dimunuées pour augmenter celles de vos alliés")
secondSuneff = effect("Insomnie","mq",CHARISMA,agility=-5,precision=-10,type=TYPE_MALUS,emoji=emojiMalus,description="Vous êtes en train d'expérimenter la joie d'avoir un lampadaire devant une fênetre sans rideau")
onstageeff = effect("Euphorie","mr",CHARISMA,10,10,10,10,10,10,5,3,3,description="C'est le moment de tout donner !",emoji=uniqueEmoji(onstage.emoji))
innerdarknessEff = effect("Ténèbres intérieurs","ms",MAGIE,power=100,type=TYPE_INDIRECT_DAMAGE)
lightspellshield = effect("Bouclier de lumière","mt",INTELLIGENCE,overhealth=10,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
lighteff = effect("Illuminé","mu",INTELLIGENCE,overhealth=35,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
lightHealeff = effect("Illuminé","mv",CHARISMA,power=35,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN)
darkspellbookeff = effect("Eclair sombre","mw",MAGIE,power=50,area=AREA_CIRCLE_1,trigger=TRIGGER_START_OF_TURN)
hemoragie = effect("Hémoragie","mx",STRENGTH,power=15,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,turnInit=3,stackable=True,lvl=3,emoji=uniqueEmoji('<:bleeding:887743186095730708>'))
affaiEffect = effect("Affaiblissement","my",INTELLIGENCE,-10,endurance=-10,resistance=-5,type=TYPE_MALUS,emoji=emojiMalus)
stupid = effect("Provoqué","mz",INTELLIGENCE,charisma=-10,intelligence=-10,type=TYPE_MALUS,emoji=emojiMalus)

enchant = effect("Enchanté","na",None,turnInit=-1,silent=True,type=TYPE_UNIQUE,unclearable=True,trigger=TRIGGER_DAMAGE)
proMalus = effect("Protecteur - Malus","nb",None,strength=-10,magie=-10,type=TYPE_MALUS)

effTB2 = [effect("Tête Brûlée","effTB",None,turnInit=-1,silent=True,type=TYPE_UNIQUE,unclearable=True)]
effMag2 = [effect("Mage","effMage",None,turnInit=-1,silent=True,type=TYPE_UNIQUE,unclearable=True)]

effTransShield = effect("Transcendance - Armure","transArm",INTELLIGENCE,overhealth=130,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)

chaosProhib = [undying,deterEff1,poidPlumeEff,dephased,cafeine,octoboum,const,lostSoul,onceButNotTwice,zelianR,octoshield]

effects = [affaiEffect,stupid,hemoragie,innerdarknessEff,darkspellbookeff,lighteff,lightHealeff,lightspellshield,onstageeff,secondSuneff,oneforallbuff,oneforalldebuff,lostSoul,nouil,isoled,const,blinde,iThink,think,octoboum,missiles,estal,cafeine,defensive,stuned,flumEffect,lightAura,hourglass1,jetlag,charme,armor,coffee,the,encrifugeEff,gpEffect,bpEffect,deterEff1,undying,onceButNotTwice,zelianR,afterShockDmg,octoshield,nostalgiaE,inkBrellaEff,stopAttacking,poidPlumeEff,hunter,hunterBuff,menthe,badaboum,courageE]
hourglassEffects = [hourglass1]

#Other
changeAspi = other("Changement d'aspiration","qa",description="Vous permet de changer d'aspiration",emoji='<:changeaspi:868831004545138718>')
changeAppa = other("Changement d'apparence","qb",description="Vous permet de changeer votre genre, couleur et espèce",emoji='<:changeAppa:872174182773977108>',price=500)
changeName = other("Changement de nom","qc",description="Vous permet de changer le nom de votre personnage",emoji='<:changeName:872174155485810718>',price=500)
restat = other("Rénitialisation des points bonus","qd",description="Vous permet de redistribuer vos points bonus",emoji='<:restats:872174136913461348>',price=500)
elementalCristal = other("Cristal élémentaire","qe",500,description="Ces cristaux vous permettent de changer l'élément de votre personnage dans /inventory element (lvl 10)",emoji="<:krysTal:888070310472073257>")
customColor = other("Couleur personnalisée","qf",500,description="Vous permet de rentrer une couleur personnalisée pour votre personnage",emoji='<:changeColor:892350738322300958>')
seeshell = other("Super Coquillage","qd",500,description="Ce coquillage permet de changer son bonus iné dans /inventory bonus (lvl 25)")

others = [elementalCristal,customColor,changeAspi,changeAppa,changeName,restat]

tablAllOcta,tablAllAllies = [],[]

# Bonus iné
inkResis = effect("Pied au sec",1,emoji=uniqueEmoji('<:piedAuSec:810918749196648459>'),silent=True,turnInit=-1,description="Réduit les dégâts indirects de 20%",unclearable=True)
respawnPunish = effect("Retour Perdant",2,emoji=uniqueEmoji('<:retourPerdant:810918739637567489>'),silent=True,turnInit=-1,description="Augmente de 20% les dégâts infligés, mais augmente de 35% les dégâts reçu",unclearable=True)
speedup = effect("Course à Pied",3,emoji=uniqueEmoji('<:course:810918753197752401>'),silent=True,turnInit=-1,description="Lorsque vous êtes attaqué réduit la précision de base de l'arme de votre attaquant de 20% (Attaque en cours uniquement)",unclearable=True)
bombDefense = effect("Philtre à Explosion",4,emoji=uniqueEmoji('<:BDDX:810918653322330112>'),silent=True,turnInit=-1,description="Réduit les dégâts de zone subis sans être la cible principale de 20%",unclearable=True)
demolish = effect("Démolition",5,emoji=uniqueEmoji('<:demolition:810918751703793665>'),silent=True,turnInit=-1,description="Les dégâts infligés à l'armure sont augmentés de 20%",unclearable=True)
mpu = effect("Arme Principale +",6,emoji=uniqueEmoji('<:mainpowerup:895025631023210638>'),silent=True,turnInit=-1,description="La puissance de votre arme principale augmente de 10%",unclearable=True)
secondpu = effect("Arme Secondaire +",7,emoji=uniqueEmoji('<:subpowerup:895025042679820378>'),silent=True,turnInit=-1,description="La puissance de vos compétences directes non ultime augmente de 10%",unclearable=True)
specialpu = effect("Arme Spéciale +",8,emoji=uniqueEmoji('<:specialpowerup:895025042361049089>'),silent=True,turnInit=-1,description="La puissance de votre compétence ultime augmente de 10%",unclearable=True)
subsaver = effect("Encrémenteur Secondaire",9,emoji=uniqueEmoji('<:subinksaver:895025042042265690>'),silent=True,turnInit=-1,description="Le temps de rechargement de vos compétences non ultime est réduit de 20%",unclearable=True)
spesaver = effect("Jauge Spéciale +",10,emoji=uniqueEmoji('<:abilitycharge:895025042927259678>'),silent=True,turnInit=-1,description="Le temps de rechargement de votre compétence ultime est réduit de 25%",unclearable=True)


# Octarien
octoEm = '<:splatted1:727586364618702898>'
octoShieldWeap = weapon("Bouclier Octarien","aaa",0,AREA_CIRCLE_2,10,sussess=50,price=0,endurance=20,effect="lo",emoji=octoEm)
octoBallWeap = weapon("Balles rebondissantes","aaa",1,AREA_CIRCLE_3,20,30,0,repetition=3,strength=10,agility=10,emoji=octoEm)
octoSnipeWeap = weapon("Snipeur Octarien","aaa",2,AREA_CIRCLE_6,50,50,0,strength=20,emoji=octoEm)
octoFly = weapon("Machinerie volante","aaa",RANGE_DIST,AREA_CIRCLE_3,40,40,0,10,emoji=octoEm)
octoHeal = weapon("Octo heal","aaa",1,AREA_CIRCLE_3,35,50,0,type=TYPE_HEAL,target=ALLIES,emoji='<:medic:882890887120699444>')
octoDef = weapon('OctoDef',"aaa",1,AREA_CIRCLE_3,0,100,0,effectOnUse="md",target=ALLIES,type=TYPE_HEAL,intelligence=20)
flyfishweap = weapon("Flyfish","aaa",2,AREA_CIRCLE_7,0,100,0,effectOnUse="mf",type=TYPE_INDIRECT_DAMAGE,strength=30)
octoBoumWeap = weapon("noneWeap","aaa",1,AREA_CIRCLE_1,0,0,0,effect="mg") 
ruddinweap = weapon("Carreaux","aaa",RANGE_DIST,AREA_CIRCLE_3,18,70,0,0,0,0,0,0,0,0,repetition=3,emoji='<:chaos:892857755143127090>')
ruddinweap2 = weapon("Carreaux","aaa",RANGE_MELEE,AREA_CIRCLE_3,25,70,0,0,0,0,0,0,0,0,repetition=3,emoji='<:chaos:892857755143127090>')
malusWeaponEff = effect("Embrouillement","aaa",INTELLIGENCE,strength=-5,magie=-5,critical=-2,type=TYPE_MALUS)
malusWeapon = weapon("Magie sombre","aaa",RANGE_DIST,AREA_CIRCLE_5,20,50,0,effectOnUse=malusWeaponEff,use=MAGIE)
malusSkill1Eff = effect("Malussé","mal",INTELLIGENCE,-15,magie=-15,resistance=-5)
malusSkill1 = skill("Abrutissement","aaa",TYPE_MALUS,0,area=AREA_CIRCLE_2,effect=malusSkill1Eff,cooldown=5,initCooldown=2)
malusSkill2 = skill("Eclair","aaa",TYPE_DAMAGE,0,50,cooldown=2,sussess=65,use=MAGIE)
kralamWeap = weapon("Décharge motivante","aaa",RANGE_DIST,AREA_DONUT_4,35,100,0,type=TYPE_HEAL,target=ALLIES,use=CHARISMA)
kralamSkillEff2 = effect("This is, my No No Square","nono",INTELLIGENCE,resistance=20,overhealth=100,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR)
kralamSkillEff1 = effect("No no, don't touch me there","squaez",trigger=TRIGGER_DAMAGE,callOnTrigger=kralamSkillEff2,lvl=1)
kralamSkill = skill("Prévention","aaa",TYPE_BOOST,0,0,AREA_DIST_5,cooldown=3,effect=kralamSkillEff1)
temNativTriggered = effect("Promue",'tem',magie=150,turnInit=-1,unclearable=True)
temNativ = effect("College",'tem1',trigger=TRIGGER_ON_REMOVE,turnInit=3,unclearable=True,callOnTrigger=temNativTriggered)
temWeap = weapon("Tem life saves","aaa",RANGE_DIST,AREA_DIST_5,35,65,0,use=MAGIE,effect=temNativ)
temSkill1 = skill("Alergies","aaa",TYPE_DAMAGE,0,50,use=MAGIE,initCooldown=3)
octoMageWeap = weapon("noneWeap","aaa",1,AREA_CIRCLE_1,0,0,0) 

class octarien:
    def __init__(self,name,maxStrength,maxEndurance,maxCharisma,maxAgility,maxPrecision,maxIntelligence,maxMagie,resistance,percing,critical,weapon,exp,icon,skill=["0","0","0","0","0"],aspiration=-1,gender=GENDER_OTHER,description="",url="",deadIcon=None,oneVAll = False):
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
        self.url = url
        self.element = ELEMENT_NEUTRAL
        self.deadIcon = deadIcon
        self.oneVAll = oneVAll

    def allStats(self):
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

class tmpAllie:
    def __init__(self,name,species,color,aspiration,weapon,stuff,gender,skill=[],description="Pas de description",url=None,element=ELEMENT_NEUTRAL,variant = False,deadIcon=None):
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
        self.icon = emoji.icon[species][getColorId(self)]
        self.description=description
        self.url = url
        self.element = element
        self.variant = variant
        self.deadIcon = deadIcon

    def changeLevel(self,level=1):
        self.level = level
        stats = [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence]
        allMax = [maxStrength,maxEndur,maxChar,maxAgi,maxPreci,maxIntel,maxMagie]
        for a in range(0,len(stats)):
            stats[a] = round(allMax[a][self.aspiration]*0.1+allMax[a][self.aspiration]*0.9*self.level/50)
        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence = stats[0],stats[1],stats[2],stats[3],stats[4],stats[5]

    def allStats(self):
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

for a in [0,1]: # Octo shield
    tablAllOcta += [octarien("OctoShield",20,50,20,30,30,10,0,25,0,0,octoShieldWeap,5,'<:OctoShield:881587820530139136>',description="Un octarien qui se cache derrière un gros et lourd bouclier")]

for a in [0,1,2]: # Octo shoot
    tablAllOcta += [octarien("OctoShooter",40,30,30,35,25,20,0,10,0,0,octoBallWeap,3,'<:octoshooter:880151608791539742>',description="Un tireur sans plus ni moins")]

for a in [0,1]: # Octo heal
    tablAllOcta += [octarien("OctoHealer",0,20,50,35,20,35,0,5,0,30,octoHeal,4,"<:octohealer:880151652710092901>",[healAura,cure,firstheal],aspiration=ALTRUISTE,description="Un octarien qui se spcésialise dans ~~passer son tour~~ soigner ses alliés")]

for a in [0,1,2]: # Rudinn
    tablAllOcta += [octarien("Rudinn",120,50,20,50,50,35,35,0,0,15,ruddinweap,6,"<a:rudinn:893246033226760232>",aspiration=TETE_BRULE,deadIcon='<:defeatrudeen:893246353415757824>')]

for a in [0,1]: # Rudinn Ranger
    tablAllOcta += [octarien("Rudinn Ranger",150,100,20,50,60,35,35,-10,0,15,ruddinweap2,8,"<a:rudinnRanger:893248570742956072>",aspiration=POIDS_PLUME,deadIcon='<:defeatrudeen:893246353415757824>')]

for a in [0,1]: # Flyfish
    tablAllOcta += [octarien("Aéro-benne",60,20,25,50,50,50,0,10,0,0,flyfishweap,5,'<:flyfish:884757237522907236>',description="Un Salmioche qui s'est passionné pour l'aviation",deadIcon='<:salmonnt:894551663950573639>')]

for a in [0,1]: # Mallus
    tablAllOcta += [octarien("Mallus",50,30,50,50,45,250,250,10,0,15,malusWeapon,6,'<:mallus:895824636716130308>',skill=[malusSkill1,malusSkill2],aspiration=PREVOYANT)]

for a in [0,1]: # Kralamour
    tablAllOcta += [octarien("Kralamour",10,50,100,30,50,100,100,20,0,0,kralamWeap,5,'<:kralamour:895443866189176842>',[kralamSkill],PREVOYANT)]

for a in [0,1,2]: # Temmie
    tablAllOcta += [octarien("Temmie",50,25,35,65,65,50,50,30,15,15,temWeap,4,'<:temmie:894546348324552724>',[temSkill1],deadIcon='<:temmient:894545999996014663>')]

for a in [0,1,2]: # Octomage
    tablAllOcta += [octarien("Octo Mage",50,20,30,30,30,20,100,20,10,15,octoMageWeap,5,'<:blocked:897631107602841600>',[flame,courant,rock,storm],MAGE)]

# Octo Protecteur
tablAllOcta += [octarien("OctoProtecteur",0,45,50,50,30,70,20,20,0,0,octoDef,5,"<:octoProtect:883303222255706142>",[inkarmor],aspiration=IDOLE,description="Un octarien qui pense que les boucliers sont la meilleure défense")]

# OctoBOUM
tablAllOcta += [octarien("OctoBOUM",30,-30,10,0,0,0,250,-10,0,0,octoBoumWeap,5,'<:octoboom:884810545457418271>',[explosion],description="Un octarien qui a placé tous ses points dans ses envies pirotechniques")]

for a in [0,1,2]:
    tablAllOcta += [octarien("Octaling",50,30,30,30,30,30,50,10,0,0,weapons[random.randint(0,len(weapons)-1)],5,'<:Octaling:866461984018137138>')]

for a in [0,1]:
    tablAllOcta += [octarien("Octarien Volant",30,0,0,50,30,0,0,10,0,0,octoFly,4,'<:octovolant:880151493171363861>')]

# Boss special skills ----------------------------------------------------------------
spamSkill1 = skill("A Call For You","aaa",TYPE_DAMAGE,0,60,area=AREA_CONE_3,sussess=50,emoji='<:call:892757436203671572>',cooldown=3,message="HOT {0} IN YOUR AREA HAVE A [[Message](https://fr.wikipedia.org/wiki/Message)] FOR [{2}] :")
spamSkill2 = skill("BIG SHOT","aaa",TYPE_DAMAGE,0,100,area=AREA_LINE_5,sussess=70,ultimate=True,cooldown=5,message="[[Press F1](https://forums.commentcamarche.net/forum/affich-19023080-press-f1-to-continue-del-to-enter-setup)] FOR HELP :",emoji='<:bigshot:892757453442277417>')

jevilWeap = weapon("CHAOS, CHAOS, CATCH ME IF YOU CAN!","aaa",RANGE_DIST,AREA_CIRCLE_4,60,50,0,area=AREA_CONE_2,message="CHAOS, CHAOS, CATCH ME IF YOU CAN!",emoji='<:chaos:892857755143127090>')
jevilSkill1 = skill("NU-HA!! I NEVER HAD SUCH FUN, FUN!!","aaa",TYPE_DAMAGE,0,50,area=AREA_CONE_3,range=AREA_DIST_5,sussess=60,emoji='<a:card:892855854712385637>',message="NU-HA!! I NEVER HAD SUCH FUN, FUN!!",cooldown=2)
jevilSkill2 = skill("KIDDING! HERE'S MY FINAL CHAOS!","aaa",TYPE_DAMAGE,0,100,AREA_MONO,area=AREA_ALL_ENNEMIES,message="KIDDING! HERE'S MY FINAL CHAOS!",initCooldown=5,cooldown=10)

tablBoss = [
    octarien("Ailill",80,20,0,30,50,50,50,10,10,0,depha,10,'<a:Ailill:882040705814503434>',[balayette],BERSERK,GENDER_FEMALE,description="Une humaine à qui la vie n'a pas vraiment souris. Du coup elle passe ses nerfs sur les autres.\nEnfin les autres plus faibles qu'elle évidamment\n\nSi il y a 5 combattants ou plus dans une équipe, les dégâts infligés à Ailill sont réduits si l'attaquant est trop éloigné"),
    octarien("OctoSniper",50,20,10,0,50,20,0,15,0,0,octoSnipeWeap,7,'<:octotSniper:873118129398624287>',aspiration=OBSERVATEUR,description="Un octarien qui a passé des années à s'entrainer pour rivaliser avec une inkling qui faisait des ravages conséquents parmis les siens"),
    octarien("[[Spamton Neo](https://deltarune.fandom.com/wiki/Spamton)]",250,1250,100,45,45,200,200,30,10,15,bigshot,45,'<a:spamton:892749040205316138>',skill=[spamSkill1,spamSkill2],description="NOW IT'S YOUR CHANCE TO BE A [Big shot] !",deadIcon='<:spamblocked:892750635315912746>',oneVAll=True),
    octarien("Jevil",250,1500,100,60,75,120,120,10,0,15,jevilWeap,50,'<a:CHAOS:762276118224961556>',[chaos,jevilSkill1,jevilSkill2],description="I CAN DO ANYTHING !",deadIcon='<:chaosnt:892857736642064455>',oneVAll=True)
]

# Alliés temporaires
tablAllAllies = [
    tmpAllie("Lena",1,light_blue,OBSERVATEUR,splatcharger,[amethystEarRings,uniform,redSnekers],GENDER_FEMALE,[splatbomb,bleedingArrow,icelance,shot],"Une inkling qui en a vu des vertes et des pas murs.\nPréfère rester loin de la mêlée et abattre ses ennemis à bonne distance","https://cdn.discordapp.com/emojis/866459302319226910.png",ELEMENT_WATER),
    tmpAllie("Gwendoline",2,yellow,TETE_BRULE,roller,[anakiMask,blackJeanJacket,blackFlat],GENDER_FEMALE,[uppercut,balayette,highkick],"Bien qu'elle essaye de l'éviter, cette jeune femme se retrouve toujours à devoir en venir aux mains pour se débarraser des gros lourds de la première ligne ennemie.\nIl est vrai aussi qu'elle n'est pas toute seule dans sa tête","https://cdn.discordapp.com/emojis/866459052132532275.png",ELEMENT_EARTH),
    tmpAllie("Clémence",2,red,MAGE,rapiere,[batEarRings,jeanJacket,mustangBoots],GENDER_FEMALE,[bleedingArrow,poisonus],"Une vampire qui a décidé de léguer sa jeunesse éternelle à l'étude des runes et la magie","https://cdn.discordapp.com/emojis/866459004439756810.png",ELEMENT_FIRE),
    tmpAllie("Alice",1,pink,IDOLE,mic,[batRuban,pinkShirt,pinkSneakers],GENDER_FEMALE,[secondSun,courage,theSkill,healAura,onstage],"Une petite fille vampirique qui veut toujours avoir l'attention sur elle. Faisant preuve d'une grande volontée, il faudrait mieux ne pas trop rester dans le coin si elle décide que vous lui faites de l'ombre","https://cdn.discordapp.com/emojis/866459344173137930.png?",ELEMENT_LIGHT),
    tmpAllie("Shushi",1,blue,TETE_BRULE,inkbrella,[patacasque,pataarmor,patabottes],GENDER_FEMALE,[coffeeSkill,inkarmor,balayette,protect,burst],"Jeune inkling pas très douée pour le combat, à la place elle essaye de gagner du temps pour permettre à ses alliés d'éliminer l'équipe adverse","https://cdn.discordapp.com/emojis/866459319049650206.png",ELEMENT_AIR),
    tmpAllie("Lohica",1,purple,PREVOYANT,butterflyP,[oldBooks,uniform,schoolShoes],GENDER_FEMALE,[contrecoup,bpotion,explosion,poisonus,boom],"Une fée à l'histoire bien mouvementée. Spécialisée dans les poisons","https://cdn.discordapp.com/emojis/866459331254550558.png?v=1",ELEMENT_DARKNESS),
    tmpAllie("Hélène",2,white,ALTRUISTE,serringue,[barrette,heleneDress,heleneShoe],GENDER_FEMALE,[cure,lapSkill,trans],"Une fée qui estime qu'essayer de sauver la vie de ses alliés est plus efficace que si elle esseyait de terminer le combat elle-même","https://cdn.discordapp.com/emojis/871149576965455933.png?v=1",ELEMENT_LIGHT),
    tmpAllie("Félicité",1,red,TETE_BRULE,dtsword,[determination,legendaryTunic,legendaryBoots],GENDER_FEMALE,[balayette,splashdown,splatbomb,monoMissiles,highkick],"Une grande pré-ado qui veut toujours tout faire, mais qui n'y arrive pas tout à fait non plus","https://cdn.discordapp.com/emojis/866459224664702977.png?v=1"),
    tmpAllie("Akira",2,black,TETE_BRULE,fauc,[anakiMask,blackJeanJacket,blackSnelers],GENDER_MALE,[balayette,burst,splashdown,bleedingDague],"Flora si tu as une description je veux bien","https://cdn.discordapp.com/emojis/871151069193969714.png?v=1",ELEMENT_DARKNESS)
]

tablVarAllies = [
    tmpAllie("Lina",1,black,POIDS_PLUME,kcharger,[darkMaidPendants,darkMaidDress,darkMaidFlats],GENDER_FEMALE,[splatbomb,balayette,soupledown,highkick],"Là où se trouve la Lumière se trouvent les Ténèbres","https://cdn.discordapp.com/emojis/871149560284741632.png?v=1",ELEMENT_DARKNESS,variant=True),
    tmpAllie("Altikia",2,yellow,ALTRUISTE,inkbrella,[maidHat,maidDress,maidHeels],GENDER_FEMALE,[healAura,inkarmor,isolement],"Une personnalité de Gwen qui préfère se concentrer sur ses alliés","https://cdn.discordapp.com/emojis/866459052132532275.png",ELEMENT_LIGHT,variant=True),
    tmpAllie("Klironovia",2,yellow,BERSERK,roller,[ironHelmet,FIACNf,blackFlat],GENDER_FEMALE,[courage,balayette,splashdown,bleedingDague,percingLance],"Une personnalité de Gwen bien plus violente que les deux autres","https://cdn.discordapp.com/emojis/866459052132532275.png",ELEMENT_AIR,variant=True),
    tmpAllie("Shihu",1,black,MAGE,spellBook,[amethystEarRings,shihuDress,shihuShoe],GENDER_FEMALE,[splatbomb,stalactic,percingArrow,bleedingArrow],"\"Eye veut zuste un pi d'attenchions...\" - Shushi","https://cdn.discordapp.com/emojis/871149560284741632.png?v=1",ELEMENT_DARKNESS,variant=True)
]

print("Mise à jour de la base de donnée...")
addAllInWeaponData()
addAllInSkillData()
addAllInStuffData()
print("Mise à jour de la base de donnée réalisée")

print("\nVérification de l'équilibrage des stuffs...")
allstats = [0,0,0,0,0,0,0,0,0,0]
for a in stuffs+weapons:
    ballerine = a.allStats()+[a.resistance,a.percing,a.critical]
    sumation = 0
    for b in range(0,len(ballerine)):
        sumation += ballerine[b]
        allstats[b] += ballerine[b]

    if sumation != 20 and a.effect == None and a.name != "Claquettes chaussettes":
        print("{0} n'a pas le bon cumul de stats : {1}".format(a.name,sumation))

    elif sumation != 10 and a.effect != None:
        print("{0} n'a pas le bon cumul de stats : {1}".format(a.name,sumation))

temp = "\nDistribution des statistiques :\n"
total = 0
for a in allstats:
    total += a

for a in range(0,len(allNameStats)):
    temp += "{0} : {1}% ({2})\n".format(allNameStats[a],round(allstats[a]/total*100,2),allstats[a])

print(temp)
print("Vérification de l'équilibrage des stuffs terminée")

def findWeapon(WeaponId):
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

def findSkill(skillId):
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

        print(skillId)
        return None

def findStuff(stuffId):
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

def findEffect(effectId):
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

def findOther(otherId):
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

def findInvoc(name):
    for a in invocTabl:
        if a.name == name:
            return a

    return None

def findAllie(name):
    for a in tablAllAllies+tablVarAllies:
        if a.name == name:
            return a
    return None

def findEnnemi(name):
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