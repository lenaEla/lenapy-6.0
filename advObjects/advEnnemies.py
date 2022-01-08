from classes import *
from constantes import *
from advObjects.advWeapons import *
from advObjects.advSkills import *
from advObjects.advStuffs import *
from advObjects.advInvocs import *
from advObjects.advEffects import *

# Octariens spells
octoEm = '<:splatted1:727586364618702898>'

systemImu = effect("Résistance aux dégâts indirects","inkResistanceOcto",HARMONIE,inkResistance=12,description="Réduit les dégâts indirects reçu par le porteur",emoji=uniqueEmoji('<:nanoMedecine:921544107053158420>'),turnInit=2)
zoneOctoInkRes = skill("Nano-Science","octoBaseInkResSkill",TYPE_BOOST,0,range=AREA_MONO,area=AREA_CIRCLE_3,use=HARMONIE,effect=systemImu,cooldown=4,emoji='<:nanoMedecine:921544107053158420>')

octoShieldWeap = weapon("Bouclier Octarien","aaa",0,AREA_CIRCLE_2,52,sussess=100,price=0,endurance=20,strength=-50,effect="lo",emoji=octoEm)
octoBallWeap = weapon("Balles rebondissantes","aaa",1,AREA_CIRCLE_3,66,30,0,repetition=3,strength=10,agility=10,emoji=octoEm)
octoSnipeWeap = weapon("Snipeur Octarien","aaa",2,AREA_CIRCLE_6,52,85,0,strength=20,emoji=octoEm)
octoFly = weapon("Machinerie volante","aaa",RANGE_DIST,AREA_CIRCLE_5,66,75,-20,10,emoji=octoEm)
octoHeal = weapon("Octo heal","aaa",1,AREA_CIRCLE_3,35,50,0,use=CHARISMA,type=TYPE_HEAL,target=ALLIES,emoji='<:medic:882890887120699444>')
octoDef = weapon('OctoDef',"aaa",1,AREA_CIRCLE_3,10,100,0,effectOnUse="md",use=INTELLIGENCE,target=ALLIES,type=TYPE_HEAL,intelligence=20)
flyfishweap = weapon("Lance-Multi-Missiles","ffweap",2,AREA_CIRCLE_7,1,200,0,effectOnUse="mf",type=TYPE_DAMAGE,strength=30,ignoreAutoVerif=True)
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
kralamSkillEff2 = effect("This is, my No No Square","nono",INTELLIGENCE,resistance=10,overhealth=100,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,turnInit=3)
kralamSkillEff1 = effect("No no, don't touch me there","squaez",trigger=TRIGGER_DAMAGE,callOnTrigger=kralamSkillEff2,lvl=1,emoji=uniqueEmoji('<a:FranziskaNo:800833215106383883>'),type=TYPE_BOOST,resistance=5)
kralamSkill = skill("Prévention","vn",TYPE_BOOST,0,0,AREA_DONUT_6,cooldown=3,effect=kralamSkillEff1,emoji='<:egide:887743268337619005>')
temNativTriggered = effect("Promue",'tem',magie=0,turnInit=-1,unclearable=True,emoji=uniqueEmoji('<:colegue:895440308257558529>'))
temNativ = effect("College",'tem1',trigger=TRIGGER_ON_REMOVE,turnInit=3,unclearable=True,callOnTrigger=temNativTriggered)
temWeap = weapon("Temmie flakes","aaa",RANGE_DIST,AREA_CIRCLE_5,42,75,0,use=MAGIE,effect=temNativ,emoji='<:temFlakes:919168887222829057>',say=["TEMMIE FLAKES ! An original breakfast !","TEMMIE FLAKES ! It's so good you can't taste it !","TEMMIE FLAKES ! Don't forget to digest it !","TEMMIE FLAKES in your mouth","Whouwhouwhouwhou !"],message="{0} donne des TEMMIE FLAKES à {1}")
temSkill1 = skill("Alergies","aaa",TYPE_DAMAGE,0,100,use=MAGIE,initCooldown=3)
octoMageWeap = weapon("noneWeap","aaa",1,AREA_CIRCLE_1,0,0,0)
chargeShot = skill('Tir chargé',"aaa",TYPE_DAMAGE,0,120,emoji=shot.emoji,cooldown=4,initCooldown=2)
ultraShot = skill("Tir pénétrant","ultraShot",TYPE_DAMAGE,0,50,cooldown=3,damageOnArmor=3,repetition=3,emoji='<:targeted:912415337088159744>',area=AREA_LINE_2)
octobomberWeap = weapon("Lance Bombe Splash",0,RANGE_LONG,AREA_CIRCLE_5,48,int(splatbomb.sussess*0.9),area=splatbomb.area,emoji=splatbomb.emoji)
tentaWeap = weapon("Double canon",0,RANGE_MELEE,AREA_CIRCLE_3,42,35,repetition=4,emoji=octoEm)
octoTour = weapon("noneWeap","aaa",RANGE_LONG,AREA_CIRCLE_1,0,0,0,resistance=500)
octoTourEff1 = effect("Grand protecteur","octTourEff1",turnInit=-1,emoji=uniqueEmoji('<:tower:905169617163538442>'),unclearable=True,description="L'octo tour protège ses alliés\nTant qu'il est en vie, celui-ci subis les dégâts directs de ses alliés à leur place")
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
octoInvocWeap = weapon("Cristal d'Invocateur","OctoSummonerWeap",RANGE_LONG,AREA_CIRCLE_5,66,75,0,strength=10,endurance=10,charisma=10,agility=10,precision=10,intelligence=10,magie=10,emoji=octoEm)

octoBoost1Eff = effect("Expérimentation 1 - Force","octoBuff1",INTELLIGENCE,strength=10,emoji=uniqueEmoji('<:strengthBuff:914904347039629472>'))
octoBoost2Eff = effect("Expérimentation 2 - Magie","octoBuff2",INTELLIGENCE,magie=10,emoji=uniqueEmoji('<:magicBuff:914904390056415292>'))
octoBoost3Eff = effect("Expérimentation 3 - Résistance","octoBuff3",INTELLIGENCE,resistance=5,emoji=uniqueEmoji('<:resisBuff:914904412357537873>'))
octoBoost4Eff = effect("Expérimentation 4 - Agilité","octoBuff4",INTELLIGENCE,agility=10,emoji=uniqueEmoji('<:agiBuff:914904736166199316>'))

