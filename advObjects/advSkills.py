from advObjects.advSkills_1 import *
reaperEff.description += "\n\n" + deathMark.description.splitlines()[-1].replace("{0} __{1}__".format(reaperEff.emoji[0][0],reaperEff.name),"{0} __{1}__".format(deathMark.emoji[0][0],deathMark.name))

hexadecaCombFinal = skill('Hexadecafrappe Enchantée',getAutoId(altyStrike.id,True),TYPE_DAMAGE,use=MAGIE,power=80,range=AREA_CIRCLE_1,emoji='<:sixtyComboFinal:1098615928998080593>',percing=50,affSkillMsg=False,description="Après un tour de chargement, inflige de nombreuses attaques magiques à l'ennemi ciblé. Le dernier coup inflige plus de dégâts et ignore une partie de la résistance adverse",accuracy=200,area=AREA_LINE_3,ultimate=True,cooldown=7)
hexadecaCombFinal_c = effect("Enchaînement - {replicaName}","sixtineCombFin",silent=True,replique=hexadecaCombFinal)
hexadecaComb_1 = skill('Hexadecafrappe Enchantée',hexadecaCombFinal.id,TYPE_DAMAGE,use=MAGIE,power=10,repetition=15,price=750,range=AREA_CIRCLE_1,emoji='<:sixtyCombo1:1098615843048399022>',description=hexadecaCombFinal.description,ultimate=True,cooldown=7,effectOnSelf=hexadecaCombFinal_c,accuracy=101,replay=True)
haxadecaComb_c = effect("Cast - {replicaName}","sixtineCombC",silent=True,turnInit=2,replique=hexadecaComb_1)
hexadecaComb = copy.deepcopy(hexadecaComb_1)
hexadecaComb.power, hexadecaComb.repetition, hexadecaComb.effectOnSelf, hexadecaComb.replay = 0, 1, haxadecaComb_c, False

galvaniseEff = effect("Galvanisation","galvaniseSummon",trigger=TRIGGER_INSTANT,emoji='<:galvanise:1104726746017837106>',iaPow=50,power=1,description="Augmente de **{0}** tour la durée de vie de l'invocation ciblée",type=TYPE_UNIQUE)
sustainEff = effect("Sustain","sustain",stackable=True,stat=HARMONIE,power=40,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji='<:sustain:1104726732663181353>',turnInit=3)
sustain = skill("Sustain",getAutoId(hexadecaCombFinal.id,True),TYPE_INDIRECT_HEAL,price=500,area=AREA_SUMMONS,range=AREA_MONO,effects=[sustainEff,galvaniseEff],cooldown=5,description="Octroi un effet régénérant à vos invocations et augmente leur durée de vie",emoji='<:sustain:1104511188483711037>')
curlEff = copy.deepcopy(defenseUp)
curlEff.stat, curlEff.turnInit, curlEff.power = HARMONIE, 3, 6.5
curl = skill("Curl",getAutoId(sustain.id,True),TYPE_BOOST,price=500,area=AREA_SUMMONS,range=AREA_MONO,effects=[curlEff,galvaniseEff],cooldown=5,description="Réduit les dégâts subis par vos invocations et augmente leur durée de vie",emoji='<:curl:1104511212579999826>')
stimEff1, stimEff2 = copy.deepcopy(dmgUp), copy.deepcopy(healDoneBonus)
stimEff1.stat, stimEff1.power, stimEff2.power = HARMONIE,5,20
stimEff1.turnInit = stimEff2.turnInit = 3
stimulate = skill("Stimulate",getAutoId(curl.id,True),TYPE_BOOST,price=500,area=AREA_SUMMONS,range=AREA_MONO,effects=[stimEff1,stimEff2,galvaniseEff],cooldown=5,description="Augmente les dégâts infligés et les soins réalisés par vos invocations et augmente leur durée de vie",emoji='<:stimulation:1104511237301227681>')
divinVealEff, divinVealEff2 = effect("Voile Divin","divinVeal", stat=ENDURANCE,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,turnInit=3,overhealth=65,emoji='<:voile:1104762361929281547>',stackable=True), copy.deepcopy(absEff)
divinVealEff2.power, divinVealEff2.turnInit = 15, divinVealEff.turnInit
divinVeal = skill("Voile Divin",getAutoId(stimulate.id,True),TYPE_ARMOR,price=500,effects=[divinVealEff],range=AREA_MONO,area=AREA_CIRCLE_2,effectOnSelf=divinVealEff2,cooldown=5,maxHpCost=10,group=SKILL_GROUP_HOLY,emoji='<:voileDivin:1104762549737631824>',description="Octroi une armure à vous et vos alliés proches et augmente les soins que vous recevez")
dvinRegenEff = effect("Régénération Divine","dvinRegen",stat=CHARISMA,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,power=40,turnInit=3,emoji='<:dvinRegen:1104496736845713440>',stackable=True)
dvinRegen = skill("Régénération Divine Etendue",getAutoId(divinVeal.id,True),TYPE_INDIRECT_HEAL,price=500,effects=dvinRegenEff,area=AREA_CIRCLE_2,maxHpCost=15,cooldown=5,group=SKILL_GROUP_HOLY,emoji=dvinRegenEff.emoji[0][0],description="Octroi un effet régénérant aux alliés ciblés")
dvinRegen2 = skill("Régénération Divine Concentrique",getAutoId(dvinRegen.id,True),TYPE_INDIRECT_HEAL,price=500,effects=dvinRegenEff,effPowerPurcent=150,maxHpCost=15,cooldown=5,group=SKILL_GROUP_HOLY,emoji=dvinRegenEff.emoji[0][0],description="Octroi un puissant effet régénérant à l'allié ciblé")
phenixSpiritEff = copy.deepcopy(galvaniseEff)
phenixSpiritEff.power = 3
phenixSpirit = skill("Esprit Phénix",getAutoId(dvinRegen2.id,True),TYPE_BOOST,price=750,emoji='<:phenixSkill1_1:1066006765340196995>',effects=phenixSpiritEff,range=AREA_MONO,area=AREA_SUMMONS,cooldown=7,description="Augmente de 3 tours la durée de vie de vos invocations")

brotherHoodEff = copy.deepcopy(dmgUp)
brotherHoodEff.power, brotherHoodEff.stat, brotherHoodEff.turnInit = 2, STRENGTH, 3
brotherHood = skill("Fraternité",getAutoId(phenixSpirit.id,True),TYPE_BOOST,price=500,range=AREA_MONO,area=AREA_CIRCLE_2,effects=brotherHoodEff,cooldown=7,replay=True,description="Augmente les dégâts infligés par vous et vos alliés proche, vous permet de rejouer votre tour",emoji='<:brotherhood:1115539498969874432>')
chakraJauge = effect("Jauge de Chakras","chakraJauge",turnInit=-1,unclearable=True,emoji='<:chakra:1115539709255487508>',jaugeValue=jaugeValue(
    emoji=[["<:chEmL:1115678424690864179>","<:chEmM:1115678452088061963>","<:chEmR:1115678501824106619>"],["<:chFuL:1115680364338368582>","<:chFulM:1115680406914732152>","<:chFulR:1115680434429382666>"]],
    conds=[
        jaugeConds(INC_START_TURN,5),
        jaugeConds(INC_DEAL_DAMAGE,50/100),
        jaugeConds(INC_USE_SKILL,10,[brotherHood]),
        jaugeConds(INC_ON_SELF_CRIT,5),
        jaugeConds(INC_ON_ALLY_CRIT,2)
    ]
))
brotherHood.description = brotherHood.description + " et augmente de {0} points votre {1} {2}".format(chakraJauge.jaugeValue.conds[2].value,chakraJauge.emoji[0][0],chakraJauge.name)
forbiddenChakra = skill("Chakra Interdit",getAutoId(brotherHood.id,True),TYPE_DAMAGE,cooldown=1,emoji='<:forbidden:1115539403444584549>',power=80,description="Inflige des dégâts à l'ennemi ciblé et vous permeet de rejouer votre tour",replay=True,minJaugeValue=35,maxJaugeValue=35,jaugeEff=chakraJauge,range=AREA_CIRCLE_1)
illumination = skill("Illumination",forbiddenChakra.id,TYPE_DAMAGE,cooldown=forbiddenChakra.cooldown,emoji='<:illumination:1115539439557562429>',power=60,description="Inflige des dégâts aux ennemis et vous permeet de rejouer votre tour",replay=True,minJaugeValue=35,maxJaugeValue=35,jaugeEff=chakraJauge,range=AREA_CIRCLE_1,area=AREA_LINE_2)
meditate = skill("Méditation",forbiddenChakra.id,TYPE_DAMAGE,price=500,become=[forbiddenChakra,illumination],emoji='<:meditate:1115723122897862707>',jaugeEff=chakraJauge,description="Vous octroi {0} {1} et vous permet d'utiliser deux compétences offensives permettant de rejouer votre tour\n\n{2} __{3} :__\n{4}\n\n{5} __{6} :__\n{7}".format(chakraJauge.emoji[0][0],chakraJauge.name,forbiddenChakra.emoji,forbiddenChakra.name,forbiddenChakra.description,illumination.emoji,illumination.name,illumination.description))

solarNadi = effect("Nadi Solaire","solarNadi",turnInit=12,emoji='<:elexirField:1115539540573159454>')
lunarNadi = effect("Nadi Lunaire","lunarNadi",turnInit=12,emoji='<:flammingDebut:1115539563516018768>')
rixeEva = skill("Rixe évanescent",getAutoId(forbiddenChakra.id,True),TYPE_DAMAGE,power=135,area=AREA_CIRCLE_1,range=AREA_CIRCLE_2,emoji='<:rixe:1115539584302989403>',cooldown=3,minJaugeValue=75,maxJaugeValue=100,maxPower=150,percing=35,damageOnArmor=1.2,description="Inflige de gros dégâts aux ennemis ciblés en ignorant une partie de leur résistance et en infligeant des dégâts augmentés aux armures",jaugeEff=chakraJauge,needEffect=[solarNadi,lunarNadi])
elexirChamp = skill("Champ d'élexir",rixeEva.id,TYPE_DAMAGE,power=100,maxPower=135,range=AREA_MONO,area=AREA_CIRCLE_1,cooldown=rixeEva.cooldown,emoji='<:elexirField:1115539540573159454>',minJaugeValue=35,maxJaugeValue=50,jaugeEff=chakraJauge,effectOnSelf=solarNadi,rejectEffect=solarNadi,description="Inflige des dégâts aux ennemis alentours")
flammingDebut = skill("Départ de Flammes",rixeEva.id,TYPE_DAMAGE,power=100,maxPower=135,range=AREA_MONO,area=AREA_CIRCLE_1,cooldown=rixeEva.cooldown,emoji='<:flammingDebut:1115539563516018768>',minJaugeValue=35,maxJaugeValue=50,jaugeEff=chakraJauge,effectOnSelf=lunarNadi,rejectEffect=lunarNadi,description="Inflige des dégâts aux ennemis alentours")
bundleRixeEva = skill("Rixe évanescent",rixeEva.id,TYPE_DAMAGE,price=500,become=[elexirChamp,flammingDebut,rixeEva],jaugeEff=chakraJauge,description="Vous octroi {0} {1} et vous permet d'utiliser plusieurs compétences offensives.\n{2} {3} ne peut être utilisé qu'une fois {4} {5} et {6} {7} utilisés\n\n{4} __{5}__ {6} __{7} :__\n{8}\n\n{2} __{3} :__\n{9}".format(chakraJauge.emoji[0][0],chakraJauge.name,rixeEva.emoji,rixeEva.name,elexirChamp.emoji,elexirChamp.name,flammingDebut.emoji,flammingDebut.name,elexirChamp.description,rixeEva.description),emoji='<:rixe:1115539584302989403>')
higanbanaEff = effect("Higanbana","Higanbana", stat=STRENGTH,power=20,turnInit=7,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,lvl=7,emoji='<:higanbana:1115723081135161424>',stackable=True)
higanbana = skill("Higanbana",getAutoId(bundleRixeEva.id,True),TYPE_DAMAGE,750,power=100,cooldown=7,range=AREA_CIRCLE_1,emoji=higanbanaEff.emoji[0][0],description="Inflige des dégâts ainsi qu'un effet de dégâts périodique durant un long moment à l'ennemi ciblé",effects=higanbanaEff)

snowFall = skill("Avalanche",getAutoId(higanbana.id,True),TYPE_DEPL,500,use=INTELLIGENCE,depl=snowFallGlypheDepl,emoji=snowFallGlypheDepl.icon[0],cooldown=5,condition=[EXCLUSIVE,ASPIRATION,PROTECTEUR],description="Pose un {0} {1} sur la cellule ciblé. Si cette dernière est libre, Saute dessus. Le glyphe inflige des dégâts aux ennemis et augmente la résistance des alliés dans la zone d'effet".format(snowFallGlypheDepl.icon[0],snowFallGlypheDepl.name),range=AREA_CIRCLE_2)
bentoEff = effect("Sharpels","bentoEff", stat=STRENGTH,power=45,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,area=AREA_DONUT_2,emoji='<:bento:1116674708214128640>')
bento = skill("Bento-Torpille",getAutoId(snowFall.id,True),TYPE_DAMAGE,500,80,area=AREA_CIRCLE_1,effects=bentoEff,cooldown=5,description="Inflige des dégâts de zone autour de l'ennemi ciblé ainsi qu'une seconde explosion infligeant des dégâts indirectes de zone supplémentaire",emoji='<:bento:1116674708214128640>')
analysedShot_1 = skill("Tir d'Analyse",getAutoId(bento.id,True),TYPE_DAMAGE,500,130,condition=[EXCLUSIVE,ASPIRATION,OBSERVATEUR],accuracy=250,percing=15,garCrit=True,emoji='<:analysedShot:1116226548081639434>',cooldown=6,description="Augmente les dégâts critiques reçus par l'ennemi ciblé durant le tour de chargement puis inflige une attaque forcément critique avec une grande précision qui ignore une partie de la résistance ennemie")
analyseCritWeak = effect("Faiblesse Critique","critWeakNEss",power=10,turnInit=2,decateEndOfTurn=True,type=TYPE_MALUS,stackable=True,description="Un point faible de l'ennemi augmente les dégâts qu'il reçoit de la part de coups critiques directs",emoji='<:critWeakness:1058021637624188958>')
analysedShot_c = effect("Cast - {replicaName}","analysedShotc",replique=analysedShot_1,turnInit=2,emoji='<:analyse:1116225083904626748>')
analysedShot = copy.deepcopy(analysedShot_1)
analysedShot.power, analysedShot.effects, analysedShot.effectOnSelf = 0, [analyseCritWeak], analysedShot_c
lenaDrone1 = skill("Drone Artilleur",getAutoId(analysedShot_1.id,True),TYPE_SUMMON,500,range=AREA_CIRCLE_2,invocation="Drone Artilleur",cooldown=7,condition=[EXCLUSIVE,ASPIRATION,OBSERVATEUR],emoji='<:lenaDrone1B:1116262917868888185>',description="Permet d'invoquer un drone infligeant des dégâts et augmentant les dégâts critiques subis par les ennemis")
eternalLightEff = effect("Aveuglement éternel","eternalBlind", stat=MAGIE,precision=-5,turnInit=3,type=TYPE_MALUS,emoji="<:MyEyes:784226383018328115>")
eternalLight_1 = skill("Lumière Eternelle",getAutoId(lenaDrone1.id,True),TYPE_DAMAGE,emoji='<:eternalLight:1116761926052089856>',accuracy=250,price=0,power=120,range=AREA_MONO,area=AREA_ALL_ENEMIES,setAoEDamage=True,cooldown=7,ultimate=True,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],description="Après un tour de chargement, inflige des dégâts à tous les ennemis qu'importe leur position et réduit leur précision pendant un petit moment",damageOnArmor=0.8,effectAroundCaster=[TYPE_MALUS,AREA_ALL_ENEMIES,eternalLightEff])
eternalLight_c = effect("Cast - {replicaName}","eternalLightc",turnInit=2,replique=eternalLight_1,silent=True)
eternalLight = copy.deepcopy(eternalLight_1)
eternalLight.power, eternalLight.effectOnSelf, eternalLight.effectAroundCaster = 0, eternalLight_c, None

