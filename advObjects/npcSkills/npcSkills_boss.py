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
jevilWeap = weapon("Projectiles","jevilWeap",RANGE_DIST,AREA_CIRCLE_4,80,50,ignoreAutoVerif=True,area=AREA_CONE_2,say="CHAOS, CHAOS, CATCH ME IF YOU CAN!",emoji='<:chaos:892857755143127090>',damageOnArmor=1.5,effects=jevilPassifEffect, priority=WEAPON_PRIORITY_NONE)

jevilSkill1_1e = effect("Pics", "jevilSkill1_1e", STRENGTH, type=TYPE_DAMAGE, area=AREA_DONUT_2, power=100, trigger=TRIGGER_INSTANT, emoji='<a:jevilSpade:1336432254309634069>')
jevilSkill1_1 = skill("Pics","jevilSkill1",TYPE_DAMAGE, power=250, area=AREA_MONO, emoji=jevilSkill1_1e.emoji[0][0], effects=jevilSkill1_1e, say="I CAN DO ANYTHING !", cooldown=3, damageOnArmor=1.5)
jevilSkill1_2 = skill("Trèfles","jevilSkill1",TYPE_DAMAGE, power=150, garCrit=True, area=AREA_CONE_2, emoji='<a:jevilClover:1336432817730617456>',say="I CAN DO ANYTHING !", cooldown=3, damageOnArmor=0.8)
jevilSkill1_3e = effect("Coeurs", 'jevilSkill1_3e', STRENGTH, type=TYPE_DAMAGE, trigger=TRIGGER_END_OF_TURN, area=AREA_CIRCLE_1, power=75, emoji='<a:jevilHeart:1336432801968296009>')
jevilSkill1_3 = skill("Coeurs","jevilSkill1",TYPE_INDIRECT_DAMAGE, range=AREA_MONO, area=AREA_RANDOMENNEMI_4, effects=[jevilSkill1_3e], emoji=jevilSkill1_3e.emoji[0][0], say="I CAN DO ANYTHING !", cooldown=3)
jevilSkill1_4 = skill("Carreaux","jevilSkill1",TYPE_DAMAGE, power=800, area=AREA_CIRCLE_3, range=AREA_CIRCLE_2, sharedDamage=True, emoji='<a:jevilPic:1336432782343274597>', say="I CAN DO ANYTHING !", cooldown=3, damageOnArmor=3)

jevilSkill1 = skill("Joker !","jevilSkill1",TYPE_DAMAGE,become=[jevilSkill1_1,jevilSkill1_2,jevilSkill1_3,jevilSkill1_4], emoji='<a:card:892855854712385637>')

jevilSkill2 = skill("Final Chaos","jevilSkill2",TYPE_DAMAGE, power=125, range=AREA_MONO, setAoEDamage=True,area=AREA_ALL_ENEMIES, say="KIDDING ! HERE'S MY FINAL CHAOS !", initCooldown=5, cooldown=4, emoji="<:devilknife:892855875600023592>", damageOnArmor=2, ultimate=True)
jevilSkill3 = skill("Carousel", "jevilSkill3", TYPE_DAMAGE, power=35, repetition=4, setAoEDamage=True, area=AREA_CIRCLE_3, range=AREA_MONO, cooldown=3, emoji='<:jevilCarousel:1336437009958309888>')

jevilSkill4Eff1, jevilSkill4Eff2 = copy.deepcopy(dmgDown), copy.deepcopy(vulne)
jevilSkill4Eff1.power = jevilSkill4Eff2.power = 50
jevilSkill4Eff3, jevilSkill4Eff4 = copy.deepcopy(incurable), copy.deepcopy(armorGetMalus)
jevilSkill4Eff4.power = jevilSkill4Eff4.power = 50
jevilSkill4Eff6 = copy.deepcopy(aconstEff)
jevilSkill4Eff6.power, jevilSkill4Eff6.stat = 50, PURCENTAGE

jevilSkill4EffList = [jevilSkill4Eff1, jevilSkill4Eff2, jevilSkill4Eff3, jevilSkill4Eff4, jevilSkill4Eff6 ]
for indx in range(len(jevilSkill4EffList)):
	jevilSkill4EffList[indx].turnInit = 3

jevilSkill4Eff5 = copy.deepcopy(deepWound)
jevilSkill4Eff5.power, jevilSkill4Eff5.stat = 200, STRENGTH
jevilSkill4EffList.append(jevilSkill4Eff5)

jevilSkill4 = skill("Chaos Chaos !", "jevilSkill4", TYPE_MALUS, effects=jevilSkill4EffList, area=AREA_ALL_ENEMIES, range=AREA_MONO, cooldown=3, emoji='<:jevilChaos:1336437049317658705>', description="Jevil inflige à tous ses ennemis un malus aléatoire parmis ceux cités dans la description de cette compétence")

# Luna (Oh it's will be funny)
lunaExPassive = effect("Position défensive", "lifeStealEffect", block=20, counterOnBlock=50, counterOnDodge=35, power=5, unclearable=True, turnInit=-1, emoji='<:lunaGuard:1348375355718766683>')
lunaWeap = weapon("Maîtrisse de l'Ombre Martiale","aaa",RANGE_MELEE,AREA_CIRCLE_1,35,40,strength=20,agility=10,precision=10,repetition=3,emoji='<:lunaGuard:1348375355718766683>',damageOnArmor=1.2,ignoreAutoVerif=True,priority=WEAPON_PRIORITY_NONE, effects=lunaExPassive)

lunaSkill1_1e = effect("Talon écrasant", "lunaSkill1_1e", superBreak=True, power=100, decateEndOfTurn=True, emoji='<:plongee:1088958906178474076>')
lunaSkill1_1 = skill("Talon écrasant", "lunaSkill1", TYPE_DAMAGE, power=400, sharedDamage=True, area=AREA_CIRCLE_1, cooldown=5, emoji='<:plongee:1088958906178474076>', effectOnSelf=lunaSkill1_1e, effBeforePow=True, description="Inflige deux attaques à l'ennemi ciblé puis une troisième attaque en zone autour de lui. La puissance de la dernière attaque est divisée par le nombre de cible ayant une arme de mêlée. Si les cibles n'ont plus d'armure après la dernière attaque, Luna leur inflige une instance de Rupture Extrême")
lunaSkill1_1c = effect("Enchainement", "lunaSkill1_1c", silent=True, replique=lunaSkill1_1)
lunaSkill1 = skill("Double Direct", "lunaSkill1", TYPE_DAMAGE, power=100/2, repetition=2, damageOnArmor=2, effectOnSelf=lunaSkill1_1c, cooldown=5, emoji='<:tripleStrike2:1060211719911264416>', replay=True)

lunaSkill5_4eff = effect("Onde de Choc","lunaSkill4_1eff", stat=STRENGTH,power=50,area=AREA_DONUT_1,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,emoji='<:darkShockWave:1185653578824679484>')

lunaSkill2_2 = skill("Plongeon", "lunaSkill2", TYPE_DAMAGE, power=100, garCrit=True, area=AREA_CIRCLE_2, tpCac=True, emoji='<:plongeon:1333183192064065557>', cooldown=5, percing=20)
lunaSkill2_2c = effect("Enchainement", "lunaSkill2_2c", replique=lunaSkill2_2, silent=True)
lunaSkill2_1 = skill("Ultimawashi", "lunaSkill2", emoji='<:ultimawashi:1088958958267535455>', types=TYPE_DAMAGE, power=100, knockback=2, tpCac=True, effects=lunaSkill5_4eff, percing=15, garCrit=True, replay=True, effectOnSelf=lunaSkill2_2c)
lunaSkill2_1c = effect("Enchainement", "lunaSkill2_1c", replique=lunaSkill2_1, silent=True)
lunaSkill2 = skill("Retourné", "lunaSkill2", TYPE_DAMAGE, power=100, effects=[weakGuard], effBeforePow=True, effectOnSelf=lunaSkill2_1c, knockback=2, emoji='<:retourne:1089331978668617848>', replay=True)

