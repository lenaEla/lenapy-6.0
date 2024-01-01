from advObjects.npcSkills.npcSkillsImports import *
import ephem

# Boss spells -------------------
# Spamton
spamWeap = copy.deepcopy(bigshot)
spamWeap.power, spamWeap.accuracy = 150, 100
spamSkill1 = skill("A Call For You","spamtomSkill1",TYPE_DAMAGE,0,200,area=AREA_CONE_3,accuracy=100,emoji='<:call:892757436203671572>',cooldown=3,message="HOT {0} IN YOUR AREA HAVE A [[Message](https://fr.wikipedia.org/wiki/Message)] FOR [{2}] :")
spamSkill2 = skill("BIG SHOT","spamtomSkill2",TYPE_DAMAGE,0,150,area=AREA_LINE_5,accuracy=150,ultimate=True,cooldown=5,message="[[Press F1](https://forums.commentcamarche.net/forum/affich-19023080-press-f1-to-continue-del-to-enter-setup)] FOR HELP :",emoji='<:bigshot:892757453442277417>')
spamSkill3 = skill("Pipis","spamSkill3",TYPE_SUMMON,invocation="Pipis",nbSummon=3,cooldown=5,say="I'VE ALWAYS BEEN A MAN OF THE [[PIPIS](https://bit.ly/3MErtTo)]. A REAL [[PIPIS](https://bit.ly/3MErtTo)] PERSON!")
spamSkill4Eff = effect("Spam Mail","spamtonSkill4Eff", stat=STRENGTH,power=50,area=AREA_CIRCLE_1,trigger=TRIGGER_ON_REMOVE,type=TYPE_INDIRECT_DAMAGE,emoji='<:spamMail:1045810340409135244>')
spamSkill4 = skill("Spam Mail","spamSkill4",TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_3,range=AREA_CIRCLE_4,cooldown=5,effects=spamSkill4Eff,emoji='<:spamMail:1045810340409135244>')
spamSkill5_1 = skill("Détonnation","spamSkill5",TYPE_DAMAGE,power=300,range=AREA_MONO,area=AREA_CIRCLE_4,cooldown=7,ultimate=True)
spamSkill5_cast = effect("Cast - {replicaName}","spamSkill5_1_cast",turnInit=2,replique=spamSkill5_1,silent=True)
spamSkill5_eff = copy.deepcopy(defenseUp)
spamSkill5_eff.power = 20
spamSKill5 = copy.deepcopy(spamSkill5_1)
spamSKill5.power, spamSKill5.effectOnSelf, spamSKill5.effectAroundCaster = 0, spamSkill5_cast, [TYPE_BOOST,AREA_MONO,spamSkill5_eff]

# Serena
serenaSpe = skill("Libération II","SerenaLibe",TYPE_INDIRECT_DAMAGE,0,100,AREA_MONO,ultimate=True,cooldown=7,emoji='<:liberation:1124759822143860808>',area=AREA_ALL_ENEMIES,description="Séréna fait imploser toutes les poudres de fées d'Estialba, infligeant des dégâts en fonction du nombre d'effets \"Poison d'Estialba\" et de leurs durées restantes")
serenaSkill = skill("Propagation","SeranaPropa",TYPE_INDIRECT_DAMAGE,0,0,AREA_MONO,area=AREA_ALL_ENEMIES,cooldown=5,effects=estial,emoji="<:propa2:993801072630046811>",effPowerPurcent=100)
serenaFocal, serenaCloud = copy.deepcopy(focal), copy.deepcopy(poisonus)
serenaFocal.effectOnSelf, serenaFocal.area, serenaFocal.cooldown, serenaCloud.area = None, AREA_CIRCLE_2, serenaFocal.cooldown +2, AREA_CIRCLE_2
serenaSkill2 = skill("Purgation","serenaSkill2",TYPE_INDIRECT_DAMAGE,0,range=AREA_MONO,area=AREA_CIRCLE_3,effects=estial,use=MAGIE,effPowerPurcent=150,emoji='<:purgation:921702426690600960>',cooldown=5)
serenaSkill3 = skill("Dispersion","serenaSkill3",TYPE_INDIRECT_DAMAGE,area=AREA_INLINE_3,range=AREA_MONO,effects=estial,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_DONUT_2,estial.id],effPowerPurcent=80,cooldown=5)
serenaSkill4 = skill("Charge des tempettes","serenaSkill4",TYPE_DAMAGE,tpCac=True,use=MAGIE,effects=estial,effPowerPurcent=50,area=AREA_LINE_2,range=AREA_INLINE_5,replay=True,cooldown=3,power=35)

# Jevil
jevilPassifEffect = effect("I can do anything !","jevilPassiveEffect",silent=True,turnInit=-1,description="Rien n'est plus amusant que le chaos !\n\nLorsque Jevil est dans le combat, tous les combattants recoivent l'effet \"__Confusion__\" qui occulte l'icones des effets dans la liste de ces derniers jusqu'à la fin du combat\n\nÀ chaque début de tour, Jevil donne l'effet \"__Boîte à malice__\" à un certain nombre de cible. Cet effet inflige des dégâts indirect avec une puissance et une zone d'effet aléatoire au début du tour du porteur\nLe nombre d'effets donnés et de cible augmente au fur et à mesure que les PVs de Jevil descendent")
jevilWeap = weapon("Projectiles","jevilWeap",RANGE_DIST,AREA_CIRCLE_4,80,50,ignoreAutoVerif=True,area=AREA_CONE_2,say="CHAOS, CHAOS, CATCH ME IF YOU CAN!",emoji='<:chaos:892857755143127090>',damageOnArmor=1.5,effects=jevilPassifEffect)
jevilSkill1_1 = skill("Pics","jevilSkill1",TYPE_DAMAGE,0,90,area=AREA_LINE_2,accuracy=60,emoji='<a:card:892855854712385637>',say="I CAN DO ANYTHING !",cooldown=1,damageOnArmor=1.5)
jevilSkill1_2 = skill("Trèfles","jevilSkill1",TYPE_DAMAGE,0,100,area=AREA_CONE_2,accuracy=70,emoji='<a:card:892855854712385637>',say="I CAN DO ANYTHING !",cooldown=1,damageOnArmor=0.8)
jevilSkill1_3 = skill("Coeurs","jevilSkill1",TYPE_DAMAGE,0,50,setAoEDamage=True,area=AREA_DIST_4,range=AREA_MONO,accuracy=60,emoji='<a:card:892855854712385637>',say="I CAN DO ANYTHING !",cooldown=2,)
jevilSkill1_4 = skill("Carreau","jevilSkill1",TYPE_DAMAGE,0,80,area=AREA_DIST_3,range=AREA_CIRCLE_2,accuracy=100,emoji='<a:card:892855854712385637>',say="I CAN DO ANYTHING !",cooldown=2,damageOnArmor=3)
jevilSkill1 = skill("Joker !","jevilSkill1",TYPE_DAMAGE,0,become=[jevilSkill1_1,jevilSkill1_2,jevilSkill1_3,jevilSkill1_4],emoji='<a:card:892855854712385637>')

