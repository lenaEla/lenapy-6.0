from classes import *
from constantes import *
from advObjects.advWeapons import *
from advObjects.advSkills import *
from advObjects.advStuffs import *
from advObjects.advInvocs import *
from advObjects.advEffects import *
from advObjects.advAllies import *

# Octariens spells
octoEm = '<:splatted1:727586364618702898>'

systemImu = effect("Résistance aux dégâts indirects","inkResistanceOcto",HARMONIE,inkResistance=12,description="Réduit les dégâts indirects reçu par le porteur",emoji=uniqueEmoji('<:nanoMedecine:921544107053158420>'),turnInit=2)
zoneOctoInkRes = skill("Nano-Science","octoBaseInkResSkill",TYPE_BOOST,0,range=AREA_MONO,area=AREA_CIRCLE_3,use=HARMONIE,effect=systemImu,cooldown=4,emoji='<:nanoMedecine:921544107053158420>')

octoShieldWeap = weapon("Bouclier Octarien","aaa",0,AREA_CIRCLE_2,power=20,sussess=100,price=0,endurance=20,strength=-50,effect="lo",emoji=octoEm,ignoreAutoVerif=True)
octoBallWeap = weapon("Balles rebondissantes","aaa",1,AREA_CIRCLE_3,45,30,0,repetition=3,strength=10,agility=10,emoji=octoEm,ignoreAutoVerif=True)
octoSnipeWeap = weapon("Snipeur Octarien","aaa",2,AREA_CIRCLE_6,52,85,0,strength=20,emoji=octoEm)
octoFly = weapon("Machinerie volante","aaa",RANGE_DIST,AREA_CIRCLE_5,50,75,-20,10,emoji=octoEm,ignoreAutoVerif=True)
octoHeal = weapon("Octo heal","aaa",1,AREA_CIRCLE_3,35,50,0,use=CHARISMA,type=TYPE_HEAL,target=ALLIES,emoji='<:medic:882890887120699444>')
octoDef = weapon('OctoDef',"aaa",1,AREA_CIRCLE_3,10,100,0,effectOnUse="md",use=INTELLIGENCE,target=ALLIES,type=TYPE_HEAL,intelligence=20)
flyfishweap = weapon("Lance-Multi-Missiles","ffweap",2,AREA_CIRCLE_7,1,200,0,effectOnUse="mf",type=TYPE_DAMAGE,strength=30,ignoreAutoVerif=True,emoji='<:tentamissile:884757344397951026>')
octoBoumWeap = weapon("noneWeap","aaa",1,AREA_CIRCLE_1,0,0,0,effect="mg") 
ruddinweap = weapon("Carreaux","aaa",RANGE_DIST,AREA_CIRCLE_5,23,70,0,0,0,0,0,0,0,0,repetition=3,emoji='<:chaos:892857755143127090>')
ruddinweap2 = weapon("Carreaux","aaa",RANGE_MELEE,AREA_CIRCLE_3,28,70,0,0,0,0,0,0,0,0,repetition=3,emoji='<:chaos:892857755143127090>')
malusWeaponEff = effect("Embrouillement","aaa",INTELLIGENCE,strength=-5,magie=-5,critical=-2,type=TYPE_MALUS)
malusWeapon = weapon("Magie sombre","aaa",RANGE_DIST,AREA_CIRCLE_5,53,60,0,effectOnUse=malusWeaponEff,use=MAGIE)
malusSkill1Eff = effect("Malussé","malusé",INTELLIGENCE,-15,magie=-15,resistance=-5,type=TYPE_MALUS)
malusSkill1 = skill("Abrutissement","aaa",TYPE_MALUS,0,area=AREA_CIRCLE_2,effect=malusSkill1Eff,cooldown=5,initCooldown=2)
malusSkill2 = skill("Éclair","aaa",TYPE_DAMAGE,0,80,cooldown=2,sussess=65,use=MAGIE,emoji='<:darkThunder:912414778356564019>')
kralamWeap = weapon("Décharge motivante","aaa",RANGE_DIST,AREA_DONUT_4,50,100,0,type=TYPE_HEAL,target=ALLIES,use=CHARISMA)
kralamSkill2 = skill("Électrochoc","kralamSkill2",TYPE_DAMAGE,0,80,area=AREA_CIRCLE_1,use=CHARISMA,cooldown=3,initCooldown=2,emoji='<:electroShoc:912414625679695873>')
temNativTriggered = effect("Promue",'tem',magie=0,turnInit=-1,unclearable=True,emoji=uniqueEmoji('<:colegue:895440308257558529>'))
temNativ = effect("College",'tem1',trigger=TRIGGER_ON_REMOVE,turnInit=3,unclearable=True,callOnTrigger=temNativTriggered)
temWeap = weapon("Temmie flakes","aaa",RANGE_DIST,AREA_CIRCLE_5,42,75,0,use=MAGIE,effect=temNativ,emoji='<:temFlakes:919168887222829057>',say=["TEMMIE FLAKES ! An original breakfast !","TEMMIE FLAKES ! It's so good you can't taste it !","TEMMIE FLAKES ! Don't forget to digest it !","TEMMIE FLAKES in your mouth","Whouwhouwhouwhou !"],message="{0} donne des TEMMIE FLAKES à {1}")
temSkill1 = skill("Alergies","aaa",TYPE_DAMAGE,0,100,use=MAGIE,initCooldown=3)
octoMageWeap = weapon("noneWeap","aaa",1,AREA_CIRCLE_1,0,0,0)
chargeShot = skill('Tir chargé',"aaa",TYPE_DAMAGE,0,80,emoji=shot.emoji,cooldown=4,initCooldown=2,damageOnArmor=1.5)
ultraShot = skill("Tir pénétrant","ultraShot",TYPE_DAMAGE,0,35,cooldown=3,damageOnArmor=5,repetition=3,emoji='<:targeted:912415337088159744>',area=AREA_LINE_2)
octobomberWeap = weapon("Lance Bombe Splash","0",RANGE_LONG,AREA_CIRCLE_5,48,int(splatbomb.sussess*0.9),area=splatbomb.area,emoji=splatbomb.emoji)
tentaWeap = weapon("Double Canons","0",RANGE_MELEE,AREA_CIRCLE_3,42,35,repetition=4,emoji=octoEm)
octoTour = weapon("noneWeap","aaa",RANGE_LONG,AREA_CIRCLE_1,0,0,0,resistance=500)
octoTourEff1 = effect("Grand protecteur","octTourEff1",turnInit=-1,emoji=uniqueEmoji('<:tower:905169617163538442>'),unclearable=True,description="L'OctoTour protège ses alliés\nTant qu'il est en vie, celui-ci subis les dégâts directs de ses alliés à leur place")
octoTourEff2 = effect("Protection magique","octTourEff2",redirection=100,turnInit=-1,emoji=uniqueEmoji('<:tower:905169617163538442>'))
octoTourSkill = skill("Grand protecteur","octoTourSkill",TYPE_PASSIVE,0,effectOnSelf=octoTourEff1,use=None,emoji='<:tower:905169617163538442>')
veterHealSkill1 = skill("Here we go again","octoHealVet1",TYPE_RESURECTION,0,120,cooldown=4,use=CHARISMA)
veterHealSkill2 = skill("Renouvellement","octaHealVet2",TYPE_HEAL,0,100,use=CHARISMA,cooldown=5,initCooldown=2,emoji='<:heal:911735386697519175>')
veterHealSkill3 = skill("I'm a healer but...","octaHealVet3",TYPE_MALUS,0,area=AREA_CIRCLE_1,effect=incur[3],cooldown=5,emoji=incur[3].emoji[0][0])
veterHealSkill4 = skill("Théorie du complot","octaHealVet4",TYPE_DAMAGE,0,100,use=CHARISMA,cooldown=3)
veterHealWeap = copy.deepcopy(octoHeal)
veterHealWeap.negativeHeal, veterHealWeap.power = -20, veterHealWeap.power + 10
antiArmorShot = skill("Tir anti-matériel","antiArmorShot",TYPE_DAMAGE,0,100,ultimate=True,damageOnArmor=666,cooldown=7)
zombieSkillEff = effect("Marcheur des limbes","zombaSkillArmor",ENDURANCE,overhealth=100,turnInit=-3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
zombieSkill = skill("Frappe d'outre-tombe","zombiSkill",TYPE_DAMAGE,0,100,use=ENDURANCE,effectOnSelf=zombieSkillEff,cooldown=5)
octoInvocWeap = weapon("Cristal d'Invocateur","OctoSummonerWeap",RANGE_LONG,AREA_CIRCLE_5,35,75,0,strength=10,endurance=10,charisma=10,agility=10,precision=10,intelligence=10,magie=10,emoji=octoEm,ignoreAutoVerif=True)

octoBoost1Eff = effect("Expérimentation 1 - Force","octoBuff1",INTELLIGENCE,strength=10,emoji=uniqueEmoji('<:strengthBuff:914904347039629472>'))
octoBoost2Eff = effect("Expérimentation 2 - Magie","octoBuff2",INTELLIGENCE,magie=10,emoji=uniqueEmoji('<:magicBuff:914904390056415292>'))
octoBoost3Eff = effect("Expérimentation 3 - Résistance","octoBuff3",INTELLIGENCE,resistance=5,emoji=uniqueEmoji('<:resisBuff:914904412357537873>'))
octoBoost4Eff = effect("Expérimentation 4 - Agilité","octoBuff4",INTELLIGENCE,agility=10,emoji=uniqueEmoji('<:agiBuff:914904736166199316>'))

octoBoostSkill1 = skill(octoBoost1Eff.name,"octoBoostSkill1",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effect=octoBoost1Eff,emoji=octoBoost1Eff.emoji[0][0],use=INTELLIGENCE,cooldown=5)
octoBoostSkill2 = skill(octoBoost2Eff.name,"octoBoostSkill2",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effect=octoBoost2Eff,emoji=octoBoost2Eff.emoji[0][0],use=INTELLIGENCE,cooldown=5)
octoBoostSkill3 = skill(octoBoost3Eff.name,"octoBoostSkill3",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effect=octoBoost3Eff,emoji=octoBoost3Eff.emoji[0][0],use=INTELLIGENCE,cooldown=5)
octoBoostSkill4 = skill(octoBoost4Eff.name,"octoBoostSkill4",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effect=octoBoost4Eff,emoji=octoBoost4Eff.emoji[0][0],use=INTELLIGENCE,cooldown=5)

octoBoostWeap = weapon("Fioles d'expérimentations","octoBoostWeap",RANGE_DIST,AREA_CIRCLE_4,35,65,intelligence=25,use=INTELLIGENCE,emoji=octoBallWeap.emoji,ignoreAutoVerif=True)

octaStransEff = effect('Multi-Bras',"ocSt",aggro=15,resistance=10,turnInit = -1,unclearable=True,emoji=uniqueEmoji('<:octoStrans:900084603140853760>'))
octaStrans = skill("Multi-Bras","octaStrans",TYPE_PASSIVE,0,effectOnSelf=octaStransEff,emoji='<:multibras:900084714675785759>')

# Kitsunes sist's spells
charming = effect("Charmé (ennemi)","kitsuneSisterEff",CHARISMA,strength=-2,magie=-2,charisma=-2,intelligence=-2,resistance=-1,stackable=True,type=TYPE_MALUS,description="Vous devriez plutôt vous concentrer sur le combat plutôt que sur celles qui sont en train de vous tuer doucement...",emoji=sameSpeciesEmoji("<:CharmeB:908793556435632158>","<:charmeR:908793574437584956>"),turnInit=2)
charming2 = effect("Charmé (allié)","kitsuneSisterEffBuff",CHARISMA,strength=10,magie=10,charisma=10,intelligence=10,resistance=5,stackable=True,type=TYPE_BOOST,description="Vous avez fortement envie d'impressioner l'une de vos alliés...",emoji=sameSpeciesEmoji("<:CharmeB:908793556435632158>","<:charmeR:908793574437584956>"),turnInit=2)

liuWeapEff = effect("Kitsune de la terre","liuWeapEff",emoji=uniqueEmoji('<:earthKitsune:917670882586017792>'),stat=CHARISMA,aggro=15,endurance=10,agility=10,turnInit=-1,unclearable=True,description="La résistance de Liu en a épaté plus d'un.\nÀ chaque attaque subis, donne l'effet Sous le Charme II à l'attaquant",callOnTrigger=charming)
liuWeap = weapon("Sable","liuWeap",RANGE_MELEE,AREA_CIRCLE_2,27,50,repetition=3,strength=10,magie=10,charisma=10,effect=liuWeapEff,effectOnUse=charming,use=MAGIE,emoji='<:liuWeap:908859892272611348>')
liaWeapEff = effect("Kitsune des vents","liaWeapEff",CHARISMA,emoji=uniqueEmoji('<:airKitsune:917670912646602823>'),aggro=15,agility=10,precision=10,turnInit=-1,unclearable=True,description="L'agilité de Lia en a épaté plus d'un\nÀ chaque attaque esquivé, donne 2 fois l'effet Sous le Charme II à l'attaquant",callOnTrigger=charming)
liaWeap = weapon("Vent","liaWeap",RANGE_MELEE,AREA_CIRCLE_2,16,50,repetition=5,charisma=10,magie=10,agility=10,effect=liaWeapEff,effectOnUse=charming,use=MAGIE,emoji='<:liaWeap:908859908034793552>')
lioWeapEff = effect("Kitsune de l'eau","lioWeapEff",CHARISMA,emoji=uniqueEmoji('<:waterKitsune:917670866626707516>'),intelligence=10,magie=10,turnInit=-1,unclearable=True,description="La douceur de Lio en a épaté plus d'un.\nÀ chaque soins réalisés par cette dernière, donne l'effet Sous le Charme III à l'allié soigné",callOnTrigger=charming2)
lioWeap = weapon("Écume","lioWeap",RANGE_LONG,AREA_CIRCLE_5,64,50,charisma=20,effect=lioWeapEff,use=CHARISMA,emoji='<:lioWeap:908859876812415036>',type=TYPE_HEAL,target=ALLIES)
lioRez = skill("Eau purifiante","lioRez",TYPE_RESURECTION,0,100,AREA_CIRCLE_7,ultimate=True,area=AREA_CIRCLE_2,use=CHARISMA,emoji='<:lioSkill:922328964926697505>',cooldown=5,say="Allez vous autre... C'est pas le moment de stagner...")
lieWeapEff = effect("Kitsune du feu","lieWeapEff",CHARISMA,emoji=uniqueEmoji('<:fireKitsune:917670925904785408>'),intelligence=10,magie=10,turnInit=-1,unclearable=True,description="L'ardeur de Liz en a comblé plus d'un\nÀ chaque attaque réalisée, donne l'effet Sous le Charme II à la cible",callOnTrigger=charming)
lieWeap = weapon("Braise","lieWeap",RANGE_LONG,AREA_CIRCLE_4,48,50,charisma=10,magie=10,area=AREA_CIRCLE_1,effect=lieWeapEff,use=MAGIE,emoji='<:lizWeap:908859856608460820>')
lieSkillEff = effect("Combustion","lieSKillEff",MAGIE,resistance=-2,power=30,turnInit=4,lvl=4,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,stackable=True,emoji=uniqueEmoji('<:lizIndirect:917204753610571776>'))
lieSkill = skill("Flamme intérieur","lizSkill",TYPE_DAMAGE,0,effect=lieSkillEff,cooldown=3,power=115,say="Voyons voir si tu va pouvoir résister longtemps...",use=MAGIE,emoji='<:lizSkill:922328829765242961>')
liaSkill = skill("Douce caresse","liaSkill",TYPE_DAMAGE,0,power=70,range=AREA_CIRCLE_1,effect=charming,effPowerPurcent=300,knockback=1,cooldown=5,use=MAGIE,say="Roh allez, détent toi un peu !",emoji='<:liaSkill:922291249002709062>')
liuSkillEff = effect("Armure Télurique","liuSkillEff",CHARISMA,overhealth=150,aggro=15,inkResistance=10,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji('<:liuArmor:922292960886915103>'),turnInit=3)
liuSkill = skill("Frappe Télurique","liuSkill",TYPE_DAMAGE,0,power=100,use=ENDURANCE,cooldown=3,effectOnSelf=liuSkillEff,say="Oh je suis pas encore finie tu va voir !",emoji='<:liuSkill:922328931502280774>')
lioHealZone = skill("Giga Soins Aquatique","lioHealZone",TYPE_HEAL,power=60,area=AREA_CIRCLE_1,cooldown=5,emoji='<:extraHeal:952522927214051348>',use=CHARISMA)
lioLB = skill("Riptide","lioLb",TYPE_DAMAGE,power=150,range=transObs.range,area=transObs.area,cooldown=transObs.cooldown+2,initCooldown=transObs.initCooldown,effectAroundCaster=[TYPE_BOOST,AREA_DONUT_5,charming2],use=CHARISMA,shareCooldown=True,description="Inflige des dégâts aux ennemis en ligne droite tout en augmantant les statistiques des alliés autour de vous\n\nCette compétence est une Transcendance", url='https://media.discordapp.net/attachments/971788596401041480/979903178252374086/20220528_021252.gif',emoji='<:purge:979903342136422440>')
liaLB = skill("Danse des Vents","liaLb",use=CHARISMA,types=TYPE_MALUS,range=AREA_MONO,area=AREA_DONUT_3,effect=charming,effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_2,charming2],effPowerPurcent=1000,cooldown=7,initCooldown=transObs.initCooldown,description="Réduit fortement les statistiques des ennemis autour de vous tout en augmentant celles des alliés autours de vous\nLa puissance du bonus sur les alliés est divisé par cinq\n\nCette compétence est une transcendance",url='https://media.discordapp.net/attachments/971788596401041480/979903177593880596/20220528_021716.gif',emoji='<:contredanse:979903303536230430>')
LIAMINDODGE = 25
liaCounterSkillEff = effect("Kurrata Kaze","liaEnCounterEff",counterProb=35,turnInit=-1,unclearable=True,emoji=windDanceEff.emoji,description="Octroi à Lia **35%** de chance d'effectuer une contre-attaque lorsqu'elle esquive un assaut venant d'un ennemi à 3 cases ou plus d'elle\nGarantie également à Lia un minimum de **{0}%** de chance d'esquiver une attaque".format(LIAMINDODGE))
liaCounterSkill = skill("Kurrata Kaze","liaCounter",TYPE_PASSIVE,effectOnSelf=liaCounterSkillEff,emoji=windDanceEff.emoji[0][0])

