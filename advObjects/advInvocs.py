from classes import *
from constantes import *
from advObjects.advSkills import *
from advObjects.advWeapons import ironSword

batWeap = weapon("Griffe","aaa",RANGE_MELEE,AREA_CIRCLE_2,50,100,0,emoji='<:griffe:884889931359596664>',use=STRENGTH,ignoreAutoVerif=True)
carbunTWeap = weapon("Griffe","aaa",RANGE_MELEE,AREA_CIRCLE_1,90,80,0,emoji='<:griffe:884889931359596664>',use=ENDURANCE,ignoreAutoVerif=True)
carbunE = weapon("Coup de vent","aab",RANGE_LONG,AREA_CIRCLE_5,80,70,0,emoji='<:vent:884889843681853460>',area=AREA_CIRCLE_1,use=MAGIE,ignoreAutoVerif=True)
carbunSkill = skill("Eclat Emeraude","aac",TYPE_DAMAGE,0,120,area=AREA_CIRCLE_2,accuracy=100,emoji='<:rafale:884889889445912577>',use=MAGIE,cooldown=4,description="Inflige des dégâts dans une large zone autour de la cible")
carbunTSKill = skill("Eclat de Topaze","aad",TYPE_DAMAGE,0,100,AREA_MONO,area=AREA_CIRCLE_2,accuracy=80,cooldown=4,emoji="<:eclattopaze:884889967397056512>",use=ENDURANCE,description="Inflige des dégâts dans une large zone autour du Carbuncle Topaze")
feeWeap = weapon("Embrassement","aae",RANGE_DIST,AREA_CIRCLE_4,60,100,0,type=TYPE_HEAL,use=CHARISMA,emoji="<:feerie:885076995522834442>",target=ALLIES,area=AREA_CIRCLE_1)
feeEffect = effect("Murmure de l'aurore","aaf",CHARISMA,type=TYPE_INDIRECT_HEAL,power=50,emoji=uniqueEmoji('<:murmure:1066827511712976947>'),trigger=TRIGGER_START_OF_TURN,turnInit=3,stackable=True)
feeSkill = skill("Murmure de l'aurore","seleneSkills1",TYPE_INDIRECT_HEAL,0,0,AREA_MONO,cooldown=3,area=AREA_CIRCLE_3,emoji="<:feerie:885076995522834442>",effects=feeEffect,description="Donne un effet régénérant aux alliés autours de la Fée Soignante")
feeSkill2Eff = copy.deepcopy(absEff)
feeSkill2Eff.power = 20
feeSkill2 = skill("Illumination Féérique","seleneSkills2",TYPE_BOOST,effects=feeSkill2Eff,range=AREA_MONO,area=AREA_CIRCLE_3,description="Augmente les soins reçus par la Fée Soignante et ses alliés alentours",cooldown=3,emoji='<:illuminationFeerique:1066827334063247371>')

