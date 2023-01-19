from advObjects.advSkills_1 import *

miracle = skill("Miracle",getAutoId(gigaLight3.id,True),TYPE_DAMAGE,500,power=80,cooldown=5,area=AREA_CIRCLE_3,range=AREA_MONO,emoji='<:holly:1009830417521713247>',effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_2,lightStun],condition=[EXCLUSIVE,ASPIRATION,MASCOTTE],description="Inflige des dégâts autour de vous et étourdit les ennemis en mêlée",use=CHARISMA,useActionStats=ACT_BOOST,group=SKILL_GROUP_HOLY)
celRivEff1, cellRivEff2 = copy.deepcopy(dmgUp), copy.deepcopy(dmgDown)
celRivEff1.power, cellRivEff2.power, celRivEff1.stat, cellRivEff2.stat = 3, 3, INTELLIGENCE, INTELLIGENCE
celRivEff3, cellRivEff4 = copy.deepcopy(celRivEff1), copy.deepcopy(cellRivEff2)
celRivEff3.power, cellRivEff4.power, celRivEff3.trigger, cellRivEff4.trigger, celRivEff3.callOnTrigger, cellRivEff4.callOnTrigger = 5, 5, TRIGGER_ON_REMOVE, TRIGGER_ON_REMOVE, celRivEff1, cellRivEff2
celRivEff5, celRivEff6 = copy.deepcopy(celRivEff3), copy.deepcopy(cellRivEff4)
celRivEff5.power, celRivEff6.power, celRivEff5.callOnTrigger, celRivEff6.callOnTrigger = 7, 7, celRivEff3, cellRivEff4
rivCel = skill("Rivière Céleste",getAutoId(miracle.id,True),TYPE_BOOST,750,effects=celRivEff5,effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_3,celRivEff6],range=AREA_MONO,area=AREA_CIRCLE_3,cooldown=7,ultimate=True,condition=[EXCLUSIVE,ASPIRATION,MASCOTTE],description="Augmente les dégâts infligés par les alliés et diminue ceux infligés par les ennemis atour de vous. La puissance des bonus et malus diminue pendant 3 tours",emoji='<:rivCel:1009830456402923681>')
toxiconEff = copy.deepcopy(vulne)
toxiconEff.power, toxiconEff.stat = 7, INTELLIGENCE
toxicon = skill("Toxicon II", getAutoId(rivCel.id,True),TYPE_DAMAGE,500,power=80,area=AREA_CIRCLE_1,effects=toxiconEff,effBeforePow=True,cooldown=5,use=INTELLIGENCE,useActionStats=ACT_BOOST,condition=[EXCLUSIVE,ASPIRATION,INOVATEUR],description="Augmente les dégâts reçus par l'ennemi ciblé puis lui inflige des dégâts, à lui ainsi qu'à vos ennemis proches",emoji='<:toxicon:1009830437012635779>')
seraphStrikeEff = copy.deepcopy(defenseUp)
seraphStrikeEff.power, seraphStrikeEff.stat, seraphStrikeEff.turnInit = 3.5, INTELLIGENCE, 3
seraphStrike = skill("Frappe Séraphique", getAutoId(toxicon.id,True),TYPE_DAMAGE,500,emoji='<:seraphStrike:1009830399352000562>',power=50,range=AREA_CIRCLE_3,tpCac=True,effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_3,seraphStrikeEff],cooldown=5,use=INTELLIGENCE,useActionStats=ACT_BOOST,condition=[EXCLUSIVE,ASPIRATION,MASCOTTE],description="Vous permet de sauter sur un ennemi en lui infligeant des dégâts, puis réduit les dégâts reçus par vous et vos alliés alentours pendant 3 tours")
sonarPaf = skill("Déployable - Sonar Paf", getAutoId(seraphStrike.id,True), TYPE_DEPL, 500, emoji='<:sonarPaf:1013747334825381938>', cooldown=7, depl=sonarPafDepl,range=AREA_CIRCLE_4, use=INTELLIGENCE)
asile = skill("Déployable - Asile", getAutoId(sonarPaf.id,True), TYPE_DEPL, 500, emoji='<:asile:1013753436300398672>', cooldown=7, depl=asileDepl,range=AREA_CIRCLE_3, use=CHARISMA)
bigBubbler = skill("Déployable - Super-Bouclier", getAutoId(asile.id,True), TYPE_DEPL, 500, emoji='<:bigBubbler:1013747304475410522>', cooldown=7, depl=bigBubbleDepl,range=AREA_MONO, use=INTELLIGENCE)
lohicaBrouillad = skill("Déployable - Brouillard Empoisonné", getAutoId(bigBubbler.id,True), TYPE_DEPL, 500, emoji="<:poisonusMist:1059084936100970556>",cooldown=7, depl=lohicaDepl, use=MAGIE,range=AREA_CIRCLE_3)
lacerTrap = skill("Déployable - Piège de Lacération", getAutoId(lohicaBrouillad.id,True), TYPE_DEPL, 500, emoji=lacerTrapDepl.icon[0],cooldown=7, depl=lacerTrapDepl, use=STRENGTH ,range=AREA_CIRCLE_3)
tacticoolerEff = effect("Raffréchis","tacticoolEff",INTELLIGENCE,endurance=3,agility=3,precision=3,dodge=5,description="Augmente légèrement l'endurance, l'agilté, la précision et la probabilité d'esquiver une attaquer",turnInit=3,emoji='<:tacticooler:1014240041960231043>')
tacticooler = skill("DistribuCool", getAutoId(lacerTrap.id,True),TYPE_BOOST,500,cooldown=5,effects=tacticoolerEff,emoji="<:tacticooler:1014240041960231043>",area=AREA_CIRCLE_2,range=AREA_CIRCLE_2)
trizooka = skill("Lance-Rafales", getAutoId(tacticooler.id,True),TYPE_DAMAGE,500,power=45,repetition=3,cooldown=7,emoji='<:triZooka:1014240959875256513>',area=AREA_CIRCLE_1,range=AREA_CIRCLE_4)
inkzooka = skill("Lance-Tornades", getAutoId(trizooka.id,True),TYPE_DAMAGE,500,power=40,repetition=3,cooldown=7,emoji='<:inkZooka:1014240929374294137>',area=AREA_LINE_3,range=AREA_CIRCLE_4)
inkStrikeEff = effect("Missile-Tornade","inkStrike",STRENGTH,power=120,area=AREA_CIRCLE_2,trigger=TRIGGER_ON_REMOVE,type=TYPE_INDIRECT_DAMAGE,emoji=sameSpeciesEmoji("<:tbMissile:1014242512443027496>","<:trMissile:1014242582185914398>"))
inkStrike = skill("Missile Tornade", getAutoId(inkzooka.id,True), TYPE_INDIRECT_DAMAGE, 500, effects=inkStrikeEff, cooldown=7, emoji='<:missileTornade:1014242376476282901>')
sacredSoil = skill("Dogme de Survie", getAutoId(inkStrike.id,True), TYPE_DEPL, 500, range=AREA_CIRCLE_3, cooldown=5, depl=dogmeDepl, use=INTELLIGENCE, emoji='<:sacredSoil:1014239981474168982>')
epidemicReject = copy.deepcopy(infection.reject[0])
epidemicReject.name, epidemicReject.id = epidemicReject.name.replace("Infection","Epidémie"), "epidemicReject"
epidemicEff = effect("Epidémie","epidemicEff",MAGIE,power=infection.power,turnInit=2,lvl=2,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN, reject=[epidemicReject], emoji='<:epidemic:1016787710666616902>')
epidemic = skill("Epidémie", getAutoId(sacredSoil.id,True), TYPE_INDIRECT_DAMAGE, 500, effects=epidemicEff, range=AREA_CIRCLE_4, emoji='<:epidemic:1016787710666616902>', cooldown=5, description="Inflige {0} __{1}__ à l'ennemi ciblé, lui infligeant des dégâts en début de tour et propageant l'effet à vos ennemis au corps à corps de lui avec une puissance réduite de **15%**\nUne cible infectée de peut plus subir l'effet {0} __{1}__ pendant **5 tours**".format(epidemicEff.emoji[0][0],epidemicEff.name))
intoxReject = copy.deepcopy(infection.reject[0])
intoxReject.name, intoxReject.id, intoxReject.turnInit = intoxReject.name.replace("Infection","Intoxication"), "intoxReject", 3
intoxEff = effect("Intoxication","intoxEff",MAGIE,power=int(infection.power*0.7),turnInit=2,lvl=2,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN, reject=[intoxReject], emoji='<:intox:1016787678299177070>')
intox = skill("Intoxication", getAutoId(epidemic.id,True), TYPE_INDIRECT_DAMAGE, 500, effects=intoxEff, range=AREA_CIRCLE_4, emoji='<:intox:1016787678299177070>', cooldown=5, description="Inflige {0} __{1}__ à l'ennemi ciblé, lui infligeant des dégâts en début de tour et propageant l'effet à vos ennemis au corps à corps de lui avec une puissance réduite de **15%**\nUne cible infectée de peut plus subir l'effet {0} __{1}__ pendant **3 tours**".format(intoxEff.emoji[0][0],intoxEff.name))
exploHealMarkEff = effect("Explosoins","exploHeal",turnInit=-1, unclearable=True, power=40, emoji='<:explosoins:1016796973636010026>', stat=HARMONIE, area=AREA_DONUT_2)
expoHeal = skill("Explosoins", getAutoId(intox.id,True), TYPE_PASSIVE, 500, effectOnSelf=exploHealMarkEff, use=HARMONIE, emoji='<:explosoins:1016796973636010026>', description = "Lorsqu'un ennemi est vaincu, tous vos effects de dégâts indirects soignent vos alliés à portée pour **{0}%** de leur puissance cumulée restante (maximum **{1}**) en utilisant la statistique d'Harmonie".format(exploHealMarkEff.power, 50), power= 50, quickDesc="Effectue des soins harmoniques autours des ennemis lorsqu'ils sont vaincu en portant vos effets de dégâts indirects")
ultraSignalEffect = effect("Ciblé","ultraTargeted",STRENGTH,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_ON_REMOVE,area=AREA_CIRCLE_1, power=70, emoji=sameSpeciesEmoji("<:usb:1020048206081560616>","<:usr:1020048267142234173>"))
ultraSignalLauch = skill("Ultra-Signal",getAutoId(expoHeal.id,True), TYPE_INDIRECT_DAMAGE, 500, effects=ultraSignalEffect, cooldown=7, area=AREA_CIRCLE_3, ultimate=True, emoji='<:ultrasignal:1020048149055815900>')
ultraSignalCast = effect("Cast - {replicaName}", "castUltraSignal", turnInit=2, silent=True, replique = ultraSignalLauch)
ultraSignal = copy.deepcopy(ultraSignalLauch)
ultraSignal.effects, ultraSignal.effectOnSelf = [None], ultraSignalCast
forestShield = effect("Protection Sylvestre","forestShield",type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,stat=INTELLIGENCE,overhealth=50,emoji='<:gardeSilvestre:1023609768427925594>')
forestGarde = skill("Protection Silvestre",getAutoId(ultraSignal.id,True),TYPE_HEAL,500, power=forestShield.power,cooldown=5,use=INTELLIGENCE,useActionStats=ACT_SHIELD,effects=forestShield,emoji='<:gardeSilvestre:1023609768427925594>',description="Soigne l'allié ciblé et lui octroi une armure avec la même puissance")
lillyTrasformHeal = effect("Bénédiction Sylvestre","lillyTransformHeal",CHARISMA,power=25,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji='<:lilly:1023609807720161351>')
lillyTransformSelf = copy.deepcopy(healDoneBonus)
lillyTransformSelf.power, lillyTransformSelf.turnInit = 15, 3
lillyTransform = skill("Appel de la Chouette",getAutoId(forestGarde.id,True), TYPE_INDIRECT_HEAL, 500, effects=lillyTrasformHeal, effectOnSelf=lillyTransformSelf, cooldown=7, emoji='<:lilly:1023609807720161351>', description="Applique un effet de récupération sur l'allié ciblé pendant 3 tours et augmente de **{0}%** vos soins réalisé sur la même durée".format(lillyTransformSelf.power))
mendRegen = effect("Remède Sylvestre","mendRegen",CHARISMA,power=15,turnInit=3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji="<:mend:1023609835981389854>")
mend = skill("Remède Sylvestre",getAutoId(lillyTransform.id,True),TYPE_HEAL,500,mendRegen.power*mendRegen.turnInit,effects=mendRegen,cooldown=5,description="Soigne l'allié ciblé et lui octroi un effet régénérant durant 3 tours",emoji=mendRegen.emoji[0][0])
constBenEff = copy.deepcopy(constEff)
constBenEff.power, constBenEff.stat, constBenEff.turnInit = 80, CHARISMA, 3
constBen = skill("Constitution Divine",getAutoId(mend.id,True),TYPE_HEAL,750,effects=constBenEff,power=70,cooldown=7,maxHpCost=10,group=SKILL_GROUP_HOLY,emoji='<:constDiv:1028679968944824351>',range=AREA_DONUT_4,description="Soigne un allié et augmente temporairement ses PV maximums")
antConstEff = copy.deepcopy(aconstEff)
antConstEff.power, antConstEff.stat, antConstEff.turnInit = 70, STRENGTH, 5
antConst = skill("Anticonstitution",getAutoId(constBen.id,True),TYPE_DAMAGE,750,power=100,range=AREA_CIRCLE_3,effects=antConstEff,cooldown=7,condition=[EXCLUSIVE,ASPIRATION,TETE_BRULE],emoji='<:ConR:1028695463651717200>',erosion=50,description="Inflige des dégâts un ennemi et réduit temporairement ses PV Maximums")
lifeSeedEff = effect("Graine de Vie","lifeSeed",CHARISMA,power=70,area=AREA_CIRCLE_1,emoji='<:lifeSeed:1028680000628596817>',trigger=TRIGGER_ON_REMOVE,type=TYPE_INDIRECT_HEAL,turnInit=3)
lifeSeed = skill("Graine de Vie",getAutoId(antConst.id,True),TYPE_HEAL,750,emoji='<:lifeSeed:1028680000628596817>',power=35,effects=lifeSeedEff,cooldown=7,description="Soigne un allié et place sur lui une Graine de Vie qui réalisera des soins en zone {0} tours plus tard".format(lifeSeedEff.turnInit))
assasinateEff = copy.deepcopy(vulne)
assasinateEff.power = 25
assasinate = skill("Assasinat",getAutoId(lifeSeed.id,True),TYPE_DAMAGE,750,power=150,range=AREA_CIRCLE_2,tpCac=True,effects=assasinateEff,cooldown=7,effBeforePow=True,ultimate=True,erosion=65,emoji='<:assasinate:1030105420552994837>',description="Augmente les dégâts reçus par la cible et lui inflige de gros dégâts tout en réduisant ses PV Maximums")
traqnardEff = effect("Vulnérabilité Indirecte","traqnardEff",inkResistance=-20,turnInit=3,type=TYPE_MALUS,emoji=sameSpeciesEmoji("<:vulneB:1029816126353444894>","<:vulneR:1029816158540546120>"),description="Augmente les dégâts indirects reçus par le porteur")
physTraqnard = skill("Traqnard Physique",getAutoId(assasinate.id,True),TYPE_DAMAGE,500,cooldown=5,power=70,range=AREA_CIRCLE_1,knockback=2,effects=traqnardEff,description="Inflige des dégâts à l'ennemi ciblé, augmente les dégâts indirects qu'il reçoit et le repousse",emoji='<:traqD:1029819539497701437>')
fairyTraqnard = skill("Traqnard Féérique",getAutoId(physTraqnard.id,True),TYPE_DAMAGE,500,power=80,effects=traqnardEff,area=AREA_CIRCLE_1,useActionStats=ACT_INDIRECT,cooldown=5,use=MAGIE,emoji='<:traqFairy:1029819512213733498>')
blodTraqnard = skill("Traqnard Sanglant",getAutoId(fairyTraqnard.id,True),TYPE_DAMAGE,500,power=80,effects=traqnardEff,area=AREA_CIRCLE_1,useActionStats=ACT_INDIRECT,cooldown=5,emoji='<:tradBlood:1029819483390492763>')
carnageEff = copy.deepcopy(incurable)
carnageEff.power = 30
carnage = skill("Carnage",getAutoId(blodTraqnard.id,True),TYPE_DAMAGE,500,emoji='<:carnage:1030489266784059472>',range=AREA_MONO,area=AREA_CIRCLE_1,power=100,cooldown=5,effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_1,carnageEff],description="Inflige des dégâts aux ennemis à votre corps à corps et réduit les osins qu'ils reçoivent durant un tour")
dissi2Eff = effect("Dissimulation Ombrale","dissi2Eff",translucide=True,aggro=-30,description="Vous rend Translucide et réduit la probabilité d'être attaqué",emoji='<:dissi:1029816091020640346>')
UmbralTravel = skill("Voyage Ombral",getAutoId(carnage.id,True),TYPE_DAMAGE,500,power=80,cooldown=5,tpCac=True,range=AREA_DIST_5,effectOnSelf=dissi2Eff,description="Vous téléporte au corps à corps de l'ennemi ciblé tout en lui infligeant des dégâts et réduit votre propabilité d'être pris pour cible jusqu'à votre prochain tour",emoji='<:umbralRush:1029819601581785169>')
silvArmorEff = effect("Armure Silvestre","silvArmor",INTELLIGENCE,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,overhealth=80,inkResistance=10,emoji='<:vegeProtect:1028680031498674266>',turnInit=3)
silvArmor = skill("Armure Silvestre",getAutoId(UmbralTravel.id,True),TYPE_ARMOR,500,cooldown=7,effects=silvArmorEff,emoji='<:vegeProtect:1028680031498674266>')
ghostlyCircleArmor = effect("Armure fantômatique","ghostArmor",INTELLIGENCE,overhealth=40,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
ghostlyCircle = skill("Cercle Fantômatique",getAutoId(silvArmor.id,True),TYPE_ARMOR,500,cooldown=5,range=AREA_MONO,area=AREA_CIRCLE_3,useActionStats=ACT_SHIELD,description="Octroi une armure au lanceur et ses alliés alentours tout en infligeant des dé^gats aux ennemis en mêlée",effectAroundCaster=[TYPE_DAMAGE,AREA_CIRCLE_2,50],setAoEDamage=True,effects=ghostlyCircleArmor,emoji='<:ghostlyCircle:1033016192081866783>',condition=[EXCLUSIVE,ASPIRATION,PROTECTEUR])
spectralFurie =  skill("Furie Spectrale",getAutoId(ghostlyCircle.id,True),TYPE_DAMAGE,500,cooldown=5,power=int(125/5),repetition=5,armorConvert=50,use=MAGIE,sussess=90,condition=[EXCLUSIVE,ASPIRATION,ENCHANTEUR],emoji='<:spectralFury:1033016230333911080>',range=AREA_CIRCLE_2,description="Inflige des dégâts à plusieurs reprises sur l'ennemi ciblé et converti une partie des dégâts infligés en armure")
spectralCircle = skill("Cercle Spectral",getAutoId(spectralFurie.id,True),TYPE_DAMAGE,500,cooldown=5,power=85,armorConvert=30,use=MAGIE,condition=[EXCLUSIVE,ASPIRATION,ENCHANTEUR],sussess=120,description="Inflige des dégâts aux ennemis alentours et convertie une partie des dégâts infligés en armure",range=AREA_MONO,area=AREA_CIRCLE_2,emoji='<:spectralCircle:1033016601584353300>')
immoArrow = skill("Flèche d'Immolation",getAutoId(spectralCircle.id,True),TYPE_DAMAGE,500,cooldown=5,emoji='<:imolArrow:1032288557286576138>',power=90,area=AREA_LINE_3,range=AREA_DIST_5,effects=physTraqnard.effects,description='Inflige des dégâts aux ennemis ciblés et augmente les dégâts indirects reçus par la cible principale',condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE])
exploArrow = skill("Flèche Explosive",getAutoId(immoArrow.id,True),TYPE_DAMAGE,500,cooldown=7,ultimate=True,power=180,range=AREA_DIST_5,area=AREA_CIRCLE_2,emoji='<:exploArrow:1032288726233124958>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE])
freezeArrow = skill("Flèche Gelante",getAutoId(exploArrow.id,True),TYPE_DAMAGE,500,cooldown=5,power=100,effects=chained,description="Inflige des dégâts à l'ennemi ciblé et l'immobilise pendant un tour",condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],emoji='<:imoArrow:1032288442433945721>',range=AREA_DIST_6)
freezeArrow2Eff = copy.deepcopy(vulne)
freezeArrow2Eff.power = 15
freezeArrow2 = skill("Flèche Givrante",getAutoId(freezeArrow.id,True),TYPE_DAMAGE,500,cooldown=5,power=100,effects=freezeArrow2Eff,effBeforePow=True,description="Augmente les dégâts reçus de l'ennemi ciblé et lui inflige des dégâts",condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],emoji='<:iceFrag:1032288516069150720>',range=AREA_DIST_6)
ebranlement = skill("Ebranlement",getAutoId(freezeArrow2.id,True),TYPE_DAMAGE,500,cooldown=5,power=100,armorConvert=50,damageOnArmor=2,range=AREA_CIRCLE_2,description="Inflige des dégâts à l'ennemi ciblé et en convertie une partie en armure pour vous même.\nDégâts augmentés sur l'armure",emoji='<:fulgur:1032288871565754408>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH])
hearthFrac = skill("Fracture Terrestre",getAutoId(ebranlement.id,True),TYPE_DAMAGE,500,cooldown=5,power=80,effects=freezeArrow2Eff,range=AREA_CIRCLE_2,description="Augmente les dégâts reçus de l'ennemi ciblé et lui inflige des dégâts",condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],emoji='<:earthFrag:1032288813499818055>')
hourglassEff = effect("Sablier","hourglassEff",MAGIE,power=80,trigger=TRIGGER_ON_REMOVE,type=TYPE_INDIRECT_DAMAGE,emoji='<:hourglass:1032288468786745487>',area=AREA_CIRCLE_1)
hourglass = skill("Sablier",getAutoId(hearthFrac.id,True),TYPE_INDIRECT_DAMAGE,500,cooldown=5,effects=hourglassEff,emoji='<:hourglass:1032288468786745487>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],description="Inflige des dégâts à la cible et aux ennemis alentours lors de votre prochain tour")
clockEff = effect("Horloge","clockEff",MAGIE,power=110,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_ON_REMOVE,emoji='<:clock:1032288491247243296>')
clock = skill("Horloge",getAutoId(hourglass.id,True),TYPE_INDIRECT_DAMAGE,500,cooldown=5,effects=clockEff,emoji=clockEff.emoji[0][0],condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],description="Inflige des dégâts à la cible lors de votre prochain tour")
elipseTerrestre = skill("Elipse Terrestre",getAutoId(clock.id,True),TYPE_DAMAGE,500,cooldown=5,power=80,range=AREA_MONO,area=AREA_CIRCLE_2,armorConvert=40,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],emoji='<:elipTer:1034208837772779530>',description="Inflige des dégâts aux ennemis autour de vous et converti une partie des dégâts infligés en armure")
piedVolt = skill("Pied Voltige",getAutoId(elipseTerrestre.id,True),TYPE_DAMAGE,500,cooldown=5,power=85,range=AREA_CIRCLE_3,tpCac=True,knockback=2,description="Vous téléporte au corps à corps de la cible, lui inflige des dégâts et le repousse",emoji='<:piedVolt:1034208868068233348>')
retImpEff = copy.deepcopy(impactShield)
retImpEff.stat = STRENGTH
retourneImpactant = skill("Retourné Impactant",getAutoId(piedVolt.id,True),TYPE_DAMAGE,500,cooldown=5,power=95,range=AREA_CIRCLE_3,effectOnSelf=retImpEff,description="Inflige des dégâts à l'ennemi ciblé, vous fait reculer d'une case et vous octroi une armure",jumpBack=1)
dmonAgiEff = effect("Esquive Démoniaque","dmonAgiEff",INTELLIGENCE,agility=5,dodge=15,counterOnDodge=35,emoji='<:dmnagi:1045691488161517609>',description="Augmente l'agilité, la probabilité d'esquive et celle d'effectuer une contre-attaque lors d'une esquive du porteur")
dmonAgi = skill("Esquive Démonaique",getAutoId(retourneImpactant.id,True),TYPE_BOOST,500,cooldown=5,effects=dmonAgiEff,emoji='<:esqDmon:1045612328588161074>',group=SKILL_GROUP_DEMON,hpCost=15,area=AREA_CIRCLE_2,description="Augmente l'agilité, la probabilité d'esquive ainsi que celle d'effectuer une contre-attaque lors d'une esquive des alliés ciblés")
dmonEndEff1 = effect("Blocage Démoniaque","dmonEnEff1",INTELLIGENCE,endurance=5,block=35,emoji='<:dmnend:1045691545686392854>',description="Augmente l'endurance et la probabilité de bloquer une attaque du porteur")
dmonEndEff2 = copy.deepcopy(defenseUp)
dmonEndEff2.stat, dmonEndEff2.power = INTELLIGENCE, 3.5
dmonEnd = skill("Blocage Démoniaque",getAutoId(dmonAgi.id,True),TYPE_BOOST,500,cooldown=5,effects=[dmonEndEff1,dmonEndEff2],emoji='<:bloDmon:1045612358107672617>',description="Augmente l'endurance ainsi que la probabilité de bloquer une attaque tout en réduisant les dégâts subis par les alliés ciblés",area=AREA_CIRCLE_2,group=SKILL_GROUP_DEMON,hpCost=15)
dmonCritEff = effect("Critique Démoniaque","dmonCritEff",INTELLIGENCE,precision=5,critical=2,critDmgUp=10,critHealUp=10,emoji='<:dmncrit:1045691517307719701>',description="Augmente la précision, le taux de critique ainsi que les dégâts et soins réalisés lors d'une action critique du lanceur")
dmonCrit = skill("Critique Démoniaque",getAutoId(dmonEnd.id,True),TYPE_BOOST,500,cooldown=5,effects=dmonCritEff,emoji='<:criDmon:1045612385588744223>',group=SKILL_GROUP_DEMON,hpCost=15,area=AREA_CIRCLE_2,description="Augmente la précision, le taux de critique ainsi que les dégâts et soins réalisés lors d'une action critique des alliés ciblés")
dmonDmgEff1 = effect("Dégât Démoniaque","dmonDmgEff1",INTELLIGENCE,strength=3.5,magie=3.5,emoji='<:dmndmg:1045691580620755006>',description="Augmente la force et la magie du porteur")
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
apexArrowEff1 = effect("Alpha Forte","apexAro1",STRENGTH,strength=5,turnInit=4,emoji="<:songPhys:1046123900519587934>",description="Augmente votre Force en fonction de votre propre Force")
apexArrowEff2 = effect("Ballade du Mage","apexAro2",CHARISMA,magie=5,turnInit=3,emoji="<:enharMag:1046122914400968735>",description="Augmente la Magie du porteur en fonction du Charisme du lanceur")
apexArrow = skill("Trait Alpha",getAutoId(dmonReconstitution2.id,True),TYPE_DAMAGE,750,110,range=AREA_DIST_6,area=AREA_LINE_3,cooldown=7,effectOnSelf=apexArrowEff1,effectAroundCaster=[TYPE_BOOST,AREA_DONUT_3,apexArrowEff2],description="Inflige des dégâts aux ennemis ciblés puis augmente votre propre Force en fonction de votre Force et la Magie de vos alliés alentours en fonction de votre Charisme",emoji="<:apexArrow:1046129746704093204>")
blastArrowEff2 = effect("Péon Martial","apexAro2",CHARISMA,strength=5,turnInit=3,emoji="<:enharPhys:1046122887028932689>",description="Augmente la Force du porteur en fonction du Charisme du lanceur")
blastArrow = skill("Flèche Musicale",getAutoId(apexArrow.id,True),TYPE_DAMAGE,750,110,range=AREA_DIST_6,area=AREA_LINE_3,cooldown=7,effectOnSelf=apexArrowEff1,effectAroundCaster=[TYPE_BOOST,AREA_DONUT_3,blastArrowEff2],description="Inflige des dégâts aux ennemis ciblés puis augmente votre propre Force en fonction de votre Force et celle de vos alliés alentours en fonction de votre Charisme",emoji="<:blastArrow:1046129829583536230>")
enhardEff1 = effect("Marche Conquérante","enhar1",MAGIE,magie=5,turnInit=4,emoji='<:songMag:1046123862712127538>',description="Augmente votre Magie en fonction de votre propre Magie")
enhardEff2 = effect("Péon Martial","enhar2",INTELLIGENCE,strength=5,turnInit=3,emoji="<:enharPhys:1046122887028932689>",description="Augmente la Force du porteur en fonction de l'Intelligence du lanceur")
enhardissement = skill("Enhardissement",getAutoId(blastArrow.id,True),TYPE_DAMAGE,750,100,use=MAGIE,range=AREA_CIRCLE_6,area=AREA_CIRCLE_1,cooldown=7,effectOnSelf=enhardEff1,effectAroundCaster=[TYPE_BOOST,AREA_DONUT_3,enhardEff2],description="Inflige des dégâts aux ennemis ciblés puis augmente votre propre Magie en fonction de votre Magie et la Force de vos alliés alentours en fonction de votre Intelligence",emoji='<:enhardissement:1046129975662743692>')
manafication2 = effect("Ballade du Mage","manafication2",INTELLIGENCE,magie=5,turnInit=3,emoji="<:enharMag:1046122914400968735>",description="Augmente la Magie du porteur en fonction de l'Intelligence du lanceur")
manafication = skill("Manafication",getAutoId(enhardissement.id,True),TYPE_DAMAGE,750,100,use=MAGIE,range=AREA_CIRCLE_6,area=AREA_CIRCLE_1,cooldown=7,effectOnSelf=enhardEff1,effectAroundCaster=[TYPE_BOOST,AREA_DONUT_3,manafication2],description="Inflige des dégâts aux ennemis ciblés puis augmente votre propre Magie en fonction de votre Magie et celle de vos alliés alentours en fonction de votre Intelligence",emoji='<:manafication:1046129876601667634>')