Hauringusutōmusōdo1_eff1 = effect("Hauringufurarī","Hauringusutōmusōdo1_eff1",stat=AGILITY,power=75,area=AREA_DONUT_2,trigger=TRIGGER_INSTANT,type=TYPE_INDIRECT_DAMAGE,emoji='<:liaSamLB2:1100185041306386439>')
Hauringusutōmusōdo1_eff2 = effect("Uindogādo","Hauringusutōmusōdo1_eff2",dodge=20,block=20,counterOnBlock=20,counterOnDodge=20,emoji='<:liaSki6:1013891089662488596>')
Hauringusutomusodo_1 = skill("Hauringusutōmusōdo",getAutoId(eternalLight.id,True),TYPE_DAMAGE,power=120,cooldown=6,garCrit=True,effects=[Hauringusutōmusōdo1_eff1],effectOnSelf=Hauringusutōmusōdo1_eff2,range=AREA_CIRCLE_3,tpBehind=True,emoji='<:liaCounter:998001563379437568>',url=demolish.url,description="Après un tour de chargement, Saute derrière l'ennemi ciblé, lui inflige une attaque forcément critique ({0}), inflige des dégâts indirects aux ennemis proches ({1}) et augmente vos chances d'esquive, de parade et de contre-attaque durant un brief moment".format(statsEmojis[STRENGTH],statsEmojis[Hauringusutōmusōdo1_eff1.stat]),ultimate=True,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR])
Hauringusutomusodo_c = effect("Cast - {replicaName}","Hauringusutomusodoc",turnInit=2,silent=True,replique=Hauringusutomusodo_1,emoji='<:liaSki1_1:1012761673427333120>')
Hauringusutomusodo = copy.deepcopy(Hauringusutomusodo_1)
Hauringusutomusodo.power, Hauringusutomusodo.effects, Hauringusutomusodo.effectOnSelf, Hauringusutomusodo.tpBehind = 0, [None], Hauringusutomusodo_c, False

kenhiJauge = effect("Jauge de Kenki","kenhiJauge",turnInit=-1,unclearable=True,emoji='<:tenki:1116773121173766164>',jaugeValue=jaugeValue(
    emoji=[["<:juEmL:1115720919676113008>","<:juEmM:1115720946473521192>","<:juEmD:1115720974977994772>"],["<:juFuL:1115721100039565424>","<:juFuM:1115721123154374787>","<:juFuR:1115721152279621663>"]],
    conds=[
        jaugeConds(INC_START_TURN,5),
        jaugeConds(INC_DEAL_DAMAGE,50/100),
        jaugeConds(INC_USE_SKILL,15,[higanbana]),
        jaugeConds(INC_ON_SELF_CRIT,5),
        jaugeConds(INC_ON_ALLY_CRIT,2)
    ]
))
higanbana.description = higanbana.description + " et augmente de {0} points votre {1} {2}".format(kenhiJauge.jaugeValue.conds[2].value,kenhiJauge.emoji[0][0],kenhiJauge.name)
shinten = skill("Hissatsu : Shinten",getAutoId(Hauringusutomusodo.id,True),TYPE_DAMAGE,cooldown=1,emoji='<:shinten:1115723001535680652>',power=85,description="Inflige des dégâts à l'ennemi ciblé et vous permet de rejouer votre tour",replay=True,minJaugeValue=35,maxJaugeValue=50,jaugeEff=kenhiJauge,range=AREA_CIRCLE_1,maxPower=100)
kyten = skill("Hissatsu : Kyten",shinten.id,TYPE_DAMAGE,cooldown=shinten.cooldown,emoji='<:kyten:1115723028760907866>',power=70,description="Inflige des dégâts aux ennemis autours de vous et vous permet de rejouer votre tour",replay=True,minJaugeValue=35,maxJaugeValue=50,jaugeEff=kenhiJauge,range=AREA_MONO,area=AREA_CIRCLE_1,maxPower=85)
hissatsu = skill("Mokusô",shinten.id,TYPE_DAMAGE,price=500,become=[shinten,kyten],emoji='<:mokuso:1116769828745785364>',jaugeEff=kenhiJauge,description="Vous octroi {0} {1} et vous permet d'utiliser deux compétences offensives permettant de rejouer votre tour\n\n{2} __{3} :__\n{4}\n\n{5} __{6} :__\n{7}".format(kenhiJauge.emoji[0][0],kenhiJauge.name,shinten.emoji,shinten.name,shinten.description,kyten.emoji,kyten.name,kyten.description))
senei = skill("Hissatsu : Sen'ei",getAutoId(hissatsu.id,True),TYPE_DAMAGE,cooldown=7,emoji=demolish.emoji,power=120,description="Inflige des dégâts à l'ennemi ciblé",minJaugeValue=50,maxJaugeValue=100,jaugeEff=kenhiJauge,range=AREA_CIRCLE_1,maxPower=160)
guren = skill("Hissatsu : Guren",senei.id,TYPE_DAMAGE,cooldown=senei.cooldown,emoji='<:guren:1115723050952958012>',power=100,description="Inflige des dégâts aux ennemis devant vous",minJaugeValue=50,maxJaugeValue=100,jaugeEff=kenhiJauge,range=AREA_CIRCLE_1,area=AREA_LINE_2,maxPower=140)
ikishoten = skill("Ikishôten",senei.id,TYPE_DAMAGE,price=500,become=[senei,guren],emoji='<:ikishoten:1115723102324805664>',jaugeEff=kenhiJauge,description="Vous octroi {0} {1} et vous permet d'utiliser deux puissantes compétences\n\n{2} __{3} :__\n{4}\n\n{5} __{6} :__\n{7}".format(kenhiJauge.emoji[0][0],kenhiJauge.name,senei.emoji,senei.name,senei.description,guren.emoji,guren.name,guren.description))

bloodButterfly = effect("Papillon Sanguin","bloodbutterfly",type=TYPE_MALUS,power=35,turnInit=3,emoji='<:bloodButterfly:1090171812782034954>',description="Absorbe **{0} %** des soins reçus par la cible. Lorsque l'effet prend fin, restitue les soins absorbés à l'entité à l'origine de l'effet")
bloodButterFlyPassifEff = effect("Volontée gravée dans le sang","bloodbutterflypass",power=25,turnInit=-1,unclearable=True,description="Vous octroi **25%** de chance d'infliger l'effet <:bloodButterfly:1090171812782034954> __Papillon Sanguin__ à la cible principale de vos compétences",emoji='<:clemHeritage:1090171016841547846>',callOnTrigger=bloodButterfly)
inMemoria = skill("In Memoria",getAutoId(ikishoten.id,True),TYPE_RESURECTION,power=200,shareCooldown=True,emoji='<:inMemoria:1119958588362866789>',use=INTELLIGENCE,area=AREA_ALL_ALLIES,range=AREA_MONO,cooldown=7,description="Réanime tous les alliés vaincus. Si un allié ne peut être réanimé, invoque un {0} {1} à la place\n\n{0} __{1}__ :\nReprésente l'esprit d'un défunt. Possède {2}% des statistiques ainsi que les mêmes compétences de l'entité qu'il représente. Translucide, Inciblable et Invulnérable\nLes PNJ du groupe Mort-Vivant ne peuvent pas créer de Memoria\n\nSi {3} Anna est présente dans la même équipe que le lanceur, cette compétence invoque à minima une Memoria".format("<:ghostB:1119951487032901722>","Memoria",50,"<:anna:943444730430246933>"))
komoriHerit = skill("Savoir Vampirique",getAutoId(inMemoria.id,True),TYPE_PASSIVE,effectOnSelf=bloodButterFlyPassifEff,emoji=bloodButterFlyPassifEff.emoji[0][0],description=bloodButterFlyPassifEff.description)

dualCastEff = effect("Double Sort","dualCastEff", stat=MAGIE,power=80,area=AREA_CIRCLE_1,lvl=4,turnInit=4,description="Lors de vos 3 prochains tours, inflige une attaque directe magique en zone autour de l'ennemi ciblé par vos compétences offensives",emoji='<:dualCast:1121436199429623888>')
dualCastEff1 = effect("Bonus de Magie","dualCastEff2", stat=PURCENTAGE,magie=15,turnInit=dualCastEff.turnInit,description="Augmente la magie",emoji=statsEmojis[MAGIE])
dualCast = skill("Double Sort",getAutoId(komoriHerit.id,True),TYPE_BOOST,effects=[dualCastEff,dualCastEff1],emoji=dualCastEff.emoji[0][0],description=dualCastEff.description+", augmente votre magie et vous permet de rejouer votre tour",cooldown=7,range=AREA_MONO)
renforPhysEff = effect("Renforcement Physique","dualCastEff", stat=STRENGTH,power=80,area=AREA_CIRCLE_1,lvl=4,turnInit=4,description="Lors de vos 3 prochains tours, inflige une attaque directe magique en zone autour de l'ennemi ciblé par vos compétences offensives",emoji='<:darkRenf:1120974892188315740>')
renforPhysEff1 = effect("Bonus de Force","dualCastEff2", stat=PURCENTAGE,strength=15,turnInit=dualCastEff.turnInit,description="Augmente la force",emoji=statsEmojis[STRENGTH])
renforPhys = skill("Renforcement Physique",getAutoId(dualCast.id,True),TYPE_BOOST,effects=[renforPhysEff,renforPhysEff1],emoji=renforPhysEff.emoji[0][0],description=renforPhysEff.description+", augmente votre force et vous permet de rejouer votre tour",cooldown=7,range=AREA_MONO)
highVibration = effect("Haute Fréquence Vibratoire","highVibr", stat=INTELLIGENCE,strength=2,magie=2,charisma=2,intelligence=2,turnInit=5,emoji='<:hfv:1124333624930615326>')
harmQuant = copy.deepcopy(absEff)
harmQuant.power, harmQuant.turnInit = 5, highVibration.turnInit
protect5g = effect("Harmonie Quantique Anti-5G","harmQuant", stat=INTELLIGENCE,inkResistance=4,turnInit=highVibration.turnInit)
increaseVibrations = skill("Augmentation des fréquences vibratoires",getAutoId(renforPhys.id,True),TYPE_BOOST,500,effects=[highVibration,harmQuant,protect5g],cooldown=7,range=AREA_MONO,area=AREA_CIRCLE_2,description="Augmente vos fréquences vibratoires et celles de vos alliés proches pendant un moment",emoji=highVibration.emoji[0][0])
lycantStrike_1 = skill("Furie Lycantropique",getAutoId(increaseVibrations.id,True),TYPE_DAMAGE,750,power=225,garCrit=True,ultimate=True,tpCac=True,cooldown=destruction.cooldown,emoji='<:griffe:884889931359596664>',url="https://cdn.discordapp.com/attachments/927195778517184534/932774912391782490/20220118_001411.gif",effectOnSelf=destruction.effectOnSelf,description="Après un tour de chargement, inflige une puissante attaque forcément critique à l'ennemi ciblé et vous empêche d'utiliser une compétence lors de votre prochain tour")
lycantStrike_c = effect("Cast - {replicaName}","lycantStrike_c",turnInit=2,silent=True,replique=lycantStrike_1)
lycantStrike = skill(lycantStrike_1.name,lycantStrike_1.id,lycantStrike_1.type,lycantStrike_1.price,range=lycantStrike_1.range,ultimate=True,cooldown=lycantStrike_1.cooldown,effectOnSelf=lycantStrike_c,emoji=lycantStrike_1.emoji)
skySharter_1 = skill("Triples Carraux Explosifs",getAutoId(lycantStrike.id,True),TYPE_DAMAGE,power=explosion.power*0.35,price=750,repetition=3,area=AREA_CIRCLE_2,effectOnSelf=explosion.effectOnSelf,percing=explosion.percing,damageOnArmor=explosion.onArmor,ultimate=True,cooldown=explosion.cooldown,emoji='<:tripleExploArrows:1135274685358145747>')
skySharter_c = effect("Cast - {replicaName}","skySharter_c",replique=skySharter_1,turnInit=2,silent=True)
skySharter = copy.deepcopy(skySharter_1)
skySharter.power, skySharter.effectOnSelf = 0, skySharter_c
tox2Eff = copy.deepcopy(vulne)
tox2Eff.power, tox2Eff.stat, tox2Eff.turnInit = 2, STRENGTH, lanceToxEff.turnInit
lanceTox2 = skill("Lance-Toxines Modifié",getAutoId(skySharter.id,True),TYPE_INDIRECT_DAMAGE,500,area=lanceTox.area,range=lanceTox.range,effects=[lanceToxEff,tox2Eff],emoji='<:toxines2:1124752297084334181>',cooldown=7,description="Inflige un effet de dégâts périodiques et augmente les dégâts reçus des ennemis ciblés durant un moment")
tox3Eff = copy.deepcopy(dmgDown)
tox3Eff.power, tox3Eff.stat, tox3Eff.turnInit = tox2Eff.power, STRENGTH, lanceToxEff.turnInit
lanceTox3 = skill("Lance-Toxines Griffé",getAutoId(lanceTox2.id,True),TYPE_INDIRECT_DAMAGE,500,area=lanceTox.area,range=lanceTox.range,effects=[lanceToxEff,tox3Eff],emoji='<:toxines3:1124752329707634759>',cooldown=7,description="Inflige un effet de dégâts périodiques et réduit les dégâts infligés des ennemis ciblés durant un moment")
liberationEff = effect("Libération","libEff", stat=MAGIE,power=95,area=AREA_CIRCLE_1,trigger=TRIGGER_INSTANT,type=TYPE_INDIRECT_DAMAGE,emoji='<:liberation:1124759822143860808>',callOnTrigger=estal2)
fairyLiberation = skill("Libération",getAutoId(lanceTox3.id,True),TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_2,cooldown=7,effects=liberationEff,emoji=liberationEff.emoji[0][0],description="Pour chaque ennemi ciblé, inflige des dégâts indirects de zone avec une puissance équivalante à **{0}%** de la puissance totale des effets {1} __{2}__ présent sur la cible. Si la puissance est supérieure à **10**, inflige également {3} __{4}__ aux ennemis autours".format(liberationEff.power,estial.emoji[0][0],estial.name,estal2.emoji[0][0],estal2.name))
exploPetal1 = effect("Explosion Florale I","exploPetal1",stat=CHARISMA,strength=2,magie=2,emoji='<:crois1:903976740869795910>')
exploPetal2 = effect("Explosion Florale I (Effet)","exploPetal2",CHARISMA,strength=1,magie=1,turnInit=2,callOnTrigger=exploPetal1,area=AREA_CIRCLE_2,trigger=TRIGGER_ON_REMOVE,emoji='<:eclosion:1124764616476602538>')
exploPetal3 = effect("Explosion Florale II","exploPetal3",CHARISMA,strength=5,magie=5,emoji='<:crois2:903976762726289520>')
exploPetal4 = effect("Explosion Florale II (Effet)","exploPetal4",CHARISMA,strength=2,magie=2,turnInit=1,callOnTrigger=exploPetal3,area=AREA_CIRCLE_2,trigger=TRIGGER_ON_REMOVE,emoji='<:eclosion:1124764616476602538>')
exploPetal5 = effect("Explosion Florale III","exploPetal5",CHARISMA,strength=10,magie=10,emoji='<:crois3:903976790530326578>')
exploPetal6 = effect("Explosion Florale III (Effet)","exploPetal6",CHARISMA,strength=3,magie=3,callOnTrigger=exploPetal5,area=AREA_CIRCLE_2,trigger=TRIGGER_INSTANT,emoji='<:eclosion:1124764616476602538>')
exploPetal = skill("Explosion Florale",getAutoId(fairyLiberation.id,True),TYPE_BOOST,effects=[exploPetal6,exploPetal4,exploPetal2],cooldown=7,emoji='<:eclosion:1124764616476602538>',description="Augmente les statistiques des alliés ciblés. Un effet moins puissant est octroyé aux alliés autours durant 2 tours")
infuEthereff = effect("Infusion d'Ether","infuEther", stat=PURCENTAGE,strength=25,magie=25,charisma=25,intelligence=25,agility=25,precision=25,endurance=25)
infuEthereff1 = effect("Infusion d'Ether","infuEther2", stat=PURCENTAGE,magie=10,turnInit=3)
infuEther = skill("Infusion d'Ether",getAutoId(exploPetal.id,True),TYPE_BOOST,500,cooldown=5,range=AREA_MONO,emoji='<:infusion:1123148866548662363>',area=AREA_SUMMONS,effects=[infuEthereff,galvaniseEff],effectOnSelf=infuEthereff1,description="Augmente de **{0}%** les statistiques de vos invocations et de **{1}** tour leur durée de vie. Accroie également votre magie de **{2}%** durant un petit moment".format(infuEthereff.strength,galvaniseEff.power,infuEthereff1.magie))
gemmes = skill("Resplandiment des gemmes",getAutoId(infuEther.id,True),TYPE_DAMAGE,500,80,use=MAGIE,cooldown=5,emoji='<:gemmes:1123148907040473159>',description="Inflige une attaque à l'ennemi ciblé. De plus, chaque Carbuncle Allié inflige une attaque supplémentaire, la puissance et la zone d'effet variant suivant le type de Carbuncle")
selfMemoria = skill("Echo de l'Âme",getAutoId(gemmes.id,True),TYPE_SUMMON,cooldown=7,ultimate=True,invocation="Memoria",description="Invoque un Mémoria de vous-même",emoji='<:selfMemoria:1129044261237686483>')
selfMemoria.iaPow = 150
squidRollArmor = effect("Armure","squidRollArmor", stat=PURCENTAGE,overhealth=5,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,lightShield=True,emoji=armor.emoji,silentRemove=True,replace=True)
squidRollEff = effect("Vrille Calamar","squidRoll",power=20,turnInit=-1,unclearable=True,emoji='<:squidRoll:1129785893851508746>',callOnTrigger=squidRollArmor,description="Octroi une amure équivalente à **{0}%** de vos PV Maximum lors d'une esquive (20%), lors d'une téléportation au corps à corps ou saut arrière réussie".format(squidRollArmor.overhealth))
squidRoll = skill("Vrille Calamar",getAutoId(selfMemoria.id,True),TYPE_PASSIVE,use=AGILITY,effectOnSelf=squidRollEff,description=squidRollEff.description,emoji=squidRollEff.emoji[0][0])

