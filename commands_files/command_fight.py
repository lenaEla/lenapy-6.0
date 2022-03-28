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
        dmg = max(1,round(basePower * (max(-65,caster.allStats()[use]+100-caster.actionStats()[actionStat]))/100 * (1-(min(95,target.resistance*(1-(caster.percing+skillPercing)/100))/100))*(danger/100)*caster.getElementalBonus(target=target,area=area,type=typeDmg)*(1+(0.01*caster.level))))
        return dmg
    else:
        return basePower

async def fight(bot : discord.Client , team1 : list, team2 : list ,ctx : SlashContext, auto:bool = True,contexte:list=[],octogone:bool=False,bigMap:bool=False, procurFight = False, msg=None): 
    try:
        """
            Base command for the fights\n
            \n
            Parameters :
            bot : the bot's discord client
            team1 : A list of Char objects
            team2 : A list of Char objects. Unlike team1, can be empty
            ctx : The context of the command, for know where to send the messages
            auto : Does the fight is a quick fight or a normal one ? Default ``True``
            contexte : A list of some parameters for the fight. Default ``[]``
                . exemple :
                    [TEAM1,<effect>] -> Give to the blue team the <effect> at the start of the fight
            octogone : If at ``False``, enable the loots and exp gains of the fight and lock the Fighting status of the team. Default ``False``
            slash : Does the command is slashed ? Default ``False``
        """
        if procurFight:
            user = loadCharFile("./userProfile/{0}.prof".format(ctx.author_id))
            team1[0].owner = user.owner
            team1[0].team = user.team

        mainUser = None
        for user in team1:
            if int(user.owner) == int(ctx.author_id):
                mainUser = user

        if mainUser == None:
            mainUser = team1[0]

        listImplicadTeams, listFasTeam = [mainUser.team], [[],[]]
        playOfTheGame = [1,None,None]

        tablIsPnjName = []
        for a in tablAllAllies + tablVarAllies:
            tablIsPnjName.append(a.name)

        for a in ["Liu","Lia","Liz","Lio","Ailill","Kiku"]:
            tablIsPnjName.append(a)

        temp = []
        for a in tablIsPnjName:
            temp.append((a,False))

        dictIsPnjVar = dict(temp)               # A dict who keep the bool for the presence of a Temp

        aliceMemCastTabl = [False,False]        # Does a team is casting Memento Angel's path 
        # Will Alice say it ? She never did
        now = datetime.now()
        logs,haveError = "[{0}]\n".format(now.strftime("%H:%M:%S, %d/%m/%Y")),False

        print(ctx.author.name + " a lancé un combat")
        cmpt,tablAllCells,tour,danger,dangerThub,tablAliveInvoc,longTurn,longTurnNumber,haveMultipleHealers = 0,[],0,100,None,[0,0],False,[], [False,False]
        dangerLevel, errorNb = [65,70,75,80,85,90,100,110,120,135,150], 0

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
            def __init__(self,x : int, y : int, id : int):
                self.x = x
                self.y = y
                self.id = id
                self.on: Union[None,entity] = None

            def distance(self,cell):
                """Return the distance with the other cell"""
                return int(abs(self.x - cell.x)+abs(self.y - cell.y))

            def getArea(self,area=AREA_MONO,team=0) -> list:
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
                    return tablAllCells
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
                elif area in [AREA_RANDOMENNEMI_1,AREA_RANDOMENNEMI_2,AREA_RANDOMENNEMI_3,AREA_RANDOMENNEMI_4,AREA_RANDOMENNEMI_5]:
                    for cell in tablAllCells:
                        if cell.on != None and cell.on.team != team:
                            rep.append(cell)
                    random.shuffle(rep)
                    return rep[0:min(area-AREA_RANDOMENNEMI_1+1,len(rep))]
                elif area in [AREA_INLINE_2,AREA_INLINE_3,AREA_INLINE_4,AREA_INLINE_5]:
                    for celly in tablAllCells:
                        if (celly.x == self.x or celly.y == self.y) and self.distance(celly) <= area + 2 - AREA_INLINE_2:
                            rep.append(celly)
                return rep

            def getEntityOnArea(self,area=AREA_MONO,team=0,wanted=ALLIES,lineOfSight=False,lifeUnderPurcentage=100,dead=False,effect=[None],ignoreInvoc = False, directTarget=True,ignoreAspiration = None) -> list: 
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

                tablArea = self.getArea(area=area,team=team)
                enties = []

                for cellule in tablArea:
                    if cellule.on != None:                                                          # If there is a entity on the cell
                        ent = cellule.on
                        if directTarget:                                                                # If we are looking for a directTarget, take into account if the entity is untargetable
                            targetable = not(ent.untargetable)
                        else:
                            targetable = True

                        if ent.hp > 0 and not(dead):
                            if ent.team == team and wanted == ALLIES and targetable:
                                enties += [ent]
                            elif ent.team != team and wanted == ENNEMIS and targetable:
                                enties += [ent]
                            elif wanted == ALL and targetable:
                                enties += [ent]
                        elif ent.status == STATUS_DEAD and dead:
                            if ent.team == team and wanted == ALLIES and targetable:
                                enties += [ent]
                            elif ent.team != team and wanted == ENNEMIS and targetable:
                                enties += [ent]
                            elif wanted == ALL:
                                enties += [ent]

                rep = enties

                if lineOfSight and wanted==ENNEMIS and (area not in [AREA_ALL_ENEMIES,AREA_ALL_ENTITES]):
                    for a in enties:
                        if not(a.translucide):
                            # Définition de la direction
                            direction, diffX, diffY = None,self.x - a.cell.x,self.y - a.cell.y

                            if diffX < 0:
                                if abs(diffY/3) < abs(diffX):
                                    direction = '➡️'
                                elif diffY > 0:
                                    direction = '↘️'
                                elif diffY < 0:
                                    direction = '↗️'
                            elif diffX > 0:
                                if abs(diffY/3) < abs(diffX):
                                    direction = '⬅️'
                                elif diffY > 0:
                                    direction = '↙️'
                                elif diffY < 0:
                                    direction = '↖️'
                            elif diffY > 0 and abs(diffX/3) < abs(diffY):
                                direction = '⬆️'
                            elif diffY < 0 and abs(diffX/3) < abs(diffY):
                                direction = '⬇️'

                            if direction == '➡️':
                                cmpt,temp,ite,yOr = a.cell.x+1,[0],0,a.cell.y
                                while cmpt < 6:
                                    for b in temp:
                                        try:
                                            tablArea.remove(findCell(cmpt,yOr+b))
                                        except:
                                            pass

                                    cmpt += 1
                                    ite += 1
                                    temp += [ite,-ite]
                            elif direction == '⬅️':
                                cmpt,temp,ite,yOr = a.cell.x-1,[0],0,a.cell.y
                                while cmpt > 0:
                                    for b in temp:
                                        try:
                                            tablArea.remove(findCell(cmpt,yOr+b))
                                        except:
                                            pass

                                    cmpt -= 1
                                    ite += 1
                                    temp += [ite,-ite]
                            elif direction == '↘️':
                                cmpt,temp,ite,yOr = a.cell.x+1,[0],0,a.cell.y+1
                                while cmpt < 6:
                                    for b in temp:
                                        try:
                                            tablArea.remove(findCell(cmpt,yOr+b))
                                        except:
                                            pass

                                    cmpt += 1
                                    yOr += 1
                                    ite += 1
                                    temp += [ite,-ite]
                            elif direction == '↗️':
                                cmpt,temp,ite,yOr = a.cell.x+1,[0],0,a.cell.y-1
                                while cmpt < 6:
                                    for b in temp:
                                        try:
                                            tablArea.remove(findCell(cmpt,yOr+b))
                                        except:
                                            pass

                                    cmpt += 1
                                    yOr -= 1
                                    ite += 1
                                    temp += [ite,-ite]
                            elif direction == '↖️':
                                cmpt,temp,ite,yOr = a.cell.x-1,[0],0,a.cell.y-1
                                while cmpt > 0:
                                    for b in temp:
                                        try:
                                            tablArea.remove(findCell(cmpt,yOr+b))
                                        except:
                                            pass

                                    cmpt -= 1
                                    yOr -= 1
                                    ite += 1
                                    temp += [ite,-ite]
                            elif direction == '↙️':
                                cmpt,temp,ite,yOr = a.cell.x-1,[0],0,a.cell.y+1
                                while cmpt > 0:
                                    for b in temp:
                                        try:
                                            tablArea.remove(findCell(cmpt,yOr+b))
                                        except:
                                            pass

                                    cmpt -= 1
                                    yOr += 1
                                    ite += 1
                                    temp += [ite,-ite]
                            elif direction == '⬆️':
                                yOr,temp,ite,cmpt = a.cell.x,[0],0,a.cell.y-1
                                while cmpt > 0:
                                    for b in temp:
                                        try:
                                            tablArea.remove(findCell(cmpt,yOr+b))
                                        except:
                                            pass

                                    cmpt -= 1
                                    ite += 1
                                    temp += [ite,-ite]
                            elif direction == '⬇️':
                                yOr,temp,ite,cmpt = a.cell.x,[0],0,a.cell.y+1
                                while cmpt < 5:
                                    for b in temp:
                                        try:
                                            tablArea.remove(findCell(cmpt,yOr+b))
                                        except:
                                            pass

                                    cmpt += 1
                                    ite += 1
                                    temp += [ite,-ite]

                    enties = []
                    for a in tablArea:
                        if a.on != None:
                            if a.on.hp > 0 and not(dead):
                                targetable = True
                                if directTarget:
                                    targetable = not(a.on.untargetable)
                                if a.on.team == team and wanted == ALLIES and targetable:
                                    enties += [a.on]
                                elif a.on.team != team and wanted == ENNEMIS and targetable:
                                    enties += [a.on]
                                elif wanted == ALL:
                                    enties += [a.on]
                            elif a.on.hp <= 0 and dead:
                                if a.on.team == team and wanted == ALLIES and targetable:
                                    enties += [a.on]
                                elif a.on.team != team and wanted == ENNEMIS and targetable:
                                    enties += [a.on]
                                elif wanted == ALL:
                                    enties += [a.on]
                    rep = enties

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
                                        if d.effect.id == actEff.id or (d.effect.id == aeff.id and not(d.effect.stackable)):
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
                return [findCell(self.x-1,self.y),findCell(self.x+1,self.y),findCell(self.x,self.y-1),findCell(self.x,self.y+1)]

        for a in [0,1,2,3,4,5]:             # Creating the board
            for b in [[0,1,2,3,4],[0,1,2,3,4,5,6]][bigMap]:
                tablAllCells += [cell(a,b,cmpt)]
                cmpt += 1

        def findCell(x : int, y : int) -> cell:
            """Return the cell in X:Y, if it exist"""
            cmpt, maxCellNum = 0, len(tablAllCells)
            while cmpt < maxCellNum:
                if tablAllCells[cmpt].x == x and tablAllCells[cmpt].y == y:
                    return tablAllCells[cmpt]
                cmpt += 1

        allEffectInFight = []
        addEffect,tablEntTeam = [],[]

        class entity:
            """Base class for the entities"""
            def __init__(self,identifiant : int, perso : Union[char,tmpAllie,octarien], team : int, player=True, auto=True, danger=100,summoner=None,dictInteraction:dict=None):
                """
                    Parameters :\n
                    .identifiant : A unique identifiant for a entity. Between ``0`` and ``15``
                        -> A summon share the same id than his summoner
                    .perso : A ``Char, TmpAllie`` or ``octarien`` object. The entity is generated from this parameter
                    .team : The team of the entity. ``0`` for the Blue Team, ``1`` for the Red Team
                    .player : Does the entity is a player ? Default ``True`` (Where this is use ?)
                    .auto : Does the entity is a manual or a automatic player ? Default ``True`` (Automatic)
                    .danger : A ``int`` use for uping the entity hp if it's a ``octarien``. Default ``100``
                    .summoner : The summoner of the entity. ``None`` if the entity isn't a summon, and by default
                """
                self.id = identifiant
                self.char = perso
                self.team = team
                self.type = player
                self.auto = auto
                self.weapon = self.char.weapon
                if not(self.char.isNpc("Kiku")):
                    self.status = STATUS_ALIVE
                else:
                    self.status = STATUS_RESURECTED

                if type(perso) != invoc:
                    self.icon = perso.icon
                else:
                    self.icon = perso.icon[team]

                self.stun = False
                self.summoner = summoner
                if not(self.char.isNpc("Kiku")):
                    self.raiser = None
                else:
                    self.raiser = self.icon
                self.specialVars = {"osPro":False,"osPre":False,"osIdo":False,"ohAlt":False,"ohPro":False,"ohIdo":False,"heritEstial":False,"heritLesath":False,"haveTrans":False,"tankTheFloor":False,"clemBloodJauge":None,"clemMemCast":False,"aspiSlot":None,"damageSlot":None,"summonerMalus":False,"finalTech":False,"foullee":False,"partner":None,"preci":False,"ironHealth":False,"fascination":None}

                if self.char.aspiration in [OBSERVATEUR, POIDS_PLUME]:
                    self.specialVars["aspiSlot"] = 0
                if type(perso) not in [invoc,octarien]:
                    baseHP,HPparLevel = 130,15
                elif type(perso) == invoc:
                    baseHP, HPparLevel, perso.level = 70, 8, summoner.char.level
                elif not(perso.oneVAll):
                    baseHP,HPparLevel = 90,10
                else:
                    baseHP,HPparLevel = 500,115

                self.effect: List[fightEffect] = []
                self.ownEffect =  []
                self.cell = None

                self.leftTurnAlive = 999
                if type(self.char) == invoc:
                    self.leftTurnAlive = 3

                self.strength,self.endurance,self.persoisma,self.agility,self.precision,self.intelligence,self.magie = 0,0,0,0,0,0,0
                self.resistance,self.percing,self.critical = 0,0,0
                self.negativeHeal, self.negativeBoost, self.negativeShield, self.negativeDirect, self.negativeIndirect = 0,0,0,0,0
                self.ressurectable = False
                self.cooldowns = [0,0,0,0,0,0,0]

                for a in [0,1,2,3,4,5,6]:
                    if type(self.char.skills[a]) == skill:
                        if self.char.skills[a].id == trans.id and self.char.skills[a].name == trans.name:
                            self.char.skills[a] = transTabl[self.char.aspiration]
                            self.specialVars["haveTrans"] = True

                        elif self.char.skills[a].id == mageUlt.id:
                            if self.char.element in [ELEMENT_FIRE,ELEMENT_AIR,ELEMENT_SPACE]:
                                temp = mageUltZone
                            elif self.char.element in [ELEMENT_WATER,ELEMENT_EARTH,ELEMENT_TIME]:
                                temp = mageUltMono
                            else:
                                temp = mageUlt

                            self.char.skills[a] = temp

                        elif self.char.skills[a].id == finalTech.id:
                            self.specialVars["finalTech"] = True
                        self.cooldowns[a] = int(self.char.skills[a].ultimate)*2+self.char.skills[a].initCooldown

                self.stats = statTabl()
                self.medals = [0,0,0]
                self.healResist = 0
                self.missedLastTurn = False
                self.translucide = False
                self.untargetable = False
                self.invisible = False
                self.immune = False
                self.name = self.char.name
                self.aspiration = self.char.aspiration
                self.level = self.char.level

                self.dmgUp, self.critDmgUp, self.healUp, self.critHealUp = 0,0,0,0

                finded = False
                self.IA = AI_AVENTURE

                if self.char.aspiration in [BERSERK,OBSERVATEUR,POIDS_PLUME,TETE_BRULE,]:
                    self.IA = AI_DPT

                elif self.char.aspiration in [IDOLE,INOVATEUR]:
                    self.IA = AI_BOOST

                elif self.char.aspiration in [ALTRUISTE,VIGILANT]:
                    self.IA = AI_ALTRUISTE

                elif self.char.aspiration in [MAGE,SORCELER]:
                    self.IA = AI_MAGE
                
                elif self.char.aspiration == ENCHANTEUR:
                    self.IA = AI_ENCHANT

                elif self.char.aspiration in [PREVOYANT,PROTECTEUR]:
                    self.IA = AI_SHIELD

                elif self.IA == AI_AVENTURE:
                    offSkill,SuppSkill,healSkill,armorSkill,invocSkill = 0,0,0,0,0
                    for b in [self.char.weapon]+self.char.skills:
                        if type(b) in [weapon,skill]:
                            if b.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]:
                                offSkill += 1
                            elif b.type in [TYPE_BOOST,TYPE_MALUS,TYPE_ARMOR]:
                                SuppSkill += 1
                            elif b.type in [TYPE_HEAL]:
                                healSkill += 1
                            elif b.type in [TYPE_SUMMON]:
                                invocSkill += 1
                        
                    if max(offSkill,SuppSkill,healSkill,armorSkill,invocSkill) == offSkill:
                        self.IA = AI_OFFERUDIT
                    elif max(offSkill,SuppSkill,healSkill,armorSkill,invocSkill) == SuppSkill:
                        self.IA = AI_BOOST
                    elif max(offSkill,SuppSkill,healSkill,armorSkill,invocSkill) == healSkill:
                        self.IA = AI_ALTRUISTE
                    elif max(offSkill,SuppSkill,healSkill,armorSkill,invocSkill) == armorSkill:
                        self.IA = AI_BOOST
                    elif max(offSkill,SuppSkill,healSkill,armorSkill,invocSkill) == invocSkill:
                        self.IA = AI_AVENTURE

                if type(self.char) != invoc:
                    baseStats = {STRENGTH:self.char.strength+self.char.majorPoints[0],ENDURANCE:self.char.endurance+self.char.majorPoints[1],CHARISMA:self.char.charisma+self.char.majorPoints[2],AGILITY:self.char.agility+self.char.majorPoints[3],PRECISION:self.char.precision+self.char.majorPoints[4],INTELLIGENCE:self.char.intelligence+self.char.majorPoints[5],MAGIE:self.char.magie+self.char.majorPoints[6],RESISTANCE:self.char.majorPoints[7],PERCING:self.char.majorPoints[8],CRITICAL:self.char.majorPoints[9],10:self.char.majorPoints[10],11:self.char.majorPoints[11],12:self.char.majorPoints[12],13:self.char.majorPoints[13],14:self.char.majorPoints[14]}
                    for obj in [self.char.weapon,self.char.stuff[0],self.char.stuff[1],self.char.stuff[2]]:
                        valueElem = 1
                        if obj.affinity == self.char.element :
                            valueElem = 1.1
                        
                        baseStats[0] += int(obj.strength*valueElem)
                        baseStats[1] += int(obj.endurance*valueElem)
                        baseStats[2] += int(obj.charisma*valueElem)
                        baseStats[3] += int(obj.agility*valueElem)
                        baseStats[4] += int(obj.precision*valueElem)
                        baseStats[5] += int(obj.intelligence*valueElem)
                        baseStats[6] += int(obj.magie*valueElem)
                        baseStats[7] += int(obj.resistance*valueElem)
                        baseStats[8] += int(obj.percing*valueElem)
                        baseStats[9] += int(obj.critical*valueElem)
                        baseStats[10] += int(obj.negativeHeal)
                        baseStats[11] += int(obj.negativeBoost)
                        baseStats[12] += int(obj.negativeShield)
                        baseStats[13] += int(obj.negativeDirect)
                        baseStats[14] += int(obj.negativeIndirect)

                else:
                    baseStats = {STRENGTH:self.char.majorPoints[0],ENDURANCE:self.char.majorPoints[1],CHARISMA:self.char.majorPoints[2],AGILITY:self.char.majorPoints[3],PRECISION:self.char.majorPoints[4],INTELLIGENCE:self.char.majorPoints[5],MAGIE:self.char.majorPoints[6],RESISTANCE:self.char.majorPoints[7],PERCING:self.char.majorPoints[8],CRITICAL:self.char.majorPoints[9],10:self.char.majorPoints[10],11:self.char.majorPoints[11],12:self.char.majorPoints[12],13:self.char.majorPoints[13],14:self.char.majorPoints[14]}
                    temp = self.char.allStats()+[self.char.resistance,self.char.percing,self.char.critical]
                    temp2 = self.summoner.allStats()+[self.summoner.resistance,self.summoner.percing,self.summoner.critical]
                    adv = 0
                    for a in range(0,len(temp)):
                        if type(temp[a]) == list:
                            if temp[a][0] == PURCENTAGE:
                                baseStats[a] += int(temp2[a]*(temp[a][1]+adv))
                            elif temp[a][0] == HARMONIE:
                                harmonie = 0
                                for b in temp2:
                                    harmonie = max(harmonie,b)
                                baseStats[a] += harmonie*adv
                        else:
                            baseStats[a] = temp[a]

                if self.char.element in [ELEMENT_FIRE, ELEMENT_UNIVERSALIS_PREMO]:
                    baseStats[7] += 5
                elif self.char.element in [ELEMENT_WATER, ELEMENT_UNIVERSALIS_PREMO]:
                    baseStats[PRECISION] += 10
                elif self.char.element in [ELEMENT_AIR, ELEMENT_UNIVERSALIS_PREMO]:
                    baseStats[AGILITY] += 10
                elif self.char.element in [ELEMENT_EARTH, ELEMENT_UNIVERSALIS_PREMO]:
                    baseStats[6] += 5

                valueToBoost = self.char.level / 50
                baseStats[ENDURANCE] += int(30*valueToBoost)
                baseStats[RESISTANCE] += int(15*valueToBoost)

                if danger > 100 and type(self.char) == octarien:
                    add = int(danger/135 * 20)
                    for cmpt in [AGILITY,PRECISION,RESISTANCE]:
                        baseStats[cmpt] += add

                if self.char.weapon.id in eternalInkWeaponIds:
                    summation = 0
                    for stat in range(10,15):
                        if baseStats[stat] > 0:
                            summation = int(baseStats[stat]*0.7)
                            baseStats[stat] = 0

                    baseStats[self.char.weapon.use] += summation

                if self.char.aspiration == BERSERK:
                    self.specialVars["aspiSlot"] = BERS_LIFE_STEAL
                elif self.char.aspiration == TETE_BRULE:
                    for cmpt in (0,2,5,6):
                        baseStats[cmpt] = baseStats[cmpt] * 0.8
                    for cmpt in range(10,15):
                        baseStats[cmpt] = baseStats[cmpt] * 1.35
                elif self.char.aspiration in [PROTECTEUR,VIGILANT,ENCHANTEUR]:
                    self.specialVars["aspiSlot"] = []

                # Specials interractions ---------------------------------------------------
                # Kitsunes Sisters
                if self.char.isNpc("Liu") or self.char.isNpc("Lia") or self.char.isNpc("Liz") or self.char.isNpc("Lio"):
                    baseStats[CHARISMA] = int(baseStats[CHARISMA] * (0.9 + 0.1 * (dictInteraction["Liu"]+dictInteraction["Lia"]+dictInteraction["Liz"]+dictInteraction["Lio"])))

                # Alice : Increase stats by sisters in the fight
                elif self.char.isNpc("Alice"):
                    baseStats[CHARISMA] = int(baseStats[CHARISMA] * (1 + 0.05 * (dictInteraction["Sixtine"]+dictInteraction["Félicité"]+dictInteraction["Clémence"])))

                # Félicité : Increase stats by sisters in the fight
                elif self.char.isNpc("Félicité"):
                    baseStats[STRENGTH] = int(baseStats[STRENGTH] * (1 + 0.05 * (dictInteraction["Sixtine"]+dictInteraction["Alice"]+dictInteraction["Clémence"])))

                # Sixtine : Increase stats by sisters in the fight
                elif self.char.isNpc("Sixtine"):
                    baseStats[INTELLIGENCE] = int(baseStats[INTELLIGENCE] * (1 + 0.05 * (dictInteraction["Félicité"]+dictInteraction["Alice"]+dictInteraction["Clémence"])))

                # Clémence : Increase stats by sisters in the fight
                elif self.char.isNpc("Clémence"):
                    baseStats[MAGIE] = int(baseStats[MAGIE] * (1 + 0.05 * (dictInteraction["Sixtine"]+dictInteraction["Alice"]+dictInteraction["Félicité"])))

                # John : Increase stats if Clemence is in the figth
                elif self.char.isNpc("John"):
                    baseStats[STRENGTH], baseStats[ENDURANCE] = int(baseStats[STRENGTH] * (1 + 0.1 * dictInteraction["Clémence"])), int(baseStats[ENDURANCE] * (1 + 0.1 * dictInteraction["Clémence"]))

                self.baseStats = baseStats
                self.maxHp = round((baseHP+perso.level*HPparLevel)*((baseStats[ENDURANCE])/100+1))

                if type(self.char) == octarien:
                    self.maxHp = round(self.maxHp * danger / 100)
                self.hp = copy.deepcopy(self.maxHp)

                if type(self.char) == invoc:
                    self.specialVars["osPro"] = summoner.specialVars["osPro"]
                    self.specialVars["osPre"] = summoner.specialVars["osPre"]
                    self.specialVars["osIdo"] = summoner.specialVars["osIdo"]
                    self.specialVars["ohAlt"] = summoner.specialVars["ohAlt"]
                    self.specialVars["ohPro"] = summoner.specialVars["ohPro"]
                    self.specialVars["ohIdo"] = summoner.specialVars["ohIdo"]

            def allStats(self):
                """Return the mains 7 stats"""
                return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

            def move(self,cellToMove:Union[cell,None]=None ,x:Union[int,None]=None ,y:Union[int,None]=None):
                """Move the entity on the given coordonates"""
                if cellToMove == x == y == None:
                    raise Exception("Argument error : No parameters given")
                actCell = self.cell
                if cellToMove == None:
                    destination = findCell(x,y)
                else:
                    destination = findCell(cellToMove.x,cellToMove.y)
                self.cell = destination
                destination.on = self
                if actCell != None:
                    actCell.on = None

            def valueBoost(self,target = 0,heal=False,armor=False):
                """
                    Return the bonus multiplier for any Buff, Debuff or Healing action\n
                    Parameter :\n
                    .target : A ``entity``.
                        -> Use for the Altruistic malus on their-self
                    .heal : Does the action is a Heal action ? Default ``False``
                """

                if target == 0:
                    raise Exception("No target given")

                if self.char.aspiration == ALTRUISTE:           # Altruistic : Better heals and buff on others
                    if heal:
                        if target == self:
                            return 1
                        else:
                            return 1.2
                    else:
                        if target == self:
                            return 0.8
                        else:
                            return 1.2

                elif self.char.aspiration == IDOLE and not(heal) and not(armor):             # Idol : The more alive allies they got, the more their buff a heals or powerfull
                    alice = 0
                    for a in tablEntTeam[self.team]:
                        if a.hp > 0 and type(a.char) != invoc:
                            alice += 1

                    return 0.9 + alice*0.05
                
                elif self.char.aspiration == INOVATEUR and not(heal) and not(armor):             # Idol : The more alive allies they got, the more their buff a heals or powerfull
                    alice = 0
                    for a in tablEntTeam[not(self.team)]:
                        if a.hp > 0 and type(a.char) != invoc:
                            alice += 1

                    return 0.9 + alice*0.05

                elif self.char.aspiration in [PREVOYANT,PROTECTEUR] and armor:
                    if self.char.aspiration == PREVOYANT:
                        return 1.2
                    else:
                        return 1 + 0.05 * len(self.specialVars["aspiSlot"])

                elif self.char.aspiration == VIGILANT and heal:
                    return 1 + 0.05 * len(self.specialVars["aspiSlot"])

                else:
                    return 1

            def effectIcons(self):
                """Return a ``string`` with alls ``fightEffects`` icons, names and values on the entity"""
                temp,allReadySeenId,allReadySeenName,allReadySeenNumber = "", [], [], []
                if self.effect != []:
                    for a in self.effect:
                        if a.effect.stackable and a.effect.id in allReadySeenId and a.effect.id not in [vulne.id,dmgUp.id,dmgDown.id,defenseUp.id]:
                            for cmpt in range(len(allReadySeenId)):
                                if a.effect.id == allReadySeenId[cmpt]:
                                    allReadySeenNumber[cmpt] += 1
                        elif a.effect.stackable and a.effect.id not in allReadySeenId and a.effect.id not in [vulne.id,dmgUp.id,dmgDown.id,defenseUp.id]:
                            allReadySeenId.append(a.effect.id)
                            allReadySeenNumber.append(1)
                            allReadySeenName.append("{0} {1}".format(a.icon,a.effect.name))
                        else:
                            name = a.effect.name
                            if name.endswith("é"):
                                name += self.accord()
                            if a.type == TYPE_ARMOR:
                                temp += f"{a.icon} {name} ({a.value} PV)\n"
                            elif a.effect.id in [vulne.id,dmgUp.id,dmgDown.id,defenseUp.id]:
                                power = round(a.effect.power,2)
                                temp += f"{a.icon} {name} ({power}%)\n"
                            elif a.effect.turnInit > 0:
                                pluriel = ""
                                if a.turnLeft > 1:
                                    pluriel = "s"
                                temp += f"{a.icon} {name} ({a.turnLeft} tour{pluriel})\n"
                            elif a.effect.id == eventFas.id:
                                temp += f"{a.icon} {name} ({a.value})\n"
                            else:
                                temp += f"{a.icon} {name}\n"
                    if allReadySeenId != []:
                        for cmpt in range(len(allReadySeenId)):
                            temp += "{0}{1}\n".format(allReadySeenName[cmpt],[""," x{0}".format(allReadySeenNumber[cmpt])][allReadySeenNumber[cmpt]>1])
                else:
                    temp = "Pas d'effet sur la cible"

                if len(temp) > 1024:
                    temp = completlyRemoveEmoji(temp)
                if len(temp) > 1024:
                    temp = "OVERLOAD"
                return temp

            def recalculate(self,ignore=None):
                """
                    Recalculate the entity stats with all their ``fightEffects``\n
                    - Parameter :
                        - ignore : A ``fightEffect`` to ignore. Default ``None``
                """
                baseStats = self.baseStats
                self.dmgUp, self.critDmgUp, self.healUp, self.critHealUp = 0,0,0,0
                sumStatsBonus = [baseStats[0],baseStats[1],baseStats[2],baseStats[3],baseStats[4],baseStats[5],baseStats[6],baseStats[7],baseStats[8],baseStats[9],baseStats[10],baseStats[11],baseStats[12],baseStats[13],baseStats[14]]

                self.translucide = False
                self.untargetable = False
                self.invisible = False
                self.immune = False
                self.stun = False

                for eff in self.effect:
                    if eff != ignore:
                        if eff.effect.stat != None and eff.effect.overhealth == 0:
                            tablEffStats = eff.allStats()
                            for cmpt in range(9):
                                sumStatsBonus[cmpt] += tablEffStats[cmpt]

                        else:
                            sumStatsBonus[0] += eff.effect.strength 
                            sumStatsBonus[1] += eff.effect.endurance 
                            sumStatsBonus[2] += eff.effect.charisma
                            sumStatsBonus[3] += eff.effect.agility
                            sumStatsBonus[4] += eff.effect.precision
                            sumStatsBonus[5] += eff.effect.intelligence
                            if eff.effect.id == "tem":
                                sumStatsBonus[6] += int(self.char.level * 2.5)
                            else:
                                sumStatsBonus[6] += eff.effect.magie
                            sumStatsBonus[7] += eff.effect.resistance
                            sumStatsBonus[8] += eff.effect.percing
                            sumStatsBonus[9] += eff.effect.critical

                    if eff.stun:
                        self.stun = True

                    if eff.effect.invisible:
                        self.translucide = True
                        self.untargetable = True
                        self.invisible = True

                    if eff.effect.translucide:
                        self.translucide = True

                    if eff.effect.untargetable:
                        self.untargetable = True

                    if eff.effect.immunity:
                        self.immune = True

                    self.dmgUp, self.critDmgUp, self.healUp, self.critHealUp = self.dmgUp+eff.effect.dmgUp, self.critDmgUp+eff.effect.critDmgUp, self.healUp+eff.effect.healUp, self.critHealUp+eff.effect.critHealUp
                if type(self.char) != invoc:
                    tRes = sumStatsBonus[7]+self.char.resistance
                else:
                    tRes = sumStatsBonus[7]

                t1 = max(0,tRes - 100)
                t2 = min(max(0,tRes - 40),60)
                t3 = min(tRes,40)

                sumStatsBonus[7] = int(t3 + t2//3 + t1//5)

                if type(self.char) in [char,tmpAllie] and sumStatsBonus[7] < 50:
                    sumStatsBonus[7] = max(5 + int(15/50*self.char.level)+sumStatsBonus[7],5 + int(15/50*self.char.level))

                if ignore == None:
                    self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie = round(sumStatsBonus[0]),round(sumStatsBonus[1]),round(sumStatsBonus[2]),round(sumStatsBonus[3]),round(sumStatsBonus[4]),round(sumStatsBonus[5]),round(sumStatsBonus[6])
                    self.resistance,self.percing,self.critical = sumStatsBonus[7],round(sumStatsBonus[8]),round(sumStatsBonus[9])
                    self.negativeHeal, self.negativeBoost, self.negativeShield, self.negativeDirect, self.negativeIndirect = sumStatsBonus[10],sumStatsBonus[11],sumStatsBonus[12],sumStatsBonus[13],sumStatsBonus[14]
                else:
                    if type(self.char) != invoc:
                        return [
                            round(self.char.strength+sumStatsBonus[0]),round(self.char.endurance+sumStatsBonus[1]),round(self.char.charisma+sumStatsBonus[2]),round(self.char.agility+sumStatsBonus[3]),round(self.char.precision+sumStatsBonus[4]),round(self.char.intelligence+sumStatsBonus[5]),round(self.char.magie+sumStatsBonus[6]),
                            sumStatsBonus[7],round(self.char.percing+sumStatsBonus[8]),round(self.char.critical+sumStatsBonus[9]),
                            sumStatsBonus[10],sumStatsBonus[11],sumStatsBonus[12],sumStatsBonus[13],sumStatsBonus[14]]
                    else:
                        return [
                            round(sumStatsBonus[0]),round(sumStatsBonus[1]),round(sumStatsBonus[2]),round(sumStatsBonus[3]),round(sumStatsBonus[4]),round(sumStatsBonus[5]),round(sumStatsBonus[6]),
                            sumStatsBonus[7],round(sumStatsBonus[8]),round(sumStatsBonus[9]),
                            sumStatsBonus[10],sumStatsBonus[11],sumStatsBonus[12],sumStatsBonus[13],sumStatsBonus[14]
                        ]

            def refreshEffects(self):
                """Add the ``fightEffects`` into the waiting list and remove the obcelettes ones"""
                for eff in self.effect[:]:
                    if eff.remove:
                        self.effect.remove(eff)
                        try:
                            eff.caster.ownEffect.remove({self:eff.id})
                        except:
                            pass

                        if eff.effect.id == lunaInfiniteDarknessShield.id:
                            self.specialVars["clemBloodJauge"] = None
                        
                        elif eff.effect.id in [clemStunEffect.id,aliceStunEffect.id]:
                            self.specialVars["clemBloodJauge"].value = 100

                for a in addEffect[:]:
                    self.effect.append(a)
                    a.caster.ownEffect.append({self:a.id})
                    addEffect.remove(a)
                    if type(a) != fightEffect:
                        raise AttributeError("Except fightEffect, but get {0} insted".format(type(a)))
                self.recalculate()

            def indirectAttack(self,target=0,value=0,icon="",ignoreImmunity=False,name='',hideAttacker=False) -> str:
                """
                Method for when the entity is attacking undirectly another.\n
                /!\ Unlike .attack(), the damage need to be pre-calculated\n
                Parameters :\n
                .target : Another ``entity`` who's receving damage
                .value : The amount of damage deal. Default ``0``
                .icon : The ``string`` to use as the icon of the attack. Default ``""``
                .ignoreImmunity : Does the attack ignore any immune effect ? Default ``False``
                .name : The ``string`` to use as the name of the attakc. Default ``""``
                """

                popopo = ""
                value = round(value)
                if target.hp > 0 and not(target.immune):
                    # Looking for a absolute shield
                    maxResist, vulnePower = 0, 0
                    for eff in target.effect:
                        if eff.effect.immunity == True and not(ignoreImmunity):
                            value = 0
                        if eff.effect.absolutShield and eff.value > 0:
                            dmg = min(value,eff.value)
                            if not(hideAttacker):
                                popopo += f"{self.icon} {icon} → {eff.icon}{eff.on.icon} -{dmg} PV\n"
                            else:
                                popopo += f"{eff.icon}{eff.on.icon} -{dmg} PV\n"
                            popopo += eff.decate(value=dmg)
                            self.stats.damageOnShield += dmg
                            if eff.value <= 0:
                                reduc = eff.on.char.level
                                if eff.effect.lightShield:
                                    reduc = 0
                                value = max(0,dmg-reduc)
                            else:
                                value = 0
                        if eff.effect.id == vulne.id:
                            vulnePower = max(vulnePower,eff.effect.power)
                        maxResist = max(maxResist,eff.inkResistance)

                    if type(target.char) == invoc and target.char.name.startswith("Patte de The Giant Enemy Spider"):
                        value = int(value * GESredirect.redirection/100)
                        target.summoner.hp -= value
                        if self != target:                  # If the damage is deal on another target, increase the correspondings stats
                            self.stats.damageDeal += value
                            self.stats.indirectDamageDeal += value
                            target.stats.damageRecived += value

                        if target.summoner.hp <= 0:
                            popopo += target.death(killer=self)

                        value = 0

                    # If the target is Ailill and she have his special effect, reduce the damage

                    secElemBonus = 1
                    if self.char.secElement == ELEMENT_LIGHT:
                        secElemBonus += 0.05
                    elif self.char.secElement == ELEMENT_DARKNESS:
                        secElemBonus -= 0.05
                    if target.char.secElement == ELEMENT_LIGHT:
                        secElemBonus += 0.05
                    elif target.char.secElement == ELEMENT_DARKNESS:
                        secElemBonus -= 0.05

                    value = int(value * (100-maxResist) / 100 * (100+vulnePower) / 100 * secElemBonus)

                    # If the number of damage is still above 0
                    if value > 0:
                        target.hp -= value
                        if self != target:                  # If the damage is deal on another target, increase the correspondings stats
                            self.stats.damageDeal += value
                            self.stats.indirectDamageDeal += value
                            target.stats.damageRecived += value
                        else:                               # Else, increase the selfBurn stats
                            self.stats.selfBurn += value
                        if name != '':
                            name = ' ({0})'.format(name)
                        if not(hideAttacker):
                            popopo += f"{self.icon} {icon} → {target.icon} -{value} PV{name}\n"
                        else:
                            popopo += f"{target.icon} -{value} PV{name}\n"
                        if self.isNpc("Liz") or self.isNpc("Kitsune"):
                            popopo += add_effect(self,target,charming)
                            target.refreshEffects()

                        if target.hp <= 0:
                            popopo += target.death(killer=self)

                return popopo

            def death(self,killer = 0,trueDeath=False) -> str:
                """
                    The death method, to use when the entity dies.\n
                    Parameter :\n
                    .killer : The ``entity`` who have kill the entity
                """

                for eff in self.effect:
                    if eff.effect.id in [undeadEff2.id,holmgangEff.id] and eff.turnLeft > 0:
                        self.hp = 1
                        return "{0} ne peut pas être vaincu{1} ({2})\n".format(self.name,self.accord(),eff.effect.name)
                    elif eff.effect.id == undeadEff.id and not(trueDeath):
                        ballerine = groupAddEffect(self,self,AREA_MONO,eff.effect.callOnTrigger,skillIcon=eff.icon)
                        ballerine += eff.decate(value=1)
                        self.refreshEffects()
                        self.hp = 1
                        return "{4} transcende la mort !\n{0} {1} → {0} +{2} __{3}__\n".format(self.icon, eff.icon, eff.effect.callOnTrigger.emoji[self.char.species-1][self.team],eff.effect.callOnTrigger.name,self.name)
                    elif eff.effect.id == deterEff1.id:
                        ballerine = eff.decate(value=1)
                        self.refreshEffects()
                        self.hp = int(self.maxHp * eff.effect.power / 100)
                        return "{3} transcende la mort !\n{0} {1} → {0} +{2} PV\n".format(self.icon, eff.icon,int(self.maxHp * (1 + eff.effect.power / 100)),self.char.name)
                pipistrelle = f"{self.char.name} ({self.icon}) est vaincu{self.accord()} !\n"
                if self.status == STATUS_RESURECTED:
                    pipistrelle = f"{self.char.name} ({self.icon}) est vaincu{self.accord()} (pour de bon) !\n"
                    self.status=STATUS_TRUE_DEATH

                if type(self.char) != invoc and killer != self and killer.char.says.onKill != None and random.randint(0,99)<33:
                    try:
                        if killer.isNpc("Ailill"):
                            pipistrelle += "{0} : *\"{1}\"*\n".format('<a:Ailill:882040705814503434>','Ça manque de sang qui gicle partout ça')
                        elif killer.isNpc("Luna prê."):
                            msgPerElement = [None,None,None,None,None,"La lumière ne peut pas toujours avoir raison de l'ombre.","Reviens donc quand tu auras compris ce que sont les vrais Ténèbres.","L'Espace peut très bien être brisé.","Essaye donc de gagner du Temps là dessus.","Tu as tous les éléments et tu n'est même pas capable de t'en sortir ?"]
                            if msgPerElement[self.char.element] != None:
                                pipistrelle += "{0} : *\"{1}\"*\n".format(killer.icon,msgPerElement[self.char.element])
                            else:
                                pipistrelle += "{0} : *\"{1}\"*\n".format(killer.icon,killer.char.says.onKill.format(target=self.char.name,caster=killer.char.name))
                        elif killer.isNpc("Ly") and self.isNpc("Zombie"):
                            pipistrelle += "{0} : *\"Tu peux ramner tous tes potes si tu veux, je connais un prêtre qui est toujours prêt à me racheter de la rotten flesh\"*\n".format(killer.icon,killer.char.says.onKill.format(target=self.char.name,caster=killer.char.name))
                        else:
                            pipistrelle += "{0} : *\"{1}\"*\n".format(killer.icon,killer.char.says.onKill.format(target=self.char.name,caster=killer.char.name))
                    except:
                        pipistrelle += "__Error whith the onKill message__\n"
                        log = format_exc()
                        if len(log) > 50:
                            pipistrelle += "{0}\n".format(log[-50:])
                        else:
                            pipistrelle += "{0}\n".format(log)

                if self.isNpc("Alice") and random.randint(0,99) < 1:
                    pipistrelle += "{0} : *\"{1}\"*\n".format(self.icon,"Tss... J'aurais du tous vous écraser quand je l'aurais pu...")
                    alicePing = True

                elif (self.isNpc("Shushi") or self.isNpc("Shihu")) and dictIsPnjVar["Lena"]:
                    pipistrelle += "{0} : *\"{1}\"*\n".format('<:lena:909047343876288552>','Shu- Ok là on va sérieusement commencer à se calmer.')
                    for ent in tablEntTeam[self.team]:
                        if ent.isNpc("Lena"):
                            mater = classes.effect("Instinct maternelle","ohFuckYou",critDmgUp=10,critical=5,percing=10,turnInit=-1,emoji=uniqueEmoji('<:angry:862321601978040350>'),stackable=True)
                            pipistrelle += add_effect(ent,ent,mater)
                            ent.refreshEffects()
                            break

                elif self.isNpc("Alice Exaltée") and killer.isNpc("Clémence pos."):
                    pipistrelle += "<a:aliceExalte:914782398451953685> : \"Clé...\"\n<a:clemPos:914709222116175922> : \"... ?\""
                    effect = classes.effect("Réveil subconsicent","clemAwakening",magie=-int((killer.baseStats[MAGIE]*0.3)),turnInit=-1,unclearable=True,type=TYPE_MALUS)
                    pipistrelle += add_effect(killer,killer,effect)
                    killer.char.exp = 35

                elif self.isNpc("Lohica") and killer != self:
                    pipistrelle += "{0} : *\"Ok {1}, qu'est-ce que tu dis de ça ?\"*\n".format(self.icon,killer.char.name) + add_effect(self,killer,estal)
                    killer.refreshEffects()
                elif random.randint(0,99)<33:
                    if self.isNpc("Hina") and dictIsPnjVar["Lohica"]:
                        pipistrelle += "{0} : *\"{1}\"*\n".format('<:lohica:919863918166417448>','Ts. Encore par terre toi ?')
                    elif self.isNpc("Edelweiss") and dictIsPnjVar["Lohica"]:
                        pipistrelle += "{0} : *\"{1}\"*\n".format('<:lohica:919863918166417448>','Am-')
                    elif self.isNpc("Clémence") and dictIsPnjVar["John"]:
                        pipistrelle += "{0} : *\"{1}\"*\n".format('<:john:908887592756449311>','Clémence !')
                    elif self.isNpc("Félicité") and dictIsPnjVar["Alice"]:
                        pipistrelle += "{0} : *\"{1}\"*\n".format('<:alice:908902054959939664>','Féli ! On se retrouve à la maison !')
                    elif self.char.says.onDeath != None:
                        try:
                            pipistrelle += "{0} : *\"{1}\"*\n".format(self.icon,self.char.says.onDeath.format(target=self.char.name,caster=killer.char.name))
                        except:
                            pipistrelle += "__Error whith the death message__\n"
                            log = format_exc()
                            if len(log) > 50:
                                pipistrelle += "{0}\n".format(log[-50:])
                            else:
                                pipistrelle += "{0}\n".format(log)

                try:                # Reactions
                    if random.randint(0,99) < 20 and type(self.char) != invoc:
                        tablAllInterract = []
                        for ent in tablEntTeam[self.team]:
                            if ent.char.says.reactAllyKilled != None and ent != self and ent.hp > 0:
                                tablAllInterract.append("{0} : *\"{1}\"*\n".format(ent.icon,ent.char.says.reactAllyKilled.format(killer=killer.char.name,downed=self.char.name)))
                        for ent in tablEntTeam[not(self.team)]:
                            if ent.char.says.reactEnnemyKilled != None and ent != killer and ent.hp > 0:
                                tablAllInterract.append("{0} : *\"{1}\"*\n".format(ent.icon,ent.char.says.reactEnnemyKilled.format(killer=killer.char.name,downed=self.char.name)))

                        if len(tablAllInterract) == 1:
                            pipistrelle += tablAllInterract[0]
                        elif len(tablAllInterract) > 1:
                            pipistrelle += tablAllInterract[random.randint(0,len(tablAllInterract)-1)]

                except:
                    pipistrelle += "__Error whith the death reaction message__\n"
                    log = format_exc()
                    if len(log) > 50:
                        pipistrelle += "{0}\n".format(log[-50:])
                    else:
                        pipistrelle += "{0}\n".format(log)

                allreadyexplose = False
                for fEffect in self.effect:
                    if fEffect.trigger == TRIGGER_DEATH:
                        pipistrelle += fEffect.triggerDeath(killer)

                    if fEffect.effect.id == estal.id and fEffect.caster.char.weapon.id == secretum.id and not(allreadyexplose):
                        summationPower = 0
                        for eff in self.effect:
                            if eff.effect.id == estal.id and eff.turnLeft > 0:
                                summationPower += eff.effect.power * secretum.effect.power / 100 * eff.turnLeft
                                eff.decate(turn=99,value=99)

                        stat,damageBase,allReadySeen = fEffect.caster.allStats()[MAGIE]-fEffect.caster.negativeIndirect,summationPower,[]
                        for a in self.cell.getEntityOnArea(area=secretum.effect.area,team=self.team,wanted=ALLIES,directTarget=False):
                            reduc = 1
                            if a != self:
                                reduc = max(AOEMINDAMAGE,1-self.cell.distance(a.cell)*AOEDAMAGEREDUCTION)

                            if stat != None:
                                damage = damageBase * (1+(stat/100)) *  (1-(min(95,a.resistance*(1-fEffect.caster.percing/100))/100)) * (reduc) * fEffect.caster.getElementalBonus(a,secretum.effect.area,TYPE_INDIRECT_DAMAGE) * (1+(0.01*self.level))

                            pipistrelle += fEffect.caster.indirectAttack(a,value=damage,icon = secretum.emoji,name=secretum.effect.name)
                            if fEffect.caster.hp > 0:
                                add_effect(fEffect.caster,a,estal,effPowerPurcent=secretum.effect.power)
                                a.refreshEffects()
                                allReadySeen.append(a.icon)

                        if len(allReadySeen) > 1:
                            temp = "{0} {1} → ".format(fEffect.caster.icon,secretum.emoji)
                            for cmpt in range(len(allReadySeen)):
                                temp += allReadySeen[cmpt]

                            pipistrelle += temp + " +{0} __{1}__ ({2}%)\n".format(estal.emoji[0][0],estal.name,secretum.effect.power)
                        allreadyexplose = True

                    elif fEffect.effect.id == reaperEff.id:
                        pipistrelle += fEffect.caster.heal(fEffect.caster,fEffect.icon,None,int(fEffect.caster.maxHp*fEffect.effect.power/100), effName = fEffect.effect.name,danger=danger, mono = True, useActionStats = None)[0]
                    
                    fEffect.decate(turn=99)
                self.refreshEffects()

                if killer.char.aspiration == SORCELER:
                    stat,damageBase = killer.allStats()[MAGIE]-killer.negativeIndirect,max(5,killer.char.level//2)
                
                    for a in self.cell.getEntityOnArea(area=AREA_CIRCLE_1,team=self.team,wanted=ALLIES,directTarget=False):
                        reduc = 1
                        if a != self:
                            reduc = max(AOEMINDAMAGE,1-self.cell.distance(a.cell)*AOEDAMAGEREDUCTION)

                        damage = damageBase * (1+(stat/100)) *  (1-(min(95,a.resistance*(1-killer.percing/100))/100)) * (reduc) * killer.getElementalBonus(a,AREA_CIRCLE_1,TYPE_INDIRECT_DAMAGE) * (1+(0.01*killer.level))

                        pipistrelle += killer.indirectAttack(a,value=damage,icon = aspiEmoji[SORCELER])

                elif killer.char.aspiration == ATTENTIF:
                    for a in range(7):
                        killer.baseStats[a] = int(killer.baseStats[a]*1.1)
                if self.status == STATUS_ALIVE:
                    if self.ressurectable:
                        if type(self.char) != octarien or (type(self.char) == octarien and self.char.rez):
                            self.status = STATUS_DEAD
                        else:
                            self.status = STATUS_TRUE_DEATH
                    else:
                        self.status = STATUS_TRUE_DEATH

                if type(self.char) != invoc and self.status != STATUS_RESURECTED:
                    if killer.isNpc("Ailill"):
                        self.icon = [None,'<:aillilKill1:898930720528011314>','<:ailillKill2:898930734063046666>','<:ailillKill2:898930734063046666>'][self.char.species]
                    elif self.char.deadIcon == None:
                        if type(self.char) != char:
                            self.icon = [None,'<:spIka:866465882540605470>','<:spTako:866465864399323167>','<:spOcta:866465980586786840>'][self.char.species]
                        else:
                            self.icon = [
                                ['<:spIka:866465882540605470>','<:spTako:866465864399323167>'][self.char.species-1],
                                ['<:oci:930481536564879370>','<:oct:930481523096969237>'][self.char.species-1],
                                '<:komoriOut:930798849969246208>',
                                '<:birdOut:930906560811646996>',
                                '<:outSkeleton:930910463951249479>',
                                ['<:fairyOut:935335430814068786>','<:fairy2Out:935336513242292324>'][self.char.species-1]
                            ][self.char.iconForm]
                    else:
                        self.icon = self.char.deadIcon

                elif self.status == STATUS_RESURECTED:
                    add_effect(self,self,onceButNotTwice)

                elif self.status == STATUS_DEAD:
                    effect = lostSoul
                    if self.specialVars["tankTheFloor"]:
                        effect.turnInit += 1
                    add_effect(killer,self,effect)
                    
                    self.refreshEffects()

                elif self.status == STATUS_TRUE_DEATH and killer.isNpc("Kitsune"):
                    pipistrelle += killer.heal(killer,"",CHARISMA,60, effName = "Âme consummée",danger=100, mono = True, useActionStats = ACT_HEAL)[0]

                if self.isNpc("Kiku"):
                    for ent in tablEntTeam[self.team]:
                        for eff in ent.effect:
                            if eff.effect.id == kikuRezEff.id:
                                ent.hp = 0
                                pipistrelle += ent.death(killer=killer)
                                break

                if type(self.char) != invoc and killer != self or killer.team != self.team:
                    killer.stats.ennemiKill += 1
                elif type(self.char) != invoc and killer != self and killer.team == self.team:
                    killer.stats.friendlyfire += 1
                return pipistrelle

            def attack(self,target=0,value = 0,icon = "",area=AREA_MONO,sussess=None,use=STRENGTH,onArmor = 1,effectOnHit = None, useActionStats = ACT_DIRECT, setAoEDamage = False, lifeSteal:int = 0, erosion = 0, skillPercing = 0) -> str:
                """
                    The method for when a entity attack.\n
                    Unlike .indirectAttack(), the targets, damages and triggered effects are all calculated in this method\n
                    - Parameters :
                        - target : The ``entity`` targeted by the entity
                        - value : The base power of the attack.
                            - If the value is at ``0``, no ``string`` is return
                        - icon : The ``string`` to use as the icon of the attack. Default ``""``
                        - area : The area of the attack. See ``constantes``. Default ``AREA_MONO``
                        - sussess : The base precision of the attack. If at ``None`` (Default), use the sussess rate of the entity weapon insted
                        - use : The base stat to take for the attack. See ``constantes``
                        - onArmor : The multiplier of damage to deal on armors effects. Default ``1``
                        - effectOnHit : Does the attack give a `effect` on the targets ? Default ``None``
                """
                if sussess==None: # If no success is gave, use the weapon success rate
                    sussess=self.char.weapon.sussess

                if value > 0 and self.specialVars["damageSlot"] != None and ((self.specialVars["damageSlot"].effect.id == physicRuneEff.id and use in [STRENGTH,PRECISION,AGILITY]) or (self.specialVars["damageSlot"].effect.id == magicRuneEff.id and use in [MAGIE,CHARISMA,INTELLIGENCE])):
                    value = value * (self.specialVars["damageSlot"].effect.power/100+1)

                if self.specialVars["clemMemCast"]:                 # If the attack is the clem' boss memento, update the damage on armor value if she has her shield
                    isufDPTLol = False
                    for eff in self.effect:
                        if eff.effect.id == clemUltShield.id:
                            isufDPTLol = True
                            onArmor = 666
                            break

                if useActionStats == None:
                    useActionStats = ACT_DIRECT

                sumDamage, deathCount = 0, 0

                popipo,critMsg = "",""

                if type(target) != int and value > 0: # If the target is valid
                    dangerMul = 1
                    if danger != None and self.team: # get danger value
                        dangerMul = danger/100

                    popipo,immune,multiplicateur,damageMul,dmgUpPower = "",False,1, 1, 0
                    if self.char.aspiration == TETE_BRULE:
                        erosion += 15

                    for a in self.effect: # Does the attacker trigger a effect
                        if a.trigger == TRIGGER_DEALS_DAMAGE and value > 0:
                            temp = a.triggerDamage(value = a.effect.power,icon=a.icon,onArmor=onArmor)
                            value = temp[0]
                            popipo += temp[1]
                        elif a.effect.id == dmgDown.id:
                            dmgUpPower -= a.effect.power
                        elif a.effect.id == dmgUp.id:
                            dmgUpPower += a.effect.power

                    damageMul = damageMul + (dmgUpPower/100)
                    damageMul = max(0,damageMul)

                    if self.hp > 0: # Does the attacker still alive ?
                        critMalusCmpt = 0
                        for entityInArea in target.cell.getEntityOnArea(area=area,team=self.team,wanted=ENNEMIS,directTarget=False): # For eatch ennemis in the area
                            self.stats.totalNumberShot += 1
                            if entityInArea.hp > 0: # If the target is alive
                                # Dodge / Miss
                                attPre,targetAgi, dodgeMul = self.precision,entityInArea.agility, 1 - (foulleeEff.power/100*int(entityInArea.specialVars['foullee']))
                                if attPre < 0:                                              # If the attacker's precision is negative
                                    targetAgi += abs(attPre)                                        # Add the negative to the target's agility
                                    attPre = 0
                                elif targetAgi < 0:                                         # Same if the target's agility is negative, add it to the attacker's precision
                                    attPre += abs(targetAgi)
                                    targetAgi = 1

                                if attPre < targetAgi:                                      # If the target's agility is (better ?) than the attacker's precision
                                    successRate = 1 - min((targetAgi-attPre)/100,1)*0.5 * dodgeMul             # The success rate is reduced to 50% of the normal
                                else:
                                    successRate = 1 + min((attPre-targetAgi)/100,1) * dodgeMul                 # The success rate is increased up to 200% of the normal

                                # It' a hit ?
                                if random.randint(0,99)<successRate*sussess:
                                    pp = 0
                                    if self.char.aspiration in [POIDS_PLUME,OBSERVATEUR]: # Apply "Poids Plume" critical bonus
                                        pp = actTurn.specialVars["aspiSlot"]

                                    # Get the stat used
                                    if use == HARMONIE:
                                        temp = 0
                                        for a in self.allStats():
                                            temp = max(a,temp)
                                        used = temp
                                    else:
                                        used = self.allStats()[use]
                                        if use == MAGIE and self.char.aspiration == ENCHANTEUR:
                                            used = int(used * 0.95+(0.05)*len(self.specialVars["aspiSlot"]))

                                    if entityInArea.immune:
                                        damage = 0
                                    else:
                                        damage = dmgCalculator(self, entityInArea, value, use, useActionStats, danger, area, typeDmg = TYPE_DAMAGE, skillPercing = 0)

                                    # AoE reduction factor
                                    if entityInArea == target or setAoEDamage: 
                                        multiplicateur = 1
                                    else:
                                        multiplicateur = 1-(min(1-AOEMINDAMAGE,target.cell.distance(entityInArea.cell)*AOEDAMAGEREDUCTION))

                                    # Damage reduction
                                    vulnePower, defenseUpPower, tempToReturn, noneArmorMsg, reaperDmgBoost = 0, 0, "", "", 0
                                    if not(entityInArea.immune):
                                        for a in entityInArea.effect:
                                            if a.trigger == TRIGGER_DAMAGE:
                                                temp = a.triggerDamage(value = damage,declancher=self,icon=icon,onArmor=onArmor)
                                                damage = temp[0]
                                                if a.effect.overhealth > 0 or a.effect.redirection > 0:
                                                    if self.icon not in tempToReturn:
                                                        tempToReturn = f"{self.icon} {icon} → "+temp[1]
                                                    else:
                                                        tempToReturn += temp[1]
                                                else:
                                                    noneArmorMsg += temp[1]

                                            if a.effect.id == vulne.id:
                                                vulnePower += a.effect.power
                                            elif a.effect.id == defenseUp.id:
                                                defenseUpPower += a.effect.power
                                            elif a.effect.id == reaperEff.id and a.caster == self:
                                                reaperDmgBoost = 0.1
                                    entityInArea.refreshEffects()
                                    vulnePower -= defenseUpPower

                                    # Critical
                                    critRoll, critBonus, critDmgMul = random.randint(0,99), 0.15 * int(self.char.weapon.id in [ElitherScope.id]), 1
                                    critMsg, hasCrit = "", False
                                    critRate = int((self.agility+self.precision)/200*35)+self.critical
                                    if critRoll < critRate and damage > 0:
                                        if self.char.aspiration not in [POIDS_PLUME, OBSERVATEUR]:
                                            critMsg = " !"
                                            critDmgMul = 1.25 + critBonus
                                        else:
                                            critMsg = " !!"
                                            critDmgMul = (1.35 + critBonus)
                                        self.stats.crits += 1
                                        critMalusCmpt += 1
                                        critDmgMul += self.critDmgUp / 100
                                        hasCrit = True
                                    elif critRoll < critRate + pp and self.char.aspiration in [POIDS_PLUME,OBSERVATEUR] and damage > 0:
                                        critDmgMul = (1.45 + critBonus)
                                        critMsg = " !!!"
                                        self.specialVars["aspiSlot"] = 0
                                        self.stats.crits += 1
                                        critMalusCmpt += 1
                                        pp = 0
                                        critDmgMul += self.critDmgUp / 100
                                        hasCrit = True
                                    else:
                                        critDmgMul += self.dmgUp / 100

                                    secElemMul = 1
                                    if entityInArea.char.secElement == ELEMENT_LIGHT or (entityInArea.char.secElement == ELEMENT_SPACE and area != AREA_MONO) or (entityInArea.char.secElement == ELEMENT_TIME and area == AREA_MONO):
                                        secElemMul += 0.05
                                    if self.char.secElement == ELEMENT_LIGHT or (self.char.secElement == ELEMENT_SPACE and area != AREA_MONO) or (self.char.secElement == ELEMENT_TIME and area == AREA_MONO):
                                        secElemMul += 0.05
                                    if entityInArea.char.secElement == ELEMENT_DARKNESS:
                                        secElemMul -= 0.05
                                    if self.char.secElement == ELEMENT_DARKNESS:
                                        secElemMul -= 0.05

                                    effectiveDmg = round(damage*(100+multiplicateur)/100*secElemMul*critDmgMul)
                                    beforeDamageMul = copy.deepcopy(effectiveDmg)
                                    effectiveDmg = round(damage*(100+multiplicateur)/100*secElemMul*critDmgMul*(100+vulnePower)/100*(damageMul+reaperDmgBoost))

                                    if self.specialVars["clemMemCast"]:
                                        if isufDPTLol:
                                            if entityInArea.hp > 100+entityInArea.char.level*13:
                                                effectiveDmg = entityInArea.hp -1
                                            else:
                                                effectiveDmg = entityInArea.hp
                                        else:
                                            if entityInArea.hp > effectiveDmg*0.33:
                                                effectiveDmg = min(effectiveDmg,entityInArea.hp-1)

                                    self.stats.shootHited += 1
                                    if entityInArea != self:
                                        self.stats.damageDeal += effectiveDmg
                                        entityInArea.stats.damageRecived += effectiveDmg
                                    else:
                                        self.stats.selfBurn += effectiveDmg

                                    sumDamage += effectiveDmg
                                    entityInArea.stats.numberAttacked += 1
                                    entityInArea.hp -= effectiveDmg

                                    if erosion != 0 and effectiveDmg > 0:
                                        lostHp = int(effectiveDmg * erosion/100)
                                        entityInArea.maxHp -= lostHp

                                    # Damage bosted
                                    if use not in [None,HARMONIE]:
                                        for statBoost in self.effect:
                                            tstats = statBoost.allStats()

                                            if (tstats[use] != 0 or tstats[PERCING] != 0) and statBoost.caster != self: # If the stat was boosted by someone esle
                                                used = self.allStats()[use] - tstats[use]

                                                tempDmg = round(value * (used+100-self.actionStats()[useActionStats])/100 * (1-(min(95,entityInArea.resistance*(1-(self.percing-tstats[PERCING])/100))/100))*dangerMul*self.getElementalBonus(target=entityInArea,area=area,type=TYPE_DAMAGE)*(1+(0.01*self.level)))
                                                tempDmg = round(tempDmg*(100+multiplicateur)/100*critDmgMul*secElemMul*(100+vulnePower)/100*(damageMul+reaperDmgBoost))

                                                dif = effectiveDmg - tempDmg
                                                if dif > 0:
                                                    statBoost.caster.stats.damageBoosted += abs(dif)
                                                    self.stats.underBoost += abs(dif)
                                                else:
                                                    statBoost.caster.stats.damageDogded += abs(dif)

                                            elif statBoost.effect.id == dmgDown.id and beforeDamageMul-effectiveDmg > 0:
                                                statBoost.caster.stats.damageDogded += int(beforeDamageMul-effectiveDmg)
                                            elif statBoost.effect.id == dmgUp.id and beforeDamageMul-effectiveDmg < 0:
                                                statBoost.caster.stats.damageBoosted += int(beforeDamageMul-effectiveDmg)*-1
                                                entityInArea.stats.underBoost += int(beforeDamageMul-effectiveDmg)*-1

                                        for statBoost in entityInArea.effect:
                                            tstats = statBoost.allStats()
                                            if tstats[RESISTANCE] != 0 and statBoost.caster != self: # If the stat was boosted by someone esle
                                                used = self.allStats()[use]
                                                tempDmg = round(value * (used+100-self.actionStats()[useActionStats])/100 * (1-(min(95,(entityInArea.resistance-tstats[RESISTANCE])*(1-self.percing/100))/100))*dangerMul*self.getElementalBonus(target=entityInArea,area=area,type=TYPE_DAMAGE)*(1+(0.01*self.level)))
                                                tempDmg = round(tempDmg*(100+multiplicateur)/100*secElemMul*critDmgMul*(100+vulnePower)/100*(damageMul+reaperDmgBoost))
                                                dif = effectiveDmg - tempDmg
                                                if dif < 0:
                                                    statBoost.caster.stats.damageBoosted += abs(dif)
                                                    self.stats.underBoost += abs(dif)
                                                else:
                                                    statBoost.caster.stats.damageDogded += abs(dif)

                                            elif statBoost.effect.id == vulne.id and beforeDamageMul-effectiveDmg < 0:
                                                statBoost.caster.stats.damageBoosted += abs(beforeDamageMul-effectiveDmg)
                                                entityInArea.stats.underBoost += abs(beforeDamageMul-effectiveDmg)
                                            elif statBoost.effect.id == defenseUp.id and beforeDamageMul-effectiveDmg > 0:
                                                statBoost.caster.stats.damageDogded += abs(beforeDamageMul-effectiveDmg)

                                    # Damage message
                                    popipo += noneArmorMsg
                                    if effectiveDmg > 0 and tempToReturn == "":
                                        popipo += f"{self.icon} {icon} → {entityInArea.icon} -{effectiveDmg} PV{critMsg}\n"
                                    else:
                                        popipo += tempToReturn + f" {entityInArea.icon} -{effectiveDmg} PV{critMsg}\n"

                                    if erosion != 0 and effectiveDmg > 0:
                                        popipo += f"{self.icon} {icon} → {entityInArea.icon} -{lostHp} PV max\n"

                                    if entityInArea.hp <= 0:
                                        popipo += entityInArea.death(killer = self)
                                        deathCount += 1

                                    if effectOnHit != None and entityInArea == target and entityInArea.hp > 0:
                                        effectOnHit = findEffect(effectOnHit)
                                        popipo += add_effect(self,target,effectOnHit)

                                        entityInArea.refreshEffects()

                                    if hasCrit and len(listFasTeam[self.team]) > 0 and random.randint(0,99) < 100:
                                        for ent in listFasTeam[self.team]:
                                            ent.specialVars["fascination"].value += 10
                                            if ent.specialVars["fascination"].value >= 100:
                                                popipo += add_effect(ent,ent,danseFasReady,skillIcon=eventFas.emoji[0][0])
                                                ent.refreshEffects()
                                                for cpmt in range(len(ent.cooldowns)):
                                                    tempi = findSkill(ent.char.skills[cmpt])
                                                    if tempi != None and findSkill(ent.char.skills[cmpt]).id == fascination.id:
                                                        ent.cooldowns[cmpt] = 0
                                                ent.specialVars["fascination"].value = 0

                                    # After damage
                                    if entityInArea.char.aspiration in [PROTECTEUR,VIGILANT,ENCHANTEUR] and self.id not in entityInArea.specialVars["aspiSlot"]:
                                        entityInArea.specialVars["aspiSlot"].append(self.id)

                                    elif self.char.aspiration == OBSERVATEUR:
                                        self.specialVars["aspiSlot"] += 3

                                    if entityInArea.isNpc("Liu") or entityInArea.isNpc("Kitsune"):
                                        popipo += add_effect(entityInArea,actTurn,charming,skillIcon = entityInArea.weapon.effect.emoji[0][0])
                                        actTurn.refreshEffects()
                                    if actTurn.isNpc("Liz") or actTurn.isNpc("Kitsune"):
                                        popipo += add_effect(actTurn,entityInArea,charming,skillIcon = actTurn.weapon.effect.emoji[0][0])
                                        actTurn.refreshEffects()

                                    for eff in entityInArea.effect:
                                        if eff.effect.id in [lightAura2ActiveEff.id, tintabuleEff.id]:                                 # Aura de lumière 2
                                            sumHeal, sumEnt = 0,[]
                                            for ent in entityInArea.cell.getEntityOnArea(area=eff.effect.area,team=entityInArea.team,wanted=ALLIES,directTarget=False):
                                                useless, tempi = eff.caster.heal(ent,eff.icon,eff.effect.stat,eff.effect.power,eff.effect.name,danger)
                                                if tempi > 0:
                                                    sumHeal += tempi
                                                    sumEnt.append(ent.icon)

                                            temp = ""
                                            for i in sumEnt:
                                                temp += i
                                            if len(sumEnt) > 0:
                                                popipo += "{0} {1} → {5} +{2} {3} PV ({4})\n".format(eff.caster.icon,eff.icon,["","≈"][len(sumEnt)>1],int(sumHeal/len(sumEnt)),eff.effect.name, temp)
                                            popipo += eff.decate(value=1)
                                            entityInArea.refreshEffects()
                                        elif eff.effect.id == flambe.id and use == STRENGTH:                         # Flambage
                                            eff.effect.power += flambe.power
                                        elif eff.effect.id == magAch.id and use == MAGIE:                            # Magia
                                            eff.effect.power += magAch.power
                                        elif eff.effect.id == rosesPhysiEff.id and use == STRENGTH:
                                            popipo += eff.triggerDamage(value = damage,declancher=self,icon=icon,onArmor=onArmor)[1]
                                        elif eff.effect.id == rosesMagicEff.id and use == MAGIE:
                                            popipo += eff.triggerDamage(value = damage,declancher=self,icon=icon,onArmor=onArmor)[1]
                                        elif eff.effect.id == haimaEffect.id:
                                            finded = False
                                            for sndEff in entityInArea.effect:
                                                if sndEff.effect.id == haimaShield.id:
                                                    finded = True
                                                    break

                                            if not(finded):
                                                popipo += add_effect(eff.caster,entityInArea,eff.effect.callOnTrigger)
                                                popipo += eff.decate(value = 1)
                                                entityInArea.refreshEffects()
                                        elif eff.effect.id in [mattSkill4Eff.id,lightLameEff.id,astralLameEff.id,timeLameEff.id]:
                                            popipo += eff.triggerDamage(value = damage,declancher=self,icon=icon,onArmor=onArmor)[1]

                                else:
                                    popipo += f"{entityInArea.char.name} esquive l'attaque\n"
                                    entityInArea.stats.dodge += 1
                                    entityInArea.stats.numberAttacked += 1
                                    if entityInArea.char.aspiration == POIDS_PLUME:
                                        entityInArea.specialVars["aspiSlot"] += 3
                                    elif self.char.aspiration == OBSERVATEUR:
                                        self.specialVars["aspiSlot"] = int(self.specialVars["aspiSlot"] * 0.5)
                                    if entityInArea.isNpc("Lia") or entityInArea.isNpc("Kitsune"):
                                        popipo += add_effect(entityInArea,actTurn,charming,skillIcon = entityInArea.weapon.effect.emoji[0][0])
                                        entityInArea.refreshEffects()

                if sumDamage > 0:
                    for eff in self.effect:
                        if eff.effect.trigger == TRIGGER_AFTER_DAMAGE:
                            if eff.effect.id == convertEff.id :                         # Convertion :
                                valueToAdd = int(sumDamage * (convertEff.power/100 * (1+(self.allStats()[convertEff.stat]/100))))
                                
                                alreadyHaveArmorEff = False
                                for eff2 in self.effect:
                                    if eff2.effect.id == convertArmor.id:
                                        alreadyHaveArmorEff = True
                                        eff2.value += valueToAdd
                                        popipo += "{0} → {1}{2} +{3} PV\n".format(eff2.caster.icon,eff2.icon,self.icon,valueToAdd)
                                        break

                                if not(alreadyHaveArmorEff):
                                    effect = convertArmor
                                    effect.overhealth = valueToAdd
                                    popipo += add_effect(eff.caster,self,effect,ignoreEndurance=True)
                                    
                                    self.refreshEffects()

                            elif eff.effect.id in [vampirismeEff.id,aliceExWeapEff]:
                                healPowa = min(self.maxHp - self.hp, int(sumDamage * (eff.effect.power/100 * (1+(self.allStats()[eff.effect.stat]/100)))))
                                temp, useless = eff.caster.heal(self,eff.icon,None,healPowa,eff.effect.name)
                                popipo += temp

                    if self.char.aspiration == BERSERK:
                        healPowa = min(self.maxHp - self.hp, min(self.char.level*10,int(sumDamage * self.specialVars["aspiSlot"]/100)))
                        temp, useless = self.heal(self,aspiEmoji[BERSERK],None,healPowa)
                        popipo += temp

                    if lifeSteal > 0:
                        healPowa = min(self.maxHp - self.hp, sumDamage * lifeSteal / 100)
                        temp, useless = self.heal(self,icon,None,healPowa)
                        popipo += temp

                if self.isNpc("Clémence pos."):
                    healPowa = min(self.maxHp - self.hp, int(sumDamage * 0.33))
                    temp, useless = self.heal(self,"",None,healPowa)
                    popipo += temp

                    self.specialVars["clemBloodJauge"].value = min(100,self.specialVars["clemBloodJauge"].value+int(sumDamage * (0.01*(1+self.level/100))))
                    if self.specialVars["clemMemCast"]:
                        self.specialVars["clemMemCast"] = False

                elif self.isNpc("Clémence Exaltée"):
                    healPowa = min(self.maxHp - self.hp, int(sumDamage * 0.2))
                    temp, useless = self.heal(self,"",None,healPowa)
                    popipo += temp

                return popipo, deathCount

            def startOfTurn(self,tablEntTeam="tabl") -> str:
                """
                    The method to call when a entity start his turn.\n
                    Reduce the duration of all their own ``fightEffects`` and return a ``string`` with the effectives changes
                """
                toReturn = ""
                allReadySeen = []
                for a in self.effect:
                    # Any normals effects --------------------------------
                    if a.trigger == TRIGGER_START_OF_TURN and (not(a.effect.stackable) or a.effect.type != TYPE_INDIRECT_DAMAGE):
                        toReturn += a.triggerStartOfTurn(danger)

                    # Stackable indirect damages effects -----------------
                        # Those effects are temporary merge into one for don't spam the action's windows
                    elif a.trigger == TRIGGER_START_OF_TURN and a.effect.stackable and a.effect.type == TYPE_INDIRECT_DAMAGE and {a.caster.id:a.effect.id} not in allReadySeen :
                        primalPower,nbOfDecate = a.effect.power,0
                        for eff in self.effect:                 # Adding the power of all sames effects by the same caster to one to have one to rule them all
                            if eff.effect.id == a.effect.id and eff.caster.id == a.caster.id:
                                a.effect.power += eff.effect.power

                        a.effect.power -= primalPower           # Deducing the base power, 'cause we are at [NbEffect]+1 * power
                        toReturn += a.triggerStartOfTurn(danger,decate=False)
                        a.effect.power = primalPower
                        
                        for eff in self.effect:
                            if eff.effect.id == a.effect.id and eff.caster.id == a.caster.id:
                                temporaty = eff.decate(value=1)
                                if temporaty != "":
                                    nbOfDecate += 1

                        if nbOfDecate > 1:                      # Regrouping all the decate messages as well
                            toReturn += "__{0}__ ne subit plus sous {1} effets de __{2}__\n".format(self.char.name,nbOfDecate,a.effect.name)
                        elif nbOfDecate == 1:
                            toReturn += temporaty

                        allReadySeen.append({a.caster.id:a.effect.id})

                    elif a.effect.id == gwenCoupeEff.id:
                        if random.randint(0,99) < 15:
                            effect = intargetable
                            toReturn += add_effect(self,self,effect)

                allReadySeenID = []
                unAffected = []
                effNames = []
                allReadySeenCharId = []

                for dictElem in self.ownEffect[:]:
                    for on, eff in dictElem.items():
                        for effOn in on.effect:
                            if effOn.id == eff:
                                temp = effOn.decate(turn=1)
                                if temp != "" :
                                    if effOn.effect.id not in allReadySeenID:
                                        allReadySeenID.append(effOn.effect.id)
                                        unAffected.append([[on.name,on.icon]])
                                        effNames.append(effOn.effect.name)
                                        allReadySeenCharId.append([on.id])
                                    else:
                                        for cmpt in range(len(allReadySeenID)):
                                            if allReadySeenID[cmpt] == effOn.effect.id and on.id not in allReadySeenCharId[cmpt]:
                                                unAffected[cmpt].append([on.name,on.icon])
                                                allReadySeenCharId[cmpt].append(on.id)

                                on.refreshEffects()
                                break

                ultimateTemp = ""

                for cmpt in range(len(allReadySeenID)):
                    tempLen = len(unAffected[cmpt])
                    if tempLen > 1:
                        for cmpt2 in range(tempLen):
                            ultimateTemp += "__{0}__".format(unAffected[cmpt][cmpt2][0])
                            if tempLen > 2 and cmpt2 < tempLen-2:
                                ultimateTemp += ", "
                            elif cmpt2 == tempLen-2:
                                ultimateTemp += " et "
                        ultimateTemp += " ne sont plus sous l'effet de __{0}__\n".format(effNames[cmpt])
                    elif tempLen == 1:
                        ultimateTemp += "__{0}__ n'est plus sous l'effet de __{1}__\n".format(unAffected[cmpt][0][0],effNames[cmpt])

                toReturn += ultimateTemp

                for a in range(7):
                    if self.cooldowns[a] > 0:
                        self.cooldowns[a] -= 1

                if self.specialVars["finalTech"] and random.randint(0,99) < 80:
                    toReturn += add_effect(self,self,pasTech,danger=danger,start=' (Final Technique)')

                if self.isNpc("Luna prê.") and self.specialVars["clemBloodJauge"] == None:
                    toRoll, roll = 20+(1-(actTurn.hp/actTurn.maxHp))*100, random.randint(0,99)
                    if roll < toRoll:
                        toReturn += add_effect(self,self,lunaQuickFightEff)

                self.refreshEffects()

                if self.isNpc("Jevil"):
                    nb = 1
                    if self.hp/self.maxHp < 0.5:
                        nb += 1
                    if self.hp/self.maxHp < 0.3:
                        nb += 1
                    cmpt = 0
                    while cmpt < nb:
                        effect = copy.deepcopy(chaosEff)

                        effect.power = [1,10,15,20,25,30][random.randint(0,5)]
                        randoma = random.randint(0,5)
                        effect.area = [AREA_CIRCLE_1,AREA_CONE_2,AREA_DIST_3,AREA_DONUT_2,AREA_LINE_2,AREA_MONO][randoma]
                        effect.name += " - {0}".format(["La croix","Le cône","L'anneau","Le cercle","La ligne","Le point"][randoma])

                        ent = tablEntTeam[0][random.randint(0,len(tablEntTeam[0])-1)]
                        if ent.hp > 0:
                            toReturn += add_effect(self,ent,effect)
                            ent.refreshEffects()
                            
                        cmpt += 1

                if self.char.weapon.id == astroGlobe.id and self.hp > 0:
                    temp = []
                    for ent in tablEntTeam[self.team]:
                        if ent.hp > 0 and type(ent.char) != invoc :
                            temp.append(ent)

                    if len(temp) > 0:
                        temp = temp[random.randint(0,len(temp)-1)]
                        toReturn += add_effect(self,temp,cardAspi[temp.char.aspiration]," ({0})".format(self.weapon.name),skillIcon = self.weapon.effect.emoji[0][0])
                        temp.refreshEffects()

                elif self.weapon.id == miltrilPlanisphere.id and self.hp > 0:
                    temp = []
                    for a in (0,1):
                        for b in tablEntTeam[a]:
                            if b.hp > 0:
                                temp.append(b)

                    if len(temp) > 1:
                        temp = temp[0]
                    else:
                        temp = random.randint(0,len(temp)-1)

                    toReturn += add_effect(self,temp,[miltrilPlanisftEffDebuff,miltrilPlanisftEffBuff][temp.team == self.team], " ({0})".format(self.weapon.name),skillIcon=self.weapon.effect.emoji[0][0])
                    temp.refreshEffects()
                return toReturn

            def endOfTurn(self,danger) -> str:
                """
                    The method to call when a entity end their turn\n
                    Return a ``string`` with all the correspondings actions
                """
                temp = ""
                for a in self.effect:
                    if a.trigger == TRIGGER_END_OF_TURN:
                        temp += a.triggerEndOfTurn(danger)
                    if a.effect.id == tablWeapExp[0].id:
                        try:
                            if random.randint(0,99) < [20,100][optionChoice==OPTION_WEAPON]:
                                for eff in tablWeapExp:
                                    if eff.name == a.effect.name:
                                        temp += add_effect(self,self,eff.callOnTrigger,skillIcon=eff.emoji[0][0])
                                        break
                        except:
                            print_exc()

                self.refreshEffects()
                if self.char.aspiration in [PROTECTEUR,VIGILANT,ENCHANTEUR]:
                    self.specialVars["aspiSlot"] = []

                if type(self.char) == invoc and (self.char.name not in ["Conviction des Ténèbres"] and not(self.char.name.startswith("Patte de The Giant Enemy Spider"))):
                    self.leftTurnAlive -= 1
                    if self.leftTurnAlive <= 0:
                        self.hp = 0
                        temp += "\n{0} est désinvoqué{1}".format(self.char.name,self.accord())
                return temp

            def atRange(self):
                """Return the entity in range of the main weapon"""
                return self.cell.getEntityOnArea(area=self.char.weapon.effectiveRange,team=self.team,wanted=self.char.weapon.target,lineOfSight= True,directTarget=True,ignoreInvoc=self.char.weapon.type==TYPE_HEAL)

            def quickEffectIcons(self):
                temp = f"{self.icon} {self.char.name} : {self.hp}/{self.maxHp} "
                if self.effect != []:
                    allReadySeenIcon, allReadySeenNumber = [], []
                    temp += "("
                    for a in self.effect:
                        if a.effect.stackable and a.icon in allReadySeenIcon:
                            for cmpt in range(len(allReadySeenIcon)):
                                if allReadySeenIcon[cmpt] == a.icon:
                                    allReadySeenNumber[cmpt] += 1
                        elif a.effect.stackable and a.icon not in allReadySeenIcon:
                            allReadySeenIcon.append(a.icon)
                            allReadySeenNumber.append(1)
                        else:
                            temp += a.icon
                    if allReadySeenIcon != []:
                        for cmpt in range(len(allReadySeenIcon)):
                            if allReadySeenNumber[cmpt] > 1:
                                temp += "{0}x{1}".format(allReadySeenIcon[cmpt],allReadySeenNumber[cmpt])
                            else:
                                temp += allReadySeenIcon[cmpt]
                    temp += ")\n"
                else:
                    temp += "\n"

                return temp

            def lightQuickEffectIcons(self):
                temp = f"{self.icon} : "
                stackableAlreaySeen = []
                if self.effect != [] and self.status != STATUS_TRUE_DEATH:
                    for eff in self.effect:
                        if eff.effect.id == "giveup":
                            return f"{self.icon} : {eff.icon} {eff.effect.name}\n"

                    if self.status == STATUS_DEAD:
                        return f"{self.icon} : <:lostSoul:887853918665707621>\n"

                    for a in self.effect:
                        if a.effect.id == lunaInfiniteDarknessStun.id:
                            return f"{self.icon} : {a.icon} {a.effect.name}\n"

                        if (a.icon not in ['<:co:888746214999339068>','<:le:892372680777539594>','<:to:905169617163538442>','<:lo:887853918665707621>','<:co:895440308257558529>']+aspiEmoji) and not(a.effect.silent and a.effect.replica == None) and a.effect.id not in [lightAura2PassiveEff.id]:
                            if a.effect.replica != None or a.effect.stun:
                                if a.effect.id != lunaInfiniteDarknessShield.id:
                                    return f"{self.icon} : {a.icon} {a.effect.name}\n"
                                else:
                                    return f"{self.icon} : {a.icon} {a.effect.name} ({a.value})\n"

                            if a.effect.stackable and (a.effect.id not in stackableAlreaySeen):
                                number = 0
                                for ent in self.effect:
                                    if ent.effect.id == a.effect.id:
                                        number += 1
                                if number > 1:
                                    if a.icon == '<:pa:930051729523879966>':
                                        temp += ['<:pt1:930051729523879966>','<:pt2:930534069576544256>','<:pt3:930534084432756738>','<:pt4:930534100324978708>','<:pt5:930534126640046118>'][number-1]
                                    else:
                                        temp += a.icon+f"({number})"
                                else:
                                    temp += a.icon

                                stackableAlreaySeen.append(a.effect.id)
                            elif not(a.effect.stackable):
                                if not(a.effect.id == eventFas.id):
                                    temp += a.icon
                                    if a.effect.id in [flambe.id,magAch.id]:
                                        temp += "("+str(a.effect.power//flambe.power)+")"
                                else:
                                    if a.value < 20:
                                        a.icon = '<:fas0:952539840157712454>'
                                    elif a.value < 40:
                                        a.icon = '<:fas20:952539890233528340>'
                                    elif a.value < 60:
                                        a.icon = '<:fas40:952539915843956796>'
                                    elif a.value < 80:
                                        a.icon = '<:fas60:952539943236935781>'
                                    else:
                                        a.icon = ["<a:fas80B:952540002011729921>","<a:fas80R:952539982680166460>"][self.team]
                                    temp += a.icon +"("+str(a.value)+")"

                    if temp != f"{self.icon} : ":
                        if self.invisible and "<:in:899788326691823656>" not in temp:
                            temp += "<:invisible:899788326691823656>"
                        if self.translucide and "<:tr:914232635176415283>" not in temp:
                            temp += "<:translucide:914232635176415283>"
                        if self.untargetable and "<:un:899610264998125589>" not in temp:
                            temp += "<:untargetable:899610264998125589>"
                        if self.immune and "<:im:914232617660981249>" not in temp:
                            temp += "<:immunite:914232617660981249>"

                        temp += "\n"
                        return temp
                    else:
                        return ""
                else:
                    return ""

            def accord(self):
                if self.char.gender == GENDER_FEMALE:
                    return "e"
                else:
                    return ""

            async def getIcon(self,bot):
                if type(self.char) == char:
                    self.icon = await getUserIcon(bot,self.char)
                else:
                    self.icon = self.char.icon
                return self.icon

            def getMedals(self,array):
                respond = ""
                tabl = [["<:topDpt:884337213670838282>","<:secondDPT:884337233241448478>","<:thirdDPT:884337256905732107>"],["<:topHealer:884337335410491394>","<:secondHealer:884337355262160937>","<:thirdHealer:884337368407093278>"],["<:topArmor:884337281547272263>","<:secondArmor:884337300975276073>","<:trdArmor:911071978163675156>"],["<:topSupp:911071783787065375>","<:sndSupp:911071803424788580>","<:trdSupp:911071819388313630>"]]
                for z in range(0,len(array)):
                    for a in (0,1,2,3):
                        try:
                            if self == array[z][a]:
                                respond+=tabl[z][a]
                                self.medals[a] += 1
                        except:
                            pass

                if respond != "":
                    return " ("+respond+")"
                else:
                    return ""

            def summon(self,summon : invoc ,timeline, cell : cell, tablEntTeam : list,tablAliveInvoc : list, ignoreLimite=False,dictInteraction:dict=None):
                funnyTempVarName = ""
                summon = copy.deepcopy(summon)
                team = self.team
                summon.color = self.char.color
                if tablAliveInvoc[team] < 3 or ignoreLimite:
                    sumEnt = entity(self.id,summon,team,False,summoner=self,dictInteraction=dictInteraction)
                    sumEnt.move(cellToMove=cell)
                    tablEntTeam[self.team].append(sumEnt)

                    if summon.name.startswith("Patte de The Giant Enemy Spider"):
                        add_effect(self,sumEnt,GESredirect)

                    if sumEnt.aspiration == POIDS_PLUME:
                        add_effect(sumEnt,sumEnt,poidPlumeEff)

                    elif sumEnt.aspiration == OBSERVATEUR:
                        add_effect(sumEnt,sumEnt,obsEff)

                    sumEnt.refreshEffects()

                    if self.id != timeline.timeline[0].id:
                        found = False
                        for cmpt in range(len(timeline.timeline)):
                            if self.id == timeline.timeline[cmpt].id and type(timeline.timeline[cmpt].char) != invoc:
                                whereToInsert = cmpt+1
                                break
                    else:
                        whereToInsert = 1

                    timeline.timeline.insert(whereToInsert,sumEnt)

                    accord = ""
                    if summon.gender == GENDER_FEMALE:
                        accord="e"
                    funnyTempVarName = f"{self.char.name} invoque un{accord} {summon.name}"
                    tablAliveInvoc[team] += 1
                    return tablEntTeam,tablAliveInvoc,timeline,funnyTempVarName

            def getElementalBonus(self,target,area : int,type : int):
                """Return the elemental damage bonus"""
                if type not in [TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_ARMOR,TYPE_INDIRECT_DAMAGE]:
                    if self.char.element in [ELEMENT_FIRE, ELEMENT_UNIVERSALIS_PREMO] and area != AREA_MONO and self.cell.distance(target.cell) > 2:
                        return 1.1
                    elif self.char.element in [ELEMENT_WATER, ELEMENT_UNIVERSALIS_PREMO] and area == AREA_MONO and self.cell.distance(target.cell) > 2:
                        return 1.1
                    elif self.char.element in [ELEMENT_AIR, ELEMENT_UNIVERSALIS_PREMO] and area != AREA_MONO and self.cell.distance(target.cell) <= 2:
                        return 1.1
                    elif self.char.element in [ELEMENT_EARTH, ELEMENT_UNIVERSALIS_PREMO] and area == AREA_MONO and self.cell.distance(target.cell) <= 2:
                        return 1.1
                elif type in [TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_ARMOR] and self.char.element == ELEMENT_LIGHT:
                    return 1.1
                elif type == TYPE_INDIRECT_DAMAGE and self.char.element == ELEMENT_DARKNESS:
                    return 1.1

                return 1

            async def resurect(self,target,value : int, icon : str,danger=danger):
                if self.team == 1:
                    value = int(value * (danger/100))
                value = min(value,target.maxHp)
                self.stats.allieResurected += 1
                self.stats.heals += value
                target.hp = value
                target.status = STATUS_RESURECTED
                if type(target.char) != char:
                    target.icon = target.char.icon
                else:
                    target.icon = await getUserIcon(bot,target.char)

                add_effect(self,target,onceButNotTwice)

                for eff in target.effect:
                    if eff.effect.id == lostSoul.id:
                        eff.decate(turn=99)

                target.refreshEffects()

                shieldValue, raiseShieldEmoji = int(target.maxHp*0.2), ['<:naB:908490062826725407>','<:naR:908490081545879673>'][target.team]
                rep = f"{self.icon} {icon} → <:renisurection:873723658315644938> {raiseShieldEmoji} +{shieldValue} PAr, {target.icon} +{value} PV\n"

                if target.char.says.onResurect != None:
                    try:
                        rep += "{0} : *\"{1}\"*\n".format(target.icon,target.char.says.onResurect.format(target=self.char.name,caster=target.char.name))
                    except:
                        rep += "__Error whith the onResurect message__\n"
                        log = format_exc()
                        if len(log) > 50:
                            rep += "{0}\n".format(log[-50:])
                        else:
                            rep += "{0}\n".format(log)

                target.raiser = self.icon

                # Recent Rez shield
                notDeadYet = classes.effect("Résurection récente","susRez",overhealth=int(target.maxHp*0.2),turnInit=3,absolutShield=True,emoji=sameSpeciesEmoji('<:naB:908490062826725407>','<:naR:908490081545879673>'))
                add_effect(self,target,notDeadYet,ignoreEndurance=True)
                if target.isNpc("Akira"):
                    mater = classes.effect("Rage Inhumaine","Akiki",strength=int(target.char.level*1.5),turnInit=-1,emoji="<a:menacing:917007335220711434>",stackable=True)
                    rep += add_effect(ent,ent,mater)
                target.refreshEffects()

                return rep

            def getAggroValue(self,target):
                """Return the aggro value agains the target. Made for be use as a key for sort lists"""
                if not(target.untargetable):
                    aggro = [20,0][type(target.char)==invoc]                                          # Base aggro value. Maybe some skills will influe on it later
                    if target.char.weapon.id == grav.id:
                        aggro += self.stats.survival

                    for eff in target.effect:                           # Change the aggro
                        aggro += eff.effect.aggro

                        if eff.effect.replica != None:
                            aggro += 25
                            break

                    distance = self.cell.distance(target.cell)          # Distance factor.
                    aggro += 40-max(distance*10,40)                     # The closer the target, the greater the aggro will be.

                    if target.char.aspiration in [BERSERK,POIDS_PLUME,ENCHANTEUR,PROTECTEUR]:       # The tanks aspirations generate more aggro than the others
                        aggro += 15

                    aggro += target.stats.damageDeal//500*5             # The more the target have deals damage, the mort aggro he will generate
                    aggro += target.stats.heals//500*5                  # The more the target have deals heals, the mort aggro he will generate
                    aggro += target.stats.shieldGived//1000*5            # The more the target have gave armor, the mort aggro he will generate

                    if self.isNpc("Luna prê."): 
                        if target.char.element == ELEMENT_DARKNESS:
                            aggro = aggro * 1.1
                        if target.char.element == ELEMENT_LIGHT or target.char.secElement in [ELEMENT_DARKNESS,ELEMENT_LIGHT]:
                            aggro = aggro * 1.05
                        
                    return int(aggro)
                else:
                    return -111

            def heal(self,target, icon : str, statUse : int, power : int, effName = None,danger=danger, mono = False, useActionStats = ACT_HEAL):
                overheath, aff, toReturn, healPowa, critMsg, diing = 0, target.hp < target.maxHp, "", 0, "", None
                if power > 0 and self.hp > 0:
                    if useActionStats == None:
                        useActionStats = ACT_HEAL
                    if statUse != None:
                        if statUse == HARMONIE:
                            temp = 0
                            for stat in self.allStats():
                                temp = max(stat,temp)
                            statUse = temp

                        else:
                            statUse = self.allStats()[statUse]

                        dangerBoost = 1
                        if self.team == 1:
                            dangerBoost = danger/100

                        secElemMul = 1
                        if self.char.secElement in [ELEMENT_FIRE, ELEMENT_UNIVERSALIS_PREMO]:
                            secElemMul += 0.05
                        elif self.char.secElement in [ELEMENT_WATER, ELEMENT_UNIVERSALIS_PREMO]:
                            secElemMul -= 0.05
                        if target.char.secElement in [ELEMENT_FIRE, ELEMENT_UNIVERSALIS_PREMO]:
                            secElemMul += 0.05
                        elif target.char.secElement in [ELEMENT_WATER, ELEMENT_UNIVERSALIS_PREMO]:
                            secElemMul -= 0.05

                        bloodPactReduc = 1
                        if target.char.aspiration == BERSERK and target.specialVars["aspiSlot"] != BERS_LIFE_STEAL:
                            bloodPactReduc -= 0.15

                        healPowa = round(power * secElemMul * (1+(max(-65,statUse-self.actionStats()[useActionStats]))/100+(target.endurance/1000))* self.valueBoost(target = target,heal=True)*self.getElementalBonus(target,area = AREA_MONO,type = TYPE_HEAL) * dangerBoost * bloodPactReduc)

                        if random.randint(0,99) < self.calHealCrit(target) * 100:
                            healPowa = int(healPowa) * (1.25 + (preciChiEff.power * int(self.specialVars["preci"]) + ironHealthEff.power * int(target.specialVars["ironHealth"])) * 0.01)
                            critMsg = " !"
                        healPowaInit = copy.deepcopy(healPowa)

                        incurableValue, undeadBonus = 0, 1
                        for eff in target.effect:
                            if eff.effect.id == incurable.id:
                                incurableValue = max(incurableValue,eff.effect.power)
                            elif eff.effect.id == undeadEff2.id:
                                undeadBonus = 1.25
                            elif eff.effect.id == kikuRezEff.id:
                                incurableValue += eff.effect.power
                            elif eff.effect.id == undeadEff2.id:
                                diing = eff
                        healPowa = int(healPowa * (100-target.healResist)/100 * (100-incurableValue)/100 * (1 + 0.006*self.level)*undeadBonus)
                        overheath = max(0,healPowa - (target.maxHp-target.hp))
                        healPowa = min(target.maxHp-target.hp,healPowa)

                        if type(self.char) != octarien:
                            target.healResist += int(healPowa/target.maxHp/2.5*100*(1+0.2*int(haveMultipleHealers[team])))
                        else:
                            target.healResist += int(healPowa/target.maxHp/1.5*100)

                        if self.isNpc("Alice Exaltée"):
                            self.specialVars["clemBloodJauge"].value = min(100,self.specialVars["clemBloodJauge"].value+int(healPowa * 0.02))
                    else:
                        incurableValue = 0
                        for eff in target.effect:
                            if eff.effect.id == incurable.id:
                                incurableValue = max(incurableValue,eff.effect.power)
                            elif eff.effect.id == undeadEff2.id:
                                diing = eff

                        healPowa = int(power * (100-target.healResist)/100 * (100-incurableValue)/100)
                        healPowa = min(target.maxHp-target.hp,healPowa)
                        healPowaInit = copy.deepcopy(healPowa)

                        if type(self.char) != octarien:
                            target.healResist += int(healPowa/target.maxHp/2.5*100)
                        else:
                            target.healResist += int(healPowa/target.maxHp/1.5*100)

                    self.stats.heals += healPowa
                    target.hp += healPowa
                    if diing != None:
                        toReturn += diing.decate(value=healPowa)
                        target.refreshEffects()

                    add = ""
                    if effName != None:
                        add = " ({0})".format(effName)

                    if healPowa > 0:
                        toReturn = f"{self.icon} {icon} → {target.icon} +{healPowa} PV{critMsg}\n"

                    if self.char.aspiration in [IDOLE,PROTECTEUR,ALTRUISTE] and overheath > 0:
                        tabli,tabla = [idoOHArmor,proOHArmor,altOHArmor],[self.specialVars["ohIdo"],self.specialVars["ohPro"],self.specialVars["ohAlt"]]
                        for carillon in (0,1,2):
                            if tabla[carillon]:
                                effect = tabli[carillon]
                                effect.overhealth = int(overheath * ([idoOHEff.power,proOHEff.power,altOHEff.power][carillon]/100))
                                toReturn += add_effect(self,target,effect,[idoOHEff.name,proOHEff.name,altOHEff.name][carillon],True)
                                target.refreshEffects()
                                return toReturn, 0

                    if self.isNpc("Lio") or self.isNpc("Kitsune"):
                        toReturn += add_effect(self,target,charming2,self.char.weapon.effect.emoji[0][0])
                        target.refreshEffects()

                    for eff in target.effect:
                        if eff.effect.id == shareTabl[0].id and mono:
                            for ent in target.cell.getEntityOnArea(area=eff.effect.area,team=target.team,wanted=ALLIES,directTarget=False):
                                tempHeal = int(min(ent.maxHp-ent.hp,healPowa*eff.effect.power/100))
                                eff.caster.stats.heals += tempHeal
                                ent.hp += tempHeal
                                add = " (Partage)"
                                if tempHeal > 0:
                                    toReturn += f"{eff.caster.icon} {eff.icon} → {ent.icon} +{tempHeal} PV{add}\n"

                if aff:
                    return toReturn, healPowa
                else:
                    return "", healPowa

            def isNpc(self, name : str) -> bool:
                """Return if the entity is a temp's with the name given"""
                return self.char.isNpc(name)

            def getCellToMove(self):
                tablOfEnt = self.cell.getEntityOnArea(area=AREA_ALL_ENEMIES-int(self.char.weapon.target==ALLIES),team=self.team,wanted=self.char.weapon.target,lineOfSight=self.char.weapon.target==ENNEMIS,ignoreInvoc = True,directTarget=True)
                if len(tablOfEnt) == 0:
                    return None
                surrondings = self.cell.surrondings()
                canMove = [surrondings[0] != None and surrondings[0].on == None, surrondings[1] != None and surrondings[1].on == None, surrondings[2] != None and surrondings[2].on == None, surrondings[3] != None and surrondings[3].on == None]

                tablOfEnt.sort(key=lambda ent:self.getAggroValue(ent))
            
                if self.cell.x - tablOfEnt[0].cell.x > 0 and canMove[0]:                # If the target is forward and we can move forward
                    return surrondings[0]
                elif self.cell.x - tablOfEnt[0].cell.x < 0 and canMove[1]:              # Elif the target is behind and we can move behind
                    return surrondings[1]
                elif self.cell.y - tablOfEnt[0].cell.y > 0 and canMove[2]:              # Elif the target is above and we can move up
                    return surrondings[2]
                elif self.cell.y - tablOfEnt[0].cell.y < 0 and canMove[3]:              # Elif the target is under and we can move down
                    return surrondings[3]
                else:
                    if canMove[2]:                                                      # Else, if we can move up, go up
                        return surrondings[2]
                    elif canMove[3]:                                                    # Else, if we can move down, go down
                        return surrondings[3]

                    else:
                        return None                                                     # Else, give up

            def knockback(self, target, power:int):
                toReturn = ""
                cellDif = (self.cell.x - target.cell.x, self.cell.y - target.cell.y)
                if cellDif[0] == 0 or cellDif[1] == 0:
                    temp = [cellDif[0] < 0, cellDif[0] > 0, cellDif[1] > 0, cellDif[1] < 0]
                    for cmpt in (0,1,2,3):
                        if temp[cmpt]:
                            axis = ["-x","+x","+y","-y"][cmpt]
                            break

                posArea = []
                for cellule in tablAllCells:
                    temp = (target.cell.x - cellule.x, target.cell.y - cellule.y)
                    if (temp[0] == 0 or temp[1] == 0) and (temp[0] != temp[1]):
                        temp2 = [temp[0] < 0, temp[0] > 0, temp[1] > 0, temp[1] < 0]
                        tablLineTeamGround = ["-x","+x","+y","-y"]
                        for cmpt in (0,1,2,3):
                            if temp2[cmpt] and axis == tablLineTeamGround[cmpt] and target.cell.distance(cellule) <= power:
                                posArea.append(cellule)
                                break

                if len(posArea) > 0:
                    posArea.sort(key=lambda dist:target.cell.distance(dist))

                cmpt = 0
                cellToPush = target.cell
                while cmpt < len(posArea) and posArea[cmpt].on == None:
                    cellToPush = posArea[cmpt]
                    cmpt += 1

                initTagetCell = target.cell
                if cellToPush != target.cell:
                    target.move(cellToMove=cellToPush)
                toReturn = "\n__{0} ({1})__ est repoussé{3} de {2} case{4} en arrière\n".format(target.char.name,target.icon,power,target.accord(),["","s"][int(power>1)])

                if cmpt < power:
                    lastingPower = power-initTagetCell.distance(cellToPush)

                    stat,damageBase = -100,10*lastingPower

                    for stats in self.allStats():
                        if not(type(self.char) == octarien and self.char.oneVAll and stats == self.allStats()[ENDURANCE]):
                            stat = max(stats,stat)

                    badaboum = [target]
                    if cmpt < len(posArea) and posArea[cmpt].on != None:
                        badaboum.append(posArea[cmpt].on)
                    for boom in badaboum:
                        damage = damageBase * (1+(stat/100)) * (1-(min(95,boom.resistance*(1-self.percing/100))/100)) * self.getElementalBonus(boom,AREA_MONO,TYPE_INDIRECT_DAMAGE) * (1+(0.01*self.level))
                        toReturn += self.indirectAttack(boom,value=damage,name="Collision")

                return toReturn

            def jumpBack(self, power:int, fromCell:cell):
                toReturn = ""

                cellDif = (self.cell.x - fromCell.x, self.cell.y - fromCell.y)
                if cellDif[0] == 0 or cellDif[1] == 0:
                    temp = [cellDif[0] < 0, cellDif[0] > 0, cellDif[1] > 0, cellDif[1] < 0]
                    for cmpt in (0,1,2,3):
                        if temp[cmpt]:
                            axis = ["-x","+x","+y","-y"][cmpt]
                            break

                posArea = []
                for cellule in tablAllCells:
                    temp = (self.cell.x - cellule.x, self.cell.y - cellule.y)
                    if (temp[0] == 0 or temp[1] == 0) and (temp[0] != temp[1]):
                        temp2 = [temp[0] < 0, temp[0] > 0, temp[1] > 0, temp[1] < 0]
                        tablLineTeamGround = ["+x","-x","-y","+y"]
                        for cmpt in (0,1,2,3):
                            if temp2[cmpt] and axis == tablLineTeamGround[cmpt] and self.cell.distance(cellule) <= power:
                                posArea.append(cellule)
                                break

                if len(posArea) > 0:
                    posArea.sort(key=lambda dist:self.cell.distance(dist))

                cmpt = 0
                cellToPush = self.cell
                while cmpt < len(posArea) and posArea[cmpt].on == None:
                    cellToPush = posArea[cmpt]
                    cmpt += 1

                initTagetCell = self.cell
                if cellToPush != self.cell:
                    self.move(cellToMove=cellToPush)
                toReturn = "\n__{0} ({1})__ saute de {2} case{4} en arrière\n".format(self.char.name,self.icon,power,self.accord(),["","s"][int(power>1)])

                if cmpt < power:
                    lastingPower = power-initTagetCell.distance(cellToPush)

                    stat,damageBase = -100,10*lastingPower

                    for stats in self.allStats():
                        stat = max(stats,stat)

                    badaboum = [self]
                    if cmpt < len(posArea) and posArea[cmpt].on != None:
                        badaboum.append(posArea[cmpt].on)
                    for boom in badaboum:
                        damage = damageBase * (1+(stat/100)) * (1-(min(95,boom.resistance*(1-self.percing/100))/100)) * self.getElementalBonus(boom,AREA_MONO,TYPE_INDIRECT_DAMAGE) * (1+(0.01*self.level))
                        toReturn += self.indirectAttack(boom,value=damage,name="Collision")

                return toReturn

            def quickEvent(self, stat:int, required:int,danger:int=100, effIfFail: classes.effect = None, fromEnt=None):
                toReturn = "\n__Maneuvre Critique !__"

                required = required*0.2 + (required*0.8/50*self.char.level)
                sussessTaux = min(1000,1000 * (self.allStats()[stat]/required))

                if random.randint(0,999) < sussessTaux:
                    toReturn += "\n{0} a réussi sa maneuvre critique !".format(self.char.name)
                    return toReturn, True
                else:
                    toReturn += "\n{0} a échoué sa maneuvre critique...\n".format(self.char.name)
                    if effIfFail != None:
                        toReturn += add_effect(fromEnt,self,effIfFail,danger=danger)
                        self.refreshEffects()
                        return toReturn, False

            def actionStats(self):
                return [self.negativeHeal, self.negativeBoost, self.negativeShield, self.negativeDirect, self.negativeIndirect]

            def calHealCrit(self,target):
                """Return the crit rate (on 1), for a crit shield or heal"""
                bonus = (preciChiEff.power * int(self.specialVars["preci"]) + ironHealthEff.power * int(target.specialVars["ironHealth"])) * 0.01
                return self.precision * 0.002 + self.critical * 0.01 + target.endurance * 0.001 + bonus

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

            def getActTurn(self) -> entity:
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

        class fightEffect:
            """Classe plus pousée que Effect pour le combat"""
            def __init__(self,id,effect : classes.effect, caster : entity, on : entity, turnLeft : int, trigger : int, type : int, icon : str, value=1, effReducPurcent:Union[None,int]=None):
                """self.id : int -> Id de l'effet
                self.effect : effect -> L'effet de base
                self.caster : entity -> L'entité qui donne l'effet
                self.on : entity -> L'entité sur laquel se trouve cet effet
                self.turnLeft : int -> Nombre de tour restant à l'effet
                self.trigger : const -> L'événement qui déclanche l'effet
                self.icon : str -> L'id de l'emoji correspondant à l'effet"""
                self.effect: classes.effect = copy.deepcopy(effect)

                if effReducPurcent != None:
                    self.effect.power = int(self.effect.power*effReducPurcent/100)
                else:
                    effReducPurcent = 100
                self.caster:entity = caster
                self.on:entity = on
                self.turnLeft = turnLeft
                self.trigger = trigger
                self.type = type
                self.value = value
                self.id = id
                self.icon = icon
                self.remove = False
                self.stun:bool = effect.stun
                self.name = effect.name
                self.replicaTarget: Union[None,entity] = None

                tablTemp = [0,0,0,0,0,0,0,0,0]

                if self.caster.char.element == ELEMENT_TIME and self.effect.type == TYPE_INDIRECT_HEAL:
                    self.effect.power = int(self.effect.power*1.2)

                if self.effect.stat != None:
                    if self.effect.stat is not HARMONIE:
                        temp = self.caster.allStats()[self.effect.stat]
                    else:
                        temp = -111
                        for a in self.caster.allStats():
                            temp = max(temp,a)

                    valueBoost, valueResis = (1 + self.caster.char.level//10/10 - 1 + caster.valueBoost(on)) * (temp+100-self.caster.negativeBoost)/100, caster.valueBoost(on) * (temp+100-self.caster.negativeShield)/100

                else:
                    valueBoost, valueResis = 1, 1

                secElemMul = 0

                if caster.char.secElement in [ELEMENT_AIR, ELEMENT_UNIVERSALIS_PREMO]:
                    secElemMul += 0.05
                if on.char.secElement in [ELEMENT_AIR, ELEMENT_UNIVERSALIS_PREMO]:
                    secElemMul += 0.05

                if caster.char.element in [ELEMENT_SPACE]:
                    secElemMul += 0.1
                elif on.char.element in [ELEMENT_SPACE] and caster.team == on.team:
                    secElemMul += 0.05
                elif on.char.element in [ELEMENT_SPACE] and caster.team != on.team:
                    secElemMul -= 0.05

                valueBoost += secElemMul

                tablTemp[0] += self.effect.strength * valueBoost * effReducPurcent * 0.01
                tablTemp[1] += self.effect.endurance * valueBoost * effReducPurcent * 0.01
                tablTemp[2] += self.effect.charisma * valueBoost * effReducPurcent * 0.01
                tablTemp[3] += self.effect.agility * valueBoost * effReducPurcent * 0.01
                tablTemp[4] += self.effect.precision * valueBoost * effReducPurcent * 0.01
                tablTemp[5] += self.effect.intelligence * valueBoost * effReducPurcent * 0.01
                tablTemp[6] += self.effect.resistance * valueBoost * effReducPurcent * 0.01
                tablTemp[7] += self.effect.percing * valueBoost * effReducPurcent * 0.01
                tablTemp[8] += self.effect.critical * valueBoost * effReducPurcent * 0.01

                self.inkResistance = min(effect.inkResistance * valueResis,effect.inkResistance*3)

                self.tablAllStats = tablTemp
                self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.resistance,self.percing,self.critical = tuple(tablTemp)

                if self.effect.id in [vulne.id,dmgDown.id,dmgUp.id,defenseUp.id] and self.effect.stat != None:
                    power = self.effect.power
                    secElemMul = 1
                    if caster.char.secElement in [ELEMENT_AIR, ELEMENT_UNIVERSALIS_PREMO]:
                        secElemMul += 0.05
                    if on.char.secElement in [ELEMENT_AIR, ELEMENT_UNIVERSALIS_PREMO]:
                        secElemMul += 0.05
                    self.effect.power = power * (100+caster.allStats()[self.effect.stat]-caster.negativeBoost)/100 * (self.caster.char.level//10/10 - 1 + caster.valueBoost(on))

            def decate(self,turn=0,value=0) -> str:
                """Réduit le leftTurn ou value de l'effet"""
                self.turnLeft -= turn
                self.value -= value
                temp = ""

                if (self.turnLeft <= 0 and self.effect.turnInit > 0) or self.value <= 0 and not(self.effect.unclearable):
                    if self.trigger == TRIGGER_ON_REMOVE:
                        temp += self.triggerRemove()
                    self.remove = True
                    if not(self.effect.silent) and self.on.hp > 0 and self.effect.id not in (astralShield.id,timeShield.id):
                        temp += f"__{self.on.char.name}__ n'est plus sous l'effet __{self.effect.name}__\n"

                    if self.effect.id == undeadEff2.id and self.turnLeft == 0:
                        self.on.hp = 0
                        temp += self.on.death(killer=self.on)
                return temp

            def triggerDamage(self,value=0,icon="",declancher = 0,onArmor = 1) -> list:
                """Déclanche l'effet"""
                value = round(value)
                temp2 = [value,""]
                if self.type == TYPE_ARMOR and value >0:
                    valueT = valueT2 = round(value)
                    if not(self.effect.absolutShield):
                        secElemMul = 1
                        if self.on.char.secElement in [ELEMENT_EARTH, ELEMENT_UNIVERSALIS_PREMO]:
                            secElemMul += 0.05
                        if self.caster.char.secElement in [ELEMENT_EARTH, ELEMENT_UNIVERSALIS_PREMO]:
                            secElemMul += 0.05
                        valueT2 = round(value * onArmor * secElemMul)

                    value = round(min(valueT2,self.value))
                    self.decate(value=value)
                    declancher.stats.damageOnShield += value
                    self.caster.stats.armoredDamage += value
                    if self.value <= 0:
                        reduc = self.on.char.level
                        if self.caster.specialVars["osPre"]:
                            reduc = reduc + self.caster.char.level * (preOSEff.power/100)
                        elif self.caster.specialVars["osIdo"] or self.caster.specialVars["osPro"]:
                            reduc = reduc + self.caster.char.level * (idoOSEff.power/100)
                        if self.effect.lightShield:
                            reduc = 0
                        reduc = int(reduc)
                        ratio = valueT/valueT2
                        funnyTempVarName = valueT2 - value - reduc
                        funnyTempVarNameButTheSecond = int(funnyTempVarName * ratio)
                        temp2 = [max(0,funnyTempVarNameButTheSecond), ["<:abB:934600555916050452> ","<:abR:934600570633867365> "][self.on.team] + "-" + str(value)+" PAr "]
                    elif value > 0:
                        temp2 = [0,f"{self.icon} -{value} PAr "]
                    else:
                        temp2 = [0,self.icon]

                elif self.effect.redirection > 0 and value > 0 and self.caster.hp > 0:
                    valueT = value
                    redirect = int(valueT * self.effect.redirection/100)
                    valueT = valueT - redirect
                    declancher.indirectAttack(target=self.caster,value=redirect,icon=icon,ignoreImmunity=False,name=self.effect.name)
                    temp2 = [valueT,"{0} -{1} PV".format(self.caster.icon,redirect)]

                elif (self.type == TYPE_INDIRECT_DAMAGE or self.effect.id in [rosesPhysiEff.id,rosesMagicEff.id,lightLameEff.id,astralLameEff.id,timeLameEff.id,mattSkill4Eff.id]) and self.value>0:
                    if self.effect.onDeclancher:
                        target = declancher
                    else:
                        target = self.on

                    variable = ""
                    damageBase = self.effect.power
                    if self.effect.stat == None:
                        stat = None
                    else:
                        stat = self.caster.allStats()[self.effect.stat]-self.caster.negativeIndirect

                    whoTarget = ALLIES
                    if target.team == self.caster.team and target != self.caster:
                        whoTarget = ENNEMIS

                    for a in target.cell.getEntityOnArea(area=self.effect.area,team=target.team,wanted=whoTarget,directTarget=False):
                        reduc = 1
                        if a != target:
                            reduc = max(AOEMINDAMAGE,1-target.cell.distance(a.cell)*AOEDAMAGEREDUCTION)

                        if stat != None:
                            damage = damageBase * (1+(stat/100)) *  (1-(min(95,a.resistance*(1-self.caster.percing/100))/100)) * reduc * self.caster.getElementalBonus(a,self.effect.area,TYPE_INDIRECT_DAMAGE) * (1+(0.01*self.on.level))
                        else:
                            damage = damageBase

                        variable += self.caster.indirectAttack(a,value=damage,icon = self.icon,name=self.effect.name)
                    temp2[1] = f"{variable}{self.decate(value=1)}"

                elif self.type == TYPE_UNIQUE:
                    if self.effect.id == enchant.id :
                        self.effect.magie += 5

                if self.effect.callOnTrigger != None:
                    temp2[1] = ""
                    if self.effect.id != "nt":
                        for a in [0,1]:
                            for b in tablEntTeam[a]:
                                if type(b.char) != invoc and b.id == self.on.id:
                                    temp2[1] += add_effect(self.caster,b,findEffect(self.effect.callOnTrigger))
                                    
                                    b.refreshEffects()
                                    break
                        temp2[1] += f"{self.decate(value=1)}"
                    else:
                        temp2[1] += add_effect(self.caster,declancher,findEffect(self.effect.callOnTrigger))
                        
                        declancher.refreshEffects()

                return temp2

            def triggerDeath(self,killer=None) -> str:
                """Déclanche l'effet"""
                toReturn = ""
                if self.type==TYPE_INDIRECT_REZ:
                    self.on.status = STATUS_RESURECTED
                    self.caster.stats.allieResurected += 1

                    if self.effect.stat == None:
                        heal = self.effect.power

                    elif self.effect.stat == PURCENTAGE:
                        heal = round(self.on.maxHp * self.effect.power /100)

                    self.on.hp = heal
                    self.caster.stats.heals += heal
                    toReturn += f"{self.on.char.name} ({self.on.icon}) est réanimé{self.on.accord()} !\n{self.caster.icon} {self.icon}→ {self.on.icon} +{heal} PV\n"
                    self.decate(value=1)

                elif self.type == TYPE_INDIRECT_DAMAGE and self.value>0:
                    variable = ""
                    stat,damageBase = self.caster.allStats()[self.effect.stat]-self.caster.negativeIndirect,self.effect.power
                    if self.effect.stat == None:
                        stat = None
                    
                    whoTarget = ALLIES
                    if self.on.team == self.caster.team and self.on != self.caster:
                        whoTarget = ENNEMIS

                    for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.on.team,wanted=whoTarget,directTarget=False):
                        reduc = 1
                        if a != self.on:
                            reduc = max(AOEMINDAMAGE,1-self.on.cell.distance(a.cell)*AOEDAMAGEREDUCTION)

                        if stat != None:
                            damage = damageBase * (1+(stat/100)) *  (1-(min(95,a.resistance*(1-self.caster.percing/100))/100)) * (reduc) * self.caster.getElementalBonus(a,self.effect.area,TYPE_INDIRECT_DAMAGE) * (1+(0.01*self.on.level))

                        variable += self.caster.indirectAttack(a,value=damage,icon = self.icon)
                    toReturn += f"L'effet __{self.effect.name}__ se déclanche :\n{variable}{self.decate(value=1)}"

                elif self.type == TYPE_UNIQUE:
                    if self.effect == hunter:
                        add_effect(self.on,self.on,hunterBuff)
                        self.on.refreshEffects()
                        tempi, useless = self.on.attack(target=killer,value = self.on.char.weapon.power,icon = self.on.char.weapon.emoji,onArmor=self.on.char.weapon.onArmor)
                        toReturn += tempi

                if self.effect.callOnTrigger != None:
                    toReturn += add_effect(self.on,self.on,findEffect(self.effect.callOnTrigger))
                    

                self.decate(value=1)

                return toReturn

            def triggerStartOfTurn(self,danger,decate=True) -> str:
                """Déclanche l'effet"""
                funnyTempVarName=""
                if self.type == TYPE_INDIRECT_HEAL and self.on.hp > 0:              # Heal Indirect
                    if self.effect.area == AREA_MONO:
                        funnyTempVarName, useless = self.caster.heal(self.on,self.icon,self.effect.stat,self.effect.power,self.effect.name,danger,mono=True)
                    else:
                        for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.caster.team,wanted=ALLIES,directTarget=False):
                            funnyTempVarName, useless = self.caster.heal(a,self.icon,self.effect.stat,self.effect.power,self.effect.name,danger)

                elif self.type == TYPE_INDIRECT_DAMAGE and self.value > 0 and ((self.effect.area==AREA_MONO and self.on.hp > 0) or self.effect.area != AREA_MONO):            # Damage indirect
                    variable,damage = "",0
                    if self.effect.stat != None:
                        if self.effect.stat != HARMONIE:
                            stat,damageBase = self.caster.allStats()[self.effect.stat]-self.caster.negativeIndirect,self.effect.power
                        else:
                            stat = -100
                            for staty in self.caster.allStats():
                                stat = max(stat,staty)
                            damageBase = self.effect.power
                        whoTarget = ALLIES
                        if self.on.team == self.caster.team and self.on != self.caster:
                            whoTarget = ENNEMIS

                        for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.on.team,wanted=whoTarget,directTarget=False):
                            if a == None:
                                raise Exception("Error while triggering {0} on {1} : The cell say than there is nobody on it ?\nYou should investigate that, Léna".format(self.effect.name,self.on.char.name))
                            selfElem = self.caster.getElementalBonus(a,self.effect.area,TYPE_INDIRECT_DAMAGE)
                            areaMul = 1
                            if a != self.on:
                                areaMul = max(AOEMINDAMAGE,1-self.on.cell.distance(a.cell)*AOEDAMAGEREDUCTION)
                            damage = damageBase * (1+(stat/100)) *  (1-(min(95,a.resistance*(1-self.caster.percing/100))/100)) * areaMul * selfElem * (1+(0.01*self.on.level))
                            variable += self.caster.indirectAttack(a,value=damage,icon = self.icon,name=self.effect.name)

                            if self.effect.id == estal.id and damage != 0:
                                self.caster.stats.estialba += damage
                            elif self.effect.id == bleeding.id and damage != 0:
                                self.caster.stats.bleeding += damage

                        funnyTempVarName = variable

                        if decate:
                            funnyTempVarName += self.decate(value=1)
                    else:
                        for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.caster.team,wanted=ENNEMIS,directTarget=False):
                            damage = self.effect.power
                            variable += self.caster.indirectAttack(a,value=damage,icon = self.icon,name=self.effect.name)
                        
                        funnyTempVarName = variable
                        if decate:
                            funnyTempVarName += self.decate(value=1)

                    if self.effect.id == lieSkillEff.id and self.value > 0:
                        effTemp = lieSkillEff
                        effTemp.turnInit,effTemp.lvl = self.turnLeft, self.value

                        funnyTempVarName += add_effect(self.caster,self.on,effTemp)
                        self.on.refreshEffects()

                    if self.effect.id == infection.id:                              # If it's the infection poisonnus effect
                        tempTabl = self.on.cell.getEntityOnArea(area=AREA_DONUT_1,team=self.on.team,wanted=ALLIES,effect=[infection],directTarget=False)
                        if len(tempTabl) > 0:
                            funnyTempVarName += "L'infection se propage...\n"
                            for ent in tempTabl:
                                funnyTempVarName += add_effect(self.caster,ent,infection)
                                add_effect(self.caster,ent,infectRej)
                                ent.refreshEffects()

                elif self.type == TYPE_BOOST and self.on.hp > 0:                    # Indirect Armor
                    funnyTempVarName += add_effect(self.caster,self.on,findEffect(self.effect.callOnTrigger))
                    self.on.refreshEffects()
                return funnyTempVarName

            def triggerEndOfTurn(self,danger) -> str:
                """Trigger the effect"""
                temp = ""
                if self.type == TYPE_INDIRECT_DAMAGE:                               # The only indirect damage effect for now is a insta death
                    if self.effect.stat == None:
                        temp += self.caster.indirectAttack(target=self.on,ignoreImmunity=self.effect.ignoreImmunity ,value=self.effect.power)
                        self.decate(value=1)
                    elif self.value > 0 and ((self.effect.area==AREA_MONO and self.on.hp > 0) or self.effect.area != AREA_MONO):
                        variable,damage = "",0
                        if self.effect.stat != HARMONIE:
                            stat,damageBase = self.caster.allStats()[self.effect.stat]-self.caster.negativeIndirect,self.effect.power
                        else:
                            stat = -100
                            for staty in self.caster.allStats():
                                stat = max(stat,staty)
                            damageBase = self.effect.power
                        whoTarget = ALLIES
                        if self.on.team == self.caster.team:
                            whoTarget = ENNEMIS

                        for ent in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.on.team,wanted=whoTarget,directTarget=False):
                            if ent == None:
                                raise Exception("Error while triggering {0} on {1} : The cell say than there is nobody on it ?\nYou should investigate that, Léna".format(self.effect.name,self.on.char.name))
                            selfElem = self.caster.getElementalBonus(ent,self.effect.area,TYPE_INDIRECT_DAMAGE)
                            areaMul = 1
                            if ent != self.on:
                                areaMul = max(AOEMINDAMAGE,1-self.on.cell.distance(ent.cell)*AOEDAMAGEREDUCTION)
                            damage = damageBase * (1+(stat/100)) *  (1-(min(95,ent.resistance*(1-self.caster.percing/100))/100)) * areaMul * selfElem * (1+(0.01*self.on.level))
                            variable += self.caster.indirectAttack(ent,value=damage,icon = self.icon,name=self.effect.name)

                            if self.effect.id == estal.id and damage != 0:
                                self.caster.stats.estialba += damage
                            elif self.effect.id == bleeding.id and damage != 0:
                                self.caster.stats.bleeding += damage

                            temp = variable + self.decate(value=1)

                elif self.type == TYPE_UNIQUE:                                      # Poids Plume effect bonus reduce
                    if self.effect == poidPlumeEff:
                        self.value = self.value//2

                elif self.type == TYPE_INDIRECT_HEAL and self.on.hp > 0:            # End of turn healing (aka Light Aura 1)
                    for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.caster.team,wanted=ALLIES,directTarget=False):
                        tempi, useless = self.caster.heal(a,self.icon,self.effect.stat,self.effect.power,self.effect.name,danger)
                        temp += tempi

                return temp

            def triggerRemove(self) -> str:
                """Trigger the effect when it's removed\n
                For now, only unique effect activly use it, but some boost effect use it to"""

                if not(self.effect.silent):
                    message = f'L\'effet __{self.effect.name}__ se déclanche :\n'
                else:
                    message = ""
                if self.type == TYPE_UNIQUE:
                    if self.effect.id == lostSoul.id:                                   # Remove the body effect
                        if self.on.status == STATUS_DEAD and not(aliceMemCastTabl[self.on.team]):
                            self.on.status = STATUS_TRUE_DEATH
                            message="{0} en avait marre d'attendre une résurection et a quitté le combat\n".format(self.on.char.name)
                        elif aliceMemCastTabl[self.on.team]:                                          # If there is a Alice Memento cast, do not remove the body
                            self.turnLeft += 1

                    elif self.effect.id in [flambe.id,magAch.id]:
                        stat,damageBase = self.caster.allStats()[self.effect.stat]-self.caster.negativeIndirect,self.effect.power

                        selfElem = self.caster.getElementalBonus(self.on,self.effect.area,TYPE_INDIRECT_DAMAGE)
                        damage = damageBase * (1+(stat/100)) *  (1-(min(95,self.on.resistance*(1-self.caster.percing/100))/100)) * selfElem

                        message += self.caster.indirectAttack(self.on,value=damage,icon = self.icon,name=self.effect.name)

                if self.effect.callOnTrigger != None:                               # If the effect give another effect when removed, give that another effect
                    for a in [0,1]:
                        for b in tablEntTeam[a]:
                            if type(b.char) != invoc and b.id == self.on.id:
                                message += add_effect(self.caster,b,findEffect(self.effect.callOnTrigger))
                                
                                b.refreshEffects()
                                if findEffect(self.effect.callOnTrigger).id == temNativTriggered.id:
                                    self.on.icon, self.on.char.icon = '<:colegue:895440308257558529>','<:colegue:895440308257558529>'
                                break

                return message

            def allStats(self):
                return self.tablAllStats

        def add_effect(caster: entity,target: entity,effect: classes.effect,start: str = "", ignoreEndurance=False, danger=danger, setReplica : Union[None,entity] = None, effPowerPurcent=100, useActionStats = ACT_SHIELD, skillIcon=""):
            """Méthode qui rajoute l'effet Effet à l'entity Target lancé par Caster dans la liste d'attente des effets"""
            valid,id,popipo = False,0,""
            valid = True
            turn = caster.stats.survival
            if effect.id == elemEff.id:
                effect = tablElemEff[caster.char.element]

            # Does the effect can be applied ?
            if effect.reject != None:                                           # The effect reject other effects
                for a in effect.reject:
                    for b in target.effect:
                        if a == b.effect.id:
                            popipo = f"{caster.icon} {effect.emoji[caster.char.species-1][caster.team]} → 🚫{findEffect(a).emoji[caster.char.species-1][caster.team]} {target.icon}\n"
                            valid = False
                            break
                    if not(valid):
                        break
            for a in target.effect:
                if a.effect.id == effect.id and not(effect.stackable):          # The effect insn't stackable
                    if a.effect.id == incurable.id:                                 # But is't Healn't
                        if a.effect.power < effect.power:                               # A better Healn't
                            diff = effect.power - a.effect.power
                            a.effect.power = effect.power
                            a.caster = caster
                            popipo = f"{caster.icon} → {a.effect.emoji[caster.char.species-1][caster.team]}+{diff} {target.icon}\n"
                        valid = False

                    elif a.effect.id in [idoOHArmor.id,proOHArmor.id,altOHArmor.id]:  # Overhealth Shield
                        if a.value < effect.overhealth:                               # A better Overhealth shield
                            diff = effect.overhealth - a.value
                            a.value = effect.overhealth
                            a.caster = caster
                            a.leftTurn = effect.turnInit
                            popipo = f"{caster.icon} {effect.emoji[caster.char.species-1][caster.team]} → {a.effect.emoji[caster.char.species-1][caster.team]}+{diff} {target.icon}\n"
                        valid = False

                    elif not(effect.silent):                                        # It's not Healn't
                        popipo = f"{caster.icon} {effect.emoji[caster.char.species-1][caster.team]} → 🚫{a.effect.emoji[caster.char.species-1][caster.team]} {target.icon}\n"
                        valid = False

                    else:
                        valid = False

            if valid:
                valid = False
                while not(valid):                                               # Why Léna. Why ?
                    id = random.randint(0,maxsize)                  # Ok, I use them now
                    valid = id not in allEffectInFight

                icon = effect.emoji[caster.char.species-1][caster.team]
                if effect.id == darkFlumPoi.id:
                    effect = darkFlumPoi
                    effect.power = int(caster.char.level * 0.2)

                if effect.overhealth > 0:                                       # Armor Effect
                    temp = caster.allStats()
                    value, critMsg = effect.overhealth, ""
                    friablility = max(1-(turn / 30),0.1)                   # Reduct over time
                    if useActionStats == None:
                        useActionStats = ACT_SHIELD

                    dangerBoost = 1
                    if caster.team == 1:
                        dangerBoost = danger/100

                    secElemMul = 1
                    if caster.char.secElement in [ELEMENT_FIRE, ELEMENT_UNIVERSALIS_PREMO]:
                        secElemMul -= 0.05
                    elif caster.char.secElement in [ELEMENT_WATER, ELEMENT_UNIVERSALIS_PREMO]:
                        secElemMul += 0.05
                    if target.char.secElement in [ELEMENT_FIRE, ELEMENT_UNIVERSALIS_PREMO]:
                        secElemMul -= 0.05
                    elif target.char.secElement in [ELEMENT_WATER, ELEMENT_UNIVERSALIS_PREMO]:
                        secElemMul += 0.05

                    if effect.stat != None:                                         # Classical armor effect
                        if effect.stat == HARMONIE:
                            maxi = -100
                            for randomVar in temp:
                                maxi = max(maxi,randomVar)

                            value = round(effect.overhealth * secElemMul * caster.valueBoost(target=target,armor=True) * (maxi-caster.actionStats()[useActionStats] +100)*((target.endurance+1250)/1250)/100 * friablility * dangerBoost * (0.8 + 0.01*caster.level))
                        else:
                            value = round(effect.overhealth * secElemMul * caster.valueBoost(target=target,armor=True) * (temp[effect.stat]-caster.actionStats()[useActionStats] +100)*((target.endurance+1250)/1250)/100 * friablility * dangerBoost * (0.8 + 0.01*caster.level))

                        if random.randint(0,99) < caster.calHealCrit(target) * 100:
                            value = int(value * (1.25 + (preciChiEff.power * int(caster.specialVars["preci"]) + ironHealthEff.power * int(target.specialVars["ironHealth"])) * 0.01))
                            critMsg = " !"
                    else:                                                           # Fixe armor effect
                        value = round(effect.overhealth)

                    if not(effect.absolutShield):
                        for a in target.effect:
                            if a.type == TYPE_ARMOR and not(effect.lightShield):
                                reduc = 0.5
                                if caster.specialVars["osPre"]:
                                    reduc = reduc + reduc * (preOSEff.power/2/100)
                                elif caster.specialVars["osIdo"] or caster.specialVars["osPro"]:
                                    reduc = reduc + reduc * (idoOSEff.power/2/100)

                                value = round(value*reduc)
                                break

                    caster.stats.shieldGived += value

                    toAppend = fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,TYPE_ARMOR,icon,value)
                    if setReplica != None:
                        toAppend.replicaTarget = setReplica

                    addEffect.append(toAppend)

                    if not(effect.silent):
                        tempTurn = effect.turnInit+int(caster.char==ELEMENT_TIME)
                        popipo = f"{caster.icon} {skillIcon} → {target.icon} {icon} +{value} PAr{critMsg}\n"

                else:                                                           # Any other effect
                    if effPowerPurcent == 100:
                        effPowerPurcent = None
                    toAppend = fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,effect.type,icon,effect.lvl,effPowerPurcent)
                    if setReplica != None:
                        toAppend.replicaTarget = setReplica
                    if effect.id == undeadEff2.id:
                        toAppend.value = target.maxHp
                    addEffect.append(toAppend)

                    if effect.id == "clemBloodJauge":
                        caster.specialVars["clemBloodJauge"] = toAppend

                    if not(effect.silent):
                        power = ["", " ({0}%)".format(effPowerPurcent)][effPowerPurcent!=None]
                        popipo = f"{caster.icon} {skillIcon} → {target.icon} +{icon} __{effect.name}__{power}\n"

                    target.refreshEffects()

                    tablTemp = [altOHEff.id,proOHEff.id,idoOHEff.id,idoOSEff.id,proOSEff.id,preOSEff.id,heriteEstialbaEff.id,heriteLesathEff.id,floorTanking.id,summonerMalus.id,foulleeEff.id,preciChiEff.id,ironHealthEff.id]
                    nameTemp = ["ohAlt","ohPro","ohIdo","osIdo","osPro","osPre","heritEstial","heritLesath","tankTheFloor","summonerMalus","foullee","preci","ironHealth"]
                    tablTempEff = [physicRuneEff.id,magicRuneEff.id, eventFas.id]
                    nameTempEff = ["damageSlot","damageSlot","fascination"]

                    for funnyVarName in range(len(tablTemp)):
                        if effect.id == tablTemp[funnyVarName]:
                            target.specialVars["{0}".format(nameTemp[funnyVarName])] = True
                            break

                    for funnyVarName in range(len(tablTempEff)):
                        if effect.id == tablTempEff[funnyVarName]:
                            target.specialVars["{0}".format(nameTempEff[funnyVarName])] = toAppend
                            break

                    if effect.id == estal.id and caster.specialVars["heritEstial"]:                               # If is the Estialba effect
                        effect = estal2
                        icon = effect.emoji[caster.char.species-1][caster.team]

                        popipo += f"{caster.icon} {heriteEstialba.emoji} → {target.icon} +{icon} __{effect.name}__\n"
                        target.refreshEffects()

                    elif effect.id == bleeding.id and caster.specialVars["heritLesath"] :                         # If is the hemorragic effect
                        effect=bleeding2
                        icon = effect.emoji[caster.char.species-1][caster.team]
                        addEffect.append(fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,effect.type,icon,effect.lvl))

                        popipo += f"{caster.icon} {heriteLesath.emoji} → {target.icon} +{icon} __{effect.name}__\n"
                        target.refreshEffects()

                    elif effect.id == bloodPactEff.id:
                        caster.specialVars["aspiSlot"] = BERS_LIFE_STEAL * (bloodPactEff.power/100 +1)
                    elif effect.id == partnerIn.id:
                        tempTabl = tablEntTeam[caster.team]
                        tempTabl.sort(key=lambda chocolatine: getPartnerValue(chocolatine.char),reverse=True)


                        if tempTabl[0] == caster:
                            tempTabl.remove(caster)

                        if len(tempTabl) > 0:
                            effect, icon = partnerOut, partnerOut.emoji[0][0]
                            addEffect.append(fightEffect(id,effect,caster,tempTabl[0],effect.turnInit,effect.trigger,effect.type,icon,effect.lvl))
                            popipo += f"{caster.icon} {partner.emoji} → {tempTabl[0].icon} +{icon} __{effect.name}__\n"
                            tempTabl[0].refreshEffects()
                            caster.specialVars["partner"] = tempTabl[0]
                    elif effect.id == eventFas.id:
                        listFasTeam[target.team].append(target)

            if target.hp > 0:
                return popipo
            else:
                return ''

        def map():
            """Renvoie un str contenant la carte du combat"""
            line1,line2,line3,line4,line5 = [None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None]
            lines = [line1,line2,line3,line4,line5]

            if bigMap:
                line6, line7 = [None,None,None,None,None,None],[None,None,None,None,None,None]
                lines.append(line6)
                lines.append(line7)

            for a in tablAllCells:
                if isLenapy or True:
                    temp = '<:em:866459463568850954>'
                else:
                    temp = f'{str(a.x)}:{str(a.y)}'                         # Show cells ID
                if a.on != None:
                    if a.on.status == STATUS_DEAD:
                        temp = ['<:ls:868838101752098837>','<:ls:868838465180151838>'][a.on.team]
                    elif a.on.status != STATUS_TRUE_DEATH:
                        if a.on.invisible:                              # If the entity is invisible, don't show it. Logic
                            temp = '<:em:866459463568850954>'
                        else:
                            temp = a.on.icon
                    else:
                        a.on = None

                lines[a.y][a.x]=temp

            temp = ""
            for a in lines:
                for b in [0,1,2,3,4]:
                    temp += f"{a[b]}|"
                temp += f"{a[b+1]}\n"

            return temp

        def getHealAggro(on : entity, skillToUse : Union[skill,weapon]):
            if on.hp < 0 or on.hp >= on.maxHp:
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

                incurValue = 0
                for eff in on.effect:
                    if eff.effect.id == incurable.id:
                        incurValue = max(eff.effect.power,incurValue)

                prio = prio * (1-(incurValue/2/100))                                # Same with the healing reduce effects
                return prio

        def getHealTarget(tablTeam : List[entity], skillToUse : skill):
            if len(tablTeam) == 1:
                return tablTeam[0]
            elif len(tablTeam) < 1:
                raise AttributeError("tablTeam is empty")
            
            temp = tablTeam
            temp.sort(key=lambda funnyTempVarName:getHealAggro(funnyTempVarName,skillToUse),reverse=True)
            return temp[0]

        def groupAddEffect(caster:entity, target:entity,area:Union[int,List[entity]],effect:List[classes.effect],skillIcon="",actionStats=ACT_BOOST,effPurcent=100):
            tablName, tablEff, tablIcon, toReturn = [], [], [], ""
            if type(effect) != list:
                effect = [effect]

            for c in effect:
                eff = findEffect(c)
                if eff != None:
                    if type(area) == int:
                        tablToSee = target.cell.getEntityOnArea(area=area,team=caster.team,wanted=[ENNEMIS,ALLIES][eff.type in [TYPE_BOOST,TYPE_ARMOR,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ]],directTarget=False)
                    else:
                        tablToSee = area
                    for ent in tablToSee:
                        ballerine = add_effect(caster,ent,eff,useActionStats=actionStats,skillIcon=skillIcon,effPowerPurcent=effPurcent)
                        if eff.type == TYPE_ARMOR:
                            toReturn += ballerine
                        else:
                            if '🚫' not in ballerine and ballerine != "":
                                if eff.name not in tablEff:
                                    tablEff.append(eff.name)
                                    tablIcon.append(eff.emoji[caster.char.species-1][caster.team])
                                    tablName.append(ent.icon)
                                else:
                                    for cmpt in range(len(tablEff)):
                                        if tablEff[cmpt] == eff.name:
                                            tablName[cmpt]+=ent.icon
                                            break
                        ent.refreshEffects()

            if tablEff != []:
                temp = ""
                if effPurcent != 100 and effPurcent != None:
                    temp = " ({0}%)".format(int(effPurcent))
                for cmpt in range(len(tablEff)):
                    toReturn += "{1} {2} → {3} +{0} __{4}__{5}\n".format(tablIcon[cmpt],caster.icon,skillIcon,tablName[cmpt],tablEff[cmpt],temp)

            return toReturn

        # =============================================== Pre fight things ================================================

        logs += "Fight triggered by {0}\n".format(ctx.author.name)
        logs += "\n=========\nTeams filling phase\n=========\n\n"
        leni = len(team1)

        for tmp in team1:
            if type(tmp) == tmpAllie:
                for cmpt in tablIsPnjName:
                    if tmp.isNpc(cmpt):
                        dictIsPnjVar[f"{cmpt}"] = True
                        break

        # Teams generations -----------------------------------------------
        if len(team1) < [8,16][bigMap] and not(octogone) and not(procurFight): # Remplisage de la team1
            aleaMax = len(tablAllAllies)-1
            alreadyFall = []
            lvlMax = 0

            for a in team1:
                lvlMax = max(lvlMax,a.level)

            copyTablTemp = copy.deepcopy(tablAllAllies)

            while len(team1) < [8,16][bigMap]:
                vacantRole = ["DPT1","DPT2","Healer","Booster"]

                for perso in team1:
                    if perso.aspiration in [BERSERK,TETE_BRULE,OBSERVATEUR,POIDS_PLUME,ENCHANTEUR,MAGE] and ("DPT1" in vacantRole):
                        vacantRole.remove("DPT1")
                    elif perso.aspiration in [BERSERK,TETE_BRULE,OBSERVATEUR,POIDS_PLUME,ENCHANTEUR,MAGE] and ("DPT2" in vacantRole):
                        vacantRole.remove("DPT2")
                    elif perso.aspiration in [IDOLE,PROTECTEUR] and ("Booster" in vacantRole):
                        vacantRole.remove("Booster")
                    elif perso.aspiration in [PREVOYANT,ALTRUISTE] and ("Healer" in vacantRole):
                        vacantRole.remove("Healer")

                tablToSee = []
                if len(vacantRole) <= 0:
                    tablToSee = copyTablTemp
                else:
                    for role in vacantRole:
                        if role in ["DPT1","DPT2"]:
                            for allie in copyTablTemp:
                                if allie.aspiration in [BERSERK,TETE_BRULE,OBSERVATEUR,POIDS_PLUME,ENCHANTEUR,MAGE]:
                                    tablToSee.append(allie)
                        elif role == "Healer":
                            for allie in copyTablTemp:
                                if allie.aspiration in [PREVOYANT,ALTRUISTE]:
                                    tablToSee.append(allie)
                        elif role == "Booster":
                            for allie in copyTablTemp:
                                if allie.aspiration in [IDOLE,PROTECTEUR]:
                                    tablToSee.append(allie)

                temp = random.randint(0,len(tablToSee)-1)
                alea = tablToSee[temp]
                copyTablTemp.remove(alea)

                if alea.isNpc("Lena") and random.randint(0,99) < 25:
                    alea = copy.deepcopy(findAllie("Luna"))
                elif alea.isNpc("Gwendoline"):
                    bidule = random.randint(0,99)
                    if bidule < 33:
                        alea = copy.deepcopy(findAllie("Klironovia"))
                    elif bidule < 66:
                        alea = copy.deepcopy(findAllie("Altikia"))
                elif alea.isNpc("Shushi") and random.randint(0,99) < 25:
                    alea = copy.deepcopy(findAllie("Shihu"))

                for cmpt in tablIsPnjName:
                    if alea.isNpc(cmpt):
                        dictIsPnjVar[f"{cmpt}"] = True
                        break

                alea.changeLevel(lvlMax)
                autoHead = getAutoStuff(alea.stuff[0],alea)
                autoBody = getAutoStuff(alea.stuff[1],alea)
                autoShoe = getAutoStuff(alea.stuff[2],alea)
                alea.stuff = [autoHead,autoBody,autoShoe]
                if alea.level < 10:
                    alea.element = ELEMENT_NEUTRAL
                elif alea.level < 20 and alea.element in [ELEMENT_SPACE,ELEMENT_TIME,ELEMENT_LIGHT,ELEMENT_DARKNESS]:
                    alea.element = ELEMENT_NEUTRAL

                team1 += [alea]

                logs += "{0} have been added into team1 ({1}, {2}, {3})\n".format(alea.name,autoHead.name,autoBody.name,autoShoe.name)

        if team2 == []: # Génération de la team 2
            lvlMax = 0
            winStreak = teamWinDB.getVictoryStreak(team1[0])
            for a in team1:
                lvlMax = max(lvlMax,a.level)

            altDanger = [40,45,50,55,60,65,70,75,80,85,90,100]

            if random.randint(0,99) > 10+winStreak or (leni < 8 and not(team1[0].isNpc("Luna prê."))): # Vs normal team
                danger = dangerLevel[winStreak]

                aleaMax = len(tablAllEnnemies)-1
                alreadyFall = []

                tablOctaTemp:List[octarien] = copy.deepcopy(tablAllEnnemies)
                oneVAll, leniOcta = False, len(team1)

                tablTeamOctaPos = [0,0,1,1,2,2]+[random.randint(0,2),random.randint(0,2)]
                tablTeamOctaComp = [4,2,2]

                random.shuffle(tablTeamOctaPos)
                if len(team2) < len(team1) and lvlMax >= 15 and not(procurFight):
                    if random.randint(0,99) < 20:               # Boss ?
                        temp = random.randint(0,len(tablBoss)-1)
                        alea = copy.deepcopy(tablBoss[temp])
                        #alea = copy.deepcopy(findEnnemi("Kiku"))

                        if alea.oneVAll:
                            oneVAll = True

                        alea.changeLevel(lvlMax)
                        team2.append(alea)
                        logs += "{0} have been added into team2\n".format(alea.name)

                        if alea.isNpc("Luna prê."):
                            canAdd, nbValidSkill = True, 3 + int(lvlToUnlockSkill[3] <= lvlMax) + int(lvlToUnlockSkill[4] <= lvlMax) + int(lvlToUnlockSkill[5] <= lvlMax) + int(lvlToUnlockSkill[6] <= lvlMax)
                            for perso in team1:
                                if perso.level >= lvlMax - 10:
                                    nbShieldSkill = 0
                                    for cmpt in perso.skills:
                                        if type(cmpt) == classes.skill and cmpt.type == TYPE_ARMOR:
                                            nbShieldSkill += 1
                                    if nbShieldSkill > nbValidSkill // 2:
                                        canAdd = False
                                        break

                            if canAdd:
                                alea = copy.deepcopy(findAllie("Shushi Cohabitée"))
                                alea.changeLevel(lvlMax)

                                team1.append(alea)
                                logs += "{0} have been added into team1\n".format(alea.name)

                            alea = copy.deepcopy(findAllie("Iliana"))
                            alea.changeLevel(lvlMax)
                            alea.stuff = [getAutoStuff(alea.stuff[0],alea),getAutoStuff(alea.stuff[1],alea),getAutoStuff(alea.stuff[2],alea)]
                            alea.says = ilianaSaysVsLuna

                            team1.append(alea)
                            logs += "{0} have been added into team1\n".format(alea.name)

                        if alea.isNpc("Clémence pos."):
                            canAdd, nbValidSkill = True, 3 + int(lvlToUnlockSkill[3] <= lvlMax) + int(lvlToUnlockSkill[4] <= lvlMax) + int(lvlToUnlockSkill[5] <= lvlMax) + int(lvlToUnlockSkill[6] <= lvlMax)
                            for perso in team1:
                                if perso.level >= lvlMax - 10:
                                    nbShieldSkill = 0
                                    for cmpt in perso.skills:
                                        if type(cmpt) == classes.skill and cmpt.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL]:
                                            nbShieldSkill += 1
                                    if nbShieldSkill > nbValidSkill // 2:
                                        canAdd = False
                                        break
                            
                            if canAdd:
                                alea = copy.deepcopy(findAllie("Alice Exaltée"))
                                alea.changeLevel(lvlMax)

                                team1.append(alea)
                                logs += "{0} have been added into team1\n".format(alea.name)

                    elif random.randint(0,99) < 5:              # Kitsune sisters ?
                        logs += "Kitsune Sisters Roll Sussed\n"
                        for name in ["Liu","Lia","Lio","Liz"]:
                            for alea in tablOctaTemp[:]:
                                if alea.isNpc(name):
                                    tablOctaTemp.remove(alea)
                                    alea.changeLevel(lvlMax)
                                    team2.append(alea)
                                    logs += "{0} have been added into team2\n".format(alea.name)
                                    break

                for octa in tablOctaTemp[:]:
                    if octa.baseLvl > lvlMax:
                        tablOctaTemp.remove(octa)

                octoRolesNPos = [[[],[],[]],[[],[],[]],[[],[],[]]] # 0 : Dmg; 1 : Heal/Armor; 2 : Buff/Debuff

                for octa in tablOctaTemp:
                    if octa.aspiration in [BERSERK, POIDS_PLUME, MAGE, ENCHANTEUR, OBSERVATEUR, TETE_BRULE,SORCELER,ATTENTIF]:
                        roleId = 0
                    elif octa.aspiration in [ALTRUISTE, PREVOYANT]:
                        roleId = 1
                    elif octa.aspiration in [IDOLE,INOVATEUR, PROTECTEUR, VIGILANT]:
                        roleId = 2
                    else:
                        roleId = random.randint(0,2)

                    octoRolesNPos[roleId][octa.weapon.range].append(octa)

                for octa in team2:
                    if octa.aspiration in [BERSERK, POIDS_PLUME, MAGE, ENCHANTEUR, OBSERVATEUR, TETE_BRULE]:
                        roleId = 0
                    elif octa.aspiration in [ALTRUISTE, PREVOYANT]:
                        roleId = 1
                    elif octa.aspiration in [IDOLE, PROTECTEUR]:
                        roleId = 2
                    else:
                        roleId = random.randint(0,2)

                    tablTeamOctaComp[roleId] -= 1
                    try:
                        tablTeamOctaPos.remove(octa.weapon.range)
                    except:
                        pass

                if lvlMax > 20 and not(procurFight):
                    while len(team2) < min(8,len(team1)) and not(oneVAll):
                        alea = None
                        for tempCmpt in range(len(tablTeamOctaComp)):
                            if tablTeamOctaComp[tempCmpt] > 0 and len(octoRolesNPos[tempCmpt][tablTeamOctaPos[0]]) > 0:
                                break

                        for secondCmpt in range(len(tablTeamOctaPos)):
                            if len(octoRolesNPos[tempCmpt][tablTeamOctaPos[secondCmpt]]) > 0:
                                break

                        if len(octoRolesNPos[tempCmpt][tablTeamOctaPos[secondCmpt]]) > 1:
                            alea = octoRolesNPos[tempCmpt][tablTeamOctaPos[secondCmpt]][random.randint(0,len(octoRolesNPos[tempCmpt][tablTeamOctaPos[secondCmpt]])-1)]
                        else:
                            try:
                                alea = octoRolesNPos[tempCmpt][tablTeamOctaPos[secondCmpt]][0]
                            except:
                                pass
                        
                        if alea != None:
                            octoRolesNPos[tempCmpt][tablTeamOctaPos[secondCmpt]].remove(alea)
                            tablTeamOctaPos.remove(tablTeamOctaPos[secondCmpt])
                            tablTeamOctaComp[tempCmpt] -= 1

                            if alea.isNpc("Octaling"):
                                alea = copy.deepcopy(alea)
                                alea.weapon = weapons[random.randint(0,len(weapons)-1)]
                                alea.aspiration = random.randint(0,len(inspi)-1)
                                temp2 = copy.deepcopy(skills)
                                for cmpt in range(7):
                                    rand = random.randint(0,len(temp2)-1)
                                    alea.skills[cmpt] = temp2[rand]
                                    temp2.remove(temp2[rand])
                                alea.element = random.randint(0,len(elemNames)-1)

                            alea.changeLevel(lvlMax)
                            
                            team2.append(alea)
                            logs += "{0} have been added into team2\n".format(alea.name)

                else:
                    while len(team2) < [len(team1),random.randint(8,15)][procurFight] and not(oneVAll) and len(tablOctaTemp)>0:
                        if len(tablOctaTemp) > 1:
                            alea = tablOctaTemp[random.randint(0,len(tablOctaTemp)-1)]
                        else:
                            alea = tablOctaTemp[0]              
                        tablOctaTemp.remove(alea)

                        if alea.isNpc("Octaling"):
                            alea = copy.deepcopy(alea)
                            alea.weapon = weapons[random.randint(0,len(weapons)-1)]
                            alea.aspiration = random.randint(0,len(inspi)-1)
                            temp2 = copy.deepcopy(skills)
                            for cmpt in range(7):
                                rand = random.randint(0,len(temp2)-1)
                                alea.skills[cmpt] = temp2[rand]
                                temp2.remove(temp2[rand])
                            alea.element = random.randint(0,len(elemNames)-1)

                        alea.changeLevel(lvlMax)
                        
                        team2.append(alea)
                        logs += "{0} have been added into team2\n".format(alea.name)

            else: # Vs temp ally team

                lvlMax, temp = 0, team1
                temp.sort(key=lambda funnyTempVarName: funnyTempVarName.level,reverse=True)

                tablAllieTemp, leniAllie, danger, lvlMax = copy.deepcopy(tablAllAllies), len(team1), altDanger[winStreak], temp[0].level

                tablTeamAlliePos = [0,0,1,1,2,2]+[random.randint(0,2),random.randint(0,2)]
                tablTeamAllieComp = [4,2,2]

                random.shuffle(tablTeamAlliePos)
                allieRolesNPos = [[[],[],[]],[[],[],[]],[[],[],[]]] # 0 : Dmg; 1 : Heal/Armor; 2 : Buff/Debuff

                for allie in tablAllieTemp:
                    if allie.aspiration in [BERSERK, POIDS_PLUME, MAGE, ENCHANTEUR, OBSERVATEUR, TETE_BRULE, SORCELER, ATTENTIF]:
                        roleId = 0
                    elif allie.aspiration in [ALTRUISTE, PREVOYANT]:
                        roleId = 1
                    elif allie.aspiration in [IDOLE, INOVATEUR, PROTECTEUR, VIGILANT]:
                        roleId = 2
                    else:
                        roleId = random.randint(0,2)

                    allieRolesNPos[roleId][allie.weapon.range].append(allie)

                for allie in team2:
                    if allie.aspiration in [BERSERK, POIDS_PLUME, MAGE, ENCHANTEUR, OBSERVATEUR, TETE_BRULE]:
                        roleId = 0
                    elif allie.aspiration in [ALTRUISTE, PREVOYANT]:
                        roleId = 1
                    elif allie.aspiration in [IDOLE, PROTECTEUR]:
                        roleId = 2
                    else:
                        roleId = random.randint(0,2)

                    tablTeamAllieComp[roleId] -= 1
                    try:
                        tablTeamAlliePos.remove(allie.weapon.range)
                    except:
                        pass

                while len(team2) < max(8,len(team1)):
                    for tempCmpt in range(len(tablTeamAllieComp)):
                        if tablTeamAllieComp[tempCmpt] > 0 and len(allieRolesNPos[tempCmpt][tablTeamAlliePos[0]]) > 0:
                            break

                    for secondCmpt in range(len(tablTeamAlliePos)):
                        if len(allieRolesNPos[tempCmpt][tablTeamAlliePos[secondCmpt]]) > 0:
                            break

                    alea = None
                    if len(allieRolesNPos[tempCmpt][tablTeamAlliePos[secondCmpt]]) > 1:
                        alea = allieRolesNPos[tempCmpt][tablTeamAlliePos[secondCmpt]][random.randint(0,len(allieRolesNPos[tempCmpt][tablTeamAlliePos[secondCmpt]])-1)]
                    else:
                        try:
                            alea = allieRolesNPos[tempCmpt][tablTeamAlliePos[secondCmpt]][0]
                        except:
                            pass

                    if alea != None:
                        allieRolesNPos[tempCmpt][tablTeamAlliePos[secondCmpt]].remove(alea)
                        tablTeamAlliePos.remove(tablTeamAlliePos[secondCmpt])
                        tablTeamAllieComp[tempCmpt] -= 1
                    else:
                        logs += "\nHum... Something gone wrong... So hum... emergency procedure"
                        emergencyTemp = tablAllAllies[:]
                        for a in team2:
                            for b in emergencyTemp[:]:
                                if a.name == b.name:
                                    emergencyTemp.remove(b)

                        alea=emergencyTemp[random.randint(0,len(emergencyTemp)-1)]

                    if alea.isNpc("Lena") and random.randint(0,99) < 25:
                        alea = copy.deepcopy(findAllie("Luna"))
                    elif alea.isNpc("Shushi") and random.randint(0,99) < 25:
                        alea = copy.deepcopy(findAllie("Shihu"))
                    elif alea.isNpc("Gwendoline"):
                        alea = copy.deepcopy(findAllie(["Gwendoline","Klironovia","Altikia"][random.randint(0,2)]))
                    elif alea.isNpc("Anna") and random.randint(0,99) < 25:
                        alea = copy.deepcopy(findAllie("Belle"))
                    alea.changeLevel(lvlMax)

                    team2.append(alea)
                    logs += "{0} have been added into team2\n".format(alea.name)

            for enemy in team2:
                for cmpt in tablIsPnjName:
                    if enemy.isNpc(cmpt):
                        dictIsPnjVar[f"{cmpt}"] = True
                        break

        if (now.day,now.month) == (19,1):
            ent = copy.deepcopy(findAllie("Lena"))
            ent.changeLevel(55+random.randint(0,14))
            team1.append(ent)

        # Updating the Danger and Team Fighting status
        if octogone:
            danger=100
        else:
            winStreak = teamWinDB.getVictoryStreak(team1[0])

        tablTeam,tablEntTeam,cmpt = [team1,team2],[[],[]],0
        readyMsg,cmpt,nbHealers = None,0, [0,0]

        for a in [0,1]:                 # Entities generations and stats calculations
            for b in tablTeam[a]:
                if auto == False and b.species != 3:
                    try:
                        await bot.fetch_user(b.owner)
                        ent = entity(cmpt,b,a,auto=False,dictInteraction=dictIsPnjVar)
                    except:
                        ent = entity(cmpt,b,a,danger=danger,dictInteraction=dictIsPnjVar)
                else:  
                    ent = entity(cmpt,b,a,danger=danger,dictInteraction=dictIsPnjVar)

                tablEntTeam[a].append(ent)
                ent.recalculate()
                await ent.getIcon(bot=bot)

                if not(haveMultipleHealers[a]) and type(ent.char) not in [octarien, invoc]:
                    nbSkill, nbHealSkill = 0,0
                    for skilly in ent.char.skills:
                        if type(skilly) == classes.skill:
                            nbSkill += 1
                            if skilly.type in [TYPE_HEAL, TYPE_INDIRECT_HEAL]:
                                nbHealSkill += 1
                    
                    if nbHealSkill >= nbSkill//2:
                        nbHealers[a] += 1
                        if nbHealers[a] >= [2,4][bigMap]:
                            haveMultipleHealers[a] = True
                cmpt+=1

        if msg == None:
            try:
                msg = await ctx.send(embed = await getRandomStatsEmbed(bot,team1,text=["Chargement...","Combat rapide en cours de génération..."][int(auto)]))
            except:
                msg = await ctx.channel.send(embed = await getRandomStatsEmbed(bot,team1,text=["Chargement...","Combat rapide en cours de génération..."][int(auto)]))

        else:
            if ctx.channel.last_message_id != msg.id and not(auto):
                await msg.delete()
                msg = await ctx.channel.send(embed = await getRandomStatsEmbed(bot,team1,text=["Chargement...","Combat rapide en cours de génération..."][int(auto)]))
            else:
                await msg.edit(embed = await getRandomStatsEmbed(bot,team1,text=["Chargement...","Combat rapide en cours de génération..."][int(auto)]))

        if not(auto):                   # Send the first embed for the inital "Vs" message and start generating the message
            if not(octogone):
                for team in listImplicadTeams:
                    teamWinDB.changeFighting(team,msg.id,ctx.channel.id,team2)

            logs += "\n"
            versus = ""
            for a in [0,1]:
                logs += "\nTeam {0} composition :\n".format(a+1)
                versus+=f"\n__Equipe {a+1} :__\n"
                for b in tablEntTeam[a]:
                    versus+=f"{b.icon} {b.char.name}\n"
                    logs += "{0}\n".format(b.char.name)

        # Placement phase -----------------------------------------------------
        logs += "\n=========\nInitial placements phase\n=========\n\n"
        tablLineTeamGround, placementlines, allAuto, maxPerLine = [[0,1,2],[3,4,5]], [[[],[],[]],[[],[],[]]], True, [5,7][bigMap]

        for actTeam in [0,1]:                     # Sort the entities and place them
            melee, dist, snipe, lenMel, lenDist, lenSnip = [],[],[],0,0,0

            for b in tablEntTeam[actTeam]:
                verif = b.char.weapon.range
                if verif == 0:
                    melee += [b]
                    lenMel += 1
                elif verif == 1:
                    dist += [b]
                    lenDist += 1
                else:
                    snipe += [b]
                    lenSnip += 1

            tablEntOnLine,tablNbEntOnLine = [[snipe,dist,melee],[melee,dist,snipe]][actTeam],[[lenSnip,lenDist,lenMel],[lenMel,lenDist,lenSnip]][actTeam]

            for b in [[2,1],[0,1]][actTeam]:
                if tablNbEntOnLine[b] > maxPerLine:
                    tablEntOnLine[b+[-1,1][actTeam]] += tablEntOnLine[b][maxPerLine:]
                    tablEntOnLine[b] = tablEntOnLine[b][0:maxPerLine]

            if tablNbEntOnLine[[0,2][actTeam]] > maxPerLine:
                tablEntOnLine[1] += tablEntOnLine[[0,2][actTeam]][maxPerLine:]
                tablEntOnLine[[0,2][actTeam]] = tablEntOnLine[[0,2][actTeam]][:maxPerLine]

                if len(tablEntOnLine[1]) > maxPerLine:
                    random.shuffle(tablEntOnLine[1])
                    tablEntOnLine[[2,0][actTeam]] += tablEntOnLine[1][maxPerLine:]
                    tablEntOnLine[1] = tablEntOnLine[1][:maxPerLine]
            
            if actTeam == 0:
                placementlines[actTeam]=[snipe,dist,melee]
            else:
                placementlines[actTeam]=[melee,dist,snipe]

            tablNbEntOnLine[0],tablNbEntOnLine[1],tablNbEntOnLine[2],lineVal = len(tablEntOnLine[0]),len(tablEntOnLine[1]),len(tablEntOnLine[2]),0

            for xLinePos in tablLineTeamGround[actTeam]:
                random.shuffle(tablEntOnLine[lineVal])

                if not(bigMap):
                    if (actTeam == 1 and xLinePos % 3 == 0) or (actTeam == 0 and xLinePos % 3 == 2):
                        tablSetPos = [
                                [],
                                [2],
                                [1,3],
                                [1,2,3],
                                [0,1,3,4],
                                [0,1,2,3,4]
                            ]

                        try:
                            if len(tablEntOnLine[lineVal]) != len(tablSetPos[len(tablEntOnLine[lineVal])]):
                                raise Exception((len(tablEntOnLine[lineVal]),len(tablSetPos[len(tablEntOnLine[lineVal])])))
                        except:
                            first = "\nlen(tablEntOnLine[lineVal]) = "
                            if lineVal < len(tablEntOnLine):
                                first += str(len(tablEntOnLine[lineVal]))
                            else:
                                first += "__OoR__"
                            second = "\nlen(tablSetPos[len(tablEntOnLine[lineVal])]) = "
                            if lineVal < len(tablEntOnLine) and len(tablEntOnLine[lineVal]) < len(tablSetPos):
                                second += str(len(tablSetPos[len(tablEntOnLine[lineVal])]))
                            else:
                                second += "__OoR__"
                            await msg.edit(embed=discord.Embed(title="__Error during placement phase__",description=format_exc()+"\ncmpt = {0}\nlen(tablEntOnLine) = {1}\nlen(tablSetPos) = {2}{3}{4}\n\nFinghting status reset".format(lineVal,len(tablEntOnLine),len(tablSetPos),first,second)))
                            for team in listImplicadTeams:
                                teamWinDB.changeFighting(team,0)
                            return 0
                        for pos in range(len(tablSetPos[len(tablEntOnLine[lineVal])])):
                            tablEntOnLine[lineVal][pos].move(y=tablSetPos[len(tablEntOnLine[lineVal])][pos],x=xLinePos)
                            logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(tablEntOnLine[lineVal][pos].char.name,0,0,xLinePos,tablSetPos[len(tablEntOnLine[lineVal])][pos])

                    else:
                        if tablNbEntOnLine[lineVal] == 1:
                            tablEntOnLine[lineVal][0].move(y=random.randint(1,3),x=xLinePos)
                            logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(tablEntOnLine[lineVal][0].char.name,0,0,xLinePos,2)

                        else:
                            tabl = [0,1,2,3,4]

                            for cmpt2 in range(tablNbEntOnLine[lineVal]):
                                if len(tabl) > 1:
                                    rand = random.randint(0,len(tabl)-1)
                                else:
                                    rand = 0
                                ruby = tabl[rand]
                                tabl.remove(ruby)
                                tablEntOnLine[lineVal][cmpt2].move(y=ruby,x=xLinePos)
                                logs += "{0} has been place at {1}:{2}\n".format(tablEntOnLine[lineVal][0].char.name,xLinePos,ruby)

                else:
                    prePos = [
                        [   # Team 1 set pos
                            [[0,3],[1,2],[2,1],[3,0],[1,4],[2,5],[3,6]],
                            [[1,3],[2,2],[3,1],[4,0],[2,4],[3,5],[4,6]],
                            [[2,3],[3,2],[4,1],[5,0],[3,4],[4,5],[5,6]]
                        ],
                        [   # Team 2 set pos
                            [[3,3]],
                            [[4,3]],
                            [[5,3]]
                        ]
                    ][actTeam]

                    for cmpt in range(len(tablEntOnLine[lineVal])):
                        if len(prePos[lineVal]) > 1:
                            rand = random.randint(0,len(prePos[lineVal])-1)
                        else:
                            rand = 0
                        ruby = prePos[lineVal][rand]
                        prePos[lineVal].remove(ruby)
                        tablEntOnLine[lineVal][cmpt].move(y=ruby[1],x=ruby[0])
                        logs += "{0} has been place at {1}:{2}\n".format(tablEntOnLine[lineVal][0].char.name,ruby[0],ruby[1])

                lineVal += 1

        if not(auto):                       # Edit the Vs embed for his message
            repEmb = discord.Embed(title = "__Ce combat oppose :__",color = light_blue, description="{0}\n\n__Carte__ :\n{1}".format(versus,map()))
            repEmb.add_field(name = "__Taux de danger :__",value=danger,inline=False)
            await msg.edit(embed = repEmb)

        choiceMsg = 0
        if not(auto):                       # User there ?
            allReady = False
            already, awaited,awaitedChar = [],[],[]

            readyMsg = await ctx.channel.send(embed= await getRandomStatsEmbed(bot,team1))

            for a in tablEntTeam: # Génération du tableau des utilisateurs devant confirmer leur présence
                for b in a:
                    if b.auto == False:
                        owner = None
                        try:
                            owner = await ctx.guild.fetch_member(b.char.owner)
                        except:
                            b.auto = True
                        
                        if owner != None:
                            awaitedChar += [b]
                            awaited += [owner]

            dateLimite = datetime.now() + timedelta(seconds=15)
            while not(allReady): # Demande aux utilisateurs de confirmer leur présence
                readyEm = discord.Embed(title = "Combat manuel",color=light_blue)
                readyEm.set_footer(text="Les utilisateurs n'ayant pas réagis dans les 15 prochaines secondes seront considérés comme combattant automatiques")
                temp,temp2 = "",""
                for a in already:
                    temp2+= a.mention + ", "
                    
                if temp2 == "":
                    temp2 = "-"

                for a in awaited:
                    temp += a.mention + ", "

                readyEm.add_field(name = "Prêts :",value = temp2,inline = False)
                readyEm.add_field(name = "En attente de :",value = temp,inline = False)
                await readyMsg.edit(embed = readyEm)
                await readyMsg.add_reaction(emoji.check)

                def checkIsIntendedUser(reaction,user):
                    mes = reaction.message == readyMsg and str(reaction) == emoji.check

                    for a in awaited:
                        if user == a and mes:
                            return True

                try:
                    timeLimite = (dateLimite - datetime.now()).total_seconds()
                    react = await bot.wait_for("reaction_add",timeout = timeLimite,check = checkIsIntendedUser)
                except:
                    break

                awaited.remove(react[1])
                already += [react[1]]
                allAuto = False

                if choiceMsg == 0:
                    choiceMsg = await ctx.channel.send(embed=await getRandomStatsEmbed(bot,team1,"Fenêtre de sélection de l'action"))

                if awaited == []:
                    allReady = True


            await readyMsg.clear_reactions()
            temp,awaitNum,temp2= "",len(awaited),""
            if awaitNum == 1:
                temp = awaited[0].mention
            elif awaitNum == 2:
                temp = f"{awaited[0].mention} et {awaited[1].mention}"
            elif awaitNum != 0:
                for a in range(0,awaitNum-2):
                    temp+=f"{awaited[a].mention}, "
                temp += f"{awaited[a+1].mention} et {awaited[a+2].mention}"
            else:
                temp = "-"

            if awaitNum != 0:
                temp2 = f"\n\n{temp} seront considérés comme combattants automatiques"
            statingEmb = discord.Embed(title = "Initialisation",color = light_blue,description = f"Le combat va commencer {emoji.loading}{temp2}")

            await readyMsg.edit(embed = statingEmb)

            for z in awaitedChar:
                for b in awaited:
                    if b.id == int(z.char.owner):
                        z.auto = True
                        break

        # Timeline's initialisation -----------------------------------------
        tempTurnMsg = "__Début du combat :__"
        if not(auto):
            turnMsg = readyMsg
            await turnMsg.clear_reactions()
        time = timeline()
        time, tablEntTeam = time.init(tablEntTeam)

        logs += "\n=========\nStuffs passives effects phase\n=========\n\n"
        for team in [0,1]:                                  # Says Start
            for ent in tablEntTeam[team]:
                if tablEntTeam[1][0].isNpc("The Giant Enemy Spider") and (ent.isNpc("Alice") or ent.isNpc("Félicité") or ent.isNpc("Lohica")):
                    tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"!?")
                    arch = classes.effect("Arachnophobie","archacnophobia",type=TYPE_MALUS,strength=-int(ent.baseStats[STRENGTH]*0.2),charisma=-int(ent.baseStats[CHARISMA]*0.2),magie=-int(ent.baseStats[MAGIE]*0.2),agility=-int(ent.baseStats[AGILITY]*0.2),intelligence=-int(ent.baseStats[INTELLIGENCE]*0.2),turnInit=-1,unclearable=True)
                    tempTurnMsg += add_effect(tablEntTeam[1][0],ent,arch)
                    ent.refreshEffects()

                elif ent.char.says.start != None and random.randint(0,99)<33:
                    if ent.isNpc("Alice"):                          # Alice specials interractions
                        if dictIsPnjVar["Hélène"]:                                    # Helene in the fight
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"__Arf, pourquoi je dois faire équipe avec elle déjà (＃￣0￣) ?__")
                            if dictIsPnjVar["Clémence"]:
                                if random.randint(0,99) < 50:
                                    tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:clemence:908902579554111549>',"__S'il te plait Alice, commence pas... Elle fait même pas le même taff que toi.__")
                                    if dictIsPnjVar["Lena"]:
                                        tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:lena:909047343876288552>',"Je sais que c'est tentant de se parler avec des ultra-sons quand on a votre ouïe, mais si vous pôuviez plutôt vous concentrer sur le combat ce sera cool")
                                else:
                                    tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:clemence:908902579554111549>',"Je l'ai entendue celle là !")
                    
                        elif dictIsPnjVar["Félicité"] and dictIsPnjVar["Sixtine"] and dictIsPnjVar["Clémence"]:         # All sisters in the fight
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"Allez ! Un p'tit combat en famille !")

                        elif dictIsPnjVar["Félicité"] or dictIsPnjVar["Sixtine"]:                         # A sister in the fight (except Clémence)
                            tempMsg = "Allez Féli ! On fonce !"
                            if dictIsPnjVar["Sixtine"]:
                                tempMsg = "Courrage Sixtine ! Ça va aller !"

                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,tempMsg)
                        else:
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,ent.char.says.start)

                    elif ent.isNpc("Clémence"):                     # Clémence specials interractions
                        if dictIsPnjVar["Alice"] or dictIsPnjVar["Félicité"] or dictIsPnjVar["Sixtine"]:          # With her sisters
                            tempTabl = []
                            if dictIsPnjVar["Alice"]:
                                tempTabl.append("Hé Alice, ça va être le moment de tester tes compétences non ?")
                            if dictIsPnjVar["Félicité"]:
                                tempTabl.append("Surtout, oublie pas de *pas* en faire trop Féli")
                            if dictIsPnjVar["Sixtine"]:
                                tempTabl.append("Sixtine, je devrais avoir ramenné des vielles peintures, ça t'interresse de regarder ça après le combat ?")

                            rand = tempTabl[random.randint(0,len(tempTabl)-1)]
                            tempTurnMsg += "\n{0} : *\"{1}\"*\n".format(ent.icon,rand)

                            if rand == "Sixtine, je devrais avoir ramenné des vielles peintures, ça t'interresse de regarder ça après le combat ?":
                                if random.randint(0,99) < 50:
                                    tempTurnMsg += "{0} : *\"{1}\"*\n".format('<:sixtine:908819887059763261>',"Oh heu... Je comptais plutôt faire une sieste après moi...")
                                    tempTurnMsg += "{0} : *\"{1}\"*\n".format(ent.icon,"Pas de soucis")
                                else:
                                    tempTurnMsg += "{0} : *\"{1}\"*\n".format('<:sixtine:908819887059763261>',"Oh heu... Pourquoi pas...")

                        else:
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,ent.char.says.start)
                    
                    elif ent.isNpc("Shushi"):                       # Shushi specials interractions
                        if dictIsPnjVar["Lena"]:
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"Allez Miman ! Ti va touz les défonzer !")
                            if random.randint(0,99) < 50:
                                if random.randint(0,99) < 50:
                                    tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:lena:909047343876288552>',"Voyons Shushi, c'est quoi ce language ?")
                                else:
                                    tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:lena:909047343876288552>',"`Ricane`")

                        else:
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,ent.char.says.start)

                    elif ent.isNpc("Shihu"):                        # Shihu specials interractions
                        if dictIsPnjVar["Lena"]:
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"Z'est le doit au Boum Boum ?")
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:lena:909047343876288552>',"`Ricane` Allez vas-y")
                        else:
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,ent.char.says.start)

                    elif ent.isNpc("John") and dictIsPnjVar["Clémence"] and random.randint(0,99) < 50:
                        tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"D-Dit Clémence, ça te dirais une balade sous la pleine lune avec moi après ça ?")
                        tempTurnMsg += "\n<:clemence:908902579554111549> : *\"Hum ? Oh heu... Pourquoi pas écoute\"*"

                    else:
                        tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,ent.char.says.start)

        if tempTurnMsg != "__Début du combat :__":
            tempTurnMsg += "\n"

        nbLB = [0,0]

        # Passives skills and stuffs effects ---------------------------------
        for a in [0,1]:
            for b in tablEntTeam[a]:
                for skil in b.char.skills:
                    if type(skil) == skill:
                        if skil.type == TYPE_PASSIVE:               # If the entity have a passive
                            effect=findEffect(skil.effectOnSelf)
                            temp = add_effect(b,b,effect," ({0})".format(skil.name),danger=danger)
                            if '🚫' not in temp:
                                tempTurnMsg += "\n{0} → {1} ({2})".format(b.icon,effect.emoji[b.char.species-1][a],skil.name)

                            logs += "{0} get the {1} effect from {2}\n".format(b.char.name,effect.name,skil.name)

                            if effect.id == "octTourEff1":              # If the entity is the Octotower, give the damage redirect at his team
                                for ent in tablEntTeam[1]:
                                    if ent != b:
                                        add_effect(b,ent,octoTourEff2)
                                        
                                        logs += "{0} gave the {1} effect at {2} for {3} turn(s)\n".format(b.char.name,effect.name,ent.char.name,effect.turnInit)

                        if skil.id == trans.id:
                            nbLB[a] += 1

                for c in [b.char.weapon,b.char.stuff[0],b.char.stuff[1],b.char.stuff[2]]:       # Look at the entity stuff to see if their is a passive effect
                    if c.effect != None:
                        if c.effect == "mk":            # Constitution
                            effect=const
                            for z in tablEntTeam[b.team]:
                                baseHP,HPparLevel = 120,8
                                temp = z.char.endurance
                                for y in [z.char.weapon,z.char.stuff[0],z.char.stuff[1],z.char.stuff[2]]:
                                    temp += y.endurance

                                if b.team == 0:
                                    dangerFact = 1
                                elif b.team == 1:
                                    dangerFact = danger/100
                                z.hp = round((baseHP+z.char.level*HPparLevel)*((temp)/100+1)*dangerFact)
                                z.maxHp = round((baseHP+z.char.level*HPparLevel)*((temp)/100+1)*dangerFact)

                                add_effect(b,z,effect," ({0} - {1})".format(c.name,b.char.name))
                                
                                logs += "{0} gave the {1} effect at {2} for {3} turn(s)\n".format(b.char.name,effect.name,z.char.name,effect.turnInit)
                                z.refreshEffects()

                            tempTurnMsg += "\n{0} ({1}) a donné l'effet de __{2}__ (<:co:888746214999339068>) à son équipe ({3})".format(b.char.name,b.icon,effect.name,c.name)
                        else:                           # Any other effects
                            effect=findEffect(c.effect)
                            temp = add_effect(b,b,effect," ({0})".format(c.name),danger=danger)
                            if '🚫' not in temp:
                                tempTurnMsg += "\n{0} → {1} ({2})".format(b.icon,effect.emoji[b.char.species-1][a],c.name)

                            logs += "{0} get the {1} effect from {2}\n".format(b.char.name,effect.name,c.name)

                if b.char.aspiration in [POIDS_PLUME,OBSERVATEUR]:
                    b.specialVars["aspiSlot"] = 0

                b.refreshEffects()

        if tablEntTeam[1][0].isNpc("The Giant Enemy Spider"):           # Giant Enemy Spider's legs summoning
            surrondingsCells = [findCell(b.cell.x-1,b.cell.y-1),findCell(b.cell.x-1,b.cell.y),findCell(b.cell.x-1,b.cell.y+1),findCell(b.cell.x,b.cell.y-1),findCell(b.cell.x,b.cell.y+1),findCell(b.cell.x+1,b.cell.y-1),findCell(b.cell.x+1,b.cell.y),findCell(b.cell.x+1,b.cell.y+1)]
            tablTemp = [TGESL1,TGESL2]
            for cmpt in range(8):
                toSummon = copy.deepcopy(tablTemp[cmpt//4])
                toSummon.name += " {0}".format(cmpt)
                tablEntTeam, tablAliveInvoc, time, funnyTempVarName = tablEntTeam[1][0].summon(toSummon,time,surrondingsCells[cmpt],tablEntTeam,tablAliveInvoc,ignoreLimite=True)
                logs += "\n"+funnyTempVarName

        elif tablEntTeam[1][0].isNpc("Jevil"):                          # Jevil Confusiong effect
            for teamCmpt in [0,1]:
                for ent in tablEntTeam[teamCmpt]:
                    add_effect(tablEntTeam[1][0],ent,jevilEff)
                    ent.refreshEffects()

        if contexte != []:                                              # If a contexte list is given
            for a in contexte:                      # Contexte need to be a list of lists
                if a[0] == ALL:
                    for b in [0,1]:
                        for c in tablEntTeam[b]:
                            tempTurnMsg += add_effect(c,c,findEffect(a[1]))
                            
                            c.refreshEffects()

                elif a[0] == TEAM1:
                    for b in tablEntTeam[0]:
                        tempTurnMsg += add_effect(b,b,findEffect(a[1]))
                        
                        b.refreshEffects()

                elif a[0] == TEAM2:
                    for b in tablEntTeam[1]:
                        tempTurnMsg += add_effect(b,b,findEffect(a[1]))
                        
                        b.refreshEffects()

        for a in [0,1]:                                                 # Raise skills verifications
            for b in tablEntTeam[a]:
                for c in b.char.skills + b.effect:
                    if type(c)==skill:
                        if c.type in [TYPE_INDIRECT_REZ,TYPE_RESURECTION] or (c.id == "lb" and b.char.aspiration in [IDOLE,ALTRUISTE]) or c.id == "ul":
                            for d in tablEntTeam[a]:
                                d.ressurectable = True
                            break
                if b.ressurectable:
                    break

        if not(auto):                               # Send the turn 0 msg
            if tempTurnMsg == "__Début du combat :__":
                tempTurnMsg += "\n -"
            await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = light_blue))
            await asyncio.sleep(2+(min(len(tempTurnMsg),2000)/2000*5))

        fight = True

        # Effective Fight Start --------------------------------------------------------------------------
        try:
            while fight:
                everyoneDead = [True,True]
                actTurn = time.getActTurn()
                nextNotAuto,lastNotAuto = 0,0

                everyoneStillThere = False
                for a in time.timeline : # Looking for the next not auto player
                    if not(a.auto):
                        everyoneStillThere = True
                        if a.hp > 0:
                            nextNotAuto = a
                            break

                if not(everyoneStillThere):
                    allAuto = True

                if nextNotAuto != actTurn and not(auto) and not(allAuto):
                    if lastNotAuto != nextNotAuto:
                        await choiceMsg.edit(embed = discord.Embed(title = "Fenêtre de selection de l'action", color=nextNotAuto.char.color,description = f"En attente du tour de {nextNotAuto.char.name} {emoji.loading}"),components=[])
                        lastNotAuto = nextNotAuto
                    elif nextNotAuto == 0:
                        await choiceMsg.edit(embed = discord.Embed(title = "Fenêtre de selection de l'action", color=light_blue,description = f"Il n'y a plus de combattants manuels en vie"),components=[])
                        lastNotAuto = nextNotAuto

                if allAuto and choiceMsg != 0:
                    await choiceMsg.delete()
                    choiceMsg = 0

                if actTurn.hp > 0:
                    tempTurnMsg = f"__Début du tour de {actTurn.char.name} :__\n"

                # Sudden death verifications and damages ---------
                if actTurn == time.begin:
                    tour += 1
                    logs += "\n\n=========\nTurn {0}\n=========".format(tour)

                    for a in [0,1]:
                        for b in tablEntTeam[a]:
                            if b.hp > 0:
                                b.stats.survival = tour

                                if b.cell != None:
                                    if b.cell.on != b and b.cell.on == None:
                                        b.cell.on = b
                                        print("{0} n'était pas sur sa cellule, apparament".format(b.char.name))
                                else:
                                    raise Exception("{0} n'est pas sur une cellule !!".format(b.char.name))

                    if tour >= 21:
                        funnyTempVarName = f"\n__Mort subite !__\nTous les combattants perdent **{10*(tour-20)}%** de leurs PV maximums\n"
                        for a in [0,1]:
                            for b in tablEntTeam[a]:
                                if b.hp > 0:
                                    if type(b.char) == octarien and b.char.oneVAll:
                                        lose = int(b.maxHp*(0.010*(tour-20)))
                                    else:
                                        lose = int(b.maxHp*(0.1*(tour-20)))
                                    funnyTempVarName += "{0} : -{1} PV\n".format(b.icon,lose)
                                    b.hp -= lose
                                    b.stats.selfBurn += lose
                                    if b.hp <= 0:
                                        funnyTempVarName += b.death(killer=b,trueDeath=True)
                                    for skil in range(len(b.char.skills)):
                                        if type(b.char.skills[skil]) == skill and b.char.skills[skil].type in [TYPE_RESURECTION,TYPE_INDIRECT_REZ]:
                                            b.cooldowns[skil] = 99

                        if not(auto):
                            if len(funnyTempVarName) > 4096:
                                funnyTempVarName = unemoji(funnyTempVarName)
                                if len(funnyTempVarName) > 4096:
                                    funnyTempVarName = "OVERLOAD"
                            await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=funnyTempVarName))
                            await asyncio.sleep(2+(min(len(funnyTempVarName),2000)/2000*5))

                        logs += funnyTempVarName

                # Dead team check --------------------------------
                for c in [0,1]:
                    for d in tablEntTeam[c]:
                        if d.hp > 0 and type(d.char) != invoc:
                            everyoneDead[c] = False
                            break

                if everyoneDead[0] or everyoneDead[1]:
                    break

                # Random fight emoji roll -----------------------
                if random.randint(0,99) <= 10:
                    rdmEmoji= randomEmojiFight[random.randint(0,lenRdmEmojiFight-1)]
                else:
                    rdmEmoji= '<:turf:810513139740573696>'

                # Generating the first part of the main message -
                if not(auto):
                    embInfo = discord.Embed(title = "__Combat {0} (D.{1})__".format(rdmEmoji,danger),color = mainUser.color,description="__Carte__ :\n{0}\n__Timeline__ :\n{1}\n<:em:866459463568850954>".format(map(),time.icons()))

                # Start of the turn ---------------------------------------------------------------------------------
                wasAlive = actTurn.hp > 0
                temp,atRange = "",actTurn.atRange()
                nbTargetAtRange = len(atRange)
                if wasAlive:
                    logs += "\n\nTurn {0} - {1}:".format(tour,actTurn.char.name)
                potgDamages,potgKills,potgHeal,potgRaises, potgArmored = [], [], [], [], []
                for cmpt in (0,1,2,3,4):
                    for team in (0,1):
                        temp = []
                        for ent in tablEntTeam[team]:
                            if type(ent.char)!=invoc:
                                temp.append((ent.id,copy.deepcopy([ent.stats.damageDeal,ent.stats.ennemiKill,ent.stats.heals,ent.stats.allieResurected,ent.stats.armoredDamage][cmpt])))
                        temp = dict(temp)
                        [potgDamages,potgKills,potgHeal,potgRaises,potgArmored][cmpt].append(temp)

                funnyTempVarName, diffDamageDeals, diffHealMakes = actTurn.startOfTurn(tablEntTeam=tablEntTeam), actTurn.stats.damageDeal, actTurn.stats.heals
                tempTurnMsg += funnyTempVarName
                logs += "\n"+funnyTempVarName
                deathCount = bigRaiseCount = 0

                # Main messages statistics generation ---------------------------------------------------------------
                if not(auto) and (wasAlive or actTurn.hp > 0):
                    infoOp,cmpt,temp = [],0, ""
                    for a in [0,1]:     # Generating the Hp's select menu
                        for b in tablEntTeam[a]:
                            if type(b.char) != invoc:
                                raised = ""
                                if b.status == STATUS_RESURECTED:
                                    raised = " (Réanimé{0})".format(["","e"][b.char.gender == GENDER_FEMALE])
                                infoOp += [create_select_option(unhyperlink(b.char.name),str(cmpt),getEmojiObject(b.icon),f"PV : {max(0,b.hp)} ({max(0,round(b.hp/b.maxHp*100))}%), R.S. : {b.healResist}%{raised}")]
                            cmpt+=1
                    infoSelect = create_select(infoOp,placeholder="Voir les PVs des combattants")

                    temp2 = actTurn.allStats()+[actTurn.resistance,actTurn.percing]
                    critRate = int((actTurn.agility+actTurn.precision)/200*35)+actTurn.critical
                    temp2 += [critRate]
                    for a in range(0,len(allStatsNames)):               # Generating the stats field of the main message
                        if a == 7:
                            temp += f"\n\n__Réduction de dégâts__ : {temp2[a]}%"
                        elif a == 8:
                            temp += f"\n__Taux pénétration d'armure__ : {temp2[a]}%"
                        elif a == 9:
                            if actTurn.char.aspiration in [POIDS_PLUME,OBSERVATEUR]:
                                temp2[a] += actTurn.specialVars["aspiSlot"]
                            temp += f"\n__Taux de coup critique__ : {temp2[a]}%"
                        else:
                            temp += f"\n__{allStatsNames[a]}__ : {temp2[a]}"

                    level = str(actTurn.char.level) + ["","<:littleStar:925860806602682369>{0}".format(actTurn.char.stars)][actTurn.char.stars>0]
                    embInfo.add_field(name = f"__{actTurn.icon} {unhyperlink(actTurn.char.name)}__ (Niveau {level})",value=f"PV : {max(0,actTurn.hp)} / {actTurn.maxHp}",inline = False)
                    embInfo.add_field(name = "__Liste des effets :__",value=actTurn.effectIcons(),inline = True)
                    embInfo.add_field(name = "__Statistiques :__",value = temp,inline = True)
                    embInfo.add_field(name = "<:empty:866459463568850954>",value='**__Liste des effets :__**',inline=False)

                    adds = ""

                    for team in [0,1]:                                  # Generating the effects fields of the main message
                        teamView, lbCd = "", 0
                        if nbLB[team] > 0:
                            for ent in time.initTimeline:
                                if ent.team == team:
                                    for num in range(len(ent.char.skills)):
                                        if type(ent.char.skills[num]) == skill and ent.char.skills[num].id == trans.id:
                                            lbCd = ent.cooldowns[num]
                                            break

                            if lbCd <= 0:
                                teamView = "<:limiteBreak:886657642553032824> Transcendance disponible\n"
                            else:
                                teamView = "<:lbnt:904174924732694528> Transcendance : {0} tour{1}\n".format(lbCd,["","s"][int(lbCd != 1)])

                        for ent in tablEntTeam[team]:
                            if type(ent.char) != invoc:
                                teamView += ent.lightQuickEffectIcons()

                        if teamView == "":
                            teamView = "Pas d'effets sur l'équipe"
                        elif len(teamView) > 1024:
                            teamView = ""
                            confusingConfusion = None
                            if lbCd <= 0:
                                teamView = "Transcendance disponible\n"
                            else:
                                teamView = "Transcendance : {0} tour{1}\n".format(lbCd,["","s"][int(lbCd != 1)])
                            for ent in tablEntTeam[team]:
                                if type(ent.char) != invoc and not(confusingConfusion):
                                    bonusCount,malusCount,damageCount,dangerCount,armorCount,healCount,stunCount = 0,0,0,0,0,0,0
                                    if ent.effect != []:
                                        nameCast = ""
                                        for eff in ent.effect:
                                            if eff.effect.id == jevilEff.id:
                                                confusingConfusion = True
                                                break
                                            if not(eff.effect.silent or eff.effect.turnInit == -1) and eff.effect.replica == None:
                                                if eff.effect.type in [TYPE_BOOST,TYPE_INDIRECT_REZ]:
                                                    bonusCount += 1
                                                elif eff.effect.type in [TYPE_INDIRECT_HEAL]:
                                                    healCount += 1
                                                elif eff.effect.type in [TYPE_MALUS]:
                                                    malusCount += 1
                                                elif eff.effect.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]:
                                                    damageCount += 1
                                                elif eff.effect.type in [TYPE_ARMOR]:
                                                    armorCount += 1
                                                
                                                if eff.effect.stun:
                                                    stunCount += 1
                                                    nameCast = eff.effect.name

                                            elif eff.effect.replica != None:
                                                dangerCount += 1
                                                nameCast = eff.effect.name

                                        if dangerCount <= 0 and stunCount <= 0 and bonusCount+malusCount+damageCount+armorCount > 0:
                                            teamView += f"{ent.icon} : "
                                            if healCount > 0:
                                                teamView += "🩹({0})".format(healCount)
                                            if bonusCount > 0:
                                                teamView += f"🔼({bonusCount})"
                                            if malusCount > 0:
                                                teamView += f"🔽({malusCount})"
                                            if damageCount > 0:
                                                teamView += f"🩸({damageCount})"
                                            if armorCount > 0:
                                                teamView += f"🛡️({armorCount})"
                                            teamView += "\n"
                                        elif dangerCount > 0:
                                            teamView += "{0} : ⚠️ {1}\n".format(ent.icon,nameCast)
                                        elif stunCount > 0:
                                            teamView += "{0} : 💫 {1}\n".format(ent.icon,nameCast)

                            if confusingConfusion:
                                teamView = "<a:giveup:902383022354079814>"
                        if len(teamView) > 1024:        # Still overload
                            teamView = "OVERLOAD !"
                        embInfo.add_field(name= "__Équipe {0} :__".format(["Bleue","Rouge"][team]),value=teamView,inline=True)

                    if tablEntTeam[1][0].isNpc("Clémence pos."):        # Generating Clemence's and Alice's blood jauges field
                        bjValue = tablEntTeam[1][0].specialVars["clemBloodJauge"].value
                        if not(tablEntTeam[1][0].specialVars["clemMemCast"]):
                            if bjValue <= 10:
                                adds += "<:BJLeftEmpty:900473865459875911>"
                            elif bjValue <= 35:
                                adds += "<:BJLeftPartial:900473933076262963>"
                            else:
                                adds += "<:BJLeftFull:900473987564441651>"

                            if bjValue <= 35:
                                adds += "<:BJMidEmpty:900473889539366994>"
                            elif bjValue <= 60:
                                adds += "<:BJMidPartial:900473950243520522>"
                            else:
                                adds += "<:BJMidFull:900474021781569604>"

                            if bjValue <= 60:
                                adds += "<:BJRightEmpty:900473909856587847>"
                            elif bjValue <= 85:
                                adds += "<:BJRightPartial:900473969524756530>"
                            else:
                                adds += "<:BJRightFull:900474036042215515>"
                        else:
                            adds += "<a:clemBloodShiny:916370970577608766><a:clemBloodShiny:916370992551583804><a:clemBloodShiny:916371010889068634>"

                        adds += " **{0}**".format(bjValue)

                        for ent in tablEntTeam[0]:
                            if ent.isNpc("Alice Exaltée"):
                                adds += "\n"
                                bjValue = ent.specialVars["clemBloodJauge"].value

                                if bjValue <= 10:
                                    adds += "<:BJLeftEmpty:900473865459875911>"
                                elif bjValue <= 35:
                                    adds += "<:aliceBJLeftMid:914780940058898462>"
                                else:
                                    adds += "<:aliceBJLeftFull:914780954336305192>"

                                if bjValue <= 35:
                                    adds += "<:BJMidEmpty:900473889539366994>"
                                elif bjValue <= 60:
                                    adds += "<:aliceBJMidMid:914780972183072768>"
                                else:
                                    adds += "<:aliceBJMidFull:914780988134019073>"

                                if bjValue <= 60:
                                    adds += "<:BJRightEmpty:900473909856587847>"
                                elif bjValue <= 85:
                                    adds += "<:aliceBJRightMid:914781005708165120>"
                                else:
                                    adds += "<:aliceBJRightFull:914781018559492106>"

                                adds += " **{0}**".format(bjValue)
                                break

                    if adds != "":                                              # Adding the Darkness convictions and Blood Jauges field
                        embInfo.add_field(name= "__Adds__",value=adds,inline=True)

                    # Editing the main message
                    nbTry = 0
                    while 1:
                        try:
                            try:
                                await msg.edit(embed = embInfo,components=[create_actionrow(infoSelect)])
                            except:
                                await msg.edit(embed = embInfo,components=[create_actionrow(create_select([create_select_option("Un icône de personnage n'a pas été trouvé","0",default=True)],disabled=True))])
                                for team in [0,1]:
                                    for ent in tablEntTeam[team]:
                                        if type(ent.char) == char and ent.hp > 0:
                                            user = loadCharFile("./userProfile/{0}.prof".format(ent.char.owner))
                                            ent.icon = customIconDB.getCustomIcon(user)
                            break
                        except SocketError as e:
                            if e.errno != errno.ECONNRESET:
                                raise
                            else:
                                if nbTry < 5:
                                    await asyncio.sleep(1)
                                    nbTry += 1
                                    errorNb += 1
                                    logs += "\nConnexion error... retrying..."
                                else:
                                    logs += "\nConnexion lost"
                                    raise

                    if nextNotAuto == actTurn:
                        await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color))

                # Turn actions --------------------------------------------------------------------------------------
                nowStartOfTurn = datetime.now()
                if wasAlive and actTurn.hp <= 0:        # Died from indirect damages at the start
                    if not(auto):
                        if len(tempTurnMsg) > 4096:
                            tempTurnMsg = unemoji(tempTurnMsg)
                            if len(tempTurnMsg) > 4096:
                                tempTurnMsg = "OVERLOAD"

                        await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color))
                        if type(actTurn.char) != invoc:
                            await asyncio.sleep(2+(min(len(tempTurnMsg),1500)/1500*5))
                        else:
                            await asyncio.sleep(2+(min(len(tempTurnMsg),2000)/2000*5))

                    potgValue = (None,0)
                    for team in (0,1):
                        for ent in tablEntTeam[team]:
                            tempPotgValue = ent.stats.damageDeal-potgDamages[team][ent.id]+(ent.stats.ennemiKill-potgKills[team][ent.id])*ent.char.level*10+ent.stats.heals-potgHeal[team][ent.id]+(ent.stats.allieResurected-potgRaises[team][ent.id])*ent.char.level*10
                            if tempPotgValue > potgValue[1]:
                                potgValue = (ent,tempPotgValue)
                    if potgValue[1] > playOfTheGame[0]:
                        playOfTheGame = [potgValue[1],potgValue[0],discord.Embed(title=f"__Action du combat\nTour {tour}__",description=tempTurnMsg,color = potgValue[0].char.color)]

                # Still alive ===========================
                elif actTurn.hp > 0:
                    cmpt,iteration,ennemi,replay,allyRea = 0,actTurn.char.weapon.repetition,actTurn,False,actTurn.stats.allieResurected
                    unsuccess = True

                    # ========== Playing the turn ==============
                    if not(actTurn.stun):                   # The entity isn't stun, so he can play his turn
                        allReadyMove = False
                        while 1:
                            atRange, nbTargetAtRange = actTurn.atRange(), len(actTurn.atRange())
                            onReplica = False
                            for eff in actTurn.effect:
                                if eff.effect.replica != None:
                                    onReplica = eff
                                    eff.decate(turn=1)
                                    break

                            canMove,cellx,celly = [True,True,True,True],actTurn.cell.x,actTurn.cell.y
                            surrondings = actTurn.cell.surrondings()
                            for a in range(0,len(surrondings)):
                                if surrondings[a] != None:
                                    if surrondings[a].on != None and surrondings[a].on.status != STATUS_TRUE_DEATH:
                                        canMove[a] = False
                                else:
                                    canMove[a] = False

                            # The entity isn't already casting something
                            if onReplica == False:
                                if not(actTurn.auto) :                      # Manual Fighter - Action select window
                                    haveOption,unsuccess = False,False

                                    waitingSelect = create_actionrow(create_select(options=[create_select_option("Veillez patienter...","PILLON!",'🕑',default=True)],disabled=True))
                                    dateLimite = datetime.now() + timedelta(seconds=30)

                                    haveIterate = False

                                    def check(m):
                                        return int(m.author_id) == int(actTurn.char.owner) and m.origin_message.id == choiceMsg.id

                                    while not(haveOption) and not(unsuccess):
                                        choiceMsgTemp,tempTabl,tabltabl,canBeUsed = "",[actTurn.char.weapon],[0]+actTurn.cooldowns,[]

                                        for a in actTurn.char.skills:
                                            if type(a) == skill:
                                                tempTabl.append(a)
                                            else:
                                                tempTabl.append(None)

                                        if len(actTurn.cell.getEntityOnArea(area=AREA_DONUT_1,team=actTurn.team,wanted=ALLIES)) > 0:
                                            freedlyPush.emoji = ["<:movePlz:928756987532029972>","<a:sparta:928795602328903721>","<a:sparta:928796053585678337>","<a:sparta:928796223215902770>"][random.randint(0,3)]
                                            tempTabl.append(freedlyPush)
                                            tabltabl.append(0)

                                        if actTurn.specialVars["summonerMalus"]:
                                            for thing in range(len(tempTabl)):
                                                if type(tempTabl[thing]) in [skill,weapon] and tempTabl[thing].type != TYPE_SUMMON:
                                                    tempTabl[thing] = None

                                        # Generating the main menu of the window

                                        for a in range(len(tabltabl)):
                                            if tempTabl[a] != None and tabltabl[a] == 0:                                   # If the option is a valid option and the cooldown is down
                                                tablToSee = [tempTabl[a]]
                                                if type(tempTabl[a]) == skill and tempTabl[a].become != None:
                                                    tablToSee, tablEffId = [], []
                                                    for eff in actTurn.effect:
                                                        tablEffId.append(eff.effect.id)

                                                    for cmpt in range(len(tempTabl[a].become)):
                                                        if tempTabl[a].become[cmpt].needEffect == tempTabl[a].become[cmpt].rejectEffect == None:
                                                            tablToSee.append(tempTabl[a].become[cmpt])
                                                        elif tempTabl[a].become[cmpt].rejectEffect == None and tempTabl[a].become[cmpt].needEffect != None:
                                                            fullValid = True
                                                            for bidule in tempTabl[a].become[cmpt].needEffect:
                                                                if bidule.id not in tablEffId:
                                                                    fullValid = False
                                                                    break

                                                            if fullValid:
                                                                tablToSee.append(tempTabl[a].become[cmpt])
                                                        else:
                                                            fullValid = True
                                                            for bidule in tempTabl[a].become[cmpt].rejectEffect:
                                                                if bidule.id in tablEffId:
                                                                    fullValid = False
                                                                    break

                                                            if fullValid:
                                                                tablToSee.append(tempTabl[a].become[cmpt])

                                                for tempOption in tablToSee:                                            
                                                    if type(tempOption) == weapon and len(actTurn.atRange()) > 0 and actTurn.char.weapon.id not in cannotUseMainWeapon:                  # Aff. the number of targets if the option is a Weapon
                                                        canBeUsed += [tempOption]
                                                        choiceMsgTemp += f"{tempOption.emoji} {tempOption.name} (Cibles à portée : {str(nbTargetAtRange)})\n"
                                                    elif type(tempOption) != weapon:
                                                        if type(tempOption) == classes.skill and tempOption.description != None:
                                                            line = tempOption.type in [TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE,TYPE_DAMAGE]
                                                            target = [ALLIES,ENNEMIS][line]
                                                            if len(actTurn.cell.getEntityOnArea(area=tempOption.range,team=actTurn.team,wanted=target,lineOfSight=line,dead=tempOption.type == TYPE_RESURECTION)) > 0:
                                                                choiceMsgTemp += f"\n{tempOption.emoji} __{tempOption.name} :__\n"
                                                                choiceMsgTemp += "> {0}\n".format(tempOption.description.replace("\n","\n> "))
                                                                canBeUsed += [tempOption]
                                                        else:
                                                            funnyTempVarNameButTheSecond = [TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE,TYPE_DAMAGE]
                                                            target = ALLIES
                                                            for b in funnyTempVarNameButTheSecond:
                                                                if (tempOption.type == b or tempOption.id == "InfiniteDarkness") and tempOption.id != freedlyPush.id:
                                                                    target = ENNEMIS
                                                                    break

                                                            healMsg = ""
                                                            if tempOption.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL]:                      # Aff. the "Allies in Danger" icons and number if the option is a Healing option
                                                                healMsg = f" (<:INeedHealing:881587796287057951> x {len(actTurn.cell.getEntityOnArea(area=tempOption.range,team=actTurn.team,wanted=target,lifeUnderPurcentage=50))})"

                                                            line = tempOption.type in funnyTempVarNameButTheSecond
                                                            if tempOption.range != AREA_MONO:
                                                                if (tempOption.type != TYPE_SUMMON and len(actTurn.cell.getEntityOnArea(area=tempOption.range,team=actTurn.team,wanted=target,lineOfSight=line,dead=tempOption.type == TYPE_RESURECTION)) > 0) or (tempOption.type == TYPE_SUMMON and tablAliveInvoc[actTurn.team] <3):
                                                                    canBeUsed += [tempOption] 
                                                                    choiceMsgTemp += f"{tempOption.emoji} {tempOption.name}{healMsg}\n"
                                                            else:
                                                                effect = tempOption.effect
                                                                if (tempOption.type != TYPE_SUMMON and len(actTurn.cell.getEntityOnArea(area=tempOption.area,team=actTurn.team,wanted=target,lineOfSight=line,effect=effect)) > 0) or (tempOption.type == TYPE_SUMMON and tablAliveInvoc[actTurn.team] <3):                                        
                                                                    canBeUsed += [tempOption]
                                                                    choiceMsgTemp += f"{tempOption.emoji} {tempOption.name}{healMsg}\n"

                                        choiceMsgTemp += "\n"
                                        if canMove[0] or canMove[1] or canMove[2] or canMove[3]:                           # If the ent. can move, add the Move option
                                            canBeUsed += [option("Déplacement",'👟')]
                                            choiceMsgTemp += "👟 Déplacement\n"

                                        canBeUsed += [option("Passer",'🚫')]                                               # Adding the Pass option, for the dark Sasuke who think that actualy playing the game is to much for them
                                        choiceMsgTemp += "🚫 Passer"

                                        mainOptions,cmpt = [],0
                                        for a in canBeUsed:                     # Generating the select menu
                                            desc = ""
                                            if type(a) != option:
                                                if type(a) != classes.skill or (type(a) == classes.skill and a.description==None):
                                                    if a.area == AREA_MONO:
                                                        desc = "Monocible"
                                                    else:
                                                        desc = "Zone"

                                                    if type(a) == weapon:
                                                        stat = a.use
                                                        if stat != None and stat != HARMONIE:
                                                            stat = nameStats[a.use]
                                                        elif stat == None:
                                                            stat = "Fixe"
                                                        elif stat == HARMONIE:
                                                            stat = "Harmonie"

                                                        multiple = [""," x{0}".format(a.repetition)][a.repetition > 1]

                                                        desc += f" - {tablTypeStr[a.type]} - {a.power}{multiple} - {stat}"
                                                    else:
                                                        powy = ""
                                                        if a.power > 0:
                                                            stat = a.use
                                                            if stat != None and stat != HARMONIE:
                                                                stat = nameStats[a.use]
                                                            elif stat == None:
                                                                stat = "Fixe"
                                                            elif stat == HARMONIE:
                                                                stat = "Harmonie"
                                                            multiple = [""," x{0}".format(a.repetition)][a.repetition > 1]
                                                            powy = f"{a.power} - {stat}{multiple}"

                                                        desc += f" - {tablTypeStr[a.type]} {powy}"
                                                else:
                                                    desc, toRemove = a.description, ["_","*","|","\n"]
                                                    for letter in toRemove:
                                                        desc = desc.replace(letter,"")
                                                    if len(desc) > 95:
                                                        desc = desc[:95] + "(...)"
                                                mainOptions += [create_select_option(unhyperlink(a.name),str(cmpt),getEmojiObject(a.emoji),desc)]
                                            else:
                                                mainOptions += [create_select_option(unhyperlink(a.name),str(cmpt),a.emoji)]
                                            cmpt += 1

                                        mainSelect = create_select(options=mainOptions,placeholder = "Séléctionnez une option :")

                                        if haveIterate:                         # Time limite stuff
                                            timeLimite = (dateLimite - datetime.now()).total_seconds()
                                            await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = choiceMsgTemp).set_footer(text=f'Fin du tour dans {round(timeLimite)} secondes'),components=[waitingSelect])
                                            await asyncio.sleep(3)
                                            dateLimite = dateLimite+timedelta(seconds=3)

                                        timeLimite = (dateLimite - datetime.now()).total_seconds()
                                        await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = choiceMsgTemp).set_footer(text=f'Fin du tour dans {round(timeLimite)} secondes'),components=[create_actionrow(mainSelect)])
                                        haveIterate = True

                                        validoption = False
                                        def checkMainOption(m):
                                            return int(m.author.id) == actTurn.char.owner
                                        while not(validoption):
                                            timeLimite = (dateLimite - datetime.now()).total_seconds()
                                            try:
                                                react = await wait_for_component(bot,messages=choiceMsg,check=checkMainOption,timeout = timeLimite)
                                            except:
                                                unsuccess = True
                                                break

                                            mainSelect = create_actionrow(getChoisenSelect(mainSelect,react.values[0]))
                                            react = canBeUsed[int(react.values[0])]
                                            validoption = True

                                        choiceMsgTemp = ""

                                        # Second Menu generating
                                        if type(react) == weapon:
                                            weapOptions = []
                                            for a in range(0,nbTargetAtRange):
                                                choiceMsgTemp += f"{a} - {atRange[a].quickEffectIcons()}"
                                                desc = f"PV : {int(atRange[a].hp/atRange[a].maxHp*100)}%, Pos : {atRange[a].cell.x} - {atRange[a].cell.y}"
                                                if react.area != AREA_MONO:
                                                    desc += f", Zone : {len(atRange[a].cell.getEntityOnArea(area=actTurn.char.weapon.area,team=actTurn.team,wanted=actTurn.char.weapon.target,directTarget=False))}"
                                                weapOptions += [create_select_option(unhyperlink(atRange[a].char.name),str(a),getEmojiObject(atRange[a].icon),desc)]

                                            weapOptions += [create_select_option("Retour",str(a+1),emoji.backward_arrow)]
                                            weapSelect = create_select(options=weapOptions,placeholder="Sélectionnez une cible :")

                                            if len(weapOptions) == 2:
                                                temp,cmpt =[],0
                                                for a in weapOptions:
                                                    temp+=[create_button(1+cmpt,a["label"],a["emoji"],a["value"])]
                                                    cmpt += 1

                                                weapSelect = [create_actionrow(temp[0],temp[1])]

                                                dateLimite = dateLimite+timedelta(seconds=3)
                                                timeLimite = (dateLimite - datetime.now()).total_seconds()
                                                await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp).set_footer(text=f'Fin du tour dans {round(timeLimite)} secondes'),components=[mainSelect]+weapSelect)

                                            elif choiceMsgTemp != "":
                                                timeLimite = (dateLimite - datetime.now()).total_seconds()
                                                await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp).set_footer(text=f'Fin du tour dans {round(timeLimite)} secondes'),components=[mainSelect,waitingSelect])
                                                dateLimite = dateLimite+timedelta(seconds=3)
                                                await asyncio.sleep(3)
                                                timeLimite = (dateLimite - datetime.now()).total_seconds()
                                                await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp).set_footer(text=f'Fin du tour dans {round(timeLimite)} secondes'),components=[mainSelect,create_actionrow(weapSelect)])

                                            timeLimite = (dateLimite - datetime.now()).total_seconds()
                                            try:
                                                react = await wait_for_component(bot,messages=choiceMsg,check=check,timeout=timeLimite)
                                            except:
                                                unsuccess = True
                                                await choiceMsg.clear_reactions()
                                                break

                                            if len(weapOptions) > 2:
                                                selectedOptionSelect = [getChoisenSelect(weapSelect,react.values[0])]
                                            else:
                                                selectedOptionSelect = None

                                            optionChoice = OPTION_WEAPON
                                            try:
                                                value = int(react.values[0])
                                            except:
                                                value = int(react.custom_id)
                                            if value<len(atRange):
                                                ennemi = atRange[value]
                                                haveOption = True

                                        elif type(react) == skill:
                                            skillOptions = []
                                            skillToUse,nbTargetAtRangeSkill,targetAtRangeSkill,a = react,0,[],-1
                                            funnyTempVarName, funnyTempVarNameButTheSecond= [TYPE_ARMOR,TYPE_BOOST,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ,TYPE_RESURECTION,TYPE_HEAL],[TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE]

                                            if skillToUse.range != AREA_MONO:
                                                if skillToUse.type in funnyTempVarName or skillToUse.id == freedlyPush.id:
                                                    targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.range,team=actTurn.team,wanted=ALLIES,dead=skillToUse.type == TYPE_RESURECTION)
                                                elif skillToUse.type in funnyTempVarNameButTheSecond:
                                                    targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.range,team=actTurn.team,wanted=ENNEMIS,lineOfSight=True)

                                            else:
                                                if skillToUse.type in funnyTempVarName:
                                                    targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES,directTarget=False)
                                                elif skillToUse.type in funnyTempVarNameButTheSecond:
                                                    targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENNEMIS,directTarget=False)

                                                if skillToUse.type == TYPE_UNIQUE:
                                                    targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALL)
                                                choiceMsgTemp += "Les combattants suivants seront affectés par la compétence :\n"

                                            if skillToUse.type != TYPE_SUMMON:
                                                nbTargetAtRangeSkill = len(targetAtRangeSkill)

                                                for a in range(0,nbTargetAtRangeSkill):
                                                    choiceMsgTemp += f"{a} - {targetAtRangeSkill[a].quickEffectIcons()}"
                                                    desc = f"PV : {int(targetAtRangeSkill[a].hp/targetAtRangeSkill[a].maxHp*100)}%, Pos : {targetAtRangeSkill[a].cell.x} - {targetAtRangeSkill[a].cell.y}"
                                                    if react.area not in [AREA_MONO,AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES]:
                                                        if react.type in funnyTempVarName:
                                                            wanted = ALLIES
                                                        else:
                                                            wanted = ENNEMIS
                                                        desc += f", Zone : {len(targetAtRangeSkill[a].cell.getEntityOnArea(area=react.area,team=actTurn.team,wanted=wanted,directTarget=False))}"
                                                    skillOptions += [create_select_option(unhyperlink(targetAtRangeSkill[a].char.name),str(a),getEmojiObject(targetAtRangeSkill[a].icon),desc)]
                                                
                                                if react.area in [AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES] or react.range == AREA_MONO:
                                                    skillOptions = [create_select_option("Valider",'✅','✅')]

                                            else:
                                                choiceMsgTemp =f"Voulez vous invoquer {skillToUse.invocation} ?"
                                                skillOptions = [create_select_option("Valider",'✅','✅')]
                                                a = 0

                                            skillOptions += [create_select_option("Retour",str(a+1),emoji.backward_arrow)]
                                            skillSelect = create_select(options=skillOptions)

                                            if len(skillOptions) == 2:
                                                temp,cmpt =[],0
                                                for a in skillOptions:
                                                    tipe = 1
                                                    if a["label"] == 'Valider':
                                                        tipe = 3
                                                    elif a["label"] == "Retour":
                                                        tipe = 2
                                                    temp+=[create_button(tipe,a["label"],a["emoji"],a["value"])]
                                                    cmpt += 1

                                                skillSelect = [create_actionrow(temp[0],temp[1])]

                                                dateLimite = dateLimite+timedelta(seconds=3)
                                                timeLimite = (dateLimite - datetime.now()).total_seconds()
                                                await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp).set_footer(text=f'Fin du tour dans {round(timeLimite)} secondes'),components=[mainSelect]+skillSelect)

                                            elif choiceMsgTemp != "":
                                                timeLimite = (dateLimite - datetime.now()).total_seconds()
                                                await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp).set_footer(text=f'Fin du tour dans {round(timeLimite)} secondes'),components=[mainSelect,waitingSelect])
                                                dateLimite = dateLimite+timedelta(seconds=3)
                                                await asyncio.sleep(3)
                                                timeLimite = (dateLimite - datetime.now()).total_seconds()
                                                await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp).set_footer(text=f'Fin du tour dans {round(timeLimite)} secondes'),components=[mainSelect]+[create_actionrow(skillSelect)])

                                            await choiceMsg.clear_reactions()
                                            try:
                                                timeLimite = (dateLimite - datetime.now()).total_seconds()
                                                react = await wait_for_component(bot,messages=choiceMsg,timeout = timeLimite,check=check)
                                            except:
                                                unsuccess = True
                                                await choiceMsg.clear_reactions()
                                                break

                                            if len(skillOptions) > 2:
                                                selectedOptionSelect = [getChoisenSelect(skillSelect,react.values[0])]
                                            else:
                                                selectedOptionSelect = None

                                            optionChoice = OPTION_SKILL
                                            try:
                                                value = react.values[0]
                                            except:
                                                value = react.custom_id[0]

                                            if value == '✅':
                                                ennemi = actTurn
                                                optionChoice = OPTION_SKILL
                                                haveOption = True
                                                break
                                            elif int(value) < len(targetAtRangeSkill):
                                                ennemi = targetAtRangeSkill[int(value)]
                                                optionChoice = OPTION_SKILL
                                                haveOption = True
                                                break

                                        elif type(react) == option:
                                            if react.emoji == '🚫':
                                                optionChoice = OPTION_SKIP
                                                unsuccess=False
                                                ennemi = actTurn
                                                haveOption=True

                                            elif react.emoji == '👟':
                                                movingOption = [None,None,None,None]
                                                actCell = actTurn.cell
                                                for cmpt in range(0,4):
                                                    if surrondings[cmpt] != None:
                                                        movingOption[cmpt] = create_button(style=ButtonStyle.grey,label="Aller sur {0}:{1}".format(surrondings[cmpt].x,surrondings[cmpt].y),emoji=moveEmoji[cmpt],custom_id=moveEmoji[cmpt],disabled=not(canMove[cmpt]))
                                                    else:
                                                        movingOption[cmpt] = create_button(style=ButtonStyle.grey,label="Aller en dehors du monde",emoji=moveEmoji[cmpt],custom_id=moveEmoji[cmpt],disabled=True)

                                                allMouvementOptions = create_actionrow(movingOption[0],movingOption[1],movingOption[2],movingOption[3])
                                                tablSurrendCells = [[findCell(actCell.x-1,actCell.y-1),findCell(actCell.x-0,actCell.y-1),findCell(actCell.x+1,actCell.y-1)],[findCell(actCell.x-1,actCell.y),findCell(actCell.x-0,actCell.y),findCell(actCell.x+1,actCell.y)],[findCell(actCell.x-1,actCell.y+1),findCell(actCell.x-0,actCell.y+1),findCell(actCell.x+1,actCell.y+1)]]
                                                mapLike = ""
                                                for litTabl in tablSurrendCells:
                                                    for cmpt in range(len(litTabl)):
                                                        if litTabl[cmpt] == None:
                                                            mapLike += '❌'
                                                        elif litTabl[cmpt].on != None:
                                                            mapLike += litTabl[cmpt].on.icon
                                                        else:
                                                            finded = False
                                                            for cmptBis in (0,1,2,3):
                                                                if litTabl[cmpt] == surrondings[cmptBis]:
                                                                    mapLike += moveEmoji[cmptBis]
                                                                    finded=True
                                                                    break

                                                            if not(finded):
                                                                mapLike += '<:empty:866459463568850954>'

                                                        if cmpt != 2:
                                                            mapLike += "|"
                                                    mapLike += "\n"

                                                await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = "Dans quelle direction voulez vous aller ?\n\n"+mapLike).set_footer(text=f'Fin du tour dans {round(timeLimite)} secondes'),components=[cancelButton,allMouvementOptions])

                                                choiceToMove = None
                                                while choiceToMove == None:
                                                    timeLimite = (dateLimite - datetime.now()).total_seconds()
                                                    try:
                                                        choiceMove = await wait_for_component(bot,messages=choiceMsg,timeout=timeLimite,check=check)
                                                    except:
                                                        unsuccess = True
                                                        break
                                                    if choiceMove.custom_id == "return":
                                                        break
                                                    else:
                                                        for a in range(0,4):
                                                            if choiceMove.custom_id == moveEmoji[a]:
                                                                choiceToMove = surrondings[a]
                                                                optionChoice = OPTION_MOVE
                                                                break

                                                        unsuccess=False
                                                        ennemi = actTurn
                                                        haveOption=True

                                    try:
                                        logs += "\nManual fighter. Option selected : {0}".format(["Use Weapon","Use Skill","Move","Skip"][optionChoice])
                                    except:
                                        logs += "\nManual fighter, but no option selected"
                                    await choiceMsg.clear_reactions()
                                    try:
                                        if selectedOptionSelect != None:
                                            await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = "Tour en cours "+emoji.loading),components=[mainSelect]+selectedOptionSelect)
                                        else:
                                            await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = "Tour en cours "+emoji.loading),components=[mainSelect])
                                    except:
                                        await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = "Tour en cours "+emoji.loading),components=[])

                                if not(actTurn.auto) and unsuccess:
                                    if actTurn.missedLastTurn == False:
                                        actTurn.missedLastTurn = True

                                    else:
                                        actTurn.auto = True
                                        nowStartOfTurn = datetime.now()

                                elif not(actTurn.auto) and not(unsuccess):
                                    actTurn.missedLastTurn = False

                                if unsuccess or type(ennemi)==int: # AI's stuffs
                                    nearestEnnemi,nearestDistance,Cell,nearestCell,ennemi = 0,9999,actTurn.cell,0,actTurn
                                    
                                    # Définition du type d'IA :
                                    choisenIA = actTurn.IA

                                    lastDPT = True
                                    for b in tablEntTeam[actTurn.team]:
                                        if b.char.aspiration in [BERSERK,OBSERVATEUR,POIDS_PLUME,TETE_BRULE,MAGE,ENCHANTEUR]:
                                            lastDPT = False
                                            break

                                    team2see = [team1,team2][int(not(actTurn.team))][:]
                                    team2compare = tablEntTeam[int(not(actTurn.team))][:]
                                    for a in team2compare[:]:
                                        if a.hp <= 0:
                                            team2compare.remove(a)

                                    ennemiesdying = False
                                    if  len(team2compare) / len(team2see) <= 0.33:
                                        ennemiesdying = True

                                    if (actTurn.char.aspiration not in [BERSERK,OBSERVATEUR,POIDS_PLUME,TETE_BRULE,MAGE,ENCHANTEUR] and actTurn.char.weapon.range != RANGE_MELEE) and (len(actTurn.cell.getEntityOnArea(area=AREA_CIRCLE_2,team=actTurn.team,wanted=ENNEMIS,directTarget=False)) > 0 or lastDPT or ennemiesdying or tour > 15):
                                        choisenIA = AI_OFFERUDIT

                                    logs += "\nAuto Fighter. Selected AI : {0}".format(["AI Damage","AI Idole","AI Shield","AI Aventurer","AI Healer","AI agressive supp","AI Mage","AI Enchant"][choisenIA])
                                    
                                    # Définition des probabilités :
                                    # [DPT_PHYS,BOOST,SHIELD,AVENTURE,ALTRUISTE,OFFERUt,MAGE,ECHANT]

                                    probaAtkWeap = [80,40,50,40,40,50,60,60] 
                                    probaHealWeap = [20,60,30,30,70,30,20,20]

                                    if actTurn.isNpc("Kiku"):                               # Kiku have a ways better chance to raise her allies
                                        probaReaSkill = [5000,5000,5000,5000,5000,5000,5000,5000]
                                    elif (dictIsPnjVar["Kiku"] and actTurn.team == 1):      # If there is a ally Kiku, let her raise
                                        probaReaSkill = [0,0,0,0,0,0,0,0]
                                    else:
                                        probaReaSkill = [50,220,200,30,200,100,50,50]

                                    probIndirectReacSkill = [30,150,100,30,150,80,30,30]
                                    probaAtkSkill = [70,40,70,30,40,70,100,100]
                                    probaIndirectAtkSkill = [50,40,40,30,40,120,100,100]
                                    probaHealSkill = [30,100,70,30,130,50,30,30]
                                    probaBoost = [30,130,50,30,70,70,30,50]
                                    probaMalus = [45,40,100,30,50,70,50,50]
                                    probaArmor = [35,100,150,30,70,70,50,35]

                                    # There is a ennemi casting ?
                                    ennemiCast = False

                                    for ent in tablEntTeam[int(not(actTurn.team))]:
                                        for eff in ent.effect:
                                            if eff.effect.replica != None:
                                                skillFinded = findSkill(eff.effect.replica)
                                                if (skillFinded.effectOnSelf == None and skillFinded.type != TYPE_HEAL) or (skillFinded.effectOnSelf != None and findEffect(skillFinded.effectOnSelf).replica == None):
                                                    ennemiCast = True
                                                    break

                                    if ennemiCast:
                                        logs += "\nA ennemi is casting !"
                                        probaArmor[actTurn.IA] = int(probaArmor[actTurn.IA] *2)

                                    # Weapons proba's ----------------------------------
                                    if actTurn.char.weapon.name.lower() == "noneweap" or (actTurn.char.weapon.id in cannotUseMainWeapon and len(actTurn.atRange()) > 0):
                                        probaHealWeap = [0,0,0,0,0,0,0,0]
                                        probaAtkWeap = [0,0,0,0,0,0,0,0]
                                    else:
                                        if actTurn.char.weapon.type == TYPE_DAMAGE:
                                            probaHealWeap = [0,0,0,0,0,0,0,0]
                                        elif actTurn.char.weapon.type == TYPE_HEAL:
                                            probaAtkWeap = [0,0,0,0,0,0,0,0]
                                            if len(actTurn.cell.getEntityOnArea(area=actTurn.char.weapon.effectiveRange,team=actTurn.team,wanted=ALLIES,directTarget=True,ignoreInvoc=True,lifeUnderPurcentage=90)) == 0 and len(actTurn.cell.getEntityOnArea(area=actTurn.char.weapon.effectiveRange,team=actTurn.team,wanted=ALLIES,directTarget=True,ignoreInvoc=True)) > 0:
                                                probaHealWeap = [0,0,0,0,0,0,0,0]

                                    surron = actTurn.cell.surrondings()
                                    if len(actTurn.atRange()) == 0 and (surron[0] != None and surron[0].on != None) and (surron[1] != None and surron[1].on != None) and (surron[2] != None and surron[2].on != None) and (surron[3] != None and surron[3].on != None):
                                        probaAtkWeap = [0,0,0,0,0,0,0,0]

                                    if actTurn.isNpc("Alice Exaltée") and actTurn.specialVars["clemBloodJauge"].value <= 40:
                                        probaHealWeap[actTurn.IA] = int(probaHealWeap[actTurn.IA]*1.35)
                                        probaBoost[actTurn.IA] = int(probaBoost[actTurn.IA]*0.6)
                                        probaHealSkill[actTurn.IA] = int(probaHealSkill[actTurn.IA] * 0.9)
                                        probaAtkSkill[actTurn.IA] = int(probaAtkSkill[actTurn.IA] * 0.7)

                                    elif actTurn.isNpc("Luna prê.") and len(atRange) > 0:
                                        probaAtkSkill[actTurn.IA] = probaAtkSkill[actTurn.IA] * 2

                                    if actTurn.char.weapon.id in [whiteSpiritWings.id,bleuSpiritWings.id,fleau.id]:
                                        probaAtkWeap[actTurn.IA] = int(probaAtkWeap[actTurn.IA] * 1.5)

                                    # Do we have a big buff ? If yes, maybe we should consider using skills if we can't attack
                                    bigbuffy = False
                                    for a in actTurn.effect:
                                        if a.type == TYPE_BOOST and a.allStats()[actTurn.char.weapon.use] > 0:
                                            logs += "\nThe stat used by the weapon is boosted"
                                            bigbuffy = True
                                            break

                                    if bigbuffy and nbTargetAtRange < 0:
                                        logs += " but no target in the range of the weapon is found"
                                        haveOffSkills = False
                                        for a in range(7):
                                            if actTurn.cooldowns[a] <= 0 and type(actTurn.skills[a]) == skill:
                                                if actTurn.skills[a].type == TYPE_DAMAGE:
                                                    if (actTurn.skills[a].range == AREA_MONO and len(actTurn.cell.getEntityOnArea(area=actTurn.skills[a].area,team=actTurn.team,wanted=ENNEMIS,effect=actTurn.skills[a].effect))> 0) or (actTurn.skills[a].range != AREA_MONO and len(actTurn.cell.getEntityOnArea(area=actTurn.skills[a].range,team=actTurn.team,wanted=ENNEMIS,effect=actTurn.skills[a].effect))> 0):
                                                        haveOffSkills = True
                                                        break

                                        if haveOffSkills:
                                            probaHealWeap = [0,0,0,0,0,0,0,0]
                                            probaAtkWeap = [0,0,0,0,0,0,0,0]
                                            logs += "\nSomes offensives skills with targets at range have been found. Weapon's proba neutralized"
                                        else:
                                            logs += "\nNo available offensives skills have been found"

                                    qCast = False
                                    for eff in actTurn.effect:
                                        if eff.effect.id == quickCastEff.id:
                                            qCast = True
                                            probaHealWeap[actTurn.IA] = 0
                                            probaAtkWeap[actTurn.IA] = 0
                                            break

                                    healSkill,atkSkill,reaSkill,indirectReaSkill,indirectAtkSkill,boostSkill,malusSkill,armorSkill,invocSkill = [],[],[],[],[],[],[],[],[]

                                    for a in range(7): # Catégorisation des sorts
                                        actSkill = actTurn.char.skills[a]
                                        if actTurn.cooldowns[a] == 0 and type(actSkill) == skill:
                                            if actSkill.become == None:
                                                tablToLook = [actSkill]
                                            else:
                                                tablToLook, tablEffId = [], []
                                                for eff in actTurn.effect:
                                                    tablEffId.append(eff.effect.id)

                                                for cmpt in range(len(actSkill.become)):
                                                    if actSkill.become[cmpt].needEffect == actSkill.become[cmpt].rejectEffect == None:
                                                        tablToLook.append(actSkill.become[cmpt])
                                                    elif actSkill.become[cmpt].rejectEffect == None and actSkill.become[cmpt].needEffect != None:
                                                        fullValid = True
                                                        for bidule in actSkill.become[cmpt].needEffect:
                                                            if bidule.id not in tablEffId:
                                                                fullValid = False
                                                                break

                                                        if fullValid:
                                                            tablToLook.append(actSkill.become[cmpt])
                                                    else:
                                                        fullValid = True
                                                        for bidule in actSkill.become[cmpt].rejectEffect:
                                                            if bidule.id in tablEffId:
                                                                fullValid = False
                                                                break

                                                        if fullValid:
                                                            tablToLook.append(actSkill.become[cmpt])

                                            for actSkill in tablToLook:
                                                if actSkill.range == AREA_MONO:                                     # If the skill is launch on self
                                                    allieAtRange,ennemiAtRange = len(actTurn.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ALLIES,effect=actSkill.effect,ignoreInvoc=True,directTarget=False))> 1,len(actTurn.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ENNEMIS,effect=actSkill.effect,directTarget=False))> 0
                                                    if actSkill.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL] and len(actTurn.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ALLIES,effect=actSkill.effect,lifeUnderPurcentage=90,ignoreInvoc = True,directTarget=False))> 0 and actSkill.id not in ["lb","ul",abnegation.id]:
                                                        if qCast and actSkill.effectOnSelf != None and findEffect(actSkill.effectOnSelf).replica != None:
                                                            atkSkill.append(actSkill)
                                                        else:
                                                            if actSkill.id not in [secondWind.id,dissi.id]:                                   # If the skill isn't Second Wind
                                                                healSkill.append(actSkill)
                                                            elif actSkill.id == secondWind.id and actTurn.hp/actTurn.maxHp <= 0.25:                          # Else, if the fighter is dying
                                                                healSkill.append(actSkill)
                                                            else:
                                                                for ent in tablEntTeam[actTurn.team]:
                                                                    if type(ent.char) == invoc and ent.id == actTurn.id:
                                                                        healSkill.append(actSkill)
                                                                        break
                                                    elif actSkill.type == TYPE_DAMAGE and ennemiAtRange:            # Damage skills
                                                        hasBeenApprouved = False
                                                        if qCast and actSkill.effectOnSelf != None and findEffect(actSkill.effectOnSelf).replica != None:
                                                            atkSkill.append(actSkill)
                                                            hasBeenApprouved = True
                                                        elif not(qCast):
                                                            atkSkill.append(actSkill)
                                                            hasBeenApprouved = True

                                                        if hasBeenApprouved and actSkill.needEffect != None:
                                                            atkSkill.append(actSkill)
                                                            probaAtkSkill[actTurn.IA] = probaAtkSkill[actTurn.IA]*1.2
                                                    elif actSkill.type == TYPE_RESURECTION and len(actTurn.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ALLIES,dead=True)) > 0 and not(qCast):                         # Resu skills (none lol)
                                                        if not(aliceMemCastTabl[actTurn.team]):
                                                            reaSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_INDIRECT_REZ and allieAtRange and not(qCast):       # Indirect Resu skills (Zelian R)
                                                        indirectReaSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_INDIRECT_DAMAGE and ennemiAtRange and not(qCast):   # Indirect damage skills
                                                        indirectAtkSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_BOOST and actSkill.area != AREA_MONO and allieAtRange:              # Buff skills
                                                        if qCast and actSkill.effectOnSelf != None and findEffect(actSkill.effectOnSelf).replica != None:
                                                            atkSkill.append(actSkill)
                                                        elif len(actTurn.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ALLIES,effect=actSkill.effect,ignoreInvoc=True,directTarget=False)) >= len(actTurn.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ALLIES,ignoreInvoc=True,directTarget=False))*0.5:
                                                            boostSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_BOOST and actSkill.area == AREA_MONO and not(qCast):
                                                        if actSkill.id not in [quickCast.id,invincible.id,holmgang.id,bolide.id]:
                                                            boostSkill.append(actSkill)
                                                        elif actSkill.id in [invincible.id,holmgang.id,bolide.id]:
                                                            hpRatio = actTurn.hp/actTurn.maxHp
                                                            if hpRatio < 0.2:
                                                                boostSkill.append(actSkill)
                                                                boostSkill.append(actSkill)
                                                                boostSkill.append(actSkill)
                                                                probaBoost[actTurn.IA] = probaBoost[actTurn.IA] * 2
                                                            elif hpRatio < 0.5:
                                                                boostSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_MALUS and ennemiAtRange and not(qCast):             # Debuff skills
                                                        malusSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_ARMOR and actSkill.area != AREA_MONO and allieAtRange and not(qCast):              # Armor skills
                                                        if actSkill.id not in ["lb"] or (actSkill.id == "lb" and nbLB[actTurn.team] == 1):
                                                            armorSkill.append(actSkill)
                                                        else:
                                                            for ent in tablEntTeam[int(not(actTurn.team))]:
                                                                for eff in ent.effect:
                                                                    if eff.effect.replica != None:
                                                                        armorSkill.append(actSkill)

                                                        if ennemiCast and actSkill.area == AREA_ALL_ALLIES: # Si l'ennemi cast et que la compétence touche tous les alliés : Proba augmentée
                                                            armorSkill.append(actSkill)
                                                        if ennemiCast and actSkill.area != AREA_MONO: # Si l'ennemi cast et que la compétence est pas mono : Proba augmentée
                                                            armorSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_ARMOR and actSkill.area == AREA_MONO and actTurn.hp / actTurn.maxHp <= 0.5 and not(qCast):
                                                        armorSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_UNIQUE and not(qCast):                              # Other
                                                        if actSkill in [chaos]:                                         # Boost
                                                            boostSkill.append(actSkill)

                                                        elif actSkill in [serenaSpe]: # Indirect Damage
                                                            poisonCount = 0
                                                            for c in tablEntTeam[int(not(actTurn))]:
                                                                for d in c.effect:
                                                                    if d.id == estal.id:
                                                                        poisonCount += 1

                                                            if poisonCount > 2:
                                                                indirectAtkSkill.append(actSkill)

                                                    elif actSkill.type == TYPE_SUMMON and len(actTurn.cell.getEmptyCellsInArea(area=actSkill.range,team=actTurn.team))>0 and not(qCast): # Invocation
                                                        temp = actTurn.cell.getEmptyCellsInArea(area=actSkill.range,team=actTurn.team)
                                                        for b in temp[:]:
                                                            if actTurn.team == 0:
                                                                if b.x > 2:
                                                                    temp.remove(b)
                                                            elif b.x < 3:
                                                                temp.remove(a)

                                                        invocSkill.append(actSkill)

                                                    elif actSkill.id in ["lb","ul",abnegation.id] and not(qCast): 
                                                        sumHp,sumMaxHp = 0,0
                                                        for b in tablEntTeam[actTurn.team]:
                                                            sumHp += max(0,b.hp)
                                                            sumMaxHp += b.maxHp
                                                        if sumHp / sumMaxHp <= 0.6:
                                                            healSkill.append(actSkill)
                                                            healSkill.append(actSkill)
                                                            for num in range(len(probaHealSkill)):
                                                                probaHealSkill[num] = probaHealSkill[num] *1.2
                                                        if sumHp / sumMaxHp <= 0.4:
                                                            healSkill.append(actSkill)
                                                            healSkill.append(actSkill)
                                                            for num in range(len(probaHealSkill)):
                                                                probaHealSkill[num] = probaHealSkill[num] *1.5

                                                else: # The skill is cast on others
                                                    ennemiTabl = actTurn.cell.getEntityOnArea(area=actSkill.range,team=actTurn.team,wanted=ENNEMIS,lineOfSight = True,effect=actSkill.effect,ignoreInvoc = (actSkill.effectOnSelf == None or (actSkill.effectOnSelf != None and findEffect(actSkill.effectOnSelf).replica != None)))
                                                    allieTabl = actTurn.cell.getEntityOnArea(area=actSkill.range,team=actTurn.team,wanted=ALLIES,effect=actSkill.effect,ignoreInvoc = True)
                                                    allieTablHeal = actTurn.cell.getEntityOnArea(area=actSkill.range,team=actTurn.team,wanted=ALLIES,lifeUnderPurcentage=90,effect=actSkill.effect,ignoreInvoc = True)
                                                    allieAtRange,ennemiAtRange = len(allieTabl)> 0,len(ennemiTabl)> 0

                                                    if (actSkill.type == TYPE_HEAL or actSkill.type == TYPE_INDIRECT_HEAL) and len(allieTablHeal)> 0 and not(qCast):
                                                        if actSkill.id != vampirisme.id:
                                                            healSkill.append(actSkill)
                                                        elif len(actTurn.cell.getEntityOnArea(area=actSkill.range,team=actTurn.team,wanted=ALLIES,lifeUnderPurcentage=90,effect=actSkill.effect,ignoreInvoc=True,ignoreAspiration=[PROTECTEUR,ALTRUISTE,IDOLE,PREVOYANT]))> 0:
                                                            healSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_DAMAGE and ennemiAtRange:
                                                        hasBeenApprouved = False
                                                        if qCast and actSkill.effectOnSelf != None and findEffect(actSkill.effectOnSelf).replica != None:
                                                            atkSkill.append(actSkill)
                                                            hasBeenApprouved = True
                                                        elif not(qCast):
                                                            if actSkill.id != trans.id:
                                                                if actSkill.id == finalTech.id:
                                                                    pasCount = 0
                                                                    for eff in actTurn.effect:
                                                                        if eff.effect.id == pasTech.id:
                                                                            pasCount += 1
                                                                    if pasCount == 5:
                                                                        atkSkill.append(actSkill)
                                                                        atkSkill.append(actSkill)
                                                                        probaAtkSkill[actTurn.IA] = probaAtkSkill[actTurn.IA]*3
                                                                        hasBeenApprouved = True
                                                                else:
                                                                    atkSkill.append(actSkill)
                                                                    hasBeenApprouved = True
                                                                    if actSkill.id in importantSkills:
                                                                        atkSkill.append(actSkill)
                                                            else:                                           # The skill is Limite Break
                                                                if nbLB[actTurn.team] == 1:                     # If there is only one LB, nothing special
                                                                    atkSkill.append(actSkill)
                                                                else:                                           # Else, if the entity is boosted, think about using the LB
                                                                    maxBS,maxNow = -111,-111
                                                                    tempBS,tempNow = actTurn.baseStats, actTurn.allStats()

                                                                    for useless1 in tempBS:
                                                                        maxBS = max(maxBS,tempBS[useless1])
                                                                    for useless1 in tempNow:
                                                                        maxNow = max(maxNow,useless1)

                                                                    valueToUse = 1.15
                                                                    if actSkill.area != AREA_MONO:
                                                                        valueToUSe = 1.2

                                                                    if maxNow > maxBS * valueToUse:
                                                                        atkSkill.append(actSkill)
                                                                        atkSkill.append(actSkill)
                                                        if hasBeenApprouved and actSkill.needEffect != None:
                                                            atkSkill.append(actSkill)
                                                            probaAtkSkill[actTurn.IA] = probaAtkSkill[actTurn.IA]*1.2
                                                    elif actSkill.type == TYPE_RESURECTION and len(actTurn.cell.getEntityOnArea(area=actSkill.range,team=actTurn.team,wanted=ALLIES,dead=True)) > 0 and not(qCast):
                                                        if not(aliceMemCastTabl[actTurn.team]):
                                                            reaSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_INDIRECT_REZ and allieAtRange and not(qCast):
                                                        indirectReaSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_INDIRECT_DAMAGE and ennemiAtRange: # Indirect damge
                                                        if not(qCast):
                                                            if actSkill.id not in [poisonus.id,bleedingTrap.id]:
                                                                indirectAtkSkill.append(actSkill)
                                                            elif actSkill.id == poisonus.id:
                                                                if actTurn.char.weapon.effectOnUse != None and findEffect(actTurn.char.weapon.effectOnUse).id == estal.id:
                                                                    target = sorted(ennemiTabl,key=lambda ent:actTurn.getAggroValue(ent))[0]
                                                                    if len(target.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ENNEMIS,lineOfSight = True)) > 1:
                                                                        indirectAtkSkill.append(actSkill)
                                                                else:
                                                                    indirectAtkSkill.append(actSkill)
                                                            elif actSkill.id == bleeding.id:
                                                                if actTurn.char.weapon.effectOnUse != None and findEffect(actTurn.char.weapon.effectOnUse).id == bleeding.id:
                                                                    target = sorted(ennemiTabl,key=lambda ent:actTurn.getAggroValue(ent))[0]
                                                                    if len(target.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ENNEMIS,lineOfSight = True)) > 1:
                                                                        indirectAtkSkill.append(actSkill)
                                                            else:
                                                                indirectAtkSkill.append(actSkill)
                                                        elif actSkill.effectOnSelf != None and findEffect(actSkill.effectOnSelf).replica != None:
                                                            indirectAtkSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_BOOST and allieAtRange and not(qCast):
                                                        effect = findEffect(actSkill.effect[0])
                                                        if effect.turnInit >= 2 and actSkill.id != derobade.id:
                                                            boostSkill.append(actSkill)
                                                        elif len(actTurn.cell.getEntityOnArea(area=actSkill.range,team=actTurn.team,wanted=ALLIES,effect=actSkill.effect,ignoreInvoc = True)) > 1:
                                                            if actSkill.id != derobade.id:                          # Any skills
                                                                boostSkill.append(actSkill)
                                                            elif actTurn.hp/actTurn.maxHp <= 0.25:                  # Dérobade
                                                                boostSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_MALUS and ennemiAtRange and not(qCast):
                                                        if actSkill not in [boom]: 
                                                            malusSkill.append(actSkill)
                                                        elif actSkill == boom: # Si il ne reste qu'un ennemi, ne pas prendre en compte Réaction en chaîne
                                                            team2see = tablEntTeam[int(not(actTurn.team))][:]
                                                            for b in team2see[:]:
                                                                if b.hp <= 0:
                                                                    team2see.remove(b)

                                                            if len(team2see) > 1:
                                                                malusSkill.append(boom)
                                                    elif actSkill.type == TYPE_ARMOR and len(allieTablHeal)>0 and not(qCast):
                                                        if actSkill.id != convert.id:
                                                            if ennemiCast and actSkill.area == AREA_ALL_ALLIES: # Si l'ennemi cast et que la compétence touche tous les alliés : Proba augmentée
                                                                armorSkill.append(actSkill)
                                                            if ennemiCast and actSkill.area != AREA_MONO: # Si l'ennemi cast et que la compétence est pas mono : Proba augmentée
                                                                armorSkill.append(actSkill)
                                                            armorSkill.append(actSkill)

                                                        elif len(actTurn.cell.getEntityOnArea(area=actSkill.range,team=actTurn.team,wanted=ALLIES,effect=actSkill.effect,ignoreInvoc = True,ignoreAspiration=[PROTECTEUR,ALTRUISTE,IDOLE,PREVOYANT])) > 0:
                                                            armorSkill.append(actSkill)
                                                    elif actSkill.type == TYPE_UNIQUE and not(qCast):
                                                        for b in [chaos]: # Boost
                                                            if b == actSkill:
                                                                boostSkill.append(b)
                                                    elif actSkill.type == TYPE_SUMMON and actTurn.cell.getCellForSummon(area=actSkill.range, team=actTurn.team, summon= findSummon(actSkill.invocation), summoner=actTurn) != None and not(qCast):
                                                        if actSkill.id != trans.id or nbLB[actTurn.team] == 0:
                                                            invocSkill.append(actSkill)
                                                        else:
                                                            canLB = True
                                                            for ent in tablEntTeam[actTurn.team]:
                                                                if ent.hp > 0 and ent.stun != True:
                                                                    for skil in ent.char.skills:
                                                                        if type(skil) == skill and skil.id == trans.id:
                                                                            canLB = False
                                                                            break
                                                                if not(canLB):
                                                                    break
                                                            if canLB:
                                                                invocSkill.append(actSkill)
                                                                invocSkill.append(actSkill)
                                                                invocSkill.append(actSkill)

                                    isTMinDanger = False
                                    for a in tablEntTeam[actTurn.team]:
                                        if a.hp / a.maxHp <= 0.35:
                                            isTMinDanger = True
                                            break

                                    if not(isTMinDanger):
                                        probIndirectReacSkill = [0,0,0,0,0,0,0,0]
                                    else:
                                        probaHealSkill = [30,120,40,50,150,150,150,150,150]

                                    if actTurn.specialVars["summonerMalus"]:
                                        probaAtkWeap = probaHealWeap = probaReaSkill = probIndirectReacSkill = probaAtkSkill = probaIndirectAtkSkill = probaHealSkill = probaBoost = probaMalus = probaArmor = [0,0,0,0,0,0,0,0] 

                                    probTabl = [probaReaSkill,probIndirectReacSkill,probaAtkSkill,probaIndirectAtkSkill,probaHealSkill,probaBoost,probaMalus,probaArmor]
                                    for a in range(0,8):
                                        analyse = [reaSkill,indirectReaSkill,atkSkill,indirectAtkSkill,healSkill,boostSkill,malusSkill,armorSkill][a]
                                        if len(analyse) == 0:
                                            probTabl[a] = [0,0,0,0,0,0,0,0]
                                        elif a == 0:
                                            logs += "\nRésu peut être tiré\nExpected ProbTabl : {0}\n".format(probTabl[0][choisenIA])

                                    if len(invocSkill) > 0 and tablAliveInvoc[actTurn.team]<3:
                                        probaInvoc = [40,40,40,40,40,40,40,40]
                                    else:
                                        probaInvoc = [0,0,0,0,0,0,0,0]

                                    totalProba = probaAtkWeap[choisenIA]+probaHealWeap[choisenIA]

                                    for a in probTabl:
                                        totalProba+= a[choisenIA]

                                    totalProba += probaInvoc[choisenIA] + 1
                                    probaRoll = random.randint(0,totalProba)-1
                                    logs += "\nTotal Proba : {0} - ProbaRoll : {1}".format(totalProba,probaRoll)

                                    optionChoisen = False

                                    if probaRoll <= probaAtkWeap[choisenIA] and probaAtkWeap[choisenIA] > 0: #Attaque à l'arme
                                        logs += "\nSelected option : Damage with weapon"

                                        atRange = actTurn.atRange()
                                        nbTargetAtRange = len(atRange)
                                        if nbTargetAtRange > 0:
                                            atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
                                            optionChoice,ennemi = OPTION_WEAPON,atRange[0]

                                        else:
                                            compromis = False
                                            
                                            for cmpt in range(len(actTurn.char.skills)):
                                                if type(actTurn.char.skills[cmpt]) == skill and actTurn.cooldowns[cmpt] == 0 and actTurn.char.skills[cmpt].tpCac == True:
                                                    atRange = actTurn.cell.getEntityOnArea(area=actTurn.char.skills[cmpt].range,team=actTurn.team,wanted=ENNEMIS,lineOfSight=True)

                                                    if len(atRange)>0:
                                                        atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
                                                        optionChoice = OPTION_SKILL
                                                        skillToUse = actTurn.char.skills[cmpt]
                                                        try:
                                                            ennemi = atRange[0]
                                                            compromis = True
                                                        except:
                                                            pass
                                                        break

                                            if not(compromis):
                                                logs += "\nNo target at range. Trying to move"
                                                optionChoice,choiceToMove = OPTION_MOVE, actTurn.getCellToMove()

                                                if choiceToMove == None:
                                                    optionChoice = OPTION_SKIP
                                                    logs += "\nNo valid cells found. Skipping the turn"

                                        optionChoisen = True
                                    else:
                                        probaRoll -= probaAtkWeap[choisenIA]

                                    if probaRoll <= probaHealWeap[choisenIA] and probaHealWeap[choisenIA] > 0 and not(optionChoisen): #Soins à l'arme
                                        mostDamageAllie,mDAHp,Cell,nearestCell = 0,1,actTurn.cell,0
                                        logs += "\nSelected option : Heal with weapon"
                                        
                                        if nbTargetAtRange > 0:
                                            optionChoice,ennemi = OPTION_WEAPON,getHealTarget(atRange,actTurn.char.weapon)

                                        else:
                                            logs += "\nNo target at range. Trying to move"
                                            optionChoice,choiceToMove = OPTION_MOVE, actTurn.getCellToMove()
                                            
                                            if choiceToMove == None:
                                                optionChoice=OPTION_SKIP
                                                logs += "\nNo valid cells found. Skipping the turn"

                                        optionChoisen = True
                                    elif not(optionChoisen):
                                        probaRoll -= probaHealWeap[choisenIA]

                                    if probaRoll <= probTabl[0][choisenIA] and probTabl[0][choisenIA] > 0 and not(optionChoisen): # Résurection
                                        logs += "\nSelected option : Resurection Skill"
                                        if len(reaSkill) > 1:
                                            skillToUse = reaSkill[random.randint(0,len(reaSkill)-1)]
                                        else:
                                            skillToUse = reaSkill[0]

                                        if skillToUse.range != AREA_MONO:
                                            for a in tablEntTeam[actTurn.team]:
                                                if a.status == STATUS_DEAD:
                                                    optionChoice = OPTION_SKILL
                                                    ennemi = a
                                                    break

                                        else:
                                            optionChoice = OPTION_SKILL
                                            ennemi = actTurn

                                        optionChoisen=True
                                    elif not(optionChoisen):
                                        probaRoll -= probTabl[0][choisenIA]

                                    if probaRoll <= probTabl[1][choisenIA] and probTabl[1][choisenIA] > 0 and not(optionChoisen): # Résurection indirect:
                                        logs += "\nSelected option : Indirect resurection skill"
                                        for a in tablEntTeam[actTurn.team]:
                                            if a.hp <= 0.3 and a.hp > 0:
                                                optionChoice = OPTION_SKILL
                                                if len(indirectReaSkill) > 1:
                                                    skillToUse = indirectReaSkill[random.randint(0,len(reaSkill)-1)]
                                                else:
                                                    skillToUse = indirectReaSkill[0]
                                                ennemi = a
                                                optionChoisen = True
                                                break

                                        optionChoisen = True
                                    elif not(optionChoisen):
                                        probaRoll -= probTabl[1][choisenIA]

                                    if probaRoll <= probTabl[2][choisenIA] and probTabl[2][choisenIA] > 0 and not(optionChoisen): # Sort de dégâts
                                        logs += "\nSelected option : Damage skill"
                                        if len(atkSkill) > 1:
                                            randomSkill = atkSkill[random.randint(0,len(atkSkill)-1)]
                                        else:
                                            randomSkill = atkSkill[0]

                                        if randomSkill.range != AREA_MONO:
                                            atRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ENNEMIS,lineOfSight = True,effect=randomSkill.effect,ignoreInvoc = (randomSkill.effectOnSelf == None or (randomSkill.effectOnSelf != None and findEffect(randomSkill.effectOnSelf).replica != None)))
                                            atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)

                                            if len(atRange) > 0:
                                                optionChoice = OPTION_SKILL
                                                skillToUse = randomSkill
                                                ennemi = atRange[0]
                                            else:
                                                optionChoice = OPTION_SKIP

                                        else:
                                            optionChoice = OPTION_SKILL
                                            skillToUse = randomSkill
                                            ennemi = actTurn

                                        optionChoisen=True
                                    elif not(optionChoisen):
                                        probaRoll -= probTabl[2][choisenIA]

                                    if probaRoll <= probTabl[3][choisenIA] and probTabl[3][choisenIA] > 0 and not(optionChoisen): # Dégâts indirects
                                        logs += "\nSelected option : Indirect damage skill"
                                        if len(indirectAtkSkill) > 1:
                                            randomSkill = indirectAtkSkill[random.randint(0,len(indirectAtkSkill)-1)]
                                        else:
                                            randomSkill = indirectAtkSkill[0]

                                        if randomSkill.range != AREA_MONO:
                                            atRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ENNEMIS,lineOfSight=True,effect=randomSkill.effect)

                                            atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)

                                            optionChoice = OPTION_SKILL
                                            skillToUse = randomSkill
                                            ennemi = atRange[0]
                                        else:
                                            if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,wanted=ENNEMIS,directTarget=False)) > 0:
                                                optionChoice = OPTION_SKILL
                                                skillToUse = randomSkill
                                                ennemi = actTurn

                                        optionChoisen=True
                                    elif not(optionChoisen):
                                        probaRoll -= probTabl[3][choisenIA]

                                    if probaRoll <= probTabl[4][choisenIA] and probTabl[4][choisenIA] > 0 and not(optionChoisen): # Heal
                                        logs += "\nSelected option : Healing skill"
                                        if len(healSkill) > 1:
                                            randomSkill = healSkill[random.randint(0,len(healSkill)-1)]
                                        else:
                                            randomSkill = healSkill[0]

                                        if randomSkill.range != AREA_MONO:
                                            if randomSkill.id != vampirisme.id:
                                                tablAtRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ALLIES,lifeUnderPurcentage=90,effect=randomSkill.effect)
                                            else:
                                                tablAtRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ALLIES,lifeUnderPurcentage=90,effect=randomSkill.effect,ignoreAspiration=[ALTRUISTE,PROTECTEUR,PREVOYANT,IDOLE])
                                    
                                            optionChoice = OPTION_SKILL
                                            skillToUse = randomSkill
                                            ennemi = getHealTarget(tablEntTeam[actTurn.team],skillToUse)

                                        else:
                                            if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,wanted=ALLIES,effect=randomSkill.effect,directTarget=False)) > 0 or (randomSkill == trans and actTurn.char.aspiration in [ALTRUISTE,IDOLE]):
                                                optionChoice = OPTION_SKILL
                                                skillToUse = randomSkill
                                                ennemi = actTurn
                                        
                                        optionChoisen = True
                                    elif not(optionChoisen):
                                        probaRoll -= probTabl[4][choisenIA]

                                    if probaRoll <= probTabl[5][choisenIA] and probTabl[5][choisenIA] > 0 and not(optionChoisen): # Boost
                                        logs += "\nSelected option : Buff skill"
                                        if len(boostSkill) > 1:
                                            randomSkill = boostSkill[random.randint(0,len(boostSkill)-1)]
                                        else:
                                            randomSkill = boostSkill[0]

                                        if randomSkill.range != AREA_MONO: # Targeted Boost Spell
                                            atRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ALLIES,effect=randomSkill.effect,ignoreInvoc = True)
                                            effect = findEffect(randomSkill.effect[0])
                                            if effect.turnInit < 2 and actTurn in atRange:
                                                atRange.remove(actTurn)
                                            effectBoost = effect.allStats()+[effect.resistance,effect.percing,effect.critical]
                                            boost = 0
                                            for a in range(0,9):
                                                if effectBoost[a] > effectBoost[boost]:
                                                    boost = a


                                            atRange.sort(key=lambda ally: (ally.allStats()+[ally.resistance,ally.percing,ally.critical])[boost],reverse=True)
                                            optionChoice = OPTION_SKILL
                                            skillToUse = randomSkill
                                            ennemi = atRange[0]

                                        else:
                                            if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,wanted=ALLIES,effect=randomSkill.effect,directTarget=False)) > 0:
                                                optionChoice = OPTION_SKILL
                                                skillToUse = randomSkill
                                                ennemi = actTurn

                                        optionChoisen = True
                                    elif not(optionChoisen):
                                        probaRoll -= probTabl[5][choisenIA]

                                    if probaRoll <= probTabl[6][choisenIA] and probTabl[6][choisenIA] > 0 and not(optionChoisen): # Malus
                                        logs += "\nSelected option : Debuff skill"
                                        if len(malusSkill) > 1:
                                            randomSkill = malusSkill[random.randint(0,len(malusSkill)-1)]
                                        else:
                                            randomSkill = malusSkill[0]

                                        if randomSkill.range != AREA_MONO:
                                            atRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ENNEMIS,effect=randomSkill.effect,ignoreInvoc = True)
                                            effect = findEffect(randomSkill.effect[0])
                                            effectBoost = effect.allStats()+[effect.resistance,effect.percing,effect.critical]
                                            boost = 0
                                            for a in range(0,9):
                                                if effectBoost[a] > effectBoost[boost]:
                                                    boost = a

                                            atRange.sort(key=lambda ennemi: ennemi.allStats()[boost],reverse=True)
                                            optionChoice = OPTION_SKILL
                                            skillToUse = randomSkill
                                            try:
                                                ennemi = atRange[0]
                                            except:
                                                logs += "\nError : No valid target find"
                                                optionChoice = OPTION_SKIP

                                        else:
                                            if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,wanted=ENNEMIS,effect=randomSkill.effect,directTarget=False)) > 0:
                                                optionChoice = OPTION_SKILL
                                                skillToUse = randomSkill
                                                ennemi = actTurn

                                        optionChoisen=True
                                    elif not(optionChoisen):
                                        probaRoll -= probTabl[6][choisenIA]

                                    if probaRoll <= probTabl[7][choisenIA] and probTabl[7][choisenIA] > 0 and not(optionChoisen): # Armure
                                        logs += "\nSelected option : Armor skill"
                                        if len(armorSkill) > 1:
                                            randomSkill = armorSkill[random.randint(0,len(armorSkill)-1)]
                                        else:
                                            randomSkill = armorSkill[0]

                                        if randomSkill.range != AREA_MONO:
                                            if randomSkill.id != convert.id:
                                                tablAtRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ALLIES,effect=randomSkill.effect)
                                            else:
                                                tablAtRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ALLIES,effect=randomSkill.effect,ignoreAspiration=[ALTRUISTE,PREVOYANT,PROTECTEUR,IDOLE])
                                            
                                            tablAtRange.sort(key=lambda fepacho: fepacho.hp/fepacho.maxHp)

                                            optionChoice = OPTION_SKILL
                                            skillToUse = randomSkill
                                            ennemi = tablAtRange[0]

                                        else:
                                            if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,wanted=ALLIES,effect=randomSkill.effect,directTarget=False)) > 0:
                                                optionChoice = OPTION_SKILL
                                                skillToUse = randomSkill
                                                ennemi = actTurn
                                        
                                        optionChoisen = True
                                    elif not(optionChoisen):
                                        probaRoll -= probTabl[7][choisenIA]

                                    if probaRoll <= probaInvoc[choisenIA] and probaInvoc[choisenIA] > 0 and not(optionChoisen): #Invocation
                                        logs += "\nSelected option : Summon skill"
                                        if len(invocSkill) > 1:
                                            randomSkill = invocSkill[random.randint(0,len(invocSkill)-1)]
                                        else:
                                            randomSkill = invocSkill[0]

                                        optionChoice = OPTION_SKILL
                                        skillToUse = randomSkill
                                        optionChoisen = True
                                    elif not(optionChoisen):
                                        probaRoll -= probaInvoc[choisenIA]

                                    if probaRoll == -1 and probaAtkWeap[choisenIA] == probaHealWeap[choisenIA] == 0 and actTurn.char.weapon.emoji != '<:noneWeap:917311409585537075>' and not(optionChoisen):     # Can't use anything
                                        logs += "\nNo target at range. Trying to move"
                                        optionChoice,choiceToMove = OPTION_MOVE, actTurn.getCellToMove()
                                        optionChoisen = True

                                        if choiceToMove == None:
                                            optionChoice = OPTION_SKIP
                                            logs += "\nNo valid cells found. Skipping the turn"

                                    elif not(optionChoisen):
                                        optionChoice = OPTION_SKIP

                                    # Boss unique skills
                                    if actTurn.isNpc("Séréna") and actTurn.cooldowns[2] == 0:
                                        poisonCount = 0
                                        for ent in tablEntTeam[int(not(actTurn.team))]:
                                            for eff in ent.effect:
                                                if eff.id == estal.id:
                                                    poisonCount += 1

                                        if poisonCount > len(team1):
                                            optionChoice = OPTION_SKILL
                                            skillToUse = serenaSpe
                                            ennemi = actTurn

                                    elif actTurn.isNpc("Ailill") and actTurn.cooldowns[0] == 0:
                                        atRangeAilill = actTurn.cell.getEntityOnArea(area=ailillSkill.range,team=actTurn.team,wanted=ENNEMIS,lineOfSight=True,effect=ailillSkill.effect,ignoreInvoc = (ailillSkill.effectOnSelf == None or (ailillSkill.effectOnSelf != None and findEffect(ailillSkill.effectOnSelf).replica != None)))
                                        if len(atRange) > 0:
                                            optionChoice = OPTION_SKILL
                                            skillToUse = ailillSkill
                                            atRangeAilill.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
                                            ennemi = atRange[0]

                                    elif actTurn.isNpc("Luna prê.") and (actTurn.cooldowns[0] == 0 or (actTurn.hp/actTurn.maxHp <= 0.25 and actTurn.cooldowns[0] < 10)):
                                        optionChoice = OPTION_SKILL
                                        skillToUse = lunaSpeCast
                                        for ent in tablEntTeam[int(not(actTurn.team))]:
                                            if ent.isNpc("Iliana") and ent.hp > 0:
                                                ennemi = ent
                                                break

                                        if ennemi == None:
                                            atRange = actTurn.cell.getEntityOnArea(area=AREA_ALL_ENEMIES,team=actTurn.team,wanted=ENNEMIS)
                                            atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
                                            ennemi = atRange[0]

                                    elif actTurn.isNpc("Clémence pos.") and actTurn.cooldowns[2] == 0 and (tour >= 7 or actTurn.hp/actTurn.maxHp <= 0.35):
                                        optionChoice = OPTION_SKILL
                                        skillToUse = clemUltCast
                                        ennemi = actTurn

                                    elif actTurn.isNpc("Akira H.") and actTurn.hp/actTurn.maxHp <= 0.2:
                                        optionChoice = OPTION_SKILL
                                        skillToUse = akikiEnrageCastInit
                                        ennemi = actTurn
                            # ==========================================
                            else:
                                logs += "\nReplica found"
                                skilly = findSkill(onReplica.effect.replica)
                                if onReplica.replicaTarget.hp > 0:
                                    optionChoice = OPTION_SKILL
                                    skillToUse = skilly
                                    ennemi = onReplica.replicaTarget
                                else:
                                    logs += "\nInitial target down, taking another target at range"
                                    skilly = copy.deepcopy(skilly)
                                    skilly.power = int(skilly.power * (0.7-0.2*int(skilly.area != AREA_MONO)))
                                    skilly.name = skilly.name + " (Changement de dernière minute)"

                                    atRange = actTurn.cell.getEntityOnArea(area=skilly.range,team=actTurn.team,wanted=ENNEMIS,lineOfSight=True,effect=skilly.effect,ignoreInvoc = True)

                                    if len(atRange) <= 0:
                                        atRange = actTurn.cell.getEntityOnArea(area=AREA_CIRCLE_7,team=actTurn.team,wanted=ENNEMIS,lineOfSight=True,ignoreInvoc = True)
                                        logs += "\nNo fucking target at range. The ennemi in line of sight with the more aggro will be targeted, but the power will be cut again"
                                        skilly.power = int(skilly.power*0.7)
                                    
                                    if len(atRange) > 0:
                                        atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)

                                        optionChoice = OPTION_SKILL
                                        skillToUse = skilly
                                        ennemi = atRange[0]
                                    else:
                                        optionChoice = OPTION_SKIP

                            lunaUsedQuickFight = ""

                            if not(actTurn.char.canMove) and optionChoice == OPTION_MOVE:
                                optionChoice = OPTION_SKIP

                            if optionChoice == OPTION_WEAPON: #Option : Weapon
                                for eff in actTurn.effect:
                                    if eff.effect.id == lunaQuickFightEff.id:
                                        replay = True
                                        lunaUsedQuickFight += eff.decate(1)
                                        needRefresh = True
                                        actTurn.refreshEffects()
                                        break

                                if actTurn.char.weapon.say != "":
                                    if type(actTurn.char.weapon.say) == str:
                                        tempTurnMsg += f"\n{actTurn.icon} : *\"{actTurn.char.weapon.say}\"*"
                                    else:
                                        if len(actTurn.char.weapon.say) > 0:
                                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,actTurn.char.weapon.say[random.randint(0,len(actTurn.char.weapon.say)-1)])
                                        else:
                                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,actTurn.char.weapon.say[0])
                                if actTurn.char.weapon.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]: # Agressive Weapon
                                    logs += "\n{0} is attacking {1} with their weapon\n".format(actTurn.char.name,ennemi.char.name)
                                    cmpt = 0
                                    while cmpt < iteration:
                                        isAlive = ennemi.hp > 0
                                        if not(isAlive) :
                                            break
                                        if cmpt == 0:
                                            if actTurn.char.weapon.message == None:
                                                tempTurnMsg += f"\n__{actTurn.char.name} attaque {ennemi.char.name} avec son arme :__\n"
                                            else:
                                                tempTurnMsg += "\n__"+actTurn.char.weapon.message.format(actTurn.char.name,ennemi.char.name)+"__\n"
                                        else:
                                            tempTurnMsg += "\n"
                                        power = actTurn.char.weapon.power

                                        for eff in actTurn.effect:
                                            if eff.effect.id == matriceEff.id:
                                                power = int(power*(100+matriceEff.power)/100)
                                                break

                                        funnyTempVarName, deathCount = actTurn.attack(target=ennemi,value=power,icon=actTurn.char.weapon.emoji,area=actTurn.char.weapon.area,use=actTurn.char.weapon.use,onArmor=actTurn.char.weapon.onArmor,effectOnHit=actTurn.char.weapon.effectOnUse)
                                        logs+= funnyTempVarName
                                        tempTurnMsg += funnyTempVarName
                                        cmpt += 1

                                        if actTurn.char.weapon.id == "ffweap":
                                            tempTabl = copy.copy(tablEntTeam[0])
                                            try:
                                                temp.remove(ennemi)
                                            except:
                                                pass

                                            for ent in tempTabl[:]:
                                                if ent.hp <= 0:
                                                    tempTabl.remove(ent)

                                            tempTabl.sort(key=lambda ent: ent.stats.damageDeal,reverse=True)
                                            if len(tempTabl) > 0:
                                                ennemi2 = tempTabl[0]
                                                funnyTempVarName = add_effect(actTurn,ennemi2,findEffect(actTurn.char.weapon.effectOnUse))
                                                
                                                logs+= funnyTempVarName
                                                tempTurnMsg += funnyTempVarName
                                                ennemi2.refreshEffects()

                                    if actTurn.char.weapon.power > 0 and actTurn.specialVars["damageSlot"] != None:
                                        loose = int(actTurn.maxHp * (actTurn.specialVars["damageSlot"].effect.power/100))
                                        tempTurnMsg += "{0} : -{1} PV ({2})\n".format(actTurn.icon,loose,actTurn.specialVars["damageSlot"].effect.name)
                                        actTurn.hp -= loose
                                        if actTurn.hp <= 0:
                                            tempTurnMsg += actTurn.death(killer=actTurn)

                                        actTurn.refreshEffects()

                                elif actTurn.char.weapon.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL]: # None agressive Weapon
                                    logs += "\n\n{0} is healing {1} with their weapon\n".format(actTurn.char.name,ennemi.char.name)
                                    if actTurn.char.weapon.message == None:
                                        if actTurn != ennemi:
                                            tempTurnMsg += f"\n__{actTurn.char.name} soigne {ennemi.char.name} avec son arme :__\n"
                                        else:
                                            tempTurnMsg += "\n__{0} utilise son arme sur {1}-même :__\n".format(actTurn.char.name,["lui","elle"][actTurn.char.gender == GENDER_FEMALE])
                                    else:
                                        tempTurnMsg += "\n__"+actTurn.char.weapon.message.format(actTurn.char.name,ennemi.char.name)+"__\n"

                                    for a in ennemi.cell.getEntityOnArea(area=actTurn.char.weapon.area,team=actTurn.team,wanted=ALLIES,directTarget=False):
                                        funnyTempVarName, useless = actTurn.heal(a, actTurn.char.weapon.emoji, actTurn.char.weapon.use, actTurn.char.weapon.power,danger=danger,mono=actTurn.char.weapon.area == AREA_MONO)
                                        tempTurnMsg += funnyTempVarName
                                        logs += funnyTempVarName

                                    if actTurn.char.weapon.effectOnUse != None:
                                        funnyTempVarName = add_effect(actTurn,ennemi,findEffect(actTurn.char.weapon.effectOnUse),danger=danger)
                                        
                                        logs+= funnyTempVarName
                                        tempTurnMsg += funnyTempVarName

                                        ennemi.refreshEffects()

                                if actTurn.char.weapon.id in [whiteSpiritWings.id,bleuSpiritWings.id]:
                                    tempTabl = []
                                    for ent in tablEntTeam[actTurn.team]:
                                        if ent.hp > 0:
                                            tempTabl.append(ent)

                                    if len(tempTabl) > 0:
                                        tempTabl.sort(key=lambda chaton: chaton.hp/chaton.maxHp)
                                        if actTurn.char.weapon.id in [whiteSpiritWings.id]:
                                            funnyTempVarName, useless = actTurn.heal(tempTabl[0], actTurn.char.weapon.effect.emoji[0][0], actTurn.char.weapon.use, actTurn.char.weapon.effect.power, danger=danger, effName = actTurn.char.weapon.effect.name, mono=actTurn.char.weapon.area == AREA_MONO)
                                            tempTurnMsg += funnyTempVarName
                                            logs += funnyTempVarName

                                        else:
                                            funnyTempVarName = add_effect(actTurn,tempTabl[0],findEffect(actTurn.char.weapon.effect.callOnTrigger),danger=danger,start=actTurn.char.weapon.effect.name,skillIcon = actTurn.weapon.effect.emoji[0][0])
                                            logs+= funnyTempVarName
                                            tempTurnMsg += funnyTempVarName
                                            tempTabl[0].refreshEffects()

                                elif actTurn.char.weapon.id == fleau.id:
                                    tablName = []
                                    for ent in actTurn.cell.getEntityOnArea(area=actTurn.char.weapon.effect.area,team=actTurn.team,wanted=ALLIES,directTarget=False):
                                        eff = actTurn.char.weapon.effect.callOnTrigger
                                        ballerine = add_effect(actTurn,ent,eff,danger=danger)
                                        if '🚫' not in ballerine and ballerine != "":
                                            tablName.append(ent.icon)
                                            ent.refreshEffects()

                                    if tablName != []:
                                        temp = "{0} {1} → ".format(actTurn.icon,actTurn.weapon.effect.emoji[0][0])
                                        for cmpt in tablName:
                                            temp += cmpt

                                        tempTurnMsg += temp + " +{0} __{1}__\n".format(actTurn.weapon.effect.emoji[0][0],actTurn.weapon.effect.name)
                                        logs += temp

                                elif actTurn.char.weapon.id in [micPurple.id,micRed.id,micPink.id]:
                                    tablName, eff = [], actTurn.weapon.effect.callOnTrigger
                                    for ent in ennemi.cell.getEntityOnArea(area=actTurn.weapon.effect.area,team=actTurn.team,wanted=ALLIES,directTarget=False):
                                        ballerine = add_effect(actTurn,ent,eff,danger=danger,useActionStats=ACT_BOOST,skillIcon = actTurn.weapon.emoji)
                                        if '🚫' not in ballerine and ballerine != "":
                                            tablName.append(ent.icon)
                                        ent.refreshEffects()

                                    if tablName != []:
                                        temp = ""
                                        for cmpt2 in tablName:
                                            temp += cmpt2

                                        temp = "{1} {2} → {3} +{0} __{4}__\n".format(eff.emoji[actTurn.char.species-1][actTurn.team],actTurn.icon,actTurn.char.weapon.emoji,temp,eff.name)
                                        tempTurnMsg += temp
                                        logs += temp

                            elif optionChoice == OPTION_MOVE: #Option : Déplacement
                                logs += "\n\n{0} is moving".format(actTurn.char.name)
                                temp = actTurn.cell
                                actTurn.move(cellToMove=choiceToMove)
                                logs += "\n{0} have been moved from {1}:{2} to {3}:{4}".format(actTurn.char.name,temp.x,temp.y,choiceToMove.x,choiceToMove.y)
                                tempTurnMsg+= "\n"+actTurn.char.name+" se déplace\n"

                            elif optionChoice == OPTION_SKIP: #Passage de tour
                                logs += "\n\n{0} is skipping their turn".format(actTurn.char.name)
                                tempTurnMsg += f"\n{actTurn.char.name} passe son tour\n"

                            elif optionChoice == OPTION_SKILL: #Skill
                                qCast, matriceUp, needRefresh, useEffElem = False, False, False, 0

                                if skillToUse.id == finFloLaunchBase.id:
                                    skillToUse, listEff, allReadySeen, golden = copy.deepcopy(finFloLaunchBase), [], [], 0
                                    for eff in actTurn.effect:
                                        if eff.effect.id in tablRosesId and eff.effect.id not in allReadySeen:
                                            if eff.effect.id == roseRed.id:
                                                listEff.append(finFloEffList[0])
                                            elif eff.effect.id == roseDarkBlu.id:
                                                listEff.append(finFloEffList[1])
                                            elif eff.effect.id == roseBlue.id:
                                                listEff.append(finFloEffList[2])
                                            elif eff.effect.id == roseGreen.id:
                                                skillToUse.effectOnSelf = finFloEffList[3]
                                            elif eff.effect.id == roseYellow.id:
                                                golden = 2
                                            elif eff.effect.id == rosePink.id:
                                                golden = 1
                                            eff.decate(value=99)
                                            allReadySeen.append(eff.effect.id)
                                    actTurn.refreshEffects()

                                    if golden == 1:
                                        for eff in listEff:
                                            eff.turnInit += 1
                                    elif golden == 2:
                                        skillToUse.effPowerPurcent = 1.3

                                    if listEff != []:
                                        skillToUse.effect = listEff

                                for eff in actTurn.effect:
                                    if eff.effect.id == quickCastEff.id:
                                        qCast = True
                                    elif eff.effect.id == matriceEff.id:
                                        matriceUp = True
                                    elif eff.effect.id == lunaQuickFightEff.id:
                                        replay = True
                                        lunaUsedQuickFight += eff.decate(1)
                                        needRefresh = True
                                    elif skillToUse.id in useElemEffId and eff.effect.id in [tablElemEff[actTurn.char.element].id,tablElemEff[ELEMENT_UNIVERSALIS_PREMO].id]:
                                        eff.decate(turn=99)
                                        useEffElem += 1
                                        needRefresh = True
                                if needRefresh:
                                    actTurn.refreshEffects()

                                if qCast and skillToUse.effectOnSelf != None and findEffect(skillToUse.effectOnSelf).replica != None:
                                    skillToUse = copy.deepcopy(findSkill(findEffect(skillToUse.effectOnSelf).replica))
                                    skillToUse.power, skillToUse.effPowerPurcent = int(skillToUse.power*0.7), skillToUse.effPowerPurcent * 0.7

                                if skillToUse.effectOnSelf != None and findEffect(skillToUse.effectOnSelf).replica != None and actTurn.auto:
                                    for cmpt in (0,1,2,3,4):
                                        if type(actTurn.char.skills[cmpt]) == skill and actTurn.cooldowns[cmpt] == 0 and actTurn.char.skills[cmpt].id == quickCast.id:
                                            skillToUse = quickCast
                                            ennemi = actTurn
                                            break

                                if skillToUse.needEffect != None:
                                    for needed in skillToUse.needEffect:
                                        for eff in actTurn.effect:
                                            if needed.id == eff.effect.id:
                                                eff.decate(turn=99)
                                                break
                                    actTurn.refreshEffects()

                                try:
                                    logs += "\n\n{0} is using {1} on {2}".format(actTurn.char.name,skillToUse.name,ennemi.char.name)
                                except:
                                    logs += "\n\nError on writing into the logs"
                                if skillToUse.say != "":
                                    if type(skillToUse.say) == str:
                                        tempTurnMsg += f"\n{actTurn.icon} : *\"{skillToUse.say}\"*"
                                    else:
                                        if len(skillToUse.say) > 0:
                                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,skillToUse.say[random.randint(0,len(skillToUse.say)-1)])
                                        else:
                                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,skillToUse.say[0])

                                # Say Ultimate
                                if actTurn.char.says.ultimate != None and skillToUse.ultimate and not(skillToUse.effectOnSelf != None and findEffect(skillToUse.effectOnSelf).replica != None and skillToUse.power == 0 and skillToUse.effect == [None]):
                                    try:
                                        tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,actTurn.char.says.ultimate.format(target=ennemi.char.name,caster=actTurn.char.name,skill=skillToUse.name))
                                    except:
                                        tempTurnMsg += "\n__Error with the ultimate message.__ See logs for more informations"
                                        logs += "\n"+format_exc()

                                # Say Limite Break
                                if actTurn.char.says.limiteBreak != None and skillToUse.id == trans.id:
                                    try:
                                        tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,actTurn.char.says.limiteBreak.format(target=ennemi.char.name,caster=actTurn.char.name,skill=skillToUse.name))
                                    except:
                                        tempTurnMsg += "\n__Error with the Limite Break message.__ See logs for more informations"
                                        logs += "\n"+format_exc()

                                # Skill base message
                                if skillToUse.message == None:
                                    tempTurnMsg += f"\n__{actTurn.char.name} utilise la compétence {skillToUse.name} :__\n"
                                else: 
                                    tempTurnMsg += "\n__"+ skillToUse.message.format(actTurn.char.name,skillToUse.name,ennemi.char.name)+"__\n"

                                # Set the cooldown
                                for a in range(7):
                                    if type(actTurn.char.skills[a]) == skill:
                                        if skillToUse.id == actTurn.char.skills[a].id:
                                            actTurn.cooldowns[a] = skillToUse.cooldown
                                        if skillToUse.id == "lb" and actTurn.char.skills[a].ultimate and actTurn.cooldowns[a] < 2:          # Anti LB in Ult combo
                                            actTurn.cooldowns[a] = 2

                                # Share cooldown
                                if skillToUse.shareCooldown and skillToUse.id != kikuRes.id:
                                    for a in tablEntTeam[actTurn.team]:
                                        if a.char.team == actTurn.char.team:
                                            for b in range(0,len(a.char.skills)):
                                                if type(a.char.skills[b]) == skill:
                                                    if a.char.skills[b].id == skillToUse.id:
                                                        a.cooldowns[b] = skillToUse.cooldown

                                # Mors Vita Est set share cooldown
                                elif skillToUse.id == kikuRes.id:
                                    for ent in tablEntTeam[actTurn.team]:
                                        for skillToSee in range(0,len(ent.char.skills)):
                                            if type(ent.char.skills[skillToSee]) == skill:
                                                if ent.char.skills[skillToSee].id in [trans.id, memAliceCast.id, renisurection.id]:
                                                    ent.cooldowns[skillToSee] = max(ent.cooldowns[skillToSee],2)
                                                elif ent.char.skills[skillToSee].id == kikuRes.id:
                                                    ent.cooldowns[skillToSee] = skillToUse.cooldown

                                # tpCac
                                if skillToUse.tpCac and actTurn.cell.distance(ennemi.cell) > 1:
                                    surrond = ennemi.cell.surrondings()
                                    for a in surrond[:]:
                                        if a == None or (a != None and a.on != None):
                                            surrond.remove(a)

                                    if len(surrond) > 0:
                                        surrond.sort(key=lambda celly:actTurn.cell.distance(celly))
                                        actTurn.move(cellToMove=surrond[0])
                                        tempTurnMsg += "__{0}__ se téléporte au corps à corps de __{1}__\n".format(actTurn.name,ennemi.name)

                                    elif not(actTurn.isNpc('Ailill')):
                                        tempTurnMsg += "__{0}__ essaye de se téléporte au corps à corps de __{1}__, mais cela échoue\n".format(actTurn.name,ennemi.name)
                                        stat,damageBase = -100,20

                                        for stats in actTurn.allStats():
                                            stat = max(stats,stat)

                                        damage = damageBase * (1+(stat/100)) * (1-(min(95,actTurn.resistance*(1-actTurn.percing/100))/100)) * actTurn.getElementalBonus(actTurn,AREA_MONO,TYPE_INDIRECT_DAMAGE) * (1+(0.01*actTurn.level))
                                        temp = actTurn.indirectAttack(actTurn,value=damage,name="Fissure spacio-temporelle")
                                        tempTurnMsg += temp
                                        logs += temp

                                    else:
                                        surrond = ennemi.cell.surrondings()
                                        for a in surrond[:]:
                                            if a == None or (a != None and a.on == None):
                                                surrond.remove(a)
                                        if len(surrond) > 1:
                                            unlucky = surrond[0].on
                                        else:
                                            unlucky = surrond[random.randint(0,len(surrond)-1)].on
                                        stat,damageBase = -100,20

                                        for stats in actTurn.allStats():
                                            stat = max(stats,stat)

                                        damage = damageBase * (1+(stat/100)) * (1-(min(95,unlucky.resistance*(1-actTurn.percing/100))/100)) * actTurn.getElementalBonus(unlucky,AREA_MONO,TYPE_INDIRECT_DAMAGE) * (1+(0.01*actTurn.level))
                                        temp = actTurn.cell
                                        actTurn.move(cellToMove=unlucky.cell)
                                        unlucky.move(cellToMove=temp)

                                        tempTurnMsg += "__{0}__ échange de place avec __{2}__ pour être au corps à corps de __{1}__\n".format(actTurn.name,ennemi.name,unlucky.name)
                                        temp = actTurn.indirectAttack(unlucky,value=damage,name="Fissure spacio-temporelle")
                                        tempTurnMsg += temp
                                        logs += temp

                                    if skillToUse.areaOnSelf:
                                        ennemi = actTurn

                                # Luna and Iliana Head to Head
                                if skillToUse.id == lunaSpe.id:
                                    if actTurn.specialVars["clemBloodJauge"] == None:
                                        actTurn.specialVars["clemBloodJauge"] = 0

                                        cellToCheck, actCell = findCell(actTurn.cell.x+1,actTurn.cell.y), actTurn.cell
                                        if cellToCheck != None and cellToCheck.on == None:
                                            actTurn.move(cellToMove=cellToCheck)
                                            ennemi.move(cellToMove=actCell)

                                        elif actCell.distance(ennemi.cell) > 1:
                                            surron = actCell.surrondings()
                                            for celly in surron[1:4]:
                                                if celly != None and celly.on == None:
                                                    ennemi.move(cellToMove=celly)
                                                    break

                                    mainPower = lunaSpe.power * (0.7+(0.3*actTurn.specialVars["clemBloodJauge"])+0.25*int(ennemi.char.element!=ELEMENT_LIGHT))
                                    secondaryPower = lunaSpe.power * 0.2 * (0.7+(0.3*actTurn.specialVars["clemBloodJauge"])+0.25*int(ennemi.char.element!=ELEMENT_LIGHT))

                                    isThereAShield = False
                                    for fightEff in actTurn.effect:
                                        if fightEff.effect.id == lunaInfiniteDarknessShield.id:
                                            isThereAShield = True
                                            fightEff.replicaTarget = ennemi
                                            break
                                    if not(isThereAShield):
                                        ballerine = add_effect(actTurn,actTurn,lunaInfiniteDarknessShield,danger=danger,setReplica=ennemi)
                                        tempTurnMsg += ballerine
                                        logs += "\n"+ballerine
                                        actTurn.refreshEffects()

                                    # Iliana main damage taking
                                    if actTurn.specialVars["clemBloodJauge"] == 0 and ennemi.char.says.blockBigAttack != None:
                                        try:
                                            tempTurnMsg += "{0} : *\"{1}\"*\n".format(ennemi.icon,ennemi.char.says.blockBigAttack.format(target=ennemi.char.name,caster=actTurn.char.name,skill=skillToUse.name))
                                        except:
                                            tempTurnMsg += "\n__Error with the BlockBigAttack.__ See logs for more informations"
                                            logs += "\n"+format_exc()
                                    funnyTempVarName, deathCount = actTurn.attack(target=ennemi,value=mainPower,icon='<:lunaSecDamage:929705185016692786>',area=AREA_MONO,sussess=500,use=skillToUse.use,onArmor=skillToUse.onArmor)
                                    tempTurnMsg += funnyTempVarName
                                    logs += "\n"+funnyTempVarName

                                    # If she's still alive, the other allies takes less damages
                                    if ennemi.hp > 0 and actTurn.specialVars["clemBloodJauge"] != None:
                                        funnyTempVarName, deathCount = actTurn.attack(target=ennemi,value=secondaryPower,icon='<a:lunaHeadToHead:929707180943355914>',area=AREA_DONUT_7,sussess=500,use=skillToUse.use,onArmor=skillToUse.onArmor,setAoEDamage=True)
                                        tempTurnMsg += funnyTempVarName
                                        logs += "\n"+funnyTempVarName

                                        actTurn.specialVars["clemBloodJauge"] += 1

                                        logs += "\n"+add_effect(actTurn,ennemi,lunaInfiniteDarknessStun)
                                        ennemi.refreshEffects()

                                    # But she's dead, so everybody take tarif
                                    else:
                                        funnyTempVarName, deathCount = actTurn.attack(target=actTurn,value=mainPower,icon='<:lunaFinal:929705208085381182>',area=AREA_ALL_ENEMIES,sussess=500,use=skillToUse.use,onArmor=int(skillToUse.onArmor*1.2),setAoEDamage=True)
                                        tempTurnMsg += funnyTempVarName
                                        logs += "\n"+funnyTempVarName

                                        for fightEff in actTurn.effect:
                                            if fightEff.effect.id == lunaInfiniteDarknessShield.id:
                                                fightEff.decate(value=99999999999999999999)
                                                actTurn.refreshEffects()
                                                actTurn.specialVars["clemBloodJauge"] = None
                                                break

                                # ======================== Any other skill ========================
                                else:
                                    if skillToUse.type in [TYPE_BOOST,TYPE_ARMOR,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ] and skillToUse.effect != [None]:
                                        if skillToUse.id != clemUltCast.id:
                                            if skillToUse.id == bolide.id:
                                                tempTurnMsg += "{0} {1} → {0} -{2} PV\n".format(actTurn.icon,skillToUse.emoji,actTurn.hp -1)
                                                actTurn.stats.selfBurn += actTurn.hp -1
                                                actTurn.hp = 1
                                            ballerine = groupAddEffect(caster=actTurn, target=ennemi, area=skillToUse.area, effect=skillToUse.effect, skillIcon=skillToUse.emoji, actionStats=skillToUse.useActionStats, effPurcent = skillToUse.effPowerPurcent)
                                            tempTurnMsg += ballerine
                                            logs += ballerine

                                            if skillToUse.type == TYPE_BOOST and skillToUse.range == AREA_MONO and actTurn.specialVars["partner"] != None and actTurn.specialVars["partner"].hp > 0:
                                                initArea = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES,directTarget=False)
                                                secondArea = actTurn.specialVars["partner"].cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES,directTarget=False)

                                                for ent in secondArea[:]:
                                                    if ent in initArea or ent == actTurn:
                                                        secondArea.remove(ent)

                                                if len(secondArea) > 0:
                                                    effPower = [skillToUse.effPowerPurcent,100][skillToUse.effPowerPurcent == None]
                                                    ballerine = groupAddEffect(caster=actTurn, target=actTurn.specialVars["partner"], area=secondArea, effect=skillToUse.effect, skillIcon=partner.emoji, actionStats=skillToUse.useActionStats, effPurcent = effPower * partnerIn.power * 0.01)
                                                    tempTurnMsg += ballerine
                                                    logs += ballerine

                                        else:
                                            effect = skillToUse.effect[0]
                                            tempVal = max(actTurn.specialVars["clemBloodJauge"].value-1,50)
                                            effect.overhealth = tempVal * len(team1)/9 * 5
                                            tempTurnMsg += add_effect(actTurn,actTurn,effect,danger=danger)
                                            logs += "\n{0} gave the {1} effect at {2} for {3} turn(s)".format(actTurn.char.name,effect.name,b.char.name,effect.turnInit)
                                            b.refreshEffects()

                                            actTurn.specialVars["clemBloodJauge"].value = 1
                                            actTurn.specialVars["clemMemCast"] = True

                                    elif skillToUse.type in [TYPE_INDIRECT_DAMAGE,TYPE_MALUS]:
                                        if skillToUse.ultimate and skillToUse.type == TYPE_INDIRECT_DAMAGE and actTurn.char.aspiration == MAGE:
                                            tempTurnMsg += add_effect(actTurn,actTurn,classes.effect("Mage","effMage",None,turnInit=2,magie=actTurn.baseStats[MAGIE]*0.15,unclearable=True,emoji=uniqueEmoji(aspiEmoji[MAGE])))
                                            actTurn.refreshEffects()

                                        ballerine = groupAddEffect(caster=actTurn, target=ennemi, area=skillToUse.area, effect=skillToUse.effect, skillIcon=skillToUse.emoji, actionStats=skillToUse.useActionStats, effPurcent = skillToUse.effPowerPurcent)
                                        tempTurnMsg += ballerine
                                        logs += ballerine

                                        if skillToUse.id == propag.id:
                                            listTarget = []
                                            sumPower = [0,0]
                                            for eff in ennemi.effect:
                                                if eff.effect.id in [estal.id,bleeding.id] and eff.value > 0:
                                                    sumPower[eff.effect.id==estal.id] += eff.effect.power * ([propag.power,propag.power//2][int(eff.caster==actTurn)])/100

                                            effTabl, tablName, effTabl2 = [bleeding,estal],[[],[]],[bleeding2,estal2]
                                            for ent in ennemi.cell.getEntityOnArea(area=AREA_DONUT_2,team=actTurn.team,wanted=ENNEMIS,directTarget=False):
                                                for effNum in [0,1]:
                                                    if sumPower[effNum] > 0:
                                                        add_effect(actTurn,ent,effTabl[effNum],effPowerPurcent=int((sumPower[effNum]/effTabl[effNum].power)*100))
                                                        tablName[effNum].append("{0}".format(ent.icon))
                                                        ent.refreshEffects()

                                            for effNum in [0,1]:
                                                temp = ""
                                                if len(tablName[effNum]) == 1:
                                                    temp = "\n{2} {4} → {0} +{1} ({3}%)".format(tablName[effNum][0],effTabl[effNum].emoji[0][0],actTurn.icon,int((sumPower[effNum]/effTabl[effNum].power)*100),skillToUse.emoji)
                                                elif len(tablName[effNum]) > 1:
                                                    temp = ""
                                                    for cmpt in range(len(tablName[effNum])):
                                                        temp += tablName[effNum][cmpt]

                                                    temp = "\n{2} {4} → {0} +{1} ({3}%)".format(temp,effTabl[effNum].emoji[0][0],actTurn.icon,int((sumPower[effNum]/effTabl[effNum].power)*100),skillToUse.emoji)
                                                if [actTurn.specialVars["heritLesath"],actTurn.specialVars["heritEstial"]][effNum]:
                                                    if len(tablName[effNum]) == 1:
                                                        temp = "\n{0} subit l'effet {1} {2} pendant 3 tours".format(tablName[effNum][0],effTabl2[effNum].emoji[0][0],effTabl2[effNum].name,int((sumPower[effNum]/effTabl2[effNum].power)*100))
                                                    elif len(tablName[effNum]) > 1:
                                                        temp = "\n"
                                                        for cmpt in range(len(tablName[effNum])):
                                                            temp += tablName[effNum][cmpt]
                                                            if cmpt < len(tablName[effNum])-2:
                                                                temp += ", "
                                                            elif cmpt == len(tablName[effNum])-2:
                                                                temp += " et "
                                                        temp += "subissent l'effet {0} {1} pendant 3 tours".format(effTabl2[effNum].emoji[0][0],effTabl2[effNum].name,int((sumPower[effNum]/effTabl2[effNum].power)*100))
                                                tempTurnMsg += temp
                                                logs += temp
                                            tempTurnMsg += "\n"
                                            logs += "\n"

                                    elif skillToUse.type == TYPE_HEAL:
                                        logs += "\n"
                                        if ennemi.hp > 0:
                                            statUse = skillToUse.use
                                            if statUse == None:
                                                statUse = 0
                                            elif statUse == HARMONIE:
                                                temp = actTurn.allStats()
                                                for a in temp:
                                                    statUse = max(a,statUse)
                                            else:
                                                statUse = actTurn.allStats()[statUse]

                                            if skillToUse.id not in [dissi.id]:                  # Any normal healing skill
                                                if skillToUse.id == trans.id:
                                                    actionStats, entActStats = 0, actTurn.actionStats()
                                                    for cmpt in (0,1,2,3,4):
                                                        if entActStats[cmpt] > entActStats[actionStats]:
                                                            actionStats = cmpt
                                                else:
                                                    actionStats = ACT_HEAL
                                                for a in ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES,directTarget=False):
                                                    funnyTempVarName, useless = actTurn.heal(a, skillToUse.emoji, skillToUse.use, skillToUse.power,danger=danger, mono = skillToUse.area == AREA_MONO, useActionStats = skillToUse.useActionStats)
                                                    tempTurnMsg += funnyTempVarName
                                                    logs += funnyTempVarName

                                                if skillToUse.effect != [None]:
                                                    ballerine = groupAddEffect(caster=actTurn, target=ennemi, area=skillToUse.area, effect=skillToUse.effect, skillIcon=skillToUse.emoji, actionStats=skillToUse.useActionStats, effPurcent = skillToUse.effPowerPurcent)
                                                    tempTurnMsg += ballerine
                                                    logs += ballerine
                                            else:
                                                nbSummon = 0
                                                for ent in tablEntTeam[actTurn.team]:
                                                    if type(ent.char) == invoc and ent.id == actTurn.id:
                                                        nbSummon += 1
                                                        tempTurnMsg += "{0} est désinvoqué\n".format(ent.char.name)
                                                        ent.hp = 0

                                                power = skillToUse.power*nbSummon
                                                
                                                for a in ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES,directTarget=False):
                                                    funnyTempVarName, useless = actTurn.heal(a, skillToUse.emoji, skillToUse.use, power,danger=danger,mono=skillToUse.area == AREA_MONO)
                                                    tempTurnMsg += funnyTempVarName
                                                    logs += funnyTempVarName

                                    elif skillToUse.type == TYPE_SUMMON:
                                        if skillToUse.id == trans.id:
                                            for teamMate in tablEntTeam[actTurn.team]:
                                                if type(teamMate.char) == invoc and teamMate.id == actTurn.id:
                                                    teamMate.leftTurnAlive += 1

                                        if skillToUse.id not in [autoBombRush.id,killerWailUltimate.id]:
                                            tablEntTeam, tablAliveInvoc, time, funnyTempVarName = actTurn.summon(findSummon(skillToUse.invocation),time,actTurn.cell.getCellForSummon(skillToUse.range,actTurn.team,findSummon(skillToUse.invocation),actTurn),tablEntTeam,tablAliveInvoc)
                                            tempTurnMsg += funnyTempVarName+"\n"
                                            logs += "\n"+funnyTempVarName
                                        else:

                                            toSummon, cmpt = findSummon(skillToUse.invocation), 0
                                            while cmpt < [3,5][skillToUse.id==killerWailUltimate.id]:
                                                cellToSummon = actTurn.cell.getCellForSummon(skillToUse.range,actTurn.team,toSummon,actTurn)
                                                if cellToSummon != None:
                                                    tablEntTeam, tablAliveInvoc, time, funnyTempVarName = actTurn.summon(toSummon,time,cellToSummon,tablEntTeam,tablAliveInvoc,ignoreLimite=True)
                                                    tempTurnMsg += funnyTempVarName+"\n"
                                                    logs += "\n"+funnyTempVarName
                                                cmpt += 1

                                    elif skillToUse.type == TYPE_UNIQUE:
                                        if skillToUse.id == chaos.id:
                                            chaosTabl = effects[:]
                                            for a in chaosTabl[:]:
                                                if a in chaosProhib:
                                                    chaosTabl.remove(a)

                                            lenChaos = len(chaosTabl)-1
                                            for a in [0,1]:
                                                for b in tablEntTeam[a]:
                                                    if b.hp > 0:
                                                        effect = chaosTabl[random.randint(0,lenChaos)]
                                                        tempTurnMsg += add_effect(actTurn,b,effect)
                                                        
                                                        logs += "\n{0} gave the {1} effect at {2} for {3} turn(s)".format(actTurn.char.name,effect.name,b.char.name,effect.turnInit)
                                                        b.refreshEffects()

                                        elif skillToUse.id == serenaSpe.id:
                                            for a in tablEntTeam[int(not(actTurn.team))]:
                                                funnyTempVarName = ""
                                                sumPower = 0
                                                for b in a.effect:
                                                    if b.effect.id == estal.id:
                                                        sumPower += int(20*b.turnLeft)
                                                        funnyTempVarName += b.decate(value=100)

                                                if sumPower > 0:
                                                    a.refreshEffects()
                                                    sumPower += 30
                                                    temp, deathCount = actTurn.attack(target=a,value = sumPower,icon = skillToUse.emoji,area=AREA_MONO,sussess=250,use=MAGIE)
                                                    funnyTempVarName += temp

                                                    tempTurnMsg += funnyTempVarName
                                                    logs += funnyTempVarName

                                    elif skillToUse.type == TYPE_RESURECTION:
                                        if skillToUse.id == aliceRez.id:
                                            nbDown = 0
                                            for ent in tablEntTeam[actTurn.team]:
                                                if ent.status == STATUS_DEAD:
                                                    nbDown += 1

                                            if nbDown >= len(team1)//2:
                                                skillToUse = aliceRez2

                                        stat, resTabl = skillToUse.use, []

                                        for a in ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES,dead=True,directTarget=False):
                                            if stat not in [PURCENTAGE,None]:
                                                if stat != HARMONIE:
                                                    statUse = actTurn.allStats()[stat]
                                                else:
                                                    temp = actTurn.allStats()
                                                    for b in temp:
                                                        statUse = max(b,statUse)

                                                healPowa = min(
                                                    a.maxHp-a.hp, round(
                                                        skillToUse.power * (1+(statUse-max(actTurn.negativeHeal,actTurn.negativeShield,actTurn.negativeBoost))/100+(a.endurance/1000))
                                                        * actTurn.valueBoost(target=a,heal=True)
                                                        *actTurn.getElementalBonus(a,area=AREA_MONO,type=TYPE_HEAL)
                                                        *(1 + 0.006*actTurn.level)
                                                    )
                                                )

                                            elif stat == PURCENTAGE:
                                                healPowa = round(a.maxHP * skillToUse.power/100 * (100-a.healResist)/100)

                                            elif stat == None:
                                                healPowa = skillToUse.power

                                            funnyTempVarName = await actTurn.resurect(a,healPowa,skillToUse.emoji,danger=danger)
                                            tempTurnMsg += funnyTempVarName
                                            logs += funnyTempVarName
                                            resTabl.append(a)


                                        for eff in skillToUse.effect:
                                            if eff != None:
                                                ballerine = groupAddEffect(actTurn, actTurn, resTabl , eff, skillIcon=skillToUse.emoji)
                                                tempTurnMsg += ballerine
                                                logs += ballerine

                                    else: # Damage
                                        if skillToUse.ultimate and actTurn.char.aspiration == MAGE:
                                            tempTurnMsg += add_effect(actTurn,actTurn,classes.effect("Mage","effMage",None,turnInit=2,magie=actTurn.baseStats[MAGIE]*0.15,unclearable=True,emoji=uniqueEmoji(aspiEmoji[MAGE]),stackable=True))
                                            actTurn.refreshEffects()
                                        power = skillToUse.power

                                        if skillToUse.condition[:2] == [0,2]:
                                            for eff in actTurn.effect:
                                                if eff.effect.id in [tablElemEff[skillToUse.condition[2]],tablElemEff[ELEMENT_UNIVERSALIS_PREMO]]:
                                                    power = int(power*(1+eff.effect.power/100))
                                                    break

                                        if matriceUp:
                                            power = int(power*(100+matriceEff.power)/100)

                                        if skillToUse.id == memClemCastSkill.id:
                                            effect = classes.effect("Bouclier vampirique","clemMemSkillShield",overhealth=(actTurn.hp-1)//2,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji('<:clemMemento2:902222663806775428>'),absolutShield=True)
                                            tempTurnMsg += "{0} : - {1} PV\n".format(actTurn.icon,actTurn.hp-1)
                                            actTurn.hp = 1
                                            actTurn.maxHp, actTurn.healResist = actTurn.maxHp//2,actTurn.healResist//2
                                            tempTurnMsg += add_effect(actTurn,actTurn,effect,ignoreEndurance=True)
                                            defIncur50 = incur[5]
                                            defIncur50.turnInit, defIncur50.unclearable = -1,True
                                            tempTurnMsg += add_effect(actTurn,actTurn,defIncur50)

                                        elif skillToUse.id == krysUlt.id:
                                            totalArmor = 0
                                            for eff in ennemi.effect:
                                                if eff.effect.type == TYPE_ARMOR and not(eff.effect.absolutShield):
                                                    reduc = eff.value // 2
                                                    eff.value -= reduc
                                                    totalArmor += reduc
                                                    tempTurnMsg += "{0} {1} → -{2}{3}{4} ({5})\n".format(actTurn.icon,skillToUse.emoji,reduc,eff.icon,ennemi.icon,skillToUse.name)

                                            if totalArmor > 0:
                                                effect = classes.effect("Réassemblé","krysShieldy",overhealth=totalArmor,type=TYPE_ARMOR,turnInit=99,trigger=TRIGGER_DAMAGE)
                                                tempTurnMsg += add_effect(actTurn,actTurn,effect,ignoreEndurance=True)
                                                actTurn.refreshEffects()

                                        elif skillToUse.id == finalTech.id:
                                            pasCount = 0
                                            for eff in actTurn.effect:
                                                if eff.effect.id == pasTech.id:
                                                    pasCount += 1
                                                    eff.decate(turn=10)

                                            power = int(power* (1+0.35*pasCount))
                                            actTurn.refreshEffects()

                                        elif skillToUse.id in akikiSkillRageList:
                                            for cmpt in range(len(akikiSkillRageList)):
                                                if skillToUse.id == akikiSkillRageList[cmpt]:
                                                    power = int(power * (100+(akikiSkillRageBonus[cmpt]*((1-actTurn.hp/actTurn.maxHp)*100)))/100)
                                                    break

                                        elif skillToUse.id == theEnd.id:
                                            for eff in ennemi.effect:
                                                if eff.effect.id == reaperEff.id:
                                                    power = int(power*1.2)
                                                    break

                                        elif skillToUse.id == blueShell.id:
                                            tempTabl = tablEntTeam[int(not(actTurn.team))][:]
                                            for ent in tempTabl[:]:
                                                if ent.hp <= 0:
                                                    tempTabl.remove(ent)

                                            tempTabl.sort(key=lambda chocolatine: chocolatine.stats.damageDeal, reverse=True)
                                            if len(tempTabl) > 0:
                                                ennemi = tempTabl[0]

                                        if skillToUse.id == trans.id:
                                            actionStats, entActStats = 0, actTurn.actionStats()
                                            for cmpt in (0,1,2,3,4):
                                                if entActStats[cmpt] > entActStats[actionStats]:
                                                    actionStats = cmpt

                                        else:
                                            actionStats = skillToUse.useActionStats

                                        cmpt = 0
                                        while cmpt < skillToUse.repetition and ennemi.hp > 0 and skillToUse.power > 0:
                                            funnyTempVarName, temp = actTurn.attack(target=ennemi,value=power,icon=skillToUse.emoji,area=skillToUse.area,sussess=skillToUse.sussess,use=skillToUse.use,onArmor=skillToUse.onArmor,useActionStats=actionStats,setAoEDamage=skillToUse.setAoEDamage,lifeSteal = skillToUse.lifeSteal,erosion = skillToUse.erosion, skillPercing = skillToUse.percing)
                                            tempTurnMsg += funnyTempVarName
                                            logs += "\n"+funnyTempVarName
                                            deathCount += temp
                                            cmpt += 1
                                            if cmpt < skillToUse.repetition:
                                                tempTurnMsg += "\n"

                                        if skillToUse.effect!=[None]:
                                            tempTurnMsg += "\n"
                                            for a in skillToUse.effect:
                                                effect = findEffect(a)
                                                tempTurnMsg += add_effect(actTurn,ennemi,effect)
                                                logs += "\n{0} gave the {1} effect at {2} for {3} turn(s)".format(actTurn.char.name,effect.name,ennemi.char.name,effect.turnInit)

                                        if skillToUse.power > 0 and actTurn.specialVars["damageSlot"] != None:
                                            loose = int(actTurn.maxHp * (actTurn.specialVars["damageSlot"].effect.power/100))
                                            funnyTempVarName = "\n{0} : -{1} PV ({2})\n".format(actTurn.icon,loose,actTurn.specialVars["damageSlot"].effect.name)
                                            tempTurnMsg += funnyTempVarName
                                            logs + funnyTempVarName
                                            actTurn.hp -= loose
                                            actTurn.stats.selfBurn += loose
                                            if actTurn.hp <= 0:
                                                tempTurnMsg += actTurn.death(killer=actTurn)

                                            actTurn.refreshEffects()

                                        if actTurn.isNpc("Ailill") and skillToUse.id == "headnt":
                                            ennemi.stats.headnt = True
                                            ennemi.status = STATUS_TRUE_DEATH
                                # =================================================================
                                # Knockback
                                if skillToUse.knockback > 0:
                                    temp = actTurn.knockback(ennemi,skillToUse.knockback)
                                    tempTurnMsg += temp
                                    logs += temp

                                # JumpBack
                                if skillToUse.jumpBack > 0:
                                    temp = actTurn.jumpBack(skillToUse.jumpBack,ennemi.cell)
                                    tempTurnMsg += temp
                                    logs += temp

                                # Does the skill give a effect on the caster ?
                                if skillToUse.effectAroundCaster != None:
                                    if skillToUse.effectAroundCaster[0] == TYPE_HEAL:
                                        for a in actTurn.cell.getEntityOnArea(area=skillToUse.effectAroundCaster[1],team=actTurn.team,wanted=ALLIES,directTarget=False):
                                            funnyTempVarName, useless = actTurn.heal(a, skillToUse.emoji, skillToUse.use, skillToUse.effectAroundCaster[2],danger=danger, mono = skillToUse.area == skillToUse.effectAroundCaster[1], useActionStats = skillToUse.useActionStats)
                                            tempTurnMsg += funnyTempVarName
                                            logs += funnyTempVarName
                                    elif skillToUse.effectAroundCaster[0] == TYPE_DAMAGE:
                                        funnyTempVarName, temp = actTurn.attack(target=ennemi,value=skillToUse.effectAroundCaster[2],icon=skillToUse.emoji,area=skillToUse.effectAroundCaster[1],sussess=skillToUse.sussess,use=skillToUse.use,onArmor=skillToUse.onArmor,useActionStats=actionStats,setAoEDamage=skillToUse.setAoEDamage,lifeSteal = skillToUse.lifeSteal)
                                        tempTurnMsg += funnyTempVarName
                                        logs += "\n"+funnyTempVarName
                                    elif type(skillToUse.effectAroundCaster[2]) == classes.effect:
                                        tablName, tablEff, tablIcon = [], [], []
                                        for ent in ennemi.cell.getEntityOnArea(area=skillToUse.effectAroundCaster[1],team=actTurn.team,wanted=ALLIES,directTarget=False):
                                            eff = skillToUse.effectAroundCaster[2]
                                            ballerine = add_effect(actTurn,ent,eff,danger=danger)
                                            if eff.type == TYPE_ARMOR:
                                                tempTurnMsg += ballerine
                                                logs += "\n{0} gave the {1} eff at {2} for {3} turn(s)".format(actTurn.char.name,eff.name,ent.char.name,eff.turnInit)
                                            else:
                                                if '🚫' not in ballerine and ballerine != "":
                                                    if eff.name not in tablEff:
                                                        tablEff.append(eff.name)
                                                        tablIcon.append(eff.emoji[actTurn.char.species-1][actTurn.team])
                                                        tablName.append(["{0}".format(ent.icon,ent.name)])
                                                    else:
                                                        for cmpt in range(len(tablEff)):
                                                            if tablEff[cmpt] == eff.name:
                                                                tablName[cmpt].append("{0}".format(ent.icon,ent.name))
                                                                break
                                            ent.refreshEffects()

                                        if tablEff != []:
                                            temp = ""
                                            for cmpt2 in range(len(tablName[0])):
                                                temp += tablName[0][cmpt2]

                                            temp = "{1} {2} → {3} +{0}{4}\n".format(tablIcon[0],actTurn.icon,skillToUse.emoji,temp,["({0}%)".format(skillToUse.effPowerPurcent),""][skillToUse.effPowerPurcent < 100])
                                            tempTurnMsg += temp
                                            logs += temp
                                    elif skillToUse.effectAroundCaster[0] == TYPE_RESURECTION:
                                        stat = skillToUse.use

                                        for a in actTurn.cell.getEntityOnArea(area=skillToUse.effectAroundCaster[1],team=actTurn.team,wanted=ALLIES,dead=True,directTarget=False):
                                            if stat != HARMONIE:
                                                statUse = actTurn.allStats()[stat]
                                            else:
                                                temp = actTurn.allStats()
                                                for b in temp:
                                                    statUse = max(b,statUse)

                                            healPowa = min(
                                                a.maxHp-a.hp, round(
                                                    skillToUse.effectAroundCaster[2] * (1+(statUse-max(actTurn.negativeHeal,actTurn.negativeShield,actTurn.negativeBoost))/100+(a.endurance/1000))
                                                    * actTurn.valueBoost(target=a,heal=True)
                                                    *actTurn.getElementalBonus(a,area=AREA_MONO,type=TYPE_HEAL)
                                                    *(1 + 0.006*actTurn.level)
                                                )
                                            )

                                            funnyTempVarName = await actTurn.resurect(a,healPowa,skillToUse.emoji,danger=danger)
                                            tempTurnMsg += funnyTempVarName
                                            logs += funnyTempVarName
                                            bigRaiseCount += 1

                                if skillToUse.effectOnSelf != None:
                                    if not(findEffect(skillToUse.effectOnSelf).silent):
                                        tempTurnMsg += "\n"
                                    eff = findEffect(skillToUse.effectOnSelf)
                                    if eff.replica != None:
                                        tempTurnMsg += add_effect(actTurn,actTurn,eff,setReplica=ennemi)
                                    else:
                                        tempTurnMsg += add_effect(actTurn,actTurn,eff,skillIcon = skillToUse.emoji)
                                    actTurn.refreshEffects()

                                if skillToUse.id in useElemEffId and useEffElem > 0:
                                    if skillToUse.id == useElemEffId[0]:
                                        burn = classes.effect("Brûlure","catFireEff",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,power=int(skillToUse.power*0.33),turnInit=useEffElem,lvl=useEffElem)
                                        ballerine = groupAddEffect(actTurn, ennemi, skillToUse.area, burn, skillToUse.emoji)
                                        logs += ballerine
                                        tempTurnMsg += ballerine
                                    elif skillToUse.id == useElemEffId[5]:
                                        burn = classes.effect("Flamme sombre","catDarkEff",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,area=skillToUse.area,power=int(skillToUse.power*0.5),turnInit=useEffElem,lvl=useEffElem)
                                        ballerine = groupAddEffect(actTurn, ennemi, AREA_MONO, burn, skillToUse.emoji)
                                        logs += ballerine
                                        tempTurnMsg += ballerine
                                    elif skillToUse.id == useElemEffId[4]:
                                        burn = classes.effect("Régénération de lumière","catLightEff",INTELLIGENCE,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_END_OF_TURN,power=int(skillToUse.effect[0].overhealth*0.2),turnInit=3)
                                        ballerine = groupAddEffect(actTurn, ennemi, skillToUse.area, burn, skillToUse.emoji, effPurcent = 100 * useEffElem)
                                        logs += ballerine
                                        tempTurnMsg += ballerine
                                    elif skillToUse.id == useElemEffId[7]:
                                        burn = classes.effect("Armure temporelle","catTimeEff",CHARISMA,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,overheath=int(skillToUse.power*0.2*useEffElem),turnInit=3)
                                        ballerine = groupAddEffect(actTurn, ennemi, skillToUse.area, burn, skillToUse.emoji)
                                        logs += ballerine
                                        tempTurnMsg += ballerine
                                    elif skillToUse.id == useElemEffId[2]:
                                        burn = classes.effect("Brûlure du vent","catAirEff",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,power=int(skillToUse.power*0.40),turnInit=useEffElem,lvl=useEffElem)
                                        ballerine = groupAddEffect(actTurn, actTurn, AREA_MONO, burn, skillToUse.emoji)
                                        logs += ballerine
                                        tempTurnMsg += ballerine
                                    elif skillToUse.id == useElemEffId[1]:
                                        cmpt = 0
                                        while cmpt < useEffElem:
                                            ballerine = actTurn.attack(ennemi,int(skillToUse.power*0.15),skillToUse.emoji,AREA_MONO,skillToUse.sussess,use=MAGIE,skillPercing=skillToUse.percing)
                                            logs += ballerine
                                            tempTurnMsg += ballerine
                                            cmpt += 1
                                    elif skillToUse.id == useElemEffId[3]:
                                        ballerine = actTurn.attack(actTurn,int(skillToUse.power*0.2*useElemEffId),skillToUse.emoji,AREA_DONUT_2,skillToUse.sussess,use=MAGIE,skillPercing=skillToUse.percing)
                                        logs += ballerine
                                        tempTurnMsg += ballerine
                                    else:
                                        tablTargets = ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENNEMIS,directTarget=False)
                                        cmpt = 0
                                        while cmpt < useEffElem and len(tablTargets) > 0:
                                            if len(tablTargets) > 1:
                                                target = tablTargets[random.randint(0,len(tablTargets))]
                                            else:
                                                target = tablTargets[0]

                                            ballerine = actTurn.attack(target,int(skillToUse.power*0.33),skillToUse.emoji,AREA_CIRCLE_1,skillToUse.sussess,use=MAGIE,skillPercing=skillToUse.percing)
                                            logs += ballerine
                                            tempTurnMsg += ballerine
                                            if target.hp <= 0:
                                                tablTargets.remove(target)
                                            cmpt += 1

                                # Memento Angel's Path anti-despawn flag
                                if skillToUse.id == memAlice2.id:
                                    aliceMemCastTabl[actTurn.team] = True
                                elif skillToUse.id == memAlice.id:
                                    aliceMemCastTabl[actTurn.team] = False

                                # Blood cost
                                if actTurn.isNpc("Clémence pos.") or actTurn.isNpc("Alice Exaltée"):
                                    for skillID, cost in clemBJcost.items():
                                        if skillToUse.id == skillID:
                                            actTurn.specialVars["clemBloodJauge"].value = max(0,actTurn.specialVars["clemBloodJauge"].value - cost)
                                            if actTurn.specialVars["clemBloodJauge"].value == 0:
                                                tempTurnMsg += "\nLa Jauge de Sang se brise !\n"
                                                if actTurn.isNpc("Clémence pos."):
                                                    tempTurnMsg += add_effect(actTurn, actTurn, clemStunEffect)
                                                    temp = copy.deepcopy(vulneTabl[3])
                                                    temp.turnInit = 3
                                                    tempTurnMsg += add_effect(actTurn, actTurn, temp)
                                                else:
                                                    tempTurnMsg += add_effect(actTurn, actTurn, aliceStunEffect)
                                                
                                                loose = actTurn.maxHp // 10
                                                tempTurnMsg += "{0} : -{1} PV\n".format(actTurn.icon,loose)
                                                actTurn.hp -= loose
                                                if actTurn.hp <= 0:
                                                    tempTurnMsg += actTurn.death(killer=actTurn)

                                                actTurn.refreshEffects()
                                            break

                                if skillToUse.maxHpCost > 0:
                                    diff = actTurn.maxHp - int(actTurn.maxHp * (1-(skillToUse.maxHpCost/100)))
                                    actTurn.maxHp = int(actTurn.maxHp * (1-(skillToUse.maxHpCost/100)))
                                    diff2 = min(0,actTurn.maxHp-actTurn.hp)
                                    actTurn.hp = min(actTurn.hp,actTurn.maxHp)
                                    tempTurnMsg += "\n{0} : -{1} PV max\n".format(actTurn.icon,diff)
                                    actTurn.stats.selfBurn += diff2

                                if skillToUse.hpCost > 0:
                                    diff = actTurn.hp - int(actTurn.hp * (1-(skillToUse.hpCost/100)))
                                    actTurn.hp -= diff
                                    tempTurnMsg += "\n{0} : -{1} PV\n".format(actTurn.icon,diff)
                                    actTurn.stats.selfBurn += diff

                                    if actTurn.hp <= 0:
                                        tempTurnMsg += actTurn.death(killer=actTurn)

                                if skillToUse.replay:
                                    replay = skillToUse.replay

                                if skillToUse.condition[:2] == [0,2] and random.randint(0,99) < mEP:
                                    for eff in actTurn.effect:
                                        if eff.effect.id == matriseElemEff.id:
                                            ballerine = add_effect(actTurn,actTurn,matriseElemEff.callOnTrigger,skillIcon=matriseElemEff.emoji[0][0])
                                            actTurn.refreshEffects()
                                            tempTurnMsg += ballerine
                                            logs += ballerine

                                if skillToUse.id in tablRosesSkillsId and skillToUse.effectOnSelf == None: # Final Floral
                                    if skillToUse.id in tablRosesSkillsId[:-2]:
                                        for skilly in actTurn.char.skills:
                                            skilly = findSkill(skilly)
                                            if skilly != None and skilly.id == finalFloral.id:
                                                roseCount = 0
                                                for eff in actTurn.effect:
                                                    if eff.effect.id in tablRosesId:
                                                        roseCount += 1

                                                if roseCount < 3:
                                                    for cmpt in range(len(tablRosesSkillsId[:-2])):
                                                        if skillToUse.id == tablRosesSkillsId[:-2][cmpt]:
                                                            ballerine = add_effect(actTurn,actTurn,tablRosesEff[cmpt],skillIcon=skillToUse.emoji)
                                                            actTurn.refreshEffects()
                                                            logs += ballerine
                                                            tempTurnMsg += ballerine

                                                            roseCount += 1
                                                            if roseCount >= 3:
                                                                ballerine = add_effect(actTurn,actTurn,finFloCast,skillIcon=finalFloral.emoji,setReplica=actTurn)
                                                                actTurn.refreshEffects()
                                                                logs += ballerine
                                                                tempTurnMsg += ballerine
                                                            break
                                                break
                                    else:
                                        for ent in tablEntTeam[actTurn.team]:
                                            for skilly in ent.char.skills:
                                                skilly = findSkill(skilly)
                                                if skilly != None and skilly.id == finalFloral.id:
                                                    roseCount = 0
                                                    for eff in ent.effect:
                                                        if eff.effect.id in tablRosesId:
                                                            roseCount += 1

                                                    if roseCount < 3:
                                                        for cmpt in range(len(tablRosesSkillsId[:-2])):
                                                            if skillToUse.id == tablRosesSkillsId[:-2][cmpt]:
                                                                ballerine = add_effect(ent,ent,tablRosesEff[cmpt],skillIcon=skillToUse.emoji)
                                                                ent.refreshEffects()
                                                                logs += ballerine
                                                                tempTurnMsg += ballerine

                                                                roseCount += 1
                                                                if roseCount >= 3:
                                                                    ballerine = add_effect(ent,ent,finFloCast,skillIcon=finalFloral.emoji,setReplica=ent)
                                                                    ent.refreshEffects()
                                                                    logs += ballerine
                                                                    tempTurnMsg += ballerine
                                                                break
                                                    break

                                # ============================= Interactions =============================
                                if skillToUse.id == strengthOfWill.id and actTurn.isNpc("Félicité") and dictIsPnjVar["Clémence"]:       # Féli / Clem
                                    tempTurnMsg += "<:felicite:909048027644317706> : *\"Alors Clémence :D ? Combien combien ?\"*\n<:clemence:908902579554111549> : *\"Hum... {0} sur 20\"*\n<:felicite:909048027644317706> : :D\n".format(random.randint(15,22))

                                if skillToUse.id == onstage.id and dictIsPnjVar["Alice"] and not(actTurn.isNpc("Alice")):               # Alice
                                    alice = None
                                    for team in [0,1]:
                                        for ent in tablEntTeam[team]:
                                            if ent.isNpc("Alice"):
                                                alice = ent
                                                break
                                        if alice != None:
                                            break

                                    damage = round(25 * (alice.charisma+100-alice.negativeBoost)/100 * (1-(min(95,actTurn.resistance*(1-alice.percing/100))/100))*alice.getElementalBonus(target=actTurn,area=AREA_MONO,type=TYPE_INDIRECT_DAMAGE)*(1+(0.01*alice.level)))
                                    murcialago = "\n"+alice.indirectAttack(target=actTurn,value=damage,icon="",ignoreImmunity=True,name='Coup bas',hideAttacker=True)
                                    tempTurnMsg += murcialago
                                    logs += "\nAlice wasn't verry happy about that\n"+murcialago

                                if skillToUse.effectOnSelf != None and findEffect(skillToUse.effectOnSelf).replica != None and skillToUse.power == 0 and skillToUse.effect == [None]:
                                    tempTurnMsg += "{0} charge la compétence __{1}__\n".format(actTurn.name,skillToUse.name)

                                if skillToUse.id == unHolly.id and (ennemi.isNpc("Liu") or ennemi.isNpc("Lia") or ennemi.isNpc("Liz") or ennemi.isNpc("Lio") or ennemi.isNpc("Kitsune")):
                                    funnyMsg, funnyMsgTabl, tablKitsunes, tablEffectGiven = "", ["Oh tu veux jouer à ça ?","Oh ^^ Mon tour maintenant !","C'est mignon x) Mais tu va apprendre à un vieux singe à faire la grimace","Tu l'as cherché...","^^ Laisse moi te montrer comment il faut faire"], [ennemi.isNpc("Liu"),ennemi.isNpc("Lia"),ennemi.isNpc("Liz"),ennemi.isNpc("Lio"),ennemi.isNpc("Kitsune")], [3,5,5,3,10]
                                    for cmpt in range(5):
                                        if tablKitsunes[cmpt]:
                                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ennemi.icon,funnyMsgTabl[cmpt])
                                            for cmpt2 in range(tablEffectGiven[cmpt]):
                                                add_effect(ennemi,actTurn,charming)
                                            tempTurnMsg += "\n{0} → {1} +{2} x{3}".format(ennemi.icon,actTurn.icon,charming.emoji[0][1],tablEffectGiven[cmpt])
                                            break

                                try:                # Big raise
                                    if actTurn.stats.allieResurected - allyRea >= 3:
                                        if actTurn.char.says.bigRaise != None:
                                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,actTurn.char.says.bigRaise.format(skill=skillToUse.name))
                                        tablReact = []
                                        for team in [0,1]:
                                            for ent in tablEntTeam[team]:
                                                if [ent.char.says.reactBigRaiseEnnemy,ent.char.says.reactBigRaiseAllie][ent.team == actTurn.team] != None:
                                                    tablReact.append([ent.icon,[ent.char.says.reactBigRaiseEnnemy,ent.char.says.reactBigRaiseAllie][ent.team == actTurn.team]])

                                        if len(tablReact) != 0:
                                            if len(tablReact) == 1:
                                                rand = 0
                                            else:
                                                rand = random.randint(0,len(tablReact)-1)
                                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(tablReact[rand][0],tablReact[rand][1].format(caster=actTurn.char.name,skill=skillToUse.name))
                                except:
                                    tempTurnMsg += "\n__Error with the BigRaisesReaction.__ See logs for more informations"
                                    logs += "\n"+format_exc()

                            if actTurn.stats.fullskip and optionChoice != OPTION_SKIP:
                                actTurn.stats.fullskip = False

                            if actTurn.isNpc("Luna prê.") and optionChoice == OPTION_SKILL and skillToUse.id in [lunaSpe.id,lunaSpeCast.id]:
                                replay = False

                            if not(replay or (optionChoice == OPTION_MOVE and not(allReadyMove))):
                                break
                            else:
                                replay = False
                                if optionChoice != OPTION_MOVE:
                                    tempTurnMsg += "\n__{0} rejoue son tour !__\n".format(actTurn.char.name)
                                tempTurnMsg += lunaUsedQuickFight
                                if optionChoice == OPTION_MOVE and not(allReadyMove):
                                    allReadyMove = True

                                if not(auto) and not(actTurn.auto):   # Sending the Turn message
                                    if len(tempTurnMsg) > 4096:
                                        tempTurnMsg = unemoji(tempTurnMsg)
                                        if len(tempTurnMsg) > 4096:
                                            tempTurnMsg = "OVERLOAD"
                                    await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color))
                                    await asyncio.sleep(3)
                    # ==========================================
                    # Else, the entity is stun
                    else:                                   # The entity is, in fact, stun
                        temp = ""
                        if tablEntTeam[1][0].isNpc("Luna prê."):
                            for eff in actTurn.effect:
                                if eff.effect.id == lunaInfiniteDarknessStun.id:
                                    temp = actTurn.quickEvent(stat=ENDURANCE, required=int(250*(1+0.3*int(actTurn.char.element != ELEMENT_LIGHT))), danger=danger, effIfFail=lunaVulne, fromEnt=tablEntTeam[1][0])[0]
                                    break
                            if temp == "":
                                temp = f"\n{actTurn.char.name} est étourdi{actTurn.accord()} !\n"
                        else:
                            temp = f"\n{actTurn.char.name} est étourdi{actTurn.accord()} !\n"
                        tempTurnMsg += temp
                        logs += "{0} is stun\n".format(actTurn.name)
                        optionChoice = OPTION_SKIP

                    funnyTempVarName = "\n__Fin du tour__\n"+actTurn.endOfTurn(danger)
                    logs += funnyTempVarName
                    tempTurnMsg += funnyTempVarName
                    timeNow = (datetime.now() - nowStartOfTurn)/timedelta(microseconds=1000)
                    logs += "Turn duration : {0} ms{1}\n".format(timeNow,[" (Manual fighter)",""][int(actTurn.auto)])
                    if timeNow > 500 and actTurn.auto:
                        longTurn = True
                        longTurnNumber.append({"turn":tour,"ent":actTurn.char.name,"duration":timeNow})

                    if not(auto):   # Sending the Turn message
                        if len(tempTurnMsg) > 4096:
                            tempTurnMsg = unemoji(tempTurnMsg)
                            if len(tempTurnMsg) > 4096:
                                tempTurnMsg = "OVERLOAD"

                        nbTry = 0
                        while 1:
                            try:
                                if optionChoice == OPTION_SKILL and skillToUse.url != None:
                                    await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color).set_image(url=skillToUse.url))
                                else:
                                    await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color))
                                break
                            except SocketError as e:
                                if e.errno not in [errno.ECONNRESET,503]:
                                    raise
                                else:
                                    if nbTry < 5:
                                        await asyncio.sleep(1)
                                        nbTry += 1
                                        errorNb += 1
                                        logs += "\nConnexion error... retrying..."
                                    else:
                                        logs += "\nConnexion lost"
                                        raise

                        if type(actTurn.char) != invoc:
                            await asyncio.sleep(2+(min(len(tempTurnMsg),1500)/1500*5))
                        else:
                            await asyncio.sleep(2+(min(len(tempTurnMsg),2000)/2000*5))

                    potgValue = (None,0)

                    for team in (0,1):
                        for ent in tablEntTeam[team]:
                            tempPotgValue = ent.stats.damageDeal-potgDamages[team][ent.id]+(ent.stats.ennemiKill-potgKills[team][ent.id])*ent.char.level*10+ent.stats.heals-potgHeal[team][ent.id]+(ent.stats.allieResurected-potgRaises[team][ent.id])*ent.char.level*15+ent.stats.armoredDamage-potgArmored[team][ent.id]
                            if tempPotgValue > potgValue[1]:
                                potgValue = (ent,tempPotgValue)

                    if potgValue[1] > playOfTheGame[0]:
                        if optionChoice == OPTION_SKILL and skillToUse.url != None:
                            playOfTheGame = [potgValue[1],potgValue[0],discord.Embed(title=f"__Action du combat\nTour {tour}__",description=tempTurnMsg,color = potgValue[0].char.color).set_image(url=skillToUse.url)]
                        else:
                            playOfTheGame = [potgValue[1],potgValue[0],discord.Embed(title=f"__Action du combat\nTour {tour}__",description=tempTurnMsg,color = potgValue[0].char.color)]
                # =========================================

                # End of the turn - timeline stuff ------------------------------------------------------------------
                tablEntTeam,tablAliveInvoc = time.endOfTurn(tablEntTeam,tablAliveInvoc)

                for team in [0,1]:                      # Does a team is dead ?
                    for ent in tablEntTeam[team]:
                        if ent.hp > 0 and type(ent.char) != invoc:
                            everyoneDead[team] = False
                            break

                if everyoneDead[0] or everyoneDead[1]:  # If Yes, ending the fight
                    fight = False

            # End of the fight ============================
            logs += "\n\n================= End of the fight ================="
        except:
            for team in listImplicadTeams:
                teamWinDB.changeFighting(team,0)
            logs += "\n"+format_exc()
            date = datetime.now()+horaire
            date = date.strftime("%H%M")
            fich = open("./data/fightLogs/ERROR_{0}_{1}.txt".format(ctx.author.name,date),"w")
            if not(isLenapy):
                try:
                    fich.write(logs.replace('\u2192','prohibited'))
                except:
                    print(format_exc())
                    fich.write("Voir la console")
            else:
                fich.write(logs)
            fich.close()
            opened = open("./data/fightLogs/ERROR_{0}_{1}.txt".format(ctx.author.name,date),"rb")
            await asyncio.sleep(1)
            desc = format_exc()
            try:
                await ctx.send(content="{0} : Une erreur est survenue".format(ctx.author.mention),file=discord.File(fp=opened),embed=discord.Embed(title=["Descriptif de l'erreur","Une erreur de communication prolongée est survenue"]["aiohttp.client_exceptions.ClientOSError: [Errno 104] Connection reset by peer" in logs],description=desc))
            except:
                await ctx.channel.send(file=discord.File(fp=opened),embed=discord.Embed(title=["Une erreur est survenue durant le combat","Une erreur de communication prolongée est survenue"]["aiohttp.client_exceptions.ClientOSError: [Errno 104] Connection reset by peer" in logs],description=desc))
            opened.close()

            if isLenapy:
                chan = await bot.fetch_channel(808394788126064680)
                opened = open("./data/fightLogs/ERROR_{0}_{1}.txt".format(ctx.author.name,date),"rb")
                await asyncio.sleep(1)
                await chan.send("Une erreur est survenue durant le combat",file=discord.File(fp=opened))
                opened.close()
            haveError = True
        # ===============================================================================================
        #                                       Post Fight Things
        # ===============================================================================================
        if not(haveError):
            print(ctx.author.name + " a fini son combat")

            for a in range(0,len(tablEntTeam[0])):      # Reload the char files (in case of changes)
                if type(tablEntTeam[0][a].char) == char:
                    tablEntTeam[0][a].char = loadCharFile(absPath + "/userProfile/" + str(tablEntTeam[0][a].char.owner) + ".prof")

            for a in range(0,len(tablEntTeam[1])):      # Reload the char files (in case of changes)
                if type(tablEntTeam[1][a].char) == char:
                    tablEntTeam[1][a].char = loadCharFile(absPath + "/userProfile/" + str(tablEntTeam[1][a].char.owner) + ".prof")

            if not(everyoneDead[1] and everyoneDead[0]):        # The winning team. 0 -> Blue, 1 -> Red
                winners = int(not(everyoneDead[1]))
            else:
                winners = 1

            if not(octogone and team2[0].isNpc('Lena') and len(team2) == 1 and not(winners)):               # None Special fights
                for z in (0,1):
                    for a in tablEntTeam[z]:
                        if type(a.char) == invoc:
                            a.hp = 0

                tablEntTeam,tablAliveInvoc = time.endOfTurn(tablEntTeam,tablAliveInvoc)

                temp = tablEntTeam[:]
                temp = temp[0]+temp[1]

                dptClass = sorted(temp,key=lambda student: student.stats.damageDeal,reverse=True)
                for a in dptClass[:]:
                    if a.stats.damageDeal < 1:
                        dptClass.remove(a)
                healClass = sorted(temp,key=lambda student: student.stats.heals,reverse=True)
                for a in healClass[:]:
                    if a.stats.heals < 1:
                        healClass.remove(a)
                shieldClass = sorted(temp,key=lambda student: student.stats.armoredDamage,reverse=True)
                for a in shieldClass[:]:
                    if a.stats.shieldGived < 1:
                        shieldClass.remove(a)
                suppClass = sorted(temp,key=lambda student: student.stats.damageBoosted + student.stats.damageDogded,reverse=True)
                for a in suppClass[:]:
                    if a.stats.damageBoosted + a.stats.damageDogded < 1:
                        suppClass.remove(a)

                listClassement = [dptClass,healClass,shieldClass,suppClass]

                if not(octogone):
                    teamWinDB.addResultToStreak(mainUser,everyoneDead[1])
                    team = mainUser.team
                    if isLenapy:
                        teamWinDB.refreshFightCooldown(team,auto,fromTime=now)

                tablSays = []
                temp= ["",""]
                for a in [0,1]:
                    for b in tablEntTeam[a]:
                        if type(b.char) != char:
                            icon = b.char.icon
                        else:
                            icon = await getUserIcon(bot,b.char)

                        raised = ""
                        if b.status == STATUS_RESURECTED and b.raiser != None:
                            raised = " ({1}{0})".format(b.raiser,['<:rezB:907289785620631603>','<:rezR:907289804188819526>'][b.team])
                        elif b.status == STATUS_TRUE_DEATH and b.raiser != None:
                            raised = " ({0})".format(['<:diedTwiceB:907289950301601843>','<:diedTwiceR:907289935663485029>'][b.team])

                        temp[a] += f"{b.icon} {b.char.name}{b.getMedals(listClassement)}{raised}\n"
                        if type(b.char) == octarien and b.char.oneVAll:
                            if a == 1 and winners and b.char.says.redWinAlive != None and b.hp > 0:
                                for cmpt in (0,1,2,3,4,5):
                                    tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redWinAlive)]

                            elif a == 1 and not(winners) and b.char.says.redLoose != None:
                                for cmpt in (0,1,2,3):
                                    tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redLoose)]

                        else:
                            if a == 0 and not(winners) and b.char.says.blueWinAlive != None and b.hp > 0:
                                for cmpt in (0,1):
                                    tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.blueWinAlive)]
                            elif a == 0 and not(winners) and b.char.says.blueWinDead != None and b.hp <= 0:
                                tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.blueWinDead)]
                            elif a == 0 and winners and b.char.says.blueLoose != None:
                                tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.blueLoose)]
                            elif a == 1 and winners and b.char.says.redWinAlive != None and b.hp > 0:
                                for cmpt in (0,1):
                                    tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redWinAlive)]
                            elif a == 1 and winners and b.char.says.redWinDead != None and b.hp <= 0:
                                tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redWinDead)]
                            elif a == 1 and not(winners) and b.char.says.redLoose != None:
                                tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redLoose)]

                    if len(temp[a]) > 1024:
                        tabl = ["<:topDpt:884337213670838282>","<:secondDPT:884337233241448478>","<:thirdDPT:884337256905732107>","<:topHealer:884337335410491394>","<:secondHealer:884337355262160937>","<:thirdHealer:884337368407093278>","<:topArmor:884337281547272263>","<:secondArmor:884337300975276073>","<:trdArmor:911071978163675156>","<:topSupp:911071783787065375>","<:sndSupp:911071803424788580>","<:trdSupp:911071819388313630>","<:rezB:907289785620631603>","<:rezR:907289804188819526>","<:diedTwiceB:907289950301601843>","<:diedTwiceR:907289935663485029>"]
                        tablName = ["1stDpt","2ndDPT","3rdDPT","1stHealer","2ndHealer","3rdHealer","1stArmor","2ndArmor","3rdArmor","1stSupp","2ndSupp","3rdSupp","Réa: ","Réa: ","D.D","D.D"]
                        for cmpt in range(len(tabl)):
                            temp[a] = temp[a].replace(tabl[cmpt],tablName[cmpt])

                say = ""
                if len(tablSays) > 1:
                    say = "\n\n{0}".format(tablSays[random.randint(0,len(tablSays)-1)])
                elif len(tablSays) == 1:
                    say = "\n\n{0}".format(tablSays[0])
        
                duree = datetime.now()
                nowTemp = duree - now
                nowTemp = str(nowTemp.seconds//60) + ":" + str(nowTemp.seconds%60)

                if not(octogone):
                    nextFigth = now + timedelta(hours=1+(2*auto)) + horaire
                    nextFightMsg = "\n__Prochain combat {0}__ : {1}".format(["normal","rapide"][auto],nextFigth.strftime("%Hh%M"))
                else:
                    nextFightMsg = ""

                resultEmbed = discord.Embed(title = "__Résultats du combat :__",color = [[0x2996E5,0x818181][danger<100],red][winners],description="__Danger :__ {0}\n__Nombre de tours :__ {1}\n__Durée :__ {2}{4}{3}".format(danger,tour,nowTemp,say,nextFightMsg))
                resultEmbed.add_field(name="<:empty:866459463568850954>\n__Vainqueurs :__",value=temp[winners],inline=True)
                resultEmbed.add_field(name="<:empty:866459463568850954>\nPerdants :",value=temp[not(winners)],inline=True)

                if longTurn:
                    resultEmbed.set_footer(text="{0} tour{1} anormalement long{1} {2} été détecté{1} durant le combat. Un rapport va être envoyé".format(len(longTurnNumber),["",'s'][int(len(longTurnNumber) > 1)],["a","ont"][int(len(longTurnNumber) > 1)]))

                endOfFightStats = copy.deepcopy(tablEntTeam)
                if procurFight:
                    team1 = []
                    user = loadCharFile("./userProfile/{0}.prof".format(ctx.author_id))
                    if user.team != 0:
                        for a in userTeamDb.getTeamMember(user.team):
                            team1 += [loadCharFile(absPath + "/userProfile/{0}.prof".format(a))]
                    else:
                        team1 = [user]

                    tablEntTeam[0], cmpt = [], 0
                    for user in team1:
                        tablEntTeam[0].append(entity(cmpt,user,0,danger=danger,dictInteraction=dictIsPnjVar))
                        cmpt+=1

                # Gain rolls and defenitions -------------------------------------------------
                if not(octogone):
                    gainExp, gainCoins, allOcta, gainMsg, listLvlUp = tour,tour*20,True,"", []
                    # Base Exp Calculation
                    for a in tablEntTeam[1]:
                        if type(a.char) == octarien:
                            if a.hp <= 0:
                                gainExp += a.char.exp
                            elif a.status == STATUS_RESURECTED:
                                gainExp += int(a.char.exp/2)
                        elif type(a.char) == tmpAllie:
                            if a.hp <= 0:
                                gainExp += 8
                            elif a.status == STATUS_RESURECTED:
                                gainExp += 4
                        else:
                            allOcta = False

                    truc = 0
                    logs += "\n\n"

                    # Win streak little exp boost
                    try:
                        if winStreak > 7:
                            truc = (winStreak-7) * 0.05
                    except:
                        pass

                    # None complete team exp boost
                    if not(procurFight):
                        multi = max(1,8/len(team1)+truc)
                    else:
                        multi = 1

                    gainInit = str(gainExp)
                    gainExp = int(gainExp*multi)
                    if winners:
                        gainCoins = gainCoins//2

                    logs += "Gains exp : {0} ({1} * {2})\n".format(gainExp,gainInit,multi)
                    gainMsg = f"Pièces : {gainCoins}"

                    maxLevel = -1
                    for players in tablEntTeam[0]:
                        maxLevel = max(players.char.level, maxLevel)

                    for a in tablEntTeam[0]: #Attribution de l'exp et loot
                        tempLevel = tablEntTeam[0][:]
                        tempLevel.sort(key=lambda sorting : sorting.char.level, reverse=True)
                        maxLevlDiff = tempLevel[0].char.level - tempLevel[len(tempLevel)-1].char.level
                        if type(a.char) == char and a.char.team == mainUser.team:
                            path = absPath + "/userProfile/" + str(a.char.owner) + ".prof"

                            veryLate = 1 + (int(maxLevel-a.char.level > 10 and winners) * 0.5)
                            if a.char.level < 55:
                                baseGain = gainExp+(a.medals[0]*3)+(a.medals[1]*2)+(a.medals[2]*1)+int((maxLevel-a.char.level)/2)
                            else:
                                baseGain = 0
                            effectiveExpGain = int(baseGain*(1+0.02*(min(10,maxLevel-a.char.level)))*veryLate*[1,1.5][a.char.stars > 0 and a.char.level <=30] * (1+(maxLevlDiff <= 5 * 0.2)+(a.auto*0.1)))
                            temp = (a.char.level, a.char.stars)
                            a.char = await addExpUser(bot,path,ctx,exp=effectiveExpGain,coins=gainCoins,send=False)

                            if (a.char.level, a.char.stars) != temp:
                                listLvlUp.append("{0} : Niv. {1}{2} → Niv. {3}{4}\n".format(await a.getIcon(bot),temp[0],["","<:littleStar:925860806602682369>{0}".format(temp[1])][temp[1]>0],a.char.level,["","<:littleStar:925860806602682369>{0}".format(a.char.stars)][a.char.stars>0]))

                            if effectiveExpGain > 0:
                                gainMsg += "\n{0} → <:exp:926106339799887892> +{1}".format(await getUserIcon(bot,a.char),effectiveExpGain)

                            if baseGain != effectiveExpGain:
                                logs += "\n{0} got a {1}% exp boost (total : +{2} exp)".format(a.char.name,int((effectiveExpGain/baseGain-1)*100),effectiveExpGain)

                            sussesfullRoll = random.randint(0,99) < [25,35,55][int(userShopPurcent(a.char)<90)+int(userShopPurcent(a.char)<25)]
                            #sussesfullRoll = False
                            if sussesfullRoll and allOcta and not(winners):
                                logs += "\n{0} have loot :".format(a.char.name)
                                drop = listAllBuyableShop[:]
                                temp = drop[:]

                                for b in drop:
                                    if a.char.have(obj=b) or (type(b)==stuff and b.minLvl > a.char.level + 5):
                                        temp.remove(b)

                                if len(temp) > 0:
                                    rand = temp[random.randint(0,len(temp)-1)]
                                    newTemp = whatIsThat(rand)
                                    logs += " {0}".format(rand.name)

                                    if newTemp == 0:
                                        a.char.weaponInventory += [rand]
                                    elif newTemp == 1:
                                        a.char.skillInventory += [rand]
                                    elif newTemp == 2:
                                        a.char.stuffInventory += [rand]

                                    saveCharFile(path,a.char)
                                    if await getUserIcon(bot,a.char) in gainMsg:
                                        gainMsg += f", {rand.emoji} {rand.name}"
                                    else:
                                        gainMsg += "\n{0} → {1} {2}".format(await getUserIcon(bot,a.char),rand.emoji,rand.name)

                                elif len(temp) == 0:
                                    gainTabl = [5,35,50,69,11,100,150,666,111,13,1,256,128,64,32]

                                    for comp in a.char.skills+a.char.stuff:                             # Dans toutes les compétences du personnage + ses équipementd
                                        if type(comp) == skill and comp.name == "Truc pas catho":       # Si On sais quoi est équipé
                                            gainTabl = [69]                                             # Tu peux gagner que 69 pièces
                                            break
                                        elif type(comp) == stuff and comp.name == "Tenue Provocante":   # Sinon, si On sait quoi 2 est équipé
                                            gainTabl = [69]                                             # Tu peux gagner que 69 pièces aussi
                                            break

                                    gain = gainTabl[random.randint(0,len(gainTabl)-1)]
                                    logs += " {0} pièces".format(gain)
                                    a.char.currencies += gain
                                    saveCharFile(path,a.char)
                                    if await getUserIcon(bot,a.char) in gainMsg:
                                        gainMsg += f", {gain} <:coins:862425847523704832>"
                                    else:
                                        gainMsg += "\n{0} → {1} <:coins:862425847523704832>".format(await getUserIcon(bot,a.char),gain)

                            elif not(sussesfullRoll) and mainUser.owner == a.char.owner and allOcta and not(winners):
                                if random.randint(0,999) < 334:
                                    aliceStatsDb.updateJetonsCount(mainUser,1)
                                    logs += "\n{0} a obtenu un jeton de roulette".format(mainUser.name)
                                    gainMsg += f", <:jeton:917793426949435402> Jeton de roulette"

                    for ent in tablEntTeam[1]:
                        if type(ent.char) != char:
                            aliceStatsDb.addEnemyStats(enemy=ent.char, tablStats=ent.stats, winner=winners)

                    if len(gainMsg)>1000:
                        gainMsg = gainMsg.replace("<:exp:926106339799887892>","exp")
                    resultEmbed.add_field(name="<:em:866459463568850954>\n__Gains de l'équipe joueur :__",value = gainMsg,inline=False)

                    if listLvlUp != []:
                        temp = ""
                        for a in listLvlUp:
                            temp+=a
                        await ctx.channel.send(embed=discord.Embed(title="__Montée de niveau__",color=light_blue,description="Le{0} personnage{0} suivant{0} {1} monté de niveau !\n".format(["","s"][len(listLvlUp)>1],["a","ont"][len(listLvlUp)>1])+temp))

                if errorNb > 0:
                    resultEmbed.add_field(name="<:empty:866459463568850954>\nDebugg :",value="{0} erreurs de connexions ont survenu durant ce combat",inline=False)

            else:
                logs += mauvaisePerdante
                for team in listImplicadTeams:
                    teamWinDB.changeFighting(team,0)
                logs += "\n"+format_exc()
                date = datetime.now()
                date = date.strftime("%H_%M")
                fich = open("./data/{0}_{1}.txt".format(ctx.author.name,date),"w")
                if not(isLenapy):
                    try:
                        fich.write(logs.replace('\u2192','prohibited'))
                    except:
                        fich.write("Prohibited")
                else:
                    fich.write(logs)
                fich.close()
                opened = open("./data/{0}_{1}.txt".format(ctx.author.name,date),"rb")

                try:
                    msg = await ctx.send("Une erreur est survenue durant le combat",file=discord.File(fp=opened))
                except:
                    msg = await ctx.channel.send("Une erreur est survenue durant le combat",file=discord.File(fp=opened))

                opened.close()
                os.remove("./data/{0}_{1}.txt".format(ctx.author.name,date))
                haveError = True

            if not(haveError):
                if not(auto):
                    await turnMsg.delete()
                    if not(allAuto):
                        await choiceMsg.delete()
                startMsg = globalVar.getRestartMsg()
                if startMsg == 0:
                    await msg.edit(embed = resultEmbed,components=[create_actionrow(create_button(ButtonStyle.grey,"Chargement...",getEmojiObject('<a:loading:862459118912667678>'),"📄",disabled=True))])
                else:
                    await msg.edit(embed = resultEmbed,components=[])
                if not(octogone):
                    for team in listImplicadTeams:
                        teamWinDB.changeFighting(team,0)
            # ------------ Succès -------------- #
            if not(octogone):
                for a in [0,1]:
                    for b in tablEntTeam[a]:
                        if type(b.char) == char and b.char.team == mainUser.team:
                            achivements = achivement.getSuccess(b.char)
                            if not(b.auto): # Ivresse du combat
                                b.char = await achivements.addCount(ctx,b.char,"fight")

                            tablAchivNpcName = ["Alice","Clémence","Akira","Gwendoline","Hélène","Icealia","Shehisa","Powehi","Félicité","Sixtine","Hina","Julie","Krys","Lio","Liu","Liz","Lia","Iliana"]
                            tablAchivNpcCode = ["alice","clemence","akira","gwen","helene","icea","sram","powehi","feli","sixtine","hina","julie","krys","lio","liu","liz","lia","light"]

                            for cmpt in range(len(tablAchivNpcName)):
                                if dictIsPnjVar["{0}".format(tablAchivNpcName[cmpt])]: # Temp or enemy presence sussesss
                                    b.char = await achivements.addCount(ctx,b.char,tablAchivNpcCode[cmpt])

                            if dictIsPnjVar["Iliana"] and (dictIsPnjVar["Luna"] or dictIsPnjVar["Shihu"]):
                                b.char = await achivements.addCount(ctx,b.char,"lightNShadow")
                            if dictIsPnjVar["Luna"] or dictIsPnjVar["Shihu"]:
                                b.char = await achivements.addCount(ctx,b.char,"fullDark")
                            if tablEntTeam[1][0].isNpc("Luna prê."):
                                b.char = await achivements.addCount(ctx,b.char,"luna")
                            if tablEntTeam[1][0].isNpc("Clémence pos."):
                                b.char = await achivements.addCount(ctx,b.char,"clemMem")

                            if b.stats.headnt:
                                b.char = await achivements.addCount(ctx,b.char,"ailill")

                            if b.stats.friendlyfire > 0:
                                b.char = await achivements.addCount(ctx,b.char,"fratere")

                            if auto and int(ctx.author.id) == int(b.char.owner): # Le temps c'est de l'argent
                                b.char = await achivements.addCount(ctx,b.char,"quickFight")

                            # Je ne veux pas d'écolière pour défendre nos terres
                            b.char = await achivements.addCount(ctx,b.char,"school")

                            # Elementaire
                            if b.char.level >= 10:
                                b.char = await achivements.addCount(ctx,b.char,"elemental")

                            if not(winners) and b.healResist >= 80 and b.hp > 0:
                                b.char = await achivements.addCount(ctx,b.char,"dangerous")

                            if not(winners) and b.stats.fullskip:
                                b.char = await achivements.addCount(ctx,b.char,"still")


                            if winners and danger == dangerLevel[0]:
                                b.char = await achivements.addCount(ctx,b.char,"loose")

                            # Dimentio
                            if b.char.level >= 20:
                                b.char = await achivements.addCount(ctx,b.char,"dimentio")

                            # Soigneur de compette
                            b.char = await achivements.addCount(ctx,b.char,"greatHeal",b.stats.heals)

                            # La meilleure défense c'est l'attaque
                            b.char = await achivements.addCount(ctx,b.char,"greatDps",b.stats.damageDeal-b.stats.indirectDamageDeal)

                            # Notre pire ennemi c'est nous même
                            b.char = await achivements.addCount(ctx,b.char,"poison",b.stats.indirectDamageDeal)

                            # Savoir utiliser ses atouts
                            b.char = await achivements.addCount(ctx,b.char,"estialba",int(b.stats.estialba))

                            # Il faut que ça sorte
                            b.char = await achivements.addCount(ctx,b.char,"lesath",int(b.stats.bleeding))

                            if b in dptClass[:3] and b.stats.indirectDamageDeal == b.stats.damageDeal:
                                b.char = await achivements.addCount(ctx,b.char,"dirty")
                            if b == dptClass[0] and b.stats.ennemiKill == 0:
                                b.char = await achivements.addCount(ctx,b.char,"delegation")

                            aliceStatsDb.addStats(b.char,b.stats)

                            saveCharFile(absPath + "/userProfile/"+str(b.char.owner)+".prof",b.char)

            timeout = False
            date, actuTeam, actuEntity, started, prec, logsAff = datetime.now()+horaire,0,0,False,None,False
            date = date.strftime("%H%M")
            fich = open("./data/fightLogs/{0}_{1}.txt".format(ctx.author.name,date),"w")
            if not(isLenapy):
                try:
                    fich.write(logs.replace('\u2192','prohibited'))
                except:
                    fich.write("Prohibited")
            else:
                fich.write(logs)
            fich.close()

            def check(m):
                return m.origin_message.id == msg.id

            logsButton = create_button(ButtonStyle.grey,"Voir les logs","📄","📄")
            startMsg, potgMsg = globalVar.getRestartMsg(),None
            startMsg = startMsg == 0

            if longTurn:
                for team in listImplicadTeams:
                    teamWinDB.changeFighting(team,0)
                logs += "\n"+format_exc()
                date = datetime.now()+horaire
                date = date.strftime("%H%M")
                fich = open("./data/fightLogs/{0}_{1}.txt".format(ctx.author.name,date),"w")
                if not(isLenapy):
                    try:
                        fich.write(logs.replace('\u2192','prohibited'))
                    except:
                        print(format_exc())
                        fich.write("Voir la console")
                else:
                    fich.write(logs)
                fich.close()
                opened = open("./data/fightLogs/{0}_{1}.txt".format(ctx.author.name,date),"rb")
                await asyncio.sleep(1)

                chan = await bot.fetch_channel(808394788126064680)

                desc = ""
                for temp in longTurnNumber:
                    desc += "Tour : {0} - {1} ({2} ms)\n".format(temp["turn"],temp["ent"],temp["duration"])

                await chan.send("Un tour anormalement long a été détecté sur ce combat :",file=discord.File(fp=opened),embed=discord.Embed(title="__Tours mis en causes :__",description=desc))
                opened.close()

            potgIcon = None
            potg = []

            if playOfTheGame[1] != None:
                try:
                    potgIcon = await playOfTheGame[1].getIcon(bot)
                    potg = [create_actionrow(create_button(ButtonStyle.grey,"Action du combat",getEmojiObject(potgIcon),"potg"))]
                except:
                    pass

            while startMsg: # Tableau des statistiques
                options = []
                for team in [0,1]:
                    for num in range(len(endOfFightStats[team])):
                        ent = endOfFightStats[team][num]
                        options.append(create_select_option(ent.name,"{0}:{1}".format(team,num),getEmojiObject(await ent.getIcon(bot)),default=started and team == actuTeam and num == actuEntity))

                select = create_select(options,placeholder="Voir les statistiques d'un combattant")
                await msg.edit(embed = resultEmbed, components=[create_actionrow(select),create_actionrow(logsButton)]+potg)

                try:
                    interact = await wait_for_component(bot,msg,check=check,timeout=60)
                except:
                    toAff = []
                    if logsAff:
                        toAff.append(create_actionrow(logsButton))
                    if potgMsg != None:
                        toAff.append(create_actionrow(create_button(ButtonStyle.URL,"Action du combat",getEmojiObject(playOfTheGame[1].icon),url=potgMsg.jump_url)))

                    await msg.edit(embed = resultEmbed, components=toAff)
                    if prec != None:
                        await prec.delete()
                    return 1

                if interact.component_type == ComponentType.button:
                    if interact.custom_id == "📄":
                        opened = open("./data/fightLogs/{0}_{1}.txt".format(ctx.author.name,date),"rb")
                        logsMsg = await interact.send("`Logs, {0} à {1}:{2}`".format(ctx.author.name,date[0:2],date[-2:]),file=discord.File(fp=opened))
                        if not(isLenapy):
                            print(logs)
                        opened.close()
                        logsButton = create_button(ButtonStyle.URL,"Voir les logs","📄",url=logsMsg.jump_url)
                        logsAff = True
                    else:
                        potgMsg = await interact.send(embed = playOfTheGame[2].set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(potgIcon)["id"])))
                        potg = [create_actionrow(create_button(ButtonStyle.URL,"Action du combat",getEmojiObject(potgIcon),url=potgMsg.jump_url))]
                else:
                    inter = interact.values[0]
                    actuTeam,actuEntity = int(inter[0]),int(inter[-1])
                    actu = endOfFightStats[actuTeam][actuEntity]
                    stats = actu.stats

                    if type(actu.char) == char:
                        userIcon = await getUserIcon(bot,actu.char)
                    else:
                        userIcon = actu.char.icon

                    descri = f"{actu.char.weapon.emoji}"

                    if type(actu.char) in [char,tmpAllie]:
                        descri += f" | {actu.char.stuff[0].emoji} {actu.char.stuff[1].emoji} {actu.char.stuff[2].emoji}"

                    skillTmp = ""
                    for a in actu.char.skills:
                        if type(a) == skill:
                            if skillTmp == "":
                                skillTmp = " |"
                            skillTmp += " {0}".format(a.emoji)

                    descri+=skillTmp
                    statsEm = discord.Embed(title = "__Statistiques de "+ userIcon +" "+actu.char.name+"__",color=actu.char.color,description=descri)

                    precisePurcent,dodgePurcent,critPurcent = "-","-","-"
                    if stats.totalNumberShot > 0:
                        precisePurcent = str(round(stats.shootHited/stats.totalNumberShot*100)) +"%"
                        critPurcent = str(round(stats.crits/stats.totalNumberShot*100)) +"%"
                    if stats.numberAttacked > 0:
                        dodgePurcent = str(round(stats.dodge/stats.numberAttacked*100)) +"%"

                    funnyTempVarName =[[stats.ennemiKill,stats.damageDeal,stats.indirectDamageDeal,stats.underBoost,stats.damageOnShield],[stats.allieResurected,stats.heals,stats.damageBoosted,stats.damageDogded,stats.shieldGived,stats.armoredDamage],[stats.survival,stats.damageRecived,stats.selfBurn,precisePurcent,dodgePurcent,critPurcent]]
                    funnyTempVarNameButTheSecond = [["Ennemis tués :","Dég. infligés :"," - Dont indirects :"," - Dont Boostés :","Dégâts sur armure :"],["Alliés ressucités :","Soins effectués :","Dégâts Boostés :","Dégâts réduits :","Armure fournie :","Dégâts protégés :"],["Tours survécus :","Dégâts reçus :","Dégats sur soi-même :","Taux de précision : ","Taux d'esquive :","Taux de coup critique :"]]
                    sneaker = ["__Stats offensives__","__Stats altruistes__","__Stats personnels__"]
                    for a in [0,1,2]:
                        statMsg = ""
                        for b in range(0,len(funnyTempVarName[a])):
                            temp = "**"
                            if funnyTempVarName[a][b] in [0,"-"]:
                                temp =""
                            statMsg += f"\n{funnyTempVarNameButTheSecond[a][b]} {temp}{str(funnyTempVarName[a][b])}{temp}"
                        statsEm.add_field(name="<:empty:866459463568850954>\n"+sneaker[a],value=statMsg)

                    statsEm.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(await actu.getIcon(bot))["id"]))

                    if prec != None:
                        await prec.edit(embed = statsEm)
                    else:
                        prec = await interact.send(embed = statsEm)
                    started = True
    except:
        if msg == None:
            await ctx.channel.send(embed=discord.Embed(title="__Uncatch error raised__",description=format_exc()),components=[])
        else:
            await msg.edit(embed=discord.Embed(title="__Uncatch error raised__",description=format_exc()),components=[])

        teamWinDB.changeFighting(mainUser.team,0)
