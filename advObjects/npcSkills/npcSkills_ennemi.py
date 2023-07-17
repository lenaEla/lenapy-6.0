from advObjects.npcSkills.npcSkillsImports import *

# Octariens spells
octoEm = '<:splatted1:727586364618702898>'
systemImu = effect("Résistance aux dégâts indirects","inkResistanceOcto",HARMONIE,inkResistance=12,description="Réduit les dégâts indirects reçu par le porteur",emoji=uniqueEmoji('<:nanoMedecine:921544107053158420>'),turnInit=2,stackable=True)
zoneOctoInkRes = skill("Nano-Science","octoBaseInkResSkill",TYPE_BOOST,0,range=AREA_MONO,area=AREA_CIRCLE_3,use=HARMONIE,effects=systemImu,cooldown=4,emoji='<:nanoMedecine:921544107053158420>')

octoShieldWeap = weapon("Bouclier Octarien","aaa",0,AREA_CIRCLE_2,power=20,accuracy=100,price=0,endurance=20,strength=-50,effects="lo",emoji=octoEm,ignoreAutoVerif=True)
octoBallWeap = weapon("Balles rebondissantes","aaa",1,AREA_CIRCLE_3,45,30,0,repetition=3,strength=10,agility=10,emoji=octoEm,ignoreAutoVerif=True)
octoSnipeWeap = weapon("Snipeur Octarien","aaa",2,AREA_CIRCLE_7,75,85,0,strength=20,emoji=octoEm,ignoreAutoVerif=True)
octoFly = weapon("Machinerie volante","aaa",RANGE_DIST,AREA_CIRCLE_5,50,75,-20,10,emoji=octoEm,ignoreAutoVerif=True)
octoHeal = weapon("Octo heal","aaa",1,AREA_CIRCLE_3,35,50,0,use=CHARISMA,type=TYPE_HEAL,target=ALLIES,emoji='<:medic:882890887120699444>')
octoDef = weapon('OctoDef',"aaa",1,AREA_CIRCLE_3,10,100,0,effectOnUse="md",use=INTELLIGENCE,target=ALLIES,type=TYPE_HEAL,intelligence=20)
flyfishweap = weapon("Lance-Multi-Missiles","ffweap",2,AREA_CIRCLE_7,1,200,0,effectOnUse="mf",type=TYPE_DAMAGE,strength=30,ignoreAutoVerif=True,emoji='<:tentamissile:884757344397951026>',effPowerPurcent=65)
octoBoumWeap = weapon("noneWeap","aaa",1,AREA_CIRCLE_1,0,0,0,effects="mg") 
ruddinweap = weapon("Carreaux","aaa",RANGE_DIST,AREA_CIRCLE_5,23,70,0,0,0,0,0,0,0,0,repetition=3,emoji='<:chaos:892857755143127090>')
ruddinweap2 = weapon("Carreaux","aaa",RANGE_MELEE,AREA_CIRCLE_3,28,70,0,0,0,0,0,0,0,0,repetition=3,emoji='<:chaos:892857755143127090>')
malusWeaponEff = effect("Embrouillement","aaa",INTELLIGENCE,strength=-5,magie=-5,critical=-2,type=TYPE_MALUS)
malusWeapon = weapon("Magie sombre","aaa",RANGE_DIST,AREA_CIRCLE_5,70,60,0,effectOnUse=malusWeaponEff,use=MAGIE,ignoreAutoVerif=True)
malusSkill1Eff = effect("Malussé","malusé",INTELLIGENCE,-15,magie=-15,resistance=-5,type=TYPE_MALUS)
malusSkill1 = skill("Abrutissement","aaa",TYPE_MALUS,0,area=AREA_CIRCLE_2,effects=malusSkill1Eff,cooldown=5,initCooldown=2)
malusSkill2 = skill("Éclair","aaa",TYPE_DAMAGE,0,75,cooldown=2,accuracy=65,use=MAGIE,emoji='<:darkThunder:912414778356564019>',area=AREA_CIRCLE_2)
malusSkill3Eff = copy.deepcopy(vulne)
malusSkill3Eff.power, malusSkill3Eff.turnInit = 10, 3
malusSkill3 = skill("Brise-Défense","malusSkill3",TYPE_DAMAGE,power=80,area=AREA_CIRCLE_1,effects=malusSkill3Eff,cooldown=5,damageOnArmor=2)
kralamWeap = weapon("Décharge motivante","aaa",RANGE_DIST,AREA_DONUT_4,35,100,0,type=TYPE_HEAL,target=ALLIES,use=CHARISMA)
kralamSkill2 = skill("Électrochoc","kralamSkill2",TYPE_DAMAGE,0,80,area=AREA_CIRCLE_1,use=CHARISMA,cooldown=3,initCooldown=2,emoji='<:electroShoc:912414625679695873>')
kralamSkill3Eff = effect("Aura électrique","kralamSkill3Eff",CHARISMA,power=40,area=AREA_DONUT_2,lvl=3,turnInit=3,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE)
kralamSkill3Eff1 = effect("Aura électrique","kralamSkill3Eff1",CHARISMA,endurance=5,resistance=3,turnInit=kralamSkill3Eff.turnInit)
kralamSkill3 = skill("Aura électrique","kralamSkill3",TYPE_BOOST,effects=[kralamSkill3Eff1,kralamSkill3Eff],cooldown=5,range=AREA_DONUT_5)
temNativTriggered = effect("Promue",'tem',magie=15,turnInit=-1,unclearable=True,emoji='<:colegue:895440308257558529>',stat=PURCENTAGE)
temNativ = effect("College",'tem1',trigger=TRIGGER_ON_REMOVE,turnInit=3,unclearable=True,callOnTrigger=temNativTriggered)
temWeap = weapon("Temmie flakes","aaa",RANGE_DIST,AREA_CIRCLE_5,42,75,0,use=MAGIE,effects=temNativ,emoji='<:temFlakes:919168887222829057>',say=["TEMMIE FLAKES ! An original breakfast !","TEMMIE FLAKES ! It's so good you can't taste it !","TEMMIE FLAKES ! Don't forget to digest it !","TEMMIE FLAKES in your mouth","Whouwhouwhouwhou !"],message="{0} donne des TEMMIE FLAKES à {1}")
temSkill1 = skill("Alergies","aaa",TYPE_DAMAGE,0,85,use=MAGIE,initCooldown=3,emoji='<:temmient:894545999996014663>')
octoMageWeap = weapon("noneWeap","aaa",1,AREA_CIRCLE_1,0,0,0)
chargeShot = skill('Tir chargé',"aaa",TYPE_DAMAGE,0,80,emoji=shot.emoji,cooldown=4,initCooldown=2,damageOnArmor=1.5)
ultraShot = skill("Tir pénétrant","ultraShot",TYPE_DAMAGE,0,35,cooldown=3,damageOnArmor=5,repetition=3,emoji='<:targeted:912415337088159744>',area=AREA_LINE_2)
octobomberWeap = weapon("Lance Bombe Splash","0",RANGE_LONG,AREA_CIRCLE_5,48,int(splatbomb.accuracy*0.9),area=splatbomb.area,emoji=splatbomb.emoji)
tentaWeap = weapon("Double Canons","0",RANGE_MELEE,AREA_CIRCLE_3,42,35,repetition=4,emoji=octoEm)
veterHealSkill1 = skill("Here we go again","octoHealVet1",TYPE_RESURECTION,0,120,cooldown=4,use=CHARISMA)
veterHealSkill2 = skill("Renouvellement","octaHealVet2",TYPE_HEAL,0,100,use=CHARISMA,cooldown=5,initCooldown=2,emoji='<:heal:911735386697519175>')
veterHealSkill3 = skill("I'm a healer but...","octaHealVet3",TYPE_MALUS,0,area=AREA_CIRCLE_1,effects=incur[3],cooldown=5,emoji=incur[3].emoji[0][0])
veterHealSkill4 = skill("Théorie du complot","octaHealVet4",TYPE_DAMAGE,0,100,use=CHARISMA,cooldown=3)
veterHealWeap = copy.deepcopy(octoHeal)
veterHealWeap.negativeHeal, veterHealWeap.power = -20, veterHealWeap.power + 10
antiArmorShot = skill("Tir anti-matériel","antiArmorShot",TYPE_DAMAGE,0,100,ultimate=True,damageOnArmor=666,cooldown=7)
zombieSkillEff = effect("Marcheur des limbes","zombaSkillArmor",ENDURANCE,overhealth=50,turnInit=-3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
zombieSkill = skill("Frappe d'outre-tombe","zombiSkill",TYPE_DAMAGE,0,100,use=ENDURANCE,effectOnSelf=zombieSkillEff,cooldown=5)
zombieSkill2 = skill("Drainage Abyssal","zombieSkill2",TYPE_DAMAGE,power=80,area=AREA_CIRCLE_1,lifeSteal=100,emoji='<:abysalDrain:1042349734934892605>',cooldown=3)
octoInvocWeap = weapon("Cristal d'Invocateur","OctoSummonerWeap",RANGE_LONG,AREA_CIRCLE_5,35,75,0,strength=10,endurance=10,charisma=10,agility=10,precision=10,intelligence=10,magie=10,emoji=octoEm,ignoreAutoVerif=True)

octoBoost1Eff = effect("Expérimentation 1 - Offense","octoBuff1",INTELLIGENCE,strength=10, magie=10,emoji='<:strengthBuff:914904347039629472>')
octoBoost2Eff = effect("Expérimentation 2 - Défense","octoBuff2",INTELLIGENCE,endurance=10, resistance=5, block=20,emoji='<:resisBuff:914904412357537873>')
octoBoost3Eff = effect("Expérimentation 3 - Mouvoir","octoBuff3",INTELLIGENCE,agility=5,precision=5,emoji="<:agiBuff:914904736166199316>")
octoBoost4Eff = effect("Expérimentation 4 - Soutiens","octoBuff4",INTELLIGENCE,charisma=10,intelligence=10,emoji='<:resisBuff:914904412357537873>')

octoBoostSkill1 = skill(octoBoost1Eff.name,"octoBoostSkill1",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effects=octoBoost1Eff,emoji=octoBoost1Eff.emoji[0][0],use=INTELLIGENCE,cooldown=5)
octoBoostSkill2 = skill(octoBoost2Eff.name,"octoBoostSkill2",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effects=octoBoost2Eff,emoji=octoBoost2Eff.emoji[0][0],use=INTELLIGENCE,cooldown=5)
octoBoostSkill3 = skill(octoBoost3Eff.name,"octoBoostSkill3",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effects=octoBoost3Eff,emoji=octoBoost3Eff.emoji[0][0],use=INTELLIGENCE,cooldown=5)
octoBoostSkill4 = skill(octoBoost4Eff.name,"octoBoostSkill4",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effects=octoBoost4Eff,emoji=octoBoost4Eff.emoji[0][0],use=INTELLIGENCE,cooldown=5)

octoBoostWeap = weapon("Fioles d'expérimentations","octoBoostWeap",RANGE_DIST,AREA_CIRCLE_4,35,65,intelligence=25,use=INTELLIGENCE,emoji=octoBallWeap.emoji,ignoreAutoVerif=True)

octaStransEff = effect('Multi-Bras',"ocSt",aggro=35,resistance=10,block=35,counterOnBlock=20,turnInit = -1,unclearable=True,emoji=uniqueEmoji('<:octoStrans:900084603140853760>'))
octaStrans = skill("Multi-Bras","octaStrans",TYPE_PASSIVE,0,effectOnSelf=octaStransEff,emoji='<:multibras:900084714675785759>')

# Kitsunes sist's spells
charmingHalf = copy.deepcopy(charming)
charmingHalf.strength,charmingHalf.magie,charmingHalf.charisma,charmingHalf.intelligence = charmingHalf.strength//2,charmingHalf.magie//2,charmingHalf.charisma//2,charmingHalf.intelligence//2
charmingHalf.name, charmingHalf.id, charmingHalf.emoji = "Atorakushon", "charming4", sameSpeciesEmoji("<:charmMalB:1103342838290329701>","<:charmMalR:1103342859840667710>")
liuWeapEff = effect("Kitsune de la terre","liuWeapEff",emoji='<:earthKitsune:917670882586017792>',stat=CHARISMA,aggro=35,endurance=10,agility=10,block=35,counterOnBlock=20,turnInit=-1,unclearable=True,description="Augmente certaines statistiques de Liu en fonction de son Charisme, ainsi que sa menace, probabilité de bloquer des attaques et de contre-attaquer lors d'un blocage\nDe plus, à chaque attaque subis, inflige l'effet {0} {1} à l'attaquant".format(charming.emoji[0][0],charming.name),callOnTrigger=charming)
liuWeap = weapon("Sable","liuWeap",RANGE_MELEE,AREA_CIRCLE_2,27,50,repetition=3,strength=10,magie=10,charisma=10,effects=liuWeapEff,effectOnUse=charmingHalf,use=ENDURANCE,emoji='<:liuWeap:908859892272611348>')
liaWeapEff = effect("Kitsune des vents","liaWeapEff",CHARISMA,emoji='<:airKitsune:917670912646602823>',aggro=35,agility=10,precision=10,turnInit=-1,unclearable=True,description="Augmente certaines statistiques de Lia en fonction de son Charisme, ainsi que sa probabilité d'esquiver des attaques et d'effectuer une contre-attaque lors d'une esquive\nDe plus, à chaque attaque esquivé, inflige l'effet {0} {1} à l'attaquant".format(charming.emoji[0][0],charming.name),callOnTrigger=charming,dodge=20,counterOnDodge=35)
liaWeap = weapon("Akashi","liaWeap",RANGE_MELEE,AREA_CIRCLE_2,20,80,repetition=5,charisma=10,magie=10,agility=10,effects=liaWeapEff,effectOnUse=charming,use=MAGIE,emoji='<:liaKat:998001500267749448>',ignoreAutoVerif=True,priority=WEAPON_PRIORITY_LOW)
lioWeapEff = effect("Kitsune de l'eau","lioWeapEff",CHARISMA,emoji='<:waterKitsune:917670866626707516>',intelligence=10,magie=10,turnInit=-1,unclearable=True,description="Augmente certaines statistiques de Lio en fonction de son Charisme\nDe plus, à chaque soins réalisés par sur un allié, lui octroi l'effet {0} {1}".format(charming2.emoji[0][0],charming2.name),callOnTrigger=charming2)
lioWeap = weapon("Écume","lioWeap",RANGE_LONG,AREA_CIRCLE_5,50,50,charisma=20,effects=lioWeapEff,use=CHARISMA,emoji='<:lioWeap:908859876812415036>',type=TYPE_HEAL,target=ALLIES)
lioRez = skill("Eau Mystique","lioRez",TYPE_RESURECTION,0,150,AREA_CIRCLE_7,ultimate=True,area=AREA_CIRCLE_2,use=CHARISMA,emoji='<:lioSkill:922328964926697505>',cooldown=3,say="Allez vous autre... C'est pas le moment de stagner...")
lieWeapEff = effect("Kitsune du feu","lieWeapEff",CHARISMA,emoji='<:fireKitsune:917670925904785408>',intelligence=10,magie=10,turnInit=-1,unclearable=True,description="Augmente certaines statistiques de Liz en fonction de son Charisme\nDe plus, à chaque attaque réalisée, inflige l'effet {0} {1} à la cible".format(charming.emoji[0][0],charming.name),callOnTrigger=charming)
lizWeapEffExplo = effect("Braise Explosive","lizWeapEffExplo",MAGIE,power=30,area=AREA_CIRCLE_1,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji='<:enemyFire:1042312985407930428>')
lieWeap = weapon("Braise","lieWeap",RANGE_LONG,AREA_CIRCLE_4,25,95,area=AREA_CONE_2,charisma=10,magie=10,effects=lieWeapEff,use=MAGIE,emoji='<:lizWeap:908859856608460820>',effectOnUse=lizWeapEffExplo,priority=WEAPON_PRIORITY_LOW)
LIESKILLEFFGAIN = 35
lieSkillEff = effect("Combustion","lieSKillEff",MAGIE,power=50,turnInit=3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,stackable=True,emoji=uniqueEmoji('<:lizIndirect:917204753610571776>'))
lieSkill = skill("Flamme intérieur","lizSkill",TYPE_DAMAGE,0,effects=lieSkillEff,cooldown=3,power=115,say="Voyons voir si tu va pouvoir résister longtemps...",use=MAGIE,emoji='<:lizSkill:922328829765242961>',description="Inflige des dégâts continus à l'ennemi ciblé. La puissance des dégâts augmente de **{0}%** après chaques déclanchement".format(LIESKILLEFFGAIN))
liaSkill = skill("Douce caresse","liaSkill",TYPE_DAMAGE,0,power=70,range=AREA_CIRCLE_1,effects=charming,effPowerPurcent=300,knockback=1,cooldown=5,use=MAGIE,say="Roh allez, détent toi un peu !",emoji='<:liaSkill:922291249002709062>')
liuSkillEff = effect("Armure Télurique","liuSkillEff",CHARISMA,overhealth=65,aggro=15,inkResistance=10,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji('<:liuArmor:922292960886915103>'),turnInit=3)
liuSkill = skill("Frappe Télurique","liuSkill",TYPE_DAMAGE,0,power=65,use=ENDURANCE,cooldown=3,effectOnSelf=liuSkillEff,effects=[charming],say="Oh je suis pas encore finie tu va voir !",emoji='<:liuSkill:922328931502280774>')
lioHealZone = skill("Giga Soins Aquatique","lioHealZone",TYPE_HEAL,power=70,area=AREA_CIRCLE_1,cooldown=5,emoji='<:extraHeal:952522927214051348>',use=CHARISMA)
lioLBHot = effect("Aqua-Purfication","lioLBHot",CHARISMA,power=25,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,turnInit=3,emoji='<:water2:1065647727708483654>',stackable=True)
lioLB = skill("Riptide","lioLb",TYPE_DAMAGE,power=150,range=AREA_CIRCLE_5,area=AREA_LINE_3,cooldown=7,ultimate=True,effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_CIRCLE_3,lioLBHot],use=CHARISMA,description="Lio inflige des dégâts aux ennemis ciblés et applique un effet de soins indirects à ses alliés alentours\nLes bonus de soins réalisés sur Lio accroissent également les dégâts infligés par cette compétences", url='https://media.discordapp.net/attachments/971788596401041480/979903178252374086/20220528_021252.gif',emoji='<:purge:979903342136422440>')
liaLB = skill("Danse des Vents","liaLb",use=CHARISMA,types=TYPE_BOOST,range=AREA_MONO,area=AREA_DONUT_3,effects=charming2,effectAroundCaster=[TYPE_BOOST,AREA_DONUT_3,charming],effPowerPurcent=250,cooldown=7,initCooldown=transObs.initCooldown,description="Augmente les statistiques des alliés autour de Lia et diminue celles des ennemis à proximité",url='https://media.discordapp.net/attachments/971788596401041480/979903177593880596/20220528_021716.gif',emoji='<:contredanse:979903303536230430>')
LIAMINDODGE = 25

