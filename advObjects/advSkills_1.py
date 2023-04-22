from copy import deepcopy
from classes import *
from constantes import *
from advObjects.advDepl import *

EXCLUSIVE = 0
WEAPON, ASPIRATION, ELEMENT = 0,1,2

soupledown = skill("Choc Ténébreux","zz",TYPE_DAMAGE,500,150,range = AREA_INLINE_3,condition=[EXCLUSIVE,ASPIRATION,POIDS_PLUME],area = AREA_CIRCLE_2,accuracy=150,tpCac=True,ultimate=True,cooldown=5,emoji='<:lunadown:932444767504203847>',use=STRENGTH)
armor = effect("Armure d'Encre","la",INTELLIGENCE,overhealth=70,emoji=sameSpeciesEmoji('<:armor1:866828463751036929>','<:armor2:866828487038205962>'),description="Une armure qui protège le porteur des dégâts directs",trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR)
inkarmor = skill("Armure d'Encre","zy",TYPE_ARMOR,250,ultimate=True,effects=armor,emoji = '<:inkArmor:866829950463246346>',area=AREA_CIRCLE_2,cooldown=5,range=AREA_CIRCLE_5)
coffee = effect("Caféiné","lb",CHARISMA,strength=10,endurance=10,description="Boost la force et l'endurance de tous les alliés",emoji=uniqueEmoji("<:coffee:867538582846963753>"))
coffeeSkill = skill("SupréCafé","zx",TYPE_BOOST,500,effects=coffee,use=CHARISMA,area=AREA_ALL_ALLIES,emoji='<:coffee:867538582846963753>',cooldown=5,message="{0} prend le café avec ses alliés :")
theSkill = skill("LiberThé","zw",TYPE_BOOST,500,effects=["lc"],use=CHARISMA,area=AREA_ALL_ALLIES,emoji='<:the:867538602644602931>',cooldown=5,message="{0} prend le thé avec ses alliés :")
gpotion = skill("Potion tonifiante","zv",TYPE_BOOST,250,emoji="<:bpotion:867165268911849522>",use=INTELLIGENCE,cooldown=3,effects="le",area=AREA_MONO,range=AREA_CIRCLE_3)
bpotion = skill("Potion étrange","zu",TYPE_MALUS,200,cooldown=3,effects="lf",emoji="<:dpotion:867165281617182760>",use=INTELLIGENCE,area=AREA_CIRCLE_1,message="{0} lance une {1} sur {2}")
zelian = skill("Chronoshift","zt",TYPE_INDIRECT_HEAL,500,cooldown=7,effects="lj",emoji='<:chronoshift:867872479719456799>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME])
courage = skill("Motivation","zs",TYPE_BOOST,500,emoji ='<:charge:866832551112081419>',area=AREA_CIRCLE_2,use=CHARISMA,effects="lk",cooldown=5,range=AREA_MONO)
nostalgia = skill("Nostalgie","zr",TYPE_MALUS,500,emoji='<:nostalgia:867162802783649802>',effects="lm",cooldown=5,use=INTELLIGENCE)
draw25 = skill("Stop attacking or draw 25","zq",TYPE_MALUS,300,25,emoji="<:draw25:869982277701103616>",use=INTELLIGENCE,effects="lq",cooldown = 3,area=AREA_ALL_ENEMIES,range=AREA_MONO,message="{0} utilise sa carte joker !")
siropMenthe = skill("Menthalité","zp",TYPE_BOOST,500,effects=["lu"],use=CHARISMA,area=AREA_ALL_ALLIES,emoji='<:menthe:867538622797054042>',cooldown=5,message="{0} prend un sirop de menthe avec ses alliés :")
unHolly = skill("Truc pas catho","zo",TYPE_MALUS,69,emoji='<:bravotakei:877202258348113960>',cooldown=2,effects="lw",use=CHARISMA,message="{0} ||fait des trucs pas catho à destination de|| {2} :",group=SKILL_GROUP_DEMON)
chaos = skill("Chaos Chaos !","zn",TYPE_BOOST,1000,range=AREA_MONO,area=AREA_ALL_ENTITES,emoji='<a:CHAOS:762276118224961556>',cooldown=7,use=None,description="Pour chaque combattant en vie, augmente ou diminue de manière aléatoire les dégâts infligés\nLes bonus ou malus de dégâts ont une puissance aléatoire entre 5% et 20% et leur durée est tout aussi aléatoire, de 1 tour à 3")
contrecoup = skill("Contre-coup","zm",TYPE_INDIRECT_DAMAGE,250,effects="ln",cooldown=2,emoji='<:aftershock:882889694269038592>',use=MAGIE)
boom = skill("Réaction en chaîne","zl",TYPE_INDIRECT_DAMAGE,250,effects="lv",cooldown=3,emoji='<:bimbamboum:873698494874017812>',use=MAGIE)
balayette = skill("Baleyette","zk",TYPE_DAMAGE,100,100,range=AREA_MONO,area=AREA_CIRCLE_1,emoji='<:baleyette:977166497422139392>',cooldown=3,setAoEDamage=True)
cure = skill("Guérison","zi",TYPE_HEAL,250,80,cooldown=5,emoji='<:cure:925190515845132341>')
lightAura = skill("Aura de Lumière","zh",TYPE_PASSIVE,250,effectOnSelf="ly",emoji="<:AdL:873548073769533470>",quickDesc="Soigne les alliés autour de vous en fin de tour",condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
splatbomb = skill("Bombe splash","zg",TYPE_DAMAGE,100,cooldown=5,area=AREA_CIRCLE_1,power=90,emoji='<:splatbomb:873527088286687272>',message="{0} lance une {1} sur {2} :")
explosionSilentEff = copy.deepcopy(silenceEff)
explosionSilentEff.turnInit = 4
explosion = skill("Explosion","KBOOM",TYPE_DAMAGE,1000,power=350,percing=0,ultimate=True,cooldown=12,area=AREA_CIRCLE_2,shareCooldown=True,effectOnSelf=explosionSilentEff,use=MAGIE,emoji='<a:explosion:882627170944573471>',damageOnArmor=0.8,url='https://media.discordapp.net/attachments/933783831272628356/934066959040016404/20220121_134758.gif',description="Inflige des dégâts colosaux dans une grande zone")
castExplo = effect("Cast - Explosion","na",turnInit=2,silent=True,emoji=sameSpeciesEmoji('<a:boomCastB:916382499704275005>','<a:boomCastR:916382515135144008>'),replique=explosion)
explosionCast = skill("Explosion","zf",TYPE_DAMAGE,1000,0,ultimate=True,cooldown=7,area=AREA_CIRCLE_2,accuracy=0,shareCooldown=True,effectOnSelf=castExplo,use=MAGIE,emoji='<a:explosion:882627170944573471>',message="{0} rassemble son mana...")
protect = skill("Orbe défensif","ze",TYPE_ARMOR,200,emoji='<:orbeDef:873725544427053076>',effects="md",cooldown=3)
poisonus = skill("Vent empoisonné","zd",TYPE_INDIRECT_DAMAGE,500,emoji='<:estabistia:883123793730609172>',effects="me",cooldown=5,area=AREA_CIRCLE_1,use=MAGIE,message="{0} propage un {1} autour de {2} :")
invocBat = skill("Invocation - Chauve-souris","zc",TYPE_SUMMON,500,invocation="Chauve-Souris",emoji="<:cutybat:884899538685530163>",shareCooldown=True,use=HARMONIE,nbSummon=3,cooldown=3)
multiMissiles = skill("Multi-Missiles","zb",TYPE_INDIRECT_DAMAGE,750,range=AREA_MONO,ultimate=True,emoji='<:tentamissile:884757344397951026>',effects="mf",cooldown=5,area=AREA_RANDOMENNEMI_5,url='https://cdn.discordapp.com/attachments/935769576808013837/935781565663948850/20220126_071157.gif')
monoMissiles = skill("Mono-Missiles","za",TYPE_INDIRECT_DAMAGE,250,range=AREA_CIRCLE_7,emoji='<:monomissile:884757360193708052>',effects="mf",cooldown=5)
classicSplashdown = skill("Choc Chromatique Classique","yz",TYPE_DAMAGE,500,150,AREA_MONO,ultimate=True,emoji='<:splashdown:884803808402735164>',cooldown=5,area=AREA_CIRCLE_2,damageOnArmor=3,url="https://cdn.discordapp.com/attachments/935769576808013837/935781564661526578/20220126_071756.gif")
invocCarbE = skill("Invocation - Carbuncle Emeraude","yy",TYPE_SUMMON,500,invocation="Carbuncle Emeraude",emoji="<:invoncEm:919857931158171659>",cooldown=3,range=AREA_CIRCLE_3,shareCooldown=True,use=MAGIE)
invocCarbT = skill("Invocation - Carbuncle Topaze","yx",TYPE_SUMMON,500,invocation="Carbuncle Topaze",emoji="<:invocTopaz:919859538943946793>",cooldown=3,range=AREA_CIRCLE_3,shareCooldown=True,use=ENDURANCE)
invocFee = skill("Invocation - Fée Soignante","yw",TYPE_SUMMON,500,0,AREA_CIRCLE_3,cooldown=5,invocation="Fée Soignante",emoji="<:selene:885077160862318602>",shareCooldown=True,use=CHARISMA)
thinkSkill = skill("Réfléchis !","yv",TYPE_BOOST,250,0,emoji="<:think:885240853696765963>",effects="mh",use=CHARISMA,cooldown = 3)
descart = skill("Nous pensons donc nous somme","yu",TYPE_BOOST,250,range=AREA_MONO,area=AREA_CIRCLE_2,emoji="<:descartes:885240392860188672>",effects='mi',cooldown=5,message="{0} a trouvé le sens de la vie !")
trans = skill("Transcendance","lb",TYPE_UNIQUE,0,initCooldown=3,setAoEDamage=True,cooldown=5,emoji="<:limiteBreak:886657642553032824>",description="Un sort particulier qui a un effet différent en fonction de l'aspiration du lanceur\n\nUtiliser Transcendance vous empêche d'utiliser une compétence ultime lors du prochain tour",use=HARMONIE,shareCooldown=True,accuracy=200)
transBerserk = copy.deepcopy(trans)
transBerserk.type,transBerserk.power, transBerserk.name = TYPE_DAMAGE, 600, transBerserk.name + " - Frappe transcendique"
transPoidsPlume = copy.deepcopy(transBerserk)
transPoidsPlume.knockback = 5
transTetBrule = copy.deepcopy(transBerserk)
transTetBrule.erosion = 65
transBerserk.lifeSteal = 65
transObs = copy.deepcopy(trans)

transObs.type,transObs.power,transObs.area, transObs.name, transObs.effBeforePow = TYPE_DAMAGE,500,AREA_LINE_6, transObs.name + " - Tir transcendique", True
transAttentif = copy.deepcopy(transObs)
transObs.effectOnSelf = effect("Transcender ses limites","transObsEff",HARMONIE,precision=25,strength=25,turnInit=3,emoji=sameSpeciesEmoji('<:lbBB:930780339947855882>','<:lbBR:930780304405327893>'),description="Augmente les statistiques de l'Observateur pendant 3 tours")
transAttentif.effects= [effect("Poison transcendique","transTetEff",HARMONIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,lvl=3,power=45,turnInit=3,emoji=sameSpeciesEmoji('<:lbDB:930780352480436244>','<:lbDR:930780318699511850>'),description="Inflige des dégâts pendant 3 tours")]
transMage = copy.deepcopy(trans)
transMage.type,transMage.power,transMage.area,transMage.name, transMage.cooldown = TYPE_DAMAGE,400,AREA_CIRCLE_2, transMage.name + " - Explosion transcendique", transMage.cooldown+1
transEnch = copy.deepcopy(transMage)
transSorceler = copy.deepcopy(transMage)
transMage.power, transSorceler.effects= int(transMage.power * 1.2), [effect("Hypernova","transSorcEff",HARMONIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,area=AREA_CIRCLE_2,power=35,turnInit=3,lvl=3,emoji=sameSpeciesEmoji('<:lbDB:930780352480436244>','<:lbDR:930780318699511850>'),description="Inflige des dégâts indirects supplémentaire autour de la cible initiale au début de son tour")]
transEnch.effectOnSelf = effect("Bouclier Transcendique","transEchShield",MAGIE,emoji=sameSpeciesEmoji("<a:transArmorB:900037831257358378>","<a:transArmorR:900037817449717800>"),type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,overhealth=100,description="Accorde une armure à l'Enchanteur")
transAlt = copy.deepcopy(trans)
transAlt.type,transAlt.power,transAlt.area,transAlt.range, transAlt.name, transAlt.cooldown, transAlt.effectAroundCaster = TYPE_HEAL,250,AREA_ALL_ALLIES,AREA_MONO, transAlt.name + " - Soins transcendiques",7, [TYPE_RESURECTION,AREA_CIRCLE_6,350]
transIdo = copy.deepcopy(trans)
transAlt.effects= [effect("Soins transcendique","transAltEff",CHARISMA,power=25,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji=sameSpeciesEmoji('<:lbHealB:933084435706953768>','<:lbHealR:933084448327606304>'),description="Soigne légèrement les alliés affectés au début de leur tour")]
transIdo.effects, transIdo.type, transIdo.effectAroundCaster, transIdo.range, transIdo.area, transIdo.name = [effect("Transcender ses limites","transIdoEff",HARMONIE,strength=30,magie=30,charisma=25,intelligence=25,percing=10,critical=5,turnInit=3,emoji=sameSpeciesEmoji('<:lbBB:930780339947855882>','<:lbBR:930780304405327893>'),description="Augmente les statistiques des alliés affectés pendant 3 tours")], TYPE_BOOST, [TYPE_RESURECTION,AREA_CIRCLE_6,150], AREA_MONO, AREA_CIRCLE_6, "Apothéose"
transInoEff = copy.deepcopy(defenseUp)
transInoEff.turnInit, transInoEff.power = 3, 20
transIno = copy.deepcopy(transIdo)
transIno.effects, transIno.effectAroundCaster, transIno.name = transIno.effects + [transInoEff], None, "Ultima Serum"
transPre = copy.deepcopy(trans)
transPro = copy.deepcopy(trans)
transAttEffOnSelf = copy.deepcopy(defenseUp)
transAttEffOnSelf.turnInit, transAttEffOnSelf.power = 3, 15
effTransPre = effect("Armure Transcendique","transArm",HARMONIE,strength=5,magie=5,inkResistance=15,overhealth=250,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji("<a:transArmorB:900037831257358378>","<a:transArmorR:900037817449717800>"),description="Donne une grosse armure et augmente les statistiques des alliés tant que celle-ci est active")
effTransPro = effect("Armure Transcendique","transArm",HARMONIE,resistance=5,overhealth=250,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji("<a:transArmorB:900037831257358378>","<a:transArmorR:900037817449717800>"),description="Donne une grosse armure et augmente la résistance des alliés tant que celle-ci est active")
transPre.type,transPre.area,transPre.range,transPre.effects,transPre.name, transPre.cooldown = TYPE_ARMOR,AREA_ALL_ALLIES,AREA_MONO,[effTransPre],transPre.name + " - Armure Transcendique",7
transPro.type,transPro.area,transPro.range,transPro.effects,transPro.name, transPro.cooldown,transPro.effectOnSelf = TYPE_ARMOR,AREA_ALL_ALLIES,AREA_MONO,[effTransPro],transPro.name + " - Armure Transcendique",7, transAttEffOnSelf
transAtt = copy.deepcopy(transAlt)
transAtt.effectAroundCaster, transAtt.effects, transAtt.name, transAtt.effectOnSelf = [TYPE_RESURECTION,AREA_ALL_ALLIES,int(transAtt.effectAroundCaster[2]*1.5)], [None], "Eclat de vie", transAttEffOnSelf
transMascEff = copy.deepcopy(vulne)
transMascEff.power = 30
transMasc = copy.deepcopy(transIdo)
transMasc.effectAroundCaster = [TYPE_MALUS,transMasc.area,transMascEff]

burst = skill("Bombe ballon","ys",TYPE_DAMAGE,0,75,area=AREA_CIRCLE_1,accuracy=70,emoji='<:burstBomb:887328853683474444>',use=HARMONIE,cooldown=3,setAoEDamage=True)
lapSkill = skill("Invocation - Lapino","yr",TYPE_SUMMON,0,invocation="Lapino",cooldown=5,shareCooldown=True,emoji='<:lapino:885899196836757527>',use=CHARISMA)
adrenaline = skill("Adrénaline","yq",TYPE_HEAL,250,cure.power,cooldown=5,emoji='<:adrenaline:887403480933863475>',use=INTELLIGENCE)
blindOnSelf = effect("Blindé","blindOnSelf",resistance=20,block=20,description="Réduit les degâts subis jusqu'à votre prochain tour")
blindage = skill("Blindage","yp",TYPE_BOOST,350,0,AREA_MONO,area=AREA_DONUT_2,effects="mj",cooldown=3,use=None,emoji="<:blindage:897635682367971338>",effectOnSelf=blindOnSelf)
secondWind = skill("Second Souffle","yo",TYPE_HEAL,350,350,AREA_MONO,emoji='<:secondWind:897634132639756310>',cooldown=99,use=ENDURANCE)
isolement = skill("Isolement","yn",TYPE_ARMOR,500,0,AREA_MONO,emoji='<:selfProtect:887743151027126302>',cooldown=5,effects="ml")
bombRobot = skill("Invocation - Bombe Robot","ym",TYPE_SUMMON,500,0,AREA_CIRCLE_3,invocation="Bombe Robot",cooldown=2,shareCooldown=True,emoji='<:autobomb:887747538994745394>',use=STRENGTH)
linx = skill("Œuil de Linx","yl",TYPE_BOOST,500,range=AREA_MONO,area=AREA_CIRCLE_2,emoji='<:noeuil:887743235131322398>',effects="mm",cooldown=5)
stalactic = skill("Stalactite","yk",TYPE_DAMAGE,300,100,emoji='<:stalactit:889089667088142346>',cooldown=3,accuracy=200,range=AREA_DIST_5)
uppercut = skill("Uppercut","yj",TYPE_DAMAGE,200,80,AREA_CIRCLE_1,emoji='<:uppercut:889091033718194196>',cooldown=3,message="{0} donne un {1} à {2} :")
oneforall = skill("Un pour tous","yi",TYPE_BOOST,500,range=AREA_MONO,area=AREA_DONUT_2,cooldown=5,use=CHARISMA,effects="mo",effectOnSelf="mp",description="Une compétence qui permet d'augmenter les résistances de ses alliés au détriment des siennes",condition=[EXCLUSIVE,ASPIRATION,ALTRUISTE],emoji='<:oneforall:893295824761663488>')
secondSun = skill("Le second Soleil","yh",TYPE_MALUS,350,0,AREA_MONO,area=AREA_ALL_ENEMIES,cooldown=5,effects="mq",emoji='<:iwanttosleeppls:893241882484817920>',use=CHARISMA,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
kiss = skill("Doux baiser","yg",TYPE_HEAL,69,75,AREA_DONUT_2,emoji='<:welp:893251469439008809>',message="{0} fait un gros bisou à {2} :",tpCac=True,cooldown=3)
onstageeff = effect("Euphorie","mr",CHARISMA,strength=15,intelligence=12,charisma=12,magie=15,resistance=5,description="C'est le moment de tout donner !",emoji=uniqueEmoji('<:alice:893463608716062760>'))
onstage = skill("En scène ","yf",TYPE_BOOST,750,0,AREA_MONO,[EXCLUSIVE,ASPIRATION,IDOLE],True,effects=onstageeff,emoji='<:alice:893463608716062760>',area=AREA_DONUT_7,use=CHARISMA,cooldown=5,message="{0} éléctrise l'ambience !")
icelance = skill("Lame glacée","ye",TYPE_DAMAGE,500,180,AREA_DIST_6,[EXCLUSIVE,ELEMENT,ELEMENT_WATER],True,emoji='<:emoji_47:893471252537298954>',cooldown=5,message="{0} fait appaître une lame de glace géante sous {2} :",use=MAGIE)
rocklance = skill("Lame rocheuse","yd",TYPE_DAMAGE,500,180,AREA_CIRCLE_3,[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],True,emoji='<:emoji_46:893471231641276496>',cooldown=5,message="{0} fait appaître une lame de roche géante sous {2} :",use=MAGIE)
infinitFire = skill("Brasier","yc",TYPE_DAMAGE,500,165,AREA_DIST_5,[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],True,emoji='<:emoji_44:893471208065101924>',cooldown=5,message="{0} déclanche un brasier autour de {2} :",area=AREA_LINE_3,use=MAGIE)
storm = skill("Ouragan","yb",TYPE_DAMAGE,500,165,AREA_CIRCLE_2,[EXCLUSIVE,ELEMENT,ELEMENT_AIR],True,emoji='<:emoji_44:893471179023732809>',cooldown=5,message="{0} déclanche un ouragan autour de {2} :",area=AREA_CIRCLE_2,use=MAGIE)
innerdarkness = skill("Ténèbres intérieurs","ya",TYPE_INDIRECT_DAMAGE,500,0,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS],ultimate=True,emoji='<:emoji_48:893471268957990982>',cooldown=5,effects="ms",use=MAGIE,group=SKILL_GROUP_DEMON,hpCost=25)
divineLight = skill("Lumière divine",'xz',TYPE_INDIRECT_HEAL,500,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],ultimate=True,emoji='<:emoji_49:893471282815963156>',cooldown=5,effects=["mu","mv"],use=CHARISMA,area=AREA_CIRCLE_1,group=SKILL_GROUP_HOLY,maxHpCost=15)
swordDance = skill("Danse des sabres","xy",TYPE_DAMAGE,350,power=120,use=STRENGTH,emoji='<:sworddance:894544710952173609>',cooldown=3,area=AREA_CIRCLE_2,range=AREA_MONO)
shot = skill("Tir net","xx",TYPE_DAMAGE,350,115,AREA_CIRCLE_6,emoji='<:shot:894544804321558608>',cooldown=5,use=STRENGTH,damageOnArmor=2)
percingLance = skill("Lance Perçante","xw",TYPE_DAMAGE,350,power=80,emoji='<:percing:894544752668708884>',cooldown=3,area=AREA_LINE_2,range=AREA_CIRCLE_2)
percingArrow = skill("Flèche Perçante","wv",TYPE_DAMAGE,350,power=70,emoji='<:percingarrow:887745340915191829>',cooldown=3,area=AREA_LINE_2,range=AREA_DIST_5)
highkick = skill("HighKick","wu",TYPE_DAMAGE,350,power=120,range=AREA_CIRCLE_1,emoji='<:highkick:894544734759030825>',cooldown=5,damageOnArmor=1.35)
multishot = skill("Tir Multiple","wt",TYPE_DAMAGE,350,power=75,range=AREA_DIST_4,emoji='<:name:894544834780622868>',cooldown=3,area=AREA_CONE_2)
bleedingArrow = skill("Flèche Hémorragique","ws",TYPE_DAMAGE,350,60,AREA_DIST_5,effects='mx',emoji='<:bleedingarrow:894544820071178292>',cooldown=3)
bleedingDague = skill("Dague Hémorragique","wr",TYPE_DAMAGE,350,60,AREA_CIRCLE_2,effects='mx',emoji='<:bleedingdague:894552391444234242>',cooldown=3)
affaiblissement = skill("Affaiblissement","wq",TYPE_MALUS,350,effects="my",cooldown=3,use=INTELLIGENCE,emoji='<:affaib:963394012771942440>',area=AREA_CIRCLE_1)
provo = skill("Provocation","wp",TYPE_MALUS,350,emoji='<:supportnt:894544669793476688>',effects='mz',cooldown=3,use=INTELLIGENCE)
flameche = skill("Flamèche","wo",TYPE_DAMAGE,100,65,area=AREA_CONE_2,cooldown=3,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],emoji='<:flame1:897811975675969556>')
flame = skill("Flamme","wn",TYPE_DAMAGE,250,90,area=AREA_CONE_2,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],cooldown=5,emoji='<:flame2:897812264185376798>')
pyro = skill("Pyrotechnie","wm",TYPE_DAMAGE,500,115,area=AREA_CONE_2,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],cooldown=7,emoji='<:flame3:897812061139140651>')
ecume = skill("Ecume","wl",TYPE_DAMAGE,100,flameche.power+10,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],cooldown=3,emoji='<:splash1:897844189184811078>')
courant = skill("Courant","wk",TYPE_DAMAGE,250,flame.power+15,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],cooldown=5,emoji='<:splash2:897844205198659594>')
torant = skill("Torrant","wd",TYPE_DAMAGE,500,pyro.power+20,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],cooldown=7,emoji='<:splash3:897844380491202581>')
brise = skill("Brise","wj",TYPE_DAMAGE,100,flameche.power,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],area=AREA_CIRCLE_1,cooldown=3,emoji='<:wind1:897845097775915038>')
storm2 = skill("Tempête","wi",TYPE_DAMAGE,250,flame.power,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],area=AREA_CIRCLE_1,cooldown=5,emoji='<:wind2:897845144299110441>')
tornado = skill("Tornade","wh",TYPE_DAMAGE,500,pyro.power,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],area=AREA_CIRCLE_1,cooldown=7,emoji='<:wind3:897845187940868156>')
stone = skill("Caillou","wg",TYPE_DAMAGE,100,ecume.power,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],cooldown=3,emoji='<:rock1:897846015552532531>')
rock = skill("Rocher","wf",TYPE_DAMAGE,250,courant.power,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],cooldown=5,emoji="<:rock2:897846028512944138>")
mont = skill("Montagne","we",TYPE_DAMAGE,500,torant.power,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],cooldown=7,emoji='<:rock3:897846042576420874>')
stingray2 = skill("Pigmalance","wd",TYPE_DAMAGE,500,115,AREA_CIRCLE_7,ultimate=True,emoji='<:stingray:899243721378390036>',cooldown=5,area=AREA_LINE_6,accuracy=120,description="Inflige des dégâts pendant deux tours.\nPuissance au premier tour : 100",damageOnArmor=0.7,url="https://cdn.discordapp.com/attachments/935769576808013837/935781565936590898/20220126_070809.gif")
pigmaCast = effect("Guide - Pigmalance","nb",turnInit=2,silent=True,emoji=uniqueEmoji('<:castStingray:899243733835456553>'),replique=stingray2)
stingray = skill("Pigmalance","wc",TYPE_DAMAGE,500,135,AREA_CIRCLE_7,ultimate=True,emoji='<:stingray:899243721378390036>',cooldown=5,area=AREA_LINE_6,accuracy=100,effectOnSelf=pigmaCast,damageOnArmor=0.7,url="https://cdn.discordapp.com/attachments/935769576808013837/935781565072547850/20220126_071411.gif")
dark1 = skill("Cécité","wb",TYPE_DAMAGE,100,ecume.power,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS],cooldown=5,emoji='<:dark1:899599162566410280>')
dark2 = skill("Obscurité","wa",TYPE_DAMAGE,250,courant.power,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS],cooldown=5,emoji='<:dark2:899599147399807006>')
dark3 = skill("Pénombre","vz",TYPE_DAMAGE,500,torant.power,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS],cooldown=7,emoji='<:dark3:899598969930399765>')
light1 = skill("Lueur","vy",TYPE_DAMAGE,100,flameche.power,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],area=AREA_CIRCLE_1,cooldown=3,emoji='<:light1:899598879576690689>')
light2 = skill("Éclat","vx",TYPE_DAMAGE,250,flame.power,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],area=AREA_CIRCLE_1,cooldown=5,emoji='<:light2:899598896613969970>')
light3 = skill("Éblouissement","vw",TYPE_DAMAGE,500,pyro.power,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],area=AREA_CIRCLE_1,cooldown=7,emoji='<:light3:899599232628043787>')
derobade = skill("Dérobade","vv",TYPE_BOOST,350,0,AREA_DONUT_3,cooldown=3,effectOnSelf="nd",effects="nc",emoji='<:derobade:899788297868558337>',use=INTELLIGENCE)
ferocite = skill("Férocité","vu",TYPE_PASSIVE,200,0,emoji='<:ferocite:899790356315512852>',effectOnSelf="ne",quickDesc="Accroi votre Magie et la probabilité d'être pris pour cible",use=ENDURANCE)
ironWillSkill = skill("Volontée de Fer","vt",TYPE_PASSIVE,200,0,emoji='<:ironwill:899793931762565251>',effectOnSelf="nh",quickDesc="Accroi votre Charisme et la probabilité d'être pris pour cible",use=ENDURANCE)
royaleGardeSkill = skill("Garde Royale","vs",TYPE_PASSIVE,200,0,emoji='<:gardeRoyale:899793954315321405>',effectOnSelf="ng",quickDesc="Accroi votre Intelligence et la probabilité d'être pris pour cible",use=ENDURANCE)
defi = skill("Défi","vr",TYPE_PASSIVE,200,0,emoji='<:defi:899793973873360977>',effectOnSelf="nf",quickDesc="Accroi votre Force et la probabilité d'être pris pour cible",use=ENDURANCE)
dissimulation = skill("Dissimulation","vq",TYPE_PASSIVE,0,effectOnSelf="nj",use=None,emoji="<:dissimulation:900083085708771349>",quickDesc="Diminue la probabilité d'être pris pour cible")
bleedingTrap = skill("Lacération","vp",TYPE_INDIRECT_DAMAGE,500,effects="mx",cooldown=5,area=AREA_CIRCLE_1,use=STRENGTH,message="{0} place et déclanche un {1} autour de {2} :",emoji='<:lacerTrap:900076484230774807>',effPowerPurcent=55)
# vn already taken (Prévention)
convertEff = effect("Convertion","nk",power=50,type=TYPE_BOOST,trigger=TRIGGER_AFTER_DAMAGE,stat=INTELLIGENCE,description="Lorsque le porteur de l'effet inflige des dégâts directs, une partie de ces dégâts lui sont rendue en Armure\nL'Intelligence du lanceur de la compétence influ sur le pourcentage de convertion",emoji=uniqueEmoji('<:convertion:900311843938115614>'))
convert = skill("Convertion","vm",TYPE_ARMOR,350,range=AREA_DONUT_5,effects=convertEff,cooldown=3,emoji='<:convertion:900311843938115614>')
vampirismeEff = effect("Vampirisme","no",power=25,type=TYPE_INDIRECT_HEAL,stat=CHARISMA,stackable=True,trigger=TRIGGER_AFTER_DAMAGE,description="Accorde au porteur un certain pourcentage de vol de vie, augmenté par les statistiques de l'entité à l'origine de l'effet",emoji=sameSpeciesEmoji('<:vampireB:900313575913062442>','<:vampireR:900313598130282496>'))
vampirisme = skill("Vampirisme","vl",TYPE_INDIRECT_HEAL,350,range=AREA_DONUT_5,effects=vampirismeEff,cooldown=3,emoji='<:vampire:900312789686571018>',group=SKILL_GROUP_DEMON,hpCost=10,effPowerPurcent=150)
vampirisme2 = skill("Vampirisme étendu","spw",TYPE_INDIRECT_HEAL,500,effects=vampirismeEff,cooldown=5,emoji='<:vampire:900312789686571018>',group=SKILL_GROUP_DEMON,hpCost=20,effPowerPurcent=75,area=AREA_CIRCLE_3,range=AREA_MONO)
heriteEstialba = skill("Héritage - Fée d'Estialba","vk",TYPE_PASSIVE,0,effectOnSelf='np',emoji='<:heriteEstialba:900318953262432306>',use=MAGIE,quickDesc="Inflige un effet de poison supplémentaire en infligeant Poison d'Estialba")
heriteLesath = skill("Héritage - Famille Lesath","vj",TYPE_PASSIVE,0,effectOnSelf='ns',emoji='<:hertiteLesath:900322590168608779>',quickDesc="Inflige un effet de poison supplémentaire en infligeant Hémorragie")
focal = skill("Focalisation","vi",TYPE_INDIRECT_DAMAGE,1000,range=AREA_CIRCLE_3,cooldown=7,effects="me",effPowerPurcent=225,area=AREA_CIRCLE_1,effectOnSelf="me",emoji='<:focal:925204877683085332>',shareCooldown=True,use=MAGIE,description="Octrois un puissant effet __Poison d'Estialba__ aux ennemis dans la zone ciblé, avec un contre-coup",selfEffPurcent=75)
suppr = skill("Suppression","vh",TYPE_DAMAGE,650,115,emoji='<a:sup:925199175681970216>',cooldown=5,use=MAGIE,damageOnArmor=3,accuracy=80)
revitalisation = skill("Mot revitalisant","vg",TYPE_HEAL,300,55,area=AREA_CIRCLE_1,emoji="<:revita:902525429183811655>",cooldown=3)
onde = skill("Onde","vf",TYPE_ARMOR,500,effects="nv",cooldown=3,area=AREA_CIRCLE_1,emoji='<:onde:902526595842072616>')
eting = skill("Marque Eting","ve",TYPE_INDIRECT_HEAL,350,effects="nw",emoji='<:eting:902525771074109462>',description="Donne un effet régénérant cumulable à l'allié ciblé")
renforce = skill("Renforcement","vd",TYPE_BOOST,500,range=AREA_DONUT_5,effects="nx",cooldown=5,description="Une compétence qui augmente la résistance d'un allié. L'effet diminue avec les tours qui passent",use=INTELLIGENCE,emoji='<:renfor:921760752065454142>')
steroide = skill("Stéroïdes","vc",TYPE_BOOST,500,range=AREA_DONUT_5,effects="oa",cooldown=3,area=AREA_CIRCLE_1,use=INTELLIGENCE,emoji='<:steroide:963548366053179392>')
renisurection = skill("Résurrection","vb",TYPE_RESURECTION,500,100,emoji='<:respls:906314646007468062>',cooldown=3,description="Permet de ressuciter un allié",use=CHARISMA)
demolish = skill("Démolition","va",TYPE_DAMAGE,750,180,AREA_CIRCLE_2,ultimate=True,cooldown=7,effects=incur[5],damageOnArmor=1.2,emoji='<:destruc:905051623108280330>',url="https://media.discordapp.net/attachments/1006418796329848954/1007574358551699466/20220812_105440.gif")
contrainteEff2 = copy.deepcopy(armorGetMalus)
contrainteEff2.power = 30
contrainte = skill("Contrainte","uz",TYPE_MALUS,500,range=AREA_CIRCLE_6,effects=[incur[3],contrainteEff2,"oc"],cooldown=3,use=INTELLIGENCE,emoji='<:contrainte:963393945704992829>')
trouble = skill("Trouble","uy",TYPE_MALUS,500,range=AREA_CIRCLE_6,effects=[incur[3],contrainteEff2,"od"],use=CHARISMA,emoji='<:trouble:963394783596933182>',cooldown=3)
infirm = skill("Infirmitée","ux",TYPE_MALUS,500,area=AREA_CIRCLE_5,effects=incur[2],cooldown=3,use=None,emoji='<:infirm:904164428545683457>')
croissance = skill("Croissance","uw",TYPE_BOOST,500,effects="oe",cooldown=5,description="Une compétence dont les bonus se renforce avec les tours qui passent",use=CHARISMA,range=AREA_DONUT_5,emoji='<:crois:921760610985865246>')
destruction = skill("Météore","uu",TYPE_DAMAGE,1000,power=int(explosion.power * 1.45),ultimate=True,percing=0,cooldown=7,shareCooldown=True,effectOnSelf=explosionSilentEff,use=MAGIE,emoji='<:meteor:904164411990749194>',damageOnArmor=explosion.onArmor,url='https://cdn.discordapp.com/attachments/933783831272628356/934069125628690482/20220121_135643.gif')
castDest = effect("Cast - Météore","nnnn",turnInit=2,silent=True,emoji=uniqueEmoji('<a:castMeteor:932827784655536139>'),replique=destruction)
destruction2 = skill("Météore","uv",TYPE_DAMAGE,1000,power=0,ultimate=True,cooldown=7,effectOnSelf=castDest,use=MAGIE,shareCooldown=True,emoji=destruction.emoji,message="Une ombre plane au dessus de {2}...")
infectRej = effect("Guérison récente (Infection)","oi",silent=True,turnInit=5,description="Une guérison récente empêche une nouvelle infection",emoji='<:unepidemic:1016788322246471801>')
infection = effect("Infection","oh",INTELLIGENCE,power=35,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,lvl=2,reject=[infectRej],description="Un effet infligeant des dégâts indirects\n\nL'infection se propage sur les ennemis autour du porteur lorsque l'effet se déclanche avec une puissance réduite de **15%**",emoji=uniqueEmoji("<:infect:904164445268369428>"),turnInit=2)
infectFiole = skill("Fiole d'infection","ut",TYPE_INDIRECT_DAMAGE,350,0,effects=infection,cooldown=5,use=INTELLIGENCE,message="{0} lance une {1} sur {2}",emoji='<:fioleInfect:904164736407597087>')
bigLaser = skill("Lasers chromanergiques - Configuration Ligne","us",TYPE_DAMAGE,0,200,emoji='<:uLaserLine:906027231128715344>',area=AREA_LINE_6,accuracy=95,damageOnArmor=1.33,ultimate=True,cooldown=7,description="Après un tour de chargement, déployez des drones énergétiques qui tirent un puissant rayon coloré en ligne droite")
bigLaserRep = effect("Cast - Las. Chrom. - Conf. Ligne","bigLaserEff",turnInit=2,silent=True,emoji=dangerEm,replique=bigLaser)
bigLaser2 = skill(bigLaser.name,"ur",bigLaser.type,750,0,area=bigLaser.area,emoji=bigLaser.emoji,effectOnSelf=bigLaserRep,ultimate=bigLaser.ultimate,cooldown=bigLaser.cooldown,message="{0} charge ses drones")
bigMonoLaser = skill("Lasers chromanergiques - Configuration Mono","uq",TYPE_DAMAGE,0,220,emoji='<:uLaserMono:906027216989716480>',area=AREA_MONO,accuracy=100,damageOnArmor=1.33,ultimate=True,cooldown=7,description="Après un tour de chargement, déployez des drones énergétiques qui tirent un puissant rayon coloré sur un adversaire depuis le ciel")
bigMonoLaserRep = effect("Cast - Las. Chrom. - Conf. Mono","bigMonoLaserEff",turnInit=2,silent=True,emoji=dangerEm,replique=bigMonoLaser)
bigMonoLaser2 = skill(bigMonoLaser.name,"up",bigMonoLaser.type,750,0,area=bigMonoLaser.area,emoji=bigMonoLaser.emoji,effectOnSelf=bigMonoLaserRep,ultimate=bigMonoLaser.ultimate,cooldown=bigMonoLaser.cooldown,message="Les drones de {0} s'envolent")
invocBat2 = skill("Invocation - Chauve-souris II","uo",TYPE_SUMMON,500,invocation="Chauve-Souris II",emoji="<:cuttybat2:904369379762925608>",shareCooldown=True,use=CHARISMA,cooldown=3)
invocCarbunR = skill("Invocation - Carbuncle Rubis","un",TYPE_SUMMON,500,invocation="Carbuncle Rubis",emoji="<:invocRuby:919857898195128362>",shareCooldown=True,use=MAGIE,cooldown=3)
concen = skill("Concentration","um",TYPE_BOOST,price=350,effects="oj",range=AREA_MONO,area=AREA_DONUT_2,cooldown=3,use=None,emoji='<:concen:921762263814262804>')
memAlice = skill("Ultima Sanguis Rosae","memAlice",TYPE_HEAL,1000,150,AREA_MONO,maxHpCost=25,shareCooldown=True,area=AREA_DONUT_4,cooldown=8,ultimate=True,group=SKILL_GROUP_HOLY,use=CHARISMA,emoji='<a:memAlice2:908424319900745768>',description="Cette compétence soigne les alliés vivants et recussite les alliés morts pour une certaine valeur des soins initiaux, affectée par le niveau de votre personnage",effectAroundCaster=[TYPE_RESURECTION,AREA_CIRCLE_6,150])
memAliceCast = effect("Cast - {0}".format(memAlice.name),"aliceMementoCast",replique=memAlice,turnInit=2,silent=True,emoji=uniqueEmoji('<a:memAliceCast:908413832194588723>'))
memAlice2 = copy.deepcopy(memAlice)
memAlice2.id, memAlice2.power, memAlice2.effectOnSelf, memAlice2.emoji, memAlice2.maxHpCost, memAlice2.effectAroundCaster = "ul",0,memAliceCast,'<a:memAliceCast:908413832194588723>', 0, None
blackHole = skill("Trou noir","uk",TYPE_PASSIVE,ironWillSkill.price,effectOnSelf="ol",use=ENDURANCE,emoji='<:blackHole:906195944406679612>',quickDesc="Accroi la probabilité d'être pris pour cible et diminue les dégâts indirects reçus")
blackHoleEff2 = copy.deepcopy(constEff)
blackHoleEff2.power, blackHoleEff2.aggro, blackHoleEff2.turnInit = 50, 35, 3
blackHoleEff4 = copy.deepcopy(absEff)
blackHoleEff4.power, blackHoleEff4.turnInit = blackHoleEff2.power, blackHoleEff2.turnInit
blackHoleEff3 = effect("Horizon des événements","on",redirection=50,description="Quelqu'un attire les dégâts sur lui",turnInit=3,aggro=-15,emoji='<:blackHole2:906195979332640828>')
blackHole2 = skill("Trou noir Avancé","uj",TYPE_BOOST,0,use=None,effects=blackHoleEff3,effectOnSelf=blackHoleEff2,emoji='<:blackHole2:906195979332640828>',cooldown=7,ultimate=True,description="Redirige **{0}%** des dégâts directs reçus par vos alliés proches vers vous tout en diminuant leur agression, et augmente vos PV Maximums et vos soins reçus de **{1}%**, le tout durant {2} tours".format(blackHoleEff3.redirection,blackHoleEff2.power,blackHoleEff2.turnInit),area=AREA_DONUT_2,range=AREA_MONO,effectAroundCaster=[TYPE_BOOST,AREA_MONO,blackHoleEff4])
fireCircle = skill("Cercle de feu","ui",TYPE_DAMAGE,350,70,AREA_DIST_5,[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],effects='oo',area=AREA_DONUT_1,cooldown=3,use=MAGIE,emoji='<:fireCircle:906219518760747159>',effBeforePow=True)
waterCircle = skill("Cercle d'eau","uh",TYPE_DAMAGE,350,50,AREA_DIST_5,[EXCLUSIVE,ELEMENT,ELEMENT_WATER],effects='op',area=AREA_DONUT_1,cooldown=3,use=MAGIE,emoji='<:waterCircle:906219492135276594>',effBeforePow=True)
airCircle = skill("Cercle d'air","ug",TYPE_DAMAGE,350,70,AREA_CIRCLE_2,[EXCLUSIVE,ELEMENT,ELEMENT_AIR],effects='oq',area=AREA_DONUT_1,cooldown=3,use=MAGIE,emoji='<:airCircle:906219469200842752>',effBeforePow=True)
earthCircle = skill("Cercle de terre","uf",TYPE_DAMAGE,350,50,AREA_DIST_5,[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],effects='or',area=AREA_DONUT_1,cooldown=3,use=MAGIE,emoji='<:earthCircle:906219450129317908>',effBeforePow=True)
fireShot = skill("Tir Feu","ue",TYPE_DAMAGE,350,85,area=AREA_CONE_2,cooldown=3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],range=AREA_DIST_5,emoji='<:fireShot:906219594639876116>')
waterShot = skill("Tir Eau","ud",TYPE_DAMAGE,350,105,cooldown=3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],range=AREA_DIST_5,emoji='<:waterShot:906219607856119868>')
airStrike = skill("Frappe Air","uc",TYPE_DAMAGE,350,85,area=AREA_CONE_2,cooldown=3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],range=AREA_CIRCLE_2,emoji='<:airStrike:906219547873386526>')
earthStrike = skill("Frappe Terre","ub",TYPE_DAMAGE,350,105,cooldown=3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],range=AREA_CIRCLE_2,emoji='<:earthStrike:906219563832709142>')
space1 = skill("Naine Blanche","ua",TYPE_DAMAGE,100,flameche.power,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE],area=AREA_CIRCLE_1,cooldown=3,emoji='<:ast1:907470821679824896>')
space2 = skill("Constelation","tz",TYPE_DAMAGE,250,flame.power,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE],area=AREA_CIRCLE_1,cooldown=5,emoji='<:ast2:907470855402033153>')
space3 = skill("Nébuluse","ty",TYPE_DAMAGE,500,pyro.power,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE],area=AREA_CIRCLE_1,cooldown=7,emoji='<:ast3:907470880676917309>')
time1 = skill("Seconde","tx",TYPE_DAMAGE,100,ecume.power,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],cooldown=3,emoji='<:time1:907474383034023977>')
time2 = skill("Minute","tw",TYPE_DAMAGE,250,courant.power,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],cooldown=5,emoji='<:time2:907474439854235668>')
time3 = skill("Heure","tv",TYPE_DAMAGE,500,torant.power,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],cooldown=7,emoji='<:time3:907474471240216658>')
timeSpEff = effect("Rembobinage","nigHotMF",CHARISMA,power=20,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,turnInit=3,emoji=uniqueEmoji('<:rlb:907687694476378112>'),stackable=True,description='Un effet de soin sur la durée qui se déclanche en début de tour')
timeSp = skill("Rembobinage","tu",TYPE_INDIRECT_HEAL,500,use=CHARISMA,range=AREA_MONO,area=AREA_CIRCLE_5,effects=timeSpEff,condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],cooldown=5,ultimate=True,emoji='<:rlb:907687694476378112>')
spaceSp = skill("Pluie d'étoiles","tt",TYPE_DAMAGE,500,150,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE],cooldown=5,area=AREA_CIRCLE_2,ultimate=True,emoji='<:starFall:907687023140302908>')
idoOH = skill("Apothéose","ts",TYPE_PASSIVE,500,effectOnSelf="idoOHEff",emoji='<:IdoOH:909278546172719184>',condition=[EXCLUSIVE,ASPIRATION,IDOLE],use=None,quickDesc="Permet de convertir une partie des soins exessifs en armure")
proOH = skill("Protection Avancée","tr",TYPE_PASSIVE,500,effectOnSelf="proOHEff",emoji='<:proOH:909278525528350720>',condition=[EXCLUSIVE,ASPIRATION,VIGILANT],use=None,quickDesc="Permet de convertir une partie des soins exessifs en armure")
altOH = skill("Bénédiction","tq",TYPE_PASSIVE,500,effectOnSelf="altOHEff",emoji='<:altOH:909278509145395220>',condition=[EXCLUSIVE,ASPIRATION,ALTRUISTE],use=None,group=SKILL_GROUP_HOLY,quickDesc="Permet de convertir une partie des soins exessifs en armure")
lightAura2 = skill("Aura de Lumière Avancée","tp",TYPE_PASSIVE,500,effectOnSelf="lightaura2Pa",emoji=lightAura.emoji,use=CHARISMA,quickDesc="Permet de soigner les ennemis alentours lorsque vous êtes attaqué",condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
tripleMissilesLaunch = skill("Missiles téléguidés","tripleMissiles",TYPE_DAMAGE,750,150,ultimate=True,repetition=3,damageOnArmor=1.2,percing=0,cooldown=10,emoji='<:missiles:909727253414445057>',condition=[EXCLUSIVE,ASPIRATION,OBSERVATEUR])
tripleMissilesEff2 = effect("Cast - {0}".format(tripleMissilesLaunch.name),"tripleMissilesEff2",turnInit=2,silent=True,emoji=sameSpeciesEmoji("<a:missileSoonB:909727376273965097>","<a:missilesSoonR:909727492510740501>"),replique=tripleMissilesLaunch)
tripleMissilesCast2 = copy.deepcopy(tripleMissilesLaunch)
tripleMissilesCast2.power, tripleMissilesCast2.message, tripleMissilesCast2.effectOnSelf, tripleMissilesCast2.id = 0,"{0} lance ses missiles",tripleMissilesEff2,"tripleMissilesCast"
tripleMissilesEff = effect("Cast - {0}".format(tripleMissilesLaunch.name),"tripleMissilesEff",turnInit=2,silent=True,emoji=uniqueEmoji('<:missilesCast:909727680264560690>'),replique=tripleMissilesCast2)
tripleMissiles = copy.deepcopy(tripleMissilesCast2)
tripleMissiles.effectOnSelf,tripleMissiles.message,tripleMissiles.say,tripleMissiles.id = tripleMissilesEff,"{0} calibre ses missiles","Ok, les missiles sont prêts pour le lancement !","to"
lightHeal2 = skill("Illumination","tn",TYPE_HEAL,350,65,cooldown=3,use=CHARISMA,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],emoji='<:illu:909134286203006997>')
extraEtingSkill = copy.deepcopy(eting)
extraEtingSkill.name, extraEtingSkill.id, extraEtingSkill.effects, extraEtingSkill.condition, extraEtingSkill.emoji = "Marque Eting +","tm",["eting+"],[0,2,ELEMENT_TIME],'<:emeB:909132040392302703>'
willShield = effect("Force de volonté","willShield",STRENGTH,overhealth=100,description="Votre force de volonté vous permet de vous protéger de quelques dégâts",turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji('<:willB:922987683217821727>','<:willR:922987661952708638>'))
strengthOfWill = skill("Force de volonté","feliUltLaunch",TYPE_DAMAGE,0,power=220,cooldown=7,effectOnSelf=willShield,ultimate=True,emoji='<:feliSlash:916208942974132245>',tpCac=True)
strengthOfWillCastEff = effect("Cast - Force de volonté","castFeliEff",turnInit=2,silent=True,emoji=uniqueEmoji('<a:feliSlashCast:932819458186158160>'),replique=strengthOfWill)
strengthOfWillCast = copy.deepcopy(strengthOfWill)
strengthOfWillCast.id, strengthOfWillCast.power, strengthOfWillCast.effectOnSelf,strengthOfWillCast.message, strengthOfWillCast.tpCac = "tl",0,strengthOfWillCastEff,"{0} rassemble toute sa Détermination dans son arme", False

