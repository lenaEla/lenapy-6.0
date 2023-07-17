from advObjects.npcSkills.npcSkillsImports import *
from advObjects.npcSkills.npcSkills_ennemi import lioLB

# Shushi alt spells
shushiSkill1 = skill("Frappe lumineuse", "shushiSkill1", TYPE_DAMAGE, 0, 80, cooldown=3, use=MAGIE, emoji='<a:ShushiLF:900088862871781427>')
shushiSkill3Eff = effect("Jeu de lumière", "diff", redirection=35, trigger=TRIGGER_DAMAGE,description="Un habile jeu de lumière permet de vous cacher de vos ennemis")
shushiSkill3 = skill("Diffraction", "shushiSkill2", TYPE_ARMOR, 0, 0, AREA_CIRCLE_6, effects=shushiSkill3Eff,cooldown=5, initCooldown=2, use=None, emoji='<a:diffraction:916260345054658590>')
shushiSkill4Eff = effect("Assimilation", "assimil", MAGIE, resistance=10, overhealth=80, description="Grâce à Shihu, vous avez réussi à utiliser les Ténèbres environant à votre avantage",emoji=uniqueEmoji("<:tarmor:909134091604090880>"), type=TYPE_ARMOR, trigger=TRIGGER_DAMAGE)
shushiSkill4 = skill("Assimilation", "shushiSkill4", TYPE_ARMOR, 0, cooldown=5, effects=shushiSkill4Eff,say='On peut y awiver !', use=MAGIE, emoji='<:assimilation:916260679944634368>')
shushiWeapEff = effect("Lueur Ténébreuse", "darkLight", MAGIE, resistance=5, overhealth=50,type=TYPE_ARMOR, emoji=uniqueEmoji('<:dualMagie:899628510463803393>'))
shushiWeap = weapon("Magie trancendante", "dualMagie", RANGE_LONG, AREA_DONUT_5, 35, 100, 0, strength=-20, endurance=10, charisma=20, intelligence=20,magie=55, type=TYPE_HEAL, target=ALLIES, use=MAGIE, effectOnUse=shushiWeapEff, affinity=ELEMENT_LIGHT, emoji='<:dualMagie:899628510463803393>')
shushiHat = stuff("Barrête de la cohabitation", "dualHat", 0, 0, strength=-20, endurance=15, charisma=20, agility=10,precision=10, intelligence=20, magie=45, affinity=ELEMENT_LIGHT, emoji='<:coaBar:911659734812229662>')
shushiDress = stuff("Robe de la cohabitation", "dualDress", 1, 0, strength=-10, endurance=35, charisma=20, agility=0,precision=10, intelligence=10, magie=60, resistance=20, affinity=ELEMENT_LIGHT, emoji='<:coaDress:911659797076660294>')
shushiBoots = stuff("Bottines de la cohabitation", "dualBoost", 2, 0, strength=-10, endurance=15, charisma=0, agility=20,precision=10, magie=45, intelligence=10, affinity=ELEMENT_LIGHT, emoji='<:coaBoots:911659778995007528>')
shushiSkill5 = skill("Lumière éternelle", "LumEt", TYPE_RESURECTION, 0, 100, emoji='<:renisurection:873723658315644938>',cooldown=3, description="Permet de ressuciter un allié", use=MAGIE, range=AREA_DONUT_7)
shushiArmorSkillEff = effect("Armure Harmonique", "shushiArmor", MAGIE, overhealth=100, turnInit=3,type=TYPE_ARMOR, trigger=TRIGGER_DAMAGE, emoji=uniqueEmoji("<a:transArmorB:900037831257358378>"))
shushiArmorSkill = skill("Armure Harmonique", "shushiArmorSkill", TYPE_ARMOR, 0, effects=shushiArmorSkillEff,range=AREA_MONO, area=AREA_CIRCLE_5, cooldown=7, use=MAGIE, emoji='<a:transArmorB:900037831257358378>')

# Alice Ex. skills
clemBloodJauge = effect("Jauge de sang","clemBloodJauge",turnInit=-1,unclearable=True,emoji=uniqueEmoji('<:vampire:900312789686571018>'),lvl=100,description="Clémence possédée tourne autour de sa Jauge de Sang\n\nElle débute le combat avec une jauge à **100** Points de sang, son maximum.\nChacunes de ses compétences ont un coût en Points de Sang, qui sont retiré à la jauge à la fin de leur utilisation\n\nSi la jauge de sang tombe à **0 point**, Clémence est étourdie pendant 2 tours durant lesquels sa résistance est diminuée\nLa jauge de sang récupère **1 point** de sang à chaque fois que Clémence inflige 50 points de dégâts, et **100 points** une fois que Clémence n'est plus étourdie\n\nLa quantité de points de sang dans la jauge de sang est constamant visible\nClémence possède 10% de vol de vie",jaugeValue=jaugeValue(
    emoji=[["<:BJLeftEmpty:900473865459875911>","<:BJMidEmpty:900473889539366994>","<:BJRightEmpty:900473909856587847>"],["<:BJLeftFull:900473987564441651>","<:BJMidFull:900474021781569604>","<:BJRightFull:900474036042215515>"]],
    conds=[
        jaugeConds(INC_START_FIGHT,100),
        jaugeConds(INC_ENEMY_DAMAGED,20/100)]
    ))

aliceBloodJauge = copy.deepcopy(clemBloodJauge)
aliceBloodJauge.emoji = uniqueEmoji("<:vampire:900312789686571018>")
aliceBloodJauge.description = "Alice exaltée tourne autour de sa Jauge de Sang\n\nElle débute le combat avec une jauge à **100** Points de sang, son maximum.\nChacunes de ses compétences ont un coût en Points de Sang, qui sont retiré à la jauge à la fin de leur utilisation\n\nSi la jauge de sang tombe à **0 point**, Alice est étourdie pendant 2 tours durant lesquels sa résistance est diminuée\nLa jauge de sang récupère **1 point** de sang à chaque fois que Alice soigne 50 points de vie, et **100 points** une fois qu'Alice n'est plus étourdie\n\nLa quantité de points de sang dans la jauge de sang est constamant visible"
aliceBloodJauge.jaugeValue = jaugeValue(
    emoji=[["<:BJLeftEmpty:900473865459875911>","<:BJMidEmpty:900473889539366994>","<:BJRightEmpty:900473909856587847>"],["<:aliceBJLeftFull:914780954336305192>","<:aliceBJMidFull:914780988134019073>","<:aliceBJRightFull:914781018559492106>"]],
    conds=[
        jaugeConds(INC_START_FIGHT,100),
        jaugeConds(INC_ALLY_HEALED,20/100)]
    )


aliceExHeadruban = stuff("Ruban vampirique", "aliceExHead", 0, 0, charisma=40, negativeHeal=-50, endurance=55, emoji=batRuban.emoji)
aliceExDress = stuff("Robe vampirique", "aliceExDress", 1, 0, endurance=10, resistance=15, charisma=45, negativeHeal=-25, emoji=aliceDress.emoji)
aliceExShoes = stuff("Ballerines vampiriques", "aliceExShoes", 2, 0, agility=25, charisma=45, negativeHeal=-35, endurance=5, emoji=aliceShoes.emoji)