lunaSkill3e = effect("Position défensive", "lifeStealEffect", block=50, counterOnBlock=50, counterOnDodge=35, power=10)

lunaSkill4_2 = skill("Plongeon Ténébreux", "lunaSkill4", TYPE_DAMAGE, power=800, area=AREA_CIRCLE_2, tpCac=True, emoji='<:darkdown:1138876529753993297>', areaOnSelf=True, sharedDamage=True, damageOnArmor=2, ultimate=True, cooldown=7, condition=[EXCLUSIVE, ELEMENT, ELEMENT_DARKNESS])
lunaSkill4_2c = effect("Enchaînement", "lunaSkill4_2c", replique=lunaSkill4_2, silent=True)
lunaSkill4_1 = skill("Salto Kick", "lunaSkill4", TYPE_DAMAGE, power=135, ultimate=True, emoji='<:tripleStrike3:1060211755793522798>', knockback=2, effectOnSelf=lunaSkill4_2c, replay=True)
lunaSkill4_1c = effect("Enchaînement", "lunaSkill4_1c", replique=lunaSkill4_1, silent=True)
lunaSkill4 = skill("Double Kick", "lunaSkill4", TYPE_DAMAGE, power=100/2, repetition=2, emoji='<:tripleStrike1:1060211689217327114>', ultimate=True, damageOnArmor=3, range=AREA_CIRCLE_3, tpCac=True, replay=True, effectOnSelf=lunaSkill4_1c)

lunaSkill5_1 = skill("Reverse roundhouse-kick","lunaSkill5",TYPE_DAMAGE,0, 120, AREA_CIRCLE_1, garCrit=True, area=AREA_ARC_1,percing=20,emoji='<:talonFracassant:1088958995030605834>',damageOnArmor=2,description='Inflige des dégâts en zone à un ennemi au corps à corps')
lunaSkill5_2e = effect("Résistance réduites","lunaSkill52e", stat=PURCENTAGE,resistance=-50,turnInit=3)
lunaSkill5_2 = skill("Side-kick fouetté","lunaSkill5",TYPE_DAMAGE,0,150,AREA_CIRCLE_1,effects=[lunaSkill5_2e, weakGuard],garCrit=True,emoji='<:highKick:1122785057531236463>',percing=20,say="Hmf !",damageOnArmor=3,description='Inflige des dégâts à une cible unique au corps à corps\nDégâts triplé sur de l\'armure')
lunaSkill5_31 = skill("Backflip","lunaSkill5",TYPE_DAMAGE,power=75,garCrit=True,range=AREA_CIRCLE_1,knockback=1,emoji='<:inercie:1058338643707695155>',percing=20)
lunaSkill5_31_e = effect("Enchainement - {replicaName}","lunaSkill5_31",replique=lunaSkill5_31,silent=True)
lunaSkill5_3 = skill("Sweeping","lunaSkill5",TYPE_DAMAGE,0,75,AREA_CIRCLE_1,area=AREA_CIRCLE_1,areaOnSelf=True,emoji='<:baleyette:977166497422139392>',percing=20,replay=True,effectOnSelf=lunaSkill5_31_e,say="C'est que tu es colant toi !",description='Inflige des dégâts, étourdit pendant un tour et repousse un ennemi au corps à corps')
lunaSkill5_41 = skill("Side Kick","lunaSkill4_1",TYPE_DAMAGE,power=100,garCrit=True,range=AREA_CIRCLE_1,emoji='<:talonFracassant:1088958995030605834>',percing=20,effects=lunaSkill5_4eff)
lunaSkill5_41_e = effect("Enchainement - {replicaName}","lunaSkill5_41",replique=lunaSkill5_41,silent=True)
lunaSkill5_4 = skill("Double High roundhouse-kick","lunaSkill5",TYPE_DAMAGE,0,75,AREA_CIRCLE_1, effects=[weakGuard], effBeforePow=True, repetition=2, effectOnSelf=lunaSkill5_41_e,percing=20,replay=True,emoji='<:chainChoc1:1058339074563379240>',say="Hé vous derrière ! Cadeau !",damageOnArmor=2,description='Inflige des dégats et repousse de 3 cases un ennemi au corps à corps')
lunaSkill5Base = skill("Corps à corps","lunaSkill5",TYPE_DAMAGE,0,0,AREA_CIRCLE_1,emoji='<:luna4inOne:919260128698589184>',become=[lunaSkill5_1,lunaSkill5_2,lunaSkill5_3,lunaSkill5_4])

lunaSkill6 = skill("Vitesse ombrale","lunaSkill6",TYPE_DAMAGE,0,50,AREA_INLINE_4,emoji='<:lunaDash:932286143884566528>',cooldown=3,replay=True,tpCac=True,accuracy=200,description='Se téléporte au corps à corps d\'un ennemi et vous permet de rejouer votre tour')
lunaSkill7eff = copy.deepcopy(lunaSkill5_4eff)
lunaSkill7eff.power = 65
lunaSkill7 = skill("Genoux Explosif","lunaSkill7",TYPE_DAMAGE,power=175,percing=25,damageOnArmor=1.5,effects=lunaSkill7eff,cooldown=3,range=AREA_INLINE_4,tpCac=True,emoji='<:darkRenf:1120974892188315740>')

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
tgesweape = copy.deepcopy(constEff)
tgesweape.power, tgesweape.stat, tgesweape.turnInit = 50, PURCENTAGE, -1
TGESWeap = weapon("noneWeap","TheGiantEnemySpiderWeapon",RANGE_DIST,AREA_CIRCLE_1,power=0,accuracy=0,effects=tgesweape)
TGESSkill1 = skill("Projectile","TheGiantEnemySpiderSkill1",TYPE_DAMAGE,0,int(GESLskill.power*1.5),emoji=webSpitterWeap.emoji)
TGESSkill2 = skill("Déluge de toile","tgesskill2",TYPE_DAMAGE,power=50,setAoEDamage=True,cooldown=3,emoji=myrlopeSkill1Eff.emoji[0][0],range=AREA_MONO,area=AREA_ALL_ENEMIES,effectAroundCaster=[TYPE_MALUS,AREA_ALL_ENEMIES,myrlopeSkill1Eff],description="Inflige des dégâts à tous les ennemis et réduit leur probabilité d'esquive")

# Matt from WiiSport
mattWeapon = weapon("Direct !","mattWeapon",RANGE_DIST,AREA_CIRCLE_1,60,70,repetition=3,emoji='<:boxe:922064460326244384>',ignoreAutoVerif=True)
mattSkill1 = skill("Home Run !","mattSkill1",TYPE_DAMAGE,0,150,AREA_CIRCLE_1,cooldown=4,knockback=5,description="Quel magnifique coup de batte !",emoji='<:homerun:922064424708239360>')
mattSkill2 = skill("Tir à trois points","mattSkill2",TYPE_DAMAGE,0,80,AREA_DIST_5,cooldown=3,description="Quel tir ! Qui aurait cru qu'il ferait un panier d'ici ?",emoji='<:basket:922064483688513567>')
mattSkill3 = skill("Strike !","mattSkill3",TYPE_DAMAGE,0,135,AREA_CIRCLE_1,area=AREA_LINE_6,cooldown=3,description="Non vous pouvez pas appuyer sur A pour passer la cinématique",emoji='<:bowling:922064440201969724>')
mattSkill4Eff = effect("Gardé","matt(en)Garde", stat=STRENGTH,power=25,lvl=99,onDeclancher=True,immunity=True,description="Une vision accru vous permet de contrer les dégâts et de contre attaquer !")
mattSkill4 = skill("Garde","mattSkill4",TYPE_DAMAGE,0,cooldown=5,range=AREA_CIRCLE_1,power=100,effectOnSelf=mattSkill4Eff,description="Inflige des dégâts à l'ennemi ciblé et vous immunise contre tous dégâts jusqu'à votre prochain tour. Si vous êtes attaqué pendant cette durée, inflige des dégâts indirects à l'attaquant")