mageBaladEff = effect("Ballade du Mage","mageBaladEff",CHARISMA,magie=5,turnInit=3,description="Augmente la magie du porteur en fonction du charisme du lanceur",emoji="<:songMag:1046123862712127538>")
mageBalad = skill("Ballade du Mage",getAutoId(manafication.id,True),TYPE_DAMAGE,500,power=100,emoji='<:mageBallad:1047197760253861959>',effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_3,mageBaladEff],description="Inflige des dégâts à l'ennemi ciblé et augmente votre Magie ainsi que celle de vos équipiers alentours",cooldown=7)
martialPeanEff = effect("Péan Martial","martialPeanEff",CHARISMA,strength=5,turnInit=3,description="Augmente la force du porteur en fonction du charisme du lanceur",emoji="<:songPhys:1046123900519587934>")
martialPean = skill("Péan Martial",getAutoId(mageBalad.id,True),TYPE_DAMAGE,500,power=100,emoji='<:martialPean:1047197814834339871>',effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_3,martialPeanEff],description="Inflige des dégâts à l'ennemi ciblé et augmente votre Force ainsi que celle de vos équipiers alentours",cooldown=7)
vanderManuetEff = effect("Menuet du Vagabon","vanderManuetEff",CHARISMA,strength=3,magie=3,turnInit=3,description="Augmente la force et la magie du porteur en fonction du charisme du lanceur",emoji="<:menuet:1047210617087467552>")
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
heroicFantasyEff1 = effect("Fantaisie Héroïque","heroicFantasyEff1",CHARISMA,strength=12,magie=7,precision=5,charisma=5,description="Augmente plusieurs de vos statistiques en fonction de votre charisme\nLa puissance de ce bonus reste la même qu'importe la quantité de {0} {1} consommée".format(heroicFantasyJauge.emoji[0][0],heroicFantasyJauge.name),emoji='<:heroicFantasy:1047213807690334289>',turnInit=4)
heroicFantasyEff2 = effect("Fantaisie Orchestrale","heroicFantasyEff2",CHARISMA,strength=15,magie=15,precision=10,intelligence=10,endurance=5,charisma=5,description="Augmente plusieurs statistiques du porteur en fonction du charisme du lanceur\nLa puissance de l'effet dépend de la quantité de {0} {1} consommée. Les statisitques affichés ici sont ceux de l'effet à sa puissance maximale".format(heroicFantasyJauge.emoji[0][0],heroicFantasyJauge.name),emoji='<:orchestralFantasy:1047213865387171931>',turnInit=3)
heroicFantasy = skill("Fantaisie Héroïque",getAutoId(vanderManuet.id,True),TYPE_BOOST,750,range=AREA_MONO,area=AREA_DONUT_5,minJaugeValue=50,maxJaugeValue=100,effects=heroicFantasyEff2,effectOnSelf=heroicFantasyEff1,ultimate=True,cooldown=3,emoji='<:fantasy:1047197880257085561>',description="Augmente grandement les statistiques de vos alliés alentours en fonction de votre {0} {1}, ainsi que vos propres statistiques indépendament de la dites jauge".format(heroicFantasyJauge.emoji[0][0],heroicFantasyJauge.name),jaugeEff=heroicFantasyJauge)
exploShotEff = effect("Tir Explosif","exploShotEff",STRENGTH,power=50,trigger=TRIGGER_INSTANT,type=TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_1,emoji="<:exploShotEff:1049704001257619476>",description="Inflige des dégâts autour du porteur")
exploShot = skill("Tir Explosif",getAutoId(heroicFantasy.id,True),TYPE_DAMAGE,500,power=60,cooldown=5,percing=35,description="Inflige des dégâts à la cible puis provoque une explosion indirecte à sa position",emoji='<:exploShot:1049703940738007050>',effects=exploShotEff)
stigmateEff = effect("Stigmate","stigmate",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,turnInit=2,lvl=2,emoji='<:stigmates:1047198003435425873>',power=40,area=AREA_CIRCLE_1,description="Inflige des dégâts aux ennemis dans la zone d'effet au début du tour du porteur")
stigmateEff2 = copy.deepcopy(mageBaladEff)
stigmate = skill("Stigmate",getAutoId(exploShot.id,True),TYPE_DAMAGE,750,50,use=MAGIE,area=AREA_CIRCLE_1,effects=stigmateEff,cooldown=7,emoji=stigmateEff.emoji[0][0],effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_3,stigmateEff2],description="Inflige des dégâts aux ennemis ciblé avec un effet de réplique lors de vos deux prochains tours et augmente la Magie de vous même et vos alliés alentours")
stigmateEff2.description += "\n\nNon cumulable avec l'effet octroyé par {0} {1}".format(mageBalad.emoji,mageBalad.name)
mageBaladEff.description+= "\n\nNon cumulable avec l'effet octroyé par {0} {1}".format(stigmate.emoji,stigmate.name)
dissEff = effect("Dissonance","dissEff",MAGIE,power=25,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,area=AREA_CIRCLE_3,emoji='<:dissonance:1047197979674681374>',description="Inflige des dégâts aux ennemis dans la zone d'effet au début du tour du porteur")
dissEff2 = copy.deepcopy(martialPeanEff)
dissonance = skill("Dissonance",getAutoId(stigmate.id,True),TYPE_DAMAGE,750,40,use=MAGIE,area=AREA_CIRCLE_3,effects=dissEff,cooldown=7,emoji=dissEff.emoji[0][0],effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_3,dissEff2],description="Inflige des dégâts aux ennemis ciblé avec un effet de réplique lors de vos deux prochains tours et augmente la Force de vous même et vos alliés alentours")
dissEff2.description += "\n\nNon cumulable avec l'effet octroyé par {0} {1}".format(martialPean.emoji,martialPean.name)
martialPeanEff.description+= "\n\nNon cumulable avec l'effet octroyé par {0} {1}".format(dissonance.emoji,dissonance.name)
vibrSonEff = copy.deepcopy(vanderManuetEff)
vibrSon = skill("Vivration Sonique",getAutoId(dissonance.id,True),TYPE_DAMAGE,500,100,use=MAGIE,area=AREA_CIRCLE_1,emoji='<:vibrSon:1047197915355037716>',effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_3,vibrSonEff],cooldown=7,description="Inflige des dégâts aux ennemis ciblés et augmente votre Force et votre Magie ainsi que celles de vos équipiers alentours")
vibrSonEff.description += "\n\nNon cumulable avec l'effet octroyé par {0} {1}".format(vanderManuet.emoji,vanderManuet.name)
vanderManuetEff.description+= "\n\nNon cumulable avec l'effet octroyé par {0} {1}".format(vibrSon.emoji,vibrSon.name)

