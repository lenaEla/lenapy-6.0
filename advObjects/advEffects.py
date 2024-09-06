from classes import *
from constantes import *
from advObjects.advSkills import *
from advObjects.advWeapons import purpleSecretEff, critBonusEff, liaKatanaEff

tankStans = ["ne","ng","nh","ol","nf"]
healStans = ["idoOHEff","proOHEff","altOHEff","ly","idoOSEff","proOSEff","preOSEff","lightaura2Pa"]
vulneEmoji = uniqueEmoji('<:vulne:930080488557793300> ')


the = effect("Théiné","lc", stat=CHARISMA,intelligence=10,magie=10,description="Boost l'agilité et la précision de tous les alliés",emoji=uniqueEmoji('<:the:867538602644602931>'))
encrifugeEff = effect("Tenue encrifugée - Armure","ld",overhealth=1,turnInit=2,trigger=TRIGGER_DAMAGE,absolutShield=True)
gpEffect = effect("Potion tonifiante","le",INTELLIGENCE,strength=5,magie=5,precision=5,turnInit=3,description="Vos connaissances en alchimie vous permettent de booster toutes vos statistiques pour le prochain tour")
bpEffect = effect("Potion étrange","lf",INTELLIGENCE,strength=-5,magie=-5,precision=-2,turnInit=3,description="Vos connaissances en alchimie vous permettent de baisser toutes les statistiques d'un adversaire pendant un tour",emoji = emojiMalus)
deterEff1 = effect("Détermination","lg",emoji=uniqueEmoji('<:determination:867894180851482644>'),turnInit=-1,lvl=1,description="Une fois par combat, en subissant des dégâts mortels, vous permet de transcender la mort et vous soigne de **{0}%** de vos PV max",power=50,type=TYPE_INDIRECT_HEAL,stat=PURCENTAGE)
onceButNotTwice = effect("Une fois mais pas deux","li",emoji=uniqueEmoji('<:notTwice:867536068110057483>'),description="La mort ne vous laissera pas filer une seconde fois",turnInit=-1,silent=True)
zelianR = effect("Chronoshift","lj",trigger=TRIGGER_ON_REMOVE,description = "À la fin de la durée de cet effet ou si le porteur reçoit des dégâts fatals, soigne ce dernier d'une valeur égale à **{0}%** des soins qu'il a reçut depuis que l'effet est actif",emoji=sameSpeciesEmoji('<:chronoshift1:867877564864790538>','<:chronoshift2:867877584518905906>'),type=TYPE_INDIRECT_HEAL,power=50,turnInit=3)
courageE = effect("Motivé","lk", stat=CHARISMA, strength=7.5, magie=7.5,emoji=sameSpeciesEmoji('<:charge1:866832660739653632>','<:charge2:866832677512282154>'),description="Augmente la force pendant un tour")
afterShockDmg = effect("Acharnement","ln", stat=MAGIE,turnInit=1,power=30,aggro=10,lvl=5,trigger=TRIGGER_DAMAGE,type=TYPE_INDIRECT_DAMAGE,emoji=sameSpeciesEmoji('<:aftershock1:882889524122898452>','<:aftershock2:882889538886852650>'),description="Lorsque la porteur reçoit des dégâts, le lanceur de la compétence lui inflige des dégâts indirects supplémentaire")
octoshield = effect("Bouclier Octarien","lo",overhealth=50,turnInit=-1,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,absolutShield=True,stat=ENDURANCE)
inkBrellaEff = effect("Toile du para-encre","lp", stat=PURCENTAGE,overhealth=25,turnInit=-1,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji='<:splatbrellareverse:876079630749147196>')
stopAttacking = effect("Stop attacking or draw 25","lq", stat=INTELLIGENCE,trigger=TRIGGER_DEALS_DAMAGE,type=TYPE_INDIRECT_DAMAGE,power=25,emoji=emojiMalus,description="Inflige des dégâts indirects au porteur si celui-ci attaque durant son tour")
hunter = effect("Chasseur","ls",None,emoji=uniqueEmoji('<:chasseur:871097673334276096>'),trigger=TRIGGER_DEATH,type=TYPE_UNIQUE,description="Un chasseur sachant chasser sans son chien a toujours une dernière carte à jouer",turnInit=-1)
hunterBuff = effect("Hunterbuff","lt",None,critical=100,precision=500,silent=True)
menthe = effect("Mentiné","lu", stat=CHARISMA,percing=3,resistance=3,critical=5,description="Boost la résistance, la pénétration et le critique de vos alliés",emoji=uniqueEmoji('<:menthe:867538622797054042>'))
badaboum = effect("Ça fait bim bam boum","lv", stat=MAGIE,aggro=10,turnInit=2,trigger=TRIGGER_DEATH,power=int(100*(1+AOEDAMAGEREDUCTION)),type=TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_2,emoji=sameSpeciesEmoji("<:deathBoomB:915050502369214474>","<:deathBoomR:915050526436102155>"),description="Lorsque le porteur meurt, cela délanche une explosion infligeant des dégâts à ses alliés alentours")
charme = effect("Sous le charme","lw", stat=CHARISMA,strength=-10,resistance=-5,magie=-10,description="Le porteur est distrait, ce qui diminue ses capacitées offensives et défensives",type=TYPE_MALUS,emoji=sameSpeciesEmoji("<:CharmeB:908793556435632158>","<:charmeR:908793574437584956>"),turnInit=2)
jetlag = effect("Jetlag",'jetLag',None,emoji=uniqueEmoji('<:jetlag:872181671372402759>'),silent=True,description="Le porteur de cet effet est insenssible aux sorts/armes de type \"Sablier\"")
lightAuraEffect = effect("Aura de Lumière I","ly", stat=CHARISMA,turnInit=-1,power=15,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_END_OF_TURN,emoji="<:lightAura:1133263881955967127>",description="À la fin du tour du porteur, lui et ses alliés proches reçoivent des soins",area=AREA_CIRCLE_2,reject=healStans)
flumEffect = effect("Douce lueur","lz", stat=CHARISMA,power=10,turnInit=-1,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji=uniqueEmoji('<:flum:876079513954557952>'),description="Soigne le porteur au début de son tour")
dephased = effect("Déphasée","ma",None,emoji=uniqueEmoji('<a:dephasee:882042949494525973>'),description="Ailill n'aime pas affronter trop d'ennemi à la fois, ni ceux qui essaye de l'avoir de loin",type=TYPE_UNIQUE,turnInit=-1)