kikuPassivSkillEff = effect("Cimetière","kikuGraveyardEff1",type=TYPE_SUMMON,callOnTrigger=lightSkeleton,trigger=TRIGGER_START_OF_TURN,turnInit=-1,unclearable=True,lvl=1,emoji='<:graveyard:1164906144339341424>',description="Kiku invoque deux squelettes autour d'elle à chaque fois qu'elle commence son tour",area=AREA_CIRCLE_1,denieWeap = True,dodge=-100)
kikuWeap = weapon("Tir d'énergie","kikuWeap", RANGE_LONG, AREA_CIRCLE_5,power=100,accuracy=150, endurance=15,magie=15, priority=WEAPON_PRIORITY_LOWEST,effects=kikuPassivSkillEff,ignoreAutoVerif=True,use=MAGIE,emoji='<:energyWeap:1164909709950730270>')
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

akikiSkill1Eff2 = copy.deepcopy(dmgUp)
akikiSkill1Eff2.power, akikiSkill1Eff2.turnInit, akikiSkill1Eff2.unclearable = 20, -1, True

akikiSkill1Eff3 = effect("Rage Croissante II","akikiSkill1Eff3",callOnTrigger=akikiSkill1Eff2, trigger=TRIGGER_HP_UNDER_70, turnInit=25, stackable=True)
akikiSkill1Eff4, akikiSkill1Eff5 = copy.deepcopy(akikiSkill1Eff3), copy.deepcopy(akikiSkill1Eff3)  
akikiSkill1Eff4.name, akikiSkill1Eff5.name, akikiSkill1Eff4.trigger, akikiSkill1Eff5.trigger = "Rage Croissante III", "Rage Croissante IV", TRIGGER_HP_UNDER_50, TRIGGER_HP_UNDER_25

akikiSkill1Eff = effect("Rage Croissante","akikiRageDmgBuff",turnInit=-1,unclearable=True,emoji=dmgUp.emoji,power=50)
akikiSkill1 = skill("Rage Croissante","akikiSkill1",TYPE_PASSIVE,effects=[akikiSkill1Eff, akikiSkill1Eff3, akikiSkill1Eff4, akikiSkill1Eff5 ],emoji=akikiSkill1Eff.emoji[0][0],description="Accroie les dégâts directs infligés par Akira au fur et à mesure que ses PVs diminuent, jusqu'à **+{0}%** avec 0.1% de PV restants".format(akikiSkill1Eff.power))

akikiSkill2_2 = skill("Destruction Explosive","akikiSkill2",TYPE_DAMAGE,emoji='<:akiTankStack:1007050856748818464>',power=600,range=AREA_CIRCLE_4,tpCac=True,cooldown=3,area=AREA_CIRCLE_1,description="Inflige d'énormes dégâts aux ennemis ciblés. La puissance est divisée par le nombre d'ennemi ayant une aspiration de mêlée dans la zone d'effet",sharedTB=True)
akikiSkill2_1 = skill("Destruction Concentrique","akikiSkill2",TYPE_DAMAGE,range=AREA_CIRCLE_3,power=250,cooldown=3,area=AREA_CIRCLE_1,emoji='<:akiTB:1007050875451220059>')
akikiSkill2 = skill("Destruction",akikiSkill2_2.id, TYPE_DAMAGE, become=[akikiSkill2_1,akikiSkill2_2], emoji=akikiSkill2_2.emoji)

akikiSkill3 = skill("Massacre","akikiSkill3",TYPE_DAMAGE,0,power=150,range=AREA_MONO,area=AREA_CIRCLE_2,accuracy=80,cooldown=5)
akikiSkill4 = skill("Intolérance","akikiSkill4",TYPE_DAMAGE,0,power=120,range=AREA_CIRCLE_3,area=AREA_LINE_2,cooldown=5)

akikiSkill5_1 = skill("Frappe Enragée","akikiSkill3_1",TYPE_DAMAGE,power=400,cooldown=5,emoji='<:akiStack:1007050822338748466>',area=AREA_CIRCLE_3,range=AREA_DONUT_5,tpCac=True,description="Akira marque un ennemi au premier tour puis inflige de lourds dégâts à l'ennemi marqué et ceux aux alentours.\nLa puissance est divisée par le nombre d'ennemi dans la zone d'effet.",sharedDamage=True)
akikiSkill5_2 = skill("Frappe Haineuse","akikiSkill3_2",TYPE_DAMAGE,power=80,cooldown=5,area=AREA_CIRCLE_1,emoji='<:akiAway:1007050839514435584>',range=AREA_DONUT_5,description="Marque 3 ennemis au premier tour puis inflige au second tour des dégâts à tous les ennemis marquées et ceux autour d'eux. Chaque attaque augmente les dégâts reçus des ennemis affecté, augmentant aussi ceux subis par les ennemis prenant plusieurs fois des dégâts par cette attaque")
akikiSkill5 = skill("Atomisation", "akikiSkill5", TYPE_DAMAGE, become=[akikiSkill5_1,akikiSkill5_2], emoji=akikiSkill5_2.emoji)

unformBossWeapon = weapon("Arme aforme","unformBossWeap",RANGE_DIST,AREA_CIRCLE_1,150,80,ignoreAutoVerif=True)
unformBossSkill1 = skill("Distorsion Dimentionelle","unformBossSkill1",TYPE_DAMAGE,power=250,range=AREA_CIRCLE_1,cooldown=7,use=MAGIE)
unformBossSkill2Eff = copy.deepcopy(dmgUp)
unformBossSkill2Eff.power = 50
unformBossSKill2 = skill("Anéantissement accéléré","unformBossSKill2",TYPE_BOOST,range=AREA_MONO,area=AREA_CIRCLE_3,effects=unformBossSkill2Eff,cooldown=5)
unformBossSkill3 = skill("Pulsion spaciale","unformBossSkill3",TYPE_HEAL,power=250,use=MAGIE,range=AREA_MONO,area=AREA_CIRCLE_5,cooldown=5)

unformBoss = octarien("Aformité incarnée",300,250,200,50,50,200,350,25,15,0,unformBossWeapon,15,'<:uShadow:938530004319477821>',[unformBossSkill1,unformBossSKill2,unformBossSkill3],description="Un leader de l'assaut des aformités, qui cherchent à détruire le multivers",deadIcon='<:em:866459463568850954>',team=NPC_UNFORM)

# Iliana Ex.
ILIREGENPOWER = 35
iliExWeapEff = effect("Conviction de la Lumière","iliExPasRegenEff", stat=CHARISMA,turnInit=-1,unclearable=True,block=35,emoji='<:ilianaStans:969819202032664596>',description="Accorde à Iliana Ex. 35% de blocage")
iliExWeapon = weapon("Epée et Bouclier de la Lumière","iliExWeap",RANGE_DIST,AREA_CIRCLE_1,100,100,effects=iliExWeapEff,emoji='<:iliShield:975785889512976434>',ignoreAutoVerif=True,use=CHARISMA,priority=WEAPON_PRIORITY_LOWEST)
iliExSkill1Eff = effect("Corruption Lumineuse","iliExSkill1Eff", stat=CHARISMA, power=25,lvl=5,stackable=True,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,description="Un déséquilibre élémentaire vous provoque des dégâts sur la durée",emoji='<:iliDot:1046387034522136609>')
iliExSkill1 = skill("Flash","iliExSkill1",TYPE_INDIRECT_DAMAGE,cooldown=5,area=AREA_CIRCLE_4,range=AREA_MONO,effects=iliExSkill1Eff,emoji='<:flash:977025336518799420>',effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER])

