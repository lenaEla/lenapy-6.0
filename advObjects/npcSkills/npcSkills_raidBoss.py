from advObjects.npcSkills.npcSkills_ennemi import *

ailillPassiveEff = effect("Acharnement","aillilPassiv",power=35,emoji=deepWound.emoji,turnInit=-1,unclearable=True,callOnTrigger=deepWound)
ailillPassive = skill("Acharnement","ailillPassiv",TYPE_PASSIVE,emoji=deepWound.emoji[0][0],effects=ailillPassiveEff,description="**{0}%** des dégâts directs infligés par Aillil sont en plus infligés en tant que {1} {2}".format(ailillPassiveEff.power, ailillPassiveEff.callOnTrigger.emoji[0][0], ailillPassiveEff.callOnTrigger.name))

ailillEffBleeding = copy.deepcopy(bleeding)
ailillEffBleeding.power, ailillEffBleeding.lifeSteal = 50, 50
ailillWeapEff2 = copy.deepcopy(vampirismeEff)
ailillWeapEff2.power, ailillWeapEff2.turnInit = 50, -1
ailillWeap = weapon("Tronçonneuse Sanglante","aillilWeap",RANGE_MELEE,AREA_CIRCLE_1,power=300,accuracy=200,strength=50,precision=25,percing=10,resistance=10,agility=20,damageOnArmor=1.5,emoji='<:chainsaw:1189299410794979479>',effects=ailillWeapEff2,effectOnUse=ailillEffBleeding,priority=WEAPON_PRIORITY_LOWEST)
ailillSkill4 = skill("Frappe Sonique",'ailillSkill4',TYPE_DAMAGE,power=200,range=AREA_RANDOMENNEMI_1,area=AREA_CIRCLE_2,lifeSteal=20,cooldown=3,tpCac=True,areaOnSelf=True,description="Ailill apparait à côté d'un ennemi et inflige des dégâts à tous les ennemis autour d'elle",emoji='<:ailillSkill2:1044634656701698088>')
ailillSkill5 = skill("Lames Dansantes","ailillSkill5",TYPE_DAMAGE,power=200,range=AREA_RANDOMENNEMI_3,area=AREA_LINE_5,cooldown=5,lifeSteal=20,description="Ailill apparait à côté d'un ennemi et inflige des dégâts sur toute une ligne dans la direction de ce dernier",emoji='<:ailillSkill3:1044636776616177734>')
ailillSkill6Eff = effect("Frappe Déphasée","ailillDephaStrikes", stat=STRENGTH,power=220,area=AREA_CIRCLE_1,lifeSteal=50,trigger=TRIGGER_ON_REMOVE,type=TYPE_DAMAGE,effPrio=1,emoji='<:ailillDephaStrikeRep:1044639469921378334>')
ailillSkill6 = skill("Frappe Déphasée","alillSkill6",TYPE_INDIRECT_DAMAGE,effects=ailillSkill6Eff,range=AREA_RANDOMENNEMI_3,area=AREA_RANDOMENNEMI_5,cooldown=5,description="Ailill marque 5 ennemis aléatoirement et viendra infliger des dé^gats autour d'eux à son prochain tour",emoji='<:ailillDephaStrike:1044639442335449113>')
ailillSkill2_4 = skill("Attaques Successives","ailillSkill2",TYPE_DAMAGE,power=400,area=AREA_CIRCLE_1,tpCac=True,range=AREA_CIRCLE_3,cooldown=6,description="Ailill effectue de multiples attaques aux airs d'effets variés sur l'ennemi ciblé",say="MAIS CREVE ENFIN !")
ailillSkill2_4_cast = effect("Cast - Attaques Successives","ailillSkill2Cast4",silent=True,replique=ailillSkill2_4)
ailillSkill2_3 = copy.deepcopy(ailillSkill2_4)
ailillSkill2_3.power, ailillSkill2_3.effectOnSelf, ailillSkill2_3.say, ailillSkill2_3.area, ailillSkill2_3.replay = 300, ailillSkill2_4_cast, "", AREA_INLINE_2, True
ailillSkill2_3_cast = effect("Cast - Attaques Successives","ailillSkill2Cast3",silent=True,replique=ailillSkill2_3)
ailillSkill2_2 = copy.deepcopy(ailillSkill2_3)
ailillSkill2_2.power, ailillSkill2_2.effectOnSelf, ailillSkill2_2.area = 200, ailillSkill2_3_cast, AREA_LINE_3
ailillSkill2_2_cast = effect("Cast - Attaques Successives","ailillSkill2Cast2",silent=True,replique=ailillSkill2_2,turnInit=2)
ailillSkill2 = copy.deepcopy(ailillSkill2_2)
ailillSkill2.power, ailillSkill2.effectOnSelf, ailillSkill2.area, ailillSkill2.tpCac, ailillSkill2.replay = 0, ailillSkill2_2_cast, AREA_MONO, False, False
ailillSkill3Eff = effect("Double Tranchant","ailillSkill3Eff", stat=STRENGTH,power=200,trigger=TRIGGER_ON_REMOVE,lifeSteal=50,type=TYPE_DAMAGE,effPrio=1,emoji='<:ailillTwoStrikeRep:1044491016679460885>')
ailillSkill3 = skill("Frappe en deux-temps","ailillSkill3",TYPE_DAMAGE,power=ailillSkill3Eff.power,effects=ailillSkill3Eff,cooldown=3,tpCac=True,range=AREA_CIRCLE_2,description='Ailill inflige des dégâts directs à une cible unique, puis inflige un second coup lors du début de son prochain tour',emoji='<:ailillTwoStrike:1044490984572076142>')
ailillSkill7Eff, ailillSkill7Eff2 = copy.deepcopy(vulne), copy.deepcopy(incurable)
ailillSkill7Eff.power, ailillSkill7Eff.turnInit, ailillSkill7Eff2.power, ailillSkill7Eff2.turnInit = 25, 3, 50, 3
ailillSkill7_1 = skill("Disparité","ailillSkill7",TYPE_DAMAGE,power=650,cooldown=6,emoji='<:ailillSkill1:1044487636561178646>',lifeSteal=35,accuracy=250,effects=[ailillSkill7Eff,ailillSkill7Eff2],description="Ailill inflige de lourd dégâts à une cible unique, vol une partie des dégâts infligés et augmente les dégâts subis ainsi que les soins reçus de la cible de respectivement **{0}%** et **{1}%** pendant 3 tours".format(ailillSkill7Eff.power,ailillSkill7Eff2.power))
ailillSkill7_c = effect("Cast - {replicaName}","ailillSkill7_c",turnInit=2,silent=True,replique=ailillSkill7_1)
ailillSkill7 = copy.deepcopy(ailillSkill7_1)
ailillSkill7.power, ailillSkill7.effectOnSelf, ailillSkill7.effects = 0, ailillSkill7_c, [None]

