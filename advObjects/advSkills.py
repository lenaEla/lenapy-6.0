from classes import *
from constantes import *

soupledown = skill("Choc Ténébreux","zz",TYPE_DAMAGE,500,150,range = AREA_CIRCLE_1,conditionType=["exclusive","aspiration",POIDS_PLUME],area = AREA_CIRCLE_2,sussess=80,ultimate=True,cooldown=7,emoji='<:darkdown:892350717384347648>',use=STRENGTH)
inkarmor = skill("Armure d'Encre","zy",TYPE_ARMOR,250,ultimate=True,effect="la",emoji = '<:inkArmor:866829950463246346>',area=AREA_ALL_ALLIES,cooldown=5,range=AREA_MONO)
coffeeSkill = skill("Suprématie du café","zx",TYPE_BOOST,500,effect=["lb","mc"],use=CHARISMA,conditionType=["reject","skill","zw"],area=AREA_ALL_ALLIES,emoji='<:coffee:867538582846963753>',cooldown=4,message="{0} prend le café avec ses alliés :")
theSkill = skill("Liberté du thé","zw",TYPE_BOOST,500,effect=["lc","mc"],use=CHARISMA,conditionType=["reject","skill","zx"],area=AREA_ALL_ALLIES,emoji='<:the:867538602644602931>',cooldown=4,message="{0} prend le thé avec ses alliés :")
gpotion = skill("Potion tonifiante","zv",TYPE_BOOST,200,emoji="<:bpotion:867165268911849522>",use=INTELLIGENCE,cooldown=3,effect="le",area=AREA_MONO,range=AREA_MONO)
bpotion = skill("Potion étrange","zu",TYPE_MALUS,200,cooldown=3,effect="lf",emoji="<:dpotion:867165281617182760>",use=INTELLIGENCE,area=AREA_CIRCLE_1,message="{0} lance une {1} sur {2}")
zelian = skill("R","zt",TYPE_INDIRECT_REZ,250,cooldown=5,effect="lj",emoji='<:chronoshift:867872479719456799>',use=None)
courage = skill("Motivation","zs",TYPE_BOOST,500,emoji ='<:charge:866832551112081419>',area=AREA_CIRCLE_2,use=CHARISMA,effect="lk",cooldown=4,range=AREA_MONO)
nostalgia = skill("Nostalgie","zr",TYPE_MALUS,500,emoji='<:nostalgia:867162802783649802>',effect="lm",cooldown=4,use=INTELLIGENCE)
draw25 = skill("Stop attacking or draw 25","zq",TYPE_MALUS,300,25,emoji="<:draw25:869982277701103616>",use=None,effect="lq",cooldown = 3,area=AREA_ALL_ENEMIES,range=AREA_MONO,ultimate=True,conditionType=["exclusive","aspiration",PREVOYANT],message="{0} utilise sa carte joker !")
siropMenthe = skill("Neutralité du Sirop de Menthe","zp",TYPE_BOOST,500,effect=["lu","mc"],use=CHARISMA,area=AREA_ALL_ALLIES,emoji='<:menthe:867538622797054042>',cooldown=4,message="{0} prend un sirop de menthe avec ses alliés :")
unHolly = skill("Truc pas catho","zo",TYPE_MALUS,69,emoji='<:bravotakei:877202258348113960>',cooldown=2,effect="lw",use=CHARISMA,message="{0} ||fait des trucs pas catho à destination de|| {2} :")
chaos = skill("Chaos Chaos !","zn",TYPE_UNIQUE,1000,range=AREA_MONO,area=AREA_ALL_ENTITES,sussess=200,emoji='<a:CHAOS:762276118224961556>',cooldown=5,ultimate=True,use=None,message="PLEASE ! JUST A SIMPLE CHAOS !")
contrecoup = skill("Contre-coup","zm",TYPE_INDIRECT_DAMAGE,250,effect="ln",cooldown=2,emoji='<:aftershock:882889694269038592>',use=MAGIE)
boom = skill("Réaction en chaîne","zl",TYPE_INDIRECT_DAMAGE,250,effect="lv",cooldown=3,emoji='<:bimbamboum:873698494874017812>',use=MAGIE)
balayette = skill("Baleyette","zk",TYPE_DAMAGE,100,70,range=AREA_MONO,area=AREA_CIRCLE_1,emoji='<:baleyette:873924668963291147>',cooldown=2)
firstheal = skill("Premiers secours","zj",TYPE_HEAL,100,40,emoji="<:bandage:873542442484396073>")
cure = skill("Guérison","zi",TYPE_HEAL,250,80,cooldown=5,emoji='<:cure:873542385731244122>')
lightAura = skill("Aura de Lumière I","zh",TYPE_PASSIVE,250,effectOnSelf="ly",emoji="<:AdL:873548073769533470>")
splatbomb = skill("Bombe splash","zg",TYPE_DAMAGE,100,cooldown=4,area=AREA_CIRCLE_1,power=87,emoji='<:splatbomb:873527088286687272>',message="{0} lance une {1} sur {2} :")
explosion = skill("Explosion","KBOOM",TYPE_DAMAGE,1000,power=300,ultimate=True,cooldown=12,area=AREA_CIRCLE_2,shareCooldown=True,effectOnSelf="mb",use=MAGIE,emoji='<a:explosion:882627170944573471>',damageOnArmor=0.8)
explosionCast = skill("Explosion","zf",TYPE_DAMAGE,1000,0,ultimate=True,cooldown=7,area=AREA_CIRCLE_2,sussess=0,shareCooldown=True,effectOnSelf="na",use=MAGIE,emoji='<a:explosion:882627170944573471>',message="{0} rassemble son mana...")
protect = skill("Orbe défensif","ze",TYPE_ARMOR,200,emoji='<:orbeDef:873725544427053076>',effect="md",cooldown=3)
poisonus = skill("Vent empoisonné","zd",TYPE_INDIRECT_DAMAGE,500,emoji='<:estabistia:883123793730609172>',effect="me",cooldown=3,area=AREA_CIRCLE_1,use=MAGIE,message="{0} propage un {1} autour de {2} :",effPowerPurcent=40)
invocBat = skill("Invocation - Chauve-souris","zc",TYPE_SUMMON,500,invocation="Chauve-Souris",emoji="<:cutybat:884899538685530163>",shareCooldown=True,use=AGILITY)
multiMissiles = skill("Multi-Missiles","zb",TYPE_INDIRECT_DAMAGE,750,range=AREA_MONO,ultimate=True,emoji='<:tentamissile:884757344397951026>',effect="mf",cooldown=4,area=AREA_ALL_ENEMIES)
monoMissiles = skill("Mono-Missiles","za",TYPE_INDIRECT_DAMAGE,250,range=AREA_CIRCLE_7,emoji='<:monomissile:884757360193708052>',effect="mf",cooldown=4)
splashdown = skill("Choc Chromatique","yz",TYPE_DAMAGE,500,150,AREA_MONO,ultimate=True,emoji='<:splashdown:884803808402735164>',cooldown=8,area=AREA_CIRCLE_2,damageOnArmor=3)
invocCarbE = skill("Invocation - Carbuncle Emeraude","yy",TYPE_SUMMON,500,invocation="Carbuncle Emeraude",emoji="<:invoncEm:919857931158171659>",cooldown=3,range=AREA_CIRCLE_3,shareCooldown=True,use=MAGIE)
invocCarbT = skill("Invocation - Carbuncle Topaze","yx",TYPE_SUMMON,500,invocation="Carbuncle Topaze",emoji="<:invocTopaz:919859538943946793>",cooldown=3,range=AREA_CIRCLE_3,shareCooldown=True,use=ENDURANCE)
invocFee = skill("Invocation - Fée Soignante","yw",TYPE_SUMMON,500,0,AREA_CIRCLE_3,cooldown=4,invocation="Fée soignante",emoji="<:selene:885077160862318602>",shareCooldown=True,use=CHARISMA)
thinkSkill = skill("Réfléchis !","yv",TYPE_BOOST,250,0,emoji="<:think:885240853696765963>",effect="mh",use=CHARISMA,cooldown = 3)
descart = skill("Nous pensons donc nous somme","yu",TYPE_BOOST,250,range=AREA_MONO,area=AREA_CIRCLE_1,emoji="<:descartes:885240392860188672>",effect='mi',cooldown=4,use=None,message="{0} a trouvé le sens de la vie !")
trans = skill("Transcendance","yt",TYPE_UNIQUE,0,initCooldown=3,cooldown=5,emoji="<:limiteBreak:886657642553032824>",description="Un sort particulier qui a un effet différent en fonction de l'aspiration du lanceur\n\nUtiliser Transcendance vous empêche d'utiliser une compétence ultime lors du prochain tour",use=HARMONIE,shareCooldown=True)

