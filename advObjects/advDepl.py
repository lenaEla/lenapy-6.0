from classes import *
from constantes import *

bigBubbleShield = effect("Armure","bigBubbleArmor", stat=INTELLIGENCE,overhealth=35,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,stackable=True)
bigBubbleSkill = skill("Bulle protectrice","bigBubbleSkill",TYPE_ARMOR,effects=bigBubbleShield,area=AREA_CIRCLE_2,range=AREA_MONO,use=INTELLIGENCE)
bigBubbleDepl = depl("Super-Bouclier",bigBubbleSkill,["<:bbb:1013740673985413130>","<:bbr:1013740701260972092>"],["<:tbbb:1013740728146460733>","<:tbbr:1013740755375902740>"],"Une bulle protectrice qui donnera de l'armure aux alliés à l'intérieur (Puissance de l'Armure : **{0}**)".format(bigBubbleShield.overhealth))

sonarPafEff = effect("Marqué","sonarPafMark",dodge=-15,description="Réduit la probabilité d'esquiver une attaque",turnInit=1,type=TYPE_MALUS,emoji='<:sonar:1013742380026953758>')
sonarPafSkill = skill("Sonar Paf","sonarPafSkill",TYPE_DAMAGE,power=35,use=INTELLIGENCE,range=AREA_MONO,area=AREA_CIRCLE_3,effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_3,sonarPafEff])
sonarPafDepl = depl("Sonar Paf",sonarPafSkill,["<:spb:1013743128253042699>","<:spr:1013743154048020561>"],["<:tspb:1013743190051930232>","<:tspr:1013743218975842334>"],description="Un dispositif qui inflige des dégâts aux ennemis autour de lui (Puissance : **{1}**) et reduit leur chance d'esquiver les attaques de **{0}%**".format(sonarPafSkill.effectAroundCaster[2].dodge,sonarPafSkill.power))

asileSkillEff = copy.deepcopy(absEff)
asileSkillEff.power = 10
asileSkill = skill("Asile","asileSkill",TYPE_HEAL,power=35,effects=asileSkillEff,range=AREA_MONO,area=AREA_CIRCLE_2,use=CHARISMA,effBeforePow=True)
asileDepl = depl("Asile",asileSkill,["<:asileB:1013751801742372947>","<:asileR:1013751836412489820>"],["<:tasileB:1013751863386046556>","<:tasileR:1013751895938048060>"],"Place une zone sur une cellule qui augmentera les soins reçus par les alliés de **{0}%** et les soigneras (Puissance : **{1}**)".format(asileSkillEff.power,asileSkill.power))

liaTornadeSkill = skill("Tatsumaki","liaTornadeSkill",TYPE_DAMAGE,power=60,range=AREA_MONO,area=AREA_CIRCLE_2,use=MAGIE,effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_3,30])
liaTornade = depl("Tatsumaki",liaTornadeSkill,["<:liaDepl:1013912739728592896>","<:liaDepl:1013912739728592896>"],["<:tliaDepl:1013912690877550664>","<:tliaDepl:1013912690877550664>"],"Lia invoque une tornade sur la cellule ciblée, infligeant des dégâts avec une puissance de **{0}** et soigne la kitsune si celle-ci se trouve à l'intérieur avec une puissance de **{1}**".format(liaTornadeSkill.power,liaTornadeSkill.effectAroundCaster[2]))

lohicaDeplSkill = skill("Brouillard Empoisonné","lohicaDeplSkill",TYPE_INDIRECT_DAMAGE,range=AREA_MONO,area=AREA_CIRCLE_2,effects="me",effPowerPurcent=70,emoji="<:poisonusMist:1059084936100970556>",use=MAGIE)
lohicaDepl = depl("Brouillard Empoisonné",lohicaDeplSkill,["<:mistB:1059086795603709972>","<:mistR:1059086825077100545>"],["<:mistRB:1059086885361823794>","<:mistRT:1059086850154844220>"],"Inflige {0} __{1}__ aux ennemis à l'intérieur du brouillard avec une puissance équivalante de **{2}%**".format("<:est:884223390804766740>","Poison d'Estialba",lohicaDeplSkill.effPowerPurcent))

lacerTrapSkill = skill("Piège de Lacération","laserTrapSKill",TYPE_DAMAGE,power=25,range=AREA_MONO,area=AREA_CIRCLE_2,setAoEDamage=True,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_CIRCLE_2,"mx"],effPowerPurcent=50)
lacerTrapDepl = depl("Piège de Lacération",lacerTrapSkill,["<:sheDepl:1014080464924983356>","<:sheDepl:1014080464924983356>"],["<:tsheDeplB:1014080494259945503>","<:tsheDeplR:1014080520386252851>"],description="Inflige des dégâts aux ennemis dans la zone d'effet (Puissance : **{0}**) et leur inflige {1} __{2}__ avec **{3}%** de sa puissance".format(lacerTrapSkill.power,"<:bleeding:1133258052225745048>","Hémorragie",lacerTrapSkill.effPowerPurcent))

dogmeEff = copy.deepcopy(defenseUp)
dogmeEff.power, dogmeEff.stat = 4, INTELLIGENCE
dogmeSkill = skill("Dogme de Survie","SacredSoilSkill",TYPE_BOOST,effects=dogmeEff,range=AREA_MONO,area=AREA_CIRCLE_2,effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_2,25])
dogmeDepl = depl("Dogme de survie",dogmeSkill,["<:ssb:1014093418600861767>","<:ssr:1014093444727193612>"], ["<:tssb:1014093472363462676>","<:tssr:1014093498116489216>"],description="Applique une zone sur la cellule ciblée qui réduit les dégâts subis par les alliés à l'intérieur (Puissance : **{0}%** non fixe) et les soignes légèrement (Puissance : **{1}**)".format(dogmeEff.power,dogmeSkill.effectAroundCaster[2]))

