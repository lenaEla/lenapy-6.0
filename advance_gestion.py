import os,discord,emoji,copy
from classes import *
from gestion import *
from adv import *
from discord_slash.utils.manage_components import *


timeoutSelect = create_select(
    options=[create_select_option("Timeout","Parfois je me demande ce que ferais Lena si elle pensais par elle même",emoji='🕛',default=True)],
    disabled=True
)
timeoutSelect = create_actionrow(timeoutSelect)

def remove_accents(input_str):
    temp =""
    for a in input_str:
        if a in ["à","ä","â"]:
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

def visuArea(area,wanted,ranged=True):
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

            elif area in [AREA_ALL_ALLIES,AREA_ALL_ENNEMIES,AREA_ALL_ENTITES]:

                for b in tablAllCells:
                    if b.on != None:
                        if a == AREA_ALL_ALLIES and b.on.team == team:
                            rep+=[b]
                        elif a == AREA_ALL_ENNEMIES and b.on.team != team:
                            rep+=[b]
                        elif a == AREA_ALL_ENTITES:
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

    visibleCell = findCell(2,2)
    if not(ranged):
        visibleCell = findCell(3,2)
    elif area in [AREA_CIRCLE_4,AREA_CONE_4,AREA_LINE_4,AREA_DONUT_4,AREA_DIST_4]:
        visibleCell = findCell(1,2)
    elif area in [5,6,7,14,15,16,20,21,26,27,28,31,32,33]:
        visibleCell = findCell(0,2)

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
        if findCell(3,2) in visibleArea: 
            if wanted==ENNEMIS:
                lines[2][3] = "<:ikaRedTargeted2:873118129541238814>"                       # Memo : Lines[y][x]
            else:    
                lines[2][3] = '<:ikaLBTargeted1:873118128958214166>'
        else:
            if wanted==ENNEMIS:
                lines[2][3] = '<:ikaRed:866459224664702977>'
            else:
                lines[2][3] = '<:ikaLBlue:866459302319226910>'
    

    temp = ""
    for a in lines:
        for b in [0,1,2,3,4]:
            temp += f"{a[b]}|"
        temp += f"{a[b+1]}\n"

    return temp

def infoEffect(effId,user,embed,ctx,self=False):
    effTmp,boucle,iteration ="",True,False
    while boucle:
        eff = findEffect(effId)
        bonus,malus = "",""
        Stat = ""
        if eff.stat == None:
            Stat = "Aucune"
        elif eff.stat == PURCENTAGE:
            Stat = "Pourcentage"
        else:
            Stat = allNameStats[eff.stat]

        tamp = str(eff.turnInit) + " tour(s)"
        if eff.turnInit == -1:
            tamp = "Infinie"

        Powa = ""
        if eff.power > 0:
            Powa = "\nPuissance : "+str(max(eff.power,eff.overhealth))
        effTmp+=f"__Nom :__ {eff.name}\n__Icone de l'effet :__ {eff.emoji[user.species-1][0]}\nDurée : {tamp}\nStatistique prise en compte : **{Stat}**{Powa}\n"
        stats = [eff.strength,eff.endurance,eff.charisma,eff.agility,eff.precision,eff.intelligence,eff.resistance,eff.percing,eff.critical,eff.overhealth,eff.redirection]
        names = nameStats+nameStats2+["Armure","Redirection"]
        for a in range(len(stats)):
            if stats[a] > 0:
                bonus += f"{names[a]} : +{stats[a]}\n"
            elif stats[a] < 0:
                malus += f"{names[a]} : {stats[a]}\n"

        if bonus !="":
            effTmp+=f"\n**__Bonus de statistiques :__**\n{bonus}"
        if malus !="":
            effTmp+=f'\n**__Malus de statistiques :__**\n{malus}'

        if eff.immunity:
            effTmp+="Tant que le porteur possède cet effet, il est **Invulnérable aux dégâts**\n"

        effTmp += f'\n__**Description :**__\n{eff.description}\n'

        if eff.reject != None:
            effTmp += "\n__Cet effet n'est pas compatible avec les effets :__\n"
            for a in eff.reject:
                rejected = findEffect(a)
                effTmp += f"{rejected.emoji[user.species-1][0]} {rejected.name}\n"

        if eff.callOnTrigger != None and not(iteration):
            effTmp += "\n**__À l'activation, cet effet donne un autre effet :__**"
            effId = eff.callOnTrigger
            iteration = True
            embed.add_field(name = "__Effet :__",value = effTmp,inline = False)
            effTmp = ""
        elif eff.callOnTrigger != None and iteration:
            effTmp += "\n**__À l'activation, cet effet donne un autre effet :__**"
            effId = findEffect(eff.callOnTrigger)
            embed.add_field(name = "**__Effet appelé :__**",value = effTmp,inline = False)
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
                embed.add_field(name = "<:empty:866459463568850954>\n**__Effet :__**",value = effTmp,inline = False)
            else:
                embed.add_field(name = "<:empty:866459463568850954>\n**__Effet sur soi :__**",value = effTmp,inline = False)
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

    return embed