transMelee = copy.deepcopy(trans)
transMelee.type,transMelee.power, transMelee.name = TYPE_DAMAGE,200, transMelee.name + " - Lasers Chromanergiques Prompts, Monocible"

transLine = copy.deepcopy(trans)
transLine.type,transLine.power,transLine.area, transLine.name = TYPE_DAMAGE,180,AREA_LINE_6, transLine.name + " - Lasers Chromanergiques Prompts, Ligne"

transCircle = copy.deepcopy(trans)
transCircle.type,transCircle.power,transCircle.area,transCircle.name, transCircle.cooldown = TYPE_DAMAGE,160,AREA_CIRCLE_2, transCircle.name + " - Explosion Prompte", transCircle.cooldown+1

transHeal = copy.deepcopy(trans)
transHeal.type,transHeal.power,transHeal.area,transHeal.range, transHeal.name, transHeal.cooldown = TYPE_HEAL,120,AREA_ALL_ALLIES,AREA_MONO, transHeal.name + " - Voie de l'Ange Prompte",7

transInvoc = copy.deepcopy(trans)
transInvoc.type, transInvoc.invocation, transInvoc.name  = TYPE_SUMMON,"Titania", transInvoc.name + " - La lumière brille brille brille"

transShield = copy.deepcopy(trans)
effTransShield = effect("Transcendance - Armure","transArm",HARMONIE,overhealth=150,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji("<a:transArmorB:900037831257358378>","<a:transArmorR:900037817449717800>"),turnInit=3)

transShield.type,transShield.area,transShield.range,transShield.effect,transShield.name, transShield.cooldown = TYPE_ARMOR,AREA_ALL_ALLIES,AREA_MONO,[effTransShield],transShield.name + " - Extra Armure d'Encre",7