glyphidPretorianAcidEff = effect("Acide Prétorien","pretorianGlyphid", stat=STRENGTH,power=50,turnInit=3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,stackable=True,emoji='<:acideCloud:1055002950788988939>')
glypdDeatCloudSkill = skill("Nuage Corrosif","glyphidDeathCloud",TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_2,effects=glyphidPretorianAcidEff,range=AREA_MONO,emoji=glyphidPretorianAcidEff .emoji[0][0])
glyphidDeathCould = depl("Nuage Corrosif",glypdDeatCloudSkill,[glyphidPretorianAcidEff.emoji[0][0],glyphidPretorianAcidEff.emoji[0][1]],["<:acideCloudR:1055002928647249930>","<:acideCloudR:1055002928647249930>"],"Un nuage corrosif laissé après la mort d'un Prétorien Glyphique")

corruptusAreaEff1, corruptusAreaEff2 = copy.deepcopy(incur[3]), copy.deepcopy(vulne)
corruptusAreaEff2.power, corruptusAreaEff2.stat = 4, INTELLIGENCE
corruptusAreaSkill = skill("Zone Corrompue","corruptusArea",TYPE_MALUS,0,range=AREA_MONO,area=AREA_CIRCLE_2,effects=[corruptusAreaEff2,corruptusAreaEff1],emoji='<:fa:1014081850257444874>')
corruptusAreaDepl = depl("Zone Corrompue",corruptusAreaSkill,["<:fa:1014081850257444874>","<:fa:1014081850257444874>"],["<:tfaB:1014081879638556675>","<:tfaR:1014081919463464970>"],description="Une zone étrange qui augmente les dégâts subis par les ennemis à l'intérieur et réduit les soins qu'ils reçoivent")

snowFallGlypheEff = effect("Avalanche","snowFallGlyphe", stat=INTELLIGENCE,resistance=3)
snowFallGlypheSkill = skill("Glyphe Avalanche","snowfallGlypheSkill",TYPE_DAMAGE,power=35,range=AREA_MONO,area=AREA_CIRCLE_2,use=INTELLIGENCE,emoji='<:imea1:1020057856772419605>',condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_2,snowFallGlypheEff])
snowFallGlypheDepl = depl("Glyphe Avalanche",snowFallGlypheSkill,["<:snowfall:1116430780445495497>","<:snowfall:1116430780445495497>"],description="Un glyphe qui inflige des dégâts ({0}) aux ennemis et augmente la résistance ({1}) des alliés".format(statsEmojis[snowFallGlypheSkill.use],statsEmojis[snowFallGlypheEff.stat]))

holyGroundIEff1 = copy.deepcopy(defenseUp)
holyGroundIEff1.power, holyGroundIEff1.stat, holyGroundIEff1.turnInit = 5, INTELLIGENCE, 1
holyGroundIEff2 = copy.deepcopy(dmgUp)
holyGroundIEff2.power, holyGroundIEff2.stat, holyGroundIEff2.turnInit = 3.5, INTELLIGENCE, 1
holyGroundISkill = skill("Terre Sacrée","holyGround1Skill",TYPE_BOOST,area=AREA_CIRCLE_2,range=AREA_MONO,effects=[holyGroundIEff1,holyGroundIEff2],emoji='<:dvinShield:1104496800100003860>')
holyGroundI = depl("Terre Sacrée",holyGroundISkill,"<:holyGroundI:950254446611431455>",description="Réduit les dégâts subis et augmente les dégâts infligés par les alliés dans la zone d'effet durant 3 tours")

holyGroundIIEff = effect("Terre Bénie","hollyGroundIIEff",stat=CHARISMA,charisma=5,intelligence=5,precision=3,agility=3,strength=5,magie=5,turnInit=1,emoji='<:holyGroundII:950254462449115136>')
holyGroundIISkill = skill("Terre Bénie","sacredGroundSkill",TYPE_BOOST,effects=[holyGroundIIEff],range=AREA_MONO,area=AREA_CIRCLE_2,effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_2,35],use=CHARISMA,emoji='<:dvinRegen:1104496736845713440>')
holyGroundII = depl("Terre Bénie",holyGroundIISkill,"<:holyGroundII:950254462449115136>",description="Augmente les statistiques des alliés dans la zone d'effet et les soigne durant 3 tours")

dmonGroundEff = copy.deepcopy(dmgUp)
dmonGroundEff.power, dmonGroundEff.stat, dmonGroundEff.turnInit = 5, INTELLIGENCE, 1
dmonGroundEff2 = copy.deepcopy(holyGroundIIEff)
dmonGroundEff2.name, dmonGroundEff2.emoji, dmonGroundEff2.stat = "Terre Démoniaque", uniqueEmoji("<:burningGround:950256060923535370>"), INTELLIGENCE
dmonGroundSkill = skill("Terre Démoniaque","dmonGroundSKill",TYPE_BOOST,range=AREA_MONO,area=AREA_CIRCLE_2,effects=[dmonGroundEff,dmonGroundEff2],emoji='<:dmonland:1006455391342829599>')
dmonGround = depl("Terre Démoniaque",dmonGroundSkill,"<:burningGround:950256060923535370>",description="Augmente les dégâts infligés et les statistiques des alliés dans la zone d'effet durant 3 tours")