LIZLBPOWERGAINPERCHARM = 15
lizLB = skill("Flamme Sentimentale","lizLb",TYPE_DAMAGE,use=CHARISMA,power=55,setAoEDamage=True,area=AREA_ALL_ENEMIES,cooldown=7,shareCooldown=True,effectAroundCaster=[TYPE_BOOST,AREA_DONUT_3,charming2],initCooldown=transObs.initCooldown,description="Inflige des dégâts à tous les ennemis en consommant leurs effet <:CharmeB:908793556435632158> __Sous le Charme II__. Pour chaque effet consummé, la puissance de cette compétence augmente de {0}\nAugmente également les statistiques des alliés autour de vous\n\nCette compétence est une transcendance".format(LIZLBPOWERGAINPERCHARM),url="https://media.discordapp.net/attachments/971788596401041480/979903177111515177/20220528_022438.gif",emoji='<:chocTermique:979903323094261771>')
liuLBEff = copy.deepcopy(defenseUp)
liuLBEff.stat, liuLBEff.power = ENDURANCE, 22
liuLB = skill("Mur Tectonique","liuLb",TYPE_ARMOR,range=AREA_MONO,area=AREA_ALL_ALLIES,cooldown=7,shareCooldown=True,effect=liuLBEff,effectAroundCaster=[TYPE_BOOST,AREA_DONUT_3,charming2],initCooldown=3,emoji=trans.emoji,url="https://cdn.discordapp.com/attachments/912137828614426707/957181011555397642/20220326_083047.gif")
liaSkill1, liaSkill2, liaSkill1Eff = copy.deepcopy(airCircle), copy.deepcopy(storm2), copy.deepcopy(findEffect(airCircle.effect[0]))
liaSkill1.use = liaSkill2.use = liaSkill1Eff.stat = AGILITY
liaSkill1.effect = [liaSkill1Eff]
liuMontBreaker = copy.deepcopy(cassMont)
liuMontBreaker.use = liuMontBreaker.effect[0].stat = ENDURANCE
liuAoEShieldEff = effect("Armure Rocheuse","liu",ENDURANCE,overhealth=50,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=liuSkillEff.emoji)
liuAoEShieldOnHer = copy.deepcopy(defenseUp)
liuAoEShieldOnHer.power = liuAoEShieldOnHer.aggro = 15
liuAoEShieldSkill = skill("Cristalisation","liuAoEShieldSkill",TYPE_ARMOR,effect=liuAoEShieldEff,cooldown=5,area=AREA_DONUT_2,range=AREA_MONO,effectOnSelf=liuAoEShieldOnHer,description="Liu octroi une armure à ses alliés alentours et réduit les dégâts qu'elle subit",use=ENDURANCE)
lizDotAoEEff = effect("Combustion Explosive","lizDotAoE",MAGIE,power=28,area=AREA_CIRCLE_3,turnInit=3,lvl=3,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji=elemEmojis[ELEMENT_FIRE])
lizDotAoE = skill("Braise Explosive","lizDotAoE",TYPE_DAMAGE,power=50,use=MAGIE,effect=lizDotAoEEff,cooldown=5,emoji=elemEmojis[ELEMENT_FIRE])

lizAoELauch = skill("Déflagration","lizAoe",TYPE_DAMAGE,power=200,area=AREA_CIRCLE_5,range=AREA_MONO,use=MAGIE,cooldown=7)
lizAoeCast = effect("Cast - {replicaName}","lizAoeCast",turnInit=2,silent=True,replique=lizAoELauch)
lizAoE = copy.deepcopy(lizAoELauch)
lizAoE.power, lizAoE.effectOnSelf = 0, lizAoeCast

liuFurTel = copy.deepcopy(earthUlt2Lanch)
liuFurTelCastEff = effect("Cast - {replicaName}","liuFurTelCast",turnInit=2,replique=liuFurTel)
liuFurTelCast = skill("Glissement Tellurique",liuFurTel.id,TYPE_DAMAGE,power=20,effectOnSelf=liuFurTelCastEff,range=AREA_MONO,area=AREA_INLINE_4,emoji=liuFurTel.emoji,cooldown=liuFurTel.cooldown,pull=3)

# Hunter's spells
hunterWeap = weapon("Logique irréfutable","hunterWeap",RANGE_LONG,AREA_CIRCLE_5,40,sussess=100,emoji='<:Objection:800829922356232202>',use=INTELLIGENCE,damageOnArmor=1.5,message="{0} utilise sa Logique irréfutable")
hunterSkill1Eff = effect("Cornered","hunterSkill1Eff",INTELLIGENCE,strength=-10,magie=-10,charisma=-10,intelligence=-10,type=TYPE_MALUS,emoji=uniqueEmoji('<a:HunterPoint:800834253889732689>'))
hunterSkill1 = skill("Preuve à l'appui","hunterSkill1",TYPE_MALUS,0,area=AREA_CIRCLE_1,effect=hunterSkill1Eff,cooldown=3,use=INTELLIGENCE,emoji='<a:HunterSmug:800841378967715841>')
hunterSkill2 = skill("Poings sur la table","hunterSkill2",TYPE_DAMAGE,0,120,use=INTELLIGENCE,cooldown=3,emoji='<a:HunterSlam:800834288487759923>')
hunterSkill3Eff = effect("Vérité","hunterSkill3Eff",INTELLIGENCE,strength=10,magie=10,charisma=10,intelligence=10,emoji=uniqueEmoji('<:Eureka:800837165688815636>'))
hunterSkill3 = skill("Vérité entrevue",'hunterSkill3',TYPE_BOOST,0,area=AREA_CIRCLE_1,effect=hunterSkill3Eff,cooldown=3,emoji='<:Eureka:800837165688815636>')
hunterSkill4 = skill("Outdated autopsy report","hunterSkill4",TYPE_RESURECTION,0,150,use=INTELLIGENCE,emoji='<:AutopsyReport:800839396151656469>',cooldown=5,message='{0} a mis à jour le rapport d\'autopsy de {2}',url='https://cdn.discordapp.com/attachments/927195778517184534/934985362462343218/20220124_023739.gif')

# Bob Hi
bobSays = copy.deepcopy(temSays)
bobSays.start = "Hello. I'm Bob"

# Cliroptère skill
clirHeal = skill("Clémence","stopSpamThatPls",TYPE_HEAL,0,70,cooldown=2,use=CHARISMA)
clirWeap = weapon("Bouclier Nocturne","clirWeap",RANGE_MELEE,AREA_CIRCLE_1,80,70,charisma=10,resistance=10,endurance=10,use=CHARISMA)

# Octa PomPom Skills
octoPom1Eff = effect("Chorégraphie 1 - Force","octoBuff1",CHARISMA,strength=10,emoji=uniqueEmoji('<:strengthBuff:914904347039629472>'))
octoPom2Eff = effect("Chorégraphie 2 - Magie","octoBuff2",CHARISMA,magie=10,emoji=uniqueEmoji('<:magicBuff:914904390056415292>'))
octoPom3Eff = effect("Chorégraphie 3 - Résistance","octoBuff3",CHARISMA,resistance=5,emoji=uniqueEmoji('<:resisBuff:914904412357537873>'))
octoPom4Eff = effect("Chorégraphie 4 - Agilité","octoBuff4",CHARISMA,agility=10,emoji=uniqueEmoji('<:agiBuff:914904736166199316>'))

octoPomSkill1 = skill(octoPom1Eff.name,"octoPomSkill1",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effect=octoPom1Eff,emoji=octoPom1Eff.emoji[0][0],use=CHARISMA,cooldown=5)
octoPomSkill2 = skill(octoPom2Eff.name,"octoPomSkill2",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effect=octoPom2Eff,emoji=octoPom2Eff.emoji[0][0],use=CHARISMA,cooldown=5)
octoPomSkill3 = skill(octoPom3Eff.name,"octoPomSkill3",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effect=octoPom3Eff,emoji=octoPom3Eff.emoji[0][0],use=CHARISMA,cooldown=5)
octoPomSkill4 = skill(octoPom4Eff.name,"octoPomSkill4",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effect=octoPom4Eff,emoji=octoPom4Eff.emoji[0][0],use=CHARISMA,cooldown=5)

octaPomWeapon = weapon("PomPom","octaPomPomWeap",RANGE_LONG,AREA_CIRCLE_6,45,50,charisma=20,emoji=octoEm,use=CHARISMA,ignoreAutoVerif=True)

# Cliroptère infirmier
clirInfWeap = weapon("Sono-Thérapie","clirInfWeap",RANGE_LONG,AREA_CIRCLE_4,45,100,charisma=20,type=TYPE_HEAL,target=ALLIES,use=CHARISMA)

# OctoSus
octoSusSkill1 = skill("Vent",'octoSusSkill1',TYPE_DAMAGE,0,80,range=AREA_RANDOMENNEMI_1,cooldown=3,emoji='<:Vent:932241554125520957>',tpCac=True)
octoSusSkill2Eff = effect("Saboté",'octoSusSkill2Eff',INTELLIGENCE,type=TYPE_MALUS,strength=-10,magie=-10,charisma=-10,intelligence=-10,emoji='<:Sabotage:932241553865465946>')
octoSusSkill2 = skill('Sabotage','octoSusSkill2',TYPE_MALUS,0,effect=octoSusSkill2Eff,area=AREA_DONUT_1,range=AREA_MONO,emoji='<:Sabotage:932241553865465946>')
octoSusWeap = weapon("Kill",'octoSusWeap',range=RANGE_LONG,effectiveRange=AREA_CIRCLE_1,power=77,sussess=90,emoji='<:Kill:932241554050023484>')

# Unform Light A
unformLightAWeapon = weapon("Lumière destructrice",'informLightAWeap',RANGE_MELEE,AREA_CIRCLE_2,108,60,strength=20,magie=20)
unformLightASkill1 = skill("Corruption",'unformLightASkill1',TYPE_DAMAGE,power=50,range=AREA_CIRCLE_3,effect=vulneTabl[2],cooldown=5)
unformLightASkill2Eff = effect('Annéantissement','unformLightASkill2Eff',MAGIE,type=TYPE_INDIRECT_DAMAGE,power=30,turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,stackable=True)
unformLightASkill2 = skill("Anéantissement de l'esprit",'unformLightASkill2',TYPE_INDIRECT_DAMAGE,range=AREA_RANDOMENNEMI_2,area=AREA_CIRCLE_1,effect=unformLightASkill2Eff,cooldown=3)
unformLightASkill3Eff = effect('Lueur mauvaise','unformLightASkill3Eff',MAGIE,magie=10,strength=5,turnInit=3)
unformLightASkill3 = skill("Lueur mauvaise",'unformLightASkill3',TYPE_BOOST,range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=5,effect=unformLightASkill3Eff)

unformDarknessDot = effect('Anéantissement','unformDarknessMainDoT',MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=15,turnInit=8,lvl=8,stackable=True)
unformDarknessAWeapon = weapon("Noirceur destructrice",'unformDarknessAWeap',RANGE_MELEE,AREA_CIRCLE_2,41,99,strength=20,magie=20,use=MAGIE,effectOnUse=unformDarknessDot)
unformDarknessASkill1 = skill('Fissure','unformDarkASkill1',TYPE_INDIRECT_DAMAGE,range=AREA_CIRCLE_1,cooldown=5,effect=unformDarknessDot,effPowerPurcent=500)
unformDarknessASkill2 = skill('Ombre aveuglante','unformDarknessASkill2',TYPE_DAMAGE,power=100,range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=3)
unformDarknessASkill3Eff = effect('Ténèbres consummants','unformDarknessASkill3Eff',MAGIE,type=TYPE_MALUS,resistance=-5,endurance=-10,turnInit=3)
unformDarknessASkill3 = skill("Ombre mauvaise",'unformDarknessASkill3',TYPE_MALUS,range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=5,effect=unformDarknessASkill3Eff)

unformDarknessBWeapon = weapon("Noirceur absurde","unformDarkBWeapon",RANGE_DIST,AREA_CIRCLE_4,46,75,magie=20,effectOnUse=unformDarknessDot,use=MAGIE)
unformDarknessBSkill1 = skill("Choc Mental","unforDarkBSkill1",TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_2,effect=unformDarknessDot,cooldown=5)
unformDarknessBSkill2 = skill("Assombrissement informe","unformDarkSkill2",TYPE_DAMAGE,power=100,cooldown=3,use=MAGIE)
unformDarknessBSkill3 = skill("Eclair Sombre Informe","darkBSkill3",TYPE_DAMAGE,power=75,setAoEDamage=True,use=MAGIE,area=AREA_CIRCLE_1,cooldown=4)

octoBooyahBomb = copy.deepcopy(booyahBombLauch)
octoBooyahBomb.power = int(octoBooyahBomb.power*0.6)
octoBooyahBombCastEff = copy.deepcopy(booyahBombEff)
octoBooyahBombCastEff.replica = octoBooyahBomb
octoBooyahBombCast = copy.deepcopy(booyahBombCast)
octoBooyahBombCast.effectOnSelf = octoBooyahBombCastEff