iliExSkill3 = skill("Vague de Lumière","iliExSkill3",TYPE_DAMAGE,power=80,area=AREA_CONE_3,use=CHARISMA,cooldown=4,range=AREA_CIRCLE_1,effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER])
iliExSkill4_1 = skill("Ardeur Lumineuse","iliExSkill4",TYPE_DAMAGE,power=100,repetition=2, garCrit=True,range=AREA_CIRCLE_2,emoji='<:iliBravor:1046381213910302834>',use=CHARISMA,cooldown=5,description="Iliana se téléporte au corps à corps d'un ennemi puis lui inflige des dégâts monocible à deux reprises",effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER],url=lb1Mono.url)
iliExSkill4_c = effect("Cast - {replicaName}","iliExSkill4_c",replique=iliExSkill4_1,silent=True)
iliExSkill4 = skill("Vitesse Lumière","iliExSkill4",TYPE_DAMAGE,tpCac=True,cooldown=iliExSkill4_1.cooldown,replay=True,power=35,use=CHARISMA,description=iliExSkill4_1.description,emoji='<:iliLightSpeed:1046384202792308797>',effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER//3],effectOnSelf=iliExSkill4_c)

iliExSkill5_2 = skill("Lumière Eternelle", "iliExLb", TYPE_DAMAGE, power=250, cooldown=7, accuracy=500, use=CHARISMA, affSkillMsg=False, setAoEDamage=True, ultimate=True, range=AREA_MONO, area=AREA_CIRCLE_2, emoji='<:ancientLight2:1147186259115118613>', description="Après un tour de chargement, Iliana inflige des dégâts à tous ses ennemis, puis une second attaque et {0} aux ennemis proche d'elle".format(weakGuard), effectAroundCaster=[TYPE_MALUS, AREA_CIRCLE_2, weakGuard])
iliExSkill5_2c = effect("","iliExLbc",silent=True,replique=iliExSkill5_2)
iliExSKill5_1 = skill("Lumière Eternelle","iliExLb",TYPE_DAMAGE,cooldown=7,power=150,use=CHARISMA, accuracy=500, setAoEDamage=True,ultimate=True, effectOnSelf=iliExSkill5_2c, replay=True,range=AREA_MONO,area=AREA_ALL_ENEMIES,emoji="<:eternalLight:1116761926052089856>",description=iliExSkill5_2.description,effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER*1.5])
iliExSkill5_c = effect("","iliExLbc",turnInit=2,silent=True,replique=iliExSKill5_1)
iliExSKill5 = skill("Lumière Eternelle","iliExLb",TYPE_DAMAGE,cooldown=iliExSKill5_1.cooldown+1,use=CHARISMA,effectOnSelf=iliExSkill5_c,range=AREA_MONO,area=AREA_ALL_ENEMIES,emoji=iliExSKill5_1.emoji,ultimate=True,description=iliExSKill5_1.description)
iliExSkill6Eff2 = effect("Bouclier Dressé","iliExSkill6EffBck",block=15,emoji='<:shieltron:971787905758560267>')
iliExSkill6_1 = skill("Fragmentation","iliExSkill6",TYPE_DAMAGE,use=CHARISMA,power=100, accuracy=150, repetition=3, percing=25, emoji='<:fragmentation:1117375884446412872>',ultimate=True,range=AREA_INLINE_3, area=AREA_CONE_2 ,effectOnSelf=iliExSkill6Eff2,description="Iliana bash violament un ennemi puis, après un tour de chargement, lui assigne plusieurs coups d'épée\nLe choc initial inflige l'effet {0} à la cible tout en augmentant le taux de blocage d'Iliana".format(weakGuard),cooldown=5,effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER//2*3])
iliExSkill6_c = effect("Cast - {replicaName}","iliExSkill6_c",turnInit=2,replique=iliExSkill6_1)
iliExSkill6 = skill(iliExSkill6_1.name,iliExSkill6_1.id,TYPE_DAMAGE,power=100,range=AREA_INLINE_4,effectOnSelf=iliExSkill6_c,effects=weakGuard, effBeforePow=True, description=iliExSkill6_1.description,effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER],ultimate=True,emoji='<:vitLum:1034208810853732524>')