LIZLBPOWERGAINPERCHARM = 15
lizLB_1 = skill("Flamme Sentimentale","lizLb_2",TYPE_DAMAGE,use=MAGIE,power=150,area=AREA_CIRCLE_3,cooldown=7,effectAroundCaster=[TYPE_BOOST,AREA_DONUT_3,charming2],description="Inflige des dégâts à tous les ennemis en consommant leurs effets {1} __{2}__. Pour chaque effet consummé sur une cible, les dégâts de cette compétence qu'elle reçoit sont augmentés de {0}%\nAugmente également les statistiques des alliés autour de Liz".format(LIZLBPOWERGAINPERCHARM,charming.emoji[0][0],charming.name),url="https://media.discordapp.net/attachments/971788596401041480/979903177111515177/20220528_022438.gif",emoji='<:chocTermique:979903323094261771>',ultimate=True,accuracy=200)
lizLb_c = effect("Cast - {replicaName}","lizLb",turnInit=2,silent=True,replique=lizLB_1)
lizLB = copy.deepcopy(lizLB_1)
lizLB.power, lizLB.effectOnSelf, lizLB.effectAroundCaster, lizLB.url, lizLB.id = 0, lizLb_c, None, None, "LizLb"
lizQuadBoom_1 = skill("Boum Boum Boum Boum","lizBoomx4",TYPE_DAMAGE,use=MAGIE,power=60,area=AREA_CIRCLE_2,repetition=4,damageOnArmor=.65,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],cooldown=7,emoji=fireCircle.emoji,description="Après un tour de chargement, Liz effectue 4 attaques autour de l'ennemi ciblé (dégâts réduits de 35% sur l'armure)")
lizQuadBoom_c = effect("Cast - {replicaName}","lizBoomx4_c",replique=lizQuadBoom_1,turnInit=2,silent=True)
lizQuadBoom = copy.deepcopy(lizQuadBoom_1)
lizQuadBoom.effectOnSelf, lizQuadBoom.power = lizQuadBoom_c, 0