octoTentaMissiles = copy.deepcopy(multiMissiles)
octoTentaMissiles.area = AREA_RANDOMENNEMI_3

lizBoomLaunch = copy.deepcopy(explosion)
lizBoomLaunch.power = int(lizBoomLaunch.power * 0.70)
lizBoomEff = copy.deepcopy(castExplo)
lizBoomEff.replica = lizBoomLaunch
lizBoomCast = copy.deepcopy(explosionCast)
lizBoomCast.effectOnSelf = lizBoomEff

stellaAuraEff = copy.deepcopy(dmgUp)
stellaAuraEff.power, stellaAuraEff.stat = 5, MAGIE
stellaAura = effect("Aura solaire","stellaAura",MAGIE,trigger=TRIGGER_END_OF_TURN,callOnTrigger=stellaAuraEff,area=AREA_DONUT_2,turnInit=-1,unclearable=True,description="En fin de tour, augmente légèrement les dégâts infligés par les alliés alentours")
stellaWeap = weapon("Pulsion électro-magnetique","stellaWeap",RANGE_DIST,AREA_CIRCLE_5,53,75,magie=10,endurance=10,resistance=10,effect=stellaAura)
stellaSkill1Eff = copy.deepcopy(dmgUp)
stellaSkill1Eff.power, stellaSkill1Eff.stat = stellaAuraEff.power*3, MAGIE
stellaSkill1 = skill("Galvanisation stellaire","stellaSkill1",TYPE_BOOST,range=AREA_MONO,area=AREA_CIRCLE_3,effect=stellaSkill1Eff,cooldown=5,description="Augmente les dégâts infligés par les alliés alentours")
stellaSkill2Eff = copy.deepcopy(defenseUp)
stellaSkill2Eff.power, stellaSkill2Eff.stat = 15, MAGIE
stellaSkill2 = skill("Diffraction stellaire","stellaSkill2",TYPE_BOOST,effect=stellaSkill2Eff,area=AREA_CIRCLE_2,range=AREA_MONO,cooldown=5,description="Réduit les dégâts subis par les alliés alentours")
stellaSkill3Eff1, stellaSkill3Eff2 = copy.deepcopy(dmgUp), copy.deepcopy(defenseUp)
stellaSkill3Eff1.stat = stellaSkill3Eff2.stat = MAGIE
stellaSkill3Eff1.power = stellaSkill3Eff2.power = 10
stellaSkill3 = skill("Focalisation galactique","stellaSkill3",TYPE_BOOST,effect=[stellaSkill3Eff1, stellaSkill3Eff2],cooldown=5,description="Augmente les dégâts infligés par un allié tout en réduisant les dégâts qu'il subit")
stellaSkill4Eff = copy.deepcopy(vulne)
stellaSkill4Eff.power, stellaSkill4Eff.stat, stellaSkill4Eff.turnInit = 7, MAGIE, 2
stellaSkill4 = skill("Affaiblissement stellaire","stellaSkill4",TYPE_MALUS,effect=stellaSkill4Eff,cooldown=5)
stellaLBEff, stellaLBEff2 = copy.deepcopy(defenseUp), copy.deepcopy(dmgUp)
stellaLBEff.power, stellaLBEff.stat, stellaLBEff2.power, stellaLBEff2.stat = 20, MAGIE, 15, MAGIE
stellaLBFinal = skill("Final stellaire","stellaLB",TYPE_ARMOR,range=AREA_MONO,area=AREA_CIRCLE_4,effect=[stellaLBEff,stellaLBEff2],effPowerPurcent=60,initCooldown=3,cooldown=10,url="https://media.discordapp.net/attachments/927195778517184534/960234772498620426/20220403_194942.gif",description="Durant 3 tours, les dégâts reçu par les alliés sont réduit. À chaque tour, l'effet est donné avec 20% de puissance en moins",emoji=trans.emoji)
stellaLBGuide = effect("{0}".format(stellaLBFinal.name),"stellaLBGuide",turnInit=2,silent=True,replique=stellaLBFinal,emoji='<a:finStel:979889173274185750>')
stellaLB2 = copy.deepcopy(stellaLBFinal)
stellaLB2.effPowerPurcent, stellaLB2.effectOnSelf = 80, stellaLBGuide
stellaLBGuide2 = copy.deepcopy(stellaLBGuide)
stellaLBGuide2.replica = stellaLB2
stellaLB = copy.deepcopy(stellaLBFinal)
stellaLB.id, stellaLB.effPowerPurcent, stellaLB.url, stellaLB.effectOnSelf = "stellaLB", 100, "https://media.discordapp.net/attachments/927195778517184534/960234772926455908/20220403_194702.gif",stellaLBGuide2

basicMobShieltron = skill("Shieltron","genericShieltron",TYPE_PASSIVE,effectOnSelf=shieltron,emoji=shieltron.emoji[0][0])
liuShieltron = copy.deepcopy(basicMobShieltron)
liuShieltron.name, liuShieltron.effectOnSelf.block, liuShieltron.id = "Shieltron Rocheux", 35, "liuShieltron"

# Octo Gazor
octoGazTox = copy.deepcopy(lanceToxEff)
octoGazTox.power = int(octoGazTox.power * 0.6)
octoGazWeap = weapon("Lance-Toxines","octoGazWeap",RANGE_MELEE,AREA_CIRCLE_2,50,75,strength=5,intelligence=5,endurance=5,emoji=lanceToxEff.emoji[0][0],effectOnUse=octoGazTox,ignoreAutoVerif=True)
octoGazSkill1 = skill("Dispersion","octoGazSkill1",TYPE_INDIRECT_DAMAGE,effect=octoGazTox,range=AREA_CIRCLE_4,area=AREA_CONE_3,emoji=lanceToxEff.emoji[0][0],cooldown=5)
octoGazSkill2 = skill("Projection","octoGazSkill2",TYPE_DAMAGE,power=35,knockback=2,area=AREA_LINE_3,range=AREA_CIRCLE_1,effect=octoGazTox,cooldown=2)
octoGazSkill3 = skill("Propagation","octoGazSkill3",TYPE_INDIRECT_DAMAGE,effect=octoGazTox,emoji=lanceToxEff.emoji[0][0],range=AREA_MONO,area=AREA_CIRCLE_3,effPowerPurcent=65,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_CIRCLE_1,octoGazTox])

# Lime Cookie
limeWeapon = weapon("Ballon de voley","noneWeap",RANGE_DIST,AREA_CIRCLE_4,30,80,strength=10,agility=10,endurance=5,ignoreAutoVerif=True)
limeSkill1 = skill("Attaque lobbée","limeSkill1",TYPE_DAMAGE,power=80,cooldown=3,range=AREA_DIST_5,area=AREA_CIRCLE_1)
limeSkill2 = skill("Smash Hit","limeSkill2",TYPE_DAMAGE,power=100,cooldown=3,effect=lightStun,range=AREA_CIRCLE_4)
limeSkill3Eff = effect("Agilité réduite","agilityDown",CHARISMA,agility=-5,turnInit=3,type=TYPE_MALUS)
limeSkill3 = skill("Spike","limeSkill3",TYPE_DAMAGE,power=100,cooldown=3,range=AREA_CIRCLE_4,tpCac=True,area=AREA_CIRCLE_2,areaOnSelf=True,effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_2,limeSkill3Eff])
limeSkill4 = skill("Push","limeSkill4",TYPE_DAMAGE,power=50,knockback=1,range=AREA_CIRCLE_4)
limeSkill5 = skill("Invocation - Mr. Lifesavor","limeSkill5",TYPE_SUMMON,range=AREA_CIRCLE_4,invocation="Mr. Lifesavor",cooldown=5,emoji="<:mrLifeSavor:1009824241954324561>",use=CHARISMA)

# --------------------------------------------------------- Tabl Unique Ennemis ---------------------------------------------------------
tablUniqueEnnemies = [
    octarien("Octo Bouclier",50,350,20,45,45,20,10,50,0,0,octoShieldWeap,5,'<:OctoShield:881587820530139136>',[octaStrans,blindage,isolement,basicMobShieltron],description="Un octarien qui se cache derrière un gros et lourd bouclier",number=2,aspiration=MASCOTTE),
    octarien("Octo Tireur",150,55,50,95,155,35,0,20,0,20,octoBallWeap,3,'<:octoshooter:880151608791539742>',[chargeShot,ultraShot],description="Un tireur sans plus ni moins",number=3,aspiration=OBSERVATEUR),
    octarien("Octo Soigneur",30,100,250,35,15,50,50,25,0,0,octoHeal,4,"<:octohealer:880151652710092901>",[lightAura,cure,firstheal],aspiration=ALTRUISTE,description="Un octarien qui se spcésialise dans ~~passer son tour~~ soigner ses alliés",number=3),
    octarien("Rudinn",175,100,20,55,100,35,35,35,0,15,ruddinweap,6,"<a:rudinn:893246033226760232>",skill=[ultraShot],aspiration=TETE_BRULE,deadIcon='<:defeatrudeen:893246353415757824>',baseLvl=10,number=3),
    octarien("Rudinn Ranger",175,175,20,30,30,125,25,35,0,15,ruddinweap2,8,"<a:rudinnRanger:893248570742956072>",aspiration=POIDS_PLUME,deadIcon='<:defeatrudeen:893246353415757824>',skill=[octaStrans],baseLvl=10,number=3),
    octarien("Aéro-benne",200,50,50,60,150,35,20,20,0,0,flyfishweap,5,'<:flyfish:884757237522907236>',description="Un Salmioche qui s'est passionné pour l'aviation",deadIcon='<:salmonnt:894551663950573639>',aspiration=OBSERVATEUR,baseLvl=10,number=2),
    octarien("Mallus",25,30,20,20,25,200,200,20,0,15,malusWeapon,6,'<:mallus:895824636716130308>',skill=[malusSkill1,malusSkill2,zoneOctoInkRes],aspiration=PREVOYANT,baseLvl=15,number=2),
    octarien("Kralamour",10,50,250,50,0,200,30,30,0,0,kralamWeap,5,'<:kralamour:895443866189176842>',[kralamSkill,kralamSkill2,zoneOctoInkRes],PREVOYANT,baseLvl=15,number=2),
    octarien("Temmie",55,100,55,50,35,30,175,30,15,15,temWeap,4,'<:temmie:894546348324552724>',[temSkill1],deadIcon='<:temmient:894545999996014663>',aspiration=TETE_BRULE,say=temSays,baseLvl=15,number=3),
    octarien("Bob",55,100,55,50,35,30,200,30,15,15,temWeap,4,'<:temmie:894546348324552724>',[temSkill1],deadIcon='<:temmient:894545999996014663>',aspiration=TETE_BRULE,say=bobSays,baseLvl=15),
    octarien("Octo Mage",50,100,30,30,30,20,250,20,10,15,octoMageWeap,5,'<:octomage:897910662758543422>',[flame,courant,rock,storm2,None,None,maitriseElementaire],MAGE,baseLvl=20,number=3,element=ELEMENT_UNIVERSALIS_PREMO),
    octarien("Octo Mage II",50,100,30,30,30,20,250,20,10,15,octoMageWeap,5,'<:octoMage2:907712297013751838>',[fireCircle,waterCircle,earthCircle,airCircle,None,None,maitriseElementaire],MAGE,baseLvl=20,number=3,element=ELEMENT_UNIVERSALIS_PREMO),
    octarien("Zombie",175,200,0,50,70,0,0,50,0,10,ironSword,6,'<:armoredZombie:899993449443491860>',[defi,zombieSkill,None,None,None,None,undead],BERSERK,baseLvl=20,number=2,rez=False),
    octarien("Octo Bombardier",225,125,20,10,150,35,0,35,20,0,octobomberWeap,6,'<:octobomber:902013837123919924>',aspiration=OBSERVATEUR,baseLvl=20,number=2,skill=[octoTentaMissiles,octoBooyahBombCast]),
    octarien("Tentassin",175,125,20,35,30,100,20,45,15,20,tentaWeap,6,'<:octoshoter2:902013858602967052>',aspiration=BERSERK,skill=[octaStrans,ultraShot],baseLvl=15,number=2),
    octarien("Octo Protecteur",0,100,50,50,30,300,20,20,0,0,octoDef,5,"<:octoProtect:883303222255706142>",[inkarmor,zoneOctoInkRes],aspiration=PREVOYANT,description="Un octarien qui pense que les boucliers sont la meilleure défense",baseLvl=5),
    octarien("OctoBOUM",120,-30,10,35,20,0,450,-10,0,0,octoBoumWeap,5,'<:octoboom:884810545457418271>',[explosionCast],MAGE,canMove=False,description="Un octarien qui a placé tous ses points dans ses envies pirotechniques",baseLvl=25,rez=False),
    octarien("Octaling",125,50,75,50,50,75,125,25,0,20,splattershotJR,5,'<:Octaling:866461984018137138>',baseLvl=10,description='Les Octalings ont une arme, aspiration, élément et compétences aléatoire définini au début du combat',number=3),
    octarien("Octarien Volant",200,45,35,120,75,20,0,25,0,35,octoFly,4,'<:octovolant:880151493171363861>',number=3,aspiration=OBSERVATEUR),
    octarien("Octo Soigneur Vétéran",50,50,300,35,40,35,0,25,20,0,veterHealWeap,7,'<:octoHealVet:906302110403010581>',[veterHealSkill1,veterHealSkill2,veterHealSkill3,veterHealSkill4,kralamSkill2],ALTRUISTE,baseLvl=30,number=3),
    octarien("Octo Moine",175,125,30,35,75,75,50,30,0,20,mainLibre,5,'<:octoMonk:907723929882337311>',[airStrike,earthStrike,None,None,None,None,maitriseElementaire],BERSERK,baseLvl=15,number=2,element=ELEMENT_UNIVERSALIS_PREMO),
    octarien("Octo Scientifique",10,25,120,75,35,250,10,30,0,0,octoBoostWeap,7,"<:octoScience:915054617933541386>",[octoBoostSkill1,octoBoostSkill2,octoBoostSkill3,octoBoostSkill4,zoneOctoInkRes],INOVATEUR,number=2),
    octarien("Octo Sniper",250,30,20,100,120,20,15,15,10,20,octoSnipeWeap,7,'<:octotSniper:873118129398624287>',aspiration=OBSERVATEUR,description="Un octarien qui a passé des années à s'entrainer pour rivaliser avec une inkling qui faisait des ravages conséquents parmis les siens",baseLvl=15,skill=[antiArmorShot]),
    octarien("Liu",30,300,155,0,50,20,0,65,0,0,liuWeap,7,'<:liu:908754674449018890>',[liuSkill,inkRes2,liuShieltron,liuMontBreaker,liuAoEShieldSkill,liuLB,liuFurTelCast],PROTECTEUR,GENDER_FEMALE,"La plus sportive de sa fratterie\n\nChaque attaque à l'arme des Soeurs Kitsune applique l'état \"Sous le charme II\" qui diminue légèrement les statistiques de la cible","<:kitsuSisterDead:908756093101015100>",baseLvl=20,say=liuSays,element=ELEMENT_EARTH),
    octarien("Lia",20,50,150,250,30,30,20,30,0,0,liaWeap,7,'<:lia:908754741226520656>',[liaSkill1, liaSkill2,liaSkill,liaCounterSkill,windBal,liaLB,sillage],POIDS_PLUME,GENDER_FEMALE,"La plus rapide et agile de sa fraterie\n\nChaque attaque à l'arme des Soeurs Kitsune applique l'état \"Sous le charme II\" qui diminue légèrement les statistiques de la cible","<:kitsuSisterDead:908756093101015100>",baseLvl=20,say=liaSays,element=ELEMENT_AIR),
    octarien("Lio",20,70,250,75,50,35,80,35,0,0,lioWeap,7,'<:lio:908754690769043546>',[offrRec,lioRez,veterHealSkill2,lioHealZone,offrRav,lioLB,misery],ALTRUISTE,GENDER_FEMALE,"La plus calme et tranquille de sa fraterie\n\nChaque attaque à l'arme des Soeurs Kitsune applique l'état \"Sous le charme II\" qui diminue légèrement les statistiques de la cible","<:kitsuSisterDead:908756093101015100>",baseLvl=20,say=lioSays,element=ELEMENT_WATER),
    octarien("Liz",10,55,135,35,20,35,205,35,20,0,lieWeap,7,'<:lie:908754710121574470>',[pyro,lizBoomCast,lieSkill,lizDotAoE,lizAoE,brasier2,lizLB],MAGE,GENDER_FEMALE,"La plus impulsive de sa fraterie\n\nChaque attaque à l'arme des Soeurs Kitsune applique l'état \"Sous le charme II\" qui diminue légèrement les statistiques de la cible","<:kitsuSisterDead:908756093101015100>",baseLvl=20,say=lizSays,element=ELEMENT_FIRE),
    octarien("Benjamin Hunter",30,100,100,30,50,250,0,35,20,0,hunterWeap,8,'<a:HunterNo:800841356502237225>',[hunterSkill1,hunterSkill2,hunterSkill3,hunterSkill4],IDOLE,GENDER_MALE,deadIcon='<:AutopsyReport:800839396151656469>',baseLvl=15),
    octarien("Octo Invocateur",135,80,45,75,75,45,135,25,0,0,octoInvocWeap,7,'<:octoSummoner:919862854683873331>',[invocCarbunR,invocCarbE,invocCarbSaphir,invocCarbObsi,invocCarbT],baseLvl=20),
    octarien("Citoptère Pal. Cor.",0,200,200,50,50,35,50,45,0,0,clirWeap,8,'<:cliropPal:921910882009759764>',[ironWillSkill,clirHeal,lightAura2,renisurection,basicMobShieltron],VIGILANT,deadIcon='<:cliroOut:921912637103698010>',baseLvl=15,number=2,gender=GENDER_FEMALE),
    octarien("Octaling PomPomGirl",10,70,300,100,45,35,10,20,0,0,octaPomWeapon,7,"<:octaPomPom:921910868097257472>",[octoPomSkill1,octoPomSkill2,octoPomSkill3,octoPomSkill4,zoneOctoInkRes],IDOLE,number=2,gender=GENDER_FEMALE),
    octarien("Citoptère Inf. Cor.",0,50,275,75,100,20,20,35,0,0,clirInfWeap,6,'<:cliroInfirm:921915716435836968>',[lightHeal2,lightBigHealArea,renisurection],ALTRUISTE,baseLvl = 15, deadIcon = '<:cliroOut:921912637103698010>',number=2),
    octarien("OctoSUS",200,75,0,35,50,200,0,35,20,0,octoSusWeap,5,'<:octoSus:932220811828412456>',[octoSusSkill1,octoSusSkill2],BERSERK,deadIcon='<:dead:932243831104102450>', baseLvl = 15, number=3),
    octarien("Lueur informe A",135,150,20,20,50,25,200,50,20,0,unformLightAWeapon,10,'<:aformLight:931881464302284871>',[unformLightASkill1,unformLightASkill2,unformLightASkill3],PROTECTEUR,description="Une lueur instable qui cherche à éliminer tous les éléments autre que Lumière de ce monde. Menace pour tout être vivant",deadIcon='<:empty:866459463568850954>',rez=False,element=[ELEMENT_LIGHT,ELEMENT_LIGHT],baseLvl=30),
    octarien("Ombre informe A",135,150,20,20,50,25,200,50,20,0,unformDarknessAWeapon,10,'<:unformDark:934406341588561941>',[unformDarknessASkill1,unformDarknessASkill2,unformDarknessASkill3],PROTECTEUR,description="Une ombre instable qui cherche à éliminer tous les éléments autre que Ténèbres de ce monde. Menace pour tout être vivant",deadIcon='<:empty:866459463568850954>',rez=False,element=[ELEMENT_DARKNESS,ELEMENT_DARKNESS],baseLvl=30),
    octarien("Ombre informe B",100,80,35,35,50,35,250,20,15,15,unformDarknessBWeapon,10,'<:unformDark:934406341588561941>',[unformDarknessBSkill1,unformDarknessBSkill2,unformDarknessBSkill3],SORCELER,description="Une ombre instable qui cherche à éliminer tous les éléments autre que Ténèbres de ce monde. Menace pour tout être vivant",deadIcon='<:empty:866459463568850954>',rez=False,element=[ELEMENT_DARKNESS,ELEMENT_DARKNESS],baseLvl=30),
    octarien("Octo Gazeur",200,70,10,50,35,200,0,50,35,0,octoGazWeap,6,'<:octogazeur:972160938104979516>',[octoGazSkill1,octoGazSkill2,octoGazSkill3],ATTENTIF,baseLvl=10,element=ELEMENT_DARKNESS,number=2),
    octarien("Lime Cookie",150,80,150,100,70,20,20,25,0,0,limeWeapon,8,"<a:limeCookieRun:1004092989557186570>",[limeSkill1,limeSkill2,limeSkill3,limeSkill4,limeSkill5],MASCOTTE,GENDER_FEMALE,deadIcon="<:limeCookieTripped:1004093087569694790>",baseLvl=5,element=[ELEMENT_SPACE,ELEMENT_AIR])
]

