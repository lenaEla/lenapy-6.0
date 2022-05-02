import copy
import io
import os
from sys import maxsize
from typing import List

import discord
from discord_slash.utils.manage_components import create_actionrow, create_select, create_select_option, create_button
import requests
from async_timeout import asyncio
from PIL import Image, ImageColor, ImageOps

import emoji
from adv import *
from classes import *
from commands_files.alice_stats_endler import *
from data.database import *
from gestion import *

stuffDB = dbHandler(database="stuff.db")
customIconDB = dbHandler(database="custom_icon.db")

timeoutSelect = create_select(
    options=[create_select_option(
        "Timeout", "Parfois je me demande ce que ferais Lena si elle pensais par elle même", emoji='🕛', default=True)],
    disabled=True
)
timeoutSelect = create_actionrow(timeoutSelect)

lvlUpUnlock = {
    5: "- Emplacement de compétence n°4",
    10: "- Eléments basiques\n- Compétences ultimes",
    15: "- Emplacement de compétence n°5",
    20: "- Eléments spaciaux-temporels",
    25: "- Emplacement de compétence n°6",
    30: "- Eléments secondaires",
    35: "- Emplacement de compétence n°7",
    55: "- Prestige"
}

def remove_accents(input_str: str):
    temp = ""
    for a in input_str:
        if a in ["à", "ä", "â", "@"]:
            temp += "a"
        elif a in ["é", "è", "ê", "ë"]:
            temp += "e"
        elif a in ["ì", "ï", "î"]:
            temp += "i"
        elif a in ["ù", "û"]:
            temp += "u"
        elif a in ["À", "Ä", "Â"]:
            temp += "A"
        elif a in ["É", "È", "Ë", "Ê"]:
            temp += "E"
        elif a == " ":
            pass
        elif a in ["?", "!", ";", ",", "."]:
            temp += "_"
        else:
            temp += a

    return temp

def visuArea(area: int, wanted, ranged=True) -> list:
    tablAllCells = []

    class cell:
        def __init__(self, x, y, id):
            self.x = x
            self.y = y
            self.id = id
            self.on = None

        def distance(self, cell=0):
            return (abs(self.x - cell.x)+abs(self.y - cell.y))

        def getArea(self, area=AREA_MONO, team=0):
            rep = []

            # Circles
            if area in [AREA_CIRCLE_1, AREA_CIRCLE_2, AREA_CIRCLE_3, AREA_CIRCLE_4, AREA_CIRCLE_5, AREA_CIRCLE_6, AREA_CIRCLE_7, AREA_DONUT_1, AREA_DONUT_2, AREA_DONUT_3, AREA_DONUT_4, AREA_DONUT_5, AREA_DONUT_6, AREA_DONUT_7, AREA_DIST_3, AREA_DIST_4, AREA_DIST_5, AREA_DIST_6, AREA_DIST_7]:
                dist = area
                if area > AREA_CIRCLE_7:
                    if area <= AREA_DONUT_7:
                        dist -= AREA_DONUT_1-1
                    elif area <= AREA_DIST_7:
                        dist -= AREA_DIST_3-3

                for a in tablAllCells:
                    if self.distance(cell=a) <= dist:
                        rep.append(a)

                if area > AREA_CIRCLE_7 and area <= AREA_DONUT_7:  # If donut, remove the center
                    rep.remove(self)
                elif area > AREA_DONUT_7 and area <= AREA_DIST_7:  # If dist only, remove melee
                    for a in rep[:]:
                        if self.distance(cell=a) <= 2:
                            rep.remove(a)

            elif area in [AREA_ALL_ALLIES, AREA_ALL_ENEMIES, AREA_ALL_ENTITES]:
                for b in tablAllCells:
                    if b.on != None:
                        if area == AREA_ALL_ALLIES and b.on.team == team:
                            rep += [b]
                        elif area == AREA_ALL_ENEMIES and b.on.team != team:
                            rep += [b]
                        elif area == AREA_ALL_ENTITES:
                            rep += [b]

            elif area in [AREA_CONE_2, AREA_CONE_3, AREA_CONE_4, AREA_CONE_5, AREA_CONE_6, AREA_CONE_7]:
                start, yDiff, xMax = self.x, 0, area-10
                areaTabl = []

                if team == 0:
                    ite = 0
                    while start <= 5 and ite <= xMax:
                        for y in range(0, yDiff+1):
                            if findCell(start, self.y+y) not in areaTabl and findCell(start, self.y+y) != None:
                                areaTabl.append(findCell(start, self.y+y))
                            if findCell(start, self.y-y) not in areaTabl and findCell(start, self.y-y) != None:
                                areaTabl.append(findCell(start, self.y-y))
                        start += 1
                        yDiff += 1
                        ite += 1
                else:
                    ite = 0
                    while start >= 0 and ite <= xMax:
                        for y in range(0, yDiff+1):
                            if findCell(start, self.y+y) not in areaTabl and findCell(start, self.y+y) != None:
                                areaTabl.append(findCell(start, self.y+y))
                            if findCell(start, self.y-y) not in areaTabl and findCell(start, self.y-y) != None:
                                areaTabl.append(findCell(start, self.y-y))
                        start -= 1
                        yDiff += 1
                        ite += 1

                return areaTabl

            elif area in [17, 18, 19, 20, 21]:  # Lines
                for a in tablAllCells:
                    if self.y == a.y and abs(a.x - self.x) <= area-16:
                        rep.append(a)

            elif area in [AREA_ARC_1, AREA_ARC_2, AREA_ARC_3]:  # Arcs
                cmptx = 1
                while cmptx < area - 32:
                    if team == 0:
                        cell1 = findCell(self.x-cmptx, self.y-cmptx)
                        if cell1 != None:
                            rep.append(cell1)
                        cell2 = findCell(self.x-cmptx, self.y+cmptx)
                        if cell2 != None:
                            rep.append(cell2)
                    if team == 1:
                        cell1 = findCell(self.x+cmptx, self.y-cmptx)
                        if cell1 != None:
                            rep.append(cell1)
                        cell2 = findCell(self.x+cmptx, self.y+cmptx)
                        if cell2 != None:
                            rep.append(cell2)
                    cmptx += 1
                rep.append(self)

            elif area == AREA_MONO:
                return [self]

            elif area in [AREA_INLINE_2, AREA_INLINE_3, AREA_INLINE_4, AREA_INLINE_5]:
                for celly in tablAllCells:
                    if (celly.x == self.x or celly.y == self.y) and self.distance(celly) <= area + 2 - AREA_INLINE_2:
                        rep.append(celly)

            return rep

    def findCell(x, y):
        cmpt = 0
        while cmpt < 30:
            if tablAllCells[cmpt].x == x and tablAllCells[cmpt].y == y:
                return tablAllCells[cmpt]
            cmpt += 1

    cmpt = 0
    for a in [0, 1, 2, 3, 4, 5]:
        for b in [0, 1, 2, 3, 4]:
            tablAllCells += [cell(a, b, cmpt)]
            cmpt += 1

    if not(ranged):
        if wanted == ALLIES:
            isAlly = -1
            isAlly2 = -2
            isAlly3 = -3
        else:
            if area in [AREA_CIRCLE_4, AREA_CONE_4, AREA_LINE_4, AREA_DONUT_4, AREA_DIST_4]:
                isAlly = -1
                isAlly2 = 0
                isAlly3 = 1
            elif area in [5, 6, 7, 14, 15, 16, 20, 21, 26, 27, 28, 31, 32, 33]:
                isAlly = -2
                isAlly2 = -1
                isAlly3 = 2
            else:
                isAlly = 0
                isAlly2 = 1
                isAlly3 = 2

        base = 3

        if area in [AREA_CIRCLE_4, AREA_CONE_4, AREA_LINE_4, AREA_DONUT_4, AREA_DIST_4]:
            visibleCell = findCell(base+isAlly2, 2)
        elif area in [5, 6, 7, 14, 15, 16, 20, 21, 26, 27, 28, 31, 32, 33]:
            visibleCell = findCell(base+isAlly3, 2)
        else:
            visibleCell = findCell(base+isAlly, 2)

    else:
        if area in [AREA_CIRCLE_4, AREA_CONE_2, AREA_LINE_4, AREA_DONUT_4, AREA_DIST_4, AREA_INLINE_3]:
            visibleCell = findCell(1, 2)
        elif area in [5, 6, 7, 14, 15, 16, 20, 21, 26, 27, 28, 31, 32, 33, AREA_CONE_3, AREA_CONE_4, AREA_INLINE_4, AREA_INLINE_5]:
            visibleCell = findCell(0, 2)
        else:
            visibleCell = findCell(2, 2)

    visibleArea = visibleCell.getArea(area=area)
    line1, line2, line3, line4, line5 = [None, None, None, None, None, None], [None, None, None, None, None, None], [
        None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None]
    lines = [line1, line2, line3, line4, line5]
    temp = ""

    for a in tablAllCells:
        temp = f'<:empty:866459463568850954>'
        if a in visibleArea:
            if wanted == ALLIES:
                temp = "<:Targeted1:873118129214083102>"
            else:
                temp = "<:Targeted2:873118129130192947>"

        lines[a.y][a.x] = temp
    if ranged:
        lines[visibleCell.y][visibleCell.x] = "<:ikaWhite:871149538554044466>"
    else:
        if visibleCell in visibleArea:
            if wanted == ENNEMIS:
                # Memo : Lines[y][x]
                lines[visibleCell.y][visibleCell.x] = "<:ikaRedTargeted2:873118129541238814>"
            else:
                lines[visibleCell.y][visibleCell.x] = '<:ikaLBTargeted1:873118128958214166>'
        else:
            if wanted == ENNEMIS:
                lines[visibleCell.y][visibleCell.x] = '<:ikaRed:866459224664702977>'
            else:
                lines[visibleCell.y][visibleCell.x] = '<:ikaLBlue:866459302319226910>'

    temp = ""
    for a in lines:
        for b in [0, 1, 2, 3, 4]:
            temp += f"{a[b]}|"
        temp += f"{a[b+1]}\n"

    return temp