jevilSkill2 = skill("Final Chaos","jevilSkill2",TYPE_DAMAGE,0,75,AREA_MONO,setAoEDamage=True,area=AREA_ALL_ENEMIES,percing=100,say="KIDDING ! HERE'S MY FINAL CHAOS !",initCooldown=5,cooldown=4,emoji="<:devilknife:892855875600023592>",damageOnArmor=2)
jevilEff = effect("Confusion","giveup",silent=True,emoji=uniqueEmoji('<a:giveup:902383022354079814>'),turnInit=-1,unclearable=True,description="Confuse confusing confusion",effPrio=10)

# Luna (Oh it's will be funny)
lunaWeap = weapon("Épee de l'ombre éternelle","aaa",RANGE_LONG,AREA_CIRCLE_1,35,40,strength=20,agility=10,precision=10,repetition=3,emoji='<:lunaWeap:915358834543968348>',damageOnArmor=1.2,ignoreAutoVerif=True,priority=WEAPON_PRIORITY_LOWEST)
lunaInfiniteDarknessStun = effect("Lumière Éternelle","ilianaInfiniteLigthEff",None,type=TYPE_MALUS,stun=True,silent=True,emoji=uniqueEmoji("<:iliEff:929705167853604895>"))
lunaVulne = effect("Vulnérabilité ombrale","lunaVulné", stat=STRENGTH,resistance=-3,turnInit=-1,emoji=vulneEmoji,type=TYPE_MALUS,stackable=True)
lunaSpe = skill("Ténèbres Éternels","InfDarkLaunch",TYPE_DAMAGE,0,250,range=AREA_CIRCLE_7,area=AREA_CIRCLE_7,emoji='<:lunaSecDamage:929705185016692786>',say=["Laissez moi vous montrer un avant goût des Ténèbres Éternels !","Arrête de toujours d'interposer comme ça !","Même toi ne peut pas contrer mes Ténèbres éternellement !","Raah cette lueur ! Cette insuportable lueur !"],description="Inflige des dégâts extrèmes après un tour de chargement",cooldown=99,initCooldown=5,ultimate=True,damageOnArmor=1.2)
lunaInfiniteDarknessShield = effect("Ténèbres Éternels","lunaInfiniteDarknessShield", stat=PURCENTAGE,dodge=-100,overhealth=25,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,replique=lunaSpe,turnInit=99,absolutShield=True,emoji=uniqueEmoji('<:bigDark:916561798948347935>'))
lunaSpeCast = skill("Ténèbres Éternels","lunaInfDarkCast",TYPE_DAMAGE,0,0,emoji='<:lunaSecDamage:929705185016692786>',range=AREA_CIRCLE_7,area=AREA_CIRCLE_7,effectOnSelf=lunaInfiniteDarknessShield,say="Ok ça suffit ! Voyons voir comment vous tiendrez face à ça...",message="Luna concentre les Ténèbres environants...",cooldown=lunaSpe.cooldown,initCooldown=lunaSpe.initCooldown,ultimate=lunaSpe.ultimate)
lunaSkill = copy.deepcopy(soupledown)
lunaSkill.power, lunaSkill.onArmor, lunaSkill.cooldown = 250, 1.3, 5
lunaSkill5_4eff = effect("Onde de Choc","lunaSkill4_1eff", stat=STRENGTH,power=35,area=AREA_DONUT_1,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,emoji='<:darkShockWave:1185653578824679484>')
lunaSkill2 = skill("Frappes des Ténèbres","lunaSkill2",TYPE_DAMAGE,0,135,AREA_CIRCLE_2,effects=lunaSkill5_4eff,repetition=3,cooldown=5,initCooldown=2,damageOnArmor=1.3,percing=35,emoji='<:lunaTb:932444874073063434>',say=["Je pense pas que tu va pouvoir prendre celui-ci sans broncher.","Tu as des healers non ? Donnons leur un peu de boulot !"],description="Inflige de lourd dégâts à une cible unique")
lunaSkill4Eff = copy.deepcopy(innerdarknessEff)
lunaSkill4Eff.stat,lunaSkill4Eff.power , lunaSkill4Eff.id, lunaSkill4Eff.emoji, lunaSkill4Eff.area = STRENGTH, 35, "lunaSkill4Eff", uniqueEmoji('<:lunaIndi:932447879786823730>'), AREA_MONO
lunaSkill4_1 = skill("Convertion rapprochée",'lunaSkill4',TYPE_INDIRECT_DAMAGE,0,range=AREA_MONO,area=AREA_CIRCLE_2,effects=lunaSkill4Eff,effPowerPurcent=200,cooldown=7,emoji=lunaSkill4Eff.emoji[0][0],say=['Vous tenez tant à voir les Ténèbres de plus près ? Voilà pour vous !','Votre Lumière ne vous protègera pas éternellement.'],description="Donne un effet de dégâts indirect monocible aux ennemis proches",effectAroundCaster=[TYPE_DAMAGE,AREA_CIRCLE_2,lunaSkill4Eff.power*2],setAoEDamage=True)
lunaSkill4_2 = skill("Convertion externe",'lunaSkill4',TYPE_INDIRECT_DAMAGE,0,range=AREA_MONO,area=AREA_DIST_7,effects=lunaSkill4Eff,cooldown=7,emoji=lunaSkill4Eff.emoji[0][0],say=["C'est pas parceque vous restez loin que vous serez épargné !","Votre Lumière sucombera à mes Ténèbres."],description="Inflige un effet de dégâts indirect en zone aux ennemis éloignés",effPowerPurcent=int(20/lunaSkill4Eff.power*100),effectAroundCaster=[TYPE_DAMAGE,AREA_DIST_7,20],setAoEDamage=True)
lunaSkill4 = skill("Convertion","lunaSkill4",TYPE_INDIRECT_DAMAGE,0,range=AREA_CIRCLE_7,use=STRENGTH,say="Votre Lumière ne vous protègera pas éternellement !",emoji=lunaSkill4Eff.emoji[0][0],become=[lunaSkill4_1,lunaSkill4_2])

