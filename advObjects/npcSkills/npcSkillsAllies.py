from advObjects.npcSkills.npcSkillsImports import *
from advObjects.npcSkills.npcSkills_ennemi import lioLB
from advObjects.npcSkills.npcSkills_boss import *

# Clem Ex.
clemBleeding = copy.deepcopy(bleeding)
clemBleeding.power, clemBleeding.stat, clemBleeding.name, clemBleeding.lifeSteal = 5, MAGIE, "Sanguisugae", 35
clemExSkill21Lauch = skill("Sanguinis Explosio", "clemExSkill2Launch", TYPE_DAMAGE, 0,accuracy=150,ultimate=True, emoji='<:clemBoom:978377130750644224>', initCooldown=2, power=750,area=AREA_CIRCLE_2, use=MAGIE, cooldown=6, description="Déclanche une explosion infligeant de lourds dégâts dans une large zone", say=["Voyons faire si quelqu'un résistera à ça.","J'espère que vous avez une bonne assurance vie.","J'espère que vous avez eu la bonne idée de rédiger votre testamant avant de venir me faire chier"])
clemExSkill21CastEff = effect("Cast - Sanguinis Explosio", "clemExSkill2CastEff",replique=clemExSkill21Lauch, silent=True, turnInit=2)
clemExSkill22Lauch = skill("Sanguinis Ray",clemExSkill21Lauch.id,TYPE_DAMAGE,accuracy=250,power=1250,ultimate=True,emoji='<:clemRay:978376646262403144>',area=AREA_INLINE_5,initCooldown=clemExSkill21Lauch.initCooldown,cooldown=clemExSkill21Lauch.cooldown,use=MAGIE,description="Tir un grand rayon d'énergie à vos points caridaux, infligeant d'extrèmes dégâts à tous les ennemis alignés\nNe peux pas être esquivé et ignore **35%** de la résistance ennemie",percing=35,say=["J'espère que vous avez une bonne assurance vie !","Faisons un peu le ménage, voulez-vous ?","Je vais mettre une croix sur vos projets d'avenirs."])
clemExSkill22Cast = effect("Cast - {0}".format(clemExSkill22Lauch.name),"clemRayonSanguinCastEff",silent=True,turnInit=2,replique=clemExSkill22Lauch)
clemExSkill22 = copy.deepcopy(clemExSkill22Lauch)
clemExSkill22.power, clemExSkill22.effectOnSelf = 0, clemExSkill22Cast
clemExSkill21 = copy.deepcopy(clemExSkill21Lauch)
clemExSkill21.power, clemExSkill21.effectOnSelf = 0, clemExSkill21CastEff
clemExSkill2 = skill('Sanguis Bang',clemExSkill21.id,TYPE_DAMAGE,cooldown=clemExSkill21.cooldown,ultimate=True,use=MAGIE,become=[clemExSkill21,clemExSkill22],area=AREA_CIRCLE_2,emoji='<:clemCast:978376938286641172>')
clemExSkill31 = skill("Sanguis Hastis", "clemExSkill3", TYPE_DAMAGE, 0, accuracy=125, power=250, range=AREA_DIST_7, use=MAGIE,area=AREA_CIRCLE_1, cooldown=3, emoji='<:clemExSkill:1015209835001815091>', description="Inflige de lourd dégâts à l'ennemi éloignés ciblé et ses alliés alentours",say=["C'est pas parceque vous êtes loin que vous aurez plus de chances de survie","Vous comptiez pas rester là bas à regarder vos camarades se faire écraser, si ?","J'ose espérer que vous ne pensiez pas que je vous avais oublié ?"])
clemExSkill32 = skill("Hastae Noctis", "clemExSkill3", TYPE_DAMAGE, 0,accuracy=250, power=350,use=MAGIE, cooldown=3, emoji='<:clemExSkill:1015209812407111770>', description="Inflige de lourd dégâts monocibles et vous soigne d'une partie des dégâts infligés",lifeSteal=35,say=["Tu penses que tu va pouvoir tenir combien de temps comme ça ?","Tu t'es pris pour qui ?"])
clemExSkill3 = skill("Sanguis Hastis/Hastae Noctis","clemExSkill3",TYPE_DAMAGE,become=[clemExSkill31,clemExSkill32],cooldown=clemExSkill32.cooldown,use=MAGIE, emoji='<:clemExSkill:1015209835001815091>')
clemExSkill5 = skill("Saturi Cum Sanguine", "clemExSkill5", TYPE_DAMAGE, 0 ,accuracy=150, power=250, emoji='<:clemExSkill:1015209760062189628>', range=AREA_MONO,area=AREA_CIRCLE_2, use=MAGIE, cooldown=5, description="Inflige de lourd aux ennemis alentours",say=["C'est bien, vous me faites le plaisir de venir mourir de vous-même","Vous n'êtes pas les premiers et vous serez clairement pas les derniers."])
clemExSkill6 = skill("Sanguis Pluvia", "clemExSkill6", TYPE_DAMAGE, emoji='<:clemExSkill:1015209784800198728>', power=50,accuracy=200, range=AREA_MONO, area=AREA_ALL_ENEMIES, initCooldown=2, use=MAGIE,cooldown=5, setAoEDamage=True, replay=True, description="Inflige des dégâts à tous les ennemis en volant une partie des dégâts infligés, tout en leur infligeant un effet de dégâts indirects sur la durée",lifeSteal=35,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_ALL_ENEMIES,clemBleeding],say=["Vous suffirez à peine à combler ma soif pour 3 minutes...","J'utilise trop de sang pour vous..."])

CLEMCOMB6POWER, CLEMCOMB5POWER, CLEMCOMB4POWER, CLEMCOMB3POWER, CLEMCOMB2POWER, CLEMCOMB1POWER = 750,100,400,350,300,100

clemExSkill41 = skill("Résolution Sanglante","clemExSkill4",TYPE_DAMAGE,power=CLEMCOMB6POWER,accuracy=200,cooldown=5,range=AREA_INLINE_5,emoji='<:resolution:978398280943804436>',area=AREA_LINE_5,description="Effectue une succession d'attaque contre un ennemi. Le dernier coup du combo inflige des dégâts en ligne",use=MAGIE,say="Prêt pour le final ?")
clemExSkill41Cast = effect("Résolution préparée","clemExSkill41Cast",silent=True,replique=clemExSkill41)
clemExSkill42 = skill("Déplacement Sanglant","clemExSkill4",TYPE_DAMAGE,accuracy=200,power=CLEMCOMB5POWER,jumpBack=1,effectOnSelf=clemExSkill41Cast,emoji='<:dep:932765889017839636>',range=AREA_CIRCLE_1,replay=True,use=MAGIE,tpCac=True)
clemExSkill42Cast = effect("Déplacement préparé","clemExSkill42Cast",silent=True,replique=clemExSkill42)
clemExSkill43 = skill("Redoublement Sanglant","clemExSkill4",TYPE_DAMAGE,accuracy=200,power=CLEMCOMB4POWER,effectOnSelf=clemExSkill42Cast,emoji='<:combo3:978398179999514624>',range=AREA_CIRCLE_1,replay=True,use=MAGIE,tpCac=True)
clemExSkill43Cast = effect("Redoublement préparé","clemExSkill43Cast",silent=True,replique=clemExSkill43)
clemExSkill44 = skill("Zwerchhau Sanglant","clemExSkill4",TYPE_DAMAGE,accuracy=200,power=CLEMCOMB3POWER,effectOnSelf=clemExSkill43Cast,emoji='<:combo2:978398160454045738>',range=AREA_CIRCLE_1,replay=True,use=MAGIE,tpCac=True)
clemExSkill44Cast = effect("Zwerchhau préparé","clemExSkill44Cast",silent=True,replique=clemExSkill44)
clemExSkill45 = skill("Riposte Sanglante","clemExSkill4",TYPE_DAMAGE,accuracy=200,power=CLEMCOMB2POWER,effectOnSelf=clemExSkill44Cast,emoji='<:combo1:978398142967992330>',range=AREA_CIRCLE_1,replay=True,use=MAGIE,tpCac=True)
clemExSkill45Cast = effect("Riposte préparée","clemExSkill45Cast",silent=True,replique=clemExSkill45)
clemExSkill4 = skill("Corps à Corps Sanglant","clemExSkill4",TYPE_DAMAGE,accuracy=200,power=CLEMCOMB1POWER,effectOnSelf=clemExSkill45Cast,replay=True,range=AREA_INLINE_5,emoji='<:cac:932765903102291999>',tpCac=True,description="Effectue une succession d'attaque contre un ennemi. Le dernier coup du combo inflige des dégâts en ligne",use=MAGIE)

clemExBloodJauge = copy.deepcopy(bloodJauge)
clemExBloodJauge.jaugeValue.conds = [
    jaugeConds(INC_START_FIGHT,50),
    jaugeConds(INC_DEAL_DAMAGE,10/100)
]

CLEMEXBLOODDEMONMAGIE, CLEMEXSCAR = 50, 10
clemExBloodDemonEff = effect("Sanguis Daemonis Exaltatus","bloodDemonEx",stat=PURCENTAGE,magie=CLEMEXBLOODDEMONMAGIE,turnInit=4,description="Augmente de **{0}%** votre magie et rend toutes vos compétences instantanée".format(CLEMEXBLOODDEMONMAGIE),emoji='<:sanguisDaemonium:1050059965630533714>')
clemExBloodDemonEff2Trig = effect("Crepitus Sanguinis Moratus","bloodDemonEx2_c", stat=MAGIE,power=80,area=AREA_CIRCLE_1,trigger=TRIGGER_INSTANT,type=TYPE_INDIRECT_DAMAGE,emoji=dislocation.emoji,lifeSteal=35)
clemExBloodDemonEff2 = effect("Crepitus Sanguinis Moratus","bloodDemonEx2",type=TYPE_BOOST,turnInit=4,lvl=99,trigger=TRIGGER_DEALS_DAMAGE,description="Lorsque vous utilisez une compétence, inflige des dégâts indirects de zone centré sur la cible principale",emoji='<:dislocation:1052697663402950667>',callOnTrigger=clemExBloodDemonEff2Trig,onDeclancher=True)
clemExBloodDemonEff3 = effect("Cicatrice Alpha","clemExBloodDemonEff3", stat=PURCENTAGE,power=CLEMEXSCAR,turnInit=4,lvl=4,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,description="Une ancienne citratrice magique réveillée par votre afflue de puissance vous inflige des dégâts à la fin de votre tour",emoji='<:griphAlpha:1064270537037197416>')
clemExBloodDemon = skill("Sanguis Daemonis Exaltatus","clemExBloodDemon",TYPE_DAMAGE,power=100,range=AREA_MONO,area=AREA_DONUT_3,effects=[clemExBloodDemonEff,clemExBloodDemonEff2,clemExBloodDemonEff3],cooldown=7,jaugeEff=clemExBloodJauge,minJaugeValue=100,description="Vous infligez des dégâts autour de vous déchénant toute votre puissance !\nAugmente votre Magie, rend toutes vos compétences instantannée, inflige des dégâts indirects supplémentaire en attaquant, mais vous subissez des dégâts continues, le tout durant quatres tours",emoji="<:sanguisDaemonium:1050059965630533714>")

clemExSay = says(
    start="Pff, vous tenez tant que ça à être au milieu de ma route ?",
    onKill="Tss, même pas le temps de faire une pause pour manger...",
    blueWinAlive="Quel résultat surprenant"
)