octoBoostSkill1 = skill(octoBoost1Eff.name,"octoBoostSkill1",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effect=octoBoost1Eff,emoji=octoBoost1Eff.emoji[0][0],use=INTELLIGENCE,cooldown=5)
octoBoostSkill2 = skill(octoBoost2Eff.name,"octoBoostSkill2",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effect=octoBoost2Eff,emoji=octoBoost2Eff.emoji[0][0],use=INTELLIGENCE,cooldown=5)
octoBoostSkill3 = skill(octoBoost3Eff.name,"octoBoostSkill3",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effect=octoBoost3Eff,emoji=octoBoost3Eff.emoji[0][0],use=INTELLIGENCE,cooldown=5)
octoBoostSkill4 = skill(octoBoost4Eff.name,"octoBoostSkill4",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effect=octoBoost4Eff,emoji=octoBoost4Eff.emoji[0][0],use=INTELLIGENCE,cooldown=5)

octoBoostWeap = weapon("Fioles d'expérimentations","octoBoostWeap",RANGE_DIST,AREA_CIRCLE_4,67,65,intelligence=25,use=INTELLIGENCE,emoji=octoBallWeap.emoji)

skills.append(kralamSkill)
effects.append(kralamSkillEff1)
effects.append(kralamSkillEff2)

octaStransEff = effect('Multi-Bras',"ocSt",aggro=15,resistance=10,turnInit = -1,unclearable=True,emoji=uniqueEmoji('<:octoStrans:900084603140853760>'))
octaStrans = skill("Multi-Bras","octaStrans",TYPE_PASSIVE,0,effectOnSelf=octaStransEff,emoji='<:multibras:900084714675785759>')

# Kitsunes sist's spells
charming = effect("Sous le charme II","kitsuneSisterEff",CHARISMA,strength=-2,magie=-2,charisma=-2,intelligence=-2,resistance=-1,stackable=True,type=TYPE_MALUS,description="Vous devriez plutôt vous concentrer sur le combat plutôt que sur celles qui sont en train de vous tuer doucement...",emoji=sameSpeciesEmoji("<:CharmeB:908793556435632158>","<:charmeR:908793574437584956>"),turnInit=2)
charming2 = effect("Sous le charme III","kitsuneSisterEffBuff",CHARISMA,strength=10,magie=10,charisma=10,intelligence=10,resistance=5,stackable=True,type=TYPE_BOOST,description="Vous avez fortement envie d'impressioner l'une de vos alliés...",emoji=sameSpeciesEmoji("<:CharmeB:908793556435632158>","<:charmeR:908793574437584956>"),turnInit=2)

liuWeapEff = effect("Kitsune de la terre","liuWeapEff",emoji=uniqueEmoji('<:earthKitsune:917670882586017792>'),stat=CHARISMA,endurance=10,agility=10,turnInit=-1,unclearable=True,description="La résistance de Liu en a épaté plus d'un.\nÀ chaque attaque subis, donne l'effet Sous le Charme II à l'attaquant",callOnTrigger=charming)
liuWeap = weapon("Sable","liuWeap",RANGE_MELEE,AREA_CIRCLE_2,27,50,repetition=3,strength=10,magie=10,charisma=10,effect=liuWeapEff,effectOnUse=charming,use=MAGIE,emoji='<:liuWeap:908859892272611348>')
liaWeapEff = effect("Kitsune des vents","liaWeapEff",CHARISMA,emoji=uniqueEmoji('<:airKitsune:917670912646602823>'),agility=10,precision=10,turnInit=-1,unclearable=True,description="L'agilité de Lia en a épaté plus d'un\nÀ chaque attaque esquivé, donne 2 fois l'effet Sous le Charme II à l'attaquant",callOnTrigger=charming)
liaWeap = weapon("Vent","liaWeap",RANGE_MELEE,AREA_CIRCLE_2,16,50,repetition=5,charisma=10,magie=10,agility=10,effect=liaWeapEff,effectOnUse=charming,use=MAGIE,emoji='<:liaWeap:908859908034793552>')
lioWeapEff = effect("Kitsune de l'eau","lioWeapEff",CHARISMA,emoji=uniqueEmoji('<:waterKitsune:917670866626707516>'),intelligence=10,magie=10,turnInit=-1,unclearable=True,description="La douceur de Lio en a épaté plus d'un.\nÀ chaque soins réalisés par cette dernière, donne l'effet Sous le Charme III à l'allié soigné",callOnTrigger=charming2)
lioWeap = weapon("Écume","lioWeap",RANGE_LONG,AREA_CIRCLE_5,64,50,charisma=20,effect=lioWeapEff,use=CHARISMA,emoji='<:lioWeap:908859876812415036>',type=TYPE_HEAL,target=ALLIES)
lioRez = skill("Eau purifiante","lioRez",TYPE_RESURECTION,0,100,AREA_MONO,ultimate=True,area=AREA_DONUT_7,use=CHARISMA,emoji='<:lioSkill:922328964926697505>',cooldown=3,say="Allez vous autre... C'est pas le moment de stagner...")
lieWeapEff = effect("Kitsune du feu","lieWeapEff",CHARISMA,emoji=uniqueEmoji('<:fireKitsune:917670925904785408>'),intelligence=10,magie=10,turnInit=-1,unclearable=True,description="L'ardeur de Liz en a comblé plus d'un\nÀ chaque attaque réalisée, donne l'effet Sous le Charme II à la cible",callOnTrigger=charming)
lieWeap = weapon("Braise","lieWeap",RANGE_LONG,AREA_CIRCLE_4,48,50,charisma=10,magie=10,area=AREA_CIRCLE_1,effect=lieWeapEff,use=MAGIE,emoji='<:lizWeap:908859856608460820>')
lieSkillEff = effect("Combustion","lieSKillEff",MAGIE,resistance=-2,power=30,turnInit=4,lvl=4,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,stackable=True,emoji=uniqueEmoji('<:lizIndirect:917204753610571776>'))
lieSkill = skill("Flamme intérieur","lizSkill",TYPE_DAMAGE,0,effect=lieSkillEff,cooldown=3,power=115,say="Voyons voir si tu va pouvoir résister longtemps...",use=MAGIE,emoji='<:lizSkill:922328829765242961>')
liaSkill = skill("Douce caresse","liaSkill",TYPE_DAMAGE,0,power=70,range=AREA_CIRCLE_1,effect=[charming,charming,charming],knockback=1,cooldown=5,use=MAGIE,say="Roh allez, détent toi un peu !",emoji='<:liaSkill:922291249002709062>')
liuSkillEff = effect("Armure Télurique","liuSkillEff",CHARISMA,overhealth=150,aggro=15,inkResistance=10,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji('<:liuArmor:922292960886915103>'),turnInit=3)
liuSkill = skill("Frappe Télurique","liuSkill",TYPE_DAMAGE,0,power=100,use=ENDURANCE,cooldown=3,effectOnSelf=liuSkillEff,say="Oh je suis pas encore finie tu va voir !",emoji='<:liuSkill:922328931502280774>')