def infoEffect(effId: str, user: char, embed: discord.Embed, ctx, self=False, txt: str = "",powerPurcent=100) -> discord.Embed:
    effTmp, boucle, iteration, fieldname, powerPurcent = "", True, False, "__Effet :__", [powerPurcent,100][powerPurcent==None]
    eff = findEffect(effId)

    while boucle:
        eff = findEffect(effId)
        bonus, malus = "", ""
        Stat = ""
        if eff.stat == None:
            Stat = "Aucune"
        elif eff.stat == PURCENTAGE:
            Stat = "Pourcentage"
        elif eff.stat != HARMONIE:
            Stat = allStatsNames[eff.stat]
        else:
            Stat = "Harmonie"

        tamp = str(eff.turnInit) + \
            " tour{0}".format(["", "s"][eff.turnInit > 1])
        if eff.turnInit == -1:
            tamp = "Infinie"

        Powa = ""
        if eff.power > 0:
            Powa = "\n__Puissance :__ "+str(int(max(eff.power, eff.overhealth)*(powerPurcent/100)))+[""," ({0}%)".format(powerPurcent)][powerPurcent!=100]

        cumu = ""
        if eff.stackable:
            cumu = "\n\nCet effet est **cumulable**"
        effTmp += f"__Nom :__ {eff.name}\n__Icone de l'effet :__ {eff.emoji[user.species-1][0]}\n__Durée :__ {tamp}\n__Statistique prise en compte :__ **{Stat}**{Powa}{cumu}"
        effTmp += "\nCet effet se délanche {0}".format(triggersTxt[eff.trigger])

        if eff.lvl != 1:
            effTmp += "\nCet effet peut se déclancher au maximum **{0} fois**".format(
                eff.lvl)
        stats = eff.allStats()+[eff.resistance, eff.percing,
                                eff.critical, eff.overhealth, eff.aggro, eff.inkResistance]
        names = nameStats+nameStats2 + \
            ["Armure", "Agression", "Résistance aux dégâts indirects"]

        if eff.redirection > 0:
            effTmp += "\nCet effet redirige **{0}**% des **dégâts direct** reçu par le porteur vers le lanceur de l'effet en tant que **dégâts indirects**\n".format(
                eff.redirection)

        if eff.immunity:
            effTmp += "\nCet effect rend le porteur **invulnérable aux dégâts**\n"

        effTmp += f'\n__Description :__\n{eff.description}\n'
        for a in range(len(stats)):
            if stats[a] > 0:
                bonus += f"{names[a]} : +{stats[a]}\n"
            elif stats[a] < 0:
                malus += f"{names[a]} : {stats[a]}\n"

        if bonus != "":
            effTmp += f"\n**__Bonus de statistiques :__**\n{bonus}"
        if malus != "":
            effTmp += f'\n**__Malus de statistiques :__**\n{malus}'

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
            embed.add_field(name=fieldname, value=effTmp, inline=False)
            effTmp = ""
            fieldname = "<:empty:866459463568850954>\n__À l'activation, cet effet donne un autre effet :__"
        elif eff.callOnTrigger != None and iteration:
            effId = findEffect(eff.callOnTrigger)
            embed.add_field(name=fieldname, value=effTmp, inline=False)
            fieldname = "<:empty:866459463568850954>\n__À l'activation, cet effet donne un autre effet :__"
            if eff.area != AREA_MONO:
                ballerine, babie = [TYPE_ARMOR, TYPE_BOOST, TYPE_INDIRECT_HEAL, TYPE_INDIRECT_REZ,
                                    TYPE_RESURECTION, TYPE_HEAL], [TYPE_INDIRECT_DAMAGE, TYPE_MALUS, TYPE_DAMAGE]
                for a in ballerine:
                    if a == eff.type:
                        embed.add_field(name="__Zone d'effet :__", value=visuArea(
                            eff.area, wanted=ALLIES, ranged=False))
                        break

                for a in babie:
                    if a == eff.type:
                        embed.add_field(name="__Zone d'effet :__", value=visuArea(
                            eff.area, wanted=ENNEMIS, ranged=False))
                        break
            break
        else:
            if not(self):
                embed.add_field(name="<:empty:866459463568850954>\n" +fieldname + txt, value=effTmp, inline=False)
            else:
                embed.add_field(name="<:empty:866459463568850954>\n**__Effet sur soi :__**", value=effTmp, inline=False)

            if eff.area != AREA_MONO:
                if eff.type in [TYPE_ARMOR, TYPE_BOOST, TYPE_INDIRECT_HEAL, TYPE_INDIRECT_REZ, TYPE_RESURECTION, TYPE_HEAL]:
                    embed.add_field(name="__Zone d'effet :__", value=visuArea(
                        eff.area, wanted=ALLIES, ranged=False))
                    break

                elif eff.type in [TYPE_INDIRECT_DAMAGE, TYPE_MALUS, TYPE_DAMAGE]:
                    embed.add_field(name="__Zone d'effet :__", value=visuArea(
                        eff.area, wanted=ENNEMIS, ranged=False))

            break

    return embed