clemExWeapon = copy.deepcopy(rapiere)
clemExWeapon.power, clemExWeapon.range, clemExWeapon.effectOnUse, clemExWeapon.name, clemExWeapon.priority = 200, RANGE_MELEE, clemBleeding, "Flos Argenteus", WEAPON_PRIORITY_LOWEST
miniStuff = stuff("Rune adaptative", 'clemRune', 0, 0, endurance=50, charisma=0, agility=50//2,precision=int(50*0.3), intelligence=50//10, magie=50*2, resistance=min(50//5, 35), emoji=clemEarRings.emoji)

# Iliana prêtresse
miniStuffHead = stuff("Casque de la neko de la lueur ultime", 'ilianaPreHead', 0, 0, endurance=int(50*1.35), agility=int(50*0.3), precision=int(50*0.3), charisma=50, magie=50, resistance=min(50//5, 50), percing=10, emoji=zenithHat.emoji)
miniStuffDress = stuff("Armure de la neko de la lueur ultime", 'ilianaPreArmor', 1, 0, endurance=int(50*1.85), agility=int(50*0.3), precision=int(50*0.5), charisma=50, magie=50, percing=15, resistance=min(50//5, 50), emoji=zenithArmor.emoji)
miniStuffFlats = stuff("Sorolets de la neko de la lueur ultime", 'ilianaPreBoots', 2, 0, endurance=int(50*1.35), agility=int(50*0.3), precision=int(50*0.3), charisma=50, magie=50, resistance=min(50//5, 50), percing=10, emoji=zenithBoots.emoji)

iliPrePoi = effect("Lumière Absolue", "ilianaIndirect", CHARISMA, power=20,type=TYPE_INDIRECT_DAMAGE, trigger=TRIGGER_START_OF_TURN, turnInit=3, lvl=3, emoji='<:iliDot:1046387034522136609>')
iliPreRegen = effect("Régénération de Lumière", "ilianaRegen", CHARISMA, power=50, trigger=TRIGGER_START_OF_TURN, type=TYPE_INDIRECT_HEAL,emoji='<a:ilianaRegen:969825374093578260>', turnInit=5, stackable=True, description="Soigne le porteur de l'effet au début de son tour")
iliPreSkill1 = skill("Lumière Tranchante", 'iliSkill1', TYPE_DAMAGE, range=AREA_MONO, area=AREA_CIRCLE_3, power=200, use=CHARISMA, cooldown=5, effectOnSelf = iliPreRegen, description='Inflige des dégâts aux ennemis alentours et vous procure un effet régénérant', emoji='<:iliBravor:1046381213910302834>',selfEffPurcent = 80)
iliPreSkill2Heal = skill('Régénération', "iliSkill2", TYPE_HEAL, power=200, range=AREA_CIRCLE_7, effects=iliPreRegen, cooldown=3, description="Soigne l'allié ciblé et lui procure un effet de régénération sur la durée", use=CHARISMA, emoji='<a:ilianaRegen:969825374093578260>')
iliPreSkill2DmgEff = copy.deepcopy(vulne)
iliPreSkill2DmgEff.power = 35
iliPreSkill2Dmg = skill("Fracturation","iliSkill2",TYPE_DAMAGE, power=125,repetition=3,tpCac=True,effects=[iliPreSkill2DmgEff],effBeforePow=True,cooldown=3,use=CHARISMA,description="Augmente les dégâts subis par la cible de **35%** et lui inflige des dégâts à trois reprises",emoji='<:fragmentation:1117375884446412872>')
iliPreSkill2 = skill("Pouvoir de la lumière","iliSkill2",TYPE_HEAL,cooldown=3,become=[iliPreSkill2Heal,iliPreSkill2Dmg], emoji='<:lightHealShield:929322808654323733>')

iliPreSkill3_1_e = copy.deepcopy(defenseUp)
iliPreSkill3_1_e.power = 20
iliPreSkill3_1 = skill("Champ lumineux", 'iliSkill3', TYPE_INDIRECT_DAMAGE, effects=iliPrePoi, range=AREA_MONO, area=AREA_CIRCLE_3, use=CHARISMA, cooldown=3, effectOnSelf=iliPreSkill3_1_e, description='Inflige des dégâts aux ennemis alentours, vous soigne légèrement puis inflige un effet de dégâts indirect aux ennemis alentours tout en réduisant vos dégâts subis de **20%** durant un tour', emoji='<:iliLightField:1046381182767603752>',effectAroundCaster=[TYPE_DAMAGE,AREA_CIRCLE_2,50])
iliPreSkill3_c = effect("Enchaînement - {replicaName}","iliSkill3Cast",replique=iliPreSkill3_1,silent=True)
iliPreSkill3 = skill("Tourbillon de Lumière", "iliSkill3", TYPE_DAMAGE, power=175, range=AREA_MONO,area=AREA_CIRCLE_3, use=CHARISMA, replay=True, description="Inflige des dégâts aux ennemis alentours, vous soigne légèrement puis inflige un effet de dégâts indirect aux ennemis alentours tout en réduisant vos dégâts subis de **20%** durant un tour", emoji='<:revolLum:1033720380281597983>', effectOnSelf=iliPreSkill3_c)

iliPreDmgReduc = copy.deepcopy(defenseUp)
iliPreDmgReduc.power = 50
iliPreSkill4 = skill("Lumière Eternelle","iliLb",TYPE_DAMAGE,power=250,area=AREA_ALL_ENEMIES,range=AREA_MONO,emoji="<:eternalLight:1116761926052089856>",ultimate=True,effectAroundCaster=[TYPE_BOOST,AREA_ALL_ALLIES,iliPreDmgReduc],cooldown=10, description='Inflige des dégârs à tous les ennemis et réduit de **50%** les dégâts subis par tous les alliés',use=CHARISMA)

iliStans1_2 = effect("Couverture Lumineuse","ilianaStans1_1",emoji='<:cover:1061384419212005417>',redirection=20,silent=True)
iliStans1_1 = effect("Voeu de la Protectrice", "ilianaStans2", charisma=30, resistance=20, aggro=100, turnInit=-1, unclearable=True, emoji='<:iliShieldStans:1072554524260188285>',power=25, trigger=TRIGGER_END_OF_TURN, area=AREA_DONUT_2, callOnTrigger=iliStans1_2, description="Augmente grandement l'Agression, le Charsime et la Résistance d'Iliana, réduit de **{0}%** les dégâts qu'elle subit et, à la fin de son tour, octroie un effet redirigeant **20%** des dégâts subis aux alliés en mêlée d'elle")
iliStans1 = skill("Voeu de la Protectrice", "ilianaSkill5_1",TYPE_PASSIVE, effects=iliStans1_1, emoji=iliStans1_1.emoji[0][0],description=iliStans1_1.description.format(iliStans1_1.power))

iliStans2_1 = effect("Voeu de la Prêtresse","ilianaStans2", turnInit=-1, unclearable=True, emoji='<:iliDptStans:1072558143772561418>',stat=CHARISMA,power=50,description="Augmente de de **{0}%** les dégâts infligés par Iliana. De plus, après chaque utilisation d'une compétence offensive ou de son arme, elle se soigne avec une puissance de **62**. Ces effets sont doublés si Iliana affronte seule les Informités")
iliStans2 = skill("Conviction de la Prêtresse", "ilianaSkill5_2",TYPE_PASSIVE, effects=iliStans2_1, emoji=iliStans2_1.emoji[0][0],description=iliStans2_1.description.format(iliStans2_1.power))

iliStans1.description += "\n\nSi Iliana est seule, cette compétence est remplacée par {0} __{1}__".format(iliStans2.emoji,iliStans2.name)
iliStans2.description += "\n\nSi Iliana combat aux côtés de Luna, cette compétence est remplacée par {0} __{1}__".format(iliStans1.emoji,iliStans1.name)

iliPreSkill5 = skill("Conviction de la Lumière","iliaSkill5",TYPE_BOOST,become=[iliStans1,iliStans2],emoji='<:ilianaStans:969819202032664596>',description='Suivant si Iliana se bat seule ou aux côtés de Luna, lui confère un effet passif augmentant ses capacités offensives ou défensives\n\n{0} __{1} :__\n{2}\n\n{3} __{4} :__\n{5}'.format(iliStans1.emoji,iliStans1.name,iliStans1.description,iliStans2.emoji,iliStans2.name,iliStans2.description))

iliPreSkill6 = skill("Vitesse Lumière", "iliSkill6", TYPE_DAMAGE, power=50, range=AREA_INLINE_4, replay=True, cooldown=2, tpCac=True,use=CHARISMA, description='Vous téléporte au corps à corps de l\'ennemi ciblé et vous permet de rejouer votre tour', emoji='<:iliLightSpeed:1046384202792308797>')

iliPreSkill7Dmg = skill("Rayon de Lumière", "iliPreSkill7", TYPE_DAMAGE, power=150, range=AREA_CIRCLE_3, area=AREA_LINE_6, cooldown=4, use=CHARISMA, description="Inflige des dégâts sur une ligne droite devant vous",emoji='<:lightArrow:980172606143606834>')
iliPreSkill7RedirectEff = effect("Diffraction","iliRedirect",redirection=100,emoji='<:cover:1061384419212005417>')
iliPreSkill7Redirect = skill('Diffraction',"iliPreSkill7",TYPE_BOOST,effects=iliPreSkill7RedirectEff,range=AREA_DONUT_7,effectOnSelf=iliPreRegen,cooldown=iliPreSkill7Dmg.cooldown,description="Redirige **{0}%** des dégâts subis par l'allié ciblé sur vous jusqu'à votre prochain tour et vous octroie un effet régénérant".format(iliPreSkill7RedirectEff.redirection),emoji='<:gardian:1061384121198317629>')
iliPreSkill7 = skill("Jeu de lumière",'iliPreSkill7',TYPE_DAMAGE,become=[iliPreSkill7Dmg,iliPreSkill7Redirect],cooldown=4, emoji='<:catLight:956599774461722655>',description='{0} __{1} :__\n{2}\n\n{3} __{4} :__\n{5}'.format(iliPreSkill7Dmg.emoji,iliPreSkill7Dmg.name,iliPreSkill7Dmg.description,iliPreSkill7Redirect.emoji,iliPreSkill7Redirect.name,iliPreSkill7Redirect.description))

iliWeap = weapon("Epée et Bouclier de la Lumière", "iliWeap", RANGE_MELEE, AREA_CIRCLE_1, 125, 100, charisma=30, endurance=20,resistance=15, area=AREA_CIRCLE_1, ignoreAutoVerif=True, emoji=infLightSword.emoji, use=CHARISMA)

LunaPreStuffHead = stuff("Boucle d'oreille ombrale", 'lunaDarkPendant', 0, 0, endurance=int(50*0.3), agility=50,precision=int(50*0.3), strength=int(50*2.2), resistance=min(50//5, 30), percing=10, emoji=darkMaidPendants.emoji)
LunaPreStuffDress = stuff("Robe de soubrette ombrale ombrale", 'lunaDarkMaidDress', 0, 0, endurance=int(50*0.7), agility=50, precision=int(50*0.5), strength=int(50*3), percing=15, resistance=min(50//5, 40), emoji=darkMaidDress.emoji)
LunaPreStuffFlats = stuff("Ballerines ombrales", 'lunaDarkFlats', 0, 0, endurance=int(50*0.3), agility=int(50*1.3), precision=int(50*0.3), strength=int(50*2.2), resistance=min(50//5, 30), percing=10, emoji=darkMaidFlats.emoji)

lunaQuickFightEff = effect('Enchaînement',"lunaQuickFight",emoji=uniqueEmoji('<:qqLuna:932318030380302386>'))
accelerant.effects= [lunaQuickFightEff]

lunaPreSkill5_1 = copy.deepcopy(lunaSkill5_4)
lunaPreSkill5_1.cooldown, lunaPreSkill5_1.description, lunaPreSkill5_1.power, lunaPreSkill5_1.affSkillMsg = 2, "Effectue plusieurs attaques sur un adversaire", int(lunaPreSkill5_1.power*1.3), False
lunaPreSkill5_1_cast = effect("Enchainement 4","ench4",silent=True,replique=lunaPreSkill5_1)
lunaPreSkill5_2 = copy.deepcopy(lunaSkill5_2)
lunaPreSkill5_2.effectOnSelf, lunaPreSkill5_2.replay, lunaPreSkill5_2.power, lunaPreSkill5_2.affSkillMsg = lunaPreSkill5_1_cast, True, int(lunaPreSkill5_2.power*1.3), False
lunaPreSkill5_2_cast = effect("Enchaînement 3","ench3",silent=True,replique=lunaPreSkill5_2)
lunaPreSkill5_3 = copy.deepcopy(lunaSkill5_1)
lunaPreSkill5_3.effectOnSelf, lunaPreSkill5_3.replay, lunaPreSkill5_3.description, lunaPreSkill5_3.name, lunaPreSkill5_3.power, lunaPreSkill5_3.affSkillMsg = lunaPreSkill5_2_cast, True, "Effectue plusieurs attaques sur un adversaire", "Combo Corps à Corps", int(lunaPreSkill5_3.power*1.3), False
lunaPreSkill2_eff = effect("Ténèbres d'Obsidienne","lunaPreIndirect", stat=STRENGTH,power=80,emoji='<:lunaIndi:932447879786823730>',turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE)
lunaPreSkill2 = skill("Obsidienne Ténébreuse","lunaPreSkill2",TYPE_INDIRECT_DAMAGE,emoji=lunaPandan.emoji,effects=lunaPreSkill2_eff,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_INLINE_4,lunaPreSkill2_eff],range=AREA_MONO,area=AREA_CIRCLE_4,cooldown=4,description="Inflige un effet de dégâts indirects aux ennemis alentours. Les adversaires allignés subissent une deuxième fois l'effet",replay=True)
lunaPreSkill3 = skill("Frappe d'Obsidienne","lunaPreSkill3",TYPE_DAMAGE,emoji=lunaSkill2.emoji,power=int(lunaSkill2.power*lunaSkill2.repetition*1.25),cooldown=lunaSkill2.cooldown,description="Inflige de lourd dégâts à un ennemi")
lunaDarkChoc = copy.deepcopy(lunaSkill)
lunaDarkChoc.power, lunaDarkChoc.lifeSteal, lunaDarkChoc.cooldown, lunaDarkChoc.description, lunaDarkChoc.name = 200, 15, 5, "Vous téléporte au corps à corps de l'ennemi ciblé et lui porte une attaque infligeant des dégâts de zone tout en vous restituant un pourcentage des dégâts infligés", "Choc d'Obsidienne"
lunaPreUltimawashi = copy.deepcopy(lunaSkill7)
lunaPreUltimawashi.area, lunaPreUltimawashi.name, lunaPreUltimawashi.description = AREA_CIRCLE_1, "Piqué Ténébreux", "Inflige des dégâts à l'ennemi ciblé ainsi qu'aux adversaires alentours, puis repousse violament ce premier".format(lunaPreUltimawashi.power)

liaExWeapEff = effect("Kazama","liaExWeapEff",turnInit=-1,unclearable=True,dodge=20,counterOnDodge=75,power=80,description="Octroie à Lia 75% de chances d'effectuer une **contre-attaque** en esquivant un assaut adverse\nLui octroie également {0}% de chance d'obtenir l'effet {1} __{2}__ en effectuant une compétence {3} __{4}__".format(50,tablElemEff[ELEMENT_AIR].emoji[0][0],tablElemEff[ELEMENT_AIR].name,elemEmojis[ELEMENT_AIR],elemNames[ELEMENT_AIR]),emoji='<:liaWeap:908859908034793552>')
liaExWeap = weapon("Akashi","noneweap",RANGE_MELEE,AREA_CIRCLE_1,power=25,accuracy=90,magie=20,agility=20,resistance=10,area=AREA_ARC_1,emoji=liaKatana.emoji,ignoreAutoVerif=True,use=MAGIE,effects=liaExWeapEff)
liaExDotOnTarget = effect("U~indobaito","liaExDotOnTarget", stat=MAGIE,power=80,turnInit=8,lvl=8,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji='<:airKitsune:917670912646602823>')
liaExSkill1_3_ready = effect("Harikenburedo préparé","liaSkill1_3_ready",turnInit=5,emoji='<:liaSki1_3:1012765729554178138>')
liaExSkill1_3 = skill("Harikenburedo","liaExSkill1",TYPE_DAMAGE,power=120,use=MAGIE,emoji='<:liaSki1_3:1012765729554178138>',range=AREA_CIRCLE_1,area=AREA_LINE_2,effects=liaExDotOnTarget,accuracy=120,description="Dernier coup du combo Lame des vents\nInflige des dégâts aux ennemis ciblé et inflige {0} __{1}__ à la cible principale, lui infligeant des dégâts continues pendant {2} tours".format(liaExDotOnTarget.emoji[0][0],liaExDotOnTarget.name,liaExDotOnTarget.turnInit),needEffect=[liaExSkill1_3_ready],condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR])
liaExSkill1_2_ready = effect("Sutomubureido préparé","liaSkill1_2_ready",turnInit=5,emoji='<:liaSki1_2:1012761707858382929>')
liaExDotOnSelf = effect("Taifu no me","liaExDotOnSelf", stat=MAGIE,power=100,area=AREA_CIRCLE_3,turnInit=8,lvl=8,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,emoji='<:windBite:961185646993637476>')
liaExSkill1_2 = skill("Sutomubureido","liaExSkill1",TYPE_DAMAGE,use=MAGIE,emoji='<:liaSki1_2:1012761707858382929>',power=100,accuracy=120,range=AREA_MONO,area=AREA_CIRCLE_3,effectOnSelf=liaExSkill1_3_ready,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_MONO,liaExDotOnSelf],needEffect=[liaExSkill1_2_ready],condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],description="Second coup du combo Lame des vents\nInflige des dégâts aux ennemis autour de vous et vous octroie {0} __{1}__, infligeant des dégâts aux ennemis autour de vous lorsque vous terminez votre tour pendant {2} tours".format(liaExDotOnSelf.emoji[0][0],liaExDotOnSelf.name,liaExDotOnSelf.turnInit))
liaExSkill1_1_eff = copy.deepcopy(dmgUp)
liaExSkill1_1_eff.power, liaExSkill1_1_eff.turnInit = 15, 8
liaExSkill1_1 = skill("Kaze no ha","liaExSkill1",TYPE_DAMAGE,use=MAGIE,power=80,emoji='<:liaSki1_1:1012761673427333120>',effectOnSelf=liaExSkill1_2_ready,effectAroundCaster=[TYPE_BOOST,AREA_MONO,liaExSkill1_1_eff],rejectEffect=[liaExSkill1_2_ready,liaExSkill1_3_ready],condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],range=AREA_CIRCLE_1,description="Premier coup du combo Lame des vents\nInflige des dégâts à l'ennemi ciblé et augmente vos dégâts infligés de 15% pendant 8 tours")
liaExSkill1 = skill("Combo Lame des vents","liaExSkill1",TYPE_DAMAGE,use=MAGIE,emoji='<:liaSki1_3:1012765729554178138>',become=[liaExSkill1_1,liaExSkill1_2,liaExSkill1_3],description="Permet d'effectuer le combo Lame des Vents.\n\n{0} __{1}__ augmente les dégâts infligés,\n{2} __{3}__ vous octroie un effet de dégâts indirects infligeant des dégâts autour de vous en fin de tour\n{4} __{5}__ inflige un effet de dégâts indirect à la cible, lui infligeant des dégâtts lorsqu'il débute son tour".format(liaExSkill1_1.emoji,liaExSkill1_1.name,liaExSkill1_2.emoji,liaExSkill1_2.name,liaExSkill1_3.emoji,liaExSkill1_3.name))
liaExSkill2_2_ready = effect("Shapuchajido préparé","liaExSkill2_2_ready",turnInit=5,emoji='<:liaCounter:998001563379437568>')
liaExSkill2_2_e = effect("Arashi no kaze","lizExSkill2_2_e", stat=AGILITY,power=100,area=AREA_CIRCLE_3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,emoji='<:liaSamLB2:1100185041306386439>')
liaExSkill2_2 = skill("Shapuchajido","liaExSkill2",TYPE_DAMAGE,cooldown=3,power=100,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],range=AREA_CIRCLE_4,tpBehind=True,replay=True,use=AGILITY,emoji='<:liaCounter:998001563379437568>',needEffect=[liaExSkill2_2_ready],effects=[liaExSkill2_2_e],description="Vous téléporte derrière l'ennemi ciblé, lui inflige des dégâts en ignorant une grosse partie de sa résistance et inflige des dégâts aux ennemis environant",percing=50,url=senbonzakura.url)
liaExSkill2_1 = skill("Terukikku","liaExSkill2",TYPE_DAMAGE,power=125,range=AREA_CIRCLE_4,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],area=AREA_CONE_2,tpCac=True,jumpBack=3,description="Charge l'ennmi ciblé, lui inflige des dégâts et le repousse de 3 cases\nVous octroie également la possibilité d'utiliser {0} __{1}__ une fois durant les {2} prochains tours".format(liaExSkill2_2.emoji,liaExSkill2_2.name,liaExSkill2_2.needEffect[0].turnInit),effectOnSelf=liaExSkill2_2.needEffect[0],rejectEffect=[liaExSkill2_2_ready],emoji='<:liaSkill:922291249002709062>')
liaExSkill2 = skill("Terukikku +","liaExSkill2",TYPE_DAMAGE,power=liaExSkill2_1.power,use=AGILITY,emoji=liaExSkill2_1.emoji,become=[liaExSkill2_1,liaExSkill2_2],description="Inflige des dégâts agilité à l'ennemi ciblé.\n\n{0} __{1}__ permet de rejouer son tour\n{2} __{3}__ ne peut pas être utilisé pendant 4 tours après utilisation".format(liaExSkill2_2.emoji, liaExSkill2_2.name, liaExSkill2_1.emoji, liaExSkill2_1.name))
liaExSkill3_eff = effect("Hariken no me","liaExSkill3_eff", stat=MAGIE,area=AREA_DIST_5,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji="<:liaTornadoEff2:1100185833115492402>",power=135,lvl=5,turnInit=5)
liaExSkill3 = skill("Hariken","liaExSkill3",TYPE_DAMAGE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],power=150,range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=5,use=MAGIE,effectOnSelf=liaExSkill3_eff,emoji=liaExSkill3_eff.emoji[0][0],description="Inflige et repousse les ennemis en mêlée et vous octroie un effet infligeant des dégâts aux ennemis éloignés à la fin de votre tour pendant 3 tour",knockback=2)
liaExSkill4_3 = skill("Keifu","liaExSkill4",TYPE_DAMAGE,power=150,effectAroundCaster=[TYPE_HEAL,AREA_MONO,150],use=MAGIE,cooldown=5,description="Inflige des dégâts aux ennemis alliégné avec vous et vous soigne",area=AREA_INLINE_5,range=AREA_MONO,emoji="<:waterKitsune:917670866626707516>")
liaExSkill4_2_eff = effect("Asuama","liaExSkill4_2_eff", stat=MAGIE,overhealth=100,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji='<:liaWindArmor:1013901987303149630>')
liaExSkill4_2 = skill("Sunaarashi","liaExSkill4",use=MAGIE,types=TYPE_DAMAGE,power=150,range=AREA_MONO,area=AREA_CIRCLE_2,effectOnSelf=liaExSkill4_2_eff,cooldown=liaExSkill4_3.cooldown, emoji="<:earthKitsune:917670882586017792>", description="Inflige des dégâts aux ennemis en mêlée et vous octroie une armure pendnant 3 tours")
liaExSkill4_1_dot = effect("Moeta","liaExSkill4_1_dot", stat=MAGIE,power=50,turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE)
liaExSkill4_1 = skill("Sabaku no kaze","liaExSkill4",TYPE_DAMAGE,area=AREA_ALL_ENEMIES,use=MAGIE,range=AREA_MONO,power=85,description="Inflige des dégâts à tous les ennemis et leur inflige un effet de dégâts indirect pendant 3 tours",effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_ALL_ENEMIES,liaExSkill4_1_dot],cooldown=liaExSkill4_3.cooldown,emoji='<:fireKitsune:917670925904785408>')
liaExSkill4 = skill("Kyodai no kyoka","liaExSkill4",TYPE_DAMAGE,use=MAGIE,initCooldown=2,power=max(liaExSkill4_3.power,liaExSkill4_2.power,liaExSkill4_1.power+liaExSkill4_1_dot.power*liaExSkill4_1_dot.turnInit),become=[liaExSkill4_1,liaExSkill4_2,liaExSkill4_3],emoji='<:kitsuWeap:935553775500947486>',description="Permet d'utiliser les éléments des soeurs de Lia pour déclancher une attaque suivant leur élément.\n\n{0} __{1}__ vous soigne en plus d'infliger des dégâts\n{2} __{3}__ vous octroie une armure en plus d'infliger des dégâts".format(liaExSkill4_3.emoji,liaExSkill4_3.name,liaExSkill4_2.emoji,liaExSkill4_2.name))
liaExUlt_4 = skill("Kaze no bakuhatsu","liaExUlt_4",TYPE_DAMAGE,power=150,cooldown=7,ultimate=True,area=AREA_CIRCLE_1,range=AREA_CIRCLE_3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],emoji='<:liaSkiUlt3:1013889062962217021>',description="Au premier tour, inflige des dégâts aux ennemis en mêlée et les repoussent.\nAu second tour, inflige à deux reprises des dégâts dans une zone en arc de cercle centrée sur l'ennemi ciblé, repoussant les ennemis touchés et vous téléportant au corps à corps de la cible à chaque reprise, puis inflige des dégâts en cercle autour de l'ennemi ciblé\n\nChaque effet {0} __{1}__ possédé au premier tour vous octroie une armure équivalante à **5%** de vos PV Max\nChaque effet {0} __{1}__ possédé augmente les puissances des attaques en arc de cercle du second tour de **10%**\nChaque effet {0} __{1}__ possédé augmente la puissance de l'attaque de zone de **15%** et les consommes pour vous soigner de **5%** de vos PV max".format(tablElemEff[ELEMENT_AIR].emoji[0][0],tablElemEff[ELEMENT_AIR].name),accuracy=200,use=MAGIE)
liaExUlt_4_cast = effect("Enchainement - {replicaName}","liaExUlt_4_c",replique=liaExUlt_4,silent=True)
liaExUlt_3 = skill("Gyakufu no suraisu","liaExUlt_3",TYPE_DAMAGE,power=120,area=AREA_ARC_3,tpCac=True,knockback=1,range=liaExUlt_4.range,condition=liaExUlt_4.condition,description=liaExUlt_4.description,cooldown=liaExUlt_4.cooldown,replay=True,effectOnSelf=liaExUlt_4_cast,emoji='<:liaSkiUlt2:1013889034600329246>',use=MAGIE)
liaExUlt_3_cast = effect("Enchainement - {replicaName}","liaExUlt_3_c",replique=liaExUlt_3,silent=True)
liaExUlt_2 = skill("Kaze no suraisu","liaExUlt_2",TYPE_DAMAGE,power=120,area=AREA_ARC_3,tpCac=True,knockback=1,range=liaExUlt_4.range,condition=liaExUlt_4.condition,description=liaExUlt_4.description,cooldown=liaExUlt_4.cooldown,replay=True,effectOnSelf=liaExUlt_3_cast,emoji='<:liaSkiUlt1:1013889002731995246>',use=MAGIE)
liaExUlt_2_cast = effect("Cast - {replicaName}","liaExult_2_c",turnInit=2,silent=True,replique=liaExUlt_2)
liaExUlt_1 = skill("Ririsu","liaExUlt",TYPE_DAMAGE,power=50,range=AREA_CIRCLE_3,ultimate=True,area=AREA_CIRCLE_2,areaOnSelf=True,cooldown=liaExUlt_4.cooldown,effectOnSelf=liaExUlt_2_cast,emoji='<:liaSkiUlt0:1013889091831599178>',description=liaExUlt_4.description,condition=liaExUlt_4.condition,knockback=3,use=MAGIE)
liaExSkill6 = skill("Déployable - Tatsumaki","liaExSkill6",TYPE_DEPL,emoji='<:liaDepl:1013912739728592896>',use=MAGIE,range=AREA_CIRCLE_2,cooldown=7,depl=liaTornade,description="Invoque une tornade sur la cellule ciblée, infligeant des dégâts à chaque début de table aux ennemis à portée",condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR])
liaExSkill7_eff = effect("Kaze no shinkiro","liaExSkill7_e",emoji='<:liaSki6:1013891089662488596>',dodge=100,counterOnDodge=100)
liaExSkill7 = skill("Kaze no shinkiro","liaExSkill7",TYPE_ARMOR,effects=liaExSkill7_eff,replay=True,cooldown=5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],use=None,range=AREA_MONO,emoji='<:liaSki6:1013891089662488596>',description="Augmente votre probabilité d'esquive et de contre-attaque de **100%** jusqu'à votre prochain tour")

# Gwen commons
gwenSkill1_3r = effect("Serre Visieuse préparée","gwenSkill1_3r",turnInit=5,silent=True,emoji='<:klMainCb3:1080150358225080341>')
gwenSkill1_2r = effect("Griffe Sauvage préparée","gwenSkill1_2r",turnInit=5,silent=True,emoji='<:klMainCb2:1080150320107233390>')

# Klironovia
kliWeapEff = effect("Représaille","kliWeapEff",block=35,counterOnBlock=40,aggro=50,turnInit=-1,emoji='<:represailles:1101242340523397191>',description="Augmente votre probabilité de bloquer une attaque et celle de contre attaquer lors d'un blocage")
kliWeap = weapon("Pistolame Vangeresse","kliWeap",RANGE_MELEE,AREA_CIRCLE_1,80,100,strength=20,endurance=10,resistance=10,ignoreAutoVerif=True,emoji='<:kGunblade:1100679173980291082>',effects=kliWeapEff,priority=WEAPON_PRIORITY_NONE)

kliSkill1Eff = effect("Frappe Explosive","kliSkill1Eff", stat=STRENGTH,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,power=50,emoji='<:exploShotEff:1049704001257619476>',lifeSteal=35)
kliSkill1_32 = skill("Perforation","gwenSkill1",TYPE_DAMAGE,power=50,range=AREA_CIRCLE_1,effects=kliSkill1Eff,emoji='<:klSecCb3:1080152258177662976>',effPowerPurcent=120)
kliSkill1_32c = effect("Enchaînement - {replicaName}","kliSkill1_32c",silent=True,replique=kliSkill1_32)
kliSkill1_31 = skill("Serre Visieuse","gwenSkill1",TYPE_DAMAGE,power=140,range=AREA_CIRCLE_1,effectOnSelf=kliSkill1_32c,needEffect=gwenSkill1_3r,replay=True,emoji='<:klMainCb3:1080150358225080341>',description="Inflige des dégâts à l'ennemi ciblé puis enchaîne avec une autre attaque directe qui inflige également dégâts indirects supplémentaire, vous soignant en fonction des dégâts infligés")
kliSkill1_22 = skill("Lacération","gwenSkill1",TYPE_DAMAGE,power=40,range=AREA_CIRCLE_1,effectOnSelf=gwenSkill1_3r,effects=kliSkill1Eff,emoji='<:klSecCb2:1080152065625571388>',effPowerPurcent=110)
kliSkill1_22c = effect("Enchaînement - {replicaName}","kliSkill1_22c",silent=True,replique=kliSkill1_22)
kliSkill1_21 = skill("Griffe Sauvage","gwenSkill1",TYPE_DAMAGE,power=120,range=AREA_CIRCLE_1,effectOnSelf=kliSkill1_22c,needEffect=gwenSkill1_2r,replay=True,emoji='<:klMainCb2:1080150320107233390>',description=kliSkill1_31.description)
kliSkill1_12 = skill("Eventration","gwenSkill1",TYPE_DAMAGE,power=30,range=AREA_CIRCLE_1,effectOnSelf=gwenSkill1_2r,effects=kliSkill1Eff,emoji='<:klSecCb1:1080152158479061093>',effPowerPurcent=100)
kliSkill1_12c = effect("Enchaînement - {replicaName}","kliSkill1_12c",silent=True,replique=kliSkill1_12)
kliSkill1_11 = skill("Croc Pugace","gwenSkill1",TYPE_DAMAGE,power=100,range=AREA_CIRCLE_1,effectOnSelf=kliSkill1_12c,rejectEffect=[gwenSkill1_3r,gwenSkill1_2r],replay=True,emoji='<:klMainCb1:1080150284514373722>',description=kliSkill1_31.description)
kliSkill1 = skill("Combo Perforation Explosive","gwenSkill1",TYPE_DAMAGE,become=[kliSkill1_11,kliSkill1_21,kliSkill1_31],emoji=kliSkill1_32.emoji)
kliSkill2e = copy.deepcopy(dmgUp)
kliSkill2e.turnInit, kliSkill2e.power = 3, 15
kliSkill2 = skill("Ruée Sanglante","gwenSkill2",TYPE_DAMAGE,tpCac=True,power=120,effectOnSelf=kliSkill2e,effBeforePow=True,cooldown=3,range=AREA_INLINE_4,emoji='<:kStrike:1100644659241422891>',lifeSteal=50-BERS_LIFE_STEAL,description="Saute sur l'ennemi ciblé, augmentant vos dégâts infligés pendant un petit moment, lui infligeant des dégâts et vous soignant d'une partie des dégâts infligés")
kliSkill3Eff = effect("Explosion","kliSkill3e",STRENGTH,type=TYPE_DAMAGE,area=AREA_DONUT_2,trigger=TRIGGER_INSTANT,emoji=exploShotEff.emoji,power=100)
kliSkill3 = skill("Sacrifice Sauvage","gwenSkill3",TYPE_DAMAGE,initCooldown=2,power=150,maxPower=350,cooldown=5,accuracy=300,effects=kliSkill3Eff,emoji=klikliStrike.emoji,effectOnSelf=bolideEff,description="Réduit de 50% vos PVs actuels pour infliger une grosse attaque à la cible principale et une attaque avec une puissance amoindrie aux ennemis autour, tout en vous rendant invulnérable aux dégâts durant un tour. La puissance dépend du pourcentage de PV consommés")
kliSkill4_1 = skill("Aimatirí Apergía","gwenSkill4",TYPE_DAMAGE,power=150,damageOnArmor=2.5,lifeSteal=150-BERS_LIFE_STEAL,garCrit=True,emoji=pentastrike5.emoji,range=AREA_CIRCLE_1,area=AREA_ARC_1,cooldown=3,description="Inflige à deux reprises des dégâts aux ennemis ciblés en vous soignant en fonction des dégâts infligés. Inflige forcément un coup critique à la cible principale",accuracy=200)
kliSkill4_c = effect("Enchaînement - {replicaName}","gwenSkill4",silent=True,replique=kliSkill4_1)
kliSkill4 = copy.deepcopy(kliSkill4_1)
kliSkill4.effectOnSelf, kliSkill4.replay, kliSkill4.emoji = kliSkill4_c, True, pentastrike.emoji

# Gwen
gwenyWeapEff = effect("Nébuleuse","gwenyWeapEff",block=50,turnInit=-1,aggro=50,emoji='<:nebuleuse:1105170021581336727>',description="Augmente grandement votre porbabilité de bloquer les attaques")
gwenyWeap = weapon("Pistolame Renforçante","gwenyExWeap",RANGE_MELEE,AREA_CIRCLE_1,80,100,intelligence=10,endurance=10,resistance=20,ignoreAutoVerif=True,emoji='<:gGunblade:1100679196436594759>',effects=gwenyWeapEff,priority=WEAPON_PRIORITY_NONE)

gwenyArmor = effect("Armure","gwenyArmor",INTELLIGENCE,overhealth=35,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,replace=True,emoji='<:gwenyShield:1215632408724901888>')
gwenySkill1_32 = skill("Perforation","gwenSkill1",TYPE_DAMAGE,power=kliSkill1_32.power,range=AREA_CIRCLE_1,emoji='<:gwSecCb3:1080152231153778699>',effectAroundCaster=[TYPE_ARMOR,AREA_CIRCLE_2,gwenyArmor],effPowerPurcent=150)
gwenySkill1_32c = effect("Enchaînement - {replicaName}","gwenySkill1_32c",silent=True,replique=gwenySkill1_32)
gwenySkill1_31 = skill("Serre Visieuse","gwenSkill1",TYPE_DAMAGE,power=kliSkill1_31.power,range=AREA_CIRCLE_1,effectOnSelf=gwenySkill1_32c,needEffect=gwenSkill1_3r,replay=True,emoji='<:klMainCb3:1080150358225080341>',description="Inflige des dégâts à l'ennemi ciblé puis enchaîne avec une autre attaque directe et octroie de l'armure à vous et vos alliés proches")
gwenySkill1_22 = skill("Lacération","gwenSkill1",TYPE_DAMAGE,power=kliSkill1_22.power,range=AREA_CIRCLE_1,effectOnSelf=gwenSkill1_3r,emoji='<:gwSecCb2:1080152032813535353>',effectAroundCaster=[TYPE_ARMOR,AREA_CIRCLE_2,gwenyArmor],effPowerPurcent=135)
gwenySkill1_22c = effect("Enchaînement - {replicaName}","gwenySkill1_22c",silent=True,replique=gwenySkill1_22)
gwenySkill1_21r = effect("Griffe Sauvage préparée","gwenySkill1_21r",turnInit=3,silent=True,emoji='<:klMainCb2:1080150320107233390>')
gwenySkill1_21 = skill("Griffe Sauvage","gwenSkill1",TYPE_DAMAGE,power=kliSkill1_21.power,range=AREA_CIRCLE_1,effectOnSelf=gwenySkill1_22c,needEffect=gwenSkill1_2r,replay=True,emoji='<:klMainCb2:1080150320107233390>',description=gwenySkill1_31.description)
gwenySkill1_12 = skill("Eventration","gwenSkill1",TYPE_DAMAGE,power=kliSkill1_12.power,range=AREA_CIRCLE_1,effectOnSelf=gwenSkill1_2r,emoji='<:gwSecCb1:1080152129613869078>',effectAroundCaster=[TYPE_ARMOR,AREA_CIRCLE_2,gwenyArmor],effPowerPurcent=100)
gwenySkill1_12c = effect("Enchaînement - {replicaName}","gwenySkill1_12c",silent=True,replique=gwenySkill1_12)
gwenySkill1_11 = skill("Croc Pugace","gwenSkill1",TYPE_DAMAGE,power=kliSkill1_11.power,range=AREA_CIRCLE_1,effectOnSelf=gwenySkill1_12c,rejectEffect=[gwenSkill1_3r,gwenSkill1_2r],replay=True,emoji='<:klMainCb1:1080150284514373722>',description=gwenySkill1_31.description)
gwenySkill1 = skill("Combo Perforation Renforçante","gwenSkill1",TYPE_DAMAGE,become=[gwenySkill1_11,gwenySkill1_21,gwenySkill1_31],emoji=gwenySkill1_32.emoji)
gwenySkill2e = copy.deepcopy(defenseUp)
gwenySkill2e.turnInit, gwenySkill2e.power = 3, 20
gwenySkill2 = skill("Taillade Sautée",kliSkill2.id,TYPE_DAMAGE,tpCac=True,range=kliSkill2.range,cooldown=kliSkill2.cooldown,power=kliSkill2.power,effectOnSelf=gwenySkill2e,emoji='<:gStrike:1100681148876718120>',effectAroundCaster=[TYPE_ARMOR,AREA_CIRCLE_2,gwenyArmor],effPowerPurcent=75,description="Saute sur l'ennemi ciblé, lui infligeant des dégâts tout en réduisant vos dégâts subis durant un moment et octroyant une armure pour vous et vos alliés proches")
gwenySkill3eff1 = copy.deepcopy(defenseUp)
gwenySkill3eff1.turnInit, gwenySkill3eff1.power = 1, 7.5
gwenySkill3 = skill("Sacrifice Protecteur",kliSkill3.id,TYPE_ARMOR,range=AREA_MONO,area=AREA_CIRCLE_5,effects=[gwenySkill3eff1,gwenyArmor],effectOnSelf=bolideEff,cooldown=kliSkill3.cooldown,emoji='<:gwenSacrifice:1215632909176934400>',description="Réduit vos PVs actuels de 50% pour octroyer une armure et réduire les dégâts subis par vos alliés proches, tout en vous rendant invulnérable durant un tour. La puissance des effets dépend de la quantité de PVs consummés")
gwenySkill4e = effect("Prostateftikí Apergía","Prostateftikí Apergía",INTELLIGENCE,strength=-5,magie=5,resistance=-5,block=-20,turnInit=3,type=TYPE_MALUS)
gwenySkill4_1 = skill("Prostateftikí Apergía","gwenSkill4",TYPE_DAMAGE,power=100,damageOnArmor=2.5,armorConvert=50,aoeArmorConvert=25,effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_2,gwenySkill4e],garCrit=True,emoji=gwenPenta5.emoji,range=AREA_CIRCLE_1,area=AREA_ARC_1,cooldown=3,description="Inflige à deux reprises des dégâts aux ennemis ciblés en vous octroyant à vous et vos alliés proches une armure en fonction des dégâts infligés tout en réduisant les statistiques des ennemis proches. Inflige forcément un coup critique à la cible principale",accuracy=200)
gwenySkill4_c = effect("Enchaînement - {replicaName}","gwenSkill4",silent=True,replique=gwenySkill4_1)
gwenySkill4 = copy.deepcopy(gwenySkill4_1)
gwenySkill4.effectOnSelf, gwenySkill4.replay, gwenySkill4.emoji, gwenySkill4.effectAroundCaster = gwenySkill4_c, True, gwenPenta.emoji, None

