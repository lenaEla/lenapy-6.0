from classes import *
from advObjects.advWeapons import *
from advObjects.advSkills import *
from advObjects.advStuffs import *
from advObjects.advInvocs import *
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

others = [elementalCristal,customColor,changeAspi,changeAppa,changeName,restat,blablator,dimentioCristal,mimique,ilianaGrelot,grandNouveau,aliceBatEarRing,birdup,Megalovania,amary]

previewDict = {
    ilianaGrelot.id:'https://cdn.discordapp.com/emojis/930806243461857301.png',
    grandNouveau.id:'https://cdn.discordapp.com/emojis/930807241064480828.png',
    aliceBatEarRing.id:'https://cdn.discordapp.com/emojis/930807423483129876.png',
    birdup.id:'https://cdn.discordapp.com/emojis/930908758773743616.png',
    Megalovania.id:'https://cdn.discordapp.com/emojis/930911733307027536.png',
    amary.id:'https://cdn.discordapp.com/emojis/935340408723112047.png'
}

changeIconForm = [grandNouveau,ilianaGrelot,aliceBatEarRing,birdup,Megalovania,amary]

# Specials skills ================================================================================
# Total Kboum
totalAnnilLauch = copy.deepcopy(explosion)

totalAnnilCastEff4 = copy.deepcopy(castExplo)
totalAnnilCastEff4.replica, totalAnnilCastEff4.name = totalAnnilLauch, "Annihilation totale dans 1 tour !"
totalAnnilCastSkill4 = copy.deepcopy(explosionCast)
totalAnnilCastSkill4.effectOnSelf = totalAnnilCastEff4

totalAnnilCastEff3 = copy.deepcopy(castExplo)
totalAnnilCastEff3.replica, totalAnnilCastEff3.name = totalAnnilCastSkill4, "Annihilation totale dans 2 tours !"
totalAnnilCastSkill3 = copy.deepcopy(explosionCast)
totalAnnilCastSkill3.effectOnSelf = totalAnnilCastEff3

totalAnnilCastEff2 = copy.deepcopy(castExplo)
totalAnnilCastEff2.replica, totalAnnilCastEff2.name = totalAnnilCastSkill3, "Annihilation totale dans 3 tours !"
totalAnnilCastSkill2 = copy.deepcopy(explosionCast)
totalAnnilCastSkill2.effectOnSelf = totalAnnilCastEff2

totalAnnilCastEff1 = copy.deepcopy(castExplo)
totalAnnilCastEff1.replica, totalAnnilCastEff1.name = totalAnnilCastSkill2, "Annihilation totale dans 4 tours !"
totalAnnilCastSkill1 = copy.deepcopy(explosionCast)
totalAnnilCastSkill1.effectOnSelf = totalAnnilCastEff1

totalAnnilCastEff0 = copy.deepcopy(castExplo)
totalAnnilCastEff0.replica, totalAnnilCastEff0.name = totalAnnilCastSkill1, "Annihilation totale dans 5 tours !"
totalAnnilCastSkill0 = copy.deepcopy(explosionCast)
totalAnnilCastSkill0.effectOnSelf = totalAnnilCastEff0

totalAnnilLauch.name = totalAnnilCastSkill1.name = totalAnnilCastSkill2.name = totalAnnilCastSkill3.name = totalAnnilCastSkill4.name = totalAnnilCastSkill0.name = "Annihilation totale"
totalAnnilLauch.ultimate = totalAnnilCastSkill1.ultimate = totalAnnilCastSkill2.ultimate = totalAnnilCastSkill3.ultimate = totalAnnilCastSkill4.ultimate = totalAnnilCastSkill0.ultimate = totalAnnilLauch.shareCooldown = totalAnnilCastSkill1.shareCooldown = totalAnnilCastSkill2.shareCooldown = totalAnnilCastSkill3.shareCooldown = totalAnnilCastSkill4.shareCooldown = totalAnnilCastSkill0.shareCooldown = False

BOUMBOUMBOUMBOUMweap = weapon("noneWeap","BoumX4",1,AREA_CIRCLE_1,0,0,0)

def findOther(otherId : Union[str,other]) -> Union[other,None]:
    if type(otherId) == other:
        return otherId
    else:
        otherId = otherId.replace("\n","")
        for a in others:
            if a.id == otherId or a.name.lower() == otherId.lower():
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
    print("Nombre d'équipements : ", len(stuffs))
    allstats = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for a in stuffs:
        if a.effect == None or (a.effect != None and findEffect(a.effect).id != summonerMalus.id):
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

    tabl = copy.deepcopy(tablAllEnnemies)
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

            awaited = int((280+110*3)*1)
            if summ < awaited*0.9 or summ > awaited*1.1:
                print("{0} n'a pas le bon cumul de stats : {1} ({2})".format(ennemi.name,summ,awaited))

    #print("")
    for num in range(3):
        #print("Nombre d'ennemis en {0} : {1}".format(["mêlée","distance","backline"][num],len([tablTank,tablMid,tablBack][num])))
        pass

    for weap in weapons:
        summation = 0
        for stats in weap.allStats()+[weap.resistance,weap.percing,weap.critical]:
            if stats < 0:
                print("{0} : Stat négative détectée !".format(weap.name))
            else:
                summation += stats

        toVerif = 30
        if weap.effect != None or weap.effectOnUse != None:
            toVerif = 15

        if int(summation) != int(toVerif):
            print("{0} : Cumule de stats non égal à {1} ({2} / {1})".format(weap.name,toVerif,summation))
    print("Vérification de l'équilibrage des stuffs terminée\n=============================")

listObjWithNoOrientation = []
for obj in stuffs:
    if obj.orientation == "Neutre":
        listObjWithNoOrientation.append(obj.name)

"""if listObjWithNoOrientation != []:
    print("=================== Objets sans orientations ===================")
    for obj in listObjWithNoOrientation:
        print(obj)
"""

allReadySeen = []
for obj in stuffs+weapons+skills+others:
    if obj.id not in allReadySeen:
        allReadySeen.append(obj.id)
    else:
        what = ""
        for whaty in stuffs+weapons+skills+others:
            if whaty.id == obj.id:
                what += whaty.name + ", "
        raise Exception("Identifiant doublon : {1}".format(obj.name,what))

#print(seeSimilarStuffNameMinLvl("Pendantif du papillon"))
#print(seeAllStuffAtMinLvl(25))

"""for stuffy in stuffs:
    if stuffy.emoji in ['<:defHead:896928743967301703>','<:defMid:896928729673109535>','<:defShoes:896928709330731018>']:
        print("{0} use a default emoji".format(stuffy.name))"""