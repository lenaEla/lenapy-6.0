from constantes import *

# CHIPS
RARITY_COMMUN, RARITY_RARE, RARITY_LEGENDARY, RARITY_MYTHICAL = 0,1,2,3
rarityMinLvl, CHIP_MAX_LEVEL, rarityEmojis = (0,3,6,9), 15, ("<:communChip:1217187986085646427>","<:rareChip:1217188006679810058>","<:legendaryChip:1217344108599967764>","<:mythicalChip:1220026683634094102>")
nbChipsForLvlUp = [1,1,2,5,10,25,40,65,80,100,150,200,300,400,500,500,500]

chipIdCount = 0

class chip():
    def __init__(self, name:str, emoji:str, rarity:int, description:str, minValue=0, maxValue=0):
        self.name, self.emoji, self.rarity, self.description = name,emoji,rarity,description
        self.minValue,self.maxValue = minValue,maxValue
        
        global chipIdCount
        self.id = chipIdCount
        chipIdCount += 1

    def __str__(self):
        return "{0} {1}".format(self.emoji, self.name)

class userChip(chip):
    def __init__(self,chipObj:chip,character,lvl:int=0,progress:int=0):
        for k, v in chipObj.__dict__.items():
            setattr(self,k,v)
        self.user = character
        self.lvl, self.progress, self.power = lvl, progress, min(max(round(self.minValue + ((self.maxValue-self.minValue)*(lvl-(rarityMinLvl[self.rarity])) / (CHIP_MAX_LEVEL-rarityMinLvl[self.rarity]-1)),2), self.minValue), self.maxValue)
        if math.modf(self.power)[0]==0:
            self.power = int(self.power)

    def addProgress(self,value:int,user=None):
        toReturn = False
        if self.lvl < CHIP_MAX_LEVEL:
            self.progress += value
            while self.progress >= nbChipsForLvlUp[self.lvl-rarityMinLvl[self.rarity]]:
                self.progress -= nbChipsForLvlUp[self.lvl-rarityMinLvl[self.rarity]]
                self.lvl += 1
                toReturn = True
        else:
            user.tc += [1,3,5,10][self.rarity]
        return toReturn, user

    def formatDescription(self):
        listFormat, listReplace = ["%power","%lvlPower"], [self.power,int(self.power*self.user.level/100)]
        toReturn = self.description
        for cmpt in range(len(listFormat)):
            try:
                toReturn = toReturn.replace(listFormat[cmpt],str(listReplace[cmpt]))
            except Exception as e:
                print("Could not format de {0} key {2}: {1}".format(listFormat[cmpt]),e,listReplace[cmpt])
        return toReturn

    def __str__(self):
        return "{0} {1} Lvl{2} Progress{3}".format(self.emoji, self.name, self.lvl, self.progress)

