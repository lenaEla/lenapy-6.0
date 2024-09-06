from classes import *
from advObjects.advWeapons import *
from advObjects.advSkills import *
from advObjects.advStuffs import *
from advObjects.advSummons import *
from advObjects.advEffects import *
from advObjects.advEnnemies import *
from advObjects.advAllies import *
from typing import Union
import copy

poidPlumeEff = effect("Poids Plume","poidCritEff",None,trigger=TRIGGER_END_OF_TURN,silent=True,lvl=0,type=TYPE_UNIQUE,unclearable=True,turnInit=-1,emoji=uniqueEmoji(aspiEmoji[POIDS_PLUME]))
obsEff = effect("Observateur","obsCritEff",None,silent=True,lvl=0,type=TYPE_UNIQUE,unclearable=True,turnInit=-1,emoji=uniqueEmoji(aspiEmoji[OBSERVATEUR]))

#Other
changeAspi = other("Changement d'aspiration","qa",description="Vous permet de changer d'aspiration",emoji='<:changeaspi:868831004545138718>')
changeAppa = other("Changement d'apparence","qb",description="Vous permet de changeer votre genre, couleur et espèce",emoji='<:changeAppa:872174182773977108>',price=500)
changeName = other("Changement de nom","qc",description="Vous permet de changer le nom de votre personnage",emoji='<:changeName:872174155485810718>',price=500)
restat = other("Rénitialisation des points bonus","qd",description="Vous permet de redistribuer vos points bonus",emoji='<:restats:872174136913461348>',price=500)
elementalCristal = other("Cristal élémentaire","qe",500,description="Ces cristaux vous permettent de changer l'élément de votre personnage dans /inventory element (lvl 10)\n\nCe cristal permet de sélectionner les éléments suivants :\n<:fire:887847475203932261> Feu\n<:water:887847459211079760> Eau\n<:air:887847440932290560> Air\n<:earth:887847425459503114> Terre",emoji="<:krysTal:888070310472073257>")
customColor = other("Couleur personnalisée","qf",500,description="Vous permet de rentrer une couleur personnalisée pour votre personnage",emoji='<:changeColor:892350738322300958>')
seeshell = other("Super Coquillage","None",500,description="Ce coquillage permet de changer son bonus iné dans /inventory bonus (lvl 25)")
blablator = other("Blablator","qg",500,description="Permet de définir des messages que votre personnages dira lors de certains événements",emoji='<:blablator:918073481562816532>')
dimentioCristal = other("Cristal dimentionel",'qh',500,'<:krysTal2:907638077307097088>',"Ces cristaux vous permettent de changer l'élément de votre personnage dans /inventory element (lvl 20)\n\nCe cristal permet de choisir les éléments suivants :\n<:light:887847410141921362> Lumière\n<:darkness:887847395067568128> Ténèbre\n<:astral:907467653147410475> Astral\n<:temporel:907467620930973707> Temporel")
token = other("Jeton de roulette","None",0,'<:jeton:917793426949435402>',"Ce jeton est à utiliser dans la Roulette\nAllez donc faire un tour à /roulette !")
mimique = other("Mimikator","qi",500,"<:mimikator:918073466077446164>","Cet emoji vous permet de changer l'apparance de votre arme ou accessoire sur votre icone de personnage.\n\nPour ce faire, appuyez juste sur le bouton correspondant lorsque vous ouvrez une page d'information d'une arme ou accessoire avec /inventory")
ilianaGrelot = other("Grelot","qj",350,'<:iliGrelot:930385123130609684>',"Vous permet de changer la forme de votre icone de personnage en Inkling Chat ou Octaling Chat")
grandNouveau = other("Boucles d'oreilles originelle","qk",350,amethystEarRings.emoji,"Vous permet de rénitialiser la forme de votre icone de personnage")
aliceBatEarRing = other("Amulette chauve-souris","ql",350,invocBat.emoji,"Vous permet de changer la forme de votre icone de personnage en Chauve-Souris")
birdup = other("Pigeon de compagnie","qm",350,'<:birdUp:930906195999473684>',"Vous permet de changer la forme de votre icone de personnage en Aviaire")
Megalovania = other("Musique qui rentre dans la tête","qn",350,'<:lazyBones:930949502133747762>',"Vous permet de changer la forme de votre icone de personnage en Crâne")
amary = other("Amaryllis",'qo',350,'<:amaryllis:935337538426642483>','Vous permet de changer la forme de votre icone en icone Féérique')
autoPoint = other("Pai'rte de Nheur'o'Nes",'qp',3500,emoji='<:autPoint:1041625800581066752>',description="Une fois cette object activé, chaque point bonus obtenus en montant de niveau est automatiquement attribué selon les statistiques recommandés pour votre aspiration\n\nNécessite d'être au moins niveau 1<:littleStar:925860806602682369>1")
autoStuff = other("Garde-robe de la Fée Niante",'qq',3500,emoji='<:autStuff:1041625746340323330>',description="Une fois cette object activé, à chaque fois que vous atteigné un pallié de niveau, modifie automatiquement votre équipement selon les statistiques recommandés pour votre aspiration\n\nNécessite d'être au moins niveau 1<:littleStar:925860806602682369>1")
dailyCardBooster1 = other("Booster journalié supplémentaire 1",getAutoId("qq"),0,"<:littleStar:925860806602682369>","Augmente le nombre de boosters de puce obtenus lors de votre premier combat du jour de 1")
dailyCardBooster2 = other("Booster journalié supplémentaire 2",getAutoId(dailyCardBooster1),0,"<:lS:925860806602682369>","Augmente le nombre de boosters de puce obtenus lors de votre premier combat du jour de 1")
tripleCommunCards = other("Booster de puces commun x3",getAutoId(dailyCardBooster2),0,rarityEmojis[0],"Vous octroie trois booster de puces commun")
singleRareCards = other("Booster de puces rare",getAutoId(tripleCommunCards),0,rarityEmojis[1],"Vous octroie un booster de puces rare")
others = [tripleCommunCards,singleRareCards,dailyCardBooster1,dailyCardBooster2,elementalCristal,customColor,changeAspi,changeAppa,changeName,restat,blablator,dimentioCristal,mimique,ilianaGrelot,grandNouveau,aliceBatEarRing,birdup,Megalovania,amary,autoPoint,autoStuff]

