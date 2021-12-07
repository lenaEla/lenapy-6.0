from classes import *
from advObjects.advWeapons import *
from advObjects.advSkills import *
from advObjects.advStuffs import *
from advObjects.advInvocs import *
from advObjects.advEffects import *
import random,copy

print("")
# Weapon
weapons = [
    julieWeap,blueButterfly,butterflyRed,luth,krystalFist,musical,gwenCoupe,inkbrella2,concentraceurZoom,klikliSword,darkSpellBook,lightSpellBook,ironSword,machinist,shehisa,armilame,airsword,waterspell,earthspell,airspell,nemefaux,bigshot,serringue,fauc,rapiere,lunarBonk,magicSword,dtsword,butterflyP,butterflyR,depha,legendarySword,spellBook,mic,butterfly,dualJetSkelcher,squiffer,flexi,splatling,dualies,clashBlaster,hourglass1Weap,plume,mainLibre,splattershotJR,splattershot,roller,splatcharger,miniBrush,inkbrella,blaster,jetSkelcher,kcharger,HunterRiffle,firework
]

# Skill
skills = [magicRuneStrike,infinitDark,preciseShot,troublon,haimaSkill,physicRune,magicRune,rosesMagic,
    idoOS,proOS,preOS,geoConCast,kikuRes,memClemCastSkill,roses,krysUlt,chaosArmor,firelame,airlame,waterlame,mudlame,shadowLame,timeLame,lightLame,astralLame,idoOH,proOH,altOH,lightAura2,tripleMissiles,lightHeal2,extraEtingSkill,strengthOfWillCast,sixtineUlt,hinaUlt,julieUlt,invocSeraf,mageUlt,soulagement,bloodyStrike,infraMedica,magAchSkill,flambeSkill,fireCircle,waterCircle,airCircle,earthCircle,fireShot,waterShot,airStrike,earthStrike,space1,space2,space3,spaceSp,time1,time2,time3,timeSp,renisurection,demolish,contrainte,trouble,epidemic,croissance,destruction2,infectFiole,bigLaser2,bigMonoLaser2,invocBat2,invocCarbunR,concen,memAlice2,blackHole,blackHole2,renforce,steroide,focal,suppr,revitalisation,onde,eting,stingray,dark1,dark2,dark3,light1,light2,light3,derobade,ferocite,ironWillSkill,royaleGardeSkill,defi,dissimulation,bleedingTrap,convert,vampirisme,heriteEstialba,heriteLesath,flameche,flame,pyro,ecume,courant,torant,brise,storm2,tornado,stone,rock,mont,bleedingArrow,bleedingDague,swordDance,shot,percingArrow,percingLance,highkick,multishot,rocklance,infinitFire,storm,innerdarkness,divineLight,icelance,onstage,kiss,secondSun,oneforall,uppercut,stalactic,linx,bombRobot,isolement,secondWind,blindage,adrenaline,lapSkill,burst,trans,descart,thinkSkill,invocFee,invocCarbT,invocCarbE,splashdown,multiMissiles,monoMissiles,invocBat,poisonus,protect,explosion2,splatbomb,lightAura,cure,firstheal,balayette,contrecoup,boom,chaos,unHolly,soupledown,inkarmor,coffeeSkill,theSkill,gpotion,bpotion,zelian,courage,nostalgia,draw25,siropMenthe
]

# Invocations
invocTabl = [seraf,
    darkness,autoBomb,lapino,titania,feeInv,carbuncleT,carbuncleE,batInvoc,cutyBat,carbunR
]

# Stuff
stuffs = [corruptRedBoots,corruptRedVeste,corruptPurpleBoots,corruptPurpleVeste,flumOr,darFlumOr,fullTempCharp,fullTempVest,fullTempShoes,firstBar,firstShoes,firstUniform,
    scienceHat,scienceBody,scienceShoes,battleHealHat,battleHealUnif,battleHealShoes,kryscharpe,krysshirt,kryschains,battleShieldHat,battleShieldUnif,battleShieldShoes,crepuHat,crepuArmor,crepuBoots,zenithHat,zenithArmor,zenithBoots,bardHat,bardShoes,bardBody,dragoonHelmet,dragoonArmor,dragoonBoots,whiteLily,bloodLily,pompomHat,pompomBody,pompomShoes,lunaPandan,lunaDress,lunaBoots,coalHat,coalDress,coalBoots,redButterFlyBoots,redChemVeste,newMoonHat,newMoonArmor,newMoonBoots,fullMoonHat,fullMoonArmor,fullMoonBoots,bunnyEars,bunnyBody,bunnyShoes,pinkChemVeste,whiteChemVeste,blueCharpe,bandNoir,blueVC,bhBoots,bhPull,julieHat,julieShoes,julieDress,obsiHelmet,obsiBody,obsiBoots,magicArmorHelmet,magicArmorBody,magicArmorBoots,mysticHat,mysticBody,mysticBoots,whiteButterFlyBoots,pinkButterFlyBoots,purpleButterFlyBoots,purpleChemVeste,blueChemVeste,blueButterFlyBoots,celestBronzeHat,celestBronzeArmor,celestBronzeBoots,armyBoots,armyArmor,hinaAcc,hinaBody,hinaShoes,starDress,starFlats,starBar,starPull,starBoots,jeanCas,pullPol,heartBask,mocas,sandPlage,pullHeart,pullJoliReve,surveste,tshirMatelot,tshirtNoue,motarVeste,babiesRose,babiesVert,carid,chemLB,chemV,chemB,chemN,chemR,coiffeInfirmR,coiffeInfirmB,blueNoeud,whiteNoeud,giletShirt,LBBerer,aliceShoes,lightBlueFlats,rangers,lightBlueJacket,encrifugeBoots,lunetteDeVisee,magicHeal1,magicHeal2,magicHeal3,shehisaBody,shehisaBoots,shehisaMask,darkFlum,hockey,laurier,lentille,kaviboots,purpleGlass,legolass,aliceDress,yellowpull,blackGhoticDress,vigilant4,vigilant5,vigilant6,vigilant1,vigilant2,vigilant3,heartSphapeObject,shihuDress,shihuShoe,mageDress,mageShoe,tankmage1,tankmage2,tankmage3,shihuHat,indeci1,indeci2,indeci3,hyperlink,darkbabie,krysCorn,darkMaidDress,darkMaidFlats,darkMaidPendants,dracBoot,tsarine,kanisand,fecaShield,ggshield,corset,heleneShoe,heleneDress,FIACNf,FIACNh,batRuban,old,robeLoliBlue,legendaryHat,robeDrac,blingbling,lunettesOv,masqueTub,casqueColor,patacasque,patabottes,intemNorak,intemShoe,intemCharpe,heroHead,heroBody,heroShoe,blackHeels,whiteHeels,redHeels,redFlat,blueFlat,camoHat,purpleBasket,amethystEarRings,legendaryBoots,legendaryTunic,pinkSneakers,pinkRuban,maidHat,maidHeels,maidDress,squidEarRings,barrette,pataarmor,redDress,pinkShirt,flum,headSG,bodySG,shoeSG,bikini,batPendant,catEars,heartLocket,blackSnelers,schoolShoes,woodenSandals,abobination,pullCamo,blackShirt,pullBrown,bbandeau,bshirt,bshoes,uniform,blueSnekers,redSnekers,encrifuge,pinkFlat,blackFlat,batEarRings,ironHelmet,determination,pinkDress,oldBooks,jeanJacket,blackJeanJacket,whiteSneakers,anakiMask,whiteBoots,mustangBoots
]

octoEmpty1 = stuff("placeolder","ht",0,0)
octoEmpty2 = stuff("placeolder","hu",0,0)
octoEmpty3 = stuff("placeolder","hv",0,0)

#Effect
effects = [idoOHEff,proOHEff,altOHEff,lightAura2PassiveEff,extraEting,sixtineUltEff,idoOSEff,proOSEff,preOSEff,physicRuneEff,magicRuneEff,
    fireCircleEff,waterCircleEff,airCircleEff,earthCircleEff,renforceEff,renforceEff2,renforceEff3,steroideEff,gwenCoupeEff,contrainteEff,troubleEff,croissanceEff,croissanceEff2,croissanceEff3,infection,infectRej,ConcenEff,inkBrella2Eff,blackHoleEff,blackHoleEff2,blackHoleEff3,convertEff,vampirismeEff,heriteEstialbaEff,estal2,hemoragie2,heriteLesathEff,darkFlumEff,darkFlumPoi,ondeEff,etingEff,encrifugeEff2,ferociteEff,defiEff,royaleGarde,ironWill,dissimulationEff,pigmaCast,derobadeBonus,derobadeMalus,castExplo,affaiEffect,stupid,hemoragie,innerdarknessEff,darkspellbookeff,lighteff,lightHealeff,lightspellshield,onstageeff,secondSuneff,oneforallbuff,oneforalldebuff,lostSoul,nouil,isoled,const,blinde,iThink,think,octoboum,missiles,estal,cafeine,defensive,stuned,flumEffect,lightAuraEffect,hourglass1,jetlag,charme,armor,coffee,the,encrifugeEff,gpEffect,bpEffect,deterEff1,undying,onceButNotTwice,zelianR,afterShockDmg,octoshield,nostalgiaE,inkBrellaEff,stopAttacking,hunter,hunterBuff,menthe,badaboum,courageE
]

poidPlumeEff = effect("Poids Plume","poidCritEff",None,trigger=TRIGGER_END_OF_TURN,silent=True,lvl=0,type=TYPE_UNIQUE,unclearable=True,turnInit=-1,emoji=uniqueEmoji(aspiEmoji[POIDS_PLUME]))
obsEff = effect("Observateur","obsCritEff",None,silent=True,lvl=0,type=TYPE_UNIQUE,unclearable=True,turnInit=-1,emoji=uniqueEmoji(aspiEmoji[OBSERVATEUR]))

hourglassEffects = [hourglass1]

#Other
changeAspi = other("Changement d'aspiration","qa",description="Vous permet de changer d'aspiration",emoji='<:changeaspi:868831004545138718>')
changeAppa = other("Changement d'apparence","qb",description="Vous permet de changeer votre genre, couleur et espèce",emoji='<:changeAppa:872174182773977108>',price=500)
changeName = other("Changement de nom","qc",description="Vous permet de changer le nom de votre personnage",emoji='<:changeName:872174155485810718>',price=500)
restat = other("Rénitialisation des points bonus","qd",description="Vous permet de redistribuer vos points bonus",emoji='<:restats:872174136913461348>',price=500)
elementalCristal = other("Cristal élémentaire","qe",500,description="Ces cristaux vous permettent de changer l'élément de votre personnage dans /inventory element (lvl 10)\n\nCe cristal permet de sélectionner les éléments suivants :\n<:fire:887847475203932261> Feu\n<:water:887847459211079760> Eau\n<:air:887847440932290560> Air\n<:earth:887847425459503114> Terre",emoji="<:krysTal:888070310472073257>")
customColor = other("Couleur personnalisée","qf",500,description="Vous permet de rentrer une couleur personnalisée pour votre personnage",emoji='<:changeColor:892350738322300958>')
seeshell = other("Super Coquillage","qd",500,description="Ce coquillage permet de changer son bonus iné dans /inventory bonus (lvl 25)")
blablator = other("Blablator","qg",500,description="Permet de définir des messages que votre personnages dira lors de certains événements")
dimentioCristal = other("Cristal dimentionel",'qh',500,'<:krysTal2:907638077307097088>',"Ces cristaux vous permettent de changer l'élément de votre personnage dans /inventory element (lvl 20)\n\nCe cristal permet de choisir les éléments suivants :\n<:light:887847410141921362> Lumière\n<:darkness:887847395067568128> Ténèbre\n<:astral:907467653147410475> Astral\n<:temporel:907467620930973707> Temporel")
others = [elementalCristal,customColor,changeAspi,changeAppa,changeName,restat,blablator,dimentioCristal]