defensive = effect("Orbe défensif","md",emoji=sameSpeciesEmoji('<:orbe1:873725384359837776>','<:orbe2:873725400730202123>'),resistance=5,overhealth=55,description='Donne de l\'armure à un allié',stat=INTELLIGENCE,trigger=TRIGGER_DAMAGE,turnInit=1,type=TYPE_ARMOR)
octoboum = effect("Explosion à venir !!","mg",emoji=uniqueEmoji('<a:explosion:882627170944573471>'),turnInit=3,aggro=20)
think = effect("REFLECHIS !","mh", stat=CHARISMA,intelligence=15,magie=15,turnInit=3)
iThink = effect("Philosophé","mi", stat=INTELLIGENCE,intelligence=15,magie=15,turnInit=3)
blinde = effect("Blindé","mj", stat=ENDURANCE,resistance=7,description="Réduit les degâts subis en fonction de l'Endurance du lanceur")
const = effect("Constitution","mk",emoji=uniqueEmoji('<:constitution:888746214999339068>'),description="Augmente de 5% les PV max de toute votre équipe",turnInit = -1)
nouil = effect("Œuil de Linx","mm", stat=PRECISION,emoji=uniqueEmoji('<:noeuil:887743235131322398>'),precision=10,block=10,critical=3,turnInit=2)
lostSoul = effect("Âme en peine","mn",emoji=uniqueEmoji('<:lostSoul:887853918665707621>'),turnInit=3,trigger=TRIGGER_ON_REMOVE,type=TYPE_UNIQUE)
oneforallbuff = effect("Un pour tous - Bonus","mo",resistance=10,stat=CHARISMA,description="Vos capacités défensives sont augmentées au détriment de celle du lanceur de cette compétence",emoji=sameSpeciesEmoji('<:one4allB:905243401157476423>','<:one4allR:905243417846636555>'))
oneforalldebuff = effect("Un pour tous - Malus","mp",resistance=-33,type=TYPE_MALUS,emoji=emojiMalus,description="Vos capacités défenses sont dimunuées pour augmenter celles de vos alliés")
secondSuneff = effect("Insomnie","mq", stat=CHARISMA,agility=-10,precision=-10,type=TYPE_MALUS,emoji=uniqueEmoji('<:MyEyes:784226383018328115>'),reject=["sixtineUltEff"],description="Vous êtes en train d'expérimenter la joie d'avoir un lampadaire devant une fênetre sans rideau")
lightspellshield = effect("Bouclier de lumière","mt", stat=INTELLIGENCE,overhealth=20,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji('<:lightspellbook:892963432222036018>'))
darkspellbookeff = effect("Eclair sombre","mw", stat=MAGIE,power=50,area=AREA_CIRCLE_1,stackable=True,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji=uniqueEmoji('<:darkspellbook:892963455773048914>'),turnInit=1)
affaiEffect = effect("Affaiblissement","my", stat=INTELLIGENCE,strength=-10,endurance=-10,resistance=-5,type=TYPE_MALUS,emoji=emojiMalus)
stupid = effect("Provoqué","mz", stat=INTELLIGENCE,charisma=-20,intelligence=-20,type=TYPE_MALUS,emoji=emojiMalus)
derobadeBonus = effect("Dérobade - Bonus","nc", stat=ENDURANCE,resistance=5,aggro=20,description="Un de vos alliés vous a gentiment inviter à prendre les coups à sa place",turnInit=2)
derobadeMalus = effect("Dérobade - Malus","nd", stat=ENDURANCE,aggro=-20,description="Vous avez fuis vos responsabilitées",type=TYPE_MALUS,turnInit=2)
ferociteEff = effect("Férocité","ne",stat=ENDURANCE,magie=10,aggro=35,block=15,turnInit=-1,emoji=uniqueEmoji('<:ferocite:899790356315512852>'),description="Vos grands airs augmentent les chances d'être attaqué par les ennemis",unclearable=True,reject=tankStans)
defiEff = effect("Défi","nf",stat=ENDURANCE,strength=10,aggro=35,block=15,turnInit=-1,emoji=uniqueEmoji('<:defi:899793973873360977>'),description="Vos grands airs augmentent les chances d'être attaqué par les ennemis",unclearable=True,reject=tankStans)
royaleGarde = effect("Garde Royale","ng",stat=ENDURANCE,intelligence=10,block=15,aggro=35,turnInit=-1,emoji=uniqueEmoji('<:gardeRoyale:899793954315321405>'),description="Vos grands airs augmentent les chances d'être attaqué par les ennemis",unclearable=True,reject=tankStans)
ironWill = effect("Volontée de Fer","nh",stat=ENDURANCE,charisma=10,aggro=35,block=15,turnInit=-1,emoji=uniqueEmoji('<:ironwill:899793931762565251>'),description="Vos grands airs augmentent les chances d'être attaqué par les ennemis",unclearable=True,reject=tankStans)
encrifugeEff2 = effect("Tenue Encrifugée","ni",callOnTrigger="ld",emoji=uniqueEmoji('<:encrifuge:871878276061212762> '),trigger=TRIGGER_START_OF_TURN,turnInit=-1,lvl=99,description="Une fois par tour, vous protège de 50 dégâts")
dissimulationEff = effect("Dissimulé","nj",aggro=-35,turnInit=-1,unclearable=True,description="Vous permet de réduire les chances d'être attaqué, mais réduit vos statistiques offensives et supports",emoji=sameSpeciesEmoji("<:dissiB:900130199826497536>","<:dissiR:900130215806779433>"))
convertArmor = effect("Armure","nl",type=TYPE_ARMOR,turnInit=5,emoji=stolenArmorEff.emoji,trigger=TRIGGER_DAMAGE,stackable=True,lightShield=True,silentRemove=True)
darkFlumPoi = effect("Ténèbres floraux","nu", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=sameSpeciesEmoji("<:dfB:922100203169923144>","<:dfR:922100216415518740>"),power=1,stackable=True,turnInit=3,lvl=3,description="Inflige des dégâts avec une puissance équivalante à **20%** du niveau du lanceur au début du tour du porteur")
darkFlumEff = effect("Fleur ténèbreuse","nt",turnInit=-1,description="En subissant des dégâts, applique l'effet \"Ténèbres floraux\" sur l'attaquant",emoji=uniqueEmoji('<:darkFlum:901849622685814814>'),callOnTrigger=darkFlumPoi,trigger=TRIGGER_AFTER_DAMAGE,thornEff=True)
ondeEff = effect("Onde","nv", stat=INTELLIGENCE,type=TYPE_ARMOR,overhealth=35,turnInit=5,emoji=uniqueEmoji('<:onde:902526595842072616>'),trigger=TRIGGER_DAMAGE,stackable=True)
renforceEff = effect("Renforcé","nx", stat=INTELLIGENCE,resistance=15,endurance=15,trigger=TRIGGER_ON_REMOVE,callOnTrigger="ny")
renforceEff2 = effect("Renforcé II","ny", stat=INTELLIGENCE,resistance=10,endurance=10,trigger=TRIGGER_ON_REMOVE,callOnTrigger="nz")
renforceEff3 = effect("Renforcé III","nz", stat=INTELLIGENCE,resistance=5,endurance=5)
steroideEff = effect("Stéroïde","oa", stat=INTELLIGENCE,strength=10,magie=10)
gwenCoupeEff = effect("Brûme sacrée","ob",emoji=uniqueEmoji('<:gwenZ:902913176562176020>'),turnInit=-1,unclearable=True,description="Vous confère 15% de chance d'obtenir l'effet **Inciblable** pendant 1 tour lorsque vous commencez votre tour")
contrainteEff = effect("Contrain","oc", stat=INTELLIGENCE,agility=-15,precision=-15,type=TYPE_MALUS)
croissanceEff = effect("Bourgeon","oe", stat=CHARISMA,strength=10,magie=10,resistance=5,trigger=TRIGGER_ON_REMOVE,callOnTrigger="of",emoji=uniqueEmoji('<:crois1:903976740869795910>'))
croissanceEff2 = effect("Jeune pousse","of", stat=CHARISMA,strength=15,magie=15,resistance=10,trigger=TRIGGER_ON_REMOVE,callOnTrigger="og",emoji=uniqueEmoji('<:crois2:903976762726289520>'))
croissanceEff3 = effect("Joli plante","og", stat=CHARISMA,strength=20,magie=20,resistance=15,emoji=uniqueEmoji('<:crois3:903976790530326578>'))
inkBrella2Eff = copy.deepcopy(inkBrellaEff)
inkBrella2Eff.id, inkBrella2Eff.emoji = "ok",uniqueEmoji("<:inkBrellaAltShield:905283041155514379>")
blackHoleEff = effect("Singularité","ol",stat=ENDURANCE,aggro=35,block=15,inkResistance=5,turnInit=-1,unclearable=True,reject=tankStans,description="Augmente considérablement les chances d'être pris pour cible par l'adversaire et réduit légèrement les dégâts indirects reçus",emoji='<:blackHole:906195944406679612>')
fireCircleEff = effect("Foyer","oo", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=50,emoji='<:fireCircle:906219518760747159>')
waterCircleEff = effect("Syphon","op", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=70,emoji='<:waterCircle:906219492135276594>')
airCircleEff = effect("Oeuil de la tempête","oq", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=50,emoji='<:airCircle:906219469200842752>')
earthCircleEff = effect("Epicentre","or", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=70,emoji='<:earthCircle:906219450129317908>')
idoOHEff = effect("Apothéose","idoOHEff",emoji=uniqueEmoji('<:IdoOH:909278546172719184>'),turnInit=-1,power=25,description="Vous motivez vos alliés plus que jamais !\n\n**{0}**% de vos sur-soins sont donnés en armure\n\n__<:idoOHArmor:909278702783836170> Overheath - Idole :__\nArmure Légère : Les armures légères n'absorbent pas de dégâts supplémentaires lors de leurs destructions\nEffet Remplaçable : Les effets remplaçables sont remplassés si le même effet avec une meilleure puissance est donné",unclearable=True,reject=healStans)
proOHEff = effect("Protection anticipée","proOHEff",emoji=uniqueEmoji('<:proOH:909278525528350720>'),turnInit=-1,power=25,description="Vous avez réusi à surpasser vos limites !\n\n**{0}**% de vos sur-soins sont donnés en armure\n\n__<:proOHArmor:909278718575394837> Overheath - Protecteur :__\nArmure Légère : Les armures légères n'absorbent pas de dégâts supplémentaires lors de leurs destructions\nEffet Remplaçable : Les effets remplaçables sont remplassés si le même effet avec une meilleure puissance est donné",unclearable=True,reject=healStans)
altOHEff = effect("Bénédiction","altOHEff",emoji=uniqueEmoji('<:altOH:909278509145395220>'),turnInit=-1,power=35,description="Votre dévotion pour vos alliés vous permet de passer à la vitesse supérieur !\n\n**{0}**% de vos sur-soins sont donnés en armure\n\n__<:aoa:909278749143490601>  Overheath - Altruiste :__\nArmure Légère : Les armures légères n'absorbent pas de dégâts supplémentaires lors de leurs destructions\nEffet Remplaçable : Les effets remplaçables sont remplassés si le même effet avec une meilleure puissance est donné",unclearable=True,reject=healStans)
lightAura2ActiveEff = effect("Charge de Lumière","lightaura2Ac", stat=CHARISMA,trigger=TRIGGER_AFTER_DAMAGE,turnInit=2,stackable=True,type=TYPE_INDIRECT_HEAL,power=10,lvl=4,description="Les 4 prochaines attaques que vous receverez déclancheront un effet de soins autour de vous",area=AREA_CIRCLE_2,emoji="<:lightAura21:1106836834572582952>",silentRemove=True)
lightAura2PassiveEff = effect("Eclat de Lumière","lightaura2Pa", stat=CHARISMA,turnInit=-1,trigger=TRIGGER_START_OF_TURN,type=TYPE_BOOST,unclearable=True,emoji="<:lightAura2:1106836809083781120>",callOnTrigger=lightAura2ActiveEff,description="Octroie \"Charge Lumineuse\" à chaques début de tours",reject=healStans)
enchant = effect("Enchanté","enchantBuffEff",None,turnInit=-1,silent=True,type=TYPE_UNIQUE,unclearable=True,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji(aspiEmoji[ENCHANTEUR]))
proMalus = effect("Protecteur - Malus","nb",stat=HARMONIE,strength=-5,magie=-5,type=TYPE_MALUS,silent=True,emoji=uniqueEmoji('<:proMalus:903137298001047573>'),stackable=False)
astralShield = effect("Armure Astrale","astShield",type=TYPE_ARMOR,turnInit=99,emoji=uniqueEmoji('<:astralShield:907467906483367936>'),trigger=TRIGGER_DAMAGE,lightShield=True)
timeShield = effect("Armure Temporelle","timeShield",type=TYPE_ARMOR,turnInit=99,emoji=uniqueEmoji('<:tempoShield:907467936975945758>'),trigger=TRIGGER_DAMAGE,lightShield=True)
idoOHArmor = effect("Apothéose","idoOHArmor",overhealth=1,type=TYPE_ARMOR,turnInit=3,trigger=TRIGGER_DAMAGE,lightShield=True,emoji='<:idoOHArmor:909278702783836170>',replace=True)
proOHArmor = effect("Protection anticipée","proOHArmor",overhealth=1,type=TYPE_ARMOR,turnInit=3,trigger=TRIGGER_DAMAGE,lightShield=True,emoji='<:proOHArmor:909278718575394837>',replace=True)
altOHArmor = effect("Bénifiction","altOHArmor",overhealth=1,type=TYPE_ARMOR,turnInit=3,trigger=TRIGGER_DAMAGE,lightShield=True,emoji='<:aoa:909278749143490601>',replace=True)