etherJauge = effect("Jauge d'Ether","jaugedether",turnInit=-1,unclearable=True,emoji='<:etherJauge:1130206278447272088>',jaugeValue=jaugeValue(
    emoji=[["<:ejEL:1130205658579468449>","<:ejEM:1130205689877373008>","<:ejER:1130205728112660691>"],["<:ejFL:1130205480061509762>","<:ejFM:1130205507601322024>","<:ejFR:1130205545110982749>"]],
    conds=[
        jaugeConds(INC_START_TURN,10),
        jaugeConds(INC_USE_SKILL,10,[infuEther])
    ]
))

energyDrain = skill("Aspiration d'énergie",getAutoId(squidRoll.id,True),TYPE_DAMAGE,power=35,replay=True,use=MAGIE,emoji='<:energyDrain:1130205922929684490>',lifeSteal=100,description="Inflige des dégâts à l'ennemi ciblé en absorbant une partie des dégats infligés, remplie votre {0} {1} de {2} points et vous permet de rejouer votre tour".format(etherJauge.emoji[0][0],etherJauge.name,etherJauge.jaugeValue.conds[1].value),cooldown=3)
energySiphon = skill("Syphon d'énergie",energyDrain.id,TYPE_DAMAGE,power=20,replay=True,area=AREA_CIRCLE_1,use=MAGIE,emoji='<:syphon:1130205955846590505>',lifeSteal=50,description="Inflige des dégâts aux ennemis ciblés en absorbant une partie des dégats infligés, remplie votre {0} {1} de {2} points et vous permet de rejouer votre tour".format(etherJauge.emoji[0][0],etherJauge.name,etherJauge.jaugeValue.conds[1].value),cooldown=3)
dualEnergyDrain = skill("Syphonage d'éther",energyDrain.id,TYPE_DAMAGE,become=[energyDrain,energySiphon],price=500,use=MAGIE,emoji=energyDrain.emoji,description="Vous permet d'utiliser {0} {1} et {2} {3}, deux compétences infligeant des dégâts, vous en soigne d'une partie, augmente de {4} {5} et vous permettent de rejouer votre tour".format(energyDrain.emoji,energyDrain.name,energySiphon.emoji,energySiphon.name,etherJauge.emoji[0][0],etherJauge.name))
etherJauge.jaugeValue.conds[1].add.append(energyDrain)
etherJauge.jaugeValue.conds[1].add.append(energySiphon)

suppuration = skill("Suppuration",getAutoId(dualEnergyDrain.id,True),TYPE_DAMAGE,power=35,maxPower=65,replay=True,use=MAGIE,emoji='<:fester:1130205891086524557>',minJaugeValue=30,maxJaugeValue=50,jaugeEff=etherJauge,description="Inflige des dégâts à l'ennemi ciblé en consommant un peu de votre {0} {1} et vous permet de rejouer votre tour".format(etherJauge.emoji[0][0],etherJauge.name))
magicFlare = skill("Brasier de Peine",suppuration.id,TYPE_DAMAGE,power=35,maxPower=50,area=AREA_CIRCLE_1,replay=True,use=MAGIE,emoji='<:flare:1130205986959917127>',minJaugeValue=30,maxJaugeValue=50,jaugeEff=etherJauge,description="Inflige des dégâts aux ennemis ciblés en consommant un peu de votre {0} {1} et vous permet de rejouer votre tour".format(etherJauge.emoji[0][0],etherJauge.name))
dualSupp = skill("Suppuration éthérique",magicFlare.id,TYPE_DAMAGE,become=[suppuration,magicFlare],use=MAGIE,price=500,emoji=suppuration.emoji,description="Vous permet d'utiliser {0} {1} et {2} {3}, deux compétences infligeant des dégâts en consommant un peu de votre {4} {5} et vous permettent de rejouer votre tour".format(energyDrain.emoji,energyDrain.name,energySiphon.emoji,energySiphon.name,etherJauge.emoji[0][0],etherJauge.name),jaugeEff=etherJauge)