kitsuneWeapEff = effect("Kitsune originelle",'kitsunePassifEff', stat=CHARISMA,magie=10,charisma=10,emoji='<:kitsuWeapEff:935553855272407080>',turnInit=-1,description="En subissant des dégâts, esquivant une attaque ou infligeant des dégâts, Kitsune donne l'effet __Charmé (Ennemi)__ à l'entité attanquante ou attaquée",callOnTrigger=charming)
kitsuneWeap = weapon("Magie multi-élémentaire",'kitsuneWeap',RANGE_DIST,AREA_CIRCLE_4,35,99,ignoreAutoVerif=True,repetition=3,charisma=35,endurance=20,effectOnUse=charming,use=MAGIE,effects=kitsuneWeapEff,emoji='<:kitsuWeap:935553775500947486>',priority=WEAPON_PRIORITY_LOWEST)
kitsuneSkill1_1 = skill("Flammes originelles",'kitsuneSkill1',TYPE_DAMAGE,power=120,area=AREA_CONE_3,cooldown=3,use=MAGIE,emoji='<:fireKitsune:917670925904785408>',say="Et si je chauffais un peu l'ambiance ?")
kitsuneSkill1_2 = skill("Glace Originelle","kitsuneSkill1",TYPE_DAMAGE,power=160,area=AREA_LINE_3,cooldown=3,use=MAGIE,emoji='<:waterKitsune:917670866626707516>')
kitsuneSkill1_3 = skill("Vent Originel",'kitsuneSkill1',TYPE_DAMAGE,power=160,range=AREA_MONO,area=AREA_CIRCLE_2,use=MAGIE,cooldown=2,emoji='<:airKitsune:917670912646602823>',say="Oh vous voulez me voir de près ? J'ai de quoi vous satisfaire")
kitsuneSkill1_4 = skill("Roche Originel",'kitsuneSkill1',TYPE_DAMAGE,power=145,range=AREA_CIRCLE_2,area=AREA_CIRCLE_1,cooldown=2,use=MAGIE,emoji='<:earthKitsune:917670882586017792>')
kitsuneSkill1 = skill("Magie Originelle",'kitsuneSkill1',TYPE_DAMAGE,become=[kitsuneSkill1_1,kitsuneSkill1_2,kitsuneSkill1_3,kitsuneSkill1_4],use=MAGIE)

