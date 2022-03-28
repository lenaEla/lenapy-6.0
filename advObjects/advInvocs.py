from classes import *
from constantes import *
from advObjects.advSkills import *

batWeap = weapon("Griffe","aaa",RANGE_MELEE,AREA_CIRCLE_1,70,80,0,emoji='<:griffe:884889931359596664>',use=AGILITY)
carbunTWeap = weapon("Griffe","aaa",RANGE_MELEE,AREA_CIRCLE_1,70,80,0,emoji='<:griffe:884889931359596664>',use=ENDURANCE)
carbunE = weapon("Coup de vent","aab",RANGE_LONG,AREA_CIRCLE_5,40,70,0,emoji='<:vent:884889843681853460>',area=AREA_CIRCLE_1,use=MAGIE)
carbunSkill = skill("Eclat Emeraude","aac",TYPE_DAMAGE,0,80,area=AREA_CIRCLE_2,sussess=55,emoji='<:rafale:884889889445912577>',use=MAGIE,cooldown=4,description="Inflige des dégâts dans une large zone autour de la cible\n__Puissance :__ **{0}**")
carbunTSKill = skill("Eclat de Topaze","aad",TYPE_DAMAGE,0,100,AREA_MONO,area=AREA_CIRCLE_2,sussess=80,cooldown=4,emoji="<:eclattopaze:884889967397056512>",use=ENDURANCE,description="Inflige des dégâts dans une large zone autour du Carbuncle Topaze\n__Puissance :__ **{0}**")
feeWeap = weapon("Embrassement","aae",RANGE_DIST,AREA_CIRCLE_4,20,100,0,type=TYPE_HEAL,use=CHARISMA,emoji="<:feerie:885076995522834442>",target=ALLIES,area=AREA_CIRCLE_1)
feeEffect = effect("Murmure de l'aurore","aaf",CHARISMA,type=TYPE_INDIRECT_HEAL,power=10,emoji=uniqueEmoji('<:feerie:885076995522834442>'),trigger=TRIGGER_START_OF_TURN,turnInit=3,stackable=True)
feeSkill = skill("Murmure de l'aurore","aag",TYPE_INDIRECT_HEAL,0,0,AREA_MONO,cooldown=3,area=AREA_CIRCLE_3,emoji="<:feerie:885076995522834442>",effect=feeEffect,description="Donne un effet régénérant aux alliés autours de la Fée Soignante\n__Puissance :__ **{0}**\n__Durée__ : {1} tours".format(feeEffect.power,feeEffect.turnInit))
titWeap = weapon("Rune de Malice","titaniaWeapo,n",RANGE_MELEE,AREA_CIRCLE_1,26,50,repetition=3,emoji='<:magicalBonk:886669168408137749>',area=AREA_CONE_2,use=MAGIE) 
lapinoWeap = weapon("Murmure de guérison","aai",RANGE_DIST,AREA_CIRCLE_3,20,100,0,0,0,0,0,0,0,0,0,0,0,'<:defHeal:885899034563313684>',use=CHARISMA,type=TYPE_HEAL,target=ALLIES,message="{0} encourage doucement {1} :")
lapinoSkill = skill("Murmure de dévoument","aaj",TYPE_HEAL,0,65,emoji='<:defHeal:885899034563313684>',cooldown=4,description="Soigne l'allié ciblé\n__Puissance :__ **{0}**")
lapinoSkill2 = skill("Murmure d'abnégation","lapinoSkill2",TYPE_HEAL,power=100,use=CHARISMA,cooldown=3,maxHpCost=95,description="Soigne l'allié ciblé au prix de la quasi totalité des PV max du Lapino\n__Puissance :__ **{0}**")
batSkill = skill("Cru-aile","aak",TYPE_DAMAGE,0,100,AREA_CIRCLE_2,emoji='<:defDamage:885899060488339456>',use=AGILITY)
autoWeap = weapon("NoneWeap","NoneWeap",RANGE_MELEE,AREA_CIRCLE_1,0,0,0,emoji="<:noneWeap:917311409585537075>")
autoEff = effect("Explosé","aam",trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,power=9999,emoji=emojiMalus,silent=True)
autoSkill = skill("Explosion","aan",TYPE_DAMAGE,0,125,AREA_MONO,emoji='<:defDamage:885899060488339456>',area=AREA_CIRCLE_1,effectOnSelf=autoEff,sussess=200,setAoEDamge=True,description="Inflige des dégâts en zone autour de la Bombe Robot, puis s'auto détruit à la fin du tour\n__Puissance :__ **{0}**")
cutyBatSkill1Eff = effect("Motivé Bis","batMotivEff",stat=CHARISMA,strength=7,magie=7,charisma=7,intelligence=7)
cutyBatSkill1 = skill("Motivation de la Chauve-Souris","batMotiv",TYPE_BOOST,0,0,AREA_MONO,area=AREA_DONUT_2,use=CHARISMA,cooldown=4,effect=cutyBatSkill1Eff,description="Augmente la Force, la Magie, le Charisme et l'Intelligence des alliés proches de la Chauve-Souris II")
cutyBatSkill2Eff = effect("Renforcement Bis","batRenforceEff",stat=INTELLIGENCE,endurance=7,resistance=3,emoji=uniqueEmoji('<:egide:887743268337619005>'))
cutyBatSkill2 = skill("Renforcement de la Chauve-Souris","batRenforce",TYPE_BOOST,0,0,range=AREA_DONUT_5,cooldown=3,emoji='<:egide:887743268337619005>',effect=cutyBatSkill2Eff,description="Augmente l'Endurance et la Résistance de l'allié ciblé")
cutyBatSkill3Eff = effect("Echolocalisé","batEchoEff",CHARISMA,agility=-7,type=TYPE_MALUS)
cutyBatSkill3 = skill("Echolocalisation","batEcho",TYPE_MALUS,0,0,AREA_MONO,area=AREA_DONUT_5,effect=cutyBatSkill3Eff,cooldown=3,description="Diminue l'Agilité des ennemis affectés")
cutyBatWeap = weapon("Onde sonore","batWeap",RANGE_DIST,AREA_CIRCLE_5,32,100,effectOnUse=incur[1],use=CHARISMA)
carbunRWeap = weapon("Griffe enflammé","rubyWeap",RANGE_MELEE,AREA_CIRCLE_1,56,100,use=MAGIE,emoji=batWeap.emoji)
carbunRSkill1 = skill("Pyrotechnie du Carbuncle","rubySkill",TYPE_DAMAGE,0,75,AREA_CIRCLE_2,cooldown=3,use=MAGIE,description="Inflige des dégâts à l'ennemi ciblé\n__Puissance :__ **{0}**")
curbunRSkill2Eff = effect("Flamme éternelle","fire",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=35,lvl=3,turnInit=3)
carbunRSkill2 = skill("Flammes éternelles","rubySkill2",TYPE_DAMAGE,0,70,AREA_CIRCLE_3,effect=curbunRSkill2Eff,cooldown=3,use=MAGIE,description="Inflige des dégâts à l'ennemi ciblé tout en lui infligeant un effet de dégâts indirects\n__Puissance :__ **{0}**\n__Puissance (indirect) :__ **35**\n__Durée (indirect) :__ 3 tours")
serafWeaponEff = effect("Bénidiction séraphique","serafWeapShield",INTELLIGENCE,overhealth=25,lightShield=True,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,emoji=sameSpeciesEmoji('<:dictameB:911078870936084551>','<:dictameR:911078775217848342>'))
serafWeapon = weapon("Bénéiction séraphique","serafWeap",RANGE_DIST,AREA_CIRCLE_5,power=10,sussess=100,effectOnUse=serafWeaponEff,type=TYPE_HEAL,use=INTELLIGENCE,emoji='<:dictameB:911078870936084551>',target=ALLIES)
dictameEff = effect("Dictame","dictameEff",INTELLIGENCE,overhealth=35,type=TYPE_ARMOR,emoji=serafWeaponEff.emoji,trigger=TRIGGER_DAMAGE)
serafSkill = skill("Dictame","dictame",TYPE_ARMOR,0,0,range=AREA_MONO,area=AREA_CIRCLE_2,effect=dictameEff,cooldown=2,use=INTELLIGENCE,emoji=serafWeapon.emoji,description="Donne une armure aux allié proches de la Fée Protectrice\n__Puissance de l'armure :__ **{0}**".format(dictameEff.overhealth))
GESLweap = weapon("noneWeap","aaa",1,AREA_CIRCLE_1,0,0,0)
GESLskill = skill("Piétinement Physique","TheGiantEnnemySpiderLeft",TYPE_DAMAGE,0,45)
GESRskill = skill("Piétinement Magique","TheGiantEnnemySpiderRigth",TYPE_DAMAGE,0,GESLskill.power,use=MAGIE)
carbOb = weapon("Griffe d'obsidienne","carObWeap",RANGE_MELEE,AREA_CIRCLE_1,33,70,repetition=3,emoji=batWeap.emoji)
carbObSkill = skill("Eclat d'Obsidenne","carbObsiSkill",TYPE_DAMAGE,0,75,AREA_CIRCLE_2,cooldown=3,emoji='<:carbSkill2:919859568685752350>',description="Inflige des dégâts autour du Carbuncle Obsidienne\n__Puissance :__ **{0}**")
carbSa = weapon("Tir de glacée","carbSaWeap",RANGE_DIST,AREA_CIRCLE_6,56,80,0)
carbSaSkill = skill("Eclat de Saphir","carbSaSkill",TYPE_DAMAGE,0,80,cooldown=2,emoji='<:carbSkill2:919859581381926933>',description="Inflige des dégâts à l'ennemi ciblé\n__Puissance :__ **{0}**")
seekerSkill = skill("Traque",'seekerSkill',TYPE_DAMAGE,0,100,AREA_RANDOMENNEMI_1,area=AREA_CIRCLE_1,tpCac=True,effectOnSelf=autoEff,areaOnSelf=True)
killerWailWeap = copy.deepcopy(autoWeap)
killerWailWeap.use, killerWailWeap.range = MAGIE, RANGE_LONG
killerWailSkill = skill("Rayon sonique","killerWail5.1SumSkill",TYPE_DAMAGE,0,45,AREA_MONO,area=AREA_LINE_6,effectOnSelf=autoEff,use=MAGIE,setAoEDamge=True,emoji='<:kwShot:933510363398418432>')
titSkill1 = skill("Rune de Feu","titSkill1",TYPE_DAMAGE,0,75,area=AREA_CIRCLE_1,setAoEDamge=True,cooldown=3,use=MAGIE,description="Inflige des dégâts de zone dans une petite zone autour de la cible\n__Puissance :__ **{0}**\nNon affecté par la réduction de dégâts de zone")
titSkill2 = skill("Rune de Gel","titSkill2",TYPE_DAMAGE,0,50,range=AREA_DIST_5,area=AREA_CIRCLE_2,cooldown=3,use=MAGIE,description="Inflige des dégâts de zone dans une large zone autour de la cible\n__Puissance :__ **{0}**")
titSkill3_1 = skill("Rune d'Illusion","titSkill3",TYPE_DAMAGE,power=100,range=AREA_MONO,area=AREA_CIRCLE_2,setAoEDamge=True,cooldown=3,use=MAGIE)
titSkill3_2 = skill("Rune d'Illusion","titSkill3",TYPE_DAMAGE,power=50,range=AREA_MONO,area=AREA_DIST_7,setAoEDamge=True,cooldown=3,use=MAGIE)
titSkill3 = skill("Rune d'Illusion","titSkill3",TYPE_DAMAGE,become=[titSkill3_1,titSkill3_2],use=MAGE,description="Effectue des dégâts magiques autour de Titania ou dans un donut large centrée autour d'elle\n__Puissances :__ **{0}**, **{1}**\nNon affecté par la réduction de dégâts de zone".format(titSkill3_1.power,titSkill3_2.power),area=AREA_CIRCLE_1)

