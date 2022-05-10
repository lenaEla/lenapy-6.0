from copy import deepcopy
from classes import *
from constantes import *

soupledown = skill("Choc Ténébreux","zz",TYPE_DAMAGE,500,150,range = AREA_INLINE_3,conditionType=["exclusive","aspiration",POIDS_PLUME],area = AREA_CIRCLE_2,sussess=150,tpCac=True,ultimate=True,cooldown=6,emoji='<:lunadown:932444767504203847>',use=STRENGTH)
inkarmor = skill("Armure d'Encre","zy",TYPE_ARMOR,250,ultimate=True,effect="la",emoji = '<:inkArmor:866829950463246346>',area=AREA_CIRCLE_2,cooldown=7,range=AREA_CIRCLE_5)
coffeeSkill = skill("SupréCafé","zx",TYPE_BOOST,500,effect=["lb"],use=CHARISMA,area=AREA_ALL_ALLIES,emoji='<:coffee:867538582846963753>',cooldown=4,message="{0} prend le café avec ses alliés :")
theSkill = skill("LiberThé","zw",TYPE_BOOST,500,effect=["lc"],use=CHARISMA,area=AREA_ALL_ALLIES,emoji='<:the:867538602644602931>',cooldown=4,message="{0} prend le thé avec ses alliés :")
gpotion = skill("Potion tonifiante","zv",TYPE_BOOST,250,emoji="<:bpotion:867165268911849522>",use=INTELLIGENCE,cooldown=3,effect="le",area=AREA_MONO,range=AREA_CIRCLE_3)
bpotion = skill("Potion étrange","zu",TYPE_MALUS,200,cooldown=3,effect="lf",emoji="<:dpotion:867165281617182760>",use=INTELLIGENCE,area=AREA_CIRCLE_1,message="{0} lance une {1} sur {2}")
zelian = skill("Chronoshift","zt",TYPE_INDIRECT_HEAL,500,cooldown=7,effect="lj",emoji='<:chronoshift:867872479719456799>',conditionType=["exclusive","element",ELEMENT_TIME])
courage = skill("Motivation","zs",TYPE_BOOST,500,emoji ='<:charge:866832551112081419>',area=AREA_CIRCLE_2,use=CHARISMA,effect="lk",cooldown=4,range=AREA_MONO)
nostalgia = skill("Nostalgie","zr",TYPE_MALUS,500,emoji='<:nostalgia:867162802783649802>',effect="lm",cooldown=4,use=INTELLIGENCE)
draw25 = skill("Stop attacking or draw 25","zq",TYPE_MALUS,300,25,emoji="<:draw25:869982277701103616>",use=None,effect="lq",cooldown = 3,area=AREA_ALL_ENEMIES,range=AREA_MONO,ultimate=True,conditionType=["exclusive","aspiration",SORCELER],message="{0} utilise sa carte joker !")
siropMenthe = skill("Menthalité","zp",TYPE_BOOST,500,effect=["lu"],use=CHARISMA,area=AREA_ALL_ALLIES,emoji='<:menthe:867538622797054042>',cooldown=4,message="{0} prend un sirop de menthe avec ses alliés :")
unHolly = skill("Truc pas catho","zo",TYPE_MALUS,69,emoji='<:bravotakei:877202258348113960>',cooldown=2,effect="lw",use=CHARISMA,message="{0} ||fait des trucs pas catho à destination de|| {2} :",group=SKILL_GROUP_DEMON)
chaos = skill("Chaos Chaos !","zn",TYPE_UNIQUE,1000,range=AREA_MONO,area=AREA_ALL_ENTITES,sussess=200,emoji='<a:CHAOS:762276118224961556>',cooldown=5,ultimate=True,use=None,message="PLEASE ! JUST A SIMPLE CHAOS !")
contrecoup = skill("Contre-coup","zm",TYPE_INDIRECT_DAMAGE,250,effect="ln",cooldown=2,emoji='<:aftershock:882889694269038592>',use=MAGIE)
boom = skill("Réaction en chaîne","zl",TYPE_INDIRECT_DAMAGE,250,effect="lv",cooldown=3,emoji='<:bimbamboum:873698494874017812>',use=MAGIE)
balayette = skill("Baleyette","zk",TYPE_DAMAGE,100,70,range=AREA_MONO,area=AREA_CIRCLE_1,emoji='<:baleyette:873924668963291147>',cooldown=2,setAoEDamge=True)
firstheal = skill("Premiers secours","zj",TYPE_HEAL,100,40,emoji="<:bandage:873542442484396073>")
cure = skill("Guérison","zi",TYPE_HEAL,250,80,cooldown=5,emoji='<:cure:925190515845132341>')
lightAura = skill("Aura de Lumière I","zh",TYPE_PASSIVE,250,effectOnSelf="ly",emoji="<:AdL:873548073769533470>")
splatbomb = skill("Bombe splash","zg",TYPE_DAMAGE,100,cooldown=4,area=AREA_CIRCLE_1,power=87,emoji='<:splatbomb:873527088286687272>',message="{0} lance une {1} sur {2} :")
explosionSilentEff = copy.deepcopy(silenceEff)
explosionSilentEff.turnInit = 4
explosion = skill("Explosion","KBOOM",TYPE_DAMAGE,1000,power=300,percing=0,ultimate=True,cooldown=12,area=AREA_CIRCLE_2,shareCooldown=True,effectOnSelf=explosionSilentEff,use=MAGIE,emoji='<a:explosion:882627170944573471>',damageOnArmor=0.8,url='https://media.discordapp.net/attachments/933783831272628356/934066959040016404/20220121_134758.gif',description="Inflige des dégâts colosaux dans une grande zone")
explosionCast = skill("Explosion","zf",TYPE_DAMAGE,1000,0,ultimate=True,cooldown=7,area=AREA_CIRCLE_2,sussess=0,shareCooldown=True,effectOnSelf="na",use=MAGIE,emoji='<a:explosion:882627170944573471>',message="{0} rassemble son mana...")
protect = skill("Orbe défensif","ze",TYPE_ARMOR,200,emoji='<:orbeDef:873725544427053076>',effect="md",cooldown=3)
poisonus = skill("Vent empoisonné","zd",TYPE_INDIRECT_DAMAGE,500,emoji='<:estabistia:883123793730609172>',effect="me",cooldown=3,area=AREA_CIRCLE_1,use=MAGIE,message="{0} propage un {1} autour de {2} :",effPowerPurcent=55)
invocBat = skill("Invocation - Chauve-souris","zc",TYPE_SUMMON,500,invocation="Chauve-Souris",emoji="<:cutybat:884899538685530163>",shareCooldown=True,use=AGILITY)
multiMissiles = skill("Multi-Missiles","zb",TYPE_INDIRECT_DAMAGE,750,range=AREA_MONO,ultimate=True,emoji='<:tentamissile:884757344397951026>',effect="mf",cooldown=4,area=AREA_RANDOMENNEMI_5,url='https://cdn.discordapp.com/attachments/935769576808013837/935781565663948850/20220126_071157.gif')
monoMissiles = skill("Mono-Missiles","za",TYPE_INDIRECT_DAMAGE,250,range=AREA_CIRCLE_7,emoji='<:monomissile:884757360193708052>',effect="mf",cooldown=4)
classicSplashdown = skill("Choc Chromatique Classique","yz",TYPE_DAMAGE,500,150,AREA_MONO,ultimate=True,emoji='<:splashdown:884803808402735164>',cooldown=5,area=AREA_CIRCLE_2,damageOnArmor=3,url="https://cdn.discordapp.com/attachments/935769576808013837/935781564661526578/20220126_071756.gif")
invocCarbE = skill("Invocation - Carbuncle Emeraude","yy",TYPE_SUMMON,500,invocation="Carbuncle Emeraude",emoji="<:invoncEm:919857931158171659>",cooldown=3,range=AREA_CIRCLE_3,shareCooldown=True,use=MAGIE)
invocCarbT = skill("Invocation - Carbuncle Topaze","yx",TYPE_SUMMON,500,invocation="Carbuncle Topaze",emoji="<:invocTopaz:919859538943946793>",cooldown=3,range=AREA_CIRCLE_3,shareCooldown=True,use=ENDURANCE)
invocFee = skill("Invocation - Fée Soignante","yw",TYPE_SUMMON,500,0,AREA_CIRCLE_3,cooldown=4,invocation="Fée soignante",emoji="<:selene:885077160862318602>",shareCooldown=True,use=CHARISMA)
thinkSkill = skill("Réfléchis !","yv",TYPE_BOOST,250,0,emoji="<:think:885240853696765963>",effect="mh",use=CHARISMA,cooldown = 3)
descart = skill("Nous pensons donc nous somme","yu",TYPE_BOOST,250,range=AREA_MONO,area=AREA_CIRCLE_1,emoji="<:descartes:885240392860188672>",effect='mi',cooldown=4,use=None,message="{0} a trouvé le sens de la vie !")
trans = skill("Transcendance","lb",TYPE_UNIQUE,0,initCooldown=3,cooldown=5,emoji="<:limiteBreak:886657642553032824>",description="Un sort particulier qui a un effet différent en fonction de l'aspiration du lanceur\n\nUtiliser Transcendance vous empêche d'utiliser une compétence ultime lors du prochain tour",use=HARMONIE,shareCooldown=True)
transBerserk = copy.deepcopy(trans)
transBerserk.type,transBerserk.power, transBerserk.name = TYPE_DAMAGE,220, transBerserk.name + " - Frappe transcendique"
transPoidsPlume = copy.deepcopy(transBerserk)
transPoidsPlume.knockback = 5
transTetBrule = copy.deepcopy(transBerserk)
transTetBrule.erosion = 35
transBerserk.lifeSteal = 35
transObs = copy.deepcopy(trans)

transObs.type,transObs.power,transObs.area, transObs.name = TYPE_DAMAGE,200,AREA_LINE_6, transObs.name + " - Tir transcendique"
transAttentif = copy.deepcopy(transObs)
transObs.effectOnSelf = effect("Transcender ses limites","transObsEff",PRECISION,precision=10,strength=10,turnInit=3,emoji=sameSpeciesEmoji('<:lbBB:930780339947855882>','<:lbBR:930780304405327893>'),description="Augmente les statistiques de l'Observateur pendant 3 tours")
transAttentif.effectOnSelf = effect("Transcender ses limites","transTetEff",HARMONIE,magie=10,strength=10,turnInit=3,emoji=sameSpeciesEmoji('<:lbBB:930780339947855882>','<:lbBR:930780304405327893>'),description="Augmente les statistiques du Tête Brulée pendant 3 tours")
transMage = copy.deepcopy(trans)
transMage.type,transMage.power,transMage.area,transMage.name, transMage.cooldown = TYPE_DAMAGE,180,AREA_CIRCLE_2, transMage.name + " - Explosion transcendique", transMage.cooldown+1
transEnch = copy.deepcopy(transMage)
transMage.effect = [effect("Hypernova","transMagEff",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,area=AREA_CIRCLE_2,power=25,emoji=sameSpeciesEmoji('<:lbDB:930780352480436244>','<:lbDR:930780318699511850>'),description="Inflige des dégâts indirects supplémentaire autour de la cible initiale au début de son tour")]
transSorceler = copy.deepcopy(transMage)
transMage.power, transMage.effect = int(transMage.power * 1.1), [None]
transEnch.effectOnSelf = effect("Bouclier Transcendique","transEchShield",MAGIE,emoji=sameSpeciesEmoji("<a:transArmorB:900037831257358378>","<a:transArmorR:900037817449717800>"),type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,overhealth=100,description="Accorde une armure à l'Enchanteur")
transAlt = copy.deepcopy(trans)
transAlt.type,transAlt.power,transAlt.area,transAlt.range, transAlt.name, transAlt.cooldown, transAlt.effectAroundCaster = TYPE_HEAL,120,AREA_ALL_ALLIES,AREA_MONO, transAlt.name + " - Soins transcendiques",7, [TYPE_RESURECTION,AREA_CIRCLE_6,150]
transIdo = copy.deepcopy(trans)
transAlt.effect = [effect("Soins transcendique","transAltEff",CHARISMA,power=15,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji=sameSpeciesEmoji('<:lbHealB:933084435706953768>','<:lbHealR:933084448327606304>'),description="Soigne légèrement les alliés affectés au début de leur tour")]
transIdo.effect, transIdo.type, transIdo.effectAroundCaster, transIdo.range, transIdo.area, transIdo.name = [effect("Transcender ses limites","transIdoEff",HARMONIE,strength=15,magie=15,charisma=10,intelligence=10,turnInit=3,emoji=sameSpeciesEmoji('<:lbBB:930780339947855882>','<:lbBR:930780304405327893>'),description="Augmente les statistiques des alliés affectés pendant 3 tours")], TYPE_BOOST, [TYPE_RESURECTION,AREA_CIRCLE_6,100], AREA_MONO, AREA_CIRCLE_6, "Apothéose"
transInoEff = copy.deepcopy(defenseUp)
transInoEff.turnInit, transInoEff.power = 3, 15
transIno = copy.deepcopy(transIdo)
transIno.effect, transIno.effectAroundCaster, transIno.name = transIno.effect + [transInoEff], None, "Ultima Serum"
transPre = copy.deepcopy(trans)
transPro = copy.deepcopy(trans)
effTransPre = effect("Armure Transcendique","transArm",HARMONIE,strength=10,magie=10,overhealth=250,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji("<a:transArmorB:900037831257358378>","<a:transArmorR:900037817449717800>"),description="Donne une grosse armure et augmente les statistiques des alliés tant que celle-ci est active")
effTransPro = effect("Armure Transcendique","transArm",HARMONIE,resistance=5,overhealth=250,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji("<a:transArmorB:900037831257358378>","<a:transArmorR:900037817449717800>"),description="Donne une grosse armure et augmente la résistance des alliés tant que celle-ci est active")
transPre.type,transPre.area,transPre.range,transPre.effect,transPre.name, transPre.cooldown = TYPE_ARMOR,AREA_ALL_ALLIES,AREA_MONO,[effTransPre],transPre.name + " - Armure Transcendique",7
transPro.type,transPro.area,transPro.range,transPro.effect,transPro.name, transPro.cooldown = TYPE_ARMOR,AREA_ALL_ALLIES,AREA_MONO,[effTransPro],transPro.name + " - Armure Transcendique",7
transAtt = copy.deepcopy(transAlt)
transAtt.effectAroundCaster, transAtt.effect, transAtt.name = [TYPE_RESURECTION,AREA_ALL_ALLIES,int(transAtt.effectAroundCaster[2]*1.5)], [None], "Eclat de vie"

