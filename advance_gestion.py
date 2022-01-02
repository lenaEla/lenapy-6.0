import os,discord,emoji,copy,requests,io
from typing import List
from classes import *
from gestion import *
from adv import *
from discord_slash.utils.manage_components import *
from commands_files.alice_stats_endler import *
from PIL import Image, ImageColor
from data.database import *
from sys import maxsize

stuffDB = dbHandler(database="stuff.db")
customIconDB = dbHandler(database="custom_icon.db")

timeoutSelect = create_select(
    options=[create_select_option("Timeout","Parfois je me demande ce que ferais Lena si elle pensais par elle même",emoji='🕛',default=True)],
    disabled=True
)
timeoutSelect = create_actionrow(timeoutSelect)

def remove_accents(input_str : str):
    temp =""
    for a in input_str:
        if a in ["à","ä","â","@"]:
            temp += "a"
        elif a in ["é","è","ê","ë"]:
            temp += "e"
        elif a in ["ì","ï","î"]:
            temp += "i"
        elif a in ["ù","û"]:
            temp += "u"
        elif a in ["À","Ä","Â"]:
            temp += "A"
        elif a in ["É","È","Ë","Ê"]:
            temp += "E"
        elif a == " ":
            pass
        else:
            temp+=a

    return temp

def visuArea(area : int,wanted,ranged=True) -> list:
    tablAllCells=[]

    class cell:
        def __init__(self,x,y,id):
            self.x = x
            self.y = y
            self.id = id
            self.on = None

        def distance(self,cell=0):
            return (abs(self.x - cell.x)+abs(self.y - cell.y))

        def getArea(self,area=AREA_MONO,team=0):
            rep = []

            # Circles
            if area in [AREA_CIRCLE_1,AREA_CIRCLE_2,AREA_CIRCLE_3,AREA_CIRCLE_4,AREA_CIRCLE_5,AREA_CIRCLE_6,AREA_CIRCLE_7,AREA_DONUT_1,AREA_DONUT_2,AREA_DONUT_3,AREA_DONUT_4,AREA_DONUT_5,AREA_DONUT_6,AREA_DONUT_7,AREA_DIST_3,AREA_DIST_4,AREA_DIST_5,AREA_DIST_6,AREA_DIST_7]:
                dist = area
                if area > AREA_CIRCLE_7:
                    if area <= AREA_DONUT_7:
                        dist -= AREA_DONUT_1-1
                    elif area <= AREA_DIST_7:
                        dist -= AREA_DIST_3-3

                for a in tablAllCells:
                    if self.distance(cell=a) <= dist:
                        rep.append(a)

                if area > AREA_CIRCLE_7 and area <= AREA_DONUT_7: # If donut, remove the center
                    rep.remove(self)
                elif area > AREA_DONUT_7 and area <= AREA_DIST_7: # If dist only, remove melee
                    for a in rep[:]:
                        if self.distance(cell=a) <= 2:
                            rep.remove(a)

            elif area in [AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES]:
                for b in tablAllCells:
                    if b.on != None:
                        if area == AREA_ALL_ALLIES and b.on.team == team:
                            rep+=[b]
                        elif area == AREA_ALL_ENEMIES and b.on.team != team:
                            rep+=[b]
                        elif area == AREA_ALL_ENTITES:
                            rep+=[b]

            elif area in [AREA_CONE_2,AREA_CONE_3,AREA_CONE_4,AREA_CONE_5,AREA_CONE_6,AREA_CONE_7]:
                start,yDiff,xMax = self.x,0,area-10
                areaTabl = []

                if team==0:
                    ite = 0
                    while start <= 5 and ite <= xMax:
                        for y in range(0,yDiff+1):
                            if findCell(start,self.y+y) not in areaTabl and findCell(start,self.y+y) != None:
                                areaTabl.append(findCell(start,self.y+y))
                            if findCell(start,self.y-y) not in areaTabl and findCell(start,self.y-y) != None:
                                areaTabl.append(findCell(start,self.y-y))
                        start += 1
                        yDiff += 1
                        ite+=1
                else:
                    ite = 0
                    while start >= 0 and ite <= xMax:
                        for y in range(0,yDiff+1):
                            if findCell(start,self.y+y) not in areaTabl and findCell(start,self.y+y) != None:
                                areaTabl.append(findCell(start,self.y+y))
                            if findCell(start,self.y-y) not in areaTabl and findCell(start,self.y-y) != None:
                                areaTabl.append(findCell(start,self.y-y))
                        start -= 1
                        yDiff += 1
                        ite+=1

                return areaTabl

            elif area in [17,18,19,20,21]: # Lines
                for a in tablAllCells:
                    if self.y == a.y and abs(a.x - self.x) <= area-16:
                        rep.append(a)

            elif area in [AREA_ARC_1,AREA_ARC_2,AREA_ARC_3]: # Arcs
                cmptx = 1
                while cmptx < area - 32:
                    if team == 0:
                        cell1 = findCell(self.x-cmptx,self.y-cmptx)
                        if cell1 != None:
                            rep.append(cell1)
                        cell2 = findCell(self.x-cmptx,self.y+cmptx)
                        if cell2 != None:
                            rep.append(cell2)
                    if team == 1:
                        cell1 = findCell(self.x+cmptx,self.y-cmptx)
                        if cell1 != None:
                            rep.append(cell1)
                        cell2 = findCell(self.x+cmptx,self.y+cmptx)
                        if cell2 != None:
                            rep.append(cell2)
                    cmptx+=1
                rep.append(self)

            elif area==AREA_MONO:
                return [self]
            
            return rep

    def findCell(x,y):
        cmpt = 0
        while cmpt < 30:
            if tablAllCells[cmpt].x == x and tablAllCells[cmpt].y == y:
                return tablAllCells[cmpt]
            cmpt += 1

    cmpt = 0
    for a in [0,1,2,3,4,5]:
        for b in [0,1,2,3,4]:
            tablAllCells += [cell(a,b,cmpt)]
            cmpt += 1

    if not(ranged):
        if wanted == ALLIES:
            isAlly = -1
            isAlly2 = -2
            isAlly3 = -3
        else:
            isAlly = 0
            isAlly2 = 1
            isAlly3 = 2

        base = 3
        
        if area in [AREA_CIRCLE_4,AREA_CONE_4,AREA_LINE_4,AREA_DONUT_4,AREA_DIST_4]:
            visibleCell = findCell(base+isAlly2,2)
        elif area in [5,6,7,14,15,16,20,21,26,27,28,31,32,33]:
            visibleCell = findCell(base+isAlly3,2)
        else:
            visibleCell = findCell(base+isAlly,2)

    else:
        if area in [AREA_CIRCLE_4,AREA_CONE_4,AREA_LINE_4,AREA_DONUT_4,AREA_DIST_4]:
            visibleCell = findCell(1,2)
        elif area in [5,6,7,14,15,16,20,21,26,27,28,31,32,33]:
            visibleCell = findCell(0,2)
        else:
            visibleCell = findCell(2,2)

    visibleArea = visibleCell.getArea(area=area)
    line1,line2,line3,line4,line5 = [None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None]
    lines = [line1,line2,line3,line4,line5]
    temp = ""

    for a in tablAllCells:
        temp = f'<:empty:866459463568850954>'
        if a in visibleArea:
            if wanted == ALLIES:
                temp = "<:Targeted1:873118129214083102>"
            else:
                temp = "<:Targeted2:873118129130192947>"

        lines[a.y][a.x]=temp
    if ranged:
        lines[visibleCell.y][visibleCell.x] = "<:ikaWhite:871149538554044466>"
    else:
        if visibleCell in visibleArea: 
            if wanted==ENNEMIS:
                lines[visibleCell.y][visibleCell.x] = "<:ikaRedTargeted2:873118129541238814>"                       # Memo : Lines[y][x]
            else:
                lines[visibleCell.y][visibleCell.x] = '<:ikaLBTargeted1:873118128958214166>'
        else:
            if wanted==ENNEMIS:
                lines[visibleCell.y][visibleCell.x] = '<:ikaRed:866459224664702977>'
            else:
                lines[visibleCell.y][visibleCell.x] = '<:ikaLBlue:866459302319226910>'

    temp = ""
    for a in lines:
        for b in [0,1,2,3,4]:
            temp += f"{a[b]}|"
        temp += f"{a[b+1]}\n"

    return temp