lunaSkill5_1e = copy.deepcopy(armorGetMalus)
lunaSkill5_1e.power, lunaSkill5_1e.turnInit = 50, 3
lunaSkill5_1 = skill("Reverse roundhouse-kick","lunaSkill5",TYPE_DAMAGE,0,120,AREA_CIRCLE_1,garCrit=True,effects=lunaSkill5_1e,area=AREA_ARC_1,percing=20,emoji='<:talonFracassant:1088958995030605834>',damageOnArmor=2,description='Inflige des dégâts en zone à un ennemi au corps à corps')
lunaSkill5_2e = effect("Résistance réduites","lunaSkill52e", stat=PURCENTAGE,resistance=-50,turnInit=3)
lunaSkill5_2 = skill("Side-kick fouetté","lunaSkill5",TYPE_DAMAGE,0,200,AREA_CIRCLE_1,effects=lunaSkill5_2e,garCrit=True,emoji='<:highKick:1122785057531236463>',percing=20,say="Hmf !",damageOnArmor=3,description='Inflige des dégâts à une cible unique au corps à corps\nDégâts triplé sur de l\'armure')
lunaSkill5_31 = skill("Backflip","lunaSkill5",TYPE_DAMAGE,power=135,garCrit=True,range=AREA_CIRCLE_1,knockback=1,emoji='<:inercie:1058338643707695155>',percing=20)
lunaSkill5_31_e = effect("Enchainement - {replicaName}","lunaSkill5_31",replique=lunaSkill5_31,silent=True)
lunaSkill5_3 = skill("Sweeping","lunaSkill5",TYPE_DAMAGE,0,100,AREA_CIRCLE_1,area=AREA_CIRCLE_1,areaOnSelf=True,emoji='<:baleyette:977166497422139392>',percing=20,replay=True,effectOnSelf=lunaSkill5_31_e,say="C'est que tu es colant toi !",description='Inflige des dégâts, étourdit pendant un tour et repousse un ennemi au corps à corps')
lunaSkill5_41 = skill("Side Kick","lunaSkill4_1",TYPE_DAMAGE,power=120,garCrit=True,range=AREA_CIRCLE_1,emoji='<:talonFracassant:1088958995030605834>',percing=20,effects=lunaSkill5_4eff)
lunaSkill5_41_e = effect("Enchainement - {replicaName}","lunaSkill5_41",replique=lunaSkill5_41,silent=True)
lunaSkill5_4 = skill("Double High roundhouse-kick","lunaSkill5",TYPE_DAMAGE,0,100,AREA_CIRCLE_1,repetition=2,effectOnSelf=lunaSkill5_41_e,percing=20,replay=True,emoji='<:chainChoc1:1058339074563379240>',say="Hé vous derrière ! Cadeau !",damageOnArmor=2,description='Inflige des dégats et repousse de 3 cases un ennemi au corps à corps')
lunaSkill5Base = skill("Corps à corps","lunaSkill5",TYPE_DAMAGE,0,0,AREA_CIRCLE_1,emoji='<:luna4inOne:919260128698589184>',become=[lunaSkill5_1,lunaSkill5_2,lunaSkill5_3,lunaSkill5_4])

lunaSkill6 = skill("Vitesse ombrale","lunaSkill6",TYPE_DAMAGE,0,50,AREA_INLINE_4,emoji='<:lunaDash:932286143884566528>',cooldown=3,replay=True,tpCac=True,accuracy=200,description='Se téléporte au corps à corps d\'un ennemi et vous permet de rejouer votre tour')
lunaSkill7eff = copy.deepcopy(lunaSkill5_4eff)
lunaSkill7eff.power = 65
lunaSkill7 = skill("Genoux DarkExplo","lunaSkill7",TYPE_DAMAGE,power=175,percing=25,damageOnArmor=1.5,effects=lunaSkill7eff,cooldown=3,range=AREA_INLINE_4,tpCac=True,emoji='<:darkRenf:1120974892188315740>')

# Clemence Pos Special skills
clemBloodJauge = effect("Jauge de sang","clemBloodJauge",turnInit=-1,unclearable=True,emoji=uniqueEmoji('<:vampire:900312789686571018>'),lvl=100,description="Clémence possédée tourne autour de sa Jauge de Sang\n\nElle débute le combat avec une jauge à **100** Points de sang, son maximum.\nChacunes de ses compétences ont un coût en Points de Sang, qui sont retiré à la jauge à la fin de leur utilisation\n\nSi la jauge de sang tombe à **0 point**, Clémence est étourdie pendant 2 tours durant lesquels sa résistance est diminuée\nLa jauge de sang récupère **1 point** de sang à chaque fois que Clémence inflige 50 points de dégâts, et **100 points** une fois que Clémence n'est plus étourdie\n\nLa quantité de points de sang dans la jauge de sang est constamant visible\nClémence possède 10% de vol de vie",jaugeValue=jaugeValue(
    emoji=[["<:BJLeftEmpty:900473865459875911>","<:BJMidEmpty:900473889539366994>","<:BJRightEmpty:900473909856587847>"],["<:BJLeftFull:900473987564441651>","<:BJMidFull:900474021781569604>","<:BJRightFull:900474036042215515>"]],
    conds=[
        jaugeConds(INC_START_FIGHT,100),
        jaugeConds(INC_ENEMY_DAMAGED,20/100)]
    ))

dateNow = datetime.now(parisTimeZone)
def get_phase_on_day(time:datetime):
  """Returns a floating-point number from 0-1. where 0=new, 0.5=full, 1=new"""
  #Ephem stores its date numbers as floating points, which the following uses
  #to conveniently extract the percent time between one new moon and the next
  #This corresponds (somewhat roughly) to the phase of the moon.

  #Use Year, Month, Day as arguments
  date = ephem.Date(time)

  nnm = ephem.next_new_moon(date)
  pnm = ephem.previous_new_moon(date)

  lunation = (date-pnm)/(nnm-pnm)

  #Note that there is a ephem.Moon().phase() command, but this returns the
  #percentage of the moon which is illuminated. This is not really what we want.

  return lunation
clemMoonPhase = get_phase_on_day(datetime.now(parisTimeZone))/0.5
if clemMoonPhase > 1:
  clemMoonPhase = 1-(clemMoonPhase-1)

clemPosBloodJauge = effect("Jauge Sanguine","clemPosBloodJauge",turnInit=-1,unclearable=True,emoji='<:bloodJauge:1050111058314018936>',jaugeValue=jaugeValue(
    emoji=bloodJauge.jaugeValue.emoji,
    conds=[
      jaugeConds(INC_START_FIGHT,round(10+(90*clemMoonPhase),2)),
      jaugeConds(INC_LIFE_STEAL,200/100),
      jaugeConds(INC_DEAL_DAMAGE,20/100)]
))

clemExBloodPassive = copy.deepcopy(bloodButterFlyPassifEff)
clemExBloodPassive.power = 100