aliceExWeapEff = effect("Bénédiction vampirique", "aliceExWeapEff", CHARISMA, emoji=uniqueEmoji("<:vampire:900312789686571018>"), power=15, type=TYPE_INDIRECT_HEAL, trigger=TRIGGER_AFTER_DAMAGE, description="Cet effect confère **{0}%** de Vol de Vie au porteur.\nLe pourcentage de convertion est augmenté par les statistiques du lanceur")
aliceExWeap = weapon("Rosa receptaculum", "aliceExWeap", RANGE_DIST, AREA_CIRCLE_5, 35, 100, 0, use=CHARISMA, charisma=35, resistance=10, type=TYPE_HEAL, target=ALLIES, effectOnUse=aliceExWeapEff, effects=aliceBloodJauge, emoji='<:vampBall:916199488891273276>', say=["Je vais essayer de vous faire tenir le plus longtemps possible...", "Je sais que tu en as encore en réserve, c'est pas vraiment le moemenent de lacher !", "On tiens le bon bou, continuons comme ça !", "Mhf..."])
aliceSkill1Eff = effect("Régénération vampirique", "aliceRegenEff", CHARISMA, power=20, emoji=uniqueEmoji("<a:aliceSkill1:914787461949960202>"), type=TYPE_INDIRECT_HEAL,turnInit=3, lvl=3, area=AREA_CIRCLE_2, description="Au début du tour du porteur, lui et ses alliés proches recoivent des soins", trigger=TRIGGER_START_OF_TURN)
aliceSkill1 = skill("Rénégération", "aliceSkill1", TYPE_INDIRECT_HEAL, 0,0, emoji="<a:aliceSkill1:914787461949960202>", effects=aliceSkill1Eff, cooldown=3)
aliceSkill2Eff = effect("Galvanision vampirique", "aliceBoostEff", CHARISMA, strength=20,magie=20, percing=3, emoji=uniqueEmoji('<a:aliceSkill2:914791502931197962>'))
aliceSkill2 = skill("Galvanisation", "aliceSkill2", TYPE_BOOST, 0, range=AREA_DONUT_6, area=AREA_CIRCLE_2, effects=aliceSkill2Eff, cooldown=3, emoji='<a:aliceSkill2:914791502931197962>', say=["Allez-s'y !", "On ne lâche rien !", "Il va falloir essayer un peu plus fort que ça..."])
aliceDirectDmg = skill("Flos luminosus", "aliceSkill3", TYPE_DAMAGE, 0, 130, emoji='<a:aliceSkill3:914794172215623690>', cooldown=3,use=CHARISMA, say=["C'est pour ton bien Clémence !", "Sit invehitur Rosa Lucis !", "Tuum, Rosa Lucis !"])
aliceIndirectDmgEff = effect("Provecta Fluos Luminosus","aliceDot",CHARISMA,power=int(150/5),turnInit=5,lvl=5,description="Inflige des dégâts indirects en début de tours",type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji='<a:aliceSkill3:914794172215623690>')
aliceDotEff2 = copy.deepcopy(dmgDown)
aliceDotEff2.power, aliceDotEff2.stat, aliceDotEff2.turnInit = 3, CHARISMA, 3
aliceIndirectDmg = skill("Provecta Fluos Luminosus","aliceSkill3",TYPE_INDIRECT_DAMAGE,effects=[aliceIndirectDmgEff,aliceDotEff2],cooldown=5)
aliceSkill3 = skill("Sorts offensifs","aliceSkill3",TYPE_DAMAGE,become=[aliceDirectDmg,aliceIndirectDmg],cooldown=3,description="Inflige des dégâts directs ou bien inflige un effet de dégâts sur la durée tout en réduisant légèrement les dégâts de la cible")
aliceSkill4 = skill("Pleine lune", "aliceSkill4", TYPE_HEAL, 0, 80, AREA_MONO, area=AREA_CIRCLE_3, use=CHARISMA, cooldown=3,emoji='<a:aliceSkill4:914796355925458984>', say=["On lache rien !", "Je donnerais tout, même si je dois y passer !", "Courage !", "Sanet nos lux plenae lunae !"])
aliceRez = skill("Vampirization", "aliceRez", TYPE_RESURECTION, 0, 300, range=AREA_CIRCLE_7, emoji="<a:memAlice2:908424319900745768>", use=CHARISMA,description="Si plus de la moitié de l'équipe est morte, la zone d'effet de la compétence deviens un cercle de 7 cases autour de Alice, mais consomme l'intégralité de sa jauge de sang", say=["C'est trop tôt pour laisser tomber !", "On a encore besoin de toi !"])
aliceRez2 = skill("Salutaris meridiem", "aliceRez+", TYPE_RESURECTION, 0, 300, range=AREA_MONO, area=AREA_CIRCLE_7,emoji="<a:memAlice2:908424319900745768>", use=CHARISMA, say="Angeli, audi me et adiuva nos, sustulite... MEMENTO VOCIS ANGELI !")
aliceSongEff2 = effect("Chant de la gloire","aliceSongEff2",CHARISMA,strength=10,endurance=10,charisma=10,agility=10,precision=10,intelligence=10,magie=10,description="Augmente toutes les statisitiques principales du porteur",emoji='<:aliceSongSkill:977011751075868682>')
aliceSongEff1 = effect("Chant de la gloire","aliceSongEff1",callOnTrigger=aliceSongEff2,area=AREA_DONUT_7,trigger=TRIGGER_END_OF_TURN,emoji='<a:aliceSongEff:977011977358544927>',turnInit=3,description="Augmente les statistiques des alliés à la fin du tour")
aliceSong1 = skill("Chant de la gloire","aliceSkill5",TYPE_BOOST,effects=aliceSongEff1,range=AREA_MONO,emoji='<:aliceSongSkill:977011751075868682>',cooldown=5,description="Se met à entonner le Chant de la Gloire, augmentant les statistiques principales des alliés autour de vous à la fin de votre tour pendant 3 tours (celui-ci inclut)",message='Alice entonne le Chant de la Gloire')
aliceSong2Eff1, aliceSong2Eff2 = copy.deepcopy(healDoneBonus), effect("Chant de la vie","aliceSong2Eff2",CHARISMA,power=15,area=AREA_CIRCLE_7,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_HEAL,turnInit=3,lvl=3,emoji=aliceSkill1.emoji)
aliceSong2Eff1.turnInit, aliceSong2Eff1.power = 3, 20
aliceSong2 = skill("Chant de la Vie","aliceSkill5",TYPE_INDIRECT_HEAL,range=AREA_MONO,effects=[aliceSong2Eff1,aliceSong2Eff2],cooldown=3)
aliceSkill5 = skill("Répertoire","aliceSkill5",TYPE_BOOST,become=[aliceSong1,aliceSong2],use=CHARISMA,cooldown=3,description="Permet d'entonner un chant pendant 3 tours\n{0} __{1} :__ Augmente toutes les statistiques principales des alliés alentours\n{2} __{3} :__ Soigne les alliés alentours tout en augmentant les soins réalisés par Alice".format(aliceSong1.emoji,aliceSong1.name,aliceSong2.emoji,aliceSong2.name))
aliceCoda1Eff = effect("Coda régénérant","aliceCoda1Eff",CHARISMA,power=30,area=AREA_CIRCLE_1,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL)
aliceCoda2Eff, aliceCoda3Eff = copy.deepcopy(defenseUp), copy.deepcopy(dmgUp)
aliceCoda2Eff.stat = aliceCoda3Eff.stat = CHARISMA
aliceCoda2Eff.power, aliceCoda3Eff.power = 7, 10
aliceCoda2Eff.turnInit = aliceCoda3Eff.turnInit = 3
aliceCoda4Eff = effect("Coda galvanisant","aliceCoda4Eff",CHARISMA,strength=15,magie=15,turnInit=3)
aliceCoda1 = skill("Coda régénérant","aliceSkill6",TYPE_INDIRECT_HEAL,cooldown=3,effects=aliceCoda1Eff)
aliceCoda2 = skill("Coda offensif","aliceSkill6",TYPE_BOOST,cooldown=3,effects=aliceCoda2Eff,area=AREA_CIRCLE_1)
aliceCoda3 = skill("Coda défensif","aliceSkill6",TYPE_BOOST,cooldown=3,effects=aliceCoda3Eff,area=AREA_CIRCLE_1)
aliceCoda4 = skill("Coda galvanisant","aliceSkill6",TYPE_BOOST,cooldown=3,effects=aliceCoda4Eff,area=AREA_CIRCLE_1)
aliceSkill6 = skill("Coda Musicaux","aliceSkill6",TYPE_BOOST,cooldown=3,become=[aliceCoda1,aliceCoda2,aliceCoda3,aliceCoda4],description="Octroi un Coda à un allié")