kitsunedDot = effect("Saignement","kitsuneBleed", stat=MAGIE,power=50,turnInit=5,emoji='<:bleed:1083761078770618460>',trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE)
kitsuneSkill2_1 = skill("Vent d'amour",'kitsuneSkill2',TYPE_MALUS,range=AREA_MONO,area=AREA_CIRCLE_2,emoji='<:verAero2:1042350921281191977>',effects=charming,effPowerPurcent=300,effectOnSelf=charming2,cooldown=3,say="Vous voulez vraiment rester aussi près ? Téméraires dites donc ^^",effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_CIRCLE_2,kitsunedDot])
kitsuneSkill2_2 = skill("Terre d'amour",'kitsuneSkill2',TYPE_MALUS,range=AREA_CIRCLE_2,area=AREA_CIRCLE_1,effects=charming,emoji='<:stone2:1053730589049618462>',effPowerPurcent=500,effectOnSelf=charming2,cooldown=3,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_CIRCLE_2,kitsunedDot])
kitsuneSkill2_3 = skill("Feu d'amour",'kitsuneSkill2',TYPE_MALUS,range=AREA_MONO,area=AREA_DIST_5,effects=charming,effPowerPurcent=100,emoji='<:fireplace:931666078092902471>',effectOnSelf=charming2,cooldown=3,say="Vous voulez pas avoir une meilleure vue ? J'ai de quoi tous vous contenter vous savez ?",effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_DIST_5,kitsunedDot])
kitsuneSkill2_4 = skill("Eau d'amour",'kitsuneSkill2',TYPE_MALUS,range=AREA_DIST_5,area=AREA_CONE_3,effects=charming,effPowerPurcent=100,emoji='<:water2:1065647727708483654>',effectOnSelf=charming2,cooldown=3,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_DIST_5,kitsunedDot])
kitsuneSkill2 = skill("Amour élémentaire",'kitsuneSkill2',TYPE_DAMAGE,become=[kitsuneSkill2_1,kitsuneSkill2_2,kitsuneSkill2_3,kitsuneSkill2_4],emoji='<:serenade:1047386802517971014>',use=CHARISMA,description="Kitsune charme les adversaires dans diverses zones d'effet et leur inflige des dégâts continus")

kitsuneSkill3_1 = skill("Vitesse aérienne",'kitsuneSkill3',TYPE_DAMAGE,power=100,range=AREA_INLINE_3,use=MAGIE,replay=True,cooldown=2,emoji='<:liaSkill:922291249002709062>',knockback=3,jumpBack=2)
kitsuneSkill3_2 = skill("Sable mouvants",'kitsuneSkill3',TYPE_DAMAGE,power=150,range=AREA_MONO,area=AREA_CIRCLE_2,use=MAGIE,cooldown=4,effectOnSelf=liuSkillEff,emoji=liuSkill.emoji)
kitsuneSkill3_3 = skill("Flamme infernales",'kitsuneSkill3',TYPE_INDIRECT_DAMAGE,range=AREA_MONO,area=AREA_ALL_ENEMIES,use=MAGIE,cooldown=3,emoji=lieSkill.emoji,effects=lizSkillSusEff)
kitsuneSKill3_4Eff = effect("Régénération",'kitsuneSkill3_4Eff', stat=CHARISMA,power=85,turnInit=3,lvl=3,emoji='<:lioWeap:908859876812415036>',type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN)
kitsuneSkill3_4 = skill("Pluie infernale",'kitsuneSkill3',TYPE_DAMAGE,power=60,range=AREA_MONO,area=AREA_ALL_ENEMIES,use=MAGIE,cooldown=5,emoji=lioRez.emoji,setAoEDamage=True,effectOnSelf=kitsuneSKill3_4Eff)
kitsuneSkill3 = skill("Magie multi-élémentaire II",'kitsuneSkill3',TYPE_DAMAGE,become=[kitsuneSkill3_1,kitsuneSkill3_2,kitsuneSkill3_3,kitsuneSkill3_4],use=MAGIE)