burst = skill("Bombe ballon","ys",TYPE_DAMAGE,0,50,area=AREA_CIRCLE_1,sussess=70,emoji='<:burstBomb:887328853683474444>',use=HARMONIE,cooldown=2)
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
kiss = skill("Baisé divin","yg",TYPE_HEAL,69,75,AREA_DONUT_2,emoji='<:welp:893251469439008809>',message="{0} fait un gros bisou à {2} :")
onstage = skill("En scène !","yf",TYPE_BOOST,750,0,AREA_MONO,["exclusive","aspiration",IDOLE],True,effect="mr",emoji='<:alice:893463608716062760>',area=AREA_DONUT_7,use=CHARISMA,cooldown=5,message="{0} éléctrise l'ambience !")
icelance = skill("Lame glacée","ye",TYPE_DAMAGE,500,246,AREA_DIST_6,["exclusive","element",ELEMENT_WATER],True,emoji='<:emoji_47:893471252537298954>',cooldown=5,message="{0} fait appaître une lame de glace géante sous {2} :",use=MAGIE)
rocklance = skill("Lame rocheuse","yd",TYPE_DAMAGE,500,246,AREA_CIRCLE_3,["exclusive","element",ELEMENT_EARTH],True,emoji='<:emoji_46:893471231641276496>',cooldown=5,message="{0} fait appaître une lame de roche géante sous {2} :",use=MAGIE)
infinitFire = skill("Brasier","yc",TYPE_DAMAGE,500,172,AREA_DIST_5,["exclusive","element",ELEMENT_FIRE],True,emoji='<:emoji_44:893471208065101924>',cooldown=5,message="{0} déclanche un brasier autour de {2} :",area=AREA_LINE_3,use=MAGIE)
storm = skill("Ouragan","yb",TYPE_DAMAGE,500,172,AREA_CIRCLE_2,["exclusive","element",ELEMENT_AIR],True,emoji='<:emoji_44:893471179023732809>',cooldown=5,message="{0} déclanche un ouragan autour de {2} :",area=AREA_CIRCLE_2,use=MAGIE)
innerdarkness = skill("Ténèbres intérieurs","ya",TYPE_INDIRECT_DAMAGE,500,0,conditionType=["exclusive","element",ELEMENT_DARKNESS],ultimate=True,emoji='<:emoji_48:893471268957990982>',cooldown=5,effect="ms",use=MAGIE)
divineLight = skill("Lumière divine",'xz',TYPE_INDIRECT_HEAL,500,conditionType=["exclusive","element",ELEMENT_LIGHT],ultimate=True,emoji='<:emoji_49:893471282815963156>',cooldown=5,effect=["mu","mv"],use=CHARISMA,area=AREA_CIRCLE_1)
swordDance = skill("Dance des sabres","xy",TYPE_DAMAGE,350,power=70,use=STRENGTH,emoji='<:sworddance:894544710952173609>',cooldown=3,area=AREA_CIRCLE_1,range=AREA_MONO)
shot = skill("Tir net","xx",TYPE_DAMAGE,350,75,AREA_CIRCLE_6,emoji='<:shot:894544804321558608>',cooldown=5,use=STRENGTH,damageOnArmor=2)
percingLance = skill("Lance Perçante","xw",TYPE_DAMAGE,350,power=70,emoji='<:percing:894544752668708884>',cooldown=3,area=AREA_LINE_2,range=AREA_CIRCLE_2)
percingArrow = skill("Flèche Perçante","wv",TYPE_DAMAGE,350,power=70,emoji='<:percingarrow:887745340915191829>',cooldown=3,area=AREA_LINE_2,range=AREA_DIST_5)
highkick = skill("HighKick","wu",TYPE_DAMAGE,350,power=123,range=AREA_CIRCLE_1,emoji='<:highkick:894544734759030825>',cooldown=5,damageOnArmor=1.35)
multishot = skill("Tir Multiple","wt",TYPE_DAMAGE,350,power=70,range=AREA_DIST_4,emoji='<:name:894544834780622868>',cooldown=3,area=AREA_CONE_2)
bleedingArrow = skill("Flèche Hémoragique","ws",TYPE_DAMAGE,350,35,AREA_DIST_5,effect='mx',emoji='<:bleedingarrow:894544820071178292>')
bleedingDague = skill("Dague Hémoragique","wr",TYPE_DAMAGE,350,35,AREA_CIRCLE_2,effect='mx',emoji='<:bleedingdague:894552391444234242>')
affaiblissement = skill("Affaiblissement","wq",TYPE_MALUS,350,effect="my",cooldown=3,use=INTELLIGENCE,emoji='<:affaiblissement:894544690400071750>',area=AREA_CIRCLE_1)
provo = skill("Provocation","wp",TYPE_MALUS,350,emoji='<:supportnt:894544669793476688>',effect='mz',cooldown=3,use=INTELLIGENCE)
flameche = skill("Flamèche","wo",TYPE_DAMAGE,100,42,area=AREA_CONE_2,use=MAGIE,conditionType=["exclusive","element",ELEMENT_FIRE],emoji='<:flame1:897811975675969556>')
flame = skill("Flamme","wn",TYPE_DAMAGE,250,84,area=AREA_CONE_2,use=MAGIE,conditionType=["exclusive","element",ELEMENT_FIRE],cooldown=3,emoji='<:flame2:897812264185376798>')
pyro = skill("Pyrotechnie","wm",TYPE_DAMAGE,500,126,area=AREA_CONE_2,use=MAGIE,conditionType=["exclusive","element",ELEMENT_FIRE],cooldown=5,emoji='<:flame3:897812061139140651>')
ecume = skill("Ecume","wl",TYPE_DAMAGE,100,60,use=MAGIE,conditionType=["exclusive","element",ELEMENT_WATER],emoji='<:splash1:897844189184811078>')
courant = skill("Courant","wk",TYPE_DAMAGE,250,120,use=MAGIE,conditionType=["exclusive","element",ELEMENT_WATER],cooldown=3,emoji='<:splash2:897844205198659594>')
torant = skill("Torrant","wd",TYPE_DAMAGE,500,180,use=MAGIE,conditionType=["exclusive","element",ELEMENT_WATER],cooldown=5,emoji='<:splash3:897844380491202581>')
brise = skill("Brise","wj",TYPE_DAMAGE,100,42,use=MAGIE,conditionType=["exclusive","element",ELEMENT_AIR],area=AREA_CIRCLE_1,emoji='<:wind1:897845097775915038>')
storm2 = skill("Tempête","wi",TYPE_DAMAGE,250,84,use=MAGIE,conditionType=["exclusive","element",ELEMENT_AIR],area=AREA_CIRCLE_1,cooldown=3,emoji='<:wind2:897845144299110441>')
tornado = skill("Tornade","wh",TYPE_DAMAGE,500,126,use=MAGIE,conditionType=["exclusive","element",ELEMENT_AIR],area=AREA_CIRCLE_1,cooldown=5,emoji='<:wind3:897845187940868156>')
stone = skill("Caillou","wg",TYPE_DAMAGE,100,60,use=MAGIE,conditionType=["exclusive","element",ELEMENT_EARTH],emoji='<:rock1:897846015552532531>')
rock = skill("Rocher","wf",TYPE_DAMAGE,250,120,use=MAGIE,conditionType=["exclusive","element",ELEMENT_EARTH],cooldown=3,emoji="<:rock2:897846028512944138>")
mont = skill("Montagne","we",TYPE_DAMAGE,500,180,use=MAGIE,conditionType=["exclusive","element",ELEMENT_EARTH],cooldown=5,emoji='<:rock3:897846042576420874>')
stingray2 = skill("Pigmalance","wd",TYPE_DAMAGE,500,120,AREA_CIRCLE_7,ultimate=True,emoji='<:stingray:899243721378390036>',cooldown=5,area=AREA_LINE_6,sussess=110,description="Cette compétence dure **2** tours",damageOnArmor=0.66)
stingray = skill("Pigmalance","wc",TYPE_DAMAGE,500,100,AREA_CIRCLE_7,ultimate=True,emoji='<:stingray:899243721378390036>',cooldown=5,area=AREA_LINE_6,sussess=80,effectOnSelf="nb",damageOnArmor=0.66)
dark1 = skill("Cécité","wb",TYPE_DAMAGE,100,60,use=MAGIE,conditionType=["exclusive","element",ELEMENT_DARKNESS],emoji='<:dark1:899599162566410280>')
dark2 = skill("Obscurité","wa",TYPE_DAMAGE,250,120,use=MAGIE,conditionType=["exclusive","element",ELEMENT_DARKNESS],cooldown=3,emoji='<:dark2:899599147399807006>')
dark3 = skill("Pénombre","vz",TYPE_DAMAGE,500,180,use=MAGIE,conditionType=["exclusive","element",ELEMENT_DARKNESS],cooldown=5,emoji='<:dark3:899598969930399765>')
light1 = skill("Lueur","vy",TYPE_DAMAGE,100,42,use=MAGIE,conditionType=["exclusive","element",ELEMENT_LIGHT],area=AREA_CIRCLE_1,emoji='<:light1:899598879576690689>')
light2 = skill("Éclat","vx",TYPE_DAMAGE,250,84,use=MAGIE,conditionType=["exclusive","element",ELEMENT_LIGHT],area=AREA_CIRCLE_1,cooldown=3,emoji='<:light2:899598896613969970>')
light3 = skill("Éblouissement","vw",TYPE_DAMAGE,500,126,use=MAGIE,conditionType=["exclusive","element",ELEMENT_LIGHT],area=AREA_CIRCLE_1,cooldown=5,emoji='<:light3:899599232628043787>')
derobade = skill("Dérobade","vv",TYPE_BOOST,350,0,AREA_DONUT_3,cooldown=4,effectOnSelf="nd",effect="nc",emoji='<:derobade:899788297868558337>',use=INTELLIGENCE)
ferocite = skill("Férocité","vu",TYPE_PASSIVE,200,0,emoji='<:ferocite:899790356315512852>',effectOnSelf="ne",use=None)
ironWillSkill = skill("Volontée de Fer","vt",TYPE_PASSIVE,200,0,emoji='<:ironwill:899793931762565251>',effectOnSelf="nh",use=None)
royaleGardeSkill = skill("Garde Royale","vs",TYPE_PASSIVE,200,0,emoji='<:gardeRoyale:899793954315321405>',effectOnSelf="ng",use=None)
defi = skill("Défi","vr",TYPE_PASSIVE,200,0,emoji='<:defi:899793973873360977>',effectOnSelf="nf",use=None)
dissimulation = skill("Dissimulation","vq",TYPE_PASSIVE,0,effectOnSelf="nj",use=None,emoji="<:dissimulation:900083085708771349>")
bleedingTrap = skill("Piège de lacération","vp",TYPE_INDIRECT_DAMAGE,500,effect="mx",cooldown=3,area=AREA_CIRCLE_1,use=STRENGTH,message="{0} place et déclanche un {1} autour de {2} :",emoji='<:lacerTrap:900076484230774807>',effPowerPurcent=66)
# vn already taken (Prévention)
convert = skill("Convertion","vm",TYPE_ARMOR,350,range=AREA_DONUT_5,effect="nk",cooldown=3,emoji='<:convertion:900311843938115614>')
vampirisme = skill("Vampirisme","vl",TYPE_INDIRECT_HEAL,350,range=AREA_DONUT_5,effect="no",cooldown=3,emoji='<:vampire:900312789686571018>')
heriteEstialba = skill("Héritage - Fée d'Estialba","vk",TYPE_PASSIVE,0,effectOnSelf='np',emoji='<:heriteEstialba:900318953262432306>',use=MAGIE)
heriteLesath = skill("Héritage - Famille Lesath","vj",TYPE_PASSIVE,0,effectOnSelf='ns',emoji='<:hertiteLesath:900322590168608779>')
focal = skill("Focalisation","vi",TYPE_INDIRECT_DAMAGE,1000,range=AREA_CIRCLE_3,cooldown=7,effect=["me","me","me"],effectOnSelf="me",emoji='<:focal:901852405338099793>',shareCooldown=True,use=MAGIE,description="Applique 3 effets Poison d'Estialba à la cible, mais vous en donne un également")
suppr = skill("Suppression","vh",TYPE_DAMAGE,650,90,emoji='<:suppression:889090900326744085>',cooldown=5,use=MAGIE,damageOnArmor=3,sussess=80)
revitalisation = skill("Mot revitalisant","vg",TYPE_HEAL,300,50,area=AREA_CIRCLE_1,emoji="<:revita:902525429183811655>",cooldown=2)
onde = skill("Onde","vf",TYPE_ARMOR,500,effect="nv",cooldown=4,area=AREA_CIRCLE_1,emoji='<:onde:902526595842072616>')
eting = skill("Marque Eting","ve",TYPE_INDIRECT_HEAL,350,effect="nw",emoji='<:eting:902525771074109462>')
renforce = skill("Renforcement","vd",TYPE_BOOST,500,range=AREA_DONUT_5,effect="nx",cooldown=5,description="Une compétence qui augmente la résistance d'un allié. L'effet diminue avec les tours qui passent",use=INTELLIGENCE,emoji='<:renfor:921760752065454142>')
steroide = skill("Stéroïdes","vc",TYPE_BOOST,500,range=AREA_DONUT_5,effect="oa",cooldown=3,area=AREA_CIRCLE_1,use=INTELLIGENCE)
renisurection = skill("Résurrection","vb",TYPE_RESURECTION,500,100,emoji='<:respls:906314646007468062>',cooldown=4,shareCooldown=True,description="Permet de ressuciter un allié",use=CHARISMA)
demolish = skill("Démolition","va",TYPE_DAMAGE,650,150,AREA_CIRCLE_2,ultimate=True,cooldown=7,effect=incur[5],damageOnArmor=1.2,emoji='<:destruc:905051623108280330>')
contrainte = skill("Contrainte","uz",TYPE_MALUS,500,range=AREA_CIRCLE_6,effect=[incur[3],"oc"],cooldown=3,use=INTELLIGENCE)
trouble = skill("Trouble","uy",TYPE_MALUS,500,range=AREA_CIRCLE_6,effect=[incur[3],"od"],use=CHARISMA,emoji='<:trouble:904164471109468200>',cooldown=3)
epidemic = skill("Infirmitée","ux",TYPE_MALUS,500,area=AREA_CIRCLE_5,effect=incur[2],cooldown=3,use=None,emoji='<:infirm:904164428545683457>')
croissance = skill("Croissance","uw",TYPE_BOOST,500,effect="oe",cooldown=5,description="Une compétence dont les bonus se renforce avec les tours qui passent",use=CHARISMA,range=AREA_DONUT_5,emoji='<:crois:921760610985865246>')
destruction = skill("Météore","uu",TYPE_DAMAGE,1000,power=309,ultimate=True,cooldown=7,shareCooldown=True,effectOnSelf="mb",use=MAGIE,emoji='<:meteor:904164411990749194>',damageOnArmor=explosion.onArmor)
castDest = effect("Cast - Météore","nnnn",turnInit=2,silent=True,emoji=dangerEm,replique=destruction)
destruction2 = skill("Météore","uv",TYPE_DAMAGE,1000,power=0,ultimate=True,cooldown=7,effectOnSelf=castDest,use=MAGIE,shareCooldown=True,emoji=destruction.emoji,message="Une ombre plane au dessus de {2}...")
infectFiole = skill("Fiole d'infection","ut",TYPE_INDIRECT_DAMAGE,350,0,effect=["oh","oi"],cooldown=3,use=INTELLIGENCE,message="{0} lance une {1} sur {2}",emoji='<:fioleInfect:904164736407597087>')
bigLaser = skill("Lasers chromanergiques - Configuration Ligne","us",TYPE_DAMAGE,0,int(transLine.power*1.2),emoji='<:uLaserLine:906027231128715344>',area=AREA_LINE_6,sussess=95,damageOnArmor=1.33,ultimate=True,cooldown=7,description="Après un tour de chargement, déployez des drones énergétiques qui tirent un puissant rayon coloré en ligne droite")
bigLaserRep = effect("Cast - Las. Chrom. - Conf. Ligne","bigLaserEff",turnInit=2,silent=True,emoji=dangerEm,replique=bigLaser)
bigLaser2 = skill(bigLaser.name,"ur",bigLaser.type,750,0,area=bigLaser.area,emoji=bigLaser.emoji,effectOnSelf=bigLaserRep,ultimate=bigLaser.ultimate,cooldown=bigLaser.cooldown,message="{0} charge ses drones")
bigMonoLaser = skill("Lasers chromanergiques - Configuration Mono","uq",TYPE_DAMAGE,0,int(transMelee.power*1.2),emoji='<:uLaserMono:906027216989716480>',area=AREA_MONO,sussess=100,damageOnArmor=1.33,ultimate=True,cooldown=7,description="Après un tour de chargement, déployez des drones énergétiques qui tirent un puissant rayon coloré sur un adversaire depuis le ciel")
bigMonoLaserRep = effect("Cast - Las. Chrom. - Conf. Mono","bigMonoLaserEff",turnInit=2,silent=True,emoji=dangerEm,replique=bigMonoLaser)
bigMonoLaser2 = skill(bigMonoLaser.name,"up",bigMonoLaser.type,750,0,area=bigMonoLaser.area,emoji=bigMonoLaser.emoji,effectOnSelf=bigMonoLaserRep,ultimate=bigMonoLaser.ultimate,cooldown=bigMonoLaser.cooldown,message="Les drones de {0} s'envolent")
invocBat2 = skill("Invocation - Chauve-souris II","uo",TYPE_SUMMON,500,invocation="Chauve-Souris II",emoji="<:cuttybat2:904369379762925608>",shareCooldown=True,use=CHARISMA,cooldown=3)
invocCarbunR = skill("Invocation - Carbuncle Rubis","un",TYPE_SUMMON,500,invocation="Carbuncle Rubis",emoji="<:invocRuby:919857898195128362>",shareCooldown=True,use=MAGIE,cooldown=3)
concen = skill("Concentration","um",TYPE_BOOST,price=350,effect="oj",range=AREA_MONO,area=AREA_DONUT_2,cooldown=4,use=None,emoji='<:concen:921762263814262804>')
memAlice = skill("Memento - Voie de l'Ange","memAlice",TYPE_HEAL,1000,int(transHeal.power*1.3),AREA_MONO,shareCooldown=True,area=AREA_DONUT_4,cooldown=8,ultimate=True,use=CHARISMA,emoji='<a:memAlice2:908424319900745768>',description="Cette compétence soigne les alliés vivants et recussite les alliés morts pour une certaine valeur des soins initiaux, affectée par le niveau de votre personnage\nL'utilisation de cette compétence diminue vos PV maximums de **25%** et ajuste vos PV courants en conséquence")
memAliceCast = effect("Cast - {0}".format(memAlice.name),"aliceMementoCast",replique=memAlice,turnInit=2,silent=True,emoji=uniqueEmoji('<a:memAliceCast:908413832194588723>'))
memAlice2 = copy.deepcopy(memAlice)
memAlice2.id, memAlice2.power, memAlice2.effectOnSelf, memAlice2.message, memAlice2.emoji = "ul",0,memAliceCast,"{0} rassemble ses souvenirs...",'<a:memAliceCast:908413832194588723>'
blackHole = skill("Trou noir","uk",TYPE_PASSIVE,ironWillSkill.price,effectOnSelf="ol",use=None,emoji='<:blackHole:906195944406679612>')
blackHole2 = skill("Trou noir II","uj",TYPE_BOOST,0,use=None,effect=[intargetable,"on"],effectOnSelf="om",emoji='<:blackHole2:906195979332640828>',cooldown=7,initCooldown=2,description="Augmente sensiblement les chances d'être pris pour cible par l'adversaire, tout en rendant vos alliés aux corps à corps **Inciblable** et en redirigeant une partie de leurs dégâts sur vous",area=AREA_DONUT_1,range=AREA_MONO)
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
time3 = skill("Heure","tv",TYPE_DAMAGE,500,180,use=MAGIE,conditionType=["exclusive","element",ELEMENT_TIME],cooldown=5,emoji='<:time3:907474471240216658>')