sernSkills = [stigmate,dissonance,vibrSon,requiem]
sernSkillsId = []
for skilly in sernSkills:
    sernSkillsId.append(skilly.id)

sernJauge = effect("Jauge de Sérénade","sernJauge",emoji='<:serenade:1047386802517971014>',turnInit=-1,unclearable=True)
sernJauge.jaugeValue = jaugeValue(
    emoji=[["<:musEL:1047184888052330496>","<:musEM:1047184918339387422>","<:musER:1047184944172105800>"],["<:musBL:1047185274364497971>","<:musBM:1047185299098304605>","<:musBR:1047185332434645052>"]],
    conds=[jaugeConds(INC_START_TURN,10),jaugeConds(INC_USE_SKILL,10,sernSkills)]
)
sernEff1 = effect("Sérénade du Courage","sernEff1",CHARISMA,magie=12,strength=7,precision=5,charisma=5,description="Augmente plusieurs de vos statistiques en fonction de votre charisme\nLa puissance de ce bonus reste la même qu'importe la quantité de {0} {1} consommée".format(sernJauge.emoji[0][0],sernJauge.name),emoji='<:sern:1047213807690334289>',turnInit=4)
sernEff2 = effect("Sérénade de la Détermination","sernEff2",CHARISMA,strength=15,magie=15,precision=10,intelligence=10,endurance=5,charisma=5,description="Augmente plusieurs statistiques du porteur en fonction du charisme du lanceur\nLa puissance de l'effet dépend de la quantité de {0} {1} consommée. Les statisitques affichés ici sont ceux de l'effet à sa puissance maximale".format(sernJauge.emoji[0][0],sernJauge.name),emoji='<:orchestralFantasy:1047213865387171931>',turnInit=3)
sernade = skill("Sérénade du Courage",getAutoId(vibrSon.id,True),TYPE_BOOST,750,range=AREA_MONO,area=AREA_DONUT_5,minJaugeValue=50,maxJaugeValue=100,effects=sernEff2,effectOnSelf=sernEff1,ultimate=True,cooldown=3,emoji='<:serenade:1047386802517971014>',description="Augmente grandement les statistiques de vos alliés alentours en fonction de votre {0} {1}, ainsi que vos propres statistiques indépendament de la dites jauge".format(sernJauge.emoji[0][0],sernJauge.name),jaugeEff=sernJauge,use=MAGIE)
thunderFiole = skill("Fiole de Foudre",getAutoId(sernade.id,True),TYPE_DAMAGE,500,cooldown=5,power=70,effectAroundCaster=[TYPE_DAMAGE,AREA_RANDOMENNEMI_3,35],setAoEDamage=True,use=MAGIE,emoji='<:thunderFiole:1049717778397020173>',description="Inflige des dégâts à l'ennemi ciblé puis de nouveaux dégâts à trois ennemis aléatoires")
deterStrike = skill("Frappe Déterminée",getAutoId(thunderFiole.id,True),TYPE_DAMAGE,500,power=85,range=AREA_CIRCLE_2,emoji='<:deterStrike:1049709129591173240>',maxPower=250,cooldown=5,lifeSteal=35,percing=25,condition=[EXCLUSIVE,ASPIRATION,TETE_BRULE],description="Consomme vos PAr pour délivrer une attaque à cible unique qui vous soigne d'une partie des dégâts infligés.\nLa puissance de cette compétence augmente par rapport au pourcentage de PAr par rapport à vos PVmax consommés\nJusqu'à l'équivalent de 100% de vos PVmax peuvent être consommés")
umbraMortis = skill("Umbra Mortis",getAutoId(deterStrike.id,True),TYPE_DAMAGE,500,deathShadow.power,cooldown=deathShadow.cooldown,emoji='<:morsDamnationem:1050066734243123282>',effects=deathShadow.effects,use=MAGIE,description="Augmente les dégâts que vous infligez à l'ennemi ciblé puis lui délivre une attaque.\nSi la cible meurt dans les tours qui suivent, vous régénérez une partie de vos PV",effBeforePow=True)
morsDamnationemExitiumReady = effect("Mors Damnationem Préparé","clemBloodDmonFinal",turnInit=4,silent=True,emoji='<:sanguisDaemonium:1050059965630533714>')
morsDamnationem = skill("Mors Damnationem",getAutoId(umbraMortis.id,True),TYPE_DAMAGE,power=150,area=AREA_CIRCLE_1,emoji='<:sanguisDaemonium:1050059965630533714>',needEffect=morsDamnationemExitiumReady,use=MAGIE,hpCost=10,group=SKILL_GROUP_DEMON)
sanguisCrucisReady = effect("Sanguis Crucis Préparé","sanguisCrucisReady",silent=True,turnInit=4,emoji='<:sangDae1:1050414458029228142>')
sanguisCrucis = skill("Sanguis Crucis",morsDamnationem.id,TYPE_DAMAGE,power=110,area=AREA_INLINE_3,emoji='<:sangDae1:1050414458029228142>',needEffect=sanguisCrucisReady,use=MAGIE,hpCost=10,group=SKILL_GROUP_DEMON)
sanguinumVerriteReady = effect("Sanguinum Verrite Préparé","sanguinumVerriteReady",silent=True,turnInit=4,emoji='<:sangDae2:1050414522541813812>')
sanguinumVerrite = skill("Sanguinum Verrite",morsDamnationem.id,TYPE_DAMAGE,power=125,area=AREA_ARC_2,emoji='<:sangDae2:1050414522541813812>',needEffect=sanguinumVerriteReady,use=MAGIE,hpCost=10,group=SKILL_GROUP_DEMON)
bloodDemonnt = effect("Epuissement Sanguin","bloodDmnn't",silent=True,turnInit=7,type=TYPE_MALUS)
bloodDemonEff = copy.deepcopy(linceuilLemure.effects[0])
cruentumOffendasEff = effect("Cruentum Offendas","cruentumOffendasEff",MAGIE,power=30,lvl=5,turnInit=3,emoji="<:cruentumOffendas:1053666959377567794>",description="Lorsque le porteur effectue une attaque, inflige des dégâts supplémentaires à la cible principale si cette dernière est un ennemi")
bloodDemon = skill("Sanguis Daemonium",morsDamnationem.id,TYPE_BOOST,effects=[bloodDemonEff,cruentumOffendasEff,sanguinumVerriteReady,sanguisCrucisReady,morsDamnationemExitiumReady],emoji=morsDamnationemExitiumReady.emoji[0][0],description="Augmente grandement vos dégâts infligés pendant vos trois prochain tour et vous donne accès à de puissantes compétences durant cette période en consommant une grande partie de votre Jauge de Sang\nCette compétence devient inutilisable durant sept tour après utilisation.\nChaque compétence vous retire 10% de vos PV actuels",jaugeEff=bloodJauge,minJaugeValue=100,maxJaugeValue=100,rejectEffect=[bloodDemonnt],hpCost=10,group=SKILL_GROUP_DEMON)
bloodDemonBundle = skill("Démon de Sang",morsDamnationem.id,TYPE_DAMAGE,750,become=[bloodDemon,sanguinumVerrite,sanguisCrucis,morsDamnationem],emoji=bloodDemon.emoji,description=bloodDemon.description,jaugeEff=bloodDemon.jaugeEff,minJaugeValue=bloodDemon.minJaugeValue,group=SKILL_GROUP_DEMON)
phenixDanceEff = copy.deepcopy(phoenixFlight)
phenixDanceEff.stat = STRENGTH
phenixDanceEff.description += "\nNon cumulable avec l'effet octroyé par {0} {1}".format(galvanisation.emoji,galvanisation.name)
phenixDance = skill("Danse du Phénix",getAutoId(bloodDemonBundle.id,True),TYPE_DAMAGE,500,110,AREA_CIRCLE_2,cooldown=galvanisation.cooldown,emoji='<:phenixDance:1065647282046898176>',effectAroundCaster=[TYPE_INDIRECT_HEAL,galvanisation.effectAroundCaster[1],phenixDanceEff],description="Inflige des dégâts à la cible et octroi un effet de rénégération à vous-même et vos alliés proches")
phoenixFlight.description += "\nNon cumulable avec l'effet octroyé par {0} {1}".format(phenixDance.emoji,phenixDance.name)
phalaxEff = copy.deepcopy(defenseUp)
phalaxEff.stat, phalaxEff.power = INTELLIGENCE, 12
phalax = skill("Phalax",getAutoId(phenixDance.id,True),TYPE_BOOST,750,effects=phalaxEff,range=AREA_MONO,area=AREA_DONUT_3,cooldown=7,emoji='<:phalax:1051958917393035375>',condition=[EXCLUSIVE,ASPIRATION,MASCOTTE],effectOnSelf=invincibleEff,description="Réduit grandement les dégâts reçus par vos alliés alentours et vous rend invulnérable durant un tour",ultimate=True)
tacShieldEff = effect("Bouclier Tactique","tacShield",INTELLIGENCE,resistance=7,aggro=25,block=30,emoji='<:tacticShield:1051958651801325568>',turnInit=3,description="Augmente votre résistance, la probabilité d'être ciblé par vos ennemis et celle de bloquer leurs attaques")
tacShiledEff2 = effect("Protection Tactique","protectTack",aggro=-20,description="Réduit la probabilité du porteur d'être ciblé par ses ennemis",turnInit=tacShieldEff.turnInit)
tacShield = skill("Bouclier Tactique",getAutoId(phalax.id,True),TYPE_BOOST,500,effects=tacShieldEff,range=AREA_MONO,effectAroundCaster=[TYPE_BOOST,AREA_DONUT_3,tacShiledEff2],emoji=tacShieldEff.emoji[0][0],cooldown=7,description="Augmente votre résistance, votre taux de blocage et attire plus facilement les attaque sur vous tout en réduisant les chances de vos alliés d'être ciblés par vos ennemis",condition=[EXCLUSIVE,ASPIRATION,MASCOTTE])
dislocationEff = copy.deepcopy(vulne)
dislocationEff.power = 10
dislocation = skill("Dislocation",getAutoId(tacShield.id,True),TYPE_DAMAGE,500,95,area=AREA_CIRCLE_1,emoji='<:dislocation:1052697663402950667>',cooldown=5,condition=[EXCLUSIVE,ASPIRATION,MAGE],description="Augmente les dégâts subis par la cible durant un touret lui inflige des dégâts, à lui et aux ennemis alentours",effBeforePow=True,effects=dislocationEff,use=MAGIE)
rubyBraser = skill("Brasier Rubis",getAutoId(dislocation.id,True),TYPE_DAMAGE,power=135,area=AREA_CIRCLE_2,emoji='<:rubyBrasero:1052698751715778631>',cooldown=6,use=MAGIE,description="Inflige des dégâts aux ennemis ciblés, puis au tour suivant effectue une attaque avec une puissance et un air d'effet augmentés",condition=[EXCLUSIVE,ASPIRATION,MAGE])
rubyBraser_c = effect("Cast - {replicaName}","castRubyBraser",turnInit=2,replique=rubyBraser)
rubyLight = skill("Lueur Rubis",rubyBraser.id,TYPE_DAMAGE,500,100,area=AREA_CIRCLE_1,description=rubyBraser.description,use=MAGIE,cooldown=rubyBraser.cooldown+1,emoji='<:rubyLight:1052698664650416158>',effectOnSelf=rubyBraser_c)
anticipationEff1, anticipationEff2 = copy.deepcopy(defenseUp), effect("Anticipation","anticipEff2",emoji='<:anticipation:1052700207407710278>',description="Jusqu'à votre prochain tour, si vous êtes touché par une compétence élementaire, vous octroi l'effet élémentaire correspondant à votre élément et remplie votre Jauge de 5 points, qu'importe la jauge",callOnTrigger=elemEff,trigger=TRIGGER_AFTER_DAMAGE)
anticipationEff1.power, anticipationEff1.stat = 8.5, MAGIE
anticipation = skill("Anticipation",getAutoId(rubyLight.id,True),TYPE_BOOST,500,range=AREA_MONO,useActionStats=ACT_DIRECT,effects=[anticipationEff1,anticipationEff2],emoji=anticipationEff2.emoji[0][0],condition=[EXCLUSIVE,ASPIRATION,MAGE],description="Jusqu'à votre prochain tour, réduit les dégâts que vous subissez. De plus, si vous êtes touché par une compétence élémentaire, vous octroi l'effet élémentaire correspondant à votre élément et remplie de 5 points la valeur de votre jauge équipée",cooldown=5)
redrum = skill("Redrum",getAutoId(anticipation.id,True),TYPE_DAMAGE,500,power=125,range=AREA_CIRCLE_1,cooldown=7,emoji='<:redrum:1053222163819286618>',damageOnArmor=1.5,effects=incur[4],description="Inflige des dégâts (augmentés de 50% sur des armures) à l'ennemi ciblé et réduit de 40% les soins qu'elle reçoit durant un tour")
interEff1, interEff2 = copy.deepcopy(heartStoneSecEff), copy.deepcopy(heartStoneSecEff2)
interEff1.stat = interEff2.stat = CHARISMA
intervantion = skill("Intervention",getAutoId(redrum.id,True),TYPE_INDIRECT_HEAL,heartStone.price,cooldown=heartStone.cooldown,effects=[holyShieltronEff2,interEff1,interEff2],condition=[EXCLUSIVE,ASPIRATION,VIGILANT],emoji='<:inter:1053655537604120586>',replay=True,description="Octroi à l'allié ciblé un effet de régénération et réduit ses dégâts subis dourant trois tour tout en vous permettant de rejouer votre tour. L'effet de réduction de dégâts est doublé durant le premier tour",range=AREA_DONUT_5)
intuitionFougEff1, intuitionFougEff2, intuitionFougEff3 = copy.deepcopy(vampirismeEff), effect("Digue au sang","bloodBarr",STRENGTH,overhealth=35,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji='<:digueAuSang:1053659293875978280>',turnInit=3), copy.deepcopy(interEff2)
intuitionFougEff1.power, intuitionFougEff1.stat, intuitionFougEff1.turnInit = 10, STRENGTH, 3
intuitionFougEff3.stat = STRENGTH
intuitionFoug = skill("Intuition Fougueuse",getAutoId(intervantion.id,True),TYPE_INDIRECT_HEAL,750,range=AREA_MONO,effects=[intuitionFougEff1,intuitionFougEff2,intuitionFougEff3],cooldown=heartStone.cooldown,emoji='<:barageSang:1053655508894109796>',condition=[EXCLUSIVE,ASPIRATION,BERSERK],description="Vous octroi un taux de vol de vie et une petite armure durant 3 tours et vous permet de rejouer votre tour. Réduit également les dégâts que vous subissez jusqu'à votre prochain tour",replay=True)
dreamInADream = skill("Rêve dans un rêve",getAutoId(intuitionFoug.id,True),TYPE_DAMAGE,500,power=20,repetition=3,cooldown=5,emoji='<:dreamWithinADream:1053655563193561138>',condition=[EXCLUSIVE,ASPIRATION,POIDS_PLUME],description="Inflige à trois reprises des dégâts à l'ennemi ciblé et vous permet de rejouer votre tour")
bunshinEff = effect("Bunshin","bunshinEff",STRENGTH,power=30,lvl=5,turnInit=3,emoji="<:Bunshi:1053655586161565726>",description="Lorsque le porteur effectue une attaque, inflige des dégâts supplémentaires à la cible principale si cette dernière est un ennemi")
bunshin = skill("Bunshin",getAutoId(dreamInADream.id,True),TYPE_BOOST,500,range=AREA_MONO,replay=True,effects=bunshinEff,condition=[EXCLUSIVE,ASPIRATION,POIDS_PLUME],cooldown=5,emoji=bunshinEff.emoji[0][0],description="Lors de vos **{0}** prochaines attaques, vous infligerez des dégâts indirects supplémentaires".format(bunshinEff.lvl))
regenEarthEff = effect("Coeur Régénérant","regenEarthEff",CHARISMA,power=50,stackable=True,lvl=3,turnInit=3,emoji='<:regenHeart:1053223398697865227>',trigger=TRIGGER_AFTER_DAMAGE,type=TYPE_INDIRECT_HEAL,description="Soigne le porteur lorsqu'il reçoit des dégâts directs")
astraRegenPhaseEff2 = copy.deepcopy(dissi2Eff)
astraRegenPhaseEff2.name, astraRegenPhaseEff2.emoji, astraRegenPhaseEff2.translucide, astraRegenPhaseEff2.description = "Dissimulation Déphasée", uniqueEmoji("<:timeDissimulation:1053326688450256926>"), False, "Réduit votre probabilité d'être pris pour cible par vos ennemis"
astraRegenPhase = skill("Phase Régénératrice",getAutoId(bunshin.id,True),TYPE_INDIRECT_HEAL,750,cooldown=5,effects=regenEarthEff,range=AREA_MONO,area=AREA_DONUT_3,effPowerPurcent=50,effectOnSelf=astraRegenPhaseEff2,emoji='<:healingPhase:1047986775387291830>',description="Octroi un effet régénérant aux alliés alentours, les soignants lorsqu'ils prennent des attaques, et réduit votre probabilité d'être ciblés par vos ennemis",condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME])
astraIncurStrike = skill("Frappe Temporelle",getAutoId(astraRegenPhase.id,True),TYPE_DAMAGE,500,power=85,range=AREA_CIRCLE_3,tpCac=True,effects=incur[3],effectOnSelf=regenEarthEff,emoji='<:incurStrike:1049717644003131412>',cooldown=5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],selfEffPurcent=85,use=CHARISMA,useActionStats=ACT_HEAL,description="Vous téléporte au corps à corps de l'ennemi ciblé, lui inflige des dégâts, réduit les soins qu'il reçoit de 30% pendant un tour et vous octroi un effet régénérant vous soignant lorsque vous prenez des dégâts directs")
astraRegenEarthEff = copy.deepcopy(regenEarthEff)
astraRegenEarthEff.lvl = 5
astraRegenEarth = skill("Coeur de Compassion",getAutoId(astraIncurStrike.id,True),TYPE_INDIRECT_HEAL,500,effects=regenEarthEff,effectOnSelf=astraRegenEarthEff,effPowerPurcent=75,selfEffPurcent=100,area=AREA_DONUT_3,range=AREA_MONO,emoji='<:timeHeart:1047986742571044895>',cooldown=7,condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],description="Vous octroi à vous et vos alliés proches un effet régénérant vous soignant lorsque vous subissez des dégâts directs. L'effet sur vous-même est plus puissant et peut se déclancher plus de fois")
florChaotEff = effect("Floraison Chaotique","florChaosEff",STRENGTH,power=25,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji='<:florChao:1053721494099873802>',description="Inflige des dégâts au début du tour du porteur")
florChaot = skill("Floraison Chaotique",getAutoId(astraRegenEarth.id,True),TYPE_DAMAGE,500,85,knockback=3,range=AREA_CIRCLE_2,effects=florChaotEff,cooldown=7,emoji='<:florChaos:1053655611516133397>',description="Inflige des dégâts à l'ennemi ciblé ainsi qu'un effet de dégâts sur la durée et le repousse de 3 cases",condition=[EXCLUSIVE,ASPIRATION,POIDS_PLUME])

