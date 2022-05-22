import discord, random, os, emoji, asyncio, datetime, copy
from discord_slash.context import SlashContext
from discord_slash.utils.manage_components import create_actionrow, create_select, create_select_option, create_button
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from commands_files.sussess_endler import *
from commands_files.alice_stats_endler import *
from traceback import format_exc
from typing import Union, List
from sys import maxsize
from socket import error as SocketError
import errno

teamWinDB = dbHandler("teamVic.db")
AI_DPT,AI_BOOST,AI_SHIELD,AI_AVENTURE,AI_ALTRUISTE,AI_OFFERUDIT,AI_MAGE,AI_ENCHANT = 0,1,2,3,4,5,6,7
moveEmoji = ['⬅️','➡️','⬆️','⬇️']
cancelButton = create_actionrow(create_button(ButtonStyle.grey,"Retour",'◀️',custom_id="return"))
waitingSelect = create_actionrow(create_select([create_select_option("Veuillez prendre votre mal en patience","wainting...",'🕰️',default=True)],disabled=True))


tablIsNpcName = []
for a in tablAllAllies + tablVarAllies + ["Liu","Lia","Liz","Lio","Ailill","Kiku","Stella","Séréna"]:
    if type(a) != str:
        tablIsNpcName.append(a.name)
    else:
        tablIsNpcName.append(a)

temp = []
for a in tablIsNpcName:
    temp.append((a,False))

primitiveDictIsNpcVar = dict(temp)

def getPartnerValue(user : classes.char):
    if user.aspiration in [BERSERK,POIDS_PLUME,TETE_BRULE,ENCHANTEUR]:
        return 10 + random.randint(-3,3)
    elif user.aspiration in [PROTECTEUR,ATTENTIF]:
        return 8 + random.randint(-3,3)
    elif user.aspiration in [OBSERVATEUR,VIGILANT,MAGE,SORCELER]:
        return 6 + random.randint(-3,3)
    else:
        return 4 + random.randint(-3,3)

def dmgCalculator(caster, target, basePower, use, actionStat, danger, area, typeDmg = TYPE_DAMAGE, skillPercing = 0):
    if use == HARMONIE:
        maxi, stats = -100, caster.allStats()
        for cmpt in range(0,7):
            if stats[cmpt] > maxi:
                maxi, use = stats[cmpt], cmpt 
    if use not in [FIXE,None]:
        dmgBonusMelee = int(caster.aspiration in [BERSERK,POIDS_PLUME,TETE_BRULE,ENCHANTEUR] and caster.char.weapon.range == RANGE_MELEE) * caster.endurance/150*0.1 +1
        resistFactor = (1-(min(95,target.resistance*(1-(caster.percing+skillPercing)/100))/100))
        dmg = round(basePower * (max(-65,caster.allStats()[use]+100-caster.actionStats()[actionStat]))/100 *(danger/100)*caster.getElementalBonus(target=target,area=area,type=typeDmg)*(1+(0.01*caster.level)))*dmgBonusMelee
        target.stats.damageResisted += dmg - (dmg*resistFactor)
        return max(1,round(dmg*resistFactor))
    else:
        return basePower

def indirectDmgCalculator(caster, target, basePower, use, danger, area):
    damage = ""
    dmgBonusMelee = int(caster.aspiration in [BERSERK,POIDS_PLUME,TETE_BRULE,ENCHANTEUR] and caster.char.weapon.range == RANGE_MELEE) * caster.endurance/150*0.1 +1
    if use != None:
        if use != HARMONIE:
            stat = caster.allStats()[use]-caster.negativeIndirect
        else:
            stat = max(caster.allStats())

        effMultiplier = 100
        for eff in caster.effect:
            if eff.effect.id == dmgUp.id:
                effMultiplier += eff.effect.power
            elif eff.effect.id == dmgDown.id:
                effMultiplier -= eff.effect.power
        for eff in target.effect:
            if eff.effect.id in [vulne.id,kikuRaiseEff.id]:
                effMultiplier += eff.effect.power
            elif eff.effect.id == defenseUp.id:
                effMultiplier -= eff.effect.power
            elif eff.effect.inkResistance != 0:
                effMultiplier -= eff.effect.inkResistance
            
        effMultiplier = max(effMultiplier, 5)
        effMultiplier = min(effMultiplier, 200)

        selfElem = caster.getElementalBonus(target,area,TYPE_INDIRECT_DAMAGE)
        dangerMul = [100, danger][caster.team == 1]
        damage = basePower * (1+(stat/100)) *  (1-(min(95,target.resistance*(1-caster.percing/100))/100)) * selfElem * (1+(0.01*target.level)) * effMultiplier/100 * dangerMul/100 * dmgBonusMelee

    return damage