transTabl = [transBerserk, transObs, transPoidsPlume, transIdo, transPre, transTetBrule, transMage, transAlt, transEnch, transPro,transAtt,transSorceler,transIno,transAttentif]
burst = skill("Bombe ballon","ys",TYPE_DAMAGE,0,50,area=AREA_CIRCLE_1,sussess=70,emoji='<:burstBomb:887328853683474444>',use=HARMONIE,cooldown=2,setAoEDamge=True)
lapSkill = skill("Invocation - Lapino","yr",TYPE_SUMMON,0,invocation="Lapino",cooldown=4,shareCooldown=True,emoji='<:lapino:885899196836757527>',use=CHARISMA)
adrenaline = skill("Adrénaline","yq",TYPE_HEAL,250,cure.power,cooldown=5,emoji='<:adrenaline:887403480933863475>',use=INTELLIGENCE)
blindOnSelf = effect("Blindé","blindOnSelf",resistance=20,description="Réduit les degâts subis jusqu'à votre prochain tour")
blindage = skill("Blindage","yp",TYPE_BOOST,350,0,AREA_MONO,area=AREA_DONUT_2,effect="mj",cooldown=3,use=None,emoji="<:blindage:897635682367971338>",effectOnSelf=blindOnSelf)
secondWind = skill("Second Souffle","yo",TYPE_HEAL,350,350,AREA_MONO,emoji='<:secondWind:897634132639756310>',cooldown=99,use=ENDURANCE)
isolement = skill("Isolement","yn",TYPE_ARMOR,500,0,AREA_MONO,emoji='<:selfProtect:887743151027126302>',cooldown=5,effect="ml")
bombRobot = skill("Invocation - Bombe Robot","ym",TYPE_SUMMON,500,0,AREA_CIRCLE_3,invocation="Bombe Robot",cooldown=2,shareCooldown=True,emoji='<:autobomb:887747538994745394>',use=STRENGTH)
linx = skill("Œuil de Linx","yl",TYPE_BOOST,500,range=AREA_MONO,area=AREA_CIRCLE_2,emoji='<:noeuil:887743235131322398>',effect="mm",cooldown=4)
stalactic = skill("Stalactite","yk",TYPE_DAMAGE,300,100,emoji='<:stalactit:889089667088142346>',cooldown=3,sussess=200,range=AREA_DIST_5)
uppercut = skill("Uppercut","yj",TYPE_DAMAGE,200,75,AREA_CIRCLE_1,emoji='<:uppercut:889091033718194196>',cooldown=2,message="{0} donne un {1} à {2} :")
oneforall = skill("Un pour tous","yi",TYPE_BOOST,500,range=AREA_MONO,area=AREA_DONUT_2,cooldown=5,use=CHARISMA,effect="mo",effectOnSelf="mp",description="Une compétence qui permet d'augmenter les résistances de ses alliés au détriment des siennes",conditionType=["exclusive","aspiration",ALTRUISTE],emoji='<:oneforall:893295824761663488>')
secondSun = skill("Le second Soleil","yh",TYPE_MALUS,350,0,AREA_MONO,area=AREA_ALL_ENEMIES,cooldown=5,effect="mq",emoji='<:iwanttosleeppls:893241882484817920>',use=CHARISMA,conditionType=["exclusive","element",ELEMENT_LIGHT])
kiss = skill("Doux baiser","yg",TYPE_HEAL,69,75,AREA_DONUT_2,emoji='<:welp:893251469439008809>',message="{0} fait un gros bisou à {2} :",tpCac=True,cooldown=3)
onstage = skill("En scène !","yf",TYPE_BOOST,750,0,AREA_MONO,["exclusive","aspiration",IDOLE],True,effect="mr",emoji='<:alice:893463608716062760>',area=AREA_DONUT_7,use=CHARISMA,cooldown=5,message="{0} éléctrise l'ambience !")
icelance = skill("Lame glacée","ye",TYPE_DAMAGE,500,246,AREA_DIST_6,["exclusive","element",ELEMENT_WATER],True,emoji='<:emoji_47:893471252537298954>',cooldown=5,message="{0} fait appaître une lame de glace géante sous {2} :",use=MAGIE)
rocklance = skill("Lame rocheuse","yd",TYPE_DAMAGE,500,246,AREA_CIRCLE_3,["exclusive","element",ELEMENT_EARTH],True,emoji='<:emoji_46:893471231641276496>',cooldown=5,message="{0} fait appaître une lame de roche géante sous {2} :",use=MAGIE)
infinitFire = skill("Brasier","yc",TYPE_DAMAGE,500,172,AREA_DIST_5,["exclusive","element",ELEMENT_FIRE],True,emoji='<:emoji_44:893471208065101924>',cooldown=5,message="{0} déclanche un brasier autour de {2} :",area=AREA_LINE_3,use=MAGIE)
storm = skill("Ouragan","yb",TYPE_DAMAGE,500,172,AREA_CIRCLE_2,["exclusive","element",ELEMENT_AIR],True,emoji='<:emoji_44:893471179023732809>',cooldown=5,message="{0} déclanche un ouragan autour de {2} :",area=AREA_CIRCLE_2,use=MAGIE)
innerdarkness = skill("Ténèbres intérieurs","ya",TYPE_INDIRECT_DAMAGE,500,0,conditionType=["exclusive","element",ELEMENT_DARKNESS],ultimate=True,emoji='<:emoji_48:893471268957990982>',cooldown=5,effect="ms",use=MAGIE,group=SKILL_GROUP_DEMON,hpCost=25)
divineLight = skill("Lumière divine",'xz',TYPE_INDIRECT_HEAL,500,conditionType=["exclusive","element",ELEMENT_LIGHT],ultimate=True,emoji='<:emoji_49:893471282815963156>',cooldown=5,effect=["mu","mv"],use=CHARISMA,area=AREA_CIRCLE_1,group=SKILL_GROUP_HOLY,maxHpCost=15)
swordDance = skill("Danse des sabres","xy",TYPE_DAMAGE,350,power=70,use=STRENGTH,emoji='<:sworddance:894544710952173609>',cooldown=3,area=AREA_CIRCLE_2,range=AREA_MONO)
shot = skill("Tir net","xx",TYPE_DAMAGE,350,75,AREA_CIRCLE_6,emoji='<:shot:894544804321558608>',cooldown=5,use=STRENGTH,damageOnArmor=2)
percingLance = skill("Lance Perçante","xw",TYPE_DAMAGE,350,power=70,emoji='<:percing:894544752668708884>',cooldown=3,area=AREA_LINE_2,range=AREA_CIRCLE_2)
percingArrow = skill("Flèche Perçante","wv",TYPE_DAMAGE,350,power=70,emoji='<:percingarrow:887745340915191829>',cooldown=3,area=AREA_LINE_2,range=AREA_DIST_5)
highkick = skill("HighKick","wu",TYPE_DAMAGE,350,power=123,range=AREA_CIRCLE_1,emoji='<:highkick:894544734759030825>',cooldown=5,damageOnArmor=1.35)
multishot = skill("Tir Multiple","wt",TYPE_DAMAGE,350,power=70,range=AREA_DIST_4,emoji='<:name:894544834780622868>',cooldown=3,area=AREA_CONE_2)
bleedingArrow = skill("Flèche Hémoragique","ws",TYPE_DAMAGE,350,35,AREA_DIST_5,effect='mx',emoji='<:bleedingarrow:894544820071178292>')
bleedingDague = skill("Dague Hémoragique","wr",TYPE_DAMAGE,350,35,AREA_CIRCLE_2,effect='mx',emoji='<:bleedingdague:894552391444234242>')
affaiblissement = skill("Affaiblissement","wq",TYPE_MALUS,350,effect="my",cooldown=3,use=INTELLIGENCE,emoji='<:affaib:963394012771942440>',area=AREA_CIRCLE_1)
provo = skill("Provocation","wp",TYPE_MALUS,350,emoji='<:supportnt:894544669793476688>',effect='mz',cooldown=3,use=INTELLIGENCE)
flameche = skill("Flamèche","wo",TYPE_DAMAGE,100,42,area=AREA_CONE_2,use=MAGIE,conditionType=["exclusive","element",ELEMENT_FIRE],emoji='<:flame1:897811975675969556>')
flame = skill("Flamme","wn",TYPE_DAMAGE,250,84,area=AREA_CONE_2,use=MAGIE,conditionType=["exclusive","element",ELEMENT_FIRE],cooldown=3,emoji='<:flame2:897812264185376798>')
pyro = skill("Pyrotechnie","wm",TYPE_DAMAGE,500,126,area=AREA_CONE_2,use=MAGIE,conditionType=["exclusive","element",ELEMENT_FIRE],cooldown=5,emoji='<:flame3:897812061139140651>')
ecume = skill("Ecume","wl",TYPE_DAMAGE,100,60,use=MAGIE,conditionType=["exclusive","element",ELEMENT_WATER],emoji='<:splash1:897844189184811078>')
courant = skill("Courant","wk",TYPE_DAMAGE,250,120,use=MAGIE,conditionType=["exclusive","element",ELEMENT_WATER],cooldown=3,emoji='<:splash2:897844205198659594>')
torant = skill("Torrant","wd",TYPE_DAMAGE,500,160,use=MAGIE,conditionType=["exclusive","element",ELEMENT_WATER],cooldown=5,emoji='<:splash3:897844380491202581>')
brise = skill("Brise","wj",TYPE_DAMAGE,100,42,use=MAGIE,conditionType=["exclusive","element",ELEMENT_AIR],area=AREA_CIRCLE_1,emoji='<:wind1:897845097775915038>')
storm2 = skill("Tempête","wi",TYPE_DAMAGE,250,84,use=MAGIE,conditionType=["exclusive","element",ELEMENT_AIR],area=AREA_CIRCLE_1,cooldown=3,emoji='<:wind2:897845144299110441>')
tornado = skill("Tornade","wh",TYPE_DAMAGE,500,126,use=MAGIE,conditionType=["exclusive","element",ELEMENT_AIR],area=AREA_CIRCLE_1,cooldown=5,emoji='<:wind3:897845187940868156>')
stone = skill("Caillou","wg",TYPE_DAMAGE,100,60,use=MAGIE,conditionType=["exclusive","element",ELEMENT_EARTH],emoji='<:rock1:897846015552532531>')
rock = skill("Rocher","wf",TYPE_DAMAGE,250,120,use=MAGIE,conditionType=["exclusive","element",ELEMENT_EARTH],cooldown=3,emoji="<:rock2:897846028512944138>")
mont = skill("Montagne","we",TYPE_DAMAGE,500,160,use=MAGIE,conditionType=["exclusive","element",ELEMENT_EARTH],cooldown=5,emoji='<:rock3:897846042576420874>')
stingray2 = skill("Pigmalance","wd",TYPE_DAMAGE,500,120,AREA_CIRCLE_7,ultimate=True,emoji='<:stingray:899243721378390036>',cooldown=5,area=AREA_LINE_6,sussess=120,description="Inflige des dégâts pendant deux tours.\nPuissance au premier tour : 100",damageOnArmor=0.7,url="https://cdn.discordapp.com/attachments/935769576808013837/935781565936590898/20220126_070809.gif")
stingray = skill("Pigmalance","wc",TYPE_DAMAGE,500,100,AREA_CIRCLE_7,ultimate=True,emoji='<:stingray:899243721378390036>',cooldown=5,area=AREA_LINE_6,sussess=100,effectOnSelf="nb",damageOnArmor=0.7,url="https://cdn.discordapp.com/attachments/935769576808013837/935781565072547850/20220126_071411.gif")
dark1 = skill("Cécité","wb",TYPE_DAMAGE,100,60,use=MAGIE,conditionType=["exclusive","element",ELEMENT_DARKNESS],emoji='<:dark1:899599162566410280>')
dark2 = skill("Obscurité","wa",TYPE_DAMAGE,250,120,use=MAGIE,conditionType=["exclusive","element",ELEMENT_DARKNESS],cooldown=3,emoji='<:dark2:899599147399807006>')
dark3 = skill("Pénombre","vz",TYPE_DAMAGE,500,160,use=MAGIE,conditionType=["exclusive","element",ELEMENT_DARKNESS],cooldown=5,emoji='<:dark3:899598969930399765>')
light1 = skill("Lueur","vy",TYPE_DAMAGE,100,42,use=MAGIE,conditionType=["exclusive","element",ELEMENT_LIGHT],area=AREA_CIRCLE_1,emoji='<:light1:899598879576690689>')
light2 = skill("Éclat","vx",TYPE_DAMAGE,250,84,use=MAGIE,conditionType=["exclusive","element",ELEMENT_LIGHT],area=AREA_CIRCLE_1,cooldown=3,emoji='<:light2:899598896613969970>')
light3 = skill("Éblouissement","vw",TYPE_DAMAGE,500,126,use=MAGIE,conditionType=["exclusive","element",ELEMENT_LIGHT],area=AREA_CIRCLE_1,cooldown=5,emoji='<:light3:899599232628043787>')
derobade = skill("Dérobade","vv",TYPE_BOOST,350,0,AREA_DONUT_3,cooldown=4,effectOnSelf="nd",effect="nc",emoji='<:derobade:899788297868558337>',use=INTELLIGENCE)
ferocite = skill("Férocité","vu",TYPE_PASSIVE,200,0,emoji='<:ferocite:899790356315512852>',effectOnSelf="ne",use=None)
ironWillSkill = skill("Volontée de Fer","vt",TYPE_PASSIVE,200,0,emoji='<:ironwill:899793931762565251>',effectOnSelf="nh",use=None)
royaleGardeSkill = skill("Garde Royale","vs",TYPE_PASSIVE,200,0,emoji='<:gardeRoyale:899793954315321405>',effectOnSelf="ng",use=None)
defi = skill("Défi","vr",TYPE_PASSIVE,200,0,emoji='<:defi:899793973873360977>',effectOnSelf="nf",use=None)
dissimulation = skill("Dissimulation","vq",TYPE_PASSIVE,0,effectOnSelf="nj",use=None,emoji="<:dissimulation:900083085708771349>")
bleedingTrap = skill("Piège de lacération","vp",TYPE_INDIRECT_DAMAGE,500,effect="mx",cooldown=4,area=AREA_CIRCLE_1,use=STRENGTH,message="{0} place et déclanche un {1} autour de {2} :",emoji='<:lacerTrap:900076484230774807>',effPowerPurcent=55)
# vn already taken (Prévention)
convert = skill("Convertion","vm",TYPE_ARMOR,350,range=AREA_DONUT_5,effect="nk",cooldown=3,emoji='<:convertion:900311843938115614>')
vampirisme = skill("Vampirisme","vl",TYPE_INDIRECT_HEAL,350,range=AREA_DONUT_5,effect="no",cooldown=3,emoji='<:vampire:900312789686571018>',group=SKILL_GROUP_DEMON,hpCost=10,effPowerPurcent=150)
heriteEstialba = skill("Héritage - Fée d'Estialba","vk",TYPE_PASSIVE,0,effectOnSelf='np',emoji='<:heriteEstialba:900318953262432306>',use=MAGIE)
heriteLesath = skill("Héritage - Famille Lesath","vj",TYPE_PASSIVE,0,effectOnSelf='ns',emoji='<:hertiteLesath:900322590168608779>')
focal = skill("Focalisation","vi",TYPE_INDIRECT_DAMAGE,1000,range=AREA_CIRCLE_3,cooldown=7,effect="me",effPowerPurcent=125,area=AREA_CIRCLE_1,effectOnSelf="me",emoji='<:focal:925204877683085332>',shareCooldown=True,use=MAGIE,description="Applique 3 effets Poison d'Estialba à la cible, mais vous en donne un également",selfEffPurcent=45)
suppr = skill("Suppression","vh",TYPE_DAMAGE,650,90,emoji='<a:sup:925199175681970216>',cooldown=5,use=MAGIE,damageOnArmor=3,sussess=80)
revitalisation = skill("Mot revitalisant","vg",TYPE_HEAL,300,50,area=AREA_CIRCLE_1,emoji="<:revita:902525429183811655>",cooldown=2)
onde = skill("Onde","vf",TYPE_ARMOR,500,effect="nv",cooldown=4,area=AREA_CIRCLE_1,emoji='<:onde:902526595842072616>')
eting = skill("Marque Eting","ve",TYPE_INDIRECT_HEAL,350,effect="nw",emoji='<:eting:902525771074109462>',description="Donne un effet régénérant cumulable à l'allié ciblé")
renforce = skill("Renforcement","vd",TYPE_BOOST,500,range=AREA_DONUT_5,effect="nx",cooldown=5,description="Une compétence qui augmente la résistance d'un allié. L'effet diminue avec les tours qui passent",use=INTELLIGENCE,emoji='<:renfor:921760752065454142>')
steroide = skill("Stéroïdes","vc",TYPE_BOOST,500,range=AREA_DONUT_5,effect="oa",cooldown=3,area=AREA_CIRCLE_1,use=INTELLIGENCE,emoji='<:steroide:963548366053179392>')
renisurection = skill("Résurrection","vb",TYPE_RESURECTION,500,100,emoji='<:respls:906314646007468062>',cooldown=4,shareCooldown=True,description="Permet de ressuciter un allié",use=CHARISMA)
demolish = skill("Démolition","va",TYPE_DAMAGE,750,180,AREA_CIRCLE_2,ultimate=True,cooldown=7,effect=incur[5],damageOnArmor=1.2,emoji='<:destruc:905051623108280330>')
contrainte = skill("Contrainte","uz",TYPE_MALUS,500,range=AREA_CIRCLE_6,effect=[incur[3],"oc"],cooldown=3,use=INTELLIGENCE,emoji='<:contrainte:963393945704992829>')
trouble = skill("Trouble","uy",TYPE_MALUS,500,range=AREA_CIRCLE_6,effect=[incur[3],"od"],use=CHARISMA,emoji='<:trouble:963394783596933182>',cooldown=3)
epidemic = skill("Infirmitée","ux",TYPE_MALUS,500,area=AREA_CIRCLE_5,effect=incur[2],cooldown=3,use=None,emoji='<:infirm:904164428545683457>')
croissance = skill("Croissance","uw",TYPE_BOOST,500,effect="oe",cooldown=5,description="Une compétence dont les bonus se renforce avec les tours qui passent",use=CHARISMA,range=AREA_DONUT_5,emoji='<:crois:921760610985865246>')
destruction = skill("Météore","uu",TYPE_DAMAGE,1000,power=int(explosion.power * 1.45),ultimate=True,percing=0,cooldown=7,shareCooldown=True,effectOnSelf=explosionSilentEff,use=MAGIE,emoji='<:meteor:904164411990749194>',damageOnArmor=explosion.onArmor,url='https://cdn.discordapp.com/attachments/933783831272628356/934069125628690482/20220121_135643.gif')
castDest = effect("Cast - Météore","nnnn",turnInit=2,silent=True,emoji=uniqueEmoji('<a:castMeteor:932827784655536139>'),replique=destruction)
destruction2 = skill("Météore","uv",TYPE_DAMAGE,1000,power=0,ultimate=True,cooldown=7,effectOnSelf=castDest,use=MAGIE,shareCooldown=True,emoji=destruction.emoji,message="Une ombre plane au dessus de {2}...")
infectFiole = skill("Fiole d'infection","ut",TYPE_INDIRECT_DAMAGE,350,0,effect=["oh","oi"],cooldown=3,use=INTELLIGENCE,message="{0} lance une {1} sur {2}",emoji='<:fioleInfect:904164736407597087>')
bigLaser = skill("Lasers chromanergiques - Configuration Ligne","us",TYPE_DAMAGE,0,int(transObs.power*1.2),emoji='<:uLaserLine:906027231128715344>',area=AREA_LINE_6,sussess=95,damageOnArmor=1.33,ultimate=True,cooldown=7,description="Après un tour de chargement, déployez des drones énergétiques qui tirent un puissant rayon coloré en ligne droite")
bigLaserRep = effect("Cast - Las. Chrom. - Conf. Ligne","bigLaserEff",turnInit=2,silent=True,emoji=dangerEm,replique=bigLaser)
bigLaser2 = skill(bigLaser.name,"ur",bigLaser.type,750,0,area=bigLaser.area,emoji=bigLaser.emoji,effectOnSelf=bigLaserRep,ultimate=bigLaser.ultimate,cooldown=bigLaser.cooldown,message="{0} charge ses drones")
bigMonoLaser = skill("Lasers chromanergiques - Configuration Mono","uq",TYPE_DAMAGE,0,int(transBerserk.power*1.2),emoji='<:uLaserMono:906027216989716480>',area=AREA_MONO,sussess=100,damageOnArmor=1.33,ultimate=True,cooldown=7,description="Après un tour de chargement, déployez des drones énergétiques qui tirent un puissant rayon coloré sur un adversaire depuis le ciel")
bigMonoLaserRep = effect("Cast - Las. Chrom. - Conf. Mono","bigMonoLaserEff",turnInit=2,silent=True,emoji=dangerEm,replique=bigMonoLaser)
bigMonoLaser2 = skill(bigMonoLaser.name,"up",bigMonoLaser.type,750,0,area=bigMonoLaser.area,emoji=bigMonoLaser.emoji,effectOnSelf=bigMonoLaserRep,ultimate=bigMonoLaser.ultimate,cooldown=bigMonoLaser.cooldown,message="Les drones de {0} s'envolent")
invocBat2 = skill("Invocation - Chauve-souris II","uo",TYPE_SUMMON,500,invocation="Chauve-Souris II",emoji="<:cuttybat2:904369379762925608>",shareCooldown=True,use=CHARISMA,cooldown=3)
invocCarbunR = skill("Invocation - Carbuncle Rubis","un",TYPE_SUMMON,500,invocation="Carbuncle Rubis",emoji="<:invocRuby:919857898195128362>",shareCooldown=True,use=MAGIE,cooldown=3)
concen = skill("Concentration","um",TYPE_BOOST,price=350,effect="oj",range=AREA_MONO,area=AREA_DONUT_2,cooldown=4,use=None,emoji='<:concen:921762263814262804>')
memAlice = skill("Ultima Sanguis Rosae","memAlice",TYPE_HEAL,1000,int(transIdo.power*1.3),AREA_MONO,maxHpCost=25,shareCooldown=True,area=AREA_DONUT_4,cooldown=8,ultimate=True,group=SKILL_GROUP_HOLY,use=CHARISMA,emoji='<a:memAlice2:908424319900745768>',description="Cette compétence soigne les alliés vivants et recussite les alliés morts pour une certaine valeur des soins initiaux, affectée par le niveau de votre personnage",effectAroundCaster=[TYPE_RESURECTION,AREA_CIRCLE_6,150])
memAliceCast = effect("Cast - {0}".format(memAlice.name),"aliceMementoCast",replique=memAlice,turnInit=2,silent=True,emoji=uniqueEmoji('<a:memAliceCast:908413832194588723>'))
memAlice2 = copy.deepcopy(memAlice)
memAlice2.id, memAlice2.power, memAlice2.effectOnSelf, memAlice2.emoji, memAlice2.maxHpCost, memAlice2.effectAroundCaster = "ul",0,memAliceCast,'<a:memAliceCast:908413832194588723>', 0, None
blackHole = skill("Trou noir","uk",TYPE_PASSIVE,ironWillSkill.price,effectOnSelf="ol",use=None,emoji='<:blackHole:906195944406679612>')
blackHoleEff2 = copy.deepcopy(defenseUp)
blackHoleEff2.power, blackHoleEff2.aggro, blackHoleEff2.turnInit = 25, 15, 3
blackHole2 = skill("Provecta Trou noir","uj",TYPE_BOOST,0,use=None,effect="on",effectOnSelf=blackHoleEff2,emoji='<:blackHole2:906195979332640828>',cooldown=7,ultimate=True,description="Redirige **25%** des dégâts directs reçus par vos alliés proches vers vous tout en réduisant de **25%** les dégâts indirects qu'ils recoivent et en diminuant leur agression, et réduit les dégâts que vous recevez de **25%** tout en augmentant votre agression pendant 3 tours",area=AREA_DONUT_2,range=AREA_MONO)
fireCircle = skill("Cercle de feu","ui",TYPE_DAMAGE,350,50,AREA_DIST_5,["exclusive","element",ELEMENT_FIRE],effect='oo',area=AREA_DONUT_1,cooldown=3,use=MAGIE,emoji='<:fireCircle:906219518760747159>')
waterCircle = skill("Cercle d'eau","uh",TYPE_DAMAGE,350,35,AREA_DIST_5,["exclusive","element",ELEMENT_WATER],effect='op',area=AREA_DONUT_1,cooldown=3,use=MAGIE,emoji='<:waterCircle:906219492135276594>')
airCircle = skill("Cercle d'air","ug",TYPE_DAMAGE,350,50,AREA_CIRCLE_2,["exclusive","element",ELEMENT_AIR],effect='oq',area=AREA_DONUT_1,cooldown=3,use=MAGIE,emoji='<:airCircle:906219469200842752>')
earthCircle = skill("Cercle de terre","uf",TYPE_DAMAGE,350,35,AREA_DIST_5,["exclusive","element",ELEMENT_EARTH],effect='or',area=AREA_DONUT_1,cooldown=3,use=MAGIE,emoji='<:earthCircle:906219450129317908>')
fireShot = skill("Tir Feu","ue",TYPE_DAMAGE,350,70,area=AREA_CONE_2,cooldown=3,conditionType=["exclusive","element",ELEMENT_FIRE],range=AREA_DIST_5,emoji='<:fireShot:906219594639876116>')
waterShot = skill("Tir Eau","ud",TYPE_DAMAGE,350,100,cooldown=3,conditionType=["exclusive","element",ELEMENT_WATER],range=AREA_DIST_5,emoji='<:waterShot:906219607856119868>')
airStrike = skill("Frappe Air","uc",TYPE_DAMAGE,350,70,area=AREA_CONE_2,cooldown=3,conditionType=["exclusive","element",ELEMENT_AIR],range=AREA_CIRCLE_2,emoji='<:airStrike:906219547873386526>')
earthStrike = skill("Frappe Terre","ub",TYPE_DAMAGE,350,100,cooldown=3,conditionType=["exclusive","element",ELEMENT_EARTH],range=AREA_CIRCLE_2,emoji='<:earthStrike:906219563832709142>')
space1 = skill("Naine Blanche","ua",TYPE_DAMAGE,100,42,use=MAGIE,conditionType=["exclusive","element",ELEMENT_SPACE],area=AREA_CIRCLE_1,emoji='<:ast1:907470821679824896>')
space2 = skill("Constelation","tz",TYPE_DAMAGE,250,84,use=MAGIE,conditionType=["exclusive","element",ELEMENT_SPACE],area=AREA_CIRCLE_1,cooldown=3,emoji='<:ast2:907470855402033153>')
space3 = skill("Nébuluse","ty",TYPE_DAMAGE,500,126,use=MAGIE,conditionType=["exclusive","element",ELEMENT_SPACE],area=AREA_CIRCLE_1,cooldown=5,emoji='<:ast3:907470880676917309>')
time1 = skill("Seconde","tx",TYPE_DAMAGE,100,60,use=MAGIE,conditionType=["exclusive","element",ELEMENT_TIME],emoji='<:time1:907474383034023977>')
time2 = skill("Minute","tw",TYPE_DAMAGE,250,120,use=MAGIE,conditionType=["exclusive","element",ELEMENT_TIME],cooldown=3,emoji='<:time2:907474439854235668>')
time3 = skill("Heure","tv",TYPE_DAMAGE,500,160,use=MAGIE,conditionType=["exclusive","element",ELEMENT_TIME],cooldown=5,emoji='<:time3:907474471240216658>')
timeSpEff = effect("Rembobinage","nigHotMF",CHARISMA,power=20,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,turnInit=3,emoji=uniqueEmoji('<:rlb:907687694476378112>'),stackable=True,description='Un effet de soin sur la durée qui se déclanche en début de tour')
timeSp = skill("Rembobinage","tu",TYPE_INDIRECT_HEAL,500,use=CHARISMA,range=AREA_MONO,area=AREA_CIRCLE_5,effect=timeSpEff,conditionType=["exclusive","element",ELEMENT_TIME],cooldown=7,ultimate=True,emoji='<:rlb:907687694476378112>')
spaceSp = skill("Pluie d'étoiles","tt",TYPE_DAMAGE,500,172,use=MAGIE,conditionType=["exclusive","element",ELEMENT_SPACE],cooldown=5,area=AREA_CIRCLE_2,ultimate=True,emoji='<:starFall:907687023140302908>')
idoOH = skill("Apothéose","ts",TYPE_PASSIVE,500,effectOnSelf="idoOHEff",emoji='<:IdoOH:909278546172719184>',conditionType=["exclusive","aspiration",IDOLE],use=None)
proOH = skill("Protection Avancée","tr",TYPE_PASSIVE,500,effectOnSelf="proOHEff",emoji='<:proOH:909278525528350720>',conditionType=["exclusive","aspiration",PROTECTEUR],use=None)
altOH = skill("Bénédiction","tq",TYPE_PASSIVE,500,effectOnSelf="altOHEff",emoji='<:altOH:909278509145395220>',conditionType=["exclusive","aspiration",ALTRUISTE],use=None,group=SKILL_GROUP_HOLY)
lightAura2 = skill("Provecta Aura de Lumière","tp",TYPE_PASSIVE,500,effectOnSelf="lightaura2Pa",emoji=lightAura.emoji,use=CHARISMA)
tripleMissilesLaunch = skill("Missiles téléguidés","tripleMissiles",TYPE_DAMAGE,750,120,ultimate=True,repetition=3,damageOnArmor=1.2,percing=0,cooldown=10,emoji='<:missiles:909727253414445057>',conditionType=["exclusive","aspiration",OBSERVATEUR])
tripleMissilesEff2 = effect("Cast - {0}".format(tripleMissilesLaunch.name),"tripleMissilesEff2",turnInit=2,silent=True,emoji=sameSpeciesEmoji("<a:missileSoonB:909727376273965097>","<a:missilesSoonR:909727492510740501>"),replique=tripleMissilesLaunch)
tripleMissilesCast2 = copy.deepcopy(tripleMissilesLaunch)
tripleMissilesCast2.power, tripleMissilesCast2.message, tripleMissilesCast2.effectOnSelf, tripleMissilesCast2.id = 0,"{0} lance ses missiles",tripleMissilesEff2,"tripleMissilesCast"
tripleMissilesEff = effect("Cast - {0}".format(tripleMissilesLaunch.name),"tripleMissilesEff",turnInit=2,silent=True,emoji=uniqueEmoji('<:missilesCast:909727680264560690>'),replique=tripleMissilesCast2)
tripleMissiles = copy.deepcopy(tripleMissilesCast2)
tripleMissiles.effectOnSelf,tripleMissiles.message,tripleMissiles.say,tripleMissiles.id = tripleMissilesEff,"{0} calibre ses missiles","Ok, les missiles sont prêts pour le lancement !","to"
lightHeal2 = skill("Illumination","tn",TYPE_HEAL,350,60,cooldown=3,use=CHARISMA,conditionType=["exclusive","element",ELEMENT_LIGHT],emoji='<:illu:909134286203006997>')
extraEtingSkill = copy.deepcopy(eting)
extraEtingSkill.name, extraEtingSkill.id, extraEtingSkill.effect, extraEtingSkill.condition, extraEtingSkill.emoji = "Marque Eting +","tm",["eting+"],[0,2,ELEMENT_TIME],'<:emeB:909132040392302703>'
willShield = effect("Force de volonté","willShield",STRENGTH,overhealth=120,description="Votre force de volonté vous permet de vous protéger de quelques dégâts",turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji('<:willB:922987683217821727>','<:willR:922987661952708638>'))
strengthOfWill = skill("Force de volonté","feliUltLaunch",TYPE_DAMAGE,0,power=200,cooldown=7,effectOnSelf=willShield,ultimate=True,emoji='<:feliSlash:916208942974132245>',tpCac=True)
strengthOfWillCastEff = effect("Cast - Force de volonté","castFeliEff",turnInit=2,silent=True,emoji=uniqueEmoji('<a:feliSlashCast:932819458186158160>'),replique=strengthOfWill)
strengthOfWillCast = copy.deepcopy(strengthOfWill)
strengthOfWillCast.id, strengthOfWillCast.power, strengthOfWillCast.effectOnSelf,strengthOfWillCast.message, strengthOfWillCast.tpCac = "tl",0,strengthOfWillCastEff,"{0} rassemble toute sa Détermination dans son arme", False