phenixReviveEff = effect("Flamme éternelle","ethernalFlame",turnInit=3,power=80,stat=MAGIE,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji='<:flammeEternelle:1066085228998836246>')
phenixReviveEff2 = copy.deepcopy(raisingPheonixFlightTrigger)
phenixReviveEff2.area = AREA_DONUT_2
phenixRevive = skill("Bénédiction du Phénix",getAutoId(dualSupp.id,True),TYPE_RESURECTION,price=500,power=renisurection.power,cooldown=5,effects=[phenixReviveEff,phenixReviveEff2],emoji='<:phenixRevive:1133392587496116234>',description="Réanime l'allié ciblé, lui octroi un effet régénérant et octroi {0} {1} aux alliés proches de lui".format(phenixReviveEff2.callOnTrigger.emoji[0][0],phenixReviveEff2.callOnTrigger.name),use=MAGIE)
tacticianEff = copy.deepcopy(defenseUp)
tacticianEff.power, tacticianEff.turnInit, tacticianEff.stat = 3, 3, STRENGTH
tactician = skill("Tacticien",getAutoId(phenixRevive.id,True),TYPE_BOOST,price=500,effects=tacticianEff,range=AREA_MONO,area=AREA_CIRCLE_2,emoji='<:tacticien:1135646088553050273>',replay=True,description="Réduit les dégâts subis par les alliés alentours et vous permet de rejouer votre tour",cooldown=7)
magicBarrierEff = copy.deepcopy(tacticianEff)
magicBarrierEff.stat = MAGIE
magicBarrier = skill("Barrière Magique",getAutoId(tactician.id,True),TYPE_BOOST,price=500,range=AREA_MONO,area=AREA_CIRCLE_2,effects=magicBarrierEff,emoji='<:magicbarrier:1135646106160738314>',replay=True,description="Réduit les dégâts subis par les alliés alentours et vous permet de rejouer votre tour",cooldown=7)
holosShield = effect("Holos","holosShield", stat=INTELLIGENCE,turnInit=3,overhealth=30,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji='<:holos:1135646124997349447>')
holosEff = copy.deepcopy(magicBarrierEff)
holosEff.stat = INTELLIGENCE
holos = skill("Holos",getAutoId(magicBarrier.id,True),TYPE_BOOST,price=500,effects=[holosEff,holosShield],range=AREA_MONO,area=AREA_CIRCLE_2,emoji=holosShield.emoji[0][0],replay=True,description="Réduit les dégâts subis par les alliés alentours, leur octroi une armure et vous permet de rejouer votre tour",cooldown=7)
inconsRegen = effect("Inconscient Collectif","incons",CHARISMA,power=20,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji='<:inconscient:1135646145486540883>')
inconsEff = copy.deepcopy(magicBarrierEff)
inconsEff.stat = CHARISMA
inconsCollect = skill("Inconscient Collectif",getAutoId(holos.id,True),TYPE_BOOST,price=500,effects=[inconsEff,inconsRegen],range=AREA_MONO,area=AREA_CIRCLE_2,emoji=inconsRegen.emoji[0][0],replay=True,description="Réduit les dégâts subis par les alliés alentours, leur un effet régénérant et vous permet de rejouer votre tour",cooldown=7)
timeBombEff = effect("Bombe Temporelle","timeBomb", stat=MAGIE,power=120,turnInit=3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_ON_REMOVE,emoji='<:timeBomb:1137298697114353775>',area=AREA_CIRCLE_2)
timeBomb = skill("Bombe Temporelle",getAutoId(inconsCollect.id,True),TYPE_INDIRECT_DAMAGE,price=750,effects=timeBombEff,cooldown=7,emoji=timeBombEff.emoji[0][0],condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],description="Après trois tours ou à la mort de l'ennemi ciblé, inflige de gros dégâts indirects à lui et aux ennemis alentours")
healingTimeBombEff = effect("Temporalité apaisante","healingTimeBomb",CHARISMA,power=85,area=AREA_CIRCLE_2,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_ON_REMOVE,emoji='<:healingHourglass:1137298677543751721>')
healingTimeBombEff2 = effect("Sablier soignant","healingTimeBomb2",CHARISMA,power=35,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_INSTANT,emoji='<:healingHourglass:1137298677543751721>')
healingTimebomb = skill("Sablier Soignant",getAutoId(timeBomb.id,True),TYPE_INDIRECT_HEAL,price=750,effects=[healingTimeBombEff2,healingTimeBombEff],cooldown=7,emoji=healingTimeBombEff2.emoji[0][0],condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],description="Soigne l'allié ciblé puis, dans trois tour ou si celui-ci reçoit des dégâts mortels, le soigne lui et vos alliés proches")
rajeunissementEff = effect("Rajeunissement","rajeunissement1",CHARISMA,power=25,turnInit=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,strength=3,magie=3,agility=3,emoji='<:revive:1137298631142166579>')
rajeunissement = skill("Rajeunissement",getAutoId(healingTimebomb.id,True),TYPE_INDIRECT_HEAL,price=500,range=AREA_MONO,area=AREA_CIRCLE_2,effects=rajeunissementEff,cooldown=5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],emoji=rajeunissementEff.emoji[0][0],description="Octroi un effet régénérant aux alliés proches et augmente leurs Force, Agilité et Magie",useActionStats=ACT_HEAL)
celestialChocEff1 = copy.deepcopy(defenseUp)
celestialChocEff1.power, celestialChocEff1.stat = 4, MAGIE
celestialChocEff2 = copy.deepcopy(celestialChocEff1)
celestialChocEff2.power = 2.5
celestialChoc = skill("Saut Céleste",getAutoId(rajeunissement.id,True),TYPE_DAMAGE,use=MAGIE,useActionStats=ACT_DIRECT,accuracy=150,condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE],price=500,power=120,range=AREA_CIRCLE_4,area=AREA_CIRCLE_2,tpCac=True,areaOnSelf=True,emoji='<:celestialChoc:1137424264929235004>',effectOnSelf=celestialChocEff1,effectAroundCaster=[TYPE_BOOST,AREA_DONUT_2,celestialChocEff2],cooldown=7,description="Saute sur l'ennemi ciblé et inflige des dégâts autour de vous. Réduit également vos dégâts subis ainsi que ceux de vos alliés alentours, dans une moindre mesure")
kliBloodyEff2, kliBloodyEff1, kliBloodyEff3 = effect("Eventration","kliBolldyEff2", stat=PURCENTAGE,resistance=-20,turnInit=3), effect("Explosion","kliBloodyEff1", stat=STRENGTH,power=50,area=AREA_CIRCLE_1,type=TYPE_DAMAGE,trigger=TRIGGER_INSTANT,emoji=exploShotEff.emoji[0][0]), effect("Saignement","kliBloodyEff", stat=STRENGTH,type=TYPE_INDIRECT_DAMAGE,power=35,turnInit=3,trigger=TRIGGER_START_OF_TURN,lifeSteal=250,emoji='<:bleed:1083761078770618460>')
kliBloody = skill("Eventration Explosive",getAutoId(celestialChoc.id,True),TYPE_DAMAGE,cooldown=7,power=60,garCrit=True,percing=50,effects=[kliBloodyEff1, kliBloodyEff2, kliBloodyEff3],description="Inflige une attaque critique à l'ennemi ciblé, puis déclanche une explosion sur sa position, infligeant des dégâts de zone, diminuant sa résistance pendant un petit moment et lui infligeant {0} {1}".format(kliBloodyEff3.emoji[0][0],kliBloodyEff3.name),emoji='<:evExplo:1145770712192266393>',price=750)
healerGlare = skill("Châtoiment de la Practicienne",getAutoId(kliBloody.id,True),TYPE_DAMAGE,use=CHARISMA,useActionStats=ACT_HEAL,power=80,maxPower=180,area=AREA_CIRCLE_1,garCrit=True,percing=35,minJaugeValue=20,maxJaugeValue=100,jaugeEff=uberJauge,emoji='<:pissedOffHelene:1146100088431726765>',url='https://media.discordapp.net/attachments/867393297520263208/1146095661914275860/20230829_165423.gif',group=SKILL_GROUP_HOLY,maxHpCost=20,price=750,cooldown=7,accuracy=150)
timeGrenadeEff = effect("Grenade Temporelle","timeGrenade", stat=STRENGTH,power=40,trigger=TRIGGER_ON_REMOVE,area=AREA_CIRCLE_1,type=TYPE_INDIRECT_DAMAGE,emoji='<:bombeTemporelle:1156598550566797373>')
timeGrenade = skill("Grenade Temporelle",getAutoId(healerGlare.id,True),TYPE_INDIRECT_DAMAGE,effects=timeGrenadeEff,emoji='<:bombeTemporelle:1156598550566797373>',area=AREA_RANDOMENNEMI_5,cooldown=5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],price=500)
fireLameEff2 = effect("Brûlure","afterburn", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=20,emoji=elemEmojis[ELEMENT_FIRE],turnInit=3,stackable=True)
fireLameEff = effect("Détonnation enflammée","firelameeff", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,power=70,area=AREA_CIRCLE_1,emoji='<:firelame2:1156452806652330024>')
fireLame = skill("Lame emflammée",getAutoId(timeGrenade.id,True),TYPE_DAMAGE,500,power=70,area=AREA_ARC_1,effects=[fireLameEff,fireLameEff2],range=AREA_CIRCLE_1,use=MAGIE,emoji='<:fireLame:1156452684803608586>',cooldown=7,condition=[EXCLUSIVE,ELEMENT,ELEMENT_FIRE],description="Inflige des dégâts directs aux ennemis ciblés, ainsi que des dégâts indirects supplémentaire indirects supplémentaire. Inflige également un effet de dégâts sur la durée à la cible principale")
iceLameEff = effect("Détonnation Givrée","cryodetonation", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,power=50,area=AREA_CIRCLE_1,emoji='<:icelame2:1156452836964569148>')
iceLame = skill("Lame Givrée",getAutoId(fireLame.id,True),TYPE_DAMAGE,500,power=85,effects=iceLameEff,area=AREA_LINE_2,garCrit=True,range=AREA_CIRCLE_1,emoji='<:iceLame:1156452720090300486>',cooldown=fireLame.cooldown,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],description="Inflige des dégâts directs aux ennemis ciblés (la cible principale subit forcément un coup critique), ainsi qu'une attaque indirecte supplémentaire centrée sur la cible principale")
aerLameEff2 = effect("Brûlure du Vent","afterburn", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,power=20,emoji=elemEmojis[ELEMENT_AIR],turnInit=3,stackable=True)
aerLameEff = effect("Détonnation venteuse","aerlameeff", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,power=75,area=AREA_CIRCLE_1,emoji='<:aerlame2:1156452871479496784>')
aerLame = skill("Lame de vent",getAutoId(iceLame.id,True),TYPE_DAMAGE,500,power=fireLame.power+10,area=AREA_ARC_1,effects=[aerLameEff,aerLameEff2],cooldown=fireLame.cooldown,emoji='<:aerLame:1156452751669207060>',description=firelame.description,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR])
stoneLameEff = effect("Détonnation Rocheuse","terradetonation", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,power=50,area=AREA_CIRCLE_1,emoji='<:stonelame2:1156452894367825930>')
stoneLame = skill("Lame Terrestre",getAutoId(aerLame.id,True),TYPE_DAMAGE,500,power=85,effects=iceLameEff,area=AREA_LINE_2,damageOnArmor=2,use=MAGIE,range=AREA_CIRCLE_1,emoji='<:stonelame:1156452777158004736>',cooldown=fireLame.cooldown,condition=[EXCLUSIVE,ELEMENT,ELEMENT_EARTH],description="Inflige des dégâts directs aux ennemis ciblés (Dégâts augmentés contre l'armure), ainsi qu'une attaque indirecte supplémentaire centrée sur la cible principale")
krakenChargeEff = effect("Réception Réussie","krakenChargeEff", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,area=AREA_CIRCLE_1,power=20,emoji='<:krakenCharge3:1156228590267019316>')
krakenCharge1 = skill("Charge du Kraken",getAutoId(stoneLame,True),TYPE_DAMAGE,500,affSkillMsg=False,power=100,use=MAGIE,garCrit=True,range=AREA_CIRCLE_1,area=AREA_LINE_3,cooldown=7,effectOnSelf=krakenChargeEff,emoji='<:krakenCharge2:1156228564505595924>',ultimate=True,description="Inflige 5 attaques successives à l'ennemi ciblé puis inflige une seconde attaque plus puissante en ligne droite (la cible initiale subis forcément des dégâts critiques). Inflige de léger dégâts indirects autour de vous à la fin")
krakenCharge_c = effect("Charge du Kraken","krakenChagec",replique=krakenCharge1,silent=True)
krakenCharge = skill("Charge du Kraken",krakenCharge1.id,TYPE_DAMAGE,krakenCharge1.price,power=10,repetition=5,effectOnSelf=krakenCharge_c,replay=True,range=krakenCharge1.range,cooldown=krakenCharge1.cooldown,ultimate=krakenCharge1.ultimate,description=krakenCharge1.description,emoji='<:krakenCharge1:1156228532838604923>',use=MAGIE)
timeManipOff = effect("Manipulation Temporelle (Offensif)","manipTimeOff", stat=MISSING_HP,power=25,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_ON_REMOVE,turnInit=3,emoji='<:manipTempo:1137298579711610971>')
timeManipBen = effect("Manipulation Temporelle (Bénéfique)","manipTimeBen", stat=MISSING_HP,power=25,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_ON_REMOVE,turnInit=3,emoji='<:decalageHoraire:1156598514843910144>')
timeManip = skill("Manipulation Temporelle",getAutoId(krakenCharge.id,True),TYPE_INDIRECT_DAMAGE,500,range=AREA_MONO,area=AREA_CIRCLE_2,effects=timeManipOff,effectAroundCaster=[TYPE_INDIRECT_HEAL,AREA_CIRCLE_2,timeManipBen],emoji=timeManipOff.emoji[0][0],cooldown=7,description="Après trois tours, inflige des dégâts aux ennemis et soigne les alliés qui étaient autour de vous en fonction de leurs pv manquants",condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME])
starDust = skill("Poussière d'étoiles",getAutoId(timeManip.id,True),TYPE_DAMAGE,500,range=AREA_MONO,use=CHARISMA,useActionStats=ACT_BOOST,area=AREA_CIRCLE_2,cooldown=5,power=100,emoji='<:starDust:1157641733161635861>',description="Inflige des dégâts aux ennemis alentours et octroi une carte astrale aux alliés proches",condition=[EXCLUSIVE,ELEMENT,ELEMENT_SPACE])
royalShieldEff = effect("Blason Royal","royalShield", stat=INTELLIGENCE,overhealth=75,emoji='<:royalInsing:1163510202713247904>',type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
royalShield = skill("Blason Royal",getAutoId(starDust.id,True),TYPE_ARMOR,750,ultimate=True,effects=royalShieldEff,cooldown=5,range=AREA_MONO,area=AREA_CIRCLE_3,emoji='<:royaleShield:1163510613255925931>',description="Octroi à vous et vos alliés dans la zone d'effet une puissante armure pendant un tour")

denoumentEff1 = effect("Vulnérabilité Augmentée","traqnardEff",inkResistance=-50,turnInit=1,block=-25,dodge=-20,aggro=50,type=TYPE_MALUS,description="Augmente les dégâts indirects reçus par le porteur",stackable=True)
denoumentEff2 = effect("Dénoument","denoumentEff2",type=TYPE_INDIRECT_DAMAGE,stat=MISSING_HP,power=15,emoji='<:denoument:1163831222087200822>')
denoument = skill("Dénouement",getAutoId(royalShield.id,True),TYPE_MALUS,750,effects=[denoumentEff1,denoumentEff2],replay=True,cooldown=7,range=AREA_CIRCLE_1,emoji=denoumentEff2.emoji[0][0],description="Augmente drastiquement les dégâts indirectes et l'aggression de l'ennemi ciblé tout en réduisant sa probabilité de contrer ou esquiver une attaque durant un tour et vous permet de rejouer votre tour. Au prochain tour, inflige des dégâts à la cible en fonction de ses PVs manquants")
smnSpaceTurets = skill("Tourelles Galactiques",getAutoId(denoument.id,True),TYPE_SUMMON,500,invocation="Tourelle Galactique",nbSummon=2,cooldown=5,emoji='<:autoTourG:1131083241718284358>',range=AREA_CIRCLE_2,description="Invoque deux tourelles infligeants de bon dégâts aux armures avec une bonne précision")

revifEff = effect("Revivification","revifEff", stat=MISSING_HP,power=15,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji='<:revivita:1168240630720381078>')
revif = skill("Revivification",getAutoId(smnSpaceTurets.id,True),TYPE_HEAL,500,cooldown=7,power=70,effects=revifEff,emoji='<:revivita:1168240630720381078>',description="Soigne l'allié ciblé et lui octroi un effet régénérant qui le soigne en fonction de ses PVs manquants en début de tour",condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER])
desyncBenEff = effect("Désyncronisation Bénéfique","desyncBenEff", stat=MISSING_HP,power=35,turnInit=3,emoji='<:desyncBenEff:1168268666282971216>',type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_ON_REMOVE)
desyncBen = skill("Désyncronisation Bénéfique",getAutoId(revif.id,True),TYPE_HEAL,750,cooldown=7,emoji='<:desyncBen:1168268576990449798>',power=50,area=AREA_CIRCLE_2,effects=desyncBenEff,description="Soigne les alliés ciblés. Après trois tours, les soigne une nouvelle fois en fonction de leurs PVs manquants",condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME])
lifeFountainEff = effect("Fontaine Vivifiante","lifeFontEff",CHARISMA,power=30,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,turnInit=3,lvl=3,area=AREA_CIRCLE_1,emoji='<:fontaine:1180550161257214063>')
lifeFountainEff2 = effect("Fontaine Vivifiante","lifeFontEff2",CHARISMA,power=30,trigger=TRIGGER_INSTANT,type=TYPE_INDIRECT_HEAL,area=AREA_CIRCLE_1,emoji='<:fontaine:1180550161257214063>')
lifeFontain = skill("Fontaine Vivifiante",getAutoId(desyncBen.id,True),TYPE_INDIRECT_HEAL,500,effects=[lifeFountainEff2,lifeFountainEff],emoji='<:fontaine:1180550161257214063>',cooldown=7,condition=[EXCLUSIVE,ELEMENT,ELEMENT_WATER],description="Soigne immédiatement l'allié ciblé et ceux alentours, puis réplique la compétence lorsque la cible commence son tour")
radianceEff = effect("Radiance","radience",CHARISMA,power=35,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_END_OF_TURN,emoji='<:radiance:1168240652799184927>',area=AREA_CIRCLE_2,turnInit=-1,unclearable=True,incHealJauge=False)
radiance = skill("Radiance",getAutoId(lifeFontain.id,True),TYPE_PASSIVE,500,effects=radianceEff,emoji='<:radiance:1168240652799184927>',jaugeEff=healerGlare.jaugeEff,description="En fin de tour, si la valeur de votre {0} {1} est supérieure ou égale à **20**, consomme **20** de votre jauge pour effectuer des soins autour de vous".format(healerGlare.jaugeEff.emoji[0][0],healerGlare.jaugeEff.name))
propagEffTrig = effect("Propagateur","propagTrig", stat=HARMONIE,power=50,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,emoji='<:propagMaster:1157361864209088684>',lifeSteal=50)
propagEff = effect("Propagateur","propag",callOnTrigger=propagEffTrig,turnInit=-1,unclearable=True,emoji='<:propagMaster:1157361864209088684>')
propagPas = skill("Propagateur",getAutoId(radiance.id,True),TYPE_PASSIVE,500,effects=propagEff,emoji=propagEff.emoji[0][0],jaugeEff=healerGlare.jaugeEff,description="Lorsque vous utilisez votre arme ou une compétence de dégâts sur un ennemi, si la valeur de votre {0} {1} est supérieure ou égale à **35**, consomme **35** points de votre jauge pour infliger une attaque indirecte supplémentaire sur la cible, avec un taux de vol de vie".format(healerGlare.jaugeEff.emoji[0][0],healerGlare.jaugeEff.name))
shareMarkEff = copy.deepcopy(partage)
shareMarkEff.power, shareMarkEff.turnInit = 35, 3
shareMark = skill("Marque de Partage",getAutoId(propagPas.id,True),TYPE_HEAL,price=500,emoji='<:shareMark:1168270797236871188>',effects=shareMarkEff,effBeforePow=True,cooldown=7,power=65,description="Applique {0} {1} à l'allié ciblé durant un petit moment puis le soigne".format(shareMarkEff.emoji[0][0],shareMarkEff.name))
intenseCureEff = copy.deepcopy(absEff)
intenseCureEff.power = 50
intenseCure = skill("Cure Intensive",getAutoId(shareMark.id,True),TYPE_HEAL,emoji='<:intenseCure:1168244627200028902>',price=750,effects=intenseCureEff,effBeforePow=True,power=65,cooldown=7,description="Augmente de **50%** les soins reçus par l'allié ciblé durant un tour puis le soinge")
gangreneEff = effect("Gangrène","gangEff", stat=MAGIE,type=TYPE_INDIRECT_DAMAGE,power=int(120/3),turnInit=3,trigger=TRIGGER_END_OF_TURN,lifeSteal=50,emoji='<:toxila:1177648787179712562>')
gangreneEff2 = copy.deepcopy(gangreneEff)
gangreneEff2.id, gangreneEff2.turnInit, gangreneEff2.lvl, gangreneEff2.trigger, gangreneEff2.emoji, gangreneEff2.power = gangreneEff2.id+"1", 1, 1, TRIGGER_INSTANT, uniqueEmoji('<:toxicTouch:1177634174350401557>'), 50
gangrene = skill("Gangrène",getAutoId(intenseCure.id,True),TYPE_INDIRECT_DAMAGE,effects=[gangreneEff2,gangreneEff],cooldown=5,lifeSteal=gangreneEff.lifeSteal,emoji='<:toxicTouch:1177634174350401557>',useActionStats=ACT_INDIRECT,use=MAGIE,description="Inflige des dégâts à la cible avec du vol de vie, et inflige un effet de poison reproduisant ces effets durant un petit moment",price=500)
dechargeGausseSolo = skill("Décharge de Gausse",getAutoId(gangrene.id,True),TYPE_DAMAGE,price=500,power=50,use=PRECISION,emoji="<:gausse:1003645652313575516>",replay=True,cooldown=3,description="Inflige des dégâts *Précision* à l'ennemi ciblé et vous permet de rejouer votre tour")
ricochetAoeEff = effect("Ricochet","ricAoe", stat=PRECISION,type=TYPE_DAMAGE,trigger=TRIGGER_INSTANT,power=35,area=AREA_DONUT_1,emoji='<:ricochet:1003645701839933520>')
ricochetSolo = skill("Ricochet",getAutoId(dechargeGausseSolo.id,True),TYPE_DAMAGE,price=500,power=dechargeGausseSolo.power,area=AREA_CIRCLE_1,use=PRECISION,emoji="<:ricochet:1003645701839933520>",effects=ricochetAoeEff,replay=True,cooldown=5,description="Inflige des dégâts *Précision* à l'ennemi ciblé et vous permet de rejouer votre tour. Les ennemis proches de la ciblesubissent aussi des dégâtd")
rapidFire = skill("Salve Rapide",getAutoId(ricochetSolo.id,True),TYPE_DAMAGE,emoji='<:barrage:1180550222435324055>',price=500,power=20,repetition=3,replay=True,condition=[EXCLUSIVE,ASPIRATION,OBSERVATEUR],cooldown=3,description="Inflige des dégâts à trois reprises à l'ennemi ciblé et vous permet de rejouer votre tour",quickDesc="Une salve de trois flèches tirées en successions rapides")
fanAscendEff = effect("Poussé Ascendante","fanRevolEff2",CHARISMA,strength=5,agility=3,magie=3,turnInit=3)
fanAscendReady = effect("Eventails Ascendants","fanAscendReady",silent=True,turnInit=5,emoji='<:ascFan:1003308417034768444>')
fanAscend = skill("Eventails Ascendants",getAutoId(rapidFire.id,True),TYPE_DAMAGE,power=70,area=AREA_LINE_2,replay=True,cooldown=3,emoji='<:ascFan:1003308417034768444>',needEffect=[fanAscendReady],effectAroundCaster=[TYPE_BOOST,AREA_DONUT_2,fanAscendEff])
fanReverseReady = effect("Eventail Virvoltant Inversé Préparé","fanReverseReady",silent=True,turnInit=5,emoji='<:revFlyingFan:1003309639280111647>')
fanReverse = skill("Eventail Virvoltant Inversé",fanAscend.id,TYPE_DAMAGE,power=60,replay=True,cooldown=1,area=AREA_ARC_3,emoji='<:revFlyingFan:1003309639280111647>',needEffect=[fanReverseReady],effectOnSelf=fanAscendReady)
fanVir = skill("Eventail Virvoltant",fanAscend.id,TYPE_DAMAGE,power=50,replay=True,cooldown=1,area=AREA_ARC_2,emoji='<:flyingFan:1003309655444963408>',effectOnSelf=fanReverseReady,rejectEffect=[fanAscendReady,fanReverseReady])
fanVirBundle = skill("Combo - Eventails Virvolants",fanAscend.id,TYPE_DAMAGE,500,become=[fanVir,fanReverse,fanAscend],emoji=fanVir.emoji,description="Vous permet d'utiliser le combo rapide {0} {1}, {2} {3} puis {4} {5}".format(fanVir.emoji,fanVir.name,fanReverse.emoji,fanReverse.name,fanAscend.emoji,fanAscend.name),quickDesc="Des lancés d'éventails rapides et successifs pour un maximum de dégâts !",replay=True)
bloodMissilesEff = effect("Explosion Sanguine","bloodMissEFF", stat=MAGIE,type=TYPE_DAMAGE,area=AREA_DONUT_1,power=35/4,emoji='<:clemExSkill:1015209760062189628>',trigger=TRIGGER_INSTANT)
bloodmissiles = skill("Missiles Sanguins",getAutoId(fanAscend.id,True),TYPE_DAMAGE,500,power=50/4,maxPower=75/4,repetition=4,replay=True,effects=[bloodMissilesEff],cooldown=3,emoji='<:bloodMissiles:1180969333929820180>',use=MAGIE,minJaugeValue=15,maxJaugeValue=25,jaugeEff=bloodJauge,description='Inflige des dégâts à plusieurs reprises à la cible et aux ennemis proches, dans une moindre mesure, puis rejoue votre tour',quickDesc="Plusieurs projectiles magiques explosifs")
quickShot = skill("Tir Rapide",getAutoId(bloodmissiles.id,True),TYPE_DAMAGE,500,power=50,cooldown=5,replay=True,emoji='<:directArrow:1180550393663590481>',description="Inflige des dégâts à l'ennemi ciblé et vous permet de rejouer votre tour",)
gwenyQCombo3_r = effect("Perforation Préparée","perfoRefReady",turnInit=3,silent=True,emoji='<:gwSecCb3:1080152231153778699>')
gwenyQCombo3 = skill("Perforation Renforcée",getAutoId(quickShot.id,True),TYPE_DAMAGE,range=AREA_CIRCLE_1,power=50,armorSteal=50,armorConvert=50,aoeArmorConvert=35,replay=True,use=INTELLIGENCE,emoji=gwenyQCombo3_r.emoji[0][0],cooldown=3,description="Inflige des dégâts à l'ennemi ciblé en vous octroyant de l'armure en fonction des dégâts infligés et vous permet de rejouer votre tour",needEffect=gwenyQCombo3_r)
gwenyQCombo2_r = effect("Lacération Préparée","LacerRefReady",turnInit=3,silent=True,emoji='<:gwSecCb2:1080152032813535353>')
gwenyQCombo2 = skill("Lacération Renforcée",gwenyQCombo3.id,TYPE_DAMAGE,power=40,range=AREA_CIRCLE_1,armorConvert=50,armorSteal=50,aoeArmorConvert=35,replay=True,use=INTELLIGENCE,emoji=gwenyQCombo2_r.emoji[0][0],cooldown=1,description="Inflige des dégâts à l'ennemi ciblé en vous octroyant de l'armure en fonction des dégâts infligés et vous permet de rejouer votre tour",needEffect=gwenyQCombo2_r,effectOnSelf=gwenyQCombo3_r)
gwenyQCombo1_r = effect("Arrachage Préparée","ArrachRefReady",turnInit=3,silent=True,emoji='<:gwSecCb1:1080152129613869078>')
gwenyQCombo1 = skill("Arrachage Renforcée",gwenyQCombo3.id,TYPE_DAMAGE,power=30,armorConvert=50,range=AREA_CIRCLE_1,armorSteal=50,aoeArmorConvert=35,replay=True,use=INTELLIGENCE,emoji=gwenyQCombo1_r.emoji[0][0],cooldown=1,description="Inflige des dégâts à l'ennemi ciblé en vous octroyant de l'armure en fonction des dégâts infligés et vous permet de rejouer votre tour",effectOnSelf=gwenyQCombo2_r,rejectEffect=[gwenyQCombo2_r,gwenyQCombo3_r])
gwenyQCombo = skill("Combo - Perforation Renforcée",gwenyQCombo3.id,TYPE_DAMAGE,price=500,become=[gwenyQCombo1,gwenyQCombo2,gwenyQCombo3],condition=[EXCLUSIVE,ASPIRATION,PROTECTEUR],emoji=gwenyQCombo3.emoji,description="Permet d'utiliser le combo {0} {1}, {2} {3} et {4} {5}, trois compétences rapides ayant un taux de convertion des dégâts en armure".format(gwenyQCombo1.emoji,gwenyQCombo1.name,gwenyQCombo2.emoji,gwenyQCombo2.name,gwenyQCombo3.emoji,gwenyQCombo3.name),replay=True,use=INTELLIGENCE)
altyQCombo3_r = effect("Perforation Préparée","perfoRefReady",turnInit=3,silent=True,emoji='<:alSecCb3:1080152283670650931>')
altyQCombo3 = skill("Perforation Revifiante",getAutoId(gwenyQCombo.id,True),TYPE_DAMAGE,range=AREA_CIRCLE_1,power=50,damageOnArmor=1.2,lifeSteal=50,aoeLifeSteal=35,replay=True,use=CHARISMA,emoji=altyQCombo3_r.emoji[0][0],cooldown=3,description="Inflige des dégâts à l'ennemi ciblé avec du vol de vie pour vous et vos alliés proche et vous permet de rejouer votre tour",needEffect=altyQCombo3_r)
altyQCombo2_r = effect("Lacération Préparée","LacerRefReady",turnInit=3,silent=True,emoji='<:alSecCb2:1080152099549098016>')
altyQCombo2 = skill("Lacération Revifiante",altyQCombo3.id,TYPE_DAMAGE,power=40,range=AREA_CIRCLE_1,lifeSteal=50,aoeLifeSteal=35,damageOnArmor=1.2,replay=True,use=CHARISMA,emoji=altyQCombo2_r.emoji[0][0],cooldown=1,description=altyQCombo3.description,needEffect=altyQCombo2_r,effectOnSelf=altyQCombo3_r)
altyQCombo1_r = effect("Arrachage Préparée","ArrachRefReady",turnInit=3,silent=True,emoji='<:alSecCb1:1080152189806325822>')
altyQCombo1 = skill("Arrachage Revifiante",altyQCombo3.id,TYPE_DAMAGE,power=30,lifeSteal=50,range=AREA_CIRCLE_1,aoeLifeSteal=35,damageOnArmor=1.2,replay=True,use=CHARISMA,emoji=altyQCombo1_r.emoji[0][0],cooldown=1,description=altyQCombo3.description,effectOnSelf=altyQCombo2_r,rejectEffect=[altyQCombo2_r,altyQCombo3_r])
altyQCombo = skill("Combo - Perforation Revifiante",altyQCombo3.id,TYPE_DAMAGE,price=500,become=[altyQCombo1,altyQCombo2,altyQCombo3],condition=[EXCLUSIVE,ASPIRATION,VIGILANT],emoji=altyQCombo3.emoji,description="Permet d'utiliser le combo {0} {1}, {2} {3} et {4} {5}, trois compétences rapides avec du vol de vie pour vous et vos alliés proches".format(altyQCombo1.emoji,altyQCombo1.name,altyQCombo2.emoji,altyQCombo2.name,altyQCombo3.emoji,altyQCombo3.name),replay=True,use=CHARISMA)
klikliQCombo3_r = effect("Perforation Préparée","perfoRefReady",turnInit=3,silent=True,emoji='<:klSecCb3:1080152258177662976>')
klikliQCombo3 = skill("Perforation Saignante",getAutoId(altyQCombo.id,True),TYPE_DAMAGE,range=AREA_CIRCLE_1,power=50,lifeSteal=35,effects=kStrikeEff,replay=True,use=STRENGTH,emoji=klikliQCombo3_r.emoji[0][0],cooldown=3,description="Inflige des dégâts à l'ennemi ciblé en vous avec du vol de vie et infligeant un effet de saignement à l'ennemi et vous permet de rejouer votre tour",needEffect=klikliQCombo3_r)
klikliQCombo2_r = effect("Lacération Préparée","LacerRefReady",turnInit=3,silent=True,emoji='<:klSecCb2:1080152065625571388>')
klikliQCombo2 = skill("Lacération Saignante",klikliQCombo3.id,TYPE_DAMAGE,power=40,range=AREA_CIRCLE_1,lifeSteal=35,replay=True,effects=kStrikeEff,use=STRENGTH,emoji=klikliQCombo2_r.emoji[0][0],cooldown=1,description=klikliQCombo3.description,needEffect=klikliQCombo2_r,effectOnSelf=klikliQCombo3_r)
klikliQCombo1_r = effect("Arrachage Préparée","ArrachRefReady",turnInit=3,silent=True,emoji='<:klSecCb1:1080152158479061093>')
klikliQCombo1 = skill("Arrachage Saignante",klikliQCombo3.id,TYPE_DAMAGE,power=30,lifeSteal=35,range=AREA_CIRCLE_1,replay=True,effects=kStrikeEff,use=STRENGTH,emoji=klikliQCombo1_r.emoji[0][0],cooldown=1,description=klikliQCombo3.description,needEffect=klikliQCombo1_r,effectOnSelf=klikliQCombo2_r,rejectEffect=[klikliQCombo2_r,klikliQCombo3_r])
klikliQCombo = skill("Combo - Perforation Saignante",klikliQCombo3.id,TYPE_DAMAGE,price=500,become=[klikliQCombo1,klikliQCombo2,klikliQCombo3],condition=[EXCLUSIVE,ASPIRATION,BERSERK],emoji=klikliQCombo3.emoji,description="Permet d'utiliser le combo {0} {1}, {2} {3} et {4} {5}, trois compétences rapides ayant un peu de vol de vie et infligeant des effets de saignements à l'ennemi".format(klikliQCombo1.emoji,klikliQCombo1.name,klikliQCombo2.emoji,klikliQCombo2.name,klikliQCombo3.emoji,klikliQCombo3.name),replay=True,use=STRENGTH)
inspirationEff1 = effect("Inspiration","inspiEff1",CHARISMA,type=TYPE_INDIRECT_HEAL,power=20,turnInit=5,trigger=TRIGGER_END_OF_TURN,emoji='<:inspirationEff:1183835012466999386>')
inspirationEff2 = copy.deepcopy(defenseUp)
inspirationEff2.power, inspirationEff2.turnInit, inspirationEff2.stat = 2.5, 3, CHARISMA
inspiration = skill("Inspiration",getAutoId(klikliQCombo.id,True),TYPE_HEAL,ultimate=True,cooldown=7,emoji='<:inspiration:1183835135200743506>',price=500,power=50,range=AREA_MONO,area=AREA_DONUT_2,effects=[inspirationEff1,inspirationEff2],effectOnSelf=inspirationEff1,condition=[EXCLUSIVE,ASPIRATION,VIGILANT],description="Soigne les alliés alentours et réduit leurs dégâts subis tout leur octroyant un effet régénérant en fonction de leurs PV maximums. Vous octroi également un effet régénérant similaire")
propagDelEffTrig = effect("Propagateur Délayé","propagTrig", stat=HARMONIE,power=int(propagEffTrig.power*0.55),type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,emoji='<:toxiStroke:1177648842393530398>',lifeSteal=50,turnInit=3,stackable=True)
propagDelEff = effect("Propagateur Délayé","propag",callOnTrigger=propagDelEffTrig,turnInit=-1,unclearable=True,emoji='<:toxicHearth:1177634139516706919>')
propagDelPas = skill("Propagateur Délayé",getAutoId(inspiration.id,True),TYPE_PASSIVE,500,effects=propagDelEff,emoji=propagDelEff.emoji[0][0],jaugeEff=healerGlare.jaugeEff,description="Lorsque vous utilisez votre arme ou une compétence de dégâts sur un ennemi, si la valeur de votre {0} {1} est supérieure ou égale à **35**, consomme **35** points de votre jauge pour infliger un effet de dégâts indirect supplémentaire, avec un taux de vol de vie".format(healerGlare.jaugeEff.emoji[0][0],healerGlare.jaugeEff.name))