# Alty
altyWeapEff = effect("Kardia","altyWeapEff",turnInit=-1,emoji=kardia.emoji,aggro=50,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_HEAL,power=50,stat=CHARISMA)
altyWeap = weapon("Pistolame Régénérante","altyExWeap",RANGE_MELEE,AREA_CIRCLE_1,80,100,charisma=10,endurance=10,resistance=20,ignoreAutoVerif=True,emoji=aWeap.emoji,effects=altyWeapEff,priority=WEAPON_PRIORITY_NONE)

altyRegen = effect("Régénération","altyRegen",CHARISMA,power=25,turnInit=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,stackable=True,emoji='<:AltyRegen:994748551932428319>')
altySkill1_32 = skill("Perforation","gwenSkill1",TYPE_DAMAGE,power=kliSkill1_32.power,range=AREA_CIRCLE_1,emoji='<:alSecCb3:1080152283670650931>',effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_CIRCLE_2,altyRegen],effPowerPurcent=150)
altySkill1_32c = effect("Enchaînement - {replicaName}","altySkill1_32c",silent=True,replique=altySkill1_32)
altySkill1_31 = skill("Serre Visieuse","gwenSkill1",TYPE_DAMAGE,power=kliSkill1_31.power,range=AREA_CIRCLE_1,effectOnSelf=altySkill1_32c,needEffect=gwenSkill1_3r,replay=True,emoji='<:klMainCb3:1080150358225080341>',description="Inflige des dégâts à l'ennemi ciblé puis enchaîne avec une autre attaque directe et octroie un effet de régénération à vous et vos alliés proches")
altySkill1_22 = skill("Lacération","gwenSkill1",TYPE_DAMAGE,power=kliSkill1_22.power,range=AREA_CIRCLE_1,effectOnSelf=gwenSkill1_3r,emoji='<:alSecCb2:1080152099549098016>',effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_CIRCLE_2,altyRegen],effPowerPurcent=135)
altySkill1_22c = effect("Enchaînement - {replicaName}","altySkill1_22c",silent=True,replique=altySkill1_22)
altySkill1_21 = skill("Griffe Sauvage","gwenSkill1",TYPE_DAMAGE,power=kliSkill1_21.power,range=AREA_CIRCLE_1,effectOnSelf=altySkill1_22c,needEffect=gwenSkill1_2r,replay=True,emoji='<:klMainCb2:1080150320107233390>',description=altySkill1_31.description)
altySkill1_12 = skill("Eventration","gwenSkill1",TYPE_DAMAGE,power=kliSkill1_12.power,range=AREA_CIRCLE_1,effectOnSelf=gwenSkill1_2r,emoji='<:alSecCb1:1080152189806325822>',effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_CIRCLE_2,altyRegen],effPowerPurcent=100)
altySkill1_12c = effect("Enchaînement - {replicaName}","altySkill1_12c",silent=True,replique=altySkill1_12)
altySkill1_11 = skill("Croc Pugace","gwenSkill1",TYPE_DAMAGE,power=kliSkill1_11.power,range=AREA_CIRCLE_1,effectOnSelf=altySkill1_12c,rejectEffect=[gwenSkill1_3r,gwenSkill1_2r],replay=True,emoji='<:klMainCb1:1080150284514373722>',description=altySkill1_31.description)
altySkill1 = skill("Combo Perforation Régénérante","gwenSkill1",TYPE_DAMAGE,become=[altySkill1_11,altySkill1_21,altySkill1_31],emoji=altySkill1_32.emoji)
altySkill2e = copy.deepcopy(healDoneBonus)
altySkill2e.turnInit, altySkill2e.power = 3, 10
altySkill2 = skill("Redoppio Glissé",kliSkill2.id,TYPE_DAMAGE,tpCac=True,cooldown=kliSkill2.cooldown,range=kliSkill2.range,power=kliSkill2.power,effectOnSelf=altySkill2e,emoji='<:aStrike:1100681172167704668>',effectAroundCaster=[TYPE_ARMOR,AREA_CIRCLE_2,altyRegen],effPowerPurcent=65,description="Saute sur l'ennemi ciblé, lui infligeant des dégâts tout augmentant vos soins et armures réalisés durant un moment et octroyant un effet régénérant à vous et vos alliés proches")
altySkill3eff1 = copy.deepcopy(dmgUp)
altySkill3eff1.turnInit, altySkill3eff1.power = 3, 5
altySkill3 = skill("Sacrifice Bienveillant",kliSkill3.id,TYPE_INDIRECT_HEAL,range=AREA_MONO,area=AREA_CIRCLE_5,effects=[altySkill3eff1,altyRegen],effectOnSelf=bolideEff,cooldown=kliSkill3.cooldown,emoji=healingSacrifice.emoji,description="Réduit vos PVs actuels de 50% pour octroyer un effet régénérant et augmenter les dégâts infligés par vos alliés proches, tout en vous rendant invulnérable durant un tour. La puissance des effets dépend de la quantité de PVs consummés")
altySkill4e = effect("Regenerans gratis","altySkill4e",CHARISMA,strength=7.5,magie=7.5,charisma=5,intelligence=5,turnInit=3)
altySkill4_1 = skill("Regenerans gratis","gwenSkill4",TYPE_DAMAGE,power=100,damageOnArmor=2.5,lifeSteal=100,aoeLifeSteal=50,garCrit=True,effectAroundCaster=[TYPE_BOOST,AREA_CIRCLE_2,altySkill4e],emoji=altyPenta5.emoji,range=AREA_CIRCLE_1,area=AREA_ARC_1,cooldown=3,description="Inflige à deux reprises des dégâts aux ennemis ciblés en vous soignant vous et vos alliés proches en fonction des dégâts infligés tout en augmentant vos statistiques. Inflige forcément un coup critique à la cible principale",accuracy=200)
altySkill4_c = effect("Enchaînement - {replicaName}","gwenSkill4",silent=True,replique=altySkill4_1)
altySkill4 = copy.deepcopy(altySkill4_1)
altySkill4.effectOnSelf, altySkill4.replay, altySkill4.emoji, altySkill4.effectAroundCaster = altySkill4_c, True, altyPenta.emoji, None

gwenyExChangeSkill = skill("Transposition - Gwendoline","gwenyExChangeSkill",TYPE_BOOST,cooldown=3,emoji='<:gwendolineStans:1080141611482218629>',description="Change votre personnage pour Gwendoline, dont les compétences sont plus accés vers la protection des alliés et l'entrave des ennemis",range=AREA_MONO,replay=True)
klikliExChangeSkill, altyExChangeSkill = copy.deepcopy(gwenyExChangeSkill),copy.deepcopy(gwenyExChangeSkill)
klikliExChangeSkill.name, klikliExChangeSkill.emoji, klikliExChangeSkill.description = "Transposition - Klironovia",'<:klironiviaStans:1080141635658207374>',"Change votre personnage pour Klironovia, dont les compétences sont plus accés vers les dégâts et le vol de vie personnel"
altyExChangeSkill.name, altyExChangeSkill.emoji, altyExChangeSkill.description = "Transposition - Altikia",'<:altikiaStans:1080141661931311235>',"Change votre personnage pour Altikia, dont les compétences sont plus accés vers les régénérations et le boost des alliés"

gwenChangeSkillKA = skill("Transposition",gwenyExChangeSkill.id,TYPE_BOOST,become=[klikliExChangeSkill, altyExChangeSkill],description="Permet de changer votre personnage pour Klironovia ou Altikya",emoji=gwenyExChangeSkill.emoji)
gwenChangeSkillKG = skill("Transposition",gwenyExChangeSkill.id,TYPE_BOOST,become=[klikliExChangeSkill, gwenyExChangeSkill],description="Permet de changer votre personnage pour Klironovia ou Gwendoline",emoji=altyExChangeSkill.emoji)
gwenChangeSkillGA = skill("Transposition",gwenyExChangeSkill.id,TYPE_BOOST,become=[gwenyExChangeSkill, altyExChangeSkill],description="Permet de changer votre personnage pour Gwendoline ou Altikya",emoji=klikliExChangeSkill.emoji)

gwenExCummonSkillEff1, gwenExCummonSkillEff2 = copy.deepcopy(dmgUp), copy.deepcopy(defenseUp)
gwenExCummonSkillEff1.power, gwenExCummonSkillEff1.turnInit = 15, 3
gwenExCummonSkillEff2.power, gwenExCummonSkillEff2.turnInit = gwenExCummonSkillEff1.power, gwenExCummonSkillEff1.turnInit
gwenExCummonSkillEff3 = effect("Tritécence","gwenExCummonSkillEff3",HARMONIE,type=TYPE_INDIRECT_HEAL,power=75,lvl=1,trigger=TRIGGER_HP_UNDER_70,emoji=heartStone.emoji,turnInit=gwenExCummonSkillEff2.turnInit)
gwenExCummonSkill = skill("Tritécence","gwenExCummonSkill",TYPE_BOOST,effects=[gwenExCummonSkillEff1,gwenExCummonSkillEff2,gwenExCummonSkillEff3],emoji=heartStone.emoji,cooldown=gwenExCummonSkillEff1.turnInit,description="Augmente les dégâts infligés et réduit ceux reçus de la cible de 15%, tout en lui octroyant un effet curatif qui le soigne si ses PVs tombent en dessous de 70%, tout en vous permetant de rejouer votre tour")


klikliExSkillList = [gwenChangeSkillGA,kliSkill1,kliSkill2,kliSkill3,kliSkill4,gwenExCummonSkill]
gwenyExSkillList = [gwenChangeSkillKA,gwenySkill1,gwenySkill2,gwenySkill3,gwenySkill4,gwenExCummonSkill]
altyExSkillList = [gwenChangeSkillKG,altySkill1,altySkill2,altySkill3,altySkill4,gwenExCummonSkill]