titWeap = weapon("Rune de Malice","titaniaWeapo,n",RANGE_MELEE,AREA_CIRCLE_1,50,80,repetition=3,emoji='<:magicalBonk:886669168408137749>',area=AREA_CONE_2,use=MAGIE,ignoreAutoVerif=True) 
lapinoWeap = weapon("Murmure de guérison","aai",RANGE_DIST,AREA_CIRCLE_3,50,100,0,0,0,0,0,0,0,0,0,0,0,'<:defHeal:885899034563313684>',use=CHARISMA,type=TYPE_HEAL,target=ALLIES,message="{0} encourage doucement {1} :")
lapinoSkill = skill("Murmure de dévoument","aaj",TYPE_HEAL,0,100,emoji='<:defHeal:885899034563313684>',cooldown=4,description="Soigne l'allié ciblé")
autoWeap = weapon("NoneWeap","NoneWeap",RANGE_MELEE,AREA_CIRCLE_1,0,0,0,emoji="<:noneWeap:917311409585537075>")
autoEff = effect("Auto-destruction","aam",trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,power=99999,emoji=emojiMalus,silent=True)
autoSkill = skill("Explosion","aan",TYPE_DAMAGE,0,200,AREA_MONO,emoji='<:exploShotEff:1049704001257619476>',area=AREA_CIRCLE_1,effectOnSelf=autoEff,accuracy=200,setAoEDamage=True,description="Inflige des dégâts en zone autour de la Bombe Robot, puis s'auto détruit à la fin du tour*")
lapinoSkill2 = skill("Murmure d'Abnégation","lapinoSkill2",TYPE_HEAL,power=150,use=CHARISMA,cooldown=3,description="Soigne l'allié ciblé mais le Lapino est vaincu par la suite",effectOnSelf=autoEff)
cutyBatSkill1Eff = effect("Motivé Bis","batMotivEff",stat=CHARISMA,strength=7,magie=7,charisma=7,intelligence=7)
cutyBatSkill1 = skill("Motivation de la Chauve-Souris","batMotiv",TYPE_BOOST,0,0,AREA_CIRCLE_3,area=AREA_CIRCLE_2,use=CHARISMA,cooldown=4,effects=cutyBatSkill1Eff,description="Augmente la Force, la Magie, le Charisme et l'Intelligence des alliés proches de la Chauve-Souris II")
cutyBatSkill2Eff = effect("Renforcement Bis","batRenforceEff",stat=INTELLIGENCE,endurance=7,resistance=3,block=20,emoji=uniqueEmoji('<:egide:887743268337619005>'))
cutyBatSkill2 = skill("Renforcement de la Chauve-Souris","batRenforce",TYPE_BOOST,0,0,range=AREA_DONUT_5,area=AREA_CIRCLE_1,cooldown=3,emoji='<:egide:887743268337619005>',effects=cutyBatSkill2Eff,description="Augmente l'Endurance et la Résistance de l'allié ciblé")
sonarPafEff = effect("Marqué","sonarPafMark",dodge=-15,description="Réduit la probabilité d'esquiver une attaque",turnInit=1,type=TYPE_MALUS,emoji='<:sonar:1013742380026953758>')
cutyBatSkill3Eff = effect("Onde Sonore","batEcho",CHARISMA,power=50,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT)
cutyBatSkill3 = skill("Echolocalisation","batEcho",TYPE_MALUS,0,0,AREA_CIRCLE_4,area=AREA_CIRCLE_2,effects=[cutyBatSkill3Eff,sonarPafEff],cooldown=3,description="Diminue l'Agilité des ennemis affectés",use=CHARISMA)
cutyBatWeap = weapon("Onde sonore","noneWeap",RANGE_DIST,AREA_CIRCLE_5,32,100,effectOnUse=incur[3],use=CHARISMA)
carbunRWeap = weapon("Griffe enflammé","rubyWeap",RANGE_MELEE,AREA_CIRCLE_1,52,100,use=MAGIE,emoji=batWeap.emoji)
carbunRSkill1 = skill("Pyrotechnie du Carbuncle","rubySkill",TYPE_DAMAGE,0,125,AREA_CIRCLE_2,cooldown=3,use=MAGIE,description="Inflige des dégâts à l'ennemi ciblé",emoji='<:enemyFire:1042312985407930428>')
curbunRSkill2Eff = effect("Flamme éternelle","fire",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=50,lvl=3)
carbunRSkill2 = skill("Flammes éternelles","rubySkill2",TYPE_DAMAGE,0,100,AREA_CIRCLE_3,effects=curbunRSkill2Eff,cooldown=3,use=MAGIE,description="Inflige des dégâts à l'ennemi ciblé tout en lui infligeant un effet de dégâts indirects",emoji='<:hellFlame:1066671455166808074>')
carbunRSKill3Eff = copy.deepcopy(dmgUp)
carbunRSKill3Eff.power = 30
carbunRSKill3 = skill("Stimulation Rubis","rubySkill3",TYPE_BOOST,effects=carbunRSKill3Eff,range=AREA_MONO,replay=True,cooldown=3,emoji='<:stimulationRubis:1066673877238939749>',description="Augmente les dégâts infligés par le carbuncle de **{0}%** jusqu'à son prochain tour et lui permet de rejouer son tour".format(carbunRSKill3Eff.power))

serafWeaponEff = effect("Voile Séraphique","serafWeapShield",INTELLIGENCE,overhealth=50,stackable=True,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,emoji='<:voileSeraphique:1066814843044249610>')
serafWeapon = weapon("Bénédiction séraphique","serafWeap",RANGE_DIST,AREA_CIRCLE_5,power=serafWeaponEff.power,accuracy=100,effectOnUse=serafWeaponEff,type=TYPE_HEAL,use=INTELLIGENCE,emoji='<:dictameB:911078870936084551>',target=ALLIES)
serafSkill = skill("Dictame","dictame",TYPE_ARMOR,0,0,range=AREA_MONO,area=AREA_CIRCLE_2,effects=serafWeaponEff,cooldown=3,use=INTELLIGENCE,emoji=serafWeapon.emoji,description="Octroi une armure aux allié proches de la Fée Protectrice\n__Puissance de l'armure :__ **{armor}**")
allianceFeeriqueEff = copy.deepcopy(defenseUp)
allianceFeeriqueEff.power = 20
serafSkill2 = skill("Alliance Féérique",'serapSkill2',TYPE_BOOST,effects=allianceFeeriqueEff,cooldown=3,description="Réduit les dégâts subis par la Fée Protectrice et ses alliés alentours",emoji='<:fairyAlliance:1066815782086004766>',range=AREA_MONO,area=AREA_CIRCLE_3)

GESLweap = weapon("noneWeap","aaa",1,AREA_CIRCLE_1,0,0,0)
GESLskill = skill("Piétinement Physique","TheGiantEnnemySpiderLeft",TYPE_DAMAGE,0,40)
GESRskill = skill("Piétinement Magique","TheGiantEnnemySpiderRigth",TYPE_DAMAGE,0,GESLskill.power,use=MAGIE)