def infoSkill(skill,user,ctx):
    skil = skill
    repEmb = discord.Embed(title = skil.name,color = user.color, description = f"Icone : { skil. emoji}\nTemps de rechargements : {skil.cooldown} tour(s)")
    temp = "Type : "

    if skil.type == TYPE_DAMAGE:
        temp+=f"Dégats\nPuissance : {skil.power}\nZone : "

        if skil.area == AREA_MONO:
            temp +=  "Monocible\n"
        else:
            temp += "Dégâts de zone\n"

        portee = skil.range
        if skill.range != AREA_MONO:
            temp += f"Portée : {skil.range}\n"

        else:
            temp += f"\nCette compétence se lance sur **soi-même**"
        
        if skil.use != STRENGTH:
            if skil.use not in [None,HARMONIE]:
                temp += f"\nCette compétence utilise la statistique de **{nameStats[skil.use]}**"
            elif skil.use == None:
                temp += f"\nCette compétence inflige un montant **fixe** de dégâts"
            elif skil.use == HARMONIE:
                temp += f"\nCette compétence utilise la statistique d'**Harmonie**"

    else:
        temp+=tablTypeStr[skil.type]

        if skil.description != None:
            temp += "\n"+skil.description+"\n"

        if skil.type == TYPE_HEAL:
            temp+="\nPuissance : {0}\nUtilise : {1}".format(skil.power,nameStats[skil.use])

        if skil.range == AREA_MONO:
            temp += "\nCette compétence se lance **sur soi-même**"
        else:
            ballerine, babie = [TYPE_ARMOR,TYPE_BOOST,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ,TYPE_RESURECTION,TYPE_HEAL],[TYPE_INDIRECT_DAMAGE,TYPE_MALUS]
            for a in ballerine:
                if a == skil.type:
                    temp+=f"\nCette compétence peut cibler les **alliés** jusqu'à **{skil.range}** de portée"
                    break
            for a in babie:
                if a == skil.type:
                    temp+=f"\nCette compétence peut cibler les **ennemis** jusqu'à **{skil.range}** de portée"
                    break

        if skil.area != AREA_MONO:
            if skil.area <= 7:
                ballerine, babie = [TYPE_ARMOR,TYPE_BOOST,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ,TYPE_RESURECTION,TYPE_HEAL],[TYPE_INDIRECT_DAMAGE,TYPE_MALUS]
                for a in ballerine:
                    if a == skil.type:
                        temp+=f"\nCette compétence affecte les **alliés** autour de la cible dans un **cercle de {skil.area}**"
                        break
                for a in babie:
                    if a == skil.type:
                        temp+=f"\nCette compétence affecte les **ennemis** autour de la cible dans un **cercle de {skil.area}**"
                        break
            else:
                ballerine = ["tous les alliés","tous les ennemis","tous les combattants"]
                for a in range(AREA_ALL_ALLIES,AREA_ALL_ENTITES+1):
                    if a == skil.area:
                        temp+=f"\nCette compétence affecte **{ballerine[a-8]}**"
        
        if skil.shareCooldown :
            temp+=f"\nCette compétence a un cooldown syncronisé avec toute l'équipe"
        if skil.initCooldown > 1:
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
        temp += "\nCette compétence est une compétence **ultime**. Vous ne pouvez équiper qu'une compétence ultime à la fois"

    repEmb.add_field(name="__Statistiques :__",value=temp,inline=False)

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

    if skil.area != AREA_MONO and skil.area != AREA_ALL_ALLIES and skil.area != AREA_ALL_ENNEMIES and skil.area != AREA_ALL_ENTITES:
        ballerine, babie = [TYPE_ARMOR,TYPE_BOOST,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ,TYPE_RESURECTION,TYPE_HEAL],[TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE]
        for a in ballerine:
            if a == skil.type:
                repEmb.add_field(name = "__Zone d'effet :__",value=visuArea(skil.area,wanted=ALLIES,ranged=False))
                break

        for a in babie:
            if a == skil.type:
                repEmb.add_field(name = "__Zone d'effet :__",value=visuArea(skil.area,wanted=ENNEMIS,ranged=False))
                break
        
    if skil.effect != [None]:
        for a in skil.effect:
            repEmb = infoEffect(a,user,repEmb,ctx)

    if skil.effectOnSelf != None:
        repEmb = infoEffect(skil.effectOnSelf,user,repEmb,ctx,True)

    if skil.invocation != None:
        repEmb = infoInvoc(findInvoc(skil.invocation),repEmb)
    return repEmb