# Clem Ex.
clemBleeding = copy.deepcopy(bleeding)
clemBleeding.power, clemBleeding.stat, clemBleeding.name, clemBleeding.lifeSteal = 35, MAGIE, "Sanguisugae", 35
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
clemExBloodDemonEff2 = effect("Crepitus Sanguinis Moratus","bloodDemonEx2",type=TYPE_INDIRECT_DAMAGE,stat=MAGIE,power=80,area=AREA_CIRCLE_1,turnInit=4,lvl=99,trigger=TRIGGER_AFTER_DAMAGE,description="Lorsque vous utilisez une compétence, inflige des dégâts indirects de zone centré sur la cible principale",emoji='<:dislocation:1052697663402950667>')
clemExBloodDemonEff3 = effect("Cicatrice Alpha","clemExBloodDemonEff3",PURCENTAGE,power=CLEMEXSCAR,turnInit=4,lvl=4,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,description="Une ancienne citratrice magique réveillée par votre afflue de puissance vous inflige des dégâts à la fin de votre tour",emoji='<:griphAlpha:1064270537037197416>')
clemExBloodDemon = skill("Sanguis Daemonis Exaltatus","clemExBloodDemon",TYPE_DAMAGE,power=100,range=AREA_MONO,area=AREA_DONUT_3,effects=[clemExBloodDemonEff,clemExBloodDemonEff2,clemExBloodDemonEff3],cooldown=7,jaugeEff=clemExBloodJauge,minJaugeValue=100,description="Vous infligez des dégâts autour de vous déchénant toute votre puissance !\nAugmente votre Magie, rend toutes vos compétences instantannée, inflige des dégâts indirects supplémentaire en attaquant, mais vous subissez des dégâts continues, le tout durant quatres tours",emoji="<:sanguisDaemonium:1050059965630533714>")

suppIndDamageEffId.append(clemExBloodDemonEff2)

clemExSay = says(
    start="Pff, vous tenez tant que ça à être au milieu de ma route ?",
    onKill="Tss, même pas le temps de faire une pause pour manger...",
    blueWinAlive="Quel résultat surprenant"
)