clemPosWeapBleeding = effect("Hémorragie","clemPosBleeding", stat=MAGIE,power=50,lifeSteal=50,emoji="<:sanguisExaltium:1115283194950996089>",trigger=TRIGGER_START_OF_TURN,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,stackable=True,description="Un effet de dégâts sur la durée qui soigne Clémence d'une partie des dégâts infligés")
clemWeapon = weapon("Rapière en argent lunaire","clemenceWeapon",RANGE_DIST,AREA_CIRCLE_2,85,100,ignoreAutoVerif=True,use=MAGIE,effectOnUse=clemPosWeapBleeding,effects=clemExBloodPassive,damageOnArmor=2,magie=50,endurance=20,emoji='<:clemWeap:915358467773063208>')
clemSkill1 = skill("Lune de Sang","clemSkill1",TYPE_DAMAGE,0,power=180,minJaugeValue=20,maxPower=125,maxJaugeValue=50,jaugeEff=clemPosBloodJauge,lifeSteal=50,range=AREA_MONO,area=AREA_CIRCLE_3,emoji='<a:clemSkill1:901147227588812890>',cooldown=2,initCooldown=2,use=MAGIE,damageOnArmor=2,say="Si vous tenez tant que ça à me coller aux basques c'est pour que je vous bute plus vite c'est ça ?",effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_2,bloodButterfly])
clemSkill2 = skill("Chiroptera perniciosius","clemSkill2",TYPE_DAMAGE,0,225,AREA_CIRCLE_2,maxPower=350,maxJaugeValue=50,cooldown=4,lifeSteal=100,minJaugeValue=35,effects=bloodButterfly,jaugeEff=clemPosBloodJauge,emoji='<a:clemSkill4:901150027706142780>',use=MAGIE,say=["Tu tombe bien toi, j'avais besoin d'un mannequin.","Il est temps que quelqu'un te remette à ta place.","Tu penses vraiment que tu seras capable de tout prendre sans brocher ?"],damageOnArmor=5,effPowerPurcent=125)
clemSilence = copy.deepcopy(silenceEff)
clemSilence.turnInit = 2
clemUltShield = effect("Bouclier sanguin","clemShield", stat=PURCENTAGE,overhealth=25,emoji="<:clemMemento2:902222663806775428>",turnInit=2,absolutShield=True)
clemSkill3 = skill("Demi-Lune","clemSkill3",TYPE_DAMAGE,0,200,AREA_CIRCLE_3,minJaugeValue=30,lifeSteal=30,jaugeEff=clemPosBloodJauge,area=AREA_ARC_2,cooldown=3,use=MAGIE,emoji='<a:clemSkill3:914759077551308844>',damageOnArmor=3)
clemSkill4 = skill("Chiroptera vastare","clemSkill4",TYPE_DAMAGE,0,100,AREA_MONO,minJaugeValue=40,lifeSteal=30,jaugeEff=clemPosBloodJauge,area=AREA_DIST_7,cooldown=5,use=MAGIE,say=["Vous pensez que vous êtes à l'abri là bas ?","Vous en faites pas, je vous ai pas oublié."],emoji='<a:clemSkill4:914756335860596737>',setAoEDamage=True,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_CIRCLE_2,clemPosWeapBleeding],effPowerPurcent=50,ultimate=True)
clemExSkill5_3 = skill("Redoublement Sanglant","clemExSkill4",TYPE_DAMAGE,accuracy=200,power=125,lifeSteal=50,minJaugeValue=1,maxJaugeValue=25,maxPower=125,emoji='<:combo3:978398179999514624>',range=AREA_CIRCLE_1,use=MAGIE,tpCac=True,effects=clemPosWeapBleeding)
clemExSkill5_3Cast = effect("Redoublement préparé","clemExSkill5_3Cast",silent=True,replique=clemExSkill5_3)
clemExSkill5_2 = skill("Zwerchhau Sanglant","clemExSkill4",TYPE_DAMAGE,accuracy=200,power=100,lifeSteal=50,effPowerPurcent=75,minJaugeValue=1,maxJaugeValue=25,maxPower=115,effectOnSelf=clemExSkill5_3Cast,emoji='<:combo2:978398160454045738>',range=AREA_CIRCLE_1,replay=True,use=MAGIE,tpCac=True,effects=clemPosWeapBleeding)
clemExSkill5_2Cast = effect("Zwerchhau préparé","clemExSkill5_2Cast",silent=True,replique=clemExSkill5_2)
clemSkill5 = skill("Riposte Sanglante","clemExSkill4",TYPE_DAMAGE,accuracy=200,power=80,minJaugeValue=15,maxJaugeValue=25,effPowerPurcent=50,maxPower=100,lifeSteal=50,jaugeEff=clemPosBloodJauge,effectOnSelf=clemExSkill5_2Cast,emoji='<:combo1:978398142967992330>',range=AREA_CIRCLE_1,replay=True,use=MAGIE,tpCac=True,effects=clemPosWeapBleeding)
clemSkill6 = skill("Lance de sang",'clemSkill6',TYPE_DAMAGE,0,150,AREA_DIST_5,minJaugeValue=30,jaugeEff=clemPosBloodJauge,lifeSteal=15,area=AREA_CIRCLE_1,use=MAGIE,cooldown=4,emoji='<:bloodlance:1118613536139124776>',effects=bloodButterfly,effPowerPurcent=150)
clemSkill7 = skill("Prise de Sang","clemPosSkill7",TYPE_DAMAGE,power=50,maxPower=85,maxJaugeValue=40,area=AREA_ALL_ENEMIES,lifeSteal=20,setAoEDamage=True,cooldown=5,use=MAGIE,minJaugeValue=25,jaugeEff=clemPosBloodJauge,effectAroundCaster=[TYPE_MALUS,AREA_ALL_ENEMIES,bloodButterfly],description="Inflige des dégâts à tous les ennemis ainsi que l'effet {0} __{1}__. De plus, absorbe le sang des ennemis, augmentant divers caractérisiques en fonction de leurs aspirations".format(bloodButterfly.emoji[0][0],bloodButterfly.name),emoji='<:clemExSkill:1015209760062189628>')

importantSkills.append(clemSkill7)

# The Giant Ennemi Spider
TGESWeap = weapon("noneWeap","TheGiantEnemySpiderWeapon",RANGE_DIST,AREA_CIRCLE_1,0,0,0,resistance=50)
TGESSkill1 = skill("Projectile","TheGiantEnemySpiderSkill1",TYPE_DAMAGE,0,int(GESLskill.power*1.5))

# Matt from WiiSport
mattWeapon = weapon("Direct !","mattWeapon",RANGE_DIST,AREA_CIRCLE_1,60,70,repetition=3,emoji='<:boxe:922064460326244384>',ignoreAutoVerif=True)
mattSkill1 = skill("Home Run !","mattSkill1",TYPE_DAMAGE,0,150,AREA_CIRCLE_1,cooldown=4,knockback=5,description="Quel magnifique coup de batte !",emoji='<:homerun:922064424708239360>')
mattSkill2 = skill("Tir à trois points","mattSkill2",TYPE_DAMAGE,0,80,AREA_DIST_5,cooldown=3,description="Quel tir ! Qui aurait cru qu'il ferait un panier d'ici ?",emoji='<:basket:922064483688513567>')
mattSkill3 = skill("Strike !","mattSkill3",TYPE_DAMAGE,0,135,AREA_CIRCLE_1,area=AREA_LINE_6,cooldown=3,description="Non vous pouvez pas appuyer sur A pour passer la cinématique",emoji='<:bowling:922064440201969724>')
mattSkill4Eff = effect("Gardé","matt(en)Garde", stat=STRENGTH,power=25,lvl=99,onDeclancher=True,immunity=True,description="Une vision accru vous permet de contrer les dégâts et de contre attaquer !")
mattSkill4 = skill("Garde","mattSkill4",TYPE_DAMAGE,0,cooldown=5,range=AREA_CIRCLE_1,power=100,effectOnSelf=mattSkill4Eff,description="Inflige des dégâts à l'ennemi ciblé et vous immunise contre tous dégâts jusqu'à votre prochain tour. Si vous êtes attaqué pendant cette durée, inflige des dégâts indirects à l'attaquant")