carbOb = weapon("Griffe d'obsidienne","carObWeap",RANGE_MELEE,AREA_CIRCLE_1,30,70,repetition=3,emoji=batWeap.emoji)
carbObSkill = skill("Eclat d'Obsidenne","carbObsiSkill",TYPE_DAMAGE,0,135,AREA_CIRCLE_2,cooldown=3,emoji='<:carbSkill2:919859568685752350>',description="Inflige des dégâts autour du Carbuncle Obsidienne")
carbObSkill2Eff = effect("Pelotenement Obsidienne","obsStim",dodge=35,aggro=50,emoji='<:pelotonementObsidienne:1066671611136192574>')
carbObSkill2 = skill("Pelotonement Obsidienne",'carbObsSkill2',TYPE_BOOST,effects=carbObSkill2Eff,cooldown=3,replay=True,description="Augmente l'aggression du Carbuncle Obsidienne et ses chances d'esquiver des attaques en lui permettant de rejouer son tour",emoji=carbObSkill2Eff.emoji[0][0])
carbSa = weapon("Tir de glacée","carbSaWeap",RANGE_DIST,AREA_CIRCLE_6,56,80,0)
carbSaSkill = skill("Eclat de Saphir","carbSaSkill",TYPE_DAMAGE,0,120,cooldown=3,emoji='<:carbSkill2:919859581381926933>',description="Inflige des dégâts à l'ennemi ciblé")
carbSaSkill2Eff = copy.deepcopy(vulne)
carbSaSkill2Eff.power = 15
carbSaSkill2 = skill("Saphir Scintillant","carSaphSkill2",TYPE_DAMAGE,power=80,effects=carbSaSkill2Eff,description="Inflige des dégâts à l'ennemi ciblé et augmente les dégâts qu'il subit jusqu'au prochain tour du Carbuncle Saphir",emoji='<:saphirScintillant:1066671545000415283>',cooldown=3,effBeforePow=True)