clemExWeapon = copy.deepcopy(rapiere)
clemExWeapon.power, clemExWeapon.range, clemExWeapon.effectOnUse, clemExWeapon.name = 200, RANGE_MELEE, clemBleeding, "Flos Argenteus"
miniStuff = stuff("Rune adaptative", 'clemRune', 0, 0, endurance=50, charisma=0, agility=50//2,precision=int(50*0.3), intelligence=50//10, magie=50*2, resistance=min(50//5, 35), emoji=clemEarRings.emoji)

# Iliana prêtresse
miniStuffHead = stuff("Casque de la neko de la lueur ultime", 'ilianaPreHead', 0, 0, endurance=int(50*1.35), agility=int(50*0.3), precision=int(50*0.3), charisma=50, magie=50, resistance=min(50//5, 50), percing=10, emoji=zenithHat.emoji)
miniStuffDress = stuff("Armure de la neko de la lueur ultime", 'ilianaPreArmor', 1, 0, endurance=int(50*1.85), agility=int(50*0.3), precision=int(50*0.5), charisma=50, magie=50, percing=15, resistance=min(50//5, 50), emoji=zenithArmor.emoji)
miniStuffFlats = stuff("Sorolets de la neko de la lueur ultime", 'ilianaPreBoots', 2, 0, endurance=int(50*1.35), agility=int(50*0.3), precision=int(50*0.3), charisma=50, magie=50, resistance=min(50//5, 50), percing=10, emoji=zenithBoots.emoji)

iliPreArmor = effect("Armure de Lumière", "ilianaShield", CHARISMA, overhealth=135, type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE, turnInit=5, stackable=True, emoji='<a:transArmorB:900037831257358378>')
iliPrePoi = effect("Lumière Absolue", "ilianaIndirect", CHARISMA, power=50,type=TYPE_INDIRECT_DAMAGE, trigger=TRIGGER_START_OF_TURN, turnInit=3, lvl=5, emoji='<:iliDot:1046387034522136609>')
iliPreRegen = effect("Régénération de Lumière", "ilianaRegen", CHARISMA, power=100, trigger=TRIGGER_START_OF_TURN, type=TYPE_INDIRECT_HEAL,emoji='<a:ilianaRegen:969825374093578260>', turnInit=5, stackable=True, description="Soigne le porteur de l'effet au début de son tour")

iliPreSkill1 = skill("Lumière Tranchante", 'iliSkill1', TYPE_DAMAGE, range=AREA_MONO, area=AREA_CIRCLE_3, power=185, use=CHARISMA, cooldown=5, effectOnSelf = iliPreRegen, description='Inflige des dégâts aux ennemis alentours et vous procure un effet régénérant', emoji='<:iliBravor:1046381213910302834>',selfEffPurcent = 80)

iliPreSkill2Heal = skill('Régénération', "iliSkill2", TYPE_HEAL, power=200, range=AREA_CIRCLE_7, effects=iliPreRegen, cooldown=3, description="Soigne l'allié ciblé et lui procure un effet de régénération sur la durée", use=CHARISMA, emoji='<a:ilianaRegen:969825374093578260>')
iliPreSkill2DmgEff = copy.deepcopy(vulne)
iliPreSkill2DmgEff.power = 35
iliPreSkill2Dmg = skill("Fracturation","iliSkill2",TYPE_DAMAGE, power=100,repetition=3,tpCac=True,effects=[iliPreSkill2DmgEff],effBeforePow=True,cooldown=3,use=CHARISMA,description="Augmente les dégâts subis par la cible de **35%** et lui inflige des dégâts à trois reprises")
iliPreSkill2 = skill("Pouvoir de la lumière","iliSkill2",TYPE_HEAL,cooldown=3,become=[iliPreSkill2Heal,iliPreSkill2Dmg], emoji= '<:lightHealShield:929322808654323733>')

iliPreSkill3_1_e = copy.deepcopy(defenseUp)
iliPreSkill3_1_e.power = 20
iliPreSkill3_1 = skill("Champ lumineux", 'iliSkill3', TYPE_INDIRECT_DAMAGE, effects=iliPrePoi, range=AREA_MONO, area=AREA_CIRCLE_3, use=CHARISMA, cooldown=3, effectOnSelf=iliPreSkill3_1_e, description='Inflige des dégâts aux ennemis alentours, vous soigne légèrement puis inflige un effet de dégâts indirect aux ennemis alentours tout en réduisant vos dégâts subis de **20%** durant un tour', emoji='<:iliLightField:1046381182767603752>')
iliPreSkill3_c = effect("Enchaînement - {replicaName}","iliSkill3Cast",replique=iliPreSkill3_1,silent=True)
iliPreSkill3 = skill("Tourbillon de Lumière", "iliSkill3", TYPE_DAMAGE, power=150, range=AREA_MONO,area=AREA_CIRCLE_3, use=CHARISMA, replay=True, description="Inflige des dégâts aux ennemis alentours, vous soigne légèrement puis inflige un effet de dégâts indirect aux ennemis alentours tout en réduisant vos dégâts subis de **20%** durant un tour", emoji='<:revolLum:1033720380281597983>', effectOnSelf=iliPreSkill3_c)

iliPreDmgReduc = copy.deepcopy(defenseUp)
iliPreDmgReduc.power = 50
iliPreSkill4 = skill("Lumière Eternelle","iliLb",TYPE_DAMAGE,power=200,area=AREA_ALL_ENEMIES,range=AREA_MONO,emoji=trans.emoji,ultimate=True,effectAroundCaster=[TYPE_BOOST,AREA_ALL_ALLIES,iliPreDmgReduc],cooldown=10, description='Inflige des dégârs à tous les ennemis et réduit de **50%** les dégâts subis par tous les alliés',use=CHARISMA)

iliStans1_2 = effect("Couverture Lumineuse","ilianaStans1_1",emoji='<:cover:1061384419212005417>',redirection=20,silent=True)
iliStans1_1 = effect("Voeu de la Protectrice", "ilianaStans2", charisma=30, resistance=20, aggro=100, turnInit=-1, unclearable=True, emoji='<:iliShieldStans:1072554524260188285>',power=25, trigger=TRIGGER_END_OF_TURN, area=AREA_DONUT_2, callOnTrigger=iliStans1_2, description="Augmente grandement l'Agression, le Charsime et la Résistance d'Iliana, réduit de **{0}%** les dégâts qu'elle subit et, à la fin de son tour, octroi un effet redirigeant **20%** des dégâts subis aux alliés en mêlée d'elle")
iliStans1 = skill("Voeu de la Protectrice", "ilianaSkill5_1",TYPE_PASSIVE, effectOnSelf=iliStans1_1, emoji=iliStans1_1.emoji[0][0],description=iliStans1_1.description.format(iliStans1_1.power))

iliStans2_1 = effect("Voeu de la Prêtresse","ilianaStans2", turnInit=-1, unclearable=True, emoji='<:iliDptStans:1072558143772561418>',stat=CHARISMA,power=50,description="Augmente de de **{0}%** les dégâts infligés par Iliana. De plus, après chaque utilisation d'une compétence offensive ou de son arme, elle se soigne avec une puissance de **62**. Ces effets sont doublés si Iliana affronte seule les Informités")
iliStans2 = skill("Conviction de la Prêtresse", "ilianaSkill5_2",TYPE_PASSIVE, effectOnSelf=iliStans2_1, emoji=iliStans2_1.emoji[0][0],description=iliStans2_1.description.format(iliStans2_1.power))

iliStans1.description += "\n\nSi Iliana est seule, cette compétence est remplacée par {0} __{1}__".format(iliStans2.emoji,iliStans2.name)
iliStans2.description += "\n\nSi Iliana combat aux côtés de Luna, cette compétence est remplacée par {0} __{1}__".format(iliStans1.emoji,iliStans1.name)

iliPreSkill5 = skill("Conviction de la Lumière","iliaSkill5",TYPE_BOOST,become=[iliStans1,iliStans2],emoji='<:ilianaStans:969819202032664596>',description='Suivant si Iliana se bat seule ou aux côtés de Luna, lui confère un effet passif augmentant ses capacités offensives ou défensives\n\n{0} __{1} :__\n{2}\n\n{3} __{4} :__\n{5}'.format(iliStans1.emoji,iliStans1.name,iliStans1.description,iliStans2.emoji,iliStans2.name,iliStans2.description))

iliPreSkill6 = skill("Vitesse Lumière", "iliSkill6", TYPE_DAMAGE, power=50, range=AREA_INLINE_4, replay=True, cooldown=2, tpCac=True,use=CHARISMA, description='Vous téléporte au corps à corps de l\'ennemi ciblé et vous permet de rejouer votre tour', emoji='<:iliLightSpeed:1046384202792308797>')

iliPreSkill7Dmg = skill("Rayon de Lumière", "iliPreSkill7", TYPE_DAMAGE, power=150, range=AREA_CIRCLE_3, area=AREA_LINE_6, cooldown=4, use=CHARISMA, description="Inflige des dégâts sur une ligne droite devant vous",emoji='<:lightArrow:980172606143606834>')
iliPreSkill7RedirectEff = effect("Diffraction","iliRedirect",redirection=100,emoji='<:cover:1061384419212005417>')
iliPreSkill7Redirect = skill('Diffraction',"iliPreSkill7",TYPE_BOOST,effects=iliPreSkill7RedirectEff,range=AREA_DONUT_7,effectOnSelf=iliPreRegen,cooldown=iliPreSkill7Dmg.cooldown,description="Redirige **{0}%** des dégâts subis par l'allié ciblé sur vous jusqu'à votre prochain tour et vous octroi un effet régénérant".format(iliPreSkill7RedirectEff.redirection),emoji='<:gardian:1061384121198317629>')
iliPreSkill7 = skill("Jeu de lumière",'iliPreSkill7',TYPE_DAMAGE,become=[iliPreSkill7Dmg,iliPreSkill7Redirect],cooldown=4, emoji='<:catLight:956599774461722655>',description='{0} __{1} :__\n{2}\n\n{3} __{4} :__\n{5}'.format(iliPreSkill7Dmg.emoji,iliPreSkill7Dmg.name,iliPreSkill7Dmg.description,iliPreSkill7Redirect.emoji,iliPreSkill7Redirect.name,iliPreSkill7Redirect.description))

iliWeap = weapon("Epée et Bouclier de la Lumière", "iliWeap", RANGE_MELEE, AREA_CIRCLE_1, 125, 100, charisma=30, endurance=20,resistance=15, area=AREA_CIRCLE_1, ignoreAutoVerif=True, emoji=infLightSword.emoji, use=CHARISMA)

LunaPreStuffHead = stuff("Boucle d'oreille ombrale", 'lunaDarkPendant', 0, 0, endurance=int(50*0.3), agility=50,precision=int(50*0.3), strength=int(50*2.2), resistance=min(50//5, 30), percing=10, emoji=darkMaidPendants.emoji)
LunaPreStuffDress = stuff("Robe de soubrette ombrale ombrale", 'lunaDarkMaidDress', 0, 0, endurance=int(50*0.7), agility=50, precision=int(50*0.5), strength=int(50*3), percing=15, resistance=min(50//5, 40), emoji=darkMaidDress.emoji)
LunaPreStuffFlats = stuff("Ballerines ombrales", 'lunaDarkFlats', 0, 0, endurance=int(50*0.3), agility=int(50*1.3), precision=int(50*0.3), strength=int(50*2.2), resistance=min(50//5, 30), percing=10, emoji=darkMaidFlats.emoji)

lunaWeap = weapon("Épee de l'ombre éternelle","aaa",RANGE_LONG,AREA_CIRCLE_1,80,40,strength=20,agility=20,precision=20,repetition=5,emoji='<:lunaWeap:915358834543968348>',damageOnArmor=1.2,ignoreAutoVerif=True)
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
lunaSkill4_1 = skill("Convertion rapprochée",'lunaSkill4',TYPE_INDIRECT_DAMAGE,0,range=AREA_MONO,area=AREA_CIRCLE_2,effects=lunaSkill4EffAlt,cooldown=3,emoji=lunaSkill4Eff.emoji[0][0],say=['Vous tenez tant à voir les Ténèbres de plus près ? Voilà pour vous !','Votre Lumière ne vous protègera pas éternellement.'],description="Donne un effet de dégâts indirect monocible aux ennemis proches")
lunaSkill4_2 = skill("Convertion externe",'lunaSkill4',TYPE_INDIRECT_DAMAGE,0,range=AREA_MONO,area=AREA_DIST_7,effects=lunaSkill4Eff,cooldown=3,emoji=lunaSkill4Eff.emoji[0][0],say=["C'est pas parceque vous restez loin que vous serez épargné !","Votre Lumière sucombera à mes Ténèbres."],description="Inflige un effet de dégâts indirect en zone aux ennemis éloignés")

lunaSkill4 = skill("Convertion","lunaSkill4",TYPE_INDIRECT_DAMAGE,0,range=AREA_CIRCLE_7,use=STRENGTH,say="Votre Lumière ne vous protègera pas éternellement !",emoji=lunaSkill4Eff.emoji[0][0],become=[lunaSkill4_1,lunaSkill4_2])
lunaSkill5_1 = skill("Reverse roundhouse-kick","lunaSkill5",TYPE_DAMAGE,0,100,AREA_CIRCLE_1,area=AREA_ARC_1,emoji='<:luna4inOne:919260128698589184>',damageOnArmor=2,description='Inflige des dégâts en zone à un ennemi au corps à corps')
lunaSkill5_2 = skill("Side-kick fouetté","lunaSkill5",TYPE_DAMAGE,0,135,AREA_CIRCLE_1,emoji='<:luna4inOne:919260128698589184>',say="Hmf !",damageOnArmor=3,description='Inflige des dégâts à une cible unique au corps à corps\nDégâts triplé sur de l\'armure')
lunaSkill5_3_eff = effect("Destabilisé","lunaSkill5_3Eff",type=TYPE_MALUS,emoji="<:stun:882597448898474024>",stun=True)
lunaSkill5_3 = skill("Sweeping into Backflip","lunaSkill5",TYPE_DAMAGE,0,80,AREA_CIRCLE_1,repetition=2,effects=lunaSkill5_3_eff,knockback=1,emoji='<:luna4inOne:919260128698589184>',say="C'est que tu es colant toi !",description='Inflige des dégâts, étourdit pendant un tour et repousse un ennemi au corps à corps')
lunaSkill5_4 = skill("Double High roundhouse-kick into Side-kick","lunaSkill5",TYPE_DAMAGE,0,40,AREA_CIRCLE_1,repetition=3,knockback=3,emoji='<:luna4inOne:919260128698589184>',say="Hé vous derrière ! Cadeau !",damageOnArmor=2,description='Inflige des dégats et repousse de 3 cases un ennemi au corps à corps')
lunaSkill6 = skill("Vitesse ombrale","lunaSkill6",TYPE_DAMAGE,0,50,AREA_INLINE_4,emoji='<:lunaDash:932286143884566528>',cooldown=2,replay=True,tpCac=True,accuracy=200,description='Se téléporte au corps à corps d\'un ennemi et vous permet de rejouer votre tour')
lunaSkill7 = skill("Ultimawashi","lunaSkill7",TYPE_DAMAGE,0,150,AREA_CIRCLE_1,cooldown=3,knockback=10,accuracy=200,emoji='<:ultimawashi:932378739327787078>',description="Inflige de lourd dégâts et repousse violament un ennemi au corps à corps")
lunaQuickFightEff = effect('Accélération',"lunaQuickFight",emoji=uniqueEmoji('<:qqLuna:932318030380302386>'),description="Permet au porteur de rejouer son tou une fois")
lunaSkill5Base = skill("Corps à corps","lunaSkill5",TYPE_DAMAGE,0,0,AREA_CIRCLE_1,description="Cette compétence peut avoir 4 effets différents, sélectionné de manière aléatoire",emoji='<:luna4inOne:919260128698589184>',become=[lunaSkill5_1,lunaSkill5_2,lunaSkill5_3,lunaSkill5_4])

accelerant.effects= [lunaQuickFightEff]

lunaPreSkill5_1 = copy.deepcopy(lunaSkill5_4)
lunaPreSkill5_1.cooldown, lunaPreSkill5_1.description, lunaPreSkill5_1.power, lunaPreSkill5_1.affSkillMsg = 2, "Effectue plusieurs attaques sur un adversaire", int(lunaPreSkill5_1.power*1.3), False
lunaPreSkill5_1_cast = effect("Enchainement 4","ench4",silent=True,replique=lunaPreSkill5_1)
lunaPreSkill5_2 = copy.deepcopy(lunaSkill5_2)
lunaPreSkill5_2.effectOnSelf, lunaPreSkill5_2.replay, lunaPreSkill5_2.power, lunaPreSkill5_2.affSkillMsg = lunaPreSkill5_1_cast, True, int(lunaPreSkill5_2.power*1.3), False
lunaPreSkill5_2_cast = effect("Enchaînement 3","ench3",silent=True,replique=lunaPreSkill5_2)
lunaPreSkill5_3 = copy.deepcopy(lunaSkill5_1)
lunaPreSkill5_3.effectOnSelf, lunaPreSkill5_3.replay, lunaPreSkill5_3.description, lunaPreSkill5_3.name, lunaPreSkill5_3.power, lunaPreSkill5_3.affSkillMsg = lunaPreSkill5_2_cast, True, "Effectue plusieurs attaques sur un adversaire", "Combo Corps à Corps", int(lunaPreSkill5_3.power*1.3), False
lunaPreSkill2_eff = effect("Ténèbres d'Obsidienne","lunaPreIndirect",STRENGTH,power=80,emoji='<:lunaIndi:932447879786823730>',turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE)
lunaPreSkill2 = skill("Obsidienne Ténébreuse","lunaPreSkill2",TYPE_INDIRECT_DAMAGE,emoji=lunaPandan.emoji,effects=lunaPreSkill2_eff,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_INLINE_4,lunaPreSkill2_eff],range=AREA_MONO,area=AREA_CIRCLE_4,cooldown=4,description="Inflige un effet de dégâts indirects aux ennemis alentours. Les adversaires allignés subissent une deuxième fois l'effet",replay=True)
lunaPreSkill3 = skill("Frappe d'Obsidienne","lunaPreSkill3",TYPE_DAMAGE,emoji=lunaSkill2.emoji,power=int(lunaSkill2.power*lunaSkill2.repetition*1.25),cooldown=lunaSkill2.cooldown,description="Inflige de lourd dégâts à un ennemi")
lunaDarkChoc = copy.deepcopy(lunaSkill)
lunaDarkChoc.power, lunaDarkChoc.lifeSteal, lunaDarkChoc.cooldown, lunaDarkChoc.description, lunaDarkChoc.name = 200, 15, 5, "Vous téléporte au corps à corps de l'ennemi ciblé et lui porte une attaque infligeant des dégâts de zone tout en vous restituant un pourcentage des dégâts infligés", "Choc d'Obsidienne"
lunaPreUltimawashi = copy.deepcopy(lunaSkill7)
lunaPreUltimawashi.area, lunaPreUltimawashi.name, lunaPreUltimawashi.description = AREA_CIRCLE_1, "Piqué Ténébreux", "Inflige des dégâts à l'ennemi ciblé ainsi qu'aux adversaires alentours, puis repousse violament ce premier".format(lunaPreUltimawashi.power)

liaExWeapEff = effect("Kazama","liaExWeapEff",turnInit=-1,unclearable=True,dodge=13,counterOnDodge=75,power=80,description="Octroi à Lia 75% de chances d'effectuer une **contre-attaque** en esquivant un assaut adverse\nLui octroi également {0}% de chance d'obtenir l'effet {1} __{2}__ en effectuant une compétence {3} __{4}__".format(50,tablElemEff[ELEMENT_AIR].emoji[0][0],tablElemEff[ELEMENT_AIR].name,elemEmojis[ELEMENT_AIR],elemNames[ELEMENT_AIR]),emoji='<:liaWeap:908859908034793552>')
liaExWeap = weapon("Akashi","noneweap",RANGE_MELEE,AREA_CIRCLE_1,power=25,accuracy=90,magie=20,agility=20,resistance=10,area=AREA_ARC_1,emoji=liaKatana.emoji,ignoreAutoVerif=True,use=MAGIE,effects=liaExWeapEff)
liaExDotOnTarget = effect("U~indobaito","liaExDotOnTarget",MAGIE,power=80,turnInit=8,lvl=8,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji='<:airKitsune:917670912646602823>')
liaExSkill1_3_ready = effect("Harikenburedo préparé","liaSkill1_3_ready",turnInit=5,emoji='<:liaSki1_3:1012765729554178138>')
liaExSkill1_3 = skill("Harikenburedo","liaExSkill1",TYPE_DAMAGE,power=90,use=MAGIE,emoji='<:liaSki1_3:1012765729554178138>',range=AREA_CIRCLE_1,area=AREA_LINE_2,effects=liaExDotOnTarget,accuracy=120,description="Dernier coup du combo Lame des vents\nInflige des dégâts aux ennemis ciblé et inflige {0} __{1}__ à la cible principale, lui infligeant des dégâts continues pendant {2} tours".format(liaExDotOnTarget.emoji[0][0],liaExDotOnTarget.name,liaExDotOnTarget.turnInit),needEffect=[liaExSkill1_3_ready],condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR])
liaExSkill1_2_ready = effect("Sutomubureido préparé","liaSkill1_2_ready",turnInit=5,emoji='<:liaSki1_2:1012761707858382929>')
liaExDotOnSelf = effect("Taifu no me","liaExDotOnSelf",MAGIE,power=60,area=AREA_CIRCLE_3,turnInit=8,lvl=8,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,emoji='<:windBite:961185646993637476>')
liaExSkill1_2 = skill("Sutomubureido","liaExSkill1",TYPE_DAMAGE,use=MAGIE,emoji='<:liaSki1_2:1012761707858382929>',power=80,accuracy=120,range=AREA_MONO,area=AREA_CIRCLE_3,effectOnSelf=liaExSkill1_3_ready,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_MONO,liaExDotOnSelf],needEffect=[liaExSkill1_2_ready],condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],description="Second coup du combo Lame des vents\nInflige des dégâts aux ennemis autour de vous et vous octroi {0} __{1}__, infligeant des dégâts aux ennemis autour de vous lorsque vous terminez votre tour pendant {2} tours".format(liaExDotOnSelf.emoji[0][0],liaExDotOnSelf.name,liaExDotOnSelf.turnInit))
liaExSkill1_1_eff = copy.deepcopy(dmgUp)
liaExSkill1_1_eff.power, liaExSkill1_1_eff.turnInit = 15, 8
liaExSkill1_1 = skill("Kaze no ha","liaExSkill1",TYPE_DAMAGE,use=MAGIE,power=75,emoji='<:liaSki1_1:1012761673427333120>',effectOnSelf=liaExSkill1_2_ready,effectAroundCaster=[TYPE_BOOST,AREA_MONO,liaExSkill1_1_eff],rejectEffect=[liaExSkill1_2_ready,liaExSkill1_3_ready],condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],range=AREA_CIRCLE_1,description="Premier coup du combo Lame des vents\nInflige des dégâts à l'ennemi ciblé et augmente vos dégâts infligés de 15% pendant 8 tours")
liaExSkill1 = skill("Combo Lame des vents","liaExSkill1",TYPE_DAMAGE,use=MAGIE,emoji='<:liaSki1_3:1012765729554178138>',become=[liaExSkill1_1,liaExSkill1_2,liaExSkill1_3],description="Permet d'effectuer le combo Lame des Vents.\n\n{0} __{1}__ augmente les dégâts infligés,\n{2} __{3}__ vous octroi un effet de dégâts indirects infligeant des dégâts autour de vous en fin de tour\n{4} __{5}__ inflige un effet de dégâts indirect à la cible, lui infligeant des dégâtts lorsqu'il débute son tour".format(liaExSkill1_1.emoji,liaExSkill1_1.name,liaExSkill1_2.emoji,liaExSkill1_2.name,liaExSkill1_3.emoji,liaExSkill1_3.name))
liaExSkill2_2_ready = effect("Shapuchajido préparé","liaExSkill2_2_ready",turnInit=5,emoji='<:liaCounter:998001563379437568>')
liaExSkill2_2_e = effect("Arashi no kaze","lizExSkill2_2_e",AGILITY,power=100,area=AREA_CIRCLE_3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,emoji='<:liaSamLB2:1100185041306386439>')
liaExSkill2_2 = skill("Shapuchajido","liaExSkill2",TYPE_DAMAGE,cooldown=3,power=120,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],range=AREA_CIRCLE_4,tpBehind=True,replay=True,use=AGILITY,emoji='<:liaCounter:998001563379437568>',needEffect=[liaExSkill2_2_ready],effects=[liaExSkill2_2_e],description="Vous téléporte derrière l'ennemi ciblé, lui inflige des dégâts en ignorant une grosse partie de sa résistance et inflige des dégâts aux ennemis environant",percing=50,url=demolish.url)
liaExSkill2_1 = skill("Terukikku","liaExSkill2",TYPE_DAMAGE,power=100,range=AREA_CIRCLE_4,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],area=AREA_CONE_2,tpCac=True,jumpBack=3,description="Charge l'ennmi ciblé, lui inflige des dégâts et le repousse de 3 cases\nVous octroi également la possibilité d'utiliser {0} __{1}__ une fois durant les {2} prochains tours".format(liaExSkill2_2.emoji,liaExSkill2_2.name,liaExSkill2_2.needEffect[0].turnInit),effectOnSelf=liaExSkill2_2.needEffect[0],rejectEffect=[liaExSkill2_2_ready],emoji='<:liaSkill:922291249002709062>')
liaExSkill2 = skill("Terukikku +","liaExSkill2",TYPE_DAMAGE,power=liaExSkill2_1.power,use=AGILITY,emoji=liaExSkill2_1.emoji,become=[liaExSkill2_1,liaExSkill2_2],description="Inflige des dégâts agilité à l'ennemi ciblé.\n\n{0} __{1}__ permet de rejouer son tour\n{2} __{3}__ ne peut pas être utilisé pendant 4 tours après utilisation".format(liaExSkill2_2.emoji, liaExSkill2_2.name, liaExSkill2_1.emoji, liaExSkill2_1.name))
liaExSkill3_eff = effect("Hariken no me","liaExSkill3_eff",MAGIE,area=AREA_DIST_5,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji="<:liaTornadoEff2:1100185833115492402>",power=135,lvl=5,turnInit=5)
liaExSkill3 = skill("Hariken","liaExSkill3",TYPE_DAMAGE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],power=100,range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=5,use=MAGIE,effectOnSelf=liaExSkill3_eff,emoji=liaExSkill3_eff.emoji[0][0],description="Inflige et repousse les ennemis en mêlée et vous octroi un effet infligeant des dégâts aux ennemis éloignés à la fin de votre tour pendant 3 tour",knockback=2)
liaExSkill4_3 = skill("Keifu","liaExSkill4",TYPE_DAMAGE,power=100,effectAroundCaster=[TYPE_HEAL,AREA_MONO,150],use=MAGIE,cooldown=5,description="Inflige des dégâts aux ennemis alliégné avec vous et vous soigne",area=AREA_INLINE_5,range=AREA_MONO,emoji="<:waterKitsune:917670866626707516>")
liaExSkill4_2_eff = effect("Asuama","liaExSkill4_2_eff",MAGIE,overhealth=100,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji='<:liaWindArmor:1013901987303149630>')
liaExSkill4_2 = skill("Sunaarashi","liaExSkill4",use=MAGIE,types=TYPE_DAMAGE,power=125,range=AREA_MONO,area=AREA_CIRCLE_2,effectOnSelf=liaExSkill4_2_eff,cooldown=liaExSkill4_3.cooldown, emoji="<:earthKitsune:917670882586017792>", description="Inflige des dégâts aux ennemis en mêlée et vous octroi une armure pendnant 3 tours")
liaExSkill4_1_dot = effect("Moeta","liaExSkill4_1_dot",MAGIE,power=35,turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE)
liaExSkill4_1 = skill("Sabaku no kaze","liaExSkill4",TYPE_DAMAGE,area=AREA_ALL_ENEMIES,use=MAGIE,range=AREA_MONO,power=25,description="Inflige des dégâts à tous les ennemis et leur inflige un effet de dégâts indirect pendant 3 tours",effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_ALL_ENEMIES,liaExSkill4_1_dot],cooldown=liaExSkill4_3.cooldown,emoji='<:fireKitsune:917670925904785408>')
liaExSkill4 = skill("Kyodai no kyoka","liaExSkill4",TYPE_DAMAGE,use=MAGIE,initCooldown=2,power=max(liaExSkill4_3.power,liaExSkill4_2.power,liaExSkill4_1.power+liaExSkill4_1_dot.power*liaExSkill4_1_dot.turnInit),become=[liaExSkill4_1,liaExSkill4_2,liaExSkill4_3],emoji='<:kitsuWeap:935553775500947486>',description="Permet d'utiliser les éléments des soeurs de Lia pour déclancher une attaque suivant leur élément.\n\n{0} __{1}__ vous soigne en plus d'infliger des dégâts\n{2} __{3}__ vous octroi une armure en plus d'infliger des dégâts".format(liaExSkill4_3.emoji,liaExSkill4_3.name,liaExSkill4_2.emoji,liaExSkill4_2.name))
liaExUlt_4 = skill("Kaze no bakuhatsu","liaExUlt_4",TYPE_DAMAGE,power=110,cooldown=7,ultimate=True,area=AREA_CIRCLE_1,range=AREA_CIRCLE_3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],emoji='<:liaSkiUlt3:1013889062962217021>',description="Au premier tour, inflige des dégâts aux ennemis en mêlée et les repoussent.\nAu second tour, inflige à deux reprises des dégâts dans une zone en arc de cercle centrée sur l'ennemi ciblé, repoussant les ennemis touchés et vous téléportant au corps à corps de la cible à chaque reprise, puis inflige des dégâts en cercle autour de l'ennemi ciblé\n\nChaque effet {0} __{1}__ possédé au premier tour vous octroi une armure équivalante à **5%** de vos PV Max\nChaque effet {0} __{1}__ possédé augmente les puissances des attaques en arc de cercle du second tour de **10%**\nChaque effet {0} __{1}__ possédé augmente la puissance de l'attaque de zone de **15%** et les consommes pour vous soigner de **5%** de vos PV max".format(tablElemEff[ELEMENT_AIR].emoji[0][0],tablElemEff[ELEMENT_AIR].name),accuracy=200,use=MAGIE)
liaExUlt_4_cast = effect("Enchainement - {replicaName}","liaExUlt_4_c",replique=liaExUlt_4,silent=True)
liaExUlt_3 = skill("Gyakufu no suraisu","liaExUlt_3",TYPE_DAMAGE,power=70,area=AREA_ARC_3,tpCac=True,knockback=1,range=liaExUlt_4.range,condition=liaExUlt_4.condition,description=liaExUlt_4.description,cooldown=liaExUlt_4.cooldown,replay=True,effectOnSelf=liaExUlt_4_cast,emoji='<:liaSkiUlt2:1013889034600329246>',use=MAGIE)
liaExUlt_3_cast = effect("Enchainement - {replicaName}","liaExUlt_3_c",replique=liaExUlt_3,silent=True)
liaExUlt_2 = skill("Kaze no suraisu","liaExUlt_2",TYPE_DAMAGE,power=70,area=AREA_ARC_3,tpCac=True,knockback=1,range=liaExUlt_4.range,condition=liaExUlt_4.condition,description=liaExUlt_4.description,cooldown=liaExUlt_4.cooldown,replay=True,effectOnSelf=liaExUlt_3_cast,emoji='<:liaSkiUlt1:1013889002731995246>',use=MAGIE)
liaExUlt_2_cast = effect("Cast - {replicaName}","liaExult_2_c",turnInit=2,silent=True,replique=liaExUlt_2)
liaExUlt_1 = skill("Ririsu","liaExUlt",TYPE_DAMAGE,power=25,range=AREA_CIRCLE_3,ultimate=True,area=AREA_CIRCLE_2,areaOnSelf=True,cooldown=liaExUlt_4.cooldown,effectOnSelf=liaExUlt_2_cast,emoji='<:liaSkiUlt0:1013889091831599178>',description=liaExUlt_4.description,condition=liaExUlt_4.condition,knockback=3,use=MAGIE)
liaExSkill6 = skill("Déployable - Tatsumaki","liaExSkill6",TYPE_DEPL,emoji='<:liaDepl:1013912739728592896>',use=MAGIE,range=AREA_CIRCLE_2,cooldown=7,depl=liaTornade,description="Invoque une tornade sur la cellule ciblée, infligeant des dégâts à chaque début de table aux ennemis à portée",condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR])
liaExSkill7_eff = effect("Kaze no shinkiro","liaExSkill7_e",emoji='<:liaSki6:1013891089662488596>',dodge=100,counterOnDodge=100)
liaExSkill7 = skill("Kaze no shinkiro","liaExSkill7",TYPE_ARMOR,effects=liaExSkill7_eff,cooldown=5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],use=None,range=AREA_MONO,emoji='<:liaSki6:1013891089662488596>',description="Augmente votre probabilité d'esquive et de contre-attaque de **100%** jusqu'à votre prochain tour")

# Klironovia
kliWeapEff = effect("Représaille","kliWeapEff",block=35,counterOnBlock=40,turnInit=-1,emoji='<:represailles:1101242340523397191>',description="Augmente votre probabilité de bloquer une attaque et celle de contre attaquer lors d'un blocage")
kliWeap = weapon("Pistolame Vangeresse","kliWeap",RANGE_MELEE,AREA_CIRCLE_1,80,100,strength=20,endurance=10,resistance=10,ignoreAutoVerif=True,emoji='<:kGunblade:1100679173980291082>',)

kliSkill1Eff = effect("Frappe Explosive","kliSkill1Eff",STRENGTH,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,power=50,emoji='<:exploShotEff:1049704001257619476>',lifeSteal=35)
kliSkill1_32 = skill("Perforation","gwenSkill1",TYPE_DAMAGE,power=50,range=AREA_CIRCLE_1,effects=kliSkill1Eff,emoji='<:klSecCb3:1080152258177662976>',effPowerPurcent=120)
kliSkill1_32c = effect("Enchaînement - {replicaName}","kliSkill1_32c",silent=True,replique=kliSkill1_32)
kliSkill1_31r = effect("Serre Visieuse préparée","kliSkill1_31r",turnInit=3,silent=True,emoji='<:klMainCb3:1080150358225080341>')
kliSkill1_31 = skill("Serre Visieuse","gwenSkill1",TYPE_DAMAGE,power=80,range=AREA_CIRCLE_1,effectOnSelf=kliSkill1_32c,needEffect=kliSkill1_31r,replay=True,emoji='<:klMainCb3:1080150358225080341>',description="Inflige des dégâts à l'ennemi ciblé, enchaîne avec une autre attaque directe puis inflige des dégâts indirects supplémentaire qui convertie une partie des dégâts infligés en soins")
kliSkill1_22 = skill("Lacération","gwenSkill1",TYPE_DAMAGE,power=40,range=AREA_CIRCLE_1,effectOnSelf=kliSkill1_31r,effects=kliSkill1Eff,emoji='<:klSecCb2:1080152065625571388>',effPowerPurcent=110)
kliSkill1_22c = effect("Enchaînement - {replicaName}","kliSkill1_22c",silent=True,replique=kliSkill1_22)
kliSkill1_21r = effect("Griffe Sauvage préparée","kliSkill1_21r",turnInit=3,silent=True,emoji='<:klMainCb2:1080150320107233390>')
kliSkill1_21 = skill("Griffe Sauvage","gwenSkill1",TYPE_DAMAGE,power=70,range=AREA_CIRCLE_1,effectOnSelf=kliSkill1_22c,needEffect=kliSkill1_21r,replay=True,emoji='<:klMainCb2:1080150320107233390>',description=kliSkill1_31.description)
kliSkill1_12 = skill("Eventration","gwenSkill1",TYPE_DAMAGE,power=30,range=AREA_CIRCLE_1,effectOnSelf=kliSkill1_21r,effects=kliSkill1Eff,emoji='<:klSecCb1:1080152158479061093>',effPowerPurcent=100)
kliSkill1_12c = effect("Enchaînement - {replicaName}","kliSkill1_12c",silent=True,replique=kliSkill1_12)
kliSkill1_11r = effect("Croc Pugace préparée","kliSkill1_11r",turnInit=3,silent=True,emoji='<:klMainCb1:1080150284514373722>')
kliSkill1_11 = skill("Croc Pugace","gwenSkill1",TYPE_DAMAGE,power=60,range=AREA_CIRCLE_1,effectOnSelf=kliSkill1_12c,needEffect=kliSkill1_11r,replay=True,emoji='<:klMainCb1:1080150284514373722>',description=kliSkill1_31.description)
kliSkill1 = skill("Combo Perforation Explosive","gwenSkill1",TYPE_DAMAGE,become=[kliSkill1_11,kliSkill1_21,kliSkill1_31],emoji=kliSkill1_32.emoji)

gwenyWeapEff = effect("Nébuleuse","kliWeapEff",block=50,turnInit=-1,emoji='<:nebuleuse:1105170021581336727>',description="Augmente grandement votre porbabilité de bloquer les attaques")
gwenyWeap = weapon("Pistolame Renforçante","kliWeap",RANGE_MELEE,AREA_CIRCLE_1,80,100,strength=10,endurance=10,resistance=20,ignoreAutoVerif=True,emoji='<:gGunblade:1100679196436594759>',effects=gwenyWeapEff)

gwenySkill1_32 = skill("Perforation","gwenSkill1",TYPE_DAMAGE,power=50,range=AREA_CIRCLE_1,emoji='<:gwSecCb3:1080152231153778699>',armorConvert=150)
gwenySkill1_32c = effect("Enchaînement - {replicaName}","gwenySkill1_32c",silent=True,replique=gwenySkill1_32)
gwenySkill1_31r = effect("Serre Visieuse préparée","gwenySkill1_31r",turnInit=3,silent=True,emoji='<:klMainCb3:1080150358225080341>')
gwenySkill1_31 = skill("Serre Visieuse","gwenSkill1",TYPE_DAMAGE,power=80,range=AREA_CIRCLE_1,effectOnSelf=gwenySkill1_32c,needEffect=gwenySkill1_31r,replay=True,emoji='<:klMainCb3:1080150358225080341>',description="Inflige des dégâts à l'ennemi ciblé puis enchaîne avec une autre attaque direct qui convertie les dégâts infligés en armure")
gwenySkill1_22 = skill("Lacération","gwenSkill1",TYPE_DAMAGE,power=40,range=AREA_CIRCLE_1,effectOnSelf=gwenySkill1_31r,emoji='<:gwSecCb2:1080152032813535353>',armorConvert=150)
gwenySkill1_22c = effect("Enchaînement - {replicaName}","gwenySkill1_22c",silent=True,replique=gwenySkill1_22)
gwenySkill1_21r = effect("Griffe Sauvage préparée","gwenySkill1_21r",turnInit=3,silent=True,emoji='<:klMainCb2:1080150320107233390>')
gwenySkill1_21 = skill("Griffe Sauvage","gwenSkill1",TYPE_DAMAGE,power=70,range=AREA_CIRCLE_1,effectOnSelf=gwenySkill1_22c,needEffect=gwenySkill1_21r,replay=True,emoji='<:klMainCb2:1080150320107233390>',description=gwenySkill1_31.description)
gwenySkill1_12 = skill("Eventration","gwenSkill1",TYPE_DAMAGE,power=30,range=AREA_CIRCLE_1,effectOnSelf=gwenySkill1_21r,emoji='<:gwSecCb1:1080152129613869078>',armorConvert=150)
gwenySkill1_12c = effect("Enchaînement - {replicaName}","gwenySkill1_12c",silent=True,replique=gwenySkill1_12)
gwenySkill1_11r = effect("Croc Pugace préparée","gwenySkill1_11r",turnInit=3,silent=True,emoji='<:klMainCb1:1080150284514373722>')
gwenySkill1_11 = skill("Croc Pugace","gwenSkill1",TYPE_DAMAGE,power=60,range=AREA_CIRCLE_1,effectOnSelf=gwenySkill1_12c,needEffect=gwenySkill1_11r,replay=True,emoji='<:klMainCb1:1080150284514373722>',description=gwenySkill1_31.description)
gwenySkill1 = skill("Combo Perforation Renforçante","gwenSkill1",TYPE_DAMAGE,become=[gwenySkill1_11,gwenySkill1_21,gwenySkill1_31],emoji=gwenySkill1_32.emoji)

altySkill1_32 = skill("Perforation","gwenSkill1",TYPE_DAMAGE,power=50,range=AREA_CIRCLE_1,emoji='<:alSecCb3:1080152283670650931>',lifeSteal=100,aoeLifeSteal=65)
altySkill1_32c = effect("Enchaînement - {replicaName}","altySkill1_32c",silent=True,replique=altySkill1_32)
altySkill1_31r = effect("Serre Visieuse préparée","altySkill1_31r",turnInit=3,silent=True,emoji='<:klMainCb3:1080150358225080341>')
altySkill1_31 = skill("Serre Visieuse","gwenSkill1",TYPE_DAMAGE,power=80,range=AREA_CIRCLE_1,effectOnSelf=altySkill1_32c,needEffect=altySkill1_31r,replay=True,emoji='<:klMainCb3:1080150358225080341>',description="Inflige des dégâts à l'ennemi ciblé puis enchaîne avec une autre attaque direct qui convertie les dégâts infligés en soins pour vous et vos alliés proches")
altySkill1_22 = skill("Lacération","gwenSkill1",TYPE_DAMAGE,power=40,range=AREA_CIRCLE_1,effectOnSelf=altySkill1_31r,emoji='<:alSecCb2:1080152099549098016>',lifeSteal=100,aoeLifeSteal=65)
altySkill1_22c = effect("Enchaînement - {replicaName}","altySkill1_22c",silent=True,replique=altySkill1_22)
altySkill1_21r = effect("Griffe Sauvage préparée","altySkill1_21r",turnInit=3,silent=True,emoji='<:klMainCb2:1080150320107233390>')
altySkill1_21 = skill("Griffe Sauvage","gwenSkill1",TYPE_DAMAGE,power=70,range=AREA_CIRCLE_1,effectOnSelf=altySkill1_22c,needEffect=altySkill1_21r,replay=True,emoji='<:klMainCb2:1080150320107233390>',description=altySkill1_31.description)
altySkill1_12 = skill("Eventration","gwenSkill1",TYPE_DAMAGE,power=30,range=AREA_CIRCLE_1,effectOnSelf=altySkill1_21r,emoji='<:alSecCb1:1080152189806325822>',lifeSteal=100,aoeLifeSteal=65)
altySkill1_12c = effect("Enchaînement - {replicaName}","altySkill1_12c",silent=True,replique=altySkill1_12)
altySkill1_11r = effect("Croc Pugace préparée","altySkill1_11r",turnInit=3,silent=True,emoji='<:klMainCb1:1080150284514373722>')
altySkill1_11 = skill("Croc Pugace","gwenSkill1",TYPE_DAMAGE,power=60,range=AREA_CIRCLE_1,effectOnSelf=altySkill1_12c,needEffect=altySkill1_11r,replay=True,emoji='<:klMainCb1:1080150284514373722>',description=altySkill1_31.description)
altySkill1 = skill("Combo Perforation Régénérante","gwenSkill1",TYPE_DAMAGE,become=[altySkill1_11,altySkill1_21,altySkill1_31],emoji=altySkill1_32.emoji)

krysWaterWeakness = effect("KrysTal","krysWaterWeakness",power=10,armorDmgBonus=0.10,turnInit=-1,unclearable=True,description="Augmente de **{0}%** les dégâts subis des compétences **Eau** mais augmente d'autant les dégâts sur armure infligés",emoji=krystalisation.emoji)
krysWeapon = copy.deepcopy(krystalFist)
krysWeapon.effects=krysWaterWeakness

lioExWeap = weapon("AquaMage","noneWeap",RANGE_LONG,AREA_CIRCLE_5,0,0,charisma=35)
lioExSkill1 = skill("AquaStrike","lioExSkill1",TYPE_DAMAGE,power=80,use=CHARISMA,emoji='<:water2:1065647727708483654>',description="Un sort simple qui inflige des dégâts à l'ennemi ciblé")
lioExSkill2_eff = effect("VibrAqua","lioExSkill2_eff",CHARISMA,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,area=AREA_DONUT_2,power=85,emoji='<:water3:1065647689129271397>')
lioExSkill2 = skill("VibrAqua","lioExSkill2",TYPE_DAMAGE,power=120,effects=lioExSkill2_eff,cooldown=5,emoji='<:vibraqua:1123874146678489118>',effectAroundCaster=[TYPE_HEAL,AREA_LOWEST_HP_ALLIE,100],description="Inflige des dégâts à l'ennemi ciblé, des dégâts indirects autour de lui et soigne  votre allié le plus blessé")
lioExSkill3_eff1, lioExSkill3_eff2 = copy.deepcopy(defenseUp), effect("AquaPurification","lioExSkill3_eff2",CHARISMA,power=40,turnInit=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji='<:water1:1065647748826791966>')
lioExSkill3_eff1.power, lioExSkill3_eff1.stat, lioExSkill3_eff1.turnInit = 3.5, CHARISMA, lioExSkill3_eff2.turnInit
lioExSkill3 = skill("AquaVoile","lioExSKill3",TYPE_INDIRECT_HEAL,effects=[lioExSkill3_eff2,lioExSkill3_eff1],cooldown=3,emoji=lioExSkill3_eff1.emoji[0][0],effPowerPurcent=150,description="Octroi un effet régénérant et réduit les dégâts subis par l'allié ciblé")
lioExSkill4_eff1 = effect("Charme","lioExSkill4_eff1",trigger=TRIGGER_INSTANT,area=AREA_DONUT_3,callOnTrigger=charming2,emoji='<:waterKitsune:917670866626707516>')
lioExSkill4_eff2 = effect("Charme","lioExSkill4_eff2",trigger=TRIGGER_INSTANT,area=AREA_LINE_5,callOnTrigger=charming,emoji='<:waterKitsune:917670866626707516>')
lioExSkill4 = skill("Gekiryū","lioExSkill4",TYPE_DAMAGE,power=135,use=CHARISMA,area=lioExSkill4_eff2.area,effects=lioExSkill4_eff2,effectOnSelf=lioExSkill4_eff1,effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_CIRCLE_2,lioExSkill3_eff2],cooldown=5,ultimate=True,emoji=lioLB.emoji,url=lioLB.url,description="Inflige des dégâts aux ennemis ciblés, réduit leurs statistiques et augmente celles des alliés alentours tout en leur octroyant un effet régénérant")
lioExSkill5_eff = effect("Oeudème","lioExSKill5_eff",CHARISMA,power=75,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,turnInit=3)
lioExSkill5 = skill("AquaBulle","lioExSkill5",TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_1,effects=lioExSkill5_eff,cooldown=3,effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_LOWEST_HP_ALLIE,lioExSkill3_eff2],emoji='<:lioSkill:922328964926697505>',description="Inflige un effet de dégâts périodiques aux ennemis ciblés et octroi un effet régénérant à l'allié le plus blessé")
lioExSkill6 = skill("Déluge","liaExSkill6",TYPE_DAMAGE,power=80,area=AREA_CIRCLE_2,range=AREA_MONO,knockback=3,cooldown=3,description="Inflige des dégâts aux ennemis ciblés et les repousse",emoji="<:enemyWater:1042313114487636038>")