sixtineGoodNight = copy.deepcopy(dmgDown)
sixtineGoodNight.power, sixtineGoodNight.stat, sixtineGoodNight.description = 8, INTELLIGENCE, "Réduit les dégâts infligés par le porteur de l'effet de **8%** affectés par les statistiques\nSi plusieurs effets de réduction de dégâts infligés sont présents sur une même cible, seul l'effet le plus puissant est pris en compte"
sixtineUlt = skill("Douce nuit","tk",TYPE_MALUS,0,range=AREA_MONO,area=AREA_ALL_ENEMIES,use=INTELLIGENCE,effects=sixtineGoodNight,ultimate=True,cooldown=7,emoji='<:night:911735172901273620>')
hinaUlt = skill("Déluge de plume","tj",TYPE_DAMAGE,0,40,accuracy=65,area=AREA_CONE_2,repetition=5,cooldown=7,emoji='<:featherStorm:909932475457884191>')
julieUltEff = effect("Prolongation","JulieUltEff",CHARISMA,power=15,turnInit=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,stackable=True,emoji=uniqueEmoji('<:plg:911734437597835316>'),description="Un effet de soin sur la durée qui se déclanche en début de tour")
julieUlt = skill("Prolongation","ti",TYPE_INDIRECT_HEAL,0,area=AREA_CIRCLE_3,range=AREA_MONO,emoji='<:plg:911734437597835316>',effects=julieUltEff,cooldown=5,use=CHARISMA)
invocSeraf = skill("Invocation - Fée protectrice","th",TYPE_SUMMON,500,invocation="Fée protectrice",emoji="<:seraphin:911078421361205289>",shareCooldown=True,use=INTELLIGENCE,cooldown=5)
mageUlt = skill("Éminence","tg",TYPE_DAMAGE,1000,emoji='<:emanence:911397114850975795>',power=150,condition=[EXCLUSIVE,ASPIRATION,MAGE],ultimate=True,cooldown=5,area=AREA_DONUT_2,use=MAGIE,description="Une compétence dont la puissance et la zone d'effet dépend de l'élément")
mageUltMono = copy.deepcopy(mageUlt)
mageUltMono.power,mageUltMono.area,mageUltMono.accuracy = 180,AREA_MONO,160
mageUltZone = copy.deepcopy(mageUlt)
mageUltZone.power,mageUltZone.area,mageUltZone.accuracy = 120,AREA_CONE_3,80
soulaEff = effect("Traité de soulagement","soulaArmor",INTELLIGENCE,overhealth=50,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji('<:tsB:911732326818545664>','<:tsR:911732347601317908>'))
soulagement = skill("Traité de soulagement","tf",TYPE_ARMOR,500,0,AREA_MONO,[EXCLUSIVE,ASPIRATION,PREVOYANT],area=AREA_CIRCLE_2,use=INTELLIGENCE,cooldown=5,effects=soulaEff,emoji='<:soul:911732783993483284>')
bloodArmor = effect("Bouclier sanguin","bloodyArmor",STRENGTH,overhealth=50,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
bloodyStrike = skill("Frappe sanguine",'te',TYPE_DAMAGE,500,105,AREA_CIRCLE_2,[EXCLUSIVE,ASPIRATION,BERSERK],lifeSteal=35,cooldown=5,effectOnSelf=bloodArmor,emoji='<:berkSlash:916210295867850782>')
infraMedicaEff = copy.deepcopy(julieUltEff)
infraMedicaEff.emoji, infraMedicaEff.power, infraMedicaEff.id, infraMedicaEff.name = sameSpeciesEmoji('<:imB:911732644193124393>','<:imR:911732657728151572>'), julieUltEff.power, "infraMedicaHeal", "Extra Medica"
infraMedica = skill("Medica","td",TYPE_HEAL,500,50,AREA_MONO,[EXCLUSIVE,ASPIRATION,ALTRUISTE],area=AREA_CIRCLE_2,cooldown=5,emoji='<:medica:911732802947530843>')
flambe = effect("Flambée","flambage",STRENGTH,type=TYPE_INDIRECT_DAMAGE,turnInit=2,power=15,aggro=10,area=AREA_CIRCLE_1,description="Pour chaque attaque physique directe reçu par la cible, la puissance de cet effet augmente de {0} lors de son déclanchement, au début du prochain tour du lanceur",trigger=TRIGGER_ON_REMOVE,emoji=uniqueEmoji('<:flamb:913165325590212659>'))
flambeSkill = skill("Flambage","tc",TYPE_INDIRECT_DAMAGE,500,effects=flambe,cooldown=5,emoji='<:flamb:913165325590212659>')
magAch = effect("Magia atrocitas","magAch",MAGIE,type=TYPE_INDIRECT_DAMAGE,turnInit=2,power=flambe.power,aggro=10,area=AREA_CIRCLE_1,description="Pour chaque attaque spirituelle directe reçu par la cible, la puissance de cet effet augmente de {0} lors de son déclanchement, au début du prochain tour du lanceur",trigger=TRIGGER_ON_REMOVE,emoji=uniqueEmoji('<:magAch:913165311291842571>'))
magAchSkill = skill("Magia atrocitas","tb",TYPE_INDIRECT_DAMAGE,500,effects=magAch,cooldown=5,emoji='<:magAch:913165311291842571>')
idoOS = skill("Clou du spectacle","ta",TYPE_PASSIVE,500,effectOnSelf="idoOSEff",emoji='<:osIdo:913885207751446544>',condition=[EXCLUSIVE,ASPIRATION,INOVATEUR],use=None,quickDesc="Permet à vos armures d'absorber plus de dégâts lorsqu'elles sont détruites")
proOS = skill("Extra Protection","sz",TYPE_PASSIVE,500,effectOnSelf="proOSEff",emoji='<:osPro:913885191800512562>',condition=[EXCLUSIVE,ASPIRATION,PROTECTEUR],use=None,quickDesc="Permet à vos armures d'absorber plus de dégâts lorsqu'elles sont détruites")
preOS = skill("Armures Avancées","sy",TYPE_PASSIVE,500,effectOnSelf="preOSEff",emoji='<:osPre:913885175161712710>',condition=[EXCLUSIVE,ASPIRATION,PREVOYANT],use=None,quickDesc="Permet à vos armures d'absorber plus de dégâts lorsqu'elles sont détruites")
geoConBoost = effect("Géo-Controlé","geocontroled",INTELLIGENCE,25,20,20,10,10,20,25,5,5,0,description="Une grande force vous envahis",emoji=sameSpeciesEmoji("<:geoContB:918422778414256158>","<:geoContR:918422792649723914>"))
geoConLaunch = skill("Géo-Controle","sx",TYPE_BOOST,1000,range=AREA_MONO,area=AREA_CIRCLE_3,effects=geoConBoost,cooldown=7,use=INTELLIGENCE,ultimate=True,emoji='<:geoCont:918422710781083668>')
geoConCastEff = effect("Cast - {0}".format(geoConLaunch.name),"geoControleCastEff",turnInit=2,silent=True,emoji=dangerEm,replique=geoConLaunch)
geoConCast = copy.deepcopy(geoConLaunch)
geoConCast.id, geoConCast.effects, geoConCast.effectOnSelf, geoConCast.message = "sx",[None],geoConCastEff,"{0} rassemble l'énergie cosmique autour de lui..."
kikuRes = skill("Mors vita est","sw",TYPE_RESURECTION,750,120,AREA_MONO,area=AREA_DONUT_5,emoji='<:mortVitaEst:916279706351968296>',initCooldown=3,shareCooldown=True,description="Réanime les alliés vaincus dans la zone d'effet",use=CHARISMA,group=SKILL_GROUP_DEMON,hpCost=25)
memClemLauchSkill = skill("Ultima Sanguis Pluviae","memClemSkillLauch",TYPE_DAMAGE,0,300,AREA_MONO,percing=0,accuracy=666,area=AREA_CIRCLE_7,ultimate=True,use=MAGIE,cooldown=99,emoji="<:clemMemento:902222089472327760>",description="\n__Effets lors du premier tour de chargement :__\nDéfini vos PVs courants à **1**\nObtenez un bouclier absolu d'une valeur de **50%** des PVs perdus\nDivise votre Résistance Soins de **50%**\nDiminue vos PV maximums de **50%** pour le reste du combat\nDonne l'effet __Incurable (50)__ sur le lanceur pour le reste du combat")
memClemCastSkillEff = effect("Cast - Ultima Sanguis Pluviae","memClemSkillCast",turnInit=2,silent=True,emoji=dangerEm,replique=memClemLauchSkill)
memClemCastSkill = copy.deepcopy(memClemLauchSkill)
memClemCastSkill.id, memClemCastSkill.effectOnSelf, memClemCastSkill.power = "sv",memClemCastSkillEff,0
rosesPhysiEff = effect("Épines","rosesPhysiEff",CHARISMA,endurance=5,resistance=3,power=35,trigger=TRIGGER_AFTER_DAMAGE,lvl=5,description="En plus de légèrement augmenter les statistiques défensives, cet effet inflige des dégâts indirects à chaques fois que le porteur reçois des dégâts **physiques**",onDeclancher=True,emoji=sameSpeciesEmoji("<:epineB:917665759684079626>","<:epineR:917665743649275904>"))
rosesPhysi = skill("Épines","su",TYPE_BOOST,500,effects=rosesPhysiEff,use=CHARISMA,cooldown=3,range=AREA_DONUT_5,emoji='<:epines:917666041243500594>')
rosesMagicEff = effect("Pétales","rosesMagEff",CHARISMA,endurance=5,resistance=3,power=int(rosesPhysiEff.power*1.3),trigger=TRIGGER_AFTER_DAMAGE,lvl=rosesPhysiEff.lvl,description="En plus de légèrement augmenter les statistiques défensives, cet effet inflige des dégâts indirects à chaques fois que le porteur reçois des dégâts **magiques**",onDeclancher=True,emoji=sameSpeciesEmoji("<:rosesAreBlue:917665779770613761>","<:rosesAreRed:917665805557198878>"))
rosesMagic = skill("Pétales","su",TYPE_BOOST,500,effects=rosesMagicEff,use=CHARISMA,cooldown=3,range=AREA_DONUT_5,emoji='<:roses:917666059413233704>')
roses = skill("Roses","su",TYPE_BOOST,500,use=CHARISMA,become=[rosesPhysi,rosesMagic],emoji='<:roses:932612186130493450>')

krysUlt = skill("Réassemblage","st",TYPE_DAMAGE,0,100,cooldown=5,description="En plus d'infliger des dégâts, cette compétence vole **50%** de l'armure normale et légère de la cible (avant d'infliger les dégâts)",emoji='<:reconvert:916121466423091240>')
chaosArmorEff = effect("Armure du Chaos","chaosArmor",INTELLIGENCE,overhealth=1,emoji=sameSpeciesEmoji('<a:caB:938375004792426496>','<a:caR:938375020261023825>'),description="Une armure chaotique dont la puissance de base est aléatoire",type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,turnInit=3)
chaosArmor = skill("Armure du Chaos","ss",TYPE_ARMOR,emoji='<a:chaosArmor:938374846843342869>',area=AREA_CIRCLE_2,price=500,effects=chaosArmorEff,cooldown=5,use=INTELLIGENCE)
firelame = skill("Ignis ferrum","sr",TYPE_DAMAGE,500,45,range=AREA_DIST_5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],cooldown=7,area=AREA_ARC_1,repetition=3,emoji='<:fireLame:916130324197543986>',damageOnArmor=1.1)
airlame = skill("Aer ferrum","sq",TYPE_DAMAGE,500,45,range=AREA_CIRCLE_3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],cooldown=7,area=AREA_ARC_1,repetition=3,emoji='<:airLame:916130609095655454>',damageOnArmor=1.1)
waterlame = skill("Aqua ferrum","sp",TYPE_DAMAGE,500,55,range=AREA_DIST_5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],cooldown=7,repetition=3,emoji='<:aquaLame:916130446125977602>',damageOnArmor=1.1)
mudlame = skill("Lapis ferrum","so",TYPE_DAMAGE,500,55,range=AREA_CIRCLE_3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],cooldown=7,repetition=3,emoji='<:earthLame:916130398914875452>',damageOnArmor=1.1)
shadowLameEff = effect("Umbra ferrum","lameD'ombre",STRENGTH,power=40,stackable=True,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:darkLame:916130473162453033>'))
shadowLame = skill("Umbra ferrum","sn",TYPE_INDIRECT_DAMAGE,500,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS],effects=[shadowLameEff,shadowLameEff,shadowLameEff],cooldown=7,emoji='<:darkLame:916130473162453033>')
lightLameEff = effect("Lux ferrum","lameDeLumière",CHARISMA,resistance=5,power=35,lvl=3,description="En plus de booster légèrement la résistance de la cible, inflige des dégâts indirects lorsque cette dernière est attaquée",trigger=TRIGGER_AFTER_DAMAGE,onDeclancher=True,emoji=uniqueEmoji('<:lightLame:916131830149816340>'))
lightLame = skill("Lux ferrum","sm",TYPE_BOOST,500,effects=lightLameEff,emoji='<:lightLame:916131830149816340>',cooldown=7,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],use=CHARISMA)
astralLameEff = effect("Stella ferrum","lameétoilée",ENDURANCE,resistance=5,power=35,lvl=3,description="En plus de booster légèrement la résistance de la cible, inflige des dégâts indirects lorsque cette dernière est attaquée",trigger=TRIGGER_AFTER_DAMAGE,onDeclancher=True,emoji=uniqueEmoji('<:astralLame:916131872352911400>'),turnInit=2)
astralLame = skill("Stella ferrum","sl",TYPE_BOOST,500,range=AREA_MONO,effects=astralLameEff,emoji='<:astralLame:916131872352911400>',cooldown=7,condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE],use=ENDURANCE)
timeLameEff = effect("Tempus ferrum","lameDuTemps",CHARISMA,resistance=5,power=35,lvl=3,description="En plus de booster légèrement la résistance de la cible, inflige des dégâts indirects lorsque cette dernière est attaquée",trigger=TRIGGER_AFTER_DAMAGE,onDeclancher=True,emoji=uniqueEmoji('<:timeLame:916131853499527208> '))
timeLame = skill("Tempus ferrum","sk",TYPE_BOOST,500,effects=timeLameEff,emoji='<:timeLame:916131853499527208> ',cooldown=7,condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],use=CHARISMA)
magicRuneArmor = effect("Bouclier magicorunique","runeArmor",MAGIE,overhealth=bloodArmor.overhealth,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
magicRuneStrike = skill("Rune magicorunique",'sj',TYPE_DAMAGE,500,125,bloodyStrike.range,[EXCLUSIVE,ASPIRATION,ENCHANTEUR],cooldown=bloodyStrike.cooldown,effectOnSelf=magicRuneArmor,emoji='<:magicoRune:916401319990947920>',use=MAGIE)
infinitDarkEff = effect("Noirceur infinie","bigDarkDark",MAGIE,stackable=True,power=60,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji("<:bigDark:916561798948347935>"))
infinitDark = skill("Noirceur infinie","si",TYPE_INDIRECT_DAMAGE,500,emoji='<:bigDark:916561798948347935>',effects=infinitDarkEff,cooldown=5,ultimate=True,use=MAGIE)
preciseShot = skill("Tir précis","sh",TYPE_DAMAGE,500,120,cooldown=5,use=PRECISION,emoji='<:preciseShot:916561817969500191>')
troublon = skill("Troublon","sg",TYPE_DAMAGE,500,100,cooldown=3,area=AREA_CONE_2,range=AREA_MONO,emoji='<:mousqueton:916561833920462889>')
haimaShield = effect("Haima - Bouclier","haimaShield",INTELLIGENCE,overhealth=20,turnInit=2,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,emoji=sameSpeciesEmoji("<:haimaB:916922889679286282>","<:haimaR:916922905672171570>"))
haimaEffect = effect("Haima","haimaEff",lvl=5,description="En subissant des dégâts sans posséder d'effet \"__Haima - Bouclier__\", le porteur de cet effet gagne le dit effet au prix d'une charge de __Haima__",callOnTrigger=haimaShield,emoji=uniqueEmoji('<:haima:916922498094858251>'),trigger=TRIGGER_AFTER_DAMAGE)
haimaSkill = skill("Haima","sf",TYPE_ARMOR,500,emoji='<:haima:916922498094858251>',effects=haimaEffect,cooldown=7,use=INTELLIGENCE)
physicRune = skill("Rune - Sanguis Pact","se",TYPE_PASSIVE,750,effectOnSelf="pacteDeSang",emoji='<:pacteDeSang:917096147452035102>',quickDesc="Augmente vos dégâts infligés mais pour inflige des dégâts lorsque vous attaquez")
magicRune = skill("Rune - Animae Foedus","sd",TYPE_PASSIVE,750,effectOnSelf="pacteD'âme",emoji='<:pacteDame:917096164942295101>',quickDesc="Augmente vos dégâts infligés mais pour inflige des dégâts lorsque vous attaquez")
lightBigHealArea = skill("Lumière éclatante","sb",TYPE_HEAL,750,90,AREA_MONO,[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],True,area=AREA_CIRCLE_4,cooldown=7,use=CHARISMA,emoji='<:eclatLum:1067824343658283089>')
focus = skill("Focus","sa",TYPE_INDIRECT_DAMAGE,1000,range=AREA_CIRCLE_3,cooldown=7,effects="mx",effPowerPurcent=225,selfEffPurcent=85,effectOnSelf="mx",shareCooldown=True,use=STRENGTH,description="Applique un puissant effet __Hémorragie__ à la cible, avec un contre coup",emoji='<:focus:925204899514417182>')
poisonusPuit = skill("Rayons Féériques Triples","zzz",TYPE_DAMAGE,500,50,area=AREA_CIRCLE_1,use=MAGIE,effects=["me"],repetition=3,cooldown=7,emoji='<a:mpp:925181294906843136>',effPowerPurcent=85,useActionStats=ACT_INDIRECT)
bleedingPuit = skill("Pièges à ressorts","zzy",TYPE_DAMAGE,500,50,area=AREA_CIRCLE_1,effects=["mx"],repetition=3,cooldown=7,emoji='<a:par:925183389252874261>',effPowerPurcent=60,useActionStats=ACT_INDIRECT)
supprZone = skill("Dispersion","zzx",TYPE_DAMAGE,650,100,emoji='<:principio:919529034663223376>',cooldown=5,use=MAGIE,damageOnArmor=3,accuracy=60,area=AREA_CIRCLE_1)
invocCarbSaphir = skill("Invocation - Carbuncle Saphir","zzw",TYPE_SUMMON,500,invocation="Carbuncle Saphir",emoji="<:innvocSafir:919857914490007574>",shareCooldown=True,use=STRENGTH,cooldown=3)
invocCarbObsi = skill("Invocation - Carbuncle Obsidienne","zzv",TYPE_SUMMON,500,invocation="Carbuncle Obsidienne",emoji="<:invocObs:919872508226830336>",shareCooldown=True,use=STRENGTH,cooldown=3)
requiem = skill("Requiem","zzu",TYPE_DAMAGE,500,35,range=AREA_MONO,area=AREA_CIRCLE_7,use=CHARISMA,cooldown=3,repetition=3,emoji='<:requiem:919869677197484052>',group=SKILL_GROUP_DEMON)
cosmicEff = effect("Pouvoir cosmique","cosmicPowerEff",HARMONIE,strength=5,magie=5,resistance=5,emoji=sameSpeciesEmoji('<:comicPowerB:919866210768801833>','<:cosmicPowerR:919866197850353685>'),redirection=15)
cosmicEffSelf = effect("Pouvoir cosmique","cosmicPowerEffOnSelf",resistance=20,emoji=sameSpeciesEmoji('<:comicPowerB:919866210768801833>','<:cosmicPowerR:919866197850353685>'))
cosmicPower = skill("Pouvoir cosmique","zzt",TYPE_BOOST,1000,range=AREA_MONO,area=AREA_DONUT_2,use=HARMONIE,cooldown=7,emoji='<:cosmic:919866054992334848>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE],effects=cosmicEff,effectOnSelf=cosmicEffSelf)
propag = skill("Propagation","zzs",TYPE_INDIRECT_DAMAGE,750,cooldown=7,emoji='<a:propa:925188411617345560>',initCooldown=3,use=MAGIE,effects="me",description="Après la pose des effets de cette compétence, les alliés en mêlée de la cible reçoivent les effets __Poison d'Estialba__ de la cible pour une puissance équivalente à **{power}%** de la puissance de l'effet, pour la durée restante de l'effet de base\nSi vous n'êtes pas à l'origine de l'effet de base, la puissance de l'effet propagé équivaux à **{power2}**% de la puissance de l'effet de base",power=40,effPowerPurcent=100)
inkResEff = effect("Pied au sec","inkRes",INTELLIGENCE,turnInit=2,inkResistance=10,description="Réduit de 10% les dégâts indirects reçu.\nLe pourcentage de réduction est affecté par l'Intelligence et le Bonus aux Armures et Mitigation")
inkResEff2 = copy.deepcopy(inkResEff)
inkResEff2.stat, inkResEff2.name, inkResEff2.emoji = ENDURANCE, "Collectivement inconscient", sameSpeciesEmoji('<:incColB:921546169203687464>','<:incColR:921546151314985020>')
inkRes = skill("Pied au sec","zzr",TYPE_BOOST,500,effects=inkResEff,cooldown=5,area=AREA_CIRCLE_1,use=INTELLIGENCE,emoji='<:inkResR:921486021265354814>')
inkRes2 = skill("Inconscient collectif","zzq",TYPE_BOOST,500,range=AREA_MONO,area=AREA_CIRCLE_2,effects=inkResEff2,cooldown=5,use=ENDURANCE,emoji='<:incCol:921545816940875817>')
booyahBombLauch = skill("Jolizator","zzp",TYPE_DAMAGE,750,180,area=AREA_CIRCLE_2,ultimate=True,cooldown=7,emoji='<:bobomb:921710328771932192>',url="https://cdn.discordapp.com/attachments/935769576808013837/935783888159125544/20220126_072826.gif")
booyahBombEff = effect("Cast - Jolizator","supercalifragilisticexpialiodocieux",turnInit=2,silent=True,emoji=sameSpeciesEmoji("<:booyahB:925796592240455701>","<:booyahR:925796570509766716>"),replique=booyahBombLauch)
booyahBombCast = copy.deepcopy(booyahBombLauch)
booyahBombCast.id, booyahBombCast.effectOnSelf, booyahBombCast.power, booyahBombCast.url = "zzp",booyahBombEff,0,"https://cdn.discordapp.com/attachments/935769576808013837/935783887748079666/20220126_073038.gif"
reconst = skill("Reconstitution","zzo",TYPE_HEAL,750,150,ultimate=True,use=CHARISMA,cooldown=7,emoji='<:mudh:922914512712138802>',description="Une puissante compétence de soins monocibles")
medicamentumEff = effect("Medicamentum","bigmonoindirect",CHARISMA,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,turnInit=3,power=55,description="Un puissant effect soignant",emoji=sameSpeciesEmoji('<:mihB:922914323037306890>','<:mihR:922914344428240937>'))
medicamentum = skill("Rune - Medicamentum",'zzn',TYPE_INDIRECT_HEAL,750,ultimate=True,emoji='<:muih:922914495737757706>',cooldown=7,use=CHARISMA,effects=medicamentumEff)
ultMonoArmorEff = effect("Armis","ultMonoArmor",INTELLIGENCE,overhealth=150,turnInit=3,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,emoji=sameSpeciesEmoji('<:runeArmis:963397040967131176>','<:armis:963397158101471272>'))
ultMonoArmor = skill("Rune - Armis","zzm",TYPE_ARMOR,750,0,ultimate=True,effects=ultMonoArmorEff,cooldown=7,use=INTELLIGENCE,emoji='<:runeArmis:963397040967131176>')
neutralZone1 = skill("Primum multi scopum magicae","zzl",TYPE_DAMAGE,100,flameche.power,area=AREA_CONE_2,use=MAGIE,cooldown=3,emoji='<:nm1:925185303659053088>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_NEUTRAL])
neutralZone2 = skill("Secundum multi scopum magicae","zzk",TYPE_DAMAGE,250,flame.power,area=AREA_CONE_2,use=MAGIE,cooldown=5,emoji='<:nm2:925185316409716746>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_NEUTRAL])
neutralZone3 = skill("Tertio multi scopum magicae","zzj",TYPE_DAMAGE,500,pyro.power,area=AREA_CONE_2,use=MAGIE,cooldown=7,emoji='<:nm3:925185333446971492>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_NEUTRAL])
neutralMono1 = skill("Primum unum scopum magicae","zzi",TYPE_DAMAGE,100,ecume.power,use=MAGIE,cooldown=3,emoji='<:nz1:925184839257317398>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_NEUTRAL])
neutralMono2 = skill("Secundum unum scopum magicae","zzh",TYPE_DAMAGE,250,courant.power,use=MAGIE,cooldown=5,emoji='<:nz2:925184858584662127>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_NEUTRAL])
neutralMono3 = skill("Tertio singula scopum magicae","zzg",TYPE_DAMAGE,500,torant.power,use=MAGIE,cooldown=7,emoji='<:nz3:925184871612157953>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_NEUTRAL])
intelRaise = copy.deepcopy(renisurection)
intelRaise.name, intelRaise.use, intelRaise.id, intelRaise.emoji = "Egeiro", INTELLIGENCE, "zzf", '<:egiero:925768359964979210>'
ultRedirectSelfEff = effect("Teliki Anakatéfthynsi","ultRedirectShield",ENDURANCE,overhealth=200,absolutShield=True,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,description="Vous accorde une grosse armure aboslue\nLes armures absolues protègent même des dégâts indirects et ne sont pas affectés par les multiplicateurs de dégâts sur l'armure")
ultRedirectEff = effect("Teliki Anakatéfthynsi","ultRedirect",redirection=100,trigger=TRIGGER_DAMAGE)
ultRedirect = skill("Teliki Anakatéfthynsi","zze",TYPE_BOOST,1000,range=AREA_MONO,area=AREA_DONUT_3,cooldown=7,ultimate=True,effects=ultRedirectEff,effectOnSelf=ultRedirectSelfEff,use=ENDURANCE,emoji='<:tekeli:963396237606912050>')
clemency = skill('Clémence','zzd',TYPE_HEAL,350,100,cooldown=5,use=ENDURANCE,emoji='<:clemency:926433653037367318>',group=SKILL_GROUP_HOLY,effectAroundCaster=[TYPE_HEAL,AREA_MONO,50])
liuSkillSusEff = effect("Asuama","liuSussessArmor",ENDURANCE,overhealth=75,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,inkResistance=10,turnInit=2,emoji=uniqueEmoji("<:liuArmor:922292960886915103>"))
liuSkillSus = skill("Guraundo Sutoraiku","zzc",TYPE_DAMAGE,0,100,range=AREA_CIRCLE_2,use=ENDURANCE,effectOnSelf=liuSkillSusEff,cooldown=5,emoji='<:liuSkill:922328931502280774>')
liaSkillSus = skill("Kuchu Sutoraiku","zzb",TYPE_DAMAGE,0,40,range=AREA_CIRCLE_1,cooldown=5,knockback=3,repetition=3,use=AGILITY,emoji='<:liaSkill:922291249002709062>')
lioSkillSusEff = effect('Shinju no haha',"lioSussessEff",CHARISMA,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,power=15,turnInit=3,strength=5,magie=5,emoji=uniqueEmoji('<:lioWeap:908859876812415036>'))
lioSkillSus = skill("Shio",'zza',TYPE_INDIRECT_HEAL,0,cooldown=5,effects=lioSkillSusEff,area=AREA_CIRCLE_2,emoji='<:lioSkill:922328964926697505>')
lizSkillSusEff = effect("Tanka",'lizWillBurnThemAll',MAGIE,power=20,area=AREA_CIRCLE_1,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:lizIndirect:917204753610571776>'))
lizSKillSus = skill("Shokyaku","zyz",TYPE_INDIRECT_DAMAGE,0,effects=lizSkillSusEff,area=AREA_CONE_4,cooldown=5,emoji='<:lizSkill:922328829765242961>',use=MAGIE)
friendlyPush = skill("Poussée amicale","movepls",TYPE_HEAL,0,1,range=AREA_DONUT_1,use=HARMONIE,knockback=2,replay=True,emoji='<:movePlz:928756987532029972>',say=["Madness ? THIS IS SPARTA !","* Out of my ways","SPAR-TA"],description="Pousse gentiment un allié de 2 cases et vous permet de rejouer votre tour")
pepsis = skill("Pepsis","zyy",TYPE_HEAL,500,50,AREA_MONO,area=AREA_CIRCLE_3,use=INTELLIGENCE,cooldown=5,emoji='<:pepsis:930049497214644235>',useActionStats=ACT_SHIELD)
darkShieldEff = effect("Nuit noirsisime","blackknightshield",ENDURANCE,overhealth=75,turnInit=2,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji("<:dsR:930048553835970580>","<:dsR:930048570688675900>"))
darkShield = skill("Nuit noirsisime","zyx",TYPE_ARMOR,500,use=ENDURANCE,effects=darkShieldEff,cooldown=3,emoji='<:dsR:930048553835970580>')
rencCelEff = effect('Rencontre Céleste','rencontreCel',CHARISMA,overhealth=50,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji('<:rcb:930048878668046377>','<:rcr:930048892886720603>'))
rencCel = skill("Rencontre Céleste",'zyw',TYPE_ARMOR,500,use=CHARISMA,range=AREA_MONO,area=AREA_CIRCLE_3,effects=rencCelEff,emoji='<:rencontreceleste:930049458488623104>',cooldown=5,useActionStats=ACT_HEAL)
valse = skill("Valse régénératrice","zyv",TYPE_HEAL,500,80,AREA_DONUT_5,area=AREA_CIRCLE_1,cooldown=7,description="Soigne en zone autour du lanceur et de l'allié le plus blessé",emoji='<:valse:930051603543760936>',useActionStats=ACT_DIRECT,effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_1,80])
pasTech = effect("Jauge Technique","pasTech",emoji='<:pas:930051729523879966>',turnInit=-1,unclearable=True)

pasTech.jaugeValue = jaugeValue(
    emoji=[["<:lej:980923743960461412>","<:mej:980923762016927764>","<:rej:980923786650075228>"],["<:ftlj:980930222679543918>","<:ftrj:980930256032641074>","<:ftmj:980930239901343834>"]],
    conds=[
        jaugeConds(INC_START_TURN,15),
        jaugeConds(INC_ON_ALLY_CRIT,5)
    ]
)

finalTech = skill("Final Technique","zyu",TYPE_DAMAGE,750,60,area=AREA_CIRCLE_1,description="Inflige des dégâts aux ennemis ciblés en consommant votre __Jauge Technique__. Plus la quantité de jauge consommée et élevée, plus la puissance de l'attaque sera grande",emoji='<:final:930051626062991371>',jaugeEff=pasTech,maxPower=150,maxJaugeValue=100,minJaugeValue=20)
dissi = skill("Dissipation","zyt",TYPE_HEAL,750,80,AREA_MONO,ultimate=True,cooldown=7,area=AREA_ALL_ALLIES,emoji='<:dissipation:930049419473211392>',use=HARMONIE,description="__**Nécessite d'avoir au moins une invocation propre sur le terrain**__\nDésinvoque toutes vos invocations pour effectuer un gros soins sur toute votre équipe. La puissance est multipliée par le nombre d'invocation renvoyés")
quickCastEff = effect("Magie Prompte","quickCast",emoji=uniqueEmoji("<:quickCast:930467995283779614>"),description="Permet d'ignorer **1** tour de chargement de la prochaine compétence à chargement utilisée",turnInit=1)
quickCast = skill("Magie Prompte","zys",TYPE_BOOST,1000,range=AREA_MONO,area=AREA_MONO,use=None,cooldown=99,description="Ignore 1 tour de chargement de votre prochaine compétence",initCooldown=3,replay=True,emoji='<:quickCast:930467995283779614>',effects=quickCastEff)
foyer = skill("Foyer","zyr",TYPE_HEAL,500,35,range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=5,use=CHARISMA,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],emoji="<:fireplace:931666078092902471>")
sweetHeatEff = effect('Douce chaleur',"sweetHeat",HARMONIE,power=25,turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,description="Un effet qui soigne le porteur pendant 3 tours")
sweetHeat = skill("Flammes intérieurs","zyq",TYPE_DAMAGE,500,85,range=AREA_CIRCLE_3,cooldown=7,effectOnSelf=sweetHeatEff,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],emoji='<:fireStrike:931715107002662912>')
darkSweetHeat = skill("Flammes infernales","zyp",TYPE_DAMAGE,500,75,range=AREA_DIST_5,cooldown=7,effectOnSelf=sweetHeatEff,use=MAGIE,description="Inflige des dégâts aux ennemis ciblés et vous octroi un effet régénératif",area=AREA_CONE_2,group=SKILL_GROUP_DEMON,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],emoji='<:infFlames:931716686745305149>')
nacre = effect("Bulle nacrée",'nacre1',INTELLIGENCE,overhealth=40,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,turnInit=2,stackable=True,emoji=uniqueEmoji('<:nacre:931666050322419732>'))
shell = skill("Coquille",'zyo',TYPE_ARMOR,500,range=AREA_DONUT_5,effects=nacre,effectOnSelf=nacre,cooldown=5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],emoji='<:shell:931714079154921472>')
nacreHit = skill("Frappe nacrée",'syn',TYPE_DAMAGE,500,80,range=AREA_CIRCLE_3,effectOnSelf=nacre,cooldown=5,use=HARMONIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER])
holyShot = skill("Flèche sacrée",'sym',TYPE_DAMAGE,500,120,cooldown=7,group=SKILL_GROUP_HOLY,maxHpCost=10,emoji='<:hollyArrow:931713039789588550>')
demonStrike = skill("Frappe démoniaque",'syl',TYPE_DAMAGE,500,50,cooldown=7,group=SKILL_GROUP_DEMON,area=AREA_CIRCLE_1,repetition=3,hpCost=15,emoji='<:demonStrike:933504978599952404>')
purify = skill("Purification","syk",TYPE_HEAL,250,60,use=CHARISMA,cooldown=5,group=SKILL_GROUP_HOLY,maxHpCost=5,emoji='<:holyHeal1:931703505268408341>')
benediction = skill("Bénédiction Avancée","syj",TYPE_HEAL,750,120,use=CHARISMA,cooldown=8,group=SKILL_GROUP_HOLY,maxHpCost=15,emoji='<:benediction:931703487258046464>')
transfert = skill("Transfert",'svi',TYPE_HEAL,350,55,use=CHARISMA,hpCost=10,group=SKILL_GROUP_DEMON,cooldown=5,emoji='<:transfert:931709644542451734>')
blackDarkMagic = skill("Magie interdite",'svh',TYPE_HEAL,350,100,use=CHARISMA,hpCost=35,group=SKILL_GROUP_DEMON,cooldown=8,emoji='<:darkMagic:931707457020002346>')
fisure = skill("Fissure",'svg',TYPE_DAMAGE,500,80,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],cooldown=5,damageOnArmor=3,emoji='<:break:931703557420367873>')
seisme = skill("Séisme",'svf',TYPE_DAMAGE,500,120,range=AREA_MONO,area=AREA_CIRCLE_3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],cooldown=5,damageOnArmor=3,emoji='<:seisme:931703529561800744>')
burningSoul = effect("Âme embrasée",'burningSoul',HARMONIE,power=40,turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji='<:ayss:931711751702085672>')
abime = skill("Âbime",'sve',TYPE_INDIRECT_DAMAGE,500,area=AREA_CIRCLE_2,cooldown=5,ultimate=True,group=SKILL_GROUP_DEMON,hpCost=25,effects=[burningSoul],emoji='<:abyss:931711751702085672>')
fadingSoul = effect("Anéantissement",'fadingSoul',HARMONIE,power=50,turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji='<:purification:931711772396777572>')
extermination = skill("Extermination",'svd',TYPE_INDIRECT_DAMAGE,500,0,effects=fadingSoul,group=SKILL_GROUP_HOLY,maxHpCost=15,cooldown=5,emoji='<:purification:931711772396777572>')
darkHeal = copy.deepcopy(lightHeal2)
darkHeal.name, darkHeal.id, darkHeal.emoji, darkHeal.condition = "Assombrissement", "svc", '<:darkHeal:931883636481982484>', [0,3,ELEMENT_DARKNESS]
matriceEff2 = copy.deepcopy(dmgUp)
matriceEff2.power = 25
matriceEff1 = effect("Matrice amplificatrice","matriceAmplEff",trigger=TRIGGER_ON_REMOVE,callOnTrigger=matriceEff2)
matriceEmpli = skill("Matrice amplificatrice",'svb',TYPE_BOOST,500,range=AREA_MONO,effects=matriceEff1,cooldown=7,description="Augmente de **{0}%** vos dégâts infligés lors de votre prochain tour".format(matriceEff2.power))
calestJump = skill("Plongeon Céleste",'sva',TYPE_DAMAGE,750,75,range=AREA_DIST_3,area=AREA_CIRCLE_1,tpCac=True,cooldown=5,emoji='<:ceslestJump:931899235270545469>')
lohicaUltLauch = skill("Brûme empoisonée","suz",TYPE_INDIRECT_DAMAGE,750,area=AREA_CONE_3,use=MAGIE,tpCac=True,effects="me",cooldown=7,ultimate=True,emoji='<:brume:1058843224933933096>',description="Téléporte à côté de la cible et empoisonne les alentours",effPowerPurcent=150)
lohicaUltCastEff = effect("Cast - Brûme empoisonée","lohicaUltCastEff",turnInit=2,silent=True,replique=lohicaUltLauch,emoji=uniqueEmoji('<a:lohicaUltCast:932823354841399296>'))
lohicaUltCast = copy.deepcopy(lohicaUltLauch)
lohicaUltCast.effectOnSelf, lohicaUltCast.effects, lohicaUltCast.tpCac = lohicaUltCastEff, [None], False
fairyFligth = skill("Envolée féérique",'suy',TYPE_DAMAGE,500,80,range=AREA_CIRCLE_1,jumpBack=1,knockback=3,cooldown=5,emoji='<:envolee:941677380181823489>')
aliceDanceEff = effect("En rythme !",'aliceDanceEff',CHARISMA,strength=7,magie=7,description="\"Tous avec moi !\"",emoji=sameSpeciesEmoji('<:dyB:932618243280085062>','<:dyR:932618257960161331>'))
aliceDanceFinal = skill("Chorégraphie Dynamique","corDynFinal",TYPE_BOOST,500,range=AREA_MONO,area=AREA_DONUT_4,effects=aliceDanceEff,emoji='<:dyna:932618114892439613>',use=CHARISMA,cooldown=5,message="{0} se donne à fond !",description="Se met à danser pendant 3 tours, durant lesquels les alliés à portée voient leur statistiques offensives augmenter",effPowerPurcent=125)
aliceDanceGuideEff1 = effect("Chrorégraphie dynamique",'aliceDanceCastEff1',turnInit=2,silent=True,replique=aliceDanceFinal,emoji=uniqueEmoji('<:dyna:932618114892439613>'),stackable=True)
aliceDanceGuide1 = copy.deepcopy(aliceDanceFinal)
aliceDanceGuide1.effectOnSelf, aliceDanceGuide1.message, aliceDanceGuide1.id, aliceDanceGuide1.area, aliceDanceGuide1.effPowerPurcent = aliceDanceGuideEff1, "{0} continue de danser", "sc", AREA_DONUT_3, 110
aliceDanceGuideEff2 = copy.deepcopy(aliceDanceGuideEff1)
aliceDanceGuideEff2.replica = aliceDanceGuide1
aliceDance = copy.deepcopy(aliceDanceGuide1)
aliceDance.effectOnSelf, aliceDance.message, aliceDance.effPowerPurcent = aliceDanceGuideEff2, "{0} commence une {1} !", 100
auroreEff = effect("Aurore",'auroreEff',CHARISMA,strength=5,magie=5,turnInit=3,emoji=sameSpeciesEmoji("<:aurB:934675375689170995>","<:aurR:934675360946212914>"))
aurore = skill('Aurore','sux',TYPE_BOOST,500,effects=auroreEff,use=CHARISMA,cooldown=7,area=AREA_CIRCLE_1,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],emoji='<:aurore:934675235268087858>')
crepEff = effect("Crépuscule",'crepEff',INTELLIGENCE,strength=-5,magie=-5,turnInit=3,emoji=sameSpeciesEmoji('<:crepB:934675391145201664>','<:crepR:934675411995074560>'))
crep = skill('Crépuscule','suw',TYPE_MALUS,500,effects=crepEff,use=INTELLIGENCE,cooldown=7,area=AREA_CIRCLE_1,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS],emoji='<:crepuscule:934675249541292033>')
toMelee = skill('Corps à corps','suv',TYPE_DAMAGE,350,30,tpCac=True,cooldown=3,emoji='<:cac:932765903102291999>',replay=True,range=AREA_CIRCLE_3)
toDistance = skill('Déplacement','suu',TYPE_DAMAGE,350,30,AREA_INLINE_2,cooldown=3,jumpBack=2,emoji='<:dep:932765889017839636>',replay=True)
autoBombRush = skill("Lance-Bombe Robot",'sut',TYPE_SUMMON,750,0,AREA_CIRCLE_4,ultimate=True,nbSummon=5,emoji='<:brAuto:933508393036029992>',invocation="Bombe Robot",cooldown=7,description="Invoque 3 Bombes Robots\nSeule la première Bombe Robot est soumise à la limitation d'invocation par équipe",shareCooldown=True)
killerWailUltimate = skill("Haut Perceur 5.1",'sus',TYPE_SUMMON,750,nbSummon=5,ultimate=True,cooldown=10,use=MAGIE,invocation='Haut-Perceur 5.1',emoji='<:killerWail:933516496196497439>',description='Invoque 5 Haut-Perceur 5.1.\nSeul le premier est soumis à la limitation d\'invocation par équipe',shareCooldown=True)
invocSeaker = skill("Invocation - Traqueur",'sur',TYPE_SUMMON,350,range=AREA_CIRCLE_3,cooldown=5,shareCooldown=True,invocation='Traqueur',emoji='<:seeker:933508405463777351>')
darkBoom = skill("Explosion Sombre",'darkBoom',TYPE_DAMAGE,500,int(explosion.power*0.35),cooldown=explosion.cooldown,percing=0,area=AREA_CIRCLE_2,effectOnSelf=explosion.effectOnSelf,accuracy=explosion.accuracy,setAoEDamage=True,repetition=2,ultimate=True,use=MAGIE,emoji='<a:db2:933676696899551273>',hpCost=30,group=SKILL_GROUP_DEMON,description="Inflige des dégâts dans une grande zone à deux reprises",damageOnArmor=0.8,url="https://media.discordapp.net/attachments/826608054468345866/1084893638812762162/20230313_183917.gif")
darkBoomCastEff = effect("Cast - Explosion Sombre",'castDarkBoom',turnInit=2,replique=darkBoom,emoji=sameSpeciesEmoji('<a:boomCastB:916382499704275005>','<a:boomCastR:916382515135144008>'),silent=True)
darkBoomCast = copy.deepcopy(darkBoom)
darkBoomCast.id, darkBoomCast.power, darkBoomCast.effectOnSelf, darkBoomCast.hpCost, darkBoomCast.url = 'suq', 0, darkBoomCastEff, 0, None
doubleShot = skill("Double Tir",'sup',TYPE_DAMAGE,500,60,repetition=2,condition=[EXCLUSIVE,ASPIRATION,OBSERVATEUR],emoji='<:doubleShot:933506156616368169>',cooldown=5)
harmShot = skill("Tir Harmonique",'suo',TYPE_DAMAGE,500,75,use=HARMONIE,condition=[EXCLUSIVE,ASPIRATION,TETE_BRULE],cooldown=3,emoji='<:hamShot:933506175633330216>')
mageSkill = skill("Détonnation",'sun',TYPE_DAMAGE,500,80,condition=[EXCLUSIVE,ASPIRATION,MAGE],area=AREA_CIRCLE_1,setAoEDamage=True,cooldown=3,use=MAGIE,emoji='<:ice:941494417926270987>')
benitWater = skill("Eau bénite",'sum',TYPE_DAMAGE,500,75,area=AREA_CIRCLE_1,cooldown=3,maxHpCost=5,group=SKILL_GROUP_HOLY,use=MAGIE,emoji='<:holyStrike:931703468652118067>')
tempShare30, divShareEff2 = copy.deepcopy(shareTabl[5]), copy.deepcopy(absEff)
tempShare30.turnInit, divShareEff2.power, divShareEff2.turnInit = 3, 20, 3
shareSkill = skill("Partage divin",'sul',TYPE_HEAL,500,50,use=CHARISMA,maxHpCost=10,cooldown=5,effects=[tempShare30,divShareEff2],effBeforePow=True,description="Donne l'effet Partage à la cible tout en augmentant les soins reçus par cette dernière pendant 3 tours tout en la soignant",emoji='<:divineShare:949891460503855125>')
extraMedica = skill("Extra Medica",'suk',TYPE_HEAL,750,int(infraMedica.power*0.8),AREA_MONO,area=AREA_CIRCLE_2,use=CHARISMA,effects=infraMedica.effects,cooldown=infraMedica.cooldown+2,group=SKILL_GROUP_HOLY,condition=[EXCLUSIVE,ASPIRATION,ALTRUISTE],description="Soigne les alliés proches et leur donne l'effet __Extra Médica__ pendant 3 tours",maxHpCost=10,emoji=infraMedica.emoji)
foulleeEff = effect("Foulée légère",'ppUniquePassifEff',emoji='<:quicky:934832147511017482>',turnInit=-1,unclearable=True,dodge=20,description="Augmente de **20%** votre probabilité d'esquiver des attaques")
foullee = skill("Foulée Légère",'suj',TYPE_PASSIVE,350,condition=[EXCLUSIVE,ASPIRATION,POIDS_PLUME],use=None,effectOnSelf=foulleeEff,emoji='<:quicky:934832147511017482>',quickDesc="Augmente vos chances d'esquiver une attaque")
lifePulseRegenEff = effect("Rénégénration","lifePulseHeal",CHARISMA,power=20,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,turnInit=3,emoji='<:heal:911735386697519175>',description="Soigne le porteur en début de tour")
lifePulseFinal = skill("Pulsation Vitale",'sui',TYPE_HEAL,1000,110,range=AREA_MONO,ultimate=True,cooldown=10,initCooldown=3,area=AREA_CIRCLE_4,effects=lifePulseRegenEff,use=CHARISMA,emoji='<a:lifePulse:934968172107403324>',group=SKILL_GROUP_HOLY,maxHpCost=35,description="Soigne les alliés aux alentours et leur donne un effet de régénération sur la durée",url='https://cdn.discordapp.com/attachments/927195778517184534/934968488550871140/20220124_012750.gif')
lifePulseCastEff = effect("Cast - Pulsation Vitale",'lifePulseCast',replique=lifePulseFinal,silent=True,turnInit=2,emoji='<a:lifePulseCast:934968316882219068>')
lifePulseCast = copy.deepcopy(lifePulseFinal)
lifePulseCast.power, lifePulseCast.effectOnSelf, lifePulseCast.url, lifePulseCast.maxHpCost, lifePulseCast.effects= 0, lifePulseCastEff, None, 0, [None]
crimsomLotus = skill("Lotus Pourpre",'suh',TYPE_DAMAGE,750,150,emoji='<a:crimsomLotus:934980446176047104>',area=AREA_LINE_6,use=CHARISMA,useActionStats=ACT_BOOST,description="Inflige des dégâts Charisme sur une ligne droite",cooldown=7,ultimate=True,url='https://cdn.discordapp.com/attachments/927195778517184534/934981029649874974/20220124_021239.gif',condition=[EXCLUSIVE,ASPIRATION,IDOLE])
crimsomLotusCastEff = effect("Cast - Lotus Pourpre",'crimstomLotusCastEff',turnInit=2,replique=crimsomLotus,silent=True,emoji=uniqueEmoji('<a:emoji_52:934980282577203210>'))
crimsomLotusCast = copy.deepcopy(crimsomLotus)
crimsomLotusCast.power, crimsomLotusCast.effectOnSelf, crimsomLotusCast.url = 0, crimsomLotusCastEff, None
abnegation = skill("Abnégation",'sug',TYPE_HEAL,750,200,emoji='<:abnegation:935538856286109726>',range=AREA_MONO,area=AREA_CIRCLE_5,group=SKILL_GROUP_DEMON,hpCost=90,ultimate=True,cooldown=7,use=CHARISMA,description="Soigne ou réanime vos alliés à portée au prix d'une grande quantité de PV",effectAroundCaster=[TYPE_RESURECTION,AREA_CIRCLE_5,150])
jumpedSplashDownLanding = copy.deepcopy(classicSplashdown)
jumpedSplashDownLanding.name, jumpedSplashDownLanding.range, jumpedSplashDownLanding.tpCac, jumpedSplashDownLanding.areaOnSelf, jumpedSplashDownLanding.url, jumpedSplashDownLanding.cooldown = "Choc Chromatique Sauté", AREA_DIST_5, True, True, "https://cdn.discordapp.com/attachments/935769576808013837/935781564145623131/20220126_072054.gif", 7
jsdJumEff = effect("Cast - Choc Chromatique Sauté", 'JumpingSlashDownEff',turnInit=2,silent=True,emoji=classicSplashdown.emoji,invisible=True,immunity=True,replique=jumpedSplashDownLanding)
jumpedSplashDown = copy.deepcopy(jumpedSplashDownLanding)
jumpedSplashDown.power, jumpedSplashDown.tpCac, jumpedSplashDown.url, jumpedSplashDown.effectOnSelf = 0, False, None, jsdJumEff
splashdown = skill("Choc Chromatique",classicSplashdown.id,TYPE_DAMAGE,750,0,ultimate=True,emoji=classicSplashdown.emoji,become=[classicSplashdown,jumpedSplashDown],area=AREA_CIRCLE_2)
pneumaArmor = effect("Pneuma",'pneumaArmor',INTELLIGENCE,overhealth=50,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
pneuma = skill("Pneuma",'suf',TYPE_DAMAGE,750,125,condition=[EXCLUSIVE,ASPIRATION,PREVOYANT],ultimate=True,emoji='<:pneuma:936515231562219581>',cooldown=7,area=AREA_LINE_3,accuracy=110,use=INTELLIGENCE,useActionStats=ACT_SHIELD,effectAroundCaster=[TYPE_ARMOR,AREA_CIRCLE_2,pneumaArmor])
absorbingStrike = skill("Frappe Convertissante",'sue',TYPE_DAMAGE,500,75,AREA_CIRCLE_2,cooldown=3,emoji='<:healStrike:936470624921075733>',lifeSteal=35)
absorbingArrow = skill("Flèche Convertissante",'sud',TYPE_DAMAGE,500,75,AREA_DIST_6,cooldown=3,emoji='<:healShot:936470641450815538>',lifeSteal=35)
absorbingStrike2 = skill("Frappe Convertissante Avancée",'suc',TYPE_DAMAGE,750,120,AREA_CIRCLE_2,cooldown=7,emoji='<:killStrike:936470659389849622>',lifeSteal=50)
absorbingArrow2 = skill("Flèche Convertissante Avancée",'sub',TYPE_DAMAGE,750,120,AREA_DIST_6,cooldown=7,emoji='<:killShot:936470681015709716>',lifeSteal=50)
magiaHeal = skill("Sort Vampirique","sua",TYPE_DAMAGE,500,80,use=MAGIE,lifeSteal=50,cooldown=5,emoji='<:vampireSpell:961190223168024606>',effectOnSelf=vampirismeEff,selfEffPurcent=50)
aff2Eff1 = copy.deepcopy(vulne)
aff2Eff1.power, aff2Eff1.stat, aff2Eff1.description = 3, INTELLIGENCE, "Augmente les dégâts subis par le porteur de **3%**, affecté par les statistiques"
aff2Eff2 = copy.deepcopy(dmgDown)
aff2Eff2.power, aff2Eff2.stat, aff2Eff2.description = 3, INTELLIGENCE, "Réduit les dégâts infligés par le porteur de **3%**, affecté par les statistiques"
bloodPactEff = effect("Pacte de Sang",'bloodyPact',power=50,turnInit=-1,emoji='<:bloodpact:937361536043843595>',unclearable=True,description="Fixe à **{0}%** le taux de vol de vie des Berskers")
bloodPact = skill("Conviction du Berserkeur",'sty',TYPE_PASSIVE,500,use=None,condition=[EXCLUSIVE,ASPIRATION,BERSERK],effectOnSelf=bloodPactEff,emoji='<:bloodpact:937361536043843595>',quickDesc="Augmente votre taux de vol de vie natif")
aff2 = skill("Affaiblissement Avancée",'stz',TYPE_MALUS,500,area=AREA_CIRCLE_1,use=INTELLIGENCE,effects=[aff2Eff1,aff2Eff2],cooldown=5,emoji='<:affaib2:963394071894835220>')
expediantDefenseUp = copy.deepcopy(defenseUp)
expediantDefenseUp.power, expediantDefenseUp.stat, expediantDefenseUp.description = 7, INTELLIGENCE, "Réduit de **7%** les dégâts subis par le porteur, affectés par les statistiques"
expediantSpeedBoost = effect("Thèse des rafales hurlantes",'expediantSpeedBooost',INTELLIGENCE,agility=10,emoji='<:expediant:937370418363367495>')
expediant = skill("Thèse fluidiques",'stx',TYPE_BOOST,750,range=AREA_MONO,area=AREA_CIRCLE_3,use=INTELLIGENCE,cooldown=7,effects=[expediantDefenseUp,expediantSpeedBoost],emoji='<:expediant:937370418363367495>')
dinationEff = copy.deepcopy(dmgUp)
dinationEff.power, dinationEff.stat, dinationEff.turnInit = 4, INTELLIGENCE, 3
divination = skill("Divination",'stw',TYPE_BOOST,500,range=AREA_MONO,area=AREA_CIRCLE_3,use=INTELLIGENCE,cooldown=7,effects=dinationEff,emoji='<:divination:937370483777748993>')
macroCosmosEff = copy.deepcopy(dmgUp)
macroCosmosEff.power, macroCosmosEff.stat, macroCosmosEff.turnInit = 5, INTELLIGENCE, 3
macroCosmos = skill("Macro-cosmos",'stv',TYPE_DAMAGE,500,130,area=AREA_CIRCLE_2,effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_2,macroCosmosEff],cooldown=7,ultimate=True,use=INTELLIGENCE,useActionStats=ACT_BOOST,description="Inflige des dégâts aux ennemis et augmente les DI des alliés",emoji='<:macroCosmos:937370437573287997>')
tintabuleEff = effect("Tintinnabule",'tintabule',CHARISMA,power=20,turnInit=3,lvl=5,type=TYPE_INDIRECT_HEAL,area=AREA_CIRCLE_2,emoji='<:tintabulbe:937370359257255976>',trigger=TRIGGER_AFTER_DAMAGE,description="Lors des 5 prochaines attaques subie par le porteur, soigne ce dernier et ses alliés dans la zone d'effet")
tintabule = skill("Tintinnabule",'stu',TYPE_INDIRECT_HEAL,500,effects=tintabuleEff,cooldown=5,emoji='<:tintabulbe:937370359257255976>')
verEarthEff = effect("VerTerre préparé",'verEarthReady',turnInit=5,emoji='<:verTerre:937807119934160917>')
verMiracleEff = effect("VerMiracle préparé",'verMiracleReady',turnInit=5,emoji='<:verMiracle:937807083447943288>')
verFire = skill("VerFeu",'stt',TYPE_DAMAGE,power=70,emoji='<:verFeu:937807102209060894>',use=MAGIE,effectOnSelf=verEarthEff,rejectEffect=[verEarthEff,verMiracleEff])
verEarth = skill("VerTerre",'stt',TYPE_DAMAGE,power=90,emoji='<:verTerre:937807119934160917>',use=MAGIE,needEffect=verEarthEff,effectOnSelf=verMiracleEff,cooldown=1)
verMiracle = skill("VerMiracle",'stt',TYPE_DAMAGE,power=145,emoji='<:verMiracle:937807083447943288>',use=MAGIE,needEffect=verMiracleEff,cooldown=5)
comboVerMiracle = skill("Combo VerMiracle",'stt',TYPE_DAMAGE,500,verMiracle.power,area=AREA_CIRCLE_1,emoji=verMiracle.emoji,become=[verFire,verEarth,verMiracle],use=MAGIE,description="Cette compétence permet d'effectuer l'enchaînement \"VerFeu\",\"VerTerre\" et \"VerMiracle\".\nIl est impossible d'utiliser \"VerMiracle\" sans avoir utilisé \"VerTerre\" précédament, lui-même necessitant d'avoir utlisé \"VerFeu\" au paravant")
faucheCroixEff = effect('Potence Améliorée préparé','faucheCroixReady',turnInit=5,emoji='<:potence:1007583474510733333>')
faucheNean = skill("Potence Améliorée",'sts',TYPE_DAMAGE,power=100,range=AREA_CIRCLE_2,area=AREA_ARC_1,needEffect=[faucheCroixEff],cooldown=4,emoji='<:potence:1007583474510733333>',description="Effectue une attaque en demi-cercle et ajoute 10 pts à votre **Jauge d'Âme**")
faucheCroix = skill("Gibet",'sts',TYPE_DAMAGE,power=80,range=AREA_CIRCLE_2,effectOnSelf=faucheCroixEff,rejectEffect=faucheCroixEff,cooldown=1,area=AREA_ARC_2,emoji='<:gibet:1007583449273614378>')
comboFaucheCroix = skill("Combo Potence Améliorée",'sts',TYPE_DAMAGE,price=500,power=faucheCroix.power,emoji=faucheCroix.emoji,become=[faucheNean,faucheCroix],description="Permet d'effectuer l'enchaînement \"Fauchage du néan\" et \"Fauchage croisé\".\nIl est nécessaire d'avoir préalablement utilisé \"Fauchage du néan\" pour pouvoir utiliser \"Fauchage croisé\"")
reaperEff = effect("Dessins de la Camarade", "that'sALongName", power=30, turnInit=5, type=TYPE_MALUS, emoji="<:longName:938167649106538556>",description="Augmente de **10%** les dégâts infligés par l'entité à l'origine de cet effect sur le porteur.\nSi le porteur est vaincu en ayant toujours l'effet sur lui (que ce soit de la main de l'initiateur de l'effet ou d'un autre), l'initiateur de l'effet se soigne de **{0}%** de ses PV maximums et sa Jauge d'Âme augmente de 5 pts supplémentaires")
deathShadow = skill("Ombre de la Mort","str",TYPE_DAMAGE,750,90,range=AREA_CIRCLE_2,emoji='<:deathShadow:937370374788755516>',effBeforePow=True,cooldown=7,effects=reaperEff,description="Inflige des dégâts et donne à la cible augmentant vos futurs dégâts à son encontre pendant plusieurs tours")
theEnd = skill("Dernier Voyage","stq",TYPE_DAMAGE,750,200,AREA_CIRCLE_3,cooldown=5,tpCac=True,ultimate=True,emoji='<a:lbReaper:938175619504689193>',damageOnArmor=1.35,description="Après un tour de chargement, délivre une puissante attaque à l'ennemi ciblé.\nSi cette dernière est sous un effet <:longName:938167649106538556> __Dessins de la Camarade__ dont vous êtes l'initiateur, la puissance de cette attaque augmente de **20%**",lifeSteal=25,url='https://cdn.discordapp.com/attachments/935769576808013837/938175773137862756/20220201_214401.gif')
theEndCastEff = effect("Cast - Dernier Voyage","reaperLbCast",turnInit=2,silent=True,replique=theEnd,emoji='<a:lbReaperCast:938175259964747816>')
theEndCast = copy.deepcopy(theEnd)
theEndCast.power, theEndCast.url, theEndCast.effectOnSelf, theEndCast.tpCac = 0, None, theEndCastEff, False
cure3Eff = effect("Extra Soins Préparé","cureIIready",turnInit=4,emoji='<:extraHeal:952522927214051348>')
cure2 = skill("Soins","stp",TYPE_HEAL,0,40,emoji='<:heal:911735386697519175>',effectOnSelf=cure3Eff,use=CHARISMA,rejectEffect=[cure3Eff])
cure3 = skill("Giga Soins","spt",TYPE_HEAL,0,55,emoji='<:extraHeal:952522927214051348>', needEffect=cure3Eff,cooldown=3,use=CHARISMA,area=AREA_CIRCLE_1)
cure2Bundle = skill("Giga Soins","stp",TYPE_HEAL,500,use=CHARISMA,become=[cure2,cure3],emoji='<:extraHeal:952522927214051348>',description="Permet d'utiliser les compétences {0} __{1}__ et {2} __{3}__.\n{2} __{3}__ ne peut être utilisé que si {0} __{1}__ a été utilisé préalablement".format(cure2.emoji,cure2.name,cure3.emoji,cure3.name))
assises = skill("Assises","sto",TYPE_DAMAGE,750,135,area=AREA_CIRCLE_1,use=CHARISMA,useActionStats=ACT_HEAL,cooldown=7,effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_2,65],condition=[EXCLUSIVE,ASPIRATION,ALTRUISTE],emoji='<:assise:941494380714414110>',description="Inflige des dégâts aux ennemis ciblés et soigne les alliés autour de vous")
debouses = skill("Debouses","stl",TYPE_HEAL,750,75,area=AREA_CIRCLE_1,use=CHARISMA,cooldown=7,useActionStats=ACT_HEAL,effectAroundCaster=[TYPE_DAMAGE,AREA_CIRCLE_2,75],condition=[EXCLUSIVE,ASPIRATION,VIGILANT],emoji='<:debouse:941494363748438027>',description="Soigne les alliés ciblés et inflige des dégâts autour de vous")
impactShield = effect("Armure Impactante",'impactArmor',INTELLIGENCE,overhealth=50,emoji='<:impact:951379371489382400>',turnInit=3,stackable=True,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,description="Protège de quelques dégâts directs")
impact = skill("Frappe Impactante","stk",TYPE_DAMAGE,500,75,AREA_CIRCLE_3,[EXCLUSIVE,ASPIRATION,PROTECTEUR],emoji='<:impact:941494342722412585>',effectOnSelf=impactShield,use=INTELLIGENCE,useActionStats=ACT_SHIELD,effectAroundCaster=[TYPE_HEAL,AREA_MONO,50],cooldown=3,description="En plus d'infliger quelques dégâts, cette compétence soigne et donne une petite armure au lanceur")
heartStoneSecEff = copy.deepcopy(defenseUp)
heartStoneSecEff.power, heartStoneSecEff.stat, heartStoneSecEff.turnInit = 5, INTELLIGENCE, 3
heartStoneSecEff2 = copy.deepcopy(heartStoneSecEff)
heartStoneSecEff2.turnInit = 1
heartStone = skill("Coeur de pierre","stj",TYPE_ARMOR,750,cooldown=3,emoji='<:earthStonr:941681433863421952>',effects=[impactShield, heartStoneSecEff, heartStoneSecEff2],condition=[EXCLUSIVE,ASPIRATION,PROTECTEUR],description="Confère une petite armure à l'allié ciblé et réduit ses dégâts reçus\nL'armure dure plus longtemps que la réduction de dégâts",replay=True)
erodStrike = skill("Frappe érosive","sti",TYPE_DAMAGE,500,110,AREA_CIRCLE_3,cooldown=5,erosion=100,emoji='<:frappeEro:941677350872047640>',damageOnArmor=1.1)
genesis = skill("Génésis","sth",TYPE_DAMAGE,750,185,area=AREA_LINE_4,group=SKILL_GROUP_HOLY,use=MAGIE,maxHpCost=35,cooldown=7,emoji='<:genesis:946529693459419217>')
invertion = skill("Inversion",'stg',TYPE_DAMAGE,500,90,group=SKILL_GROUP_DEMON,use=CHARISMA,useActionStats=ACT_HEAL,hpCost=15,cooldown=5)
ice2Eff = effect("Détonnation avancée","ice2Eff",MAGIE,power=60,area=AREA_CIRCLE_1,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji='<:ice2:941494399337136208>')
ice2 = skill("Détonnation Avancée","stf",TYPE_INDIRECT_DAMAGE,500,use=MAGIE,cooldown=3,emoji='<:ice2:941494399337136208>',condition=[EXCLUSIVE,ASPIRATION,SORCELER],effects=ice2Eff)
lifeWind = skill("Vent de vie","ste",TYPE_HEAL,500,60,AREA_MONO,[EXCLUSIVE,ASPIRATION,VIGILANT],area=AREA_CIRCLE_2,use=CHARISMA,cooldown=3,emoji='<:divineWind:949888558355869747>')
renf2Eff1 = copy.deepcopy(defenseUp)
renf2Eff1.power, renf2Eff1.stat = 10, INTELLIGENCE
renf2Eff2 = copy.deepcopy(dmgUp)
renf2Eff2.power, renf2Eff2.stat = 10, INTELLIGENCE
renf2 = skill("Renforcement Avancé","std",TYPE_BOOST,750,condition=[EXCLUSIVE,ASPIRATION,INOVATEUR],effects=[renf2Eff2,renf2Eff1],cooldown=7,emoji='<:renfAv:989529323063107605>')
entraide = skill("Entraide","stc",TYPE_HEAL,500,100,range=AREA_DONUT_6,area=AREA_CIRCLE_2,cooldown=7,group=SKILL_GROUP_DEMON,hpCost=25,use=CHARISMA,emoji='<:entraide:941677392722808913>')
perfectShot = skill("Tir Parfait","stb",TYPE_DAMAGE,750,170,cooldown=7,ultimate=True,emoji='<:tirParfait:961187760134311996>')
lastRessource = skill("Dernier recours","sta",TYPE_RESURECTION,500,135,cooldown=7,shareCooldown=True,use=STRENGTH,initCooldown=5,emoji='<:strengthRaise:949890176195383318>')
strengthOfDesepearance = skill("Force du désespoir","ssz",TYPE_RESURECTION,500,135,cooldown=7,shareCooldown=True,use=MAGIE,initCooldown=5,emoji='<:magicRaise:949890198190305300>')
nova = skill("Nova","ssy",TYPE_DAMAGE,500,90,use=INTELLIGENCE,useActionStats=ACT_SHIELD,emoji='<:wtfIsThatAlready:1023615143063601283>',hpCost=5,cooldown=5,group=SKILL_GROUP_DEMON)
undeadEff2 = effect("Mort en sursie","undeadEff2",turnInit=-1,description="Augmente vos soins et vol de vies reçus mais vous inflige des dégâts indirects équivalents à 30% de vos PV Maximums en fin de tour",emoji='<a:undead:953259661568663602>',silent=False,power=30,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN)
undeadEff = effect("Mort-Vivant","undead",turnInit=20,callOnTrigger=undeadEff2,description="1 fois par combats, en recevant des dégâts mortels, le porteur est soigné de l'intégralité de ses PV mais subis l'effet {0} __{1}__, lui infligeant des dégâts à la fin de son tour".format(undeadEff2.emoji[0][0],undeadEff2.name),emoji='<:undead:944989590836637736>',silent=False,lvl=1)
undead = skill("Mort Vivant","ssx",TYPE_PASSIVE,500,effectOnSelf=undeadEff,emoji='<:undead:944989590836637736>',group=SKILL_GROUP_DEMON,description=undeadEff.description)
ironStormDmgBoost = copy.deepcopy(dmgUp)
ironStormDmgBoost.power = 10
ironStormReady = effect('Tempête de Fer préparée','ironStormReady',turnInit=3,emoji='<:ironStorm3:945054940412383332>')
ironStorm = skill("Tempête de fer","ssw",TYPE_DAMAGE,power=100,range=AREA_CIRCLE_2,emoji='<:ironStorm3:945054940412383332>',cooldown=3,effectOnSelf=ironStormDmgBoost,description="Inflige des dégâts puis augmente vos dégâts de 10% pour le prochain tour",needEffect=ironStormReady)
mutilationReady = effect("Mutilation préparée","mutilationReady",turnInit=3,emoji='<:ironStorm2:945054925291925554>')
mutilation = skill('Mutilation',"ssw",TYPE_DAMAGE,power=90,range=AREA_CIRCLE_2,emoji='<:ironStorm2:945054925291925554>',effectOnSelf=ironStormReady,needEffect=mutilationReady,rejectEffect=ironStormReady)
powerStrike = skill("Coup puissant","ssw",TYPE_DAMAGE,power=80,range=AREA_CIRCLE_2,rejectEffect=[mutilationReady,ironStormReady],effectOnSelf=mutilationReady,emoji='<:ironStorm1:945054903452180500>')
ironStormBundle = skill("Combo Tempête de Fer","ssw",TYPE_DAMAGE,500,become=[powerStrike,mutilation,ironStorm],description="Permet d'effetuer l'enchaînement Coup Puissant, Mutilation et Tempête de Fer\nLes compétences doivent être effectuée dans cet ordre définis\n\n__Tempête de Fer__ augmente vos dégâts de 10% pour le tour suivant",emoji='<:ironStorm3:945054940412383332>')
bolideEff = effect("Bolide",'vroumvroum',immunity=True,emoji='<:bolide:945058044495167538>',description="Le porteur est insensible à tous dégâts")
bolide = skill("Bolide","ssv",TYPE_BOOST,500,range=AREA_MONO,effects=bolideEff,cooldown=7,use=None,emoji='<:bolide:945058044495167538>',description="Réduit vos PV courrants à **1**, puis vous rend invulnérable à tous dégâts pendant un tour")
invincibleEff = effect("Invincible","borringImunity",immunity=True,emoji='<:invincible:945054839203852359>',description="Le porteur est insensible à tous dégâts")
invincible = skill("Invincible","ssu",TYPE_BOOST,750,range=AREA_MONO,emoji='<:invincible:945054839203852359>',use=None,cooldown=10,effectOnSelf=invincibleEff,description="Vous rend invulnérable à tous dégâts pendant un tour")
holmgangEff = effect("Holmgang","Holmgang",emoji='<:complicated:945054889573240883>',description="Cet effet empêche le porteur de tomber en dessous de **1** PV et augmente les soins reçus et le vol de vie de {0}%",power=15,aggro=-15)
holmgang = skill("Holmgang","sst",TYPE_BOOST,500,range=AREA_MONO,effPowerPurcent=200,emoji='<:complicated:945054889573240883>',use=None,effects=holmgangEff,cooldown=5,effectAroundCaster=[TYPE_MALUS,AREA_DONUT_2,chained],description="Empêche vos PV de tomber en dessous de 1 pendant 1 tour")
extraVerFoudreReady = effect("Extra VerFoudre préparé","extraVerFoudreReady",turnInit=5,emoji='<:extraVerFoudre:946042839287091300>')
verBrasierReady = effect("VerBrasier Préparé","verBrasierReady",emoji="<:verBrasier:946042912511250522>",turnInit=5)
extraVerVent = skill("Extra VerVent","sss",TYPE_DAMAGE,power=60,area=AREA_CIRCLE_1,use=MAGIE,effectOnSelf=extraVerFoudreReady,emoji='<:extraVerVent:946042871176396871>',rejectEffect=[extraVerFoudreReady,verBrasierReady])
extraVerFoudre = skill("Extra VerFoudre","sss",TYPE_DAMAGE,power=65,area=AREA_CIRCLE_1,use=MAGIE,needEffect=extraVerFoudreReady,effectOnSelf=verBrasierReady,emoji='<:extraVerFoudre:946042839287091300>')
verBrasier = skill("VerBrasier",'sss',TYPE_DAMAGE,power=100,area=AREA_CIRCLE_1,emoji='<:verBrasier:946042912511250522>',cooldown=3,use=MAGIE,needEffect=verBrasierReady)
comboVerBrasier = skill("Combo VerBrasier",'sss',TYPE_DAMAGE,500,power=verBrasier.power,emoji=verBrasier.emoji,become=[extraVerVent,extraVerFoudre,verBrasier],use=MAGIE,description="Permet d'effectuer l'enchaînement __Extra VerVent__, __Extra VerFoudre__ et __Ver Miracle__.\nLes compétences doivent être utilisée dans l'odre précédament énoncé")
phoenixFlight = effect("Vol du phénix","phoenixFlight",MAGIE,power=25,turnInit=3,stackable=True,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji='<:phenixFlight:1066023587305234484>',description="Soigne le porteur en début de tour")
galvanisation = skill("Galvanisation",'ssr',TYPE_DAMAGE,750,emoji='<:galvaPheonix:946042576413290506>',area=AREA_CIRCLE_1,power=120,use=MAGIE,effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_CIRCLE_2,phoenixFlight],cooldown=7,description="Inflige des dégâts aux ennemis ciblés et donne un effet régénérant aux alliés autour de vous\n\n{0} __{1}__ :\nSoigne le porteur avec une puissance de **{2}** en utilisant la statistique de magie pendant 3 tours".format(phoenixFlight.emoji[0][0],phoenixFlight.name,phoenixFlight.power))
contreDeSixte = skill("Contre de Sixte",'ssq',TYPE_DAMAGE,350,75,area=AREA_CIRCLE_1,cooldown=3,emoji='<:contreDeSixte:946042932643913788>')
selenShield = effect("Armure sélènomantique","selenArmor",INTELLIGENCE,overhealth=40,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
selenomancie = skill("Sélènomancie","ssp",TYPE_ARMOR,500,range=AREA_MONO,area=AREA_CIRCLE_2,effects=selenShield,cooldown=5,condition=[EXCLUSIVE,ASPIRATION,PROTECTEUR],use=INTELLIGENCE,emoji='<:selenomancie:949888629721927730>')
helioRegen = effect("Régénération hélomancique","helioRegen",CHARISMA,power=25,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN)
holiomancie = skill("Héliomancie",'sso',TYPE_INDIRECT_HEAL,500,effects=helioRegen,use=CHARISMA,area=AREA_CIRCLE_2,range=AREA_MONO,cooldown=5,condition=[EXCLUSIVE,ASPIRATION,VIGILANT],emoji='<:heliomancie:949888728116133889>')
partnerIn = effect("Position raprochée","partE",turnInit=-1,unclearable=True,description="En rélisant une compétence de Boost utilisable uniquement sur soi même, la zone d'effet de cette compétence est répliquée sur le porteur de <:partB:949074187513905172> __Partenaire de Position Rapprochée__.\n\nLes alliés se trouvant uniquement dans cette deuxième air d'effet bénificie du bonus de la compétence avec des bonus équivalants à **{0} %** de l'effet de base",power=35,emoji='<:partA:949074204333047809>')
partnerOut = effect("Partenaire de position rapprochée","partS",turnInit=-1,unclearable=True,description="Tant que le porteur est en état de se battre, permet d'étendre les zones d'effets de certaines compétences de l'entité à l'origine de cet effet",emoji='<:partB:949074187513905172>')
partner = skill("Position Raprochée","ssn",TYPE_PASSIVE,750,effectOnSelf=partnerIn,effects=partnerOut,emoji='<:partnaire:949075450360123482>',description="Vous confère l'effet {0} __{1}__ et donne l'effet {2} __{3}__ à un autre allié aléatoire au début du combat".format(partnerIn.emoji[0][0],partnerIn.name,partnerOut.emoji[0][0],partnerOut.name),quickDesc="Etend la porté de vos compétences de boost en les répliquants sur un allié")
exhibitionnisme = skill("Exhibitionnisme","ssm",TYPE_MALUS,69,range=AREA_MONO,area=AREA_CIRCLE_5,cooldown=7,effects=unHolly.effects[0],group=SKILL_GROUP_DEMON,use=CHARISMA,hpCost=20,emoji='<:exhibitionnisme:949893142402990120>',effPowerPurcent=80)
invocTitania = skill("Invocation - Titania","ssl",TYPE_SUMMON,750,invocation="Titania",ultimate=True,cooldown=10,emoji='<:smnTitania:950210129276579871>',shareCooldown=True,url='https://cdn.discordapp.com/attachments/927195778517184534/932704180731265054/20220117_193200.gif')
demonBloodEff = effect("Sang de Démon","demonBloodEff",CHARISMA,strength=12,magie=12,endurance=5,turnInit=3)
dmonBlood = skill("Sang de Démon","ssk",TYPE_BOOST,500,emoji='<:dmonBlood:950256044322459649>',range=AREA_MONO,area=AREA_CIRCLE_4,effects=demonBloodEff,hpCost=20,cooldown=7,group=SKILL_GROUP_DEMON,description="Augmente la Force, la Magie et l'Endurance des alliés affectés pendant 3 tours")
hollyGroundEff = copy.deepcopy(defenseUp)
hollyGroundEff.power, hollyGroundEff.stat, hollyGroundEff.turnInit = 10, INTELLIGENCE, 2
hollyGround = skill("Terre Sacrée I","ssj",TYPE_BOOST,750,emoji='<:holyGroundI:950254446611431455>',range=AREA_MONO,area=AREA_CIRCLE_2,effects=hollyGroundEff,cooldown=7,maxHpCost=25,group=SKILL_GROUP_HOLY,description="Réduit les dégâts subis par les alliés aux alentours au prix de 25% des PV max")
hollyGround2Eff = effect("Terre Sacrée II","hollyGroundIIEff",stat=CHARISMA,charisma=10,intelligence=10,precision=5,turnInit=3)
hollyGround2 = skill("Terre Sacrée Étendue","ssi",TYPE_BOOST,750,emoji='<:holyGroundII:950254462449115136>',range=AREA_MONO,area=AREA_CIRCLE_4,effects=hollyGround2Eff,cooldown=7,group=SKILL_GROUP_HOLY,description="Augmente le Charisme, l'Intelligence et la Précision des alliés dans la zone d'effet au prix de 15% des PV max",maxHpCost=15)
burningGroundEff = copy.deepcopy(dmgUp)
burningGroundEff.power, burningGroundEff.stat, burningGroundEff.turnInit = 10, INTELLIGENCE, 2
burningGround = skill("Terre Brûlée","ssh",TYPE_BOOST,750,emoji='<:burningGround:950256060923535370>',range=AREA_MONO,area=AREA_CIRCLE_2,effects=burningGroundEff,cooldown=7,hpCost=40,group=SKILL_GROUP_DEMON,description="Augmente les dégâts infligés par les alliés à portée au prix de 40% des PV actuels")
blueShell = skill("Carapace à épines","ssg",TYPE_DAMAGE,500,85,AREA_CIRCLE_7,area=AREA_CIRCLE_1,setAoEDamage=True,emoji='<:blue:950231849337233448>',cooldown=7,description="Inflige de dégâts en zone sur l'ennemi ayant réalisé le plus de dégâts")
preciChiEff = effect("Précision Chirurgicale","preciChiru",None,emoji=sameSpeciesEmoji('<:preciChiru:951692831230140437>','<:preciChiruR:951692959131267073>'),turnInit=-1,unclearable=True,reject=["ironHealth"],description="Augmente de **{0}%** la valeur des Soins ou Armures Critiques réalisés",power=10)
preciChi = skill("Précision Chirurgicale","ssf",TYPE_PASSIVE,500,effectOnSelf=preciChiEff,emoji='<:preciChiru:951692831230140437>',quickDesc="Augmente les soins et armures critiques octryés")
ironHealthEff = effect("Santé de Fer","ironHealth",turnInit=-1,unclearable=True,emoji='<:ironHealth:951692715727409253>',reject=[preciChiEff.id],description="Augmente de **{0}%** la valeur des Soins ou Armures Critiques réalisés par autruis sur vous",power=10)
ironHealth = skill("Santé de Fer","sse",TYPE_PASSIVE,500,effectOnSelf=ironHealthEff,emoji='<:ironHealth:951692715727409253>',quickDesc="Augmente les soins et armures critiques reçus")
windBurn = effect("Morsure du vent","windBurn",AGILITY,power=30,turnInit=5,lvl=5,stackable=True,area=AREA_DONUT_1,emoji='<:windBite:961185646993637476>',trigger=TRIGGER_END_OF_TURN,description="Inflige des dégâts magiques aux ennemis aux corps à corps du porteur à la fin du tour de celui-ci",type=TYPE_INDIRECT_DAMAGE)
windBal = skill("Balleyage éventé",'ssd',TYPE_DAMAGE,500,85,range=AREA_CIRCLE_1,use=AGILITY,emoji='<:windBite:961185646993637476>',cooldown=7,effectAroundCaster=[TYPE_DAMAGE,AREA_CIRCLE_1,50],effectOnSelf=windBurn,description="Inflige des dégâts à l'ennemi ciblé, puis aux ennemis à votre corps à coprs tout en vous octroyant un effet infligeant passivement des dégâts aux ennemis à votre corps à corps",condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR])
brasier2Eff = effect("Brûlure","brasier2Eff",MAGIE,power=25,turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE)
brasier2 = skill("Brasier Avancé","ssc",TYPE_DAMAGE,500,75,range=AREA_DIST_5,area=AREA_CIRCLE_2,use=MAGIE,emoji='<:brasier3:961185593482682398>',effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_CIRCLE_2,brasier2Eff],setAoEDamage=True,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],cooldown=5,ultimate=True,description="Inflige des dégâts aux ennemis dans la zone d'effet toute en infligeant un effet de dégâts sur la durée aux ennemis proche de vous\n__Puissance (Brûlure) :__ **{0}** ({1} tours)".format(brasier2Eff.power, brasier2Eff.turnInit))
earthUlt2Shield = effect("Armure Tellurique","earthUlt2Shield",ENDURANCE,emoji='<:liuArmor:922292960886915103>',overhealth=80,turnInit=3,trigger=TRIGGER_DAMAGE,type=TYPE_DAMAGE,inkResistance=10)
earthUlt2Lanch = skill("Fureur Tellurique","ssb",TYPE_DAMAGE,750,150,emoji='<:furTellu:951700536732823622>',range=AREA_MONO,area=AREA_CIRCLE_1,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],use=ENDURANCE,setAoEDamage=True,effectOnSelf=earthUlt2Shield,description="Inflige des dégâts aux ennemis à votre corps à corps et vous octrois une armure réduisant également les dégâts indirects reçus",ultimate=True,cooldown=7)
earthUlt2CastEff = effect("Cast - {0}".format(earthUlt2Lanch.name),"castEarthUlt2",turnInit=2,silent=True,replique=earthUlt2Lanch)
earthUlt2 = copy.deepcopy(earthUlt2Lanch)
earthUlt2.power, earthUlt2.effectOnSelf = 0, earthUlt2CastEff
geyser = skill("Geyser","ssa",TYPE_DAMAGE,500,75,area=AREA_CIRCLE_1,emoji='<:geyser:961185615859290163>',cooldown=5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],use=MAGIE)
rouletteEff = effect("Pile ou Face","pileouface",dmgUp = -50, critDmgUp= 100,turnInit=2,description="Augmente vos dégâts critiques infligés de **100%**, mais réduit vos dégâts non critiques de **50%**")
rouletteSkill = skill("Pile ou face","srz",TYPE_BOOST,350,range=AREA_MONO,cooldown=5,effects=rouletteEff,description="Lors de votre prochain tour, les dégâts critiques sont doublés, mais réduits de moitié sinon",emoji='<a:rotativeYPositiveCoin:917927342918221865>')
constEffI = effect("Constance","const1Eff",dmgUp=5,emoji=sameSpeciesEmoji('<:cst:951692626506178620>','<:ctsR:951692410155569172>'),critDmgUp=-15,turnInit=-1,unclearable=True,description="Augmente vos dégâts non critiques de **5%** mais réduit vos dégâts critiques de **15%**")
constEffII = effect("Constance Critique","const2Eff",emoji=sameSpeciesEmoji('<:cstCrit:951692598182027314>','<:cstCritR:951692193045835816>'),dmgUp=-10,critDmgUp=5,turnInit=-1,unclearable=True,description="Augmente vos dégâts critiques de **5%** mais réduit vos dégâts non critiques de **10%**")
constance = skill("Constance","sry",TYPE_PASSIVE,500,emoji='<:cst:951692626506178620>',effectOnSelf=constEffI,use=None,description="Augmente vos dégâts non critique au dépriment de vos dégâts critiques",quickDesc="Augmente vos dégâts non critiques au dépriment vos dégâts critiques")
constance2 = skill("Constance Critique","srx",TYPE_PASSIVE,500,effectOnSelf=constEffII,emoji='<:cstCrit:951692598182027314>',use=None,description="Augmente vos dégâts critiques au dépriment de vos dégâts non critiques",quickDesc="Augmente vos dégâts critiques au dépriment vos dégâts non critiques")
revelEff = copy.deepcopy(defenseUp)
revelEff.power, revelEff.stat, revelEff.turnInit = divination.effects[0].power, INTELLIGENCE, 3
revelation = skill("Révélation","srw",TYPE_BOOST,divination.price,effects=revelEff,cooldown=divination.cooldown,emoji=divination.emoji,range=AREA_MONO,area=AREA_CIRCLE_2)
elemEff = effect("Energie multiélémentaire","elemEff",None,turnInit=4,stackable=True,description="Cet effet devient un effet élémentaire correspondant à votre élément, augmentant de **{0}%** la puissance de vos compétences exclusives à votre élément\nCertaines compétences peuvent consommer les effets élémentaires pour obtenir des propriétés supplémentaires",power=5,emoji=elemEmojis[ELEMENT_UNIVERSALIS_PREMO])
elemEffName = ["Neutralité","Flamme intérieur","Courrant interne","Tempête intérieur","Minéralisation","Lueur interne","Ombre interne","Poussière cosmique","Seconde temporelle","Illuminae"]
mEP = 35
matriseElemEff = effect("Maîtrise élémentaire","maitriseElemPas",None,turnInit=-1,unclearable=True,description="Vous octroit **{0}%** de chance d'obtenir l'effet {1} __{2}__ lorsque vous utilisez une compétence élémentaire".format(mEP,elemEff.emoji[0][0],elemEff.name),emoji='<:catDefault:956599837128802324>',callOnTrigger=elemEff)
maitriseElementaire = skill("Maîtrise élémentaire","srv",TYPE_PASSIVE,effectOnSelf=matriseElemEff,emoji='<:catDefault:956599837128802324>',price=500,quickDesc="Vous octrois une chance d'obtenir un effet élémentaire en utilisant une compétence élémentaire")
magicEffGiver = skill("Concentration élémentaire","sru",TYPE_DAMAGE,500,100,effectOnSelf=elemEff,emoji='<:elemStrike:953217204629950484>',description="Inflige des dégâts à l'ennemi ciblé et vous octroit l'effet élémentaire correspondant à votre élément",cooldown=5,use=MAGIE)
physEffGiver = skill("Convertion élémentaire","srt",TYPE_DAMAGE,500,100,effectOnSelf=elemEff,emoji='<:elemSpell:953217184795078697>',description="Inflige des dégâts à l'ennemi ciblé et vous octroit l'effet élémentaire correspondant à votre élément",cooldown=5)