liuLBEff2 = effect("Armure Tectonique","liuLbArmorEff",ENDURANCE,overhealth=75,turnInit=3,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,emoji=liuSkillEff.emoji[0][0])
liuLB = skill("Mur Tectonique","liuLb",TYPE_ARMOR,range=AREA_MONO,area=AREA_ALL_ALLIES,cooldown=7,shareCooldown=True,effects=[liuLBEff2],effectAroundCaster=[TYPE_BOOST,AREA_DONUT_3,charming2],initCooldown=3,emoji=trans.emoji,url="https://cdn.discordapp.com/attachments/912137828614426707/957181011555397642/20220326_083047.gif",description="Liu octroi une armure à ses alliés proche et elle-même")
liuMontBreaker = copy.deepcopy(cassMont)
liuMontBreaker.use = liuMontBreaker.effects[0].stat = ENDURANCE
liuMontBreaker.effects[0].power = round(liuMontBreaker.effects[0].power*0.5)
liuAoEShieldEff = effect("Armure Rocheuse","liu",ENDURANCE,overhealth=50,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=liuSkillEff.emoji)
liuAoEShieldOnHer = copy.deepcopy(defenseUp)
liuAoEShieldOnHer.power = liuAoEShieldOnHer.aggro = 25
liuAoEShieldSkill = skill("Cristalisation","liuAoEShieldSkill",TYPE_ARMOR,emoji='<:enemyStone:1042313085400133632>',effects=liuAoEShieldEff,cooldown=5,area=AREA_DONUT_2,range=AREA_MONO,effectOnSelf=liuAoEShieldOnHer,description="Liu octroi une armure à ses alliés alentours et réduit les dégâts qu'elle subit",use=ENDURANCE)
lizDotAoEEff = effect("Combustion Explosive","lizDotAoE",MAGIE,power=32,area=AREA_CIRCLE_3,turnInit=3,lvl=3,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji='<:enemyFire:1042312985407930428>')
lizDotAoE = skill("Braise Explosive","lizDotAoE",TYPE_DAMAGE,power=80,use=MAGIE,effects=lizDotAoEEff,cooldown=5,emoji='<:enemyFire:1042312985407930428>')

lizAoELauchEff = effect("Déflagration","lizAoePostDamage",MAGIE,power=25,area=AREA_CIRCLE_2,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,emoji="<:majorFire2:1042349795353825320>",turnInit=3)
lizAoELauch = skill("Déflagration","lizAoe",TYPE_DAMAGE,power=165,area=AREA_CIRCLE_2,range=AREA_CIRCLE_5,use=MAGIE,cooldown=5,emoji="<:majorFire2:1042349795353825320>",effects=[lizAoELauchEff],description="Après un tour de chargement inflige de lourd dégâts magiques aux ennemis ciblés et inflige un effet de dégâts périodique de zone à la cible principale")
lizAoeCast = effect("Cast - {replicaName}","lizAoeCast",turnInit=2,silent=True,replique=lizAoELauch)
lizAoE = copy.deepcopy(lizAoELauch)
lizAoE.power, lizAoE.effectOnSelf, lizAoE.effects = 0, lizAoeCast, [None]

liuFurTel = copy.deepcopy(earthUlt2Lanch)
liuFurTelCastEff, liuFurTel.effectOnSelf, liuFurTel.armorConvert, liuFurTel.power = effect("Cast - {replicaName}","liuFurTelCast",turnInit=2,replique=liuFurTel), None, 50, 120
liuFurTelCast = skill("Glissement Tellurique",liuFurTel.id,TYPE_DAMAGE,power=20,effectOnSelf=liuFurTelCastEff,range=AREA_MONO,area=AREA_INLINE_4,emoji=liuFurTel.emoji,cooldown=liuFurTel.cooldown,pull=3,description="Attire sur vous les ennemis alignés puis inflige des dégâts au corps à corps lors du second tour")

lioIndirectHeal_eff = copy.deepcopy(healDoneBonus)
lioIndirectHeal_eff.power, lioIndirectHeal_eff.turnInit = 20, 3
lioIndirectHeal = skill("Aqua-Purification","lioIndirectHeal",TYPE_INDIRECT_HEAL,area=AREA_CIRCLE_4,effects=lioLBHot,range=AREA_MONO,effectAroundCaster=[TYPE_BOOST,AREA_MONO,lioIndirectHeal_eff],cooldown=7,description="Lio octroi un effet de soins indirects aux alliés atour d'elle et augmente ses propres soisn réalisés pendant une petite durée",emoji=lioIndirectHeal_eff.emoji[0][0])

liaPassEff = effect("Aura Charmante","liaPassEff",CHARISMA,turnInit=-1,trigger=TRIGGER_END_OF_TURN,unclearable=True,callOnTrigger=charmingHalf,area=AREA_DONUT_2,description="À la fin de son tour, Lia inflige un effet Atorakushon aux ennemis autour d'elle",emoji='<:liaAura:1105353814518792213>')
liaPassive = skill("Aura Charmante","liaPassive",TYPE_PASSIVE,effectOnSelf=liaPassEff,emoji=liaPassEff.emoji[0][0])