inercieJauge = effect("Jauge d'Inercie","inercyJauge",turnInit=-1, unclearable=True, emoji='<:inercie:1058338643707695155>', 
    jaugeValue= jaugeValue(
        emoji = [["<:inLE:1058337002472345610>","<:inME:1058337036362321972>","<:inRE:1058337067962220635>"],["<:inLF:1058337108307230751>","<:inMF:1058337140515295252>","<:inRF:1058337174417854485>"]],
        conds = [
            jaugeConds(INC_START_TURN,2),
            jaugeConds(INC_JUMP_PER_CASE,5),
            jaugeConds(INC_PER_PUSH,5),
            jaugeConds(INC_JUMP_BACK,5),
            jaugeConds(INC_COLISION,5)
        ]
    ))

tripleChoc_2 = skill('Triple Choc',getAutoId(florChaot.id,True)+"_2",TYPE_DAMAGE,750,80,sussess=180,cooldown=7,ultimate=True,tpCac=True,range=AREA_CIRCLE_3,area=AREA_CIRCLE_2,maxPower=135,minJaugeValue=1,maxJaugeValue=25,emoji='<:chainChoc3:1058339138383908925>',jumpBack=2,description="Inflige à trois reprises des dégâts à l\'ennemi ciblé. Le dernier coup inflige des dégâts de zone\nLa première et troisième attaque vous rapprochent de l'adversaire\nLa seconde le repousse de deux cases\nLa troisème vous fait reculer de deux cases\n\nSeul 25 points de votre {0} {1} sont nessaires pour utliser cette compétence, mais elle atteint sa puissance maximale avec 100 points".format(inercieJauge.emoji[0][0],inercieJauge.name),jaugeEff=inercieJauge)
tripleChoc_2_c = effect("Enchaînement - Triple Choc","tripleChoc_c2",silent=True,replique=tripleChoc_2)
tripleChoc_1 = copy.deepcopy(tripleChoc_2)
tripleChoc_1.id, tripleChoc_1.power, tripleChoc_1.area, tripleChoc_1.knockback, tripleChoc_1.jumpBack, tripleChoc_1.maxPower, tripleChoc_1.replay, tripleChoc_1.effectOnSelf, tripleChoc_1.emoji = tripleChoc_2.id.replace('_2','_1'),50,AREA_MONO,2,0,100, True, tripleChoc_2_c, "<:chainChoc2:1058339104900796468>"
tripleChoc_1_c = effect("Enchaînement - Triple Choc","tripleChoc_c1",silent=True,replique=tripleChoc_1)
tripleChoc = copy.deepcopy(tripleChoc_2)
tripleChoc.id, tripleChoc.power, tripleChoc.area, tripleChoc.jumpBack, tripleChoc.maxPower, tripleChoc.replay, tripleChoc.effectOnSelf, tripleChoc.emoji, tripleChoc.minJaugeValue, tripleChoc.maxJaugeValue = tripleChoc_2.id.replace("_2",""), 60, AREA_ARC_1, 0, 100, True, tripleChoc_1_c, "<:chainChoc1:1058339074563379240>", 25, 50