# --------------------------------------------------------- Tabl All Ennemis ---------------------------------------------------------
tablAllEnnemies = []
for ennemi in tablUniqueEnnemies:
    cmpt = 0
    while cmpt < ennemi.number:
        tablAllEnnemies.append(ennemi)
        cmpt += 1

# --------------------------------------------------------- Bosses ---------------------------------------------------------
# Boss spells -------------------
# Spamton
spamSkill1 = skill("A Call For You","spamtomSkill1",TYPE_DAMAGE,0,135,area=AREA_CONE_3,sussess=50,emoji='<:call:892757436203671572>',cooldown=3,message="HOT {0} IN YOUR AREA HAVE A [[Message](https://fr.wikipedia.org/wiki/Message)] FOR [{2}] :")
spamSkill2 = skill("BIG SHOT","spamtomSkill2",TYPE_DAMAGE,0,150,area=AREA_LINE_5,sussess=70,ultimate=True,cooldown=5,message="[[Press F1](https://forums.commentcamarche.net/forum/affich-19023080-press-f1-to-continue-del-to-enter-setup)] FOR HELP :",emoji='<:bigshot:892757453442277417>')
spamSkill3 = skill("Pipis","spamSkill3",TYPE_SUMMON,invocation="Pipis",cooldown=5,say="I'VE ALWAYS BEEN A MAN OF THE [[PIPIS](https://bit.ly/3MErtTo)]. A REAL [[PIPIS](https://bit.ly/3MErtTo)] PERSON!")

# Serena
serenaSpe = skill("Libération","SerenaLibe",TYPE_INDIRECT_DAMAGE,0,200,AREA_MONO,ultimate=True,cooldown=7,area=AREA_ALL_ENEMIES,description="Séréna fait imploser toutes les poudres de fées d'Estialba, infligeant des dégâts en fonction du nombre d'effets \"Poison d'Estialba\" et de leurs durées restantes",emoji=estal.emoji[0][0])
serenaSkill = skill("Propagation","SeranaPropa",TYPE_INDIRECT_DAMAGE,0,0,AREA_MONO,area=AREA_ALL_ENEMIES,cooldown=3,effect=estal,emoji="<:propa2:993801072630046811>",effPowerPurcent=120)
serenaFocal, serenaCloud = copy.deepcopy(focal), copy.deepcopy(poisonus)
serenaFocal.effectOnSelf, serenaFocal.area, serenaFocal.cooldown, serenaCloud.area = None, AREA_CIRCLE_2, serenaFocal.cooldown +2, AREA_CIRCLE_2
serenaSkill2 = skill("Purgation","serenaSkill2",TYPE_INDIRECT_DAMAGE,0,range=AREA_MONO,area=AREA_CIRCLE_3,effect=estal,use=MAGIE,effPowerPurcent=200,emoji='<:purgation:921702426690600960>')
serenaSkill3 = skill("Dispersion","serenaSkill3",TYPE_INDIRECT_DAMAGE,area=AREA_INLINE_3,range=AREA_MONO,effect="me",effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_DONUT_2,"me"],effPowerPurcent=80,cooldown=5)
serenaSkill4 = skill("Charge des tempettes","serenaSkill4",TYPE_DAMAGE,tpCac=True,use=MAGIE,effect="me",effPowerPurcent=50,area=AREA_LINE_2,range=AREA_INLINE_5,replay=True,cooldown=3,power=35)

# Jevil
jevilPassifEffect = effect("I can do anything !","jevilPassiveEffect",silent=True,turnInit=-1,description="Rien n'est plus amusant que le chaos !\n\nLorsque Jevil est dans le combat, tous les combattants recoivent l'effet \"__Confusion__\" qui occulte l'icones des effets dans la liste de ces derniers jusqu'à la fin du combat\n\nÀ chaque début de tour, Jevil donne l'effet \"__Boîte à malice__\" à un certain nombre de cible. Cet effet inflige des dégâts indirect avec une puissance et une zone d'effet aléatoire au début du tour du porteur\nLe nombre d'effets donnés et de cible augmente au fur et à mesure que les PVs de Jevil descendent")
jevilWeap = weapon("Projectiles","jevilWeap",RANGE_DIST,AREA_CIRCLE_4,80,50,ignoreAutoVerif=True,area=AREA_CONE_2,say="CHAOS, CHAOS, CATCH ME IF YOU CAN!",emoji='<:chaos:892857755143127090>',damageOnArmor=1.5,effect=jevilPassifEffect)
jevilSkill1_1 = skill("Pics","jevilSkill1",TYPE_DAMAGE,0,90,area=AREA_LINE_2,sussess=60,emoji='<a:card:892855854712385637>',say="I CAN DO ANYTHING !",cooldown=1,damageOnArmor=1.5)
jevilSkill1_2 = skill("Trèfles","jevilSkill1",TYPE_DAMAGE,0,100,area=AREA_CONE_2,sussess=70,emoji='<a:card:892855854712385637>',say="I CAN DO ANYTHING !",cooldown=1,damageOnArmor=0.8)
jevilSkill1_3 = skill("Coeurs","jevilSkill1",TYPE_DAMAGE,0,50,setAoEDamage=True,area=AREA_DIST_4,range=AREA_MONO,sussess=60,emoji='<a:card:892855854712385637>',say="I CAN DO ANYTHING !",cooldown=2,)
jevilSkill1_4 = skill("Carreau","jevilSkill1",TYPE_DAMAGE,0,80,area=AREA_DIST_3,range=AREA_CIRCLE_2,sussess=100,emoji='<a:card:892855854712385637>',say="I CAN DO ANYTHING !",cooldown=2,damageOnArmor=3)
jevilSkill1 = skill("Joker !","jevilSkill1",TYPE_DAMAGE,0,become=[jevilSkill1_1,jevilSkill1_2,jevilSkill1_3,jevilSkill1_4],emoji='<a:card:892855854712385637>')

jevilSkill2 = skill("Final Chaos","jevilSkill2",TYPE_DAMAGE,0,75,AREA_MONO,setAoEDamage=True,area=AREA_ALL_ENEMIES,percing=100,say="KIDDING ! HERE'S MY FINAL CHAOS !",initCooldown=5,cooldown=4,emoji="<:devilknife:892855875600023592>",damageOnArmor=2)
jevilEff = effect("Confusion","giveup",silent=True,emoji=uniqueEmoji('<a:giveup:902383022354079814>'),turnInit=-1,unclearable=True,description="Confuse confusing confusion")

# Luna (Oh it's will be funny)
lunaWeap = weapon("Épee de l'ombre éternelle","aaa",RANGE_LONG,AREA_CIRCLE_1,35,40,strength=20,agility=20,precision=20,repetition=5,emoji='<:lunaWeap:915358834543968348>',damageOnArmor=1.2,ignoreAutoVerif=True)
lunaInfiniteDarknessStun = effect("Lumière Éternelle","ilianaInfiniteLigthEff",None,type=TYPE_MALUS,stun=True,silent=True,emoji=uniqueEmoji("<:iliEff:929705167853604895>"))

lunaVulne = effect("Vulnérabilité ombrale","lunaVulné",STRENGTH,resistance=-3,turnInit=-1,emoji=vulneEmoji,type=TYPE_MALUS,stackable=True)