# Hunter's spells
hunterWeap = weapon("Logique irréfutable","hunterWeap",RANGE_LONG,AREA_CIRCLE_5,40,sussess=100,emoji='<:Objection:800829922356232202>',use=INTELLIGENCE,damageOnArmor=1.5,message="{0} utilise sa Logique irréfutable")
hunterSkill1Eff = effect("Cornered","hunterSkill1Eff",INTELLIGENCE,strength=-10,magie=-10,charisma=-10,intelligence=-10,type=TYPE_MALUS,emoji=uniqueEmoji('<a:HunterPoint:800834253889732689>'))
hunterSkill1 = skill("Preuve à l'appui","hunterSkill1",TYPE_MALUS,0,area=AREA_CIRCLE_1,effect=hunterSkill1Eff,cooldown=3,use=INTELLIGENCE,emoji='<a:HunterSmug:800841378967715841>')
hunterSkill2 = skill("Poings sur la table","hunterSkill2",TYPE_DAMAGE,0,120,use=INTELLIGENCE,cooldown=3,emoji='<a:HunterSlam:800834288487759923>')
hunterSkill3Eff = effect("Vérité","hunterSkill3Eff",INTELLIGENCE,strength=10,magie=10,charisma=10,intelligence=10,emoji=uniqueEmoji('<:Eureka:800837165688815636>'))
hunterSkill3 = skill("Vérité entrevue",'hunterSkill3',TYPE_BOOST,0,area=AREA_CIRCLE_1,effect=hunterSkill3Eff,cooldown=3,emoji='<:Eureka:800837165688815636>')
hunterSkill4 = skill("Outdated autopsy report","hunterSkill4",TYPE_RESURECTION,0,150,use=INTELLIGENCE,emoji='<:AutopsyReport:800839396151656469>',cooldown=5,message='{0} a mis à jour le rapport d\'autopsy de {2}')

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

octaPomWeapon = weapon("PomPom","octaPomPomWeap",RANGE_LONG,AREA_CIRCLE_6,72,50,charisma=20,emoji=octoEm,use=CHARISMA)

# Cliroptère infirmier
clirInfWeap = weapon("Sono-Thérapie","clirInfWeap",RANGE_LONG,AREA_CIRCLE_4,45,100,charisma=20,type=TYPE_HEAL,target=ALLIES,use=CHARISMA)

