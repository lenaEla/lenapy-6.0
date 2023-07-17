from advObjects.advSkills_1 import *
reaperEff.description += "\n\n" + deathMark.description.splitlines()[-1].replace("{0} __{1}__".format(reaperEff.emoji[0][0],reaperEff.name),"{0} __{1}__".format(deathMark.emoji[0][0],deathMark.name))

hexadecaCombFinal = skill('Hexadecafrappe Enchantée',getAutoId(altyStrike.id,True),TYPE_DAMAGE,use=MAGIE,power=100,range=AREA_CIRCLE_1,emoji='<:sixtyComboFinal:1098615928998080593>',affSkillMsg=False,description="Durant trois tours, inflige une multitude d'attaque, en réduisant la résistance de la cible. Le dernier tour se termine par une attaque suppplémentaire infligeant des dégâts de zone",accuracy=200,area=AREA_LINE_3,ultimate=True,cooldown=7)
hexadecaCombFinal_c = effect("Enchaînement - {replicaName}","sixtineCombFin",silent=True,replique=hexadecaCombFinal,turnInit=2)
sixtLacerEff1 = copy.deepcopy(lacerEff)
sixtLacerEff1.resistance = -10
hexadecaComb3 = skill('Hexadecafrappe Enchantée',hexadecaCombFinal.id,TYPE_DAMAGE,use=MAGIE,power=(120/5),replay=True,repetition=5,price=750,range=AREA_CIRCLE_1,emoji='<:sixtyCombo3:1098615885813534791>',description=hexadecaCombFinal.description,ultimate=True,cooldown=7,effectOnSelf=hexadecaCombFinal_c,effects=sixtLacerEff1)
hexadecaComb3_c = effect("10 hit combo","sixtineComb3",silent=True,replique=hexadecaComb3,turnInit=2)
sixtLacerEff2 = copy.deepcopy(sixtLacerEff1)
sixtLacerEff2.turnInit = 2
hexadecaComb2 = skill('Hexadecafrappe Enchantée',hexadecaCombFinal.id,TYPE_DAMAGE,use=MAGIE,power=(110/5),repetition=5,price=750,range=AREA_CIRCLE_1,emoji='<:sixtyCombo2:1098615864414179381>',description=hexadecaCombFinal.description,ultimate=True,cooldown=7,effectOnSelf=hexadecaComb3_c,effects=sixtLacerEff2)
hexadecaComb2_c = effect("5 hit combo","sixtineComb2",silent=True,replique=hexadecaComb2,turnInit=2)
sixtLacerEff3 = copy.deepcopy(sixtLacerEff1)
sixtLacerEff3.turnInit = 3
hexadecaComb = skill('Hexadecafrappe Enchantée',hexadecaCombFinal.id,TYPE_DAMAGE,use=MAGIE,power=(100/5),repetition=5,price=750,range=AREA_CIRCLE_1,emoji='<:sixtyCombo1:1098615843048399022>',description=hexadecaCombFinal.description,ultimate=True,cooldown=7,effectOnSelf=hexadecaComb2_c,effects=sixtLacerEff3)

galvaniseEff = effect("Galvanisation","galvaniseSummon",trigger=TRIGGER_INSTANT,emoji='<:galvanise:1104726746017837106>',iaPow=50,power=1,description="Augmente de **{0}** tour la durée de vie de l'invocation ciblée",type=TYPE_UNIQUE)
sustainEff = effect("Sustain","sustain",stackable=True,stat=HARMONIE,power=40,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,emoji='<:sustain:1104726732663181353>',turnInit=3)
sustain = skill("Sustain",getAutoId(hexadecaCombFinal.id,True),TYPE_INDIRECT_HEAL,price=500,area=AREA_SUMMON,range=AREA_MONO,effects=[sustainEff,galvaniseEff],cooldown=5,description="Octroi un effet régénérant à vos invocations et augmente leur durée de vie",emoji='<:sustain:1104511188483711037>')
curlEff = copy.deepcopy(defenseUp)
curlEff.stat, curlEff.turnInit, curlEff.power = HARMONIE, 3, 6.5
curl = skill("Curl",getAutoId(sustain.id,True),TYPE_BOOST,price=500,area=AREA_SUMMON,range=AREA_MONO,effects=[curlEff,galvaniseEff],cooldown=5,description="Réduit les dégâts subis par vos invocations et augmente leur durée de vie",emoji='<:curl:1104511212579999826>')
stimEff1, stimEff2 = copy.deepcopy(dmgUp), copy.deepcopy(healDoneBonus)
stimEff1.stat, stimEff1.power, stimEff2.power = HARMONIE,5,20
stimEff1.turnInit = stimEff2.turnInit = 3
stimulate = skill("Stimulate",getAutoId(curl.id,True),TYPE_BOOST,price=500,area=AREA_SUMMON,range=AREA_MONO,effects=[stimEff1,stimEff2,galvaniseEff],cooldown=5,description="Augmente les dégâts infligés et les soins réalisés par vos invocations et augmente leur durée de vie",emoji='<:stimulation:1104511237301227681>')
divinVealEff, divinVealEff2 = effect("Voile Divin","divinVeal",ENDURANCE,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,turnInit=3,overhealth=65,emoji='<:voile:1104762361929281547>',stackable=True), copy.deepcopy(absEff)
divinVealEff2.power, divinVealEff2.turnInit = 15, divinVealEff.turnInit
divinVeal = skill("Voile Divin",getAutoId(stimulate.id,True),TYPE_ARMOR,price=500,effects=[divinVealEff],range=AREA_MONO,area=AREA_CIRCLE_2,effectOnSelf=divinVealEff2,cooldown=5,maxHpCost=10,group=SKILL_GROUP_HOLY,emoji='<:voileDivin:1104762549737631824>',description="Octroi une armure à vous et vos alliés proches et augmente les soins que vous recevez")
dvinRegenEff = effect("Régénération Divine","dvinRegen",CHARISMA,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,power=40,turnInit=3,emoji='<:dvinRegen:1104496736845713440>',stackable=True)
dvinRegen = skill("Régénération Divine Etendue",getAutoId(divinVeal.id,True),TYPE_INDIRECT_HEAL,price=500,effects=dvinRegenEff,area=AREA_CIRCLE_2,maxHpCost=15,cooldown=5,group=SKILL_GROUP_HOLY,emoji=dvinRegenEff.emoji[0][0],description="Octroi un effet régénérant aux alliés ciblés")
dvinRegen2 = skill("Régénération Divine Concentrique",getAutoId(dvinRegen.id,True),TYPE_INDIRECT_HEAL,price=500,effects=dvinRegenEff,effPowerPurcent=150,maxHpCost=15,cooldown=5,group=SKILL_GROUP_HOLY,emoji=dvinRegenEff.emoji[0][0],description="Octroi un puissant effet régénérant à l'allié ciblé")
phenixSpiritEff = copy.deepcopy(galvaniseEff)
phenixSpiritEff.power = 3
phenixSpirit = skill("Esprit Phénix",getAutoId(dvinRegen2.id,True),TYPE_BOOST,price=750,emoji='<:phenixSkill1_1:1066006765340196995>',effects=phenixSpiritEff,range=AREA_MONO,area=AREA_SUMMON,cooldown=7,description="Augmente de 3 tours la durée de vie de vos invocations")

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
higanbanaEff = effect("Higanbana","Higanbana",STRENGTH,power=20,turnInit=7,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,lvl=7,emoji='<:higanbana:1115723081135161424>',stackable=True)
higanbana = skill("Higanbana",getAutoId(bundleRixeEva.id,True),TYPE_DAMAGE,750,power=100,cooldown=7,range=AREA_CIRCLE_1,emoji=higanbanaEff.emoji[0][0],description="Inflige des dégâts ainsi qu'un effet de dégâts périodique durant un long moment à l'ennemi ciblé",effects=higanbanaEff)