chaosEff = effect("Boîte à malice","chaosed", stat=STRENGTH,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji=uniqueEmoji('<:surprise:904916065778274304>'))

idoOSEff = effect("Clou du spectacle","idoOSEff",emoji=uniqueEmoji('<:osIdo:913885207751446544>'),turnInit=-1,power=30,description="Lorsque vous donnez une armure, réduit de **{1}**% les pertes dû au malus d'armure cumulée\nLorsque l'une de vos armures est détruite, celle-ci absorbe des dégâts supplémentaires équivalants à **{0}**% de votre niveau",unclearable=True,reject=healStans)
proOSEff = effect("Seconde Couche","proOSEff",emoji=uniqueEmoji('<:osPro:913885191800512562>'),turnInit=-1,power=30,description="Lorsque vous donnez une armure, réduit de **{1}**% les pertes dû au malus d'armure cumulée\nLorsque l'une de vos armures est détruite, celle-ci absorbe des dégâts supplémentaires équivalants à **{0}**% de votre niveau",unclearable=True,reject=healStans)
preOSEff = effect("Armures avancées","preOSEff",emoji=uniqueEmoji('<:osPre:913885175161712710>'),turnInit=-1,power=50,description="Lorsque vous donnez une armure, réduit de **{1}**% les pertes dû au malus d'armure cumulée\nLorsque l'une de vos armures est détruite, celle-ci absorbe des dégâts supplémentaires équivalants à **{0}**% de votre niveau",unclearable=True,reject=healStans)