smnMyrlope = skill("Invocation - Myrlopé",getAutoId(propagDelPas.id,True),TYPE_SUMMON,500,invocation="Myrlopé",replay=True,cooldown=5,emoji='<:myrideB:1186673309656559677>',range=AREA_DONUT_2,description="Invoque __Myrlopé__, une invocation infligeant de petits dégâts et entravant les ennemis, et vous permet de rejouer votre tour",quickDesc="Cette araignée est l'animale de compagnie de Shehisa, qui l'emmène un peu partout. Elle a une petite tendance à se mettre au chaud sous ses vêtements si elle a trop froid")
trainePlumeEff = copy.deepcopy(deepWound)
trainePlumeEff.power, trainePlumeEff.stat = 20, STRENGTH
trainePlume = skill("Trainée de Plumes",getAutoId(smnMyrlope.id,True),TYPE_DAMAGE,500,power=40,repetition=3,emoji='<:trainePlume:1188527300728344608>',range=AREA_DIST_3,area=AREA_LINE_3,effects=trainePlumeEff,setAoEDamage=True,cooldown=7)
magicMissile = skill("Missile Magique",getAutoId(trainePlume.id,True),TYPE_DAMAGE,500,power=40,repetition=2,cooldown=7,replay=True,use=MAGIE,description="Inflige des dégâts à deux reprises et vous permet de rejouer votre tour",emoji='<:energyWeap:1164909709950730270>')
sectumsempraEff = copy.deepcopy(deepWound)
sectumsempraEff.power, sectumsempraEff.stat = 80, MAGIE
sectumsempra = skill("Sectumsempra",getAutoId(magicMissile.id,True),TYPE_DAMAGE,500,power=80,effBeforePow=True,effects=sectumsempraEff,use=MAGIE,cooldown=7,description="Inflige des dégâts à l'ennemi ciblé ainsi qu'une forte valeur de {0} {1}".format(deepWound.emoji[0][0],sectumsempraEff.name),quickDesc="Pour les ennemis...",emoji='<:darkThunder:912414778356564019>')
featherCrossEff = copy.deepcopy(deepWound)
featherCrossEff.stat, featherCrossEff.power = STRENGTH, 50
featherCross = skill("Croix de Plumes",getAutoId(sectumsempra.id,True),TYPE_DAMAGE,500,power=100,area=AREA_INLINE_2,cooldown=7,effects=featherCrossEff,emoji='<:plumeCross:1188868838964600892>')

triSlashdown = skill("Triple Choc Chromatique",getAutoId(featherCross.id,True),TYPE_DAMAGE,750,power=80,ultimate=True,damageOnArmor=2,cooldown=7,area=AREA_CIRCLE_2,url='https://i.ibb.co/Gpxwc5y/tri-Splashdown.gif',range=AREA_MONO,repetition=3,description="Inflige des dégâts autour de vous, puis replique la compétence deux fois sur des cases devant vous",emoji='<:triSlashDown:1193165562038198292>')
drkCombo3NeedEff = effect("Dévoreur d'Âme préparé","souleaterReady",emoji='<:lsCombo3:1131081663460413491>',turnInit=5,silent=True)
drkCombo3 = skill("Dévoreur d'Âme",getAutoId(triSlashdown.id,True),TYPE_DAMAGE,500,power=110,lifeSteal=100,range=AREA_CIRCLE_1,cooldown=5,needEffect=drkCombo3NeedEff,emoji=drkCombo3NeedEff.emoji[0][0],description="Inflige des dégâs à l'ennemi ciblé avec un fort taux de vol de vie")
drkCombo2NeedEff = effect("Frappe Syphon préparé","drkCOmbo2Need",emoji='<:lsCombo2:1131081625220943963>',turnInit=5,silent=True)
drkCombo2 = skill("Frappe Syphon",drkCombo3.id,TYPE_DAMAGE,drkCombo3.price,power=100,range=AREA_CIRCLE_1,cooldown=1,needEffect=drkCombo2NeedEff,emoji=drkCombo2NeedEff.emoji[0][0],effectOnSelf=drkCombo3NeedEff)
drkCombo1 = skill("Taillade Violente",drkCombo3.id,TYPE_DAMAGE,drkCombo3.price,power=80,range=AREA_CIRCLE_1,cooldown=1,emoji="<:lsCombo1:1131081594417991700>",effectOnSelf=drkCombo2NeedEff,rejectEffect=[drkCombo2NeedEff,drkCombo3NeedEff])
drkCombo = skill("Combo - Dévoreur d'Âme",drkCombo3.id,TYPE_DAMAGE,drkCombo3.price,become=[drkCombo1,drkCombo2,drkCombo3],emoji=drkCombo3.emoji)