kikuPassivSkillEff = effect("Cimetière","kikuGraveyardEff1",type=TYPE_SUMMON,callOnTrigger=lightSkeleton,trigger=TRIGGER_START_OF_TURN,turnInit=-1,unclearable=True,lvl=1,emoji='<:graveyard:1164906144339341424>',description="Kiku invoque deux squelettes autour d'elle à chaque fois qu'elle commence son tour",area=AREA_CIRCLE_1,denieWeap = True,dodge=-100)
kikuWeap = weapon("Tir d'énergie","kikuWeap",RANGE_LONG,AREA_CIRCLE_5,power=100,accuracy=150,endurance=15,magie=15,priority=WEAPON_PRIORITY_LOWEST,effects=kikuPassivSkillEff,ignoreAutoVerif=True,use=MAGIE,emoji='<:energyWeap:1164909709950730270>')
kikuSkill1Eff1 = effect("Mors Vita Est","kikuSkill1Eff",type=TYPE_SUMMON,callOnTrigger=skeletonBow,lvl=2,area=AREA_CIRCLE_3,trigger=TRIGGER_INSTANT,emoji=kikuRes.emoji)
kikuSkill1Eff2 = effect("Mors Vita Est","kikuSkill2Eff",type=TYPE_SUMMON,callOnTrigger=lightZombi,lvl=2,area=AREA_CIRCLE_4,trigger=TRIGGER_INSTANT,emoji=kikuRes.emoji)
kikuSkill1 = skill("Mors Vita Est",'kikuSkill1',TYPE_SUMMON,cooldown=7,use=MAGIE,invocation=skeletonMage,effectOnSelf=kikuSkill1Eff1,emoji=kikuSkill1Eff1.emoji[0][0],range=AREA_CIRCLE_2,effectAroundCaster=[TYPE_SUMMON,AREA_MONO,kikuSkill1Eff2],description="Kiku invoque un mage mort-vivant à ses côtés, pouvant infliger des dégâts de zone et réduire les soins des ennemis, deux squelettes archers pouvant repousser les adversaires et infliger de bon dégâts critiques aux armures ainsi que deux zombies légers, pouvant absorber un bon nombre de dégâts et booster leurs alliés")
kikuSkill2 = skill("Dénis",'kikuSkill2',TYPE_DAMAGE,cooldown=3,power=120,setAoEDamage=True,range=AREA_MONO,use=MAGIE,area=AREA_CIRCLE_2,description="Kiku inflige des dégâts aux ennemis proches et les repousses",knockback=3,emoji='<:kikuUltraVoca:1044270141338308648>')
kikuSkill3Eff = copy.deepcopy(dmgUp)
kikuSkill3Eff.power, kikuSkill3Eff.turnInit = 35, 3
kikuSkill3 = skill("Terre Nécrosée","kikuSkill3",TYPE_DAMAGE,cooldown=3,power=135,range=AREA_MONO,area=AREA_CIRCLE_3,emoji='<:kikuHellCircle:1044269043911249921>',use=MAGIE,effectAroundCaster=[TYPE_BOOST,AREA_SUMMONS,kikuSkill3Eff],description="Kiku inflige des dégâts aux ennemis autour d'elle et augmente les dégâts infligés par ses invocations durant un petit moment")
kikuSkill4Eff1 = effect("Putréfaction","kikuSkill4Eff1", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,turnInit=5,power=50,trigger=TRIGGER_END_OF_TURN,emoji=decompositionEff.emoji[0][0])
kikuSkill4Eff12 = copy.deepcopy(kikuSkill4Eff1)
kikuSkill4Eff12.power, kikuSkill4Eff12.stackable = kikuSkill4Eff12.power // 2, True
kikuSkill4Eff2 = effect("Explosion Nécromantique","kikuSkill4Eff2",type=TYPE_MALUS,callOnTrigger=kikuSkill4Eff12,area=AREA_DONUT_3,emoji=putrefaction.emoji,trigger=TRIGGER_DEATH)
kikuSkill4Eff3, kikuSkill4Eff4 = copy.deepcopy(aconstEff), copy.deepcopy(incurable)
kikuSkill4Eff3.power, kikuSkill4Eff3.turnInit, kikuSkill4Eff4.power, kikuSkill4Eff4.turnInit = 25, kikuSkill4Eff1.turnInit, 25, kikuSkill4Eff1.turnInit
kikuSkill4 = skill("Toucher Nécrosant","kikuSkill4",TYPE_INDIRECT_DAMAGE,effects=[kikuSkill4Eff1,kikuSkill4Eff2,kikuSkill4Eff3,kikuSkill4Eff4],initCooldown=3,cooldown=kikuSkill4Eff1.turnInit,emoji="<:kikuTb:1044348246039994470>",description="Kiku inflige un fort effet de dégâts à l'ennemi ciblé en réduisant également temporairement ses PV maximums et les soins qu'il reçoit. Si la cible meurt, les ennemis autours subissent un effet de dégâts indirects similaire avec une puissance amoindri")
kikuSkill5_1Eff = effect("Explosion des Morts","explosiondesesmorts", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_ON_REMOVE,area=AREA_CIRCLE_2,power=70,emoji='<:deathBlade3:1164997666837635113>')
kikuSkill5_1Eff2 = effect("Résistance réduite","kikuSkill5_1Eff2",resistance=-50,type=TYPE_MALUS,stat=PURCENTAGE)
kikuSkill5_1 = skill("Epée des Morts","kikuSkill5_1",TYPE_DAMAGE,power=175,damageOnArmor=1.25,emoji='<:deathBlade2:1164997642296766475>',cooldown=7,ultimate=True,effects=[kikuSkill5_1Eff,kikuSkill5_1Eff2],description="Après un tour de chargement, Kiku inflige de gros dégâts à l'ennemi ciblé et réduit drastiquement sa résistance. Après un autre tour, la cible et les ennemis alentours subissent une nouvelle attaque indirecte")
kikuSkill5c = effect("Cast - {replicaName}","kikuSkill5c",silent=True,replique=kikuSkill5_1,turnInit=2,emoji='<:deathBlade1:1164997616384364624>')
kikuSkill5 = copy.deepcopy(kikuSkill5_1)
kikuSkill5.power, kikuSkill5.id, kikuSkill5.emoji, kikuSkill5.effects, kikuSkill5.effectOnSelf = 0, "kikuSkill5", kikuSkill5c.emoji[0][0], [None], kikuSkill5c
kikuSkill6Eff1, kikuSkill6Eff2 = copy.deepcopy(vulne), effect("Brûme Funèbre","fog", stat=PURCENTAGE,strength=20,magie=20,turnInit=3,emoji='<:moramMortis:1084865158884630528>')
kikuSkill6Eff1.power, kikuSkill6Eff1.turnInit = 20, kikuSkill6Eff2.turnInit
kikuSkill6 = skill("Brûme Funèbre","kikuSkill6",TYPE_MALUS,effects=[kikuSkill6Eff1],effectAroundCaster=[TYPE_BOOST,AREA_SUMMONS,kikuSkill6Eff2],range=AREA_MONO,area=AREA_ALL_ENEMIES,emoji='<:rubyBrasero:1052698751715778631>',cooldown=5,description="Augmente les dégâts subis par les ennemis et accroi les statistiques offensives de vos invocations")