tablAllOcta,tablAllAllies = [],[]

# Octarien
octoEm = '<:splatted1:727586364618702898>'
octoShieldWeap = weapon("Bouclier Octarien","aaa",0,AREA_CIRCLE_2,52,sussess=100,price=0,endurance=20,strength=-50,effect="lo",emoji=octoEm)
octoBallWeap = weapon("Balles rebondissantes","aaa",1,AREA_CIRCLE_3,66,30,0,repetition=3,strength=10,agility=10,emoji=octoEm)
octoSnipeWeap = weapon("Snipeur Octarien","aaa",2,AREA_CIRCLE_6,52,85,0,strength=20,emoji=octoEm)
octoFly = weapon("Machinerie volante","aaa",RANGE_DIST,AREA_CIRCLE_3,80,75,-20,10,emoji=octoEm)
octoHeal = weapon("Octo heal","aaa",1,AREA_CIRCLE_3,35,50,0,use=CHARISMA,type=TYPE_HEAL,target=ALLIES,emoji='<:medic:882890887120699444>')
octoDef = weapon('OctoDef',"aaa",1,AREA_CIRCLE_3,10,100,0,effectOnUse="md",use=INTELLIGENCE,target=ALLIES,type=TYPE_HEAL,intelligence=20)
flyfishweap = weapon("Flyfish","ffweap",2,AREA_CIRCLE_7,1,200,0,effectOnUse="mf",type=TYPE_INDIRECT_DAMAGE,strength=30)
octoBoumWeap = weapon("noneWeap","aaa",1,AREA_CIRCLE_1,0,0,0,effect="mg") 
ruddinweap = weapon("Carreaux","aaa",RANGE_DIST,AREA_CIRCLE_3,28,70,0,0,0,0,0,0,0,0,repetition=3,emoji='<:chaos:892857755143127090>')
ruddinweap2 = weapon("Carreaux","aaa",RANGE_MELEE,AREA_CIRCLE_3,28,70,0,0,0,0,0,0,0,0,repetition=3,emoji='<:chaos:892857755143127090>')
malusWeaponEff = effect("Embrouillement","aaa",INTELLIGENCE,strength=-5,magie=-5,critical=-2,type=TYPE_MALUS)
malusWeapon = weapon("Magie sombre","aaa",RANGE_DIST,AREA_CIRCLE_5,45,70,0,effectOnUse=malusWeaponEff,use=MAGIE)
malusSkill1Eff = effect("Malussé","mal",INTELLIGENCE,-15,magie=-15,resistance=-5,type=TYPE_MALUS)
malusSkill1 = skill("Abrutissement","aaa",TYPE_MALUS,0,area=AREA_CIRCLE_2,effect=malusSkill1Eff,cooldown=5,initCooldown=2)
malusSkill2 = skill("Éclair","aaa",TYPE_DAMAGE,0,80,cooldown=2,sussess=65,use=MAGIE,emoji='<:darkThunder:912414778356564019>')
kralamWeap = weapon("Décharge motivante","aaa",RANGE_DIST,AREA_DONUT_4,50,100,0,type=TYPE_HEAL,target=ALLIES,use=CHARISMA)
kralamSkill2 = skill("Électrochoc","kralamSkill2",TYPE_DAMAGE,0,60,area=AREA_CIRCLE_1,use=CHARISMA,cooldown=3,initCooldown=2,emoji='<:electroShoc:912414625679695873>')
kralamSkillEff2 = effect("This is, my No No Square","nono",INTELLIGENCE,resistance=20,overhealth=100,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,turnInit=3)
kralamSkillEff1 = effect("No no, don't touch me there","squaez",trigger=TRIGGER_DAMAGE,callOnTrigger=kralamSkillEff2,lvl=1,emoji=uniqueEmoji('<a:FranziskaNo:800833215106383883>'),type=TYPE_BOOST,resistance=5)
kralamSkill = skill("Prévention","vn",TYPE_BOOST,0,0,AREA_DONUT_6,cooldown=3,effect=kralamSkillEff1,emoji='<:egide:887743268337619005>')
temNativTriggered = effect("Promue",'tem',magie=0,turnInit=-1,unclearable=True,emoji=uniqueEmoji('<:colegue:895440308257558529>'))
temNativ = effect("College",'tem1',trigger=TRIGGER_ON_REMOVE,turnInit=3,unclearable=True,callOnTrigger=temNativTriggered)
temWeap = weapon("Tem life saves","aaa",RANGE_DIST,AREA_CIRCLE_5,42,75,0,use=MAGIE,effect=temNativ)
temSkill1 = skill("Alergies","aaa",TYPE_DAMAGE,0,75,use=MAGIE,initCooldown=3)
octoMageWeap = weapon("noneWeap","aaa",1,AREA_CIRCLE_1,0,0,0)
chargeShot = skill('Tir chargé',"aaa",TYPE_DAMAGE,0,120,emoji=shot.emoji,cooldown=3,initCooldown=2)
ultraShot = skill("Tir pénétrant","ultraShot",TYPE_DAMAGE,0,40,cooldown=3,damageOnArmor=3,repetition=3,emoji='<:targeted:912415337088159744>',area=AREA_LINE_2)
octobomberWeap = weapon("Lance Bombe Splash",0,RANGE_LONG,AREA_CIRCLE_5,48,int(splatbomb.sussess*0.9),area=splatbomb.area,emoji=splatbomb.emoji)
tentaWeap = weapon("Double canon",0,RANGE_MELEE,AREA_CIRCLE_3,42,35,repetition=4,emoji=octoEm)
octoTour = weapon("noneWeap","aaa",RANGE_LONG,AREA_CIRCLE_1,0,0,0,resistance=500)
octoTourEff1 = effect("Grand protecteur","octTourEff1",turnInit=-1,emoji=uniqueEmoji('<:tower:905169617163538442>'),unclearable=True,description="L'octo tour protège ses alliés\nTant qu'il est en vie, celui-ci subis les dégâts directs de ses alliés à leur place")
octoTourEff2 = effect("Protection magique","octTourEff2",redirection=100,turnInit=-1,emoji=uniqueEmoji('<:tower:905169617163538442>'))
octoTourSkill = skill("Grand protecteur","octoTourSkill",TYPE_PASSIVE,0,effectOnSelf=octoTourEff1,use=None,emoji='<:tower:905169617163538442>')
veterHealSkill1 = skill("Here we go again","octoHealVet1",TYPE_RESURECTION,0,120,cooldown=4,use=CHARISMA)
veterHealSkill2 = skill("Renouvellement","octaHealVet2",TYPE_HEAL,0,100,use=CHARISMA,cooldown=5,initCooldown=2,emoji='<:heal:911735386697519175>')
veterHealSkill3 = skill("I'm a healer but...","octaHealVet3",TYPE_MALUS,0,area=AREA_CIRCLE_1,effect=incur[3],cooldown=5,emoji=incur[3].emoji[0][0])
veterHealSkill4 = skill("Théorie du complot","octaHealVet4",TYPE_DAMAGE,0,80,use=CHARISMA,cooldown=3)
veterHealWeap = copy.deepcopy(octoHeal)
veterHealWeap.negativeHeal, veterHealWeap.power = -20, veterHealWeap.power + 10
antiArmorShot = skill("Tir anti-matériel","antiArmorShot",TYPE_DAMAGE,0,100,ultimate=True,damageOnArmor=666,cooldown=7)
zombieSkillEff = effect("Marcheur des limbes","zombaSkillArmor",ENDURANCE,overhealth=80,turnInit=-3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
zombieSkill = skill("Frappe d'outre-tombe","zombiSkill",TYPE_DAMAGE,0,50,use=ENDURANCE,effectOnSelf=zombieSkillEff,cooldown=5)

octoBoost1Eff = effect("Expérimentation 1 - Force","octoBuff1",INTELLIGENCE,strength=10,emoji=uniqueEmoji('<:strengthBuff:914904347039629472>'))
octoBoost2Eff = effect("Expérimentation 2 - Magie","octoBuff2",INTELLIGENCE,magie=10,emoji=uniqueEmoji('<:magicBuff:914904390056415292>'))
octoBoost3Eff = effect("Expérimentation 3 - Résistance","octoBuff3",INTELLIGENCE,resistance=5,emoji=uniqueEmoji('<:resisBuff:914904412357537873>'))
octoBoost4Eff = effect("Expérimentation 4 - Agilité","octoBuff4",INTELLIGENCE,agility=10,emoji=uniqueEmoji('<:agiBuff:914904736166199316>'))
octoBoost5Eff = effect("Expérimentation 5 - Précision","octoBuff5",INTELLIGENCE,precision=10,emoji=uniqueEmoji('<:preciBuff:914904449615552532>'))

octoBoostSkill1 = skill(octoBoost1Eff.name,"octoBoostSkill1",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effect=octoBoost1Eff,emoji=octoBoost1Eff.emoji[0][0],use=INTELLIGENCE,cooldown=5)
octoBoostSkill2 = skill(octoBoost2Eff.name,"octoBoostSkill2",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effect=octoBoost2Eff,emoji=octoBoost2Eff.emoji[0][0],use=INTELLIGENCE,cooldown=5)
octoBoostSkill3 = skill(octoBoost3Eff.name,"octoBoostSkill3",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effect=octoBoost3Eff,emoji=octoBoost3Eff.emoji[0][0],use=INTELLIGENCE,cooldown=5)
octoBoostSkill4 = skill(octoBoost4Eff.name,"octoBoostSkill4",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effect=octoBoost4Eff,emoji=octoBoost4Eff.emoji[0][0],use=INTELLIGENCE,cooldown=5)
octoBoostSkill5 = skill(octoBoost5Eff.name,"octoBoostSkill5",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_2,effect=octoBoost5Eff,emoji=octoBoost5Eff.emoji[0][0],use=INTELLIGENCE,cooldown=5)

octoBoostWeap = weapon("Fioles d'expérimentations","octoBoostWeap",RANGE_DIST,AREA_CIRCLE_4,35,60,intelligence=25,use=INTELLIGENCE,emoji=octoBallWeap.emoji)

skills.append(kralamSkill)
effects.append(kralamSkillEff1)
effects.append(kralamSkillEff2)

octaStransEff = effect('Multi-Bras',"ocSt",aggro=15,resistance=10,turnInit = -1,unclearable=True,emoji=uniqueEmoji('<:octoStrans:900084603140853760>'))
octaStrans = skill("Multi-Bras","octaStrans",TYPE_PASSIVE,0,effectOnSelf=octaStransEff,emoji='<:multibras:900084714675785759>')

class octarien:
    def __init__(self,name,maxStrength,maxEndurance,maxCharisma,maxAgility,maxPrecision,maxIntelligence,maxMagie,resistance,percing,critical,weapon,exp,icon,skill=["0","0","0","0","0"],aspiration=INVOCATEUR,gender=GENDER_OTHER,description="",deadIcon=None,oneVAll = False,say=says(),baseLvl = 1,rez=True):
        self.name = name
        self.species = 3
        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie = maxStrength,maxEndurance,maxCharisma,maxAgility,maxPrecision,maxIntelligence,maxMagie
        self.resistance,self.percing,self.critical = resistance,percing,critical
        self.aspiration = aspiration
        self.weapon = weapon
        self.skills = skill
        while len(self.skills) < 5:
            self.skills+=["0"]

        self.skillsInventory = []
        self.color = red
        self.level = 1
        self.stuff = [octoEmpty1,octoEmpty2,octoEmpty3]
        self.exp = exp
        self.icon = icon
        self.gender = gender
        self.description = description
        self.element = ELEMENT_NEUTRAL
        self.deadIcon = deadIcon
        self.oneVAll = oneVAll
        self.says = say
        self.baseLvl = baseLvl
        self.rez = rez
        self.bonusPoints = [0,0,0,0,0,0,0]

    def allStats(self):
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]
    
    def changeLevel(self,level=1):
        self.level = level
        stats = copy.deepcopy(self.allStats())
        for a in range(0,len(stats)):
            stats[a] = round(stats[a]*0.1+stats[a]*0.9*self.level/50)

        if level > 50:
            tempStats = copy.deepcopy(self.allStats())
            for a in range(0,len(tempStats)):
                stats[a] = tempStats[a] + (stats[a]-tempStats[a])//3

        if self.level < 25:
            self.skills[4] = "0"
        if self.level < 20:
            self.skills[3] = "0"
        if self.level < 15:
            self.skills[2] = "0"
        if self.level < 10:
            self.skills[1] = "0"

        if self.level < 10:
            self.element = ELEMENT_NEUTRAL
        elif self.level < 20 and self.element in [ELEMENT_SPACE,ELEMENT_DARKNESS,ELEMENT_LIGHT,ELEMENT_LIGHT]:
            self.element = random.randint(0,3)

        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie = stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],stats[6]

    def isNpc(self,name : str):
        return self.name == name