previewDict = {
    ilianaGrelot.id:'https://cdn.discordapp.com/emojis/930806243461857301.png',
    grandNouveau.id:'https://cdn.discordapp.com/emojis/930807241064480828.png',
    aliceBatEarRing.id:'https://cdn.discordapp.com/emojis/930807423483129876.png',
    birdup.id:'https://cdn.discordapp.com/emojis/930908758773743616.png',
    Megalovania.id:'https://cdn.discordapp.com/emojis/930911733307027536.png',
    amary.id:'https://cdn.discordapp.com/emojis/935340408723112047.png'
}

changeIconForm = [grandNouveau,ilianaGrelot,aliceBatEarRing,birdup,Megalovania,amary]

smnAnaisEff.callOnTrigger=anais

# Specials skills ================================================================================
# Total Kboum
totalAnnilLauch = copy.deepcopy(explosion)
totalAnnilLauch.power = 500

totalAnnilCastEff = effect("Cast - {replicaName}","totalBoomCast",turnInit=2,silent=True,replique=totalAnnilLauch)
totalAnnilCast = copy.deepcopy(totalAnnilLauch)
totalAnnilCast.power, totalAnnilCast.effectOnSelf = 0, totalAnnilCastEff

BOUMBOUMBOUMBOUMweap = weapon("BoumWeap","BoumWeap",1,AREA_CIRCLE_1,0,0,0,priority=WEAPON_PRIORITY_NONE)
fairyBomb.effects[0].callOnTrigger = copy.deepcopy(findEffect(estial.id))
fairyBomb.effects[0].callOnTrigger.power = int(fairyBomb.effects[0].callOnTrigger.power*0.4)