# Akira H.
akikiWeap = weapon("Faux Haineuse","akikiWeap",range=RANGE_MELEE,effectiveRange=AREA_CIRCLE_1,power=150,accuracy=70,strength=25,endurance=25,emoji=fauc.emoji,area=AREA_ARC_1,priority=WEAPON_PRIORITY_LOWEST)
akikiSkill3 = skill("Massacre","akikiSkill3",TYPE_DAMAGE,0,power=65,range=AREA_MONO,area=AREA_CIRCLE_2,accuracy=80,cooldown=7)
akikiSkill4 = skill("Intolérance","akikiSkill4",TYPE_DAMAGE,0,power=120,range=AREA_CIRCLE_3,area=AREA_LINE_2,cooldown=7)
akikiSkill1Eff = effect("Rage Croissante","akikiRageDmgBuff",turnInit=-1,unclearable=True,emoji=dmgUp.emoji,power=50)
akikiSkill1 = skill("Rage Croissante","akikiSkill1",TYPE_PASSIVE,effectOnSelf=akikiSkill1Eff,emoji=akikiSkill1Eff.emoji[0][0],description="Accroie les dégâts directs infligés par Akira au fur et à mesure que ses PVs diminuent, jusqu'à **+{0}%** avec 0.1% de PV restants".format(akikiSkill1Eff.power))
akikiSkill2_1_2 = skill("Destruction Explosive","akikiSkill2_1",TYPE_DAMAGE,emoji='<:akiTankStack:1007050856748818464>',power=600,range=AREA_CIRCLE_4,tpCac=True,cooldown=5,area=AREA_CIRCLE_1,description="Au premier tour, Akira marque un ennemi puis il inflige au second tour d'énormes dégâts à l'ennemi marqué et ceux alentours. La puissance est divisée par le nombre d'ennemi ayant une aspiration de mêlée dans la zone d'effet")
akikiSkill2_mark = effect("Cible : Destruction Explosive","akikiSkill2_mark",type=TYPE_MALUS,emoji='<:akiTankStack:1007050856748818464>')
akikiSkill2_1_cast = effect("Cast - {replicaName}","akikiSkill2_1_cast",silent=True,turnInit=2,replique=akikiSkill2_1_2,emoji='<:akiTankStack:1007050856748818464>')
akikiSkill2_1_1 = copy.deepcopy(akikiSkill2_1_2)
akikiSkill2_1_1.id, akikiSkill2_1_1.power, akikiSkill2_1_1.tpCac, akikiSkill2_1_1.effectOnSelf, akikiSkill2_1_1.type, akikiSkill2_1_1.effects, akikiSkill2_1_1.area = "akikiSkill2", 0, False, akikiSkill2_1_cast,TYPE_MALUS, [akikiSkill2_mark], AREA_MONO
akikiSkill2_2 = skill("Destruction Concentrique","akikiSkill2",TYPE_DAMAGE,range=AREA_CIRCLE_3,power=250,cooldown=5,area=AREA_CIRCLE_1,emoji='<:akiTB:1007050875451220059>')

akikiSkill3_1_1 = skill("Frappe Enragée","akikiSkill3_1",TYPE_DAMAGE,power=400,cooldown=5,emoji='<:akiStack:1007050822338748466>',area=AREA_CIRCLE_3,range=AREA_DONUT_5,tpCac=True,description="Akira marque un ennemi au premier tour puis inflige de lourds dégâts à l'ennemi marqué et ceux aux alentours.\nLa puissance est divisée par le nombre d'ennemi dans la zone d'effet.")
akikiSkill3_1_cast = effect("Cast - {replicaName}","akikiSkill3_1_cast",silent=True,turnInit=2,replique=akikiSkill3_1_1,emoji='<:akiStack:1007050822338748466>')
akikiSkill3_1_mark = effect("Cible : Frappe Enragée","akikiSkill3_1_mark",type=TYPE_MALUS,emoji='<:akiStack:1007050822338748466>')
akikiSkill3_1_2 = copy.deepcopy(akikiSkill3_1_1)
akikiSkill3_1_2.id, akikiSkill3_1_2.power, akikiSkill3_1_2.tpCac, akikiSkill3_1_2.effectOnSelf, akikiSkill3_1_2.type, akikiSkill3_1_2.area, akikiSkill3_1_2.effects= 'akikiSkill3', 0, False, akikiSkill3_1_cast,TYPE_MALUS, AREA_MONO, [akikiSkill3_1_mark]
akikiSkill3_2_1 = skill("Frappe Haineuse","akikiSkill3_2",TYPE_DAMAGE,power=80,cooldown=5,area=AREA_CIRCLE_1,emoji='<:akiAway:1007050839514435584>',range=AREA_DONUT_5,description="Marque 3 ennemis au premier tour puis inflige au second tour des dégâts à tous les ennemis marquées et ceux autour d'eux. Chaque attaque augmente les dégâts reçus des ennemis affecté, augmentant aussi ceux subis par les ennemis prenant plusieurs fois des dégâts par cette attaque")
akikiSkill3_2_cast = effect("Cast - {replicaName}","akikiSkill3_2_cast",silent=True,turnInit=2,replique=akikiSkill3_2_1,emoji='<:akiAway:1007050839514435584>')
akikiSkill3_2_mark = effect("Cible : Frappe Haineuse","akikiSkill3_2_mark",type=TYPE_MALUS,emoji='<:akiAway:1007050839514435584>')
akikiSkill3_2_2 = copy.deepcopy(akikiSkill3_2_1)
akikiSkill3_2_2.id, akikiSkill3_1_2.power, akikiSkill3_1_2.type, akikiSkill3_1_2.effects, akikiSkill3_1_2.effectOnSelf, akikiSkill3_1_2.area = 'akikiSkill3', 0,TYPE_MALUS, [akikiSkill3_2_mark], akikiSkill3_2_cast, AREA_RANDOMENNEMI_3

akikiEnrage2 = skill("En-Rage","akikiEnrage",TYPE_DAMAGE,0,500,range=AREA_MONO,ultimate=True,area=AREA_ALL_ENEMIES,accuracy=500,description="Cette compétence exécute tous les ennemis encore vivants.\nCette compétence est forcément utilisée lorsque les PVs restants sont inférieurs à **15%** des PVmax",initCooldown=99,cooldown=99)
akikiEnrage2_c = effect("Cast - Rage (1 tour !)","akikiEnrage2_c",turnInit=2,silent=True,replique=akikiEnrage2)
akikiEnrage1 = copy.deepcopy(akikiEnrage2)
akikiEnrage1.power, akikiEnrage1.effectOnSelf = 0, akikiEnrage2_c
akikiEnrage1_c = effect("Cast - Rage (2 tour !)","akikiEnrage1_c",turnInit=2,silent=True,replique=akikiEnrage1)
akikiEnrage = copy.deepcopy(akikiEnrage1)
akikiEnrage.effectOnSelf = akikiEnrage1_c