corruptusArea = skill("Déployable - Zone Corrompue",getAutoId(tripleChoc.id,True),TYPE_DEPL,750,depl=corruptusAreaDepl,emoji="<:fa:1014081850257444874>",cooldown=7,group=SKILL_GROUP_DEMON,hpCost=15,description="Pose une zone au sol qui augmente les dégâts subis par les ennemis à l'intérieur et réduits les soins qu'ils reçoivent",use=INTELLIGENCE)
bastionEff = effect("Bastion","bastionEff",redirection=25,emoji='<:bastion:1063117878095790170>')
bastion = skill("Bastion",getAutoId(corruptusArea.id,True),TYPE_BOOST,350,effects=bastionEff,emoji='<:bastion:1063117878095790170>',replay=True,cooldown=5,range=AREA_DONUT_4,description="Redirige **{0}%** des dégâts reçus par l'allié ciblé jusqu'au début de votre prochain tour et vous permet de rejouer votre tour".format(bastionEff.redirection))
orage = skill("Orage",getAutoId(bastion.id,True),TYPE_DAMAGE,500,power=50,use=MAGIE,effectAroundCaster=[TYPE_DAMAGE,AREA_DONUT_1,85],emoji='<:orage:1063117783929470996>',cooldown=5,pull=3,area=AREA_INLINE_3,description="Attire l'ennemi ciblé sur soi en lui infligeant des dégâts, puis inflige de nouveaux dégâts à tous vos ennemis à votre corps à corps")
magmaEff = copy.deepcopy(defenseUp)
magmaEff.power = 15
magma = skill("Magma",getAutoId(orage.id,True),TYPE_DAMAGE,500,power=75,area=AREA_INLINE_3,range=AREA_MONO,pull=3,emoji='<:magma:1063117817848791050>',effectOnSelf=magmaEff,cooldown=5,description="Attire les ennemis autour de vous en leur infligeant des dégâts, tout en réduisant les dégâts que vous subirrez jusqu'à votre prochain tour")
soulScealEff = effect("Sceau d'Âme","soulSceal",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,stackable=True,power=20,emoji='<:soulSeals:1023610978107146240>',turnInit=8,description="Inflige des dégâts continues à la fin du tour du porteur. La puissance de cet effet augmente de **{0}%** après chaque déclanchement.\nSi la cible est vaincu, l'effet est transmis aux ennemis alentours pour la durée restante mais avec une puissance rénitialisée".format(15),iaPow=20*(1.15**8 - 1.15) * 5)
soulSceal = skill("Sceau d'Âme",getAutoId(magma.id,True),TYPE_INDIRECT_DAMAGE,750,effects=soulScealEff,emoji='<:soulSceal:1064141053927628881>',cooldown=7,condition=[EXCLUSIVE,ASPIRATION,SORCELER],description="Inflige des dégâts continus à l'ennemi ciblé. La puissance des dégâts augmentent au fil du temps")
soulTwinEff = effect("Âme Jumelle","twinSoul",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,power=int(soulScealEff.power*1.25),emoji='<:soulTwin:1064141076581077095>')
soulTwin = skill("Âme Jumelle",getAutoId(soulSceal.id,True),TYPE_DAMAGE,500,use=MAGIE,useActionStats=ACT_INDIRECT,emoji='<:soulTwin:1064141076581077095>',effects=soulTwinEff,cooldown=5,condition=[EXCLUSIVE,ASPIRATION,SORCELER],power=90,description="Inflige des dégâts à l'ennemi ciblé. Si celui-ci subis un effet {0} __{1}__ infligé par vous-même, inflige des dégâts indirects supplémentaires équivalents à **{2}%** de la puissance actuelle du dit effet".format(soulScealEff.emoji[0][0],soulScealEff.name,round((soulTwinEff.power/soulScealEff.power)*100)))
soulWaveEff = effect("Vague à l'Âme","soulSceal2",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,stackable=True,power=soulScealEff.power,emoji='<:soulWaveEff:1064164761320816680>',turnInit=8,description="Inflige des dégâts continues à la fin du tour du porteur. La puissance de cet effet augmente de **{0}%** après chaque déclanchement".format(15),iaPow=int(soulScealEff.power*0.5)*(1.15**8 - 1.15) * 5)
soulWave = skill("Vague à l'Âme",getAutoId(soulTwin.id,True),TYPE_DAMAGE,500,use=MAGIE,useActionStats=ACT_INDIRECT,effects=soulWaveEff,power=110,cooldown=7,emoji='<:soulWave:1064141030737322044>',description="Inflige des dégâts à l'ennemi ciblé. Si celui-ci subis un effet {0} __{1}__ infligé par vous-même, inflige {2} __{3}__ aux ennemis environnants avec **{4}%** de la puissance actuelle du premier effect pour la durée restante du dit effet".format(soulScealEff.emoji[0][0],soulScealEff.name,soulWaveEff.emoji[0][0],soulWaveEff.name,50),condition=[EXCLUSIVE,ASPIRATION,SORCELER],effPowerPurcent=50)
gigaChadEff = effect("Giga Chad","gigaChad",CHARISMA,strength=15,endurance=20,charisma=20,agility=10,precision=10,intelligence=20,magie=15,emoji='<a:gigaChad:1065649083513053275>',effPrio=1.5)
gigaChad = skill("Giga Chad",getAutoId("sfu",True),TYPE_BOOST,750,use=CHARISMA,effects=gigaChadEff,cooldown=7,ultimate=True,emoji=gigaChadEff.emoji[0][0],description="Augmente grandement les statistiques de l'allié ciblé durant un tour",range=AREA_DONUT_5)
megaVentEff = effect("Méga Vent","aero3",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=40,turnInit=3,emoji='<:megaVent:1065673324484628571>',area=AREA_CIRCLE_1)
megaVent = skill("Méga Vent",getAutoId(gigaChad.id,True),TYPE_DAMAGE,500,use=MAGIE,power=50,cooldown=5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],effects=megaVentEff,area=AREA_CIRCLE_1,range=AREA_CIRCLE_3,description="Inflige des dégâts aux ennemis ciblés et inflige un effet de dégâts indirects de zone à la cible principale")
dismantleEff = copy.deepcopy(dmgDown)
dismantleEff.power, dismantleEff.stat = 4, STRENGTH
dismantle = skill("Brise-Arme",getAutoId(megaVent.id,True),TYPE_MALUS,500,effects=dismantleEff,replay=True,emoji='<:dismantle:1065647433322872902>',cooldown=5,description="Réduit les dégâts infligés par la cible et vous permet de rejouer votre tour")
leadShotEff = effect("Balle de Plomb","leadShotEff",STRENGTH,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=15,turnInit=3,emoji='<:leadShot:1065676062874419222>')
leadShot = skill("Tir de Plomb",getAutoId(dismantle.id,True),TYPE_DAMAGE,500,power=35,effects=leadShotEff,replay=True,cooldown=5,description="Inflige des dégâts à l'ennemi ciblé ainsi qu'un effet de dégâts continus et vous permet de rejouer votre tour",emoji='<:bleedingShot:1065647049703428218>')
heatedCleanShotEff = effect("Dégâts critiques augmentés","critDmgButClean",turnInit=4,critDmgUp=15)
heatedCleanShotReady = effect("Tir Net Chauffé préparé","heatedCleanShotReady",turnInit=3,emoji='<:cleanShotCombo3:1065647407020392468>')
heatedCleanShot = skill("Tir Net Chauffé",getAutoId(leadShot.id,True),TYPE_DAMAGE,500,power=110,effectOnSelf=heatedCleanShotEff,cooldown=5,needEffect=heatedCleanShotReady,description="Inflige des dégâts à l'ennemi ciblé et augmente vos dégâts critiques durant un court instant",emoji="<:cleanShotCombo3:1065647407020392468>")
heatedSlugShotReady = effect("Tir de Balle Chauffé préparé","heatedSlugShotReady",turnInit=3,emoji='<:cleanShotCombo2:1065647381208641556>')
heatedSlugShot = skill("Tir de Balle Chauffé",heatedCleanShot.id,TYPE_DAMAGE,500,power=100,effectOnSelf=heatedCleanShotReady,needEffect=heatedSlugShotReady,emoji='<:cleanShotCombo2:1065647381208641556>',description="Inflige des dégâts à l'ennemi ciblé et vous permet d'utiliser {0} {1}".format(heatedCleanShot.emoji,heatedCleanShot.name))
heatedSlitShot = skill("Tir Scyndé Chauffé",heatedCleanShot.id,TYPE_DAMAGE,power=90,effectOnSelf=heatedSlugShotReady,rejectEffect=[heatedSlugShotReady,heatedCleanShotReady],emoji='<:cleanShotCombo1:1065647347113148436>',description="Inflige des dégâts à l'ennemi ciblé et vous permet d'utiliser {0} {1}".format(heatedSlugShot.emoji,heatedSlugShot.name))
comboHeatedCleanShot = skill("Combo - Tir Net Chauffé",heatedCleanShot.id,TYPE_DAMAGE,become=[heatedSlitShot,heatedSlugShot,heatedCleanShot],description="Permet d'utiliser {0} {1}, {2} {3} et {4} {5}, devant être utlisés dans cet ordre. La dernière compétence augmente vos dégâts critiques infligés pendant {6} tours".format(heatedSlitShot.emoji,heatedSlitShot.name,heatedSlugShot.emoji,heatedSlugShot.name,heatedCleanShot.emoji,heatedCleanShot.name,heatedCleanShot.effectOnSelf.turnInit),emoji=heatedCleanShot.emoji)