def infoWeapon(weapon,user,ctx):
    weap = weapon
    repEmb = discord.Embed(title = weap.name,color = user.color, description = f"Icone : {weap.emoji}")
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

    repEmb.add_field(name = "__Informations Principales :__",value = f"__Position :__ {portee}\n__Portée :__ {weap.effectiveRange}\n__Type :__{tablTypeStr[weap.type]}\n__Puissance :__ {weap.power}\n__Précision par défaut :__ {weap.sussess}%\n__Nombre de tirs :__ {weap.repetition}\n<:empty:866459463568850954>")
    repEmb.add_field(name="__Statistiques secondaires :__",value=f'{element}{info}\n<:empty:866459463568850954>',inline=True)
    bonus,malus = "",""
    stats = [weap.strength,weap.endurance,weap.charisma,weap.agility,weap.precision,weap.intelligence,weap.resistance,weap.percing]
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

    if weap.area != AREA_MONO and weap.area != AREA_ALL_ALLIES and weap.area != AREA_ALL_ENNEMIES and weap.area != AREA_ALL_ENTITES:
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

def infoStuff(stuff,user,ctx):
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

    repEmb = discord.Embed(title = weap.name,color = user.color, description = f"Icone : {weap.emoji}\nType : {temp}\nOrientation : {weap.orientation}{element}")

    bonus,malus = "",""
    stats = [weap.strength,weap.endurance,weap.charisma,weap.agility,weap.precision,weap.intelligence,weap.resistance,weap.percing]
    names = nameStats+nameStats2
    for a in range(len(stats)):
        if stats[a] > 0:
            bonus += f"{names[a]} : +{stats[a]}\n"
        elif stats[a] < 0:
            malus += f"{names[a]} : {stats[a]}\n"

    if bonus != "":
        repEmb.add_field(name ="__Bonus de statistiques :__",value = bonus,inline = True)
    if malus != "":
        repEmb.add_field(name="__Malus de statistiques :__",value = malus, inline = True)

    if weap.effect != None:
        infoEffect(weap.effect,user,repEmb,ctx)
        
    return repEmb

def infoOther(other,user):
    weap = other
    repEmb = discord.Embed(title = weap.name,color = user.color, description = f"Icone : { weap. emoji}")
    repEmb.add_field(name="Description :",value = weap.description)

    return repEmb