batInvoc = invoc("Chauve-Souris",aspiration=POIDS_PLUME,strength=[PURCENTAGE,0.5],endurance=[PURCENTAGE,0.3],charisma=[PURCENTAGE,0.5],agility=[PURCENTAGE,0.7],precision=[PURCENTAGE,0.7],intelligence=[PURCENTAGE,0.5],magie=[PURCENTAGE,0.5],resistance=20,percing=0,critical=30,icon=["<:bat1:884519906819862568>","<:bat2:884519927208357968>"],gender=GENDER_FEMALE,weapon=batWeap,description="Une invocation de mêlée peu resistante, mais sans temps de rechargement",skill=[batSkill],element=ELEMENT_AIR)
carbuncleE = invoc("Carbuncle Emeraude",[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0.7],20,10,[PURCENTAGE,1],MAGE,["<:carbEmR:919858018739437568>",'<:carbEmB:919857996274749451>'],carbunE,[carbunSkill],description="Une invocation utilisant des compétences de zone pour vaincre des groupes d'ennemis de loin",element=ELEMENT_AIR)
carbuncleT = invoc("Carbuncle Topaze",[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.1],0,10,PROTECTEUR,["<:ct1:884889748274028666>","<:ct2:884889807111749662>"],carbunTWeap,[carbunTSKill],description="Une invocation résistante qui n'a pas froid au yeux et viendra sauter dans la mêlée",element=ELEMENT_EARTH)
feeInv = invoc("Fée soignante",[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.7],10,0,0,ALTRUISTE,["<:fee1:885076945333805086>","<:fee2:885076961695760386>"],feeWeap,[feeSkill],gender=GENDER_FEMALE,description="Une fée qui soigne ses alliés grace à sa magie curative",element=ELEMENT_LIGHT)
titania = invoc("Titania",[PURCENTAGE,0.3],[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.5],[PURCENTAGE,0.7],25,10,20,ENCHANTEUR,["<:tita1:886663550796431390>","<:tita2:886663565220651028>"],titWeap,[titSkill1,titSkill2,titSkill3],GENDER_FEMALE,element=ELEMENT_UNIVERSALIS_PREMO,description="Une invocation magique qui inflige de lourd dégâts de zone")
lapino = invoc("Lapino",[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.3],[PURCENTAGE,0.5],[PURCENTAGE,0.5],[PURCENTAGE,0.5],10,0,0,ALTRUISTE,['<:lapino1:885899366966112266>','<:lapino2:885899382539571221>'],lapinoWeap,[lapinoSkill,eting,lapinoSkill2],description="Fidèle Lapino d'Hélène, il la suit partout là où elle aura besoin de lui",element=ELEMENT_LIGHT)
autoBomb = invoc("Bombe Robot",[PURCENTAGE,0.8],50,0,0,0,0,0,20,0,0,POIDS_PLUME,["<:auto1:887747795497394267>","<:auto2:887747819866312735>"],autoWeap,[autoSkill])
darkness = invoc("Conviction des Ténèbres",0,-25,0,0,0,0,0,0,0,0,ASPI_NEUTRAL,['<:infiniteDarkness:898497770531455008>','<:infiniteDarkness:898497770531455008>'],autoWeap,gender=GENDER_FEMALE,element=ELEMENT_DARKNESS)
cutyBat = invoc("Chauve-Souris II",strength=[PURCENTAGE,0.5],endurance=[PURCENTAGE,0.3],charisma=[PURCENTAGE,0.7],agility=[PURCENTAGE,0.7],precision=[PURCENTAGE,0.5],intelligence=[PURCENTAGE,0.7],magie=[PURCENTAGE,0.5],resistance=[PURCENTAGE,1],percing=0,critical=0,aspiration=IDOLE,icon=['<:bat2B:904368975952085012>','<:bat2R:904368991710101515>'],weapon=cutyBatWeap,skill=[cutyBatSkill1,cutyBatSkill2,cutyBatSkill3],gender=GENDER_FEMALE,description="Une chauve-souris spécialisée dans le soutiens")
carbunR = invoc("Carbuncle Rubis",strength=[PURCENTAGE,0.5],endurance=[PURCENTAGE,0.7],charisma=[PURCENTAGE,0.5],agility=[PURCENTAGE,0.7],precision=[PURCENTAGE,0.7],intelligence=[PURCENTAGE,0.5],magie=[PURCENTAGE,0.7],resistance=[PURCENTAGE,1],percing=[PURCENTAGE,1],critical=25,aspiration=ENCHANTEUR,icon=['<:carbunRB:904368034200834089>','<:carbunRR:904368049547776010>'],weapon=carbunRWeap,skill=[carbunRSkill1,carbunRSkill2],description="Un carbuncle de mêlée",element=ELEMENT_FIRE)
seraf = invoc("Fée protectrice",strength=[PURCENTAGE,0.5],endurance=[PURCENTAGE,0.5],charisma=[PURCENTAGE,0.5],agility=[PURCENTAGE,0.3],precision=[PURCENTAGE,0.5],intelligence=[PURCENTAGE,0.7],magie=[PURCENTAGE,0.5],resistance=[PURCENTAGE,1],percing=0,critical=0,aspiration=PREVOYANT,icon=['<:seraphB:911078241404608522>','<:seraphR:911078257078706256>'],weapon=serafWeapon,skill=[serafSkill],description="Une fée spécialisée dans les armures\nPeut donner des armures légères avec son arme ou des armures sur les alliés autour d'elle avec Dictame",element=ELEMENT_LIGHT,gender=GENDER_FEMALE)
TGESL1 = invoc("Patte de The Giant Enemy Spider",[PURCENTAGE,0.5],[PURCENTAGE,0.3],0,[PURCENTAGE,0.7],[PURCENTAGE,0.7],0,0,[PURCENTAGE,0.3],0,0,ASPI_NEUTRAL,['<:TGESlegs2:917303003936063538>','<:TGESlegs2:917303003936063538>'],GESLweap,[GESLskill],gender=GENDER_FEMALE)
TGESL2 = copy.deepcopy(TGESL1)
TGESL2.strength, TGESL2.magie, TGESL2.icon, TGESL2.skills[0] = 0,TGESL1.strength,['<:TGESlegs1:917302968104144906>','<:TGESlegs1:917302968104144906>'],GESRskill
seeker = invoc("Traqueur",[PURCENTAGE,0.7],[PURCENTAGE,0.1],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.7],[PURCENTAGE,0.3],[PURCENTAGE,0.3],0,[PURCENTAGE,1],[PURCENTAGE,1],BERSERK,['<:seekerB:933508361863954432>','<:seekerR:933508377584234606>'],autoBomb.weapon,[seekerSkill],description="Une machine qui se téléporte sur une cible aléatoire puis explose (Puissance : {0}, Zone : Cercle de 1)".format(seekerSkill.power))
killerWailSum = invoc("Haut-Perceur 5.1",[PURCENTAGE,0.3],[PURCENTAGE,0.1],[PURCENTAGE,0.3],[PURCENTAGE,0.5],[PURCENTAGE,0.7],[PURCENTAGE,0.3],[PURCENTAGE,0.7],0,[PURCENTAGE,1],[PURCENTAGE,1],OBSERVATEUR,['<:kwB:933510332733882378>','<:kwR:933510345488736346>'],killerWailWeap,[killerWailSkill],description="Une machine qui tire un laser sonique sur toute sa ligne, infligeant des dégâts aux ennemis s'y trouveant, puis s'auto-détruit (Puissance : {0}, non affecté par la réduction de dégâts de zone)".format(killerWailSkill.power),canMove=False)

