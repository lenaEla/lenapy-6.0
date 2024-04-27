import copy
import os, io
from sys import maxsize
from typing import List, Union
import requests
import interactions
from PIL import ImageColor, ImageOps
import PIL.Image
from adv import *
from classes import *
from commands_files.alice_stats_endler import *
from data.database import *
from gestion import *

stuffDB = dbHandler(database="stuff.db")
customIconDB = dbHandler(database="custom_icon.db")

timeoutSelect = interactions.StringSelectMenu(interactions.StringSelectOption(label="Timeout", value="Parfois je me demande ce que ferais Lena si elle pensais par elle même", default=True),custom_id = "timeoutSelect",disabled=True
)
timeoutSelect = interactions.ActionRow(timeoutSelect)

lvlUpUnlock = {
    5: "- Emplacement de compétence n°4",
    10: "- Eléments basiques\n- Compétences ultimes",
    15: "- Emplacement de compétence n°5",
    20: "- Eléments spaciaux-temporels",
    25: "- Emplacement de compétence n°6",
    30: "- Eléments secondaires",
    35: "- Emplacement de compétence n°7",
    MAXLEVEL: "- Prestige"
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
        elif a in ["ù", "û", "Ü"]:
            temp += "u"
        elif a in ["À", "Ä", "Â"]:
            temp += "A"
        elif a in ["É", "È", "Ë", "Ê"]:
            temp += "E"
        elif a in ["Ù", "Û", "Ü"]:
            temp += "U"
        elif a in ["?", "!", ";", ",", "."," ","-"]:
            temp += "_"
        else:
            temp += a

    return temp

def getDirection(cellFrom,cellTarget):
    if cellFrom == cellTarget:
        return FROM_POINT
    xDif, yDif = cellFrom.x-cellTarget.x, cellFrom.y-cellTarget.y
    if abs(xDif) >= abs(yDif):
        if xDif > 0:
            return FROM_LEFT
        elif xDif < 0:
            return FROM_RIGHT
    else:
        if yDif > 0:
            return FROM_UP
        elif yDif < 0:
            return FROM_DOWN

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
        self.depl = None
        self.surrondings = None

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
        elif area in [AREA_CIRCLE_1,AREA_CIRCLE_2,AREA_CIRCLE_3,AREA_CIRCLE_4,AREA_CIRCLE_5,AREA_CIRCLE_6,AREA_CIRCLE_7,AREA_DONUT_1,AREA_DONUT_2,AREA_DONUT_3,AREA_DONUT_4,AREA_DONUT_5,AREA_DONUT_6,AREA_DONUT_7,AREA_DIST_3,AREA_DIST_4,AREA_DIST_5,AREA_DIST_6,AREA_DIST_7,AREA_BOMB_5,AREA_BOMB_6,AREA_BOMB_7]:
            dist = area
            if area > AREA_CIRCLE_7:
                if area <= AREA_DONUT_7:
                    dist -= AREA_DONUT_1-1
                elif area <= AREA_DIST_7:
                    dist -= AREA_DIST_3-3
                elif area <= AREA_BOMB_7:
                    dist -= AREA_BOMB_5-5

            for a in self.tablAllCells:
                if self.distance(cell=a) <= dist:
                    rep.append(a)

            if area > AREA_CIRCLE_7 and area <= AREA_DONUT_7: # If donut, remove the center
                rep.remove(self)
            elif area > AREA_DONUT_7 and area <= AREA_DIST_7: # If dist only, remove melee
                for a in rep[:]:
                    if self.distance(cell=a) <= 2:
                        rep.remove(a)
            elif area > AREA_DIST_7 and area <= AREA_BOMB_7: # If dist only, remove melee
                for a in rep[:]:
                    if self.distance(cell=a) <= 4:
                        rep.remove(a)
        elif area in [AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES]:
            return self.tablAllCells
        elif area in [AREA_CONE_2,AREA_CONE_3,AREA_CONE_4,AREA_CONE_5,AREA_CONE_6,AREA_CONE_7]:
            areaTabl, coneLength, direction = [self],area-(AREA_CONE_2-2), getDirection(fromCell,self)
            if direction in [FROM_RIGHT,FROM_POINT]:
                for cmpt in range(coneLength+1):
                    for celly in self.tablAllCells:
                        if celly not in areaTabl:
                            if celly == self:
                                areaTabl.append(celly)
                            elif celly.x == self.x+(cmpt-1) and celly.x >=self.x:
                                if ((celly.y>self.y and celly.y < self.y+cmpt) or (celly.y<self.y and celly.y > self.y-cmpt) or (celly.y == self.y)):
                                    areaTabl.append(celly)
            elif direction == FROM_LEFT:
                for cmpt in range(coneLength+1):
                    for celly in self.tablAllCells:
                        if celly not in areaTabl:
                            if celly == self:
                                areaTabl.append(celly)
                            elif celly.x == self.x-(cmpt-1) and celly.x <= self.x:
                                if ((celly.y>self.y and celly.y < self.y+cmpt) or (celly.y<self.y and celly.y > self.y-cmpt) or (celly.y == self.y)):
                                    areaTabl.append(celly)
            elif direction == FROM_DOWN:
                for cmpt in range(coneLength+1):
                    for celly in self.tablAllCells:
                            if celly not in areaTabl:
                                if celly == self:
                                    areaTabl.append(celly)
                                elif celly.y == self.y+(cmpt-1) and celly.y >= self.y:
                                    if ((celly.x>self.x and celly.x < self.x+cmpt) or (celly.x<self.x and celly.x > self.x-cmpt) or (celly.x == self.x)):
                                        areaTabl.append(celly)
            elif direction == FROM_UP:
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
            if direction in [FROM_LEFT,FROM_POINT]:
                for cellToSee in self.tablAllCells:
                    if self.y == cellToSee.y and (cellToSee.x - self.x <= area-(AREA_LINE_2-1) and cellToSee.x - self.x >= 0):
                        rep.append(cellToSee)
            elif direction == FROM_RIGHT:
                for cellToSee in self.tablAllCells:
                    if self.y == cellToSee.y and (self.x - cellToSee.x <= area-(AREA_LINE_2-1) and cellToSee.x - self.x <= 0):
                        rep.append(cellToSee)
            elif direction == FROM_UP:
                for cellToSee in self.tablAllCells:
                    if self.x == cellToSee.x and (cellToSee.y - self.y <= area-(AREA_LINE_2-1) and cellToSee.y - self.y >= 0):
                        rep.append(cellToSee)
            elif direction == FROM_DOWN:
                for cellToSee in self.tablAllCells:
                    if self.x == cellToSee.x and (self.y - cellToSee.y <= area-(AREA_LINE_2-1) and cellToSee.y - self.y <= 0):
                        rep.append(cellToSee)
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
                        cell1 = findCell(self.x-cmptx,self.y-cmptx,self.tablAllCells)
                        if cell1 != None:
                            rep.append(cell1)
                        cell2 = findCell(self.x+cmptx,self.y-cmptx,self.tablAllCells)
                        if cell2 != None:
                            rep.append(cell2)
                    else:
                        cell1 = findCell(self.x-cmptx,self.y+cmptx,self.tablAllCells)
                        if cell1 != None:
                            rep.append(cell1)
                        cell2 = findCell(self.x+cmptx,self.y+cmptx,self.tablAllCells)
                        if cell2 != None:
                            rep.append(cell2)
                    cmptx+=1
            rep.append(self)
        elif area in [AREA_RANDOMENNEMI_1,AREA_RANDOMENNEMI_2,AREA_RANDOMENNEMI_3,AREA_RANDOMENNEMI_4,AREA_RANDOMENNEMI_5,AREA_RANDOMALLIE_1,AREA_RANDOMALLIE_2,AREA_RANDOMALLIE_3,AREA_RANDOMALLIE_4,AREA_RANDOMALLIE_5]:
            for cell in self.tablAllCells:
                if (cell.on != None and cell.on.team != team and area <= AREA_RANDOMENNEMI_5) or (cell.on != None and cell.on.team == team and area > AREA_RANDOMENNEMI_5) and type(cell.on.char) != classes.invoc:
                    rep.append(cell)
            nbToReturn = area-[AREA_RANDOMENNEMI_1,AREA_RANDOMALLIE_1][area>=AREA_RANDOMALLIE_1]+1
            while len(rep) < nbToReturn-2:
                rep.append(rep[random.randint(0,len(rep)-1)])
            return rep[0:min(nbToReturn,len(rep))]
        elif area in [AREA_INLINE_2,AREA_INLINE_3,AREA_INLINE_4,AREA_INLINE_5]:
            for celly in self.tablAllCells:
                if (celly.x == self.x or celly.y == self.y) and self.distance(celly) <= area + 2 - AREA_INLINE_2:
                    rep.append(celly)
        elif area in [AREA_LOWEST_HP_ALLIE, AREA_LOWEST_HP_ENEMY]:
            listEnt = []
            for a in self.tablAllCells:
                if a.on != None and [a.on.team == team, a.on.team != team][area == AREA_LOWEST_HP_ENEMY] and a.on.char.__class__ not in [invoc,depl] and a.on.hp > 0:
                    listEnt.append(a.on)

            if len(listEnt) > 0:
                listEnt.sort(key=lambda ballerine: ballerine.hp/ballerine.maxHp)
                return [listEnt[0].cell]
            else:
                return []
        elif area in [AREA_SUMMONS]:
            for a in self.tablAllCells:
                if a.on != None and a.on.team == team and type(a.on.char) == classes.invoc:
                    rep.append(a)
        elif area in [AREA_SUMMONER]:
            if self.on != None and type(self.on.char) in [depl, invoc]:
                for cell in self.tablAllCells:
                    if cell.on != None and cell.on.id == self.on.summoner.id:
                        return [cell]
        elif area in [AREA_BIGDONUT]:
            for a in self.tablAllCells:
                if self.distance(cell=a) == 2:
                    rep.append(a)
        return rep

    def getEntityOnArea(self,area=AREA_MONO,team=0,wanted=ALLIES,lineOfSight=False,lifeUnderPurcentage=99999,dead=False,effect=[None],ignoreInvoc = False, directTarget=True,ignoreAspiration = None,fromCell=None) -> list: 
        """
            Return a list of the targetable entities in the area\n
            \n
            Parameters :\n
            .area : See ``constantes``
            .team : The team of the entity who's looking in the area. ``0`` for Blue Team (and Default), ``1`` else for the Red Team
            .wanted : Who are we looking for ? ``ALLIES`` for the allies of the entity (and Default), ``ENEMIES`` else
            .lineOfSight : Do we look for the line of sight ? Default ``False``
                -> The line of sight will always be ignore if Wanted is at ``ALLIES`` or Area is in ``AREA_ALL_ALLIES,AREA_ALL_ENNEMIS,AREA_ALL_ENTITIES``
            .lifeUnderPurcentage : Only select entities under or egal at ``lifeUnderPurcentage``% of their maxHp. Default ``100``
            .dead : Are we looking for dead entities ? Default ``False``
            .effects : A list of ``effect``objects. If the entities can't be applyed a effect of the list, exclude them. Defaul ``[None]``
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
            ent = None
            if cellule.on != None:                                                          # If there is a entity on the cell
                ent = cellule.on
            else:
                for celly in cellule.getSurrondings():
                    if celly != None and celly.on != None and TRAIT_GIANTESS in celly.on.char.trait:
                        if ent not in enties:
                            ent = cellule.on
                            break

            if ent != None:
                if directTarget:                                                                # If we are looking for a directTarget, take into account if the entity is untargetable
                    targetable = not(ent.untargetable)
                else:
                    targetable = True

                if ent.hp > 0 and not(dead):
                    if self.on != None:
                        kitsuFlag = self.on.char.npcTeam in [NPC_KITSUNE,NPC_GOLEM] and ent.char.npcTeam == [NPC_KITSUNE,NPC_GOLEM][ent.char.npcTeam == NPC_KITSUNE]
                    else:
                        kitsuFlag = False
                    allieTeamVerif = ent.team == team and wanted == ALLIES and not(kitsuFlag)
                    ennemiTeamVerif = (ent.team != team and wanted == ENEMIES) or kitsuFlag
                    if targetable and (allieTeamVerif or ennemiTeamVerif or (wanted == ALL) or (area == AREA_ALL_ENTITES)):
                        enties.append(ent)

                elif ent.hp <= 0 and dead:
                    if self.on != None:
                        kitsuFlag = self.on.char.npcTeam in [NPC_KITSUNE,NPC_GOLEM] and ent.char.npcTeam == [NPC_KITSUNE,NPC_GOLEM][ent.char.npcTeam == NPC_KITSUNE]
                    else:
                        kitsuFlag = False
                    allieTeamVerif = ent.team == team and wanted == ALLIES and not(kitsuFlag)
                    ennemiTeamVerif = (ent.team != team and wanted == ENEMIES) or kitsuFlag
                    if (allieTeamVerif) or (ennemiTeamVerif) or (wanted == ALL):
                        enties.append(ent)
        rep = enties

        if lineOfSight and wanted==ENEMIES and (area not in [AREA_ALL_ENEMIES,AREA_ALL_ENTITES]):
            for ent in enties[:]:
                if ent.team != team:
                    celly, direction = ent.cell, getDirection(self,ent.cell)
                    if direction == FROM_RIGHT:
                        cellToFind = findCell(celly.x+1,celly.y,self.tablAllCells)
                        if cellToFind != None:
                            for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=self):
                                if celly2.on != None and celly.on.team != team and celly2.on in enties:
                                    enties.remove(celly2.on)
                    elif direction == FROM_LEFT:
                        cellToFind = findCell(celly.x-1,celly.y,self.tablAllCells)
                        if cellToFind != None:
                            for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=self):
                                if celly2.on != None and celly.on.team != team and celly2.on in enties:
                                    enties.remove(celly2.on)
                    elif direction == FROM_DOWN:
                        cellToFind = findCell(celly.x,celly.y+1,self.tablAllCells)
                        if cellToFind != None:
                            for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=self):
                                if celly2.on != None and celly.on.team != team and celly2.on in enties:
                                    enties.remove(celly2.on)
                    elif direction == FROM_UP:
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
        for aeff in effect: # Forbiden effects ?
            aeff = findEffect(aeff)
            if aeff != None:
                if not(aeff.stackable):
                    for tempEnt in tempToReturn:
                        for tempEff in tempEnt.effects:
                            if tempEff.effects.id == aeff.id:
                                if aeff.replace and fromCell != None and tempEff.caster.id == fromCell.on.id:
                                    pass
                                elif tempEnt in rep:
                                    try:
                                        rep.remove(tempEnt)
                                    except:
                                        pass
                                    break
                if aeff.reject != None:
                    for b in aeff.reject:
                        actEff = findEffect(b)
                        if actEff != None:
                            for tempEnt in tempToReturn:
                                for d in tempEnt.effects:
                                    if d.effects.id == actEff.id:
                                        if tempEnt in rep:
                                            try:
                                                rep.remove(tempEnt)
                                            except:
                                                pass
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

        rep = list(set(rep))
        rep.sort(key=lambda toSort: self.distance(toSort.cell))
        for indx, ent in enumerate(rep):
            if type(ent) == None:
                try:
                    rep.remove(ent)
                except:
                    pass
            elif ent.isNpc(TGESL1.name):
                rep[indx] = ent.summoner
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
        rangeTabl = {RANGE_MELEE:[2,3],RANGE_DIST:[1,4],RANGE_LONG:[0,5]}[summon.weapon.range][team]

        if len(tabl)>0:
            return sorted(tabl, key = lambda ballerine: cellShort(ballerine, rangeTabl, team), reverse=True)[0]

    def getSurrondings(self):
        if self.surrondings == None or len(self.surrondings) < 4:
            self.surrondings = [findCell(self.x-1,self.y,self.tablAllCells),findCell(self.x+1,self.y,self.tablAllCells),findCell(self.x,self.y-1,self.tablAllCells),findCell(self.x,self.y+1,self.tablAllCells)]
        return self.surrondings

    def __str__(self):
        return "Cell #{0} at {1}:{2}".format(self.id,self.x,self.y)

def cellShort(tmpCell, rangeTabl, team):
    value = 0
    if tmpCell.x == rangeTabl:
        value += 100
    if tmpCell.x == rangeTabl + [1,-1][team]:
        value += 50
    
    value += abs(2-tmpCell.y)*10
    return value

def findCell(x : int, y : int, tablAllCells) -> cell:
    """Return the cell in X:Y, if it exist"""
    cmpt, maxCellNum = 0, len(tablAllCells)
    while cmpt < maxCellNum:
        if tablAllCells[cmpt].x == x and tablAllCells[cmpt].y == y:
            return tablAllCells[cmpt]
        cmpt += 1

def visuArea(area: int, wanted, ranged=True, fromDir=FROM_LEFT) -> list:
    tablAllCells, cmpt = [], 0
    for a in [0, 1, 2, 3, 4, 5]:
        for b in [0, 1, 2, 3, 4]:
            tablAllCells += [cell(a, b, cmpt, tablAllCells)]
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
            elif area in [5, 6, 7, 14, 15, 16, 26, 27, 28, 31, 32, 33]:
                isAlly = -2
                isAlly2 = -1
                isAlly3 = 2
            else:
                isAlly = 0
                isAlly2 = 1
                isAlly3 = 2

        base = 3

        if area in [AREA_CIRCLE_4, AREA_CONE_4, AREA_LINE_4, AREA_DONUT_4, AREA_DIST_4]:
            visibleCell = findCell(base+isAlly2, 2, tablAllCells)
        elif area in [5, 6, 7, 14, 15, 16, 26, 27, 28, 31, 32, 33]:
            visibleCell = findCell(base+isAlly3, 2, tablAllCells)
        else:
            visibleCell = findCell(base+isAlly, 2, tablAllCells)
    else:
        if area in [AREA_CIRCLE_4, AREA_CONE_2, AREA_LINE_4, AREA_DONUT_4, AREA_DIST_4, AREA_INLINE_3]:
            visibleCell = findCell(1, 2, tablAllCells)
        elif area in [5, 6, 7, 14, 15, 16, 20, 21, 26, 27, 28, 31, 32, 33, AREA_CONE_3, AREA_CONE_4, AREA_INLINE_4, AREA_INLINE_5,AREA_BOMB_5,AREA_BOMB_6,AREA_BOMB_7]:
            visibleCell = findCell(0, 2, tablAllCells)
        else:
            visibleCell = findCell(2, 2, tablAllCells)

    if fromDir == FROM_LEFT:
        fromCell = findCell(0,2,tablAllCells)
    elif fromDir == FROM_RIGHT:
        fromCell =  findCell(5,2,tablAllCells)
    elif fromDir == FROM_UP:
        fromCell = findCell(3,0,tablAllCells)
    elif fromDir == FROM_DOWN:
        fromCell = findCell(3,4,tablAllCells)

    visibleArea = visibleCell.getArea(area=area, fromCell = [visibleCell,fromCell][not(ranged)])
    line1, line2, line3, line4, line5 = [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None]
    lines = [line1, line2, line3, line4, line5]
    temp = ""

    for a in tablAllCells:
        temp = f'<:em:866459463568850954>'
        if a in visibleArea:
            if wanted == ALLIES:
                temp = "<:t1:873118129214083102>"
            else:
                temp = "<:t2:873118129130192947>"

        if [a.x,a.y] == [fromCell.x,fromCell.y] and not(ranged) and area not in notOrientedAreas:
            temp = [tablAllAllies[0].icon,'<:tl:979408929467539537>'][a in visibleArea and wanted == ALLIES]
        lines[a.y][a.x] = temp
    if ranged and area not in notOrientedAreas:
        lines[visibleCell.y][visibleCell.x] = [tablAllAllies[0].icon,'<:tl:979408929467539537>'][visibleCell in visibleArea and wanted == ALLIES]
    else:
        if visibleCell in visibleArea:
            if wanted == ENEMIES:
                # Memo : Lines[y][x]
                lines[visibleCell.y][visibleCell.x] = "<:ir:873118129541238814>"
            else:
                lines[visibleCell.y][visibleCell.x] = '<:ib:873118128958214166>'
        else:
            if wanted == ENEMIES:
                lines[visibleCell.y][visibleCell.x] = '<:ir:866459224664702977>'
            else:
                lines[visibleCell.y][visibleCell.x] = '<:ib:866459302319226910>'

    temp = ""
    for a in lines:
        for b in [0, 1, 2, 3, 4]:
            temp += f"{a[b]}|"
        temp += f"{a[b+1]}\n"

    return temp

def infoEffect(effId: Union[str,effect], user: char, emb: interactions.Embed, self=False, txt: str = "",powerPurcent=100) -> interactions.Embed:
    effTmp, boucle, iteration, powerPurcent = "", True, False, [powerPurcent,100][powerPurcent==None]
    while boucle:
        eff = findEffect(effId)
        if eff.callOnTrigger != None and eff.trigger==TRIGGER_INSTANT and eff.type in [TYPE_BOOST,TYPE_MALUS]:
            effSelf = findEffect(eff.callOnTrigger)
            txt = " ({0} autour de la cible)".format(areaEmojis[eff.area])
            eff: classes.effect = effSelf
        fieldname, bonus, malus, Stat = "{0} :".format(eff), "", "", ""
        if eff.stat == None:
            Stat = "- Fixe"
        elif eff.stat == PURCENTAGE:
            Stat = "% Pourcentage"
        elif eff.stat == MISSING_HP:
            Stat = "% Pourcentage PV Manquant"
        elif eff.stat != HARMONIE:
            Stat = statsEmojis[eff.stat] + " " +allStatsNames[eff.stat]
        else:
            Stat = "Harmonie"

        if eff.turnInit == -1:
            initDur = "\n__Durée :__ Infinie\n"
        elif eff.trigger!=TRIGGER_INSTANT:
            initDur = "\n__Durée :__ {0} tour{1}\n".format(eff.turnInit,["","s"][eff.turnInit>1])
        else:
            initDur = "\n"
        if eff.callOnTrigger != None and findEffect(eff.callOnTrigger) != None:
            effCalled = findEffect(eff.callOnTrigger)
            called = "\nLorsqu'il se déclanche, cet effet {0} {1} __{2}__ aux cibles dans la zone d'effet".format(["octroi","inflige"][effCalled.type in hostileTypes],effCalled.emoji[0][0], effCalled.name)
        else:
            called = ""
        typeEmoji = ""

        if eff.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_RESURECTION]:
            typeEmoji = statsEmojis[ACT_HEAL_FULL]
        elif eff.type in [TYPE_INDIRECT_DAMAGE]:
            typeEmoji = statsEmojis[ACT_INDIRECT_FULL]
        elif eff.type in [TYPE_ARMOR]:
            typeEmoji = statsEmojis[ACT_SHIELD_FULL]
        elif eff.type in [TYPE_BOOST,TYPE_MALUS]:
            typeEmoji = statsEmojis[ACT_BOOST_FULL]
        elif eff.type in [TYPE_SUMMON,TYPE_DEPL]:
            typeEmoji = "<:Icn_Sprinkler:1080807633432350801>"
        elif eff.type in [TYPE_DAMAGE]:
            typeEmoji = statsEmojis[ACT_DIRECT_FULL]

        effTmp += "__Type :__ {1} {0}".format(allTypeNames[eff.type],typeEmoji)
        if eff.power > 0:
            powa = max(eff.power, eff.overhealth)*([powerPurcent,100][eff.stat in [PURCENTAGE,FIXE,None,MISSING_HP]]/100)
            effTmp += "\n__Puissance :__ **"+str(round(powa,[1,0][powa.is_integer()]))+"**"

        if eff.stackable:
            cumu = "\n\nCet effet est **cumulable**"
        effTmp += "{0}__Statistique :__ **{1}**".format(initDur,Stat)

        if eff.type in [TYPE_INDIRECT_DAMAGE,TYPE_INDIRECT_HEAL] or eff.area != AREA_MONO:
            effTmp += "\n__Zone d'effet :__ {0} {1}".format(areaEmojis[eff.area],areaNames[eff.area])
        
        addTxt = ""
        if eff.trigger != TRIGGER_PASSIVE:
            addTxt += "\nCet effet se délanche {0}".format(triggersTxt[eff.trigger])
        if eff.stackable:
            addTxt += "\nCet effet est **cumulable**"
        if eff.callOnTrigger != None and findEffect(eff.callOnTrigger) != None:
            effCalled = findEffect(eff.callOnTrigger)
            addTxt += "\nEn se déclanchant, {0} {1}".format(["octroi","inflige"][effCalled.type in hostileTypes],effCalled)

        if eff.lvl not in [1,99] and eff.trigger not in [TRIGGER_PASSIVE] and eff.type not in [TYPE_PASSIVE,TYPE_BOOST,TYPE_MALUS,TYPE_ARMOR] and eff.lvl != eff.turnInit:
            addTxt += "\nCet effet peut se déclancher au maximum **{0} fois**".format(eff.lvl)
        stats = eff.allStats()+[eff.resistance, eff.percing, eff.critical, eff.overhealth, eff.aggro, eff.inkResistance, eff.block, eff.dodge, eff.critDmgUp, eff.critHealUp, eff.dmgUp, eff.healUp, eff.counterOnBlock, eff.counterOnDodge]
        names = nameStats+nameStats2 + ["Puissance de l'Armure", "Agression", "Résistance aux dégâts indirects","Blocage","Prob. Esquive", "Dégâts Critiques","Soins Critiques", "Dégâts non critiques","Soins non critiques","Prob. Contre lors d'un blocage","Prob. Contre lors d'une esquive"]

        if eff.redirection > 0:
            addTxt += "\nCet effet redirige **{0}**% des **dégâts direct** reçu par le porteur vers le lanceur de l'effet en tant que **dégâts indirects**".format(eff.redirection)
        if eff.immunity:
            addTxt += "\nCet effect rend le porteur **invulnérable aux dégâts**"

        if addTxt != "":
            effTmp += "\n"+addTxt
        if eff.description != "Pas de description":
            if eff.stat not in [FIXE,None,PURCENTAGE]:
                statEm = " ({})".format(statsEmojis[eff.stat])
            else:
                statEm = ""
            effTmp += "\n\n{1}__Description :__\n{0}\n".format(eff.description.format(str([round(eff.power*(powerPurcent/100),1),eff.power][type(eff.power)==int])+statEm, str(int(eff.power*powerPurcent/100)//2)+statEm),["","\n"][effTmp[-1] == "\n"])
        for a in range(len(stats)):
            if stats[a] > 0:
                bonus += "{2} __{0}__ : +{1}\n".format(names[a],int(stats[a]*powerPurcent/100),[statsEmojis[a],""][a>CRITICAL])
            elif stats[a] < 0:
                malus += "{2} __{0}__ : {1}\n".format(names[a],int(stats[a]*powerPurcent/100),[statsEmojis[a],""][a>CRITICAL])

        if bonus != "":
            effTmp += ["\n",""][effTmp[-1]=="\n"]+"\n**__Bonus de statistiques :__**{0}\n".format([""," *({0}%)*".format(powerPurcent)][powerPurcent!=100]) + bonus
        if malus != "":
            effTmp += ["\n",""][effTmp[-1]=="\n"]+"\n**__Malus de statistiques :__**{0}\n".format([""," *({0}%)*".format(powerPurcent)][powerPurcent!=100]) + malus

        if eff.inkResistance > 0 and eff.stat != None:
            effTmp += "\nLa résistance aux dégâts indirects ne peux pas dépasser 3 fois sa valeur de base"
        if eff.block > 0:
            effTmp += "\n__Blocage :__\nUne attaque bloquée réduit de **35%** les dégâts reçus"
        if eff.counterOnDodge > 0:
            effTmp += "\n__Contre Attaque :__\n- Puissance : **{0}**, Harmonie".format(COUNTERPOWER)
        if eff.reject != None:
            effTmp += "\n{0}__Cet effet n'est pas compatible avec les effets :__\n".format(["","\n"][effTmp[-1]!="\n"])
            for a in eff.reject:
                rejected = findEffect(a)
                effTmp += f"{rejected.emoji[user.species-1][0]} {rejected.name}\n"

        effTmp = reduceEmojiNames(effTmp)
        if len(effTmp) > 1024:
            effTmp = completlyRemoveEmoji(effTmp)
        if eff.callOnTrigger != None and not(iteration) and type(eff.callOnTrigger) in [str,effect]:
            lastName = effId.name
            effId = findEffect(eff.callOnTrigger)
            iteration = True

            emb.add_field(name=fieldname, value=effTmp, inline=False)
            effTmp, txt = "", " ("+lastName+")"
        elif eff.callOnTrigger != None and iteration and type(eff.callOnTrigger) in [str,effect]:
            effId = findEffect(eff.callOnTrigger)
            emb.add_field(name=fieldname, value=effTmp, inline=False)
            if eff.area != AREA_MONO:
                emb.add_field(name="__Zone d'effet :__", value="{0} {1}".format(areaEmojis[eff.area],areaNames[eff.area]))
            break
        elif eff.callOnTrigger != None and type(eff.callOnTrigger) == depl:
            emb.add_field(name="__Cet effet invoque un Déployable :__",value="{0} __{1}__ : {2}".format(eff.callOnTrigger.icon[0],eff.callOnTrigger.name,eff.callOnTrigger.description),inline=False)
            break
        elif eff.callOnTrigger != None and type(eff.callOnTrigger) == invoc:
            smn: invoc = findSummon(eff.callOnTrigger)
            smnDesc = ""
            for ski in smn.skills:
                if type(ski) == classes.skill:
                    smnDesc += "{0} {1}\n".format(ski.emoji, ski.name)
                    if ski.description != None:
                        smnDesc += "> {0}\n".format(ski.description.replace("\n","\n> "))

            emb.add_field(name="__Cet effet invoque {0} {1} autour de la cible :__".format(smn.icon[0],smn.name),value=smnDesc,inline=False)
            break
        else:
            if not(self):
                emb.add_field(name="<:em:866459463568850954>\n" +fieldname + txt, value=reduceEmojiNames(effTmp), inline=False)
            else:
                emb.add_field(name="<:em:866459463568850954>\n" + fieldname, value=reduceEmojiNames(effTmp), inline=False)
            break

    if eff.id == neutralCard.id:
        cardDesc = ''
        for cmpt in range(len(cardAspi)-1):
            cardDesc += "{0} __{1}__ : ".format(cardAspi[cmpt].emoji[0][0],inspi[cmpt])
            tmpCardStat, cardStat = [], cardAspi[cmpt].allStats() + [cardAspi[cmpt].resistance, cardAspi[cmpt].percing, cardAspi[cmpt].critical]
            for statCmpt in range(len(cardStat)):
                if cardStat[statCmpt] > 0:
                    tmpCardStat.append([statCmpt,cardStat[statCmpt]])

            for statCmpt in range(len(tmpCardStat)):
                cardDesc += "{1} +{0}".format(tmpCardStat[statCmpt][1],allStatsNames[statCmpt])
                if statCmpt < len(tmpCardStat)-1:
                    cardDesc += ", "
                else:
                    cardDesc += "\n"

        cardDesc = reduceEmojiNames(cardDesc)
        emb.add_field(name="__Cartes astrales :__",value=cardDesc,inline=False)

    return emb

def infoSkill(skill: skill, user: char, ctx):
    skil: classes.skill = skill
    if skil.become != None and len(skil.become) > 3:
        listToReturn, desc, embedTitle = [], "Cette compétence regroupe les compétences suivantes :\n\n", reduceEmojiNames(skil.emoji) + " " + skil.name
        for skilly in skil.become:
            temp = ""
            if len(skil.become) < 10:
                temp += reduceEmojiNames("{0} __{1}__ :\n".format(skilly.emoji,skilly.name) + skilly.getSummary() + "\n\n")
            else:
                temp += reduceEmojiNames("{0} __{1}__ :\n{2}\n\n".format(skilly.emoji,skilly.name,skilly.description))

            if len(desc+temp) > EMBED_MAX_DESC_LENGTH:
                listToReturn.append(Embed(title=embedTitle,color=light_blue, description=desc))
                desc = temp
                temp = ""
            else:
                desc += temp
        listToReturn.append(Embed(title=embedTitle,color=light_blue, description=desc))
        listToReturn[-1].set_footer(text="Id : {0} - iaPow : {1}".format(skil.id,skil.iaPow))
        return listToReturn

    else:
        cast, multiPower, multiSkill, guide, maxPowerComb, indPow =  0, [], [], 0, 0, 0
        while skil.effectOnSelf != None:
            eff = findEffect(skil.effectOnSelf)
            if eff.replica != None:
                if skil.power != 0 or skil.effects != [None]:
                    multiPower.append(skil)
                    if not(skil.replay):
                        guide += 1
                if skil.replay:
                    multiSkill.append(skil)
                skil = findSkill(eff.replica)
            else:
                guide += 1
                break
            cast += 1

        if multiSkill != []:
            multiSkill.append(skil)
        if multiPower != []:
            multiPower.append(skil)

        desc = ""
        if skil.become != None:
            desc, listConds = desc + "\n\nCette compétence regroupe les compétences suivantes :\n", []
            for cmpt in range(len(skil.become)):
                desc += "{1} __{0}__".format(skil.become[cmpt].name, skil.become[cmpt].emoji)
                if cmpt < len(skil.become)-2:
                    desc += ", "
                elif cmpt == len(skil.become)-2:
                    desc += " et "

            desc += "\nLeurs temps de rechargement sont syncronisés"

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
            if multiSkill != []:
                desc += "\n\nCette compétence permet d'enchaîner "
                lenMultiSkill = len(multiSkill)
                for cmpt in range(lenMultiSkill):
                    desc += "{1} __{0}__".format(multiSkill[cmpt].name, multiSkill[cmpt].emoji)
                    if cmpt < lenMultiSkill-2:
                        desc += ", "
                    elif cmpt == lenMultiSkill-2:
                        desc += " et "
                desc += " durant le même tour"
            elif len(multiPower) > 1:
                desc += "\nCette compétence s'utilise en continue pendant **{0}** tours".format(len(multiPower))
            else:
                desc += "\n__Tours de chargements__ : **{0} tour{1}**".format(cast, ["", "s"][int(cast > 1)])

        typeEmoji = ""
        if skil.type in [TYPE_DAMAGE]:
            typeEmoji = statsEmojis[ACT_DIRECT_FULL]
        elif skil.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_RESURECTION]:
            typeEmoji = statsEmojis[ACT_HEAL_FULL]
        elif skil.type in [TYPE_INDIRECT_DAMAGE]:
            typeEmoji = statsEmojis[ACT_INDIRECT_FULL]
        elif skil.type in [TYPE_ARMOR]:
            typeEmoji = statsEmojis[ACT_SHIELD_FULL]
        elif skil.type in [TYPE_BOOST,TYPE_MALUS]:
            typeEmoji = statsEmojis[ACT_BOOST_FULL]
        elif skil.type in [TYPE_SUMMON,TYPE_DEPL]:
            typeEmoji = "<:sprink1:887747751339757599>"

        temp = "__Type :__ " + typeEmoji + " " + allTypeNames[skil.type] + "\n"
        if skil.use not in [None, HARMONIE]:
            temp += "__Stat. utilisé :__ {0} {1}".format(statsEmojis[skil.use],allStatsNames[skil.use])
            if skil.useActionStats != None:
                temp += " ({0} {1})".format(statsEmojis[CRITICAL+1+skil.useActionStats],allStatsNames[CRITICAL+1+skil.useActionStats])
            temp += "\n"

        if skil.description != None:
            temp += "\n__Description :__\n"+skil.quickDesc+["","\n\n"][len(skil.quickDesc)>0]+skil.description+"\n"

        # Power, Success and Damage Type
        if skil.become == None:
            if skil.power > 0:
                if skil.repetition > 1:
                    nbShot = " x{0}".format(skil.repetition)
                else:
                    nbShot = ""

                if multiPower == []:
                    temp += "\n__Puissance :__ {0}".format([f"**{skil.power}**{nbShot}","**Execution**"][int(skil.execution)])
                    if skil.effects != None:
                        for eff in skil.effects:
                            eff = findEffect(eff)
                            if eff != None and eff.type == TYPE_INDIRECT_DAMAGE and eff.trigger == TRIGGER_INSTANT:
                                indPow += (eff.power * skil.effPowerPurcent / 100)

                    if indPow > 0:
                        temp += " **+ {0}{1}**".format(statsEmojis[ACT_INDIRECT_FULL],round(indPow))
                    if skil.maxPower != 0 and skil.maxPower != skil.power:
                        temp += "\n__Puissance Max :__ {0}".format([f"**{skil.maxPower}**{nbShot}","**Execution**"][int(skil.execution)])
                    temp += "\n__Zone d'effet :__ "+ areaNames[skil.area] + "\n__Précision :__ {0}%\n".format(skil.accuracy)
                else:
                    temp += "\n__Puissance :__ **"
                    txtTmp,sumPowa,areaDict, preciDict, maxPowerCom = "(", 0, {}, {}, 0
                    for cmpt in range(len(multiPower)):
                        areaAlreadyAdded, precisionAlreadyAdded, maxPowerCom = False, False, maxPowerCom + multiPower[cmpt].maxPower
                        sumPowa += (multiPower[cmpt].power * multiPower[cmpt].repetition)
                        txtTmp += multiPower[cmpt].emoji + " " + str(int((multiPower[cmpt].power * multiPower[cmpt].repetition)))
                        if cmpt < len(multiPower)-1:
                            txtTmp += " + "
                        else:
                            txtTmp += ")"
                        for areaId in areaDict:
                            if areaId == multiPower[cmpt].area:
                                areaDict[areaId] += multiPower[cmpt].emoji
                                areaAlreadyAdded = True
                                break
                        if not(areaAlreadyAdded):
                            areaDict[multiPower[cmpt].area] = multiPower[cmpt].emoji
                        for precision in preciDict:
                            if precision == multiPower[cmpt].accuracy:
                                preciDict[precision] += multiPower[cmpt].emoji
                                precisionAlreadyAdded = True
                                break
                        if not(precisionAlreadyAdded):
                            preciDict[multiPower[cmpt].accuracy] = multiPower[cmpt].emoji
                    for cmpt in range(len(multiSkill)):
                        if multiSkill[cmpt].effects != None:
                            for eff in multiSkill[cmpt].effects:
                                eff = findEffect(eff)
                                if eff != None and eff.type == TYPE_INDIRECT_DAMAGE and eff.trigger == TRIGGER_INSTANT:
                                    indPow += (eff.power * multiSkill[cmpt].effPowerPurcent / 100)

                    temp += str(sumPowa) + [" + {0}{1} ".format(statsEmojis[ACT_INDIRECT_FULL],round(indPow)),""][indPow<=0] + "** " + txtTmp
                    if sumPowa != maxPowerCom and maxPowerCom != 0:
                        temp += "\n__Puissance maximale :__ **{0}** (".format(maxPowerCom)
                        for cmpt in range(len(multiSkill)):
                            temp += "{0}{1}{2}".format(multiSkill[cmpt].maxPower,multiSkill[cmpt].emoji,[""," + "][cmpt < len(multiSkill)-1])
                        temp += ")\n"
                    temp += "\n__Zones d'effets :__"
                    for cmpt in areaDict:
                        temp += "\n{0} ({1})".format(areaEmojis[cmpt], areaNames[cmpt],areaDict[cmpt])
                    temp += "\n\n__Précisions :__"
                    for cmpt in preciDict:
                        temp += "\n{0}% ({1})".format(cmpt,preciDict[cmpt])
                    temp += "\n"

        else:
            tempMsg = ""
            for tmpSkill in skil.become:
                if tmpSkill.power > 0:
                    multi = maPow = ""
                    if tmpSkill.repetition > 1:
                        multi = " x{0}".format(tmpSkill.repetition)
                    if type(tmpSkill.maxPower) == int and (tmpSkill.maxPower > 0 and tmpSkill.maxPower != tmpSkill.power):
                        maPow = " → **{0}**".format(tmpSkill.maxPower)
                    tempMsg += "**{0}**{2}{3} ({1})\n".format(tmpSkill.power, tmpSkill.name, multi, maPow)
                maxPowerComb += tmpSkill.maxPower

            if tempMsg != "":
                temp += "\n__Puissances :__\n"+tempMsg

            tempMsg = ""
            for tmpSkill in skil.become:
                if tmpSkill.type == TYPE_DAMAGE:
                    tempMsg += "{0}% ({1})\n".format(tmpSkill.accuracy, tmpSkill.name)

            if tempMsg != "":
                temp += "\n__Précisions :__\n"+tempMsg

        suppStats, temp3 = "", ""

        if skil.jaugeEff != None:
            if skil.minJaugeValue != 0:
                temp3 += "\n__Coût minimal en {1} {2} :__ **{0}**".format(skil.minJaugeValue, skil.jaugeEff.emoji[0][0], skil.jaugeEff.name)
            if skil.maxJaugeValue != skil.minJaugeValue:
                temp3 += "\n__Coût maximal en {1} {2} :__ **{0}**".format(skil.maxJaugeValue, skil.jaugeEff.emoji[0][0], skil.jaugeEff.name)

        if skil.range == AREA_MONO and skil.type != TYPE_PASSIVE:
            suppStats += "{0} Se lance sur soi-même\n".format(rangeAreaEmojis[0])

        if skil.effects != [None]:
            effDesc = "\n**__Effet{0} {2}{0} {1} :__**\n".format(["","s"][len(skil.effects)>1],["à la cible",'aux cibles'][skil.area != AREA_MONO], ["octroyé","infligé"][skil.type in hostileTypes])
            if skil.effPowerPurcent != 100:
                if skil.jaugeEff == None or (skil.type not in [TYPE_BOOST,TYPE_ARMOR,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_DAMAGE,TYPE_MALUS]):
                    effDesc += "*Puissance et statistiques : {0}%*\n".format(skil.effPowerPurcent)
                else:
                    effDesc += "*Puissance et statistiques : de {0}% à {1}%*\n".format(skil.effPowerPurcent//2,skil.effPowerPurcent)
            for eff in skil.effects:
                if type(eff) == effect:
                    effDesc += "{0} {1}".format(eff.emoji[0][0], eff.name)
                    if len(skil.effects) > 1 and skil.effects[-1] != eff:
                        effDesc +=", "

            temp3 += effDesc + "\n<:em:866459463568850954>"

        if skil.effectOnSelf != None:
            effDesc = "\n__Effet octroyé au lanceur :__\n"
            if skil.effPowerPurcent != 100 or skil.selfEffPurcent != 100:
                effDesc += "*Puissance et statistiques : {0}%*\n".format(skil.selfEffPurcent)
            effDesc += "{0} {1}".format(skil.effectOnSelf.emoji[0][0], skil.effectOnSelf.name)

            temp3 += effDesc + "\n"

        if skil.become == None and skil.type in friendlyTypes+hostileTypes and not(skil.range == skil.area == AREA_MONO):
            tempEm = areaEmojis[[AREA_ALL_ALLIES,AREA_ALL_ENEMIES][skil.type in hostileTypes]]
            suppStats += "{0} Cible les **{1}**\n".format([rangeAreaEmojis[AREA_ALL_ALLIES],areaEmojis[AREA_ALL_ENEMIES]][skil.type in hostileTypes], ["alliés","ennemis"][skil.type in hostileTypes])

        if skil.onArmor != 1 and skil.become == None:
            suppStats += "{0} Inflige **{1}%** de dégâts aux armures\n".format(["<:abB:934600555916050452>","<:abR:934600570633867365>"][skil.onArmor<0], int(skil.onArmor*100))
        elif skil.become != None:
            for becomeName in skil.become:
                if becomeName.onArmor != 1:
                    temp3 += "\n__{2} {1}__ inflige **{0}%** de ses dégâts aux armures".format(int(becomeName.onArmor*100), becomeName.name, becomeName.emoji)

        if skil.shareCooldown:
            suppStats += "Cooldown Partagé"
        if skil.initCooldown > 1 and skil.type != TYPE_PASSIVE:
            suppStats += "Cooldown Initial : {0}\n".format(skil.initCooldown)

        if skil.condition != []:
            tempTabl, tempName = [aspiEmoji,elemEmojis][skil.condition[1]==ELEMENT], [inspi,elemNames][skil.condition[1]==ELEMENT]
            suppStats += "{0} Exclusivité de l'{1} **{2}**\n".format(tempTabl[skil.condition[2]],["aspiration","élément"][skil.condition[1]==ELEMENT], tempName[skil.condition[2]])

        if skil.replay:
            suppStats += "<:qqLuna:932318030380302386> Permet de **rejouer son tour**\n"

        if skil.maxHpCost > 0:
            suppStats += "<:dvin:1004737746377654383> Réduit de **{0}%** les PV Max\n".format(skil.maxHpCost)
        if skil.hpCost > 0:
            suppStats += "<:dmon:1004737763771433130> Réduit de **{0}%** les PV actuels\n".format(skil.hpCost)

        if skil.ultimate:
            suppStats += "<:littleStar:925860806602682369> Compétence Ultime\n"
        if skil.execution :
            suppStats += "<:sacrified:973313400056725545> Exécution"
        if skil.group != 0:
            suppStats += "{0} Compétence {1}\n".format(["","<:dvin:1004737746377654383>","<:dmon:1004737763771433130>"][skil.group],skillGroupNames[skil.group][0].upper()+skillGroupNames[skil.group][1:])
        if skil.setAoEDamage:
            suppStats += "<:dislocation:1052697663402950667> Ignore la réduction de Dégâts de zone\n"
        if skil.lifeSteal > 0:
            suppStats += "<:vampire:900312789686571018> Soigne de **{0}%** des dégâts infligés\n".format(skil.lifeSteal)
        if skil.aoeLifeSteal > 0:
            suppStats += "<:aoeLifeSteal:1100770895846457376> Soigne les alliés alentours de **{0}%** des dégâts infligés\n".format(skil.aoeLifeSteal)
        if skil.armorConvert > 0:
            suppStats += "<:converted:902527031663788032> Vous octroi une armure équivalent à **{0}%** des dégâts infligés\n".format(skil.armorConvert)
        if skil.aoeArmorConvert > 0:
            suppStats += "<:aoeConvert:1100770918340497519> Octroi aux alliés alentours une armure équivalent à **{0}%** des dégâts infligés\n".format(skil.aoeArmorConvert)
        if skil.erosion != 0:
            suppStats += "<:ConR:1028695463651717200> Réduit les PVs Max de la cible de **{0}%** des dégâts infliés\n".format(skil.erosion)
        temp2 = ""
        if skil.tpCac:
            suppStats += "<:iliLightSpeed:1046384202792308797> Saute **devant** de la cible\n"
        if skil.tpBehind:
            suppStats += "<:liaCounter:998001563379437568> Saute **derrière** de la cible\n"
        if skil.percing > 0:
            suppStats += "{1} Ignore **{0}%** de la Résistance de la cible\n".format(skil.percing,statsEmojis[PERCING])

        if skil.knockback > 0 and skil.become == None:
            suppStats += "<:piedVolt:1034208868068233348> Pousse les cibles de **{0} case{1}**\n".format(skil.knockback,["","s"][skil.knockback > 1])
        if skil.pull > 0 and skil.become == None:
            suppStats += "<:spectralFury:1033016230333911080> Attire les cibles de **{0} case{1}**\n".format(skil.pull,["","s"][skil.pull > 1])
        if skil.jumpBack:
            suppStats += "<:retPercu:1034210776703062057> Vous fait reculer de **{0} case{1}**\n".format(skil.jumpBack,["","s"][skil.jumpBack > 1])
        if skil.garCrit:
            suppStats += "{0} Inflige forcément un coup critique\n".format(statsEmojis[CRITICAL])

        if skil.jaugeEff != None:
            temp2 = "\nCette compétence octroi et utilise {0} **{1}**. La valeur de cette jauge augmente dans les conditions suivantes :\n".format(skil.jaugeEff.emoji[0][0],skil.jaugeEff.name)
            jaugeVal: jaugeValue = skil.jaugeEff.jaugeValue
            for conds in jaugeVal.conds:
                temp2 += "- "+incCondsStr[conds.type] + "** +{0}**\n".format(conds.value)
                if conds.type == INC_USE_SKILL:
                    for condSkill in conds.add:
                        temp2 += "> - {0} {1}\n".format(condSkill.emoji, condSkill.name)
                elif conds.type == INC_EFFECT_TRIGGERED:
                    for condEff in conds.add:
                        temp2 += "> - {0} {1}\n".format(condEff.emoji[0][0], condEff.name)
                elif conds.type == INC_USE_ELEMENT_SKILL:
                    temp2 += "> - {0} {1}\n".format(elemEmojis[conds.add],elemNames[conds.add])
                elif conds.type == INC_USE_GROUP_SKILL:
                    temp2 += "> - {0} Compétences {1}\n".format(["","<:dvin:1004737746377654383>","<:dmon:1004737763771433130>"][conds.add],["Normales","Divines","Démoniaques"])

        if temp2 != "":
            temp3 += "\n"+temp2

        if skil.become != None:
            allreadyAdd = False
            for becomeName in skil.become:
                if becomeName.knockback > 0:
                    if not(allreadyAdd):
                        temp3 += "\n\n**__Repoussement :__**"
                        allreadyAdd = True
                    temp3 += "\n__{1}__ repousse la cible de **{0}** case{2}".format(
                        becomeName.knockback, becomeName.name, ["", "s"][becomeName.knockback > 1])

        repEmb:interactions.Embed = interactions.Embed(title="__{0}__".format(skil.name), color=user.color,description=desc+"\n\n__Statistiques :__"+"\n"+temp+"\n"+suppStats+temp3)

        if skil.become == None: # AREA
            if skil.type != TYPE_PASSIVE:
                repEmb.add_field(name="__Portée et air d'effet :__", value="__Portée :__ {0} {1}\n__Zone d'effet :__ {2} {3}".format(rangeAreaEmojis[skil.range],areaNames[skil.range],areaEmojis[skil.area],areaNames[skil.area]))
        else:
            tempValuesRange, tempValuesArea = "", ""
            for skilly in skil.become:
                tempValuesRange += "{0} __{1}__ : {2} {3}\n".format(skilly.emoji, skilly.name, rangeAreaEmojis[skilly.range], areaNames[skilly.range])
                tempValuesArea += "{0} __{1}__ : {2} {3}\n".format(skilly.emoji, skilly.name, areaEmojis[skilly.area], areaNames[skilly.area])

            repEmb.add_field(name="<:em:866459463568850954>\n__Portées :__", value=tempValuesRange,inline=False)
            repEmb.add_field(name="<:em:866459463568850954>\n__Zones d'Effets :__", value=tempValuesArea,inline=False)

        if skil.effectAroundCaster != None:
            if type(skil.effectAroundCaster[2]) == effect:
                toAdd = "__Effet :__ {1} {0}".format(skil.effectAroundCaster[2].name, skil.effectAroundCaster[2].emoji[0][0])
            else:
                toAdd = "__Puissance :__ {0}".format(skil.effectAroundCaster[2])
            
            typeEmoji = ''
            if skil.effectAroundCaster[0] == TYPE_DAMAGE:
                typeEmoji += statsEmojis[ACT_DIRECT_FULL]
            elif skil.effectAroundCaster[0] == TYPE_INDIRECT_DAMAGE:
                typeEmoji += statsEmojis[ACT_INDIRECT_FULL]
            elif skil.effectAroundCaster[0] in [TYPE_BOOST,TYPE_MALUS]:
                typeEmoji += statsEmojis[ACT_BOOST_FULL]
            elif skil.effectAroundCaster[0] == TYPE_ARMOR:
                typeEmoji += statsEmojis[ACT_SHIELD_FULL]
            elif skil.effectAroundCaster[0] in [TYPE_HEAL,TYPE_INDIRECT_HEAL]:
                typeEmoji += statsEmojis[ACT_HEAL_FULL]
            elif skil.effectAroundCaster[0] in [TYPE_SUMMON,TYPE_DEPL]:
                typeEmoji += "<:sprink1:887747751339757599>"
            elif skil.effectAroundCaster[0] == TYPE_RESURECTION:
                typeEmoji += "'<:renisurection:873723658315644938>'"
            else:
                typeEmoji += "<:i1b:866828199156252682>"
            repEmb.add_field(name="<:em:866459463568850954>\n__Effet supplémentaire autour du lanceur :__",inline=False,value="__Type :__ {3} {0}\n__Zone d'effet :__ {4} {1}\n{2}".format(allTypeNames[skil.effectAroundCaster[0]], areaNames[skil.effectAroundCaster[1]], toAdd, typeEmoji,areaEmojis[skil.effectAroundCaster[1]]))

        if skil.emoji[1] == "a":
            repEmb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.gif".format(getEmojiObject(skil.emoji).id))
        else:
            repEmb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(skil.emoji).id))

        allReadySeen, effToSee = [], []
        for eff in skil.effects:
            if eff != None:
                eff = findEffect(eff)
                if eff not in allReadySeen:
                    allReadySeen.append(eff)
                    effToSee.append(1)
                else:
                    for cmpt in range(len(effToSee)):
                        if allReadySeen[cmpt].id == eff.id:
                            effToSee[cmpt] += 1

        for cmpt in range(len(allReadySeen)):
            txt = ["", " x{0}".format(effToSee[cmpt])][effToSee[cmpt] > 1]
            repEmb = infoEffect(allReadySeen[cmpt], user, repEmb, txt=txt, powerPurcent=skil.effPowerPurcent)

        if skil.become != None:
            for skilly in skil.become:
                if skilly.effects != [None]:
                    allReadySeenEff = []
                    for eff in skilly.effects:
                        if eff.id not in allReadySeenEff:
                            repEmb = infoEffect(findEffect(eff), user, repEmb, ctx, txt=" ({0})".format(skilly.name))
                            allReadySeenEff.append(eff.id)

        if skil.effectOnSelf != None:
            if skil.type == TYPE_PASSIVE:
                repEmb = infoEffect(skil.effectOnSelf, user, repEmb, True," (passif)", powerPurcent=skil.selfEffPurcent)
            else:
                repEmb = infoEffect(skil.effectOnSelf, user, repEmb, True , powerPurcent=skil.selfEffPurcent)

        if skil.effectAroundCaster != None and type(skil.effectAroundCaster[2])==effect:
            repEmb = infoEffect(skil.effectAroundCaster[2], user, repEmb, powerPurcent=[skil.effPowerPurcent,int(liaLB.effPowerPurcent/5)][skil==liaLB],txt = " *(autour du lanceur)*")

        if skil.invocation != None:
            repEmb = infoInvoc(findSummon(skil.invocation), repEmb)
        if skil.depl != None:
            repEmb.add_field(name="<:em:866459463568850954>\n__Déployable__",value="Cette compétence permet de déployer {0} __{1}__\n\"{2}\"".format(skil.depl.icon[0],skil.depl.name,skil.depl.description),inline=False)
            repEmb.add_field(name="<:em:866459463568850954>\n__Zone d'effet ({0}) :__".format(skil.depl.name), value=visuArea(skil.depl.skills.area, wanted=[ALLIES, ENEMIES][skil.depl.skills.type in hostileTypes], ranged=False))

        repEmb.description = reduceEmojiNames(repEmb.description)
        for cmpt in range(len(repEmb.fields)):
            repEmb.fields[cmpt].name = reduceEmojiNames(repEmb.fields[cmpt].name)
            repEmb.fields[cmpt].value = reduceEmojiNames(repEmb.fields[cmpt].value)

        if getEmbedLength(repEmb) > 4000:
            repEmb = interactions.Embed(title=skil.name, color=user.color, description=desc + "\n__Statistiques :__\n"+temp+"\n\nCertaines infromations n'ont pas pu être affichées.")
            if skil.emoji[1] == "a":
                repEmb.set_thumbnail(
                    url="https://cdn.discordapp.com/emojis/{0}.gif".format(getEmojiObject(skil.emoji).id))
            else:
                repEmb.set_thumbnail(
                    url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(skil.emoji).id))

        if skil.url != None:
            repEmb.set_image(url=skil.url)

        if skil.become != None:         # Effect on self list
            listEffSelf, listEffCombo, listCombo = "", {}, ""
            for skilly in skil.become:
                if skilly.effectOnSelf != None:
                    if not skilly.effectOnSelf.silent:
                        listEffSelf += "\n{3} __{0}__ : {1} {2}".format(skilly.name, skilly.effectOnSelf.emoji[0][0], skilly.effectOnSelf.name, skilly.emoji)
                    listEffCombo[skilly.effectOnSelf.id] = skilly

                if skilly.needEffect != None:
                    for eff in skilly.needEffect:
                        try:
                            if listCombo == "":
                                listCombo = "{0} -> {1}".format(listEffCombo[eff.id],skilly)
                            else:
                                listCombo += " -> {0}".format(skilly)
                        except KeyError:
                            pass

            if listCombo != "":
                repEmb.add_field(name="__Combo :__", value=listCombo, inline=False)

            if len(listEffSelf) > 0:
                repEmb.add_field(name="__Effets sur soi des compétences :__", value=listEffSelf, inline=False)

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

    repEmb.set_footer(text="Id : {0} - iaPow : {1}".format(skil.id,skil.iaPow))
    return repEmb

def infoWeapon(weap: weapon, user: char, ctx):
    repEmb = interactions.Embed(title=weap.emoji + "**__"+ unhyperlink(weap.name)+ "__**", color=user.color)
    repEmb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(weap.emoji).id))

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

    prioMsg = ["Faible","Normale","Elevée"][int(weap.priority+1)]
    info += "\n__Zone d'effet :__ " + cible + f"\n__Statistique utilisée :__ {statsEmojis[weap.use]} {nameStats[weap.use]}\n__Fréquence d'uilisation :__ {prioMsg}"

    if weap.onArmor != 1 and weap.type == TYPE_DAMAGE:
        info = f"\n__Dégâts sur armure :__ **{int(weap.onArmor*100)}**%"

    element = ""
    if weap.affinity != None:
        element = f"\n__Affinité :__ {elemEmojis[weap.affinity]} {elemNames[weap.affinity]}"

    if weap.repetition > 1:
        nbShot = " x{0}".format(weap.repetition)
    else:
        nbShot = ""

    repEmb.add_field(name="<:em:866459463568850954>\n__Informations Principales :__", value=f"__Position :__ {portee}\n__Portée :__ {weap.effectiveRange}\n__Type :__ {allTypeNames[weap.type]}\n__Puissance :__ {weap.power}{nbShot}\n__Précision :__ {weap.accuracy}%", inline=True)
    repEmb.add_field(name="<:em:866459463568850954>\n__Statistiques secondaires :__",value=f'{element}{info}', inline=True)
    bonus, malus = "", ""
    stats = weap.allStats()+[weap.resistance, weap.percing, weap.critical]
    for a in range(len(stats)):
        if stats[a] != 0:
            bonus += "{0} __{1}__ : {2}{3}\n".format(statsEmojis[a],allStatsNames[a],["","+"][stats[a]>0],stats[a])

    if bonus != "":
        repEmb.add_field(name="<:em:866459463568850954>\n__Bonus de statistiques :__",value=bonus, inline=False)

    repEmb.add_field(name="__Portée :__", value=visuArea(weap.effectiveRange, wanted=weap.target))

    if weap.area != AREA_MONO and weap.area != AREA_ALL_ALLIES and weap.area != AREA_ALL_ENEMIES and weap.area != AREA_ALL_ENTITES:
        ballerine, babie = [TYPE_ARMOR, TYPE_BOOST, TYPE_INDIRECT_HEAL, TYPE_INDIRECT_REZ,TYPE_RESURECTION, TYPE_HEAL], [TYPE_INDIRECT_DAMAGE, TYPE_MALUS, TYPE_DAMAGE]
        for a in ballerine:
            if a == weap.type:
                repEmb.add_field(name="__Zone d'effet :__", value=visuArea(
                    weap.area, wanted=ALLIES, ranged=False))
                break

        for a in babie:
            if a == weap.type:
                repEmb.add_field(name="__Zone d'effet :__", value=visuArea(
                    weap.area, wanted=ENEMIES, ranged=False))
                break

    if weap.effects != None:
        infoEffect(weap.effects, user, repEmb,txt=" (effet passif)")

    if weap.effectOnUse != None:
        infoEffect(weap.effectOnUse, user, repEmb,txt=" (effet sur la cible)")
    repEmb.set_footer(text="Id : "+weap.id)
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

    repEmb = interactions.Embed(title=unhyperlink(weap.name), color=user.color,
                           description=f"Niveau : {weap.minLvl}\nType : {temp}\nOrientation : {weap.orientation}{element}")
    repEmb.set_thumbnail(
        url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(weap.emoji).id))

    bonus, malus = "", ""
    stats = weap.allStats()+[weap.resistance, weap.percing, weap.critical] + [weap.negativeHeal*-1, weap.negativeBoost*-1,weap.negativeShield*-1, weap.negativeDirect*-1, weap.negativeIndirect*-1]
    for cmpt in range(len(stats)):
        if stats[cmpt] > 0:
            bonus += "{2} __{0}__ : +{1}\n".format(allStatsNames[cmpt],stats[cmpt],statsEmojis[cmpt])
        elif stats[cmpt] < 0:
            malus += "{2} __{0}__ : {1}\n".format(allStatsNames[cmpt],stats[cmpt],statsEmojis[cmpt])

    if bonus != "":
        repEmb.add_field(name="__Bonus de statistiques :__",
                         value=bonus, inline=True)
    if malus != "":
        repEmb.add_field(name="__Malus de statistiques :__",
                         value=malus, inline=True)

    if weap.effects != None:
        infoEffect(weap.effects, user, repEmb, txt= " (effet passif)")
    repEmb.set_footer(text="Id : "+weap.id)
    return repEmb

def infoOther(other: other, user: char):
    weap = other
    repEmb = interactions.Embed(title=weap.name, color=user.color,
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
        stats[a] = round(aspiStats[user.aspiration][a]*0.1 +aspiStats[user.aspiration][a]*0.9*user.level/50)

    user.points = user.level * BONUSPOINTPERLEVEL + 5 + ((user.level//10) * 5)
    user.majorPointsCount = user.stars
    user.bonusPoints = [0, 0, 0, 0, 0, 0, 0]
    user.majorPoints = [0, 0, 0, 0, 0, 0, 0]+[0, 0, 0]+[0, 0, 0, 0, 0]

    if user.autoPoint:
        while user.points > 0:
            for recStat in recommandedStat[user.aspiration]:
                if user.bonusPoints[recStat] < MAXBONUSPERSTAT and user.points > 0:
                    user.bonusPoints[recStat] += 1
                    user.points -= 1
    return userMajStats(user, stats)

def silentRestats(user: char):
    """Function for restat a user without reset the bonus points"""
    stats = user.allStats()
    for a in range(0, len(stats)):
        stats[a] = round(aspiStats[user.aspiration][a]*0.1 + aspiStats[user.aspiration][a]*0.9*user.level/50)+user.bonusPoints[a]

    return userMajStats(user, stats)

async def addExpUser(bot: interactions.Client, path: Union[str,char], ctx: Union[interactions.Message, interactions.SlashContext], exp=3, coins=0, send=True):
    if type(path) == str:
        user = loadCharFile(path)
    else:
        user = path

    if user.level < MAXLEVEL:
        user.exp = user.exp + exp
    else:
        user.exp = 0
    user.currencies = user.currencies + coins

    upLvl = (user.level-1)*50+30

    while user.exp >= upLvl and user.level < MAXLEVEL:
        user.points = user.points + BONUSPOINTPERLEVEL
        if (user.level+1) // 10 == 0:
            user.points = user.points + 5
        temp = user.allStats()
        up = [0, 0, 0, 0, 0, 0, 0]
        stats = user.allStats()
        for a in range(0, len(stats)):
            stats[a] = round(aspiStats[user.aspiration][a]*0.1 +aspiStats[user.aspiration][a]*0.9*user.level/50+user.bonusPoints[a])
            temp[a] = round(aspiStats[user.aspiration][a]*0.1+aspiStats[user.aspiration][a]*0.9*(user.level+1)/50+user.bonusPoints[a])
            up[a] = temp[a]-stats[a]

        user.strength, user.endurance, user.charisma, user.agility, user.precision, user.intelligence, user.magie = temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6]

        user.exp = user.exp - upLvl
        user.level = user.level + 1
        upLvl = (user.level-1)*50+30

        if user.level % 5 == 0 and user.autoStuff and user.level <= MAXLEVEL:
            user.stuff[0] = getAutoStuff(user.stuff[0],user,recommandedStuffStat[user.aspiration])
            user.stuff[1] = getAutoStuff(user.stuff[1],user,recommandedStuffStat[user.aspiration])
            user.stuff[2] = getAutoStuff(user.stuff[2],user,recommandedStuffStat[user.aspiration])

        if user.autoPoint:
            while user.points > 0:
                for recStat in recommandedStat[user.aspiration]:
                    if user.bonusPoints[recStat] < MAXBONUSPERSTAT and user.points > 0:
                        user.bonusPoints[recStat] += 1
                        user.points -= 1

    saveCharFile(user=user)
    return user

def getChoisenSelect(select: Union[StringSelectMenu, ActionRow], value: str):
    trouv = False
    if type(select) == ActionRow:
        select = select.data.components[0]
    temp = copy.deepcopy(select)
    for op in temp.options:
        if op.value == value:
            trouv = True
            op.default = True
    if trouv:
        temp.disabled = True
    return temp

async def downloadAllHeadGearPng(bot: interactions.Client, msg=None, lastTime=None):
    listEmojiHead = []
    for stuffy in stuffs:
        if stuffy.type == 0:
            listEmojiHead.append(stuffy.emoji)
    listDir = os.listdir("./data/images/headgears/")
    num, cmpt = len(listEmojiHead), 0
    for a in listEmojiHead:
        emojiObject, finded = getEmojiObject(a), False
        if emojiObject.name + ".png" not in listDir:
            print("Trying to find the emoji of {0} on the lasts guilds...".format(emojiObject.name))
            for b in stuffIconGuilds[-5:]:
                guild = bot.get_guild(b)
                await asyncio.sleep(1)
                emojiList = await guild.fetch_all_custom_emojis()
                for emoji_2 in emojiList:
                    try:
                        if emoji_2.id == emojiObject.id:
                            image = requests.get("https://cdn.discordapp.com/emojis/{0}.webp".format(emoji_2.id), stream=True)
                            image.raw.decode_content = True
                            open(f"./data/images/headgears/{emojiObject.name}.png", "wb").write(image.content)
                            image = PIL.Image.open(f"./data/images/headgears/{emojiObject.name}.png")
                            image = image.resize((70, 70))
                            image.save(f"./data/images/headgears/{emojiObject.name}.png")
                            print(" - "+emojiObject.name + " downloaded")
                            finded=True
                            listDir = os.listdir("./data/images/headgears/")
                            break
                    except Exception as e:
                        print("A error happened during the downloading of {0} :\nurl : {1}\n{2}\n=======".format(emoji_2.name,"https://cdn.discordapp.com/emojis/{0}.webp".format(emoji_2.id),e))
            if not(finded):
                print(" - {0}'s emoji not quick finded, looking more deeply...".format(emojiObject.name))
                for b in stuffIconGuilds[:-5]:
                    guild = bot.get_guild(b)
                    await asyncio.sleep(1)
                    emojiList = await guild.fetch_all_custom_emojis()
                    for emoji_2 in emojiList:
                        try:
                            if emoji_2.id == emojiObject.id:
                                image = requests.get("https://cdn.discordapp.com/emojis/{0}.webp".format(emoji_2.id), stream=True)
                                image.raw.decode_content = True
                                open(f"./data/images/headgears/{emojiObject.name}.png", "wb").write(image.content)
                                image = PIL.Image.open(f"./data/images/headgears/{emojiObject.name}.png")
                                image = image.resize((70, 70))
                                image.save(f"./data/images/headgears/{emojiObject.name}.png")
                                print(" - "+emojiObject.name + " downloaded")
                                finded=True
                                listDir = os.listdir("./data/images/headgears/")
                                break
                        except Exception as e:
                            print("A error happened during the downloading of {0} :\nurl : {1}\n{2}\n=======".format(emoji_2.name,"https://cdn.discordapp.com/emojis/{0}.webp".format(emoji_2.id),e))
            
            if not(finded):
                print(emojiObject.name + " not found")

        if msg != None:
            cmpt += 1
            now = datetime.now(parisTimeZone).second
            if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
                lastTime = now
                await msg.edit(embeds=interactions.Embed(title="l!admin resetCustomEmoji", description="Téléchargement des images d'accessoires ({0}%)".format(round(cmpt/num*100, 1))))

async def downloadAllWeapPng(bot: interactions.Client, msg=None, lastTime=None):
    listEmojiWeapon = []
    for weap in weapons:
        listEmojiWeapon.append(weap.emoji)
    listEmojiWeapon = listEmojiWeapon + etInkBases + etInkLines
    listDir = os.listdir("./data/images/weapons/")
    num, cmpt = len(listEmojiWeapon+etInkBases+etInkLines), 0
    for a in listEmojiWeapon:
        emojiObject, finded = getEmojiObject(a), False
        if emojiObject.name + ".png" not in listDir:
            for b in weaponIconGuilds:
                guild = bot.get_guild(b)
                await asyncio.sleep(1)
                emojiList = await guild.fetch_all_custom_emojis()
                for emoji_2 in emojiList:
                    try:
                        if int(emoji_2.id) == int(emojiObject.id):
                            image = requests.get("https://cdn.discordapp.com/emojis/{0}.webp".format(emoji_2.id), stream=True)
                            image.raw.decode_content = True
                            open(f"./data/images/weapons/{emojiObject.name}.png", "wb").write(image.content)
                            image = PIL.Image.open(f"./data/images/weapons/{emojiObject.name}.png")
                            background = PIL.Image.new("RGBA", (120, 120), (0, 0, 0, 0))
                            image = image.resize((100, 100))
                            background.paste(image, (10, 10))
                            background.save(f"./data/images/weapons/{emojiObject.name}.png")
                            print(emojiObject.name + " downlowded")
                            finded=True
                            listDir = os.listdir("./data/images/weapons/")
                            break
                    except Exception as e:
                        print("A error happened during the downloading of {0} :\nurl : {1}\n{2}\n=======".format(emoji_2.name,"https://cdn.discordapp.com/emojis/{0}.webp".format(emoji_2.id),e))
            if not(finded):
                print(emojiObject.name + " not found")

        if msg != None:
            cmpt += 1
            now = datetime.now(parisTimeZone).second
            if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
                lastTime = now
                await msg.edit(embeds=interactions.Embed(title="l!admin resetCustomEmoji", description="Téléchargement des images d'armes ({0}%)".format(round(cmpt/num*100, 1))))

    if not(os.path.exists("./data/images/weapons/akifaux.png")):
        image = requests.get(
            "https://cdn.discordapp.com/emojis/887334842595942410.png?v=1", stream=True)
        image.raw.decode_content = True
        open(f"./data/images/weapons/akifaux.png", "wb").write(image.content)
        image = PIL.Image.open(f"./data/images/weapons/akifaux.png")
        background = PIL.Image.new("RGBA", (120, 120), (0, 0, 0, 0))
        image = image.resize((100, 100))
        background.paste(image, (10, 10))
        background = background.rotate(30)
        background.save(f"./data/images/weapons/akifaux.png")
        print("akifaux downlowded")

async def downloadAllIconPng(bot: interactions.Client):
    listEmojiHead = EmIcon
    listDir = os.listdir("./data/images/char_icons/")
    for a in (1, 2, 4):
        for b in range(0, len(listEmojiHead[a])):
            emojiObject, finded = getEmojiObject(listEmojiHead[a][b]), False
            if emojiObject.name + ".png" not in listDir:
                for b in [862320563590529056, 615257372218097691, 810212019608485918, 894528703185424425]:
                    guild = bot.get_guild(b)
                    emojiList = await guild.fetch_all_custom_emojis()
                for emoji_2 in emojiList:
                    try:
                        if emoji_2.id == emojiObject.id:
                            image = requests.get("https://cdn.discordapp.com/emojis/{0}.webp".format(emoji_2.id), stream=True)
                            image.raw.decode_content = True
                            open(f"./data/images/char_icons/{emojiObject.name}.png", "wb").write(image.content)
                            image = PIL.Image.open(f"./data/images/char_icons/{emojiObject.name}.png")
                            background = PIL.Image.new("RGBA", (145, 145), (0, 0, 0, 0))
                            image = image.resize((128, 128))
                            background.paste(image, ((145-128)//2, (145-128)//2))
                            background.save(f"./data/images/char_icons/{emojiObject.name}.png")
                            customIconDB.addIconFiles(a, b, f"{emojiObject.name}.png")
                            print(emojiObject[0] + " downlowded")
                            listDir = os.listdir("./data/images/char_icons/")
                            finded=True
                            break
                    except Exception as e:
                        print("A error happened during the downloading of {0} :\nurl : {1}\n{2}\n=======".format(emoji_2.name,"https://cdn.discordapp.com/emojis/{0}.webp".format(emoji_2.id),e))

                if not(finded):
                    print(emojiObject[0] + " not found")

async def makeCustomIcon(bot: interactions.Client, user: char, returnImage: bool = False):
    # Paramètres de l'accessoire ----------------------------------
    if user.apparaAcc == None:
        if os.path.exists("./data/images/headgears/{0}.png".format(getEmojiObject(user.stuff[0].emoji).name)):
            accessoire, pos = PIL.Image.open("./data/images/headgears/{0}.png".format(getEmojiObject(user.stuff[0].emoji).name)), user.stuff[0].position
        else:
            accessoire  = PIL.Image.new("RGBA", [0,0], (0, 0, 0, 0))

    else:
        user.apparaAcc, user.apparaWeap = findStuff(user.apparaAcc), findWeapon(user.apparaWeap)
        if os.path.exists("./data/images/headgears/{0}.png".format(getEmojiObject(user.apparaAcc.emoji).name)):
            accessoire, pos = PIL.Image.open("./data/images/headgears/{0}.png".format(getEmojiObject(user.apparaAcc.emoji).name)), user.apparaAcc.position
        else:
            accessoire  = PIL.Image.new("RGBA", [0,0], (0, 0, 0, 0))

    # Récupération de l'icone de base -----------------------------
    tablBase = [["./data/images/char_icons/baseIka.png", "./data/images/char_icons/baseTako.png"], ["./data/images/char_icons/ikaCatBody.png", "./data/images/char_icons/takoCatBody.png"], ["./data/images/char_icons/komoriBody.png", "./data/images/char_icons/komoriBody.png"],["./data/images/char_icons/birdColor.png", "./data/images/char_icons/birdColor.png"], ["./data/images/char_icons/skeletonColor.png", "./data/images/char_icons/skeletonColor.png"], ['./data/images/char_icons/fairyColor.png', './data/images/char_icons/fairy2Color.png']][user.iconForm]
    tablLine = [["./data/images/char_icons/empty_squid.png", "./data/images/char_icons/empty_octo.png"], ["./data/images/char_icons/ikaCatLine.png", "./data/images/char_icons/takoCatLine.png"], ["./data/images/char_icons/komoriLine.png", "./data/images/char_icons/komoriLine.png"],["./data/images/char_icons/birdLine.png", "./data/images/char_icons/birdLine.png"], ["./data/images/char_icons/skeletonLine.png", "./data/images/char_icons/skeletonLine.png"], ["./data/images/char_icons/fairyLine.png", "./data/images/char_icons/fairy2Line.png"]][user.iconForm]
    background = PIL.Image.open(tablBase[user.species-1])
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
        background2 = PIL.Image.new("RGBA", background.size, (0, 0, 0, 0))

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
            background2 = PIL.Image.new("RGBA", background.size, (0, 0, 0, 0))
        cmpt = 0
        while cmpt < user.stars:
            litStar = PIL.Image.open("./data/images/char_icons/littleStar.png")
            litStar = litStar.resize((38, 38))
            background2.paste(litStar, (30*(cmpt % 4), 30*(cmpt//4)), litStar)
            litStar.close()
            cmpt += 1

    pixel = background.load()
    layer = PIL.Image.open(tablLine[user.species-1])

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
        weapToSee = findWeapon(user.weapon)
        weapEmName = getEmojiObject(weapToSee.emoji).name
        if user.apparaWeap != None:
            weapToSee = findWeapon(user.apparaWeap)
            weapEmName = getEmojiObject(weapToSee.emoji).name

        if (user.apparaWeap != None and user.apparaWeap.id in eternalInkWeaponIds) or (user.apparaWeap == None and user.weapon.id in eternalInkWeaponIds):
            if user.apparaWeap != None:
                toBase = getEmojiObject(user.apparaWeap.emoji).name
            else:
                toBase = getEmojiObject(user.weapon.emoji).name
            line = PIL.Image.open("./data/images/weapons/Line{0}.png".format(toBase))
            base = PIL.Image.open("./data/images/weapons/Base{0}.png".format(toBase))

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
            weapon = PIL.Image.open(
                "./data/images/weapons/{0}.png".format(weapEmName))
        else:
            weapon = PIL.Image.open("./data/images/weapons/akifaux.png")

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
            element = PIL.Image.open(
                "./data/images/elemIcon/"+getEmojiObject(secElemEmojis[user.secElement]).name+".png")
            background.paste(element, [
                             (0, 90), (background.size[0]-element.size[0], 90)][user.handed], element)
            element.close()

        element = PIL.Image.open("./data/images/elemIcon/" +
                             getEmojiObject(elemEmojis[user.element]).name+".png")
        background.paste(element, [
                         (0, 90), (background.size[0]-element.size[0], 90)][user.handed], element)
        element.close()

    # Updating the new emote and the database
    imgByteArr = io.BytesIO()
    background.save(f"./data/images/temp.png")
    background.save(imgByteArr, format="png")
    background = imgByteArr.getvalue()

    if returnImage:
        return background

    iconGuildList = []
    if os.path.exists("../Kawi/"):
        iconGuildList = ShushyCustomIcons
    else:
        iconGuildList = LenaCustomIcons

    background = "./data/images/temp.png"

    if not(customIconDB.haveCustomIcon(user)):
        for icGuildID in iconGuildList:
            try:
                icGuild = bot.get_guild(icGuildID)
                emojiList = await icGuild.fetch_all_custom_emojis()
                if len(emojiList) < icGuild.emoji_limit:
                    try:
                        new_icon = await asyncio.wait_for(icGuild.create_custom_emoji(name=remove_accents(user.name), imagefile=background), timeout=3)
                        customIconDB.editCustomIcon(user, new_icon)
                        print(f"{user.name}'s new emoji uploaded")
                    except asyncio.TimeoutError:
                        print("{0}'s emoji took to long to upload".format(user.name))
                    break
            except:
                print_exc()

    else:
        customId = getEmojiObject(customIconDB.getCustomIcon(user)).id
        custom = None
        for icGuild in iconGuildList:
            icGuild: interactions.Guild = bot.get_guild(icGuild)
            emojiList = await icGuild.fetch_all_custom_emojis()
            for custom in emojiList:
                if custom.id == customId:
                    try:
                        userName = remove_accents(user.name)
                        while len(userName) < 2:
                            userName += "_"
                        new_icon = await asyncio.wait_for(icGuild.create_custom_emoji(name=userName, imagefile=background), timeout=3)
                        customIconDB.editCustomIcon(user, new_icon)
                        await custom.delete()
                        print(f"{user.name}'s emoji updated")
                    except asyncio.TimeoutError:
                        print("{0}'s emoji took to long to upload".format(user.name))
                    except:
                        print_exc()
                        print("{0} - {1}".format(custom.name,custom.id))
                    break

async def getUserIcon(bot: interactions.Client, user: char):
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

def infoInvoc(invoc: invoc, emb: interactions.Embed):
    emb.add_field(name="<:em:866459463568850954>\n{} __{}__".format(invoc.icon[0],invoc.name), value=reduceEmojiNames(f"__Aspiration :__ {aspiEmoji[invoc.aspiration]} {inspi[invoc.aspiration]}\n__Elément :__ {elemEmojis[invoc.element]} {elemNames[invoc.element]}\n__Description :__\n{invoc.description}"), inline=False)
    stats, rep = invoc.allStats()+[invoc.resistance, invoc.percing, invoc.critical], ""

    for a in range(0, len(stats)):
        if type(stats[a]) == list:
            if stats[a][0] in [PURCENTAGE,HARMONIE]:
                rep += "\n__{0} {1} :__ {2}%".format(statsEmojis[a],allStatsNames[a],highlight(round(stats[a][1]*100)))
                if stats[a][0] == HARMONIE:
                    rep += " (Harmonie)"
        else:
            rep += "\n__{0} {1} :__ {2}".format(statsEmojis[a],allStatsNames[a],highlight(stats[a]))

    emb.add_field(name="<:em:866459463568850954>\n__Statistiques :__", value=reduceEmojiNames(rep), inline=False)
    
    rep = ""
    if invoc.weapon.priority != WEAPON_PRIORITY_NONE:
        rep += "{0} __{1}__ :\n{2}\n\n".format(invoc.weapon.emoji,invoc.weapon.name,invoc.weapon.getSummary())
    for a in invoc.skills:
        if type(a) == skill:
            rep += "{0} __{1}__ :\n> {2}\n\n".format(a.emoji,a.name,a.description.replace("\n","\n> "))

    emb.add_field(name="<:em:866459463568850954>\n__Armes et compétences :__", value=reduceEmojiNames(rep), inline=False)
    return emb

def infoAllie(allie: tmpAllie):
    var = ""
    if allie.variant:
        var = "Cet allié temporaire est une variante d'un autre allié temporaire\n\n"
    teamName = ""
    if allie.npcTeam != None:
        teamName = "__Affinité :__ {0}{1}\n".format(npcTeamEmojis[allie.npcTeam]+[""," "][npcTeamEmojis[allie.npcTeam]!=""], npcTeamNames[allie.npcTeam])

    rep = f"{var}__Aspiration :__ {inspi[allie.aspiration]}\n__Element :__ {elemEmojis[allie.element]} {elemNames[allie.element]} ({elemEmojis[allie.secElement]} {elemNames[allie.secElement]})\n{teamName}__Description :__\n{allie.description}"
    allMaxStats, accStats, dressStats, flatsStats, statsWeapon = allie.allStats(), allie.stuff[0].allStats(), allie.stuff[1].allStats(), allie.stuff[2].allStats(), allie.weapon.allStats()
    stats = ""
    for a in range(0, len(allMaxStats)):
        allyStat = int((allMaxStats[a]+accStats[a]+dressStats[a]+flatsStats[a]+statsWeapon[a]) * ((100+allie.limitBreaks[a])/100))
        stats += f"{statsEmojis[a]} __{nameStats[a]}.__ : {allyStat}\n"

    stats2 = ""
    accStats = [allie.stuff[0].resistance,allie.stuff[0].percing, allie.stuff[0].critical]
    dressStats = [allie.stuff[1].resistance,allie.stuff[1].percing, allie.stuff[1].critical]
    flatsStats = [allie.stuff[2].resistance,allie.stuff[2].percing, allie.stuff[2].critical]
    weaponStats = [allie.weapon.resistance,allie.weapon.percing, allie.weapon.critical]
    statsPlusName = nameStats2
    for num in range(3):
        summation = accStats[num] + dressStats[num] + flatsStats[num] + weaponStats[num]
        stats2 += f"{statsEmojis[num+RESISTANCE]} __{statsPlusName[num]}__ : {summation}\n"

    accStats = [allie.stuff[0].negativeHeal, allie.stuff[0].negativeBoost,allie.stuff[0].negativeShield, allie.stuff[0].negativeDirect, allie.stuff[0].negativeIndirect]
    dressStats = [allie.stuff[1].negativeHeal, allie.stuff[1].negativeBoost,allie.stuff[1].negativeShield, allie.stuff[1].negativeDirect, allie.stuff[1].negativeIndirect]
    flatsStats = [allie.stuff[2].negativeHeal, allie.stuff[2].negativeBoost,allie.stuff[2].negativeShield, allie.stuff[2].negativeDirect, allie.stuff[2].negativeIndirect]
    statsPlusName = ["Soins", "Bonus/Malus","Armure", "Dégâts directs", "Dégâts indirect"]
    stats2 += "\n"
    for num in range(5):
        summation = accStats[num]*-1 + dressStats[num]*-1 + flatsStats[num]*-1
        stats2 += f"{statsEmojis[num+ACT_HEAL_FULL]} __{statsPlusName[num]}__ : {summation}\n"


    rep += f"\n\n__**Arme et compétences** :__\n{allie.weapon.emoji} {allie.weapon.name}\n"
    for a in allie.skills:
        if type(a) == skill:
            rep += f"\n{a.emoji} {a.name}"

    rep += f"\n\n__**Equipement :**__\n__Accessoire__ : {allie.stuff[0].emoji} {allie.stuff[0].name}\n__Vêtements__ : {allie.stuff[1].emoji} {allie.stuff[1].name}\n__Chaussures__ : {allie.stuff[2].emoji} {allie.stuff[2].name}"

    emb = interactions.Embed(title="__Allié temporaire : "+allie.name+"__", color=allie.color, description= reduceEmojiNames(rep)+"\n<:em:866459463568850954>")
    emb.add_field(name="__**Statistiques au niveau {0} :**__".format(allie.level), value=reduceEmojiNames(stats),inline=True)
    emb.add_field(name="__**Statistiques secondaires :**__", value=reduceEmojiNames(stats2),inline=True)
    emb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.{1}".format(getEmojiObject([allie.icon,allie.splashIcon][allie.splashIcon != None]).id, ["png","gif"][allie.splashIcon != None and [allie.icon[1],allie.splashIcon[1]][allie.splashIcon != None] == "a"]))

    if allie.splashArt != None:
        emb.set_image(url=allie.splashArt)

    if allie.changeDict != None:
        for altBuild in allie.changeDict:
            fieldValue = ""
            if altBuild.aspiration != None:
                fieldValue += "{0}|".format(aspiEmoji[altBuild.aspiration])
            else:
                fieldValue += "{0}|".format(aspiEmoji[allie.aspiration])
            if altBuild.weapon != None:
                fieldValue += "{0}|".format(altBuild.weapon.emoji)
            else:
                fieldValue += "{0}|".format(allie.weapon.emoji)
            if altBuild.stuff != None:
                if altBuild.proba > 0:
                    stuffToSee = [getAutoStuff(altBuild.stuff[0], allie), getAutoStuff(altBuild.stuff[1], allie), getAutoStuff(altBuild.stuff[2], allie)]
                else:
                    stuffToSee = altBuild.stuff
            else:
                stuffToSee = allie.stuff
            for stuffy in stuffToSee:
                fieldValue += stuffy.emoji
            fieldValue += "|"
            if altBuild.skills != None:
                listActSkills = altBuild.skills
            else:
                listActSkills = allie.skills
            
            for skilly in listActSkills:
                if type(skilly) == skill:
                    fieldValue += skilly.emoji
     
            emb.add_field(name="<:em:866459463568850954>\n__Build alternatif ({0}%) :__".format(altBuild.proba), value=fieldValue, inline=False)

    if allie.elemAffinity:
        emb = infoEffect(elemResistanceEffects[allie.element],allie,emb)

    return emb

def infoEnnemi(ennemi: octarien):
    teamName = ""
    if ennemi.npcTeam != None:
        teamName = "__Affinité :__ {0}{1}\n".format(npcTeamEmojis[ennemi.npcTeam]+[""," "][npcTeamEmojis[ennemi.npcTeam]!=""], npcTeamNames[ennemi.npcTeam])
    rep = f"__Aspiration :__ {inspi[ennemi.aspiration]}\n__Niveau Minimum :__ {ennemi.baseLvl}\n__Element :__ {elemEmojis[ennemi.element]} {elemNames[ennemi.element]}\n{teamName}\n__Description :__\n{ennemi.description}\n\n__**Statistiques au niveau 50 :**__\n"
    allMaxStats, accStats, dressStats, flatsStats, weapStats = ennemi.allStats(), ennemi.stuff[0].allStats(), ennemi.stuff[1].allStats(), ennemi.stuff[2].allStats(), ennemi.weapon.allStats()
    for a in range(0, len(allMaxStats)):
        enStat = allMaxStats[a]+ accStats[a] + dressStats[a]+flatsStats[a]+weapStats[a]
        rep += f"\n{statsEmojis[a]} __{nameStats[a]}__ : {enStat}"

    rep += f"\n\n__**Arme et compétences** :__\n{ennemi.weapon.emoji} __{ennemi.weapon.name}__\n{ennemi.weapon.getSummary()}\n"
    for skilly in ennemi.skills:
        if type(skilly) == skill:
            rep += "{3}{0} __{1}__\n{2}\n".format(skilly.emoji,skilly.name,skilly.getSummary(),["\n",""][rep[-2:] == "\n\n"])

    emb = interactions.Embed(title="__Ennemi : "+ennemi.name +"__", color=ennemi.color, description=rep)
    emb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.{1}".format(getEmojiObject([ennemi.icon,ennemi.splashIcon][ennemi.splashIcon != None]).id,["png","gif"][ennemi.splashIcon != None and [ennemi.icon[1],ennemi.splashIcon[1]][ennemi.splashIcon != None] == "a"]))
    if ennemi.splashArt != None:
        emb.set_image(url=ennemi.splashArt)
    if ennemi.elemAffinity:
        emb = infoEffect(elemResistanceEffects[ennemi.element],ennemi,emb)

    return emb

def getAutoStuff(object: stuff, user: Union[char, tmpAllie], tablStats = None):
    if user.level//5 == object.minLvl//5 or (object.minLvl == MAXLEVEL//10*10 and user.level >= MAXLEVEL) and (type(user) == char and user.have(object)):
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
            tablToSee = user.stuffInventory[:]
        elif type(user) == tmpAllie:
            tablToSee = stuffs[:]

        def getSortValue(obj: stuff, statsMaxPlace: list[int]=statsMaxPlace, aff=False):
            objStats: list[int] = obj.allStats()+[obj.resistance, obj.percing, obj.critical]+[obj.negativeHeal*-1, obj.negativeBoost*-1, obj.negativeShield*-1, obj.negativeDirect*-1, obj.negativeIndirect*-1]
            value: list[int] = []
            for a in statsMaxPlace:
                value.append(objStats[a])

            for cmpt in range(len(statsMaxPlace)):
                if cmpt < 3:
                    value[cmpt] = value[cmpt] * [1,0.5,0.25][cmpt]

            if aff:
                print(obj.name, temp)
            return sum(value)

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

async def downloadElementIcon(bot: interactions.Client):
    listEmojiHead = elemEmojis+secElemEmojis
    listDir = os.listdir("./data/images/elemIcon/")
    for b in range(len(listEmojiHead)):
        emojiObject, finded = getEmojiObject(listEmojiHead[b]), False
        if emojiObject.name + ".png" not in listDir:
            for c in [615257372218097691,932941135276560455, 862320563590529056]:
                guild = bot.get_guild(c)
                emojiList = await guild.fetch_all_custom_emojis()
                for emoji_2 in emojiList:
                    if emoji_2.id == emojiObject.id:
                        image = requests.get("https://cdn.discordapp.com/emojis/{0}.webp".format(emoji_2.id), stream=True)
                        image.raw.decode_content = True
                        open(f"./data/images/elemIcon/{emojiObject.name}.png", "wb").write(image.content)
                        image = PIL.Image.open(f"./data/images/elemIcon/{emojiObject.name}.png")
                        image = image.resize((60, 60))
                        image.save(f"./data/images/elemIcon/{emojiObject.name}.png")
                        print(emojiObject.name + " downlowded")
                        finded=True
                        listDir = os.listdir("./data/images/elemIcon/")
                        break

            if not(finded):
                print(emojiObject.name + " not found")

async def getRandomStatsEmbed(bot: interactions.Client, team: List[classes.char], text="Chargement...", fullStats=False, fullTips=False) -> interactions.Embed:
    if (fullStats or (random.randint(0, 99) < 50)) and not(fullTips) :
        title, desc = "<:alice:908902054959939664> :", "\""
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
                print_exc()
                desc += "placeholder.error.unknow"

            biggest = random.randint(0, 4)
            if biggest < 2:
                if rdm2 == "max":
                    try:
                        records = aliceStatsDb.getRecord(
                            "max{0}".format(randomStat))
                        if int(records["owner"]) == int(choisen["char"].owner):
                            desc += "\n\nC'est d'ailleurs le record tiens"
                        else:
                            try:
                                recorder = loadCharFile(
                                    absPath + "/userProfile/" + str(records["owner"]) + ".json")
                                desc += "\n\n"+randomRecordMsg[random.randint(0, len(randomRecordMsg)-1)].format(icon=await getUserIcon(bot, recorder), value=separeUnit(int(records["value"])), name=recorder.name, il=["il", "elle"][recorder.gender == GENDER_FEMALE], e=["", "e"][recorder.gender == GENDER_FEMALE])
                            except:
                                desc += "\n\nJ'ai pas pu trouver qui avait le record, par contre"
                    except:
                        pass
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
        emb = interactions.Embed(title="__{0}__".format(text), color=aliceColor)
        emb.add_field(name=title,value = desc+"\"")
        return emb
    
    else:
        emb = interactions.Embed(title="__{0}__".format(text), color=light_blue)
        emb.add_field(name="<:lena:909047343876288552> :",value="\""+lenaTipsMsgTabl[random.randint(0, len(lenaTipsMsgTabl)-1)]+"\"")
        return emb

async def getFullTeamEmbed(bot: interactions.Client, team: List[char], mainUser: char, see = 0) -> interactions.Embed:
    toReturn = Embed("__Equipe de {0}__".format(mainUser.name),color=mainUser.color)
    for ent in team:
        entDesc = ""
        tablToSee = [ent.skills,[ent.weapon]+ent.stuff]
        if see < 2:
            for obj in tablToSee[see]:
                if type(obj) in [classes.weapon, classes.stuff, classes.skill]:
                    entDesc += "{0} {1}\n".format(obj.emoji,obj.name)
                    if type(obj) == classes.weapon:
                        entDesc += "\n"

        else:
            sumStatsBonus = [ent.majorPoints[0], ent.majorPoints[1], ent.majorPoints[2], ent.majorPoints[3], ent.majorPoints[4], ent.majorPoints[5], ent.majorPoints[6], ent.majorPoints[7], ent.majorPoints[8], ent.majorPoints[9], ent.majorPoints[10], ent.majorPoints[11], ent.majorPoints[12], ent.majorPoints[13], ent.majorPoints[14]]

            for a in [ent.weapon]+ent.stuff:
                sumStatsBonus[0] += a.strength
                sumStatsBonus[1] += a.endurance
                sumStatsBonus[2] += a.charisma
                sumStatsBonus[3] += a.agility
                sumStatsBonus[4] += a.precision
                sumStatsBonus[5] += a.intelligence
                sumStatsBonus[6] += a.magie
                sumStatsBonus[7] += a.resistance
                sumStatsBonus[8] += a.percing
                sumStatsBonus[9] += a.critical
                sumStatsBonus[10] += a.negativeHeal * -1
                sumStatsBonus[11] += a.negativeBoost * -1
                sumStatsBonus[12] += a.negativeShield * -1
                sumStatsBonus[13] += a.negativeDirect * -1
                sumStatsBonus[14] += a.negativeIndirect * -1

            estimPV = separeUnit(round((130+ent.level*15)*(int((ent.endurance+sumStatsBonus[ENDURANCE]*(1+ent.limitBreaks[ENDURANCE]/100)))/100+1)))
            entDesc = "\n__PVs :__ {0}".format(estimPV)
            allStatsUser = ent.allStats()+[ent.resistance,ent.percing,ent.critical,ent.majorPoints[ACT_BOOST_FULL],ent.majorPoints[ACT_HEAL_FULL],ent.majorPoints[ACT_SHIELD_FULL],ent.majorPoints[ACT_DIRECT_FULL],ent.majorPoints[ACT_INDIRECT_FULL]]
            for cmpt in range(0,MAGIE+1):
                userStats = int((allStatsUser[cmpt]+sumStatsBonus[cmpt]) * (1+ent.limitBreaks[cmpt]/100))
                entDesc += "\n{0} __{1}__ : {2}".format(statsEmojis[cmpt],allStatsNames[cmpt],userStats)

        entDesc = reduceEmojiNames(entDesc)
        toReturn.add_field("{0} __{1} :__\n".format(await getUserIcon(bot,ent),ent.name),inline=True,value=entDesc)
    return toReturn

async def updateHaveProcurOn():
    dictHaveProcur, listUserId = [], []
    for temp in os.listdir("./userProfile/"):
        listUserId.append(int(temp.replace(".json","")))

    for temp in listUserId:
        dictHaveProcur.append((temp,[]))

    dictHaveProcur = dict(dictHaveProcur)

    for temp in listUserId:
        user = loadCharFile("./userProfile/"+str(temp)+".json")
        for procur in user.procuration:
            if int(procur) != user.owner:
                dictHaveProcur[int(procur)].append(user.owner)
    
    for userId in dictHaveProcur:
        if dictHaveProcur[userId] != []:
            user = loadCharFile("./userProfile/"+str(userId)+".json")
            user.haveProcurOn = dictHaveProcur[userId]
            saveCharFile(user=user)
            print("Les procurations de {0} ont bien été mise à jour".format(user.name))

def newTeam(user):
    rdm, teamIds = str(random.randint(1, 999999999)), userTeamDb.getAllTeamIds()
    while rdm in teamIds:
        rdm = str(random.randint(1, 999999999))
    userTeamDb.updateTeam(rdm, [user])
    user.team = rdm
    saveCharFile(user=user)
    return user

catSelect = interactions.ActionRow(interactions.StringSelectMenu([StringSelectOption(label="Players",value="0",description="Show players"),StringSelectOption(label="Allies",value="1",description="Show allies"),StringSelectOption(label="Ennemis",value="2",description="Show ennemis"),StringSelectOption(label="Small Bosses",value="3",description="Show small bosses"),StringSelectOption(label="Stands Alones",value="4",description="Show stands alones bosses"),StringSelectOption(label="Raids",value="5",description="Show raids bosses")],custom_id="catSelect",placeholder="Sort by entity category"))
async def kikimerFunction(bot:interactions.Client,ctx:interactions.SlashContext,period:bool=False):
    destination, msg, sortValue, page = 0, None, 0, 0
    await ctx.defer()
    while 1:
        tablResultDict = []
        try:
            if destination == 0: # Players
                tempTablResultDict = []
                cursory = aliceStatsDb.con.cursor()
                if not(period):
                    cursory.execute("SELECT * FROM userStats")
                else:
                    cursory.execute("SELECT * FROM lastMouthUsers")
                tempTablResultDict = cursory.fetchall()
                cursory.close()

                for cmpt in range(len(tempTablResultDict)):
                    try:
                        if os.path.exists("./userProfile/{0}.json".format(tempTablResultDict[cmpt]["id"])):
                            tempUser = loadCharFile(path="./userProfile/{0}.json".format(tempTablResultDict[cmpt]["id"]))
                            if tempUser != None:
                                tablResultDict.append([tempUser,tempTablResultDict[cmpt]])
                    except:
                        pass
            else:
                tempTablResultDict = []
                cursory = aliceStatsDb.con.cursor()
                if not(period):
                    cursory.execute("SELECT * FROM enemyStats")
                else:
                    cursory.execute("SELECT * FROM lastMouthEnemy")
                tempTablResultDict = cursory.fetchall()
                cursory.close()

                for cmpt in range(len(tempTablResultDict)):
                    try:
                        if destination == 1:
                            tempEnt = findAllie(tempTablResultDict[cmpt]["name"])
                            if tempEnt != None:
                                tablResultDict.append([tempEnt,tempTablResultDict[cmpt]])
                        else:
                            tempEnt = findEnnemi(tempTablResultDict[cmpt]["name"])
                            if tempEnt != None:
                                if destination == 2:
                                    for ent in tablUniqueEnnemies:
                                        if tempEnt.name == ent.name:
                                            tablResultDict.append([tempEnt,tempTablResultDict[cmpt]])
                                            break
                                elif destination == 3:
                                    for ent in tablBoss:
                                        if tempEnt.name == ent.name and not(ent.standAlone):
                                            tablResultDict.append([tempEnt,tempTablResultDict[cmpt]])
                                            break
                                elif destination == 4:
                                    for ent in tablBoss:
                                        if tempEnt.name == ent.name and ent.standAlone:
                                            tablResultDict.append([tempEnt,tempTablResultDict[cmpt]])
                                            break
                                if destination == 5:
                                    for ent in tablRaidBoss:
                                        if tempEnt.name == ent.name:
                                            tablResultDict.append([tempEnt,tempTablResultDict[cmpt]])
                                            break
                        
                    except:
                        pass
        except:
            print_exc()

        if len(tablResultDict) == 0:
            if msg == None:
                msg = await ctx.send(embeds=interactions.Embed(title="============== Kikimeter ==============",description="No result found"),components=[catSelect])
            else:
                await msg.edit(embeds=interactions.Embed(title="============== Kikimeter ==============",description="No result found"),components=[catSelect])

            try:
                respond: interactions.ComponentContext = await bot.wait_for_component(messages=msg,components=[catSelect,sortSelect,buttonsActRow],timeout=60)
            except asyncio.TimeoutError:
                await msg.edit(embeds=interactions.Embed(title="============== Kikimeter ==============",description="No result found"),components=[])
                return 0

            if respond.custom_id == catSelect.components[0].custom_id:
                destination, sortValue, page = int(respond.values[0]), 0, 0
        else:
            selectSortOptions, cmpt, itemList = [], 0, tablResultDict[0][1].keys()
            itemList = itemList[1:]

            for ballerine in itemList:
                selectSortOptions.append(interactions.StringSelectOption(label=ballerine,value=str(cmpt)))
                cmpt += 1
            sortSelect = interactions.ActionRow(interactions.StringSelectMenu(selectSortOptions,custom_id='selectMenu',placeholder="Sort by stat category"))
            tablResultDict.sort(key=lambda ballerine: ballerine[1][itemList[sortValue]],reverse=True)
            description = ""
            for cmpt in range(10*page,min((page+1)*10,len(tablResultDict))):
                if type(tablResultDict[cmpt][0]) == char:
                    icon = await getUserIcon(bot,tablResultDict[cmpt][0])
                else:
                    icon = [tablResultDict[cmpt][0].splashIcon,tablResultDict[cmpt][0].icon][tablResultDict[cmpt][0].splashIcon == None]
                
                description += "\n{0}. {1} {4}        [{2}] : {3}".format(cmpt,icon,itemList[sortValue],tablResultDict[cmpt][1][itemList[sortValue]],tablResultDict[cmpt][0].name)

            buttonsActRow = interactions.ActionRow(interactions.Button(style=ButtonStyle.SECONDARY,custom_id="previous",label="Previous",emoji=PartialEmoji(name="◀️"),disabled=page<=0),interactions.Button(style=ButtonStyle.SECONDARY,custom_id="next",label="Next",emoji=PartialEmoji(name="▶️"),disabled=(page+1)*10>len(tablResultDict)-1))

            if msg == None:
                msg = await ctx.send(embeds=interactions.Embed(title="============== Kikimeter ==============",description=reduceEmojiNames(description)),components=[catSelect,sortSelect,buttonsActRow])
            else:
                await msg.edit(embeds=interactions.Embed(title="============== Kikimeter ==============",description=reduceEmojiNames(description)),components=[catSelect,sortSelect,buttonsActRow])

            try:
                respond: interactions.ComponentContext = await bot.wait_for_component(messages=msg,components=[catSelect,sortSelect,buttonsActRow],timeout=60)
                respond: interactions.ComponentContext = respond.ctx
            except asyncio.TimeoutError:
                await msg.edit(embeds=interactions.Embed(title="============== Kikimeter ==============",description=reduceEmojiNames(description)),components=[])
                return 0

            if respond.custom_id == catSelect.components[0].custom_id:
                destination, sortValue, page = int(respond.values[0]), 0, 0
            elif respond.custom_id == sortSelect.components[0].custom_id:
                sortValue, page = int(respond.values[0]), 0
            elif respond.custom_id == buttonsActRow.components[0].custom_id:
                page -= 1
            elif respond.custom_id == buttonsActRow.components[1].custom_id:
                page += 1

async def createOsaSmnEmojis(bot:interactions.Client):
    osaSmnDict, cmpt2 = getOsamodasJson(), 0
    emojiGuild:interactions.Guild = bot.get_guild(1171852774217093120)
    emojiList = await emojiGuild.fetch_all_custom_emojis()
    for smnDict in osaSmnDict[:]:
        try:
            smnDict["emojiStr"]
        except KeyError:
            imageUrl = smnDict["imageUrl"]
            if ".w133h.png" not in imageUrl:
                imageUrl = imageUrl.replace(".png",".w133h.png")
            image = requests.get(imageUrl, stream=True)
            image.raw.decode_content = True
            open("./data/images/temp.png", "wb").write(image.content)
            image = PIL.Image.open("./data/images/temp.png")
            image = image.resize((128, 128))
            image.save("./data/images/temp.png")
            newEmoji = await emojiGuild.create_custom_emoji(name="osaSmn{0}".format(cmpt2),imagefile="./data/images/temp.png")
            print("{0}'s emoji uploaded".format(smnDict["name"]))

            for cmpt in range(len(osaSmnDict)):
                if osaSmnDict[cmpt]["name"]==smnDict["name"]:
                    osaSmnDict[cmpt]["emojiStr"] = "<:{0}:{1}>".format(newEmoji.name,newEmoji.id)
            cmpt2 += 1
        except:
            print_exc()
            print("{0} as encounter a error".format(smnDict["name"]))
        await asyncio.sleep(0.15)

    jsonFile = open("./data/database/osamodas.json","w")
    json.dump({"smnList":osaSmnDict},jsonFile)
    jsonFile.close()

def openBooster(user:char, boosters = [], infield = True):
    drawnedChip = {}
    for boosterType in boosters:
        probaRarity, chipsPulls = probaRarityTabl[boosterType], 0

        if boosterType == RARITY_MYTHICAL:
            for cmpt in range(3):
                listChipPull = chipMythic[:]
                pulledChip =  listChipPull[random.randint(0,len(listChipPull)-1)]
                try:
                    drawnedChip[pulledChip.id][1] += 1
                except KeyError:
                    drawnedChip[pulledChip.id] = [pulledChip,1]
                chipsPulls+=1

        for cmpt in range(10-chipsPulls):
            randRoll, rarity = random.randint(0,999), RARITY_MYTHICAL
            for rar in range(4):
                if randRoll < probaRarity[rar]:
                    rarity = rar
                    break
                else:
                    randRoll -= probaRarity[rar]

            listChipPull = [chipCommun,chipRare,chipLegend,chipMythic][rarity][:]
            pulledChip =  listChipPull[random.randint(0,len(listChipPull)-1)]

            nbDrawnedChips, neededChips = 1, nbChipsForLvlUp[user.chipInventory[pulledChip.id].lvl-rarityMinLvl[pulledChip.rarity]]
            if neededChips > 20:
                tmp = int(neededChips*0.05)
                nbDrawnedChips += random.randint(0,max(tmp,1))

            try:
                drawnedChip[pulledChip.id][1] += nbDrawnedChips
            except KeyError:
                drawnedChip[pulledChip.id] = [user.chipInventory[pulledChip.id],nbDrawnedChips]

        drawnedChip = {k: v for k, v in sorted(drawnedChip.items(), key=lambda item: item[1][0].rarity)}
        user.tc += 10

    toReturn = ""
    for pulledChipId in drawnedChip:
        temp, user = user.chipInventory[pulledChipId].addProgress(value=drawnedChip[pulledChipId][1],user=user)
        toReturn += "{4} {0}*{1}* x**{2}** *{3}*\n".format(
            user.chipInventory[pulledChipId].emoji+[""," "][user.chipInventory[pulledChipId].emoji != ""],
            user.chipInventory[pulledChipId].name,
            drawnedChip[pulledChipId][1],
            ["({0}/{1})".format(user.chipInventory[pulledChipId].progress,nbChipsForLvlUp[user.chipInventory[pulledChipId].lvl-rarityMinLvl[user.chipInventory[pulledChipId].rarity]]),"(↑ Lv. {0})".format(user.chipInventory[pulledChipId].lvl)][temp],
            rarityEmojis[user.chipInventory[pulledChipId].rarity])

    toReturn, charLimit = reduceEmojiNames(toReturn), [EMBED_MAX_DESC_LENGTH,EMBED_FIELD_VALUE_LENGTH][infield]
    if len(toReturn) > charLimit:
        tablToRemove, tablToRemplace = ("<:co:1217187986085646427>","<:ra:1217188006679810058>","<:le:1217344108599967764>","<:my:1217569212642365520>"), ("C","R","L","M")
        for cmpt, toReplace in enumerate(tablToRemplace):
            toReturn = toReturn.replace(tablToRemove[cmpt],toReplace)
        if len(toReturn) > charLimit:
            tablToRemove = []
            for chipid in drawnedChip:
                if drawnedChip[chipid][0].emoji != "":
                    tablToRemove.append(reduceEmojiNames(drawnedChip[chipid][0].emoji))
            for toReplace in tablToRemove:
                toReturn = toReturn.replace(toReplace,"")
        if len(toReturn) > charLimit:
            toReturn, nbRarity = "Overload <:iliSip:1119011945157230692>\n", [0,0,0,0]
            for chipid in drawnedChip:
                nbRarity[drawnedChip[chipid][0].rarity]+=drawnedChip[chipid][1]
            for indx, nbCards in enumerate(nbRarity):
                toReturn += "{0} x{1}, ".format(rarityEmojis[indx],nbCards)
            toReturn = reduceEmojiNames(toReturn)[:-2]

    return user, toReturn