snowFall = skill("Avalanche",getAutoId(higanbana.id,True),TYPE_DEPL,500,use=INTELLIGENCE,depl=snowFallGlypheDepl,emoji=snowFallGlypheDepl.icon[0],cooldown=5,condition=[EXCLUSIVE,ASPIRATION,PROTECTEUR],description="Pose un {0} {1} sur la cellule ciblé. Si cette dernière est libre, vous téléporte dessus. Le glyphe inflige des dégâts aux ennemis et augmente la résistance des alliés dans la zone d'effet".format(snowFallGlypheDepl.icon[0],snowFallGlypheDepl.name),range=AREA_CIRCLE_2)
bentoEff = effect("Sharpels","bentoEff",STRENGTH,power=45,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,area=AREA_DONUT_2,emoji='<:bento:1116674708214128640>')
bento = skill("Bento-Torpille",getAutoId(snowFall.id,True),TYPE_DAMAGE,500,80,area=AREA_CIRCLE_1,effects=bentoEff,cooldown=5,description="Inflige des dégâts de zone autour de l'ennemi ciblé ainsi qu'une seconde explosion infligeant des dégâts indirectes de zone supplémentaire",emoji='<:bento:1116674708214128640>')
analysedShot_1 = skill("Tir d'Analyse",getAutoId(bento.id,True),TYPE_DAMAGE,500,130,condition=[EXCLUSIVE,ASPIRATION,OBSERVATEUR],accuracy=250,percing=15,garCrit=True,emoji='<:analysedShot:1116226548081639434>',cooldown=6,description="Augmente les dégâts critiques reçus par l'ennemi ciblé durant le tour de chargement puis inflige une attaque forcément critique avec une grande précision qui ignore une partie de la résistance ennemie")
analyseCritWeak = effect("Faiblesse Critique","critWeakNEss",power=10,turnInit=1,type=TYPE_MALUS,description="Un point faible de l'ennemi augmente les dégâts qu'il reçoit de la part de coups critiques directs",emoji='<:critWeakness:1058021637624188958>')
analysedShot_c = effect("Cast - {replicaName}","analysedShotc",replique=analysedShot_1,turnInit=2,emoji='<:analyse:1116225083904626748>')
analysedShot = copy.deepcopy(analysedShot_1)
analysedShot.power, analysedShot.effects, analysedShot.effectOnSelf = 0, [analyseCritWeak], analysedShot_c
lenaDrone1 = skill("Drone Artilleur",getAutoId(analysedShot_1.id,True),TYPE_SUMMON,500,range=AREA_CIRCLE_2,invocation="Drone Artilleur",cooldown=7,condition=[EXCLUSIVE,ASPIRATION,OBSERVATEUR],emoji='<:lenaDrone1B:1116262917868888185>',description="Permet d'invoquer un drone infligeant des dégâts et augmentant les dégâts critiques subis par les ennemis")
eternalLightEff = effect("Aveuglement éternel","eternalBlind",MAGIE,precision=-5,turnInit=3,type=TYPE_MALUS,emoji="<:MyEyes:784226383018328115>")
eternalLight_1 = skill("Lumière Eternelle",getAutoId(lenaDrone1.id,True),TYPE_DAMAGE,emoji='<:eternalLight:1116761926052089856>',accuracy=250,price=0,power=120,range=AREA_MONO,area=AREA_ALL_ENEMIES,setAoEDamage=True,cooldown=7,ultimate=True,use=MAGIE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_LIGHT],description="Après un tour de chargement, inflige des dégâts à tous les ennemis qu'importe leur position et réduit leur précision pendant un petit moment",damageOnArmor=0.8,effectAroundCaster=[TYPE_MALUS,AREA_ALL_ENEMIES,eternalLightEff])
eternalLight_c = effect("Cast - {replicaName}","eternalLightc",turnInit=2,replique=eternalLight_1,silent=True)
eternalLight = copy.deepcopy(eternalLight_1)
eternalLight.power, eternalLight.effectOnSelf, eternalLight.effectAroundCaster = 0, eternalLight_c, None