dptStans = ["ns","np",physicRuneEff1.id,magicRuneEff1.id,"purpleSecrets",critBonusEff.id]
purpleSecretEff.reject = critBonusEff.reject = heriteLesathEff.reject = heriteEstialbaEff.reject = physicRuneEff1.reject = magicRuneEff1.reject = dptStans

charming = effect("Miryoku","kitsuneSisterEff", stat=CHARISMA,strength=-2,magie=-2,charisma=-2,intelligence=-2,stackable=True,type=TYPE_MALUS,description="Réduit vos statistiques et augmente les dégâts subis de la part des kitsunes",emoji=sameSpeciesEmoji("<:charm1B:1105349312126386226>","<:charm1R:1105349381848305714>"),turnInit=2)
charming2 = effect("Kantan","kitsuneSisterEffBuff", stat=CHARISMA,strength=5,magie=5,charisma=5,intelligence=5,stackable=True,type=TYPE_BOOST,description="Augmente vos statitiques et augmente les soins et armures reçus de la part des kitsunes",emoji=sameSpeciesEmoji("<:charm2B:1105349280539103273>","<:charm2R:1105349341448773703>"),turnInit=2)

clemExOvershield = effect("Armure Sanguine","clemExOvershield",turnInit=20,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji="<:clemMemento2:902222663806775428>",absolutShield=True)
cicatrisationEff = effect("Cicatrisation","chipCica",PURCENTAGE,emoji=getChip("Cicatrisation").emoji,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_END_OF_TURN,turnInit=-1,unclearable=True)
lythophageEff = effect("Lithophage",'chipLytho',FIXE,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_END_OF_TURN,emoji=getChip("Lithophage").emoji)
overshieldEff = effect("Overhealth","chipOverhealth",FIXE,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji='<:clemMemento2:902222663806775428>',absolutShield=True,turnInit=3,silentRemove=True,replace=True)
openingGambitEff = effect("Opening Gambit","openingGambitEff",PURCENTAGE,turnInit=-1,unclearable=True,emoji="<:OpeningGambit:1217580002120306750>")
lastDitchEffortEff = effect("Last Ditch Effort","lastDitchEffortEff",PURCENTAGE,turnInit=-1,unclearable=True,emoji="<:lastDitchEffort:1216413813079937125>")