class timeline:
    """Classe de la timeline"""
    def __init__(self):
        self.timeline = []
        self.initTimeline = []
        self.begin = None

    def init(self,tablEntTeam : list):
        timeline = []

        for tabl in (0,1):
            tablPrio, tablNorm, tablLast = [],[],[]

            for ent in tablEntTeam[tabl]:
                suppSkillsCount,healSkillsCount = 0,0
                for skil in ent.char.skills:
                    if type(skil) == skill:
                        if skil.type in [TYPE_BOOST,TYPE_MALUS] or skil.id in [invocBat2.id]:
                            suppSkillsCount += 1
                        elif skil.type in [TYPE_ARMOR,TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_RESURECTION] or skil.id in [idoOSEff.id,proOSEff.id,preOSEff.id,invocSeraf.id,idoOHEff.id,proOHEff.id,altOHEff.id,lightAura.id,lightAura2.id,invocFee.id,lapSkill.id]:
                            healSkillsCount += 1

                if (suppSkillsCount >= 3 and random.randint(0,99)<50) or (ent.char.weapon.range == RANGE_MELEE and random.randint(0,99)<33):
                    tablPrio.append(ent)
                elif healSkillsCount >= 3 and random.randint(0,99)<50:
                    tablLast.append(ent)
                else:
                    tablNorm.append(ent)

            tabltabl = [tablPrio,tablNorm,tablLast]
            for cmpt in (0,1,2):
                random.shuffle(tabltabl[cmpt])

            tablEntTeam[tabl] = tabltabl[0]+tabltabl[1]+tabltabl[2]
        for a in range(max(len(tablEntTeam[0]),len(tablEntTeam[1]))):
            try:
                timeline+=[tablEntTeam[0][a]]
            except:
                pass
            try:
                timeline+=[tablEntTeam[1][a]]
            except:
                pass

        self.timeline = timeline
        self.initTimeline = copy.copy(timeline)
        self.begin = self.initTimeline[0]

        return self, tablEntTeam

    def getActTurn(self):
        return self.timeline[0]

    def icons(self):
        temp = ""
        for a in self.timeline:
            if a == self.initTimeline[-1]:
                temp += f"{a.icon} <|- "
            else:
                temp += f"{a.icon} <- "
        return temp

    def endOfTurn(self,tablEntTeam,tablAliveInvoc):
        timelineTempo = self.timeline
        actTurn = timelineTempo[0]

        timelineTempo.remove(actTurn)
        timelineTempo.append(actTurn)

        for ent in self.timeline[:]:
            if ent.hp <= 0 and type(ent.char) == invoc:
                inv = ent
                timelineTempo.remove(inv)
                inv.cell.on = None
                for ent2 in tablEntTeam[inv.team]:
                    if ent2.id == inv.summoner.id:
                        smn = ent2
                        smn.stats.damageDeal += inv.stats.damageDeal
                        smn.stats.indirectDamageDeal += inv.stats.indirectDamageDeal
                        smn.stats.ennemiKill += inv.stats.ennemiKill
                        smn.stats.damageRecived += inv.stats.damageRecived
                        smn.stats.heals += inv.stats.heals
                        smn.stats.damageOnShield += inv.stats.damageOnShield
                        smn.stats.shieldGived += inv.stats.shieldGived

                        for dictElem in inv.ownEffect:
                            for on, effID in dictElem.items():
                                for effOn in on.effect:
                                    if effOn.id == effID:
                                        effOn.caster = smn
                                        effOn.effect.power = int(effOn.effect.power * 0.7)
                                        break

                                on.refreshEffects()

                        smn.ownEffect += inv.ownEffect
                        break

                tablEntTeam[inv.team].remove(inv)
                tablAliveInvoc[inv.team] -= 1

        self.timeline = timelineTempo
        return tablEntTeam, tablAliveInvoc