markInfexEff = effect("Marque d'Infection","markInfect",type=TYPE_MALUS,trigger=TRIGGER_INSTANT,emoji='<:markInfex:1212102833059663953>',area=AREA_CIRCLE_2,power=50)
markInfex = skill("Marque d'Infection",getAutoId(drkCombo.id,True),TYPE_INDIRECT_DAMAGE,price=500,effects=[markInfexEff,infection,epidemicEff,intoxEff],cooldown=7,effPowerPurcent=50,emoji=markInfexEff.emoji[0][0],description="Inflige à la cible et aux ennemis alentours un effet de dégâts indirects avec une puissance équivalente à **{0}%** de la puissance cumulée des effets {1}, {2} et {3} sur la cible. Octroi également les dits effets. Si ils étaient déjà présent, rénitialise leur durée et augmente leur puissance, si celle-ci était plus basse".format(markInfexEff.power,infection,epidemicEff,intoxEff))

lavenderShield = effect("Armure Lavandula","laverderShield",INTELLIGENCE,turnInit=3,overhealth=65,emoji='<:lavenderShield:1213202793758986382>',trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,description="Protège d'un certain nombre de dégâts\n\nSi un autre effet <:ls:1213202793758986382> __Armure Lavandula__ est octroyé au porteur, l'armure la plus faible est convertie en soins",replace=True)
lavenderHeal = effect("Soins Angustifolia","lavenderHeal",INTELLIGENCE,power=lavenderShield.overhealth,trigger=TRIGGER_HP_UNDER_50,type=TYPE_INDIRECT_HEAL,emoji='<:lavenderHeal:1213202818845122560>',turnInit=3)
lavenderVielEff = effect("Voile Lavande",defenseUp.id,INTELLIGENCE,power=5,inkResistance=10,emoji='<:lavenderVeil:1213202549604221028>',turnInit=3,description="Réduit de {0}% les dégâts subis par le porteur et réduit également les dégâts indirects subis")
lavenderSmallProtectEff = copy.deepcopy(lavenderShield)
lavenderSmallProtectEff.power = 20
lavenderViel = skill("Voile Lavande",getAutoId(markInfex.id,True),TYPE_ARMOR,price=750,cooldown=7,ultimate=True,effects=[lavenderShield,lavenderVielEff,lavenderHeal],range=AREA_CIRCLE_4,area=AREA_CIRCLE_2,emoji=lavenderVielEff.emoji[0][0],description="Octroi aux alliés ciblés {0} ainsi qu'un effet de soins se déclanchant quand leurs PV tombent en dessous de 50%, réduit les dégâts qu'ils subissent et une réduction supplémentaire des dégâts indirects reçu".format(lavenderShield),effectAroundCaster=[TYPE_ARMOR,AREA_SUMMONER,lavenderSmallProtectEff])

smnAnaisEff = effect("Invocation - Anaïs","smnAnais",type=TYPE_SUMMON,callOnTrigger="Anaïs",trigger=TRIGGER_INSTANT,area=AREA_CIRCLE_2,emoji='<:anais:1166806279042375780>')
smnAnais = skill("Invocation - Anaïs",getAutoId(lavenderViel.id,True),TYPE_PASSIVE,effects=[smnAnaisEff],description="Invoque Anaïs à vos côtés, une pixie spécialisée dans la protection de son invocateur et ses alliés",ultimate=True,price=700)
toxiOverchargeEff1 = effect("Toxines Overdose","toxiOverchargeEff1",MAGIE,power=40,turnInit=3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,lifeSteal=50,emoji='<:zenecaUlt1:1214961183673684018>')
toxiOverchargeEff2 = effect("Toxines Overcharge","toxiOverchargeEff2",MAGIE,power=toxiOverchargeEff1.power//2,turnInit=3,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,lifeSteal=50,emoji='<:zenecaUlt2:1214960718126784522>')
toxiOverchargeEff3 = effect("Toxines Overcharge","toxiOverchargeEff3",callOnTrigger=toxiOverchargeEff2,area=AREA_DONUT_2,emoji=toxiOverchargeEff2.emoji,trigger=TRIGGER_INSTANT)
toxiOvercharge = skill("Toxines Overdose",getAutoId(smnAnais.id,True),TYPE_INDIRECT_DAMAGE,price=750,ultimate=True,effects=[toxiOverchargeEff1, traqnardEff,toxiOverchargeEff3],cooldown=7,emoji=toxiOverchargeEff1.emoji[0][0],description="Inflige {0} à la cible et {1} aux ennemis proches, des effets de dégâts périodiques avec un taux de vol de vie, durant un petit moment. Accroi également les dégâts indirects reçus par la cible durant cette période".format(toxiOverchargeEff1,toxiOverchargeEff2))

tmpChip = getChip("Appel de la Lumière")
lightCalEff = effect(tmpChip.name, tmpChip.name+str(tmpChip.id), turnInit=3, emoji=tmpChip.emoji)
lightCallSkill = skill(tmpChip.name, tmpChip.name+str(tmpChip.id), TYPE_BOOST, range=AREA_MONO, area=AREA_CIRCLE_2, cooldown=7, effects=[lightCalEff], emoji=tmpChip.emoji, description="Augmente la puissance des compétences divines des alliés proches et vous-même de **%power%** durant un petit moment")

tmpChip = getChip("Appel de la Nuit")
nightCalEff = effect(tmpChip.name, tmpChip.name+str(tmpChip.id), turnInit=3, emoji=tmpChip.emoji)
nightCallSkill = skill(tmpChip.name, tmpChip.name+str(tmpChip.id), TYPE_BOOST, range=AREA_MONO, area=AREA_CIRCLE_2, cooldown=7, effects=[nightCalEff], emoji=tmpChip.emoji, description="Augmente la puissance des compétences démoniaques des alliés proches et vous-même de **%power%** durant un petit moment")

tmpChip = getChip("Retour de Bâton")
ilianaBonk = skill(tmpChip.name,tmpChip.name+str(tmpChip.id), TYPE_DAMAGE, range=AREA_CIRCLE_1, cooldown=5, emoji=tmpChip.emoji, use=FIXE, accuracy=500)

lenaInkStrike_2 = skill("Frappe Aérienne",getAutoId(toxiOvercharge,True)+"1",TYPE_DAMAGE,power=125,repetition=4,area=AREA_CIRCLE_1,damageOnArmor=1.5,ultimate=True)
lenaInkStrike_depl1 = depl("Missile Tornade",lenaInkStrike_2,["<:lenaInkStrikeB:1226234953235435662>","<:lenaInkStrikeR:1226234929747202188>"],["<:lenaInkStrikeAreaB:1226234884683726979>","<:lenaInkStrikeAreaR:1226234907450413076>"],lifeTime=0)
lenaInkStrike_depl = depl("lenaInkStrike",lenaInkStrike_2,["<:lenaInkStrikeB:1226234953235435662>","<:lenaInkStrikeR:1226234929747202188>"],["<:lenaInkStrikeAreaB:1226234884683726979>","<:lenaInkStrikeAreaR:1226234907450413076>"],lifeTime=0)
lenaInkStrike_depl.skills = copy.deepcopy(lenaInkStrike_depl.skills)
lenaInkStrike_depl.skills.area = AREA_CIRCLE_2
lenaInkStrike_c = effect("Cast - {replicaName}","lenaInkStrike_c",emoji="<:lenaInkStrike:1226224552162496563>",replique=lenaInkStrike_2,turnInit=2,silent=True)
lenaInkStrike_1 = skill("Frappe Aérienne",lenaInkStrike_2.id.replace("1",""),TYPE_DEPL,depl=lenaInkStrike_depl,cooldown=7,ultimate=True,effectOnSelf=lenaInkStrike_c,emoji="<:lenaInkStrike:1226224552162496563>",description="Cette compétence s'utilise comme un déployable. Au premier tour, marque une zone et pose un nombre variable de déployables en fonction du nombre d'ennemi à l'intérieur. Au prochain tour, inflige des dégâts de zone sur les déployables")
lenaInkStrike = skill("Frappe Aérienne",lenaInkStrike_1.id,TYPE_DAMAGE,price=750,cooldown=lenaInkStrike_1.cooldown,damageOnArmor=lenaInkStrike_2.onArmor,ultimate=lenaInkStrike_1.ultimate,emoji=lenaInkStrike_1.emoji,power=lenaInkStrike_2.power, repetition=lenaInkStrike_2.repetition, description=lenaInkStrike_1.description)

counterTimeEff1 = effect("Contre-Temps","counterTimeEff1",MAGIE,power=COUNTERPOWER,decateOnTurn=True,trigger=TRIGGER_ON_REMOVE,type=TYPE_INDIRECT_DAMAGE,emoji='<:desyncNegEff:1168268631516393503>',dodge=-35)
counterTimeEff = effect("Contre-Temps","counterTimeEff",turnInit=-1,unclearable=True,callOnTrigger=counterTimeEff1,emoji='<:desyncBenEff:1168268666282971216>',counterOnDodge=10)
counterTime = skill("Contre-Temps",getAutoId(lenaInkStrike_1.id,True),TYPE_PASSIVE,price=500,effects=counterTimeEff,condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],description="Lors de vos contre-attaques, inflige également {0} à l'adversaire, réduisant ses chances d'esquive et infligeant des dégâts indirects lors de son prochain tour".format(counterTimeEff1))

timeRipEff = effect("Déchirure Temporelle","timeRipEff",power=50,trigger=TRIGGER_ON_REMOVE,type=TYPE_DAMAGE,stat=MAGIE,dodge=-35,emoji='<:timeRipEff:1226439137788432466>')
timeRip = skill("Déchirure Temporelle",getAutoId(counterTime.id,True),TYPE_DAMAGE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_TIME],emoji='<:timeRip:1226438876823027782>',range=AREA_MONO,power=75,area=AREA_CIRCLE_2,setAoEDamage=True,use=MAGIE,description="Inflige des dégâts autour de vous en ignorant la réduction de dégâts de zone ainsi que {0}, un effet réduisant l'esquive de vos adversaires et infligeant des dégâts directs lors votre prochain tour".format(timeRipEff),effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_DONUT_2,timeRipEff],price=500,cooldown=5)

demonSpell1Eff = copy.deepcopy(vulne)
demonSpell1Eff.power = 25
demonSpell1 = skill("Infernatum",getAutoId(timeRip.id,True),TYPE_DAMAGE,price=500,effBeforePow=True,emoji='<:demonSkill1:1226597142089568406>',effects=demonSpell1Eff,area=AREA_CIRCLE_1,power=120,hpCost=10,group=SKILL_GROUP_DEMON,use=MAGIE,cooldown=7,description="Augmente les dégâts subis par la cible principal et lui inflige des dégâts de zone. Dégâts accrus contre l'armure",damageOnArmor=1.35)
demonMissileEff = copy.deepcopy(incurable)
demonMissileEff.power = 35
demonMissile = skill("Missile Daemonium",getAutoId(demonSpell1.id,True),TYPE_DAMAGE,price=500,emoji='<:demonMissile:1226594720722190419>',effects=demonMissileEff,power=50,replay=True,cooldown=5,use=MAGIE,hpCost=5,group=SKILL_GROUP_DEMON,description="Inflige des dégâts à l'ennemi ciblé, réduit les soins qu'il reçoit et vous permet de rejouer votre tour")
sterialSoilSkill = skill("Terre Stérile","sterialSoilSKill",TYPE_DAMAGE,power=35,setAoEDamage=True,range=AREA_MONO,area=AREA_CIRCLE_1,use=MAGIE,emoji='<:burningGround:950256060923535370>')
sterialSoilDepl = depl("Terre Stérile",sterialSoilSkill,["<:sterialSoil:1226595905931706378>","<:sterialSoil:1226595905931706378>"],description="Inflige des dégâts directs supplémentaire aux ennemis présent dans la zone d'effet")
sterialSoilEff = effect("Terre Stérile","sterialSoilEff",callOnTrigger=sterialSoilDepl,type=TYPE_DEPL,emoji=sterialSoilSkill.emoji,trigger=TRIGGER_INSTANT)
sterialSoil = skill("Terre Stérile",getAutoId(demonMissile.id,True),TYPE_DAMAGE,price=500,use=MAGIE,power=100,cooldown=7,setAoEDamage=True,garCrit=True,area=AREA_CIRCLE_1,effects=sterialSoilEff,hpCost=15,group=SKILL_GROUP_DEMON,emoji=sterialSoilDepl.icon[0],description="Inflige des dégâts aux ennemis ciblés et invoque un déployable sous les pieds de la cible principale, infligeant des dégâts supplémentaires durant un petit moment. La cible principale subis forcément un coup critique lors des dégâts initiaux")
daemoniumTerraeMotusEff = effect("Daemonium Terrae Motus","daemoniumTerraeMotusEff",MAGIE,power=40,type=TYPE_DAMAGE,trigger=TRIGGER_END_OF_TURN,turnInit=3,area=AREA_CIRCLE_2,emoji='<:seismeDemoniaque:1226591474150408252>')
daemoniumTerraeMotus = skill(daemoniumTerraeMotusEff.name,getAutoId(sterialSoil.id,True),TYPE_DAMAGE,price=750,effects=daemoniumTerraeMotusEff,use=MAGIE,area=daemoniumTerraeMotusEff.area,power=int(daemoniumTerraeMotusEff.power*1.25),cooldown=7,hpCost=35,group=SKILL_GROUP_DEMON,emoji=daemoniumTerraeMotusEff.emoji[0][0],description="Inflige des dégâts aux ennemis ciblés. La compétence est répliquée trois fois en fin de tour de la cible principale")
angelStrikeEff = effect("Saut de l'Ange","angelStrikeEff",STRENGTH,trigger=TRIGGER_INSTANT,area=AREA_DONUT_2,emoji='<:angelStrikeEff:1226968261980324001>',type=TYPE_DAMAGE,power=80)
angelStrike = skill("Saut de l'Ange",getAutoId(daemoniumTerraeMotus.id,True),TYPE_DAMAGE,range=AREA_DIST_4,tpCac=True,price=500,effects=angelStrikeEff,cooldown=7,power=125,group=SKILL_GROUP_HOLY,emoji='<:angelStrike:1233110358445789235>',description="Saute sur l'ennemi ciblé en lui inglieant des dégâts. Les ennemis proches de la cibles reçoivent également des dégâts avec une puissance moindre")

trappedFieldDepl = depl("Terrain Minné",skill("Terrain Minné","trappedField",TYPE_DAMAGE,range=AREA_MONO,area=AREA_CIRCLE_2),["<:littleTrap:1227279093075153048>","<:littleTrap:1227279093075153048>"])
trappedFieldTrueDepl = copy.deepcopy(littleTrapDepl)
trappedFieldTrueDepl.power = 75
trappedFieldMockup = skill("Terrain Minné",getAutoId(angelStrike.id,True),TYPE_DEPL,range=AREA_CIRCLE_3,depl=trappedFieldDepl,emoji='<:trappedField:1227290251353919571>',cooldown=5,description="Cette compétence s'utilise comme un déployable. Pose 3 {0} {1} dans la zone ciblée. Les {0} {1} explosent si un ennemi marche à proximité ou après trois tours".format(trappedFieldTrueDepl.icon[0], trappedFieldTrueDepl.name))
trappedField = skill(trappedFieldMockup.name, trappedFieldMockup.id, TYPE_DAMAGE, range=trappedFieldMockup.range, area=trappedFieldMockup.depl.skills.area, emoji=trappedFieldMockup.emoji, cooldown=trappedFieldMockup.cooldown, description=trappedFieldMockup.description, price=500, power=trappedFieldTrueDepl.power, repetition=3)