sixtineGoodNight = copy.deepcopy(dmgDown)
sixtineGoodNight.power, sixtineGoodNight.stat, sixtineGoodNight.description = 8, INTELLIGENCE, "Réduit les dégâts infligés par le porteur de l'effet de **8%** affectés par les statistiques\nSi plusieurs effets de réduction de dégâts infligés sont présents sur une même cible, seul l'effet le plus puissant est pris en compte"
sixtineUlt = skill("Douce nuit","tk",TYPE_MALUS,0,range=AREA_MONO,area=AREA_ALL_ENEMIES,use=INTELLIGENCE,effect=sixtineGoodNight,ultimate=True,cooldown=7,emoji='<:night:911735172901273620>')
hinaUlt = skill("Déluge de plume","tj",TYPE_DAMAGE,0,28,sussess=40,area=AREA_CONE_2,repetition=5,cooldown=7,emoji='<:featherStorm:909932475457884191>')
julieUltEff = effect("Prolongation","JulieUltEff",CHARISMA,power=15,turnInit=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,stackable=True,emoji=uniqueEmoji('<:plg:911734437597835316>'),description="Un effet de soin sur la durée qui se déclanche en début de tour")
julieUlt = skill("Prolongation","ti",TYPE_INDIRECT_HEAL,0,area=AREA_CIRCLE_3,range=AREA_MONO,emoji='<:plg:911734437597835316>',effect=julieUltEff,cooldown=7,use=CHARISMA)
invocSeraf = skill("Invocation - Fée protectrice","th",TYPE_SUMMON,500,invocation="Fée protectrice",emoji="<:seraphin:911078421361205289>",shareCooldown=True,use=INTELLIGENCE,cooldown=5)
mageUlt = skill("Éminence","tg",TYPE_DAMAGE,1000,emoji='<:emanence:911397114850975795>',power=120,conditionType=["exclusive","aspiration",MAGE],ultimate=True,cooldown=5,area=AREA_DONUT_2,use=MAGIE,description="Une compétence dont la puissance et la zone d'effet dépend de l'élément")
mageUltMono = copy.deepcopy(mageUlt)
mageUltMono.power,mageUltMono.area,mageUltMono.sussess = 150,AREA_MONO,160
mageUltZone = copy.deepcopy(mageUlt)
mageUltZone.power,mageUltZone.area,mageUltZone.sussess = 80,AREA_CONE_3,80
soulaEff = effect("Traité de soulagement","soulaArmor",INTELLIGENCE,overhealth=50,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji('<:tsB:911732326818545664>','<:tsR:911732347601317908>'))
soulagement = skill("Traité de soulagement","tf",TYPE_ARMOR,500,0,AREA_MONO,["exclusive","aspiration",PREVOYANT],area=AREA_CIRCLE_2,use=INTELLIGENCE,cooldown=5,effect=soulaEff,emoji='<:soul:911732783993483284>')
bloodArmor = effect("Bouclier sanguin","bloodyArmor",STRENGTH,overhealth=50,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
bloodyStrike = skill("Frappe sanguine",'te',TYPE_DAMAGE,500,100,AREA_CIRCLE_2,["exclusive","aspiration",BERSERK],cooldown=5,effectOnSelf=bloodArmor,emoji='<:berkSlash:916210295867850782>')
infraMedicaEff = copy.deepcopy(julieUltEff)
infraMedicaEff.emoji, infraMedicaEff.power, infraMedicaEff.id, infraMedicaEff.name = sameSpeciesEmoji('<:imB:911732644193124393>','<:imR:911732657728151572>'), int(julieUltEff.power*1.35), "infraMedicaHeal", "Infra Medica"
infraMedica = skill("Infra Medica","td",TYPE_INDIRECT_HEAL,500,0,AREA_MONO,["exclusive","aspiration",ALTRUISTE],area=AREA_CIRCLE_2,cooldown=5,effect=infraMedicaEff,emoji='<:medica:911732802947530843>')
flambe = effect("Flambé","flambage",STRENGTH,type=TYPE_INDIRECT_DAMAGE,power=10,aggro=10,area=AREA_CIRCLE_1,description="Pour chaque attaque physique directe reçu par la cible, la puissance de cet effet augmente de {0} lors de son déclanchement, au début du prochain tour du lanceur",trigger=TRIGGER_ON_REMOVE,emoji=uniqueEmoji('<:flamb:913165325590212659>'))
flambeSkill = skill("Flambage","tc",TYPE_INDIRECT_DAMAGE,500,effect=flambe,cooldown=5,emoji='<:flamb:913165325590212659>')
magAch = effect("Magia atrocitas","magAch",MAGIE,type=TYPE_INDIRECT_DAMAGE,power=flambe.power,aggro=10,area=AREA_CIRCLE_1,description="Pour chaque attaque magique directe reçu par la cible, la puissance de cet effet augmente de {0} lors de son déclanchement, au début du prochain tour du lanceur",trigger=TRIGGER_ON_REMOVE,emoji=uniqueEmoji('<:magAch:913165311291842571>'))
magAchSkill = skill("Magia atrocitas","tb",TYPE_INDIRECT_DAMAGE,500,effect=magAch,cooldown=5,emoji='<:magAch:913165311291842571>')
idoOS = skill("Clou du spectacle","ta",TYPE_PASSIVE,500,effectOnSelf="idoOSEff",emoji='<:osIdo:913885207751446544>',conditionType=["exclusive","aspiration",IDOLE],use=None)
proOS = skill("Extra Protection","sz",TYPE_PASSIVE,500,effectOnSelf="proOSEff",emoji='<:osPro:913885191800512562>',conditionType=["exclusive","aspiration",PROTECTEUR],use=None)
preOS = skill("Armures Avancées","sy",TYPE_PASSIVE,500,effectOnSelf="preOSEff",emoji='<:osPre:913885175161712710>',conditionType=["exclusive","aspiration",PREVOYANT],use=None)
geoConBoost = effect("Géo-Controlé","geocontroled",INTELLIGENCE,25,20,20,10,10,20,25,5,5,0,description="Une grande force vous envahis",emoji=sameSpeciesEmoji("<:geoContB:918422778414256158>","<:geoContR:918422792649723914>"))
geoConLaunch = skill("Géo-Controle","geoControleFinal",TYPE_BOOST,1000,range=AREA_MONO,area=AREA_CIRCLE_3,effect=geoConBoost,cooldown=7,use=INTELLIGENCE,ultimate=True,emoji='<:geoCont:918422710781083668>')
geoConCastEff = effect("Cast - {0}".format(geoConLaunch.name),"geoControleCastEff",turnInit=2,silent=True,emoji=dangerEm,replique=geoConLaunch)
geoConCast = copy.deepcopy(geoConLaunch)
geoConCast.id, geoConCast.effect, geoConCast.effectOnSelf, geoConCast.message = "sx",[None],geoConCastEff,"{0} rassemble l'énergie cosmique autour de lui..."
kikuRes = skill("Mors vita est","sw",TYPE_RESURECTION,750,80,AREA_MONO,area=AREA_DONUT_5,emoji='<:mortVitaEst:916279706351968296>',initCooldown=3,shareCooldown=True,description="Utiliser cette compétence empêche l'équipe d'utiliser Ultima Sanguis Rosae, Résurrection ainsi que n'importe quelle Transcendance jusqu'au prochain tour",use=CHARISMA,group=SKILL_GROUP_DEMON,hpCost=10)
memClemLauchSkill = skill("Ultima Sanguis Pluviae","memClemSkillLauch",TYPE_DAMAGE,0,200,AREA_MONO,setAoEDamge=True,percing=0,sussess=666,area=AREA_CIRCLE_7,ultimate=True,use=MAGIE,cooldown=99,emoji="<:clemMemento:902222089472327760>",description="\n__Effets lors du premier tour de chargement :__\nDéfini vos PVs courants à **1**\nObtenez un bouclier absolu d'une valeur de **50%** des PVs perdus\nDivise votre Résistance Soins de **50%**\nDiminue vos PV maximums de **50%** pour le reste du combat\nDonne l'effet __Incurable (50)__ sur le lanceur pour le reste du combat")
memClemCastSkillEff = effect("Cast - Ultima Sanguis Pluviae","memClemSkillCast",turnInit=2,silent=True,emoji=dangerEm,replique=memClemLauchSkill)
memClemCastSkill = copy.deepcopy(memClemLauchSkill)
memClemCastSkill.id, memClemCastSkill.effectOnSelf, memClemCastSkill.power = "sv",memClemCastSkillEff,0
rosesPhysiEff = effect("Épines","rosesPhysiEff",CHARISMA,endurance=5,resistance=3,power=35,trigger=TRIGGER_AFTER_DAMAGE,lvl=5,description="En plus de légèrement augmenter les statistiques défensives, cet effet inflige des dégâts indirects à chaques fois que le porteur reçois des dégâts **physiques**",onDeclancher=True,emoji=sameSpeciesEmoji("<:epineB:917665759684079626>","<:epineR:917665743649275904>"))
rosesPhysi = skill("Épines","su",TYPE_BOOST,500,effect=rosesPhysiEff,use=CHARISMA,cooldown=3,range=AREA_DONUT_5,emoji='<:epines:917666041243500594>')
rosesMagicEff = effect("Pétales","rosesMagEff",CHARISMA,endurance=5,resistance=3,power=int(rosesPhysiEff.power*1.3),trigger=TRIGGER_AFTER_DAMAGE,lvl=rosesPhysiEff.lvl,description="En plus de légèrement augmenter les statistiques défensives, cet effet inflige des dégâts indirects à chaques fois que le porteur reçois des dégâts **magiques**",onDeclancher=True,emoji=sameSpeciesEmoji("<:rosesAreBlue:917665779770613761>","<:rosesAreRed:917665805557198878>"))
rosesMagic = skill("Pétales","su",TYPE_BOOST,500,effect=rosesMagicEff,use=CHARISMA,cooldown=3,range=AREA_DONUT_5,emoji='<:roses:917666059413233704>')
roses = skill("Roses","su",TYPE_BOOST,500,use=CHARISMA,become=[rosesPhysi,rosesMagic],emoji='<:roses:932612186130493450>')

krysUlt = skill("Réassemblage","st",TYPE_DAMAGE,0,80,cooldown=5,description="En plus d'infliger des dégâts, cette compétence vole **50%** de l'armure normale et légère de la cible (avant d'infliger les dégâts)",emoji='<:reconvert:916121466423091240>')
chaosArmorEff = effect("Armure du Chaos","chaosArmor",INTELLIGENCE,overhealth=1,emoji=sameSpeciesEmoji('<a:caB:938375004792426496>','<a:caR:938375020261023825>'),description="Une armure chaotique dont la puissance de base est aléatoire",type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,turnInit=3)
chaosArmor = skill("Armure du Chaos","ss",TYPE_ARMOR,emoji='<a:chaosArmor:938374846843342869>',area=AREA_CIRCLE_2,price=500,effect=chaosArmorEff,cooldown=5,use=INTELLIGENCE)
firelame = skill("Ignis ferrum","sr",TYPE_DAMAGE,500,38,range=AREA_DIST_5,conditionType=["exclusive","element",ELEMENT_FIRE],cooldown=6,area=AREA_ARC_1,repetition=3,emoji='<:fireLame:916130324197543986>',damageOnArmor=1.1)
airlame = skill("Aer ferrum","sq",TYPE_DAMAGE,500,38,range=AREA_CIRCLE_3,conditionType=["exclusive","element",ELEMENT_AIR],cooldown=6,area=AREA_ARC_1,repetition=3,emoji='<:airLame:916130609095655454>',damageOnArmor=1.1)
waterlame = skill("Aqua ferrum","sp",TYPE_DAMAGE,500,55,range=AREA_DIST_5,conditionType=["exclusive","element",ELEMENT_WATER],cooldown=6,repetition=3,emoji='<:aquaLame:916130446125977602>',damageOnArmor=1.1)
mudlame = skill("Lapis ferrum","so",TYPE_DAMAGE,500,55,range=AREA_CIRCLE_3,conditionType=["exclusive","element",ELEMENT_EARTH],cooldown=6,repetition=3,emoji='<:earthLame:916130398914875452>',damageOnArmor=1.1)
shadowLameEff = effect("Umbra ferrum","lameD'ombre",STRENGTH,power=30,stackable=True,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:darkLame:916130473162453033>'))
shadowLame = skill("Umbra ferrum","sn",TYPE_INDIRECT_DAMAGE,500,conditionType=["exclusive","element",ELEMENT_DARKNESS],effect=[shadowLameEff,shadowLameEff,shadowLameEff],cooldown=6,emoji='<:darkLame:916130473162453033>')
lightLameEff = effect("Lux ferrum","lameDeLumière",CHARISMA,resistance=5,power=30,lvl=3,description="En plus de booster légèrement la résistance de la cible, inflige des dégâts indirects lorsque cette dernière est attaquée",trigger=TRIGGER_AFTER_DAMAGE,onDeclancher=True,emoji=uniqueEmoji('<:lightLame:916131830149816340>'))
lightLame = skill("Lux ferrum","sm",TYPE_BOOST,500,effect=lightLameEff,emoji='<:lightLame:916131830149816340>',cooldown=6,conditionType=["exclusive","element",ELEMENT_LIGHT],use=CHARISMA)
astralLameEff = effect("Stella ferrum","lameétoilée",ENDURANCE,resistance=5,power=30,lvl=3,description="En plus de booster légèrement la résistance de la cible, inflige des dégâts indirects lorsque cette dernière est attaquée",trigger=TRIGGER_AFTER_DAMAGE,onDeclancher=True,emoji=uniqueEmoji('<:astralLame:916131872352911400>'),turnInit=2)
astralLame = skill("Stella ferrum","sl",TYPE_BOOST,500,range=AREA_MONO,effect=astralLameEff,emoji='<:astralLame:916131872352911400>',cooldown=6,conditionType=["exclusive","element",ELEMENT_SPACE],use=ENDURANCE)
timeLameEff = effect("Tempus ferrum","lameDuTemps",CHARISMA,resistance=5,power=30,lvl=3,description="En plus de booster légèrement la résistance de la cible, inflige des dégâts indirects lorsque cette dernière est attaquée",trigger=TRIGGER_AFTER_DAMAGE,onDeclancher=True,emoji=uniqueEmoji('<:timeLame:916131853499527208> '))
timeLame = skill("Tempus ferrum","sk",TYPE_BOOST,500,effect=timeLameEff,emoji='<:timeLame:916131853499527208> ',cooldown=6,conditionType=["exclusive","element",ELEMENT_TIME],use=CHARISMA)
magicRuneArmor = effect("Bouclier magicorunique","runeArmor",MAGIE,overhealth=bloodArmor.overhealth,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
magicRuneStrike = skill("Rune - Frappe magicorunique",'sj',TYPE_DAMAGE,500,125,bloodyStrike.range,["exclusive","aspiration",ENCHANTEUR],cooldown=bloodyStrike.cooldown,effectOnSelf=magicRuneArmor,emoji='<:magicoRune:916401319990947920>',use=MAGIE)
infinitDarkEff = effect("Noirceur infinie","bigDarkDark",MAGIE,stackable=True,power=35,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji("<:bigDark:916561798948347935>"))
infinitDark = skill("Noirceur infinie","si",TYPE_INDIRECT_DAMAGE,500,emoji='<:bigDark:916561798948347935>',effect=infinitDarkEff,cooldown=5,ultimate=True,use=MAGIE)
preciseShot = skill("Tir précis","sh",TYPE_DAMAGE,500,130,cooldown=5,use=PRECISION,emoji='<:preciseShot:916561817969500191>')
troublon = skill("Troublon","sg",TYPE_DAMAGE,500,70,cooldown=3,area=AREA_CONE_2,range=AREA_MONO,emoji='<:mousqueton:916561833920462889>')
haimaShield = effect("Haima - Bouclier","haimaShield",INTELLIGENCE,overhealth=20,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,emoji=sameSpeciesEmoji("<:haimaB:916922889679286282>","<:haimaR:916922905672171570>"))
haimaEffect = effect("Haima","haimaEff",lvl=5,description="En subissant des dégâts sans posséder d'effet \"__Haima - Bouclier__\", le porteur de cet effet gagne le dit effet au prix d'une charge de __Haima__",callOnTrigger=haimaShield,emoji=uniqueEmoji('<:haima:916922498094858251>'),trigger=TRIGGER_AFTER_DAMAGE)
haimaSkill = skill("Haima","sf",TYPE_ARMOR,500,emoji='<:haima:916922498094858251>',effect=haimaEffect,cooldown=7,use=INTELLIGENCE)
physicRune = skill("Rune - Sanguis Pact","se",TYPE_PASSIVE,750,effectOnSelf="pacteDeSang",emoji='<:pacteDeSang:917096147452035102>')
magicRune = skill("Rune - Animae Foedus","sd",TYPE_PASSIVE,750,effectOnSelf="pacteD'âme",emoji='<:pacteDame:917096164942295101>')
lightBigHealArea = skill("Lumière éclatante","sb",TYPE_HEAL,750,80,AREA_MONO,["exclusive","element",ELEMENT_LIGHT],True,area=AREA_CIRCLE_4,cooldown=7,use=CHARISMA,emoji='<a:slu:925192820824870982>')
focus = skill("Focus","sa",TYPE_INDIRECT_DAMAGE,1000,range=AREA_CIRCLE_3,cooldown=7,effect="mx",effPowerPurcent=225,selfEffPurcent=85,effectOnSelf="mx",shareCooldown=True,use=STRENGTH,description="Applique 3 effets Hémorragie à la cible, mais vous en donne un également",emoji='<:focus:925204899514417182>')
poisonusPuit = skill("Rayons Féériques Triples","zzz",TYPE_DAMAGE,500,39,area=AREA_CIRCLE_1,use=MAGIE,effect=["me"],repetition=3,cooldown=7,emoji='<a:mpp:925181294906843136>',effPowerPurcent=85)
bleedingPuit = skill("Pièges à ressorts","zzy",TYPE_DAMAGE,500,40,area=AREA_CIRCLE_1,effect=["mx"],repetition=3,cooldown=7,emoji='<a:par:925183389252874261>',effPowerPurcent=60)
supprZone = skill("Dispersion","zzx",TYPE_DAMAGE,650,70,emoji='<:principio:919529034663223376>',cooldown=5,use=MAGIE,damageOnArmor=3,sussess=60,area=AREA_CIRCLE_1)
invocCarbSaphir = skill("Invocation - Carbuncle Saphir","zzw",TYPE_SUMMON,500,invocation="Carbuncle Saphir",emoji="<:innvocSafir:919857914490007574>",shareCooldown=True,use=STRENGTH,cooldown=3)
invocCarbObsi = skill("Invocation - Carbuncle Obsidienne","zzv",TYPE_SUMMON,500,invocation="Carbuncle Obsidienne",emoji="<:invocObs:919872508226830336>",shareCooldown=True,use=STRENGTH,cooldown=3)
requiem = skill("Requiem","zzu",TYPE_DAMAGE,500,23,range=AREA_MONO,area=AREA_CIRCLE_7,use=CHARISMA,cooldown=3,repetition=3,emoji='<:requiem:919869677197484052>',group=SKILL_GROUP_DEMON)
cosmicEff = effect("Pouvoir cosmique","cosmicPowerEff",HARMONIE,strength=5,magie=5,resistance=5,emoji=sameSpeciesEmoji('<:comicPowerB:919866210768801833>','<:cosmicPowerR:919866197850353685>'),redirection=15)
cosmicEffSelf = effect("Pouvoir cosmique","cosmicPowerEffOnSelf",resistance=20,emoji=sameSpeciesEmoji('<:comicPowerB:919866210768801833>','<:cosmicPowerR:919866197850353685>'))
cosmicPower = skill("Pouvoir cosmique","zzt",TYPE_BOOST,1000,range=AREA_MONO,area=AREA_DONUT_2,use=HARMONIE,cooldown=7,emoji='<:cosmic:919866054992334848>',conditionType=["exclusive","element",ELEMENT_SPACE],effect=cosmicEff,effectOnSelf=cosmicEffSelf)
propag = skill("Propagation","zzs",TYPE_INDIRECT_DAMAGE,750,cooldown=7,emoji='<a:propa:925188411617345560>',initCooldown=3,use=MAGIE,effect=["me","mx"],description="Après la pose des effets de cette compétence, les alliés en mêlée de la cible reçoivent les effets __Poison d'Estialba__ et __Hémorragie__ de la cible pour une puissance équivalente à **{power}%** de la puissance de l'effet, pour la durée restante de l'effet de base\nSi vous n'êtes pas à l'origine de l'effet de base, la puissance de l'effet propagé équivaux à **{power2}**% de la puissance de l'effet de base",power=40,effPowerPurcent=65)

inkResEff = effect("Pied au sec","inkRes",INTELLIGENCE,turnInit=2,inkResistance=10,description="Réduit de 10% les dégâts indirects reçu.\nLe pourcentage de réduction est affecté par l'Intelligence et le Bonus aux Armures et Mitigation")
inkResEff2 = copy.deepcopy(inkResEff)
inkResEff2.stat, inkResEff2.name, inkResEff2.emoji = ENDURANCE, "Collectivement inconscient", sameSpeciesEmoji('<:incColB:921546169203687464>','<:incColR:921546151314985020>')
inkRes = skill("Pied au sec","zzr",TYPE_BOOST,500,effect=inkResEff,cooldown=4,area=AREA_CIRCLE_1,use=INTELLIGENCE,emoji='<:inkResR:921486021265354814>')
inkRes2 = skill("Inconscient collectif","zzq",TYPE_BOOST,500,range=AREA_MONO,area=AREA_CIRCLE_2,effect=inkResEff2,cooldown=4,use=ENDURANCE,emoji='<:incCol:921545816940875817>')

booyahBombLauch = skill("Jolizator","zzp",TYPE_DAMAGE,750,213,area=AREA_CIRCLE_2,ultimate=True,cooldown=7,emoji='<:bobomb:921710328771932192>',url="https://cdn.discordapp.com/attachments/935769576808013837/935783888159125544/20220126_072826.gif")
booyahBombEff = effect("Cast - Jolizator","supercalifragilisticexpialiodocieux",turnInit=2,silent=True,emoji=sameSpeciesEmoji("<:booyahB:925796592240455701>","<:booyahR:925796570509766716>"),replique=booyahBombLauch)
booyahBombCast = copy.deepcopy(booyahBombLauch)
booyahBombCast.id, booyahBombCast.effectOnSelf, booyahBombCast.power, booyahBombCast.url = "zzp",booyahBombEff,0,"https://cdn.discordapp.com/attachments/935769576808013837/935783887748079666/20220126_073038.gif"

reconst = skill("Reconstitution","zzo",TYPE_HEAL,750,130,ultimate=True,use=CHARISMA,cooldown=7,emoji='<:mudh:922914512712138802>',description="Une puissante compétence de soins monocibles")
medicamentumEff = effect("Medicamentum","bigmonoindirect",CHARISMA,type=TYPE_INDIRECT_HEAL,turnInit=3,power=55,description="Un puissant effect soignant",emoji=sameSpeciesEmoji('<:mihB:922914323037306890>','<:mihR:922914344428240937>'))
medicamentum = skill("Rune - Medicamentum",'zzn',TYPE_INDIRECT_HEAL,750,ultimate=True,emoji='<:muih:922914495737757706>',cooldown=7,use=CHARISMA,effect=medicamentumEff)

ultMonoArmorEff = effect("Armis","ultMonoArmor",INTELLIGENCE,overhealth=150,turnInit=3,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,emoji=sameSpeciesEmoji('<:runeArmis:963397040967131176>','<:armis:963397158101471272>'))
ultMonoArmor = skill("Rune - Armis","zzm",TYPE_ARMOR,750,0,ultimate=True,effect=ultMonoArmorEff,cooldown=7,use=INTELLIGENCE,emoji='<:runeArmis:963397040967131176>')

neutralZone1 = skill("Primum multi scopum magicae","zzl",TYPE_DAMAGE,100,42,area=AREA_CONE_2,use=MAGIE,emoji='<:nm1:925185303659053088>',conditionType=["exclusive","element",ELEMENT_NEUTRAL])
neutralZone2 = skill("Secundum multi scopum magicae","zzk",TYPE_DAMAGE,250,84,area=AREA_CONE_2,use=MAGIE,cooldown=3,emoji='<:nm2:925185316409716746>',conditionType=["exclusive","element",ELEMENT_NEUTRAL])
neutralZone3 = skill("Tertio multi scopum magicae","zzj",TYPE_DAMAGE,500,126,area=AREA_CONE_2,use=MAGIE,cooldown=5,emoji='<:nm3:925185333446971492>',conditionType=["exclusive","element",ELEMENT_NEUTRAL])
neutralMono1 = skill("Primum unum scopum magicae","zzi",TYPE_DAMAGE,100,60,use=MAGIE,emoji='<:nz1:925184839257317398>',conditionType=["exclusive","element",ELEMENT_NEUTRAL])
neutralMono2 = skill("Secundum unum scopum magicae","zzh",TYPE_DAMAGE,250,120,use=MAGIE,cooldown=3,emoji='<:nz2:925184858584662127>',conditionType=["exclusive","element",ELEMENT_NEUTRAL])
neutralMono3 = skill("Tertio singula scopum magicae","zzg",TYPE_DAMAGE,500,160,use=MAGIE,cooldown=5,emoji='<:nz3:925184871612157953>',conditionType=["exclusive","element",ELEMENT_NEUTRAL])

intelRaise = copy.deepcopy(renisurection)
intelRaise.name, intelRaise.use, intelRaise.id, intelRaise.emoji = "Egeiro", INTELLIGENCE, "zzf", '<:egiero:925768359964979210>'

ultRedirectSelfEff = effect("Teliki Anakatéfthynsi","ultRedirectShield",ENDURANCE,overhealth=200,absolutShield=True,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,description="Vous accorde une grosse armure aboslue\nLes armures absolues protègent même des dégâts indirects et ne sont pas affectés par les multiplicateurs de dégâts sur l'armure")
ultRedirectEff = effect("Teliki Anakatéfthynsi","ultRedirect",redirection=100,trigger=TRIGGER_DAMAGE)
ultRedirect = skill("Teliki Anakatéfthynsi","zze",TYPE_BOOST,1000,range=AREA_MONO,area=AREA_DONUT_3,cooldown=7,ultimate=True,effect=ultRedirectEff,effectOnSelf=ultRedirectSelfEff,use=ENDURANCE,emoji='<:tekeli:963396237606912050>')
clemency = skill('Clémence','zzd',TYPE_HEAL,350,60,cooldown=5,use=ENDURANCE,emoji='<:clemency:926433653037367318>',group=SKILL_GROUP_HOLY,effectAroundCaster=[TYPE_HEAL,AREA_MONO,40])

liuSkillSusEff = effect("Asuama","liuSussessArmor",ENDURANCE,overhealth=75,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,inkResistance=10,turnInit=2,emoji=uniqueEmoji("<:liuArmor:922292960886915103>"))
liuSkillSus = skill("Guraundo Sutoraiku","zzc",TYPE_DAMAGE,0,50,range=AREA_CIRCLE_2,use=ENDURANCE,effectOnSelf=liuSkillSusEff,cooldown=5,emoji='<:liuSkill:922328931502280774>')
liaSkillSus = skill("Kuchu Sutoraiku","zzb",TYPE_DAMAGE,0,25,range=AREA_CIRCLE_1,cooldown=5,knockback=1,repetition=3,use=AGILITY,emoji='<:liaSkill:922291249002709062>')
lioSkillSusEff = effect('Shinju no haha',"lioSussessEff",CHARISMA,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,power=10,turnInit=3,strength=5,magie=5,emoji=uniqueEmoji('<:lioWeap:908859876812415036>'))
lioSkillSus = skill("Shio",'zza',TYPE_INDIRECT_HEAL,0,cooldown=7,effect=lioSkillSusEff,area=AREA_CIRCLE_2,emoji='<:lioSkill:922328964926697505>')
lizSkillSusEff = effect("Tanka",'lizWillBurnThemAll',MAGIE,power=20,area=AREA_CIRCLE_1,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:lizIndirect:917204753610571776>'))
lizSKillSus = skill("Shokyaku","zyz",TYPE_INDIRECT_DAMAGE,0,effect=lizSkillSusEff,area=AREA_CONE_4,cooldown=7,emoji='<:lizSkill:922328829765242961>',use=MAGIE)

freedlyPush = skill("Pousée amicale","movepls",TYPE_DAMAGE,0,1,range=AREA_DONUT_1,use=HARMONIE,knockback=3,emoji='<:movePlz:928756987532029972>',say=["Madness ? THIS IS SPARTA !","* Out of my ways","SPAR-TA"],description="Pousse gentiment un allié de 3 cases")

pepsis = skill("Pepsis","zyy",TYPE_HEAL,500,50,AREA_MONO,area=AREA_CIRCLE_3,use=INTELLIGENCE,cooldown=5,emoji='<:pepsis:930049497214644235>',useActionStats=ACT_SHIELD)
darkShieldEff = effect("Nuit noirsisime","blackknightshield",ENDURANCE,overhealth=75,turnInit=2,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji("<:dsR:930048553835970580>","<:dsR:930048570688675900>"))
darkShield = skill("Nuit noirsisime","zyx",TYPE_ARMOR,500,use=ENDURANCE,effect=darkShieldEff,cooldown=3,emoji='<:dsR:930048553835970580>')
rencCelEff = effect('Rencontre Céleste','rencontreCel',CHARISMA,overhealth=50,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji('<:rcb:930048878668046377>','<:rcr:930048892886720603>'))
rencCel = skill("Rencontre Céleste",'zyw',TYPE_ARMOR,500,use=CHARISMA,range=AREA_MONO,area=AREA_CIRCLE_3,effect=rencCelEff,emoji='<:rencontreceleste:930049458488623104>',cooldown=5,useActionStats=ACT_HEAL)
valse = skill("Valse régénératrice","zyv",TYPE_HEAL,500,80,AREA_CIRCLE_5,area=AREA_CIRCLE_1,cooldown=7,description="Soigne en zone autour du lanceur et de l'allié le plus blessé",emoji='<:valse:930051603543760936>',useActionStats=ACT_DIRECT,effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_1,80])
pasTech = effect("Pas Technique","pasTech",turnInit=5,emoji='<:pas:930051729523879966>',stackable=True)
finalTech = skill("Final Technique","zyu",TYPE_DAMAGE,750,55,area=AREA_CIRCLE_1,cooldown=3,initCooldown=3,description="Equiper cette compétence accorde un effet __{0} {1}__ en début de tour (Cumulable jusqu'à 5 effets)\nLors de l'utilisation, tous les effets __{1}__ sont consommés, augmentant la puissance de cette compétence de **35%** par effet".format(pasTech.emoji[0][0],pasTech.name),emoji='<:final:930051626062991371>')
dissi = skill("Dissipation","zyt",TYPE_HEAL,750,80,AREA_MONO,ultimate=True,cooldown=7,area=AREA_ALL_ALLIES,emoji='<:dissipation:930049419473211392>',use=HARMONIE,description="__**Nécessite d'avoir au moins une invocation propre sur le terrain**__\nDésinvoque toutes vos invocations pour effectuer un gros soins sur toute votre équipe. La puissance est multipliée par le nombre d'invocation renvoyés")
quickCastEff = effect("Magie Prompte","quickCast",emoji=uniqueEmoji("<:quickCast:930467995283779614>"),description="Permet d'ignorer **1** tour de chargement de la prochaine compétence à chargement utilisée",turnInit=1)
quickCast = skill("Magie Prompte","zys",TYPE_BOOST,1000,range=AREA_MONO,area=AREA_MONO,use=None,cooldown=99,description="Ignore 1 tour de chargement de votre prochaine compétence",initCooldown=3,replay=True,emoji='<:quickCast:930467995283779614>',effect=quickCastEff)

foyer = skill("Foyer","zyr",TYPE_HEAL,500,35,range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=5,use=CHARISMA,conditionType=["exclusive","secElem",ELEMENT_FIRE],emoji="<:fireplace:931666078092902471>")
sweetHeatEff = effect('Douce chaleur',"sweetHeat",HARMONIE,power=10,turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,description="Un effet qui soigne le porteur pendant 3 tours")
sweetHeat = skill("Flammes intérieurs","zyq",TYPE_DAMAGE,500,80,range=AREA_CIRCLE_4,cooldown=7,effectOnSelf=sweetHeatEff,conditionType=["exclusive","secElem",ELEMENT_FIRE],emoji='<:fireStrike:931715107002662912>')
darkSweetHeat = skill("Flammes infernales","zyp",TYPE_DAMAGE,500,60,range=AREA_CIRCLE_4,cooldown=7,effectOnSelf=sweetHeatEff,use=MAGIE,area=AREA_CONE_2,group=SKILL_GROUP_DEMON,conditionType=["exclusive","secElem",ELEMENT_FIRE],emoji='<:infFlames:931716686745305149>')

nacre = effect("Bulle nacrée",'nacre1',HARMONIE,overhealth=35,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,turnInit=2,stackable=True,emoji=uniqueEmoji('<:nacre:931666050322419732>'))
shell = skill("Coquille",'zyo',TYPE_ARMOR,500,range=AREA_CIRCLE_7,use=HARMONIE,effect=nacre,effectOnSelf=nacre,cooldown=5,conditionType=["exclusive","secElem",ELEMENT_WATER],emoji='<:shell:931714079154921472>')
nacreHit = skill("Frappe nacrée",'syn',TYPE_DAMAGE,500,80,range=AREA_CIRCLE_3,effectOnSelf=nacre,cooldown=5,use=HARMONIE,conditionType=["exclusive","secElem",ELEMENT_WATER])
holyShot = skill("Flèche sacrée",'sym',TYPE_DAMAGE,500,130,cooldown=7,group=SKILL_GROUP_HOLY,maxHpCost=10,emoji='<:hollyArrow:931713039789588550>')
demonStrike = skill("Frappe démoniaque",'syl',TYPE_DAMAGE,500,35,cooldown=7,group=SKILL_GROUP_DEMON,area=AREA_CIRCLE_1,repetition=3,hpCost=15,emoji='<:demonStrike:933504978599952404>')
purify = skill("Purification","syk",TYPE_HEAL,250,50,use=CHARISMA,cooldown=5,group=SKILL_GROUP_HOLY,maxHpCost=5,emoji='<:holyHeal1:931703505268408341>')
benediction = skill("Provecta Bénédiction","syj",TYPE_HEAL,750,100,use=CHARISMA,cooldown=8,group=SKILL_GROUP_HOLY,maxHpCost=10,emoji='<:benediction:931703487258046464>')
transfert = skill("Transfert",'svi',TYPE_HEAL,350,55,use=CHARISMA,hpCost=10,group=SKILL_GROUP_DEMON,cooldown=5,emoji='<:transfert:931709644542451734>')
blackDarkMagic = skill("Magie interdite",'svh',TYPE_HEAL,350,100,use=CHARISMA,hpCost=35,group=SKILL_GROUP_DEMON,cooldown=8,emoji='<:darkMagic:931707457020002346>')
fisure = skill("Fissure",'svg',TYPE_DAMAGE,500,70,conditionType=["exclusive","secElem",ELEMENT_EARTH],cooldown=5,damageOnArmor=3,emoji='<:break:931703557420367873>')
seisme = skill("Séisme",'svf',TYPE_DAMAGE,500,60,range=AREA_MONO,area=AREA_CIRCLE_3,conditionType=["exclusive","secElem",ELEMENT_EARTH],cooldown=5,damageOnArmor=3,emoji='<:seisme:931703529561800744>')
burningSoul = effect("Âme embrasée",'burningSoul',HARMONIE,power=25,turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji='<:ayss:931711751702085672>')
abime = skill("Âbime",'sve',TYPE_INDIRECT_DAMAGE,500,area=AREA_CIRCLE_2,cooldown=7,ultimate=True,group=SKILL_GROUP_DEMON,hpCost=25,effect=[burningSoul],emoji='<:abyss:931711751702085672>')
fadingSoul = effect("Anéantissement",'fadingSoul',HARMONIE,power=50,turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji='<:purification:931711772396777572>')
extermination = skill("Extermination",'svd',TYPE_INDIRECT_DAMAGE,500,0,effect=fadingSoul,group=SKILL_GROUP_HOLY,maxHpCost=15,cooldown=7,emoji='<:purification:931711772396777572>')
darkHeal = copy.deepcopy(lightHeal2)
darkHeal.name, darkHeal.id, darkHeal.emoji, darkHeal.condition = "Assombrissement", "svc", '<:darkHeal:931883636481982484>', [0,3,ELEMENT_DARKNESS]
matriceEff2 = copy.deepcopy(dmgUp)
matriceEff2.power = 25
matriceEff1 = effect("Matrice amplificatrice","matriceAmplEff",trigger=TRIGGER_ON_REMOVE,callOnTrigger=matriceEff2)
matriceEmpli = skill("Matrice amplificatrice",'svb',TYPE_BOOST,500,range=AREA_MONO,effect=matriceEff1,cooldown=7,description="Augmente de **{0}%** vos dégâts infligés lors de votre prochain tour".format(matriceEff2.power))
calestJump = skill("Plongeon Céleste",'sva',TYPE_DAMAGE,750,75,range=AREA_DIST_3,area=AREA_CIRCLE_1,tpCac=True,cooldown=7,emoji='<:ceslestJump:931899235270545469>')
lohicaUltLauch = skill("Brûme empoisonée","suz",TYPE_INDIRECT_DAMAGE,750,area=AREA_CIRCLE_2,use=MAGIE,tpCac=True,effect="me",cooldown=7,ultimate=True,emoji='<:brume:931908895083991100>',areaOnSelf=True,description="Téléporte à côté de la cible et empoisonne les alentours")
lohicaUltCastEff = effect("Cast - Brûme empoisonée","lohicaUltCastEff",turnInit=2,silent=True,replique=lohicaUltLauch,emoji=uniqueEmoji('<a:lohicaUltCast:932823354841399296>'))
lohicaUltCast = copy.deepcopy(lohicaUltLauch)
lohicaUltCast.effectOnSelf, lohicaUltCast.effect, lohicaUltCast.tpCac = lohicaUltCastEff, [None], False
fairyFligth = skill("Envolée féérique",'suy',TYPE_DAMAGE,500,65,range=AREA_CIRCLE_1,jumpBack=2,knockback=1,cooldown=5,emoji='<:envolee:941677380181823489>')

aliceDanceEff = effect("En rythme !",'aliceDanceEff',CHARISMA,strength=7,magie=7,description="\"Tous avec moi !\"",emoji=sameSpeciesEmoji('<:dyB:932618243280085062>','<:dyR:932618257960161331>'))
aliceDanceFinal = skill("Chorégraphie Dynamique","corDynFinal",TYPE_BOOST,500,range=AREA_MONO,area=AREA_DONUT_3,effect=aliceDanceEff,emoji='<:dyna:932618114892439613>',use=CHARISMA,cooldown=5,message="{0} se donne à fond !",description="Se met à danser pendant 3 tours, durant lesquels les alliés à portée voient leur statistiques offensives augmenter")
aliceDanceGuideEff1 = effect("Chrorégraphie dynamique",'aliceDanceCastEff1',turnInit=2,silent=True,replique=aliceDanceFinal,emoji=uniqueEmoji('<:dyna:932618114892439613>'),stackable=True)
aliceDanceGuide1 = copy.deepcopy(aliceDanceFinal)
aliceDanceGuide1.effectOnSelf, aliceDanceGuide1.message, aliceDanceGuide1.id = aliceDanceGuideEff1, "{0} continue de danser", "sc"
aliceDanceGuideEff2 = copy.deepcopy(aliceDanceGuideEff1)
aliceDanceGuideEff2.replica = aliceDanceGuide1
aliceDance = copy.deepcopy(aliceDanceGuide1)
aliceDance.effectOnSelf, aliceDance.message = aliceDanceGuideEff2, "{0} commence une {1} !"
auroreEff = effect("Aurore",'auroreEff',CHARISMA,strength=5,magie=5,turnInit=3,emoji=sameSpeciesEmoji("<:aurB:934675375689170995>","<:aurR:934675360946212914>"))
aurore = skill('Aurore','sux',TYPE_BOOST,500,effect=auroreEff,use=CHARISMA,cooldown=7,area=AREA_CIRCLE_1,conditionType=["exclusive","element",ELEMENT_LIGHT],emoji='<:aurore:934675235268087858>')
crepEff = effect("Crépuscule",'crepEff',INTELLIGENCE,strength=-5,magie=-5,turnInit=3,emoji=sameSpeciesEmoji('<:crepB:934675391145201664>','<:crepR:934675411995074560>'))
crep = skill('Crépuscule','suw',TYPE_MALUS,500,effect=crepEff,use=INTELLIGENCE,cooldown=7,area=AREA_CIRCLE_1,conditionType=["exclusive","secElem",ELEMENT_DARKNESS],emoji='<:crepuscule:934675249541292033>')
toMelee = skill('Corps à corps','suv',TYPE_DAMAGE,350,25,tpCac=True,cooldown=3,emoji='<:cac:932765903102291999>',replay=True,range=AREA_CIRCLE_3)
toDistance = skill('Déplacement','suu',TYPE_DAMAGE,350,25,AREA_INLINE_2,cooldown=3,jumpBack=2,emoji='<:dep:932765889017839636>',replay=True)
autoBombRush = skill("Lance-Bombe Robot",'sut',TYPE_SUMMON,750,0,AREA_CIRCLE_4,["exclusive","aspiration",ASPI_NEUTRAL],True,emoji='<:brAuto:933508393036029992>',invocation="Bombe Robot",cooldown=7,description="Invoque 3 Bombes Robots\nSeule la première Bombe Robot est soumise à la limitation d'invocation par équipe",shareCooldown=True)
killerWailUltimate = skill("Haut Perceur 5.1",'sus',TYPE_SUMMON,750,conditionType=["exclusive","aspiration",ASPI_NEUTRAL],ultimate=True,cooldown=10,use=MAGIE,invocation='Haut-Perceur 5.1',emoji='<:killerWail:933516496196497439>',description='Invoque 5 Haut-Perceur 5.1.\nSeul le premier est soumis à la limitation d\'invocation par équipe',shareCooldown=True)
invocSeaker = skill("Invocation - Traqueur",'sur',TYPE_SUMMON,350,range=AREA_CIRCLE_3,cooldown=5,shareCooldown=True,invocation='Traqueur',emoji='<:seeker:933508405463777351>')

darkBoom = skill("Explosion Sombre",'darkBoom',TYPE_DAMAGE,500,int(explosion.power*0.35),cooldown=explosion.cooldown,percing=0,area=AREA_CIRCLE_2,effectOnSelf=explosion.effectOnSelf,sussess=explosion.sussess,setAoEDamge=True,repetition=2,ultimate=True,use=MAGIE,emoji='<a:db2:933676696899551273>',hpCost=30,group=SKILL_GROUP_DEMON,description="Inflige des dégâts dans une grande zone à deux reprises")
darkBoomCastEff = effect("Cast - Explosion Sombre",'castDarkBoom',turnInit=2,replique=darkBoom,emoji=sameSpeciesEmoji('<a:boomCastB:916382499704275005>','<a:boomCastR:916382515135144008>'),silent=True)
darkBoomCast = copy.deepcopy(darkBoom)
darkBoomCast.id, darkBoomCast.power, darkBoomCast.effectOnSelf, darkBoomCast.hpCost = 'suq', 0, darkBoomCastEff, 0
doubleShot = skill("Double Tir",'sup',TYPE_DAMAGE,500,60,repetition=2,conditionType=["exclusive","aspiration",OBSERVATEUR],emoji='<:doubleShot:933506156616368169>',cooldown=5)
harmShot = skill("Tir Harmonique",'suo',TYPE_DAMAGE,500,75,use=HARMONIE,conditionType=["exclusive",'aspiration',TETE_BRULE],cooldown=3,emoji='<:hamShot:933506175633330216>')
mageSkill = skill("Glace",'sun',TYPE_DAMAGE,500,60,conditionType=["exclusive",'aspiration',MAGE],area=AREA_CIRCLE_1,setAoEDamge=True,cooldown=3,use=MAGIE,emoji='<:ice:941494417926270987>')
benitWater = skill("Eau bénite",'sum',TYPE_DAMAGE,500,75,area=AREA_CIRCLE_1,cooldown=3,maxHpCost=5,group=SKILL_GROUP_HOLY,use=MAGIE,emoji='<:holyStrike:931703468652118067>')
tempShare30 = copy.deepcopy(shareTabl[3])
tempShare30.turnInit = 3
shareSkill = skill("Partage divin",'sul',TYPE_HEAL,500,50,use=CHARISMA,maxHpCost=10,cooldown=5,effect=tempShare30,description="Soigne la cible puis lui donne l'effet Partage (30) pendant 3 tours",emoji='<:divineShare:949891460503855125>')
extraMedica = skill("Extra-Medica",'suk',TYPE_HEAL,750,35,AREA_MONO,area=AREA_CIRCLE_2,use=CHARISMA,effect=infraMedica.effect,cooldown=infraMedica.cooldown,group=SKILL_GROUP_HOLY,conditionType=["exclusive",'aspiration',ALTRUISTE],description="Soigne les alliés proches et leur donne l'effet __Infra Médica__ pendant 3 tours",maxHpCost=10,emoji=infraMedica.emoji)

foulleeEff = effect("Foulée légère",'ppUniquePassifEff',turnInit=-1,unclearable=True,power=20,description="Augmente de **{0}%** votre probabilité d'esquiver des attaques")
foullee = skill("Foulée Légère",'suj',TYPE_PASSIVE,350,conditionType=["exclusive","aspiration",POIDS_PLUME],use=None,effectOnSelf=foulleeEff,emoji='<:quicky:934832147511017482>')

lifePulseRegenEff = effect("Rénégénration","lifePulseHeal",CHARISMA,power=20,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,turnInit=3,emoji='<:heal:911735386697519175>',description="Soigne le porteur en début de tour")
lifePulseFinal = skill("Pulsion de vie",'sui',TYPE_HEAL,1000,120,range=AREA_MONO,ultimate=True,cooldown=10,initCooldown=3,area=AREA_CIRCLE_5,effect=lifePulseRegenEff,use=CHARISMA,emoji='<a:lifePulse:934968172107403324>',group=SKILL_GROUP_HOLY,maxHpCost=35,description="Soigne les alliés aux alentours et leur donne un effet de régénération sur la durée",url='https://cdn.discordapp.com/attachments/927195778517184534/934968488550871140/20220124_012750.gif')
lifePulseCastEff = effect("Cast - Pulsion de vie",'lifePulseCast',replique=lifePulseFinal,silent=True,turnInit=2,emoji='<a:lifePulseCast:934968316882219068>')
lifePulseCast = copy.deepcopy(lifePulseFinal)
lifePulseCast.power, lifePulseCast.effectOnSelf, lifePulseCast.url, lifePulseCast.maxHpCost, lifePulseCast.effect = 0, lifePulseCastEff, None, 0, [None]

crimsomLotus = skill("Lotus Pourpre",'suh',TYPE_DAMAGE,750,transObs.power,emoji='<a:crimsomLotus:934980446176047104>',area=AREA_LINE_6,use=CHARISMA,useActionStats=ACT_BOOST,description="Inflige des dégâts Charisme sur une ligne droite",cooldown=7,ultimate=True,url='https://cdn.discordapp.com/attachments/927195778517184534/934981029649874974/20220124_021239.gif',conditionType=["exclusive","aspiration",IDOLE])
crimsomLotusCastEff = effect("Cast - Lotus Pourpre",'crimstomLotusCastEff',turnInit=2,replique=crimsomLotus,silent=True,emoji=uniqueEmoji('<a:emoji_52:934980282577203210>'))
crimsomLotusCast = copy.deepcopy(crimsomLotus)
crimsomLotusCast.power, crimsomLotusCast.effectOnSelf, crimsomLotusCast.url = 0, crimsomLotusCastEff, None

abnegation = skill("Abnégation",'sug',TYPE_HEAL,750,int(memAlice.power * 1.1),emoji='<:abnegation:935538856286109726>',range=AREA_MONO,area=AREA_CIRCLE_5,group=SKILL_GROUP_DEMON,hpCost=90,ultimate=True,cooldown=7,use=CHARISMA,description="Soigne ou réanime vos alliés à portée au prix d'une grande quantité de PV",effectAroundCaster=[TYPE_RESURECTION,AREA_CIRCLE_5,100])

jumpedSplashDownLanding = copy.deepcopy(classicSplashdown)
jumpedSplashDownLanding.name, jumpedSplashDownLanding.range, jumpedSplashDownLanding.tpCac, jumpedSplashDownLanding.areaOnSelf, jumpedSplashDownLanding.url, jumpedSplashDownLanding.cooldown = "Choc Chromatique Sauté", AREA_DIST_5, True, True, "https://cdn.discordapp.com/attachments/935769576808013837/935781564145623131/20220126_072054.gif", 7
jsdJumEff = effect("Cast - Choc Chromatique Sauté", 'JumpingSlashDownEff',turnInit=2,silent=True,emoji=classicSplashdown.emoji,invisible=True,immunity=True,replique=jumpedSplashDownLanding)
jumpedSplashDown = copy.deepcopy(jumpedSplashDownLanding)
jumpedSplashDown.power, jumpedSplashDown.tpCac, jumpedSplashDown.url, jumpedSplashDown.effectOnSelf = 0, False, None, jsdJumEff

splashdown = skill("Choc Chromatique",classicSplashdown.id,TYPE_DAMAGE,750,0,ultimate=True,emoji=classicSplashdown.emoji,become=[classicSplashdown,jumpedSplashDown],area=AREA_CIRCLE_2)
pneumaArmor = effect("Pneuma",'pneumaArmor',INTELLIGENCE,overhealth=50,type=TYPE_ARMOR,trigger=TRIGGER_START_OF_TURN)
pneuma = skill("Pneuma",'suf',TYPE_DAMAGE,750,125,conditionType=["exclusive","aspiration",PREVOYANT],ultimate=True,emoji='<:pneuma:936515231562219581>',cooldown=7,area=AREA_LINE_3,sussess=110,use=INTELLIGENCE,useActionStats=ACT_SHIELD,effectAroundCaster=[TYPE_ARMOR,AREA_CIRCLE_2,pneumaArmor])

absorbingStrike = skill("Frappe Convertissante",'sue',TYPE_DAMAGE,500,50,AREA_CIRCLE_2,cooldown=3,emoji='<:healStrike:936470624921075733>',lifeSteal=35)
absorbingArrow = skill("Flèche Convertissante",'sud',TYPE_DAMAGE,500,50,AREA_DIST_6,cooldown=3,emoji='<:healShot:936470641450815538>',lifeSteal=35)
absorbingStrike2 = skill("Provecta Frappe Convertissante",'suc',TYPE_DAMAGE,750,120,AREA_CIRCLE_2,cooldown=7,emoji='<:killStrike:936470659389849622>',lifeSteal=50)
absorbingArrow2 = skill("Provecta Flèche Convertissante",'sub',TYPE_DAMAGE,750,120,AREA_DIST_6,cooldown=7,emoji='<:killShot:936470681015709716>',lifeSteal=50)
vampStrikeEff = effect("Vampirisme","no",power=25,type=TYPE_HEAL,stat=MAGIE,trigger=TRIGGER_AFTER_DAMAGE,description="Accorde au porteur un certain pourcentage de vol de vie, augmenté par les statistiques de l'entité à l'origine de l'effet",emoji=sameSpeciesEmoji('<:vampireB:900313575913062442>','<:vampireR:900313598130282496>'))
magiaHeal = skill("Sort Vampirique","sua",TYPE_DAMAGE,500,80,use=MAGIE,lifeSteal=50,cooldown=5,emoji='<:vampireSpell:961190223168024606>',effectOnSelf=vampStrikeEff)

aff2Eff1 = copy.deepcopy(vulne)
aff2Eff1.power, aff2Eff1.stat, aff2Eff1.description = 3, INTELLIGENCE, "Augmente les dégâts subis par le porteur de **3%**, affecté par les statistiques"
aff2Eff2 = copy.deepcopy(dmgDown)
aff2Eff2.power, aff2Eff2.stat, aff2Eff2.description = 3, INTELLIGENCE, "Réduit les dégâts infligés par le porteur de **3%**, affecté par les statistiques"

bloodPactEff = effect("Pacte de sang",'bloodyPact',power=75,turnInit=-1,emoji='<:bloodpact:937361536043843595>',unclearable=True,description="Augmente de **{0}%** le taux de vol de vie des Berskers mais réduit de **15%** les soins reçus par n'importe quelle autre source")
bloodPact = skill("Pacte de sang",'sty',TYPE_PASSIVE,500,use=None,conditionType=["exclusive","aspiration",BERSERK],effectOnSelf=bloodPactEff,emoji='<:bloodpact:937361536043843595>')
aff2 = skill("Provecta Affaiblissement",'stz',TYPE_MALUS,500,area=AREA_CIRCLE_1,use=INTELLIGENCE,effect=[aff2Eff1,aff2Eff2],cooldown=5,emoji='<:affaib2:963394071894835220>')

expediantDefenseUp = copy.deepcopy(defenseUp)
expediantDefenseUp.power, expediantDefenseUp.stat, expediantDefenseUp.description = 7, INTELLIGENCE, "Réduit de **7%** les dégâts subis par le porteur, affectés par les statistiques"
expediantSpeedBoost = effect("Thèse des rafales hurlantes",'expediantSpeedBooost',INTELLIGENCE,agility=10,emoji='<:expediant:937370418363367495>')
expediant = skill("Thèse fluidiques",'stx',TYPE_BOOST,750,range=AREA_MONO,area=AREA_CIRCLE_3,use=INTELLIGENCE,cooldown=7,effect=[expediantDefenseUp,expediantSpeedBoost],emoji='<:expediant:937370418363367495>')
dinationEff = copy.deepcopy(dmgUp)
dinationEff.power, dinationEff.stat, dinationEff.turnInit = 4, INTELLIGENCE, 3
divination = skill("Divination",'stw',TYPE_BOOST,500,range=AREA_MONO,area=AREA_CIRCLE_3,use=INTELLIGENCE,cooldown=7,effect=dinationEff,emoji='<:divination:937370483777748993>')
macroCosmosEff = copy.deepcopy(dmgUp)
macroCosmosEff.power = 5
macroCosmos = skill("Macro-cosmos",'stv',TYPE_DAMAGE,500,130,area=AREA_CIRCLE_1,effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_2,macroCosmosEff],cooldown=5,ultimate=True,use=INTELLIGENCE,useActionStats=ACT_BOOST,description="Inflige des dégâts aux ennemis et augmente les DI des alliés",emoji='<:macroCosmos:937370437573287997>')
tintabuleEff = effect("Tintinnabule",'tintabule',CHARISMA,power=20,turnInit=3,lvl=5,type=TYPE_INDIRECT_HEAL,area=AREA_CIRCLE_2,emoji='<:tintabulbe:937370359257255976>',trigger=TRIGGER_AFTER_DAMAGE,description="Lors des 5 prochaines attaques subie par le porteur, soigne ce dernier et ses alliés dans la zone d'effet")
tintabule = skill("Tintinnabule",'stu',TYPE_INDIRECT_HEAL,500,effect=tintabuleEff,cooldown=5,emoji='<:tintabulbe:937370359257255976>')

verEarthEff = effect("VerTerre préparé",'verEarthReady',turnInit=5,emoji='<:verTerre:937807119934160917>')
verMiracleEff = effect("VerMiracle préparé",'verMiracleReady',turnInit=5,emoji='<:verMiracle:937807083447943288>')
verFire = skill("VerFeu",'stt',TYPE_DAMAGE,power=70,emoji='<:verFeu:937807102209060894>',use=MAGIE,effectOnSelf=verEarthEff,rejectEffect=[verEarthEff,verMiracleEff])
verEarth = skill("VerTerre",'stt',TYPE_DAMAGE,power=90,emoji='<:verTerre:937807119934160917>',use=MAGIE,needEffect=verEarthEff,effectOnSelf=verMiracleEff,cooldown=2)
verMiracle = skill("VerMiracle",'stt',TYPE_DAMAGE,power=145,emoji='<:verMiracle:937807083447943288>',use=MAGIE,needEffect=verMiracleEff,cooldown=5)
comboVerMiracle = skill("Combo VerMiracle",'stt',TYPE_DAMAGE,500,verMiracle.power,area=AREA_CIRCLE_1,emoji=verMiracle.emoji,become=[verFire,verEarth,verMiracle],use=MAGIE,description="Cette compétence permet d'effectuer l'enchaînement \"VerFeu\",\"VerTerre\" et \"VerMiracle\".\nIl est impossible d'utiliser \"VerMiracle\" sans avoir utilisé \"VerTerre\" précédament, lui-même necessitant d'avoir utlisé \"VerFeu\" au paravant")

faucheCroixEff = effect('Fauchage croisé préparé','faucheCroixReady',turnInit=6,emoji='<:faucheCroix:937807152058343474>')
faucheNean = skill("Fauchage du néan",'sts',TYPE_DAMAGE,power=100,range=AREA_CIRCLE_2,area=AREA_ARC_1,cooldown=3,emoji='<:faucheNean:937807137306976337>',rejectEffect=faucheCroixEff,effectOnSelf=faucheCroixEff)
faucheCroix = skill("Fauchage croisé",'sts',TYPE_DAMAGE,power=145,range=AREA_CIRCLE_2,needEffect=faucheCroixEff,cooldown=5,area=AREA_ARC_2,emoji='<:faucheCroix:937807152058343474>')
comboFaucheCroix = skill("Combo Fauchage croisé",'sts',TYPE_DAMAGE,price=500,power=faucheCroix.power,emoji=faucheCroix.emoji,become=[faucheNean,faucheCroix],description="Permet d'effectuer l'enchaînement \"Fauchage du néan\" et \"Fauchage croisé\".\nIl est nécessaire d'avoir préalablement utilisé \"Fauchage du néan\" pour pouvoir utiliser \"Fauchage croisé\"")

reaperEff = effect("Dessins de la Camarade", "that'sALongName", power=35, turnInit=4, type=TYPE_MALUS, emoji="<:longName:938167649106538556>",description="Augmente de **10%** les dégâts infligés par l'entité à l'origine de cet effect sur le porteur.\nSi le porteur est vaincu en ayant toujours l'effet sur lui (que ce soit de la main de l'initiateur de l'effet ou d'un autre), l'initiateur de l'effet se soigne de **{0}%** de ses PV maximums")
deathShadow = skill("Ombre de la Mort","str",TYPE_DAMAGE,750,50,range=AREA_CIRCLE_2,emoji='<:deathShadow:937370374788755516>',cooldown=7,effect=reaperEff,description="Inflige des dégâts et donne à la cible augmentant vos futurs dégâts à son encontre pendant plusieurs tours")
theEnd = skill("Dernier Voyage","stq",TYPE_DAMAGE,750,200,AREA_CIRCLE_3,cooldown=5,tpCac=True,ultimate=True,emoji='<a:lbReaper:938175619504689193>',damageOnArmor=1.35,description="Après un tour de chargement, délivre une puissante attaque à l'ennemi ciblé.\nSi cette dernière est sous un effet <:longName:938167649106538556> __Dessins de la Camarade__ dont vous êtes l'initiateur, la puissance de cette attaque augmente de **20%**",lifeSteal=25,url='https://cdn.discordapp.com/attachments/935769576808013837/938175773137862756/20220201_214401.gif')
theEndCastEff = effect("Cast - Dernier Voyage","reaperLbCast",turnInit=2,silent=True,replique=theEnd,emoji='<a:lbReaperCast:938175259964747816>')
theEndCast = copy.deepcopy(theEnd)
theEndCast.power, theEndCast.url, theEndCast.effectOnSelf, theEndCast.tpCac = 0, None, theEndCastEff, False

cure3Eff = effect("Extra Soins Préparé","cureIIready",turnInit=4,emoji='<:extraHeal:952522927214051348>')
cure2 = skill("Soins","stp",TYPE_HEAL,0,40,emoji='<:heal:911735386697519175>',effectOnSelf=cure3Eff,use=CHARISMA,rejectEffect=[cure3Eff])
cure3 = skill("Extra Soins","spt",TYPE_HEAL,0,55,emoji='<:extraHeal:952522927214051348>', needEffect=cure3Eff,cooldown=3,use=CHARISMA,area=AREA_CIRCLE_1)
cure2Bundle = skill("Extra Soins","stp",TYPE_HEAL,500,use=CHARISMA,become=[cure2,cure3],emoji='<:extraHeal:952522927214051348>',description="Permet d'utiliser les compétences {0} __{1}__ et {2} __{3}__.\n{2} __{3}__ ne peut être utilisé que si {0} __{1}__ a été utilisé préalablement".format(cure2.emoji,cure2.name,cure3.emoji,cure3.name))

assises = skill("Assises","sto",TYPE_DAMAGE,750,135,area=AREA_CIRCLE_1,use=CHARISMA,cooldown=7,effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_2,65],conditionType=["exclusive","aspiration",ALTRUISTE],emoji='<:assise:941494380714414110>',description="Inflige des dégâts aux ennemis ciblés et soigne les alliés autour de vous")
debouses = skill("Debouses","stl",TYPE_HEAL,750,75,area=AREA_CIRCLE_1,use=CHARISMA,cooldown=7,effectAroundCaster=[TYPE_DAMAGE,AREA_CIRCLE_2,75],conditionType=["exclusive","aspiration",VIGILANT],emoji='<:debouse:941494363748438027>',description="Soigne les alliés ciblés et inflige des dégâts autour de vous")

impactShield = effect("Armure Impactante",'impactArmor',INTELLIGENCE,overhealth=35,emoji='<:impact:951379371489382400>',turnInit=3,stackable=True,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,description="Protège de quelques dégâts directs")
impact = skill("Frappe Impactante","stk",TYPE_DAMAGE,500,50,AREA_CIRCLE_3,["exclusive","aspiration",PROTECTEUR],emoji='<:impact:941494342722412585>',effectOnSelf=impactShield,use=INTELLIGENCE,useActionStats=ACT_SHIELD,effectAroundCaster=[TYPE_HEAL,AREA_MONO,35],cooldown=3,description="En plus d'infliger quelques dégâts, cette compétence soigne et donne une petite armure au lanceur")
heartStoneSecEff = copy.deepcopy(defenseUp)
heartStoneSecEff.power, heartStoneSecEff.stat = 5, INTELLIGENCE
heartStone = skill("Coeur de pierre","stj",TYPE_ARMOR,750,cooldown=3,emoji='<:earthStonr:941681433863421952>',effect=[impactShield, heartStoneSecEff],conditionType=["exclusive","aspiration",PROTECTEUR],description="Confère une petite armure à l'allié ciblé et réduit ses dégâts reçus\nL'armure dure plus longtemps que la réduction de dégâts")
erodStrike = skill("Frappe érosive","sti",TYPE_DAMAGE,500,100,AREA_CIRCLE_3,cooldown=5,erosion=35,emoji='<:frappeEro:941677350872047640>')

genesis = skill("Génésis","sth",TYPE_DAMAGE,750,200,area=AREA_LINE_4,group=SKILL_GROUP_HOLY,use=MAGIE,maxHpCost=35,cooldown=7,emoji='<:genesis:946529693459419217>')
invertion = skill("Inversion",'stg',TYPE_DAMAGE,500,80,group=SKILL_GROUP_DEMON,use=CHARISMA,useActionStats=ACT_HEAL,hpCost=15,cooldown=4)
ice2Eff = effect("Glace II","ice2Eff",MAGIE,power=60,area=AREA_CIRCLE_1,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji='<:ice2:941494399337136208>')
ice2 = skill("Glace II","stf",TYPE_INDIRECT_DAMAGE,500,use=MAGIE,cooldown=3,emoji='<:ice2:941494399337136208>',conditionType=["exclusive","aspiration",SORCELER],effect=ice2Eff)
lifeWind = skill("Vent de vie","ste",TYPE_HEAL,500,50,AREA_MONO,["exclusive","aspiration",VIGILANT],area=AREA_CIRCLE_2,use=CHARISMA,cooldown=4,emoji='<:divineWind:949888558355869747>')
renf2Eff1 = copy.deepcopy(defenseUp)
renf2Eff1.power, renf2Eff1.stat = 5, INTELLIGENCE
renf2Eff2 = copy.deepcopy(dmgUp)
renf2Eff2.power, renf2Eff2.stat = 5, INTELLIGENCE
renf2Eff3 = effect("Renforcement IV","renf4",INTELLIGENCE,strength=5,magie=5,resistance=5)
renf2 = skill("Provecta Renforcement","std",TYPE_BOOST,750,conditionType=["exclusive","aspiration",INOVATEUR],effect=[renf2Eff3,renf2Eff1,renf2Eff2],cooldown=7)
entraide = skill("Entraide","stc",TYPE_HEAL,500,100,area=AREA_CIRCLE_1,cooldown=7,group=SKILL_GROUP_DEMON,hpCost=35,use=CHARISMA,emoji='<:entraide:941677392722808913>')
perfectShot = skill("Tir Parfait","stb",TYPE_DAMAGE,750,180,cooldown=10,ultimate=True,emoji='<:tirParfait:961187760134311996>')
lastRessource = skill("Dernier recours","sta",TYPE_RESURECTION,500,135,cooldown=7,shareCooldown=True,use=STRENGTH,initCooldown=5,emoji='<:strengthRaise:949890176195383318>')
strengthOfDesepearance = skill("Force du désespoir","ssz",TYPE_RESURECTION,500,135,cooldown=7,shareCooldown=True,use=MAGIE,initCooldown=5,emoji='<:magicRaise:949890198190305300>')
nova = skill("Nova","ssy",TYPE_DAMAGE,500,80,use=INTELLIGENCE,useActionStats=ACT_SHIELD,hpCost=15,cooldown=4,group=SKILL_GROUP_DEMON)
undeadEff2 = effect("Mort en sursie","undeadEff2",turnInit=3,description="Tant que cet effet est actif, le porteur ne peut pas être vaincu\nCet effet est retiré si le porteur est soigné d'un montant égalant **100%** de ses PV max au moment de la pose de l'effet durant sa durée\nSi l'effet atteint la fin de sa durée, le porteur est automatiquement vaincu\nAugmente les soins reçus et accorde un bonus de vol de vie de **{0}** tant que l'effet est actif",emoji='<a:undead:953259661568663602>',silent=False,power=50)
undeadEff = effect("Mort-Vivant","undead",turnInit=-1,callOnTrigger=undeadEff2,description="1 fois par combats, en recevant des dégâts mortels, le porteur survie avec **1 PV** et obtiens l'effet {0} __{1}__".format(undeadEff2.emoji[0][0],undeadEff2.name),emoji='<:undead:944989590836637736>',silent=False)
undead = skill("Mort Vivant","ssx",TYPE_PASSIVE,500,effectOnSelf=undeadEff,emoji='<:undead:944989590836637736>',group=SKILL_GROUP_DEMON)

ironStormDmgBoost = copy.deepcopy(dmgUp)
ironStormDmgBoost.power = 10
ironStormReady = effect('Tempête de Fer préparée','ironStormReady',turnInit=3,emoji='<:ironStorm3:945054940412383332>')
ironStorm = skill("Tempête de fer","ssw",TYPE_DAMAGE,power=80,range=AREA_CIRCLE_2,emoji='<:ironStorm3:945054940412383332>',cooldown=3,effectOnSelf=ironStormDmgBoost,description="Inflige des dégâts puis augmente vos dégâts de 10% pour le prochain tour",needEffect=ironStormReady)
mutilationReady = effect("Mutilation préparée","mutilationReady",turnInit=3,emoji='<:ironStorm2:945054925291925554>')
mutilation = skill('Mutilation',"ssw",TYPE_DAMAGE,power=70,range=AREA_CIRCLE_2,emoji='<:ironStorm2:945054925291925554>',effectOnSelf=ironStormReady,needEffect=mutilationReady,rejectEffect=ironStormReady)
powerStrike = skill("Coup puissant","ssw",TYPE_DAMAGE,power=60,range=AREA_CIRCLE_2,rejectEffect=[mutilationReady,ironStormReady],effectOnSelf=mutilationReady,emoji='<:ironStorm1:945054903452180500>')
ironStormBundle = skill("Combo Tempête de Fer","ssw",TYPE_DAMAGE,500,become=[powerStrike,mutilation,ironStorm],description="Permet d'effetuer l'enchaînement Coup Puissant, Mutilation et Tempête de Fer\nLes compétences doivent être effectuée dans cet ordre définis\n\n__Tempête de Fer__ augmente vos dégâts de 10% pour le tour suivant",emoji='<:ironStorm3:945054940412383332>')
bolideEff = effect("Bolide",'vroumvroum',immunity=True,emoji='<:bolide:945058044495167538>',description="Le porteur est insensible à tous dégâts")
bolide = skill("Bolide","ssv",TYPE_BOOST,500,range=AREA_MONO,effect=bolideEff,cooldown=7,use=None,emoji='<:bolide:945058044495167538>',description="Réduit vos PV courrants à **1**, puis vous rend invulnérable à tous dégâts pendant un tour")
invincibleEff = effect("Invincible","borringImunity",immunity=True,emoji='<:invincible:945054839203852359>',description="Le porteur est insensible à tous dégâts")
invincible = skill("Invincible","ssu",TYPE_BOOST,750,range=AREA_MONO,emoji='<:invincible:945054839203852359>',use=None,cooldown=15,effectOnSelf=invincibleEff,description="Vous rend invulnérable à tous dégâts pendant un tour")
holmgangEff = effect("Holmgang","Holmgang",emoji='<:complicated:945054889573240883>',description="Cet effet empêche le porteur de tomber en dessous de **1** PV")
holmgang = skill("Holmgang","sst",TYPE_BOOST,500,range=AREA_MONO,emoji='<:complicated:945054889573240883>',use=None,effect=holmgangEff,cooldown=7,description="Empêche vos PV de tomber en dessous de 1 pendant 1 tour")

extraVerFoudreReady = effect("Extra VerFoudre préparé","extraVerFoudreReady",turnInit=5,emoji='<:extraVerFoudre:946042839287091300>')
verBrasierReady = effect("VerBrasier Préparé","verBrasierReady",emoji="<:verBrasier:946042912511250522>",turnInit=5)
extraVerVent = skill("Extra VerVent","sss",TYPE_DAMAGE,power=60,area=AREA_CIRCLE_1,use=MAGIE,effectOnSelf=extraVerFoudreReady,emoji='<:extraVerVent:946042871176396871>',rejectEffect=[extraVerFoudreReady,verBrasierReady])
extraVerFoudre = skill("Extra VerFoudre","sss",TYPE_DAMAGE,power=60,area=AREA_CIRCLE_1,use=MAGIE,needEffect=extraVerFoudreReady,effectOnSelf=verBrasierReady,emoji='<:extraVerFoudre:946042839287091300>')
verBrasier = skill("VerBrasier",'sss',TYPE_DAMAGE,power=100,area=AREA_CIRCLE_1,emoji='<:verBrasier:946042912511250522>',cooldown=3,use=MAGIE,needEffect=verBrasierReady)
comboVerBrasier = skill("Combo VerBrasier",'sss',TYPE_DAMAGE,500,power=verBrasier.power,emoji=verBrasier.emoji,become=[extraVerVent,extraVerFoudre,verBrasier],use=MAGIE,description="Permet d'effectuer l'enchaînement __Extra VerVent__, __Extra VerFoudre__ et __Ver Miracle__.\nLes compétences doivent être utilisée dans l'odre précédament énoncé")
phoenixFlight = effect("Vol du phénix","phoenixFlight",MAGIE,power=15,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji='<:voldevie:946042594616561715>')
galvanisation = skill("Galvanisation",'ssr',TYPE_DAMAGE,750,emoji='<:galvaPheonix:946042576413290506>',area=AREA_CIRCLE_1,power=125,use=MAGIE,effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_CIRCLE_2,phoenixFlight],cooldown=7,description="Inflige des dégâts aux ennemis ciblés et donne un effet régénérant aux alliés autour de vous\n\n{0} __{1}__ :\nSoigne le porteur avec une puissance de **{2}** en utilisant la statistique de magie pendant 3 tours".format(phoenixFlight.emoji[0][0],phoenixFlight.name,phoenixFlight.power))
contreDeSixte = skill("Contre de Sixte",'ssq',TYPE_DAMAGE,350,75,area=AREA_CIRCLE_1,cooldown=3,emoji='<:contreDeSixte:946042932643913788>')
selenShield = effect("Armure sélènomantique","selenArmor",INTELLIGENCE,overhealth=40,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
selenomancie = skill("Sélènomancie","ssp",TYPE_ARMOR,500,range=AREA_MONO,area=AREA_CIRCLE_2,effect=selenShield,cooldown=5,conditionType=["exclusive","aspiration",PROTECTEUR],use=INTELLIGENCE,emoji='<:selenomancie:949888629721927730>')
helioRegen = effect("Régénération hélomancique","helioRegen",CHARISMA,power=25,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN)
holiomancie = skill("Héliomancie",'sso',TYPE_INDIRECT_HEAL,500,effect=helioRegen,use=CHARISMA,area=AREA_CIRCLE_2,range=AREA_MONO,cooldown=5,conditionType=["exclusive","aspiration",VIGILANT],emoji='<:heliomancie:949888728116133889>')
partnerIn = effect("Position raprochée","partE",turnInit=-1,unclearable=True,description="En rélisant une compétence de Boost utilisable uniquement sur soi même, la zone d'effet de cette compétence est répliquée sur le porteur de <:partB:949074187513905172> __Partenaire de Position Rapprochée__.\n\nLes alliés se trouvant uniquement dans cette deuxième air d'effet bénificie du bonus de la compétence avec des bonus équivalants à **{0} %** de l'effet de base",power=35,emoji='<:partA:949074204333047809>')
partnerOut = effect("Partenaire de position rapprochée","partS",turnInit=-1,unclearable=True,description="Tant que le porteur est en état de se battre, permet d'étendre les zones d'effets de certaines compétences de l'entité à l'origine de cet effet",emoji='<:partB:949074187513905172>')
partner = skill("Position Raprochée","ssn",TYPE_PASSIVE,750,effectOnSelf=partnerIn,effect=partnerOut,emoji='<:partnaire:949075450360123482>',description="Vous confère l'effet {0} __{1}__ et donne l'effet {2} __{3}__ à un autre allié aléatoire au début du combat".format(partnerIn.emoji[0][0],partnerIn.name,partnerOut.emoji[0][0],partnerOut.name))
exhibitionnisme = skill("Exhibitionnisme","ssm",TYPE_MALUS,69,range=AREA_MONO,area=AREA_CIRCLE_4,cooldown=7,effect=unHolly.effect[0],group=SKILL_GROUP_DEMON,use=CHARISMA,hpCost=20,emoji='<:exhibitionnisme:949893142402990120>')
invocTitania = skill("Invocation - Titania","ssl",TYPE_SUMMON,750,invocation="Titania",ultimate=True,cooldown=10,emoji='<:smnTitania:950210129276579871>',shareCooldown=True,url='https://cdn.discordapp.com/attachments/927195778517184534/932704180731265054/20220117_193200.gif')
demonBloodEff = effect("Sang de Démon","demonBloodEff",CHARISMA,strength=10,magie=10,endurance=5,turnInit=3)
dmonBlood = skill("Sang de Démon","ssk",TYPE_BOOST,500,emoji='<:dmonBlood:950256044322459649>',range=AREA_MONO,area=AREA_CIRCLE_4,effect=demonBloodEff,hpCost=20,cooldown=7,group=SKILL_GROUP_DEMON,description="Augmente la Force, la Magie et l'Endurance des alliés affectés pendant 3 tours")
hollyGroundEff = copy.deepcopy(defenseUp)
hollyGroundEff.power, hollyGroundEff.stat, hollyGroundEff.turnInit = 10, INTELLIGENCE, 2
hollyGround = skill("Terre Sacrée I","ssj",TYPE_BOOST,750,emoji='<:holyGroundI:950254446611431455>',range=AREA_MONO,area=AREA_CIRCLE_2,effect=hollyGroundEff,cooldown=7,maxHpCost=25,group=SKILL_GROUP_HOLY,description="Réduit les dégâts subis par les alliés aux alentours au prix de 25% des PV max")
hollyGround2Eff = effect("Provecta Terre Sacrée","hollyGroundIIEff",stat=CHARISMA,charisma=10,intelligence=10,precision=5,turnInit=3)
hollyGround2 = skill("Provecta Terre Sacrée","ssi",TYPE_BOOST,750,emoji='<:holyGroundII:950254462449115136>',range=AREA_MONO,area=AREA_CIRCLE_4,effect=hollyGround2Eff,cooldown=7,group=SKILL_GROUP_HOLY,description="Augmente le Charisme, l'Intelligence et la Précision des alliés dans la zone d'effet au prix de 15% des PV max",maxHpCost=15)
burningGroundEff = copy.deepcopy(dmgUp)
burningGroundEff.power, burningGroundEff.stat, burningGroundEff.turnInit = 10, INTELLIGENCE, 2
burningGround = skill("Terre Brulée","ssh",TYPE_BOOST,750,emoji='<:burningGround:950256060923535370>',range=AREA_MONO,area=AREA_CIRCLE_2,effect=burningGroundEff,cooldown=7,hpCost=40,group=SKILL_GROUP_DEMON,description="Augmente les dégâts infligés par les alliés à portée au prix de 40% des PV actuels")
blueShell = skill("Carapace à épines","ssg",TYPE_DAMAGE,500,85,AREA_CIRCLE_7,area=AREA_CIRCLE_1,setAoEDamge=True,emoji='<:blue:950231849337233448>',cooldown=7,description="Inflige de dégâts en zone sur l'ennemi ayant réalisé le plus de dégâts")
preciChiEff = effect("Précision Chirurgicale","preciChiru",None,emoji=sameSpeciesEmoji('<:preciChiru:951692831230140437>','<:preciChiruR:951692959131267073>'),turnInit=-1,unclearable=True,reject=["ironHealth"],description="Augmente de **{0}%** votre probabilité d'effectuer des Soins ou Armures Critiques\nAugmente de **{0}%** la valeur des Soins ou Armures Critiques réalisés",power=10)
preciChi = skill("Précision Chirurgicale","ssf",TYPE_PASSIVE,500,effectOnSelf=preciChiEff,emoji='<:preciChiru:951692831230140437>')
ironHealthEff = effect("Santé de Fer","ironHealth",turnInit=-1,unclearable=True,emoji='<:ironHealth:951692715727409253>',reject=[preciChiEff.id],description="Augmente de **{0}%** la probabilité qu'on les autres d'effectuer des Soins ou Armures Critiques sur vous\nAugmente de **{0}%** la valeur des Soins ou Armures Critiques réalisés par autruis sur vous",power=10)
ironHealth = skill("Santé de Fer","sse",TYPE_PASSIVE,500,effectOnSelf=ironHealthEff,emoji='<:ironHealth:951692715727409253>')
windBurn = effect("Morsure du vent","windBurn",AGILITY,power=25,turnInit=3,lvl=3,area=AREA_DONUT_1,emoji='<:windBite:961185646993637476>',trigger=TRIGGER_END_OF_TURN,description="Inflige des dégâts magiques aux ennemis aux corps à corps du porteur à la fin du tour de celui-ci",type=TYPE_INDIRECT_DAMAGE)
windBal = skill("Balleyage éventé",'ssd',TYPE_DAMAGE,500,50,range=AREA_CIRCLE_1,use=AGILITY,emoji='<:windBite:961185646993637476>',cooldown=7,effectAroundCaster=[TYPE_DAMAGE,AREA_CIRCLE_1,50],effectOnSelf=windBurn,description="Inflige des dégâts à l'ennemi ciblé, puis aux ennemis à votre corps à coprs tout en vous octroyant un effet infligeant passivement des dégâts aux ennemis à votre corps à corps",conditionType=["exclusive","element",ELEMENT_AIR])
brasier2Eff = effect("Brûlure","brasier2Eff",MAGIE,power=25,turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE)
brasier2 = skill("Provecta Brasier","ssc",TYPE_DAMAGE,500,50,range=AREA_DIST_5,area=AREA_CIRCLE_2,use=MAGIE,emoji='<:brasier3:961185593482682398>',effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_CIRCLE_2,brasier2Eff],setAoEDamge=True,conditionType=["exclusive","element",ELEMENT_FIRE],cooldown=5,ultimate=True,description="Inflige des dégâts aux ennemis dans la zone d'effet toute en infligeant un effet de dégâts sur la durée aux ennemis proche de vous\n__Puissance (Brûlure) :__ **{0}** ({1} tours)".format(brasier2Eff.power, brasier2Eff.turnInit))
earthUlt2Shield = effect("Armure Tellurique","earthUlt2Shield",ENDURANCE,emoji='<:liuArmor:922292960886915103>',overhealth=80,turnInit=3,trigger=TRIGGER_DAMAGE,type=TYPE_DAMAGE,inkResistance=10)
earthUlt2Lanch = skill("Fureur Tellurique","ssb",TYPE_DAMAGE,750,125,emoji='<:furTellu:951700536732823622>',range=AREA_MONO,area=AREA_CIRCLE_1,conditionType=["exclusive","element",ELEMENT_EARTH],use=ENDURANCE,setAoEDamge=True,effectOnSelf=earthUlt2Shield,description="Inflige des dégâts aux ennemis à votre corps à corps et vous octrois une armure réduisant également les dégâts indirects reçus",ultimate=True,cooldown=7)
earthUlt2CastEff = effect("Cast - {0}".format(earthUlt2Lanch.name),"castEarthUlt2",turnInit=2,silent=True,replique=earthUlt2Lanch)
earthUlt2 = copy.deepcopy(earthUlt2Lanch)
earthUlt2.power, earthUlt2.effectOnSelf = 0, earthUlt2CastEff
geyser = skill("Geyser","ssa",TYPE_DAMAGE,500,75,area=AREA_CIRCLE_1,emoji='<:geyser:961185615859290163>',cooldown=5,conditionType=["exclusive","element",ELEMENT_WATER],use=MAGIE)
rouletteEff = effect("Pile ou Face","pileouface",dmgUp = -50, critDmgUp= 100,turnInit=2,description="Augmente vos dégâts critiques infligés de **100%**, mais réduit vos dégâts non critiques de **50%**")
rouletteSkill = skill("Pile ou face","srz",TYPE_BOOST,350,range=AREA_MONO,cooldown=5,effect=rouletteEff,description="Lors de votre prochain tour, les dégâts critiques sont doublés, mais réduits de moitié sinon",emoji='<a:rotativeYPositiveCoin:917927342918221865>')
constEffI = effect("Constance","const1Eff",dmgUp=5,emoji=sameSpeciesEmoji('<:cst:951692626506178620>','<:ctsR:951692410155569172>'),critDmgUp=-15,turnInit=-1,unclearable=True,description="Augmente vos dégâts non critiques de **5%** mais réduit vos dégâts critiques de **15%**")
constEffII = effect("Constance Critique","const2Eff",emoji=sameSpeciesEmoji('<:cstCrit:951692598182027314>','<:cstCritR:951692193045835816>'),dmgUp=-10,critDmgUp=5,turnInit=-1,unclearable=True,description="Augmente vos dégâts critiques de **5%** mais réduit vos dégâts non critiques de **10%**")
constance = skill("Constance","sry",TYPE_PASSIVE,500,emoji='<:cst:951692626506178620>',effectOnSelf=constEffI,use=None,description="Augmente vos dégâts non critique au dépriment de vos dégâts critiques")
constance2 = skill("Constance Critique","srx",TYPE_PASSIVE,500,effectOnSelf=constEffII,emoji='<:cstCrit:951692598182027314>',use=None,description="Augmente vos dégâts critiques au dépriment de vos dégâts non critiques")
revelEff = copy.deepcopy(defenseUp)
revelEff.power, revelEff.stat, revelEff.turnInit = divination.effect[0].power, INTELLIGENCE, 3
revelation = skill("Révélation","srw",TYPE_BOOST,divination.price,effect=revelEff,cooldown=divination.cooldown,emoji=divination.emoji,range=AREA_MONO,area=AREA_CIRCLE_2)
elemEff = effect("Energie multiélémentaire","elemEff",None,turnInit=3,stackable=True,description="Cet effet devient un effet élémentaire correspondant à votre élément, augmentant de **{0}%** la puissance de vos compétences exclusives à votre élément (Non cumulable)\nCertaines compétences peuvent consommer les effets élémentaires pour obtenir des propriétés supplémentaires",power=5,emoji=elemEmojis[ELEMENT_UNIVERSALIS_PREMO])
elemEffName = ["Neutralité","Flamme intérieur","Courrant interne","Tempête intérieur","Minéralisation","Lueur interne","Ombre interne","Poussière cosmique","Seconde temporelle","Illuminae"]
mEP = 35
matriseElemEff = effect("Maîtrise élémentaire","maitriseElemPas",None,turnInit=-1,unclearable=True,description="Vous octroit **{0}%** de chance d'obtenir l'effet {1} __{2}__ lorsque vous utilisez une compétence élémentaire".format(mEP,elemEff.emoji[0][0],elemEff.name),emoji=elemEmojis[ELEMENT_UNIVERSALIS_PREMO],callOnTrigger=elemEff)
maitriseElementaire = skill("Maîtrise élémentaire","srv",TYPE_PASSIVE,effectOnSelf=matriseElemEff,emoji=elemEmojis[ELEMENT_UNIVERSALIS_PREMO],price=500)
magicEffGiver = skill("Concentration élémentaire","sru",TYPE_DAMAGE,500,75,effectOnSelf=elemEff,emoji='<:elemStrike:953217204629950484>',description="Inflige des dégâts à l'ennemi ciblé et vous octroit l'effet élémentaire correspondant à votre élément",cooldown=5,use=MAGIE)
physEffGiver = skill("Convertion élémentaire","srt",TYPE_DAMAGE,500,75,effectOnSelf=elemEff,emoji='<:elemSpell:953217184795078697>',description="Inflige des dégâts à l'ennemi ciblé et vous octroit l'effet élémentaire correspondant à votre élément",cooldown=5)
finalFasEff = effect("Final Fascinatoire","finalFas",critical=10,critDmgUp=10,emoji="<:finalFas:951824644523040788>",description="Augmente le taux de coup critique et de dégâts critiques de **10%**")
danseFasReady = effect("Danse de la Lame Fascinatoire préparée","danseFasReady",turnInit=5,description="Vous permet d'utiliser la compétence {0} __Danse de la Lame Fascinatoire__".format(swordDance.emoji),emoji=swordDance.emoji)
finalFas = skill("Final Fascinatoire","srs",TYPE_BOOST,effect=finalFasEff,area=AREA_DONUT_2,range=AREA_MONO,emoji="<:finalFas:951824644523040788>",cooldown=7,description="Augmente le taux de critique et les dégâts critiques des alliés proches de **10%**",rejectEffect=[danseFasReady])
danceFas = skill("Danse de la Lame Fascinatoire","srs",TYPE_DAMAGE,power=125,area=AREA_CIRCLE_1,use=CHARISMA,cooldown=5,emoji=swordDance.emoji,needEffect=danseFasReady)
eventFas = effect("Eventail Fascinatoire","evFac",turnInit=-1,unclearable=True,emoji='<:evFas:951824800488230932>',description="Effet passif donné par Fascination. Voir la description de la compétence",callOnTrigger=danseFasReady)
fascination = skill("Fascination","srs",TYPE_PASSIVE,price=750,emoji='<:evFas:951824800488230932>',effectOnSelf=eventFas,become=[finalFas,danceFas],description="Posséder cette compétence vous octrois l'effet {0} __{1}__.\nPour chaque coup critique effectué par un alliés, la valeur de l'éventail augmente de **10**. Une fois **100 points** atteints, vous obtenez l'effet {2} __{3}__ et le temps de rechargement de cette compétence ainsi que la valeur de l'éventail sont réduit à 0".format(eventFas.emoji[0][0], eventFas.name, danseFasReady.emoji[0][0], danseFasReady.name),use=CHARISMA)
corGraEff = effect("Chorégraphie Grâcieuse","chorGra",CHARISMA,charisma=7,intelligence=7,endurance=7,emoji=sameSpeciesEmoji('<:graceB:956700633531043933>','<:graceR:956700653785346149>'),description="Augmente les statistiques de support du porteur")
corGraFinal = skill("Chorégraphie Grâcieuse","corGraceFinal",TYPE_BOOST,500,range=AREA_MONO,area=aliceDance.area,effect=corGraEff,cooldown=aliceDance.cooldown,emoji='<:corGra:956700501095899217>',description="Augmente les statistiques de support de vos alliés proches durant 3 tours")
corGraGuideEff = effect(corGraFinal.name,"corGraGuideEff",turnInit=2,silent=True,emoji=corGraFinal.emoji,replique=corGraFinal)
corGraGuide = copy.deepcopy(corGraFinal)
corGraGuide.effectOnSelf, corGraGuide.id = corGraGuideEff, "srq"
corGraGuideEff2 = copy.deepcopy(corGraGuideEff)
corGraGuideEff2.replica = corGraGuide
corGraCast = copy.deepcopy(corGraGuide)
corGraCast.effectOnSelf = corGraGuideEff2