lunaSpe = skill("Ténèbres Éternels","InfDarkLaunch",TYPE_DAMAGE,0,235,range=AREA_CIRCLE_7,area=AREA_CIRCLE_7,emoji='<:lunaSecDamage:929705185016692786>',say=["Laissez moi vous montrer un avant goût des Ténèbres Éternels !","Arrête de toujours d'interposer comme ça !","Même toi ne peut pas contrer mes Ténèbres éternellement !","Raah cette lueur ! Cette insuportable lueur !"],description="Inflige des dégâts extrèmes après un tour de chargement",cooldown=99,initCooldown=5,ultimate=True,damageOnArmor=1.2)
lunaInfiniteDarknessShield = effect("Ténèbres Éternels","lunaInfiniteDarknessShield",STRENGTH,agility=-500,overhealth=350,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,replique=lunaSpe,turnInit=99,absolutShield=True,emoji=uniqueEmoji('<:lunaEff:929700784537477150>'))
lunaRepEffect = effect("Cast - Ténèbres Éternels","darkerYetDarker3",replique=lunaSpe,turnInit=2,silent=True,emoji=uniqueEmoji("<a:lu:916575004492169226>"))
lunaSpeCast = skill("Ténèbres Éternels","lunaInfDarkCast",TYPE_DAMAGE,0,0,emoji='<:lunaSecDamage:929705185016692786>',range=AREA_CIRCLE_7,area=AREA_CIRCLE_7,effectOnSelf=lunaRepEffect,say="Ok ça suffit ! Voyons voir comment vous tiendrez face à ça...",message="Luna concentre les Ténèbres environants...",cooldown=lunaSpe.cooldown,initCooldown=lunaSpe.initCooldown,ultimate=lunaSpe.ultimate)
lunaSkill = copy.deepcopy(soupledown)
lunaSkill.power, lunaSkill.onArmor, lunaSkill.cooldown = 180, 1.3, 4
lunaSkill2 = skill("Frappes des Ténèbres","lunaSkill2",TYPE_DAMAGE,0,150,AREA_CIRCLE_2,repetition=3,cooldown=5,initCooldown=2,damageOnArmor=1.3,emoji='<:lunaTb:932444874073063434>',say=["Je pense pas que tu va pouvoir prendre celui-ci sans broncher.","Tu as des healers non ? Donnons leur un peu de boulot !"],description="Inflige de lourd dégâts à une cible unique")
lunaSkill4Eff = copy.deepcopy(innerdarknessEff)
lunaSkill4Eff.stat,lunaSkill4Eff.power , lunaSkill4Eff.id, lunaSkill4Eff.emoji = STRENGTH, 40, "lunaSkill4Eff", uniqueEmoji('<:lunaIndi:932447879786823730>')
lunaSkill4EffAlt = copy.deepcopy(lunaSkill4Eff)
lunaSkill4EffAlt.power, lunaSkill4EffAlt.area, lunaSkill4EffAlt.id = 75 , AREA_MONO, "lunaSkill4Eff2"
lunaSkill4_1 = skill("Convertion rapprochée",'lunaSkill4',TYPE_INDIRECT_DAMAGE,0,range=AREA_MONO,area=AREA_CIRCLE_2,effect=lunaSkill4EffAlt,cooldown=3,emoji=lunaSkill4Eff.emoji[0][0],say=['Vous tenez tant à voir les Ténèbres de plus près ? Voilà pour vous !','Votre Lumière ne vous protègera pas éternellement.'],description="Donne un effet de dégâts indirect monocible aux ennemis proches")
lunaSkill4_2 = skill("Convertion externe",'lunaSkill4',TYPE_INDIRECT_DAMAGE,0,range=AREA_MONO,area=AREA_DIST_7,effect=lunaSkill4Eff,cooldown=3,emoji=lunaSkill4Eff.emoji[0][0],say=["C'est pas parceque vous restez loin que vous serez épargné !","Votre Lumière sucombera à mes Ténèbres."],description="Inflige un effet de dégâts indirect en zone aux ennemis éloignés")
lunaSkill4 = skill("Convertion","lunaSkill4",TYPE_INDIRECT_DAMAGE,0,range=AREA_CIRCLE_7,use=STRENGTH,say="Votre Lumière ne vous protègera pas éternellement !",emoji=lunaSkill4Eff.emoji[0][0],become=[lunaSkill4_1,lunaSkill4_2])
lunaSkill5_1 = skill("Reverse roundhouse-kick","lunaSkill5",TYPE_DAMAGE,0,100,AREA_CIRCLE_1,area=AREA_ARC_1,emoji='<:luna4inOne:919260128698589184>',damageOnArmor=2,description='Inflige des dégâts en zone à un ennemi au corps à corps')
lunaSkill5_2 = skill("Side-kick fouetté","lunaSkill5",TYPE_DAMAGE,0,135,AREA_CIRCLE_1,emoji='<:luna4inOne:919260128698589184>',say="Hmf !",damageOnArmor=3,description='Inflige des dégâts à une cible unique au corps à corps\nDégâts triplé sur de l\'armure')
lunaSkill5_3_eff = effect("Destabilisé","lunaSkill5_3Eff",type=TYPE_MALUS,emoji='<:stun:882597448898474024>',stun=True)
lunaSkill5_3 = skill("Sweeping into Backflip","lunaSkill5",TYPE_DAMAGE,0,80,AREA_CIRCLE_1,repetition=2,effect=lunaSkill5_3_eff,knockback=1,emoji='<:luna4inOne:919260128698589184>',say="C'est que tu es colant toi !",description='Inflige des dégâts, étourdit pendant un tour et repousse un ennemi au corps à corps')
lunaSkill5_4 = skill("Double High roundhouse-kick into Side-kick","lunaSkill5",TYPE_DAMAGE,0,40,AREA_CIRCLE_1,repetition=3,knockback=3,emoji='<:luna4inOne:919260128698589184>',say="Hé vous derrière ! Cadeau !",damageOnArmor=2,description='Inflige des dégats et repousse de 3 cases un ennemi au corps à corps')
lunaSkill6 = skill("Vitesse ombrale","lunaSkill6",TYPE_DAMAGE,0,50,AREA_INLINE_4,emoji='<:lunaDash:932286143884566528>',cooldown=2,replay=True,tpCac=True,sussess=200,description='Se téléporte au corps à corps d\'un ennemi et vous permet de rejouer votre tour')
lunaSkill7 = skill("Ultimawashi","lunaSkill7",TYPE_DAMAGE,0,150,AREA_CIRCLE_1,cooldown=3,knockback=10,sussess=200,emoji='<:ultimawashi:932378739327787078>',description="Inflige de lourd dégâts et repousse violament un ennemi au corps à corps")
lunaQuickFightEff = effect('Enchaînement',"lunaQuickFight",emoji=uniqueEmoji('<:qqLuna:932318030380302386>'))
lunaSkill5Base = skill("Corps à corps","lunaSkill5",TYPE_DAMAGE,0,0,AREA_CIRCLE_1,description="Cette compétence peut avoir 4 effets différents, sélectionné de manière aléatoire",emoji='<:luna4inOne:919260128698589184>',become=[lunaSkill5_1,lunaSkill5_2,lunaSkill5_3,lunaSkill5_4])

# Clemence Pos Special skills
clemPosWeapBleeding = effect("Hémorragie","clemPosBleeding",MAGIE,power=35,emoji=bleeding.emoji,trigger=TRIGGER_START_OF_TURN,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,stackable=True,description="Un effet de dégâts sur la durée. Clémence possédé récupère 3% des dégâts infligés par cet effet en point de jauge de sang")
clemWeapon = weapon("Rapière en argent lunaire","clemenceWeapon",RANGE_DIST,AREA_CIRCLE_2,150,100,ignoreAutoVerif=True,use=MAGIE,effectOnUse=clemPosWeapBleeding,effect=clemBloodJauge,damageOnArmor=2,magie=50,endurance=20,emoji='<:clemWeap:915358467773063208>')
clemStunEffect = effect("Thrombophilie","clemStun",stun=True,emoji=uniqueEmoji("<:stun:882597448898474024>"),turnInit=3,type=TYPE_MALUS)
aliceStunEffect = effect("Hémophilie","aliceStun",stun=True,emoji=uniqueEmoji("<:stun:882597448898474024>"),turnInit=3,type=TYPE_MALUS)
clemSkill1 = skill("Rune - Lune de Sang","clemSkill1",TYPE_DAMAGE,0,power=170,range=AREA_MONO,area=AREA_CIRCLE_3,emoji='<a:clemSkill1:901147227588812890>',cooldown=2,initCooldown=2,use=MAGIE,damageOnArmor=2,say="Si vous tenez tant que ça à me coller aux basques c'est pour que je vous bute plus vite c'est ça ?")
clemSkill2 = skill("Sort - Chiroptera perniciosius","clemSkill2",TYPE_DAMAGE,0,320,AREA_CIRCLE_2,cooldown=4,emoji='<a:clemSkill4:901150027706142780>',use=MAGIE,say=["Tu tombe bien toi, j'avais besoin d'un mannequin.","Il est temps que quelqu'un te remette à ta place.","Tu penses vraiment que tu seras capable de tout prendre sans brocher ?"],damageOnArmor=5,effect=clemPosWeapBleeding)
clemSilence = copy.deepcopy(silenceEff)
clemSilence.turnInit = 2
clemUltLauch = skill("Ultima Sanguinis Flurry","clemUlt",TYPE_DAMAGE,0,200,AREA_MONO,setAoEDamage=True,area=AREA_CIRCLE_7,emoji='<:clemMemento:902222089472327760>',say=["Vous avez suffisamant résisté comme ça !","`Soupir` Je me donne trop de peine pour vous."],sussess=666,cooldown=9,ultimate=True,description="Au premier tour, consomme tous les **Points de sang** de la Jauge de Sang, sauf 1, pour obtenir un bouclier absolu, dont la puissance dépend du nombre de points consommés\nAu second tour, si ce bouclier est toujours présent, Clémence gagne 50% de dégâts infligés. Consomme la jauge de sang",use=MAGIE,effectOnSelf=clemSilence)
clemultCastEffect = effect("Cast - Ultima Sanguinis Flurry","clemUltEff",replique=clemUltLauch,turnInit=2,silent=True,emoji=dangerEm)
clemUltShield = effect("Bouclier sanguin","clemShield",MAGIE,overhealth=1,emoji=uniqueEmoji("<:clemMemento2:902222663806775428>"),turnInit=2,absolutShield=True)
clemUltCast = skill("Ultima Sanguinis Flurry","clemUltCast",TYPE_ARMOR,0,range=AREA_MONO,emoji="<:clemMemento2:902222663806775428>",effect=clemUltShield,say="Très bien.",effectOnSelf=clemultCastEffect,ultimate=True,cooldown=10)
clemSkill3 = skill("Rune - Demi-Lune","clemSkill3",TYPE_DAMAGE,0,220,AREA_CIRCLE_3,area=AREA_ARC_2,cooldown=2,use=MAGIE,emoji='<a:clemSkill3:914759077551308844>',damageOnArmor=3)
clemSkill4 = skill("Sort - Chiroptera vastare","clemSkill4",TYPE_DAMAGE,0,80,AREA_MONO,area=AREA_DIST_7,cooldown=4,use=MAGIE,say=["Vous pensez que vous êtes à l'abri là bas ?","Vous en faites pas, je vous ai pas oublié."],emoji='<a:clemSkill4:914756335860596737>',setAoEDamage=True,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_CIRCLE_2,clemPosWeapBleeding],effPowerPurcent=50,ultimate=True)
clemSkill5 = skill("Sort - Tempus Fugit",'clemSkill5',TYPE_DAMAGE,0,50,use=MAGIE,cooldown=2,damageOnArmor=10,replay=True,effect=clemPosWeapBleeding,effPowerPurcent=20,say=["J'ai pas le temps pour vos conneries.","On va un peu accélrer la cadence !","Je commence sérieusement à me faire chier, qu'on en finisse."],emoji='<:TemposFigit:931703850447024138>')
clemSkill6 = skill("Lance de sang",'clemSkill6',TYPE_DAMAGE,0,100,AREA_DIST_5,area=AREA_CIRCLE_1,use=MAGIE,cooldown=4,emoji='<:bloodSpear:931703831245488128>',effect=clemPosWeapBleeding,effPowerPurcent=40)

clemBJcost = {"clemSkill1":30,"clemSkill2":35,"clemUlt":90,"clemSkill3":30,"clemSkill4":30,"aliceSkill1":15,"aliceSkill2":20,"aliceSkill3":22,"aliceSkill4":20,"aliceRez":25,"aliceRez+":150,"clemSkill5":10,"clemSkill5":30}

# The Giant Ennemi Spider
TGESWeap = weapon("noneWeap","TheGiantEnemySpiderWeapon",RANGE_DIST,AREA_CIRCLE_1,0,0,0,resistance=50)
TGESSkill1 = skill("Projectile","TheGiantEnemySpiderSkill1",TYPE_DAMAGE,0,int(GESLskill.power*1.5))

# Matt from WiiSport
mattWeapon = weapon("Direct !","mattWeapon",RANGE_DIST,AREA_CIRCLE_1,33,70,repetition=3,emoji='<:boxe:922064460326244384>')
mattSkill1 = skill("Home Run !","mattSkill1",TYPE_DAMAGE,0,100,AREA_CIRCLE_1,cooldown=5,knockback=5,description="Quel magnifique coup de batte !",emoji='<:homerun:922064424708239360>')
mattSkill2 = skill("Tir à trois points","mattSkill2",TYPE_DAMAGE,0,80,AREA_DIST_5,cooldown=3,description="Quel tir ! Qui aurait cru qu'il ferait un panier d'ici ?",emoji='<:basket:922064483688513567>')
mattSkill3 = skill("Strike !","mattSkill3",TYPE_DAMAGE,0,120,AREA_CIRCLE_1,area=AREA_LINE_6,cooldown=3,description="Non vous pouvez pas appuyer sur A pour passer la cinématique",emoji='<:bowling:922064440201969724>')
mattSkill4Eff = effect("Gardé","matt(en)Garde",STRENGTH,power=20,lvl=99,onDeclancher=True,immunity=True,description="Une vision accru vous permet de contrer les dégâts et de contre attaquer !")
mattSkill4 = skill("Garde","mattSkill4",TYPE_DAMAGE,0,cooldown=5,range=AREA_CIRCLE_1,power=0,effectOnSelf=mattSkill4Eff)

# Kiku
kikuRaiseEff = effect("Mors Vita Est","kikuBossRaiseEff",power=20,type=TYPE_MALUS,trigger=TRIGGER_DEATH,turnInit=-1,description="\n__Sur les vivants :__\nAugmente les dégâts reçus de **{0}%**, qui augmente de 20% à chaque de tour de table\nLorsque le porteur est vaincu, celui-ci est immédiatement réanimé avec **75%** de ses PVs max et ces derniers sont augmenté d'un pourcentage équivalant à l'augmentation de dégâts\n\n__Sur les morts, en début de combat :__\nOctroi <:un:984241071397670912> __Cadeau de la Non-Vie__\n\nAugmente les dégâts infligés d'une valeur égale à la augmentation de dégâts jusqu'à la fin du combat lors de son déclanchement\nL'augmentation de dégâts est capée à 200%\nSi l'effet est toujours actif au tour **16**, le porteur est immédiatement exécuté",emoji='<:mortVitaEst:916279706351968296>')
kikuUnlifeGift = effect("Cadeau de la non-vie","kikuUnlifeGift",emoji='<:unlifeGift:984241071397670912>',power=10,turnInit=-1,unclearable=True,description="Augmente les dégâts infligés de 10% multiplié par le nombre de tour de table actuel\nRéduit les dégâts subis de 5% multiplié par le nombre de tour de table actuel (maximum 80%)")
kikuMechExplain = effect("Fée de l'Au-Dela","kikuMechExplain",turnInit=-1,unclearable=True,emoji='<:mortVitaEst:916279706351968296>',silent=True,description="Octroi l'effet <:mortVitaEst:916279706351968296> __Mors Vita Est__ à tous les combattants en début de combat",callOnTrigger=kikuRaiseEff)
kikuBossWeap = weapon("Energie Vitale","kikuWeap",RANGE_LONG,AREA_CIRCLE_5,66,60,0,magie=10,endurance=10,use=MAGIE,effect=kikuMechExplain,ignoreAutoVerif=True)
kikuTerraFerrum, kikuAquaFerrum, kikuIgnisFerrum, kikuAerFerrum = copy.deepcopy(mudlame), copy.deepcopy(waterlame), copy.deepcopy(firelame), copy.deepcopy(airlame)
kikuTerraFerrum.use = kikuAquaFerrum.use = kikuIgnisFerrum.use = kikuAerFerrum.use = MAGIE
kikuTerraFerrum.id = kikuAquaFerrum.id = kikuIgnisFerrum.id = kikuAerFerrum.id = "kikuUltimaFerrum"
kikuTerraFerrum.cooldown = kikuAquaFerrum.cooldown = kikuIgnisFerrum.cooldown = kikuAerFerrum.cooldown = 2
kikuUltimaFerrum = skill('UltimaFerrum',"kikuUltimaFerrum",TYPE_DAMAGE,0,0,use=MAGIE,become=[kikuTerraFerrum, kikuAquaFerrum, kikuIgnisFerrum, kikuAerFerrum],emoji='<:kikuEtFerrum:922065497460203570>')
kikuSkill2 = skill("Ultra Voca","kikuSkill2",TYPE_DAMAGE,power=65,area=AREA_CIRCLE_2,range=AREA_DONUT_7,cooldown=4,description="Inflige des dégâts à un groupe d'ennemi éloigné\nSi la cible principale n'a pas encore été réanimée, la puissance est doublée")
kikuSkill3 = skill("Cercle des enfers","kikuSkill3",TYPE_DAMAGE,power=75,setAoEDamage=True,range=AREA_MONO,area=AREA_ALL_ENEMIES,cooldown=7,effectAroundCaster=[TYPE_DAMAGE,AREA_CIRCLE_3,50])

# Akira H.
akikiSkillRageBonus = [1,2,0.5,5]
akikiWeap = weapon("Faux Haineuse","akikiWeap",range=RANGE_DIST,effectiveRange=AREA_CIRCLE_1,power=120,sussess=70,strength=25,endurance=25,emoji=fauc.emoji,area=AREA_ARC_1,ignoreAutoVerif=True)
akikiSkill3 = skill("Massacre","akikiSkill3",TYPE_DAMAGE,0,power=50,range=AREA_MONO,area=AREA_ALL_ENEMIES,sussess=80,cooldown=7)
akikiSkill4 = skill("Intolérance","akikiSkill4",TYPE_DAMAGE,0,power=120,range=AREA_CIRCLE_3,area=AREA_LINE_2,cooldown=7)