timeSpEff = effect("Rembobinage","nigHotMF",CHARISMA,power=20,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,turnInit=3,emoji=uniqueEmoji('<:rollback:907687694476378112>'),stackable=True,description='Un effet de soin sur la durée qui se déclanche en début de tour')
timeSp = skill("Rembobinage","tu",TYPE_INDIRECT_HEAL,500,use=CHARISMA,range=AREA_MONO,area=AREA_CIRCLE_5,effect=timeSpEff,conditionType=["exclusive","element",ELEMENT_TIME],cooldown=7,ultimate=True,emoji='<:rollback:907687694476378112>')

spaceSp = skill("Pluie d'étoiles","tt",TYPE_DAMAGE,500,172,use=MAGIE,conditionType=["exclusive","element",ELEMENT_SPACE],cooldown=5,area=AREA_CIRCLE_2,ultimate=True,emoji='<:starFall:907687023140302908>')
idoOH = skill("Apothéose","ts",TYPE_PASSIVE,500,effectOnSelf="idoOHEff",emoji='<:IdoOH:909278546172719184>',conditionType=["exclusive","aspiration",IDOLE],use=None)
proOH = skill("Protection Avancée","tr",TYPE_PASSIVE,500,effectOnSelf="proOHEff",emoji='<:proOH:909278525528350720>',conditionType=["exclusive","aspiration",PROTECTEUR],use=None)
altOH = skill("Bénédiction","tq",TYPE_PASSIVE,500,effectOnSelf="altOHEff",emoji='<:altOH:909278509145395220>',conditionType=["exclusive","aspiration",ALTRUISTE],use=None)
lightAura2 = skill("Aura de Lumière II","tp",TYPE_PASSIVE,500,effectOnSelf="lightaura2Pa",emoji=lightAura.emoji,use=CHARISMA)