class tmpAllie:
    def __init__(self,name,species,color,aspiration,weapon,stuff,gender,skill=[],description="Pas de description",url="",element=ELEMENT_NEUTRAL,variant = False,deadIcon=None,icon = None,bonusPoints = [None,None],say=says(),changeDict = None):
        self.name = name
        self.species = species
        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie = 0,0,0,0,0,0,0
        self.resistance,self.percing,self.critical = 0,0,0
        self.aspiration = aspiration
        self.weapon = weapon
        self.skills = ["0","0","0","0","0"]
        for a in range(0,len(skill)):
            self.skills[a] = skill[a]
        self.skillsInventory = []
        self.color = color
        self.level = 1
        self.stuff = stuff
        self.gender = gender
        if icon == None:
            self.icon = emoji.icon[species][getColorId(self)]
        else:
            self.icon = icon
        self.description=description
        self.url = url
        self.element = element
        self.variant = variant
        self.deadIcon = deadIcon
        self.bonusPoints = bonusPoints
        self.says = say
        if changeDict == None or type(changeDict) == list:
            self.changeDict = changeDict
        else:
            self.changeDict = [changeDict]

    def changeLevel(self,level=1):
        self.level = level
        stats = self.allStats()
        allMax = [maxStrength,maxEndur,maxChar,maxAgi,maxPreci,maxIntel,maxMagie]
        for a in range(0,len(stats)):
            stats[a] = round(allMax[a][self.aspiration]*0.1+allMax[a][self.aspiration]*0.9*self.level/50)

        bPoints = level
        for a in self.bonusPoints:
            if a != None:
                distribute = min(30,bPoints)
                bPoints -= distribute
                stats[a] += distribute

        if self.changeDict != None:
            haveChanged = False
            for changeDictCell in self.changeDict:
                roll = random.randint(0,99)
                if changeDictCell["level"] <= level and roll < changeDictCell["proba"] and not(haveChanged):
                    if changeDictCell["changeWhat"] == 0:               # Change Skills
                        for num in range(len(changeDictCell["change"])):
                            for skillNum in range(len(self.skills)):
                                if self.skills[skillNum].id == changeDictCell["change"][num].id:
                                    self.skills[skillNum] = changeDictCell["to"][num]
                                    break
                        haveChanged = True

        if self.level < 25:
            self.skills[4] = "0"
        if self.level < 20:
            self.skills[3] = "0"
        if self.level < 15:
            self.skills[2] = "0"
        if self.level < 10:
            self.skills[1] = "0"

        if self.level < 10:
            self.element = ELEMENT_NEUTRAL
        elif self.level < 20 and self.element in [ELEMENT_SPACE,ELEMENT_DARKNESS,ELEMENT_LIGHT,ELEMENT_LIGHT]:
            self.element = random.randint(0,3)

        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie = stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],stats[6]

    def allStats(self):
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

    def isNpc(self,name : str):
        return self.name == name

for a in [0,1]: # Octo shield
    tablAllOcta += [octarien("OctoShield",50,225,20,45,45,20,10,50,0,0,octoShieldWeap,5,'<:OctoShield:881587820530139136>',[octaStrans,blindage,isolement],description="Un octarien qui se cache derrière un gros et lourd bouclier")]

for a in [0,1,2]: # Octo shoot
    tablAllOcta += [octarien("OctoShooter",150,55,30,95,105,35,0,20,0,20,octoBallWeap,3,'<:octoshooter:880151608791539742>',[chargeShot,ultraShot],description="Un tireur sans plus ni moins")]

for a in [0,1]: # Octo heal
    tablAllOcta += [octarien("OctoHealer",30,100,220,35,15,25,50,25,0,0,octoHeal,4,"<:octohealer:880151652710092901>",[lightAura,cure,firstheal],aspiration=ALTRUISTE,description="Un octarien qui se spcésialise dans ~~passer son tour~~ soigner ses alliés")]

for a in [0,1,2]: # Rudinn
    tablAllOcta += [octarien("Rudinn",150,70,20,55,50,35,35,35,0,15,ruddinweap,6,"<a:rudinn:893246033226760232>",skill=[ultraShot],aspiration=TETE_BRULE,deadIcon='<:defeatrudeen:893246353415757824>',baseLvl=10)]

for a in [0,1]: # Rudinn Ranger
    tablAllOcta += [octarien("Rudinn Ranger",150,150,20,30,30,25,25,35,0,15,ruddinweap2,8,"<a:rudinnRanger:893248570742956072>",aspiration=POIDS_PLUME,deadIcon='<:defeatrudeen:893246353415757824>',skill=[octaStrans],baseLvl=10)]

for a in [0,1,2]: # Flyfish
    tablAllOcta += [octarien("Aéro-benne",200,40,35,60,45,35,20,20,0,0,flyfishweap,5,'<:flyfish:884757237522907236>',description="Un Salmioche qui s'est passionné pour l'aviation",deadIcon='<:salmonnt:894551663950573639>',aspiration=OBSERVATEUR,baseLvl=10)]

for a in [0,1]: # Mallus
    tablAllOcta += [octarien("Mallus",25,30,20,20,25,150,150,20,0,15,malusWeapon,6,'<:mallus:895824636716130308>',skill=[malusSkill1,malusSkill2],aspiration=PREVOYANT,baseLvl=15)]

for a in [0,1]: # Kralamour
    tablAllOcta += [octarien("Kralamour",10,50,175,50,0,120,30,30,0,0,kralamWeap,5,'<:kralamour:895443866189176842>',[kralamSkill,kralamSkill2],PREVOYANT,baseLvl=15)]

for a in [0,1,2]: # Temmie
    tablAllOcta += [octarien("Temmie",55,100,55,35,35,30,130,30,15,15,temWeap,4,'<:temmie:894546348324552724>',[temSkill1],deadIcon='<:temmient:894545999996014663>',aspiration=TETE_BRULE,say=temSays,baseLvl=15)]

for a in [0,1,2]: # Octo Mage
    tablAllOcta += [octarien("Octo Mage",50,50,30,30,30,20,200,20,10,15,octoMageWeap,5,'<:octomage:897910662758543422>',[flame,courant,rock,storm2],MAGE,baseLvl=20)]

for a in [0,1,2]: # Armored Zombie
    tablAllOcta += [octarien("Zombie",150,150,0,50,70,0,0,35,0,10,ironSword,6,'<:armoredZombie:899993449443491860>',[defi,zombieSkill],BERSERK,baseLvl=20)]

for a in [0,1,2]: # OctoBomber
    tablAllOcta.append(octarien("Octo Bomber",200,80,20,10,75,35,0,25,10,0,octobomberWeap,6,'<:octobomber:902013837123919924>',aspiration=OBSERVATEUR,baseLvl=20))

for a in [0,1,2]: # Tentassin
    tablAllOcta.append(octarien("Tentassin",175,90,20,35,30,20,20,35,15,20,tentaWeap,6,'<:octoshoter2:902013858602967052>',aspiration=BERSERK,skill=[octaStrans,ultraShot],baseLvl=15))

# Octo Protecteur
tablAllOcta += [octarien("OctoProtecteur",0,100,50,50,30,200,20,20,0,0,octoDef,5,"<:octoProtect:883303222255706142>",[inkarmor],aspiration=PREVOYANT,description="Un octarien qui pense que les boucliers sont la meilleure défense",baseLvl=5)]

# OctoBOUM
tablAllOcta += [octarien("OctoBOUM",120,-30,10,35,20,0,350,-10,0,0,octoBoumWeap,5,'<:octoboom:884810545457418271>',[explosion2],MAGE,description="Un octarien qui a placé tous ses points dans ses envies pirotechniques",baseLvl=25,rez=False)]

for a in [0,1,2]: # Octaling
    tablAllOcta += [octarien("Octaling",80,50,50,50,50,50,80,25,0,20,weapons[random.randint(0,len(weapons)-1)],5,'<:Octaling:866461984018137138>',[skills[random.randint(0,len(skills)-1)],skills[random.randint(0,len(skills)-1)],skills[random.randint(0,len(skills)-1)]],baseLvl=10)]

for a in [0,1]: # OctoFly
    tablAllOcta += [octarien("Octarien Volant",200,45,35,100,50,20,0,25,0,35,octoFly,4,'<:octovolant:880151493171363861>')]

for a in [0,1,2]: # OctoHeal 2
    tablAllOcta.append(octarien("OctoHealer Vétéran",0,50,300,35,40,35,0,25,0,0,veterHealWeap,7,'<:octoHealVet:906302110403010581>',[veterHealSkill1,veterHealSkill2,veterHealSkill3,veterHealSkill4,kralamSkill2],ALTRUISTE,baseLvl=30))