iliExSkill2_1 = skill("Champ de Lumière","iliExSkill2",TYPE_INDIRECT_DAMAGE,effects=iliExSkill1Eff,emoji='<:iliLightField:1046381182767603752>',range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=5,effPowerPurcent=125,description="Iliana inflige des dégâts puis inflige un effet de dégâts continus aux ennemis autour d'elle",effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER])
iliExSkill2_c = effect("Cast - {replicaName}","iliExSkill2_c",silent=True,replique=iliExSkill2_1)
iliExSkill2 = skill("Révolution de Lumière","iliExSkill2",TYPE_DAMAGE,power=125,emoji='<:revolLum:1033720380281597983>',range=AREA_MONO,area=iliExSkill2_1.area,accuracy=120,cooldown=iliExSkill2_1.cooldown,effectAroundCaster=[TYPE_HEAL,AREA_MONO,ILIREGENPOWER//3],use=CHARISMA,description=iliExSkill2_1.description,replay=True,effectOnSelf=iliExSkill2_c)

iliExSay = says(start="Je pense que ça devrait suffire... Je pense pouvoir vous donner suffisamant de fil à retordre tout en vous laissant une chance comme ça, bon courage !",onKill='Désolée si tu as du mal à voir pendant quelques temps',reactBigRaiseEnnemy="Ah, contente de voir que ce combat risque d'être un peu moins à sens unique",redWinAlive="Une autre fois peut-être",redLoose="Hé bah... Je dois avouer que vous vous débrouillez pas trop mal")

# Stella
stellaAuraEff = effect("Aura Stellaire", "stellaAuraEff", stat=MAGIE, strength=5, magie=5, silentRemove=True, emoji='<:stellaBuff:1355625272489021574>')
stellaAura = effect("Aura solaire","stellaAura", stat=MAGIE,trigger=TRIGGER_END_OF_TURN, emoji='<:stellaAura:1355564851166056448>',denieWeap=True,callOnTrigger=stellaAuraEff,area=AREA_DONUT_5,turnInit=-1,unclearable=True,description="En fin de tour, augmente les statistiques offensives des alliés alentours")
stellaWeap = weapon("Pulsion électro-magnetique","stellaWeap",RANGE_DIST,AREA_CIRCLE_5,53,75,magie=10,endurance=10,resistance=10,effects=stellaAura)

stellaSkill1Eff = copy.deepcopy(dmgUp)
stellaSkill1Eff.stat, stellaSkill1Eff.power, stellaSkill1Eff.turnInit = MAGIE, 5, 3
stellaSkill1 = skill("Galvanisation stellaire","stellaSkill1", TYPE_BOOST, emoji='<:lightAura:1133263881955967127>', range=AREA_CIRCLE_3, area=AREA_CIRCLE_3, effects=stellaSkill1Eff, cooldown=7, description="Augmente les dégâts infligés par les alliés ciblés durant 3 tours")
stellaSkill2Eff = copy.deepcopy(defenseUp)
stellaSkill2Eff.power, stellaSkill2Eff.stat = 7.5, MAGIE
stellaSkill2Eff2 = effect("Protection Stellaire", "stellaSkill2Eff2", MAGIE, overhealth=20, type=TYPE_ARMOR, emoji='<:illumi1:902008944887746611>')
stellaSkill2 = skill("Diffraction stellaire","stellaSkill2", TYPE_BOOST, effects=[stellaSkill2Eff, stellaSkill2Eff2], emoji='<:lightAura3:1133264372957978745>', area=stellaSkill1.area, range=stellaSkill1.range, cooldown=5, description="Réduit les dégâts subis par les alliés ciblés et leur octroi de armure")

stellaSkill3Eff1, stellaSkill3Eff2 = copy.deepcopy(dmgUp), copy.deepcopy(defenseUp)
stellaSkill3Eff1.stat = stellaSkill3Eff2.stat = MAGIE
stellaSkill3Eff1.turnInit = stellaSkill3Eff2.turnInit = 3
stellaSkill3Eff1.power, stellaSkill3Eff2.power = 10, 5
stellaSkill3Eff3, stellaSkill3Eff4 = copy.deepcopy(stellaSkill3Eff1), copy.deepcopy(stellaSkill3Eff2)
stellaSkill3Eff3.power, stellaSkill3Eff4.power = stellaSkill3Eff1.power/2, stellaSkill3Eff2.power/2
stellaSkill3Eff5, stellaSkill3Eff6 = effect("Focalisation Offensive", "stellaSkill3Eff5", trigger=TRIGGER_INSTANT, area=AREA_DONUT_2, callOnTrigger=stellaSkill3Eff3), effect("Focalisation Défensive", "stellaSkill3Eff6", trigger=TRIGGER_INSTANT, area=AREA_DONUT_2, callOnTrigger=stellaSkill3Eff4)
stellaSkill3 = skill("Focalisation galactique","stellaSkill3",TYPE_BOOST, emoji='<:spaceLong:957762451515011112>', range=AREA_DONUT_4, effects=[stellaSkill3Eff1, stellaSkill3Eff2, stellaSkill3Eff5, stellaSkill3Eff6], cooldown=5, description="Augmente les dégâts infligés par un allié tout en réduisant les dégâts qu'il subit. Les alliés proches de la cible reçoivent également les bonus dans un effet moindre")

stellaSkill4Eff = copy.deepcopy(vulne)
stellaSkill4Eff.power, stellaSkill4Eff.stat, stellaSkill4Eff.turnInit = 7.5, MAGIE, 3
stellaSkill4Eff2 = copy.deepcopy(stellaSkill4Eff)
stellaSkill4Eff2.power = stellaSkill4Eff2.power / 2
stellaSkill4Eff3 = effect("Éclatement Stellaire", "stellaSkill4Eff3", area=AREA_DONUT_2, callOnTrigger=stellaSkill4Eff2, trigger=TRIGGER_INSTANT)
stellaSkill4Eff4 = effect("Lumino Desturbance", "stellaSkill4Eff4", type=TYPE_MALUS, power=35, superBreak=True, turnInit=stellaSkill4Eff.turnInit, emoji='<:eclatLum:1067824343658283089>')
stellaSkill4 = skill("Affaiblissement stellaire","stellaSkill4",TYPE_DAMAGE, area=AREA_CIRCLE_2, accuracy=500, power=50, percing=50, use=MAGIE, effects=[stellaSkill4Eff4, stellaSkill4Eff, stellaSkill4Eff3], cooldown=5, emoji='<:eclatLum:1067824343658283089>', description="Inflige des dégâts à l'ennemi ciblé, puis augmente les dégâts qu'il subit")

stellaLBEff, stellaLBEff2, stellaLBEff3 = copy.deepcopy(defenseUp), copy.deepcopy(dmgUp), effect("Éclat", "stellaLbEff3", MAGIE, power=50, area=AREA_CIRCLE_1, silentRemove=True, replace=True, emoji='<:starDust:1157641733161635861>', magie=5, strength=5, charisma=5, intelligence=5, precision=5, agility=5)
stellaLBEff.power, stellaLBEff.stat, stellaLBEff2.power, stellaLBEff2.stat = 7.5, MAGIE, 10, MAGIE
stellaLBEff.turnInit = stellaLBEff2.turnInit
stellaLB = skill("Final stellaire","stellaLB", TYPE_BOOST, range=AREA_MONO, area=AREA_ALL_ALLIES, effects=[stellaLBEff,stellaLBEff2,stellaLBEff3], ultimate=True, cooldown=7, url="https://media.discordapp.net/attachments/927195778517184534/960234772926455908/20220403_194702.gif",description="Aumgente les dégâts infligés ainsi que les statistiques principales de tous les alliés et réduit les dégâts qu'ils subissent",emoji=trans.emoji)

stellaSkill5Eff = copy.deepcopy(vulne)
stellaSkill5Eff.power, stellaSkill5Eff.stat, stellaSkill5Eff.turnInit = 5, MAGIE, 3
stellaSkill5Eff2 = effect("Galvanisation Stellaire","stellaSkill5Eff2", stat=MAGIE,strength=7.5,magie=7.5,charisma=5,intelligence=5,endurance=3,agility=3,precision=3,turnInit=3,emoji="<:buffStellaire:1083755558517100677>")
stellaSkill5_1 = skill("Eruption Stellaire","stellaSkill5",TYPE_DAMAGE,power=100,area=AREA_ARC_1,use=MAGIE,effects=stellaSkill5Eff,description="Stella inflige des dégâts aux ennemis ciblés et augmente les dégâts reçus par la cible principale pendant 3 tours",emoji='<:erupStell:1083754013582971010>')
stellaSkill5_2 = skill("Explosion Stellaire","stellaSkill5",TYPE_DAMAGE,power=80,area=AREA_CIRCLE_3,use=MAGIE,effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_3,stellaSkill5Eff2],description="Stella inflige des dégâts aux ennemis ciblés et augmente les statistiques des alliés autour d'elle pendant 3 tours",emoji='<:erupStell:1083754013582971010>')
stellaSkill5 = skill("Puissance Stellaire","stellaSkill5",TYPE_DAMAGE,become=[stellaSkill5_1,stellaSkill5_2],emoji=stellaSkill5_2.emoji,description="Stella inflige des dégâts de zone et augmente les statistiques de ses alliés ou les dégâts reçus des ennemis")

# Kitsunes elem eff
earthKitEff = effect("Energie Téllurique","earthKitEff",turnInit=5,emoji='<:earth:918212824805801984>')

KITCHARMVULNE, KITCHARM2VULNE = 2, 15

octoTour = weapon("noneWeap","aaa",RANGE_LONG,AREA_CIRCLE_1,0,0,0,resistance=500)
octoTourEff2 = effect("Protection magique","octTourEff2",redirection=100,turnInit=99,emoji='<:tower:905169617163538442>',silent=True, hide=True)
octoTourEff1 = effect("Grand protecteur","octTourEff1",emoji='<:tower:905169617163538442>',description="L'OctoTour protège ses alliés\nTant qu'il est en vie, celui-ci subis les dégâts directs de ses alliés à leur place",trigger=TRIGGER_INSTANT,area=AREA_ALL_ALLIES,callOnTrigger=octoTourEff2)
octoTourSkill = skill("Grand protecteur","octoTourSkill",TYPE_PASSIVE,0,effectOnSelf=octoTourEff1,use=None,emoji='<:tower:905169617163538442>')

darkZenecaWeap = weapon("Pinceau KuroMagic","darkZenecaWeap",RANGE_DIST,AREA_CIRCLE_3,power=80,accuracy=0,priority=WEAPON_PRIORITY_NONE,emoji="<:zenecaBrush2:1214961720691527800>",effects=toxicure,use=MAGIE)
darkZenecaDot = effect("Peste", "darkZenecaDot", MAGIE, power=35, turnInit=5, trigger=TRIGGER_START_OF_TURN, stackable=True, type=TYPE_INDIRECT_DAMAGE, emoji='<:darkTox:1231975040912723998>', lifeSteal=15)
darkZenecaSkill1DeplSkill = skill("CoroZone","darkZenecaSkill1DeplSkill",TYPE_INDIRECT_DAMAGE,effects=[darkZenecaDot],range=AREA_MONO,area=AREA_CIRCLE_1,emoji='<:toxicTouch:1177634174350401557>', effPowerPurcent=50)
darkZenecaSkill1Depl = depl("CoroZone",darkZenecaSkill1DeplSkill,["<:toxiEff:1223595956415496213>","<:toxiEff:1223595956415496213>"])
darkZenecaSkill1Eff = effect("CoroZone","coroZoneEff",type=TYPE_DEPL,callOnTrigger=darkZenecaSkill1Depl,trigger=TRIGGER_INSTANT,emoji=darkZenecaSkill1Depl.icon[0])
darkZenecaSkill1 = skill("CoroZone","darkZenecaSkill1",TYPE_DAMAGE, range=AREA_CIRCLE_3, area=darkZenecaSkill1DeplSkill.area+1,emoji='<:toxicTouch:1177634174350401557>',ultimate=False,cooldown=7,power=125,effects=darkZenecaSkill1Eff,description="Inflige des dégâts aux ennemis ciblés et fait apparaitre une flaque de poison à leur pieds, empoisant les ennemis dedans durant un moment",use=MAGIE)
darkZenecaSkill2Eff = effect("DarkSad","darkZenecaSkill2Eff",MAGIE, trigger=TRIGGER_ON_REMOVE, area=AREA_CIRCLE_2,type=TYPE_INDIRECT_DAMAGE,emoji='<:disizosadEff:1177590836238753852>',power=75)
darkZenecaSkill2 = skill("DarkSad","darkZenecaSkill2",TYPE_DAMAGE, power=100, percing=50,effects=darkZenecaSkill2Eff,emoji="<:disizisad:1177590810338930708>",use=MAGIE,cooldown=5,description="Inflige des dégâts à l'ennemi ciblé en ignorant une partie de son endurance. Lors du prochain tour, inflige des dégâts indirects en zone autour de la cible")
darkZenecaSkill3 = skill("ToxiMarre","darkZenecaSkill3",TYPE_DAMAGE, power=120, setAoEDamage=True, range=AREA_MONO, area=AREA_CIRCLE_2, effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_CIRCLE_2,darkZenecaDot], cooldown=5, emoji='<:chipToxiHeal:1221119824223014924>', use=MAGIE, description="Inflige des dégâts aux ennemis alentours et leur inflige {0}".format(darkZenecaDot), minTargetRequired=3 )
darkZenecaSkill4 = skill("ToxiStrike","darkZenecaSkill4",TYPE_DAMAGE, power=80, effects=darkZenecaDot, effPowerPurcent=70, emoji='<:toxicHearth:1177634139516706919>',description="Inflige des dégâts à l'ennemi ciblé ainsi que {0} (70%)".format(darkZenecaDot),use=MAGIE)
darkZenecaSkill4.iaPow = 10
darkZenecaSkill5Eff1, darkZenecaSkill5Eff2 = copy.deepcopy(incurable), copy.deepcopy(armorGetMalus)
darkZenecaSkill5Eff1.power = darkZenecaSkill5Eff2.power = 40
darkZenecaSkill5Eff1.turnInit = darkZenecaSkill5Eff2.turnInit = 3
darkZenecaSkill5Eff3, darkZenecaSkill5Eff4 = effect("DarkSentiments","darkSentEff1",trigger=TRIGGER_INSTANT,callOnTrigger=darkZenecaSkill5Eff1,type=TYPE_MALUS, emoji='<:zenecaUlt1:1214961183673684018>'), effect("DarkSentiments","darkSentEff2",trigger=TRIGGER_INSTANT,callOnTrigger=darkZenecaSkill5Eff2,type=TYPE_MALUS, emoji='<:zenecaUlt2:1214960718126784522>')
darkZenecaSkill5Eff3.area = darkZenecaSkill5Eff4.area = AREA_CIRCLE_2
darkZenecaSkill5 = skill("Rancour","darkZenecaSkill5",TYPE_INDIRECT_DAMAGE,effects=[intoxEff,epidemicEff,markInfexEff,darkZenecaSkill5Eff3, darkZenecaSkill5Eff4],ultimate=True,cooldown=7,description="Inflige {0}, {1} à l'ennemi ciblé, et {2} et {3} à la cible et aux ennemis alentours".format(intoxEff,epidemicEff,darkZenecaSkill5Eff3.callOnTrigger,darkZenecaSkill5Eff4.callOnTrigger),emoji='<:markInfex:1212102833059663953>')