liaSillageDeplSkill = skill("Tatsumaki","liaTornadeSkill",TYPE_DAMAGE,power=10,range=AREA_MONO,area=AREA_CIRCLE_2,use=AGILITY,effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_2,charmingHalf],emoji='<:liaTornadoEff2:1100185833115492402>')
liaSillageDepl = depl("Tatsumaki",liaSillageDeplSkill,["<:liaDepl:1013912739728592896>","<:liaDepl:1013912739728592896>"],["<:tliaDepl:1013912690877550664>","<:tliaDepl:1013912690877550664>"],"Lia invoque une tornade sur la cellule ciblée, infligeant des dégâts avec une puissance de **{0}** et inflige l'effet Atorakushon aux ennemis".format(liaSillageDeplSkill.power))
liaSillageEff = effect("Tatsumaki","liaSillageEff",AGILITY,type=TYPE_DEPL,callOnTrigger=liaSillageDepl,trigger=TRIGGER_INSTANT)
liaSillage = skill("Tatsumaki","liaSillage",TYPE_DAMAGE,use=AGILITY,power=50,accuracy=200,range=AREA_CIRCLE_3,tpCac=True,emoji='<:liaDepl:1013912739728592896>',cooldown=5,description="Lia dash sur l'ennemi ciblé, lui inflige des dégâts et invoque un déployable à ses pieds, infligeant des dégâts de zones et charmant les ennemis à l'intérieur durant 3 tours",effects=liaSillageEff)
liaWindBite = copy.deepcopy(windBal)
liaWindBite.cooldown, liaWindBite.emoji, liaWindBite.effectOnSelf.power = 5, "<:liaSkiUlt1:1013889002731995246>", int(liaWindBite.effectOnSelf.power*0.7) 
liaDashEff = effect("Kaze no shinkiro","liaDashEff",AGILITY,emoji='<:liaSki6:1013891089662488596>',inkResistance=8,turnInit=3)
liaDashEff2 = effect("Arashi no kaze","liaDashEff2",AGILITY,power=25,area=AREA_DONUT_2,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,emoji='<:liaSamLB2:1100185041306386439>')
liaDash = skill("Shapuchajido","liaDash",TYPE_DAMAGE,power=50,use=AGILITY,tpBehind=True,cooldown=5,effects=liaDashEff2,emoji='<:liaCounter:998001563379437568>',effectOnSelf=liaDashEff,url=demolish.url,percing=25,description="Lia se téléporte derrière sa cible, lui inflige des dégâts en ignorant une partie de sa résistance, inflige des dégâts indirects aux ennemis alentours et réduit les dégâts indirects qu'elle reçoit durant un court instant")
liaSkill5 = skill("Sutomubureido","liaSkill5",TYPE_DAMAGE,power=50,use=AGILITY,cooldown=5,range=AREA_MONO,area=AREA_CIRCLE_2,emoji='<:liaSkiUlt0:1013889091831599178>',effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_2,charmingHalf],effPowerPurcent=80,description="Lia inflige des dégâts autour d'elle et charme un peu les ennemis affectés")

liuEarthCircle = copy.deepcopy(justiceEnigma)
liuEarthCircle.effects[0].emoji, liuEarthCircle.emoji = uniqueEmoji('<:earthEnigma:1106676312057319484>'), "<:earthEnigma:1106676738211201167>"
liuEarthCircle.name = liuEarthCircle.effects[0].name = "Cercle de Terre"

# Hunter's spells
hunterWeap = weapon("Logique irréfutable","hunterWeap",RANGE_LONG,AREA_CIRCLE_5,40,accuracy=100,emoji='<:Objection:800829922356232202>',use=INTELLIGENCE,damageOnArmor=1.5,message="{0} utilise sa Logique irréfutable")
hunterSkill1Eff = effect("Cornered","hunterSkill1Eff",INTELLIGENCE,strength=-10,magie=-10,charisma=-10,intelligence=-10,type=TYPE_MALUS,emoji=uniqueEmoji('<a:HunterPoint:800834253889732689>'))
hunterSkill1 = skill("Preuve à l'appui","hunterSkill1",TYPE_MALUS,0,area=AREA_CIRCLE_1,effects=hunterSkill1Eff,cooldown=3,use=INTELLIGENCE,emoji='<a:HunterSmug:800841378967715841>')
hunterSkill2 = skill("Poings sur la table","hunterSkill2",TYPE_DAMAGE,0,120,use=INTELLIGENCE,cooldown=3,emoji='<a:HunterSlam:800834288487759923>')
hunterSkill3Eff = effect("Vérité","hunterSkill3Eff",INTELLIGENCE,strength=10,magie=10,charisma=10,intelligence=10,emoji=uniqueEmoji('<:Eureka:800837165688815636>'))
hunterSkill3 = skill("Vérité entrevue",'hunterSkill3',TYPE_BOOST,0,area=AREA_CIRCLE_1,effects=hunterSkill3Eff,cooldown=3,emoji='<:Eureka:800837165688815636>')
hunterSkill4 = skill("Outdated autopsy report","hunterSkill4",TYPE_RESURECTION,0,150,use=INTELLIGENCE,emoji='<:AutopsyReport:800839396151656469>',cooldown=5,message='{0} a mis à jour le rapport d\'autopsy de {2}',url='https://cdn.discordapp.com/attachments/927195778517184534/934985362462343218/20220124_023739.gif')

# Bob Hi
bobSays = copy.deepcopy(temSays)
bobSays.start = "Hello. I'm Bob"

# Cliroptère skill
clirHeal = skill("Clémence","stopSpamThatPls",TYPE_HEAL,0,70,cooldown=2,use=CHARISMA)
clirWeap = weapon("Bouclier Nocturne","clirWeap",RANGE_MELEE,AREA_CIRCLE_1,74,70,charisma=10,resistance=10,endurance=10,use=CHARISMA)
clirSkill1 = skill("Frappe Nocturne","clirSkill1",TYPE_DAMAGE,power=85,use=CHARISMA,effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_3,70],emoji=requiescat.emoji,cooldown=4)

# Octa PomPom Skills
octoPom1Eff = effect("Chorégraphie 1 - Force","octoBuff1",CHARISMA,strength=10,emoji=uniqueEmoji('<:strengthBuff:914904347039629472>'))
octoPom2Eff = effect("Chorégraphie 2 - Magie","octoBuff2",CHARISMA,magie=10,emoji=uniqueEmoji('<:magicBuff:914904390056415292>'))
octoPom3Eff = effect("Chorégraphie 3 - Résistance","octoBuff3",CHARISMA,resistance=5,emoji=uniqueEmoji('<:resisBuff:914904412357537873>'))
octoPom4Eff = effect("Chorégraphie 4 - Agilité","octoBuff4",CHARISMA,agility=10,emoji=uniqueEmoji('<:agiBuff:914904736166199316>'))

octoPomSkill1 = skill(octoPom1Eff.name,"octoPomSkill1",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effects=octoPom1Eff,emoji=octoPom1Eff.emoji[0][0],use=CHARISMA,cooldown=5)
octoPomSkill2 = skill(octoPom2Eff.name,"octoPomSkill2",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effects=octoPom2Eff,emoji=octoPom2Eff.emoji[0][0],use=CHARISMA,cooldown=5)
octoPomSkill3 = skill(octoPom3Eff.name,"octoPomSkill3",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effects=octoPom3Eff,emoji=octoPom3Eff.emoji[0][0],use=CHARISMA,cooldown=5)
octoPomSkill4 = skill(octoPom4Eff.name,"octoPomSkill4",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effects=octoPom4Eff,emoji=octoPom4Eff.emoji[0][0],use=CHARISMA,cooldown=5)

octaPomWeapon = weapon("PomPom","octaPomPomWeap",RANGE_LONG,AREA_CIRCLE_6,45,50,charisma=20,emoji=octoEm,use=CHARISMA,ignoreAutoVerif=True)

# Cliroptère infirmier
clirInfWeap = weapon("Sono-Thérapie","clirInfWeap",RANGE_LONG,AREA_CIRCLE_4,45,100,charisma=20,type=TYPE_HEAL,target=ALLIES,use=CHARISMA)
clirInfSkill1Eff = copy.deepcopy(healDoneBonus)
clirInfSkill1Eff.power, clirInfSkill1Eff.turnInit = 20, 3
clirInSkill1Eff2 = effect("Récupération","clirInfSkill1Eff",CHARISMA,power=18,turnInit=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,stackable=True)
clirInfSkill1 = skill("Largesse","clirInfSkill1",TYPE_BOOST,effects=clirInfSkill1Eff,range=AREA_MONO,cooldown=5,emoji=healDoneBonus.emoji[0][0],effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_DONUT_3,clirInSkill1Eff2],description="Augmente les soins réalisés par le lanceur et octroi un effet de régénération à ses alliés proches pendant un petit instant")

# OctoSus
octoSusSkill1 = skill("Vent",'octoSusSkill1',TYPE_DAMAGE,0,80,range=AREA_RANDOMENNEMI_1,cooldown=3,emoji='<:Vent:932241554125520957>',tpCac=True)
octoSusSkill2Eff = effect("Saboté",'octoSusSkill2Eff',INTELLIGENCE,type=TYPE_MALUS,strength=-10,magie=-10,charisma=-10,intelligence=-10,emoji='<:Sabotage:932241553865465946>')
octoSusSkill2 = skill('Sabotage','octoSusSkill2',TYPE_MALUS,0,effects=octoSusSkill2Eff,area=AREA_DONUT_1,range=AREA_MONO,emoji='<:Sabotage:932241553865465946>')
octoSusWeap = weapon("Kill",'octoSusWeap',range=RANGE_LONG,effectiveRange=AREA_CIRCLE_1,power=72,accuracy=90,emoji='<:Kill:932241554050023484>')