danceFas = skill("Danse de la Lame Fascinatoire","srs",TYPE_DAMAGE,power=125,area=AREA_CIRCLE_2,range=AREA_MONO,use=HARMONIE,cooldown=5,emoji=swordDance.emoji)
danseFasReady = effect("Cast - Danse de la Lame Fascinatoire","danseFasReady",turnInit=2,description="Vous permet d'utiliser la compétence {0} __Danse de la Lame Fascinatoire__".format(swordDance.emoji),emoji=swordDance.emoji,replique=danceFas)
eventFas = effect("Eventail Fascinatoire","evFac",turnInit=-1,unclearable=True,emoji='<:evFas:951824800488230932>',description="L'Eventail Fascinatoir se remplie lorsqu'un allié réalise un coup critique (+ 10 pts)",callOnTrigger=danseFasReady)
eventFas.jaugeValue = jaugeValue(
    emoji=[["<:lej:980923743960461412>","<:mej:980923762016927764>","<:rej:980923786650075228>"],["<:lfj:980923958587191356>","<:mrj:980923874927575120>","<:rfj:980923857642856589>"]],
    conds=[jaugeConds(INC_ON_ALLY_CRIT,10)]
)

fascination = skill("Fascination","srs",TYPE_PASSIVE,price=750,emoji='<:evFas:951824800488230932>',effectOnSelf=eventFas,use=HARMONIE,description="Lorsque vous-même ou votre équipe ont réalisés suffisament de coup critique, vous permet d'effectuer une puissante attaque autour de vous")
corGraEff = effect("Chorégraphie Grâcieuse","chorGra",CHARISMA,charisma=7,intelligence=7,endurance=7,emoji=sameSpeciesEmoji('<:graceB:956700633531043933>','<:graceR:956700653785346149>'),description="Augmente les statistiques de support du porteur")
corGraFinal = skill("Chorégraphie Grâcieuse","corGraceFinal",TYPE_BOOST,500,range=AREA_MONO,area=aliceDanceFinal.area,effects=corGraEff,cooldown=aliceDance.cooldown,emoji='<:corGra:956700501095899217>',description="Augmente les statistiques de support de vos alliés proches durant 3 tours",effPowerPurcent=125)
corGraGuideEff = effect(corGraFinal.name,"corGraGuideEff",turnInit=2,silent=True,emoji=corGraFinal.emoji,replique=corGraFinal)
corGraGuide = copy.deepcopy(corGraFinal)
corGraGuide.effectOnSelf, corGraGuide.id, corGraGuide.effPowerPurcent, corGraGuide.area = corGraGuideEff, "srq", 110, aliceDanceGuide1.area
corGraGuideEff2 = copy.deepcopy(corGraGuideEff)
corGraGuideEff2.replica = corGraGuide
corGraCast = copy.deepcopy(corGraGuide)
corGraCast.effectOnSelf, corGraCast.effPowerPurcent = corGraGuideEff2, 100
rosePink = effect("Rose rose","finFloRose",turnInit=-1,emoji='<:roseRose:956716583915491378>',stackable=True)
roseBlue = effect("Rose azurée","finFloBlu",turnInit=-1,emoji='<:roseBlue:956716604333367326>',stackable=True)
roseGreen = effect("Rose verte","finFloGre",turnInit=-1,emoji='<:roseGreen:956716536742150254>',stackable=True)
roseRed = effect("Rose rouge","finFloRed",turnInit=-1,emoji='<:roseRed:956716516232032257>',stackable=True)
roseYellow = effect("Rose jaune","finFloYel",turnInit=-1,emoji='<:roseYellow:956716561136242748>',stackable=True)
roseDarkBlu = effect("Rose bleue","finFloDBlue",turnInit=-1,emoji='<:roseDBlue:956725613585133598>',stackable=True)
finFloLaunchBase = skill("Final Floral","finFlo",TYPE_BOOST,use=CHARISMA,emoji='<:finFlor:956715059772538981>',range=AREA_MONO,area=AREA_CIRCLE_4)
finFloCast = effect("Cast - Final Floral","castFinFlo",turnInit=2,emoji=finFloLaunchBase.emoji,replique=finFloLaunchBase)
finFloEff = effect("Final Floral","finFloEffPas",turnInit=-1,unclearable=True,emoji=sameSpeciesEmoji('<:finalFloralB:956715210549362748>','<:finalFloralR:956715234842791937>'),description="Vous avez la compétence <:finFlor:956715059772538981> __Final Floral__ d'équipé")