# --------------------------------------------------------- Tabl Unique Ennemis ---------------------------------------------------------
tablUniqueEnnemies = [
    octarien("Octo Bouclier",50,225,20,45,45,20,10,50,0,0,octoShieldWeap,5,'<:OctoShield:881587820530139136>',[octaStrans,blindage,isolement],description="Un octarien qui se cache derrière un gros et lourd bouclier",number=2,aspiration=PROTECTEUR),
    octarien("Octo Tireur",150,55,30,95,105,35,0,20,0,20,octoBallWeap,3,'<:octoshooter:880151608791539742>',[chargeShot,ultraShot],description="Un tireur sans plus ni moins",number=3,aspiration=OBSERVATEUR),
    octarien("Octo Soigneur",30,100,220,35,15,25,50,25,0,0,octoHeal,4,"<:octohealer:880151652710092901>",[lightAura,cure,firstheal],aspiration=ALTRUISTE,description="Un octarien qui se spcésialise dans ~~passer son tour~~ soigner ses alliés",number=3),
    octarien("Rudinn",150,70,20,55,50,35,35,35,0,15,ruddinweap,6,"<a:rudinn:893246033226760232>",skill=[ultraShot],aspiration=TETE_BRULE,deadIcon='<:defeatrudeen:893246353415757824>',baseLvl=10,number=3),
    octarien("Rudinn Ranger",150,150,20,30,30,25,25,35,0,15,ruddinweap2,8,"<a:rudinnRanger:893248570742956072>",aspiration=POIDS_PLUME,deadIcon='<:defeatrudeen:893246353415757824>',skill=[octaStrans],baseLvl=10,number=3),
    octarien("Aéro-benne",150,50,35,60,80,35,20,20,0,0,flyfishweap,5,'<:flyfish:884757237522907236>',description="Un Salmioche qui s'est passionné pour l'aviation",deadIcon='<:salmonnt:894551663950573639>',aspiration=OBSERVATEUR,baseLvl=10,number=2),
    octarien("Mallus",25,30,20,20,25,150,150,20,0,15,malusWeapon,6,'<:mallus:895824636716130308>',skill=[malusSkill1,malusSkill2,zoneOctoInkRes],aspiration=PREVOYANT,baseLvl=15,number=2),
    octarien("Kralamour",10,50,175,50,0,120,30,30,0,0,kralamWeap,5,'<:kralamour:895443866189176842>',[kralamSkill,kralamSkill2,zoneOctoInkRes],PREVOYANT,baseLvl=15,number=2),
    octarien("Temmie",55,100,55,35,35,30,130,30,15,15,temWeap,4,'<:temmie:894546348324552724>',[temSkill1],deadIcon='<:temmient:894545999996014663>',aspiration=TETE_BRULE,say=temSays,baseLvl=15,number=3),
    octarien("Bob",55,100,55,35,35,30,130,30,15,15,temWeap,4,'<:temmie:894546348324552724>',[temSkill1],deadIcon='<:temmient:894545999996014663>',aspiration=TETE_BRULE,say=bobSays,baseLvl=15),
    octarien("Octo Mage",50,50,30,30,30,20,200,20,10,15,octoMageWeap,5,'<:octomage:897910662758543422>',[flame,courant,rock,storm2],MAGE,baseLvl=20,number=3),
    octarien("Octo Mage II",50,50,30,30,30,20,200,20,10,15,octoMageWeap,5,'<:octoMage2:907712297013751838>',[fireCircle,waterCircle,earthCircle,airCircle],MAGE,baseLvl=20,number=3),
    octarien("Zombie",150,150,0,50,70,0,0,35,0,10,ironSword,6,'<:armoredZombie:899993449443491860>',[defi,zombieSkill],BERSERK,baseLvl=20,number=2),
    octarien("Octo Bombardier",150,80,20,10,100,35,0,35,20,0,octobomberWeap,6,'<:octobomber:902013837123919924>',aspiration=OBSERVATEUR,baseLvl=20,number=2,skill=[multiMissiles,booyahBombCast]),
    octarien("Tentassin",175,90,20,35,30,20,20,35,15,20,tentaWeap,6,'<:octoshoter2:902013858602967052>',aspiration=BERSERK,skill=[octaStrans,ultraShot],baseLvl=15,number=2),
    octarien("Octo Protecteur",0,100,50,50,30,200,20,20,0,0,octoDef,5,"<:octoProtect:883303222255706142>",[inkarmor,zoneOctoInkRes],aspiration=PREVOYANT,description="Un octarien qui pense que les boucliers sont la meilleure défense",baseLvl=5),
    octarien("OctoBOUM",120,-30,10,35,20,0,350,-10,0,0,octoBoumWeap,5,'<:octoboom:884810545457418271>',[explosionCast],MAGE,description="Un octarien qui a placé tous ses points dans ses envies pirotechniques",baseLvl=25,rez=False),
    octarien("Octaling",80,50,50,50,50,50,80,25,0,20,splattershotJR,5,'<:Octaling:866461984018137138>',baseLvl=10,description='Les Octalings ont une arme, aspiration, élément et compétences aléatoire définini au début du combat',number=3),
    octarien("Octarien Volant",200,45,35,100,50,20,0,25,0,35,octoFly,4,'<:octovolant:880151493171363861>',number=3,aspiration=OBSERVATEUR),
    octarien("Octo Soigneur Vétéran",0,50,300,35,40,35,0,25,0,0,veterHealWeap,7,'<:octoHealVet:906302110403010581>',[veterHealSkill1,veterHealSkill2,veterHealSkill3,veterHealSkill4,kralamSkill2],ALTRUISTE,baseLvl=30,number=3),
    octarien("Octo Moine",150,100,30,35,40,25,50,30,0,20,mainLibre,5,'<:octoMonk:907723929882337311>',[airStrike,earthStrike],BERSERK,baseLvl=15,number=2),
    octarien("Octo Scientifique",10,25,120,35,35,200,10,30,0,0,octoBoostWeap,7,"<:octoScience:915054617933541386>",[octoBoostSkill1,octoBoostSkill2,octoBoostSkill3,octoBoostSkill4,zoneOctoInkRes],IDOLE,number=2),
    octarien("Octo Sniper",250,30,20,0,120,20,15,15,10,20,octoSnipeWeap,7,'<:octotSniper:873118129398624287>',aspiration=OBSERVATEUR,description="Un octarien qui a passé des années à s'entrainer pour rivaliser avec une inkling qui faisait des ravages conséquents parmis les siens",baseLvl=15,skill=[antiArmorShot]),
    octarien("Liu",30,200,145,10,10,20,0,45,0,0,liuWeap,7,'<:liu:908754674449018890>',[ironWillSkill,liuSkill,inkRes2],PROTECTEUR,GENDER_FEMALE,"La plus sportive de sa fratterie\n\nChaque attaque à l'arme des Soeurs Kitsune applique l'état \"Sous le charme II\" qui diminue légèrement les statistiques de la cible","<:kitsuSisterDead:908756093101015100>",baseLvl=20,say=liuSays,element=ELEMENT_EARTH),
    octarien("Lia",20,50,150,170,30,30,20,30,0,0,liaWeap,7,'<:lia:908754741226520656>',[ironWillSkill,airCircle,storm2,liaSkill],POIDS_PLUME,GENDER_FEMALE,"La plus rapide et agile de sa fraterie\n\nChaque attaque à l'arme des Soeurs Kitsune applique l'état \"Sous le charme II\" qui diminue légèrement les statistiques de la cible","<:kitsuSisterDead:908756093101015100>",baseLvl=20,say=liaSays,element=ELEMENT_AIR),
    octarien("Lio",20,70,200,35,50,35,50,35,0,0,lioWeap,7,'<:lio:908754690769043546>',[revitalisation,lioRez,veterHealSkill2],ALTRUISTE,GENDER_FEMALE,"La plus calme et tranquille de sa fraterie\n\nChaque attaque à l'arme des Soeurs Kitsune applique l'état \"Sous le charme II\" qui diminue légèrement les statistiques de la cible","<:kitsuSisterDead:908756093101015100>",baseLvl=20,say=lioSays,element=ELEMENT_WATER),
    octarien("Liz",10,60,90,35,20,35,200,35,0,0,lieWeap,7,'<:lie:908754710121574470>',[pyro,explosionCast,lieSkill],MAGE,GENDER_FEMALE,"La plus impulsive de sa fraterie\n\nChaque attaque à l'arme des Soeurs Kitsune applique l'état \"Sous le charme II\" qui diminue légèrement les statistiques de la cible","<:kitsuSisterDead:908756093101015100>",baseLvl=20,say=lizSays,element=ELEMENT_FIRE),
    octarien("Benjamin Hunter",30,100,50,30,50,200,0,35,20,0,hunterWeap,8,'<a:HunterNo:800841356502237225>',[hunterSkill1,hunterSkill2,hunterSkill3,hunterSkill4],IDOLE,GENDER_MALE,deadIcon='<:AutopsyReport:800839396151656469>',baseLvl=15),
    octarien("Octo Invocateur",120,70,45,50,50,45,120,25,0,0,octoInvocWeap,7,'<:octoSummoner:919862854683873331>',[invocCarbunR,invocCarbE,invocCarbSaphir,invocCarbObsi,invocCarbT],baseLvl=20),
    octarien("Citoptère Pal. Cor.",0,135,135,50,50,35,50,45,0,0,clirWeap,8,'<:cliropPal:921910882009759764>',[ironWillSkill,clirHeal,lightAura2,renisurection],ALTRUISTE,deadIcon='<:cliroOut:921912637103698010>',baseLvl=15,number=2,gender=GENDER_FEMALE),
    octarien("Octaling PomPomGirl",10,70,200,100,45,35,10,20,0,0,octaPomWeapon,7,"<:octaPomPom:921910868097257472>",[octoPomSkill1,octoPomSkill2,octoPomSkill3,octoPomSkill4,zoneOctoInkRes],IDOLE,number=2,gender=GENDER_FEMALE),
    octarien("Citoptère Inf. Cor.",0,50,230,75,75,20,20,20,0,0,clirInfWeap,6,'<:cliroInfirm:921915716435836968>',[lightHeal2,lightBigHealArea,renisurection],ALTRUISTE,baseLvl = 15, deadIcon = '<:cliroOut:921912637103698010>',number=2)
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
spamSkill1 = skill("A Call For You","spamtomSkill1",TYPE_DAMAGE,0,150,area=AREA_CONE_3,sussess=50,emoji='<:call:892757436203671572>',cooldown=3,message="HOT {0} IN YOUR AREA HAVE A [[Message](https://fr.wikipedia.org/wiki/Message)] FOR [{2}] :")
spamSkill2 = skill("BIG SHOT","spamtomSkill2",TYPE_DAMAGE,0,200,area=AREA_LINE_5,sussess=70,ultimate=True,cooldown=5,message="[[Press F1](https://forums.commentcamarche.net/forum/affich-19023080-press-f1-to-continue-del-to-enter-setup)] FOR HELP :",emoji='<:bigshot:892757453442277417>')

# Serena
serenaSpe = skill("Libération","SerenaLibe",TYPE_UNIQUE,0,35,AREA_MONO,ultimate=True,cooldown=5,area=AREA_ALL_ENEMIES,description="Séréna fait imploser toutes les poudres de fées d'Estialba, infligeant des dégâts en fonction du nombre d'effets \"Poison d'Estialba\" et de leurs durées restantes",emoji=estal.emoji[0][0])
serenaSkill = skill("Propagation","SeranaPropa",TYPE_INDIRECT_DAMAGE,0,0,AREA_MONO,area=AREA_ALL_ENEMIES,cooldown=3,effect=estal,emoji=estal.emoji[0][0],effPowerPurcent=60)
serenaFocal = copy.deepcopy(focal)
serenaFocal.effectOnSelf = None
serenaSkill2 = skill("Purgation","serenaSkill2",TYPE_INDIRECT_DAMAGE,0,range=AREA_MONO,area=AREA_CIRCLE_3,effect=estal,use=MAGIE,effPowerPurcent=80,emoji='<:purgation:921702426690600960>')

# Jevil
jevilPassifEffect = effect("I can do anything !","jevilPassiveEffect",silent=True,turnInit=-1,description="Rien n'est plus amusant que le chaos !\n\nLorsque Jevil est dans le combat, tous les combattants recoivent l'effet \"__Confusion__\" qui occulte l'icones des effets dans la liste de ces derniers jusqu'à la fin du combat\n\nÀ chaque début de tour, Jevil donne l'effet \"__Boîte à malice__\" à un certain nombre de cible. Cet effet inflige des dégâts indirect avec une puissance et une zone d'effet aléatoire au début du tour du porteur\nLe nombre d'effets donnés et de cible augmente au fur et à mesure que les PVs de Jevil descendent")
jevilWeap = weapon("Projectiles","jevilWeap",RANGE_DIST,AREA_CIRCLE_4,60,50,area=AREA_CONE_2,say="CHAOS, CHAOS, CATCH ME IF YOU CAN!",emoji='<:chaos:892857755143127090>',damageOnArmor=1.5,effect=jevilPassifEffect)
jevilSkill1_1 = skill("Pics","jevilSkill1",TYPE_DAMAGE,0,120,area=AREA_LINE_2,sussess=60,emoji='<a:card:892855854712385637>',say="I CAN DO ANYTHING !",cooldown=1,damageOnArmor=1.5)
jevilSkill1_2 = skill("Trèfles","jevilSkill1",TYPE_DAMAGE,0,100,area=AREA_CONE_2,sussess=70,emoji='<a:card:892855854712385637>',say="I CAN DO ANYTHING !",cooldown=1,damageOnArmor=0.8)
jevilSkill1_3 = skill("Coeurs","jevilSkill1",TYPE_DAMAGE,0,150,area=AREA_DIST_4,range=AREA_MONO,sussess=60,emoji='<a:card:892855854712385637>',say="I CAN DO ANYTHING !",cooldown=2,)
jevilSkill1_4 = skill("Carreau","jevilSkill1",TYPE_DAMAGE,0,100,area=AREA_DIST_3,range=AREA_CIRCLE_2,sussess=100,emoji='<a:card:892855854712385637>',say="I CAN DO ANYTHING !",cooldown=2,damageOnArmor=3)
jevilSkill1 = skill("Joker !","jevilSkill1",TYPE_DAMAGE,0,become=[jevilSkill1_1,jevilSkill1_2,jevilSkill1_3,jevilSkill1_4],emoji='<a:card:892855854712385637>')

jevilSkill2 = skill("Final Chaos","jevilSkill2",TYPE_DAMAGE,0,120,AREA_MONO,area=AREA_ALL_ENEMIES,say="KIDDING ! HERE'S MY FINAL CHAOS !",initCooldown=5,cooldown=10,emoji="<:devilknife:892855875600023592>",damageOnArmor=2)
jevilEff = effect("Confusion","giveup",silent=True,emoji=uniqueEmoji('<a:giveup:902383022354079814>'),turnInit=-1,unclearable=True,description="Confuse confusing confusion")

# Luna (Oh it's will be funny)
lunaSpe = skill("Ténèbres Éternels","InfDarkLaunch",TYPE_DAMAGE,0,80,AREA_MONO,area=AREA_CIRCLE_7,emoji='<a:darkExplosion:899451335269822475>',say="Laissez moi vous montrer un avant goût des Ténèbres Éternels !",description="\n\nInvoque X **Convictions des Ténèbres**, X étant la taille de l'équipe bleue au début du combat.\nAprès 3 tours de chargement, Luna enveloppe le terrain de Ténèbres, infligeant des dégâts massifs à toute l'équipe en fonction du nombre de **Convictions des Ténèbres** présent sur le terrain\n\nDurant la période de chargement, Luna est **Invisible**, **Inciblable** et **Imunisée**",cooldown=99,initCooldown=10,damageOnArmor=1.33)
lunaRepEffect = effect("Cast - Ténèbres Éternels","darkerYetDarker3",replique=lunaSpe,turnInit=2,silent=True,emoji=uniqueEmoji("<a:lunaInfDarkTurn3:916575004492169226>"),immunity=True,translucide=True,untargetable=True)
lunaSpe2 = skill("Ténèbres Éternels","aab",TYPE_DAMAGE,0,0,AREA_MONO,area=AREA_DONUT_7,effectOnSelf=lunaRepEffect,say="Si je dois en arriver à là pour vous montrer que vous faites fausses routes, alors soit !",message="Luna concentre les Ténèbres environants...",emoji='<:infiniteDarkness:898497770531455008>')
lunaWeap = weapon("Épee de l'ombre éternelle","aaa",RANGE_MELEE,AREA_CIRCLE_1,50,50,agility=20,precision=20,repetition=5,emoji='<:lunaWeap:915358834543968348>',damageOnArmor=1.2,ignoreAutoVerif=True)
lenaRepEffect2 = effect("Cast - Ténèbres Éternels","darkerYetDarker2",replique=lunaSpe2,turnInit=3,silent=True,emoji=uniqueEmoji('<a:lunaInfDarkTurn2:916574989933748235>'),immunity=True,translucide=True,untargetable=True)
lunaSpe3 = skill("Ténèbres Éternels","aac",TYPE_DAMAGE,0,0,AREA_MONO,area=AREA_DONUT_7,effectOnSelf=lenaRepEffect2,message="Luna concentre les Ténèbres environants...",emoji='<:infiniteDarkness:898497770531455008>',say="Vous comprenez rien.")
lenaRepEffect3 = effect("Cast - Ténèbres Éternels","darkerYetDarker1",replique=lunaSpe3,turnInit=4,silent=True,emoji=uniqueEmoji('<a:lunaInfDarkTurn1:916574972321873951>'),immunity=True,translucide=True,untargetable=True)
lunaSpe4 = skill("Ténèbres Éternels","InfiniteDarkness",TYPE_DAMAGE,0,0,AREA_MONO,cooldown=99,initCooldown=8,area=AREA_DONUT_7,effectOnSelf=lenaRepEffect3,emoji='<:infiniteDarkness:898497770531455008>',say="C'est que vous commencez vraiment à être gênant vous !")
lunaSkill = copy.deepcopy(soupledown)
lunaSkill.power = 220
lunaSkill2 = skill("Frappes des Ténèbres","aaa",TYPE_DAMAGE,0,130,AREA_CIRCLE_2,repetition=3,cooldown=5,initCooldown=2,emoji='<a:lunaTB:899456356036251658>',say="Je pense pas que tu va pouvoir prendre celui-ci sans broncher.")
lunaSkill4Eff = copy.deepcopy(innerdarknessEff)
lunaSkill4Eff.stat = STRENGTH
lunaSkill4Eff.power = 50
lunaSkill4EffAlt = copy.deepcopy(lunaSkill4Eff)
lunaSkill4EffAlt.power, lunaSkill4EffAlt.area = 85,AREA_MONO
lunaSkill4 = skill("Déchirment","lunaSkill4",TYPE_INDIRECT_DAMAGE,0,range=AREA_MONO,area=AREA_DIST_7,effect=lunaSkill4Eff,cooldown=3,use=DPT_MAGIC,say="Votre Lumière ne vous protègera pas éternellement !",emoji=innerdarkness.emoji,description="Cette compétence à 50% de change de voir sa zone d'effet modifiée ainsi que la puissance de son effet et sa zone d'effet modifiée")
lunaSkill5_1 = skill("Reverse roundhouse-kick","lunaSkill5",TYPE_DAMAGE,0,110,AREA_CIRCLE_1,area=AREA_ARC_1,emoji='<:luna4inOne:919260128698589184>')
lunaSkill5_2 = skill("Side-kick fouetté","lunaSkill5",TYPE_DAMAGE,0,135,AREA_CIRCLE_1,emoji='<:luna4inOne:919260128698589184>',say="Hmf !")
lunaSkill5_3_eff = effect("Destabilisé","lunaSkill5_3Eff",type=TYPE_MALUS,emoji=stuned.emoji,stun=True)
lunaSkill5_3 = skill("Sweeping into Backflip","lunaSkill5",TYPE_DAMAGE,0,85,AREA_CIRCLE_1,repetition=2,effect=lunaSkill5_3_eff,knockback=1,emoji='<:luna4inOne:919260128698589184>',say="C'est que tu es colant toi !")
lunaSkill5_4 = skill("Double High roundhouse-kick into Side-kick","lunaSkill5",TYPE_DAMAGE,0,50,AREA_CIRCLE_1,repetition=3,knockback=3,emoji='<:luna4inOne:919260128698589184>',say="Hé vous derrière ! Cadeau !")

lunaSkill5Base = skill("Corps à corps","lunaSkill5",TYPE_DAMAGE,0,0,AREA_CIRCLE_1,description="Cette compétence peut avoir 4 effets différents, sélectionné de manière aléatoire",emoji='<:luna4inOne:919260128698589184>',become=[lunaSkill5_1,lunaSkill5_2,lunaSkill5_3,lunaSkill5_4])

# Clemence Pos Special skills
clemBloodJauge = effect("Jauge de sang","clemBloodJauge",turnInit=-1,unclearable=True,emoji=uniqueEmoji('<:clemBJ:914710384299106345>'),lvl=100,description="Clémence possédée tourne autour de sa Jauge de Sang\n\nElle débute le combat avec une jauge à **100** Points de sang, son maximum.\nChacunes de ses compétences ont un coût en Points de Sang, qui sont retiré à la jauge à la fin de leur utilisation\n\nSi la jauge de sang tombe à **0 point**, Clémence est étourdie pendant 2 tours durant lesquels sa résistance est diminuée\nLa jauge de sang récupère **1 point** de sang à chaque fois que Clémence inflige 50 points de dégâts, et **100 points** une fois que Clémence n'est plus étourdie\n\nLa quantité de points de sang dans la jauge de sang est constamant visible\nClémence possède 10% de vol de vie")
clemWeapon = weapon("Rapière en argent lunaire","clemenceWeapon",RANGE_DIST,AREA_CIRCLE_1,150,100,ignoreAutoVerif=True,use=MAGIE,effect=clemBloodJauge,magie=50,endurance=20,emoji='<:clemWeap:915358467773063208>')
clemStunEffect = effect("Thrombophilie","clemStun",stun=True,emoji=uniqueEmoji("<:stun:882597448898474024>"),turnInit=3,type=TYPE_MALUS,resistance=-85)
aliceStunEffect = effect("Hémophilie","aliceStun",stun=True,emoji=uniqueEmoji("<:stun:882597448898474024>"),turnInit=3,type=TYPE_MALUS,charisma=-50)
clemSkill1 = skill("Rune - Lune de Sang","clemSkill1",TYPE_DAMAGE,0,power=150,range=AREA_MONO,area=AREA_CIRCLE_3,emoji='<a:clemSkill1:901147227588812890>',cooldown=2,initCooldown=2,use=MAGIE)
clemSkill2 = skill("Sort - Chiroptera perniciosius","clemSkill2",TYPE_DAMAGE,0,180,AREA_CIRCLE_2,cooldown=3,emoji='<a:clemSkill4:901150027706142780>',use=MAGIE,say="Tu es trop collant.")
clemUltLauch = skill("Memento - L'Ange noir","clemUlt",TYPE_DAMAGE,0,50,AREA_MONO,area=AREA_CIRCLE_7,emoji='<:clemMemento:902222089472327760>',say="Vous avez suffisamant résisté comme ça !",sussess=666,cooldown=99,ultimate=True,description="Au premier tour, consomme tous les **Points de sang** de la Jauge de Sang, sauf 1, pour obtenir un bouclier absolu, dont la puissance dépend du nombre de points consommés\nAu second tour, si ce bouclier est toujours présent, cette attaque fait des dégâts colosaux. Consomme la jauge de sang",use=MAGIE)
clemultCastEffect = effect("Cast - Memento - L'Ange noir","clemUltEff",replique=clemUltLauch,turnInit=2,silent=True,emoji=dangerEm)
clemUltShield = effect("Bouclier sanguin","clemShield",MAGIE,overhealth=1,emoji=uniqueEmoji("<:clemMemento2:902222663806775428>"),turnInit=2,absolutShield=True)
clemUltCast = skill("Memento - L'Ange Noir","clemUltCast",TYPE_ARMOR,0,range=AREA_MONO,emoji="<:clemMemento2:902222663806775428>",effect=clemUltShield,say="Très bien.",effectOnSelf=clemultCastEffect,ultimate=True,cooldown=99)
clemSkill3 = skill("Rune - Demi-Lune","clemSkill3",TYPE_DAMAGE,0,125,AREA_CIRCLE_3,area=AREA_ARC_2,cooldown=2,use=MAGIE,emoji='<a:clemSkill3:914759077551308844>')
clemSkill4 = skill("Sort - Chiroptera vastare","clemSkill4",TYPE_DAMAGE,0,180,AREA_MONO,area=AREA_DIST_7,cooldown=4,use=MAGIE,say="Vous pensez que vous êtes à l'abri là bas ?",emoji='<a:clemSkill4:914756335860596737>')

clemBJcost = {"clemSkill1":35,"clemSkill2":35,"clemUlt":99,"clemSkill3":35,"clemSkill4":35,"aliceSkill1":25,"aliceSkill2":30,"aliceSkill3":32,"aliceSkill4":30,"aliceRez":35,"aliceRez+":150}

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
kikuBossRes = skill("Mors Vita Est","kikuRaiseLet'sGo",TYPE_RESURECTION,0,range=AREA_MONO,area=AREA_DONUT_7,use=MAGIE,power=500,emoji=kikuRes.emoji)
kikuBossWeap = weapon("Energie Vitale","kikuWeap",RANGE_LONG,AREA_CIRCLE_5,66,60,0,magie=10,endurance=10,use=MAGIE)
kikuTerraFerrum, kikuAquaFerrum, kikuIgnisFerrum, kikuAerFerrum = copy.deepcopy(mudlame), copy.deepcopy(waterlame), copy.deepcopy(firelame), copy.deepcopy(airlame)
kikuTerraFerrum.use = kikuAquaFerrum.use = kikuIgnisFerrum.use = kikuAerFerrum.use = MAGIE
kikuTerraFerrum.id = kikuAquaFerrum.id = kikuIgnisFerrum.id = kikuAerFerrum.id = "kikuUltimaFerrum"
kikuTerraFerrum.cooldown = kikuAquaFerrum.cooldown = kikuIgnisFerrum.cooldown = kikuAerFerrum.cooldown = 1
kikuUltimaFerrum = skill('UltimaFerrum',"kikuUltimaFerrum",TYPE_DAMAGE,0,0,use=MAGIE,become=[kikuTerraFerrum, kikuAquaFerrum, kikuIgnisFerrum, kikuAerFerrum],emoji='<:kikuEtFerrum:922065497460203570>')

# Tabl Boss ----------------------------------------------------
tablBoss = [
    octarien("[[Spamton Neo](https://deltarune.fandom.com/wiki/Spamton)]",500,250,100,45,45,200,200,30,33,15,bigshot,45,'<a:spamton:892749040205316138>',skill=[spamSkill1,spamSkill2],description="NOW IT'S YOUR CHANCE TO BE A [Big shot] !",deadIcon='<:spamblocked:892750635315912746>',oneVAll=True,say=spamtonSays,element=ELEMENT_DARKNESS),
    octarien("Jevil",550,230,100,60,75,120,120,10,25,15,jevilWeap,50,'<a:CHAOS:762276118224961556>',[chaos,jevilSkill1,jevilSkill2],description="I CAN DO ANYTHING !",deadIcon='<:chaosnt:892857736642064455>',oneVAll=True,say=jevilSays,element=ELEMENT_DARKNESS),
    octarien("Séréna",50,220,-50,70,50,50,330,25,0,15,armilame,10,'<:serena:897912402354511894>',[poisonus,serenaSkill,serenaSpe,serenaSkill2,serenaFocal],ENCHANTEUR,GENDER_FEMALE,rez=False,deadIcon='<:flowernt:894550324705120266>'),
    octarien("Luna prê.",435,125,80,200,50,80,0,25,35,15,lunaWeap,50,'<:luna:909047362868105227>',[lunaSpe4,lunaSkill,lunaSkill5Base,lunaSkill2,lunaSkill4],POIDS_PLUME,GENDER_FEMALE,lunaDesc,'<:spIka:866465882540605470>',True,say=lunaBossSays,element=ELEMENT_DARKNESS),
    octarien("Octo Tour",0,350,0,0,0,0,0,50,0,0,octoTour,12,'<:tower:905169617163538442>',[octoTourSkill],PROTECTEUR,rez=False,description="Une tour de siège. Tant qu'elle est en vie, tous les dégâts directs reçu par ses alliés lui sont redirigés"),
    octarien("Clémence pos.",100,160,50,50,80,150,350,35,20,0,clemWeapon,50,'<a:clemPos:914709222116175922>',[clemSkill1,clemSkill2,clemUltCast,clemSkill3,clemSkill4],MAGE,GENDER_FEMALE,"Durant l'une de ses aventures, Clémence a commis l'erreur de baisser sa garde, et une entité malveillante en a profiter pour se loger dans son esprit, perturbant sa vision de la réalitée et manipulant ses émotions",oneVAll=True,deadIcon='<:clemence:908902579554111549>',say=clemPosSays,element=ELEMENT_DARKNESS),
    octarien("The Giant Enemy Spider",300,300,0,80,100,50,300,70,10,20,TGESWeap,50,'<:TGES:917302938785968148>',[TGESSkill1],description="En début de combat, invoque 8 __\"Patte de The Giant Enemy Spider\"__ autour de lui",oneVAll=True),
    octarien("Matt",450,120,100,100,100,100,0,35,20,0,mattWeapon,50,'<:matt:922064304793059340>',[mattSkill1,mattSkill2,mattSkill3,mattSkill4],BERSERK,GENDER_MALE,"L'ultime adversaire. Dans les jeux Wii Sports en tous cas",'<:matt:922064304793059340>',True),
    octarien("Kiku",0,135,50,120,100,5,350,25,35,0,kikuBossWeap,10,'<:kiku:921704515332358174>',[kikuBossRes,kikuUltimaFerrum],gender=GENDER_FEMALE,deadIcon ='<:kikuOut:921709153892831294>',baseLvl=15,rez=False,element=ELEMENT_EARTH)
]

# ====================================== Raid Boss ======================================
nookWeapon = weapon("Dettes","nookWeapon",RANGE_DIST,AREA_CIRCLE_1,120,65,area=AREA_ARC_1,ignoreAutoVerif=True)
nookSkill1 = skill("Fissure temporelle","nookSkill1",TYPE_DAMAGE,0,150,range=AREA_MONO,area=AREA_ALL_ENEMIES,sussess=80,initCooldown=2,cooldown=5)
nookSkill2 = skill("Stonks","nookSkill2",TYPE_DAMAGE,0,250,range=AREA_CIRCLE_1,area=AREA_CIRCLE_1,repetition=3,cooldown=6,initCooldown=2)
nookSkill3 = skill("Habitat naturel","nookSkill3",TYPE_DAMAGE,0,200,area=AREA_CIRCLE_2,range=AREA_MONO,cooldown=5,initCooldown=2)
nookSkill4 = skill("Déluge insulaire","nookSkill4",TYPE_DAMAGE,0,135,AREA_MONO,area=AREA_DIST_7,cooldown=6)

ailillSkill = skill("Décapitage","headnt",TYPE_DAMAGE,0,5000,AREA_CIRCLE_1,ultimate=True,cooldown=3,damageOnArmor=500,message="{0} a assez vu {2} :",emoji='<:decapitage:897846515979149322>',say="J'en ai assez de ta tête.")
ailillWeap = copy.deepcopy(depha)
ailillEffBleeding = copy.deepcopy(bleeding)
ailillEffBleeding.power = 50
ailillWeap.effectOnUse, ailillWeap.power, ailillWeap.range, ailillWeap.endurance = ailillEffBleeding, ailillWeap.power + 45, RANGE_DIST, 35
ailillSKill2 = skill("Course déphasée","ailillSkill2",TYPE_DAMAGE,0,150,area=AREA_RANDOMENNEMI_5,cooldown=4)
ailillSKill3 = skill("Saignement déphasé","ailillSkill3",TYPE_INDIRECT_DAMAGE,0,area=AREA_RANDOMENNEMI_5,cooldown=3,effect=ailillEffBleeding)

tablRaidBoss = [
    octarien("Tom Nook",350,400,100,20,50,250,0,35,10,0,nookWeapon,70,'<:nook:927252158141849670>',[nookSkill1,nookSkill2,nookSkill3,nookSkill4],oneVAll=True,baseLvl=25),
    octarien("Ailill",450,330,0,50,250,50,30,10,33,0,ailillWeap,10,'<a:Ailill:882040705814503434>',[ailillSkill,ailillSKill2,ailillSKill3],BERSERK,GENDER_FEMALE,description="Une humaine à qui la vie n'a pas vraiment souris. Du coup elle passe ses nerfs sur les autres.\nEnfin les autres plus faibles qu'elle évidamment\n\nSi il y a 5 combattants ou plus dans une équipe, les dégâts infligés à Ailill sont réduits si l'attaquant est trop éloigné",say=ailillSays,oneVAll=True,deadIcon='<:aillilKill1:898930720528011314>'),
]


# --------------------------------------------------------- FindEnnemi ---------------------------------------------------------
def findEnnemi(name:str) -> Union[octarien,None]:
    """Return the normal ennemi or the boss with the given name\n
    Return ``None`` if not found\n
    
    /!\ Return the original and not a copy"""
    for a in tablUniqueEnnemies+tablBoss+tablRaidBoss:
        if a.name == name:
            return a
    return None