rosePink = effect("Rose rose","finFloRose",turnInit=-1,emoji='<:roseRose:956716583915491378>',stackable=True)
roseBlue = effect("Rose azurée","finFloBlu",turnInit=-1,emoji='<:roseBlue:956716604333367326>',stackable=True)
roseGreen = effect("Rose verte","finFloGre",turnInit=-1,emoji='<:roseGreen:956716536742150254>',stackable=True)
roseRed = effect("Rose rouge","finFloRed",turnInit=-1,emoji='<:roseRed:956716516232032257>',stackable=True)
roseYellow = effect("Rose jaune","finFloYel",turnInit=-1,emoji='<:roseYellow:956716561136242748>',stackable=True)
roseDarkBlu = effect("Rose bleue","finFloDBlue",turnInit=-1,emoji='<:roseDBlue:956725613585133598>',stackable=True)

tablRosesEff,tablRosesSkillsId,tablRosesId = [roseRed,roseDarkBlu,rosePink,roseYellow,roseBlue,roseGreen], [aliceDanceFinal.id,corGraFinal.id,onstage.id,crimsomLotus.id,finalTech.id,valse.id],[roseRed.id,roseDarkBlu.id,rosePink.id,roseYellow.id,roseBlue.id,roseGreen.id]

finFloLaunchBase = skill("Final Floral","finFlo",TYPE_BOOST,use=CHARISMA,emoji='<:finFlor:956715059772538981>',range=AREA_MONO,area=AREA_CIRCLE_4)
finFloCast = effect("Cast - Final Floral","castFinFlo",turnInit=2,emoji=finFloLaunchBase.emoji,replique=finFloLaunchBase)
finFloEff = effect("Final Floral","finFloEffPas",turnInit=-1,unclearable=True,emoji=sameSpeciesEmoji('<:finalFloralB:956715210549362748>','<:finalFloralR:956715234842791937>'),description="Vous avez la compétence <:finFlor:956715059772538981> __Final Floral__ d'équipé")
finalFloral = skill("Final Floral","srr",TYPE_PASSIVE,750,effectOnSelf=finFloEff,emoji='<:finFlor:956715059772538981>',description="En utilisant certaines compétences, vous obtiendrez une *Rose* :\n{0} __{1}__ : {2} {3}\n{4} __{5}__ : {6} {7}\n{8} __{9}__ : {10} {11}\n{12} __{13}__ : {14} {15}\n\nVous pouvez aussi orbtenir une rose quand vos alliés utilisent certaines compétences :\n{16} __{17}__ : {18} {19}\n{20} __{21}__ : {22} {23}\n\nLorsque vous possédez trois effets *Rose*, vous vous mettrez à charger la compétence {24} __{25}__, dont l'effet dépend des *Roses* possédées :\n{2} __{3}__ : Augmente les dégâts infligés des alliés de **7%** (Charisme)\n{6} __{7}__ : Réduit les dégâts reçus des alliés de **5%** (Charisme)\n{10} __{11}__ : Augmente la durée des effets déclanchés par les autres *Roses* de **1 tour**\n{14} __{15}__ : Augmente la puissance des effets déclanchés par les autres *Roses* de **30%**\n{18} __{19}__ : Augmente le taux de coup critique des alliés de **7%** (Charisme)\n{22} __{23}__ : Vous procure une aura qui soigne les alliés autour de vous en fin de tour pendant **3 tours** (Charisme)\n\nVous ne pouvez cummuler que **3** *Roses* à la fois, et avoir une *Rose* en doublon n'augmente pas les effets associés".format(
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
    finFloLaunchBase.emoji, finFloLaunchBase.name
))