finFloEffList = [copy.deepcopy(dmgUp),copy.deepcopy(defenseUp),effect("Critique Floral",'finFloCrit',CHARISMA,critical=7,emoji=finFloEff.emoji),effect("Aura Florale","finFloHeal",CHARISMA,power=20,turnInit=3,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji=finFloEff.emoji,area=AREA_CIRCLE_2)]
finFloEffList[0].power, finFloEffList[1].power, finFloEffList[0].stat, finFloEffList[1].stat = 7, 7, CHARISMA, CHARISMA
divineSave = skill("Salut Divin","srp",TYPE_RESURECTION,500,300,group=SKILL_GROUP_HOLY,maxHpCost=25,cooldown=5,shareCooldown=True,use=CHARISMA, emoji='<:hollyRaise:958065170645655642>')
redemption = skill("Rédemption","sro",TYPE_DAMAGE,500,150,area=AREA_CIRCLE_1,maxHpCost=15,group=SKILL_GROUP_HOLY,ultimate=True,cooldown=5,use=MAGIE,emoji='<:rdemption:958065152098455673>')
tablElemEff = []
for cmpt in range(len(elemNames)):
    temp = copy.deepcopy(elemEff)
    temp.emoji, temp.name, temp.description, temp.id = uniqueEmoji(elemEmojis[cmpt]), elemEffName[cmpt], "Augmente de **{0}%** la puissance de vos compétences exclusives à l'élément **{1}**\n\nCertaines compétences peuvent consommer cet effet pour obtenir des propriétés supplémentaires".format(temp.power,elemNames[cmpt]), temp.id + str(cmpt)
    tablElemEff.append(temp)