def infoEffect(effId : str, user : char, embed : discord.Embed,ctx ,self=False) -> discord.Embed:
    effTmp,boucle,iteration,fieldname ="",True,False,"__Effet :__"
    eff = findEffect(effId)

    if eff.id == lunaSkill5_3_eff.id:
        fieldname = "**__Effet sur la cible :__** ({0})".format(lunaSkill5_3.name)

    while boucle:
        eff = findEffect(effId)
        bonus,malus = "",""
        Stat = ""
        if eff.stat == None:
            Stat = "Aucune"
        elif eff.stat == PURCENTAGE:
            Stat = "Pourcentage"
        elif eff.stat != HARMONIE:
            Stat = allStatsNames[eff.stat]
        else:
            Stat = "Harmonie"

        tamp = str(eff.turnInit) + " tour{0}".format(["","s"][eff.turnInit>1])
        if eff.turnInit == -1:
            tamp = "Infinie"

        Powa = ""
        if eff.power > 0:
            Powa = "\n__Puissance :__ "+str(max(eff.power,eff.overhealth))
        if eff.id == lunaSkill4Eff.id:
            Powa += "\n__Puissance alternative :__ "+str(lunaSkill4EffAlt.power)

        cumu = ""
        if eff.stackable:
            cumu = "\n\nCet effet est **cumulable**"
        effTmp+=f"__Nom :__ {eff.name}\n__Icone de l'effet :__ {eff.emoji[user.species-1][0]}\n__Durée :__ {tamp}\n__Statistique prise en compte :__ **{Stat}**{Powa}{cumu}"

        if eff.lvl != 1:
            effTmp += "\nCet effet peut se déclancher au maximum **{0} fois**".format(eff.lvl)
        stats = eff.allStats()+[eff.resistance,eff.percing,eff.critical,eff.overhealth,eff.aggro,eff.inkResistance]
        names = nameStats+nameStats2+["Armure","Agression","Résistance aux dégâts indirects"]

        if eff.redirection > 0:
            effTmp +="\nCet effet redirige **{0}**% des **dégâts direct** reçu par le porteur vers le lanceur de l'effet en tant que **dégâts indirects**\n".format(eff.redirection)

        if eff.immunity:
            effTmp+="Tant que le porteur possède cet effet, il est **Invulnérable aux dégâts**\n"

        effTmp += f'\n\n__Description :__\n{eff.description}\n'
        for a in range(len(stats)):
            if stats[a] > 0:
                bonus += f"{names[a]} : +{stats[a]}\n"
            elif stats[a] < 0:
                malus += f"{names[a]} : {stats[a]}\n"

        if bonus !="":
            effTmp+=f"\n**__Bonus de statistiques :__**\n{bonus}"
        if malus !="":
            effTmp+=f'\n**__Malus de statistiques :__**\n{malus}'

        if eff.inkResistance > 0 and eff.stat != None:
            effTmp += "\nLa résistance aux dégâts indirects ne peux pas dépasser 3 fois sa valeur de base\nSi plusieurs effects de réduction de dégâts indirects sont cumulés, seul le plus puissant sera pris en compte"
        if eff.reject != None:
            effTmp += "\n__Cet effet n'est pas compatible avec les effets :__\n"
            for a in eff.reject:
                rejected = findEffect(a)
                effTmp += f"{rejected.emoji[user.species-1][0]} {rejected.name}\n"

        if eff.callOnTrigger != None and not(iteration):
            effId = eff.callOnTrigger
            iteration = True
            embed.add_field(name = fieldname,value = effTmp,inline = False)
            effTmp = ""
            fieldname = "<:empty:866459463568850954>\n__À l'activation, cet effet donne un autre effet :__"
        elif eff.callOnTrigger != None and iteration:
            effId = findEffect(eff.callOnTrigger)
            embed.add_field(name = fieldname,value = effTmp,inline = False)
            fieldname = "<:empty:866459463568850954>\n__À l'activation, cet effet donne un autre effet :__"
            if eff.area != AREA_MONO:
                ballerine, babie = [TYPE_ARMOR,TYPE_BOOST,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ,TYPE_RESURECTION,TYPE_HEAL],[TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE]
                for a in ballerine:
                    if a == eff.type:
                        embed.add_field(name = "__Zone d'effet :__",value=visuArea(eff.area,wanted=ALLIES,ranged=False))
                        break

                for a in babie:
                    if a == eff.type:
                        embed.add_field(name = "__Zone d'effet :__",value=visuArea(eff.area,wanted=ENNEMIS,ranged=False))
                        break
            break
        else:
            if not(self):
                embed.add_field(name = fieldname,value = effTmp,inline = False)
            else:
                embed.add_field(name = "<:empty:866459463568850954>\n**__Effet sur soi :__**",value = effTmp,inline = False)

            if eff.area != AREA_MONO:
                if eff.type in [TYPE_ARMOR,TYPE_BOOST,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ,TYPE_RESURECTION,TYPE_HEAL]:
                    embed.add_field(name = "__Zone d'effet :__",value=visuArea(eff.area,wanted=ALLIES,ranged=False))
                    break

                elif eff.type in [TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE]:
                    embed.add_field(name = "__Zone d'effet :__",value=visuArea(eff.area,wanted=ENNEMIS,ranged=False))

                if eff.id == lunaSkill4Eff.id:
                    embed.add_field(name = "__Zone d'effet alternative :__",value=visuArea(AREA_MONO,wanted=ENNEMIS,ranged=False))
            break

    return embed