seekerSkill = skill("Traque",'seekerSkill',TYPE_DAMAGE,0,150,AREA_RANDOMENNEMI_1,area=AREA_CIRCLE_1,tpCac=True,effectOnSelf=autoEff,areaOnSelf=True)
killerWailWeap = copy.deepcopy(autoWeap)
killerWailWeap.use, killerWailWeap.range = MAGIE, RANGE_LONG
killerWailSkill = skill("Rayon sonique","killerWail5.1SumSkill",TYPE_DAMAGE,0,100,AREA_CIRCLE_5,area=AREA_LINE_6,effectOnSelf=autoEff,use=MAGIE,setAoEDamage=True,emoji='<:kwShot:933510363398418432>')
titSkill1 = skill("Rune de Feu","titSkill1",TYPE_DAMAGE,0,125,area=AREA_CIRCLE_1,setAoEDamage=True,cooldown=3,use=MAGIE,description="Inflige des dégâts de zone dans une petite zone autour de la cible\nNon affecté par la réduction de dégâts de zone")
titSkill2 = skill("Rune de Gel","titSkill2",TYPE_DAMAGE,0,100,range=AREA_DIST_5,area=AREA_CIRCLE_2,cooldown=3,use=MAGIE,description="Inflige des dégâts de zone dans une large zone autour de la cible")
titSkill3_1 = skill("Rune d'Illusion","titSkill3",TYPE_DAMAGE,power=150,range=AREA_MONO,area=AREA_CIRCLE_2,setAoEDamage=True,cooldown=3,use=MAGIE)
titSkill3_2 = skill("Rune d'Illusion","titSkill3",TYPE_DAMAGE,power=80,range=AREA_MONO,area=AREA_DIST_7,setAoEDamage=True,cooldown=3,use=MAGIE)
titSkill3 = skill("Rune d'Illusion","titSkill3",TYPE_DAMAGE,become=[titSkill3_1,titSkill3_2],use=MAGE,description="Effectue des dégâts magiques autour de Titania ou dans un donut large centrée autour d'elle\n__Puissances :__ **{0}**, **{1}**\nNon affecté par la réduction de dégâts de zone".format(titSkill3_1.power,titSkill3_2.power),area=AREA_CIRCLE_1)
autTourWeap = weapon("Tir à la volée","autoTourWeap",RANGE_LONG,AREA_CIRCLE_6,125,100,ignoreAutoVerif=True,emoji='<:rookWeap:983594054199701544>',use=PRECISION)
autFouWeap = copy.deepcopy(autoWeap)
autFouWeap.use, autFouWeap.range = INTELLIGENCE, RANGE_DIST
autFouSkill1Eff, autFouSkill2Eff, autFouSkill2Armor = copy.deepcopy(vulne), copy.deepcopy(dmgUp), effect("Mortier d'ether bénéfique","autFouSkill2Armor",INTELLIGENCE,overhealth=50,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,emoji=sameSpeciesEmoji("<:mortarB:983594992708751410>","<:mortarR:983595021859184650>"))
autFouSkill1Eff.power, autFouSkill1Eff.stat, autFouSkill2Eff.power, autFouSkill2Eff.stat = 7, INTELLIGENCE, 7, INTELLIGENCE
autFouSkill1 = skill("Mortier d'ether néfaste","autFouSkill1",TYPE_MALUS,effects=autFouSkill1Eff,area=AREA_CIRCLE_3,use=INTELLIGENCE,range=AREA_MONO,effectAroundCaster=[TYPE_DAMAGE,AREA_DONUT_3,80],cooldown=3,emoji='<:mortarR:983595021859184650>',description="Augmente les dégâts reçus par les ennemis à portée et leur inflige des dégâts\n__Puissance des dégâts :__ 80\n__Puissance de l'augmentation de dégâts subis :__ 7% (Intelligence)")
autFouSkill2 = skill("Mortier d'ether bénéfique","autFouSKill2",TYPE_BOOST,effects=[autFouSkill2Eff,autFouSkill2Armor],area=AREA_CIRCLE_3,range=AREA_MONO,emoji='<:mortarB:983594992708751410>',description="Augmente les dégâts infligés par les alliés à portée et leur procure une armure\n__Puissance de l'augmentation des dégâts infligés :__ 7%\n__Puissance de l'armure :__ 50")
autQueenWeap = weapon("Coup de poings","autQueenWeap",RANGE_MELEE,AREA_CIRCLE_1,80,200,emoji='<:queenWeap:983594110025863189>',ignoreAutoVerif=True)
autQueenSkill1 = skill("Roue véloce","autQueenSkill1",TYPE_DAMAGE,power=50,range=AREA_INLINE_4,tpCac=True,replay=True,emoji='<:queenDash:983594130338902066>',description="L'auto tourelle reine charge un ennemi et rejoue son tour")
autQueenSkill2 = skill("Marteau Piqueur","autQueenSkill2",TYPE_DAMAGE,range=AREA_CIRCLE_1,power=180,accuracy=200,damageOnArmor=3,emoji='<:queenColi:983595079916736542>',cooldown=3,description="L'auto tourelle reine porte une puissance attaque sur l'ennemi ciblé avec une précision parfaite. Dégâts triplés sur l'armure")
pipisSkill = skill("Auto-Pipisation","autopipisboom",TYPE_DAMAGE,power=150,range=AREA_MONO,area=AREA_CIRCLE_3,effectOnSelf=autoEff,initCooldown=3)
pipisWeap = copy.deepcopy(autoWeap)
lightButterflyWeap = weapon("Lueur Volatile","lightButterflyWeap",RANGE_DIST,AREA_CIRCLE_5,power=65,accuracy=100,use=CHARISMA,type=TYPE_HEAL,target=ALLIES,ignoreAutoVerif=True,emoji='<:light1:1095249264105508874>')
lightButterflySkill1 = skill("Eclats Lumineux","lightButterflySkill1",TYPE_HEAL,power=75,range=AREA_MONO,area=AREA_CIRCLE_3,emoji='<:light3:1095249327376584794>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
lightButterflySkill2Eff = effect("Bénédiction Lumineuse","lightButterflySkill2Eff",CHARISMA,type=TYPE_INDIRECT_HEAL,power=50,turnInit=3,trigger=TRIGGER_START_OF_TURN,stackable=True,emoji='<:light2:1095249294388383764>')
lightButterflySkill2 = skill("Bénédiction Concentrique","lightButterflySkill2",TYPE_INDIRECT_HEAL,effects=lightButterflySkill2Eff,use=CHARISMA,emoji='<:light2:1095249294388383764>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
lightButterflySkill3 = skill("Bénédiction Lumineuse","lightButterflySkill3",TYPE_INDIRECT_HEAL,effects=lightButterflySkill2Eff,use=CHARISMA,effPowerPurcent=40,area=AREA_CIRCLE_1,range=AREA_CIRCLE_4,emoji='<:light2:1095249294388383764>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
mrLifeWeap = weapon("Sifflement","mrLifeWeap",RANGE_DIST,AREA_CIRCLE_4,power=30,use=CHARISMA,ignoreAutoVerif=True,accuracy=60)
mrLifeSkill1Eff = effect("Ralentisment","mrLifeSkill1Eff",CHARISMA,agility=-7,precision=-7,turnInit=3,type=TYPE_MALUS,stackable=True)
mrLifeSkill1 = skill("Ralentissement","mrLifeSkill1",TYPE_MALUS,effects=mrLifeSkill1Eff,cooldown=3,description="Réduit l'agilité et la précision de la cible",range=AREA_CIRCLE_4)
mrLifeSkill2 = skill("Ralentissement Avancé","mrLifeSkill2",TYPE_MALUS,effects=mrLifeSkill1Eff,cooldown=3,description="Réduit l'agilité et la précision des ennemis alentours",range=AREA_MONO,area=AREA_CIRCLE_4,effPowerPurcent=40)
skeletonWeap = weapon("Epée nécromantique","skeletonWeap",RANGE_MELEE,AREA_CIRCLE_2,batWeap.power,batWeap.accuracy,0,strength=10,magie=10,use=MAGIE,emoji=ironSword.emoji,ignoreAutoVerif=True)

hinoroWeapon = weapon("Flamme Ecarlate","noneweap",RANGE_DIST,AREA_CIRCLE_3,60,80,emoji='<:phenixSkill1_2:1066006794549329980>',use=MAGIE)
hinoroRegen2 = effect("Flamme éternelle","hinoroRegen2",MAGIE,power=50,turnInit=3,emoji='<:flammeEternelle:1066085228998836246>',trigger=TRIGGER_START_OF_TURN,stackable=True,type=TYPE_INDIRECT_HEAL)
hinoroRegen = effect("Ravivement","hinoroRegen",MAGIE,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_HP_ENDER_70,turnInit=3,callOnTrigger=hinoroRegen2,lvl=1,emoji='<:ravivement:1066085083796221952>',stackable=True)
hinoroPassiveEff = effect("Vol du Phénix","phenixFlight",MAGIE,area=AREA_DONUT_3,callOnTrigger=phoenixFlight,trigger=TRIGGER_INSTANT,emoji='<:summonHinoro:1066006465225171005>')
hinoroPassive = skill("Vol du Phénix","hinoroPassive",TYPE_PASSIVE,effectOnSelf=hinoroPassiveEff,emoji=hinoroPassiveEff.emoji[0][0],description="Octroi {0} {1} aux alliés autour d'Hinoro lorsqu'il est invoqué".format(phoenixFlight.emoji[0][0],phoenixFlight.name))
hinoroSkill1 = skill("Flamme de Vie","hinoroSkill1",TYPE_DAMAGE,power=125,cooldown=5,emoji='<:phenixSkill1_1:1066006765340196995>',effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_LOWEST_HP_ALLIE,hinoroRegen],description="Inflige des dégâts monocibles à l'ennemi ciblé et octroi une régénération à l'allié ayant le moins de PV")
hinoroSkill2 = skill("Tissons du Purgatoire","hinoroSkill2",TYPE_DAMAGE,use=MAGIE,power=110,area=AREA_CIRCLE_1,cooldown=5,emoji='<:phenixSkill1_2:1066006794549329980>',effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_LOWEST_HP_ALLIE,hinoroRegen],description="Inflige des dégâts aux ennemis ciblés et octroi une régénération à l'allié ayant le moins de PV")
hinoroSkill3 = skill("Révélation","hinoroSkill3",TYPE_DAMAGE,use=MAGIE,cooldown=5,power=95,area=AREA_CIRCLE_2,effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_CIRCLE_3,phoenixFlight],effPowerPurcent=55,emoji='<:phenixSkill2:1066006837637427242>',description="Inflige des dégâts aux ennemis ciblés et octroi une régénération aux alliés alentours")