fireElemUse = skill("Brasier Infernal","srn",TYPE_DAMAGE,500,120,setAoEDamage=True,range=AREA_MONO,area=AREA_DIST_5,ultimate=True,cooldown=7,use=MAGIE,emoji='<:catFire:956599672737243166>',description="Consomme vos effets {0} __{1}__\nInflige des dégâts aux ennemis éloignés de vous\nSi au moins un {0} __{1}__ a été consommé, donne également un effet de dégâts indirects aux ennemis infligeants **33%** de dégâts supplémentaires à la fin de leur tour dont la durée dépend du nombre d'effets consommés".format(tablElemEff[1].emoji[0][0],tablElemEff[1].name),condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE])
waterElemUse = skill("Pluie Glacée","srm",TYPE_DAMAGE,500,135,ultimate=True,cooldown=7,use=MAGIE,emoji='<:catWater:956599696594444418>',description="Consomme vos effets {0} __{1}__\nInflige des dégâts à l'ennemi ciblé.\nPour chaque effet {0} __{1}__ consommé, réalise une nouvelle attaque infligeant **15%** de dégâts supplémentaires".format(tablElemEff[2].emoji[0][0],tablElemEff[2].name),condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER])
airElemUse = skill("Tempête Jupiterrienne","srl",TYPE_DAMAGE,500,120,knockback=3,setAoEDamage=True,range=AREA_MONO,area=AREA_CIRCLE_2,ultimate=True,cooldown=7,use=MAGIE,emoji='<:catAir:956599718522265610>',description="Consomme vos effets {0} __{1}__\nInflige des dégâts aux ennemis autour de vous\nSi au moins un effet {0} __{1}__ a été consommé, vous octrois un effet infligeant des dégâts indirects aux ennemis autour de vous à la fin de votre tour dont la durée dépend du nombre d'effets consommés".format(tablElemEff[3].emoji[0][0],tablElemEff[3].name),condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR])
earthElemUse = skill("Déchirure Tectonique","srk",TYPE_DAMAGE,500,135,ultimate=True,cooldown=7,use=MAGIE,emoji='<:catEarth:956599751002963998>',description="Consomme vos effets {0} __{1}__\nInflige des dégâts à l'ennemi ciblé.\nSi au moins un effet {0} __{1}__ a été consommé, réalise une nouvelle attaque infligeant **20%** de dégâts supplémentaires sur les ennemis autour de vous. La puissance de l'attaque est multipliée par le nombre d'effets consommés".format(tablElemEff[4].emoji[0][0],tablElemEff[4].name),condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH])
lightElemUseEff = effect("Armure de lumière","lightArmorElemUse",INTELLIGENCE,overhealth=75,turnInit=3,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR)
lightElemUse = skill("Lumière Protectrice","srj",TYPE_ARMOR,500,range=AREA_MONO,area=AREA_CIRCLE_3,effects=lightElemUseEff,cooldown=7,ultimate=True,emoji='<:catLight:956599774461722655>',description="Consomme vos effets {0} __{1}__\nDonne une armure à vous et vos alliés alentours.\nSi au moins un effet {0} __{1}__ a été consommé, octroie un effet de soins sur la durée avec une puissance de **30%** de celle de l'armure. La durée de l'effet dépend du nombre d'effets consommés".format(tablElemEff[5].emoji[0][0],tablElemEff[5].name),condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],use=INTELLIGENCE)
darkElemUse = skill("Brasier des Ténèbres","sri",TYPE_DAMAGE,500,135,area=AREA_CIRCLE_2,ultimate=True,cooldown=7,use=MAGIE,emoji='<:catDark:950942244523872256>',description="Consomme vos effets {0} __{1}__\nInflige des dégâts aux ennemis dans la zone d'effet\nSi au moins un {0} __{1}__ a été consommé, donne également un effet de dégâts indirects à l'ennemi ciblé infligeant **50%** de dégâts supplémentaires à la fin de son tour à lui et ses alliés proches dont la durée dépend du nombre d'effets consommés".format(tablElemEff[6].emoji[0][0],tablElemEff[6].name),condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS])
spaceElemUse = skill("Déluge Céleste","srh",TYPE_DAMAGE,500,135,area=AREA_CIRCLE_2,ultimate=True,cooldown=7,use=MAGIE,emoji='<:catSpace:956599795110277150>',description="Consomme vos effets {0} __{1}__\nInflige des dégâts aux ennemis dans la zone d'effet\nPour chaque effet {0} __{1}__ consommé, inflige des dégâts supplémentaires équivalents à **33%** des dégâts de base à un ennemi aléatoire dans la zone d'effet et ses alliés aux corps à corps".format(tablElemEff[7].emoji[0][0],tablElemEff[7].name),condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE])
timeElemUse = skill("Déphasage Temporel","srg",TYPE_HEAL,500,100,area=AREA_CIRCLE_2,ultimate=True,cooldown=7,use=CHARISMA,emoji='<:catTime:956599814898999328>',description="Consomme vos effets {0} __{1}__\nSoigne les alliés dans la zone d'effet.\nSi au moins un effet {0} __{1}__ a été consommé, octroi également une armure aux alliés dans la zone d'effet dont la puissance équivant à **20%** de celle des soins. La puissance est multipliée par le nombre d'effets consommés".format(tablElemEff[8].emoji[0][0],tablElemEff[8].name),condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME])
bleedingConvert = skill("Taillade des veines","srf",TYPE_DAMAGE,500,80,useActionStats=ACT_INDIRECT,range=AREA_CIRCLE_3,cooldown=7,lifeSteal=50,emoji="<:shiLifeSteal:960007047984857148>",percing=50,description="Inflige des dégâts à la cible et vole une partie des dégâts infligés tout en ignorant une partie de la résistance de la cible\nConsomme tous les effets <:ble:887743186095730708> __Hémorragie__ présents sur la cible pour augmenter la puissance de cette compétence")

elemShieldEff = effect("Armure élémentaire","elemShield",INTELLIGENCE,overhealth=40,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,description="Une armure qui protège de quelques dégâts direct.",emoji=sameSpeciesEmoji('<:elemShield:960061614739050537>','<:elemShield:960061540164313088>'))
elemShield = skill("Armure élémentaire","srd",TYPE_ARMOR,500,effects=[elemShieldEff,elemEff],cooldown=7,emoji='<:elemShield:960061614739050537>',description="Octroi une armure à l'allié ciblé ainsi qu'un effet élementaire de son élément")
shieldAuraShield = effect("Armure","armorAuraArmor",INTELLIGENCE,overhealth=20,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,description="Protège de quelques dégâts directs")
shieldAuraEff = effect("Aura armurière","shieldAuraEff",INTELLIGENCE,callOnTrigger=shieldAuraShield,emoji=sameSpeciesEmoji('<:armorAura:960060538119929927>','<:armorAura:960060634517602344>'),lvl=3,area=AREA_CIRCLE_2,trigger=TRIGGER_END_OF_TURN,turnInit=3,description="À la fin du tour du porteur, ocrtoi une armure à celui-ci et ses alliés aux alentours")
shieldAura = skill("Aura Armurière","src",TYPE_ARMOR,500,cooldown=7,effects=shieldAuraEff,emoji='<:armorAura:960060538119929927>',description="Pose une aura sur l'allié ciblé, qui octroira de l'armure autour de lui quand il terminera son tour pendant 3 tours")
horoscope = skill("Horoscope","srb",TYPE_BOOST,emoji='<:horoscope:960312586371477524>',description="Consomme tous vos signes astrologiques pour augmenter les statistiques de vos alliés durant 3 tours\nLes statistiques augmentées dépendent des signes astrologiques conssommés\nVous obtenez un signe astrologique aléatoire en fin de tour",cooldown=3,initCooldown=3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE],use=INTELLIGENCE,range=AREA_MONO, area=AREA_CIRCLE_5)
ShiHemophilie = effect("Anti-Coagulant","increaseBlooding",description="Augmente de **{0}%** les dégâts subis par l'effet <:ble:887743186095730708> __Hémorragie__",power=35,emoji='<:hemophillie:960721463772610613>')
ShiUltimateLauch = skill("Percée ensanglantée","sra",TYPE_DAMAGE,750,175,AREA_CIRCLE_2,effects=["mx",ShiHemophilie],useActionStats=ACT_INDIRECT,emoji='<:shiUlt:960760921666510908>',description="Après 1 tour de chargement, inflige de lourd dégâts à l'ennemi ciblé, lui applique <:ble:887743186095730708> __Hémorragie__ et augmente les dégâts de <:ble:887743186095730708> __Hémorragie__ durant 1 tour",ultimate=True,cooldown=7)
ShiUltimateCast = effect("Cast - {0}".format(ShiUltimateLauch.name),"shiUltCast",turnInit=2,silent=True,replique=ShiUltimateLauch,emoji='<a:shiUltCast:960764930217377802>')
ShiUltimate = copy.deepcopy(ShiUltimateLauch)
ShiUltimate.effects, ShiUltimate.power, ShiUltimate.effectOnSelf = [None], 0, ShiUltimateCast

intaveneuse = skill("Intraveineuse",'sqz',TYPE_INDIRECT_DAMAGE,500,effects="me",effPowerPurcent=150,cooldown=5,emoji='<:intraveineuse:963390544770367488>',use=MAGIE)
decolation = skill("Colation","sqy",TYPE_DAMAGE,effects=ShiUltimateLauch.effects,useActionStats=ACT_INDIRECT,effPowerPurcent=60,cooldown=5,power=40,lifeSteal=100,emoji='<:collation:963390564655579156>',price=500)
dephaIncantEff = effect("Déphasage Incantatoire","dephaIncant",MAGIE,power=80,area=AREA_CIRCLE_1,trigger=TRIGGER_ON_REMOVE,emoji='<:dephaInc:980450895785521242>',type=TYPE_INDIRECT_DAMAGE,description="Inflige des dégâts lors du début du prochain tour de l'entité à l'origine de l'effet")
dephaIncant = skill("Déphasage incantatoire","sqx",TYPE_INDIRECT_DAMAGE,500,effects=dephaIncantEff,cooldown=5,emoji='<:dephaInc:980450895785521242>',description="Place l'effet {effIcon} __{effName}__ sur la cible. Au début de votre prochain tour, l'effet explosera en blessant le porteur et ses alliés proches",condition=[EXCLUSIVE,ASPIRATION,SORCELER])

coroWind = effect("Corruptus sanguis","coroWind",MAGIE,power=45,turnInit=3,stackable=True,lvl=3,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji='<:corruptusSanguis:1050065948599660595>',description="Un vent empoisonné qui fait des dégâts à la fin du tour du porteur.\nPossède une légère odeur de sang")
bloodJauge = effect("Jauge de Sang","bloodJauge",turnInit=-1,unclearable=True,emoji='<:bloodJauge:1050111058314018936>')
bloodJauge.jaugeValue = jaugeValue(
    emoji = [["<:BJLeftEmpty:900473865459875911>","<:BJMidEmpty:900473889539366994>","<:BJRightEmpty:900473909856587847>"],["<:BJLeftFull:900473987564441651>","<:BJMidFull:900474021781569604>","<:BJRightFull:900474036042215515>"]],
    conds = [
        jaugeConds(INC_START_TURN,2),
        jaugeConds(INC_DEAL_DAMAGE,10/100),
        jaugeConds(INC_ENEMY_DAMAGED,10/100),
        jaugeConds(INC_ALLY_DAMAGED,5/100)
    ]
)