def userMajStats(user,tabl):
    user.strength,user.endurance,user.charisma,user.agility,user.precision,user.intelligence = tabl[0],tabl[1],tabl[2],tabl[3],tabl[4],tabl[5]
    return user

def restats(user):
    stats = user.allStats()
    allMax = [maxStrength,maxEndur,maxChar,maxAgi,maxPreci,maxIntel]
    for a in range(0,len(stats)):
        stats[a] = round(allMax[a][user.aspiration]*0.1+allMax[a][user.aspiration]*0.9*user.level/50)

    user.points = user.level
    user.bonusPoints = [0,0,0,0,0,0]

    return userMajStats(user,stats)

def silentRestats(user):
    stats = user.allStats()
    allMax = [maxStrength,maxEndur,maxChar,maxAgi,maxPreci,maxIntel]
    for a in range(0,len(stats)):
        stats[a] = round(allMax[a][user.aspiration]*0.1+allMax[a][user.aspiration]*0.9*user.level/50)+user.bonusPoints[a]

    return userMajStats(user,stats)

async def addExpUser(bot,guild,path,ctx,exp = 3,coins = 0):
    user = quickLoadCharFile(path)

    if guild.colorRole.enable:
        tablId,cmpt,result = [guild.colorRole.red,guild.colorRole.orange,guild.colorRole.yellow,guild.colorRole.green,guild.colorRole.lightBlue,guild.colorRole.blue,guild.colorRole.purple,guild.colorRole.pink,guild.colorRole.white,guild.colorRole.black],0,0
        while cmpt < len(colorId):
            if user[0].color == colorId[cmpt]:
                result = tablId[cmpt]
            cmpt += 1
        roles,find = ctx.author.roles,False
        for a in roles:
            if a == ctx.guild.get_role(result):
                find = True

        if not(find):
            print(f"{ctx.author.name} a débuté l'aventure mais n'a pas son role de couleur")
            try:
                await ctx.author.add_roles(ctx.guild.get_role(result))       
            except:
                pass            

    user[0].exp = user[0].exp + exp
    user[0].currencies = user[0].currencies + coins

    upLvl = (user[0].level -1)*50+30

    if user[0].exp >= upLvl:
        perso = loadCharFile(path,ctx)
        perso.currencies, perso.exp = user[0].currencies, user[0].exp
        perso.points = perso.points + 1

        temp = perso.allStats()
        up,bonus = [0,0,0,0,0,0],[0,0,0,0,0,0]
        tabl = [maxStrength,maxEndur,maxChar,maxAgi,maxPreci,maxIntel]
        stats = perso.allStats()
        for a in range(0,len(stats)):
            stats[a] = round(tabl[a][perso.aspiration]*0.1+tabl[a][perso.aspiration]*0.9*perso.level/50+perso.bonusPoints[a])
            bonus[a] = perso.bonusPoints[a]
            temp[a] = round(tabl[a][perso.aspiration]*0.1+tabl[a][perso.aspiration]*0.9*(perso.level+1)/50+perso.bonusPoints[a])
            up[a] = temp[a]-stats[a]


        perso.strength, perso.endurance, perso.charisma, perso.agility, perso.precision, perso.intelligence = temp[0]+bonus[0],temp[1]+bonus[1],temp[2]+bonus[2],temp[3]+bonus[3],temp[4]+bonus[4],temp[5]+bonus[5]

        ballerine = await bot.fetch_user(perso.owner)
        lvlEmbed = discord.Embed(title = f"__Niveau supérieur__",color = perso.color,description = f"Le personnage de {ballerine.mention} ({perso.name}) a gagné un niveau !\n\nForce : {perso.strength} (+{up[0]})\nEndurance : {perso.endurance} (+{up[1]})\nCharisme : {perso.charisma} (+{up[2]})\nAgilité : {perso.agility} (+{up[3]})\nPrécision : {perso.precision} (+{up[4]})\nIntelligence : {perso.intelligence} (+{up[5]})\n\nVous avez {perso.points} bonus à répartir en utilisant la commande \"points\".")
        if guild.bot != 0:
            await bot.get_guild(guild.id).get_channel(guild.bot).send(embed = lvlEmbed)
        else:
            await ctx.channel.send(embed = lvlEmbed)

        perso.exp = perso.exp - (user[0].level)*50+30
        perso.level = perso.level + 1
        saveCharFile(path,perso)
        return perso
    else:
        quickSaveCharFile(path,user)
        return None

