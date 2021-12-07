import discord, random, os, emoji, asyncio,datetime,copy
from discord_slash.context import SlashContext
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from commands_files.sussess_endler import *
from commands_files.alice_stats_endler import *
from traceback import format_exc
from typing import List

teamWinDB = dbHandler("teamVic.db")
AI_DPT,AI_BOOST,AI_SHIELD,AI_AVENTURE,AI_ALTRUISTE,AI_OFFERUDIT,AI_MAGE,AI_ENCHANT = 0,1,2,3,4,5,6,7
moveEmoji = ['⬅️','➡️','⬆️','⬇️']
cancelButton = create_actionrow(create_button(ButtonStyle.grey,"Retour",'◀️',custom_id="return"))

async def fight(bot : discord.Client ,team1 : list, team2 : list ,ctx : SlashContext,guild,auto = True,contexte=[],octogone=False,slash=False):
    """
        Base command for the fights\n
        \n
        Parameters :
        bot : the bot's discord client
        team1 : A list of Char objects
        team2 : A list of Char objects. Unlike team1, can be empty
        ctx : The context of the command, for know where to send the messages
        guild : A server object, for know where to send the level ups messages
        auto : Does the fight is a quick fight or a normal one ? Default ``True``
        contexte : A list of some parameters for the fight. Default ``[]``
            . exemple :
                [TEAM1,<effect>] -> Give to the blue team the <effect> at the start of the fight
        octogone : If at ``False``, enable the loots and exp gains of the fight and lock the Fighting status of the team. Default ``False``
        slash : Does the command is slashed ? Default ``False``
    """

    mainUser = None
    for user in team1:
        if int(user.owner) == int(ctx.author_id):
            mainUser = user

    if mainUser == None:
        raise Exception("Loading error : Main user not found")

    tablIsPnjName = []
    for a in tablAllAllies + tablVarAllies:
        tablIsPnjName.append(a.name)

    temp = []
    for a in tablIsPnjName:
        temp.append((a,False))

    dictIsPnjVar = dict(temp)               # A dict who keep the bool for the presence of a Temp

    aliceMemCastTabl = [False,False]        # Does a team is casting Memento Angel's path 
    alicePing = False                       # Will Alice say it ?
    now = datetime.datetime.now()
    logs,haveError = "[{0}]\n".format(now.strftime("%H:%M:%S, %d/%m/%Y")),False

    print(ctx.author.name + " a lancé un combat")
    cmpt,tablAllCells,tour,danger,dangerThub,tablAliveInvoc,longTurn,longTurnNumber = 0,[],0,100,None,[0,0],False,[]
    dangerLevel = [65,70,75,80,85,90,95,100,110,120,135]

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
            self.on = None

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

            temp = rep[:] 
            for a in effect: # Forbiden effects ?
                if a != None:
                    aeff = findEffect(a)
                    if aeff.reject != None:
                        for b in aeff.reject:
                            for c in temp:
                                for d in c.effect:
                                    if d.effect.id == b or (d.effect.id == a and not(d.effect.stackable)):
                                        if c in rep:
                                            rep.remove(c)

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
                temp = sorted(tabl, key= lambda babie: abs(2-babie.x-portee)+abs(babie.y-summoner.cell.y))
                return temp[0]

            else:
                temp = sorted(tabl, key= lambda babie: abs(3-babie.x+portee)+abs(babie.y-summoner.cell.y))
                return temp[0]

    for a in [0,1,2,3,4,5]:             # Creating the board
        for b in [0,1,2,3,4]:
            tablAllCells += [cell(a,b,cmpt)]
            cmpt += 1

    def findCell(x : int, y : int) -> cell:
        """Return the cell in X:Y, if it exist"""
        cmpt = 0
        while cmpt < 30:
            if tablAllCells[cmpt].x == x and tablAllCells[cmpt].y == y:
                return tablAllCells[cmpt]
            cmpt += 1

    allEffectInFight = []
    addEffect,tablEntTeam = [],[]

    class entity:
        """Base class for the entities"""
        def __init__(self,identifiant : int, perso : Union[char,tmpAllie,octarien], team : int, player=True, auto=True, danger=100,summoner=None):
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
            self.status = STATUS_ALIVE
            if type(perso) != invoc:
                self.icon = perso.icon
            else:
                self.icon = perso.icon[team]
            self.stun = False
            self.summoner = copy.copy(summoner)
            self.raiser = None
            self.specialVars = {"osPro":False,"osPre":False,"osIdo":False,"ohAlt":False,"ohPro":False,"ohIdo":False,"heritEstial":False,"heritLesath":False,"haveTrans":False,"tankTheFloor":False,"clemBloodJauge":None,"clemMemCast":False,"aspiSlot":None,"damageSlot":None}
            
            if type(perso) not in [invoc,octarien]:
                baseHP,HPparLevel = 100,8

            elif type(perso) == invoc:
                baseHP,HPparLevel = 50,5
                perso.level = summoner.char.level
        
            else:
                baseHP,HPparLevel = 90,6.5

            self.effect = []
            self.ownEffect =  []
            self.cell = None

            self.leftTurnAlive = 999
            if type(self.char) == invoc:
                self.leftTurnAlive = 3

            self.strength,self.endurance,self.persoisma,self.agility,self.precision,self.intelligence,self.magie = 0,0,0,0,0,0,0
            self.resistance,self.percing,self.critical = 0,0,0
            self.negativeHeal, self.negativeBoost, self.negativeShield, self.negativeDirect, self.negativeIndirect = 0,0,0,0,0
            self.ressurectable = False
            cooldowns = [0,0,0,0,0]

            for a in [0,1,2,3,4]:
                if type(self.char.skills[a]) == skill:
                    if self.char.skills[a].id == trans.id:
                        if self.char.aspiration in [BERSERK,POIDS_PLUME]:
                            temp = transMelee
                        elif self.char.aspiration in [ENCHANTEUR,MAGE]:
                            temp = transCircle
                        elif self.char.aspiration in [TETE_BRULE,OBSERVATEUR]:
                            temp = transLine
                        elif self.char.aspiration in [ALTRUISTE,IDOLE]:
                            temp = transHeal
                        elif self.char.aspiration == INVOCATEUR:
                            temp = transInvoc
                        elif self.char.aspiration in [PROTECTEUR, PREVOYANT]:
                            temp = transShield

                        self.char.skills[a] = temp
                        self.specialVars["haveTrans"] = True
                    
                    elif self.char.skills[a].id == mageUlt.id:
                        if self.char.element in [ELEMENT_FIRE,ELEMENT_AIR,ELEMENT_SPACE]:
                            temp = mageUltZone
                        elif self.char.element in [ELEMENT_WATER,ELEMENT_EARTH,ELEMENT_TIME]:
                            temp = mageUltMono
                        else:
                            temp = mageUlt

                        self.char.skills[a] = temp

                    cooldowns[a] = int(self.char.skills[a].ultimate)*2+self.char.skills[a].initCooldown

            self.cooldowns = cooldowns
            self.stats = statTabl()
            self.medals = [0,0,0]
            self.healResist = 0
            self.missedLastTurn = False
            self.translucide = False
            self.untargetable = False
            self.invisible = False
            self.name = self.char.name
            self.aspiration = self.char.aspiration

            finded = False
            self.IA = AI_AVENTURE

            if self.char.aspiration in [BERSERK,OBSERVATEUR,POIDS_PLUME,TETE_BRULE]:
                self.IA = AI_DPT

            elif self.char.aspiration in [IDOLE,PROTECTEUR]:
                self.IA = AI_BOOST

            elif self.char.aspiration == ALTRUISTE:
                self.IA = AI_ALTRUISTE

            elif self.char.aspiration == MAGE:
                self.IA = AI_MAGE
            
            elif self.char.aspiration == ENCHANTEUR:
                self.IA = AI_ENCHANT

            elif self.char.aspiration == PREVOYANT:
                self.IA = AI_SHIELD

            elif PREVOYANT == self.char.aspiration:
                offSkill,SuppSkill = 0,0
                for b in [self.char.weapon]+self.char.skills:
                    if type(b) in [weapon,skill]:
                        if b.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]:
                            offSkill += 1
                        else:
                            SuppSkill += 1
                    
                if SuppSkill >= offSkill:
                    self.IA = AI_BOOST
                else:
                    self.IA = AI_OFFERUDIT

            if self.IA == AI_AVENTURE:
                offSkill,SuppSkill,healSkill,armorSkill,invocSkill = 0,0,0,0,0
                for b in [self.char.weapon]+self.char.skills:
                    if type(b) in [weapon,skill]:
                        if b.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]:
                            offSkill += 1
                        elif b.type in [TYPE_BOOST,TYPE_MALUS,TYPE_ARMOR]:
                            SuppSkill += 1
                        elif b.type in [TYPE_HEAL]:
                            healSkill += 1
                        elif b.type in [TYPE_INVOC]:
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
                baseStats = {STRENGTH:self.char.strength,ENDURANCE:self.char.endurance,CHARISMA:self.char.charisma,AGILITY:self.char.agility,PRECISION:self.char.precision,INTELLIGENCE:self.char.intelligence,MAGIE:self.char.magie,RESISTANCE:0,PERCING:0,CRITICAL:0,10:0,11:0,12:0,13:0,14:0}
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
                baseStats = {STRENGTH:0,ENDURANCE:0,CHARISMA:0,AGILITY:0,PRECISION:0,INTELLIGENCE:0,MAGIE:0,RESISTANCE:0,PERCING:0,CRITICAL:0,10:0,11:0,12:0,13:0,14:0}
                temp = self.char.allStats()+[self.char.resistance,self.char.percing,self.char.critical]
                temp2 = self.summoner.allStats()+[self.summoner.resistance,self.summoner.percing,self.summoner.critical]
                adv = 0
                if self.summoner.char.aspiration == INVOCATEUR:
                    adv = summoner.specialVars["aspiSlot"]["mul"]
                    temp2 = summoner.specialVars["aspiSlot"]["baseStats"]
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

            if self.char.element == ELEMENT_FIRE:
                baseStats[7] += 5
            elif self.char.element == ELEMENT_WATER:
                baseStats[PRECISION] += 10
            elif self.char.element == ELEMENT_AIR:
                baseStats[AGILITY] += 10
            elif self.char.element == ELEMENT_EARTH:
                baseStats[6] += 5

            if danger > 100:
                add = int(danger/135 * 20)
                for cmpt in [AGILITY,PRECISION,RESISTANCE]:
                    baseStats[cmpt] += add

            if self.char.aspiration == INVOCATEUR:          # Invoc passif
                statsAtStart = []
                for cmpt, stat in baseStats.items():
                    statsAtStart.append(stat)
                    baseStats[cmpt] = stat*0.8
                
                invocMul = 0.1
                for skil in self.char.skills:
                    if type(skil) == skill and skil.type == TYPE_INVOC:
                        invocMul += 0.06

                self.specialVars["aspiSlot"] = {"baseStats":statsAtStart,"mul":invocMul}

            elif self.char.aspiration == BERSERK:
                val = baseStats[ENDURANCE] * 0.2
                self.specialVars["aspiSlot"] = round(val/2.5,1)
                baseStats[ENDURANCE] -= val
            elif self.char.aspiration == TETE_BRULE:
                for cmpt in (0,2,5,6):
                    baseStats[cmpt] = baseStats[cmpt] * 0.8
                for cmpt in range(10,15):
                    baseStats[cmpt] = baseStats[cmpt] * 1.35

            self.baseStats = baseStats
            self.maxHp = round((baseHP+perso.level*HPparLevel)*((baseStats[ENDURANCE])/120+1))

            if type(self.char) == octarien:
                self.maxHp = round(self.maxHp * danger / 100)
            self.hp = copy.deepcopy(self.maxHp)

        def allStats(self):
            """Return the mains 7 stats"""
            return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

        def move(self,cellToMove=None,x=None,y=None):
            """Move the entity on the given coordonates"""
            if cellToMove == None and x == None and y == None:
                raise Exception("Argument error : No parameters given")
            actCell = self.cell
            if cellToMove == None:
                destination = findCell(x,y)
            else:
                destination = cellToMove
            self.cell = destination
            destination.on = self
            if actCell != None:
                temp.on = None

        def valueBoost(self,target = 0,heal=False):
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
                if not(heal):
                    if target == self:
                        return 0.8
                    else:
                        return 1.2
                else:
                    if target == self:
                        return 1
                    else:
                        return 1.2

            elif self.char.aspiration == IDOLE:             # Idol : The more alive allies they got, the more their buff a heals or powerfull
                alice = 0
                for a in tablEntTeam[self.team]:
                    if a.hp > 0:
                        alice += 1

                if not(heal):
                    return 0.9 + alice*0.05
                else:
                    return 0.8 + alice*0.025

            elif self.char.aspiration in [PREVOYANT,PROTECTEUR]:
                return 1.05
            else:
                return 1

        def effectIcons(self):
            """Return a ``string`` with alls ``fightEffects`` icons, names and values on the entity"""
            temp = ""
            if self.effect != []:
                for a in self.effect:
                    name = a.effect.name
                    if name.endswith("é"):
                        name += self.accord()
                    if a.type == TYPE_ARMOR:
                        temp += f"{a.icon} {name} ({a.value} PV)\n"
                    elif a.effect.turnInit > 0:
                        pluriel = ""
                        if a.turnLeft > 1:
                            pluriel = "s"
                        temp += f"{a.icon} {name} ({a.turnLeft} tour{pluriel})\n"
                    elif a.effect.id == enchant.id:
                        temp += f"{a.icon} {name} ({a.effect.magie})\n"
                    elif a.effect.id == poidPlumeEff.id:
                        temp += f"{a.icon} {name} ({a.value})\n"

                    else:
                        temp += f"{a.icon} {name}\n"
            else:
                temp = "Pas d'effet sur la cible"

            return temp

        def recalculate(self,ignore=None):
            """
                Recalculate the entity stats with all their ``fightEffects``\n
                Parameter :\n
                .ignore : A ``fightEffect`` to ignore. Default ``None``
            """
            baseStats = self.baseStats
            sumStatsBonus = [baseStats[0],baseStats[1],baseStats[2],baseStats[3],baseStats[4],baseStats[5],baseStats[6],baseStats[7],baseStats[8],baseStats[9],baseStats[10],baseStats[11],baseStats[12],baseStats[13],baseStats[14]]
            stuned = False
            self.translucide = False
            self.untargetable = False
            self.invisible = False

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

                if eff.stun == True:
                    stuned = True

                if eff.effect.invisible:
                    self.translucide = True
                    self.untargetable = True
                    self.invisible = True

                elif eff.effect.translucide:
                    self.translucide = True

                elif eff.effect.untargetable:
                    self.untargetable = True

            if type(self.char) != invoc:
                tRes = sumStatsBonus[7]+self.char.resistance
            else:
                tRes = sumStatsBonus[7]

            t1 = max(0,tRes - 100)
            t2 = min(max(0,tRes - 40),60)
            t3 = min(tRes,40)

            sumStatsBonus[7] = int(t3 + t2//3 + t1//5)

            if ignore == None:
                self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie = round(sumStatsBonus[0]),round(sumStatsBonus[1]),round(sumStatsBonus[2]),round(sumStatsBonus[3]),round(sumStatsBonus[4]),round(sumStatsBonus[5]),round(sumStatsBonus[6])
                self.resistance,self.percing,self.critical = sumStatsBonus[7],round(sumStatsBonus[8]),round(sumStatsBonus[9])
                self.negativeHeal, self.negativeBoost, self.negativeShield, self.negativeDirect, self.negativeIndirect = sumStatsBonus[10],sumStatsBonus[11],sumStatsBonus[12],sumStatsBonus[13],sumStatsBonus[14]

                self.stun = stuned
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
                        print("L'effet {0} (caster : {1}) n'a pas pu être retiré de la liste des effets donnés par ce dernier".format(eff.effect.name,eff.caster.char.name))
                    
                    if eff.effect.id in [clemStunEffect.id,aliceStunEffect.id]:
                        self.specialVars["clemBloodJauge"].value = 100

            for a in addEffect[:]:
                self.effect.append(a)
                a.caster.ownEffect.append({self:a.id})
                addEffect.remove(a)
                if type(a) != fightEffect:
                    raise AttributeError("Except fightEffect, but get {0} insted".format(type(a)))
            self.recalculate()

        def indirectAttack(self,target=0,value=0,icon="",ignoreImmunity=False,name='') -> str:
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
            if target.hp > 0:
                for a in target.effect:
                    if a.effect.immunity == True and not(ignoreImmunity):
                        value = 0
                    if a.effect.absolutShield and a.value > 0:
                        dmg = min(value,a.value)
                        popopo += f"{self.icon} {icon} → {a.icon}{a.on.icon} -{dmg} PV\n"
                        popopo += a.decate(value=dmg)
                        self.stats.damageOnShield += dmg
                        if a.value <= 0:
                            reduc = a.on.char.level
                            if a.effect.lightShield:
                                reduc = 0
                            value = max(0,dmg-reduc)
                        else:
                            value = 0

                if target.char.name == "Ailill":
                    for eff in target.effect:
                        if eff.effect.id == "ma" and target.cell.distance(cell=self.cell) > 2:
                            value = int(value*0.25)
                            break

                if value > 0:
                    target.hp -= value
                    if value <= 9000:
                        self.stats.damageDeal += value
                        self.stats.indirectDamageDeal += value
                        target.stats.damageRecived += value
                    addName = ''
                    if name != '':
                        addName = ' ({0})'.format(name)
                    popopo = f"{self.icon} {icon} → {target.icon} -{value} PV{addName}\n"
                    if self.isNpc("Liz"):
                        popopo += add_effect(self,target,charming)
                        target.refreshEffects()
                        

                    if target.hp <= 0:
                        popopo += target.death(killer=self)

            return popopo

        def death(self,killer = 0) -> str:
            """
                The death method, to use when the entity dies.\n
                Parameter :\n
                .killer : The ``entity`` who have kill the entity
            """
            pipistrelle = f"{self.char.name} ({self.icon}) est vaincu{self.accord()} !\n"
            if self.status == STATUS_RESURECTED:
                pipistrelle = f"{self.char.name} ({self.icon}) est vaincu{self.accord()} (pour de bon) !\n"
                self.status=STATUS_TRUE_DEATH

            if killer != self and killer.char.says.onKill != None and random.randint(0,99)<33:
                pipistrelle += "{0} : *\"{1}\"*\n".format(killer.icon,killer.char.says.onKill)

            if self.isNpc("Alice") and random.randint(0,99) < 1:
                pipistrelle += "{0} : *\"{1}\"*\n".format(self.icon,"Tss... J'aurais du tous vous écraser quand je l'aurais pu...")
                alicePing = True

            elif (self.isNpc("Shushi") or self.isNpc("Shihu")) and dictIsPnjVar["Lena"]:
                pipistrelle += "{0} : *\"{1}\"*\n".format('<:lena:909047343876288552>','Shu- Ok là on va sérieusement commencer à se calmer.')
                for ent in tablEntTeam[self.team]:
                    if ent.isNpc("Lena"):
                        mater = classes.effect("Instinct maternelle","ohFuckYou",strength=ent.char.level,turnInit=-1,emoji=uniqueEmoji('<:angry:862321601978040350>'))
                        pipistrelle += add_effect(ent,ent,mater)
                        ent.refreshEffects()

            elif self.isNpc("Alice Exaltée") and killer.isNpc("Clémence pos."):
                pipistrelle += "<a:aliceExalte:914782398451953685> : \"Clé...\"\n<a:clemPos:914709222116175922> : \"... ?\""
                effect = classes.effect("Réveil subconsicent","clemAwakening",magie=-int((killer.baseStats[MAGIE]*0.3)),turnInit=-1,unclearable=True,type=TYPE_MALUS)
                pipistrelle += add_effect(killer,killer,effect)
                killer.char.exp = 35

            elif random.randint(0,99)<33:
                if self.isNpc("Hina") and dictIsPnjVar["Lohica"]:
                    pipistrelle += "{0} : *\"{1}\"*\n".format('<a:lohicaGif:900378281877057658>','Ts. Encore par terre toi ?')
                elif self.isNpc("Clémence") and dictIsPnjVar["John"]:
                    pipistrelle += "{0} : *\"{1}\"*\n".format('<:john:908887592756449311>','Clémence !')
                elif self.isNpc("Félicité") and dictIsPnjVar["Alice"]:
                    pipistrelle += "{0} : *\"{1}\"*\n".format('<:alice:908902054959939664>','Féli ! On se retrouve à la maison !')

                elif self.char.says.onDeath != None:
                    pipistrelle += "{0} : *\"{1}\"*\n".format(self.icon,self.char.says.onDeath)

            for a in self.effect:
                if a.trigger == TRIGGER_DEATH:
                    pipistrelle += a.triggerDeath(killer)
                
                if a.effect.id not in [undying.id]:
                    a.decate(turn=99)

            self.refreshEffects()

            if self.status == STATUS_ALIVE:
                if self.ressurectable:
                    if type(self.char) != octarien or (type(self.char) == octarien and self.char.rez):
                        self.status = STATUS_DEAD
                    else:
                        self.status = STATUS_TRUE_DEATH
                else:
                    self.status = STATUS_TRUE_DEATH
                    
            if type(self.char) != invoc and self.status != STATUS_RESURECTED:
                if self.char.deadIcon == None:
                    self.icon = [None,'<:spIka:866465882540605470>' ,'<:spTako:866465864399323167>','<:spOcta:866465980586786840>'][self.char.species]
                else:
                    self.icon = self.char.deadIcon
            
            elif self.status == STATUS_RESURECTED:
                pipistrelle += add_effect(self,self,onceButNotTwice)
                

            if self.status == STATUS_DEAD:
                effect = copy.deepcopy(lostSoul)
                if self.specialVars["tankTheFloor"]:
                    effect.turnInit += 1
                add_effect(killer,self,effect)
                
                self.refreshEffects()

            killer.stats.ennemiKill += 1
            return pipistrelle

        def attack(self,target=0,value = 0,icon = "",area=AREA_MONO,sussess=None,maxRange=None,use=STRENGTH,onArmor = 1,effectOnHit = None) -> str:
            """
                The method for when a entity attack.\n
                Unlike .indirectAttack(), the targets, damages and triggered effects are all calculated in this method\n
                Parameters :\n
                .target : The ``entity`` targeted by the entity
                .value : The base power of the attack.
                    -> If the value is at ``0``, no ``string`` is return
                .icon : The ``string`` to use as the icon of the attack. Default ``""``
                .area : The area of the attack. See ``constantes``. Default ``AREA_MONO``
                .sussess : The base precision of the attack. If at ``None`` (Default), use the sussess rate of the entity weapon insted
                .maxRange : ``Useless now``
                    -> Used to be needed for the first Observator's passive effect
                .use : The base stat to take for the attack. See ``constantes``
                .onArmor : The multiplier of damage to deal on armors effects. Default ``1``
                .effectOnHit : Does the attack give a `effect` on the targets ? Default ``None``
            """
            if sussess==None: # If no success is gave, use the weapon success rate
                sussess=self.char.weapon.sussess
            if maxRange==None: # If no maxRange is gave, use the weapon max range
                maxRange=self.char.weapon.range

            if value > 0 and self.specialVars["damageSlot"] != None and ((self.specialVars["damageSlot"].effect.id == physicRuneEff.id and use in [STRENGTH,PRECISION,AGILITY]) or (self.specialVars["damageSlot"].effect.id == magicRuneEff.id and use in [MAGIE,CHARISMA,INTELLIGENCE])):
                value = value * (self.specialVars["damageSlot"].effect.power/100+1)

            if self.specialVars["clemMemCast"]:
                isufDPTLol = False
                for eff in self.effect:
                    if eff.effect.id == clemUltShield.id:
                        isufDPTLol = True
                        onArmor = 31000
                        break

            sumDamage = 0
            
            popipo,critMsg = "",""

            if type(target) != int and value > 0: # If the target is valid
                dangerMul = 1
                if danger != None and self.team: # get danger value
                    dangerMul = danger/100

                if target.hp > 0 and value > 0: # If the target is alive
                    popipo,immune,multiplicateur = "",False,1

                    for a in self.effect: # Does the attacker trigger a effect
                        if a.trigger == TRIGGER_DEALS_DAMAGE and value > 0:
                            temp = a.triggerDamage(value = a.effect.power,icon=a.icon,onArmor=onArmor)
                            value = temp[0]
                            popipo += temp[1]

                if self.hp > 0: # Does the attacker still alive ?
                    critRate = round(self.precision/3)+round(self.agility/5)+self.critical
                    for z in target.cell.getEntityOnArea(area=area,team=self.team,wanted=ENNEMIS,directTarget=False): # For eatch ennemis in the area
                        self.stats.totalNumberShot += 1
                        if z.hp > 0: # If the target is alive
                            pp = 0
                            if self.char.aspiration in [POIDS_PLUME,OBSERVATEUR]: # Apply "Poids Plume" critical bonus
                                pp = actTurn.specialVars["aspiSlot"].value

                            # Get the stat used
                            if use == HARMONIE:
                                temp = 0
                                for a in self.allStats():
                                    temp = max(a,temp)
                                used = temp
                            else:
                                used = self.allStats()[use]
                            
                            damage = round(value * (used+100-self.negativeDirect)/100 * (1-(min(95,z.resistance*(1-self.percing/100))/100))*dangerMul*self.getElementalBonus(target=z,area=area,type=TYPE_DAMAGE))
                            
                            # AoE reduction factor
                            if z == target: 
                                multiplicateur = 1
                            else:
                                multiplicateur = 1-(min(0.8,target.cell.distance(z.cell)*0.3))
                            
                            # Dodge / Miss
                            attPre,targetAgi = self.precision,z.agility
                            if attPre < 0:                                              # If the attacker's precision is negative
                                targetAgi += abs(attPre)                                        # Add the negative to the target's agility
                                attPre = 0
                            elif targetAgi < 0:                                         # Same if the target's agility is negative, add it to the attacker's precision
                                attPre += abs(targetAgi)
                                targetAgi = 1

                            if attPre < targetAgi:                                      # If the target's agility is (better ?) than the attacker's precision
                                successRate = 1 - min((targetAgi-attPre)/100,1)*0.5             # The success rate is reduced to 50% of the normal
                            else:
                                successRate = 1 + min((attPre-targetAgi)/100,1)                 # The success rate is increased up to 200% of the normal

                            # It' a hit ?
                            if random.randint(0,99)<successRate*sussess:
                                immune = False
                                for a in z.effect:
                                    if a.effect.immunity:
                                        immune,damage = True,0
                                        break

                                # "dimension déphasée" special damage reduction
                                ailill = 100
                                if not(immune):
                                    for a in z.effect:
                                        if a.trigger == TRIGGER_DAMAGE:
                                            temp = a.triggerDamage(value = damage,declancher=self,icon=icon,onArmor=onArmor)
                                            damage = temp[0]
                                            popipo += temp[1]
                                        if a.effect.id == "ma":
                                            if z.cell.distance(cell=self.cell) > 2:
                                                ailill = 2
                                
                                z.refreshEffects()

                                # Critical
                                critRoll = random.randint(0,99)
                                critMsg = ""
                                if critRoll < critRate and damage > 0:
                                    if self.char.aspiration not in [POIDS_PLUME, OBSERVATEUR]:
                                        critMsg = " (Critique !)"
                                        multiplicateur = multiplicateur * 1.25
                                    else:
                                        critMsg = " (Critique !!)"
                                        multiplicateur = multiplicateur * 1.35
                                    self.stats.crits += 1
                                elif critRoll < critRate + pp and self.char.aspiration in [POIDS_PLUME,OBSERVATEUR] and damage > 0:
                                    multiplicateur = multiplicateur * 1.45
                                    critMsg = " (Critique !!!)"
                                    actTurn.specialVars["aspiSlot"].value = 0
                                    self.stats.crits += 1
                                    break
                                    
                                    pp = 0

                                effectiveDmg = round(damage*multiplicateur*ailill/100)

                                if self.specialVars["clemMemCast"]:
                                    if isufDPTLol:
                                        effectiveDmg = z.hp -1
                                    else:
                                        effectiveDmg = min(effectiveDmg,z.hp-1)

                                self.stats.shootHited += 1
                                self.stats.damageDeal += effectiveDmg
                                z.stats.damageRecived += effectiveDmg
                                sumDamage += effectiveDmg
                                z.stats.numberAttacked += 1
                                z.hp -= effectiveDmg

                                if z.char.element == ELEMENT_SPACE and effectiveDmg > 0:
                                    valueToAdd = int(effectiveDmg * 0.15)

                                    alreadyHaveArmorEff = False
                                    for eff2 in z.effect:
                                        if eff2.effect.id == astralShield.id:
                                            alreadyHaveArmorEff = True
                                            eff2.value += valueToAdd
                                            break

                                    if not(alreadyHaveArmorEff):
                                        effect = copy.deepcopy(astralShield)
                                        effect.overhealth = valueToAdd
                                        add_effect(z,z,effect,ignoreEndurance=True)
                                        
                                        z.refreshEffects()

                                # Damage bosted
                                if use != None:
                                    for statBoost in self.effect:
                                        tstats = statBoost.allStats()
                                        effStat,actTurnStat = -111,0
                                        if use != HARMONIE:
                                            effStat = tstats[use]
                                        elif use == HARMONIE:
                                            for chocobot in tstats:
                                                effStat = max(actTurnStat,chocobot)

                                        if effStat != 0 and statBoost.caster != self: # If the stat was boosted by someone esle
                                            if use == HARMONIE:
                                                temp = 0
                                                for a in self.recalculate(ignore=statBoost):
                                                    temp = max(a,temp)
                                                used = temp
                                            else:
                                                used = self.recalculate(ignore=statBoost)[use]
                                            tempDmg = round(round(value * (used+100)/100 * (1-(min(95,z.resistance*(1-self.percing/100))/100)) * dangerMul)*multiplicateur*ailill/100)
                                            dif = effectiveDmg - tempDmg
                                            if dif > 0:
                                                statBoost.caster.stats.damageBoosted += abs(dif)
                                                self.stats.underBoost += abs(dif)
                                            else:
                                                statBoost.caster.stats.damageDogded += abs(dif)

                                # Damage message
                                if effectiveDmg > 0:
                                    popipo  += f"{self.icon} {icon} → {z.icon} -{effectiveDmg} PV{critMsg}\n"
                                if z.hp <= 0:
                                    popipo += z.death(killer = self)

                                if effectOnHit != None and z == target and z.hp > 0:
                                    effectOnHit = findEffect(effectOnHit)
                                    popipo += add_effect(self,target,effectOnHit)
                                    

                                    z.refreshEffects()

                                # After damage
                                if z.char.aspiration == PROTECTEUR:
                                    popipo += add_effect(z,actTurn,proMalus)
                                elif self.char.aspiration == OBSERVATEUR:
                                    self.specialVars["aspiSlot"].value += 3

                                if z.isNpc("Liu"):
                                    popipo += add_effect(z,actTurn,charming)
                                    
                                    actTurn.refreshEffects()
                                if actTurn.isNpc("Liz"):
                                    popipo += add_effect(actTurn,z,charming)
                                    
                                    actTurn.refreshEffects()

                                for eff in z.effect:
                                    if eff.effect == hourglass1:
                                        eff.value += effectiveDmg
                                    elif eff.effect.id == lightAura2ActiveEff.id:                                 # Aura de lumière 2
                                        for ent in z.cell.getEntityOnArea(area=lightAura2ActiveEff.area,team=z.team,wanted=ALLIES,directTarget=False):
                                            popipo += eff.caster.heal(ent,eff.icon,lightAura2ActiveEff.stat,lightAura2ActiveEff.power,eff.effect.name,danger)
                                        popipo += eff.decate(value=1)
                                        z.refreshEffects()
                                    elif eff.effect.id == flambe.id and use == STRENGTH:                         # Flambage
                                        eff.effect.power += flambe.power
                                    elif eff.effect.id == magAch.id and use == MAGIE:                            # Flambage
                                        eff.effect.power += magAch.power
                                    elif eff.effect.id == rosesEff.id and use == STRENGTH:
                                        popipo += eff.triggerDamage(value = damage,declancher=self,icon=icon,onArmor=onArmor)[1]
                                    elif eff.effect.id == rosesMagicEff.id and use == MAGIE:
                                        popipo += eff.triggerDamage(value = damage,declancher=self,icon=icon,onArmor=onArmor)[1]
                                    elif eff.effect.id == haimaEffect.id:
                                        finded = False
                                        for sndEff in z.effect:
                                            if sndEff.effect.id == haimaShield.id:
                                                finded = True
                                                break

                                        if not(finded):
                                            popipo += add_effect(eff.caster,z,eff.effect.callOnTrigger)
                                            popipo += eff.decate(value = 1)

                            else:
                                popipo += f"{z.char.name} esquive l'attaque\n"
                                z.stats.dodge += 1
                                z.stats.numberAttacked += 1
                                if z.char.aspiration == POIDS_PLUME:
                                    z.specialVars["aspiSlot"].value += 3
                                elif self.char.aspiration == OBSERVATEUR:
                                    self.specialVars["aspiSlot"].value = int(self.specialVars["aspiSlot"].value * 0.7)
                                if z.isNpc("Lia"):
                                    popipo += add_effect(z,actTurn,charming)
                                    popipo += add_effect(z,actTurn,charming)
                                    z.refreshEffects()

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
                                effect = copy.deepcopy(convertArmor)
                                effect.overhealth = valueToAdd
                                popipo += add_effect(eff.caster,self,effect,ignoreEndurance=True)
                                
                                self.refreshEffects()

                        elif eff.effect.id in [vampirismeEff.id,aliceExWeapEff]:
                            healPowa = min(self.maxHp - self.hp, int(sumDamage * (eff.effect.power/100 * (1+(self.allStats()[eff.effect.stat]/100)))))
                            popipo += eff.caster.heal(self,eff.icon,None,healPowa,eff.effect.name)

                if self.char.aspiration == BERSERK:
                    healPowa = min(self.maxHp - self.hp, int(sumDamage * self.specialVars["aspiSlot"]/100))
                    popipo += self.heal(self,aspiEmoji[BERSERK],None,healPowa)

            if self.isNpc("Clémence pos."):
                healPowa = min(self.maxHp - self.hp, int(sumDamage * 0.1))
                popipo += self.heal(self,"",None,healPowa)

                self.specialVars["clemBloodJauge"].value = min(100,self.specialVars["clemBloodJauge"].value+int(sumDamage * 0.02))
                if self.specialVars["clemMemCast"]:
                    self.specialVars["clemMemCast"] = False

            return popipo

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
                            temporaty = eff.decate(value=1)
                            if temporaty != "":
                                nbOfDecate += 1

                    a.effect.power -= primalPower           # Deducing the base power, 'cause we are at [NbEffect]+1 * power
                    toReturn += a.triggerStartOfTurn(danger,decate=False)
                    a.effect.power = primalPower
                    if temporaty != "":
                        nbOfDecate += 1

                    if nbOfDecate > 1:                      # Regrouping all the decate messages as well
                        toReturn += "__{0}__ ne subit plus sous {1} effets de __{2}__\n".format(self.char.name,nbOfDecate,a.effect.name)
                    elif nbOfDecate == 1:
                        toReturn += temporaty

                    allReadySeen.append({a.caster.id:a.effect.id})

            for dictElem in self.ownEffect[:]:
                for on, eff in dictElem.items():
                    for effOn in on.effect:
                        if effOn.id == eff:
                            toReturn += effOn.decate(turn=1)
                            on.refreshEffects()

            for a in range(0,5):
                if self.cooldowns[a] > 0:
                    self.cooldowns[a] -= 1
            
            for a in self.effect:
                if a.effect.id == gwenCoupeEff.id:
                    if random.randint(0,99) < 15:
                        effect = intargetable
                        toReturn += add_effect(self,self,effect)
                        

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

                if a.effect.id == enchant.id:
                    a.effect.magie = 0

            self.refreshEffects()
            if type(self.char) == invoc and self.char.name not in ["Conviction des Ténèbres"] or not(self.char.name.startswith("Patte de The Giant Enemy Spider")):
                self.leftTurnAlive -= 1
                if self.leftTurnAlive <= 0:
                    self.hp = 0
                    temp += "\n{0} est désinvoqué{1}".format(self.char.name,self.accord())
            return temp

        def atRange(self):
            """Renvoie les ennemis à portée de tir"""
            return self.cell.getEntityOnArea(area=self.char.weapon.effectiveRange,team=self.team,wanted=self.char.weapon.target,lineOfSight= True,directTarget=True)

        def quickEffectIcons(self):
            temp = f"{self.icon} {self.char.name} : {self.hp}/{self.maxHp} "
            if self.effect != []:
                temp += "("
                for a in self.effect:
                    temp += a.icon
                temp += ")\n"
            else:
                temp += "\n"

            return temp

        def lightQuickEffectIcons(self):
            temp = f"{self.icon} : "
            stackableAlreaySeen = []
            if self.effect != [] and self.status != STATUS_TRUE_DEATH:
                giveyouup = False
                for eff in self.effect:
                    if eff.effect.id == "giveup":
                        giveyouup = True
                        break

                if self.status == STATUS_DEAD:
                    return f"{self.icon} : <:lostSoul:887853918665707621>\n"

                for a in self.effect:
                    if (a.icon not in ['<:constitution:888746214999339068>','<:lenapy:892372680777539594>','<:tower:905169617163538442>','<:lostSoul:887853918665707621>','<:colegue:895440308257558529>']+aspiEmoji) and not(a.effect.silent and a.effect.replica == None) and a.effect.id not in [lightAura2PassiveEff.id]:
                        if a.effect.stackable and (a.effect.id not in stackableAlreaySeen):
                            number = 0
                            for ent in self.effect:
                                if ent.effect.id == a.effect.id:
                                    number += 1
                            if number > 1:
                                if not(giveyouup):
                                    temp += a.icon+f"({number})"
                                else:
                                    temp += '<a:giveup:902383022354079814>'+f"({number})"
                            elif not(giveyouup):
                                temp += a.icon
                            else:
                                temp += '<a:giveup:902383022354079814>'
                            stackableAlreaySeen.append(a.effect.id)
                        elif not(a.effect.stackable) and not(giveyouup):
                            temp += a.icon
                            if a.effect.id in [flambe.id,magAch.id]:
                                temp += "("+str(a.effect.power//flambe.power)+")"
                        elif not(a.effect.stackable):
                            temp += '<a:giveup:902383022354079814>'
                if temp != f"{self.icon} : ":
                    if self.invisible and "<:invisible:899788326691823656>" not in temp:
                        temp += "<:invisible:899788326691823656>"
                    if self.translucide and "<:translucide:914232635176415283>" not in temp:
                        temp += "<:translucide:914232635176415283>"
                    if self.untargetable and "<:untargetable:899610264998125589>" not in temp:
                        temp += "<:untargetable:899610264998125589>"

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

        def summon(self,summon : invoc ,timeline, cell : cell, tablEntTeam : list,tablAliveInvoc : list, ignoreLimite=False):
            ballerine = ""
            team = self.team
            summon.color = self.char.color
            if tablAliveInvoc[team] < 3 or ignoreLimite:
                sumEnt = entity(self.id,summon,team,False,summoner=self)
                sumEnt.move(cellToMove=cell)
                tablEntTeam[self.team].append(sumEnt)

                if summon.name.startswith("Patte de The Giant Enemy Spider"):
                    add_effect(self,sumEnt,GESredirect)

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
                ballerine = f"{self.char.name} invoque un{accord} {summon.name}"
                tablAliveInvoc[team] += 1
                return {"tablEntTeam":tablEntTeam,"tablAliveInvoc":tablAliveInvoc,"timeline":timeline,"text":ballerine}

        def getElementalBonus(self,target,area : int,type : int):
            """Return the elemental damage bonus"""
            if type not in [TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_ARMOR,TYPE_INDIRECT_DAMAGE]:
                if self.char.element == ELEMENT_FIRE and area != AREA_MONO and self.cell.distance(target.cell) > 2:
                    return 1.1
                elif self.char.element == ELEMENT_WATER and area == AREA_MONO and self.cell.distance(target.cell) > 2:
                    return 1.1
                elif self.char.element == ELEMENT_AIR and area != AREA_MONO and self.cell.distance(target.cell) <= 2:
                    return 1.1
                elif self.char.element == ELEMENT_EARTH and area == AREA_MONO and self.cell.distance(target.cell) <= 2:
                    return 1.1
            elif type in [TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_ARMOR] and self.char.element == ELEMENT_LIGHT:
                return 1.1
            elif type == TYPE_INDIRECT_DAMAGE and self.char.element == ELEMENT_DARKNESS:
                return 1.1

            return 1

        async def resurect(self,target,value : int, icon : str,danger=danger):
            if self.team == 1:
                value = int(value * (danger/100))
            self.stats.allieResurected += 1
            self.stats.heals += value
            target.healResist += int(value/target.maxHp/2*100/2)
            target.hp = value
            target.status = STATUS_RESURECTED
            if type(target.char) != char:
                target.icon = target.char.icon
            else:
                target.icon = await getUserIcon(bot,target.char)

            add_effect(self,target,onceButNotTwice)
            
            for eff in target.effect:
                if eff.id == lostSoul.id:
                    eff.decate(turn=99)
            target.refreshEffects()
            
            rep = f"{target.char.name} est réanimé{target.accord()} !\n{self.icon} {icon} → {target.icon} +{value} PV\n"

            if target.char.says.onResurect != None:
                rep += "{0} : *\"{1}\"*\n".format(target.icon,target.char.says.onResurect)

            target.raiser = self.icon

            # Recent Rez shield
            notDeadYet = classes.effect("Résurection récente","susRez",overhealth=int(target.maxHp*0.2),turnInit=3,absolutShield=True,emoji=sameSpeciesEmoji('<:naB:908490062826725407>','<:naR:908490081545879673>'))
            rep += add_effect(self,target,notDeadYet,ignoreEndurance=True)
            target.refreshEffects()

            return rep

        def getAggroValue(self,target):
            """Return the aggro value agains the target. Made for be use as a key for sort lists"""
            if not(target.untargetable):
                aggro = 20                                          # Base aggro value. Maybe some skills will influe on it later

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

                return int(aggro)
            else:
                return -111

        def heal(self,target, icon : str, statUse : int, power : int, effName = None,danger=danger):
            overheath = 0
            aff = target.hp < target.maxHp
            ballerine = ""
            if power > 0 and self.hp > 0:
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

                    healPowa = round(power * (1+(statUse-self.negativeHeal)/120+(target.endurance/1500))* self.valueBoost(target = target,heal=True)*self.getElementalBonus(target,area = AREA_MONO,type = TYPE_HEAL)*dangerBoost)
                    healPowaInit = copy.deepcopy(healPowa)

                    incurableValue = 0
                    for eff in target.effect:
                        if eff.effect.id == incurable.id:
                            incurableValue = max(incurableValue,eff.effect.power)

                    healPowa = int(healPowa * (100-target.healResist)/100 * (100-incurableValue)/100)
                    overheath = max(0,healPowa - (target.maxHp-target.hp))
                    healPowa = min(target.maxHp-target.hp,healPowa)
                    target.healResist += int(healPowa/target.maxHp/2*100)

                    if self.isNpc("Alice Exaltée"):
                        self.specialVars["clemBloodJauge"].value = min(100,self.specialVars["clemBloodJauge"].value+int(healPowa * 0.02))

                else:
                    healPowa = min(target.maxHp-target.hp,power)
                    healPowaInit = copy.deepcopy(healPowa)

                self.stats.heals += healPowa
                target.hp += healPowa
                add = ""
                if effName != None:
                    add = " ({0})".format(effName)

                lost = ""
                if healPowa < healPowaInit:
                    lost = " `{0}`".format(healPowaInit-healPowa)
                ballerine = f"{self.icon} {icon} → {target.icon} +{healPowa}{lost} PV{add}\n"

                if self.char.element == ELEMENT_TIME and target != self:
                    valueToAdd = int(healPowa * 0.05)

                    alreadyHaveArmorEff = False
                    for eff2 in self.effect:
                        if eff2.effect.id == timeShield.id:
                            alreadyHaveArmorEff = True
                            eff2.value += valueToAdd
                            break

                    if not(alreadyHaveArmorEff):
                        effect = copy.deepcopy(timeShield)
                        effect.overhealth = valueToAdd
                        add_effect(self,self,effect,ignoreEndurance=True)
                        
                        self.refreshEffects()

                if self.char.aspiration in [IDOLE,PROTECTEUR,ALTRUISTE] and overheath > 0:
                    tabli,tabla = [idoOHArmor,proOHArmor,altOHArmor],[self.specialVars["ohIdo"],self.specialVars["ohPro"],self.specialVars["ohAlt"]]
                    for carillon in (0,1,2):
                        if tabla[carillon]:
                            effect = copy.deepcopy(tabli[carillon])
                            effect.overhealth = int(overheath * ([idoOHEff.power,proOHEff.power,altOHEff.power][carillon]/100))
                            ballerine += add_effect(self,target,effect,[idoOHEff.name,proOHEff.name,altOHEff.name][carillon],True)
                            target.refreshEffects()
                            return ballerine

                if self.isNpc("Lio"):
                    ballerine += add_effect(self,target,charming2)
                    target.refreshEffects()

            if aff:
                return ballerine
            else:
                return ""

        def isNpc(self, name : str) -> bool:
            """Return if the entity is a temp's with the name given"""
            return self.char.isNpc(name)

    class fightEffect:
        """Classe plus pousée que Effect pour le combat"""

        def __init__(self,id,effect : classes.effect, caster : entity, on : entity, turnLeft : int, trigger : int, type : int, icon : str, value=1):
            """self.id : int -> Id de l'effet
            self.effect : effect -> L'effet de base
            self.caster : entity -> L'entité qui donne l'effet
            self.on : entity -> L'entité sur laquel se trouve cet effet
            self.turnLeft : int -> Nombre de tour restant à l'effet
            self.trigger : const -> L'événement qui déclanche l'effet
            self.icon : str -> L'id de l'emoji correspondant à l'effet"""
            self.effect = copy.deepcopy(effect)
            self.caster = caster
            self.on = on
            self.turnLeft = turnLeft
            self.trigger = trigger
            self.type = type
            self.value = value
            self.id = id
            self.icon = icon
            self.remove = False
            self.stun = effect.stun
            self.name = effect.name

            tablTemp = [0,0,0,0,0,0,0,0,0]

            if self.effect.stat != None:
                if self.effect.stat is not HARMONIE:
                    temp = self.caster.allStats()[self.effect.stat]
                else:
                    temp = -111
                    for a in self.caster.allStats():
                        temp = max(temp,a)
    
                value = (1 + self.caster.char.level//10/10 - 1 + caster.valueBoost(on)) * (temp+100)/100
            else:
                value = 1

            tablTemp[0] += self.effect.strength * value
            tablTemp[1] += self.effect.endurance * value
            tablTemp[2] += self.effect.charisma * value
            tablTemp[3] += self.effect.agility * value
            tablTemp[4] += self.effect.precision * value
            tablTemp[5] += self.effect.intelligence * value
            tablTemp[6] += self.effect.resistance * value
            tablTemp[7] += self.effect.percing * value
            tablTemp[8] += self.effect.critical * value

            self.tablAllStats = tablTemp

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
                    temp += f"{self.on.char.name} n'est plus sous l'effet __{self.effect.name}__\n"
            return temp

        def triggerDamage(self,value=0,icon="",declancher = 0,onArmor = 1) -> list:
            """Déclanche l'effet"""
            value = round(value)
            temp2 = [value,""]
            if self.type == TYPE_ARMOR and value >0:
                valueT,valueT2 = round(value),round(value)
                if not(self.effect.absolutShield):
                    valueT2 = round(value * onArmor)
                value = round(min(valueT2,self.value))
                temp2 = [0,f"{declancher.icon} {icon} → {self.icon}{self.on.icon} -{value} PV\n"]
                temp2[1] += self.decate(value=value)
                declancher.stats.damageOnShield += value
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
                    ballerine = valueT2 - value - reduc
                    babie = int(ballerine * ratio)
                    temp2[0] = max(0,babie)

            elif self.effect.redirection > 0 and value > 0 and self.caster.hp > 0:
                valueT = value
                redirect = int(valueT * self.effect.redirection/100)
                valueT = valueT - redirect
                temp2 = [valueT,declancher.indirectAttack(target=self.caster,value=redirect,icon=icon,ignoreImmunity=False,name=self.effect.name)]

            elif (self.type == TYPE_INDIRECT_DAMAGE or self.effect.id in [rosesEff.id,rosesMagicEff.id,lightLameEff.id,astralLameEff.id,timeLameEff.id]) and self.value>0:
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
                        reduc = max(0.33,1-target.cell.distance(a.cell)*0.33)

                    if stat != None:
                        damage = damageBase * (1+(stat/100)) *  (1-(min(95,a.resistance*(1-self.caster.percing/100))/100)) * reduc * self.caster.getElementalBonus(a,self.effect.area,TYPE_INDIRECT_DAMAGE)
                    else:
                        damage = damageBase

                    variable += self.caster.indirectAttack(a,value=damage,icon = self.icon,name=self.effect.name)
                temp2[1] = f"{variable}{self.decate(value=1)}"

            elif self.type == TYPE_UNIQUE:
                if self.effect.id == enchant.id :
                    self.effect.magie += 5

            if self.effect.callOnTrigger != None:
                temp2[1] = f"L'effet __{self.effect.name}__ se déclanche :\n"
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
            temp = ""
            if self.type==TYPE_INDIRECT_REZ:
                self.on.status = STATUS_RESURECTED
                self.caster.stats.allieResurected += 1

                if self.effect.stat == None:
                    heal = self.effect.power

                elif self.effect.stat == PURCENTAGE:
                    heal = round(self.on.maxHp * self.effect.power /100)

                self.on.hp = heal
                self.caster.stats.heals += heal
                temp += f"{self.on.char.name} ({self.on.icon}) est réanimé{self.on.accord()} !\n{self.caster.icon} {self.icon}→ {self.on.icon} +{heal} PV\n"
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
                        reduc = max(0.33,1-self.on.cell.distance(a.cell)*0.33)

                    if stat != None:
                        damage = damageBase * (1+(stat/100)) *  (1-(min(95,a.resistance*(1-self.caster.percing/100))/100)) * (reduc) * self.caster.getElementalBonus(a,self.effect.area,TYPE_INDIRECT_DAMAGE)

                    variable += self.caster.indirectAttack(a,value=damage,icon = self.icon)
                temp += f"L'effet __{self.effect.name}__ se déclanche :\n{variable}{self.decate(value=1)}"

            elif self.type == TYPE_UNIQUE:
                if self.effect == hunter:
                    add_effect(self.on,self.on,hunterBuff)
                    self.on.refreshEffects()
                    temp+= self.on.attack(target=killer,value = self.on.char.weapon.power,icon = self.on.char.weapon.emoji,onArmor=self.on.char.weapon.onArmor)

            if self.effect.callOnTrigger != None:
                temp += add_effect(self.on,self.on,findEffect(self.effect.callOnTrigger))
                

            self.decate(value=1)

            return temp

        def triggerStartOfTurn(self,danger,decate=True) -> str:
            """Déclanche l'effet"""
            ballerine=f"L'effet __{self.effect.name}__ se déclanche :\n"
            if self.type == TYPE_INDIRECT_HEAL and self.on.hp > 0:              # Heal Indirect
                for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.caster.team,wanted=ALLIES,directTarget=False):
                    ballerine = self.caster.heal(a,self.icon,self.effect.stat,self.effect.power,self.effect.name,danger)

            elif self.type == TYPE_INDIRECT_DAMAGE and self.value >0 and ((self.effect.area==AREA_MONO and self.on.hp > 0) or self.effect.area != AREA_MONO):            # Damage indirect
                variable,damage = "",0
                if self.effect.stat != None:
                    stat,damageBase = self.caster.allStats()[self.effect.stat]-self.caster.negativeIndirect,self.effect.power
                    whoTarget = ALLIES
                    if self.on.team == self.caster.team and self.on != self.caster:
                        whoTarget = ENNEMIS

                    for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.on.team,wanted=whoTarget,directTarget=False):
                        if a == None:
                            raise Exception("Error while triggering {0} on {1} : The cell say than there is nobody on it ?\nYou should investigate that, Léna".format(self.effect.name,self.on.char.name))
                        selfElem = self.caster.getElementalBonus(a,self.effect.area,TYPE_INDIRECT_DAMAGE)
                        areaMul = 1
                        if a != self.on:
                            areaMul = max(0.2,1-self.on.cell.distance(a.cell)*0.35)
                        damage = damageBase * (1+(stat/100)) *  (1-(min(95,a.resistance*(1-self.caster.percing/100))/100)) * areaMul * selfElem
                        variable += self.caster.indirectAttack(a,value=damage,icon = self.icon,name=self.effect.name)

                        if self.effect.id == estal.id and damage != 0:
                            self.caster.stats.estialba += damage
                        elif self.effect.id == hemoragie.id and damage != 0:
                            self.caster.stats.bleeding += damage

                    ballerine = variable

                    if decate:
                        ballerine += self.decate(value=1)
                else:
                    for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.caster.team,wanted=ENNEMIS,directTarget=False):
                        damage = self.effect.power
                        variable += self.caster.indirectAttack(a,value=damage,icon = self.icon,name=self.effect.name)
                    
                    ballerine = variable
                    if decate:
                        ballerine += self.decate(value=1)

                if self.effect.id == lieSkillEff.id and self.value > 0:
                    effTemp = copy.deepcopy(lieSkillEff)
                    effTemp.turnInit,effTemp.lvl = self.turnLeft, self.value

                    ballerine += add_effect(self.caster,self.on,effTemp)
                    self.on.refreshEffects()

                if self.effect.id == infection.id:                              # If it's the infection poisonnus effect
                    tempTabl = self.on.cell.getEntityOnArea(area=AREA_DONUT_1,team=self.on.team,wanted=ALLIES,effect=[infection],directTarget=False)
                    if len(tempTabl) > 0:
                        ballerine += "L'infection se propage...\n"
                        for ent in tempTabl:
                            ballerine += add_effect(self.caster,ent,infection)
                            add_effect(self.caster,ent,infectRej)
                            ent.refreshEffects()

            elif self.type == TYPE_BOOST and self.on.hp > 0:                    # Indirect Armor
                ballerine += add_effect(self.caster,self.on,findEffect(self.effect.callOnTrigger))
                self.on.refreshEffects()
            return ballerine

        def triggerEndOfTurn(self,danger) -> str:
            """Trigger the effect"""
            temp = ""
            if self.type == TYPE_INDIRECT_DAMAGE:                               # The only indirect damage effect for now is a insta death
                temp += self.caster.indirectAttack(target=self.on,ignoreImmunity=self.effect.ignoreImmunity ,value=self.effect.power)
                self.decate(value=1)
            elif self.type == TYPE_UNIQUE:                                      # Poids Plume effect bonus reduce
                if self.effect == poidPlumeEff:
                    self.value = self.value//2

            elif self.type == TYPE_INDIRECT_HEAL and self.on.hp > 0:            # End of turn healing (aka Light Aura 1)
                for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.caster.team,wanted=ALLIES,directTarget=False):
                    temp += self.caster.heal(a,self.icon,self.effect.stat,self.effect.power,self.effect.name,danger)

            return temp

        def triggerRemove(self) -> str:
            """Trigger the effect when it's removed\n
            For now, only unique effect activly use it, but some boost effect use it to"""

            if not(self.effect.silent):
                message = f'L\'effet __{self.effect.name}__ se déclanche :\n'
            else:
                message = ""
            if self.type == TYPE_UNIQUE:
                if self.effect == hourglass1 and self.on.hp > 0:                # Sablier Imtempo 1 effect
                    heal = min(self.on.maxHp - self.on.hp, round(self.value * 0.50))
                    message = self.caster.heal(self.on,self.icon,None,heal,self.effect.name)

                elif self.effect.id == lostSoul.id:                                   # Remove the body effect
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

    def add_effect(caster: entity,target: entity,effect: classes.effect,start="",ignoreEndurance=False,turn=tour,danger=danger):
        """Méthode qui rajoute l'effet Effet à l'entity Target lancé par Caster dans la liste d'attente des effets"""
        valid,id,popipo = False,0,""
        valid = True
        turn = caster.stats.survival

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
                    else:                                                           # A less powerful Healn't
                        popipo = f"{caster.icon} {effect.emoji[caster.char.species-1][caster.team]} → 🚫{a.effect.emoji[caster.char.species-1][caster.team]} {target.icon}\n"
                    valid = False

                elif a.effect.id in [idoOHArmor.id,proOHArmor.id,altOHArmor.id]:  # Overhealth Shield
                    if a.value < effect.overhealth:                               # A better Overhealth shield
                        diff = effect.overhealth - a.value
                        a.value = effect.overhealth
                        a.caster = caster
                        a.leftTurn = effect.turnInit
                        popipo = f"{caster.icon} {effect.emoji[caster.char.species-1][caster.team]} → {a.effect.emoji[caster.char.species-1][caster.team]}+{diff} {target.icon}\n"
                    else:                                                           # A less powerful shield
                        popipo = f"{caster.icon} {effect.emoji[caster.char.species-1][caster.team]} → 🚫{a.effect.emoji[caster.char.species-1][caster.team]} {target.icon}\n"
                    valid = False
                elif not(effect.silent):                                        # It's not Healn't
                    popipo = f"{caster.icon} {effect.emoji[caster.char.species-1][caster.team]} → 🚫{a.effect.emoji[caster.char.species-1][caster.team]} {target.icon}\n"
                    valid = False
                break

        if valid:
            valid = False
            while not(valid):                                               # Why Lena. Why ?
                id,trouv = random.randint(1000,9999),False                  # Ok, I use them now
                for a in allEffectInFight:
                    if a == id:
                        trouv = True
                        break
                
                if not(trouv):
                    valid = True

            icon = effect.emoji[caster.char.species-1][caster.team]
            if effect.id == darkFlumPoi.id:
                effect = copy.deepcopy(darkFlumPoi)
                effect.power = int(caster.char.level * 0.2)

            if effect.overhealth > 0:                                       # Armor Effect
                temp = caster.allStats()

                value = effect.overhealth
                friablility = max(1-(max(0,turn-5) / 20),0.1)                   # Reduct over time

                dangerBoost = 1
                if caster.team == 1:
                    dangerBoost = danger/100
                if effect.stat != None:                                         # Classical armor effect
                    if effect.stat == HARMONIE:
                        maxi = 0
                        for randomVar in temp:
                            maxi = max(maxi,randomVar)
                        value = round(effect.overhealth * caster.valueBoost(target=target) * (maxi-caster.negativeShield+100)*((target.endurance+1000)/1000)/100 * friablility * dangerBoost)
                    else:
                        value = round(effect.overhealth * caster.valueBoost(target=target) * (temp[effect.stat]-caster.negativeShield+100)*((target.endurance+1000)/1000)/100 * friablility * dangerBoost)
                elif not(ignoreEndurance):                                      # Semi-fixe armor effect
                    value = round(effect.overhealth * caster.valueBoost(target=target) * ((target.endurance+1000)/1000) * friablility)
                else:                                                           # Fixe armor effect
                    value = round(effect.overhealth)

                if caster.char.aspiration == PREVOYANT:
                    value = int(value*1.2)                      # Shield +20%
                if caster.char.element == ELEMENT_TIME:
                    value = int(value*1.05)                      # Shield +5%

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
                addEffect.append(fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,TYPE_ARMOR,icon,value))
                
                if not(effect.silent):
                    pluriel = ""
                    name = effect.name
                    if start != "":
                        if start.startswith('('):
                            start = start[1:]
                        if start.endswith(')'):
                            start = start[:-1]
                        start = ' ({0})'.format(start)
                    if name.endswith("é"):
                        name += target.accord()
                    if value > 1:
                        pluriel = "s"
                    if effect.turnInit > 0:
                        popipo = f"{target.char.name} ({target.icon}) est protégé par __{name}__ ({icon} {value}) pendant {effect.turnInit} tour{pluriel}{start}\n"
                    else:
                        popipo = f"{target.char.name} ({target.icon}) est protégé par __{name}__ ({icon} {value}){start}\n"

            else:                                                           # Any other effect
                toAppend = fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,effect.type,icon,effect.lvl)
                addEffect.append(toAppend)

                if effect.id == "clemBloodJauge":
                    caster.specialVars["clemBloodJauge"] = toAppend

                name = effect.name
                if name.endswith("é"):                                      # Add a "e" if the caracter is a girl
                    name += target.accord()
                if not(effect.silent):
                    if caster.team == target.team :
                        under = "bénificie de"
                    else:
                        under = "subis"
                    if effect.turnInit > 0:
                        conjug = ""
                        if effect.turnInit > 1:
                            conjug ="s"
                        popipo = f"{target.char.name} ({target.icon}) {under} l'effet de __{name}__ ({icon}) pendant {effect.turnInit} tour{conjug}{start}\n"
                    else:
                        popipo = f"{target.char.name} ({target.icon}) {under} l'effet de __{name}__ ({icon}){start}\n"
                target.refreshEffects()

                tablTemp = [altOHEff.id,proOHEff.id,idoOHEff.id,idoOSEff.id,proOSEff.id,preOSEff.id,heriteEstialbaEff.id,heriteLesathEff.id,floorTanking.id]
                nameTemp = ["ohAlt","ohPro","ohIdo","osIdo","osPro","osPre","heritEstial","heritLesath","tankTheFloor"]
                tablTempEff = [physicRuneEff.id,magicRuneEff.id]
                nameTempEff = ["damageSlot","damageSlot"]

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
                    addEffect.append(fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,effect.type,icon,effect.lvl))
                    name = effect.name
                    if name.endswith("é"):
                        name += target.accord()

                    popipo += f"__{target.char.name}__ ({target.icon}) subis l'effet de __{name}__ ({icon}) pendant {effect.turnInit} tour ({heriteEstialbaEff.name})\n"
                    target.refreshEffects()

                elif effect.id == hemoragie.id and caster.specialVars["heritLesath"] :                         # If is the hemorragic effect
                    effect=hemoragie2
                    icon = effect.emoji[caster.char.species-1][caster.team]
                    addEffect.append(fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,effect.type,icon,effect.lvl))
                    name = effect.name
                    if name.endswith("é"):
                        name += target.accord()

                    popipo += f"__{target.char.name}__ ({target.icon}) subis l'effet de __{name}__ ({icon}) pendant {effect.turnInit} tour ({heriteLesathEff.name})\n"
                    target.refreshEffects()

                if effect.id in [poidPlumeEff.id,obsEff.id,enchant.id]:
                    caster.specialVars["aspiSlot"] = toAppend

        return popipo

    def map():
        """Renvoie un str contenant la carte du combat"""
        line1,line2,line3,line4,line5 = [None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None]
        lines = [line1,line2,line3,line4,line5]

        for a in tablAllCells:
            temp = '<:empty:866459463568850954>'
            #temp = f'{str(a.x)}-{str(a.y)}'                        Show cells ID
            if a.on != None:
                if a.on.status == STATUS_DEAD:
                    temp = ['<:ls1:868838101752098837>','<:ls2:868838465180151838>'][a.on.team]
                elif a.on.status != STATUS_TRUE_DEATH:
                    if a.on.invisible:                              # If the entity is invisible, don't show it. Logic
                        temp = '<:empty:866459463568850954>'
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
        temp.sort(key=lambda ballerine:getHealAggro(ballerine,skillToUse),reverse=True)
        return temp[0]

    # Début du combat ------------------------------------------------------
    logs += "Fight triggered by {0}\n".format(ctx.author.name)
    logs += "\n=========\nTeams filling phase\n=========\n\n"
    leni = len(team1)

    # Teams generations ------------------------
    if len(team1) < 4 and not(octogone): # Remplisage de la team1
        aleaMax = len(tablAllAllies)-1
        alreadyFall = []
        lvlMax = 0

        for a in team1:
            lvlMax = max(lvlMax,a.level)

        copyTablTemp = copy.deepcopy(tablAllAllies)
        while len(team1) < 4:
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
            
            if alea.isNpc("Lena") and random.randint(0,99) < 10:
                alea = copy.deepcopy(findAllie("Luna"))
            elif alea.isNpc("Gwendoline"):
                bidule = random.randint(0,99)
                if bidule < 50:
                    alea = copy.deepcopy(findAllie("Klironovia"))
                elif bidule < 60:
                    alea = copy.deepcopy(findAllie("Altikia"))
            elif alea.isNpc("Shushi") and random.randint(0,99) < 10:
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
        for a in team1:
            lvlMax = max(lvlMax,a.level)

        altDanger = [60,60,60,60,70,70,80,80,90,90,100,100]
        dangerThugLevel = ['https://media.discordapp.net/attachments/810212020049543221/882219019644575796/danger65.png','https://cdn.discordapp.com/attachments/810212020049543221/882218077419339776/danger70.png','https://cdn.discordapp.com/attachments/810212020049543221/882218077650030632/danger75.png','https://cdn.discordapp.com/attachments/810212020049543221/882218077859762177/danger80.png','https://cdn.discordapp.com/attachments/810212020049543221/882218078119796776/danger85.png','https://cdn.discordapp.com/attachments/810212020049543221/882218078346297384/danger90.png','https://cdn.discordapp.com/attachments/810212020049543221/882218078606340136/danger95.png','https://cdn.discordapp.com/attachments/810212020049543221/882218078870593536/danger100.png','https://cdn.discordapp.com/attachments/810212020049543221/882218079407443998/danger110.png','https://cdn.discordapp.com/attachments/867393297520263208/884453208477532210/effect_20210902093005.png','https://media.discordapp.net/attachments/810212020049543221/882218079625568316/danger120.png']
        altDangerThug = ['https://media.discordapp.net/attachments/810212020049543221/882219019644575796/danger65.png','https://media.discordapp.net/attachments/810212020049543221/882219019644575796/danger65.png','https://cdn.discordapp.com/attachments/810212020049543221/882218077419339776/danger70.png','https://cdn.discordapp.com/attachments/810212020049543221/882218077419339776/danger70.png','https://cdn.discordapp.com/attachments/810212020049543221/882218077650030632/danger75.png','https://cdn.discordapp.com/attachments/810212020049543221/882218077650030632/danger75.png','https://cdn.discordapp.com/attachments/810212020049543221/882218077859762177/danger80.png','https://cdn.discordapp.com/attachments/810212020049543221/882218077859762177/danger80.png','https://cdn.discordapp.com/attachments/810212020049543221/882218078119796776/danger85.png','https://cdn.discordapp.com/attachments/810212020049543221/882218078346297384/danger90.png','https://cdn.discordapp.com/attachments/810212020049543221/882218078606340136/danger95.png','https://cdn.discordapp.com/attachments/810212020049543221/882218078870593536/danger100.png']

        if random.randint(0,99) < 80 or leni < 4: # Vs normal team
            winStreak = teamWinDB.getVictoryStreak(team1[0])
        
            danger = dangerLevel[winStreak]
            dangerThub = dangerThugLevel[winStreak]

            aleaMax = len(tablAllOcta)-1
            alreadyFall = []

            tablOctaTemp = copy.deepcopy(tablAllOcta)
            oneVAll = False
            if len(team2) < len(team1) and lvlMax >= 15:
                if random.randint(0,99) < 25:               # Boss ?
                    temp = random.randint(0,len(tablBoss)-1)
                    alea = copy.deepcopy(tablBoss[temp])
                    #alea = copy.deepcopy(findEnnemi("The Giant Enemy Spider"))

                    if alea.oneVAll:
                        oneVAll = True
                        littleTeam = len(team1)/8
                        alea.strenght = int(alea.strength * littleTeam)
                        alea.endurance = int(alea.endurance * littleTeam)
                        alea.charisma = int(alea.charisma * littleTeam)
                        alea.agility = int(alea.agility * littleTeam)
                        alea.precision = int(alea.precision * littleTeam)
                        alea.intelligence = int(alea.intelligence * littleTeam)
                        alea.magie = int(alea.magie * littleTeam)

                    alea.changeLevel(lvlMax)
                    team2.append(alea)
                    logs += "{0} have been added into team2\n".format(alea.name)

                    if alea.isNpc("Luna"):
                        alea = copy.deepcopy(findAllie("Shushi Cohabitée"))
                        alea.changeLevel(lvlMax)

                        for play in team1:
                            shushiCount = 0
                            for skil in play.skills:
                                if type(skil) == skill and (skil.type in [TYPE_ARMOR] or skil.id in [idoOSEff.id,proOSEff.id,preOSEff.id,invocSeraf.id]):
                                    shushiCount += 1
                            if shushiCount > 2:
                                for cmpt in range(len(alea.skills)):
                                    if type(alea.skills[cmpt]) == skill and alea.skills[cmpt].type == TYPE_ARMOR:
                                        alea.skills[cmpt].effect[0].overhealth = int(alea.skills[cmpt].effect[0].overhealth * 0.6)
                                        logs += "La puissance de l'effet {0} de la compétence {1} de {2} a été diminuée\n".format(alea.skills[cmpt].effect[0].name,alea.skills[cmpt].name,alea.name)
                                break

                        team1.append(alea)
                        logs += "{0} have been added into team1\n".format(alea.name)

                    if alea.isNpc("Clémence pos."):
                        alea = copy.deepcopy(findAllie("Alice Exaltée"))
                        alea.changeLevel(lvlMax)

                        for play in team1:
                            aliceCount = 0
                            for skil in play.skills:
                                if type(skil) == skill and (skil.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_RESURECTION] or skil.id in [idoOHEff.id,proOHEff.id,altOHEff.id,lightAura.id,lightAura2.id,invocFee.id,lapSkill.id]):
                                    aliceCount += 1
                            if aliceCount > 2:
                                for cmpt in range(len(alea.skills)):
                                    if type(alea.skills[cmpt]) == skill:
                                        if alea.skills[cmpt].type == TYPE_HEAL:
                                            alea.skills[cmpt].power = int(alea.skills[cmpt].power * 0.7)
                                            logs += "La puissance de la compétence {0} de {1} a été diminuée\n".format(alea.skills[cmpt].name,alea.name)
                                        elif alea.skills[cmpt].type == TYPE_INDIRECT_HEAL:
                                            alea.skills[cmpt].effect[0].power = int(alea.skills[cmpt].effect[0].power * 0.6)
                                            logs += "La puissance de l'effet {0} de la compétence {1} de {2} a été diminuée\n".format(alea.skills[cmpt].effect[0].name,alea.skills[cmpt].name,alea.name)
                                break

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

            while len(team2) < len(team1) and not(oneVAll):
                aleaMax = len(tablOctaTemp)-1
                temp = random.randint(0,aleaMax)

                alea = tablOctaTemp[temp]
                tablOctaTemp.remove(alea)
                alea.changeLevel(lvlMax)
                
                team2.append(alea)
                logs += "{0} have been added into team2\n".format(alea.name)

        else: # Vs temp ally team
            winStreak = teamWinDB.getVictoryStreak(team1[0])

            lvlMax = 0
            temp = copy.deepcopy(team1)
            temp.sort(key=lambda ballerine: ballerine.level)
            lvlMax = temp[0].level

            danger = altDanger[winStreak]
            dangerThub = altDangerThug[winStreak]

            tabl = copy.deepcopy(tablAllAllies)
            tablTank = []
            tablMid = []
            tablBack = []

            for allie in tabl:
                [tablTank,tablMid,tablBack][allie.weapon.range].append(allie)
            
            lenTeam1 = len(team1)
            if lenTeam1 == 5:
                placeTabl = ["Tank","Tank","Midle","Midle","Back"]+[["Tank","Midle","Back"][random.randint(0,2)]]+[None]
            elif lenTeam1 == 6:
                placeTabl = ["Tank","Tank","Midle","Midle","Back"]+[["Midle","Back"][random.randint(0,1)]]+[["Tank","Back"][random.randint(0,1)]]+[None]
            elif lenTeam1 == 7:
                placeTabl = ["Tank","Tank","Midle","Midle","Back","Back"]+[["Tank","Midle","Back"][random.randint(0,2)]]+[None]
            elif lenTeam1 == 8:
                placeTabl = ["Tank","Tank","Tank","Midle","Midle","Back","Back"]+[["Midle","Back"][random.randint(0,1)]]+[None]

            while len(team2) < len(team1):
                if placeTabl[0] == "Tank":
                    rand = random.randint(0,len(tablTank)-1)
                    alea = tablTank[rand]
                    tablTank.remove(alea)
                    placeTabl = placeTabl[1:]
                elif placeTabl[0] == "Midle":
                    rand = random.randint(0,len(tablMid)-1)
                    alea = tablMid[rand]
                    tablMid.remove(alea)
                    placeTabl = placeTabl[1:]
                elif placeTabl[0] == "Back":
                    rand = random.randint(0,len(tablBack)-1)
                    alea = tablBack[rand]
                    tablBack.remove(alea)
                    placeTabl = placeTabl[1:]

                if alea.name == "Lena" and random.randint(0,99) < 10:
                    alea = tablVarAllies[0]
                elif alea.name == "Gwendoline":
                    bidule = random.randint(0,99)
                    if bidule > 66:
                        alea = tablVarAllies[1]
                    elif bidule > 33:
                        alea = tablVarAllies[2]
                elif alea.name == "Shushi" and random.randint(0,99) < 10:
                    alea = tablVarAllies[3]

                alea.changeLevel(lvlMax)
                alea.stuff = [getAutoStuff(alea.stuff[0],alea),getAutoStuff(alea.stuff[1],alea),getAutoStuff(alea.stuff[2],alea)]

                for cmpt in tablIsPnjName:
                    if alea.isNpc(cmpt):
                        dictIsPnjVar[f"{cmpt}"] = True
                        break

                team2 += [alea]
                logs += "{0} have been added into team1 ({1}, {2}, {3})\n".format(alea.name,alea.stuff[0].name,alea.stuff[1].name,alea.stuff[2].name)
    elif octogone:
        danger=100
    else:
        winStreak = teamWinDB.getVictoryStreak(team1[0])
        danger = dangerLevel[winStreak]

    tablTeam,tablEntTeam,cmpt = [team1,team2],[[],[]],0
    readyMsg,msg,cmpt = None,None,0

    for a in [0,1]:                 # Entities generations and stats calculations
        for b in tablTeam[a]:
            if auto == False and b.species != 3:
                try:
                    await bot.fetch_user(b.owner)
                    ent = entity(cmpt,b,a,auto=False)
                except:
                    ent = entity(cmpt,b,a,danger=danger)
            else:  
                ent = entity(cmpt,b,a,danger=danger)

            tablEntTeam[a].append(ent)
            ent.recalculate()
            await ent.getIcon(bot=bot)
            cmpt+=1

    try:
        msg = await ctx.send(embed = await getRandomStatsEmbed(bot,team1,text=["Chargement...","Combat rapide en cours de génération..."][int(auto)]))
    except:
        msg = await ctx.channel.send(embed = await getRandomStatsEmbed(bot,team1))

    if not(auto):                   # Send the first embed for the inital "Vs" message and start generating the message
        if not(octogone):
            team = team1[0].team
            teamWinDB.changeFighting(team,True)

        repEmb = discord.Embed(tilte = "Combat <:turf:810513139740573696>",color = light_blue)
        
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
    temp3 = [[0,1,2],[3,4,5]]
    placementlines=[[[],[],[]],[[],[],[]]]
    allAuto = True
    for a in [0,1]:                     # Sort the entities and place them
        melee, dist, snipe, lenMel, lenDist, lenSnip = [],[],[],0,0,0

        for b in tablEntTeam[a]:
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

        if a == 1:
            temp1,temp2 = [melee,dist,snipe],[lenMel,lenDist,lenSnip]
        else:
            temp1,temp2 = [snipe,dist,melee],[lenMel,lenDist,lenSnip]

        for b in [0,1]:
            if temp2[b] > 5:
                temp1[b+1] += temp1[b][5:]
                temp1[b] = temp1[b][0:5]

        if temp2[2] > 5:
            temp1[1] += temp1[2][5:]
            temp1[2] = temp1[2][0:5]

            if len(temp[1]) > 5:
                random.shuffle(temp[1])
                temp1[0] += temp1[1][5:]
                temp1[1] = temp1[1][0:5]
        
        if a == 0:
            placementlines[a]=[snipe,dist,melee]
        else:
            placementlines[a]=[melee,dist,snipe]
    
        temp2[0],temp2[1],temp2[2],cmpt = len(temp1[0]),len(temp1[1]),len(temp1[2]),0

        for b in temp3[a]:
            random.shuffle(temp1[cmpt])


            if (a == 1 and b % 3 == 0) or (a == 0 and b % 3 == 2):
                if temp2[cmpt] == 1:
                    temp1[cmpt][0].move(y=2,x=b)
                    logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(temp1[cmpt][0].char.name,0,0,b,2)

                elif temp2[cmpt] == 2:
                    temp1[cmpt][0].move(y=1,x=b)
                    logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(temp1[cmpt][0].char.name,0,0,b,1)
                    temp1[cmpt][1].move(y=3,x=b)
                    logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(temp1[cmpt][1].char.name,0,0,b,3)

                elif temp2[cmpt] == 3:
                    temp1[cmpt][0].move(y=1,x=b)
                    logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(temp1[cmpt][0].char.name,0,0,b,1)
                    temp1[cmpt][1].move(y=2,x=b)
                    logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(temp1[cmpt][1].char.name,0,0,b,2)
                    temp1[cmpt][2].move(y=3,x=b)
                    logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(temp1[cmpt][2].char.name,0,0,b,3)

                elif temp2[cmpt] == 4:
                    temp1[cmpt][0].move(y=0,x=b)
                    logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(temp1[cmpt][0].char.name,0,0,b,0)
                    temp1[cmpt][1].move(y=1,x=b)
                    logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(temp1[cmpt][1].char.name,0,0,b,1)
                    temp1[cmpt][2].move(y=3,x=b)
                    logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(temp1[cmpt][2].char.name,0,0,b,3)
                    temp1[cmpt][3].move(y=4,x=b) 
                    logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(temp1[cmpt][3].char.name,0,0,b,4)
                
                elif temp2[cmpt] == 5:
                    temp1[cmpt][0].move(y=0,x=b)
                    logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(temp1[cmpt][0].char.name,0,0,b,0)
                    temp1[cmpt][1].move(y=1,x=b)
                    logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(temp1[cmpt][1].char.name,0,0,b,1)
                    temp1[cmpt][2].move(y=2,x=b)
                    logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(temp1[cmpt][2].char.name,0,0,b,2)
                    temp1[cmpt][3].move(y=3,x=b)
                    logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(temp1[cmpt][3].char.name,0,0,b,3)
                    temp1[cmpt][4].move(y=4,x=b)
                    logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(temp1[cmpt][4].char.name,0,0,b,4)
            else:
                if temp2[cmpt] == 1:
                    temp1[cmpt][0].move(y=random.randint(1,3),x=b)
                    logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(temp1[cmpt][0].char.name,0,0,b,2)

                else:
                    tabl = [0,1,2,3,4]
                    cmpt2 = 0

                    for useless in range(temp2[cmpt]):
                        rand = random.randint(0,len(tabl)-1)
                        ruby = tabl[rand]
                        tabl.remove(ruby)
                        temp1[cmpt][cmpt2].move(y=ruby,x=b)
                        logs += "{0} has been place at {1}:{2}\n".format(temp1[cmpt][0].char.name,b,ruby)
                        cmpt2 += 1
            cmpt += 1

    if not(auto):                       # Edit the Vs embed for his message
        if dangerThub != None:
            repEmb.set_thumbnail(url=dangerThub)
        repEmb.add_field(name = "Ce combat oppose :",value = versus)
        repEmb.add_field(name = "__Carte__",value= map(),inline = False)
        await msg.edit(embed = repEmb)

    choiceMsg = 0
    if not(auto):                       # Utilisateurs présent ?
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

        dateLimite = datetime.datetime.now() + datetime.timedelta(seconds=15)
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
                timeLimite = (dateLimite - datetime.datetime.now()).total_seconds()
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
    tempTurnMsg = "__Début du combat :__\n"
    if not(auto):
        turnMsg = readyMsg
        await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = light_blue))
        await turnMsg.clear_reactions()
    time = timeline()
    time, tablEntTeam = time.init(tablEntTeam)

    logs += "\n=========\nStuffs passives effects phase\n=========\n\n"
    for team in [0,1]:                                  # Says Start
        for ent in tablEntTeam[team]:
            if (ent.isNpc("Alice") or ent.isNpc("Félicité") or ent.isNpc("Lohica")) and tablEntTeam[1][0].isNpc("The Giant Enemy Spider"):
                tempTurnMsg += "{0} : *\"{1}\"*\n".format(ent.icon,"!?")
                arch = classes.effect("Arachnophobie","archacnophobia",type=TYPE_MALUS,strength=-int(ent.baseStats[STRENGTH]*0.2),charisma=-int(ent.baseStats[CHARISMA]*0.2),magie=-int(ent.baseStats[MAGIE]*0.2),agility=-int(ent.baseStats[AGILITY]*0.2),intelligence=-int(ent.baseStats[INTELLIGENCE]*0.2),turnInit=-1,unclearable=True)
                tempTurnMsg += add_effect(tablEntTeam[1][0],ent,arch)
                ent.refreshEffects()

            elif ent.char.says.start != None and random.randint(0,99)<33:
                if ent.isNpc("Alice"):                          # Alice specials interractions
                    if dictIsPnjVar["Hélène"]:                                    # Helene in the fight
                        tempTurnMsg += "{0} : *\"{1}\"*\n".format(ent.icon,"__Arf, pourquoi je dois faire équipe avec elle déjà (＃￣0￣) ?__")
                        if dictIsPnjVar["Clémence"]:
                            if random.randint(0,99) < 50:
                                tempTurnMsg += "{0} : *\"{1}\"*\n".format('<:clemence:908902579554111549>',"__S'il te plait Alice, commence pas... Elle fait même pas le même taff que toi.__")
                                if dictIsPnjVar["Lena"]:
                                    tempTurnMsg += "{0} : *\"{1}\"*\n".format('<:lena:909047343876288552>',"Je sais que c'est tentant de se parler avec des ultra-sons quand on a votre ouïe, mais si vous pôuviez plutôt vous concentrer sur le combat ce sera cool")
                            else:
                                tempTurnMsg += "{0} : *\"{1}\"*\n".format('<:clemence:908902579554111549>',"Je l'ai entendue celle là !")
                
                    elif dictIsPnjVar["Félicité"] and dictIsPnjVar["Sixtine"] and dictIsPnjVar["Clémence"]:         # All sisters in the fight
                        tempTurnMsg += "{0} : *\"{1}\"*\n".format(ent.icon,"Allez ! Un p'tit combat en famille !")

                    elif dictIsPnjVar["Félicité"] or dictIsPnjVar["Sixtine"]:                         # A sister in the fight (except Clémence)
                        tempMsg = "Allez Féli ! On fonce !"
                        if dictIsPnjVar["Sixtine"]:
                            tempMsg = "Courrage Sixtine ! Ça va aller !"

                        tempTurnMsg += "{0} : *\"{1}\"*\n".format(ent.icon,tempMsg)
                    else:
                        tempTurnMsg += "{0} : *\"{1}\"*\n".format(ent.icon,ent.char.says.start)

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
                        tempTurnMsg += "{0} : *\"{1}\"*\n".format(ent.icon,rand)

                        if rand == "Sixtine, je devrais avoir ramenné des vielles peintures, ça t'interresse de regarder ça après le combat ?":
                            if random.randint(0,99) < 50:
                                tempTurnMsg += "{0} : *\"{1}\"*\n".format('<:sixtine:908819887059763261>',"Oh heu... Je comptais plutôt faire une sieste après moi...")
                                tempTurnMsg += "{0} : *\"{1}\"*\n".format(ent.icon,"Pas de soucis")
                            else:
                                tempTurnMsg += "{0} : *\"{1}\"*\n".format('<:sixtine:908819887059763261>',"Oh heu... Pourquoi pas...")

                    else:
                        tempTurnMsg += "{0} : *\"{1}\"*\n".format(ent.icon,ent.char.says.start)
                
                elif ent.isNpc("Shushi"):                       # Shushi specials interractions
                    if dictIsPnjVar["Lena"]:
                        tempTurnMsg += "{0} : *\"{1}\"*\n".format(ent.icon,"Allez Miman ! Ti va touz les défonzer !")
                        if random.randint(0,99) < 50:
                            if random.randint(0,99) < 50:
                                tempTurnMsg += "{0} : *\"{1}\"*\n".format('<:lena:909047343876288552>',"Voyons Shushi, c'est quoi ce language ?")
                            else:
                                tempTurnMsg += "{0} : *\"{1}\"*\n".format('<:lena:909047343876288552>',"`Ricane`")

                    else:
                        tempTurnMsg += "{0} : *\"{1}\"*\n".format(ent.icon,ent.char.says.start)

                elif ent.isNpc("Shihu"):                        # Shihu specials interractions
                    if dictIsPnjVar["Lena"]:
                        tempTurnMsg += "{0} : *\"{1}\"*\n".format(ent.icon,"Z'est le doit au Boum Boum ?")
                        tempTurnMsg += "{0} : *\"{1}\"*\n".format('<:lena:909047343876288552>',"`Ricane` Allez vas-y")
                    else:
                        tempTurnMsg += "{0} : *\"{1}\"*\n".format(ent.icon,ent.char.says.start)

                elif ent.isNpc("John") and dictIsPnjVar["Clémence"] and random.randint(0,99) < 50:
                    tempTurnMsg += "{0} : *\"{1}\"*\n".format(ent.icon,"D-Dit Clémence, ça te dirais une balade sous la pleine lune avec moi après ça ?")
                    tempTurnMsg += "<:clemence:908902579554111549> : *\"Hum ? Oh heu... Pourquoi pas écoute\"*\n"

                else:
                    tempTurnMsg += "{0} : *\"{1}\"*\n".format(ent.icon,ent.char.says.start)

    if tempTurnMsg != "__Début du combat :__\n":
        tempTurnMsg += "\n"

    nbLB = [0,0]

    # Passives skills and stuffs effects ---------------------------------
    for a in [0,1]:
        for b in tablEntTeam[a]:
            for skil in b.char.skills:
                if type(skil) == skill:
                    if skil.type == TYPE_PASSIVE:               # If the entity have a passive
                        effect=findEffect(skil.effectOnSelf)
                        tempTurnMsg += add_effect(b,b,effect," ({0})".format(skil.name),danger=danger)
                        
                        logs += "{0} gave the {1} effect at {2} for {3} turn(s)\n".format(b.char.name,effect.name,b.char.name,effect.turnInit)

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

                        tempTurnMsg += "{0} ({1}) a donné l'effet de __{2}__ (<:constitution:888746214999339068>) à son équipe ({3})\n".format(b.char.name,b.icon,effect.name,c.name)
                    else:                           # Any other effects
                        effect=findEffect(c.effect)
                        tempTurnMsg += add_effect(b,b,effect," ({0})".format(c.name),danger=danger)
                        
                        logs += "{0} gave the {1} effect at {2} for {3} turn(s)\n".format(b.char.name,effect.name,b.char.name,effect.turnInit)

            if b.char.aspiration == POIDS_PLUME:
                add_effect(b,b,poidPlumeEff)
                logs += "{0} gave the {1} effect to {2}\n".format(b.char.name,poidPlumeEff.name,b.char.name)

            elif b.char.aspiration == OBSERVATEUR:
                add_effect(b,b,obsEff)
                logs += "{0} gave the {1} effect to {2}\n".format(b.char.name,obsEff.name,b.char.name)

            elif b.char.aspiration == ENCHANTEUR:
                add_effect(b,b,enchant)
                logs += "{0} gave the {1} effect to {2}\n".format(b.char.name,enchant.name,b.char.name)

            if b.isNpc("Aillil") and len(tablEntTeam[0])>4:
                tempTurnMsg += add_effect(b,b,dephased)
                logs += "{0} gave the {1} effect at {2}\n".format(b.char.name,dephased.name,b.char.name)

            b.refreshEffects()

    if tablEntTeam[1][0].isNpc("The Giant Enemy Spider"):           # Giant Enemy Spider's legs summoning
        surrondingsCells = [findCell(b.cell.x-1,b.cell.y-1),findCell(b.cell.x-1,b.cell.y),findCell(b.cell.x-1,b.cell.y+1),findCell(b.cell.x,b.cell.y-1),findCell(b.cell.x,b.cell.y+1),findCell(b.cell.x+1,b.cell.y-1),findCell(b.cell.x+1,b.cell.y),findCell(b.cell.x+1,b.cell.y+1)]
        tablTemp = [TGESL1,TGESL2]
        for cmpt in range(8):
            toSummon = copy.deepcopy(tablTemp[cmpt//4])
            toSummon.name += " {0}".format(cmpt)
            summoned = tablEntTeam[1][0].summon(toSummon,time,surrondingsCells[cmpt],tablEntTeam,tablAliveInvoc,ignoreLimite=True)
            logs += "\n"+summoned["text"]
            time = summoned["timeline"]
            tablEntTeam = summoned["tablEntTeam"]
            tablAliveInvoc = summoned["tablAliveInvoc"]

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
                    if c.type in [TYPE_INDIRECT_REZ,TYPE_RESURECTION] or (c.id == "yt" and b.char.aspiration in [IDOLE,ALTRUISTE]) or c.id == "ul":
                        for d in tablEntTeam[a]:
                            d.ressurectable = True
                        break
            if b.ressurectable:
                break

    if not(auto):                               # Send the turn 0 msg
        await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = light_blue))
        await asyncio.sleep(2+(len(tempTurnMsg)/1500*5))

    fight = True

    # Début effectif du combat --------------------------------------------------------------------------------
    try:
        while fight:
            everyoneDead = [True,True]
            actTurn = time.getActTurn()
            nextNotAuto,lastNotAuto = 0,0

            everyoneStillThere = False
            for a in time.timeline : # Vérification du prochain joueur non automatique
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

                if tour >= 16:
                    ballerine = f"\n__Mort subite !__\nTous les combattants perdent **{5*(tour-15)}%** de leurs PV maximums\n"
                    for a in [0,1]:
                        for b in tablEntTeam[a]:
                            if b.hp > 0:
                                if type(b.char) == octarien and b.char.oneVAll:
                                    lose = int(b.maxHp*(0.005*(tour-15)))
                                else:
                                    lose = int(b.maxHp*(0.05*(tour-15)))
                                ballerine += "{0} : -{1} PV\n".format(b.icon,lose)
                                b.hp -= lose
                                if b.hp <= 0:
                                    ballerine += b.death(killer=b)

                    if not(auto):
                        if len(ballerine) > 4096:
                            ballerine = unemoji(ballerine)
                            if len(ballerine) > 4096:
                                ballerine = "OVERLOAD"
                        await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=ballerine))
                        await asyncio.sleep(2+(len(ballerine)/1500)*5)

                    logs += ballerine

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
                embInfo = discord.Embed(title = "Combat {0}".format(rdmEmoji),color = mainUser.color)

                if dangerThub != None:
                    embInfo.set_thumbnail(url=dangerThub)
                embInfo.add_field(name = "__Carte__",value=map(),inline = False)
                embInfo.add_field(name = "__Timeline__",value=time.icons(),inline = False)

            # Start of the turn ---------------------------------------------------------------------------------
            wasAlive = actTurn.hp > 0
            temp,atRange = "",actTurn.atRange()
            nbTargetAtRange = len(atRange)
            if wasAlive:
                logs += "\n\nTurn {0} - {1}:".format(tour,actTurn.char.name)
            ballerine = actTurn.startOfTurn(tablEntTeam=tablEntTeam)
            tempTurnMsg += ballerine
            logs += "\n"+ballerine

            # Main messages statistics generation ---------------------------------------------------------------
            if not(auto) and (wasAlive or actTurn.hp > 0):
                infoOp,cmpt = [],0
                for a in [0,1]:     # Generating the Hp's select menu
                    for b in tablEntTeam[a]:
                        if type(b.char) != invoc:
                            infoOp += [create_select_option(b.char.name,str(cmpt),getEmojiObject(b.icon),f"PV : {max(0,b.hp)} ({max(0,round(b.hp/b.maxHp*100))}%), R.S. : {b.healResist}%")]
                        cmpt+=1
                infoSelect = create_select(infoOp,placeholder="Voir les PVs des combattants")


                temp2 = actTurn.allStats()+[actTurn.resistance,actTurn.percing]
                critRate = round(actTurn.precision/3)+round(actTurn.agility/5)+actTurn.critical
                temp2 += [critRate]
                for a in range(0,len(allStatsNames)):               # Generating the stats field of the main message
                    if a == 7:
                        temp += f"\n\n__Réduction de dégâts__ : {temp2[a]}%"
                    elif a == 9:
                        if actTurn.char.aspiration in [POIDS_PLUME,OBSERVATEUR]:
                            temp2[a] += actTurn.specialVars["aspiSlot"].value
                        temp += f"\n__Taux de coup critique__ : {temp2[a]}%"
                    else:
                        temp += f"\n__{allStatsNames[a]}__ : {temp2[a]}"

                embInfo.add_field(name = f"__{actTurn.icon} {unhyperlink(actTurn.char.name)}__ (Niveau {actTurn.char.level})",value=f"PV : {max(0,actTurn.hp)} / {actTurn.maxHp}",inline = False)
                embInfo.add_field(name = "__Liste des effets :__",value=actTurn.effectIcons(),inline = True)
                embInfo.add_field(name = "__Statistiques :__",value = temp,inline = True)
                embInfo.add_field(name = "<:empty:866459463568850954>",value='**__Liste des effets :__**',inline=False)

                adds = ""

                for team in [0,1]:                                  # Generating the effects fields of the main message
                    teamView = ""
                    if nbLB[team] > 0:
                        lbCd = 0
                        for ent in time.initTimeline:
                            if ent.team == team:
                                for num in range(5):
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
                        elif ent.char.name == "Conviction des Ténèbres":
                            adds += "{0} : **{1}**/{2} ({3}%)\n".format(ent.icon,ent.hp,ent.maxHp,int(ent.hp/ent.maxHp*100))

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
                                bonusCount,malusCount,damageCount,dangerCount,armorCount = 0,0,0,0,0
                                if ent.effect != []:
                                    nameCast = ""
                                    for eff in ent.effect:
                                        if eff.effect.id == jevilEff.id:
                                            confusingConfusion = True
                                            break
                                        if not(eff.effect.silent or eff.effect.turnInit == -1) and eff.effect.replica == None:
                                            if eff.effect.type in [TYPE_BOOST,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ]:
                                                bonusCount += 1
                                            elif eff.effect.type in [TYPE_MALUS]:
                                                malusCount += 1
                                            elif eff.effect.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]:
                                                damageCount += 1
                                            elif eff.effect.type in [TYPE_ARMOR]:
                                                armorCount += 1

                                        elif eff.effect.replica != None:
                                            dangerCount += 1
                                            nameCast = eff.effect.name

                                    if dangerCount <= 0 and bonusCount+malusCount+damageCount+armorCount > 0:
                                        teamView += f"{ent.icon} : "
                                        if bonusCount > 0:
                                            teamView += f"Bon. x{bonusCount}"
                                        if malusCount > 0:
                                            teamView += f"; Mal. x{malusCount}"
                                        if damageCount > 0:
                                            teamView += f"; Dég. Ind. x{damageCount}"
                                        if armorCount > 0:
                                            teamView += f"; Arm. x{armorCount}"
                                        teamView += "\n"
                                    elif dangerCount > 0:
                                        teamView += "{0} : ⚠️ {1}\n".format(ent.icon,nameCast)
                    
                        if confusingConfusion:
                            teamView = "<a:giveup:902383022354079814>"
                    if len(teamView) > 1024:        # Still overload
                        teamView = "OVERLOAD !"
                    embInfo.add_field(name= "__Équipe {0} :__".format(["Bleue","Rouge"][team]),value=teamView,inline=True)

                if tablEntTeam[1][0].isNpc("Clémence pos."):        # Generating Clemence's and Alice's blood jauges field
                    bjValue = tablEntTeam[1][0].specialVars["clemBloodJauge"].value
                    if not(tablEntTeam[1][0].specialVars["clemMemCast"]):
                        if bjValue == 0:
                            adds += "<:BJLeftEmpty:900473865459875911>"
                        elif bjValue <= 25:
                            adds += "<:BJLeftPartial:900473933076262963>"
                        else:
                            adds += "<:BJLeftFull:900473987564441651>"

                        if bjValue <= 25:
                            adds += "<:BJMidEmpty:900473889539366994>"
                        elif bjValue <= 50:
                            adds += "<:BJMidPartial:900473950243520522>"
                        else:
                            adds += "<:BJMidFull:900474021781569604>"

                        if bjValue <= 50:
                            adds += "<:BJRightEmpty:900473909856587847>"
                        elif bjValue <= 75:
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

                            if bjValue == 0:
                                adds += "<:BJLeftEmpty:900473865459875911>"
                            elif bjValue <= 25:
                                adds += "<:aliceBJLeftMid:914780940058898462>"
                            else:
                                adds += "<:aliceBJLeftFull:914780954336305192>"

                            if bjValue <= 25:
                                adds += "<:BJMidEmpty:900473889539366994>"
                            elif bjValue <= 50:
                                adds += "<:aliceBJMidMid:914780972183072768>"
                            else:
                                adds += "<:aliceBJMidFull:914780988134019073>"

                            if bjValue <= 50:
                                adds += "<:BJRightEmpty:900473909856587847>"
                            elif bjValue <= 75:
                                adds += "<:aliceBJRightMid:914781005708165120>"
                            else:
                                adds += "<:aliceBJRightFull:914781018559492106>"

                            adds += " **{0}**".format(bjValue)
                            break

                if adds != "":                                              # Adding the Darkness convictions and Blood Jauges field
                    embInfo.add_field(name= "__Adds__",value=adds,inline=True)

                if not(actTurn.char.name == "Conviction des Ténèbres" and type(actTurn.char) == invoc):        # Editing the main message
                    try:
                        await msg.edit(embed = embInfo,components=[create_actionrow(infoSelect)])
                    except:
                        await msg.edit(embed = embInfo,components=[create_actionrow(create_select([create_select_option("Un icône de personnage n'a pas été trouvé","0",default=True)],disabled=True))])
                    if nextNotAuto == actTurn:
                        await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color))

            # Turn actions --------------------------------------------------------------------------------------
            nowStartOfTurn = datetime.datetime.now()
            if wasAlive and actTurn.hp <= 0 and not(auto):        # Died from indirect damages at the start
                await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color))
                if type(actTurn.char) != invoc:
                    await asyncio.sleep(2+(len(tempTurnMsg)/1500*5))
                else:
                    await asyncio.sleep(2+(len(tempTurnMsg)/2500*5))

            elif actTurn.hp > 0:                    # Still alive
                cmpt,iteration,ennemi = 0,actTurn.char.weapon.repetition,0
                optionChoice,unsuccess = OPTION_SKIP,True
                canMove,cellx,celly = [True,True,True,True],actTurn.cell.x,actTurn.cell.y
                surrondings = [findCell(cellx-1,celly),findCell(cellx+1,celly),findCell(cellx,celly-1),findCell(cellx,celly+1)]
                for a in range(0,len(surrondings)):
                    if surrondings[a] != None:
                        if surrondings[a].on != None and surrondings[a].on.status != STATUS_TRUE_DEATH:
                            canMove[a] = False
                    else:
                        canMove[a] = False

                if not(actTurn.stun):                   # The entity isn't stun, so he can play his turn
                    onReplica = False
                    for eff in actTurn.effect:
                        if eff.effect.replica != None:
                            onReplica = eff.effect
                            eff.decate(turn=99)
                            break

                    if onReplica == False:                  # The entity isn't already casting something
                        if not(actTurn.auto) :                      # Manual Fighter - Action select window
                            haveOption,unsuccess = False,False

                            waitingSelect = create_actionrow(create_select(options=[create_select_option("Veillez patienter...","PILLON!",'🕑',default=True)],disabled=True))
                            dateLimite = datetime.datetime.now() + datetime.timedelta(seconds=30)

                            haveIterate = False

                            def checkIsPlayerReact(reaction,user):
                                return user == awaitedUsr and reaction.message == choiceMsg
                                
                            def check(m):
                                return int(m.author_id) == int(actTurn.char.owner) and m.origin_message.id == choiceMsg.id

                            while not(haveOption) and not(unsuccess):
                                choiceMsgTemp,tempTabl,tabltabl,canBeUsed = "",[actTurn.char.weapon],[0]+actTurn.cooldowns,[]

                                for a in actTurn.char.skills:
                                    if type(a) == skill:
                                        tempTabl.append(a)
                                    else:
                                        tempTabl.append(None)

                                # Generating the main menu of the window
                                for a in range(len(tabltabl)):
                                    if tempTabl[a] != None and tabltabl[a] == 0:                                   # If the option is a valid option and the cooldown is down
                                        if type(tempTabl[a]) == weapon and len(actTurn.atRange()) > 0:                  # Aff. the number of targets if the option is a Weapon
                                            canBeUsed += [tempTabl[a]]
                                            choiceMsgTemp += f"{tempTabl[a].emoji} {tempTabl[a].name} (Cibles à portée : {str(nbTargetAtRange)})\n"
                                        elif type(tempTabl[a]) != weapon:
                                            babie = [TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE,TYPE_DAMAGE]
                                            target = ALLIES
                                            for b in babie:
                                                if tempTabl[a].type == b or tempTabl[a].id == "InfiniteDarkness":
                                                    target = ENNEMIS
                                                    break

                                            healMsg = ""
                                            if tempTabl[a].type in [TYPE_HEAL,TYPE_INDIRECT_HEAL]:                      # Aff. the "Allies in Danger" icons and number if the option is a Healing option
                                                healMsg = f" (<:INeedHealing:881587796287057951> x {len(actTurn.cell.getEntityOnArea(area=tempTabl[a].range,team=actTurn.team,wanted=target,lifeUnderPurcentage=50))})"

                                            line = tempTabl[a].type in babie
                                            if tempTabl[a].range != AREA_MONO:
                                                if (tempTabl[a].type != TYPE_INVOC and len(actTurn.cell.getEntityOnArea(area=tempTabl[a].range,team=actTurn.team,wanted=target,lineOfSight=line,dead=tempTabl[a].type == TYPE_RESURECTION)) > 0) or (tempTabl[a].type == TYPE_INVOC and tablAliveInvoc[actTurn.team] <3):
                                                    canBeUsed += [tempTabl[a]] 
                                                    choiceMsgTemp += f"{tempTabl[a].emoji} {tempTabl[a].name}{healMsg}\n"
                                            else:
                                                if type(tempTabl[a]) == weapon:
                                                    effect = tempTabl[a].effectOnUse
                                                else:
                                                    effect = tempTabl[a].effect
                                                if (tempTabl[a].type != TYPE_INVOC and len(actTurn.cell.getEntityOnArea(area=tempTabl[a].area,team=actTurn.team,wanted=target,lineOfSight=line,effect=effect)) > 0) or (tempTabl[a].type == TYPE_INVOC and tablAliveInvoc[actTurn.team] <3):                                        
                                                    canBeUsed += [tempTabl[a]]
                                                    choiceMsgTemp += f"{tempTabl[a].emoji} {tempTabl[a].name}{healMsg}\n"

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

                                            desc += f" - {tablTypeStr[a.type]} ({a.power}) - {stat}"
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
                                                powy = f"{a.power} {stat}"
                                            
                                            desc += f" - {tablTypeStr[a.type]} {powy}"

                                        mainOptions += [create_select_option(unhyperlink(a.name),str(cmpt),getEmojiObject(a.emoji),desc)]
                                    else:
                                        mainOptions += [create_select_option(unhyperlink(a.name),str(cmpt),a.emoji)]
                                    cmpt += 1

                                mainSelect = create_select(options=mainOptions,placeholder = "Séléctionnez une option :")

                                if haveIterate:                         # Time limite stuff
                                    timeLimite = (dateLimite - datetime.datetime.now()).total_seconds()
                                    await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = choiceMsgTemp).set_footer(text=f'Fin du tour dans {round(timeLimite)} secondes'),components=[waitingSelect])
                                    await asyncio.sleep(3)
                                    dateLimite = dateLimite+datetime.timedelta(seconds=3)

                                timeLimite = (dateLimite - datetime.datetime.now()).total_seconds()
                                await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = choiceMsgTemp).set_footer(text=f'Fin du tour dans {round(timeLimite)} secondes'),components=[create_actionrow(mainSelect)])
                                haveIterate = True
                                awaitedUsr = await bot.fetch_user(actTurn.char.owner)

                                validoption = False
                                while not(validoption):
                                    timeLimite = (dateLimite - datetime.datetime.now()).total_seconds()
                                    try:
                                        react = await wait_for_component(bot,components=mainSelect,check=check,timeout = timeLimite)
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

                                        dateLimite = dateLimite+datetime.timedelta(seconds=3)
                                        timeLimite = (dateLimite - datetime.datetime.now()).total_seconds()
                                        await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp).set_footer(text=f'Fin du tour dans {round(timeLimite)} secondes'),components=[mainSelect]+weapSelect)

                                    elif choiceMsgTemp != "":
                                        timeLimite = (dateLimite - datetime.datetime.now()).total_seconds()
                                        await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp).set_footer(text=f'Fin du tour dans {round(timeLimite)} secondes'),components=[mainSelect,waitingSelect])
                                        await asyncio.sleep(3)
                                        dateLimite = dateLimite+datetime.timedelta(seconds=3)
                                        timeLimite = (dateLimite - datetime.datetime.now()).total_seconds()
                                        await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp).set_footer(text=f'Fin du tour dans {round(timeLimite)} secondes'),components=[mainSelect,create_actionrow(weapSelect)])

                                    timeLimite = (dateLimite - datetime.datetime.now()).total_seconds()
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
                                    skillToUse,nbTargetAtRangeSkill,targetAtRangeSkill = react,0,[]
                                    ballerine, babie= [TYPE_ARMOR,TYPE_BOOST,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ,TYPE_RESURECTION,TYPE_HEAL],[TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE]
                                    if skillToUse.range != AREA_MONO:                    
                                        for a in ballerine:
                                            if a == skillToUse.type:
                                                targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.range,team=actTurn.team,wanted=ALLIES,dead=skillToUse.type == TYPE_RESURECTION)
                                                break
                                        for a in babie:
                                            if a == skillToUse.type:
                                                targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.range,team=actTurn.team,wanted=ENNEMIS,lineOfSight=True)
                                                break

                                    else:
                                        for a in ballerine:
                                            if a == skillToUse.type:
                                                targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES,directTarget=False)
                                                break
                                        for a in babie:
                                            if a == skillToUse.type:
                                                targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENNEMIS,directTarget=False)
                                                break

                                        if skillToUse.type == TYPE_UNIQUE:
                                            targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALL)
                                        choiceMsgTemp += "Les combattants suivants seront affectés par la compétence :\n"

                                    if skillToUse.type != TYPE_INVOC:
                                        nbTargetAtRangeSkill = len(targetAtRangeSkill)

                                        for a in range(0,nbTargetAtRangeSkill):
                                            choiceMsgTemp += f"{a} - {targetAtRangeSkill[a].quickEffectIcons()}"
                                            desc = f"PV : {int(targetAtRangeSkill[a].hp/targetAtRangeSkill[a].maxHp*100)}%, Pos : {targetAtRangeSkill[a].cell.x} - {targetAtRangeSkill[a].cell.y}"
                                            if react.area not in [AREA_MONO,AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES]:
                                                if react.type in ballerine:
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

                                        dateLimite = dateLimite+datetime.timedelta(seconds=3)
                                        timeLimite = (dateLimite - datetime.datetime.now()).total_seconds()
                                        await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp).set_footer(text=f'Fin du tour dans {round(timeLimite)} secondes'),components=[mainSelect]+skillSelect)

                                    elif choiceMsgTemp != "":
                                        timeLimite = (dateLimite - datetime.datetime.now()).total_seconds()
                                        await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp).set_footer(text=f'Fin du tour dans {round(timeLimite)} secondes'),components=[mainSelect,waitingSelect])
                                        await asyncio.sleep(3)
                                        dateLimite = dateLimite+datetime.timedelta(seconds=3)
                                        timeLimite = (dateLimite - datetime.datetime.now()).total_seconds()
                                        await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp).set_footer(text=f'Fin du tour dans {round(timeLimite)} secondes'),components=[mainSelect]+[create_actionrow(skillSelect)])

                                    await choiceMsg.clear_reactions()
                                    try:
                                        timeLimite = (dateLimite - datetime.datetime.now()).total_seconds()
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
                                        choiceOption = OPTION_SKIP

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
                                            timeLimite = (dateLimite - datetime.datetime.now()).total_seconds()
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

                            logs += "\nManual fighter. Option selected : {0}".format(["Use Weapon","Use Skill","Move","Skip"][optionChoice])
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
                                nowStartOfTurn = datetime.datetime.now()

                        elif not(actTurn.auto) and not(unsuccess):
                            actTurn.missedLastTurn = False

                        if unsuccess or type(ennemi)==int: # AI's stuffs

                            if actTurn.char.name == "Conviction des Ténèbres" and type(actTurn.char) == invoc:
                                optionChoice = OPTION_SKIP

                            else: # Normal IA
                                nearestEnnemi,nearestDistance,Cell,nearestCell = 0,9999,actTurn.cell,0

                                for a in tablAllCells: # Ennemi le plus proche
                                    if a.on != None:
                                        if a.on.team != actTurn.team and a.on.hp > 0:
                                            if Cell.distance(cell=a) < nearestDistance:
                                                nearestEnnemi, nearestDistance, nearestCell = a.on,Cell.distance(cell=a),a

                                ennemi = nearestEnnemi
                                
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

                                if (len(actTurn.cell.getEntityOnArea(area=AREA_CIRCLE_2,team=actTurn.team,wanted=ENNEMIS,directTarget=False)) > 0 and (actTurn.char.aspiration not in [BERSERK,OBSERVATEUR,POIDS_PLUME,TETE_BRULE,MAGE,ENCHANTEUR]) and actTurn.char.weapon.range != RANGE_MELEE) or lastDPT or ennemiesdying:
                                    choisenIA = AI_OFFERUDIT

                                logs += "\nAuto Fighter. Selected AI : {0}".format(["AI Damage","AI Idole","AI Shield","AI Aventurer","AI Healer","AI agressive supp","AI Mage","AI Enchant"][choisenIA])
                                # Définition des probabilités :
                                # [DPT,BOOST,SHIELD,AVENTURE,ALTRUISTE,OFFERUt,MAGE,ECHANT]

                                probaAtkWeap = [70,30,40,30,30,40,50,50] 
                                probaHealWeap = [0,70,30,30,80,10,30,30]
                                probaIndirectWeap = [20,30,40,30,20,50,70,70]
                                probaReaSkill = [50,150,150,30,150,100,50,50]
                                probIndirectReacSkill = [30,150,100,30,150,80,30,30]
                                probaAtkSkill = [80,40,70,30,40,70,100,100]
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
                                    for value in range(len(probaArmor)):
                                        probaArmor[value] = int(probaArmor[value]*2)

                                # Weapons proba's ----------------------------------
                                if actTurn.char.weapon.name == "noneWeap":
                                    probaHealWeap = [0,0,0,0,0,0,0,0]
                                    probaIndirectWeap = [0,0,0,0,0,0,0,0]
                                    probaAtkWeap = [0,0,0,0,0,0,0,0]
                                else:
                                    if actTurn.char.weapon.type == TYPE_DAMAGE:
                                        probaHealWeap = [0,0,0,0,0,0,0,0]
                                        probaIndirectWeap = [0,0,0,0,0,0,0,0]
                                    elif actTurn.char.weapon.type == TYPE_HEAL:
                                        probaAtkWeap = [0,0,0,0,0,0,0,0]
                                        probaIndirectWeap = [0,0,0,0,0,0,0,0]
                                        if nbTargetAtRange == 0 and len(actTurn.cell.getEntityOnArea(area=actTurn.char.weapon.effectiveRange,team=actTurn.team,wanted=actTurn.char.weapon.target)) > 0:
                                            probaHealWeap = [0,0,0,0,0,0,0,0]
                                    else:
                                        probaHealWeap = [0,0,0,0,0,0,0,0]
                                        probaAtkWeap = [0,0,0,0,0,0,0,0]

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
                                    for a in (0,1,2,3,4):
                                        if actTurn.cooldowns[a] <= 0 and type(actTurn.skills[a]) == skill:
                                            if actTurn.skills[a].type == TYPE_DAMAGE:
                                                if (actTurn.skills[a].range == AREA_MONO and len(actTurn.cell.getEntityOnArea(area=actTurn.skills[a].area,team=actTurn.team,wanted=ENNEMIS,effect=actTurn.skills[a].effect))> 0) or (actTurn.skills[a].range != AREA_MONO and len(actTurn.cell.getEntityOnArea(area=actTurn.skills[a].range,team=actTurn.team,wanted=ENNEMIS,effect=actTurn.skills[a].effect))> 0):
                                                    haveOffSkills = True
                                                    break

                                    if haveOffSkills:
                                        probaHealWeap = [0,0,0,0,0,0,0,0]
                                        probaIndirectWeap = [0,0,0,0,0,0,0,0]
                                        probaAtkWeap = [0,0,0,0,0,0,0,0]
                                        logs += "\nSomes offensives skills with targets at range have been found. Weapon's proba neutralized"
                                    else:
                                        logs += "\nNo available offensives skills have been found"

                                healSkill,atkSkill,reaSkill,indirectReaSkill,indirectAtkSkill,boostSkill,malusSkill,armorSkill,invocSkill = [],[],[],[],[],[],[],[],[]

                                for a in range(0,5): # Catégorisation des sorts
                                    actSkill = actTurn.char.skills[a]
                                    if actTurn.cooldowns[a] == 0 and actSkill != None and actSkill != "0":
                                        if actSkill.range == AREA_MONO:                                     # If the skill is launch on self
                                            allieAtRange,ennemiAtRange = len(actTurn.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ALLIES,effect=actSkill.effect,ignoreInvoc=True,directTarget=False))> 1,len(actTurn.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ENNEMIS,effect=actSkill.effect,directTarget=False))> 0
                                            if actSkill.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL] and len(actTurn.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ALLIES,effect=actSkill.effect,lifeUnderPurcentage=90,ignoreInvoc = True,directTarget=False))> 0 and actSkill.id not in ["yt","ul"]:
                                                if actSkill.id != secondWind.id:                                   # If the skill isn't Second Wind
                                                    healSkill.append(actSkill)
                                                elif actTurn.hp/actTurn.maxHp <= 0.25:                          # Else, if the fighter is dying
                                                    healSkill.append(actSkill)
                                            elif actSkill.type == TYPE_DAMAGE and ennemiAtRange:            # Damage skills
                                                atkSkill.append(actSkill)
                                            elif actSkill.type == TYPE_RESURECTION and len(actTurn.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ALLIES,dead=True)) > 0:                         # Resu skills (none lol)
                                                if not(aliceMemCastTabl[actTurn.team]):
                                                    reaSkill.append(actSkill)
                                            elif actSkill.type == TYPE_INDIRECT_REZ and allieAtRange:       # Indirect Resu skills (Zelian R)
                                                indirectReaSkill.append(actSkill)
                                            elif actSkill.type == TYPE_INDIRECT_DAMAGE and ennemiAtRange:   # Indirect damage skills
                                                indirectAtkSkill.append(actSkill)
                                            elif actSkill.type == TYPE_BOOST and allieAtRange:              # Buff skills
                                                boostSkill.append(actSkill)
                                            elif actSkill.type == TYPE_MALUS and ennemiAtRange:             # Debuff skills
                                                malusSkill.append(actSkill)
                                            elif actSkill.type == TYPE_ARMOR and allieAtRange:              # Armor skills
                                                if actSkill.id not in ["yt"] or (actSkill.id == "yt" and nbLB[actTurn.team] == 1):
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

                                            elif actSkill.type == TYPE_UNIQUE:                              # Other
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

                                            elif actSkill.type == TYPE_INVOC and len(actTurn.cell.getEmptyCellsInArea(area=actSkill.range,team=actTurn.team))>0: # Invocation
                                                temp = actTurn.cell.getEmptyCellsInArea(area=actSkill.range,team=actTurn.team)
                                                for b in temp[:]:
                                                    if actTurn.team == 0:
                                                        if b.x > 2:
                                                            temp.remove(b)
                                                    elif b.x < 3:
                                                        temp.remove(a)

                                                invocSkill.append(actSkill)

                                            elif actSkill.id in ["yt","ul"]: 
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

                                            if (actSkill.type == TYPE_HEAL or actSkill.type == TYPE_INDIRECT_HEAL) and len(allieTablHeal)> 0:
                                                if actSkill.id != vampirisme.id:
                                                    healSkill.append(actSkill)
                                                elif len(actTurn.cell.getEntityOnArea(area=actSkill.range,team=actTurn.team,wanted=ALLIES,lifeUnderPurcentage=90,effect=actSkill.effect,ignoreInvoc=True,ignoreAspiration=[PROTECTEUR,ALTRUISTE,IDOLE,PREVOYANT]))> 0:
                                                    healSkill.append(actSkill)
                                            
                                            elif actSkill.type == TYPE_DAMAGE and ennemiAtRange:
                                                if actSkill.id != trans.id:
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
                                            
                                            elif actSkill.type == TYPE_RESURECTION and len(actTurn.cell.getEntityOnArea(area=actSkill.range,team=actTurn.team,wanted=ALLIES,dead=True)) > 0:
                                                if not(aliceMemCastTabl[actTurn.team]):
                                                    reaSkill.append(actSkill)

                                            elif actSkill.type == TYPE_INDIRECT_REZ and allieAtRange:
                                                indirectReaSkill.append(actSkill)

                                            elif actSkill.type == TYPE_INDIRECT_DAMAGE and ennemiAtRange: # Indirect damge
                                                if actSkill.id not in [poisonus.id,bleedingTrap.id]:
                                                    indirectAtkSkill.append(actSkill)
                                                elif actSkill.id == poisonus.id:
                                                    if actTurn.char.weapon.effectOnUse != None and findEffect(actTurn.char.weapon.effectOnUse).id == estal.id:
                                                        target = sorted(ennemiTabl,key=lambda ent:actTurn.getAggroValue(ent))[0]
                                                        if len(target.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ENNEMIS,lineOfSight = True)) > 1:
                                                            indirectAtkSkill.append(actSkill)
                                                    else:
                                                        indirectAtkSkill.append(actSkill)
                                                elif actSkill.id == hemoragie.id:
                                                    if actTurn.char.weapon.effectOnUse != None and findEffect(actTurn.char.weapon.effectOnUse).id == hemoragie.id:
                                                        target = sorted(ennemiTabl,key=lambda ent:actTurn.getAggroValue(ent))[0]
                                                        if len(target.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ENNEMIS,lineOfSight = True)) > 1:
                                                            indirectAtkSkill.append(actSkill)
                                                    else:
                                                        indirectAtkSkill.append(actSkill)

                                            elif actSkill.type == TYPE_BOOST and allieAtRange:
                                                effect = findEffect(actSkill.effect[0])
                                                if effect.turnInit >= 2 and actSkill.id != derobade.id:
                                                    boostSkill.append(actSkill)
                                                elif len(actTurn.cell.getEntityOnArea(area=actSkill.range,team=actTurn.team,wanted=ALLIES,effect=actSkill.effect,ignoreInvoc = True)) > 1:
                                                    if actSkill.id != derobade.id:                          # Any skills
                                                        boostSkill.append(actSkill)
                                                    elif actTurn.hp/actTurn.maxHp <= 0.25:                  # Dérobade
                                                        boostSkill.append(actSkill)
                                            elif actSkill.type == TYPE_MALUS and ennemiAtRange:
                                                if actSkill not in [boom]: 
                                                    malusSkill.append(actSkill)
                                                elif actSkill == boom: # Si il ne reste qu'un ennemi, ne pas prendre en compte Réaction en chaîne
                                                    team2see = tablEntTeam[int(not(actTurn.team))][:]
                                                    for b in team2see[:]:
                                                        if b.hp <= 0:
                                                            team2see.remove(b)

                                                    if len(team2see) > 1:
                                                        malusSkill.append(boom)
                                            elif actSkill.type == TYPE_ARMOR and len(allieTablHeal)>0:
                                                if actSkill.id != convert.id:
                                                    if ennemiCast and actSkill.area == AREA_ALL_ALLIES: # Si l'ennemi cast et que la compétence touche tous les alliés : Proba augmentée
                                                        armorSkill.append(actSkill)
                                                    if ennemiCast and actSkill.area != AREA_MONO: # Si l'ennemi cast et que la compétence est pas mono : Proba augmentée
                                                        armorSkill.append(actSkill)
                                                    armorSkill.append(actSkill)

                                                elif len(actTurn.cell.getEntityOnArea(area=actSkill.range,team=actTurn.team,wanted=ALLIES,effect=actSkill.effect,ignoreInvoc = True,ignoreAspiration=[PROTECTEUR,ALTRUISTE,IDOLE,PREVOYANT])) > 0:
                                                    armorSkill.append(actSkill)

                                            elif actSkill.type == TYPE_UNIQUE:
                                                for b in [chaos]: # Boost
                                                    if b == actSkill:
                                                        boostSkill.append(b)
                                            
                                            elif actSkill.type == TYPE_INVOC and len(actTurn.cell.getEmptyCellsInArea(area=actSkill.range,team=actTurn.team))>0:
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

                                probTabl = [probaReaSkill,probIndirectReacSkill,probaAtkSkill,probaIndirectAtkSkill,probaHealSkill,probaBoost,probaMalus,probaArmor]
                                for a in range(0,8):
                                    analyse = [reaSkill,indirectReaSkill,atkSkill,indirectAtkSkill,healSkill,boostSkill,malusSkill,armorSkill][a]
                                    if len(analyse) == 0:
                                        probTabl[a] = [0,0,0,0,0,0,0,0]
                                    elif a == 0:
                                        logs += "\nRésu peut être tiré\nExpected ProbTabl : {0}\n".format(probTabl[0][choisenIA])

                                if len(invocSkill) > 0 and tablAliveInvoc[actTurn.team]<3:
                                    if actTurn.char.aspiration == INVOCATEUR:
                                        probaInvoc = [65,65,65,65,65,65,65,65]
                                    else:
                                        probaInvoc = [40,40,40,40,40,40,40,40]
                                else:
                                    probaInvoc = [0,0,0,0,0,0,0,0]

                                totalProba = probaAtkWeap[choisenIA]+probaHealWeap[choisenIA]

                                for a in probTabl:
                                    totalProba+= a[choisenIA]

                                totalProba += probaIndirectWeap[choisenIA]+probaInvoc[choisenIA] + 1
                                probaRoll = random.randint(0,totalProba)-1
                                logs += "\nTotal Proba : {0} - ProbaRoll : {1}".format(totalProba,probaRoll)

                                optionChoisen = False

                                if probaRoll <= probaAtkWeap[choisenIA] and probaAtkWeap[choisenIA] > 0: #Attaque à l'arme
                                    logs += "\nSelected option : Damage with weapon"
                                    nearestEnnemi,nearestDistance,myCell,nearestCell = 0,100,actTurn.cell,0
                                    if nbTargetAtRange > 0:
                                        atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
                                        optionChoice,ennemi = OPTION_WEAPON,atRange[0]

                                    else:
                                        logs += "\nNo target at range. Trying to move"
                                        
                                        tempEnemy = actTurn.cell.getEntityOnArea(area=AREA_ALL_ENEMIES,team=actTurn.team,wanted=ENNEMIS,lineOfSight=True,ignoreInvoc = True)

                                        tempEnemy.sort(key=lambda ent:actTurn.getAggroValue(ent))
                                        nearestCell = tempEnemy[0].cell

                                        optionChoice,Cell = OPTION_MOVE,actTurn.cell
                                        if Cell.x - nearestCell.x > 0 and canMove[0]:
                                            choiceToMove = surrondings[0]
                                        elif Cell.x - nearestCell.x < 0 and canMove[1]:
                                            choiceToMove = surrondings[1]
                                        elif Cell.y - nearestCell.y > 0 and canMove[2]:
                                            choiceToMove = surrondings[2]
                                        elif Cell.y - nearestCell.y < 0 and canMove[3]:
                                            choiceToMove = surrondings[3]
                                        else:
                                            if canMove[2]:
                                                choiceToMove = surrondings[2]
                                            elif canMove[3]:
                                                choiceToMove = surrondings[3]
                                            else:
                                                optionChoice=OPTION_SKIP
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
                                        
                                        tempEnemy = actTurn.cell.getEntityOnArea(area=AREA_ALL_ALLIES,team=actTurn.team,wanted=ALLIES,ignoreInvoc = True)

                                        tempEnemy.sort(key=lambda ent:getHealTarget(tempEnemy, actTurn.char.weapon))
                                        nearestCell = tempEnemy[0].cell

                                        optionChoice,Cell = OPTION_MOVE,actTurn.cell
                                        if Cell.x - nearestCell.x > 0 and canMove[0]:
                                            choiceToMove = surrondings[0]
                                        elif Cell.x - nearestCell.x < 0 and canMove[1]:
                                            choiceToMove = surrondings[1]
                                        elif Cell.y - nearestCell.y > 0 and canMove[2]:
                                            choiceToMove = surrondings[2]
                                        elif Cell.y - nearestCell.y < 0 and canMove[3]:
                                            choiceToMove = surrondings[3]
                                        else:
                                            if canMove[2]:
                                                choiceToMove = surrondings[2]
                                            elif canMove[3]:
                                                choiceToMove = surrondings[3]
                                            else:
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
                                        atRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ENNEMIS,lineOfSight=True,effect=randomSkill.effect,ignoreInvoc = (randomSkill.effectOnSelf == None or (randomSkill.effectOnSelf != None and findEffect(randomSkill.effectOnSelf).replica != None)))

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
                                        nearestEnnemi,nearestDistance,myCell,nearestCell = 0,100,actTurn.cell,0
                                        if randomSkill.id != convert.id:
                                            tablAtRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ALLIES,lifeUnderPurcentage=90,effect=randomSkill.effect)
                                        else:
                                            tablAtRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ALLIES,lifeUnderPurcentage=90,effect=randomSkill.effect,ignoreAspiration=[ALTRUISTE,PREVOYANT,PROTECTEUR,IDOLE])
                                        for a in tablAtRange: # Allié le blessé
                                            if a.team == actTurn.team and a.hp > 0:
                                                if a.hp/a.maxHp < nearestDistance:
                                                    nearestEnnemi, nearestDistance, nearestCell = a,a.hp/a.maxHp,a.cell

                                        optionChoice = OPTION_SKILL
                                        skillToUse = randomSkill
                                        ennemi = nearestEnnemi

                                    else:
                                        if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,wanted=ALLIES,effect=randomSkill.effect,directTarget=False)) > 0:
                                            optionChoice = OPTION_SKILL
                                            skillToUse = randomSkill
                                            ennemi = actTurn
                                    
                                    optionChoisen = True
                                elif not(optionChoisen):
                                    probaRoll -= probTabl[7][choisenIA]

                                if probaRoll <= probaIndirectWeap[choisenIA] and probaIndirectWeap[choisenIA] > 0 and not(optionChoisen): #Attaque à l'arme indirecte
                                    logs += "\nSelected option : Indirect damages with weapon"
                                    nearestEnnemi,nearestDistance,myCell,nearestCell = 0,100,actTurn.cell,0
                                    if nbTargetAtRange > 0:
                                        atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
                                        optionChoice,ennemi = OPTION_WEAPON,atRange[0]

                                    else:
                                        tempEnemy = copy.deepcopy(tablEntTeam[int(not(actTurn.team))])

                                        tempEnemy.sort(key=lambda ent:actTurn.cell.distance(ent.cell))
                                        nearestCell = tempEnemy[0].cell
                                        
                                        optionChoice,Cell = OPTION_MOVE,actTurn.cell
                                        if Cell.x - nearestCell.x > 0 and canMove[0]:
                                            choiceToMove = [Cell.x-1,Cell.y]
                                        elif Cell.x - nearestCell.x < 0 and canMove[1]:
                                            choiceToMove = [Cell.x +1,Cell.y]
                                        elif Cell.y - nearestCell.y > 0 and canMove[2]:
                                            choiceToMove = [Cell.x,Cell.y -1]
                                        elif Cell.y - nearestCell.y < 0 and canMove[3]:
                                            choiceToMove = [Cell.x,Cell.y +1]
                                        else:
                                            if canMove[2]:
                                                choiceToMove = [Cell.x,Cell.y -1]
                                            elif canMove[3]:
                                                choiceToMove = [Cell.x,Cell.y +1]
                                            else:
                                                optionChoice=OPTION_SKIP

                                    optionChoisen = True
                                elif not(optionChoisen):
                                    probaRoll -= probaIndirectWeap[choisenIA]
                    
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

                                elif actTurn.isNpc("Ailill") and actTurn.cooldowns[2] == 0:
                                    atRangeAilill = actTurn.cell.getEntityOnArea(area=ailillSkill.range,team=actTurn.team,wanted=ENNEMIS,lineOfSight=True,effect=ailillSkill.effect,ignoreInvoc = (ailillSkill.effectOnSelf == None or (ailillSkill.effectOnSelf != None and findEffect(ailillSkill.effectOnSelf).replica != None)))
                                    if len(atRange) > 0:
                                        optionChoice = OPTION_SKILL
                                        skillToUse = ailillSkill
                                        atRangeAilill.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
                                        ennemi = atRange[0]

                                elif actTurn.isNpc("Luna") and type(actTurn.char) == octarien and ((lunaSpe4 in atkSkill) or (actTurn.hp/actTurn.maxHp <= 0.25 and actTurn.cooldowns[0] < 10)):
                                    optionChoice = OPTION_SKILL
                                    skillToUse = lunaSpe4
                                    ennemi = actTurn

                                elif actTurn.isNpc("Clémence pos.") and actTurn.cooldowns[2] == 0 and (tour >= 7 or actTurn.hp/actTurn.maxHp <= 0.35):
                                    optionChoice = OPTION_SKILL
                                    skillToUse = clemUltCast
                                    ennemi = actTurn

                        if type(ennemi) == int:
                            logs += "\nNo target have been found. Skipping the turn"
                            optionChoice = OPTION_SKIP

                    else:
                        logs += "\nReplica found"
                        skilly = findSkill(onReplica.replica)
                        if not(skilly.area == AREA_MONO and onReplica.replicaTarget.hp <= 0):
                            optionChoice = OPTION_SKILL
                            skillToUse = skilly
                            ennemi = onReplica.replicaTarget
                        else:
                            logs += "\nInitial target down, taking another target at range"
                            skilly = copy.deepcopy(skilly)
                            skilly.power = int(skilly.power * 0.7)
                            skilly.name = skilly.name + " (Changement de dernière minute)"

                            atRange = actTurn.cell.getEntityOnArea(area=skilly.range,team=actTurn.team,wanted=ENNEMIS,lineOfSight=True,effect=skilly.effect,ignoreInvoc = True)

                            if len(atRange) <= 0:
                                atRange = atRange = actTurn.cell.getEntityOnArea(area=AREA_CIRCLE_7,team=actTurn.team,wanted=ENNEMIS,lineOfSight=True,effect=skilly.effect,ignoreInvoc = True)
                                logs += "\nNo fucking target at range. The ennemi in line of sight with the more aggro will be targeted, but the power will be cut again"
                                skilly.power = int(skilly.power*0.714)

                            atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)

                            optionChoice = OPTION_SKILL
                            skillToUse = skilly
                            ennemi = atRange[0]

                    if optionChoice == OPTION_WEAPON: #Option : Attaque
                        if actTurn.char.weapon.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]: # Agressive Weapon
                            logs += "\n{0} is attacking {1} with their weapon\n".format(actTurn.char.name,ennemi.char.name)
                            cmpt = 0
                            while cmpt < iteration:
                                isAlive = ennemi.hp > 0
                                if not(isAlive) :
                                    break
                                if actTurn.char.weapon.say != "":
                                    tempTurnMsg += f"\n{actTurn.icon} : *{skillToUse.say}*"
                                if actTurn.char.weapon.message == None:
                                    tempTurnMsg += f"\n__{actTurn.char.name} attaque {ennemi.char.name} avec son arme :__\n"
                                else:
                                    tempTurnMsg += "\n__"+actTurn.char.weapon.message.format(actTurn.char.name,ennemi.char.name)+"__\n"
                                
                                ballerine = actTurn.attack(target=ennemi,value=actTurn.char.weapon.power,icon=actTurn.char.weapon.emoji,area=actTurn.char.weapon.area,use=actTurn.char.weapon.use,onArmor=actTurn.char.weapon.onArmor,effectOnHit=actTurn.char.weapon.effectOnUse)
                                logs+= ballerine
                                tempTurnMsg += ballerine
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
                                        ballerine = add_effect(actTurn,ennemi2,findEffect(actTurn.char.weapon.effectOnUse))
                                        
                                        logs+= ballerine
                                        tempTurnMsg += ballerine
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
                                tempTurnMsg += f"\n__{actTurn.char.name} soigne {ennemi.char.name} avec son arme :__\n"
                            else:
                                tempTurnMsg += "\n__"+actTurn.char.weapon.message.format(actTurn.char.name,ennemi.char.name)+"__\n"

                            for a in ennemi.cell.getEntityOnArea(area=actTurn.char.weapon.area,team=actTurn.team,wanted=ALLIES,directTarget=False):
                                ballerine = actTurn.heal(a, actTurn.char.weapon.emoji, actTurn.char.weapon.use, actTurn.char.weapon.power,danger=danger)
                                tempTurnMsg += ballerine
                                logs += ballerine

                            if actTurn.char.weapon.effectOnUse != None:
                                ballerine = add_effect(actTurn,ennemi,findEffect(actTurn.char.weapon.effectOnUse),danger=danger)
                                
                                logs+= ballerine
                                tempTurnMsg += ballerine

                                for a in hourglassEffects:
                                    if a == findEffect(actTurn.char.weapon.effectOnUse):
                                        add_effect(actTurn,ennemi,jetlag.setTurnInit(newTurn = 2))
                                        
                                        break
                                ennemi.refreshEffects()

                        elif actTurn.char.weapon.effectOnUse != None: # Other weapons
                            logs += "\n\n{0} is using their weapon on {1}".format(actTurn.char.name,ennemi.char.name)
                            tempTurnMsg += f"\n__{actTurn.char.name} utilise son arme sur {ennemi.char.name} :__\n"
                            ballerine = add_effect(actTurn,ennemi,findEffect(actTurn.char.weapon.effectOnUse),danger=danger)
                            
                            logs+= ballerine
                            tempTurnMsg += ballerine

                            for a in hourglassEffects:
                                if a == findEffect(actTurn.char.weapon.effectOnUse):
                                    add_effect(actTurn,ennemi,jetlag.setTurnInit(newTurn = 2))
                                    
                                    break
                            ennemi.refreshEffects()

                    elif optionChoice == OPTION_MOVE: #Option : Déplacement
                        logs += "\n\n{0} is moving".format(actTurn.char.name)
                        temp = actTurn.cell
                        actTurn.move(cellToMove=choiceToMove)
                        logs += "\n{0} have been moved from {1}:{2} to {3}:{4}".format(actTurn.char.name,temp.x,temp.y,choiceToMove.x,choiceToMove.y)
                        tempTurnMsg+= "\n"+actTurn.char.name+" se déplace\n"

                    elif optionChoice == OPTION_SKIP: #Passage de tour
                        logs += "\n\n{0} is skipping their turn".format(actTurn.char.name)
                        tempTurnMsg += f"\n{actTurn.char.name}  passe son tour\n"

                    elif optionChoice == OPTION_SKILL: #Skill :(
                        logs += "\n\n{0} is using {1} on {2}".format(actTurn.char.name,skillToUse.name,ennemi.char.name)
                        if skillToUse.say != "":
                            tempTurnMsg += f"\n{actTurn.icon} : *\"{skillToUse.say}\"*"

                        if actTurn.char.says.ultimate != None and skillToUse.ultimate and (skillToUse.type != TYPE_DAMAGE or (skillToUse.type == TYPE_DAMAGE and skillToUse.power > 0)):
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,actTurn.char.says.ultimate)
                        if actTurn.char.says.limiteBreak != None and skillToUse.id == trans.id:
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,actTurn.char.says.limiteBreak)

                        if skillToUse.message == None:
                            tempTurnMsg += f"\n__{actTurn.char.name} utilise la compétence {skillToUse.name} :__\n"
                        else: 
                            tempTurnMsg += "\n__"+ skillToUse.message.format(actTurn.char.name,skillToUse.name,ennemi.char.name)+"__\n"
                        for a in range(0,5):
                            if type(actTurn.char.skills[a]) == skill:
                                if skillToUse.id == actTurn.char.skills[a].id:
                                    actTurn.cooldowns[a] = skillToUse.cooldown
                                if skillToUse.id == "yt" and actTurn.char.skills[a].ultimate and actTurn.cooldowns[a] < 2:
                                    actTurn.cooldowns[a] = 2

                        if skillToUse.shareCooldown and skillToUse.id != kikuRes.id:
                            for a in tablEntTeam[actTurn.team]:
                                for b in range(0,len(a.char.skills)):
                                    if type(a.char.skills[b]) == skill:
                                        if a.char.skills[b].id == skillToUse.id:
                                            a.cooldowns[b] = skillToUse.cooldown

                        elif skillToUse.shareCooldown:
                            for ent in tablEntTeam[actTurn.team]:
                                for skillToSee in range(0,len(ent.char.skills)):
                                    if type(ent.char.skills[skillToSee]) == skill:
                                        if ent.char.skills[skillToSee].id in [trans.id, memAliceCast.id, renisurection.id]:
                                            ent.cooldowns[skillToSee] = max(ent.cooldowns[skillToSee],2)
                                        elif ent.char.skills[skillToSee].id == kikuRes.id:
                                            ent.cooldowns[skillToSee] = skillToUse.cooldown

                        if skillToUse.type in [TYPE_BOOST,TYPE_ARMOR,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ]:
                            if skillToUse.id != clemUltCast.id:
                                for b in ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES,directTarget=False):
                                    if skillToUse.id == chaosArmor.id:
                                        eff = copy.deepcopy(skillToUse.effect[0])
                                        eff.overhealth = random.randint(1,100)
                                        skillToUse.effect = [eff]
                                    for c in skillToUse.effect:
                                        effect = findEffect(c)
                                        tempTurnMsg += add_effect(actTurn,b,effect,danger=danger)
                                        logs += "\n{0} gave the {1} effect at {2} for {3} turn(s)".format(actTurn.char.name,effect.name,b.char.name,effect.turnInit)
                                    b.refreshEffects()

                            else:
                                effect = skillToUse.effect[0]
                                tempVal = max(actTurn.specialVars["clemBloodJauge"].value-1,30)
                                effect.overhealth = tempVal * len(team1)/9 * 3
                                tempTurnMsg += add_effect(actTurn,actTurn,effect,danger=danger)
                                logs += "\n{0} gave the {1} effect at {2} for {3} turn(s)".format(actTurn.char.name,effect.name,b.char.name,effect.turnInit)
                                b.refreshEffects()

                                actTurn.specialVars["clemBloodJauge"].value = 1
                                actTurn.specialVars["clemMemCast"] = True

                        elif skillToUse.type in [TYPE_INDIRECT_DAMAGE,TYPE_MALUS]:
                            for y in skillToUse.effect:
                                effect = findEffect(y)
                                areaTabl = ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENNEMIS,directTarget=False)
                                if effect.id == missiles.id and len(areaTabl) > 5:
                                    random.shuffle(areaTabl)
                                    areaTabl = areaTabl[:5]

                                for b in areaTabl:
                                    tempTurnMsg += add_effect(actTurn,b,effect)
                                    
                                    logs += "\n{0} gave the {1} effect at {2} for {3} turns".format(actTurn.char.name,effect.name,b.char.name,effect.turnInit)
                                b.refreshEffects()

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

                                if skillToUse.id not in ["yt","memAlice"]:                  # Any normal healing skill
                                    for a in ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES,directTarget=False):
                                        ballerine = actTurn.heal(a, skillToUse.emoji, skillToUse.use, skillToUse.power,danger=danger)
                                        tempTurnMsg += ballerine
                                        logs += ballerine
                                else:                                                       # Limitebreak Heal and Alice Memento
                                    for a in range(0,len(tablEntTeam[actTurn.team])):
                                        if tablEntTeam[actTurn.team][a].hp > 0:                     # On Living allies
                                            ballerine = actTurn.heal(tablEntTeam[actTurn.team][a], skillToUse.emoji, skillToUse.use, skillToUse.power,danger=danger)
                                            tempTurnMsg += ballerine
                                            logs += ballerine
                                        elif tablEntTeam[actTurn.team][a].status == STATUS_DEAD:    # Resurect
                                            healPowa = round(skillToUse.power * (1+(statUse-actTurn.negativeHeal)/120+(tablEntTeam[actTurn.team][a].endurance/1500))* actTurn.valueBoost(target = tablEntTeam[actTurn.team][a],heal=True)*actTurn.getElementalBonus(tablEntTeam[actTurn.team][a],area = AREA_MONO,type = TYPE_HEAL))
                                            healPowa = round(healPowa * (0.5+actTurn.char.level*0.01))
                                            ballerine = await actTurn.resurect(tablEntTeam[actTurn.team][a],healPowa,skillToUse.emoji,danger=danger)
                                            tempTurnMsg += ballerine
                                            logs += "\n{0} have been resurected.\n"+ballerine

                        elif skillToUse.type == TYPE_INVOC:
                            summoned = actTurn.summon(findInvoc(skillToUse.invocation),time,actTurn.cell.getCellForSummon(skillToUse.range,actTurn.team,findInvoc(skillToUse.invocation),actTurn),tablEntTeam,tablAliveInvoc)
                            tempTurnMsg += summoned["text"]+"\n"
                            logs += "\n"+summoned["text"]
                            time = summoned["timeline"]
                            tablEntTeam = summoned["tablEntTeam"]
                            tablAliveInvoc = summoned["tablAliveInvoc"]

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
                                    ballerine = ""
                                    sumPower = 0
                                    for b in a.effect:
                                        if b.effect.id == estal.id:
                                            sumPower += int(20*b.turnLeft)
                                            ballerine += b.decate(value=100)

                                    if sumPower > 0:
                                        a.refreshEffects()
                                        sumPower += 30
                                        ballerine += actTurn.attack(target=a,value = sumPower,icon = skillToUse.emoji,area=AREA_MONO,sussess=250,use=MAGIE)

                                        tempTurnMsg += ballerine
                                        logs += ballerine

                        elif skillToUse.type == TYPE_RESURECTION:
                            stat = skillToUse.use

                            for a in ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES,dead=True,directTarget=False):
                                if stat not in [PURCENTAGE,None]:
                                    if stat != HARMONIE:
                                        statUse = actTurn.allStats()[stat]
                                    else:
                                        temp = actTurn.allStats()
                                        for a in temp:
                                            statUse = max(a,statUse)

                                    healPowa = min(a.maxHp-a.hp,round(skillToUse.power * (1+(statUse-actTurn.negativeHeal)/120)* actTurn.valueBoost(target=a,heal=True)*actTurn.getElementalBonus(a,area=AREA_MONO,type=TYPE_HEAL)))

                                elif stat == PURCENTAGE:
                                    healPowa = round(a.maxHP * skillToUse.power/100 * (100-a.healResist)/100)

                                elif stat == None:
                                    healPowa = skillToUse.power

                                ballerine = await actTurn.resurect(a,healPowa,skillToUse.emoji,danger=danger)
                                tempTurnMsg += ballerine
                                logs += ballerine

                        else: # Damage
                            power = skillToUse.power

                            if skillToUse.id == lunaSpe.id:
                                for ent in range(len(tablEntTeam[actTurn.team])):
                                    if tablEntTeam[actTurn.team][ent].char.name == "Conviction des Ténèbres" and type(tablEntTeam[actTurn.team][ent].char) == invoc:
                                        tablEntTeam[actTurn.team][ent].hp = 0
                                        tablEntTeam[actTurn.team][ent].cell.on = None
                                        power += lunaSpe.power

                            elif skillToUse.id == memClemCastSkill.id:
                                effect = classes.effect("Bouclier vampirique","clemMemSkillShield",overhealth=(actTurn.hp-1)//2,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji('<:clemMemento2:902222663806775428>'),absolutShield=True)
                                tempTurnMsg += "{0} : - {1} PV\n".format(actTurn.icon,actTurn.hp-1)
                                actTurn.hp = 1
                                actTurn.maxHp, actTurn.healResist = actTurn.maxHp//2,actTurn.healResist//2
                                tempTurnMsg += add_effect(actTurn,actTurn,effect,ignoreEndurance=True)
                                defIncur50 = copy.deepcopy(incur[5])
                                defIncur50.turnInit, defIncur50.unclearable = -1,True
                                tempTurnMsg += add_effect(actTurn,actTurn,defIncur50)

                            elif skillToUse.id == memAlice.id:
                                actPurcentHp, actActuHp = actTurn.hp/actTurn.maxHp, actTurn.hp
                                actTurn.maxHp = int(actTurn.maxHp * 0.75)
                                actTurn.hp = int(actTurn.maxHp*actPurcentHp)
                                if actActuHp - actTurn.hp != 0:
                                    tempTurnMsg += "{0} : - {1} PV\n".format(actTurn.icon,actActuHp - actTurn.hp)

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

                            cmpt = 0
                            while cmpt < skillToUse.repetition:
                                ballerine = actTurn.attack(target=ennemi,value=power,icon=skillToUse.emoji,area=skillToUse.area,sussess=skillToUse.sussess,use=skillToUse.use,onArmor=skillToUse.onArmor)
                                tempTurnMsg += ballerine
                                logs += "\n"+ballerine
                                cmpt += 1
                                if cmpt < skillToUse.repetition:
                                    tempTurnMsg += "\n"

                            if skillToUse.effect!=[None]:
                                for a in skillToUse.effect:
                                    effect = findEffect(a)
                                    tempTurnMsg += add_effect(actTurn,ennemi,effect)
                                    
                                    logs += "\n{0} gave the {1} effect at {2} for {3} turn(s)".format(actTurn.char.name,effect.name,ennemi.char.name,effect.turnInit)

                            if skillToUse.id == lunaSpe4.id:
                                tablCellsEmpty = []
                                for cell in tablAllCells:
                                    if cell.on == None and [cell.x,cell.y] not in [[5,0],[5,1],[5,3],[5,4],[4,0],[4,4]]:
                                        tablCellsEmpty.append(cell)

                                lenSummon = 0
                                while lenSummon < len(team1)-1:
                                    celli = tablCellsEmpty[random.randint(0,len(tablCellsEmpty)-1)]
                                    tablCellsEmpty.remove(celli)
                                    summoned = actTurn.summon(findInvoc("Conviction des Ténèbres"),time,celli,tablEntTeam,tablAliveInvoc,ignoreLimite=True)
                                    tempTurnMsg += summoned["text"]+"\n"
                                    logs += "\n"+summoned["text"]
                                    time = summoned["timeline"]
                                    tablEntTeam = summoned["tablEntTeam"]
                                    tablAliveInvoc = summoned["tablAliveInvoc"]
                                    lenSummon += 1

                            if skillToUse.power > 0 and actTurn.specialVars["damageSlot"] != None:
                                loose = int(actTurn.maxHp * (actTurn.specialVars["damageSlot"].effect.power/100))
                                tempTurnMsg += "{0} : -{1} PV ({2})\n".format(actTurn.icon,loose,actTurn.specialVars["damageSlot"].effect.name)
                                actTurn.hp -= loose
                                if actTurn.hp <= 0:
                                    tempTurnMsg += actTurn.death(killer=actTurn)


                                actTurn.refreshEffects()

                        if skillToUse.effectOnSelf != None:
                            eff = findEffect(skillToUse.effectOnSelf)
                            if eff.replica != None:
                                eff.replicaTarget = ennemi
                                if actTurn.char.aspiration == MAGE:
                                    tempTurnMsg += add_effect(actTurn,actTurn,classes.effect("Mage","effMage",None,turnInit=2,magie=actTurn.baseStats[MAGIE]*0.15,unclearable=True,emoji=uniqueEmoji(aspiEmoji[MAGE])))


                            tempTurnMsg += add_effect(actTurn,actTurn,findEffect(skillToUse.effectOnSelf))
                            
                            actTurn.refreshEffects()

                        if skillToUse.id == memAlice2.id:
                            aliceMemCastTabl[actTurn.team] = True
                        elif skillToUse.id == memAlice.id:
                            aliceMemCastTabl[actTurn.team] = True
                        elif skillToUse.id == strengthOfWill.id and actTurn.isNpc("Félicité") and dictIsPnjVar["Clémence"]:
                            tempTurnMsg += "<:felicite:909048027644317706> : *\"Alors Clémence :D ? Combien combien ?\"*\n<:clemence:908902579554111549> : *\"Hum... {0} sur 20\"*\n<:felicite:909048027644317706> : :D\n"
                        if actTurn.isNpc("Clémence pos.") or actTurn.isNpc("Alice Exaltée"):
                            for skillID, cost in clemBJcost.items():
                                if skillToUse.id == skillID:
                                    actTurn.specialVars["clemBloodJauge"].value = max(0,actTurn.specialVars["clemBloodJauge"].value - cost)
                                    if actTurn.specialVars["clemBloodJauge"].value == 0:
                                        tempTurnMsg += "\nLa Jauge de Sang se brise !\n"
                                        if actTurn.isNpc("Clémence pos."):
                                            tempTurnMsg += add_effect(actTurn, actTurn, clemStunEffect)
                                        else:
                                            tempTurnMsg += add_effect(actTurn, actTurn, aliceStunEffect)
                                        
                                        loose = actTurn.maxHp // 10
                                        tempTurnMsg += "{0} : -{1} PV\n".format(actTurn.icon,loose)
                                        actTurn.hp -= loose
                                        if actTurn.hp <= 0:
                                            tempTurnMsg += actTurn.death(killer=actTurn)

                                        actTurn.refreshEffects()
                                    break

                else:                                   # The entity is, in fact, stun
                    tempTurnMsg += f"\n{actTurn.char.name} est étourdi{actTurn.accord()} !\n"

                ballerine = "\n__Fin du tour__\n"+actTurn.endOfTurn(danger)
                logs += ballerine
                tempTurnMsg += ballerine
                timeNow = (datetime.datetime.now() - nowStartOfTurn)/datetime.timedelta(microseconds=1000)
                logs += "Turn duration : {0} ms{1}\n".format(timeNow,[" (Manual fighter)",""][int(actTurn.auto)])
                if timeNow > 500 and actTurn.auto:
                    longTurn = True
                    longTurnNumber.append({"turn":tour,"ent":actTurn.char.name,"duration":timeNow})
                if not(auto) and not(actTurn.char.name == "Conviction des Ténèbres" and type(actTurn.char) == invoc):   # Sending the Turn message
                    if len(tempTurnMsg) > 4096:
                        tempTurnMsg = unemoji(tempTurnMsg)
                        if len(tempTurnMsg) > 4096:
                            tempTurnMsg = "OVERLOAD"
                    await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color))
                    if type(actTurn.char) != invoc:
                        await asyncio.sleep(2+(len(tempTurnMsg)/1500*5))
                    else:
                        await asyncio.sleep(2+(len(tempTurnMsg)/2500*5))

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
        logs += "\n\n=================\nEnd of the fight"
    except:
        team = team1[0].team
        teamWinDB.changeFighting(team,False)
        logs += "\n"+format_exc()
        date = datetime.datetime.now()+horaire
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

        try:
            await ctx.send("Une erreur est survenue durant le combat",file=discord.File(fp=opened))
        except:
            await ctx.channel.send("Une erreur est survenue durant le combat",file=discord.File(fp=opened))
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
                tablEntTeam[0][a].char = loadCharFile(absPath + "/userProfile/" + str(tablEntTeam[0][a].char.owner) + ".prof",ctx)

        for a in range(0,len(tablEntTeam[1])):      # Reload the char files (in case of changes)
            if type(tablEntTeam[1][a].char) == char:
                tablEntTeam[1][a].char = loadCharFile(absPath + "/userProfile/" + str(tablEntTeam[1][a].char.owner) + ".prof",ctx)

        winners = int(not(everyoneDead[1]))         # The winning team. 0 -> Blue, 1 -> Red

        if not(octogone and type(team2[0])==tmpAllie and team2[0].name=='Lena' and len(team2) == 1 and not(winners)):               # None Special fights
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
            shieldClass = sorted(temp,key=lambda student: student.stats.shieldGived,reverse=True)
            for a in shieldClass[:]:
                if a.stats.shieldGived < 1:
                    shieldClass.remove(a)
            suppClass = sorted(temp,key=lambda student: student.stats.damageBoosted + student.stats.damageDogded,reverse=True)
            for a in suppClass[:]:
                if a.stats.damageBoosted + a.stats.damageDogded < 1:
                    suppClass.remove(a)

            listClassement = [dptClass,healClass,shieldClass,suppClass]

            if not(octogone):
                teamWinDB.addResultToStreak(team1[0],everyoneDead[1])
                team = team1[0].team
                if team == 0:
                    team = team1[0].owner
                if isLenapy:
                    teamWinDB.refreshFightCooldown(team,auto)

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
                            tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redWinAlive)]
                            tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redWinAlive)]
                            tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redWinAlive)]
                            tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redWinAlive)]
                            tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redWinAlive)]
                            tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redWinAlive)]
                        elif a == 1 and not(winners) and b.char.says.redLoose != None:
                            tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redLoose)]
                            tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redLoose)]
                            tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redLoose)]
                            tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redLoose)]
                    else:
                        if a == 0 and not(winners) and b.char.says.blueWinAlive != None and b.hp > 0:
                            tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.blueWinAlive)]
                            tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.blueWinAlive)]
                        elif a == 0 and not(winners) and b.char.says.blueWinDead != None and b.hp <= 0:
                            tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.blueWinDead)]
                        elif a == 0 and winners and b.char.says.blueLoose != None:
                            tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.blueLoose)]
                        elif a == 1 and winners and b.char.says.redWinAlive != None and b.hp > 0:
                            tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redWinAlive)]
                            tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redWinAlive)]
                        elif a == 1 and winners and b.char.says.redWinDead != None and b.hp <= 0:
                            tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redWinDead)]
                        elif a == 1 and not(winners) and b.char.says.redLoose != None:
                            tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redLoose)]
            
                if len(temp[a]) > 1024:
                    temp[a] = unemoji(temp[a])
            say = ""
            if len(tablSays) > 1:
                say = "\n\n{0}".format(tablSays[random.randint(0,len(tablSays)-1)])
            elif len(tablSays) == 1:
                say = "\n\n{0}".format(tablSays[0])
    
            duree = datetime.datetime.now()
            now = duree - now
            now = str(now.seconds//60) + ":" + str(now.seconds%60)
            temp1 = discord.Embed(title = "__Résultats du combat :__",color = [0x2996E5,red][winners],description="__Danger :__ {0}\n__Nombre de tours :__ {1}\n__Durée :__ {2}{3}".format(danger,tour,now,say))
            temp1.add_field(name="<:empty:866459463568850954>\n__Vainqueurs :__",value=temp[winners],inline=True)
            temp1.add_field(name="<:empty:866459463568850954>\nPerdants :",value=temp[not(winners)],inline=True)

            if longTurn:
                temp1.set_footer(text="{0} tour{1} anormalement long{1} {2} été détecté{1} durant le combat. Un rapport va être envoyé".format(len(longTurnNumber),["",'s'][int(len(longTurnNumber) > 1)],["a","ont"][int(len(longTurnNumber) > 1)]))
            
            if not(octogone):
                gainExp, gainCoins, allOcta,gainMsg = 0,tour*20,True,""
                for a in tablEntTeam[1]:
                    if type(a.char) == octarien:
                        gainExp += a.char.exp
                    elif type(a.char) == tmpAllie:
                        gainExp += 5
                    else:
                        allOcta = False

                truc = 0
                logs += "\n\n"
                try:
                    if winStreak > 7:
                        truc = (winStreak-7) * 0.05
                except:
                    pass

                multiStr,multi = "",max(1,8/len(team1)+truc)
                if multi > 1:
                    multiStr = f" *(bonus exp : + {int(multi*100-100)}%)*"

                gainInit = str(gainExp)
                gainExp = int(gainExp*multi)
                if winners:
                    gainInit = str(int(gainInit)//2)
                    gainExp = gainExp//2
                    gainCoins = gainCoins//2

                logs += "Gains exp : {0} ({1} * {2})\n".format(gainExp,gainInit,multi)
                gainMsg = f"Points d'expériences : {gainInit}{multiStr}\nPièces : {gainCoins}\n"

                for a in tablEntTeam[0]: #Attribution de l'exp et loot
                    if type(a.char) == char:
                        path = absPath + "/userProfile/" + str(a.char.owner) + ".prof"
                        temp = a.char
                        a.char = await addExpUser(bot,guild,path,ctx,exp=gainExp+(a.medals[0]*3)+(a.medals[1]*2)+(a.medals[2]*1),coins=gainCoins)
                        if a.char == None:
                            temp.exp += gainExp+(a.medals[0]*3)+(a.medals[1]*2)+(a.medals[2]*1)
                            temp.currencies += gainCoins
                            a.char = temp

                        if random.randint(0,99) < [20,33][int(userShopPurcent(a.char)<90)] and allOcta and not(winners):
                            logs += "\n{0} a réusi son jet :".format(a.char.name)
                            drop = listAllBuyableShop[:]
                            temp = drop[:]
                            
                            for b in drop:
                                if a.char.have(obj=b):
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
                                gainMsg += f"{await getUserIcon(bot,a.char)} → {rand.emoji} {rand.name}\n"

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
                                gainMsg += f"{await getUserIcon(bot,a.char)} → {gain} <:coins:862425847523704832>\n"

                temp1.add_field(name="<:empty:866459463568850954>\n__Gains de l'équipe joueur :__",value = gainMsg,inline=False)
        else:
            logs += mauvaisePerdante
            team = team1[0].team
            teamWinDB.changeFighting(team,False)
            logs += "\n"+format_exc()
            date = datetime.datetime.now()
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
                await msg.edit(embed = temp1,components=[create_actionrow(create_button(ButtonStyle.grey,"Chargement...",getEmojiObject('<a:loading:862459118912667678>'),"📄",disabled=True))])
            else:
                await msg.edit(embed = temp1,components=[])
            if not(octogone):
                teamWinDB.changeFighting(team,False)
        # ------------ Succès -------------- #
        if not(octogone):
            for a in [0,1]:
                for b in tablEntTeam[a]:
                    if type(b.char) == char:
                        achivements = achivement.getSuccess(b.char)
                        if not(b.auto): # Ivresse du combat
                            b.char = await achivements.addCount(ctx,b.char,"fight")

                        if dictIsPnjVar["Alice"]: # Souvenez vous que chaque roses a des épines
                            b.char = await achivements.addCount(ctx,b.char,"alice")
                        if dictIsPnjVar["Clémence"]: # La quête de la nuit
                            b.char = await achivements.addCount(ctx,b.char,"clemence")
                        if dictIsPnjVar["Akira"]: # Seconde impression
                            b.char = await achivements.addCount(ctx,b.char,"akira")
                        if dictIsPnjVar["Gwendoline"]: # Une histoire de vangeance
                            b.char = await achivements.addCount(ctx,b.char,"gwen")
                        if dictIsPnjVar["Hélène"]: # Là où mes ailes me porteront
                            b.char = await achivements.addCount(ctx,b.char,"helene")
                        if dictIsPnjVar["Icealia"]: # Prévoir l'imprévisible
                            b.char = await achivements.addCount(ctx,b.char,"icea")
                        if dictIsPnjVar["Shehisa"]: # Pas vue, pas prise
                            b.char = await achivements.addCount(ctx,b.char,"sram")
                        if dictIsPnjVar["Powehi"]: # La fin de tout, et renouvellement
                            b.char = await achivements.addCount(ctx,b.char,"powehi")
                        if dictIsPnjVar["Félicité"]:
                            b.char = await achivements.addCount(ctx,b.char,"feli")
                        if dictIsPnjVar["Sixtine"]:
                            b.char = await achivements.addCount(ctx,b.char,"sixtine")
                        if dictIsPnjVar["Hina"]:
                            b.char = await achivements.addCount(ctx,b.char,"hina")
                        if dictIsPnjVar["Julie"]:
                            b.char = await achivements.addCount(ctx,b.char,"julie")
                        if tablEntTeam[1][0].isNpc("Luna") and type(tablEntTeam[1][0].char) == octarien:
                            b.char = await achivements.addCount(ctx,b.char,"luna")
                        if tablEntTeam[1][0].isNpc("Clémence pos."):
                            b.char = await achivements.addCount(ctx,b.char,"clemMem")
                        if dictIsPnjVar["Krys"]:
                            b.char = await achivements.addCount(ctx,b.char,"krys")

                        if auto and int(ctx.author.id) == int(b.char.owner): # Le temps c'est de l'argent
                            b.char = await achivements.addCount(ctx,b.char,"quickFight")

                        # Je ne veux pas d'écolière pour défendre nos terres
                        b.char = await achivements.addCount(ctx,b.char,"school")

                        # Elementaire
                        if b.char.level >= 10:
                            b.char = await achivements.addCount(ctx,b.char,"elemental")

                        # Dimentio
                        if b.char.level >= 20:
                            b.char = await achivements.addCount(ctx,b.char,"dimentio")

                        # Soigneur de compette
                        b.char = await achivements.addCount(ctx,b.char,"greatHeal",b.stats.heals)

                        # Situation désespérée
                        if b.char.aspiration not in [ALTRUISTE,PREVOYANT,IDOLE,PROTECTEUR]:
                            b.char = await achivements.addCount(ctx,b.char,"notHealBut",b.stats.heals)

                        # La meilleure défense c'est l'attaque
                        b.char = await achivements.addCount(ctx,b.char,"greatDps",b.stats.damageDeal-b.stats.indirectDamageDeal)

                        # Notre pire ennemi c'est nous même
                        b.char = await achivements.addCount(ctx,b.char,"poison",b.stats.indirectDamageDeal)

                        # Savoir utiliser ses atouts
                        b.char = await achivements.addCount(ctx,b.char,"estialba",int(b.stats.estialba))

                        # Il faut que ça sorte
                        b.char = await achivements.addCount(ctx,b.char,"lesath",int(b.stats.bleeding))

                        aliceStatsDb.addStats(b.char,b.stats)

                        saveCharFile(absPath + "/userProfile/"+str(b.char.owner)+".prof",b.char)

        timeout = False
        date = datetime.datetime.now()+horaire
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

        if alicePing:
            chan = await bot.fetch_channel(808394788126064680)
            opened = open("./data/fightLogs/{0}_{1}.txt".format(ctx.author.name,date),"rb")
            await chan.send("Hé <@!213027252953284609> ! Elle l'a dit !",file=discord.File(fp=opened))
            opened.close()

        actuTeam = 0
        actuEntity = 0
        started = False
        prec = None
        logsAff = False

        def check(m):
            return m.origin_message.id == msg.id

        logsButton = create_button(ButtonStyle.grey,"Voir les logs","📄","📄")
        startMsg = globalVar.getRestartMsg()
        startMsg = startMsg == 0

        if longTurn:
            team = team1[0].team
            teamWinDB.changeFighting(team,False)
            logs += "\n"+format_exc()
            date = datetime.datetime.now()+horaire
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

        while startMsg: # Tableau des statistiques
            options = []
            for team in [0,1]:
                for num in range(len(tablEntTeam[team])):
                    ent = tablEntTeam[team][num]
                    options.append(create_select_option(ent.name,"{0}:{1}".format(team,num),getEmojiObject(await ent.getIcon(bot)),default=started and team == actuTeam and num == actuEntity))

            select = create_select(options,placeholder="Voir les statistiques d'un combattant")
            await msg.edit(embed = temp1, components=[create_actionrow(select),create_actionrow(logsButton)])

            try:
                interact = await wait_for_component(bot,msg,check=check,timeout=60)
            except:
                if logsAff:
                    await msg.edit(embed = temp1, components=[create_actionrow(logsButton)])
                else:
                    await msg.edit(embed = temp1, components=[])
                if prec != None:
                    await prec.delete()
                break

            try:
                inter = interact.values[0]
                actuTeam,actuEntity = int(inter[0]),int(inter[-1])
                actu = tablEntTeam[actuTeam][actuEntity]
                stats = actu.stats

                if type(actu.char) == char:
                    userIcon = await getUserIcon(bot,actu.char)
                else:
                    userIcon = actu.char.icon

                if type(actu.char) in [char,tmpAllie] or actu.isNpc("Octaling"):
                    descri = f"{actu.char.weapon.emoji}"

                    if not(actu.isNpc("Octaling")):
                        descri += f" | {actu.char.stuff[0].emoji} {actu.char.stuff[1].emoji} {actu.char.stuff[2].emoji}"

                    skillTmp = ""
                    for a in actu.char.skills:
                        if type(a) == skill:
                            if skillTmp == "":
                                skillTmp = " |"
                            skillTmp += " {0}".format(a.emoji)
                    
                    descri+=skillTmp
                    statsEm = discord.Embed(title = "__Statistiques de "+ userIcon +" "+actu.char.name+"__",color=actu.char.color,description=descri)
                else:
                    statsEm = discord.Embed(title = "__Statistiques de "+ userIcon +" "+actu.char.name+"__",color=actu.char.color)
    
                ballerine =[[stats.ennemiKill,stats.damageDeal,stats.indirectDamageDeal,stats.underBoost,stats.damageOnShield],[stats.allieResurected,stats.heals,stats.damageBoosted,stats.damageDogded,stats.shieldGived],[stats.survival,stats.damageRecived,round(stats.shootHited/stats.totalNumberShot*100),round(stats.dodge/stats.numberAttacked*100),round(stats.crits/stats.totalNumberShot*100)]]
                babie = [["Ennemis tués :","Dégâts infligés :","→ Dont indirects :","→ Dont Boostés :","Dégâts sur armure :"],["Alliés ressucités :","Soins effectués :","Dégâts Boostés :","Dégâts réduits :","Armure fournie :"],["Tours survécus :","Dégâts reçus :","Taux de précision : ","Taux d'esquive :","Taux de coup critique :"]]
                sneaker = ["__Stats offensives__","__Stats altruistes__","__Stats personnels__"]
                for a in [0,1,2]:
                    statMsg = ""
                    for b in range(0,len(ballerine[a])):
                        temp = "**"
                        purcent = ""
                        if babie[a][b].startswith("Taux"):
                            purcent = " %"
                        if ballerine[a][b] == 0:
                            temp =""
                        statMsg += f"\n{babie[a][b]} {temp}{str(ballerine[a][b])}{temp}{purcent}"
                    statsEm.add_field(name="<:empty:866459463568850954>\n"+sneaker[a],value=statMsg,inline = False)
                
                if prec != None:
                    await prec.edit(embed = statsEm)
                else:
                    prec = await interact.send(embed = statsEm)
                started = True
            except:
                opened = open("./data/fightLogs/{0}_{1}.txt".format(ctx.author.name,date),"rb")
                logsMsg = await interact.send("`Logs, {0} à {1}:{2}`".format(ctx.author.name,date[0:2],date[-2:]),file=discord.File(fp=opened))
                if not(isLenapy):
                    print(logs)
                opened.close()
                logsButton = create_button(ButtonStyle.URL,"Voir les logs","📄",url=logsMsg.jump_url)
                logsAff = True