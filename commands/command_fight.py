from typing import Type
from asyncio.locks import Condition
import discord, random, gestion, os, emoji, pathlib, neutral,asyncio,datetime,time,traceback,copy
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from discord.ext import commands, tasks
from commands.sussess_endler import *
from traceback import format_exc

teamWinDB = dbHandler("teamVic.db")

async def loadingEmbed(ctx):
    return await ctx.channel.send(embed = discord.Embed(title = commandArgs(ctx)[0], description = emoji.loading))
async def loadingSlashEmbed(ctx):
    return await ctx.channel.send(embed = discord.Embed(title = "slash_command", description = emoji.loading))

AI_DPT,AI_BOOST,AI_MALUS,AI_AVENTURE,AI_ALTRUISTE,AI_OFFERUDIT = 0,1,2,3,4,5

async def fight(bot,team1,team2,ctx,guild,auto = True,contexte=[],octogone=False,slash=False):
    now = datetime.datetime.now()
    logs,haveError = "[{0}]\n".format(now.strftime("%H:%M:%S, %D/%m/%Y")),False
    try:
        print(ctx.author.name + " a lancé un combat")
    except:
        pass
    cmpt,tablAllCells,tour,sleepTime,danger,dangerThub,tablAliveInvoc = 0,[],0,0.7,None,None,[0,0]

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
                        if area == AREA_ALL_ALLIES and b.on.team == team:
                            rep+=[b]
                        elif area == AREA_ALL_ENNEMIES and b.on.team != team:
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
    
        def getEntityOnArea(self,area=AREA_MONO,team=0,wanted=ALLIES,lineOfSight=False,lifeUnderPurcentage=100,dead=False,effect=[None],ignoreInvoc = False):
            rep = []
            if type(effect)!=list:
                effect = [effect]

            tablArea = self.getArea(area=area,team=team)
            enties = []
            for a in tablArea:
                if a.on != None:
                    if a.on.hp > 0 and not(dead):
                        if a.on.team == team and wanted == ALLIES:
                            enties += [a.on]
                        elif a.on.team != team and wanted == ENNEMIS:
                            enties += [a.on]
                        elif wanted == ALL:
                            enties += [a.on]
                    elif a.on.hp <= 0 and dead:
                        if a.on.team == team and wanted == ALLIES:
                            enties += [a.on]
                        elif a.on.team != team and wanted == ENNEMIS:
                            enties += [a.on]
                        elif wanted == ALL:
                            enties += [a.on]
            
            rep = enties

            if lineOfSight and wanted==ENNEMIS and (area not in [AREA_ALL_ENNEMIES,AREA_ALL_ENTITES]):
                for a in enties:
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
                            if a.on.team == team and wanted == ALLIES:
                                enties += [a.on]
                            elif a.on.team != team and wanted == ENNEMIS:
                                enties += [a.on]
                            elif wanted == ALL:
                                enties += [a.on]
                        elif a.on.hp <= 0 and dead:
                            if a.on.team == team and wanted == ALLIES:
                                enties += [a.on]
                            elif a.on.team != team and wanted == ENNEMIS:
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

            return rep

        def getVisibleArea(self,area=AREA_MONO,team=0,wanted=ALLIES,lineOfSight=False):
            tablArea = self.getArea(area=area,team=team)
            enties = []
            for a in tablArea:
                if a.on != None:
                    if a.on.status == STATUS_ALIVE or a.on.status == STATUS_RESURECTED:
                        if a.on.team == team and wanted == ALLIES:
                            enties += [a.on]
                        elif a.on.team != team and wanted == ENNEMIS:
                            enties += [a.on]
        
            if lineOfSight:
                for a in enties:
                    # Définition de la direction
                    direction, diffX, diffY = None,self.x - a.cell.x,self.y - a.cell.y

                    if diffX <= 0:
                        if abs(diffY/3) < abs(diffX):
                            direction = '➡️'
                        elif abs(diffX/3) < abs(diffY):
                            if diffY > 0:
                                direction = '⬆️'
                            else:
                                direction = '⬇️'

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
                        elif abs(diffX/3) < abs(diffY):
                            if diffY > 0:
                                direction = '⬆️'
                            else:
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
                        while cmpt > 0:
                            for b in temp:
                                try:
                                    tablArea.remove(findCell(cmpt,yOr+b))
                                except:
                                    pass

                            cmpt += 1
                            ite += 1
                            temp += [ite,-ite]
            return tablArea

        def getEmptyCellsInArea(self,area,team):
            tabl = []
            cells = self.getArea(area,team)

            for a in cells:
                if a.on == None:
                    tabl.append(a)

            return tabl

        def getCellForSummon(self,area,team,summon,summoner):
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

    for a in [0,1,2,3,4,5]:
        for b in [0,1,2,3,4]:
            tablAllCells += [cell(a,b,cmpt)]
            cmpt += 1

    def findCell(x,y):
        cmpt = 0
        while cmpt < 30:
            if tablAllCells[cmpt].x == x and tablAllCells[cmpt].y == y:
                return tablAllCells[cmpt]
            cmpt += 1
    
    if not(auto) and not(slash):
        await ctx.add_reaction(emoji.loading)
    allEffectInFight,turnMsgTemp = [],""
    supprEffect,addEffect,tablEntTeam = [],[],[]

    class entity:
        """Classe des entités du combat. Se base sur un class Char"""
        def __init__(self,identifiant,perso,team,player=True,auto=True,danger=100,summoner=None):
            """id : id de l'entity (int)
            char : char de base de l'entité (char ou octarien)
            team : équipe de l'entité (int)
            type : Type de l'entité (const)
            auto : si l'entité est en mode automatique ou non (bool)"""
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
            
            if type(perso) != invoc:
                baseHP,HPparLevel = 100,8
                temp = perso.endurance
                for a in [perso.weapon,perso.stuff[0],perso.stuff[1],perso.stuff[2]]:
                    temp += a.endurance

            else:
                baseHP,HPparLevel = 50,5
                perso.level = summoner.char.level
                temp = 0
                if perso.endurance[0] == PURCENTAGE:
                    temp = int(summoner.char.endurance * perso.endurance[1])

            self.effect = []
            self.ownEffect = []
            self.cell = tablAllCells[0]
            self.hp = round((baseHP+perso.level*HPparLevel)*((temp)/100+1))
            self.maxHp = round((baseHP+perso.level*HPparLevel)*((temp)/100+1))

            if type(self.char) == octarien:
                self.hp = round(self.hp * danger / 100)
                self.maxHp = round(self.maxHp * danger / 100)

            self.strength,self.endurance,self.persoisma,self.agility,self.precision,self.intelligence = 0,0,0,0,0,0
            self.resistance,self.percing,self.critical = 0,0,0
            self.ressurectable = False
            cooldowns = [0,0,0,0,0]

            for a in [0,1,2,3,4]:
                if type(self.char.skills[a]) == skill:
                    if self.char.skills[a].id == trans.id:
                        temp = copy.deepcopy(self.char.skills[a])
                        temp.use = HARMONIE
                        if self.char.aspiration in [BERSERK,TETE_BRULE,POIDS_PLUME,ERUDIT,OBSERVATEUR]:
                            temp.type = TYPE_DAMAGE
                            if self.char.aspiration == BERSERK:
                                temp.power = 160
                            elif self.char.aspiration in [TETE_BRULE,POIDS_PLUME,ERUDIT,OBSERVATEUR]:
                                temp.power = 150
                                if self.char.aspiration in [TETE_BRULE,POIDS_PLUME]:
                                    temp.area = AREA_LINE_6
                                    temp.range = AREA_MONO
                                elif self.char.aspiration in [ERUDIT,OBSERVATEUR]:
                                    temp.area = AREA_CIRCLE_2
                        elif self.char.aspiration in [ALTRUISTE,IDOLE]:
                            temp.type = TYPE_HEAL
                            temp.area = AREA_ALL_ALLIES
                            temp.range = AREA_MONO
                            temp.power = 70
                        elif self.char.aspiration == AVENTURIER:
                            temp.type = TYPE_INVOC
                            temp.invocation = "Titania"

                        self.char.skills[a] = temp                 
                    cooldowns[a] = int(self.char.skills[a].ultimate)*2+self.char.skills[a].initCooldown

            self.cooldowns = cooldowns
            self.stats = statTabl()
            self.medals = [0,0,0]
            self.healResist = 0
            self.missedLastTurn = False

            finded = False
            self.IA = AI_AVENTURE

            if self.char.aspiration in [BERSERK,OBSERVATEUR,POIDS_PLUME,TETE_BRULE]:
                self.IA = AI_DPT

            elif self.char.aspiration == IDOLE:
                self.IA = AI_BOOST

            elif self.char.aspiration == ALTRUISTE:
                self.IA = AI_ALTRUISTE

            elif ERUDIT == self.char.aspiration:
                offSkill,SuppSkill = 0,0
                for b in [self.char.weapon]+self.char.skills:
                    if type(b) in [weapon,skill]:
                        if b.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]:
                            offSkill += 1
                        else:
                            SuppSkill += 1
                    
                if SuppSkill >= offSkill:
                    self.IA = AI_MALUS
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

        def allStats(self):
            return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence]

        def tetedepioche(self):
            if self.char.aspiration == 5:
                return [1.2,0.8]
            else:
                return [1,1]

        def move(self,x=0,y=0):
            """Déplace l'entié sur la cellule correspondant aux coordonnés donnés"""
            temp = self.cell
            temp2 = findCell(x,y)
            self.cell = temp2
            temp.on = None
            temp2.on = self

        def valueBoost(self,target = 0,heal=False):
            """Renvoie la valeur d'un boost reçu."""
            if self.char.aspiration == ALTRUISTE:
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

            elif self.char.aspiration == IDOLE:
                alice = 0
                for a in tablEntTeam[self.team]:
                    if a.hp > 0:
                        alice += 1

                if not(heal):
                    return 0.9 + alice*0.05
                else:
                    return 0.8 + alice*0.025

            elif self.char.aspiration == ERUDIT:
                return 1.1
            else:
                return 1

        def berserked(self):
            """Renvoie le boost de dégâts des Berserks"""
            if self.char.aspiration == BERSERK:
                return round(0.35*(1-self.hp/self.maxHp),2)
            else:
                return 0

        def effectIcons(self):
            """Renvoie un str contenant les icones, les noms et la valeur ou tour restant des effets de l'entité"""
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

                    else:
                        temp += f"{a.icon} {a.effect.name}\n"
            else:
                temp = "Pas d'effet sur la cible"

            return temp

        def recalculate(self):
            """Méthode qui recalcule les statistiques de l'entité en prenant en compte les effets"""
            sumStatsBonus = [0,0,0,0,0,0,0,0,0]
            stuned = False

            if type(self.char) != invoc:
                for a in [self.char.weapon,self.char.stuff[0],self.char.stuff[1],self.char.stuff[2]]:
                    valueElem = 1
                    if a.affinity == self.char.element :
                        valueElem = 1.1
                    
                    sumStatsBonus[0] += int(a.strength*valueElem)
                    sumStatsBonus[1] += int(a.endurance*valueElem)
                    sumStatsBonus[2] += int(a.charisma*valueElem)
                    sumStatsBonus[3] += int(a.agility*valueElem)
                    sumStatsBonus[4] += int(a.precision*valueElem)
                    sumStatsBonus[5] += int(a.intelligence*valueElem)
                    sumStatsBonus[6] += int(a.resistance*valueElem)
                    sumStatsBonus[7] += int(a.percing*valueElem)
                    sumStatsBonus[8] += int(a.critical*valueElem)
            else:
                temp = self.char.allStats()+[self.char.resistance,self.char.percing,self.char.critical]
                temp2 = self.summoner.allStats()+[self.summoner.resistance,self.summoner.percing,self.summoner.critical]
                adv = 1
                if self.summoner.char.aspiration == AVENTURIER:
                    adv = 1.2
                for a in range(0,len(temp)):
                    if type(temp[a]) == list:
                        if temp[a][0] == PURCENTAGE:
                            sumStatsBonus[a] += int(temp2[a]*temp[a][1]*adv)
                        elif temp[a][0] == HARMONIE:
                            harmonie = 0
                            for b in temp2:
                                harmonie = max(harmonie,b)
                            sumStatsBonus[a] += harmonie*adv
                    else:
                        sumStatsBonus[a] = temp[a]

            for a in self.effect:
                if a.effect.stat != None:
                    temp = a.caster.allStats()[a.effect.stat]
                    sumStatsBonus[0] += a.effect.strength * a.value * (temp+100)/100
                    sumStatsBonus[1] += a.effect.endurance * a.value * (temp+100)/100
                    sumStatsBonus[2] += a.effect.charisma * a.value * (temp+100)/100
                    sumStatsBonus[3] += a.effect.agility* a.value * (temp+100)/100
                    sumStatsBonus[4] += a.effect.precision* a.value * (temp+100)/100
                    sumStatsBonus[5] += a.effect.intelligence* a.value * (temp+100)/100
                    sumStatsBonus[6] += a.effect.resistance* a.value * (temp+100)/100
                    sumStatsBonus[7] += a.effect.percing* a.value * (temp+100)/100
                    sumStatsBonus[8] += a.effect.critical* a.value * (temp+100)/100

                else:
                    sumStatsBonus[0] += a.effect.strength 
                    sumStatsBonus[1] += a.effect.endurance 
                    sumStatsBonus[2] += a.effect.charisma
                    sumStatsBonus[3] += a.effect.agility
                    sumStatsBonus[4] += a.effect.precision
                    sumStatsBonus[5] += a.effect.intelligence
                    sumStatsBonus[6] += a.effect.resistance
                    sumStatsBonus[7] += a.effect.percing
                    sumStatsBonus[8] += a.effect.critical
                
                if a.stun == True:
                    stuned = True

            if self.char.element == ELEMENT_FIRE:
                sumStatsBonus[7] += 5
            elif self.char.element == ELEMENT_WATER:
                sumStatsBonus[PRECISION] += 10
            elif self.char.element == ELEMENT_AIR:
                sumStatsBonus[AGILITY] += 10
            elif self.char.element == ELEMENT_EARTH:
                sumStatsBonus[6] += 5

            if type(self.char) != invoc:
                self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence = round(self.char.strength+sumStatsBonus[0]*self.tetedepioche()[0]),round(self.char.endurance+sumStatsBonus[1]*self.tetedepioche()[0]),round(self.char.charisma+sumStatsBonus[2]),round(self.char.agility+sumStatsBonus[3]*self.tetedepioche()[1]),round(self.char.precision+sumStatsBonus[4]*self.tetedepioche()[1]),round(self.char.intelligence+sumStatsBonus[5])
                self.resistance,self.percing,self.critical = round(self.char.resistance+sumStatsBonus[6]),round(self.char.percing+sumStatsBonus[7]),round(self.char.critical+sumStatsBonus[8])
            else:
                self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence = round(sumStatsBonus[0]*self.tetedepioche()[0]),round(sumStatsBonus[1]*self.tetedepioche()[0]),round(sumStatsBonus[2]),round(sumStatsBonus[3]*self.tetedepioche()[1]),round(sumStatsBonus[4]*self.tetedepioche()[1]),round(sumStatsBonus[5])
                self.resistance,self.percing,self.critical = round(sumStatsBonus[6]),round(sumStatsBonus[7]),round(sumStatsBonus[8])

            self.stun = stuned

        def refreshEffect(self):
            """Rajoute les effets en liste d'attente à l'entité et retire les effets périmés"""
            for a in self.effect:
                if a.remove:
                    self.effect.remove(a)
                    a.caster.ownEffect.remove(a)

            for a in addEffect:
                self.effect.append(a)
                a.caster.ownEffect.append(a)
                addEffect.remove(a)
            self.recalculate()

        def indirectAttack(self,target=0,value=0,icon="",ignoreImmunity=False):
            """Méthode à appeler lorsque l'entité attaque de manière indirecte.
            Renvoie un str contenant les messages correspondant aux actions effectuées"""

            popopo = ""
            value = round(value)
            if target.hp > 0:
                for a in target.effect:
                    if a.effect.immunity == True and not(ignoreImmunity):
                        value = 0
                        break

                target.hp -= value
                if value <= 9000:
                    self.stats.damageDeal += value
                    self.stats.indirectDamageDeal += value
                    target.stats.damageRecived += value
                popopo = f"{self.icon} {icon} → {target.icon} -{value} PV\n"

                if target.hp <= 0:
                    popopo += target.death(killer=self)

            return popopo

        def death(self,killer = 0):
            """Méthode à appeler lorsque l'entité meurt.
            Renvoie un str contenant les messages correspondant aux actions effectuées"""
            pipistrelle = f"{self.char.name} ({self.icon}) est mort{self.accord()} !\n"
            if self.status == STATUS_RESURECTED:
                pipistrelle = f"{self.char.name} ({self.icon}) est mort{self.accord()} (pour de bon) !\n"
                self.status=STATUS_TRUE_DEATH

            for a in self.effect:
                if a.trigger == TRIGGER_DEATH:
                    pipistrelle += a.triggerDeath(killer)

            self.refreshEffect()

            if self.status == STATUS_ALIVE:
                if self.ressurectable:
                    self.status = STATUS_DEAD
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
                add_effect(killer,self,lostSoul)
                self.refreshEffect()

            killer.stats.ennemiKill += 1
            return pipistrelle

        def attack(self,target=0,value = 0,icon = "",area=AREA_MONO,sussess=None,maxRange=None,use=STRENGTH,onArmor = 1):
            """Méthode à appeler lorsque l'entité attaque.
            Renvoie un str contenant les messages correspondant aux actions effectuées"""
            if sussess==None: # If no success is gave, use the weapon success rate
                sussess=self.char.weapon.sussess
            if maxRange==None: # If no maxRange is gave, use the weapon max range
                maxRange=self.char.weapon.range
            
            popipo,critMsg,ppEffect = "","",0

            if type(target) != int: # If the target is valid
                dangerMul = 1
                if danger != None and self.team: # get danger value
                    dangerMul = danger/100

                if target.hp > 0: # If the target is alive
                    critRate = round(self.precision/3.33)+round(self.agility/6.66)+self.critical
                    popipo,immune,multiplicateur = "",False,1

                    for a in self.effect: # Does the attacker trigger a effect
                        if a.trigger == TRIGGER_DEALS_DAMAGE:
                            temp = a.triggerDamage(value = a.effect.power,icon=a.icon,onArmor=onArmor)
                            value = temp[0]
                            popipo += temp[1]

                    if self.hp > 0 and target.hp > 0: # Does the attacker still alive ?
                        for z in target.cell.getEntityOnArea(area=area,team=self.team,wanted=ENNEMIS): # For eatch ennemis in the area
                            pp = 0
                            if self.char.aspiration == POIDS_PLUME: # Apply "Poids Plume" critical bonus
                                for a in self.effect:
                                    if a.effect == poidPlumeEff:
                                        pp = a.value
                                        ppEffect = a
                                        break

                            self.stats.totalNumberShot += 1
                            if z.hp > 0: # If the target is alive

                                # Get the stat used
                                if use == HARMONIE:
                                    temp = 0
                                    for a in self.allStats():
                                        temp = max(a,temp)
                                    used = temp
                                else:
                                    used = self.allStats()[use]
                                
                                damage = round(value * (used+100)/100 * (1-(min(95,z.resistance-self.percing)/100))*dangerMul*self.getElementalBonus(target=z,area=area,type=TYPE_DAMAGE))
                                
                                # AoE reduction factor
                                if z == target: 
                                    multiplicateur = 1
                                else:
                                    multiplicateur = 1-(min(0.66,target.cell.distance(z.cell)*0.33))
                                
                                # Dodge / Miss
                                successRate = 1
                                temp7,temp8 = self.precision,z.agility
                                if temp7 < 0:
                                    temp8 += abs(temp7)
                                    temp7 = 0
                                elif temp8 <= 0:
                                    temp7 += abs(temp8)
                                    temp8 = 1

                                if temp7 > temp8:
                                    successRate = successRate + max((temp8-temp7)/200,0.5)
                                else:
                                    successRate = successRate + min((temp8-temp7)/100,1)

                                # It' a hit ?
                                if random.randint(0,99)<successRate*sussess:
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
                                                    ailill = 25
                                                
                                    z.refreshEffect()

                                    # Critical
                                    critRoll = random.randint(0,99)
                                    critMsg = ""
                                    if critRoll < critRate and damage > 0:
                                        critMsg = " (Critique !)"
                                        multiplicateur += 0.45
                                        self.stats.crits += 1
                                    elif critRoll < critRate + pp and self.char.aspiration == POIDS_PLUME and damage > 0:
                                        for a in self.effect:
                                            if a == ppEffect:
                                                multiplicateur += 0.45
                                                critMsg = " (Critique !)"
                                                ppEffect.value = 0
                                                self.stats.crits += 1
                                                break

                                    effectiveDmg = round(damage*(multiplicateur+self.berserked()+self.observateur(target=z,maxRange=maxRange))*ailill/100)                                 

                                    self.stats.shootHited += 1
                                    self.stats.damageDeal += effectiveDmg
                                    z.stats.damageRecived += effectiveDmg
                                    z.stats.numberAttacked += 1
                                    z.hp -= effectiveDmg

                                    # Damage bosted
                                    if use != None:
                                        for statBoost in self.effect:
                                            tstats = statBoost.allStats()
                                            turnStat,actTurnStat = 0,0
                                            if use != HARMONIE:
                                                turnStat = self.allStats()[use]
                                                actTurnStat = tstats[use]
                                            elif use == HARMONIE:
                                                for chocobot in self.allStats():
                                                    turnStat = max(turnStat,chocobot)
                                                for chocobot in tstats:
                                                    actTurnStat = max(actTurnStat,chocobot)                                        

                                            if turnStat != actTurnStat: # If the stat was boosted
                                                if use == HARMONIE:
                                                    temp = 0
                                                    for a in self.allStats():
                                                        temp = max(a,temp)
                                                    used = temp
                                                else:
                                                    used = self.allStats()[use]
                                                tempDmg = round(round(value * (used+100)/100 * (1-(min(95,z.resistance-self.percing)/100)) * dangerMul)*(multiplicateur+self.berserked()+self.observateur(target=z,maxRange=maxRange))*ailill/100)
                                                dif = effectiveDmg - tempDmg
                                                if dif < 0:
                                                    statBoost.caster.stats.damageBoosted += abs(dif)
                                                else:
                                                    statBoost.caster.stats.damageDogded += abs(dif)

                                    # Damage message
                                    if effectiveDmg > 0:
                                        popipo  += f"{self.icon} {icon} → {z.icon} -{effectiveDmg} PV{critMsg}\n"
                                    if z.hp <= 0:
                                        popipo += z.death(killer = self)

                                    for a in z.effect:
                                        if a.effect == hourglass1:
                                            a.value += effectiveDmg
                                            break
                                else:
                                    popipo += f"{z.char.name} esquive l'attaque\n"
                                    z.stats.dodge += 1
                                    z.stats.numberAttacked += 1
                                    if z.char.aspiration == POIDS_PLUME:
                                        for a in z.effect:
                                            if a.effect == poidPlumeEff:
                                                a.value += 5
                                                break
            else:
                popipo =f"{self.char.name} ne sait pas quoi faire"

            return popipo

        def startOfTurn(self,tablEntTeam="tabl"):
            """Méthode à appeler lorsque l'entité acommence son tour.

            Diminue le leftTurn des effets dont elle est l'auteur sur toutes les autre entités.

            Renvoie un str contenant les messages correspondant aux actions effectuées"""
            temp = ""
            for a in self.effect:
                if a.trigger == TRIGGER_START_OF_TURN:
                    temp += a.triggerStartOfTurn()

            cmpt = 0
            tempTabl = []
            for a in self.ownEffect:
                tempTabl += [a]
            while cmpt < len(tempTabl):
                a = tempTabl[cmpt]
                for b in a.on.effect:
                    if b.effect.id == a.effect.id:
                        temp += b.decate(turn=1)
                a.on.refreshEffect()
                cmpt+=1

            for a in range(0,5):
                if self.cooldowns[a] > 0:
                    self.cooldowns[a] -= 1
                
            self.refreshEffect()

            return temp

        def endOfTurn(self):
            """Méthode à appeler lorsque l'entité termine son tour.
            Renvoie un str contenant les messages correspondant aux actions effectuées"""
            temp = ""
            for a in self.effect:
                if a.trigger == TRIGGER_END_OF_TURN:
                    temp += a.triggerEndOfTurn()

            self.refreshEffect()
            return temp

        def atRange(self):
            """Renvoie les ennemis à portée de tir"""
            return self.cell.getEntityOnArea(area=self.char.weapon.effectiveRange,team=self.team,wanted=self.char.weapon.target,lineOfSight= True)

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

        def accord(self):
            if self.char.gender == GENDER_FEMALE:
                return "e"
            else:
                return ""
    
        def erudit(self):
            if self.char.aspiration == ERUDIT:
                return 80
            else:
                return 100
 
        def observateur(self,target,maxRange):
            if self.cell.distance(target.cell) == maxRange and self.char.aspiration == OBSERVATEUR:
                return 0.2
            else:
                return 0

        async def getIcon(self,bot):
            if type(self.char) == char:
                self.icon = await getUserIcon(bot,self.char)
            else:
                self.icon = self.char.icon

        def getMedals(self,array):
            respond = ""
            tabl = [["<:topDpt:884337213670838282>","<:secondDPT:884337233241448478>","<:thirdDPT:884337256905732107>"],["<:topHealer:884337335410491394>","<:secondHealer:884337355262160937>","<:thirdHealer:884337368407093278>"],["<:topArmor:884337281547272263>","<:secondArmor:884337300975276073>","<:thirdArmor:884337319707037736>"]]
            for z in range(0,len(array)):
                for a in (0,1,2):
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

        def summon(self,summon,timeline,cell,tablEntTeam,tablAliveInvoc):
            ballerine = ""
            team = self.team
            summon.color = self.char.color
            if tablAliveInvoc[team] < 3:
                sumEnt = entity(self.id,summon,team,False,summoner=self)
                sumEnt.move(cell.x,cell.y)
                tablEntTeam[self.team].append(sumEnt)

                timeline.timeline.insert(1,sumEnt)

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

    class fightEffect:
        """Classe plus pousée que Effect pour le combat"""

        def __init__(self,id,effect,caster,on,turnLeft,trigger,type,icon,value=1):
            """self.id : int -> Id de l'effet
            self.effect : effect -> L'effet de base
            self.caster : entity -> L'entité qui donne l'effet
            self.on : entity -> L'entité sur laquel se trouve cet effet
            self.turnLeft : int -> Nombre de tour restant à l'effet
            self.trigger : const -> L'événement qui déclanche l'effet
            self.icon : str -> L'id de l'emoji correspondant à l'effet"""
            self.effect = effect
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

        def decate(self,turn=0,value=0):
            """Réduit le leftTurn ou value de l'effet"""
            self.turnLeft -= turn
            self.value -= value
            temp = ""

            if (self.turnLeft <= 0 and self.effect.turnInit > 0) or self.value <= 0 and not(self.effect.unclearable):
                if self.trigger == TRIGGER_ON_REMOVE:
                    temp += self.triggerRemove()
                self.remove = True
                if not(self.effect.silent) and self.on.hp > 0:
                    temp += f"{self.on.char.name} n'est plus sous l'effet __{self.effect.name}__\n"
            return temp

        def triggerDamage(self,value=0,icon="",declancher = 0,onArmor = 1):
            """Déclanche l'effet"""
            value = round(value)
            temp2 = [value,""]
            if self.type == TYPE_ARMOR and value >0:
                valueT = value
                valueT2 = round(value * onArmor)
                value = min(valueT2,self.value)
                temp2 = [0,f"{declancher.icon} {icon} → {self.icon}{self.on.icon} -{value} PV\n"]
                temp2[1] += self.decate(value=value)
                declancher.stats.damageOnShield += value
                if self.value <= 0:
                    ratio = valueT/valueT2
                    ballerine = valueT2 - value - 50
                    babie = int(ballerine * ratio)
                    temp2[0] = max(0,babie)

            elif self.type == TYPE_INDIRECT_DAMAGE and self.value>0:
                variable = ""
                damageBase = self.effect.power
                if self.effect.stat == None:
                    stat = None
                else:
                    stat = self.caster.allStats()[self.effect.stat]

                whoTarget = ALLIES
                if self.on.team == self.caster.team and self.on != self.caster:
                    whoTarget = ENNEMIS

                for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.on.team,wanted=whoTarget):
                    reduc = 1
                    if a != self.on:
                        reduc = max(0.33,1-self.on.cell.distance(a.cell)*0.33)

                    if stat != None:
                        damage = damageBase * (1+(stat/self.caster.erudit())) * (1-min(95,self.on.resistance-self.caster.percing)/100) * reduc * self.caster.getElementalBonus(a,self.effect.area,TYPE_INDIRECT_DAMAGE)

                    variable += self.caster.indirectAttack(a,value=damage,icon = self.icon)
                temp2[1] = f"L'effet __{self.effect.name}__ se déclanche :\n{variable}{self.decate(value=1)}"
                
            return temp2

        def triggerDeath(self,killer=None):
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
                temp += f"{self.on.char.name} ({self.on.icon}) est ressucité{self.on.accord()} !\n{self.caster.icon} {self.icon}→ {self.on.icon} +{heal} PV\n"
                self.decate(value=1)

            elif self.type == TYPE_INDIRECT_DAMAGE and self.value>0:
                variable = ""
                stat,damageBase = self.caster.allStats()[self.effect.stat],self.effect.power
                if self.effect.stat == None:
                    stat = None
                
                whoTarget = ALLIES
                if self.on.team == self.caster.team and self.on != self.caster:
                    whoTarget = ENNEMIS

                for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.on.team,wanted=whoTarget):
                    reduc = 1
                    if a != self.on:
                        reduc = max(0.33,1-self.on.cell.distance(a.cell)*0.33)

                    if stat != None:
                        damage = damageBase * (1+(stat/self.caster.erudit())) * (1-min(95,self.on.resistance-self.caster.percing)/100) * (reduc) * self.caster.getElementalBonus(a,self.effect.area,TYPE_INDIRECT_DAMAGE)

                    variable += self.caster.indirectAttack(a,value=damage,icon = self.icon)
                temp += f"L'effet __{self.effect.name}__ se déclanche :\n{variable}{self.decate(value=1)}"

            elif self.type == TYPE_UNIQUE:
                if self.effect == hunter:
                    add_effect(self.on,self.on,hunterBuff)
                    self.on.refreshEffect()
                    temp+= self.on.attack(target=killer,value = self.on.char.weapon.power,icon = self.on.char.weapon.emoji,onArmor=self.on.char.weapon.onArmor)

            if self.effect.callOnTrigger != None:
                temp += add_effect(self.on,self.on,findEffect(self.effect.callOnTrigger))

            self.decate(value=1)

            return temp

        def triggerStartOfTurn(self):
            """Déclanche l'effet"""
            ballerine=f"L'effet {self.effect.name} se déclanche :\n"
            if self.type == TYPE_INDIRECT_HEAL:
                healPowa = min(self.on.maxHp - self.on.hp,round(self.effect.power * (1+self.caster.charisma/100)* self.caster.valueBoost(target = self.on)*self.caster.getElementalBonus(self.on,area = AREA_MONO,type = TYPE_INDIRECT_HEAL)))
                for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.caster.team,wanted=ALLIES):
                    healPowa = round(healPowa * ((100-self.on.healResist)/100))
                    self.on.healResist += int(healPowa/self.on.maxHp/2*100)
                    self.on.hp += healPowa
                    self.caster.stats.heals += healPowa
                    ballerine += f"{self.caster.icon} {self.icon}→ {self.on.icon} +{healPowa} PV\n"

            elif self.type == TYPE_INDIRECT_DAMAGE and self.value>0:
                variable = ""
                if self.effect.stat != None:
                    stat,damageBase = self.caster.allStats()[self.effect.stat],self.effect.power
                    whoTarget = ALLIES
                    if self.on.team == self.caster.team and self.on != self.caster:
                        whoTarget = ENNEMIS


                    for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.on.team,wanted=whoTarget):
                        selfElem = self.caster.getElementalBonus(a,self.effect.area,TYPE_INDIRECT_DAMAGE)
                        areaMul = 1
                        if a != self.on:
                            areaMul = max(0.33,1-self.on.cell.distance(a.cell)*0.33)
                        damage = damageBase * (1+(stat/self.caster.erudit())) * (1-min(95,self.on.resistance-self.caster.percing)/100) * areaMul * selfElem
                        variable += self.caster.indirectAttack(a,value=damage,icon = self.icon)
                    ballerine = f"L'effet __{self.effect.name}__ se déclanche :\n{variable}{self.decate(value=1)}"
                else:
                    for a in self.on.cell.getEntityOnArea(area=self.effect.area,team=self.on.team,wanted=whoTarget):
                        damage = self.effect.power
                        variable += self.caster.indirectAttack(a,value=damage,icon = self.icon)
                    ballerine = f"L'effet __{self.effect.name}__ se déclanche :\n{variable}{self.decate(value=1)}"

            return ballerine

        def triggerEndOfTurn(self):
            """Déclanche l'effet"""
            temp = ""
            if self.type == TYPE_INDIRECT_DAMAGE:
                temp += self.caster.indirectAttack(target=self.on,ignoreImmunity=self.effect.ignoreImmunity ,value=self.effect.power)
                self.decate(value=1)
            elif self.type == TYPE_UNIQUE:
                if self.effect == poidPlumeEff:
                    self.value = self.value//2
            return temp

        def triggerRemove(self):
            if not(self.effect.silent):
                message = f'L\'effet __{self.effect.name}__ se déclanche :\n'
            else:
                message = ""
            if self.type == TYPE_UNIQUE:
                if self.effect == hourglass1 and self.on.hp > 0:
                    heal = min(self.on.maxHp - self.on.hp, round(self.value * 0.75))
                    self.on.hp += heal
                    self.caster.stats.heals += heal
                    message = f'{self.caster.icon} {self.icon}→ {self.on.icon} +{heal}\n'

                elif self.effect == lostSoul:
                    if self.on.status == STATUS_DEAD:
                        self.on.status = STATUS_TRUE_DEATH
                        message="{0} en avait marre d'attendre une résurection et a quitté le combat\n".format(self.on.char.name)

            return message

        def allStats(self):
            tablTemp = [0,0,0,0,0,0,0,0,0]
            if self.effect.stat != None:
                temp = self.caster.allStats()[self.effect.stat]
                tablTemp[0] += self.effect.strength * self.value * (temp+100)/100
                tablTemp[1] += self.effect.endurance * self.value * (temp+100)/100
                tablTemp[2] += self.effect.charisma * self.value * (temp+100)/100
                tablTemp[3] += self.effect.agility* self.value * (temp+100)/100
                tablTemp[4] += self.effect.precision* self.value * (temp+100)/100
                tablTemp[5] += self.effect.intelligence* self.value * (temp+100)/100
                tablTemp[6] += self.effect.resistance* self.value * (temp+100)/100
                tablTemp[7] += self.effect.percing* self.value * (temp+100)/100
                tablTemp[8] += self.effect.critical* self.value * (temp+100)/100

            else:
                tablTemp[0] += self.effect.strength 
                tablTemp[1] += self.effect.endurance 
                tablTemp[2] += self.effect.charisma
                tablTemp[3] += self.effect.agility
                tablTemp[4] += self.effect.precision
                tablTemp[5] += self.effect.intelligence
                tablTemp[6] += self.effect.resistance
                tablTemp[7] += self.effect.percing
                tablTemp[8] += self.effect.critical

            return tablTemp
        
    class timeline:
        """Classe de la timeline"""
        def __init__(self,tablEntTeam):

            timeline = []
            random.shuffle(tablEntTeam[0])
            random.shuffle(tablEntTeam[1])

            for a in range(0,max(len(tablEntTeam[0]),len(tablEntTeam[1]))):
                try:
                    timeline+=[tablEntTeam[0][a]]
                except:
                    pass
                try:
                    timeline+=[tablEntTeam[1][a]]
                except:
                    pass

            self.timeline = timeline
            self.begin = self.timeline[0]

        def icons(self):
            temp = ""
            for a in self.timeline:
                temp += f"{a.icon} <- "

            return temp

        def endOfTurn(self,tablEntTeam,tablAliveInvoc):
            temp = self.timeline
            temp2 = temp[0]

            temp.remove(temp2)
            temp.append(temp2)

            for a in temp[:]:
                if a.hp <= 0 and type(a.char) == invoc:
                    temp.remove(a)
                    for c in range(0,len(tablEntTeam[a.team])):
                        if tablEntTeam[a.team][c].id == a.summoner.id:
                            tablEntTeam[a.team][c].stats.damageDeal += a.stats.damageDeal
                            tablEntTeam[a.team][c].stats.indirectDamageDeal += a.stats.indirectDamageDeal
                            tablEntTeam[a.team][c].stats.ennemiKill += a.stats.ennemiKill
                            tablEntTeam[a.team][c].stats.damageRecived += a.stats.damageRecived
                            tablEntTeam[a.team][c].stats.heals += a.stats.heals
                            tablEntTeam[a.team][c].stats.damageOnShield += a.stats.damageOnShield
                            tablEntTeam[a.team][c].stats.shieldGived += a.stats.shieldGived
                            break
                    
                    tablEntTeam[a.team].remove(a)
                    tablAliveInvoc[a.team] -= 1
            
            self.timeline = temp
            return {"tablEntTeam":tablEntTeam,"tablAliveInvoc":tablAliveInvoc}

    def add_effect(caster,target,effect):
        """Méthode qui rajoute l'effet Effet à l'entity Target lancé par Caster dans la liste d'attente des effets"""
        valid,id,popipo = False,0,""
        valid = True
        if effect.reject != None:
            for a in effect.reject:
                for b in target.effect:
                    if a == b.effect.id:
                        popipo = f"{caster.icon} {effect.emoji[caster.char.species-1][caster.team]} → 🚫{findEffect(a).emoji[caster.char.species-1][caster.team]} {target.icon}\n"
                        valid = False
                        break
                if not(valid):
                    break
        for a in target.effect:
            if a.effect.id == effect.id and not(effect.stackable):
                if not(effect.silent):
                    popipo = f"{caster.icon} {effect.emoji[caster.char.species-1][caster.team]} → 🚫{a.effect.emoji[caster.char.species-1][caster.team]} {target.icon}\n"
                valid = False
                break
                
        if valid:
            valid = False
            while not(valid):
                id,trouv = random.randint(1000,9999),False

                for a in allEffectInFight:
                    if a == id:
                        trouv = True
                        break
                
                if not(trouv):
                    valid = True

            icon = effect.emoji[caster.char.species-1][caster.team]

            if effect.overhealth > 0:
                temp = caster.allStats()
                value = effect.overhealth
                if effect.stat != None:
                    value = round(effect.overhealth * caster.valueBoost(target=target) * (target.endurance + temp[effect.stat]+ 100)/100)
                else:
                    value = round(effect.overhealth * caster.valueBoost(target=target) * (target.endurance + 100)/100)

                for a in target.effect:
                    if a.type == TYPE_ARMOR:
                        value = round(value/2)

                caster.stats.shieldGived += value
                addEffect.append(fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,TYPE_ARMOR,icon,value))
                
                if not(effect.silent):
                    pluriel = ""
                    name = effect.name
                    if name.endswith("é"):
                        name += target.accord()
                    if value > 1:
                        pluriel = "s"
                    if effect.turnInit > 0:
                        popipo = f"{target.char.name} ({target.icon}) est sous l'effet de __{name}__ ({icon} {value}) pendant {effect.turnInit} tour{pluriel}\n"
                    else:
                        popipo = f"{target.char.name} ({target.icon}) est sous l'effet de __{name}__ ({icon} {value})\n"

            else:
                addEffect.append(fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,effect.type,icon,effect.lvl))
                name = effect.name
                if name.endswith("é"):
                    name += target.accord()
                if not(effect.silent):
                    if effect.turnInit > 0:
                        conjug = ""
                        if effect.turnInit > 1:
                            conjug ="s"
                        popipo = f"{target.char.name} ({target.icon}) est sous l'effet de __{name}__ ({icon}) pendant {effect.turnInit} tour{conjug}\n"
                    else:
                        popipo = f"{target.char.name} ({target.icon}) est sous l'effet de __{name}__ ({icon})\n"
                target.refreshEffect()
        return popipo

    def map():
        """Renvoie un str contenant la carte du combat"""
        line1,line2,line3,line4,line5 = [None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None]
        lines = [line1,line2,line3,line4,line5]

        for a in tablAllCells:
            temp = f'<:empty:866459463568850954>'
            #temp = f'{str(a.x)}-{str(a.y)}'
            if a.on != None:
                if a.on.status == STATUS_DEAD:
                    temp = ['<:ls1:868838101752098837>','<:ls2:868838465180151838>'][a.on.team]
                elif a.on.status != STATUS_TRUE_DEATH:
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

    def visibleArea(cells,middle):
        """Renvoie un str contenant la carte du combat en mettant en évidence les cellules Cells"""
        line1,line2,line3,line4,line5 = [None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None]
        lines = [line1,line2,line3,line4,line5]

        for a in tablAllCells:
            temp = '<:empty:866459463568850954>'
            for b in cells:
                if a == middle:
                    temp = '<:splatted2:727586393173524570>'
                elif a == b:
                    temp = '<:splatted1:727586364618702898>'
                    break

            lines[a.y][a.x]=temp

        temp = ""
        for a in lines:
            for b in [0,1,2,3,4]:
                temp += f"{a[b]}|"
            temp += f"{a[b+1]}\n"

        return temp

    # Début du combat ------------------------------------------------------
    logs += "Fight triggered by {0}\n".format(ctx.author.name)
    logs += "\n=========\nTeams filling phase\n=========\n\n"
    if len(team1) < 4 and not(octogone): # Remplisage de la team1
        aleaMax = len(tablAllAllies)-1
        alreadyFall = []
        lvlMax = 0

        for a in team1:
            lvlMax = max(lvlMax,a.level)

        while len(team1) < 4:
            temp,trouv = random.randint(0,aleaMax),False
            for a in alreadyFall:
                if a == temp:
                    trouv=True
                    break

            if not(trouv):
                alreadyFall+=[temp]
                alea = tablAllAllies[temp]
                alea.changeLevel(lvlMax)
                
                if temp == 0 and random.randint(0,99) < 10:
                    alea = tablVarAllies[0]
                elif temp == 1:
                    bidule = random.randint(0,99)
                    if bidule < 50:
                        alea = tablVarAllies[1]                        
                    elif bidule < 60:
                        alea = tablVarAllies[2]
                elif temp == 4 and random.randint(0,99) < 10:
                    alea = tablVarAllies[3]

                team1 += [alea]
                logs += "{0} have been added into team1\n".format(alea.name)

    if team2 == []: # Génération de la team 2
        lvlMax = 0
        for a in team1:
            lvlMax = max(lvlMax,a.level)
        
        dangerLevel = [65,70,75,80,85,90,95,100,110,120,135]
        dangerThugLevel = ['https://media.discordapp.net/attachments/810212020049543221/882219019644575796/danger65.png','https://cdn.discordapp.com/attachments/810212020049543221/882218077419339776/danger70.png','https://cdn.discordapp.com/attachments/810212020049543221/882218077650030632/danger75.png','https://cdn.discordapp.com/attachments/810212020049543221/882218077859762177/danger80.png','https://cdn.discordapp.com/attachments/810212020049543221/882218078119796776/danger85.png','https://cdn.discordapp.com/attachments/810212020049543221/882218078346297384/danger90.png','https://cdn.discordapp.com/attachments/810212020049543221/882218078606340136/danger95.png','https://cdn.discordapp.com/attachments/810212020049543221/882218078870593536/danger100.png','https://cdn.discordapp.com/attachments/810212020049543221/882218079407443998/danger110.png','https://cdn.discordapp.com/attachments/867393297520263208/884453208477532210/effect_20210902093005.png','https://media.discordapp.net/attachments/810212020049543221/882218079625568316/danger120.png']

        if random.randint(0,99) < 80 or len(team1) < 5: # Vs normal team
            winStreak = teamWinDB.getVictoryStreak(team1[0])
        
            for a in range(0,12):
                if winStreak == a:
                    danger = dangerLevel[a]
                    dangerThub = dangerThugLevel[a]
                aleaMax = len(tablAllOcta)-1
                alreadyFall = []

            oneVAll = False
            if len(team2) < len(team1):
                if random.randint(0,99) <= 33:
                    temp = random.randint(0,len(tablBoss)-1)
                    bottine = tablBoss[temp]

                    if bottine.oneVAll:
                        print("[Big shot]")
                        oneVAll = True
                        littleTeam = len(team1)/8
                    else:
                        littleTeam = 1
                    alea = octarien(bottine.name,bottine.strength*littleTeam,bottine.endurance*littleTeam,bottine.charisma*littleTeam,bottine.agility*littleTeam,bottine.precision*littleTeam,bottine.intelligence*littleTeam,bottine.resistance,bottine.percing,bottine.critical,bottine.weapon,bottine.exp,bottine.icon,bottine.skills,bottine.aspiration,bottine.gender,deadIcon=bottine.deadIcon)
                    alea.level = lvlMax
                    tempStats = alea.allStats()
                    for b in range(0,len(tempStats)):
                        tempStats[b] = round(tempStats[b]*0.1+tempStats[b]*0.9*lvlMax/50)

                    alea.strength,alea.endurance,alea.charisma,alea.agility,alea.precision,alea.intelligence = tempStats[0],tempStats[1],tempStats[2],tempStats[3],tempStats[4],tempStats[5]
                    team2 += [alea]
                    logs += "{0} have been added into team2\n".format(alea.name)

            while len(team2) < len(team1) and not(oneVAll):
                temp = random.randint(0,aleaMax)
                if temp not in alreadyFall:
                    alreadyFall += [temp]
                    bottine = tablAllOcta[temp]
                    alea = octarien(bottine.name,bottine.strength,bottine.endurance,bottine.charisma,bottine.agility,bottine.precision,bottine.intelligence,bottine.resistance,bottine.percing,bottine.critical,bottine.weapon,bottine.exp,bottine.icon,bottine.skills,bottine.aspiration,bottine.gender,deadIcon=bottine.deadIcon)
                    alea.level = lvlMax
                    tempStats = alea.allStats()
                    for b in range(0,len(tempStats)):
                        tempStats[b] = round(tempStats[b]*0.1+tempStats[b]*0.9*lvlMax/50)

                    alea.strength,alea.endurance,alea.charisma,alea.agility,alea.precision,alea.intelligence = tempStats[0],tempStats[1],tempStats[2],tempStats[3],tempStats[4],tempStats[5]
                    team2 += [alea]
                    logs += "{0} have been added into team2\n".format(alea.name)

        else: # Vs temp ally team
            danger = dangerLevel[1]
            dangerThub = dangerThugLevel[1]
            tabl = tablAllAllies[:]
            while len(team2) < len(team1):
                rand = random.randint(0,len(tabl)-1)

                alea = tabl[rand]
                tabl.remove(alea)

                if alea.name == "Lena" and random.randint(0,99) < 10:
                    alea = tablVarAllies[0]
                elif alea.name == "Gwendoline":
                    bidule = random.randint(0,99)
                    if bidule < 50:
                        alea = tablVarAllies[1]                        
                    elif bidule < 60:
                        alea = tablVarAllies[2]
                elif alea.name == "Shushi" and random.randint(0,99) < 10:
                    alea = tablVarAllies[3]

                alea.changeLevel(lvlMax)

                team2 += [alea]
                logs += "{0} have been added into team2".format(alea.name)

    tablTeam,tablEntTeam,cmpt = [team1,team2],[[],[]],0
    readyMsg,msg,cmpt = None,None,0

    for a in [0,1]:
        for b in tablTeam[a]:
            if auto == False and b.species != 3:
                try:
                    await bot.fetch_user(b.owner)
                    tablEntTeam[a] += [entity(cmpt,b,a,auto=False)]
                except:
                    tablEntTeam[a] += [entity(cmpt,b,a,danger=danger)]
            else:  
                tablEntTeam[a] += [entity(cmpt,b,a,danger=danger)]
            cmpt+=1
    
    for a in [0,1]:
        for b in tablEntTeam[a]:
            b.recalculate()
            await b.getIcon(bot=bot)

    if not(auto):
        if not(slash):
            await ctx.clear_reaction(emoji.loading)
            msg = await loadingEmbed(ctx)            
        else:
            msg = await ctx.send(embed = discord.Embed(title = "slash_command", description = emoji.loading))
    repEmb = discord.Embed(tilte = "Combat <:turf:810513139740573696>",color = light_blue)
    
    logs += "\n"
    versus = ""
    for a in [0,1]:
        logs += "\nTeam {0} composition :\n".format(a+1)
        versus+=f"\n__Equipe {a+1} :__\n"
        for b in tablEntTeam[a]:
            versus+=f"{b.icon} {b.char.name}\n"
            logs += "{0}\n".format(b.char.name)

    #Phase de placement --------------------------------------------------
    logs += "\n=========\nInitial placements phase\n=========\n\n"
    temp3 = [[2,1,0],[3,4,5]]
    placementlines=[[[],[],[]],[[],[],[]]]
    allAuto = True
    for a in [0,1]:
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

        temp1,temp2 = [melee,dist,snipe],[lenMel,lenDist,lenSnip]
        
        for b in [0,1,2]:
            if temp2[b] > 5:
                temp1[b+1] += temp1[b][5:]
                temp1[b] = temp1[b][0:5]
        
        placementlines[a]=[melee,dist,snipe]
        temp2[0],temp2[1],temp2[2],cmpt = len(temp1[0]),len(temp1[1]),len(temp1[2]),0

        for b in temp3[a]:
            random.shuffle(temp1[cmpt])

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
            cmpt += 1

    if dangerThub != None:
        repEmb.set_thumbnail(url=dangerThub)
    repEmb.add_field(name = "Ce combat oppose :",value = versus)
    repEmb.add_field(name = "__Carte__",value= map(),inline = False)
    if not(auto):
        await msg.edit(embed = repEmb)

    if not(auto): # Utilisateurs présent ?
        allReady = False
        already, awaited,awaitedChar = [],[],[]
        if not(slash):
            readyMsg = await loadingEmbed(ctx)
        else:
            readyMsg = await loadingSlashEmbed(ctx)

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
                
                awaited.remove(react[1])
                already += [react[1]]
                allAuto = False

                if awaited == []:
                    allReady = True
            except:
                break

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
                
    # Initialisation de la timeline --------------------------------------
    tempTurnMsg = "__Début du combat :__\n"
    if not(auto):
        turnMsg = readyMsg
        await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = light_blue))
        await turnMsg.clear_reactions()
    time = timeline(tablEntTeam)

    logs += "\n=========\nStuffs passives effects phase\n=========\n\n"
    for a in [0,1]: # Don des effets équipés
        for b in tablEntTeam[a]:
            for c in [b.char.weapon,b.char.stuff[0],b.char.stuff[1],b.char.stuff[2]]:
                if c.effect != None:
                    if c.effect == "mk":
                        for z in tablEntTeam[b.team]:
                            baseHP,HPparLevel = 130,8
                            temp = z.char.endurance
                            for y in [z.char.weapon,z.char.stuff[0],z.char.stuff[1],z.char.stuff[2]]:
                                temp += y.endurance

                            if b.team == 0:
                                dangerFact = 1
                            elif b.team == 1:
                                dangerFact = danger/100
                            z.hp = round((baseHP+z.char.level*HPparLevel)*((temp)/100+1)*dangerFact)
                            z.maxHp = round((baseHP+z.char.level*HPparLevel)*((temp)/100+1)*dangerFact)

                            effect=findEffect(c.effect)
                            tempTurnMsg += add_effect(b,z,effect)
                            logs += "{0} gave the {1} effect at {2} for {3} turns\n".format(b.char.name,effect.name,z.char.name,effect.turnInit)
                            z.refreshEffect()
                    else:
                        effect=findEffect(c.effect)
                        tempTurnMsg += add_effect(b,b,effect)
                        logs += "{0} gave the {1} effect at {2} for {3} turns\n".format(b.char.name,effect.name,b.char.name,effect.turnInit)

            if b.char.aspiration == POIDS_PLUME:
                tempTurnMsg += add_effect(b,b,poidPlumeEff)
                logs += "{0} gave the {1} effect at {2} for {3} turns\n".format(b.char.name,poidPlumeEff.name,b.char.name,poidPlumeEff.turnInit)

            if type(b.char)==octarien and b.char.name=="Ailill" and len(tablEntTeam[0])>4:
                tempTurnMsg += add_effect(b,b,dephased)
                logs += "{0} gave the {1} effect at {2} for {3} turns\n".format(b.char.name,dephased.name,b.char.name,dephased.turnInit)

            b.refreshEffect()

    if contexte != []:
        for a in contexte:
            if a[0] == ALL:
                for b in [0,1]:
                    for c in tablEntTeam[b]:
                        tempTurnMsg += add_effect(c,c,findEffect(a[1]))
                        c.refreshEffect()

            elif a[0] == TEAM1:
                for b in tablEntTeam[0]:
                    tempTurnMsg += add_effect(b,b,findEffect(a[1]))
                    b.refreshEffect()

            elif a[0] == TEAM2:
                for b in tablEntTeam[1]:
                    tempTurnMsg += add_effect(b,b,findEffect(a[1]))
                    b.refreshEffect()

    for a in [0,1]: # Vérification de présence de sort de résurection
        for b in tablEntTeam[a]:
            for c in b.char.skills + b.effect:
                if c != None and c!="0":
                    if c.type == TYPE_INDIRECT_REZ or c.type == TYPE_RESURECTION or (c.id == "yt" and b.char.aspiration in [IDOLE,ALTRUISTE]):
                        for d in tablEntTeam[a]:
                            d.ressurectable = True
                        break
            if b.ressurectable:
                break

    choiceMsg = 0
    if not(auto):
        await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = light_blue))
        await asyncio.sleep(3)
        if not(allAuto):
            if not(slash):
                choiceMsg = await loadingEmbed(ctx)
            else:
                choiceMsg = await loadingSlashEmbed(ctx)

    fight = True
    
    # Début effectif du combat --------------------------------------------------------------------------------
    try:   
        while fight:
            everyoneDead = [True,True]
            actTurn = time.timeline[0]
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
    
            tempTurnMsg = f"__Début du tour de {actTurn.char.name} :__\n"

            if actTurn == time.begin:
                tour += 1
                logs += "\n\n=========\nTurn {0}\n=========".format(tour)

                for a in [0,1]:
                    for b in tablEntTeam[a]:
                        if b.hp > 0:
                            b.stats.survival = tour

                if tour >= 16:
                    tempTurnMsg += f"\nMort subite !\nTous les combattants perdent {10*(tour-15)} PV\n"
                    for a in [0,1]:
                        for b in tablEntTeam[a]:
                            if b.hp > 0:
                                b.hp -= 10*(tour-15)
                                if b.hp <= 0:
                                    tempTurnMsg += b.death(killer=b)

            for c in [0,1]:
                for d in tablEntTeam[c]:
                    if d.hp > 0 and type(d.char) != invoc:
                        everyoneDead[c] = False
                        break

            if everyoneDead[0] or everyoneDead[1]:
                break

            embInfo = discord.Embed(title = "Combat <:turf:810513139740573696>",color = light_blue)

            if dangerThub != None:
                embInfo.set_thumbnail(url=dangerThub)
            embInfo.add_field(name = "__Carte__",value=map(),inline = False)
            embInfo.add_field(name = "__Timeline__",value=time.icons(),inline = False)

            # Tour en cours -------------------------------------------------------------------------------------
            wasAlive = actTurn.hp > 0
            temp,atRange = "",actTurn.atRange()
            nbTargetAtRange = len(atRange)
            tempTurnMsg += actTurn.startOfTurn(tablEntTeam=tablEntTeam)

            infoOp,cmpt = [],0
            for a in [0,1]:
                for b in tablEntTeam[a]:
                    if type(b.char) != invoc:
                        infoOp += [create_select_option(b.char.name,str(cmpt),getEmojiObject(b.icon),f"PV : {max(0,b.hp)} ({max(0,round(b.hp/b.maxHp*100))}%), R.S. : {b.healResist}%")]
                    cmpt+=1
            infoSelect = create_select(infoOp,placeholder="Voir les PVs des combattants")

            if wasAlive and actTurn.hp <= 0: # Died from poison
                temp2 = actTurn.allStats()
                
                for a in range(0,len(nameStats)): # Affichage des statistiques
                    temp += f"{nameStats[a]} : {temp2[a]}\n"

                embInfo.add_field(name = f"__{actTurn.icon} {actTurn.char.name}__",value=f"PV : {max(0,actTurn.hp)} / {actTurn.maxHp}",inline = False)
                embInfo.add_field(name = "__Liste des effets :__",value=actTurn.effectIcons(),inline = True)
                embInfo.add_field(name = "__Statistiques :__",value = temp,inline = True)

                if not(auto):
                    await msg.edit(embed = embInfo, components=[create_actionrow(infoSelect)])
                    await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color))
                    await asyncio.sleep(2+(len(tempTurnMsg)/1000)*5)
        
            elif actTurn.hp > 0:
                logs += "\n\nTurn {0} - {1} :".format(tour,actTurn.char.name)
                temp2 = actTurn.allStats()
                
                for a in range(0,len(nameStats)): # Affichage des statistiques
                    temp += f"{nameStats[a]} : {temp2[a]}\n"

                embInfo.add_field(name = f"__{actTurn.icon} {actTurn.char.name}__",value=f"PV : {max(0,actTurn.hp)} / {actTurn.maxHp}",inline = False)
                embInfo.add_field(name = "__Liste des effets :__",value=actTurn.effectIcons(),inline = True)
                embInfo.add_field(name = "__Statistiques :__",value = temp,inline = True)

                if not(auto):
                    await msg.edit(embed = embInfo,components=[create_actionrow(infoSelect)])
                    if nextNotAuto == actTurn:
                        await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color))

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

                if not(actTurn.stun): # Tour
                    if not(actTurn.auto) : # Fenêtre de sélection de l'option d'un joueur non automatique
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
                                if a != None and a != "0":
                                    tempTabl += [a]
                                else:
                                    tempTabl += [None]

                            for a in range(0,len(tabltabl)):
                                if tempTabl[a] != None:
                                    if tabltabl[a] == 0:
                                        if type(tempTabl[a]) == weapon and len(actTurn.atRange()) > 0:
                                            canBeUsed += [tempTabl[a]]
                                            choiceMsgTemp += f"{tempTabl[a].emoji} {tempTabl[a].name} (Cibles à portée : {str(nbTargetAtRange)})\n"
                                        elif type(tempTabl[a]) != weapon:
                                            babie = [TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE,TYPE_DAMAGE]
                                            target = ALLIES
                                            for b in babie:
                                                if tempTabl[a].type == b:
                                                    target = ENNEMIS
                                                    break

                                            healMsg = ""
                                            if tempTabl[a].type == TYPE_HEAL:
                                                healMsg = f" (<:INeedHealing:881587796287057951> x {len(actTurn.cell.getEntityOnArea(area=tempTabl[a].range,team=actTurn.team,wanted=target,lifeUnderPurcentage=50))})"

                                            line = tempTabl[a].type in babie
                                            if tempTabl[a].range != AREA_MONO:
                                                if (tempTabl[a].type != TYPE_INVOC and len(actTurn.cell.getEntityOnArea(area=tempTabl[a].range,team=actTurn.team,wanted=target,lineOfSight=line)) > 0) or (tempTabl[a].type == TYPE_INVOC and tablAliveInvoc[actTurn.team] <3):
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
                            if canMove[0] or canMove[1] or canMove[2] or canMove[3]:
                                canBeUsed += [option("Déplacement",'👟')]
                                choiceMsgTemp += "👟 Déplacement\n"

                            canBeUsed += [option("Passer",'🚫')]
                            choiceMsgTemp += "🚫 Passer"

                            mainOptions,cmpt = [],0
                            for a in canBeUsed:
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

                                    mainOptions += [create_select_option(a.name,str(cmpt),getEmojiObject(a.emoji),desc)]
                                else:
                                    mainOptions += [create_select_option(a.name,str(cmpt),a.emoji)]
                                cmpt += 1

                            mainSelect = create_select(options=mainOptions,placeholder = "Séléctionnez une option :")

                            if haveIterate:
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
                                
                            if type(react) == weapon:
                                weapOptions = []
                                for a in range(0,nbTargetAtRange):
                                    choiceMsgTemp += f"{a} - {atRange[a].quickEffectIcons()}"
                                    desc = f"PV : {int(atRange[a].hp/atRange[a].maxHp*100)}%, Pos : {atRange[a].cell.x} - {atRange[a].cell.y}"
                                    if react.area != AREA_MONO:
                                        desc += f", Zone : {len(atRange[a].cell.getEntityOnArea(area=actTurn.char.weapon.area,team=actTurn.team,wanted=actTurn.char.weapon.target))}"
                                    weapOptions += [create_select_option(atRange[a].char.name,str(a),getEmojiObject(atRange[a].icon),desc)]

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
                                            targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.range,team=actTurn.team,wanted=ALLIES)
                                            break
                                    for a in babie:
                                        if a == skillToUse.type:
                                            targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.range,team=actTurn.team,wanted=ENNEMIS,lineOfSight=True)
                                            break

                                else:
                                    for a in ballerine:
                                        if a == skillToUse.type:
                                            targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES)
                                            break
                                    for a in babie:
                                        if a == skillToUse.type:
                                            targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENNEMIS,lineOfSight=True)
                                            break

                                    if skillToUse.type == TYPE_UNIQUE:
                                        targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALL)
                                    choiceMsgTemp += "Les combattants suivants seront affectés par la compétence :\n"

                                if skillToUse.type != TYPE_INVOC:
                                    nbTargetAtRangeSkill = len(targetAtRangeSkill)

                                    for a in range(0,nbTargetAtRangeSkill):
                                        choiceMsgTemp += f"{a} - {targetAtRangeSkill[a].quickEffectIcons()}"
                                        desc = f"PV : {int(targetAtRangeSkill[a].hp/targetAtRangeSkill[a].maxHp*100)}%, Pos : {targetAtRangeSkill[a].cell.x} - {targetAtRangeSkill[a].cell.y}"
                                        if react.area not in [AREA_MONO,AREA_ALL_ALLIES,AREA_ALL_ENNEMIES,AREA_ALL_ENTITES]:
                                            if react.type in ballerine:
                                                wanted = ALLIES
                                            else:
                                                wanted = ENNEMIS
                                            desc += f", Zone : {len(targetAtRangeSkill[a].cell.getEntityOnArea(area=react.area,team=actTurn.team,wanted=wanted))}"
                                        skillOptions += [create_select_option(targetAtRangeSkill[a].char.name,str(a),getEmojiObject(targetAtRangeSkill[a].icon),desc)]
                                    
                                    if react.area in [AREA_ALL_ALLIES,AREA_ALL_ENNEMIES,AREA_ALL_ENTITES] or react.range == AREA_MONO:
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
                                    await choiceMsg.clear_reactions()
                                    await choiceMsg.edit(embed = discord.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = "Dans quelle direction voulez vous aller ?").set_footer(text=f'Fin du tour dans {round(timeLimite)} secondes'))
                                    moveEmoji = ['⬅️','➡️','⬆️','⬇️']
                                    for a in range(0,4):
                                        if canMove[a]:
                                            await choiceMsg.add_reaction(moveEmoji[a])

                                    choiceToMove = None
                                    while choiceToMove == None:
                                        timeLimite = (dateLimite - datetime.datetime.now()).total_seconds()
                                        try:
                                            choiceMove = await bot.wait_for("reaction_add",timeout=timeLimite,check=checkIsPlayerReact)
                                        except:
                                            unsuccess = True
                                            break
                                        for a in range(0,4):
                                            if str(choiceMove[0]) == moveEmoji[a]:
                                                choiceToMove = [surrondings[a].x,surrondings[a].y]
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

                    elif not(actTurn.auto) and not(unsuccess):
                        actTurn.missedLastTurn = False
                
                    if unsuccess or type(ennemi)==int: # Définition des IA
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
                            if b.char.aspiration in [BERSERK,OBSERVATEUR,POIDS_PLUME,TETE_BRULE]:
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

                        if (len(actTurn.cell.getEntityOnArea(area=AREA_CIRCLE_2,team=actTurn.team,wanted=ENNEMIS)) > 0 and (actTurn.char.aspiration not in [BERSERK,OBSERVATEUR,POIDS_PLUME,TETE_BRULE]) and actTurn.char.weapon.range != RANGE_MELEE) or lastDPT or ennemiesdying:
                            choisenIA = AI_OFFERUDIT

                        logs += "\nAuto Fighter. Selected AI : {0}".format(["AI Damage","AI Boost","AI Malus","AI Aventurer","AI Healer","AI agressive supp"][choisenIA])
                        # Définition des probabilités :
                        # [DPT,BOOST,MALUS,AVENTURE,ALTRUISTE,OFFERUt]

                        probaAtkWeap = [70,30,40,30,30,40] 
                        probaHealWeap = [0,70,30,30,80,10]
                        probaIndirectWeap = [20,30,40,30,20,50]
                        probaReaSkill = [50,150,100,30,150,100]
                        probIndirectReacSkill = [30,150,100,30,150,80]
                        probaAtkSkill = [50,40,70,30,40,70]
                        probaIndirectAtkSkill = [30,40,70,30,40,120]
                        probaHealSkill = [30,100,40,30,130,50]
                        probaBoost = [30,130,50,30,70,70]
                        probaMalus = [45,40,100,30,50,70]
                        probaArmor = [35,100,50,30,70,70]

                        # Weapons proba's ----------------------------------
                        if actTurn.char.weapon.name == "noneWeap":
                            probaHealWeap = [0,0,0,0,0,0]
                            probaIndirectWeap = [0,0,0,0,0,0]
                            probaAtkWeap = [0,0,0,0,0,0]
                        else:
                            if actTurn.char.weapon.type == TYPE_DAMAGE:
                                probaHealWeap = [0,0,0,0,0,0]
                                probaIndirectWeap = [0,0,0,0,0,0]
                            elif actTurn.char.weapon.type == TYPE_HEAL:
                                probaAtkWeap = [0,0,0,0,0,0]
                                probaIndirectWeap = [0,0,0,0,0,0]
                            else:
                                probaHealWeap = [0,0,0,0,0,0]
                                probaAtkWeap = [0,0,0,0,0,0]

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
                                probaHealWeap = [0,0,0,0,0,0]
                                probaIndirectWeap = [0,0,0,0,0,0]
                                probaAtkWeap = [0,0,0,0,0,0]
                                logs += "\nSomes offensives skills with targets at range have been found. Weapon's proba neutralized"
                            else:
                                logs += "\nNo available offensives skills have been found"

                        healSkill,atkSkill,reaSkill,indirectReaSkill,indirectAtkSkill,boostSkill,malusSkill,armorSkill,invocSkill = [],[],[],[],[],[],[],[],[]

                        for a in range(0,5): # Catégorisation des sorts
                            actskill = actTurn.char.skills[a]
                            if actTurn.cooldowns[a] == 0 and actskill != None and actskill != "0":
                                if actskill.range == AREA_MONO: # If the skill is launch on self
                                    allieAtRange,ennemiAtRange = len(actTurn.cell.getEntityOnArea(area=actskill.area,team=actTurn.team,wanted=ALLIES,effect=actskill.effect,ignoreInvoc=True))> 0,len(actTurn.cell.getEntityOnArea(area=actskill.area,team=actTurn.team,wanted=ENNEMIS,effect=actskill.effect))> 0
                                    if (actskill.type == TYPE_HEAL or actskill.type == TYPE_INDIRECT_HEAL) and len(actTurn.cell.getEntityOnArea(area=actskill.area,team=actTurn.team,wanted=ALLIES,effect=actskill.effect,lifeUnderPurcentage=90,ignoreInvoc = True))> 0 and (actskill.id != "yt"):
                                        healSkill.append(actskill)
                                    elif actskill.type == TYPE_DAMAGE and ennemiAtRange: # Damage skills
                                        atkSkill.append(actskill)
                                    elif actskill.type == TYPE_RESURECTION: # Resu skills (none lol)
                                        reaSkill.append(actskill)
                                    elif actskill.type == TYPE_INDIRECT_REZ and allieAtRange: # Indirect Resu skills (Zelian R)
                                        indirectReaSkill.append(actskill)
                                    elif actskill.type == TYPE_INDIRECT_DAMAGE and ennemiAtRange: # Indirect damage skills
                                        indirectAtkSkill.append(actskill)
                                    elif actskill.type == TYPE_BOOST and allieAtRange: # Buff skills
                                        boostSkill.append(actskill)
                                    elif actskill.type == TYPE_MALUS and ennemiAtRange: # Debuff skills
                                        malusSkill.append(actskill)
                                    elif actskill.type == TYPE_ARMOR and allieAtRange: # Armor skills
                                        armorSkill.append(actskill)
                                    elif actskill.type == TYPE_UNIQUE: # Other
                                        for b in [chaos]: # Boost
                                            if b == actskill:
                                                boostSkill.append(b)

                                    elif actskill.type == TYPE_INVOC and len(actTurn.cell.getEmptyCellsInArea(area=actskill.range,team=actTurn.team))>0: # Invocation
                                        temp = actTurn.cell.getEmptyCellsInArea(area=actskill.range,team=actTurn.team)
                                        for b in temp[:]:
                                            if actTurn.team == 0:
                                                if b.x > 2:
                                                    temp.remove(b)
                                            elif b.x < 3:
                                                temp.remove(a)                                            

                                        invocSkill.append(actskill)

                                    elif actskill.id == "yt": 
                                        sumHp,sumMaxHp = 0,0
                                        for b in tablEntTeam[actTurn.team]:
                                            sumHp += max(0,b.hp)
                                            sumMaxHp += b.maxHp
                                        if sumHp / sumMaxHp <= 0.5:
                                            healSkill.append(actskill)
                                    
                                else: # The skill is cast on others
                                    allieAtRange,ennemiAtRange = len(actTurn.cell.getEntityOnArea(area=actskill.range,team=actTurn.team,wanted=ALLIES,lineOfSight = True,effect=actskill.effect,ignoreInvoc = True))> 0,len(actTurn.cell.getEntityOnArea(area=actskill.range,team=actTurn.team,wanted=ENNEMIS,lineOfSight = True,effect=actskill.effect))> 0
                                    if (actskill.type == TYPE_HEAL or actskill.type == TYPE_INDIRECT_HEAL) and len(actTurn.cell.getEntityOnArea(area=actskill.range,team=actTurn.team,wanted=ALLIES,lifeUnderPurcentage=90,effect=actskill.effect,ignoreInvoc = True))> 0:
                                        healSkill.append(actskill)
                                    elif actskill.type == TYPE_DAMAGE and ennemiAtRange:
                                        atkSkill.append(actskill)
                                    elif actskill.type == TYPE_RESURECTION and len(actTurn.cell.getEntityOnArea(area=actskill.range,team=actTurn.team,wanted=ALLIES,dead=True)):
                                        reaSkill.append(actskill)
                                    elif actskill.type == TYPE_INDIRECT_REZ and allieAtRange:
                                        indirectReaSkill.append(actskill)
                                    elif actskill.type == TYPE_INDIRECT_DAMAGE and ennemiAtRange:
                                        indirectAtkSkill.append(actskill)
                                    elif actskill.type == TYPE_BOOST and allieAtRange:
                                        boostSkill.append(actskill)
                                    elif actskill.type == TYPE_MALUS and ennemiAtRange:
                                        if actskills not in [boom]: 
                                            malusSkill.append(actskill)
                                        elif actskill == boom: # Si il ne reste qu'un ennemi, ne pas prendre en compte Réaction en chaîne
                                            team2see = tablEntTeam[int(not(actTurn.team))][:]
                                            for b in team2see[:]:
                                                if b.hp <= 0:
                                                    team2see.remove(b)

                                            if len(team2see) > 1:
                                                malusSkill.append(boom)

                                    elif actskill.type == TYPE_ARMOR and allieAtRange:
                                        armorSkill.append(actskill)
                                    elif actskill.type == TYPE_UNIQUE:
                                        for b in [chaos]: # Boost
                                            if b == actskill:
                                                boostSkill.append(b)
                                    
                                    elif actskill.type == TYPE_INVOC and len(actTurn.cell.getEmptyCellsInArea(area=actskill.range,team=actTurn.team))>0:
                                        invocSkill.append(actskill)
                
                        isTMinDanger, isTeamMateDown = False, False
                        for a in tablEntTeam[actTurn.team]:
                            if a.hp / a.maxHp <= 0.35:
                                isTMinDanger = True
                            elif a.hp <= 0:
                                isTeamMateDown = True

                        if not(isTMinDanger):
                            probIndirectReacSkill = [0,0,0,0,0,0]
                        else:
                            probaHealSkill = [30,120,40,50,150,150]

                        if not(isTeamMateDown):
                            probaReaSkill = [0,0,0,0,0,0]

                        probTabl = [probaReaSkill,probIndirectReacSkill,probaAtkSkill,probaIndirectAtkSkill,probaHealSkill,probaBoost,probaMalus,probaArmor]
                        for a in range(0,8):
                            analyse = [reaSkill,indirectReaSkill,atkSkill,indirectAtkSkill,healSkill,boostSkill,malusSkill,armorSkill][a]
                            if len(analyse) == 0:
                                probTabl[a] = [0,0,0,0,0,0]

                        if len(invocSkill) > 0 and tablAliveInvoc[actTurn.team]<3:
                            if actTurn.char.aspiration == AVENTURIER:
                                probaInvoc = [65,65,65,65,65,65]
                            else:
                                probaInvoc = [40,40,40,40,40,40]
                        else:
                            probaInvoc = [0,0,0,0,0,0]

                        totalProba = probaAtkWeap[choisenIA]+probaHealWeap[choisenIA]
                        for a in probTabl:
                            totalProba+= a[choisenIA]
            
                        totalProba += probaIndirectWeap[choisenIA]+probaInvoc[choisenIA] + 1
                        probaRoll = random.randint(0,totalProba) -1
                        logs += "\nTotal Proba : {0} - ProbaRoll : {1}".format(totalProba,probaRoll)

                        optionChoisen = False

                        if probaRoll <= probaAtkWeap[choisenIA] and probaAtkWeap[choisenIA] > 0: #Attaque à l'arme
                            logs += "\nSelected option : Damage with weapon"
                            nearestEnnemi,nearestDistance,myCell,nearestCell = 0,100,actTurn.cell,0
                            if nbTargetAtRange > 0:
                                for a in atRange: # Ennemi le plus proche
                                    if a.team != actTurn.team and a.hp > 0:
                                        if myCell.distance(cell=a.cell) < nearestDistance:
                                            nearestEnnemi, nearestDistance, nearestCell = a,myCell.distance(cell=a.cell),a.cell
                
                                optionChoice,ennemi = OPTION_WEAPON,nearestEnnemi

                            else:
                                logs += "\nNo target at range. Trying to move"
                                for a in tablAllCells: # Ennemi le plus proche
                                    if a.on != None:
                                        b = a.on
                                        if b.team != actTurn.team and b.hp > 0:
                                            if myCell.distance(cell=b.cell) < nearestDistance:
                                                nearestEnnemi, nearestDistance, nearestCell = b,myCell.distance(cell=b.cell),b.cell
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
                                    logs += "\nNo valid cells found. Skipping the turn"
                                    optionChoice=OPTION_SKIP

                            optionChoisen = True
                        else:
                            probaRoll -= probaAtkWeap[choisenIA]

                        if probaRoll <= probaHealWeap[choisenIA] and probaHealWeap[choisenIA] > 0 and not(optionChoisen): #Soins à l'arme
                            mostDamageAllie,mDAHp,Cell,nearestCell = 0,1,actTurn.cell,0
                            logs += "\nSelected option : Heal with weapon"
                            
                            if nbTargetAtRange > 0:
                                for a in atRange: # Allié le blessé
                                    if a.team == actTurn.team and a.hp > 0:
                                        if a.hp/a.maxHp < mDAHp:
                                            mostDamageAllie, mDAHp = a,a.hp/a.maxHp

                                optionChoice,ennemi = OPTION_WEAPON,mostDamageAllie
                                            
                            else:
                                logs += "\nNo target at range. Trying to move"
                                nearestEnnemi, nearestDistance, nearestCell = 0,1,0
                                for a in tablAllCells: # Allié le blessé
                                    if a.on != None:
                                        b = a.on
                                        if b.team == actTurn.team and b.hp > 0 and b.hp/b.maxHp <= 0.9:
                                            if b.hp/b.maxHp < nearestDistance:
                                                nearestEnnemi, nearestDistance, nearestCell = b,b.hp/b.maxHp,b.cell

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
                                    optionChoice=OPTION_SKIP
                                    logs += "\nNo valid cells found. Skipping the turn"

                            optionChoisen = True
                        elif not(optionChoisen):
                            probaRoll -= probaHealWeap[choisenIA]

                        if probaRoll <= probTabl[0][choisenIA] and probTabl[0][choisenIA] > 0 and not(optionChoisen): # Résurection
                            logs += "\nSelected option : Resurection Skill"
                            for a in tablEntTeam[actTurn.team]:
                                if a.hp <= 0:
                                    optionChoice = OPTION_SKILL
                                    if len(reaSkill) > 1:
                                        skillToUse = reaSkill[random.randint(0,len(reaSkill)-1)]
                                    else:
                                        skillToUse = reaSkill[0]
                                    ennemi = a
                                    optionChoisen = true
                                    break
                        
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
                                    optionChoisen = true
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

                            if randomSkill == trans:
                                randomSkill = copy.deepcopy(randomSkill)
                                if actTurn.char.aspiration in [BERSERK,TETE_BRULE,POIDS_PLUME,ERUDIT,OBSERVATEUR]:
                                    randomSkill.type = TYPE_DAMAGE
                                    if actTurn.char.aspiration == BERSERK:
                                        randomSkill.power = 180
                                    else:
                                        randomSkill.power = 135
                                        if randomSkill.type in [TETE_BRULE,POIDS_PLUME]:
                                            randomSkill.area = AREA_LINE_6
                                            randomSkill.range = AREA_MONO
                                        elif randomSkill.type in [ERUDIT,OBSERVATEUR]:
                                            randomSkill.type = CIRCLE_AREA_2
                                    
                            if randomSkill.range != AREA_MONO:
                                nearestEnnemi,nearestDistance,myCell,nearestCell = 0,100,actTurn.cell,0 # Ennemi le plus proche
                                for a in actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ENNEMIS,lineOfSight=True,effect=randomSkill.effect):
                                    if a.team != actTurn.team and a.hp > 0:
                                        if myCell.distance(cell=a.cell) < nearestDistance:
                                            nearestEnnemi, nearestDistance, nearestCell = a,myCell.distance(cell=a.cell),a.cell

                                optionChoice = OPTION_SKILL
                                skillToUse = randomSkill
                                ennemi = nearestEnnemi

                            else:
                                if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,wanted=ENNEMIS)) > 0:
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
                                nearestEnnemi,nearestDistance,myCell,nearestCell = 0,100,actTurn.cell,0 # Ennemi le plus proche
                                for a in actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ENNEMIS,lineOfSight=True,effect=randomSkill.effect):
                                    if a.team != actTurn.team and a.hp > 0:
                                        if myCell.distance(cell=a.cell) < nearestDistance:
                                            nearestEnnemi, nearestDistance, nearestCell = a,myCell.distance(cell=a.cell),a.cell

                                optionChoice = OPTION_SKILL
                                skillToUse = randomSkill
                                ennemi = nearestEnnemi

                            else:
                                if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,wanted=ENNEMIS)) > 0:
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
                                nearestEnnemi,nearestDistance,myCell,nearestCell = 0,100,actTurn.cell,0
                                for a in actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ALLIES,lifeUnderPurcentage=90,effect=randomSkill.effect): # Allié le blessé
                                    if a.team == actTurn.team and a.hp > 0:
                                        if a.hp/a.maxHp < nearestDistance:
                                            nearestEnnemi, nearestDistance, nearestCell = a,a.hp/a.maxHp,a.cell

                                optionChoice = OPTION_SKILL
                                skillToUse = randomSkill
                                ennemi = nearestEnnemi

                            else:
                                if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,wanted=ALLIES,effect=randomSkill.effect)) > 0 or (randomSkill == trans and actTurn.char.aspiration in [ALTRUISTE,IDOLE]):
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

                            if randomSkill.range != AREA_MONO:
                                nearestEnnemi,nearestDistance,myCell,nearestCell,dpt = 0,100,actTurn.cell,0,[]
                                for a in actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ALLIES,lineOfSight=True,effect=randomSkill.effect): # Allié le blessé
                                    if a.char.aspiration in [BERSERK,OBSERVATEUR,POIDS_PLUME,TETE_BRULE]:
                                        dpt.append(a)

                                for a in dpt:
                                    if a.team == actTurn.team and a.hp > 0:
                                        if a.hp/a.maxHp < nearestDistance:
                                            nearestEnnemi, nearestDistance, nearestCell = a,a.hp/a.maxHp,a.cell

                                    optionChoice = OPTION_SKILL
                                    skillToUse = randomSkill
                                    ennemi = nearestEnnemi

                            else:
                                if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,wanted=ALLIES,effect=randomSkill.effect)) > 0:
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
                                nearestEnnemi,nearestDistance,myCell,nearestCell = 0,100,actTurn.cell,0 # Ennemi le plus proche
                                for a in actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ENNEMIS,lineOfSight=True,effect=randomSkill.effect):
                                    if a.team != actTurn.team and a.hp > 0:
                                        if myCell.distance(cell=a.cell) < nearestDistance:
                                            nearestEnnemi, nearestDistance, nearestCell = a,myCell.distance(cell=a.cell),a.cell

                                optionChoice = OPTION_SKILL
                                skillToUse = randomSkill
                                ennemi = nearestEnnemi

                            else:
                                if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,wanted=ENNEMIS,effect=randomSkill.effect)) > 0:
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
                                for a in actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ALLIES,lifeUnderPurcentage=90,effect=randomSkill.effect): # Allié le blessé
                                    if a.team == actTurn.team and a.hp > 0:
                                        if a.hp/a.maxHp < nearestDistance:
                                            nearestEnnemi, nearestDistance, nearestCell = a,a.hp/a.maxHp,a.cell

                                optionChoice = OPTION_SKILL
                                skillToUse = randomSkill
                                ennemi = nearestEnnemi

                            else:
                                if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,wanted=ALLIES,effect=randomSkill.effect)) > 0:
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
                                for a in atRange: # Ennemi le plus proche
                                    if a.team != actTurn.team and a.hp > 0:
                                        if myCell.distance(cell=a.cell) < nearestDistance:
                                            nearestEnnemi, nearestDistance, nearestCell = a,myCell.distance(cell=a.cell),a.cell
                
                                optionChoice,ennemi = OPTION_WEAPON,nearestEnnemi

                            else:
                                for a in tablAllCells: # Ennemi le plus proche
                                    if a.on != None:
                                        b = a.on
                                        if b.team != actTurn.team and b.hp > 0:
                                            if myCell.distance(cell=b.cell) < nearestDistance:
                                                nearestEnnemi, nearestDistance, nearestCell = b,myCell.distance(cell=b.cell),b.cell
                                
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

                    if type(ennemi) == int:
                        logs += "\nNo target have been found. Skipping the turn"
                        optionChoice = OPTION_SKIP

                    if optionChoice == OPTION_WEAPON: #Option : Attaque
                        if actTurn.char.weapon.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]: # Agressive Weapon
                            logs += "\n{0} is attacking {1} with their weapon\n".format(actTurn.char.name,ennemi.char.name)
                            cmpt = 0
                            while cmpt < iteration:
                                isAlive = ennemi.hp > 0
                                if not(isAlive) :
                                    break
                                if actTurn.char.weapon.message == None:
                                    tempTurnMsg += f"\n__{actTurn.char.name} attaque {ennemi.char.name} avec son arme :__\n"
                                else:
                                    tempTurnMsg += "\n__"+actTurn.char.weapon.message.format(actTurn.char.name,ennemi.char.name)+"__\n"
                                
                                ballerine = actTurn.attack(target=ennemi,value=actTurn.char.weapon.power,icon=actTurn.char.weapon.emoji,area=actTurn.char.weapon.area,use=actTurn.char.weapon.use,onArmor=actTurn.char.weapon.onArmor)
                                logs+= ballerine
                                tempTurnMsg += ballerine
                                cmpt += 1

                                if actTurn.char.weapon.effectOnUse != None:
                                    ballerine = add_effect(actTurn,ennemi,findEffect(actTurn.char.weapon.effectOnUse))
                                    logs+= ballerine
                                    tempTurnMsg += ballerine

                                    for a in hourglassEffects:
                                        if a == findEffect(actTurn.char.weapon.effectOnUse):
                                            add_effect(actTurn,ennemi,jetlag.setTurnInit(newTurn = 2))
                                            break
                                    ennemi.refreshEffect()
                                            
                        elif actTurn.char.weapon.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL]: # None agressive Weapon
                            logs += "\n\n{0} is healing {1} with their weapon".format(actTurn.char.name,ennemi.char.name)
                            if actTurn.char.weapon.message == None:
                                tempTurnMsg += f"\n__{actTurn.char.name} soigne {ennemi.char.name} avec son arme :__\n"
                            else:
                                tempTurnMsg += "\n__"+actTurn.char.weapon.message.format(actTurn.char.name,ennemi.char.name)+"__\n"

                            for a in ennemi.cell.getEntityOnArea(area=actTurn.char.weapon.area,team=actTurn.team,wanted=ALLIES):
                                healPowa = min(a.maxHp-a.hp,round(actTurn.char.weapon.power * (1+actTurn.charisma/100)* actTurn.valueBoost(target=a,heal=True)* actTurn.getElementalBonus(a,area = AREA_MONO,type = TYPE_HEAL)))
                                healPowa = round(healPowa * ((100-a.healResist)/100))
                                a.healResist += int(healPowa/a.maxHp/2*100)
                                a.hp += healPowa
                                actTurn.stats.heals += healPowa
                                ballerine = f"{actTurn.icon} {actTurn.char.weapon.emoji} → {a.icon} +{healPowa} PV\n"
                                logs+= ballerine + ". {0}'s healing resist : +{1}".format(a.char.name,int(healPowa/a.maxHp/2*100))
                                tempTurnMsg += ballerine

                            if actTurn.char.weapon.effectOnUse != None:
                                ballerine = add_effect(actTurn,ennemi,findEffect(actTurn.char.weapon.effectOnUse))
                                logs+= ballerine
                                tempTurnMsg += ballerine

                                for a in hourglassEffects:
                                    if a == findEffect(actTurn.char.weapon.effectOnUse):
                                        add_effect(actTurn,ennemi,jetlag.setTurnInit(newTurn = 2))
                                        break
                                ennemi.refreshEffect()

                        elif actTurn.char.weapon.effectOnUse != None: # Other weapons
                            logs += "\n\n{0} is using their weapon on {1}".format(actTurn.char.name,ennemi.char.name)
                            tempTurnMsg += f"\n__{actTurn.char.name} utilise son arme sur {ennemi.char.name} :__\n"
                            ballerine = add_effect(actTurn,ennemi,findEffect(actTurn.char.weapon.effectOnUse))
                            logs+= ballerine
                            tempTurnMsg += ballerine

                            for a in hourglassEffects:
                                if a == findEffect(actTurn.char.weapon.effectOnUse):
                                    add_effect(actTurn,ennemi,jetlag.setTurnInit(newTurn = 2))
                                    break
                            ennemi.refreshEffect()

                    elif optionChoice == OPTION_MOVE: #Option : Déplacement
                        logs += "\n\n{0} is moving".format(actTurn.char.name)
                        temp = actTurn.cell
                        actTurn.move(x=choiceToMove[0],y=choiceToMove[1])
                        logs += "\n{0} have been moved from {1}:{2} to {3}:{4}".format(actTurn.char.name,temp.x,temp.y,choiceToMove[0],choiceToMove[1])
                        tempTurnMsg+= "\n"+actTurn.char.name+" se déplace\n"

                    elif optionChoice == OPTION_SKIP: #Passage de tour
                        logs += "\n\n{0} is skipping their turn".format(actTurn.char.name)
                        tempTurnMsg += f"\n{actTurn.char.name}  passe son tour\n"

                    elif optionChoice == OPTION_SKILL: #Skill :(
                        logs += "\n\n{0} is using {1} on {2}".format(actTurn.char.name,skillToUse.name,ennemi.char.name)
                        if skillToUse.message == None:
                            tempTurnMsg += f"\n__{actTurn.char.name} utilise la compétence {skillToUse.name} :__\n"
                        else: 
                            tempTurnMsg += "\n__"+ skillToUse.message.format(actTurn.char.name,skillToUse.name,ennemi.char.name)+"__\n"
                        trouv=False
                        for a in range(0,5):
                            if type(actTurn.char.skills[a]) == skill:
                                if skillToUse.id == actTurn.char.skills[a].id:
                                    actTurn.cooldowns[a] = skillToUse.cooldown
                                    trouv=True
                                if skillToUse.id == "yt" and actTurn.char.skills[a].ultimate and actTurn.cooldowns[a] < 2:
                                    actTurn.cooldowns[a] = 2
                        
                        if skillToUse.shareCooldown :
                            for a in tablEntTeam[actTurn.team]:
                                for b in range(0,len(a.char.skills)):
                                    if type(a.char.skills[b]) == skill:
                                        if a.char.skills[b].id == skillToUse.id:
                                            a.cooldowns[b] = skillToUse.cooldown
                        
                        if not(trouv):
                            print("Capacitée non trouvée !!")
                            print(skillToUse.name,skillToUse.id)
                            for a in range(0,5):
                                if type(actTurn.char.skills[a]) == skill:
                                    print(actTurn.char.skills[a].name,actTurn.char.skills[a].id)

                        played = False
                        if skillToUse.type in [TYPE_BOOST,TYPE_ARMOR,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ]:
                            for b in ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES):
                                for c in skillToUse.effect:
                                    effect = findEffect(c)
                                    tempTurnMsg += add_effect(actTurn,b,effect)
                                    logs += "{0} gave the {1} effect at {2} for {3} turns\n".format(actTurn.char.name,effect.name,b.char.name,effect.turnInit)
                                b.refreshEffect()
                            played=True

                        if not(played) and skillToUse.type in [TYPE_INDIRECT_DAMAGE,TYPE_MALUS]:
                            for y in skillToUse.effect:
                                for b in ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENNEMIS):
                                    effect = findEffect(y)
                                    tempTurnMsg += add_effect(actTurn,b,effect)
                                    logs += "\n{0} gave the {1} effect at {2} for {3} turns".format(actTurn.char.name,effect.name,b.char.name,effect.turnInit)
                                b.refreshEffect()
                            played=True

                        if not(played) and skillToUse.type == TYPE_HEAL:
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

                                if skillToUse.id != "yt": # Any normal healing skill
                                    healPowa = min(ennemi.maxHp-ennemi.hp,round(skillToUse.power * (1+statUse/100)* actTurn.valueBoost(target = ennemi,heal=True)*actTurn.getElementalBonus(a,area = AREA_MONO,type = TYPE_HEAL)))
                                    for a in ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES):
                                        healPowa = round(healPowa * ((100-a.healResist)/100))
                                        a.healResist += int(healPowa/a.maxHp/2*100)
                                        actTurn.stats.heals += healPowa
                                        a.hp += healPowa
                                        ballerine = f"{actTurn.icon} {skillToUse.emoji}→ {a.icon} +{healPowa} PV\n"
                                        logs+= ballerine + ". {0}'s healing resist : +{1}".format(a.char.name,int(healPowa/a.maxHp/2*100))
                                        tempTurnMsg += ballerine
                                    played=True
                                else: # Limitebreak Heal
                                    for a in range(0,len(tablEntTeam[actTurn.team])):
                                        if tablEntTeam[actTurn.team][a].hp > 0:
                                            healPowa = min(tablEntTeam[actTurn.team][a].maxHp-tablEntTeam[actTurn.team][a].hp,round(skillToUse.power * (1+statUse/100)* actTurn.valueBoost(target = tablEntTeam[actTurn.team][a],heal=True)*actTurn.getElementalBonus(a,area = AREA_MONO,type = TYPE_HEAL)))
                                            healPowa = round(healPowa * ((100-tablEntTeam[actTurn.team][a].healResist)/100))
                                            tablEntTeam[actTurn.team][a].healResist += int(healPowa/tablEntTeam[actTurn.team][a].maxHp/2*100)
                                            actTurn.stats.heals += healPowa
                                            tablEntTeam[actTurn.team][a].hp += healPowa
                                            ballerine = f"{actTurn.icon} {skillToUse.emoji}→ {tablEntTeam[actTurn.team][a].icon} +{healPowa} PV\n"
                                            logs+= ballerine + ". {0}'s healing resist : +{1}".format(tablEntTeam[actTurn.team][a].char.name,int(healPowa/tablEntTeam[actTurn.team][a].maxHp/2*100))
                                            tempTurnMsg += ballerine
                                        elif tablEntTeam[actTurn.team][a].status == STATUS_DEAD:
                                            healPowa = min(tablEntTeam[actTurn.team][a].maxHp,round(skillToUse.power * (1+statUse/100)* actTurn.valueBoost(target = tablEntTeam[actTurn.team][a],heal=True)*0.3))
                                            actTurn.stats.allieResurected += 1
                                            actTurn.stats.heals += healPowa
                                            tablEntTeam[actTurn.team][a].healResist += int(healPowa/tablEntTeam[actTurn.team][a].maxHp/2*100)
                                            tablEntTeam[actTurn.team][a].hp = healPowa
                                            tablEntTeam[actTurn.team][a].status = STATUS_RESURECTED
                                            if type(tablEntTeam[actTurn.team][a].char) == octarien:
                                                tablEntTeam[actTurn.team][a].icon = tablEntTeam[actTurn.team][a].char.icon
                                            elif type(tablEntTeam[actTurn.team][a].char) == tmpAllie:
                                                tablEntTeam[actTurn.team][a].icon = emoji.icon[tablEntTeam[actTurn.team][a].char.species][getColorId(tablEntTeam[actTurn.team][a].char)]
                                            else:
                                                tablEntTeam[actTurn.team][a].icon = await getUserIcon(bot,tablEntTeam[actTurn.team][a].char)

                                            add_effect(actTurn,tablEntTeam[actTurn.team][a],onceButNotTwice)
                                            tempTurnMsg += f"{tablEntTeam[actTurn.team][a].char.name} est ressucité{tablEntTeam[actTurn.team][a].accord()} !\n"
                                            ballerine = f"{actTurn.icon} {skillToUse.emoji}→ {tablEntTeam[actTurn.team][a].icon} +{healPowa} PV\n"
                                            tempTurnMsg += ballerine
                                            logs += "\n{0} have been resurected. "+ballerine
                                    played=True

                        if not(played) and skillToUse.type == TYPE_INVOC:
                            summoned = actTurn.summon(findInvoc(skillToUse.invocation),time,actTurn.cell.getCellForSummon(skillToUse.range,actTurn.team,findInvoc(skillToUse.invocation),actTurn),tablEntTeam,tablAliveInvoc)
                            tempTurnMsg += summoned["text"]+"\n"
                            logs += "\n"+summoned["text"]
                            time = summoned["timeline"]
                            tablEntTeam = summoned["tablEntTeam"]
                            tablAliveInvoc = summoned["tablAliveInvoc"]
                            played = True

                        if skillToUse.type == TYPE_UNIQUE:
                            if skillToUse == chaos:
                                chaosTabl = effects[:]
                                for a in chaosTabl[:]:
                                    if a in chaosProhib:
                                        chaosTabl.remove(a)

                                lenChaos = len(chaosTabl)-1
                                for a in [0,1]:
                                    for b in tablEntTeam[a]:
                                        if b.hp > 0:
                                            tempTurnMsg += add_effect(actTurn,b,chaosTabl[random.randint(0,lenChaos)])
                                            b.refreshEffect()
                                played = True

                        if not(played):
                            ballerine = actTurn.attack(target=ennemi,value=skillToUse.power,icon=skillToUse.emoji,area=skillToUse.area,sussess=skillToUse.sussess,use=skillToUse.use,onArmor=skillToUse.onArmor)
                            tempTurnMsg += ballerine
                            logs += "\n"+ballerine

                        if skillToUse.effectOnSelf != None:
                            tempTurnMsg += add_effect(actTurn,actTurn,findEffect(skillToUse.effectOnSelf))
                            actTurn.refreshEffect()

                else:
                    end = actTurn.accord()
                    if end != "e":
                        end = "s"

                    tempTurnMsg += f"\n{actTurn.char.name} est étourdi{end} !\n"

                tempTurnMsg += "\n__Fin du tour__\n"
                tempTurnMsg += actTurn.endOfTurn()
                if not(auto):
                    await turnMsg.edit(embed = discord.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color))
                    await asyncio.sleep(2+(len(tempTurnMsg)/1000)*5)
            
            eot = time.endOfTurn(tablEntTeam,tablAliveInvoc)
            tablAliveInvoc = eot["tablAliveInvoc"]
            tablEntTeam = eot["tablEntTeam"]

            for c in [0,1]:
                for d in tablEntTeam[c]:
                    if d.hp > 0 and type(d.char) != invoc:
                        everyoneDead[c] = False
                        break

            if everyoneDead[0] or everyoneDead[1]:
                fight = False
        
        # Fin du combat
        logs += "\n\n=================\nEnd of the fight"
    except:
        team = team1[0].team
        teamWinDB.changeFighting(team,False)
        logs += "\n"+format_exc()
        date = datetime.datetime.now()
        date = date.strftime("%H_%M")
        fich = open("./data/{0}_{1}.txt".format(ctx.author.name,date),"w")
        if not(isLenapy):
            fich.write(logs.replace('\u2192','prohibited'))
        else:
            fich.write(logs)
        fich.close()
        opened = open("./data/{0}_{1}.txt".format(ctx.author.name,date),"rb")

        try:
            await ctx.send("Une erreur est survenue durant le combat",file=discord.File(fp=opened))
        except:
            await msg.channel.send("Une erreur est survenue durant le combat",file=discord.File(fp=opened))

        opened.close()
        os.remove("./data/{0}_{1}.txt".format(ctx.author.name,date))
        haveError = True

    if not(haveError):
        print(ctx.author.name + " a fini son combat")

        for a in range(0,len(tablEntTeam[0])):
            if type(tablEntTeam[0][a].char) == char:
                tablEntTeam[0][a].char = loadCharFile(absPath + "/userProfile/" + str(tablEntTeam[0][a].char.owner) + ".prof",ctx)

        for a in range(0,len(tablEntTeam[1])):
            if type(tablEntTeam[1][a].char) == char:
                tablEntTeam[1][a].char = loadCharFile(absPath + "/userProfile/" + str(tablEntTeam[1][a].char.owner) + ".prof",ctx)
            
        winners = int(not(everyoneDead[1]))
        if not(octogone and type(team2[0])==tmpAllie and team2[0].name=='Lena' and len(team2) == 1 and not(winners)):
            for z in (0,1):
                for a in tablEntTeam[z]:
                    if type(a.char) == invoc:
                        a.hp = 0

            eot = time.endOfTurn(tablEntTeam,tablAliveInvoc)
            tablAliveInvoc = eot["tablAliveInvoc"]
            tablEntTeam = eot["tablEntTeam"]

            temp = tablEntTeam[:]
            temp = temp[0]+temp[1]

            dptClass = sorted(temp,key=lambda student: student.stats.damageDeal,reverse=True)
            for a in dptClass:
                if a.stats.damageDeal < 1:
                    dptClass.remove(a)
            healClass = sorted(temp,key=lambda student: student.stats.heals,reverse=True)
            for a in healClass:
                if a.stats.heals < 1:
                    healClass.remove(a)
            shieldClass = sorted(temp,key=lambda student: student.stats.shieldGived,reverse=True)
            for a in shieldClass:
                if a.stats.shieldGived < 1:
                    shieldClass.remove(a)

            listClassement = [dptClass,healClass,shieldClass]

            if not(octogone):
                teamWinDB.addResultToStreak(team1[0],everyoneDead[1])
            team = team1[0].team
            if team == 0:
                team = team1[0].owner
            if isLenapy and not(octogone):
                teamWinDB.refreshFightCooldown(team,auto)
            if not(octogone):
                teamWinDB.changeFighting(team,False)

            temp= ["",""]
            for a in [0,1]:
                for b in tablEntTeam[a]:
                    temp[a] += f"{b.icon} {b.char.name}{b.getMedals(listClassement)}\n"

            temp1 = discord.Embed(title = "__Résultats du combat :__",color = [0x2996E5,red][winners])
            temp1.add_field(name="__Vainqueurs :__",value=temp[winners],inline=True)
            temp1.add_field(name="Perdants :",value=temp[not(winners)],inline=True)
            
            if not(octogone):
                gainExp, gainCoins, allOcta,gainMsg = 0,tour*10,True,""
                for a in tablEntTeam[1]:
                    if type(a.char) == octarien:
                        gainExp += a.char.exp
                    elif type(a.char) == tmpAllie:
                        gainExp += 5
                    else:
                        allOcta = False

                truc = 0
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
                        if random.randint(0,99) < 20 and allOcta:
                            drop = listAllBuyableShop[:]
                            temp = drop[:]
                            
                            for b in drop:
                                if a.char.have(obj=b):
                                    temp.remove(b)

                            if len(temp) > 0 and not(winners):
                                rand = temp[random.randint(0,len(temp)-1)]
                                newTemp = whatIsThat(rand)

                                if newTemp == 0:
                                    a.char.weaponInventory += [rand]
                                elif newTemp == 1:
                                    a.char.skillInventory += [rand]
                                elif newTemp == 2:
                                    a.char.stuffInventory += [rand]

                                saveCharFile(path,a.char)
                                gainMsg += f"{await getUserIcon(bot,a.char)} → {rand.emoji} {rand.name}\n"

                            elif len(temp) == 0:
                                print(f"{a.char.name} a looté un truc mais a déjà tout")

                temp1.add_field(name="<:empty:866459463568850954>\n__Gains de l'équipe joueur :__",value = gainMsg,inline=False)
        else:
            temp1 = discord.Embed(title = "on_message",color=red,description="Une erreur est survenue :)\nUn rapport d'erreur n'a pas été envoyé")

        if not(auto):
            await turnMsg.delete()
            if not(allAuto):
                await choiceMsg.delete()
            await msg.edit(embed = temp1,components=[])
        else:
            if slash:
                msg = await ctx.send(embed = temp1,components=[])
            else:
                msg = await ctx.channel.send(embed = temp1,components=[])

        # ------------ Succès -------------- #
        if not(octogone):
            isAlice = False
            isClemence = False
            isAkira = False
            isGwen = False
            isHelene = False

            for a in [0,1]:
                for b in tablEntTeam[a]:
                    if type(b.char) == tmpAllie:
                        if b.char.name == "Alice":
                            isAlice = True
                        elif b.char.name == "Clémence":
                            isClemence = True
                        elif b.char.name == "Akira":
                            isAkira = True
                        elif b.char.name in ["Gwendoline","Altikia","Klironovia"]:
                            isGwen = True
                        elif b.char.name == "Hélène":
                            isHelene = True

            for a in [0,1]:
                for b in tablEntTeam[a]:
                    if type(b.char) == char:
                        achivements = achivement.getSuccess(b.char)
                        if not(b.auto): # Ivresse du combat
                            b.char = await achivements.addCount(ctx,b.char,"fight")

                        if isAlice: # Souvenez vous que chaque roses a des épines
                            b.char = await achivements.addCount(ctx,b.char,"alice")
                        if isClemence: # La quête de la nuit
                            b.char = await achivements.addCount(ctx,b.char,"clemence")
                        if isAkira: # Seconde impression
                            b.char = await achivements.addCount(ctx,b.char,"akira")
                        if isGwen: # Une histoire de vangeance
                            b.char = await achivements.addCount(ctx,b.char,"gwen")
                        if isHelene: # Là où mes ailes me porteront
                            b.char = await achivements.addCount(ctx,b.char,"helene")

                        if auto and int(ctx.author.id) == int(b.char.owner): # Le temps c'est de l'argent
                            b.char = await achivements.addCount(ctx,b.char,"quickFight")

                        # Je ne veux pas d'écolière pour défendre nos terres
                        b.char = await achivements.addCount(ctx,b.char,"school")

                        # Elementaire
                        if b.char.level >= 10:
                            b.char = await achivements.addCount(ctx,b.char,"elemental")

                        # Soigneur de compette
                        b.char = await achivements.addCount(ctx,b.char,"greatHeal",b.stats.heals)

                        # Situation désespérée
                        if b.char.aspiration not in [ALTRUISTE,ERUDIT,IDOLE]:
                            b.char = await achivements.addCount(ctx,b.char,"notHealBut",b.stats.heals)

                        # La meilleure défense c'est l'attaque
                        b.char = await achivements.addCount(ctx,b.char,"greatDps",b.stats.damageDeal-b.stats.indirectDamageDeal)

                        # Notre pire ennemi c'est nous même
                        b.char = await achivements.addCount(ctx,b.char,"poison",b.stats.indirectDamageDeal)

                        saveCharFile(absPath + "/userProfile/"+str(b.char.owner)+".prof",b.char)

        await msg.add_reaction(emoji.plus)
        await msg.add_reaction('📄')
        timeout = False
        def checkIsPlusReact(reaction,user):
            return user.id != bot.user.id and reaction.message.id == msg.id and (str(reaction) in [emoji.plus,'📄'])
        while 1:
            try:
                react = await bot.wait_for("reaction_add",timeout=60,check=checkIsPlusReact)
            except:
                await msg.clear_reactions()
                break

            if str(react[0]) == '📄':
                date = datetime.datetime.now()
                date = date.strftime("%H_%M")
                fich = open("./data/{0}_{1}.txt".format(ctx.author.name,date),"w")
                if not(isLenapy):
                    fich.write(logs.replace('\u2192','prohibited'))
                else:
                    fich.write(logs)
                fich.close()
                opened = open("./data/{0}_{1}.txt".format(ctx.author.name,date),"rb")
                if slash:
                    await msg.channel.send("Voici les logs du combat :",file=discord.File(fp=opened))

                opened.close()
                os.remove("./data/{0}_{1}.txt".format(ctx.author.name,date))
                await msg.clear_reaction('📄')

            elif str(react[0]) == emoji.plus:
                await msg.clear_reaction('📄')
                if not(slash):
                    msgStats = await loadingEmbed(ctx)
                else:
                    msgStats = await loadingSlashEmbed(ctx)

                tablReaction = ['⏪',emoji.backward_arrow,emoji.forward_arrow,'⏩']
                actuTeam = 0
                actuEntity = 0
                def checkIsReact(reaction,user):
                    temp = False
                    for a in tablReaction:
                        if str(reaction)==a:
                            temp=True
                            break
                    return user != bot.user and reaction.message == msgStats and temp
    
                while 1: # Tableau des statistiques
                    actu = tablEntTeam[actuTeam][actuEntity]
                    stats = actu.stats

                    if type(actu.char) == char:
                        userIcon = await getUserIcon(bot,actu.char)
                    else:
                        userIcon = actu.char.icon

                    statsEm = discord.Embed(title = "__Statistiques de "+ userIcon +" "+actu.char.name+"__",color=actu.char.color)
                    ballerine =[[stats.ennemiKill,stats.damageDeal,stats.indirectDamageDeal,stats.damageOnShield,stats.damageBoosted],[stats.allieResurected,stats.heals,stats.damageDogded,stats.shieldGived],[stats.survival,stats.damageRecived,round(stats.shootHited/stats.totalNumberShot*100),round(stats.dodge/stats.numberAttacked*100),round(stats.crits/stats.totalNumberShot*100)]]
                    babie = [["Ennemis tués :","Dégâts infligés :","Dont indirects :","Dégâts sur armure :","Dégâts Boostés :"],["Alliés ressucités :","Soins effectués :","Dégâts réduits :","Armure fournie :"],["Tours survécus :","Dégâts reçus :","Taux de précision : ","Taux d'esquive :","Taux de coup critique :"]]
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
                        statsEm.add_field(name=sneaker[a],value=statMsg+"\n<:empty:866459463568850954>",inline = False)
                    await msgStats.edit(embed = statsEm)

                    for a in tablReaction:
                        await msgStats.add_reaction(a)

                    try:
                        react = await bot.wait_for("reaction_add",timeout = 60,check = checkIsReact)
                        reaction = react
                    except:
                        break

                    for a in [0,1,2,3]:
                        if str(react[0]) == tablReaction[a]:
                            react = a
                            break

                    if react == 0:
                        actuTeam,actuEntity = 0,0
                    elif react == 1:
                        if actuEntity == 0:
                            actuTeam = int(not(actuTeam))
                            actuEntity = len(tablEntTeam[actuTeam])-1
                        else:
                            actuEntity -= 1
                    elif react == 2:
                        if actuEntity == len(tablEntTeam[actuTeam])-1:
                            actuTeam = int(not(actuTeam))
                            actuEntity = 0
                        else:
                            actuEntity += 1
                    elif react == 3:
                        actuTeam,actuEntity = 1,0
                
                    await msgStats.remove_reaction(str(reaction[0]),reaction[1])

                break
                await msgStats.clear_reactions()
        
        await msg.clear_reactions()
        try:
            await msgStats.clear_reations()
        except:
            pass