Hauringusutōmusōdo1_eff1 = effect("Hauringufurarī","Hauringusutōmusōdo1_eff1",AGILITY,power=75,area=AREA_DONUT_2,trigger=TRIGGER_INSTANT,type=TYPE_INDIRECT_DAMAGE,emoji='<:liaSamLB2:1100185041306386439>')
Hauringusutōmusōdo1_eff2 = effect("Uindogādo","Hauringusutōmusōdo1_eff2",dodge=20,block=20,counterOnBlock=20,counterOnDodge=20,emoji='<:liaSki6:1013891089662488596>')
Hauringusutomusodo_1 = skill("Hauringusutōmusōdo",getAutoId(eternalLight.id,True),TYPE_DAMAGE,power=120,cooldown=6,garCrit=True,effects=[Hauringusutōmusōdo1_eff1],effectOnSelf=Hauringusutōmusōdo1_eff2,range=AREA_CIRCLE_3,tpBehind=True,emoji='<:liaCounter:998001563379437568>',url=demolish.url,description="Après un tour de chargement, vous téléporte derrière l'ennemi ciblé, lui inflige une attaque forcément critique ({0}), inflige des dégâts indirects aux ennemis proches ({1}) et augmente vos chances d'esquive, de parade et de contre-attaque durant un brief moment".format(statsEmojis[STRENGTH],statsEmojis[Hauringusutōmusōdo1_eff1.stat]),ultimate=True,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR])
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
bloodButterFlyPassifEff = effect("Volontée gravée dans le sang","bloodbutterflypass",power=25,turnInit=-1,unclearable=True,description="Vous octroi **{power}%** de chance d'infliger l'effet <:bloodButterfly:1090171812782034954> __Papillon Sanguin__ à la cible principale de vos compétences",emoji='<:clemHeritage:1090171016841547846>',callOnTrigger=bloodButterfly)
inMemoria = skill("In Memoria",getAutoId(ikishoten.id,True),TYPE_RESURECTION,power=200,emoji='<:inMemoria:1119958588362866789>',use=INTELLIGENCE,area=AREA_ALL_ALLIES,range=AREA_MONO,cooldown=7,description="Réanime tous les alliés vaincus. Si un allié ne peut être réanimé, invoque un {0} {1} à la place\n\n{0} __{1}__ :\nReprésente l'esprit d'un défunt. Possède {2}% des statistiques ainsi que les mêmes compétences de l'entité qu'il représente. Translucide, Inciblable et Invulnérable\nLes PNJ du groupe Mort-Vivant ne peuvent pas créer de Memoria\n\nSi {3} Anna est présente dans la même équipe que le lanceur, cette compétence invoque à minima une Memoria".format("<:ghostB:1119951487032901722>","Memoria",50,"<:anna:943444730430246933>"))
komoriHerit = skill("Savoir Vampirique",getAutoId(inMemoria.id,True),TYPE_PASSIVE,effectOnSelf=bloodButterFlyPassifEff,emoji=bloodButterFlyPassifEff.emoji[0][0],description=bloodButterFlyPassifEff.description,quickDesc="Vous octroi une chance de réduite les soins des ennemis ciblés")