# Skill
skills: List[skill] = [comboHeatedCleanShot,leadShot,dismantle,megaVent,gigaChad,soulWave,soulTwin,soulSceal,magma,orage,bastion,corruptusArea,tripleChoc,florChaot,astraRegenEarth,astraIncurStrike,astraRegenPhase,bunshin,dreamInADream,intervantion,intuitionFoug,redrum,anticipation,rubyLight,dislocation,tacShield,phalax,phenixDance,bloodDemonBundle,umbraMortis,deterStrike,thunderFiole,sernade,vibrSon,dissonance,stigmate,exploShot,heroicFantasy,mageBalad,martialPean,vanderManuet,manafication,enhardissement,blastArrow,apexArrow,dmonReconstitution,dmonReconstitution2,dmonDmg,dmonCrit,dmonEnd,dmonAgi,piedVolt,elipseTerrestre,clock,hourglass,ebranlement,hearthFrac,freezeArrow2,freezeArrow,exploArrow,immoArrow,spectralFurie,spectralCircle,ghostlyCircle,silvArmor,UmbralTravel,carnage,assasinate,physTraqnard,fairyTraqnard,blodTraqnard,lifeSeed,antConst,constBen,mend,lillyTransform,forestGarde,ultraSignal,expoHeal,intox,epidemic,sacredSoil,inkStrike,trizooka,inkzooka,tacticooler,lacerTrap,lohicaBrouillad,bigBubbler,asile,sonarPaf,convictionVigilante,convicPro,convictTet,convictEncht,megaDark1,megaDark2,megaDark3,gigaDark1,gigaDark2,gigaDark3,megaLight1,megaLight2,megaLight3,gigaLight1,gigaLight2,gigaLight3,miracle,rivCel,toxicon,seraphStrike,
    bundleFetu,soulPendant,corruptBecon,moissoneur,bundleLemure,lowBlow,legStrike,provoke,comboFanCelest,demonLand,demonArmor,demonArmor2,demonConst,
    comboConfiteor,cryoChargeBundle,pyroChargeBundle,drill,anchor,chainsaw,mysticShot,cycloneEcarlate,sillage,cassMont,finalClassique,offrRec,offrRav,lightEstoc,lightTranche,lightShot,lightPulse,accelerant,tripleAttaque,liberation,acidRain,coroRocket,coroMissile,coroShot,quadFleau,charmingPandant,kralamSkill,windDance,barrage,hemoBomb,dmonProtect,raisingPheonix,fairyGarde,sumLightButterfly,fairySlash,plumRem,fairyBomb,bloodBath,erodAoe,divineAbne,astrodyn,cercleCon,aliceFanDanse,plumeCel,plumePers,pousAviaire,demonRegen,demonLink,bloodBath2,altyCover,klikliStrike,gwenyStrike,mve2,krasis,pandaima,graviton,temperance,terachole,aquavoile,misery,tangoEnd,danseStarFall,graviton2,invocAutTour,invocAutFou,invocAutQueen,recall,divineBenediction,divineCircle,divineGuid,uberCharge,petalisation,roseeHeal,floraisonFinale,vampirisme2,krystalisation,regenVigil,fragmentation,machDeFer,lanceTox,trickAttack,aurore2,holyShieltron,kerachole,gigaFoudre,morsTempSkill,combustion,morsCaudiqueSkill,lbRdmCast,lightEarth,darkAmb,solarEruption,firstArmor,refLum,refConc,dephaIncant,cwFocus,propaUlt,cwUlt,sanguisGladio,sanguisGladio2,cardiChoc,equatorial,elemShield,shieldAura,horoscope,ShiUltimate,intaveneuse,decolation,corGraCast,finalFloral,divineSave,redemption,fireElemUse,waterElemUse,airElemUse,earthElemUse,lightElemUse,darkElemUse,spaceElemUse,timeElemUse,bleedingConvert,revelation,maitriseElementaire,magicEffGiver,physEffGiver,fascination,selenomancie,holiomancie,partner,exhibitionnisme,invocTitania,dmonBlood,hollyGround,hollyGround2,burningGround,blueShell,preciChi,ironHealth,windBal,brasier2,earthUlt2,geyser,rouletteSkill,constance,constance2,undead,ironStormBundle,bolide,invincible,holmgang,comboVerBrasier,galvanisation,contreDeSixte,lifeWind,ice2,renf2,entraide,perfectShot,lastRessource,strengthOfDesepearance,nova,deathShadow,comboVerMiracle,comboFaucheCroix,theEndCast,cure2Bundle,assises,debouses,impact,heartStone,erodStrike,genesis,invertion,pneuma,absorbingStrike,absorbingArrow,absorbingStrike2,absorbingArrow2,magiaHeal,aff2,bloodPact,expediant,divination,macroCosmos,tintabule,toMelee,toDistance,autoBombRush,killerWailUltimate,invocSeaker,darkBoomCast,mageSkill,doubleShot,harmShot,benitWater,shareSkill,extraMedica,foullee,lifePulseCast,crimsomLotusCast,abnegation,foyer,sweetHeat,darkSweetHeat,shell,nacreHit,holyShot,demonStrike,purify,benediction,transfert,blackDarkMagic,fisure,seisme,abime,extermination,darkHeal,calestJump,lohicaUltCast,fairyFligth,aliceDance,aurore,crep,quickCast,pepsis,darkShield,rencCel,valse,finalTech,dissi,intelRaise,ultRedirect,clemency,liuSkillSus,liaSkillSus,lioSkillSus,lizSKillSus,neutralMono1,neutralZone1,neutralMono2,neutralZone2,neutralMono3,neutralZone3,reconst,medicamentum,ultMonoArmor,inkRes,inkRes2,booyahBombCast,propag,invocCarbSaphir,invocCarbObsi,supprZone,cosmicPower,requiem,magicRuneStrike,infinitDark,preciseShot,troublon,haimaSkill,physicRune,magicRune,lightBigHealArea,focus,poisonusPuit,bleedingPuit,idoOS,proOS,preOS,geoConCast,kikuRes,memClemCastSkill,roses,krysUlt,chaosArmor,firelame,airlame,waterlame,mudlame,shadowLame,timeLame,lightLame,astralLame,idoOH,proOH,altOH,lightAura2,tripleMissiles,lightHeal2,extraEtingSkill,strengthOfWillCast,sixtineUlt,hinaUlt,julieUlt,invocSeraf,mageUlt,soulagement,bloodyStrike,infraMedica,magAchSkill,flambeSkill,fireCircle,waterCircle,airCircle,earthCircle,fireShot,waterShot,airStrike,earthStrike,space1,space2,space3,spaceSp,time1,time2,time3,timeSp,renisurection,demolish,contrainte,trouble,infirm,croissance,destruction2,infectFiole,bigLaser2,bigMonoLaser2,invocBat2,invocCarbunR,concen,memAlice2,blackHole,blackHole2,renforce,steroide,focal,suppr,revitalisation,onde,eting,stingray,dark1,dark2,dark3,light1,light2,light3,derobade,ferocite,ironWillSkill,royaleGardeSkill,defi,dissimulation,bleedingTrap,convert,vampirisme,heriteEstialba,heriteLesath,flameche,flame,pyro,ecume,courant,torant,brise,storm2,tornado,stone,rock,mont,bleedingArrow,bleedingDague,swordDance,shot,percingArrow,percingLance,highkick,multishot,rocklance,infinitFire,storm,innerdarkness,divineLight,icelance,onstage,kiss,secondSun,oneforall,uppercut,stalactic,linx,bombRobot,isolement,secondWind,blindage,adrenaline,lapSkill,burst,descart,thinkSkill,invocFee,invocCarbT,invocCarbE,splashdown,multiMissiles,monoMissiles,invocBat,poisonus,protect,explosionCast,splatbomb,lightAura,cure,balayette,contrecoup,boom,chaos,unHolly,soupledown,inkarmor,coffeeSkill,theSkill,gpotion,bpotion,zelian,courage,nostalgia,draw25,siropMenthe
] + elemArrowSkill + elemRuneSkill + horoSkills + tablAdvBaseElemSkills + baseSkills