cwFocus = skill("Incarnatus Puff","sqw",TYPE_INDIRECT_DAMAGE,500,cooldown=focal.cooldown-2,effects=coroWind,effPowerPurcent=350,effectOnSelf=coroWind,description="Donne un puissant effet {effIcon} __{effName}__  à l'ennemi ciblé, mais en subissez un également",emoji='<:IncPuf:968327189508542484>',jaugeEff=bloodJauge,minJaugeValue=20,maxJaugeValue=35)
propaUltLaunch = skill("Propagation Avancée","sqv",TYPE_INDIRECT_DAMAGE,750,range=AREA_MONO,emoji='<:probagUlt:1058851761680551987>',area=AREA_ALL_ENEMIES,ultimate=True,cooldown=7,effects="me",effPowerPurcent=85,description="Après un tour de chargement, inflige <:est:884223390804766740> __Poison d'Estialba__ à tous les ennemis avec **35%** de sa puissance",use=MAGIE)
propaUltCastEff = effect("Cast - {replicaName}","propaUltCastEff",turnInit=2,silent=True,replique=propaUltLaunch,emoji='<a:propagUltCast:1058849678470434828>')
propaUlt = copy.deepcopy(propaUltLaunch)
propaUlt.effects, propaUlt.effectOnSelf, propaUlt.description = [None], propaUltCastEff, None
cwUlt = skill("Ultima Exitium","squ",TYPE_INDIRECT_DAMAGE,750,ultimate=True,cooldown=5,effects=coroWind,power=25,effPowerPurcent=150,description="Inflige l'effet {effIcon} __{effName}__ à la cible, puis inflige immédiatement des dégâts indirects en fonction du nombre d'effets de Dégâts Indirects ainsi que leur durée restante présents sur la cible\nLes effets autres que {effIcon} __{effName}__ augmentent un peu plus la puissance de l'attaque mais sont consommés par cette dernière",jaugeEff=bloodJauge,minJaugeValue=25,maxJaugeValue=50,maxPower=50)
sanguisGladio = skill("Sanguis Gladio","sqt",TYPE_DAMAGE,500,80,cooldown=3,effects=coroWind,effPowerPurcent=125,use=MAGIE,emoji='<:sgladio:968478994724950056>',jaugeEff=bloodJauge,minJaugeValue=15,maxJaugeValue=25,maxPower=110)
sanguisGladio2 = skill("Sanguis Gladio Avancée","sqs",TYPE_DAMAGE,750,100,cooldown=5,area=AREA_LINE_2,effects=coroWind,effPowerPurcent=110,use=MAGIE,emoji='<:sgladio2:968479144293855252>',jaugeEff=bloodJauge,minJaugeValue=15,maxJaugeValue=25,maxPower=135)
cardiChoc = skill("Choc Cardinal","sqr",TYPE_DAMAGE,500,100,range=AREA_MONO,area=AREA_INLINE_3,accuracy=120,cooldown=5,description="Inflige des dégâts aux ennemis prochent allignés avec vous avec une précision importante",emoji='<:chocCardi:989536077117276250>')
equatorial = skill("Equatorial","sqq",TYPE_DAMAGE,500,50,range=AREA_MONO,area=AREA_LINE_6,accuracy=120,cooldown=7,setAoEDamage=True,description="Inflige des dégâts aux ennemis allignés avec vous avec une précision importante")
kralamSkillEff2 = effect("This is, my No No Square","nono",INTELLIGENCE,resistance=10,overhealth=55,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,turnInit=3)
kralamSkillEff1 = effect("No no, don't touch me there","squaez",trigger=TRIGGER_AFTER_DAMAGE,callOnTrigger=kralamSkillEff2,lvl=1,emoji=uniqueEmoji('<a:FranziskaNo:800833215106383883>'),type=TYPE_BOOST,resistance=5)
kralamSkill = skill("Prévention","vn",TYPE_BOOST,0,0,AREA_DONUT_6,cooldown=5,effects=kralamSkillEff1,emoji='<:egide:887743268337619005>')
krystalisationEff = effect("Cristalisé","krysArmor",ENDURANCE,overhealth=65,inkResistance=12.5,turnInit=3,emoji='<:cristalisation:989540878953619506>',type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
krystalisation = skill("Cristalisation","sqp",TYPE_ARMOR,500,range=AREA_MONO,effects=krystalisationEff,cooldown=7,emoji='<:cristalisation:989540878953619506>',description="Vous octrois une armure qui réduit également les dégâts indirects subis",condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH])
regenVigilEff = effect("Régénération vigilante","vigilRegen",CHARISMA,power=35,turnInit=5,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_END_OF_TURN)
regenVigil = skill("Régénération Vigilante","sqo",TYPE_HEAL,750,35,AREA_DONUT_4,[EXCLUSIVE,ASPIRATION,VIGILANT],cooldown=7,emoji='<:regenVigil:980450876265218109>',effects=regenVigilEff,effectOnSelf=regenVigilEff,description="Soigne l'allié ciblé et procure à ce dernier et vous même un effet de soin sur la durée")
fragmentation = skill("Fragmentation","sqn",TYPE_DAMAGE,500,90,AREA_CIRCLE_4,cooldown=5,damageOnArmor=3,emoji='<:fragmentation:1065854021979607051>',erosion=65,condition=[EXCLUSIVE,ASPIRATION,TETE_BRULE],description="Inflige des dégâts à l'ennemi ciblé avec un grand pourcentage de réduction des PvMax adverses ainsi qu'un multiplicateur de dégâts sur l'armure conséquant")
morsTempette = effect("Morsure de la Tempette","morsTempette",STRENGTH,power=30,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,stackable=True,turnInit=5,lvl=5,emoji='<:morsTemp:971788828278943776>')
morsCaudique = effect("Morsure Caudique","morsCaudique",INTELLIGENCE,power=30,trigger=TRIGGER_END_OF_TURN,stackable=True,type=TYPE_INDIRECT_DAMAGE,turnInit=5,lvl=5,emoji='<:morsCaudique:971788772289163274>')
machDeFer = skill("Mâchoire de Fer","sqm",TYPE_DAMAGE,500,condition=[EXCLUSIVE,ASPIRATION,ATTENTIF],power=80,useActionStats=ACT_INDIRECT,effects=[morsTempette,morsCaudique],cooldown=7,emoji='<:machFer:971787963795124235>')
lanceToxEff = effect("Toxine","toxi",STRENGTH,power=25,emoji='<:lanceTox:971789592145580103>',stackable=True,turnInit=5,lvl=5,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE)
lanceTox = skill("Lance-Toxine","sql",TYPE_INDIRECT_DAMAGE,500,area=AREA_CONE_3,effects=lanceToxEff,emoji='<:lanceTox:971789592145580103>',cooldown=5,condition=[EXCLUSIVE,ASPIRATION,ATTENTIF])
gigaFoudreEff = effect("Giga Foudre","gigaFoudre",MAGIE,power=20,emoji='<:gigaFoudre:971789611087036487>',stackable=True,turnInit=5,lvl=5,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN)
gigaFoudre = skill("Giga Foudre","sqk",TYPE_INDIRECT_DAMAGE,500,area=AREA_CIRCLE_1,effects=gigaFoudreEff,emoji='<:gigaFoudre:971789611087036487>',cooldown=5,condition=[EXCLUSIVE,ASPIRATION,SORCELER])
trickAttackEff = copy.deepcopy(vulne)
trickAttackEff.power = 10
trickAttack = skill("Attaque Sournoise","sqj",TYPE_DAMAGE,500,50,effects=trickAttackEff,cooldown=5,emoji='<:trickAttack:971788242284343336>',description="Inflige des dégâts à l'adversaire sublié puis augmente les dégâts qu'il reçoit de **10%** jusqu'à votre prochain tour")
aurore2Eff = effect("Aurore II","aur2Eff",type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,power=20,stat=CHARISMA,turnInit=3,emoji='<:aurore:971787846639841310>')
aurore2 = skill("Aurore II","sqh",TYPE_INDIRECT_HEAL,500,effects=aurore2Eff,cooldown=5,emoji='<:aurore:971787846639841310>',condition=[EXCLUSIVE,ASPIRATION,VIGILANT])
holyShieltronEff1 = effect("Sheltron Sacré","holyShieltron1",block=100,emoji='<:shieltron:971787905758560267>')
holyShieltronEff2 = effect("Bénédiction du Paladin","holyShieltron2",CHARISMA,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,power=20,turnInit=3,emoji='<:bene:1005850393747673171>')
holyShieltron = skill("Sheltron Sacré","sqg",TYPE_BOOST,500,range=AREA_MONO,effects=[holyShieltronEff2,holyShieltronEff1],emoji=holyShieltronEff1.emoji[0][0],condition=[EXCLUSIVE,ASPIRATION,VIGILANT],group=SKILL_GROUP_HOLY,maxHpCost=5,cooldown=5,description="Vous octroi 100% de blocage ainsi qu'une petite régénération sur la durée")
KeracholeRegen = effect("Kerachole","keracholeRegen",INTELLIGENCE,power=15,turnInit=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji='<:kerachole:971787391058722847>')
KeracholeReduc = copy.deepcopy(defenseUp)
KeracholeReduc.power, KeracholeReduc.stat, KeracholeReduc.turnInit = 3.5, INTELLIGENCE, 3
kerachole = skill("Kerachole","sqf",TYPE_BOOST,500,effects=[KeracholeReduc,KeracholeRegen],emoji='<:kerachole:971787391058722847>',cooldown=7,range=AREA_MONO,area=AREA_CIRCLE_2,description="Réduit les dégâts subis par vous et vos allié proches tout en vous octroyanr un effet de régénération sur la durée")
morsTempSkill = skill("Morsure de la Tempette","sqe",TYPE_DAMAGE,350,power=35,useActionStats=ACT_INDIRECT,effects=morsTempette,cooldown=5,condition=[EXCLUSIVE,ASPIRATION,ATTENTIF],emoji=morsTempette.emoji[0][0])
morsCaudiqueSkill = skill("Morsure Caudique","sqd",TYPE_DAMAGE,350,power=35,useActionStats=ACT_INDIRECT,effects=morsCaudique,cooldown=5,condition=[EXCLUSIVE,ASPIRATION,ATTENTIF],emoji=morsCaudique.emoji[0][0])
combEff = effect("Combustion","combustion",MAGIE,power=15,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_1,turnInit=-1,lvl=99,emoji='<:fireKitsune:917670925904785408>')
combustion = skill("Combustion","sqc",TYPE_PASSIVE,500,effectOnSelf=combEff,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],emoji='<:fireKitsune:917670925904785408>',description="À chaque de tour, inflige des dégâts aux ennemis à votre corps à corps",quickDesc="Permet d'infliger des dégâts indirects à tout ennemi au corps à corps à la fin de votre tour")
lbRdmBlind = effect("Aveuglement Vermeil","verBlind",type=TYPE_BOOST,power=35,emoji='<:MyEyes:784226383018328115>')
lbRdmLauch = skill("Fléau Vermeil","sqb",TYPE_DAMAGE,750,200,area=AREA_CIRCLE_2,use=MAGIE,ultimate=True,cooldown=7,emoji='<a:verBlind:974545990369574982>',effectAroundCaster=[TYPE_MALUS,AREA_ALL_ALLIES,lbRdmBlind],description="Après un tour de chargement, inflige de sérieux dégâts aux ennemis dans une large zone, mais réduit la précision de tous les alliés de {0}% pendant un tour".format(lbRdmBlind.power),url='https://media.discordapp.net/attachments/927195778517184534/932773655732158525/20220118_000607.gif')
lbRdmCaustEff = effect("Cast - {0}".format(lbRdmLauch.name),"lbRedMageCast",turnInit=2,silent=True,replique=lbRdmLauch)
lbRdmCast = copy.deepcopy(lbRdmLauch)
lbRdmCast.power, lbRdmCast.url, lbRdmCast.effectAroundCaster, lbRdmCast.effectOnSelf = 0, None, None, lbRdmCaustEff
lightEarthEff = copy.deepcopy(defenseUp)
lightEarthEff.power, lightEarthEff.stat = 7, INTELLIGENCE
lightEarth = skill("Coeur de Lumière","sqa",TYPE_BOOST,500,cooldown=7,range=AREA_MONO,area=AREA_CIRCLE_3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],effects=lightEarthEff,emoji='<:lumHeart:980451074429288478>')
darkAmbEff = copy.deepcopy(lightEarthEff)
darkAmbEff.stat = ENDURANCE
darkAmb = skill("Missionaire des Ténèbres","spz",TYPE_BOOST,500,area=AREA_CIRCLE_4,range=AREA_MONO,cooldown=7,effects=darkAmbEff,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS],emoji='<:missionaire:980451008901701633>')
solarEruption = skill("Eruption Solaire","spy",TYPE_DAMAGE,500,100,area=AREA_ARC_1,cooldown=5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE],use=MAGIE,emoji='<:erupStell:1083754013582971010>')
firstArmorEff, firstArmorEff2 = effect("Armure préliminaire","armurepreliminaire",INTELLIGENCE,overhealth=65,inkResistance=10,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji("<:prelimB:981607841070739506>","<:prelimR:981607818442473492>")), copy.deepcopy(absEff)
firstArmorEff2.power = 20
firstArmor = skill("Armure préliminaire","spx",TYPE_ARMOR,500,cooldown=7,effects=[firstArmorEff,firstArmorEff2],emoji='<:prelimB:981607841070739506>',description="Octroi une puissante armure à l'allié ciblé, réduisant également les dégâts indirects qu'il reçoit tant qu'elle est active, et augmente également les soins qu'il reçoit de 20%")
refLum = skill("Lueur réfléchissante","spv",TYPE_HEAL,500,50,area=AREA_CIRCLE_1,cooldown=5,effectOnSelf=tablElemEff[ELEMENT_LIGHT],condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],description="Soigne les alliés dans la zone d'effet et vous octroi un effet élémentaire")
refConc = skill("Lueur concentrique","spu",TYPE_HEAL,500,70,cooldown=5,effectOnSelf=tablElemEff[ELEMENT_LIGHT],condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],description="Soigne l'allié ciblé et vous octroi un effet élémentaire")

petalisEff = effect("Pétalisation","petalEff",CHARISMA,endurance=5,block=15,inkResistance=5,turnInit=5,description="Les statistiques défensives sont augmentées",emoji=sameSpeciesEmoji('<:petB:979448518345359451>','<:petR:979448539446911016>'))
petalisation = skill("Pétalisation","spt",TYPE_BOOST,500,effects=petalisEff,range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=5,emoji='<:petR:979448539446911016>',description="Augmente l'endurance et le blocage des alliés alentours durant 5 tours")
roseeHealEff = effect("Rosée matinale","roseedumatin",CHARISMA,agility=5,type=TYPE_BOOST,turnInit=3)
roseeHeal = skill("Rosée matinale","sps",TYPE_BOOST,500,range=AREA_MONO,area=AREA_CIRCLE_3,cooldown=3,effects=roseeHealEff,effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_2,35],description="Augmente l'esquive des alliés à portée tout en les soignants un peu")
floraisonFinalEff = copy.deepcopy(onstageeff) 
floraisonFinalEff = effect("Floraison finale","floraisonFinale",CHARISMA,int(onstageeff.strength*0.7),int(onstageeff.endurance*0.7),int(onstageeff.charisma*0.7),int(onstageeff.agility*0.7),int(onstageeff.precision*0.7),int(onstageeff.intelligence*0.7),int(onstageeff.magie*0.7),turnInit=onstageeff.turnInit+2,emoji=sameSpeciesEmoji('<:florFinB:979450403890548786>','<:florFinR:979450384244432896>'))
floraisonFinale = copy.deepcopy(onstage)
floraisonFinale.effects, floraisonFinale.name, floraisonFinale.id, floraisonFinale.emoji, floraisonFinale.cooldown, floraisonFinale.message, floraisonFinale.url = [floraisonFinalEff], "Floraison Finale", "spr", '<:florFinR:979450384244432896>', floraisonFinale.cooldown + 1, "{0} déclanche une floraison surprise", "https://media.discordapp.net/attachments/971788596401041480/979891716104540170/20220528_013916.gif"
INCREASEPOWERPURCENTBYELEMEFF = 20
elemArrowNames, elemArrowSkill, elemArrowId, elemArrowEmoji = ["neutre","emflammée","de glace", "aérienne", "tellurique", "de Lumière", "sombre", "dimentionnelle","temporelle"], [], ["spq","spp","spo","spn","spm","spl","spk","spj","spi"], ["<:neutralArrow:980172549264670730>","<:fireArrow:980172729531658332>","<:iceArrow:980172688284876830>","<:airArrow:980172706504908841>","<:earthArrow:980172665878896700>","<:lightArrow:980172606143606834>","<:darkArrow:980172639219888138>","<:spaceArrow:980172585235005440>","<:timeArrow:980172567048511519>"]
for cmpt in range(len(elemNames)-1):
    isMono = cmpt % 2 == 0
    if cmpt in [0,5,6,7,8]:
        skillRange = AREA_CIRCLE_5
    elif cmpt in [1,2]:
        skillRange = AREA_DIST_5
    else:
        skillRange = AREA_CIRCLE_3
    elemArrowSkill.append(skill("Flèche {0}".format(elemArrowNames[cmpt]),elemArrowId[cmpt],TYPE_DAMAGE,500,[65,80][isMono]+15*int(skillRange==AREA_CIRCLE_3)+10*int(skillRange==AREA_DIST_5),range=skillRange,area=[AREA_LINE_2,AREA_MONO][isMono],description="Inflige des dégâts {0} en consommants tous vos effets {1} __{2}__\nPour chaque effets consommés, la puissance de cette compétence augmente de **{3}**".format(["aux ennemis ciblés","à l'ennemi ciblé"][isMono],tablElemEff[cmpt].emoji[0][0],tablElemEff[cmpt].name,INCREASEPOWERPURCENTBYELEMEFF),cooldown=5,condition=[EXCLUSIVE,ELEMENT,cmpt], emoji=elemArrowEmoji[cmpt]))

finalFloral = skill("Final Floral","srr",TYPE_PASSIVE,750,effectOnSelf=finFloEff,emoji='<:finFlor:956715059772538981>',quickDesc="Permet d'utliser une compétence de boost dont l'effet dépend de vos autres compétences utilisées au préalable",description="En utilisant certaines compétences, vous obtiendrez une *Rose* :\n{0} __{1}__, {26} __{27}__ : {2} {3}\n{4} __{5}__, {28} __{29}__ : {6} {7}\n{8} __{9}__, {30} __{31}__ : {10} {11}\n{12} __{13}__ : {14} {15}\n\nVous pouvez aussi orbtenir une rose quand vos alliés utilisent certaines compétences :\n{16} __{17}__, {32} __{33}__ : {18} {19}\n{20} __{21}__, {34} __{35}__ : {22} {23}\n\nLorsque vous possédez trois effets *Rose*, vous vous mettrez à charger la compétence {24} __{25}__, dont l'effet dépend des *Roses* possédées :\n{2} __{3}__ : Augmente les dégâts infligés des alliés de **7%** (Charisme)\n{6} __{7}__ : Réduit les dégâts reçus des alliés de **5%** (Charisme)\n{10} __{11}__ : Augmente la durée des effets déclanchés par les autres *Roses* de **1 tour**\n{14} __{15}__ : Augmente la puissance des effets déclanchés par les autres *Roses* de **30%**\n{18} __{19}__ : Augmente le taux de coup critique des alliés de **7%** (Charisme)\n{22} __{23}__ : Vous procure une aura qui soigne les alliés autour de vous en fin de tour pendant **3 tours** (Charisme)\n\nVous ne pouvez cummuler que **3** *Roses* à la fois, et avoir une *Rose* en doublon n'augmente pas les effets associés".format(
    aliceDance.emoji,aliceDance.name,
    roseRed.emoji[0][0], roseRed.name,
    corGraFinal.emoji,corGraFinal.name,
    roseDarkBlu.emoji[0][0], roseDarkBlu.name,
    onstage.emoji, onstage.name,
    rosePink.emoji[0][0], rosePink.name,
    crimsomLotus.emoji, crimsomLotus.name,
    roseYellow.emoji[0][0], roseYellow.name,
    finalTech.emoji, finalTech.name,
    roseBlue.emoji[0][0], roseBlue.name,
    valse.emoji, valse.name,
    roseGreen.emoji[0][0], roseGreen.name,
    finFloLaunchBase.emoji, finFloLaunchBase.name,
    danceFas.emoji,danceFas.name,
    petalisation.emoji,petalisation.name,
    floraisonFinale.emoji,floraisonFinale.name,
    croissance.emoji,croissance.name,
    roseeHeal.emoji,roseeHeal.name
))
mve2Eff = effect("Mors Vita Est Eternatum","mve2Eff",power=65,type=TYPE_BOOST,turnInit=-1,description="Lorsque le porteur de l'effet est vaincu et qu'il peut être réanimé, le réanime imédiament avec **{0}%** de ses PVmax",emoji='<:unlifeGift:984241071397670912>')
mve2 = skill("Mors Vita Est Eternatum","spg",TYPE_PASSIVE,0,effectOnSelf=mve2Eff,description="Lorsque vous êtes vaincu, vous vous réanimés directement avec un certain pourcentage de vos PV max",emoji="<:unlifeGift:984241071397670912>",quickDesc="Vous permet de vous réanimer vous même une fois vaincu")
krasisEff = copy.deepcopy(absEff)
krasisEff.power, krasisEff.inkResistance, krasisEff.stat, krasisEff.turnInit = 20, 15, INTELLIGENCE, 3
krasis = skill("Krasis","spf",TYPE_BOOST,500,effects=krasisEff,cooldown=5,description="Augmente de **20%** les soins reçus par la cible et réduit les dégâts indirects qu'elle reçoit durant **2** tours",emoji='<:krasis:982359813742800947>')
pandaimaShield = copy.deepcopy(haimaShield)
pandaimaShield.name, pandaimaShield.overhealth, pandaimaShield.emoji = "Pandaima (Armure)", 10, sameSpeciesEmoji('<:panhaimaB:916922951054540810>','<:panhaimaR:916922965420040263>')
pandaimaEff = copy.deepcopy(haimaEffect)
pandaimaEff.callOnTrigger, pandaimaEff.description, pandaimaEff.name, pandaimaEff.emoji = pandaimaShield, "En subissant des dégâts sans posséder d'effet \"__Pandaima - Bouclier__\", le porteur de cet effet gagne le dit effet au prix d'une charge de __Pandaima__", "Pandaima", uniqueEmoji('<:pandaima:982349300505931856>')
pandaima = copy.deepcopy(haimaSkill)
pandaima.name, pandaima.id, pandaima.effects, pandaima.range, pandaima.area, pandaima.emoji = "Pandaima", "spe", [pandaimaEff], AREA_MONO, AREA_CIRCLE_3, "<:pandaima:982349300505931856>"
gravitonEff = effect("Gravité","GravitonEff",agility=-5,precision=-3,emoji='<:graviton:982316403078078464>',type=TYPE_MALUS,stat=ENDURANCE)
graviton = skill("Graviton","spd",TYPE_MALUS,350,range=AREA_MONO,area=AREA_INLINE_5,effects=gravitonEff,pull=5,cooldown=5,emoji='<:graviton:982316403078078464>',description="Réduit l'agilité et la précision des ennemis à porté et les attirent sur vous")
temperanceEff1, temperanceEff2 = copy.deepcopy(healDoneBonus), copy.deepcopy(defenseUp)
temperanceEff1.power, temperanceEff2.power, temperanceEff2.stats, temperanceEff2.turnInit, temperanceEff1.turnInit = 20, 7, CHARISMA, 3, 3
temperance = skill("Tempérance","spc",TYPE_BOOST,750,effects=temperanceEff2,effectOnSelf=temperanceEff1,range=AREA_MONO,area=AREA_DONUT_4,cooldown=7,description="Réduit les dégâts subis par les alliés alentours tout en augmentant votre quantité de soins réalisés",emoji='<:temperance:982349348992081960>')
teracholeEff = copy.deepcopy(defenseUp)
teracholeEff.power, teracholeEff.stat = 10, CHARISMA
terachole = skill("Terachole","spb",TYPE_HEAL,price=500,power=60,effects=teracholeEff,cooldown=5,emoji='<:terachole:982349368864698428>',description="Soigne l'allié ciblé tout en réduisant les dégâts qu'il subit pendant un tour")
aquavoileEff = copy.deepcopy(defenseUp)
aquavoileEff.power, aquavoileEff.stat, aquavoileEff.turnInit = 10, CHARISMA, 2
aquavoile = skill("Aquavoile","spa",TYPE_BOOST,350,effects=aquavoileEff,cooldown=5,emoji='<:aquavoile:982349320835727400>')
misery = skill("Offrande de misère","soz",TYPE_DAMAGE,750,120,area=AREA_CIRCLE_1,use=CHARISMA,useActionStats=ACT_HEAL,cooldown=7,emoji='<:misery:982359796239966238>')
tangoEndEff = effect("Tango Endiablé","tango",CHARISMA,critical=5,critDmgUp=15,turnInit=3,description="Augmente le taux de critique et les dégâts critiques infligés pendant 3 tours\nSi cet effet est octroyé grace à __Position Rapprochée__, sa puissance n'en est pas réduite",emoji='<:tango:982359831518277772>')
tangoEnd = skill('Tango Endiablé',"soy",TYPE_BOOST,price=500,area=AREA_CIRCLE_1,range=AREA_MONO,emoji='<:tango:982359831518277772>',cooldown=7,effects=tangoEndEff)
danseStarFall = skill("Danse de la pluie étoilée","sox",TYPE_DAMAGE,750,175,area=AREA_LINE_4,effBeforePow=True,effectOnSelf=tangoEndEff,cooldown=7,description="Inflige des dégâts en ligne droite puis augmente votre taux de critique et vos dégâts critiques pour vos deux prochains tours",ultimate=True,emoji='<:pluieEtoile:982359861679521833>')
graviton2 = skill("Gravi som'Mont","sow",TYPE_DAMAGE,500,range=AREA_MONO,area=AREA_INLINE_5,use=ENDURANCE,knockback=5,power=50,cooldown=5,emoji='<:graviton:982316403078078464>',description="Inflige des dégâts aux ennemis dans la zone d'effet et les repousses")
invocAutTour = skill("Invocation - Auto tourelle Tour","sov",TYPE_SUMMON,500,range=AREA_CIRCLE_4,invocation="Auto tourelle Tour",cooldown=5,emoji='<:autoTowB:982946185247588372>',description="Invoque une Auto tourelle Tour, une invocation de dégâts à longue portée",use=PRECISION,shareCooldown=True)
invocAutFou = skill("Invocation - Auto tourelle Fou","sou",TYPE_SUMMON,500,range=AREA_CIRCLE_4,invocation="Auto tourelle Fou",emoji='<:autoFouR:982946204046462987>',cooldown=5,description="Invoque une Auto tourelle Fou, une invocation de soutien",use=INTELLIGENCE,shareCooldown=True)
invocAutQueen = skill("Invocation - Auto tourelle Reine","sot",TYPE_SUMMON,750,range=AREA_CIRCLE_4,invocation="Auto tourelle Reine",emoji='<:autoQueenB:982946221599641610>',cooldown=7,description="Invoque une Auto tourelle Reine, une invocation dedégâts de mêlée",use=STRENGTH,shareCooldown=True)

jetLagDmgEff = effect("Déphasage temporel","jetLagDmgEff",None,power=1,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,stackable=True,emoji=sameSpeciesEmoji("<:jetLagB:984520122150555728>","<:jetLagR:984520139745689600>"))
jetLagEff = effect("Déphasage Intemporel","jetLagEff",None,power=50,emoji=sameSpeciesEmoji("<:jetLagB:984519444082610227>","<:jetLagR:984519461111472228>"),turnInit=3,type=TYPE_MALUS,description="**{0}%** des dégâts directs infligés par le porteur sont convertis en dégâts indirects en fin de tour sur la cible")
recall = skill("Rappel","soq",TYPE_RESURECTION,750,power=150,use=CHARISMA,emoji="<:rewind:984519329993347082>",cooldown=7,area=AREA_CIRCLE_3,effects=jetLagEff,condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],description="Réanime les alliés vaincus, mais leur inflige <:jetLagB:984519444082610227> __Déphasage Intemporel__")
divineBenediction = skill("Bénédiction Divine","sol",TYPE_RESURECTION,750,kikuRes.power,kikuRes.range,group=SKILL_GROUP_HOLY,area=kikuRes.area,maxHpCost=25,initCooldown=kikuRes.initCooldown,cooldown=kikuRes.cooldown,use=CHARISMA,emoji='<:divineRez:989531100332310569>')

elemRuneNames, elemRuneSkill, elemRuneId, elemRuneEmoji = ["neutre","flamboyante","givrée", "coupante", "fracasante", "lumineuse", "assombrissante", "dimentionnelle","temporelle"], [], list(getArrayAutoId(divineBenediction.id,9,True)), ["<:nrs:989526817624981535>","<:frs:989526738226778142>","<:wrs:989526716206702743>","<:ars:989526692118790254>","<:ers:989526669889003610>","<:lrs:989526613043601438>","<:drs:989526594257305670>","<:srs:989526647579476050>","<:trs:989526631213314048>"]
for cmpt in range(len(elemNames)-1):
    isMono = cmpt % 2 == 0
    if cmpt in [0,5,6,7,8]:
        skillRange = AREA_CIRCLE_5
    elif cmpt in [1,2]:
        skillRange = AREA_DIST_5
    else:
        skillRange = AREA_CIRCLE_3
    elemRuneSkill.append(skill("Rune {0}".format(elemRuneNames[cmpt]),elemRuneId[cmpt],TYPE_DAMAGE,500,[65,80][isMono]+15*int(skillRange==AREA_CIRCLE_3)+10*int(skillRange==AREA_DIST_5),range=skillRange,area=[AREA_LINE_2,AREA_MONO][isMono],description="Inflige des dégâts {0} en consommants tous vos effets {1} __{2}__\nPour chaque effets consommés, la puissance de cette compétence augmente de **{3}**".format(["aux ennemis ciblés","à l'ennemi ciblé"][isMono],tablElemEff[cmpt].emoji[0][0],tablElemEff[cmpt].name,INCREASEPOWERPURCENTBYELEMEFF),cooldown=5,condition=[EXCLUSIVE,ELEMENT,cmpt],use=MAGIE,emoji=elemRuneEmoji[cmpt]))

divineCircleEff = effect("Cercle Sacré","divineCircleEff",MAGIE,magie=10,turnInit=3,emoji='<:divineCercle:989532178109042698>')
divineCircle = skill("Cercle Sacré",getAutoId(elemRuneSkill[-1].id,True),TYPE_BOOST,500,effects=divineCircleEff,area=AREA_CIRCLE_3,cooldown=5,maxHpCost=10,emoji='<:divineCercle:989532178109042698>')
divineWayEff = effect("Guide Divin","divineGuide",CHARISMA,strength=12,magie=12,turnInit=3)
divineGuid = skill("Guide Divin",getAutoId(divineCircle.id,True),TYPE_BOOST,price=500,effects=divineWayEff,cooldown=5,maxHpCost=7,group=SKILL_GROUP_HOLY)
THEALNEEDEDFORUBER, TINDHNEEDFORUBER = 3000, 5000
uberJauge = effect("ÜberJauge","uberJauge",turnInit=-1,emoji='<:ubc:985647422556495913>',unclearable=True)

uberJauge.jaugeValue = jaugeValue(
    emoji=pasTech.jaugeValue.emoji,
    conds=[
        jaugeConds(INC_DEAL_HEALING,25/100)
    ]
)

uberImune = effect("Übercharge","uberImune",emoji='<:ubc:985647422556495913>',immunity=True)
uberCharge = skill("Übercharge",getAutoId(divineGuid.id,True),TYPE_HEAL,750,65,emoji='<:ubc:985647422556495913>',jaugeEff=uberJauge,cooldown=5,description="Consomme votre ÜberJauge pour soigner l'allié ciblé.\nPlus la ÜberJauge était remplie, plus les soins seront puissants, jusqu'à **+100%**\n\nOctroi également un effet de réduction de dégâts à la cible.\nPlus la ÜberJauge était remplie, plus la réduction de dégâts sera élevée, jusqu'à **75%**\nSi la ÜberJauge était pleine, rend la cible **Immunisée** à la place",maxPower=120,minJaugeValue=20,maxJaugeValue=100)

bloodBathEff = copy.deepcopy(vampirismeEff)
bloodBathEff.stat, bloodBathEff.power = STRENGTH, 20
bloodBath = skill("Bain de Sang",getAutoId(uberCharge.id,True),TYPE_DAMAGE,500,75,range=AREA_MONO,area=AREA_CIRCLE_2,effectOnSelf=bloodBathEff,effBeforePow=True,cooldown=7,condition=[EXCLUSIVE,ASPIRATION,BERSERK],emoji='<:bloodbath:986614852082626570>',description="Vous octroi __Vampirisme__ pendant 2 tours et effectue une attaque sur les ennemis proches")
erodAoe = skill("Erosion Avancée",getAutoId(bloodBath.id,True),TYPE_DAMAGE,500,80,AREA_CIRCLE_2,area=AREA_CONE_2,condition=[EXCLUSIVE,ASPIRATION,TETE_BRULE],cooldown=5,erosion=50,emoji='<:eros:986614877076488202>',description="Inflige des dégâts aux ennemis ciblés en réduisant leurs PVmax")
divineAbneEff = copy.deepcopy(dmgUp)
divineAbneEff.turnInit, divineAbneEff.power, divineAbneEff.unclearable = -1, 25, True
divineAbne = skill("Abnégation Divine",getAutoId(erodAoe.id,True),TYPE_PASSIVE,use=None,emoji='<:abdiv:987022697991139358>',price=500,effectOnSelf=divineAbneEff,group=SKILL_GROUP_HOLY,power=35,description="Augmente vos dégâts infligés de **25%** durant tout le combat mais réduits vos PV maximums de **35%**",quickDesc="Augmente vos dégâts innfligés mais réduit vos PV maximum")
astrodynEff = effect("Astrodynamie","astrodyn",CHARISMA,strength=10,magie=10,agility=5,precision=5,emoji='<:astro:986614953047912499>',description="Augmente les statistiques offensives du porteur")
astrodyn = skill("Astrodynamie",getAutoId(divineAbne.id,True),TYPE_BOOST,750,effects=astrodynEff,url="https://media.discordapp.net/attachments/1006418796329848954/1007574359403151450/20220812_105137.gif",range=AREA_MONO,area=AREA_CIRCLE_3,emoji='<:astro:986614953047912499>',description='Augmente les statistiques des alliés proches et réduit le temps de rechargement de votre Transcendance de 3 tours',cooldown=7,condition=[EXCLUSIVE,ASPIRATION,IDOLE])
cercleConEff = copy.deepcopy(dmgUp)
cercleConEff.power, cercleConEff.stat = 6.5, INTELLIGENCE
cercleCon = skill("Cercle de Connaissance",getAutoId(astrodyn.id,True),TYPE_BOOST,750,range=AREA_MONO,area=AREA_CIRCLE_3,effects=cercleConEff,url='https://media.discordapp.net/attachments/1003025632415973510/1007612026220204062/20220812_132824.gif',emoji='<:arcCircle:986615034627113040>',cooldown=7,description="Augmente les dégâts infligés par vos alliés proches et réduit le temps de rechargement de votre Transcendance de 3 tours",condition=[EXCLUSIVE,ASPIRATION,INOVATEUR])
aliceFanDanse2Eff = effect("Galvanisation de l'éventail","aliceFanDanseBuff",CHARISMA,strength=7,magie=7,endurance=5,charisma=5,intelligence=5,turnInit=3)
aliceFanDanse2 = skill("Chorégraphie de l'éventail",getAutoId(cercleCon.id,True),TYPE_DAMAGE,500,power=110,range=AREA_MONO,area=AREA_CIRCLE_5,setAoEDamage=True,cooldown=5,effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_4,aliceFanDanse2Eff],description="Effectue une chorégraphie de l'éventail durant 3 tours, infligeant des dégâts croissants aux ennemis autour de vous. Au dernier tour, la compétence a plus de portée et augmente la force, magie et endurance et alliés alentours",emoji='<:fanDance:986987567557775490>')
aliceFanDanse2Cast = effect(aliceFanDanse2.name,"aliceFanDanse2Cast",turnInit=2,silent=True,replique=aliceFanDanse2,emoji=aliceFanDanse2.emoji)
aliceFanDanse1 = skill("Chorégraphie de l'éventail",aliceFanDanse2.id,TYPE_DAMAGE,500,power=100,range=AREA_MONO,area=AREA_CIRCLE_3,setAoEDamage=True,cooldown=6,effectOnSelf=aliceFanDanse2Cast,description="Effectue une chorégraphie de l'éventail durant 3 tours, infligeant des dégâts croissants aux ennemis autour de vous. Au dernier tour, la compétence a plus de portée et augmente la force, magie et endurance et alliés alentours",emoji='<:fanDance:986987567557775490>')
aliceFanDanse1Cast = effect(aliceFanDanse2.name,"aliceFanDanse1Cast",turnInit=2,silent=True,replique=aliceFanDanse1,emoji=aliceFanDanse2.emoji)
aliceFanDanse = skill("Chorégraphie de l'éventail",aliceFanDanse2.id,TYPE_DAMAGE,500,power=90,range=AREA_MONO,area=AREA_CIRCLE_3,setAoEDamage=True,cooldown=5,effectOnSelf=aliceFanDanse1Cast,description="Effectue une chorégraphie de l'éventail durant 3 tours, infligeant des dégâts croissants aux ennemis autour de vous. Au dernier tour, la compétence a plus de portée et augmente la force, magie et endurance et alliés alentours",emoji='<:fanDance:986987567557775490>')
plumeCel = skill("Plumes Célestes",getAutoId(aliceFanDanse.id,True),TYPE_DAMAGE,500,power=100,area=AREA_CIRCLE_2,range=AREA_DIST_6,cooldown=5,emoji='<:plumeCel:989539461224337432>')
plumePers = skill("Plumes Perçantes",getAutoId(plumeCel.id,True),TYPE_DAMAGE,500,power=90,range=AREA_DIST_4,area=AREA_LINE_3,percing=35,cooldown=5,emoji='<:plumePers:989539480375525408>')
pousAviaire = skill("Poussée Aviaire",getAutoId(plumePers.id,True),TYPE_DAMAGE,500,power=120,range=AREA_CIRCLE_1,area=AREA_CONE_2,knockback=1,jumpBack=1,cooldown=5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],emoji='<:birdPush:989537549838090310>')
demonRegenEff = effect("Régénération Démonique","demonRegen",CHARISMA,power=50,turnInit=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji='<:regenDem:989529378885107782>')
demonRegen = skill("Régénération Démoniaque",getAutoId(pousAviaire.id,True),TYPE_INDIRECT_HEAL,500,effects=demonRegenEff,hpCost=20,group=SKILL_GROUP_DEMON,cooldown=7,emoji='<:regenDem:989529378885107782>')
demonDmgBuff = copy.deepcopy(dmgUp)
demonDmgBuff.stat, demonDmgBuff.power, demonDmgBuff.turnInit = INTELLIGENCE, 10, 3
demonLink = skill("Union Démoniaque",getAutoId(demonRegen.id,True),TYPE_BOOST,500,effects=demonDmgBuff,area=AREA_CIRCLE_1,hpCost=25)