hemoBomb.effects[0].callOnTrigger = copy.deepcopy(findEffect(bleeding.id))
hemoBomb.effects[0].callOnTrigger.power = fairyBomb.effects[0].callOnTrigger.power//2

starDustNeutralCard = copy.deepcopy(neutralCard)
starDustNeutralCard.turnInit = 1
starDust.effectAroundCaster = [TYPE_BOOST,AREA_CIRCLE_2,starDustNeutralCard]

def findOther(otherId : Union[str,other]) -> Union[other,None]:
    if type(otherId) == other:
        return otherId
    else:
        otherId = otherId.replace("\n","")
        for a in others:
            if a.id == otherId or a.name.lower() == otherId.lower():
                return a
    return None

listAllyEnemies = ["Lia","Liz","Liu","Lio"]
for tmpName in listAllyEnemies: 
    try: findAllie(tmpName).says = findEnnemi(tmpName).says
    except: pass

listAllBuyableShop, cmpt, idList = [], 0, []
for eff in effects:
    idList.append(eff.id)

for a in weapons+skills+stuffs:
    if a.price > 0: listAllBuyableShop.append(a)

    idList = []
    for eff in effects:
        idList.append(eff.id)

    if a.__class__ == skill:
        skillsToSee, tablSkillsEff = [[a], a.become][a.become != None], []
        for skillSeen in skillsToSee:
            skillEffs = skillSeen.effects
            for skillEffect in skillEffs:
                skillEffect = findEffect(skillEffect)
                if skillEffect != None:
                    tablSkillsEff.append(skillEffect)
                    while skillEffect != None and skillEffect.callOnTrigger != None:
                        tablSkillsEff.append(skillEffect)
                        skillEffect = findEffect(skillEffect.callOnTrigger)

        for effectSeen in tablSkillsEff:
            if (effectSeen.replace or effectSeen.reject != None) and not(effectSeen.id in idList):
                effects.append(effectSeen)
                idList.append(effectSeen.id)
                cmpt += 1

print("{0} effects has been added to the FindEffect list".format(cmpt))

undeadPasEff = copy.deepcopy(constEff)
undeadPasEff.power, undeadPasEff.stat, undeadPasEff.turnInit = 20, PURCENTAGE, -1

for cmpt in range(len(skills)):
    if skills[cmpt].invocation != None:
        summon: invoc = findSummon(skills[cmpt].invocation)
        timeLeft, iaPow, selfDestruc = 0, 0, False
        for skil in summon.skills:
            if type(skil) == skill:
                iaPow += skil.iaPow
                if not(skil.replay) or skil.type not in [TYPE_PASSIVE]:
                    timeLeft += 1
                if skil.effectOnSelf != None and skil.effectOnSelf.id == autoEff.id:
                    iaPow -= autoEff.power
                    selfDestruct = True
        if timeLeft < 3 and not(selfDestruc):
            iaPow += summon.weapon.power * (3-timeLeft)
        skills[cmpt].iaPow += (iaPow * skills[cmpt].nbSummon)
        if skills[cmpt].description in [None,""]:
            skills[cmpt].description = "Permet d'invoquer (un{0}) {2} {1} : {3}".format(["","e"][summon.gender == GENDER_FEMALE], summon.icon[0], summon.name, summon.description)

def userShopPurcent(user : char):
    totalShop = len(listAllBuyableShop)
    tablToSee = listAllBuyableShop[:]
    for a in listAllBuyableShop:
        if user.have(a):
            tablToSee.remove(a)

    return 100-(len(tablToSee)/totalShop*100)