akikiSkill1Eff = effect("Rage Croissante","akikiRageDmgBuff",turnInit=-1,unclearable=True,emoji=dmgUp.emoji,power=50)
akikiSkill1 = skill("Rage Croissante","akikiSkill1",TYPE_PASSIVE,effectOnSelf=akikiSkill1Eff,emoji=akikiSkill1Eff.emoji[0][0],description="Accroie les dégâts directs infligés par Akira au fur et à mesure que ses PVs diminuent, jusqu'à **+{0}%** avec 0.1% de PV restants".format(akikiSkill1Eff.power))
akikiSkill2_1_2 = skill("Destruction Explosive","akikiSkill2_1",TYPE_DAMAGE,emoji='<:akiTankStack:1007050856748818464>',power=500,range=AREA_CIRCLE_4,tpCac=True,cooldown=5,area=AREA_CIRCLE_1,description="Au premier tour, Akira marque un ennemi puis il inflige au second tour d'énormes dégâts à l'ennemi marqué et ceux alentours. La puissance est divisée par le nombre d'ennemi ayant une aspiration de mêlée dans la zone d'effet")
akikiSkill2_mark = effect("Cible : Destruction Explosive","akikiSkill2_mark",type=TYPE_MALUS,emoji='<:akiTankStack:1007050856748818464>')
akikiSkill2_1_cast = effect("Cast - {replicaName}","akikiSkill2_1_cast",silent=True,turnInit=2,replique=akikiSkill2_1_2,emoji='<:akiTankStack:1007050856748818464>')
akikiSkill2_1_1 = copy.deepcopy(akikiSkill2_1_2)
akikiSkill2_1_1.id, akikiSkill2_1_1.power, akikiSkill2_1_1.tpCac, akikiSkill2_1_1.effectOnSelf, akikiSkill2_1_1.type, akikiSkill2_1_1.effect, akikiSkill2_1_1.area = "akikiSkill2", 0, False, akikiSkill2_1_cast,TYPE_MALUS, [akikiSkill2_mark], AREA_MONO
akikiSkill2_2 = skill("Destruction Concentrique","akikiSkill2",TYPE_DAMAGE,range=AREA_CIRCLE_3,power=350,cooldown=5,area=AREA_CIRCLE_1,emoji='<:akiTB:1007050875451220059>')

akikiSkill3_1_1 = skill("Frappe Enragée","akikiSkill3_1",TYPE_DAMAGE,power=400,cooldown=5,emoji='<:akiStack:1007050822338748466>',area=AREA_CIRCLE_3,range=AREA_DONUT_5,tpCac=True,description="Akira marque un ennemi au premier tour puis inflige de lourds dégâts à l'ennemi marqué et ceux aux alentours.\nLa puissance est divisée par le nombre d'ennemi dans la zone d'effet.")
akikiSkill3_1_cast = effect("Cast - {replicaName}","akikiSkill3_1_cast",silent=True,turnInit=2,replique=akikiSkill3_1_1,emoji='<:akiStack:1007050822338748466>')
akikiSkill3_1_mark = effect("Cible : Frappe Enragée","akikiSkill3_1_mark",type=TYPE_MALUS,emoji='<:akiStack:1007050822338748466>')
akikiSkill3_1_2 = copy.deepcopy(akikiSkill3_1_1)
akikiSkill3_1_2.id, akikiSkill3_1_2.power, akikiSkill3_1_2.tpCac, akikiSkill3_1_2.effectOnSelf, akikiSkill3_1_2.type, akikiSkill3_1_2.area, akikiSkill3_1_2.effect = 'akikiSkill3', 0, False, akikiSkill3_1_cast,TYPE_MALUS, AREA_MONO, [akikiSkill3_1_mark]
akikiSkill3_2_1 = skill("Frappe Haineuse","akikiSkill3_2",TYPE_DAMAGE,power=80,cooldown=5,area=AREA_CIRCLE_1,emoji='<:akiAway:1007050839514435584>',range=AREA_DONUT_5,description="Marque 3 ennemis au premier tour puis inflige au second tour des dégâts à tous les ennemis marquées et ceux autour d'eux. Chaque attaque augmente les dégâts reçus des ennemis affecté, augmentant aussi ceux subis par les ennemis prenant plusieurs fois des dégâts par cette attaque")
akikiSkill3_2_cast = effect("Cast - {replicaName}","akikiSkill3_2_cast",silent=True,turnInit=2,replique=akikiSkill3_2_1,emoji='<:akiAway:1007050839514435584>')
akikiSkill3_2_mark = effect("Cible : Frappe Haineuse","akikiSkill3_2_mark",type=TYPE_MALUS,emoji='<:akiAway:1007050839514435584>')
akikiSkill3_2_2 = copy.deepcopy(akikiSkill3_2_1)
akikiSkill3_2_2.id, akikiSkill3_1_2.power, akikiSkill3_1_2.type, akikiSkill3_1_2.effect, akikiSkill3_1_2.effectOnSelf, akikiSkill3_1_2.area = 'akikiSkill3', 0,TYPE_MALUS, [akikiSkill3_2_mark], akikiSkill3_2_cast, AREA_RANDOMENNEMI_3

akikiEnrageLaunch = skill("En-Rage","akikiEnrageLaunch",TYPE_DAMAGE,0,100,range=AREA_MONO,ultimate=True,execution=True,area=AREA_ALL_ENEMIES,sussess=500,description="Cette compétence exécute tous les ennemis encore vivants.\nCette compétence est forcément utilisée lorsque les PVs restants sont inférieurs à **20%** des PVmax".format(akikiSkillRageBonus[3]),initCooldown=99,cooldown=99)
akikiEnrageRepEff1 = effect("Cast - Rage (1 tour !)","akikiEnrageRepEff1",turnInit=2,silent=True,replique=akikiEnrageLaunch)
akikiEnrageCast1 = copy.deepcopy(akikiEnrageLaunch)
akikiEnrageCast1.id, akikiEnrageCast1.power, akikiEnrageCast1.effectOnSelf, akikiEnrageCast1.execution = "akikiEnrageCast1", 0, akikiEnrageRepEff1, False
akikiEnrageRepEff2 = copy.deepcopy(akikiEnrageRepEff1)
akikiEnrageRepEff2.name, akikiEnrageRepEff2.id, akikiEnrageRepEff2.replica = "Cast - Rage (2 tours)", "akikiEnrageRepEff2", akikiEnrageCast1
akikiEnrageCastInit = copy.deepcopy(akikiEnrageLaunch)
akikiEnrageCastInit.id, akikiEnrageCastInit.power, akikiEnrageCastInit.effectOnSelf = "akikiEnrageCastInit", 0, akikiEnrageRepEff2

unformBossWeapon = weapon("Arme aforme","unformBossWeap",RANGE_DIST,AREA_CIRCLE_1,150,80,ignoreAutoVerif=True)
unformBossSkill1 = skill("Distorsion Dimentionelle","unformBossSkill1",TYPE_DAMAGE,power=250,range=AREA_CIRCLE_1,cooldown=7,use=MAGIE)
unformBossSkill2Eff = copy.deepcopy(dmgUp)
unformBossSkill2Eff.power = 50
unformBossSKill2 = skill("Anéantissement accéléré","unformBossSKill2",TYPE_BOOST,range=AREA_MONO,area=AREA_CIRCLE_3,effect=unformBossSkill2Eff,cooldown=5)
unformBossSkill3 = skill("Pulsion spaciale","unformBossSkill3",TYPE_HEAL,power=250,use=MAGIE,range=AREA_MONO,area=AREA_CIRCLE_5,cooldown=5)

unformBoss = octarien("Aformité incarnée",300,250,200,50,50,200,350,25,15,0,unformBossWeapon,35,'<:uShadow:938530004319477821>',[unformBossSkill1,unformBossSKill2,unformBossSkill3],description="Un leader de l'assaut des aformités, qui cherchent à détruire le multivers",deadIcon='<:empty:866459463568850954>')

# Iliana Ex.
ILIREGENPOWER = 40
iliExWeapEff = effect("Conviction de la Lumière","iliExPasRegenEff",CHARISMA,turnInit=-1,unclearable=True,block=35,emoji='<:ilianaStans:969819202032664596>',description="Accorde à Iliana Ex. 35% de blocage")
iliExWeapon = weapon("Epée et Bouclier de la Lumière","iliExWeap",RANGE_DIST,AREA_CIRCLE_1,80,100,effect=iliExWeapEff,emoji='<:iliShield:975785889512976434>',ignoreAutoVerif=True,use=CHARISMA)
iliExSkill1Eff = effect("Flashé","iliExSkill1Eff",CHARISMA,precision=-15,power=30,lvl=2,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,description="Un fort flash lumineux à réduit votre visibilité et vous a fait mal aux yeux",emoji='<:MyEyes:784226383018328115>')
iliExSkill1 = skill("Flash","iliExSkill1",TYPE_INDIRECT_DAMAGE,cooldown=3,area=AREA_CIRCLE_4,range=AREA_MONO,effect=iliExSkill1Eff,emoji='<:flash:977025336518799420>',effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER])
iliExSkill3 = skill("Vague de Lumière","iliExSkill3",TYPE_DAMAGE,power=80,area=AREA_CONE_2,use=CHARISMA,cooldown=4,range=AREA_CIRCLE_1,effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER])
iliExSkill4 = skill("Vitesse Lumière","iliExSkill4",TYPE_DAMAGE,tpCac=True,cooldown=3,replay=True,power=35,use=CHARISMA)
iliExSkill5Eff = copy.deepcopy(defenseUp)
iliExSkill5Eff.power=95
iliExSKill5 = skill("Lumière Eternelle","iliExLb",TYPE_ARMOR,cooldown=7,effect=iliExSkill5Eff,range=AREA_MONO,emoji=trans.emoji)
iliExSkill6Eff1 = effect("Etourdissement","iliExSkill6EffStun",type=TYPE_MALUS,emoji="<:stun:882597448898474024>",stun=True)
iliExSkill6Eff2 = effect("Bouclier Dressé","iliExSkill6EffBck",block=15,emoji='<:shieltron:971787905758560267>')
iliExSkill6 = skill("Fragmentation","iliExSkill6",TYPE_DAMAGE,use=CHARISMA,power=75,repetition=3,percing=15,tpCac=True,range=AREA_INLINE_3,effect=iliExSkill6Eff1,effectOnSelf=iliExSkill6Eff2,description="Iliana bash violament un ennemi avant de lui assigner plusieurs coups d'épée\nLe choc initial étoudit la cible tout en augmentant le taux de blocage d'Iliana",cooldown=4,effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER])
iliExSkill2 = skill("Révolution de Lumière","iliExSkill2",TYPE_DAMAGE,power=100,range=AREA_MONO,area=AREA_CIRCLE_2,sussess=101,cooldown=3,effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER],use=CHARISMA)

iliExSay = says(start="Je pense que ça devrait suffire... Je pense pouvoir vous donner suffisamant de fil à retordre tout en vous laissant une chance comme ça, bon courage !",onKill='Désolée si tu as du mal à voir pendant quelques temps',reactBigRaiseEnnemy="Ah, contente de voir que ce combat risque d'être un peu moins à sens unique",redWinAlive="Une autre fois peut-être",redLoose="Hé bah... Je dois avouer que vous vous débrouillez pas trop mal")

# Kitsunes elem eff
earthKitEff = effect("Energie Téllurique","earthKitEff",turnInit=5,emoji='<:earth:918212824805801984>')

kitsuneExCharmEff = effect("Charme exalté","kitsuneExCharmEff",CHARISMA,strength=-3,magie=-3,charisma=-3,intelligence=-3,precision=-3,agility=-3,turnInit=3,description="Les compétences magiques des kitsunes réduisent peut à peut la concentration de leurs adversaires",emoji='<:charmeR:908793574437584956>')

# Tabl Boss ----------------------------------------------------
tablBoss = [
    octarien("[[Spamton Neo](https://deltarune.fandom.com/wiki/Spamton)]",435,200,100,45,45,200,200,30,33,15,bigshot,45,'<a:spamton:892749040205316138>',skill=[spamSkill1,spamSkill2,spamSkill3],description="NOW IT'S YOUR CHANCE TO BE A [Big shot] !",deadIcon='<:spamblocked:892750635315912746>',oneVAll=True,say=spamtonSays,element=ELEMENT_DARKNESS),
    octarien("Jevil",450,200,100,60,75,120,120,10,25,15,jevilWeap,50,'<a:CHAOS:762276118224961556>',[chaos,jevilSkill1,jevilSkill2],description="I CAN DO ANYTHING !",deadIcon='<:chaosnt:892857736642064455>',oneVAll=True,say=jevilSays,element=ELEMENT_DARKNESS),
    octarien("Séréna",50,220,-50,70,50,50,350,60,0,15,armilame,10,'<:serena:897912402354511894>',[serenaCloud,serenaSkill,serenaSpe,serenaSkill2,serenaFocal,serenaSkill3,serenaSkill4],SORCELER,GENDER_FEMALE,rez=False,deadIcon='<:flowernt:894550324705120266>'),
    octarien("Luna ex.",550,85,80,185,75,80,0,25,35,0,lunaWeap,50,'<:luna:909047362868105227>',[lunaSpeCast,lunaSkill,lunaSkill5Base,lunaSkill2,lunaSkill4,lunaSkill6,lunaSkill7],POIDS_PLUME,GENDER_FEMALE,lunaDesc,'<:spIka:866465882540605470>',True,say=lunaBossSays,element=ELEMENT_DARKNESS),
    octarien("OctoTour",0,350,0,0,0,0,0,50,0,0,octoTour,12,'<:tower:905169617163538442>',[octoTourSkill],PROTECTEUR,canMove=False,rez=False,description="Une tour de siège. Tant qu'elle est en vie, tous les dégâts directs reçu par ses alliés lui sont redirigés"),
    octarien("Clémence pos.",100,165,50,50,80,150,550,35,20,0,clemWeapon,50,'<a:clemPos:914709222116175922>',[clemSkill1,clemSkill2,clemUltCast,clemSkill3,clemSkill4,clemSkill5,clemSkill6],MAGE,GENDER_FEMALE,"Durant l'une de ses aventures, Clémence a commis l'erreur de baisser sa garde, et une entité malveillante en a profiter pour se loger dans son esprit, perturbant sa vision de la réalitée et manipulant ses émotions",oneVAll=True,deadIcon='<:clemence:908902579554111549>',say=clemPosSays,element=ELEMENT_DARKNESS),
    octarien("The Giant Enemy Spider",280,280,0,80,100,50,280,70,10,20,TGESWeap,50,'<:TGES:917302938785968148>',[TGESSkill1],description="En début de combat, invoque 8 __\"Patte de The Giant Enemy Spider\"__ autour de lui",oneVAll=True),
    octarien("Matt",450,120,100,100,100,100,0,35,20,0,mattWeapon,50,'<:matt:922064304793059340>',[mattSkill1,mattSkill2,mattSkill3,mattSkill4],BERSERK,GENDER_MALE,"L'ultime adversaire. Dans les jeux Wii Sports en tous cas",'<:matt:922064304793059340>',True),
    octarien("Kiku",0,100,50,120,100,5,250,25,35,0,kikuBossWeap,12,'<:kiku:962082466368213043>',[undead,kikuUltimaFerrum,kikuSkill2,kikuSkill3,corruptBecon],gender=GENDER_FEMALE,deadIcon ='<:kiku:962082466368213043>',baseLvl=15,rez=False,element=ELEMENT_EARTH),
    octarien("Akira H.",450,120,80,50,120,100,100,30,0,10,akikiWeap,50,'<:akiraH:1007049315056881704>',[akikiSkill1,akikiSkill2_1_1,akikiSkill2_2,akikiSkill3_1_2,akikiSkill3_2_2,akikiSkill4,akikiEnrageCastInit],BERSERK,GENDER_MALE,description="Bah bravo, vous avez réussi à le mettre en colère. Maintenant battez vous pour votre dignité ou fuyez pour votre vie.",deadIcon='<:spTako:866465864399323167>',oneVAll=True,baseLvl=15,element=ELEMENT_DARKNESS),
    octarien("Iliana ex.",10,100,400,50,100,100,15,80,35,15,iliExWeapon,50,'<:Iliana:926425844056985640>',[iliExSkill1,iliExSkill2,iliExSkill3,iliExSkill4,iliExSKill5,iliExSkill6],VIGILANT,GENDER_FEMALE,"Voyant que vous aviez du mal à trouver un adveraire à votre taille, Iliana a décidé de se confronter à vous en utilisant 1% de sa vrai puissance",'<:oci:930481536564879370>',True,baseLvl=25,element=[ELEMENT_LIGHT,ELEMENT_LIGHT],say=iliExSay),
    octarien("Stella",0,100,70,80,50,50,250,20,20,20,stellaWeap,10,'<:stella:958786101940736061>',[stellaSkill1,stellaSkill2,stellaSkill3,stellaSkill4,stellaLB,solarEruption],IDOLE,GENDER_FEMALE,"Représentation astrale du Soleil, Stella aime pas qu'on lui fasse de l'ombre et a un léger complexe de supporiorité\nSa seule présence suffit à réchauffer l'ambiance et fait gagner quelques degrés de luminosité",'<:spIka:866465882540605470>',baseLvl=25,element=[ELEMENT_SPACE,ELEMENT_LIGHT])
]