finFloEffList = [copy.deepcopy(dmgUp),copy.deepcopy(defenseUp),effect("Critique Floral",'finFloCrit',CHARISMA,critical=7,emoji=finFloEff.emoji),effect("Aura Florale","finFloHeal",CHARISMA,power=20,turnInit=3,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji=finFloEff.emoji,area=AREA_CIRCLE_2)]
finFloEffList[0].power, finFloEffList[1].power, finFloEffList[0].stat, finFloEffList[1].stat = 7, 7, CHARISMA, CHARISMA

divineSave = skill("Salut Divin","srp",TYPE_RESURECTION,500,300,group=SKILL_GROUP_HOLY,maxHpCost=35,cooldown=5,shareCooldown=True,use=CHARISMA, emoji='<:hollyRaise:958065170645655642>')
redemption = skill("Rédemption","sro",TYPE_DAMAGE,500,150,area=AREA_CIRCLE_1,maxHpCost=15,group=SKILL_GROUP_HOLY,ultimate=True,cooldown=5,use=MAGIE,emoji='<:rdemption:958065152098455673>')

tablElemEff = []
for cmpt in range(len(elemNames)):
    temp = copy.deepcopy(elemEff)
    temp.emoji, temp.name, temp.description, temp.id = uniqueEmoji(elemEmojis[cmpt]), elemEffName[cmpt], "Augmente de **{0}%** la puissance de vos compétences exclusives à l'élément **{1}** (Non cumulable)\n\nCertaines compétences peuvent consommer cet effet pour obtenir des propriétés supplémentaires".format(temp.power,elemNames[cmpt]), temp.id + str(cmpt)
    tablElemEff.append(temp)