dualCastEff = effect("Double Sort","dualCastEff",MAGIE,power=80,area=AREA_CIRCLE_1,lvl=4,turnInit=4,description="Lors de vos 3 prochains tours, inflige une attaque directe magique en zone autour de l'ennemi ciblé par vos compétences offensives",emoji='<:dualCast:1121436199429623888>')
dualCastEff1 = effect("Bonus de Magie","dualCastEff2",PURCENTAGE,magie=15,turnInit=dualCastEff.turnInit,description="Augmente la magie")
dualCast = skill("Double Sort",getAutoId(komoriHerit.id,True),TYPE_BOOST,effects=[dualCastEff,dualCastEff1],emoji=dualCastEff.emoji[0][0],description=dualCastEff.description+", augmente votre magie et vous permet de rejouer votre tour",cooldown=7,range=AREA_MONO)
renforPhysEff = effect("Renforcement Physique","dualCastEff",STRENGTH,power=80,area=AREA_CIRCLE_1,lvl=4,turnInit=4,description="Lors de vos 3 prochains tours, inflige une attaque directe magique en zone autour de l'ennemi ciblé par vos compétences offensives",emoji='<:darkRenf:1120974892188315740>')
renforPhysEff1 = effect("Bonus de Force","dualCastEff2",PURCENTAGE,magie=15,turnInit=dualCastEff.turnInit,description="Augmente la force")
renforPhys = skill("Renforcement Physique",getAutoId(dualCast.id,True),TYPE_BOOST,effects=[renforPhysEff,renforPhysEff1],emoji=renforPhysEff.emoji[0][0],description=renforPhysEff.description+", augmente votre force et vous permet de rejouer votre tour",cooldown=7,range=AREA_MONO)
highVibration = effect("Haute Fréquence Vibratoire","highVibr",INTELLIGENCE,strength=2,magie=2,charisma=2,intelligence=2,turnInit=5,emoji='<:hfv:1124333624930615326>')
harmQuant = copy.deepcopy(absEff)
harmQuant.power, harmQuant.turnInit = 5, highVibration.turnInit
protect5g = effect("Harmonie Quantique Anti-5G","harmQuant",INTELLIGENCE,inkResistance=4,turnInit=highVibration.turnInit)
increaseVibrations = skill("Augmentation des fréquences vibratoires",getAutoId(renforPhys.id,True),TYPE_BOOST,500,effects=[highVibration,harmQuant,protect5g],cooldown=7,range=AREA_MONO,area=AREA_CIRCLE_2,description="Augmente vos fréquences vibratoires et celles de vos alliés proches pendant un moment",emoji=highVibration.emoji[0][0])
lycantStrike_1 = skill("Furie Lycantropique",getAutoId(increaseVibrations.id,True),TYPE_DAMAGE,750,power=225,garCrit=True,ultimate=True,tpCac=True,cooldown=destruction.cooldown,emoji='<:griffe:884889931359596664>',url="https://cdn.discordapp.com/attachments/927195778517184534/932774912391782490/20220118_001411.gif",effectOnSelf=destruction.effectOnSelf,description="Après un tour de chargement, inflige une puissante attaque forcément critique à l'ennemi ciblé et vous empêche d'utiliser une compétence lors de votre prochain tour")
lycantStrike_c = effect("Cast - {replicaName}","lycantStrike_c",turnInit=2,silent=True,replique=lycantStrike_1)
lycantStrike = skill(lycantStrike_1.name,lycantStrike_1.id,lycantStrike_1.type,lycantStrike_1.price,0,lycantStrike_1.range,ultimate=True,cooldown=lycantStrike_1.cooldown,effectOnSelf=lycantStrike_c,emoji=lycantStrike_1.emoji)
skySharter_1 = skill("Comdamnation Explosive",getAutoId(lycantStrike.id,True),TYPE_DAMAGE,power=explosion.power*0.35,price=750,repetition=3,area=AREA_CIRCLE_2,effectOnSelf=explosion.effectOnSelf,percing=explosion.percing,damageOnArmor=explosion.onArmor,ultimate=True,cooldown=explosion.cooldown)
skySharter_c = effect("Cast - {replicaName}","skySharter_c",replique=skySharter_1,turnInit=2,silent=True)
skySharter = copy.deepcopy(skySharter_1)
skySharter.power, skySharter.effectOnSelf = 0, skySharter_c
tox2Eff = copy.deepcopy(vulne)
tox2Eff.power, tox2Eff.stat, tox2Eff.turnInit = 2, STRENGTH, lanceToxEff.turnInit
lanceTox2 = skill("Lance-Toxines Modifié",getAutoId(skySharter.id,True),TYPE_INDIRECT_DAMAGE,500,area=lanceTox.area,range=lanceTox.range,effects=[lanceToxEff,tox2Eff],emoji='<:toxines2:1124752297084334181>',cooldown=7,description="Inflige un effet de dégâts périodiques et augmente les dégâts reçus des ennemis ciblés durant un moment")
tox3Eff = copy.deepcopy(dmgDown)
tox3Eff.power, tox3Eff.stat, tox3Eff.turnInit = tox2Eff.power, STRENGTH, lanceToxEff.turnInit
lanceTox3 = skill("Lance-Toxines Griffé",getAutoId(lanceTox2.id,True),TYPE_INDIRECT_DAMAGE,500,area=lanceTox.area,range=lanceTox.range,effects=[lanceToxEff,tox3Eff],emoji='<:toxines3:1124752329707634759>',cooldown=7,description="Inflige un effet de dégâts périodiques et réduit les dégâts infligés des ennemis ciblés durant un moment")
liberationEff = effect("Libération","libEff",MAGIE,power=75,area=AREA_CIRCLE_1,trigger=TRIGGER_INSTANT,type=TYPE_INDIRECT_DAMAGE,emoji='<:liberation:1124759822143860808>',callOnTrigger=estal2)
fairyLiberation = skill("Libération",getAutoId(lanceTox3.id,True),TYPE_INDIRECT_DAMAGE,area=AREA_CIRCLE_2,cooldown=7,effects=liberationEff,emoji=liberationEff.emoji[0][0],description="Pour chaque ennemi ciblé, inflige des dégâts indirects de zone avec une puissance équivalante à **{0}%** de la puissance totale des effets {1} __{2}__ présent sur la cible. Si la puissance est supérieure à **10**, inflige également {3} __{4}__ aux ennemis autours".format(liberationEff.power,estial.emoji[0][0],estial.name,estal2.emoji[0][0],estal2.name))
exploPetal1 = effect("Explosion Florale I","exploPetal1",CHARISMA,strength=2,magie=2,emoji='<:crois1:903976740869795910>')
exploPetal2 = effect("Explosion Florale I (Effet)","exploPetal2",CHARISMA,strength=1,magie=1,turnInit=3,callOnTrigger=exploPetal1,area=AREA_CIRCLE_2,trigger=TRIGGER_ON_REMOVE,emoji='<:eclosion:1124764616476602538>')
exploPetal3 = effect("Explosion Florale II","exploPetal3",CHARISMA,strength=5,magie=5,emoji='<:crois2:903976762726289520>')
exploPetal4 = effect("Explosion Florale II (Effet)","exploPetal4",CHARISMA,strength=2,magie=2,turnInit=2,callOnTrigger=exploPetal3,area=AREA_CIRCLE_2,trigger=TRIGGER_ON_REMOVE,emoji='<:eclosion:1124764616476602538>')
exploPetal5 = effect("Explosion Florale III","exploPetal5",CHARISMA,strength=10,magie=10,emoji='<:crois2:903976762726289520>')
exploPetal6 = effect("Explosion Florale III (Effet)","exploPetal6",CHARISMA,strength=3,magie=3,callOnTrigger=exploPetal5,area=AREA_CIRCLE_2,trigger=TRIGGER_INSTANT,emoji='<:eclosion:1124764616476602538>')
exploPetal = skill("Explosion Florale",getAutoId(fairyLiberation.id,True),TYPE_BOOST,effects=[exploPetal6,exploPetal4,exploPetal2],cooldown=7,emoji='<:eclosion:1124764616476602538>',description="Augmente les statistiques des alliés ciblés. Un effet moins puissant est octroyé aux alliés autours durant 2 tours")
infuEthereff = effect("Infusion d'Ether","infuEther",PURCENTAGE,strength=25,magie=25,charisma=25,intelligence=25,agility=25,precision=25,endurance=25)
infuEthereff1 = effect("Infusion d'Ether","infuEther2",PURCENTAGE,magie=10,turnInit=3)
infuEther = skill("Infusion d'Ether",getAutoId(exploPetal.id,True),TYPE_BOOST,500,cooldown=5,range=AREA_MONO,emoji='<:infusion:1123148866548662363>',area=AREA_SUMMON,effects=[infuEthereff,galvaniseEff],effectOnSelf=infuEthereff1,description="Augmente de **{0}%** les statistiques de vos invocations et de **{1}** tour leur durée de vie. Accroie également votre magie de **{2}%** durant un petit moment".format(infuEthereff.strength,galvaniseEff.power,infuEthereff1.magie))
gemmes = skill("Resplandiment des gemmes",getAutoId(infuEther.id,True),TYPE_DAMAGE,500,80,use=MAGIE,cooldown=5,emoji='<:gemmes:1123148907040473159>',description="Inflige une attaque à l'ennemi ciblé. De plus, chaque Carbuncle Allié inflige une attaque supplémentaire, la puissance et la zone d'effet variant suivant le type de Carbuncle")
selfMemoria = skill("Echo de l'Âme",getAutoId(gemmes.id,True),TYPE_SUMMON,cooldown=7,invocation="Memoria",description="Invoque un Mémoria de vous-même",emoji='<:selfMemoria:1129044261237686483>')
selfMemoria.iaPow = 150
squidRollArmor = effect("Armure","squidRollArmor",PURCENTAGE,overhealth=10,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
squidRollEff = effect("Vrille Calamar","squidRoll",power=20,turnInit=-1,unclearable=True,emoji='<:squidRoll:1129785893851508746>',callOnTrigger=squidRollArmor,description="Octroi une amure équivalente à **{0}%** de vos PV Maximum lors d'une esquive (20%) ou lors d'une téléportation au corps à corps réussie".format(squidRollArmor.overhealth))
squidRoll = skill("Vrille Calamar",getAutoId(selfMemoria.id,True),TYPE_PASSIVE,use=AGILITY,effectOnSelf=squidRollEff,description=squidRollEff.description,emoji=squidRollEff.emoji[0][0])

etherJauge = effect("Jauge d'Ether","jaugedether",turnInit=-1,unclearable=True,emoji='<:etherJauge:1130206278447272088>',jaugeValue=jaugeValue(
    emoji=[["<:ejEL:1130205658579468449>","<:ejEM:1130205689877373008>","<:ejER:1130205728112660691>"],["<:ejFL:1130205480061509762>","<:ejFM:1130205507601322024>","<:ejFR:1130205545110982749>"]],
    conds=[
        jaugeConds(INC_START_TURN,10),
        jaugeConds(INC_USE_SKILL,30,[infuEther])
    ]
))

energyDrain = skill("Aspiration d'énergie",getAutoId(squidRoll.id,True),TYPE_DAMAGE,power=60,replay=True,use=MAGIE,emoji='<:energyDrain:1130205922929684490>',lifeSteal=35,description="Inflige des dégâts à l'ennemi ciblé en absorbant une partie des dégats infligés, remplie votre {0} {1} de {2} points et vous permet de rejouer votre tour".format(etherJauge.emoji[0][0],etherJauge.name,etherJauge.jaugeValue.conds[1].value),cooldown=3)
energySiphon = skill("Syphon d'énergie",energyDrain.id,TYPE_DAMAGE,power=45,replay=True,area=AREA_CIRCLE_1,use=MAGIE,emoji='<:syphon:1130205955846590505>',lifeSteal=20,description="Inflige des dégâts aux ennemis ciblés en absorbant une partie des dégats infligés, remplie votre {0} {1} de {2} points et vous permet de rejouer votre tour".format(etherJauge.emoji[0][0],etherJauge.name,etherJauge.jaugeValue.conds[1].value),cooldown=3)
dualEnergyDrain = skill("Syphonage d'éther",energyDrain.id,TYPE_DAMAGE,become=[energyDrain,energySiphon],price=500,use=MAGIE,emoji=energyDrain.emoji,description="Vous permet d'utiliser {0} {1} et {2} {3}, deux compétences infligeant des dégâts, vous en soigne d'une partie, augmente de {4} {5} et vous permettent de rejouer votre tour".format(energyDrain.emoji,energyDrain.name,energySiphon.emoji,energySiphon.name,etherJauge.emoji[0][0],etherJauge.name))
etherJauge.jaugeValue.conds[1].add.append(energyDrain)
etherJauge.jaugeValue.conds[1].add.append(energySiphon)

suppuration = skill("Suppuration",getAutoId(dualEnergyDrain.id,True),TYPE_DAMAGE,power=85,maxPower=100,replay=True,use=MAGIE,emoji='<:fester:1130205891086524557>',minJaugeValue=30,maxJaugeValue=50,jaugeEff=etherJauge,description="Inflige des dégâts à l'ennemi ciblé en consommant un peu de votre {0} {1} et vous permet de rejouer votre tour".format(etherJauge.emoji[0][0],etherJauge.name))
magicFlare = skill("Brasier de Peine",suppuration.id,TYPE_DAMAGE,power=60,maxPower=85,area=AREA_CIRCLE_1,replay=True,use=MAGIE,emoji='<:flare:1130205986959917127>',minJaugeValue=30,maxJaugeValue=50,jaugeEff=etherJauge,description="Inflige des dégâts aux ennemis ciblés en consommant un peu de votre {0} {1} et vous permet de rejouer votre tour".format(etherJauge.emoji[0][0],etherJauge.name))
dualSupp = skill("Suppuration éthérique",magicFlare.id,TYPE_DAMAGE,become=[suppuration,magicFlare],use=MAGIE,price=500,emoji=suppuration.emoji,description="Vous permet d'utiliser {0} {1} et {2} {3}, deux compétences infligeant des dégâts en consommant un peu de votre {4} {5} et vous permettent de rejouer votre tour".format(energyDrain.emoji,energyDrain.name,energySiphon.emoji,energySiphon.name,etherJauge.emoji[0][0],etherJauge.name),jaugeEff=etherJauge)

# Skill
skills: List[skill] = [dualSupp,dualEnergyDrain,squidRoll,selfMemoria,gemmes,infuEther,exploPetal,fairyLiberation,lanceTox2,lanceTox3,skySharter,lycantStrike,increaseVibrations,renforPhys,dualCast,komoriHerit,inMemoria,ikishoten,hissatsu,Hauringusutomusodo,eternalLight,lenaDrone1,analysedShot,bento,snowFall,higanbana,brotherHood,meditate,bundleRixeEva,phenixSpirit,dvinRegen,dvinRegen2,divinVeal,sustain,curl,stimulate,hexadecaComb,altyStrike,altyPenta,pandaiStrike,gwenCharge,gwenPenta,kStrike,gravPulse,guardianAngel,pentastrike,moonLight,bloodMoon,blueMoon,newMoon,fullMoon,ripping,weakPoint,justiceEnigma,holyVoice,plongeFracas,revolutionFracas,fracas,synastie,purify2,nonVitaUnionis,sinisterLux,flammaSinister,decomposition ,putrefaction,lifeLight,lifeFlame,moramMortem,moramMortem2,infDraw,funDraw,seitonTenchu,echecEtMat,deathPercing,healingSacrifice,summonHinoro,comboHeatedCleanShot,leadShot,dismantle,megaVent,gigaChad,soulWave,soulTwin,soulSceal,magma,orage,bastion,corruptusArea,tripleChoc,florChaot,astraRegenEarth,astraIncurStrike,astraRegenPhase,bunshin,dreamInADream,intervantion,intuitionFoug,redrum,anticipation,rubyLight,dislocation,tacShield,phalax,phenixDance,bloodDemonBundle,umbraMortis,deterStrike,thunderFiole,sernade,vibrSon,dissonance,stigmate,exploShot,heroicFantasy,mageBalad,martialPean,vanderManuet,manafication,enhardissement,blastArrow,apexArrow,dmonReconstitution,dmonReconstitution2,dmonDmg,dmonCrit,dmonEnd,dmonAgi,piedVolt,elipseTerrestre,clock,hourglass,ebranlement,hearthFrac,freezeArrow2,freezeArrow,exploArrow,immoArrow,spectralFurie,spectralCircle,ghostlyCircle,silvArmor,UmbralTravel,carnage,assasinate,physTraqnard,fairyTraqnard,blodTraqnard,lifeSeed,antConst,constBen,mend,lillyTransform,forestGarde,ultraSignal,expoHeal,intox,epidemic,sacredSoil,inkStrike,trizooka,inkzooka,tacticooler,lacerTrap,lohicaBrouillad,bigBubbler,asile,sonarPaf,convictionVigilante,convicPro,convictTet,convictEncht,megaDark1,megaDark2,megaDark3,gigaDark1,gigaDark2,gigaDark3,megaLight1,megaLight2,megaLight3,gigaLight1,gigaLight2,gigaLight3,miracle,rivCel,toxicon,seraphStrike,
    bundleFetu,soulPendant,corruptBecon,moissoneur,bundleLemure,lowBlow,legStrike,provoke,comboFanCelest,demonLand,demonArmor,demonArmor2,demonConst,
    comboConfiteor,cryoChargeBundle,pyroChargeBundle,drill,anchor,chainsaw,mysticShot,cycloneEcarlate,sillage,cassMont,finalClassique,offrRec,offrRav,lightEstoc,lightTranche,lightShot,lightPulse,accelerant,tripleAttaque,liberation,acidRain,coroRocket,coroMissile,coroShot,quadFleau,charmingPandant,kralamSkill,windDance,barrage,hemoBomb,dmonProtect,raisingPheonix,fairyGarde,sumLightButterfly,fairySlash,plumRem,fairyBomb,bloodBath,erodAoe,divineAbne,astrodyn,cercleCon,aliceFanDanse,plumeCel,plumePers,pousAviaire,demonRegen,demonLink,bloodBath2,altyCover,klikliStrike,gwenyStrike,mve2,krasis,pandaima,graviton,temperance,terachole,aquavoile,misery,tangoEnd,danseStarFall,graviton2,invocAutTour,invocAutFou,invocAutQueen,recall,divineBenediction,divineCircle,divineGuid,uberCharge,petalisation,roseeHeal,floraisonFinale,vampirisme2,krystalisation,regenVigil,fragmentation,machDeFer,lanceTox,trickAttack,aurore2,holyShieltron,kerachole,gigaFoudre,morsTempSkill,combustion,morsCaudiqueSkill,lbRdmCast,lightEarth,darkAmb,solarEruption,firstArmor,refLum,refConc,dephaIncant,cwFocus,propaUlt,cwUlt,sanguisGladio,sanguisGladio2,cardiChoc,equatorial,elemShield,shieldAura,horoscope,ShiUltimate,intaveneuse,decolation,corGraCast,finalFloral,divineSave,redemption,fireElemUse,waterElemUse,airElemUse,earthElemUse,lightElemUse,darkElemUse,spaceElemUse,timeElemUse,bleedingConvert,revelation,maitriseElementaire,magicEffGiver,physEffGiver,danceFas,selenomancie,holiomancie,partner,exhibitionnisme,invocTitania,dmonBlood,hollyGround,hollyGround2,burningGround,blueShell,preciChi,ironHealth,windBal,brasier2,earthUlt2,geyser,rouletteSkill,constance,constance2,undead,ironStormBundle,bolide,invincible,holmgang,comboVerBrasier,galvanisation,contreDeSixte,lifeWind,ice2,renf2,entraide,perfectShot,lastRessource,strengthOfDesepearance,nova,deathShadow,comboVerMiracle,comboFaucheCroix,theEndCast,cure2Bundle,assises,debouses,impact,heartStone,erodStrike,genesis,invertion,pneuma,absorbingStrike,absorbingArrow,absorbingStrike2,absorbingArrow2,magiaHeal,aff2,bloodPact,expediant,divination,macroCosmos,tintabule,bundleCaC,engage,autoBombRush,killerWailUltimate,invocSeaker,darkBoomCast,mageSkill,doubleShot,harmShot,benitWater,shareSkill,extraMedica,foullee,lifePulseCast,crimsomLotusCast,abnegation,foyer,sweetHeat,darkSweetHeat,shell,nacreHit,holyShot,demonStrike,purify,benediction,transfert,blackDarkMagic,fisure,seisme,abime,extermination,darkHeal,calestJump,lohicaUltCast,fairyFligth,aliceDance,aurore,crep,quickCast,pepsis,darkShield,rencCel,valse,finalTech,dissi,intelRaise,ultRedirect,clemency,liuSkillSus,liaSkillSus,lioSkillSus,lizSKillSus,neutralMono1,neutralZone1,neutralMono2,neutralZone2,neutralMono3,neutralZone3,reconst,medicamentum,ultMonoArmor,inkRes,inkRes2,booyahBombCast,propag,invocCarbSaphir,invocCarbObsi,supprZone,cosmicPower,requiem,magicRuneStrike,infinitDark,preciseShot,troublon,haimaSkill,physicRune,magicRune,lightBigHealArea,focus,poisonusPuit,bleedingPuit,idoOS,proOS,preOS,geoConCast,kikuRes,memClemCastSkill,roses,krysUlt,chaosArmor,firelame,airlame,waterlame,mudlame,shadowLame,timeLame,lightLame,astralLame,idoOH,proOH,altOH,lightAura2,tripleMissiles,lightHeal2,extraEtingSkill,strengthOfWillCast,sixtineUlt,hinaUlt,julieUlt,invocSeraf,mageUlt,soulagement,bloodyStrike,infraMedica,magAchSkill,flambeSkill,fireCircle,waterCircle,airCircle,earthCircle,fireShot,waterShot,airStrike,earthStrike,space1,space2,space3,spaceSp,time1,time2,time3,timeSp,renisurection,demolish,contrainte,trouble,infirm,croissance,destruction2,infectFiole,bigLaser2,bigMonoLaser2,invocBat2,invocCarbunR,concen,memAlice2,blackHole,blackHole2,renforce,steroide,focal,suppr,revitalisation,onde,eting,stingray,dark1,dark2,dark3,light1,light2,light3,derobade,ferocite,ironWillSkill,royaleGardeSkill,defi,dissimulation,bleedingTrap,convert,vampirisme,heriteEstialba,heriteLesath,flameche,flame,pyro,ecume,courant,torant,brise,storm2,tornado,stone,rock,mont,bleedingArrow,bleedingDague,swordDance,shot,percingArrow,percingLance,highkick,multishot,rocklance,infinitFire,storm,innerdarkness,divineLight,icelance,onstage,kiss,secondSun,oneforall,uppercut,stalactic,linx,bombRobot,isolement,secondWind,blindage,adrenaline,lapSkill,burst,descart,thinkSkill,invocFee,invocCarbT,invocCarbE,splashdown,multiMissiles,monoMissiles,invocBat,poisonus,protect,explosionCast,splatbomb,lightAura,cure,balayette,contrecoup,boom,chaos,unHolly,soupledown,inkarmor,coffeeSkill,theSkill,gpotion,bpotion,zelian,courage,nostalgia,draw25,siropMenthe
] + elemArrowSkill + elemRuneSkill + horoSkills + tablAdvBaseElemSkills + baseSkills

if not(isLenapy):
    skills.append(bestSkill)

importantSkills = [deathShadow.id, umbraMortis.id, soulSceal.id]
useElemEffId = [fireElemUse.id,waterElemUse.id,airElemUse.id,earthElemUse.id,lightElemUse.id,darkElemUse.id,spaceElemUse.id,timeElemUse.id]
finFloOtherSkillsId = [valse.id, finalTech.id,roseeHeal.id,croissance.id]
tablRosesEff,tablRosesSkillsId,tablRosesId = [roseRed,roseDarkBlu,rosePink,roseYellow,roseBlue,roseGreen], [aliceDanceFinal.id,corGraFinal.id,onstage.id,crimsomLotus.id,floraisonFinale.id,petalisation.id,danceFas.id],[roseRed.id,roseDarkBlu.id,rosePink.id,roseYellow.id,roseBlue.id,roseGreen.id]

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
    [effect("Verseau","horVerseau",turnInit=-1,emoji='<:verseau:960319751136108546>',silent=True),[[INTELLIGENCE,3,PRECISION,2]]],
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
lb2ArmorEff = effect("Proctection de Nacialisla",'lb2Armor',HARMONIE,overhealth=int(effTransPre.overhealth*0.7),turnInit=2,emoji=effTransPre.emoji)
lb2Armor = skill("Protection de Nacialisla","lb",TYPE_ARMOR,effects=lb2ArmorEff,area=transPre.area,range=AREA_MONO,emoji=trans.emoji,description="Octroi une armure aux alliés à portée\n__Puissance de l'armure :__ {0}".format(lb2ArmorEff.overhealth),url='https://media.discordapp.net/attachments/971787705216274495/988822434016792596/20220621_165940.gif')
lb1Mono = skill("Ardeur courageuse","lb",TYPE_DAMAGE,power=int(transBerserk.power*0.4),accuracy=200,range=transBerserk.range,emoji=trans.emoji,use=HARMONIE,description="Inflige des dégâts harmoniques à l'ennemi ciblé\n__Puissance :__ {power}",url='https://media.discordapp.net/attachments/971787705216274495/988822435098947604/20220621_165401.gif')
lb1Line = skill("Gros calibre","lb",TYPE_DAMAGE,power=int(transObs.power*0.4),accuracy=200,range=transObs.range,area=transObs.area,emoji=trans.emoji,use=HARMONIE,description="Inflige des dégâts harmoniques aux ennemis dans une zone linéaire\n__Puissance :__ {power}",url='https://media.discordapp.net/attachments/971787705216274495/988822436982190130/20220621_164657.gif')
lb1AoE = skill("Décharge Stellaire","lb",TYPE_DAMAGE,power=int(transEnch.power*0.4),accuracy=200,range=transMage.range,area=AREA_CIRCLE_1,emoji=trans.emoji,use=HARMONIE,description="Inflige des dégâts harmoniques aux ennemis dans la zone d'effet\n__Puissance :__ {power}",url='https://media.discordapp.net/attachments/971787705216274495/988822435753250916/20220621_165155.gif')
lb1Heal = skill("Souffle de la Terre","lb",TYPE_HEAL,power=int(transAlt.power*0.4),range=transAlt.range,area=transAlt.area,emoji=trans.emoji,use=HARMONIE,description="Soigne les alliés dans la zone d'effet\n__Puissance :__ {power}",url="https://media.discordapp.net/attachments/971787705216274495/988822436315279360/20220621_164949.gif")
lb1ArmorEff = effect("Proctection de la Terre",'lb1Armor',HARMONIE,overhealth=int(effTransPre.overhealth*0.4),turnInit=1,emoji=effTransPre.emoji)
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
lb4 = skill("Conviction de Silicia","lb",TYPE_DAMAGE,power=int(transBerserk.power*1.5),accuracy=200,emoji=trans.emoji,description="Inflige de lourd dégâts à un ennemi ciblé et réanime les alliés vaincus autour de vous\n__Puissance :__ {power}",use=HARMONIE,effectAroundCaster=[TYPE_RESURECTION,AREA_ALL_ALLIES,350],url='https://media.discordapp.net/attachments/989526512288030742/991051124746387506/20220627_204219.gif')

# SkillsCat

skillsCat = list(range(TYPE_DEPL+1))
for cmpt in range(len(skillsCat)):
    skillsCat[cmpt] = list(range(MASCOTTE+ELEMENT_TIME+3))
    for cmpt2 in range(len(skillsCat[cmpt])):
        skillsCat[cmpt][cmpt2] = []

# FindSkill
dictTablSkills, dictSkills = {}, {}

for skilly in skills:
    try:
        dictTablSkills[skilly.id[:2]].append(skilly)
    except KeyError:
        dictTablSkills[skilly.id[:2]] = [skilly]

    if skilly.condition == []:
        skillsCat[skilly.type][0].append(skilly)
    elif skilly.condition[1] == ASPIRATION:
        skillsCat[skilly.type][1+skilly.condition[2]].append(skilly)
    elif skilly.condition[1] == ELEMENT:
        skillsCat[skilly.type][1+skilly.condition[2]+MASCOTTE+1].append(skilly)

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

suppIndDamageEffId = [casseMontEff,bunshinEff,cruentumOffendasEff]
for eff in suppIndDamageEffId:
    copyTabl, eff.description = suppIndDamageEffId[:], eff.description + "\n\nSi cet effet est cumulé avec "
    copyTabl.remove(eff)
    for effName in copyTabl:
        eff.description += "{0} {1}".format(effName.emoji[0][0],effName.name)
        if len(copyTabl) > 1 and effName != copyTabl[-1]:
            eff.description += ", "
    eff.description += " ou lui-même, seul l'effet le plus ancien est déclanché"

for cmpt in range(len(suppIndDamageEffId)):
    suppIndDamageEffId[cmpt] = suppIndDamageEffId[cmpt].id

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