bloodBath2 = skill("Bain de Sang Avancé",getAutoId(demonLink.id,True),TYPE_DAMAGE,0,135,range=AREA_CIRCLE_2,cooldown=7,condition=[EXCLUSIVE,ASPIRATION,BERSERK],emoji=bloodBath.emoji,effectOnSelf=bloodBathEff,effBeforePow=True)
altyCoverEff2 = effect("Couverture","altyCoverEff2",redirection=100,trigger=TRIGGER_DAMAGE,emoji='<:altyCover:988767335974326272>')
altyCoverEff1 = effect("Régénération compréhensive","altyCoverEff1",CHARISMA,power=22,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji='<:AltyRegen:994748551932428319>')
altyCover = skill("Couverture Compréhensive",getAutoId(bloodBath2.id,True),TYPE_INDIRECT_HEAL,emoji='<:altyCover:988767335974326272>',effects=[altyCoverEff1,altyCoverEff2],range=AREA_DONUT_5,initCooldown=3,cooldown=7,description="Redirige l'intégralité des dégâts directs reçus par un allié sur vous pendant 1 tour tout en lui octroyant un effet de régénération pendant 3 tours")
klikliStrike = skill("Frappe Vangeresse",getAutoId(altyCover.id,True),TYPE_DAMAGE,power=95,maxPower=200,range=AREA_CIRCLE_3,emoji='<:klikliStrike:994743803514732664>',cooldown=7,effectOnSelf=holmgangEff,effBeforePow=True,effects=chained,description="Consomme la quasi totalité de vos PVs pour infliger des dégâts à l'ennemi ciblé\nPlus votre pourcentage de PV était élevé, plus l'attaque sera puissance\nVous octroi également Holmgang et entrave les déplacements de l'ennemi ciblé")
gwenyStrike = skill("Impact Justicier",getAutoId(klikliStrike.id,True),TYPE_DAMAGE,power=50,maxPower=150,range=AREA_MONO,emoji='<:gwenyStrike:994747468182978663>',area=AREA_CIRCLE_2,selfEffPurcent=35,cooldown=7,effectOnSelf=holmgangEff,effectAroundCaster=[TYPE_MALUS,AREA_DONUT_1,chained],effBeforePow=True,description="Consomme la quasi totalité de vos PVs pour infliger des dégâts aux ennemis alentours\nPlus votre pourcentage de PV était élevé, plus l'attaque sera puissance\nVous octroi également Holmgang et entrave les déplacements des ennemis aux corps à corps", minTargetRequired=3)

plumRemEff = effect("Plumes Rémanantes","plumRemEff",STRENGTH,power=100,area=AREA_CIRCLE_1,turnInit=6,type=TYPE_INDIRECT_DAMAGE,emoji="<:plumeRem:989543669839319102>",stackable=True)
plumRem = skill("Plumes Rémanantes",getAutoId(gwenyStrike.id,True),TYPE_DAMAGE,750,50,AREA_DIST_7,initCooldown=3,cooldown=5,area=AREA_CIRCLE_3,emoji="<:plumeRem:989543669839319102>",description="Vos compétences {0} __{1}__, {2} __{3}__, {4} __{5}__ et {6} __{7}__ ont désormais **40%** de chance d'infliger l'effet {8} __{9}__ aux cibles affectées.\nVotre arme <:plume:871893045296128030> __Plumes Perçantes__ octroi désormais l'effet {8} __{9}__ à la place d'Incurable.\n\nLors de l'utilisation de cette compétence, tous les effets {8} __{9}__ présents sur les ennemis dans la zone d'effet infligent des dégâts dans une zone Cercle 1 avec une puissance de **{10}** (Dégâts Directs)".format(hinaUlt.emoji,hinaUlt.name,plumeCel.emoji,plumeCel.name,plumePers.emoji,plumePers.name,pousAviaire.emoji,pousAviaire.name,plumRemEff.emoji[0][0],plumRemEff.name,plumRemEff.power))

raisingPheonixLaunch = skill("Envolée du Phénix",getAutoId(plumRem.id,True),TYPE_DAMAGE,750,150,area=AREA_CIRCLE_3,emoji='<:rizePhenix:992940415080726688>',range=AREA_MONO,ultimate=True,cooldown=7,effectAroundCaster=[TYPE_RESURECTION,AREA_CIRCLE_3,150],use=MAGIE,useActionStats=ACT_DIRECT,description="Après un tour de chargement, Inflige des dégâts aux ennemis alentours tout en réanimant les alliés à portée")
raisingPhonixCastEff = effect("Cast - {0}".format(raisingPheonixLaunch.name),"raisingPhoenixCast",turnInit=2,emoji='<:rizePhenix:992940415080726688>',silent=True,replique=raisingPheonixLaunch)
raisingPheonix = copy.deepcopy(raisingPheonixLaunch)
raisingPheonix.power, raisingPheonix.effectAroundCaster, raisingPheonix.effectOnSelf = 0, None, raisingPhonixCastEff
fairyGardeEff = effect("Garde Féérique","fairyGarde",CHARISMA,power=100,type=TYPE_INDIRECT_HEAL,lvl=1,turnInit=3,trigger=TRIGGER_ON_REMOVE,emoji='<:suivFee:992496696321912902>')
fairyGarde = skill("Garde Féérique",getAutoId(raisingPheonix.id,True),TYPE_INDIRECT_HEAL,500,emoji='<:suivFee:992496696321912902>',effects=fairyGardeEff,cooldown=7,description="Octroi à l'allié ciblé un effet de soin qui se déclanchera à la fin de sa durée ou avant que le porteur subisse des dégâts mortels")
jaugeButLight = effect("Jauge Lumineuse","lightbutJauge",emoji=sameSpeciesEmoji("<:blum:992495387812311060>","<:rlum:992495404933455974>"),turnInit=-1,unclearable=True)
jaugeButLight.jaugeValue = jaugeValue(
    emoji=[["<:lej:980923743960461412>","<:mej:980923762016927764>","<:rej:980923786650075228>"],["<:wjl:992574938353516555>","<:wjr:992574974210625556>","<:wjm:992574958033174558>"]],
    conds=[jaugeConds(INC_START_TURN,10),jaugeConds(INC_USE_ELEMENT_SKILL,10,ELEMENT_LIGHT)]
)

sumLightButterfly = skill("Papillons de Lumière",getAutoId(fairyGarde.id,True),TYPE_SUMMON,500,use=CHARISMA,invocation="Papillon de Lumière",jaugeEff=jaugeButLight,cooldown=5,ultimate=True,description="Invoque un Papillon de Lumière qui soignera vos alliés.\n\nPour chaque pallié de **40 points** sur votre Jauge Lumineuse, un Papillon de Lumière supplémentaire est invoqué.",emoji='<:lumBut:992495232463667200>')
fairySlash = skill("Eclat Féérique",getAutoId(sumLightButterfly.id,True),TYPE_DAMAGE,500,power=85,cooldown=5,use=MAGIE,emoji='<:fairySlash:992497227459215451>',area=AREA_CIRCLE_1)
fairyBombEff = effect("Cogitation Féérique","cogiFee",MAGIE,power=60,trigger=TRIGGER_ON_REMOVE,type=TYPE_INDIRECT_DAMAGE,turnInit=2,area=AREA_CIRCLE_2,emoji='<:fairyBomb:992498513940332675>',description="Inflige des dégâts au porteur et ses alliés à portée de mêlée et leur inflige __Poison d'Estialba__ avec 40% de sa puissance")
fairyBomb = skill("Cogitation Féérique",getAutoId(fairySlash.id,True),TYPE_INDIRECT_DAMAGE,750,effects=fairyBombEff,cooldown=7,emoji='<:fairyBomb:992498513940332675>',description="Après deux tours ou si l'ennemi ciblé est vaincu, déclanche une détonatin à sa position lui infligeant des dégâts ainsi qu'à vos ennemis proches.\nLes entités affectés subissent l'effet __Poison d'Estialba__ (50%) pendant 3 tours")
dmonProtectEff = copy.deepcopy(defenseUp)
dmonProtectEff.power, dmonProtectEff.stat, dmonProtectEff.turnInit, dmonProtectEff.block = 8, INTELLIGENCE, 3, 35
dmonProtect = skill("Protection Démoniaque",getAutoId(fairyBomb.id,True),TYPE_BOOST,500,effects=dmonProtectEff,cooldown=5,hpCost=15,range=AREA_DONUT_5,description="Réduit les dégâts subis par un allié et sa probabilité de bloquer une attaque pendant **3** tours",emoji='<:proDmon:994026279680606258>')
hemoBombEff = effect("Cogitation Hemorragique","hemoBomb",STRENGTH,power=110,area=AREA_INLINE_2,turnInit=2,trigger=TRIGGER_ON_REMOVE,emoji='<:bloodyBomb:992499935738089592>',description="Après deux tours ou si l'ennemi ciblé est vaincu, déclanche une détonatin à sa position lui infligeant des dégâts ainsi qu'à vos ennemis allignés.\nLes entités affectés subissent l'effet __Hémorragie__ (25%) pendant 3 tours")
hemoBomb = skill("Cogitation Hémorragique",getAutoId(dmonProtect.id,True),TYPE_INDIRECT_DAMAGE,750,effects=hemoBombEff,cooldown=7,emoji='<:bloodyBomb:992499935738089592>',description="Après deux tours ou si l'ennemi ciblé est vaincu, déclanche une détonatin à sa position lui infligeant des dégâts ainsi qu'à vos ennemis allignés.\nLes entités affectés subissent l'effet __Hémorragie__ (25%) pendant 3 tours")
barrage = skill("Barrage",getAutoId(hemoBomb.id,True),TYPE_DAMAGE,500,40,range=AREA_CIRCLE_4,area=AREA_CONE_2,cooldown=5,repetition=3,emoji="<:barrage:994031489773748265>",accuracy=40)
liberation = skill("Libération",getAutoId(barrage.id,True),TYPE_DAMAGE,500,75,range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=5,knockback=3,condition=[EXCLUSIVE,ASPIRATION,POIDS_PLUME])
tripleAttaque2 = skill("Triple Attaque",getAutoId(liberation.id,True),TYPE_DAMAGE,500,50,range=AREA_CIRCLE_3,cooldown=5,description="Inflige trois attaques sur l'ennemi ciblé. Le dernier coup repousse la cible",knockback=2,condition=[EXCLUSIVE,ASPIRATION,POIDS_PLUME],emoji='<:tripleStrike3:1060211755793522798>')
tripleAttaque2cast = effect("Cast - Triple Attaque","tripleAttaque2",replique=tripleAttaque2,silent=True)
tripleAttaque1 = copy.deepcopy(tripleAttaque2)
tripleAttaque1.power, tripleAttaque1.effectOnSelf, tripleAttaque1.knockback, tripleAttaque1.replay, tripleAttaque1.emoji = 45, tripleAttaque2cast, 0, True, "<:tripleStrike2:1060211719911264416>"
tripleAttaque1cast = effect("Cast - Triple Attaque","tripleAttaque1",replique=tripleAttaque1,silent=True)
tripleAttaque = copy.deepcopy(tripleAttaque1)
tripleAttaque.power, tripleAttaque.effectOnSelf, tripleAttaque.replay, tripleAttaque.emoji = 40, tripleAttaque1cast, True, "<:tripleStrike1:1060211689217327114>"

arsenic = effect("Arsenic","arsenic",STRENGTH,power=30,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,stackable=True,emoji='<:arsenic:995361025773817916>')
acidRain1 = skill("Pluie Acide",getAutoId(tripleAttaque.id,True),TYPE_INDIRECT_DAMAGE,750,range=AREA_MONO,area=AREA_ALL_ENEMIES,emoji='<:acidRain:995360946241417388>',minTargetRequired=3,effects=arsenic,effPowerPurcent=propaUltLaunch.effPowerPurcent,ultimate=True,cooldown=propaUltLaunch.cooldown,description="Après un tour de chargement, inflige __Arsenic__ à tous les ennemis")
acidRainCast = effect("Cast - Pluie Acide","acidRainCast",turnInit=2,silent=True,replique=acidRain1)
acidRain = copy.deepcopy(acidRain1)
acidRain.effects, acidRain.effectOnSelf = [None], acidRainCast
coroRocket = skill("Fusée Corosive",getAutoId(acidRain.id,True),TYPE_INDIRECT_DAMAGE,500,effects=arsenic,area=AREA_CONE_2,cooldown=poisonus.cooldown,emoji='<:coroRocket:995360986603196417>')
coroMissile1 = skill("Missile corrosif",getAutoId(coroRocket.id,True),TYPE_INDIRECT_DAMAGE,750,effects=arsenic,area=AREA_CONE_3,minTargetRequired=2,cooldown=7,emoji='<:coroMissile:995361003581739018>')
coroMissileCast = effect("Cast - Missile corrosif","coroMissileCast",turnInit=2,silent=True,replique=coroMissile1)
coroMissile = copy.deepcopy(coroMissile1)
coroMissile.effects, coroMissile.effectOnSelf = [None], coroMissileCast
coroShot = skill("Tir corrosif",getAutoId(coroMissile.id,True),TYPE_DAMAGE,500,80,area=AREA_LINE_3,effects=arsenic,cooldown=5,emoji='<:coroShot:995360968697716837>')

quadFleau = skill("Quadruple Fléau",getAutoId(coroShot.id,True),TYPE_INDIRECT_DAMAGE,750,effects=["me",coroWind,"mx",arsenic],effPowerPurcent=50,cooldown=7,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS], emoji='<:quaFleau:1016796997887459370>')
charmingPandant = skill("Médaillon d'Amour","sph",TYPE_BOOST,emoji='<:lovePendant:982175214773358593>',price=750,area=AREA_CIRCLE_2,range=AREA_MONO,cooldown=5,description="Augmente les statistiques des alliés proches tout en réduisant légèrement celles des ennemis autour de vous")
windDanceEff = effect("Soyokaze","windDanceEff",turnInit=-1,unclearable=True,emoji='<:liaCounter:998001563379437568>',reject=["liaKatanaEff"],counterOnDodge=25,description="Vous octroi **25%** de chance d'effectuer une **contre-attaque** en esquivant une attaque d'un adversaire se trouvant à 3 cases ou moins de vous")
windDance = skill("Soyokaze",getAutoId(quadFleau.id,True),TYPE_PASSIVE,500,effectOnSelf=windDanceEff,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],emoji="<:liaCounter:998001563379437568>",quickDesc="Vous donne une chance de contre-attaquer en esquivant une attaque")

belierChargeEff = copy.deepcopy(defenseUp)
belierChargeEff.power, belierChargeEff.block = 25, 35
belierCharge = skill("Charge du Bélier","jushu",TYPE_DAMAGE,500,power=60,effectOnSelf=belierChargeEff,cooldown=7,range=AREA_INLINE_4,description="Vous téléporte au corps à corps d'un ennemi en lui infligeant des dégâts tout en réduisant vos dégâts réçus et augmentant votre taux de blocage jusqu'au prochain tour")
taureauFury = skill("Furie du Taureau","geghthz",TYPE_DAMAGE,500,power=37,setAoEDamage=True,repetition=3,accuracy=100,area=AREA_CIRCLE_2,range=AREA_MONO,cooldown=7,description="Inflige trois attaques aux ennemis à portée de mêlée avec une précision accrue")
gemeauSynEff = copy.deepcopy(dmgUp)
gemeauSynEff.power = 15
gemeauSyn = skill("Synergie des Jumeaux","hehge",TYPE_BOOST,500,effects=gemeauSynEff,effectOnSelf=gemeauSynEff,cooldown=7,replay=True,description="Augmente vos propres dégâts infligés ainsi que ceux de l'allié ciblé de **15%** pendant un tour et vous permet de rejouer")
cancerAssault = skill("Assaut du Crabe","hehehe",TYPE_DAMAGE,500,power=12,repetition=10,cooldown=7,range=AREA_INLINE_4,description="Attaque à dix reprises l'ennemi ciblé")
lionRoarEff= effect("Couardise","lion'sroareff",ENDURANCE,strength=-10,magie=-10,charisma=-10,intelligence=-10,type=TYPE_MALUS)
lionRoar = skill("Rugissement du Lion","hehehe",TYPE_MALUS,500,range=AREA_MONO,area=AREA_DONUT_4,effects=lionRoarEff,cooldown=7,description="Réduit les statistiques des ennemis alentours pendant un tour")
viergeSkillEff = effect("Bénédiction de la vierge","viergeBene",type=TYPE_BOOST,stat=INTELLIGENCE,resistance=7,inkResistance=12,turnInit=3)
vierge = skill("Bénidiction de la Vièrge","rgege",TYPE_BOOST,500,effects=viergeSkillEff,cooldown=7,description="Accroi la Résistance et réduit les dégâts indirects subis de l'allié ciblé")
balanceBoostEff = effect("Egaltité de la Balance",'balanceBoostEff',CHARISMA,strength=5,endurance=5,charisma=5,intelligence=5,agility=5,precision=5,magie=5,emoji='<:balance:960319658823667762>')
balanceBoost = skill("Equilibre de la Balance","rejgikjhg",TYPE_BOOST,500,area=AREA_CIRCLE_5,range=AREA_MONO,effects=balanceBoostEff,cooldown=7,description="Augmente légèrement les statistiques principaux de vos alliés proches")
scorpVenum = effect("Venin du Scorpion","scorpionVenum",MAGIE,power=40,turnInit=2,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,description="Inflige des dégâts à la fin du tour du porteur pendant deux tours",lvl=2)
scorpionByte = skill("Piqûre du Scorpion","gsg",TYPE_DAMAGE,500,power=65,use=MAGIE,effects=scorpVenum,cooldown=7,description="Inflige des dégâts à l'ennemi ciblé et l'empoisonne pendant 2 tours",useActionStats=ACT_INDIRECT)
sagArrow = skill("Flèche du Sagitaire","hhehe",TYPE_DAMAGE,500,power=120,area=AREA_LINE_3,range=AREA_CIRCLE_4,cooldown=7,description="Inflige des dégâts aux ennemis ciblés")
capricorne = skill("Percée du Capricorne","hehehe",TYPE_DAMAGE,500,135,area=AREA_LINE_3,range=AREA_CIRCLE_1,cooldown=7,use=MAGIE,description="Inflige des dégâts aux ennemis ciblés")
verseauShield = effect("Versatilité","verseauShield",INTELLIGENCE,overhealth=40,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
verseau = skill("Omniprésence du Verseau","hehhee",TYPE_HEAL,500,50,area=AREA_CIRCLE_2,effects=verseauShield,range=AREA_CIRCLE_4,cooldown=7,description="Soigne les alliés ciblés et leur octroi une armure",use=INTELLIGENCE)
fishHot = effect("Grâce du Poisson","fishGrace",CHARISMA,power=22,turnInit=3,type=TYPE_HEAL,trigger=TRIGGER_START_OF_TURN)
fishGrace = skill("Grâce du Poisson","heheheh",TYPE_INDIRECT_HEAL,500,effects=fishHot,area=AREA_CIRCLE_3,range=AREA_MONO,cooldown=7,description="Applique un effet de régénération sur vous et vos alliés proches")
lightEstoc = skill("Estoc Lumineuse",getAutoId("smh",True),TYPE_DAMAGE,500,power=80,range=AREA_CIRCLE_1,emoji='<:estocLum:1015221284726128710>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_4,40],cooldown=5,description="Inflige des dégâts aux ennemis ciblés et vous soigne ainsi que vos alliés alentours",use=CHARISMA,useActionStats=ACT_HEAL,area=AREA_LINE_2)
lightTrancheShield = effect("Armure de Lumière","lightArmor",INTELLIGENCE,stackable=True,type=TYPE_ARMOR,trigger=TRIGGER_START_OF_TURN,turnInit=3,overhealth=40)
lightTranche = skill("Tranche Lumineuse",getAutoId(lightEstoc.id,True),TYPE_DAMAGE,500,power=85,range=AREA_CIRCLE_1,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],effectAroundCaster=[TYPE_ARMOR,AREA_CIRCLE_4,lightTrancheShield],cooldown=5,description="Inflige des dégâts aux ennemis ciblés et vous procure ainsi qu'à vos alliés alentours une armure",use=INTELLIGENCE,useActionStats=ACT_SHIELD,area=AREA_ARC_1,emoji='<:trancheLum:1066757399949606922>')
lightShot = skill("Tir Lumineux",getAutoId(lightTranche.id,True),TYPE_DAMAGE,500,emoji='<:tirLum:1015221197627211857>',power=70,range=AREA_CIRCLE_5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_4,35],cooldown=5,description="Inflige des dégâts aux ennemis ciblés et vous soigne ainsi que vos alliés alentours",use=CHARISMA,useActionStats=ACT_HEAL,area=AREA_LINE_2)
lightPulseShield = effect("Armure de Lumière","lightArmor",INTELLIGENCE,stackable=True,type=TYPE_ARMOR,trigger=TRIGGER_START_OF_TURN,turnInit=3,overhealth=30)
lightPulse = skill("Pulsation Lumineuse",getAutoId(lightShot.id,True),TYPE_DAMAGE,500,power=65,range=AREA_CIRCLE_1,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],effectAroundCaster=[TYPE_ARMOR,AREA_CIRCLE_4,lightPulseShield],cooldown=5,description="Inflige des dégâts aux ennemis ciblés et vous procure ainsi qu'à vos alliés alentours une armure",use=INTELLIGENCE,useActionStats=ACT_SHIELD,emoji='<:pulLum:1066757422976356514>')

accelerant = skill("Accélération",getAutoId(lightPulse.id,True),TYPE_BOOST,750,cooldown=5,description="Permet à l'allié ciblé de jouer deux fois lors de son prochain tour",condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],emoji='<:qqLuna:932318030380302386>')
assautEcarlateEff = copy.deepcopy(defenseUp)
assautEcarlateEff.power = 20
assautEcarlate = skill("Assaut Ecarlate",getAutoId(accelerant.id,True),TYPE_DAMAGE,500,50,range=AREA_CIRCLE_1,area=AREA_CONE_3,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],cooldown=5,emoji='<:assEcar:999762960484409454>',description="Vous téléporte au corps à corps de l'ennemi ciblé, lui inflige des dégâts ainsi qu'à ses alliés proches, puis effectue une seconde attaque dans une large zone d'effet tout en réduisant de **{0}%** les dégâts subis pendant un tour".format(assautEcarlateEff.power),effectOnSelf=assautEcarlateEff)
assautEcarlateCast = effect("Cast - Assaut Ecarlate","assEcarCast",replique=assautEcarlate,silent=True)
cycloneEcarlate = skill("Cyclone Ecarlate",assautEcarlate.id,TYPE_DAMAGE,assautEcarlate.price,assautEcarlate.power,tpCac=True,range=AREA_INLINE_4,area=AREA_CIRCLE_1,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],cooldown=7,emoji='<:cyclEcar:999762891513266287>',description="Vous téléporte au corps à corps de l'ennemi ciblé, lui inflige des dégâts ainsi qu'à ses alliés proches, puis effectue une seconde attaquedans une large zone d'effet tout en réduisant de **{0}%** les dégâts subis pendant un tour".format(assautEcarlateEff.power),effectOnSelf=assautEcarlateCast,replay=True)
sillageEff = effect("Sillage","sillageEff",MAGIE,power=40,area=AREA_CIRCLE_2,trigger=TRIGGER_END_OF_TURN,turnInit=2,lvl=2,emoji='<:sill:999763058526269510>',type=TYPE_INDIRECT_DAMAGE)
sillage = skill("Sillage",getAutoId(cycloneEcarlate.id,True),TYPE_DAMAGE,500,sillageEff.power+10,use=MAGIE,area=AREA_CIRCLE_1,range=AREA_CIRCLE_4,effects=sillageEff,cooldown=5,emoji=sillageEff.emoji[0][0],description="Inflige des dégâts à l'ennemi ciblé et lui inflige un effet de poison qui infligera des dégâts en zone durant les deux prochains tours",condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR])
casseMontEff = effect("Casse Montagne","cassMont",MAGIE,power=30,lvl=5,turnInit=3,emoji="<:cassMont:999763013722701944>",description="Lorsque le porteur effectue une attaque, inflige des dégâts supplémentaires à la cible principale si cette dernière est un ennemi")
cassMont = skill("Casse-Montagne",getAutoId(sillage.id,True),TYPE_BOOST,500,range=AREA_MONO,replay=True,effects=casseMontEff,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],cooldown=5,emoji=casseMontEff.emoji[0][0],description="Lors de vos **{0}** prochaines attaques, vous infligerez des dégâts indirects supplémentaires".format(casseMontEff.lvl))
finalClassique = skill("Final Classique",getAutoId(cassMont.id,True),TYPE_DAMAGE,500,power=50,maxPower=125,accuracy=105,range=AREA_MONO,area=AREA_CIRCLE_2,jaugeEff=finalTech.jaugeEff,minJaugeValue=15,maxJaugeValue=50,description="Consomme une partie de votre __Jauge Technique__ pour infliger des dégâts aux ennemis autour de vous avec une précision accrue. Plus la quantité de jauge consommée est élevée, plus les dégats seront importants",emoji='<:finCla:1000145130357006436>')
lysJauge = effect("Canne fleurie","lysJaugeEff",turnInit=-1,unclearable=True,emoji='<:canFleur:1000145818877177886>')

lysJauge.jaugeValue = jaugeValue(
    emoji=pasTech.jaugeValue.emoji,
    conds=[jaugeConds(INC_START_TURN,15)]
)

offrRec = skill("Offrande de Réconfort",getAutoId(finalClassique.id,True),TYPE_HEAL,500,power=int(cure.power*0.8),jaugeEff=lysJauge,minJaugeValue=30,description="Soigne l'allié ciblé. Cette compétence n'a pas de délais de récupération mais consomme une partie de votre {0} __{1}__ à chaque utilisation".format(lysJauge.emoji[0][0],lysJauge.name),emoji='<:recof:1000144740651634748>')
offrRav = skill("Offrande de Ravissement",getAutoId(offrRec.id,True),TYPE_HEAL,500,power=int(offrRec.power*0.6),jaugeEff=lysJauge,minJaugeValue=30,description="Vous soigne ainsi que les alliés autour de vous. Cette compétence n'a pas de délais de récupération mais consomme une partie de votre {0} __{1}__ à chaque utilisation".format(lysJauge.emoji[0][0],lysJauge.name),area=AREA_CIRCLE_4,range=AREA_MONO,emoji='<:ravis:1000144722427392010>')
confiteorReady = effect("Confiteor préparé","confiteorReady",turnInit=5,emoji='<:confiteor:1003026495050096731>')
confiteor = skill("Confiteor",getAutoId(offrRav.id,True),TYPE_DAMAGE,0,125,area=AREA_CIRCLE_1,emoji='<:confiteor:1003026495050096731>',needEffect=[confiteorReady],cooldown=5)
holyCircleReady = effect("Cercle Sacré préparé","holyCircleReady",turnInit=5,emoji='<:cerSacre:1003026472262451300>')
cercleSacre = skill("Cercle Sacré",confiteor.id,TYPE_DAMAGE,0,90,area=AREA_CIRCLE_2,range=AREA_MONO,emoji='<:cerSacre:1003026472262451300>',needEffect=[holyCircleReady],effectOnSelf=confiteorReady)
holySpiritReady = effect("Esprit Saint préparé","holySpiritReady",turnInit=5,emoji='<:espSaint:1003026446706544733>')
espritSaint = skill("Esprit Saint",confiteor.id,TYPE_DAMAGE,0,90,emoji='<:espSaint:1003026446706544733>',needEffect=[holySpiritReady],effectOnSelf=holyCircleReady)
requiescat = skill("Requiescat",confiteor.id,TYPE_DAMAGE,0,80,emoji='<:requiescat:1003026420798328974>',effectOnSelf=holySpiritReady,description="Inflige des dégâts à l'ennemi ciblé et vous permet de commencer le Conbot Confiteor",condition=[EXCLUSIVE,ASPIRATION,ENCHANTEUR],use=MAGIE,range=AREA_CIRCLE_1,rejectEffect=[confiteorReady,holyCircleReady,holySpiritReady])
comboConfiteor = skill("Combo Confiteor",confiteor.id,TYPE_DAMAGE,500,confiteor.power,condition=[EXCLUSIVE,ASPIRATION,ENCHANTEUR],become=[requiescat,espritSaint,cercleSacre,confiteor],area=AREA_CIRCLE_1,emoji=confiteor.emoji,description="Vous permet d'effectuer le Combot Confiteor.\n{0} __{1}__, {2} __{3}__ et {4} __{5}__ vous soigne également d'une puissance de **{6}** en utilisant la statistique d'action de dégâts directs.\n{2} __{3}__ se lance sur soi-même.".format(espritSaint.emoji,espritSaint.name,cercleSacre.emoji,cercleSacre.name,confiteor.emoji,confiteor.name,40),use=MAGIE)