surpriseJumpEff = effect("Mine Surprise","surpriseMine",type=TYPE_DEPL,callOnTrigger=littleTrapDepl,trigger=TRIGGER_INSTANT,emoji=littleTrapEff.emoji[0][0])
surpriseJumpForward = skill("Saut Surprise (Avant)",getAutoId(trappedFieldMockup.id,True),TYPE_DAMAGE,range=AREA_BIGDONUT,effectOnSelf=surpriseJumpEff,effBeforePow=True,tpBehind=True,power=35,replay=True,emoji='<:chipSurprise:1227279072451629237>',description="Pose une {0} {1} à vos pieds puis vous fait sauter sur l'ennemi ciblé avant de lui infliger des dégâts et vous permettre de rejouer votre tour".format(littleTrapEff.emoji[0][0], littleTrapDepl.name),cooldown=5)
surpriseJumpBackward = skill("Saut Surprise (Arrière)",surpriseJumpForward.id,True,TYPE_DAMAGE,range=AREA_CIRCLE_1,effectOnSelf=surpriseJumpEff,jumpBack=1,power=surpriseJumpForward.power,replay=True,emoji='<:jumpBack:1227296915805180036>',description="Inflige des dégâts à l'ennemi ciblé, pose une {0} {1} à vos pieds puis vous fait sauter en arrière avant de lui infliger des dégâts et vous permettre de rejouer votre tour".format(littleTrapEff.emoji[0][0], littleTrapDepl.name),cooldown=surpriseJumpForward.cooldown)
bundleSurpriseJump = skill("Saut Surprise",surpriseJumpBackward.id,TYPE_DAMAGE,replay=True,become=[surpriseJumpForward,surpriseJumpBackward],emoji=surpriseJumpForward.emoji,description="Vous permet d'utiliser {0} et {1}, deux compétences de déplacements rapides laissant une {2} {3} à vos pieds".format(surpriseJumpForward, surpriseJumpBackward, littleTrapEff.emoji[0][0], surpriseJumpBackward.effectOnSelf.callOnTrigger.name),price=500)

healingFieldDeplSkill = skill("Champ Herbu","healingFieldDeplSkill",TYPE_HEAL,area=AREA_CIRCLE_2,power=25,range=AREA_MONO,use=CHARISMA,emoji=mend.emoji)
healingFieldDepl = depl("Champ Herbu",healingFieldDeplSkill,["<:healingField:1228774328095473744>","<:healingField:1228774328095473744>"],description="Soigne les alliés dans la zone d'effet (**{0} {1}**)".format(statsEmojis[healingFieldDeplSkill.use],healingFieldDeplSkill.power))
healingFieldDeplEff = effect("Champ Herbu","healingFieldDeplEff",type=TYPE_DEPL,trigger=TRIGGER_INSTANT,callOnTrigger=healingFieldDepl,emoji=healingFieldDepl.icon[0])
healingField = skill("Champ Herbu",getAutoId(surpriseJumpForward,True),TYPE_HEAL,range=AREA_MONO,power=50,area=healingFieldDeplSkill.area,effectOnSelf=healingFieldDeplEff,emoji=healingFieldDeplEff.emoji[0][0],use=healingFieldDeplSkill.use,description="Soigne les alliés à proximité et place un {0} {1} sous vous pieds, soignant les alliés à l'intérieur durant un petit moment".format(healingFieldDepl.icon[0],healingFieldDepl.name),cooldown=7,price=750)

bombThrowEff = effect("Jeter de bombe","bombThrowEff",type=TYPE_SUMMON,lvl=2,area=AREA_DONUT_1,callOnTrigger="Petit Bombe",trigger=TRIGGER_INSTANT,emoji='<:bombThrow:1229038233309020222>')
bombThrow = skill("Jeter de bombe",getAutoId(healingField,True),TYPE_DAMAGE,price=500,power=75,effects=bombThrowEff,cooldown=5,emoji=bombThrowEff.emoji[0][0],description="Inflige des dégâts à l'ennemi ciblé et invoque {0} {1} {2} à côté de lui. Si les bombes ne peuvent être posées, elles explosent instantanéments".format(bombThrowEff.lvl,"<:terrabombB:1155475225979408454>",bombThrowEff.callOnTrigger))
bleedingTrapSkill = skill("Explosion","bleedingTrapSkill",TYPE_DAMAGE,power=50,price=500,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_CIRCLE_1,bleeding],area=AREA_CIRCLE_1,range=AREA_MONO,emoji="<:mudraLacer:1189975861068320768>")
bleedingTrapDepl = depl("Mine Lacérante",bleedingTrapSkill,icon=["<:bleedingTrap:1229038214032003103>","<:bleedingTrap:1229038214032003103>"],description="Un piège qui se déclanche quand un ennemi marche dessus ou après trois tours, infligeant des dégâts et {0} aux ennemis dans la zone d'effet".format(bleeding),trap=True)
bleedingTrap = skill("Mine Lacérante",getAutoId(bombThrow,True),TYPE_DEPL,price=500,depl=bleedingTrapDepl,emoji=bleedingTrapDepl.icon[0],description="Place un piège de lacération dans la zone ciblée, infligeant des dégâts et {0} aux ennemis lorsqu'il se déclanche".format(bleeding),cooldown=5)
fizzbang = skill("Balle Pyroteck",getAutoId(bleedingTrap,True),TYPE_DAMAGE,use=HARMONIE,cooldown=3,price=350,power=40,url="https://media.discordapp.net/attachments/927195778517184534/1233089227990896751/fizzbang.gif",replay=True,area=AREA_CIRCLE_1,description="Inflige des dégâts (Harmonie) aux ennemis ciblés et vous permet de rejouer votre tour",emoji='<:fizzbang:1232910382301970482>')
shortTeleport = skill("Courte Téléportation",getAutoId(fizzbang,True),TYPE_DAMAGE,use=MAGIE,range=AREA_DIST_5,garCrit=True,emoji="<:shortTeleport:1233097703832162324>",tpBehind=True,area=AREA_CONE_2,cooldown=5,percing=20,power=95,description="Vous téléporte derrière la cible et inflige des dégâts de zone dans sa direction. Dégâts doublés sur l'armure, précision accrue, ignore une partie de la résistance ennemie et inflige forcément un coup critique à la cible principale",price=500,damageOnArmor=2,accuracy=150)

# Skill
skills: List[skill] = [shortTeleport,fizzbang,dosisBundle,bleedingTrap,bombThrow,healingField,bundleSurpriseJump,trappedField,angelStrike,daemoniumTerraeMotus,sterialSoil,demonMissile,demonSpell1,timeRip,counterTime,lenaInkStrike,toxiOvercharge, smnAnais,lavenderViel,markInfex,drkCombo,triSlashdown,featherCross,sectumsempra,magicMissile,trainePlume,smnMyrlope,inspiration,klikliQCombo,altyQCombo,gwenyQCombo,quickShot,bloodmissiles,fanVirBundle,rapidFire,dechargeGausseSolo,ricochetSolo,gangrene,intenseCure,shareMark,propagPas,radiance,lifeFontain,desyncBen,revif,smnSpaceTurets,denoument,royalShield,starDust,timeManip,krakenCharge,stoneLame,aerLame,iceLame,fireLame,timeGrenade,healerGlare,kliBloody,celestialChoc,rajeunissement,healingTimebomb,timeBomb,inconsCollect,holos,tactician,magicBarrier,phenixRevive,dualSupp,dualEnergyDrain,squidRoll,selfMemoria,gemmes,infuEther,exploPetal,fairyLiberation,lanceTox2,lanceTox3,skySharter,lycantStrike,increaseVibrations,renforPhys,dualCast,komoriHerit,inMemoria,ikishoten,hissatsu,Hauringusutomusodo,eternalLight,lenaDrone1,analysedShot,bento,snowFall,higanbana,brotherHood,meditate,bundleRixeEva,phenixSpirit,dvinRegen,dvinRegen2,divinVeal,sustain,curl,stimulate,hexadecaComb,altyStrike,altyPenta,pandaiStrike,gwenCharge,gwenPenta,kStrike,gravPulse,guardianAngel,pentastrike,moonLight,buffMoonBundle,debuffMoonBundle,ripping,weakPoint,justiceEnigma,holyVoice,plongeFracas,revolutionFracas,fracas,synastie,purify2,nonVitaUnionis,sinisterLux,flammaSinister,decomposition ,putrefaction,lifeLight,lifeFlame,moramMortem,moramMortem2,infDraw,funDraw,seitonTenchu,echecEtMat,deathPercing,healingSacrifice,summonHinoro,comboHeatedCleanShot,leadShot,dismantle,megaVent,gigaChad,soulWave,soulTwin,soulSceal,magma,orage,bastion,corruptusArea,tripleChoc,florChaot,astraRegenEarth,astraIncurStrike,astraRegenPhase,bunshin,dreamInADream,intervantion,intuitionFoug,redrum,anticipation,rubyLight,dislocation,tacShield,phalax,phenixDance,bloodDemonBundle,umbraMortis,deterStrike,thunderFiole,sernade,vibrSon,dissonance,stigmate,exploShot,heroicFantasy,mageBalad,martialPean,vanderManuet,manafication,enhardissement,blastArrow,apexArrow,dmonReconstitution,dmonReconstitution2,dmonDmg,dmonCrit,dmonEnd,dmonAgi,piedVolt,elipseTerrestre,clock,hourglass,ebranlement,hearthFrac,freezeArrow2,freezeArrow,exploArrow,immoArrow,spectralFurie,spectralCircle,ghostlyCircle,silvArmor,UmbralTravel,carnage,assasinate,physTraqnard,fairyTraqnard,blodTraqnard,lifeSeed,antConst,constBen,mend,lillyTransform,forestGarde,ultraSignal,intox,epidemic,sacredSoil,inkStrike,trizooka,inkzooka,tacticooler,lacerTrap,lohicaBrouillad,bigBubbler,asile,sonarPaf,convictionVigilante,convicPro,convictTet,convictEncht,miracle,rivCel,toxicon,seraphStrike,
    bundleFetu,soulPendant,corruptBecon,moissoneur,bundleLemure,lowBlow,legStrike,provoke,fanRevol,demonLand,demonArmor,demonArmor2,demonConst,
    comboConfiteor,cryoChargeBundle,pyroChargeBundle,drill,anchor,chainsaw,mysticShot,cycloneEcarlate,sillage,cassMont,finalClassique,bundleOffr,tetragramme,lightEstoc,lightTranche,lightShot,lightPulse,accelerant,tripleAttaque,expultion,acidRain,coroRocket,coroMissile,coroShot,quadFleau,charmingPandant,kralamSkill,windDance,barrage,hemoBomb,dmonProtect,raisingPheonix,fairyGarde,sumLightButterfly,fairySlash,plumRem,fairyBomb,bloodBath,erodAoe,divineAbne,astrodyn,cercleCon,aliceFanDanse,plumeCel,plumePers,pousAviaire,demonRegen,demonLink,bloodBath2,altyCover,klikliStrike,gwenyStrike,mve2,krasis,graviton,temperance,terachole,aquavoile,misery,tangoEnd,danseStarFall,graviton2,invocAutTour,invocAutFou,invocAutQueen,recall,divineBenediction,divineCircle,divineGuid,uberCharge,petalisation,roseeHeal,floraisonFinale,vampirisme2,krystalisation,regenVigil,fragmentation,machDeFer,lanceTox,trickAttack,aurore2,holyShieltron,kerachole,gigaFoudre,morsTempSkill,combustion,morsCaudiqueSkill,lbRdmCast,lightEarth,darkAmb,solarEruption,firstArmor,refLum,refConc,dephaIncant,cwFocus,propaUlt,cwUlt,sanguisGladio,sanguisGladio2,cardiChoc,chiStrike,elemShield,shieldAura,horoscope,ShiUltimate,intaveneuse,decolation,corGra,finalFloral,divineSave,redemption,fireElemUse,waterElemUse,airElemUse,earthElemUse,lightElemUse,darkElemUse,spaceElemUse,timeElemUse,bleedingConvert,revelation,maitriseElementaire,magicEffGiver,physEffGiver,danceFas,selenomancie,holiomancie,partner,exhibitionnisme,invocTitania,dmonBlood,hollyGround,hollyGround2,burningGround,blueShell,nanoHeal,ironHealth,windBal,brasier2,earthUlt2,geyser,rouletteSkill,constShot,const2Shot,undead,ironStormBundle,bolide,invincible,holmgang,comboVerBrasier,galvanisation,contreDeSixte,lifeWind,ice2,renf2,entraide,perfectShot,lastRessource,strengthOfDesepearance,nova,deathShadow,comboVerMiracle,comboFaucheCroix,theEndCast,cure2Bundle,assises,debouses,impact,heartStone,erodStrike,genesis,invertion,pneuma,absorbingStrike,absorbingArrow,absorbingStrike2,absorbingArrow2,magiaHeal,aff2,bloodPact,expediant,divination,macroCosmos,tintabule,bundleCaC,engage,autoBombRush,killerWailUltimate,invocSeaker,darkBoomCast,mageSkill,doubleShot,harmShot,benitWater,shareSkill,extraMedica,foullee,lifePulseCast,crimsomLotusCast,abnegation,foyer,sweetHeat,darkSweetHeat,shell,nacreHit,holyShot,demonStrike,purify,benediction,transfert,blackDarkMagic,fisure,seisme,abime,extermination,darkHeal,calestJump,lohicaUltCast,fairyFligth,aliceDance,aurore,crep,quickCast,pepsis,darkShield,rencCel,valse,finalTech,dissi,intelRaise,ultRedirect,clemency,liuSkillSus,liaSkillSus,lioSkillSus,lizSKillSus,reconst,medicamentum,ultMonoArmor,inkRes,inkRes2,booyahBombCast,propag,invocCarbSaphir,invocCarbObsi,supprZone,cosmicPower,requiem,magicRuneStrike,infinitDark,preciseShot,troublon,haimaBundle,physicRune,magicRune,lightBigHealArea,focus,fairyRay,bleedingPuit,idoOS,proOS,preOS,geoConCast,kikuRes,memClemCastSkill,roses,krysUlt,chaosArmor,firelame,airlame,waterlame,mudlame,shadowLame,timeLame,lightLame,astralLame,idoOH,proOH,altOH,lightAura2,tripleMissiles,lightHeal2,extraEting,strengthOfWillCast,sixtineUlt,hinaUlt,julieUlt,invocSeraf,bloodCross,soulagement,bloodyStrike,infraMedica,magAchSkill,flambeSkill,fireCircle,waterCircle,airCircle,earthCircle,fireShot,waterShot,airStrike,earthStrike,spaceMagicCombo,spaceSp,timeMagicCombo,timeSp,renisurection,demolish,contrainte,trouble,infirm,croissance,destruction2,infectFiole,bigLaser2,bigMonoLaser2,invocBat2,invocCarbunR,concen,memAlice2,blackHole,blackHole2,renforce,steroide,focal,suppr,revitalisation,onde,eting,stingray,darknessMagicCombo,lightMagicCombo,derobade,ferocite,ironWillSkill,royaleGardeSkill,defi,ombralStrike,laceration,convert,vampirisme,fireMagicCombo,waterMagicCombo,airMagicCombo,earthMagicCombo,bleedingArrow,bleedingDague,swordDance,shot,percingArrow,percingLance,highkick,multishot,rocklance,infinitFire,storm,innerdarkness,divineLight,icelance,onstage,kiss,secondSun,oneforall,uppercut,stalactic,linx,bombRobot,isolement,secondWind,blindage,adrenaline,lapSkill,burst,descart,thinkSkill,invocFee,invocCarbT,invocCarbE,splashdown,multiMissiles,monoMissiles,invocBat,poisonus,protect,explosionCast,splatbomb,lightAura,cure,balayette,contrecoup,exploMark,chaos,unHolly,soupledown,inkarmor,coffeeSkill,theSkill,gpotion,bpotion,zelian,courage,nostalgia,draw25,siropMenthe
] + elemArrowSkill + elemRuneSkill + horoSkills + tablAdvBaseElemSkills + baseSkills