def getChoisenSelect(select, value : str):
    trouv = False
    temp = copy.deepcopy(select)
    for a in temp["options"]:
        if a["value"] == value:
            trouv=True
            a["default"] = True
    if trouv:
        temp["disabled"] = True
    return temp

async def downloadAllHeadGearPng(bot):
    listEmojiHead = stuffDB.getAllHeadGear()
    listDir = os.listdir("./data/images/headgears/")
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

async def downloadAllWeapPng(bot):
    listEmojiHead = stuffDB.getAllWeap()
    listDir = os.listdir("./data/images/weapons/")
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

async def downloadAllIconPng(bot):
    listEmojiHead = emoji.icon
    listDir = os.listdir("./data/images/char_icons/")
    for a in (1,2,4):
        for b in range(0,len(listEmojiHead[a])):
            emojiObject = getEmojiInfo(listEmojiHead[a][b])
            if emojiObject[0] + ".png" not in listDir:
                guildStuff = [862320563590529056]

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
                    background.paste(image,(145-128,145-128))
                    background.save(f"./data/images/char_icons/{emojiObject[0]}.png")
                    customIconDB.addIconFiles(a,b,f"{emojiObject[0]}.png")
                    print(emojiObject[0] + " téléchargé")
                else:
                    print(emojiObject[0] + " non trouvé")

async def makeCustomIcon(bot,user):
    # Récupération de l'icone de base
    if not(user.customColor):
        background = Image.open("./data/images/char_icons/"+customIconDB.getColorFile(user))
    else:
        tabl = [["./data/images/char_icons/empty_squid.png","./data/images/char_icons/white_squid.png"],["./data/images/char_icons/empty_octo.png","./data/images/char_icons/white_octo.png"]]
        background = Image.open(tabl[user.species-1][1])
        pixel = background.load()
        layer = Image.open(tabl[user.species-1][0])

        for x in range(0,background.size[0]):
            for y in range(0,background.size[1]):
                if pixel[x,y] != (0,0,0,0):
                    background.putpixel([x,y],hex_to_rgb(hex(user.color)))

        background.paste(layer,[0,0],layer)

    # Récupération de l'icone de l'arme
    if "./data/images/weapons/"+customIconDB.getWeaponFile(user) != "./data/images/weapons/akifauxgif.png":
        weapon = Image.open("./data/images/weapons/"+customIconDB.getWeaponFile(user))
    else:
        weapon = Image.open("./data/images/weapons/akifaux.png")
    weapon = weapon.resize((120,120))

    if user.weapon.needRotate == False:
        weapon = weapon.rotate(-30)

    # Récupération de l'icone de l'accessoire
    accessoire = Image.open("./data/images/headgears/"+customIconDB.getAccFile(user))
    
    # Paramètres de l'accessoire
    pos = user.stuff[0].position
    position = []
    if pos == 0:
        if user.species == 2:
            accessoire = accessoire.resize((round(accessoire.size[0]*1.3),accessoire.size[1]))
        position = (round(background.size[0]/2-accessoire.size[0]/2+8),0)
    elif pos == 1:
        accessoire = accessoire.resize((accessoire.size[0],accessoire.size[1]))
        if user.species==1:
            position = (5,round(background.size[1]/2))
        else:
            position = (10,round(background.size[1]/2))
    elif pos == 2:
        accessoire = accessoire.resize((accessoire.size[0],round(accessoire.size[1]*0.8)))
        position = (round(background.size[0]/2-accessoire.size[0]/2+8),round(background.size[1]/2+27))
    elif pos == 3:
        accessoire = accessoire.rotate(30)
        position = (round(background.size[0]*0.28-accessoire.size[0]/2+8),13)

    # Collage de l'accessoire
    background.paste(accessoire,position,accessoire)

    # Collage de l'arme
    background.paste(weapon,(50,45),weapon)

    imgByteArr = io.BytesIO()
    background.save(imgByteArr, format=background.format)
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