# Unform Light
unformLightAWeapon = weapon("Lumière destructrice",'informLightAWeap',RANGE_MELEE,AREA_CIRCLE_2,108,60,strength=20,magie=20,emoji='<:light1:1095249264105508874>')
unformLightASkill1 = skill("Corruption",'unformLightASkill1',TYPE_DAMAGE,power=50,range=AREA_CIRCLE_3,effects=vulneTabl[2],cooldown=5,emoji='<:light2:1095249294388383764>')
unformLightASkill2Eff = effect('Annéantissement','unformLightASkill2Eff',MAGIE,type=TYPE_INDIRECT_DAMAGE,power=35,turnInit=5,lvl=5,trigger=TRIGGER_START_OF_TURN,stackable=True,emoji='<:iliDot:1046387034522136609>')
unformLightASkill2 = skill("Anéantissement de l'esprit",'unformLightASkill2',TYPE_INDIRECT_DAMAGE,range=AREA_RANDOMENNEMI_2,area=AREA_CIRCLE_1,effects=unformLightASkill2Eff,cooldown=3,emoji='<:iliDot:1046387034522136609>')
unformLightASkill3Eff = effect('Lueur mauvaise','unformLightASkill3Eff',MAGIE,magie=10,strength=5,turnInit=3,stackable=True)
unformLightASkill3 = skill("Lueur mauvaise",'unformLightASkill3',TYPE_BOOST,range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=5,effects=unformLightASkill3Eff)
unformLightASkill4 = skill("Réflexion Néfaste","unformLihtASkill4",TYPE_DAMAGE,power=100,range=AREA_MONO,area=AREA_CIRCLE_2,pull=1,cooldown=3,use=MAGIE,emoji='<:light3:1095249327376584794>')

# Unform Dark
unformDarknessDot = effect('Anéantissement','unformDarknessMainDoT',MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=20,turnInit=8,lvl=8,stackable=True,emoji='<:lunaDot:1046387641807020092>')
unformDarknessAWeapon = weapon("Noirceur destructrice",'unformDarknessAWeap',RANGE_MELEE,AREA_CIRCLE_2,41,99,strength=20,magie=20,use=MAGIE,effectOnUse=unformDarknessDot,emoji='<:dark1:1095250637790388224>')
unformDarknessASkill1 = skill('Fissure','unformDarkASkill1',TYPE_INDIRECT_DAMAGE,range=AREA_CIRCLE_1,cooldown=5,effects=unformDarknessDot,effPowerPurcent=500,use=MAGIE,emoji='<:lunaDot:1046387641807020092>')
unformDarknessASkill2 = skill('Ombre aveuglante','unformDarknessASkill2',TYPE_DAMAGE,power=100,range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=3,use=MAGIE,emoji='<:dark2:1095250672955437146>')
unformDarknessASkill3Eff = effect('Ténèbres consummants','unformDarknessASkill3Eff',MAGIE,type=TYPE_MALUS,resistance=-5,endurance=-10,turnInit=3)
unformDarknessASkill3 = skill("Ombre mauvaise",'unformDarknessASkill3',TYPE_MALUS,range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=5,effects=unformDarknessASkill3Eff,use=MAGIE,emoji='<:dark3:1095250712029569044>')

# Unform Space
unformSpaceWeap = weapon("Fracture dimentionnelle","unformSpaceWeap",RANGE_DIST,AREA_CIRCLE_4,46,65,area=AREA_CIRCLE_1,magie=15,precision=15,emoji='<:space1:1095252262563102720>',use=MAGIE)
unformSpaceSkill1Eff = effect("Statistiques offensives augmentées","unformSpaceSkill1Eff",MAGIE,strength=5,magie=5,turnInit=5)
unformSpaceSkill1 = skill("Pulsion Dimensionnelle Informe","unformSpaceSkill1",TYPE_BOOST,effects=unformSpaceSkill1Eff,area=AREA_CIRCLE_2,cooldown=5,range=AREA_DIST_5,emoji='<:space2:1095252290744619018>',effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_2,unformSpaceSkill1Eff],description="Augmente les statistiques offensives des alliés ciblés et ceux autour du lanceur")
unformSpacePassiveEff = effect("Supernova Informe","unformSpacePassiveEff",MAGIE,power=150,area=AREA_DONUT_3,turnInit=20,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_DEATH,lvl=1,emoji="<:space3:1095252316959035452>")
unformSpacePassive = skill("Supernova Informe","unformSpacePassive",TYPE_PASSIVE,effectOnSelf=unformSpacePassiveEff,emoji=unformSpacePassiveEff.emoji[0][0],description="Lors de la mort, provoque une puissante explosion pouvant infliger de sérieux dégâts aux ennemis")
unformSpaceSkill2 = skill("Macrocosme Informe","unformSpaceSkill2",TYPE_DAMAGE,power=120,range=AREA_MONO,area=AREA_CIRCLE_4,use=MAGIE,cooldown=5,emoji="<:space2:1095252290744619018>",description="Inflige des dégâts aux ennemis environants")

# Unform Time
unformTimeWeapEff = effect("Armure","unformTimeShield",MAGIE,overhealth=25,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,turnInit=3,stackable=True)
unformTimeWeap = weapon("Temporalité Informe","unformTimeWeap",RANGE_LONG,AREA_CIRCLE_4,unformTimeWeapEff.overhealth,100,magie=30,effectOnUse=unformTimeWeapEff,target=ALLIES,type=TYPE_HEAL,use=MAGIE,emoji='<:time1:1095254189950640148>')
unformTimeSkill1 = skill("Vision Aforme","unformTimeSkill1",TYPE_ARMOR,area=AREA_CIRCLE_2,cooldown=5,effects=unformTimeWeapEff,effPowerPurcent=150,emoji='<:time1:1095254189950640148>',description="Octroi une armure aux alliés ciblés")
unformTimeSkill2Eff1 = effect("Perception Temporelle","unformTimeSkill2Eff1",MAGIE,power=unformTimeWeapEff.overhealth,turnInit=5,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji='<:catTime:956599814898999328>')
unformTimeSkill2Eff2 = effect("Perception Temporelle","unformTimeSkill2Eff2",MAGIE,power=int(unformTimeWeapEff.overhealth*1.25),turnInit=5,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji='<:catTime:956599814898999328>')
unformTimeSkill2 = skill("Horloge Aforme","unformTimeSkill2",TYPE_INDIRECT_HEAL,range=AREA_MONO,area=AREA_CIRCLE_3,effects=unformTimeSkill2Eff1,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_CIRCLE_3,unformTimeSkill2Eff2],cooldown=5,emoji='<:time3:1095254245491605574>',description="Octroi un effet régénérant aux alliés proches et un effet de dégâts indirects aux ennemis dans la zone d'effet")
unformTimeSkill3Eff = effect("Distorsion Temporelle","unformTimeSkill3",MAGIE,power=100,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_ON_REMOVE,area=AREA_CIRCLE_2)
unformTimeSkill3 = skill("Distorsion Temporelle","unformTimeSkill3",TYPE_INDIRECT_DAMAGE,effects=unformTimeSkill3Eff,cooldown=5,emoji='<:time2:1095254219298181260>',description="Inflige à l'ennemi ciblé un effet qui causera des dégâts indirects de zone au porteur et vos ennemis proches a début de votre prochain tour")

octoBooyahBomb = copy.deepcopy(booyahBombLauch)
octoBooyahBomb.power = int(octoBooyahBomb.power*0.6)
octoBooyahBombCastEff = copy.deepcopy(booyahBombEff)
octoBooyahBombCastEff.replica = octoBooyahBomb
octoBooyahBombCast = copy.deepcopy(booyahBombCast)
octoBooyahBombCast.effectOnSelf = octoBooyahBombCastEff

octoTentaMissiles = copy.deepcopy(multiMissiles)
octoTentaMissiles.area = AREA_RANDOMENNEMI_3

lizBoomLaunch = copy.deepcopy(explosion)
lizBoomLaunch.power, lizBoomLaunch.effectOnSelf.turnInit = 200, 2
lizBoomEff = copy.deepcopy(castExplo)
lizBoomEff.replica = lizBoomLaunch
lizBoomCast = copy.deepcopy(explosionCast)
lizBoomCast.effectOnSelf = lizBoomEff