if not(isLenapy):
    skills.append(bestSkill)

importantSkills = [deathShadow.id, umbraMortis.id, soulSceal.id]
useElemEffId = [fireElemUse.id,waterElemUse.id,airElemUse.id,earthElemUse.id,lightElemUse.id,darkElemUse.id,spaceElemUse.id,timeElemUse.id]
finFloOtherSkillsId = [valse.id, finalTech.id,roseeHeal.id,croissance.id]
tablRosesEff,tablRosesSkillsId,tablRosesId = [roseRed,roseDarkBlu,rosePink,roseYellow,roseBlue,roseGreen], [aliceDanceFinal.id,corGraFinal.id,onstage.id,crimsomLotus.id,floraisonFinale.id,petalisation.id,danceFas.id],[roseRed.id,roseDarkBlu.id,rosePink.id,roseYellow.id,roseBlue.id,roseGreen.id]

horoscopeEff = [
    [effect("Bélier","horBélier",turnInit=-1,emoji='<:belier:960319494167867473>',silent=True),[[STRENGTH,2],[ENDURANCE,3]]],
    [effect("Taureau","horTaureau",turnInit=-1,emoji='<:taureau:960319518004092939>',silent=True),[[STRENGTH,3],[ENDURANCE,2]]],
    [effect("Gémeaux","horGémeaux",turnInit=-1,emoji='<:gemeaux:960319543228649523>',silent=True),[[CHARISMA,1],[INTELLIGENCE,2],[MAGIE,2]]],
    [effect("Cancer","horCancer",turnInit=-1,emoji='<:cancer:960319573003997215>',silent=True),[[AGILITY,1],[STRENGTH,2],[MAGIE,2]]],
    [effect("Lion","horLio",turnInit=-1,emoji='<:lion:960319606050914336>',silent=True),[[STRENGTH,5]]],
    [effect("Vierge","horVierge",turnInit=-1,emoji='<:vierge:960319632982540329>',silent=True),[[CHARISMA,5]]],
    [effect("Balance","horBalance",turnInit=-1,emoji='<:balance:960319658823667762>',silent=True),[[INTELLIGENCE,2],[MAGIE,3]]],
    [effect("Scorpion","horScorpion",turnInit=-1,emoji='<:scorpion:960319682861232211>',silent=True),[[STRENGTH,3],[MAGIE,2]]],
    [effect("Sagittaire","horSagittaire",turnInit=-1,emoji='<:sagittaire:960319710380036146>',silent=True),[[MAGIE,5]]],
    [effect("Capricorne","horCapricorne",turnInit=-1,emoji='<:capricorne:960319731343175781>',silent=True),[[MAGIE,3],[ENDURANCE,2]]],
    [effect("Verseau","horVerseau",turnInit=-1,emoji='<:verseau:960319751136108546>',silent=True),[[INTELLIGENCE,3,PRECISION,2]]],
    [effect("Poisson","horPoisson",turnInit=-1,emoji='<:poisson:960319770337628191>',silent=True),[[AGILITY,3],[PRECISION,2]]]
]

hroscopeNickNames = ["Nébulique","Galactique","Cosmique","Spatiale","Stellaire","Macroscopique","Infini"]
tablHoroSkillsId = getArrayAutoId(windDance.id,len(horoSkills),True)
for cmpt in range(len(horoSkills)):
    horoSkills[cmpt].description += "\n\n__Effet supplémentaire avec l'élément {0} Astral :__\nCette compétence est considérée comme une compétence élémentaire.\nSi vous ou un de vos alliés a la compétence {1} __Horoscope__ d'équipé et n'est pas sous l'effet de {2} __{3}__, lui ocrtoi le dit effet et vous octroi {4} __{5}__".format(elemEmojis[ELEMENT_SPACE],horoscope.emoji,horoscopeEff[cmpt][0].emoji[0][0],horoscopeEff[cmpt][0].name,tablElemEff[ELEMENT_SPACE].emoji[0][0],tablElemEff[ELEMENT_SPACE].name)
    horoSkills[cmpt].emoji, horoSkills[cmpt].id = horoscopeEff[cmpt][0].emoji[0][0], tablHoroSkillsId[cmpt]