sonarPafSkill = skill("Sonar Paf","sonarPafSkill",TYPE_DAMAGE,power=50,use=STRENGTH,range=AREA_MONO,area=AREA_CIRCLE_3,effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_3,sonarPafEff])
sonarPafSmn = invoc("Sonar Paf",[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.7],[PURCENTAGE,0],25,0,0,ASPI_NEUTRAL,["<:spb:1013743128253042699>","<:spr:1013743154048020561>"],GESLweap,[sonarPafSkill],description="Inflige des dégâts et {0} {1} aux ennemis autour de lui, réduisant leur esquive".format(sonarPafEff.emoji[0][0],sonarPafEff.name))
batInvoc = invoc("Chauve-Souris",aspiration=POIDS_PLUME,strength=[HARMONIE,0.35],endurance=[PURCENTAGE,0.35],charisma=[PURCENTAGE,0.35],agility=[PURCENTAGE,0.35],precision=[PURCENTAGE,0.35],intelligence=[PURCENTAGE,0.35],magie=[PURCENTAGE,0.35],resistance=20,percing=0,critical=0,icon=["<:bat1:884519906819862568>","<:bat2:884519927208357968>"],gender=GENDER_FEMALE,weapon=batWeap,description="Une invocation de mêlée peu resistante, mais pouvant submerger les ennemis",element=ELEMENT_AIR)
carbuncleE = invoc("Carbuncle Emeraude",[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0.7],20,10,[PURCENTAGE,1],MAGE,["<:carbEmR:919858018739437568>",'<:carbEmB:919857996274749451>'],carbunE,[carbunSkill,sillage],description="Une invocation utilisant des compétences de zone pour vaincre des groupes d'ennemis de loin",element=ELEMENT_AIR)
carbuncleT = invoc("Carbuncle Topaze",[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.1],0,10,PROTECTEUR,["<:ct1:884889748274028666>","<:ct2:884889807111749662>"],carbunTWeap,[carbunTSKill],description="Une invocation résistante qui n'a pas froid au yeux et viendra sauter dans la mêlée",element=ELEMENT_EARTH)
feeInv = invoc("Fée Soignante",[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.7],10,0,0,ALTRUISTE,["<:fee1:885076945333805086>","<:fee2:885076961695760386>"],feeWeap,[feeSkill,feeSkill2],gender=GENDER_FEMALE,description="Une fée qui soigne ses alliés grace à sa magie curative pouvant également augmenter les soins reçus par les alliés",element=ELEMENT_LIGHT)
titania = invoc("Titania",[PURCENTAGE,0.3],[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0.7],25,10,20,ENCHANTEUR,["<:tita1:886663550796431390>","<:tita2:886663565220651028>"],titWeap,[titSkill1,titSkill2,titSkill3],GENDER_FEMALE,element=ELEMENT_UNIVERSALIS_PREMO,description="Une invocation magique qui inflige de lourd dégâts de zone")
lapino = invoc("Lapino",[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.3],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.5],10,0,0,ALTRUISTE,['<:lapino1:885899366966112266>','<:lapino2:885899382539571221>'],lapinoWeap,[lapinoSkill,eting,lapinoSkill2],description="Fidèle Lapino d'Hélène, il la suit partout là où elle aura besoin de lui",element=ELEMENT_LIGHT)
autoBomb = invoc("Bombe Robot",[PURCENTAGE,0.8],50,0,0,0,0,0,20,0,0,POIDS_PLUME,["<:auto1:887747795497394267>","<:auto2:887747819866312735>"],autoWeap,[autoSkill])
darkness = invoc("Conviction des Ténèbres",0,-25,0,0,0,0,0,0,0,0,ASPI_NEUTRAL,['<:infiniteDarkness:898497770531455008>','<:infiniteDarkness:898497770531455008>'],autoWeap,gender=GENDER_FEMALE,element=ELEMENT_DARKNESS)
cutyBat = invoc("Chauve-Souris II",strength=[PURCENTAGE,0.5],endurance=[PURCENTAGE,0.3],charisma=[PURCENTAGE,0.7],agility=[PURCENTAGE,0.7],precision=[PURCENTAGE,0.5],intelligence=[PURCENTAGE,0.7],magie=[PURCENTAGE,0.5],resistance=[PURCENTAGE,1],percing=0,critical=0,aspiration=IDOLE,icon=['<:bat2B:904368975952085012>','<:bat2R:904368991710101515>'],weapon=cutyBatWeap,skills=[cutyBatSkill1,cutyBatSkill2,cutyBatSkill3],gender=GENDER_FEMALE,description="Une chauve-souris spécialisée dans le soutien")
carbunR = invoc("Carbuncle Rubis",strength=[PURCENTAGE,0.5],endurance=[PURCENTAGE,0.7],charisma=[PURCENTAGE,0.5],agility=[PURCENTAGE,0.7],precision=[PURCENTAGE,0.7],intelligence=[PURCENTAGE,0.5],magie=[PURCENTAGE,0.7],resistance=[PURCENTAGE,1],percing=[PURCENTAGE,1],critical=25,aspiration=ENCHANTEUR,icon=['<:carbunRB:904368034200834089>','<:carbunRR:904368049547776010>'],weapon=carbunRWeap,skills=[carbunRSkill1,carbunRSkill2,carbunRSKill3],description="Un carbuncle de mêlée infligeant des dégâts magiques",element=ELEMENT_FIRE)
seraf = invoc("Fée protectrice",strength=[PURCENTAGE,0.5],endurance=[PURCENTAGE,0.5],charisma=[PURCENTAGE,0.5],agility=[PURCENTAGE,0.3],precision=[PURCENTAGE,0.5],intelligence=[PURCENTAGE,0.7],magie=[PURCENTAGE,0.5],resistance=[PURCENTAGE,1],percing=0,critical=0,aspiration=PREVOYANT,icon=['<:seraphB:911078241404608522>','<:seraphR:911078257078706256>'],weapon=serafWeapon,skills=[serafSkill,serafSkill2],description="Une fée octroyant des armures aux alliés et réduisant les dégâts qu'ils subissent",element=ELEMENT_LIGHT,gender=GENDER_FEMALE)
TGESL1 = invoc("Patte de The Giant Enemy Spider",[PURCENTAGE,0.5],[PURCENTAGE,0.3],0,[PURCENTAGE,0.7],[PURCENTAGE,0.7],0,0,[PURCENTAGE,0.3],0,0,ASPI_NEUTRAL,['<:TGESlegs2:917303003936063538>','<:TGESlegs2:917303003936063538>'],GESLweap,[GESLskill],gender=GENDER_FEMALE)
TGESL2 = copy.deepcopy(TGESL1)
TGESL2.strength, TGESL2.magie, TGESL2.icon, TGESL2.skills[0] = 0,TGESL1.strength,['<:TGESlegs1:917302968104144906>','<:TGESlegs1:917302968104144906>'],GESRskill
seeker = invoc("Traqueur",[PURCENTAGE,0.7],[PURCENTAGE,0.1],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.7],[PURCENTAGE,0.3],[PURCENTAGE,0.3],0,[PURCENTAGE,1],[PURCENTAGE,1],BERSERK,['<:seekerB:933508361863954432>','<:seekerR:933508377584234606>'],autoBomb.weapon,[seekerSkill],description="Une machine qui se téléporte sur une cible aléatoire puis explose (Puissance : {0}, Zone : Cercle de 1)".format(seekerSkill.power))
killerWailSum = invoc("Haut-Perceur 5.1",[PURCENTAGE,0.3],[PURCENTAGE,0.1],[PURCENTAGE,0.3],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.3],[PURCENTAGE,0.7],0,[PURCENTAGE,1],[PURCENTAGE,1],OBSERVATEUR,['<:kwB:933510332733882378>','<:kwR:933510345488736346>'],killerWailWeap,[killerWailSkill],description="Une machine qui tire un laser sonique sur toute sa ligne, infligeant des dégâts aux ennemis s'y trouveant, puis s'auto-détruit (Puissance : {0}, non affecté par la réduction de dégâts de zone)".format(killerWailSkill.power),canMove=False)
autTour = invoc("Auto tourelle Tour",[PURCENTAGE,0.7],[PURCENTAGE,0.3],[PURCENTAGE,0.1],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.3],[PURCENTAGE,0.1],[PURCENTAGE,1],[PURCENTAGE,1],[PURCENTAGE,0.7],OBSERVATEUR,["<:autoTowB:982946185247588372>","<:autoTowR:982946121901019136>"],autTourWeap,description="Une invocation stationnaire dont les attaques à l'arme font de bons dégâts et ont une bonne précision",canMove=False,gender=GENDER_FEMALE)
autFou = invoc("Auto tourelle Fou",[PURCENTAGE,0.3],[PURCENTAGE,0.5],[PURCENTAGE,0.1],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.7],[PURCENTAGE,0.1],[PURCENTAGE,1],[PURCENTAGE,1],[PURCENTAGE,0.7],INOVATEUR,["<:autoFouB:982946138502098944>","<:autoFouR:982946204046462987>"],autFouWeap,[autFouSkill1,autFouSkill2],description="Une invocation stationnaire qui peut affaiblir les ennemis ou galvaniser les alliés autour d'elle",canMove=False,gender=GENDER_FEMALE)
autQueen = invoc("Auto tourelle Reine",[PURCENTAGE,0.7],[PURCENTAGE,0.7],[PURCENTAGE,0.1],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.1],[PURCENTAGE,0.1],[PURCENTAGE,1],[PURCENTAGE,1],[PURCENTAGE,0.7],ASPI_NEUTRAL,["<:autoQueenB:982946221599641610>","<:autoQuennR:982946154222354442>"],autQueenWeap,[autQueenSkill1,autQueenSkill2],description="Une invocation de mêlée pouvant réaliser de bon dégâts et qui manque rarement sa cible",gender=GENDER_FEMALE)
carbObsi = invoc("Carbuncle Obsidienne",strength=[PURCENTAGE,0.7],endurance=[PURCENTAGE,0.5],charisma=[PURCENTAGE,0.5],agility=[PURCENTAGE,0.7],precision=[PURCENTAGE,0.5],intelligence=[PURCENTAGE,0.5],magie=[PURCENTAGE,0.3],resistance=[PURCENTAGE,1],percing=[PURCENTAGE,1],critical=[PURCENTAGE,0.5],aspiration=POIDS_PLUME,icon=['<:carbObsiB:919857954029707284>','<:carObsiR:919857975051558954>'],weapon=carbOb,skills=[carbObSkill,carbObSkill2],element=ELEMENT_DARKNESS,description="Un Carbucle de mêlée infligeant des dégâts physiques")
carbSaphir = invoc("Carbuncle Saphir",strength=[PURCENTAGE,0.7],endurance=[PURCENTAGE,0.5],charisma=[PURCENTAGE,0.5],agility=[PURCENTAGE,0.5],precision=[PURCENTAGE,0.7],intelligence=[PURCENTAGE,0.5],magie=[PURCENTAGE,0.3],resistance=[PURCENTAGE,0.5],percing=[PURCENTAGE,1],critical=[PURCENTAGE,1],aspiration=OBSERVATEUR,icon=["<:ce1:884889724114841610>","<:ce2:884889693374775357>"],weapon=carbSa,skills=[carbSaSkill,carbSaSkill2],element=ELEMENT_WATER,description="Un Carbuncle distant infligeant des dégâts physiques et réduisant les défenses de la cible")
pipis = invoc("Pipis",[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.3],[PURCENTAGE,0.1],[PURCENTAGE,1],[PURCENTAGE,1],[PURCENTAGE,0.7],ASPI_NEUTRAL,["<:pipis:984865081672212491>","<:pipis:984865081672212491>"],pipisWeap,[pipisSkill])
lightButterfly = invoc("Papillon de Lumière",[PURCENTAGE,0.3],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.3],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.5],25,0,15,ALTRUISTE,["<:blum:992495387812311060>","<:rlum:992495404933455974>"],lightButterflyWeap,[lightButterflySkill1,lightButterflySkill2,lightButterflySkill3],description="Un papillon pouvant soigner les combattants alliés, efficace aussi bien en zone qu'en monocible",element=ELEMENT_LIGHT)
mrLifeSavor = invoc("Mr. Lifesavor",[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,1],[PURCENTAGE,0.5],[PURCENTAGE,1],[PURCENTAGE,0.7],[PURCENTAGE,0.7],30,10,15,INOVATEUR,["<:mrLifeSavor:1009824241954324561>","<:mrLifeSavor:1009824241954324561>"],mrLifeWeap,[mrLifeSkill1,mrLifeSkill2],description="Sifflet animé de Lime Cookie, Mr Lifesavor prend garde à ce que personne ne court à côté de la piscine\nPeut réduire l'agilité et la précision ses ennemis")
skeleton = invoc("Squelette",aspiration=POIDS_PLUME,strength=[PURCENTAGE,0.25],endurance=[PURCENTAGE,0.35],charisma=[PURCENTAGE,0.25],agility=[PURCENTAGE,0.25],precision=[PURCENTAGE,0.25],intelligence=[PURCENTAGE,0.25],magie=[PURCENTAGE,0.35],resistance=20,percing=10,critical=0,icon=['<:skeleton:1034363693724610580>','<:skeleton:1034363693724610580>'],weapon=skeletonWeap,description="Une invocation faible mais pouvant facilement submerger l'ennemi",team=NPC_UNDEAD)
hinoro = invoc("Hinoro",aspiration=ASPI_NEUTRAL,strength=[PURCENTAGE,0.25],endurance=[PURCENTAGE,0.55],charisma=[PURCENTAGE,0.5],agility=[PURCENTAGE,0.65],precision=[PURCENTAGE,0.75],intelligence=[PURCENTAGE,0.50],magie=[PURCENTAGE,0.75],resistance=50,percing=0,critical=25,icon=["<:phenixBlue:1066006625980264449>","<:phenixRed:1066006652349849670>"],weapon=hinoroWeapon,skills=[hinoroPassive,hinoroSkill1,hinoroSkill2,hinoroSkill3],description="Phénix lié à Chûri, Hinoro inflige des dégâts magiques tout en soignant les alliés autour de lui",element=ELEMENT_FIRE)