carbObsi = invoc("Carbuncle Obsidienne",strength=[PURCENTAGE,0.7],endurance=[PURCENTAGE,0.5],charisma=[PURCENTAGE,0.5],agility=[PURCENTAGE,0.7],precision=[PURCENTAGE,0.5],intelligence=[PURCENTAGE,0.5],magie=[PURCENTAGE,0.3],resistance=[PURCENTAGE,1],percing=[PURCENTAGE,1],critical=[PURCENTAGE,0.5],aspiration=POIDS_PLUME,icon=['<:carbObsiB:919857954029707284>','<:carObsiR:919857975051558954>'],weapon=carbOb,skill=[carbObSkill],element=ELEMENT_DARKNESS)
carbSaphir = invoc("Carbuncle Saphir",strength=[PURCENTAGE,0.7],endurance=[PURCENTAGE,0.5],charisma=[PURCENTAGE,0.5],agility=[PURCENTAGE,0.5],precision=[PURCENTAGE,0.7],intelligence=[PURCENTAGE,0.5],magie=[PURCENTAGE,0.3],resistance=[PURCENTAGE,0.5],percing=[PURCENTAGE,1],critical=[PURCENTAGE,1],aspiration=OBSERVATEUR,icon=["<:ce1:884889724114841610>","<:ce2:884889693374775357>"],weapon=carbSa,skill=[carbSaSkill],element=ELEMENT_WATER)

# Invocations
invocTabl = [seraf,carbObsi,carbSaphir,seeker,killerWailSum,darkness,autoBomb,lapino,titania,feeInv,carbuncleT,carbuncleE,batInvoc,cutyBat,carbunR
]

def findSummon(name) -> invoc:
    for a in invocTabl:
        if a.name == name:
            return a

    return None