def seeSimilarStuffNameMinLvl(name:str):
    tablLvl,tablName = [],[]

    name = name.lower()

    for obj in stuffs:
        if name in obj.name.lower():
            if obj.minLvl in tablLvl:
                for cmpt in range(len(tablLvl)):
                    if tablLvl[cmpt] == obj.minLvl:
                        tablName[cmpt].append(obj)
                        break
            else:
                tablLvl.append(obj.minLvl)
                tablName.append([obj])

    if tablLvl == []:
        return "==================================\n\"{0}\" :\nAucun objet trouvé".format(name)

    tablLvl.sort()
    tablName.sort(key=lambda alice: alice[0].minLvl)

    toReturn = "==================================\n\"{0}\" :".format(name)
    for cmpt in range(len(tablLvl)):
        toReturn += "\n- {0}".format(tablLvl[cmpt])
        tablName[cmpt].sort(key=lambda clemence:clemence.name)
        for obj in tablName[cmpt]:
            toReturn += "\n   {0}".format(obj.name)

    return toReturn

def seeAllStuffAtMinLvl(level:int):
    tablToSee = []
    for obj in stuffs:
        if obj.minLvl == level:
            tablToSee.append(obj.name)

    if tablToSee == []:
        return "==================================\n\"{0}\" :\nAucun objet trouvé".format(level)

    tablToSee.sort()

    toReturn = "==================================\n\"{0}\" :".format(level)
    for name in tablToSee:
        toReturn += "\n   {0}".format(name)

    return toReturn

# Stuff verifications ===========================================================================
if not(isLenapy):
    print("=============================\nVérification de l'équilibrage des stuffs...")
    print("Nombre d'équipements :", len(stuffs))
    allstats = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for a in stuffs:
        if a.effects == None:
            ballerine = a.allStats()+[a.resistance,a.percing,a.critical]
            babie = [a.negativeHeal,a.negativeBoost,a.negativeShield,a.negativeDirect,a.negativeIndirect]
            sumation = 0
            for b in range(0,len(ballerine)):
                sumation += ballerine[b]
                allstats[b] += ballerine[b]

            for b in babie:
                sumation -= b

            if sumation < 18 and summation > 22 and a.effects == None and a.name != "Claquettes chaussettes":
                print("{0} n'a pas le bon cumul de stats : {1}".format(a.name,sumation))

            elif sumation != 10 and a.effects != None:
                print("{0} n'a pas le bon cumul de stats : {1}".format(a.name,sumation))

    temp = "\nDistribution des statistiques :\n"
    total = 0
    for a in allstats:
        total += a

    for a in range(0,len(allStatsNames)):
        temp += "{0} : {1}% ({2})\n".format(allStatsNames[a],round(allstats[a]/total*100,2),allstats[a])
    #print(temp)

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

    tempToPrint = ''
    for temp in lvlTabl:
        tempToPrint+="\nObjets de niveau {0} : {1} ({2})%, statsAttendues : {3}".format(temp["level"],temp["nombre"],round(temp["nombre"]/lenStuff*100,2),20 + (temp["level"] * 2))
    #print(tempToPrint)

    tabl = copy.deepcopy(tablAllAllies)
    tablTank = []
    tablMid = []
    tablBack = []

    for allie in tabl:
        [tablTank,tablMid,tablBack][allie.weapon.range].append(allie)

    #print("")
    for num in range(3):
        pass
        #print("Nombre de Temp's en {0} : {1}".format(["mêlée","distance","backline"][num],len([tablTank,tablMid,tablBack][num])))

    tablTank, tablMid, tablBack = [], [], []
    for ennemi in tablUniqueEnnemies:
        [tablTank,tablMid,tablBack][ennemi.weapon.range].append(ennemi)
        summ = sum(ennemi.allStats()+[ennemi.resistance,ennemi.percing,ennemi.critical])
        awaited = int((280+110*3)*1)
        if summ < awaited*0.9 or summ > awaited*1.1:
            print("{0} n'a pas le bon cumul de stats : {1} ({2})".format(ennemi.name,summ,awaited))

    #print("")
    for num in range(3):
        #print("Nombre d'ennemis en {0} : {1}".format(["mêlée","distance","backline"][num],len([tablTank,tablMid,tablBack][num])))
        pass


    print("Vérification de l'équilibrage des stuffs terminée\n=============================")