darkZenecaSkill6e = copy.deepcopy(kafkaUltEff)
darkZenecaSkill6e.power, darkZenecaSkill6e.name, darkZenecaSkill6e.emoji = 65, "Implosion", uniqueEmoji("<:propabMark:1126773443975729153>")
darkZenecaSkill6 = skill("Implosion", "darkZenSkill6", TYPE_DAMAGE, power=100, area=AREA_CIRCLE_1, use=MAGIE, cooldown=5, initCooldown=3, emoji='<:propagMark:1126773337914359949>', effects=darkZenecaSkill6e, description="Inflige des dégâts à la cible et les ennemis alentours. La cible reçoit des dégâts supplémentaires en fonction de tous les effects de dégâts sur la durée dont elle souffre")
darkZenecaPassiveEff = effect("Dégâts indirects subis réduits","darkZenecaPassifEff",turnInit=-1,unclearable=True,silent=True,inkResistance=40,counterOnDodge=25,dodge=15,aggro=-35)
darkZenecaPassive = skill("Vaccin","sarkZenecaPassive",TYPE_PASSIVE,effects=[darkZenecaPassiveEff,counterTimeEff],description="Réduit les dégâts indirects reçus")

darkZenecaSays=says(
    start="J'espère que vous n'oublirez pas de respecter les distanciations sociales.",
    ultimate="J'vais vous montrer pourquoi vous auriez dû vous faire vacciner",
    onKill="Ni repris ni échangé",
    redWinAlive="Prenez ça bande d'anti-vaxs.",
    reactEnnemyKilled="Hm.",
    getHealed="Thx.",
    redLoose="Aw."
)


cohozonaWeap = weapon("écailles d'argent", "cohozonaWeap", range=RANGE_DIST, effectiveRange=AREA_CIRCLE_1, power=0, priority=WEAPON_PRIORITY_NONE)
cohozonaSkill1 = skill("Body Slam", "cohozonaSkill1", TYPE_DAMAGE, power=120, area=AREA_LINE_2, range=AREA_CIRCLE_1, cooldown=1)
cohozonaSkill2_1 = skill("Splash Chromatique", "cohozonaSkill2", TYPE_DAMAGE, power=200, area=AREA_CIRCLE_2, range=AREA_CIRCLE_3, tpCac=True, areaOnSelf=True, cooldown=3, emoji='<:splashdown:884803808402735164>')
cohozonaSkill2_c = effect("Cast - {replicaName}", "cohozonaSkill2_c", silent=True, turnInit=2, replique=cohozonaSkill2_1)
cohozonaSkill2 = copy.deepcopy(cohozonaSkill2_1)
cohozonaSkill2.power, cohozonaSkill2.tpCac, cohozonaSkill2.areaOnSelf, cohozonaSkill2.effectOnSelf = 0, False, False, cohozonaSkill2_c


SALMOTORI_NB_BOSS = 8
cohozonaGoldenCanonEff = effect("Tir de canon à oeuf", "eggCanonShot", PURCENTAGE, type=TYPE_UNIQUE, hide=True, power=round(75/(SALMOTORI_NB_BOSS-1),2), turnInit=99, trigger=TRIGGER_DEATH, emoji='<:Egg_Cannon:1314639875538161715>',)
cohozonaGoldenCanonEff2 = effect("Eggxtra Wave", "cohozonaGoldenCanonEff2", type=TYPE_MALUS, trigger=TRIGGER_INSTANT, area=AREA_DONUT_7, callOnTrigger=cohozonaGoldenCanonEff , emoji='<:golden_egg:1314640526842269766>', stat=FIXE)
cohozonaPasEff2 = copy.deepcopy(aconstEff)
cohozonaPasEff2.power, cohozonaPasEff2.turnInit, cohozonaPasEff2.unclearable, cohozonaPasEff2.stat, cohozonaPasEff2.hide = 25, -1, True, PURCENTAGE, True
cohozonaPasEff = effect("Eggxtra Wave", "cohozonaPasEff", None, callOnTrigger=cohozonaPasEff2, trigger=TRIGGER_INSTANT, area=AREA_DONUT_7)
cohozonaGoldenCanonPass = skill("Eggxtra Wave", "cohozonaSkillp", TYPE_PASSIVE, effects=[cohozonaGoldenCanonEff2, cohozonaPasEff], description="Lors qu'un Salmonoboss est vaincu, le SalmoMonarque subis des dégâts indirects fixes d'une valeur de **{0}%** de ses PV maximums de la part de l'entité ayant vaincu le salmonoboss".format(cohozonaGoldenCanonEff.power))