gwenyExStuff = [
    stuff("Barrette noire","gwenyExStuff1",0,strength=75,endurance=120,intelligence=100,charisma=35,resistance=25,percing=20,agility=20,precision=20,emoji=''),
    stuff("Robe et Leggins noirs","gwenyExStuff2",1,strength=75,endurance=130,intelligence=100,charisma=35,resistance=30,percing=20,agility=20,precision=20,emoji=''),
    stuff("Ballerines noires","gwenyExStuff3",2,strength=75,endurance=120,intelligence=100,charisma=35,resistance=25,percing=20,agility=20,precision=20,emoji='')
]
klikliExStuff = [
    stuff("Barrette noire","gwenyExStuff1",0,strength=150,endurance=120,intelligence=35,charisma=35,resistance=25,percing=20,agility=20,precision=20,emoji=''),
    stuff("Robe et Leggins noirs","gwenyExStuff2",1,strength=150,endurance=130,intelligence=35,charisma=35,resistance=30,percing=20,agility=20,precision=20,emoji=''),
    stuff("Ballerines noires","gwenyExStuff3",2,strength=150,endurance=120,intelligence=35,charisma=35,resistance=25,percing=20,agility=20,precision=20,emoji='')
]
altyExStuff = [
    stuff("Barrette noire","gwenyExStuff1",0,strength=75,endurance=120,intelligence=35,charisma=100,resistance=25,percing=20,agility=20,precision=20,emoji=''),
    stuff("Robe et Leggins noirs","gwenyExStuff2",1,strength=75,endurance=130,intelligence=35,charisma=100,resistance=30,percing=20,agility=20,precision=20,emoji=''),
    stuff("Ballerines noires","gwenyExStuff3",2,strength=75,endurance=120,intelligence=35,charisma=100,resistance=25,percing=20,agility=20,precision=20,emoji='')
]


krysWaterWeakness = effect("KrysTal","krysWaterWeakness",power=10,armorDmgBonus=0.10,turnInit=-1,unclearable=True,description="Augmente de **{0}%** les dégâts subis des compétences **Eau** mais augmente d'autant les dégâts sur armure infligés",emoji=krystalisation.emoji)
krysWeapon = copy.deepcopy(krystalFist)
krysWeapon.effects=krysWaterWeakness

lioExWeap = weapon("AquaMage","noneWeap",RANGE_LONG,AREA_CIRCLE_5,0,0,charisma=35)
lioExSkill1 = skill("AquaStrike","lioExSkill1",TYPE_DAMAGE,power=80,use=CHARISMA,emoji='<:water2:1065647727708483654>',description="Un sort simple qui inflige des dégâts à l'ennemi ciblé")
lioExSkill2_eff = effect("VibrAqua","lioExSkill2_eff", stat=CHARISMA,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,area=AREA_DONUT_2,power=85,emoji='<:water3:1065647689129271397>')
lioExSkill2 = skill("VibrAqua","lioExSkill2",TYPE_DAMAGE,power=120,effects=lioExSkill2_eff,cooldown=5,emoji='<:vibraqua:1123874146678489118>',effectAroundCaster=[TYPE_HEAL,AREA_LOWEST_HP_ALLIE,100],description="Inflige des dégâts à l'ennemi ciblé, des dégâts indirects autour de lui et soigne  votre allié le plus blessé")
lioExSkill3_eff1, lioExSkill3_eff2 = copy.deepcopy(defenseUp), effect("AquaPurification","lioExSkill3_eff2", stat=CHARISMA,power=40,turnInit=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji='<:water1:1065647748826791966>')
lioExSkill3_eff1.power, lioExSkill3_eff1.stat, lioExSkill3_eff1.turnInit = 3.5, CHARISMA, lioExSkill3_eff2.turnInit
lioExSkill3 = skill("AquaVoile","lioExSKill3",TYPE_INDIRECT_HEAL,effects=[lioExSkill3_eff2,lioExSkill3_eff1],cooldown=3,emoji=lioExSkill3_eff1.emoji[0][0],effPowerPurcent=150,description="Octroie un effet régénérant et réduit les dégâts subis par l'allié ciblé")
lioExSkill4_eff1 = effect("Charme","lioExSkill4_eff1",trigger=TRIGGER_INSTANT,area=AREA_DONUT_3,callOnTrigger=charming2,emoji='<:waterKitsune:917670866626707516>')
lioExSkill4_eff2 = effect("Charme","lioExSkill4_eff2",trigger=TRIGGER_INSTANT,area=AREA_LINE_5,callOnTrigger=charming,emoji='<:waterKitsune:917670866626707516>')
lioExSkill4 = skill("Gekiryū","lioExSkill4",TYPE_DAMAGE,power=135,use=CHARISMA,area=lioExSkill4_eff2.area,effects=lioExSkill4_eff2,effectOnSelf=lioExSkill4_eff1,effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_CIRCLE_2,lioExSkill3_eff2],cooldown=5,ultimate=True,emoji=lioLB.emoji,url=lioLB.url,description="Inflige des dégâts aux ennemis ciblés, réduit leurs statistiques et augmente celles des alliés alentours tout en leur octroyant un effet régénérant")
lioExSkill5_eff = effect("Oeudème","lioExSKill5_eff", stat=CHARISMA,power=75,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,turnInit=3)
lioExSkill5 = skill("AquaBulle","lioExSkill5",TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_1,effects=lioExSkill5_eff,cooldown=3,effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_LOWEST_HP_ALLIE,lioExSkill3_eff2],emoji='<:lioSkill:922328964926697505>',description="Inflige un effet de dégâts périodiques aux ennemis ciblés et octroie un effet régénérant à l'allié le plus blessé")
lioExSkill6 = skill("Déluge","liaExSkill6",TYPE_DAMAGE,power=80,area=AREA_CIRCLE_2,range=AREA_MONO,knockback=3,cooldown=3,description="Inflige des dégâts aux ennemis ciblés et les repousse",emoji="<:enemyWater:1042313114487636038>")

beneRedempt = copy.deepcopy(redemption)
beneRedempt.say = "Repentez vous !!"

lenaExStuff1 = stuff("Boucle d'Oreille en Améthyste","",0,strength=100,endurance=25,charisma=35,agility=20,precision=75,intelligence=20,magie=10,resistance=10,percing=15,emoji=amethystEarRings.emoji)
lenaExStuff2 = stuff("Robe Azurée","",1,strength=100,endurance=25,charisma=35,agility=20,precision=75,intelligence=20,magie=10,resistance=10,percing=15,emoji=lightBlueJacket.emoji)
lenaExStuff3 = stuff("Ballerines Azurées","",2,strength=100,endurance=25,charisma=35,agility=20,precision=75,intelligence=20,magie=10,resistance=10,percing=15,emoji=lightBlueFlats.emoji)
lenaExWeapon = weapon("Fusil de précision","",RANGE_LONG,AREA_CIRCLE_7,power=80,accuracy=120,strength=25,precision=25,emoji=splatcharger.emoji,priority=WEAPON_PRIORITY_LOWEST)

lenaExSkill1_3_n = effect("Tir Duo chargé","tirDuoReady",turnInit=5,silent=True,emoji='<:lenaShot3:1205601393306501221>')
lenaExSkill1_3 = skill("Tir Duo","lenaExSkill1",TYPE_DAMAGE,power=100,repetition=2,emoji=lenaExSkill1_3_n.emoji[0][0],needEffect=lenaExSkill1_3_n,description="Inflige des dégâts à deux reprises à l'ennemi ciblé")
lenaExSkill1_2_n = effect("Tir Concentré","tirconcenready",turnInit=5,silent=True,emoji='<:lenaShot2:1205600415006334998>')
lenaExSkill1_2 = skill("Tir Concentré","lenaExSkill1",TYPE_DAMAGE,power=150,needEffect=lenaExSkill1_2_n,effectOnSelf=lenaExSkill1_3_n,emoji=lenaExSkill1_2_n.emoji[0][0],description="Inflige des dégâts à l'ennemi ciblé")
lenaExSkill1_1 = skill("Tir Direct","lenaExSkill1",TYPE_DAMAGE,power=100,effectOnSelf=lenaExSkill1_2_n,emoji="<:lenaShot1:1205600391224369222>",rejectEffect=[lenaExSkill1_2_n,lenaExSkill1_3_n],description="Inflige des dégâts à l'ennemi ciblé")
lenaExSkill1 = skill("Combo - Tir Duo","lenaExSkill1",TYPE_DAMAGE,emoji=lenaExSkill1_3.emoji,become=[lenaExSkill1_1,lenaExSkill1_2,lenaExSkill1_3],description="Permet d'utiliser le combo Tir Duo, un combo simple de dégâts sans temps de rechargement")

lenaExSkill2_2_e1 = effect("Givre","leanExSkill2_2_e1",dodge=-20,turnInit=3,type=TYPE_MALUS,emoji='<:icelame2:1156452836964569148>')
lenaExSkill2_2_e2 = effect("Grenade Cryogénique","lenaExSkill22e2",trigger=TRIGGER_INSTANT,area=AREA_DONUT_1,callOnTrigger=lenaExSkill2_2_e1,emoji='<:ice2:941494399337136208>')
lenaExSkill2_2_e3 = copy.deepcopy(chained)
lenaExSkill2_2_e3.turnInit, lenaExSkill2_2_e3.name, lenaExSkill2_2_e3.emoji = 3, "Congelé", uniqueEmoji("<:ice:941494417926270987>")
lenaExSkill2_2 = skill("Grenade Cryogénique","lenaExSkill2",TYPE_DAMAGE,power=150,effects=[lenaExSkill2_2_e3,lenaExSkill2_2_e2],cooldown=3,emoji=lenaExSkill2_2_e2.emoji[0][0],condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],description="Inflige des dégâts aux ennemis ciblé, immobilise la cible principale et réduit la probabilité d'esquive des autres ennemis autour durant un moment")
lenaExSkill2_3_e = effect("Grenade Temporelle","lenaExSkill2_3_e",STRENGTH,type=TYPE_INDIRECT_DAMAGE,power=175,trigger=TRIGGER_INSTANT,emoji='<:bombeTemporelle:1156598550566797373>')
lenaExSkill2_3 = skill("Grenade Temporelle","lenaExSkill2",TYPE_INDIRECT_DAMAGE,effects=lenaExSkill2_3_e,area=AREA_CIRCLE_1,emoji=lenaExSkill2_3_e.emoji[0][0],description="Inflige des dégâts indirects aux ennemis ciblés",cooldown=3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME])
lenaExSkill2 = skill("Lance-Grenade","lenaExSkill2",TYPE_DAMAGE,become=[lenaExSkill2_2,lenaExSkill2_3],description="Vous permet d'utiliser une grenade élémentaire",emoji=lenaExSkill2_3.emoji)

lenaExSkill3_1 = skill("Balle Rapide","lenaExSkill3",TYPE_DAMAGE,power=100,damageOnArmor=2,emoji='<:balleDirect:1145784901673693265>',replay=True,description="Inflige des dégâts à l'ennemi ciblé (augmentés contre l'armure) et vous permet de rejouer votre tour")
lenaExSkill3_2 = skill("Balle Fendue","lenaExSkill3",TYPE_DAMAGE,power=70,damageOnArmor=2,area=AREA_CONE_2,emoji='<:balleFendue:1145784926441046046>',replay=True,description="Inflige des dégâts aux ennemis ciblés (augmentés contre l'armure) et vous permet de rejouer votre tour")
lenaExSkill3_3_e1 = effect("Balle Intemporelle","lenaExSkill3_3_e1",STRENGTH,power=85,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_ON_REMOVE,emoji='<:balleIntemporelle:1156598486435889172>')
lenaExSkill3_3_e2 = effect("Distorsion Intemporelle","lenaExSkill3_3_e2",STRENGTH,power=50,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_ON_REMOVE,area=AREA_DONUT_1,emoji=desyncBenEff.emoji)
lenaExSkill3_3 = skill("Balle Intemporelle","lenaExSkill3",TYPE_INDIRECT_DAMAGE,effects=[lenaExSkill3_3_e1,lenaExSkill3_3_e2],emoji=lenaExSkill3_3_e1.emoji[0][0],replay=True,description="Marque l'ennemi et vous permet de rejouer votre tour. Lors de votre prochain tour, inflige des dégâts à l'ennemi marqué et aux ennemis autour")
lenaExSkill3 = skill("Tir Rapide",lenaExSkill3_1.id,TYPE_DAMAGE,become=[lenaExSkill3_1,lenaExSkill3_2,lenaExSkill3_3],description="Vous permet d'utiliser des compétences rapides",emoji=lenaExSkill3_1.emoji)

lenaExSkill3_1.iaPow, lenaExSkill3_2.iaPow, lenaExSkill3_3.iaPow = lenaExSkill3_1.iaPow+100, lenaExSkill3_2.iaPow+100, lenaExSkill3_3.iaPow+100

lenaExSkill4_1 = skill("Déploiement","lenaExSkill4",TYPE_SUMMON, range=AREA_CIRCLE_3, nbSummon = 3, invocation = lenaDrone2Smn.name, cooldown=4, description="Invoque trois drônes artilleurs autour de vous",emoji=lenaDrone1Smn.icon[0])
lenaExSkill4_e = effect("Déploiement","lenaExSkill4_e",type=TYPE_SUMMON, callOnTrigger=lenaDrone2Smn, lvl = 2, area=AREA_BIGDONUT, trigger=TRIGGER_INSTANT)
lenaExSkill4 = skill("Déploiement","lenaExSkill4",TYPE_PASSIVE,effects=lenaExSkill4_e,become=[lenaExSkill4_1],emoji=lenaExSkill4_1.emoji,description="Permet d'invoquer trois {0} {1}. Passivement, deux sont invoqués au début du combat".format(lenaDrone2Smn.icon[0],lenaDrone2Smn.name))
lenaExSkill4.initCooldown = 4

lenaExSkill5e = effect("Surchage du Limiteur","lenaOverchargeEff",power=50,turnInit=4,callOnTrigger=explosion.effectOnSelf,trigger=TRIGGER_ON_REMOVE,precision=25,emoji='<:analyse:1116225083904626748>',stackable=True)
lenaExSkill5e1 = effect("Overdrive","lenaExSkill5e1",trigger=TRIGGER_ON_REMOVE,callOnTrigger=lenaExSkill5e)
lenaExSkill5e1.iaPow = lenaExSkill5e.iaPow
lenaExSkill51d = effect("Rechargement","lenaExSkill5d",silent=True,turnInit=8,type=TYPE_MALUS,emoji='<:unepidemic:1016788322246471801>')
lenaExSkill51 = skill("Surcharge du Limiteur","lenaExSkill5",TYPE_BOOST,effects=lenaExSkill5e1,emoji=lenaExSkill5e.emoji[0][0],range=AREA_MONO,description="Lors de votre prochain tour, accroie grandement vos dégâts infligés lors des trois prochains tours, mais vous empêche d'utiliser une compétence lors du quatrième",rejectEffect=lenaExSkill51d,effectAroundCaster=[TYPE_MALUS,AREA_MONO,lenaExSkill51d])
lenaExSkill51.iaPow = 100
lenaExSkill52 = skill("Railgun","lenaRailgun",TYPE_DAMAGE,power=350,ultimate=True,damageOnArmor=3,area=AREA_LINE_5,range=AREA_CIRCLE_7,accuracy=500,garCrit=True,emoji='<:lenaRailgun:1209368562750201886>',needEffect=lenaExSkill5e,effectFinisher=True,description="Inflige d'importants dégâts sur toute une ligne. Ignore la réduction de dégâts de zone, inflige forcément un coup critique à la cible principale, dispose d'une précision parfaite et met fin à {0}".format(lenaExSkill5e))

lenaExSkill5 = skill(lenaExSkill51.name,lenaExSkill51.id,TYPE_BOOST,become=[lenaExSkill51,lenaExSkill52],emoji=lenaExSkill51.emoji)

shushiStuff1 = stuff("Bêret Scolaire","",0,magie=115,endurance=50,charisma=35,agility=75,precision=75,intelligence=20,resistance=20,percing=10,emoji=shushi50Hat.emoji,effects=squidRollEff,critical=-20)
shushiStuff2 = stuff("Uniforme Scolaire","",1,magie=115,endurance=50,charisma=35,agility=75,precision=75,intelligence=20,resistance=20,percing=10,emoji=shushi50Dress.emoji,critical=-20)
shushiStuff3 = stuff("Mocassins à Froufrou Scolaire","",2,magie=115,endurance=50,charisma=35,agility=75,precision=75,intelligence=20,resistance=20,percing=10,emoji=shushi50Shoes.emoji,critical=-20)
shushiWeapon = weapon("Eclatana Doto Chic","",RANGE_MELEE,AREA_BIGDONUT,power=100,accuracy=200,magie=25,precision=25,emoji=eclatanaDoto.emoji,priority=WEAPON_PRIORITY_LOWEST,effects=copy.deepcopy(eclataDash))
shushiWeapon.effects.id, shushiWeapon.effects.aggro, shushiWeapon.effects.dodge = shushiWeapon.effects.id+"+", 500, 20

shushiMikel = effect("Mikel","mikel",turnInit=5,silent=True,emoji="<:mikel:988359917062725682>")
shushiSkill111_1 = skill("Mikelat","shushiSkill111",TYPE_DAMAGE,power=100,range=AREA_CIRCLE_1,emoji='<:mikelat:988360079919185921>',use=MAGIE,accuracy=150)
shushiSkill111_c = effect("Enchaînement - {replicaName}","shushiSkill111_c",silent=True,replique=shushiSkill111_1)
shushiSkill111 = skill(shushiSkill111_1.name,shushiSkill111_1.id,TYPE_DAMAGE,power=50,repetition=4,accuracy=70,replay=True,use=MAGIE,emoji=shushiSkill111_1.emoji,effectOnSelf=shushiSkill111_c,description="Inflige des dégâts à cinq reprises à l'ennemi ciblé",needEffect=shushiMikel)
shushiSkill112 = skill("Mikelet","shushiSkill112",TYPE_DAMAGE,power=200,garCrit=True,area=AREA_INLINE_3,tpCac=True,use=MAGIE,emoji='<:mikelet:988360011489112134>',needEffect=shushiMikel,description="Saute sur l'ennemi ciblé et lui inflige des dégâts forcément critiques")
shushiSkill113_3 = skill("Mikelit","shushiSkill113",TYPE_DAMAGE,tpCac=True,emoji='<:mikelit:988360135485313085>',range=AREA_CIRCLE_1,use=MAGIE,damageOnArmor=2,power=50,percing=20,garCrit=True,description="Inflige une série d'attaque sur l'ennemi ciblé. Les dégâts infligés sur l'armure sont augmentés")
shushiSkill113_3c = effect("Enchaînement - {replicaName}","shushiSkill113_3c",replique=shushiSkill113_3,silent=True,emoji=shushiSkill113_3.emoji)
shushiSkill113_2 = skill("Mikelit","shushiSkill113",TYPE_DAMAGE,tpCac=True,emoji='<:mikelit:988360135485313085>',range=AREA_CIRCLE_1,use=MAGIE,damageOnArmor=2,power=25,repetition=4,effectOnSelf=shushiSkill113_3c,replay=True,knockback=1,description="Inflige une série d'attaque sur l'ennemi ciblé. Les dégâts infligés sur l'armure sont augmentés")
shushiSkill113_2c = effect("Enchaînement - {replicaName}","shushiSkill113_2c",replique=shushiSkill113_2,silent=True,emoji=shushiSkill113_2.emoji)
shushiSkill113_1 = skill("Mikelit","shushiSkill113",TYPE_DAMAGE,tpCac=True,emoji='<:mikelit:988360135485313085>',range=AREA_CIRCLE_1,use=MAGIE,damageOnArmor=2,power=20,repetition=3,effectOnSelf=shushiSkill113_2c,replay=True,knockback=1,description="Inflige une série d'attaque sur l'ennemi ciblé. Les dégâts infligés sur l'armure sont augmentés")
shushiSkill113_1c = effect("Enchaînement - {replicaName}","shushiSkill113_2c",replique=shushiSkill113_1,silent=True,emoji=shushiSkill113_2.emoji)
shushiSkill113 = skill("Mikelit","shushiSkill113",TYPE_DAMAGE,emoji='<:mikelit:988360135485313085>',range=AREA_CIRCLE_1,use=MAGIE,needEffect=shushiMikel,damageOnArmor=2,power=25,repetition=2,effectOnSelf=shushiSkill113_1c,replay=True,knockback=1,description="Inflige une série d'attaque sur l'ennemi ciblé. Les dégâts infligés sur l'armure sont augmentés")
shushiMipoi = effect("Mipoi","mipoi",turnInit=5,silent=True,emoji='<:mipoi:988360255413039124>')
shushiSkill121 = skill("Mipoitau","shushiSkill121",TYPE_DAMAGE,emoji="<:mipoitau:988360402201108511>",power=150,range=AREA_INLINE_3,area=AREA_CIRCLE_1,use=MAGIE,tpCac=True,description="Saute sur l'ennemi ciblé et inflige des dégâts de zone",needEffect=shushiMipoi)
shushiSkill122 = skill("Mipoicou","shushiSkill122",TYPE_DAMAGE,emoji="<:mipoitou:988360468496273488>",power=80,repetition=3,use=MAGIE,range=AREA_MONO,area=AREA_CIRCLE_2,description=triSlashdown.description,needEffect=shushiMipoi,damageOnArmor=triSlashdown.onArmor,accuracy=90)
shushiSkill123 = skill("Mipoidyu","shushiSkill123",TYPE_DAMAGE,emoji='<:mipoityu:988360346102292520>',power=80,range=AREA_CIRCLE_1,area=AREA_CONE_2,accuracy=135,repetition=3,use=MAGIE,description="Inflige des dégâts à trois reprises dans la zone ciblé, avec une bonne précision",needEffect=shushiMipoi)