nbAdjustedWeap = 0
for weap in weapons:
    summation = 0
    for stats in weap.allStats()+[weap.resistance,weap.percing,weap.critical]:
        summation += stats

    toVerif = 50
    if weap.effects != None or weap.effectOnUse != None:
        toVerif -= 20

    if int(summation) != int(toVerif):
        print("{0} : Cumule de stats non égal à {1} ({2} / {1})".format(weap.name,toVerif,summation))
    if weap.type == TYPE_DAMAGE and weap.power != 0 and weap.accuracy != 0 and not(weap.ignoreAutoVerif):
        expectation = 60 - {RANGE_MELEE:0,RANGE_DIST:10,RANGE_LONG:20}[weap.range]

        if weap.area != AREA_MONO:
            expectation = expectation * 0.7
        if weap.effects != None or weap.effectOnUse != None:
            if weap.id not in ["ob"]:
                expectation = expectation * 0.8
            else:
                expectation = expectation * 0.9
        expectation = int(expectation)

        weapAccu = weap.accuracy/100
        reality = int(weap.power * weap.repetition * weapAccu)
        if reality != expectation:
            suggest = int(expectation / (weap.repetition * weapAccu))
            if suggest != weap.power:
                #print("{0} : Expected {1} finalPower, got {2}. Suggested basePower : {3}\n> Base Power : {4}, Accuracy : {5}".format(weap.name,expectation,reality,suggest,weap.power,weap.accuracy))
                weap.power, nbAdjustedWeap = suggest, nbAdjustedWeap+1
if nbAdjustedWeap > 0:
    print("> Puissance de {0} armes auto ajustée".format(nbAdjustedWeap))

if not(isLenapy):
    allReadySeen, allReadySeenName = [],[]
    for obj in stuffs+weapons+skills+others:
        if obj.id not in allReadySeen:
            allReadySeen.append(obj.id)
        else:
            what = ""
            for whaty in stuffs+weapons+skills+others:
                if whaty.id == obj.id:
                    what += whaty.name + ", "
            raise Exception("Identifiant doublon : {0}({1})".format(what,obj.id))
        if obj.name.lower() not in allReadySeenName:
            allReadySeenName.append(obj.name.lower())
        else:
            what = obj.id
            for whaty in stuffs+weapons+skills+others:
                if whaty.name.lower() == obj.name.lower() and whaty.id != obj.id:
                    what += ", {0}".format(whaty.id)
            raise Exception("Nom doublon : {0} ({1})".format(obj.name,what))
    del allReadySeen, allReadySeenName

#print(seeSimilarStuffNameMinLvl("papillon rose"))
#print(seeAllStuffAtMinLvl(0))

"""for stuffy in stuffs:
    if stuffy.emoji in ['<:defHead:896928743967301703>','<:defMid:896928729673109535>','<:defShoes:896928709330731018>']:
        print("{0} use a default emoji".format(stuffy.name))"""

class preDefSkillSet:
    def __init__(self,element: Union[int, None] = None, skillList : List[skill] = []):
        self.element = element
        self.skillList = skillList