def infoSkill(skill : skill, user : char,ctx):
    skil = skill
    cast = 0
    while skil.effectOnSelf != None:
        eff = findEffect(skil.effectOnSelf)
        if eff.replica != None:
            skil = findSkill(eff.replica)
        else:
            break
        cast += 1

    if skill.id == trans.id:
        if user.aspiration in [BERSERK,POIDS_PLUME]:
            skil = transMelee
        elif user.aspiration in [ENCHANTEUR,MAGE]:
            skil = transCircle  
        elif user.aspiration in [TETE_BRULE,OBSERVATEUR]:
            skil = transLine
        elif user.aspiration in [ALTRUISTE,IDOLE]:
            skil = transHeal
        elif user.aspiration == INVOCATEUR:
            skil = transInvoc
        elif user.aspiration in [PROTECTEUR, PREVOYANT]:
            skil = transShield

    elif skil.id == mageUlt.id:
        if user.element in [ELEMENT_FIRE,ELEMENT_AIR,ELEMENT_SPACE]:
            skil = mageUltZone
        elif user.element in [ELEMENT_WATER,ELEMENT_EARTH,ELEMENT_TIME]:
            skil = mageUltMono
        else:
            skil = mageUlt

    if skil.become != None:
        desc = "Cette compétence peut devenir les compétences :\n"
        for cmpt in range(len(skil.become)):
            desc += "__{1} {0}__".format(skil.become[cmpt].name,skil.become[cmpt].emoji)
            if cmpt < len(skil.become)-2:
                desc += ",\n"
            elif cmpt == len(skil.become)-2:
                desc += " et\n"
        desc += " si les conditions sont réunies.\nLeurs temps de rechargement sont syncronisés"
    else:
        desc = ""
    # Cooldown ---------------------------
    if skil.type != TYPE_PASSIVE:
        if skil.become != None:
            desc += "\n\n__Temps de rechargements :__\n"
            for cmpt in range(len(skil.become)):
                s = ""
                if skil.become[cmpt].cooldown > 1:
                    s = "s"
                desc += "{0} tour{2} ({1})\n".format(skil.become[cmpt].cooldown, skil.become[cmpt].name, s)

        else:
            s = ""
            if skil.cooldown > 1:
                s = "s"
            desc += f"\n__Temps de rechargements :__ {skil.cooldown} tour{s}"""

    if cast > 0:
        desc += "\n__Tours de chargements__ : **{0} tour{1}**".format(cast,["","s"][int(cast > 1)])

    temp = "__Type :__ "

    if skil.type == TYPE_DAMAGE:
        temp+="Dégats\n"
        
        if skil.description != None:
            temp += "\n__Description :__\n"+skil.description+"\n\n"
        
        # Power, Success and Damage Type
        if skil.become == None:
            if skil.repetition > 1:
                nbShot = " x{0}".format(skil.repetition)
            else:
                nbShot = ""
            temp+=f"\n__Puissance :__ **{skil.power}**{nbShot}\n__Zone d'effet :__ "
            temp+= areaNames[skil.area]
            temp += "\n__Précision :__ {0}%\n".format(skil.sussess)

        else:
            temp += "\n__Puissances :__\n"
            for cmpt in range(len(skil.become)):
                multi = ""
                if skil.become[cmpt].repetition > 1:
                    multi = " x{0}".format(skil.become[cmpt].repetition)
                temp += "__{0}__{2} ({1})\n".format(skil.become[cmpt].power, skil.become[cmpt].name, multi)

            
            temp+="\n__Zone d'effet :__\n"
            for cmpt in range(len(skil.become)):
                temp += "{0} ({1})\n".format(areaNames[skil.become[cmpt].area], skil.become[cmpt].name)
            
            temp+="\n__Précisions :__\n"
            for cmpt in range(len(skil.become)):
                temp += "{0}% ({1})\n".format(skil.become[cmpt].sussess, skil.become[cmpt].name)

        # Clem and Alice blood jauge skills
        if skil.id.startswith("clem") or skil.id.startswith("alice"):
            for skillID, cost in clemBJcost.items():
                if skil.id == skillID:
                    temp += "\n__Coût en points de sang :__ **{0}**".format(cost)

        if skil.range == AREA_MONO:
            if skil.type != TYPE_PASSIVE:
                temp += f"\nCette compétence se lance sur **soi-même**"
            else:
                temp += f"\nLes compétences passives se déclanchent au début du combat"

        if skil.become == None:
            temp += "\nCette compétence cible les **ennemis**"

        if skil.onArmor != 1 and skil.become == None:
            temp += "\n__Dégâts sur armure :__ **{0}%**".format(int(skil.onArmor*100))
        elif skil.become != None:
            for becomeName in skil.become:
                if becomeName.onArmor != 1:
                    temp += "\n__{2} {1}__ inflige **{0}%** de ses dégâts aux armures".format(int(becomeName.onArmor*100), becomeName.name, becomeName.emoji)


        if skil.use not in [None,HARMONIE]:
            temp += f"\nCette compétence utilise la statistique de **{nameStats[skil.use]}**"
        elif skil.use == None:
            temp += f"\nCette compétence inflige un montant **fixe** de dégâts"
        elif skil.use == HARMONIE:
            temp += f"\nCette compétence utilise la statistique d'**Harmonie**"

    else:
        temp+=tablTypeStr[skil.type]

        if skil.description != None:
            temp += "\n\n__Description :__\n"+skil.description+"\n"
        
        if skil.id.startswith("clem") or skil.id.startswith("alice"):
            for skillID, cost in clemBJcost.items():
                if skil.id == skillID:
                    temp += "\n__Coût en points de sang :__ **{0}**".format(cost)

        if skil.type in [TYPE_HEAL,TYPE_RESURECTION]:
            temp+="\n__Puissance :__ {0}".format(skil.power)
            if skil.use not in [None,HARMONIE]:
                temp += f"\nCette compétence utilise la statistique de **{nameStats[skil.use]}**"
            elif skil.use == None:
                temp += f"\nCette compétence soigne d'un montant **fixe** de PV"
            elif skil.use == HARMONIE:
                temp += f"\nCette compétence utilise la statistique d'**Harmonie**"

        if skil.range == AREA_MONO:
            if skil.type != TYPE_PASSIVE:
                temp += f"\nCette compétence se lance sur **soi-même**"
            else:
                temp += f"\nLes compétences passives se déclanchent au début du combat"
        else:
            ballerine, babie = [TYPE_ARMOR,TYPE_BOOST,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ,TYPE_RESURECTION,TYPE_HEAL],[TYPE_INDIRECT_DAMAGE,TYPE_MALUS]
            for a in ballerine:
                if a == skil.type:
                    temp+=f"\nCette compétence cible les **alliés**"
                    break
            for a in babie:
                if a == skil.type:
                    temp+=f"\nCette compétence cible les **ennemis**"
                    break

        if skil.area != AREA_MONO:
            ballerine = ["tous les alliés","tous les ennemis","tous les combattants"]
            for a in range(AREA_ALL_ALLIES,AREA_ALL_ENTITES+1):
                if a == skil.area:
                    temp+=f"\nCette compétence affecte **{ballerine[a-8]}**"

    if skil.shareCooldown :
        temp+=f"\nCette compétence a un cooldown syncronisé avec toute l'équipe"
    if skil.initCooldown > 1 and skil.type != TYPE_PASSIVE:
        temp+=f"\nCette compétence ne peut pas être utilisée avant le tour {skil.initCooldown}"

    if skil.condition != []:
        temp += "\nCette compétence "
        if skil.condition[0] == 0:
            temp += "est exclusive à "
            if skil.condition[1] == 0:
                temp += "l'arme "+findWeapon(skil.condition[2]).name+"**"
            elif skil.condition[1] == 1:
                temp += "l'aspiration **"+inspi[skil.condition[2]]+"**"
            elif skil.condition[1] == 2:
                temp += "l'élément **"+elemNames [skil.condition[2]]+"**"
        elif skil.condition[0] == 1:
            temp += f"nécessite que la statistique **{nameStats[skil.condition[1]]}** du personnage soit à **{skil.condition[2]}**"
        elif skil.condition[0] == 2:
            temp += "n'est pas compatible avec "
            if skil.condition[1] == 0:
                reject = findWeapon(skil.condition[2])
                temp += f"l'arme **{reject.name}** ({reject.emoji})" 
            elif skil.condition[1] == 1:
                reject = findSkill(skil.condition[2])
                temp += f"la compétence **{reject.name}** ({reject.emoji})"
    if skil.ultimate:
        temp += "\nCette compétence est une compétence ultime"
    if skil.effPowerPurcent != 100:
        temp+="\nLes effets donnés par cette compétence ont une puissance équivalente à **{0}%** de leur puissance initiale".format(skil.effPowerPurcent)

    if skil.knockback > 0 and skil.become == None:
        temp+="\n\n__Repoussement :__\nCette compétence repousse la cible de **{0}** case{1}".format(skil.knockback,["","s"][int(skil.knockback > 1)])

    if skil.become != None:
        allreadyAdd = False
        for becomeName in skil.become:
            if becomeName.knockback > 0:
                if not(allreadyAdd):
                    temp += "\n\n**__Repoussement :__**"
                    allreadyAdd = True
                temp+="\n__{1}__ repousse la cible de **{0}** case{2}".format(becomeName.knockback,becomeName.name,["","s"][becomeName.knockback > 1])

    repEmb = discord.Embed(title = skil.name,color = user.color, description = desc+"\n__Statistiques :__\n"+temp)
    if skil.emoji[1] == "a":
        repEmb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.gif".format(getEmojiObject(skil.emoji)["id"]))
    else:
        repEmb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(skil.emoji)["id"]))

    if skil.become == None:
        if skil.range != AREA_MONO:
            ballerine, babie = [TYPE_ARMOR,TYPE_BOOST,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ,TYPE_RESURECTION,TYPE_HEAL],[TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE]
            for a in ballerine:
                if a == skil.type:
                    repEmb.add_field(name = "__Portée :__",value=visuArea(skil.range,wanted=ALLIES))
                    break

            for a in babie:
                if a == skil.type:
                    repEmb.add_field(name = "__Portée :__",value=visuArea(skil.range,wanted=ENNEMIS))
                    break

        if skil.area != AREA_MONO and skil.area != AREA_ALL_ALLIES and skil.area != AREA_ALL_ENEMIES and skil.area != AREA_ALL_ENTITES:
            if skil.type in [TYPE_ARMOR,TYPE_BOOST,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ,TYPE_RESURECTION,TYPE_HEAL]:
                repEmb.add_field(name = "__Zone d'effet :__",value=visuArea(skil.area,wanted=ALLIES,ranged=False))

            elif skil.type in [TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE]:
                repEmb.add_field(name = "__Zone d'effet :__",value=visuArea(skil.area,wanted=ENNEMIS,ranged=False))

            if skil.id == lunaSkill4.id:
                repEmb.add_field(name = "__Zone d'effet alternative :__",value=visuArea(AREA_CIRCLE_2,wanted=ENNEMIS,ranged=False))

    else:
        listArea,listName = [],[]
        for become in skil.become:
            if become.range not in listArea:
                listArea.append(become.range)
                listName.append([become.name])
            else:
                for cmpt in range(len(listArea)):
                    if listArea[cmpt] == become.range:
                        listName[cmpt].append(become.name)
                        break
        
        if len(listArea) == 1:
            repEmb.add_field(name = "__Portée :__",value=visuArea(listArea[0],wanted=ENNEMIS))
        else:
            for cmpt in range(len(listArea)):
                temporis = "__Portée :__\n("
                for name in range(len(listName[cmpt])):
                    temporis += listName[cmpt][name]
                    if name != len(listName[cmpt]) - 1:
                        temporis += ",\n"
                    else:
                        temporis += ")"

                repEmb.add_field(name = temporis,value=visuArea(listArea[cmpt],wanted=ENNEMIS))

        listArea,listName = [],[]
        for become in skil.become:
            if become.area not in listArea:
                listArea.append(become.area)
                listName.append([become.name])
            else:
                for cmpt in range(len(listArea)):
                    if listArea[cmpt] == become.area:
                        listName[cmpt].append(become.name)
                        break
        
        if len(listArea) == 1:
            repEmb.add_field(name = "__Zone d'effet :__",value=visuArea(listArea[0],wanted=ENNEMIS,ranged=False))
        elif len(listArea) != 0:
            for cmpt in range(len(listArea)):
                if listArea[cmpt] != AREA_MONO:
                    temporis = "__Zone d'effet :__\n("
                    for name in range(len(listName[cmpt])):
                        temporis += listName[cmpt][name]
                        if name != len(listName[cmpt]) - 1:
                            temporis += ",\n"
                        else:
                            temporis += ")"

                    repEmb.add_field(name = temporis,value=visuArea(listArea[cmpt],wanted=ENNEMIS,ranged=False))

    if skil.effect != [None]:
        for a in skil.effect:
            repEmb = infoEffect(a,user,repEmb,ctx)

    if skil.effectOnSelf != None:
        repEmb = infoEffect(skil.effectOnSelf,user,repEmb,ctx,True)

    if skil.invocation != None:
        repEmb = infoInvoc(findInvoc(skil.invocation),repEmb)
    
    if repEmb.__len__() > 6000:
        repEmb = discord.Embed(title = skil.name,color = user.color, description = desc+"\n__Statistiques :__\n"+temp+"\n\nCertaines infromations n'ont pas pu être affichées.")
        if skil.emoji[1] == "a":
            repEmb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.gif".format(getEmojiObject(skil.emoji)["id"]))
        else:
            repEmb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(skil.emoji)["id"]))

    return repEmb