for skilly in [confiteor,cercleSacre,espritSaint]:
    skilly.condition, skilly.effectAroundCaster, skilly.useActionStats, skilly.use = [EXCLUSIVE,ASPIRATION,ENCHANTEUR], [TYPE_HEAL,AREA_MONO,40], ACT_DIRECT, MAGIE

horoSkills = [belierCharge,taureauFury,gemeauSyn,cancerAssault,lionRoar,vierge,balanceBoost,scorpionByte,sagArrow,capricorne,verseau,fishGrace]


focusJauge = effect("Jauge Focus","focusJauge",emoji='<:reasable:983595291930415124>',turnInit=-1,unclearable=True)
focusJauge.jaugeValue = jaugeValue(
    emoji=lysJauge.jaugeValue.emoji,
    conds=[
        jaugeConds(INC_START_TURN,5),
        jaugeConds(INC_ON_SELF_CRIT,15)
    ]
)

hyperchargent = effect("Déchargé","hyperchargen't",turnInit=5,type=TYPE_MALUS,silent=True,emoji='<:uncharged:1007588186165346356>')
fakedechargeEff = effect("Enchaînement - Décharge de Gausse","enchDechGausse",emoji='<:gausse:1003645652313575516>',silent=True)
dechargeGausse = skill("Décharge de Gausse",getAutoId(comboConfiteor.id,True),TYPE_DAMAGE,power=40,use=PRECISION,emoji="<:gausse:1003645652313575516>",needEffect=[fakedechargeEff],cooldown=0,description="Inflige des dégâts *Précision* à l'ennemi ciblé",jaugeEff=focusJauge)
fakedechargeEff.replica = dechargeGausse
cryoExplosionReady = effect("Cryo-Explosion Préparée","cryoExploReady",stackable=True,turnInit=3,emoji='<:cryoexplo:1003645574647660605>')
cryoExplosion = skill("Cryo-Explosion",dechargeGausse.id,TYPE_DAMAGE,power=70,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],emoji='<:cryoexplo:1003645574647660605>',effectOnSelf=fakedechargeEff,replay=True,needEffect=[cryoExplosionReady],cooldown=0,description="Inflige des dégâts Eau *Force* à l'ennemi ciblé et enchaîne directement avec {0} __{1}__ en ciblant ce même ennemi".format(dechargeGausse.emoji,dechargeGausse.name),jaugeEff=focusJauge)
cryoExplosionReady.description = "Permet d'utiliser la compétence {0} __{1}__".format(cryoExplosion.emoji,cryoExplosion.name)
cryoChargeEff = copy.deepcopy(dmgUp)
cryoChargeEff.power, cryoChargeEff.turnInit = 10, 3
cryoCharge = skill("Cryo-Charge",dechargeGausse.id,TYPE_BOOST,range=AREA_MONO,cooldown=0,replay=True,jaugeEff=focusJauge,minJaugeValue=35,maxJaugeValue=35,effects=[cryoChargeEff,cryoExplosionReady,cryoExplosionReady,cryoExplosionReady],effectOnSelf=hyperchargent,rejectEffect=[hyperchargent],description="Augmente vos dégâts infligés de **{0}%** durant 3 tours et vous octroi 3 effets {1} __{2}__ sur la même durée".format(cryoChargeEff.power,cryoExplosionReady.emoji[0][0],cryoExplosionReady.name),emoji='<:icecharge:1003645528468373565>')
cryoChargeBundle = skill("Cryo-Hypercharge",dechargeGausse.id,TYPE_DAMAGE,750,power=cryoExplosion.power+dechargeGausse.power,become=[cryoCharge,cryoExplosion,dechargeGausse],jaugeEff=focusJauge,emoji=cryoCharge.emoji,description="{0} __{1}__ :\n{2}\nUtiliser __{1}__ coûte {9} pts de {10} __{11}__\n\n{3} __{4}__ :\n{5}\n__{4}__ est considérée comme une compétence Eau\n\n{6} __{7}__ :\n{8}".format(cryoCharge.emoji, cryoCharge.name, cryoCharge.description, cryoExplosion.emoji, cryoExplosion.name, cryoExplosion.description, dechargeGausse.emoji, dechargeGausse.name, dechargeGausse.description, cryoCharge.minJaugeValue, focusJauge.emoji[0][0], focusJauge.name),condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER])

ricochetReady = effect("Enchaînement - Ricochet","enchDechGausse",emoji='<:ricochet:1003645701839933520>',silent=True)
ricochet = skill("Ricochet",getAutoId(cryoChargeBundle.id,True),TYPE_DAMAGE,power=30,area=AREA_CIRCLE_1,jaugeEff=focusJauge,use=PRECISION,emoji="<:ricochet:1003645701839933520>",needEffect=[ricochetReady],cooldown=0,description="Inflige des dégâts *Précision* à l'ennemi ciblé")
ricochetReady.replica = ricochet
pyroArbaReady = effect("Pyro-Arbalette Préparée","pyroArbaready",stackable=True,turnInit=3,emoji='<:arbalte:1003645679450738770>')
pyroArba = skill("Pyro-Arbalette",ricochet.id,TYPE_DAMAGE,power=60,jaugeEff=focusJauge,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],area=AREA_CONE_2,emoji='<:arbalte:1003645679450738770>',effectOnSelf=ricochetReady,replay=True,needEffect=[pyroArbaReady],cooldown=0,description="Inflige des dégâts Eau *Force* à l'ennemi ciblé et enchaîne directement avec {0} __{1}__ en ciblant ce même ennemi".format(ricochet.emoji,ricochet.name))
pyroArbaReady.description = "Permet d'utiliser la compétence {0} __{1}__".format(pyroArba.emoji,pyroArba.name)
pyroCharge = skill("Pyro-Charge",ricochet.id,TYPE_BOOST,range=AREA_MONO,cooldown=0,replay=True,jaugeEff=focusJauge,minJaugeValue=35,maxJaugeValue=35,effects=[cryoChargeEff,pyroArbaReady,pyroArbaReady,pyroArbaReady],effectOnSelf=hyperchargent,rejectEffect=[hyperchargent],description="Augmente vos dégâts infligés de **{0}%** durant 3 tours et vous octroi 3 effets {1} __{2}__ sur la même durée".format(cryoChargeEff.power,pyroArbaReady.emoji[0][0],pyroArbaReady.name),emoji='<:firecharge:1003645503709388860>')
pyroChargeBundle = skill("Pyro-Hypercharge",ricochet.id,TYPE_DAMAGE,750,power=pyroArba.power+ricochet.power,become=[pyroCharge,pyroArba,ricochet],jaugeEff=focusJauge,emoji=pyroCharge.emoji,description="{0} __{1}__ :\n{2}\nUtiliser __{1}__ coûte {9} pts de {10} __{11}__\n\n{3} __{4}__ :\n{5}\n__{4}__ est considérée comme une compétence Feu\n\n{6} __{7}__ :\n{8}".format(pyroCharge.emoji, pyroCharge.name, pyroCharge.description, pyroArba.emoji, pyroArba.name, pyroArba.description, ricochet.emoji, ricochet.name, ricochet.description, pyroCharge.minJaugeValue, focusJauge.emoji[0][0], focusJauge.name),condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE])

drill = skill("Foreuse",getAutoId(pyroChargeBundle.id,True),TYPE_DAMAGE,750,power=125,jaugeEff=focusJauge,minJaugeValue=40,maxJaugeValue=40,percing=35,description="Inflige des dégâts à l'ennemi ciblé en ignorant **35%** de sa résistance",emoji='<:drill:1003645776876015626>',cooldown=3)
anchorEff = copy.deepcopy(chained)
anchorEff.turnInit = 3
anchor = skill("Ancre Aérienne",getAutoId(drill.id,True),TYPE_DAMAGE,750,power=125,jaugeEff=focusJauge,minJaugeValue=50,maxJaugeValue=50,effects=anchorEff,description="Inflige des dégâts à l'ennemi ciblé et restrain ses déplacements pendant 3 tours",emoji='<:anchor:1003645801421099018>',cooldown=3)
chainsaw = skill("Tronçonneuse Rotatives",getAutoId(anchor.id,True),TYPE_DAMAGE,750,power=125,jaugeEff=focusJauge,minJaugeValue=60,maxJaugeValue=60,area=AREA_LINE_3,description="Inflige des dégâts aux ennemis ciblés",cooldown=3,emoji="<:tronc:1003645821826371684>")
mysticShot = skill("Fusil Mystique",getAutoId(chainsaw.id,True),TYPE_DAMAGE,750,power=150,maxPower=200,jaugeEff=focusJauge,minJaugeValue=50,url="https://media.discordapp.net/attachments/1006418796329848954/1007574358983704646/20220812_105247.gif",maxJaugeValue=100,ultimate=True,cooldown=5,description="Inflige des dégâts à l'ennemi ciblé. La puissance augmente en fonction de la quantité de jauge consommée",emoji="<:fusil:1003646584497655839>")

bestSkill = skill("Best Skill","bestSkill",TYPE_DAMAGE,0,999,emoji='<a:giveup:902383022354079814>',description="Omae wa mou shinderu")

tablAdvBaseElemSkills, baseAoEElemSkills, baseMonoElemSkills = [], [flameche,flame,pyro,brise,storm2,tornado,space1,space2,space3,light1,light2,light3,neutralZone1,neutralZone2,neutralZone3], [ecume,courant,torant,stone,rock,mont,time1,time2,time3,dark1,dark2,dark3,neutralMono1,neutralMono2,neutralMono3]
for skilly in baseAoEElemSkills:
    tempSkilly = copy.deepcopy(skilly)
    tempSkilly.area, tempSkilly.power, tempSkilly.name = AREA_MONO, tempSkilly.power + [0,0,10,0,15,0,20][tempSkilly.cooldown-1], "Extra " +tempSkilly.name
    tablAdvBaseElemSkills.append(tempSkilly)

for skilly in baseMonoElemSkills:
    tempSkilly = copy.deepcopy(skilly)
    tempSkilly.area, tempSkilly.power, tempSkilly.name = AREA_CIRCLE_1, tempSkilly.power - [0,0,10,0,15,0,20][tempSkilly.cooldown-1], "Extra " +tempSkilly.name
    tablAdvBaseElemSkills.append(tempSkilly)

tablAdvBaseElemSkillsId = getArrayAutoId(mysticShot.id,len(tablAdvBaseElemSkills),True)
for cmpt in range(len(tablAdvBaseElemSkills)):
    tablAdvBaseElemSkills[cmpt].id = tablAdvBaseElemSkillsId[cmpt]

lowBlow = skill("Coup Bas",getAutoId(tablAdvBaseElemSkills[-1].id,True),TYPE_DAMAGE,750,power=45,range=AREA_CIRCLE_2,use=ENDURANCE,effects=lightStun,cooldown=5,maxPower=75,description="Inflige des dégâts et étourdi l'ennemi ciblé.\nLa puissance de la compétence est augmentée contre un boss Stand Alone, un boss de Raid ou certains ennemis",emoji='<:lowblow:1005127208412651591>')
legStrike = skill("Fauchage de Jambes",getAutoId(lowBlow.id,True),TYPE_DAMAGE,750,80,AREA_CIRCLE_2,effects=lightStun,cooldown=7,description="Inflige des dégâts à étourdi l'ennemi ciblé",emoji='<:legsStrike:1005127243401539645>')
provokeEff = effect("Provocation","voke",emoji='<:voke:1005127164749959178>',type=TYPE_MALUS,description="Augmente considérablement l'aggressivité du porteur envers l'entity à l'origine de cet effet")
provoke = skill("Provocation",getAutoId(legStrike.id,True),TYPE_MALUS,500,effects=provokeEff,cooldown=5,pull=4,range=AREA_CIRCLE_4,description="Augmente considérablement la probabilité d'être ciblé par l'adversaire désigné et attire celui-ci vers vous",emoji=provokeEff.emoji[0][0])

fanRevolEff = effect("Poussé Céleste","fanRevolEff",CHARISMA,strength=10,agility=5,turnInit=3)
fanRevolReady = effect("Eventails Célestes préparés","fanRevolReady",silent=True,turnInit=5,emoji='<:celestianFans:1003313557242388622>')
fanRevol = skill("Eventails Célestes",getAutoId(provoke.id,True),TYPE_DAMAGE,power=125,area=AREA_CIRCLE_3,cooldown=5,range=AREA_MONO,emoji='<:celestianFans:1003313557242388622>',effectAroundCaster=[TYPE_BOOST,AREA_DONUT_3,fanRevolEff],description="Inflige des dégâts aux ennemis alentours et augmente la Force et l'Agilité des alliés dans la zone d'effet",needEffect=[fanRevolReady])
fanAscendEff = effect("Poussé Ascendante","fanRevolEff2",CHARISMA,strength=5,agility=3,magie=3,turnInit=3)
fanAscendReady = effect("Eventails Ascendants","fanAscendReady",silent=True,turnInit=5,emoji='<:ascFan:1003308417034768444>')
fanAscend = skill("Eventails Ascendants",fanRevol.id,TYPE_DAMAGE,power=110,emoji='<:ascFan:1003308417034768444>',effectOnSelf=fanRevolReady,needEffect=[fanAscendReady],effectAroundCaster=[TYPE_BOOST,AREA_DONUT_2,fanAscendEff])
fanReverseReady = effect("Eventail Virvoltant Inversé Préparé","fanReverseReady",silent=True,turnInit=5,emoji='<:revFlyingFan:1003309639280111647>')
fanReverse = skill("Eventail Virvoltant Inversé",fanRevol.id,TYPE_DAMAGE,power=95,area=AREA_ARC_3,emoji='<:revFlyingFan:1003309639280111647>',needEffect=[fanReverseReady],effectOnSelf=fanAscendReady)
fanVir = skill("Eventail Virvoltant",fanRevol.id,TYPE_DAMAGE,power=80,area=AREA_ARC_2,emoji='<:flyingFan:1003309655444963408>',effectOnSelf=fanReverseReady)
comboFanCelest = skill("Combo Eventails Célestes",fanRevol.id,TYPE_DAMAGE,750,become=[fanVir,fanReverse,fanAscend,fanRevol],emoji=fanRevol.emoji,description="Effectue le Combo Eventails Célestes. Le dernier coup augmente la force et l'agilité des alliés alentours (Charisme)")
demonLandEff1, demonLandEff2 = copy.deepcopy(dmgUp), copy.deepcopy(defenseUp)
demonLandEff1.power = demonLandEff2.power = 7.5
demonLandEff1.stat = demonLandEff2.stat = INTELLIGENCE
demonLandEff1.turnInit = demonLandEff2.turnInit = 3
demonLand = skill("Terre Démoniaque",getAutoId(comboFanCelest.id,True),TYPE_BOOST,500,cooldown=7,effects=[demonLandEff1,demonLandEff2],area=AREA_DONUT_3,range=AREA_MONO,group=SKILL_GROUP_DEMON,hpCost=20,emoji='<:dmonland:1006455391342829599>')
demonArmorEff = effect("Armure Démoniaque","demonArmor",INTELLIGENCE,overhealth=70,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji='<:dmonArmor:1006455374464946226>')
demonArmor = skill("Armure Démoniaque",getAutoId(demonLand.id,True),TYPE_ARMOR,750,effects=demonArmorEff,cooldown=5,group=SKILL_GROUP_DEMON,hpCost=10,emoji='<:dmonArmor:1006455374464946226>')
demonArmorEff2 = effect("Armure Démoniaque Étendue","demonArmor2",INTELLIGENCE,overhealth=50,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji='<:dmonArmor:1006455374464946226>')
demonArmor2 = skill("Armure Démoniaque Étendue",getAutoId(demonArmor.id,True),TYPE_ARMOR,750,effects=demonArmorEff,cooldown=5,group=SKILL_GROUP_DEMON,hpCost=15,area=AREA_CIRCLE_3,range=AREA_MONO,emoji='<:dmonArmor:1006455374464946226>')
demonConstEff = copy.deepcopy(absEff)
demonConstEff.power, demonConstEff.turnInit = 20, 3
demonConst = skill("Constitution Démoniaque",getAutoId(demonArmor2.id,True),TYPE_BOOST,500,area=AREA_CIRCLE_3,range=AREA_MONO,effects=demonConstEff,cooldown=5,group=SKILL_GROUP_DEMON,hpCost=10,emoji='<:dmonConst:1006455408250081310>')

soulJauge = effect("Jauge d'Âme","soulJauge",emoji='<:soulJauge:983595647292829716>',turnInit=-1,unclearable=True)
soulJauge.jaugeValue = jaugeValue(
    emoji=[["<:lej:980923743960461412>","<:mej:980923762016927764>","<:rej:980923786650075228>"],["<:sjl:983600118152441886>","<:sjm:983600154252808202>","<:sjr:983600136125022248>"]],
    conds=[
        jaugeConds(INC_START_TURN,5),
        jaugeConds(INC_ENEMY_KILLED,15),
        jaugeConds(INC_ALLY_KILLED,5)
    ]
)
noneLem = effect("Repos du Néan","noneLem",silent=True,turnInit=7,type=TYPE_MALUS,emoji='<:noneLem:1007588165512593431>',description="Empêche l'utilisation de Linceuil de Lémure durant sa durée")
comunioReady = effect("Linceuil de Lémure","comunioReady",turnInit=3,emoji='<:linc:1007583748491051058>')
comunio = skill("Communio",getAutoId(demonConst.id,True),TYPE_DAMAGE,power=125,area=AREA_CIRCLE_1,range=AREA_CIRCLE_3,emoji='<:comunio:1007583832947568740>',needEffect=comunioReady)
soulFauchCroixReady = effect("Fauchage Croisé Préparé","soulFaucCroixReady",turnInit=3,emoji="<:faucheCroix:937807152058343474>")
soulFauchCroix = skill("Fauchage Croisé",comunio.id,TYPE_DAMAGE,power=110,range=AREA_CIRCLE_3,area=AREA_ARC_2,accuracy=99,emoji="<:faucheCroix:937807152058343474>",needEffect=soulFauchCroixReady)
soulFauchNeanReady = effect("Fauchage du Néan Préparé","soulFauchNean",turnInit=3,emoji='<:faucheNean:937807137306976337>')
soulFauchNean = skill("Fauchage du Néan",comunio.id,TYPE_DAMAGE,power=100,range=AREA_CIRCLE_3,area=AREA_ARC_1,accuracy=120,emoji="<:faucheNean:937807137306976337>",needEffect=soulFauchNeanReady,effectOnSelf=soulFauchCroixReady)
tranchNeanReady = effect("Tranchage du Néan préparé","trancNeanReady",turnInit=3,emoji='<:tranch:1007583800135524442>')
tranchNean = skill("Tranchage du Néan",comunio.id,TYPE_DAMAGE,cooldown=0,emoji='<:tranch:1007583800135524442>',range=AREA_CIRCLE_3,needEffect=tranchNeanReady,replay=True,tpCac=True,power=50,description="Vous téléporte au corps à corps de l'ennemi ciblé, lui inflige des dégâts et vous permet de rejouer votre tour")
lincEff = copy.deepcopy(dmgUp)
lincEff.power, lincEff.turnInit = 25, 4
linceuilLemure = skill("Linceuil de Lémure",comunio.id,TYPE_BOOST,range=AREA_MONO,url='https://media.discordapp.net/attachments/1003025632415973510/1007612026585092148/20220812_132659.gif',cooldown=0,area=AREA_MONO,emoji='<:linc:1007583748491051058>',effects=[lincEff,comunioReady,soulFauchNeanReady,tranchNeanReady,noneLem],rejectEffect=noneLem,jaugeEff=soulJauge,minJaugeValue=35,maxJaugeValue=35,description="Consomme une partie de votre jauge d'âme pour augmenter vos dégâts infligés de 10% pendant 3 tours et vous permet d'effectuer plusieurs nouvelles compétences sur la même durée")
bundleLemure = skill("Linceuil de Lémure",linceuilLemure.id,TYPE_DAMAGE,750,url='https://media.discordapp.net/attachments/1003025632415973510/1007612026585092148/20220812_132659.gif',emoji='<:linc:1007583748491051058>',jaugeEff=soulJauge,power=comunio.power,become=[linceuilLemure,tranchNean,soulFauchNean,soulFauchCroix,comunio],description="Permet d'utiliser {0} __{1}__ en utilisant {2} pts de votre {3} __{4}__, augmentant vos dégâts infligés et vous permettant d'utiliser diverses compétences pendant 3 tours".format(linceuilLemure.emoji,linceuilLemure.name,linceuilLemure.minJaugeValue,linceuilLemure.jaugeEff.emoji[0][0],linceuilLemure.jaugeEff.name),minJaugeValue=linceuilLemure.minJaugeValue)
moissoneur = skill("Moissoneur d'Âmes",getAutoId(bundleLemure.id,True),TYPE_DAMAGE,500,125,range=AREA_MONO,emoji='<:soulMois:1007600776337694781>',area=AREA_CIRCLE_2,use=MAGIE,cooldown=5,jaugeEff=soulJauge,minJaugeValue=30,maxJaugeValue=45,maxPower=150)
corruptBecon = skill("Balise Corrompue",getAutoId(moissoneur.id,True),TYPE_DAMAGE,500,emoji='<:corruptBcon:1007601099622076486>',power=75,range=AREA_INLINE_5,area=AREA_LINE_5,jaugeEff=soulJauge,minJaugeValue=20,maxJaugeValue=50,maxPower=135,cooldown=5,use=MAGIE)
soulPendant = skill("Amulette d'Âmes",getAutoId(corruptBecon.id,True),TYPE_HEAL,500,use=CHARISMA,emoji='<:soulEater:1007600800576589884>',power=65,maxPower=80,jaugeEff=soulJauge,minJaugeValue=20,maxJaugeValue=35,cooldown=5)

potSuplReady = effect("Potence Suppliante Préparée","potSuplReady",turnInit=6,emoji='<:supPot:1007583690794221588>')
potSupl = skill("Potence Suppliante",getAutoId(soulPendant.id,True),TYPE_DAMAGE,range=AREA_CIRCLE_3,power=60,replay=True,needEffect=potSuplReady,emoji='<:supPot:1007583690794221588>',cooldown=3,jaugeEff=soulJauge,minJaugeValue=10,maxJaugeValue=10)
gibSuplReady = effect("Gibet Suppliant Préparé","gibSplReady",turnInit=6,emoji='<:supGibet:1007583627028221993>')
gibSupl = skill("Gibet Suppliant",potSupl.id,TYPE_DAMAGE,power=50,replay=True,range=AREA_CIRCLE_3,needEffect=gibSuplReady,emoji='<:supGibet:1007583627028221993>',effectOnSelf=potSuplReady,cooldown=3,jaugeEff=soulJauge,minJaugeValue=10,maxJaugeValue=10)
fetuSang = skill("Fétu Sanglant",gibSupl.id,TYPE_DAMAGE,power=40,replay=True,cooldown=3,range=AREA_CIRCLE_3,rejectEffect=[potSuplReady,gibSuplReady],effectOnSelf=gibSuplReady,emoji='<:fetu:1007583554319962112>',jaugeEff=soulJauge,minJaugeValue=10,maxJaugeValue=10)
bundleFetu = skill("Fétu Suppliant",gibSupl.id,TYPE_DAMAGE,500,potSupl.power,range=AREA_CIRCLE_3,emoji=fetuSang.emoji,become=[fetuSang,gibSupl,potSupl],description="Chaque compétence de Fétu Suppliant consomment **{0} pts** de votre {1} __{2}__ et permettent de rejouer votre tour après avoir infligé leurs dégâts".format(potSupl.minJaugeValue,soulJauge.emoji[0][0],soulJauge.name),jaugeEff=soulJauge,minJaugeValue=potSupl.minJaugeValue)
convictionVigilantEff = effect("Conviction du Vigilant","convVigil",CHARISMA,power=35,type=TYPE_INDIRECT_HEAL,unclearable=True,turnInit=-1,description="Lorsque le porteur utilise son arme ou une compétence de dégâts directs, le soigne légèrement",emoji="<:regenVigil:982210651353137153>")
convictionVigilante = skill("Conviction du Vigilant",getAutoId(bundleFetu.id,True),TYPE_PASSIVE,500,effectOnSelf=convictionVigilantEff,emoji='<:regenVigil:982210651353137153>',quickDesc="Vous soigne légèrement lorsque vous utilisez une option offensive",condition=[EXCLUSIVE,ASPIRATION,VIGILANT])
convictionProtecArmor = effect("Armure","convicProAmor",INTELLIGENCE,overhealth=35,stackable=True,lightShield=True,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
convicProEff = effect("Conviction du Protecteur","convicPro",INTELLIGENCE,emoji='<:convicPro:1089710483990388756>',callOnTrigger=convictionProtecArmor,turnInit=-1,unclearable=True,description="Octroi une armure légère au porteur lorsque celui-ci utilise son arme ou une compétence de dégâts direct")
convicPro = skill("Conviction du Protecteur",getAutoId(convictionVigilante.id,True),TYPE_PASSIVE,price=500,effectOnSelf=convicProEff,emoji=convicProEff.emoji[0][0],condition=[EXCLUSIVE,ASPIRATION,PROTECTEUR],quickDesc="Vous octroi une armure quand vous utiliser votre arme ou une compétence offensive")
convictEnchtEff = effect("Conviction de l'Enchanteur","convVigil",MAGIE,power=50,type=TYPE_INDIRECT_HEAL,unclearable=True,turnInit=-1,description="Lorsque le porteur utilise son arme ou une compétence de dégâts directs, le soigne légèrement",emoji="<:enchantConvic:1066018568136818759>")
convictEncht = skill("Conviction de l'Enchanteur",getAutoId(convicPro.id,True),TYPE_PASSIVE,500,effectOnSelf=convictEnchtEff,emoji='<:enchantConvic:1066018568136818759>',quickDesc="Vous soigne légèrement lorsque vous utilisez une option offensive",condition=[EXCLUSIVE,ASPIRATION,ENCHANTEUR])
convictTeteArmor = effect("Armure","convicTetAmor",STRENGTH,overhealth=35,stackable=True,lightShield=True,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji='<:idoOHArmor:909278702783836170>')
convictTetEff = effect("Conviction du Tête Brulée","convicPro",STRENGTH,callOnTrigger=convictTeteArmor,turnInit=-1,unclearable=True,emoji='<:tetebruleConvic:1066010806635995146>',description="Octroi une armure légère au porteur lorsque celui-ci utilise son arme ou une compétence de dégâts direct")
convictTet = skill("Conviction du Tête Brulée",getAutoId(convictEncht.id,True),TYPE_PASSIVE,500,effectOnSelf=convictTetEff,emoji=convictTetEff.emoji[0][0],condition=[EXCLUSIVE,ASPIRATION,TETE_BRULE],quickDesc="Vous octroi une armure quand vous utiliser votre arme ou une compétence offensive")

megaDark1Eff = effect("Méga Cécité","megaCeci",MAGIE,power=30,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,emoji=dark1.emoji,trigger=TRIGGER_START_OF_TURN)
megaDark2Eff = effect("Méga Obscurité","megaObs",MAGIE,power=37,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,emoji=dark2.emoji,trigger=TRIGGER_START_OF_TURN)
megaDark3Eff = effect("Méga Pénombre","megaPen",MAGIE,power=45,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,emoji=dark3.emoji,trigger=TRIGGER_START_OF_TURN)
gigaDark1Eff = effect("Giga Cécité","gigaCeci",MAGIE,power=25,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,emoji=dark1.emoji,trigger=TRIGGER_START_OF_TURN)
gigaDark2Eff = effect("Giga Obscurité","gigaObs",MAGIE,power=30,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,emoji=dark2.emoji,trigger=TRIGGER_START_OF_TURN)
gigaDark3Eff = effect("Giga Pénombre","gigaPen",MAGIE,power=35,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,emoji=dark3.emoji,trigger=TRIGGER_START_OF_TURN)
megaDark1 = skill("Méga Cécité",getAutoId(convictTet.id,True),TYPE_INDIRECT_DAMAGE,dark1.price,effects=megaDark1Eff,emoji=dark1.emoji,cooldown=dark1.cooldown,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS])
megaDark2 = skill("Méga Obscurité",getAutoId(megaDark1.id,True),TYPE_INDIRECT_DAMAGE,dark2.price,effects=megaDark2Eff,emoji=dark2.emoji,cooldown=dark2.cooldown,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS])
megaDark3 = skill("Méga Pénombre",getAutoId(megaDark2.id,True),TYPE_INDIRECT_DAMAGE,dark3.price,effects=megaDark3Eff,emoji=dark3.emoji,cooldown=dark3.cooldown,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS])
gigaDark1 = skill("Giga Cécité",getAutoId(megaDark3.id,True),TYPE_INDIRECT_DAMAGE,dark1.price,effects=gigaDark1Eff,emoji=dark1.emoji,cooldown=dark1.cooldown,area=AREA_CIRCLE_1,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS])
gigaDark2 = skill("Giga Obscurité",getAutoId(gigaDark1.id,True),TYPE_INDIRECT_DAMAGE,dark2.price,effects=gigaDark2Eff,emoji=dark2.emoji,cooldown=dark2.cooldown,area=AREA_CIRCLE_1,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS])
gigaDark3 = skill("Giga Pénombre",getAutoId(gigaDark2.id,True),TYPE_INDIRECT_DAMAGE,dark3.price,effects=gigaDark3Eff,emoji=dark3.emoji,cooldown=dark3.cooldown,area=AREA_CIRCLE_1,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS])
megaLight1 = skill("Méga {0}".format(light1.name),getAutoId(gigaDark3.id,True),TYPE_HEAL,light1.price,power=50,cooldown=light1.cooldown,emoji=light1.emoji,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
megaLight2 = skill("Méga {0}".format(light2.name),getAutoId(megaLight1.id,True),TYPE_HEAL,light2.price,power=65,cooldown=light2.cooldown,emoji=light2.emoji,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
megaLight3 = skill("Méga {0}".format(light3.name),getAutoId(megaLight2.id,True),TYPE_HEAL,light3.price,power=80,cooldown=light3.cooldown,emoji=light3.emoji,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
gigaLight1Eff = effect("Giga {0}".format(light1.name),"giga{0}Armor".format(light1.name),INTELLIGENCE,overhealth=40,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
gigaLight2Eff = effect("Giga {0}".format(light2.name),"giga{0}Armor".format(light2.name),INTELLIGENCE,overhealth=55,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
gigaLight3Eff = effect("Giga {0}".format(light3.name),"giga{0}Armor".format(light3.name),INTELLIGENCE,overhealth=70,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
gigaLight1 = skill("Giga {0}".format(light1.name),getAutoId(megaLight3.id,True),TYPE_ARMOR,light1.price,effects=gigaLight1Eff,cooldown=light1.cooldown,emoji=light1.emoji,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
gigaLight2 = skill("Giga {0}".format(light2.name),getAutoId(gigaLight1.id,True),TYPE_ARMOR,light2.price,effects=gigaLight2Eff,cooldown=light2.cooldown,emoji=light2.emoji,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
gigaLight3 = skill("Giga {0}".format(light3.name),getAutoId(gigaLight2.id,True),TYPE_ARMOR,light3.price,effects=gigaLight3Eff,cooldown=light3.cooldown,emoji=light3.emoji,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])