dictPreDefSkillSet = {
    BERSERK:[
        preDefSkillSet(skillList=[findSkill("Défi"),findSkill("Danse des sabres"),findSkill("Combo Tempête de Fer"),findSkill("Conviction du Berserkeur"),findSkill("Choc Chromatique"),findSkill("Bain de Sang Avancé"),findSkill("Impact Justicier")]),
        preDefSkillSet(element=ELEMENT_EARTH,skillList=[findSkill("Défi"),findSkill("Elipse Terrestre"),findSkill("Frappe Terre"),findSkill("Bain de Sang"),findSkill("Force de volonté"),findSkill("Frappe Convertissante Avancée"),findSkill("Pied Voltige")]),
        preDefSkillSet(element=ELEMENT_AIR,skillList=[findSkill("Défi"),findSkill("Frappe Air"),findSkill("Poussée Aviaire"),findSkill("Convertion élémentaire"),findSkill("Dernier Voyage"),findSkill("Soyokaze"),findSkill("Aer ferrum")]),
        preDefSkillSet(skillList=[findSkill("Défi"),findSkill("Linceuil de Lémure"),findSkill("Fétu Suppliant"),findSkill("Uppercut"),findSkill("Dernier Voyage"),findSkill("Ombre de la Mort"),findSkill("HighKick")]),
        preDefSkillSet(skillList=[findSkill("Défi"),findSkill("Attaque Sournoise"),findSkill("Pied Voltige"),findSkill("Corps à corps / Déplacement"),findSkill("Assasinat"),findSkill("Mort Vivant"),findSkill("Bain de Sang")]),
        preDefSkillSet(skillList=[findSkill("Défi"),findSkill("Invocation - Chauve-souris"),findSkill("Carnage"),findSkill("Choc Cardinal"),findSkill("Démolition"),findSkill("Voyage Ombral"),findSkill("Frappe Vangeresse")]),
        preDefSkillSet(element=ELEMENT_AIR,skillList=[findSkill("Défi"),findSkill("Plumes Perçantes"),findSkill("Déluge de Plumes"),findSkill("Plumes Célestes"),findSkill("Danse de la pluie étoilée"),findSkill("Plumes Rémanantes"),findSkill("Flèche aérienne")])
    ],
    POIDS_PLUME:[
        preDefSkillSet(element=ELEMENT_AIR,skillList=[findSkill("Défi"),findSkill("Plumes Perçantes"),findSkill("Déluge de Plumes"),findSkill("Plumes Célestes"),findSkill("Danse de la pluie étoilée"),findSkill("Plumes Rémanantes"),findSkill("Flèche aérienne")]),
        preDefSkillSet(skillList=[findSkill("Défi"),findSkill("Baleyette"),findSkill("Uppercut"),findSkill("Pied Voltige"),findSkill("Choc Ténébreux"),findSkill("Triple Attaque"),findSkill("Assaut du Crabe")]),
        preDefSkillSet(element=ELEMENT_AIR,skillList=[findSkill("Défi"),findSkill("Libération"),findSkill("Flèche aérienne"),findSkill("Convertion élémentaire"),findSkill("Démolition"),findSkill("Envolée féérique"),findSkill("Soyokaze")]),
        preDefSkillSet(skillList=[findSkill("Défi"),findSkill("Combo Eventails Célestes"),findSkill("Chorégraphie de l'éventail"),findSkill("Danse des sabres"),findSkill("Danse de la pluie étoilée"),findSkill("Final Classique"),findSkill("Final Technique")]),
        preDefSkillSet(skillList=[findSkill("Défi"),findSkill("Attaque Sournoise"),findSkill("Pied Voltige"),findSkill("Corps à corps / Déplacement"),findSkill("Assasinat"),findSkill("Mort Vivant"),findSkill("Bain de Sang")]),
        preDefSkillSet(skillList=[findSkill("Défi"),findSkill("Linceuil de Lémure"),findSkill("Fétu Suppliant"),findSkill("Uppercut"),findSkill("Dernier Voyage"),findSkill("Ombre de la Mort"),findSkill("HighKick")]),
    ],
}

for cmpt in range(ASPI_NEUTRAL):
    try:
        dictPreDefSkillSet[cmpt]
    except KeyError:
        dictPreDefSkillSet[cmpt] = []

varAllies = [
    findAllie("Shihu"),findAllie("Belle"),findAllie("Klironovia"),findAllie("Altikia"),findAllie("Luna"),findAllie("Chûri-Hinoro")
]