shushiMisil = effect("Misil","misil",turnInit=5,silent=True,emoji='<:misil:988359552619671592>')
shushiSkill131Eff1, shushiSkill131Eff2 = copy.deepcopy(incurable), copy.deepcopy(armorGetMalus)
shushiSkill131Eff1.power = shushiSkill131Eff2.power = 50
shushiSkill131Eff1.turnInit = shushiSkill131Eff2.turnInit = 3
shushiSkill131 = skill("Misilcil","shushiSkill131",TYPE_DAMAGE,emoji='<:misilcil:988359764960489482>',needEffect=shushiMisil,use=MAGIE,effects=[shushiSkill131Eff1, shushiSkill131Eff2],power=150,range=AREA_CIRCLE_3,tpCac=True,description="Saute sur l'ennemi ciblé et lui inflige des dégâts tout en réduisant les soins et armures qu'il reçoit pendant un moment")
shushiSkill132Eff = copy.deepcopy(dmgDown)
shushiSkill132Eff.power, shushiSkill132Eff.turnInit = 15, 3
shushiSkill132 = skill("Misilcol","shushiSkill132",TYPE_DAMAGE,power=125,emoji="<:misilcol:988359700930261022>",needEffect=shushiMisil,range=AREA_MONO,area=AREA_CIRCLE_2,damageOnArmor=1.5,effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_2,shushiSkill132Eff],use=MAGIE,description="Inflige des dégâts autour de vous (dégâts accrus contre l'armure) et réduit les dégâts infligés par les ennemis dans la zone d'effet")
shushiSkill133Eff = copy.deepcopy(deepWound)
shushiSkill133Eff.power, shushiSkill133Eff.stat = 40, MAGIE
shushiSkill133 = skill("Misiltal","shushiSkill133",TYPE_DAMAGE,power=125,emoji='<:misiltal:988359632055595008>',needEffect=shushiMisil,range=AREA_MONO,area=AREA_CIRCLE_2,effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_2,shushiSkill133Eff],use=MAGIE,description="Inflige des dégâts et {0} aux ennemis alentour".format(shushiSkill133Eff))

shushiMi = effect("Mi","mi",turnInit=5,silent=True,emoji='<:mi:988359489210175528>')
shushiSkill11 = skill(shushiMikel.name,"shushiSkill11",TYPE_DAMAGE,power=125,needEffect=shushiMi,effectOnSelf=shushiMikel,use=MAGIE,range=AREA_CIRCLE_1,percing=10,emoji=shushiMikel.emoji[0][0],description="Inflige des dégâts à l'ennemi ciblé en ignorant une partie de sa résistance et vous donne accès à des compétences offensives monocibles")
shushiSkill12 = skill(shushiMipoi.name,"shushiSkill12",TYPE_DAMAGE,power=100,needEffect=shushiMi,effectOnSelf=shushiMipoi,use=MAGIE,range=AREA_CIRCLE_2,area=AREA_CIRCLE_1,percing=10,emoji=shushiMikel.emoji[0][0],description="Inflige des dégâts aux ennemis ciblés en ignorant une partie de sa résistance et vous donne accès à des compétences offensives de zone")
shushiSkill13Eff = effect(shushiMisil.name,"shushiSkill13Eff",MAGIE,type=TYPE_DAMAGE,area=AREA_DONUT_2,power=60,emoji=shushiMisil.emoji,trigger=TRIGGER_INSTANT)
shushiSkill13 = skill(shushiMisil.name,"shushiSkill13",TYPE_DAMAGE,power=100,needEffect=shushiMi,effects=shushiSkill13Eff,effectOnSelf=shushiMisil,use=MAGIE,range=AREA_CIRCLE_2,area=AREA_CIRCLE_1,percing=10,emoji=shushiMisil.emoji[0][0],description="Inflige des dégâts à l'ennemi ciblé puis des dégats aux ennemis et vous donnes accès à des compétences offensives infligeant des dégâts aux ennemis")

shushiSkill1_1 = skill(shushiMi.name, "shushiSkill1_1", TYPE_DAMAGE,power=80,range=AREA_CIRCLE_1,use=MAGIE,effectOnSelf=shushiMi,rejectEffect=[shushiMikel,shushiMipoi,shushiMisil,shushiMi],emoji=shushiMi.emoji[0][0],description="Inflige des dégâts à l'ennemi ciblé et vous permet d'utiliser des compétences tornées offensivement")
shushiSkill1 = skill("Combinaison - Mi","shushiSkill1",TYPE_DAMAGE,become=[shushiSkill1_1,shushiSkill11,shushiSkill12,shushiSkill13,shushiSkill111,shushiSkill112,shushiSkill113,shushiSkill121,shushiSkill123,shushiSkill131,shushiSkill132,shushiSkill133],emoji=shushiSkill1_1.emoji)

shushiShiah = effect("Shihay","shiah",turnInit=5,silent=True,emoji='<:shiha:988365794159263774>')
shushiSkill211e = copy.deepcopy(deepWound)
shushiSkill211e.stat, shushiSkill211e.power = MAGIE, 20
shushiSkill211 = skill("Shihaytal","shushiSkill211",TYPE_DAMAGE,emoji="<:shihaytal:988366029413568532>",needEffect=shushiShiah,effects=shushiSkill211e,power=120,lifeSteal=50,aoeLifeSteal=20,use=MAGIE,range=AREA_CIRCLE_2,description="Inflige des dégâts à l'ennemi ciblé en lui volant de la vie. Soigne aussi les alliés proches, en fonction des dégâts infligés. Inflige également {0} à la cible.".format(shushiSkill211e),effPowerPurcent=150)
shushiSkill212 = skill("Shihayto","shushiSkill212",TYPE_DAMAGE,emoji="<:shihayto:988365942234947655>",needEffect=shushiShiah,effects=shushiSkill211e,power=95,lifeSteal=50,aoeLifeSteal=35,use=MAGIE,range=AREA_CIRCLE_2,area=AREA_CIRCLE_1,description="Inflige des dégâts aux ennemis ciblés en leur volant de la vie. Soigne aussi les alliés proches, en fonction des dégâts infligés. Inflige également {0} à la cible principale".format(shushiSkill211e),effPowerPurcent=135)

shushiSkill213_2 = skill("Shihaytu","shushiSkill213",TYPE_DAMAGE,emoji="<:shihaytu:988365873658101780>",power=40,area=AREA_CIRCLE_1,range=AREA_CIRCLE_3,tpCac=True,use=MAGIE,lifeSteal=35,aoeLifeSteal=20,description="Inflige une attaque en arc de cercle vers l'ennemi ciblé, une attaque autour de vous repoussant les ennemis et saute sur l'ennemi ciblé pour infliger une nouvelle attaque de zone. Chaque attaque vous soigne vous et vous alliés proches en fonction des dégâts infligés. Inflige {0} aux ennemis proches après la dernière attaque".format(shushiSkill211e),effectAroundCaster=[TYPE_MALUS,AREA_DONUT_2,shushiSkill211e])
shushiSkill213_2c = effect("Enchaînement - {replicaName}","shushiSkill213_2c",silent=True,emoji=shushiSkill213_2.emoji,replique=shushiSkill213_2)
shushiSkill213_1 = skill(shushiSkill213_2.name,shushiSkill213_2.id,TYPE_DAMAGE,power=40,areaOnSelf=True,use=MAGIE,area=AREA_CIRCLE_2,range=AREA_CIRCLE_1,knockback=1,affSkillMsg=False,replay=True,effectOnSelf=shushiSkill213_2c,emoji=shushiSkill213_2.emoji,description=shushiSkill213_2.description,lifeSteal=35,aoeLifeSteal=20)
shushiSkill213_1c = effect("Enchaînement - {replicaName}","shushiSkill213_1c",silent=True,emoji=shushiSkill213_1.emoji,replique=shushiSkill213_1)
shushiSkill213 = skill(shushiSkill213_2.name,shushiSkill213_2.id,TYPE_DAMAGE,emoji=shushiSkill213_1.emoji,needEffect=shushiShiah,effects=shushiSkill211e,power=35,lifeSteal=35,aoeLifeSteal=35,use=MAGIE,range=AREA_MONO,area=AREA_ARC_2,description=shushiSkill213_1.description,effectOnSelf=shushiSkill213_1c)

shushiShijal= effect("Shijal","shijal",turnInit=5,silent=True,emoji='<:shijal:988365479678734346>')
shushiSkill221 = skill("Shijalxa","shushiSkill221",TYPE_DAMAGE,emoji="<:shijalxa:988365533239988286>",damageOnArmor=2,needEffect=shushiShiah,power=125,armorSteal=50,armorConvert=35,aoeArmorConvert=20,use=MAGIE,range=AREA_CIRCLE_2,description="Inflige des dégâts à l'ennemi ciblé. Convertie une partie des dégâts infligés en armure pour vous et vos alliés proches. Inflige des dégâts supplmémentaire à l'armure et en vole une partie")
shushiSkill222 = skill("Shijalxe","shushiSkill222",TYPE_DAMAGE,emoji="<:shijalxe:988365607625965628>",damageOnArmor=1.5,needEffect=shushiShiah,power=100,armorSteal=35,armorConvert=35,aoeArmorConvert=20,use=MAGIE,range=AREA_CIRCLE_2,area=AREA_CIRCLE_1,description="Inflige des dégâts aux ennemis ciblés. Convertie une partie des dégâts infligés en armure pour vous et vos alliés proches. Inflige des dégâts supplmémentaire à l'armure et en vole une partie")
shushiSkill223_1 = skill("Shijalxo","shushiSkill223",TYPE_DAMAGE,emoji="<:shijalxo:988365721555828736>",damageOnArmor=2,power=60,range=AREA_CIRCLE_1,area=AREA_LINE_2,garCrit=True,armorSteal=50,armorConvert=35,affSkillMsg=False,aoeArmorConvert=20,use=MAGIE,description="Inflige deux attaques en arc en cercle en direction de l'ennemi ciblé puis une troisième attaque en ligne infligeant un coup critique à la cible principale. Une partie des dégâts est convertie en armure pour vous et vos alliés proches. Inflige des dégâts supplémentaire à l'armure")
shushiSkill223_c = effect("Enchaînement - {replicaName}","shushiSkill223c",silent=True,emoji=shushiSkill223_1.emoji,replique=shushiSkill223_1)
shushiSkill223 = skill("Shijalxo","shushiSkill223",TYPE_DAMAGE,emoji="<:shijalxo:988365721555828736>",damageOnArmor=2,replay=True,needEffect=shushiShiah,power=40,repetition=2,effectOnSelf=shushiSkill223_c,armorSteal=35,armorConvert=20,aoeArmorConvert=20,use=MAGIE,range=AREA_CIRCLE_1,area=AREA_ARC_1,description=shushiSkill223_1.description)
shushiShiquo = effect("Shiquo","shiquo",turnInit=5,silent=True,emoji='<:shiquo:988365365606252574>')
shushiSkill231 = skill("Shiquopat","shushiSkill231",TYPE_DAMAGE,emoji="<:shiquopat:988364858019958855>",needEffect=shushiShiah,power=120,armorSteal=35,armorConvert=35,lifeSteal=35,use=MAGIE,range=AREA_CIRCLE_2,description="Inflige des dégâts à l'ennemi ciblé. Convertie une partie des dégâts infligés en soins et en armure pour vous. Inflige des dégâts supplmémentaire à l'armure et en vole une partie")
shushiSkill232 = skill("Shiquopet","shushiSkill232",TYPE_DAMAGE,emoji="<:shiquopet:988365028174467082>",needEffect=shushiShiah,power=100,armorSteal=35,armorConvert=35,lifeSteal=35,use=MAGIE,range=AREA_CIRCLE_2,area=AREA_CIRCLE_1,description="Inflige des dégâts aux ennemis ciblés. Convertie une partie des dégâts infligés en soins et en armure pour vous. Inflige des dégâts supplmémentaire à l'armure et en vole une partie")
shushiSkill233_2 = skill("Shiquopot","shushiSkill233",TYPE_DAMAGE,emoji="<:shiquopot:988365099486044170>",power=40,area=AREA_LINE_2,knockback=1,use=MAGIE,garCrit=True,armorSteal=30,armorConvert=35,lifeSteal=35,affSkillMsg=False,range=AREA_CIRCLE_1,description="Inflige une succession d'attaque en direction de l'ennemi ciblé, avec un taux de vol de vie et en convertissant une partie des dégâts infligés en armure. La dernière attaque est forcément critique et repousse la cible")
shushiSkill233_2c = effect("Enchaînement - {replicaName}","shushiSkill233_2c",silent=True,emoji=shushiSkill233_2.emoji,replique=shushiSkill233_2)
shushiSkill233_1 = skill(shushiSkill233_2.name,shushiSkill233_2.id,TYPE_DAMAGE,emoji=shushiSkill233_2.emoji,power=15,repetition=4,armorConvert=10,armorSteal=10,lifeSteal=10,use=MAGIE,range=shushiSkill233_2.range,description=shushiSkill233_2.description,affSkillMsg=False,effectOnSelf=shushiSkill233_2c,replay=True)
shushiSkill233_1c = effect("Enchaînement - {replicaName}","shushiSkill233_1c",silent=True,emoji=shushiSkill233_1.emoji,replique=shushiSkill233_1)
shushiSkill233 = skill(shushiSkill233_2.name,shushiSkill233_2.id,TYPE_DAMAGE,emoji=shushiSkill233_2.emoji,needEffect=shushiShiah,power=30,armorSteal=20,armorConvert=20,lifeSteal=20,use=MAGIE,range=shushiSkill233_2.range,area=AREA_ARC_1,description=shushiSkill233_2.description,effectOnSelf=shushiSkill233_1c,replay=True)

shushiShi = effect("Shi","shi",turnInit=5,silent=True,emoji='<:shi:988364800629276712>')
shushiSkill21 = skill(shushiShiah.name,"shushiSkill21",TYPE_DAMAGE,power=shushiSkill11.power,needEffect=shushiShi,range=AREA_CIRCLE_1,emoji=shushiShiah.emoji[0][0],effectOnSelf=shushiShiah,description="Inflige des dégâts à l'ennemi ciblé avec un petit taux de vol de vie. Vous permet ensuite d'utiliser des compétences accentuées sur le vol de vie (pour vous et vos alliés proches) et infligeant également {0}".format(deepWound),lifeSteal=50,aoeLifeSteal=35)
shushiSkill22 = skill(shushiShijal.name,"shushiSkill22",TYPE_DAMAGE,power=shushiSkill12.power,needEffect=shushiShi,range=AREA_CIRCLE_1,emoji=shushiShijal.emoji[0][0],effectOnSelf=shushiShijal,description="Inflige des dégâts à l'ennemi ciblé avec un petit taux de convertion des dégâts en armure. Vous permet ensuite d'utiliser des compétences accentuées sur la convertion des dégâts en armure (pour vous et vos alliés proches) et infligeant plus de dégâts contre l'armure",armorConvert=35,aoeArmorConvert=20)
shushiSkill23 = skill(shushiShiquo.name,"shushiSkill23",TYPE_DAMAGE,power=shushiSkill13.power,needEffect=shushiShi,range=AREA_CIRCLE_1,emoji=shushiShiquo.emoji[0][0],effectOnSelf=shushiShiquo,description="Inflige des dégâts à l'ennemi ciblé avec un petit taux de convertion des dégâts en armure et de vol de vie. Vous permet ensuite d'utiliser des compétences accentuées sur la convertion des dégâts en armure et le vol de vie personnel",armorConvert=35,lifeSteal=35)

shushiSkill2_1 = skill(shushiShi.name, "shushiSkill2_1",TYPE_DAMAGE,range=AREA_CIRCLE_1, power=shushiSkill1_1.power-10,lifeSteal=35,armorSteal=35,armorConvert=35,emoji=shushiShi.emoji[0][0],effectOnSelf=shushiShi,rejectEffect=[shushiShi,shushiShiquo,shushiShijal,shushiShiah],description="Inflige des dégâts à l'ennemi ciblé en convertisant une partie des dégâts infligés avec un taux de vol de vie et vous permet d'utiliser des compétences accentués sur la survivabilité (vol de vie, convertion de dégâts en armure)")
shushiSkill2 = skill("Combinaison - Shi","shushiSkill2",TYPE_DAMAGE,become=[shushiSkill2_1,shushiSkill21,shushiSkill22,shushiSkill23,shushiSkill211,shushiSkill212,shushiSkill213,shushiSkill221,shushiSkill222,shushiSkill223,shushiSkill231,shushiSkill232,shushiSkill233],emoji=shushiSkill2_1.emoji,description="Permet d'utliser les compétences liées à la marque Shi, compétences accés sur la survivabilité")

shushiTiCli = effect("Ticli","ticli",emoji='<:ticli:988362274584530965>',turnInit=5,silent=True)
shushiSkill311e1, shushiSkill311e2 = effect("Esquive Accrue","shushuSkill311e1",dodge=15,turnInit=7,counterOnDodge=35), copy.deepcopy(dmgDown)
shushiSkill311e2.power, shushiSkill311e2.turnInit = 35, 3
shushiSkill311 = skill("Ticlipiel","shushiSkill311",TYPE_DAMAGE,power=135,needEffect=shushiTiCli,range=AREA_CIRCLE_1,effectOnSelf=shushiSkill311e1,effectAroundCaster=[TYPE_MALUS,AREA_DONUT_2,shushiSkill311e2],emoji='<:ticlipiel:988362414166798356>',use=MAGIE,percing=10,description="Inflige des dégâts à l'ennemi ciblé en ignorant une partie de sa résistance, accroi votre esquive pendant un long moment et diminue les dégâts infligés par les ennemis alentours durant un moment")
shushiSkill312e = effect("Résistance Réduite","shushiSkill312e",PURCENTAGE,resistance=-10,type=TYPE_MALUS,turnInit=3,stackable=True,emoji='<:ticlipil:988362341827629156>')
shushiSkill312 = skill("Ticlipil","shushiSkill312",TYPE_DAMAGE,needEffect=shushiTiCli,power=20,repetition=5,range=AREA_CIRCLE_2,tpCac=True,effectOnSelf=shushiSkill311e1,effects=shushiSkill312e,emoji='<:ticlipil:988362341827629156>',use=MAGIE,description="Inflige à cinq reprises des dégâts à l'ennemi ciblé. Chaque coup porté réduit sa résistance durant un moment. Accroi également votre esquive durant un long moment")
shushiSkill313e1, shushiSkill313e2, shushiSkill313e3, shushiSkill313e4 = copy.deepcopy(incurable), copy.deepcopy(armorGetMalus), copy.deepcopy(incurable), copy.deepcopy(armorGetMalus)
shushiSkill313e1.power, shushiSkill313e2.power, shushiSkill313e3.power, shushiSkill313e4.power =  50, 50, 30, 30
shushiSkill313e1.turnInit = shushiSkill313e2.turnInit = shushiSkill313e3.turnInit = shushiSkill313e4.turnInit = 3
shushiSkill313e5, shushiSkill313e6 = effect("Ticlipiol","ticlipiol1",trigger=TRIGGER_INSTANT,type=TYPE_MALUS,callOnTrigger=shushiSkill313e3,area=AREA_DONUT_1,emoji='<:ticlipiol:988362511269130261>'), effect("Ticlipiol","ticlipiol2",trigger=TRIGGER_INSTANT,type=TYPE_MALUS,callOnTrigger=shushiSkill313e4,area=AREA_DONUT_1,emoji='<:ticlipiol:988362511269130261>')
shushiSkill313 = skill(shushiSkill313e5.name,"shushiSkill313",TYPE_DAMAGE,needEffect=shushiTiCli,power=100,garCrit=True,range=AREA_CIRCLE_1,effectOnSelf=shushiSkill311e1,effects=[shushiSkill313e1,shushiSkill313e2,shushiSkill313e5,shushiSkill313e6],emoji=shushiSkill313e5.emoji[0][0],use=MAGIE,description="inflige une attaque critique à l'ennemi ciblé, et réduit de **{0}%** les soins et armures qu'il reçoit durant un moment. Réduit également de **{1}%** les soins et armures reçus par les ennemis autour de la cible pour la même durée et accroi votre esquive pendant un long moment".format(shushiSkill313e1.power,shushiSkill313e3.power))