def getDirection(cell1,cell2):
    xDif, yDif = cell1.x-cell2.x, cell1.y-cell2.y
    if abs(xDif) > abs(yDif):
        if xDif < 0:
            return FROM_LEFT
        elif xDif > 0:
            return FROM_RIGHT
    elif abs(xDif) < abs(yDif):
        if yDif > 0:
            return FROM_UP
        elif yDif < 0:
            return FROM_DOWN
    return FROM_POINT
            
class cell:
    """
        The base class for the board\n
        \n
        Attributs :\n
        x : The collum of the cell. Between ``0`` and ``5``
        y : The line of the cell. Between ``0`` and ``4``
        id : The number of the cell. Between ``0`` and ``30``
        on : The object who's on the cell. ``entity`` or ``None``
    """
    def __init__(self,x : int, y : int, id : int, tablAllCells):
        self.x = x
        self.y = y
        self.id = id
        self.on = None
        self.tablAllCells:list = tablAllCells

    def distance(self,cell):
        """Return the distance with the other cell"""
        return int(abs(self.x - cell.x)+abs(self.y - cell.y))

    def getArea(self,area=AREA_MONO,team=0,fromCell=None) -> list:
        """
            Return a list of the cells in the area\n\n
            Parameters :\n
            area : See ``constantes``
            team : The team of the entity who's looking for the area
        """
        rep = []

        # Circles
        if area==AREA_MONO:
            return [self]
        elif area in [AREA_CIRCLE_1,AREA_CIRCLE_2,AREA_CIRCLE_3,AREA_CIRCLE_4,AREA_CIRCLE_5,AREA_CIRCLE_6,AREA_CIRCLE_7,AREA_DONUT_1,AREA_DONUT_2,AREA_DONUT_3,AREA_DONUT_4,AREA_DONUT_5,AREA_DONUT_6,AREA_DONUT_7,AREA_DIST_3,AREA_DIST_4,AREA_DIST_5,AREA_DIST_6,AREA_DIST_7]:
            dist = area
            if area > AREA_CIRCLE_7:
                if area <= AREA_DONUT_7:
                    dist -= AREA_DONUT_1-1
                elif area <= AREA_DIST_7:
                    dist -= AREA_DIST_3-3

            for a in self.tablAllCells:
                if self.distance(cell=a) <= dist:
                    rep.append(a)

            if area > AREA_CIRCLE_7 and area <= AREA_DONUT_7: # If donut, remove the center
                rep.remove(self)
            elif area > AREA_DONUT_7 and area <= AREA_DIST_7: # If dist only, remove melee
                for a in rep[:]:
                    if self.distance(cell=a) <= 2:
                        rep.remove(a)
        elif area in [AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES]:
            return self.tablAllCells
        elif area in [AREA_CONE_2,AREA_CONE_3,AREA_CONE_4,AREA_CONE_5,AREA_CONE_6,AREA_CONE_7]:
            areaTabl, coneLength, direction = [self],area-(AREA_CONE_2-1), getDirection(fromCell,self)
            if direction == FROM_LEFT:
                for cmpt in range(coneLength+1):
                    for celly in self.tablAllCells:
                        if celly not in areaTabl:
                            if celly == self:
                                areaTabl.append(celly)
                            elif celly.x == self.x+(cmpt-1) and celly.x >=self.x:
                                if ((celly.y>self.y and celly.y < self.y+cmpt) or (celly.y<self.y and celly.y > self.y-cmpt) or (celly.y == self.y)):
                                    areaTabl.append(celly)
            elif direction == FROM_RIGHT:
                for cmpt in range(coneLength+1):
                    for celly in self.tablAllCells:
                        if celly not in areaTabl:
                            if celly == self:
                                areaTabl.append(celly)
                            elif celly.x == self.x-(cmpt-1) and celly.x <= self.x:
                                if ((celly.y>self.y and celly.y < self.y+cmpt) or (celly.y<self.y and celly.y > self.y-cmpt) or (celly.y == self.y)):
                                    areaTabl.append(celly)
            elif direction == FROM_UP:
                for cmpt in range(coneLength+1):
                    for celly in self.tablAllCells:
                            if celly not in areaTabl:
                                if celly == self:
                                    areaTabl.append(celly)
                                elif celly.y == self.y+(cmpt-1) and celly.y >= self.y:
                                    if ((celly.x>self.x and celly.x < self.x+cmpt) or (celly.x<self.x and celly.x > self.x-cmpt) or (celly.x == self.x)):
                                        areaTabl.append(celly)
            elif direction == FROM_DOWN:
                for cmpt in range(coneLength+1):
                    for celly in self.tablAllCells:
                            if celly not in areaTabl:
                                if celly == self:
                                    areaTabl.append(celly)
                                elif celly.y == self.y-(cmpt-1) and celly.y <= self.y:
                                    if ((celly.x>self.x and celly.x < self.x+cmpt) or (celly.x<self.x and celly.x > self.x-cmpt) or (celly.x == self.x)):
                                        areaTabl.append(celly)
            
            return areaTabl
        elif area in [17,18,19,20,21]: # Lines
            direction = getDirection(self,fromCell)
            if direction == FROM_LEFT:
                for a in self.tablAllCells:
                    if self.y == a.y and (a.x - self.x <= area-16 and a.x - self.x >= 0):
                        rep.append(a)
            elif direction == FROM_RIGHT:
                for a in self.tablAllCells:
                    if self.y == a.y and (a.x - self.x <= area-16 and a.x - self.x <= 0):
                        rep.append(a)
            elif direction == FROM_UP:
                for a in self.tablAllCells:
                    if self.x == a.x and (a.y - self.y <= area-16 and a.y - self.y >= 0):
                        rep.append(a)
            elif direction == FROM_DOWN:
                for a in self.tablAllCells:
                    if self.x == a.x and (a.y - self.y <= area-16 and a.y - self.y <= 0):
                        rep.append(a)

        elif area in [AREA_ARC_1,AREA_ARC_2,AREA_ARC_3]: # Arcs
            cmptx, direction = 1, getDirection(self,fromCell)
            if direction in [FROM_LEFT,FROM_RIGHT]:
                while cmptx < area - 32:
                    if direction == FROM_LEFT:
                        cell1 = findCell(self.x-cmptx,self.y-cmptx,self.tablAllCells)
                        if cell1 != None:
                            rep.append(cell1)
                        cell2 = findCell(self.x-cmptx,self.y+cmptx,self.tablAllCells)
                        if cell2 != None:
                            rep.append(cell2)
                    else:
                        cell1 = findCell(self.x+cmptx,self.y-cmptx,self.tablAllCells)
                        if cell1 != None:
                            rep.append(cell1)
                        cell2 = findCell(self.x+cmptx,self.y+cmptx,self.tablAllCells)
                        if cell2 != None:
                            rep.append(cell2)
                    cmptx+=1
            else:
                while cmptx < area - 32:
                    if direction == FROM_UP:
                        cell1 = findCell(self.x-cmptx,self.y+cmptx,self.tablAllCells)
                        if cell1 != None:
                            rep.append(cell1)
                        cell2 = findCell(self.x-cmptx,self.y+cmptx,self.tablAllCells)
                        if cell2 != None:
                            rep.append(cell2)
                    else:
                        cell1 = findCell(self.x+cmptx,self.y-cmptx,self.tablAllCells)
                        if cell1 != None:
                            rep.append(cell1)
                        cell2 = findCell(self.x+cmptx,self.y-cmptx,self.tablAllCells)
                        if cell2 != None:
                            rep.append(cell2)
                    cmptx+=1
            rep.append(self)
        elif area in [AREA_RANDOMENNEMI_1,AREA_RANDOMENNEMI_2,AREA_RANDOMENNEMI_3,AREA_RANDOMENNEMI_4,AREA_RANDOMENNEMI_5]:
            for cell in self.tablAllCells:
                if cell.on != None and cell.on.team != team:
                    rep.append(cell)
            random.shuffle(rep)
            return rep[0:min(area-AREA_RANDOMENNEMI_1+1,len(rep))]
        elif area in [AREA_INLINE_2,AREA_INLINE_3,AREA_INLINE_4,AREA_INLINE_5]:
            for celly in self.tablAllCells:
                if (celly.x == self.x or celly.y == self.y) and self.distance(celly) <= area + 2 - AREA_INLINE_2:
                    rep.append(celly)
        return rep

    def getEntityOnArea(self,area=AREA_MONO,team=0,wanted=ALLIES,lineOfSight=False,lifeUnderPurcentage=100,dead=False,effect=[None],ignoreInvoc = False, directTarget=True,ignoreAspiration = None,fromCell=None) -> list: 
        """
            Return a list of the targetable entities in the area\n
            \n
            Parameters :\n
            .area : See ``constantes``
            .team : The team of the entity who's looking in the area. ``0`` for Blue Team (and Default), ``1`` else for the Red Team
            .wanted : Who are we looking for ? ``ALLIES`` for the allies of the entity (and Default), ``ENNEMIS`` else
            .lineOfSight : Do we look for the line of sight ? Default ``False``
                -> The line of sight will always be ignore if Wanted is at ``ALLIES`` or Area is in ``AREA_ALL_ALLIES,AREA_ALL_ENNEMIS,AREA_ALL_ENTITIES``
            .lifeUnderPurcentage : Only select entities under or egal at ``lifeUnderPurcentage``% of their maxHp. Default ``100``
            .dead : Are we looking for dead entities ? Default ``False``
            .effect : A list of ``effect``objects. If the entities can't be applyed a effect of the list, exclude them. Defaul ``[None]``
            .ignoreInvoc : Do we ignore the summons ? Default ``False``
            .directTarget : Do we take into account the Untargetable status effect ? Default ``True``
            .ignoreAspiration : Do we need to ignore certains entities for their aspirations ? Default ``None``
        """
        
        if area==AREA_MONO:                 # If the area is monocible, directly return a list with only the entity on the cell
            return [self.on]

        rep = []
        if type(effect)!=list:
            effect = [effect]

        tablArea = self.getArea(area=area,team=team,fromCell=fromCell)
        enties = []

        for cellule in tablArea:
            if cellule.on != None:                                                          # If there is a entity on the cell
                ent = cellule.on
                if directTarget:                                                                # If we are looking for a directTarget, take into account if the entity is untargetable
                    targetable = not(ent.untargetable)
                else:
                    targetable = True

                if ent.hp > 0 and not(dead):
                    if targetable and ((ent.team == team and wanted == ALLIES) or (ent.team != team and wanted == ENNEMIS) or (wanted == ALL)):
                        enties.append(ent)

                elif ent.hp <= 0 and dead:
                    if (ent.team == team and wanted == ALLIES) or (ent.team != team and wanted == ENNEMIS) or (wanted == ALL):
                        enties.append(ent)
        rep = enties

        if lineOfSight and wanted==ENNEMIS and (area not in [AREA_ALL_ENEMIES,AREA_ALL_ENTITES]):
            for ent in enties[:]:
                celly = ent.cell
                direction = getDirection(self,celly)
                if direction == FROM_LEFT:
                    cellToFind = findCell(celly.x+1,celly.y,self.tablAllCells)
                    if cellToFind != None:
                        for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=self):
                            if celly2.on != None and celly.on.team != team and celly2.on in enties:
                                enties.remove(celly2.on)
                elif direction == FROM_RIGHT:
                    cellToFind = findCell(celly.x-1,celly.y,self.tablAllCells)
                    if cellToFind != None:
                        for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=self):
                            if celly2.on != None and celly.on.team != team and celly2.on in enties:
                                enties.remove(celly2.on)
                elif direction == FROM_UP:
                    cellToFind = findCell(celly.x,celly.y+1,self.tablAllCells)
                    if cellToFind != None:
                        for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=self):
                            if celly2.on != None and celly.on.team != team and celly2.on in enties:
                                enties.remove(celly2.on)
                elif direction == FROM_DOWN:
                    cellToFind = findCell(celly.x,celly.y-1,self.tablAllCells)
                    if cellToFind != None:
                        for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=self):
                            if celly2.on != None and celly.on.team != team and celly2.on in enties:
                                enties.remove(celly2.on)

        temp = []
        for a in rep:
            if a.hp/a.maxHp <= lifeUnderPurcentage/100:
                temp+=[a]
        rep=temp

        tempToReturn = rep[:] 
        for rejEff in effect: # Forbiden effects ?
            if rejEff != None:
                aeff = findEffect(rejEff)
                if aeff.reject != None:
                    for b in aeff.reject:
                        actEff = findEffect(b)
                        for tempEnt in tempToReturn:
                            for d in tempEnt.effect:
                                if d.effect.id == actEff.id:
                                    if tempEnt in rep:
                                        rep.remove(tempEnt)
                                        break
                if not(aeff.stackable):
                    for tempEnt in tempToReturn:
                        for tempEff in tempEnt.effect:
                            if tempEff.id == aeff.id:
                                if tempEnt in rep:
                                    rep.remove(tempEnt)
                                    break

        if ignoreInvoc: # Ignorer les invocations ?
            for a in rep[:]:
                if type(a.char) == invoc:
                    rep.remove(a)

        if ignoreAspiration != None:
            if type(ignoreAspiration) != list:
                ignoreAspiration = [ignoreAspiration]
            for snobed in ignoreAspiration:
                for ent in rep[:]:
                    if ent.char.aspiration == snobed and (ent in rep):
                        rep.remove(ent)

        rep.sort(key=lambda toSort: self.distance(toSort.cell))
        return rep

    def getEmptyCellsInArea(self,area=AREA_DONUT_3,team=0):
        """Return a list of the empty cells in the area"""
        tabl = []
        cells = self.getArea(area,team)

        for a in cells:
            if a.on == None:
                tabl.append(a)

        return tabl

    def getCellForSummon(self,area: int, team: int, summon : invoc, summoner):
        """Return the best cell for summon something"""
        tabl = self.getEmptyCellsInArea(area,team)
        for a in tabl[:]:
            if team == 0:
                if a.x > 2:
                    tabl.remove(a)
            else:
                if a.x < 3:
                    tabl.remove(a)

        portee = summon.weapon.range
        if team == 0:
            temp = sorted(tabl, key= lambda funnyTempVarNameButTheSecond: abs(2-funnyTempVarNameButTheSecond.x-portee)+abs(funnyTempVarNameButTheSecond.y-summoner.cell.y))
            if len(temp)>0:
                return temp[0]
            else:
                return None

        else:
            temp = sorted(tabl, key= lambda funnyTempVarNameButTheSecond: abs(3-funnyTempVarNameButTheSecond.x+portee)+abs(funnyTempVarNameButTheSecond.y-summoner.cell.y))
            if len(temp)>0:
                return temp[0]
            else:
                return None

    def surrondings(self):
        return [findCell(self.x-1,self.y,self.tablAllCells),findCell(self.x+1,self.y,self.tablAllCells),findCell(self.x,self.y-1,self.tablAllCells),findCell(self.x,self.y+1,self.tablAllCells)]