def infoSkill(skill: skill, user: char, ctx):
    skil = skill
    cast = 0
    while skil.effectOnSelf != None:
        eff = findEffect(skil.effectOnSelf)
        if eff.replica != None:
            skil = findSkill(eff.replica)
        else:
            break
        cast += 1

    if [skill.id, skill.name] == [trans.id, trans.name]:
        skil = transTabl[user.aspiration]

    elif skil.id == mageUlt.id:
        if user.element in [ELEMENT_FIRE, ELEMENT_AIR, ELEMENT_SPACE]:
            skil = mageUltZone
        elif user.element in [ELEMENT_WATER, ELEMENT_EARTH, ELEMENT_TIME]:
            skil = mageUltMono
        else:
            skil = mageUlt

    if skil.become != None:
        desc, listConds = "Cette compétence permet d'utiliser :\n", []
        for cmpt in range(len(skil.become)):
            desc += "{1} __{0}__".format(
                skil.become[cmpt].name, skil.become[cmpt].emoji)
            if cmpt < len(skil.become)-2:
                desc += ", "
            elif cmpt == len(skil.become)-2:
                desc += " et "
            if skil.become[cmpt].needEffect != None:
                temp2 = "\n{1} __{0}__ : ".format(
                    skil.become[cmpt].name, skil.become[cmpt].emoji)
                for temp in skil.become[cmpt].needEffect:
                    temp2 += "{0} {1}".format(temp.emoji[0][0], temp.name)
                listConds.append(temp2)

        desc += "\nLorsque leurs conditions sont réunies. Leurs temps de rechargement sont syncronisés"
    else:
        desc = ""
    # Cooldown ---------------------------
    if skil.type != TYPE_PASSIVE:
        if skil.become != None:
            desc += "\n\n__Temps de rechargements :__"
            for cmpt in range(len(skil.become)):
                s = ""
                if skil.become[cmpt].cooldown > 1:
                    s = "s"
                desc += "\n{0} tour{2} ({1})".format(
                    skil.become[cmpt].cooldown, skil.become[cmpt].name, s)

        else:
            s = ""
            if skil.cooldown > 1:
                s = "s"
            desc += f"\n__Temps de rechargements :__ {skil.cooldown} tour{s}"""

    if cast > 0:
        desc += "\n__Tours de chargements__ : **{0} tour{1}**".format(
            cast, ["", "s"][int(cast > 1)])

    temp = "__Type :__ "

    if skil.type == TYPE_DAMAGE:
        temp += "Dégats\n"

        if skil.description != None:
            temp += "\n__Description :__\n"+skil.description+"\n"

        # Power, Success and Damage Type
        if skil.become == None:
            if skil.repetition > 1:
                nbShot = " x{0}".format(skil.repetition)
            else:
                nbShot = ""
            temp += "\n__Puissance :__ {0}\n__Zone d'effet :__ ".format([f"**{skil.power}**{nbShot}","**Execution**"][int(skil.execution)])
            temp += areaNames[skil.area]
            temp += "\n__Précision :__ {0}%\n".format(skil.sussess)

        else:
            temp += "\n__Puissances :__\n"
            for cmpt in range(len(skil.become)):
                multi = ""
                if skil.become[cmpt].repetition > 1:
                    multi = " x{0}".format(skil.become[cmpt].repetition)
                temp += "__{0}__{2} ({1})\n".format(
                    skil.become[cmpt].power, skil.become[cmpt].name, multi)

            temp += "\n__Zone d'effet :__\n"
            for cmpt in range(len(skil.become)):
                temp += "{0} ({1})\n".format(
                    areaNames[skil.become[cmpt].area], skil.become[cmpt].name)

            temp += "\n__Précisions :__\n"
            for cmpt in range(len(skil.become)):
                temp += "{0}% ({1})\n".format(
                    skil.become[cmpt].sussess, skil.become[cmpt].name)

        # Clem and Alice blood jauge skills
        if skil.id.startswith("clem") or skil.id.startswith("alice"):
            for skillID, cost in clemBJcost.items():
                if skil.id == skillID:
                    temp += "\n__Coût en points de sang :__ **{0}**".format(
                        cost)

        if skil.range == AREA_MONO:
            if skil.type != TYPE_PASSIVE:
                temp += f"\nCette compétence se lance sur **soi-même**"
            else:
                temp += f"\nLes compétences passives se déclanchent au début du combat"

        if skil.become == None:
            temp += "\nCette compétence cible les **ennemis**"

        if skil.onArmor != 1 and skil.become == None:
            temp += "\n__Dégâts sur armure :__ **{0}%**".format(
                int(skil.onArmor*100))
        elif skil.become != None:
            for becomeName in skil.become:
                if becomeName.onArmor != 1:
                    temp += "\n__{2} {1}__ inflige **{0}%** de ses dégâts aux armures".format(
                        int(becomeName.onArmor*100), becomeName.name, becomeName.emoji)

        if skil.use not in [None, HARMONIE]:
            temp += f"\n\nCette compétence utilise la statistique de **{nameStats[skil.use]}**"
        elif skil.use == None:
            temp += f"\nCette compétence inflige un montant **fixe** de dégâts"
        elif skil.use == HARMONIE:
            temp += f"\nCette compétence utilise la statistique d'**Harmonie**"

    else:
        temp += tablTypeStr[skil.type]

        if skil.become != None:
            for skilly in skil.become:
                temp += "\n__Type ({0}) :__ {1}".format(skilly.name,
                                                        tablTypeStr[skilly.type])
                if skilly.type in [TYPE_DAMAGE, TYPE_HEAL]:
                    temp += "\n> Puissance : **{0}**, {1}".format(
                        skilly.power, nameStats[skilly.use])

        if skil.description != None:
            temp += "\n\n__Description :__\n"+skil.description+"\n"

        if skil.type != TYPE_PASSIVE:
            temp += "\n__Zone d'effet :__ {0}".format(areaNames[skil.area])

        if skil.id.startswith("clem") or skil.id.startswith("alice"):
            for skillID, cost in clemBJcost.items():
                if skil.id == skillID:
                    temp += "\n__Coût en points de sang :__ **{0}**".format(
                        cost)

        if skil.type in [TYPE_HEAL, TYPE_RESURECTION] and skil.become == None:
            temp += "\n__Puissance :__ {0}".format(skil.power)
            if skil.use not in [None, HARMONIE]:
                temp += f"\n\nCette compétence utilise la statistique de **{nameStats[skil.use]}**"
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
            ballerine, babie = [TYPE_ARMOR, TYPE_BOOST, TYPE_INDIRECT_HEAL, TYPE_INDIRECT_REZ,
                                TYPE_RESURECTION, TYPE_HEAL], [TYPE_INDIRECT_DAMAGE, TYPE_MALUS]
            for a in ballerine:
                if a == skil.type:
                    temp += f"\nCette compétence cible les **alliés**"
                    break
            for a in babie:
                if a == skil.type:
                    temp += f"\nCette compétence cible les **ennemis**"
                    break

        if skil.area != AREA_MONO:
            ballerine = ["tous les alliés",
                         "tous les ennemis", "tous les combattants"]
            for a in range(AREA_ALL_ALLIES, AREA_ALL_ENTITES+1):
                if a == skil.area:
                    temp += f"\nCette compétence affecte **{ballerine[a-8]}**"

    if skil.shareCooldown:
        temp += f"\nCette compétence a un cooldown syncronisé avec toute l'équipe"
    if skil.initCooldown > 1 and skil.type != TYPE_PASSIVE:
        temp += f"\nCette compétence ne peut pas être utilisée avant le tour {skil.initCooldown}"

    if skil.useActionStats != None:
        temp += "\nCette compétence utilise la statistiques d'action **{0}**".format(
            ["Soins", "Bonus et Malus", "Armures et Mitigeation", 'Dégâts Directs', "Dégâts Indirects"][skil.useActionStats])
    if skil.condition != []:
        temp += "\nCette compétence "
        if skil.condition[0] == 0:
            temp += "est exclusive à "
            if skil.condition[1] == 0:
                temp += "l'arme "+findWeapon(skil.condition[2]).name+"**"
            elif skil.condition[1] == 1:
                temp += "l'aspiration **"+inspi[skil.condition[2]]+"**"
            elif skil.condition[1] == 2:
                temp += "l'élément principal **" + \
                    elemNames[skil.condition[2]]+"**"
            elif skil.condition[1] == 3:
                temp += "l'élément secondaire **" + \
                    elemNames[skil.condition[2]]+"**"
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

    if skil.effPowerPurcent != 100:
        temp += "\nLes effets donnés par cette compétence ont une puissance équivalente à **{0}%** de leur puissance initiale".format(
            skil.effPowerPurcent)
    if skil.replay:
        temp += "\nCette compétence permet de rejouer son tour"

    if skil.maxHpCost > 0:
        temp += "\nCette compétence consome **{0}%** des PV maximums du lanceur lors de son utilisation".format(
            skil.maxHpCost)
    if skil.hpCost > 0:
        temp += "\nCette compétence consome **{0}%** des PV actuels du lanceur lors de son utilisation".format(
            skil.hpCost)

    if skil.ultimate:
        temp += "\nCette compétence est une compétence **ultime**."
    if skil.execution :
        temp += "\nCette compétence est une **exécution**. Les cibles exécutées sont immédiatement misent hors-jeu et ne peuvent pas être réanimés"
    if skil.group != 0:
        temp += "\nCette compétence est une compétence **{0}**.".format(
            skillGroupNames[skil.group])
    if skil.setAoEDamage:
        temp += "\nLes dégâts de cette compétence ne sont pas affectés par la réduction de dégâts de zone"
    if skil.lifeSteal > 0:
        temp += "\nCette compétence soigne son lanceur de l'équivalent de **{0}%** des dégâts infligés".format(
            skil.lifeSteal)
    if skil.erosion != 0:
        temp += "\nCette compétence a **{0}%** d'Erosion Spirituelle.'".format(skil.erosion)
    temp2 = ""
    if skil.tpCac:
        temp2 += "\n__Téléportation :__\nCette compétence téléporte le lanceur au corps à corps de la cible\n> - Si aucune case n'est libre, le lanceur subit des dégâts indirects Harmonie\n"

    if skil.knockback > 0 and skil.become == None:
        temp2 += "\n__Repoussement :__\nCette compétence repousse la cible de **{0}** case{1}\n> - Si la cible percute une autre entité ou le bord du terrain, les entités affectées reçoivent des dégâts indirects Harmonie\n".format(skil.knockback, [
                                                                                                                                                                                                                                       "", "s"][int(skil.knockback > 1)])
    if skil.jumpBack:
        temp2 += "\n__Saut :__\nCette compétence fait reculer le lanceur de **{0}** case{1}\n> - Si le lanceur percute une autre entité ou le bord du terrain, les entités affectées reçoivent des dégâts indirects Harmonie\n".format(skil.jumpBack, [
                                                                                                                                                                                                                                       "", "s"][int(skil.jumpBack > 1)])

    if temp2 != "":
        temp += "\n"+temp2

    if skil.become != None:
        allreadyAdd = False
        for becomeName in skil.become:
            if becomeName.knockback > 0:
                if not(allreadyAdd):
                    temp += "\n\n**__Repoussement :__**"
                    allreadyAdd = True
                temp += "\n__{1}__ repousse la cible de **{0}** case{2}".format(
                    becomeName.knockback, becomeName.name, ["", "s"][becomeName.knockback > 1])

    if skil.effectAroundCaster != None:
        if type(skil.effectAroundCaster[2]) == effect:
            toAdd = "__Effet :__ {0} ({1})".format(
                skil.effectAroundCaster[2].name, tablTypeStr[skil.effectAroundCaster[2].type])
        else:
            toAdd = "__Puissance :__ {0}".format(skil.effectAroundCaster[2])
        temp += "\n\n__Effet supplémentaire autour du lanceur :__\n__Type :__ {0}\n__Zone d'effet :__ {1}\n{2}".format(
            tablTypeStr[skil.effectAroundCaster[0]], areaNames[skil.effectAroundCaster[1]], toAdd)

    repEmb = discord.Embed(title=skil.name, color=user.color,
                           description=desc+"\n\n__Statistiques :__\n"+temp)
    if skil.emoji[1] == "a":
        repEmb.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/{0}.gif".format(getEmojiObject(skil.emoji)["id"]))
    else:
        repEmb.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(skil.emoji)["id"]))

    if skil.become == None:
        if skil.range not in [AREA_MONO, AREA_RANDOMENNEMI_1, AREA_RANDOMENNEMI_2, AREA_RANDOMENNEMI_3, AREA_RANDOMENNEMI_4, AREA_RANDOMENNEMI_5]:
            repEmb.add_field(name="__Portée :__", value=visuArea(skil.range, wanted=[
                             ALLIES, ENNEMIS][skil.type in [TYPE_INDIRECT_DAMAGE, TYPE_MALUS, TYPE_DAMAGE]]))

        if skil.area not in [AREA_MONO, AREA_RANDOMENNEMI_1, AREA_RANDOMENNEMI_2, AREA_RANDOMENNEMI_3, AREA_RANDOMENNEMI_4, AREA_RANDOMENNEMI_5, AREA_ALL_ALLIES, AREA_ALL_ENEMIES, AREA_ALL_ENTITES]:
            repEmb.add_field(name="__Zone d'effet :__", value=visuArea(skil.area, wanted=[
                             ALLIES, ENNEMIS][skil.type in [TYPE_INDIRECT_DAMAGE, TYPE_MALUS, TYPE_DAMAGE]], ranged=False))

    else:
        listRange, listRangeName, listArea, listName = [], [], [], []
        for become in skil.become:
            wantedTarget = [ALLIES, ENNEMIS][become.type in [
                TYPE_DAMAGE, TYPE_INDIRECT_DAMAGE, TYPE_MALUS]]
            if [become.range, wantedTarget] not in listRange:
                listRange.append([become.range, wantedTarget])
                listRangeName.append([become.name])
            else:
                for cmpt in range(len(listRange)):
                    if listRange[cmpt][0] == become.range:
                        listRangeName[cmpt].append(become.name)
                        break

            if [become.area, wantedTarget] not in listArea:
                listArea.append([become.area, wantedTarget])
                listName.append([become.name])
            else:
                for cmpt in range(len(listArea)):
                    if listArea[cmpt][0] == become.area:
                        listName[cmpt].append(become.name)
                        break

        if len(listRange) == 1:
            if listRange[0][0] not in [AREA_MONO, AREA_RANDOMENNEMI_1, AREA_RANDOMENNEMI_2, AREA_RANDOMENNEMI_3, AREA_RANDOMENNEMI_4, AREA_RANDOMENNEMI_5]:
                repEmb.add_field(name="__Portée :__", value=visuArea(listRange[0][0], wanted=listRange[0][1]), inline=len(
                    listRange) == len(listArea) == 0 or len(listRange) > 1)
        else:
            for cmpt in range(len(listRange)):
                if listRange[cmpt][0] not in [AREA_MONO, AREA_RANDOMENNEMI_1, AREA_RANDOMENNEMI_2, AREA_RANDOMENNEMI_3, AREA_RANDOMENNEMI_4, AREA_RANDOMENNEMI_5]:
                    temporis = "("
                    for name in range(len(listRangeName[cmpt])):
                        temporis += listRangeName[cmpt][name]
                        if name != len(listRangeName[cmpt]) - 1:
                            temporis += ",\n"
                        else:
                            temporis += ")"

                    repEmb.add_field(name="__Portée :__", value=temporis+"\n" +
                                     visuArea(listRange[cmpt][0], wanted=listRange[cmpt][1]))

        if len(listArea) == 1:
            if listArea[0][0] not in [AREA_MONO, AREA_RANDOMENNEMI_1, AREA_RANDOMENNEMI_2, AREA_RANDOMENNEMI_3, AREA_RANDOMENNEMI_4, AREA_RANDOMENNEMI_5, AREA_ALL_ALLIES, AREA_ALL_ENEMIES, AREA_ALL_ENTITES]:
                repEmb.add_field(name="__Zone d'effet :__", value=visuArea(
                    listArea[0][0], wanted=listArea[0][1], ranged=False))
        elif len(listArea) != 0:
            for cmpt in range(len(listArea)):
                if listArea[cmpt][0] not in [AREA_MONO, AREA_RANDOMENNEMI_1, AREA_RANDOMENNEMI_2, AREA_RANDOMENNEMI_3, AREA_RANDOMENNEMI_4, AREA_RANDOMENNEMI_5, AREA_ALL_ALLIES, AREA_ALL_ENEMIES, AREA_ALL_ENTITES]:
                    temporis = "("
                    for name in range(len(listName[cmpt])):
                        temporis += listName[cmpt][name]
                        if name != len(listName[cmpt]) - 1:
                            temporis += ",\n"
                        else:
                            temporis += ")"

                    repEmb.add_field(name="__Zone d'effet :__", value=temporis+"\n"+visuArea(
                        listArea[cmpt][0], wanted=listArea[cmpt][1], ranged=False))

    if skil.effect != [None]:
        allReadySeen, effToSee = [], []
        for a in skil.effect:
            eff = findEffect(a)
            if eff not in allReadySeen:
                allReadySeen.append(eff)
                effToSee.append(1)
            else:
                for cmpt in range(len(effToSee)):
                    if allReadySeen[cmpt].id == eff.id:
                        effToSee[cmpt] += 1

        for a in range(len(allReadySeen)):
            txt = ["", " x{0}".format(effToSee[a])][effToSee[a] > 1]
            repEmb = infoEffect(allReadySeen[a], user, repEmb, ctx, txt=txt,powerPurcent=skil.effPowerPurcent)

    if skil.become != None:
        for skilly in skil.become:
            if skilly.effect != [None]:
                for eff in skilly.effect:
                    repEmb = infoEffect(findEffect(
                        eff), user, repEmb, ctx, txt=" ({0})".format(skilly.name))

    if skil.effectOnSelf != None:
        if skil.type != TYPE_PASSIVE:
            repEmb = infoEffect(skil.effectOnSelf, user, repEmb, ctx, True,powerPurcent=skil.selfEffPurcent)
        else:
            repEmb = infoEffect(skil.effectOnSelf, user, repEmb, ctx,True," (passif)",powerPurcent=skil.selfEffPurcent)

    if skil.invocation != None:
        repEmb = infoInvoc(findSummon(skil.invocation), repEmb)

    if repEmb.__len__() > 6000:
        repEmb = discord.Embed(title=skil.name, color=user.color, description=desc +
                               "\n__Statistiques :__\n"+temp+"\n\nCertaines infromations n'ont pas pu être affichées.")
        if skil.emoji[1] == "a":
            repEmb.set_thumbnail(
                url="https://cdn.discordapp.com/emojis/{0}.gif".format(getEmojiObject(skil.emoji)["id"]))
        else:
            repEmb.set_thumbnail(
                url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(skil.emoji)["id"]))

    if skil.url != None:
        repEmb.set_image(url=skil.url)

    if skil.become != None:         # Effect on self list
        listEffSelf = ""
        for skilly in skil.become:
            if skilly.effectOnSelf != None:
                listEffSelf += "\n{3} __{0}__ : {1} {2}".format(
                    skilly.name, skilly.effectOnSelf.emoji[0][0], skilly.effectOnSelf.name, skilly.emoji)

        if len(listConds) > 0:
            condsDesc = ""
            for conds in listConds:
                condsDesc += conds

            repEmb.add_field(
                name="__Conditions des compétences :__", value=condsDesc, inline=False)

        if len(listEffSelf) > 0:
            repEmb.add_field(
                name="__Effets sur soi des compétences :__", value=listEffSelf, inline=False)
    
    if skil.id == horoscope.id:
        desc = ""
        for cmpt in horoscopeEff:
            desc += "{0} __{1}__ :".format(cmpt[0].emoji[0][0],cmpt[0].name)
            for staty in range(len(cmpt[1])):
                desc += " {0} +{1}".format(nameStats[cmpt[1][staty][0]],cmpt[1][staty][1])
                if staty != len(cmpt[1])-1:
                    desc += ","
            desc += "\n"

        repEmb.add_field(name="__Bonus par signe astrologique :__",value=desc,inline=False)

    return repEmb