for a in [0,1,2]: # OctoMoine
    tablAllOcta.append(octarien("OctoMoine",150,100,30,35,40,25,50,30,0,20,mainLibre,5,'<:octoMonk:907723929882337311>',[airStrike,earthStrike],BERSERK,baseLvl=15))

for a in [0,1,2]: # OctoMage2
    tablAllOcta.append(octarien("Octo Mage II",50,50,30,30,30,20,250,20,10,20,octoMageWeap,5,'<:octoMage2:907712297013751838>',[fireCircle,waterCircle,earthCircle,airCircle],MAGE,baseLvl=20))

for a in (0,1,2): # Octobooster
    tablAllOcta.append(octarien("OctoBooster",10,25,120,35,35,200,10,30,0,0,octoBoostWeap,7,"<:octoScience:915054617933541386>",[octoBoostSkill1,octoBoostSkill2,octoBoostSkill3,octoBoostSkill4,octoBoostSkill5],IDOLE,baseLvl = 20))

# OctoSnipe
tablAllOcta += [octarien("OctoSniper",250,30,20,0,120,20,15,15,10,20,octoSnipeWeap,7,'<:octotSniper:873118129398624287>',aspiration=OBSERVATEUR,description="Un octarien qui a passé des années à s'entrainer pour rivaliser avec une inkling qui faisait des ravages conséquents parmis les siens",baseLvl=15,skill=[antiArmorShot])]

# Kitsune Sisters
charming = effect("Sous le charme II","kitsuneSisterEff",CHARISMA,strength=-3,magie=-3,charisma=-3,intelligence=-3,resistance=-1,stackable=True,type=TYPE_MALUS,description="Vous devriez plutôt vous concentrer sur le combat plutôt que sur celles qui sont en train de vous tuer doucement...",emoji=sameSpeciesEmoji("<:CharmeB:908793556435632158>","<:charmeR:908793574437584956>"))
charming2 = effect("Sous le charme III","kitsuneSisterEffBuff",CHARISMA,strength=10,magie=10,charisma=10,intelligence=10,resistance=5,stackable=True,type=TYPE_BOOST,description="Vous avez fortement envie d'impressioner l'une de vos alliés...",emoji=sameSpeciesEmoji("<:CharmeB:908793556435632158>","<:charmeR:908793574437584956>"))