chipList = [
    chip("Force augmentée I",statsEmojis[STRENGTH],RARITY_COMMUN,"Augmente votre **Force** de **%power%** de votre niveau (**%lvlPower**)",25,60),
    chip("Force augmentée II",statsEmojis[STRENGTH],RARITY_COMMUN,"Augmente votre **Force** de **%power%**",5,10),
    chip("Endurance augmenté I",statsEmojis[ENDURANCE],RARITY_COMMUN,"Augmente votre **Endurance** de **%power%** de votre niveau (**%lvlPower**)",25,60),
    chip("Endurance augmenté II",statsEmojis[ENDURANCE],RARITY_COMMUN,"Augmente votre **Endurance** de **%power%**",5,10),
    chip("Charisme augmenté I",statsEmojis[CHARISMA],RARITY_COMMUN,"Augmente votre **Charisme** de **%power%** de votre niveau (**%lvlPower**)",25,60),
    chip("Charisme augmenté II",statsEmojis[CHARISMA],RARITY_COMMUN,"Augmente votre **Charisme** de **%power%**",5,10),
    chip("Agilité augmentée I",statsEmojis[AGILITY],RARITY_COMMUN,"Augmente votre **Agilité** de **%power%** de votre niveau (**%lvlPower**)",10,40),
    chip("Agilité augmentée II",statsEmojis[AGILITY],RARITY_COMMUN,"Augmente votre **Agilité** de **%power%**",5,10),
    chip("Précision augmentée I",statsEmojis[PRECISION],RARITY_COMMUN,"Augmente votre **Précision** de **%power%** de votre niveau (**%lvlPower**)",10,40),
    chip("Précision augmentée II",statsEmojis[PRECISION],RARITY_COMMUN,"Augmente votre **Précision** de **%power%**",5,10),
    chip("Intelligence augmentée I",statsEmojis[INTELLIGENCE],RARITY_COMMUN,"Augmente votre **Intelligence** de **%power%** de votre niveau (**%lvlPower**)",25,60),
    chip("Intelligence augmentée II",statsEmojis[INTELLIGENCE],RARITY_COMMUN,"Augmente votre **Intelligence** de **%power%**",5,10),
    chip("Magie augmentée I",statsEmojis[MAGIE],RARITY_COMMUN,"Augmente votre **Magie** de **%power%** de votre niveau (**%lvlPower**)",25,60),
    chip("Magie augmentée II",statsEmojis[MAGIE],RARITY_COMMUN,"Augmente votre **Magie** de **%power%**",5,10),
    chip("Renforcement",statsEmojis[RESISTANCE],RARITY_COMMUN,"Augmente votre **Résistance** de **%power** points",2.5,10),
    chip("Pénétration",statsEmojis[PERCING],RARITY_COMMUN,"Augmente votre **Pénétration** de **%power** points",2.5,10),
    chip("Critique universel",statsEmojis[CRITICAL],RARITY_COMMUN,"Augmente votre **probabilité de critique** lors d'une attaque directe, indirecte, en réalisant un soin ou octroyant une armure de **%power%**",2.5,10),
    chip("Constitution I",'<:constB:1028695344059518986>',RARITY_COMMUN,"Augmente vos **Points de Vie** de base de **%power%** de votre niveau (**%lvlPower**)",100,500),
    chip("Constitution II",'<:constB:1028695344059518986>',RARITY_COMMUN,"Augmente vos **Points de Vie** de **%power%**",3.5,10),
    chip("Soins augmentés I",statsEmojis[ACT_HEAL_FULL],RARITY_COMMUN,"Augmente votre statistique d'action de **Soins** de **%power%** de votre niveau (**%lvlPower**)",15,40),
    chip("Soins augmentés II",statsEmojis[ACT_HEAL_FULL],RARITY_COMMUN,"Augmente votre statistique d'action de **Soins** de **%power%**",2.5,7.5),
    chip("Boosts augmenté I",statsEmojis[ACT_BOOST_FULL],RARITY_COMMUN,"Augmente votre statistique d'action de **Boost** de **%power%** de votre niveau (**%lvlPower**)",15,40),
    chip("Boosts augmenté II",statsEmojis[ACT_BOOST_FULL],RARITY_COMMUN,"Augmente votre statistique d'action de **Boost** de **%power%**",2.5,7.5),
    chip("Armures augmenté I",statsEmojis[ACT_SHIELD_FULL],RARITY_COMMUN,"Augmente votre statistique d'action de **Armure** de **%power%** de votre niveau (**%lvlPower**)",15,40),
    chip("Armures augmenté II",statsEmojis[ACT_SHIELD_FULL],RARITY_COMMUN,"Augmente votre statistique d'action de **Armure** de **%power%**",2.5,7.5),
    chip("Directs augmentée I",statsEmojis[ACT_DIRECT_FULL],RARITY_COMMUN,"Augmente votre statistique d'action de **Dégâts Directs** de **%power%** de votre niveau (**%lvlPower**)",15,40),
    chip("Directs augmentée II",statsEmojis[ACT_DIRECT_FULL],RARITY_COMMUN,"Augmente votre statistique d'action de **Dégâts Directs** de **%power%**",2.5,7.5),
    chip("Indirects augmentée I",statsEmojis[ACT_INDIRECT_FULL],RARITY_COMMUN,"Augmente votre statistique d'action de **Dégâts Indirects** de **%power%** de votre niveau (**%lvlPower**)",15,40),
    chip("Indirects augmentée II",statsEmojis[ACT_INDIRECT_FULL],RARITY_COMMUN,"Augmente votre statistique d'action de **Dégâts Indirects** de **%power%**",2.5,7.5),

    chip("Vampirisme I",'<:vampire:900312789686571018>',RARITY_RARE,"Vous recevez des soins équivalents à **%power%** des **dégâts directs** infligés lorsque vous attaquez",10,20),
    chip("Vampirisme II",'<:vampire:900312789686571018>',RARITY_RARE,"Vous recevez des soins équivalents à **%power%** des **dégâts indirects** infligés lorsque vos effets de dégats indirects se déclanchent",10,20),
    chip("Absorbtion",'<:absB:1143285351608221838>',RARITY_RARE,"Augmente les soins et armures reçus d'autrui de **%power%**",2.5,12.5),
    chip("Soins et armures réalisés augmentés",'<:largesse:1086390291055005736>',RARITY_RARE,"Augmente les soins et armures réalisés de **%power%**",2.5,10),
    chip("Dégâts universels augmentés",'<a:dmgBuffB:954429227657224272>',RARITY_RARE,"Augmente tous les dégâts infligés de **%power%**",1,5),
    chip("Dégâts directs augmentés",statsEmojis[ACT_DIRECT_FULL],RARITY_RARE,"Augmente les dégâts directs infligés de **%power%**",2.5,10),
    chip("Dégâts indirects augmentés",statsEmojis[ACT_INDIRECT_FULL],RARITY_RARE,"Augmente les dégâts indirects infligés de **%power%**",2.5,10),
    chip("Convertion",'<:convertion:900311843938115614>',RARITY_RARE,"Vous recevez une armure légère équivalente à **%power%** des **dégâts directs** infligés lorsque vous attaquez",10,20),
    chip("Incurable",'<:incurR:1143285244477317233>',RARITY_RARE,"Les adversaires ciblés directement par vos compétences offensives voient les soins qu'ils reçoivent réduit de **%power%** durant un tour",5,20),
    chip("Friable",'<:abR:934600570633867365>',RARITY_RARE,"Les adversaires ciblés directement par vos compétences offensives voient les armures qu'ils reçoivent réduit de **%power%** durant un tour",5,20),
    chip("Dégâts indirects reçus réduits",'<:inkResB:1143285391009529896>',RARITY_RARE,"Les dégâts indirects que vous subissez sont réduit de **%power%**",5,20),
    chip("Dégâts reçus réduits",'<a:defBuffB:954537632543682620>',RARITY_RARE,"Les dégâts directs et indirects que vous subissez sont réduit de **%power%**",2.5,10),
    chip("Blocage augmenté",'<:shieltron:971787905758560267>',RARITY_RARE,"Augmente votre probabilité de bloquer une attaque directe de **%power%**",5,15),
    chip("Esquive augmentée",'<:quicky:934832147511017482>',RARITY_RARE,"Augmente votre probabilité d'esquiver des attaques directes ennemies de **%power%**",5,15),
    chip("Démolition",'<:demolition:1217142138425315510>',RARITY_RARE,"Augmente les dégâts infligés aux armures adverses de **%power%**",15,35),
    chip("Lame Dissimulée","<:chiphidenBlade:1223632204421140610>",RARITY_RARE,"Augmente les dégâts directs infligés à la cible principale de vos compétence de **%power%** de votre niveau (**lvlPower**)",15,35),

    chip("Cicatrisation","<:chipCicatrisation:1218696306583797851>",RARITY_LEGENDARY,"À la fin de votre tour, vous soigne de l'équivalent de **%power%** de vos PVs maximums",2.5,7.5),
    chip("Lithophage","",RARITY_LEGENDARY,"Vous vous soignez de l'équivalent de **%power%** des dégâts infligés sur de l'armure",15,35),
    chip("Sur-Vie","<:chipOverhealthB:1217345964856311870>",RARITY_LEGENDARY,"Lorsque vous recevez des soins de n'importe quelle source qui excèdent vos PVs max, une armure légère à la valeur équivalente aux soins éxédant vous est octroyé, pour un maximum de **%power%** de vos PVs maximums",10,25),
    chip("Diffraction","<:chipDiffraction:1222633497945182319>",RARITY_LEGENDARY,"En ingligeant une attaque monocible à un adversaire ayant au moins **1** adversaire autour de lui, la puissance de l'attaque est réduite de **%power%**. Les dégâts réduits sont infligés aux ennemis proches de la cible principale",10,25),
    chip("Dispersion","<:explosoins:1016796973636010026>",RARITY_LEGENDARY,"Lorsqu'un adversaire est vaincu, vous infligez un effet de dégâts indirects d'une puissance équivalente à **%power%** de la puissance cumulée de vos effets de dégâts indirects encore présent sur l'adversaire aux ennemis proches",25,45),
    chip("Achèvement","<:assassination:1157411186514596002>",RARITY_LEGENDARY,"Lorsque vous effectuez une attaque directe sur un adversaire ayant moins de **35%** de ses PVs max, la puissance de votre attaque est augmentée de **%power%**",15,30),
    chip("Convertion Vitale","<:chipConvertVital:1217346007558262874>",RARITY_LEGENDARY,"En début de tour, jusqu'à **%power%** de vos PArs sont convertient en soins",10,25),

    chip("Totem de Protection","<:undying:1220101605412835359>",RARITY_MYTHICAL,"Une fois par combat, lorsque vos PVs tombent en dessous de 0, vous soigne immédiatement de **%power%** de vos PVs maximums, vous octroie une armure équivalente à **%power%** de vos PVs maximums, réduit de **50%** vos dégâts subis et vous octroie un effet régénérant équivalent aux soins initiaux durant un petit moment",15,25),
    chip("Bénédiction","<:waterIntents:1185653674781970502>",RARITY_MYTHICAL,"Une fois par combat, lorsque les PVs d'un allié (hors invocation) tombent en dessous de 0, le soigne immédiatement de **%power%** de ses PVs maximums",50,100),
    chip("Plot Armor","<:complicated:945054889573240883>",RARITY_MYTHICAL,"Une fois par combat, en recevant des dégâts mortels, empêche vos PVs de passer en dessous de 1 et augmente vos dégâts infligés de **%power%**",25,50),
    chip("Transgression","<:transgression:1154369057630453780>",RARITY_MYTHICAL,"Après avoir soigné l'équivalent de **100%** de vos PVs max (les soins de zone et/ou indirects contribuent à hauteur de 50%), à la fin de votre tour, inflige __Blessure Profonde__ à tous les ennemis, avec une puissance équivalente à **%power%** de vos PVs max, divisés par le nombre d'ennemis affectés",50,150),
    chip("Overpower","<:sanguisDaemonium:1050059965630533714>",RARITY_MYTHICAL,"Une fois par combat, en utilisant votre compétence ultime, augmente la puissance et/ou celle des effets infligés ou octroyés de **%power%**, mais elle vous coûtera **50%** de vos PVs actuels",25,50),

    chip("Crucifix","<:dvin:1004737746377654383>",RARITY_COMMUN,"Reduit de **%power%** le coût en PVs maximums des compétences divines",10,25),
    chip("Démaniaque","<:dmon:1004737763771433130>",RARITY_COMMUN,"Reduit de **%power%** le coût en PVs courants des compétences démoniaque",10,25),
    chip("Bouclier d'épines","<:chipSpikeShield:1218699342148407409>",RARITY_COMMUN, "Augmente de **%power%** votre probabiliter de contre-attaquer lors d'un blocage",10,20),
    chip("Réflex","<:liaCounter:998001563379437568>",RARITY_COMMUN,"Augmente de **%power%** votre probabiliter de contre-attaquer lors d'une esquive",10,20),
    chip("Châpeau de Roues","<:openingGambit:1217580002120306750>",RARITY_COMMUN,"Lors du premier tour, puis lorsque vos PVs acutels sont supérieurs ou égaux à **90%** de vos PVs maximums, augmente toutes vos statistiques principales de **%power%** de votre niveau (**%lvlPower**)",25,50),
    chip("Ultime Sursaut","<:lastDitchEffort:1216413813079937125>",RARITY_COMMUN,"Lorsque vos PVs acutels sont inférieurs ou égaux à **25%** de vos PVs maximums ou à partir du **Tour 17**, augmente toutes vos statistiques principales de **%power%** de votre niveau (**%lvlPower**)",25,50),
    chip("Spotlight","<:alice:893463608716062760>",RARITY_RARE,"Augmente la puissance de vos effets de boost de statistiques de **%power%**",2.5,10),
    chip("Maître Invocateur","<:sprink1:887747751339757599>",RARITY_RARE,"Augmente les statistiques de base de vos invocations de **%power%**",10,25),
    chip("Barrière","<:chipBarrier:1218696256335908885>",RARITY_RARE,"À chaque tour, réduit les **3** prochaines attaques directes reçus de **%power%** de votre niveau (**%lvlPower**)",20,65),
    chip("Solidité","<:tetebruleConvic:1066010806635995146>",RARITY_RARE,"En subisant des dégâts directs supérieurs ou égaux à **25%** de vos PVs maximums, réduit ceux-ci de **%power%** de votre niveau (**%lvlPower**)",100,350),
    chip("Précaution","<:bpotion:867165268911849522>",RARITY_RARE,"Lors du **Tour 2**, vous octroie un effet régénérant **%power%** de vos PVs maximums en fin de tour durant cinq tours",3.5,10),
    chip("Radiance Toxique","<:chipToxiHeal:1221119824223014924>",RARITY_LEGENDARY,"En fin de tour, soigne les allies autour de vous de **%power%** des dégâts indirects infligés entre vos tours",10,20),
    chip("Présence","<:chipPresence:1221466077943562312>",RARITY_LEGENDARY,"Augmente la probabilité d'être ciblé par les adversaires. De plus, vous soigne en début de tour de l'équivalent de **%power%** des dégâts subis entre deux tours",7.5,15),
    chip("Toxiception","<:chipToxiception:1223595936370917486>",RARITY_MYTHICAL,"En utilisant une compétence de dégâts directs ou indirects, inflige <:toxiEff:1223595956415496213> Toxiception à la cible principale\n> Au début du tour du porteur, augmente les dégâts indirects reçus de **%power%** par effet de dégâts indirects infligés par le lanceur sur le porteur (maximum **30%**)",5,10),
    chip("Ambivalance","<:stopUndoingMyDoings:1154368777476132864>",RARITY_MYTHICAL,"En fin de tour, inflige à l'ennemi le plus blessé des dégâts indirects équivalents à **%power%** des soins réalisés depuis le dernier tour (les soins indirects comptent pour 40% et les soins directs de zone pour 65%)",25,50),
    chip("Armure Initiale","<:armorPack:1063490980759748789>",RARITY_MYTHICAL,"Au début du combat, octroie à toute votre équipe une armure équivalante à **%power%** de vos PVs maximums",20,35),
    chip("Retour de Bâton","<:iliBonk:1220101642259529829>",RARITY_MYTHICAL,"Permet d'utiliser d'utiliser Retour de Bâton\n> Inflige **%lvlPower** + **%power%** dégâts bloqués entre deux utilisations (5 tours)",35,50),
    chip("Appel de la Nuit","<:dmonland:1006455391342829599>",RARITY_MYTHICAL,"Permet d'utiliser Appel de la Nuit\n> Augmente la puissance des compétences démoniaques de votre équipe de **%power%** durant trois tours (7 tours)",20,35),
    chip("Appel de la Lumière","<:ascendance:1051510131105464370>",RARITY_MYTHICAL,"Permet d'utiliser Appel de la Lumière\n> Augmente la puissance des compétences divines de votre équipe de **%power%** durant trois tours (7 tours)",20,35),
    chip("Contre-Offensive",'<:chipOffensifCounter:1218696364855132280>',RARITY_LEGENDARY,"Après avoir bloqué **5** attaques (ou **1** venant d'un boss Stand Alone), les dégâts infligés à la cible principale de votre prochaine compétence sont augmentés d'une valeur équivalente à **%power%** de votre niveau (**%lvlPower**)",125,650),
    chip("Héritage d'Estialba","<:estialLegacy:1191001141304119376>",RARITY_LEGENDARY,"Augmente de **%power%** le vol de vie de vos effets de dégâts indirects psychiques",10,20),
    chip("Héritage Lesath","<:lesathLegacy:1191001162300801095>",RARITY_LEGENDARY,"Augmente de **%power%** le vol de vie de vos effets de dégâts indirects physiques",10,20),
    chip("Dissimulation","<:dissi:1029816091020640346>",RARITY_RARE,"Diminue la probabilité d'être ciblé par les adversaires. De plus, votre première attaque du tour inflige **%power%** de dégâts supplémantaire à la cible principale si elle ne vous pas infligé de dégâts le tour précédent et que vous vous trouvez à son corps à corps",25,40),
    chip("Goût du Sang","<:bloodpact:937361536043843595>",RARITY_RARE,"En fin de tour, vous soigne de l'équivalent de **%power%** des dégâts infligés ou des soins réduits avec l'effet Blessure Profonde",20,50),
    chip("Lune de Sang","<:BloodMoon:1094026774448443512>",RARITY_LEGENDARY,"Lorsque vous infligez des dégâts directs, les cibles subbissent Blessure Profonde avec une valeur équivalente à **%power%** des dégâts infligés en plus",5,15),
    chip("Précision Chirurgicale","<:preciChiru:951692831230140437>",RARITY_COMMUN,"Augmente les soins et armures critiques réalisés de **%power%**",5,12.5),
    chip("Précision Critique","<:critB:925763298346033193>",RARITY_COMMUN,"Augmente les dégâts critiques infligés de **%power%**",5,10),
    chip("Camalataque","<:chipCalamataque:1221474463300976670>",RARITY_RARE,"Lorsque vous utilisez une compétence vous faisant sauter au corps à corps d'un ennemi ou les attirants sur vous, inflige des dégâts indirects Harmonie avec une puissance équivalente à **%power%** de votre niveau (**%lvlPower**)",20,40),
    chip("Un pour tous","<:royaleShield:1163510613255925931>",RARITY_LEGENDARY,"Vos compétences d'armures augmentent également la résistance des cibles de **%power** points, réduit de 60% pour les compétences de zone",7.5,15),
    chip("Bouclier Sacrificiel","<:chipsBarrier:1218078941034840095>",RARITY_MYTHICAL,"Lorsqu'un de vos alliés a moins de **35%** de ses PV maximums, redirige sur vous **%power%** des dégâts directes qu'il reçoit",50,100),
    chip("Altruisme","<:altyCover:988767335974326272>",RARITY_RARE,"Réduit les dégâts subis suite à une redirection des dégâts directs reçus d'un allié sur vous de **%power%**",20,50),
    chip("Médaille de la Chauve-Souris","<:bat1:884519906819862568>",RARITY_RARE,"Tous les trois tours à partir du tour 1, invoque une **Chauve-souris** à vos côtés. Cette dernière voit ses PVs maximums et ses dégâts infligés augmenter de **%power%**",10,25),
    chip("Symbiose","<:batPrincess:1197056891688321094>",RARITY_MYTHICAL,"Lorsque vous utilisez une compétence de **Boosts** sur vous-mêmes, les zones d'effets de la compétences sont répliquées sur vos invocations avec une puissance équivalente à **%power%** de la compétence de base. Les zones d'effets ne peuvent se cumuler",25,50),
    chip("Aura Galvanisante","<:voixDivine:1085991767834370108>",RARITY_LEGENDARY,"En fin de tour, augmente les statistiques principales des alliés proches de **%power%** jusqu'à votre prochain tour",3,10),
    chip("Armure Solide","",RARITY_RARE,"Lorsqu'une de vos armures est détruite, celle-ci absorbe l'équivalent de **%power%** de votre niveau (**%lvlPower**) dégâts supplémentaire",25,65),
    chip("Pas Piégés","<:chipSurprise:1227279072451629237>",RARITY_LEGENDARY,"Lorsque vous êtes déplacés par une compétence ennemie, déploie une Petite Mine sur le sol. En utilisant une compétence vous faisant sauter sur l'adversaire ou sauter en arrière, lui inflige l'effet Petite Mine. La Petite Mine inflige des dégâts **Force** avec une puissance de **%power** lorsqu'un ennemi marche à proximité, après 3 tours ou si le porteur est déplacé",20,40),
    chip("Haut-Perceur 5.1","<:kwB:933510332733882378>",RARITY_RARE,"Tous les trois tours à partir du tour 1, invoque un **Haut-Perceur 5.1** à vos côtés. Celui-ci voit ses PVs maximums et ses dégâts infligés augmenter de **%power%**",10,25),
    chip("Cadeau Explosif","<:terrabombB:1155475225979408454>",RARITY_RARE,"Tous les trois tours à partir du tour 1, invoque une **Petite Bombe** autour de vous. Celui-ci voit ses PVs maximums et ses dégâts infligés augmenter de **%power%**",10,25),
    chip("Rentre-Dedans","<:angelStrike:1233110358445789235>",RARITY_RARE,"Augmente la puissance de vos compétences vous faisant sauter dedans ou derrière une cible de **%power**",15,25),
    chip("Bout-Portant","<:shortTeleport:1233097703832162324>",RARITY_LEGENDARY,"Une fois par tour et si l'ennemi ciblé se trouve à votre corps à corps, augmente la puissance de votre attaque de **%power**",15,35),
    chip("Empathie","<:oneforall:893295824761663488>",RARITY_RARE,"Réduit la puissance des attaques de zone dont vous êtes la cible principale et qui touchent d'autres alliés de **%power%**",5,20),
    chip("Sourire Agile","<:niceSmile:1257711547145519145>", RARITY_LEGENDARY,"Lorsque vous esquivez une attaque, vous avez **%power%** de chance d'infliger l'effet Charmé (50%) à l'attaquant. Certaines conditions peuvent faire varier cette probabilité", 20, 50),
    chip("Sourire Mazo","<:niceSmile:1257711547145519145>", RARITY_LEGENDARY,"Lorsque vous subissez une attaque, vous avez **%power%** de chance d'infliger l'effet Charmé (50%) à l'attaquant. Certaines conditions peuvent faire varier cette probabilité", 15, 40),
    chip("Sourire Sadique","<:niceSmile:1257711547145519145>", RARITY_LEGENDARY,"Lorsque vous infligez une attaque, vous avez **%power%** de chance d'infliger l'effet Charmé (50%) à la cible. Certaines conditions peuvent faire varier cette probabilité", 10, 30),
    chip("Sourire Bienveillant","<:niceSmile:1257711547145519145>", RARITY_LEGENDARY,"Lorsque vous soignez un équipier, vous avez **%power%** de chance de lui octroyer l'effet Enjolé. Certaines conditions peuvent faire varier cette probabilité", 20, 40),
]