lizDespairFire2Eff = effect('Burasuto',"lizFire4Eff",MAGIE,power=70,area=AREA_DONUT_2,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,emoji="<:pyromaniac:1075074652763856970>")
lizDespairFire2 = skill("Neppa","lizFire4",TYPE_DAMAGE,power=130,use=MAGIE,effects=lizDespairFire2Eff,cooldown=5,description="Liz inflige des dégâts à une cible unique puis une seconde attaque lors du second tour, infligeant en plus des dégâts aux ennemis environants",percing=20,emoji='<:lizExUlt:1075074594748252222>')
lizDespairFire2_c = effect("Cast - Neppa","castNeppa",turnInit=2,emoji='<:lizExUltCast:1075074712146825357>',replique=lizDespairFire2)
lizDespairFire = skill("Giga Feu","lizFire3",TYPE_DAMAGE,use=MAGIE,power=100,range=AREA_CIRCLE_4,emoji='<:fire3:1042349767411376148>',cooldown=5,effectOnSelf=lizDespairFire2_c,percing=20,description=lizDespairFire2.description)

# Octo Gazor
octoGazTox = copy.deepcopy(lanceToxEff)
octoGazTox.power = int(octoGazTox.power * 0.6)
octoGazWeap = weapon("Lance-Toxines","octoGazWeap",RANGE_MELEE,AREA_CIRCLE_2,50,75,strength=5,intelligence=5,endurance=5,emoji=lanceToxEff.emoji[0][0],effectOnUse=octoGazTox,ignoreAutoVerif=True)
octoGazSkill1 = skill("Dispersion","octoGazSkill1",TYPE_INDIRECT_DAMAGE,effects=octoGazTox,range=AREA_CIRCLE_4,area=AREA_CONE_3,emoji=lanceToxEff.emoji[0][0],cooldown=5)
octoGazSkill2 = skill("Projection","octoGazSkill2",TYPE_DAMAGE,power=35,knockback=2,area=AREA_LINE_3,range=AREA_CIRCLE_1,effects=octoGazTox,cooldown=2)
octoGazSkill3 = skill("Propagation","octoGazSkill3",TYPE_INDIRECT_DAMAGE,effects=octoGazTox,emoji=lanceToxEff.emoji[0][0],range=AREA_MONO,area=AREA_CIRCLE_3,effPowerPurcent=65,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_CIRCLE_1,octoGazTox])

# Lime Cookie
limeWeapon = weapon("Ballon de voley","noneWeap",RANGE_DIST,AREA_CIRCLE_4,30,80,strength=10,agility=10,endurance=5,ignoreAutoVerif=True)
limeSkill1 = skill("Attaque lobbée","limeSkill1",TYPE_DAMAGE,power=80,cooldown=3,range=AREA_DIST_5,area=AREA_CIRCLE_1)
limeSkill2 = skill("Smash Hit","limeSkill2",TYPE_DAMAGE,power=100,cooldown=3,effects=lightStun,range=AREA_CIRCLE_4)
limeSkill3Eff = effect("Agilité réduite","agilityDown",CHARISMA,agility=-5,turnInit=3,type=TYPE_MALUS)
limeSkill3 = skill("Spike","limeSkill3",TYPE_DAMAGE,power=100,cooldown=3,range=AREA_CIRCLE_4,tpCac=True,area=AREA_CIRCLE_2,areaOnSelf=True,effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_2,limeSkill3Eff])
limeSkill4 = skill("Push","limeSkill4",TYPE_DAMAGE,power=50,knockback=1,range=AREA_CIRCLE_4)
limeSkill5 = skill("Invocation - Mr. Lifesavor","limeSkill5",TYPE_SUMMON,range=AREA_CIRCLE_4,invocation="Mr. Lifesavor",cooldown=5,emoji="<:mrLifeSavor:1009824241954324561>",use=CHARISMA)
limeSkill6Eff = copy.deepcopy(dmgUp)
limeSkill6Eff.power, limeSkill6Eff.turnInit, limeSkill6Eff.stat = 5, 3, CHARISMA
limeSkill6 =  skill("Final Push","limeSkill6",TYPE_BOOST,range=AREA_MONO,area=AREA_CIRCLE_3,cooldown=7,effects=limeSkill6Eff)
limeSkill7_2 = skill("Final Splash","limeSkill7_2",TYPE_DAMAGE,area=AREA_CIRCLE_2,power=80,range=AREA_MONO,knockback=3, cooldown=7,description="Au premier tour, Lime Cookie saute dans les airs en attirant ses ennemis vers elle et augmentant de **50%** ses chances d'esquiver une attaque, puis ratterris au second tour en infligeant des dégâts autour d'elle et repoussant les ennemis touchés")
limeSkill7_2_cast = effect("Cast - {replicaName}","limeSkill7_2_cast",turnInit=2,replique=limeSkill7_2)
limeSkill7_1_eff = effect("Envolée","limeSkill7_eff",dodge=50)
limeSkill7 = skill("Rebond","limeSkill7",TYPE_DAMAGE,power=25,range=AREA_MONO,area=AREA_CIRCLE_3,pull=2,effectOnSelf=limeSkill7_2_cast,cooldown=7,effectAroundCaster=[TYPE_BOOST,AREA_MONO,limeSkill7_1_eff])

# Octo Bouclier Bubble
shieldBubble = copy.deepcopy(bigBubbler)
shieldBubble.use = shieldBubble.depl.skills.use = shieldBubble.depl.skills.effects[0].stat = ENDURANCE
shieldBubble.depl.skills.effects[0].overhealth = int(shieldBubble.depl.skills.effects[0].overhealth*0.5)
shieldBubble.name = shieldBubble.name + " (Endurance)"
shieldBubble.depl.description = shieldBubble.depl.description.replace("{0} __{1}__".format(statsEmojis[sonarPaf.use],allStatsNames[sonarPaf.use]), "{0} __{1}__".format(statsEmojis[shieldBubble.depl.skills.use],allStatsNames[shieldBubble.depl.skills.use]))

imeaDot = effect("Gelûres","imeaDot",MAGIE,emoji='<:imea1:1020057856772419605>',power=25,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,stackable=True,dodge=-3,description="Le froid engourdit vos membres, vous infligeants des dégâts en début de tour et diminuant vos chances d'esquiver des attaques")
imeaWeap = weapon("Pic de glace","imeaWeap",RANGE_LONG,AREA_CIRCLE_5,magie=20,power=53,emoji='<:iceArrow:980172688284876830>',accuracy=60,effectOnUse=imeaDot,use=MAGIE)
imeaSkill1 = skill("Stalactite","imeaSkill1",TYPE_DAMAGE,power=100,cooldown=5,effects=imeaDot,use=MAGIE,emoji='<:ice:941494417926270987>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER])
imeaSkill2 = skill("Lames de glace","imeaSkill2",TYPE_DAMAGE,power=80,cooldown=5,effects=imeaDot,area=AREA_CIRCLE_2,use=MAGIE,emoji='<:imea3:1020057922190974997>',effPowerPurcent=75,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER])
imeaSkill3 = skill("Tempête de neige","imeaSkill3",TYPE_INDIRECT_DAMAGE,cooldown=7,effects=imeaDot,area=AREA_CIRCLE_2,effPowerPurcent=135,emoji='<:imea2:1020057890209407088>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER])
imeaSkill4Lauch = skill("Tombe gelée","imeaUlt",TYPE_DAMAGE,power=200,ultimate=True,cooldown=7,use=MAGIE,effects=imeaDot,effPowerPurcent=150,emoji='<:ice2:941494399337136208>',accuracy=200,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER])
imeaSkill4Cast = effect("Cast - {replicaName}","castSnowgrave",silent=True,turnInit=2,replique=imeaSkill4Lauch)
imeaSkill4 = copy.deepcopy(imeaSkill4Lauch)
imeaSkill4.power, imeaSkill4.effects, imeaSkill4.effectOnSelf = 0, [None], imeaSkill4Cast
imeaSkill5 = skill("Croix gelée","imeaSkill5",TYPE_DAMAGE,power=100,cooldown=7,area=AREA_INLINE_5,use=MAGIE,emoji='<:imea1:1020057856772419605>',effects=imeaDot,effPowerPurcent=85,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER])

# BigShot
bigShotWeapon = weapon("Canon à gros boulets","noneweap",RANGE_LONG,AREA_BOMB_6,ignoreAutoVerif=True,power=0,accuracy=0)
bigShotSkill = skill("Tir de Gros Boulets","bigShotSkill",TYPE_DAMAGE,power=85,area=AREA_CIRCLE_2,cooldown=3,repetition=2,range=AREA_BOMB_6,damageOnArmor=2,accuracy=65,emoji='<:bigShotShot:1030393123077095514>')

