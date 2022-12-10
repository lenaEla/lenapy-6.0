from commands_files.command_fight_add import *
from socket import error as SocketError
import errno

async def fight(bot : interactions.Client , team1 : list, team2 : list ,ctx : interactions.CommandContext, auto:bool = True,contexte:fightContext=fightContext(),octogone:bool=False,bigMap:bool=False, procurFight = False, msg=None, teamSettings:dict=None, testFight = False, waitEnd = True):
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
            user = loadCharFile("./userProfile/{0}.prof".format(ctx.author.id))
            team1[0].owner = user.owner
            team1[0].team = user.team
        now, mainUser, skillToUse = datetime.now(), None, None
        teamJaugeDict, teamHealReistMul, teamArmorReducer, deplTabl = [{},{}], [1,1], [1,1], []

        for user in team1:
            if int(user.owner) == int(ctx.author.id):
                mainUser = user
                break

        if mainUser == None:
            mainUser = team1[0]

        # Base vars declalation
        listImplicadTeams, listFasTeam, tablAllieTemp, enableMiror, footerText, playOfTheGame, logs, haveError, dangerLevel, errorNb, optionChoice, kikuExect = [mainUser.team], [[],[]], copy.deepcopy(tablAllAllies), True, "", [1500,None,None], "[{0}]\n".format(now.strftime("%H:%M:%S, %d/%m/%Y")),False, [65,70,75,80,85,90,100,110,120,135,150], 0, None, False

        # dictIsNpcVar creation
        dictIsNpcVar = copy.deepcopy(primitiveDictIsNpcVar)

        print(ctx.author.name + " a lancé un combat")
        cmpt,tablAllCells,tour,danger,tablAliveInvoc,longTurn,longTurnNumber,haveMultipleHealers, oneVAll = 0,[],0,100,[0,0],False,[], [False,False], False

        for a in [0,1,2,3,4,5]:             # Creating the board
            for b in [[0,1,2,3,4],[0,1,2,3,4,5,6]][bigMap]:
                tablAllCells += [cell(a,b,cmpt,tablAllCells)]
                cmpt += 1

        allEffectInFight = []
        addEffect,tablEntTeam, ressurected = [],[],[[],[]]

        class entity:
            """Base class for the entities"""
            def __init__(self,identifiant : int, perso : Union[char,tmpAllie,octarien,invoc,depl], team : int, player=True, auto=True, danger=100,summoner=None,dictInteraction:dict=None, cell=None):
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
                self.chained = False
                self.leftTurnAlive = 999
                if type(self.char) == invoc:
                    self.leftTurnAlive = 3
                elif type(self.char) == depl:
                    self.leftTurnAlive = self.char.lifeTime
                    self.char.element, self.char.secElement, self.char.aspiration, self.char.level, self.char.stars = summoner.char.element, summoner.char.secElement, summoner.char.aspiration, summoner.char.level, summoner.char.stars
                    self.char.species = summoner.char.species

                if not(self.char.isNpc("Kiku") or self.char.isNpc("Zombie")):
                    self.status = STATUS_ALIVE
                else:
                    self.status = STATUS_RESURECTED

                if type(perso) not in [invoc, depl]:
                    self.icon = perso.icon
                else:
                    self.icon = perso.icon[team]

                self.stun = False
                self.summoner = summoner
                self.silent = False
                if not(self.char.isNpc("Kiku")):
                    self.raiser = None
                else:
                    self.raiser = self.icon
                self.specialVars = {"osPro":False,"osPre":False,"osIdo":False,"ohAlt":False,"ohPro":False,"ohIdo":False,"heritEstial":False,"heritLesath":False,"haveTrans":False,"tankTheFloor":False,"clemBloodJauge":None,"clemMemCast":False,"aspiSlot":None,"damageSlot":None,"summonerMalus":False,"finalTech":False,"foullee":False,"partner":None,"preci":False,"ironHealth":False,"fascination":None,"liaBaseDodge":False,"convicVigil":None,"convicPro":None,"exploHeal":False}

                if self.char.aspiration in [OBSERVATEUR, POIDS_PLUME]:
                    self.specialVars["aspiSlot"] = 0
                if type(perso) not in [invoc,octarien]:
                    baseHP,HPparLevel = 130,15
                elif type(perso) == invoc:
                    baseHP, HPparLevel, perso.level = 70, 8, summoner.char.level
                elif not(perso.oneVAll):
                    baseHP,HPparLevel = 90,10
                elif type(self.char) == depl:
                    baseHP,HPparLevel = 9999999,999
                else:
                    baseHP,HPparLevel = 500,115

                self.effects: List[fightEffect] = []
                self.ownEffect = []
                self.cell = cell

                self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie = 0,0,0,0,0,0,0
                self.resistance,self.percing,self.critical = 0,0,0
                self.negativeHeal, self.negativeBoost, self.negativeShield, self.negativeDirect, self.negativeIndirect = 0,0,0,0,0
                self.ressurectable = False
                self.cooldowns = [0,0,0,0,0,0,0]

                if type(self.char) != depl: # Skill Verif
                    for a in [0,1,2,3,4,5,6]:
                        if type(self.char.skills[a]) == skill:
                            if self.char.skills[a].id == mageUlt.id:
                                if self.char.element in [ELEMENT_FIRE,ELEMENT_AIR,ELEMENT_SPACE]:
                                    temp = mageUltZone
                                elif self.char.element in [ELEMENT_WATER,ELEMENT_EARTH,ELEMENT_TIME]:
                                    temp = mageUltMono
                                else:
                                    temp = mageUlt

                                self.char.skills[a] = temp

                            elif self.char.skills[a].id == finalTech.id:
                                self.specialVars["finalTech"] = True
                            
                            if self.char.element == ELEMENT_SPACE:
                                for cmpt in range(len(horoSkills)):
                                    if self.char.skills[a] == horoSkills[cmpt]:
                                        self.char.skills[a] = altHoroSkillsTabl[cmpt]
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
                if type(self.char) != depl:
                    self.level = self.char.level
                else:
                    self.level = summoner.level
                self.dmgUp, self.critDmgUp, self.healUp, self.critHealUp = 0,0,0,0
                self.dodge = 0

                finded = False
                self.IA = AI_AVENTURE

                if self.char.aspiration in [BERSERK,OBSERVATEUR,POIDS_PLUME,TETE_BRULE,ATTENTIF]:
                    self.IA = AI_DPT

                elif self.char.aspiration in [IDOLE,INOVATEUR,MASCOTTE]:
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
                    offSkill,SuppSkill,healSkill,armorSkill,invocSkill, tablAllSkills = 0,0,0,0,0, [self.char.weapon]
                    if type(self.char) == depl:
                        tablAllSkills.append(self.char.skills)
                    else:
                        tablAllSkills = tablAllSkills + self.char.skills
                    for b in tablAllSkills:
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

                if type(self.char) not in [invoc, depl]:
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

                elif type(self.char) == invoc:
                    actionsStats = 0
                    for actStats in [summoner.baseStats[ACT_HEAL_FULL],summoner.baseStats[ACT_BOOST_FULL],summoner.baseStats[ACT_SHIELD_FULL],summoner.baseStats[ACT_DIRECT_FULL],summoner.baseStats[ACT_INDIRECT_FULL]]:
                        actionsStats = max(actionsStats,actStats)
                    actionsStats = int(actionsStats*0.7)
                    baseStats = {STRENGTH:self.char.majorPoints[0],ENDURANCE:self.char.majorPoints[1],CHARISMA:self.char.majorPoints[2],AGILITY:self.char.majorPoints[3],PRECISION:self.char.majorPoints[4],INTELLIGENCE:self.char.majorPoints[5],MAGIE:self.char.majorPoints[6],RESISTANCE:self.char.majorPoints[7],PERCING:self.char.majorPoints[8],CRITICAL:self.char.majorPoints[9],10:actionsStats,11:actionsStats,12:actionsStats,13:actionsStats,14:actionsStats}
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
                
                else:
                    baseStats = summoner.baseStats
                    baseStats[ACT_HEAL_FULL] = baseStats[ACT_BOOST_FULL] = baseStats[ACT_SHIELD_FULL] = baseStats[ACT_DIRECT_FULL] = baseStats[ACT_INDIRECT_FULL] = int(max(summoner.baseStats[ACT_HEAL_FULL],summoner.baseStats[ACT_BOOST_FULL],summoner.baseStats[ACT_SHIELD_FULL],summoner.baseStats[ACT_DIRECT_FULL],summoner.baseStats[ACT_INDIRECT_FULL])*0.7)

                if self.char.element in [ELEMENT_FIRE, ELEMENT_UNIVERSALIS_PREMO]:
                    baseStats[7] += 5
                elif self.char.element in [ELEMENT_WATER, ELEMENT_UNIVERSALIS_PREMO]:
                    baseStats[PRECISION] += 10
                elif self.char.element in [ELEMENT_AIR, ELEMENT_UNIVERSALIS_PREMO]:
                    baseStats[AGILITY] += 10
                elif self.char.element in [ELEMENT_EARTH, ELEMENT_UNIVERSALIS_PREMO]:
                    baseStats[6] += 5

                valueToBoost =  min(1,self.level / 50)
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
                elif self.char.aspiration in [PROTECTEUR,VIGILANT,ENCHANTEUR,MASCOTTE]:
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

                if (self.char.level >= 40 or self.char.stars > 0) and type(self.char) not in [invoc, depl]:
                    for cmpt in range(len(self.char.limitBreaks)):
                        if self.char.limitBreaks[cmpt] != 0:
                            baseStats[cmpt] = int(baseStats[cmpt] * (100+self.char.limitBreaks[cmpt])/100)

                if type(self.char) not in [invoc, depl]:
                    hasSkillUpdated, lvl = True, self.char.level - 5
                    nbExpectedSkills, nbSkills = 0, 0

                    for skilly in self.char.skills:
                        if type(skilly) == skill:
                            nbSkills += 1
                    

                    if type(self.char) != octarien:
                        for cmpt in range(len(lvlToUnlockSkill)):
                            if lvl >= lvlToUnlockSkill[cmpt]:
                                nbExpectedSkills += 1
                        hasSkillUpdated = nbSkills >= nbExpectedSkills
                    else:
                        hasSkillUpdated = nbSkills == self.char.baseSkillNb

                    hasUpdatedStuff = True
                    for stuffy in self.char.stuff:
                        if stuffy.minLvl < self.char.level-10:
                            hasUpdatedStuff = False
                            break

                    hasBonusPointsUpdated, updateBonus = self.char.points < 5, "\n\n"

                    if (hasBonusPointsUpdated and hasSkillUpdated and hasUpdatedStuff):
                        for cmpt in range(MAGIE+1):
                            baseStats[cmpt] = int(baseStats[cmpt] * 1.05)

                self.baseStats = baseStats
                self.maxHp = round((baseHP+perso.level*HPparLevel)*((baseStats[ENDURANCE])/100+1))

                if type(self.char) in [octarien,tmpAllie] and team == 1:
                    self.maxHp = round(self.maxHp * danger / 100)
                self.hp = copy.deepcopy(self.maxHp)

                self.counterOnDodge, self.counterOnBlock = 0, 0

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
                if self.chained:
                    return ""
                if cellToMove == None and x == None and y == None:
                    raise Exception("Argument error : No parameters given")
                actCell = self.cell
                if cellToMove == None:
                    destination = findCell(x,y,tablAllCells)
                else:
                    destination = findCell(cellToMove.x,cellToMove.y,tablAllCells)
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
                        if a.hp > 0 and type(a.char) not in [invoc, depl]:
                            alice += 1

                    return 0.9 + alice*0.05
                
                elif self.char.aspiration == INOVATEUR and not(heal) and not(armor):             # Idol : The more alive allies they got, the more their buff a heals or powerfull
                    alice = 0
                    for a in tablEntTeam[not(self.team)]:
                        if a.hp > 0 and type(a.char) not in [invoc, depl]:
                            alice += 1

                    return 0.9 + alice*0.05

                elif self.char.aspiration in [PREVOYANT,PROTECTEUR] and armor:
                    if self.char.aspiration == PREVOYANT:
                        return 1.2
                    else:
                        return 1 + 0.03 * len(self.specialVars["aspiSlot"])

                elif self.char.aspiration == VIGILANT and heal:
                    return 1 + 0.03 * len(self.specialVars["aspiSlot"])

                else:
                    return 1

            def effectIcons(self):
                """Return a ``string`` with alls ``fightEffects`` icons, names and values on the entity"""
                temp,allReadySeenId,allReadySeenName,allReadySeenNumber = "", [], [], []
                if self.effects != []:
                    for a in self.effects:
                        if a.effects.stackable and a.effects.id in allReadySeenId and a.effects.id not in [vulne.id,dmgUp.id,dmgDown.id,defenseUp.id,kikuRaiseEff.id,kikuUnlifeGift.id,akikiSkill1Eff.id]:
                            for cmpt in range(len(allReadySeenId)):
                                if a.effects.id == allReadySeenId[cmpt]:
                                    allReadySeenNumber[cmpt] += 1
                        elif a.effects.stackable and a.effects.id not in allReadySeenId and a.effects.id not in [vulne.id,dmgUp.id,dmgDown.id,defenseUp.id,kikuRaiseEff.id,kikuUnlifeGift.id,akikiSkill1Eff.id]:
                            allReadySeenId.append(a.effects.id)
                            allReadySeenNumber.append(1)
                            allReadySeenName.append("{0} {1}".format(a.icon,a.effects.name))
                        else:
                            name = a.effects.name
                            if name.endswith("é"):
                                name += self.accord()
                            if a.type == TYPE_ARMOR:
                                temp += f"{a.icon} {name} ({a.value} PAr)\n"
                            elif a.effects.id in [vulne.id,dmgUp.id,dmgDown.id,defenseUp.id,kikuRaiseEff.id,kikuUnlifeGift.id,akikiSkill1Eff.id]:
                                power = round(a.effects.power,2)
                                temp += f"{a.icon} {name} ({power}%)\n"
                            elif a.effects.turnInit > 0:
                                pluriel = ""
                                if a.turnLeft > 1:
                                    pluriel = "s"
                                temp += f"{a.icon} {name} ({a.turnLeft} tour{pluriel})\n"
                            elif a.effects.id == eventFas.id:
                                temp += f"{a.icon} {name} ({a.value})\n"
                            else:
                                temp += f"{a.icon} {name}\n"
                    if allReadySeenId != []:
                        for cmpt in range(len(allReadySeenId)):
                            temp += "{0}{1}\n".format(allReadySeenName[cmpt],[""," x{0}".format(allReadySeenNumber[cmpt])][allReadySeenNumber[cmpt]>1])
                else:
                    temp = "Pas d'effet sur la cible\n"

                for deplEnt in deplTabl:
                    if self.cell in deplEnt[2]:
                        temp += '{0} {1}\n'.format(deplEnt[0].char.cellIcon[deplEnt[0].team],deplEnt[0].char.name)
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
                self.dmgUp, self.critDmgUp, self.healUp, self.critHealUp, self.silent, self.translucide, self.untargetable, self.invisible, self.immune, self.stun, baseStats, self.dodge = 0,0,0,0, False, False, False, False, False, False, self.baseStats, 0
                sumStatsBonus, self.chained = copy.deepcopy(baseStats), False
                self.counterOnDodge, self.counterEmoji, self.blockRate, self.counterOnBlock = 0, "", 0, 0

                for eff in self.effects:
                    if eff != ignore:
                        if eff.effects.stat != None and eff.effects.overhealth == 0:
                            tablEffStats = eff.allStats()
                            for cmpt in range(9):
                                sumStatsBonus[cmpt] += tablEffStats[cmpt]

                        else:
                            sumStatsBonus[0] += eff.effects.strength 
                            sumStatsBonus[1] += eff.effects.endurance 
                            sumStatsBonus[2] += eff.effects.charisma
                            sumStatsBonus[3] += eff.effects.agility
                            sumStatsBonus[4] += eff.effects.precision
                            sumStatsBonus[5] += eff.effects.intelligence
                            if eff.effects.id == "tem":
                                sumStatsBonus[6] += int(self.char.level * 2.5)
                            else:
                                sumStatsBonus[6] += eff.effects.magie
                            sumStatsBonus[7] += eff.effects.resistance
                            sumStatsBonus[8] += eff.effects.percing
                            sumStatsBonus[9] += eff.effects.critical

                    if eff.stun:
                        self.stun = True
                    if eff.effects.invisible:
                        self.translucide = True
                        self.untargetable = True
                        self.invisible = True
                    if eff.effects.translucide:
                        self.translucide = True
                    if eff.effects.untargetable:
                        self.untargetable = True
                    if eff.effects.immunity:
                        self.immune = True
                    if eff.effects.id == silenceEff.id:
                        self.silent = True
                    elif eff.effects.id == chained.id:
                        self.chained = True
                    self.dmgUp, self.critDmgUp, self.healUp, self.critHealUp, self.dodge = self.dmgUp+eff.effects.dmgUp, self.critDmgUp+eff.effects.critDmgUp, self.healUp+eff.effects.healUp, self.critHealUp+eff.effects.critHealUp, self.dodge + eff.effects.dodge
                    if eff.effects.counterOnDodge > 0:
                        self.counterOnDodge += eff.effects.counterOnDodge
                        self.counterEmoji = eff.icon
                    if eff.effects.block > 0:
                        self.blockRate += eff.effects.block
                    
                if type(self.char) not in [invoc, depl]:
                    tRes = sumStatsBonus[7]+self.char.resistance
                else:
                    tRes = sumStatsBonus[7]

                if self.dodge > 100:
                    self.counterOnDodge += self.dodge - 100
                if self.blockRate > 100:
                    self.counterOnBlock += self.blockRate - 100

                t1 = max(0,tRes - 100)
                t2 = min(max(0,tRes - 40),60)
                t3 = min(tRes,40)

                sumStatsBonus[7] = int(t3 + t2//3 + t1//5)

                if type(self.char) in [char,tmpAllie] and sumStatsBonus[7] < 50:
                    sumStatsBonus[7] = max(5 + int(15/50*self.char.level)+sumStatsBonus[7],5 + int(15/50*self.char.level))

                for temp in range(len(sumStatsBonus)):
                    sumStatsBonus[temp] = round(sumStatsBonus[temp])
                if ignore == None:
                    self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie, self.resistance,self.percing,self.critical, self.negativeHeal, self.negativeBoost, self.negativeShield, self.negativeDirect, self.negativeIndirect = sumStatsBonus[0], sumStatsBonus[1], sumStatsBonus[2], sumStatsBonus[3], sumStatsBonus[4] ,sumStatsBonus[5] ,sumStatsBonus[6], sumStatsBonus[7], sumStatsBonus[8],sumStatsBonus[9],sumStatsBonus[10],sumStatsBonus[11],sumStatsBonus[12],sumStatsBonus[13],sumStatsBonus[14]
                else:
                    if type(self.char) not in [invoc, depl]:
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
                for eff in self.effects[:]:
                    if eff.remove:
                        self.effects.remove(eff)
                        try:
                            eff.caster.ownEffect.remove({self:eff.id})
                        except:
                            pass

                        if eff.effects.id == lunaInfiniteDarknessShield.id:
                            self.specialVars["clemBloodJauge"] = None
                        
                        elif eff.effects.id in [clemStunEffect.id,aliceStunEffect.id]:
                            self.specialVars["clemBloodJauge"].value = 100

                        if eff.effects.id == constEff.id:
                            self.maxHp = max(self.maxHp - eff.value,1)
                            self.hp = min(self.hp,self.maxHp)
                        elif eff.effects.id == aconstEff.id:
                            self.maxHp = self.maxHp + eff.value
                for a in addEffect[:]:
                    self.effects.append(a)
                    a.caster.ownEffect.append({self:a.id})
                    addEffect.remove(a)
                    if type(a) != fightEffect:
                        raise AttributeError("Except fightEffect, but get {0} insted".format(type(a)))
                self.recalculate()

            def indirectAttack(self,target=0,value=0,icon="",ignoreImmunity=False,name='',hideAttacker=False,canCrit=True) -> str:
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
                popopo, hasCrit = "", ""
                if canCrit:
                    if random.randint(0,99) < self.intelligence/200*25 * (1-(target.intelligence/100*10)/100):
                        if self.char.aspiration == SORCELER:
                            value = value * 1.25
                            hasCrit = " !!"
                        else:
                            value = value * 1.15
                            hasCrit = " !"

                if target.hp > 0 and not(target.immune):
                    # Looking for a absolute shield
                    maxResist, vulnePower, lifeSavor = 0, 0, []
                    for eff in target.effects:
                        if eff.effects.immunity == True and not(ignoreImmunity):
                            value = 0
                        if eff.effects.absolutShield and eff.value > 0:
                            dmg = min(value,eff.value)
                            if not(hideAttacker):
                                popopo += f"{self.icon} {icon} → {eff.icon}{eff.on.icon} -{dmg} PV\n"
                            else:
                                popopo += f"{eff.icon}{eff.on.icon} -{dmg} PV\n"
                            popopo += eff.decate(value=dmg)
                            self.stats.damageOnShield += dmg
                            if eff.value <= 0:
                                reduc = eff.on.char.level
                                if eff.effects.lightShield:
                                    reduc = 0
                                value = max(0,dmg-reduc)
                            else:
                                value = 0
                        if eff.effects.id in [deterEff1.id,zelianR.id,fairyGardeEff.id]:
                            lifeSavor.append(eff)
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

                    # If the number of damage is still above 0
                    if value > 0:
                        value = int(value)
                        if value >= target.hp and len(lifeSavor) > 0:
                            for eff in lifeSavor:
                                healMsg, why = eff.caster.heal(target,eff.icon,None,eff.value,eff.name,mono=True)
                                popopo += healMsg
                                eff.decate(value=99999999)
                                
                            target.refreshEffects()
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
                            popopo += f"{self.icon} {icon} → {target.icon} -{value} PV{hasCrit}{name}\n"
                        else:
                            popopo += f"{target.icon} -{value} PV{hasCrit}{name}\n"

                        if target.hp <= 0:
                            popopo += target.death(killer=self)
                            if self == target:
                                self.stats.sufferingFromSucess = True

                        if self.isNpc("Clémence pos."):
                            self.specialVars["clemBloodJauge"].value = min(100,self.specialVars["clemBloodJauge"].value+int(value * (0.03*(1+self.level/100))))

                return popopo

            def death(self,killer = 0,trueDeath=False) -> str:
                """
                    The death method, to use when the entity dies.\n
                    Parameter :\n
                    .killer : The ``entity`` who have kill the entity
                """

                for eff in self.effects:
                    if not(trueDeath):
                        if eff.effects.id in [undeadEff2.id,holmgangEff.id] and eff.turnLeft > 0:
                            self.hp = 1
                            return "{0} ne peut pas être vaincu{1} ({2})\n".format(self.name,self.accord(),eff.effects.name)
                        elif eff.effects.id == undeadEff.id:
                            ballerine = groupAddEffect(self,self,AREA_MONO,eff.effects.callOnTrigger,skillIcon=eff.icon)
                            ballerine += eff.decate(value=1)
                            self.refreshEffects()
                            self.hp = 1
                            return "{4} transcende la mort !\n{0} {1} → {0} +{2} __{3}__\n".format(self.icon, eff.icon, eff.effects.callOnTrigger.emoji[self.char.species-1][self.team],eff.effects.callOnTrigger.name,self.name)
                        elif eff.effects.id == kikuRaiseEff.id:
                            self.status = STATUS_RESURECTED
                            actMaxHp = self.maxHp
                            self.maxHp = int(self.maxHp*(100+eff.effects.power)/100)
                            self.hp = int(self.maxHp*0.75)
                            eff.decate(value=99)
                            shieldValue = int(self.maxHp*0.2)
                            add_effect(eff.caster,self,classes.effect("Résurection récente","susRez",overhealth=shieldValue,turnInit=3,absolutShield=True,emoji=sameSpeciesEmoji('<:naB:908490062826725407>','<:naR:908490081545879673>')),ignoreEndurance=True)
                            tempEff,healBuffPerma = copy.deepcopy(dmgUp), copy.deepcopy(absEff)
                            tempEff.power, tempEff.turnInit, healBuffPerma.power, healBuffPerma.turnInit, healBuffPerma.silent = eff.effects.power, -1, eff.effects.power, -1, True
                            add_effect(eff.caster,self,tempEff)
                            add_effect(eff.caster,self,healBuffPerma)
                            self.refreshEffects()
                            self.raiser = eff.caster.icon
                            eff.caster.stats.allieResurected += 1
                            for team in [0,1]:
                                for jaugeEnt, jaugeEff in teamJaugeDict[team].items():
                                    for conds in jaugeEff.effects.jaugeValue.conds:
                                        if (conds == INC_ALLY_KILLED and jaugeEnt.team == self.team) or (conds == INC_ENEMY_KILLED and jaugeEnt.team != self.team):
                                            jaugeEff.value = min(jaugeEff.value+conds.value,100)

                            return "{4} ({0}) est vaincu{5} !\n<:kiku:962082466368213043> <:mortVitaEst:916279706351968296> → <:renisurection:873723658315644938> {0} +{1} PV +{6} PvMax {2} +{3} PAr\n".format(self.icon,self.hp,['<:naB:908490062826725407>','<:naR:908490081545879673>'][self.team],shieldValue,self.char.name,self.accord(),int(self.maxHp-actMaxHp))
                        elif eff.effects.id == mve2Eff.id:
                            if self.status == STATUS_ALIVE:
                                self.status = STATUS_RESURECTED
                                self.hp = int(self.maxHp*eff.effects.power/100)
                                eff.decate(value=99)
                                shieldValue = int(self.maxHp*0.2)
                                add_effect(eff.caster,self,classes.effect("Résurection récente","susRez",overhealth=shieldValue,turnInit=3,absolutShield=True,emoji=sameSpeciesEmoji('<:naB:908490062826725407>','<:naR:908490081545879673>')),ignoreEndurance=True)
                                self.refreshEffects()
                                self.raiser = eff.caster.icon
                                eff.caster.stats.allieResurected += 1
                                return "{4} ({0}) est vaincu{5} !\n{0} <:mortVitaEst:916279706351968296> → <:renisurection:873723658315644938> {0} +{1} PV {2} +{3} PAr\n".format(self.icon,self.hp,['<:naB:908490062826725407>','<:naR:908490081545879673>'][self.team],shieldValue,self.char.name,self.accord())

                if self.isNpc("Aformité incarnée") and dictIsNpcVar["Luna prê."]:
                    if not(killer.isNpc("Luna prê.")):
                        self.hp = 1
                        return ""
                    else:
                        add_effect(self,killer,classes.effect("Borgne","lunaBlinded",precision=-50,stat=MAGIE,turnInit=-1,unclearable=True))
                        killer.refreshEffects()

                pipistrelle = f"{self.char.name} ({self.icon}) est vaincu{self.accord()} !\n"
                if self.status == STATUS_RESURECTED:
                    pipistrelle = f"{self.char.name} ({self.icon}) est vaincu{self.accord()} (pour de bon) !\n"
                    self.status=STATUS_TRUE_DEATH

                if type(self.char) not in [invoc, depl] and killer != self and killer.char.says.onKill != None and random.randint(0,99)<33:
                    try:
                        if killer.isNpc("Ailill"):
                            pipistrelle += "{0} : *\"{1}\"*\n".format('<a:Ailill:882040705814503434>','Ça manque de sang qui gicle partout ça')
                        elif killer.isNpc("Luna prê.") or killer.isNpc("Luna ex."):
                            msgPerElement = [None,None,None,None,None,"La lumière ne peut pas toujours avoir raison de l'ombre.","Reviens donc quand tu auras compris ce que sont les vrais Ténèbres.","L'Espace peut très bien être brisé.","Essaye donc de gagner du Temps là dessus.","Tu as tous les éléments et tu n'est même pas capable de t'en sortir ?"]
                            if msgPerElement[self.char.element] != None:
                                pipistrelle += "{0} : *\"{1}\"*\n".format(killer.icon,msgPerElement[self.char.element])
                            else:
                                pipistrelle += "{0} : *\"{1}\"*\n".format(killer.icon,killer.char.says.onKill.format(target=self.char.name,caster=killer.char.name))
                        elif killer.isNpc("Ly") and self.isNpc("Zombie"):
                            pipistrelle += "{0} : *\"Tu peux ramner tous tes potes si tu veux, je connais un prêtre qui est toujours prêt à me racheter de la rotten flesh\"*\n".format(killer.icon,killer.char.says.onKill.format(target=self.char.name,caster=killer.char.name))
                        elif killer.isNpc("Shehisa") and not(actTurn.isNpc("Shehisa")):
                            pipistrelle += "{0} : *\"Tu devrais faire plus attention où tu met les pieds la prochaine fois\"*\n".format(killer.icon)
                        elif killer.isNpc("Lohica") and not(actTurn.isNpc("Lohica")):
                            pipistrelle += "{0} : *\"Alors, ça t'a coupé le souffle hein ?\"*\n".format(killer.icon)
                        elif killer.isNpc("Clémence Exaltée"):
                            pipistrelle += "{0} : *\"{1}\"*\n".format(killer.icon,clemExKillReact[self.char.aspiration].format(target=self.char.name,caster=killer.char.name))
                        elif killer.hp > 0:
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

                elif self.isNpc("Alice Exaltée") and killer.isNpc("Clémence pos."):
                    pipistrelle += "<a:aliceExalte:914782398451953685> : \"Clé...\"\n<a:clemPos:914709222116175922> : \"... ?\""
                    effect = classes.effect("Réveil subconsicent","clemAwakening",magie=-int((killer.baseStats[MAGIE]*0.3)),turnInit=-1,unclearable=True,type=TYPE_MALUS)
                    pipistrelle += add_effect(killer,killer,effect)
                    killer.char.exp = 35

                elif self.isNpc("Lohica") and killer != self:
                    pipistrelle += "{0} : *\"Ok {1}, qu'est-ce que tu dis de ça ?\"*\n".format(self.icon,killer.char.name) + add_effect(self,killer,estal)
                    killer.refreshEffects()

                elif self.isNpc("Amary") and killer != self and dictIsNpcVar["Lohica"]:
                    lohica = None
                    for team in (0,1):
                        for ent in tablEntTeam[team]:
                            if ent.isNpc("Lohica") and ent.hp > 0:
                                lohica = ent
                                break

                    if lohica != None:
                        pipistrelle += "{0} : *\"Tu vas payer pour ça.\"*\n".format(lohica.icon) + add_effect(lohica,killer,estal,effPowerPurcent=[100,150][lohica.team != killer.team])
                        killer.refreshEffects()
                
                elif random.randint(0,99)<33:
                    if self.isNpc("Hina") and dictIsNpcVar["Lohica"]:
                        pipistrelle += "{0} : *\"{1}\"*\n".format('<:lohica:919863918166417448>',lohicaReactHinaDeath[random.randint(0,len(lohicaReactHinaDeath)-1)])
                        if dictIsNpcVar["Lena"] and random.randint(0,99) < 50:
                            pipistrelle += "{0} : *\"{1}\"*\n".format('<:lena:909047343876288552>',"Lache lui la grappe pour une fois, tu veux ?")
                    elif self.isNpc("Edelweiss") and dictIsNpcVar["Lohica"]:
                        pipistrelle += "{0} : *\"{1}\"*\n".format('<:lohica:919863918166417448>','Am-')
                    elif self.isNpc("Clémence") and dictIsNpcVar["John"]:
                        pipistrelle += "{0} : *\"{1}\"*\n".format('<:john:908887592756449311>','Clémence !')
                    elif self.isNpc("Félicité") and dictIsNpcVar["Alice"]:
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
                    if self.isNpc("Stella") and dictIsNpcVar["Alice"]:
                        for ent in tablEntTeam[int(not(self.team))]:
                            if ent.isNpc("Alice") and ent.hp > 0:
                                pipistrelle += "{0} : *\"J'ai même pas envie d'exprimer une once d'empatie.\"*\n".format(ent.icon)
                                break
                    
                    elif self.isNpc("Alice") and dictIsNpcVar["Stella"]:
                        for ent in tablEntTeam[int(not(self.team))]:
                            if ent.isNpc("Stella") and ent.hp > 0:
                                pipistrelle += "{0} : *\"Même pas capable de supporter quelques dégâts et tu espères me concurrencer ?\"\n".format(ent.icon)
                                break

                    elif self.isNpc("Séréna") and dictIsNpcVar["Lohica"]:
                        for ent in tablEntTeam[int(not(self.team))]:
                            if ent.isNpc("Lohica") and ent.hp > 0:
                                pipistrelle += "{0} : *\"J'espère que tu passeras bien le restant de tes jours à croupir aux enfers.\"\n".format(ent.icon)
                                break

                    elif self.isNpc("Lohica") and dictIsNpcVar["Séréna"]:
                        for ent in tablEntTeam[int(not(self.team))]:
                            if ent.isNpc("Séréna") and ent.hp > 0:
                                pipistrelle += "{0} : *\"T'en fais pas, je me rappellerais de comment tu as vainnement essayé de me tenir tête quand je consulterais ta fleur déséchée dans mon herbier\"\n".format(ent.icon)
                                break

                    elif random.randint(0,99) < 20 and type(self.char) not in [invoc, depl]:
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
                for fEffect in self.effects:
                    if fEffect.trigger == TRIGGER_DEATH:
                        pipistrelle += fEffect.triggerDeath(killer)

                    if fEffect.effects.id == estal.id and fEffect.caster.char.weapon.id == secretum.id and not(allreadyexplose):
                        summationPower = 0
                        for eff in self.effects:
                            if eff.effects.id == estal.id and eff.turnLeft > 0:
                                summationPower += eff.effects.power * secretum.effects.power / 100 * eff.turnLeft
                                eff.decate(turn=99,value=99)
                        self.refreshEffects()

                        stat,damageBase,allReadySeen, killCount, dmgDict, beforeDmg, tempMsg, nbHit = fEffect.caster.allStats()[MAGIE]-fEffect.caster.negativeIndirect,summationPower,[], 0 , "", copy.deepcopy(fEffect.caster.stats.indirectDamageDeal), "", 0
                        for a in self.cell.getEntityOnArea(area=secretum.effects.area,team=self.team,wanted=ALLIES,directTarget=False,fromCell=actTurn.cell):
                            reduc = 1
                            if a != self:
                                reduc = max(AOEMINDAMAGE,1-self.cell.distance(a.cell)*AOEDAMAGEREDUCTION)

                            damage = indirectDmgCalculator(fEffect.caster,self,summationPower,MAGIE,[100,danger][fEffect.caster.team==1],AREA_CIRCLE_2)*reduc

                            tempMsg += fEffect.caster.indirectAttack(a,value=damage,icon = secretum.emoji,name=secretum.effects.name)

                            if a.hp <= 0:
                                killCount += 1
                            else:
                                dmgDict += a.icon
                                nbHit += 1
                            
                        if killCount == 0 and nbHit > 0:
                            pipistrelle += "{0} {1} → {2} -{5} {3} ({4})\n".format(fEffect.caster.icon, fEffect.caster.char.weapon.emoji, dmgDict, (fEffect.caster.stats.indirectDamageDeal-beforeDmg)//nbHit,secretum.effects.name,["","≈"][nbHit > 1])
                        else:
                            pipistrelle += tempMsg
        
                        if fEffect.caster.hp > 0:
                            pipistrelle += groupAddEffect(killer,self,allReadySeen,fEffect.caster.char.weapon.effects.emoji[0][0],effPurcent=secretum.effects.power)
                        allreadyexplose = True

                    if fEffect.caster.specialVars["exploHeal"] and fEffect.effects.type == TYPE_INDIRECT_DAMAGE:
                        power = min(fEffect.effects.power*fEffect.turnLeft*exploHealMarkEff.power/100,expoHeal.power)
                        for ent in fEffect.on.cell.getEntityOnArea(area=exploHealMarkEff.area,team=fEffect.caster.team,fromCell=fEffect.on.cell,wanted=ALLIES,directTarget=False):
                            funnyTempVarName, useless = fEffect.caster.heal(ent, exploHealMarkEff.emoji[0][0], exploHealMarkEff.stat, power, danger=danger, mono = False)
                            pipistrelle += funnyTempVarName
                    
                    if fEffect.turnLeft > 0:
                        if fEffect.trigger == TRIGGER_ON_REMOVE:
                            pipistrelle += fEffect.decate(turn=99)
                        else:
                            fEffect.decate(turn=99)
                self.refreshEffects()

                if killer.char.aspiration == SORCELER and type(self.char) not in [invoc, depl] and killer != self:
                    for a in self.cell.getEntityOnArea(area=AREA_CIRCLE_1,team=self.team,wanted=ALLIES,directTarget=False,fromCell=actTurn.cell):
                        reduc = 1
                        if a != self:
                            reduc = max(AOEMINDAMAGE,1-self.cell.distance(a.cell)*AOEDAMAGEREDUCTION)
                        damage = indirectDmgCalculator(killer,a,max(5,killer.char.level),MAGIE,[100,danger][killer.team==1],AREA_CIRCLE_1)*reduc

                        pipistrelle += killer.indirectAttack(a,value=damage,icon = aspiEmoji[SORCELER])

                if self.status == STATUS_ALIVE:
                    if self.ressurectable:
                        if type(self.char) != octarien or (type(self.char) == octarien and self.char.rez):
                            self.status = STATUS_DEAD
                        else:
                            self.status = STATUS_TRUE_DEATH
                    else:
                        self.status = STATUS_TRUE_DEATH

                if type(self.char) not in [invoc, depl] and self.status != STATUS_RESURECTED:
                    if self.char.deadIcon == None:
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

                if self.status == STATUS_DEAD:
                    effect = lostSoul
                    if self.specialVars["tankTheFloor"]:
                        effect = copy.deepcopy(lostSoul)
                        effect.turnInit += 1
                    add_effect(killer,self,effect)
                    
                    self.refreshEffects()

                elif self.status == STATUS_TRUE_DEATH and killer.isNpc("Kitsune"):
                    pipistrelle += killer.heal(killer,"",CHARISMA,60, effName = "Âme consummée",danger=100, mono = True, useActionStats = ACT_HEAL)[0]

                if type(self.char) not in [invoc, depl]: 
                    for team in [0,1]:
                        for jaugeEnt, jaugeEff in teamJaugeDict[team].items():
                            for conds in jaugeEff.effects.jaugeValue.conds:
                                if (conds == INC_ALLY_KILLED and jaugeEnt.team == self.team) or (conds == INC_ENEMY_KILLED and jaugeEnt.team != self.team):
                                    jaugeEff.value = min(jaugeEff.value+conds.value,100)

                if type(self.char) not in [invoc, depl] and killer != self or killer.team != self.team:
                    killer.stats.ennemiKill += 1
                elif type(self.char) not in [invoc, depl] and killer != self and killer.team == self.team:
                    killer.stats.friendlyfire += 1
                return pipistrelle

            def attack(self,target=0,value = 0,icon = "",area=AREA_MONO,sussess=None,use=STRENGTH,onArmor = 1,effectOnHit = None, useActionStats = ACT_DIRECT, setAoEDamage = False, lifeSteal:int = 0, erosion = 0, skillPercing = 0, execution = False, armorConvert = 0) -> str:
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

                if value > 0 and self.specialVars["damageSlot"] != None and ((self.specialVars["damageSlot"].effects.id == physicRuneEff.id and use in [STRENGTH,PRECISION,AGILITY]) or (self.specialVars["damageSlot"].effects.id == magicRuneEff.id and use in [MAGIE,CHARISMA,INTELLIGENCE])):
                    value = value * (self.specialVars["damageSlot"].effects.power/100+1)

                if useActionStats == None:
                    useActionStats = ACT_DIRECT

                sumDamage, deathCount, cassMontFlag = 0, 0, None

                popipo,critMsg = "",""

                if type(target) != int and value > 0: # If the target is valid
                    dangerMul, tmpBalancing, dodgeMul = 1, 0, 1
                    if danger != None and self.team: # get danger value
                        dangerMul = danger/100

                    popipo,aoeFactor,dmgUpPower,eroTxt, damageMul, isDepha, lifeStealBonus = "",1, 0+5*int(not(self.auto)),["",aspiEmoji[TETE_BRULE]][self.char.aspiration == TETE_BRULE], 1, False, 0
                    if erosion != 0:
                        eroTxt += icon
                    if self.char.aspiration == TETE_BRULE:
                        erosion += 35

                    for a in self.effects: # Does the attacker trigger a effect
                        if a.trigger == TRIGGER_DEALS_DAMAGE and value > 0:
                            temp = a.triggerDamage(value = a.effects.power,icon=a.icon,onArmor=onArmor)
                            value = temp[0]
                            popipo += temp[1]
                        elif a.effects.id == dmgDown.id:
                            dmgUpPower -= a.effects.power
                        elif a.effects.id == dmgUp.id:
                            dmgUpPower += a.effects.power
                        elif a.effects.id == akikiSkill1Eff.id:
                            dmgUpPower += akikiSkill1Eff.power * (self.hp/self.maxHp)
                        elif a.effects.id == kikuUnlifeGift.id:
                            dmgUpPower += kikuUnlifeGift.power * tour
                        elif a.effects.id == areaDmgReductionTmp.id:
                            tmpBalancing = 1
                        elif a.effects.id == monoDmgReductionTmp.id:
                            tmpBalancing = 2
                        elif a.effects.id == lbRdmBlind.id:
                            dodgeMul -= lbRdmBlind.power/100  
                            pass
                        elif a.effects.id == jetLagEff.id:
                            isDepha = True
                        elif a.effects.id == upgradedLifeSteal.id:
                            lifeStealBonus += a.effects.power
                        elif a.effects.id == casseMontEff.id:
                            cassMontFlag = a
                    damageMul = damageMul + (dmgUpPower/100)
                    damageMul = max(0.05,damageMul)

                    if self.hp > 0: # Does the attacker still alive ?
                        critMalusCmpt, tablTarget = 0, target.cell.getEntityOnArea(area=area,team=self.team,wanted=ENEMIES,directTarget=False,fromCell=actTurn.cell)
                        for entityInArea in tablTarget: # For eatch ennemis in the area
                            self.stats.totalNumberShot += 1
                            if entityInArea.hp > 0: # If the target is alive
                                # Dodge / Miss
                                attPre,targetAgi = self.precision,entityInArea.agility
                                if area != AREA_MONO and len(tablTarget) == 1:
                                    sussess += 20

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
                                if random.randint(0,99)<min(successRate*sussess*(1-(entityInArea.dodge/100)),[100,100-LIAMINDODGE][entityInArea.specialVars["liaBaseDodge"]]):
                                    pp = 0
                                    if self.char.aspiration in [POIDS_PLUME,OBSERVATEUR]: # Apply "Poids Plume" critical bonus
                                        pp = self.specialVars["aspiSlot"]

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
                                        if self.team == 0 or octogone:
                                            dangerValue = 100
                                        else:
                                            dangerValue = danger
                                        damage = dmgCalculator(self, entityInArea, value, use, useActionStats, dangerValue, area, typeDmg = TYPE_DAMAGE, skillPercing = 0)

                                    # AoE reduction factor
                                    if target.cell.distance(entityInArea.cell) == 0 or setAoEDamage:
                                        if tmpBalancing == 2 and entityInArea == target:
                                            aoeFactor = 1 - monoDmgReductionTmp.power/100
                                        else:
                                            aoeFactor = 1
                                    else:
                                        aoeFactor = 1-(min(1-AOEMINDAMAGE,(target.cell.distance(entityInArea.cell)-int(target==self))*AOEDAMAGEREDUCTION))
                                        if tmpBalancing == 1:
                                            aoeFactor = max(0.1,aoeFactor-(areaDmgReductionTmp.power/100))

                                    # Damage reduction
                                    vulnePower, defenseUpPower, tempToReturn, noneArmorMsg, reaperDmgBoost, lifeSavor, tablRedirect, tablArmor, blocked = 0, 0, "", "", 0, [], [], [], False
                                    if not(entityInArea.immune) and not(execution):
                                        for a in entityInArea.effects:
                                            if a.trigger == TRIGGER_DAMAGE and not(a.effects.overhealth > 0 or a.effects.redirection > 0):
                                                temp = a.triggerDamage(value = damage,declancher=self,icon=icon,onArmor=onArmor)
                                                damage = temp[0]
                                                if len(noneArmorMsg) == 0 or (len(temp[1]) > 0 and noneArmorMsg[-1] == temp[1][0] == "\n"):
                                                    temp[1] = temp[1][1:]
                                                if len(temp[1]) > 0 and self.icon not in noneArmorMsg and self.icon not in temp[1]:
                                                    temp[1] = self.icon + temp[1]
                                                noneArmorMsg += temp[1]
                                            elif a.effects.overhealth > 0:
                                                tablArmor.append(a)
                                            elif a.effects.redirection > 0:
                                                if a.effects.id != lenaShuRedirect.id:
                                                    tablRedirect.append(a)
                                                elif entityInArea.hp / entityInArea.maxHp <= 0.25:
                                                    tablRedirect.append(a)
                                                    blocked = True

                                            if a.effects.id in [vulne.id,kikuRaiseEff.id]:
                                                vulnePower += a.effects.power
                                            elif a.effects.id == kikuUnlifeGift.id:
                                                defenseUpPower += min(80,kikuUnlifeGift.power/2 * tour)
                                            elif a.effects.id == defenseUp.id:
                                                defenseUpPower += a.effects.power
                                            elif a.effects.id == reaperEff.id and a.caster == self:
                                                reaperDmgBoost = 0.1
                                            elif a.effects.id in [deterEff1.id,zelianR.id,fairyGardeEff.id]:
                                                lifeSavor.append(a)

                                    entityInArea.refreshEffects()
                                    vulnePower -= defenseUpPower
                                    vulnePower = max(vulnePower,-90)

                                    # Critical
                                    critRoll, critDmgMul = random.randint(0,99), 1
                                    critMsg, hasCrit = "", False
                                    critRate = probCritDmg(self) + pp
                                    if critRoll < critRate and damage > 0:
                                        if self.char.aspiration not in [POIDS_PLUME, OBSERVATEUR]:
                                            critDmgMul += 0.3
                                            critMsg = " !"
                                        else:
                                            critMsg = " !!"
                                            critDmgMul += 0.4
                                            self.specialVars["aspiSlot"], pp = 0, 0

                                        self.stats.crits += 1
                                        critMalusCmpt += 1
                                        critDmgMul += self.critDmgUp / 100
                                        hasCrit = True

                                        if critRate > 100:
                                            critDmgMul = critDmgMul * critRate/100

                                    else:
                                        critDmgMul += self.dmgUp / 100

                                    if random.randint(0,99) > 100-entityInArea.blockRate or blocked:
                                        critMsg += " (Blocage !)"
                                        blocked = True

                                    secElemMul = 1
                                    if entityInArea.char.secElement == ELEMENT_LIGHT or (entityInArea.char.secElement == ELEMENT_SPACE and area != AREA_MONO) or (entityInArea.char.secElement == ELEMENT_TIME and area == AREA_MONO):
                                        secElemMul += 0.05
                                    if self.char.secElement == ELEMENT_LIGHT or (self.char.secElement == ELEMENT_SPACE and area != AREA_MONO) or (self.char.secElement == ELEMENT_TIME and area == AREA_MONO):
                                        secElemMul += 0.05
                                    if entityInArea.char.secElement == ELEMENT_DARKNESS:
                                        secElemMul -= 0.05
                                    if self.char.secElement == ELEMENT_DARKNESS:
                                        secElemMul -= 0.05

                                    effectiveDmg = round(damage*aoeFactor*secElemMul*critDmgMul)
                                    beforeDamageMul = copy.deepcopy(effectiveDmg)
                                    effectiveDmg, dephaReducedDmg = round(damage*aoeFactor*secElemMul*critDmgMul*(100+vulnePower)/100*(damageMul+reaperDmgBoost)),0
                                    blockDamage = [0,int(effectiveDmg*0.35)][blocked]
                                    effectiveDmg -= blockDamage
                                    tmpMsg = ""

                                    for tabl in [tablArmor,tablRedirect]:
                                        for eff in tabl:
                                            if effectiveDmg > 0:
                                                triggerReturn = eff.triggerDamage(value = effectiveDmg,declancher=self,icon=icon,onArmor=onArmor)
                                                effectiveDmg = max(effectiveDmg-triggerReturn[0],0)
                                                if self.icon not in tmpMsg:
                                                    tmpMsg += f"{self.icon} {icon} → "+triggerReturn[1]
                                                else:
                                                    tmpMsg += triggerReturn[1]
                                    
                                    popipo += tmpMsg

                                    if self.isNpc("Clémence pos.") and entityInArea.hp - effectiveDmg <= 0 and entityInArea.hp / entityInArea.maxHp >= 0.2:
                                        effectiveDmg = entityInArea.hp - int(entityInArea.maxHp * (random.randint(1,5)/100))

                                    if entityInArea.isNpc("Clémence Exaltée"):
                                        effectiveDmg = min(effectiveDmg,int(entityInArea.maxHp/30))
                                    if blocked:
                                        entityInArea.stats.blockCount += 1
                                        entityInArea.stats.damageBlocks += blockDamage

                                    if isDepha:
                                        dephaReducedDmg = int(effectiveDmg * jetLagEff.power / 100)
                                        effectiveDmg -= dephaReducedDmg

                                    if execution:           # If the attack is a execution, the damage or equal to target's max hp for exploding the "damage receved" stat
                                        effectiveDmg = entityInArea.maxHp

                                    self.stats.shootHited += 1
                                    if entityInArea != self:
                                        self.stats.damageDeal += effectiveDmg
                                        entityInArea.stats.damageRecived += effectiveDmg
                                    else:
                                        self.stats.selfBurn += effectiveDmg

                                    sumDamage += effectiveDmg
                                    entityInArea.stats.numberAttacked += 1
                                    if not execution:
                                        if lifeSavor != []:
                                            for eff in lifeSavor:
                                                if entityInArea.hp - effectiveDmg <= 0:
                                                    healMsg, why = eff.caster.heal(entityInArea,eff.icon,eff.effects.stat,[eff.effects.power,eff.value][eff.effects.stat in [None,FIXE]],eff.name,mono=True)
                                                    popipo += healMsg
                                                    eff.decate(value=99999999)

                                        entityInArea.refreshEffects()
                                        entityInArea.hp -= effectiveDmg

                                        for team in [0,1]:
                                            for jaugeEnt, jaugeEff in teamJaugeDict[team].items():
                                                for conds in jaugeEff.effects.jaugeValue.conds:
                                                    if conds.type == INC_ENEMY_DAMAGED and jaugeEnt.team == self.team:
                                                        jaugeEff.value = min(jaugeEff.value+(conds.value*effectiveDmg/entityInArea.maxHp),100)
                                                    elif conds.type == INC_ALLY_DAMAGED and jaugeEnt.team == entityInArea.team:
                                                        jaugeEff.value = min(jaugeEff.value+(conds.value*effectiveDmg/entityInArea.maxHp),100)
                                        
                                        try:
                                            for conds in teamJaugeDict[self.team][self].effects.jaugeValue.conds:
                                                if conds.type == INC_DEAL_DAMAGE:
                                                    teamJaugeDict[self.team][self].value = min(teamJaugeDict[self.team][self].value+(conds.value*effectiveDmg/entityInArea.maxHp),100)
                                        except KeyError:
                                            pass

                                    else:
                                        entityInArea.hp = 0

                                    if erosion != 0 and effectiveDmg > 0:
                                        lostHp = int(effectiveDmg * erosion/100)
                                        self.stats.maxHpReduced += lostHp
                                        entityInArea.maxHp -= lostHp

                                    # Damage bosted
                                    if use not in [None,HARMONIE] and not execution:
                                        for statBoost in self.effects:
                                            tstats = statBoost.allStats()

                                            if (tstats[use] != 0 or tstats[PERCING] != 0) and statBoost.caster != self: # If the stat was boosted by someone esle
                                                used = self.allStats()[use] - tstats[use]

                                                tempDmg = round(value * (used+100-self.actionStats()[useActionStats])/100 * (1-(min(95,entityInArea.resistance*(1-(self.percing-tstats[PERCING])/100))/100))*dangerMul*self.getElementalBonus(target=entityInArea,area=area,type=TYPE_DAMAGE)*(1+(0.01*self.level)))
                                                tempDmg = round(tempDmg*aoeFactor*critDmgMul*secElemMul*(100+vulnePower)/100*(damageMul+reaperDmgBoost))

                                                dif = effectiveDmg - tempDmg
                                                if dif > 0:
                                                    statBoost.caster.stats.damageBoosted += abs(dif)
                                                    self.stats.underBoost += abs(dif)
                                                else:
                                                    statBoost.caster.stats.damageDodged += abs(dif)

                                            elif statBoost.effects.id == dmgDown.id and beforeDamageMul-effectiveDmg > 0:
                                                statBoost.caster.stats.damageDodged += int(beforeDamageMul-effectiveDmg)
                                            elif statBoost.effects.id == dmgUp.id and beforeDamageMul-effectiveDmg < 0:
                                                statBoost.caster.stats.damageBoosted += int(beforeDamageMul-effectiveDmg)*-1
                                                entityInArea.stats.underBoost += int(beforeDamageMul-effectiveDmg)*-1

                                        for statBoost in entityInArea.effects:
                                            tstats = statBoost.allStats()
                                            if tstats[RESISTANCE] != 0 and statBoost.caster != self: # If the stat was boosted by someone esle
                                                used = self.allStats()[use]
                                                tempDmg = round(value * (used+100-self.actionStats()[useActionStats])/100 * (1-(min(95,(entityInArea.resistance-tstats[RESISTANCE])*(1-self.percing/100))/100))*dangerMul*self.getElementalBonus(target=entityInArea,area=area,type=TYPE_DAMAGE)*(1+(0.01*self.level)))
                                                tempDmg = round(tempDmg*aoeFactor*secElemMul*critDmgMul*(100+vulnePower)/100*(damageMul+reaperDmgBoost))
                                                dif = effectiveDmg - tempDmg
                                                if dif < 0:
                                                    statBoost.caster.stats.damageBoosted += abs(dif)
                                                    self.stats.underBoost += abs(dif)
                                                else:
                                                    statBoost.caster.stats.damageDodged += abs(dif)

                                            elif statBoost.effects.id == vulne.id and beforeDamageMul-effectiveDmg < 0:
                                                statBoost.caster.stats.damageBoosted += abs(beforeDamageMul-effectiveDmg)
                                                entityInArea.stats.underBoost += abs(beforeDamageMul-effectiveDmg)
                                            elif statBoost.effects.id == defenseUp.id and beforeDamageMul-effectiveDmg > 0:
                                                statBoost.caster.stats.damageDodged += abs(beforeDamageMul-effectiveDmg)

                                    # Damage message
                                    popipo += noneArmorMsg
                                    if not(execution):
                                        if effectiveDmg > 0 and tempToReturn == "":
                                            splited = (popipo+"\n").splitlines()
                                            if len(splited)> 0 and self.icon in splited[-1]:
                                                popipo += f" {entityInArea.icon} -{separeUnit(effectiveDmg)} PV{critMsg}\n"
                                            else:
                                                popipo += f"{self.icon} {icon} → {entityInArea.icon} -{separeUnit(effectiveDmg)} PV{critMsg}\n"
                                        else:
                                            popipo += tempToReturn + f" {entityInArea.icon} -{separeUnit(effectiveDmg)} PV{critMsg}\n"
                                    else:
                                        popipo += "{0} {2} → <:sacrified:973313400056725545> {1}\n".format(self.icon,entityInArea.icon,icon)

                                    if erosion != 0 and effectiveDmg > 0:
                                        popipo += f"{self.icon} {eroTxt} → {entityInArea.icon} -{lostHp} PV max\n"

                                    if blocked and entityInArea.counterOnBlock > 0 and random.randint(0,99) < entityInArea.counterOnBlock:
                                        popipo += entityInArea.counter(self,entityInArea.counterOnBlock)

                                    if entityInArea.hp <= 0:
                                        popipo += entityInArea.death(killer = self,trueDeath=execution)
                                        deathCount += 1
                                        if execution:
                                            entityInArea.status, entityInArea.icon = STATUS_TRUE_DEATH, ["","<:aillilKill1:898930720528011314>","<:ailillKill2:898930734063046666>","<:ailillKill2:898930734063046666>"][entityInArea.char.species]
                                    elif self.isNpc("Lena") and random.randint(0,99) < PROBLENAMSG and type(entityInArea.char)!=tmpAllie:
                                        popipo += "*{0} : \"{1}\"*\n".format(self.icon,lenaNotKillMsg[random.randint(0,len(lenaNotKillMsg)-1)])

                                    if isDepha:
                                        eff = copy.deepcopy(jetLagDmgEff)
                                        eff.power = dephaReducedDmg
                                        popipo += groupAddEffect(self, entityInArea, AREA_MONO, [eff], skillIcon=["<:jetLagB:984519444082610227>","<:jetLagR:984519461111472228>"][self.team])
                                    if effectOnHit != None and entityInArea == target and entityInArea.hp > 0:
                                        effectOnHit = findEffect(effectOnHit)
                                        popipo += add_effect(self,target,effectOnHit,skillIcon=icon)

                                        entityInArea.refreshEffects()

                                    if hasCrit:
                                        for jaugeEnt, jaugeEff in teamJaugeDict[self.team].items():
                                            for conds in jaugeEff.effects.jaugeValue.conds:
                                                if conds.type == INC_ON_SELF_CRIT and jaugeEnt == self:
                                                    jaugeEff.value = min(jaugeEff.value+conds.value,100)
                                                if conds.type == INC_ON_ALLY_CRIT and jaugeEnt.hp > 0:
                                                    jaugeEff.value = min(jaugeEff.value+conds.value,100)

                                            if jaugeEff.effects.id == eventFas.id and jaugeEnt.hp > 0 and jaugeEff.value >= 100:
                                                popipo += add_effect(jaugeEnt,jaugeEnt,jaugeEff.effects.callOnTrigger,skillIcon=eventFas.emoji[0][0],setReplica=entityInArea)
                                                jaugeEnt.refreshEffects()
                                                for cmpt in range(len(jaugeEnt.char.skills)):
                                                    tempi = findSkill(jaugeEnt.char.skills[cmpt])
                                                    if tempi != None and findSkill(jaugeEnt.char.skills[cmpt]).id == fascination.id:
                                                        jaugeEnt.cooldowns[cmpt] = 0
                                                jaugeEff.value = 0

                                    # After damage
                                    if entityInArea.char.aspiration in [PROTECTEUR,VIGILANT,ENCHANTEUR,MASCOTTE] and self.id not in entityInArea.specialVars["aspiSlot"]:
                                        entityInArea.specialVars["aspiSlot"].append(self.id)

                                    elif self.char.aspiration == OBSERVATEUR:
                                        self.specialVars["aspiSlot"] += 3

                                    if (entityInArea.isNpc(["Liu","Kitsune"])) and type(actTurn.char != classes.invoc):
                                        popipo += add_effect(entityInArea,actTurn,charming,skillIcon = entityInArea.weapon.effects.emoji[0][0])
                                        actTurn.refreshEffects()

                                    for eff in entityInArea.effects:
                                        if eff.effects.id in [lightAura2ActiveEff.id, tintabuleEff.id]:                                 # Aura de lumière 2
                                            sumHeal, sumEnt = 0,[]
                                            for ent in entityInArea.cell.getEntityOnArea(area=eff.effects.area,team=entityInArea.team,wanted=ALLIES,directTarget=False,fromCell=actTurn.cell):
                                                useless, tempi = eff.caster.heal(ent,eff.icon,eff.effects.stat,eff.effects.power,eff.effects.name,danger)
                                                if tempi > 0:
                                                    sumHeal += tempi
                                                    sumEnt.append(ent.icon)

                                            temp = ""
                                            for i in sumEnt:
                                                temp += i
                                            if len(sumEnt) > 0:
                                                popipo += "{0} {1} → {5} +{2} {3} PV ({4})\n".format(eff.caster.icon,eff.icon,["","≈"][len(sumEnt)>1],int(sumHeal/len(sumEnt)),eff.effects.name, temp)
                                            popipo += eff.decate(value=1)
                                            entityInArea.refreshEffects()
                                        elif eff.effects.id == flambe.id and use in [STRENGTH,ENDURANCE,AGILITY,PRECISION]:                         # Flambage
                                            eff.effects.power += flambe.power
                                        elif eff.effects.id == magAch.id and use == [MAGIE,CHARISMA,INTELLIGENCE,HARMONIE]:                            # Magia
                                            eff.effects.power += magAch.power
                                        elif eff.effects.id == rosesPhysiEff.id and use == STRENGTH:
                                            popipo += eff.triggerDamage(value = damage,declancher=self,icon=icon,onArmor=onArmor)[1]
                                        elif eff.effects.id == rosesMagicEff.id and use == MAGIE:
                                            popipo += eff.triggerDamage(value = damage,declancher=self,icon=icon,onArmor=onArmor)[1]
                                        elif eff.effects.id in [haimaEffect.id,pandaimaEff.id]:
                                            finded = False
                                            for sndEff in entityInArea.effects:
                                                if sndEff.effects.id == eff.effects.callOnTrigger.id:
                                                    finded = True
                                                    break

                                            if not(finded):
                                                popipo += add_effect(eff.caster,entityInArea,eff.effects.callOnTrigger)
                                                popipo += eff.decate(value = 1)
                                                entityInArea.refreshEffects()
                                        elif eff.effects.id in [mattSkill4Eff.id,lightLameEff.id,astralLameEff.id,timeLameEff.id]:
                                            popipo += eff.triggerDamage(value = damage,declancher=self,icon=icon,onArmor=onArmor)[1]

                                else:
                                    popipo += f"{entityInArea.char.name} esquive l'attaque\n"
                                    if self.isNpc("Lena") and random.randint(0,99) < PROBLENAMSG and type(entityInArea.char)!=tmpAllie:
                                        popipo += "*{0} : \"{1}\"*\n".format(self.icon,lenaMissMsg[random.randint(0,len(lenaMissMsg)-1)])
                                    entityInArea.stats.dodge += 1
                                    entityInArea.stats.numberAttacked += 1
                                    if entityInArea.char.aspiration == POIDS_PLUME:
                                        entityInArea.specialVars["aspiSlot"] += 3
                                    elif self.char.aspiration == OBSERVATEUR:
                                        self.specialVars["aspiSlot"] = int(self.specialVars["aspiSlot"] * 0.5)
                                    if (entityInArea.isNpc("Lia") or (entityInArea.isNpc("Kitsune") or entityInArea.isNpc("Lia Ex")) and type(self.char) not in [invoc,depl]):
                                        popipo += add_effect(entityInArea,actTurn,charming,skillIcon = entityInArea.weapon.effects.emoji[0][0])
                                        entityInArea.refreshEffects()

                                    if self.cell.distance(entityInArea.cell) <= 3 and random.randint(0,99) < entityInArea.counterOnDodge:
                                        popipo += entityInArea.counter(self,entityInArea.counterOnDodge)

                                if cassMontFlag != None and cassMontFlag.value > 0 and target.team != self.team and entityInArea == target:
                                    damage = indirectDmgCalculator(cassMontFlag.caster, target, cassMontFlag.effects.power, cassMontFlag.effects.stat, danger, area=cassMontFlag.effects.area)
                                    popipo += cassMontFlag.caster.indirectAttack(target,value=damage,icon = cassMontFlag.icon,name=cassMontFlag.effects.name)
                                    popipo += cassMontFlag.decate(value=1)
                                    self.refreshEffects()

                        if (self.isNpc(["Liz","Kitsune"])) and type(entityInArea.char != classes.invoc) and ((skillToUse != None and skillToUse.id != kitsuneSkill4.id) or skillToUse == None):
                            popipo = groupAddEffect(caster=self, target=target,area=tablTarget, effect=charming, skillIcon=self.weapon.effects.emoji[0][0])

                    if sumDamage > 0:
                        sumLifeSteal, lifeStealEmote, lifeStealCapBoost = 0, "", 0
                        for eff in self.effects:
                            if eff.effects.id == convertEff.id :                         # Convertion :
                                armorConvert += convertEff.power/100
                            elif eff.effects.id in [vampirismeEff.id,aliceExWeapEff.id,undeadEff2.id,holmgangEff.id]:
                                sumLifeSteal += eff.effects.power
                                lifeStealEmote += eff.icon
                            elif eff.effects.id == upgradedLifeSteal.id:
                                lifeStealCapBoost += eff.effects.power
                        if self.char.aspiration == BERSERK:
                            sumLifeSteal += self.specialVars["aspiSlot"]
                            lifeStealEmote += aspiEmoji[BERSERK]
                        if lifeSteal > 0:
                            sumLifeSteal += lifeSteal
                            lifeStealEmote += icon
                        if self.isNpc("Clémence pos."):
                            sumLifeSteal += 33
                            lifeStealEmote += vampirismeEff.emoji[1][1]
                            self.specialVars["clemBloodJauge"].value = min(100,self.specialVars["clemBloodJauge"].value+int(sumDamage * (0.01*(1+self.level/100))))
                            if self.specialVars["clemMemCast"]:
                                self.specialVars["clemMemCast"] = False
                        elif self.isNpc("Clémence Exaltée"):
                            sumLifeSteal += 30
                            if self.hp / self.maxHp <= 0.25:
                                sumLifeSteal += 70
                            lifeStealEmote += vampirismeEff.emoji[1][1]

                        if sumLifeSteal > 0:
                            supposedHealPowa, moreHealPowa = min(sumDamage * sumLifeSteal / 100,self.level*(45+lifeStealCapBoost)*(1+lifeStealBonus/100)), 0
                            if self.isNpc("Clémence Exaltée") and supposedHealPowa + self.hp > self.maxHp:
                                moreHealPowa = supposedHealPowa - (self.maxHp - self.hp)

                            healPowa = min(self.maxHp - self.hp, supposedHealPowa)
                            temp, useless = self.heal(self,lifeStealEmote,None,healPowa)
                            popipo += temp
                        
                            if moreHealPowa > 0:
                                clemExOvershield = classes.effect("Armure Sanguine","clemExOvershield",overhealth=int(moreHealPowa//2),turnInit=-1,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=clemUltShield.emoji,absolutShield=True)
                                popipo += groupAddEffect(self, self, AREA_MONO, clemExOvershield, vampirismeEff.emoji[1][1])
                        elif armorConvert > 0:
                            eff = copy.deepcopy(convertArmor)
                            eff.overhealth = int(sumDamage/(armorConvert/100))
                            popipo += add_effect(self,self,eff,ignoreEndurance=True)                            
                            self.refreshEffects()
                return popipo, deathCount

            def startOfTurn(self,tablEntTeam="tabl") -> str: 
                """
                    The method to call when a entity start his turn.\n
                    Reduce the duration of all their own ``fightEffects`` and return a ``string`` with the effectives changes
                """
                toReturn = ""
                allReadySeen = []
                for a in self.effects:
                    # Any normals effects --------------------------------
                    if a.trigger == TRIGGER_START_OF_TURN and (not(a.effects.stackable) or a.effects.type != TYPE_INDIRECT_DAMAGE):
                        toReturn += a.triggerStartOfTurn(danger)

                    # Stackable indirect damages effects -----------------
                        # Those effects are temporary merge into one for don't spam the action's windows
                    elif a.trigger == TRIGGER_START_OF_TURN and a.effects.stackable and a.effects.type == TYPE_INDIRECT_DAMAGE and {a.caster.id:a.effects.id} not in allReadySeen :
                        primalPower,nbOfDecate = a.effects.power,0
                        for eff in self.effects:                 # Adding the power of all sames effects by the same caster to one to have one to rule them all
                            if eff.effects.id == a.effects.id and eff.caster.id == a.caster.id:
                                a.effects.power += eff.effects.power

                        a.effects.power -= primalPower           # Deducing the base power, 'cause we are at [NbEffect]+1 * power
                        toReturn += a.triggerStartOfTurn(danger,decate=False)
                        a.effects.power = primalPower
                        
                        for eff in self.effects:
                            if eff.effects.id == a.effects.id and eff.caster.id == a.caster.id:
                                temporaty = eff.decate(value=1)
                                if temporaty != "":
                                    nbOfDecate += 1

                        if nbOfDecate > 1:                      # Regrouping all the decate messages as well
                            toReturn += "__{0}__ ne subit plus sous {1} effets de __{2}__\n".format(self.char.name,nbOfDecate,a.effects.name)
                        elif nbOfDecate == 1:
                            toReturn += temporaty

                        allReadySeen.append({a.caster.id:a.effects.id})

                    elif a.effects.id == gwenCoupeEff.id:
                        if random.randint(0,99) < 15:
                            effect = intargetable
                            toReturn += add_effect(self,self,effect)

                    if a.effects.id == kikuRaiseEff.id and tour >= 16:
                        self.stats.lauthingAtTheFaceOfDeath = True
                
                    elif a.effects.id == clemUltShield.id:
                        a.decate(turn=99)
                        effect = copy.deepcopy(dmgUp)
                        effect.power, effect.turnInit = 50, 2
                        toReturn += add_effect(caster=self,target=self,effect=effect, start = a.name, danger=danger, skillIcon=a.icon)

                allReadySeenID, unAffected, effNames, allReadySeenCharId = [], [], [], []

                for dictElem in self.ownEffect[:]:
                    for on, eff in dictElem.items():
                        for effOn in on.effects:
                            if effOn.id == eff:
                                temp = effOn.decate(turn=1)
                                if temp != "" and effOn.effects.trigger != TRIGGER_ON_REMOVE:
                                    if effOn.effects.id not in allReadySeenID:
                                        allReadySeenID.append(effOn.effects.id)
                                        unAffected.append([on.icon])
                                        effNames.append(effOn.effects.name)
                                        allReadySeenCharId.append([on.id])
                                    else:
                                        for cmpt in range(len(allReadySeenID)):
                                            if allReadySeenID[cmpt] == effOn.effects.id and on.id not in allReadySeenCharId[cmpt]:
                                                unAffected[cmpt].append(on.icon)
                                                allReadySeenCharId[cmpt].append(on.id)
                                else:
                                    toReturn += temp

                                on.refreshEffects()
                                break

                ultimateTemp = ""

                for cmpt in range(len(allReadySeenID)):
                    tempLen = len(unAffected[cmpt])
                    if tempLen > 1:
                        for cmpt2 in range(tempLen):
                            ultimateTemp += unAffected[cmpt][cmpt2]
                        ultimateTemp += " → ~~{0}~~\n".format(effNames[cmpt])
                    elif tempLen == 1:
                        ultimateTemp += "{0} → ~~{1}~~\n".format(unAffected[cmpt][0],effNames[cmpt])

                toReturn += ultimateTemp

                for a in range(7):
                    if self.cooldowns[a] > 0:
                        self.cooldowns[a] -= 1

                try:
                    for conds in teamJaugeDict[self.team][self].effects.jaugeValue.conds:
                        if conds.type == INC_START_TURN:
                            teamJaugeDict[self.team][self].value = min(teamJaugeDict[self.team][self].value+conds.value,100)
                            break

                except KeyError:
                    pass

                if (self.isNpc("Luna ex.") or self.isNpc("Luna prê.")) and self.specialVars["clemBloodJauge"] == None:
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
                        if ent.hp > 0 and type(ent.char) not in [invoc, depl] :
                            temp.append(ent)

                    if len(temp) > 0:
                        temp = temp[random.randint(0,len(temp)-1)]
                        toReturn += add_effect(self,temp,cardAspi[temp.char.aspiration]," ({0})".format(self.weapon.name),skillIcon = self.weapon.effects.emoji[0][0])
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

                    toReturn += add_effect(self,temp,[miltrilPlanisftEffDebuff,miltrilPlanisftEffBuff][temp.team == self.team], " ({0})".format(self.weapon.name),skillIcon=self.weapon.effects.emoji[0][0])
                    temp.refreshEffects()
                
                if self.char.aspiration == MASCOTTE:
                    nbEnnemiHit = len(self.specialVars["aspiSlot"])
                    if nbEnnemiHit > 0:
                        self.specialVars["aspiSlot"] = []
                        mascDmgBuff = copy.deepcopy(dmgUp)
                        mascDmgBuff.silent, mascDmgBuff.power, mascDmgBuff.emoji = True, min(MASC_MAX_BOOST, max(MASC_MIN_BOOST, self.char.level * MASC_LVL_CONVERT/100 * nbEnnemiHit)), uniqueEmoji(aspiEmoji[MASCOTTE])
                        groupAddEffect(self, self, AREA_DONUT_4, mascDmgBuff)

                return toReturn

            def endOfTurn(self,danger) -> str:
                """
                    The method to call when eff entity end their turn\n
                    Return eff ``string`` with all the correspondings actions
                """
                toReturn,allReadySeen  = "",[]
                for eff in self.effects:
                    if eff.trigger == TRIGGER_END_OF_TURN and (not(eff.effects.stackable) or eff.effects.type != TYPE_INDIRECT_DAMAGE):
                        toReturn += eff.triggerEndOfTurn(danger)

                    # Stackable indirect damages effects -----------------
                        # Those effects are temporary merge into one for don't spam the action's windows
                    elif eff.trigger == TRIGGER_END_OF_TURN and eff.effects.stackable and eff.effects.type == TYPE_INDIRECT_DAMAGE and {eff.caster.id:eff.effects.id} not in allReadySeen :
                        primalPower,nbOfDecate = eff.effects.power,0
                        for eff2 in self.effects:                 # Adding the power of all sames effects by the same caster to one to have one to rule them all
                            if eff2.effects.id == eff.effects.id and eff2.caster.id == eff.caster.id:
                                eff.effects.power += eff2.effects.power

                        eff.effects.power -= primalPower           # Deducing the base power, 'cause we are at [NbEffect]+1 * power
                        toReturn += eff.triggerEndOfTurn(danger,decate=False)
                        eff.effects.power = primalPower
                        
                        for eff2 in self.effects:
                            if eff2.effects.id == eff.effects.id and eff2.caster.id == eff.caster.id:
                                temporaty = eff.decate(value=1)
                                if temporaty != "":
                                    nbOfDecate += 1

                        if nbOfDecate > 1:                      # Regrouping all the decate messages as well
                            toReturn += "__{0}__ ne subit plus sous {1} effets de __{2}__\n".format(self.char.name,nbOfDecate,eff.effects.name)
                        elif nbOfDecate == 1:
                            toReturn += temporaty

                        allReadySeen.append({eff.caster.id:eff.effects.id})
                    
                    if eff.effects.id == tablWeapExp[0].id:
                        try:
                            if random.randint(0,99) < [20,100][optionChoice==OPTION_WEAPON]:
                                for eff2 in tablWeapExp:
                                    if eff.name == eff2.name:
                                        toReturn += add_effect(self,self,eff.effects.callOnTrigger,skillIcon=eff.icon)
                                        break
                        except:
                            print_exc()

                for skilly in self.char.skills:
                    if findSkill(skilly) != None and findSkill(skilly).id == horoscope.id:
                        tablHorEff = []
                        for eff in horoscopeEff:
                            tablHorEff.append(copy.deepcopy(eff[0]))
                        for eff in self.effects:
                            for toCompare in tablHorEff[:]:
                                if eff.effects.id == toCompare.id:
                                    tablHorEff.remove(toCompare)
                                    break
                        if len(tablHorEff) > 0:
                            if len(tablHorEff) == 1:
                                randy = 0
                            else:
                                randy = random.randint(0,len(tablHorEff)-1)
                            toReturn += add_effect(self,self,tablHorEff[randy],skillIcon=skilly.emoji)
                        self.refreshEffects()
                        break

                self.refreshEffects()
                if self.char.aspiration in [PROTECTEUR,VIGILANT,ENCHANTEUR]:
                    self.specialVars["aspiSlot"] = []

                if type(self.char) == invoc and not(self.char.name.startswith("Patte de The Giant Enemy Spider")):
                    self.leftTurnAlive -= 1
                    if self.leftTurnAlive <= 0:
                        self.hp = 0
                        toReturn += "\n{0} est désinvoqué{1}".format(self.char.name,self.accord())
                return toReturn

            def atRange(self):
                """Return the entity in range of the main weapon"""
                atRangeVar = self.cell.getEntityOnArea(area=self.char.weapon.effectiveRange,team=self.team,wanted=self.char.weapon.target,lineOfSight= True,directTarget=True,ignoreInvoc=self.char.weapon.type==TYPE_HEAL,fromCell=self.cell)
                surrondingsEnnemis = self.cell.getEntityOnArea(area=self.char.weapon.effectiveRange,team=self.team,wanted=ENEMIES,directTarget=True,fromCell=self.cell)
                return atRangeVar

            def quickEffectIcons(self):
                temp = f"{self.icon} {self.char.name} : {separeUnit(self.hp)}/{separeUnit(self.maxHp)} "
                if self.effects != []:
                    allReadySeenIcon, allReadySeenNumber = [], []
                    temp += "("
                    for a in self.effects:
                        if a.effects.stackable and a.icon in allReadySeenIcon:
                            for cmpt in range(len(allReadySeenIcon)):
                                if allReadySeenIcon[cmpt] == a.icon:
                                    allReadySeenNumber[cmpt] += 1
                        elif a.effects.stackable and a.icon not in allReadySeenIcon:
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
                if type(self.char) != octarien or (type(self.char) == octarien and not(self.char.oneVAll)):
                    temp = f"{self.icon} : "
                else:
                    temp = "{0} __{1}__ :\n({2} Pv /{3})\n".format(self.icon,self.char.name,separeUnit(self.hp),separeUnit(self.maxHp))
                stackableAlreaySeen = []
                if self.status == STATUS_DEAD:
                    return (f"{self.icon} : <:lostSoul:887853918665707621>\n",f"{self.icon} : <:lostSoul:887853918665707621>\n",f"{self.icon} : <:lostSoul:887853918665707621>\n")
                elif self.effects != [] and self.status != STATUS_TRUE_DEATH:
                    normMsg, lightMsg, ulightMsg, prioEff, nbBuff, nbDebuff, nbIndHeal, nbIndDmg, nbPassive, nbArmor = temp, temp, temp, [], 0, 0, 0, 0, 0, 0

                    for eff in self.effects:
                        if eff.effects.prio > 0:
                            prioEff.append(eff)
                        else:
                            if eff.effects.jaugeValue != None or eff.icon in hiddenIcons:
                                nbPassive += 1
                            elif eff.effects.stackable and (eff.effects.id not in stackableAlreaySeen):
                                number = 0
                                for ent in self.effects:
                                    if ent.effects.id == eff.effects.id:
                                        number += 1

                                toAdd = eff.icon + ["({0})".format(number),""][number <= 1]
                                normMsg += toAdd
                                if not((eff.effects.silent or eff.effects.turnInit == -1)):
                                    lightMsg += toAdd
                                else:
                                    nbPassive += number

                                if eff.effects.type in [TYPE_BOOST]:
                                    nbBuff += number
                                elif eff.effects.type in [TYPE_INDIRECT_HEAL]:
                                    nbIndHeal += number
                                elif eff.effects.type in [TYPE_MALUS]:
                                    nbDebuff += number
                                elif eff.effects.type in [TYPE_INDIRECT_DAMAGE]:
                                    nbIndDmg += number
                                elif eff.effects.type in [TYPE_ARMOR]:
                                    nbArmor += number

                                stackableAlreaySeen.append(eff.effects.id)
                            elif not(eff.effects.stackable and (eff.effects.id in stackableAlreaySeen)):
                                toAdd = eff.icon
                                normMsg += toAdd
                                if not(eff.effects.silent or eff.effects.turnInit == -1):
                                    lightMsg += toAdd
                                else:
                                    nbPassive += 1
                                if eff.effects.type in [TYPE_BOOST]:
                                    nbBuff += 1
                                elif eff.effects.type in [TYPE_INDIRECT_HEAL]:
                                    nbIndHeal += 1
                                elif eff.effects.type in [TYPE_MALUS]:
                                    nbDebuff += 1
                                elif eff.effects.type in [TYPE_INDIRECT_DAMAGE]:
                                    nbIndDmg += 1
                                elif eff.effects.type in [TYPE_ARMOR]:
                                    nbArmor += 1


                    if len(prioEff) > 0:
                        prioEff.sort(key=lambda ballerine: ballerine.effects.prio - (0.01* ballerine.turnLeft), reverse=True)
                        toReturn = "{2}{0} {1}\n".format(prioEff[0].icon, prioEff[0].effects.name,temp)
                        return (toReturn, toReturn, toReturn)
                    else:
                        tabluLightIcon = ["🛡️","🩸","🩹","🔼","🔽","⏺️"]
                        tabluLightValues = [nbArmor,nbIndDmg,nbIndHeal,nbBuff,nbDebuff,nbPassive]

                        for cmpt in range(len(tabluLightValues)):
                            if tabluLightValues[cmpt] > 0:
                                ulightMsg += "{0} {1} ".format(tabluLightIcon[cmpt],tabluLightValues[cmpt])
                        if normMsg == f"{self.icon} : ":
                            normMsg = ""
                        else:
                            normMsg = normMsg + "\n"
                        return (normMsg,lightMsg+[""," + ⏺️ {0}".format(nbPassive)][nbPassive > 0]+"\n",ulightMsg+"\n")
                else:
                    return ("","","")

            def accord(self):
                if self.char.gender == GENDER_FEMALE:
                    return "e"
                else:
                    return ""

            async def getIcon(self,bot):
                if type(self.char) == char or (type(self.char) == tmpAllie and self.team == 0):
                    if teamSettings["settingsAllyIcon"] == TEAM_SET_ALLY_ICON_DEFAULT and type(self.char) == char:
                        self.icon = await getUserIcon(bot,self.char)
                    elif teamSettings["settingsAllyIcon"] == TEAM_SET_ALLY_ICON_DEFAULT and type(self.char) == tmpAllie:
                        self.icon = [self.char.splashIcon,self.char.icon][self.char.splashIcon == None]
                    elif teamSettings["settingsAllyIcon"] == TEAM_SET_ALLY_ICON_ASPIRATION:
                        self.icon = aspiEmoji[self.char.aspiration]
                    elif teamSettings["settingsAllyIcon"] == TEAM_SET_ALLY_ICON_WEAPON:
                        self.icon = self.char.weapon.emoji
                elif type(self.char) not in [invoc,depl]:
                    if self.isNpc("Chûri-Hinoro"):
                        self.icon = [None,'<:churHi:994045813175111811>'][teamSettings["settingsEnemyIcon"]==TEAM_SET_ENEMY_ICON_CLASSICAL or self.char.splashIcon == None]
                    else:
                        self.icon = [self.char.splashIcon,self.char.icon][teamSettings["settingsEnemyIcon"]==TEAM_SET_ENEMY_ICON_CLASSICAL or self.char.splashIcon == None]
                else:
                    self.icon = self.char.icon[self.team]
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
                    return "("+respond+")"
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

                    sumEnt.refreshEffects()

                    if self.id != timeline.timeline[0].id:
                        found = False
                        for cmpt in range(len(timeline.timeline)):
                            if self.id == timeline.timeline[cmpt].id and type(timeline.timeline[cmpt].char) not in [invoc, depl]:
                                whereToInsert = cmpt+1
                                break
                    else:
                        whereToInsert = 1

                    timeline.insert(self,sumEnt)

                    accord = ""
                    if summon.gender == GENDER_FEMALE:
                        accord="e"
                    funnyTempVarName = f"{self.char.name} invoque un{accord} {summon.name}"
                    tablAliveInvoc[team] += 1
                    self.stats.nbSummon += 1
                    return tablEntTeam,tablAliveInvoc,timeline,funnyTempVarName

            def getElementalBonus(self,target,area : int,type : int):
                """Return the elemental damage bonus"""
                if type not in [TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_ARMOR,TYPE_INDIRECT_DAMAGE]:
                    baseMul = 1
                    if self.char.element == ELEMENT_UNIVERSALIS_PREMO:
                        baseMul += FIREDMGBUFF*2/100
                    elif self.char.element == ELEMENT_DARKNESS:
                        baseMul += DARKNESSDMGBUFF/100

                    if self.char.element in [ELEMENT_FIRE]:
                        return baseMul + (FIREDMGBUFF/100*(area != AREA_MONO))+(FIREDMGBUFF/100*(self.cell.distance(target.cell) > 2))
                    elif self.char.element in [ELEMENT_WATER]:
                        return baseMul + (WATERDMGBUFF/100*(area == AREA_MONO))+(WATERDMGBUFF/100*(self.cell.distance(target.cell) > 2))
                    elif self.char.element in [ELEMENT_AIR]:
                        return baseMul + (AIRDMGBUFF/100*(area != AREA_MONO))+(AIRDMGBUFF/100*(self.cell.distance(target.cell) <= 2))
                    elif self.char.element in [ELEMENT_EARTH]:
                        return baseMul + (EARTHDMGBUFF/100*(area == AREA_MONO))+(EARTHDMGBUFF/100*(self.cell.distance(target.cell) <= 2))

                return 1

            async def resurect(self,target,value : int, icon : str,danger=danger):
                if tour <= 20 and target.status != STATUS_TRUE_DEATH:
                    if self.team == 1:
                        value = int(value * (danger/100))
                    value = min(value,target.maxHp)
                    self.stats.allieResurected += 1
                    self.stats.heals += value
                    target.hp = value
                    target.status = STATUS_RESURECTED
                    target.icon = await target.getIcon(bot)
                    
                    add_effect(self,target,onceButNotTwice)

                    for eff in target.effects:
                        if eff.effects.id == lostSoul.id:
                            eff.decate(turn=99)

                    target.refreshEffects()

                    shieldValue, raiseShieldEmoji = int(target.maxHp*(0.2+0.3*int(not(target.auto)))), ['<:naB:908490062826725407>','<:naR:908490081545879673>'][target.team]
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
                    notDeadYet = classes.effect("Résurection récente","susRez",overhealth=shieldValue,turnInit=3,absolutShield=True,emoji=sameSpeciesEmoji('<:naB:908490062826725407>','<:naR:908490081545879673>'))
                    add_effect(self,target,notDeadYet,ignoreEndurance=True)
                    if target.isNpc("Akira"):
                        mater = classes.effect("Rage Inhumaine","Akiki",strength=int(target.char.level*1.5),turnInit=-1,emoji="<a:menacing:917007335220711434>",stackable=True)
                        rep += add_effect(target,target,mater)
                    target.refreshEffects()
                    ressurected[target.team].append(target)

                    return rep
                else:
                    return ""

            def getAggroValue(self,target):
                """Return the aggro value agains the target. Made for be use as a key for sort lists"""
                if not(target.untargetable):
                    aggro = [20,0][type(target.char)==invoc]                                          # Base aggro value. Maybe some skills will influe on it later
                    if target.char.weapon.id == grav.id:
                        aggro += self.stats.survival

                    for eff in target.effects:                           # Change the aggro
                        aggro += eff.effects.aggro

                        if eff.effects.replica != None and type(target.char) not in [char,tmpAllie]:
                            aggro += 25
                        if eff.effects.id == provokeEff.id and eff.caster == target:
                            aggro += 9999
                    distance = self.cell.distance(target.cell)          # Distance factor.
                    aggro += 40-max(distance*10,40)                     # The closer the target, the greater the aggro will be.

                    if target.char.aspiration in [BERSERK,POIDS_PLUME,ENCHANTEUR,PROTECTEUR]:       # The tanks aspirations generate more aggro than the others
                        aggro += 15

                    baseGainDmg = 500
                    baseGainHeal = 500
                    baseGainShield = 750
                    baseGainBoost = 350

                    if self.char.charSettings["offTarget"] != 0:
                        if self.char.charSettings["offTarget"] == CHARSET_OFFTARGET_DMG:
                            baseGainDmg = baseGainDmg // 2
                        elif self.char.charSettings["offTarget"] == CHARSET_OFFTARGET_HEAL:
                            baseGainHeal = baseGainHeal // 2
                            baseGainShield = baseGainShield // 2
                        elif self.char.charSettings["offTarget"] == CHARSET_OFFTARGET_BUFF:
                            baseGainBoost = baseGainBoost // 2

                    aggro += target.stats.damageDeal//baseGainDmg*5             # The more the target have deals damage, the mort aggro he will generate
                    aggro += target.stats.heals//baseGainHeal*5                  # The more the target have deals heals, the mort aggro he will generate
                    aggro += target.stats.shieldGived//baseGainShield*5            # The more the target have gave armor, the mort aggro he will generate
                    aggro += target.stats.damageBoosted//baseGainBoost*5            # The more the target have gave armor, the mort aggro he will generate

                    if self.isNpc("Luna ex."): 
                        if target.char.element == ELEMENT_DARKNESS:
                            aggro = aggro * 1.1
                        if target.char.element == ELEMENT_LIGHT or target.char.secElement in [ELEMENT_DARKNESS,ELEMENT_LIGHT]:
                            aggro = aggro * 1.05
                    elif self.isNpc("Kiku") and target.status == STATUS_ALIVE:
                        aggro = aggro * 1.2

                    return int(aggro)
                else:
                    return -111

            def heal(self,target, icon : str, statUse : Union[int,None], power : int, effName = None,danger=danger, mono = False, useActionStats = ACT_HEAL):
                overheath, aff, toReturn, healPowa, critMsg, diing, healBuffer, statUsed = 0, target.hp < target.maxHp, "", 0, "", None, {"total":0}, copy.deepcopy(statUse)
                if power > 0 and target.hp > 0:
                    if useActionStats == None:
                        useActionStats = ACT_HEAL
                    if statUse not in [None,FIXE]:
                        if statUse == HARMONIE:
                            temp, selfStats = 0, self.allStats()
                            for cmpt in range(len(selfStats)):
                                if selfStats[cmpt] > temp:
                                    temp = selfStats[cmpt]
                                    statUsed = cmpt
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

                        healPowa = calHealPower(self,target,power,secElemMul,statUse,useActionStats,danger)
                        critRate = probCritHeal(self,target)
                        
                        if random.randint(0,99) < probCritHeal(self,target):
                            critBonus = 1.25 + (preciChiEff.power * int(self.specialVars["preci"])/100) + (ironHealthEff.power * int(target.specialVars["ironHealth"])/100)
                            if critRate > 100:
                                critBonus = critBonus * critRate/100
                            healPowa = int(healPowa/critBonus)
                            critMsg = " !"
                            self.stats.critHeal += 1
                        self.stats.nbHeal += 1
                        healPowaInit = copy.deepcopy(healPowa)

                        incurableValue, healBonus, attIncurPower = 0, 1+(5/100*int(not(self.auto))), 0
                        for eff in target.effects:
                            if eff.effects.id == incurable.id:
                                incurableValue = max(incurableValue,eff.effects.power)
                            elif eff.effects.id == undeadEff2.id:
                                healBonus += eff.effects.power/100
                                diing = eff
                            elif eff.effects.id == healReciveReductionTmp:
                                healBonus -= healReciveReductionTmp.power/100
                            elif eff.effects.type == TYPE_INDIRECT_DAMAGE and eff.caster.char.aspiration == ATTENTIF:
                                attIncurPower += eff.effects.power
                            elif eff.effects.id in [absEff.id,holmgangEff.id]:
                                healBonus += eff.effects.power/100
                                finded = False
                                for key in healBuffer:
                                    if key == eff.caster:
                                        healBuffer[key][0] += eff.effects.power
                                        finded = True
                                        break
                                if not(finded):
                                    healBuffer[eff.caster] = [eff.effects.power,0]
                                healBuffer["total"] += eff.effects.power
                        for eff in self.effects:
                            if eff.effects.id == healReductionTmp.id:
                                healBonus -= healReductionTmp.power/100
                            elif eff.effects.id == healDoneBonus.id:
                                healBonus += healReductionTmp.power/100
                                finded=False
                                for key in healBuffer:
                                    if key == eff.caster:
                                        healBuffer[key][0] += eff.effects.power
                                        finded = True
                                        break
                                if not(finded):
                                    healBuffer[eff.caster] = [eff.effects.power,0]
                                healBuffer["total"] += eff.effects.power
                            if eff.effects.allStats()[statUsed] > 0:
                                diff = (self.allStats()[statUsed]-eff.effects.allStats()[statUsed])/self.allStats()[statUsed]
                                finded = False
                                for key in healBuffer:
                                    if key == eff.caster:
                                        healBuffer[key][1] += diff
                                        finded = True
                                        break
                                if not(finded):
                                    healBuffer[eff.caster] = [0,diff]

                        healBonus -= (incurableValue/100 + min(attIncurPower/1000,0.3))
                        healBonus = max(healBonus,0.1)

                        healPowa = int(healPowa * (100-target.healResist)/100 * (1 + HEALBONUSPERLEVEL*self.level) * healBonus)
                        overheath = max(0,healPowa - (target.maxHp-target.hp))
                        healPowa = min(target.maxHp-target.hp,healPowa)

                        for ent in healBuffer:
                            if ent != "total":
                                ent.stats.healIncreased += int(min(healPowa*(100-target.healResist)/100*(1 + HEALBONUSPERLEVEL*self.level),target.maxHp-target.hp)-min(target.maxHp-target.hp,healPowaInit*(100-target.healResist)/100*(1 + HEALBONUSPERLEVEL*self.level)*healBuffer[ent][1])) + int(healPowaInit*(1 + HEALBONUSPERLEVEL*self.level)*healBuffer[ent][0]/100)

                        if type(self.char) != octarien:
                            if not(target.auto):
                                target.healResist += int(healPowa/target.maxHp/2.5*100*teamHealReistMul[target.team])
                            else:
                                target.healResist += int(healPowa/target.maxHp/3.5*100*teamHealReistMul[target.team])
                        else:
                            target.healResist += int(healPowa/target.maxHp/1.5*100*teamHealReistMul[target.team])

                        if self.isNpc("Alice Exaltée"):
                            self.specialVars["clemBloodJauge"].value = min(100,self.specialVars["clemBloodJauge"].value+int(healPowa * 0.035))
                    else:
                        incurableValue = 0
                        for eff in target.effects:
                            if eff.effects.id == incurable.id:
                                incurableValue = max(incurableValue,eff.effects.power)
                            elif eff.effects.id == undeadEff2.id:
                                diing = eff

                        healPowa = int(power*(100-incurableValue)/100)
                        healPowaInit = copy.deepcopy(healPowa)

                        if type(self.char) != octarien:
                            target.healResist += int(healPowa/target.maxHp/2.5*100)
                        else:
                            target.healResist += int(healPowa/target.maxHp/1.5*100)

                    healPowa = int(round(healPowa))
                    self.stats.heals += healPowa
                    target.hp += healPowa
                    if diing != None:
                        toReturn += diing.decate(value=healPowa)
                        target.refreshEffects()

                    add = ""
                    if effName != None:
                        add = " ({0})".format(effName)

                    if healPowa > 0:
                        toReturn = f"{self.icon} {icon} → {target.icon} +{separeUnit(healPowa)} PV{critMsg}\n"

                        for team in [0,1]:
                            for jaugeEnt, jaugeEff in teamJaugeDict[team].items():
                                for conds in jaugeEff.effects.jaugeValue.conds:
                                    if conds.type == INC_ALLY_HEALED and jaugeEnt.team == self.team:
                                        jaugeEff.value = min(jaugeEff.value+(conds.value*healPowa/target.maxHp),100)
                                    elif conds.type == INC_ENEMY_HEALED and jaugeEnt.team != self.team:
                                        jaugeEff.value = min(jaugeEff.value+(conds.value*healPowa/target.maxHp),100)

                        try:
                            for conds in teamJaugeDict[self.team][self].effects.jaugeValue.conds:
                                if conds.type == INC_DEAL_HEALING:
                                    teamJaugeDict[self.team][self].value = min(teamJaugeDict[self.team][self].value+(conds.value*healPowa/target.maxHp),100)
                        except KeyError:
                            pass

                    if self.char.aspiration in [IDOLE,VIGILANT,ALTRUISTE] and overheath > 0:
                        tabli,tabla = [idoOHArmor,proOHArmor,altOHArmor],[self.specialVars["ohIdo"],self.specialVars["ohPro"],self.specialVars["ohAlt"]]
                        for carillon in (0,1,2):
                            if tabla[carillon]:
                                effect = tabli[carillon]
                                effect.overhealth = int(overheath * ([idoOHEff.power,proOHEff.power,altOHEff.power][carillon]/100))
                                toReturn += add_effect(self,target,effect,[idoOHEff.name,proOHEff.name,altOHEff.name][carillon],True)
                                target.refreshEffects()
                                return toReturn, 0

                    if self.isNpc(["Lio","Kitsune"]) and type(target.char != classes.invoc):
                        toReturn += add_effect(self,target,charming2,self.char.weapon.effects.emoji[0][0],skillIcon=self.char.weapon.effects.emoji[0][0],effPowerPurcent=[100,50][actTurn!=self])
                        target.refreshEffects()

                    for eff in target.effects:
                        if eff.effects.id == shareTabl[0].id and mono:
                            entEmList = ""
                            for ent in target.cell.getEntityOnArea(area=eff.effects.area,team=target.team,wanted=ALLIES,directTarget=False,fromCell=actTurn.cell):
                                tempHeal = int(min(ent.maxHp-ent.hp,healPowa*eff.effects.power/100))
                                eff.caster.stats.heals += tempHeal
                                ent.hp += tempHeal
                                add = " (Partage)"
                                if tempHeal > 0:
                                    entEmList += ent.icon
                            if entEmList != "":
                                toReturn += f"{eff.caster.icon} {eff.icon} → {entEmList} +{int(healPowa*eff.effects.power/100)} PV{add}\n"
                        elif eff.effects.id == zelianR.id:
                            eff.value += int(healPowa * eff.effects.power / 100)

                if aff:
                    return toReturn, healPowa
                else:
                    return "", healPowa

            def isNpc(self, name : str) -> bool:
                """Return if the entity is a temp's with the name given"""
                if type(name) != list:
                    name = [name]
                for namy in name:
                    if self.char.isNpc(namy):
                        return True
                return False

            def getCellToMove(self,cellToMove:cell=None):
                if cellToMove == None:
                    tablOfEnt = self.cell.getEntityOnArea(area=AREA_ALL_ENEMIES-int(self.char.weapon.target==ALLIES),team=self.team,wanted=self.char.weapon.target,lineOfSight=self.char.weapon.target==ENEMIES,fromCell=actTurn.cell,ignoreInvoc = True,directTarget=True)
                    if len(tablOfEnt) == 0:
                        return None
                    tablOfEnt.sort(key=lambda ent:self.cell.distance(ent.cell))
                    cellToMove = tablOfEnt[0].cell
                surrondings = self.cell.surrondings()
                canMove = [surrondings[0] != None and surrondings[0].on == None, surrondings[1] != None and surrondings[1].on == None, surrondings[2] != None and surrondings[2].on == None, surrondings[3] != None and surrondings[3].on == None]
            
                if self.cell.x - cellToMove.x > 0 and canMove[0]:                # If the target is forward and we can move forward
                    return surrondings[0]
                elif self.cell.x - cellToMove.x < 0 and canMove[1]:              # Elif the target is behind and we can move behind
                    return surrondings[1]
                elif self.cell.y - cellToMove.y > 0 and canMove[2]:              # Elif the target is above and we can move up
                    return surrondings[2]
                elif self.cell.y - cellToMove.y < 0 and canMove[3]:              # Elif the target is under and we can move down
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
                if target.chained:
                    return toReturn
                cellDif, axis = (self.cell.x - target.cell.x, self.cell.y - target.cell.y), getDirection(target.cell,self.cell)

                posArea = []
                for cellule in tablAllCells:
                    temp = (target.cell.x - cellule.x, target.cell.y - cellule.y)
                    if (temp[0] == 0 or temp[1] == 0) and (temp[0] != temp[1]):
                        temp2 = [temp[0] < 0, temp[0] > 0, temp[1] < 0, temp[1] > 0]
                        tablLineTeamGround = [FROM_LEFT,FROM_RIGHT,FROM_UP,FROM_DOWN]
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
                
                liaExBuff = 1 + 0.3*int(self.isNpc("Lia Ex"))

                toReturn = "__{0} ({1})__ est repoussé{3} de {2} case{4} en arrière\n".format(target.char.name,target.icon,power,target.accord(),["","s"][int(power>1)])

                if cmpt < power:
                    lastingPower = power-initTagetCell.distance(cellToPush)

                    stat,damageBase = -100,10*lastingPower*liaExBuff

                    for stats in self.allStats():
                        if not(type(self.char) == octarien and self.char.oneVAll and stats == self.allStats()[ENDURANCE]):
                            stat = max(stats,stat)

                    badaboum = [target]
                    if cmpt < len(posArea) and posArea[cmpt].on != None:
                        badaboum.append(posArea[cmpt].on)
                    for boom in badaboum:
                        damage = indirectDmgCalculator(self,boom,damageBase,HARMONIE,[100,danger][self.team==1],AREA_MONO)
                        toReturn += self.indirectAttack(boom,value=damage,name="Collision")

                return toReturn

            def jumpBack(self, power:int, fromCell:cell):
                toReturn = ""
                if self.chained:
                    return toReturn

                cellDif, axis = (self.cell.x - fromCell.x, self.cell.y - fromCell.y), getDirection(fromCell,self.cell)
                posArea = []
                for cellule in tablAllCells:
                    temp = (fromCell.x - cellule.x, fromCell.y - cellule.y)
                    if (temp[0] == 0 or temp[1] == 0) and (temp[0] != temp[1]):
                        temp2 = [temp[0] < 0, temp[0] > 0, temp[1] < 0, temp[1] > 0]
                        tablLineTeamGround = [FROM_RIGHT,FROM_LEFT,FROM_DOWN,FROM_UP]
                        for cmpt in (0,1,2,3):
                            if temp2[cmpt] and axis == tablLineTeamGround[cmpt] and fromCell.distance(cellule) <= power:
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

                return toReturn

            def pull(self, target, power:int):
                toReturn = ""
                if target.chained:
                    return toReturn
                cellDif, axis = (self.cell.x - target.cell.x, self.cell.y - target.cell.y), getDirection(target.cell,self.cell)

                posArea = []
                for cellule in tablAllCells:
                    temp = (target.cell.x - cellule.x, target.cell.y - cellule.y)
                    if (temp[0] == 0 or temp[1] == 0) and (temp[0] != temp[1]):
                        temp2 = [temp[0] > 0, temp[0] < 0, temp[1] > 0, temp[1] < 0]
                        tablLineTeamGround = [FROM_LEFT,FROM_RIGHT,FROM_UP,FROM_DOWN]
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
                if cmpt > 0:
                    toReturn = "\n__{0} ({1})__ est attiré{3} vers {4}\n".format(target.char.name,target.icon,power,target.accord(),self.char.name)

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

            def smnDepl(self,depl,cell):
                if cell.depl == None:
                    depl = copy.deepcopy(depl)
                    deplEnt = entity(identifiant=self.id, perso = depl, team=self.team, player=False, auto=True, danger=100 ,summoner=self, dictInteraction=dictIsNpcVar, cell=cell)
                    cell.depl = deplEnt
                    deplTabl.append([deplEnt,cell,cell.getArea(area=depl.skills.area,team=self.team,fromCell=cell)])
                    self.stats.nbSummon += 1

            def counter(self,target,counterOnDodge):
                try:
                    canCounter = target not in counterTracker[self]
                except KeyError:
                    counterTracker[self] = []
                    canCounter = True
                
                if canCounter:
                    actStat, tablActStats = ACT_INDIRECT, [self.negativeHeal,self.negativeBoost,self.negativeShield,self.negativeDirect,self.negativeIndirect]
                    for cmpt in range(len(tablActStats)):
                        if tablActStats[cmpt] < tablActStats[actStat]:
                            actStat = cmpt 

                    counterDmgBuff = max(0,counterOnDodge/100)
                    if self.isNpc("Lia Ex"):
                        counterDmgBuff += 0.3

                    damage = indirectDmgCalculator(self, target, COUNTERPOWER*(1+counterDmgBuff), HARMONIE, danger, area=AREA_MONO, useActionStat=actStat)
                    counterTracker[self].append(self)
                    return self.indirectAttack(target,value=damage,icon = self.counterEmoji,name="Contre Attaque")
                else:
                    return ""

        class fightEffect:
            """Classe plus pousée que Effect pour le combat"""
            def __init__(self,id,effect : classes.effect, caster : entity, on : entity, turnLeft : int, trigger : int, type : int, icon : str, value=1, effReducPurcent:Union[None,int]=None):
                """self.id : int -> Id de l'effet
                self.effects : effect -> L'effet de base
                self.caster : entity -> L'entité qui donne l'effet
                self.on : entity -> L'entité sur laquel se trouve cet effet
                self.turnLeft : int -> Nombre de tour restant à l'effet
                self.trigger : const -> L'événement qui déclanche l'effet
                self.icon : str -> L'id de l'emoji correspondant à l'effet"""
                self.effects: classes.effect = copy.deepcopy(effect)

                if effReducPurcent != None:
                    self.effects.power = int(self.effects.power*effReducPurcent/100)
                else:
                    effReducPurcent = 100
                self.caster:entity = caster
                self.on:entity = on
                self.turnLeft = turnLeft
                self.trigger = trigger
                self.type = type
                if value != 1:
                    self.value = value
                else:
                    self.value = [1,0][self.effects.unclearable]

                if self.effects.id == deterEff1.id:
                    self.value = int(on.maxHp * self.effects.power / 100)

                self.id = id
                self.icon = icon
                self.remove = False
                self.stun:bool = effect.stun
                self.name = effect.name
                self.replicaTarget: Union[None,entity] = None

                tablTemp = [0,0,0,0,0,0,0,0,0]

                if self.caster.char.element == ELEMENT_TIME and self.effects.type == TYPE_INDIRECT_HEAL:
                    self.effects.power = int(self.effects.power*1.2)

                if self.effects.stat not in [None,FIXE,PURCENTAGE]:
                    if self.effects.stat is not HARMONIE:
                        temp = self.caster.allStats()[self.effects.stat]
                    else:
                        temp = -111
                        for a in self.caster.allStats():
                            temp = max(temp,a)

                    valueBoost, valueResis = (1 + min(self.caster.char.level,200)//10/10 - 1 + caster.valueBoost(on)) * (temp+100-self.caster.negativeBoost)/100, caster.valueBoost(on) * (temp+100-self.caster.negativeShield)/100

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

                tablTemp[0] += self.effects.strength * valueBoost * effReducPurcent * 0.01
                tablTemp[1] += self.effects.endurance * valueBoost * effReducPurcent * 0.01
                tablTemp[2] += self.effects.charisma * valueBoost * effReducPurcent * 0.01
                tablTemp[3] += self.effects.agility * valueBoost * effReducPurcent * 0.01
                tablTemp[4] += self.effects.precision * valueBoost * effReducPurcent * 0.01
                tablTemp[5] += self.effects.intelligence * valueBoost * effReducPurcent * 0.01
                tablTemp[6] += self.effects.resistance * valueBoost * effReducPurcent * 0.01
                tablTemp[7] += self.effects.percing * valueBoost * effReducPurcent * 0.01
                tablTemp[8] += self.effects.critical * valueBoost * effReducPurcent * 0.01

                for cmpt in range(8):
                    tablTemp[cmpt] = [min(tablTemp[cmpt],0),max(tablTemp[cmpt],0)][self.effects.type == TYPE_BOOST]

                self.inkResistance = min(effect.inkResistance * valueResis,effect.inkResistance*3)

                self.tablAllStats = tablTemp
                self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.resistance,self.percing,self.critical = tuple(tablTemp)

                if self.effects.id in [vulne.id,dmgDown.id,dmgUp.id,defenseUp.id] and self.effects.stat != None:
                    power = self.effects.power
                    secElemMul = 1
                    if caster.char.secElement in [ELEMENT_AIR, ELEMENT_UNIVERSALIS_PREMO]:
                        secElemMul += 0.05
                    if on.char.secElement in [ELEMENT_AIR, ELEMENT_UNIVERSALIS_PREMO]:
                        secElemMul += 0.05
                    self.effects.power = min(power * (100+caster.allStats()[self.effects.stat]-caster.negativeBoost)/100 * (self.caster.char.level//10/10 - 1 + caster.valueBoost(on)), power * 10)
                elif self.effects.id in [vampirismeEff.id] and self.effects.stat != None:
                    power = self.effects.power
                    secElemMul = 1
                    if caster.char.secElement in [ELEMENT_FIRE, ELEMENT_UNIVERSALIS_PREMO]:
                        secElemMul += 0.05
                    if on.char.secElement in [ELEMENT_WATER, ELEMENT_UNIVERSALIS_PREMO]:
                        secElemMul += 0.05
                    if self.effects.stat == HARMONIE:
                        maxStats = max(caster.allStats())
                    else:
                        maxStats = caster.allStats()[self.effects.stat]
                    self.effects.power = power * (100+maxStats-caster.negativeHeal)/100 * (1 + caster.valueBoost(on,heal=True))

            def decate(self,turn=0,value=0) -> str:
                """Réduit le turnLeft ou value de l'effet"""
                self.turnLeft -= turn
                self.value -= value
                temp = ""

                if (self.turnLeft <= 0 and self.effects.turnInit > 0) or self.value <= 0 and not(self.effects.unclearable):
                    if self.trigger == TRIGGER_ON_REMOVE:
                        temp += self.triggerRemove()
                    self.remove = True
                    if not(self.effects.silent) and self.on.hp > 0 and self.effects.id not in (astralShield.id,timeShield.id):
                        temp += f"__{self.on.char.name}__ n'est plus sous l'effet __{self.effects.name}__\n"

                    if self.effects.id == undeadEff2.id and self.turnLeft == 0:
                        self.on.hp = 0
                        temp += self.on.death(killer=self.on)
                    elif self.effects.id == elemShieldEff.id and self.value <= 0:
                        temp += groupAddEffect(self.caster, self.on, self.effects.callOnTrigger,self.effects.area,self.icon,ACT_SHIELD)
                return temp

            def triggerDamage(self,value=0,icon="",declancher = 0,onArmor = 1) -> list:
                """Déclanche l'effet"""
                value = round(value)
                temp2 = [value,""]

                if self.effects.overhealth > 0 and value > 0 and self.value > 0:
                    shieldPAr, returnDmg, toReturnTxt = self.value, value, ""
                    if not(self.effects.absolutShield):
                        if self.on.char.secElement in [ELEMENT_EARTH, ELEMENT_UNIVERSALIS_PREMO]:
                            onArmor += 0.05
                        if self.caster.char.secElement in [ELEMENT_EARTH, ELEMENT_UNIVERSALIS_PREMO]:
                            onArmor += 0.05
                    dmgRecived = round(value * onArmor)

                    if dmgRecived >= shieldPAr:
                        declancher.stats.damageOnShield += shieldPAr
                        self.caster.stats.armoredDamage += shieldPAr
                        self.on.stats.damageProtected += shieldPAr
                        addedReduc = [self.on.char.level,0][self.effects.lightShield]
                        if self.caster.specialVars["osPre"]:
                            addedReduc += self.caster.char.level * (preOSEff.power/100)
                        elif self.caster.specialVars["osIdo"] or self.caster.specialVars["osPro"]:
                            addedReduc += self.caster.char.level * (idoOSEff.power/100)

                        returnDmg = int((shieldPAr+addedReduc)/onArmor)
                        toReturnTxt = ["<:abB:934600555916050452> ","<:abR:934600570633867365> "][self.on.team] + "-" + str(shieldPAr)+" PAr "
                        self.decate(value=shieldPAr)
                        return (returnDmg,toReturnTxt)
                    else:
                        declancher.stats.damageOnShield += shieldPAr
                        self.caster.stats.armoredDamage += shieldPAr
                        self.on.stats.damageProtected += shieldPAr
                        returnDmg = value
                        toReturnTxt = self.icon + "-" + str(dmgRecived)+" PAr "
                        self.decate(value=dmgRecived)
                        return (returnDmg,toReturnTxt)

                elif self.effects.redirection > 0 and value > 0:
                    if self.caster.hp > 0:
                        valueT = value
                        redirect = int(valueT * self.effects.redirection/100)
                        declancher.indirectAttack(target=self.caster,value=redirect,icon=icon,ignoreImmunity=False,name=self.effects.name,canCrit=False)
                        return (redirect,"{0} -{1} PV".format(self.caster.icon,redirect))
                    else:
                        return (0,"")

                elif (self.type == TYPE_INDIRECT_DAMAGE or self.effects.id in [rosesPhysiEff.id,rosesMagicEff.id,lightLameEff.id,astralLameEff.id,timeLameEff.id,mattSkill4Eff.id]) and self.value>0:
                    if self.effects.onDeclancher:
                        target = declancher
                    else:
                        target = self.on

                    temp2[1] = self.triggeredIndDamage([self.on,declancher][self.effects.onDeclancher])

                elif self.type == TYPE_UNIQUE:
                    if self.effects.id == enchant.id :
                        self.effects.magie += 5

                if self.effects.callOnTrigger != None:
                    temp2[1] = ""
                    if self.effects.id != "nt":
                        if type(self.on.char) not in [invoc, depl]:
                            eff = findEffect(self.effects.callOnTrigger)
                            add_effect(self.caster,self.on,eff,skillIcon=self.icon)

                            temp2[1] += "\n{1} +{0} {2}\n".format(eff.emoji[self.on.char.species-1][self.on.team],self.on.icon,eff.name)                            
                            self.on.refreshEffects()
                        temp2[1] += f"{self.decate(value=1)}"
                    else:
                        eff = findEffect(self.effects.callOnTrigger)
                        add_effect(self.caster,declancher,eff)
                        temp2[1] += "\n{1} +{0} {2}\n".format(eff.emoji[self.on.char.species-1][self.on.team],declancher.icon,eff.name)                        
                        declancher.refreshEffects()

                return temp2

            def triggerDeath(self,killer=None) -> str:
                """Déclanche l'effet"""
                toReturn = ""
                if self.type==TYPE_INDIRECT_REZ:
                    self.on.status = STATUS_RESURECTED
                    self.caster.stats.allieResurected += 1

                    if self.effects.stat == None:
                        heal = self.effects.power

                    elif self.effects.stat == PURCENTAGE:
                        heal = round(self.on.maxHp * self.effects.power /100)

                    self.on.hp = heal
                    self.caster.stats.heals += heal
                    toReturn += f"{self.on.char.name} ({self.on.icon}) est réanimé{self.on.accord()} !\n{self.caster.icon} {self.icon}→ {self.on.icon} +{heal} PV\n"
                    self.decate(value=1)

                elif self.type == TYPE_INDIRECT_DAMAGE and self.value> 0:
                    variable = self.triggeredIndDamage(self.on)

                elif self.type == TYPE_UNIQUE:
                    if self.effects == hunter:
                        add_effect(self.on,self.on,hunterBuff)
                        self.on.refreshEffects()
                        tempi, useless = self.on.attack(target=killer,value = self.on.char.weapon.power,icon = self.on.char.weapon.emoji,onArmor=self.on.char.weapon.onArmor)
                        toReturn += tempi

                if self.effects.callOnTrigger != None:
                    toReturn += add_effect(self.on,self.on,findEffect(self.effects.callOnTrigger))
                    
                self.decate(value=1)

                return toReturn

            def triggerStartOfTurn(self,danger,decate=True) -> str:
                """Déclanche l'effet"""
                funnyTempVarName=""
                if self.type == TYPE_INDIRECT_HEAL and self.on.hp > 0:              # Heal Indirect
                    return self.triggeredIndHeal()

                elif self.type == TYPE_INDIRECT_DAMAGE and self.value > 0 and ((self.effects.area==AREA_MONO and self.on.hp > 0) or self.effects.area != AREA_MONO) and self.on != None:            # Damage indirect
                    funnyTempVarName = self.triggeredIndDamage(self.on,decate)

                    if self.effects.id == lieSkillEff.id and self.value > 0:
                        effTemp = lieSkillEff
                        effTemp.turnInit,effTemp.lvl = self.turnLeft, self.value

                        funnyTempVarName += add_effect(self.caster,self.on,effTemp)
                        self.on.refreshEffects()

                    if self.effects.id in [infection.id,epidemicEff.id]:                              # If it's the infection poisonnus effect
                        tempTabl = self.on.cell.getEntityOnArea(area=AREA_DONUT_1,team=self.caster.team,wanted=ENEMIES,effect=[self.effects],directTarget=False,fromCell=actTurn.cell)
                        if len(tempTabl) > 0:
                            funnyTempVarName += "L'{0} se propage...\n".format(self.effects.name)
                            for ent in tempTabl:
                                funnyTempVarName += add_effect(self.caster,ent,self.effects,effPowerPurcent=85)
                                add_effect(self.caster,ent,self.effects.reject[0])
                                ent.refreshEffects()

                elif self.type == TYPE_BOOST and self.on.hp > 0:                    # Indirect Armor
                    funnyTempVarName += add_effect(self.caster,self.on,findEffect(self.effects.callOnTrigger))
                    self.on.refreshEffects()
                return funnyTempVarName

            def triggerEndOfTurn(self,danger,decate=True) -> str:
                """Trigger the effect"""
                temp = ""
                if self.type == TYPE_INDIRECT_DAMAGE and self.value > 0:                               # The only indirect damage effect for now is a insta death
                    temp = self.triggeredIndDamage(self.on,decate)
                elif self.type == TYPE_UNIQUE:                                      # Poids Plume effect bonus reduce
                    if self.effects == poidPlumeEff:
                        self.value = self.value//2

                elif self.type == TYPE_INDIRECT_HEAL and self.on.hp > 0:            # End of turn healing (aka Light Aura 1)
                    return self.triggeredIndHeal()
                if self.effects.callOnTrigger != None:
                    temp += groupAddEffect(self.caster, self.on, self.effects.area, self.effects.callOnTrigger, self.icon, actionStats=[ACT_BOOST,ACT_SHIELD][self.effects.callOnTrigger.type == TYPE_ARMOR])
                return temp

            def triggerRemove(self) -> str:
                """Trigger the effect when it's removed\n
                For now, only unique effect activly use it, but some boost effect use it to"""
                message = ""

                if self.type == TYPE_UNIQUE:
                    if self.effects.id == lostSoul.id:                                   # Remove the body effect
                        if self.on.status == STATUS_DEAD:
                            self.on.status = STATUS_TRUE_DEATH
                            message="{0} est hors combat !\n".format(self.on.char.name)

                elif self.type == TYPE_INDIRECT_DAMAGE:
                    message = self.triggeredIndDamage(self.on,decate=False)
                elif self.type == TYPE_INDIRECT_HEAL and self.on.hp > 0:
                    if self.effects.id == zelianR.id:
                        if self.value > 0:
                            message += self.caster.heal(self.on, self.icon, FIXE, self.value, self.name, mono = True)[0]
                    else:
                        return self.triggeredIndHeal()
                if self.effects.callOnTrigger != None:                               # If the effect give another effect when removed, give that another effect
                    message += groupAddEffect(self.caster, self.on, self.effects.area, self.effects.callOnTrigger, skillIcon=self.icon)
                    if findEffect(self.effects.callOnTrigger).id == temNativTriggered.id:
                        self.on.icon, self.on.char.icon = '<:colegue:895440308257558529>','<:colegue:895440308257558529>'

                return message

            def triggerInstant(self,danger) -> str:
                """Déclanche l'effet"""
                funnyTempVarName, decate ="", True
                if self.type == TYPE_INDIRECT_HEAL and self.on.hp > 0:              # Heal Indirect
                    return self.triggeredIndHeal()

                elif self.type == TYPE_INDIRECT_DAMAGE and self.value > 0 and ((self.effects.area==AREA_MONO and self.on.hp > 0) or self.effects.area != AREA_MONO) and self.on != None:            # Damage indirect
                    funnyTempVarName = self.triggeredIndDamage(self.on,decate)

                if self.effects.callOnTrigger != None:
                    funnyTempVarName = groupAddEffect(caster=self.caster, target=self.on, area=self.area, effect=self.effects.callOnTrigger, skillIcon=self.icon)

                return funnyTempVarName

            def allStats(self):
                return self.tablAllStats

            def triggeredIndDamage(self,target,decate=True):
                toReturn = ""
                damageBase = self.effects.power
                if self.effects.stat == None:
                    stat = None
                else:
                    stat = self.caster.allStats()[self.effects.stat]-self.caster.negativeIndirect

                tablTarget = target.cell.getEntityOnArea(area=self.effects.area,team=target.team,wanted=[ALLIES,ENEMIES][target.team == self.caster.team and target != self.caster],directTarget=False,fromCell=self.caster.cell)

                for entityInArea in tablTarget:
                    reduc = 1
                    if entityInArea != target:
                        reduc = max(AOEMINDAMAGE,1-target.cell.distance(entityInArea.cell)*AOEDAMAGEREDUCTION)

                    toReturn += self.caster.indirectAttack(entityInArea,value=indirectDmgCalculator(self.caster, target, self.effects.power*reduc, self.effects.stat, danger, area=self.effects.area),icon = self.icon, name=self.effects.name, canCrit=self.effects.stat!=None)

                if decate:
                    toReturn += self.decate(value=1)

                if self.caster.isNpc("Liz") or (self.caster.isNpc("Kitsune") and type(self.on.char != classes.invoc) and ((skillToUse != None and skillToUse.id != kitsuneSkill4.id)or(skillToUse == None))):
                    toReturn += groupAddEffect(caster=self.caster, target=self.on, area=tablTarget, effect=charming, skillIcon=self.caster.char.weapon.effects.emoji[0][0], effPurcent=50)
                return toReturn

            def triggeredIndHeal(self):
                toReturn, tablTargets = "", self.on.cell.getEntityOnArea(area=self.effects.area,team=self.caster.team,wanted=ALLIES,directTarget=False,fromCell=self.on.cell)

                for entityInArea in tablTargets:
                    funnyTempVarName, useless = self.caster.heal(entityInArea,self.icon,self.effects.stat,[self.effects.power,self.value][self.effects.trigger==TRIGGER_ON_REMOVE and self.effects.stat==None],self.effects.name,danger)
                    toReturn += funnyTempVarName

                return toReturn

        def add_effect(caster: entity,target: entity,effect: classes.effect,start: str = "", ignoreEndurance=False, danger=danger, setReplica : Union[None,entity] = None, effPowerPurcent=100, useActionStats = ACT_SHIELD, skillIcon=""):
            """Méthode qui rajoute l'effet Effet à l'entity Target lancé par Caster dans la liste d'attente des effets"""
            if type(target) == entity and not(type(target.char) == depl) or type(effect) == classes.effect:
                valid,id,popipo = False,0,""
                valid = True
                turn = caster.stats.survival
                if effect.id == elemEff.id:
                    effect = tablElemEff[target.char.element]
                elif effect.id == lightStun.id and (type(target.char) == octarien and (target.char.oneVAll or target.name in ENEMYIGNORELIGHTSTUN)):
                    return "{0} est immunisé{1} aux étourdissements\n".format(target.name,target.accord())
                # Does the effect can be applied ?
                
                if not(effect.stackable and effect.reject == None):               
                    if effect.reject != None:                                           # The effect reject other effects
                        for a in effect.reject:
                            for b in target.effects:
                                if a == b.effects.id:
                                    popipo = f"{caster.icon} {effect.emoji[caster.char.species-1][caster.team]} → 🚫{findEffect(a).emoji[caster.char.species-1][caster.team]} {target.icon}\n"
                                    valid = False
                                    break
                            if not(valid):
                                break
                    if not(effect.stackable):
                        for a in target.effects:
                            if a.effects.id == effect.id:          # The effect insn't stackable
                                if a.effects.id == incurable.id:                                 # But is't Healn't
                                    if a.effects.power < effect.power:                               # A better Healn't
                                        diff = effect.power - a.effects.power
                                        a.effects.power = effect.power
                                        a.caster = caster
                                        popipo = f"{caster.icon} → {a.effects.emoji[caster.char.species-1][caster.team]}+{diff} {target.icon}\n"
                                    valid = False

                                elif a.effects.id in [idoOHArmor.id,proOHArmor.id,altOHArmor.id,"clemExOvershield"]:  # Overhealth Shield
                                    if a.value < effect.overhealth:                               # A better Overhealth shield
                                        diff = separeUnit(effect.overhealth - a.value)
                                        a.value = effect.overhealth
                                        a.caster = caster
                                        a.turnLeft = effect.turnInit
                                        popipo = f"{caster.icon} {effect.emoji[caster.char.species-1][caster.team]} → {target.icon} {a.effects.emoji[caster.char.species-1][caster.team]} +{diff} PAr\n"
                                    valid = False

                                elif not(effect.silent):                                        # It's not Healn't
                                    popipo = f"{caster.icon} {effect.emoji[caster.char.species-1][caster.team]} → 🚫{a.effects.emoji[caster.char.species-1][caster.team]} {target.icon}\n"
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
                    elif effect.id == constEff.id:
                        actPVPurcent = target.hp / target.maxHp
                        if effect.stat in [None,FIXE]:
                            boostHp = effect.power
                        elif effect.stat == PURCENTAGE:
                            boostHp = int(target.maxHp*(1+(effect.power/100)))
                        else:
                            if useActionStats == None:
                                useActionStats = ACT_BOOST
                            boostHp = effect.power * (100+(caster.allStats()[effect.stat]+[caster.negativeHeal,caster.negativeBoost,caster.negativeShield,caster.negativeDirect,caster.negativeIndirect][useActionStats]))/100

                        target.maxHp = target.maxHp + boostHp
                        target.hp = int(target.maxHp * actPVPurcent)
                        toAppend = fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,effect.type,icon,boostHp,effPowerPurcent)
                        addEffect.append(toAppend)
                        target.refreshEffects()

                        if not(effect.silent):
                            return f"{caster.icon} {skillIcon} → {target.icon} +{icon} __{effect.name}__({boostHp})\n"
                        else:
                            return ""
                    elif effect.id == aconstEff.id:
                        actPVPurcent = target.hp / target.maxHp
                        if effect.stat in [None,FIXE]:
                            boostHp = effect.power
                        elif effect.stat == PURCENTAGE:
                            boostHp = int(target.maxHp*(1+(effect.power/100)))
                        else:
                            if useActionStats == None:
                                useActionStats = ACT_BOOST
                            boostHp = effect.power * (100+(caster.allStats()[effect.stat]+[caster.negativeHeal,caster.negativeBoost,caster.negativeShield,caster.negativeDirect,caster.negativeIndirect][useActionStats]))/100

                        target.maxHp = target.maxHp - boostHp
                        target.hp = int(target.maxHp * actPVPurcent)
                        toAppend = fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,effect.type,icon,boostHp,effPowerPurcent)
                        addEffect.append(toAppend)
                        target.refreshEffects()

                        if not(effect.silent):
                            return f"{caster.icon} {skillIcon} → {target.icon} +{icon} __{effect.name}__(-{boostHp})\n"
                        else:
                            return ""

                    if effect.overhealth > 0:                                       # Armor Effect
                        temp = caster.allStats()
                        value, critMsg = effect.overhealth * (1+LIGHTHEALBUFF/100*(caster.char.element == ELEMENT_LIGHT)), ""
                        if effect.id == chaosArmorEff.id:
                            value = random.randint(10,50)
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

                        if effect.stat != None:   # Classical armor effect
                            if effect.stat == HARMONIE:
                                maxi = -100
                                for randomVar in caster.allStats():
                                    maxi = max(maxi,randomVar)
                                stati = maxi
                            else:
                                stati = caster.allStats()[effect.stat]

                            value = round(value * secElemMul * caster.valueBoost(target=target,armor=True) * (1+(stati-caster.actionStats()[useActionStats])/100) * (1+(target.endurance/1500)) * friablility * dangerBoost * (1 - (ARMORMALUSATLVL0/100) + (ARMORLBONUSPERLEVEL*caster.level)) * teamArmorReducer[target.team])

                            critRate = probCritHeal(caster,target)
                            if random.randint(0,99) < critRate:
                                critBonus = 1.25 + (preciChiEff.power * int(caster.specialVars["preci"])/100) + (ironHealthEff.power * int(target.specialVars["ironHealth"])/100)
                                if critRate > 100:
                                    critBonus = critBonus * critRate/100
                                value = int(value*critBonus)
                                caster.stats.critHeal += 1
                            caster.stats.nbHeal += 1
                        else:                                                           # Fixe armor effect
                            value = round(effect.overhealth)

                        tmpBalancing = 1
                        for eff in caster.effects:
                            if eff.effects.id == armorReductionTmp.id:
                                tmpBalancing -= armorReductionTmp.power/100
                        value = int(value*tmpBalancing)
                        caster.stats.shieldGived += value

                        toAppend = fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,TYPE_ARMOR,icon,value)
                        if setReplica != None:
                            toAppend.replicaTarget = setReplica

                        addEffect.append(toAppend)

                        if not(effect.silent):
                            tempTurn = effect.turnInit+int(caster.char==ELEMENT_TIME)
                            popipo = f"{caster.icon} {skillIcon} → {target.icon} {icon} +{separeUnit(value)} PAr{critMsg}\n"

                    else:                                                           # Any other effect
                        if effect.id == kikuRaiseEff.id and ((type(target.char)==octarien and (not(target.char.rez) or target.status == STATUS_RESURECTED)) or target.isNpc("Chûri")):
                            effect = kikuUnlifeGift
                        
                        if (effect.type == TYPE_INDIRECT_DAMAGE and effect.trigger in [TRIGGER_START_OF_TURN,TRIGGER_END_OF_TURN] and caster.char.element == ELEMENT_DARKNESS):
                            effPowerPurcent += DARKNESSDMGBUFF
                        elif (effect.type == TYPE_INDIRECT_HEAL and caster.char.element == ELEMENT_TIME):
                            effPowerPurcent += TIMEHEALBUFF
                        elif (effect.type == TYPE_INDIRECT_DAMAGE and effect.trigger in [TRIGGER_ON_REMOVE] and caster.char.element == ELEMENT_TIME):
                            effPowerPurcent += TIMEDMGBUFF
                        elif (effect.type == TYPE_BOOST and (caster.char.element == ELEMENT_SPACE or target.char.element == ELEMENT_SPACE)):
                            effPowerPurcent += SPACEBONUSBUFF
                        if effPowerPurcent == 100:
                            effPowerPurcent = None

                        toAppend = fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,effect.type,icon,effect.lvl,effPowerPurcent)
                        if effect.trigger != TRIGGER_INSTANT:
                            if setReplica != None:
                                toAppend.replicaTarget = setReplica
                            if effect.id == undeadEff2.id:
                                toAppend.value = target.maxHp//2
                            addEffect.append(toAppend)

                            if effect.id == "clemBloodJauge":
                                caster.specialVars["clemBloodJauge"] = toAppend

                            if not(effect.silent):
                                power = ["", " ({0}%)".format(effPowerPurcent)][effPowerPurcent!=None]
                                popipo = f"{caster.icon} {skillIcon} → {target.icon} +{icon} __{effect.name}__{power}\n"

                            if effect.id == lightStun.id and type(target.char) in [tmpAllie,char]:
                                toAppend = fightEffect(id+1,imuneLightStun,caster,target,imuneLightStun.turnInit,imuneLightStun.trigger,imuneLightStun.type,imuneLightStun.emoji[caster.char.species-1][caster.team],imuneLightStun.lvl,effPowerPurcent)
                                addEffect.append(toAppend)
                            target.refreshEffects()

                            tablTemp = [altOHEff.id,proOHEff.id,idoOHEff.id,idoOSEff.id,proOSEff.id,preOSEff.id,heriteEstialbaEff.id,heriteLesathEff.id,floorTanking.id,summonerMalus.id,foulleeEff.id,preciChiEff.id,ironHealthEff.id,liaCounterSkillEff.id,exploHealMarkEff.id]
                            nameTemp = ["ohAlt","ohPro","ohIdo","osIdo","osPro","osPre","heritEstial","heritLesath","tankTheFloor","summonerMalus","foullee","preci","ironHealth","liaBaseDodge","exploHeal"]
                            tablTempEff = [physicRuneEff.id,magicRuneEff.id, eventFas.id, convictionVigilantEff.id,convicProEff.id]
                            nameTempEff = ["damageSlot","damageSlot","fascination","convicVigil","convicPro"]

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
                                caster.specialVars["aspiSlot"] = bloodPactEff.power
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
                            elif effect.id in [haimaEffect.id,pandaimaEff.id]:
                                temp, eff = caster.allStats(), effect.callOnTrigger
                                value, critMsg = eff.overhealth, ""
                                friablility = max(1-(turn / 30),0.1)                   # Reduct over time
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

                                value = round(value * secElemMul * caster.valueBoost(target=target,armor=True) * (temp[eff.stat]-caster.actionStats()[useActionStats] +100)*((target.endurance+1250)/1250)/100 * friablility * dangerBoost * (min((1-ARMORMALUSATLVL0/100) + ARMORLBONUSPERLEVEL*caster.level,3)))

                                critRate = probCritHeal(caster,target)
                                if random.randint(0,99) < critRate:
                                    critBonus = 1.25 + (preciChiEff.power * int(caster.specialVars["preci"])/100) + (ironHealthEff.power * int(target.specialVars["ironHealth"])/100)
                                    if critRate > 100:
                                        critBonus = critBonus * critRate/100
                                    value = int(value * (1.25 + (preciChiEff.power * int(caster.specialVars["preci"]) + ironHealthEff.power * int(target.specialVars["ironHealth"])) * 0.01))
                                    critMsg = " !"
                                    caster.stats.critHeal += 1
                                caster.stats.nbHeal += 1

                                for a in target.effects:
                                    if a.type == TYPE_ARMOR:
                                        reduc = 0.5
                                        if caster.specialVars["osPre"]:
                                            reduc = reduc + reduc * (preOSEff.power/2/100)
                                        elif caster.specialVars["osIdo"] or caster.specialVars["osPro"]:
                                            reduc = reduc + reduc * (idoOSEff.power/2/100)

                                        value = round(value*reduc)
                                        break

                                tmpBalancing = 1
                                for eff2 in caster.effects:
                                    if eff2.effects.id == armorReductionTmp.id:
                                        tmpBalancing -= armorReductionTmp.power/100
                                value = int(value*tmpBalancing)
                                caster.stats.shieldGived += value
                                toAppend = fightEffect(id,eff,caster,target,eff.turnInit,eff.trigger,TYPE_ARMOR,eff.emoji[caster.char.species-1][caster.team],value)
                                if setReplica != None:
                                    toAppend.replicaTarget = setReplica

                                addEffect.append(toAppend)
                                target.refreshEffects()

                                if not(eff.silent):
                                    tempTurn = eff.turnInit+int(caster.char==ELEMENT_TIME)
                                    popipo = f"{caster.icon} {skillIcon} → {target.icon} {icon} +{separeUnit(value)} PAr{critMsg}\n"
                        else:
                            popipo = toAppend.triggerInstant(danger)
                if target.hp > 0:
                    return popipo
                else:
                    return ''
            else:
                return ""

        def groupAddEffect(caster:entity, target:entity,area:Union[int,List[entity]],effect:List[classes.effect],skillIcon="",actionStats=ACT_BOOST,effPurcent=100):
            tablName, tablEff, tablIcon, toReturn = [], [], [], ""
            if type(effect) != list:
                effect = [effect]

            for c in effect:
                eff = findEffect(c)
                if eff != None:
                    if type(area) == int:
                        tablToSee = target.cell.getEntityOnArea(area=area,team=caster.team,wanted=[ENEMIES,ALLIES][eff.type in friendlyTypes],directTarget=False,fromCell=caster.cell)
                    else:
                        tablToSee = area
                    for ent in tablToSee:
                        if type(ent) != None:
                            ballerine = add_effect(caster,ent,eff,useActionStats=actionStats,skillIcon=skillIcon,effPowerPurcent=effPurcent)
                            if eff.type == TYPE_ARMOR or eff.trigger==TRIGGER_INSTANT:
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

        for tmp in team1:   # dictIsNpcVar actualisation
            if type(tmp) == tmpAllie:
                for cmpt in tablIsNpcName:
                    if tmp.isNpc(cmpt):
                        dictIsNpcVar[f"{cmpt}"] = True
                        break

        # Teams generations -----------------------------------------------
        if not(bigMap):
            team1.sort(key=lambda star: star.stars, reverse = True)
            starLevel = team1[0].stars
        else:
            starLevel = 0
            for ent in team1:
                starLevel += ent.stars
            starLevel = round(starLevel / len(team1))

        if len(team1) < [8,16][bigMap] and not(octogone) and not(procurFight): # Remplisage de la team1
            aleaMax = len(tablAllAllies)-1
            alreadyFall = []
            lvlMax = 0

            for a in team1:
                lvlMax = max(lvlMax,a.level)

            while len(team1) < [8,16][bigMap]:
                vacantRole = ["DPT1","DPT2","Healer","Booster"]

                for perso in team1:
                    if perso.aspiration in [BERSERK,TETE_BRULE,OBSERVATEUR,POIDS_PLUME,ENCHANTEUR,MAGE] and ("DPT1" in vacantRole):
                        vacantRole.remove("DPT1")
                    elif perso.aspiration in [BERSERK,TETE_BRULE,OBSERVATEUR,POIDS_PLUME,ENCHANTEUR,MAGE] and ("DPT2" in vacantRole):
                        vacantRole.remove("DPT2")
                    elif perso.aspiration in [IDOLE,INOVATEUR,MASCOTTE] and ("Booster" in vacantRole):
                        vacantRole.remove("Booster")
                    elif perso.aspiration in [PREVOYANT,ALTRUISTE,VIGILANT,PROTECTEUR] and ("Healer" in vacantRole):
                        vacantRole.remove("Healer")

                tablToSee = []
                if len(vacantRole) <= 0:
                    tablToSee = tablAllieTemp
                else:
                    for role in vacantRole:
                        if role in ["DPT1","DPT2"]:
                            for allie in tablAllieTemp:
                                if allie.aspiration in [BERSERK,TETE_BRULE,OBSERVATEUR,POIDS_PLUME,ENCHANTEUR,MAGE]:
                                    tablToSee.append(allie)
                        elif role == "Healer":
                            for allie in tablAllieTemp:
                                if allie.aspiration in [PREVOYANT,ALTRUISTE,VIGILANT,PROTECTEUR]:
                                    tablToSee.append(allie)
                        elif role == "Booster":
                            for allie in tablAllieTemp:
                                if allie.aspiration in [IDOLE,INOVATEUR,MASCOTTE]:
                                    tablToSee.append(allie)

                temp = random.randint(0,len(tablToSee)-1)
                alea = tablToSee[temp]
                tablAllieTemp.remove(alea)

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
                elif alea.isNpc("Anna") and random.randint(0,99) < 25 and enableMiror:
                    alea = copy.deepcopy(findAllie("Belle"))
                if alea.name in ["Alice","Alice alt.","Ruby","Clémence"]:
                    enableMiror = False
                elif alea.name == "Belle":
                    for allies in tablAllieTemp[:]:
                        if allies.name in ["Alice","Clémence"]:
                            try:
                                tablAllieTemp.remove(allies)
                            except:
                                logs += "\nCouldn't remove Alice or Clemence from the list, somehow"

                for cmpt in tablIsNpcName:
                    if alea.isNpc(cmpt):
                        dictIsNpcVar[f"{cmpt}"] = True
                        break

                alea.changeLevel(lvlMax,stars=starLevel)
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
        team1.sort(key=lambda star: star.level, reverse = True)

        if team2 == []: # Génération de la team 2
            lvlMax = team1[0].level
            if team1[0].isNpc("Clémence Exaltée"):
                lvlMax -= 200
            elif len(team1) > 1 and (team1[0].isNpc("Iliana prê.") or team1[1].isNpc("Iliana prê.")):
                lvlMax += 150
            elif team1[0].isNpc("Lia Ex"):
                lvlMax -= 50
            winStreak = teamWinDB.getVictoryStreak(team1[0])

            # random.randint(0,99) > 10+winStreak
            if random.randint(0,99) > 10+winStreak or (team1[0].isNpc("Clémence Exaltée") or team1[0].isNpc("Lia Ex")): # Vs normal team
                danger = dangerLevel[winStreak] + (starLevel * DANGERUPPERSTAR)

                tablOctaTemp:List[octarien] = copy.deepcopy(tablAllEnnemies)
                if team1[0].isNpc("Lia Ex"):
                    for enmy in tablOctaTemp[:]:
                        if enmy.name in ["Lia","Liu","Liz","Lio"]:
                            tablOctaTemp.remove(enmy)

                oneVAll = False

                tablTeamOctaPos = [0,0,1,1,2,2]+[random.randint(0,2),random.randint(0,2)]
                tablTeamOctaComp = [4,2,2]

                random.shuffle(tablTeamOctaPos)
                if len(team2) < len(team1) and lvlMax >= 15:
                    if random.randint(0,99) < 25:               # Boss ?
                        temp = random.randint(0,len(tablBoss)-1)
                        alea = copy.deepcopy(tablBoss[temp])
                        while team1[0].isNpc("Clémence Exaltée") and alea.isNpc("Clémence pos."):
                            temp = random.randint(0,len(tablBoss)-1)
                            alea = copy.deepcopy(tablBoss[temp])

                        #alea = copy.deepcopy(findEnnemi("Sorcière"))          

                        oneVAll = alea.oneVAll

                        alea.changeLevel(lvlMax)
                        team2.append(alea)
                        logs += "{0} have been added into team2\n".format(alea.name)

                        if alea.isNpc("Luna ex."):
                            alea = copy.deepcopy(findAllie("Shushi Cohabitée"))
                            procurData = procurTempStuff["Shushi Cohabitée"]
                            alea.changeLevel(lvlMax)

                            alea.stuff = [
                                stuff(procurData[1][0],procurData[1][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*lvlMax),int(procurData[4][1][0]*procurData[4][1][1]*lvlMax),int(procurData[4][2][0]*procurData[4][2][1]*lvlMax),int(procurData[4][3][0]*procurData[4][3][1]*lvlMax),int(procurData[4][4][0]*procurData[4][4][1]*lvlMax),int(procurData[4][5][0]*procurData[4][5][1]*lvlMax),int(procurData[4][6][0]*procurData[4][6][1]*lvlMax),int(procurData[4][7][0]*procurData[4][7][1]*lvlMax),int(procurData[4][8][0]*procurData[4][8][1]*lvlMax),int(procurData[4][9][0]*procurData[4][9][1]*lvlMax),emoji=procurData[1][2]),
                                stuff(procurData[2][0],procurData[2][1],1,0,int(procurData[4][0][0]*procurData[4][0][1]*lvlMax),int(procurData[4][1][0]*procurData[4][1][1]*lvlMax),int(procurData[4][2][0]*procurData[4][2][1]*lvlMax),int(procurData[4][3][0]*procurData[4][3][1]*lvlMax),int(procurData[4][4][0]*procurData[4][4][1]*lvlMax),int(procurData[4][5][0]*procurData[4][5][1]*lvlMax),int(procurData[4][6][0]*procurData[4][6][1]*lvlMax),int(procurData[4][7][0]*procurData[4][7][1]*lvlMax),int(procurData[4][8][0]*procurData[4][8][1]*lvlMax),int(procurData[4][9][0]*procurData[4][9][1]*lvlMax),emoji=procurData[2][2]),
                                stuff(procurData[3][0],procurData[3][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*lvlMax),int(procurData[4][1][0]*procurData[4][1][1]*lvlMax),int(procurData[4][2][0]*procurData[4][2][1]*lvlMax),int(procurData[4][3][0]*procurData[4][3][1]*lvlMax),int(procurData[4][4][0]*procurData[4][4][1]*lvlMax),int(procurData[4][5][0]*procurData[4][5][1]*lvlMax),int(procurData[4][6][0]*procurData[4][6][1]*lvlMax),int(procurData[4][7][0]*procurData[4][7][1]*lvlMax),int(procurData[4][8][0]*procurData[4][8][1]*lvlMax),int(procurData[4][9][0]*procurData[4][9][1]*lvlMax),emoji=procurData[2][2])
                            ]

                            team1.append(alea)
                            logs += "{0} have been added into team1\n".format(alea.name)

                            alea = copy.deepcopy(findAllie("Iliana"))
                            alea.changeLevel(lvlMax)
                            alea.stuff = [getAutoStuff(alea.stuff[0],alea),getAutoStuff(alea.stuff[1],alea),getAutoStuff(alea.stuff[2],alea)]
                            alea.says = ilianaSaysVsLuna

                            team1.append(alea)
                            logs += "{0} have been added into team1\n".format(alea.name)

                        elif alea.isNpc("Clémence pos."):
                            alea = copy.deepcopy(findAllie("Alice Exaltée"))
                            procurData = procurTempStuff["Alice Exaltée"]
                            alea.changeLevel(lvlMax)

                            alea.stuff = [
                                stuff(procurData[1][0],procurData[1][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*lvlMax),int(procurData[4][1][0]*procurData[4][1][1]*lvlMax),int(procurData[4][2][0]*procurData[4][2][1]*lvlMax),int(procurData[4][3][0]*procurData[4][3][1]*lvlMax),int(procurData[4][4][0]*procurData[4][4][1]*lvlMax),int(procurData[4][5][0]*procurData[4][5][1]*lvlMax),int(procurData[4][6][0]*procurData[4][6][1]*lvlMax),int(procurData[4][7][0]*procurData[4][7][1]*lvlMax),int(procurData[4][8][0]*procurData[4][8][1]*lvlMax),int(procurData[4][9][0]*procurData[4][9][1]*lvlMax),emoji=procurData[1][2]),
                                stuff(procurData[2][0],procurData[2][1],1,0,int(procurData[4][0][0]*procurData[4][0][1]*lvlMax),int(procurData[4][1][0]*procurData[4][1][1]*lvlMax),int(procurData[4][2][0]*procurData[4][2][1]*lvlMax),int(procurData[4][3][0]*procurData[4][3][1]*lvlMax),int(procurData[4][4][0]*procurData[4][4][1]*lvlMax),int(procurData[4][5][0]*procurData[4][5][1]*lvlMax),int(procurData[4][6][0]*procurData[4][6][1]*lvlMax),int(procurData[4][7][0]*procurData[4][7][1]*lvlMax),int(procurData[4][8][0]*procurData[4][8][1]*lvlMax),int(procurData[4][9][0]*procurData[4][9][1]*lvlMax),emoji=procurData[2][2]),
                                stuff(procurData[3][0],procurData[3][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*lvlMax),int(procurData[4][1][0]*procurData[4][1][1]*lvlMax),int(procurData[4][2][0]*procurData[4][2][1]*lvlMax),int(procurData[4][3][0]*procurData[4][3][1]*lvlMax),int(procurData[4][4][0]*procurData[4][4][1]*lvlMax),int(procurData[4][5][0]*procurData[4][5][1]*lvlMax),int(procurData[4][6][0]*procurData[4][6][1]*lvlMax),int(procurData[4][7][0]*procurData[4][7][1]*lvlMax),int(procurData[4][8][0]*procurData[4][8][1]*lvlMax),int(procurData[4][9][0]*procurData[4][9][1]*lvlMax),emoji=procurData[2][2])
                            ]

                            team1.append(alea)
                            logs += "{0} have been added into team1\n".format(alea.name)

                for octa in tablOctaTemp[:]:
                    if octa.baseLvl > lvlMax:
                        tablOctaTemp.remove(octa)

                octoRolesNPos = [[[],[],[]],[[],[],[]],[[],[],[]]] # 0 : Dmg; 1 : Heal/Armor; 2 : Buff/Debuff

                for octa in tablOctaTemp:
                    if octa.aspiration in [BERSERK, POIDS_PLUME, MAGE, ENCHANTEUR, OBSERVATEUR, TETE_BRULE,SORCELER,ATTENTIF]:
                        roleId = 0
                    elif octa.aspiration in [ALTRUISTE, PREVOYANT]:
                        roleId = 1
                    elif octa.aspiration in [IDOLE,INOVATEUR, PROTECTEUR, VIGILANT,MASCOTTE]:
                        roleId = 2
                    else:
                        roleId = random.randint(0,2)

                    octoRolesNPos[roleId][octa.weapon.range].append(octa)

                for octa in team2:
                    if octa.aspiration in [BERSERK, POIDS_PLUME, MAGE, ENCHANTEUR, OBSERVATEUR, TETE_BRULE]:
                        roleId = 0
                    elif octa.aspiration in [ALTRUISTE, PREVOYANT]:
                        roleId = 1
                    elif octa.aspiration in [IDOLE,INOVATEUR, PROTECTEUR, VIGILANT,MASCOTTE]:
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
                    while len(team2) < [8,12][team1[0].isNpc("Clémence Exaltée")] and not(oneVAll) and len(tablOctaTemp)>0:
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
                lvlMax, temp =  0, team1
                temp.sort(key=lambda funnyTempVarName: funnyTempVarName.level,reverse=True)

                leniAllie, danger, lvlMax =  len(team1), altDanger[winStreak], min(temp[0].level,55)
                
                tablTeamAlliePos = [0,0,1,1,2,2]+[random.randint(0,2),random.randint(0,2)]
                tablTeamAllieComp = [4,2,2]

                random.shuffle(tablTeamAlliePos)
                allieRolesNPos = [[[],[],[]],[[],[],[]],[[],[],[]]] # 0 : Dmg; 1 : Heal/Armor; 2 : Buff/Debuff

                for allie in tablAllieTemp:
                    if allie.aspiration in [BERSERK, POIDS_PLUME, MAGE, ENCHANTEUR, OBSERVATEUR, TETE_BRULE, SORCELER, ATTENTIF]:
                        roleId = 0
                    elif allie.aspiration in [ALTRUISTE, PREVOYANT, PROTECTEUR, VIGILANT]:
                        roleId = 1
                    elif allie.aspiration in [IDOLE, INOVATEUR,MASCOTTE]:
                        roleId = 2
                    else:
                        roleId = random.randint(0,2)

                    allieRolesNPos[roleId][allie.weapon.range].append(allie)

                while len(team2) < 8:
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
                        if len(tablAllieTemp) > 1:
                            alea=tablAllieTemp[random.randint(0,len(tablAllieTemp)-1)]
                        else:
                            alea=tablAllieTemp[0]
                    try:
                        tablAllieTemp.remove(alea)
                    except:
                        rdmAspi = random.randint(0,ASPI_NEUTRAL-1)
                        tablTempAspi = []
                        for ally in tablAllAllies:
                            if ally.aspiration == rdmAspi:
                                tablTempAspi.append(ally)
                        
                        skillTabl = []
                        if len(tablTempAspi) == 1:
                            skillTabl = tablTempAspi[0].skills
                        elif len(tablTempAspi) > 1:
                            skillTabl = tablTempAspi[random.randint(tablTempAspi)-1].skills
                        alea = tmpAllie("Akia",2,white,rdmAspi,akiaPreWeapon[rdmAspi],akiaStuffPreDef[rdmAspi],GENDER_FEMALE,skillTabl,deadIcon="<:empty:866459463568850954>",icon="<a:akia:993550766415564831>",bonusPoints=recommandedStat[rdmAspi],say=says(start="Je suppose que je vais me dévouer, sinon tout va encre cracher\"\n<:lena:909047343876288552> :\"Merci Akia"))

                    if alea.isNpc("Lena") and random.randint(0,99) < 25:
                        alea = copy.deepcopy(findAllie("Luna"))
                    elif alea.isNpc("Shushi") and random.randint(0,99) < 25:
                        alea = copy.deepcopy(findAllie("Shihu"))
                    elif alea.isNpc("Gwendoline"):
                        alea = copy.deepcopy(findAllie(["Gwendoline","Klironovia","Altikia"][random.randint(0,2)]))
                    elif alea.isNpc("Anna") and random.randint(0,99) < 25 and enableMiror:
                        alea = copy.deepcopy(findAllie("Belle"))
                    alea.changeLevel(lvlMax,stars=starLevel)

                    alea.stuff = [getAutoStuff(alea.stuff[0],alea),getAutoStuff(alea.stuff[1],alea),getAutoStuff(alea.stuff[2],alea)]
                    if alea.name in ["Alice alt","Alice","Clémence","Ruby"]:
                        enableMiror = False
                    elif alea.name == "Belle":
                        for allies in tablAllieTemp[:]:
                            if allies.name in ["Alice","Clémence","Ruby"]:
                                try:
                                    tablAllieTemp.remove(allies)
                                except:
                                    logs += "\nCouldn't remove Alice or Clemence from the list, somehow"

                    team2.append(alea)
                    logs += "{0} have been added into team2\n".format(alea.name)

            for enemy in team2:
                for cmpt in tablIsNpcName:
                    if enemy.isNpc(cmpt):
                        dictIsNpcVar[f"{cmpt}"] = True
                        break
        elif bigMap:
            for enemy in team2:
                for cmpt in tablIsNpcName:
                    if enemy.isNpc(cmpt):
                        dictIsNpcVar[f"{cmpt}"] = True
                        break
            danger = 100 + round(5*starLevel/2,2)
        elif not octogone:
            winStreak = teamWinDB.getVictoryStreak(team1[0])
            danger = dangerLevel[winStreak] + (starLevel * DANGERUPPERSTAR)

        # Temp Anniversary Add
        if not(octogone) and not(procurFight):
            today = (now.day,now.month)
            for tmp in tablAllAllies:
                if today == tmp.birthday:
                    ent = copy.deepcopy(tmp)
                    ent.changeLevel(55+random.randint(0,14))
                    team1.append(ent)

        # Updating the Danger and Team Fighting status
        if octogone:
            danger=100
        else:
            winStreak = teamWinDB.getVictoryStreak(team1[0])

        tablTeam,tablEntTeam,cmpt = [team1,team2],[[],[]],0
        readyMsg, cmpt, nbHealer, nbShielder = None, 0, [0,0], [0,0]

        for teamNum in [0,1]:                 # Entities generations and stats calculations
            for initChar in tablTeam[teamNum]:
                ent = entity(cmpt,initChar,teamNum,auto=not(type(initChar) == char and not(auto)) ,dictInteraction=dictIsNpcVar,danger=danger)

                tablEntTeam[teamNum].append(ent)
                ent.recalculate()
                await ent.getIcon(bot=bot)

                nbHealer[teamNum] = nbHealer[teamNum]+ int(ent.char.aspiration in [VIGILANT,ALTRUISTE])
                nbShielder[teamNum] = nbShielder[teamNum]+ int(ent.char.aspiration in [PROTECTEUR,PREVOYANT])

                cmpt += 1

            if nbHealer[teamNum] > (1+int(bigMap)):
                teamHealReistMul[teamNum] = teamHealReistMul[teamNum] + ((nbHealer[teamNum]-1) * HEALRESISTCROIS / (1+int(bigMap)))
            if nbShielder[teamNum] > (1+int(bigMap)):
                teamArmorReducer[teamNum] = teamArmorReducer[teamNum] - ((nbShielder[teamNum]-1) * SHIELDREDUC / (1+int(bigMap)))

        if not(auto):
            emby = await getRandomStatsEmbed(bot,team1,text="Chargement...")
            if type(msg) != interactions.Message:
                print(type(msg))
                try:
                    msg = await ctx.send(embeds = await getRandomStatsEmbed(bot,team1,text="Chargement..."))
                except:
                    timeWHoraire = now + horaire
                    footerText = "/fight de {0}#{1} ({2}:{3})".format(ctx.author.name,ctx.author.discriminator,["0{0}".format(timeWHoraire.hour),timeWHoraire.hour][timeWHoraire.hour>9],["0{0}".format(timeWHoraire.minute),timeWHoraire.minute][timeWHoraire.minute>9])
                    msg = await ctx.channel.send(embeds = emby.set_footer(text=footerText,icon_url=ctx.author.avatar_url))

        else:
            if not(ctx.responded):
                msg = await ctx.send(embeds = emby)
            else:
                msg = await ctx.channel.send(embeds = await getRandomStatsEmbed(bot,team1,text=["Chargement...","Combat rapide en cours de génération..."][int(auto)]))

        if not(auto):                   # Send the first embed for the inital "Vs" message and start generating the message
            if not(octogone):
                for team in listImplicadTeams:
                    teamWinDB.changeFighting(team,msg.id,ctx.channel_id,team2)

            logs += "\n"
            versus = ""
            for a in [0,1]:
                logs += "\nTeam {0} composition :\n".format(a+1)
                versus+=f"\n__Equipe {a+1} :__\n"
                for b in tablEntTeam[a]:
                    versus+=f"{b.icon} {b.char.name}\n"
                    logs += "{0}\n".format(b.char.name)

        for ent in tablEntTeam[0]:
            if type(ent.char) == tmpAllie:
                for tmpName, tmpStats in procurTempStuff.items():
                    if ent.char.name == tmpName:
                        tempMsg, allStats = "\n{0} (lvl {1})\n".format(ent.char.name,ent.char.level), ent.allStats()+[ent.resistance,ent.percing,ent.critical]
                        for cmpt in range(len(allStats)):
                            tempMsg += "{0} : {1}".format(allStatsNames[cmpt][:3],allStats[cmpt])
                            if cmpt != len(allStats) - 1:
                                tempMsg += ", "
                        logs += tempMsg

        # Placement phase -----------------------------------------------------
        logs += "\n=========\nInitial placements phase\n=========\n\n"
        tablLineTeamGround, placementlines, allAuto, maxPerLine = [[0,1,2],[3,4,5]], [[[],[],[]],[[],[],[]]], True, [5,7][bigMap]

        for actTeam in [0,1]:               # Sort the entities and place them
            logs += "len(team1) : {0}; len(team2) : {1}".format(len(team1),len(team2))
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
                    tablEntOnLine[b+[-1,1][actTeam]] += tablEntOnLine[b][maxPerLine-1:]
                    tablEntOnLine[b] = tablEntOnLine[b][0:maxPerLine]

            if tablNbEntOnLine[[0,2][actTeam]] > maxPerLine:
                tablEntOnLine[1] += tablEntOnLine[[0,2][actTeam]][maxPerLine-1:]
                tablEntOnLine[[0,2][actTeam]] = tablEntOnLine[[0,2][actTeam]][:maxPerLine]

                if len(tablEntOnLine[1]) > maxPerLine:
                    random.shuffle(tablEntOnLine[1])
                    tablEntOnLine[[2,0][actTeam]] += tablEntOnLine[1][maxPerLine-1:]
                    tablEntOnLine[1] = tablEntOnLine[1][:maxPerLine]
            
            if actTeam == 0:
                placementlines[actTeam]=[snipe,dist,melee]
            else:
                placementlines[actTeam]=[melee,dist,snipe]

            tablNbEntOnLine[0],tablNbEntOnLine[1],tablNbEntOnLine[2],lineVal, unplaced = len(tablEntOnLine[0]),len(tablEntOnLine[1]),len(tablEntOnLine[2]),0, []

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
                            first = "\nlineVal = {0}\nlen(tablEntOnLine[lineVal]) = ".format(lineVal)
                            if lineVal < len(tablEntOnLine):
                                first += str(len(tablEntOnLine[lineVal]))
                            else:
                                first += "__OoR__"
                            second = "\nlen(tablSetPos[len(tablEntOnLine[lineVal])]) = "


                            if lineVal < len(tablEntOnLine) and len(tablEntOnLine[lineVal]) < len(tablSetPos):
                                second += str(len(tablSetPos[len(tablEntOnLine[lineVal])]))
                            
                            else:
                                second += "__OoR__"
                            
                            tablLine =[[],[],[]]
                            for ent in tablEntTeam[actTeam]:
                                tablLine[ent.weapon.range].append(ent)

                            for cmpt in range(3):
                                tempText = "\n"
                                for ent in tablLine[cmpt]:
                                    tempText += "{0} {1}".format(ent.icon,ent.name)
                                    if ent != tablLine[cmpt][-1]:
                                        tempText += ", "
                                second += tempText + "\n"

                            await msg.edit(embeds=interactions.Embed(title="__Error during placement phase__",description=format_exc()+"\ncmpt = {0}\nlen(tablEntOnLine) = {1}\nlen(tablSetPos) = {2}{3}{4}\n\nFinghting status reset".format(lineVal,len(tablEntOnLine),len(tablSetPos),first,second)))
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
                                if len(tabl) <= 0:
                                    unplaced.append(tablEntOnLine[lineVal][cmpt2])
                                else:
                                    ruby = tabl[rand]
                                    tabl.remove(ruby)
                                    tablEntOnLine[lineVal][cmpt2].move(y=ruby,x=xLinePos)
                                    logs += "{0} has been place at {1}:{2}\n".format(tablEntOnLine[lineVal][0].char.name,xLinePos,ruby)

                    if len(unplaced) > 0:
                        emptyCells = [[],[]]
                        for celly in tablAllCells:
                            if celly.on == None:
                                emptyCells[celly.x > 2].append(celly)

                        for ent in unplaced:
                            if len(emptyCells[ent.team]) > 1:
                                rdmCell = emptyCells[ent.team][random.randint(0,len(emptyCells[ent.team])-1)]
                            else:
                                rdmCell = emptyCells[ent.team][0]
                            
                            ent.move(cellToMove=rdmCell)
                            emptyCells[ent.team].remove(rdmCell)
                            logs += "{0} has been randomly placed at {1}:{2}\n".format(ent.char.name,rdmCell.x,rdmCell.y)
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
            initTeamEmbed = interactions.Embed(title = "__Ce combat oppose :__",color = light_blue, description=reducedEmojiNames("{0}\n\n__Carte__ :\n{1}".format(versus,map(tablAllCells,bigMap))))
            initTeamEmbed.add_field(name = "__Taux de danger :__",value=str(danger),inline=False)
            if footerText != "":
                initTeamEmbed.set_footer(text=footerText,icon_url=ctx.author.avatar_url)

        choiceEmbed = []
        if not(auto):                       # User there ?
            allReady = False
            already, awaited,awaitedChar = [],[],[]

            for teamNum in tablEntTeam: # Génération du tableau des utilisateurs devant confirmer leur présence
                for ent in teamNum:
                    if ent.auto == False and ent.char.owner > 100:
                        owner = None
                        try:
                            owner = await get(bot, interactions.Member, parent_id=ctx.guild_id, object_id=ent.char.owner)
                        except Exception as e:
                            ent.auto = True

                        if owner != None:
                            awaitedChar += [ent]
                            awaited += [owner]
                    else:
                        ent.auto = True

            dateLimite = datetime.now() + timedelta(seconds=15)
            while not(allReady): # Demande aux utilisateurs de confirmer leur présence
                readyEm = interactions.Embed(title = "Combat manuel",color=light_blue)
                readyEm.set_footer(text="Les utilisateurs n'ayant pas réagis dans les 15 prochaines secondes seront considérés comme combattant automatiques")
                temp,temp2 = "",""
                for a in already:
                    temp2+= a.mention + ", "
                if temp2 == "":
                    temp2 = "-"

                for a in awaited:
                    temp += a.mention + ", "
                if temp == "":
                    temp = "-"

                readyEm.add_field(name = "Prêts :",value = temp2)
                readyEm.add_field(name = "En attente de :",value = temp)
                await msg.edit(embeds = [initTeamEmbed,readyEm])

                def checkIsIntendedUser(reaction,user):
                    mes = reaction.message == readyMsg and str(reaction) == "✅"

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

                if choiceEmbed == 0:
                    choiceEmbed = [await getRandomStatsEmbed(bot,team1,"Fenêtre de sélection de l'action")]

                if awaited == []:
                    allReady = True

            await msg.remove_all_reactions()
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
            statingEmb = interactions.Embed(title = "Initialisation",color = light_blue,description = f"Le combat va commencer {emLoading}{temp2}")

            await msg.edit(embeds = [initTeamEmbed,statingEmb])

            for z in awaitedChar:
                for b in awaited:
                    if b.id == int(z.char.owner):
                        z.auto = True
                        break

        # Timeline's initialisation -----------------------------------------
        tempTurnMsg = "__Début du combat :__"
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
                        if dictIsNpcVar["Hélène"]:                                    # Helene in the fight
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"__Arf, pourquoi je dois faire équipe avec elle déjà (＃￣0￣) ?__")
                            if dictIsNpcVar["Clémence"]:
                                if random.randint(0,99) < 50:
                                    tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:clemence:908902579554111549>',"__S'il te plait Alice, commence pas... Elle fait même pas le même taff que toi.__")
                                    if dictIsNpcVar["Lena"]:
                                        tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:lena:909047343876288552>',"Je sais que c'est tentant de se parler avec des ultra-sons quand on a votre ouïe, mais si vous pôuviez plutôt vous concentrer sur le combat ce sera cool")
                                else:
                                    tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:clemence:908902579554111549>',"Je l'ai entendue celle là !")
                    
                        elif dictIsNpcVar["Félicité"] and dictIsNpcVar["Sixtine"] and dictIsNpcVar["Clémence"]:         # All sisters in the fight
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"Allez ! Un p'tit combat en famille !")

                        elif dictIsNpcVar["Félicité"] or dictIsNpcVar["Sixtine"]:                         # A sister in the fight (except Clémence)
                            tempMsg = "Allez Féli ! On fonce !"
                            if dictIsNpcVar["Sixtine"]:
                                tempMsg = "Courrage Sixtine ! Ça va aller !"

                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,tempMsg)
                        elif dictIsNpcVar["Stella"]:
                            tempTurnMsg += "\n{0} : *\"Il est hors de question que je la laise gagner.\"*".format(ent.icon)
                        elif dictIsNpcVar["Anna"]:
                            tempTurnMsg += "\n{0} : *\"Tiens coucou Anna. Tu passeras le bonjour de ma part à ta soeur !\"*".format(ent.icon)
                            if random.randint(0,99) < 50:
                                tempTurnMsg += "\n<:anna:943444730430246933> : *\"Elle sera contente\"*"
                            else:
                                tempTurnMsg += "\n<:anna:943444730430246933> : *\"Elle aura préféré que ton reflet le fasse directement, mais je lui passerais le message, t'en fais pas\"*"
                        else:
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,ent.char.says.start)

                    elif ent.isNpc("Clémence"):                     # Clémence specials interractions
                        if dictIsNpcVar["Alice"] or dictIsNpcVar["Félicité"] or dictIsNpcVar["Sixtine"]:          # With her sisters
                            tempTabl = []
                            if dictIsNpcVar["Alice"]:
                                tempTabl.append("Hé Alice, ça va être le moment de tester tes compétences non ?")
                            if dictIsNpcVar["Félicité"]:
                                tempTabl.append("Surtout, oublie pas de *pas* en faire trop Féli")
                            if dictIsNpcVar["Sixtine"]:
                                tempTabl.append("Sixtine, je devrais avoir ramenné des vielles peintures, ça t'interresse de regarder ça après le combat ?")

                            rand = tempTabl[random.randint(0,len(tempTabl)-1)]
                            tempTurnMsg += "\n{0} : *\"{1}\"*\n".format(ent.icon,rand)

                            if rand == "Sixtine, je devrais avoir ramenné des vielles peintures, ça t'interresse de regarder ça après le combat ?":
                                if random.randint(0,99) < 50:
                                    tempTurnMsg += "{0} : *\"{1}\"*\n".format('<:sixtine:908819887059763261>',"Oh heu... Je comptais plutôt faire une sieste après moi...")
                                    tempTurnMsg += "{0} : *\"{1}\"*\n".format(ent.icon,"Pas de soucis")
                                else:
                                    tempTurnMsg += "{0} : *\"{1}\"*\n".format('<:sixtine:908819887059763261>',"Oh heu... Pourquoi pas...")

                        elif dictIsNpcVar["Ruby"]:
                            tempTurnMsg += "\n{0} : *\"Oh Madame Ruby, j'espère que vous comptez pas juger mes compétences durant ce combat\"*".format(ent.icon)
                            randy = random.randint(0,99)
                            if randy < 33:
                                tempTurnMsg += "\n<:ruby:958786374759251988> : *\"`Ricane` Tu as peur que je pense que tu as régréssé ?\"*"
                            elif randy < 66:
                                tempTurnMsg += "\n<:ruby:958786374759251988> : *\"Tu sais bien que je suis toujours interresée par tes progrès\"*"
                            elif dictIsNpcVar["John"]:
                                tempTurnMsg += "\n<:ruby:958786374759251988> : *\"Je suis plutôt là pour surveiller un certain loup garou aujourd'hui\"*"
                                if random.randint(0,99) < 60:
                                    tempTurnMsg += "\n<:john:908887592756449311> : *`Ne se sens pas vraiment à l'aise avec les auras des deux puissantes vampires cotes à cotes`*"
                        else:
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,ent.char.says.start)

                    elif ent.isNpc("Shushi"):                       # Shushi specials interractions
                        if dictIsNpcVar["Lena"]:
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"Allez Miman ! Ti va touz les défonzer !")
                            if random.randint(0,99) < 50:
                                if random.randint(0,99) < 50:
                                    tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:lena:909047343876288552>',"Voyons Shushi, c'est quoi ce language ?")
                                else:
                                    tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:lena:909047343876288552>',"`Ricane`")

                        else:
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,ent.char.says.start)

                    elif ent.isNpc("Shihu"):                        # Shihu specials interractions
                        if dictIsNpcVar["Lena"]:
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"Z'est le doit au Boum Boum ?")
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:lena:909047343876288552>',"`Ricane` Allez vas-y")
                        else:
                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,ent.char.says.start)

                    elif ent.isNpc("John") and dictIsNpcVar["Clémence"] and random.randint(0,99) < 50:
                        tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"D-Dit Clémence, ça te dirais une balade sous la pleine lune avec moi après ça ?")
                        tempTurnMsg += "\n<:clemence:908902579554111549> : *\"Hum ? Oh heu... Pourquoi pas écoute\"*"

                    elif ent.isNpc("Stella") and dictIsNpcVar["Alice"]:
                        tempTurnMsg += "\n{0} : *\"Va te faire voir toi, c'est mon terrain de jeu ici !\"*".format(ent.icon)

                    else:
                        tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,ent.char.says.start)

        if tempTurnMsg != "__Début du combat :__":
            tempTurnMsg += "\n"

        nbLB, LBBars = [8,8], [[0,0],[0,0]]

        # Passives skills and stuffs effects ---------------------------------
        for team in [0,1]:
            teamHasLb = False
            for ent in tablEntTeam[team]:
                listEffGiven, listEffGiver = [],[]                
                if not(octogone) and type(ent.char) == tmpAllie and ent.team == 1:
                    for allyTmpName, allyBalancingEff in tmpBalancingDict.items():
                        if ent.char.name.lower() == allyTmpName.lower():
                            add_effect(ent,ent,allyBalancingEff)
                            listEffGiven.append(allyBalancingEff.emoji[ent.char.species][ent.team])
                            listEffGiver.append('<:lenapy:979953598807031918>')

                for skil in ent.char.skills:
                    if type(skil) == skill:
                        if skil.type == TYPE_PASSIVE or skil.jaugeEff != None:               # If the entity have a passive
                            effect=[findEffect(skil.effectOnSelf),findEffect(skil.jaugeEff)][skil.jaugeEff!=None]
                            temp = add_effect(ent,ent,effect," ({0})".format(skil.name),danger=danger)
                            if '🚫' not in temp:
                                listEffGiven.append(effect.emoji[ent.char.species-1][ent.team])
                                listEffGiver.append(skil.emoji)
                                logs += "{0} get the {1} effect from {2}\n".format(ent.char.name,effect.name,skil.name)
                        elif skil.id == divineAbne.id:
                            ent.maxHp = int(ent.maxHp * (1-skil.power/100))
                            ent.hp = copy.deepcopy(ent.maxHp)
                        elif skil.id == plumRem.id:
                            ent.char.weapon = plume2
                for equip in [ent.char.weapon]+ent.char.stuff:       # Look at the entity stuff to see if their is a passive effect
                    if equip.effects != None:
                        if equip.effects == "mk":            # Constitution
                            effect=const
                            for z in tablEntTeam[ent.team]:
                                z.maxHp = int(z.maxHp*(1+const.power/100))
                                z.hp = z.maxHp

                                add_effect(ent,z,effect," ({0} - {1})".format(equip.name,ent.char.name))
                                
                                logs += "{0} gave the {1} effect at {2} for {3} turn(s)\n".format(ent.char.name,effect.name,z.char.name,effect.turnInit)
                                z.refreshEffects()

                            tempTurnMsg += "\n{0} ({1}) a donné l'effet de __{2}__ (<:co:888746214999339068>) à son équipe ({3})".format(ent.char.name,ent.icon,effect.name,equip.name)
                        else:                           # Any other effects
                            effect=findEffect(equip.effects)
                            temp = add_effect(ent,ent,effect," ({0})".format(equip.name),danger=danger)
                            if '🚫' not in temp:
                                listEffGiven.append(effect.emoji[ent.char.species-1][ent.team])
                                listEffGiver.append(equip.emoji)
                                logs += "{0} get the {1} effect from {2}\n".format(ent.char.name,effect.name,equip.name)

                if ent.char.name in upLifeStealNames:
                    for cmpt in range(len(upLifeStealNames)):
                        if ent.char.name == upLifeStealNames[cmpt]:
                            add_effect(ent,ent, upLifeStealEff[cmpt],danger=danger)

                ent.refreshEffects()
                if listEffGiven != []:
                    tempTurnMsg += "\n{0} ".format(ent.icon)
                    for equip in listEffGiver:
                        tempTurnMsg += equip
                    tempTurnMsg += " → "
                    for equip in listEffGiven:
                        tempTurnMsg += equip

                for bosses in tablBoss+tablRaidBoss:
                    if bosses.name == ent.name:
                        LBBars[0][0] += 1
                        if ent.char.oneVAll:
                            LBBars[0][0] += 1
            if type(tablEntTeam[team][0].char) in [tmpAllie,char]:
                LBBars[team][0] = int(len(tablEntTeam[team])>=8)+int(len(tablEntTeam[team])>=16)+int(type(tablEntTeam[not(team)][0].char) in [tmpAllie,char])
            elif teamHasLb:
                LBBars[team][0] = 1

        if tablEntTeam[0][0].isNpc("Luna prê.") and len(tablEntTeam[0]) <= 1:
            lunaDmgRes = copy.deepcopy(defenseUp)
            lunaDmgRes.power, lunaDmgRes.turnInit, lunaDmgRes.unclearable = 50, -1, True
            groupAddEffect(tablEntTeam[0][0], tablEntTeam[0][0], AREA_MONO, lunaDmgRes)
            lunaLifeSteal = copy.deepcopy(vampirismeEff)
            lunaLifeSteal.power, lunaLifeSteal.turnInit, lunaLifeSteal.unclearable = 30, -1, True
            groupAddEffect(tablEntTeam[0][0], tablEntTeam[0][0], AREA_MONO, lunaLifeSteal)

        if tablEntTeam[1][0].isNpc("The Giant Enemy Spider"):           # Giant Enemy Spider's legs summoning
            surrondingsCells = [findCell(tablEntTeam[1][0].cell.x-1,tablEntTeam[1][0].cell.y-1,tablAllCells),findCell(tablEntTeam[1][0].cell.x-1,tablEntTeam[1][0].cell.y,tablAllCells),findCell(tablEntTeam[1][0].cell.x-1,tablEntTeam[1][0].cell.y+1,tablAllCells),findCell(tablEntTeam[1][0].cell.x,tablEntTeam[1][0].cell.y-1,tablAllCells),findCell(tablEntTeam[1][0].cell.x,tablEntTeam[1][0].cell.y+1,tablAllCells),findCell(tablEntTeam[1][0].cell.x+1,tablEntTeam[1][0].cell.y-1,tablAllCells),findCell(tablEntTeam[1][0].cell.x+1,tablEntTeam[1][0].cell.y,tablAllCells),findCell(tablEntTeam[1][0].cell.x+1,tablEntTeam[1][0].cell.y+1,tablAllCells)]
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

        elif dictIsNpcVar["Kiku"]:
            kikuEnt = None
            for ent in tablEntTeam[1]:
                if ent.isNpc("Kiku"):
                    kikuEnt=ent
                    break
            for teamCmpt in [0,1]:
                for ent in tablEntTeam[teamCmpt]:
                    add_effect(kikuEnt,ent,kikuRaiseEff)
                    ent.refreshEffects()

        elif dictIsNpcVar["OctoTour"]:
            octoTour = None
            for ent in tablEntTeam[1]:
                if ent.isNpc("OctoTour"):
                    octoTour = ent
                    break

            for ent in tablEntTeam[1]:
                if ent != octoTour:
                    add_effect(octoTour,ent,octoTourEff2)                                        
                    logs += "{0} gave the {1} effect at {2} for {3} turn(s)\n".format(octoTour.char.name,effect.name,ent.char.name,effect.turnInit)
                    ent.refreshEffects()
    
        if dictIsNpcVar["Lena"] and (dictIsNpcVar["Shushi"] or dictIsNpcVar["Shihu"]):
            lenaEnt = None
            targetEnt = None
            for team in [0,1]:
                for ent in tablEntTeam[team]:
                    if ent.isNpc("Lena"):
                        lenaEnt = ent
                    elif ent.isNpc(['Shushi',"Shihu"]):
                        targetEnt = ent
                    if lenaEnt != None and targetEnt != None:
                        break
                if lenaEnt != None and targetEnt != None:
                    break
        
            if lenaEnt != None and targetEnt != None and lenaEnt.team == targetEnt.team:
                add_effect(lenaEnt,targetEnt,lenaShuRedirect)

        if len(contexte.giveEffToTeam1) > 0:
            lenPy1 = entity(0,copy.deepcopy(findAllie("Lena")),0,False,True)
            groupAddEffect(lenPy1, tablEntTeam[0][0], tablEntTeam[0], contexte.giveEffToTeam1)
        if len(contexte.giveEffToTeam2) > 0:
            lenPy2 = entity(0,copy.deepcopy(findAllie("Lena")),1,False,True)
            groupAddEffect(lenPy2, tablEntTeam[1][0], tablEntTeam[1], contexte.giveEffToTeam2)

        for team in [0,1]:                                                 # Raise skills verifications
            for ent in tablEntTeam[team]:
                for skilly in ent.char.skills + ent.effects:
                    if type(skilly)==skill:
                        if skilly.type in [TYPE_INDIRECT_REZ,TYPE_RESURECTION] or (skilly.effectAroundCaster != None and skilly.effectAroundCaster[0] == TYPE_RESURECTION):
                            for ent2 in tablEntTeam[team]:
                                ent2.ressurectable = True
                            break

                for eff in ent.effects:
                    if eff.effects.jaugeValue != None :
                        teamJaugeDict[team][ent] = eff
                        break

        if not(auto):                               # Send the turn 0 msg
            if tempTurnMsg == "__Début du combat :__":
                tempTurnMsg += "\n -"
            emby = interactions.Embed(title=f"__Tour {tour}__",description= reducedEmojiNames(tempTurnMsg),color = light_blue)
            if footerText != "":
                emby.set_footer(text=footerText,icon_url=ctx.author.avatar_url)
            embInfo = interactions.Embed(title = "__Combat (D.{0})__".format(danger), color = mainUser.color, description=reducedEmojiNames("__Carte__ :\n{0}\n__Timeline__ :\n{1}".format(map(tablAllCells,bigMap,deplTabl=deplTabl),time.icons())))
            await msg.edit(embeds = [embInfo,emby])
            await asyncio.sleep(2+(min(len(tempTurnMsg),2000)/2000*5))

        fight, ennemi, counterTracker = True, tablEntTeam[1][0], {}
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
                        choiceEmbDesc = nextNotAuto.quickEffectIcons()
                        choiceEmbed = [interactions.Embed(title = "Fenêtre de selection de l'action", color=nextNotAuto.char.color,description = f"En attente du tour de {nextNotAuto.char.name} {emLoading}\n{choiceEmbDesc}")]
                        lastNotAuto = nextNotAuto
                    elif nextNotAuto == 0:
                        choiceEmbed = [interactions.Embed(title = "Fenêtre de selection de l'action", color=light_blue,description = f"Il n'y a plus de combattants manuels en vie")]
                        lastNotAuto = nextNotAuto

                if allAuto and choiceEmbed != []:
                    choiceEmbed = []

                if actTurn.hp > 0:
                    tempTurnMsg = f"__Début du tour de {actTurn.char.name} :__\n"

                # Sudden death verifications and damages ----------------------------
                if actTurn == time.begin:
                    funnyTempVarName, counterTracker = "", {}
                    tour += 1
                    logs += "\n\n=========\nTurn {0}\n=========".format(tour)

                    for team in [0,1]:
                        for ent in tablEntTeam[team]:
                            if ent.hp > 0:
                                ent.stats.survival += 1

                                if ent.cell != None:
                                    if ent.cell.on != ent and ent.cell.on == None:
                                        ent.cell.on = ent
                                        print("{0} n'était pas sur sa cellule, apparament".format(ent.char.name))
                                else:
                                    raise Exception("{0} n'est pas sur une cellule !!".format(ent.char.name))
                            if dictIsNpcVar["Kiku"] and tour > 1:
                                for eff in ent.effects:
                                    if eff.effects.id == kikuRaiseEff.id:
                                        eff.effects.power = min(round(eff.effects.power*1.2,2),200)

                        if LBBars[team][0] > 0:
                            LBBars[team][1] = min(LBBars[team][1]+1,LBBars[team][0]*3)
                    if dictIsNpcVar["Kiku"] and tour >= 16 and not(kikuExect):
                        kikuEnt, isEligible = None, True
                        for b in tablEntTeam[1]:
                            if b.isNpc("Kiku"):
                                kikuEnt = b
                                if b.hp <= 0:
                                    isEligible = False
                                    break
                                for eff in b.effects:
                                    if eff.effects.id == undeadEff2.id:
                                        isEligible = False
                                        break
                                break
                        if isEligible:
                            kikuExect = True
                            for a in [0,1]:
                                for b in tablEntTeam[a]:
                                    if b.hp > 0:
                                        for eff in b.effects:
                                            if eff.effects.id == kikuRaiseEff.id:
                                                ballerine, chocolatine = kikuEnt.attack(target=b,value = 999,icon = eff.icon,area=AREA_MONO,sussess=666,use=MAGIE,onArmor = 100, execution = True)
                                                funnyTempVarName += ballerine

                            if not(auto):
                                funnyTempVarName = reducedEmojiNames(funnyTempVarName)
                                if len(funnyTempVarName) > 4096:
                                    funnyTempVarName = unemoji(funnyTempVarName)
                                    if len(funnyTempVarName) > 4096:
                                        funnyTempVarName = "OVERLOAD"
                                await msg.edit(embeds = [embInfo,interactions.Embed(title=f"__Tour {tour}__",description=funnyTempVarName)]+choiceEmbed,componenets=[infoSelect])
                                await asyncio.sleep(2+(min(len(funnyTempVarName),2000)/2000*5))

                    if tour >= 21:
                        funnyTempVarName += f"\n__Mort subite !__\nTous les combattants perdent **{SUDDENDEATHDMG*(tour-20)}%** de leurs PV maximums\n"
                        for a in [0,1]:
                            for b in tablEntTeam[a]:
                                if b.hp > 0:
                                    if type(b.char) == octarien and b.char.oneVAll:
                                        lose = int(b.maxHp*((SUDDENDEATHDMG/1000)*(tour-20)))
                                    else:
                                        lose = int(b.maxHp*((SUDDENDEATHDMG/100)*(tour-20)))
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
                            await msg.edit(embeds = [embInfo,interactions.Embed(title=f"__Tour {tour}__",description=funnyTempVarName)]+choiceEmbed,componenets=[infoSelect])
                            await asyncio.sleep(2+(min(len(funnyTempVarName),2000)/2000*5))

                        logs += funnyTempVarName

                    for entDepl in deplTabl:
                        tempMsg = "__Tour de {0} {1} ({2}) :__\n".format(entDepl[0].icon,entDepl[0].name,entDepl[0].summoner.name)+entDepl[0].startOfTurn(tablEntTeam)
                        if entDepl[0].leftTurnAlive > 0:
                            if entDepl[0].char.skills.type in [TYPE_BOOST,TYPE_ARMOR,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ,TYPE_INDIRECT_DAMAGE,TYPE_MALUS] and entDepl[0].char.skills.effects != [None]:
                                ballerine = groupAddEffect(caster=entDepl[0], target=entDepl[0], area=entDepl[0].char.skills.area, effect=entDepl[0].char.skills.effects, skillIcon=entDepl[0].char.skills.emoji, actionStats=entDepl[0].char.skills.useActionStats, effPurcent = entDepl[0].char.skills.effPowerPurcent)
                                tempMsg += ballerine
                                logs += ballerine

                            elif entDepl[0].char.skills.type == TYPE_HEAL:
                                logs += "\n"
                                statUse = entDepl[0].char.skills.use
                                if statUse == None:
                                    statUse = 0
                                elif statUse == HARMONIE:
                                    temp = entDepl[0].allStats()
                                    for a in temp:
                                        statUse = max(a,statUse)
                                else:
                                    statUse = entDepl[0].allStats()[statUse]

                                power = entDepl[0].char.skills.power
                                actionStats = ACT_HEAL

                                if entDepl[0].char.skills.effects != [None] and entDepl[0].char.skills.effBeforePow:
                                    ballerine = groupAddEffect(caster=entDepl[0], target=entDepl[0], area=entDepl[0].char.skills.area, effect=entDepl[0].char.skills.effects, skillIcon=entDepl[0].char.skills.emoji, actionStats=entDepl[0].char.skills.useActionStats, effPurcent = entDepl[0].char.skills.effPowerPurcent)
                                    tempMsg = tempMsg + ballerine
                                    logs += ballerine

                                for ent in entDepl[1].getEntityOnArea(area=entDepl[0].char.skills.area,team=entDepl[0].team,fromCell=entDepl[1],wanted=ALLIES,directTarget=False):
                                    funnyTempVarName, useless = entDepl[0].heal(ent, entDepl[0].char.skills.emoji, entDepl[0].char.skills.use, power,danger=danger, mono = entDepl[0].char.skills.area == AREA_MONO, useActionStats = entDepl[0].char.skills.useActionStats)
                                    tempMsg += funnyTempVarName
                                    logs += funnyTempVarName

                                if entDepl[0].char.skills.effects != [None] and not(entDepl[0].char.skills.effBeforePow):
                                    ballerine = groupAddEffect(caster=entDepl[0], target=entDepl[0], area=entDepl[0].char.skills.area, effect=entDepl[0].char.skills.effects, skillIcon=entDepl[0].char.skills.emoji, actionStats=entDepl[0].char.skills.useActionStats, effPurcent = entDepl[0].char.skills.effPowerPurcent)
                                    tempMsg += ballerine
                                    logs += ballerine

                            else: # Damage
                                power, elemPowBonus, cmpt = entDepl[0].char.skills.power, 0, 0
                                while cmpt < entDepl[0].char.skills.repetition and entDepl[0].char.skills.power > 0:
                                    funnyTempVarName, temp = entDepl[0].attack(target=entDepl[0],value=power,icon=entDepl[0].char.skills.emoji,area=entDepl[0].char.skills.area,sussess=entDepl[0].char.skills.sussess,use=entDepl[0].char.skills.use,onArmor=entDepl[0].char.skills.onArmor,useActionStats=actionStats,setAoEDamage=entDepl[0].char.skills.setAoEDamage,lifeSteal = entDepl[0].char.skills.lifeSteal,erosion = entDepl[0].char.skills.erosion, skillPercing = entDepl[0].char.skills.percing, execution=entDepl[0].char.skills.execution)
                                    tempMsg += funnyTempVarName
                                    logs += "\n"+funnyTempVarName
                                    deathCount += temp
                                    cmpt += 1
                                    if cmpt < entDepl[0].char.skills.repetition:
                                        tempMsg += "\n"

                                if None not in entDepl[0].char.skills.effects and not(entDepl[0].char.skills.effBeforePow):
                                    tempMsg += "\n"
                                    for a in entDepl[0].char.skills.effects:
                                        effect = findEffect(a)
                                        tempMsg += add_effect(entDepl[0],entDepl[0],effect,effPowerPurcent=entDepl[0].char.skills.effPowerPurcent)
                                        logs += "\n{0} gave the {1} effect at {2} for {3} turn(s)".format(entDepl[0].char.name,effect.name,entDepl[0].char.name,effect.turnInit)
 
                            if entDepl[0].char.skills.effectAroundCaster != None:
                                tempMsg += "\n"
                                if entDepl[0].char.skills.effectAroundCaster[0] == TYPE_HEAL:
                                    for a in entDepl[1].getEntityOnArea(area=entDepl[0].char.skills.effectAroundCaster[1],fromCell=entDepl[1],team=entDepl[0].team,wanted=ALLIES,directTarget=False):
                                        funnyTempVarName, useless = entDepl[0].heal(a, entDepl[0].char.skills.emoji, entDepl[0].char.skills.use, entDepl[0].char.skills.effectAroundCaster[2], danger=danger, mono = entDepl[0].char.skills.area == entDepl[0].char.skills.effectAroundCaster[1], useActionStats = entDepl[0].char.skills.useActionStats)
                                        tempMsg += funnyTempVarName
                                        logs += funnyTempVarName
                                elif entDepl[0].char.skills.effectAroundCaster[0] == TYPE_DAMAGE:
                                    funnyTempVarName, temp = entDepl[0].attack(target=entDepl[0],value=entDepl[0].char.skills.effectAroundCaster[2],icon=entDepl[0].char.skills.emoji,area=entDepl[0].char.skills.effectAroundCaster[1],sussess=entDepl[0].char.skills.sussess,use=entDepl[0].char.skills.use,onArmor=entDepl[0].char.skills.onArmor,useActionStats=actionStats,setAoEDamage=entDepl[0].char.skills.setAoEDamage,lifeSteal = entDepl[0].char.skills.lifeSteal)
                                    tempMsg += funnyTempVarName
                                    logs += "\n"+funnyTempVarName
                                elif type(entDepl[0].char.skills.effectAroundCaster[2]) == classes.effect or findEffect(entDepl[0].char.skills.effectAroundCaster[2]) != None :
                                    ballerine = groupAddEffect(entDepl[0], entDepl[0] , entDepl[0].char.skills.effectAroundCaster[1], entDepl[0].char.skills.effectAroundCaster[2], entDepl[0].char.skills.emoji, effPurcent=entDepl[0].char.skills.effPowerPurcent)
                                    tempMsg += ballerine
                                    logs += ballerine

                            entDepl[0].leftTurnAlive = entDepl[0].leftTurnAlive -1
                            if entDepl[0].leftTurnAlive <= 0:
                                entDepl[1].depl = None
                                entDepl[1], entDepl[2] = None, []
                            if not(auto):
                                if len(tempMsg) > 4096:
                                    funnyTempVarName = unemoji(tempMsg)
                                    if len(tempMsg) > 4096:
                                        tempMsg = "OVERLOAD"
                                await msg.edit(embeds = [embInfo,interactions.Embed(title=f"__Tour {tour}__",description=funnyTempVarName)]+choiceEmbed,components=[infoSelect])
                                await asyncio.sleep(2+(min(len(tempMsg),2000)/2000*5))

                    if auto and tour in [1,6,11,16] and not(testFight):
                        temp = tablEntTeam[0][:]+tablEntTeam[1][:]
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
                        suppClass = sorted(temp,key=lambda student: student.stats.damageBoosted + student.stats.damageDodged,reverse=True)
                        for a in suppClass[:]:
                            if a.stats.damageBoosted + a.stats.damageDodged < 1:
                                suppClass.remove(a)

                        listClassement = [dptClass,healClass,shieldClass,suppClass]

                        endResultRep, pvTabls = {}, [[0,0],[0,0]]
                        for team in [0,1]:             # Result msg character showoff
                            for ent in tablEntTeam[team]:
                                if type(ent.char) not in [invoc,depl]:
                                    pvTabls[team] = [pvTabls[team][0]+max(0,ent.hp),pvTabls[team][1]+max(0,ent.maxHp)]
                                    raised = ""
                                    if ent.status == STATUS_RESURECTED and ent.raiser != None:
                                        raised = " ({1}{0})".format(ent.raiser,['<:rezB:907289785620631603>','<:rezR:907289804188819526>'][ent.team])
                                    elif ent.status == STATUS_TRUE_DEATH and ent.raiser != None:
                                        raised = " ({0})".format(['<:diedTwiceB:907289950301601843>','<:diedTwiceR:907289935663485029>'][ent.team])

                                    nbLB, nbSummon = "",""
                                    if ent.stats.nbLB > 1:
                                        nbLB = "(<:lb:886657642553032824>x{0})".format(ent.stats.nbLB)
                                    elif ent.stats.nbLB == 1:
                                        nbLB = "(<:lb:886657642553032824>)"
                                    if ent.stats.nbSummon > 0:
                                        nbSummon = "(<:carbi:884899235332522016>x{0})".format(ent.stats.nbSummon)

                                    addText = ent.getMedals(listClassement)+raised+nbLB+nbSummon
                                    if addText != "":
                                        addText = " "+addText
                                    resultMsg = reducedEmojiNames("{0} {1}{2}\n".format(ent.icon,ent.char.name,addText))
                                    
                                    if type(ent.char) != tmpAllie or ent.team == 1:
                                        try:
                                            endResultRep[ent.char.team] += resultMsg
                                        except KeyError:
                                            endResultRep[ent.char.team] = resultMsg

                                    else:
                                        teamToSee = mainUser.team 
                                        try:
                                            endResultRep[teamToSee] += resultMsg
                                        except KeyError:
                                            endResultRep[teamToSee] = resultMsg

                        resultEmbed = interactions.Embed(title = "__Combat rapide en cours<a:loading:862459118912667678> :__",color = mainUser.color,description="Vous pouvez toujours lancer des combats normaux durant ce chargement\n__Tour {0}__".format(tour))

                        for indexTeam in endResultRep:
                            if len(endResultRep[indexTeam]) > 1024:
                                temp, temp2, haveStarted = "", "", False
                                for letter in endResultRep[indexTeam]:
                                    if letter == "\n":
                                        temp += temp2+letter
                                        temp2, haveStarted = "", False
                                    elif letter in ["(",")"]:
                                        haveStarted = not(haveStarted)
                                    elif not(haveStarted):
                                        temp2+=letter
                                
                                if len(temp2)>0 and temp2[-1] != "\n":
                                    temp += temp2
                                endResultRep[indexTeam] = temp

                        cmpt = 0
                        for indexTeam in endResultRep:
                            try:
                                cmpt += 1
                                txt = "__PVs :__ {0}%\n".format(round((pvTabls[cmpt-1][0]/pvTabls[cmpt-1][1])*100,2))+endResultRep[indexTeam]
                                if len(txt) >= 1024:
                                    txt = unemoji(txt)
                                resultEmbed.add_field(name="\n__Equipe {0} :__".format(cmpt),value=txt,inline=True)
                            except:
                                resultEmbed.add_field(name="\n__Equipe ??? :__",value="???",inline=True)

                        await msg.edit(embeds=resultEmbed)
                        await asyncio.sleep(1)

                # Dead team check --------------------------------
                for c in [0,1]:
                    for d in tablEntTeam[c]:
                        if d.hp > 0 and type(d.char) not in [invoc, depl]:
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
                    embInfo = interactions.Embed(title = "__Combat {0} (D.{1})__".format(rdmEmoji,danger),color = mainUser.color,description="__Carte__ :\n{0}\n__Timeline__ :\n{1}\n<:em:866459463568850954>".format(map(tablAllCells,bigMap,deplTabl=deplTabl),time.icons()))
                    if footerText != "":
                        embInfo.set_footer(text=footerText,icon_url=ctx.author.avatar_url)

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

                funnyTempVarName = actTurn.startOfTurn(tablEntTeam=tablEntTeam)
                tempTurnMsg += reducedEmojiNames(funnyTempVarName)
                logs += "\n"+funnyTempVarName
                deathCount = bigRaiseCount = 0

                # Main messages statistics generation ---------------------------------------------------------------
                if not(auto) and (wasAlive or actTurn.hp > 0):
                    infoOp,cmpt,temp = [],0, ""
                    for a in [0,1]:     # Generating the Hp's select menu
                        for b in tablEntTeam[a]:
                            if type(b.char) not in [invoc, depl]:
                                raised = ""
                                if b.status == STATUS_RESURECTED:
                                    raised = " (Réanimé{0})".format(["","e"][b.char.gender == GENDER_FEMALE])
                                armorValue = 0
                                for eff in b.effects:
                                    if eff.type == TYPE_ARMOR:
                                        armorValue += eff.value
                                
                                armorTxt, armorPurcent = "", ""
                                if armorValue > 0:
                                    armorTxt = " +{0} PAr".format(separeUnit(armorValue))
                                    armorPurcent = " +{0}%".format(int(armorValue/b.maxHp*100))
                                infoOp += [interactions.SelectOption(label=unhyperlink(b.char.name),value=str(cmpt),emoji=getEmojiObject(b.icon),description=f"{separeUnit(max(0,b.hp))} PV{armorTxt} ({max(0,round(b.hp/b.maxHp*100))}%{armorPurcent}), R.S. : {b.healResist}%{raised}")]
                            cmpt+=1
                    infoSelect =  interactions.ActionRow(components=[interactions.SelectMenu(custom_id = "seeFightersPv", options=infoOp, placeholder="Voir les PVs des combattants")])

                    temp2 = actTurn.allStats()+[actTurn.resistance,actTurn.percing]
                    critRate = round(probCritDmg(actTurn),1)
                    temp2 += [critRate]
                    for a in range(CRITICAL+1):               # Generating the stats field of the main message
                        if a == 7:
                            temp += f"\n\n__Réduction de dégâts__ : {temp2[a]}%"
                        elif a == 8:
                            temp += f"\n__Taux pénétration d'armure__ : {temp2[a]}%"
                        elif a == 9:
                            if actTurn.char.aspiration in [POIDS_PLUME,OBSERVATEUR]:
                                temp2[a] += actTurn.specialVars["aspiSlot"]
                            temp += f"\n__Taux de coup critique__ : {min(temp2[a],80)}%"
                        else:
                            temp += f"\n__{allStatsNames[a]}__ : {temp2[a]}"

                    level = str(actTurn.char.level) + ["","<:littleStar:925860806602682369>{0}".format(actTurn.char.stars)][actTurn.char.stars>0]
                    embInfo.add_field(name = f"__{actTurn.icon} {unhyperlink(actTurn.char.name)}__ (Niveau {level})",value=f"PV : {max(0,actTurn.hp)} / {actTurn.maxHp}",inline = False)
                    embInfo.add_field(name = "__Liste des effets :__",value=actTurn.effectIcons(),inline = True)
                    embInfo.add_field(name = "__Statistiques :__",value = temp,inline = True)
                    embInfo.add_field(name = "<:empty:866459463568850954>",value='**__Liste des effets :__**',inline=False)

                    adds, deplMsg = "", ""

                    for team in [0,1]:                                  # Generating the effects fields of the main message
                        teamView, lbCd = "", 0
                        if LBBars[team][0] > 0:
                            teamView = ["","<:lb:886657642553032824>"][LBBars[team][0]>0 and LBBars[team][1]>=3]
                            lbCd, barsLb = LBBars[team][1], 0
                            while barsLb < 4:
                                if barsLb < LBBars[team][0]:
                                    if lbCd>=3:
                                        teamView += "<:l3:983450379205378088>"
                                    elif lbCd > 0:
                                        teamView += ["<:l3:983450379205378088>","<:l1:983450416010371183>","<:l2:983450398645977218>"][lbCd%3]
                                    else:
                                        teamView += "<:l0:983450435404849202>"
                                    lbCd = max(0,lbCd-3)
                                barsLb += 1
                            teamView += "\n"
                        teamView2 = ["","",""]
                        for ent in tablEntTeam[team]:
                            if type(ent.char) not in [invoc, depl]:
                                tempQuickEffects = ent.lightQuickEffectIcons()
                                teamView2[0], teamView2[1], teamView2[2] = teamView2[0]+tempQuickEffects[0], teamView2[1]+tempQuickEffects[1], teamView2[2]+tempQuickEffects[2]

                        if teamView2[0] == "":
                            teamView += "Pas d'effets sur l'équipe"
                        else:
                            teamView = reducedEmojiNames(teamView)
                            if len(teamView2[0]) <= (1024-len(teamView)):
                                teamView += teamView2[0]
                            elif len(teamView2[1]) <= (1024-len(teamView)):
                                teamView += teamView2[1]
                            elif len(teamView2[2]) <= (1024-len(teamView)):
                                teamView += teamView2[2]
                            else:
                                teamView = "Overload"

                        embInfo.add_field(name= "__Équipe {0} :__".format(["Bleue","Rouge"][team]),value=teamView,inline=True)

                    if teamJaugeDict != [{},{}]:
                        jaugeField = ""
                        for team in [0,1]:
                            for jaugeEnt, jaugeEff in teamJaugeDict[team].items():
                                if jaugeEnt.hp > 0:
                                    jaugeField += "{0} : {1} ".format(jaugeEnt.icon,jaugeEff.icon)
                                    nbFieldEm, cmpt = len(jaugeEff.effects.jaugeValue.emoji[0]), 0
                                    nbPointPerField = 100/nbFieldEm
                                    while cmpt * nbPointPerField < jaugeEff.value:
                                        cmpt += 1

                                    if jaugeEff.value - nbPointPerField * (cmpt-1) < (nbPointPerField * cmpt/2) and cmpt > 0:
                                        cmpt -= 1
                                    
                                    jaugeField += jaugeEff.effects.jaugeValue.emoji[jaugeEff.value > 25][0]+jaugeEff.effects.jaugeValue.emoji[jaugeEff.value>=65][1]+jaugeEff.effects.jaugeValue.emoji[jaugeEff.value>=90][2]
                                    
                                    jaugeField += " **{0}**\n".format(jaugeEff.value)
                            
                        if jaugeField:
                            embInfo.add_field(name="__Jauges :__",value=jaugeField,inline=False)
                    
                    for deplEnt in deplTabl:
                        if deplEnt[0].leftTurnAlive > 0:
                            on = ""
                            if deplEnt[1].on != None:
                                on = " ({0})".format(deplEnt[1].on.icon)
                            deplMsg += "{0}{1} {2}:{3}{4}\n".format(deplEnt[0].summoner.icon, deplEnt[0].icon, deplEnt[1].x, deplEnt[1].y, on)
                    
                    if deplMsg != "":
                        embInfo.add_field(name="__Déployables :__",value=deplMsg,inline=False)

                    if nextNotAuto == actTurn:
                        await msg.edit(embeds = [embInfo,interactions.Embed(title=f"__Tour {tour}__",description=reducedEmojiNames(tempTurnMsg),color = actTurn.char.color)]+choiceEmbed,components=[infoSelect])

                # Turn actions --------------------------------------------------------------------------------------
                nowStartOfTurn = datetime.now()
                if wasAlive and actTurn.hp <= 0:        # Died from indirect damages at the startinfoSelect
                    if not(auto):
                        if len(tempTurnMsg) > 4096:
                            tempTurnMsg = unemoji(tempTurnMsg)
                            if len(tempTurnMsg) > 4096:
                                tempTurnMsg = "OVERLOAD"

                        await msg.edit(embeds = [embInfo,interactions.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color)]+choiceEmbed,components=[infoSelect])
                        if type(actTurn.char) not in [invoc, depl]:
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
                        playOfTheGame = [potgValue[1],potgValue[0],interactions.Embed(title=f"__Action du combat\nTour {tour}__",description=tempTurnMsg,color = potgValue[0].char.color)]

                # Still alive ===========================
                elif actTurn.hp > 0:
                    cmpt,iteration,replay,allyRea = 0,actTurn.char.weapon.repetition,False,actTurn.stats.allieResurected
                    unsuccess = True

                    # ========== Playing the turn ==============
                    if not(actTurn.stun):                   # The entity isn't stun, so he can play his turn
                        allReadyMove = False
                        while 1:
                            atRange, nbTargetAtRange = actTurn.atRange(), len(actTurn.atRange())
                            onReplica = False
                            for eff in actTurn.effects:
                                if eff.effects.replica != None:
                                    onReplica = eff
                                    eff.decate(turn=1)
                                    actTurn.refreshEffects()
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
                                    haveOption,unsuccess, waitingSelect, haveIterate, lbSkill = False,False, interactions.ActionRow(components=[interactions.SelectMenu(custom_id = "anotherWaitingSelect", options=[interactions.SelectOption(label="Veillez patienter...",value="PILLON!",emoji=Emoji(name='🕑'),default=True)],disabled=True)]), False, None
                                    def check(m):
                                        return int(m.author.id) == int(actTurn.char.owner) and m.message.id == msg.id

                                    if LBBars[actTurn.team][0]> 0 and LBBars[actTurn.team][1]//3 >= 1:
                                        if LBBars[actTurn.team][1]//3 == 1:
                                            lbSkill = lb1Tabl[actTurn.char.aspiration]
                                        elif LBBars[actTurn.team][1]//3 == 2:
                                            lbSkill = lb2Tabl[actTurn.char.aspiration]
                                        elif LBBars[actTurn.team][1]//3 == 3:
                                            lbSkill = lb3Tabl[actTurn.char.aspiration]
                                        elif LBBars[actTurn.team][1]//3 == 4:
                                            lbSkill = lb4

                                    while not(haveOption) and not(unsuccess):
                                        choiceMsgTemp,tempTabl,tabltabl,canBeUsed = getPrelimManWindow(actTurn, LBBars, tablEntTeam)+"\n\n__Options disponibles :__\n",[actTurn.char.weapon],[0]+actTurn.cooldowns,[]

                                        if not(actTurn.silent):
                                            for a in actTurn.char.skills:
                                                if type(a) == skill:
                                                    tempTabl.append(a)
                                                else:
                                                    tempTabl.append(None)

                                        if len(actTurn.cell.getEntityOnArea(area=AREA_CIRCLE_1,team=actTurn.team,wanted=ALLIES,fromCell=actTurn.cell)) > 1:
                                            friendlyPush.emoji = ["<:movePlz:928756987532029972>","<a:sparta:928795602328903721>","<a:sparta:928796053585678337>","<a:sparta:928796223215902770>"][random.randint(0,3)]
                                            tempTabl.append(friendlyPush)
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
                                                    for eff in actTurn.effects:
                                                        tablEffId.append(eff.effects.id)

                                                    for cmpt in range(len(tempTabl[a].become)):
                                                        jaugeRequierment = False
                                                        if tempTabl[a].become[cmpt].jaugeEff != None:
                                                            try:
                                                                jaugeRequierment = teamJaugeDict[actTurn.team][actTurn].effects.id == tempTabl[a].become[cmpt].jaugeEff.id and teamJaugeDict[actTurn.team][actTurn].value >= tempTabl[a].become[cmpt].minJaugeValue
                                                            except KeyError:
                                                                jaugeRequierment = True
                                                        else:
                                                            jaugeRequierment = True
                                                        if jaugeRequierment:
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
                                                            target = [ALLIES,ENEMIES][line]
                                                            if len(actTurn.cell.getEntityOnArea(area=tempOption.range,team=actTurn.team,wanted=target,lineOfSight=line,dead=tempOption.type == TYPE_RESURECTION,fromCell=actTurn.cell)) > 0:
                                                                choiceMsgTemp += f"\n{tempOption.emoji} __{tempOption.name} :__\n"
                                                                choiceMsgTemp += "> {0}\n".format(tempOption.description.replace("\n","\n> "))
                                                                addDesc = ""
                                                                if tempOption.condition[:2] == [EXCLUSIVE,ELEMENT]:
                                                                    addDesc += "{0}".format(elemEmojis[tempOption.condition[2]])
                                                                if tempOption.type in [TYPE_DAMAGE,TYPE_INDIRECT_HEAL]:
                                                                    addDesc += "{1}Puis. : {0}".format(tempOption.power,["",", "][addDesc != ""])
                                                                    if tempOption.maxPower > 0 and tempOption.maxPower != tempOption.power:
                                                                        addDesc += ", Puis. Max. : {0}".format(tempOption.maxPower)
                                                                if tempOption.jaugeEff != None:
                                                                    addDesc += "{0}{1} -{2}".format(["",", "][addDesc != ""],tempOption.jaugeEff.emoji[0][0],tempOption.minJaugeValue)
                                                                    if tempOption.maxJaugeValue > 0 and tempOption.maxJaugeValue != tempOption.minJaugeValue:
                                                                        addDesc += "/-{0}".format(tempOption.maxJaugeValue)
                                                                if addDesc != "":
                                                                    choiceMsgTemp = choiceMsgTemp[:-1] + ["","\n> "][addDesc != ""] + addDesc + "\n"
                                                                canBeUsed += [tempOption]
                                                        else:
                                                            funnyTempVarNameButTheSecond = [TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE,TYPE_DAMAGE]
                                                            target = ALLIES
                                                            for b in funnyTempVarNameButTheSecond:
                                                                if (tempOption.type == b or tempOption.id == "InfiniteDarkness") and tempOption.id != friendlyPush.id:
                                                                    target = ENEMIES
                                                                    break

                                                            line = tempOption.type in funnyTempVarNameButTheSecond
                                                            if tempOption.range != AREA_MONO:
                                                                if (tempOption.type != TYPE_SUMMON and len(actTurn.cell.getEntityOnArea(area=tempOption.range,team=actTurn.team,wanted=target,lineOfSight=line,dead=tempOption.type == TYPE_RESURECTION,fromCell=actTurn.cell)) > 0) or (tempOption.type == TYPE_SUMMON and tablAliveInvoc[actTurn.team] <3):
                                                                    canBeUsed += [tempOption] 
                                                                    choiceMsgTemp += f"{tempOption.emoji} {tempOption.name}\n"
                                                            else:
                                                                effect = tempOption.effects
                                                                if (tempOption.type != TYPE_SUMMON and len(actTurn.cell.getEntityOnArea(area=tempOption.area,team=actTurn.team,wanted=target,lineOfSight=line,effect=effect,fromCell=actTurn.cell)) > 0) or (tempOption.type == TYPE_SUMMON and tablAliveInvoc[actTurn.team] <3):                                        
                                                                    canBeUsed += [tempOption]
                                                                    choiceMsgTemp += f"{tempOption.emoji} {tempOption.name}\n"

                                        if LBBars[actTurn.team][1]>=3:
                                            line = lbSkill.type in [TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE,TYPE_DAMAGE]
                                            target = [ALLIES,ENEMIES][line]
                                            if len(actTurn.cell.getEntityOnArea(area=lbSkill.range,team=actTurn.team,wanted=target,lineOfSight=line,dead=lbSkill.type == TYPE_RESURECTION,fromCell=actTurn.cell)) > 0:
                                                choiceMsgTemp += f"\n{lbSkill.emoji} __{lbSkill.name} :__\n"
                                                choiceMsgTemp += "> {0}\n".format(lbSkill.description.replace("\n","\n> "))
                                                canBeUsed += [lbSkill]

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
                                                    desc, toRemove = completlyRemoveEmoji(a.description), ["_","*","|","\n"]
                                                    for letter in toRemove:
                                                        desc = desc.replace(letter,"")
                                                    if len(desc) > 95:
                                                        desc = desc[:95] + "(...)"
                                                mainOptions += [interactions.SelectOption(label=unhyperlink(a.name),value=str(cmpt),emoji=getEmojiObject(a.emoji),description=desc)]
                                            else:
                                                mainOptions += [interactions.SelectOption(label=unhyperlink(a.name),value=str(cmpt),emoji=getEmojiObject(a.emoji))]
                                            cmpt += 1

                                        mainSelect = interactions.SelectMenu(custom_id = "selectAOption", options=mainOptions,placeholder = "Séléctionnez une option :")
                                        emby = interactions.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color)
                                        if footerText != "":
                                            emby.set_footer(text=footerText,icon_url=ctx.author.avatar_url)

                                        if haveIterate:                         # Time limite stuff
                                            await msg.edit(embeds = [embInfo,emby,interactions.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = choiceMsgTemp)],components=[infoSelect,waitingSelect])
                                            await asyncio.sleep(3)

                                        await msg.edit(embeds = [embInfo,emby,interactions.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = choiceMsgTemp)],components=[infoSelect,interactions.ActionRow(components=[mainSelect])])
                                        haveIterate = True

                                        validoption = False
                                        def checkMainOption(m):
                                            return int(m.author.id) == actTurn.char.owner
                                        while not(validoption):
                                            try:
                                                react = await bot.wait_for_component(messages=msg,check=checkMainOption,timeout = 30)
                                            except:
                                                unsuccess = True
                                                break

                                            mainSelect = interactions.ActionRow(components=[getChoisenSelect(mainSelect,react.data.values[0])])
                                            react = canBeUsed[int(react.data.values[0])]
                                            validoption = True

                                        choiceMsgTemp = ""

                                        # Second Menu generating
                                        if type(react) == weapon:
                                            viArea = actTurn.cell.getArea(area=actTurn.char.weapon.effectiveRange,team=actTurn.team,fromCell=actTurn.cell)
                                            for celly in viArea[:]:
                                                if celly.on != None and (celly.on in atRange and celly.on.team != actTurn.team):
                                                    direction = getDirection(actTurn.cell,celly)
                                                    if direction == FROM_LEFT:
                                                        cellToFind = findCell(celly.x+1,celly.y,tablAllCells)
                                                        if cellToFind != None:
                                                            for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=actTurn.cell):
                                                                if celly2 in viArea:
                                                                    viArea.remove(celly2)
                                                    elif direction == FROM_RIGHT:
                                                        cellToFind = findCell(celly.x-1,celly.y,tablAllCells)
                                                        if cellToFind != None:
                                                            for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=actTurn.cell):
                                                                if celly2 in viArea:
                                                                    viArea.remove(celly2)
                                                    elif direction == FROM_UP:
                                                        cellToFind = findCell(celly.x,celly.y+1,tablAllCells)
                                                        if cellToFind != None:
                                                            for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=actTurn.cell):
                                                                if celly2 in viArea:
                                                                    viArea.remove(celly2)
                                                    elif direction == FROM_RIGHT:
                                                        cellToFind = findCell(celly.x,celly.y-1,tablAllCells)
                                                        if cellToFind != None:
                                                            for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=actTurn.cell):
                                                                if celly2 in viArea:
                                                                    viArea.remove(celly2)

                                            weapOptions, choiceMsgTemp = [], "__Carte :__\n{0}\n\n__Combattants à portée :__\n".format(map(tablAllCells,bigMap,actTurn.cell.getArea(area=actTurn.char.weapon.effectiveRange,team=actTurn.team,fromCell=actTurn.cell),fromEnt=actTurn,wanted=actTurn.char.weapon.target,numberEmoji=atRange))
                                            for a in range(0,nbTargetAtRange):
                                                choiceMsgTemp += f"{listNumberEmoji[a]} - {atRange[a].quickEffectIcons()}"
                                                desc = f"PV : {int(atRange[a].hp/atRange[a].maxHp*100)}%, Pos : {atRange[a].cell.x} - {atRange[a].cell.y}"
                                                if react.area != AREA_MONO:
                                                    desc += f", Zone : {len(atRange[a].cell.getEntityOnArea(area=actTurn.char.weapon.area,team=actTurn.team,wanted=actTurn.char.weapon.target,directTarget=False,fromCell=actTurn.cell))}"
                                                weapOptions += [interactions.SelectOption(label=listNumberEmoji[a] + " "+unhyperlink(atRange[a].char.name),value=str(a),emoji=getEmojiObject(atRange[a].icon),description=desc)]

                                            weapOptions += [interactions.SelectOption(label="Retour",value=str(a+1),emoji=Emoji(name='\u25C0'))]
                                            weapSelect = interactions.SelectMenu(custom_id = "weapSelect", options=weapOptions,placeholder="Sélectionnez une cible :")

                                            if len(weapOptions) == 2:
                                                temp,cmpt =[],0
                                                for a in weapOptions:
                                                    temp+=[interactions.Button(type=2, style=1+cmpt, label=a.label, emoji=a.emoji, value= a.value)]
                                                    cmpt += 1
                                                weapSelect = [interactions.ActionRow(components=[temp[0],temp[1]])]
                                                await msg.edit(embeds = [embInfo,emby,interactions.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp)],components=[mainSelect]+weapSelect)

                                            elif choiceMsgTemp != "":
                                                await msg.edit(embeds = [embInfo,emby,interactions.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp)],components=[mainSelect,waitingSelect])
                                                await asyncio.sleep(3)
                                                await msg.edit(embeds = [embInfo,emby,interactions.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp)],components=[mainSelect,interactions.ActionRow(components=[weapSelect])])

                                            try:
                                                react = await bot.wait_for_component(messages=choiceEmbed,check=check,timeout=timeLimite)
                                            except:
                                                unsuccess = True
                                                await choiceEmbed.remove_all_reactions()
                                                break

                                            if len(weapOptions) > 2:
                                                selectedOptionSelect = [getChoisenSelect(weapSelect,react.data.values[0])]
                                            else:
                                                selectedOptionSelect = None

                                            optionChoice = OPTION_WEAPON
                                            try:
                                                value = int(react.data.values[0])
                                            except:
                                                value = int(react.custom_id)
                                            if value<len(atRange):
                                                ennemi = atRange[value]
                                                haveOption = True

                                        elif type(react) == skill:
                                            skillToUse,targetAtRangeSkill,a, funnyTempVarName, funnyTempVarNameButTheSecond = react,[],-1, [TYPE_ARMOR,TYPE_BOOST,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ,TYPE_RESURECTION,TYPE_HEAL],[TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE]

                                            if skillToUse.type == TYPE_UNIQUE:
                                                targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALL,fromCell=actTurn.cell)
                                            elif skillToUse.range != AREA_MONO:
                                                if skillToUse.type in funnyTempVarName:
                                                    targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.range,team=actTurn.team,wanted=ALLIES,dead=skillToUse.type == TYPE_RESURECTION,fromCell=actTurn.cell)
                                                elif skillToUse.type in funnyTempVarNameButTheSecond:
                                                    targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.range,team=actTurn.team,wanted=ENEMIES,lineOfSight=True,fromCell=actTurn.cell)
                                                else:
                                                    tablCells = actTurn.cell.getArea(area=react.range,team=actTurn.team,fromCell=actTurn.cell)
                                                    for celly in tablCells[:]:
                                                        if celly.depl != None:
                                                            tablCells.remove(celly)
                                                    tablCells.sort(key=lambda ballerine: len(ballerine.getEntityOnArea(area=react.depl.skills.area,team=actTurn.team,wanted=[ALLIES,ENEMIES][react.depl.skills.type in hostilesTypes], ignoreInvoc = True, directTarget=False, fromCell= ballerine))+0.5-(ballerine.distance(actTurn.cell)*0.1),reverse=True)
                                                    targetAtRangeSkill = tablCells[:min(len(tablCells),5)]
                                            else:
                                                if skillToUse.type in funnyTempVarName:
                                                    targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES,directTarget=False,fromCell=actTurn.cell)
                                                elif skillToUse.type in funnyTempVarNameButTheSecond:
                                                    targetAtRangeSkill = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENEMIES,directTarget=False,fromCell=actTurn.cell)

                                            viArea, altViArea = actTurn.cell.getArea(area=[skillToUse.range,skillToUse.area][skillToUse.range==AREA_MONO],team=actTurn.team,fromCell=actTurn.cell), actTurn.cell.getArea(area=[skillToUse.range,skillToUse.area][skillToUse.range==AREA_MONO],team=actTurn.team,fromCell=actTurn.cell)
                                            if skillToUse.range != AREA_MONO and skillToUse.type in [TYPE_DAMAGE,TYPE_MALUS,TYPE_INDIRECT_DAMAGE]:
                                                for celly in viArea[:]:
                                                    if celly.on != None and (celly.on in atRange and celly.on.team != actTurn.team):
                                                        direction = getDirection(actTurn.cell,celly)
                                                        if direction == FROM_RIGHT:
                                                            cellToFind = findCell(celly.x+1,celly.y,tablAllCells)
                                                            if cellToFind != None:
                                                                for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=actTurn.cell):
                                                                    try:
                                                                        viArea.remove(celly2)
                                                                    except:
                                                                        pass
                                                        elif direction == FROM_LEFT:
                                                            cellToFind = findCell(celly.x-1,celly.y,tablAllCells)
                                                            if cellToFind != None:
                                                                for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=actTurn.cell):
                                                                    try:
                                                                        viArea.remove(celly2)
                                                                    except:
                                                                        pass
                                                        elif direction == FROM_DOWN:
                                                            cellToFind = findCell(celly.x,celly.y+1,tablAllCells)
                                                            if cellToFind != None:
                                                                for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=actTurn.cell):
                                                                    try:
                                                                        viArea.remove(celly2)
                                                                    except:
                                                                        pass
                                                        elif direction == FROM_UP:
                                                            cellToFind = findCell(celly.x,celly.y-1,tablAllCells)
                                                            if cellToFind != None:
                                                                for celly2 in cellToFind.getArea(area=AREA_CONE_7,fromCell=actTurn.cell):
                                                                    try:
                                                                        viArea.remove(celly2)
                                                                    except:
                                                                        pass

                                            skillOptions, choiceMsgTemp = [], "__Carte :__\n{0}\n\n__Combattants à portée :__\n".format(map(tablAllCells,bigMap,viArea,fromEnt=actTurn,wanted=[ENEMIES,ALLIES][skillToUse.type in funnyTempVarName],numberEmoji=targetAtRangeSkill,fullArea=altViArea))

                                            if skillToUse.type not in [TYPE_SUMMON,TYPE_DEPL]:
                                                nbTargetAtRangeSkill = len(targetAtRangeSkill)

                                                for a in range(nbTargetAtRangeSkill):
                                                    choiceMsgTemp += f"{listNumberEmoji[a]} - {targetAtRangeSkill[a].quickEffectIcons()}"
                                                    desc = f"PV : {int(targetAtRangeSkill[a].hp/targetAtRangeSkill[a].maxHp*100)}%, Pos : {targetAtRangeSkill[a].cell.x} - {targetAtRangeSkill[a].cell.y}"
                                                    if react.area not in [AREA_MONO,AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES]:
                                                        if react.type in funnyTempVarName:
                                                            wanted = ALLIES
                                                        else:
                                                            wanted = ENEMIES
                                                        desc += f", Zone : {len(targetAtRangeSkill[a].cell.getEntityOnArea(area=react.area,team=actTurn.team,wanted=wanted,directTarget=False,fromCell=actTurn.cell))}"
                                                    skillOptions += [interactions.SelectOption(label=listNumberEmoji[a] + " "+unhyperlink(targetAtRangeSkill[a].char.name),value=str(a),emoji=getEmojiObject(targetAtRangeSkill[a].icon),description=desc)]
                                                
                                                if react.area in [AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES] or react.range == AREA_MONO:
                                                    skillOptions = [interactions.SelectOption(label="Valider",value='✅',emoji=Emoji(name='✅'))]

                                            elif skillToUse.type == TYPE_SUMMON:
                                                choiceMsgTemp =f"Voulez vous invoquer {skillToUse.invocation} ?"
                                                skillOptions = [interactions.SelectOption(label="Valider",value='✅',emoji=Emoji(name='✅'))]
                                                a = 0

                                            else:
                                                nbTargetAtRangeSkill = len(targetAtRangeSkill)

                                                for a in range(nbTargetAtRangeSkill):
                                                    choiceMsgTemp += f"{listNumberEmoji[a]} - {targetAtRangeSkill[a].x}:{targetAtRangeSkill[a].y}\n"
                                                    desc = f"{targetAtRangeSkill[a].x} - {targetAtRangeSkill[a].y}"
                                                    desc += f", Zone : {len(targetAtRangeSkill[a].getEntityOnArea(area=react.depl.skills.area,team=actTurn.team,wanted=[ALLIES,ENEMIES][react.depl.skills.type in hostilesTypes],directTarget=False,fromCell=actTurn.cell))}"
                                                    skillOptions += [interactions.SelectOption(label=str(targetAtRangeSkill[a].x) + ":" + str(targetAtRangeSkill[a].y),value=str(a),emoji=Emoji(name=listNumberEmoji[a]),description=desc)]
                                                
                                                if react.area in [AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES] or react.range == AREA_MONO:
                                                    skillOptions = [interactions.SelectOption(label="Valider",value='✅',emoji=Emoji(name='✅'))]

                                            skillOptions += [interactions.SelectOption(label="Retour",value=str(a+1),emoji=Emoji(name='\u25C0'))]
                                            skillSelect = interactions.SelectMenu(custom_id = "skillOptions", options=skillOptions)

                                            if len(skillOptions) == 2:
                                                temp,cmpt =[],0
                                                for a in skillOptions:
                                                    tipe = 1
                                                    if a["label"] == 'Valider':
                                                        tipe = 3
                                                    elif a["label"] == "Retour":
                                                        tipe = 2
                                                    temp+=[interactions.Button(type=2, style=tipe,label=a.label, emoji=a.emoji, value= a.value)]
                                                    cmpt += 1
                                                skillSelect = [interactions.ActionRow(components=[temp[0],temp[1]])]
                                                await msg.edit(embeds = [embInfo,emby,interactions.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp)],components=[infoSelect,mainSelect]+skillSelect)

                                            elif choiceMsgTemp != "":
                                                await msg.edit(embeds = [embInfo,emby,interactions.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp)],components=[infoSelect,mainSelect,waitingSelect])
                                                await asyncio.sleep(3)
                                                await msg.edit(embeds = [embInfo,emby,interactions.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp)],components=[infoSelect,mainSelect]+[interactions.ActionRow(components=[skillSelect])])

                                            try:
                                                react = await bot.wait_for_component(messages=choiceEmbed,timeout = 30,check=check)
                                            except:
                                                unsuccess = True
                                                await choiceEmbed.remove_all_reactions()
                                                break

                                            if len(skillOptions) > 2:
                                                selectedOptionSelect = [getChoisenSelect(skillSelect,react.data.values[0])]
                                            else:
                                                selectedOptionSelect = None

                                            optionChoice = OPTION_SKILL
                                            try:
                                                value = react.data.values[0]
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
                                                        movingOption[cmpt] = interactions.Button(type=2, style=2, label="Aller sur {0}:{1}".format(surrondings[cmpt].x,surrondings[cmpt].y),emoji=moveEmoji[cmpt],custom_id=moveEmoji[cmpt],disabled=not(canMove[cmpt]))
                                                    else:
                                                        movingOption[cmpt] = interactions.Button(type=2, style=2,label="Aller en dehors du monde",emoji=moveEmoji[cmpt],custom_id=moveEmoji[cmpt],disabled=True)

                                                allMouvementOptions = interactions.ActionRow(components=[movingOption[0],movingOption[1],movingOption[2],movingOption[3]])
                                                tablSurrendCells = [[findCell(actCell.x-1,actCell.y-1,tablAllCells),findCell(actCell.x-0,actCell.y-1,tablAllCells),findCell(actCell.x+1,actCell.y-1,tablAllCells)],[findCell(actCell.x-1,actCell.y,tablAllCells),findCell(actCell.x-0,actCell.y,tablAllCells),findCell(actCell.x+1,actCell.y,tablAllCells)],[findCell(actCell.x-1,actCell.y+1,tablAllCells),findCell(actCell.x-0,actCell.y+1,tablAllCells),findCell(actCell.x+1,actCell.y+1,tablAllCells)]]
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

                                                await msg.edit(embeds = [embInfo,emby,interactions.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = "Dans quelle direction voulez vous aller ?\n\n"+mapLike)],components=[infoSelect,cancelButton,allMouvementOptions])

                                                choiceToMove = None
                                                while choiceToMove == None:
                                                    try:
                                                        choiceMove = await bot.wait_for_component(messages=choiceEmbed,timeout=30,check=check)
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
                                    choiceEmbed = [interactions.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = "Tour en cours "+emLoading)]

                                if not(actTurn.auto) and unsuccess:
                                    if actTurn.missedLastTurn == False:
                                        actTurn.missedLastTurn = True

                                    else:
                                        actTurn.auto = True
                                        nowStartOfTurn = datetime.now()

                                elif not(actTurn.auto) and not(unsuccess):
                                    actTurn.missedLastTurn = False

                                if unsuccess or type(ennemi)==int: # AI's stuffs
                                    team2maxHp, team2Hp, team1maxHp, team1Hp, optionChoisen = 0, 0, 0, 0, False
                                    for ent in tablEntTeam[int(not(actTurn.team))]:
                                        team2maxHp, team2Hp = team2maxHp+ent.maxHp, team2Hp+ent.hp
                                    for ent in tablEntTeam[actTurn.team]:
                                        team1maxHp, team1Hp = team1maxHp+ent.maxHp, team1Hp+ent.hp

                                    ennemiesdying, alliesdying = team2Hp / team2maxHp <= 0.3, team1Hp / team1maxHp <= 0.4
                                    
                                    # Définition du type d'IA :
                                    choisenIA = actTurn.IA

                                    if actTurn.char.aspiration in [IDOLE, INOVATEUR, PREVOYANT, VIGILANT, MASCOTTE]:
                                        allyDPTAlive = 0
                                        for ent in tablEntTeam[actTurn.team]:
                                            if ent.char.aspiration in [BERSERK,OBSERVATEUR,POIDS_PLUME,TETE_BRULE,MAGE,ENCHANTEUR,ATTENTIF,SORCELER] and ent.hp > 0:
                                                allyDPTAlive += 1

                                        if allyDPTAlive <= 2 or ennemiesdying or tour > 15:
                                            choisenIA = AI_OFFERUDIT

                                    logs += "\nAuto Fighter. Selected AI : {0}".format(["AI Damage","AI Booster","AI Shield","AI Aventurer","AI Healer","AI Agressive Supp","AI Mage","AI Enchant",][choisenIA])
                                    
                                    # Définition des probabilités :
                                    # [DPT_PHYS,BOOST,SHIELD,AVENTURE,ALTRUISTE,OFFERUt,MAGE,ECHANT]

                                    if actTurn.isNpc("Séréna") and actTurn.cooldowns[2] == 0:
                                        poisonCount = 0
                                        for ent in tablEntTeam[int(not(actTurn.team))]:
                                            for eff in ent.effects:
                                                if eff.effects.id == estal.id:
                                                    poisonCount += 1

                                        if poisonCount >= 8:
                                            optionChoice = OPTION_SKILL
                                            skillToUse = serenaSpe
                                            ennemi = actTurn
                                            optionChoisen = True

                                    elif actTurn.isNpc("Ailill") and actTurn.cooldowns[0] == 0:
                                        atRangeAilill = actTurn.cell.getEntityOnArea(area=ailillSkill.range,team=actTurn.team,fromCell=actTurn.cell,wanted=ENEMIES,lineOfSight=True,effect=ailillSkill.effects,ignoreInvoc = (ailillSkill.effectOnSelf == None or (ailillSkill.effectOnSelf != None and findEffect(ailillSkill.effectOnSelf).replica != None)))
                                        if len(atRange) > 0:
                                            optionChoice = OPTION_SKILL
                                            skillToUse = ailillSkill
                                            atRangeAilill.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
                                            ennemi = atRange[0]
                                            optionChoisen = True

                                    elif (actTurn.isNpc("Luna prê.") or actTurn.isNpc("Luna ex.")) and (actTurn.cooldowns[0] == 0 or (actTurn.hp/actTurn.maxHp <= 0.25 and actTurn.cooldowns[0] < 10)):
                                        optionChoice = OPTION_SKILL
                                        skillToUse = lunaSpeCast
                                        optionChoisen = True
                                        for ent in tablEntTeam[int(not(actTurn.team))]:
                                            if ent.isNpc("Iliana") and ent.hp > 0:
                                                ennemi = ent
                                                break

                                        if ennemi == None:
                                            atRange = actTurn.cell.getEntityOnArea(area=AREA_ALL_ENEMIES,fromCell=actTurn.cell,team=actTurn.team,wanted=ENEMIES)
                                            atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
                                            ennemi = atRange[0]

                                    elif actTurn.isNpc("Clémence pos.") and actTurn.cooldowns[2] == 0 and (tour >= 7 or actTurn.hp/actTurn.maxHp <= 0.35):
                                        optionChoice = OPTION_SKILL
                                        skillToUse = clemUltCast
                                        ennemi = actTurn
                                        optionChoisen = True

                                    elif actTurn.isNpc("Akira H.") and actTurn.hp/actTurn.maxHp <= 0.15:
                                        optionChoice = OPTION_SKILL
                                        skillToUse = akikiEnrageCastInit
                                        ennemi = actTurn
                                        optionChoisen = True                                    

                                    elif actTurn.char.aspiration in [IDOLE, INOVATEUR, VIGILANT, PROTECTEUR, MASCOTTE] and not(allReadyMove):
                                        nbAllies = len(actTurn.cell.getEntityOnArea(area=AREA_DONUT_3,team=actTurn.team,wanted=ALLIES,lineOfSight=False,lifeUnderPurcentage=99999,dead=False,effect=[None],ignoreInvoc = True, directTarget=False,ignoreAspiration = None,fromCell=actTurn.cell))
                                        nbAliveAllies = 0
                                        for ent in tablEntTeam[actTurn.team]:
                                            if type(ent.char) not in [invoc, depl] and ent.hp > 0:
                                                nbAliveAllies += 1
                                        if nbAllies < nbAliveAllies/2:
                                            potCell = actTurn.getCellToMove(cellToMove=findCell(2, [2,3][bigMap], tablAllCells))
                                            if potCell != None:
                                                optionChoice,choiceToMove,optionChoisen = OPTION_MOVE, potCell, True
                                    
                                    if not(optionChoisen):
                                        probaAtkWeap = [50,40,40,40,40,50,50,50] 
                                        probaHealWeap = [20,50,30,30,50,30,20,20]
                                        probaReaSkill = [50,220,200,30,200,100,50,50]
                                        probaIndirectReaSkill = [30,150,100,30,150,80,30,30]
                                        probaAtkSkill = [100,65,70,50,50,100,100,100]
                                        probaIndirectAtkSkill = [50,40,40,30,40,120,100,100]
                                        probaHealSkill = [50,100,70,30,130,50,30,30]
                                        probaBoost = [50,130,50,30,70,50,30,50]
                                        probaMalus = [50,40,100,30,50,50,50,50]
                                        probaArmor = [50,100,150,30,70,50,50,35]
                                        probaInvoc = [80,80,80,80,80,80,80,80]
                                        probaDepl = [70,70,70,70,70,70,70,70]

                                        tablSetProb = [
                                            [probaAtkWeap,probaHealWeap],
                                            [probaAtkSkill,probaIndirectAtkSkill],
                                            [probaHealSkill,probaReaSkill,probaIndirectReaSkill],
                                            [probaArmor],
                                            [probaBoost],
                                            [probaMalus],
                                            [probaInvoc,probaDepl]
                                        ]
                                        tablCharSet = [
                                            actTurn.char.charSettings["weaponUse"],
                                            actTurn.char.charSettings["dmgSkillUse"],
                                            actTurn.char.charSettings["healSkillUse"],
                                            actTurn.char.charSettings["armorSkillUse"],
                                            actTurn.char.charSettings["buffSkillUse"],
                                            actTurn.char.charSettings["debuffSkillUse"],
                                            actTurn.char.charSettings["summonSkillUse"],
                                            ]

                                        for cmpt1 in range(len(tablCharSet)):
                                            for cmpt2 in range(len(tablSetProb[cmpt1])):
                                                tablSetProb[cmpt1][cmpt2][choisenIA] = int(tablSetProb[cmpt1][cmpt2][choisenIA] * [0.5,1,1.5][tablCharSet[cmpt1]])

                                        # There is a ennemi casting ?
                                        ennemiCast = False
                                        for ent in tablEntTeam[int(not(actTurn.team))]:
                                            for eff in ent.effects:
                                                if eff.effects.replica != None and eff.effects.id != clemultCastEffect.id:
                                                    skillFinded = findSkill(eff.effects.replica)
                                                    if (skillFinded.effectOnSelf == None and skillFinded.type in [TYPE_DAMAGE]) or (skillFinded.effectOnSelf != None and findEffect(skillFinded.effectOnSelf).replica == None) and skillFinded.area != AREA_MONO:
                                                        ennemiCast = True
                                                        break

                                        if ennemiCast:
                                            logs += "\nA ennemi is casting !"
                                            probaArmor[actTurn.IA] = int(probaArmor[choisenIA] *2)
                                        if alliesdying and not(ennemiesdying):
                                            probaHealSkill[choisenIA] = int(probaHealSkill[choisenIA] * 1.25)                                 
                                        
                                        # Weapons proba's ----------------------------------
                                        if actTurn.char.weapon.name.lower() == "noneweap" or actTurn.char.weapon.id.lower() == "noneweap" or (actTurn.char.weapon.id in cannotUseMainWeapon and len(actTurn.atRange()) > 0):
                                            probaHealWeap = [0,0,0,0,0,0,0,0]
                                            probaAtkWeap = [0,0,0,0,0,0,0,0]
                                        else:
                                            if actTurn.char.weapon.type == TYPE_DAMAGE:
                                                probaHealWeap = [0,0,0,0,0,0,0,0]
                                            elif actTurn.char.weapon.type == TYPE_HEAL:
                                                probaAtkWeap = [0,0,0,0,0,0,0,0]
                                                if len(actTurn.cell.getEntityOnArea(area=actTurn.char.weapon.effectiveRange,team=actTurn.team,wanted=ALLIES,directTarget=True,ignoreInvoc=True,lifeUnderPurcentage=90,fromCell=actTurn.cell)) == 0 and len(actTurn.cell.getEntityOnArea(area=actTurn.char.weapon.effectiveRange,team=actTurn.team,wanted=ALLIES,directTarget=True,ignoreInvoc=True,fromCell=actTurn.cell)) > 0:
                                                    probaHealWeap = [0,0,0,0,0,0,0,0]

                                        reduceWeaponProbaNPC = ["Séréna","Clémence Exaltée","Clémence Possédée","Akira H."]

                                        for NPCName in reduceWeaponProbaNPC:
                                            if actTurn.isNpc(NPCName):
                                                probaAtkWeap[choisenIA] = probaAtkWeap[choisenIA] * 0.1
                                                break

                                        surron = actTurn.cell.surrondings()
                                        if len(actTurn.atRange()) == 0 and (surron[0] != None and surron[0].on != None) and (surron[1] != None and surron[1].on != None) and (surron[2] != None and surron[2].on != None) and (surron[3] != None and surron[3].on != None):
                                            probaAtkWeap = [0,0,0,0,0,0,0,0]

                                        try:
                                            if actTurn.isNpc("Alice Exaltée") and actTurn.specialVars["clemBloodJauge"].value <= 40:
                                                probaHealWeap[actTurn.IA] = int(probaHealWeap[actTurn.IA]*1.35)
                                                probaBoost[actTurn.IA] = int(probaBoost[actTurn.IA]*0.6)
                                                probaHealSkill[actTurn.IA] = int(probaHealSkill[actTurn.IA] * 0.9)
                                                probaAtkSkill[actTurn.IA] = int(probaAtkSkill[actTurn.IA] * 0.7)
                                        except Exception as e:
                                            logs += "\n{0}".format(e)
                                            tempTurnMsg += "\n{0}\n".format(e)

                                        if actTurn.isNpc("Luna ex.") and len(atRange) > 0:
                                            probaAtkSkill[actTurn.IA] = probaAtkSkill[actTurn.IA] * 2

                                        elif actTurn.isNpc("Lio"):
                                            downedAllies = 0
                                            for ent in tablEntTeam[actTurn.team]:
                                                if ent.hp <= 0:
                                                    downedAllies += 1
                                            probaAtkSkill[choisenIA] = probaAtkSkill[choisenIA] * (1 + downedAllies/7)
                                        
                                        if actTurn.char.weapon.id in [whiteSpiritWings.id,bleuSpiritWings.id,fleau.id]:
                                            probaAtkWeap[actTurn.IA] = int(probaAtkWeap[actTurn.IA] * 1.5)

                                        # Do we have a big buff ? If yes, maybe we should consider using skills if we can't attack
                                        bigbuffy, dmgUpValue = actTurn.allStats()[actTurn.char.weapon.use] >= actTurn.baseStats[actTurn.char.weapon.use] * 1.1, 0
                                        if not(bigbuffy):
                                            for a in actTurn.effects:
                                                if a.effects.id == dmgUp.id:
                                                    dmgUpValue += a.effects.power
                                        bigbuffy = dmgUpValue >= max(5,actTurn.level / 5)

                                        if bigbuffy:
                                            logs += "\nDmg or stat buff detected"                                    

                                        if bigbuffy and nbTargetAtRange < 0:
                                            logs += " but no target in the range of the weapon is found"
                                            haveOffSkills = False
                                            for a in range(7):
                                                if actTurn.cooldowns[a] <= 0 and type(actTurn.skills[a]) == skill:
                                                    if actTurn.skills[a].type == TYPE_DAMAGE:
                                                        if (actTurn.skills[a].range == AREA_MONO and len(actTurn.cell.getEntityOnArea(area=actTurn.skills[a].area,team=actTurn.team,wanted=ENEMIES,effect=actTurn.skills[a].effects,fromCell=actTurn.cell))> 0) or (actTurn.skills[a].range != AREA_MONO and len(actTurn.cell.getEntityOnArea(area=actTurn.skills[a].range,team=actTurn.team,wanted=ENEMIES,fromCell=actTurn.cell,effect=actTurn.skills[a].effects))> 0):
                                                            haveOffSkills = True
                                                            break

                                            if haveOffSkills:
                                                probaHealWeap = [0,0,0,0,0,0,0,0]
                                                probaAtkWeap = [0,0,0,0,0,0,0,0]
                                                logs += "\nSomes offensives skills with targets at range have been found. Weapon's proba neutralized"
                                            else:
                                                logs += "\nNo available offensives skills have been found"

                                        qCast = False
                                        for eff in actTurn.effects:
                                            if eff.effects.id == quickCastEff.id:
                                                qCast = True
                                                probaHealWeap[actTurn.IA] = 0
                                                probaAtkWeap[actTurn.IA] = 0
                                                break

                                        healSkill,atkSkill,reaSkill,indirectReaSkill,indirectAtkSkill,boostSkill,malusSkill,armorSkill,invocSkill,deplSkills = [],[],[],[],[],[],[],[],[],[]

                                        for a in range(7): # Catégorisation des sorts
                                            actSkill = actTurn.char.skills[a]

                                            if actTurn.cooldowns[a] == 0 and type(actSkill) == classes.skill and not(actTurn.silent) and actSkill.id != "lb":
                                                if actSkill.become == None:
                                                    tablToLook = [actSkill]

                                                else:
                                                    tablToLook, tablEffId = [], []
                                                    for eff in actTurn.effects:
                                                        tablEffId.append(eff.effects.id)

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

                                                cpTablToLook = tablToLook[:]
                                                for cmpt in range(len(cpTablToLook)):
                                                    jaugeConds, jaugeValue = cpTablToLook[cmpt].jaugeEff == None, 0
                                                    if not(jaugeConds):
                                                        try:
                                                            if teamJaugeDict[actTurn.team][actTurn].effects.id == cpTablToLook[cmpt].jaugeEff.id:
                                                                jaugeConds, jaugeValue = teamJaugeDict[actTurn.team][actTurn].value >= cpTablToLook[cmpt].minJaugeValue, teamJaugeDict[actTurn.team][actTurn].value
                                                        except KeyError:
                                                            jaugeConds = cpTablToLook[cmpt].minJaugeValue <= 0

                                                    if not(jaugeConds):
                                                        try:
                                                            tablToLook.remove(cpTablToLook[cmpt])
                                                        except:
                                                            pass

                                                for actSkill in tablToLook:
                                                    jaugeValue = 0
                                                    raisable = actTurn.cell.getEntityOnArea(area=[actSkill.range,actSkill.area][actSkill.range == AREA_MONO],fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,dead=True)
                                                    if actSkill.jaugeEff != None:
                                                        try:
                                                            if teamJaugeDict[actTurn.team][actTurn].effects.id == actSkill.jaugeEff.id:
                                                                jaugeValue = teamJaugeDict[actTurn.team][actTurn].value
                                                        except KeyError:
                                                            pass
                                                    
                                                    if actSkill.type in friendlyTypes+hostilesTypes:
                                                        if actSkill.range == AREA_MONO:
                                                            tablAtRangeTargets, posTarget = [actTurn], actTurn
                                                        else:
                                                            tablAtRangeTargets = actTurn.cell.getEntityOnArea(area=actSkill.range,team=actTurn.team,wanted=[ENEMIES,ALLIES][actSkill.type in friendlyTypes],effect=actSkill.effects,fromCell=actTurn.cell,directTarget=actSkill.type in hostilesTypes,lifeUnderPurcentage=[90,99999][actSkill.type in hostilesTypes],dead=actSkill.type == TYPE_RESURECTION)
                                                            if actSkill.type in hostilesTypes:
                                                                tablAtRangeTargets.sort(key=lambda ballerine: actTurn.getAggroValue(ballerine),reverse=True)
                                                            elif actSkill.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_ARMOR]:
                                                                tablAtRangeTargets.sort(key=lambda ballerine: getHealAggro(actTurn,ballerine,actSkill,armor=actSkill.type == TYPE_ARMOR),reverse=True)
                                                            elif actSkill.type in [TYPE_BOOST]:
                                                                tablAtRangeTargets.sort(key=lambda ballerine: getBuffAggro(actTurn,ballerine,actSkill.effects[0]),reverse=True)

                                                            if len(tablAtRangeTargets) > 0:
                                                                posTarget = tablAtRangeTargets[0]
                                                            else:
                                                                posTarget = None

                                                        if posTarget != None:
                                                            if actSkill.area == AREA_MONO:
                                                                tablHotEnemiesInArea = [posTarget]
                                                            else:
                                                                tablHotEnemiesInArea = posTarget.cell.getEntityOnArea(area=actSkill.area,team=actTurn.team,wanted=ENEMIES,effect=actSkill.effects,fromCell=actTurn.cell,directTarget=False)
                                                            nbHotTargetsInArea = len(tablHotEnemiesInArea)

                                                            if nbHotTargetsInArea >= actSkill.minTargetRequired:
                                                                iaPow = actSkill.iaPow * nbHotTargetsInArea
                                                                if actSkill.jaugeEff != None:
                                                                    try:
                                                                        if teamJaugeDict[actTurn.team][actTurn].effects.id == actSkill.jaugeEff.id and teamJaugeDict[actTurn.team][actTurn].value >= 85:
                                                                            iaPow = iaPow + 150
                                                                        elif teamJaugeDict[actTurn.team][actTurn].effects.id == actSkill.jaugeEff.id and teamJaugeDict[actTurn.team][actTurn].value >= 35:
                                                                            iaPow = iaPow + 50
                                                                    except:
                                                                        pass
                                                                if actSkill.needEffect != None:
                                                                    iaPow = iaPow + 150

                                                                maxCmpt, cmpt = iaPow//10, 1
                                                                if actSkill.type == TYPE_DAMAGE:
                                                                    while cmpt <= maxCmpt:
                                                                        atkSkill.append(actSkill)
                                                                        cmpt += 1
                                                                elif actSkill.type == TYPE_INDIRECT_DAMAGE:
                                                                    while cmpt <= maxCmpt:
                                                                        indirectAtkSkill.append(actSkill)
                                                                        cmpt += 1
                                                                elif actSkill.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL]:
                                                                    while cmpt <= maxCmpt:
                                                                        healSkill.append(actSkill)
                                                                        cmpt += 1
                                                                elif actSkill.type == TYPE_ARMOR:
                                                                    while cmpt <= maxCmpt:
                                                                        armorSkill.append(actSkill)
                                                                        cmpt += 1
                                                                elif actSkill.type == TYPE_BOOST:
                                                                    while cmpt <= maxCmpt:
                                                                        boostSkill.append(actSkill)
                                                                        cmpt += 1
                                                                elif actSkill.type == TYPE_MALUS:
                                                                    while cmpt <= maxCmpt:
                                                                        malusSkill.append(actSkill)
                                                                        cmpt += 1
                                                                elif actSkill.type == TYPE_RESURECTION:
                                                                    while cmpt <= maxCmpt:
                                                                        reaSkill.append(actSkill)
                                                                        cmpt += 1

                                                    else:
                                                        if actSkill.range == AREA_MONO:                                     # If the skill is launch on self
                                                            if actSkill.type == TYPE_SUMMON and len(actTurn.cell.getEmptyCellsInArea(area=actSkill.range,team=actTurn.team,fromCell=actTurn.cell))>0 and not(qCast): # Invocation
                                                                temp = actTurn.cell.getEmptyCellsInArea(area=actSkill.range,team=actTurn.team)
                                                                for b in temp[:]:
                                                                    if [b.x > 2, b.x < 3][actTurn.team] :
                                                                        temp.remove(b)

                                                                if len(temp) > 0:
                                                                    invocSkill.append(actSkill)
                                                            elif actSkill.type == TYPE_DEPL and len(actTurn.cell.getEntityOnArea(area=actSkill.depl.skills.area,team=actTurn.team,wanted=[ALLIES,ENEMIES][actSkill.depl.skills.type in hostilesTypes],ignoreInvoc = True, directTarget=False ,fromCell=actTurn.cell)) > 1:
                                                                deplSkills.append(actSkill)

                                                            elif actSkill.id in ["ul",abnegation.id] and not(qCast): 
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
                                                            if actSkill.type == TYPE_UNIQUE and not(qCast):
                                                                for b in [chaos]: # Boost
                                                                    if b == actSkill:
                                                                        boostSkill.append(b)
                                                            elif actSkill.type == TYPE_SUMMON and actTurn.cell.getCellForSummon(area=actSkill.range, team=actTurn.team, summon= findSummon(actSkill.invocation), summoner=actTurn) != None and not(qCast):
                                                                invocSkill.append(actSkill)
                                                                if actSkill.ultimate:
                                                                    probaInvoc[choisenIA] = probaInvoc[choisenIA]*2
                                                                    invocSkill.append(actSkill)
                                                                    invocSkill.append(actSkill)
                                                            elif actSkill.type == TYPE_DEPL:
                                                                deplSkills.append(actSkill)

                                        if LBBars[actTurn.team][0]> 0 and LBBars[actTurn.team][1]//3 >= 1 and type(actTurn.char) not in [invoc,octarien]:
                                            if LBBars[actTurn.team][1]//3 == 1:
                                                lbSkill = lb1Tabl[actTurn.char.aspiration]
                                            elif LBBars[actTurn.team][1]//3 == 2:
                                                lbSkill = lb2Tabl[actTurn.char.aspiration]
                                            elif LBBars[actTurn.team][1]//3 == 3:
                                                lbSkill = lb3Tabl[actTurn.char.aspiration]
                                            elif LBBars[actTurn.team][1]//3 == 4:
                                                lbSkill = lb4
                                            
                                            lbPrio = LBBars[actTurn.team][1]//3 == LBBars[actTurn.team][0]
                                            if lbSkill.type == TYPE_DAMAGE and lbPrio:
                                                ennemiTabl = actTurn.cell.getEntityOnArea(area=lbSkill.range,team=actTurn.team,wanted=ENEMIES,fromCell=actTurn.cell,lineOfSight = True,ignoreInvoc = True)
                                                ennemiTabl.sort(key=lambda ballerine: actTurn.getAggroValue(ballerine),reverse=True)

                                                if lbSkill.area == AREA_MONO:
                                                    ennemiNb = 0
                                                    for ent in tablEntTeam[not(actTurn.team)]:
                                                        if type(ent.char) not in [invoc, depl] and ent.hp > 0:
                                                            ennemiNb += 1
                                                    if ennemiNb <= 2:
                                                        atkSkill.append(lbSkill)
                                                        atkSkill.append(lbSkill)
                                                elif len(ennemiTabl) > 0 and (not dictIsNpcVar["The Giant Enemy Spider"] and not dictIsNpcVar["[[Spamton Neo](https://deltarune.fandom.com/wiki/Spamton)]"]):
                                                    if len(ennemiTabl[0].cell.getEntityOnArea(area=lbSkill.area,team=actTurn.team,wanted=ENEMIES,fromCell=actTurn.cell,ignoreInvoc = True)) >= [2,3][lbSkill.area==lb1AoE.area]:
                                                        atkSkill.append(lbSkill)
                                                        atkSkill.append(lbSkill)
                                                elif dictIsNpcVar["The Giant Enemy Spider"] or dictIsNpcVar["[[Spamton Neo](https://deltarune.fandom.com/wiki/Spamton)]"]:
                                                    atkSkill.append(lbSkill)
                                                    if lbSkill.area==lb1AoE.area:
                                                        atkSkill.append(lbSkill)
                                                        atkSkill.append(lbSkill)

                                            elif lbSkill.type == TYPE_HEAL:
                                                aliveAlliesHp, aliveAlliesMaxHp, rezableAllies = 0, 0,0
                                                for ent in tablEntTeam[actTurn.team]:
                                                    if type(ent.char) not in [invoc, depl] and ent.hp > 0:
                                                        aliveAlliesHp += ent.hp
                                                        aliveAlliesMaxHp += ent.maxHp
                                                    elif ent.hp <= 0 and ent.status == STATUS_DEAD:
                                                        rezableAllies += 1
                                                hpRatio = aliveAlliesHp/aliveAlliesMaxHp

                                                if hpRatio <= 0.25:
                                                    probaHealSkill[choisenIA] = probaHealSkill[choisenIA] * 1.2
                                                    healSkill.append(lbSkill)
                                                if hpRatio <= 0.15:
                                                    probaHealSkill[choisenIA] = probaHealSkill[choisenIA] * 1.2
                                                    healSkill.append(lbSkill)

                                                if LBBars[actTurn.team][1]//3 >= 2 and rezableAllies >=3 :
                                                    probaHealSkill[choisenIA] = probaHealSkill[choisenIA] * 1.2
                                                    healSkill.append(lbSkill)
                                                    healSkill.append(lbSkill)
                                            elif lbSkill.type == TYPE_ARMOR and ennemiCast:
                                                armorSkill.append(lbSkill)
                                            elif lbSkill.type == TYPE_BOOST:
                                                alliesCastingDpsSkill = 0
                                                for ent in tablEntTeam[actTurn.team]:
                                                    for eff in ent.effects:
                                                        if eff.effects.replica != None and (findSkill(eff.effects.replica).effectOnSelf == None or findEffect(findSkill(eff.effects.replica).effectOnSelf).replica == None) and findSkill(eff.effects.replica).type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]:
                                                            alliesCastingDpsSkill += 1
                                                            break
                                                if 6 - LBBars[actTurn.team][1]//3 <= alliesCastingDpsSkill:
                                                    boostSkill.append(lbSkill)
                                                    boostSkill.append(lbSkill)
                                        isTMinDanger = False
                                        for a in tablEntTeam[actTurn.team]:
                                            if a.hp / a.maxHp <= 0.35:
                                                isTMinDanger = True
                                                break

                                        if not(isTMinDanger):
                                            probaIndirectReaSkill = [0,0,0,0,0,0,0,0]
                                        else:
                                            probaHealSkill = [30,120,40,50,150,150,150,150,150]

                                        if actTurn.specialVars["summonerMalus"]:
                                            probaAtkWeap = probaHealWeap = probaReaSkill = probaIndirectReaSkill = probaAtkSkill = probaIndirectAtkSkill = probaHealSkill = probaBoost = probaMalus = probaArmor = [0,0,0,0,0,0,0,0] 

                                        probTabl, analyse = [probaReaSkill,probaIndirectReaSkill,probaAtkSkill,probaIndirectAtkSkill,probaHealSkill,probaBoost,probaMalus,probaArmor,probaDepl], [reaSkill,indirectReaSkill,atkSkill,indirectAtkSkill,healSkill,boostSkill,malusSkill,armorSkill,deplSkills]
                                        for cmpt in range(len(probTabl)):
                                            if len(analyse[cmpt]) == 0:
                                                probTabl[cmpt][choisenIA] = 0
                                            if actTurn.isNpc("Akira H.") and cmpt == 3:
                                                logs += "\n" + str(analyse[cmpt])

                                        if len(invocSkill) == 0 or tablAliveInvoc[actTurn.team]>=3:
                                            probaInvoc[choisenIA] = 0

                                        totalProba = probaAtkWeap[choisenIA]+probaHealWeap[choisenIA]+probaInvoc[choisenIA]

                                        for cmpt in range(len(probTabl)):
                                            totalProba += probTabl[cmpt][choisenIA]

                                        nbIte, optionChoice = 0, OPTION_WEAPON
                                        atRange = actTurn.atRange()
                                        nbTargetAtRange = len(atRange)

                                        if not(actTurn.char.weapon.name.lower() == "noneweap" or actTurn.char.weapon.id.lower() == "noneweap" or (actTurn.char.weapon.id in cannotUseMainWeapon and len(actTurn.atRange()) > 0)):
                                            if actTurn.char.weapon.target == ENEMIES:
                                                if nbTargetAtRange > 0:
                                                    atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
                                                    optionChoice,ennemi = OPTION_WEAPON,atRange[0]

                                                else:
                                                    optionChoice,choiceToMove = OPTION_MOVE, actTurn.getCellToMove()
                                                    if choiceToMove == None:
                                                        optionChoice=OPTION_SKIP

                                            else:
                                                if nbTargetAtRange > 0:
                                                    optionChoice,ennemi = OPTION_WEAPON,getHealTarget(actTurn,atRange,actTurn.char.weapon)
                                                else:
                                                    optionChoice,choiceToMove = OPTION_MOVE, actTurn.getCellToMove()
                                                    if choiceToMove == None:
                                                        optionChoice=OPTION_SKIP
                                        else:
                                            optionChoice,choiceToMove = OPTION_MOVE, actTurn.getCellToMove()
                                            if choiceToMove == None:
                                                optionChoice=OPTION_SKIP
                                        subWeapon = 0
                                        while nbIte <= 2:
                                            totalProba -= subWeapon
                                            try:
                                                probaRoll = random.randint(0,totalProba)
                                            except:
                                                probaRoll = 0
                                            logs += "\nTotal Proba : {0} - ProbaRoll : {1}".format(totalProba,probaRoll)

                                            optionChoisen = False

                                            if probaRoll <= probaAtkWeap[choisenIA] and probaAtkWeap[choisenIA] > 0: #Attaque à l'arme
                                                logs += "\nSelected option : Damage with weapon\nTargets at range : {0}\n".format(nbTargetAtRange)
                                                if optionChoice == OPTION_MOVE:          
                                                    for cmpt in range(len(actTurn.char.skills)):
                                                        if type(actTurn.char.skills[cmpt]) == skill and actTurn.cooldowns[cmpt] == 0 and actTurn.char.skills[cmpt].tpCac == True:
                                                            atRange2 = actTurn.cell.getEntityOnArea(area=actTurn.char.skills[cmpt].range,fromCell=actTurn.cell,team=actTurn.team,wanted=ENEMIES,lineOfSight=True)
                                                            if len(atRange2)>0:
                                                                try:
                                                                    atRange2.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
                                                                    optionChoice = OPTION_SKILL
                                                                    skillToUse = actTurn.char.skills[cmpt]
                                                                    ennemi = atRange2[0]
                                                                    compromis = True
                                                                except:
                                                                    pass
                                                                break
                                                if optionChoice != OPTION_SKIP:
                                                    optionChoisen = True
                                                else:
                                                    logs += "\nSkipping ? No, try again"
                                                    if probaRoll - probaAtkWeap[choisenIA] > 0:
                                                        subWeapon = probaAtkWeap[choisenIA]
                                            else:
                                                probaRoll -= probaAtkWeap[choisenIA]

                                            if probaRoll <= probaHealWeap[choisenIA] and probaHealWeap[choisenIA] > 0 and not(optionChoisen): #Soins à l'arme
                                                logs += "\nSelected option : Heal with weapon"
                                                optionChoisen = True
                                            elif not(optionChoisen):
                                                probaRoll -= probaHealWeap[choisenIA]

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

                                            if probaRoll <= probaReaSkill[choisenIA] and probaReaSkill[choisenIA] > 0 and not(optionChoisen): # Résurection
                                                logs += "\nSelected option : Resurection Skill"
                                                if len(reaSkill) > 1:
                                                    skillToUse = reaSkill[random.randint(0,len(reaSkill)-1)]
                                                else:
                                                    skillToUse = reaSkill[0]

                                                if skillToUse.range != AREA_MONO:
                                                    atRangeRaise = actTurn.cell.getEntityOnArea(area=skillToUse.range,team=actTurn.team,wanted=ALLIES,effect=skillToUse.effects,fromCell=actTurn.cell,directTarget=True,lifeUnderPurcentage=99,dead=True)
                                                    atRangeRaise.sort(key=lambda ballerine : getRaiseAggro(actTurn,ballerine))

                                                    if len(atRangeRaise) < 1:
                                                        print("No target at range ? Wtf ?")
                                                    else:
                                                        optionChoice = OPTION_SKILL
                                                        optionChoisen=True
                                                        ennemi = atRangeRaise[0]
                                                else:
                                                    ennemi = actTurn
                                                    optionChoice = OPTION_SKILL
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
                                                    atRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,fromCell=actTurn.cell,team=actTurn.team,wanted=ENEMIES,lineOfSight = True,effect=randomSkill.effects,ignoreInvoc = (randomSkill.effectOnSelf == None or (randomSkill.effectOnSelf != None and findEffect(randomSkill.effectOnSelf).replica != None)))
                                                    atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)

                                                    if len(atRange) > 0:
                                                        optionChoice = OPTION_SKILL
                                                        skillToUse = randomSkill
                                                        ennemi = atRange[0]

                                                else:
                                                    optionChoice = OPTION_SKILL
                                                    skillToUse = randomSkill
                                                    ennemi = actTurn

                                                optionChoisen=True
                                            elif not(optionChoisen):
                                                probaRoll -= probTabl[2][choisenIA]

                                            if probaRoll <= probTabl[3][choisenIA] and probTabl[3][choisenIA] > 0 and not(optionChoisen) and indirectAtkSkill != []: # Dégâts indirects
                                                logs += "\nSelected option : Indirect damage skill"
                                                finded = True
                                                while 1:
                                                    if len(indirectAtkSkill) > 1:
                                                        randomSkill = indirectAtkSkill[random.randint(0,len(indirectAtkSkill)-1)]
                                                    elif len(indirectAtkSkill) == 0:
                                                        randomSkill = indirectAtkSkill[0]
                                                    else:
                                                        logs += "\n"+str(indirectAtkSkill)
                                                        finded = False
                                                        break

                                                    atRange = actTurn.cell.getEntityOnArea(area=[randomSkill.range,randomSkill.area][randomSkill.range == AREA_MONO],team=actTurn.team,fromCell=actTurn.cell,wanted=ENEMIES,lineOfSight=randomSkill.range != AREA_MONO)
                                                    if len(atRange) > 0:
                                                        break
                                                    else:
                                                        logs += "\nNo target at range finded w/ {0}, retrying...".format(randomSkill.name)
                                                        indirectAtkSkill.remove(randomSkill)

                                                if finded:
                                                    if randomSkill.range != AREA_MONO:
                                                        atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
                                                        optionChoice, skillToUse, ennemi = OPTION_SKILL, randomSkill, atRange[0]
                                                    else:
                                                        optionChoice, skillToUse, ennemi = OPTION_SKILL, randomSkill, actTurn

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
                                                        tablAtRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,fromCell=actTurn.cell,wanted=ALLIES,lifeUnderPurcentage=90,effect=randomSkill.effects)
                                                    else:
                                                        tablAtRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,fromCell=actTurn.cell,wanted=ALLIES,lifeUnderPurcentage=90,effect=randomSkill.effects,ignoreAspiration=[ALTRUISTE,PROTECTEUR,PREVOYANT,IDOLE])
                                            
                                                    if len(tablAtRange) > 0:
                                                        optionChoice = OPTION_SKILL
                                                        skillToUse = randomSkill
                                                        ennemi = getHealTarget(actTurn,tablAtRange,skillToUse)

                                                else:
                                                    if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,wanted=ALLIES,fromCell=actTurn.cell,effect=randomSkill.effects,directTarget=False)) > 0 or (randomSkill == trans and actTurn.char.aspiration in [ALTRUISTE,IDOLE]):
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
                                                    atRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,effect=randomSkill.effects,ignoreInvoc = True)
                                                    atRange.sort(key=lambda ballerine:getBuffAggro(actTurn,ballerine,findEffect(randomSkill.effects[0])))
                                                    optionChoice = OPTION_SKILL
                                                    skillToUse = randomSkill
                                                    ennemi = atRange[0]

                                                else:
                                                    if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,effect=randomSkill.effects,directTarget=False)) > 0:
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
                                                    atRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,fromCell=actTurn.cell,team=actTurn.team,wanted=ENEMIES,lineOfSight = True,effect=randomSkill.effects,ignoreInvoc = (randomSkill.effectOnSelf == None or (randomSkill.effectOnSelf != None and findEffect(randomSkill.effectOnSelf).replica != None)))
                                                    atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)

                                                    optionChoice = OPTION_SKILL
                                                    skillToUse = randomSkill
                                                    try:
                                                        ennemi = atRange[0]
                                                    except:
                                                        logs += "\nError : No valid target find"
                                                        optionChoice = OPTION_SKIP

                                                else:
                                                    if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,fromCell=actTurn.cell,wanted=ENEMIES,effect=randomSkill.effects,directTarget=False)) > 0:
                                                        optionChoice = OPTION_SKILL
                                                        skillToUse = randomSkill
                                                        ennemi = actTurn

                                                optionChoisen=True
                                            elif not(optionChoisen):
                                                probaRoll -= probTabl[6][choisenIA]

                                            if probaRoll <= probTabl[7][choisenIA] and probTabl[7][choisenIA] > 0 and not(optionChoisen): # Armure
                                                logs += "\nSelected option : Armor skill"
                                                if len(armorSkill) > 1:
                                                    randomSkill = findSkill(armorSkill[random.randint(0,len(armorSkill)-1)])
                                                else:
                                                    randomSkill = findSkill(armorSkill[0])

                                                if randomSkill.range != AREA_MONO:
                                                    if randomSkill.id != convert.id:
                                                        tablAtRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,effect=randomSkill.effects)
                                                    else:
                                                        tablAtRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ALLIES,fromCell=actTurn.cell,effect=randomSkill.effects,ignoreAspiration=[ALTRUISTE,PREVOYANT,PROTECTEUR,IDOLE])
                                                    
                                                    tablAtRange.sort(key=lambda fepacho: getHealAggro(actTurn, fepacho, randomSkill, armor=True))

                                                    optionChoice = OPTION_SKILL
                                                    skillToUse = randomSkill
                                                    ennemi = tablAtRange[0]

                                                else:
                                                    if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,fromCell=actTurn.cell,wanted=ALLIES,effect=randomSkill.effects,directTarget=False)) > 0:
                                                        optionChoice = OPTION_SKILL
                                                        skillToUse = randomSkill
                                                        ennemi = actTurn
                                                
                                                optionChoisen = True
                                            elif not(optionChoisen):
                                                probaRoll -= probTabl[7][choisenIA]

                                            if probaRoll <= probaDepl[choisenIA] and probaDepl[choisenIA] > 0 and not(optionChoisen): # Déployable
                                                logs += "\nSelected option : Depl skill"
                                                if len(deplSkills) > 1:
                                                    randomSkill = deplSkills[random.randint(0,len(deplSkills)-1)]
                                                else:
                                                    randomSkill = deplSkills[0]

                                                optionChoice = OPTION_SKILL
                                                skillToUse = randomSkill
                                                optionChoisen = True

                                                if randomSkill.range == AREA_MONO:
                                                    ennemi = actTurn.cell
                                                else:
                                                    tablCells = actTurn.cell.getArea(area=randomSkill.range,team=actTurn.team,fromCell=actTurn.cell)
                                                    for celly in tablCells[:]:
                                                        if celly.depl != None:
                                                            tablCells.remove(celly)
                                                    tablCells.sort(key=lambda ballerine: len(ballerine.getEntityOnArea(area=randomSkill.depl.skills.area,team=actTurn.team,wanted=[ALLIES,ENEMIES][randomSkill.depl.skills.type in hostilesTypes], ignoreInvoc = True, directTarget=False, fromCell= ballerine))+0.5-(ballerine.distance(actTurn.cell)*0.1),reverse=True)
                                                    ennemi = tablCells[0]

                                            elif not(optionChoisen):
                                                probaRoll -= probaDepl[choisenIA]

                                            if probaRoll == -1 and probaAtkWeap[choisenIA] == probaHealWeap[choisenIA] == 0 and actTurn.char.weapon.emoji != '<:noneWeap:917311409585537075>' and not(optionChoisen):     # Can't use anything
                                                logs += "\nNo target at range. Trying to move"
                                                optionChoice,choiceToMove = OPTION_MOVE, actTurn.getCellToMove()
                                                optionChoisen = True

                                                if choiceToMove == None:
                                                    optionChoice = OPTION_SKIP
                                                    logs += "\nNo valid cells found. Skipping the turn"

                                            if not(optionChoisen):
                                                nbIte += 1
                                            else:
                                                break
                            # ==========================================
                            else:
                                logs += "\nReplica found"
                                skilly = findSkill(onReplica.effects.replica)
                                if onReplica.replicaTarget.hp > 0:
                                    optionChoice = OPTION_SKILL
                                    skillToUse = skilly
                                    ennemi = onReplica.replicaTarget
                                else:
                                    logs += "\nInitial target down, taking another target at range"
                                    skilly = copy.deepcopy(skilly)
                                    skilly.power = int(skilly.power * (0.7-0.2*int(skilly.area != AREA_MONO)))
                                    skilly.name = skilly.name + " 0.5"
                                    skilly.effPowerPurcent = [100, skilly.effPowerPurcent][skilly.effPowerPurcent != None] * (0.7-0.2*int(skilly.area != AREA_MONO))

                                    atRange = actTurn.cell.getEntityOnArea(area=skilly.range,fromCell=actTurn.cell,team=actTurn.team,wanted=ENEMIES,lineOfSight=True,effect=skilly.effects,ignoreInvoc = True)

                                    if len(atRange) <= 0:
                                        atRange = actTurn.cell.getEntityOnArea(area=AREA_CIRCLE_7,team=actTurn.team,fromCell=actTurn.cell,wanted=ENEMIES,lineOfSight=True,ignoreInvoc = True)
                                        logs += "\nNo fucking target at range. The ennemi in line of sight with the more aggro will be targeted, but the power will be cut again"
                                        skilly.power = int(skilly.power*0.7)
                                        skilly.effPowerPurcent = skilly.effPowerPurcent * 0.7
                                    
                                    if len(atRange) > 0:
                                        atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)

                                        optionChoice = OPTION_SKILL
                                        skillToUse = skilly
                                        ennemi = atRange[0]
                                    else:
                                        optionChoice = OPTION_SKIP

                            lunaUsedQuickFight, lunaQFEff = "", None

                            if not(actTurn.char.canMove) and optionChoice == OPTION_MOVE:
                                optionChoice = OPTION_SKIP

                            if optionChoice == OPTION_WEAPON: #Option : Weapon
                                for eff in actTurn.effects:
                                    if eff.effects.id == lunaQuickFightEff.id:
                                        lunaQFEff = eff
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

                                        funnyTempVarName, deathCount = actTurn.attack(target=ennemi,value=power,icon=actTurn.char.weapon.emoji,area=actTurn.char.weapon.area,use=actTurn.char.weapon.use,onArmor=actTurn.char.weapon.onArmor,effectOnHit=actTurn.char.weapon.effectOnUse)
                                        logs+= funnyTempVarName
                                        tempTurnMsg += funnyTempVarName
                                        cmpt += 1

                                        if actTurn.char.weapon.id == flyfishweap.id:
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
                                                funnyTempVarName = add_effect(actTurn,ennemi2,findEffect(actTurn.char.weapon.effectOnUse),skillIcon=flyfishweap.emoji,effPowerPurcent=70)
                                                
                                                logs+= funnyTempVarName
                                                tempTurnMsg += funnyTempVarName
                                                ennemi2.refreshEffects()

                                    if actTurn.char.weapon.power > 0 and actTurn.specialVars["damageSlot"] != None:
                                        loose = int(actTurn.maxHp * (15/100))
                                        tempTurnMsg += "{0} : -{1} PV ({2})\n".format(actTurn.icon,loose,actTurn.specialVars["damageSlot"].effects.name)
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

                                    for a in ennemi.cell.getEntityOnArea(area=actTurn.char.weapon.area,team=actTurn.team,fromCell=actTurn.cell,wanted=ALLIES,directTarget=False):
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
                                            funnyTempVarName, useless = actTurn.heal(tempTabl[0], actTurn.char.weapon.effects.emoji[0][0], actTurn.char.weapon.use, actTurn.char.weapon.effects.power, danger=danger, effName = actTurn.char.weapon.effects.name, mono=actTurn.char.weapon.area == AREA_MONO)
                                            tempTurnMsg += funnyTempVarName
                                            logs += funnyTempVarName

                                        else:
                                            funnyTempVarName = add_effect(actTurn,tempTabl[0],findEffect(actTurn.char.weapon.effects.callOnTrigger),danger=danger,start=actTurn.char.weapon.effects.name,skillIcon = actTurn.weapon.effects.emoji[0][0])
                                            logs+= funnyTempVarName
                                            tempTurnMsg += funnyTempVarName
                                            tempTabl[0].refreshEffects()

                                elif actTurn.char.weapon.id == fleau.id:
                                    tablName = []
                                    for ent in actTurn.cell.getEntityOnArea(area=actTurn.char.weapon.effects.area,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,directTarget=False):
                                        eff = actTurn.char.weapon.effects.callOnTrigger
                                        ballerine = add_effect(actTurn,ent,eff,danger=danger)
                                        if '🚫' not in ballerine and ballerine != "":
                                            tablName.append(ent.icon)
                                            ent.refreshEffects()

                                    if tablName != []:
                                        temp = "{0} {1} → ".format(actTurn.icon,actTurn.weapon.effects.emoji[0][0])
                                        for cmpt in tablName:
                                            temp += cmpt

                                        tempTurnMsg += temp + " +{0} __{1}__\n".format(actTurn.weapon.effects.emoji[0][0],actTurn.weapon.effects.name)
                                        logs += temp

                                elif actTurn.char.weapon.id in [micPurple.id,micRed.id,micPink.id]:
                                    tablName, eff = [], actTurn.weapon.effects.callOnTrigger
                                    for ent in actTurn.cell.getEntityOnArea(area=actTurn.weapon.effects.area,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,directTarget=False):
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

                                if actTurn.specialVars["convicVigil"] != None:
                                    ballerine = actTurn.specialVars["convicVigil"].triggerStartOfTurn(danger,decate=True)
                                    logs += ballerine
                                    tempTurnMsg += ballerine
                                elif actTurn.specialVars["convicPro"] != None:
                                    ballerine = actTurn.specialVars["convicPro"].triggerStartOfTurn(danger,decate=True)
                                    logs += ballerine
                                    tempTurnMsg += ballerine
                            elif optionChoice == OPTION_MOVE: #Option : Déplacement
                                logs += "\n{0} is moving".format(actTurn.char.name)
                                temp = actTurn.cell
                                actTurn.move(cellToMove=choiceToMove)
                                logs += "\n{0} have been moved from {1}:{2} to {3}:{4}".format(actTurn.char.name,temp.x,temp.y,choiceToMove.x,choiceToMove.y)
                                tempTurnMsg+= "\n"+actTurn.char.name+" se déplace\n"
                            elif optionChoice == OPTION_SKIP: #Passage de tour
                                logs += "\n{0} is skipping their turn".format(actTurn.char.name)
                                tempTurnMsg += f"\n{actTurn.char.name} passe son tour\n"
                                actTurn.stats.turnSkipped += 1
                            elif optionChoice == OPTION_SKILL: #Skill
                                qCast, needRefresh, useEffElem = False, False, 0

                                if skillToUse.id == finFloLaunchBase.id:
                                    skillToUse, listEff, allReadySeen, golden = copy.deepcopy(finFloLaunchBase), [], [], 0
                                    for eff in actTurn.effects:
                                        if eff.effects.id in tablRosesId and eff.effects.id not in allReadySeen:
                                            if eff.effects.id == roseRed.id:
                                                listEff.append(finFloEffList[0])
                                            elif eff.effects.id == roseDarkBlu.id:
                                                listEff.append(finFloEffList[1])
                                            elif eff.effects.id == roseBlue.id:
                                                listEff.append(finFloEffList[2])
                                            elif eff.effects.id == roseGreen.id:
                                                skillToUse.effectOnSelf = finFloEffList[3]
                                            elif eff.effects.id == roseYellow.id:
                                                golden = 2
                                            elif eff.effects.id == rosePink.id:
                                                golden = 1
                                            eff.decate(value=99)
                                            allReadySeen.append(eff.effects.id)
                                    actTurn.refreshEffects()

                                    if golden == 1:
                                        for eff in listEff:
                                            eff.turnInit += 1
                                    elif golden == 2:
                                        skillToUse.effPowerPurcent = 130

                                    if listEff != []:
                                        skillToUse.effects = listEff
                                elif skillToUse.id == horoscope.id:
                                    skillToUse, horoEff, tablStats = copy.deepcopy(horoscope), classes.effect("Horoscope","horoscope",INTELLIGENCE,turnInit=3,emoji=sameSpeciesEmoji('<:horoscope:960312586371477524>','<:horoscope:960312676469321838>')), [0,0,0,0,0,0,0]
                                    for eff in actTurn.effects:
                                        for effy in horoscopeEff:
                                            if eff.effects.id == effy[0].id:
                                                for staty in effy[1]:
                                                    tablStats[staty[0]] += staty[1]
                                                eff.decate(value=99)
                                    needRefresh = True
                                    horoEff.strength, horoEff.endurance, horoEff.charisma, horoEff.agility, horoEff.precision, horoEff.intelligence, horoEff.magie = tuple(tablStats)
                                    bestStat = [[0,horoEff.strength],[1, horoEff.endurance],[2, horoEff.charisma],[3, horoEff.agility],[4, horoEff.precision],[5, horoEff.intelligence],[6, horoEff.magie]]
                                    bestStat.sort(key=lambda astralSign: astralSign[1],reverse=True)
                                    horoEff.name += " " + hroscopeNickNames[bestStat[0][0]]
                                    skillToUse.effects = [horoEff]

                                for eff in actTurn.effects:
                                    if eff.effects.id == quickCastEff.id:
                                        qCast = True
                                    elif eff.effects.id == lunaQuickFightEff.id:
                                        lunaQFEff = eff
                                    elif skillToUse.id in useElemEffId+elemArrowId+elemRuneId and eff.effects.id in [tablElemEff[actTurn.char.element].id,tablElemEff[ELEMENT_UNIVERSALIS_PREMO].id]:
                                        eff.decate(turn=99)
                                        useEffElem += 1
                                        needRefresh = True
                                if needRefresh:
                                    actTurn.refreshEffects()

                                if skillToUse.id in useElemEffId+elemArrowId+elemRuneId:
                                    skillToUse = copy.deepcopy(skillToUse)
                                    skillToUse.name = skillToUse.name + " +{0}".format(useEffElem)

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
                                        for eff in actTurn.effects:
                                            if needed.id == eff.effects.id:
                                                eff.decate(turn=99)
                                                break
                                    actTurn.refreshEffects()

                                try:
                                    logs += "\n\n{0} is using {1} on {2}\n".format(actTurn.char.name,skillToUse.name,ennemi.char.name)
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
                                if actTurn.char.says.ultimate != None and skillToUse.ultimate and not(skillToUse.effectOnSelf != None and findEffect(skillToUse.effectOnSelf).replica != None and skillToUse.power == 0 and skillToUse.effects == [None]):
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
                                        if skillToUse.id == "lb":
                                            LBBars[actTurn.team][1] = 0

                                # Share cooldown
                                if skillToUse.shareCooldown:
                                    for a in tablEntTeam[actTurn.team]:
                                        if a.char.team == actTurn.char.team:
                                            for b in range(0,len(a.char.skills)):
                                                if type(a.char.skills[b]) == skill:
                                                    if a.char.skills[b].id == skillToUse.id:
                                                        a.cooldowns[b] = skillToUse.cooldown

                                # Mors Vita Est set share cooldown
                                # tpCac
                                if skillToUse.tpCac and type(ennemi) == entity and actTurn.cell.distance(ennemi.cell) > 1:
                                    surrond = ennemi.cell.surrondings()
                                    for a in surrond[:]:
                                        if a == None or (a != None and a.on != None):
                                            surrond.remove(a)

                                    if len(surrond) > 0:
                                        surrond.sort(key=lambda celly:actTurn.cell.distance(celly))
                                        actTurn.move(cellToMove=surrond[0])
                                        tempTurnMsg += "__{0}__ se téléporte au corps à corps de __{1}__\n".format(actTurn.name,ennemi.name)

                                    else:
                                        tempTurnMsg += "__{0}__ essaye de se téléporte au corps à corps de __{1}__, mais cela échoue\n".format(actTurn.name,ennemi.name)
                                        stat,damageBase = -100,20

                                        for stats in actTurn.allStats():
                                            stat = max(stats,stat)

                                        damage = damageBase * (1+(stat/100)) * (1-(min(95,actTurn.resistance*(1-actTurn.percing/100))/100)) * actTurn.getElementalBonus(actTurn,AREA_MONO,TYPE_INDIRECT_DAMAGE) * (1+(0.01*actTurn.level))
                                        temp = actTurn.indirectAttack(actTurn,value=damage,name="Fissure spacio-temporelle")
                                        tempTurnMsg += temp
                                        logs += temp

                                    if skillToUse.areaOnSelf:
                                        ennemi = actTurn

                                # Luna and Iliana Head to Head
                                if skillToUse.id == lunaSpe.id:
                                    if not(ennemi.isNpc("Luna prê.") or ennemi.isNpc("Clémence Exaltée")):
                                        if actTurn.specialVars["clemBloodJauge"] == None:
                                            actTurn.specialVars["clemBloodJauge"] = 0

                                            cellToCheck, actCell = findCell(actTurn.cell.x+1,actTurn.cell.y,tablAllCells), actTurn.cell
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
                                        for fightEff in actTurn.effects:
                                            if fightEff.effects.id == lunaInfiniteDarknessShield.id:
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

                                            for fightEff in actTurn.effects:
                                                if fightEff.effects.id == lunaInfiniteDarknessShield.id:
                                                    fightEff.decate(value=99999999999999999999)
                                                    actTurn.refreshEffects()
                                                    actTurn.specialVars["clemBloodJauge"] = None
                                                    break
                                    
                                    else:
                                        funnyTempVarName, temp = actTurn.attack(target=ennemi,value=skillToUse.power*1.5,icon=skillToUse.emoji,area=skillToUse.area,sussess=500,use=skillToUse.use,onArmor=skillToUse.onArmor,useActionStats=actionStats,setAoEDamage=skillToUse.setAoEDamage,lifeSteal = skillToUse.lifeSteal,erosion = skillToUse.erosion, skillPercing = skillToUse.percing, execution=skillToUse.execution)
                                        tempTurnMsg += funnyTempVarName
                                        logs += "\n"+funnyTempVarName
                                        deathCount += temp

                                elif skillToUse.id == plumRem.id:
                                    for ent in ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENEMIES,ignoreInvoc = True, directTarget=False,fromCell=actTurn.cell):
                                        nbPlume = 0
                                        for eff in ent.effects:
                                            if eff.effects.id == plumRemEff.id:
                                                temp, temp2 = actTurn.attack(target=ent,value = eff.effects.power,icon = eff.icon ,area=AREA_MONO,sussess=200)
                                                logs += temp
                                                tempTurnMsg += temp
                                                eff.decate(turn=99)
                                                nbPlume += 1
                                        if nbPlume == 0:
                                            tempTurnMsg += "Cela n'affecte pas {0}\n".format(ent.name)
                                        else:
                                            ent.refreshEffects()
                                
                                elif skillToUse.id == akikiSkill3_2_1.id:
                                    for ent in ennemi.cell.getEntityOnArea(area=AREA_ALL_ENEMIES, team=actTurn.team, wanted=ENEMIES, ignoreInvoc= True, directTarget=False, fromCell=actTurn.cell):
                                        for eff in ent.effects:
                                            if eff.effects.id == akikiSkill3_2_mark.id:
                                                temp, temp2 = actTurn.attack(target=ent,value = skillToUse.power,icon = skillToUse.emoji,area=skillToUse.area,sussess=skillToUse.success)
                                                eff.decate(turn=99)
                                                akikidenfensedown = copy.deepcopy(vulne)
                                                akikidenfensedown.power = 15
                                                temp += groupAddEffect(caster=actTurn, target=ent, area=ent.cell.getEntityOnArea(area=skillToUse.area, team=actTurn.team, wanted=ENEMIES, ignoreInvoc = True, directTarget=False, fromCell=actTurn.cell),effect=[akikidenfensedown],skillIcon=skillToUse.emoji)
                                                logs += temp
                                                tempTurnMsg += temp
                                        ent.refreshEffects()
                                    
                                elif skillToUse.id == chaos.id:
                                    for team in [0,1]:
                                        for ent in tablEntTeam[team]:
                                            if ent.hp > 0 and type(ent.char) not in [invoc, depl]:
                                                if random.randint(0,1):
                                                    eff = copy.deepcopy(dmgUp)
                                                else:
                                                    eff = copy.deepcopy(dmgDown)
                                                eff.power, eff.turnInit = random.randint(5,20), random.randint(0,3)
                                                eff.name = eff.name + " ({0}%)".format(eff.power)
                                                ballerine = add_effect(actTurn, ent, eff, skillIcon=skillToUse.emoji)
                                                tempTurnMsg += ballerine
                                                logs += ballerine

                                # ======================== Any other skill ========================
                                else:
                                    if skillToUse.effectOnSelf != None and skillToUse.effBeforePow:
                                        effect = findEffect(skillToUse.effectOnSelf)
                                        tempTurnMsg = [tempTurnMsg[:-1],tempTurnMsg][skillToUse.type != TYPE_HEAL] + add_effect(actTurn,actTurn,effect,effPowerPurcent=skillToUse.effPowerPurcent,skillIcon = skillToUse.emoji)
                                        logs += "\n{0} gave the {1} effect at {2} for {3} turn(s)".format(actTurn.char.name,effect.name,ennemi.char.name,effect.turnInit)
                                    actionStats = skillToUse.useActionStats
                                    if skillToUse.id == trans.id:
                                        actionStats, entActStats = 0, actTurn.actionStats()
                                        for cmpt in (0,1,2,3,4):
                                            if entActStats[cmpt] > entActStats[actionStats]:
                                                skillToUse.useActionStats = cmpt
                                        actTurn.stats.nbLB += 1
                                    
                                    if skillToUse.type in [TYPE_BOOST,TYPE_ARMOR,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ] and skillToUse.effects != [None]:
                                        if skillToUse.id != clemUltCast.id:
                                            if skillToUse.id == bolide.id:
                                                tempTurnMsg += "{0} {1} → {0} -{2} PV\n".format(actTurn.icon,skillToUse.emoji,actTurn.hp -1)
                                                actTurn.stats.selfBurn += actTurn.hp -1
                                                actTurn.hp = 1
                                            if skillToUse.jaugeEff != None:
                                                skillToUse = copy.deepcopy(skillToUse)
                                                try:
                                                    if teamJaugeDict[actTurn.team][actTurn].effects.id == skillToUse.jaugeEff.id:
                                                        jaugeConsumed = [teamJaugeDict[actTurn.team][actTurn].value,skillToUse.maxJaugeValue][skillToUse.maxJaugeValue<teamJaugeDict[actTurn.team][actTurn].value]
                                                        teamJaugeDict[actTurn.team][actTurn].value -= jaugeConsumed
                                                        if skillToUse.maxJaugeValue != skillToUse.minJaugeValue and skillToUse.maxJaugeValue != 0:
                                                            skillToUse.effPowerPurcent = (skillToUse.effPowerPurcent//2) + (skillToUse.effPowerPurcent//2)*(jaugeConsumed/(skillToUse.maxJaugeValue-skillToUse.minJaugeValue))
                                                    else:
                                                        jaugeConsumed = 0

                                                except KeyError:
                                                    logs += "\n{0} hasn't any jauge eff"
                                                    jaugeConsumed = 0
                                                except KeyError:
                                                    logs += "\n{0} hasn't any jauge eff"
                                        
                                            ballerine = groupAddEffect(caster=actTurn, target=ennemi, area=skillToUse.area, effect=skillToUse.effects, skillIcon=skillToUse.emoji, actionStats=skillToUse.useActionStats, effPurcent = skillToUse.effPowerPurcent)
                                            tempTurnMsg += ballerine
                                            logs += ballerine

                                            if skillToUse.type == TYPE_BOOST and skillToUse.range == AREA_MONO and actTurn.specialVars["partner"] != None and actTurn.specialVars["partner"].hp > 0:
                                                initArea = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES,directTarget=False)
                                                secondArea = actTurn.specialVars["partner"].cell.getEntityOnArea(area=skillToUse.area,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,directTarget=False)

                                                for ent in secondArea[:]:
                                                    if ent in initArea or ent == actTurn:
                                                        secondArea.remove(ent)

                                                if len(secondArea) > 0:
                                                    effPower = [skillToUse.effPowerPurcent,100][skillToUse.effPowerPurcent == None]
                                                    ballerine = groupAddEffect(caster=actTurn, target=actTurn.specialVars["partner"], area=secondArea, effect=skillToUse.effects, skillIcon=partner.emoji, actionStats=skillToUse.useActionStats, effPurcent = [effPower * partnerIn.power * 0.01,effPower][findEffect(skillToUse.effects[0]).id == tangoEndEff.id])
                                                    tempTurnMsg += ballerine
                                                    logs += ballerine

                                        else:
                                            effect = skillToUse.effects[0]
                                            tempVal, clemShieldBefore = max(actTurn.specialVars["clemBloodJauge"].value-1,30), actTurn.stats.shieldGived
                                            effect.overhealth = tempVal * 2
                                            tempTurnMsg += add_effect(actTurn,actTurn,effect,danger=danger)
                                            logs += "\nClemClem gave herself her ult shield with {2} PAr (base power : {0} ({1} * 2))".format(effect.overhealth,tempVal, actTurn.stats.shieldGived-clemShieldBefore)
                                            actTurn.refreshEffects()

                                            actTurn.specialVars["clemBloodJauge"].value = 1
                                            actTurn.specialVars["clemMemCast"] = True

                                    elif skillToUse.type in [TYPE_INDIRECT_DAMAGE,TYPE_MALUS]:
                                        if skillToUse.jaugeEff != None:
                                            skillToUse = copy.deepcopy(skillToUse)
                                            try:
                                                if teamJaugeDict[actTurn.team][actTurn].effects.id == skillToUse.jaugeEff.id:
                                                    jaugeConsumed = [teamJaugeDict[actTurn.team][actTurn].value,skillToUse.maxJaugeValue][skillToUse.maxJaugeValue<teamJaugeDict[actTurn.team][actTurn].value]
                                                    teamJaugeDict[actTurn.team][actTurn].value -= jaugeConsumed
                                                    if skillToUse.maxJaugeValue != skillToUse.minJaugeValue and skillToUse.maxJaugeValue != 0:
                                                        skillToUse.effPowerPurcent = (skillToUse.effPowerPurcent//2) + (skillToUse.effPowerPurcent//2)*(jaugeConsumed/(skillToUse.maxJaugeValue-skillToUse.minJaugeValue))
                                                else:
                                                    jaugeConsumed = 0


                                            except KeyError:
                                                logs += "\n{0} hasn't any jauge eff"
                                        
                                        if skillToUse.id != serenaSpe.id:
                                            ballerine = groupAddEffect(caster=actTurn, target=ennemi, area=skillToUse.area, effect=skillToUse.effects, skillIcon=skillToUse.emoji, actionStats=skillToUse.useActionStats, effPurcent = skillToUse.effPowerPurcent)
                                            tempTurnMsg += ballerine
                                            logs += ballerine
                                        else:
                                            for ent in tablEntTeam[int(not(actTurn.team))]:
                                                if ent.hp > 0:
                                                    sumPower = 0
                                                    for eff in ent.effects:
                                                        if eff.effects.id == estal.id:
                                                            sumPower += int(eff.effects.power*eff.turnLeft*(skillToUse.power/100))
                                                            eff.decate(value=100)

                                                    if sumPower > 0:
                                                        ent.refreshEffects()
                                                        sumPower += estal.power * estal.turnInit * (skillToUse.power/100)
                                                        temp = actTurn.indirectAttack(target=ent,value=indirectDmgCalculator(actTurn, ent, sumPower, skillToUse.use, danger, skillToUse.area),icon=skillToUse.emoji)
                                                    else:
                                                        temp = "Cela a aucun effet sur __{0}__\n".format(ent.name)
                                                    tempTurnMsg += temp
                                                    logs += temp

                                        if skillToUse.id == cwUlt.id:
                                            skillToUse.power = skillToUse.power + (skillToUse.maxPower-skillToUse.power)/(jaugeConsumed/[skillToUse.maxJaugeValue,skillToUse.minJaugeValue][skillToUse.maxJaugeValue==0])

                                            power = 0
                                            for eff in ennemi.effects:
                                                if eff.effects.type == TYPE_INDIRECT_DAMAGE:
                                                    if eff.effects.id == coroWind.id:
                                                        power += skillToUse.power * eff.turnLeft/eff.effects.turnInit
                                                    else:
                                                        power += skillToUse.power * eff.turnLeft/eff.effects.turnInit * 1.35
                                                        eff.decate(turn=99)

                                            if power > 0:
                                                ballerine = actTurn.indirectAttack(ennemi,value=indirectDmgCalculator(actTurn, ennemi, power, skillToUse.use, danger, area=skillToUse.area),icon = skillToUse.emoji)
                                                tempTurnMsg += ballerine
                                                logs += ballerine
                                                ennemi.refreshEffects()

                                        elif skillToUse.id == propag.id:
                                            listTarget = []
                                            sumPower = 0
                                            for eff in ennemi.effects:
                                                if eff.effects.id in [estal.id] and eff.value > 0:
                                                    sumPower += eff.effects.power * ([propag.power,propag.power//2][int(eff.caster==actTurn)])/100

                                            effTabl, tablName, effTabl2 = [estal],[[]],[estal2]
                                            for ent in ennemi.cell.getEntityOnArea(area=AREA_DONUT_2,team=actTurn.team,wanted=ENEMIES,fromCell=actTurn.cell,directTarget=False):
                                                if sumPower > 0:
                                                    add_effect(actTurn,ent,effTabl[0],effPowerPurcent=int((sumPower/effTabl[0].power)*100))
                                                    tablName[0].append("{0}".format(ent.icon))
                                                    ent.refreshEffects()

                                            temp = ""
                                            if len(tablName[0]) == 1:
                                                temp = "\n{2} {4} → {0} +{1} ({3}%)".format(tablName[0][0],effTabl[0].emoji[0][0],actTurn.icon,int((sumPower/effTabl[0].power)*100),skillToUse.emoji)
                                            elif len(tablName[0]) > 1:
                                                temp = ""
                                                for cmpt in range(len(tablName[0])):
                                                    temp += tablName[0][cmpt]

                                                temp = "\n{2} {4} → {0} +{1} ({3}%)".format(temp,effTabl[0].emoji[0][0],actTurn.icon,int((sumPower/effTabl[0].power)*100),skillToUse.emoji)
                                            if actTurn.specialVars["heritEstial"]:
                                                if len(tablName[0]) == 1:
                                                    temp += "\n{0} subit l'effet {1} {2} pendant 3 tours".format(tablName[0][0],effTabl2[0].emoji[0][0],effTabl2[0].name,int((sumPower/effTabl2[0].power)*100))
                                                elif len(tablName[0]) > 1:
                                                    temp += "\n"
                                                    for cmpt in range(len(tablName[0])):
                                                        temp += tablName[0][cmpt]
                                                        if cmpt < len(tablName[0])-2:
                                                            temp += ", "
                                                        elif cmpt == len(tablName[0])-2:
                                                            temp += " et "
                                                    temp += "subissent l'effet {0} {1} pendant 3 tours".format(effTabl2[0].emoji[0][0],effTabl2[0].name,int((sumPower/effTabl2[0].power)*100))
                                            tempTurnMsg += temp
                                            logs += temp
                                            tempTurnMsg += "\n"
                                            logs += "\n"

                                    elif skillToUse.type == TYPE_HEAL:
                                        logs += "\n"
                                        if ennemi.hp > 0:
                                            elemPowBonus = 0
                                            if skillToUse.condition[:2] == [0,2]:
                                                for eff in actTurn.effects:
                                                    if eff.effects.id in [tablElemEff[skillToUse.condition[2]],tablElemEff[ELEMENT_UNIVERSALIS_PREMO]]:
                                                        elemPowBonus += eff.effects.power
                                            statUse = skillToUse.use
                                            if statUse == None:
                                                statUse = 0
                                            elif statUse == HARMONIE:
                                                temp = actTurn.allStats()
                                                for a in temp:
                                                    statUse = max(a,statUse)
                                            else:
                                                statUse = actTurn.allStats()[statUse]

                                            power = skillToUse.power * (1+(LIGHTHEALBUFF/100*actTurn.char.element == ELEMENT_LIGHT))
                                            if skillToUse.jaugeEff != None:
                                                try:
                                                    if teamJaugeDict[actTurn.team][actTurn].effects.id == skillToUse.jaugeEff.id:
                                                        jaugeConsumed = [teamJaugeDict[actTurn.team][actTurn].value,skillToUse.maxJaugeValue][skillToUse.maxJaugeValue<teamJaugeDict[actTurn.team][actTurn].value]
                                                        if skillToUse.power != skillToUse.maxPower:
                                                            power = power + (skillToUse.maxPower-skillToUse.power)/(jaugeConsumed/[skillToUse.maxJaugeValue,skillToUse.minJaugeValue][skillToUse.maxJaugeValue==0])

                                                        teamJaugeDict[actTurn.team][actTurn].value -= jaugeConsumed
                                                    else:
                                                        jaugeConsumed = 0
                                                except KeyError:
                                                    logs += "\n{0} hasn't any jauge eff"

                                            power = power * (1+elemPowBonus * 0.05)

                                            if skillToUse.id == dissi.id:
                                                nbSummon = 0
                                                for ent in tablEntTeam[actTurn.team]:
                                                    if type(ent.char) == invoc and ent.id == actTurn.id:
                                                        nbSummon += 1
                                                        tempTurnMsg += "{0} est désinvoqué\n".format(ent.char.name)
                                                        ent.hp = 0
                                                power += skillToUse.power*nbSummon
                                            
                                            if skillToUse.id == trans.id:
                                                actionStats, entActStats = 0, actTurn.actionStats()
                                                for cmpt in (0,1,2,3,4):
                                                    if entActStats[cmpt] > entActStats[actionStats]:
                                                        actionStats = cmpt
                                            else:
                                                actionStats = ACT_HEAL

                                            if skillToUse.effects != [None] and skillToUse.effBeforePow:
                                                ballerine = groupAddEffect(caster=actTurn, target=ennemi, area=skillToUse.area, effect=skillToUse.effects, skillIcon=skillToUse.emoji, actionStats=skillToUse.useActionStats, effPurcent = skillToUse.effPowerPurcent)
                                                tempTurnMsg = tempTurnMsg + ballerine
                                                logs += ballerine

                                            if skillToUse.id == uberCharge.id:
                                                if jaugeConsumed >= 100:
                                                    skillToUse.effects[0] = uberImune
                                                else:
                                                    skillToUse.effects[0] = copy.deepcopy(defenseUp)
                                                    skillToUse.effects[0].power = 5 + (70/100*jaugeConsumed)

                                            for ent in ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,fromCell=actTurn.cell,wanted=ALLIES,directTarget=False):
                                                funnyTempVarName, useless = actTurn.heal(ent, skillToUse.emoji, skillToUse.use, power,danger=danger, mono = skillToUse.area == AREA_MONO, useActionStats = skillToUse.useActionStats)
                                                tempTurnMsg += funnyTempVarName
                                                logs += funnyTempVarName

                                            if skillToUse.effects != [None] and not(skillToUse.effBeforePow):
                                                ballerine = groupAddEffect(caster=actTurn, target=ennemi, area=skillToUse.area, effect=skillToUse.effects, skillIcon=skillToUse.emoji, actionStats=skillToUse.useActionStats, effPurcent = skillToUse.effPowerPurcent)
                                                tempTurnMsg += ballerine
                                                logs += ballerine

                                    elif skillToUse.type == TYPE_SUMMON:
                                        toSummon, cmpt, limit = findSummon(skillToUse.invocation), 0, skillToUse.nbSummon
                                        if skillToUse.id == sumLightButterfly.id:
                                            try:
                                                if teamJaugeDict[actTurn.team][actTurn].effects.id == jaugeButLight.id:
                                                    limit += teamJaugeDict[actTurn.team][actTurn].value//40
                                                    teamJaugeDict[actTurn.team][actTurn].value = int(teamJaugeDict[actTurn.team][actTurn].value%40)
                                            except KeyError:
                                                pass

                                        while cmpt < limit:
                                            cellToSummon = actTurn.cell.getCellForSummon(skillToUse.range,actTurn.team,toSummon,actTurn)
                                            if cellToSummon != None:
                                                tablEntTeam, tablAliveInvoc, time, funnyTempVarName = actTurn.summon(toSummon,time,cellToSummon,tablEntTeam,tablAliveInvoc,ignoreLimite=True)
                                                tempTurnMsg += funnyTempVarName+"\n"
                                                logs += "\n"+funnyTempVarName
                                            cmpt += 1

                                    elif skillToUse.type == TYPE_RESURECTION:
                                        if skillToUse.id == aliceRez.id:
                                            nbDown = 0
                                            for ent in tablEntTeam[actTurn.team]:
                                                if ent.status == STATUS_DEAD:
                                                    nbDown += 1

                                            if nbDown >= len(team1)//2:
                                                skillToUse = aliceRez2

                                        stat, resTabl = skillToUse.use, []

                                        for entityInArea in ennemi.cell.getEntityOnArea(area=skillToUse.area,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,dead=True,directTarget=False,ignoreInvoc=True):
                                            if stat not in [PURCENTAGE,None]:
                                                if stat != HARMONIE:
                                                    statUse = actTurn.allStats()[stat]
                                                else:
                                                    temp = actTurn.allStats()
                                                    for b in temp:
                                                        statUse = max(b,statUse)

                                                tempActStatsTabl = [[ACT_HEAL,actTurn.negativeHeal],[ACT_BOOST,actTurn.negativeBoost],[ACT_SHIELD,actTurn.negativeShield]]
                                                tempActStatsTabl.sort(key=lambda ballerine:ballerine[1])
                                                healPowa = min(entityInArea.maxHp, calHealPower(actTurn,entityInArea,skillToUse.power,1,skillToUse.use,tempActStatsTabl[0][0],danger))

                                            elif stat == PURCENTAGE:
                                                healPowa = round(entityInArea.maxHP * skillToUse.power/100 * (100-entityInArea.healResist)/100)

                                            elif stat == None:
                                                healPowa = skillToUse.power

                                            funnyTempVarName = await actTurn.resurect(entityInArea,healPowa,skillToUse.emoji,danger=danger)
                                            tempTurnMsg += funnyTempVarName
                                            logs += funnyTempVarName
                                            resTabl.append(entityInArea)


                                        for eff in skillToUse.effects:
                                            if eff != None:
                                                ballerine = groupAddEffect(actTurn, actTurn, resTabl , eff, skillIcon=skillToUse.emoji)
                                                tempTurnMsg += ballerine
                                                logs += ballerine

                                    elif skillToUse.type == TYPE_DEPL:
                                        actTurn.smnDepl(skillToUse.depl,ennemi)
                                        logs += "\n{0} is placing a {1} at {2}:{3}".format(actTurn.name,skillToUse.depl.name,ennemi.x,ennemi.y)
                                        tempTurnMsg += "{0} a déployé {1} __{2}__ sur la cellule {3}:{4}".format(actTurn.name,skillToUse.depl.icon[actTurn.team],skillToUse.depl.name,ennemi.x,ennemi.y)
                                        if ennemi.on != None:
                                            tempTurnMsg += " ({0})\n".format(ennemi.on.icon)
                                        else:
                                            tempTurnMsg += "\n"

                                    elif type(ennemi) == entity: # Damage
                                        power, elemPowBonus, elemEffGet = skillToUse.power, 0, 0
                                        if skillToUse.ultimate and actTurn.char.aspiration == MAGE:
                                            power = int(power*1.2)

                                        if skillToUse.condition[:2] == [0,2]:
                                            for eff in actTurn.effects:
                                                if eff.effects.id in [tablElemEff[skillToUse.condition[2]],tablElemEff[ELEMENT_UNIVERSALIS_PREMO]]:
                                                    elemPowBonus += eff.effects.power
                                                    elemEffGet += 1
                                        if elemPowBonus > 0:
                                            power = power * (1+(elemPowBonus/100))

                                        if skillToUse.jaugeEff != None:
                                            try:
                                                if teamJaugeDict[actTurn.team][actTurn].effects.id == skillToUse.jaugeEff.id:
                                                    jaugeConsumed = [teamJaugeDict[actTurn.team][actTurn].value,skillToUse.maxJaugeValue][skillToUse.maxJaugeValue<teamJaugeDict[actTurn.team][actTurn].value]
                                                    if skillToUse.power != skillToUse.maxPower:
                                                        power = power + (skillToUse.maxPower-skillToUse.power)/(jaugeConsumed/[skillToUse.maxJaugeValue,skillToUse.minJaugeValue][skillToUse.maxJaugeValue==0])
                                                    teamJaugeDict[actTurn.team][actTurn].value -= jaugeConsumed
                                                else:
                                                    jaugeConsumed = 0
                                            except KeyError:
                                                logs += "\n{0} hasn't any jauge eff"

                                        if skillToUse.id == lowBlow.id and (type(ennemi.char) == octarien and (ennemi.char.oneVAll or ennemi.name in ENEMYIGNORELIGHTSTUN)):
                                            power += skillToUse.maxPower - skillToUse.power
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
                                            for eff in ennemi.effects:
                                                if eff.effects.type == TYPE_ARMOR and not(eff.effects.absolutShield):
                                                    reduc = eff.value // 2
                                                    eff.value -= reduc
                                                    totalArmor += reduc
                                                    tempTurnMsg += "{0} {1} → -{2}{3}{4} ({5})\n".format(actTurn.icon,skillToUse.emoji,reduc,eff.icon,ennemi.icon,skillToUse.name)

                                            if totalArmor > 0:
                                                effect = classes.effect("Réassemblé","krysShieldy",overhealth=totalArmor,type=TYPE_ARMOR,turnInit=99,trigger=TRIGGER_DAMAGE)
                                                tempTurnMsg += add_effect(actTurn,actTurn,effect,ignoreEndurance=True)
                                                actTurn.refreshEffects()
                                        elif skillToUse.id == theEnd.id:
                                            for eff in ennemi.effects:
                                                if eff.effects.id == reaperEff.id:
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
                                                ennemi.stats.sufferingFromSucess = True
                                        elif skillToUse.id == bleedingConvert.id:
                                            bleedingNumber = 0
                                            for eff in ennemi.effects:
                                                if eff.effects.id == bleeding.id:
                                                    bleedingNumber += eff.effects.power/bleeding.power * eff.turnLeft * 0.1
                                                    eff.decate(turn=99)
                                            power = power * (bleedingNumber+1)
                                        elif skillToUse.id == kikuSkill2.id and ennemi.status == STATUS_ALIVE:
                                            power = int(power*2)
                                        elif skillToUse.id == lizLB.id:
                                            nbCharm = 0
                                            for ent in tablEntTeam[not(actTurn.team)]:
                                                for eff in ent.effects:
                                                    if eff.effects.id == charming.id:
                                                        nbCharm += 1
                                                        eff.decate(turn=99)
                                                ent.refreshEffects()
                                            power += LIZLBPOWERGAINPERCHARM*nbCharm
                                        elif skillToUse.id in elemArrowId+elemRuneId:
                                            power += INCREASEPOWERPURCENTBYELEMEFF * useEffElem
                                        elif skillToUse.id in [klikliStrike.id,gwenyStrike.id]:
                                            hpConsumed = actTurn.hp - 1
                                            actTurn.stats.selfBurn += hpConsumed
                                            actTurn.hp = 1
                                            tempTurnMsg += "Les PVs de {0} sont réduits à 1 !\n".format(actTurn.name)
                                            power += (skillToUse.maxPower - skillToUse.power) * (hpConsumed/actTurn.maxHp)
                                        elif skillToUse.id in [akikiSkill3_1_1.id,akikiSkill2_1_2.id]:
                                            nbEnnemis = len(ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENEMIES,directTarget=False,fromCell=ennemi.cell,ignoreAspiration = [[OBSERVATEUR,ATTENTIF,SORCELER,MAGE,ALTRUISTE,IDOLE,INOVATEUR,PREVOYANT,MASCOTTE],None][skillToUse.id==akikiSkill3_1_1.id]))
                                            power = skillToUse.power // max(nbEnnemis,1)
                                        elif skillToUse.id == liaExUlt_1.id:
                                            effect = classes.effect("Kaze no yoroi","liaExUltShield",overhealth=int(actTurn.maxHp * (1-10*elemEffGet)),type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,turnInit=2)
                                            tempTurnMsg += add_effect(actTurn,actTurn,effect,ignoreEndurance=True)
                                            actTurn.refreshEffects()
                                        elif skillToUse.id in [liaExUlt_2.id,liaExUlt_3.id]:
                                            power = int(power * (1+10*elemEffGet))
                                        elif skillToUse.id in [liaExUlt_4.id]:
                                            power = int(power * (1+15*elemEffGet))

                                        actionStats = skillToUse.useActionStats
                                        
                                        if None not in skillToUse.effects and skillToUse.effBeforePow:
                                            tempTurnMsg += "\n"
                                            for a in skillToUse.effects:
                                                effect = findEffect(a)
                                                tempTurnMsg = tempTurnMsg[:-1] + add_effect(actTurn,ennemi,effect,effPowerPurcent=skillToUse.effPowerPurcent)

                                        cmpt = 0
                                        while cmpt < skillToUse.repetition and ennemi.hp > 0 and skillToUse.power > 0:
                                            funnyTempVarName, temp = actTurn.attack(target=ennemi,value=power,icon=skillToUse.emoji,area=skillToUse.area,sussess=skillToUse.sussess,use=skillToUse.use,onArmor=skillToUse.onArmor,useActionStats=actionStats,setAoEDamage=skillToUse.setAoEDamage,lifeSteal = skillToUse.lifeSteal,erosion = skillToUse.erosion, skillPercing = skillToUse.percing, execution=skillToUse.execution, armorConvert=skillToUse.armorConvert)
                                            tempTurnMsg += funnyTempVarName
                                            logs += "\n"+funnyTempVarName
                                            deathCount += temp
                                            cmpt += 1
                                            if cmpt < skillToUse.repetition:
                                                tempTurnMsg += "\n"

                                        if None not in skillToUse.effects and not(skillToUse.effBeforePow):
                                            tempTurnMsg += "\n"
                                            for a in skillToUse.effects:
                                                eff = findEffect(a)
                                                tempTurnMsg += add_effect(actTurn,ennemi,eff,effPowerPurcent=skillToUse.effPowerPurcent)
                                                logs += "\n{0} gave the {1} effect at {2} for {3} turn(s)".format(actTurn.char.name,effect.name,ennemi.char.name,effect.turnInit)


                                        if skillToUse.power > 0 and actTurn.specialVars["damageSlot"] != None:
                                            loose = int(actTurn.maxHp * (15/100))
                                            funnyTempVarName = "\n{0} : -{1} PV ({2})\n".format(actTurn.icon,loose,actTurn.specialVars["damageSlot"].effects.name)
                                            tempTurnMsg += funnyTempVarName
                                            logs + funnyTempVarName
                                            actTurn.hp -= loose
                                            actTurn.stats.selfBurn += loose
                                            if actTurn.hp <= 0:
                                                tempTurnMsg += actTurn.death(killer=actTurn)

                                            actTurn.refreshEffects()

                                        if actTurn.isNpc("Ailill") and skillToUse.id == "headnt":
                                            ennemi.stats.headnt = True
                                        if skillToUse.execution:
                                            ennemi.status = STATUS_TRUE_DEATH

                                # =================================================================
                                # Knockback
                                if skillToUse.knockback > 0:
                                    tablEnt = ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=[ENEMIES,ALLIES][skillToUse.id == friendlyPush.id],directTarget=False,fromCell=actTurn.cell)
                                    tablEnt.sort(key=lambda ent: actTurn.cell.distance(ent.cell),reverse=True)
                                    for ent in tablEnt:
                                        temp = actTurn.knockback(ent,skillToUse.knockback)
                                        tempTurnMsg += temp
                                        logs += temp
                                
                                if skillToUse.pull > 0:
                                    tablEnt = ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENEMIES,directTarget=False,fromCell=actTurn.cell)
                                    tablEnt.sort(key=lambda ent: actTurn.cell.distance(ent.cell))
                                    for ent in tablEnt:
                                        temp = actTurn.pull(ent,skillToUse.pull)
                                        tempTurnMsg += temp
                                        logs += temp

                                # JumpBack
                                if skillToUse.jumpBack > 0:
                                    temp = actTurn.jumpBack(skillToUse.jumpBack,ennemi.cell)
                                    tempTurnMsg += temp
                                    logs += temp

                                # Does the skill give a effect on the caster ?
                                if skillToUse.effectAroundCaster != None:
                                    tempTurnMsg += "\n"
                                    if skillToUse.effectAroundCaster[0] == TYPE_HEAL:
                                        for a in actTurn.cell.getEntityOnArea(area=skillToUse.effectAroundCaster[1],fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,directTarget=False):
                                            funnyTempVarName, useless = actTurn.heal(a, skillToUse.emoji, skillToUse.use, skillToUse.effectAroundCaster[2] * (1+LIGHTHEALBUFF/100*(actTurn.char.element == ELEMENT_LIGHT)),danger=danger, mono = skillToUse.area == skillToUse.effectAroundCaster[1], useActionStats = skillToUse.useActionStats)
                                            tempTurnMsg += funnyTempVarName
                                            logs += funnyTempVarName
                                    elif skillToUse.effectAroundCaster[0] == TYPE_DAMAGE:
                                        funnyTempVarName, temp = actTurn.attack(target=actTurn,value=skillToUse.effectAroundCaster[2],icon=skillToUse.emoji,area=skillToUse.effectAroundCaster[1],sussess=skillToUse.sussess,use=skillToUse.use,onArmor=skillToUse.onArmor,useActionStats=actionStats,setAoEDamage=skillToUse.setAoEDamage,lifeSteal = skillToUse.lifeSteal)
                                        tempTurnMsg += funnyTempVarName
                                        logs += "\n"+funnyTempVarName
                                    elif type(skillToUse.effectAroundCaster[2]) == classes.effect:
                                        ballerine = groupAddEffect(actTurn, actTurn , skillToUse.effectAroundCaster[1], skillToUse.effectAroundCaster[2], skillToUse.emoji, effPurcent=[skillToUse.effPowerPurcent,liaLB.effPowerPurcent/5][skillToUse.id == trans.id and actTurn.isNpc("Lia")])
                                        tempTurnMsg += ballerine
                                        logs += ballerine

                                    elif skillToUse.effectAroundCaster[0] == TYPE_RESURECTION:
                                        stat = skillToUse.use

                                        for a in actTurn.cell.getEntityOnArea(area=skillToUse.effectAroundCaster[1],fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,dead=True,directTarget=False):
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

                                if skillToUse.id == trans.id and skillToUse.name == lb4.name:
                                    for a in actTurn.cell.getEntityOnArea(area=AREA_ALL_ALLIES,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,directTarget=False):
                                        funnyTempVarName, useless = actTurn.heal(a, skillToUse.emoji, skillToUse.use, 200,danger=danger, mono = False, useActionStats = skillToUse.useActionStats)
                                        tempTurnMsg += funnyTempVarName
                                        logs += funnyTempVarName

                                    lb4DmgBuff = copy.deepcopy(dmgUp)
                                    lb4DmgBuff.power, lb4DmgBuff.turnInit = 15,3
                                    lb4DefBuff = copy.deepcopy(defenseUp)
                                    lb4DefBuff.power, lb4DefBuff.turnInit = 15,3
                                    ballerine = groupAddEffect(actTurn, actTurn , AREA_ALL_ALLIES, [lb4DmgBuff,lb4DefBuff], skillToUse.emoji)
                                    tempTurnMsg += ballerine
                                    logs += ballerine
                                    
                                if skillToUse.effectOnSelf != None and not(skillToUse.effBeforePow):
                                    if not(findEffect(skillToUse.effectOnSelf).silent):
                                        if tempTurnMsg[-1] == "\n":
                                            tempTurnMsg += "\n"
                                        else:
                                            tempTurnMsg += "\n\n"
                                    eff = findEffect(skillToUse.effectOnSelf)
                                    if eff.replica != None:
                                        tempTurnMsg += add_effect(actTurn,actTurn,eff,setReplica=ennemi)
                                        if ennemi != actTurn and not(skillToUse.replay):
                                            eff2 = classes.effect("⚠️ Cible - {0}".format(eff.replica.name),"targeted{0}".format(eff.replica.id),effPrio=1,silent=True,turnInit=eff.turnInit-1,emoji=eff.replica.emoji)
                                            add_effect(actTurn,ennemi,eff2)
                                            ennemi.refreshEffects()
                                    else:
                                        tempTurnMsg += add_effect(actTurn,actTurn,eff,skillIcon = skillToUse.emoji,effPowerPurcent=skillToUse.selfEffPurcent)
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
                                        burn = classes.effect("Régénération de lumière","catLightEff",INTELLIGENCE,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_END_OF_TURN,power=int(skillToUse.effects[0].overhealth*0.2),turnInit=3)
                                        ballerine = groupAddEffect(actTurn, ennemi, skillToUse.area, burn, skillToUse.emoji, effPurcent = 100 * useEffElem)
                                        logs += ballerine
                                        tempTurnMsg += ballerine
                                    elif skillToUse.id == useElemEffId[7]:
                                        burn = classes.effect("Armure temporelle","catTimeEff",CHARISMA,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,overhealth=int(skillToUse.power*0.2*useEffElem),turnInit=3)
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
                                            ballerine, why = actTurn.attack(ennemi,int(skillToUse.power*0.15),skillToUse.emoji,AREA_MONO,skillToUse.sussess,use=MAGIE,skillPercing=skillToUse.percing)
                                            logs += ballerine
                                            tempTurnMsg += ballerine
                                            cmpt += 1
                                    elif skillToUse.id == useElemEffId[3]:
                                        ballerine, why = actTurn.attack(actTurn,int(skillToUse.power*0.2*useElemEffId),skillToUse.emoji,AREA_DONUT_2,skillToUse.sussess,use=MAGIE,skillPercing=skillToUse.percing)
                                        logs += ballerine
                                        tempTurnMsg += ballerine
                                    else:
                                        tablTargets = ennemi.cell.getEntityOnArea(area=skillToUse.area,fromCell=actTurn.cell,team=actTurn.team,wanted=ENEMIES,directTarget=False)
                                        cmpt = 0
                                        while cmpt < useEffElem and len(tablTargets) > 0:
                                            if len(tablTargets) > 1:
                                                target = tablTargets[random.randint(0,len(tablTargets)-1)]
                                            else:
                                                target = tablTargets[0]

                                            ballerine, why = actTurn.attack(target,int(skillToUse.power*0.30),skillToUse.emoji,AREA_CIRCLE_1,skillToUse.sussess,use=MAGIE,skillPercing=skillToUse.percing)
                                            logs += ballerine
                                            tempTurnMsg += "\n"+ballerine
                                            if target.hp <= 0:
                                                tablTargets.remove(target)
                                            cmpt += 1

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

                                    if skillToUse.id == clemUltLauch.id:
                                        for ent in tablEntTeam[int(not(actTurn.team))]:
                                            if ent.isNpc("Alice Exaltée"):
                                                for eff in ent.effects:
                                                    if eff.effects.id == aliceStunEffect.id:
                                                        tempTurnMsg += eff.decate(turn=99)

                                # Max Hp cost
                                if skillToUse.maxHpCost > 0:
                                    diff = actTurn.maxHp - int(actTurn.maxHp * (1-(skillToUse.maxHpCost/100)))
                                    actTurn.maxHp = int(actTurn.maxHp * (1-(skillToUse.maxHpCost/100)))
                                    diff2 = min(0,actTurn.maxHp-actTurn.hp)
                                    actTurn.hp = min(actTurn.hp,actTurn.maxHp)
                                    tempTurnMsg += "\n<:dvin:1004737746377654383> → {0} -{1} PV max\n".format(actTurn.icon,diff)
                                    actTurn.stats.selfBurn += abs(diff2)

                                # Act HpCost
                                if skillToUse.hpCost > 0:
                                    diff = actTurn.hp - int(actTurn.hp * (1-(skillToUse.hpCost/100)))
                                    actTurn.hp -= diff
                                    tempTurnMsg += "\n<:dmon:1004737763771433130> → {0} -{1} PV\n".format(actTurn.icon,diff)
                                    actTurn.stats.selfBurn += diff

                                    if actTurn.hp <= 0:
                                        tempTurnMsg += actTurn.death(killer=actTurn)

                                if skillToUse.replay:
                                    replay = skillToUse.replay

                                if skillToUse.condition[:2] == [0,2]:
                                    for eff in actTurn.effects:
                                        if eff.effects.id in [matriseElemEff.id,liaExWeapEff.id]:
                                            if random.randint(0,99) <= eff.effects.power:
                                                ballerine = add_effect(actTurn,actTurn,matriseElemEff.callOnTrigger,skillIcon=matriseElemEff.emoji[0][0])
                                                actTurn.refreshEffects()
                                                tempTurnMsg += ballerine
                                                logs += ballerine

                                if actTurn.specialVars["convicVigil"] != None and skillToUse.type == TYPE_DAMAGE:
                                    ballerine = actTurn.specialVars["convicVigil"].triggerStartOfTurn(danger,decate=True)
                                    logs += ballerine
                                    tempTurnMsg += ballerine
                                elif actTurn.specialVars["convicPro"] != None and skillToUse.type == TYPE_DAMAGE:
                                    ballerine = actTurn.specialVars["convicPro"].triggerStartOfTurn(danger,decate=True)
                                    logs += ballerine
                                    tempTurnMsg += ballerine

                                if skillToUse.id == liaExUlt_4.id:
                                    elemNm = 0
                                    for eff in actTurn.effects:
                                        if eff.effects.id in [tablElemEff[skillToUse.condition[2]],tablElemEff[ELEMENT_UNIVERSALIS_PREMO]]:
                                            elemNm += 1
                                            eff.decate(turn=99)
                                    
                                    funnyTempVarName, useless = actTurn.heal(actTurn, skillToUse.emoji, None, int(actTurn.maxHp * (0.05*elemNm)),danger=danger, mono = True, useActionStats = skillToUse.useActionStats)
                                    tempTurnMsg += funnyTempVarName
                                    logs += funnyTempVarName
                                    actTurn.refreshEffects()

                                # ============================= Interactions =============================
                                if skillToUse.id == strengthOfWill.id and actTurn.isNpc("Félicité") and dictIsNpcVar["Clémence"]:       # Féli / Clem
                                    tempTurnMsg += "<:felicite:909048027644317706> : *\"Alors Clémence :D ? Combien combien ?\"*\n<:clemence:908902579554111549> : *\"Hum... {0} sur 20\"*\n<:felicite:909048027644317706> : :D\n".format(random.randint(15,22))

                                if skillToUse.ultimate and skillToUse.effects != [None] and skillToUse.type == TYPE_BOOST and dictIsNpcVar["Alice"] and not(actTurn.isNpc("Alice")):               # Alice
                                    for team in [0,1]:
                                        for ent in tablEntTeam[team]:
                                            if ent.isNpc("Alice") and ent.hp > 0:
                                                damage = indirectDmgCalculator(ent, actTurn, [15,25][skillToUse.id == onstage.id], CHARISMA, 100, area=AREA_MONO)
                                                murcialago = "\n"+ent.indirectAttack(target=actTurn,value=damage,icon="",ignoreImmunity=True,name='Coup bas',hideAttacker=True)
                                                tempTurnMsg += murcialago
                                                logs += "\nAlice wasn't verry happy about that\n"+murcialago
                                                break

                                if skillToUse.effectOnSelf != None and findEffect(skillToUse.effectOnSelf).replica != None and skillToUse.power == 0 and skillToUse.effects == [None]:
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

                                elif skillToUse.id in tablRosesSkillsId and skillToUse.effectOnSelf == None: # Final Floral On Self
                                    for skilly in actTurn.char.skills:
                                        if type(skilly) == classes.skill and skilly.id == finalFloral.id:
                                            roseCount = 0
                                            for eff in actTurn.effects:
                                                if eff.effects.id in tablRosesId:
                                                    roseCount += 1

                                            if roseCount < 3:
                                                if skillToUse.id in [onstage.id,floraisonFinale.id]:
                                                    roseToAdd = rosePink
                                                elif skillToUse.id in [crimsomLotus.id]:
                                                    roseToAdd = roseYellow
                                                elif skillToUse.id in [corGraFinal.id,petalisation.id]:
                                                    roseToAdd = roseDarkBlu
                                                elif skillToUse.id in [aliceDanceFinal.id,danceFas.id]:
                                                    roseToAdd = roseRed
                                                
                                                tempMsg = groupAddEffect(actTurn,actTurn,AREA_MONO,roseToAdd,skillToUse.emoji)
                                                tempTurnMsg += tempMsg
                                                logs += tempMsg
                                                roseCount += 1
                                                if roseCount == 3:
                                                    tempMsg = add_effect(actTurn,actTurn,finFloCast,setReplica=actTurn,skillIcon=finFloEff.emoji[0][actTurn.team])
                                                    tempTurnMsg += tempMsg
                                                    logs += tempMsg
                                            break

                                elif skillToUse.id in finFloOtherSkillsId: # Final Floral on others
                                    for ent in tablEntTeam[actTurn.team]:
                                        rosesNb, haveFinFlo = 0, False
                                        for eff in ent.effects:
                                            if eff.effects.id == finFloEff.id:
                                                haveFinFlo = True
                                            elif eff.effects.id in tablRosesId:
                                                rosesNb += 1
                                        
                                        if haveFinFlo and rosesNb <= 2:
                                            if skillToUse.id in [finalTech.id,croissance.id]:
                                                roseToAdd = roseBlue
                                            elif skillToUse.id in [valse.id,roseeHeal.id]:
                                                roseToAdd = roseGreen
                                            tempMsg = groupAddEffect(ent,ent,AREA_MONO,roseToAdd,skillToUse.emoji)
                                            tempTurnMsg += tempMsg
                                            logs += tempMsg

                                            rosesNb += 1
                                            if rosesNb == 3:
                                                tempMsg = add_effect(ent,ent,finFloCast,setReplica=ent,skillIcon=finFloEff.emoji[0][ent.team])
                                                tempTurnMsg += tempMsg
                                                logs += tempMsg

                                elif skillToUse.id in [astrodyn.id,cercleCon.id]:
                                    LBBars[actTurn.team][1] = min(LBBars[actTurn.team][1]+3,LBBars[actTurn.team][0]*3)
                                
                                elif skillToUse.id in [plumeCel.id,hinaUlt.id,plumePers.id,pousAviaire.id]:
                                    for skilly in actTurn.char.skills:
                                        skillo = findSkill(skilly)
                                        if skillo != None and skillo.id == plumRem.id:
                                            tablSuccess, tablEnt = [], ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENEMIES,ignoreInvoc = True, directTarget=False,fromCell=actTurn.cell)
                                            for ent in tablEnt:
                                                if random.randint(0,99) < skillo.power:
                                                    tablSuccess.append(ent)
                                            if len(tablSuccess) > 0:
                                                temp = groupAddEffect(actTurn, ennemi, tablSuccess, [plumRemEff], skillIcon=skillo.emoji)
                                                tempTurnMsg += "\n"+temp
                                                logs += temp
                                            break

                                elif skillToUse.id == raisingPheonixLaunch.id and skillToUse.power != 0 and actTurn.isNpc("Chûri"):
                                    actTurn.icon = "<:churHi:994045813175111811>"
                                    actTurn.char.name, actTurn.char.element = "Chûri-Hinoro", ELEMENT_FIRE
                                    tempChurSkills = copy.deepcopy(churInoSkills)
                                    for cmpt in range(len(lvlToUnlockSkill)):
                                        if actTurn.level < lvlToUnlockSkill[cmpt]:
                                            tempChurSkills[cmpt] = "0"
                                    actTurn.char.skills = tempChurSkills

                                    for eff in actTurn.effects:
                                        if eff.effects.id == tablElemEff[ELEMENT_EARTH].id:
                                            eff.effects, eff.icon = copy.deepcopy(tablElemEff[ELEMENT_FIRE]), tablElemEff[ELEMENT_EARTH].emoji[0][0]
                                    if tempTurnMsg[-1] == "\n":
                                        tempTurnMsg += "\n<:churi:992941366537633914> __Chûri__ prend sa forme de Demi-Phenix !"
                                    else:
                                        tempTurnMsg += "\n\n<:churi:992941366537633914> __Chûri__ prend sa forme de Demi-Phenix !"
                                    logs += "\nChuri is ready to burn everything !\n"

                                else:
                                    for cmpt in range(len(horoSkills)):
                                        if skillToUse.id == horoSkills[cmpt].id:
                                            haveFound = False
                                            for ent in tablEntTeam[actTurn.team]:
                                                for skilly in ent.char.skills:
                                                    if type(skilly) == classes.skill and skilly.id == horoscope.id:
                                                        allreadyhave = False
                                                        for eff in ent.effects:
                                                            if eff.effects.id == horoscopeEff[cmpt][0].id:
                                                                allreadyhave = True
                                                                break
                                                        if not(allreadyhave):
                                                            tempMsg = groupAddEffect(caster=actTurn, target=ent, area=AREA_MONO, effect=[horoscopeEff[cmpt][0]], skillIcon=skillToUse.emoji)
                                                            tempMsg += groupAddEffect(caster=actTurn, target=actTurn, area=AREA_MONO, effect=[elemEff], skillIcon=skillToUse.emoji)
                                                            logs += tempMsg
                                                            tempTurnMsg += tempMsg
                                
                                try:                # Big raise
                                    if actTurn.stats.allieResurected - allyRea >= 3:
                                        if actTurn.char.says.bigRaise != None:
                                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,actTurn.char.says.bigRaise.format(skill=skillToUse.name))
                                        tablReact = []
                                        for team in [0,1]:
                                            for ent in tablEntTeam[team]:
                                                if ent.hp > 0 and ent != actTurn and [ent.char.says.reactBigRaiseEnnemy,ent.char.says.reactBigRaiseAllie][ent.team == actTurn.team] != None and (ent not in ressurected[ent.team]):
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

                                try:                # LB React
                                    if skillToUse.id == trans.id:
                                        tablReact = []
                                        for team in [0,1]:
                                            for ent in tablEntTeam[team]:
                                                if ent.hp > 0 and ent != actTurn and [ent.char.says.reactEnemyLb ,ent.char.says.reactAllyLb][ent.team == actTurn.team] != None:
                                                    tablReact.append([ent.icon,[ent.char.says.reactEnemyLb ,ent.char.says.reactAllyLb][ent.team == actTurn.team]])

                                        if len(tablReact) != 0:
                                            if len(tablReact) == 1:
                                                rand = 0
                                            else:
                                                rand = random.randint(0,len(tablReact)-1)
                                            tempTurnMsg += "\n{0} : *\"{1}\"*".format(tablReact[rand][0],tablReact[rand][1].format(caster=actTurn.char.name,skill=skillToUse.name))
                                except:
                                    tempTurnMsg += "\n__Error with the LBs reactions.__ See logs for more informations"
                                    logs += "\n"+format_exc()

                                try:
                                    for conds in teamJaugeDict[actTurn.team][actTurn].effects.jaugeValue.conds:
                                        if conds.type == INC_USE_SKILL:
                                            for skilly in conds.add:
                                                if skilly.id == skillToUse.id:
                                                    teamJaugeDict[actTurn.team][actTurn].value = min(teamJaugeDict[actTurn.team][actTurn].value+conds.value,100)
                                        if conds.type == INC_USE_ELEMENT_SKILL and skillToUse.condition == [EXCLUSIVE, ELEMENT, conds.add]:
                                            teamJaugeDict[actTurn.team][actTurn].value = min(teamJaugeDict[actTurn.team][actTurn].value+conds.value,100)
                                        if conds.type == INC_USE_GROUP_SKILL and skillToUse.group == conds.add:
                                            teamJaugeDict[actTurn.team][actTurn].value = min(teamJaugeDict[actTurn.team][actTurn].value+conds.value,100)
                                except KeyError:
                                    pass
                                # Skill React
                                if skillToUse.name in [lb3Tabl[VIGILANT].name,lb3Tabl[ALTRUISTE].name] and dictIsNpcVar["Nacialisla"]:
                                    tempTurnMsg += "\n{0} : *\"{1}\"*".format("<:nacialisla:985933665534103564>","Si vous pensez que mettre mon nom sur vos sorts plus puissants va m'attendrir vous vous mettez le doigt dans l'oeuil.")

                            if actTurn.stats.fullskip and optionChoice != OPTION_SKIP:
                                actTurn.stats.fullskip = False

                            if actTurn.isNpc("Luna prê.") and optionChoice == OPTION_SKILL and skillToUse.id in [lunaSpe.id,lunaSpeCast.id]:
                                replay = False

                            if lunaQFEff != None and not(replay or (optionChoice == OPTION_MOVE and not(allReadyMove))):
                                replay = True
                                lunaUsedQuickFight += lunaQFEff.decate(1)
                                actTurn.refreshEffects()

                            if not(replay or (optionChoice == OPTION_MOVE and not(allReadyMove))):
                                if actTurn.isNpc("Epiphyllum"):
                                    if dictIsNpcVar["Amary"]:
                                        for ent in tablEntTeam[actTurn.team]:
                                            if ent.isNpc("Amary"):
                                                if ent.hp <= 0 and ent.status == STATUS_DEAD:
                                                    ballerine = await actTurn.resurect(ent,calHealPower(actTurn,ent,100,1,HARMONIE,ACT_SHIELD,danger),lifeSeed.emoji,danger)
                                                    logs += ballerine
                                                    tempTurnMsg += ballerine
                                                break
                                    if dictIsNpcVar["Edelweiss"]:
                                        for ent in tablEntTeam[actTurn.team]:
                                            if ent.isNpc("Edelweiss"):
                                                if ent.hp <= 0 and ent.status == STATUS_DEAD:
                                                    ballerine = await actTurn.resurect(ent,calHealPower(actTurn,ent,100,1,HARMONIE,ACT_SHIELD,danger),lifeSeed.emoji,danger)
                                                    logs += ballerine
                                                    tempTurnMsg += ballerine
                                                break                                
                                break
                            else:
                                replay, isCasting = False, False
                                if optionChoice != OPTION_MOVE:
                                    for eff in actTurn.effects:
                                        if eff.effects.replica != None:
                                            isCasting = True
                                            break
                                    
                                tempTurnMsg += lunaUsedQuickFight
                                if optionChoice == OPTION_MOVE and not(allReadyMove):
                                    allReadyMove = True
                                    logs += "\n"

                                if not(auto) and not(actTurn.auto):   # Sending the Turn message
                                    if len(tempTurnMsg) > 4096:
                                        tempTurnMsg = unemoji(tempTurnMsg)
                                        if len(tempTurnMsg) > 4096:
                                            tempTurnMsg = "OVERLOAD"
                                    await msg.edit(embeds = [embInfo, interactions.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color)]+choiceEmbed,components=[infoSelect])
                                    if not(isCasting):
                                        await asyncio.sleep(3)
                                    else:
                                        await asyncio.sleep(1)
                    
                                for team in [0,1]:                      # Does a team is dead ?
                                    for ent in tablEntTeam[team]:
                                        if ent.hp > 0 and type(ent.char) not in [invoc, depl]:
                                            everyoneDead[team] = False
                                            break

                                if everyoneDead[0] or everyoneDead[1]:  # If Yes, ending the fight
                                    fight = False
                                    break
                    # ==========================================
                    # Else, the entity is stun
                    else:                                   # The entity is, in fact, stun
                        temp = ""
                        if tablEntTeam[1][0].isNpc("Luna prê.") or tablEntTeam[1][0].isNpc("Luna ex."):
                            for eff in actTurn.effects:
                                if eff.effects.id == lunaInfiniteDarknessStun.id:
                                    temp = actTurn.quickEvent(stat=ENDURANCE, required=int(250*(1+0.3*int(actTurn.char.element != ELEMENT_LIGHT))), danger=danger, effIfFail=lunaVulne, fromEnt=tablEntTeam[1][0])[0]
                                    break
                            if temp == "":
                                temp = f"\n{actTurn.char.name} est étourdi{actTurn.accord()} !\n"
                        else:
                            temp = f"\n{actTurn.char.name} est étourdi{actTurn.accord()} !\n"
                        tempTurnMsg += temp
                        logs += "{0} is stun\n".format(actTurn.name)
                        optionChoice = OPTION_SKIP

                    funnyTempVarName, ressurected = "\n__Fin du tour__\n"+actTurn.endOfTurn(danger), [[],[]]
                    logs += funnyTempVarName
                    tempTurnMsg += funnyTempVarName
                    timeNow = (datetime.now() - nowStartOfTurn)/timedelta(microseconds=1000)
                    logs += "Turn duration : {0} ms{1}\n ----------".format(timeNow,[" (Manual fighter)",""][int(actTurn.auto)])
                    if timeNow > 500 and actTurn.auto:
                        longTurn = True
                        longTurnNumber.append({"turn":tour,"ent":actTurn.char.name,"duration":timeNow})

                    if not(auto):   # Sending the Turn message
                        tempTurnMsg = reducedEmojiNames(tempTurnMsg)
                        if len(tempTurnMsg) > 4096:
                            tempTurnMsg = unemoji(tempTurnMsg)
                            if len(tempTurnMsg) > 4096:
                                tempTurnMsg = "OVERLOAD"

                        nbTry = 0
                        while 1:
                            emby = interactions.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color)
                            if footerText != "":
                                emby.set_footer(text=footerText,icon_url=ctx.author.avatar_url)
                            try:
                                if optionChoice == OPTION_SKILL and skillToUse.url != None:
                                    emby.set_image(url=skillToUse.url)
                                    await msg.edit(embeds = [embInfo,emby]+choiceEmbed,components=[infoSelect])
                                else:
                                    await msg.edit(embeds = [embInfo,emby]+choiceEmbed,components=[infoSelect])
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

                        if type(actTurn.char) not in [invoc, depl]:
                            await asyncio.sleep(2-([0,0.5][int(bigMap or not(allAuto))])+(min(len(tempTurnMsg),2500)/2500*5))
                        else:
                            await asyncio.sleep(1+(min(len(tempTurnMsg),3500)/3500*5))

                    # POTG
                    potgValue = (None,0)
                    for team in (0,1):
                        for ent in tablEntTeam[team]:
                            tempPotgValue = (ent.stats.damageDeal-potgDamages[team][ent.id])*0.7+(ent.stats.ennemiKill-potgKills[team][ent.id])*ent.char.level*10+(ent.stats.heals-potgHeal[team][ent.id])*0.6+(ent.stats.allieResurected-potgRaises[team][ent.id])*ent.char.level*15+(ent.stats.armoredDamage-potgArmored[team][ent.id])*0.7+200*int(optionChoice==OPTION_SKILL and skillToUse.id == "lb")-1000*int(type(actTurn.char)==octarien)
                            if tempPotgValue > potgValue[1]:
                                potgValue = (ent,tempPotgValue)

                    if potgValue[1] > playOfTheGame[0]:
                        if optionChoice == OPTION_SKILL and skillToUse.url != None:
                            playOfTheGame = [potgValue[1],potgValue[0],interactions.Embed(title=f"__Action du combat\nTour {tour}__",description=tempTurnMsg,color = potgValue[0].char.color).set_image(url=skillToUse.url)]
                        else:
                            playOfTheGame = [potgValue[1],potgValue[0],interactions.Embed(title=f"__Action du combat\nTour {tour}__",description=tempTurnMsg,color = potgValue[0].char.color)]

                        if getEmbedLength(playOfTheGame[2]) > 4000:
                            playOfTheGame[2] = interactions.Embed(title=f"__Action du combat\nTour {tour}__",description=unemoji(tempTurnMsg),color = potgValue[0].char.color)
                            if getEmbedLength(playOfTheGame[2]) > 4000:
                                tempVeryCut, tempLine = "", ""
                                for letter in tempTurnMsg:
                                    if letter == "\n":
                                        if "\"" not in tempLine and "rejoue son tour" not in tempLine:
                                            tempVeryCut += tempLine + "\n"
                                        tempLine = ""
                                    else:
                                        tempLine += letter
                                if "\"" not in tempLine:
                                    tempVeryCut += tempLine
                                playOfTheGame[2] = interactions.Embed(title=f"__Action du combat\nTour {tour}__",description=tempVeryCut,color = potgValue[0].char.color)
                                if getEmbedLength(playOfTheGame[2]) > 4000 :
                                    tempVeryCut = '(...)\n'+tempVeryCut[-4000:]
                                    playOfTheGame[2] = interactions.Embed(title=f"__Action du combat\nTour {tour}__",description=tempVeryCut,color = potgValue[0].char.color)

                # =========================================

                # End of the turn - timeline stuff ------------------------------------------------------------------
                tablEntTeam,tablAliveInvoc = time.endOfTurn(tablEntTeam,tablAliveInvoc)

                for team in [0,1]:                      # Does a team is dead ?
                    for ent in tablEntTeam[team]:
                        if ent.hp > 0 and type(ent.char) not in [invoc, depl]:
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
            fileName="ERROR_{0}_{1}.txt".format(ctx.author.name,date)
            fich = open("./data/fightLogs/{0}".format(fileName),"w",encoding='utf-8')
            if not(isLenapy):
                try:
                    fich.write(unemoji(logs))
                except:
                    print_exc()

            else:
                fich.write(unemoji(logs))
            fich.close()
            opened = open("./data/fightLogs/{0}".format(fileName),"rb")
            await asyncio.sleep(1)
            desc = format_exc().replace("^","")
            for letter in ["*","_"]:
                desc = desc.replace(letter,"\{0}".format(letter))

            desc += "\n__Variables :__\n__ActTurn :__ "
            try:
                desc += actTurn.char.name
            except:
                desc += ":x:"
            desc += "\n__SkillToUse :__ "
            try:
                desc += skillToUse.name
            except:
                desc += ":x:"
            desc += "\n__Ennemi :__ "
            try:
                desc += ennemi.char.name
            except:
                desc += ":x:"

            try:
                await ctx.send(content="{0} : Une erreur est survenue".format(ctx.author.mention),files =interactions.File(filename=fileName,fp=opened),embeds=interactions.Embed(title=["Descriptif de l'erreur","Une erreur de communication prolongée est survenue"]["aiohttp.client_exceptions.ClientOSError: [Errno 104] Connection reset by peer" in logs],description=desc))
            except:
                await ctx.channel.send(files=interactions.File(filename=fileName,fp=opened),embeds=interactions.Embed(title=["Une erreur est survenue durant le combat","Une erreur de communication prolongée est survenue"]["aiohttp.client_exceptions.ClientOSError: [Errno 104] Connection reset by peer" in logs],description=desc))
            opened.close()

            if isLenapy:
                chan = await get(bot, interactions.Channel, parent_id = 912137828614426704, object_id=808394788126064680)
                opened = open("./data/fightLogs/ERROR_{0}_{1}.txt".format(ctx.author.name,date),"rb")
                await asyncio.sleep(1)
                await chan.send("Une erreur est survenue durant le combat",files =interactions.File(filename=fileName,fp=opened))
                opened.close()
            haveError = True
        # ===============================================================================================
        #                                       Post Fight Things
        # ===============================================================================================
        if not(haveError):
            print(ctx.author.name + " a fini son combat")
            startMsg = not(globalVar.getRestartMsg()) and not(waitEnd)

            if not(everyoneDead[1] and everyoneDead[0]):        # The winning team. 0 -> Blue, 1 -> Red
                winners, nullMatch = int(not(everyoneDead[1])), False
            else:
                winners, nullMatch = 1, True

            if not(octogone and team2[0].isNpc('Lena') and len(team2) == 1 and not(winners)):               # None Special fights
                for z in (0,1):
                    for a in tablEntTeam[z]:
                        if type(a.char) == invoc:
                            a.hp = 0

                tablEntTeam,tablAliveInvoc = time.endOfTurn(tablEntTeam,tablAliveInvoc) 
                for deplEnt in deplTabl:
                    for cmpt in range(len(tablEntTeam[deplEnt[0].team])):
                        if tablEntTeam[deplEnt[0].team][cmpt].id == deplEnt[0].summoner.id:
                            tablEntTeam[deplEnt[0].team][cmpt].stats.damageDeal = tablEntTeam[deplEnt[0].team][cmpt].stats.damageDeal+deplEnt[0].stats.damageDeal
                            tablEntTeam[deplEnt[0].team][cmpt].stats.indirectDamageDeal = tablEntTeam[deplEnt[0].team][cmpt].stats.indirectDamageDeal+deplEnt[0].stats.indirectDamageDeal
                            tablEntTeam[deplEnt[0].team][cmpt].stats.ennemiKill = tablEntTeam[deplEnt[0].team][cmpt].stats.ennemiKill+deplEnt[0].stats.ennemiKill
                            tablEntTeam[deplEnt[0].team][cmpt].stats.heals = tablEntTeam[deplEnt[0].team][cmpt].stats.heals+deplEnt[0].stats.heals
                            tablEntTeam[deplEnt[0].team][cmpt].stats.shieldGived = tablEntTeam[deplEnt[0].team][cmpt].stats.shieldGived+deplEnt[0].stats.shieldGived
                            tablEntTeam[deplEnt[0].team][cmpt].stats.summonDmg = tablEntTeam[deplEnt[0].team][cmpt].stats.summonDmg + deplEnt[0].stats.damageDeal + deplEnt[0].stats.indirectDamageDeal
                            tablEntTeam[deplEnt[0].team][cmpt].stats.summonHeal = tablEntTeam[deplEnt[0].team][cmpt].stats.summonHeal + deplEnt[0].stats.shieldGived + deplEnt[0].stats.heals
                            break

                temp = tablEntTeam[0][:]+tablEntTeam[1][:]

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
                suppClass = sorted(temp,key=lambda student: student.stats.damageBoosted + student.stats.damageDodged,reverse=True)
                for a in suppClass[:]:
                    if a.stats.damageBoosted + a.stats.damageDodged < 1:
                        suppClass.remove(a)

                listClassement = [dptClass,healClass,shieldClass,suppClass]

                tablSays = []
                temp = ["",""]
                endResultRep, teamWon, nbTeamMates, truePlayer = {}, {}, {}, 0
                for ent in tablEntTeam[0]:
                    if type(ent.char) == char and ent.char.team == mainUser.team:
                        truePlayer += 1
                for a in [0,1]:             # Result msg character showoff
                    for b in tablEntTeam[a]:
                        raised, actIcon, icon = "", b.icon, await b.getIcon(bot)
                        if b.status == STATUS_RESURECTED and b.raiser != None:
                            raised = " ({1}{0})".format(b.raiser,['<:rezB:907289785620631603>','<:rezR:907289804188819526>'][b.team])
                        elif b.status == STATUS_TRUE_DEATH and b.raiser != None:
                            raised = " ({0})".format(['<:diedTwiceB:907289950301601843>','<:diedTwiceR:907289935663485029>'][b.team])

                        
                        nbLB, nbSummon = "",""
                        if b.stats.nbLB > 1:
                            nbLB = "(<:lb:886657642553032824>x{0})".format(b.stats.nbLB)
                        elif b.stats.nbLB == 1:
                            nbLB = "(<:lb:886657642553032824>)"
                        if b.stats.nbSummon > 0:
                            nbSummon = "(<:carbi:884899235332522016>x{0})".format(b.stats.nbSummon)

                        addText = b.getMedals(listClassement)+raised+nbLB+nbSummon
                        if addText != "":
                            addText = " "+addText
                        resultMsg = "{0} {1}{2}\n".format(actIcon,b.char.name,addText)
                        
                        if type(b.char) != tmpAllie or b.team == 1:
                            try:
                                endResultRep[b.char.team] += resultMsg
                                nbTeamMates[b.char.team] += 1
                            except KeyError:
                                endResultRep[b.char.team] = resultMsg
                                teamWon[b.char.team] = (not(winners) and b.team == 0) or (winners and b.team == 1)
                                nbTeamMates[b.char.team] = 1
                        else:
                            try:
                                if truePlayer < 8:
                                    teamToSee = mainUser.team
                                    truePlayer += 1
                                else:
                                    teamToSee = -1
                                    for teamIndex in endResultRep:
                                        if teamIndex not in [-2, mainUser.team]:
                                            teamToSee = teamIndex
                                            break
                            except KeyError:
                                if truePlayer < 8:
                                    teamToSee = mainUser.team
                                else:
                                    teamToSee = -1

                            try:
                                endResultRep[teamToSee] += resultMsg
                                nbTeamMates[teamToSee] += 1
                            except KeyError:
                                endResultRep[teamToSee] = resultMsg
                                teamWon[teamToSee] = (not(winners) and b.team == 0) or (winners and b.team == 1)
                                nbTeamMates[teamToSee] = 1

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

                say = ""
                if len(tablSays) > 1:
                    say = "\n\n{0}".format(tablSays[random.randint(0,len(tablSays)-1)])
                elif len(tablSays) == 1:
                    say = "\n\n{0}".format(tablSays[0])
        
                duree = datetime.now()
                nowTemp = duree - now
                nowTemp = str(nowTemp.seconds//60) + ":" + str(nowTemp.seconds%60)

                if not(octogone):       # Add the "next fight" field
                    nextFigth = now + timedelta(hours=1+(2*auto)) + horaire
                    nextFightMsg = "\n__Prochain combat {0}__ : {1}".format(["normal","rapide"][auto],nextFigth.strftime("%Hh%M"))
                else:
                    nextFightMsg = ""

                if not(nullMatch):
                    color = [[0x2996E5,0x00107D][danger<100],red][winners]
                else:
                    color = 0x818181

                resultEmbed = interactions.Embed(title = "__Résultats du combat :__",color = color,description="__Danger :__ {0}\n__Nombre de tours :__ {1}\n__Durée :__ {2}{4}{3}".format(danger,tour,nowTemp,say,nextFightMsg))

                for indexTeam in endResultRep:
                    if len(endResultRep[indexTeam]) > 1024:
                        temp, temp2, haveStarted = "", "", False
                        for letter in endResultRep[indexTeam]:
                            if letter == "\n":
                                temp += temp2+letter
                                temp2, haveStarted = "", False
                            elif letter in ["(",")"]:
                                haveStarted = not(haveStarted)
                            elif not(haveStarted):
                                temp2+=letter
                        
                        if len(temp2)>0 and temp2[-1] != "\n":
                            temp += temp2
                        endResultRep[indexTeam] = temp

                for indexTeam in endResultRep:
                    if teamWon[indexTeam]:
                        resultEmbed.add_field(name="<:empty:866459463568850954>\n__Vainqueurs :__",value=endResultRep[indexTeam],inline=True)
                for indexTeam in endResultRep:
                    if not(teamWon[indexTeam]):
                        resultEmbed.add_field(name="<:empty:866459463568850954>\nPerdants :",value=endResultRep[indexTeam],inline=True)
                if footerText != "":
                    resultEmbed.set_footer(text=footerText,icon_url=ctx.author.avatar_url)

                if longTurn:
                    resultEmbed.set_footer(text="{0} tour{1} anormalement long{1} {2} été détecté{1} durant le combat. Un rapport va être envoyé".format(len(longTurnNumber),["",'s'][int(len(longTurnNumber) > 1)],["a","ont"][int(len(longTurnNumber) > 1)]))

                endOfFightStats = copy.deepcopy(tablEntTeam)
                if procurFight:
                    team1 = []
                    user = loadCharFile("./userProfile/{0}.prof".format(ctx.author.id))
                    if user.team != 0:
                        for a in userTeamDb.getTeamMember(user.team):
                            team1 += [loadCharFile(absPath + "/userProfile/{0}.prof".format(a))]
                    else:
                        team1 = [user]

                    tablEntTeam[0], cmpt = [], 0
                    for user in team1:
                        tablEntTeam[0].append(entity(cmpt,user,0,danger=danger,dictInteraction=dictIsNpcVar))
                        cmpt+=1

                # Gain rolls and defenitions -------------------------------------------------
                if not(octogone):
                    gainExp, gainCoins, allOcta, gainMsg, listLvlUp = tour,tour*20,True,"", []
                    # Base Exp Calculation
                    for ent in tablEntTeam[1]:
                        if type(ent.char) == octarien:
                            if ent.hp <= 0:
                                gainExp += ent.char.exp
                            elif ent.status == STATUS_RESURECTED:
                                gainExp += int(ent.char.exp/2)
                        elif type(ent.char) == tmpAllie:
                            if ent.hp <= 0:
                                gainExp += 10
                            elif ent.status == STATUS_RESURECTED:
                                gainExp += 5
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

                    for ent in tablEntTeam[0]: #Attribution de l'exp et loot
                        tempLevel = tablEntTeam[0][:]
                        tempLevel.sort(key=lambda sorting : sorting.char.level, reverse=True)
                        maxLevlDiff = tempLevel[0].char.level - tempLevel[len(tempLevel)-1].char.level
                        if type(ent.char) == char and ent.char.team == mainUser.team:
                            ent.char = loadCharFile(user=ent.char)
                            veryLate = 1 + (int(maxLevel-ent.char.level > 10 and winners) * 0.5)
                            if ent.char.level < 55:
                                baseGain = gainExp+(ent.medals[0]*3)+(ent.medals[1]*2)+(ent.medals[2]*1)+int((maxLevel-ent.char.level)/2)
                            else:
                                baseGain = 0
                            effectiveExpGain = int(baseGain*(1+0.02*(min(10,maxLevel-ent.char.level)))*veryLate*[1,1.5][ent.char.stars > 0 and ent.char.level <=30] * (1+(maxLevlDiff <= 5 * 0.2)+(ent.auto*0.1)) // [1,2][winners or nullMatch])
                            temp = (ent.char.level, ent.char.stars)

                            ent.char = await addExpUser(bot,ent.char,ctx,exp=effectiveExpGain,coins=gainCoins,send=False)

                            if (ent.char.level, ent.char.stars) != temp:
                                listLvlUp.append("{0} : Niv. {1}{2} → Niv. {3}{4}\n".format(await ent.getIcon(bot),temp[0],["","<:littleStar:925860806602682369>{0}".format(temp[1])][temp[1]>0],ent.char.level,["","<:littleStar:925860806602682369>{0}".format(ent.char.stars)][ent.char.stars>0]))

                            if effectiveExpGain > 0:
                                gainMsg += "\n{0} → <:exp:926106339799887892> +{1}".format(await getUserIcon(bot,ent.char),effectiveExpGain)

                            if baseGain != effectiveExpGain:
                                logs += "\n{0} got ent {1}% exp boost (total : +{2} exp)".format(ent.char.name,int((effectiveExpGain/baseGain-1)*100),effectiveExpGain)

                            userShop = userShopPurcent(ent.char)
                            stuffRoll, skillRoll = constStuffDrop[userShop//10*10], constSkillDrop[userShop//10*10]
                            if allOcta:             # Loots
                                if not(winners):
                                    if random.randint(0,99) < stuffRoll:                   # Drop Stuff
                                        logs += "\n{0} have loot :".format(ent.char.name)
                                        drop = listAllBuyableShop[:]
                                        for b in drop[:]:
                                            if ent.char.have(obj=b) or type(b) not in [classes.weapon,classes.stuff]:
                                                drop.remove(b)

                                        if len(drop) > 0:
                                            rand = drop[random.randint(0,len(drop)-1)]
                                            newTemp = whatIsThat(rand)
                                            logs += " {0}".format(rand.name)

                                            if newTemp == 0:
                                                ent.char.weaponInventory += [rand]
                                            elif newTemp == 2:
                                                ent.char.stuffInventory += [rand]

                                            saveCharFile(user=ent.char)
                                            usrIcon = await getUserIcon(bot,ent.char)
                                            if usrIcon in gainMsg:
                                                gainMsg += f", {rand.emoji} {rand.name}"
                                            else:
                                                gainMsg += "\n{0} → {1} {2}".format(usrIcon,rand.emoji,rand.name)

                                        elif len(drop) == 0:
                                            gainTabl = [5,35,50,69,11,100,150,666,111,13,1,256,128,64,32]

                                            for comp in ent.char.skills+ent.char.stuff:                             # Dans toutes les compétences du personnage + ses équipementd
                                                if type(comp) == skill and comp.name == "Truc pas catho":       # Si On sais quoi est équipé
                                                    gainTabl = [69]                                             # Tu peux gagner que 69 pièces
                                                    break
                                                elif type(comp) == stuff and comp.name == "Tenue Provocante":   # Sinon, si On sait quoi 2 est équipé
                                                    gainTabl = [69]                                             # Tu peux gagner que 69 pièces aussi
                                                    break

                                            gain = gainTabl[random.randint(0,len(gainTabl)-1)]
                                            logs += " {0} pièces".format(gain)
                                            ent.char.currencies += gain
                                            saveCharFile(user=ent.char)
                                            if await getUserIcon(bot,ent.char) in gainMsg:
                                                gainMsg += f", {gain} <:coins:862425847523704832>"
                                            else:
                                                gainMsg += "\n{0} → {1} <:coins:862425847523704832>".format(await getUserIcon(bot,ent.char),gain)

                                    if random.randint(0,99) < skillRoll:
                                        logs += "\n{0} have loot :".format(ent.char.name)
                                        drop = listAllBuyableShop[:]

                                        for b in drop[:]:
                                            if type(b) != classes.skill or ent.char.have(obj=b):
                                                drop.remove(b)

                                        if len(drop) > 0:
                                            rand = drop[random.randint(0,len(drop)-1)]
                                            ent.char.skillInventory += [rand]

                                            saveCharFile(user=ent.char)
                                            usrIcon = await getUserIcon(bot,ent.char)
                                            if usrIcon in gainMsg:
                                                gainMsg += f", {rand.emoji} {rand.name}"
                                            else:
                                                gainMsg += "\n{0} → {1} {2}".format(usrIcon,rand.emoji,rand.name)
                                            
                                            if ent.char.owner == mainUser.owner:
                                                gainMsg += "\n__{0}__ :\n{1}".format(rand.name,rand.getSummary())

                                        elif len(drop) == 0:
                                            gainTabl = [5,35,50,69,11,100,150,666,111,13,1,256,128,64,32]

                                            for comp in ent.char.skills+ent.char.stuff:                             # Dans toutes les compétences du personnage + ses équipementd
                                                if type(comp) == skill and comp.name == "Truc pas catho":       # Si On sais quoi est équipé
                                                    gainTabl = [69]                                             # Tu peux gagner que 69 pièces
                                                    break
                                                elif type(comp) == stuff and comp.name == "Tenue Provocante":   # Sinon, si On sait quoi 2 est équipé
                                                    gainTabl = [69]                                             # Tu peux gagner que 69 pièces aussi
                                                    break

                                            gain = gainTabl[random.randint(0,len(gainTabl)-1)]
                                            logs += " {0} pièces".format(gain)
                                            ent.char.currencies += gain
                                            saveCharFile(user=ent.char)
                                            if await getUserIcon(bot,ent.char) in gainMsg:
                                                gainMsg += f", {gain} <:coins:862425847523704832>"
                                            else:
                                                gainMsg += "\n{0} → {1} <:coins:862425847523704832>".format(await getUserIcon(bot,ent.char),gain)

                                    elif mainUser.owner == ent.char.owner:
                                        if random.randint(0,99) < (20-(10*int(userShop>80))-(10*int(userShop>95))):
                                            aliceStatsDb.updateJetonsCount(mainUser,1)
                                            logs += "\n{0} ent obtenu un jeton de roulette".format(mainUser.name)
                                            usrIcon = await getUserIcon(bot,ent.char)
                                            if usrIcon in gainMsg:
                                                gainMsg += f", <:jeton:917793426949435402> Jeton de roulette"
                                            else:
                                                gainMsg += "\n{0} → <:jeton:917793426949435402> Jeton de roulette".format(usrIcon)
                                elif userShop < 10:
                                    if random.randint(0,99) < constLooseStuffDrop[int(userShop//10)]:
                                        logs += "\n{0} have loot :".format(ent.char.name)
                                        drop = listAllBuyableShop[:]
                                        for b in drop[:]:
                                            if not(type(b) in [classes.weapon,classes.stuff,classes.skill] and not(ent.char.have(obj=b))):
                                                if not(type(b) in [classes.weapon,classes.skill] or (type(b) == classes.stuff and b.minLvl < ent.char.level)):
                                                    drop.remove(b)

                                        if len(drop) > 0:
                                            rand = drop[random.randint(0,len(drop)-1)]
                                            newTemp = whatIsThat(rand)
                                            logs += " {0}".format(rand.name)

                                            if newTemp == 0:
                                                ent.char.weaponInventory += [rand]
                                            elif newTemp == 1:
                                                ent.char.stuffInventory += [rand]                                            
                                            elif newTemp == 2:
                                                ent.char.stuffInventory += [rand]

                                            saveCharFile(user=ent.char)
                                            usrIcon = await getUserIcon(bot,ent.char)
                                            if usrIcon in gainMsg:
                                                gainMsg += f", {rand.emoji} {rand.name}"
                                            else:
                                                gainMsg += "\n{0} → {1} {2}".format(usrIcon,rand.emoji,rand.name)

                                        elif len(drop) == 0:
                                            gainTabl = [5,35,50,69,11,100,150,666,111,13,1,256,128,64,32]

                                            for comp in ent.char.skills+ent.char.stuff:                             # Dans toutes les compétences du personnage + ses équipementd
                                                if type(comp) == skill and comp.name == "Truc pas catho":       # Si On sais quoi est équipé
                                                    gainTabl = [69]                                             # Tu peux gagner que 69 pièces
                                                    break
                                                elif type(comp) == stuff and comp.name == "Tenue Provocante":   # Sinon, si On sait quoi 2 est équipé
                                                    gainTabl = [69]                                             # Tu peux gagner que 69 pièces aussi
                                                    break

                                            gain = gainTabl[random.randint(0,len(gainTabl)-1)]
                                            logs += " {0} pièces".format(gain)
                                            ent.char.currencies += gain
                                            saveCharFile(user=ent.char)
                                            if await getUserIcon(bot,ent.char) in gainMsg:
                                                gainMsg += f", {gain} <:coins:862425847523704832>"
                                            else:
                                                gainMsg += "\n{0} → {1} <:coins:862425847523704832>".format(await getUserIcon(bot,ent.char),gain)

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
                        await ctx.channel.send(embeds=interactions.Embed(title="__Montée de niveau__",color=light_blue,description="Le{0} personnage{0} suivant{0} {1} monté de niveau !\n".format(["","s"][len(listLvlUp)>1],["a","ont"][len(listLvlUp)>1])+temp))

                if errorNb > 0:
                    resultEmbed.add_field(name="<:empty:866459463568850954>\nDebugg :",value="{0} erreurs de connexions ont survenu durant ce combat",inline=False)

            else:
                logs += mauvaisePerdante
                for team in listImplicadTeams:
                    teamWinDB.changeFighting(team,0)
                logs += "\n"+format_exc()
                date = datetime.now()
                date = date.strftime("%H_%M")
                fileName ="{0}_{1}.txt".format(ctx.author.name,date)
                fich = open("./data/{0}".format(fileName),"w",encoding='utf-8')
                if not(isLenapy):
                    try:
                        fich.write(unemoji(logs))
                    except:
                        print_exc()

                else:
                    fich.write(unemoji(logs))
                fich.close()
                opened = open("./data/{0}.txt".format(fileName),"rb")

                try:
                    msg = await ctx.send("Une erreur est survenue durant le combat",files =interactions.File(filename=fileName,fp=opened))
                except:
                    msg = await ctx.channel.send("Une erreur est survenue durant le combat",files =interactions.File(filename=fileName,fp=opened))

                opened.close()
                os.remove("./data/{0}_{1}.txt".format(ctx.author.name,date))
                haveError = True

            if not(haveError):
                if startMsg == 0:
                    await msg.edit(embeds = resultEmbed,components=[interactions.ActionRow(components=[interactions.Button(type=2, style=2, label="Chargement...", emoji=getEmojiObject('<a:loading:862459118912667678>'), custom_id="📄",disabled=True)])])
                else:
                    await msg.edit(embeds = resultEmbed,components=[])
                if not(octogone):
                    for team in listImplicadTeams:
                        teamWinDB.changeFighting(team,0)
            # ------------ Succès -------------- #
            if not(octogone):
                for team in [0,1]:
                    for ent in tablEntTeam[team]:
                        if type(ent.char) == char and ent.char.team == mainUser.team:
                            achivements = achivement.getSuccess(ent.char)
                            if not(ent.auto): # Ivresse du combat
                                ent.char = await achivements.addCount(ctx,ent.char,"fight")

                            tablAchivNpcName = ["Alice","Clémence","Akira","Gwendoline","Hélène","Icealia","Shehisa","Powehi","Félicité","Sixtine","Hina","Julie","Krys","Lio","Liu","Liz","Lia","Iliana","Stella","Kiku","Kitsune","Ailill","Altikia","Klironovia"]
                            tablAchivNpcCode = ["alice","clemence","akira","gwen","helene","icea","sram","powehi","feli","sixtine","hina","julie","krys","lio","liu","liz","lia","light","stella","kiku1","momKitsune","ailill2","alty","klikli"]

                            for cmpt in range(len(tablAchivNpcName)):
                                if dictIsNpcVar["{0}".format(tablAchivNpcName[cmpt])]: # Temp or enemy presence sussesss
                                    ent.char = await achivements.addCount(ctx,ent.char,tablAchivNpcCode[cmpt])

                            if dictIsNpcVar["Iliana"] and (dictIsNpcVar["Luna"] or dictIsNpcVar["Shihu"]):
                                ent.char = await achivements.addCount(ctx,ent.char,"lightNShadow")
                            if dictIsNpcVar["Luna"] or dictIsNpcVar["Shihu"]:
                                ent.char = await achivements.addCount(ctx,ent.char,"fullDark")
                            if tablEntTeam[1][0].isNpc("Luna ex."):
                                ent.char = await achivements.addCount(ctx,ent.char,"luna")
                            if tablEntTeam[1][0].isNpc("Clémence pos."):
                                ent.char = await achivements.addCount(ctx,ent.char,"clemMem")

                            # Act achivements
                            tablStatToSee = [ent.stats.headnt,ent.stats.sufferingFromSucess,ent.stats.lauthingAtTheFaceOfDeath]
                            tablCode = ["ailill","suffering","kiku2"]
                            for cmpt in range(len(tablStatToSee)):
                                if tablStatToSee[cmpt]:
                                    ent.char = await achivements.addCount(ctx,ent.char,tablCode[cmpt])

                            if ent.stats.friendlyfire > 0:
                                ent.char = await achivements.addCount(ctx,ent.char,"fratere")


                            if auto and int(ctx.author.id) == int(ent.char.owner): # Le temps c'est de l'argent
                                ent.char = await achivements.addCount(ctx,ent.char,"quickFight")

                            # Je ne veux pas d'écolière pour défendre nos terres
                            ent.char = await achivements.addCount(ctx,ent.char,"school")

                            # Elementaire
                            if ent.char.level >= 10:
                                ent.char = await achivements.addCount(ctx,ent.char,"elemental")

                            if not(winners) and ent.healResist >= 80 and ent.hp > 0:
                                ent.char = await achivements.addCount(ctx,ent.char,"dangerous")

                            if not(winners) and ent.stats.fullskip:
                                ent.char = await achivements.addCount(ctx,ent.char,"still")

                            if winners and danger == (dangerLevel[0] + (starLevel * DANGERUPPERSTAR)):
                                ent.char = await achivements.addCount(ctx,ent.char,"loose")

                            # Dimentio
                            if ent.char.level >= 20:
                                ent.char = await achivements.addCount(ctx,ent.char,"dimentio")

                            # Soigneur de compette
                            ent.char = await achivements.addCount(ctx,ent.char,"greatHeal",ent.stats.heals)

                            # La meilleure défense c'est l'attaque
                            ent.char = await achivements.addCount(ctx,ent.char,"greatDps",ent.stats.damageDeal-ent.stats.indirectDamageDeal)

                            # Notre pire ennemi c'est nous même
                            ent.char = await achivements.addCount(ctx,ent.char,"poison",ent.stats.indirectDamageDeal)

                            # Savoir utiliser ses atouts
                            ent.char = await achivements.addCount(ctx,ent.char,"estialba",int(ent.stats.estialba))

                            # Il faut que ça sorte
                            ent.char = await achivements.addCount(ctx,ent.char,"lesath",int(ent.stats.bleeding))

                            if ent in dptClass[:3] and ent.stats.indirectDamageDeal == ent.stats.damageDeal:
                                ent.char = await achivements.addCount(ctx,ent.char,"dirty")
                            if ent == dptClass[0] and ent.stats.ennemiKill == 0:
                                ent.char = await achivements.addCount(ctx,ent.char,"delegation")

                            aliceStatsDb.addStats(ent.char,ent.stats)
                            saveCharFile(absPath + "/userProfile/"+str(ent.char.owner)+".prof",ent.char)

            timeout = False
            date, actuTeam, actuEntity, started, prec, logsAff = datetime.now()+horaire,0,0,False,None,False
            date = date.strftime("%H%M")
            fich = open("./data/fightLogs/{0}_{1}.txt".format(ctx.author.name,date),"w",encoding='utf-8')
            if not(isLenapy):
                try:
                    fich.write(unemoji(logs))
                except:
                    print_exc()
            else:
                fich.write(unemoji(logs))
            fich.close()

            def check(m):
                return m.message.id == msg.id

            logsButton = interactions.Button(type=2, style=2, label="Voir les logs", emoji=Emoji(name="📄"),custom_id="📄")
            potgMsg = None

            if longTurn:
                for team in listImplicadTeams:
                    teamWinDB.changeFighting(team,0)
                logs += "\n"+format_exc()
                date = datetime.now()+horaire
                date = date.strftime("%H%M")
                fileName = "{0}_{1}.txt".format(ctx.author.name,date)
                fich = open("./data/fightLogs/{0}".format(fileName),"w",encoding='utf-8')
                if not(isLenapy):
                    try:
                        fich.write(unemoji(logs))
                    except:
                        print_exc()

                else:
                    fich.write(unemoji(logs))
                fich.close()
                opened = open("./data/fightLogs/{0}".format(fileName),"rb")
                await asyncio.sleep(1)

                chan = await get(bot, interactions.Channel, parent_id = 912137828614426704, object_id=808394788126064680)

                desc = ""
                for temp in longTurnNumber:
                    desc += "Tour : {0} - {1} ({2} ms)\n".format(temp["turn"],temp["ent"],temp["duration"])

                await chan.send("Un tour anormalement long a été détecté sur ce combat :",files =interactions.File(filename=fileName,fp=opened),embeds=interactions.Embed(title="__Tours mis en causes :__",description=desc))
                opened.close()

            potgIcon = None
            potg = []

            if playOfTheGame[1] != None:
                try:
                    potgIcon = await playOfTheGame[1].getIcon(bot)
                    potg = [interactions.ActionRow(components=[interactions.Button(type=2, style=2, label="Action du combat", emoji=getEmojiObject(potgIcon),custom_id="potg")])]
                except:
                    pass

            if not(octogone):           # Add result to streak
                    teamWinDB.addResultToStreak(mainUser,not(everyoneDead[0]))
            if isLenapy and not(octogone):
                teamWinDB.refreshFightCooldown(mainUser.team,auto,fromTime=now)
            while startMsg: # Tableau des statistiques
                options = []
                for team in [0,1]:
                    for num in range(len(endOfFightStats[team])):
                        ent = endOfFightStats[team][num]
                        options.append(interactions.SelectOption(label=ent.name,value="{0}:{1}".format(team,num),emoji=getEmojiObject(await ent.getIcon(bot)),default=started and team == actuTeam and num == actuEntity))

                select = interactions.SelectMenu(custom_id = "seeFighterStats", options=options, placeholder="Voir les statistiques d'un combattant")
                await msg.edit(embeds = resultEmbed, components=[interactions.ActionRow(components=[select]),interactions.ActionRow(components=[logsButton])]+potg)

                try:
                    interact: ComponentContext = await bot.wait_for_component(msg,check=check,timeout=[0,180][waitEnd])
                except asyncio.TimeoutError:
                    toAff = []
                    if logsAff:
                        toAff.append(interactions.ActionRow(components=[logsButton]))
                    if potgMsg != None:
                        toAff.append(interactions.ActionRow(components=[interactions.Button(type=2, style=ButtonStyle.URL,label="Action du combat",emoji=getEmojiObject(playOfTheGame[1].icon),url=potgMsg.jump_url)]))

                    await msg.edit(embeds = resultEmbed, components=toAff)
                    if prec != None:
                        await prec.delete()
                    return 1


                if interact.data.component_type == 2:
                    if interact.custom_id == "📄":
                        opened = open("./data/fightLogs/{0}".format(fileName),"rb")
                        logsMsg = await interact.send("`Logs, {0} à {1}:{2}`".format(ctx.author.name,date[0:2],date[-2:]),files =interactions.File(filename=fileName,fp=opened))
                        opened.close()
                        logsButton = interactions.Button(type=2, style=ButtonStyle.URL,label="Voir les logs",emoji=Emoji(name="📄"),url=logsMsg.jump_url)
                        logsAff = True
                    else:
                        emb: Embed = playOfTheGame[2]
                        emb.set_footer(icon_url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(potgIcon).id),text="Action du combat")
                        potgMsg = await interact.send(embeds = emb)
                        print(potgMsg.url)
                        potg = []
                else:
                    inter = interact.data.values[0]
                    haveTriggered = False
                    actuTeam,actuEntity = "",""
                    for letter in inter:
                        if letter != ":" and not(haveTriggered):
                            actuTeam += letter
                        elif letter != ":":
                            actuEntity += letter
                        else:
                            haveTriggered = True
                    actuTeam,actuEntity = int(actuTeam),int(actuEntity)
                    actu = endOfFightStats[actuTeam][actuEntity]
                    
                    if prec != None:
                        await prec.edit(embeds = await getResultScreen(bot,actu))
                    else:
                        prec = await interact.send(embeds = await getResultScreen(bot,actu))
                    started = True    
            return not(winners)
    except:
        emby = interactions.Embed(title="__Uncatch error raised__",description=format_exc().replace("*",""))
        try:
            if footerText != "":
                emby.set_footer(text=footerText,icon_url=ctx.author.avatar_url)
        except:
            pass
        if msg == None:
            await ctx.channel.send(embeds=emby,components=[])
        else:
            await msg.edit(embeds=emby,components=[])

        teamWinDB.changeFighting(mainUser.team,0)