def infoWeapon(weap: weapon, user: char, ctx):
    repEmb = discord.Embed(title=unhyperlink(
        weap.name), color=user.color, description=f"Icone : {weap.emoji}")
    repEmb.set_thumbnail(
        url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(weap.emoji)["id"]))

    portee = ["Mêlée", "Dist.", "L. Dist."][weap.range]

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

    info += "\n__Zone d'effet :__ " + cible + \
        f"\n__Statistique utilisée :__ {nameStats[weap.use]}"

    if weap.onArmor != 1 and weap.type == TYPE_DAMAGE:
        info = f"\n__Dégâts sur armure :__ **{int(weap.onArmor*100)}**%"

    element = ""
    if weap.affinity != None:
        element = f"\n__Affinité :__ {elemEmojis[weap.affinity]} {elemNames[weap.affinity]}"

    if weap.repetition > 1:
        nbShot = " x{0}".format(weap.repetition)
    else:
        nbShot = ""

    repEmb.add_field(name="__Informations Principales :__",
                     value=f"__Position :__ {portee}\n__Portée :__ {weap.effectiveRange}\n__Type :__ {tablTypeStr[weap.type]}\n__Puissance :__ {weap.power}{nbShot}\n__Précision par défaut :__ {weap.sussess}%\n<:empty:866459463568850954>", inline=False)
    repEmb.add_field(name="__Statistiques secondaires :__",
                     value=f'{element}{info}\n<:empty:866459463568850954>', inline=False)
    bonus, malus = "", ""
    stats = weap.allStats()+[weap.resistance, weap.percing, weap.critical]
    names = nameStats+nameStats2
    for a in range(len(stats)):
        if stats[a] > 0:
            bonus += f"{names[a]} : +{stats[a]}\n"
        elif stats[a] < 0:
            malus += f"{names[a]} : {stats[a]}\n"

    if bonus != "":
        repEmb.add_field(name="__Bonus de statistiques :__",
                         value=bonus+"\n<:empty:866459463568850954>", inline=False)
    if malus != "":
        repEmb.add_field(name="__Malus de statistiques :__",
                         value=malus+"\n<:empty:866459463568850954>", inline=False)

    ballerine, babie = [TYPE_ARMOR, TYPE_BOOST, TYPE_INDIRECT_HEAL, TYPE_INDIRECT_REZ,
                        TYPE_RESURECTION, TYPE_HEAL], [TYPE_INDIRECT_DAMAGE, TYPE_MALUS, TYPE_DAMAGE]
    for a in ballerine:
        if a == weap.type:
            repEmb.add_field(name="__Portée :__", value=visuArea(
                weap.effectiveRange, wanted=ALLIES))
            break

    for a in babie:
        if a == weap.type:
            repEmb.add_field(name="__Portée :__", value=visuArea(
                weap.effectiveRange, wanted=ENNEMIS))
            break

    if weap.area != AREA_MONO and weap.area != AREA_ALL_ALLIES and weap.area != AREA_ALL_ENEMIES and weap.area != AREA_ALL_ENTITES:
        ballerine, babie = [TYPE_ARMOR, TYPE_BOOST, TYPE_INDIRECT_HEAL, TYPE_INDIRECT_REZ,
                            TYPE_RESURECTION, TYPE_HEAL], [TYPE_INDIRECT_DAMAGE, TYPE_MALUS, TYPE_DAMAGE]
        for a in ballerine:
            if a == weap.type:
                repEmb.add_field(name="__Zone d'effet :__", value=visuArea(
                    weap.area, wanted=ALLIES, ranged=False))
                break

        for a in babie:
            if a == weap.type:
                repEmb.add_field(name="__Zone d'effet :__", value=visuArea(
                    weap.area, wanted=ENNEMIS, ranged=False))
                break

    if weap.effect != None:
        repEmb.add_field(name="<:empty:866459463568850954>\n__Effet Passif :__",
                         value="Cette arme accorde un effet passif à son porteur", inline=False)
        infoEffect(weap.effect, user, repEmb, ctx)

    if weap.effectOnUse != None:
        repEmb.add_field(name="<:empty:866459463568850954>\n__Effet à l'utilisation :__",
                         value="Cette arme donne un effet à la cible", inline=False)
        infoEffect(weap.effectOnUse, user, repEmb, ctx)
    return repEmb

def infoStuff(stuff: stuff, user: char, ctx):
    weap = stuff
    temp = ""
    if weap.type == 0:
        temp = "Accessoire"
    elif weap.type == 1:
        temp = "Haut"
    else:
        temp = "Chaussures"

    element = ""
    if weap.affinity != None:
        element = f"\nAffinité : {elemEmojis[weap.affinity]} {elemNames[weap.affinity]}"

    repEmb = discord.Embed(title=unhyperlink(weap.name), color=user.color,
                           description=f"Niveau : {weap.minLvl}\nType : {temp}\nOrientation : {weap.orientation}{element}")
    repEmb.set_thumbnail(
        url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(weap.emoji)["id"]))

    bonus, malus = "", ""
    stats = weap.allStats()+[weap.resistance, weap.percing]
    names = nameStats+nameStats2
    for a in range(len(stats)):
        if stats[a] > 0:
            bonus += f"{names[a]} : +{stats[a]}\n"
        elif stats[a] < 0:
            malus += f"{names[a]} : {stats[a]}\n"

    negative = [weap.negativeHeal, weap.negativeBoost,
                weap.negativeShield, weap.negativeDirect, weap.negativeIndirect]
    for stat in range(len(negative)):
        if negative[stat] > 0:
            malus += "{0} : {1}\n".format(["Soins", "Boosts et Malus", "Armures et Mitigation",
                                          "Dégâts directs", "Dégâts indirects"][stat], negative[stat]*-1)
        elif negative[stat] < 0:
            bonus += "{0} : {1}\n".format(["Soins", "Boosts et Malus", "Armures et Mitigation",
                                          "Dégâts directs", "Dégâts indirects"][stat], negative[stat]*-1)

    if bonus != "":
        repEmb.add_field(name="__Bonus de statistiques :__",
                         value=bonus, inline=True)
    if malus != "":
        repEmb.add_field(name="__Malus de statistiques :__",
                         value=malus, inline=True)

    if weap.effect != None:
        infoEffect(weap.effect, user, repEmb, ctx)

    return repEmb

def infoOther(other: other, user: char):
    weap = other
    repEmb = discord.Embed(title=weap.name, color=user.color,
                           description=f"Icone : { weap. emoji}")
    repEmb.add_field(name="Description :", value=weap.description)

    if other in changeIconForm:
        repEmb.set_image(url=previewDict[other.id])

    return repEmb

def userMajStats(user: char, tabl: list):
    """What ?"""
    user.strength, user.endurance, user.charisma, user.agility, user.precision, user.intelligence, user.magie = tabl[
        0], tabl[1], tabl[2], tabl[3], tabl[4], tabl[5], tabl[6]
    return user

def restats(user: char):
    """Function for restat a user"""
    stats = user.allStats()
    for a in range(0, len(stats)):
        stats[a] = round(aspiStats[user.aspiration][a]*0.1 +
                         aspiStats[user.aspiration][a]*0.9*user.level/50)

    user.points = user.level
    user.majorPointsCount = user.stars
    user.bonusPoints = [0, 0, 0, 0, 0, 0, 0]
    user.majorPoints = [0, 0, 0, 0, 0, 0, 0]+[0, 0, 0]+[0, 0, 0, 0, 0]

    return userMajStats(user, stats)

def silentRestats(user: char):
    """Function for restat a user without reset the bonus points"""
    stats = user.allStats()
    for a in range(0, len(stats)):
        stats[a] = round(aspiStats[user.aspiration][a]*0.1 +
                         aspiStats[user.aspiration][a]*0.9*user.level/50)+user.bonusPoints[a]

    return userMajStats(user, stats)

async def addExpUser(bot: discord.Client, path: str, ctx: Union[discord.Message, discord_slash.SlashContext], exp=3, coins=0, send=True):
    user = loadCharFile(path)

    if user.level < 55:
        user.exp = user.exp + exp
    else:
        user.exp = 0
    user.currencies = user.currencies + coins

    upLvl = (user.level-1)*50+30

    while user.exp >= upLvl and user.level < 55:
        temp = user.allStats()
        up = [0, 0, 0, 0, 0, 0, 0]
        stats = user.allStats()
        for a in range(0, len(stats)):
            stats[a] = round(aspiStats[user.aspiration][a]*0.1 +
                             aspiStats[user.aspiration][a]*0.9*user.level/50+user.bonusPoints[a])
            temp[a] = round(aspiStats[user.aspiration][a]*0.1+aspiStats[user.aspiration]
                            [a]*0.9*(user.level+1)/50+user.bonusPoints[a])
            up[a] = temp[a]-stats[a]

        user.strength, user.endurance, user.charisma, user.agility, user.precision, user.intelligence, user.magie = temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6]

        level, ballerine = str(user.level+1) + ["", "<:littleStar:925860806602682369>{0}".format(user.stars)][user.stars > 0], await getUserIcon(bot, user)
        lvlEmbed = discord.Embed(title=f"__Montée de niveau__", color=user.color,
                                 description=f"{ballerine} {user.name} est passé au niveau {level} !\n\nForce : {user.strength} (+{up[0]})\nEndurance : {user.endurance} (+{up[1]})\nCharisme : {user.charisma} (+{up[2]})\nAgilité : {user.agility} (+{up[3]})\nPrécision : {user.precision} (+{up[4]})\nIntelligence : {user.intelligence} (+{up[5]})\nMagie : {user.magie} (+{up[6]})\n\nVous avez {user.points} bonus à répartir en utilisant la commande /points\.")

        for lvl in lvlUpUnlock:
            if user.level+1 == lvl:
                lvlEmbed.add_field(
                    name="__<:empty:866459463568850954>\nContenu débloqué :__", value=lvlUpUnlock[lvl], inline=False)
                break

        if (user.level+1) % 5 == 0:
            unlock = ""
            listUnlock = []
            for stuffy in user.stuffInventory:
                if stuffy.minLvl == user.level+1:
                    listUnlock.append(stuffy)

            if len(listUnlock) <= 10:
                for stuffy in listUnlock:
                    unlock += "{0} {1}\n".format(stuffy.emoji, stuffy.name)
            else:
                for stuffy in listUnlock[:10]:
                    unlock += "{0} {1}\n".format(stuffy.emoji, stuffy.name)
                unlock += "Et {0} autre(s)".format(len(listUnlock)-10)

            if unlock != "":
                lvlEmbed.add_field(
                    name="<:empty:866459463568850954>\n__Vous pouvez désormais équiper les objets de votre inventaire suivants :__", value=unlock)

        if send:
            if globalVar.getGuildBotChannel(ctx.guild.id) not in [0, None]:
                await ctx.guild.get_channel(globalVar.getGuildBotChannel(ctx.guild.id)).send(embed=lvlEmbed)
            else:
                await ctx.channel.send(embed=lvlEmbed)

        user.exp = user.exp - upLvl
        user.level = user.level + 1
        user.points = user.points + 1
        upLvl = (user.level-1)*50+30

        if user.level % 5 == 0 and user.autoStuff and user.level <= 50:
            user.stuff[0] = getAutoStuff(user.stuff[0],user,recommandedStuffStat[user.aspiration])
            user.stuff[1] = getAutoStuff(user.stuff[1],user,recommandedStuffStat[user.aspiration])
            user.stuff[2] = getAutoStuff(user.stuff[2],user,recommandedStuffStat[user.aspiration])

        if user.autoPoint:
            while user.points > 0:
                for recStat in recommandedStat[user.aspiration]:
                    if user.bonusPoints[recStat] < 30 and user.points > 0:
                        user.bonusPoints[recStat] += 1
                        user.points -= 1
    saveCharFile(user=user)
    return user