for en in tablBoss:
    en.baseLvl = 15

tablBossPlus = [unformBoss,
]
# ====================================== Raid Boss ======================================
nookWeapon = weapon("Dettes","nookWeapon",RANGE_DIST,AREA_CIRCLE_1,120,65,area=AREA_ARC_1,ignoreAutoVerif=True)
nookSkill1 = skill("Fissure temporelle","nookSkill1",TYPE_DAMAGE,0,135,range=AREA_MONO,area=AREA_ALL_ENEMIES,sussess=80,initCooldown=2,cooldown=5)
nookSkill2 = skill("Stonks","nookSkill2",TYPE_DAMAGE,0,250,range=AREA_CIRCLE_1,area=AREA_CIRCLE_1,repetition=3,cooldown=6,initCooldown=2)
nookSkill3 = skill("Habitat naturel","nookSkill3",TYPE_DAMAGE,0,150,area=AREA_CIRCLE_2,range=AREA_MONO,cooldown=5,initCooldown=2)
nookSkill4 = skill("Déluge insulaire","nookSkill4",TYPE_DAMAGE,0,40,AREA_MONO,area=AREA_DIST_7,cooldown=6,setAoEDamage=True,initCooldown=3)

ailillSkill = skill("Décapitage","headnt",TYPE_DAMAGE,0,5000,AREA_RANDOMENNEMI_1,tpCac=True,ultimate=True,cooldown=5,execution=True,damageOnArmor=500,emoji='<:decapitage:897846515979149322>',say=["J'en ai assez de ta tête.","Pff, j'en ai assez de jouer avec toi, t'es pas drôle","Laisse moi libérer tes épaules d'un poids beaucoup trop grand pour elles"],description="Ailill exécute un ennemi au hasard à interval réguliers")
ailillWeap = copy.deepcopy(depha)
ailillEffBleeding = copy.deepcopy(bleeding)
ailillEffBleeding.power = 50
ailillWeap.effectOnUse, ailillWeap.power, ailillWeap.range, ailillWeap.endurance = ailillEffBleeding, ailillWeap.power + 100, RANGE_DIST, 35
ailillSkill4 = skill("Frappe Sonique",'ailillSkill4',TYPE_DAMAGE,0,150,AREA_RANDOMENNEMI_1,area=AREA_CIRCLE_2,cooldown=3,tpCac=True,areaOnSelf=True,description="Ailill apparait à côté d'un ennemi et inflige des dégâts à tous les ennemis autour d'elle")
ailillSkill5 = skill("Lames Dansantes","ailillSkill5",TYPE_DAMAGE,power=200,range=AREA_RANDOMENNEMI_3,area=AREA_LINE_5,cooldown=5,description="Ailill apparait à côté d'un ennemi et inflige des dégâts sur toute une ligne dans la direction de ce dernier")
ailillSkill6Eff = effect("Frappe Déphasée","ailillDephaStrikes",STRENGTH,power=85,area=AREA_CIRCLE_1,trigger=TRIGGER_ON_REMOVE,type=TYPE_INDIRECT_DAMAGE)
ailillSkill6 = skill("Frappe Déphasée","alillSkill6",TYPE_INDIRECT_DAMAGE,effect=ailillSkill6Eff,range=AREA_RANDOMENNEMI_3,area=AREA_RANDOMENNEMI_5,cooldown=5,description="Les mouvements d'Ailill deviennent difficilement percevables\nCette dernière marque 5 ennemis aléatoirement et viendra infliger des dé^gats autour d'eux à sont prochain tour")
ailillSkill2_4 = skill("Attaques Successives","ailillSkill2",TYPE_DAMAGE,power=275,area=AREA_CIRCLE_1,tpCac=True,range=AREA_CIRCLE_3,cooldown=7,description="Effectue de multiples attaques aux airs d'effets variés sur l'ennemi ciblé",say="MAIS CREVE ENFIN !")
ailillSkill2_4_cast = effect("Cast - Attaques Successives","ailillSkill2Cast4",silent=True,replique=ailillSkill2_4)
ailillSkill2_3 = copy.deepcopy(ailillSkill2_4)
ailillSkill2_3.power, ailillSkill2_3.effectOnSelf, ailillSkill2_3.say, ailillSkill2_3.area, ailillSkill2_3.replay = 235, ailillSkill2_4_cast, "", AREA_INLINE_2, True
ailillSkill2_3_cast = effect("Cast - Attaques Successives","ailillSkill2Cast3",silent=True,replique=ailillSkill2_3)
ailillSkill2_2 = copy.deepcopy(ailillSkill2_3)
ailillSkill2_2.power, ailillSkill2_2.effectOnSelf, ailillSkill2_2.area = 150, ailillSkill2_3_cast, AREA_LINE_3
ailillSkill2_2_cast = effect("Cast - Attaques Successives","ailillSkill2Cast2",silent=True,turnInit=True,replique=ailillSkill2_2)
ailillSkill2 = copy.deepcopy(ailillSkill2_2)
ailillSkill2.power, ailillSkill2.effectOnSelf, ailillSkill2.area, ailillSkill2.tpCac, ailillSkill2.replay = 0, ailillSkill2_2_cast, AREA_MONO, False, False
ailillSkill3Eff = effect("Double Tranchant","ailillSkill3Eff",STRENGTH,power=200,trigger=TRIGGER_ON_REMOVE,type=TYPE_INDIRECT_DAMAGE)
ailillSkill3 = skill("Frappe en deux-temps","ailillSkill3",TYPE_DAMAGE,power=ailillSkill3Eff.power,effect=ailillSkill3Eff,cooldown=3,tpCac=True,range=AREA_CIRCLE_2,description='Inflige des dégâts directs à la cible, puis inflige un secind coup au début de votre prochain tour')
ailillSkill7Eff = copy.deepcopy(vulne)
ailillSkill7Eff.power, ailillSkill7Eff.turnInit = 35, 4
ailillSkill7 = skill("Disparité","ailillSkill7",TYPE_DAMAGE,power=450,cooldown=4,lifeSteal=35,sussess=250,effect=ailillSkill7Eff,description="Inflige de lourd dégâts à l'ennemi ciblé, vol une partie des dégâts infligés et augmente les dégâts qu'elle subit de **35%** pendant 4 tours")

kitsuneWeapEff = effect("Kitsune originelle",'kitsunePassifEff',CHARISMA,magie=10,charisma=10,emoji='<:kitsuWeapEff:935553855272407080>',turnInit=-1,description="En subissant des dégâts, esquivant une attaque ou infligeant des dégâts, Kitsune donne l'effet __Sous le Charme II__ à l'entité attanquante ou attaquée",callOnTrigger=charming)
kitsuneWeap = weapon("Magie multi-élémentaire",'kitsuneWeap',RANGE_DIST,AREA_CIRCLE_4,35,99,ignoreAutoVerif=True,repetition=3,charisma=35,endurance=20,effectOnUse=charming,use=MAGIE,effect=kitsuneWeapEff,emoji='<:kitsuWeap:935553775500947486>')
kitsuneSkill1_1 = skill("Flammes originelles",'kitsuneSkill1',TYPE_DAMAGE,power=100,area=AREA_CONE_3,cooldown=3,use=MAGIE,emoji='<:fireKitsune:917670925904785408>',say="Et si je chauffais un peu l'ambiance ?")
kitsuneSkill1_2 = skill("Glace Originelle","kitsuneSkill1",TYPE_DAMAGE,power=150,area=AREA_LINE_3,cooldown=3,use=MAGIE,emoji='<:waterKitsune:917670866626707516>')
kitsuneSkill1_3 = skill("Vent Originel",'kitsuneSkill1',TYPE_DAMAGE,power=150,range=AREA_MONO,area=AREA_CIRCLE_2,use=MAGIE,cooldown=2,emoji='<:airKitsune:917670912646602823>',say="Oh vous voulez me voir de près ? J'ai de quoi vous satisfaire")
kitsuneSkill1_4 = skill("Roche Originel",'kitsuneSkill1',TYPE_DAMAGE,power=135,range=AREA_CIRCLE_2,area=AREA_CIRCLE_1,cooldown=2,use=MAGIE,emoji='<:earthKitsune:917670882586017792>')
kitsuneSkill1 = skill("Magie Originelle",'kitsuneSkill1',TYPE_DAMAGE,become=[kitsuneSkill1_1,kitsuneSkill1_2,kitsuneSkill1_3,kitsuneSkill1_4],use=MAGIE)
kitsuneSkill2_1 = skill("Vent d'amour",'kitsuneSkill2',TYPE_MALUS,range=AREA_MONO,area=AREA_CIRCLE_2,effect=charming,effPowerPurcent=300,effectOnSelf=charming2,cooldown=3,say="Vous voulez vraiment rester aussi près ? Téméraires dites donc ^^")
kitsuneSkill2_2 = skill("Terre d'amour",'kitsuneSkill2',TYPE_MALUS,range=AREA_CIRCLE_2,area=AREA_CIRCLE_1,effect=charming,effPowerPurcent=700,effectOnSelf=charming2,cooldown=3,message="{0} recouvre {2} et ses alliés proches avec ses queues")
kitsuneSkill2_3 = skill("Feu d'amour",'kitsuneSkill2',TYPE_MALUS,range=AREA_MONO,area=AREA_DIST_5,effect=charming,effPowerPurcent=300,effectOnSelf=charming2,cooldown=3,say="Vous voulez pas avoir une meilleure vue ? J'ai de quoi tous vous contenter vous savez ?")
kitsuneSkill2_4 = skill("Eau d'amour",'kitsuneSkill2',TYPE_MALUS,range=AREA_DIST_5,area=AREA_CONE_3,effect=charming,effPowerPurcent=500,effectOnSelf=charming2,cooldown=3,message="{0} fait pleuvoir un {1} autour de {2}")
kitsuneSkill2 = skill("Amour élémentaire",'kitsuneSkill2',TYPE_DAMAGE,become=[kitsuneSkill2_1,kitsuneSkill2_2,kitsuneSkill2_3,kitsuneSkill2_4],use=CHARISMA,description="Donne entre 3 et 5 effect __Sous le Charme II__ avec des zones d'effets variables, et __Sous le Charme III__ sur soi-même")
kitsuneSkill3_1 = skill("Vitesse aérienne",'kitsuneSkill3',TYPE_DAMAGE,power=50,range=AREA_INLINE_3,use=MAGIE,replay=True,cooldown=2,emoji='<:liaSkill:922291249002709062>',knockback=3,jumpBack=2,message="{0} file tel une brise et frappe {2} avec ses queues")
kitsuneSkill3_2 = skill("Sable mouvants",'kitsuneSkill3',TYPE_DAMAGE,power=100,range=AREA_MONO,area=AREA_CIRCLE_2,use=MAGIE,cooldown=4,effectOnSelf=liuSkillEff,emoji=liuSkill.emoji)
kitsuneSkill3_3 = skill("Flamme infernales",'kitsuneSkill3',TYPE_INDIRECT_DAMAGE,range=AREA_MONO,area=AREA_ALL_ENEMIES,use=MAGIE,cooldown=3,emoji=lieSkill.emoji,effect=lizSkillSusEff,message="{0} déploie ses queues en éventail qui se mirent à briller, échauffant le terrain")
kitsuneSKill3_4Eff = effect("Régénération",'kitsuneSkill3_4Eff',CHARISMA,power=75,turnInit=3,lvl=3,emoji='<:lioWeap:908859876812415036>',type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN)
kitsuneSkill3_4 = skill("Pluie infernale",'kitsuneSkill3',TYPE_DAMAGE,power=35,range=AREA_MONO,area=AREA_ALL_ENEMIES,use=MAGIE,cooldown=5,emoji=lioRez.emoji,setAoEDamage=True,effectOnSelf=kitsuneSKill3_4Eff,message="{0} pointe ses queues vers le ciel, qui se mirent à projeter de l'eau")
kitsuneSkill3 = skill("Magie multi-élémentaire II",'kitsuneSkill3',TYPE_DAMAGE,become=[kitsuneSkill3_1,kitsuneSkill3_2,kitsuneSkill3_3,kitsuneSkill3_4],use=MAGIE)
kitsuneSkill4Finish = skill("Final éventé","kitsuneSkill4",TYPE_DAMAGE,power=150,knockback=5,area=AREA_CIRCLE_3,range=AREA_MONO,emoji='<:ak:917670912646602823>',ultimate=True,cooldown=7,use=MAGIE,description="Après un tour de chargement, Kitsune effectue une succéssion d'attaques ayant des puissances et des zones d'effets variées")
kitsuneSkill4Cast1 = effect("Cast - Final éventé","kitsuneSkill4Cast1",replique=kitsuneSkill4Finish,silent=True)
kitsuneSkill4Earth = skill("Trainée Rocheuse","kitsuneSkill4",TYPE_DAMAGE,power=250,area=AREA_INLINE_5,range=AREA_MONO,emoji='<:ek:917670882586017792>',replay=True,effectOnSelf=kitsuneSkill4Cast1,ultimate=True,use=MAGIE)
kitsuneSkill4Cast2 = effect("Cast - Trainée Rochause","kitsuneSkill4Cast2",replique=kitsuneSkill4Earth,silent=True)
kitsuneSkill4Fire = skill("Terre Brûlée","kitsuneSkill4",TYPE_DAMAGE,power=180,setAoEDamage=True,area=AREA_CIRCLE_2,range=AREA_MONO,emoji='<:fk:917670925904785408>',replay=True,effectOnSelf=kitsuneSkill4Cast2,ultimate=True,use=MAGIE)
kitsuneSkill4Cast3 = effect("Cast - Terre Brûlée","kitsuneSkill4Cast3",replique=kitsuneSkill4Fire,silent=True)
kitsuneSkill4Water = skill("Anneau Hydro","kitsuneSkill4",TYPE_DAMAGE,power=100,setAoEDamage=True,area=AREA_DIST_4,range=AREA_MONO,emoji='<:wk:917670866626707516>',replay=True,effectOnSelf=kitsuneSkill4Cast3,ultimate=True,use=MAGIE)
kitsuneSkill4Cast3 = effect("Cast - Danse Quadra_Elémentaire","kitsuneSkill4Cast4",replique=kitsuneSkill4Water,silent=True,turnInit=2,emoji='<:univ:936302039456165898>')
kitsuneSkill4 = skill("Danse Quadra-Elémentaire","kitsuneSkill4",TYPE_DAMAGE,range=AREA_MONO,effectOnSelf=kitsuneSkill4Cast3,cooldown=8,emoji='<:univ:936302039456165898>',ultimate=True,use=MAGIE)