precautionEff2 = effect("Précaution","precautioEff2",PURCENTAGE,power=5,turnInit=5,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji=getChip("Précaution").emoji)
precautionEff = effect("Précaution","precautionEff",callOnTrigger=precautionEff2,trigger=TRIGGER_ON_REMOVE,turnInit=2,emoji=rarityEmojis[getChip("Précaution").rarity])
tmpChip = getChip("Présence")
presenceEff = effect(tmpChip.name,"présenceEff",aggro=25,emoji=rarityEmojis[tmpChip.rarity],turnInit=-1,unclearable=True)
toxiceptionEff2 = effect("Toxiception","toxiceptEff2",inkResistance=-50,type=TYPE_MALUS,decateOnTurn=True,turnInit=2,stackable=True)
toxiceptionEff = effect("Toxiception","toxiceptEff1",type=TYPE_MALUS,trigger=TRIGGER_START_OF_TURN,callOnTrigger=toxiceptionEff2,stackable=True, silentRemove=True,emoji='<:toxiEff:1223595956415496213>')

#Effect
effects = [liaKatanaEff,windDanceEff,imuneLightStun,critBonusEff,idoOHEff,proOHEff,altOHEff,lightAura2PassiveEff,sixtineUltEff,idoOSEff,proOSEff,preOSEff,physicRuneEff1,magicRuneEff1,purpleSecretEff,fireCircleEff,waterCircleEff,airCircleEff,earthCircleEff,renforceEff,renforceEff2,renforceEff3,steroideEff,gwenCoupeEff,contrainteEff,troubleEff,croissanceEff,croissanceEff2,croissanceEff3,infection,infectRej,ConcenEff,inkBrella2Eff,blackHoleEff,blackHoleEff3,heriteEstialbaEff,estal2,bleeding2,heriteLesathEff,darkFlumEff,darkFlumPoi,ondeEff,etingEff,encrifugeEff2,ferociteEff,defiEff,royaleGarde,ironWill,dissimulationEff,pigmaCast,derobadeBonus,derobadeMalus,castExplo,affaiEffect,stupid,bleeding,innerdarknessEff,darkspellbookeff,lighteff,lightHealeff,lightspellshield,secondSuneff,oneforallbuff,oneforalldebuff,lostSoul,nouil,isoled,const,blinde,iThink,think,octoboum,missiles,estial,defensive,flumEffect,lightAuraEffect,jetlag,charme,armor,coffee,the,encrifugeEff,gpEffect,bpEffect,deterEff1,onceButNotTwice,zelianR,afterShockDmg,octoshield,nostalgiaE,inkBrellaEff,stopAttacking,hunter,hunterBuff,menthe,badaboum,courageE
]

def findEffect(effectId) -> effect:
    if type(effectId) == effect:
        return effectId
    elif type(effectId) != str:
        
        return None
    else:
        rep,id = None,effectId
        for a in effects:
            if a.id == id or a.name.lower() == id.lower():
                rep = a
                break
    
        return rep