# SteelHead
steelHeadWeap = weapon("Salive Explosive","noneWeap",RANGE_MELEE,AREA_CIRCLE_2,0,0,ignoreAutoVerif=True)
steelHeadSkill1_1 = skill("BigBomb","steelHeadSkill",TYPE_DAMAGE,power=120,area=AREA_CIRCLE_2,range=AREA_CIRCLE_3,cooldown=2,emoji='<:bigBomb:1042308669150343200>')
steelHeadSkill1_c = effect("Cast - {replicaName}","steelHealSkillCast",silent=True,turnInit=2,replique=steelHeadSkill1_1,resistance=-100)
steelHeadSkill1 = copy.deepcopy(steelHeadSkill1_1)
steelHeadSkill1.power, steelHeadSkill1.effectOnSelf = 0, steelHeadSkill1_c

# Witch
witchWeapon = weapon("Balles d'énergies","witchWeapon",RANGE_DIST,AREA_CIRCLE_4,power=15,repetition=2,area=AREA_CIRCLE_1,use=MAGIE,accuracy=75,ignoreAutoVerif=True)
witchSkill = skill("Invocation - Squlettes","invocSkeleton",TYPE_SUMMON,invocation="Squelette",nbSummon=3,cooldown=5,emoji='<:squeleton:1034363693724610580>',description="Invoque trois squelettes en ignorant la limite d'invocation",firstSumIgnoreLimit=True)
witchPoisonEff = effect("Poison","witchPoison",MAGIE,power=18,turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji='<:poisonSpell:1042307610847748116>')
witchPoisonEff2 = copy.deepcopy(dmgDown)
witchPoisonEff2.power, witchPoisonEff2.stat, witchPoisonEff2.turnInit = 3, MAGIE, 3
witchPoisonSpell = skill("Fiole de Poison","witchPoisonSpell",TYPE_INDIRECT_DAMAGE,effects=[witchPoisonEff, witchPoisonEff2], emoji='<:poisonSpell:1042307610847748116>',cooldown=5,area=AREA_CIRCLE_2, description="Inflige des dégâts sur la durée et réduit les dégâts infligés par les ennemis ciblé pendant un petit instant")
witchRageEff = effect("Rage",'witchRage',MAGIE,strength=5,magie=5,turnInit=3,emoji='<:rageSpell:1042307646100885514>')
witchRageEff2 = copy.deepcopy(dmgUp)
witchRageEff2.power, witchRageEff2.stat, witchRageEff2.turnInit = 3, MAGIE, 3
witchRageSpell = skill("Sort de Rage","witchRageSpell",TYPE_BOOST,effects=[witchRageEff, witchRageEff2], emoji='<:rageSpell:1042307646100885514>',cooldown=5,area=AREA_CIRCLE_2, description="Augmente la force, la magie et les dégâts infligés des alliés ciblés")

# Rocket Drone
rocketWeap = weapon("Missile","rocketDroneWeap",RANGE_LONG,AREA_CIRCLE_5,power=43,accuracy=80,area=AREA_CIRCLE_1,emoji='<:missile:1051436723252498462>',damageOnArmor=1.35,strength=15,precision=15)
rocketSkill1 = skill("Salve de missiles","rocketSkill1",TYPE_DAMAGE,power=25,repetition=6,damageOnArmor=1.5,cooldown=5,emoji='<:miss2:1051436754101612585>',description="Inflige des dégâts à répétition sur une cible unique avec un bonus de dégâts sur l'armure")
rocketSkill2 = skill("Pluie de missiles","rocketSkill2",TYPE_DAMAGE,power=35,setAoEDamage=True,range=AREA_CIRCLE_5,area=AREA_RANDOMENNEMI_3,repetition=3,emoji='<:miss3:1051436776721481879>',description="Envoi trois salves de missiles qui toucheront des ennemis aléatoires",cooldown=5)

# GlyphidPreorian 
glyphidArmor = effect("Armure Glyphique","glyphidArmor",ENDURANCE,overhealth=350,turnInit=35,resistance=15,type=TYPE_ARMOR,trigger=TRIGGER_START_OF_TURN,description="Le squelette externe du Prétorien Glyphique lui procure une grosse armure qui augmente également sa résistance")
glyphidWeap = weapon("Morsure","glyphidPreWeap",RANGE_MELEE,AREA_CIRCLE_1,power=57,accuracy=90,endurance=15,strength=15,effects=glyphidArmor,effectOnUse = glyphidPretorianAcidEff)
critWeaknessEff = effect("Faiblesse Critique","critWeakNEss",power=35,turnInit=-1,type=TYPE_MALUS,description="Un point faible de l'ennemi augmente les dégâts qu'il reçoit de la part de coups critiques directs",emoji='<:critWeakness:1058021637624188958>')
glyphidCritWeakness = skill("Point Faible","glyphidWeakness",TYPE_PASSIVE,effectOnSelf=critWeaknessEff,emoji="<:critWeakness:1058021637624188958>",description="Une faiblesse dans la carapace du Prétorien Glyphique augmente les dégâts critiques directs qu'il reçoit")
glyphidDeathCloudEff = effect("Nuage Mortuaire","glyphidDeathCloudEff",trigger=TRIGGER_DEATH,type=TYPE_DEPL,turnInit=99,callOnTrigger=glyphidDeathCould,emoji=glyphidDeathCould.cellIcon[1],description="À sa mort, le Prétorien Glyphique laisse un nuage corrosif qui empoissonne les ennemis qui restent à l'intérieur durant 3 tours")
glyphidDeathCloudPassif = skill("Nuage Mortuaire","glyphidDeathCloudPAssif",TYPE_PASSIVE,effectOnSelf=glyphidDeathCloudEff,description=glyphidDeathCloudEff.description,emoji=glyphidDeathCloudEff.emoji[0][0])
glyphidSkill1 = skill("Coup de patte","glyphidSkill1",TYPE_DAMAGE,power=100,range=AREA_CIRCLE_1,damageOnArmor=2,cooldown=5,description="Inflige des dégâts à l'ennemi ciblé, doublés sur l'armure",emoji=batWeap.emoji)
glyphidSkill2 = skill("Crachat Corrosif","glyphidSkill2",TYPE_INDIRECT_DAMAGE,effects=glyphidPretorianAcidEff,range=AREA_CIRCLE_2,area=AREA_LINE_3,effPowerPurcent=150,cooldown=5,emoji=glyphidPretorianAcidEff.emoji[0][0],description="Empoissone les ennemis ciblés")

# Marinier Sabreur
marSabWeap = weapon("Sabre","marSabWeap",RANGE_MELEE,AREA_CIRCLE_1,25,65,strength=10,endurance=10,resistance=10,emoji=ironSword.emoji,repetition=4)
marSabSkill1 = skill("Lame Rapide","marSabSkill1",TYPE_DAMAGE,power=100,range=AREA_CIRCLE_2,cooldown=5,emoji='<:quickSword:1061384146397700096>')
marSabSkill2 = skill("Irruption Brutale","marSabSkill2",TYPE_DAMAGE,replay=True,power=50,cooldown=3,range=AREA_CIRCLE_2,emoji='<:irruption:1061384198071533589>',tpCac=True,description="Vous téléporte au corps à corps de l'ennemi ciblé, lui inflige des dégâts et vous permet de rejouer votre tour")
marSabSkill3_eff = effect("Couvert","cover",redirection=100,emoji='<:cover:1061384419212005417>')
marSabSkill3_eff2 = copy.deepcopy(defenseUp)
marSabSkill3_eff2.power = 20
marSabSkill3 = skill("Gardien","marSabSkill3",TYPE_HEAL,power=40,effects=[marSabSkill3_eff2,marSabSkill3_eff],cooldown=5,tpCac=True,description="Vous téléporte au corps à corps de l'allié ciblé, le soigne, réduit les dégâts qu'il subis et redirige l'intégralité des dégâts directs qu'il reçoit sur vous",emoji='<:gardian:1061384121198317629>')

# Marinier Tireur
marGunWeap = weapon("Pistolet à silex","marGunWeap",RANGE_DIST,AREA_CIRCLE_4,84,65,strength=15,precision=10,agility=5,emoji=troublon.emoji)
marGunSkill1_eff = effect("Oeuil de Linx","marGunSkill1_eff",STRENGTH,precision=10,critical=2,critDmgUp=15,turnInit=3,emoji=linx.emoji)
marGunSkill1 = skill("Oeil de Linx","marGunSkill1",TYPE_BOOST,range=AREA_MONO,effects=marGunSkill1_eff,emoji=linx.emoji,cooldown=5,replay=True,description="Augmente votre précision, taux de coup critique et vos dégâts critiques pendant un instant et vous permet de rejouer votre tour")
marGunSkill2 = skill("Tir Précis","marGunSkill2",TYPE_DAMAGE,power=105,cooldown=5,emoji=shot.emoji)
marGunSkill3 = skill("Balle Fendue","marGunSkill3",TYPE_DAMAGE,power=85,area=AREA_CONE_2,emoji=fireShot.emoji)