lenaDrone1Weap = weapon("Tir de balle","lenadrone1Weap",RANGE_LONG,AREA_CIRCLE_5,80,120,ignoreAutoVerif=True,emoji='<:lenaDrone1Weap:1116612753247981639>')
lenaDrone1Skill1 = skill("Tir dirigé","lenaDrone1Skill1",TYPE_DAMAGE,power=100,garCrit=True,accuracy=150,effects=[analyseCritWeak],effBeforePow=True,cooldown=3,description="Augmente les dégâts critiques reçus par la cible puis lui inflige une attaque forcément critique",emoji='<:lenaDrone1Skill:1116613296628445226>')
lenaDrone1Skill2 = skill("Salve de Mini-Missiles","lenaDrone1Skill2",TYPE_DAMAGE,power=50,area=AREA_RANDOMENNEMI_3,setAoEDamage=True,cooldown=3,emoji='<:miss2:1051436754101612585>',description="Inflige des dégâts à trois ennemis aléatoires")
lenaDrone1Smn = invoc("Drone Artilleur",[PURCENTAGE,0.7],[PURCENTAGE,0.3],[PURCENTAGE,0.3],[PURCENTAGE,0.5],[PURCENTAGE,1],[PURCENTAGE,0.5],[PURCENTAGE,0.3],20,10,15,OBSERVATEUR,["<:lenaDrone1B:1116262917868888185>","<:lenaDrone1R:1116262947178680320>"],lenaDrone1Weap,[lenaDrone1Skill1,lenaDrone1Skill2],description="Un drone automatique infligeant des dégâts ({0}) aux ennemis et pouvant augmenter les dégâts critiques qu'ils subissent".format(statsEmojis[lenaDrone1Weap.use]))