for ally in tablAllAllies+varAllies:
    elem = None
    for skilly in ally.skills:
        skilly = findSkill(skilly)
        if skilly != None and len(skilly.condition) > 1 and skilly.condition[1] == ELEMENT:
            elem = skilly.condition[2]
    dictPreDefSkillSet[ally.aspiration].append(preDefSkillSet(skillList=ally.skills,element=elem))

    if ally.changeDict != None:
        for chDict in ally.changeDict:
            try:
                asp, elem = ally.aspiration, None
                if chDict.aspiration != None:
                    asp = chDict.aspiration
                if chDict.skills != None:
                    for skilly in chDict.skills:
                        try:
                            if len(skilly.condition) > 1 and skilly.condition[1] == ELEMENT:
                                elem = skilly.condition[2]
                        except:
                            print("Une ou plusieurs compétences de {0} n'a pas pu être retrouvée".format(ally.name))
                    dictPreDefSkillSet[asp].append(preDefSkillSet(skillList=chDict.skills,element=elem))
            except: print(ally.name, chDict)
    if ally.name in descKeys:
        ally.description = pnjDescriptions[ally.name]

listUseSkills = []
for aspiCmpt in dictPreDefSkillSet:
    for defSki in dictPreDefSkillSet[aspiCmpt]:
        for skilly in defSki.skillList:
            if skilly not in listUseSkills:
                listUseSkills.append(skilly)

for ally in tablAllAllies:
    for skilly in ally.skills:
        if type(skilly) == skill and skilly not in listUseSkills:
            listUseSkills.append(skilly)
    if ally.changeDict != None:
        for cdi in ally.changeDict:
            if type(cdi) == tempAltBuild:
                for skilly in cdi.skills:
                    if type(skilly) == skill and skilly not in listUseSkills:
                        listUseSkills.append(skilly)
            else:
                for cdi2 in cdi:
                    for skilly in cdi2.skills:
                        if type(skilly) == skill and skilly not in listUseSkills:
                            listUseSkills.append(skilly)

for pnj in tablBoss+tablBossPlus+tablRaidBoss:
    if pnj.name in descKeys:
        ennemi.description = pnjDescriptions[ennemi.name]

#exclusiveRepartition()

dictSmallReticens = {
    "Clémence":["Gwendoline","Klironovia","Altikia","Lena","Luna","Ruby","Julie"],
    "Lena":["Clémence","Gwendoline","Klironovia","Altikia","Iliana"],
    "Lohica":["Shehisa","Hélène","Astra","Hina","Ly"],
    "Félicité":["Clémence","Lia","Lio"],
    "Alice":["Lio"],
    "Ruby":["Félicité","Sixtine","Alice","Shushi","Shihu"],
    "Julie":["Félicité","Sixtine","Alice","Shushi","Shihu"],
    "Ly":["Lohica"],
    "Anna":["Shushi","Shihu"],
    "Bénédicte":["Clémence"],
    "Shehisa":["Icealia","Lohica"],
    "Hélène":["Icealia","Lohica"]
}

dictMediumReticens = {
    "Lena":["Félicité","Sixtine","Alice"],
    "Gwendoline":["Félicité","Sixtine","Alice","Shushi","Shihu"],
    "Clémence":["Félicité","Sixtine","Alice","Shushi","Shihu"],
    "Alice":["Clémence","Bénédicte","Lily","Anna","Belle"],
    "Shushi":["Lena","Gwendoline","Klironovia","Altikia","Luna","Félicité","Sixtine","Alice"],
    "Shihu":["Lena","Gwendoline","Klironovia","Altikia","Luna","Félicité","Sixtine","Alice"],
    "Hélène":["Shehisa","Astra","Amary"],
    "Shehisa":["Amary","Astra","Hélène"],
    "Astra":["Shehisa","Hélène","Icealia"],
    "Félicité":["Sixtine","Lena","Gwendoline","Klironovia","Altikia","Luna","Iliana"],
    "Sixtine":["Félicité","Lena","Gwendoline","Klironovia","Altikia","Luna","Iliana"],
    "Icealia":["Shehisa","Lohica","Astra","Amary"],
    "Ruby":["Julie","Clémence"],
    "Julie":["Clémence"],
    "Iliana":["Félicité","Sixtine","Alice","Gwendoline","Klironovia","Altikia"]
}