# Imea
imeaDot = effect("Gelûres","imeaDot", stat=MAGIE,emoji='<:icelame2:1156452836964569148>',power=35,turnInit=3,lvl=3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,stackable=True,dodge=-3,description="Le froid engourdit vos membres, vous infligeants des dégâts en début de tour et diminuant vos chances d'esquiver des attaques")
imeaWeap = weapon("Pic de glace","imeaWeap",RANGE_LONG,AREA_CIRCLE_5,magie=20,power=66,emoji='<:iceArrow:980172688284876830>',accuracy=60,effectOnUse=imeaDot,use=MAGIE, priority=WEAPON_PRIORITY_NONE)

imeaSkill1_3ne = effect("", "", turnInit=7, silent=True)
imeaSkill1_3 = skill("Giga Glace","imeaSkill1",TYPE_DAMAGE,power=140, effects=imeaDot, use=MAGIE, emoji='<:ice3:1335698092070011001>', condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER], description="Inflige des dégâts eau à l'ennemi ciblé", needEffect=imeaSkill1_3ne)

imeaSkill1_2ne = effect("", "", turnInit=7, silent=True)
imeaSkill1_2 = skill("Méga Glace","imeaSkill1", TYPE_DAMAGE, power=120, effects=imeaDot, effPowerPurcent=75, use=MAGIE, emoji='<:ice2:941494399337136208>', condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER], description="Inflige des dégâts eau à l'ennemi ciblé", needEffect=imeaSkill1_2ne, effectOnSelf=imeaSkill1_3ne)
imeaSkill1_3.effectOnSelf = imeaSkill1_2ne

imeaSkill1_1 = skill("Glace","imeaSkill1", TYPE_DAMAGE, power=100, effects=imeaDot, effPowerPurcent=50, use=MAGIE, emoji='<:ice:941494417926270987>', condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER], description="Inflige des dégâts eau à l'ennemi ciblé", rejectEffect=[imeaSkill1_3ne, imeaSkill1_2ne], effectOnSelf=imeaSkill1_2ne)
imeaSkill1 = skill("Maitrise glacière", "imeaSkill1", TYPE_DAMAGE, become=[imeaSkill1_1, imeaSkill1_2, imeaSkill1_3], emoji=imeaSkill1_3.emoji)

imeaSkill2e1 = effect("Lames de glace", "imeaSkill2", MAGIE, type=TYPE_DAMAGE, trigger=TRIGGER_INSTANT, power=20, emoji='<:imea2:1020057890209407088>', area=AREA_DONUT_2)
imeaSkill2e3 = copy.deepcopy(imeaDot)
imeaSkill2e3.power = 7.5
imeaSkill2e2 = effect("Lames de glace", "imeaSkill2", callOnTrigger=imeaSkill2e3, trigger=TRIGGER_INSTANT, emoji='<:imea2:1020057890209407088>', area=AREA_CIRCLE_2)
imeaSkill2 = skill("Lames de glace","imeaSkill2",TYPE_DAMAGE, power=40, repetition=4, cooldown=5, effects=[imeaSkill2e1, imeaSkill2e2], accuracy=500, use=MAGIE, emoji='<:imea2:1020057890209407088>', condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER], description="Inflige des dégâts à l'ennemi ciblé et ses alliés alentours tout en leur infligeant {0} avec une puissance réduite, à quatre reprises".format(imeaDot))

imeaSkill3e = effect("Permafrost", "imeaSkill3e", PURCENTAGE, resistance=-15, turnInit=imeaDot.turnInit)
imeaSkill3e2 = copy.deepcopy(defenseUp)
imeaSkill3e2.power, imeaSkill3e2.silentRemove = 25, True
imeaSkill3e3 = effect("Couronne de Glace", "imeaSkill3e3", MAGIE, type=TYPE_INDIRECT_DAMAGE, power=25, area=AREA_CIRCLE_1, trigger=TRIGGER_INSTANT, emoji='<:iceCrown:1335698110776873011>')
imeaSkill3e1 = effect("Couronne de Glace", "imeaSkill3e1", emoji='<:iceCrown:1335698110776873011>', lvl=10, callOnTrigger=imeaSkill3e3, trigger=TRIGGER_AFTER_DAMAGE, turnInit=3)
imeaSkill3 = skill("Tempête de neige","imeaSkill3", TYPE_INDIRECT_DAMAGE, cooldown=7, effects=[imeaDot, imeaSkill3e], area=AREA_CIRCLE_3, range=AREA_CIRCLE_3, emoji='<:iceCrown:1335698110776873011>', effectOnSelf=imeaSkill3e1, effectAroundCaster=[TYPE_BOOST, AREA_CIRCLE_5, imeaSkill3e2], condition=[EXCLUSIVE, ELEMENT, ELEMENT_WATER], description="Imea inflige {0} aux ennemis ciblés et réduit leur résistance durant un petit moment. De plus, elle réduit les dégâts qu'elle et ses alliés reçoivent et s'octroi {1}, infligeant des dégâts indirects en zone lorsqu'elle est subit des dégâts directs à l'attaquant".format(imeaDot, imeaSkill3e1))

imeaSkill4e = effect("Showgrave", "imeaSkill4e", MAGIE, power=150, area=AREA_DONUT_2, type=TYPE_DAMAGE, trigger=TRIGGER_INSTANT, emoji='<:iceAstral:1335698130158616626>')
imeaSkill4Lauch = skill("Snowgrave","imeaUlt",TYPE_DAMAGE, power=300, ultimate=True, cooldown=7, garCrit=True, use=MAGIE, effects=imeaSkill4e, emoji='<:iceAstral:1335698130158616626>',accuracy=200,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],url="https://media.discordapp.net/attachments/264128214593568768/1135671627267461160/20230731_223151.gif",description="Après un tour de chargement, Imea inflige de gros dégâts critiques à l'ennemi ciblé et des dégâts moindres aux ennemis autour")
imeaSkill4Cast = effect("Cast - {replicaName}","castSnowgrave",silent=True,turnInit=2,replique=imeaSkill4Lauch)
imeaSkill4 = copy.deepcopy(imeaSkill4Lauch)
imeaSkill4.power, imeaSkill4.effects, imeaSkill4.effectOnSelf, imeaSkill4.url = 0, [None], imeaSkill4Cast, None

imeaSkill5 = skill("Croix gelée","imeaSkill5",TYPE_DAMAGE,power=100,cooldown=7,area=AREA_INLINE_5,use=MAGIE,emoji='<:imea1:1020057856772419605>',effects=imeaDot,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],description="Inflige des dégâts aux ennemis ciblés en ligne droite ainsi que {0} {1} à la cible principale".format(imeaDot.emoji[0][0],imeaDot.name))

imeaSkill6Eff = effect("Voie Royale", "imeaSkill6eff", MAGIE, strength=7.5, magie=7.5, resistance=2.5, turnInit=3)
imeaSkill6 = skill("Commandement Royal", 'imeaSkill6', TYPE_BOOST, range=AREA_MONO, area=AREA_DONUT_5, effects=imeaSkill6Eff, cooldown=7, ultimate=True)

# BlackSlime
BLACKSLIME_DURING_PHY_FIGHT = 20

bSlimeWeap = weapon("Gelatine", "bSlimeWeap", RANGE_DIST, AREA_CIRCLE_3, 0, 0, endurance=40, priority=WEAPON_PRIORITY_NONE)
bSlimePassiveEff1 = effect("Gigantification", "bSlimePassiveEff1", PURCENTAGE, strength=35, magie=35, turnInit=-1, unclearable=True, hide=True, emoji='<:naciaGiantEff:1052323849288568975>')
bSlimePassiveEff2 = copy.deepcopy(constEff)
bSlimePassiveEff2.power, bSlimePassiveEff2.stat, bSlimePassiveEff2.turnInit, bSlimePassiveEff2.unclearable = 125, PURCENTAGE, -1, True
bSlimePassive = skill("Gigantification", "bSlimePassive", TYPE_PASSIVE, effects=[bSlimePassiveEff1, bSlimePassiveEff2], description="Augmente grandement la Force, Magie et les PV max du Slime Noir en début de combat")