unformBossWeapon = weapon("Arme aforme","unformBossWeap",RANGE_DIST,AREA_CIRCLE_1,150,80,ignoreAutoVerif=True)
unformBossSkill1 = skill("Distorsion Dimentionelle","unformBossSkill1",TYPE_DAMAGE,power=250,range=AREA_CIRCLE_1,cooldown=7,use=MAGIE)
unformBossSkill2Eff = copy.deepcopy(dmgUp)
unformBossSkill2Eff.power = 50
unformBossSKill2 = skill("Anéantissement accéléré","unformBossSKill2",TYPE_BOOST,range=AREA_MONO,area=AREA_CIRCLE_3,effects=unformBossSkill2Eff,cooldown=5)
unformBossSkill3 = skill("Pulsion spaciale","unformBossSkill3",TYPE_HEAL,power=250,use=MAGIE,range=AREA_MONO,area=AREA_CIRCLE_5,cooldown=5)

unformBoss = octarien("Aformité incarnée",300,250,200,50,50,200,350,25,15,0,unformBossWeapon,15,'<:uShadow:938530004319477821>',[unformBossSkill1,unformBossSKill2,unformBossSkill3],description="Un leader de l'assaut des aformités, qui cherchent à détruire le multivers",deadIcon='<:em:866459463568850954>',team=NPC_UNFORM)

# Iliana Ex.
ILIREGENPOWER = 50
iliExWeapEff = effect("Conviction de la Lumière","iliExPasRegenEff", stat=CHARISMA,turnInit=-1,unclearable=True,block=35,emoji='<:ilianaStans:969819202032664596>',description="Accorde à Iliana Ex. 35% de blocage")
iliExWeapon = weapon("Epée et Bouclier de la Lumière","iliExWeap",RANGE_DIST,AREA_CIRCLE_1,100,100,effects=iliExWeapEff,emoji='<:iliShield:975785889512976434>',ignoreAutoVerif=True,use=CHARISMA,priority=WEAPON_PRIORITY_LOWEST)
iliExSkill1Eff = effect("Corruption Lumineuse","iliExSkill1Eff", stat=CHARISMA,power=30,lvl=3,stackable=True,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,description="Un déséquilibre élémentaire vous provoque des dégâts sur la durée",emoji='<:iliDot:1046387034522136609>')
iliExSkill1 = skill("Flash","iliExSkill1",TYPE_INDIRECT_DAMAGE,cooldown=5,area=AREA_CIRCLE_4,range=AREA_MONO,effects=iliExSkill1Eff,emoji='<:flash:977025336518799420>',effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER])
iliExSkill3 = skill("Vague de Lumière","iliExSkill3",TYPE_DAMAGE,power=80,area=AREA_CONE_3,use=CHARISMA,cooldown=4,range=AREA_CIRCLE_1,effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER])
iliExSkill4_1 = skill("Ardeur Lumineuse","iliExSkill4",TYPE_DAMAGE,power=70,repetition=2,range=AREA_CIRCLE_2,emoji='<:iliBravor:1046381213910302834>',use=CHARISMA,cooldown=5,description="Iliana se téléporte au corps à corps d'un ennemi puis lui inflige des dégâts monocible à deux reprises",effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER],url=lb1Mono.url)
iliExSkill4_c = effect("Cast - {replicaName}","iliExSkill4_c",replique=iliExSkill4_1,silent=True)
iliExSkill4 = skill("Vitesse Lumière","iliExSkill4",TYPE_DAMAGE,tpCac=True,cooldown=iliExSkill4_1.cooldown,replay=True,power=35,use=CHARISMA,description=iliExSkill4_1.description,emoji='<:iliLightSpeed:1046384202792308797>',effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER//3],effectOnSelf=iliExSkill4_c)
iliExSKill5_1 = skill("Lumière Eternelle","iliExLb",TYPE_DAMAGE,cooldown=6,power=100,use=CHARISMA,setAoEDamage=True,ultimate=True,range=AREA_MONO,area=AREA_ALL_ENEMIES,emoji="<:eternalLight:1116761926052089856>",description="Après un tour de chargement, Iliana inflige des dégâts à tous ses ennemis",effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER*1.5])
iliExSkill5_c = effect("","iliExLbc",turnInit=2,silent=True,replique=iliExSKill5_1)
iliExSKill5 = skill("Lumière Eternelle","iliExLb",TYPE_DAMAGE,cooldown=iliExSKill5_1.cooldown+1,use=CHARISMA,effectOnSelf=iliExSkill5_c,range=AREA_MONO,area=AREA_ALL_ENEMIES,emoji=iliExSKill5_1.emoji,ultimate=True,description=iliExSKill5_1.description)
iliExSkill6Eff1 = effect("Etourdissement","iliExSkill6EffStun",type=TYPE_MALUS,emoji="<:stun:882597448898474024>",stun=True)
iliExSkill6Eff2 = effect("Bouclier Dressé","iliExSkill6EffBck",block=15,emoji='<:shieltron:971787905758560267>')
iliExSkill6_1 = skill("Fragmentation","iliExSkill6",TYPE_DAMAGE,use=CHARISMA,power=75,repetition=3,percing=25,emoji='<:fragmentation:1117375884446412872>',ultimate=True,range=AREA_INLINE_3,effectOnSelf=iliExSkill6Eff2,description="Iliana bash violament un ennemi puis, après un tour de chargement, lui assigne plusieurs coups d'épée\nLe choc initial étoudit la cible tout en augmentant le taux de blocage d'Iliana",cooldown=5,effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER//2*3])
iliExSkill6_c = effect("Cast - {replicaName}","iliExSkill6_c",turnInit=2,replique=iliExSkill6_1)
iliExSkill6 = skill(iliExSkill6_1.name,iliExSkill6_1.id,TYPE_DAMAGE,power=50,range=AREA_INLINE_4,effectOnSelf=iliExSkill6_c,effects=iliExSkill6Eff1,description=iliExSkill6_1.description,effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER],ultimate=True,emoji='<:vitLum:1034208810853732524>')
iliExSkill2_1 = skill("Champ de Lumière","iliExSkill2",TYPE_INDIRECT_DAMAGE,effects=iliExSkill1Eff,emoji='<:iliLightField:1046381182767603752>',range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=5,effPowerPurcent=65,description="Iliana inflige des dégâts puis inflige un effet de dégâts continus aux ennemis autour d'elle",effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER])
iliExSkill2_c = effect("Cast - {replicaName}","iliExSkill2_c",silent=True,replique=iliExSkill2_1)
iliExSkill2 = skill("Révolution de Lumière","iliExSkill2",TYPE_DAMAGE,power=100,emoji='<:revolLum:1033720380281597983>',range=AREA_MONO,area=iliExSkill2_1.area,accuracy=120,cooldown=iliExSkill2_1.cooldown,effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER//3],use=CHARISMA,description=iliExSkill2_1.description,replay=True,effectOnSelf=iliExSkill2_c)

iliExSay = says(start="Je pense que ça devrait suffire... Je pense pouvoir vous donner suffisamant de fil à retordre tout en vous laissant une chance comme ça, bon courage !",onKill='Désolée si tu as du mal à voir pendant quelques temps',reactBigRaiseEnnemy="Ah, contente de voir que ce combat risque d'être un peu moins à sens unique",redWinAlive="Une autre fois peut-être",redLoose="Hé bah... Je dois avouer que vous vous débrouillez pas trop mal")

# Stella
stellaAuraEff = copy.deepcopy(dmgUp)
stellaAuraEff.power, stellaAuraEff.stat, stellaAuraEff.strength, stellaAuraEff.magie = 3.5, MAGIE, 5, 5
stellaAura = effect("Aura solaire","stellaAura", stat=MAGIE,trigger=TRIGGER_END_OF_TURN,denieWeap=True,callOnTrigger=stellaAuraEff,area=AREA_DONUT_2,turnInit=-1,unclearable=True,description="En fin de tour, augmente légèrement les dégâts infligés par les alliés alentours")
stellaWeap = weapon("Pulsion électro-magnetique","stellaWeap",RANGE_DIST,AREA_CIRCLE_5,53,75,magie=10,endurance=10,resistance=10,effects=stellaAura)
stellaSkill1 = skill("Galvanisation stellaire","stellaSkill1",TYPE_BOOST,range=AREA_MONO,area=AREA_CIRCLE_3,effects=stellaAuraEff,effPowerPurcent=300,cooldown=5,description="Augmente les dégâts infligés par les alliés alentours")
stellaSkill2Eff = copy.deepcopy(defenseUp)
stellaSkill2Eff.power, stellaSkill2Eff.stat = 7.5, MAGIE
stellaSkill2 = skill("Diffraction stellaire","stellaSkill2",TYPE_BOOST,effects=stellaSkill2Eff,area=AREA_CIRCLE_2,range=AREA_MONO,cooldown=5,description="Réduit les dégâts subis par les alliés alentours")
stellaSkill3Eff1, stellaSkill3Eff2 = copy.deepcopy(dmgUp), copy.deepcopy(defenseUp)
stellaSkill3Eff1.stat = stellaSkill3Eff2.stat = MAGIE
stellaSkill3Eff1.power, stellaSkill3Eff2.power = 5, 3.5
stellaSkill3 = skill("Focalisation galactique","stellaSkill3",TYPE_BOOST,effects=[stellaSkill3Eff1, stellaSkill3Eff2],cooldown=5,description="Augmente les dégâts infligés par un allié tout en réduisant les dégâts qu'il subit")
stellaSkill4Eff = copy.deepcopy(vulne)
stellaSkill4Eff.power, stellaSkill4Eff.stat, stellaSkill4Eff.turnInit = 7.5, MAGIE, 2
stellaSkill4 = skill("Affaiblissement stellaire","stellaSkill4",TYPE_MALUS,effects=stellaSkill4Eff,cooldown=5)
stellaLBEff, stellaLBEff2 = copy.deepcopy(defenseUp), copy.deepcopy(dmgUp)
stellaLBEff.power, stellaLBEff.stat, stellaLBEff2.power, stellaLBEff2.stat = 5, MAGIE, 7.5, MAGIE
stellaLBFinal = skill("Final stellaire","stellaLB",TYPE_ARMOR,range=AREA_MONO,area=AREA_CIRCLE_4,effects=[stellaLBEff,stellaLBEff2],effPowerPurcent=50,ultimate=True,cooldown=7,url="https://media.discordapp.net/attachments/927195778517184534/960234772498620426/20220403_194942.gif",description="Durant 3 tours, les dégâts reçu par les alliés sont réduit. À chaque tour, l'effet est donné avec 20% de puissance en moins",emoji=trans.emoji)
stellaLBGuide = effect("{0}".format(stellaLBFinal.name),"stellaLBGuide",turnInit=2,silent=True,replique=stellaLBFinal,emoji='<a:finStel:979889173274185750>')
stellaLB2 = copy.deepcopy(stellaLBFinal)
stellaLB2.effPowerPurcent, stellaLB2.effectOnSelf = 75, stellaLBGuide
stellaLBGuide2 = copy.deepcopy(stellaLBGuide)
stellaLBGuide2.replica = stellaLB2
stellaLB = copy.deepcopy(stellaLBFinal)
stellaLB.id, stellaLB.effPowerPurcent, stellaLB.url, stellaLB.effectOnSelf = "stellaLB", 100, "https://media.discordapp.net/attachments/927195778517184534/960234772926455908/20220403_194702.gif",stellaLBGuide2
stellaSkill5Eff = copy.deepcopy(vulne)
stellaSkill5Eff.power, stellaSkill5Eff.stat, stellaSkill5Eff.turnInit = 5, MAGIE, 3
stellaSkill5Eff2 = effect("Galvanisation Stellaire","stellaSkill5Eff2", stat=MAGIE,strength=10,magie=10,charisma=5,intelligence=5,endurance=3,agility=3,precision=3,turnInit=3,emoji="<:buffStellaire:1083755558517100677>")
stellaSkill5_1 = skill("Eruption Stellaire","stellaSkill5",TYPE_DAMAGE,power=100,area=AREA_ARC_1,use=MAGIE,effects=stellaSkill5Eff,description="Stella inflige des dégâts aux ennemis ciblés et augmente les dégâts reçus par la cible principale pendant 3 tours",emoji='<:erupStell:1083754013582971010>')
stellaSkill5_2 = skill("Explosion Stellaire","stellaSkill5",TYPE_DAMAGE,power=80,area=AREA_CIRCLE_3,use=MAGIE,effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_3,stellaSkill5Eff2],description="Stella inflige des dégâts aux ennemis ciblés et augmente les statistiques des alliés autour d'elle pendant 3 tours",emoji='<:erupStell:1083754013582971010>')
stellaSkill5 = skill("Puissance Stellaire","stellaSkill5",TYPE_DAMAGE,become=[stellaSkill5_1,stellaSkill5_2],emoji=stellaSkill5_2.emoji,description="Stella inflige des dégâts de zone et augmente les statistiques de ses alliés ou les dégâts reçus des ennemis")