# Warden
wardenWeap = weapon("Griffe","wardenWeap",RANGE_LONG,AREA_CIRCLE_1,power=50,accuracy=100,ignoreAutoVerif=True,emoji=batWeap.emoji,use=INTELLIGENCE)
wardenSkill1_eff2 = copy.deepcopy(defenseUp)
wardenSkill1_eff2.power, wardenSkill1_eff2.stat = 4, INTELLIGENCE
wardenSkill1_eff = effect("Aura Protectrice","wardenSkill1_eff",callOnTrigger=wardenSkill1_eff2,area=AREA_DONUT_2,emoji='<:glyphidProtect:1061392660159541389>',turnInit=-1,trigger=TRIGGER_END_OF_TURN)
wardenSkill1 = skill("Protection Glyphique (Résistance)","wardenSkill1",TYPE_PASSIVE,effectOnSelf=wardenSkill1_eff,emoji=wardenSkill1_eff.emoji[0][0],description="À la fin de votre tour, réduit les dégâts subis de vos alliés autour de vous")
wardenSkill2_eff = effect("Aura Protectrice","wardenSkill2_eff",area=AREA_CIRCLE_2,emoji='<:glyphidProtect:1061392660159541389>',turnInit=-1,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_HEAL,power=35,stat=INTELLIGENCE)
wardenSkill2 = skill("Protection Glyphique (Soins)","wardenSkill2",TYPE_PASSIVE,effectOnSelf=wardenSkill2_eff,emoji=wardenSkill1_eff.emoji[0][0],description="À la fin de votre tour, vous soigne vous et vos alliés alentours")

earthGolemWeap = weapon("Masse Rocheuse","earthGolem",RANGE_MELEE,AREA_CIRCLE_1,power=81,accuracy=80,strength=10,endurance=10,resistance=10,emoji='<:stone1:1053730561648246804>')
earthGolemSkill1Eff = effect("Armure Rocheuse","earthGolemEff1",ENDURANCE,overhealth=50,resistance=3,turnInit=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_ARMOR,emoji='<:liuArmor:922292960886915103>',stackable=True)
earthGolemSkill1 = skill("Lancé de Roche","earthGolemSkill1",TYPE_DAMAGE,use=ENDURANCE,power=60,range=AREA_CIRCLE_3,cooldown=5,effectOnSelf=earthGolemSkill1Eff,damageOnArmor=1.2,description="Inflige des dégâts à l'ennemi ciblé (Dégâts augmentés sur l'armure) et octroi une armure au lanceur",emoji='<:stone2:1053730589049618462>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH])
earthGolemSkill2 = skill("Fracture Rocheuse","eathGolemSkill2",TYPE_DAMAGE,use=ENDURANCE,power=100,range=AREA_MONO,area=AREA_CIRCLE_2,emoji='<:enemyStone:1042313085400133632>',cooldown=5,description="Inflige des dégâts autour du lanceur et lui procure une armure",effectOnSelf=earthGolemSkill1Eff,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH])
earthGolemSkill3 = skill("Protection Rocheuse","earthGolemSkill3",TYPE_ARMOR,area=AREA_DONUT_2,range=AREA_MONO,effects=earthGolemSkill1Eff,cooldown=5,effectOnSelf=earthGolemSkill1Eff,selfEffPurcent=125,description='Octroi une armure aux alliés alentours et une armure plus puissante au lanceur',emoji='<:stone4:1053730609685602344>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH])

windGolemDot = effect("Morsure du Vent","windGolemDot",MAGIE,power=30,turnInit=3,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,stackable=True,emoji=megaVentEff.emoji[0][0])
airGolemWeap = weapon("Vent Furieux","windGolem",RANGE_MELEE,AREA_CIRCLE_3,power=43,accuracy=60,area=AREA_CIRCLE_1,use=MAGIE,magie=10,endurance=10,resistance=10,emoji='<:enemyAer:1042313031926947920>',effectOnUse=windGolemDot)
windGolemSkill1 = skill("Tornade Venteuse",'windGolemSkill1',TYPE_DAMAGE,range=AREA_MONO,area=AREA_CIRCLE_2,power=100,use=MAGIE,cooldown=3,emoji='<:aero3:1065647076563746847>',effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_CIRCLE_2,windGolemDot],description="Inflige des dégâts aux ennemis alentours et leur inflige un effet de dégâts sur la durée",effPowerPurcent=75,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR])
windGolemSkill2 = skill("Repoussement Venteux",'windGolemSkill2',TYPE_DAMAGE,range=AREA_MONO,area=AREA_CIRCLE_2,knockback=3,power=80,cooldown=3,use=MAGIE,emoji='<:verAero2:1042350921281191977>',description='Inflige des dégâts et repousse les ennemis proches',condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR])
windGolemSkill3 = skill("Puissance Venteuse",'windGolemSkill3',TYPE_DAMAGE,use=MAGIE,power=120,range=AREA_CIRCLE_3,area=AREA_CIRCLE_1,effects=windGolemDot,emoji='<:verAero:1042350888628535346>',description='Inflige des dégâts aux ennemis ciblés et inflige des dégâts continus à la cible principale',condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR])

zombieUndeadEff = copy.deepcopy(undeadEff)
zombieUndeadEff.power = 50
zombieUndead = copy.deepcopy(undead)
zombieUndead.effectOnSelf = zombieUndeadEff

# FireGolem
fireGolemWeapon = weapon("Flamèche","firegolemweap",RANGE_DIST,AREA_CIRCLE_4,power=46,area=AREA_CONE_2,accuracy=65,use=MAGIE,magie=15,precision=15,emoji='<:enemyFire:1042312985407930428>')
fireGolemSkill1 = skill("Boule de feu","firegolemSkill1",TYPE_DAMAGE,power=80,area=AREA_CONE_2,cooldown=3,emoji=fireCircle.emoji,description="Inflige des dégâts en zone",condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],use=MAGIE)
fireGolemSkill2 = skill("Plus Grosse Boule de feu","firegolemSkill2",TYPE_DAMAGE,power=120,area=AREA_CONE_2,cooldown=5,emoji='<:majorFire2:1042349795353825320>',description="Inflige de plus gros dégâts en zone",condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],use=MAGIE)
fireGolemSkill3 = skill("Très Grosse Boule de feu","firegolemSkill3",TYPE_DAMAGE,power=150,ultimate=True,percing=0,area=AREA_CONE_2,cooldown=7,emoji='<:fire3:1042349767411376148>',description="Inflige de très gros dégâts en zone",condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],use=MAGIE)

# WaterGolem
waterGolemWeapon = weapon("AquaLance","waterGolemWeap",RANGE_LONG,AREA_CIRCLE_5,power=61,accuracy=65,use=MAGIE,magie=15,precision=15,emoji='<:aquaLame:916130446125977602>')
waterGolemSkill1 = skill("Pression","waterGolem1",TYPE_DAMAGE,power=100,cooldown=5,knockback=2,emoji='<:water1:1065647748826791966>',use=MAGIE,description="Inflige des dégâts et repousse la cible",condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER])
waterGolemSkill2Eff = effect("Destabilisé","waterGolem2",MAGIE,agility=-5,precision=-5)
waterGolemSkill2 = skill("Geyser","waterGolem2",TYPE_DAMAGE,power=120,cooldown=5,emoji='<:geyser:961185615859290163>',effects=waterGolemSkill2Eff,use=MAGIE,description="Inflige des dégâts et réduit l'agilité ainsi que la précision de la cible",condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER])


# Surriner
surrinWeap = weapon("Surrin","surrinWeap",RANGE_MELEE,AREA_CIRCLE_1,65,80,strength=10,endurance=10,agility=10,emoji='<:bleedingdague:894552391444234242>',ignoreAutoVerif=True)
surrinSkill1Eff = copy.deepcopy(vulne)
surrinSkill1Eff.stat, surrinSkill1Eff.power, surrinSkill1Eff.turnInit = STRENGTH, 5, 3
surrinSkill1 = skill("Attaque Sournoise","surrinSkill1",TYPE_DAMAGE,power=60,cooldown=3,effBeforePow=True,emoji='<:trickAttack:971788242284343336>',effects=surrinSkill1Eff,range=AREA_CIRCLE_1)
surrinSkill2 = skill("Triple Attaque","surrinSkill2",TYPE_DAMAGE,power=50,repetition=3,emoji='<:dreamWithinADream:1053655563193561138>',range=AREA_CIRCLE_1,cooldown=5)

# Archer
bowWeap = weapon("Arc","bowWeap",RANGE_DIST,AREA_CIRCLE_4,power=50,accuracy=75,strength=10,precision=10,intelligence=10,emoji='<:tirPuissant:1113688115689816094>',ignoreAutoVerif=True)
bowSkill1 = skill("Tir Droit","bowSkill1",TYPE_DAMAGE,power=100,cooldown=5,emoji='<:tirDroit:1113688144190128158>',range=AREA_CIRCLE_4)
bowSkill2 = skill("Mâchoires de Fer","bowSkill2",TYPE_DAMAGE,power=60,range=AREA_CIRCLE_4,effects=machDeFer.effects,emoji=machDeFer.emoji,cooldown=5)