shushiTisen = effect("Tisen","tisen",emoji='<:ticli:988362274584530965>',turnInit=5,silent=True)
shushiSkill321e, shushiTisene = effect("Tisenklo","shushiSkill321e",MAGIE,emoji='<:tisenklo:988362689862574181>',magie=5, strength=5, turnInit=3), effect("Bonus de Magie","shushiTisene",PURCENTAGE,magie=20,turnInit=7,emoji=statsEmojis[MAGIE])
shushiSkill321 = skill(shushiSkill321e.name,"shushiSkill321",TYPE_DAMAGE,power=100,range=AREA_CIRCLE_3,needEffect=shushiTisen,area=AREA_CIRCLE_1,tpCac=True,use=MAGIE,emoji=shushiSkill321e.emoji[0][0],effectAroundCaster=[TYPE_BOOST,AREA_DONUT_3,shushiSkill321e],effectOnSelf=shushiTisene,description="Saute sur l'ennem ciblé et inflige des dégâts de zone autour de lui. Augmente la Force et la Magie des alliés alentours durant un petit moment et accroi votre propre Magie de **{0}%** durant un long moment".format(shushiTisene.magie))
shushiSkill322e = effect('Tisenplo',"shushiSkill322e",MAGIE,emoji="<:tisenplo:988362818766143498>",endurance=3,turnInit=3)
shushiSkill322 = skill(shushiSkill322e.name,"shushiSkill322",TYPE_DAMAGE,power=35,setAoEDamage=True,needEffect=shushiTisen,area=AREA_ALL_ENEMIES,range=AREA_MONO,use=MAGIE,effectOnSelf=shushiTisene,effectAroundCaster=[TYPE_BOOST,AREA_ALL_ALLIES,shushiSkill322e],emoji=shushiSkill322e.emoji[0][0],description="Inflige des dégâts à tous les ennemis en ignorant la réduction des dégâts de zone, accroi l'Endurance de tous vos alliés (vous incluts) durant un petit moment et augmente votre propre Magie de **{0}%** durant un long moment".format(shushiTisene.magie))
shushiSkill323e1, shushiSkill323e2 = copy.deepcopy(defenseUp), copy.deepcopy(vulne)
shushiSkill323e1.power = shushiSkill323e2.power = 10 
shushiSkill323e1.turnInit = shushiSkill323e2.turnInit = 3
shushiSkill323_1 = skill("Tisenshi","shushiSkill323",TYPE_DAMAGE,emoji='<:tisenshi:988362763216748544>',power=60,range=AREA_MONO,area=AREA_CIRCLE_2,use=MAGIE,effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_2,shushiSkill323e2],effectOnSelf=shushiTisene,description="Inflige des dégâts aux ennemis environnants à deux reprises, réduit les dégâts subis par les alliés proches et augmente les dégâts subis par les ennemis alentours durant un petit moment. Accroi également votre propre Magie de **{0}%** durant un long moment".format(shushiTisene.magie))
shushiSkill323_c = effect("Enchaînement - {replicaName}","shushiSkill323_c",silent=True,replique=shushiSkill323_1)
shushiSkill323 = skill("Tisenshi","shushiSkill323",TYPE_DAMAGE,emoji='<:tisenshi:988362763216748544>',range=AREA_MONO,power=60,area=AREA_CIRCLE_2,use=MAGIE,effectAroundCaster=[TYPE_MALUS,AREA_CIRCLE_2,shushiSkill323e1],needEffect=shushiTisen,replay=True,effectOnSelf=shushiSkill323_c,description=shushiSkill323_1.description)

shushiTiwal = effect("Tiwal","tiwal",emoji='<:tiwal:988363057292005427>',turnInit=5,silent=True)
shushiSkill331e1, shushiSkill331e2 = effect("Tiwafel","shushiSkill331e1",MAGIE,type=TYPE_INDIRECT_HEAL,power=25,turnInit=4,emoji='<:tiwalfel:988363277903998986>',trigger=TRIGGER_START_OF_TURN), effect("Tiwafel","shushiSkill331e2",MISSING_HP,type=TYPE_INDIRECT_HEAL,power=12,turnInit=4,emoji='<:tiwalfel:988363277903998986>',trigger=TRIGGER_START_OF_TURN)
shushiSkill331 = skill("Tiwafel","shushiSkill331",TYPE_DAMAGE,power=100,range=AREA_MONO,area=AREA_CIRCLE_2,effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_DONUT_2,shushiSkill331e1],effectOnSelf=shushiSkill331e2,emoji=shushiSkill331e1.emoji[0][0],use=MAGIE,needEffect=shushiTiwal,description="Inflige des dégâts aux ennemis autours avec un petit taux de vol de vie personnel. Octroie un effet régénérant aux alliés proches et vous octroie un autre effet régénérant, vous soignant en fonction de vos PV manquants en fin de tour",lifeSteal=25)
shushiSkill332e = effect("Tiwagel","shushiSkill332e",PURCENTAGE,overhealth=10,turnInit=7,emoji='<:tiwalgel:988363208576335872>',type=TYPE_ARMOR)
shushiSkill332 = skill(shushiSkill332e.name,"shushiSkill332",TYPE_DAMAGE,needEffect=shushiTiwal,power=100,range=AREA_MONO,area=AREA_CIRCLE_2,effectAroundCaster=[TYPE_ARMOR,AREA_CIRCLE_2,shushiSkill332e],emoji=shushiSkill332e.emoji[0][0],use=MAGIE,armorConvert=25,description="Inflige des dégâts aux ennemis alentours, et octroie aux alliés alentours et vous-même une armure équivalante à **{0}%** de vos PV Maximums".format(shushiSkill332e.overhealth))
shushiSkill333e1, shushiSkill333e2 = copy.deepcopy(constEff), copy.deepcopy(absEff)
shushiSkill333e1.power, shushiSkill333e1.stat, shushiSkill333e1.turnInit = 20, PURCENTAGE, 3
shushiSkill333e2.power, shushiSkill333e2.turnInit = shushiSkill333e1.power, shushiSkill333e1.turnInit
shushiSkill333_1 = skill("Tiwawel","shushiSkill333",TYPE_DAMAGE,power=65,garCrit=True,effectAroundCaster=[TYPE_BOOST,AREA_MONO,shushiSkill333e1],use=MAGIE,range=AREA_CIRCLE_1,description="Inflige deux attaques à l'ennemi (la seconde est forcément critique). Augmente également vos PV maximums et vos soins reçus de **{0}%** durant un moment".format(shushiSkill333e1.power),emoji='<:tiwalwel:988363155258368050>')
shushiSkill333_c = effect("Enchaînement - {replicaName}","shushiSkill333_c",replique=shushiSkill333_1,silent=True)
shushiSkill333 = skill("Tiwawel","shushiSkill333",TYPE_DAMAGE,power=65,needEffect=shushiTiwal,area=AREA_ARC_1,effectAroundCaster=[TYPE_BOOST,AREA_MONO,shushiSkill333e2],use=MAGIE,range=AREA_CIRCLE_1,description=shushiSkill333_1.description,emoji=shushiSkill333_1.emoji,effectOnSelf=shushiSkill333_c,replay=True)

shushiTi = effect("Ti","ti",emoji='<:ti:988362222550016010>',turnInit=5,silent=True)
shushiSkill31 = skill(shushiTiCli.name,"shushiSkill31",TYPE_DAMAGE,needEffect=shushiTi,power=85,range=AREA_CIRCLE_1,emoji=shushiTiCli.emoji[0][0],use=MAGIE,effectOnSelf=shushiTiCli,lifeSteal=35,description="Inflige des dégâts à l'ennmi ciblé avec un petit taux de vol de vie, et vous donne accès à des compétences accentué sur l'entrave des adversaires")
shushiSkill32 = skill(shushiTisen.name,"shushiSkill32",TYPE_DAMAGE,needEffect=shushiTi,power=85,range=AREA_CIRCLE_1,emoji=shushiTisen.emoji[0][0],use=MAGIE,effectOnSelf=shushiTisen,lifeSteal=35,description="Inflige des dégâts à l'ennmi ciblé avec un petit taux de vol de vie, et vous donne accès à des compétences accentué sur les bonus de statistiques")
shushiSkill33 = skill(shushiTiwal.name,"shushiSkill33",TYPE_DAMAGE,needEffect=shushiTi,power=85,range=AREA_CIRCLE_1,emoji=shushiTiwal.emoji[0][0],use=MAGIE,effectOnSelf=shushiTiwal,lifeSteal=35,description="Inflige des dégâts à l'ennmi ciblé avec un petit taux de vol de vie, et vous donne accès à des compétences accentué sur la régénération et l'armure")

shushiSkill3_1 = skill(shushiTi.name,"shushiSkill3",TYPE_DAMAGE,power=70,range=AREA_CIRCLE_2,area=AREA_CIRCLE_1,effectOnSelf=shushiTi,use=MAGIE,emoji=shushiTi.emoji[0][0],description="Inflige des dégâts aux ennemis ciblés et vous permet d'utiliser des compétences orientés soutiens",rejectEffect=[shushiTi,shushiTiwal,shushiTisen,shushiTisen])
shushiSkill3 = skill("Combinaison Ti","shushiSkill3",TYPE_DAMAGE,become=[shushiSkill3_1,shushiSkill31,shushiSkill311,shushiSkill312,shushiSkill313,shushiSkill32,shushiSkill321,shushiSkill322,shushiSkill323,shushiSkill33,shushiSkill331,shushiSkill332,shushiSkill333],emoji=shushiSkill3_1.emoji)

for tmpSkill in [shushiSkill1,shushiSkill2,shushiSkill3]:
    for indx, tmpSkill2 in enumerate(tmpSkill.become):
        if tmpSkill2.use != MAGIE: tmpSkill.become[indx].use = MAGIE

sixtineStuff1 = stuff("Barette Rompiche","sixtineStuff1",0,magie=80,intelligence=100,endurance=5,resistance=10,strength=10,charisma=20,agility=15,precision=25,emoji=sixitneBarrette.emoji)
sixtineStuff2 = stuff("Pull en Laine","sixtineStuff2",1,magie=80,intelligence=100,endurance=10,resistance=10,strength=10,charisma=20,agility=20,precision=25,emoji=sixitnePull.emoji)
sixtineStuff3 = stuff("Tennis montantes bleues","sixtineStuff3",2,magie=80,intelligence=100,endurance=5,resistance=10,strength=10,charisma=20,agility=15,precision=25,emoji=blackBlueSnelers.emoji)
sixtineWeap = weapon("Rapière Onirique","sixtineExWeap",RANGE_DIST,AREA_CIRCLE_3,power=85,accuracy=100,ignoreAutoVerif=True,emoji=dSixtineWeap.emoji,priority=WEAPON_PRIORITY_LOWEST,magie=20,intelligence=20)
sixtineCardEff = effect("Jeu de carte","sixtineCardEff",type=TYPE_BOOST,turnInit=-1,trigger=TRIGGER_START_OF_TURN,emoji=cardsDeck.emoji)
cardValueNames, cardColorNames = ["Six de","Sept de","Huit de","Neuf de","Dix de","Valet de","Dame de","Roi de","As de"], ["Pique","Trèfle","Coeur","Carreau"]
cardEmojiTabl = ["🂦","🂧","🂨","🂩","🂪","🂫","🂬","🂭","🂡", "🂶","🂷","🂸","🂹","🂺","🂻","🂼","🂽","🂾","🂱","🃆","🃇","🃈","🃉","🃊","🃋","🃌","🃍","🃎","🃁","🃖","🃗","🃘","🃙","🃚","🃛","🃜","🃝","🃞","🃑"]
playSixtineCard, sixtineSkill1_1c, sixtineSkill1_2c = effect("Tirage","sixtinePlayCard",trigger=TRIGGER_INSTANT,emoji='<:redraw:1205542192828125284>'), effect("Tirage Rapide épuisé","redrawOut",emoji='<:redrawout:1205542505781796924>',turnInit=3,silent=True,type=TYPE_MALUS), effect("Grand Tirage épuisé","bigRedrawOut",emoji='<:greatdrawout:1205542382960123924>',turnInit=5,silent=True,type=TYPE_MALUS)
playSixtineCard.iaPow = 50
sixtineSkill1_1 = skill("Tirage Rapide","sixtineSkill1",TYPE_BOOST,effects=playSixtineCard,rejectEffect=sixtineSkill1_1c,effectOnSelf=sixtineSkill1_1c,range=AREA_MONO,emoji='<:redraw:1205542192828125284>',description="Permet de tirer une carte de votre deck supplémentaire et vous permet de rejouer votre tour. Ne peux pas être réutilisé durant trois tours",replay=True)
sixtineSkill1_2 = skill("Grand Tirage","sixtineSkill1",TYPE_BOOST,effects=[playSixtineCard,playSixtineCard,playSixtineCard],rejectEffect=sixtineSkill1_2c,effectOnSelf=sixtineSkill1_2c,range=AREA_MONO,emoji='<:greatdraw:1205542317612597388>',description="Permet de tirer trois carte de votre deck supplémentaire. Ne peux pas être réutilisé durant cinq tours")
sixtineSkill1 = skill("Deck de Jeu","sixtineSkill1",TYPE_PASSIVE,effects=sixtineCardEff,become=[sixtineSkill1_1,sixtineSkill1_2],emoji=sixtineCardEff.emoji[0][0],description="À chaque début de tour, Sixtine tire une carte d'un deck de 36 cartes, et joue les cartes tirées à la fin de son tour\nL'effet des cartes dépends de sa valeur et sa couleur\n\nPermet aussi d'utiliser {0} et {1}, deux compétences permettant de tirer des cartes supplémentaires\n\nSi toutes les cartes sont épuisés, le deck est remélangé".format(sixtineSkill1_1,sixtineSkill1_2))
sixtineSkill1.initCooldown = 1
sixtineSkill2_e3 = effect("Réveil Soudain","sixtineSkill2_e3",MAGIE,power=50,trigger=TRIGGER_INSTANT,type=TYPE_INDIRECT_DAMAGE,emoji=sixtineUltEff3.emoji)
sixtineSkill2_e2, sixtineSkill2_e1 = effect("Somnolence","sixtineSkill2_e2",type=TYPE_MALUS,callOnTrigger=sixtineSkill2_e3,trigger=TRIGGER_DAMAGE,lvl=1,turnInit=3,emoji="<:sixtyCombo1:1098615843048399022>"), effect("Soporique","sixtineSkill2_e1",INTELLIGENCE,strength=-5,magie=-5,charisma=-3,intelligence=-3,resistance=-2,turnInit=3,type=TYPE_MALUS,emoji=sixtineUlt.emoji)
sixtineSkill2 = skill("Sommeil","sixtineSkill2",TYPE_MALUS,area=AREA_CIRCLE_3,effects=[sixtineSkill2_e1,sixtineSkill2_e2],emoji=sixtineSkill2_e2.emoji[0][0],cooldown=5,description="Réduit les statistiques des ennemis ciblés. De plus, la prochaine fois qu'ils reçoivent des dégâts directs, leur inflige une autre attaque indirecte")
sixtineSkill3e1, sixtineSkill3e2 = effect("Poussière d'étoile","sixtineSkill3e1",INTELLIGENCE,overhealth=35,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE), effect("Vent Cosmique","sixtineSkill3e2",MAGIE,power=30,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN)
sixtineSkill3 = skill("Dualité Cosmique","sixtineSkill3",TYPE_ARMOR,effects=[sixtineSkill3e1, sixtineSkill3e2],emoji='<:sixtineSkill2:1205624341488865290>',cooldown=3,description="Octroie une armure et un effet de régénération aux alliés ciblés",area=AREA_CIRCLE_2)
sixtineSkill4_1e1, sixtineSkill4_1e2 = copy.deepcopy(dmgUp), copy.deepcopy(defenseUp)
sixtineSkill4_1e1.power = sixtineSkill4_1e2.power = 20
sixtineSkill4_1e1.turnInit = sixtineSkill4_1e2.turnInit = 3
sixtineSkill4_1 = skill("Bonne étoile","sixtineSkill4",TYPE_BOOST,area=AREA_CIRCLE_2,effects=[sixtineSkill4_1e1, sixtineSkill4_1e2],cooldown=3,emoji='<:sixtineSkill3_1:1205624733987766333>',description="Augmente les dégâts infligés et réduits les dégâts reçus par les alliés ciblés de **{0}%** durant un petit moment".format(sixtineSkill4_1e1.power))
sixtineSkill4_2 = skill("Supernova","sixtineSkill4",TYPE_DAMAGE,use=MAGIE,cooldown=sixtineSkill4_1.cooldown,area=sixtineSkill4_1.area,power=150,aoeArmorConvert=25,armorConvert=50,emoji='<:sixtineSkill3_2:1205629279480844349>',description="Inflige des dégâts aux ennemis ciblés, octryant une armure en fonction des dégâts infligés aux alliés proches et à vous même",damageOnArmor=3)
sixtineSkill4 = skill("Puissance Cosmique","sixtineSkill4",TYPE_BOOST,become=[sixtineSkill4_1,sixtineSkill4_2],emoji=sixtineSkill4_1.emoji)

clemExStuffeff = copy.deepcopy(dmgUp)
clemExStuffeff.power, clemExStuffeff.turnInit, clemExStuffeff.unclearable = 25, -1, True

clemExStuff1 = stuff("Chapeau du Mage écarlate","clemExStuff0",0,strength=100,endurance=120,charisma=50,agility=75,precision=75,intelligence=100,magie=650,resistance=10,percing=15,effects=clemExStuffeff)
clemExStuff2 = stuff("Robe du Mage écarlate","clemExStuff1",0,strength=100,endurance=120,charisma=50,agility=75,precision=75,intelligence=100,magie=650,resistance=20,percing=10)
clemExStuff3 = stuff("Bottines du Mage écarlate","clemExStuff2",0,strength=100,endurance=120,charisma=50,agility=75,precision=75,intelligence=100,magie=650,resistance=15,percing=15)
clemExBloodMissiles = skill("Missiles Sanguins","clemExBloodMissiles",TYPE_DAMAGE,power=75,area=AREA_RANDOMENNEMI_5,repetition=4,emoji=bloodmissiles.emoji,cooldown=5,use=MAGIE,description="Inflige des dégâts à cinqs ennemis aléatoirement, quatre fois", setAoEDamage=True)


echo = skill("Echo","jadeSkill",TYPE_DAMAGE,0,power=80,use=CHARISMA,useActionStats=ACT_BOOST,emoji='<:requiem:1178936044238942258>',cooldown=3)

zenecaSays=says(
    start="Oubliez pas de respecter les distanciations sociales !",
    ultimate="J'vais vous montrer ce que peut faire quelqu'un de majeur et vacciné ! Oh c'est vrai je suis pas majeure...",
    limiteBreak="C'est... Parti !",
    onKill="Faut pas négliger sa santé tant que ça voyons",
    onResurect="Arf... Merci {caster}",
    blueWinAlive="Prenez ça bande d'anti-vaxs !",
    reactEnnemyKilled="Wooow. C'était pas mal ça !",
    reactAllyLb="Tu leur en a fait voir de toutes les couleurs {caster} !",
    getHealed="Thx"
)

victoireTeleportBehindYou = copy.deepcopy(shortTeleport)
victoireTeleportBehindYou.say = "Nothing personal kid."

victoireSays=says(
    start="Que Dieu nous montre la voie !",
    ultimate="REPENTEZ VOUS !",
    limiteBreak="C'est l'heure du JUGEMENT !",
    onKill="Puisse Dieu te pardonner",
    onResurect="Merci pour ce miracle",
    blueWinAlive="Yupey !",
    takeHit="Prépare-toi pour ma rétribution divine, {caster} !",
    getHealed="J'te remercie pour ta miséricorde, {caster}"
)

alexandreSays=says(
    start="Qui veut se prendre un bon coup de marteau ?",
    ultimate="Voyez ! Ceci est le pouvoir des nains ?",
    takeHit="Ah ! Il va falloir faire mieux que ça pour me faire tomber !",
    blueWinAlive="Ahah ! C'est tout ce que vous savez faire ?",
    reactAllyKilled="Hé bah {target}, on fatigue ?"
)

jadeSays = says(
    start = "Evitez de trop en faire cette fois...",
    ultimate="Bouchez vous les oreilles !",
    blueWinAlive="`Fredonne joyeusement`",
    reactEnnemyKilled="Ew...",
    onKill="Désolée..."
)

heleneSays= says(
    start="Et c'est qui qui va encore vous sauver le cul ? Ewi c'est mwaaaa. Sérieusement...",
    ultimate="Tu me donne vraiment trop de taff supplémentaire {target}, tu sais ?",
    limiteBreak="Ok là je suis à bout.",
    onKill="Oh fait pas genre {target}, tu l'as cherché",
    onResurect="Si c'est pas ironique",
    blueWinAlive="Pas trop tôt",blueWinDead="Doooonc vous m'avez fait venir pour rien enfaite ?",
    reactAllyKilled="Huh, tu sais, je peux soigner plein de trucs mais pas la mort",
    getHealed="Tps. Merci.",
    takeHit="Tps."
)