def getChoisenSelect(select: dict, value: str):
    trouv = False
    temp = copy.deepcopy(select)
    for a in temp["options"]:
        if a["value"] == value:
            trouv = True
            a["default"] = True
    if trouv:
        temp["disabled"] = True
    return temp

async def downloadAllHeadGearPng(bot: discord.Client, msg=None, lastTime=None):
    listEmojiHead = []
    for stuffy in stuffs:
        if stuffy.type == 0:
            listEmojiHead.append(stuffy.emoji)
    listDir = os.listdir("./data/images/headgears/")
    num, cmpt = len(listEmojiHead), 0
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
                image = requests.get(emoji_2.url, stream=True)
                image.raw.decode_content = True
                open(
                    f"./data/images/headgears/{emojiObject[0]}.png", "wb").write(image.content)
                image = Image.open(
                    f"./data/images/headgears/{emojiObject[0]}.png")
                image = image.resize((70, 70))
                image.save(f"./data/images/headgears/{emojiObject[0]}.png")
                print(emojiObject[0] + " downloaded")
            else:
                print(emojiObject[0] + " not found")

        if msg != None:
            cmpt += 1
            now = datetime.now().second
            if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
                lastTime = now
                await msg.edit(embed=discord.Embed(title="l!admin resetCustomEmoji", description="Téléchargement des images d'accessoires ({0}%)".format(round(cmpt/num*100, 1))))

async def downloadAllWeapPng(bot: discord.Client, msg=None, lastTime=None):
    listEmojiWeapon = []
    for weap in weapons:
        listEmojiWeapon.append(weap.emoji)
    listDir = os.listdir("./data/images/weapons/")
    num, cmpt = len(listEmojiWeapon+etInkBases+etInkLines), 0
    for a in listEmojiWeapon:
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
                image = requests.get(emoji_2.url, stream=True)
                image.raw.decode_content = True
                open(
                    f"./data/images/weapons/{emojiObject[0]}.png", "wb").write(image.content)
                image = Image.open(
                    f"./data/images/weapons/{emojiObject[0]}.png")
                background = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
                image = image.resize((100, 100))
                background.paste(image, (10, 10))

                background.save(f"./data/images/weapons/{emojiObject[0]}.png")
                print(emojiObject[0] + " downlowded")
            else:
                print(emojiObject[0] + " not found")

        if msg != None:
            cmpt += 1
            now = datetime.now().second
            if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
                lastTime = now
                await msg.edit(embed=discord.Embed(title="l!admin resetCustomEmoji", description="Téléchargement des images d'armes ({0}%)".format(round(cmpt/num*100, 1))))

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
                image = requests.get(emoji_2.url, stream=True)
                image.raw.decode_content = True
                open(
                    f"./data/images/weapons/{emojiObject[0]}.png", "wb").write(image.content)
                image = Image.open(
                    f"./data/images/weapons/{emojiObject[0]}.png")
                background = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
                image = image.resize((100, 100))
                background.paste(image, (10, 10))
                background = background.rotate(30)
                background.save(f"./data/images/weapons/{emojiObject[0]}.png")
                print(emojiObject[0] + " downlowded")
            else:
                print(emojiObject[0] + " not found")

        if msg != None:
            cmpt += 1
            now = datetime.now().second
            if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
                lastTime = now
                await msg.edit(embed=discord.Embed(title="l!admin resetCustomEmoji", description="Téléchargement des images d'armes ({0}%)".format(round(cmpt/num*100, 1))))

    if not(os.path.exists("./data/images/weapons/akifaux.png")):
        image = requests.get(
            "https://cdn.discordapp.com/emojis/887334842595942410.png?v=1", stream=True)
        image.raw.decode_content = True
        open(f"./data/images/weapons/akifaux.png", "wb").write(image.content)
        image = Image.open(f"./data/images/weapons/akifaux.png")
        background = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
        image = image.resize((100, 100))
        background.paste(image, (10, 10))
        background = background.rotate(30)
        background.save(f"./data/images/weapons/akifaux.png")
        print("akifaux downlowded")