def findCell(x : int, y : int, tablAllCells) -> cell:
    """Return the cell in X:Y, if it exist"""
    cmpt, maxCellNum = 0, len(tablAllCells)
    while cmpt < maxCellNum:
        if tablAllCells[cmpt].x == x and tablAllCells[cmpt].y == y:
            return tablAllCells[cmpt]
        cmpt += 1

def map(tablAllCells,bigMap,showArea:List[cell]=[],fromEnt=None,wanted=None,numberEmoji=None):
    """Renvoie un str contenant la carte du combat"""
    line1,line2,line3,line4,line5 = [None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None]
    lines = [line1,line2,line3,line4,line5]

    if bigMap:
        line6, line7 = [None,None,None,None,None,None],[None,None,None,None,None,None]
        lines.append(line6)
        lines.append(line7)

    for a in tablAllCells:
        if isLenapy or True:
            temp = ['<:em:866459463568850954>',['<:tb:873118129214083102>','<:tr:873118129130192947>'][wanted==ENNEMIS]][a in showArea]
        else:
            temp = f'{str(a.x)}:{str(a.y)}'                         # Show cells ID
        if a.on != None:
            if a.on.status == STATUS_DEAD:
                temp = ['<:ls:868838101752098837>','<:ls:868838465180151838>'][a.on.team]
            elif a.on.status != STATUS_TRUE_DEATH:
                if a.on.invisible:                              # If the entity is invisible, don't show it. Logic
                    temp = '<:em:866459463568850954>'
                elif a not in showArea or (wanted==ALLIES and a.on.team != fromEnt.team) or (wanted==ENNEMIS and a.on.team == fromEnt.team):
                    temp = [a.on.icon,'❇️'][a.on==fromEnt]
                elif a != fromEnt.cell:
                    temp = '<:unsee:899788326691823656>'
                    for cmpt in range(len(numberEmoji)):
                        if a.on == numberEmoji[cmpt]:
                            temp = listNumberEmoji[cmpt]
                            break
                else:
                    temp = '<:ikaWhiteTargeted1:873118129021157377>'
            else:
                a.on = None
        lines[a.y][a.x]=temp
    temp = ""
    for a in lines:
        for b in [0,1,2,3,4]:
            temp += f"{a[b]}|"
        temp += f"{a[b+1]}\n"
    return temp