for cmpt in range(len(transTabl)):
    transTabl[cmpt].name, transTabl[cmpt].description = lbNames[cmpt], lbDesc[cmpt]

    if cmpt < len(limitBeakGif):
        transTabl[cmpt].url = limitBeakGif[cmpt]

fireElemUse = skill("Brasier Infernal","srn",TYPE_DAMAGE,500,65,setAoEDamge=True,range=AREA_MONO,area=AREA_DIST_5,ultimate=True,cooldown=7,use=MAGIE,emoji='<:catFire:956599672737243166>',description="Consomme vos effets {0} __{1}__\nInflige des dégâts aux ennemis éloignés de vous\nSi au moins un {0} __{1}__ a été consommé, donne également un effet de dégâts indirects aux ennemis infligeants **33%** de dégâts supplémentaires à la fin de leur tour dont la durée dépend du nombre d'effets consommés".format(tablElemEff[1].emoji[0][0],tablElemEff[1].name),conditionType=["exclusive","element",ELEMENT_FIRE])
waterElemUse = skill("Pluie Glacée","srm",TYPE_DAMAGE,500,120,ultimate=True,cooldown=7,use=MAGIE,emoji='<:catWater:956599696594444418>',description="Consomme vos effets {0} __{1}__\nInflige des dégâts à l'ennemi ciblé.\nPour chaque effet {0} __{1}__ consommé, réalise une nouvelle attaque infligeant **15%** de dégâts supplémentaires".format(tablElemEff[2].emoji[0][0],tablElemEff[2].name),conditionType=["exclusive","element",ELEMENT_WATER])
airElemUse = skill("Tempête Jupiterrienne","srl",TYPE_DAMAGE,500,70,setAoEDamge=True,range=AREA_MONO,area=AREA_CIRCLE_2,ultimate=True,cooldown=7,use=MAGIE,emoji='<:catAir:956599718522265610>',description="Consomme vos effets {0} __{1}__\nInflige des dégâts aux ennemis autour de vous\nSi au moins un effet {0} __{1}__ a été consommé, vous octrois un effet infligeant des dégâts indirects aux ennemis autour de vous à la fin de votre tour dont la durée dépend du nombre d'effets consommés".format(tablElemEff[3].emoji[0][0],tablElemEff[3].name),conditionType=["exclusive","element",ELEMENT_AIR])
earthElemUse = skill("Déchirure Tectonique","srk",TYPE_DAMAGE,500,120,ultimate=True,cooldown=7,use=MAGIE,emoji='<:catEarth:956599751002963998>',description="Consomme vos effets {0} __{1}__\nInflige des dégâts à l'ennemi ciblé.\nSi au moins un effet {0} __{1}__ a été consommé, réalise une nouvelle attaque infligeant **20%** de dégâts supplémentaires sur les ennemis autour de vous. La puissance de l'attaque est multipliée par le nombre d'effets consommés".format(tablElemEff[4].emoji[0][0],tablElemEff[4].name),conditionType=["exclusive","element",ELEMENT_EARTH])
lightElemUseEff = effect("Armure de lumière","lightArmorElemUse",INTELLIGENCE,overhealth=65,turnInit=3,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR)
lightElemUse = skill("Lumière Protectrice","srj",TYPE_ARMOR,500,range=AREA_MONO,area=AREA_CIRCLE_3,effect=lightElemUseEff,cooldown=7,ultimate=True,emoji='<:catLight:956599774461722655>',description="Consomme vos effets {0} __{1}__\nDonne une armure à vous et vos alliés alentours.\nSi au moins un effet {0} __{1}__ a été consommé, octroie un effet de soins sur la durée avec une puissance de **30%** de celle de l'armure. La durée de l'effet dépend du nombre d'effets consommés".format(tablElemEff[5].emoji[0][0],tablElemEff[5].name),conditionType=["exclusive","element",ELEMENT_LIGHT],use=INTELLIGENCE)
darkElemUse = skill("Brasier des Ténèbres","sri",TYPE_DAMAGE,500,75,setAoEDamge=True,area=AREA_CIRCLE_2,ultimate=True,cooldown=7,use=MAGIE,emoji='<:catDark:950942244523872256>',description="Consomme vos effets {0} __{1}__\nInflige des dégâts aux ennemis dans la zone d'effet\nSi au moins un {0} __{1}__ a été consommé, donne également un effet de dégâts indirects à l'ennemi ciblé infligeant **50%** de dégâts supplémentaires à la fin de son tour à lui et ses alliés proches dont la durée dépend du nombre d'effets consommés".format(tablElemEff[6].emoji[0][0],tablElemEff[6].name),conditionType=["exclusive","element",ELEMENT_DARKNESS])
spaceElemUse = skill("Déluge Céleste","srh",TYPE_DAMAGE,500,100,setAoEDamge=True,area=AREA_CIRCLE_2,ultimate=True,cooldown=7,use=MAGIE,emoji='<:catSpace:956599795110277150>',description="Consomme vos effets {0} __{1}__\nInflige des dégâts aux ennemis dans la zone d'effet\nPour chaque effet {0} __{1}__ consommé, inflige des dégâts supplémentaires équivalents à **33%** des dégâts de base à un ennemi aléatoire dans la zone d'effet et ses alliés aux corps à corps".format(tablElemEff[7].emoji[0][0],tablElemEff[7].name),conditionType=["exclusive","element",ELEMENT_SPACE])
timeElemUse = skill("Déphasage Temporel","srg",TYPE_HEAL,500,100,area=AREA_CIRCLE_2,ultimate=True,cooldown=7,use=CHARISMA,emoji='<:catTime:956599814898999328>',description="Consomme vos effets {0} __{1}__\nSoigne les alliés dans la zone d'effet.\nSi au moins un effet {0} __{1}__ a été consommé, octroi également une armure aux alliés dans la zone d'effet dont la puissance équivant à **20%** de celle des soins. La puissance est multipliée par le nombre d'effets consommés".format(tablElemEff[8].emoji[0][0],tablElemEff[8].name),conditionType=["exclusive","element",ELEMENT_TIME])
bleedingConvert = skill("Taillade des veines","srf",TYPE_DAMAGE,500,75,range=AREA_CIRCLE_3,cooldown=7,lifeSteal=50,emoji="<:shiLifeSteal:960007047984857148>",percing=50,description="Inflige des dégâts à la cible et vole une partie des dégâts infligés tout en ignorant une partie de la résistance de la cible\nConsomme tous les effets <:ble:887743186095730708> __Hémorragie__ présents sur la cible pour augmenter la puissance de cette compétence")