lb2Mono = skill("Danse de la lame","lb",TYPE_DAMAGE,power=int(transBerserk.power*0.5),setAoEDamage=True,range=transBerserk.range,emoji=trans.emoji,use=HARMONIE,description="Inflige des dégâts harmoniques à l'ennemi ciblé\n__Puissance :__ {power}",sussess=200,url='https://media.discordapp.net/attachments/971787705216274495/988822433471545384/20220621_170114.gif')
lb2Line = skill("Desperados","lb",TYPE_DAMAGE,power=int(transObs.power*0.5),range=transObs.range,area=transObs.area,emoji=trans.emoji,use=HARMONIE,description="Inflige des dégâts harmoniques aux ennemis dans une zone linéaire\n__Puissance :__ {power}",sussess=200,url='https://media.discordapp.net/attachments/971787705216274495/988822431839969280/20220621_170516.gif')
lb2AoE = skill("Conviction de Stella","lb",TYPE_DAMAGE,power=int(transEnch.power*0.5),range=transMage.range,area=AREA_CIRCLE_2,emoji=trans.emoji,use=HARMONIE,description="Inflige des dégâts harmoniques aux ennemis dans la zone d'effet\n__Puissance :__ {power}",sussess=200,url='https://media.discordapp.net/attachments/971787705216274495/988822433014378516/20220621_170240.gif')
lb2Heal = skill("Souffle de Nacialisla","lb",TYPE_HEAL,power=int(transAlt.power*0.5),setAoEDamage=True,range=transAlt.range,area=transAlt.area,emoji=trans.emoji,use=HARMONIE,description="Soigne les alliés dans la zone d'effet en réanimant les alliés proches\n__Puissance :__ {power}",effectAroundCaster=[TYPE_RESURECTION,AREA_CIRCLE_3,int(transAlt.effectAroundCaster[2]*0.65)],url='https://media.discordapp.net/attachments/971787705216274495/988822432288739439/20220621_170410.gif')
lb2ArmorEff = effect("Proctection de Nacialisla",'lb2Armor',HARMONIE,overhealth=int(effTransPre.overhealth*0.5),turnInit=2,emoji=effTransPre.emoji)
lb2Armor = skill("Protection de Nacialisla","lb",TYPE_ARMOR,effects=lb2ArmorEff,area=transPre.area,range=AREA_MONO,emoji=trans.emoji,description="Octroi une armure aux alliés à portée\n__Puissance de l'armure :__ {0}".format(lb2ArmorEff.overhealth),url='https://media.discordapp.net/attachments/971787705216274495/988822434016792596/20220621_165940.gif')
lb1Mono = skill("Ardeur courageuse","lb",TYPE_DAMAGE,power=int(transBerserk.power*0.35),sussess=200,range=transBerserk.range,emoji=trans.emoji,use=HARMONIE,description="Inflige des dégâts harmoniques à l'ennemi ciblé\n__Puissance :__ {power}",url='https://media.discordapp.net/attachments/971787705216274495/988822435098947604/20220621_165401.gif')
lb1Line = skill("Gros calibre","lb",TYPE_DAMAGE,power=int(transObs.power*0.35),sussess=200,range=transObs.range,area=transObs.area,emoji=trans.emoji,use=HARMONIE,description="Inflige des dégâts harmoniques aux ennemis dans une zone linéaire\n__Puissance :__ {power}",url='https://media.discordapp.net/attachments/971787705216274495/988822436982190130/20220621_164657.gif')
lb1AoE = skill("Décharge Stellaire","lb",TYPE_DAMAGE,power=int(transEnch.power*0.35),sussess=200,range=transMage.range,area=AREA_CIRCLE_1,emoji=trans.emoji,use=HARMONIE,description="Inflige des dégâts harmoniques aux ennemis dans la zone d'effet\n__Puissance :__ {power}",url='https://media.discordapp.net/attachments/971787705216274495/988822435753250916/20220621_165155.gif')
lb1Heal = skill("Souffle de la Terre","lb",TYPE_HEAL,power=int(transAlt.power*0.35),range=transAlt.range,area=transAlt.area,emoji=trans.emoji,use=HARMONIE,description="Soigne les alliés dans la zone d'effet\n__Puissance :__ {power}",url="https://media.discordapp.net/attachments/971787705216274495/988822436315279360/20220621_164949.gif")
lb1ArmorEff = effect("Proctection de la Terre",'lb1Armor',HARMONIE,overhealth=int(effTransPre.overhealth*0.35),turnInit=1,emoji=effTransPre.emoji)
lb1Armor = skill("Proctection de la Terre","lb",TYPE_ARMOR,effects=lb1ArmorEff,area=transPre.area,range=AREA_MONO,emoji=trans.emoji,description="Octroi une armure aux alliés à portée\n__Puissance de l'armure :__ {0}".format(lb1ArmorEff.overhealth),url='https://media.discordapp.net/attachments/971787705216274495/988822434662723584/20220621_165803.gif')

lb3Tabl = [transBerserk, transObs, transPoidsPlume, transIdo, transPre, transTetBrule, transMage, transAlt, transEnch, transPro, transAtt, transSorceler, transIno, transAttentif, transMasc, lb2Mono]
for cmpt in range(len(lb3Tabl)-1):
    lb3Tabl[cmpt].name, lb3Tabl[cmpt].description = lbNames[cmpt], lbDesc[cmpt]
    if lb3Tabl[cmpt].type in [TYPE_DAMAGE,TYPE_HEAL]:
        lb3Tabl[cmpt].description += "\n__Puissance :__ {0}".format(lb3Tabl[cmpt].power*lb3Tabl[cmpt].repetition)
    elif lb3Tabl[cmpt].type == TYPE_ARMOR:
        lb3Tabl[cmpt].description += "\n__Puissance de l'armure :__ {0}".format(lb3Tabl[cmpt].effects[0].overhealth)
    elif lb3Tabl[cmpt].type == TYPE_BOOST:
        lb3Tabl[cmpt].description += "\n__Puissance du bonus :__ {0}".format(lb3Tabl[cmpt].effects[0].strength)
    if cmpt < len(limitBeakGif):
        lb3Tabl[cmpt].url = limitBeakGif[cmpt]
altHoroSkillsTabl = []
for skilly in horoSkills:
    tempSkilly = copy.deepcopy(skilly)
    tempSkilly.condition = [0,1,ELEMENT_SPACE]
    altHoroSkillsTabl.append(tempSkilly)

lb2Tabl = [lb2Mono, lb2Line, lb2Mono, lb2Heal, lb2Armor, lb2Mono, lb2AoE, lb2Heal, lb2AoE, lb2Armor, lb2Heal, lb2AoE, lb2Armor, lb2Line, lb2Mono, lb2Heal]
lb1Tabl = [lb1Mono, lb1Line, lb1Mono, lb1Heal, lb1Armor, lb1Mono, lb1AoE, lb1Heal, lb1AoE, lb1Armor, lb1Heal, lb1AoE, lb1Armor, lb1Line, lb1Mono, lb2Heal]

lb1MinTabl = [lb1Mono,lb1Line,lb1AoE,lb1Heal,lb1Armor]
lb2MinTabl = [lb2Mono,lb2Line,lb2AoE,lb2Heal,lb2Armor]
lb4 = skill("Conviction de Silicia","lb",TYPE_DAMAGE,power=int(transBerserk.power*1.5),sussess=200,emoji=trans.emoji,description="Inflige de lourd dégâts à un ennemi ciblé et réanime les alliés vaincus autour de vous\n__Puissance :__ {power}",use=HARMONIE,effectAroundCaster=[TYPE_RESURECTION,AREA_ALL_ALLIES,350],url='https://media.discordapp.net/attachments/989526512288030742/991051124746387506/20220627_204219.gif')

# SkillsCat

skillsCat = list(range(TYPE_DEPL+1))
for cmpt in range(len(skillsCat)):
    skillsCat[cmpt] = list(range(MASCOTTE+ELEMENT_TIME+3))
    for cmpt2 in range(len(skillsCat[cmpt])):
        skillsCat[cmpt][cmpt2] = []

# FindSkill
dictTablSkills, dictSkills = {}, {}

for skilly in skills:
    try:
        dictTablSkills[skilly.id[:2]].append(skilly)
    except KeyError:
        dictTablSkills[skilly.id[:2]] = [skilly]

    if skilly.condition == []:
        skillsCat[skilly.type][0].append(skilly)
    elif skilly.condition[1] == ASPIRATION:
        skillsCat[skilly.type][1+skilly.condition[2]].append(skilly)
    elif skilly.condition[1] == ELEMENT:
        skillsCat[skilly.type][1+skilly.condition[2]+MASCOTTE+1].append(skilly)

    dictSkills[skilly.id] = skilly

def findSkill(skillId) -> skill:
    """Renvoie une compétence Skill, si trouvé"""
    typi = type(skillId)
    if typi == skill:
        return skillId
    elif typi != str or skillId == "0":
        return None
    else:
        if skillId.startswith("\n"):
            skillId = skillId.replace("\n","")

        try:
            return dictSkills[skillId]
        except KeyError:
            for a in skills:
                if a.name.lower() == skillId.lower():
                    return a

# Exclusive Repartition
def exclusiveRepartition():
    """Print the number of skills exclusives to certains aspiration / main element / sec element"""
    tablExclu, ttSkill, ttSkillwConds = [[],[],[],[],[]], 0, 0
    for cmpt in range(len(inspi)):
        tablExclu[0].append([])
    for cmpt in range(len(elemNames)):
        tablExclu[1].append([])
    for cmpt in range(len(elemNames)):
        tablExclu[2].append([])
    for skilly in skills:
        if skilly.condition != []:
            tablExclu[skilly.condition[1]-1][skilly.condition[2]].append(skilly)
            ttSkillwConds +=1
        elif skilly.group == SKILL_GROUP_DEMON:
            tablExclu[3].append(skilly)
            ttSkillwConds +=1
        elif skilly.group == SKILL_GROUP_HOLY:
            tablExclu[4].append(skilly)
            ttSkillwConds +=1
        
        ttSkill += 1

    print("Skills conditions repartition =======================")
    print("Aspirations --------------------------------")
    for cmpt in range(len(tablExclu[0])):
        print("{0} : {1}".format(inspi[cmpt],len(tablExclu[0][cmpt])))
    print("ElemPrinc ----------------------------------")
    for cmpt in range(len(tablExclu[1])):
        print("{0} : {1}".format(elemNames[cmpt],len(tablExclu[1][cmpt])))
    print("ElemSec ------------------------------------")
    print("Groupe -------------------------------------")
    print("Démon : {0}\nDivin : {1}".format(len(tablExclu[3]),len(tablExclu[4])))
    print("Totals -------------------------------------\nNb Comp : {0}\nNb Comp w/ conditions : {1} ({2}%)".format(ttSkill,ttSkillwConds,round(ttSkillwConds/ttSkill*100,2)))

def getSkillsRanges():
    skillMelee, skillDist, skillMixt = [], [], []
    for skilly in skills:
        if skilly.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]:
            if skilly.range in areaMelee:
                skillMelee.append(skilly)
            elif skilly.range in areaDist:
                skillDist.append(skilly)
            elif skilly.range in areaMixte:
                skillMixt.append(skilly)

    print("Compétences mêlées : {0}\nCompétences distances : {1}\nCompétences mixtes : {2}".format(len(skillMelee),len(skillDist),len(skillMixt)))

suppIndDamageEffId = [casseMontEff,bunshinEff,cruentumOffendasEff]
for eff in suppIndDamageEffId:
    copyTabl, eff.description = suppIndDamageEffId[:], eff.description + "\n\nSi cet effet est cumulé avec "
    copyTabl.remove(eff)
    for effName in copyTabl:
        eff.description += "{0} {1}".format(effName.emoji[0][0],effName.name)
        if len(copyTabl) > 1 and effName != copyTabl[-1]:
            eff.description += ", "
    eff.description += " ou lui-même, seul l'effet le plus ancien est déclanché"

for cmpt in range(len(suppIndDamageEffId)):
    suppIndDamageEffId[cmpt] = suppIndDamageEffId[cmpt].id

astraEarthEffList = [regenEarthEff]
for eff in astraEarthEffList:
    copyTabl, eff.description = astraEarthEffList[:], eff.description + "\n\nSi cet effet est cumulé avec "
    copyTabl.remove(eff)
    for effName in copyTabl:
        eff.description += "{0} {1}".format(effName.emoji[0][0],effName.name)
        if len(copyTabl) > 1 and effName != copyTabl[-2]:
            eff.description += ", "
    eff.description += " ou lui-même, seul l'effet le plus ancien est déclanché"

for cmpt in range(len(astraEarthEffList)):
    astraEarthEffList[cmpt] = astraEarthEffList[cmpt].id