# Kitsunes elem eff
earthKitEff = effect("Energie Téllurique","earthKitEff",turnInit=5,emoji='<:earth:918212824805801984>')

kitsuneExCharmEff = effect("Kyōhaku kan'nen","kitsuneExCharmEff",power=5,stat=CHARISMA,strength=-4,magie=-4,charisma=-3,intelligence=-3,precision=-2,agility=-2,turnInit=3,type=TYPE_MALUS,description="Réduit grandement les statistiques et augmente les dégâts subis de la part des kitsunes",emoji=sameSpeciesEmoji("<:charmExB:1103342588842475620>","<:charmExR:1103342559893405867>"),stackable=True)

KITCHARMVULNE, KITCHARM2VULNE = 2, 5

octoTour = weapon("noneWeap","aaa",RANGE_LONG,AREA_CIRCLE_1,0,0,0,resistance=500)
octoTourEff2 = effect("Protection magique","octTourEff2",redirection=100,turnInit=-1,emoji='<:tower:905169617163538442>')
octoTourEff1 = effect("Grand protecteur","octTourEff1",emoji='<:tower:905169617163538442>',description="L'OctoTour protège ses alliés\nTant qu'il est en vie, celui-ci subis les dégâts directs de ses alliés à leur place",trigger=TRIGGER_INSTANT,area=AREA_ALL_ALLIES,callOnTrigger=octoTourEff2)
octoTourSkill = skill("Grand protecteur","octoTourSkill",TYPE_PASSIVE,0,effectOnSelf=octoTourEff1,use=None,emoji='<:tower:905169617163538442>')