def infoWeapon(weap : weapon, user : char ,ctx):
    repEmb = discord.Embed(title = unhyperlink(weap.name),color = user.color, description = f"Icone : {weap.emoji}")
    repEmb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(weap.emoji)["id"]))
    portee = weap.range
    if portee == 0:
        portee = "Mêlée"
    elif portee == 1:
        portee = "Distance"
    else:
        portee = "Longue distance"
    
    info = "\n__Cible :__ "
    if weap.target == ALLIES:
        info += "**Alliés**"
    else:
        info += "Ennemis"

    cible = weap.area  
    if cible == AREA_MONO:
        cible = "Monocible"
    else:
        cible = "Dégâts de zone"
    
    info += "\n__Zone d'effet :__ " + cible + f"\n__Statistique utilisée :__ {nameStats[weap.use]}"
    
    if weap.onArmor != 1 and weap.type == TYPE_DAMAGE:
        info = f"\n__Dégâts sur armure :__ **{int(weap.onArmor*100)}**%"

    element = ""
    if weap.affinity != None:
        element = f"\n__Affinité :__ {elemEmojis[weap.affinity]} {elemNames[weap.affinity]}"

    if weap.repetition > 1:
        nbShot = " x{0}".format(weap.repetition)
    else:
        nbShot = ""

    repEmb.add_field(name = "__Informations Principales :__",value = f"__Position :__ {portee}\n__Portée :__ {weap.effectiveRange}\n__Type :__ {tablTypeStr[weap.type]}\n__Puissance :__ {weap.power}{nbShot}\n__Précision par défaut :__ {weap.sussess}%\n<:empty:866459463568850954>")
    repEmb.add_field(name="__Statistiques secondaires :__",value=f'{element}{info}\n<:empty:866459463568850954>',inline=True)
    bonus,malus = "",""
    stats = weap.allStats()+[weap.resistance,weap.percing,weap.critical]
    names = nameStats+nameStats2
    for a in range(len(stats)):
        if stats[a] > 0:
            bonus += f"{names[a]} : +{stats[a]}\n"
        elif stats[a] < 0:
            malus += f"{names[a]} : {stats[a]}\n"

    if bonus != "":
        repEmb.add_field(name ="__Bonus de statistiques :__",value = bonus+"\n<:empty:866459463568850954>",inline = False)
    if malus != "":
        repEmb.add_field(name="__Malus de statistiques :__",value = malus+"\n<:empty:866459463568850954>", inline = False)

    
    ballerine, babie = [TYPE_ARMOR,TYPE_BOOST,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ,TYPE_RESURECTION,TYPE_HEAL],[TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE]
    for a in ballerine:
        if a == weap.type:
            repEmb.add_field(name = "__Portée :__",value=visuArea(weap.effectiveRange,wanted=ALLIES))
            break

    for a in babie:
        if a == weap.type:
            repEmb.add_field(name = "__Portée :__",value=visuArea(weap.effectiveRange,wanted=ENNEMIS))
            break

    if weap.area != AREA_MONO and weap.area != AREA_ALL_ALLIES and weap.area != AREA_ALL_ENEMIES and weap.area != AREA_ALL_ENTITES:
        ballerine, babie = [TYPE_ARMOR,TYPE_BOOST,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ,TYPE_RESURECTION,TYPE_HEAL],[TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE]
        for a in ballerine:
            if a == weap.type:
                repEmb.add_field(name = "__Zone d'effet :__",value=visuArea(weap.area,wanted=ALLIES,ranged=False))
                break

        for a in babie:
            if a == weap.type:
                repEmb.add_field(name = "__Zone d'effet :__",value=visuArea(weap.area,wanted=ENNEMIS,ranged=False))
                break


    if weap.effect != None:
        repEmb.add_field(name="<:empty:866459463568850954>\n__Effet Passif :__",value = "Cette arme accorde un effet passif à son porteur",inline=False)
        infoEffect(weap.effect,user,repEmb,ctx)

    if weap.effectOnUse != None:
        repEmb.add_field(name="<:empty:866459463568850954>\n__Effet à l'utilisation :__",value = "Cette arme donne un effet à la cible",inline=False)
        infoEffect(weap.effectOnUse,user,repEmb,ctx)
    return repEmb

def infoStuff(stuff : stuff, user : char ,ctx):
    weap = stuff
    temp =""
    if weap.type == 0:
        temp="Accessoire"
    elif weap.type == 1:
        temp="Haut"
    else:
        temp="Chaussures"

    element = ""
    if weap.affinity != None:
        element = f"\nAffinité : {elemEmojis[weap.affinity]} {elemNames[weap.affinity]}"

    repEmb = discord.Embed(title = unhyperlink(weap.name),color = user.color, description = f"Niveau : {weap.minLvl}\nType : {temp}\nOrientation : {weap.orientation}{element}")
    repEmb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(weap.emoji)["id"]))

    bonus,malus = "",""
    stats = weap.allStats()+[weap.resistance,weap.percing]
    names = nameStats+nameStats2
    for a in range(len(stats)):
        if stats[a] > 0:
            bonus += f"{names[a]} : +{stats[a]}\n"
        elif stats[a] < 0:
            malus += f"{names[a]} : {stats[a]}\n"

    negative = [weap.negativeHeal,weap.negativeBoost,weap.negativeShield,weap.negativeDirect,weap.negativeIndirect]
    for stat in range(len(negative)):
        if negative[stat] > 0:
            malus += "{0} : {1}\n".format(["Soins","Boosts et Malus","Armures et Mitigation","Dégâts directs","Dégâts indirects"][stat],negative[stat]*-1)
        elif negative[stat] < 0:
            bonus += "{0} : {1}\n".format(["Soins","Boosts et Malus","Armures et Mitigation","Dégâts directs","Dégâts indirects"][stat],negative[stat]*-1)

    if bonus != "":
        repEmb.add_field(name ="__Bonus de statistiques :__",value = bonus,inline = True)
    if malus != "":
        repEmb.add_field(name="__Malus de statistiques :__",value = malus, inline = True)

    if weap.effect != None:
        infoEffect(weap.effect,user,repEmb,ctx)
        
    return repEmb

def infoOther(other : other, user : char):
    weap = other
    repEmb = discord.Embed(title = weap.name,color = user.color, description = f"Icone : { weap. emoji}")
    repEmb.add_field(name="Description :",value = weap.description)

    return repEmb

def userMajStats(user : char, tabl : list):
    """What ?"""
    user.strength,user.endurance,user.charisma,user.agility,user.precision,user.intelligence,user.magie = tabl[0],tabl[1],tabl[2],tabl[3],tabl[4],tabl[5],tabl[6]
    return user

def restats(user : char):
    """Function for restat a user"""
    stats = user.allStats()
    allMax = [maxStrength,maxEndur,maxChar,maxAgi,maxPreci,maxIntel,maxMagie]
    for a in range(0,len(stats)):
        stats[a] = round(allMax[a][user.aspiration]*0.1+allMax[a][user.aspiration]*0.9*user.level/50)

    user.points = user.level
    user.majorPointsCount = user.stars
    user.bonusPoints = [0,0,0,0,0,0,0]
    user.majorPoints = [0,0,0,0,0,0,0]+[0,0,0]+[0,0,0,0,0]

    return userMajStats(user,stats)