async def getUserIcon(bot,user):
    if customIconDB.isDifferent(user):
        await makeCustomIcon(bot,user)
    
    if customIconDB.haveCustomIcon(user):
        return customIconDB.getCustomIcon(user)

def infoInvoc(invoc,embed):
    rep = f"__Aspiration de l'invocation:__ {inspi[invoc.aspiration]}\n__Elément de l'invocation :__ {elemEmojis[invoc.element]} {elemNames[invoc.element]}\n__Description :__ {invoc.description}\n\n**__Statistiques :__**\n*\"Invoc\" est un raccourci pour \"Statistique de l'Invocateur\"*\n"

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

    embed.add_field(name="__"+invoc.name+"__",value=rep,inline = False)
    return embed

def infoAllie(allie):
    var = ""
    if allie.variant:
        var = "Cet allié temporaire est une variante d'un autre allié temporaire\n\n"
    rep = f"{var}__Aspiration :__ {inspi[allie.aspiration]}\n__Element :__ {elemEmojis[allie.element]} {elemNames[allie.element]}\n__Description :__\n{allie.description}\n\n__**Statistiques au niveau 50 :**__\n*Entre parenthèse : Les bonus donnés par l'équipement*\n"
    allMaxStats, accStats, dressStats, flatsStats = [maxStrength,maxEndur,maxChar,maxAgi,maxPreci,maxIntel],allie.stuff[0].allStats(),allie.stuff[1].allStats(),allie.stuff[2].allStats()
    for a in range(0,len(allMaxStats)):
        temp,tempi = allMaxStats[a][allie.aspiration],accStats[a]+dressStats[a]+flatsStats[a]
        rep += f"\n__{nameStats[a]}__ : {temp} ({tempi})"


    rep += f"\n\n__**Arme et compétences** :__\n{allie.weapon.emoji} {allie.weapon.name}\n"
    for a in allie.skills:
        if type(a) == skill:
            rep += f"\n{a.emoji} {a.name}"

    rep += f"\n\n__**Equipement :**__\n__Accessoire__ : {allie.stuff[0].emoji} {allie.stuff[0].name}\n__Vêtements__ : {allie.stuff[1].emoji} {allie.stuff[1].name}\n__Chaussures__ : {allie.stuff[2].emoji} {allie.stuff[2].name}"

    embed = discord.Embed(title="__Allié temporaire : "+allie.name+"__",color=allie.color,description=rep)
    embed.set_thumbnail(url=allie.url)
    return embed

def infoEnnemi(ennemi):
    rep = f"__Aspiration :__ {inspi[ennemi.aspiration]}\n__Description :__\n{ennemi.description}\n\n__**Statistiques au niveau 50 :**__\n*Entre parenthèse : Les bonus donnés par l'équipement*\n"
    allMaxStats, accStats, dressStats, flatsStats,weapStats = ennemi.allStats(),ennemi.stuff[0].allStats(),ennemi.stuff[1].allStats(),ennemi.stuff[2].allStats(),ennemi.weapon.allStats()
    for a in range(0,len(allMaxStats)):
        temp,tempi = allMaxStats[a],accStats[a]+dressStats[a]+flatsStats[a]+weapStats[a]
        rep += f"\n__{nameStats[a]}__ : {temp} ({tempi})"

    rep += f"\n\n__**Arme et compétences** :__\n{ennemi.weapon.emoji} {ennemi.weapon.name}\n"
    for a in ennemi.skills:
        if type(a) == skill:
            rep += f"\n{a.emoji} {a.name}"

    embed = discord.Embed(title="__Ennemis : "+ennemi.name+"__",color=ennemi.color,description=rep)
    if ennemi.url != None:
        embed.set_thumbnail(url=ennemi.url)
    return embed