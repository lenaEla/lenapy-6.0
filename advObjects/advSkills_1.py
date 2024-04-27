from copy import deepcopy
from classes import *
from constantes import *
from advObjects.advDepl import *

estial = effect("Poison d'Estialba","me",emoji=uniqueEmoji('<:est:884223390804766740>'),turnInit=3,stat=MAGIE,description="Un virulant poison, faisant la sinistre renommée des fées de cette île",trigger=TRIGGER_START_OF_TURN,stackable=True,power=25,type=TYPE_INDIRECT_DAMAGE,lvl=3)
estal2 = effect("Poison d'Estialba II","nq", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=int(estial.power/3),turnInit=3,emoji='<:estialba2:900329155974008863>',stackable=True,lvl=3)
bleeding = effect("Hémorragie","mx", stat=STRENGTH,power=30,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,turnInit=3,stackable=True,lvl=3,emoji="<:bleeding:1133258052225745048>")

soupledown = skill("Choc Ténébreux","zz",TYPE_DAMAGE,500,150,range = AREA_INLINE_3,condition=[EXCLUSIVE,ASPIRATION,POIDS_PLUME],area = AREA_CIRCLE_2,accuracy=150,tpCac=True,ultimate=True,cooldown=7,emoji='<:darkdown:1138876529753993297>',use=STRENGTH)
armor = effect("Armure d'Encre","la", stat=INTELLIGENCE,overhealth=60,emoji=sameSpeciesEmoji('<:armor1:866828463751036929>','<:armor2:866828487038205962>'),description="Une armure qui protège le porteur des dégâts directs",trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,turnInit=2)
inkArmor2 = effect("Armure d'Encre en formation","loadupArmor",trigger=TRIGGER_ON_REMOVE,callOnTrigger=armor)
inkarmor = skill("Armure d'Encre","zy",TYPE_ARMOR,250,ultimate=True,effects=inkArmor2,emoji='<:inkArmor:866829950463246346>',area=AREA_ALL_ALLIES,cooldown=5,range=AREA_MONO,description="Octroi un effet à tous les alliés. Lors de votre prochain tour, cet effet leur octroi une armure")
coffee = effect("Caféiné","lb", stat=CHARISMA,strength=10,endurance=10,description="Boost la force et l'endurance de tous les alliés",emoji=uniqueEmoji("<:coffee:867538582846963753>"))
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
exploMarkEff = effect("Disizosad","alexaPlayDespasito", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_DEATH,power=80,area=AREA_DONUT_2,turnInit=5,emoji='<:disizosadEff:1177590836238753852>',lvl=1)
exploMarkEff1 = effect("Disizosad","alexaPlayDespasito1", stat=MAGIE,callOnTrigger=exploMarkEff,emoji=exploMarkEff.emoji,area=AREA_LINE_3,trigger=TRIGGER_INSTANT,block=-20)
exploMark = skill("Marque Disizosad","zl",TYPE_DAMAGE,500,effects=exploMarkEff1,cooldown=5,emoji='<:disizisad:1177590810338930708>',use=MAGIE,area=exploMarkEff1.area,power=80,description="Inflige des dégâts aux ennemis ciblés. Si ceux-ci sont vaincu dans un laps de temps, provoque une autre explosion indirecte",effBeforePow=True,quickDesc="Une marque de zone qui peut provoquer de belles réactions en chaîne",useActionStats=ACT_INDIRECT)
balayette = skill("Baleyette","zk",TYPE_DAMAGE,100,100,range=AREA_MONO,area=AREA_CIRCLE_1,emoji='<:baleyette:977166497422139392>',cooldown=5,setAoEDamage=True)
cure = skill("Guérison","zi",TYPE_HEAL,250,80,cooldown=5,emoji='<:cure:925190515845132341>')
lightAura = skill("Aura de Lumière","zh",TYPE_PASSIVE,250,effectOnSelf="ly",emoji="<:lightAura:1133263881955967127>",quickDesc="Soigne les alliés autour de vous en fin de tour",condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
splatbomb = skill("Bombe splash","zg",TYPE_DAMAGE,100,cooldown=5,area=AREA_CIRCLE_1,power=90,emoji='<:splatbomb:873527088286687272>',message="{0} lance une {1} sur {2} :")
explosionSilentEff = copy.deepcopy(silenceEff)
explosionSilentEff.turnInit = 2
explosion = skill("Explosion","KBOOM",TYPE_DAMAGE,1000,power=250,percing=0,ultimate=True,cooldown=12,area=AREA_CIRCLE_2,shareCooldown=True,effectOnSelf=explosionSilentEff,use=MAGIE,emoji='<a:explosion:882627170944573471>',damageOnArmor=0.8,url='https://media.discordapp.net/attachments/933783831272628356/934066959040016404/20220121_134758.gif',description="Inflige des dégâts colosaux dans une grande zone")
castExplo = effect("Cast - Explosion","na",turnInit=2,silent=True,emoji=sameSpeciesEmoji('<a:boomCastB:916382499704275005>','<a:boomCastR:916382515135144008>'),replique=explosion)
explosionCast = skill("Explosion","zf",TYPE_DAMAGE,1000,ultimate=True,cooldown=7,area=AREA_CIRCLE_2,accuracy=0,shareCooldown=True,effectOnSelf=castExplo,use=MAGIE,emoji='<a:explosion:882627170944573471>',message="{0} rassemble son mana...")
protect = skill("Orbe défensif","ze",TYPE_ARMOR,200,emoji='<:orbeDef:873725544427053076>',effects="md",cooldown=3)
poisonus = skill("Vent empoisonné","zd",TYPE_INDIRECT_DAMAGE,500,emoji='<:estabistia:883123793730609172>',effects=estial,cooldown=5,area=AREA_CIRCLE_1,use=MAGIE,effPowerPurcent=30/estial.power*100)
invocBat = skill("Invocation - Chauve-souris","zc",TYPE_SUMMON,500,invocation="Chauve-Souris",emoji="<:cutybat:884899538685530163>",shareCooldown=True,use=HARMONIE,nbSummon=3,cooldown=5)
missiles = effect("Ciblé","mf",emoji=uniqueEmoji('<:tentamissile:884757344397951026>'),stat=STRENGTH,trigger=TRIGGER_START_OF_TURN,power=50,type=TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_1,stackable=True)
multiMissiles = skill("Multi-Missiles","zb",TYPE_INDIRECT_DAMAGE,750,range=AREA_MONO,ultimate=True,emoji='<:tentamissile:884757344397951026>',effects=missiles,cooldown=5,area=AREA_RANDOMENNEMI_5,url='https://cdn.discordapp.com/attachments/935769576808013837/935781565663948850/20220126_071157.gif',description="Inflige des dégâts indirects de zone autour de 5 ennemis aléatoires au début de leur tour")
monoMissiles = skill("Mono-Missiles","za",TYPE_INDIRECT_DAMAGE,250,range=AREA_CIRCLE_7,emoji='<:monomissile:884757360193708052>',effects=missiles,cooldown=3,effPowerPurcent=125,description="Inflige des dégâts indirects de zone autour de l'ennemi ciblé lorsqu'il commence son tour")
classicSplashdown = skill("Choc Chromatique Classique","yz",TYPE_DAMAGE,500,power=150,range=AREA_MONO,ultimate=True,emoji='<:splashdown:884803808402735164>',cooldown=5,area=AREA_CIRCLE_2,damageOnArmor=3,url="https://cdn.discordapp.com/attachments/935769576808013837/935781564661526578/20220126_071756.gif")
invocCarbE = skill("Invocation - Carbuncle Emeraude","yy",TYPE_SUMMON,500,invocation="Carbuncle Emeraude",emoji="<:invoncEm:919857931158171659>",cooldown=3,range=AREA_CIRCLE_3,shareCooldown=True,use=MAGIE)
invocCarbT = skill("Invocation - Carbuncle Topaze","yx",TYPE_SUMMON,500,invocation="Carbuncle Topaze",emoji="<:invocTopaz:919859538943946793>",cooldown=3,range=AREA_CIRCLE_3,shareCooldown=True,use=ENDURANCE)
invocFee = skill("Invocation - Fée Soignante","yw",TYPE_SUMMON,500,range=AREA_CIRCLE_3,cooldown=5,invocation="Fée Soignante",emoji="<:selene:885077160862318602>",shareCooldown=True,use=CHARISMA)
thinkSkill = skill("Réfléchis !","yv",TYPE_BOOST, replay=True, price=250,emoji="<:think:885240853696765963>",effects="mh",use=CHARISMA,cooldown = 3)
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
transObs.effectOnSelf = effect("Transcender ses limites","transObsEff", stat=HARMONIE,precision=25,strength=25,turnInit=3,emoji=sameSpeciesEmoji('<:lbBB:930780339947855882>','<:lbBR:930780304405327893>'),description="Augmente les statistiques de l'Observateur pendant 3 tours")
transAttentif.effects= [effect("Poison transcendique","transTetEff", stat=HARMONIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,lvl=3,power=45,turnInit=3,emoji=sameSpeciesEmoji('<:lbDB:930780352480436244>','<:lbDR:930780318699511850>'),description="Inflige des dégâts pendant 3 tours")]
transMage = copy.deepcopy(trans)
transMage.type,transMage.power,transMage.area,transMage.name, transMage.cooldown = TYPE_DAMAGE,400,AREA_CIRCLE_2, transMage.name + " - Explosion transcendique", transMage.cooldown+1
transEnch = copy.deepcopy(transMage)
transSorceler = copy.deepcopy(transMage)
transMage.power, transSorceler.effects= int(transMage.power * 1.2), [effect("Hypernova","transSorcEff", stat=HARMONIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,area=AREA_CIRCLE_2,power=35,turnInit=3,lvl=3,emoji=sameSpeciesEmoji('<:lbDB:930780352480436244>','<:lbDR:930780318699511850>'),description="Inflige des dégâts indirects supplémentaire autour de la cible initiale au début de son tour")]
transEnch.effectOnSelf = effect("Bouclier Transcendique","transEchShield", stat=MAGIE,emoji=sameSpeciesEmoji("<a:transArmorB:900037831257358378>","<a:transArmorR:900037817449717800>"),type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,overhealth=100,description="Accorde une armure à l'Enchanteur")
transAlt = copy.deepcopy(trans)
transAlt.type,transAlt.power,transAlt.area,transAlt.range, transAlt.name, transAlt.cooldown, transAlt.effectAroundCaster = TYPE_HEAL,250,AREA_ALL_ALLIES,AREA_MONO, transAlt.name + " - Soins transcendiques",7, [TYPE_RESURECTION,AREA_CIRCLE_6,350]
transIdo = copy.deepcopy(trans)
transAlt.effects= [effect("Soins transcendique","transAltEff", stat=CHARISMA,power=25,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji=sameSpeciesEmoji('<:lbHealB:933084435706953768>','<:lbHealR:933084448327606304>'),description="Soigne légèrement les alliés affectés au début de leur tour")]
transIdo.effects, transIdo.type, transIdo.effectAroundCaster, transIdo.range, transIdo.area, transIdo.name = [effect("Transcender ses limites","transIdoEff", stat=HARMONIE,strength=30,magie=30,charisma=25,intelligence=25,percing=10,critical=5,turnInit=3,emoji=sameSpeciesEmoji('<:lbBB:930780339947855882>','<:lbBR:930780304405327893>'),description="Augmente les statistiques des alliés affectés pendant 3 tours")], TYPE_BOOST, [TYPE_RESURECTION,AREA_CIRCLE_6,150], AREA_MONO, AREA_CIRCLE_6, "Apothéose"
transInoEff = copy.deepcopy(defenseUp)
transInoEff.turnInit, transInoEff.power = 3, 20
transIno = copy.deepcopy(transIdo)
transIno.effects, transIno.effectAroundCaster, transIno.name = transIno.effects + [transInoEff], None, "Ultima Serum"
transPre = copy.deepcopy(trans)
transPro = copy.deepcopy(trans)
transAttEffOnSelf = copy.deepcopy(defenseUp)
transAttEffOnSelf.turnInit, transAttEffOnSelf.power = 3, 15
effTransPre = effect("Armure Transcendique","transArm", stat=HARMONIE,strength=5,magie=5,inkResistance=15,overhealth=250,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji("<a:transArmorB:900037831257358378>","<a:transArmorR:900037817449717800>"),description="Donne une grosse armure et augmente les statistiques des alliés tant que celle-ci est active")
effTransPro = effect("Armure Transcendique","transArm", stat=HARMONIE,resistance=5,overhealth=250,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji("<a:transArmorB:900037831257358378>","<a:transArmorR:900037817449717800>"),description="Donne une grosse armure et augmente la résistance des alliés tant que celle-ci est active")
transPre.type,transPre.area,transPre.range,transPre.effects,transPre.name, transPre.cooldown = TYPE_ARMOR,AREA_ALL_ALLIES,AREA_MONO,[effTransPre],transPre.name + " - Armure Transcendique",7
transPro.type,transPro.area,transPro.range,transPro.effects,transPro.name, transPro.cooldown,transPro.effectOnSelf = TYPE_ARMOR,AREA_ALL_ALLIES,AREA_MONO,[effTransPro],transPro.name + " - Armure Transcendique",7, transAttEffOnSelf
transAtt = copy.deepcopy(transAlt)
transAtt.effectAroundCaster, transAtt.effects, transAtt.name, transAtt.effectOnSelf = [TYPE_RESURECTION,AREA_ALL_ALLIES,int(transAtt.effectAroundCaster[2]*1.5)], [None], "Eclat de vie", transAttEffOnSelf
transMascEff = copy.deepcopy(vulne)
transMascEff.power = 30
transMasc = copy.deepcopy(transIdo)
transMasc.effectAroundCaster = [TYPE_MALUS,transMasc.area,transMascEff]

burst = skill("Bombe ballon","ys",TYPE_DAMAGE,0,80,area=AREA_CIRCLE_1,emoji='<:burstBomb:887328853683474444>',use=HARMONIE,cooldown=3,setAoEDamage=True)
lapSkill = skill("Invocation - Lapino","yr",TYPE_SUMMON,0,invocation="Lapino",cooldown=5,shareCooldown=True,emoji='<:lapino:885899196836757527>',use=CHARISMA)
adrenaline = skill("Adrénaline","yq",TYPE_HEAL,250,cure.power,cooldown=5,emoji='<:adrenaline:887403480933863475>',use=INTELLIGENCE)
blindOnSelf = effect("Blindé","blindOnSelf",resistance=20,block=20,description="Réduit les degâts subis jusqu'à votre prochain tour")
blindage = skill("Blindage","yp",TYPE_BOOST,350,AREA_MONO,area=AREA_DONUT_2,effects="mj",cooldown=3,use=None,emoji="<:blindage:897635682367971338>",effectOnSelf=blindOnSelf)
secondWind = skill("Second Souffle","yo",TYPE_HEAL,500,power=300,range=AREA_MONO,emoji='<:secondWind:897634132639756310>',cooldown=7,use=ENDURANCE)
isolemenntEff = effect("Isolation","isolation", stat=INTELLIGENCE,inkResistance=8,turnInit=3)
isoled = effect("Isolé","ml",emoji=uniqueEmoji('<:selfProtect:887743151027126302>'),description="S'isoler mentalement pôur ne pas faire attention au dégâts",overhealth=35,stat=PURCENTAGE,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR)
isolement = skill("Isolement","yn",TYPE_ARMOR,500,AREA_MONO,use=INTELLIGENCE,emoji='<:selfProtect:887743151027126302>',cooldown=7,effects=[isolemenntEff,isoled],description="Réduit les dégâts indirects reçus et vous octroie une armure en fonction de vos PV maximums")
bombRobot = skill("Invocation - Bombe Robot","ym",TYPE_SUMMON,500,AREA_CIRCLE_3,invocation="Bombe Robot",cooldown=2,shareCooldown=True,emoji='<:autobomb:887747538994745394>',use=STRENGTH)
linx = skill("Œuil de Linx","yl",TYPE_BOOST,500,range=AREA_MONO,area=AREA_CIRCLE_2,emoji='<:noeuil:887743235131322398>',effects="mm",cooldown=5)
stalactic = skill("Stalactite","yk",TYPE_DAMAGE,300,100,emoji='<:stalactit:889089667088142346>',cooldown=3,accuracy=200,range=AREA_DIST_5)
uppercutEff = effect("Faiblesse","Uppercut",resistance=-45,stat=PURCENTAGE,type=TYPE_MALUS)
uppercut = skill("Uppercut","yj",TYPE_DAMAGE,500,range=AREA_CIRCLE_1,emoji='<:uppercut:889091033718194196>',cooldown=5,effects=uppercutEff,damageOnArmor=1.2,garCrit=True,description="Inflige une attaque critique à l'ennemi ciblé et réduit sa résistance")
oneforall = skill("Un pour tous","yi",TYPE_BOOST,500,range=AREA_MONO,area=AREA_DONUT_2,cooldown=5,use=CHARISMA,effects="mo",effectOnSelf="mp",description="Une compétence qui permet d'augmenter les résistances de ses alliés au détriment des siennes",condition=[EXCLUSIVE,ASPIRATION,ALTRUISTE],emoji='<:oneforall:893295824761663488>')
secondSun = skill("Le second Soleil","yh",TYPE_MALUS,350,AREA_MONO,area=AREA_ALL_ENEMIES,cooldown=5,effects="mq",emoji='<:iwanttosleeppls:893241882484817920>',use=CHARISMA,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
kiss = skill("Doux baiser","yg",TYPE_HEAL,69,75,AREA_DONUT_2,emoji='<:welp:893251469439008809>',message="{0} fait un gros bisou à {2} :",tpCac=True,cooldown=3)
onstageeff = effect("Euphorie","mr", stat=CHARISMA,strength=15,intelligence=15,charisma=15,magie=15,resistance=5,emoji=uniqueEmoji('<:alice:893463608716062760>'))
onstage = skill("En scène ","yf",TYPE_BOOST,750,AREA_MONO,condition=[EXCLUSIVE,ASPIRATION,IDOLE],ultimate=True,effects=onstageeff,emoji='<:alice:893463608716062760>',area=AREA_CIRCLE_3,use=CHARISMA,cooldown=7)
icelance = skill("Lame glacée","ye",TYPE_DAMAGE,500,180,AREA_DIST_6,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],ultimate=True,emoji='<:emoji_47:893471252537298954>',cooldown=7,use=MAGIE)
rocklance = skill("Lame rocheuse","yd",TYPE_DAMAGE,500,180,AREA_CIRCLE_3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],ultimate=True,emoji='<:emoji_46:893471231641276496>',cooldown=7,use=MAGIE)
infinitFire = skill("Brasier","yc",TYPE_DAMAGE,500,165,AREA_DIST_5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],ultimate=True,emoji='<:emoji_44:893471208065101924>',cooldown=7,area=AREA_LINE_3,use=MAGIE)
storm = skill("Ouragan","yb",TYPE_DAMAGE,500,165,AREA_CIRCLE_2,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],ultimate=True,emoji='<:emoji_44:893471179023732809>',cooldown=7,area=AREA_CIRCLE_2,use=MAGIE)
innerdarknessEff = effect("Ténèbres intérieurs","ms", stat=MAGIE,power=70,stackable=True,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:innerdarkness:902008902776938628>'),turnInit=3,area=AREA_CIRCLE_1,description="Au début de tour, les Ténèbres de l'âme du porteur provoquent une explosion en croix, le blessant lui et ses alliés proches")
innerdarkness = skill("Ténèbres intérieurs","ya",TYPE_INDIRECT_DAMAGE,500,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS],ultimate=True,emoji='<:emoji_48:893471268957990982>',cooldown=7,effects=innerdarknessEff,use=MAGIE,group=SKILL_GROUP_DEMON,hpCost=15)
lighteff = effect("Illuminé","mu", stat=INTELLIGENCE,overhealth=75,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji('<:illumi1:902008944887746611>'))
lightHealeff = effect("Illuminé","mv", stat=CHARISMA,power=50,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:illumi2:902008962134712380>'),turnInit=2)
divineLight = skill("Lumière divine",'xz',TYPE_INDIRECT_HEAL,500,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],ultimate=True,emoji='<:emoji_49:893471282815963156>',cooldown=7,effects=[lightHealeff,lighteff],use=CHARISMA,area=AREA_CIRCLE_1,group=SKILL_GROUP_HOLY,maxHpCost=15)
swordDance = skill("Danse Tranchante","xy",TYPE_DAMAGE,500,power=120,use=STRENGTH,emoji='<:sworddance:894544710952173609>',cooldown=5,area=AREA_CIRCLE_2,range=AREA_MONO)
shot = skill("Tir net","xx",TYPE_DAMAGE,350,115,AREA_CIRCLE_6,emoji='<:shot:894544804321558608>',cooldown=7,use=STRENGTH,damageOnArmor=2)
percingLance = skill("Lance Perçante","xw",TYPE_DAMAGE,350,power=80,emoji='<:percing:894544752668708884>',cooldown=3,area=AREA_LINE_2,range=AREA_CIRCLE_2)
percingArrow = skill("Flèche Perçante","wv",TYPE_DAMAGE,350,power=70,emoji='<:percingarrow:887745340915191829>',cooldown=3,area=AREA_LINE_2,range=AREA_DIST_5)
highkick = skill("HighKick","wu",TYPE_DAMAGE,500,power=100,range=AREA_CIRCLE_1,emoji='<:highKick:1122785057531236463>',cooldown=7,damageOnArmor=1.35,garCrit=True)
multishot = skill("Tir Multiple","wt",TYPE_DAMAGE,500,power=80,range=AREA_DIST_4,emoji='<:name:894544834780622868>',cooldown=5,area=AREA_CONE_2)
bleedingArrow = skill("Flèche Hémorragique","ws",TYPE_DAMAGE,350,70,AREA_DIST_5,effects=bleeding,emoji='<:bleedingarrow:894544820071178292>',cooldown=3)
bleedingDague = skill("Dague Hémorragique","wr",TYPE_DAMAGE,350,80,AREA_CIRCLE_2,effects=bleeding,emoji='<:bleedingdague:894552391444234242>',cooldown=3)
affaiblissement = skill("Affaiblissement","wq",TYPE_MALUS,350,effects="my",cooldown=3,use=INTELLIGENCE,emoji='<:affaib:963394012771942440>',area=AREA_CIRCLE_1)
provo = skill("Provocation","wp",TYPE_MALUS,350,emoji='<:supportnt:894544669793476688>',effects='mz',cooldown=3,use=INTELLIGENCE)

dictElemSkills = {
    ELEMENT_FIRE:{"emojis":['<:flame1:897811975675969556>','<:flame2:897812264185376798>','<:flame3:897812061139140651>'],"area":AREA_CONE_2,"id":"wm","names":["Flammèche","Flamme","Pyrotechnie"]},
    ELEMENT_WATER:{"emojis":["<:splash1:897844189184811078>","<:splash2:897844205198659594>","<:splash3:897844380491202581>"],"area":AREA_MONO,"id":"wd","names":["Écume","Courant","Torrant"]},
    ELEMENT_AIR:{"emojis":["<:wind1:897845097775915038>","<:wind2:897845144299110441>","<:wind3:897845187940868156>"],"area":AREA_CIRCLE_1,"id":"wh","names":["Brise","Tempête","Tornade"]},
    ELEMENT_EARTH:{"emojis":["<:rock1:897846015552532531>","<:rock2:897846028512944138>","<:rock3:897846042576420874>"],"area":AREA_MONO,"id":"we","names":["Caillou","Rocher","Montagne"]},
    ELEMENT_DARKNESS:{"emojis":["<:dark1:899599162566410280>","<:dark2:899599147399807006>","<:dark3:899598969930399765>"],"area":AREA_MONO,"id":"vz","names":["Cécité","Obscurité","Pénombre"]},
    ELEMENT_LIGHT:{"emojis":["<:light1:899598879576690689>","<:light2:899598896613969970>","<:light3:899599232628043787>"],"area":AREA_MONO,"id":"vw","names":["Lueur","Éclat","Éblouissement"]},
    ELEMENT_SPACE:{"emojis":["<:ast1:907470821679824896>","<:ast2:907470855402033153>","<:ast3:907470880676917309>"],"area":AREA_MONO,"id":"ty","names":["Naine Blanche","Constellation","Nébuluse"]},
    ELEMENT_TIME:{"emojis":["<:time1:907474383034023977>","<:time2:907474439854235668>","<:time3:907474471240216658>"],"area":AREA_MONO,"id":"tv","names":["Seconde","Minute","Heure"]},
}

def createElemComboSkill(element:int):
    tmpDict = dictElemSkills[element]
    neededEffect1, neededEffect2 = effect(tmpDict["names"][1]+" préparé",tmpDict["names"][1]+"ready",turnInit=3,silent=True,emoji=tmpDict["emojis"][1]), effect(tmpDict["names"][2]+" préparé",tmpDict["names"][2]+"ready",turnInit=3,silent=True,emoji=tmpDict["emojis"][2])

    skill0 = skill(tmpDict["names"][0],tmpDict["id"],TYPE_DAMAGE,use=MAGIE,power=[65,80][tmpDict["area"]==AREA_MONO],emoji=tmpDict["emojis"][0],condition=[EXCLUSIVE,ELEMENT,element],rejectEffect=[neededEffect1,neededEffect2],effectOnSelf=neededEffect1)
    skill1 = skill(tmpDict["names"][1],tmpDict["id"],TYPE_DAMAGE,use=MAGIE,power=skill0.power+20,emoji=tmpDict["emojis"][1],condition=[EXCLUSIVE,ELEMENT,element],needEffect=neededEffect1,effectOnSelf=neededEffect2)
    skill2 = skill(tmpDict["names"][2],tmpDict["id"],TYPE_DAMAGE,use=MAGIE,power=skill1.power+20,emoji=tmpDict["emojis"][2],condition=[EXCLUSIVE,ELEMENT,element],needEffect=neededEffect2,cooldown=5)

    return skill("Combo Élem{0}'".format(["","en"][elemNames[element][0] in ["A","E","I","O","U","Y"]])+elemNames[element],skill1.id,TYPE_DAMAGE,price=500,become=[skill0, skill1, skill2],emoji=skill2.emoji,description="Vous permet d'utiliser le combo {0}, {1} et {2}".format(skill0, skill1, skill2))

fireMagicCombo = createElemComboSkill(ELEMENT_FIRE)
waterMagicCombo = createElemComboSkill(ELEMENT_WATER)
airMagicCombo = createElemComboSkill(ELEMENT_AIR)
earthMagicCombo = createElemComboSkill(ELEMENT_EARTH)
darknessMagicCombo = createElemComboSkill(ELEMENT_DARKNESS)
lightMagicCombo = createElemComboSkill(ELEMENT_LIGHT)
spaceMagicCombo = createElemComboSkill(ELEMENT_SPACE)
timeMagicCombo = createElemComboSkill(ELEMENT_TIME)

stingray2 = skill("Pigmalance","wd",TYPE_DAMAGE,500,150,AREA_CIRCLE_7,ultimate=True,emoji='<:stingray:899243721378390036>',cooldown=5,area=AREA_LINE_6,accuracy=120,description="Inflige des dégâts pendant deux tours.\nPuissance au premier tour : 100",damageOnArmor=0.7,url="https://cdn.discordapp.com/attachments/935769576808013837/935781565936590898/20220126_070809.gif")
pigmaCast = effect("Guide - Pigmalance","nb",turnInit=2,silent=True,emoji=uniqueEmoji('<:castStingray:899243733835456553>'),replique=stingray2)
stingray = skill("Pigmalance","wc",TYPE_DAMAGE,500,150,AREA_CIRCLE_7,ultimate=True,emoji='<:stingray:899243721378390036>',cooldown=5,area=AREA_LINE_6,accuracy=100,effectOnSelf=pigmaCast,damageOnArmor=0.7,url="https://cdn.discordapp.com/attachments/935769576808013837/935781565072547850/20220126_071411.gif")

derobade = skill("Dérobade","vv",TYPE_BOOST,350,AREA_DONUT_3,cooldown=3,effectOnSelf="nd",effects="nc",emoji='<:derobade:899788297868558337>',use=INTELLIGENCE)
ferocite = skill("Férocité","vu",TYPE_PASSIVE,200,emoji='<:ferocite:899790356315512852>',effectOnSelf="ne",quickDesc="Accroi votre Magie et la probabilité d'être pris pour cible",use=ENDURANCE)
ironWillSkill = skill("Volontée de Fer","vt",TYPE_PASSIVE,200,emoji='<:ironwill:899793931762565251>',effectOnSelf="nh",quickDesc="Accroi votre Charisme et la probabilité d'être pris pour cible",use=ENDURANCE)
royaleGardeSkill = skill("Garde Royale","vs",TYPE_PASSIVE,200,emoji='<:gardeRoyale:899793954315321405>',effectOnSelf="ng",quickDesc="Accroi votre Intelligence et la probabilité d'être pris pour cible",use=ENDURANCE)
defi = skill("Défi","vr",TYPE_PASSIVE,200,emoji='<:defi:899793973873360977>',effectOnSelf="nf",quickDesc="Accroi votre Force et la probabilité d'être pris pour cible",use=ENDURANCE)
ombralStrikeEff = effect("Frappe Ombrale","vqE1",STRENGTH,type=TYPE_DAMAGE,trigger=TRIGGER_END_OF_TURN,emoji="<:chiphidenBlade:1223632204421140610>",power=75)
ombralStrike = skill(ombralStrikeEff.name,'vq',TYPE_DAMAGE,0,power=ombralStrikeEff.power,cooldown=7,effects=ombralStrikeEff,accuracy=150,range=AREA_CIRCLE_1,emoji=ombralStrikeEff.emoji[0][0],description="Inflige des dégâts à l'ennemi ciblé. À la fin de son tour, la compétence est répliquée")
laceration = skill("Lacération","vp",TYPE_INDIRECT_DAMAGE,500,effects=bleeding,cooldown=5,area=AREA_CIRCLE_1,use=STRENGTH,emoji='<:lacerTrap:900076484230774807>',effPowerPurcent=int(35/bleeding.power*100))
# vn already taken (Prévention)
convertEff = effect("Convertion","nk",power=15,type=TYPE_BOOST,stat=INTELLIGENCE,description="Lorsque le porteur de l'effet inflige des dégâts directs, une partie de ces dégâts lui sont rendue en Armure\nL'Intelligence du lanceur de la compétence influ sur le pourcentage de convertion",emoji=uniqueEmoji('<:convertion:900311843938115614>'))
aoeConvertEff = effect("Convertion étendue","aoeConvert",power=5,type=TYPE_BOOST,stat=INTELLIGENCE,description="Lorsque le porteur de l'effet inflige des dégâts directs, une partie de ces dégâts sont converties en armure pour ses alliés proches\nL'Intelligence du lanceur de la compétence influ sur le pourcentage de convertion",emoji='<:aoeConvert:1100770918340497519>')
convert = skill("Convertion","vm",TYPE_ARMOR,350,range=AREA_DONUT_5,effects=[convertEff,aoeConvertEff],cooldown=5,emoji='<:convertion:900311843938115614>',description="Lors que l'allié ciblé inflige des dégâts directs, il vole une partie des dégâts infligés en armure pour lui et vos alliés proches de lui")
vampirismeEff = effect("Vampirisme","no",power=15,type=TYPE_INDIRECT_HEAL,stat=CHARISMA,stackable=True,description="Accorde au porteur **{0}%** de vol de vie",emoji=sameSpeciesEmoji('<:vampireB:900313575913062442>','<:vampireR:900313598130282496>'))
aoeVampirismeEff = effect("Vampirisme étendu","aoeVamp",power=5,type=TYPE_INDIRECT_HEAL,stat=CHARISMA,stackable=True,description="Lorsque le porteur inflige des dégâts, une partie est volé et octroyé aux alliés proches",emoji='<:aoeLifeSteal:1100770895846457376>')
vampirisme = skill("Vampirisme","vl",TYPE_INDIRECT_HEAL,350,range=AREA_DONUT_5,effects=[vampirismeEff,aoeVampirismeEff],cooldown=5,emoji='<:vampire:900312789686571018>')
vampirisme2 = skill("Vampirisme étendu","spw",TYPE_INDIRECT_HEAL,500,effects=vampirismeEff,cooldown=7,emoji='<:vampire:900312789686571018>',group=SKILL_GROUP_DEMON,hpCost=15,effPowerPurcent=80,area=AREA_CIRCLE_2,range=AREA_MONO)

heriteEstialbaEff = effect("Héritage - Estialba","np",turnInit=-1,unclearable=True,callOnTrigger=estal2,emoji="<:estialLegacy:1191001141304119376>")
heriteEstialba = skill("Héritage - Estialba","vk",TYPE_PASSIVE,0,effects=heriteEstialbaEff,emoji=heriteEstialbaEff.emoji[0][0],use=MAGIE,quickDesc="Grâce aux enseignements de Lohica, vous êtes de plus en plus rodé en terme de poison",description="Lorsque vous infligez l'effet {0} à un ennemi, lui inflige également l'effet {1}".format(estial,estal2))

bleeding2 = effect("Hémoragie II","nr", stat=STRENGTH,power=int(bleeding.power/3),type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,turnInit=3,stackable=True,emoji=uniqueEmoji('<:bleeding2:1133258082470871061>'),lvl=3)
heriteLesathEff = effect("Héritage - Lesath","ns",turnInit=-1,unclearable=True,callOnTrigger=bleeding2,emoji="<:lesathLegacy:1191001162300801095>")
heriteLesath = skill("Héritage - Lesath","vj",TYPE_PASSIVE,0,effects=heriteLesathEff,emoji=heriteLesathEff.emoji[0][0],quickDesc="Grâce aux enseignements de Shehisa, vous en connaissez un peu plus sur les points faibles de vos adversaires",description="Lorsque vous infligez l'effet {0} à un ennemi, lui inflige également l'effet {1}".format(bleeding,bleeding2))

focal = skill("Focalisation","vi",TYPE_INDIRECT_DAMAGE,750,range=AREA_CIRCLE_4,cooldown=7,effects=estial,effPowerPurcent=int(50/estial.power*100),area=AREA_CIRCLE_1,effectOnSelf=estial,emoji='<:focal:925204877683085332>',shareCooldown=True,use=MAGIE,description="Octrois un puissant effet __Poison d'Estialba__ aux ennemis dans la zone ciblé, avec un contre-coup",selfEffPurcent=int(20/estial.power*100))
suppr = skill("Suppression","vh",TYPE_DAMAGE,650,105,emoji='<a:sup:925199175681970216>',cooldown=5,use=MAGIE,damageOnArmor=3,accuracy=120)
revitalisation = skill("Mot revitalisant","vg",TYPE_HEAL,300,55,area=AREA_CIRCLE_1,emoji="<:revita:902525429183811655>",cooldown=3)
onde = skill("Onde","vf",TYPE_ARMOR,500,effects="nv",cooldown=3,area=AREA_CIRCLE_1,emoji='<:onde:902526595842072616>')
etingEff = effect("Marque Eting","nw", stat=CHARISMA,power=50,turnInit=3,lvl=1,stackable=True,trigger=TRIGGER_HP_UNDER_50,emoji=uniqueEmoji('<:eting:902525771074109462>'),type=TYPE_INDIRECT_HEAL)
eting = skill("Marque Eting","ve",TYPE_HEAL,500,power=35,effects=etingEff,emoji='<:eting:902525771074109462>',cooldown=5,description="Soigne l'allié ciblé. Si ses PVs tombent en dessous de 50% ou après trois tours, la cible reçoit des soins supplémentaires")
renforce = skill("Renforcement","vd",TYPE_BOOST,500,range=AREA_DONUT_5,effects="nx",cooldown=5,description="Une compétence qui augmente la résistance d'un allié. L'effet diminue avec les tours qui passent",use=INTELLIGENCE,emoji='<:renfor:921760752065454142>')
steroide = skill("Stéroïdes","vc",TYPE_BOOST,500,range=AREA_DONUT_5,effects="oa",cooldown=3,area=AREA_CIRCLE_1,use=INTELLIGENCE,emoji='<:steroide:963548366053179392>')
renisurection = skill("Résurrection","vb",TYPE_RESURECTION,500,150,emoji='<:respls:906314646007468062>',cooldown=3,description="Permet de ressuciter un allié",use=CHARISMA)
demolishEff = effect("Fracture","demolishEff", stat=PURCENTAGE,resistance=-45,type=TYPE_MALUS)
demolish = skill("Démolition","va",TYPE_DAMAGE,750,165,AREA_CIRCLE_2,ultimate=True,cooldown=7,effects=demolishEff,damageOnArmor=1.5,emoji='<:destruc:905051623108280330>',description="Réduit la résistance de l'ennemi ciblé et lui inflige une puissante attaque",effBeforePow=True)
contrainteEff2 = copy.deepcopy(armorGetMalus)
contrainteEff2.power = 30
contrainte = skill("Contrainte","uz",TYPE_MALUS,500,range=AREA_CIRCLE_6,effects=[incur[3],contrainteEff2,"oc"],cooldown=3,use=INTELLIGENCE,emoji='<:contrainte:963393945704992829>')
trouble = skill("Trouble","uy",TYPE_MALUS,500,range=AREA_CIRCLE_6,effects=[incur[3],contrainteEff2,"od"],use=CHARISMA,emoji='<:trouble:963394783596933182>',cooldown=3)
infirm = skill("Infirmitée","ux",TYPE_MALUS,500,area=AREA_CIRCLE_5,effects=incur[2],cooldown=3,use=None,emoji='<:infirm:904164428545683457>')
croissance = skill("Croissance","uw",TYPE_BOOST,500,effects="oe",cooldown=5,description="Une compétence dont les bonus se renforce avec les tours qui passent",use=CHARISMA,range=AREA_DONUT_5,emoji='<:crois:921760610985865246>')
destruction = skill("Météore","uu",TYPE_DAMAGE,1000,power=350,ultimate=True,percing=0,cooldown=7,shareCooldown=True,effectOnSelf=explosionSilentEff,use=MAGIE,emoji='<:meteor:904164411990749194>',damageOnArmor=explosion.onArmor,url='https://cdn.discordapp.com/attachments/933783831272628356/934069125628690482/20220121_135643.gif')
castDest = effect("Cast - Météore","nnnn",turnInit=2,silent=True,emoji=uniqueEmoji('<a:castMeteor:932827784655536139>'),replique=destruction)
destruction2 = skill("Météore","uv",TYPE_DAMAGE,1000,power=0,ultimate=True,cooldown=7,effectOnSelf=castDest,use=MAGIE,shareCooldown=True,emoji=destruction.emoji,message="Une ombre plane au dessus de {2}...")
infectRej = effect("Guérison récente (Infection)","oi",silent=True,turnInit=3,description="Une guérison récente empêche une nouvelle infection",emoji='<:unepidemic:1016788322246471801>')
infection = effect("Infection","oh", stat=INTELLIGENCE,power=30,trigger=TRIGGER_START_OF_TURN,lifeSteal=20,type=TYPE_INDIRECT_DAMAGE,lvl=3,reject=[infectRej],description="Un effet infligeant des dégâts indirects\n\nL'infection se propage sur les ennemis autour du porteur lorsque l'effet se déclanche avec une puissance réduite de **15%**",emoji=uniqueEmoji("<:infect:904164445268369428>"),turnInit=3,replace=True)
infectFiole = skill("Fiole d'infection","ut",TYPE_INDIRECT_DAMAGE,350,effects=infection,cooldown=5,use=INTELLIGENCE,message="{0} lance une {1} sur {2}",emoji='<:fioleInfect:904164736407597087>')
bigLaser = skill("Lasers chromanergiques - Configuration Ligne","us",TYPE_DAMAGE,0,200,emoji='<:uLaserLine:906027231128715344>',area=AREA_LINE_6,accuracy=95,damageOnArmor=1.33,ultimate=True,cooldown=7,description="Après un tour de chargement, déployez des drones énergétiques qui tirent un puissant rayon coloré en ligne droite")
bigLaserRep = effect("Cast - Las. Chrom. - Conf. Ligne","bigLaserEff",turnInit=2,silent=True,emoji=dangerEm,replique=bigLaser)
bigLaser2 = skill(bigLaser.name,"ur",bigLaser.type,750,area=bigLaser.area,emoji=bigLaser.emoji,effectOnSelf=bigLaserRep,ultimate=bigLaser.ultimate,cooldown=bigLaser.cooldown,message="{0} charge ses drones")
bigMonoLaser = skill("Lasers chromanergiques - Configuration Mono","uq",TYPE_DAMAGE,0,250,emoji='<:uLaserMono:906027216989716480>',area=AREA_MONO,accuracy=100,damageOnArmor=1.33,ultimate=True,cooldown=7,description="Après un tour de chargement, déployez des drones énergétiques qui tirent un puissant rayon coloré sur un adversaire depuis le ciel")
bigMonoLaserRep = effect("Cast - Las. Chrom. - Conf. Mono","bigMonoLaserEff",turnInit=2,silent=True,emoji=dangerEm,replique=bigMonoLaser)
bigMonoLaser2 = skill(bigMonoLaser.name,"up",bigMonoLaser.type,750,area=bigMonoLaser.area,emoji=bigMonoLaser.emoji,effectOnSelf=bigMonoLaserRep,ultimate=bigMonoLaser.ultimate,cooldown=bigMonoLaser.cooldown,message="Les drones de {0} s'envolent")
invocBat2 = skill("Invocation - Chauve-souris II","uo",TYPE_SUMMON,500,invocation="Chauve-Souris II",emoji="<:cuttybat2:904369379762925608>",shareCooldown=True,use=CHARISMA,cooldown=3)
invocCarbunR = skill("Invocation - Carbuncle Rubis","un",TYPE_SUMMON,500,invocation="Carbuncle Rubis",emoji="<:invocRuby:919857898195128362>",shareCooldown=True,use=MAGIE,cooldown=3)
ConcenEff = effect("Concentration",'oj',redirection=50,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji('<:concenB:1138879438738706453>','<:concenR:1138879459307556889>'),turnInit=1,description="Une partie des dégâts directs reçu par le porteur de l'effet sont redirigé vers le combattant qui a donné l'effet")
concenEff2 = copy.deepcopy(defenseUp)
concenEff2.power = 15
concen = skill("Concentration","um",TYPE_BOOST,price=500,effects=[ConcenEff,concenEff2],range=AREA_MONO,area=AREA_DONUT_2,cooldown=5,emoji='<:concentration:1138879338805211156>',description="Réduit et redirige une partie des dégâts subis par vos alliés autour de vous sur vous-même")
memAlice = skill("Ultima Sanguis Rosae","memAlice",TYPE_HEAL,1000,150,AREA_MONO,maxHpCost=25,shareCooldown=True,area=AREA_DONUT_4,cooldown=7,ultimate=True,group=SKILL_GROUP_HOLY,use=CHARISMA,emoji='<a:memAlice2:908424319900745768>',description="Cette compétence soigne les alliés vivants et recussite les alliés morts pour une certaine valeur des soins initiaux",effectAroundCaster=[TYPE_RESURECTION,AREA_CIRCLE_6,150])
memAliceCast = effect("Cast - {0}".format(memAlice.name),"aliceMementoCast",replique=memAlice,turnInit=2,silent=True,emoji=uniqueEmoji('<a:memAliceCast:908413832194588723>'))
memAlice2 = copy.deepcopy(memAlice)
memAlice2.id, memAlice2.power, memAlice2.effectOnSelf, memAlice2.emoji, memAlice2.maxHpCost, memAlice2.effectAroundCaster = "ul",0,memAliceCast,'<a:memAliceCast:908413832194588723>', 0, None
blackHole = skill("Trou noir","uk",TYPE_PASSIVE,ironWillSkill.price,effectOnSelf="ol",use=ENDURANCE,emoji='<:blackHole:906195944406679612>',quickDesc="Accroi la probabilité d'être pris pour cible et diminue les dégâts indirects reçus")
blackHoleEff2 = copy.deepcopy(constEff)
blackHoleEff2.power, blackHoleEff2.aggro, blackHoleEff2.turnInit, blackHoleEff2.stat = 50, 35, 3, PURCENTAGE
blackHoleEff4 = copy.deepcopy(absEff)
blackHoleEff4.power, blackHoleEff4.turnInit = blackHoleEff2.power, blackHoleEff2.turnInit
blackHoleEff3 = effect("Horizon des événements","on",redirection=50,description="Quelqu'un attire les dégâts sur lui",turnInit=3,aggro=-15,emoji='<:blackHole2:906195979332640828>')
blackHole2 = skill("Trou noir Avancé","uj",TYPE_BOOST,0,use=None,effects=blackHoleEff3,effectOnSelf=blackHoleEff2,emoji='<:blackHole2:906195979332640828>',cooldown=7,ultimate=True,description="Redirige **{0}%** des dégâts directs reçus par vos alliés proches vers vous tout en diminuant leur agression, et augmente vos PV Maximums et vos soins reçus de **{1}%**, le tout durant {2} tours".format(blackHoleEff3.redirection,blackHoleEff2.power,blackHoleEff2.turnInit),area=AREA_DONUT_2,range=AREA_MONO,effectAroundCaster=[TYPE_BOOST,AREA_MONO,blackHoleEff4])
fireCircle = skill("Cercle de feu","ui",TYPE_DAMAGE,350,100,AREA_DIST_5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],effects='oo',area=AREA_DONUT_1,cooldown=5,use=MAGIE,emoji='<:fireCircle:906219518760747159>',effBeforePow=True)
waterCircle = skill("Cercle d'eau","uh",TYPE_DAMAGE,350,70,AREA_DIST_5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],effects='op',area=AREA_DONUT_1,cooldown=5,use=MAGIE,emoji='<:waterCircle:906219492135276594>',effBeforePow=True)
airCircle = skill("Cercle d'air","ug",TYPE_DAMAGE,350,100,AREA_CIRCLE_2,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],effects='oq',area=AREA_DONUT_1,cooldown=5,use=MAGIE,emoji='<:airCircle:906219469200842752>',effBeforePow=True)
earthCircle = skill("Cercle de terre","uf",TYPE_DAMAGE,350,70,AREA_DIST_5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],effects='or',area=AREA_DONUT_1,cooldown=5,use=MAGIE,emoji='<:earthCircle:906219450129317908>',effBeforePow=True)
fireShot = skill("Tir Feu","ue",TYPE_DAMAGE,350,95,area=AREA_CONE_2,cooldown=5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],range=AREA_DIST_5,emoji='<:fireShot:906219594639876116>')
waterShot = skill("Tir Eau","ud",TYPE_DAMAGE,350,110,cooldown=5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],range=AREA_DIST_5,emoji='<:waterShot:906219607856119868>')
airStrike = skill("Frappe Air","uc",TYPE_DAMAGE,350,95,area=AREA_CONE_2,cooldown=5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],range=AREA_CIRCLE_2,emoji='<:airStrike:906219547873386526>')
earthStrike = skill("Frappe Terre","ub",TYPE_DAMAGE,350,110,cooldown=5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],range=AREA_CIRCLE_2,emoji='<:earthStrike:906219563832709142>')

timeSpEff = effect("Rembobinage","nigHotMF", stat=CHARISMA,power=30,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,turnInit=5,emoji=uniqueEmoji('<:rlb:907687694476378112>'),stackable=True,description='Un effet de soin sur la durée qui se déclanche en début de tour')
timeSp = skill("Rembobinage","tu",TYPE_INDIRECT_HEAL,500,use=CHARISMA,range=AREA_MONO,area=AREA_CIRCLE_5,effects=timeSpEff,condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],cooldown=7,ultimate=True,emoji='<:rlb:907687694476378112>')
spaceSp = skill("Pluie d'étoiles","tt",TYPE_DAMAGE,500,150,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE],cooldown=5,area=AREA_CIRCLE_2,ultimate=True,emoji='<:starFall:907687023140302908>')
idoOH = skill("Apothéose","ts",TYPE_PASSIVE,500,effectOnSelf="idoOHEff",emoji='<:IdoOH:909278546172719184>',condition=[EXCLUSIVE,ASPIRATION,IDOLE],use=None,quickDesc="Permet de convertir une partie des soins exessifs en armure")
proOH = skill("Protection Avancée","tr",TYPE_PASSIVE,500,effectOnSelf="proOHEff",emoji='<:proOH:909278525528350720>',condition=[EXCLUSIVE,ASPIRATION,VIGILANT],use=None,quickDesc="Permet de convertir une partie des soins exessifs en armure")
altOH = skill("Bénédiction","tq",TYPE_PASSIVE,500,effectOnSelf="altOHEff",emoji='<:altOH:909278509145395220>',condition=[EXCLUSIVE,ASPIRATION,ALTRUISTE],use=None,group=SKILL_GROUP_HOLY,quickDesc="Permet de convertir une partie des soins exessifs en armure")
lightAura2 = skill("Aura de Lumière Avancée","tp",TYPE_PASSIVE,500,effectOnSelf="lightaura2Pa",emoji="<:lightAura2:1106836809083781120>",use=CHARISMA,quickDesc="Permet de soigner les ennemis alentours lorsque vous êtes attaqué",condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
tripleMissilesLaunch = skill("Missiles téléguidés","tripleMissiles",TYPE_DAMAGE,750,200,ultimate=True,repetition=3,damageOnArmor=1.2,percing=0,cooldown=10,emoji='<:missiles:909727253414445057>',condition=[EXCLUSIVE,ASPIRATION,OBSERVATEUR])
tripleMissilesEff2 = effect("Cast - {0}".format(tripleMissilesLaunch.name),"tripleMissilesEff2",turnInit=2,silent=True,emoji=sameSpeciesEmoji("<a:missileSoonB:909727376273965097>","<a:missilesSoonR:909727492510740501>"),replique=tripleMissilesLaunch)
tripleMissilesCast2 = copy.deepcopy(tripleMissilesLaunch)
tripleMissilesCast2.power, tripleMissilesCast2.message, tripleMissilesCast2.effectOnSelf, tripleMissilesCast2.id = 0,"{0} lance ses missiles",tripleMissilesEff2,"tripleMissilesCast"
tripleMissilesEff = effect("Cast - {0}".format(tripleMissilesLaunch.name),"tripleMissilesEff",turnInit=2,silent=True,emoji=uniqueEmoji('<:missilesCast:909727680264560690>'),replique=tripleMissilesCast2)
tripleMissiles = copy.deepcopy(tripleMissilesCast2)
tripleMissiles.effectOnSelf,tripleMissiles.message,tripleMissiles.say,tripleMissiles.id = tripleMissilesEff,"{0} calibre ses missiles","Ok, les missiles sont prêts pour le lancement !","to"
lightHeal2 = skill("Illumination","tn",TYPE_HEAL,350,85,cooldown=5,use=CHARISMA,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],emoji='<:illu:909134286203006997>')
extraEtingEff = effect("Récupération","eting+", stat=CHARISMA,power=30,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji=sameSpeciesEmoji('<:emeB:909132040392302703>','<:emeR:909132070251536486>'))
extraEtingEff3 = copy.deepcopy(extraEtingEff)
extraEtingEff3.power, extraEtingEff3.name = 20, extraEtingEff3.name + " ({0}%)".format(round(20/extraEtingEff.power*100))
extraEtingEff2 = effect("Récupération (AoE)","eting++",trigger=TRIGGER_INSTANT,callOnTrigger=extraEtingEff3,emoji=extraEtingEff3.emoji[0][0],area=AREA_DONUT_1)
extraEting = skill("Récupération","tm",TYPE_INDIRECT_HEAL,500,effects=[extraEtingEff,extraEtingEff3],cooldown=5,emoji=extraEtingEff.emoji[0][0],condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],description="Octroi un effet régénérant à l'allié ciblé, et un effet moins puissant aux alliés autour de lui")
strengthOfWill = skill("Force de volonté","feliUltLaunch",TYPE_DAMAGE,0,power=220,cooldown=7,ultimate=True,emoji='<:feliSlash:916208942974132245>',tpCac=True,armorConvert=50,description="Après un tour de chargement, inflige de lours dégâts à l'ennemi ciblé et en convertie une partie en armure")
strengthOfWillCastEff = effect("Cast - Force de volonté","castFeliEff",turnInit=2,silent=True,emoji=uniqueEmoji('<a:feliSlashCast:932819458186158160>'),replique=strengthOfWill)
strengthOfWillCast = copy.deepcopy(strengthOfWill)
strengthOfWillCast.id, strengthOfWillCast.power, strengthOfWillCast.effectOnSelf,strengthOfWillCast.message, strengthOfWillCast.tpCac = "tl",0,strengthOfWillCastEff,"{0} rassemble toute sa Détermination dans son arme", False

sixtineUltEff = copy.deepcopy(dmgDown)
sixtineUltEff.power, sixtineUltEff.stat, sixtineUltEff.description, sixtineUltEff.turnInit = 5, INTELLIGENCE, "Réduit les dégâts infligés par le porteur de l'effet de **{0}%**", 3
sixtineUltEff3 = effect("Réveil Soudain","sixtineUltEff3", stat=INTELLIGENCE,power=35,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,emoji=sameSpeciesEmoji('<:critB:925763298346033193>','<:critR:925763310383677490>'))
sixtineUltEff2 = effect("Somnolence","sixtineUltEff2", stat=INTELLIGENCE,strength=-5,magie=-5,charisma=-5,intelligence=-5,type=TYPE_MALUS,emoji='<:night:911735172901273620>',trigger=TRIGGER_AFTER_DAMAGE,callOnTrigger=sixtineUltEff3,turnInit=3,lvl=1)
sixtineUlt = skill("Douce nuit","tk",TYPE_MALUS,0,range=AREA_MONO,area=AREA_ALL_ENEMIES,use=INTELLIGENCE,effects=[sixtineUltEff,sixtineUltEff2],ultimate=True,cooldown=7,emoji='<:night:911735172901273620>',description="Réduit les statistiques des ennemis ainsi que leurs dégâts infligés. Si un ennemi subit des dégâts, le malus de statistique est retiré et des dégâts supplémentaires sont infligés")
hinaUltEff = copy.deepcopy(deepWound)
hinaUltEff.stat, hinaUltEff.power = STRENGTH, 20
hinaUlt = skill("Déluge de Plumes","tj",TYPE_DAMAGE,0,power=35,accuracy=60,area=AREA_CONE_2,repetition=5,cooldown=7,emoji='<:featherStorm:909932475457884191>',effects=hinaUltEff,description="Inflige à plusieurs reprises des dégâts aux ennemis ciblés et inflige {0} {1} à chaque fois que la cible principale est touchée".format(hinaUltEff.emoji[0][0],hinaUltEff.name))
julieUltEff = effect("Prolongation","JulieUltEff", stat=CHARISMA,power=15,turnInit=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,stackable=True,emoji=uniqueEmoji('<:plg:911734437597835316>'),description="Un effet de soin sur la durée qui se déclanche en début de tour")
julieUlt = skill("Prolongation","ti",TYPE_INDIRECT_HEAL,0,area=AREA_CIRCLE_3,range=AREA_MONO,emoji='<:plg:911734437597835316>',effects=julieUltEff,cooldown=5,use=CHARISMA)
invocSeraf = skill("Invocation - Fée protectrice","th",TYPE_SUMMON,500,invocation="Fée protectrice",emoji="<:seraphin:911078421361205289>",shareCooldown=True,use=INTELLIGENCE,cooldown=5)

bloodCross = skill("Blood Cross","tg",TYPE_DAMAGE,1000,emoji="<:clemRay:978376646262403144>",power=150,condition=[EXCLUSIVE,ASPIRATION,MAGE],ultimate=True,cooldown=7,area=AREA_INLINE_3,use=MAGIE,description="Inflige de gros dégâts dans une zone en forme de croix en infligeant forcément un coup critique à la cible principale tout en vous soignant et vous octroyant une armureen fonction des dégâts infligés",lifeSteal=10,armorConvert=10,garCrit=True)

soulaEff = effect("Traité de soulagement","soulaArmor", stat=INTELLIGENCE,overhealth=50,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji('<:tsB:911732326818545664>','<:tsR:911732347601317908>'))
soulagement = skill("Traité de soulagement","tf",TYPE_ARMOR,500,AREA_MONO,condition=[EXCLUSIVE,ASPIRATION,PREVOYANT],area=AREA_CIRCLE_2,use=INTELLIGENCE,cooldown=5,effects=soulaEff,emoji='<:soul:911732783993483284>')
bloodyStrike = skill("Frappe sanguine",'te',TYPE_DAMAGE,500,105,AREA_CIRCLE_2,condition=[EXCLUSIVE,ASPIRATION,BERSERK],lifeSteal=35,cooldown=5,armorConvert=35,emoji='<:berkSlash:916210295867850782>',description="Inflige des dégâts à l'ennemi ciblé, vous soigne et vous octroi une armure en fonction d'une partie des dégâts infligés")
infraMedica = skill("Medica","td",TYPE_HEAL,500,65,AREA_MONO,condition=[EXCLUSIVE,ASPIRATION,ALTRUISTE],area=AREA_CIRCLE_2,cooldown=5,emoji='<:medica:1137300676721000508>',description="Soigne les alliés alentours")
flambe = effect("Flambée","flambage", stat=STRENGTH,type=TYPE_INDIRECT_DAMAGE,turnInit=2,power=15,aggro=10,area=AREA_CIRCLE_1,description="Pour chaque attaque physique directe reçu par la cible, la puissance de cet effet augmente de {0} lors de son déclanchement, au début du prochain tour du lanceur",trigger=TRIGGER_ON_REMOVE,emoji=uniqueEmoji('<:flamb:913165325590212659>'))
flambeSkill = skill("Flambage","tc",TYPE_INDIRECT_DAMAGE,500,effects=flambe,cooldown=5,emoji='<:flamb:913165325590212659>')
magAch = effect("Magia atrocitas","magAch", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,turnInit=2,power=flambe.power,aggro=10,area=AREA_CIRCLE_1,description="Pour chaque attaque spirituelle directe reçu par la cible, la puissance de cet effet augmente de {0} lors de son déclanchement, au début du prochain tour du lanceur",trigger=TRIGGER_ON_REMOVE,emoji=uniqueEmoji('<:magAch:913165311291842571>'))
magAchSkill = skill("Magia atrocitas","tb",TYPE_INDIRECT_DAMAGE,500,effects=magAch,cooldown=5,emoji='<:magAch:913165311291842571>')
idoOS = skill("Clou du spectacle","ta",TYPE_PASSIVE,500,effectOnSelf="idoOSEff",emoji='<:osIdo:913885207751446544>',condition=[EXCLUSIVE,ASPIRATION,INOVATEUR],use=None,quickDesc="Permet à vos armures d'absorber plus de dégâts lorsqu'elles sont détruites")
proOS = skill("Extra Protection","sz",TYPE_PASSIVE,500,effectOnSelf="proOSEff",emoji='<:osPro:913885191800512562>',condition=[EXCLUSIVE,ASPIRATION,PROTECTEUR],use=None,quickDesc="Permet à vos armures d'absorber plus de dégâts lorsqu'elles sont détruites")
preOS = skill("Armures Avancées","sy",TYPE_PASSIVE,500,effectOnSelf="preOSEff",emoji='<:osPre:913885175161712710>',condition=[EXCLUSIVE,ASPIRATION,PREVOYANT],use=None,quickDesc="Permet à vos armures d'absorber plus de dégâts lorsqu'elles sont détruites")
geoConBoost = effect("Géo-Controle","geocontroled", stat=INTELLIGENCE,strength=15,endurance=10,charisma=10,agility=5,precision=5,intelligence=10,magie=15,resistance=2,description="Une grande force vous envahis",emoji=sameSpeciesEmoji("<:geoContB:918422778414256158>","<:geoContR:918422792649723914>"))
geoConLaunch = skill("Géo-Controle","sx",TYPE_BOOST,1000,range=AREA_MONO,area=AREA_CIRCLE_3,effects=geoConBoost,cooldown=7,use=INTELLIGENCE,ultimate=True,emoji='<:geoCont:918422710781083668>',url="https://media.discordapp.net/attachments/1130204608900386910/1130580362381230131/20230717_212119.gif",description="Après un tour de chargement, accroi grandement toutes les statistiques des alliés")
geoConCastEff = effect("Cast - {0}".format(geoConLaunch.name),"geoControleCastEff",turnInit=2,silent=True,replique=geoConLaunch)
geoConCast = copy.deepcopy(geoConLaunch)
geoConCast.id, geoConCast.effects, geoConCast.effectOnSelf, geoConCast.url = "sx",[None],geoConCastEff, "https://media.discordapp.net/attachments/1130204608900386910/1130579692588630026/20230717_211801.gif"
kikuRes = skill("Mors vita est","sw",TYPE_RESURECTION,750,120,AREA_MONO,area=AREA_DONUT_5,emoji='<:mortVitaEst:916279706351968296>',initCooldown=3,shareCooldown=True,description="Réanime les alliés vaincus dans la zone d'effet",use=CHARISMA,group=SKILL_GROUP_DEMON,hpCost=25)
memClemLauchSkill = skill("Ultima Sanguis Pluviae","memClemSkillLauch",TYPE_DAMAGE,0,300,AREA_MONO,percing=0,accuracy=666,area=AREA_CIRCLE_7,ultimate=True,use=MAGIE,cooldown=99,emoji="<:clemMemento:902222089472327760>",description="\n__Effets lors du premier tour de chargement :__\nDéfini vos PVs courants à **1**\nObtenez un bouclier absolu d'une valeur de **50%** des PVs perdus\nDivise votre Résistance Soins de **50%**\nDiminue vos PV maximums de **50%** pour le reste du combat\nDonne l'effet __Incurable (50)__ sur le lanceur pour le reste du combat")
memClemCastSkillEff = effect("Cast - Ultima Sanguis Pluviae","memClemSkillCast",turnInit=2,silent=True,emoji=dangerEm,replique=memClemLauchSkill)
memClemCastSkill = copy.deepcopy(memClemLauchSkill)
memClemCastSkill.id, memClemCastSkill.effectOnSelf, memClemCastSkill.power = "sv",memClemCastSkillEff,0
rosesThornEff = effect("Epines","rosesMagEff2", stat=CHARISMA,power=35,trigger=TRIGGER_INSTANT,type=TYPE_INDIRECT_DAMAGE,emoji=sameSpeciesEmoji("<:epineB:917665759684079626>","<:epineR:917665743649275904>"))
rosesMagicEff = effect("Pétales","rosesMagEff", stat=CHARISMA,endurance=5,resistance=3,turnInit=3,emoji=sameSpeciesEmoji("<:rosesAreBlue:917665779770613761>","<:rosesAreRed:917665805557198878>"),trigger=TRIGGER_AFTER_DAMAGE,thornEff=True,callOnTrigger=rosesThornEff)
roses = skill("Roses","su",TYPE_BOOST,500,use=CHARISMA,effects=[rosesMagicEff],cooldown=5,description="Augmente les statistiques défensives de l'allié ciblé et inflige des dégâts indirects aux ennemis qui l'attaque",emoji='<:roses:932612186130493450>')
krysUlt = skill("Réassemblage","st",TYPE_DAMAGE,0,100,cooldown=5,description="Inflige des dégâts à la cible (dégâts augmentés sur l'armure). Vole une partie des dégâts infligés à l'armure de l'adversaire et convertie une partie des dégâts infligés en armure",emoji='<:reconvert:916121466423091240>',damageOnArmor=2,armorSteal=100,armorConvert=100)
chaosArmorEff = effect("Armure du Chaos","chaosArmor", stat=INTELLIGENCE,overhealth=1,emoji=sameSpeciesEmoji('<a:caB:938375004792426496>','<a:caR:938375020261023825>'),description="Une armure chaotique dont la puissance de base est aléatoire",type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,turnInit=3)
chaosArmor = skill("Armure du Chaos","ss",TYPE_ARMOR,emoji='<a:chaosArmor:938374846843342869>',area=AREA_CIRCLE_2,price=500,effects=chaosArmorEff,cooldown=5,use=INTELLIGENCE)
firelame = skill("Ignis ferrum","sr",TYPE_DAMAGE,500,45,range=AREA_DIST_5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],cooldown=7,area=AREA_ARC_1,repetition=3,emoji='<:fireLame:916130324197543986>',damageOnArmor=1.1)
airlame = skill("Aer ferrum","sq",TYPE_DAMAGE,500,45,range=AREA_CIRCLE_3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],cooldown=7,area=AREA_ARC_1,repetition=3,emoji='<:airLame:916130609095655454>',damageOnArmor=1.1)
waterlame = skill("Aqua ferrum","sp",TYPE_DAMAGE,500,55,range=AREA_DIST_5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],cooldown=7,repetition=3,emoji='<:aquaLame:916130446125977602>',damageOnArmor=1.1)
mudlame = skill("Lapis ferrum","so",TYPE_DAMAGE,500,55,range=AREA_CIRCLE_3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],cooldown=7,repetition=3,emoji='<:earthLame:916130398914875452>',damageOnArmor=1.1)
shadowLameEff = effect("Umbra ferrum","lameD'ombre", stat=STRENGTH,power=40,stackable=True,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:darkLame:916130473162453033>'))
shadowLame = skill("Umbra ferrum","sn",TYPE_INDIRECT_DAMAGE,500,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS],effects=[shadowLameEff,shadowLameEff,shadowLameEff],cooldown=7,emoji='<:darkLame:916130473162453033>')
lightLameEffTrig = effect("Lux ferrum","lightLameTrig", stat=CHARISMA,power=35,trigger=TRIGGER_INSTANT,type=TYPE_INDIRECT_DAMAGE,emoji="<:lightLame:916131830149816340>")
lightLameEff = effect("Lux ferrum","lameDeLumière", stat=CHARISMA,resistance=5,callOnTrigger=lightLameEffTrig,lvl=3,description="En plus de booster légèrement la résistance de la cible, inflige des dégâts indirects lorsque cette dernière est attaquée",trigger=TRIGGER_AFTER_DAMAGE,thornEff=True,emoji=uniqueEmoji('<:lightLame:916131830149816340>'))
lightLame = skill("Lux ferrum","sm",TYPE_BOOST,500,effects=lightLameEff,emoji='<:lightLame:916131830149816340>',cooldown=7,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],use=CHARISMA)
astraLameEffTrig = effect("Stella ferrum","lameétoiléeTrig", stat=ENDURANCE,power=35,trigger=TRIGGER_INSTANT,type=TYPE_INDIRECT_DAMAGE,emoji="<:astralLame:916131872352911400>")
astralLameEff = effect("Stella ferrum","lameétoilée", stat=ENDURANCE,resistance=5,callOnTrigger=astraLameEffTrig,lvl=3,description="En plus de booster légèrement la résistance de la cible, inflige des dégâts indirects lorsque cette dernière est attaquée",trigger=TRIGGER_AFTER_DAMAGE,thornEff=True,emoji=uniqueEmoji('<:astralLame:916131872352911400>'),turnInit=2)
astralLame = skill("Stella ferrum","sl",TYPE_BOOST,500,range=AREA_MONO,effects=astralLameEff,emoji='<:astralLame:916131872352911400>',cooldown=7,condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE],use=ENDURANCE)
timeLameEffTrig = effect("Tempus ferrum","lameDuTempsTrig", stat=CHARISMA,power=35,trigger=TRIGGER_INSTANT,type=TYPE_INDIRECT_DAMAGE,emoji="<:timeLame:916131853499527208>")
timeLameEff = effect("Tempus ferrum","lameDuTemps", stat=CHARISMA,resistance=5,callOnTrigger=timeLameEffTrig,lvl=3,description="En plus de booster légèrement la résistance de la cible, inflige des dégâts indirects lorsque cette dernière est attaquée",trigger=TRIGGER_AFTER_DAMAGE,thornEff=True,emoji=uniqueEmoji('<:timeLame:916131853499527208> '))
timeLame = skill("Tempus ferrum","sk",TYPE_BOOST,500,effects=timeLameEff,emoji='<:timeLame:916131853499527208>',cooldown=7,condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],use=CHARISMA)
magicRuneStrike = skill("Frappe Runique",'sj',TYPE_DAMAGE,500,bloodyStrike.power,bloodyStrike.range,condition=[EXCLUSIVE,ASPIRATION,ENCHANTEUR],cooldown=bloodyStrike.cooldown,lifeSteal=bloodyStrike.lifeSteal,armorConvert=bloodyStrike.armorConvert,emoji='<:magicoRune:916401319990947920>',use=MAGIE)
infinitDarkEff = effect("Noirceur infinie","bigDarkDark", stat=MAGIE,stackable=True,power=60,turnInit=5,lvl=5,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji("<:bigDark:916561798948347935>"))
infinitDark = skill("Noirceur infinie","si",TYPE_INDIRECT_DAMAGE,500,emoji='<:bigDark:916561798948347935>',effects=infinitDarkEff,cooldown=7,ultimate=True,use=MAGIE,description="Inflige des dégâts indirects à l'ennemi ciblé durant un petit moment")
preciseShot = skill("Tir précis","sh",TYPE_DAMAGE,500,120,cooldown=5,use=PRECISION,emoji='<:preciseShot:916561817969500191>')
troublon = skill("Troublon","sg",TYPE_DAMAGE,500,100,cooldown=3,area=AREA_CONE_2,range=AREA_MONO,emoji='<:mousqueton:916561833920462889>')
haimaShield = effect("Haima - Bouclier","haimaShield",stat=INTELLIGENCE,overhealth=20,turnInit=2,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,emoji=sameSpeciesEmoji("<:haimaB:916922889679286282>","<:haimaR:916922905672171570>"))
haimaEffect = effect("Haima","haimaEff",lvl=3,callOnTrigger=haimaShield,emoji='<:haima:916922498094858251>',trigger=TRIGGER_AFTER_DAMAGE)
haimaSkill = skill("Haima","sf",TYPE_ARMOR,500,emoji='<:haima:916922498094858251>',effects=[haimaEffect,haimaEffect.callOnTrigger],cooldown=5,use=INTELLIGENCE,description="Octroi {0} et {1} à l'allié ciblé. Si {1} est détruit par une attaque ennemi, l'effet lui est re-octroyé (maximum {2} fois)".format(haimaEffect,haimaEffect.callOnTrigger,haimaEffect.lvl))
pandaimaShield = copy.deepcopy(haimaShield)
pandaimaShield.name, pandaimaShield.overhealth, pandaimaShield.emoji = "Panhaima (Armure)", 10, sameSpeciesEmoji('<:panhaimaB:916922951054540810>','<:panhaimaR:916922965420040263>')
pandaimaEff = copy.deepcopy(haimaEffect)
pandaimaEff.callOnTrigger, pandaimaEff.name, pandaimaEff.emoji, pandaimaEff.lvl = pandaimaShield, "Panhaima", uniqueEmoji('<:pandaima:982349300505931856>'), 3
pandaima = copy.deepcopy(haimaSkill)
pandaima.name, pandaima.effects, pandaima.range, pandaima.area, pandaima.emoji, pandaima.description = "Panhaima", [pandaimaEff,pandaimaEff.callOnTrigger], AREA_MONO, AREA_CIRCLE_2, "<:pandaima:982349300505931856>", "Octroi {0} et {1} aux alliés alentours et vous-même. Si {1} est détruite par une attaque adverse, l'effet est re-octroyé à la cible (maximum {2} fois)".format(pandaimaEff,pandaimaEff.callOnTrigger,pandaimaEff,pandaimaEff.lvl)

haimaBundle = skill("(Pan)Haima",haimaSkill.id,TYPE_ARMOR,become=[haimaSkill,pandaima],emoji=haimaSkill.emoji,description="Vous permet d'utilse {0} et {1}, deux compétences d'armures qui octroi une nouvelle armure lorsque l'armure initiale est brisée".format(haimaSkill,pandaima),price=500)

physicRuneEff1 = effect("Sanguis Pact","SinguisPact", stat=PURCENTAGE,strength=25,power=25,turnInit=-1,unclearable=True,emoji='<:pacteDeSang:917096147452035102>')
magicRuneEff1 = effect("Animae Foedus","AnimaeFoedus", stat=PURCENTAGE,magie=25,power=25,turnInit=-1,unclearable=True,emoji='<:pacteDame:917096164942295101>')
physicRuneEff2 = effect("Contre-coup","pacteReturn", stat=PURCENTAGE,power=7.5,turnInit=-1,unclearable=True,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN)
physicRune = skill("Sanguis Pact","se",TYPE_PASSIVE,750,effects=[physicRuneEff1,physicRuneEff2],description="Augmente de **{0}%** votre {1} Force et inflige un malus de PV incurables équivalent à **{2}%** des dégâts directs infligés, mais vous fait subir des dégâts équivalents à **{3}%** de vos PVs Max à chaque fin de tours".format(physicRuneEff1.strength,statsEmojis[STRENGTH],physicRuneEff1.power, physicRuneEff2.power))
magicRune = skill("Animae Foedus","sd",TYPE_PASSIVE,750,effects=[magicRuneEff1,physicRuneEff2],description="Augmente de **{0}%** votre {1} Force et inflige un malus de PV incurables équivalent à **{2}%** des dégâts directs infligés, mais vous fait subir des dégâts équivalents à **{3}%** de vos PVs Max à chaque fin de tours".format(magicRuneEff1.strength,statsEmojis[MAGIE],magicRuneEff1.power, physicRuneEff2.power))
lightBigHealArea = skill("Lumière éclatante","sb",TYPE_HEAL,750,90,AREA_MONO,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],ultimate=True,area=AREA_CIRCLE_4,cooldown=7,use=CHARISMA,emoji='<:eclatLum:1067824343658283089>')
focus = skill("Focus","sa",TYPE_INDIRECT_DAMAGE,1000,range=AREA_CIRCLE_4,cooldown=7,effects=bleeding,effPowerPurcent=int(50/bleeding.power*100),effectOnSelf=bleeding,shareCooldown=True,use=STRENGTH,description="Applique un puissant effet __Hémorragie__ à la cible, avec un contre coup",emoji='<:focus:925204899514417182>')
FAIRYRAYMONODMG, FAIRYRAYAOEDMG, FAIRYRAYPOWER = 100, 50, 125
fairyRayEff = effect("Explosion Empoisonnée","fairyRayEff", stat=MAGIE,power=FAIRYRAYAOEDMG,area=AREA_DONUT_2,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,emoji='<:fairyRay:1172873672151806093>',description="Si la cible souffre de {0} {1} :\n- Inflige des dégâts indirects avec une puissance équivalante à **{2}%** de la puissance cumulée de l'effet restante\n- Inflige des dégâts indirects aux ennemis proches avec une puissance équivalente à **{3}%** de la puissance cumulée de l'effet restante\n- Consomme l'effet\n\nSinon :\n- Inflie {0} {1} avec **{4}%** de sa puissance".format(estial.emoji[0][0],estial.name,FAIRYRAYMONODMG,FAIRYRAYAOEDMG,FAIRYRAYPOWER))
fairyRay = skill("Rayon Féérique","zzz",TYPE_DAMAGE,500,100,AREA_INLINE_5,emoji=fairyRayEff.emoji[0][0],use=MAGIE,effects=fairyRayEff,area=AREA_LINE_5,cooldown=7,description="Inflige des dégâts (direct) en ligne. Si l'ennemi ciblé souffre de {0} {1}, lui inflige des dégâts supplémentaires et inflige des dégâts aux ennemis autour en consommant l'effet. Sinon, lui inflige l'effet".format(estial.emoji[0][0],estial.name))

bleedingPuitAoEBleed = copy.deepcopy(bleeding)
bleedingPuitAoEBleed.power, bleedingPuitAoEBleed.name = bleedingPuitAoEBleed.power * 0.65, bleedingPuitAoEBleed.name + " (65%)"
bleedingPuitAoE = effect("Lacération","lacerEff",callOnTrigger=bleedingPuitAoEBleed,area=AREA_DONUT_2,type=TYPE_MALUS,trigger=TRIGGER_INSTANT,emoji='<:mudraLacer:1189975861068320768>')
bleedingPuit = skill("Mûdra Lacérant","zzy",TYPE_DAMAGE,500,135,area=AREA_CIRCLE_1,effects=[bleeding,bleedingPuitAoE],cooldown=7,emoji=bleedingPuitAoE.emoji[0][0],effPowerPurcent=int(35/bleeding.power*100),useActionStats=ACT_INDIRECT,description="Inflige des dégâts aux ennemis ciblés et leur inflige {0} {1}".format(bleeding.emoji[0][0],bleeding.name))
supprZone = skill("Dispersion","zzx",TYPE_DAMAGE,650,100,emoji='<:principio:919529034663223376>',cooldown=5,use=MAGIE,damageOnArmor=3,accuracy=80,area=AREA_CIRCLE_1)
invocCarbSaphir = skill("Invocation - Carbuncle Saphir","zzw",TYPE_SUMMON,500,invocation="Carbuncle Saphir",emoji="<:innvocSafir:919857914490007574>",shareCooldown=True,use=STRENGTH,cooldown=3)
invocCarbObsi = skill("Invocation - Carbuncle Obsidienne","zzv",TYPE_SUMMON,500,invocation="Carbuncle Obsidienne",emoji="<:invocObs:919872508226830336>",shareCooldown=True,use=STRENGTH,cooldown=3)
requiemEff = effect("Requiem","reqEff", stat=CHARISMA,strength=-5,magie=-5,resistance=-3,turnInit=3,type=TYPE_MALUS,emoji=sameSpeciesEmoji('<:requiemB:1179147661971038309>','<:requiemR:1179147626952806450>'))
requiem = skill("Requiem","zzu",TYPE_DAMAGE,500,80,range=AREA_MONO,area=AREA_ALL_ENEMIES,use=CHARISMA,cooldown=7,emoji='<:requiem:1178936044238942258>',setAoEDamage=True,ultimate=True,effectAroundCaster=[TYPE_MALUS,AREA_ALL_ENEMIES,requiemEff],useActionStats=ACT_BOOST,description="Inflige des dégâts à tous les ennemis et réduit leurs statistiques. Plus un ennemi est proche du lanceur, plus les dégâts et le malus sont élevés",quickDesc="D'après Félicité, Alice avec un mégaphone est une arme trop violente pour la guerre")
cosmicEff = effect("Pouvoir cosmique","cosmicPowerEff", stat=HARMONIE,strength=5,magie=5,resistance=5,emoji=sameSpeciesEmoji('<:comicPowerB:919866210768801833>','<:cosmicPowerR:919866197850353685>'),redirection=15)
cosmicEffSelf = effect("Pouvoir cosmique","cosmicPowerEffOnSelf",resistance=20,emoji=sameSpeciesEmoji('<:comicPowerB:919866210768801833>','<:cosmicPowerR:919866197850353685>'))
cosmicPower = skill("Pouvoir cosmique","zzt",TYPE_BOOST,1000,range=AREA_MONO,area=AREA_DONUT_2,use=HARMONIE,cooldown=7,emoji='<:cosmic:919866054992334848>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE],effects=cosmicEff,effectOnSelf=cosmicEffSelf)
propag = skill("Propagation","zzs",TYPE_INDIRECT_DAMAGE,750,cooldown=7,emoji='<:propag:1190975386541113424>',initCooldown=3,use=MAGIE,effects=estial,description="Inflige {0} {1} à l'ennemi ciblé. Si d'autres ennemis sont proches de la cible, leur inflige également {0} {1} avec une puissance dépendante des dit effets déjà présents sur la cible. Si au contraire, la cible est isolée, augmente les dégâts indirects qu'elle subit durant un moment".format(estial.emoji[0][0], "__"+estial.name+"__"),power=40,effPowerPurcent=100)
inkResEff = effect("Pied au sec","inkRes", stat=INTELLIGENCE,turnInit=2,inkResistance=10,description="Réduit de 10% les dégâts indirects reçu.\nLe pourcentage de réduction est affecté par l'Intelligence et le Bonus aux Armures et Mitigation")
inkResEff2 = copy.deepcopy(inkResEff)
inkResEff2.stat, inkResEff2.name, inkResEff2.emoji = ENDURANCE, "Collectivement inconscient", sameSpeciesEmoji('<:incColB:921546169203687464>','<:incColR:921546151314985020>')
inkRes = skill("Pied au sec","zzr",TYPE_BOOST,500,effects=inkResEff,cooldown=5,area=AREA_CIRCLE_1,use=INTELLIGENCE,emoji='<:inkResR:921486021265354814>')
inkRes2 = skill("Bulle d'Inconscience","zzq",TYPE_BOOST,500,range=AREA_MONO,area=AREA_CIRCLE_2,effects=inkResEff2,cooldown=5,use=ENDURANCE,emoji='<:incCol:921545816940875817>')
booyahBombLauch = skill("Jolizator","zzp",TYPE_DAMAGE,750,200,area=AREA_CIRCLE_2,ultimate=True,cooldown=7,emoji='<:bobomb:921710328771932192>',url="https://cdn.discordapp.com/attachments/935769576808013837/935783888159125544/20220126_072826.gif")
booyahBombEff = effect("Cast - Jolizator","supercalifragilisticexpialiodocieux",turnInit=2,silent=True,emoji=sameSpeciesEmoji("<:booyahB:925796592240455701>","<:booyahR:925796570509766716>"),replique=booyahBombLauch)
booyahBombCast = copy.deepcopy(booyahBombLauch)
booyahBombCast.id, booyahBombCast.effectOnSelf, booyahBombCast.power, booyahBombCast.url = "zzp",booyahBombEff,0,"https://cdn.discordapp.com/attachments/935769576808013837/935783887748079666/20220126_073038.gif"
reconst = skill("Reconstitution","zzo",TYPE_HEAL,750,150,ultimate=True,use=CHARISMA,cooldown=7,emoji='<:mudh:922914512712138802>',description="Une puissante compétence de soins monocibles")
medicamentumEff = effect("Medicamentum","bigmonoindirect", stat=CHARISMA,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,turnInit=3,power=65,description="Un puissant effect soignant",emoji=sameSpeciesEmoji('<:mihB:922914323037306890>','<:mihR:922914344428240937>'))
medicamentum = skill("Medicamentum",'zzn',TYPE_INDIRECT_HEAL,750,ultimate=True,emoji='<:muih:922914495737757706>',cooldown=7,use=CHARISMA,effects=medicamentumEff)
ultMonoArmorEff = effect("Armis","ultMonoArmor", stat=INTELLIGENCE,overhealth=150,turnInit=3,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,emoji=sameSpeciesEmoji('<:runeArmis:963397040967131176>','<:armis:963397158101471272>'))
ultMonoArmor = skill("Armis","zzm",TYPE_ARMOR,750,ultimate=True,effects=ultMonoArmorEff,cooldown=7,use=INTELLIGENCE,emoji='<:runeArmis:963397040967131176>')

intelRaise = copy.deepcopy(renisurection)
intelRaise.name, intelRaise.use, intelRaise.id, intelRaise.emoji = "Egeiro", INTELLIGENCE, "zzf", '<:egiero:925768359964979210>'
ultRedirectSelfEff = effect("Teliki Anakatéfthynsi","ultRedirectShield", stat=ENDURANCE,overhealth=200,absolutShield=True,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,description="Vous accorde une grosse armure aboslue\nLes armures absolues protègent même des dégâts indirects et ne sont pas affectés par les multiplicateurs de dégâts sur l'armure")
ultRedirectEff = effect("Teliki Anakatéfthynsi","ultRedirect",redirection=100,trigger=TRIGGER_DAMAGE,emoji='<:tekeli:1138900473626230796>')
ultRedirect = skill("Teliki Anakatéfthynsi","zze",TYPE_BOOST,1000,range=AREA_MONO,area=AREA_DONUT_3,cooldown=7,ultimate=True,effects=ultRedirectEff,effectOnSelf=ultRedirectSelfEff,use=ENDURANCE,emoji='<:tekeli:1138900383540973608>')
clemency = skill('Clémence','zzd',TYPE_HEAL,350,120,cooldown=7,use=ENDURANCE,emoji='<:clemency:926433653037367318>',group=SKILL_GROUP_HOLY,effectAroundCaster=[TYPE_HEAL,AREA_MONO,60])
liuSkillSusEff = effect("Asuama","liuSussessArmor", stat=ENDURANCE,overhealth=75,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,inkResistance=10,turnInit=2,emoji=uniqueEmoji("<:liuArmor:922292960886915103>"))
liuSkillSus = skill("Guraundo Sutoraiku","zzc",TYPE_DAMAGE,0,100,range=AREA_CIRCLE_2,use=ENDURANCE,effectOnSelf=liuSkillSusEff,cooldown=5,emoji='<:liuSkill:922328931502280774>')
liaSkillSus = skill("Kuchu Sutoraiku","zzb",TYPE_DAMAGE,0,40,range=AREA_CIRCLE_1,cooldown=5,knockback=3,repetition=3,use=AGILITY,emoji='<:liaSkill:922291249002709062>')
lioSkillSusEff = effect('Shinju no haha',"lioSussessEff", stat=CHARISMA,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,power=15,turnInit=3,strength=5,magie=5,emoji=uniqueEmoji('<:lioWeap:908859876812415036>'))
lioSkillSus = skill("Shio",'zza',TYPE_INDIRECT_HEAL,0,cooldown=5,effects=lioSkillSusEff,area=AREA_CIRCLE_2,emoji='<:lioSkill:922328964926697505>')
lizSkillSusEff = effect("Tanka",'lizWillBurnThemAll', stat=MAGIE,power=multiMissiles.effects[0].power,area=AREA_CIRCLE_1,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:lizIndirect:917204753610571776>'))
lizSKillSus = skill("Shokyaku","zyz",TYPE_INDIRECT_DAMAGE,0,effects=lizSkillSusEff,area=AREA_CONE_4,cooldown=5,emoji='<:lizSkill:922328829765242961>',use=MAGIE)
friendlyPush = skill("Poussée amicale","movepls",TYPE_HEAL,0,power=1,range=AREA_DONUT_1,use=HARMONIE,knockback=2,replay=True,emoji='<:movePlz:928756987532029972>',say=["Madness ? THIS IS SPARTA !","* Out of my ways","SPAR-TA"],description="Pousse gentiment un allié de 2 cases et vous permet de rejouer votre tour")
pepsis = skill("Pepsis","zyy",TYPE_HEAL,500,50,AREA_MONO,area=AREA_CIRCLE_3,use=INTELLIGENCE,cooldown=5,emoji='<:pepsis:930049497214644235>',useActionStats=ACT_SHIELD)
darkShieldEff = effect("Nuit noirsisime","blackknightshield", stat=ENDURANCE,overhealth=75,turnInit=2,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji("<:dsR:930048553835970580>","<:dsR:930048570688675900>"))
darkShield = skill("Nuit noirsisime","zyx",TYPE_ARMOR,500,use=ENDURANCE,effects=darkShieldEff,cooldown=3,emoji='<:dsR:930048553835970580>')
rencCelEff = effect('Rencontre Céleste','rencontreCel', stat=CHARISMA,overhealth=50,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji('<:rcb:930048878668046377>','<:rcr:930048892886720603>'))
rencCel = skill("Rencontre Céleste",'zyw',TYPE_ARMOR,500,use=CHARISMA,range=AREA_MONO,area=AREA_CIRCLE_3,effects=rencCelEff,emoji='<:rencontreceleste:930049458488623104>',cooldown=5,useActionStats=ACT_HEAL)
valse = skill("Valse régénératrice","zyv",TYPE_HEAL,500,80,AREA_DONUT_5,area=AREA_CIRCLE_1,cooldown=5,description="Soigne en zone autour du lanceur et de l'allié le plus blessé",emoji='<:valse:930051603543760936>',useActionStats=ACT_DIRECT,effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_1,80])

eventFas = effect("Jauge de Fascination","evFac",turnInit=-1,unclearable=True,emoji='<:evFas:951824800488230932>')
eventFas.jaugeValue = jaugeValue(
    emoji=[["<:lej:980923743960461412>","<:mej:980923762016927764>","<:rej:980923786650075228>"],["<:lfj:980923958587191356>","<:mrj:980923874927575120>","<:rfj:980923857642856589>"]],
    conds=[jaugeConds(INC_START_TURN,10),
        jaugeConds(INC_ON_ALLY_CRIT,5),
        jaugeConds(INC_ON_SELF_CRIT,5)]
)

finalTechEff = copy.deepcopy(dmgUp)
finalTechEff.stat, finalTechEff.power = STRENGTH, 5
finalTech = skill("Final Technique","zyu",TYPE_DAMAGE,750,100,area=AREA_CIRCLE_2,range=AREA_MONO,description="Inflige des dégâts aux ennemis autour de vous et augmente les dégâts infligés par les alliés alentours en consommant votre {0} __{1}__. Plus la quantité de jauge consommée et élevée, plus la puissance de l'attaque et du bonus de dégâts sera grande".format(eventFas.emoji[0][0],eventFas.name),emoji='<:final:930051626062991371>',jaugeEff=eventFas,maxPower=150,maxJaugeValue=100,minJaugeValue=50,effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_2,finalTechEff])
dissi = skill("Dissipation","zyt",TYPE_HEAL,750,80,AREA_MONO,ultimate=True,cooldown=7,area=AREA_ALL_ALLIES,emoji='<:dissipation:930049419473211392>',use=HARMONIE,description="__**Nécessite d'avoir au moins une invocation propre sur le terrain**__\nDésinvoque toutes vos invocations pour effectuer un gros soins sur toute votre équipe. La puissance est multipliée par le nombre d'invocation renvoyés")
quickCastEff = effect("Magie Prompte","quickCast",emoji=uniqueEmoji("<:quickCast:930467995283779614>"),description="Permet d'ignorer **1** tour de chargement de la prochaine compétence à chargement utilisée",turnInit=1)
quickCast = skill("Magie Prompte","zys",TYPE_BOOST,1000,range=AREA_MONO,area=AREA_MONO,use=None,cooldown=99,description="Ignore 1 tour de chargement de votre prochaine compétence",initCooldown=3,replay=True,emoji='<:quickCast:930467995283779614>',effects=quickCastEff)
quickCast.iaPow = 0
foyer = skill("Foyer","zyr",TYPE_HEAL,500,35,range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=5,use=CHARISMA,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],emoji="<:fireplace:931666078092902471>")
sweetHeatEff = effect('Douce chaleur',"sweetHeat", stat=HARMONIE,power=25,turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,description="Un effet qui soigne le porteur pendant 3 tours")
sweetHeat = skill("Flammes intérieurs","zyq",TYPE_DAMAGE,500,120,range=AREA_CIRCLE_3,cooldown=7,effectOnSelf=sweetHeatEff,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],emoji='<:fireStrike:931715107002662912>',area=AREA_CONE_2)
darkSweetHeat = skill("Flammes infernales","zyp",TYPE_DAMAGE,500,120,range=AREA_DIST_5,cooldown=7,effectOnSelf=sweetHeatEff,use=MAGIE,description="Inflige des dégâts aux ennemis ciblés et vous octroi un effet régénératif",area=AREA_CONE_2,group=SKILL_GROUP_DEMON,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],emoji='<:infFlames:931716686745305149>',effPowerPurcent=125)
nacre = effect("Bulle nacrée",'nacre1', stat=INTELLIGENCE,overhealth=40,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,turnInit=2,stackable=True,emoji=uniqueEmoji('<:nacre:931666050322419732>'))
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
burningSoul = effect("Âme embrasée",'burningSoul', stat=HARMONIE,power=50,turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji='<:ayss:931711751702085672>')
abime = skill("Âbime",'sve',TYPE_INDIRECT_DAMAGE,500,area=AREA_CIRCLE_2,cooldown=5,ultimate=True,group=SKILL_GROUP_DEMON,hpCost=25,effects=[burningSoul],emoji='<:abyss:931711751702085672>')
fadingSoul = effect("Anéantissement",'fadingSoul', stat=HARMONIE,power=50,turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji='<:purification:931711772396777572>')
extermination = skill("Extermination",'svd',TYPE_INDIRECT_DAMAGE,500,effects=fadingSoul,group=SKILL_GROUP_HOLY,maxHpCost=15,cooldown=5,emoji='<:purification:931711772396777572>')
darkHeal = copy.deepcopy(lightHeal2)
darkHeal.name, darkHeal.id, darkHeal.emoji, darkHeal.condition = "Assombrissement", "svc", '<:darkHeal:931883636481982484>', [0,3,ELEMENT_DARKNESS]
matriceEff2 = copy.deepcopy(dmgUp)
matriceEff2.power = 25
matriceEff1 = effect("Matrice amplificatrice","matriceAmplEff",trigger=TRIGGER_ON_REMOVE,callOnTrigger=matriceEff2)
matriceEmpli = skill("Matrice amplificatrice",'svb',TYPE_BOOST,500,range=AREA_MONO,effects=matriceEff1,cooldown=7,description="Augmente de **{0}%** vos dégâts infligés lors de votre prochain tour".format(matriceEff2.power))
calestJump = skill("Plongeon Céleste",'sva',TYPE_DAMAGE,750,75,range=AREA_DIST_3,area=AREA_CIRCLE_1,tpCac=True,cooldown=5,emoji='<:ceslestJump:931899235270545469>')
lohicaUltLauch = skill("Brûme empoisonée","suz",TYPE_INDIRECT_DAMAGE,750,area=AREA_CONE_3,use=MAGIE,tpCac=True,effects=estial,cooldown=7,ultimate=True,emoji='<:brume:1058843224933933096>',description="Saute à côté de la cible et empoisonne les alentours",effPowerPurcent=int(65/estial.power*100))
lohicaUltCastEff = effect("Cast - Brûme empoisonée","lohicaUltCastEff",turnInit=2,silent=True,replique=lohicaUltLauch,emoji=uniqueEmoji('<a:lohicaUltCast:932823354841399296>'))
lohicaUltCast = copy.deepcopy(lohicaUltLauch)
lohicaUltCast.effectOnSelf, lohicaUltCast.effects, lohicaUltCast.tpCac = lohicaUltCastEff, [None], False
fairyFligth = skill("Envolée féérique",'suy',TYPE_DAMAGE,500,80,range=AREA_CIRCLE_1,jumpBack=1,knockback=3,cooldown=5,emoji='<:envolee:941677380181823489>')
aliceDanceEff = effect("Chant Dynamique",'aliceDanceEff', stat=CHARISMA,strength=5,magie=5,silentRemove=True)
aliceDanceEff2 = effect("Chant Dynamique (Effect)","corDynEff",callOnTrigger=aliceDanceEff,turnInit=3,area=AREA_DONUT_3,trigger=TRIGGER_START_OF_TURN,emoji=sameSpeciesEmoji('<:dyB:932618243280085062>','<:dyR:932618257960161331>'))
aliceDance = skill("Chant Dynamique","sc",TYPE_BOOST,500,range=AREA_MONO,area=aliceDanceEff2.area,effects=aliceDanceEff,effectOnSelf=aliceDanceEff2,emoji='<:dyna:932618114892439613>',use=CHARISMA,cooldown=7,description="Augmente les statistiques offensives des alliés autour de vous durant 3 tours")
auroreEff = effect("Aurore",'auroreEff', stat=CHARISMA,strength=5,magie=5,turnInit=3,emoji=sameSpeciesEmoji("<:aurB:934675375689170995>","<:aurR:934675360946212914>"))
aurore = skill('Aurore','sux',TYPE_BOOST,500,effects=auroreEff,replay=True,use=CHARISMA,cooldown=5,area=AREA_CIRCLE_1,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],emoji='<:aurore:934675235268087858>')
crepEff = effect("Crépuscule",'crepEff', stat=INTELLIGENCE,strength=-5,magie=-5,turnInit=3,emoji=sameSpeciesEmoji('<:crepB:934675391145201664>','<:crepR:934675411995074560>'))
crep = skill('Crépuscule','suw',TYPE_MALUS,500,effects=crepEff,use=INTELLIGENCE,replay=True,cooldown=5,area=AREA_CIRCLE_1,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS],emoji='<:crepuscule:934675249541292033>')
toMelee = skill('Corps à corps','suv',TYPE_DAMAGE,350,50,use=HARMONIE,tpCac=True,cooldown=3,emoji='<:cac:932765903102291999>',replay=True,range=AREA_CIRCLE_3,description="Saute au corps à corps de l'ennemi ciblé, lui inflige des dégâts et vous permet de rejouer votre tour")
toDistance = skill('Déplacement',toMelee.id,TYPE_DAMAGE,350,50,AREA_INLINE_2,use=HARMONIE,cooldown=3,jumpBack=2,emoji='<:dep:932765889017839636>',replay=True,description="Inflige des dégâts à l'ennemi ciblé, recule de deux cases et vous permet de rejouer votre tour")
bundleCaC = skill("Corps à corps / Déplacement",toMelee.id,TYPE_DAMAGE,350,become=[toMelee,toDistance],emoji=toMelee.emoji,description="{0} __{1} :__\n{2}\n\n{3} __{4} :__\n{5}".format(toMelee.emoji,toMelee.name,toMelee.description,toDistance.emoji,toDistance.name,toDistance.description))
engage = skill("Engagement",getAutoId(bundleCaC.id,True),TYPE_DAMAGE,350,50,AREA_CIRCLE_1,cooldown=3,emoji='<:engagement:1115723140933361865>',replay=True,description="Inflige des dégâts à l'ennemi ciblé et vous permet de rejouer votre tour")
autoBombRush = skill("Lance-Bombe Robot",'sut',TYPE_SUMMON,750,AREA_CIRCLE_4,ultimate=True,nbSummon=5,emoji='<:brAuto:933508393036029992>',invocation="Bombe Robot",cooldown=7,description="Invoque 3 Bombes Robots\nSeule la première Bombe Robot est soumise à la limitation d'invocation par équipe",shareCooldown=True)
killerWailUltimate = skill("Haut Perceur 5.1",'sus',TYPE_SUMMON,750,nbSummon=3,ultimate=True,cooldown=7,use=MAGIE,invocation='Haut-Perceur 5.1',emoji='<:killerWail:933516496196497439>',description='Invoque 3 Haut-Perceur 5.1.\nSeul le premier est soumis à la limitation d\'invocation par équipe',shareCooldown=True)
invocSeaker = skill("Invocation - Traqueur",'sur',TYPE_SUMMON,350,range=AREA_CIRCLE_3,cooldown=5,shareCooldown=True,invocation='Traqueur',emoji='<:seeker:933508405463777351>')
darkBoom = skill("Explosion Sombre",'darkBoom',TYPE_DAMAGE,500,85,cooldown=explosion.cooldown,percing=0,area=AREA_CIRCLE_2,effectOnSelf=explosion.effectOnSelf,accuracy=explosion.accuracy,setAoEDamage=True,repetition=2,ultimate=True,use=MAGIE,emoji='<a:db2:933676696899551273>',hpCost=30,group=SKILL_GROUP_DEMON,description="Inflige des dégâts dans une grande zone à deux reprises",damageOnArmor=0.8,url="https://media.discordapp.net/attachments/826608054468345866/1084893638812762162/20230313_183917.gif")
darkBoomCastEff = effect("Cast - Explosion Sombre",'castDarkBoom',turnInit=2,replique=darkBoom,emoji=sameSpeciesEmoji('<a:boomCastB:916382499704275005>','<a:boomCastR:916382515135144008>'),silent=True)
darkBoomCast = copy.deepcopy(darkBoom)
darkBoomCast.id, darkBoomCast.power, darkBoomCast.effectOnSelf, darkBoomCast.hpCost, darkBoomCast.url = 'suq', 0, darkBoomCastEff, 0, None
doubleShot = skill("Double Tir",'sup',TYPE_DAMAGE,500,60,repetition=2,condition=[EXCLUSIVE,ASPIRATION,OBSERVATEUR],emoji='<:doubleShot:933506156616368169>',cooldown=5)
harmShot = skill("Tir Harmonique",'suo',TYPE_DAMAGE,500,75,use=HARMONIE,condition=[EXCLUSIVE,ASPIRATION,TETE_BRULEE],cooldown=3,emoji='<:hamShot:933506175633330216>')
mageSkill = skill("Détonnation",'sun',TYPE_DAMAGE,500,80,condition=[EXCLUSIVE,ASPIRATION,MAGE],area=AREA_CIRCLE_1,setAoEDamage=True,cooldown=3,use=MAGIE,emoji='<:ice:941494417926270987>')
benitWater = skill("Eau bénite",'sum',TYPE_DAMAGE,500,75,area=AREA_CIRCLE_1,cooldown=3,maxHpCost=5,group=SKILL_GROUP_HOLY,use=MAGIE,emoji='<:holyStrike:931703468652118067>')
tempShare30, divShareEff2 = copy.deepcopy(shareTabl[5]), copy.deepcopy(absEff)
tempShare30.turnInit, divShareEff2.power, divShareEff2.turnInit = 3, 20, 3
shareSkill = skill("Partage divin",'sul',TYPE_HEAL,500,50,use=CHARISMA,maxHpCost=10,cooldown=5,effects=[tempShare30,divShareEff2],effBeforePow=True,description="Donne l'effet Partage à la cible tout en augmentant les soins reçus par cette dernière pendant 3 tours tout en la soignant",emoji='<:divineShare:949891460503855125>')
infraMedicaEff = effect("Extra Médica","extraMedica", stat=CHARISMA,power=35,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji="<:medica:911732802947530843>")
extraMedica = skill("Extra Medica",'suk',TYPE_HEAL,750,40,AREA_MONO,area=AREA_CIRCLE_2,use=CHARISMA,effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_CIRCLE_3,infraMedicaEff],cooldown=infraMedica.cooldown+2,group=SKILL_GROUP_HOLY,condition=[EXCLUSIVE,ASPIRATION,ALTRUISTE],description="Soigne les alliés proches et leur octroi un effet régénérant",maxHpCost=10,emoji='<:medica:911732802947530843>')
foulleeEff = effect("Foulée légère",'ppUniquePassifEff',emoji='<:quicky:934832147511017482>',turnInit=-1,unclearable=True,dodge=20,description="Augmente de **20%** votre probabilité d'esquiver des attaques")
foullee = skill("Foulée Légère",'suj',TYPE_PASSIVE,350,condition=[EXCLUSIVE,ASPIRATION,POIDS_PLUME],use=None,effectOnSelf=foulleeEff,emoji='<:quicky:934832147511017482>',quickDesc="Augmente vos chances d'esquiver une attaque")
lifePulseRegenEff = effect("Rénégénration","lifePulseHeal", stat=CHARISMA,power=20,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,turnInit=3,emoji='<:heal:911735386697519175>',description="Soigne le porteur en début de tour")
lifePulseFinal = skill("Pulsation Vitale",'sui',TYPE_HEAL,1000,110,range=AREA_MONO,ultimate=True,cooldown=10,initCooldown=3,area=AREA_CIRCLE_4,effects=lifePulseRegenEff,use=CHARISMA,emoji='<a:lifePulse:934968172107403324>',group=SKILL_GROUP_HOLY,maxHpCost=35,description="Soigne les alliés aux alentours et leur donne un effet de régénération sur la durée",url='https://cdn.discordapp.com/attachments/927195778517184534/934968488550871140/20220124_012750.gif')
lifePulseCastEff = effect("Cast - Pulsation Vitale",'lifePulseCast',replique=lifePulseFinal,silent=True,turnInit=2,emoji='<a:lifePulseCast:934968316882219068>')
lifePulseCast = copy.deepcopy(lifePulseFinal)
lifePulseCast.power, lifePulseCast.effectOnSelf, lifePulseCast.url, lifePulseCast.maxHpCost, lifePulseCast.effects= 0, lifePulseCastEff, None, 0, [None]
crimsomLotus = skill("Lotus Pourpre",'suh',TYPE_DAMAGE,750,220,emoji='<a:crimsomLotus:934980446176047104>',area=AREA_LINE_6,use=CHARISMA,accuracy=200,useActionStats=ACT_BOOST,description="Inflige des dégâts Charisme sur une ligne droite",cooldown=7,ultimate=True,url='https://cdn.discordapp.com/attachments/927195778517184534/934981029649874974/20220124_021239.gif',condition=[EXCLUSIVE,ASPIRATION,IDOLE])
crimsomLotusCastEff = effect("Cast - Lotus Pourpre",'crimstomLotusCastEff',turnInit=2,replique=crimsomLotus,silent=True,emoji=uniqueEmoji('<a:emoji_52:934980282577203210>'))
crimsomLotusCast = copy.deepcopy(crimsomLotus)
crimsomLotusCast.power, crimsomLotusCast.effectOnSelf, crimsomLotusCast.url = 0, crimsomLotusCastEff, None
abnegation = skill("Abnégation",'sug',TYPE_HEAL,750,200,emoji='<:abnegation:935538856286109726>',range=AREA_MONO,area=AREA_CIRCLE_5,group=SKILL_GROUP_DEMON,hpCost=90,ultimate=True,cooldown=7,use=CHARISMA,description="Soigne ou réanime vos alliés à portée au prix d'une grande quantité de PV",effectAroundCaster=[TYPE_RESURECTION,AREA_CIRCLE_5,150])
jumpedSplashDownLanding = copy.deepcopy(classicSplashdown)
jumpedSplashDownLanding.name, jumpedSplashDownLanding.range, jumpedSplashDownLanding.tpCac, jumpedSplashDownLanding.areaOnSelf, jumpedSplashDownLanding.url, jumpedSplashDownLanding.cooldown, jumpedSplashDownLanding.power = "Choc Chromatique Sauté", AREA_DIST_5, True, True, "https://cdn.discordapp.com/attachments/935769576808013837/935781564145623131/20220126_072054.gif", 7, jumpedSplashDownLanding.power - 20
jsdJumEff = effect("Cast - Choc Chromatique Sauté", 'JumpingSlashDownEff',turnInit=2,silent=True,emoji=classicSplashdown.emoji,untargetable=True,replique=jumpedSplashDownLanding)
jumpedSplashDown = copy.deepcopy(jumpedSplashDownLanding)
jumpedSplashDown.power, jumpedSplashDown.tpCac, jumpedSplashDown.url, jumpedSplashDown.effectOnSelf = 0, False, None, jsdJumEff
splashdown = skill("Choc Chromatique",classicSplashdown.id,TYPE_DAMAGE,750,ultimate=True,emoji=classicSplashdown.emoji,become=[classicSplashdown,jumpedSplashDown],area=AREA_CIRCLE_2)
pneumaArmor = effect("Pneuma",'pneumaArmor', stat=INTELLIGENCE,overhealth=50,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
pneuma = skill("Pneuma",'suf',TYPE_DAMAGE,750,125,condition=[EXCLUSIVE,ASPIRATION,PREVOYANT],ultimate=True,emoji='<:pneuma:936515231562219581>',url='https://media.discordapp.net/attachments/1130204608900386910/1131311294729945088/20230719_214640.gif',cooldown=7,area=AREA_LINE_3,accuracy=110,use=INTELLIGENCE,useActionStats=ACT_SHIELD,effectAroundCaster=[TYPE_ARMOR,AREA_CIRCLE_2,pneumaArmor])
absorbingStrike = skill("Frappe Convertissante",'sue',TYPE_DAMAGE,500,75,AREA_CIRCLE_2,cooldown=3,emoji='<:healStrike:936470624921075733>',lifeSteal=35)
absorbingArrow = skill("Flèche Convertissante",'sud',TYPE_DAMAGE,500,75,AREA_DIST_6,cooldown=3,emoji='<:healShot:936470641450815538>',lifeSteal=35)
absorbingStrike2 = skill("Frappe Convertissante Avancée",'suc',TYPE_DAMAGE,750,120,AREA_CIRCLE_2,cooldown=7,emoji='<:killStrike:936470659389849622>',lifeSteal=50,aoeLifeSteal=35)
absorbingArrow2 = skill("Flèche Convertissante Avancée",'sub',TYPE_DAMAGE,750,120,AREA_DIST_6,cooldown=7,emoji='<:killShot:936470681015709716>',lifeSteal=50,aoeLifeSteal=35)
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
expediantSpeedBoost = effect("Thèse des rafales hurlantes",'expediantSpeedBooost', stat=INTELLIGENCE,agility=10,emoji='<:expediant:937370418363367495>')
expediant = skill("Thèses fluidiques",'stx',TYPE_BOOST,750,range=AREA_MONO,area=AREA_CIRCLE_3,use=INTELLIGENCE,cooldown=7,url="https://media.discordapp.net/attachments/1130204608900386910/1131326190645420093/20230719_224517.gif",effects=[expediantDefenseUp,expediantSpeedBoost],emoji='<:expediant:937370418363367495>')
dinationEff = copy.deepcopy(dmgUp)
dinationEff.power, dinationEff.stat, dinationEff.turnInit = 4, INTELLIGENCE, 3
divination = skill("Divination",'stw',TYPE_BOOST,500,range=AREA_MONO,area=AREA_CIRCLE_3,use=INTELLIGENCE,cooldown=7,effects=dinationEff,emoji='<:divination:937370483777748993>')
macroCosmosEff = copy.deepcopy(dmgUp)
macroCosmosEff.power, macroCosmosEff.stat, macroCosmosEff.turnInit = 5, INTELLIGENCE, 3
macroCosmos = skill("Macro-cosmos",'stv',TYPE_DAMAGE,500,130,area=AREA_CIRCLE_2,effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_2,macroCosmosEff],cooldown=7,ultimate=True,use=INTELLIGENCE,useActionStats=ACT_BOOST,description="Inflige des dégâts aux ennemis et augmente les DI des alliés",emoji='<:macroCosmos:937370437573287997>')
tintabuleEff = effect("Tintinnabule",'tintabule', stat=CHARISMA,power=20,turnInit=3,lvl=5,type=TYPE_INDIRECT_HEAL,area=AREA_CIRCLE_2,emoji='<:tintabulbe:937370359257255976>',trigger=TRIGGER_AFTER_DAMAGE,description="Lors des 5 prochaines attaques subie par le porteur, soigne ce dernier et ses alliés dans la zone d'effet")
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

REAPEREFFDMGBUFF = 20
reaperEff = effect("Dessins de la Camarade", "that'sALongName", power=35, turnInit=5, type=TYPE_MALUS, emoji="<:longName:938167649106538556>",stackable=True,description="Augmente de **20%** les dégâts infligés par l'entité à l'origine de cet effect sur le porteur.\nSi le porteur est vaincu en ayant toujours l'effet sur lui (que ce soit de la main de l'initiateur de l'effet ou d'un autre), l'initiateur de l'effet se soigne de **{0}%** de ses PV maximums et sa Jauge d'Âme augmente de 5 pts supplémentaires")
deathShadow = skill("Ombre de la Mort","str",TYPE_DAMAGE,750,90,range=AREA_CIRCLE_2,emoji='<:deathShadow:937370374788755516>',effBeforePow=True,cooldown=7,effects=reaperEff,description="Inflige des dégâts et donne à la cible augmentant vos futurs dégâts à son encontre pendant plusieurs tours")
theEnd = skill("Dernier Voyage","stq",TYPE_DAMAGE,750,225,AREA_CIRCLE_3,cooldown=5,tpCac=True,ultimate=True,emoji='<a:lbReaper:938175619504689193>',damageOnArmor=1.35,description="Après un tour de chargement, délivre une puissante attaque à l'ennemi ciblé.\nSi cette dernière est sous un effet <:longName:938167649106538556> __Dessins de la Camarade__ dont vous êtes l'initiateur, la puissance de cette attaque augmente de **20%**",lifeSteal=25,url='https://cdn.discordapp.com/attachments/935769576808013837/938175773137862756/20220201_214401.gif')
theEndEff = copy.deepcopy(deepWound)
theEndEff.stat, theEndEff.power = theEnd.use, int(theEnd.power*0.3)
theEnd.effects=[theEndEff]
theEndCastEff = effect("Cast - Dernier Voyage","reaperLbCast",turnInit=2,silent=True,replique=theEnd,emoji='<a:lbReaperCast:938175259964747816>')
theEndCast = copy.deepcopy(theEnd)
theEndCast.power, theEndCast.url, theEndCast.effectOnSelf, theEndCast.tpCac, theEndCast.effects = 0, None, theEndCastEff, False, [None]
cure3Eff = effect("Extra Soins Préparé","cureIIready",turnInit=4,emoji='<:extraHeal:952522927214051348>')
cure2 = skill("Soins","stp",TYPE_HEAL,0,40,emoji='<:heal:911735386697519175>',effectOnSelf=cure3Eff,use=CHARISMA,rejectEffect=[cure3Eff])
cure3 = skill("Giga Soins","spt",TYPE_HEAL,0,55,emoji='<:extraHeal:952522927214051348>', needEffect=cure3Eff,cooldown=3,use=CHARISMA,area=AREA_CIRCLE_1)
cure2Bundle = skill("Giga Soins","stp",TYPE_HEAL,500,use=CHARISMA,become=[cure2,cure3],emoji='<:extraHeal:952522927214051348>',description="Permet d'utiliser les compétences {0} __{1}__ et {2} __{3}__.\n{2} __{3}__ ne peut être utilisé que si {0} __{1}__ a été utilisé préalablement".format(cure2.emoji,cure2.name,cure3.emoji,cure3.name))
assises = skill("Assises","sto",TYPE_DAMAGE,750,135,area=AREA_CIRCLE_1,use=CHARISMA,useActionStats=ACT_HEAL,cooldown=7,effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_2,65],condition=[EXCLUSIVE,ASPIRATION,ALTRUISTE],emoji='<:assise:941494380714414110>',description="Inflige des dégâts aux ennemis ciblés et soigne les alliés autour de vous")
debouses = skill("Debouses","stl",TYPE_HEAL,750,75,area=AREA_CIRCLE_1,use=CHARISMA,cooldown=7,useActionStats=ACT_HEAL,effectAroundCaster=[TYPE_DAMAGE,AREA_CIRCLE_2,75],condition=[EXCLUSIVE,ASPIRATION,VIGILANT],emoji='<:debouse:941494363748438027>',description="Soigne les alliés ciblés et inflige des dégâts autour de vous")
impactShield = effect("Armure Impactante",'impactArmor', stat=INTELLIGENCE,overhealth=50,emoji='<:impact:951379371489382400>',turnInit=3,stackable=True,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,description="Protège de quelques dégâts directs")
impact = skill("Frappe Impactante","stk",TYPE_DAMAGE,500,75,AREA_CIRCLE_3,condition=[EXCLUSIVE,ASPIRATION,PROTECTEUR],emoji='<:impact:941494342722412585>',effectOnSelf=impactShield,use=INTELLIGENCE,useActionStats=ACT_SHIELD,effectAroundCaster=[TYPE_HEAL,AREA_MONO,50],cooldown=3,description="En plus d'infliger quelques dégâts, cette compétence soigne et donne une petite armure au lanceur")
heartStoneSecEff = copy.deepcopy(defenseUp)
heartStoneSecEff.power, heartStoneSecEff.stat, heartStoneSecEff.turnInit = 5, INTELLIGENCE, 3
heartStoneSecEff2 = copy.deepcopy(heartStoneSecEff)
heartStoneSecEff2.turnInit = 1
heartStone = skill("Coeur de pierre","stj",TYPE_ARMOR,750,cooldown=3,emoji='<:earthStonr:941681433863421952>',effects=[impactShield, heartStoneSecEff, heartStoneSecEff2],condition=[EXCLUSIVE,ASPIRATION,PROTECTEUR],description="Confère une petite armure à l'allié ciblé et réduit ses dégâts reçus\nL'armure dure plus longtemps que la réduction de dégâts",replay=True)
erodStrikeEff = copy.deepcopy(deepWound)
erodStrikeEff.stat, erodStrikeEff.power = STRENGTH, 50
erodStrike = skill("Frappe érosive","sti",TYPE_DAMAGE,500,110,AREA_CIRCLE_3,cooldown=5,erosion=100,effects=[erodStrikeEff],emoji='<:ailillTwoStrike:1044490984572076142>',damageOnArmor=1.2)
genesis = skill("Génésis","sth",TYPE_DAMAGE,750,185,area=AREA_LINE_4,group=SKILL_GROUP_HOLY,use=MAGIE,maxHpCost=35,cooldown=7,emoji='<:genesis:946529693459419217>',ultimate=True)
invertion = skill("Inversion",'stg',TYPE_DAMAGE,500,90,group=SKILL_GROUP_DEMON,use=CHARISMA,useActionStats=ACT_HEAL,hpCost=15,cooldown=5,emoji='<:invertion:1228790737022357525>')
ice2Eff = effect("Détonnation avancée","ice2Eff", stat=MAGIE,power=60,area=AREA_CIRCLE_1,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji='<:ice2:941494399337136208>')
ice2 = skill("Détonnation Avancée","stf",TYPE_INDIRECT_DAMAGE,500,use=MAGIE,cooldown=3,emoji='<:ice2:941494399337136208>',condition=[EXCLUSIVE,ASPIRATION,SORCELER],effects=ice2Eff)
lifeWind = skill("Vent de vie","ste",TYPE_HEAL,500,60,AREA_MONO,condition=[EXCLUSIVE,ASPIRATION,VIGILANT],area=AREA_CIRCLE_2,use=CHARISMA,cooldown=5,emoji='<:divineWind:949888558355869747>')
renf2Eff1 = copy.deepcopy(defenseUp)
renf2Eff1.power, renf2Eff1.stat = 7.5, INTELLIGENCE
renf2Eff2 = copy.deepcopy(dmgUp)
renf2Eff2.power, renf2Eff2.stat = 7.5, INTELLIGENCE
renf2 = skill("Renforcement Avancé","std",TYPE_BOOST,750,condition=[EXCLUSIVE,ASPIRATION,INOVATEUR],effects=[renf2Eff2,renf2Eff1],cooldown=7,range=AREA_DONUT_5,emoji='<:renfAv:989529323063107605>')
entraide = skill("Entraide","stc",TYPE_HEAL,500,50,range=AREA_MONO,area=AREA_DONUT_7,cooldown=5,group=SKILL_GROUP_DEMON,hpCost=10,use=CHARISMA,emoji='<:entraide:941677392722808913>')
perfectShot = skill("Tir Parfait","stb",TYPE_DAMAGE,750,170,cooldown=7,ultimate=True,emoji='<:tirParfait:961187760134311996>')
lastRessource = skill("Dernier recours","sta",TYPE_RESURECTION,500,135,cooldown=7,shareCooldown=True,use=STRENGTH,initCooldown=5,emoji='<:strengthRaise:949890176195383318>')
strengthOfDesepearance = skill("Force du désespoir","ssz",TYPE_RESURECTION,500,135,cooldown=7,shareCooldown=True,use=MAGIE,initCooldown=5,emoji='<:magicRaise:949890198190305300>')
nova = skill("Nova","ssy",TYPE_DAMAGE,500,115,use=INTELLIGENCE,useActionStats=ACT_SHIELD,emoji='<:wtfIsThatAlready:1023615143063601283>',hpCost=5,cooldown=5,group=SKILL_GROUP_DEMON)
undeadEff2 = effect("Mort en sursie","undeadEff2",turnInit=-1,description="Augmente vos soins et vol de vies reçus mais vous inflige des dégâts indirects équivalents à 30% de vos PV Maximums en fin de tour",emoji='<a:undead:953259661568663602>',silent=False,power=30,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN)
undeadEff = effect("Mort-Vivant","undead",turnInit=20,callOnTrigger=undeadEff2,power=100,description="1 fois par combats, en recevant des dégâts mortels, le porteur est soigné de l'intégralité de ses PV mais subis l'effet {0} __{1}__, lui infligeant des dégâts à la fin de son tour".format(undeadEff2.emoji[0][0],undeadEff2.name),emoji='<:undead:944989590836637736>',silent=False,lvl=1)
undead = skill("Mort Vivant","ssx",TYPE_PASSIVE,500,effectOnSelf=undeadEff,emoji='<:undead:944989590836637736>',group=SKILL_GROUP_DEMON,description=undeadEff.description)
ironStormDmgBoost = copy.deepcopy(dmgUp)
ironStormDmgBoost.power, ironStormDmgBoost.turnInit = 10, 3
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
extraVerVent = skill("Extra VerVent","sss",TYPE_DAMAGE,power=80,area=AREA_CIRCLE_1,use=MAGIE,effectOnSelf=extraVerFoudreReady,emoji='<:extraVerVent:946042871176396871>',rejectEffect=[extraVerFoudreReady,verBrasierReady])
extraVerFoudre = skill("Extra VerFoudre","sss",TYPE_DAMAGE,power=85,area=AREA_CIRCLE_1,use=MAGIE,needEffect=extraVerFoudreReady,effectOnSelf=verBrasierReady,emoji='<:extraVerFoudre:946042839287091300>')
verBrasier = skill("VerBrasier",'sss',TYPE_DAMAGE,power=120,area=AREA_CIRCLE_1,emoji='<:verBrasier:946042912511250522>',cooldown=3,use=MAGIE,needEffect=verBrasierReady)
comboVerBrasier = skill("Combo VerBrasier",'sss',TYPE_DAMAGE,500,power=verBrasier.power,emoji=verBrasier.emoji,become=[extraVerVent,extraVerFoudre,verBrasier],use=MAGIE,description="Permet d'effectuer l'enchaînement __Extra VerVent__, __Extra VerFoudre__ et __Ver Miracle__.\nLes compétences doivent être utilisée dans l'odre précédament énoncé")
phoenixFlight = effect("Vol du phénix","phoenixFlight", stat=MAGIE,power=25,turnInit=3,stackable=True,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji='<:phenixFlight:1066023587305234484>',description="Soigne le porteur en début de tour")
galvanisation = skill("Galvanisation",'ssr',TYPE_DAMAGE,750,emoji='<:galvaPheonix:946042576413290506>',area=AREA_CIRCLE_1,power=120,use=MAGIE,effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_CIRCLE_2,phoenixFlight],cooldown=7,description="Inflige des dégâts aux ennemis ciblés et donne un effet régénérant aux alliés autour de vous\n\n{0} __{1}__ :\nSoigne le porteur avec une puissance de **{2}** en utilisant la statistique de magie pendant 3 tours".format(phoenixFlight.emoji[0][0],phoenixFlight.name,phoenixFlight.power))
contreDeSixte = skill("Contre de Sixte",'ssq',TYPE_DAMAGE,350,75,area=AREA_CIRCLE_1,cooldown=3,emoji='<:contreDeSixte:946042932643913788>')
selenShield = effect("Armure sélènomantique","selenArmor", stat=INTELLIGENCE,overhealth=40,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
selenomancie = skill("Sélènomancie","ssp",TYPE_ARMOR,500,range=AREA_MONO,area=AREA_CIRCLE_2,effects=selenShield,cooldown=5,condition=[EXCLUSIVE,ASPIRATION,PROTECTEUR],use=INTELLIGENCE,emoji='<:selenomancie:949888629721927730>')
helioRegen = effect("Régénération hélomancique","helioRegen", stat=CHARISMA,power=25,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN)
holiomancie = skill("Héliomancie",'sso',TYPE_INDIRECT_HEAL,500,effects=helioRegen,use=CHARISMA,area=AREA_CIRCLE_2,range=AREA_MONO,cooldown=5,condition=[EXCLUSIVE,ASPIRATION,VIGILANT],emoji='<:heliomancie:949888728116133889>')
partnerIn = effect("Position raprochée","partE",turnInit=-1,unclearable=True,description="En rélisant une compétence de Boost utilisable uniquement sur soi même, la zone d'effet de cette compétence est répliquée sur le porteur de <:partB:949074187513905172> __Partenaire de Position Rapprochée__.\n\nLes alliés se trouvant uniquement dans cette deuxième air d'effet bénificie du bonus de la compétence avec des bonus équivalants à **{0} %** de l'effet de base",power=35,emoji='<:partA:949074204333047809>')
partnerOut = effect("Partenaire de position rapprochée","partS",turnInit=-1,unclearable=True,description="Tant que le porteur est en état de se battre, permet d'étendre les zones d'effets de certaines compétences de l'entité à l'origine de cet effet",emoji='<:partB:949074187513905172>')
partner = skill("Position Raprochée","ssn",TYPE_PASSIVE,750,effectOnSelf=partnerIn,effects=partnerOut,emoji='<:partnaire:949075450360123482>',description="Vous confère l'effet {0} __{1}__ et donne l'effet {2} __{3}__ à un autre allié aléatoire au début du combat".format(partnerIn.emoji[0][0],partnerIn.name,partnerOut.emoji[0][0],partnerOut.name),quickDesc="Etend la porté de vos compétences de boost en les répliquants sur un allié")
exhibitionnisme = skill("Exhibitionnisme","ssm",TYPE_MALUS,69,range=AREA_MONO,area=AREA_CIRCLE_5,cooldown=7,effects=unHolly.effects[0],group=SKILL_GROUP_DEMON,use=CHARISMA,hpCost=20,emoji='<:exhibitionnisme:949893142402990120>',effPowerPurcent=80)
invocTitania = skill("Invocation - Titania","ssl",TYPE_SUMMON,750,invocation="Titania",ultimate=True,cooldown=10,emoji='<:smnTitania:950210129276579871>',shareCooldown=True,url='https://cdn.discordapp.com/attachments/927195778517184534/932704180731265054/20220117_193200.gif')
demonBloodEff = effect("Sang de Démon","demonBloodEff", stat=CHARISMA,strength=12,magie=12,endurance=5,turnInit=3)
dmonBlood = skill("Sang de Démon","ssk",TYPE_BOOST,500,emoji='<:dmonBlood:950256044322459649>',range=AREA_MONO,area=AREA_CIRCLE_4,effects=demonBloodEff,hpCost=15,cooldown=7,group=SKILL_GROUP_DEMON,description="Augmente la Force, la Magie et l'Endurance des alliés affectés pendant 3 tours")
hollyGround = skill("Terre Sacrée","ssj",TYPE_DEPL,750,emoji='<:holyGroundI:950254446611431455>',range=AREA_CIRCLE_2,cooldown=7,maxHpCost=15,group=SKILL_GROUP_HOLY,depl=holyGroundI,description="Pose un déployable qui réduit les dégâts reçus et augmente les dégâts infligés par les alliés dans la zone d'effet")
hollyGround2 = skill("Terre Sacrée Étendue","ssi",TYPE_DEPL,750,emoji='<:holyGroundII:950254462449115136>',range=AREA_CIRCLE_2,cooldown=7,group=SKILL_GROUP_HOLY,description="Pose un déployable qui augmente les statistiques des alliés dans la zone d'effet et les soigne",maxHpCost=15,depl=holyGroundII)
burningGround = skill("Terre Démoniaque","ssh",TYPE_DEPL,750,emoji='<:burningGround:950256060923535370>',range=AREA_CIRCLE_2,cooldown=7,hpCost=25,depl=dmonGround,group=SKILL_GROUP_DEMON,description="Pose un déployable qui augmente les dégâts infligés et les statistiques par les alliés dans la zone d'effet")
blueShell = skill("Carapace à épines","ssg",TYPE_DAMAGE,500,100,AREA_CIRCLE_7,area=AREA_CIRCLE_1,emoji='<:blue:950231849337233448>',cooldown=7,description="Inflige de dégâts en zone sur l'ennemi ayant réalisé le plus de dégâts")
nanoHealEff1, nanoHealEff2 = copy.deepcopy(dmgUp), copy.deepcopy(defenseUp)
nanoHealEff1.power = nanoHealEff2.power = 5
nanoHealEff1.turnInit = nanoHealEff2.turnInit = 3
nanoHealEff1.stat = nanoHealEff2.stat = CHARISMA
nanoHeal = skill("Nano-Heal","ssf",TYPE_HEAL,500,power=cure.power,cooldown=7,effects=[nanoHealEff1, nanoHealEff2],range=AREA_DONUT_5,emoji='<:nanoBoost:1223601259244687432>',use=CHARISMA,description="Soigne l'allié ciblé tout en augmentant les dégâts qu'il inflige et réduisant les dégâts qu'il subit durant un petit moment")
ironHealthEff1, ironHealthEff2 = copy.deepcopy(constEff), copy.deepcopy(absEff)
ironHealthEff1.power, ironHealthEff1.turnInit, ironHealthEff1.stat, ironHealthEff1.unclearable  = 15, -1, PURCENTAGE, True
ironHealthEff2.power, ironHealthEff2.turnInit, ironHealthEff2.unclearable = ironHealthEff1.power, ironHealthEff1.turnInit, True
ironHealth = skill("Santé de Fer","sse",TYPE_PASSIVE,500,effects=[ironHealthEff1,ironHealthEff2],emoji='<:ironHealth:951692715727409253>',description="Augmente vos PVs maximums et les soins et armures reçus de **15%**")
windBurn = effect("Morsure du vent","windBurn", stat=AGILITY,power=30,turnInit=5,lvl=5,stackable=True,area=AREA_DONUT_1,emoji='<:windBite:961185646993637476>',trigger=TRIGGER_END_OF_TURN,description="Inflige des dégâts magiques aux ennemis aux corps à corps du porteur à la fin du tour de celui-ci",type=TYPE_INDIRECT_DAMAGE)
windBal = skill("Balleyage éventé",'ssd',TYPE_DAMAGE,500,85,range=AREA_CIRCLE_1,use=AGILITY,emoji='<:windBite:961185646993637476>',cooldown=7,effectAroundCaster=[TYPE_DAMAGE,AREA_CIRCLE_1,50],effectOnSelf=windBurn,description="Inflige des dégâts à l'ennemi ciblé, puis aux ennemis à votre corps à coprs tout en vous octroyant un effet infligeant passivement des dégâts aux ennemis à votre corps à corps",condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR])
brasier2Eff = effect("Brûlure","brasier2Eff", stat=MAGIE,power=25,turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE)
brasier2 = skill("Brasier Avancé","ssc",TYPE_DAMAGE,500,75,range=AREA_DIST_5,area=AREA_CIRCLE_2,use=MAGIE,emoji='<:brasier3:961185593482682398>',effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_CIRCLE_2,brasier2Eff],setAoEDamage=True,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],cooldown=5,ultimate=True,description="Inflige des dégâts aux ennemis dans la zone d'effet toute en infligeant un effet de dégâts sur la durée aux ennemis proche de vous\n__Puissance (Brûlure) :__ **{0}** ({1} tours)".format(brasier2Eff.power, brasier2Eff.turnInit))
earthUlt2Shield = effect("Armure Tellurique","earthUlt2Shield", stat=ENDURANCE,emoji='<:liuArmor:922292960886915103>',overhealth=50,turnInit=3,trigger=TRIGGER_DAMAGE,type=TYPE_DAMAGE,inkResistance=10)
earthUlt2Lanch = skill("Fureur Tellurique","ssb",TYPE_DAMAGE,750,150,emoji='<:furTellu:951700536732823622>',range=AREA_MONO,area=AREA_CIRCLE_1,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],use=ENDURANCE,setAoEDamage=True,effectOnSelf=earthUlt2Shield,description="Inflige des dégâts aux ennemis à votre corps à corps et vous octrois une armure réduisant également les dégâts indirects reçus",ultimate=True,cooldown=7)
earthUlt2CastEff = effect("Cast - {0}".format(earthUlt2Lanch.name),"castEarthUlt2",turnInit=2,silent=True,replique=earthUlt2Lanch)
earthUlt2 = copy.deepcopy(earthUlt2Lanch)
earthUlt2.power, earthUlt2.effectOnSelf = 0, earthUlt2CastEff
geyser = skill("Geyser","ssa",TYPE_DAMAGE,500,75,area=AREA_CIRCLE_1,emoji='<:geyser:961185615859290163>',cooldown=5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],use=MAGIE)
rouletteEff = effect("Pile ou Face","pileouface",dmgUp = -50, critDmgUp= 100,turnInit=2,description="Augmente vos dégâts critiques infligés de **100%**, mais réduit vos dégâts non critiques de **50%**")
rouletteSkill = skill("Pile ou face","srz",TYPE_BOOST,350,range=AREA_MONO,cooldown=5,effects=rouletteEff,description="Lors de votre prochain tour, les dégâts critiques sont doublés, mais réduits de moitié sinon",emoji='<a:rotativeYPositiveCoin:917927342918221865>')
constEffI = effect("Tir Constant","const1Eff",dmgUp=10,emoji=sameSpeciesEmoji('<:cst:951692626506178620>','<:ctsR:951692410155569172>'),turnInit=3)
constEffII = effect("Tir Critique","const2Eff",emoji=sameSpeciesEmoji('<:cstCrit:951692598182027314>','<:cstCritR:951692193045835816>'),critDmgUp=10,turnInit=3)
constShot = skill("Tir Constant","sry",TYPE_DAMAGE,500,power=100,effectOnSelf=constEffI, cooldown=5, effBeforePow=True,emoji=constEffI.emoji[0][0],description="Augmente vos dégâts non critiques et inflige des dégâts à l'ennemi ciblé")
const2Shot = skill("Tir Critique","srx",TYPE_DAMAGE,500,power=90,effectOnSelf=constEffII, cooldown=5, effBeforePow=True,emoji=constEffII.emoji[0][0],description="Augmente vos dégâts critiques et inflige des dégâts critiques à l'ennemi ciblé",garCrit=True)
revelEff = copy.deepcopy(defenseUp)
revelEff.power, revelEff.stat, revelEff.turnInit = divination.effects[0].power, INTELLIGENCE, 3
revelation = skill("Révélation","srw",TYPE_BOOST,divination.price,effects=revelEff,cooldown=divination.cooldown,emoji=divination.emoji,range=AREA_MONO,area=AREA_CIRCLE_2)
elemEff = effect("Energie multiélémentaire","elemEff",turnInit=4,stackable=True,description="Cet effet devient un effet élémentaire correspondant à votre élément, augmentant de **{0}%** la puissance de vos compétences exclusives à votre élément\nCertaines compétences peuvent consommer les effets élémentaires pour obtenir des propriétés supplémentaires",power=5,emoji=elemEmojis[ELEMENT_UNIVERSALIS_PREMO])
elemEffName = ["Neutralité","Flamme intérieure","Courrant interne","Tempête intérieur","Minéralisation","Lueur interne","Ombre interne","Poussière cosmique","Seconde temporelle","Illuminae"]
mEP = 35
matriseElemEff = effect("Maîtrise élémentaire","maitriseElemPas",turnInit=-1,unclearable=True,description="Vous octroit **{0}%** de chance d'obtenir l'effet {1} __{2}__ lorsque vous utilisez une compétence élémentaire".format(mEP,elemEff.emoji[0][0],elemEff.name),emoji='<:catDefault:956599837128802324>',callOnTrigger=elemEff)
maitriseElementaire = skill("Maîtrise élémentaire","srv",TYPE_PASSIVE,effectOnSelf=matriseElemEff,emoji='<:catDefault:956599837128802324>',price=500,quickDesc="Vous octrois une chance d'obtenir un effet élémentaire en utilisant une compétence élémentaire")
magicEffGiver = skill("Concentration élémentaire","sru",TYPE_DAMAGE,500,100,effectOnSelf=elemEff,emoji='<:elemStrike:953217204629950484>',description="Inflige des dégâts à l'ennemi ciblé et vous octroit l'effet élémentaire correspondant à votre élément",cooldown=5,use=MAGIE)
physEffGiver = skill("Convertion élémentaire","srt",TYPE_DAMAGE,500,100,effectOnSelf=elemEff,emoji='<:elemSpell:953217184795078697>',description="Inflige des dégâts à l'ennemi ciblé et vous octroit l'effet élémentaire correspondant à votre élément",cooldown=5)
danceFas = skill("Danse de la Lame Fascinatoire","srs",TYPE_DAMAGE,500,power=125,maxPower=150,area=AREA_CIRCLE_2,use=STRENGTH,cooldown=5,emoji="<:sworddance:894544710952173609>",jaugeEff=eventFas,minJaugeValue=50,maxJaugeValue=100)
corGraEff = effect("Chant Grâcieux","chorGra", stat=CHARISMA,charisma=5,intelligence=5,endurance=5,silentRemove=True,emoji=sameSpeciesEmoji('<:graceB:956700633531043933>','<:graceR:956700653785346149>'),description="Augmente les statistiques de support du porteur")
corGraEff2 = effect("Chant Grâcieux (Effet)","corGracEff2",area=AREA_DONUT_3,turnInit=3,callOnTrigger=corGraEff,trigger=TRIGGER_START_OF_TURN,emoji=sameSpeciesEmoji('<:graceB:956700633531043933>','<:graceR:956700653785346149>'))
corGra = skill("Chant Grâcieux","srq",TYPE_BOOST,500,range=AREA_MONO,area=corGraEff2.area,effects=corGraEff,cooldown=aliceDance.cooldown,effectOnSelf=corGraEff2,emoji='<:corGra:956700501095899217>',description="Augmente les statistiques de support de vos alliés proches durant 3 tours")
rosePink = effect("Rose rose","finFloRose",turnInit=-1,emoji='<:roseRose:956716583915491378>',stackable=True)
roseBlue = effect("Rose azurée","finFloBlu",turnInit=-1,emoji='<:roseBlue:956716604333367326>',stackable=True)
roseGreen = effect("Rose verte","finFloGre",turnInit=-1,emoji='<:roseGreen:956716536742150254>',stackable=True)
roseRed = effect("Rose rouge","finFloRed",turnInit=-1,emoji='<:roseRed:956716516232032257>',stackable=True)
roseYellow = effect("Rose jaune","finFloYel",turnInit=-1,emoji='<:roseYellow:956716561136242748>',stackable=True)
roseDarkBlu = effect("Rose bleue","finFloDBlue",turnInit=-1,emoji='<:roseDBlue:956725613585133598>',stackable=True)
finFloLaunchBase = skill("Final Floral","finFlo",TYPE_BOOST,use=CHARISMA,emoji='<:finFlor:956715059772538981>',range=AREA_MONO,area=AREA_CIRCLE_4)
finFloCast = effect("Cast - Final Floral","castFinFlo",turnInit=2,emoji=finFloLaunchBase.emoji,replique=finFloLaunchBase)
finFloEff = effect("Final Floral","finFloEffPas",turnInit=-1,unclearable=True,emoji=sameSpeciesEmoji('<:finalFloralB:956715210549362748>','<:finalFloralR:956715234842791937>'),description="Vous avez la compétence <:finFlor:956715059772538981> __Final Floral__ d'équipé")

finFloEffList = [copy.deepcopy(dmgUp),copy.deepcopy(defenseUp),effect("Critique Floral",'finFloCrit', stat=CHARISMA,critical=7,emoji=finFloEff.emoji),effect("Aura Florale","finFloHeal", stat=CHARISMA,power=20,turnInit=3,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji=finFloEff.emoji,area=AREA_CIRCLE_2)]
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
lightElemUseEff = effect("Armure de lumière","lightArmorElemUse", stat=INTELLIGENCE,overhealth=75,turnInit=3,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR)
lightElemUse = skill("Lumière Protectrice","srj",TYPE_ARMOR,500,range=AREA_MONO,area=AREA_CIRCLE_3,effects=lightElemUseEff,cooldown=7,ultimate=True,emoji='<:catLight:956599774461722655>',description="Consomme vos effets {0} __{1}__\nDonne une armure à vous et vos alliés alentours.\nSi au moins un effet {0} __{1}__ a été consommé, octroie un effet de soins sur la durée avec une puissance de **30%** de celle de l'armure. La durée de l'effet dépend du nombre d'effets consommés".format(tablElemEff[5].emoji[0][0],tablElemEff[5].name),condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],use=INTELLIGENCE)
darkElemUse = skill("Brasier des Ténèbres","sri",TYPE_DAMAGE,500,135,area=AREA_CIRCLE_2,ultimate=True,cooldown=7,use=MAGIE,emoji='<:catDark:950942244523872256>',description="Consomme vos effets {0} __{1}__\nInflige des dégâts aux ennemis dans la zone d'effet\nSi au moins un {0} __{1}__ a été consommé, donne également un effet de dégâts indirects à l'ennemi ciblé infligeant **50%** de dégâts supplémentaires à la fin de son tour à lui et ses alliés proches dont la durée dépend du nombre d'effets consommés".format(tablElemEff[6].emoji[0][0],tablElemEff[6].name),condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS])
spaceElemUse = skill("Déluge Céleste","srh",TYPE_DAMAGE,500,135,area=AREA_CIRCLE_2,ultimate=True,cooldown=7,use=MAGIE,emoji='<:catSpace:956599795110277150>',description="Consomme vos effets {0} __{1}__\nInflige des dégâts aux ennemis dans la zone d'effet\nPour chaque effet {0} __{1}__ consommé, inflige des dégâts supplémentaires équivalents à **33%** des dégâts de base à un ennemi aléatoire dans la zone d'effet et ses alliés aux corps à corps".format(tablElemEff[7].emoji[0][0],tablElemEff[7].name),condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE])
timeElemUse = skill("Déphasage Temporel","srg",TYPE_HEAL,500,100,area=AREA_CIRCLE_2,ultimate=True,cooldown=7,use=CHARISMA,emoji='<:catTime:956599814898999328>',description="Consomme vos effets {0} __{1}__\nSoigne les alliés dans la zone d'effet.\nSi au moins un effet {0} __{1}__ a été consommé, octroi également une armure aux alliés dans la zone d'effet dont la puissance équivant à **20%** de celle des soins. La puissance est multipliée par le nombre d'effets consommés".format(tablElemEff[8].emoji[0][0],tablElemEff[8].name),condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME])
bleedingConvert = skill("Taillade des veines","srf",TYPE_DAMAGE,500,80,useActionStats=ACT_INDIRECT,range=AREA_CIRCLE_3,cooldown=7,lifeSteal=50,emoji="<:shiLifeSteal:960007047984857148>",percing=50,description="Inflige des dégâts à la cible et vole une partie des dégâts infligés tout en ignorant une partie de la résistance de la cible\nConsomme tous les effets <:bleeding:1133258052225745048> __Hémorragie__ présents sur la cible pour augmenter la puissance de cette compétence")

elemShieldEff = effect("Armure élémentaire","elemShield", stat=INTELLIGENCE,overhealth=40,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,description="Une armure qui protège de quelques dégâts direct.",emoji=sameSpeciesEmoji('<:elemShield:960061614739050537>','<:elemShield:960061540164313088>'))
elemShield = skill("Armure élémentaire","srd",TYPE_ARMOR,500,effects=[elemShieldEff,elemEff],cooldown=7,emoji='<:elemShield:960061614739050537>',description="Octroi une armure à l'allié ciblé ainsi qu'un effet élementaire de son élément")
shieldAuraShield = effect("Armure","armorAuraArmor", stat=INTELLIGENCE,overhealth=20,type=TYPE_ARMOR,decateOnTurn=True,trigger=TRIGGER_DAMAGE,description="Protège de quelques dégâts directs")
shieldAuraEff = effect("Aura armurière","shieldAuraEff", stat=INTELLIGENCE,callOnTrigger=shieldAuraShield,emoji=sameSpeciesEmoji('<:armorAura:960060538119929927>','<:armorAura:960060634517602344>'),lvl=3,area=AREA_CIRCLE_2,trigger=TRIGGER_END_OF_TURN,turnInit=3,description="À la fin du tour du porteur, ocrtoi une armure à celui-ci et ses alliés aux alentours")
shieldAura = skill("Aura Armurière","src",TYPE_ARMOR,500,cooldown=7,effects=shieldAuraEff,emoji='<:armorAura:960060538119929927>',description="Pose une aura sur l'allié ciblé, qui octroira de l'armure autour de lui quand il terminera son tour pendant 3 tours")
horoscope = skill("Horoscope","srb",TYPE_BOOST,emoji='<:horoscope:960312586371477524>',description="Consomme tous vos signes astrologiques pour augmenter les statistiques de vos alliés durant 3 tours\nLes statistiques augmentées dépendent des signes astrologiques conssommés\nVous obtenez un signe astrologique aléatoire en fin de tour",cooldown=3,initCooldown=3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE],use=INTELLIGENCE,range=AREA_MONO, area=AREA_CIRCLE_5)
ShiHemophilie = effect("Anti-Coagulant","increaseBlooding",description="Augmente de **{0}%** les dégâts subis par l'effet <:bleeding:1133258052225745048> __Hémorragie__",power=35,emoji='<:hemophillie:960721463772610613>')
ShiUltimateLauch = skill("Percée ensanglantée","sra",TYPE_DAMAGE,750,200,AREA_CIRCLE_2,effects=[bleeding,ShiHemophilie],useActionStats=ACT_INDIRECT,emoji='<:shiUlt:960760921666510908>',description="Après 1 tour de chargement, inflige de lourd dégâts à l'ennemi ciblé, lui applique <:bleeding:1133258052225745048> __Hémorragie__ et augmente les dégâts de <:bleeding:1133258052225745048> __Hémorragie__ durant 1 tour",ultimate=True,cooldown=7)
ShiUltimateCast = effect("Cast - {0}".format(ShiUltimateLauch.name),"shiUltCast",turnInit=2,silent=True,replique=ShiUltimateLauch,emoji='<a:shiUltCast:960764930217377802>')
ShiUltimate = copy.deepcopy(ShiUltimateLauch)
ShiUltimate.effects, ShiUltimate.power, ShiUltimate.effectOnSelf = [None], 0, ShiUltimateCast

intraEff = effect("Vulnérabilité Indirecte","traqnardEff",inkResistance=-15,turnInit=3,type=TYPE_MALUS,description="Augmente les dégâts indirects reçus par le porteur")
intaveneuse = skill("Intraveineuse",'sqz',TYPE_INDIRECT_DAMAGE,500,effects=[estial,intraEff],effPowerPurcent=int(35/estial.power*100),cooldown=5,emoji='<:intraveineuse:963390544770367488>',use=MAGIE)
decolation = skill("Colation","sqy",TYPE_DAMAGE,effects=ShiUltimateLauch.effects,useActionStats=ACT_INDIRECT,effPowerPurcent=60,cooldown=5,power=80,lifeSteal=100,emoji='<:collation:963390564655579156>',price=500)
dephaIncantEff = effect("Déphasage Incantatoire","dephaIncant", stat=MAGIE,power=80,area=AREA_CIRCLE_1,trigger=TRIGGER_ON_REMOVE,emoji='<:dephaInc:980450895785521242>',type=TYPE_INDIRECT_DAMAGE,description="Inflige des dégâts lors du début du prochain tour de l'entité à l'origine de l'effet")
dephaIncant = skill("Déphasage incantatoire","sqx",TYPE_INDIRECT_DAMAGE,500,effects=dephaIncantEff,cooldown=5,emoji='<:dephaInc:980450895785521242>',description="Place l'effet {effIcon} __{effName}__ sur la cible. Au début de votre prochain tour, l'effet explosera en blessant le porteur et ses alliés proches",condition=[EXCLUSIVE,ASPIRATION,SORCELER])

coroWind = effect("Corruptus sanguis","coroWind", stat=MAGIE,power=30,turnInit=3,stackable=True,lvl=3,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji='<:corruptusSanguis:1050065948599660595>',description="Un vent empoisonné qui fait des dégâts à la fin du tour du porteur.\nPossède une légère odeur de sang")
bloodJauge = effect("Jauge de Sang","bloodJauge",turnInit=-1,unclearable=True,emoji='<:bloodJauge:1050111058314018936>')
bloodJauge.jaugeValue = jaugeValue(
    emoji = [["<:BJLeftEmpty:900473865459875911>","<:BJMidEmpty:900473889539366994>","<:BJRightEmpty:900473909856587847>"],["<:BJLeftFull:900473987564441651>","<:BJMidFull:900474021781569604>","<:BJRightFull:900474036042215515>"]],
    conds = [
        jaugeConds(INC_START_TURN,5),
        jaugeConds(INC_DEAL_DAMAGE,5/100),
        jaugeConds(INC_ENEMY_DAMAGED,5/100),
        jaugeConds(INC_ALLY_DAMAGED,5/100)
    ]
)

cwFocus = skill("Incarnatus Puff","sqw",TYPE_INDIRECT_DAMAGE,500,cooldown=focal.cooldown-2,effects=coroWind,effPowerPurcent=int(50/coroWind.power*100),effectOnSelf=coroWind,description="Donne un puissant effet {effIcon} __{effName}__  à l'ennemi ciblé, mais en subissez un également",emoji='<:IncPuf:968327189508542484>',jaugeEff=bloodJauge,minJaugeValue=20,maxJaugeValue=35)
propaUltLaunch = skill("Propagation Avancée","sqv",TYPE_INDIRECT_DAMAGE,750,range=AREA_MONO,emoji='<:probagUlt:1058851761680551987>',area=AREA_ALL_ENEMIES,ultimate=True,cooldown=7,effects=estial,effPowerPurcent=int(40/estial.power*100),description="Après un tour de chargement, inflige <:est:884223390804766740> __Poison d'Estialba__ à tous les ennemis avec **125%** de sa puissance",use=MAGIE)
propaUltCastEff = effect("Cast - {replicaName}","propaUltCastEff",turnInit=2,silent=True,replique=propaUltLaunch,emoji='<a:propagUltCast:1058849678470434828>')
propaUlt = copy.deepcopy(propaUltLaunch)
propaUlt.effects, propaUlt.effectOnSelf, propaUlt.description = [None], propaUltCastEff, None
cwUlt = skill("Ultima Exitium","squ",TYPE_INDIRECT_DAMAGE,750,ultimate=True,cooldown=5,emoji='<:sanguisExaltium:1115283194950996089>',effects=coroWind,power=70,effPowerPurcent=int(70/coroWind.power*100),description="Inflige l'effet {effIcon} __{effName}__ à la cible, puis inflige immédiatement des dégâts indirects en fonction du nombre d'effets de Dégâts Indirects ainsi que leur durée restante présents sur la cible\nLes effets autres que {effIcon} __{effName}__ augmentent un peu plus la puissance de l'attaque mais sont consommés par cette dernière",jaugeEff=bloodJauge,minJaugeValue=25,maxJaugeValue=50,maxPower=75)
sanguisGladio = skill("Sanguis Gladio","sqt",TYPE_DAMAGE,500,80,cooldown=3,effects=coroWind,use=MAGIE,emoji='<:sgladio:968478994724950056>',effPowerPurcent=int(40/coroWind.power*100),jaugeEff=bloodJauge,minJaugeValue=15,maxJaugeValue=25,maxPower=110)
sanguisGladio2 = skill("Sanguis Gladio Avancée","sqs",TYPE_DAMAGE,750,100,cooldown=5,area=AREA_LINE_2,effects=coroWind,effPowerPurcent=int(40/coroWind.power*100),use=MAGIE,emoji='<:sgladio2:968479144293855252>',jaugeEff=bloodJauge,minJaugeValue=15,maxJaugeValue=25,maxPower=135)
cardiChoc = skill("Choc Cardinal","sqr",TYPE_DAMAGE,500,100,range=AREA_MONO,area=AREA_INLINE_3,accuracy=120,cooldown=5,description="Inflige des dégâts aux ennemis prochent allignés avec vous avec une précision importante",emoji='<:chocCardi:989536077117276250>')
chiStrike = skill("Frappe de Chi","sqq",TYPE_DAMAGE,500,80,range=AREA_CIRCLE_1,area=AREA_LINE_3,accuracy=120,cooldown=5,setAoEDamage=True,garCrit=True,description="Inflige des dégâts aux ennemis allignés avec la cible, en infligeant forcément un coup critique à cette dernière. Ignore aussi également une partie de la résistance adverse",percing=20,emoji='<:chiStrike:1164901504566706237>')
kralamSkillEff2 = effect("Prévention","nono", stat=INTELLIGENCE,overhealth=75,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,turnInit=3,emoji='<:prevention:1170999486684864573>')
kralamSkillEff1 = effect("Prévention (effet)","squaez", stat=INTELLIGENCE,trigger=TRIGGER_HP_UNDER_50,callOnTrigger=kralamSkillEff2,lvl=1,turnInit=3,emoji='<:resisUp:1170999443861020742>',type=TYPE_BOOST,resistance=5)
kralamSkill = skill("Prévention","vn",TYPE_BOOST,0,AREA_DONUT_6,cooldown=5,effects=kralamSkillEff1,emoji=kralamSkillEff2.emoji[0][0],description="Augmente les résistances de la cible. Si celle-ci passe en dessous de 50% de ses PV Max, le bonus devient une armure")
krystalisationEff = effect("Cristalisation","krysArmor", stat=ENDURANCE,overhealth=65,inkResistance=12.5,turnInit=3,emoji='<:cristalisation:989540878953619506>',type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
krystalEff3 = copy.deepcopy(krystalisationEff)
krystalEff3.overhealth, krystalEff3.inkResistance = krystalEff3.overhealth*0.4, krystalEff3.inkResistance*0.4
krystalisation = skill("Cristalisation","sqp",TYPE_ARMOR,500,range=AREA_MONO,effects=[krystalisationEff],effectAroundCaster=[TYPE_ARMOR,AREA_DONUT_2,krystalEff3],cooldown=7,emoji='<:cristalisation:989540878953619506>',description="Vous octrois une armure, les dégâts indirects subis et réplique cet effet dans une moindre mesure autour de vous",condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH])
regenVigilEff = effect("Régénération vigilante","vigilRegen", stat=CHARISMA,power=35,turnInit=5,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_END_OF_TURN)
regenVigil = skill("Régénération Vigilante","sqo",TYPE_HEAL,750,35,AREA_DONUT_4,condition=[EXCLUSIVE,ASPIRATION,VIGILANT],cooldown=7,emoji='<:regenVigil:980450876265218109>',effects=regenVigilEff,effectOnSelf=regenVigilEff,description="Soigne l'allié ciblé et procure à ce dernier et vous même un effet de soin sur la durée")
fragmentationEff = effect("Fragmentation","fragEff", stat=PURCENTAGE,type=TYPE_MALUS,resistance=-40)
fragmEff2 = copy.deepcopy(armorGetMalus)
fragmEff2.power, fragmEff2.turnInit = 20, 3
fragmentation = skill("Fragmentation","sqn",TYPE_DAMAGE,500,90,AREA_CIRCLE_4,cooldown=5,damageOnArmor=3,emoji='<:fragmentation:1065854021979607051>',effects=[fragmentationEff,fragmEff2],effBeforePow=True,condition=[EXCLUSIVE,ASPIRATION,TETE_BRULEE],description="Réduit la résistance et l'armure reçus de la cible et lui inflige un attaque aux dégâts augmentés contre l'armure")
morsTempette = effect("Morsure de la Tempette","morsTempette", stat=STRENGTH,power=30,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,stackable=True,turnInit=5,lvl=5,emoji='<:morsTemp:971788828278943776>')
morsCaudique = effect("Morsure Caudique","morsCaudique", stat=INTELLIGENCE,power=40,trigger=TRIGGER_END_OF_TURN,stackable=True,type=TYPE_INDIRECT_DAMAGE,turnInit=5,lvl=5,emoji='<:morsCaudique:971788772289163274>')
machDeFer = skill("Mâchoire de Fer","sqm",TYPE_DAMAGE,500,condition=[EXCLUSIVE,ASPIRATION,ATTENTIF],power=100,useActionStats=ACT_INDIRECT,effects=[morsTempette,morsCaudique],cooldown=7,emoji='<:machFer:971787963795124235>',effPowerPurcent=125)
lanceToxEff = effect("Toxines","toxi", stat=STRENGTH,power=20,emoji='<:lanceTox:971789592145580103>',stackable=True,turnInit=5,lvl=5,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE)
lanceTox = skill("Lance-Toxines","sql",TYPE_INDIRECT_DAMAGE,500,area=AREA_CONE_3,effects=lanceToxEff,emoji='<:lanceTox:971789592145580103>',effPowerPurcent=125,cooldown=5,condition=[EXCLUSIVE,ASPIRATION,ATTENTIF])
gigaFoudreEff = effect("Giga Foudre","gigaFoudre", stat=MAGIE,power=20,emoji='<:gigaFoudre:971789611087036487>',stackable=True,turnInit=5,lvl=5,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN)
gigaFoudre = skill("Giga Foudre","sqk",TYPE_INDIRECT_DAMAGE,500,area=AREA_CIRCLE_1,effects=gigaFoudreEff,emoji='<:gigaFoudre:971789611087036487>',cooldown=5,condition=[EXCLUSIVE,ASPIRATION,SORCELER])
trickAttackEff = copy.deepcopy(vulne)
trickAttackEff.power, trickAttackEff.turnInit = 15, 3
trickAttack = skill("Attaque Sournoise","sqj",TYPE_DAMAGE,500,50,effects=trickAttackEff,cooldown=5,emoji='<:trickAttack:971788242284343336>',description="Inflige des dégâts à l'adversaire sublié puis augmente les dégâts qu'il reçoit de **10%** jusqu'à votre prochain tour")
aurore2Eff = effect("Aurore II","aur2Eff",type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,power=20,stat=CHARISMA,turnInit=3,emoji='<:aurore:971787846639841310>')
aurore2 = skill("Aurore II","sqh",TYPE_INDIRECT_HEAL,500,effects=aurore2Eff,cooldown=5,emoji='<:aurore:971787846639841310>',condition=[EXCLUSIVE,ASPIRATION,VIGILANT])
holyShieltronEff1 = effect("Sheltron Sacré","holyShieltron1",block=100,emoji='<:shieltron:971787905758560267>')
holyShieltronEff2 = effect("Bénédiction du Paladin","holyShieltron2", stat=CHARISMA,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,power=20,turnInit=3,emoji='<:bene:1005850393747673171>')
holyShieltron = skill("Sheltron Sacré","sqg",TYPE_BOOST,500,range=AREA_MONO,effects=[holyShieltronEff2,holyShieltronEff1],emoji=holyShieltronEff1.emoji[0][0],condition=[EXCLUSIVE,ASPIRATION,VIGILANT],group=SKILL_GROUP_HOLY,maxHpCost=5,cooldown=5,description="Vous octroi 100% de blocage ainsi qu'une petite régénération sur la durée")
KeracholeRegen = effect("Kerachole","keracholeRegen", stat=INTELLIGENCE,power=15,turnInit=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji='<:kerachole:971787391058722847>')
KeracholeReduc = copy.deepcopy(defenseUp)
KeracholeReduc.power, KeracholeReduc.stat, KeracholeReduc.turnInit = 3.5, INTELLIGENCE, 3
kerachole = skill("Kerachole","sqf",TYPE_BOOST,500,effects=[KeracholeReduc,KeracholeRegen],emoji='<:kerachole:971787391058722847>',cooldown=7,range=AREA_MONO,area=AREA_CIRCLE_2,description="Réduit les dégâts subis par vous et vos allié proches tout en vous octroyanr un effet de régénération sur la durée")
morsTempSkill = skill("Morsure de la Tempette","sqe",TYPE_DAMAGE,350,power=75,useActionStats=ACT_INDIRECT,effects=morsTempette,cooldown=5,condition=[EXCLUSIVE,ASPIRATION,ATTENTIF],emoji=morsTempette.emoji[0][0])
morsCaudiqueSkill = skill("Morsure Caudique","sqd",TYPE_DAMAGE,350,power=75,useActionStats=ACT_INDIRECT,effects=morsCaudique,cooldown=5,condition=[EXCLUSIVE,ASPIRATION,ATTENTIF],emoji=morsCaudique.emoji[0][0])
combEff = effect("Combustion","combustion", stat=MAGIE,power=15,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_1,turnInit=-1,lvl=99,emoji='<:fireKitsune:917670925904785408>')
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
firstArmorEff, firstArmorEff2 = effect("Armure préliminaire","armurepreliminaire", stat=INTELLIGENCE,overhealth=65,inkResistance=10,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji("<:prelimB:981607841070739506>","<:prelimR:981607818442473492>")), copy.deepcopy(absEff)
firstArmorEff2.power = 20
firstArmor = skill("Armure préliminaire","spx",TYPE_ARMOR,500,cooldown=7,effects=[firstArmorEff,firstArmorEff2],emoji='<:prelimB:981607841070739506>',description="Octroi une puissante armure à l'allié ciblé, réduisant également les dégâts indirects qu'il reçoit tant qu'elle est active, et augmente également les soins qu'il reçoit de 20%")
refLum = skill("Lueur réfléchissante","spv",TYPE_HEAL,500,50,area=AREA_CIRCLE_1,cooldown=5,effectOnSelf=tablElemEff[ELEMENT_LIGHT],condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],description="Soigne les alliés dans la zone d'effet et vous octroi un effet élémentaire")
refConc = skill("Lueur Concentrique","spu",TYPE_HEAL,500,70,cooldown=5,effectOnSelf=tablElemEff[ELEMENT_LIGHT],condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],emoji='<:lueurConcen:1177705418655543347>',description="Soigne l'allié ciblé et vous octroi un effet élémentaire")

petalisEff = effect("Pétalisation","petalEff", stat=CHARISMA,endurance=5,block=15,inkResistance=5,turnInit=5,description="Les statistiques défensives sont augmentées",emoji=sameSpeciesEmoji('<:petB:979448518345359451>','<:petR:979448539446911016>'))
petalisation = skill("Pétalisation","spt",TYPE_BOOST,500,effects=petalisEff,range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=5,emoji='<:petR:979448539446911016>',description="Augmente l'endurance et le blocage des alliés alentours durant 5 tours")
roseeHealEff = effect("Rosée matinale","roseedumatin", stat=CHARISMA,agility=5,intelligence=3,charisma=3,type=TYPE_BOOST,turnInit=3,emoji=petalisEff.emoji)
roseeHeal = skill("Rosée matinale","sps",TYPE_BOOST,500,range=AREA_MONO,area=AREA_CIRCLE_3,cooldown=5,emoji='<:rosee:1119132836709007470>',effects=roseeHealEff,effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_2,50],description="Augmente l'agilité, le charisme et l'intelligence des alliés à portée tout en les soignants un peu")
floraisonFinalEff = copy.deepcopy(onstageeff) 
floraisonFinalEff = effect("Floraison finale","floraisonFinale", stat=CHARISMA, strength=int(onstageeff.strength*0.7), endurance=int(onstageeff.endurance*0.7), charisma=int(onstageeff.charisma*0.7), agility=int(onstageeff.agility*0.7), precision=int(onstageeff.precision*0.7), intelligence=int(onstageeff.intelligence*0.7), magie=int(onstageeff.magie*0.7),turnInit=onstageeff.turnInit+2,emoji=sameSpeciesEmoji('<:florFinB:979450403890548786>','<:florFinR:979450384244432896>'))
floraisonFinale = copy.deepcopy(onstage)
floraisonFinale.effects, floraisonFinale.name, floraisonFinale.id, floraisonFinale.emoji, floraisonFinale.url = [floraisonFinalEff], "Floraison Finale", "spr", '<:florFinR:979450384244432896>', "https://media.discordapp.net/attachments/826608054468345866/1119162147990163547/20230616_091003.gif"
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
    corGra.emoji,corGra.name,
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
krasisEff.power, krasisEff.stat, krasisEff.turnInit = 20, INTELLIGENCE, 3
krasisEff2 = effect("Krasis","krasisEff", stat=INTELLIGENCE,inkResistance=10, turnInit=krasisEff.turnInit)
krasis = skill("Krasis","spf",TYPE_BOOST,500,effects=[krasisEff,krasisEff2],cooldown=5,replay=True,description="Augmente de **{0}%** les soins reçus par la cible, réduit les dégâts indirects qu'elle reçoit durant **{1}** tours et vous permet de rejouer votre tour".format(krasisEff.power,krasisEff.turnInit),emoji='<:krasis:982359813742800947>')

dosisSkill = skill("Dosis","spe",TYPE_DAMAGE,power=75,cooldown=3,use=INTELLIGENCE,useActionStats=ACT_SHIELD,emoji='<:dosis:1229489041515352174>',description="Inflige des dégâts à l'ennemi ciblé")
dosisEukraEff = effect("Dosis Eucratique","dosisEukratique",INTELLIGENCE,power=40,turnInit=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji='<:dosisEucra:1229489020174860421>',stackable=True)
dosisEucraSkill = skill(dosisEukraEff.name,dosisSkill.id,TYPE_INDIRECT_DAMAGE,effects=dosisEukraEff,cooldown=5,emoji=dosisEukraEff.emoji[0][0],description="Inflige un effet de dégâts indirects à l'ennemi ciblé")
dosisBundle = skill("Eucrosis ",dosisSkill.id,TYPE_DAMAGE,become=[dosisSkill,dosisEucraSkill],description="Vous permet d'utiliser {0}, une compétence de dégâts utilisant votre Intelligence et votre statistique d'armure, ou bien {1}, une compétence de dégâts indirecte utilisant votre Intelligence, pour infliger plus de dégâts avec un temps de rechargement augmenté".format(dosisSkill,dosisEucraSkill),emoji=dosisSkill.emoji,price=500,use=INTELLIGENCE,useActionStats=ACT_SHIELD)

gravitonEff = effect("Gravité","GravitonEff",agility=-5,precision=-3,emoji='<:graviton:982316403078078464>',type=TYPE_MALUS,stat=ENDURANCE)
graviton = skill("Graviton","spd",TYPE_MALUS,350,range=AREA_MONO,area=AREA_INLINE_5,effects=gravitonEff,pull=5,cooldown=5,emoji='<:graviton:982316403078078464>',description="Réduit l'agilité et la précision des ennemis à porté et les attirent sur vous")
temperanceEff1, temperanceEff2 = copy.deepcopy(healDoneBonus), copy.deepcopy(defenseUp)
temperanceEff1.power, temperanceEff2.power, temperanceEff2.stats, temperanceEff2.turnInit, temperanceEff1.turnInit = 20, 7, CHARISMA, 3, 3
temperance = skill("Tempérance","spc",TYPE_BOOST,750,effects=temperanceEff2,effectOnSelf=temperanceEff1,range=AREA_MONO,area=AREA_DONUT_4,cooldown=7,description="Réduit les dégâts subis par les alliés alentours tout en augmentant votre quantité de soins réalisés",emoji='<:temperance:982349348992081960>')
teracholeEff = copy.deepcopy(defenseUp)
teracholeEff.power, teracholeEff.stat = 10, CHARISMA
terachole = skill("Terachole","spb",TYPE_HEAL,price=500,power=60,effects=teracholeEff,cooldown=5,emoji='<:terachole:982349368864698428>',description="Soigne l'allié ciblé tout en réduisant les dégâts qu'il subit pendant un tour")
aquavoileEff = copy.deepcopy(defenseUp)
aquavoileEff.power, aquavoileEff.stat, aquavoileEff.turnInit = 10, CHARISMA, 1
aquavoile = skill("Aquavoile","spa",TYPE_BOOST,350,effects=aquavoileEff,cooldown=5,emoji='<:aquavoile:982349320835727400>',replay=True)
misery = skill("Offrande de Misère","soz",TYPE_DAMAGE,750,120,area=AREA_CIRCLE_1,use=CHARISMA,useActionStats=ACT_HEAL,cooldown=7,emoji='<:misery:982359796239966238>')
tangoEndEff = effect("Tango Endiablé","tango", stat=CHARISMA,critical=5,critDmgUp=15,turnInit=3,description="Augmente le taux de critique et les dégâts critiques infligés pendant 3 tours\nSi cet effet est octroyé grace à __Position Rapprochée__, sa puissance n'en est pas réduite",emoji='<:tango:982359831518277772>')
tangoEnd = skill('Tango Endiablé',"soy",TYPE_BOOST,price=500,area=AREA_CIRCLE_1,range=AREA_MONO,emoji='<:tango:982359831518277772>',cooldown=7,effects=tangoEndEff)
danseStarFall = skill("Danse de la pluie étoilée","sox",TYPE_DAMAGE,750,150,area=AREA_LINE_4,effBeforePow=True,garCrit=True,effectOnSelf=tangoEndEff,cooldown=7,description="Inflige des dégâts en ligne droite puis augmente votre taux de critique et vos dégâts critiques pour vos deux prochains tours",ultimate=True,emoji='<:pluieEtoile:982359861679521833>')
graviton2 = skill("Gravi som'Mont","sow",TYPE_DAMAGE,500,range=AREA_MONO,area=AREA_INLINE_5,use=ENDURANCE,knockback=5,power=50,cooldown=5,emoji='<:graviton:982316403078078464>',description="Inflige des dégâts aux ennemis dans la zone d'effet et les repousses")
invocAutTour = skill("Invocation - Auto tourelle Tour","sov",TYPE_SUMMON,500,range=AREA_CIRCLE_4,invocation="Auto tourelle Tour",cooldown=5,emoji='<:autoTowB:982946185247588372>',description="Invoque une Auto tourelle Tour, une invocation de dégâts à longue portée",use=PRECISION,shareCooldown=True)
invocAutFou = skill("Invocation - Auto tourelle Fou","sou",TYPE_SUMMON,500,range=AREA_CIRCLE_4,invocation="Auto tourelle Fou",emoji='<:autoFouR:982946204046462987>',cooldown=5,description="Invoque une Auto tourelle Fou, une invocation de soutien",use=INTELLIGENCE,shareCooldown=True)
invocAutQueen = skill("Invocation - Auto tourelle Reine","sot",TYPE_SUMMON,750,range=AREA_CIRCLE_4,invocation="Auto tourelle Reine",emoji='<:autoQueenB:982946221599641610>',cooldown=7,description="Invoque une Auto tourelle Reine, une invocation dedégâts de mêlée",use=STRENGTH,shareCooldown=True)

jetLagDmgEff = effect("Déphasage temporel","jetLagDmgEff",power=1,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,stackable=True,emoji=sameSpeciesEmoji("<:jetLagB:984520122150555728>","<:jetLagR:984520139745689600>"))
jetLagEff = effect("Déphasage Intemporel","jetLagEff",power=50,emoji=sameSpeciesEmoji("<:jetLagB:984519444082610227>","<:jetLagR:984519461111472228>"),turnInit=3,type=TYPE_MALUS,description="**{0}%** des dégâts directs infligés par le porteur sont convertis en dégâts indirects en fin de tour sur la cible")
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

divineCircleEff = effect("Cercle Sacré","divineCircleEff", stat=MAGIE,magie=10,turnInit=3,emoji='<:divineCercle:989532178109042698>')
divineCircle = skill("Cercle Sacré",getAutoId(elemRuneSkill[-1].id,True),TYPE_BOOST,500,effects=divineCircleEff,area=AREA_CIRCLE_3,cooldown=5,maxHpCost=10,emoji='<:divineCercle:989532178109042698>')
divineWayEff = effect("Guide Divin","divineGuide", stat=CHARISMA,strength=12,magie=12,turnInit=3)
divineGuid = skill("Guide Divin",getAutoId(divineCircle.id,True),TYPE_BOOST,price=500,effects=divineWayEff,cooldown=5,maxHpCost=7,group=SKILL_GROUP_HOLY)
THEALNEEDEDFORUBER, TINDHNEEDFORUBER = 3000, 5000
uberJauge = effect("Jauge de soins","uberJauge",turnInit=-1,emoji=statsEmojis[ACT_HEAL_FULL],unclearable=True)

uberJauge.jaugeValue = jaugeValue(
    emoji=[["<:lej:980923743960461412>","<:mej:980923762016927764>","<:rej:980923786650075228>"],["<:ftlj:980930222679543918>","<:ftrj:980930256032641074>","<:ftmj:980930239901343834>"]],
    conds=[
        jaugeConds(INC_START_TURN,5),
        jaugeConds(INC_DEAL_HEALING,40/100),
        jaugeConds(INC_LIFE_STEAL,30/100)
    ]
)

uberImune = effect("Übercharge","uberImune",emoji='<:ubc:985647422556495913>',immunity=True)
uberCharge = skill("Übercharge",getAutoId(divineGuid.id,True),TYPE_HEAL,750,75,emoji='<:ubc:985647422556495913>',jaugeEff=uberJauge,cooldown=5,description="Consomme votre ÜberJauge pour soigner l'allié ciblé.\nPlus la ÜberJauge était remplie, plus les soins seront puissants, jusqu'à **+100%**\n\nOctroi également un effet de réduction de dégâts à la cible.\nPlus la ÜberJauge était remplie, plus la réduction de dégâts sera élevée, jusqu'à **75%**\nSi la ÜberJauge était pleine, rend la cible **Immunisée** à la place",maxPower=125,minJaugeValue=20,maxJaugeValue=100)

bloodBathEff = copy.deepcopy(vampirismeEff)
bloodBathEff.stat, bloodBathEff.power = STRENGTH, 15
bloodBath = skill("Bain de Sang",getAutoId(uberCharge.id,True),TYPE_DAMAGE,500,75,range=AREA_MONO,area=AREA_CIRCLE_2,effectOnSelf=bloodBathEff,effBeforePow=True,cooldown=7,condition=[EXCLUSIVE,ASPIRATION,BERSERK],emoji='<:bloodbath:986614852082626570>',description="Vous octroi __Vampirisme__ pendant 2 tours et effectue une attaque sur les ennemis proches")
erodAoeEff = copy.deepcopy(aconstEff)
erodAoeEff.power, erodAoeEff.turnInit = 20, 3
erodAoe = skill("Erosion Avancée",getAutoId(bloodBath.id,True),TYPE_DAMAGE,500,80,AREA_CIRCLE_2,area=AREA_CONE_2,effects=erodAoeEff,condition=[EXCLUSIVE,ASPIRATION,TETE_BRULEE],cooldown=5,erosion=150,emoji='<:eros:986614877076488202>',description="Inflige des dégâts aux ennemis ciblés en réduisant leurs PVmax, et réduit temporairement ceux de l'ennemi ciblé une nouvelle fois")
divineAbneEff = copy.deepcopy(dmgUp)
divineAbneEff.turnInit, divineAbneEff.power, divineAbneEff.unclearable = -1, 25, True
divineAbne = skill("Abnégation Divine",getAutoId(erodAoe.id,True),TYPE_PASSIVE,use=None,emoji='<:abdiv:987022697991139358>',price=500,effectOnSelf=divineAbneEff,group=SKILL_GROUP_HOLY,power=35,description="Augmente vos dégâts infligés de **25%** durant tout le combat mais réduits vos PV maximums de **35%**",quickDesc="Augmente vos dégâts innfligés mais réduit vos PV maximum")
astrodynEff = effect("Astrodynamie","astrodyn", stat=CHARISMA,strength=3,magie=3,agility=1,precision=1,emoji='<:astro:986614953047912499>',description="Augmente les statistiques offensives du porteur")
astrodyn = skill("Astrodynamie",getAutoId(divineAbne.id,True),TYPE_BOOST,750,effects=astrodynEff,url="https://media.discordapp.net/attachments/1006418796329848954/1007574359403151450/20220812_105137.gif",range=AREA_MONO,area=AREA_CIRCLE_3,emoji='<:astro:986614953047912499>',description='Augmente les statistiques des alliés proches et réduit le temps de rechargement de votre Transcendance de 3 tours',cooldown=7,condition=[EXCLUSIVE,ASPIRATION,IDOLE])
cercleConEff = copy.deepcopy(dmgUp)
cercleConEff.power, cercleConEff.stat = 2.5, INTELLIGENCE
cercleCon = skill("Cercle de Connaissance",getAutoId(astrodyn.id,True),TYPE_BOOST,750,range=AREA_MONO,area=AREA_CIRCLE_3,effects=cercleConEff,url='https://media.discordapp.net/attachments/1003025632415973510/1007612026220204062/20220812_132824.gif',emoji='<:arcCircle:986615034627113040>',cooldown=7,description="Augmente les dégâts infligés par vos alliés proches et réduit le temps de rechargement de votre Transcendance de 3 tours",condition=[EXCLUSIVE,ASPIRATION,INOVATEUR])
aliceFanDanse2Eff = effect("Galvanisation de l'éventail","aliceFanDanseBuff", stat=CHARISMA,strength=7,magie=7,endurance=5,charisma=5,intelligence=5,turnInit=3)
aliceFanDanse2 = skill("Chorégraphie de l'éventail",getAutoId(cercleCon.id,True),TYPE_DAMAGE,500,power=110,range=AREA_MONO,area=AREA_CIRCLE_5,setAoEDamage=True,cooldown=5,effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_4,aliceFanDanse2Eff],description="Effectue une chorégraphie de l'éventail durant 3 tours, infligeant des dégâts croissants aux ennemis autour de vous. Au dernier tour, la compétence a plus de portée et augmente la force, magie et endurance et alliés alentours",emoji='<:fanDance:986987567557775490>')
aliceFanDanse2Cast = effect(aliceFanDanse2.name,"aliceFanDanse2Cast",turnInit=2,silent=True,replique=aliceFanDanse2,emoji=aliceFanDanse2.emoji)
aliceFanDanse1 = skill("Chorégraphie de l'éventail",aliceFanDanse2.id,TYPE_DAMAGE,500,power=100,range=AREA_MONO,area=AREA_CIRCLE_3,setAoEDamage=True,cooldown=6,effectOnSelf=aliceFanDanse2Cast,description="Effectue une chorégraphie de l'éventail durant 3 tours, infligeant des dégâts croissants aux ennemis autour de vous. Au dernier tour, la compétence a plus de portée et augmente la force, magie et endurance et alliés alentours",emoji='<:fanDance:986987567557775490>')
aliceFanDanse1Cast = effect(aliceFanDanse2.name,"aliceFanDanse1Cast",turnInit=2,silent=True,replique=aliceFanDanse1,emoji=aliceFanDanse2.emoji)
aliceFanDanse = skill("Chorégraphie de l'éventail",aliceFanDanse2.id,TYPE_DAMAGE,500,power=90,range=AREA_MONO,area=AREA_CIRCLE_3,setAoEDamage=True,cooldown=5,effectOnSelf=aliceFanDanse1Cast,description="Effectue une chorégraphie de l'éventail durant 3 tours, infligeant des dégâts croissants aux ennemis autour de vous. Au dernier tour, la compétence a plus de portée et augmente la force, magie et endurance et alliés alentours",emoji='<:fanDance:986987567557775490>')
plumeCel = skill("Plumes Célestes",getAutoId(aliceFanDanse.id,True),TYPE_DAMAGE,500,power=120,area=AREA_CIRCLE_2,range=AREA_DIST_6,cooldown=7,emoji='<:plumeCel:989539461224337432>')
plumePers = skill("Plumes Perçantes",getAutoId(plumeCel.id,True),TYPE_DAMAGE,500,power=100,garCrit=True,range=AREA_DIST_4,area=AREA_LINE_3,percing=35,cooldown=5,emoji='<:plumePers:989539480375525408>',description="Inflige des dégâts aux ennemis ciblés. Inflige également {0} {1} à la cible principale".format(deepWound.emoji[0][0],deepWound.name))
pousAviaire = skill("Poussée Aviaire",getAutoId(plumePers.id,True),TYPE_DAMAGE,500,power=100,range=AREA_CIRCLE_3,area=AREA_CONE_2,knockback=1,jumpBack=1,cooldown=5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],emoji='<:birdPush:989537549838090310>')
demonRegenEff = effect("Régénération Démonique","demonRegen", stat=CHARISMA,power=50,turnInit=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji='<:regenDem:989529378885107782>')
demonRegen = skill("Régénération Démoniaque",getAutoId(pousAviaire.id,True),TYPE_INDIRECT_HEAL,500,effects=demonRegenEff,hpCost=20,group=SKILL_GROUP_DEMON,cooldown=7,emoji='<:regenDem:989529378885107782>')
demonDmgBuff = copy.deepcopy(dmgUp)
demonDmgBuff.stat, demonDmgBuff.power, demonDmgBuff.turnInit = INTELLIGENCE, 10, 3
demonLink = skill("Union Démoniaque",getAutoId(demonRegen.id,True),TYPE_BOOST,500,effects=demonDmgBuff,area=AREA_CIRCLE_1,hpCost=25)

bloodBath2 = skill("Bain de Sang Avancé",getAutoId(demonLink.id,True),TYPE_DAMAGE,0,135,range=AREA_CIRCLE_2,cooldown=7,condition=[EXCLUSIVE,ASPIRATION,BERSERK],emoji=bloodBath.emoji,effectOnSelf=bloodBathEff,effBeforePow=True)
altyCoverEff2 = effect("Couverture","altyCoverEff2",redirection=100,trigger=TRIGGER_DAMAGE,emoji='<:altyCover:988767335974326272>')
altyCoverEff1 = effect("Régénération compréhensive","altyCoverEff1", stat=CHARISMA,power=22,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji='<:AltyRegen:994748551932428319>')
altyCover = skill("Couverture Compréhensive",getAutoId(bloodBath2.id,True),TYPE_INDIRECT_HEAL,emoji='<:altyCover:988767335974326272>',effects=[altyCoverEff1,altyCoverEff2],range=AREA_DONUT_5,initCooldown=3,cooldown=7,description="Redirige l'intégralité des dégâts directs reçus par un allié sur vous pendant 1 tour tout en lui octroyant un effet de régénération pendant 3 tours")
klikliStrike = skill("Frappe Vangeresse",getAutoId(altyCover.id,True),TYPE_DAMAGE,power=95,maxPower=200,range=AREA_CIRCLE_3,emoji='<:klikliStrike:994743803514732664>',cooldown=7,effectOnSelf=holmgangEff,effBeforePow=True,effects=chained,description="Consomme la quasi totalité de vos PVs pour infliger des dégâts à l'ennemi ciblé\nPlus votre pourcentage de PV était élevé, plus l'attaque sera puissance\nVous octroi également Holmgang et entrave les déplacements de l'ennemi ciblé")
gwenyStrike = skill("Impact Justicier",getAutoId(klikliStrike.id,True),TYPE_DAMAGE,power=50,maxPower=150,range=AREA_MONO,emoji='<:gwenyStrike:994747468182978663>',area=AREA_CIRCLE_2,selfEffPurcent=35,cooldown=7,effectOnSelf=holmgangEff,effectAroundCaster=[TYPE_MALUS,AREA_DONUT_1,chained],effBeforePow=True,description="Consomme la quasi totalité de vos PVs pour infliger des dégâts aux ennemis alentours\nPlus votre pourcentage de PV était élevé, plus l'attaque sera puissance\nVous octroi également Holmgang et entrave les déplacements des ennemis aux corps à corps", minTargetRequired=3)

plumRemEff2 = copy.deepcopy(deepWound)
plumRemEff2.stat, plumRemEff2.power = STRENGTH, 35
plumRemEff = effect("Plumes Rémanantes","plumRemEff", stat=STRENGTH,power=35,area=AREA_CIRCLE_1,turnInit=7,type=TYPE_DAMAGE,emoji="<:plumeRem:989543669839319102>",stackable=True, callOnTrigger=plumRemEff2,trigger=TRIGGER_ON_REMOVE)
plumRemEff.iaPow = 25
plumRem = skill("Plumes Rémanantes",getAutoId(gwenyStrike.id,True),TYPE_DAMAGE,750,50,AREA_DIST_7,initCooldown=3,cooldown=5,area=AREA_CIRCLE_3,emoji="<:plumeRem:989543669839319102>",description="Vos compétences {0} __{1}__, {2} __{3}__, {4} __{5}__ et {6} __{7}__ ont désormais **40%** de chance d'infliger l'effet {8} __{9}__ aux cibles affectées.\nVotre arme <:plume:871893045296128030> __Plumes Perçantes__ octroi désormais l'effet {8} __{9}__ à la place d'Incurable.\n\nLors de l'utilisation de cette compétence, tous les effets {8} __{9}__ présents sur les ennemis dans la zone d'effet infligent des dégâts dans une zone Cercle 1 avec une puissance de **{10}** (Dégâts Directs)".format(hinaUlt.emoji,hinaUlt.name,plumeCel.emoji,plumeCel.name,plumePers.emoji,plumePers.name,pousAviaire.emoji,pousAviaire.name,plumRemEff.emoji[0][0],plumRemEff.name,plumRemEff.power*1.5))

plumePers.effects=[plumRemEff2]

raisingPheonixFlight = copy.deepcopy(phoenixFlight)
raisingPheonixFlight.power, raisingPheonixFlight.name = raisingPheonixFlight.power // 2, raisingPheonixFlight.name + " (50%)"
raisingPheonixFlightTrigger = effect(raisingPheonixFlight.name, "raisingPhenixFligtTrieer",trigger=TRIGGER_INSTANT,callOnTrigger=raisingPheonixFlight,area=AREA_CIRCLE_3,emoji='<:phenixSkill1_2:1066006794549329980>')
raisingPheonixLaunch = skill("Envolée du Phénix",getAutoId(plumRem.id,True),TYPE_DAMAGE,750,175,area=AREA_CIRCLE_2,emoji='<:rizePhenix:992940415080726688>',effectOnSelf=raisingPheonixFlightTrigger,range=AREA_MONO,ultimate=True,cooldown=7,effectAroundCaster=[TYPE_RESURECTION,AREA_CIRCLE_3,150],use=MAGIE,useActionStats=ACT_DIRECT,description="Après un tour de chargement, Inflige des dégâts aux ennemis alentours tout en réanimant les alliés à portée, et octroi leur octroi Vol du Phénix avec la moitié de sa puissance")
raisingPhonixCastEff = effect("Cast - {0}".format(raisingPheonixLaunch.name),"raisingPhoenixCast",turnInit=2,emoji='<:rizePhenix:992940415080726688>',silent=True,replique=raisingPheonixLaunch)
raisingPheonix = copy.deepcopy(raisingPheonixLaunch)
raisingPheonix.power, raisingPheonix.effectAroundCaster, raisingPheonix.effectOnSelf = 0, None, raisingPhonixCastEff
fairyGardeEff = effect("Garde Féérique","fairyGarde", stat=CHARISMA,power=80,type=TYPE_INDIRECT_HEAL,lvl=1,turnInit=3,trigger=TRIGGER_HP_UNDER_25,emoji='<:suivFee:992496696321912902>')
fairyGarde = skill("Garde Féérique",getAutoId(raisingPheonix.id,True),TYPE_INDIRECT_HEAL,500,emoji='<:suivFee:992496696321912902>',effects=fairyGardeEff,cooldown=7,description="Octroi à l'allié ciblé un effet de soin qui se déclanchera à la fin de sa durée ou si les PVs du porteur deviennent critiques")
jaugeButLight = effect("Jauge Lumineuse","lightbutJauge",emoji=sameSpeciesEmoji("<:blum:992495387812311060>","<:rlum:992495404933455974>"),turnInit=-1,unclearable=True)
jaugeButLight.jaugeValue = jaugeValue(
    emoji=[["<:lej:980923743960461412>","<:mej:980923762016927764>","<:rej:980923786650075228>"],["<:wjl:992574938353516555>","<:wjr:992574974210625556>","<:wjm:992574958033174558>"]],
    conds=[jaugeConds(INC_START_TURN,10),jaugeConds(INC_USE_ELEMENT_SKILL,10,ELEMENT_LIGHT)]
)
sumLightButterfly = skill("Papillons de Lumière",getAutoId(fairyGarde.id,True),TYPE_SUMMON,500,use=CHARISMA,invocation="Papillon de Lumière",cooldown=7,ultimate=True,emoji='<:lumBut:992495232463667200>',nbSummon=3)
fairySlash = skill("Eclat Féérique",getAutoId(sumLightButterfly.id,True),TYPE_DAMAGE,500,power=85,cooldown=5,use=MAGIE,emoji='<:fairySlash:992497227459215451>',area=AREA_CIRCLE_1)
fairyBombEff = effect("Cogitation Féérique","cogiFee", stat=MAGIE,power=60,trigger=TRIGGER_ON_REMOVE,type=TYPE_INDIRECT_DAMAGE,turnInit=2,area=AREA_CIRCLE_2,emoji='<:fairyBomb:992498513940332675>',description="Inflige des dégâts au porteur et ses alliés à portée de mêlée et leur inflige __Poison d'Estialba__ avec 40% de sa puissance")
fairyBomb = skill("Cogitation Féérique",getAutoId(fairySlash.id,True),TYPE_INDIRECT_DAMAGE,750,effects=fairyBombEff,cooldown=7,emoji='<:fairyBomb:992498513940332675>',description="Après deux tours ou si l'ennemi ciblé est vaincu, déclanche une détonatin à sa position lui infligeant des dégâts ainsi qu'à vos ennemis proches.\nLes entités affectés subissent l'effet __Poison d'Estialba__ (50%) pendant 3 tours")
dmonProtectEff = copy.deepcopy(defenseUp)
dmonProtectEff.power, dmonProtectEff.stat, dmonProtectEff.turnInit, dmonProtectEff.block = 8, INTELLIGENCE, 3, 35
dmonProtect = skill("Protection Démoniaque",getAutoId(fairyBomb.id,True),TYPE_BOOST,500,effects=dmonProtectEff,cooldown=5,hpCost=15,range=AREA_DONUT_5,description="Réduit les dégâts subis par un allié et sa probabilité de bloquer une attaque pendant **3** tours",emoji='<:proDmon:994026279680606258>')
hemoBombEff = effect("Cogitation Hemorragique","hemoBomb", stat=STRENGTH,type=TYPE_INDIRECT_DAMAGE,power=110,area=AREA_INLINE_2,turnInit=2,trigger=TRIGGER_ON_REMOVE,emoji='<:bloodyBomb:992499935738089592>',description="Après deux tours ou si l'ennemi ciblé est vaincu, déclanche une détonatin à sa position lui infligeant des dégâts ainsi qu'à vos ennemis allignés.\nLes entités affectés subissent l'effet __Hémorragie__ (25%) pendant 3 tours")
hemoBomb = skill("Cogitation Hémorragique",getAutoId(dmonProtect.id,True),TYPE_INDIRECT_DAMAGE,750,effects=hemoBombEff,cooldown=7,emoji='<:bloodyBomb:992499935738089592>',description="Après deux tours ou si l'ennemi ciblé est vaincu, déclanche une détonatin à sa position lui infligeant des dégâts ainsi qu'à vos ennemis allignés.\nLes entités affectés subissent l'effet __Hémorragie__ (25%) pendant 3 tours")
barrage = skill("Barrage",getAutoId(hemoBomb.id,True),TYPE_DAMAGE,500,50,range=AREA_CIRCLE_4,area=AREA_CONE_2,cooldown=5,repetition=3,emoji="<:barrage:994031489773748265>")
expultion = skill("Expulsion",getAutoId(barrage.id,True),TYPE_DAMAGE,500,85,range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=5,knockback=2,condition=[EXCLUSIVE,ASPIRATION,POIDS_PLUME],emoji='<:liberation:1138942307916337172>')
tripleAttaque2 = skill("Triple Attaque",getAutoId(expultion.id,True),TYPE_DAMAGE,500,50,range=AREA_CIRCLE_3,cooldown=5,description="Inflige trois attaques sur l'ennemi ciblé. Le dernier coup repousse la cible",knockback=2,condition=[EXCLUSIVE,ASPIRATION,POIDS_PLUME],emoji='<:tripleStrike3:1060211755793522798>',affSkillMsg=False)
tripleAttaque2cast = effect("Cast - Triple Attaque","tripleAttaque2",replique=tripleAttaque2,silent=True)
tripleAttaque1 = copy.deepcopy(tripleAttaque2)
tripleAttaque1.power, tripleAttaque1.effectOnSelf, tripleAttaque1.knockback, tripleAttaque1.replay, tripleAttaque1.emoji = 45, tripleAttaque2cast, 0, True, "<:tripleStrike2:1060211719911264416>"
tripleAttaque1cast = effect("Cast - Triple Attaque","tripleAttaque1",replique=tripleAttaque1,silent=True)
tripleAttaque = copy.deepcopy(tripleAttaque1)
tripleAttaque.power, tripleAttaque.effectOnSelf, tripleAttaque.replay, tripleAttaque.emoji, tripleAttaque.affSkillMsg = 40, tripleAttaque1cast, True, "<:tripleStrike1:1060211689217327114>", True

arsenic = effect("Arsenic","arsenic", stat=STRENGTH,power=25,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,stackable=True,emoji='<:arsenic:995361025773817916>')
acidRain1 = skill("Pluie Acide",getAutoId(tripleAttaque.id,True),TYPE_INDIRECT_DAMAGE,750,range=AREA_MONO,area=AREA_ALL_ENEMIES,emoji='<:acidRain:995360946241417388>',minTargetRequired=3,effects=arsenic,effPowerPurcent=int(65/arsenic.power*100),ultimate=True,cooldown=propaUltLaunch.cooldown,description="Après un tour de chargement, inflige __Arsenic__ à tous les ennemis")
acidRainCast = effect("Cast - Pluie Acide","acidRainCast",turnInit=2,silent=True,replique=acidRain1)
acidRain = copy.deepcopy(acidRain1)
acidRain.effects, acidRain.effectOnSelf = [None], acidRainCast
coroRocket = skill("Fusée Corosive",getAutoId(acidRain.id,True),TYPE_INDIRECT_DAMAGE,500,effects=arsenic,effPowerPurcent=int(40/arsenic.power*100),area=AREA_CONE_2,cooldown=poisonus.cooldown,emoji='<:coroRocket:995360986603196417>')
coroMissile1 = skill("Missile corrosif",getAutoId(coroRocket.id,True),TYPE_INDIRECT_DAMAGE,750,effPowerPurcent=int(35/arsenic.power*100),effects=arsenic,area=AREA_CONE_3,minTargetRequired=2,cooldown=7,emoji='<:coroMissile:995361003581739018>')
coroMissileCast = effect("Cast - Missile corrosif","coroMissileCast",turnInit=2,silent=True,replique=coroMissile1)
coroMissile = copy.deepcopy(coroMissile1)
coroMissile.effects, coroMissile.effectOnSelf = [None], coroMissileCast
coroShot = skill("Tir corrosif",getAutoId(coroMissile.id,True),TYPE_DAMAGE,500,80,area=AREA_LINE_3,effects=arsenic,effPowerPurcent=int(35/arsenic.power*100),cooldown=5,emoji='<:coroShot:995360968697716837>')

quadFleau = skill("Quadruple Fléau",getAutoId(coroShot.id,True),TYPE_INDIRECT_DAMAGE,750,effects=[estial,coroWind,bleeding,arsenic],cooldown=7,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS], emoji='<:quaFleau:1016796997887459370>', effPowerPurcent=125)
charmingPandant = skill("Médaillon d'Amour","sph",TYPE_BOOST,emoji='<:lovePendant:982175214773358593>',price=750,area=AREA_CIRCLE_2,range=AREA_MONO,cooldown=5,description="Augmente les statistiques des alliés proches tout en réduisant légèrement celles des ennemis autour de vous")
windDanceEff = effect("Soyokaze","windDanceEff",turnInit=-1,unclearable=True,emoji='<:liaCounter:998001563379437568>',reject=["liaKatanaEff"],counterOnDodge=25,description="Vous octroi **25%** de chance d'effectuer une **contre-attaque** en esquivant une attaque d'un adversaire se trouvant à 3 cases ou moins de vous")
windDance = skill("Soyokaze",getAutoId(quadFleau.id,True),TYPE_PASSIVE,500,effectOnSelf=windDanceEff,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],emoji="<:liaCounter:998001563379437568>",quickDesc="Vous donne une chance de contre-attaquer en esquivant une attaque")

belierChargeEff = copy.deepcopy(defenseUp)
belierChargeEff.power, belierChargeEff.block = 25, 35
belierCharge = skill("Charge du Bélier","jushu",TYPE_DAMAGE,500,power=60,effectOnSelf=belierChargeEff,cooldown=7,range=AREA_INLINE_4,description="Saute au corps à corps d'un ennemi en lui infligeant des dégâts tout en réduisant vos dégâts réçus et augmentant votre taux de blocage jusqu'au prochain tour")
taureauFury = skill("Furie du Taureau","geghthz",TYPE_DAMAGE,500,power=37,setAoEDamage=True,repetition=3,accuracy=100,area=AREA_CIRCLE_2,range=AREA_MONO,cooldown=7,description="Inflige trois attaques aux ennemis à portée de mêlée avec une précision accrue")
gemeauSynEff = copy.deepcopy(dmgUp)
gemeauSynEff.power = 15
gemeauSyn = skill("Synergie des Jumeaux","hehge",TYPE_BOOST,500,effects=gemeauSynEff,effectOnSelf=gemeauSynEff,cooldown=7,replay=True,description="Augmente vos propres dégâts infligés ainsi que ceux de l'allié ciblé de **15%** pendant un tour et vous permet de rejouer")
cancerAssault = skill("Assaut du Crabe","hehehe",TYPE_DAMAGE,500,power=12,repetition=10,cooldown=7,range=AREA_INLINE_4,description="Attaque à dix reprises l'ennemi ciblé")
lionRoarEff= effect("Couardise","lion'sroareff", stat=ENDURANCE,strength=-10,magie=-10,charisma=-10,intelligence=-10,type=TYPE_MALUS)
lionRoar = skill("Rugissement du Lion","hehehe",TYPE_MALUS,500,range=AREA_MONO,area=AREA_DONUT_4,effects=lionRoarEff,cooldown=7,description="Réduit les statistiques des ennemis alentours pendant un tour")
viergeSkillEff = effect("Bénédiction de la vierge","viergeBene",type=TYPE_BOOST,stat=INTELLIGENCE,resistance=7,inkResistance=12,turnInit=3)
vierge = skill("Bénidiction de la Vièrge","rgege",TYPE_BOOST,500,effects=viergeSkillEff,cooldown=7,description="Accroi la Résistance et réduit les dégâts indirects subis de l'allié ciblé")
balanceBoostEff = effect("Egaltité de la Balance",'balanceBoostEff', stat=CHARISMA,strength=5,endurance=3,charisma=5,intelligence=5,agility=3,precision=3,magie=5,emoji='<:balance:960319658823667762>')
balanceBoost = skill("Equilibre de la Balance","rejgikjhg",TYPE_BOOST,500,area=AREA_CIRCLE_5,range=AREA_MONO,effects=balanceBoostEff,cooldown=7,description="Augmente légèrement les statistiques principaux de vos alliés proches")
scorpVenum = effect("Venin du Scorpion","scorpionVenum", stat=MAGIE,power=40,turnInit=2,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,description="Inflige des dégâts à la fin du tour du porteur pendant deux tours",lvl=2)
scorpionByte = skill("Piqûre du Scorpion","gsg",TYPE_DAMAGE,500,power=65,use=MAGIE,effects=scorpVenum,cooldown=7,description="Inflige des dégâts à l'ennemi ciblé et l'empoisonne pendant 2 tours",useActionStats=ACT_INDIRECT)
sagArrow = skill("Flèche du Sagitaire","hhehe",TYPE_DAMAGE,500,power=120,area=AREA_LINE_3,range=AREA_CIRCLE_4,cooldown=7,description="Inflige des dégâts aux ennemis ciblés")
capricorne = skill("Percée du Capricorne","hehehe",TYPE_DAMAGE,500,135,area=AREA_LINE_3,range=AREA_CIRCLE_1,cooldown=7,use=MAGIE,description="Inflige des dégâts aux ennemis ciblés")
verseauShield = effect("Versatilité","verseauShield", stat=INTELLIGENCE,overhealth=60,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
verseau = skill("Omniprésence du Verseau","hehhee",TYPE_HEAL,500,verseauShield.overhealth,area=AREA_CIRCLE_2,effects=verseauShield,range=AREA_CIRCLE_4,cooldown=7,description="Soigne les alliés ciblés et leur octroi une armure",use=INTELLIGENCE)
fishHot = effect("Grâce du Poisson","fishGrace", stat=CHARISMA,power=22,turnInit=3,type=TYPE_HEAL,trigger=TRIGGER_START_OF_TURN)
fishGrace = skill("Grâce du Poisson","heheheh",TYPE_INDIRECT_HEAL,500,effects=fishHot,area=AREA_CIRCLE_3,range=AREA_MONO,cooldown=7,description="Applique un effet de régénération sur vous et vos alliés proches")
lightEstoc = skill("Estoc Lumineuse",getAutoId("smh",True),TYPE_DAMAGE,500,power=80,range=AREA_CIRCLE_1,emoji='<:estocLum:1015221284726128710>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_4,40],cooldown=5,description="Inflige des dégâts aux ennemis ciblés et vous soigne ainsi que vos alliés alentours",use=CHARISMA,useActionStats=ACT_HEAL,area=AREA_LINE_2)
lightTrancheShield = effect("Armure de Lumière","lightArmor", stat=INTELLIGENCE,stackable=True,type=TYPE_ARMOR,trigger=TRIGGER_START_OF_TURN,turnInit=3,overhealth=40)
lightTranche = skill("Tranche Lumineuse",getAutoId(lightEstoc.id,True),TYPE_DAMAGE,500,power=85,range=AREA_CIRCLE_1,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],effectAroundCaster=[TYPE_ARMOR,AREA_CIRCLE_4,lightTrancheShield],cooldown=5,description="Inflige des dégâts aux ennemis ciblés et vous procure ainsi qu'à vos alliés alentours une armure",use=INTELLIGENCE,useActionStats=ACT_SHIELD,area=AREA_ARC_1,emoji='<:trancheLum:1066757399949606922>')
lightShot = skill("Tir Lumineux",getAutoId(lightTranche.id,True),TYPE_DAMAGE,500,emoji="<:lightShot:1137430291976306759>",power=70,range=AREA_CIRCLE_5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_3,35],cooldown=5,description="Inflige des dégâts aux ennemis ciblés et vous soigne ainsi que vos alliés alentours",use=CHARISMA,useActionStats=ACT_HEAL,area=AREA_LINE_2)
lightPulseShield = effect("Armure de Lumière","lightArmor", stat=INTELLIGENCE,stackable=True,type=TYPE_ARMOR,trigger=TRIGGER_START_OF_TURN,turnInit=3,overhealth=30)
lightPulse = skill("Pulsation Lumineuse",getAutoId(lightShot.id,True),TYPE_DAMAGE,500,power=65,range=AREA_CIRCLE_1,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],effectAroundCaster=[TYPE_ARMOR,AREA_CIRCLE_4,lightPulseShield],cooldown=5,description="Inflige des dégâts aux ennemis ciblés et vous procure ainsi qu'à vos alliés alentours une armure",use=INTELLIGENCE,useActionStats=ACT_SHIELD,emoji='<:pulLum:1066757422976356514>')

accelerant = skill("Accélération",getAutoId(lightPulse.id,True),TYPE_BOOST,750,cooldown=5,description="Permet à l'allié ciblé de jouer deux fois lors de son prochain tour",condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],emoji='<:qqLuna:932318030380302386>')
assautEcarlateEff = copy.deepcopy(defenseUp)
assautEcarlateEff.power = 20
assautEcarlate = skill("Assaut Ecarlate",getAutoId(accelerant.id,True),TYPE_DAMAGE,500,70,range=AREA_CIRCLE_1,area=AREA_CONE_3,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],cooldown=5,emoji='<:assEcar:999762960484409454>',description="Saute au corps à corps de l'ennemi ciblé, lui inflige des dégâts ainsi qu'à ses alliés proches, puis effectue une seconde attaque dans une large zone d'effet tout en réduisant de **{0}%** les dégâts subis pendant un tour".format(assautEcarlateEff.power),effectOnSelf=assautEcarlateEff)
assautEcarlateCast = effect("Cast - Assaut Ecarlate","assEcarCast",replique=assautEcarlate,silent=True)
cycloneEcarlate = skill("Cyclone Ecarlate",assautEcarlate.id,TYPE_DAMAGE,assautEcarlate.price,assautEcarlate.power,tpCac=True,range=AREA_INLINE_4,area=AREA_CIRCLE_1,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],cooldown=7,emoji='<:cyclEcar:999762891513266287>',description="Saute au corps à corps de l'ennemi ciblé, lui inflige des dégâts ainsi qu'à ses alliés proches, puis effectue une seconde attaquedans une large zone d'effet tout en réduisant de **{0}%** les dégâts subis pendant un tour".format(assautEcarlateEff.power),effectOnSelf=assautEcarlateCast,replay=True)
sillageEff = effect("Sillage","sillageEff", stat=MAGIE,power=35,area=AREA_CIRCLE_2,trigger=TRIGGER_END_OF_TURN,turnInit=3,lvl=3,emoji='<:sill:999763058526269510>',type=TYPE_INDIRECT_DAMAGE)
sillage = skill("Sillage",getAutoId(cycloneEcarlate.id,True),TYPE_DAMAGE,500,70,use=MAGIE,area=AREA_CIRCLE_1,range=AREA_CIRCLE_4,effects=sillageEff,cooldown=5,emoji=sillageEff.emoji[0][0],description="Inflige des dégâts à l'ennemi ciblé et lui inflige un effet de poison qui infligera des dégâts en zone durant les deux prochains tours",condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR])
cassMontEffTrig = effect("Casse-Montagne","cassMontEff", stat=MAGIE,power=50,trigger=TRIGGER_INSTANT,type=TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_1,emoji='<:cassMont:999763013722701944>')
casseMontEff = effect("Casse-Montagne","cassMont", stat=MAGIE,lvl=5,turnInit=3,onDeclancher=True,emoji=cassMontEffTrig.emoji[0][0],description="Lorsque le porteur effectue une attaque, inflige des dégâts supplémentaires à la cible principale si cette dernière est un ennemi",callOnTrigger=cassMontEffTrig,trigger=TRIGGER_DEALS_DAMAGE)
cassMont = skill("Casse-Montagne",getAutoId(sillage.id,True),TYPE_BOOST,500,range=AREA_MONO,replay=True,effects=casseMontEff,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],cooldown=5,emoji=casseMontEff.emoji[0][0],description="Lors de vos **{0}** prochaines attaques, vous infligerez des dégâts indirects supplémentaires".format(casseMontEff.lvl))
finalClassique = skill("Final Classique",getAutoId(cassMont.id,True),TYPE_DAMAGE,500,power=50,maxPower=125,accuracy=105,range=AREA_MONO,area=AREA_CIRCLE_2,jaugeEff=finalTech.jaugeEff,minJaugeValue=15,maxJaugeValue=50,description="Consomme une partie de votre {0} __{1}__ pour infliger des dégâts aux ennemis autour de vous avec une précision accrue. Plus la quantité de jauge consommée est élevée, plus les dégats seront importants".format(eventFas.emoji[0][0],eventFas.name),emoji='<:finCla:1000145130357006436>')
lysJauge = effect("Canne fleurie","lysJaugeEff",turnInit=-1,unclearable=True,emoji='<:canFleur:1000145818877177886>')

lysJauge.jaugeValue = jaugeValue(
    emoji=[["<:lej:980923743960461412>","<:mej:980923762016927764>","<:rej:980923786650075228>"],["<:ftlj:980930222679543918>","<:ftrj:980930256032641074>","<:ftmj:980930239901343834>"]],
    conds=[jaugeConds(INC_START_TURN,15)]
)

offrRec = skill("Offrande de Réconfort",getAutoId(finalClassique.id,True),TYPE_HEAL,power=int(cure.power*0.85),description="Soigne l'allié ciblé",emoji='<:recof:1000144740651634748>',cooldown=3)
offrRav = skill("Offrande de Ravissement",offrRec.id,TYPE_HEAL,power=int(cure.power*0.55),description="Vous soigne ainsi que les alliés autour de vous",area=AREA_CIRCLE_2,range=AREA_MONO,emoji='<:ravis:1000144722427392010>',cooldown=3)
bundleOffr = skill("Offrande des Lys",offrRec.id,TYPE_HEAL,become=[offrRec,offrRav],emoji=lysJauge.emoji[0][0],price=500)
tetragramme = skill("Tétragramme",getAutoId(bundleOffr.id,True),TYPE_HEAL,500,power=45,cooldown=5,replay=True,emoji='<:tetragramme:1229488862380822590>')
confiteorReady = effect("Confiteor préparé","confiteorReady",turnInit=5,emoji='<:confiteor:1003026495050096731>',silent=True)
confiteor = skill("Confiteor",getAutoId(tetragramme.id,True),TYPE_DAMAGE,0,power=135,area=AREA_CIRCLE_1,emoji='<:confiteor:1003026495050096731>',needEffect=[confiteorReady],cooldown=5,condition=[EXCLUSIVE,ASPIRATION,ENCHANTEUR],use=MAGIE,range=AREA_CIRCLE_3,effectAroundCaster=[TYPE_HEAL,AREA_MONO,50])
holyCircleReady = effect("Cercle Sacré préparé","holyCircleReady",turnInit=5,emoji='<:cerSacre:1003026472262451300>',silent=True)
cercleSacre = skill("Cercle Sacré",confiteor.id,TYPE_DAMAGE,0,power=100,area=AREA_CIRCLE_2,range=AREA_MONO,emoji='<:cerSacre:1003026472262451300>',needEffect=[holyCircleReady],effectOnSelf=confiteorReady,condition=[EXCLUSIVE,ASPIRATION,ENCHANTEUR],use=MAGIE,effectAroundCaster=[TYPE_HEAL,AREA_MONO,50])
holySpiritReady = effect("Esprit Saint préparé","holySpiritReady",turnInit=5,emoji='<:espSaint:1003026446706544733>',silent=True)
espritSaint = skill("Esprit Saint",confiteor.id,TYPE_DAMAGE,0,power=80,emoji='<:espSaint:1003026446706544733>',needEffect=[holySpiritReady],effectOnSelf=holyCircleReady,condition=[EXCLUSIVE,ASPIRATION,ENCHANTEUR],use=MAGIE,range=AREA_CIRCLE_3,effectAroundCaster=[TYPE_HEAL,AREA_MONO,50])
requiescat = skill("Requiescat",confiteor.id,TYPE_DAMAGE,0,power=50,emoji='<:requiescat:1003026420798328974>',effectOnSelf=holySpiritReady,description="Inflige des dégâts à l'ennemi ciblé et vous permet de commencer le Combot Confiteor",condition=[EXCLUSIVE,ASPIRATION,ENCHANTEUR],use=MAGIE,range=AREA_CIRCLE_1,effectAroundCaster=[TYPE_HEAL,AREA_MONO,35],rejectEffect=[confiteorReady,holyCircleReady,holySpiritReady],replay=True)
comboConfiteor = skill("Combo Confiteor",confiteor.id,TYPE_DAMAGE,500,confiteor.power,condition=[EXCLUSIVE,ASPIRATION,ENCHANTEUR],become=[requiescat,espritSaint,cercleSacre,confiteor],area=AREA_CIRCLE_1,emoji=confiteor.emoji,description="Vous permet d'effectuer le Combot Confiteor.\n{0} __{1}__, {2} __{3}__ et {4} __{5}__ vous soigne également d'une puissance de **{6}** en utilisant la statistique d'action de dégâts directs.\n{2} __{3}__ se lance sur soi-même.".format(espritSaint.emoji,espritSaint.name,cercleSacre.emoji,cercleSacre.name,confiteor.emoji,confiteor.name,40),use=MAGIE)

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
dechargeGausse = skill("Décharge de Gausse",getAutoId(comboConfiteor.id,True),TYPE_DAMAGE,power=50,use=PRECISION,emoji="<:gausse:1003645652313575516>",needEffect=[fakedechargeEff],cooldown=0,description="Inflige des dégâts *Précision* à l'ennemi ciblé",jaugeEff=focusJauge)
fakedechargeEff.replica = dechargeGausse
cryoExplosionReady = effect("Cryo-Explosion Préparée","cryoExploReady",stackable=True,turnInit=3,emoji='<:cryoexplo:1003645574647660605>')
cryoExplosion = skill("Cryo-Explosion",dechargeGausse.id,TYPE_DAMAGE,power=80,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],emoji='<:cryoexplo:1003645574647660605>',effectOnSelf=fakedechargeEff,replay=True,needEffect=[cryoExplosionReady],cooldown=0,description="Inflige des dégâts Eau *Force* à l'ennemi ciblé et enchaîne directement avec {0} __{1}__ en ciblant ce même ennemi".format(dechargeGausse.emoji,dechargeGausse.name),jaugeEff=focusJauge)
cryoExplosionReady.description = "Permet d'utiliser la compétence {0} __{1}__".format(cryoExplosion.emoji,cryoExplosion.name)
cryoChargeEff = copy.deepcopy(dmgUp)
cryoChargeEff.power, cryoChargeEff.turnInit = 15, 3
cryoCharge = skill("Cryo-Charge",dechargeGausse.id,TYPE_BOOST,range=AREA_MONO,cooldown=0,replay=True,jaugeEff=focusJauge,minJaugeValue=35,maxJaugeValue=35,effects=[cryoChargeEff,cryoExplosionReady],effectOnSelf=hyperchargent,rejectEffect=[hyperchargent],description="Augmente vos dégâts infligés de **{0}%** durant 3 tours et vous octroi 3 effets {1} __{2}__ sur la même durée".format(cryoChargeEff.power,cryoExplosionReady.emoji[0][0],cryoExplosionReady.name),emoji='<:icecharge:1003645528468373565>')
cryoChargeBundle = skill("Cryo-Hypercharge",dechargeGausse.id,TYPE_DAMAGE,750,power=cryoExplosion.power+dechargeGausse.power,become=[cryoCharge,cryoExplosion,dechargeGausse],jaugeEff=focusJauge,emoji=cryoCharge.emoji,description="{0} __{1}__ :\n{2}\nUtiliser __{1}__ coûte {9} pts de {10} __{11}__\n\n{3} __{4}__ :\n{5}\n__{4}__ est considérée comme une compétence Eau\n\n{6} __{7}__ :\n{8}".format(cryoCharge.emoji, cryoCharge.name, cryoCharge.description, cryoExplosion.emoji, cryoExplosion.name, cryoExplosion.description, dechargeGausse.emoji, dechargeGausse.name, dechargeGausse.description, cryoCharge.minJaugeValue, focusJauge.emoji[0][0], focusJauge.name),condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER])

ricochetReady = effect("Enchaînement - Ricochet","enchDechGausse",emoji='<:ricochet:1003645701839933520>',silent=True)
ricochet = skill("Ricochet",getAutoId(cryoChargeBundle.id,True),TYPE_DAMAGE,power=35,area=AREA_CIRCLE_1,jaugeEff=focusJauge,use=PRECISION,emoji="<:ricochet:1003645701839933520>",needEffect=[ricochetReady],cooldown=0,description="Inflige des dégâts *Précision* à l'ennemi ciblé")
ricochetReady.replica = ricochet
pyroArbaReady = effect("Pyro-Arbalette Préparée","pyroArbaready",stackable=True,turnInit=3,emoji='<:arbalte:1003645679450738770>')
pyroArba = skill("Pyro-Arbalette",ricochet.id,TYPE_DAMAGE,power=65,jaugeEff=focusJauge,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],area=AREA_CONE_2,emoji='<:arbalte:1003645679450738770>',effectOnSelf=ricochetReady,replay=True,needEffect=[pyroArbaReady],cooldown=0,description="Inflige des dégâts Eau *Force* à l'ennemi ciblé et enchaîne directement avec {0} __{1}__ en ciblant ce même ennemi".format(ricochet.emoji,ricochet.name))
pyroArbaReady.description = "Permet d'utiliser la compétence {0} __{1}__".format(pyroArba.emoji,pyroArba.name)
pyroCharge = skill("Pyro-Charge",ricochet.id,TYPE_BOOST,range=AREA_MONO,cooldown=0,replay=True,jaugeEff=focusJauge,minJaugeValue=35,maxJaugeValue=35,effects=[cryoChargeEff,pyroArbaReady],effectOnSelf=hyperchargent,rejectEffect=[hyperchargent],description="Augmente vos dégâts infligés de **{0}%** durant 3 tours et vous octroi 3 effets {1} __{2}__ sur la même durée".format(cryoChargeEff.power,pyroArbaReady.emoji[0][0],pyroArbaReady.name),emoji='<:firecharge:1003645503709388860>')
pyroChargeBundle = skill("Pyro-Hypercharge",ricochet.id,TYPE_DAMAGE,750,power=pyroArba.power+ricochet.power,become=[pyroCharge,pyroArba,ricochet],jaugeEff=focusJauge,emoji=pyroCharge.emoji,description="{0} __{1}__ :\n{2}\nUtiliser __{1}__ coûte {9} pts de {10} __{11}__\n\n{3} __{4}__ :\n{5}\n__{4}__ est considérée comme une compétence Feu\n\n{6} __{7}__ :\n{8}".format(pyroCharge.emoji, pyroCharge.name, pyroCharge.description, pyroArba.emoji, pyroArba.name, pyroArba.description, ricochet.emoji, ricochet.name, ricochet.description, pyroCharge.minJaugeValue, focusJauge.emoji[0][0], focusJauge.name),condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE])

drill = skill("Foreuse",getAutoId(pyroChargeBundle.id,True),TYPE_DAMAGE,750,power=125,jaugeEff=focusJauge,minJaugeValue=40,url='https://media.discordapp.net/attachments/1130204608900386910/1131443230240690227/20230720_063044.gif',maxJaugeValue=40,percing=35,description="Inflige des dégâts à l'ennemi ciblé en ignorant **35%** de sa résistance",emoji='<:drill:1003645776876015626>',cooldown=3)
anchorEff = copy.deepcopy(chained)
anchorEff.turnInit = 3
anchor = skill("Ancre Aérienne",getAutoId(drill.id,True),TYPE_DAMAGE,750,power=125,url='https://media.discordapp.net/attachments/1130204608900386910/1131443230613962792/20230720_062040.gif',jaugeEff=focusJauge,minJaugeValue=50,maxJaugeValue=50,effects=anchorEff,description="Inflige des dégâts à l'ennemi ciblé et restrain ses déplacements pendant 3 tours",emoji='<:anchor:1003645801421099018>',cooldown=3)
chainsaw = skill("Tronçonneuse Rotatives",getAutoId(anchor.id,True),TYPE_DAMAGE,750,power=125,jaugeEff=focusJauge,url='https://media.discordapp.net/attachments/1130204608900386910/1131443229808656424/20230720_062306.gif',minJaugeValue=60,maxJaugeValue=60,area=AREA_LINE_3,description="Inflige des dégâts aux ennemis ciblés",cooldown=3,emoji="<:tronc:1003645821826371684>")
mysticShot = skill("Fusil Mystique",getAutoId(chainsaw.id,True),TYPE_DAMAGE,750,power=150,maxPower=200,jaugeEff=focusJauge,minJaugeValue=50,url="https://media.discordapp.net/attachments/1006418796329848954/1007574358983704646/20220812_105247.gif",maxJaugeValue=100,ultimate=True,cooldown=5,description="Inflige des dégâts à l'ennemi ciblé. La puissance augmente en fonction de la quantité de jauge consommée",emoji="<:fusil:1003646584497655839>")

bestSkill = skill("Pls Die","bestSkill",TYPE_DAMAGE,0,power=1000,area=AREA_ALL_ENEMIES,use=PURCENTAGE,emoji='<a:giveup:902383022354079814>',description="Omae wa mou shinderu",say="Omae wa mou shinderu")

pyroSparkleEff = effect("Résistance Réduite","pyroBlastEff", stat=PURCENTAGE,resistance=-20,turnInit=3,type=TYPE_MALUS)
pyroSparkle = skill("Fire Sparkle","",TYPE_DAMAGE,500,100,area=AREA_CONE_2,cooldown=7,use=MAGIE,effects=pyroSparkleEff,emoji='<:pyroDeflag:1171159256259637310>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],description="Inflige des dégâts aux ennemis ciblés et réduit la résistance de la cible principale")
pyroCalcinateEff1 = copy.deepcopy(incurable)
pyroCalcinateEff1.power, pyroCalcinateEff1.turnInit = 20, 3
pyroCalcinateEff = effect("Fire Wave","pyroCalcination",callOnTrigger=pyroCalcinateEff1,area=AREA_CIRCLE_1,type=TYPE_MALUS,emoji='<:pillierdefeu:1171155826908598332>',trigger=TRIGGER_INSTANT)
pyroCalcinate = skill("Fire Wave","",TYPE_DAMAGE,500,100,AREA_BOMB_6,area=AREA_CIRCLE_1,cooldown=7,effects=pyroCalcinateEff,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],emoji=pyroCalcinateEff.emoji[0][0],description="Inflige des dégâts à des ennemis éloignés et réduit les soins qu'ils reçoivent durant un moment")
pyroBlastEff = effect("Fire Blast","pyroBlastEff", stat=MAGIE,power=20,turnInit=3,trigger=TRIGGER_START_OF_TURN,stackable=True,type=TYPE_INDIRECT_DAMAGE,emoji='<:pyroblast:1171177670663483413>')
pyroBlast = skill("Fire Blast","",TYPE_DAMAGE,500,100,area=AREA_LINE_2,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],emoji=pyroBlastEff.emoji[0][0],effectOnSelf=tablElemEff[ELEMENT_FIRE],damageOnArmor=1.25,effects=pyroBlastEff,cooldown=7,description="Inflige des dégâts en ligne aux ennemis ciblés (dégâts augmentés contre l'armure) ainsi qu'un petit effet de dégâts indirects à la cible principale et vous octroi {0} {1}".format(tablElemEff[ELEMENT_FIRE].emoji[0][0],tablElemEff[ELEMENT_FIRE].name))
windCutter = skill("Wind Cutter","",TYPE_DAMAGE,500,100,AREA_INLINE_3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],cooldown=7,setAoEDamage=True,area=AREA_LINE_2,emoji='<:windcutter:1170960775439974432>',description="Inflige des dégâts en ligne aux ennemis ciblés et vous octroi {0} {1}".format(tablElemEff[ELEMENT_AIR].emoji[0][0],tablElemEff[ELEMENT_AIR].name),effectOnSelf=tablElemEff[ELEMENT_AIR],use=MAGIE)
windBlast = skill("Wind Blast","",TYPE_DAMAGE,500,120,AREA_CIRCLE_3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],cooldown=7,area=AREA_CIRCLE_1,use=MAGIE,description="Inflige des dégâts aux ennemis ciblés avec du vol de vie et armure",emoji='<:windblast:1170960798949064745>',lifeSteal=25,armorSteal=25,armorConvert=25)
windZephir = skill("Zephir","",TYPE_DAMAGE,500,120,AREA_MONO,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],emoji='<:zephir:1170960752698470472>',cooldown=7,area=AREA_CIRCLE_2,accuracy=150,knockback=2,use=MAGIE,description="Inflige des dégâts et repousse les ennemis autour de vous")
spaceCrush = skill("Choc Astral","",TYPE_DAMAGE,500,85,AREA_MONO,condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE],area=AREA_CIRCLE_2,cooldown=7,use=MAGIE,emoji='<:celestialChoc:1183652099620360252>',armorConvert=50,replay=True,description="Inflige des dégâts aux ennemis autour de vous et convertie tous les dégâts infligés en armure")
spacePulse2 = skill("Pulsation Céleste","",TYPE_DAMAGE,500,50,AREA_CIRCLE_2,emoji='<:pulsation:1228790863799517354>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE],cooldown=7,use=MAGIE,area=AREA_CIRCLE_1,knockback=1,description="Inflige des dégâts aux ennemis ciblés et les repousses à trois reprises")
spacePulse2_c = effect("Enchaînement - {replicaName}","spacePulse2_c",replique=spacePulse2,silent=True)
spacePulse1 = copy.deepcopy(spacePulse2)
spacePulse1.effectOnSelf, spacePulse1.replay = spacePulse2_c, True
spacePulse1_c = effect("Enchaînement - {replicaName}","spacePulse1_c",replique=spacePulse1,silent=True)
spacePulse = copy.deepcopy(spacePulse1)
spacePulse.effectOnSelf = spacePulse1_c
spaceComet = skill("Comète Céleste","",TYPE_DAMAGE,500,120,AREA_DIST_5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE],cooldown=7,use=MAGIE,area=AREA_CIRCLE_1,emoji='<:spaceComet:1191496284859801650>',description="Inflige des dégâts aux ennemis ciblés et vous octroi {0} {1}".format(tablElemEff[ELEMENT_SPACE].emoji[0][0],tablElemEff[ELEMENT_SPACE].name),effectOnSelf=tablElemEff[ELEMENT_SPACE])
lightCrossEff = effect("Armure Lumineuse","lightArmorCross", stat=PURCENTAGE,overhealth=20,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji="<:lightHealShield:929322808654323733>")
lightCross = skill("Croix de Lumière","",TYPE_HEAL,500,50,AREA_CIRCLE_4,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],cooldown=7,area=AREA_INLINE_3,effects=lightCrossEff,use=CHARISMA,description="Soigne les alliés en croix et leur octroi une armure en fonction de leurs PV maximums",emoji='<:ancientLight1:1147186235727695943>')
lightPillarCombo3NeededEffect = effect("Pullier de Lumière Préparé","lightPillarCombo3NeededEffect",turnInit=5,emoji='<:lightMagic2:1118249005172936767>',silent=True)
lightPillarCombo3 = skill("Pillier de Lumière","",TYPE_DAMAGE,power=150,range=AREA_CIRCLE_4,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],cooldown=7,lifeSteal=35,aoeLifeSteal=20,use=MAGIE,emoji=lightPillarCombo3NeededEffect.emoji[0][0],needEffect=lightPillarCombo3NeededEffect,description="Inflige des dégâts aux ennemis ciblés avec un taux de vol de vie de zone")
lightPillarCombo2NeededEffect = effect("Fontaine de Lumière","lightPillarCombo2NeededEffect",turnInit=5,emoji='<:lightMagic3:1118249044683260027>',silent=True)
lightPillarCombo2 = skill("Fontaine de Lumière","",TYPE_DAMAGE,power=120,range=AREA_CIRCLE_4,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],cooldown=1,lifeSteal=35,aoeLifeSteal=20,use=MAGIE,emoji=lightPillarCombo2NeededEffect.emoji[0][0],needEffect=lightPillarCombo2NeededEffect,effectOnSelf=lightPillarCombo3NeededEffect,description="Inflige des dégâts aux ennemis ciblés avec un taux de vol de vie de zone")
lightPillarCombo1 = skill("Missile de Lumière","",TYPE_DAMAGE,power=100,range=AREA_CIRCLE_4,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],cooldown=1,lifeSteal=35,aoeLifeSteal=20,use=MAGIE,emoji="<:lightMagic1:1118248965389959228>'",rejectEffect=[lightPillarCombo2NeededEffect,lightPillarCombo3NeededEffect],effectOnSelf=lightPillarCombo2NeededEffect,description="Inflige des dégâts aux ennemis ciblés avec un taux de vol de vie de zone")
lightPillar = skill("Combo - Pillier de Lumière","",TYPE_DAMAGE,500,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],become=[lightPillarCombo1,lightPillarCombo2,lightPillarCombo3],emoji=lightPillarCombo3.emoji,description="Permet d'effectuer un combo de compétences offensives vous soignant vous et vos alliés proches en fonction des dégâts infligés")
lightFlashEff = effect("Flash de Lumière","lightFlash", stat=MISSING_HP,power=20,trigger=TRIGGER_INSTANT,type=TYPE_INDIRECT_HEAL,emoji='<:lightHealShield:929322808654323733>')
lightFlash = skill("Flash de Lumière","",TYPE_DAMAGE,500,power=120,cooldown=7,range=AREA_MONO,area=AREA_CIRCLE_2,effectOnSelf=lightFlashEff,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],emoji='<:iliLightField:1046381182767603752>',description="Inflige des dégâts aux ennemis alentours et vous soigne en fonction de vos PV manquants")
bouncingWaterEff = effect("Bouncing Water","bouncingWater", stat=MISSING_HP,power=20,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_INSTANT,emoji='<:aquabounce:1171550661683462145>')
bouncingWater = skill("Bouncing Water","",TYPE_DAMAGE,750,80,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],effectOnSelf=bouncingWaterEff,effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_LOWEST_HP_ALLIE,bouncingWaterEff],emoji=bouncingWaterEff.emoji[0][0],use=MAGIE,cooldown=7,description="Inflige des dégâts à l'ennemi ciblé puis vous soigne vous et votre allié le plus blessé en fonction de vos PVs manquants")
waterRangEff1 = effect("AquaBoom","aquaRangEff1", stat=MAGIE,trigger=TRIGGER_INSTANT,type=TYPE_INDIRECT_DAMAGE,power=35,area=AREA_DONUT_1,emoji='<:water1:1065647748826791966>')
waterRangEff = effect("AquaBoom","aquaRangEff", stat=MAGIE,callOnTrigger=waterRangEff1,trigger=TRIGGER_INSTANT,area=AREA_ARC_2,emoji=waterRangEff1.emoji)
waterRang = skill("WaterRang","",TYPE_DAMAGE,500,85,AREA_BOMB_5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],effects=waterRangEff,use=MAGIE,cooldown=7,area=AREA_ARC_2,setAoEDamage=True,emoji='<:aquarang:1171550682302652537>',lifeSteal=35,description="Inflige des dégâts dans une zone d'arc de cercle en ciblant un ennemi éloigné avec un taux de vol de vie. Une petite explosion inflige des dégâts indirects aux ennemis proches des cibles initiales",quickDesc="Un disque d'eau qui file au travers des lignes ennemis")
waterBlast = skill("Water Blast","",TYPE_DAMAGE,500,100,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],effectOnSelf=tablElemEff[ELEMENT_WATER],emoji='<:aquablast:1171550598550790215>',use=MAGIE,cooldown=5,description="Inflige des dégâts à l'ennemi ciblé et vous octroi {0} {1}".format(tablElemEff[ELEMENT_WATER].emoji[0][0],tablElemEff[ELEMENT_WATER].name))
rockStomp = skill("Rock Stomp","",TYPE_DAMAGE,500,120,area=AREA_MONO,range=AREA_CIRCLE_1,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],cooldown=7,use=MAGE,damageOnArmor=1.25,armorSteal=50,armorConvert=25,description="Inflige des dégâts augmentés contre l'armure aux ennemis proche, en volant de l'armure et en convertissant une partie des dégâts infligés en armure",emoji='<:terraStamp:1171322788355780618>')
rockSpikeEff1, rockSpikeEff2 = effect("Résistance Réduite","rockSpikeEff1", stat=PURCENTAGE,resistance=-25,type=TYPE_MALUS), copy.deepcopy(armorGetMalus)
rockSpikeEff2.power = 25
rockSpike = skill("Rock Spike","",TYPE_DAMAGE,500,100,AREA_CIRCLE_3,emoji='<:rockLame:1208760088463155240>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],cooldown=7,effects=[rockSpikeEff1,rockSpikeEff2],garCrit=True,use=MAGIE,description="Inflige des dégâts critiques à l'ennemi ciblé et réduit sa résistance et l'armure qu'il reçoit pendant un tour")
rockBlast = skill("Rock Blast","",TYPE_DAMAGE,500,100,AREA_CIRCLE_2,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],cooldown=5,effectOnSelf=tablElemEff[ELEMENT_EARTH],use=MAGE,emoji='<:terrablast:1171185878723469424>',description="Inflige des dégâts à l'ennemi ciblé et vous octroi {0} {1}".format(tablElemEff[ELEMENT_EARTH].emoji[0][0],tablElemEff[ELEMENT_EARTH].name))
descynNegEff = effect("Désyncronisation Négative","negDescync", stat=MISSING_HP,power=10,turnInit=3,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji='<:desyncNegEff:1168268631516393503>')
descynNeg = skill("Désyncronisation Négative","",TYPE_DAMAGE,500,100,range=AREA_MONO,area=AREA_CIRCLE_2,condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_DONUT_2,descynNegEff],emoji='<:desyncNeg:1168268606614818968>',use=MAGIE,cooldown=7,description="Inflige des dégâts aux ennemis alentours puis, après trois tours, des dégâts en fonction de leurs PVs manquants")
periodStrikeEff = effect("Frappes Périodiques","periodStrikeEff", stat=MAGIE,power=40,type=TYPE_DAMAGE,trigger=TRIGGER_END_OF_TURN,turnInit=2,emoji='<:timeAttack:1226444587032383549>')
periodStrike = skill("Frappes Périodiques","",TYPE_DAMAGE,500,periodStrikeEff.power,AREA_CIRCLE_2,cooldown=5,replay=True,condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],emoji=periodStrikeEff.emoji[0][0],effects=periodStrikeEff,description="Inflige des dégâts à l'ennemi ciblé et vous permet de rejouer votre tour. Les dégâts sont répliquées lors de la fin des deux prochains tours de la cible",use=MAGIE)
cancelingEff = effect("Annulation","cancellingEff", stat=MISSING_HP,power=50,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_ON_REMOVE, emoji='<:annulation:1228790811278311474>')
canceling = skill("Annulation","",TYPE_INDIRECT_HEAL,750,cooldown=7,initCooldown=3,use=FIXE,effects=cancelingEff, emoji='<:annulation:1228790811278311474>',range=AREA_CIRCLE_3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],description="Lors de votre prochain tour, soigne la ciblé de la moitié de ses PVs manquants")

darkFlameEff1, darkFlameEff2 = effect("Flamme Sombre","darkFlammeEff", stat=MAGIE,power=20,turnInit=3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji='<:darkFlame:1228795277490655313>'), copy.deepcopy(incurable)
darkFlameEff2.power, darkFlameEff2.turnInit = 20, darkFlameEff1.turnInit
darkFlamme = skill("Flamme Sombre","",TYPE_DAMAGE,500,80,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS],effects=[darkFlameEff1,darkFlameEff2],use=MAGIE,emoji='<:darkFlame:1228795277490655313>',cooldown=5,description="Inflige des dégâts à l'ennemi cliblé puis lui inflige un effet de dégâts indirect et réduit les soins qu'il reçoit durant un petit moment")
darkThunder = skill("Foudre Sombre","",TYPE_DAMAGE,500,80,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS],emoji='<:darkThunder:1177705396639649863>',damageOnArmor=1.25,area=AREA_CIRCLE_1,use=MAGE,description="Inflige des dégâts augmentés contre l'armure aux ennemis ciblés",cooldown=5)
darkIce = skill("Glace Sombre","",TYPE_DAMAGE,500,100,condition=[EXCLUSIVE,ELEMENT,ELEMENT_DARKNESS],emoji='<:darkIce:1177705370102268024>',damageOnArmor=1.5,garCrit=True,cooldown=7,use=MAGIE,description="Inflige des dégâts critiques et augmentés contre l'armure à l'ennemi ciblé",quickDesc="Un stalactique de glace ombrale")

replacedSkills = [pyroSparkle,pyroCalcinate,pyroBlast,windCutter,windBlast,windZephir,spaceCrush,spacePulse,spaceComet,lightCross,lightPillar,lightFlash,"","","",bouncingWater,waterRang,waterBlast,rockStomp,rockSpike,rockBlast,descynNeg,periodStrike,canceling,darkFlamme,darkThunder,darkIce]

tablAdvBaseElemSkills = replacedSkills

tablAdvBaseElemSkillsId = getArrayAutoId(mysticShot.id,len(tablAdvBaseElemSkills),True)
for cmpt in range(len(tablAdvBaseElemSkills)):
    if type(tablAdvBaseElemSkills[cmpt]) != str:
        tablAdvBaseElemSkills[cmpt].id = tablAdvBaseElemSkillsId[cmpt]

for cmpt in range(len(lightPillar.become)):
    lightPillar.become[cmpt].id = lightPillar.id

for tmpSkill in tablAdvBaseElemSkills[:]:
    if type(tmpSkill) != skill:
        tablAdvBaseElemSkills.remove(tmpSkill)

spacePulse2.id = spacePulse1.id = spacePulse.id
spacePulse.iaPow = spacePulse.iaPow * 3

lowBlow = skill("Coup Bas","skk",TYPE_DAMAGE,750,power=45,range=AREA_CIRCLE_2,use=ENDURANCE,effects=lightStun,cooldown=5,maxPower=75,description="Inflige des dégâts et étourdi l'ennemi ciblé.\nLa puissance de la compétence est augmentée contre un boss Stand Alone, un boss de Raid ou certains ennemis",emoji='<:lowblow:1005127208412651591>')
legStrike = skill("Fauchage de Jambes",getAutoId(lowBlow.id,True),TYPE_DAMAGE,750,95,AREA_CIRCLE_2,effects=lightStun,cooldown=7,description="Inflige des dégâts à étourdi l'ennemi ciblé",emoji='<:legsStrike:1005127243401539645>')
provokeEff = effect("Provocation","voke",emoji='<:voke:1005127164749959178>',type=TYPE_MALUS,description="Augmente considérablement l'aggressivité du porteur envers l'entity à l'origine de cet effet")
provoke = skill("Provocation",getAutoId(legStrike.id,True),TYPE_MALUS,500,effects=provokeEff,cooldown=5,pull=4,range=AREA_CIRCLE_4,description="Augmente considérablement la probabilité d'être ciblé par l'adversaire désigné, et attire celui-ci vers vous et vous permet de rejouer votre tour",emoji=provokeEff.emoji[0][0],replay=True)

fanRevol_1 = skill("Pirouette Céleste",getAutoId(provoke.id,True),TYPE_DAMAGE,500,70,AREA_MONO,area=AREA_BIGDONUT,use=CHARISMA,cooldown=7,setAoEDamage=True,emoji='<:celestianFans:1003313557242388622>',effectAroundCaster=[TYPE_DAMAGE,AREA_DONUT_1,70],description="Inflige des dégâts à deux reprises aux ennemis alentours. Le premier coup utilise la {0} {1} et le second le {2} {3}".format(statsEmojis[STRENGTH],allStatsNames[STRENGTH],statsEmojis[CHARISMA],allStatsNames[CHARISMA]))
fanRevol_c = effect("Echaînement - {replicaName}","encFanRevol",replique=fanRevol_1)
fanRevol = skill("Pirouette Céleste",fanRevol_1.id,TYPE_DAMAGE,500,fanRevol_1.power,AREA_MONO,area=AREA_DONUT_1,cooldown=fanRevol_1.cooldown,description=fanRevol_1.description,setAoEDamage=True,emoji=fanRevol_1.emoji,effectAroundCaster=[TYPE_DAMAGE,AREA_BIGDONUT,70],effectOnSelf=fanRevol_c,replay=True)

demonLandEff1, demonLandEff2 = copy.deepcopy(dmgUp), copy.deepcopy(defenseUp)
demonLandEff1.power = demonLandEff2.power = 5
demonLandEff1.stat = demonLandEff2.stat = INTELLIGENCE
demonLandEff1.turnInit = demonLandEff2.turnInit = 3
demonLand = skill("Aura Démoniaque",getAutoId(fanRevol.id,True),TYPE_BOOST,500,cooldown=7,effects=[demonLandEff1,demonLandEff2],area=AREA_DONUT_3,range=AREA_MONO,group=SKILL_GROUP_DEMON,hpCost=20,emoji='<:dmonland:1006455391342829599>')
demonArmorEff = effect("Armure Démoniaque","demonArmor", stat=INTELLIGENCE,overhealth=70,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji='<:dmonArmor:1006455374464946226>')
demonArmor = skill("Armure Démoniaque",getAutoId(demonLand.id,True),TYPE_ARMOR,750,effects=demonArmorEff,cooldown=5,group=SKILL_GROUP_DEMON,hpCost=10,emoji='<:dmonArmor:1006455374464946226>')
demonArmorEff2 = effect("Armure Démoniaque Étendue","demonArmor2", stat=INTELLIGENCE,overhealth=50,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji='<:dmonArmor:1006455374464946226>')
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
        jaugeConds(INC_ALLY_KILLED,5),
        jaugeConds(INC_ENEMY_DAMAGED,10/100)
    ]
)

lemureDeepWound = copy.deepcopy(deepWound)
lemureDeepWound.stat, lemureDeepWound.power = STRENGTH, 20
noneLem = effect("Repos du Néan","noneLem",silent=True,turnInit=7,type=TYPE_MALUS,emoji='<:noneLem:1007588165512593431>',description="Empêche l'utilisation de Linceuil de Lémure durant sa durée")
comunioReady = effect("Linceuil de Lémure","comunioReady",turnInit=3,emoji='<:linc:1007583748491051058>')
comunio = skill("Communio",getAutoId(demonConst.id,True),TYPE_DAMAGE,power=125,area=AREA_CIRCLE_1,range=AREA_CIRCLE_3,emoji='<:comunio:1007583832947568740>',needEffect=comunioReady,effects=lemureDeepWound,effPowerPurcent=int(lemureDeepWound.power/50*100),effectFinisher=True)
soulFauchCroixReady = effect("Fauchage Croisé Préparé","soulFaucCroixReady",turnInit=3,emoji="<:faucheCroix:937807152058343474>")
soulFauchCroix = skill("Fauchage Croisé",comunio.id,TYPE_DAMAGE,power=100,range=AREA_CIRCLE_3,area=AREA_ARC_1,effects=lemureDeepWound,accuracy=99,emoji="<:faucheCroix:937807152058343474>",needEffect=soulFauchCroixReady)
soulFauchNeanReady = effect("Fauchage du Néan Préparé","soulFauchNean",turnInit=3,emoji='<:faucheNean:937807137306976337>')
soulFauchNean = skill("Fauchage du Néan",comunio.id,TYPE_DAMAGE,power=100,range=AREA_CIRCLE_3,area=AREA_ARC_1,effects=lemureDeepWound,accuracy=120,emoji="<:faucheNean:937807137306976337>",needEffect=soulFauchNeanReady,effectOnSelf=soulFauchCroixReady)
tranchNeanReady = effect("Tranchage du Néan préparé","trancNeanReady",turnInit=3,emoji='<:tranch:1007583800135524442>')
tranchNean = skill("Tranchage du Néan",comunio.id,TYPE_DAMAGE,cooldown=0,emoji='<:tranch:1007583800135524442>',effects=lemureDeepWound,range=AREA_CIRCLE_3,needEffect=tranchNeanReady,replay=True,tpCac=True,power=50,description="Saute au corps à corps de l'ennemi ciblé, lui inflige des dégâts et vous permet de rejouer votre tour")
lincEff = copy.deepcopy(dmgUp)
lincEff.power, lincEff.turnInit = 15, 3
linceuilLemure = skill("Linceuil de Lémure",comunio.id,TYPE_BOOST,range=AREA_MONO,url='https://media.discordapp.net/attachments/1003025632415973510/1007612026585092148/20220812_132659.gif',cooldown=0,area=AREA_MONO,emoji='<:linc:1007583748491051058>',effects=[lincEff,comunioReady,soulFauchNeanReady,tranchNeanReady,noneLem],rejectEffect=noneLem,jaugeEff=soulJauge,minJaugeValue=50,maxJaugeValue=50,description="Consomme une partie de votre jauge d'âme pour augmenter vos dégâts infligés de 10% pendant 3 tours et vous permet d'effectuer plusieurs nouvelles compétences sur la même durée",replay=True)
bundleLemure = skill("Linceuil de Lémure",linceuilLemure.id,TYPE_DAMAGE,750,url='https://media.discordapp.net/attachments/1003025632415973510/1007612026585092148/20220812_132659.gif',emoji='<:linc:1007583748491051058>',jaugeEff=soulJauge,power=comunio.power,become=[linceuilLemure,tranchNean,soulFauchNean,soulFauchCroix,comunio],description="Permet d'utiliser {0} __{1}__ en utilisant {2} pts de votre {3} __{4}__, augmentant vos dégâts infligés et vous permettant d'utiliser diverses compétences pendant 3 tours".format(linceuilLemure.emoji,linceuilLemure.name,linceuilLemure.minJaugeValue,linceuilLemure.jaugeEff.emoji[0][0],linceuilLemure.jaugeEff.name),minJaugeValue=linceuilLemure.minJaugeValue)
moissoneur = skill("Moissoneur d'Âmes",getAutoId(bundleLemure.id,True),TYPE_DAMAGE,500,100,range=AREA_MONO,emoji='<:soulMois:1007600776337694781>',area=AREA_CIRCLE_2,use=MAGIE,cooldown=5,jaugeEff=soulJauge,minJaugeValue=30,maxJaugeValue=50,maxPower=120)
corruptBecon = skill("Balise Corrompue",getAutoId(moissoneur.id,True),TYPE_DAMAGE,500,emoji='<:corruptBcon:1007601099622076486>',power=75,range=AREA_INLINE_5,area=AREA_LINE_5,jaugeEff=soulJauge,minJaugeValue=20,maxJaugeValue=75,maxPower=135,cooldown=5,use=MAGIE)
soulPendant = skill("Amulette d'Âmes",getAutoId(corruptBecon.id,True),TYPE_HEAL,500,use=CHARISMA,emoji='<:soulEater:1007600800576589884>',power=65,maxPower=80,jaugeEff=soulJauge,minJaugeValue=20,maxJaugeValue=50,cooldown=5)

potSuplReady = effect("Potence Suppliante Préparée","potSuplReady",turnInit=6,emoji='<:supPot:1007583690794221588>')
potSupl = skill("Potence Suppliante",getAutoId(soulPendant.id,True),TYPE_DAMAGE,range=AREA_CIRCLE_3,power=60,replay=True,needEffect=potSuplReady,emoji='<:supPot:1007583690794221588>',cooldown=3,jaugeEff=soulJauge,minJaugeValue=10,maxJaugeValue=10)
gibSuplReady = effect("Gibet Suppliant Préparé","gibSplReady",turnInit=6,emoji='<:supGibet:1007583627028221993>')
gibSupl = skill("Gibet Suppliant",potSupl.id,TYPE_DAMAGE,power=50,maxPower=75,replay=True,effects=lemureDeepWound,range=AREA_CIRCLE_3,needEffect=gibSuplReady,emoji='<:supGibet:1007583627028221993>',effectOnSelf=potSuplReady,cooldown=3,jaugeEff=soulJauge,minJaugeValue=10,maxJaugeValue=25)
fetuSang = skill("Fétu Sanglant",gibSupl.id,TYPE_DAMAGE,power=40,maxPower=60,replay=True,effects=lemureDeepWound,cooldown=3,range=AREA_CIRCLE_3,rejectEffect=[potSuplReady,gibSuplReady],effectOnSelf=gibSuplReady,emoji='<:fetu:1007583554319962112>',jaugeEff=soulJauge,minJaugeValue=10,maxJaugeValue=25)
bundleFetu = skill("Fétu Suppliant",gibSupl.id,TYPE_DAMAGE,500,potSupl.power,range=AREA_CIRCLE_3,emoji=fetuSang.emoji,become=[fetuSang,gibSupl,potSupl],description="Chaque compétence de Fétu Suppliant consomment **{0} pts** de votre {1} __{2}__ et permettent de rejouer votre tour après avoir infligé leurs dégâts".format(potSupl.minJaugeValue,soulJauge.emoji[0][0],soulJauge.name),jaugeEff=soulJauge,minJaugeValue=potSupl.minJaugeValue)
convictionVigilantEff = effect("Conviction du Vigilant","convVigil", stat=CHARISMA,power=25,type=TYPE_INDIRECT_HEAL,unclearable=True,turnInit=-1,description="Lorsque le porteur utilise son arme ou une compétence de dégâts directs, le soigne légèrement",emoji="<:regenVigil:982210651353137153>")
convictionVigilante = skill("Conviction du Vigilant",getAutoId(bundleFetu.id,True),TYPE_PASSIVE,500,effectOnSelf=convictionVigilantEff,emoji='<:regenVigil:982210651353137153>',quickDesc="Vous soigne légèrement lorsque vous utilisez une option offensive",condition=[EXCLUSIVE,ASPIRATION,VIGILANT])
convictionProtecArmor = effect("Armure","convicProAmor", stat=INTELLIGENCE,overhealth=25,stackable=True,lightShield=True,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
convicProEff = effect("Conviction du Protecteur","convicPro", stat=INTELLIGENCE,emoji='<:convicPro:1089710483990388756>',callOnTrigger=convictionProtecArmor,turnInit=-1,unclearable=True,description="Octroi une armure légère au porteur lorsque celui-ci utilise son arme ou une compétence de dégâts direct")
convicPro = skill("Conviction du Protecteur",getAutoId(convictionVigilante.id,True),TYPE_PASSIVE,price=500,effectOnSelf=convicProEff,emoji=convicProEff.emoji[0][0],condition=[EXCLUSIVE,ASPIRATION,PROTECTEUR],quickDesc="Vous octroi une armure quand vous utiliser votre arme ou une compétence offensive")
convictEnchtEff = effect("Conviction de l'Enchanteur","convVigil", stat=MAGIE,power=35,type=TYPE_INDIRECT_HEAL,unclearable=True,turnInit=-1,description="Lorsque le porteur utilise son arme ou une compétence de dégâts directs, le soigne légèrement",emoji="<:enchantConvic:1066018568136818759>")
convictEncht = skill("Conviction de l'Enchanteur",getAutoId(convicPro.id,True),TYPE_PASSIVE,500,effectOnSelf=convictEnchtEff,emoji='<:enchantConvic:1066018568136818759>',quickDesc="Vous soigne légèrement lorsque vous utilisez une option offensive",condition=[EXCLUSIVE,ASPIRATION,ENCHANTEUR])
convictTetEff = copy.deepcopy(convertEff)
convictTetEff.power, convictTetEff.stat, convictTetEff.emoji, convictTetEff.turnInit, convictTetEff.unclearable = 25, None, uniqueEmoji('<:tetebruleConvic:1066010806635995146>'), -1, True
convictTet = skill("Conviction du Tête Brulée",getAutoId(convictEncht.id,True),TYPE_PASSIVE,500,effectOnSelf=convictTetEff,emoji=convictTetEff.emoji[0][0],condition=[EXCLUSIVE,ASPIRATION,TETE_BRULEE],description="**{0}%** des dégâts infligés sont convertient en armure".format(convictTetEff.power))

miracle = skill("Miracle","sjh",TYPE_DAMAGE,500,power=80,cooldown=5,area=AREA_CIRCLE_3,range=AREA_MONO,emoji='<:holly:1009830417521713247>',effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_2,lightStun],condition=[EXCLUSIVE,ASPIRATION,MASCOTTE],description="Inflige des dégâts autour de vous et étourdit les ennemis en mêlée",use=CHARISMA,useActionStats=ACT_BOOST,group=SKILL_GROUP_HOLY)
celRivEff1, celRivEff2 = copy.deepcopy(dmgUp), copy.deepcopy(dmgDown)
celRivEff1.power, celRivEff2.power, celRivEff1.stat, celRivEff2.stat = 3, 3, INTELLIGENCE, INTELLIGENCE
celRivEff3, celRivEff4 = copy.deepcopy(celRivEff1), copy.deepcopy(celRivEff2)
celRivEff3.power, celRivEff4.power = 5, 5
celRivEff5, celRivEff6 = copy.deepcopy(celRivEff3), copy.deepcopy(celRivEff4)
celRivEff5.power, celRivEff6.power = 7, 7

celRivT1Ben = effect("Rivière Céleste (Bénéfique) 1","rivCelB1",trigger=TRIGGER_INSTANT,emoji="<:018327_hr1:1089724274706751561>",callOnTrigger=celRivEff5,area=AREA_CIRCLE_3)
celRivT2Ben = effect("Rivière Céleste (Bénéfique) 2","rivCelB2",trigger=TRIGGER_ON_REMOVE,emoji="<:018327_hr1:1089724274706751561>",callOnTrigger=celRivEff3,area=AREA_CIRCLE_3,turnInit=2)
celRivT3Ben = effect("Rivière Céleste (Bénéfique) 3","rivCelB3",trigger=TRIGGER_ON_REMOVE,emoji="<:018327_hr1:1089724274706751561>",callOnTrigger=celRivEff1,area=AREA_CIRCLE_3,turnInit=3)
celRivT1Nef = effect("Rivière Céleste (Néfaste) 1","rivCelN1",trigger=TRIGGER_INSTANT,emoji="<:018351_hr1:1089724201696501890>",callOnTrigger=celRivEff6,area=AREA_CIRCLE_3)
celRivT2Nef = effect("Rivière Céleste (Néfaste) 2","rivCelN2",trigger=TRIGGER_ON_REMOVE,emoji="<:018351_hr1:1089724201696501890>",callOnTrigger=celRivEff4,area=AREA_CIRCLE_3,turnInit=2)
celRivT3Nef = effect("Rivière Céleste (Néfaste) 3","rivCelN3",trigger=TRIGGER_ON_REMOVE,emoji="<:018351_hr1:1089724201696501890>",callOnTrigger=celRivEff2,area=AREA_CIRCLE_3,turnInit=3)

rivCel = skill("Rivière Céleste",getAutoId(miracle.id,True),TYPE_BOOST,750,effects=[celRivT1Ben,celRivT2Ben,celRivT3Ben,celRivT1Nef,celRivT2Nef,celRivT3Nef],range=AREA_MONO,area=AREA_MONO,cooldown=7,ultimate=True,condition=[EXCLUSIVE,ASPIRATION,MASCOTTE],description="Augmente les dégâts infligés par les alliés et diminue ceux infligés par les ennemis atour de vous. La puissance des bonus et malus diminue pendant 3 tours",emoji='<:rivCel:1009830456402923681>',url=astrodyn.url)
toxiconEff = copy.deepcopy(vulne)
toxiconEff.power, toxiconEff.stat = 5, INTELLIGENCE
toxiconEff3 = copy.deepcopy(toxiconEff)
toxiconEff3.power = toxiconEff3.power*0.4
toxiconEff2 = effect("Toxicon","toxicon",trigger=TRIGGER_INSTANT,area=AREA_DONUT_1,callOnTrigger=toxiconEff3,type=TYPE_MALUS,emoji='<:toxicon:1140219770428469400>')
toxicon = skill("Toxicon II", getAutoId(rivCel.id,True),TYPE_DAMAGE,500,power=50,area=AREA_CIRCLE_1,effects=[toxiconEff,toxiconEff2],garCrit=True,effBeforePow=True,cooldown=5,use=INTELLIGENCE,useActionStats=ACT_BOOST,condition=[EXCLUSIVE,ASPIRATION,INOVATEUR],description="Augmente les dégâts reçus par les ennemis ciblés puis leur inflige des dégâts. La cible principale reçoit forcément un coup critique et voit ses dégâts reçus augmenter encore plus",emoji='<:toxicon:1009830437012635779>')
seraphStrikeEff = copy.deepcopy(defenseUp)
seraphStrikeEff.power, seraphStrikeEff.stat, seraphStrikeEff.turnInit = 3.5, INTELLIGENCE, 3
seraphStrike = skill("Frappe Séraphique", getAutoId(toxicon.id,True),TYPE_DAMAGE,500,emoji='<:seraphStrike:1009830399352000562>',power=100,range=AREA_CIRCLE_3,tpCac=True,effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_3,seraphStrikeEff],cooldown=5,use=INTELLIGENCE,useActionStats=ACT_BOOST,condition=[EXCLUSIVE,ASPIRATION,MASCOTTE],description="Vous permet de sauter sur un ennemi en lui infligeant des dégâts, puis réduit les dégâts reçus par vous et vos alliés alentours pendant 3 tours")
sonarPaf = skill("Sonar Paf", getAutoId(seraphStrike.id,True), TYPE_SUMMON, 500, emoji='<:sonarPaf:1013747334825381938>', cooldown=7, invocation="Sonar Paf",range=AREA_CIRCLE_2, use=STRENGTH)
asile = skill("Asile", getAutoId(sonarPaf.id,True), TYPE_DEPL, 500, emoji='<:asile:1013753436300398672>', cooldown=7, depl=asileDepl,range=AREA_CIRCLE_3, use=CHARISMA)
bigBubbler = skill("Super-Bouclier", getAutoId(asile.id,True), TYPE_DEPL, 500, emoji='<:bigBubbler:1013747304475410522>', cooldown=7, depl=bigBubbleDepl,range=AREA_MONO, use=INTELLIGENCE)
lohicaBrouillad = skill("Brouillard Empoisonné", getAutoId(bigBubbler.id,True), TYPE_DEPL, 500, emoji="<:poisonusMist:1059084936100970556>",cooldown=7, depl=lohicaDepl, use=MAGIE,range=AREA_CIRCLE_3)
lacerTrap = skill("Piège de Lacération", getAutoId(lohicaBrouillad.id,True), TYPE_DEPL, 500, emoji=lacerTrapDepl.icon[0],cooldown=7, depl=lacerTrapDepl, use=STRENGTH ,range=AREA_CIRCLE_3)
tacticooler = skill("DistribuCool", getAutoId(lacerTrap.id,True),TYPE_SUMMON,500,cooldown=7,invocation="Distribucool",emoji="<:tacticooler:1014240041960231043>",range=AREA_CIRCLE_3,use=INTELLIGENCE,description="Invoque un {0} {1}. Les alliés proches de son point d'apparition voient leurs statistiques principales augmentés et une partie des dégâts reçus redirigé vers le {1}".format("<:tacticooler:1014240041960231043>","Distribucool"))
trizooka = skill("Lance-Rafales", getAutoId(tacticooler.id,True),TYPE_DAMAGE,500,power=55,percing=20,repetition=3,cooldown=7,emoji='<:triZooka:1014240959875256513>',area=AREA_CIRCLE_1,range=AREA_CIRCLE_4)
inkzooka = skill("Lance-Tornades", getAutoId(trizooka.id,True),TYPE_DAMAGE,500,power=55,percing=20,repetition=3,cooldown=7,emoji='<:inkZooka:1014240929374294137>',area=AREA_LINE_3,range=AREA_CIRCLE_4)
inkStrikeEff = effect("Missile-Tornade","inkStrike", stat=STRENGTH,power=120,area=AREA_CIRCLE_2,trigger=TRIGGER_ON_REMOVE,type=TYPE_INDIRECT_DAMAGE,emoji=sameSpeciesEmoji("<:tbMissile:1014242512443027496>","<:trMissile:1014242582185914398>"))
inkStrike = skill("Missile Tornade", getAutoId(inkzooka.id,True), TYPE_INDIRECT_DAMAGE, 500, effects=inkStrikeEff, cooldown=7, emoji='<:missileTornade:1014242376476282901>')
sacredSoil = skill("Dogme de Survie", getAutoId(inkStrike.id,True), TYPE_DEPL, 500, range=AREA_CIRCLE_3, cooldown=5, depl=dogmeDepl, use=INTELLIGENCE, emoji='<:sacredSoil:1014239981474168982>')
epidemicReject = copy.deepcopy(infection.reject[0])
epidemicReject.name, epidemicReject.id = epidemicReject.name.replace("Infection","Epidémie"), "epidemicReject"
epidemicEff = effect("Epidémie","epidemicEff", stat=MAGIE,power=infection.power,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN, reject=[epidemicReject], emoji='<:epidemic:1016787710666616902>')
epidemic = skill("Epidémie", getAutoId(sacredSoil.id,True), TYPE_INDIRECT_DAMAGE, 500, effects=epidemicEff, range=AREA_CIRCLE_4, emoji='<:epidemic:1016787710666616902>', cooldown=5, description="Inflige {0} __{1}__ à l'ennemi ciblé, lui infligeant des dégâts en début de tour et propageant l'effet à vos ennemis au corps à corps de lui avec une puissance réduite de **15%**\nUne cible infectée de peut plus subir l'effet {0} __{1}__ pendant **5 tours**".format(epidemicEff.emoji[0][0],epidemicEff.name))
intoxReject = copy.deepcopy(infection.reject[0])
intoxReject.name, intoxReject.id, intoxReject.turnInit = intoxReject.name.replace("Infection","Intoxication"), "intoxReject", 3
intoxEff = effect("Intoxication","intoxEff", stat=MAGIE,power=25,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN, reject=[intoxReject], emoji='<:intox:1016787678299177070>',strength=-3,magie=-3, replace=True)
intox = skill("Intoxication", getAutoId(epidemic.id,True), TYPE_INDIRECT_DAMAGE, 500, effects=intoxEff, range=AREA_CIRCLE_4, emoji='<:intox:1016787678299177070>', cooldown=5, description="Inflige {0} __{1}__ à l'ennemi ciblé, lui infligeant des dégâts en début de tour et propageant l'effet à vos ennemis au corps à corps de lui avec une puissance réduite de **15%**\nUne cible infectée de peut plus subir l'effet {0} __{1}__ pendant **3 tours**".format(intoxEff.emoji[0][0],intoxEff.name))
exploHealMarkEff = effect("Explosoins","exploHeal",turnInit=-1, unclearable=True, power=40, emoji='<:explosoins:1016796973636010026>', stat=HARMONIE, area=AREA_DONUT_2)
expoHeal = skill("Explosoins", getAutoId(intox.id,True), TYPE_PASSIVE, 500, effectOnSelf=exploHealMarkEff, use=HARMONIE, emoji='<:explosoins:1016796973636010026>', description = "Lorsqu'un ennemi est vaincu, tous vos effects de dégâts indirects soignent vos alliés à portée pour **{0}%** de leur puissance cumulée restante (maximum **{1}**) en utilisant la statistique d'Harmonie".format(exploHealMarkEff.power, 50), power= 50, quickDesc="Effectue des soins harmoniques autours des ennemis lorsqu'ils sont vaincu en portant vos effets de dégâts indirects")
ultraSignalEffect = effect("Ciblé - Ultra Signal","ultraTargeted", stat=STRENGTH,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_ON_REMOVE,area=AREA_CIRCLE_1, power=70, emoji=sameSpeciesEmoji("<:ultraB3:1105108367023816857>","<:ultraR3:1105108390658707507>"))
ultraSignalLauch = skill("Ultra-Signal",getAutoId(expoHeal.id,True), TYPE_INDIRECT_DAMAGE, 500, effects=ultraSignalEffect, cooldown=7, area=AREA_CIRCLE_3, ultimate=True, emoji='<:ultrasignal:1020048149055815900>',minTargetRequired=3)
ultraSignalCast = effect("Cast - {replicaName}", "castUltraSignal", turnInit=2, silent=True, replique = ultraSignalLauch,emoji=[["<:ultraB1:1105108256050905189>","<:ultraR1:1105108319489761310>"],["<:ultraB2:1105108287822766191>","<:ultraR2:1105108343363747901>"],["<:ultraB2:1105108287822766191>","<:ultraR2:1105108343363747901>"]])
ultraSignal = copy.deepcopy(ultraSignalLauch)
ultraSignal.effects, ultraSignal.effectOnSelf = [None], ultraSignalCast
forestShield = effect("Protection Sylvestre","forestShield",type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,stat=INTELLIGENCE,overhealth=50,emoji='<:gardeSilvestre:1023609768427925594>')
forestGarde = skill("Protection Silvestre",getAutoId(ultraSignal.id,True),TYPE_HEAL,500,power=forestShield.overhealth,cooldown=5,use=INTELLIGENCE,useActionStats=ACT_SHIELD,effects=forestShield,emoji='<:gardeSilvestre:1023609768427925594>',description="Soigne l'allié ciblé et lui octroi une armure avec la même puissance")
lillyTrasformHeal = effect("Bénédiction Sylvestre","lillyTransformHeal", stat=CHARISMA,power=25,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji='<:lilly:1023609807720161351>')
lillyTransformSelf = copy.deepcopy(healDoneBonus)
lillyTransformSelf.power, lillyTransformSelf.turnInit = 20, 3
lillyTransform = skill("Appel de la Chouette",getAutoId(forestGarde.id,True), TYPE_INDIRECT_HEAL, 500, effects=lillyTrasformHeal, effectOnSelf=lillyTransformSelf, cooldown=7, emoji='<:lilly:1023609807720161351>', description="Applique un effet de récupération sur l'allié ciblé pendant 3 tours et augmente de **{0}%** vos soins réalisé sur la même durée".format(lillyTransformSelf.power))
mendRegen = effect("Remède Sylvestre","mendRegen", stat=CHARISMA,power=20,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji="<:mend:1023609835981389854>")
mend = skill("Remède Sylvestre",getAutoId(lillyTransform.id,True),TYPE_HEAL,500,60,effects=mendRegen,cooldown=5,description="Soigne l'allié ciblé et lui octroi un effet régénérant durant 3 tours",emoji=mendRegen.emoji[0][0])
constBenEff = copy.deepcopy(constEff)
constBenEff.power, constBenEff.stat, constBenEff.turnInit = 20, PURCENTAGE, 3
constBen = skill("Constitution Divine",getAutoId(mend.id,True),TYPE_HEAL,750,effects=constBenEff,power=70,cooldown=7,maxHpCost=10,group=SKILL_GROUP_HOLY,emoji='<:constDiv:1028679968944824351>',range=AREA_DONUT_4,description="Soigne un allié et augmente temporairement ses PV maximums")
antConstEff = copy.deepcopy(aconstEff)
antConstEff.power, antConstEff.stat, antConstEff.turnInit = 20, PURCENTAGE, 3
antConst = skill("Anticonstitution",getAutoId(constBen.id,True),TYPE_DAMAGE,750,power=120,range=AREA_CIRCLE_3,effects=antConstEff,cooldown=7,condition=[EXCLUSIVE,ASPIRATION,TETE_BRULEE],emoji='<:ConR:1028695463651717200>',erosion=50,description="Inflige des dégâts un ennemi et réduit temporairement ses PV Maximums")
lifeSeedEff = effect("Graine de Vie","lifeSeed", stat=CHARISMA,power=70,area=AREA_CIRCLE_1,emoji='<:lifeSeed:1028680000628596817>',trigger=TRIGGER_ON_REMOVE,type=TYPE_INDIRECT_HEAL,turnInit=3)
lifeSeed = skill("Graine de Vie",getAutoId(antConst.id,True),TYPE_HEAL,750,emoji='<:lifeSeed:1028680000628596817>',power=35,effects=lifeSeedEff,cooldown=7,description="Soigne un allié et place sur lui une Graine de Vie qui réalisera des soins en zone {0} tours plus tard ou si la cible reçoit des dégâts mortels".format(lifeSeedEff.turnInit))
asssasinateEff3 = effect("Assassinat","assasinateEff",type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,stat=MISSING_HP,power=35,emoji='<:laceration:1100428518401245194>')
assasinate = skill("Assassinat",getAutoId(lifeSeed.id,True),TYPE_DAMAGE,750,power=150,range=AREA_CIRCLE_2,tpCac=True,effects=[asssasinateEff3],cooldown=7,ultimate=True,erosion=100,emoji='<:assassination:1157411186514596002>',description="Inflige à l'ennemi ciblé de gros dégâts tout en réduisant ses PV Maximums. La cible subis des dégâts supplémentaires en fonction de ses PV manquants")
traqnardEff = effect("Vulnérabilité Indirecte","traqnardEff",inkResistance=-20,turnInit=3,type=TYPE_MALUS,description="Augmente les dégâts indirects reçus par le porteur",stackable=True)
physTraqnard = skill("Traqnard Physique",getAutoId(assasinate.id,True),TYPE_DAMAGE,500,cooldown=5,power=70,range=AREA_CIRCLE_1,knockback=2,effects=traqnardEff,description="Inflige des dégâts à l'ennemi ciblé, augmente les dégâts indirects qu'il reçoit et le repousse",emoji='<:traqD:1029819539497701437>')
fairyTraqnard = skill("Traqnard Féérique",getAutoId(physTraqnard.id,True),TYPE_DAMAGE,500,power=80,effects=traqnardEff,area=AREA_CIRCLE_1,useActionStats=ACT_INDIRECT,cooldown=5,use=MAGIE,emoji='<:traqFairy:1029819512213733498>')
blodTraqnard = skill("Traqnard Sanglant",getAutoId(fairyTraqnard.id,True),TYPE_DAMAGE,500,power=80,effects=traqnardEff,area=AREA_CIRCLE_1,useActionStats=ACT_INDIRECT,cooldown=5,emoji='<:tradBlood:1029819483390492763>')
carnageEff = copy.deepcopy(incurable)
carnageEff.power = 30
carnage = skill("Carnage",getAutoId(blodTraqnard.id,True),TYPE_DAMAGE,500,emoji='<:carnage:1030489266784059472>',range=AREA_MONO,area=AREA_CIRCLE_1,power=85,cooldown=5,effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_1,carnageEff],description="Inflige des dégâts aux ennemis à votre corps à corps et réduit les soins qu'ils reçoivent durant un tour")
dissi2Eff = effect("Dissimulation Ombrale","dissi2Eff",translucide=True,aggro=-30,description="Vous rend Translucide et réduit la probabilité d'être attaqué",emoji='<:dissi:1029816091020640346>')
UmbralTravel = skill("Voyage Ombral",getAutoId(carnage.id,True),TYPE_DAMAGE,500,power=85,garCrit=True,cooldown=5,tpBehind=True,range=AREA_DIST_5,effectOnSelf=dissi2Eff,description="Saute derrière l'ennemi ciblé tout en lui infligeant des dégâts et réduit votre propabilité d'être pris pour cible jusqu'à votre prochain tour",emoji='<:ombralTravel:1227306665133473815>')
silvArmorEff = effect("Armure Silvestre","silvArmor", stat=INTELLIGENCE,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,overhealth=80,inkResistance=10,emoji='<:vegeProtect:1028680031498674266>',turnInit=3)
silvArmorEff3 = effect("Armure Végétale","silvArmor2", stat=INTELLIGENCE,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,overhealth=silvArmorEff.overhealth*0.4,inkResistance=5,emoji='<:vegeProtect:1028680031498674266>',turnInit=3)
silvArmorEff2 = effect("Armure Végétale",'silvArmor3',trigger=TRIGGER_INSTANT,area=AREA_DONUT_1,callOnTrigger=silvArmorEff3)
silvArmor = skill("Armure Silvestre",getAutoId(UmbralTravel.id,True),TYPE_ARMOR,500,cooldown=7,effects=[silvArmorEff,silvArmorEff2],emoji='<:vegeProtect:1028680031498674266>',description="Octroi une puissance armure à l'allié ciblé. Les alliés autour recoivent une armure dans une moindre mesure")
ghostlyCircleArmor = effect("Armure fantômatique","ghostArmor", stat=INTELLIGENCE,overhealth=40,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
ghostlyCircle = skill("Cercle Fantômatique",getAutoId(silvArmor.id,True),TYPE_ARMOR,500,cooldown=5,range=AREA_MONO,area=AREA_CIRCLE_3,useActionStats=ACT_SHIELD,description="Octroi une armure au lanceur et ses alliés alentours tout en infligeant des dé^gats aux ennemis en mêlée",effectAroundCaster=[TYPE_DAMAGE,AREA_CIRCLE_2,50],setAoEDamage=True,effects=ghostlyCircleArmor,emoji='<:ghostlyCircle:1033016192081866783>',condition=[EXCLUSIVE,ASPIRATION,PROTECTEUR])
spectralFurie =  skill("Furie Spectrale",getAutoId(ghostlyCircle.id,True),TYPE_DAMAGE,500,cooldown=5,power=int(125/5),repetition=5,armorConvert=50,use=MAGIE,accuracy=90,condition=[EXCLUSIVE,ASPIRATION,ENCHANTEUR],emoji='<:spectralFury:1033016230333911080>',range=AREA_CIRCLE_2,description="Inflige des dégâts à plusieurs reprises sur l'ennemi ciblé et converti une partie des dégâts infligés en armure")
spectralCircle = skill("Cercle Spectral",getAutoId(spectralFurie.id,True),TYPE_DAMAGE,500,cooldown=5,power=85,armorConvert=30,use=MAGIE,condition=[EXCLUSIVE,ASPIRATION,ENCHANTEUR],accuracy=120,description="Inflige des dégâts aux ennemis alentours et convertie une partie des dégâts infligés en armure",range=AREA_MONO,area=AREA_CIRCLE_2,emoji='<:spectralCircle:1033016601584353300>')
immoArrow = skill("Flèche d'Immolation",getAutoId(spectralCircle.id,True),TYPE_DAMAGE,500,cooldown=5,emoji='<:imolArrow:1032288557286576138>',power=90,area=AREA_LINE_3,range=AREA_DIST_5,effects=physTraqnard.effects,description='Inflige des dégâts aux ennemis ciblés et augmente les dégâts indirects reçus par la cible principale',condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE])
exploArrow = skill("Flèche Explosive",getAutoId(immoArrow.id,True),TYPE_DAMAGE,500,cooldown=7,ultimate=True,power=180,range=AREA_DIST_5,area=AREA_CIRCLE_2,emoji='<:exploArrow:1032288726233124958>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE])
freezeArrow = skill("Flèche Gelante",getAutoId(exploArrow.id,True),TYPE_DAMAGE,500,cooldown=5,power=100,damageOnArmor=1.2,effects=chained,description="Inflige des dégâts à l'ennemi ciblé et l'immobilise pendant un tour",condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],emoji='<:imoArrow:1032288442433945721>',range=AREA_DIST_6)
freezeArrow2Eff = copy.deepcopy(vulne)
freezeArrow2Eff.power, freezeArrow2Eff.stat, freezeArrow2Eff.turnInit = 3.5, PRECISION, 3
freezeArrow2 = skill("Flèche Givrante",getAutoId(freezeArrow.id,True),TYPE_DAMAGE,500,cooldown=5,power=100,effects=freezeArrow2Eff,effBeforePow=True,description="Augmente les dégâts reçus de l'ennemi ciblé et lui inflige des dégâts",condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],emoji='<:iceFrag:1032288516069150720>',range=AREA_DIST_6)
ebranlement = skill("Ebranlement",getAutoId(freezeArrow2.id,True),TYPE_DAMAGE,500,cooldown=5,power=100,armorConvert=50,damageOnArmor=2,range=AREA_CIRCLE_2,description="Inflige des dégâts à l'ennemi ciblé et en convertie une partie en armure pour vous même.\nDégâts augmentés sur l'armure",emoji='<:fulgur:1032288871565754408>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH])
hearthFrac = skill("Fracture Terrestre",getAutoId(ebranlement.id,True),TYPE_DAMAGE,500,cooldown=5,power=80,effects=freezeArrow2Eff,range=AREA_CIRCLE_2,description="Augmente les dégâts reçus de l'ennemi ciblé et lui inflige des dégâts",condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],emoji='<:earthFrag:1032288813499818055>')
hourglassEff = effect("Sablier","hourglassEff", stat=MAGIE,power=80,trigger=TRIGGER_ON_REMOVE,type=TYPE_INDIRECT_DAMAGE,emoji='<:hourglass:1032288468786745487>',area=AREA_CIRCLE_1)
hourglass = skill("Sablier",getAutoId(hearthFrac.id,True),TYPE_INDIRECT_DAMAGE,500,cooldown=5,effects=hourglassEff,emoji='<:hourglass:1032288468786745487>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],description="Inflige des dégâts à la cible et aux ennemis alentours lors de votre prochain tour")
clockEff = effect("Horloge","clockEff", stat=MAGIE,power=110,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_ON_REMOVE,emoji='<:clock:1032288491247243296>')
clock = skill("Horloge",getAutoId(hourglass.id,True),TYPE_INDIRECT_DAMAGE,500,cooldown=5,effects=clockEff,emoji=clockEff.emoji[0][0],condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],description="Inflige des dégâts à la cible lors de votre prochain tour")
elipseTerrestre = skill("Elipse Terrestre",getAutoId(clock.id,True),TYPE_DAMAGE,500,cooldown=5,power=80,range=AREA_MONO,area=AREA_CIRCLE_2,armorConvert=40,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],emoji='<:elipTer:1034208837772779530>',description="Inflige des dégâts aux ennemis autour de vous et converti une partie des dégâts infligés en armure")
piedVolt = skill("Pied Voltige",getAutoId(elipseTerrestre.id,True),TYPE_DAMAGE,500,cooldown=5,power=120,garCrit=True,accuracy=80,range=AREA_CIRCLE_3,tpCac=True,knockback=2,description="Saute au corps à corps de la cible, lui inflige des dégâts et le repousse",emoji='<:piedVolt:1034208868068233348>')
retImpEff = copy.deepcopy(impactShield)
retImpEff.stat = STRENGTH
retourneImpactant = skill("Retourné Impactant",getAutoId(piedVolt.id,True),TYPE_DAMAGE,500,cooldown=5,power=100,range=AREA_CIRCLE_3,effectOnSelf=retImpEff,description="Inflige des dégâts à l'ennemi ciblé, vous fait reculer d'une case et vous octroi une armure",jumpBack=1,emoji='<:retPercu:1034210776703062057>')
dmonAgiEff = effect("Esquive Démoniaque","dmonAgiEff", stat=INTELLIGENCE,agility=5,dodge=15,counterOnDodge=35,emoji='<:dmnagi:1045691488161517609>',description="Augmente l'agilité, la probabilité d'esquive et celle d'effectuer une contre-attaque lors d'une esquive du porteur")
dmonAgi = skill("Esquive Démonaique",getAutoId(retourneImpactant.id,True),TYPE_BOOST,500,cooldown=5,effects=dmonAgiEff,emoji='<:esqDmon:1045612328588161074>',group=SKILL_GROUP_DEMON,hpCost=15,area=AREA_CIRCLE_2,description="Augmente l'agilité, la probabilité d'esquive ainsi que celle d'effectuer une contre-attaque lors d'une esquive des alliés ciblés")
dmonEndEff1 = effect("Blocage Démoniaque","dmonEnEff1", stat=INTELLIGENCE,endurance=5,block=35,emoji='<:dmnend:1045691545686392854>',description="Augmente l'endurance et la probabilité de bloquer une attaque du porteur")
dmonEndEff2 = copy.deepcopy(defenseUp)
dmonEndEff2.stat, dmonEndEff2.power = INTELLIGENCE, 3.5
dmonEnd = skill("Blocage Démoniaque",getAutoId(dmonAgi.id,True),TYPE_BOOST,500,cooldown=5,effects=[dmonEndEff1,dmonEndEff2],emoji='<:bloDmon:1045612358107672617>',description="Augmente l'endurance ainsi que la probabilité de bloquer une attaque tout en réduisant les dégâts subis par les alliés ciblés",area=AREA_CIRCLE_2,group=SKILL_GROUP_DEMON,hpCost=15)
dmonCritEff = effect("Critique Démoniaque","dmonCritEff", stat=INTELLIGENCE,precision=5,critical=2,critDmgUp=10,critHealUp=10,emoji='<:dmncrit:1045691517307719701>',description="Augmente la précision, le taux de critique ainsi que les dégâts et soins réalisés lors d'une action critique du lanceur")
dmonCrit = skill("Critique Démoniaque",getAutoId(dmonEnd.id,True),TYPE_BOOST,500,cooldown=5,effects=dmonCritEff,emoji='<:criDmon:1045612385588744223>',group=SKILL_GROUP_DEMON,hpCost=15,area=AREA_CIRCLE_2,description="Augmente la précision, le taux de critique ainsi que les dégâts et soins réalisés lors d'une action critique des alliés ciblés")
dmonDmgEff1 = effect("Dégât Démoniaque","dmonDmgEff1", stat=INTELLIGENCE,strength=3.5,magie=3.5,emoji='<:dmndmg:1045691580620755006>',description="Augmente la force et la magie du porteur")
dmonDmgEff2 = copy.deepcopy(dmgUp)
dmonDmgEff2.stat, dmonDmgEff2.power = dmonEndEff2.stat, dmonEndEff2.power
dmonDmg = skill("Dégât Démoniaque",getAutoId(dmonCrit.id,True),TYPE_BOOST,500,cooldown=5,effects=[dmonDmgEff1,dmonDmgEff2],emoji='<:dmgDmn:1045612421546528799>',description="Augmente la force, la magie et les dégâts infligés par les alliés ciblés",area=AREA_CIRCLE_2,group=SKILL_GROUP_DEMON,hpCost=15)
dmonReconst1Eff1 = copy.deepcopy(dmgUp)
dmonReconst1Eff1.stat, dmonReconst1Eff1.power = INTELLIGENCE, 6.5
dmonReconst1Eff2 = copy.deepcopy(convertEff)
dmonReconst1Eff2.stat, dmonReconst1Eff2.power = INTELLIGENCE, 20
dmonReconst1Eff3 = copy.deepcopy(vampirismeEff)
dmonReconst1Eff3.stat, dmonReconst1Eff3.power = dmonReconst1Eff2.stat, dmonReconst1Eff2.power
dmonReconstitution = skill("Reconstitution Démoniaque",getAutoId(dmonDmg.id,True),TYPE_BOOST,500,cooldown=5,effects=[dmonReconst1Eff1,dmonReconst1Eff2,dmonReconst1Eff3],emoji='<:dmnRec:1045690240632897658>',description="Augmente les dégâts infligés, le taux de vol de vie et le taux de convertion des dégâts infligés en armure de l'allié ciblé",range=AREA_DONUT_5,group=SKILL_GROUP_DEMON,hpCost=15)
dmonReconstitution2 = skill("Reconstitution Démoniaque Étendue",getAutoId(dmonReconstitution.id,True),TYPE_BOOST,500,cooldown=5,effects=[dmonReconst1Eff1,dmonReconst1Eff2,dmonReconst1Eff3],emoji='<:dmnRec:1045690240632897658>',effPowerPurcent=45,description="Augmente les dégâts infligés, le taux de vol de vie et le taux de convertion des dégâts infligés en armure des alliés ciblés",area=AREA_CIRCLE_2,group=SKILL_GROUP_DEMON,hpCost=15)
apexArrowEff1 = effect("Alpha Forte","apexAro1", stat=STRENGTH,strength=5,turnInit=4,emoji="<:songPhys:1046123900519587934>",description="Augmente votre Force en fonction de votre propre Force")
apexArrowEff2 = effect("Ballade du Mage","apexAro2", stat=CHARISMA,magie=5,turnInit=3,emoji="<:enharMag:1046122914400968735>",description="Augmente la Magie du porteur en fonction du Charisme du lanceur")
apexArrow = skill("Trait Alpha",getAutoId(dmonReconstitution2.id,True),TYPE_DAMAGE,750,110,range=AREA_DIST_6,area=AREA_LINE_3,cooldown=7,effectOnSelf=apexArrowEff1,effectAroundCaster=[TYPE_BOOST,AREA_DONUT_3,apexArrowEff2],description="Inflige des dégâts aux ennemis ciblés puis augmente votre propre Force en fonction de votre Force et la Magie de vos alliés alentours en fonction de votre Charisme",emoji="<:apexArrow:1046129746704093204>")
blastArrowEff2 = effect("Péon Martial","apexAro2", stat=CHARISMA,strength=5,turnInit=3,emoji="<:enharPhys:1046122887028932689>",description="Augmente la Force du porteur en fonction du Charisme du lanceur")
blastArrow = skill("Flèche Musicale",getAutoId(apexArrow.id,True),TYPE_DAMAGE,750,110,range=AREA_DIST_6,area=AREA_LINE_3,cooldown=7,effectOnSelf=apexArrowEff1,effectAroundCaster=[TYPE_BOOST,AREA_DONUT_3,blastArrowEff2],description="Inflige des dégâts aux ennemis ciblés puis augmente votre propre Force en fonction de votre Force et celle de vos alliés alentours en fonction de votre Charisme",emoji="<:blastArrow:1046129829583536230>")
enhardEff1 = effect("Marche Conquérante","enhar1", stat=MAGIE,magie=5,turnInit=4,emoji='<:songMag:1046123862712127538>',description="Augmente votre Magie en fonction de votre propre Magie")
enhardEff2 = effect("Péon Martial","enhar2", stat=INTELLIGENCE,strength=5,turnInit=3,emoji="<:enharPhys:1046122887028932689>",description="Augmente la Force du porteur en fonction de l'Intelligence du lanceur")
enhardissement = skill("Enhardissement",getAutoId(blastArrow.id,True),TYPE_DAMAGE,750,100,use=MAGIE,range=AREA_CIRCLE_6,area=AREA_CIRCLE_1,cooldown=7,effectOnSelf=enhardEff1,effectAroundCaster=[TYPE_BOOST,AREA_DONUT_3,enhardEff2],description="Inflige des dégâts aux ennemis ciblés puis augmente votre propre Magie en fonction de votre Magie et la Force de vos alliés alentours en fonction de votre Intelligence",emoji='<:enhardissement:1046129975662743692>')
manafication2 = effect("Ballade du Mage","manafication2", stat=INTELLIGENCE,magie=5,turnInit=3,emoji="<:enharMag:1046122914400968735>",description="Augmente la Magie du porteur en fonction de l'Intelligence du lanceur")
manafication = skill("Manafication",getAutoId(enhardissement.id,True),TYPE_DAMAGE,750,100,use=MAGIE,range=AREA_CIRCLE_6,area=AREA_CIRCLE_1,cooldown=7,effectOnSelf=enhardEff1,effectAroundCaster=[TYPE_BOOST,AREA_DONUT_3,manafication2],description="Inflige des dégâts aux ennemis ciblés puis augmente votre propre Magie en fonction de votre Magie et celle de vos alliés alentours en fonction de votre Intelligence",emoji='<:manafication:1046129876601667634>')

mageBaladEff = effect("Ballade du Mage","mageBaladEff", stat=CHARISMA,magie=5,turnInit=3,description="Augmente la magie du porteur en fonction du charisme du lanceur",emoji="<:songMag:1046123862712127538>")
mageBalad = skill("Ballade du Mage",getAutoId(manafication.id,True),TYPE_DAMAGE,500,power=100,emoji='<:mageBallad:1047197760253861959>',effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_3,mageBaladEff],description="Inflige des dégâts à l'ennemi ciblé et augmente votre Magie ainsi que celle de vos équipiers alentours",cooldown=7)
martialPeanEff = effect("Péan Martial","martialPeanEff", stat=CHARISMA,strength=5,turnInit=3,description="Augmente la force du porteur en fonction du charisme du lanceur",emoji="<:songPhys:1046123900519587934>")
martialPean = skill("Péan Martial",getAutoId(mageBalad.id,True),TYPE_DAMAGE,500,power=100,emoji='<:martialPean:1047197814834339871>',effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_3,martialPeanEff],description="Inflige des dégâts à l'ennemi ciblé et augmente votre Force ainsi que celle de vos équipiers alentours",cooldown=7)
vanderManuetEff = effect("Menuet du Vagabon","vanderManuetEff", stat=CHARISMA,strength=3,magie=3,turnInit=3,description="Augmente la force et la magie du porteur en fonction du charisme du lanceur",emoji="<:menuet:1047210617087467552>")
vanderManuet = skill("Menuet du Vagabon",getAutoId(martialPean.id,True),TYPE_DAMAGE,500,power=100,emoji='<:vangarMenuet:1047197725361455144>',effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_3,vanderManuetEff],description="Inflige des dégâts à l'ennemi ciblé et augmente votre Force et votre Magie ainsi que celles de vos équipiers alentours",cooldown=7)

heroicFantasySkills = [mageBalad,martialPean,vanderManuet,machDeFer]
heroicFantasySkillsId = []
for skilly in heroicFantasySkills:
    heroicFantasySkillsId.append(skilly.id)

heroicFantasyJauge = effect("Jauge Fantaisiste","heroicFantasyJauge",emoji='<:fantasy:1047197880257085561>',turnInit=-1,unclearable=True,description="__La jauge Fantaisite se remplie à deux occasions :__\n> - Lorsque vous commencez votre tour : +10\n> - Lorsque vous utilisez une des compétences cités ci-dessous : +10\n> ")
heroicFantasyJauge.jaugeValue = jaugeValue(
    emoji=[["<:musEL:1047184888052330496>","<:musEM:1047184918339387422>","<:musER:1047184944172105800>"],["<:musYL:1047184982122172506>","<:musYM:1047185039915499530>","<:musYR:1047185234967396382>"]],
    conds=[jaugeConds(INC_START_TURN,10),jaugeConds(INC_USE_SKILL,10,heroicFantasySkills)]
)
heroicFantasyEff1 = effect("Fantaisie Héroïque","heroicFantasyEff1", stat=CHARISMA,strength=12,magie=7,precision=5,charisma=5,description="Augmente plusieurs de vos statistiques en fonction de votre charisme\nLa puissance de ce bonus reste la même qu'importe la quantité de {0} {1} consommée".format(heroicFantasyJauge.emoji[0][0],heroicFantasyJauge.name),emoji='<:heroicFantasy:1047213807690334289>',turnInit=4)
heroicFantasyEff2 = effect("Fantaisie Orchestrale","heroicFantasyEff2", stat=CHARISMA,strength=15,magie=15,precision=10,intelligence=10,endurance=5,charisma=5,description="Augmente plusieurs statistiques du porteur en fonction du charisme du lanceur\nLa puissance de l'effet dépend de la quantité de {0} {1} consommée. Les statisitques affichés ici sont ceux de l'effet à sa puissance maximale".format(heroicFantasyJauge.emoji[0][0],heroicFantasyJauge.name),emoji='<:orchestralFantasy:1047213865387171931>',turnInit=3)
heroicFantasy = skill("Fantaisie Héroïque",getAutoId(vanderManuet.id,True),TYPE_BOOST,750,range=AREA_MONO,area=AREA_DONUT_5,minJaugeValue=50,maxJaugeValue=100,effects=heroicFantasyEff2,effectOnSelf=heroicFantasyEff1,ultimate=True,cooldown=3,emoji='<:fantasy:1047197880257085561>',description="Augmente grandement les statistiques de vos alliés alentours en fonction de votre {0} {1}, ainsi que vos propres statistiques indépendament de la dites jauge".format(heroicFantasyJauge.emoji[0][0],heroicFantasyJauge.name),jaugeEff=heroicFantasyJauge)
exploShotEff = effect("Tir Explosif","exploShotEff", stat=STRENGTH,power=50,trigger=TRIGGER_INSTANT,type=TYPE_DAMAGE,area=AREA_CIRCLE_1,emoji="<:exploShotEff:1049704001257619476>",description="Inflige des dégâts autour du porteur")
exploShot = skill("Tir Explosif",getAutoId(heroicFantasy.id,True),TYPE_DAMAGE,500,power=60,cooldown=5,percing=35,description="Inflige des dégâts à la cible puis provoque une explosion à sa position, infligeant des dégâts de zones supplémentaires",emoji='<:exploShot:1049703940738007050>',effects=exploShotEff)
stigmateEff = effect("Stigmate","stigmate", stat=MAGIE,type=TYPE_DAMAGE,trigger=TRIGGER_START_OF_TURN,turnInit=2,lvl=2,emoji='<:stigmates:1047198003435425873>',power=40,area=AREA_CIRCLE_1,description="Inflige des dégâts aux ennemis dans la zone d'effet au début du tour du porteur")
stigmateEff2 = copy.deepcopy(mageBaladEff)
stigmate = skill("Stigmate",getAutoId(exploShot.id,True),TYPE_DAMAGE,750,50,use=MAGIE,area=AREA_CIRCLE_1,effects=stigmateEff,cooldown=7,emoji=stigmateEff.emoji[0][0],effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_3,stigmateEff2],description="Inflige des dégâts aux ennemis ciblé avec un effet de réplique lors de vos deux prochains tours et augmente la Magie de vous même et vos alliés alentours")
stigmateEff2.description += "\n\nNon cumulable avec l'effet octroyé par {0} {1}".format(mageBalad.emoji,mageBalad.name)
mageBaladEff.description+= "\n\nNon cumulable avec l'effet octroyé par {0} {1}".format(stigmate.emoji,stigmate.name)
dissEff = effect("Dissonance","dissEff", stat=MAGIE,power=25,turnInit=3,lvl=3,type=TYPE_DAMAGE,trigger=TRIGGER_START_OF_TURN,area=AREA_CIRCLE_3,emoji='<:dissonance:1047197979674681374>',description="Inflige des dégâts aux ennemis dans la zone d'effet au début du tour du porteur")
dissEff2 = copy.deepcopy(martialPeanEff)
dissonance = skill("Dissonance",getAutoId(stigmate.id,True),TYPE_DAMAGE,750,40,use=MAGIE,area=AREA_CIRCLE_3,effects=dissEff,cooldown=7,emoji=dissEff.emoji[0][0],effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_3,dissEff2],description="Inflige des dégâts aux ennemis ciblé avec un effet de réplique lors de vos deux prochains tours et augmente la Force de vous même et vos alliés alentours")
dissEff2.description += "\n\nNon cumulable avec l'effet octroyé par {0} {1}".format(martialPean.emoji,martialPean.name)
martialPeanEff.description+= "\n\nNon cumulable avec l'effet octroyé par {0} {1}".format(dissonance.emoji,dissonance.name)
vibrSonEff = copy.deepcopy(vanderManuetEff)
vibrSon = skill("Vibration Sonique",getAutoId(dissonance.id,True),TYPE_DAMAGE,500,100,use=MAGIE,area=AREA_CIRCLE_1,emoji='<:vibrSon:1047197915355037716>',effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_3,vibrSonEff],cooldown=7,description="Inflige des dégâts aux ennemis ciblés et augmente votre Force et votre Magie ainsi que celles de vos équipiers alentours")
vibrSonEff.description += "\n\nNon cumulable avec l'effet octroyé par {0} {1}".format(vanderManuet.emoji,vanderManuet.name)
vanderManuetEff.description+= "\n\nNon cumulable avec l'effet octroyé par {0} {1}".format(vibrSon.emoji,vibrSon.name)

sernSkills = [stigmate,dissonance,vibrSon]
sernSkillsId = []
for skilly in sernSkills:
    sernSkillsId.append(skilly.id)

sernJauge = effect("Jauge de Sérénade","sernJauge",emoji='<:serenade:1047386802517971014>',turnInit=-1,unclearable=True)
sernJauge.jaugeValue = jaugeValue(
    emoji=[["<:musEL:1047184888052330496>","<:musEM:1047184918339387422>","<:musER:1047184944172105800>"],["<:musBL:1047185274364497971>","<:musBM:1047185299098304605>","<:musBR:1047185332434645052>"]],
    conds=[jaugeConds(INC_START_TURN,10),jaugeConds(INC_USE_SKILL,10,sernSkills)]
)
sernEff1 = effect("Sérénade du Courage","sernEff1", stat=CHARISMA,magie=12,strength=7,precision=5,charisma=5,description="Augmente plusieurs de vos statistiques en fonction de votre charisme\nLa puissance de ce bonus reste la même qu'importe la quantité de {0} {1} consommée".format(sernJauge.emoji[0][0],sernJauge.name),emoji='<:sern:1047213807690334289>',turnInit=4)
sernEff2 = effect("Sérénade de la Détermination","sernEff2", stat=CHARISMA,strength=15,magie=15,precision=10,intelligence=10,endurance=5,charisma=5,description="Augmente plusieurs statistiques du porteur en fonction du charisme du lanceur\nLa puissance de l'effet dépend de la quantité de {0} {1} consommée. Les statisitques affichés ici sont ceux de l'effet à sa puissance maximale".format(sernJauge.emoji[0][0],sernJauge.name),emoji='<:orchestralFantasy:1047213865387171931>',turnInit=3)
sernade = skill("Sérénade du Courage",getAutoId(vibrSon.id,True),TYPE_BOOST,750,range=AREA_MONO,area=AREA_DONUT_5,minJaugeValue=50,maxJaugeValue=100,effects=sernEff2,effectOnSelf=sernEff1,ultimate=True,cooldown=3,emoji='<:serenade:1047386802517971014>',description="Augmente grandement les statistiques de vos alliés alentours en fonction de votre {0} {1}, ainsi que vos propres statistiques indépendament de la dites jauge".format(sernJauge.emoji[0][0],sernJauge.name),jaugeEff=sernJauge,use=MAGIE)
thunderFiole = skill("Fiole de Foudre",getAutoId(sernade.id,True),TYPE_DAMAGE,500,cooldown=5,power=70,effectAroundCaster=[TYPE_DAMAGE,AREA_RANDOMENNEMI_3,35],setAoEDamage=True,use=MAGIE,emoji='<:thunderFiole:1049717778397020173>',description="Inflige des dégâts à l'ennemi ciblé puis de nouveaux dégâts à trois ennemis aléatoires")
deterStrike = skill("Frappe Déterminée",getAutoId(thunderFiole.id,True),TYPE_DAMAGE,500,power=100,range=AREA_CIRCLE_2,emoji='<:deterStrike:1049709129591173240>',cooldown=5,lifeSteal=35,percing=25,condition=[EXCLUSIVE,ASPIRATION,TETE_BRULEE],description="Consomme vos PAr pour délivrer une attaque à cible unique qui vous soigne d'une partie des dégâts infligés.\nLa cible subis des dégâts fixes supplémentaires en fonction de la quantité de PAr consommés")
umbraMortis = skill("Umbra Mortis",getAutoId(deterStrike.id,True),TYPE_DAMAGE,500,deathShadow.power,cooldown=deathShadow.cooldown,emoji='<:morsDamnationem:1050066734243123282>',effects=deathShadow.effects,use=MAGIE,description="Augmente les dégâts que vous infligez à l'ennemi ciblé puis lui délivre une attaque.\nSi la cible meurt dans les tours qui suivent, vous régénérez une partie de vos PV",effBeforePow=True)
morsDamnationemExitiumReady = effect("Mors Damnationem Préparé","clemBloodDmonFinal",turnInit=4,silent=True,emoji='<:sanguisDaemonium:1050059965630533714>')
morsDamnationem = skill("Mors Damnationem",getAutoId(umbraMortis.id,True),TYPE_DAMAGE,power=150,area=AREA_CIRCLE_1,emoji='<:sanguisDaemonium:1050059965630533714>',needEffect=morsDamnationemExitiumReady,use=MAGIE,hpCost=10,group=SKILL_GROUP_DEMON)
sanguisCrucisReady = effect("Sanguis Crucis Préparé","sanguisCrucisReady",silent=True,turnInit=4,emoji='<:sangDae1:1050414458029228142>')
sanguisCrucis = skill("Sanguis Crucis",morsDamnationem.id,TYPE_DAMAGE,power=110,area=AREA_INLINE_3,emoji='<:sangDae1:1050414458029228142>',needEffect=sanguisCrucisReady,use=MAGIE,hpCost=10,group=SKILL_GROUP_DEMON)
sanguinumVerriteReady = effect("Sanguinum Verrite Préparé","sanguinumVerriteReady",silent=True,turnInit=4,emoji='<:sangDae2:1050414522541813812>')
sanguinumVerrite = skill("Sanguinum Verrite",morsDamnationem.id,TYPE_DAMAGE,power=125,area=AREA_ARC_2,emoji='<:sangDae2:1050414522541813812>',needEffect=sanguinumVerriteReady,use=MAGIE,hpCost=10,group=SKILL_GROUP_DEMON)
bloodDemonnt = effect("Epuissement Sanguin","bloodDmnn't",silent=True,turnInit=7,type=TYPE_MALUS)
bloodDemonEff = copy.deepcopy(linceuilLemure.effects[0])
cruentumOffendasEff = effect("Cruentum Offendas","cruentumOffendasEff", stat=MAGIE,power=30,lvl=5,turnInit=3,emoji="<:cruentumOffendas:1053666959377567794>",description="Lorsque le porteur effectue une attaque, inflige des dégâts supplémentaires à la cible principale si cette dernière est un ennemi",trigger=TRIGGER_DAMAGE,afterchocEff=True,type=TYPE_DAMAGE)
bloodDemon = skill("Sanguis Daemonium",morsDamnationem.id,TYPE_BOOST,range=AREA_MONO,effects=[bloodDemonEff,cruentumOffendasEff,sanguinumVerriteReady,sanguisCrucisReady,morsDamnationemExitiumReady],emoji=morsDamnationemExitiumReady.emoji[0][0],description="Augmente grandement vos dégâts infligés pendant vos trois prochain tour et vous donne accès à de puissantes compétences durant cette période en consommant une grande partie de votre Jauge de Sang\nCette compétence devient inutilisable durant sept tour après utilisation.\nChaque compétence vous retire 10% de vos PV actuels",jaugeEff=bloodJauge,minJaugeValue=50,maxJaugeValue=50,rejectEffect=[bloodDemonnt],hpCost=10,group=SKILL_GROUP_DEMON,replay=True)
bloodDemonBundle = skill("Démon de Sang",morsDamnationem.id,TYPE_DAMAGE,750,become=[bloodDemon,sanguinumVerrite,sanguisCrucis,morsDamnationem],emoji=bloodDemon.emoji,description=bloodDemon.description,jaugeEff=bloodDemon.jaugeEff,minJaugeValue=bloodDemon.minJaugeValue,group=SKILL_GROUP_DEMON)
phenixDanceEff = copy.deepcopy(phoenixFlight)
phenixDanceEff.stat = STRENGTH
phenixDance = skill("Danse du Phénix",getAutoId(bloodDemonBundle.id,True),TYPE_DAMAGE,500,110,AREA_CIRCLE_2,cooldown=galvanisation.cooldown,emoji='<:phenixDance:1065647282046898176>',effectAroundCaster=[TYPE_INDIRECT_HEAL,galvanisation.effectAroundCaster[1],phenixDanceEff],description="Inflige des dégâts à la cible et octroi un effet de rénégération à vous-même et vos alliés proches")
phalaxEff = copy.deepcopy(defenseUp)
phalaxEff.stat, phalaxEff.power = INTELLIGENCE, 12
phalax = skill("Phalax",getAutoId(phenixDance.id,True),TYPE_BOOST,750,effects=phalaxEff,range=AREA_MONO,area=AREA_DONUT_3,cooldown=7,emoji='<:phalax:1051958917393035375>',condition=[EXCLUSIVE,ASPIRATION,MASCOTTE],effectOnSelf=invincibleEff,description="Réduit grandement les dégâts reçus par vos alliés alentours et vous rend invulnérable durant un tour",ultimate=True)
tacShieldEff = effect("Bouclier Tactique","tacShield", stat=INTELLIGENCE,resistance=7,aggro=25,block=30,emoji='<:tacticShield:1051958651801325568>',turnInit=3,description="Augmente votre résistance, la probabilité d'être ciblé par vos ennemis et celle de bloquer leurs attaques")
tacShiledEff2 = effect("Protection Tactique","protectTack",aggro=-20,description="Réduit la probabilité du porteur d'être ciblé par ses ennemis",turnInit=tacShieldEff.turnInit)
tacShield = skill("Bouclier Tactique",getAutoId(phalax.id,True),TYPE_BOOST,500,effects=tacShieldEff,range=AREA_MONO,effectAroundCaster=[TYPE_BOOST,AREA_DONUT_3,tacShiledEff2],emoji=tacShieldEff.emoji[0][0],cooldown=7,description="Augmente votre résistance, votre taux de blocage et attire plus facilement les attaque sur vous tout en réduisant les chances de vos alliés d'être ciblés par vos ennemis",condition=[EXCLUSIVE,ASPIRATION,MASCOTTE])
dislocationEff = copy.deepcopy(vulne)
dislocationEff.power, dislocationEff.turnInit = 15, 3
dislocation = skill("Dislocation",getAutoId(tacShield.id,True),TYPE_DAMAGE,500,95,area=AREA_CIRCLE_1,emoji='<:dislocation:1052697663402950667>',cooldown=5,condition=[EXCLUSIVE,ASPIRATION,MAGE],description="Augmente les dégâts subis par la cible durant un touret lui inflige des dégâts, à lui et aux ennemis alentours",effBeforePow=True,effects=dislocationEff,use=MAGIE)
rubyBraser = skill("Brasier Rubis",getAutoId(dislocation.id,True),TYPE_DAMAGE,power=135,area=AREA_CIRCLE_2,emoji='<:rubyBrasero:1052698751715778631>',cooldown=6,use=MAGIE,description="Inflige des dégâts aux ennemis ciblés, puis au tour suivant effectue une attaque avec une puissance et un air d'effet augmentés",condition=[EXCLUSIVE,ASPIRATION,MAGE])
rubyBraser_c = effect("Cast - {replicaName}","castRubyBraser",turnInit=2,replique=rubyBraser)
rubyLight = skill("Lueur Rubis",rubyBraser.id,TYPE_DAMAGE,500,100,area=AREA_CIRCLE_1,description=rubyBraser.description,use=MAGIE,cooldown=rubyBraser.cooldown+1,emoji='<:rubyLight:1052698664650416158>',effectOnSelf=rubyBraser_c)
anticipationEff1, anticipationEff2 = copy.deepcopy(defenseUp), effect("Anticipation","anticipEff2",emoji='<:anticipation:1052700207407710278>',description="Jusqu'à votre prochain tour, si vous êtes touché par une compétence élementaire, vous octroi l'effet élémentaire correspondant à votre élément et remplie votre Jauge de 5 points, qu'importe la jauge",callOnTrigger=elemEff,trigger=TRIGGER_AFTER_DAMAGE)
anticipationEff1.power, anticipationEff1.stat = 8.5, MAGIE
anticipation = skill("Anticipation",getAutoId(rubyLight.id,True),TYPE_BOOST,500,range=AREA_MONO,useActionStats=ACT_DIRECT,effects=[anticipationEff1,anticipationEff2],emoji=anticipationEff2.emoji[0][0],condition=[EXCLUSIVE,ASPIRATION,MAGE],description="Jusqu'à votre prochain tour, réduit les dégâts que vous subissez. De plus, si vous êtes touché par une compétence élémentaire, vous octroi l'effet élémentaire correspondant à votre élément et remplie de 5 points la valeur de votre jauge équipée",cooldown=5)
redRumEff2 = copy.deepcopy(armorGetMalus)
redRumEff2.power = 30
redrum = skill("Redrum",getAutoId(anticipation.id,True),TYPE_DAMAGE,500,power=125,range=AREA_CIRCLE_1,cooldown=7,emoji='<:redrum:1053222163819286618>',damageOnArmor=1.5,effects=[incur[3],redRumEff2],description="Inflige des dégâts (augmentés de 50% sur des armures) à l'ennemi ciblé et réduit de 40% les soins qu'elle reçoit durant un tour")
interEff1, interEff2 = copy.deepcopy(heartStoneSecEff), copy.deepcopy(heartStoneSecEff2)
interEff1.stat = interEff2.stat = CHARISMA
intervantion = skill("Intervention",getAutoId(redrum.id,True),TYPE_INDIRECT_HEAL,heartStone.price,cooldown=heartStone.cooldown,effects=[holyShieltronEff2,interEff1,interEff2],condition=[EXCLUSIVE,ASPIRATION,VIGILANT],emoji='<:inter:1053655537604120586>',replay=True,description="Octroi à l'allié ciblé un effet de régénération et réduit ses dégâts subis dourant trois tour tout en vous permettant de rejouer votre tour. L'effet de réduction de dégâts est doublé durant le premier tour",range=AREA_DONUT_5)
intuitionFougEff1, intuitionFougEff2, intuitionFougEff3 = copy.deepcopy(vampirismeEff), effect("Digue au sang","bloodBarr", stat=STRENGTH,overhealth=35,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji='<:digueAuSang:1053659293875978280>',turnInit=3), copy.deepcopy(interEff2)
intuitionFougEff1.power, intuitionFougEff1.stat, intuitionFougEff1.turnInit = 10, STRENGTH, 3
intuitionFougEff3.stat = STRENGTH
intuitionFoug = skill("Intuition Fougueuse",getAutoId(intervantion.id,True),TYPE_INDIRECT_HEAL,750,range=AREA_MONO,effects=[intuitionFougEff1,intuitionFougEff2,intuitionFougEff3],cooldown=heartStone.cooldown,emoji='<:barageSang:1053655508894109796>',condition=[EXCLUSIVE,ASPIRATION,BERSERK],description="Vous octroi un taux de vol de vie et une petite armure durant 3 tours et vous permet de rejouer votre tour. Réduit également les dégâts que vous subissez jusqu'à votre prochain tour",replay=True)
dreamInADream = skill("Rêve dans un rêve",getAutoId(intuitionFoug.id,True),TYPE_DAMAGE,500,power=25,repetition=3,cooldown=5,emoji='<:dreamWithinADream:1053655563193561138>',condition=[EXCLUSIVE,ASPIRATION,POIDS_PLUME],description="Inflige à trois reprises des dégâts à l'ennemi ciblé et vous permet de rejouer votre tour",replay=True)
bunshinEffTrig = effect("Bunshin","bunshinEffTrig", stat=STRENGTH,type=TYPE_DAMAGE,power=35,trigger=TRIGGER_INSTANT,emoji="<:Bunshi:1053655586161565726>")
bunshinEff = effect("Bunshin","bunshinEff", stat=STRENGTH,lvl=5,turnInit=3,emoji=bunshinEffTrig.emoji,description="Lorsque le porteur effectue une attaque, inflige des dégâts supplémentaires à la cible principale si cette dernière est un ennemi",callOnTrigger=bunshinEffTrig,onDeclancher=True)
bunshin = skill("Bunshin",getAutoId(dreamInADream.id,True),TYPE_BOOST,500,range=AREA_MONO,replay=True,effects=bunshinEff,condition=[EXCLUSIVE,ASPIRATION,POIDS_PLUME],cooldown=5,emoji=bunshinEff.emoji[0][0],description="Lors de vos **{0}** prochaines attaques, vous infligerez des dégâts supplémentaires".format(bunshinEff.lvl))
regenEarthEff = effect("Coeur Régénérant","regenEarthEff", stat=CHARISMA,power=35,stackable=True,lvl=3,turnInit=3,emoji='<:regenHeart:1053223398697865227>',trigger=TRIGGER_AFTER_DAMAGE,type=TYPE_INDIRECT_HEAL,description="Soigne le porteur lorsqu'il reçoit des dégâts directs")
astraRegenPhaseEff2 = effect("Déphasé","astraDeohase",emoji='<:timeDissimulation:1053326688450256926>',untargetable=True)
astraRegenPhase = skill("Phase Régénératrice",getAutoId(bunshin.id,True),TYPE_INDIRECT_HEAL,750,cooldown=5,effects=regenEarthEff,range=AREA_MONO,area=AREA_DONUT_3,effPowerPurcent=75,effectOnSelf=astraRegenPhaseEff2,emoji='<:healingPhase:1047986775387291830>',description="Octroi un effet régénérant aux alliés alentours, les soignants lorsqu'ils prennent des attaques, et réduit votre probabilité d'être ciblés par vos ennemis",condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME])
astraIncurStrikeEff = copy.deepcopy(incurable)
astraIncurStrikeEff.power, astraIncurStrikeEff.turnInit = 25, 3
astraIncurStrikeEff2 = effect("Fragilité","astraIncurStrike", stat=PURCENTAGE,type=TYPE_MALUS,resistance=-25,turnInit=3)
astraIncurStrike = skill("Attaque Contre-Nature",getAutoId(astraRegenPhase.id,True),TYPE_DAMAGE,500,power=100,range=AREA_CIRCLE_3,tpCac=True,effects=[astraIncurStrikeEff,astraIncurStrikeEff2],effBeforePow=True,effectOnSelf=regenEarthEff,emoji='<:incurStrike:1049717644003131412>',cooldown=5,selfEffPurcent=85,use=CHARISMA,useActionStats=ACT_HEAL,description="Saute au corps à corps de l'ennemi ciblé, lui inflige des dégâts, réduit les soins qu'il reçoit et sa résistance pendant un moment et vous octroi un effet régénérant vous soignant lorsque vous prenez des dégâts directs")
astraRegenEarthEff = copy.deepcopy(regenEarthEff)
astraRegenEarthEff.lvl = 5
astraRegenEarth = skill("Coeur de Compassion",getAutoId(astraIncurStrike.id,True),TYPE_INDIRECT_HEAL,500,effects=[regenEarthEff],effectOnSelf=astraRegenEarthEff,effPowerPurcent=75,selfEffPurcent=100,area=AREA_DONUT_3,range=AREA_MONO,emoji='<:timeHeart:1047986742571044895>',cooldown=7,condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],description="Vous octroi à vous et vos alliés proches un effet régénérant vous soignant lorsque vous subissez des dégâts directs. L'effet sur vous-même est plus puissant et peut se déclancher plus de fois")
florChaotEff = effect("Floraison Chaotique","florChaosEff", stat=STRENGTH,power=25,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji='<:florChao:1053721494099873802>',description="Inflige des dégâts au début du tour du porteur")
florChaot = skill("Floraison Chaotique",getAutoId(astraRegenEarth.id,True),TYPE_DAMAGE,500,125,knockback=2,range=AREA_CIRCLE_2,effects=florChaotEff,cooldown=7,emoji='<:florChaos:1053655611516133397>',description="Inflige des dégâts à l'ennemi ciblé ainsi qu'un effet de dégâts sur la durée et le repousse de 3 cases",condition=[EXCLUSIVE,ASPIRATION,POIDS_PLUME])

inercieJauge = effect("Jauge d'Inercie","inercyJauge",turnInit=-1, unclearable=True, emoji='<:inercie:1058338643707695155>', 
    jaugeValue= jaugeValue(
        emoji = [["<:inLE:1058337002472345610>","<:inME:1058337036362321972>","<:inRE:1058337067962220635>"],["<:inLF:1058337108307230751>","<:inMF:1058337140515295252>","<:inRF:1058337174417854485>"]],
        conds = [
            jaugeConds(INC_START_TURN,2),
            jaugeConds(INC_JUMP_PER_CASE,5),
            jaugeConds(INC_PER_PUSH,10),
            jaugeConds(INC_JUMP_BACK,15),
            jaugeConds(INC_COLISION,10)
        ]
    ))

tripleChoc_2 = skill('Triple Impact',getAutoId(florChaot.id,True)+"_2",TYPE_DAMAGE,750,power=60,accuracy=180,cooldown=7,ultimate=True,affSkillMsg=False,tpCac=True,range=AREA_CIRCLE_3,area=AREA_CIRCLE_2,maxPower=120,minJaugeValue=1,maxJaugeValue=100,emoji='<:chainChoc3:1058339138383908925>',jumpBack=2,description="Inflige à trois reprises des dégâts à l\'ennemi ciblé. Le dernier coup inflige des dégâts de zone\nLa première et troisième attaque vous rapprochent de l'adversaire\nLa seconde le repousse de deux cases\nLa troisème vous fait reculer de deux cases\n\nSeul 25 points de votre {0} {1} sont nessaires pour utliser cette compétence, mais elle atteint sa puissance maximale avec 100 points".format(inercieJauge.emoji[0][0],inercieJauge.name),jaugeEff=inercieJauge)
tripleChoc_2_c = effect("Enchaînement - Triple Impact","tripleChoc_c2",silent=True,replique=tripleChoc_2)
tripleChoc_1 = copy.deepcopy(tripleChoc_2)
tripleChoc_1.id, tripleChoc_1.power, tripleChoc_1.area, tripleChoc_1.knockback, tripleChoc_1.jumpBack, tripleChoc_1.maxPower, tripleChoc_1.replay, tripleChoc_1.effectOnSelf, tripleChoc_1.emoji = tripleChoc_2.id.replace('_2','_1'),60,AREA_MONO,2,0,100, True, tripleChoc_2_c, "<:chainChoc2:1058339104900796468>"
tripleChoc_1_c = effect("Enchaînement - Triple Impact","tripleChoc_c1",silent=True,replique=tripleChoc_1)
tripleChoc = copy.deepcopy(tripleChoc_2)
tripleChoc.id, tripleChoc.power, tripleChoc.area, tripleChoc.jumpBack, tripleChoc.maxPower, tripleChoc.replay, tripleChoc.effectOnSelf, tripleChoc.emoji, tripleChoc.minJaugeValue, tripleChoc.maxJaugeValue , tripleChoc.affSkillMsg = tripleChoc_2.id.replace("_2",""), 60, AREA_ARC_1, 0, 80, True, tripleChoc_1_c, "<:chainChoc1:1058339074563379240>", 25, 100, True

corruptusArea = skill("Déployable - Zone Corrompue",getAutoId(tripleChoc.id,True),TYPE_DEPL,750,depl=corruptusAreaDepl,emoji="<:fa:1014081850257444874>",cooldown=7,group=SKILL_GROUP_DEMON,hpCost=15,description="Pose une zone au sol qui augmente les dégâts subis par les ennemis à l'intérieur et réduits les soins qu'ils reçoivent",use=INTELLIGENCE)
bastionEff = effect("Bastion","bastionEff",redirection=25,emoji='<:bastion:1063117878095790170>')
bastion = skill("Bastion",getAutoId(corruptusArea.id,True),TYPE_BOOST,350,effects=bastionEff,emoji='<:bastion:1063117878095790170>',replay=True,cooldown=5,range=AREA_DONUT_4,description="Redirige **{0}%** des dégâts reçus par l'allié ciblé jusqu'au début de votre prochain tour et vous permet de rejouer votre tour".format(bastionEff.redirection))
orage = skill("Orage",getAutoId(bastion.id,True),TYPE_DAMAGE,500,power=50,use=MAGIE,effectAroundCaster=[TYPE_DAMAGE,AREA_DONUT_1,65],emoji='<:orage:1063117783929470996>',cooldown=5,pull=3,area=AREA_INLINE_3,description="Attire l'ennemi ciblé sur soi en lui infligeant des dégâts, puis inflige de nouveaux dégâts à tous vos ennemis à votre corps à corps")
magmaEff = copy.deepcopy(defenseUp)
magmaEff.power = 15
magma = skill("Magma",getAutoId(orage.id,True),TYPE_DAMAGE,500,power=75,area=AREA_INLINE_3,range=AREA_MONO,pull=3,emoji='<:magma:1063117817848791050>',effectOnSelf=magmaEff,cooldown=5,description="Attire les ennemis autour de vous en leur infligeant des dégâts, tout en réduisant les dégâts que vous subirrez jusqu'à votre prochain tour")
soulScealEff = effect("Sceau d'Âme","soulSceal", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,stackable=True,power=20,emoji='<:soulSeals:1023610978107146240>',turnInit=8,description="Inflige des dégâts continues à la fin du tour du porteur. La puissance de cet effet augmente de **{0}%** après chaque déclanchement.\nSi la cible est vaincu, l'effet est transmis aux ennemis alentours pour la durée restante mais avec une puissance rénitialisée".format(15),iaPow=20*(1.15**8 - 1.15) * 5)
soulSceal = skill("Sceau d'Âme",getAutoId(magma.id,True),TYPE_INDIRECT_DAMAGE,750,effects=soulScealEff,emoji='<:soulSceal:1064141053927628881>',cooldown=7,condition=[EXCLUSIVE,ASPIRATION,SORCELER],description="Inflige des dégâts continus à l'ennemi ciblé. La puissance des dégâts augmentent au fil du temps")
soulTwinEff = effect("Âme Jumelle","twinSoul", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,power=int(soulScealEff.power*1.25),emoji='<:soulTwin:1064141076581077095>')
soulTwin = skill("Âme Jumelle",getAutoId(soulSceal.id,True),TYPE_DAMAGE,500,use=MAGIE,useActionStats=ACT_INDIRECT,emoji='<:soulTwin:1064141076581077095>',effects=soulTwinEff,cooldown=5,condition=[EXCLUSIVE,ASPIRATION,SORCELER],power=90,description="Inflige des dégâts à l'ennemi ciblé. Si celui-ci subis un effet {0} __{1}__ infligé par vous-même, inflige des dégâts indirects supplémentaires équivalents à **{2}%** de la puissance actuelle du dit effet".format(soulScealEff.emoji[0][0],soulScealEff.name,round((soulTwinEff.power/soulScealEff.power)*100)))
soulWaveEff = effect("Vague à l'Âme","soulSceal2", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,stackable=True,power=soulScealEff.power,emoji='<:soulWaveEff:1064164761320816680>',turnInit=8,description="Inflige des dégâts continues à la fin du tour du porteur. La puissance de cet effet augmente de **{0}%** après chaque déclanchement".format(15),iaPow=int(soulScealEff.power*0.5)*(1.15**8 - 1.15) * 5)
soulWave = skill("Vague à l'Âme",getAutoId(soulTwin.id,True),TYPE_DAMAGE,500,use=MAGIE,useActionStats=ACT_INDIRECT,effects=soulWaveEff,power=110,cooldown=7,emoji='<:soulWave:1064141030737322044>',description="Inflige des dégâts à l'ennemi ciblé. Si celui-ci subis un effet {0} __{1}__ infligé par vous-même, inflige {2} __{3}__ aux ennemis environnants avec **{4}%** de la puissance actuelle du premier effect pour la durée restante du dit effet".format(soulScealEff.emoji[0][0],soulScealEff.name,soulWaveEff.emoji[0][0],soulWaveEff.name,50),condition=[EXCLUSIVE,ASPIRATION,SORCELER],effPowerPurcent=50)
gigaChadEff = effect("Giga Chad","gigaChad", stat=CHARISMA,strength=15,endurance=20,charisma=20,agility=10,precision=10,intelligence=20,magie=15,emoji='<a:gigaChad:1065649083513053275>',effPrio=1.5)
gigaChad = skill("Giga Chad",getAutoId("sfu",True),TYPE_BOOST,750,use=CHARISMA,effects=gigaChadEff,cooldown=7,ultimate=True,emoji=gigaChadEff.emoji[0][0],description="Augmente grandement les statistiques de l'allié ciblé durant un tour",range=AREA_DONUT_5)
megaVentEff = effect("Méga Vent","aero3", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=40,turnInit=3,emoji='<:megaVent:1065673324484628571>',area=AREA_CIRCLE_1)
megaVent = skill("Méga Vent",getAutoId(gigaChad.id,True),TYPE_DAMAGE,500,emoji='<:aero3:1065647076563746847>',use=MAGIE,power=50,cooldown=5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],effects=megaVentEff,area=AREA_CIRCLE_1,range=AREA_CIRCLE_3,description="Inflige des dégâts aux ennemis ciblés et inflige un effet de dégâts indirects de zone à la cible principale")
dismantleEff = copy.deepcopy(dmgDown)
dismantleEff.power, dismantleEff.stat = 4, STRENGTH
dismantle = skill("Brise-Arme",getAutoId(megaVent.id,True),TYPE_MALUS,500,effects=dismantleEff,replay=True,emoji='<:dismantle:1065647433322872902>',cooldown=5,description="Réduit les dégâts infligés par la cible et vous permet de rejouer votre tour")
leadShotEff = effect("Balle de Plomb","leadShotEff", stat=STRENGTH,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=20,turnInit=3,emoji='<:leadShot:1065676062874419222>')
leadShot = skill("Tir de Plomb",getAutoId(dismantle.id,True),TYPE_DAMAGE,500,power=35,effects=leadShotEff,replay=True,cooldown=5,description="Inflige des dégâts à l'ennemi ciblé ainsi qu'un effet de dégâts continus et vous permet de rejouer votre tour",emoji='<:bleedingShot:1065647049703428218>')
heatedCleanShotEff = effect("Dégâts critiques augmentés","critDmgButClean",turnInit=5,critDmgUp=15)
heatedCleanShotReady = effect("Tir Net Chauffé préparé","heatedCleanShotReady",turnInit=5,emoji='<:cleanShotCombo3:1065647407020392468>')
heatedCleanShot = skill("Tir Net Chauffé",getAutoId(leadShot.id,True),TYPE_DAMAGE,power=125,effectOnSelf=heatedCleanShotEff,cooldown=5,needEffect=heatedCleanShotReady,description="Inflige des dégâts à l'ennemi ciblé et augmente vos dégâts critiques durant un court instant",emoji="<:cleanShotCombo3:1065647407020392468>")
heatedSlugShotReady = effect("Tir de Balle Chauffé préparé","heatedSlugShotReady",turnInit=5,emoji='<:cleanShotCombo2:1065647381208641556>')
heatedSlugShot = skill("Tir de Balle Chauffé",heatedCleanShot.id,TYPE_DAMAGE,power=100,effectOnSelf=heatedCleanShotReady,needEffect=heatedSlugShotReady,emoji='<:cleanShotCombo2:1065647381208641556>',description="Inflige des dégâts à l'ennemi ciblé et vous permet d'utiliser {0} {1}".format(heatedCleanShot.emoji,heatedCleanShot.name))
heatedSlitShot = skill("Tir Scyndé Chauffé",heatedCleanShot.id,TYPE_DAMAGE,power=80,effectOnSelf=heatedSlugShotReady,rejectEffect=[heatedSlugShotReady,heatedCleanShotReady],emoji='<:cleanShotCombo1:1065647347113148436>',description="Inflige des dégâts à l'ennemi ciblé et vous permet d'utiliser {0} {1}".format(heatedSlugShot.emoji,heatedSlugShot.name))
comboHeatedCleanShot = skill("Combo - Tir Net Chauffé",heatedCleanShot.id,TYPE_DAMAGE,become=[heatedSlitShot,heatedSlugShot,heatedCleanShot],price=500,description="Permet d'utiliser {0} {1}, {2} {3} et {4} {5}, devant être utlisés dans cet ordre. La dernière compétence augmente vos dégâts critiques infligés pendant {6} tours".format(heatedSlitShot.emoji,heatedSlitShot.name,heatedSlugShot.emoji,heatedSlugShot.name,heatedCleanShot.emoji,heatedCleanShot.name,heatedCleanShot.effectOnSelf.turnInit),emoji=heatedCleanShot.emoji)
summonHinoro = skill("Invocation - Hinoro",getAutoId(heatedCleanShot.id,True),TYPE_SUMMON,use=MAGIE,price=750,invocation="Hinoro",emoji='<:summonHinoro:1066006465225171005>',ultimate=True,cooldown=7,description="Permet d'invoquer Hinoro, une invocation magique qui inflige des dégâts aux ennemis tout en soignant ses alliés")
healingSacrificeEff = effect("Régénération Sacrificielle","healingSacrifice", stat=CHARISMA,power=80,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji='<:AltyRegen:994748551932428319>')
healingSacrifice = skill("Sacrifice Bienveillant",getAutoId(summonHinoro.id,True),TYPE_HEAL,price=750,initCooldown=3,power=50,range=AREA_MONO,area=AREA_DONUT_3,cooldown=7,effectOnSelf=bolideEff,effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_MONO,healingSacrificeEff],description="Réduit vos PVs actuels à 1, soigne les alliés alentours d'une valeur égalant **{power}%** des PVs sacrifiés, vous rend **Invulnérable** jusqu'à votre prochain tour et vous octroi un effet régénérant dont la puissance dépend du pourcentage de PV consommés par rapport à vos PV Max",emoji='<:lovingSacrifice:1066737438288003092>')

deathMark = effect("Marque Funèbre","deathMark",turnInit=7,type=TYPE_DAMAGE,trigger=TRIGGER_ON_REMOVE,power=10,emoji='<:deathMark:1072900011140063302>',stackable=True,stat=STRENGTH,description="Augmente de **20%** les dégâts infligés au porteur par l'entité à l'origine de cet effet.\nCertaines compétences ont des effets supplémentaires si le lanceur a infligé cet effet à la cible.\nSi le décompte de cet effet atteint 0, il inflige des dégâts indirects équivalents à **50%** de sa puissance\nSi vous avez déjà infligé cet effet, la puissance du premier effet augmente de l'équivalent de **50%** de ce nouvel effet.\n\nCet effet remplace <:longName:938167649106538556> __Dessins de la Camarade__ si vous avez infligé cet effet à la cible préalablement, déclanchant ses effets prématuréments avec **50%** de sa puissance")
triggerDeathMark = effect("Déclanche Marque Funèbre","triggerDeathMark",power=100,trigger=TRIGGER_INSTANT,type=TYPE_UNIQUE,emoji='<:triggerDeathMark:1072905603971809321>',description="Déclanche la {0} __{1}__ que vous avez infligé sur l'ennemi ciblé, infligeant des dégâts indirects avec un pourcentage de sa puissance équivalante à la puissance de cet effet dans la zone d'effet spécifié".format(deathMark.emoji[0][0],deathMark.name))
deathPercing = skill("Percée Funèbre",getAutoId(healingSacrifice.id,True),TYPE_DAMAGE,price=500,effPowerPurcent=75,power=80,cooldown=5,effects=deathMark,emoji='<:percFun:1072900310164574278>',description="Inflige {0} __{1}__ à l'ennemi ciblé et lui inflige des dégâts".format(deathMark.emoji[0][0],deathMark.name),effBeforePow=True)
deathMarkNeeded = effect("Marque Funèbre sur la cible","deathMarkNeeded",emoji=deathMark.emoji)
matEff2 = copy.deepcopy(armorGetMalus)
matEff2.power = 30
mat = skill("Echec et Mat",getAutoId(deathPercing.id,True),TYPE_DAMAGE,range=AREA_CIRCLE_3,needEffect=[deathMarkNeeded],power=135,effects=[incur[3],matEff2],tpBehind=True,effectOnSelf=triggerDeathMark,emoji='<:mat:1072905343920779264>',cooldown=7,ultimate=True,description="Inflige des dégâts à l'ennemi ciblé, réduit de **50%** les soins qu'il reçoit et déclanche {0} __{1}__".format(deathMark.emoji[0][0],deathMark.name))
echec = skill("Echec",mat.id,TYPE_DAMAGE,power=50,effects=deathMark,range=AREA_CIRCLE_3,effPowerPurcent=65,tpCac=True,emoji='<:echec:1072900255827365940>',cooldown=3,ultimate=True,description="Inflige des dégâts à l'ennemi ciblé et lui inflige {0} __{1}__.\n\nSi vous avez préalablement infligé ce dit effet, cette compétence devient {2} __{3}__".format(deathMark.emoji[0][0],deathMark.name,mat.emoji,mat.name))
echecEtMat = skill("Echec (et Mat)",echec.id,TYPE_DAMAGE,become=[echec,mat],price=500,emoji=mat.emoji,description="Inflige des petits dégâts à l'ennemi ciblé et lui inflige {6} __{7}__. Si vous aviez déjà infligé l'effet, inflige de plus gros dégâts, déclanche la marque et réduit les soins reçus par la cible.\n\n{0} __{1}__ :\n{2}\n\n{3} __{4}__ :\n{5}".format(echec.emoji,echec.name,echec.description,mat.emoji,mat.name,mat.description,deathMark.emoji[0][0],deathMark.name))
seitonTenchu = skill("Seiton Tenchû",getAutoId(echec.id,True),TYPE_DAMAGE,price=500,cooldown=7,power=120,emoji='<:ninjaLb:1072904057393520791>',tpCac=True,effBeforePow=True,effects=[deathMark],description='Inflige {0} __{1}__ à l\'ennemi ciblé puis lui inflige des dégâts'.format(deathMark.emoji[0][0],deathMark.name),range=AREA_CIRCLE_4)
funDraw = skill("Dessin Funèbre",types=TYPE_DAMAGE,emoji='<:marqFun:1073973428001968128>',id=getAutoId(seitonTenchu.id,True),power=80,cooldown=5,price=500,use=MAGIE,useActionStats=ACT_INDIRECT,area=AREA_LINE_2,description="Inflige des dégâts aux ennemis ciblés et augmente de **35%** la puissance de tous les effets {0} __{1}__ présents sur la cible principale".format(deathMark.emoji[0][0],deathMark.name))
infDraw = skill("Dessin Infecteux",getAutoId(funDraw.id,True),types=TYPE_DAMAGE,price=500,effPowerPurcent=65,power=80,cooldown=5,use=MAGIE,useActionStats=ACT_INDIRECT,effects=[infection,epidemicEff,intoxEff],emoji='<:marqInf:1073978855766892605>',description="Inflige des dégâts à la cible. Rénitialise la puissance et la durée des effets {0}, {1} et {2} présents sur la cible".format(infection,epidemicEff,intoxEff))
moramMortemEff = effect("Moram Mortem","moramMortem", stat=INTELLIGENCE,type=TYPE_ARMOR,overhealth=50,turnInit=3,trigger=TRIGGER_DAMAGE,emoji='<:moramMortis:1084865158884630528>',stackable=True)
extensasVita = effect("Extensas Vita","extensasVita", stat=INTELLIGENCE,type=TYPE_ARMOR,overhealth=moramMortemEff.overhealth,turnInit=moramMortemEff.turnInit,trigger=TRIGGER_DAMAGE,emoji='<:extensaVita:1084865373733650574>',stackable=True)
moramMortem = skill("Moram Mortem",getAutoId(infDraw.id,True),price=500,types=TYPE_HEAL,power=40,use=INTELLIGENCE,useActionStats=ACT_SHIELD,effects=[moramMortemEff,extensasVita],cooldown=5,emoji='<:moramMortem:1084865748586995824>',description="Soigne l'allié ciblé et lui procure un grand nombre de points d'armure",condition=[EXCLUSIVE,ASPIRATION,PREVOYANT])
moramMortem2 =skill("Extra Moram Mortem",getAutoId(moramMortem.id,True),price=500,types=TYPE_HEAL,range=AREA_MONO,area=AREA_CIRCLE_2,use=INTELLIGENCE,useActionStats=ACT_SHIELD,power=30,effects=[moramMortemEff],cooldown=5,emoji='<:moramMortem2:1084867372080435220>',description="Vous soigne vous et vos alliés proches et vous octroi une armure",condition=[EXCLUSIVE,ASPIRATION,PREVOYANT])
lifeFlame = skill("Flamma Vitae",getAutoId(moramMortem2.id,True),price=500,types=TYPE_INDIRECT_HEAL,emoji='<:lifeFlame:1084263863874228414>',use=MAGIE,cooldown=5,replay=True,effPowerPurcent=65,effects=[phoenixFlight],range=AREA_MONO,area=AREA_CIRCLE_2,condition=[EXCLUSIVE,ASPIRATION,MAGE],description="Octroi à vous et vos alliés proches un effet de régénération et vous permet de rejouer votre tour")
lifeLight = skill("Lux Vitae",getAutoId(lifeFlame.id,True),cooldown=7,price=750,emoji='<:lifeLight:1084263898926035024>',use=MAGIE,types=TYPE_DAMAGE,power=120,effectAroundCaster=galvanisation.effectAroundCaster,effPowerPurcent=galvanisation.effPowerPurcent,condition=[EXCLUSIVE,ASPIRATION,MAGE],description="Inflige des dégâts à l'ennemi ciblé et octroi un effet de régénération à vous et vos alliés proches")
putrefaction = skill("Putrefactio",getAutoId(lifeLight.id,True),TYPE_DAMAGE,price=500,emoji='<:putrfaction:1084871857586569256>',cooldown=7,power=120,effects=[incur[4]],description="Inflige des dégâts à l'ennemi ciblé et réduit de **40%** les soins qu'il reçoit jusqu'à votre prochain tour",use=MAGIE,condition=[EXCLUSIVE,ASPIRATION,MAGE])
decompositionEff = effect("Décompositionis","decompositionEff", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,power=40,turnInit=3,emoji='<:dcomposition:1084872910314950656>')
decompositionEff2 = copy.deepcopy(incur[2])
decompositionEff2.turnInit = decompositionEff2.lvl = 3
decomposition = skill("Decompositionis",getAutoId(putrefaction.id,True),TYPE_INDIRECT_DAMAGE,effects=[decompositionEff,decompositionEff2],emoji='<:dcomposition:1084872775157682288>',cooldown=7,condition=[EXCLUSIVE,ASPIRATION,SORCELER],description="Inflige des dégâts continus à l'ennemi ciblé et réduit de **20%** les soins qu'il reçoit pendant 3 tours",price=500)
flammaSinister = skill("Sinister Flamma",getAutoId(decomposition.id,True),TYPE_ARMOR,price=500,effects=moramMortemEff,effPowerPurcent=40,replay=True,range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=5,description="Vous octroi à vous et vos alliés proches une armure et vous permet de rejouer votre tour",condition=[EXCLUSIVE,ASPIRATION,PREVOYANT],emoji='<:deadlyWave:1084263973530107904>')
sinisterLux = skill("Sinister Lux",getAutoId(flammaSinister.id,True),TYPE_DAMAGE,price=750,power=100,use=INTELLIGENCE,useActionStats=ACT_SHIELD,cooldown=7,effPowerPurcent=65,effectAroundCaster=[TYPE_ARMOR,AREA_CIRCLE_2,moramMortemEff],emoji='<:sinisterLight:1084263936599265381>',description="Inflige des dégâts à l'ennemi ciblé et octroi une armure à vous et vos alliés proches")
nonVitaUnionis = skill("Non Vita Unionis",getAutoId(sinisterLux.id,True),TYPE_INDIRECT_HEAL,price=750,effects=[galvanisation.effectAroundCaster[2],moramMortemEff],range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=7,emoji='<:union:1084863427907944469>',description="Vous soigne vous et vos alliés proches tout en vous octroyant un effet régénérant et une armure",use=HARMONIE)
purify2Eff1, purify2Eff2 = copy.deepcopy(healDoneBonus), copy.deepcopy(absEff)
purify2Eff1.power, purify2Eff2.power = 15, 10
purify2Eff1.turnInit = purify2Eff2.turnInit = 3
purify2 = skill("Purification Augmentée",getAutoId(nonVitaUnionis.id,True),TYPE_HEAL,power=35,price=750,effects=purify2Eff2,range=AREA_MONO,area=AREA_DONUT_2,effectOnSelf=purify2Eff1,group=SKILL_GROUP_HOLY,maxHpCost=25,cooldown=7,emoji='<:emoji_11:1085991767834370108>',description="Soigne vos alliés alentours et augmente les soins qu'ils recoivent de **{0}%** tout en augmentant vos soins réalisés de **{1}%**, durant **{2}** tours".format(purify2Eff2.power,purify2Eff1.power,purify2Eff1.turnInit))
synastieEff = effect("Synastie","synastieEff", stat=CHARISMA,strength=7, magie=7,turnInit=3,emoji='<:muscBat:1028695550645784576>')
synastie = skill("Synastie",getAutoId(purify2.id,True),TYPE_BOOST,price=750,effects=synastieEff,area=AREA_CIRCLE_2,range=AREA_DIST_5,effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_2,synastieEff],cooldown=7,description="Augmente les statistiques offensives des alliés ciblés et de ceux autour de vous",emoji='<:synastie:1085991733336219728>')
fracasEff = copy.deepcopy(armorGetMalus)
fracasEff.power, fracasEff.turnInit = 20, 3
fracasEff2 = effect("Fraccasé","fracas", stat=PURCENTAGE,turnInit=3,resistance=-25,type=TYPE_MALUS)
fracas = skill("Talon Fracassant",getAutoId(synastie.id,True),TYPE_DAMAGE,use=STRENGTH,price=500,power=115,percing=20,cooldown=7,effects=[fracasEff,fracasEff2],range=AREA_CIRCLE_2,emoji='<:talonFracassant:1088958995030605834>',description="Inflige des dégâts à l'ennemi ciblé et réduit l'armure qu'il reçoit durant 3 tours. Dégâts augmentés sur l'armure",damageOnArmor=1.2)
revolFracasEff = copy.deepcopy(armorGetMalus)
revolFracasEff.power, fracasEff.turnInit = 10, 3
revolutionFracas = skill("Révolution Fracassante",getAutoId(fracas.id,True),TYPE_DAMAGE,use=STRENGTH,price=500,power=55,repetition=2,range=AREA_MONO,area=AREA_CIRCLE_2,emoji='<:rvolution:1089332047165800458>',cooldown=7,damageOnArmor=1.5,description="Inflige à deux reprises des dégâts aux ennemis alentours et réduit les armures qu'ils reçoivent durant 3 tours. Dégâts augmentés sur l'armure",effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_2,revolFracasEff])
plongeFracasEff = effect("Onde de choc","plongeFracasEff",stat=STRENGTH,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,power=60,area=AREA_DONUT_2,emoji='<:darkThunder:912414778356564019>')
plongeFracas = skill("Salto Fracassant",getAutoId(revolutionFracas.id,True),TYPE_DAMAGE,emoji='<:plongee:1088958906178474076>',range=AREA_CIRCLE_2,power=100,effects=[revolFracasEff,plongeFracasEff],cooldown=7,description="Inflige des dégâts à l'ennemi ciblé et réduit l'armure qu'il reçoit durant 3 tours. Inflige également des dégâts indirects aux ennemis proches",price=500)
holyVoiceEff1 = effect("Voix divine","divineVoice", stat=CHARISMA,strength=10,magie=10,endurance=5,emoji='<:holyVoice:1085991767834370108>',turnInit=3)
holyVoiceEff2 = copy.deepcopy(dmgUp)
holyVoiceEff2.power, holyVoiceEff2.stat, holyVoiceEff2.turnInit = 3, CHARISMA, 3
holyVoice = skill("Voix Divine",getAutoId(plongeFracas.id,True),TYPE_BOOST,price=750,emoji='<:voixDivine:1085991767834370108>',group=SKILL_GROUP_HOLY,area=AREA_CIRCLE_3,maxHpCost=20,range=AREA_MONO,effects=[holyVoiceEff1,holyVoiceEff2],cooldown=7,description="Augmente grandement les statistiques offensives et l'endurance ainsi que légèrement les dégâts infligés des alliés elntours durant 3 tours")
justiceEnigmaEff = effect("Enigme de la Justice","justiceEnigma",type=TYPE_UNIQUE,turnInit=1,power=35,aggro=50,trigger=TRIGGER_ON_REMOVE,emoji='<:gwenEnigma:1089710449299292241>',description="Réduit de **{0}%** les dégâts reçus et augmente grandement la probabilité d'être pris pour cible. Lors de votre prochain tour, inflige des dégâts aux ennemis alentours équivalents à la quantité de dégâts réduits par cet effet et vous soigne de la même quantité",iaPow=100)
justiceEnigma = skill("Enigme de la Justice",getAutoId(holyVoice.id,True),TYPE_BOOST,price=500,cooldown=5,effects=justiceEnigmaEff,range=AREA_MONO,emoji=justiceEnigmaEff.emoji[0][0],description="Réduit vos dégâts subis et augmente votre niveau d'agression jusqu'à votre prochain tour. Au début de celui-ci, inflige des dégâts aux ennemis proches et vous soigne en fonction des dégâts reçus")
weakPointEff1 = effect("Point Faible révélé","weakPointRevealed",stat=PURCENTAGE,resistance=-50,type=TYPE_MALUS)
weakPointEff2 = copy.deepcopy(deathMark)
weakPointEff2.power = 35
weakPoint = skill("Point Faible",getAutoId(justiceEnigma.id,True),TYPE_DAMAGE,price=750,power=85,cooldown=5,percing=35,emoji='<:weakPoint:1091006907470332004>',effects=[weakPointEff1,weakPointEff2],description="Inflige {0} __{1}__ et réduit la résistance de l'ennemi ciblé avant de lui infliger des dégâts en ignorant une partie de sa résistance".format(weakPointEff2.emoji[0][0],weakPointEff2.name),effBeforePow=True)
rippingEff = copy.deepcopy(triggerDeathMark)
rippingEff.power = 85
ripping = skill("Eventration",getAutoId(weakPoint.id,True),TYPE_DAMAGE,price=500,power=85,cooldown=5,effects=rippingEff,range=AREA_CIRCLE_3,emoji='<:ripped:1091006942715068526>',tpCac=True,description="Inflige des dégâts à l'ennemi ciblé en ignorant une partie de sa résistance tout en déclanchant {0} __{1}__ avec **{2} %** de sa puissance".format(deathMark.emoji[0][0],deathMark.name,rippingEff.power),percing=20)
bloodMoonEff, bloodMoonEff2 = copy.deepcopy(dmgUp), copy.deepcopy(vampirismeEff)
bloodMoonEff.stat = bloodMoonEff2.stat = INTELLIGENCE
bloodMoonEff.power = bloodMoonEff2.power = 5
bloodMoon = skill("Lever de la Nouvelle Lune",getAutoId(ripping.id,True),TYPE_BOOST,cooldown=5,area=AREA_CIRCLE_2,effects=[bloodMoonEff,bloodMoonEff2],emoji='<:newMoon:1094026598690324573>',description="Augmente les dégâts infligés par les alliés ciblés et leur octroi un pourcentage de vol de vie",condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE])
blueMoonEff2 = copy.deepcopy(convertEff)
blueMoonEff2.stat, blueMoonEff2.power = bloodMoonEff2.stat, bloodMoonEff2.power
blueMoon = skill("Lever de la Pleine Lune",bloodMoon.id,TYPE_BOOST,cooldown=5,area=AREA_CIRCLE_2,effects=[bloodMoonEff,blueMoonEff2],emoji='<:fullMoon:1094026627106738246>',description="Augmente les dégâts infligés par les alliés ciblés et convertie une partie des dégâts qu'ils infligent en armure",condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE])
buffMoonBundle = skill("Lever de la Lune Bénéfique",blueMoon.id,TYPE_BOOST,price=500,become=[blueMoon,bloodMoon],emoji=blueMoon.emoji,description="Vous permet d'utiliser {0} et {1}, deux compétences aumgentant les dégâts infligés et la survivabilité des alliés ciblés".format(blueMoon,bloodMoon))

newMoonEff, newMoonEff2 = copy.deepcopy(dmgDown), copy.deepcopy(armorGetMalus)
newMoonEff.stat, newMoonEff.power, newMoonEff2.power = INTELLIGENCE, 4, 30

newMoon = skill("Lever de la Lune Bleu",getAutoId(buffMoonBundle.id,True),TYPE_MALUS,cooldown=5,area=AREA_CIRCLE_2,effects=[newMoonEff,newMoonEff2],emoji='<:blueMoon:1094026561784643604>',description="Réduits les dégâts infligés par les ennemis ciblés ainsi que l'armure qu'ils reçoivent",condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE])
fullMoon = skill("Lever de la Lune de Sang",newMoon.id,TYPE_MALUS,cooldown=5,area=AREA_CIRCLE_2,effects=[newMoonEff,incur[3]],emoji='<:BloodMoon:1094026774448443512>',description="Réduits les dégâts infligés par les ennemis ciblés ainsi que les soins qu'ils reçoivent",condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE])

debuffMoonBundle = skill("Lever de la Lune Maléfique",newMoon.id,TYPE_MALUS,price=500,become=[newMoon,fullMoon],emoji=fullMoon.emoji,description="Vous permet d'utiliser {0} et {1}, deux compétences réduisant les dégâts infligés et la survivabilité des ennemis ciblés".format(newMoon,fullMoon))

moonLightEff1, moonLightEff2 = copy.deepcopy(defenseUp), effect("Clair de Lune","moonLight",stat=INTELLIGENCE,overhealth=35,trigger=TRIGGER_DAMAGE,emoji='<:moonLight:1094028166449868840>',type=TYPE_ARMOR)
moonLightEff1.power, moonLightEff1.stat = 3.5, INTELLIGENCE
moonLight = skill("Clair de Lune","sel",TYPE_BOOST,price=500,cooldown=5,effects=[moonLightEff1,moonLightEff2],area=AREA_CIRCLE_1,emoji=moonLightEff2.emoji[0][0],description="Réduit les dégâts subis par les alliés ciblés et leur octroi une légère armure")
lacerEff = effect("Lacération","lacerationEff",stat=PURCENTAGE,resistance=-7,type=TYPE_MALUS,stackable=True,emoji='<:laceration:1100428518401245194>')
exploStrikeEff = effect("Frappe Explosive","exploStrike",stat=STRENGTH,type=TYPE_DAMAGE,trigger=TRIGGER_INSTANT,area=AREA_DONUT_1,power=20,emoji='<:exploShotEff:1049704001257619476>')
exploStrikeEff2 = copy.deepcopy(deepWound)
exploStrikeEff2.stat, exploStrikeEff2.power = STRENGTH, 50
pentastrike5 = skill("PentaStrike Explosive",getAutoId(moonLight.id,True),TYPE_DAMAGE,price=750,ultimate=True,affSkillMsg=False,range=AREA_CIRCLE_1,effects=[lacerEff,exploStrikeEff,exploStrikeEff2],effPowerPurcent=150,power=100,emoji='<:kPentaStrikeFinal:1101004392506855515>',cooldown=7,description="Après un tour de chargement, inflige 5 coups à l'ennemi ciblé. Chaque attaque réduit sa résistance et inflige des dégâts indirects suplémentaires à la cible et aux ennemis proches")
pentastrike5_c = effect("Enchaînement - {replicaName}","pentaStrike5",silent=True,replique=pentastrike5)
pentastrike1 = copy.deepcopy(pentastrike5)
pentastrike1.power, pentastrike1.effectOnSelf, pentastrike1.emoji, pentastrike1.replay, pentastrike1.repetition, pentastrike1.affSkillMsg, pentastrike1.effPowerPurcent = 20, pentastrike5_c, "<:kPentaStrike:1101004369727602688>", True, 4, True, 100
pentastrike1_c = effect("Cast - {replicaName}","pentaStrike1",silent=True,replique=pentastrike1,turnInit=2,emoji='<:kpentaCast:1102576167627792455>')
pentastrike = copy.deepcopy(pentastrike5)
pentastrike.power, pentastrike.effects, pentastrike.effectOnSelf, pentastrike.affSkillMsg = 0, [None], pentastrike1_c, True
guardianAngelEff = copy.deepcopy(healDoneBonus)
guardianAngelEff.power, guardianAngelEff.turnInit = 35, 3
guardianAngel = skill("Shugo Tenshi",getAutoId(pentastrike.id,True),TYPE_HEAL,price=750,power=80,area=AREA_CIRCLE_3,range=AREA_MONO,effectOnSelf=guardianAngelEff,ultimate=True,cooldown=7,effBeforePow=True,effectAroundCaster=[TYPE_RESURECTION,AREA_CIRCLE_3,100],description="Augmente vos soins réalisés pendant 3 tours, soigne et réanime les alliés autours de vous",emoji='<:guardianAngel:1098144514796953661>')
gravPulse1 = skill("Pulsation Gravitationnelle",getAutoId(guardianAngel.id,True),TYPE_DAMAGE,use=MAGIE,power=160,area=AREA_CIRCLE_2,range=AREA_MONO,emoji='<:pulsationGrav2:1097521800352632832>',knockback=3,cooldown=7,ultimate=True,description="Attire au premier tours les ennemis autour de vous en leur infligeant des dégâts, puis leur inflige de nouveaux dégâts au second tour en les repoussants",condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE])
gravPulse_c = effect("Cast - {replicaName}","pulsGravEff",replique=gravPulse1,turnInit=2)
gravPulse = skill("Pulsation Gravitationnelle",gravPulse1.id,TYPE_DAMAGE,price=500,use=MAGIE,power=100,area=AREA_CIRCLE_3,pull=5,ultimate=True,condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE],effectOnSelf=gravPulse_c,emoji='<:pulsationGrav:1097521731331170456>',cooldown=7,description=gravPulse1.description)

kStrikeEff2 = copy.deepcopy(deepWound)
kStrikeEff2.stat, kStrikeEff2.power = STRENGTH, 50
kStrikeEff = effect("Saignement","bleedingKEff", stat=STRENGTH,type=TYPE_INDIRECT_DAMAGE,power=25,turnInit=3,trigger=TRIGGER_START_OF_TURN,lifeSteal=250,emoji='<:bleed:1083761078770618460>')
kStrike = skill("Frappe Sanglante",getAutoId(gravPulse.id,True),TYPE_DAMAGE,range=AREA_CIRCLE_1,power=95,effects=[kStrikeEff,kStrikeEff2],cooldown=5,condition=[EXCLUSIVE,ASPIRATION,BERSERK],emoji='<:kStrike:1100644659241422891>',price=500,description="Inflige des dégâts à l'ennemi ciblé ainsi qu'un effet de dégâts période vous soignant en fonction des dégâts qu'il inflige")

gwenPenta5 = skill("PentaStrike Armurée",getAutoId(kStrike.id,True),TYPE_DAMAGE,price=750,range=AREA_CIRCLE_1,use=INTELLIGENCE,affSkillMsg=False,armorSteal=35,damageOnArmor=1.2,power=pentastrike5.power,effects=lacerEff,cooldown=pentastrike5.cooldown,ultimate=True,emoji='<:gPentaStrineFinal:1100778233831641118>',armorConvert=70,accuracy=150,aoeArmorConvert=50,description="Après un tour de chargement, inflige 5 coups à l'ennemi ciblé. Chaque attaque réduit sa résistance et octroi à vous et vos alliés proches une armure en fonction des dégâts infligés")
gwenPenta5_c = effect("Enchaînement - {replicaName}","pentaStrike5",silent=True,replique=gwenPenta5)
gwenPenta1 = copy.deepcopy(gwenPenta5)
gwenPenta1.power, gwenPenta1.effectOnSelf, gwenPenta1.emoji, gwenPenta1.replay, gwenPenta1.armorConvert, gwenPenta1.aoeArmorConvert, gwenPenta1.affSkillMsg, gwenPenta1.repetition = pentastrike1.power, gwenPenta5_c, "<:gPentaStrike:1100778209450139688>", True, 50, 35, True, 4
gwenPenta1_c = effect("Cast - {replicaName}","pentaStrike1",silent=True,replique=gwenPenta1,turnInit=2,emoji='<:gpentaCast:1102576189937299526>')
gwenPenta = copy.deepcopy(gwenPenta5)
gwenPenta.power, gwenPenta.effects, gwenPenta.effectOnSelf, gwenPenta.affSkillMsg = 0, [None], gwenPenta1_c, True

gwenCharge = skill("Taillade Sautée",getAutoId(gwenPenta5.id,True),TYPE_DAMAGE,power=85,price=500,range=AREA_CIRCLE_4,tpCac=True,use=INTELLIGENCE,armorConvert=50,aoeArmorConvert=35,armorSteal=50,cooldown=5,emoji="<:gStrike:1100681148876718120>",description="Saute sur l'ennemi ciblé, lui inflige des dégâts et octroi à vous et vos alliés proches une armure en fonction des dégâts infligés")
pandaiStrike = skill("Frappe Pandaimique",getAutoId(gwenCharge.id,True),TYPE_DAMAGE,power=85,price=500,effectOnSelf=pandaimaEff,cooldown=7,range=AREA_CIRCLE_1,emoji=pandaima.emoji,description="Inflige des dégâts à l'ennemi ciblé et vous octroi l'effet {0} {1}".format(pandaimaEff.emoji[0][0],pandaimaEff.name),condition=[EXCLUSIVE,ASPIRATION,PROTECTEUR],use=INTELLIGENCE)

altyPenta5 = skill("QuinqueStrike Régénérante",getAutoId(pandaiStrike.id,True),TYPE_DAMAGE,price=750,range=AREA_CIRCLE_1,use=CHARISMA,affSkillMsg=False,damageOnArmor=1.2,power=pentastrike5.power,effects=lacerEff,cooldown=pentastrike5.cooldown,ultimate=True,emoji="<:aPentaStrikeFinal:1101009327302660167>",lifeSteal=75,accuracy=150,aoeLifeSteal=50,description="Après un tour de chargement, inflige 5 coups à l'ennemi ciblé. Chaque attaque réduit sa résistance et vous soigne vous et vos alliés proches en fonction des dégâts infligés")
altyPenta5_c = effect("Enchaînement - {replicaName}","pentaStrike5",silent=True,replique=altyPenta5)
altyPenta1 = copy.deepcopy(altyPenta5)
altyPenta1.power, altyPenta1.effectOnSelf, altyPenta1.emoji, altyPenta1.replay, altyPenta1.lifeSteal, altyPenta1.aoeLifeSteal, altyPenta1.affSkillMsg, altyPenta1.repetition = pentastrike1.power, altyPenta5_c,'<:aPentaStrike:1101009306121416734>', True, 50, 35, True, 4
altyPenta1_c = effect("Cast - {replicaName}","pentaStrike1",silent=True,replique=altyPenta1,turnInit=2,emoji='<:apentaCast:1102576216034250823>')
altyPenta = copy.deepcopy(altyPenta5)
altyPenta.power, altyPenta.effects, altyPenta.effectOnSelf, altyPenta.affSkillMsg = 0, [None], altyPenta1_c, True

altyStrike = skill("Vertical Régénérant",getAutoId(altyPenta.id,True),TYPE_DAMAGE,use=CHARISMA,price=500,power=100,range=AREA_CIRCLE_1,lifeSteal=100,aoeLifeSteal=40,condition=[EXCLUSIVE,ASPIRATION,VIGILANT],emoji='<:aStrike:1100681172167704668>',description="Inflige des dégâts à l'ennmi ciblé et vous soigne vous et vos alliés proche en fonction des dégâts infligés",cooldown=5)