tripleMissilesLaunch = skill("Missiles téléguidés","tripleMissiles",TYPE_DAMAGE,750,120,ultimate=True,repetition=3,damageOnArmor=1.5,cooldown=10,emoji='<:missiles:909727253414445057>',conditionType=["exclusive","aspiration",OBSERVATEUR])
tripleMissilesEff2 = effect("Cast - {0}".format(tripleMissilesLaunch.name),"tripleMissilesEff2",turnInit=2,silent=True,emoji=sameSpeciesEmoji("<a:missileSoonB:909727376273965097>","<a:missilesSoonR:909727492510740501>"),replique=tripleMissilesLaunch)
tripleMissilesCast2 = copy.deepcopy(tripleMissilesLaunch)
tripleMissilesCast2.power, tripleMissilesCast2.message, tripleMissilesCast2.effectOnSelf, tripleMissilesCast2.id = 0,"{0} lance ses missiles",tripleMissilesEff2,"tripleMissilesCast"
tripleMissilesEff = effect("Cast - {0}".format(tripleMissilesLaunch.name),"tripleMissilesEff",turnInit=2,silent=True,emoji=uniqueEmoji('<:missilesCast:909727680264560690>'),replique=tripleMissilesCast2)
tripleMissiles = copy.deepcopy(tripleMissilesCast2)
tripleMissiles.effectOnSelf,tripleMissiles.message,tripleMissiles.say,tripleMissiles.id = tripleMissilesEff,"{0} calibre ses missiles","Ok, les missiles sont prêts pour le lancement !","to"

lightHeal2 = skill("Illumination","tn",TYPE_HEAL,350,60,cooldown=3,use=CHARISMA,conditionType=["exclusive","element",ELEMENT_LIGHT],emoji='<:illu:909134286203006997>')
extraEtingSkill = copy.deepcopy(eting)
extraEtingSkill.name, extraEtingSkill.id, extraEtingSkill.effect, extraEtingSkill.condition, extraEtingSkill.emoji = "Marque Eting +","tm",["eting+"],[0,2,ELEMENT_TIME],'<:emeB:909132040392302703>'