kitsuneSkill4_1_eff = effect("Feu des volcans","With all the strength of a raging fire", stat=MAGIE,power=40,turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,emoji='<:enemyFire:1042312985407930428>',type=TYPE_INDIRECT_DAMAGE)
kitsuneSkill4_1_c = effect("Être plus ardent que le feu des volcans","volcanosReady",turnInit=3,silent=True,emoji='<:fire3:1042349767411376148>')
kitsuneSkill4_1 = skill("Feu des volcans","be a man",TYPE_DAMAGE,power=70,cooldown=5,use=MAGIE,setAoEDamage=True,range=AREA_MONO,area=AREA_ALL_ENEMIES,description="Kitsune inflige des dégâts à tous les ennemis et leur inflige un effet de dégâts sur la durée",effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_ALL_ENEMIES,kitsuneSkill4_1_eff],emoji="<:fire3:1042349767411376148>",needEffect=[kitsuneSkill4_1_c])
kitsuneSkill4_2_c = effect("Être plus puissant que les ouragans","tyfood",turnInit=3,emoji='<:verAero3:1042350960321769503>',silent=True)
kitsuneSkill4_2 = skill("Ouragans","be a man",TYPE_DAMAGE,power=160,cooldown=5,use=MAGIE,range=AREA_MONO,area=AREA_CIRCLE_4,description="Kitsune attire les ennemis autour d'elle et leur inflige des dégâts",pull=5,emoji="<:verAero3:1042350960321769503>",needEffect=[kitsuneSkill4_2_c],effectOnSelf=kitsuneSkill4_1_c)
kitsuneSkill4_3 = skill("Cours du Tourrant","be a man",TYPE_DAMAGE,power=150,cooldown=5,use=MAGIE,range=AREA_MONO,area=AREA_CIRCLE_3,description="Kitsune inflige des dégâts aux ennemis autour d'elle et les repousses",knockback=2,emoji="<:water3:1065647689129271397>",effectOnSelf=kitsuneSkill4_2_c)
kitsuneSkill4 = skill("Lune de l'Orient","be a man",TYPE_DAMAGE,become=[kitsuneSkill4_3,kitsuneSkill4_2,kitsuneSkill4_1],use=MAGIE,description="Kitsune inflige des dégâts aux ennemis autour d'elle et leur inflige des effets secondaires à l'aide de 3 compétences",emoji='<:enemyWater:1042313114487636038>')