if not(isLenapy):
    skills.append(bestSkill)

importantSkills = [deathShadow.id, umbraMortis.id, soulSceal.id]
useElemEffId = [fireElemUse.id,waterElemUse.id,airElemUse.id,earthElemUse.id,lightElemUse.id,darkElemUse.id,spaceElemUse.id,timeElemUse.id]
finFloOtherSkillsId = [valse.id, finalTech.id,roseeHeal.id,croissance.id]
tablRosesEff,tablRosesSkillsId,tablRosesId = [roseRed,roseDarkBlu,rosePink,roseYellow,roseBlue,roseGreen], [aliceDance.id,corGra.id,onstage.id,crimsomLotus.id,floraisonFinale.id,petalisation.id,danceFas.id],[roseRed.id,roseDarkBlu.id,rosePink.id,roseYellow.id,roseBlue.id,roseGreen.id]

horoscopeEff = [
    [effect("Bélier","horBélier",turnInit=-1,emoji='<:belier:960319494167867473>',silent=True),[[STRENGTH,2],[ENDURANCE,3]]],
    [effect("Taureau","horTaureau",turnInit=-1,emoji='<:taureau:960319518004092939>',silent=True),[[STRENGTH,3],[ENDURANCE,2]]],
    [effect("Gémeaux","horGémeaux",turnInit=-1,emoji='<:gemeaux:960319543228649523>',silent=True),[[CHARISMA,1],[INTELLIGENCE,2],[MAGIE,2]]],
    [effect("Cancer","horCancer",turnInit=-1,emoji='<:cancer:960319573003997215>',silent=True),[[AGILITY,1],[STRENGTH,2],[MAGIE,2]]],
    [effect("Lion","horLio",turnInit=-1,emoji='<:lion:960319606050914336>',silent=True),[[STRENGTH,5]]],
    [effect("Vierge","horVierge",turnInit=-1,emoji='<:vierge:960319632982540329>',silent=True),[[CHARISMA,5]]],
    [effect("Balance","horBalance",turnInit=-1,emoji='<:balance:960319658823667762>',silent=True),[[INTELLIGENCE,2],[MAGIE,3]]],
    [effect("Scorpion","horScorpion",turnInit=-1,emoji='<:scorpion:960319682861232211>',silent=True),[[STRENGTH,3],[MAGIE,2]]],
    [effect("Sagittaire","horSagittaire",turnInit=-1,emoji='<:sagittaire:960319710380036146>',silent=True),[[MAGIE,5]]],
    [effect("Capricorne","horCapricorne",turnInit=-1,emoji='<:capricorne:960319731343175781>',silent=True),[[MAGIE,3],[ENDURANCE,2]]],
    [effect("Verseau","horVerseau",turnInit=-1,emoji='<:verseau:960319751136108546>',silent=True),[[INTELLIGENCE,3, PRECISION,2]]],
    [effect("Poisson","horPoisson",turnInit=-1,emoji='<:poisson:960319770337628191>',silent=True),[[AGILITY,3],[PRECISION,2]]]
]

hroscopeNickNames = ["Nébulique","Galactique","Cosmique","Spatiale","Stellaire","Macroscopique","Infini"]
tablHoroSkillsId = getArrayAutoId(windDance.id,len(horoSkills),True)
for cmpt in range(len(horoSkills)):
    horoSkills[cmpt].description += "\n\n__Effet supplémentaire avec l'élément {0} Astral :__\nCette compétence est considérée comme une compétence élémentaire.\nSi vous ou un de vos alliés a la compétence {1} __Horoscope__ d'équipé et n'est pas sous l'effet de {2} __{3}__, lui ocrtoi le dit effet et vous octroi {4} __{5}__".format(elemEmojis[ELEMENT_SPACE],horoscope.emoji,horoscopeEff[cmpt][0].emoji[0][0],horoscopeEff[cmpt][0].name,tablElemEff[ELEMENT_SPACE].emoji[0][0],tablElemEff[ELEMENT_SPACE].name)
    horoSkills[cmpt].emoji, horoSkills[cmpt].id = horoscopeEff[cmpt][0].emoji[0][0], tablHoroSkillsId[cmpt]

lb2Mono = skill("Danse de la lame","lb",TYPE_DAMAGE,power=int(transBerserk.power*0.7),setAoEDamage=True,range=transBerserk.range,emoji=trans.emoji,use=HARMONIE,description="Inflige des dégâts harmoniques à l'ennemi ciblé\n__Puissance :__ {power}",accuracy=200,url='https://media.discordapp.net/attachments/971787705216274495/988822433471545384/20220621_170114.gif')
lb2Line = skill("Desperados","lb",TYPE_DAMAGE,power=int(transObs.power*0.7),range=transObs.range,area=transObs.area,emoji=trans.emoji,use=HARMONIE,description="Inflige des dégâts harmoniques aux ennemis dans une zone linéaire\n__Puissance :__ {power}",accuracy=200,url='https://media.discordapp.net/attachments/971787705216274495/988822431839969280/20220621_170516.gif')
lb2AoE = skill("Conviction de Stella","lb",TYPE_DAMAGE,power=int(transEnch.power*0.7),range=transMage.range,area=AREA_CIRCLE_2,emoji=trans.emoji,use=HARMONIE,description="Inflige des dégâts harmoniques aux ennemis dans la zone d'effet\n__Puissance :__ {power}",accuracy=200,url='https://media.discordapp.net/attachments/971787705216274495/988822433014378516/20220621_170240.gif')
lb2Heal = skill("Souffle de Nacialisla","lb",TYPE_HEAL,power=int(transAlt.power*0.7),setAoEDamage=True,range=transAlt.range,area=transAlt.area,emoji=trans.emoji,use=HARMONIE,description="Soigne les alliés dans la zone d'effet en réanimant les alliés proches\n__Puissance :__ {power}",effectAroundCaster=[TYPE_RESURECTION,AREA_CIRCLE_3,int(transAlt.effectAroundCaster[2]*0.65)],url='https://media.discordapp.net/attachments/971787705216274495/988822432288739439/20220621_170410.gif')
lb2ArmorEff = effect("Proctection de Nacialisla",'lb2Armor', stat=HARMONIE,overhealth=int(effTransPre.overhealth*0.7),turnInit=2,emoji=effTransPre.emoji)
lb2Armor = skill("Protection de Nacialisla","lb",TYPE_ARMOR,effects=lb2ArmorEff,area=transPre.area,range=AREA_MONO,emoji=trans.emoji,description="Octroi une armure aux alliés à portée\n__Puissance de l'armure :__ {0}".format(lb2ArmorEff.overhealth),url='https://media.discordapp.net/attachments/971787705216274495/988822434016792596/20220621_165940.gif')
lb1Mono = skill("Ardeur courageuse","lb",TYPE_DAMAGE,power=int(transBerserk.power*0.4),accuracy=200,range=transBerserk.range,emoji=trans.emoji,use=HARMONIE,description="Inflige des dégâts harmoniques à l'ennemi ciblé\n__Puissance :__ {power}",url='https://media.discordapp.net/attachments/971787705216274495/988822435098947604/20220621_165401.gif')
lb1Line = skill("Gros calibre","lb",TYPE_DAMAGE,power=int(transObs.power*0.4),accuracy=200,range=transObs.range,area=transObs.area,emoji=trans.emoji,use=HARMONIE,description="Inflige des dégâts harmoniques aux ennemis dans une zone linéaire\n__Puissance :__ {power}",url='https://media.discordapp.net/attachments/971787705216274495/988822436982190130/20220621_164657.gif')
lb1AoE = skill("Décharge Stellaire","lb",TYPE_DAMAGE,power=int(transEnch.power*0.4),accuracy=200,range=transMage.range,area=AREA_CIRCLE_1,emoji=trans.emoji,use=HARMONIE,description="Inflige des dégâts harmoniques aux ennemis dans la zone d'effet\n__Puissance :__ {power}",url='https://media.discordapp.net/attachments/971787705216274495/988822435753250916/20220621_165155.gif')
lb1Heal = skill("Souffle de la Terre","lb",TYPE_HEAL,power=int(transAlt.power*0.4),range=transAlt.range,area=transAlt.area,emoji=trans.emoji,use=HARMONIE,description="Soigne les alliés dans la zone d'effet\n__Puissance :__ {power}",url="https://media.discordapp.net/attachments/971787705216274495/988822436315279360/20220621_164949.gif")
lb1ArmorEff = effect("Proctection de la Terre",'lb1Armor', stat=HARMONIE,overhealth=int(effTransPre.overhealth*0.4),turnInit=1,emoji=effTransPre.emoji)
lb1Armor = skill("Proctection de la Terre","lb",TYPE_ARMOR,effects=lb1ArmorEff,area=transPre.area,range=AREA_MONO,emoji=trans.emoji,description="Octroi une armure aux alliés à portée\n__Puissance de l'armure :__ {0}".format(lb1ArmorEff.overhealth),url='https://media.discordapp.net/attachments/971787705216274495/988822434662723584/20220621_165803.gif')

lb3Tabl = [transBerserk, transObs, transPoidsPlume, transIdo, transPre, transTetBrule, transMage, transAlt, transEnch, transPro, transAtt, transSorceler, transIno, transAttentif, transMasc, lb2Mono]
for cmpt in range(len(lb3Tabl)-1):
    lb3Tabl[cmpt].name, lb3Tabl[cmpt].description = lbNames[cmpt], lbDesc[cmpt]
    if lb3Tabl[cmpt].type in [TYPE_DAMAGE,TYPE_HEAL]:
        lb3Tabl[cmpt].description += "\n__Puissance :__ {0}".format(lb3Tabl[cmpt].power*lb3Tabl[cmpt].repetition)
    elif lb3Tabl[cmpt].type == TYPE_ARMOR:
        lb3Tabl[cmpt].description += "\n__Puissance de l'armure :__ {0}".format(lb3Tabl[cmpt].effects[0].overhealth)
    elif lb3Tabl[cmpt].type == TYPE_BOOST:
        lb3Tabl[cmpt].description += "\n__Puissance du bonus :__ {0}".format(lb3Tabl[cmpt].effects[0].strength)
    if cmpt < len(limitBeakGif):
        lb3Tabl[cmpt].url = limitBeakGif[cmpt]
altHoroSkillsTabl = []
for skilly in horoSkills:
    tempSkilly = copy.deepcopy(skilly)
    tempSkilly.condition = [0,1,ELEMENT_SPACE]
    altHoroSkillsTabl.append(tempSkilly)

lb2Tabl = [lb2Mono, lb2Line, lb2Mono, lb2Heal, lb2Armor, lb2Mono, lb2AoE, lb2Heal, lb2AoE, lb2Armor, lb2Heal, lb2AoE, lb2Armor, lb2Line, lb2Mono, lb2Heal]
lb1Tabl = [lb1Mono, lb1Line, lb1Mono, lb1Heal, lb1Armor, lb1Mono, lb1AoE, lb1Heal, lb1AoE, lb1Armor, lb1Heal, lb1AoE, lb1Armor, lb1Line, lb1Mono, lb2Heal]

lb1MinTabl = [lb1Mono,lb1Line,lb1AoE,lb1Heal,lb1Armor]
lb2MinTabl = [lb2Mono,lb2Line,lb2AoE,lb2Heal,lb2Armor]
lb4 = skill("Conviction de Silicia","lb",TYPE_DAMAGE,power=int(transBerserk.power*1.5),accuracy=200,garCrit=True,emoji=trans.emoji,description="Inflige de lourd dégâts à un ennemi ciblé et réanime les alliés vaincus autour de vous\n__Puissance :__ {power}",use=HARMONIE,effectAroundCaster=[TYPE_RESURECTION,AREA_ALL_ALLIES,350],url='https://media.discordapp.net/attachments/989526512288030742/991051124746387506/20220627_204219.gif')

# SkillsCat
skillsCat: List[List[skill]] = []
for cmpt in range(TYPE_DEPL+1):
    skillsCat.append([])

# FindSkill
dictTablSkills, dictSkills = {}, {}

for skilly in skills:
    if type(skilly) == skill:
        try:
            dictTablSkills[skilly.id[:2]].append(skilly)
        except KeyError:
            dictTablSkills[skilly.id[:2]] = [skilly]
        except Exception as e:
            raise Exception("{0} : Id {1}".format(skilly.name,e))
        skillsCat[skilly.type].append(skilly)
        dictSkills[skilly.id] = skilly

def findSkill(skillId) -> skill:
    """Renvoie une compétence Skill, si trouvé"""
    typi = type(skillId)
    if typi == skill:
        return skillId
    elif typi != str or skillId == "0":
        return None
    else:
        if skillId.startswith("\n"):
            skillId = skillId.replace("\n","")

        try:
            return dictSkills[skillId]
        except KeyError:
            for a in skills:
                if a.name.lower() == skillId.lower():
                    return a

# Exclusive Repartition
def exclusiveRepartition():
    """Print the number of skills exclusives to certains aspiration / main element / sec element"""
    tablExclu, ttSkill, ttSkillwConds = [[],[],[],[],[]], 0, 0
    for cmpt in range(len(inspi)):
        tablExclu[0].append([])
    for cmpt in range(len(elemNames)):
        tablExclu[1].append([])
    for cmpt in range(len(elemNames)):
        tablExclu[2].append([])
    for skilly in skills:
        if skilly.condition != []:
            tablExclu[skilly.condition[1]-1][skilly.condition[2]].append(skilly)
            ttSkillwConds +=1
        elif skilly.group == SKILL_GROUP_DEMON:
            tablExclu[3].append(skilly)
            ttSkillwConds +=1
        elif skilly.group == SKILL_GROUP_HOLY:
            tablExclu[4].append(skilly)
            ttSkillwConds +=1
        
        ttSkill += 1

    print("Skills condition repartition =======================")
    print("Aspirations --------------------------------")
    for cmpt in range(len(tablExclu[0])):
        print("{0} : {1}".format(inspi[cmpt],len(tablExclu[0][cmpt])))
    print("ElemPrinc ----------------------------------")
    for cmpt in range(len(tablExclu[1])):
        print("{0} : {1}".format(elemNames[cmpt],len(tablExclu[1][cmpt])))
    print("ElemSec ------------------------------------")
    print("Groupe -------------------------------------")
    print("Démon : {0}\nDivin : {1}".format(len(tablExclu[3]),len(tablExclu[4])))
    print("Totals -------------------------------------\nNb Comp : {0}\nNb Comp w/ condition : {1} ({2}%)".format(ttSkill,ttSkillwConds,round(ttSkillwConds/ttSkill*100,2)))

def getSkillsRanges():
    skillMelee, skillDist, skillMixt = [], [], []
    for skilly in skills:
        if skilly.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]:
            if skilly.range in areaMelee:
                skillMelee.append(skilly)
            elif skilly.range in areaDist:
                skillDist.append(skilly)
            elif skilly.range in areaMixte:
                skillMixt.append(skilly)

    print("Compétences mêlées : {0}\nCompétences distances : {1}\nCompétences mixtes : {2}".format(len(skillMelee),len(skillDist),len(skillMixt)))

astraEarthEffList = [regenEarthEff]
for eff in astraEarthEffList:
    copyTabl, eff.description = astraEarthEffList[:], eff.description + "\n\nSi cet effet est cumulé avec "
    copyTabl.remove(eff)
    for effName in copyTabl:
        eff.description += "{0} {1}".format(effName.emoji[0][0],effName.name)
        if len(copyTabl) > 1 and effName != copyTabl[-2]:
            eff.description += ", "
    eff.description += " ou lui-même, seul l'effet le plus ancien est déclanché"

for cmpt in range(len(astraEarthEffList)):
    astraEarthEffList[cmpt] = astraEarthEffList[cmpt].id