naciaWeap = weapon("Lame Pangéenne","noneWeap",RANGE_DIST,AREA_CIRCLE_1,200,100,ignoreAutoVerif=True)
naciaEarthEff = effect("Puissance Tellurique","naciaEarthEff",turnInit=10,emoji=liuWeap.effect.emoji,description="Nacialisa a galvanisé les alentours avec une grande puissance élémentaire")
naciaEarthSkill1 = skill("Séisme de la génitrice","naciaSkill1",TYPE_DAMAGE,power=175,range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=4,effectOnSelf=naciaEarthEff,condition=["exclusive","element",ELEMENT_EARTH])
naciaEarthSkill2 = skill("Lames Rocheuses","naciaSkill1",TYPE_DAMAGE,power=180,range=AREA_MONO,area=AREA_INLINE_5,cooldown=4,effectOnSelf=naciaEarthEff,condition=["exclusive","element",ELEMENT_EARTH])
naciaEarthSkill3Eff = effect("Enlisé","naciaQuickSandEff",ENDURANCE,agility=-15,turnInit=4,description="Réduit l'agilité pendant 4 tours",stackable=True)
naciaEarthSkill3 = skill("Sables Mouvants","naciaSkill1",TYPE_DAMAGE,power=85,range=AREA_MONO,setAoEDamage=True,area=AREA_CIRCLE_3,cooldown=4,effectOnSelf=naciaEarthEff,effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_3,naciaEarthSkill3Eff],condition=["exclusive","element",ELEMENT_EARTH])
naciaEarthSkill = skill("Conviction de la planète","naciaSkill1",TYPE_DAMAGE,emoji=liuWeap.effect.emoji[0][0],become=[naciaEarthSkill1,naciaEarthSkill2,naciaEarthSkill3],cooldown=4,description="Nacialisla utilise des compétences terrestres pour infliger des dégâts autour d'elle",condition=["exclusive","element",ELEMENT_EARTH])
naciaFireEff = effect("Puissance Volcanique","naciaFireEff",turnInit=10,emoji=lieWeap.effect.emoji,description="Nacialisa a galvanisé les alentours avec une grande puissance élémentaire")
naciaFireSkill1Eff = effect("Brûlure volcanique","naciaDot",MAGIE,power=40,turnInit=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,lvl=3,description="Des braises infligent des dégâts périodiquements",stackable=True)
naciaFireSkill1 = skill("Eruption Explosive","naciaSkill2",TYPE_INDIRECT_DAMAGE,range=AREA_MONO,area=AREA_CIRCLE_5,effect=naciaFireSkill1Eff,effPowerPurcent=100,cooldown=4,effectOnSelf=naciaFireEff,condition=["exclusive","element",ELEMENT_FIRE])
naciaFireSkill2 = skill("Eruption Effusive","naciaSkill2",TYPE_INDIRECT_DAMAGE,range=AREA_CIRCLE_3,area=AREA_CIRCLE_3,effect=naciaFireSkill1Eff,effPowerPurcent=125,cooldown=4,effectOnSelf=naciaFireEff,condition=["exclusive","element",ELEMENT_FIRE])
naciaFireSkill3 = skill("Frappe Eruptive","naciaSkill2",TYPE_DAMAGE,power=350,effect=naciaFireSkill1Eff,effPowerPurcent=300,cooldown=4,effectOnSelf=naciaFireEff,use=MAGIE,condition=["exclusive","element",ELEMENT_FIRE])
naciaFireSkill = skill("Ardeur de la planète","naciaSkill2",TYPE_INDIRECT_DAMAGE,emoji=lieWeap.effect.emoji[0][0],become=[naciaFireSkill1,naciaFireSkill2,naciaFireSkill3],cooldown=4,description="Nacialisla utilise des compétences emflammées magiques pour infliger des dégâts sur la durée",condition=["exclusive","element",ELEMENT_FIRE])
naciaAirEff = effect("Puissance Aérienne","naciaAirEff",turnInit=10,emoji=liaWeap.effect.emoji,description="Nacialisa a galvanisé les alentours avec une grande puissance élémentaire")
naciaAirSkill1 = skill("Ouragant de la génitrice","naciaSkill3",TYPE_DAMAGE,power=120,knockback=3,range=AREA_MONO,area=AREA_CIRCLE_2,effectOnSelf=naciaAirEff,cooldown=4,condition=["exclusive","element",ELEMENT_AIR])
naciaAirSkill2 = skill("Oeuil de la Tempette","naciaSkill3",TYPE_DAMAGE,power=80,setAoEDamage=True,knockback=1,range=AREA_MONO,area=AREA_DIST_5,effectOnSelf=naciaAirEff,cooldown=4,condition=["exclusive","element",ELEMENT_AIR])
naciaAirSkill3_3 = skill("Vitesse Aérienne","naciaSkill3",TYPE_DAMAGE,power=80,setAoEDamage=True,area=AREA_RANDOMENNEMI_4,effectOnSelf=naciaAirEff,cooldown=4,condition=["exclusive","element",ELEMENT_AIR])
naciaAirSkill3_cast_3 = effect("Cast - Vitesse Aérienne","naciaVitCast1",replique=naciaAirSkill3_3,silent=True)
naciaAirSkill3_2 = skill("Vitesse Aérienne","naciaSkill3",TYPE_DAMAGE,power=70,setAoEDamage=True,area=AREA_RANDOMENNEMI_4,effectOnSelf=naciaAirSkill3_cast_3,condition=["exclusive","element",ELEMENT_AIR],replay=True)
naciaAirSkill3_cast_2 = effect("Cast - Vitesse Aérienne","naciaVitCast1",replique=naciaAirSkill3_2,silent=True)
naciaAirSkill3 = skill("Vitesse Aérienne","naciaSkill3",TYPE_DAMAGE,power=60,setAoEDamage=True,area=AREA_RANDOMENNEMI_4,effectOnSelf=naciaAirSkill3_cast_2,condition=["exclusive","element",ELEMENT_AIR],replay=True)
naciaAirSkill = skill("Souffle de la planète","naciaSkill3",TYPE_DAMAGE,emoji=liaWeap.effect.emoji[0][0],become=[naciaAirSkill1,naciaAirSkill2,naciaAirSkill3],cooldown=4,description="Nacialisla utilise des compétences aérienne pour infliger des dégâts tout en repoussant ses ennemis",condition=["exclusive","element",ELEMENT_AIR])
naciaWaterEff = effect("Puissance Aquatique","naciaWaterEff",turnInit=10,emoji=lioWeap.effect.emoji,description="Nacialisa a galvanisé les alentours avec une grande puissance élémentaire")
naciaWaterSkill1 = skill("Pluie diluvienne","naciaSkill4",TYPE_DAMAGE,power=85,setAoEDamage=True,range=AREA_MONO,area=AREA_ALL_ENEMIES,cooldown=4,effectOnSelf=naciaWaterEff,use=MAGIE,condition=["exclusive","element",ELEMENT_WATER])
naciaWaterSkill2 = skill("Déluge","naciaSkill4",TYPE_DAMAGE,power=150,setAoEDamage=True,range=AREA_MONO,area=AREA_CIRCLE_4,knockback=2,cooldown=4,effectOnSelf=naciaWaterEff,use=MAGIE,condition=["exclusive","element",ELEMENT_WATER])
naciaWaterSkill3 = skill("Grèle","naciaSkill4",TYPE_DAMAGE,power=100,setAoEDamage=True,range=AREA_MONO,area=AREA_DIST_7,cooldown=4,effectOnSelf=naciaWaterEff,use=MAGIE,condition=["exclusive","element",ELEMENT_WATER])
naciaWaterSkill = skill("Tempéralité de la planète","naciaSkill4",TYPE_DAMAGE,emoji=lioWeap.effect.emoji[0][0],become=[naciaWaterSkill1,naciaWaterSkill2,naciaWaterSkill3],cooldown=4,description="Nacialisla utilise des compétences aquatique magique pour infliger des dégâts à un grand nombre d'ennemis",use=MAGIE,condition=["exclusive","element",ELEMENT_WATER])
naciaNoneSkill = skill("Méditation","naciaMultiElemSkill",TYPE_BOOST,effect=tablElemEff[ELEMENT_UNIVERSALIS_PREMO],range=AREA_MONO,cooldown=3,effPowerPurcent=200,rejectEffect=[naciaEarthEff,naciaFireEff,naciaAirEff,naciaWaterEff])
naciaEarthFire = skill("Terre Brûlée","naciaMultiElemSkill",TYPE_DAMAGE,power=135,range=AREA_MONO,area=AREA_CIRCLE_3,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_CIRCLE_3,naciaFireSkill1Eff],effPowerPurcent=80,cooldown=3,needEffect=[naciaEarthEff,naciaFireEff])
naciaEarthWater = skill("Marécage","naciaMultiElemSkill",TYPE_DAMAGE,power=120,range=AREA_MONO,area=AREA_CIRCLE_3,effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_3,naciaEarthSkill3Eff],effPowerPurcent=80,cooldown=3,needEffect=[naciaEarthEff,naciaWaterEff])
naciaEarthAir = skill("Tempette de sable","naciaMultiElemSkill",TYPE_DAMAGE,power=120,range=AREA_MONO,area=AREA_CIRCLE_3,knockback=7,cooldown=3,needEffect=[naciaEarthEff,naciaAirEff])
naciaFireWaterEff = effect("Geyser","naciaFWEff",MAGIE,power=70,area=AREA_CIRCLE_1,trigger=TRIGGER_ON_REMOVE,type=TYPE_INDIRECT_DAMAGE)
naciaFireWater = skill("Pulsation phréatique","naciaMultiElemSkill",TYPE_INDIRECT_DAMAGE,range=AREA_MONO,area=AREA_RANDOMENNEMI_5,cooldown=3,needEffect=[naciaFireEff,naciaWaterEff])
naciaFireAir = skill("Vent enflammé","naciaMultiElemSkill",TYPE_DAMAGE,range=AREA_MONO,area=AREA_ALL_ENEMIES,power=100,setAoEDamage=True,cooldown=3,needEffect=[naciaFireEff,naciaAirEff],use=MAGIE)
naciaAirWaterEff = effect("Trempé","naciaAWEff",STRENGTH,strength=-10,magie=-10,charisma=-10,intelligence=-10,turnInit=3,type=TYPE_MALUS)
naciaAirWater = skill("Tempette","naciaMultiElemSkill",TYPE_DAMAGE,range=AREA_MONO,area=AREA_ALL_ENEMIES,power=85,setAoEDamage=True,cooldown=3,needEffect=[naciaWaterEff,naciaAirEff],effectAroundCaster=[TYPE_MALUS,AREA_ALL_ENEMIES,naciaAirWaterEff])
naciaMultiElemSkill = skill("Volonté de la planète","naciaMultiElemSkill",TYPE_DAMAGE,become=[naciaNoneSkill,naciaEarthFire,naciaEarthWater,naciaEarthAir,naciaFireWater,naciaFireAir,naciaAirWater],cooldown=3,description="Nacialisla utilise les énergies élémentaires dispersés par ses autre compétences pour en utiliser de nouvelles")

tablRaidBoss = [
    octarien("Tom Nook",335,450,100,20,50,250,0,35,10,0,nookWeapon,100,'<:nook:927252158141849670>',[nookSkill1,nookSkill2,nookSkill3,nookSkill4],oneVAll=True,baseLvl=25),
    octarien("Ailill",565,435,0,100,350,50,30,35,33,0,ailillWeap,100,'<a:Ailill:882040705814503434>',[ailillSkill,ailillSkill2,ailillSkill3,ailillSkill4,ailillSkill5,ailillSkill6,ailillSkill7],BERSERK,GENDER_FEMALE,description="Une humaine à qui la vie n'a pas vraiment souris. Du coup elle passe ses nerfs sur les autres.\nEnfin les autres plus faibles qu'elle évidamment. Si c'est le cas, il y a de bonne chance pour votre dernière vision dans ce monde soit de la voir en train de lécher votre sang sur son épée ou bien en train d'essuyer ses semelles sur votre tête",say=ailillSays,oneVAll=True,deadIcon='<:aillilKill1:898930720528011314>'),
    octarien("Kitsune",50,500,500,125,125,350,650,25,35,0,kitsuneWeap,100,'<:kitsune:935552850686255195>',element=ELEMENT_UNIVERSALIS_PREMO,aspiration=MAGE,gender=GENDER_FEMALE,deadIcon='<:kitsuSisterDead:908756093101015100>',oneVAll=True,skill=[kitsuneSkill1,kitsuneSkill2,kitsuneSkill3,kitsuneSkill4],say=kitsuneSays),
    octarien("Nacialisla",500,550,200,100,150,150,450,50,10,10,naciaWeap,100,'<:nacialisla:985933665534103564>',[naciaEarthSkill,naciaFireSkill,naciaAirSkill,naciaWaterSkill,naciaMultiElemSkill],gender=GENDER_FEMALE,description="Représentation Astrale de la Terre et de la Vie, Nacialisla a pour habitude et réputation de concerver une position de neutralité dans les conflits\nDu moins c'était jusqu'à qu'elle finisse par admettre que les Humains en avait rien a faire d'elle et de ses autres créations et qu'elle décide de les élimier, même si cela va à contre-sens de tous ses principes",deadIcon="<:spIka:866465882540605470>",oneVAll=True,baseLvl=25,element=[ELEMENT_UNIVERSALIS_PREMO,ELEMENT_UNIVERSALIS_PREMO])
]

for en in tablRaidBoss:
    en.baseLvl = 25
# --------------------------------------------------------- FindEnnemi ---------------------------------------------------------
def findEnnemi(name:str) -> Union[octarien,None]:
    """Return the normal ennemi or the boss with the given name\n
    Return ``None`` if not found\n
    
    /!\ Return the original and not a copy"""
    for a in tablUniqueEnnemies+tablBoss+tablRaidBoss+tablBossPlus:
        if a.name == name:
            return a
    return None

def simulEnnemisStats(name:str,lvl=55):
    try:
        ent:octarien = copy.deepcopy(findEnnemi(name))
        ent.changeLevel(lvl)

        baseStats = {STRENGTH:ent.strength,ENDURANCE:ent.endurance,CHARISMA:ent.charisma,AGILITY:ent.agility,PRECISION:ent.precision,INTELLIGENCE:ent.intelligence,MAGIE:ent.magie,RESISTANCE:ent.resistance,PERCING:ent.percing,CRITICAL:ent.critical}
        toPrint = "{0} (lvl {1}) :".format(name,ent.level)
        for statName, statValue in baseStats.items():
            if statName <= CRITICAL:
                toPrint += "\n{0} : {1}".format(allStatsNames[statName],statValue)

        toPrint += "\nPVs estimés : {0}".format(round((90+ent.level*10)*((baseStats[ENDURANCE])/100+1)))

        tempRes = 0
        tRes = tempRes+baseStats[RESISTANCE]
        t1 = max(0,tRes - 100)
        t2 = min(max(0,tRes - 40),60)
        t3 = min(tRes,40)

        tempRes = int(t3 + t2//3 + t1//5)
        toPrint += "\nRésistance estimée : {0}".format(tempRes)
        print(toPrint)
    except:
        print_exc()

charmingPandant.effect, charmingPandant.effectAroundCaster, charmingPandant.url = [charming2],[TYPE_MALUS,AREA_CIRCLE_5,charming], liaLB.url