disabled = [
]

chipCommun,chipRare,chipLegend,chipMythic = [],[],[],[]
for tmpChip in chipList:
    [chipCommun,chipRare,chipLegend,chipMythic][tmpChip.rarity].append(tmpChip)

nbAvalibleChips = len(chipList)
rangeChipList = list(range(nbAvalibleChips))
initChipInv = {}
for cmpt in rangeChipList:
    initChipInv[cmpt] = [0,0]

def getChip(*toGet:Union[str,int,list]) -> Union[chip, List[chip]]:
    if toGet[0].__class__ == list:
        toGet = toGet[0]
    toReturn = []
    for toGet1 in toGet:
        if type(toGet1) == chip:
            toReturn.append(toGet1)
        elif type(toGet1) == str and toGet1.isdigit():
            toGet1 = int(toGet1)
        for tmpChip in chipList:
            if tmpChip.id == toGet1 or tmpChip.name == toGet1:
                toReturn.append(tmpChip)
    
    toReturnTemp = None
    if len(toReturn) == 1:
        toReturnTemp = toReturn[0]
    elif len(toReturn) > 1:
        toReturnTemp = toReturn
    #print(toReturn,"returned",toReturnTemp)
    return toReturnTemp

probaRarityTabl = [(690,205,100,5),(350,400,200,50),(50, 450, 400, 100),(50, 350, 450, 150)]