def getAllieFromEnemy(enemy:octarien,lvl:int,gearEmotes:List[str]=[None,None,None],color=None) -> tmpAllie:
    """Return a `tmpAllie` object from a `octarien` object"""
    if type(enemy) == str:
        enemy = copy.deepcopy(findEnnemi(enemy))
    tablStats = [
        int(enemy.strength*(max(10,lvl)/50)/3),
        int(enemy.endurance*(max(10,lvl)/50)/3),
        int(enemy.charisma*(max(10,lvl)/50)/3),
        int(enemy.agility*(max(10,lvl)/50)/3),
        int(enemy.precision*(max(10,lvl)/50)/3),
        int(enemy.intelligence*(max(10,lvl)/50)/3),
        int(enemy.magie*(max(10,lvl)/50)/3),
        int(enemy.resistance/3),
        int(enemy.percing/3),
        int(enemy.critical/3)
    ]
    tempStuff = [
        stuff("noName","noId",0,0,
              strength=tablStats[0],
              endurance=tablStats[1],
              charisma=tablStats[2],
              agility=tablStats[3],
              precision=tablStats[4],
              intelligence=tablStats[5],
              magie=tablStats[6],
              resistance=tablStats[7],
              percing=tablStats[8],
              critical=tablStats[9],
              emoji=gearEmotes[0]),
        stuff("noName","noId",1,0,
              strength=tablStats[0],
              endurance=tablStats[1],
              charisma=tablStats[2],
              agility=tablStats[3],
              precision=tablStats[4],
              intelligence=tablStats[5],
              magie=tablStats[6],
              resistance=tablStats[7],
              percing=tablStats[8],
              critical=tablStats[9],
              emoji=gearEmotes[1]),
        stuff("noName","noId",2,0,
              strength=tablStats[0],
              endurance=tablStats[1],
              charisma=tablStats[2],
              agility=tablStats[3],
              precision=tablStats[4],
              intelligence=tablStats[5],
              magie=tablStats[6],
              resistance=tablStats[7],
              percing=tablStats[8],
              critical=tablStats[9],
              emoji=gearEmotes[2])
        ]

    toReturn = tmpAllie(
        enemy.name,
        1,
        [color,light_blue][color==None],
        enemy.aspiration,
        enemy.weapon,
        tempStuff,
        enemy.gender,
        enemy.skills,
        enemy.description,
        deadIcon=enemy.deadIcon,
        icon=enemy.icon,
        say=enemy.says,
        splashArt=enemy.splashArt,
        splashIcon=enemy.splashIcon,
        team = ennemi.npcTeam)

    if toReturn.name == "Marinier Sabreur":
        toReturn.name = "Pirate Sabreur"
        if random.randint(0,1) < 1:
            toReturn.species, toReturn.icon = 1, "<:pirSab1:1059519845177249812>"
        else:
            toReturn.species, toReturn.icon = 2, "<:pirSan2:1059519736347631696>"
    elif toReturn.name == "Marinier Tireur":
        toReturn.name = "Pirate Tireur"
        if random.randint(0,1) < 1:
            toReturn.species, toReturn.icon = 1, "<:pirGun1:1059519820376330351>"
        else:
            toReturn.species, toReturn.icon = 2, "<:pirGun2:1059519760284528640>"

    toReturn.standAlone = enemy.standAlone
    toReturn.changeLevel(lvl,False,0,False)

    return toReturn

findAllie("Shehisa").counterEmoji, findAllie("Luna").counterEmoji, findAllie("Klironovia").counterEmoji, findAllie("Félicité").counterEmoji, findAllie("Alice").counterEmoji = "<:chiphidenBlade:1223632204421140610>", fracas.emoji, fracas.emoji, uppercut.emoji, "<:aliceCounter:1190621769581727755>"
findEnnemi("Lia").counterEmoji, findEnnemi("Liu").counterEmoji = "<:liaCounter:998001563379437568>", "<:liuSkill:922328931502280774>"

importantSkills.append(lenaExSkill5)