aliceExStuff = [
    stuff("Barrette de la chauve-souris","aliceExStuff1",0,charisma=125,endurance=15,resistance=10,agility=20,precision=35,magie=25),
    stuff("Robe de scène","aliceExStuff2",1,charisma=125,endurance=15,resistance=10,magie=25,agility=20,precision=30),
    stuff("Bottines de scène","aliceExStuff3",2,charisma=125,endurance=15,resistance=10,magie=25,agility=20,precision=35)
]

aliceExWeapEff1 = effect("Chant Motivant","aliceExWeapEff1",CHARISMA,strength=5,magie=5,charisma=3,intelligence=3,silentRemove=True)
aliceExWeapEff = effect("Chanson Motivante","aliceExWeapEff",trigger=TRIGGER_WEAPON_USE,area=AREA_DONUT_5,callOnTrigger=aliceExWeapEff1,emoji=micPink.emoji,turnInit=-1,unclearable=True)
aliceExWeap = weapon("Echo","aliceExWeap",RANGE_DIST,AREA_CIRCLE_4,80,100,charisma=20,effects=aliceExWeapEff,emoji='<:requiem:1178936044238942258>',priority=WEAPON_PRIORITY_LOWEST,use=CHARISMA, message="{0} utilise Echo :")
aliceSong1Eff1 = effect("Chant de la Détermination","aliceSong1eff1",CHARISMA,strength=5,magie=5,silentRemove=True,emoji=aliceDanceEff2.emoji,stackable=True,turnInit=2)
aliceSong1Eff = effect("Chant de la Détermination","aliceSong1Eff",CHARISMA,charisma=5,turnInit=2,trigger=TRIGGER_START_OF_TURN,callOnTrigger=aliceSong1Eff1,emoji=aliceDance.emoji,area=AREA_DONUT_7)
aliceSong1Eff_1 = copy.deepcopy(aliceSong1Eff)
aliceSong1Eff_1.trigger, aliceSong1Eff_1.turnInit = TRIGGER_INSTANT, 1
aliceSong1Eff3 = effect("Rose Rouge","aliceSong1Eff3",turnInit=25,emoji=roseRed.emoji)
aliceSong1Eff2 = effect("Chant en court: Détermination","aliceSong1Eff2",turnInit=aliceSong1Eff.turnInit,trigger=TRIGGER_ON_REMOVE,callOnTrigger=aliceSong1Eff3)
aliceSong1 = skill("Chant de la Détermination","aliceExSkill1",TYPE_BOOST,range=AREA_MONO,effects=[aliceSong1Eff_1,aliceSong1Eff,aliceSong1Eff2],cooldown=aliceSong1Eff.turnInit,emoji=aliceDance.emoji,description="Entone le Chant de la Détermination, augmentant les statistiques offensives de vos alliés tout en augmentant votre Charisme. À la fin du chant, vous octroie {0}".format(aliceSong1Eff3),rejectEffect=aliceSong1Eff3)

aliceSong2Eff1, aliceSong2Eff2 = copy.deepcopy(constEff), copy.deepcopy(absEff)
aliceSong2Eff1.silentRemove = aliceSong2Eff2.silentRemove = True; aliceSong2Eff1.stat = aliceSong2Eff2.stat = PURCENTAGE; aliceSong2Eff1.power = aliceSong2Eff2.power = 20; aliceSong2Eff1.turnInit = aliceSong2Eff2.turnInit = 2; aliceSong2Eff1.stackable = aliceSong2Eff2.stackable = True
aliceSong2Eff_3, aliceSong2Eff_4 = effect("Chant de l'Apaisement","aliceSong2Eff", turnInit=aliceSong1Eff.turnInit, trigger=TRIGGER_START_OF_TURN, area=AREA_DONUT_7, charisma=5, callOnTrigger=aliceSong2Eff1, emoji=corGra.emoji, stackable=True), effect("Chant de l'Apaisement","aliceSong2Eff", turnInit=aliceSong1Eff.turnInit, trigger=TRIGGER_START_OF_TURN, area=AREA_DONUT_7, callOnTrigger=aliceSong2Eff2, emoji=corGra.emoji, stackable=True)
aliceSong2Eff_1, aliceSong2Eff_2 = copy.deepcopy(aliceSong2Eff_3), copy.deepcopy(aliceSong2Eff_4)
aliceSong2Eff_1.trigger = aliceSong2Eff_2.trigger = TRIGGER_INSTANT; aliceSong2Eff_1.turnInit = aliceSong2Eff_2.turnInit = 1
aliceSong2Eff3 = effect("Rose Bleue","aliceSong2Eff3",turnInit=25,emoji=roseBlue.emoji)
aliceSong3Eff4 = effect("Chant en court: Apaisement","aliceSong2Eff4",turnInit=aliceSong1Eff.turnInit,trigger=TRIGGER_ON_REMOVE,callOnTrigger=aliceSong2Eff3)
aliceSong2 = skill("Chant de l'Apaisement","aliceExSkill1",TYPE_BOOST,range=AREA_MONO,effects=[aliceSong2Eff_1, aliceSong2Eff_2, aliceSong2Eff_3, aliceSong2Eff_4, aliceSong3Eff4],cooldown=aliceSong1Eff.turnInit,emoji=corGra.emoji,description="Entone le Chant de l'appaisement, augmentant Points de Vies et les soins et armures reçus de vos alliés tout en augmentant votre Charisme. À la fin du chant, vous octroie {0}".format(aliceSong2Eff3),rejectEffect=aliceSong2Eff3)

aliceSong3Eff1 = copy.deepcopy(dmgUp)
aliceSong3Eff1.silentRemove, aliceSong3Eff1.power, aliceSong3Eff1.stat, aliceSong3Eff1.turnInit = True, 5, CHARISMA, 2
aliceSong3Eff = effect("Chant de la Volonté","aliceSong3Eff",CHARISMA,charisma=5,turnInit=aliceSong1Eff.turnInit,trigger=TRIGGER_START_OF_TURN,callOnTrigger=aliceSong3Eff1,emoji=aliceFanDanse.emoji,area=AREA_DONUT_7)
aliceSong3Eff_1 = copy.deepcopy(aliceSong3Eff)
aliceSong3Eff_1.trigger, aliceSong3Eff_1.turnInit = TRIGGER_INSTANT, 1
aliceSong3Eff3 = effect("Rose Rose","aliceSong3Eff3",turnInit=25,emoji=rosePink.emoji)
aliceSong3Eff2 = effect("Chant en court: Volonté","aliceSong3Eff2",turnInit=aliceSong1Eff.turnInit,trigger=TRIGGER_ON_REMOVE,callOnTrigger=aliceSong3Eff3)
aliceSong3 = skill("Chant de la Volonté","aliceExSkill1",TYPE_BOOST,range=AREA_MONO,effects=[aliceSong3Eff_1,aliceSong3Eff,aliceSong3Eff2],cooldown=aliceSong1Eff.turnInit,emoji=aliceFanDanse.emoji,description="Entone le Chant de la Volonté, augmentant les dégâts infligés de vos alliés tout en augmentant votre Charisme. À la fin du chant, vous octroie {0}".format(aliceSong3Eff3),rejectEffect=aliceSong3Eff3)

aliceSong4Eff1, aliceSong4Eff2 = effect("Aphotéose","aliceSong4Eff1",CHARISMA,strength=10,magie=10,charisma=5,intelligence=5,emoji='<:aliceSongSkill:977011751075868682>',silentRemove=True), copy.deepcopy(dmgUp)
aliceSong4Eff2.stat, aliceSong4Eff2.power, aliceSong4Eff2.silentRemove = CHARISMA, 7.5, True
aliceSong4Eff_3, aliceSong4Eff_4 = effect("Aphotéose","aliceSong4Eff", turnInit=3, trigger=TRIGGER_START_OF_TURN, area=AREA_DONUT_7, charisma=10, callOnTrigger=aliceSong4Eff1, emoji=onStage.emoji, stackable=True), effect("Aphotéose","aliceSong4Eff", turnInit=3, trigger=TRIGGER_START_OF_TURN, area=AREA_DONUT_7, callOnTrigger=aliceSong4Eff2, emoji=onStage.emoji, stackable=True)
aliceSong4Eff_1, aliceSong4Eff_2 = copy.deepcopy(aliceSong4Eff_3), copy.deepcopy(aliceSong4Eff_4)
aliceSong4Eff_1.trigger = aliceSong4Eff_2.trigger = TRIGGER_INSTANT; aliceSong4Eff_1.turnInit = aliceSong4Eff_2.turnInit = 1
aliceSong4 = skill("Apothéose","aliceExSkill1",TYPE_BOOST,range=AREA_MONO,effects=[aliceSong4Eff_1, aliceSong4Eff_2, aliceSong4Eff_3, aliceSong4Eff_4],cooldown=3,use=CHARISMA,emoji=onStage.emoji,description="Augmente grandement les statistiques et dégâts infligés de vos alliés ainsi que votre Charisme. Nécessite {0}, {1} et {2} pour pouvoir être utilisé".format(aliceSong1Eff3,aliceSong2Eff3,aliceSong3Eff3),needEffect=[aliceSong1Eff3,aliceSong2Eff3,aliceSong3Eff3])
aliceSongBundle = skill("Répertoire","aliceExSkill1",TYPE_BOOST,become=[aliceSong1,aliceSong2,aliceSong3,aliceSong4],emoji=holyVoice.emoji,description="Permet d'utiliser les compétences {0}, {1} et {2}, trois chants boostant vos alliés et votre statistique de Charisma. Une fois les trois chants effectué, vous permet d'utiliser {3}, un chant accroisant énormément le potentiel offensif de vos alliés et votre charisme".format(aliceSong1,aliceSong2,aliceSong3,aliceSong4))

aliceSkill2Eff = effect("Invocation Chauve-Souris II","aliceSkill2Eff",type=TYPE_SUMMON,area=AREA_CIRCLE_3,callOnTrigger=cutyBat,trigger=TRIGGER_INSTANT,emoji=cutyBat.icon[0])
aliceSkill2 = skill("Chant de Raliment","aliceSkill2",TYPE_SUMMON,cooldown=5,effBeforePow=True,range=aliceSkill2Eff.area,nbSummon=3,effectOnSelf=aliceSkill2Eff,emoji='<:batPrincess:1197056891688321094>',invocation=batInvoc,description="Invoque trois {0} et une {1} à vos cotés".format(batInvoc, cutyBat))
aliceSkill3eff = effect("Bouclier de foi","aliceSkill3eff",PURCENTAGE,overhealth=40,turnInit=5,emoji='<:dvinShield:1104496800100003860>',type=TYPE_ARMOR, trigger=TRIGGER_DAMAGE)
aliceSkill3 = skill("Ascendance","aliceSkill3",TYPE_RESURECTION,power=300,use=CHARISMA,range=AREA_CIRCLE_7,emoji='<:dvinRegen:1104496736845713440>',group=SKILL_GROUP_HOLY,maxHpCost=10,description="Réanime l'allié ciblé au prix de 10% de vos PV max et lui octroie une armure",effects=aliceSkill3eff)

clemTmpStuff = [
    stuff("Barrête de la chauve-souris","clemTmpStuff",0,strength=15,endurance=30,charisma=20,agility=30,precision=35,intelligence=50,magie=250,resistance=15,percing=15),
    stuff("Robe gothique rouge","clemTmpStuff",1,strength=15,endurance=30,charisma=20,agility=30,precision=35,intelligence=50,magie=250,resistance=20,percing=20),
    stuff("Bottines à lacet à talon","clemTmpStuff",2,strength=15,endurance=30,charisma=20,agility=30,precision=35,intelligence=50,magie=250,resistance=15,percing=15)
]

clemTmpBloodJauge = copy.deepcopy(bloodJauge)
clemTmpBloodJauge.jaugeValue.conds.append(jaugeConds(INC_START_FIGHT,40))

clemTmpWeapEff = effect("Lien du Sang","clemTmpWeapEff",PURCENTAGE,power=25,area=AREA_LOWEST_HP_ALLIE,trigger=TRIGGER_START_OF_TURN,turnInit=-1,unclearable=True,emoji=bloodButterFlyPassifEff.emoji,description="En début de tour, transfert jusqu'à **{0}%** de vos PV actuels à l'allié le plus blessé. Augmente également de **{0}%** votre taux de vol de vie")
clemTmpWeap = weapon("Fleos Argentum","clemTmpWeap",RANGE_LONG,AREA_CIRCLE_5,power=100,accuracy=100,priority=WEAPON_PRIORITY_NONE,use=MAGIE,magie=20,emoji='<:clemWeap:915358467773063208>',effects=clemTmpWeapEff)
clemTmpSkill1_1 = skill("Missiles Sanguins","clemTmpSkill1",TYPE_DAMAGE,power=55,repetition=2,use=MAGIE,minJaugeValue=20,jaugeEff=clemTmpBloodJauge,replay=True,description="Consomme 20 points de votre {0} pour infliger des dégâts à deux reprises aux ennemis ciblés (coup critique garanti sur la cible principale) et vous permet de rejouer votre tour".format(clemTmpBloodJauge),garCrit=True,area=AREA_CIRCLE_1,emoji='<:bloodMissiles:1180969333929820180>')
clemTmpSkill1_2 = skill("Missiles Magique",clemTmpSkill1_1.id,TYPE_DAMAGE,power=40,repetition=2,use=MAGIE,replay=True,description="Inflige des dégâts à deux reprises à l'ennemi ciblé et vous permet de rejouer votre tour",emoji=magicMissile.emoji)
clemTmpSkill1 = skill("Missiles Magiques",clemTmpSkill1_1.id,TYPE_DAMAGE,become=[clemTmpSkill1_2, clemTmpSkill1_1],emoji=clemTmpSkill1_2.emoji,jaugeEff=clemTmpBloodJauge,description="Vous permet d'utiliser {0}. Si votre {1} est suffisament remplie, permet d'utiliser {2}, une version plus puissante de {0}, à la place".format(clemTmpSkill1_2, clemTmpBloodJauge, clemTmpSkill1_1))
clemTmpSkill2_1Eff = effect("Lance de sang","clemTmpSkill2Eff",trigger=TRIGGER_INSTANT,callOnTrigger=bloodButterfly,area=AREA_CIRCLE_2,emoji='<:bloodlance:1118613536139124776>')
clemTmpSkill2_1 = skill("Lance de Sang","clemTmpSkill2",TYPE_DAMAGE,power=150,area=AREA_CIRCLE_2,effects=clemTmpSkill2_1Eff,emoji=clemTmpSkill2_1Eff.emoji[0][0],cooldown=7,use=MAGIE,minJaugeValue=35,jaugeEff=clemTmpBloodJauge,description="Consomme 35 points de votre {0} pour infliger de lourds dégâts de zone aux ennemis ciblé et leur infliger {1}".format(clemTmpBloodJauge,bloodButterfly))
clemTmpSkill2_2Eff = copy.deepcopy(incurable)
clemTmpSkill2_2Eff.turnInit, clemTmpSkill2_2Eff.power = 3, 30
clemTmpSkill2_2 = skill("Lance Arcanique",clemTmpSkill2_1.id,TYPE_DAMAGE,power=120,area=AREA_CIRCLE_1,cooldown=clemTmpSkill2_1.cooldown,use=MAGIE,effects=clemTmpSkill2_2Eff,emoji='<:dislocation:1052697663402950667>',description="Inflige des dégâts de zone aux ennemis ciblés et réduit de 30% les soins reçus par la cible principale")
clemTmpSkill2 = skill("Lance Arcanique",clemTmpSkill2_1.id,TYPE_DAMAGE,become=[clemTmpSkill2_2, clemTmpSkill2_1],jaugeEff=clemTmpBloodJauge,emoji=clemTmpSkill2_2.emoji,description="Vous permet d'utiliser {0}. Si votre {1} est suffisament remplie, permet d'utiliser {2}, une version plus puissante de {0}, à la place".format(clemTmpSkill2_2, clemTmpBloodJauge, clemTmpSkill2_1))

clemTmpSkill3_3_ne = effect("Magie Arcanique II",'clemTmpSkill3_3_ne',turnInit=5,silent=True,emoji='<:galvaPheonix:946042576413290506>')
clemTmpSkill3_3_1 = skill("Blood Cross","clemTmpSkill3",TYPE_DAMAGE,power=150,area=AREA_INLINE_2,use=MAGIE,emoji='<:clemRay:978376646262403144>',minJaugeValue=20,jaugeEff=clemTmpBloodJauge,needEffect=clemTmpSkill3_3_ne,description="Consomme 20 points de votre {0} pour infliger des dégât aux ennemis ciblés".format(clemTmpBloodJauge))
clemTmpSkill3_3_2 = skill("Foudre Sombre","clemTmpSkill3",TYPE_DAMAGE,power=115,area=AREA_INLINE_2,use=MAGIE,emoji='<:darkThunder:1177705396639649863>',needEffect=clemTmpSkill3_3_ne,description="Infliger des dégât aux ennemis ciblés")
clemTmpSkill3_2_ne = effect("Magie Arcanique I",'clemTmpSkill3_2_ne',turnInit=5,silent=True,emoji='<:infusion:1123148866548662363>')
clemTmpSkill3_2_1 = skill("Blood Eye","clemTmpSkill3",TYPE_DAMAGE,power=135,area=AREA_CIRCLE_1,use=MAGIE,emoji='<:clemBoom:978377130750644224>',minJaugeValue=15,jaugeEff=clemTmpBloodJauge,needEffect=clemTmpSkill3_2_ne,description="Consomme 15 points de votre {0} pour infliger des dégât aux ennemis ciblés".format(clemTmpBloodJauge),effectOnSelf=clemTmpSkill3_3_ne)
clemTmpSkill3_2_2 = skill("Flamme Sombre","clemTmpSkill3",TYPE_DAMAGE,power=105,use=MAGIE,emoji='<:darkFlame:1228795277490655313>',needEffect=clemTmpSkill3_2_ne,description="Infliger des dégât à l'ennemi ciblé",effectOnSelf=clemTmpSkill3_3_ne)
clemTmpSkill3_1_1 = skill("Blood Diamond","clemTmpSkill3",TYPE_DAMAGE,power=125,use=MAGIE,emoji='<:clemMono:978376664822186054>',minJaugeValue=10,jaugeEff=clemTmpBloodJauge,rejectEffect=[clemTmpSkill3_2_ne,clemTmpSkill3_3_ne],description="Consomme 10 points de votre {0} pour infliger des dégât à l'ennemi ciblé".format(clemTmpBloodJauge),effectOnSelf=clemTmpSkill3_2_ne)
clemTmpSkill3_1_2 = skill("Glace Sombre","clemTmpSkill3",TYPE_DAMAGE,power=95,use=MAGIE,emoji='<:darkIce:1177705370102268024>',rejectEffect=[clemTmpSkill3_2_ne,clemTmpSkill3_2_ne],description="Infliger des dégât à l'ennemi ciblé",effectOnSelf=clemTmpSkill3_2_ne)
clemTmpSkill3 = skill("Combo Arcanique",'clemTmpSkill3',TYPE_DAMAGE,become=[clemTmpSkill3_1_2,clemTmpSkill3_1_1,clemTmpSkill3_2_2,clemTmpSkill3_2_1,clemTmpSkill3_3_2,clemTmpSkill3_3_1],emoji='<:infusion:1123148866548662363>',description="Permet d'utiliser le combo {0}, {2} et {4}. En consommant un peu de votre {6}, vous pouvez remplacer ces sorts par des versions améliorés, à savoir {1}, {3} et {5}".format(clemTmpSkill3_1_2,clemTmpSkill3_1_1,clemTmpSkill3_2_2,clemTmpSkill3_2_1,clemTmpSkill3_3_2,clemTmpSkill3_3_1,clemTmpBloodJauge))
clemTmpSkill4Eff = copy.deepcopy(dmgUp)
clemTmpSkill4Eff.power, clemTmpSkill4Eff.stat, clemTmpSkill4Eff.turnInit = 25, None, 3
clemTmpSkill4 = skill("Cercle Arcanique","clemTmpSkill4",TYPE_BOOST,range=AREA_MONO,replay=True,minJaugeValue=10,emoji="<:arcCircle:986615034627113040>",effects=clemTmpSkill4Eff,cooldown=5,description="Augmente vos dégâts infligés de 25% durant un petit moment et vous permet de rejouer votre tour")