bSlimeToxiBuff = effect("ToxiBuff", "bSlimeToxiBuff", turnInit=-1, unclearable=True, emoji='<:toxila:1177648787179712562>')
bSlimeToxiBuffPassive = skill("ToxiBuff", "bSlimeToxiBuffPassive", TYPE_PASSIVE, effects=bSlimeToxiBuff, description="Si le niveau du Slime Noir est suffisament élevé pour qu'il puisse avoir cette compétence, certaines de ses compétences sont renforcées")

bSlimeSkill1_2_2 = skill("Plongeon Toxique", "bSlimeSkill1", TYPE_DAMAGE, power=150, accuracy=150, range=AREA_CIRCLE_4, area=AREA_CIRCLE_2, areaOnSelf=True, tpCac=True, effectAroundCaster=[TYPE_INDIRECT_DAMAGE, AREA_CIRCLE_2, darkZenecaDot], effPowerPurcent=50, cooldown=5, description="Après un tour de chargement, le Slime Noire saute sur un ennemi, infligeant des dégâts de zone à l'atterrisage, ainsi que {0} avec une puissance réduite de 50%".format(darkZenecaDot))
bSlimeSkill1_2_2c = effect("Cast - {replicaName}", "bSlimeSkill1_2_2c", turnInit=2, replique=bSlimeSkill1_2_2, silent=True)
bSlimeSkill1_2_1 = skill(bSlimeSkill1_2_2.name, bSlimeSkill1_2_2.id, TYPE_DAMAGE, range=bSlimeSkill1_2_2.range, area=bSlimeSkill1_2_2.area, cooldown=bSlimeSkill1_2_2.cooldown, description=bSlimeSkill1_2_2.description, emoji=bSlimeSkill1_2_2.emoji, effectOnSelf=bSlimeSkill1_2_2c, needEffect=bSlimeToxiBuff)
bSlimeSkill1_1_2 = skill("Plongeon", "bSlimeSkill1", TYPE_DAMAGE, power=120, range=AREA_CIRCLE_4, area=AREA_CIRCLE_2, areaOnSelf=True, tpCac=True, cooldown=5, description="Après un tour de chargement, le Slime Noire saute sur un ennemi, infligeant des dégâts de zone à l'atterrisage".format(darkZenecaDot))
bSlimeSkill1_1_2c = effect("Cast - {replicaName}", "bSlimeSkill1_1_2c", turnInit=2, replique=bSlimeSkill1_1_2, silent=True)
bSlimeSkill1_1_1 = skill(bSlimeSkill1_1_2.name, bSlimeSkill1_1_2.id, TYPE_DAMAGE, range=bSlimeSkill1_1_2.range, area=bSlimeSkill1_1_2.area, cooldown=bSlimeSkill1_1_2.cooldown, description=bSlimeSkill1_1_2.description, emoji=bSlimeSkill1_1_2.emoji, effectOnSelf=bSlimeSkill1_1_2c, rejectEffect=bSlimeToxiBuff)
bSlimeSkill1 = skill("Plongeon", "bSlimeSkill1", TYPE_DAMAGE, become=[bSlimeSkill1_1_1, bSlimeSkill1_2_1], emoji=bSlimeSkill1_1_1.emoji, description="Après un tour de chargement, le Slime Noir saute sur un ennemi, infligeant des dégâts à l'atterrisage. Si son niveau est assez élevé, l'attaque inflige plus de dégâts ainsi que l'effet {0} avec une puissance réduite".format(darkZenecaDot))

bSlimeSkill2_2_e0 = copy.deepcopy(darkZenecaDot)
bSlimeSkill2_2_e0.power, bSlimeSkill2_2_e0.name = bSlimeSkill2_2_e0.power * 0.3, bSlimeSkill2_2_e0.name + " (30%)"
bSlimeSkill2_e = effect("Redirection", "bSlimeSkill2_e", None, redirection=50, trigger=TRIGGER_DAMAGE)
bSlimeSkill2_2_e1 = effect("Pointes de Poisons", "bSlimeSkill2_2_e1", None, thornEff=True, callOnTrigger=bSlimeSkill2_2_e0, trigger=TRIGGER_AFTER_DAMAGE, lvl=10, aggro=20)
bSlimeSkill2_2 = skill("Redirection Toxique", "bSlimeSkill2", TYPE_BOOST, effects=[bSlimeSkill2_e], range=AREA_MONO, area=AREA_DONUT_3, cooldown=3, effectOnSelf=bSlimeSkill2_2_e1, description="Le Slime Noir redirige sur lui {0}% des dégâts subits par ses alliés".format(bSlimeSkill2_e.redirection), needEffect=bSlimeToxiBuff)
bSlimeSkill2_1 = copy.deepcopy(bSlimeSkill2_2)
bSlimeSkill2_1.effectOnSelf, bSlimeSkill2_1.needEffect, bSlimeSkill2_1.rejectEffect, bSlimeSkill2_1.name = None, None, [bSlimeToxiBuff], bSlimeSkill2_1.name.replace(" Toxique", "")
bSlimeSkill2_2.description += " De plus, lorsqu'il reçoit des dégâts directs, le Slime Noir inflige {0} à l'attaquant".format(bSlimeSkill2_2_e0)
bSlimeSkill2 = skill(bSlimeSkill2_1.name, bSlimeSkill2_1.id, TYPE_BOOST, become=[bSlimeSkill2_1, bSlimeSkill2_2], emoji=bSlimeSkill2_1.emoji, description=bSlimeSkill2_1.description + " Si le Slime Noir est renforcé, il inflige un effet de poison à l'attaquant lorsqu'il reçoit des dégâts directs")

bSlimeSkill3_2 = skill("Miriade Toxique", "bSlimeSkill3", TYPE_DAMAGE, power=40, repetition=3, area=AREA_RANDOMENNEMI_3, effects=darkZenecaDot, use=MAGIE, effPowerPurcent=35, needEffect=bSlimeToxiBuff, cooldown=3, description="Le Slime Noir inflige des dégâts à plusieurs ennemis aléatoirement, ainsi que {0} avec une puissance réduite, à plusieurs reprises".format(darkZenecaDot))
bSlimeSkill3_1 = skill("Miriade", "bSlimeSkill3", TYPE_DAMAGE, power=35, repetition=3, area=AREA_RANDOMENNEMI_3, use=MAGIE, rejectEffect=bSlimeSkill3_2.needEffect, cooldown=3, description="Le Slime Noir inflige des dégâts à plusieurs ennemis aléatoirement, à plusieurs reprises")
bSlimeSkill3 = skill("Miriade", "bSlimeSkill3", TYPE_DAMAGE, become=[bSlimeSkill3_1, bSlimeSkill3_2], emoji=bSlimeSkill3_1.emoji, description=bSlimeSkill3_1.description)

bSlimeSkill4_2e = effect("Mortier Toxique", "bSlimeSkill4_2e", callOnTrigger=bSlimeSkill2_2_e0, area=AREA_CIRCLE_1, trigger=TRIGGER_INSTANT)
bSlimeSkill4_2 = skill("Mortier Toxique", "bSlimeSkill4", TYPE_DAMAGE, power=100, use=MAGIE, range=AREA_BOMB_6, area=AREA_CIRCLE_1, cooldown=3, effects=bSlimeSkill4_2e, needEffect=bSlimeToxiBuff)
bSlimeSkill4_1 = skill("Mortier", "bSlimeSkill4", TYPE_DAMAGE, power=80, use=MAGIE, range=AREA_BOMB_6, area=AREA_CIRCLE_1, cooldown=3, rejectEffect=bSlimeToxiBuff)
bSlimeSkill4 = skill("Mortier", "bSlimeSkill4", TYPE_DAMAGE, become=[bSlimeSkill4_1, bSlimeSkill4_2])