naciaWeap = weapon("Lame Pangéenne","noneWeap",RANGE_DIST,AREA_CIRCLE_1,200,100,ignoreAutoVerif=True)
naciaEarthEff = effect("Puissance Tellurique","naciaEarthEff",turnInit=10,emoji=liuWeap.effects.emoji,description="Nacialisa a galvanisé les alentours avec une grande puissance élémentaire")
naciaEarthSkill1 = skill("Séisme de la génitrice","naciaSkill1",TYPE_DAMAGE,emoji="<:stone4:1053730609685602344>",power=175,range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=4,effectOnSelf=naciaEarthEff,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],damageOnArmor=0.8)
naciaEarthSkill2 = skill("Lames Rocheuses","naciaSkill1",TYPE_DAMAGE,emoji='<:enemyStone:1042313085400133632>',power=180,range=AREA_MONO,area=AREA_INLINE_5,cooldown=4,effectOnSelf=naciaEarthEff,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],damageOnArmor=0.8)
naciaEarthSkill3Eff = effect("Enlisé","naciaQuickSandEff", stat=ENDURANCE,emoji='<:stone1:1053730561648246804>',agility=-10,dodge=-15,turnInit=4,description="Réduit l'agilité pendant 4 tours",stackable=True,type=TYPE_MALUS)
naciaEarthSkill3 = skill("Sables Mouvants","naciaSkill1",TYPE_DAMAGE,emoji='<:stone2:1053730589049618462>',power=85,range=AREA_MONO,setAoEDamage=True,area=AREA_CIRCLE_3,cooldown=4,effectOnSelf=naciaEarthEff,effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_3,naciaEarthSkill3Eff],condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],damageOnArmor=0.8)
naciaEarthSkill = skill("Conviction de la planète","naciaSkill1",TYPE_DAMAGE,emoji=liuWeap.effects.emoji[0][0],become=[naciaEarthSkill1,naciaEarthSkill2,naciaEarthSkill3],cooldown=4,description="Nacialisla utilise des compétences terrestres pour infliger des dégâts autour d'elle",condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH])
naciaFireEff = effect("Puissance Volcanique","naciaFireEff",turnInit=10,emoji=lieWeap.effects.emoji,description="Nacialisa a galvanisé les alentours avec une grande puissance élémentaire")
naciaFireSkill1Eff = effect("Brûlure volcanique","naciaDot", stat=MAGIE,power=30,turnInit=3,trigger=TRIGGER_START_OF_TURN,emoji='<:enemyFire:1042312985407930428>',type=TYPE_INDIRECT_DAMAGE,lvl=3,description="Des braises infligent des dégâts périodiquements",stackable=True)
naciaFireSkill1 = skill("Eruption Explosive","naciaSkill2",TYPE_INDIRECT_DAMAGE,range=AREA_MONO,area=AREA_CIRCLE_5,effects=naciaFireSkill1Eff,emoji=fireCircle.emoji,effPowerPurcent=100,cooldown=4,effectOnSelf=naciaFireEff,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE])
naciaFireSkill2 = skill("Eruption Effusive","naciaSkill2",TYPE_INDIRECT_DAMAGE,range=AREA_CIRCLE_3,area=AREA_CIRCLE_3,effects=naciaFireSkill1Eff,emoji='<:majorFire2:1042349795353825320>',effPowerPurcent=125,cooldown=4,effectOnSelf=naciaFireEff,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE])
naciaFireSkill3 = skill("Frappe Eruptive","naciaSkill2",TYPE_DAMAGE,power=350,effects=naciaFireSkill1Eff,effPowerPurcent=300,cooldown=4,effectOnSelf=naciaFireEff,use=MAGIE,emoji='<:fire3:1042349767411376148>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE])
naciaFireSkill = skill("Ardeur de la planète","naciaSkill2",TYPE_INDIRECT_DAMAGE,emoji=lieWeap.effects.emoji[0][0],become=[naciaFireSkill1,naciaFireSkill2,naciaFireSkill3],cooldown=4,description="Nacialisla utilise des compétences emflammées magiques pour infliger des dégâts sur la durée",condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE])
naciaAirEff = effect("Puissance Aérienne","naciaAirEff",turnInit=10,emoji=liaWeap.effects.emoji,description="Nacialisa a galvanisé les alentours avec une grande puissance élémentaire")
naciaAirSkill1 = skill("Ouragant de la génitrice","naciaSkill3",TYPE_DAMAGE,power=120,knockback=3,range=AREA_MONO,area=AREA_CIRCLE_2,emoji=airCircle.emoji,effectOnSelf=naciaAirEff,cooldown=4,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],damageOnArmor=0.8)
naciaAirSkill2 = skill("Oeuil de la Tempette","naciaSkill3",TYPE_DAMAGE,power=80,setAoEDamage=True,knockback=1,emoji='<:verAero3:1042350960321769503>',range=AREA_MONO,area=AREA_DIST_5,effectOnSelf=naciaAirEff,cooldown=4,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],damageOnArmor=0.7)
naciaAirSkill3_3 = skill("Vitesse Aérienne","naciaSkill3",TYPE_DAMAGE,power=80,setAoEDamage=True,area=AREA_RANDOMENNEMI_4,effectOnSelf=naciaAirEff,cooldown=4,emoji='<:enemyAer:1042313031926947920>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR])
naciaAirSkill3_cast_3 = effect("Cast - Vitesse Aérienne","naciaVitCast1",replique=naciaAirSkill3_3,silent=True)
naciaAirSkill3_2 = skill("Vitesse Aérienne","naciaSkill3",TYPE_DAMAGE,power=70,setAoEDamage=True,area=AREA_RANDOMENNEMI_4,effectOnSelf=naciaAirSkill3_cast_3,emoji='<:enemyAer:1042313031926947920>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],replay=True)
naciaAirSkill3_cast_2 = effect("Cast - Vitesse Aérienne","naciaVitCast1",replique=naciaAirSkill3_2,silent=True)
naciaAirSkill3 = skill("Vitesse Aérienne","naciaSkill3",TYPE_DAMAGE,power=60,setAoEDamage=True,area=AREA_RANDOMENNEMI_4,effectOnSelf=naciaAirSkill3_cast_2,emoji='<:enemyAer:1042313031926947920>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],replay=True)
naciaAirSkill = skill("Souffle de la planète","naciaSkill3",TYPE_DAMAGE,emoji=liaWeap.effects.emoji[0][0],become=[naciaAirSkill1,naciaAirSkill2,naciaAirSkill3],cooldown=4,description="Nacialisla utilise des compétences aérienne pour infliger des dégâts tout en repoussant ses ennemis",condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR])
naciaWaterEff = effect("Puissance Aquatique","naciaWaterEff",turnInit=10,emoji=lioWeap.effects.emoji,description="Nacialisa a galvanisé les alentours avec une grande puissance élémentaire")
naciaWaterSkill1 = skill("Pluie diluvienne","naciaSkill4",TYPE_DAMAGE,power=85,setAoEDamage=True,range=AREA_MONO,area=AREA_ALL_ENEMIES,cooldown=4,effectOnSelf=naciaWaterEff,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],effectAroundCaster=[TYPE_HEAL,AREA_MONO,50],damageOnArmor=0.6)
naciaWaterSkill2 = skill("Déluge","naciaSkill4",TYPE_DAMAGE,power=150,range=AREA_MONO,area=AREA_CIRCLE_4,knockback=2,cooldown=4,effectOnSelf=naciaWaterEff,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],effectAroundCaster=[TYPE_HEAL,AREA_MONO,50],damageOnArmor=0.7)
naciaWaterSkill3 = skill("Grèle","naciaSkill4",TYPE_DAMAGE,power=80,setAoEDamage=True,range=AREA_MONO,area=AREA_DIST_7,cooldown=4,effectOnSelf=naciaWaterEff,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],effectAroundCaster=[TYPE_HEAL,AREA_MONO,50],damageOnArmor=0.7)
naciaWaterSkill = skill("Tempéralité de la planète","naciaSkill4",TYPE_DAMAGE,emoji=lioWeap.effects.emoji[0][0],become=[naciaWaterSkill1,naciaWaterSkill2,naciaWaterSkill3],cooldown=4,description="Nacialisla utilise des compétences aquatique magique pour infliger des dégâts à un grand nombre d'ennemis",use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER])
naciaEarthFire = skill("Terre Brûlée","naciaMultiElemSkill",TYPE_DAMAGE,power=135,emoji='<:nasElem1:1048532399451033640>',range=AREA_MONO,area=AREA_CIRCLE_3,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_CIRCLE_3,naciaFireSkill1Eff],effPowerPurcent=80,cooldown=3,needEffect=[naciaEarthEff,naciaFireEff],condition=[EXCLUSIVE,ELEMENT,ELEMENT_UNIVERSALIS_PREMO])
naciaEarthWater = skill("Marécage","naciaMultiElemSkill",TYPE_DAMAGE,power=120,emoji='<:nasElem2:1048532444783058944>',range=AREA_MONO,area=AREA_CIRCLE_3,effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_3,naciaEarthSkill3Eff],effPowerPurcent=80,cooldown=3,needEffect=[naciaEarthEff,naciaWaterEff],condition=[EXCLUSIVE,ELEMENT,ELEMENT_UNIVERSALIS_PREMO])
naciaEarthAir = skill("Tempette de sable","naciaMultiElemSkill",TYPE_DAMAGE,power=120,emoji='<:nasElem3:1048532480468205711>',range=AREA_MONO,area=AREA_CIRCLE_3,knockback=7,cooldown=3,needEffect=[naciaEarthEff,naciaAirEff],condition=[EXCLUSIVE,ELEMENT,ELEMENT_UNIVERSALIS_PREMO])
naciaFireWaterEff = effect("Geyser","naciaFWEff", stat=MAGIE,power=50,area=AREA_CIRCLE_1,trigger=TRIGGER_ON_REMOVE,type=TYPE_INDIRECT_DAMAGE)
naciaFireWater = skill("Pulsation phréatique","naciaMultiElemSkill",TYPE_INDIRECT_DAMAGE,effects=naciaFireWaterEff,emoji='<:nasElem5:1048537048149151764>',range=AREA_MONO,area=AREA_RANDOMENNEMI_5,cooldown=3,needEffect=[naciaFireEff,naciaWaterEff],condition=[EXCLUSIVE,ELEMENT,ELEMENT_UNIVERSALIS_PREMO])
naciaFireAir = skill("Vent enflammé","naciaMultiElemSkill",TYPE_DAMAGE,emoji='<:nasElem4:1048537010543017994>',range=AREA_MONO,area=AREA_ALL_ENEMIES,power=80,setAoEDamage=True,cooldown=3,needEffect=[naciaFireEff,naciaAirEff],use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_UNIVERSALIS_PREMO])
naciaAirWaterEff = effect("Trempé","naciaAWEff", stat=STRENGTH,strength=-10,magie=-10,charisma=-10,intelligence=-10,turnInit=3,type=TYPE_MALUS)
naciaAirWater = skill("Tempette","naciaMultiElemSkill",TYPE_DAMAGE,emoji='<:nasElem6:1048540760909303818>',range=AREA_MONO,area=AREA_ALL_ENEMIES,power=65,setAoEDamage=True,cooldown=3,needEffect=[naciaWaterEff,naciaAirEff],effectAroundCaster=[TYPE_MALUS,AREA_ALL_ENEMIES,naciaAirWaterEff],condition=[EXCLUSIVE,ELEMENT,ELEMENT_UNIVERSALIS_PREMO])
naciaMultiElemSkill = skill("Volonté de la planète","naciaMultiElemSkill",TYPE_DAMAGE,emoji='<:nasElemBundle:1048541047485104258> ',become=[naciaEarthFire,naciaEarthWater,naciaEarthAir,naciaFireWater,naciaFireAir,naciaAirWater],cooldown=3,description="Nacialisla utilise les énergies élémentaires dispersés par ses autre compétences pour en utiliser de nouvelles")