elemShieldEff = effect("Armure élémentaire","elemShield",INTELLIGENCE,overhealth=40,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,callOnTrigger=elemEff,area=AREA_DONUT_2,description="Une armure qui protège de quelques dégâts directs\nLorsqu'elle est brisée, donne l'effet {0} __{1}__ aux alliés autour du porteur".format(elemEff.emoji[0][0],elemEff.name),emoji=sameSpeciesEmoji('<:elemShield:960061614739050537>','<:elemShield:960061540164313088>'))
elemShield = skill("Armure élémentaire","srd",TYPE_ARMOR,500,effect=elemShieldEff,cooldown=7,emoji='<:elemShield:960061614739050537>',description="Octroi une armure à l'allié ciblé. Quand celle-ci est détruite, donne un effet élémentaire aux alliés aux alentours")
shieldAuraShield = effect("Armure","armorAuraArmor",INTELLIGENCE,overhealth=20,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,description="Protège de quelques dégâts directs")
shieldAuraEff = effect("Aura armurière","shieldAuraEff",INTELLIGENCE,callOnTrigger=shieldAuraShield,emoji=sameSpeciesEmoji('<:armorAura:960060538119929927>','<:armorAura:960060634517602344>'),lvl=3,area=AREA_CIRCLE_2,trigger=TRIGGER_END_OF_TURN,turnInit=3,description="À la fin du tour du porteur, ocrtoi une armure à celui-ci et ses alliés aux alentours")
shieldAura = skill("Aura Armurière","src",TYPE_ARMOR,500,cooldown=7,effect=shieldAuraEff,emoji='<:armorAura:960060538119929927>',description="Pose une aura sur l'allié ciblé, qui octroira de l'armure autour de lui quand il terminera son tour pendant 3 tours")
horoscope = skill("Horoscope","srb",TYPE_BOOST,emoji='<:horoscope:960312586371477524>',description="Consomme tous vos signes astrologiques pour augmenter les statistiques de vos alliés durant 3 tours\nLes statistiques augmentées dépendent des signes astrologiques conssommés\nVous obtenez un signe astrologique aléatoire en fin de tour",cooldown=4,initCooldown=5,conditionType=["exclusive","element",ELEMENT_SPACE],use=INTELLIGENCE,range=AREA_MONO, area=AREA_CIRCLE_5)
ShiHemophilie = effect("Anti-Coagulant","increaseBlooding",description="Augmente de **{0}%** les dégâts subis par l'effet <:ble:887743186095730708> __Hémorragie__",power=35,emoji='<:hemophillie:960721463772610613>')
ShiUltimateLauch = skill("Percée ensanglantée","sra",TYPE_DAMAGE,750,150,AREA_CIRCLE_2,effect=["mx",ShiHemophilie],emoji='<:shiUlt:960760921666510908>',description="Après 1 tour de chargement, inflige de lourd dégâts à l'ennemi ciblé, lui applique <:ble:887743186095730708> __Hémorragie__ et augmente les dégâts de <:ble:887743186095730708> __Hémorragie__ durant 1 tour",ultimate=True,cooldown=7)
ShiUltimateCast = effect("Cast - {0}".format(ShiUltimateLauch.name),"shiUltCast",turnInit=2,silent=True,replique=ShiUltimateLauch,emoji='<a:shiUltCast:960764930217377802>')
ShiUltimate = copy.deepcopy(ShiUltimateLauch)
ShiUltimate.effect, ShiUltimate.power, ShiUltimate.effectOnSelf = [None], 0, ShiUltimateCast