liuWeapEff = effect("Kitsune de la terre","liuWeapEff",emoji=uniqueEmoji('<:earthKitsune:917670882586017792>'),stat=CHARISMA,endurance=10,agility=10,turnInit=-1,unclearable=True,description="La résistance de Liu en a épaté plus d'un.\nÀ chaque attaque subis, donne l'effet Sous le Charme II à l'attaquant",callOnTrigger=charming)
liuWeap = weapon("Sable","liuWeap",RANGE_MELEE,AREA_CIRCLE_2,27,50,repetition=3,strength=10,magie=10,charisma=10,effect=liuWeapEff,effectOnUse=charming,use=MAGIE,emoji='<:liuWeap:908859892272611348>')
liaWeapEff = effect("Kitsune des vents","liaWeapEff",CHARISMA,emoji=uniqueEmoji('<:airKitsune:917670912646602823>'),agility=10,precision=10,turnInit=-1,unclearable=True,description="L'agilité de Lia en a épaté plus d'un\nÀ chaque attaque esquivé, donne 2 fois l'effet Sous le Charme II à l'attaquant",callOnTrigger=charming)
liaWeap = weapon("Vent","liaWeap",RANGE_MELEE,AREA_CIRCLE_2,16,50,repetition=5,charisma=10,magie=10,agility=10,effect=liaWeapEff,effectOnUse=charming,use=MAGIE,emoji='<:liaWeap:908859908034793552>')
lioWeapEff = effect("Kitsune de l'eau","lioWeapEff",CHARISMA,emoji=uniqueEmoji('<:waterKitsune:917670866626707516>'),intelligence=10,magie=10,turnInit=-1,unclearable=True,description="La douceur de Lio en a épaté plus d'un.\nÀ chaque soins réalisés par cette dernière, donne l'effet Sous le Charme III à l'allié soigné",callOnTrigger=charming2)
lioWeap = weapon("Écume","lioWeap",RANGE_LONG,AREA_CIRCLE_5,64,50,charisma=20,effect=lioWeapEff,effectOnUse=charming,use=MAGIE,emoji='<:lioWeap:908859876812415036>')
lioRez = skill("Eau purifiante","lioRez",TYPE_RESURECTION,0,100,AREA_MONO,ultimate=True,area=AREA_DONUT_7,use=CHARISMA,emoji='<:lioUlt:911738565703135293>',cooldown=3,say="Allez vous autre... C'est pas le moment de stagner...")
lieWeapEff = effect("Kitsune du feu","lieWeapEff",CHARISMA,emoji=uniqueEmoji('<:fireKitsune:917670925904785408>'),intelligence=10,magie=10,turnInit=-1,unclearable=True,description="L'ardeur de Liz en a comblé plus d'un\nÀ chaque attaque réalisée, donne l'effet Sous le Charme II à la cible",callOnTrigger=charming)
lieWeap = weapon("Braise","lieWeap",RANGE_LONG,AREA_CIRCLE_4,48,50,charisma=10,magie=10,area=AREA_CIRCLE_1,effect=lieWeapEff,effectOnUse=charming,use=MAGIE,emoji='<:lizWeap:908859856608460820>')
lieSkillEff = effect("Combustion","lieSKillEff",MAGIE,resistance=-2,power=35,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,stackable=True,emoji=uniqueEmoji('<:lizIndirect:917204753610571776>'))
lieSkill = skill("Flamme intérieur","lizSkill",TYPE_DAMAGE,0,effect=lieSkillEff,cooldown=3,power=80,say="Voyons voir si tu va pouvoir résister longtemps...",use=MAGIE,emoji='<:lizDirectSkill:917202291042435142>')
liaSkill = skill("Douce caresse","liaSkill",TYPE_DAMAGE,0,power=50,effect=[charming,charming,charming,charming,charming,charming],cooldown=5,use=MAGIE,say="Roh allez, détent toi un peu !")
liuSkillEff = effect("Endurance Terrestre","liuSkillEff",MAGIE,overhealth=75,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
liuSkill = skill("Reconstitution","liuSkill",TYPE_DAMAGE,0,power=70,use=MAGIE,cooldown=2,effectOnSelf=liuSkillEff,say="Oh je suis pas encore finie tu va voir !")

tablAllOcta.append(octarien("Liu",30,130,35,80,10,20,120,45,0,0,liuWeap,7,'<:liu:908754674449018890>',[earthStrike,earthCircle,rocklance,liuSkill],POIDS_PLUME,GENDER_FEMALE,"La plus sportive de sa fratterie\n\nChaque attaque à l'arme des Soeurs Kitsune applique l'état \"Sous le charme II\" qui diminue légèrement les statistiques de la cible","<:kitsuSisterDead:908756093101015100>",baseLvl=20,say=liuSays))
tablAllOcta.append(octarien("Lia",20,70,150,150,30,30,20,30,0,0,liaWeap,7,'<:lia:908754741226520656>',[airStrike,airCircle,storm2,liaSkill],POIDS_PLUME,GENDER_FEMALE,"La plus rapide et agile de sa fraterie\n\nChaque attaque à l'arme des Soeurs Kitsune applique l'état \"Sous le charme II\" qui diminue légèrement les statistiques de la cible","<:kitsuSisterDead:908756093101015100>",baseLvl=20,say=liaSays))
tablAllOcta.append(octarien("Lio",20,70,200,35,50,35,50,35,0,0,lioWeap,7,'<:lio:908754690769043546>',[revitalisation,eting,lioRez,veterHealSkill2],ALTRUISTE,GENDER_FEMALE,"La plus calme et tranquille de sa fraterie\n\nChaque attaque à l'arme des Soeurs Kitsune applique l'état \"Sous le charme II\" qui diminue légèrement les statistiques de la cible","<:kitsuSisterDead:908756093101015100>",baseLvl=20,say=lioSays))
tablAllOcta.append(octarien("Liz",10,70,80,35,20,35,200,35,0,0,lieWeap,7,'<:lie:908754710121574470>',[fireCircle,pyro,infinitFire,lieSkill],MAGE,GENDER_FEMALE,"La plus impulsive de sa fraterie\n\nChaque attaque à l'arme des Soeurs Kitsune applique l'état \"Sous le charme II\" qui diminue légèrement les statistiques de la cible","<:kitsuSisterDead:908756093101015100>",baseLvl=20,say=lizSays))

# Boss special skills ----------------------------------------------------------------
spamSkill1 = skill("A Call For You","aaa",TYPE_DAMAGE,0,70,area=AREA_CONE_3,sussess=50,emoji='<:call:892757436203671572>',cooldown=3,message="HOT {0} IN YOUR AREA HAVE A [[Message](https://fr.wikipedia.org/wiki/Message)] FOR [{2}] :")
spamSkill2 = skill("BIG SHOT","aaa",TYPE_DAMAGE,0,130,area=AREA_LINE_5,sussess=70,ultimate=True,cooldown=5,message="[[Press F1](https://forums.commentcamarche.net/forum/affich-19023080-press-f1-to-continue-del-to-enter-setup)] FOR HELP :",emoji='<:bigshot:892757453442277417>')
serenaSpe = skill("Libération","aaa",TYPE_UNIQUE,0,35,AREA_MONO,ultimate=True,cooldown=5,area=AREA_ALL_ENEMIES,description="Séréna fait imploser toutes les poudres de fées d'Estialba, infligeant des dégâts en fonction du nombre d'effets \"Poison d'Estialba\" et de leurs durées restantes",emoji=estal.emoji[0][0])
serenaSkill = skill("Propagation","aaa",TYPE_INDIRECT_DAMAGE,0,0,AREA_MONO,area=AREA_ALL_ENEMIES,cooldown=3,effect=[estal],emoji=estal.emoji[0][0])

jevilWeap = weapon("Trèfle","aaa",RANGE_DIST,AREA_CIRCLE_4,76,50,0,area=AREA_CONE_2,say="CHAOS, CHAOS, CATCH ME IF YOU CAN!",emoji='<:chaos:892857755143127090>',damageOnArmor=1.5)
jevilSkill1 = skill("Pics","aaa",TYPE_DAMAGE,0,70,area=AREA_CONE_3,range=AREA_DIST_5,sussess=60,emoji='<a:card:892855854712385637>',say="NU-HA!! I NEVER HAD SUCH FUN, FUN!!",cooldown=2,damageOnArmor=1.5)
jevilSkill2 = skill("Final Chaos","aaa",TYPE_DAMAGE,0,120,AREA_MONO,area=AREA_ALL_ENEMIES,say="KIDDING ! HERE'S MY FINAL CHAOS !",initCooldown=5,cooldown=10,emoji="<:devilknife:892855875600023592>",damageOnArmor=2)
ailillSkill = skill("Décapitage","aaa",TYPE_DAMAGE,0,1000,AREA_CIRCLE_1,initCooldown=5,cooldown=5,damageOnArmor=500,message="{0} a assez vu {2} :",emoji='<:decapitage:897846515979149322>',say="J'en ai assez de ta tête.")
lunaSpe = skill("Ténèbres Éternels","InfDarkLaunch",TYPE_DAMAGE,0,70,AREA_MONO,area=AREA_CIRCLE_7,emoji='<a:darkExplosion:899451335269822475>',say="Voyons voir comment vous allez résister à ça !",description="\n\nInvoque X **Convictions des Ténèbres**, X étant la taille de l'équipe bleue au début du combat.\nAprès 3 tours de chargement, Luna enveloppe le terrain de Ténèbres, infligeant des dégâts massifs à toute l'équipe en fonction du nombre de **Convictions des Ténèbres** présent sur le terrain\n\nDurant la période de chargement, Luna est **Invisible**, **Inciblable** et **Imunisée**",cooldown=99,initCooldown=10,damageOnArmor=1.33)
lunaRepEffect = effect("Cast - Ténèbres Éternels","darkerYetDarker3",replique=lunaSpe,turnInit=2,silent=True,emoji=uniqueEmoji("<a:lunaInfDarkTurn3:916575004492169226>"),immunity=True,translucide=True,untargetable=True)
lunaSpe2 = skill("Ténèbres Éternels","aab",TYPE_DAMAGE,0,0,AREA_MONO,area=AREA_DONUT_7,effectOnSelf=lunaRepEffect,say="On s'accroche toujours hein ?",message="Luna concentre les Ténèbres environants...",emoji='<:infiniteDarkness:898497770531455008>')
lunaWeap = weapon("Épee de l'ombre éternelle","aaa",RANGE_MELEE,AREA_CIRCLE_1,50,40,0,0,0,0,0,0,0,0,0,0,0,5,'<:lunaWeap:915358834543968348>',damageOnArmor=1.2)
lenaRepEffect2 = effect("Cast - Ténèbres Éternels","darkerYetDarker2",replique=lunaSpe2,turnInit=3,silent=True,emoji=uniqueEmoji('<a:lunaInfDarkTurn2:916574989933748235>'),immunity=True,translucide=True,untargetable=True)
lunaSpe3 = skill("Ténèbres Éternels","aac",TYPE_DAMAGE,0,0,AREA_MONO,area=AREA_DONUT_7,effectOnSelf=lenaRepEffect2,message="Luna concentre les Ténèbres environants...",emoji='<:infiniteDarkness:898497770531455008>')
lenaRepEffect3 = effect("Cast - Ténèbres Éternels","darkerYetDarker1",replique=lunaSpe3,turnInit=4,silent=True,emoji=uniqueEmoji('<a:lunaInfDarkTurn1:916574972321873951>'),immunity=True,translucide=True,untargetable=True)
lunaSpe4 = skill("Ténèbres Éternels","InfiniteDarkness",TYPE_DAMAGE,0,0,AREA_MONO,cooldown=99,initCooldown=8,area=AREA_DONUT_7,effectOnSelf=lenaRepEffect3,emoji='<:infiniteDarkness:898497770531455008>',say='OK ! FINI DE JOUER !')
lunaSkill = copy.deepcopy(soupledown)
lunaSkill.power = 120
lunaSkill2 = skill("Tank Burst","aaa",TYPE_DAMAGE,0,300,AREA_CIRCLE_2,cooldown=5,initCooldown=2,emoji='<a:lunaTB:899456356036251658>')
lunaSkill4Eff = copy.deepcopy(innerdarknessEff)
lunaSkill4Eff.stat = STRENGTH
lunaSkill4Eff.power = 55
lunaSkill4 = skill("Déchirment","aaa",TYPE_INDIRECT_DAMAGE,0,range=AREA_MONO,area=AREA_DIST_7,effect=lunaSkill4Eff,cooldown=5,use=MAGIC,say="Ne sentez vous pas les ténèbres de votre âme s'agiter ?",emoji=innerdarkness.emoji)
lunaSkill5 = skill("Assombrissement","lunaSkill5",TYPE_DAMAGE,0,100,AREA_MONO,cooldown=4,emoji='<:lunaSkill5:905401258658115615>',area=AREA_CIRCLE_2,say="Je comprend pas pourquoi vous tenez tant à vous mettre en travers de mon chemin")
jevilEff = effect("Confusion","giveup",silent=True,emoji=uniqueEmoji('<a:giveup:902383022354079814>'),turnInit=3,description="Confuse confusing confusion")
jevilSkill3 = skill("Confusion","aaa",TYPE_MALUS,0,range=AREA_MONO,area=AREA_ALL_ENTITES,effect=jevilEff,cooldown=5,emoji='<a:giveup:902383022354079814>',say='I CAN DO ANYTHING !')

clemBloodJauge = effect("Jauge de sang","clemBloodJauge",turnInit=-1,unclearable=True,emoji=uniqueEmoji('<:clemBJ:914710384299106345>'),lvl=100,description="Clémence possédée tourne autour de sa Jauge de Sang\n\nElle débute le combat avec une jauge à **100** Points de sang, son maximum.\nChacunes de ses compétences ont un coût en Points de Sang, qui sont retiré à la jauge à la fin de leur utilisation\n\nSi la jauge de sang tombe à **0 point**, Clémence est étourdie pendant 2 tours durant lesquels sa résistance est diminuée\nLa jauge de sang récupère **1 point** de sang à chaque fois que Clémence inflige 50 points de dégâts, et **100 points** une fois que Clémence n'est plus étourdie\n\nLa quantité de points de sang dans la jauge de sang est constamant visible\nClémence possède 10% de vol de vie")
clemWeapon = weapon("Rapière en argent lunaire","clemenceWeapon",RANGE_DIST,AREA_CIRCLE_1,85,100,use=MAGIE,effect=clemBloodJauge,magie=50,endurance=150,emoji='<:clemWeap:915358467773063208>')
clemStunEffect = effect("Thrombophilie","clemStun",stun=True,emoji=uniqueEmoji("<:stun:882597448898474024>"),turnInit=3,type=TYPE_MALUS,resistance=-85)
aliceStunEffect = effect("Hémophilie","aliceStun",stun=True,emoji=uniqueEmoji("<:stun:882597448898474024>"),turnInit=3,type=TYPE_MALUS,charisma=-50)
clemSkill1 = skill("Rune - Lune de Sang","clemSkill1",TYPE_DAMAGE,0,power=230,range=AREA_MONO,area=AREA_CIRCLE_3,emoji='<a:clemSkill1:901147227588812890>',cooldown=2,initCooldown=2,use=MAGIE)
clemSkill2 = skill("Sort - Chiroptera perniciosius","clemSkill2",TYPE_DAMAGE,0,350,AREA_CIRCLE_2,cooldown=3,emoji='<a:clemSkill4:901150027706142780>',use=MAGIE,say="Tu es trop collant.")
clemUltLauch = skill("Memento - L'Ange noir","clemUlt",TYPE_DAMAGE,0,300,AREA_MONO,area=AREA_CIRCLE_7,emoji='<:clemMemento:902222089472327760>',say="Vous avez suffisamant résisté comme ça !",sussess=666,cooldown=99,ultimate=True,description="Au premier tour, consomme tous les **Points de sang** de la Jauge de Sang, sauf 1, pour obtenir un bouclier absolu, dont la puissance dépend du nombre de points consommés\nAu second tour, si ce bouclier est toujours présent, cette attaque fait des dégâts colosaux. Consomme la jauge de sang",use=MAGIE)
clemultCastEffect = effect("Cast - Memento - L'Ange noir","clemUltEff",replique=clemUltLauch,turnInit=2,silent=True,emoji=dangerEm)
clemUltShield = effect("Bouclier sanguin","clemShield",MAGIE,overhealth=1,emoji=uniqueEmoji("<:clemMemento2:902222663806775428>"),turnInit=2,absolutShield=True)
clemUltCast = skill("Memento - L'Ange Noir","clemUltCast",TYPE_ARMOR,0,range=AREA_MONO,emoji="<:clemMemento2:902222663806775428>",effect=clemUltShield,say="Très bien.",effectOnSelf=clemultCastEffect,ultimate=True,cooldown=99)
clemSkill3 = skill("Rune - Demi-Lune","clemSkill3",TYPE_DAMAGE,0,150,AREA_CIRCLE_3,area=AREA_ARC_2,cooldown=2,use=MAGIE,emoji='<a:clemSkill3:914759077551308844>')
clemSkill4 = skill("Sort - Chiroptera vastare","clemSkill4",TYPE_DAMAGE,0,320,AREA_MONO,area=AREA_DIST_7,cooldown=4,use=MAGIE,say="Vous pensez que vous êtes à l'abri là bas ?",emoji='<a:clemSkill4:914756335860596737>')

clemBJcost = {"clemSkill1":25,"clemSkill2":32,"clemUlt":100,"clemSkill3":30,"clemSkill4":35,"aliceSkill1":28,"aliceSkill2":25,"aliceSkill3":28,"aliceSkill4":35,"aliceRez":45}

TGESWeap = weapon("noneWeap","aaa",RANGE_DIST,AREA_CIRCLE_1,0,0,0,resistance=50)
TGESSkill1 = skill("Projectile","TheGiantEnemySpiderSkill1",TYPE_DAMAGE,0,int(GESLskill.power*1.5))

tablBoss = [ # Table des boss
    octarien("Ailill",300,50,0,50,75,50,30,10,33,0,depha,10,'<a:Ailill:882040705814503434>',[balayette,uppercut,ailillSkill],BERSERK,GENDER_FEMALE,description="Une humaine à qui la vie n'a pas vraiment souris. Du coup elle passe ses nerfs sur les autres.\nEnfin les autres plus faibles qu'elle évidamment\n\nSi il y a 5 combattants ou plus dans une équipe, les dégâts infligés à Ailill sont réduits si l'attaquant est trop éloigné",say=ailillSays,rez=False),
    octarien("[[Spamton Neo](https://deltarune.fandom.com/wiki/Spamton)]",500,1450,100,45,45,200,200,30,33,15,bigshot,45,'<a:spamton:892749040205316138>',skill=[spamSkill1,spamSkill2],description="NOW IT'S YOUR CHANCE TO BE A [Big shot] !",deadIcon='<:spamblocked:892750635315912746>',oneVAll=True,say=spamtonSays),
    octarien("Jevil",550,1500,100,60,75,120,120,10,25,15,jevilWeap,50,'<a:CHAOS:762276118224961556>',[chaos,jevilSkill1,jevilSkill2,jevilSkill3],description="I CAN DO ANYTHING !",deadIcon='<:chaosnt:892857736642064455>',oneVAll=True,say=jevilSays),
    octarien("Séréna",50,65,-50,70,50,50,300,25,0,15,armilame,10,'<:serena:897912402354511894>',[poisonus,serenaSkill,serenaSpe],ENCHANTEUR,GENDER_FEMALE,rez=False,deadIcon='<:flowernt:894550324705120266>'),
    octarien("Luna",400,1250,100,75,50,100,0,25,35,25,lunaWeap,50,'<:luna:909047362868105227>',[lunaSpe4,lunaSkill,lunaSkill5,lunaSkill2,lunaSkill4],POIDS_PLUME,GENDER_FEMALE,"Il viendra toujours un moment où vous allez devoir affronter votre côté sombre",'<:spIka:866465882540605470>',True,say=lunaBossSays),
    octarien("Octo Tour",0,350,0,0,0,0,0,50,0,0,octoTour,12,'<:tower:905169617163538442>',[octoTourSkill],PROTECTEUR,rez=False,description="Une tour de siège. Tant qu'elle est en vie, tous les dégâts directs reçu par ses alliés lui sont redirigés"),
    octarien("Clémence pos.",100,1200,50,50,80,150,325,35,20,0,clemWeapon,50,'<a:clemPos:914709222116175922>',[clemSkill1,clemSkill2,clemUltCast,clemSkill3,clemSkill4],MAGE,GENDER_FEMALE,"Durant l'une de ses aventures, Clémence a commis l'erreur de baisser sa garde, et une entité malveillante en a profiter pour se loger dans son esprit, perturbant sa vision de la réalitée et manipulant ses émotions",oneVAll=True,deadIcon='<:clemence:908902579554111549>',say=clemPosSays),
    octarien("The Giant Enemy Spider",300,1500,0,80,100,50,300,70,10,20,TGESWeap,50,'<:TGES:917302938785968148>',[TGESSkill1],description="En début de combat, invoque 8 __\"Patte de The Giant Enemy Spider\"__ autour de lui",oneVAll=True)
]

clemInnerDark = copy.deepcopy(innerdarkness)
aliceOnStage = copy.deepcopy(onstage)
aliceOnStage.say = "Hé ! Hé ! J'ai une avant première pour vous tous, vous en pensez quoi ?"
lohicaFocal = copy.deepcopy(focal)
lohicaFocal.say = "Vous commencez sérieusement à me tapez sur les nerfs..."

lenaChangeDict = createTpmChangeDict(30,0,[bigMonoLaser2],[tripleMissiles],35)
aliceChangeDict = createTpmChangeDict(1,0,[roses],[rosesMagic],50)

# Alliés temporaires
tablAllAllies = [
    tmpAllie("Lena",1,light_blue,OBSERVATEUR,splatcharger,[amethystEarRings,lightBlueJacket,lightBlueFlats],GENDER_FEMALE,[splatbomb,bigMonoLaser2,trans,shot,multishot],"Une inkling qui en a vu des vertes et des pas murs.\nPréfère rester loin de la mêlée et abattre ses ennemis à bonne distance","https://cdn.discordapp.com/emojis/899120815205929010.png",ELEMENT_WATER,icon='<:lena:909047343876288552>',bonusPoints=[STRENGTH,PRECISION],say=lenaSays,changeDict=lenaChangeDict),
    tmpAllie("Gwendoline",2,yellow,POIDS_PLUME,roller,[anakiMask,FIACNf,blackFlat],GENDER_FEMALE,[defi,splashdown,balayette,airStrike],"Bien qu'elle essaye de l'éviter, cette jeune femme se retrouve toujours à devoir en venir aux mains pour se débarraser des gros lourds de la première ligne ennemie.\nIl est vrai aussi qu'elle n'est pas toute seule dans sa tête","https://cdn.discordapp.com/emojis/906303014665617478.png",ELEMENT_AIR,bonusPoints=[STRENGTH,ENDURANCE],icon='<:gweny:906303014665617478>'),
    tmpAllie("Clémence",2,red,MAGE,rapiere,[shihuHat,shihuDress,shihuShoe],GENDER_FEMALE,[memClemCastSkill,dark2,dark3,invocCarbE,invocCarbunR],"Clémence est née orpheline, ses parents ayant été tués par des chasseresses d'Arthémis peut après sa naissance.\nElle fût donc élevée par des chauve-souris dans une grotte pendant une bonne partie de son enfance\nCependant, elle rencontra dans un lieu nommé la \"Ville Onirique\", une ville magique accessible via les rêves permettant aux vampires vivants comme mort de s'y retrouver, une jeune vampire majeure du nom de Ruby.\nCette dernière lui apprit les bases de la magie au fils des années, ainsi que celles des sociétés humaines que les chauve-souris pouvaient évidamment pas lui apprendre.\n\nMalgré tout, elle manquait d'amis vampire \"réels\", Ruby habitant à des centaines de kilomètres dans la réalité. Elle alla donc, par une belle soirée d'Haloween, mordre une jeune femme envers laquelle Clémence avait un bon sentiment.\nOn peut dire que sur tous les choix qu'elle a fait, ça allait être celui qui allait être le plus lourd en conséquence, dans de bons comme mauvais thermes.\n\nJe vous en passe et des meilleurs, sinon je vais casser la limite de caractères, mais en grandissant, Clémence a continué son apprentissage de la magie et a décidé de parcourir le monde pour étudier les Anciennes Runes ainsi que pour purifier les artéfacts maudits qui tourmentent les monstres pour éviter qu'ils se fassent chasser par les humains, tel ses parents biologiques",ELEMENT_DARKNESS,icon='<:clemence:908902579554111549>',bonusPoints=[MAGIE,STRENGTH],say=clemSays,deadIcon='<:AliceOut:908756108045332570>'),
    tmpAllie("Alice",1,aliceColor,IDOLE,mic,[batRuban,aliceDress,aliceShoes],GENDER_FEMALE,[invocBat2,vampirisme,renisurection,roses,aliceOnStage],"Alice est la petite dernière des trois sœurs Kohishu, et la seule à être une vampire\n\nDès son plus jeune âge, elle a fortement démontré sa volontée à vouloir être le centre de l'attention, bien que ça ai frustrée sa sœur ainée. En grandissant, cette envie de reconnaissance ne s'est pas vraiment tarie, et a réussi grâce à son charme naturel à devenir rapidement une fille populaire\n\nElle décida de suivre la voie de sa mère et de devenir une chanteuse renommé, c'est ainsi qu'elle participa au concours de jeune talent de son école et réussi à se faire remarquer par une maison de disque qui recherchait de jeunes chanteurs\n\nLorsqu'elle n'est pas retenue par ses obligations, elle aime bien accompagner Félicité et Clémence dans leurs aventures, mais refuse de participer activement aux combats. À la place elle les encourages avec ses chansons légèrement magiques",ELEMENT_LIGHT,icon='<:alice:908902054959939664>',bonusPoints=[CHARISMA,INTELLIGENCE],say=aliceSays,deadIcon='<:AliceOut:908756108045332570>',changeDict=aliceChangeDict),
    tmpAllie("Shushi",1,blue,ENCHANTEUR,airspell,[tankmage3,tankmage2,tankmage1],GENDER_FEMALE,[ferocite,invocCarbT,storm2,storm,suppr],"Jeune inkling pas très douée pour le combat, à la place elle essaye de gagner du temps pour permettre à ses alliés d'éliminer l'équipe adverse","https://cdn.discordapp.com/emojis/899117520211042334.png",ELEMENT_AIR,icon='<:shushi:909047653524963328>',bonusPoints=[MAGIE,ENDURANCE],say=shushiSays),
    tmpAllie("Lohica",1,purple,MAGE,butterflyP,[old,robeLoliBlue,blueFlat],GENDER_FEMALE,[lohicaFocal,poisonus,heriteEstialba,dark2],"Une fée à l'histoire bien mouvementée. Spécialisée dans les poisons","https://cdn.discordapp.com/emojis/899694452334022706.png",ELEMENT_DARKNESS,bonusPoints=[MAGIE,STRENGTH],icon='<a:lohicaGif:900378281877057658>',deadIcon='<:flowernt:894550324705120266>'),
    tmpAllie("Hélène",2,white,ALTRUISTE,serringue,[barrette,heleneDress,heleneShoe],GENDER_FEMALE,[cure,lapSkill,renisurection,eting,lightHeal2],"Une fée qui estime qu'essayer de sauver la vie de ses alliés est plus efficace que si elle esseyait de terminer le combat elle-même","https://cdn.discordapp.com/emojis/906303162854543390.png",ELEMENT_LIGHT,bonusPoints=[CHARISMA,INTELLIGENCE],icon='<:helene:906303162854543390>'),
    tmpAllie("Félicité",1,red,BERSERK,dtsword,[celestBronzeHat,celestBronzeArmor,celestBronzeBoots],GENDER_FEMALE,[defi,uppercut,strengthOfWillCast,highkick,bloodyStrike],"Soeur ainée de Sixtine et Alice, Félicité est née dans un monde désolé et post apocaliptique\n\n<:lena:909047343876288552> : Mais parle pour toi !\n\nN'ayant plus aucun humain dans ce monde pas si désolé et pas si post apocaliptique, elle hérita de l'âme de Détermination de ce monde (ainsi que quelques bénédictions de dieux grecs mais c'est une autre histoire\n\nEn grandissant, ces dites bénédictions lui ont permis de développer rapidement son esprit et ses capacités, mais aussi d'attirer sur elle tous les monstres mythologiques du coin. Fort heureusement elle pu compter sur ses parents ainsi que sur sa sœur adoptive ainnée Clémence pour la protéger jusqu'au jour où elle en a eu marre de devoir laisser les autres la défendre.\nElle alla donc trouver les seuls autres personnes avec des âmes de Détermination à sa connaissance : Frisk et Chara, qui lui apprirent les bases. Sa volontée ainsi que ses bénédictions lui permirent de rapidement faire des progrès dans l'escrime, quand pour la maîtrise de la magie, c'est grâce à Hécate qu'elle le doit\n\nEn grandissant, elle a choisi une voie plus ou moins similaire à celle de Clémence, c'est à dire de chercher à purifier des artéfacts maudits agitants les monstres alentours ainsi que l'étude d'ancienne magie. Cependant, là où Féli le fait pour protéger les populations d'hommes, Clémence le fait pour protéger les monstres de ces derniers. Mais ça ne les empêche pas de faire équipe de temps en temps. Après tout le but reste le même",bonusPoints=[ENDURANCE,STRENGTH],icon='<:felicite:909048027644317706>'),
    tmpAllie("Akira",2,black,TETE_BRULE,fauc,[anakiMask,heartSphapeObject,hyperlink],GENDER_MALE,[defi,balayette,highkick,bleedingDague,demolish],"Flora si tu as une description je veux bien","https://cdn.discordapp.com/emojis/899693936199753779.png",ELEMENT_DARKNESS,bonusPoints=[ENDURANCE,STRENGTH],icon='<:akira:909048455828238347>'),
    tmpAllie("Icealia",2,light_blue,PREVOYANT,blueButterfly,[blueCharpe,blueChemVeste,blueButterFlyBoots],GENDER_FEMALE,[soulagement,inkarmor,kralamSkill,convert,onde],"Une érudite qui préfère protéger ses compagnons",element=ELEMENT_LIGHT,bonusPoints=[INTELLIGENCE,ENDURANCE],icon='<:icealia:909065559516250112>'),
    tmpAllie("Powehi",2,black,PROTECTEUR,inkbrella2,[starBar,bhPull,bhBoots],GENDER_FEMALE,[blackHole,trans,blindage,secondWind,blackHole2],"Une manifestation cosmique d'un trou noir. Si vous vous sentez attiré par elle, c'est probablement à raison\nNe lui demandez pas de vous marchez dessus par contre, si vous voulez un conseil. Elle a beau paraître avoir un petit gabarie, ce n'est pas pour rien qu'elle évite de marcher sur le sol",element=ELEMENT_SPACE,bonusPoints=[ENDURANCE,INTELLIGENCE],icon='<:powehi:909048473666596905>',deadIcon = '<:powehiDisiped:907326521641955399>',say=powehiSays),
    tmpAllie("Shehisa",1,purple,TETE_BRULE,shehisa,[shehisaMask,shehisaBody,shehisaBoots],GENDER_FEMALE,[dissimulation,bleedingDague,bleedingArrow,bleedingTrap,heriteLesath],"Soeur d'Hélène, elle a cependant préférer suivre un chemin beaucoup moins altruiste",element=ELEMENT_NEUTRAL,bonusPoints=[STRENGTH,ENDURANCE],icon='<:shehisa:901555930066473000>'),
    tmpAllie("Rasalhague",1,light_blue,MAGE,spellBook,[lentille,chemB,mocas],GENDER_MALE,[space1,space2,space3,spaceSp],element=ELEMENT_SPACE,icon='<:rasalhague:907689992745271376>',bonusPoints=[MAGIE]),
    tmpAllie("Sixtine",1,blue,PREVOYANT,lightSpellBook,[blueNoeud,pullHeart,heartBask],icon='<:sixtine:908819887059763261>',skill=[bpotion,affaiblissement,nostalgia,provo,sixtineUlt],gender=GENDER_FEMALE,element=ELEMENT_NEUTRAL,bonusPoints=[INTELLIGENCE,ENDURANCE],description="Soeur cadette, Sixtine est plutôt du genre à vouloir rester dans son coin sans être dérangée\n\nElle ne se démarque pas particulièrement de Félicité ou Alice, mais ça ne la dérange pas. Elle passe le plus clair de son temps libre à rêvasser, à du mal à faire le premier pas vers les autres et n'a pas vraiment l'air de s'interresser à grand chose\nMais quand elle s'interresse à un truc, elle veux souvent en connaître un maximum de chose dessus."),
    tmpAllie("Hina",1,purple,OBSERVATEUR,plume,[hinaAcc,hinaBody,hinaShoes],GENDER_FEMALE,[multishot,multiMissiles,hinaUlt],icon='<:hina:908820821185810454>',element=ELEMENT_AIR,bonusPoints=[AGILITY,STRENGTH]),
    tmpAllie("John",2,orange,POIDS_PLUME,airsword,[bandNoir,pullCamo,kanisand],GENDER_MALE,[airlame,airStrike],description="Un Loup Garou qui a réussi à tomber amoureux de la vampire responsable des pluparts des vas et viens à l'infirmerie du village de sa meute\n\nAprès de multiple tentatives de l'approcher sans grand succès, il a réussi à changer la clémence qu'éprouvait cette dernière à son égars en affection, mais a peur d'essayer de monter dans son estime",icon='<:john:908887592756449311>',bonusPoints=[STRENGTH,AGILITY],say=johnSays),
    tmpAllie("Julie",1,red,ALTRUISTE,julieWeap,[julieHat,julieDress,julieShoes],GENDER_FEMALE,[altOH,infraMedica,extraEtingSkill,timeSp,trans],"La principale (et unique) servante d'une des vampires les plus puissante du pays.\nElle a appris la magie curative à l'aide des nombreux grimoires dans la bibliothèque du manoire, mais il lui arrive souvent de demander de l'aide à Clémence lorsque sa maîtresse (qui ai d'ailleurs la tutrice magique de cette dernière) lui demande de récupérer des organes de monstres.\nElle se sent souvent petite, en compagnie de ces puissantes vampires\n\nDire qu'elle est légèrement inspirée serait un euphémisme. Au moins elle utilise pas de dagues",element=ELEMENT_TIME,bonusPoints=[CHARISMA,INTELLIGENCE],icon="<:julie:910185448951906325>"),
    tmpAllie("Krys",2,purple,TETE_BRULE,krystalFist,[kryscharpe,krysshirt,kryschains],GENDER_OTHER,[krysUlt,earthStrike,mudlame,rocklance],"placeholder.krys.desc",element=ELEMENT_EARTH,icon="<:krys:916118008991215726>",deadIcon='<:krysCan:916117137339322388>',bonusPoints=[ENDURANCE,STRENGTH])
]

# Shushi alt spells
shushiSkill1 = skill("Frappe lumineuse","aaa",TYPE_DAMAGE,0,80,cooldown=3,use=MAGIE,emoji='<a:ShushiLF:900088862871781427>')
shushiSkill3Eff = effect("Jeu de lumière","diff",redirection=35,trigger=TRIGGER_DAMAGE,description="Un habile jeu de lumière permet de vous cacher de vos ennemis")
shushiSkill3 = skill("Diffraction","aaa",TYPE_ARMOR,0,0,AREA_CIRCLE_6,effect=shushiSkill3Eff,cooldown=5,initCooldown=2,use=None,emoji='<a:diffraction:916260345054658590>')
shushiSkill4Eff = effect("Assimilation","assimil",MAGIE,resistance=5,overhealth=35,description="Grâce à Shihu, vous avez réussi à utiliser les Ténèbres environant à votre avantage",emoji=uniqueEmoji("<:tarmor:909134091604090880>"),type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
shushiSkill4 = skill("Assimilation","aaa",TYPE_ARMOR,0,cooldown=3,effect=shushiSkill4Eff,say='On peut y awiver !',use=MAGIE,emoji='<:assimilation:916260679944634368>')
shushiWeapEff = effect("Lueur Ténébreuse","darkLight",MAGIE,resistance=5,overhealth=15,type=TYPE_ARMOR,emoji=uniqueEmoji('<:dualMagie:899628510463803393>'))
shushiWeap = weapon("Magie trancendante","dualMagie",RANGE_LONG,AREA_DONUT_5,35,100,0,strength=-20,endurance=10,charisma=20,intelligence=20,magie=55,type=TYPE_HEAL,target=ALLIES,use=MAGIE,effectOnUse=shushiWeapEff,affinity=ELEMENT_LIGHT,emoji='<:dualMagie:899628510463803393>')
shushiHat = stuff("Barrête de la cohabitation","dualHat",0,0,strength=-20,endurance=15,charisma=20,agility=10,precision=10,intelligence=20,magie=45,affinity=ELEMENT_LIGHT,emoji='<:coaDress:911659797076660294>')
shushiDress = stuff("Robe de la cohabitation","dualDress",1,0,strength=-10,endurance=35,charisma=20,agility=0,precision=10,intelligence=10,magie=60,resistance=20,affinity=ELEMENT_LIGHT,emoji='<:coaBar:911659734812229662>')
shushiBoots = stuff("Bottines de la cohabitation","dualBoost",2,0,strength=-10,endurance=15,charisma=0,agility=20,precision=10,magie=45,intelligence=10,affinity=ELEMENT_LIGHT,emoji='<:coaBoots:911659778995007528>')
shushiSkill5 = skill("Lumière éternelle","LumEt",TYPE_RESURECTION,0,100,emoji='<:renisurection:873723658315644938>',cooldown=3,description="Permet de ressuciter un allié",use=MAGIE,range=AREA_DONUT_7)
shushiArmorSkillEff = effect("Armure Harmonique","shushiArmor",MAGIE,overhealth=75,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji("<a:transArmorB:900037831257358378>"))
shushiArmorSkill = skill("Armure Harmonique","shushiArmorSkill",TYPE_ARMOR,0,effect=shushiArmorSkillEff,range=AREA_MONO,area=AREA_CIRCLE_5,cooldown=7,use=MAGIE,emoji='<a:transArmorB:900037831257358378>')

shihuDarkBoom1 = copy.deepcopy(explosion)
shihuDarkBoom2 = copy.deepcopy(explosion2)
shihuDarkBoomEff = copy.deepcopy(castExplo)
shihuDarkBoom1.emoji= '<a:darkExplosion:899451335269822475>'
shihuDarkBoom1.id = "ShihuDarkBoomLaunch"
shihuDarkBoom1.say = "Za va fire Boum Boum !"
shihuDarkBoom1.name, shihuDarkBoom1.repetition, shihuDarkBoom1.power = "Explosion Noire",2,int(explosion.power * 0.45)

shihuDarkBoomEff.replica = shihuDarkBoom1
shihuDarkBoomEff.id = "ShihuDarkBoomEff"
shihuDarkBoom2.effectOnSelf, shihuDarkBoom2.name,shihuDarkBoom2.emoji = shihuDarkBoomEff,"Explosion Noire",'<a:darkExplosion:899451335269822475>'
shihuDarkBoom2.id = "ShihuDarkBoom"

aliceBloodJauge = copy.deepcopy(clemBloodJauge)
aliceBloodJauge.emoji = uniqueEmoji("<:aliceBJ:914798086667264010>")
aliceBloodJauge.description = "Alice exaltée tourne autour de sa Jauge de Sang\n\nElle débute le combat avec une jauge à **100** Points de sang, son maximum.\nChacunes de ses compétences ont un coût en Points de Sang, qui sont retiré à la jauge à la fin de leur utilisation\n\nSi la jauge de sang tombe à **0 point**, Alice est étourdie pendant 2 tours durant lesquels sa résistance est diminuée\nLa jauge de sang récupère **1 point** de sang à chaque fois que Alice soigne 50 points de vie, et **100 points** une fois qu'Alice n'est plus étourdie\n\nLa quantité de points de sang dans la jauge de sang est constamant visible"

aliceExHeadruban = stuff("Ruban vampirique","aliceExHead",0,0,charisma=40,negativeHeal=-50,endurance=55,emoji=batRuban.emoji)
aliceExDress = stuff("Robe vampirique","aliceExDress",1,0,endurance=10,resistance=15,charisma=45,negativeHeal=-25,emoji=aliceDress.emoji)
aliceExShoes = stuff("Ballerines vampiriques","aliceExShoes",2,0,agility=25,charisma=45,negativeHeal=-35,endurance=5,emoji=aliceShoes.emoji)

aliceExWeapEff = effect("Bénédiction vampirique","aliceExWeapEff",CHARISMA,emoji=uniqueEmoji("<:vampire:900312789686571018>"),power=7,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_AFTER_DAMAGE,description="Cet effect confère **{0}%** de Vol de Vie au porteur.\nLe pourcentage de convertion est augmenté par les statistiques du lanceur")
aliceExWeap = weapon("Rosa receptaculum","aliceExWeap",RANGE_DIST,AREA_CIRCLE_5,25,100,0,charisma=35,resistance=10,type=TYPE_HEAL,target=ALLIES,effectOnUse=aliceExWeapEff,effect=aliceBloodJauge,emoji='<:vampBall:916199488891273276>')
aliceSkill1Eff = effect("Régénération vampirique","aliceRegenEff",CHARISMA,power=15,emoji=uniqueEmoji("<a:aliceSkill1:914787461949960202>"),type=TYPE_INDIRECT_HEAL,turnInit=3,lvl=3,area=AREA_CIRCLE_2,description="Au début du tour du porteur, lui et ses alliés proches recoivent des soins",trigger=TRIGGER_START_OF_TURN)
aliceSkill1 = skill("Sort - Rénégération","aliceSkill1",TYPE_INDIRECT_HEAL,0,0,emoji="<a:aliceSkill1:914787461949960202>",effect=aliceSkill1Eff,cooldown=3)
aliceSkill2Eff = effect("Galvanision vampirique","aliceBoostEff",CHARISMA,strength=10,magie=10,critical=5,emoji=uniqueEmoji('<a:aliceSkill2:914791502931197962>'))
aliceSkill2 = skill("Sort - Galvanisation","aliceSkill2",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_3,effect=aliceSkill2Eff,cooldown=1,emoji='<a:aliceSkill2:914791502931197962>')
aliceSkill3 = skill("Rune - Flos luminosus","aliceSkill3",TYPE_DAMAGE,0,100,emoji='<a:aliceSkill3:914794172215623690>',cooldown=2,use=CHARISMA)
aliceSkill4 = skill("Rune - Pleine lune","aliceSkill4",TYPE_HEAL,0,100,AREA_MONO,area=AREA_CIRCLE_3,use=CHARISMA,cooldown=3,emoji='<a:aliceSkill4:914796355925458984>')
aliceRez = skill("Memento - Voie de l'Ange II","aliceRez",TYPE_RESURECTION,0,250,range=AREA_CIRCLE_7,emoji="<a:memAlice2:908424319900745768>",use=CHARISMA)

tablVarAllies = [
    tmpAllie("Luna",1,black,POIDS_PLUME,kcharger,[lunaPandan,lunaDress,lunaBoots],GENDER_FEMALE,[defi,splatbomb,balayette,soupledown,highkick],"Là où se trouve la Lumière se trouvent les Ténèbres","https://cdn.discordapp.com/emojis/899120831152680971.png?size=96",ELEMENT_DARKNESS,variant=True,icon='<:luna:909047362868105227>',bonusPoints=[STRENGTH,ENDURANCE],say=lunaSays),
    tmpAllie("Altikia",2,yellow,PROTECTEUR,inkbrella,[maidHat,yellowpull,maidHeels],GENDER_FEMALE,[ironWillSkill,lightAura2,inkarmor,renisurection,concen],"Une personnalité de Gwen qui préfère se concentrer sur ses alliés","https://cdn.discordapp.com/emojis/906303048542990347.png",ELEMENT_LIGHT,variant=True,bonusPoints=[ENDURANCE,CHARISMA],icon='<:alty:906303048542990347>'),
    tmpAllie("Klironovia",2,yellow,BERSERK,klikliSword,[darkMaidPendants,FIACNf,blackFlat],GENDER_FEMALE,[defi,demolish,bloodyStrike,trans,highkick],"Une personnalité de Gwen bien plus violente que les deux autres","https://cdn.discordapp.com/emojis/906303031837073429.png",ELEMENT_EARTH,variant=True,bonusPoints=[STRENGTH,AGILITY],icon='<:klikli:906303031837073429>'),
    tmpAllie("Shihu",1,black,MAGE,darkSpellBook,[shihuHat,shihuDress,shihuShoe],GENDER_FEMALE,[dark2,dark3,shihuDarkBoom2,suppr],"\"Eye veut zuste un pi d'attenchions...\" - Shushi","https://cdn.discordapp.com/emojis/899117502800461824.png?size=96",ELEMENT_DARKNESS,variant=True,icon='<:shihu:909047672541945927>',bonusPoints=[MAGIE,STRENGTH],say=shihuSays),
    tmpAllie("Shushi Cohabitée",1,blue,PREVOYANT,shushiWeap,[shushiHat,shushiDress,shushiBoots],GENDER_FEMALE,[shushiSkill1,shushiArmorSkill,shushiSkill3,shushiSkill4,shushiSkill5],"S'étant comprise l'une et l'autre, Shushi et Shihu ont décidé de se liguer contre la mère de cette dernière.\nCette allié temporaire n'apparait que contre le boss \"Luna\"","https://cdn.discordapp.com/emojis/899608664770506783.png?size=96",ELEMENT_LIGHT,True,icon='<:shushiCoa:915488591654842368>',bonusPoints=[MAGIE,AGILITY]),
    tmpAllie("Alice Exaltée",1,aliceColor,IDOLE,aliceExWeap,[aliceExHeadruban,aliceExDress,aliceExShoes],GENDER_FEMALE,[aliceSkill1,aliceSkill2,aliceSkill3,aliceSkill4,aliceRez],"Voyant qu'elle n'arriverai pas à ramener sa sœur à la raison, Alice a décider d'aller contre ses principes et de révéler toute sa puissance vampirique pour tenter de redresser la balance.\nN'apparait que contre Clémence possédée",element=ELEMENT_LIGHT,variant=True,deadIcon="<:AliceOut:908756108045332570>",icon="<a:aliceExalte:914782398451953685>",bonusPoints=[CHARISMA,ENDURANCE],say=aliceExSays)
]

if not(isLenapy):
    print("\nVérification de l'équilibrage des stuffs...")
    allstats = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for a in stuffs+weapons:
        ballerine = a.allStats()+[a.resistance,a.percing,a.critical]
        babie = [a.negativeHeal,a.negativeBoost,a.negativeShield,a.negativeDirect,a.negativeIndirect]
        sumation = 0
        for b in range(0,len(ballerine)):
            sumation += ballerine[b]
            allstats[b] += ballerine[b]

        for b in babie:
            sumation -= b

        if sumation != 20 and a.effect == None and a.name != "Claquettes chaussettes":
            print("{0} n'a pas le bon cumul de stats : {1}".format(a.name,sumation))

        elif sumation != 10 and a.effect != None:
            print("{0} n'a pas le bon cumul de stats : {1}".format(a.name,sumation))

    temp = "\nDistribution des statistiques :\n"
    total = 0
    for a in allstats:
        total += a

    for a in range(0,len(allStatsNames)):
        temp += "{0} : {1}% ({2})\n".format(allStatsNames[a],round(allstats[a]/total*100,2),allstats[a])
    print(temp)

    lvlTabl = [{"level":0,"nombre":0}]
    for equip in stuffs:
        find = False
        for temp in lvlTabl:
            if temp["level"] == equip.minLvl:
                temp["nombre"]+=1
                find = True
                break

        if not(find):
            lvlTabl.append({"level":equip.minLvl,"nombre":1})

    lenStuff = len(stuffs)
    lvlTabl.sort(key=lambda ballerine: ballerine["level"])

    for temp in lvlTabl:
        print("Objets de niveau {0} : {1} ({2})%, statsAttendues : {3}".format(temp["level"],temp["nombre"],round(temp["nombre"]/lenStuff*100,2),10 + (temp["level"] * 2)))

    tabl = copy.deepcopy(tablAllAllies)
    tablTank = []
    tablMid = []
    tablBack = []

    for allie in tabl:
        [tablTank,tablMid,tablBack][allie.weapon.range].append(allie)

    print("")
    for num in range(3):
        print("Nombre de Temp's en {0} : {1}".format(["mêlée","distance","backline"][num],len([tablTank,tablMid,tablBack][num])))

    tabl = copy.deepcopy(tablAllOcta)
    alReadySeen = []
    tablTank = []
    tablMid = []
    tablBack = []

    for ennemi in tabl:
        if ennemi.name not in alReadySeen:
            [tablTank,tablMid,tablBack][ennemi.weapon.range].append(ennemi)
            alReadySeen.append(ennemi.name)
            stat = ennemi.allStats()+[ennemi.resistance,ennemi.percing,ennemi.critical]
            summ = 0
            for a in stat:
                summ += a

            awaited = int((230+110*3)*0.9)
            if summ < awaited*0.9 or summ > awaited*1.1:
                print("{0} n'a pas le bon cumul de stats : {1} ({2})".format(ennemi.name,summ,awaited))

    print("")
    for num in range(3):
        print("Nombre d'ennemis en {0} : {1}".format(["mêlée","distance","backline"][num],len([tablTank,tablMid,tablBack][num])))

    print("\nVérification de l'équilibrage des stuffs terminée")

def findWeapon(WeaponId) -> weapon:
    typi = type(WeaponId)
    if typi == weapon:
        return WeaponId

    elif type(WeaponId) != str:
        return None
    else:
        rep,id = None,WeaponId

        if WeaponId.startswith("\n"):
            id = WeaponId[-2:]
        for a in weapons:
            if a.id == id or a.name.lower() == id.lower():
                rep = a
                break
    
        return rep

def findSkill(skillId) -> skill:
    """Renvoie une compétence Skill, si trouvé"""
    typi = type(skillId)
    if typi == skill:
        return skillId

    elif type(skillId) != str or skillId == "0":
        return None
    else:
        if skillId.startswith("\n"):
            skillId = skillId[-2:]
        for a in skills:
            if a.id == skillId or a.name.lower() == skillId.lower():
                return a

        #print("ID non trouvée : ",skillId)
        return None

def findStuff(stuffId) -> stuff:
    """Renvoie un équipement Stuff, si trouvé"""
    typi = type(stuffId)
    if typi == stuff:
        return stuffId

    elif type(stuffId) != str:
        return None
    else:
        rep,id = None,stuffId
        if stuffId.startswith("\n"):
            id = stuffId[-2:]
        for a in stuffs:
            if a.id == id or a.name.lower() == id.lower():
                rep = a
                break

        return rep

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

def findOther(otherId) -> other:
    if type(otherId) == other:
        return otherId
    else:
        rep,id = None,otherId
        if otherId.startswith("\n"):
            id = otherId[-2:]
        for a in others:
            if a.id == id or a.name.lower() == id.lower():
                rep = a
    
    return rep

def findInvoc(name) -> invoc:
    for a in invocTabl:
        if a.name == name:
            return a

    return None

def findAllie(name) -> tmpAllie:
    for a in tablAllAllies+tablVarAllies:
        if a.name == name:
            return a
    return None

def findEnnemi(name) -> octarien:
    for a in tablAllOcta+tablBoss:
        if a.name == name:
            return a
    return None

listAllBuyableShop = []
for a in weapons+skills+stuffs:
    if a.price > 0:
        listAllBuyableShop.append(a)

def userShopPurcent(user : char):
    totalShop = len(listAllBuyableShop)
    tablToSee = listAllBuyableShop[:]
    for a in listAllBuyableShop:
        if user.have(a):
            tablToSee.remove(a)

    return 100-(len(tablToSee)/totalShop*100)

print("\nVérification des identifiants...")
allReadySeen = []
for obj in stuffs+weapons+skills+others:
    if obj.id not in allReadySeen:
        allReadySeen.append(obj.id)
    else:
        what = ""
        for whaty in stuffs+weapons+skills+others:
            if whaty.id == obj.id:
                what += whaty.name + ", "
        print("Identifiant doublon : {1}".format(obj.name,what))
print("\nVérification des identifiants terminée")