GIANTESSHPBONUS, GIANTESSSTATBONUS = 65, 50
naciaGiantEff = effect("Puissance originelle","giantess",type=TYPE_UNIQUE,emoji='<:naciaGiant:1052323784562049185>',description="Augmente de **{0}%** les PV max et actuels de Nacialisla ainsi de **{1}%** sa Force, son Endurance, sa Précision et sa Magie, mais réduit de 100% sa probabilité d'esquive une attaque".format(GIANTESSHPBONUS,GIANTESSSTATBONUS),turnInit=15,trigger=TRIGGER_ON_REMOVE)
naciaGiant = skill("Gigantification","naciaGiant",TYPE_PASSIVE,effectOnSelf=naciaGiantEff,description="Lorsque Nacialisla tombe en dessous de **60%** de ses PV maximums, cette dernière prend une forme gigantesque, augmentant toutes ses statistiques",emoji='<:naciaGiant:1052323784562049185>')

iliOvlWeaponEff = effect("Contre","iliOvlWeaponEff",block=10,counterOnBlock=100,turnInit=-1,unclearable=True,emoji='<:iliOvlWeap:1139249680031699027>')
iliOvlWeapon = weapon("Rapière de Lumière","iliOvlWeapon",RANGE_DIST,AREA_CIRCLE_1,power=150,accuracy=80,emoji='<:iliOvlWeap:1139249680031699027>',effects=iliOvlWeaponEff,ignoreAutoVerif=True,priority=WEAPON_PRIORITY_LOWEST,use=MAGIE,damageOnArmor=2)
iliOvlSkill1 = skill("Perforation","iliOvlSkill1",TYPE_DAMAGE,power=350,range=AREA_CIRCLE_1,area=AREA_LINE_3,accuracy=200,emoji='<:iliOvlSkill1:1139249727012098229>',garCrit=True,cooldown=5,description="Iliana inflige une attaque transperçante aux ennemis ciblés. La cible initiale reçoit forcément un coup critique",use=MAGIE,damageOnArmor=1.25,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
iliOvlSkill2_1 = skill("Rayon Diffractif","iliOvlSkill2",TYPE_DAMAGE,power=250,area=AREA_CONE_3,range=AREA_CIRCLE_1,cooldown=3,emoji='<:iliOvlSkill22:1139254745337438300>',description="Inflige une attaque en cône aux ennemis ciblés",use=MAGIE,damageOnArmor=1.25,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
iliOvlSkill2_2 = skill("Rayon Concentré","iliOvlSkill2",TYPE_DAMAGE,power=350,area=AREA_CIRCLE_1,range=AREA_CIRCLE_1,cooldown=3,emoji='<:iliOvlSkill21:1139254767604990002>',description="Inflige une attaque en cercle aux ennemis ciblés",use=MAGIE,damageOnArmor=1.5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
iliOvlSkill2 = skill("Rayon de Lumière","iliOvlSkill2",TYPE_DAMAGE,become=[iliOvlSkill2_1,iliOvlSkill2_2],emoji='<:iliOvlSkill21:1139254767604990002>',description="Iliana inflige des dégâts de zone aux ennemis ciblés",condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
iliOvlSkill3 = skill("Vitesse Lumière","iliOvlSkill3",TYPE_DAMAGE,power=50,area=AREA_RANDOMENNEMI_5,range=AREA_MONO,repetition=3,emoji='<:iliOvlSkill3:1139249659701887027>',damageOnArmor=1.25,accuracy=200,setAoEDamage=True,cooldown=5,use=MAGIE,description="Inflige des dégâts à 15 reprises à des ennemis aléatoire",condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
iliOvlSkill4Eff1 = copy.deepcopy(vulne)
iliOvlSkill4Eff1.power, iliOvlSkill4Eff1.turnInit = 25,3
iliOvlSkill4 = skill("Corruption","iliSkill4",TYPE_DAMAGE,power=225,range=AREA_MONO,area=AREA_CIRCLE_3,cooldown=5,effectAroundCaster=[TYPE_MALUS,AREA_DONUT_3,iliOvlSkill4Eff1],emoji='<:iliOvlSkill4:1139249705570795690>',accuracy=200,use=MAGIE,description="Inflige des dégâts aux ennemis alentours et augmente les dégâts qu'ils subissent",damageOnArmor=1.25,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT])
iliOvlSkill5 = skill("Révolution","iliSkill5",TYPE_DAMAGE,power=275,range=AREA_MONO,area=AREA_DIST_7,effectAroundCaster=[TYPE_DAMAGE,AREA_CIRCLE_2,150],use=MAGIE,initCooldown=2,cooldown=7,description="Inflige des dégâts aux ennemis éloignés, ainsi qu'une attaque plus puissante aux ennemis proches de vous",damageOnArmor=1.35,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],emoji='<:iliOvlSkill5:1139249633877557309>')
iliOvlSkill6Eff = copy.deepcopy(dmgUp)
iliOvlSkill6Eff.turnInit, iliOvlSkill6Eff.power, 5, 15
iliOvlSkill6 = skill("Oblation","iliOvlSkill6",TYPE_DAMAGE,power=180,area=AREA_CIRCLE_2,range=AREA_CIRCLE_3,effectOnSelf=iliOvlSkill6Eff,use=MAGIE,description="Inflige des dégâts aux ennemis ciblés et augmente vos dégâts infligés",initCooldown=2,cooldown=5,emoji='<:iliOvlSkill6:1139254326494244864>')

iliOvlSkill7Eff = effect("Jauge de Lumière","iliLightJauge",turnInit=-1,unclearable=True,emoji=elemEmojis[ELEMENT_LIGHT],jaugeValue=jaugeValue(
    emoji=jaugeButLight.jaugeValue.emoji,
    conds=[
        jaugeConds(INC_ALLY_DAMAGED,100/75/5)
    ]
))
iliOvlSkill7_1 = skill("Lumière de l'Éternité","iliOvlSkill7",TYPE_DAMAGE,power=500,range=AREA_MONO,setAoEDamage=True,cooldown=99,area=AREA_CIRCLE_2,emoji='<:ancientLight2:1147186259115118613>',ultimate=True,percing=5,description="Lorsque la {0} {1} d'Iliana est remplie, celle-ci inflige des dégâts en croix autour d'elle puis se met à charger Lumière de l'Éternité, infligeant d'énormes dégâts à tous ses ennemis".format(iliOvlSkill7Eff.emoji[0][0],iliOvlSkill7Eff.name),jaugeEff=iliOvlSkill7Eff,accuracy=500,effectAroundCaster=[TYPE_DAMAGE,AREA_DIST_7,175],use=MAGIE,minJaugeValue=100,say="ET MOURREZ !")
iliOvlSkill7_c = effect("Cast - Lumière de l'Éternité","iliOvlSkill7_c",turnInit=2,emoji='<:ancientLight1:1147186235727695943>',replique=iliOvlSkill7_1)
iliOvlSkill7 = skill("Lumière de l'Éternité","iliOvlSkill7",TYPE_DAMAGE,power=150,range=AREA_MONO,cooldown=99,area=AREA_INLINE_2,emoji='<:ancientLight1:1147186235727695943>',ultimate=True,description=iliOvlSkill7_1.description,effectOnSelf=iliOvlSkill7_c,jaugeEff=iliOvlSkill7Eff,minJaugeValue=100,use=MAGIE,say="MARCHEZ DANS LA LUMIÈRE !")
iliOvlSkill7.iaPow = 9999

importantSkills.append(iliOvlSkill6.id)
importantSkills.append(iliOvlSkill4.id)
importantSkills.append(iliOvlSkill3.id)
importantSkills.append(iliOvlSkill7.id)

says()

iliOvlSay= says(
    start="Vous pensez tenir combien de temps ?",
    onKill=["Un de moins !","Déjà ?","C'est tout ?","Moh, j'avais encore plein de trucs à te montrer"],
    redWinAlive="Vous pensiez avoir une chance ?",redWinDead="Tss. Trop lente",redLoose="Hmf... Ce que j'aimerais me cacher dans un coin là tout de suite...",
    blockBigAttack="C'est tout ce que tu peux faire ?",onHit=["Heh. On va bien voir combien de temps tu va pouvoir tenir","On encaisse bien manifestement","Pas trop mal","Oh je suppose que j'n'ai qu'à taper plus fort"],
    onMiss=["Huh","Hé tu pourrais arrêter de bouger deux secondes oui ?","Hmf"],takeHit=["Même un moustique a plus d'effet","Tu essayais vraiment là ?","Pas mal. À mon tour","Pas mal. J'peux commencer maintenant ?"])

naciaSay= says(
    start="Dooonc vous êtes venus à 16 et vous vous êtes dit que ça suffirai ?",
    onKill=["Vous m'obligez à employer les grands moyens là","Et donc, c'est tout ?","Je m'attendais à mieux...","Plutôt fragile ce jouet en fin de compte..."],
    redWinAlive="Bien essayé, mais je me suis un peu ennuyée quand même",redLoose="Très bien très bien félicitation vous avez gagné cette fois-ci",
    takeHit=["`Baille`","Hé le but c'est pas de me faire une manicure hein","Si c'est que ça...","Très bien. Mais je te préviens je changerais pas ta couche","Tu sais, je peux continuer longtemps comme ça"]
)