intaveneuse = skill("Intraveineuse",'sqz',TYPE_INDIRECT_DAMAGE,500,effect="me",effPowerPurcent=135,cooldown=5,emoji='<:intraveineuse:963390544770367488>',use=MAGIE)
decolation = skill("Colation","sqy",TYPE_DAMAGE,effect=ShiUltimateLauch.effect,effPowerPurcent=60,cooldown=5,power=40,lifeSteal=100,emoji='<:collation:963390564655579156>',price=500)
dephaIncantEff = effect("Déphasage Incantatoire","dephaIncant",MAGIE,power=80,area=AREA_CIRCLE_1,trigger=TRIGGER_ON_REMOVE,type=TYPE_INDIRECT_DAMAGE,description="Inflige des dégâts lors du début du prochain tour de l'entité à l'origine de l'effet")
dephaIncant = skill("Déphasage incantatoire","sqx",TYPE_INDIRECT_DAMAGE,500,effect=dephaIncantEff,cooldown=5,description="Place l'effet {effIcon} __{effName}__ sur la cible. Au début de votre prochain tour, l'effet explosera en blessant le porteur et ses alliés proches")

coroWind = effect("Mordax Ventus","coroWind",MAGIE,power=35,turnInit=3,stackable=True,lvl=3,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji='<:corWind:968321700922028062>',description="Un vent empoisonné qui fait des dégâts à la fin du tour du porteur.\nPossède une légère odeur de sang")

cwFocus = skill("Incarnatus Puff","sqw",TYPE_INDIRECT_DAMAGE,500,cooldown=focal.cooldown,effect=coroWind,effPowerPurcent=300,effectOnSelf=coroWind,description="Donne un effet {effIcon} __{effName}__ trois fois plus puissant à l'ennemi ciblé, mais en subissez un également",emoji='<:IncPuf:968327189508542484>')
propaUltLaunch = skill("Provecta Propagation","sqv",TYPE_INDIRECT_DAMAGE,750,range=AREA_MONO,area=AREA_ALL_ENEMIES,ultimate=True,cooldown=7,effect="me",effPowerPurcent=35,description="Après un tour de chargement, inflige <:est:884223390804766740> __Poison d'Estialba__ à tous les ennemis avec **35%** de sa puissance")
propaUltCastEff = effect("Cast - {replicaName}","propaUltCastEff",turnInit=2,silent=True,replique=propaUltLaunch)
propaUlt = copy.deepcopy(propaUltLaunch)
propaUlt.effect, propaUlt.effectOnSelf, propaUlt.description = [None], propaUltCastEff, None
cwUlt = skill("Ultima Exitium","squ",TYPE_INDIRECT_DAMAGE,750,ultimate=True,cooldown=7,effect=coroWind,power=25,description="Inflige l'effet {effIcon} __{effName}__ à la cible, puis inflige immédiatement des dégâts indirects en fonction du nombre d'effets de Dégâts Indirects ainsi que leur durée restante présents sur la cible\nLes effets autres que {effIcon} __{effName}__ augmentent un peu plus la puissance de l'attaque mais sont consommés par cette dernière")
sanguisGladio = skill("Sanguis Gladio","sqt",TYPE_DAMAGE,500,80,cooldown=5,effect=coroWind,effPowerPurcent=80,use=MAGIE,emoji='<:sgladio:968478994724950056>')
sanguisGladio2 = skill("Provecta Sanguis Gladio","sqs",TYPE_DAMAGE,750,100,cooldown=7,area=AREA_LINE_2,effect=coroWind,effPowerPurcent=65,use=MAGIE,emoji='<:sgladio2:968479144293855252>')
cardiChoc = skill("Choc Cardinal","sqr",TYPE_DAMAGE,500,100,range=AREA_MONO,area=AREA_INLINE_3,sussess=120,cooldown=5,description="Inflige des dégâts aux ennemis prochent allignés avec vous avec une précision importante")
equatorial = skill("Equatorial","sqq",TYPE_DAMAGE,500,50,range=AREA_MONO,area=AREA_LINE_6,sussess=120,cooldown=7,setAoEDamge=True,description="Inflige des dégâts aux ennemis allignés avec vous avec une précision importante")
kralamSkillEff2 = effect("This is, my No No Square","nono",INTELLIGENCE,resistance=10,overhealth=55,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,turnInit=3)
kralamSkillEff1 = effect("No no, don't touch me there","squaez",trigger=TRIGGER_DAMAGE,callOnTrigger=kralamSkillEff2,lvl=1,emoji=uniqueEmoji('<a:FranziskaNo:800833215106383883>'),type=TYPE_BOOST,resistance=5)
kralamSkill = skill("Prévention","vn",TYPE_BOOST,0,0,AREA_DONUT_6,cooldown=5,effect=kralamSkillEff1,emoji='<:egide:887743268337619005>')
krystalisationEff = effect("Cristalisé","krysArmor",ENDURANCE,overhealth=65,inkResistance=12.5,turnInit=3,emoji='<:liuArmor:922292960886915103>',type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
krystalisation = skill("Cristallisation","sqp",TYPE_ARMOR,500,range=AREA_MONO,effect=krystalisationEff,cooldown=7,description="Vous octrois une armure qui réduit également les dégâts indirects subis",conditionType=["exclusive","element",ELEMENT_EARTH])
regenVigilEff = effect("Régénération vigilante","vigilRegen",CHARISMA,power=35,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_END_OF_TURN)
regenVigil = skill("Régénération Vigilante","sqo",TYPE_HEAL,750,35,AREA_DONUT_4,["exclusive","aspiration",VIGILANT],cooldown=7,effect=regenVigilEff,effectOnSelf=regenVigilEff,description="Soigne l'allié ciblé et procure à ce dernier et vous même un effet de soin sur la durée")
fragmentation = skill("Fragmentation","sqn",TYPE_DAMAGE,500,50,AREA_CIRCLE_4,cooldown=5,damageOnArmor=3,erosion=65,conditionType=["exclusive","aspiration",TETE_BRULE],description="Inflige des dégâts à l'ennemi ciblé avec un grand pourcentage de réduction des PvMax adverses ainsi qu'un multiplicateur de dégâts sur l'armure conséquant")
morsTempette = effect("Morsure de la Tempette","morsTempette",STRENGTH,power=30,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,stackable=True,turnInit=5,lvl=5,emoji='<:morsTemp:971788828278943776>')
morsCaudique = effect("Morsure Caudique","morsCaudique",INTELLIGENCE,power=30,trigger=TRIGGER_END_OF_TURN,stackable=True,type=TYPE_INDIRECT_DAMAGE,turnInit=5,lvl=5,emoji='<:morsCaudique:971788772289163274>')
machDeFer = skill("Mâchoire de Fer","sqm",TYPE_INDIRECT_DAMAGE,500,conditionType=["exclusive","aspiration",ATTENTIF],effect=[morsTempette,morsCaudique],cooldown=7,emoji='<:machFer:971787963795124235>')
lanceToxEff = effect("Toxine","toxi",STRENGTH,power=25,emoji='<:lanceTox:971789592145580103>',stackable=True,turnInit=5,lvl=5,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE)
lanceTox = skill("Lance-Toxine","sql",TYPE_INDIRECT_DAMAGE,500,area=AREA_CONE_3,effect=lanceToxEff,emoji='<:lanceTox:971789592145580103>',cooldown=5,conditionType=["exclusive",'aspiration',ATTENTIF])
gigaFoudreEff = effect("Giga Foudre","gigaFoudre",MAGIE,power=20,emoji='<:gigaFoudre:971789611087036487>',stackable=True,turnInit=5,lvl=5,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN)
gigaFoudre = skill("Giga Foudre","sqk",TYPE_INDIRECT_DAMAGE,500,area=AREA_CIRCLE_1,effect=gigaFoudreEff,emoji='<:gigaFoudre:971789611087036487>',cooldown=5,conditionType=["exclusive",'aspiration',SORCELER])
trickAttackEff = copy.deepcopy(vulne)
trickAttackEff.power = 10
trickAttack = skill("Attaque Sournoise","sqj",TYPE_DAMAGE,500,50,effect=trickAttackEff,cooldown=5,emoji='<:trickAttack:971788242284343336>',description="Inflige des dégâts à l'adversaire sublié puis augmente les dégâts qu'il reçoit de **10%** jusqu'à votre prochain tour")
aurore2Eff = effect("Aurore II","aur2Eff",type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,power=20,stat=CHARISMA,turnInit=3,emoji='<:aurore:971787846639841310>')
aurore2 = skill("Aurore II","sqh",TYPE_INDIRECT_HEAL,500,effect=aurore2Eff,cooldown=5,emoji='<:aurore:971787846639841310>',conditionType=["exclusive","aspiration",VIGILANT])
holyShieltronEff1 = effect("Shieltron Sacré","holyShieltron1",block=100,emoji='<:shieltron:971787905758560267>')
holyShieltronEff2 = effect("Shieltron Sacré (régen)","holyShieltron2",CHARISMA,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,power=15,turnInit=3,emoji='<:shieltron:971787905758560267>')
holyShieltron = skill("Shieltron Sacré","sqg",TYPE_BOOST,500,range=AREA_MONO,effect=[holyShieltronEff2,holyShieltronEff1],emoji=holyShieltronEff1.emoji[0][0],conditionType=["exclusive","aspiration",VIGILANT],group=SKILL_GROUP_HOLY,maxHpCost=5,cooldown=5,description="Vous octroi 100% de blocage ainsi qu'une petite régénération sur la durée")
KeracholeRegen = effect("Kerachole","keracholeRegen",INTELLIGENCE,power=15,turnInit=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji='<:kerachole:971787391058722847>')
KeracholeReduc = copy.deepcopy(defenseUp)
KeracholeReduc.power, KeracholeReduc.stat, KeracholeReduc.turnInit = 3.5, INTELLIGENCE, 3
kerachole = skill("Kerachole","sqf",TYPE_BOOST,500,effect=[KeracholeReduc,KeracholeRegen],emoji='<:kerachole:971787391058722847>',cooldown=7,range=AREA_MONO,area=AREA_CIRCLE_2,description="Réduit les dégâts subis par vous et vos allié proches tout en vous octroyanr un effet de régénération sur la durée")
morsTempSkill = skill("Morsure de la Tempette","sqe",TYPE_INDIRECT_DAMAGE,350,effect=morsTempette,cooldown=5,conditionType=["exclusive","aspiration",ATTENTIF],emoji=morsTempette.emoji[0][0])
morsCaudiqueSkill = skill("Morsure Caudique","sqd",TYPE_INDIRECT_DAMAGE,350,effect=morsCaudique,cooldown=5,conditionType=["exclusive","aspiration",ATTENTIF],emoji=morsCaudique.emoji[0][0])
combEff = effect("Combustion","combustion",MAGIE,power=15,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_1,turnInit=-1,lvl=99)
combustion = skill("Combustion","sqc",TYPE_PASSIVE,500,effectOnSelf=combEff,conditionType=["exclusive","secElem",ELEMENT_FIRE],description="À chaque de tour, inflige des dégâts aux ennemis à votre corps à corps")

# Skill
skills = [krystalisation,regenVigil,fragmentation,machDeFer,lanceTox,trickAttack,aurore2,holyShieltron,kerachole,gigaFoudre,morsTempSkill,combustion,morsCaudiqueSkill,
    dephaIncant,cwFocus,propaUlt,cwUlt,sanguisGladio,sanguisGladio2,cardiChoc,equatorial,
    elemShield,shieldAura,horoscope,ShiUltimate,intaveneuse,decolation,
    corGraCast,finalFloral,divineSave,redemption,fireElemUse,waterElemUse,airElemUse,earthElemUse,lightElemUse,darkElemUse,spaceElemUse,timeElemUse,bleedingConvert,
    revelation,maitriseElementaire,magicEffGiver,physEffGiver,fascination,
    selenomancie,holiomancie,partner,exhibitionnisme,invocTitania,dmonBlood,hollyGround,hollyGround2,burningGround,blueShell,preciChi,ironHealth,windBal,brasier2,earthUlt2,geyser,rouletteSkill,constance,constance2,
    undead,ironStormBundle,bolide,invincible,holmgang,comboVerBrasier,galvanisation,contreDeSixte,
    lifeWind,ice2,renf2,entraide,perfectShot,lastRessource,strengthOfDesepearance,nova,deathShadow,comboVerMiracle,comboFaucheCroix,theEndCast,cure2Bundle,assises,debouses,impact,heartStone,erodStrike,genesis,invertion,
    pneuma,absorbingStrike,absorbingArrow,absorbingStrike2,absorbingArrow2,magiaHeal,aff2,bloodPact,expediant,divination,macroCosmos,tintabule,toMelee,toDistance,autoBombRush,killerWailUltimate,invocSeaker,darkBoomCast,mageSkill,doubleShot,harmShot,benitWater,shareSkill,extraMedica,foullee,lifePulseCast,crimsomLotusCast,abnegation,
    foyer,sweetHeat,darkSweetHeat,shell,nacreHit,holyShot,demonStrike,purify,benediction,transfert,blackDarkMagic,fisure,seisme,abime,extermination,darkHeal,calestJump,lohicaUltCast,fairyFligth,aliceDance,aurore,crep,
    quickCast,pepsis,darkShield,rencCel,valse,finalTech,dissi,intelRaise,ultRedirect,clemency,liuSkillSus,liaSkillSus,lioSkillSus,lizSKillSus,neutralMono1,neutralZone1,neutralMono2,neutralZone2,neutralMono3,neutralZone3,reconst,medicamentum,ultMonoArmor,inkRes,inkRes2,booyahBombCast,propag,invocCarbSaphir,invocCarbObsi,supprZone,cosmicPower,requiem,magicRuneStrike,infinitDark,preciseShot,troublon,haimaSkill,physicRune,magicRune,lightBigHealArea,focus,poisonusPuit,bleedingPuit,idoOS,proOS,preOS,geoConCast,kikuRes,memClemCastSkill,roses,krysUlt,chaosArmor,firelame,airlame,waterlame,mudlame,shadowLame,timeLame,lightLame,astralLame,idoOH,proOH,altOH,lightAura2,tripleMissiles,lightHeal2,extraEtingSkill,strengthOfWillCast,sixtineUlt,hinaUlt,julieUlt,invocSeraf,mageUlt,soulagement,bloodyStrike,infraMedica,magAchSkill,flambeSkill,fireCircle,waterCircle,airCircle,earthCircle,fireShot,waterShot,airStrike,earthStrike,space1,space2,space3,spaceSp,time1,time2,time3,timeSp,renisurection,demolish,contrainte,trouble,epidemic,croissance,destruction2,infectFiole,bigLaser2,bigMonoLaser2,invocBat2,invocCarbunR,concen,memAlice2,blackHole,blackHole2,renforce,steroide,focal,suppr,revitalisation,onde,eting,stingray,dark1,dark2,dark3,light1,light2,light3,derobade,ferocite,ironWillSkill,royaleGardeSkill,defi,dissimulation,bleedingTrap,convert,vampirisme,heriteEstialba,heriteLesath,flameche,flame,pyro,ecume,courant,torant,brise,storm2,tornado,stone,rock,mont,bleedingArrow,bleedingDague,swordDance,shot,percingArrow,percingLance,highkick,multishot,rocklance,infinitFire,storm,innerdarkness,divineLight,icelance,onstage,kiss,secondSun,oneforall,uppercut,stalactic,linx,bombRobot,isolement,secondWind,blindage,adrenaline,lapSkill,burst,trans,descart,thinkSkill,invocFee,invocCarbT,invocCarbE,splashdown,multiMissiles,monoMissiles,invocBat,poisonus,protect,explosionCast,splatbomb,lightAura,cure,firstheal,balayette,contrecoup,boom,chaos,unHolly,soupledown,inkarmor,coffeeSkill,theSkill,gpotion,bpotion,zelian,courage,nostalgia,draw25,siropMenthe
]

importantSkills = [deathShadow.id]
useElemEffId = [fireElemUse.id,waterElemUse.id,airElemUse.id,earthElemUse.id,lightElemUse.id,darkElemUse.id,spaceElemUse.id,timeElemUse.id]

horoscopeEff = [
    [effect("Bélier","horBélier",turnInit=-1,emoji='<:belier:960319494167867473>'),[[STRENGTH,1],[ENDURANCE,2]]],
    [effect("Taureau","horTaureau",turnInit=-1,emoji='<:taureau:960319518004092939>'),[[STRENGTH,2],[ENDURANCE,1]]],
    [effect("Gémeaux","horGémeaux",turnInit=-1,emoji='<:gemeaux:960319543228649523>'),[[CHARISMA,1],[INTELLIGENCE,1],[MAGIE,1]]],
    [effect("Cancer","horCancer",turnInit=-1,emoji='<:cancer:960319573003997215>'),[[AGILITY,1],[STRENGTH,1],[MAGIE,1]]],
    [effect("Lion","horLio",turnInit=-1,emoji='<:lion:960319606050914336>'),[[STRENGTH,3]]],
    [effect("Vierge","horVierge",turnInit=-1,emoji='<:vierge:960319632982540329>'),[[CHARISMA,3]]],
    [effect("Balance","horBalance",turnInit=-1,emoji='<:balance:960319658823667762>'),[[INTELLIGENCE,1],[MAGIE,2]]],
    [effect("Scorpion","horScorpion",turnInit=-1,emoji='<:scorpion:960319682861232211>'),[[STRENGTH,2],[MAGIE,1]]],
    [effect("Sagittaire","horSagittaire",turnInit=-1,emoji='<:sagittaire:960319710380036146>'),[[MAGIE,3]]],
    [effect("Capricorne","horCapricorne",turnInit=-1,emoji='<:capricorne:960319731343175781>'),[[MAGIE,2],[ENDURANCE,1]]],
    [effect("Verseau","horVerseau",turnInit=-1,emoji='<:verseau:960319751136108546>'),[[INTELLIGENCE,2,PRECISION,1]]],
    [effect("Poisson","horPoisson",turnInit=-1,emoji='<:poisson:960319770337628191>'),[[AGILITY,2],[PRECISION,1]]]
]

# FindSkill
def findSkill(skillId) -> skill:
    """Renvoie une compétence Skill, si trouvé"""
    typi = type(skillId)
    if typi == skill:
        return skillId

    elif type(skillId) != str or skillId == "0":
        return None
    else:
        if skillId.startswith("\n"):
            skillId = id.replace("\n","")
        for a in skills:
            if a.id == skillId or a.name.lower() == skillId.lower():
                return a

        #print("ID non trouvée : ",skillId)
        return None