# Invocations

invocTabl = [lenaDrone1Smn,sonarPafSmn,hinoro,skeleton,seraf,carbObsi,carbSaphir,seeker,killerWailSum,darkness,autoBomb,lapino,titania,feeInv,carbuncleT,carbuncleE,batInvoc,cutyBat,carbunR,autTour,autFou,autQueen,pipis,lightButterfly,mrLifeSavor,
]

def findSummon(name) -> invoc:
    for a in invocTabl:
        if a.name == name:
            return a

    return None

MEMORIASTATCONVERT = 0.75
memoriaEff = effect("In Memoria","memoriaEff",translucide=True,immunity=True,turnInit=-1,unclearable=True)
memoriaWeap = weapon("In Memoria","noneWeap",RANGE_DIST,AREA_CIRCLE_5,0,0,ignoreAutoVerif=True,effects=memoriaEff)
memoria = invoc("Memoria",[PURCENTAGE,MEMORIASTATCONVERT],[PURCENTAGE,MEMORIASTATCONVERT],[PURCENTAGE,MEMORIASTATCONVERT],[PURCENTAGE,MEMORIASTATCONVERT],[PURCENTAGE,MEMORIASTATCONVERT],[PURCENTAGE,MEMORIASTATCONVERT],[PURCENTAGE,MEMORIASTATCONVERT],0,0,0,ASPI_NEUTRAL,["<:ghostB:1119951487032901722>","<:ghostR:1119951498395271218>"],memoriaWeap,[],team=NPC_UNDEAD,description="Une invocation qui se base sur une autre entité. Un mémoria copie toutes les compétences de cette entité ainsi que **{0}%** de ses statistiques".format(int(MEMORIASTATCONVERT*100)))
invocTabl.append(memoria)