willShield = effect("Force de volonté","willShield",STRENGTH,overhealth=120,description="Votre force de volonté vous permet de vous protéger de quelques dégâts",turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
strengthOfWill = skill("Détermination inflexible","feliUltLaunch",TYPE_DAMAGE,0,power=200,cooldown=7,effectOnSelf=willShield,ultimate=True,emoji='<:feliSlash:916208942974132245>')
strengthOfWillCastEff = effect("Cast - Force de volonté","castFeliEff",turnInit=2,silent=True,emoji=dangerEm,replique=strengthOfWill)
strengthOfWillCast = copy.deepcopy(strengthOfWill)
strengthOfWillCast.id, strengthOfWillCast.power, strengthOfWillCast.effectOnSelf,strengthOfWillCast.message = "tl",0,strengthOfWillCastEff,"{0} rassemble toute sa Détermination dans son arme"

sixtineUlt = skill("Douce nuit","tk",TYPE_MALUS,0,range=AREA_MONO,area=AREA_ALL_ENEMIES,use=INTELLIGENCE,effect='sixtineUltEff',ultimate=True,cooldown=5,emoji='<:night:911735172901273620>')
hinaUlt = skill("Déluge de plume","tj",TYPE_DAMAGE,0,28,sussess=40,area=AREA_CONE_2,repetition=5,cooldown=7,emoji='<:featherStorm:909932475457884191>')
julieUltEff = effect("Prolongation","JulieUltEff",CHARISMA,power=15,turnInit=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,stackable=True,emoji=uniqueEmoji('<:prolong:911734437597835316>'),description="Un effet de soin sur la durée qui se déclanche en début de tour")
julieUlt = skill("Prolongation","ti",TYPE_INDIRECT_HEAL,0,area=AREA_CIRCLE_3,range=AREA_MONO,emoji='<:prolong:911734437597835316>',effect=julieUltEff,cooldown=7,use=CHARISMA)
invocSeraf = skill("Invocation - Fée protectrice","th",TYPE_SUMMON,500,invocation="Fée protectrice",emoji="<:seraphin:911078421361205289>",shareCooldown=True,use=INTELLIGENCE,cooldown=5)

mageUlt = skill("Éminence","tg",TYPE_DAMAGE,1000,emoji='<:emanence:911397114850975795>',power=120,conditionType=["exclusive","aspiration",MAGE],ultimate=True,cooldown=5,area=AREA_DONUT_2,use=MAGIE,description="Une compétence dont la puissance et la zone d'effet dépend de l'élément")
mageUltMono = copy.deepcopy(mageUlt)
mageUltMono.power,mageUltMono.area,mageUltMono.sussess = 150,AREA_MONO,160
mageUltZone = copy.deepcopy(mageUlt)
mageUltZone.power,mageUltZone.area,mageUltZone.sussess = 80,AREA_CONE_3,80

soulaEff = effect("Traité de soulagement","soulaArmor",INTELLIGENCE,overhealth=55,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=sameSpeciesEmoji('<:tsB:911732326818545664>','<:tsR:911732347601317908>'))
soulagement = skill("Traité de soulagement","tf",TYPE_ARMOR,500,0,AREA_MONO,["exclusive","aspiration",PREVOYANT],area=AREA_CIRCLE_2,use=INTELLIGENCE,cooldown=3,effect=soulaEff,emoji='<:soul:911732783993483284>')

bloodArmor = effect("Bouclier sanguin","bloodyArmor",STRENGTH,overhealth=50,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
bloodyStrike = skill("Frappe sanguine",'te',TYPE_DAMAGE,500,100,AREA_CIRCLE_2,["exclusive","aspiration",BERSERK],cooldown=5,effectOnSelf=bloodArmor,emoji='<:berkSlash:916210295867850782>')

infraMedicaEff = copy.deepcopy(julieUltEff)
infraMedicaEff.emoji, infraMedicaEff.power, infraMedicaEff.id, infraMedicaEff.name = sameSpeciesEmoji('<:imB:911732644193124393>','<:imR:911732657728151572>'), int(julieUltEff.power*1.35), "infraMedicaHeal", "Infra Medica"
infraMedica = skill("Infra Medica","td",TYPE_INDIRECT_HEAL,500,0,AREA_MONO,["exclusive","aspiration",ALTRUISTE],area=AREA_CIRCLE_2,cooldown=5,effect=infraMedicaEff,emoji='<:medica:911732802947530843>')

flambe = effect("Flambé","flambage",STRENGTH,type=TYPE_UNIQUE,power=10,aggro=10,description="Pour chaque attaque physique directe reçu par la cible, la puissance de cet effet augmente de {0} lors de son déclanchement, au début du prochain tour du lanceur",trigger=TRIGGER_ON_REMOVE,emoji=uniqueEmoji('<:flamb:913165325590212659>'))
flambeSkill = skill("Flambage","tc",TYPE_INDIRECT_DAMAGE,500,effect=flambe,cooldown=5,emoji='<:flamb:913165325590212659>')

magAch = effect("Magia atrocitas","magAch",MAGIE,type=TYPE_UNIQUE,power=flambe.power,aggro=10,description="Pour chaque attaque magique directe reçu par la cible, la puissance de cet effet augmente de {0} lors de son déclanchement, au début du prochain tour du lanceur",trigger=TRIGGER_ON_REMOVE,emoji=uniqueEmoji('<:magAch:913165311291842571>'))
magAchSkill = skill("Magia atrocitas","tb",TYPE_INDIRECT_DAMAGE,500,effect=magAch,cooldown=5,emoji='<:magAch:913165311291842571>')

idoOS = skill("Clou du spectacle","ta",TYPE_PASSIVE,500,effectOnSelf="idoOSEff",emoji='<:osIdo:913885207751446544>',conditionType=["exclusive","aspiration",IDOLE],use=None)
proOS = skill("Extra Protection","sz",TYPE_PASSIVE,500,effectOnSelf="proOSEff",emoji='<:osPro:913885191800512562>',conditionType=["exclusive","aspiration",PROTECTEUR],use=None)
preOS = skill("Armures Avancées","sy",TYPE_PASSIVE,500,effectOnSelf="preOSEff",emoji='<:osPre:913885175161712710>',conditionType=["exclusive","aspiration",PREVOYANT],use=None)

geoConBoost = effect("Géo-Controlé","geocontroled",INTELLIGENCE,20,20,20,10,10,20,20,5,5,0,description="Une grande force vous envahis",emoji=sameSpeciesEmoji("<:geoContB:918422778414256158>","<:geoContR:918422792649723914>"))
geoConLaunch = skill("Géo-Controle","geoControleFinal",TYPE_BOOST,1000,range=AREA_MONO,area=AREA_CIRCLE_3,effect=geoConBoost,cooldown=7,use=INTELLIGENCE,ultimate=True,emoji='<:geoCont:918422710781083668>')
geoConCastEff = effect("Cast - {0}".format(geoConLaunch.name),"geoControleCastEff",turnInit=2,silent=True,emoji=dangerEm,replique=geoConLaunch)
geoConCast = copy.deepcopy(geoConLaunch)
geoConCast.id, geoConCast.effect, geoConCast.effectOnSelf, geoConCast.message = "sx",[None],geoConCastEff,"{0} rassemble l'énergie cosmique autour de lui..."

kikuRes = skill("Mors vita est","sw",TYPE_RESURECTION,750,80,AREA_MONO,area=AREA_DONUT_3,emoji='<:mortVitaEst:916279706351968296>',initCooldown=3,shareCooldown=True,description="Utiliser cette compétence empêche l'équipe d'utiliser Memento - Voie de l'Ange, Résurrection ainsi que n'importe quelle Transcendance jusqu'au prochain tour",use=CHARISMA)
memClemLauchSkill = skill("Memento - L'Ange noir","memClemSkillLauch",TYPE_DAMAGE,0,666,AREA_MONO,sussess=666,area=AREA_CIRCLE_7,ultimate=True,use=MAGIE,cooldown=99,emoji="<:clemMemento:902222089472327760>",description="\n__Effets lors du premier tour de chargement :__\nDéfini vos PVs courants à **1**\nObtenez un bouclier absolu d'une valeur de **50%** des PVs perdus\nDivise votre Résistance Soins de **50%**\nDiminue vos PV maximums de **50%** pour le reste du combat\nDonne l'effet __Incurable (50)__ sur le lanceur pour le reste du combat")
memClemCastSkillEff = effect("Cast - Memento - L'Ange noir","memClemSkillCast",turnInit=2,silent=True,emoji=dangerEm,replique=memClemLauchSkill)
memClemCastSkill = copy.deepcopy(memClemLauchSkill)
memClemCastSkill.id, memClemCastSkill.effectOnSelf, memClemCastSkill.power = "sv",memClemCastSkillEff,0

rosesEff = effect("Épines","rosesEff",CHARISMA,endurance=5,resistance=3,power=35,trigger=TRIGGER_AFTER_DAMAGE,lvl=5,description="En plus de légèrement augmenter les statistiques défensives, cet effet inflige des dégâts indirects à chaques fois que le porteur reçois des dégâts **physiques**",onDeclancher=True,emoji=sameSpeciesEmoji("<:epineB:917665759684079626>","<:epineR:917665743649275904>"))
roses = skill("Épines","su",TYPE_BOOST,500,effect=rosesEff,use=CHARISMA,cooldown=5,range=AREA_DONUT_4,emoji='<:epines:917666041243500594>')
rosesMagicEff = effect("Pétales","rosesMagEff",CHARISMA,endurance=5,resistance=3,power=rosesEff.power,trigger=TRIGGER_AFTER_DAMAGE,lvl=rosesEff.lvl,description="En plus de légèrement augmenter les statistiques défensives, cet effet inflige des dégâts indirects à chaques fois que le porteur reçois des dégâts **magiques**",onDeclancher=True,emoji=sameSpeciesEmoji("<:rosesAreBlue:917665779770613761>","<:rosesAreRed:917665805557198878>"))
rosesMagic = skill("Pétales","sc",TYPE_BOOST,500,effect=rosesMagicEff,use=CHARISMA,cooldown=5,range=AREA_DONUT_4,emoji='<:roses:917666059413233704>')

krysUlt = skill("Réassemblage","st",TYPE_DAMAGE,0,80,cooldown=5,description="En plus d'infliger des dégâts, cette compétence vole **50%** de l'armure normale et légère de la cible (avant d'infliger les dégâts)",emoji='<:reconvert:916121466423091240>')
chaosArmorEff = effect("Armure du Chaos","chaosArmor",INTELLIGENCE,overhealth=1,description="Une armure chaotique dont la puissance de base est aléatoire",type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,turnInit=3)
chaosArmor = skill("Armure du Chaos","ss",TYPE_ARMOR,range=AREA_MONO,area=AREA_ALL_ALLIES,price=500,effect=chaosArmorEff,cooldown=5,use=INTELLIGENCE)

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
preciseShot = skill("Tir précis","sh",TYPE_DAMAGE,500,150,cooldown=5,use=PRECISION,emoji='<:preciseShot:916561817969500191>')
troublon = skill("Troublon","sg",TYPE_DAMAGE,500,70,cooldown=3,area=AREA_CONE_2,range=AREA_MONO,emoji='<:mousqueton:916561833920462889>')
haimaShield = effect("Haima - Bouclier","haimaShield",INTELLIGENCE,overhealth=20,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,emoji=sameSpeciesEmoji("<:haimaB:916922889679286282>","<:haimaR:916922905672171570>"))
haimaEffect = effect("Haima","haimaEff",lvl=5,description="En subissant des dégâts sans posséder d'effet \"__Haima - Bouclier__\", le porteur de cet effet gagne le dit effet au prix d'une charge de __Haima__",callOnTrigger=haimaShield,emoji=uniqueEmoji('<:haima:916922498094858251>'),trigger=TRIGGER_AFTER_DAMAGE)
haimaSkill = skill("Haima","sf",TYPE_ARMOR,500,emoji='<:haima:916922498094858251>',effect=haimaEffect,cooldown=7,use=INTELLIGENCE)
physicRune = skill("Rune - Sanguis Pact","se",TYPE_PASSIVE,750,effectOnSelf="pacteDeSang",emoji='<:pacteDeSang:917096147452035102>')
magicRune = skill("Rune - Animae Foedus","sd",TYPE_PASSIVE,750,effectOnSelf="pacteD'âme",emoji='<:pacteDame:917096164942295101>')
lightBigHealArea = skill("Lumière éclatante","sb",TYPE_HEAL,750,80,AREA_MONO,["exclusive","element",ELEMENT_LIGHT],True,area=AREA_CIRCLE_4,cooldown=7,use=CHARISMA,emoji='<:shiningLight:919514898784981012>')
focus = skill("Focus","sa",TYPE_INDIRECT_DAMAGE,1000,range=AREA_CIRCLE_3,cooldown=7,effect=["mx","mx","mx"],effectOnSelf="mx",shareCooldown=True,use=STRENGTH,description="Applique 3 effets Hémorragie à la cible, mais vous en donne un également",emoji='<:focus:919515555738820628>')
poisonusPuit = skill("Piliers magico-empoisoné","zzz",TYPE_DAMAGE,500,39,area=AREA_CIRCLE_1,use=MAGIE,effect=["me"],repetition=3,cooldown=7,emoji='<a:poisPillard:918424661631569960>')
bleedingPuit = skill("Pièges à ressorts","zzy",TYPE_DAMAGE,500,32,area=AREA_CIRCLE_1,effect=["mx"],repetition=3,cooldown=7,emoji='<a:shiTrap:919513726338625626>')
supprZone = skill("Dispersion","zzx",TYPE_DAMAGE,650,70,emoji='<:principio:919529034663223376>',cooldown=5,use=MAGIE,damageOnArmor=3,sussess=60,area=AREA_CIRCLE_1)
invocCarbSaphir = skill("Invocation - Carbuncle Saphir","zzw",TYPE_SUMMON,500,invocation="Carbuncle Saphir",emoji="<:innvocSafir:919857914490007574>",shareCooldown=True,use=STRENGTH,cooldown=3)
invocCarbObsi = skill("Invocation - Carbuncle Obsidienne","zzv",TYPE_SUMMON,500,invocation="Carbuncle Obsidienne",emoji="<:invocObs:919872508226830336>",shareCooldown=True,use=STRENGTH,cooldown=3)
requiem = skill("Requiem","zzu",TYPE_DAMAGE,500,23,range=AREA_MONO,area=AREA_CIRCLE_7,use=CHARISMA,cooldown=3,repetition=3,emoji='<:requiem:919869677197484052>')
cosmicEff = effect("Pouvoir cosmique","cosmicPowerEff",HARMONIE,strength=5,magie=5,resistance=5,emoji=sameSpeciesEmoji('<:comicPowerB:919866210768801833>','<:cosmicPowerR:919866197850353685>'),redirection=15)
cosmicEffSelf = effect("Pouvoir cosmique","cosmicPowerEffOnSelf",resistance=20,emoji=sameSpeciesEmoji('<:comicPowerB:919866210768801833>','<:cosmicPowerR:919866197850353685>'))
cosmicPower = skill("Pouvoir cosmique","zzt",TYPE_BOOST,1000,range=AREA_MONO,area=AREA_DONUT_2,use=HARMONIE,cooldown=7,emoji='<:cosmic:919866054992334848>',conditionType=["exclusive","element",ELEMENT_SPACE],effect=cosmicEff,effectOnSelf=cosmicEffSelf)
propag = skill("Propagation","zzs",TYPE_INDIRECT_DAMAGE,750,cooldown=5,ultimate=True,emoji='<:dispersion:919516925644648518>',use=MAGIE,effect=["me","mx"],description="Après la pose des effets de cette compétence, les alliés en mêlée de la cible reçoivent les effets __Poison d'Estialba__ et __Hémorragie__ de la cible pour une puissance équivalente à **{0}%** de la puissance de l'effet, pour la durée restante de l'effet de base\nSi vous n'êtes pas à l'origine de l'effet de base, la puissance de l'effet propagé équivaux à **{1}**% de la puissance de l'effet de base",power=30,effPowerPurcent=55)

inkResEff = effect("Pied au sec","inkRes",INTELLIGENCE,turnInit=2,inkResistance=10,description="Réduit de 10% les dégâts indirects reçu.\nLe pourcentage de réduction est affecté par l'Intelligence et le Bonus aux Armures et Mitigation")
inkResEff2 = copy.deepcopy(inkResEff)
inkResEff2.stat, inkResEff2.name, inkResEff2.emoji = ENDURANCE, "Collectivement inconscient", sameSpeciesEmoji('<:incColB:921546169203687464>','<:incColR:921546151314985020>')
inkRes = skill("Pied au sec","zzr",TYPE_BOOST,500,effect=inkResEff,cooldown=4,area=AREA_CIRCLE_1,use=INTELLIGENCE)
inkRes2 = skill("Inconscient collectif","zzq",TYPE_BOOST,500,range=AREA_MONO,area=AREA_CIRCLE_2,effect=inkResEff2,cooldown=4,use=ENDURANCE,emoji='<:incCol:921545816940875817>')

booyahBombLauch = skill("Jolizator","zzp",TYPE_DAMAGE,750,213,area=AREA_CIRCLE_2,ultimate=True,cooldown=7,emoji='<:bobomb:921710328771932192>')
booyahBombEff = effect("Cast - Jolizator","supercalifragilisticexpialiodocieux",turnInit=2,silent=True,emoji=dangerEm,replique=booyahBombLauch)
booyahBombCast = copy.deepcopy(booyahBombLauch)
booyahBombCast.id, booyahBombCast.effectOnSelf, booyahBombCast.power = "zzp",booyahBombEff,0

reconst = skill("Reconstitution","zzo",TYPE_HEAL,750,130,ultimate=True,use=CHARISMA,cooldown=7,emoji='<:mudh:922914512712138802>',description="Une puissante compétence de soins monocibles")
medicamentumEff = effect("Medicamentum","bigmonoindirect",CHARISMA,type=TYPE_INDIRECT_HEAL,turnInit=3,power=55,description="Un puissant effect soignant",emoji=sameSpeciesEmoji('<:mihB:922914323037306890>','<:mihR:922914344428240937>'))
medicamentum = skill("Rune - Medicamentum",'zzn',TYPE_INDIRECT_HEAL,750,ultimate=True,emoji='<:muih:922914495737757706>',cooldown=7,use=CHARISMA)

ultMonoArmorEff = effect("Armis","ultMonoArmor",INTELLIGENCE,overhealth=150,turnInit=3,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR)
ultMonoArmor = skill("Rune - Armis","zzm",TYPE_ARMOR,750,0,ultimate=True,effect=ultMonoArmorEff,cooldown=7,use=INTELLIGENCE)

# Skill
skills = [reconst,medicamentum,ultMonoArmor,
    inkRes,inkRes2,booyahBombCast,
    propag,invocCarbSaphir,invocCarbObsi,supprZone,cosmicPower,requiem,
    magicRuneStrike,infinitDark,preciseShot,troublon,haimaSkill,physicRune,magicRune,rosesMagic,lightBigHealArea,focus,poisonusPuit,bleedingPuit,
    idoOS,proOS,preOS,geoConCast,kikuRes,memClemCastSkill,roses,krysUlt,chaosArmor,firelame,airlame,waterlame,mudlame,shadowLame,timeLame,lightLame,astralLame,idoOH,proOH,altOH,lightAura2,tripleMissiles,lightHeal2,extraEtingSkill,strengthOfWillCast,sixtineUlt,hinaUlt,julieUlt,invocSeraf,mageUlt,soulagement,bloodyStrike,infraMedica,magAchSkill,flambeSkill,fireCircle,waterCircle,airCircle,earthCircle,fireShot,waterShot,airStrike,earthStrike,space1,space2,space3,spaceSp,time1,time2,time3,timeSp,renisurection,demolish,contrainte,trouble,epidemic,croissance,destruction2,infectFiole,bigLaser2,bigMonoLaser2,invocBat2,invocCarbunR,concen,memAlice2,blackHole,blackHole2,renforce,steroide,focal,suppr,revitalisation,onde,eting,stingray,dark1,dark2,dark3,light1,light2,light3,derobade,ferocite,ironWillSkill,royaleGardeSkill,defi,dissimulation,bleedingTrap,convert,vampirisme,heriteEstialba,heriteLesath,flameche,flame,pyro,ecume,courant,torant,brise,storm2,tornado,stone,rock,mont,bleedingArrow,bleedingDague,swordDance,shot,percingArrow,percingLance,highkick,multishot,rocklance,infinitFire,storm,innerdarkness,divineLight,icelance,onstage,kiss,secondSun,oneforall,uppercut,stalactic,linx,bombRobot,isolement,secondWind,blindage,adrenaline,lapSkill,burst,trans,descart,thinkSkill,invocFee,invocCarbT,invocCarbE,splashdown,multiMissiles,monoMissiles,invocBat,poisonus,protect,explosionCast,splatbomb,lightAura,cure,firstheal,balayette,contrecoup,boom,chaos,unHolly,soupledown,inkarmor,coffeeSkill,theSkill,gpotion,bpotion,zelian,courage,nostalgia,draw25,siropMenthe
]