def silentRestats(user : char):
    """Function for restat a user without reset the bonus points"""
    stats = user.allStats()
    allMax = [maxStrength,maxEndur,maxChar,maxAgi,maxPreci,maxIntel,maxMagie]
    for a in range(0,len(stats)):
        stats[a] = round(allMax[a][user.aspiration]*0.1+allMax[a][user.aspiration]*0.9*user.level/50)+user.bonusPoints[a]

    return userMajStats(user,stats)

async def addExpUser(bot : discord.Client, guild, path : str,ctx,exp = 3,coins = 0):
    user = loadCharFile(path)

    if user.level < 55:
        user.exp = user.exp + exp
    else:
        user.exp = 0
    user.currencies = user.currencies + coins

    upLvl = (user.level-1)*50+30

    if user.exp >= upLvl:
        user.points = user.points + 1

        temp = user.allStats()
        up = [0,0,0,0,0,0,0]
        tabl = [maxStrength,maxEndur,maxChar,maxAgi,maxPreci,maxIntel,maxMagie]
        stats = user.allStats()
        for a in range(0,len(stats)):
            stats[a] = round(tabl[a][user.aspiration]*0.1+tabl[a][user.aspiration]*0.9*user.level/50+user.bonusPoints[a])
            temp[a] = round(tabl[a][user.aspiration]*0.1+tabl[a][user.aspiration]*0.9*(user.level+1)/50+user.bonusPoints[a])
            up[a] = temp[a]-stats[a]

        user.strength, user.endurance, user.charisma, user.agility, user.precision, user.intelligence, user.magie = temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6]

        ballerine = await bot.fetch_user(user.owner)
        level = str(user.level+1) + ["","<:littleStar:925860806602682369>{0}".format(user.stars)][user.stars>0]
        lvlEmbed = discord.Embed(title = f"__Niveau supérieur__",color = user.color,description = f"Le personnage de {ballerine.mention} ({user.name}) est passé au niveau {level} !\n\nForce : {user.strength} (+{up[0]})\nEndurance : {user.endurance} (+{up[1]})\nCharisme : {user.charisma} (+{up[2]})\nAgilité : {user.agility} (+{up[3]})\nPrécision : {user.precision} (+{up[4]})\nIntelligence : {user.intelligence} (+{up[5]})\nMagie : {user.magie} (+{up[6]})\n\nVous avez {user.points} bonus à répartir en utilisant la commande \"points\".")
        
        if (user.level+1) % 5 == 0:
            unlock = ""
            listUnlock = []
            for stuffy in user.stuffInventory:
                if stuffy.minLvl == user.level+1:
                    listUnlock.append(stuffy)

            if len(listUnlock) <= 10:
                for stuffy in listUnlock:
                    unlock += "{0} {1}\n".format(stuffy.emoji,stuffy.name)
            else:
                for stuffy in listUnlock[:10]:
                    unlock += "{0} {1}\n".format(stuffy.emoji,stuffy.name)
                unlock += "Et {0} autre(s)".format(len(listUnlock)-10)

            if unlock != "":
                lvlEmbed.add_field(name="<:empty:866459463568850954>\n__Vous pouvez désormais équiper les objets de votre inventaire suivants :__",value=unlock)
        
        if guild.bot != 0:
            await bot.get_guild(guild.id).get_channel(guild.bot).send(embed = lvlEmbed)
        else:
            await ctx.channel.send(embed = lvlEmbed)

        user.exp = user.exp - (user.level)*50+30
        user.level = user.level + 1

    saveCharFile(user=user)
    return user

def getChoisenSelect(select : dict, value : str):
    trouv = False
    temp = copy.deepcopy(select)
    for a in temp["options"]:
        if a["value"] == value:
            trouv=True
            a["default"] = True
    if trouv:
        temp["disabled"] = True
    return temp

async def downloadAllHeadGearPng(bot : discord.Client, msg = None, lastTime = None):
    listEmojiHead = stuffDB.getAllHeadGear()
    listDir = os.listdir("./data/images/headgears/")
    num,cmpt = len(listEmojiHead),0
    for a in listEmojiHead:
        emojiObject = getEmojiInfo(a)
        if emojiObject[0] + ".png" not in listDir:
            guildStuff = stuffIconGuilds

            emoji_2 = None
            for b in guildStuff:
                try:
                    guild = await bot.fetch_guild(b)
                    emoji_2 = await guild.fetch_emoji(emojiObject[1])
                except:
                    pass

            if emoji_2 != None:
                image = requests.get(emoji_2.url,stream=True)
                image.raw.decode_content=True
                open(f"./data/images/headgears/{emojiObject[0]}.png","wb").write(image.content)
                image = Image.open(f"./data/images/headgears/{emojiObject[0]}.png")
                image = image.resize((70,70))
                image.save(f"./data/images/headgears/{emojiObject[0]}.png")
                customIconDB.addHeadGearImageFiles(stuffDB.getIdFromEmoji(a,"gear"),f"{emojiObject[0]}.png")
                print(emojiObject[0] + " téléchargé")
            else:
                print(emojiObject[0] + " non trouvé")

        if msg != None:
            cmpt += 1
            now = datetime.datetime.now().second
            if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
                lastTime = now
                await msg.edit(embed = discord.Embed(title="l!admin resetCustomEmoji",description="Téléchargement des images d'accessoires ({0}%)".format(round(cmpt/num*100,1))))

async def downloadAllWeapPng(bot : discord.Client, msg=None, lastTime=None):
    listEmojiHead = stuffDB.getAllWeap()
    listDir = os.listdir("./data/images/weapons/")
    num,cmpt = len(listEmojiHead+etInkBases+etInkLines),0
    for a in listEmojiHead:
        emojiObject = getEmojiInfo(a)
        if emojiObject[0] + ".png" not in listDir:
            guildStuff = weaponIconGuilds

            emoji_2 = None
            for b in guildStuff:
                try:
                    guild = await bot.fetch_guild(b)
                    emoji_2 = await guild.fetch_emoji(emojiObject[1])
                except:
                    pass

            if emoji_2 != None:
                image = requests.get(emoji_2.url,stream=True)
                image.raw.decode_content=True
                open(f"./data/images/weapons/{emojiObject[0]}.png","wb").write(image.content)
                image = Image.open(f"./data/images/weapons/{emojiObject[0]}.png")
                background = Image.new("RGBA",(120,120),(0,0,0,0))
                image = image.resize((100,100))
                background.paste(image,(10,10))
                background = background.rotate(30)

                background.save(f"./data/images/weapons/{emojiObject[0]}.png")
                customIconDB.addWeapImageFiles(stuffDB.getIdFromEmoji(a,"weapon"),f"{emojiObject[0]}.png")
                print(emojiObject[0] + " téléchargé")
            else:
                print(emojiObject[0] + " non trouvé")

        if msg != None:
            cmpt += 1
            now = datetime.datetime.now().second
            if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
                lastTime = now
                await msg.edit(embed = discord.Embed(title="l!admin resetCustomEmoji",description="Téléchargement des images d'armes ({0}%)".format(round(cmpt/num*100,1))))

    for a in etInkBases+etInkLines:
        emojiObject = getEmojiInfo(a)
        if emojiObject[0] + ".png" not in listDir:
            guildStuff = weaponIconGuilds

            emoji_2 = None
            for b in guildStuff:
                try:
                    guild = await bot.fetch_guild(b)
                    emoji_2 = await guild.fetch_emoji(emojiObject[1])
                except:
                    pass

            if emoji_2 != None:
                image = requests.get(emoji_2.url,stream=True)
                image.raw.decode_content=True
                open(f"./data/images/weapons/{emojiObject[0]}.png","wb").write(image.content)
                image = Image.open(f"./data/images/weapons/{emojiObject[0]}.png")
                background = Image.new("RGBA",(120,120),(0,0,0,0))
                image = image.resize((100,100))
                background.paste(image,(10,10))
                background = background.rotate(30)

                background.save(f"./data/images/weapons/{emojiObject[0]}.png")
                print(emojiObject[0] + " téléchargé")
            else:
                print(emojiObject[0] + " non trouvé")

        if msg != None:
            cmpt += 1
            now = datetime.datetime.now().second
            if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
                lastTime = now
                await msg.edit(embed = discord.Embed(title="l!admin resetCustomEmoji",description="Téléchargement des images d'armes ({0}%)".format(round(cmpt/num*100,1))))
    
    if not(os.path.exists("./data/images/weapons/akifaux.png")):
        image = requests.get("https://cdn.discordapp.com/emojis/887334842595942410.png?v=1",stream=True)
        image.raw.decode_content=True
        open(f"./data/images/weapons/akifaux.png","wb").write(image.content)
        image = Image.open(f"./data/images/weapons/akifaux.png")
        background = Image.new("RGBA",(120,120),(0,0,0,0))
        image = image.resize((100,100))
        background.paste(image,(10,10))
        background = background.rotate(30)
        background.save(f"./data/images/weapons/akifaux.png")
        print("akifaux téléchargé")