def getHealAggro(on, skillToUse : Union[skill,weapon]):
    if on.hp <= 0 or on.hp >= on.maxHp:
        return 0
    elif type(on.char) == invoc:
        return -111
    else:
        prio = (1-on.hp/on.maxHp)*100

        prio = prio * (1.2 - (0.1*on.char.weapon.range))                # If the entity is a melee, he is more important
        if not(on.auto):
            prio = prio * 1.1                                           # If the entity is a active player, he is a little more important, for reduce the use of the spoon

        if (skillToUse.type == TYPE_HEAL and skillToUse.power >= 75 and on.maxHp - on.hp < on.char.level * 3) or (skillToUse.type == TYPE_INDIRECT_HEAL and on.hp/on.maxHp <= 0.35):
            prio = prio * 0.7                                           # If the skill is a big direct heal and the entity is not low Hp or if the skill is a HoT and the entity is low Hp
                                                                            # The entity is less important
        
        prio = prio * (1-(on.healResist/2/100))                             # If the entity have a big healing resist, he is less important

        incurValue, healAggroBonus = 0, 100
        for eff in on.effect:
            if eff.effect.id == incurable.id:
                incurValue = max(eff.effect.power,incurValue)
            elif eff.effect.id == undeadEff2.id:
                healAggroBonus += undeadEff2.power

        prio = prio * (1-(incurValue/2/100)) * (healAggroBonus/100)                              # Same with the healing reduce effects
        return prio

def getHealTarget(tablTeam : list, skillToUse : skill):
    if len(tablTeam) == 1:
        return tablTeam[0]
    elif len(tablTeam) < 1:
        raise AttributeError("tablTeam is empty")
    
    temp = tablTeam
    temp.sort(key=lambda funnyTempVarName:getHealAggro(funnyTempVarName,skillToUse),reverse=True)
    return temp[0]