clemTmpSkill5_1_1 = skill("Explosion Sanguine","clemTmpSkill5",TYPE_DAMAGE,power=350,area=AREA_CIRCLE_2,cooldown=7,use=MAGIE,ultimate=True,emoji='<:clemCast:978376938286641172>',description="En consommant 35 points de votre {0} et après un tour de chargement, inflige d'énorme dégâts de zones aux ennemis ciblés, ainsi que {1} aux ennemis restant".format(bloodJauge,bloodButterfly),effectAroundCaster=[TYPE_MALUS,AREA_ALL_ENEMIES,bloodButterfly],url=explosion.url)
clemTmpSkill5_1_c = effect("Cast - {replicaName}","clemTmpSkill5_1_c",silent=True,turnInit=2,replique=clemTmpSkill5_1_1)
clemTmpSkill5_1 = copy.deepcopy(clemTmpSkill5_1_1)
clemTmpSkill5_1.power, clemTmpSkill5_1.effectOnSelf, clemTmpSkill5_1.effectAroundCaster, clemTmpSkill5_1.minJaugeValue, clemTmpSkill5_1.jaugeEff, clemTmpSkill5_1.url = 0, clemTmpSkill5_1_c, None, 35, clemTmpBloodJauge, None
clemTmpSkill5_2_1 = skill("Explosion","clemTmpSkill5",TYPE_DAMAGE,power=200,area=AREA_CIRCLE_2,use=MAGIE,cooldown=7,ultimate=True,emoji=explosion.emoji,description="Après un tour de chargement, inflige de gros dégâts de zones aux ennemis ciblés",url=explosion.url)
clemTmpSkill5_2_c = effect("Cast - {replicaName}","clemTmpSkill5_1_c",silent=True,turnInit=2,replique=clemTmpSkill5_2_1,emoji=explosionCast.emoji)
clemTmpSkill5_2 = copy.deepcopy(clemTmpSkill5_2_1)
clemTmpSkill5_2.power, clemTmpSkill5_2.effectOnSelf, clemTmpSkill5_2.url = 0, clemTmpSkill5_2_c, None
clemTmpSkill5 = skill("Explosion","clemTmpSkill5",TYPE_DAMAGE,become=[clemTmpSkill5_2,clemTmpSkill5_1],ultimate=True,emoji=clemTmpSkill5_2.emoji,description="Vous permet d'utiliser {0}. Si votre {1} est suffisament remplie, permet d'utiliser {2}, une version plus puissante de {0}, à la place".format(clemTmpSkill5_2, clemBloodJauge, clemTmpSkill5_1))

iliTmpStuff = [
    stuff("Boucle d'Oreilles Lumineuse","iliTmpSutff",0,strength=50,endurance=175,charisma=100,agility=50,precision=75,intelligence=50,magie=100,resistance=30,critical=-10,emoji='<:lightPldPendant:1216758201488380016>'),
    stuff("Robe Lumineuse","iliTmpSutff",1,strength=50,endurance=175,charisma=135,agility=50,precision=75,intelligence=50,magie=100,resistance=30,critical=-10,emoji='<:lightPldDress:1216620247294021723>'),
    stuff("Sandales Lumineuses Compensées","iliTmpSutff",2,strength=50,endurance=175,charisma=100,agility=50,precision=75,intelligence=50,magie=100,resistance=30,critical=-10,emoji='<:lightPldSandals:1216618164427685898>'),
]

iliTmpWeapEff = effect("Aura de Lumière","iliTmpWeapEff",CHARISMA,area=AREA_CIRCLE_2,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_WEAPON_USE,power=50,aggro=50,block=25,turnInit=-1,unclearable=True,emoji='<:iliShieldStans:1072554524260188285>')
iliTmpWeap = weapon("Bouclier de Lumière","iliTmpWeap",use=CHARISMA,power=80,range=RANGE_MELEE,effectiveRange=AREA_CIRCLE_1,accuracy=100,effects=iliTmpWeapEff,emoji='<:iliShield:975785889512976434>',priority=WEAPON_PRIORITY_LOWEST)
iliTmpSkill1_renfort = effect("Renforcement Magique","iliTmpSkill1_renfort",silent=True,turnInit=3,emoji='<:requiescat:1003026420798328974>',description="Durant trois tours, renforce vos compétences en augmentant leur puissance, portée et zone d'effet")
iliTmpSkill1_4_ne = effect("Combo III","iliTmpSkill1_4_ne",silent=True,turnInit=5,emoji='<:absolution:1236661667497250919>',stackable=True)
iliTmpSkill1_4_1 = skill("Absolution","iliTmpSkill1",TYPE_DAMAGE,power=120,use=CHARISMA, range=AREA_CIRCLE_1, effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_2,50], needEffect=iliTmpSkill1_4_ne, rejectEffect=iliTmpSkill1_renfort, emoji='<:absolution:1236661667497250919>',description="Inflige des dégâts à l'ennemi ciblé et soigne les alliés autour de vous")
iliTmpSkill1_4_2 = skill("Confitéore","iliTmpSkill1",TYPE_DAMAGE,power=150,use=CHARISMA, range=AREA_CIRCLE_4, area=AREA_CIRCLE_1, effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_2,50], needEffect=[iliTmpSkill1_4_ne, iliTmpSkill1_renfort], emoji='<:confiteor:1003026495050096731>',description="Inflige des dégâts aux ennemis ciblés et soigne les alliés autour de vous")
iliTmpSkill1_3_ne = effect("Combo II","iliTmpSkill1_3_ne",silent=True,turnInit=3,emoji='<:alMainCb3:1080150503972950086>')
iliTmpSkill1_3_1 = skill("Autorité","iliTmpSkill1",TYPE_DAMAGE,power=100,use=CHARISMA, range=AREA_CIRCLE_1, effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_2,50], needEffect=iliTmpSkill1_3_ne, rejectEffect=[iliTmpSkill1_renfort, iliTmpSkill1_4_ne], emoji=iliTmpSkill1_3_ne.emoji[0][0], description="Inflige des dégâts à l'ennemi ciblé et soigne les alliés autour de vous")
iliTmpSkill1_3_2 = skill("Lame de Vailliance","iliTmpSkill1",TYPE_DAMAGE,power=130,use=CHARISMA, range=AREA_CIRCLE_4, area=AREA_CIRCLE_1, effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_2,50], rejectEffect= iliTmpSkill1_4_ne, needEffect=[iliTmpSkill1_3_ne, iliTmpSkill1_renfort], emoji='<:vaillance:1003026550112931841>',description="Inflige des dégâts aux ennemis ciblés et soigne les alliés autour de vous")
iliTmpSkill1_2_ne = effect("Combo I","iliTmpSkill1_2_ne",silent=True,turnInit=3,emoji='<:alMainCb2:1080150472406609990>')
iliTmpSkill1_2_1 = skill("Lame Acharnée","iliTmpSkill1",TYPE_DAMAGE,power=90,use=CHARISMA, range=AREA_CIRCLE_1, effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_2,50], needEffect=iliTmpSkill1_2_ne, rejectEffect=[iliTmpSkill1_renfort, iliTmpSkill1_4_ne], effectOnSelf=iliTmpSkill1_3_ne, emoji=iliTmpSkill1_2_ne.emoji[0][0], description="Inflige des dégâts à l'ennemi ciblé et soigne les alliés autour de vous")
iliTmpSkill1_2_2 = skill("Lame de Vérité","iliTmpSkill1",TYPE_DAMAGE,power=120,use=CHARISMA, range=AREA_CIRCLE_4, area=AREA_CIRCLE_1, effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_2,50], rejectEffect= iliTmpSkill1_4_ne, needEffect=[iliTmpSkill1_2_ne, iliTmpSkill1_renfort], effectOnSelf=iliTmpSkill1_3_ne, emoji='<:verite:1003026534090682448>',description="Inflige des dégâts aux ennemis ciblés et soigne les alliés autour de vous")
iliTmpSkill1_1_1 = skill("Lame Rapide","iliTmpSkill1",TYPE_DAMAGE,power=80,use=CHARISMA, range=AREA_CIRCLE_1, effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_2,50], rejectEffect=[iliTmpSkill1_renfort,iliTmpSkill1_2_ne,iliTmpSkill1_3_ne, iliTmpSkill1_4_ne], effectOnSelf=iliTmpSkill1_2_ne, emoji=' <:alMainCb1:1080150415632498788>', description="Inflige des dégâts à l'ennemi ciblé et soigne les alliés autour de vous")
iliTmpSkill1_1_2 = skill("Lame de Foi","iliTmpSkill1",TYPE_DAMAGE,power=110,use=CHARISMA, range=AREA_CIRCLE_4, area=AREA_CIRCLE_1, effectAroundCaster=[TYPE_HEAL,AREA_CIRCLE_2,50], needEffect=iliTmpSkill1_renfort, rejectEffect=[iliTmpSkill1_2_ne,iliTmpSkill1_3_ne, iliTmpSkill1_4_ne], effectOnSelf=iliTmpSkill1_2_ne, emoji='<:foi:1003026514872377346>',description="Inflige des dégâts aux ennemis ciblés et soigne les alliés autour de vous")
iliTmpSkill1 = skill("Maîtrise d'arme",iliTmpSkill1_4_1.id,TYPE_DAMAGE,become=[iliTmpSkill1_1_1,iliTmpSkill1_1_2,iliTmpSkill1_2_1,iliTmpSkill1_2_2,iliTmpSkill1_3_1,iliTmpSkill1_3_2,iliTmpSkill1_4_1,iliTmpSkill1_4_2],emoji=iliTmpSkill1_4_1.emoji)

iliTmpSkill2_2_ne = effect("Bash Lumineux","iliTmpSkill2_2_ne",silent=True,turnInit=5,emoji='<:iliOvlSkill3:1139249659701887027>')
iliTmpSkill2_2 = skill("Lames Lumineuses","iliTmpSkill2",TYPE_DAMAGE, tpBehind=True, areaOnSelf=True, area=AREA_CIRCLE_1, range=AREA_CIRCLE_3, needEffect=iliTmpSkill2_2_ne, emoji=iliTmpSkill2_2_ne.emoji[0][0], use=CHARISMA, power=80, effectOnSelf=iliTmpSkill1_4_ne, description="Saute derrière l'ennemi ciblé, infligeant des dégâts aux ennemis autour de vous, vous octroie {0} et vous permet de rejouer votre tour".format(iliTmpSkill1_4_ne),replay=True,cooldown=3)
iliTmpSkill2_1 = skill("Bash Lumineux","iliTmpSkill2",TYPE_DAMAGE, tpBehind=True, range=AREA_CIRCLE_4, emoji='<:iliLightSpeed:1046384202792308797>', use=CHARISMA, power=50, effectOnSelf=iliTmpSkill2_2_ne, rejectEffect=iliTmpSkill2_2_ne, description="Saute derrière l'ennemi ciblé en lui infligeant des dégâts et vous permet de rejouer votre tour",replay=True,cooldown=1)
iliTmpSkill2 = skill("Bash Lumineux",iliTmpSkill2_1.id,TYPE_DAMAGE,become=[iliTmpSkill2_1,iliTmpSkill2_2],emoji=iliTmpSkill2_2.emoji)

iliTmpSkill3 = skill("Requiescat","iliTmpSkill3",TYPE_DAMAGE,power=75,range=AREA_CIRCLE_1,effectOnSelf=iliTmpSkill1_renfort,emoji=iliTmpSkill1_renfort.emoji[0][0],cooldown=7,replay=True,use=CHARISMA,description="Inflige des dégâts à l'ennemi ciblé et vous permet de rejouer votre tour. Durant un petit moment, remplace votre combo {0}-{2}-{4} par {1}-{3}-{5} et {6} par {7}".format(iliTmpSkill1_1_1,iliTmpSkill1_1_2,iliTmpSkill1_2_1,iliTmpSkill1_2_2,iliTmpSkill1_3_1,iliTmpSkill1_3_2,iliTmpSkill1_4_1,iliTmpSkill1_4_2))

iliTmpSkill4_2_ne = effect("Tourbillon de Lumière","iliTmpSkill4_2_ne",silent=True,turnInit=5,emoji='<:iliOvlSkill5:1139249633877557309>')
iliTmpSkill4_2 = skill("Tourbillon Inversé","iliTmpSkill4_2",TYPE_DAMAGE,use=CHARISMA,range=AREA_MONO,area=AREA_CIRCLE_2,emoji=iliTmpSkill4_2_ne.emoji[0][0],power=80,replay=True,needEffect=iliTmpSkill4_2_ne,effectOnSelf=iliTmpSkill1_4_ne,description="Inflige des dégâts aux ennemis autour de vous, vous octroie {0} et vous permet de rejouer votre tour".format(iliTmpSkill1_4_ne),cooldown=3)
iliTmpSkill4_1 = skill("Tourbillon de Lumière","iliTmpSkill4_2",TYPE_DAMAGE,use=CHARISMA,range=AREA_MONO,area=AREA_CIRCLE_1,emoji='<:iliBravor:1046381213910302834>',power=50,replay=True,effectOnSelf=iliTmpSkill4_2_ne, rejectEffect=iliTmpSkill4_2_ne, description="Inflige des dégâts aux ennemis autour de vous et vous permet de rejouer votre tour".format(iliTmpSkill1_4_ne),cooldown=1)
iliTmpSkill4 = skill(iliTmpSkill4_1.name,iliTmpSkill4_1.id,TYPE_DAMAGE,become=[iliTmpSkill4_1,iliTmpSkill4_2],emoji=iliTmpSkill4_1.emoji)

iliTmpSkill5_e = effect("Régénération","iliTmpSkill5_e",CHARISMA,turnInit=3,trigger=TRIGGER_START_OF_TURN,power=50,type=TYPE_INDIRECT_HEAL,emoji='<a:ilianaRegen:969825374093578260>')
iliTmpSkill5_e1 = effect("Régénération","iliTmpSkill5_e1",CHARISMA,trigger=TRIGGER_INSTANT,power=35,type=TYPE_INDIRECT_HEAL,emoji='<:lightAura3:1133264372957978745>')
iliTmpSkill5 = skill("Régénération","iliTmpSkill5",TYPE_HEAL,power=iliTmpSkill5_e.power, effects=[iliTmpSkill5_e], cooldown=iliTmpSkill5_e.turnInit, emoji='<:lightAura2:1106836809083781120>', range=AREA_DONUT_7, replay=True, use=CHARISMA, effectOnSelf=iliTmpSkill1_4_ne, description="Soigne l'allié ciblé, lui octroie un effet régénérant, vous octroie {0} et vous permet de rejouer votre tour".format(iliTmpSkill1_4_ne))

clemSmn = copy.deepcopy(batInvoc)
clemSmn.name, clemSmn.icon, clemSmn.strength, clemSmn.endurance, clemSmn.gender = "Isa", ["<:isa:1158136337061400797>","<:isa:1158136337061400797>"], [HARMONIE,1], GENDER_FEMALE, [HARMONIE,1]
clemSmnEff = effect("Garde maternelle","clemSmnEff",trigger=TRIGGER_DEATH,turnInit=21,type=TYPE_SUMMON,callOnTrigger=clemSmn,emoji="<:isa:1158136337061400797>",area=AREA_CIRCLE_2,lvl=1)
aliceSmnEff = effect("Princess des chauve-souris","aliceSmnEff",trigger=TRIGGER_DEATH,turnInit=21,type=TYPE_SUMMON,callOnTrigger=batInvoc,emoji='<:batPrincess:1197056891688321094>',area=AREA_CIRCLE_2,lvl=3)

tmpFeliStuff = [
    stuff("Bandeau Blanc","",0,strength=200,endurance=100,agility=55,precision=50,charisma=20,intelligence=35,magie=75,resistance=15,percing=5,critical=5),
    stuff("Tee-Shirt Rouge","",1,strength=200,endurance=100,agility=55,precision=50,charisma=20,intelligence=35,magie=75,resistance=15,percing=5,critical=5),
    stuff("Sneakers Blanches","",0,strength=200,endurance=100,agility=55,precision=50,charisma=20,intelligence=35,magie=75,resistance=15,percing=5,critical=5)
]

tmpFeliWeap = copy.deepcopy(dtsword)
tmpFeliWeap.priority = WEAPON_PRIORITY_NONE
tmpFeliSkill1ElementTabl = []
for indx in range(ELEMENT_FIRE,ELEMENT_TIME+1):
    tmpFeliSkill1ElementTabl.append(effect("Maîtrise {0}".format(elemNames[indx]),"feliTmpMaitrise{0}".format(indx),turnInit=-1,unclearable=True,emoji=elemEmojis[indx]))

tmpFeliSkill1BecomeList, listInitSkills = [], [firePhysCombo,waterPhysCombo,airPhysCombo,earthPhysCombo,darknessPhysCombo,lightPhysCombo,spacePhysCombo,timePhysCombo]
for indx, tmpInitSkills in enumerate(listInitSkills):
    tmpSkill1, tmpSkill2, tmpSkill3 = copy.deepcopy(tmpInitSkills.become[0]), copy.deepcopy(tmpInitSkills.become[1]), copy.deepcopy(tmpInitSkills.become[2])
    tmpSkill2.needEffect.append(tmpFeliSkill1ElementTabl[indx]), tmpSkill3.needEffect.append(tmpFeliSkill1ElementTabl[indx])
    tmpSkill1.needEffect = [tmpFeliSkill1ElementTabl[indx]]
    tmpSkill1.iaPow, tmpSkill2.iaPow, tmpSkill3.iaPow = 10, 20, 30
    tmpSkill1.id = tmpSkill2.id = tmpSkill3.id = "tmpFeliSkill1"
    tmpSkill1.cooldown = tmpSkill2.cooldown = tmpSkill3.cooldown = 1
    tmpFeliSkill1BecomeList += [tmpSkill1, tmpSkill2, tmpSkill3]

tmpFeliSkill1Eff = effect("Maîtrise Universelle","feliTmpMaitrise-1",trigger=TRIGGER_INSTANT,emoji=elemEmojis[ELEMENT_UNIVERSALIS])
tmpFeliSkill1 = skill("Maîtrise Universelle","tmpFeliSkill1",TYPE_PASSIVE,become=tmpFeliSkill1BecomeList,emoji=elemEmojis[ELEMENT_UNIVERSALIS],effects=tmpFeliSkill1Eff)
tmpFeliSkill1.cooldown, tmpFeliSkill1.initCooldown = 1, 1

tmpFeliSkill2_1 = copy.deepcopy(fragmentation)
tmpFeliSkill2_1.power, tmpFeliSkill2_1.range, tmpFeliSkill2_1.cooldown, tmpFeliSkill2_1.description = 150, AREA_CIRCLE_3, 3, "Saute sur l'ennemi ciblé en lui infligeant des dégâts tout en réduisant sa résistance et l'armure qu'il reçoit momentanément"
tmpFeliSkill2_2_eff3 = copy.deepcopy(tmpFeliSkill2_1.effects[0])
tmpFeliSkill2_2_eff3.resistance = tmpFeliSkill2_2_eff3.resistance // 2
tmpFeliSkill2_2_eff2 = effect("Get dunked on","tmpFeliSkill2_2_eff2",trigger=TRIGGER_INSTANT,type=TYPE_MALUS,callOnTrigger=tmpFeliSkill2_2_eff3)
tmpFeliSkill2_2 = skill("Dunk", tmpFeliSkill2_1.id, TYPE_DAMAGE, power=100, garCrit=True, setAoEDamage=True, effects=[tmpFeliSkill2_1.effects[0],tmpFeliSkill2_2_eff2], cooldown=tmpFeliSkill2_1.cooldown, tpCac=True, area=AREA_CIRCLE_1, range=tmpFeliSkill2_1.range, description="Saute sur les ennemis ciblés en leur infligeant des dégâts tout en réduisant la résistance de la cible principale ainsi que celle des cibles secondaires, dans une moindre mesure", emoji="<:getDunked:1250078493421732014>")
tmpFeliSkill2 = skill("Saut Transperçant",tmpFeliSkill2_1.id,TYPE_DAMAGE,become=[tmpFeliSkill2_1,tmpFeliSkill2_2],emoji=tmpFeliSkill2_2.emoji, description="{0} :\n{1}\n\n{2} : {3}".format(tmpFeliSkill2_1,tmpFeliSkill2_1.description,tmpFeliSkill2_2,tmpFeliSkill2_2.description))

iliTmpSkill6 = copy.deepcopy(dicetiny)
iliTmpSkill6.power, iliTmpSkill6.initPower, iliTmpSkill6.maxPower, iliTmpSkill6.cooldown = 100, 100, 200, 3

sixtineSkill5 = copy.deepcopy(backupdancer)
sixtineSkill5.effects[0].power, sixtineSkill5.effects[2].callOnTrigger.power, sixtineSkill5.ultimate = 100, 50, False

tmpFeliSkill3 = skill("Taillade Sautée","tmpFeliSkill3",TYPE_DAMAGE,power=150,range=AREA_CIRCLE_3,tpCac=True,emoji='<:feliSlash:916208942974132245>',cooldown=5,damageOnArmor=2)

lenaExSkill6 = copy.deepcopy(amethysArcane)
lenaExSkill6.use, lenaExSkill6.effectAroundCaster, lenaExSkill6.effectOnSelf, lenaExSkill6.power = STRENGTH, [TYPE_HEAL,lenaExSkill6.effectOnSelf.callOnTrigger.area, lenaExSkill6.effectOnSelf.callOnTrigger.power*1.5], None, lenaExSkill6.power*2