async def downloadAllIconPng(bot : discord.Client):
    listEmojiHead = emoji.icon
    listDir = os.listdir("./data/images/char_icons/")
    for a in (1,2,4):
        for b in range(0,len(listEmojiHead[a])):
            emojiObject = getEmojiInfo(listEmojiHead[a][b])
            if emojiObject[0] + ".png" not in listDir:
                guildStuff = [862320563590529056,615257372218097691]

                emoji_2 = None
                for c in guildStuff:
                    try:
                        guild = await bot.fetch_guild(c)
                        emoji_2 = await guild.fetch_emoji(emojiObject[1])
                    except:
                        pass

                if emoji_2 != None:
                    image = requests.get(emoji_2.url,stream=True)
                    image.raw.decode_content=True
                    open(f"./data/images/char_icons/{emojiObject[0]}.png","wb").write(image.content)
                    image = Image.open(f"./data/images/char_icons/{emojiObject[0]}.png")
                    background = Image.new("RGBA",(145,145),(0,0,0,0))
                    image = image.resize((128,128))
                    background.paste(image,((145-128)//2,(145-128)//2))
                    background.save(f"./data/images/char_icons/{emojiObject[0]}.png")
                    customIconDB.addIconFiles(a,b,f"{emojiObject[0]}.png")
                    print(emojiObject[0] + " téléchargé")
                else:
                    print(emojiObject[0] + " non trouvé")

async def makeCustomIcon(bot : discord.Client, user : char):
    accessoire = Image.open("./data/images/headgears/"+customIconDB.getAccFile(user))
    # Paramètres de l'accessoire ----------------------------------
    if user.apparaAcc == None:
        pos = user.stuff[0].position
    else:
        pos = user.apparaAcc.position
    position = []

    if (user.apparaAcc == None and user.stuff[0].id == lentille.id) or (user.apparaAcc != None and user.apparaAcc.id == lentille.id):
        accessoire.close()
        accessoire = Image.new("RGBA",(1,1),(0,0,0,0))

    position = []

    # Récupération de l'icone de base -----------------------------
    tabl = [["./data/images/char_icons/empty_squid.png","./data/images/char_icons/baseIka.png"],["./data/images/char_icons/empty_octo.png","./data/images/char_icons/baseTako.png"]]
    background = Image.open(tabl[user.species-1][1])
    background2 = None

    if pos == 6:                                 # Behind
        background2 = Image.new("RGBA",background.size,(0,0,0,0))
        if user.species == 2:
            accessoire = accessoire.resize((round(accessoire.size[0]*1.3),accessoire.size[1]))
        position = (round(background.size[0]/2-accessoire.size[0]/2),-10)
        background2.paste(accessoire,position,accessoire)
        accessoire.close()

    if user.stars > 0:
        print("printy")
        if background2 == None:
            background2 = Image.new("RGBA",background.size,(0,0,0,0))
        cmpt = 0
        while cmpt < user.stars:
            litStar = Image.open("./data/images/char_icons/littleStar.png")
            litStar = litStar.resize((38,38))
            background2.paste(litStar,(33*(cmpt%4)+5,38*(cmpt//4)),litStar)
            litStar.close()
            cmpt += 1

    pixel = background.load()
    layer = Image.open(tabl[user.species-1][0])

    colorToUse = user.colorHex.replace("0x","#")
    if colorToUse == "None":
        if user.color != black:
            colorToUse = hex(user.color).replace("0x","#")
        else:
            colorToUse = "#000000"
    baseUserColor = ImageColor.getcolor(colorToUse, "RGB")
    baseTemp = [baseUserColor[0],baseUserColor[1],baseUserColor[2]]
    for x in range(0,background.size[0]):
        for y in range(0,background.size[1]):
            if pixel[x,y] != (0,0,0,0):
                color = list(pixel[x,y])
                for cmpt in (0,1,2):
                    color[cmpt] = color[cmpt]-121
                    baseTemp[cmpt] = min(baseUserColor[cmpt] + color[cmpt],255)

                background.putpixel([x,y],tuple(baseTemp))

    background.paste(layer,[0,0],layer)
    background.paste(layer,[0,0],layer)

    if pos == 6 or user.stars > 0:
        background2.paste(background,[0,0],background)
        background = background2

    # Récupération de l'icone de l'accessoire
    if pos == 0:                                            # Casques
        if user.species == 2:
            accessoire = accessoire.resize((round(accessoire.size[0]*1.3),accessoire.size[1]))
        position = (round(background.size[0]/2-accessoire.size[0]/2),-10)
    elif pos == 1:                                          # Boucles d'oreilles
        accessoire = accessoire.resize((round(accessoire.size[0]*0.8),round(accessoire.size[1]*0.8)))
        if user.species==1:
            position = (0,round(background.size[1]/2)-5)
        else:
            position = (3,round(background.size[1]/2)-5)
    elif pos == 2:                                          # Colliers
        accessoire = accessoire.resize((round(accessoire.size[0]*1.2),round(accessoire.size[1]*0.7)))
        position = (round(background.size[0]/2-accessoire.size[0]/2),round(background.size[1]/2+20))
    elif pos == 3:                                          # Barettes
        accessoire = accessoire.resize((round(accessoire.size[0]*0.8),round(accessoire.size[1]*0.8)))
        accessoire = accessoire.rotate(30)
        if user.species==1:
            position = (round(background.size[0]*0.25-accessoire.size[0]/2+8),13)
        else:
            position = (round(background.size[0]*0.25-accessoire.size[0]/2+3),7)
    elif pos == 4:                                          # Boucliers
        position = (round(background.size[0]*0.20-accessoire.size[0]/2),75)
    elif pos == 5:                                          # Masques
        accessoire = accessoire.resize((round(accessoire.size[0]*1.2),round(accessoire.size[1]*0.7)))
        position = (round(background.size[0]/2-accessoire.size[0]/2),round(background.size[1]/2+10))

    # Collage de l'accessoire
    if pos != 6:
        background.paste(accessoire,position,accessoire)
        accessoire.close()


    # Récupération de l'icone de l'arme
    if (user.apparaWeap != None and user.apparaWeap.id in eternalInkWeaponIds) or (user.apparaWeap == None and user.weapon.id in eternalInkWeaponIds):

        if user.apparaWeap != None:
            toBase = getEmojiObject(user.apparaWeap.emoji)["name"]
        else:
            toBase = getEmojiObject(user.weapon.emoji)["name"]
        line = Image.open("./data/images/weapons/Line{0}.png".format(toBase))
        base = Image.open("./data/images/weapons/Base{0}.png".format(toBase))

        pixel = base.load()
        baseTemp = [baseUserColor[0],baseUserColor[1],baseUserColor[2]]
        for x in range(0,base.size[0]):
            for y in range(0,base.size[1]):
                if pixel[x,y] != (0,0,0,0):
                    color = list(pixel[x,y])
                    for cmpt in (0,1,2):
                        color[cmpt] = color[cmpt]-143
                        baseTemp[cmpt] = min(baseUserColor[cmpt] + color[cmpt],255)
                    base.putpixel([x,y],tuple(baseTemp))
        base.paste(line,[0,0],line)
        weapon = base
    elif (user.apparaWeap == None and user.weapon.id == mainLibre.id) or (user.apparaWeap != None and user.apparaWeap.id == mainLibre.id):
        weapon = Image.new("RGBA",(1,1),(0,0,0,0))

    elif "./data/images/weapons/"+customIconDB.getWeaponFile(user) != "./data/images/weapons/akifauxgif.png":
        weapon = Image.open("./data/images/weapons/"+customIconDB.getWeaponFile(user))
    else:
        weapon = Image.open("./data/images/weapons/akifaux.png")
    weapon = weapon.resize((120,120))

    if (user.apparaWeap == None and user.weapon.needRotate == False) or (user.apparaWeap != None and user.apparaWeap.needRotate == False):
        weapon = weapon.rotate(-30)

    # Collage de l'arme
    background.paste(weapon,(55,40),weapon)
    weapon.close()

    # Collage de l'élément
    element = Image.open("./data/images/elemIcon/"+getEmojiObject(elemEmojis[user.element])["name"]+".png")
    background.paste(element,(0,90),element)
    element.close()

    imgByteArr = io.BytesIO()
    background.save(imgByteArr, format="png")
    background = imgByteArr.getvalue()

    iconGuildList = []
    if os.path.exists("../Kawi/"):
        iconGuildList = ShushyCustomIcons
    else:
        iconGuildList = LenaCustomIcons

    if not(customIconDB.haveCustomIcon(user)):
        for icGuild in iconGuildList:
            icGuild = await bot.fetch_guild(icGuild)

            if len(icGuild.emojis) < 50:
                new_icon = await icGuild.create_custom_emoji(name=remove_accents(user.name),image=background)
                customIconDB.editCustomIcon(user,new_icon)
                print(f"Icone de {user.name} bien crée !")
                break

    else:
        customId = getEmojiObject(customIconDB.getCustomIcon(user))["id"]
        custom = None
        for icGuild in iconGuildList:
            icGuild = await bot.fetch_guild(icGuild)
            try:
                custom = await icGuild.fetch_emoji(customId)
            except:
                pass

            if custom != None:
                await custom.delete()
                new_icon = await icGuild.create_custom_emoji(name=remove_accents(user.name),image=background)
                customIconDB.editCustomIcon(user,new_icon)
                print(f"Icone de {user.name} bien mis à jour !")
                break

async def getUserIcon(bot : discord.Client,user : char):
    """Function for get the user custom icon\nIf a (re)make is needed, remake the icon"""
    fun = random.randint(0,9999)
    if fun == 666:
        return "<a:lostSilver:917783593441456198>"

    try:
        if customIconDB.isDifferent(user):
            await makeCustomIcon(bot,user)
        
        if customIconDB.haveCustomIcon(user):
            return customIconDB.getCustomIcon(user)
    except:
        return "<:LenaWhat:760884455727955978>"

def infoInvoc(invoc : invoc, embed : discord.Embed):
    rep = f"__Aspiration de l'invocation :__ {aspiEmoji[invoc.aspiration]} {inspi[invoc.aspiration]}\n__Elément de l'invocation :__ {elemEmojis[invoc.element]} {elemNames[invoc.element]}\n__Description :__\n{invoc.description}\n\n__Statistique principale :__ **{nameStats[invoc.weapon.use]}**\n\n**__Statistiques :__**\n*\"Invoc\" est un raccourci pour \"Statistique de l'Invocateur\"*\n"

    stats = invoc.allStats()+[invoc.resistance,invoc.percing,invoc.critical]
    names = nameStats+nameStats2
    for a in range(0,len(stats)):
        if type(stats[a]) == list:
            if stats[a][0] == PURCENTAGE:
                rep += f"\n__{names[a]} :__ Invoc x{stats[a][1]}"
            elif stats[a][0] == HARMONIE :
                 rep += f"\n__{names[a]} :__ Invoc : Harmonie"
        else:
            rep += f"\n__{names[a]} :__ {stats[a]}"

    ranged = ["Mêlée","Distance","Longue Distance"][invoc.weapon.range]
    rep += f"\n\n__Arme et compétences :__\n\n{invoc.weapon.emoji} {invoc.weapon.name} ({ranged})"
    for a in invoc.skills:
        if type(a) == skill:
            ranged=["Monocible","Zone"][int(a.area != AREA_MONO)]
            rep += f"\n{a.emoji} {a.name} ({tablTypeStr[a.type]}, {ranged})"

    embed.add_field(name="<:empty:866459463568850954>\n__"+invoc.name+"__",value=rep,inline = False)
    return embed

def infoAllie(allie : tmpAllie):
    var = ""
    if allie.variant:
        var = "Cet allié temporaire est une variante d'un autre allié temporaire\n\n"
    rep = f"{var}__Aspiration :__ {inspi[allie.aspiration]}\n__Element :__ {elemEmojis[allie.element]} {elemNames[allie.element]}\n__Description :__\n{allie.description}"
    allMaxStats, accStats, dressStats, flatsStats = [maxStrength,maxEndur,maxChar,maxAgi,maxPreci,maxIntel,maxMagie],allie.stuff[0].allStats(),allie.stuff[1].allStats(),allie.stuff[2].allStats()
    stats = ""
    for a in range(0,len(allMaxStats)):
        temp,tempi = allMaxStats[a][allie.aspiration],accStats[a]+dressStats[a]+flatsStats[a]
        stats += f"__{nameStats[a]}__ : {temp} ({tempi})\n"

    stats2 = ""
    accStats = [allie.stuff[0].resistance,allie.stuff[0].percing,allie.stuff[0].critical]
    dressStats = [allie.stuff[1].resistance,allie.stuff[1].percing,allie.stuff[1].critical]
    flatsStats = [allie.stuff[2].resistance,allie.stuff[2].percing,allie.stuff[2].critical]
    statsPlusName = nameStats2
    for num in range(3):
        summation = accStats[num] + dressStats[num] + flatsStats[num]
        if summation > 0:
            stats2 += f"__{statsPlusName[num]}__ : +{summation}\n"
        else:
            stats2 += f"__{statsPlusName[num]}__ : {summation}\n"


    accStats = [allie.stuff[0].negativeHeal,allie.stuff[0].negativeBoost,allie.stuff[0].negativeShield,allie.stuff[0].negativeDirect,allie.stuff[0].negativeIndirect]
    dressStats = [allie.stuff[1].negativeHeal,allie.stuff[1].negativeBoost,allie.stuff[1].negativeShield,allie.stuff[1].negativeDirect,allie.stuff[1].negativeIndirect]
    flatsStats = [allie.stuff[2].negativeHeal,allie.stuff[2].negativeBoost,allie.stuff[2].negativeShield,allie.stuff[2].negativeDirect,allie.stuff[2].negativeIndirect]
    statsPlusName = ["Soins","Bonus/Malus","Armure","Dégâts directs","Dégâts indirect"]
    stats2 += "\n"
    for num in range(5):
        summation = accStats[num]*-1 + dressStats[num]*-1 + flatsStats[num]*-1
        if summation > 0:
            stats2 += f"__{statsPlusName[num]}__ : +{summation}\n"
        else:
            stats2 += f"__{statsPlusName[num]}__ : {summation}\n"


    rep += f"\n\n__**Arme et compétences** :__\n{allie.weapon.emoji} {allie.weapon.name}\n"
    for a in allie.skills:
        if type(a) == skill:
            rep += f"\n{a.emoji} {a.name}"

    rep += f"\n\n__**Equipement :**__\n__Accessoire__ : {allie.stuff[0].emoji} {allie.stuff[0].name}\n__Vêtements__ : {allie.stuff[1].emoji} {allie.stuff[1].name}\n__Chaussures__ : {allie.stuff[2].emoji} {allie.stuff[2].name}"

    embed = discord.Embed(title="__Allié temporaire : "+allie.name+"__",color=allie.color,description=rep+"\n<:empty:866459463568850954>")
    embed.add_field(name="__**Statistiques au niveau 50 :**__",value=stats)
    embed.add_field(name="__**Statistiques secondaires :**__",value=stats2)
    if allie.icon[1] == "a":
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.gif".format(getEmojiObject(allie.icon)["id"]))
    else:
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(allie.icon)["id"]))

    if allie.changeDict != None:
        temp = ""
        changeSkill = ""
        toSkill = ""
        for changeDictCell in allie.changeDict:
            if changeDictCell["changeWhat"] == 0:               # Change Skills
                for num in range(len(changeDictCell["to"])):
                    for skillNum in range(len(allie.skills)):
                        if allie.skills[skillNum].id == changeDictCell["change"][num].id:
                            toSkill += changeDictCell["to"][num].emoji+" __"+changeDictCell["to"][num].name+"__"
                            changeSkill += allie.skills[skillNum].emoji+" __"+allie.skills[skillNum].name+"__"
                            if num != len(changeDictCell["to"])-1:
                                changeSkill+= ", "
                                toSkill += ", "
                            break
            
            ses,s = "sa",""
            if len(changeDictCell["change"]) > 1:
                ses,s = "ses","s"
            temp += "À partir du niveau {3}, cet allié temporaire a {0}% de chance de voir {4} compétence{5} suivante{5} :\n{1}\nremplacé{5} par :\n{2}\n".format(changeDictCell["proba"],changeSkill,toSkill,changeDictCell["level"],ses,s)
        embed.add_field(name="<:empty:866459463568850954>\n__Variations aléatoires :__",value=temp,inline=False)

    if allie.unlock == None:
        embed.add_field(name = "<:empty:866459463568850954>\n__Aventure : Condition d'utilisation__",value="Vous pouvez rajouter cet allié temporaire à votre escouade dès le début")
    elif allie.unlock != False:
        tempTabl, temp = [], ""
        for letter in allie.unlock+"|":
            if letter == "|":
                tempTabl.append(temp)
                temp = ""
            else:
                temp.append(letter)
        embed.add_field(name = "<:empty:866459463568850954>\n__Aventure : Condition d'utilisation__",value="Cet allié temporaire ne peut être ajouté à votre escouade qu'après la mission \"{0} - {1}\"".format(tempTabl[0],tempTabl[1]))
    else:
        embed.add_field(name = "<:empty:866459463568850954>\n__Aventure : Condition d'utilisation__",value="Cet allié temporaire ne peut être ajouté à votre escouade")

    return embed

def infoEnnemi(ennemi : octarien):
    rep = f"__Aspiration :__ {inspi[ennemi.aspiration]}\n__Niveau Minimum :__ {ennemi.baseLvl}\n__Element :__ {elemEmojis[ennemi.element]} {elemNames[ennemi.element]}\n\n__Description :__\n{ennemi.description}\n\n__**Statistiques au niveau 50 :**__\n*Entre parenthèse : Les bonus donnés par l'équipement*\n"
    allMaxStats, accStats, dressStats, flatsStats,weapStats = ennemi.allStats(),ennemi.stuff[0].allStats(),ennemi.stuff[1].allStats(),ennemi.stuff[2].allStats(),ennemi.weapon.allStats()
    for a in range(0,len(allMaxStats)):
        temp,tempi = allMaxStats[a],accStats[a]+dressStats[a]+flatsStats[a]+weapStats[a]
        rep += f"\n__{nameStats[a]}__ : {temp} ({tempi})"

    rep += f"\n\n__**Arme et compétences** :__\n{ennemi.weapon.emoji} {ennemi.weapon.name}\n"
    for a in ennemi.skills:
        if type(a) == skill:
            rep += f"\n{a.emoji} {a.name}"

    embed = discord.Embed(title="__Ennemis : "+ennemi.name+"__",color=ennemi.color,description=rep)
    if ennemi.icon[1] == "a":
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.gif".format(getEmojiObject(ennemi.icon)["id"]))
    else:
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(ennemi.icon)["id"]))
    return embed

def getAutoStuff(object: stuff, user: char):
    if user.level//5 == object.minLvl//5 or object.minLvl == 50:
        return object
    else:
        tablAllStats = object.allStats()+[object.resistance,object.percing,object.critical]+[object.negativeHeal*-1,object.negativeBoost*-1,object.negativeShield*-1,object.negativeDirect*-1,object.negativeIndirect*-1]
        
        for comp in user.skills:
            if type(comp) == skill and comp.use not in [None,HARMONIE]:
                tablAllStats[comp.use] += 1
        dictList = []
        for cmpt in range(len(tablAllStats)):
            dictList.append({"Stats":cmpt,"Value":tablAllStats[cmpt]})

        dictList.sort(key=lambda ballerine: ballerine["Value"],reverse=True)
        dictList = dictList[0:3]

        statsMaxPlace = []
        for a in dictList:
            if a["Value"] > 0:
                statsMaxPlace.append(a["Stats"])

        if type(user) == char:
            tablToSee = copy.deepcopy(user.stuffInventory)
        elif type(user) == tmpAllie:
            tablToSee = copy.deepcopy(stuffs)


        def getSortValue(obj:stuff,statsMaxPlace=statsMaxPlace,aff=False):
            if obj.effect != None and findEffect(obj.effect).id == summonerMalus.id:
                return -maxsize
            objStats = obj.allStats()+[obj.resistance,obj.percing,obj.critical]+[obj.negativeHeal*-1,obj.negativeBoost*-1,obj.negativeShield*-1,obj.negativeDirect*-1,obj.negativeIndirect*-1]
            value = []
            for a in statsMaxPlace:
                value.append(objStats[a])

            for a in range(len(value)):
                if value[a] <= 0:
                    if a == 0:
                        for b in value:
                            b = 0
                        break
                    elif a == 1:
                        for b in value:
                            b = b*0.75
                        break
                    elif a == 2:
                        for b in value:
                            b = b*0.5
                        break
            temp = 0
            for a in value:
                temp += a
            if aff:
                print(obj.name, temp)
            return temp

        for stuffy in tablToSee[:]:
            if (stuffy.minLvl > user.level or stuffy.type != object.type or getSortValue(stuffy) <= 0) and (object.minLvl//5 >= stuffy.minLvl//5):
                tablToSee.remove(stuffy)
            elif (stuffy.minLvl > user.level or stuffy.type != object.type or getSortValue(stuffy) <= 0) and (object.minLvl//5 <= stuffy.minLvl//5):
                tablToSee.remove(stuffy)

        if len(tablToSee) > 0:
            tablToSee.sort(key=lambda ballerine:getSortValue(ballerine),reverse=True)
            return tablToSee[0]
        else:
            return [bbandeau,bshirt,bshoes][object.type]

async def downloadElementIcon(bot : discord.Client):
    listEmojiHead = elemEmojis
    listDir = os.listdir("./data/images/elemIcon/")
    for b in range(len(listEmojiHead)):
        emojiObject = getEmojiInfo(listEmojiHead[b])
        if emojiObject[0] + ".png" not in listDir:
            guildStuff = [615257372218097691]

            emoji_2 = None
            for c in guildStuff:
                try:
                    guild = await bot.fetch_guild(c)
                    emoji_2 = await guild.fetch_emoji(emojiObject[1])
                except:
                    pass

            if emoji_2 != None:
                image = requests.get(emoji_2.url,stream=True)
                image.raw.decode_content=True
                open(f"./data/images/elemIcon/{emojiObject[0]}.png","wb").write(image.content)
                image = Image.open(f"./data/images/elemIcon/{emojiObject[0]}.png")
                image = image.resize((60,60))
                image.save(f"./data/images/elemIcon/{emojiObject[0]}.png")
                print(emojiObject[0] + " téléchargé")
            else:
                print(emojiObject[0] + " non trouvé")

async def getRandomStatsEmbed(bot : discord.Client,team : List[classes.char], text = "Chargement..."):
    desc = ""
    whatRandomStat = random.randint(0,len(tablAdd)-1)
    randomStat = tablAdd[whatRandomStat]
    rdm2 = ["max","total"][random.randint(0,1)]

    listDict = []
    for perso in team:
        if type(perso) == char:
            value = aliceStatsDb.getUserStats(perso,rdm2+randomStat)
            if value > 0:
                listDict.append({"name" : perso.name,"value" : value,"char" : perso})

    if len(listDict) > 0:
        if len(listDict) == 1:
            choisen = listDict[0]
        else:
            choisen = listDict[random.randint(0,len(listDict)-1)]

        if rdm2 == "max":
            msgMax = [randomMaxDmg,randomMaxKill,randomMaxRes,randomMaxTank,randomMaxHeal,randomMaxArmor,randomMaxSupp]
        else:
            msgMax = [randomTotalDmg,randomTotalKill,randomTotalRes,randomTotalTank,randomTotalHeal,randomTotalArmor,randomTotalSupp]
        
        try:
            desc = msgMax[whatRandomStat][random.randint(0,len(msgMax[whatRandomStat])-1)].format(icon=await getUserIcon(bot,choisen["char"]),value=separeUnit(int(choisen["value"])),name=choisen["name"])
        except:
            desc = "placeholder.error.unknow"

        biggest = random.randint(0,4)
        if biggest < 2:
            if rdm2 == "max":
                records = aliceStatsDb.getRecord("max{0}".format(randomStat))
                if int(records["owner"]) == int(choisen["char"].owner):
                    desc += "\n\nC'est d'ailleurs le record tiens"
                else:
                    try:
                        recorder = loadCharFile(absPath + "/userProfile/" + str(records["owner"]) + ".prof")
                        desc += "\n\n"+randomRecordMsg[random.randint(0,len(randomRecordMsg)-1)].format(icon=await getUserIcon(bot,recorder),value=separeUnit(int(records["value"])),name=recorder.name)
                    except:
                        desc += "\n\nJ'ai pas pu trouver qui avait le record, par contre"
            else:
                summation = 0
                for di in listDict:
                    summation += int(di["value"])

                desc += "\n\n"+randomPurcenMsg[random.randint(0,len(randomPurcenMsg)-1)].format(purcent=int(choisen["value"]/summation*100))

    else:
        desc = "placeholder.error.nothingtoshow.{0}".format(randomStat)
    return discord.Embed(title="__{0}__\n<:alice:908902054959939664> :".format(text),color=aliceColor,description="\""+desc+"\"")