async def downloadAllIconPng(bot: discord.Client):
    listEmojiHead = emoji.icon
    listDir = os.listdir("./data/images/char_icons/")
    for a in (1, 2, 4):
        for b in range(0, len(listEmojiHead[a])):
            emojiObject = getEmojiInfo(listEmojiHead[a][b])
            if emojiObject[0] + ".png" not in listDir:
                guildStuff = [862320563590529056, 615257372218097691,
                              810212019608485918, 894528703185424425]

                emoji_2 = None
                for c in guildStuff:
                    try:
                        guild = await bot.fetch_guild(c)
                        emoji_2 = await guild.fetch_emoji(emojiObject[1])
                    except:
                        pass

                if emoji_2 != None:
                    image = requests.get(emoji_2.url, stream=True)
                    image.raw.decode_content = True
                    open(
                        f"./data/images/char_icons/{emojiObject[0]}.png", "wb").write(image.content)
                    image = Image.open(
                        f"./data/images/char_icons/{emojiObject[0]}.png")
                    background = Image.new("RGBA", (145, 145), (0, 0, 0, 0))
                    image = image.resize((128, 128))
                    background.paste(image, ((145-128)//2, (145-128)//2))
                    background.save(
                        f"./data/images/char_icons/{emojiObject[0]}.png")
                    customIconDB.addIconFiles(a, b, f"{emojiObject[0]}.png")
                    print(emojiObject[0] + " downlowded")
                else:
                    print(emojiObject[0] + " not found")

async def makeCustomIcon(bot: discord.Client, user: char, returnImage: bool = False):
    # Paramètres de l'accessoire ----------------------------------
    if user.apparaAcc == None:
        accessoire, pos = Image.open("./data/images/headgears/{0}.png".format(
            getEmojiObject(user.stuff[0].emoji)["name"])), user.stuff[0].position

    else:
        accessoire, pos = Image.open("./data/images/headgears/{0}.png".format(
            getEmojiObject(user.apparaAcc.emoji)["name"])), user.apparaAcc.position

    # Récupération de l'icone de base -----------------------------
    tablBase = [["./data/images/char_icons/baseIka.png", "./data/images/char_icons/baseTako.png"], ["./data/images/char_icons/ikaCatBody.png", "./data/images/char_icons/takoCatBody.png"], ["./data/images/char_icons/komoriBody.png", "./data/images/char_icons/komoriBody.png"],
                ["./data/images/char_icons/birdColor.png", "./data/images/char_icons/birdColor.png"], ["./data/images/char_icons/skeletonColor.png", "./data/images/char_icons/skeletonColor.png"], ['./data/images/char_icons/fairyColor.png', './data/images/char_icons/fairy2Color.png']][user.iconForm]
    tablLine = [["./data/images/char_icons/empty_squid.png", "./data/images/char_icons/empty_octo.png"], ["./data/images/char_icons/ikaCatLine.png", "./data/images/char_icons/takoCatLine.png"], ["./data/images/char_icons/komoriLine.png", "./data/images/char_icons/komoriLine.png"],
                ["./data/images/char_icons/birdLine.png", "./data/images/char_icons/birdLine.png"], ["./data/images/char_icons/skeletonLine.png", "./data/images/char_icons/skeletonLine.png"], ["./data/images/char_icons/fairyLine.png", "./data/images/char_icons/fairy2Line.png"]][user.iconForm]
    background = Image.open(tablBase[user.species-1])
    background2 = None

    resizeByPos = [
        [   # IconForm 0
            [None, (round(accessoire.size[0]*1.3),
                    accessoire.size[1])],          # 0
            [(round(accessoire.size[0]*0.8), round(accessoire.size[1]*0.8))],    # 1
            [(round(accessoire.size[0]*1.2), round(accessoire.size[1]*0.7))],    # 2
            [(round(accessoire.size[0]*0.8), round(accessoire.size[1]*0.8))],    # 3
            # 4
            [None],
            [(round(accessoire.size[0]*1.2), round(accessoire.size[1]*0.7))],    # 5
            [None, (round(accessoire.size[0]*1.3),
                    accessoire.size[1])]           # 6
        ],
        [   # IconForm 1
            [None, (round(accessoire.size[0]*1.3), accessoire.size[1])],    # 0
            [(round(accessoire.size[0]*0.7), round(accessoire.size[1]*0.7))],    # 1
            [(round(accessoire.size[0]*1.2), round(accessoire.size[1]*0.7))],    # 2
            [(round(accessoire.size[0]*0.8), round(accessoire.size[1]*0.8))],    # 3
            [None],    # 4
            [(round(accessoire.size[0]*1.2), round(accessoire.size[1]*0.7))],    # 5
            [None, (round(accessoire.size[0]*1.3), accessoire.size[1])]     # 6
        ],
        [   # IconForm 2
            [(round(accessoire.size[0]*0.7), round(accessoire.size[1]*0.6))],    # 0
            [(round(accessoire.size[0]*0.35), round(accessoire.size[1]*0.35))],    # 1
            [(round(accessoire.size[0]*0.4), round(accessoire.size[1]*0.3))],    # 2
            [(round(accessoire.size[0]*0.5), round(accessoire.size[1]*0.5))],    # 3
            [None],    # 4
            [(round(accessoire.size[0]*0.6), round(accessoire.size[1]*0.4))],    # 5
            [(round(accessoire.size[0]*0.7), round(accessoire.size[1]*0.6))]     # 6
        ],
        [   # IconForm 3
            [(round(accessoire.size[0]*0.7), round(accessoire.size[1]*0.6))],    # 0
            [(round(accessoire.size[0]*0.35), round(accessoire.size[1]*0.35))],    # 1
            [(round(accessoire.size[0]*0.4), round(accessoire.size[1]*0.3))],    # 2
            [(round(accessoire.size[0]*0.5), round(accessoire.size[1]*0.5))],    # 3
            [None],    # 4
            [(round(accessoire.size[0]*0.6), round(accessoire.size[1]*0.4))],    # 5
            [(round(accessoire.size[0]*0.7), round(accessoire.size[1]*0.6))]     # 6
        ],
        [   # IconForm 4
            [None, (round(accessoire.size[0]*1.3),
                    accessoire.size[1])],          # 0
            [(round(accessoire.size[0]*0.8), round(accessoire.size[1]*0.8))],    # 1
            [(round(accessoire.size[0]*1.2), round(accessoire.size[1]*0.7))],    # 2
            [(round(accessoire.size[0]*0.8), round(accessoire.size[1]*0.8))],    # 3
            # 4
            [None],
            [(round(accessoire.size[0]*1.2), round(accessoire.size[1]*0.7))],    # 5
            [None, (round(accessoire.size[0]*1.3),
                    accessoire.size[1])]           # 6
        ],
        [   # IconForm 5
            [(round(accessoire.size[0]*1), round(accessoire.size[1]*0.8)),
             (round(accessoire.size[0]*1.3), accessoire.size[1])],          # 0
            [(round(accessoire.size[0]*0.7), round(accessoire.size[1]*0.7))],    # 1
            [(round(accessoire.size[0]*1.1), round(accessoire.size[1]*0.6))],    # 2
            [(round(accessoire.size[0]*0.8), round(accessoire.size[1]*0.8))],    # 3
            # 4
            [None],
            [(round(accessoire.size[0]*1.0), round(accessoire.size[1]*0.7))],    # 5
            [None, (round(accessoire.size[0]*1.3),
                    accessoire.size[1])]           # 6
        ]
    ]

    if len(resizeByPos[user.iconForm][pos]) > 1:
        if resizeByPos[user.iconForm][pos][user.species-1] != None:
            accessoire = accessoire.resize(
                resizeByPos[user.iconForm][pos][user.species-1])
    else:
        if resizeByPos[user.iconForm][pos][0] != None:
            accessoire = accessoire.resize(resizeByPos[user.iconForm][pos][0])

    tablPosByPos = [
        [   # IconForm 0
            [(round(background.size[0]/2-accessoire.size[0]/2), -10)
             ],                               # 0
            [(0, round(background.size[1]/2)-5),
             (3, round(background.size[1]/2)-5)],                  # 1
            [(round(background.size[0]/2-accessoire.size[0]/2),
              round(background.size[1]/2+20))],    # 2
            [(round(background.size[0]*0.25-accessoire.size[0]/2+8), 13),
             (round(background.size[0]*0.25-accessoire.size[0]/2+3), 7)],    # 3
            [(round(background.size[0]*0.20-accessoire.size[0]/2), 75)
             ],                             # 4
            [(round(background.size[0]/2-accessoire.size[0]/2),
              round(background.size[1]/2+10))],    # 5
            [(round(background.size[0]/2-accessoire.size[0]/2), -10)
             ]                                # 6
        ],
        [   # IconForm 1
            [(round(background.size[0]/2-accessoire.size[0]/2), -10)
             ],                               # 0
            [(5, round(background.size[1]*0.1)),
             (3, round(background.size[1]*0.1))],                  # 1
            [(round(background.size[0]/2-accessoire.size[0]/2),
              round(background.size[1]/2+20))],    # 2
            [(round(background.size[0]*0.25-accessoire.size[0]/2+8), 13),
             (round(background.size[0]*0.25-accessoire.size[0]/2+3), 7)],    # 3
            [(round(background.size[0]*0.20-accessoire.size[0]/2), 75)
             ],                             # 4
            [(round(background.size[0]/2-accessoire.size[0]/2),
              round(background.size[1]/2+10))],    # 5
            [(round(background.size[0]/2-accessoire.size[0]/2), -10)
             ]                                # 6
        ],
        [   # IconForm 2
            [(round(background.size[0]/2-accessoire.size[0]/2), 0)
             ],                                     # 0
            [(round(background.size[0]*0.25), 21)
             ],                                  # 1
            [(round(background.size[0]/2-accessoire.size[0]/2),
              round(background.size[1]/2+2))],      # 2
            [(round(background.size[0]*0.25), 15)
             ],                                  # 3
            [(round(background.size[0]*0.20-accessoire.size[0]/2), 75)
             ],                                 # 4
            [(round(background.size[0]/2-accessoire.size[0]/2),
              round(background.size[1]/2-18))],     # 5
            [(round(background.size[0]/2-accessoire.size[0]/2), 0)
             ]                                      # 6
        ],
        [   # IconForm 3
            [(round(background.size[0]/2-accessoire.size[0]/2), 0)
             ],                                     # 0
            [(round(background.size[0]*0.25), 21)
             ],                                  # 1
            [(round(background.size[0]/2-accessoire.size[0]/2),
              round(background.size[1]/2+2))],      # 2
            [(round(background.size[0]*0.25), 15)
             ],                                  # 3
            [(round(background.size[0]*0.20-accessoire.size[0]/2), 75)
             ],                                 # 4
            [(round(background.size[0]/2-accessoire.size[0]/2),
              round(background.size[1]/2-18))],     # 5
            [(round(background.size[0]/2-accessoire.size[0]/2), 0)
             ]                                      # 6
        ],
        [   # IconForm 4
            [(round(background.size[0]/2-accessoire.size[0]/2), -10)
             ],                               # 0
            [(0, round(background.size[1]/2)-5),
             (3, round(background.size[1]/2)-5)],                  # 1
            [(round(background.size[0]/2-accessoire.size[0]/2),
              round(background.size[1]/2+20))],    # 2
            [(round(background.size[0]*0.25-accessoire.size[0]/2+8), 13),
             (round(background.size[0]*0.25-accessoire.size[0]/2+3), 7)],    # 3
            [(round(background.size[0]*0.20-accessoire.size[0]/2), 75)
             ],                             # 4
            [(round(background.size[0]/2-accessoire.size[0]/2),
              round(background.size[1]/2+10))],    # 5
            [(round(background.size[0]/2-accessoire.size[0]/2), -10)
             ]                                # 6
        ],
        [   # IconForm 5
            [(round(background.size[0]/2-accessoire.size[0]/2), 0)
             ],                               # 0
            [(0, round(background.size[1]/2)-5),
             (3, round(background.size[1]/2)-5)],                  # 1
            [(round(background.size[0]/2-accessoire.size[0]/2),
              round(background.size[1]/2+20))],    # 2
            [(round(background.size[0]*0.25-accessoire.size[0]/2+8), 13),
             (round(background.size[0]*0.25-accessoire.size[0]/2+3), 7)],    # 3
            [(round(background.size[0]*0.20-accessoire.size[0]/2), 75)
             ],                             # 4
            [(round(background.size[0]/2-accessoire.size[0]/2),
              round(background.size[1]/2+10))],    # 5
            [(round(background.size[0]/2-accessoire.size[0]/2), 0)
             ]                                # 6
        ]
    ]

    if pos == 6 and user.showAcc:                                 # Behind
        background2 = Image.new("RGBA", background.size, (0, 0, 0, 0))

        if len(tablPosByPos[user.iconForm][pos]) > 1:
            if tablPosByPos[user.iconForm][pos][user.species-1] != None:
                position = (tablPosByPos[user.iconForm][pos][user.species-1])
            else:
                position = (0, 0)
        else:
            if tablPosByPos[user.iconForm][pos][0] != None:
                position = (tablPosByPos[user.iconForm][pos][0])
            else:
                position = (0, 0)

        background2.paste(accessoire, position, accessoire)
        accessoire.close()

    if user.stars > 0:
        if background2 == None:
            background2 = Image.new("RGBA", background.size, (0, 0, 0, 0))
        cmpt = 0
        while cmpt < user.stars:
            litStar = Image.open("./data/images/char_icons/littleStar.png")
            litStar = litStar.resize((38, 38))
            background2.paste(
                litStar, (33*(cmpt % 4)+5, 38*(cmpt//4)), litStar)
            litStar.close()
            cmpt += 1

    pixel = background.load()
    layer = Image.open(tablLine[user.species-1])

    colorToUse = user.colorHex.replace("0x", "#")
    if colorToUse == "None":
        if user.color != black:
            colorToUse = hex(user.color).replace("0x", "#")
        else:
            colorToUse = "#000000"
    baseUserColor = ImageColor.getcolor(colorToUse, "RGB")
    baseTemp = [baseUserColor[0], baseUserColor[1], baseUserColor[2]]
    for x in range(0, background.size[0]):
        for y in range(0, background.size[1]):
            if pixel[x, y] != (0, 0, 0, 0):
                color = list(pixel[x, y])
                for cmpt in (0, 1, 2):
                    color[cmpt] = color[cmpt]-121
                    baseTemp[cmpt] = min(
                        baseUserColor[cmpt] + color[cmpt], 255)

                background.putpixel([x, y], tuple(baseTemp+[pixel[x, y][3]]))

    background.paste(layer, [0, 0], layer)
    background.paste(layer, [0, 0], layer)

    if pos == 6 or user.stars > 0:
        background2.paste(background, [0, 0], background)
        background = background2

    # Récupération de l'icone de l'accessoire
    if user.showAcc:
        if pos == 3:                                          # Barettes
            accessoire = accessoire.rotate(30)
        if pos != 6:
            if len(tablPosByPos[user.iconForm][pos]) > 1:
                if tablPosByPos[user.iconForm][pos][user.species-1] != None:
                    position = (
                        tablPosByPos[user.iconForm][pos][user.species-1])
                else:
                    position = (0, 0)
            else:
                if tablPosByPos[user.iconForm][pos][0] != None:
                    position = (tablPosByPos[user.iconForm][pos][0])
                else:
                    position = (0, 0)
            if pos in [1, 4] and user.handed:
                position = (
                    background.size[0]-position[0]-accessoire.size[0], position[1])
                accessoire = ImageOps.mirror(accessoire)

            # Collage de l'accessoire
            background.paste(accessoire, position, accessoire)
            accessoire.close()

    # Récupération de l'icone de l'arme
    if user.showWeapon:
        weapEmName, weapToSee = getEmojiObject(user.weapon.emoji)[
            "name"], user.weapon
        if user.apparaWeap != None:
            weapEmName, weapToSee = getEmojiObject(user.apparaWeap.emoji)[
                "name"], user.apparaWeap

        if (user.apparaWeap != None and user.apparaWeap.id in eternalInkWeaponIds) or (user.apparaWeap == None and user.weapon.id in eternalInkWeaponIds):
            if user.apparaWeap != None:
                toBase = getEmojiObject(user.apparaWeap.emoji)["name"]
            else:
                toBase = getEmojiObject(user.weapon.emoji)["name"]
            line = Image.open(
                "./data/images/weapons/Line{0}.png".format(toBase))
            base = Image.open(
                "./data/images/weapons/Base{0}.png".format(toBase))

            pixel = base.load()
            baseTemp = [baseUserColor[0], baseUserColor[1], baseUserColor[2]]
            for x in range(0, base.size[0]):
                for y in range(0, base.size[1]):
                    if pixel[x, y] != (0, 0, 0, 0):
                        color = list(pixel[x, y])
                        for cmpt in (0, 1, 2):
                            color[cmpt] = color[cmpt]-143
                            baseTemp[cmpt] = min(
                                baseUserColor[cmpt] + color[cmpt], 255)
                        base.putpixel([x, y], tuple(baseTemp))
            base.paste(line, [0, 0], line)
            weapon = base
        elif "./data/images/weapons/{0}.png".format(weapEmName) != "./data/images/weapons/akifauxgif.png":
            weapon = Image.open(
                "./data/images/weapons/{0}.png".format(weapEmName))
        else:
            weapon = Image.open("./data/images/weapons/akifaux.png")

        if weapToSee.taille == 0:
            weapon = weapon.resize(
                [int(weapon.size[0]*0.8), int(weapon.size[0]*0.8)])
        elif weapToSee.taille == 2:
            weapon = weapon.resize(
                [int(weapon.size[0]*1.2), int(weapon.size[0]*1.2)])

        if user.handed == 1:
            weapon = ImageOps.mirror(weapon)
        if (user.apparaWeap == None and user.weapon.needRotate) or (user.apparaWeap != None and user.apparaWeap.needRotate):
            if user.handed == 1:
                weapon = weapon.rotate(-30)
            else:
                weapon = weapon.rotate(30)

        # Collage de l'arme
        background.paste(weapon, [(int(background.size[0]-weapon.size[0]*0.7)-10*int(weapToSee.taille == 0), 40+15*int(weapToSee.taille == 0)),
                         (int(0-weapon.size[0]*0.3)+10*int(weapToSee.taille == 0), 40+15*int(weapToSee.taille == 0))][user.handed], weapon)
        weapon.close()

    # Collage de l'élément
    if user.showElement:
        if user.level >= 30:
            element = Image.open(
                "./data/images/elemIcon/"+getEmojiObject(secElemEmojis[user.secElement])["name"]+".png")
            background.paste(element, [
                             (0, 90), (background.size[0]-element.size[0], 90)][user.handed], element)
            element.close()

        element = Image.open("./data/images/elemIcon/" +
                             getEmojiObject(elemEmojis[user.element])["name"]+".png")
        background.paste(element, [
                         (0, 90), (background.size[0]-element.size[0], 90)][user.handed], element)
        element.close()

    # Updating the new emote and the database
    imgByteArr = io.BytesIO()
    background.save(imgByteArr, format="png")
    background = imgByteArr.getvalue()

    if returnImage:
        return background

    iconGuildList = []
    if os.path.exists("../Kawi/"):
        iconGuildList = ShushyCustomIcons
    else:
        iconGuildList = LenaCustomIcons

    if not(customIconDB.haveCustomIcon(user)):
        for icGuild in iconGuildList:
            try:
                icGuild = await bot.fetch_guild(icGuild)
                if len(icGuild.emojis) < 50:
                    try:
                        new_icon = await asyncio.wait_for(icGuild.create_custom_emoji(name=remove_accents(user.name), image=background), timeout=1)
                        customIconDB.editCustomIcon(user, new_icon)
                        print(f"{user.name}'s new emoji uploaded")
                    except asyncio.TimeoutError:
                        print(
                            "{0}'s emoji took to long to upload".format(user.name))
                    break
            except:
                print_exc()

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
                try:
                    new_icon = await asyncio.wait_for(icGuild.create_custom_emoji(name=remove_accents(user.name), image=background), timeout=1)
                    customIconDB.editCustomIcon(user, new_icon)
                    print(f"{user.name}'s emoji updated")
                    await custom.delete()
                except asyncio.TimeoutError:
                    print("{0}'s emoji took to long to upload".format(user.name))
                break

async def getUserIcon(bot: discord.Client, user: char):
    """Function for get the user custom icon\nIf a (re)make is needed, remake the icon"""
    fun, toReturn = random.randint(0, 9999), None
    if fun == 666:
        toReturn = "<a:lostSilver:917783593441456198>"
    try:
        if customIconDB.isDifferent(user):
            await makeCustomIcon(bot, user)

        if customIconDB.haveCustomIcon(user):
            if customIconDB.getCustomIcon(user) not in [None, "None"]:
                toReturn = customIconDB.getCustomIcon(user)
            else:
                toReturn = "<:LenaWhat:760884455727955978>"
    except:
        print_exc()
        toReturn = "<:LenaWhat:760884455727955978>"
    if toReturn == None:
        return "<:LenaWhat:760884455727955978>"
    else:
        return toReturn

def infoInvoc(invoc: invoc, embed: discord.Embed):
    rep = f"__Aspiration de l'invocation :__ {aspiEmoji[invoc.aspiration]} {inspi[invoc.aspiration]}\n__Elément de l'invocation :__ {elemEmojis[invoc.element]} {elemNames[invoc.element]}\n__Description :__\n{invoc.description}\n\n__Statistique principale :__ **{nameStats[invoc.weapon.use]}**\n\n**__Statistiques :__**\n*\"Invoc\" est un raccourci pour \"Statistique de l'Invocateur\"*\n"

    stats = invoc.allStats()+[invoc.resistance, invoc.percing, invoc.critical]
    names = nameStats+nameStats2
    for a in range(0, len(stats)):
        if type(stats[a]) == list:
            if stats[a][0] == PURCENTAGE:
                rep += f"\n__{names[a]} :__ Invoc x{stats[a][1]}"
            elif stats[a][0] == HARMONIE:
                rep += f"\n__{names[a]} :__ Invoc : Harmonie"
        else:
            rep += f"\n__{names[a]} :__ {stats[a]}"

    embed.add_field(name="<:empty:866459463568850954>\n__" +
                    invoc.name+"__", value=rep, inline=False)
    rep = ""
    ranged = ["Mêlée", "Distance", "Longue Distance"][invoc.weapon.range]
    rep += f"{invoc.weapon.emoji} {invoc.weapon.name} ({ranged})"
    for a in invoc.skills:
        if type(a) == skill:
            if a.description == None:
                ranged = ["Monocible", "Zone"][int(a.area != AREA_MONO)]
                rep += f"\n{a.emoji} {a.name} ({tablTypeStr[a.type]}, {ranged})"
            else:
                rep += f"\n{a.emoji} __{a.name} :__\n> " + \
                    a.description.replace("\n", "\n> ") + "\n"

    embed.add_field(
        name="<:empty:866459463568850954>\n__Armes et compétences :__", value=rep, inline=False)
    return embed

def infoAllie(allie: tmpAllie):
    var = ""
    if allie.variant:
        var = "Cet allié temporaire est une variante d'un autre allié temporaire\n\n"
    rep = f"{var}__Aspiration :__ {inspi[allie.aspiration]}\n__Element :__ {elemEmojis[allie.element]} {elemNames[allie.element]} ({elemEmojis[allie.secElement]} {elemNames[allie.secElement]})\n__Description :__\n{allie.description}"
    allMaxStats, accStats, dressStats, flatsStats, statsWeapon = allie.allStats(), allie.stuff[0].allStats(
    ), allie.stuff[1].allStats(), allie.stuff[2].allStats(), allie.weapon.allStats()
    stats = ""
    for a in range(0, len(allMaxStats)):
        tempi = accStats[a]+dressStats[a]+flatsStats[a]+statsWeapon[a]
        stats += f"__{nameStats[a]}__ : {allMaxStats[a]} ({tempi})\n"

    stats2 = ""
    accStats = [allie.stuff[0].resistance,
                allie.stuff[0].percing, allie.stuff[0].critical]
    dressStats = [allie.stuff[1].resistance,
                  allie.stuff[1].percing, allie.stuff[1].critical]
    flatsStats = [allie.stuff[2].resistance,
                  allie.stuff[2].percing, allie.stuff[2].critical]
    weaponStats = [allie.weapon.resistance,
                   allie.weapon.percing, allie.weapon.critical]
    statsPlusName = nameStats2
    for num in range(3):
        summation = accStats[num] + dressStats[num] + \
            flatsStats[num] + weaponStats[num]
        if summation > 0:
            stats2 += f"__{statsPlusName[num]}__ : +{summation}\n"
        else:
            stats2 += f"__{statsPlusName[num]}__ : {summation}\n"

    accStats = [allie.stuff[0].negativeHeal, allie.stuff[0].negativeBoost,
                allie.stuff[0].negativeShield, allie.stuff[0].negativeDirect, allie.stuff[0].negativeIndirect]
    dressStats = [allie.stuff[1].negativeHeal, allie.stuff[1].negativeBoost,
                  allie.stuff[1].negativeShield, allie.stuff[1].negativeDirect, allie.stuff[1].negativeIndirect]
    flatsStats = [allie.stuff[2].negativeHeal, allie.stuff[2].negativeBoost,
                  allie.stuff[2].negativeShield, allie.stuff[2].negativeDirect, allie.stuff[2].negativeIndirect]
    statsPlusName = ["Soins", "Bonus/Malus",
                     "Armure", "Dégâts directs", "Dégâts indirect"]
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

    embed = discord.Embed(title="__Allié temporaire : "+allie.name+"__",
                          color=allie.color, description=rep+"\n<:empty:866459463568850954>")
    embed.add_field(
        name="__**Statistiques au niveau {0} :**__".format(allie.level), value=stats)
    embed.add_field(name="__**Statistiques secondaires :**__", value=stats2)
    if allie.icon[1] == "a":
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/{0}.gif".format(getEmojiObject(allie.icon)["id"]))
    else:
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(allie.icon)["id"]))

    if allie.changeDict != None:
        temp = ""
        msgChangeDict = ""
        for changeDictCell in allie.changeDict:
            if changeDictCell["changeWhat"] == 0:               # Change Skills
                for num in range(len(changeDictCell["to"])):
                    for skillNum in range(len(allie.skills)):
                        try:
                            if allie.skills[skillNum].id == changeDictCell["change"][num].id:
                                msgChangeDict += allie.skills[skillNum].emoji+" __"+allie.skills[skillNum].name + \
                                    "__ → " + \
                                    changeDictCell["to"][num].emoji+" __" + \
                                    changeDictCell["to"][num].name + "__\n"
                                if num != len(changeDictCell["to"])-1:
                                    changeSkill += ", "
                                    toSkill += ", "
                                break
                        except:
                            pass

            temp += "À partir du __niveau {1}__, cet allié temporaire a **{0}%** de chance d'avoir un build alternatif :\n{2}".format(
                changeDictCell["proba"], changeDictCell["level"], msgChangeDict)
        embed.add_field(
            name="<:empty:866459463568850954>\n__Build alternatif :__", value=temp, inline=False)

    return embed

def infoEnnemi(ennemi: octarien):
    rep = f"__Aspiration :__ {inspi[ennemi.aspiration]}\n__Niveau Minimum :__ {ennemi.baseLvl}\n__Element :__ {elemEmojis[ennemi.element]} {elemNames[ennemi.element]}\n\n__Description :__\n{ennemi.description}\n\n__**Statistiques au niveau 50 :**__\n*Entre parenthèse : Les bonus donnés par l'équipement*\n"
    allMaxStats, accStats, dressStats, flatsStats, weapStats = ennemi.allStats(), ennemi.stuff[0].allStats(
    ), ennemi.stuff[1].allStats(), ennemi.stuff[2].allStats(), ennemi.weapon.allStats()
    for a in range(0, len(allMaxStats)):
        temp, tempi = allMaxStats[a], accStats[a] + \
            dressStats[a]+flatsStats[a]+weapStats[a]
        rep += f"\n__{nameStats[a]}__ : {temp} ({tempi})"

    rep += f"\n\n__**Arme et compétences** :__\n{ennemi.weapon.emoji} {ennemi.weapon.name}\n"
    for a in ennemi.skills:
        if type(a) == skill:
            rep += f"\n{a.emoji} {a.name}"

    embed = discord.Embed(title="__Ennemis : "+ennemi.name +
                          "__", color=ennemi.color, description=rep)
    if ennemi.icon[1] == "a":
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/{0}.gif".format(getEmojiObject(ennemi.icon)["id"]))
    else:
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(ennemi.icon)["id"]))
    return embed

def getAutoStuff(object: stuff, user: char, tablStats = None):
    if user.level//5 == object.minLvl//5 or (object.minLvl == 50 and user.level >= 50):
        return object
    else:
        if tablStats == None:
            tablAllStats = object.allStats()+[object.resistance, object.percing, object.critical]+[object.negativeHeal*-1, object.negativeBoost*-1, object.negativeShield*-1, object.negativeDirect*-1, object.negativeIndirect*-1]

            for comp in user.skills:
                if type(comp) == skill and comp.use not in [None, HARMONIE]:
                    tablAllStats[comp.use] += 1
            dictList = []
            for cmpt in range(len(tablAllStats)):
                dictList.append({"Stats": cmpt, "Value": tablAllStats[cmpt]})

            dictList.sort(key=lambda ballerine: ballerine["Value"], reverse=True)
            dictList = dictList[0:3]

            statsMaxPlace = []
            for a in dictList:
                if a["Value"] > 0:
                    statsMaxPlace.append(a["Stats"])
        
        else:
            statsMaxPlace = tablStats

        if type(user) == char:
            tablToSee = copy.deepcopy(user.stuffInventory)
        elif type(user) == tmpAllie:
            tablToSee = copy.deepcopy(stuffs)

        def getSortValue(obj: stuff, statsMaxPlace=statsMaxPlace, aff=False):
            if obj.effect != None and findEffect(obj.effect).id == summonerMalus.id and (object.effect == None or findEffect(object.effect).id != summonerMalus.id):
                return -maxsize
            objStats = obj.allStats()+[obj.resistance, obj.percing, obj.critical]+[obj.negativeHeal*-1, obj.negativeBoost*-1, obj.negativeShield*-1, obj.negativeDirect*-1, obj.negativeIndirect*-1]
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
            tablToSee.sort(key=lambda ballerine: getSortValue(ballerine), reverse=True)
            return tablToSee[0]
        else:
            return [bbandeau, bshirt, bshoes][object.type]

async def downloadElementIcon(bot: discord.Client):
    listEmojiHead = elemEmojis+secElemEmojis
    listDir = os.listdir("./data/images/elemIcon/")
    for b in range(len(listEmojiHead)):
        emojiObject = getEmojiInfo(listEmojiHead[b])
        if emojiObject[0] + ".png" not in listDir:
            guildStuff = [615257372218097691,
                          932941135276560455, 862320563590529056]

            emoji_2 = None
            for c in guildStuff:
                try:
                    guild = await bot.fetch_guild(c)
                    emoji_2 = await guild.fetch_emoji(emojiObject[1])
                except:
                    pass

            if emoji_2 != None:
                image = requests.get(emoji_2.url, stream=True)
                image.raw.decode_content = True
                open(
                    f"./data/images/elemIcon/{emojiObject[0]}.png", "wb").write(image.content)
                image = Image.open(
                    f"./data/images/elemIcon/{emojiObject[0]}.png")
                image = image.resize((60, 60))
                image.save(f"./data/images/elemIcon/{emojiObject[0]}.png")
                print(emojiObject[0] + " downlowded")
            else:
                print(emojiObject[0] + " not found")

async def getRandomStatsEmbed(bot: discord.Client, team: List[classes.char], text="Chargement...") -> discord.Embed:
    if random.randint(0, 99) < 50:
        desc = "<:alice:908902054959939664> :\n\""
        whatRandomStat = random.randint(0, len(tablAdd)-1)
        randomStat = tablAdd[whatRandomStat]
        rdm2 = ["max", "total"][random.randint(0, 1)]

        listDict = []
        for perso in team:
            if type(perso) == char:
                value = aliceStatsDb.getUserStats(perso, rdm2+randomStat)
                if value > 0:
                    listDict.append(
                        {"name": perso.name, "value": value, "char": perso})

        if len(listDict) > 0:
            if len(listDict) == 1:
                choisen = listDict[0]
            else:
                choisen = listDict[random.randint(0, len(listDict)-1)]

            if rdm2 == "max":
                msgMax = [randomMaxDmg, randomMaxKill, randomMaxRes,
                          randomMaxTank, randomMaxHeal, randomMaxArmor, randomMaxSupp]
            else:
                msgMax = [randomTotalDmg, randomTotalKill, randomTotalRes,
                          randomTotalTank, randomTotalHeal, randomTotalArmor, randomTotalSupp]

            try:
                desc += msgMax[whatRandomStat][random.randint(0, len(msgMax[whatRandomStat])-1)].format(icon=await getUserIcon(bot, choisen["char"]), value=separeUnit(int(choisen["value"])), name=choisen["name"], il=["il", "elle"][choisen["char"].gender == GENDER_FEMALE], e=["", "e"][choisen["char"].gender == GENDER_FEMALE])
            except:
                desc += "placeholder.error.unknow"

            biggest = random.randint(0, 4)
            if biggest < 2:
                if rdm2 == "max":
                    records = aliceStatsDb.getRecord(
                        "max{0}".format(randomStat))
                    if int(records["owner"]) == int(choisen["char"].owner):
                        desc += "\n\nC'est d'ailleurs le record tiens"
                    else:
                        try:
                            recorder = loadCharFile(
                                absPath + "/userProfile/" + str(records["owner"]) + ".prof")
                            desc += "\n\n"+randomRecordMsg[random.randint(0, len(randomRecordMsg)-1)].format(icon=await getUserIcon(bot, recorder), value=separeUnit(int(records["value"])), name=recorder.name, il=["il", "elle"][recorder.gender == GENDER_FEMALE], e=["", "e"][recorder.gender == GENDER_FEMALE])
                        except:
                            desc += "\n\nJ'ai pas pu trouver qui avait le record, par contre"
                elif len(team) > 1:
                    summation = 0
                    for di in listDict:
                        summation += int(di["value"])

                    desc += "\n\n"+randomPurcenMsg[random.randint(0, len(randomPurcenMsg)-1)].format(
                        purcent=int(choisen["value"]/summation*100))

        else:
            rand = [0, len(aliceStatsNothingToShow[whatRandomStat]) -
                    1][len(aliceStatsNothingToShow[whatRandomStat]) > 1]
            desc += aliceStatsNothingToShow[whatRandomStat][rand]
        return discord.Embed(title="__{0}__".format(text), color=aliceColor, description=desc+"\"")
    else:
        return discord.Embed(title="__{0}__".format(text), color=light_blue, description="<:lena:909047343876288552> :\n\""+lenaTipsMsgTabl[random.randint(0, len(lenaTipsMsgTabl)-1)]+"\"")

async def getFullteamEmbed(bot: discord.Client, team: List[char], mainUser: char) -> discord.Embed:
    toReturn, tablFullCat, maxLenght = discord.Embed(title="__Equipe de {0} :__".format(
        mainUser.name), color=mainUser.color), ["Arme", "Acc.", "Vêt.", "Chaus."], 25 - (5*len(team)//4)

    for user in team:
        tablAnsCat, tablAnsEmoji, temp = [user.weapon.name, user.stuff[0].name, user.stuff[1].name, user.stuff[2].name], [
            user.weapon.emoji, user.stuff[0].emoji, user.stuff[1].emoji, user.stuff[2].emoji], ""

        # Level
        if user.stars < 1:
            temp += "__Niv. :__ {0}".format(user.level)
        else:
            temp += "__Niv. :__ {0}\\⭐{1}".format(user.level, user.stars)

        # Aspiration & Element
        temp += "\n__Aspi. :__ {0} {1}\n__Elem. :__ {2} {3} ({4} {5})\n".format(
            aspiEmoji[user.aspiration], inspi[user.aspiration], elemEmojis[user.element], elemNames[user.element], secElemEmojis[user.secElement], elemNames[user.secElement])

        # Weapon & Stuff
        for cmpt in range(4):
            if len(tablAnsCat[cmpt]) > maxLenght:
                temp += "\n__{0} :__ {1}".format(
                    tablFullCat[cmpt], tablAnsEmoji[cmpt])
                tempTemp, tablWord = "", []
                for letter in tablAnsCat[cmpt]:
                    if letter == " ":
                        if len(tempTemp) > 2:
                            tablWord.append(tempTemp)
                            tempTemp = ""
                    else:
                        tempTemp += letter
                if len(tempTemp) > 2:
                    tablWord.append(tempTemp)

                for word in tablWord:
                    if len(word) > 4:
                        temp += " {0}.".format(word[:3])
                    elif len(word) > 2:
                        temp += " {0}".format(word)
            else:
                temp += "\n__{0} :__ {1} {2}".format(
                    tablFullCat[cmpt], tablAnsEmoji[cmpt], tablAnsCat[cmpt])

        # Skill
        for nbDispSkill in range(len(lvlToUnlockSkill)):
            if user.level < lvlToUnlockSkill[nbDispSkill]:
                break
        temp += "\n\n__Compétences :__"
        for cmpt in range(7):
            skilly = findSkill(user.skills[cmpt])
            if skilly != None:
                temp += "\n{0}".format(skilly.emoji)
                if len(skilly.name) < 25:
                    temp += " "+skilly.name
                else:
                    tempTemp, tablWord = "", []
                    for letter in skilly.name:
                        if letter == " ":
                            if len(tempTemp) > 2:
                                tablWord.append(tempTemp)
                                tempTemp = ""
                        else:
                            tempTemp += letter
                    if len(tempTemp) > 2:
                        tablWord.append(tempTemp)
                    for word in tablWord:
                        if len(word) > 6:
                            temp += " {0}.".format(word[:5])
                        elif len(word) > 2:
                            temp += " {0}".format(word)
            elif cmpt <= nbDispSkill:
                temp += "\n -"

        if len(temp) > 1024:
            temp = completlyRemoveEmoji(temp)
        toReturn.add_field(name="{0} __{1}__".format(await getUserIcon(bot, user), user.name), value=temp)

    if len(toReturn) > 6000:
        print("To much ({0})".format(len(toReturn)))
        tempEmb = discord.Embed(title=toReturn.title, color=toReturn.color)
        for fields in toReturn.fields:
            tempEmb.add_field(name=fields.name,
                              value=completlyRemoveEmoji(fields.value))
        toReturn = tempEmb
        print(len(toReturn))

    print(len(toReturn))
    return toReturn

def updateHaveProcurOn():
    dictHaveProcur, listUserId = [], []
    for temp in os.listdir("./userProfile/"):
        listUserId.append(int(temp.replace(".prof","")))

    for temp in listUserId:
        dictHaveProcur.append((temp,[]))

    dictHaveProcur = dict(dictHaveProcur)

    for temp in listUserId:
        user = loadCharFile("./userProfile/"+str(temp)+".prof")
        for procur in user.procuration:
            if int(procur) != user.owner:
                dictHaveProcur[int(procur)].append(user.owner)
    
    for userId in dictHaveProcur:
        if dictHaveProcur[userId] != []:
            user = loadCharFile("./userProfile/"+str(userId)+".prof")
            user.haveProcurOn = dictHaveProcur[userId]
            saveCharFile(user=user)
            print("Les procurations de {0} ont bien été mise à jour".format(user.name))
