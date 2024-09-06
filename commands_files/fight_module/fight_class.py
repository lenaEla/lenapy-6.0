from classes import *

class timeline:
    """Classe de la timeline"""
    def __init__(self):
        self.timeline = []
        self.initTimeline = []
        self.begin = None
        entDict = {}

    def init(self,tablEntTeam : list,entDict):
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

                if (suppSkillsCount >= 3 and random.randint(0,99)<50) or (ent.char.weapon.range == RANGE_MELEE and random.randint(0,99)<33) or not(ent.auto):
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
        entDict = entDict

        return self, tablEntTeam

    def getActTurn(self):
        return self.timeline[0]

    def icons(self):
        temp, duplicateList = "", []
        
        alreadySeen = []
        for icn in self.timeline:
            if icn.icon not in alreadySeen:
                alreadySeen.append(icn.icon)
            elif icn.icon not in duplicateList and type(icn.char) not in [classes.invoc, classes.octarien]:
                duplicateList.append(icn.icon)

        for a in self.timeline:
            temp += "{0}{2} {1} ".format(a.icon,["←","<|-"][a == self.initTimeline[-1]],["","{0}".format(["🔹","🔺"][a.team])][a.icon in duplicateList])
        return temp

    def endOfTurn(self,tablEntTeam,tablAliveInvoc,entDict):
        timelineTempo = self.timeline
        actTurn = timelineTempo[0]

        timelineTempo.remove(actTurn)
        timelineTempo.append(actTurn)

        for ent in self.timeline[:]:
            if ent.hp <= 0 and type(ent.char) == invoc:
                inv = ent
                timelineTempo.remove(inv)
                inv.cell.on = None
                tablEntTeam[inv.team].remove(inv)
                tablAliveInvoc[inv.team] -= 1

        self.timeline = timelineTempo
        return tablEntTeam, tablAliveInvoc, entDict

    def insert(self,entBefore,entToInsert):
        try:
            whereToInsert = self.timeline.index(entBefore) + 1
        except ValueError:
            print("Havn't found the entity")
            found, whereToInsert = False, 1
            for cmpt in range(len(self.timeline)):
                if entBefore.id == self.timeline[cmpt].id and type(self.timeline[cmpt].char) not in [invoc, depl]:
                    for cmpt2 in range(len(self.timeline[cmpt+1:])):
                        if self.timeline[cmpt+1:][cmpt2].id != entBefore.id and type(self.timeline[cmpt+1:][cmpt2].char) not in [invoc, depl]:
                            whereToInsert, found = cmpt+cmpt2, True
                            break
                    if found:
                        break
                if found:
                    break

        self.timeline.insert(whereToInsert,entToInsert)

class entity:
	"""Base class for the entities"""
	def __init__(self, identifiant : int, character : Union[char,tmpAllie,octarien,invoc,depl], team : int, player=True, auto=True, danger=100, summoner=None, tablEntTeam:List[list] = None):
		"""
			Parameters :\n
			.identifiant : A unique identifiant for a entity. Between ``0`` and ``15``
				-> A summon share the same id than his summoner
			.character : A ``Char, TmpAllie`` or ``octarien`` object. The entity is generated from this parameter
			.team : The team of the entity. ``0`` for the Blue Team, ``1`` for the Red Team
			.player : Does the entity is a player ? Default ``True`` (Where this is use ?)
			.auto : Does the entity is a manual or a automatic player ? Default ``True`` (Automatic)
			.danger : A ``int`` use for uping the entity hp if it's a ``octarien``. Default ``100``
			.summoner : The summoner of the entity. ``None`` if the entity isn't a summon, and by default
		"""
		self.id = identifiant
		if tablEntTeam == None:
			if summoner == None: raise AttributeError("No tablEntTeam attribut on a none summon type entity")
			else: self.tablEntTeam = summoner.tabl
		
		self.tablEntTeam = tablEntTeam
		self.char = character
		self.team = team
		self.type = player
		self.auto = auto
		self.weapon = self.char.weapon
		self.chained = False
		self.rawResist, self.rawPercing = 0,0
		self.leftTurnAlive = 999
		self.raiser = None
		self.chipAddInfo = [None,None,None,None,None]
		if summoner != None and type(summoner.char) in [invoc,depl]: summoner = summoner.summoner
		self.summoner = summoner
		if type(self.char) == invoc:
			self.leftTurnAlive = self.char.lifeTime
			self.char.equippedChips, self.char.chipInventory = copy.deepcopy(self.summoner.char.equippedChips), self.summoner.char.chipInventory
			for indx, tmpChipId in enumerate(self.char.equippedChips):
				tmpChip = getChip(tmpChipId)
				if tmpChip != None and (tmpChip.rarity >= RARITY_LEGENDARY or tmpChip.name in ["Médaille de la Chauve-Souris","Haut-Perceur 5.1","Cadeau Explosif"]):
					self.char.equippedChips[indx] = None
		elif type(self.char) == depl:
			self.leftTurnAlive = max(1,self.char.lifeTime)
			self.char.element, self.char.secElement, self.char.aspiration, self.char.level, self.char.stars = self.summoner.char.element, self.summoner.char.secElement, self.summoner.char.aspiration, self.summoner.char.level, self.summoner.char.stars
			self.char.species = self.summoner.char.species
			self.char.chipInventory, self.chipAddInfo = self.summoner.char.chipInventory, self.summoner.chipAddInfo

		self.status = [STATUS_ALIVE,STATUS_RESURECTED][self.char.npcTeam == NPC_UNDEAD]
		self.addSkill, self.addCd = [None], [0]

		if type(character) not in [invoc, depl]: self.icon = character.icon
		else: self.icon = character.icon[team]

		self.stun = False
		self.silent = False
		self.specialVars = []
		self.effects: List[fightEffect] = []
		self.ownEffect = []
		self.cell = None

		self.strength, self.endurance, self.charisma, self.agility, self.precision, self.intelligence, self.magie = 0,0,0,0,0,0,0
		self.resistance, self.percing, self.critical = 0,0,0
		self.negativeHeal, self.negativeBoost, self.negativeShield, self.negativeDirect, self.negativeIndirect = 0,0,0,0,0
		self.ressurectable = False
		self.skills: List[classes.skill] = self.char.skills
		self.clemBloodJauge, self.aspiSlot = None, None

		if type(self.char) != depl: # Skill Verif
			tmpList = []
			for tmpSkill in self.skills:
				if type(tmpSkill) == classes.skill or type(findSkill(tmpSkill)) == classes.skill: tmpList.append(tmpSkill)
			self.skills = tmpList
			self.cooldowns = list(range(max(len(self.skills),7)))
			for indx, tmpSkill in enumerate(self.skills):
				try:
					if type(tmpSkill) == skill:
						if self.char.element == ELEMENT_SPACE:
							for cmpt in range(len(horoSkills)):
								if tmpSkill == horoSkills[cmpt]:
									tmpSkill = altHoroSkillsTabl[cmpt]
						self.cooldowns[indx] = int(tmpSkill.ultimate)*2+tmpSkill.initCooldown
				except: self.skills.append(None)
		else:
			self.cooldowns = [0,0,0,0,0,0,0]
			self.effects, self.specialVars = [], []
			self.effects, self.specialVars = entDict[self.summoner.id].effects, entDict[self.summoner.id].specialVars

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
		if type(self.char) not in [depl,invoc]: self.level = self.char.level
		else: self.level = self.summoner.level
		self.dmgUp, self.critDmgUp, self.healUp, self.critHealUp = 0,0,0,0
		self.dodge = 0
		self.dualCast = None

		self.init_stats()
		self.counterOnDodge, self.counterOnBlock = 0, 0

		if type(self.char) == invoc:
			nonlocal logs
			logs += "\n[Summon : {0}]\n[Stats : {1}]\n".format(self.name,self.baseStats)

	def init_stats(self):
		if type(self.char) not in [invoc, depl]:
			baseStats = {STRENGTH:self.char.strength+self.char.majorPoints[0],ENDURANCE:self.char.endurance+self.char.majorPoints[1],CHARISMA:self.char.charisma+self.char.majorPoints[2],AGILITY:self.char.agility+self.char.majorPoints[3],PRECISION:self.char.precision+self.char.majorPoints[4],INTELLIGENCE:self.char.intelligence+self.char.majorPoints[5],MAGIE:self.char.magie+self.char.majorPoints[6],RESISTANCE:self.char.resistance+self.char.majorPoints[7],PERCING:self.char.percing+self.char.majorPoints[8],CRITICAL:self.char.critical+self.char.majorPoints[9],10:self.char.majorPoints[10],11:self.char.majorPoints[11],12:self.char.majorPoints[12],13:self.char.majorPoints[13],14:self.char.majorPoints[14]}

			for obj in [self.char.weapon,self.char.stuff[0],self.char.stuff[1],self.char.stuff[2]]:
				valueElem = 1
				if obj.affinity == self.char.element : valueElem = 1.1

				if type(self.char) == octarien and self.team == 1: dangerMul = (100 + (20*((danger-100)/50)))/100
				else: dangerMul = 1

				baseStats[0] += int(obj.strength*valueElem*dangerMul)
				baseStats[1] += int(obj.endurance*valueElem*dangerMul)
				baseStats[2] += int(obj.charisma*valueElem*dangerMul)
				baseStats[3] += int(obj.agility*valueElem*dangerMul)
				baseStats[4] += int(obj.precision*valueElem*dangerMul)
				baseStats[5] += int(obj.intelligence*valueElem*dangerMul)
				baseStats[6] += int(obj.magie*valueElem*dangerMul)
				baseStats[7] += int(obj.resistance*valueElem)
				baseStats[8] += int(obj.percing*valueElem)
				baseStats[9] += int(obj.critical*valueElem)
				baseStats[10] += int(obj.negativeHeal)
				baseStats[11] += int(obj.negativeBoost)
				baseStats[12] += int(obj.negativeShield)
				baseStats[13] += int(obj.negativeDirect)
				baseStats[14] += int(obj.negativeIndirect)

			if TRAIT_CATGIRL in self.char.trait: baseStats[STRENGTH] = max(baseStats[STRENGTH],0) + self.char.level
			if self.char.npcTeam == NPC_KITSUNE: baseStats[CHARISMA] = max(baseStats[CHARISMA],self.char.level+self.char.stars*10) 

			if self.char.__class__ == classes.tmpAllie and self.team == 1 and not(octogone):
				for cmpt in range(CRITICAL+1):
					baseStats[cmpt] -= int(baseStats[cmpt]*.25)
		elif type(self.char) == invoc:
			actionsStats: int = int(min(self.summoner.baseStats[ACT_HEAL_FULL], self.summoner.baseStats[ACT_BOOST_FULL], self.summoner.baseStats[ACT_SHIELD_FULL], self.summoner.baseStats[ACT_DIRECT_FULL], self.summoner.baseStats[ACT_INDIRECT_FULL]) * 0.65)
			summonStats, summonerStats = self.char.allStats()+[self.char.resistance,self.char.percing,self.char.critical], self.summoner.baseStats
			baseStats = {STRENGTH:0, ENDURANCE:0 ,CHARISMA:0, AGILITY:0, PRECISION:0, INTELLIGENCE:0, MAGIE:0, RESISTANCE:0, PERCING:0, CRITICAL:0, 10:actionsStats, 11:actionsStats, 12:actionsStats, 13:actionsStats, 14:actionsStats}

			bonusPower = 1
			tmpChip = getChip("Maître Invocateur")
			if tmpChip.id in self.summoner.char.equippedChips: bonusPower = bonusPower* 1+ (self.summoner.char.chipInventory[tmpChip.id].power/100)
			
			for cmpt in range(len(summonStats)):
				if type(summonStats[cmpt]) == list:
					if summonStats[cmpt][0] == PURCENTAGE:
						baseStats[cmpt] += int(summonerStats[cmpt]*(summonStats[cmpt][1]))
					elif summonStats[cmpt][0] == HARMONIE:
						harmonie = 0
						for b, c in summonerStats.items():
							harmonie = max(harmonie,c)
						baseStats[cmpt] += round(harmonie*summonStats[cmpt][1])
				else:
					baseStats[cmpt] = summonStats[cmpt]
		else: 
			baseStats = copy.deepcopy(self.summoner.baseStats)
			baseStats[self.skills.use] += round(min(self.summoner.baseStats[ACT_HEAL_FULL],self.summoner.baseStats[ACT_BOOST_FULL],self.summoner.baseStats[ACT_SHIELD_FULL],self.summoner.baseStats[ACT_DIRECT_FULL],self.summoner.baseStats[ACT_INDIRECT_FULL])*-0.65)

		if self.char.element in [ELEMENT_FIRE, ELEMENT_UNIVERSALIS]: baseStats[PERCING] += 5
		elif self.char.element in [ELEMENT_WATER, ELEMENT_UNIVERSALIS]: baseStats[PRECISION] += 10
		elif self.char.element in [ELEMENT_AIR, ELEMENT_UNIVERSALIS]: baseStats[AGILITY] += 10
		elif self.char.element in [ELEMENT_EARTH, ELEMENT_UNIVERSALIS]: baseStats[RESISTANCE] += 5

		valueToBoost =  min(1,self.level / MAXLEVEL)
		baseStats[ENDURANCE] += int(30*valueToBoost)
		baseStats[RESISTANCE] += int(15*valueToBoost)

		if danger > 100 and type(self.char) == octarien:
			add = int(danger/135 * 20)
			for cmpt in [AGILITY,PRECISION,RESISTANCE]: baseStats[cmpt] += add

		if self.char.weapon.id in eternalInkWeaponIds:
			summation = 0
			for stat in range(10,15):
				if baseStats[stat] > 0:
					summation = int(baseStats[stat]*0.7)
					baseStats[stat] = 0

			baseStats[self.char.weapon.use] += summation

		if self.char.aspiration == BERSERK: self.aspiSlot = BERS_LIFE_STEAL
		elif self.char.aspiration in [PROTECTEUR,VIGILANT,ENCHANTEUR,MASCOTTE]: self.aspiSlot = []

		if type(self.char) not in [invoc, depl]:
			hasSkillUpdated, lvl = True, self.char.level - 5
			nbExpectedSkills, nbSkills = 0, 0

			for skilly in self.skills:
				if type(skilly) == skill: nbSkills += 1

			if type(self.char) != octarien:
				for cmpt in range(len(lvlToUnlockSkill)):
					if lvl >= lvlToUnlockSkill[cmpt]: nbExpectedSkills += 1
				hasSkillUpdated = nbSkills >= nbExpectedSkills
			else: hasSkillUpdated = nbSkills == self.char.baseSkillNb

			hasUpdatedStuff = True
			for stuffy in self.char.stuff:
				if stuffy.minLvl < self.char.level-10:
					hasUpdatedStuff = False
					break

			hasBonusPointsUpdated = self.char.points < 5

			if (hasBonusPointsUpdated and hasSkillUpdated and hasUpdatedStuff):
				for cmpt in range(MAGIE+1):
					baseStats[cmpt] = int(baseStats[cmpt] * 1.05)

		for cmpt in range(ACT_INDIRECT_FULL+1):
			communChipList = {STRENGTH:["Force augmentée I","Force augmentée II"],ENDURANCE:["Endurance augmenté I","Endurance augmenté II"],CHARISMA:["Charisme augmenté I","Charisme augmenté II"],AGILITY:["Agilité augmentée I",'Agilité augmentée II'],PRECISION:["Précision augmentée I","Précision augmentée II"],INTELLIGENCE:["Intelligence augmentée I","Intelligence augmentée II"],MAGIE:["Magie augmentée I","Magie augmentée II"],CRITICAL:["Critique universel"],RESISTANCE:["Renforcement"],PERCING:["Pénétration"],ACT_HEAL_FULL:["Soins augmentés I","Soins augmentés II"],ACT_BOOST_FULL:["Boosts augmenté I","Boosts augmenté II"],ACT_SHIELD_FULL:["Armures augmenté I","Armures augmenté II"],ACT_DIRECT_FULL:["Directs augmentée I","Directs augmentée II"],ACT_INDIRECT_FULL:["Indirects augmentée I","Indirects augmentée II"]}[cmpt]
			for indx, chipName in enumerate(communChipList):
				tmpChip = getChip(chipName)
				if tmpChip != None:
					if tmpChip.id in self.char.equippedChips:
						added = abs(round(self.char.chipInventory[tmpChip.id].power/100*[self.level,baseStats[cmpt]][indx]))
						baseStats[cmpt] += added
				else: print(chipName)

		self.baseStats = baseStats

		if type(self.char) not in [invoc,octarien]: baseHP,HPparLevel = BASEHP_PLAYER, HPPERLVL_PLAYER
		elif type(self.char) == invoc: baseHP, HPparLevel, self.char.level = BASEHP_SUMMON, HPPERLVL_SUMMON, self.summoner.char.level
		elif not(self.char.standAlone): baseHP, HPparLevel = BASEHP_ENNEMI, HPPERLVL_ENNEMI
		elif type(self.char) == depl: baseHP,HPparLevel = 9999999, 9999
		else: baseHP,HPparLevel = BASEHP_BOSS, HPPERLVL_BOSS

		initHpBonus, addHpMul = 0, 1
		communChipList = ["Constitution I","Constitution II"]
		for indx, chipName in enumerate(communChipList):
			tmpChip = getChip(chipName)
			if tmpChip != None and tmpChip.id in self.char.equippedChips:
				if indx == 0: initHpBonus += round(self.char.chipInventory[tmpChip.id].power/100*self.level)
				else: addHpMul += self.char.chipInventory[tmpChip.id].power/100

		self.maxHp = round((baseHP+initHpBonus+(self.char.level*HPparLevel))*(((self.baseStats[ENDURANCE])*0.85)/100+1)*addHpMul)
		if type(self.char) in [octarien,tmpAllie] and self.team: self.maxHp = round(self.maxHp * danger / 100)
		self.hp = copy.deepcopy(self.maxHp)
		self.trueMaxHp = copy.deepcopy(self.maxHp)

		if self.char.aspiration in [BERSERK,OBSERVATEUR,POIDS_PLUME,TETE_BRULEE,ATTENTIF]: self.IA = AI_DPT
		elif self.char.aspiration in [IDOLE,INOVATEUR,MASCOTTE]: self.IA = AI_BOOST
		elif self.char.aspiration in [ALTRUISTE,VIGILANT]: self.IA = AI_ALTRUISTE
		elif self.char.aspiration in [MAGE,SORCELER]: self.IA = AI_MAGE
		elif self.char.aspiration == ENCHANTEUR: self.IA = AI_ENCHANT
		elif self.char.aspiration in [PREVOYANT,PROTECTEUR]: self.IA = AI_SHIELD
		else:
			offSkill,SuppSkill,healSkill,armorSkill,invocSkill, tablAllSkills = 0,0,0,0,0, [self.char.weapon]
			if type(self.char) == depl: tablAllSkills.append(self.skills)
			else: tablAllSkills = tablAllSkills + self.skills
			for b in tablAllSkills:
				if type(b) in [weapon,skill]:
					if b.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]: offSkill += 1
					elif b.type in [TYPE_BOOST,TYPE_MALUS,TYPE_ARMOR]: SuppSkill += 1
					elif b.type in [TYPE_HEAL]: healSkill += 1
					elif b.type in [TYPE_SUMMON]: invocSkill += 1

			max_all = max(offSkill,SuppSkill,healSkill,armorSkill,invocSkill)
			if max_all == offSkill: self.IA = AI_OFFERUDIT
			elif max_all == SuppSkill: self.IA = AI_BOOST
			elif max_all == healSkill: self.IA = AI_ALTRUISTE
			elif max_all == armorSkill: self.IA = AI_BOOST
			else : self.IA = AI_AVENTURE

	def __str__(self): return "{0} {1}".format(self.icon, self.name)

	def allStats(self): return [self.strength, self.endurance, self.charisma, self.agility, self.precision, self.intelligence, self.magie]

	def move(self, cellToMove:Union[cell,None]=None, x:Union[int,None]=None, y:Union[int,None]=None):
		"""Move the entity on the given coordonates"""
		toReturn = ""
		if self.chained: return ""
		if cellToMove == None and x == None and y == None: raise Exception("Argument error : No parameters given")
		
		actCell = self.cell
		if cellToMove == None: destination = findCell(x,y, tablAllCells)
		else: destination = findCell(cellToMove.x,cellToMove.y, tablAllCells)
		self.cell = destination
		destination.on = self
		if actCell != None: actCell.on = None

		nonlocal deplTabl
		for tmpDepl in deplTabl:
			if tmpDepl[0].char.trap and self.cell in tmpDepl[2]:
				toReturn = tmpDepl[0].triggerDepl()
				tmpDepl[0].leftTurnAlive -= 99

				if tmpDepl[0].leftTurnAlive <= 0:
					tmpDepl[2], tmpDepl[1].depl = [], None
					if len(tmpDepl[0].ownEffect) == 0:
						try: deplTabl.remove(tmpDepl); tmpDepl[1].depl = None
						except: print_exc()

		for eff in self.effects:
			if eff.effects.trigger == TRIGGER_ON_MOVE:
				toReturn += eff.triggerStartOfTurn(danger)

		return toReturn

	def valueBoost(self, target = None, heal=False, armor=False):
		"""
			Return the bonus multiplier for any Buff, Debuff or Healing action\n
			Parameter :\n
			.target : A ``entity``.
				-> Use for the Altruistic malus on their-self
			.heal : Does the action is a Heal action ? Default ``False``
		"""

		if target == None: raise Exception("No target given")

		if self.char.aspiration == ALTRUISTE and heal: return [1, 1.2][target == self]

		elif self.char.aspiration == IDOLE and not(heal or armor):			 # Idol : The more alive allies they got, the more their buff a heals or powerfull
			nbAliveAllies = 0
			for ent in self.tablEntTeam[self.team]:
				if ent.hp > 0 and type(a.char) not in [invoc, depl]: nbAliveAllies += 1

			return 0.8 + min(nbAliveAllies, 8)*0.05

		elif self.char.aspiration == INOVATEUR and not(heal or armor):			 # Idol : The more alive allies they got, the more their buff a heals or powerfull
			nbAliveEnemies = 0
			for ent in self.tablEntTeam[not(self.team)]:
				if ent.hp > 0 and type(a.char) not in [invoc, depl]: nbAliveEnemies += 1
				if ent.char.standAlone: nbAliveEnemies = 6; break
			return 1 + nbAliveEnemies*0.04

		elif self.char.aspiration in [PREVOYANT,PROTECTEUR] and armor:
			if self.char.aspiration == PREVOYANT: return 1.2
			else: return 1 + 0.02 * len(self.aspiSlot)
	
		elif self.char.aspiration == VIGILANT and heal: return 1 + 0.02 * len(self.aspiSlot)
		else: return 1

	def effectIcons(self):
		"""Return a ``string`` with alls ``fightEffects`` icons, names and values on the entity"""
		res, allReadySeenId, allReadySeenName, allReadySeenNumber = "", [], [], []
		if self.effects != []:
			for a in self.effects:
				if a.effects.stackable and a.effects.id in allReadySeenId and a.effects.id not in effListShowPower:
					for cmpt in range(len(allReadySeenId)):
						if a.effects.id == allReadySeenId[cmpt]:
							allReadySeenNumber[cmpt] += 1
				elif a.effects.stackable and a.effects.id not in allReadySeenId and a.effects.id not in effListShowPower:
					allReadySeenId.append(a.effects.id)
					allReadySeenNumber.append(1)
					allReadySeenName.append("{0} {1}".format(a.icon,a.effects.name))
				else:
					name = a.effects.name
					if name.endswith("é"): name += self.accord()
					if a.type == TYPE_ARMOR: res += f"{a.icon} {name} ({a.value} PAr)\n"
					elif a.effects.id in effListShowPower: power = round(a.effects.power,2);  res += f"{a.icon} {name} ({power}%)\n"
					elif a.effects.turnInit > 0:
						pluriel = ""
						if a.turnLeft > 1: pluriel = "s"
						res += f"{a.icon} {name} ({a.turnLeft} tour{pluriel})\n"
					elif a.effects.id == eventFas.id: res += f"{a.icon} {name} ({a.value})\n"
					else: res += f"{a.icon} {name}\n"
			if allReadySeenId != []:
				for cmpt in range(len(allReadySeenId)): res += "{0}{1}\n".format(allReadySeenName[cmpt],[""," *(x{0})*".format(allReadySeenNumber[cmpt])][allReadySeenNumber[cmpt]>1])
		else: res = "Pas d'effet sur la cible\n"

		for deplEnt in deplTabl:
			if self.cell in deplEnt[2]: res += '{0} {1}\n'.format(deplEnt[0].char.cellIcon[deplEnt[0].team], deplEnt[0].char.name)
		res = reduceEmojiNames(res)
		if len(res) > EMBED_FIELD_VALUE_LENGTH: res = completlyRemoveEmoji(res)
		if len(res) > EMBED_FIELD_VALUE_LENGTH: res = "OVERLOAD"
		return res

	def recalculate(self):
		"""
			Recalculate the entity stats with all their ``fightEffects``\n
			- Parameter :
				- ignore : A ``fightEffect`` to ignore. Default ``None``
		"""
		self.dmgUp, self.critDmgUp, self.healUp, self.critHealUp, self.silent, self.translucide, self.untargetable, self.invisible, self.immune, self.stun, baseStats, self.dodge, self.dmgOnArmor = 0,0,0,0, False, False, False, False, False, False, self.baseStats, [0,10][self.char.aspiration == POIDS_PLUME], 1
		sumStatsBonus, self.chained = copy.deepcopy(baseStats), False
		self.counterOnDodge, self.blockRate, self.counterOnBlock, self.dualCast = 0, 0, 0, None

		for eff in self.effects:
			if eff.effects.stat != None and eff.effects.overhealth == 0:
				tablEffStats = eff.allStats()
				for cmpt in range(CRITICAL+1): sumStatsBonus[cmpt] += tablEffStats[cmpt]

			elif eff.effects.id not in [lastDitchEffortEff.id,openingGambitEff.id]:
				sumStatsBonus[0] += eff.effects.strength 
				sumStatsBonus[1] += eff.effects.endurance 
				sumStatsBonus[2] += eff.effects.charisma
				sumStatsBonus[3] += eff.effects.agility
				sumStatsBonus[4] += eff.effects.precision
				sumStatsBonus[5] += eff.effects.intelligence
				if eff.effects.id == "tem": sumStatsBonus[6] += int(self.char.level * 2.5)
				else: sumStatsBonus[6] += eff.effects.magie
				sumStatsBonus[7] += eff.effects.resistance
				sumStatsBonus[8] += eff.effects.percing
				sumStatsBonus[9] += eff.effects.critical

			elif (eff.effects.id == lastDitchEffortEff.id and (tour >= 17 or self.hp/self.maxHp <= 0.25)) or (eff.effects.id == openingGambitEff.id and (tour <= 1 or self.hp/self.maxHp >= 0.9)):
				effPowa = 1 + (self.char.chipInventory[getChip(["Châpeau de Roues","Ultime Sursaut"][eff.effects.id == lastDitchEffortEff.id]).id].power/100)
				sumStatsBonus[0] += self.baseStats[STRENGTH] * effPowa
				sumStatsBonus[1] += self.baseStats[ENDURANCE] * effPowa
				sumStatsBonus[2] += self.baseStats[CHARISMA] * effPowa
				sumStatsBonus[3] += self.baseStats[AGILITY] * effPowa
				sumStatsBonus[4] += self.baseStats[PRECISION] * effPowa
				sumStatsBonus[5] += self.baseStats[INTELLIGENCE] * effPowa
				sumStatsBonus[6] += self.baseStats[MAGIE] * effPowa

			if eff.stun: self.stun = True
			if eff.effects.invisible: self.translucide, self.untargetable, self.invisible = True, True, True
			if eff.effects.translucide: self.translucide = True
			if eff.effects.untargetable: self.untargetable = True
			if eff.effects.immunity: self.immune = True
			if eff.effects.id == silenceEff.id: self.silent = True
			elif eff.effects.id == chained.id: self.chained = True

			self.dmgUp, self.critDmgUp, self.healUp, self.critHealUp, self.dodge, self.dmgOnArmor = self.dmgUp+eff.effects.dmgUp, self.critDmgUp+eff.effects.critDmgUp, self.healUp+eff.effects.healUp, self.critHealUp+eff.effects.critHealUp, self.dodge + eff.effects.dodge, self.dmgOnArmor * (1+eff.effects.armorDmgBonus)
			if eff.effects.counterOnDodge > 0: self.counterOnDodge += eff.effects.counterOnDodge
			if eff.effects.counterOnBlock > 0: self.counterOnBlock += eff.effects.counterOnBlock
			if eff.effects.block > 0: self.blockRate += eff.effects.block
			if eff.effects.id in [dualCastEff.id]: self.dualCast = eff
		
		if type(self.char) not in [invoc, depl]: tRes = sumStatsBonus[7]+self.char.resistance
		else: tRes = sumStatsBonus[7]

		if self.dodge > 100: self.counterOnDodge += self.dodge - 100; self.dodge = 100
		if self.blockRate > 100: self.counterOnBlock += self.blockRate - 100

		self.rawResist, self.rawPercing = sumStatsBonus[7], sumStatsBonus[PERCING]

		sumStatsBonus[7] = getResistante(resist=sumStatsBonus[7])
		sumStatsBonus[PERCING] = getPenetration(sumStatsBonus[PERCING])

		for temp in range(len(sumStatsBonus)): sumStatsBonus[temp] = round(sumStatsBonus[temp])
		
		self.strength, self.endurance, self.charisma, self.agility, self.precision, self.intelligence, self.magie, self.resistance, self.percing,self.critical, self.negativeHeal, self.negativeBoost, self.negativeShield, self.negativeDirect, self.negativeIndirect = sumStatsBonus[0], sumStatsBonus[1], sumStatsBonus[2], sumStatsBonus[3], sumStatsBonus[4] ,sumStatsBonus[5] ,sumStatsBonus[6], sumStatsBonus[7], sumStatsBonus[8],sumStatsBonus[9],sumStatsBonus[10],sumStatsBonus[11],sumStatsBonus[12],sumStatsBonus[13],sumStatsBonus[14]

	def refreshEffects(self):
		"""Add the ``fightEffects`` into the waiting list and remove the obcelettes ones"""
		for eff in self.effects[:]:
			if eff.remove:
				self.effects.remove(eff)
				try: eff.caster.ownEffect.remove({self:eff.id})
				except: pass

				if eff.effects.id == constEff.id:
					self.maxHp = int(max(self.maxHp - eff.value,1))
					self.hp = min(self.hp,self.maxHp)
				elif eff.effects.id == aconstEff.id:
					self.maxHp = int(self.maxHp + eff.value)
				elif eff.effects.id in naciaElemEffIds:
					self.char.splashIcon = ["<:nacialisla:1208074071779315712>","<:giantessNacia:1208132139342626846>"][naciaFlag]
					self.icon = self.char.splashIcon
		for a in addEffect[:]:
			self.effects.append(a)
			a.caster.ownEffect.append({self:a.id})
			addEffect.remove(a)
			if type(a) != fightEffect: raise AttributeError("Except fightEffect, but get {0} insted".format(type(a)))
		self.recalculate()

	def indirectAttack(self,target=0,value=0,icon="",ignoreImmunity=False,name='',hideAttacker=False,canCrit=True, redirected=False) -> str:
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
		if type(value) == tuple: value = value[0]
		if canCrit and random.randint(0,99) < self.intelligence/200*25 * (1-(target.intelligence/100*10)/100): value, hasCrit = value * [1.15,1.25][self.char.aspiration in [SORCELER,ATTENTIF]], " !"

		if target.hp > 0 and not(target.immune):
			# Looking for a absolute shield
			maxResist, vulnePower, lifeSavor = 0, 0, []
			for eff in target.effects:
				if eff.effects.immunity == True and not(ignoreImmunity):
					value = 0
				if eff.effects.absolutShield and eff.value > 0:
					dmg = int(min(value,eff.value))
					if not(hideAttacker):
						popopo += f"{self.icon} {icon} → {eff.icon}{eff.on.icon} -{dmg} PV\n"
					else:
						popopo += f"{eff.icon}{eff.on.icon} -{dmg} PV\n"
					popopo += eff.decate(value=dmg)
					self.stats.damageOnShield += dmg
					if eff.value <= 0:
						value = max(0,dmg-eff.on.char.level)
					else:
						value = 0
				if eff.effects.id in LIFESAVOREFF:
					lifeSavor.append(eff)
			if type(target.char) == invoc and target.char.name.startswith("Patte de The Giant Enemy Spider"):
				value = int(value * target.char.weapon.effects.redirection/100)
				target.summoner.hp -= value
				if self != target:				  # If the damage is deal on another target, increase the correspondings stats
					self.stats.damageDeal += value
					self.stats.indirectDamageDeal += value
					target.stats.damageRecived += value
				if target.summoner.hp <= 0:
					popopo += target.death(killer=self)
				popipo = f"{self.icon} {icon} → {target.summoner.icon} -{value} PV {target.icon} - 0 PV{hasCrit}{name}\n"
				value = 0

			# If the number of damage is still above 0
			if value > 0:
				value = int(value)
				if value >= target.hp and len(lifeSavor) > 0:
					for eff in lifeSavor:
						healMsg, why = eff.caster.heal(target,eff.icon,eff.effects.stat,[eff.effects.power,eff.value][eff.effects.stat in [None,FIXE]],eff.name,mono=True,direct=False)
						popopo += healMsg
						eff.decate(value=99999999)
						
					target.refreshEffects()
				target.hp -= value

				for indx, chipId in enumerate(self.char.equippedChips):
					tmpChip = getChip(chipId)
					if tmpChip != None:
						if tmpChip.name == "Radiance Toxique":
							self.chipAddInfo[indx] += value * self.char.chipInventory[chipId].power/100

				if self != target:				  # If the damage is deal on another target, increase the correspondings stats
					if type(self.char) not in [invoc,depl]:
						self.stats.damageDeal += value
						self.stats.indirectDamageDeal += value
					else:
						entDict[self.summoner.id].stats.damageDeal += value
						entDict[self.summoner.id].stats.indirectDamageDeal += value
						entDict[self.summoner.id].stats.summonDmg += value
					target.stats.damageRecived += value
				else: self.stats.selfBurn += value
				if name != '': name = ' ({0})'.format(name)

				if redirected: target.stats.redirectedDamage += value

				if target.hp <= 0 and len(self.tablEntTeam[target.team]) == 1 and self.isNpc("Lia Ex"): popopo += "{0}{1} : \"*お前はもう死んでいる*\"\n{2} : \"*なに- !?*\"\n".format(["","\n"][len(popopo) > 0 and popopo[-2:-1] != "\n"],self.icon,target.icon)
				if not(hideAttacker): valueFrmt = separeUnit(value); popopo += f"{self.icon} {icon} → {target.icon} -{valueFrmt} PV{hasCrit}{name}\n"
				else: popopo += f"{target.icon} -{value} PV{hasCrit}{name}\n"

				if target.hp <= 0:
					popopo += target.death(killer=self)
					if self == target: self.stats.sufferingFromSucess = True

				for team in [0,1]:
					for jaugeEnt, jaugeEff in teamJaugeDict[team].items():
						for conds in jaugeEff.effects.jaugeValue.conds:
							if conds.type == INC_ENEMY_DAMAGED and jaugeEnt.team == self.team:
								jaugeEff.value = min(jaugeEff.value+((conds.value*value/target.maxHp*100)*([1,5][target.char.standAlone])),100)
							elif conds.type == INC_ALLY_DAMAGED and jaugeEnt.team == target.team:
								jaugeEff.value = min(jaugeEff.value+((conds.value*value/target.maxHp*100)*([1,5][target.char.standAlone])),100)

				try:
					for conds in teamJaugeDict[self.team][[self,self.summoner][type(self.char) in [invoc,depl]]].effects.jaugeValue.conds:
						if conds.type == INC_DEAL_DAMAGE:
							teamJaugeDict[self.team][[self,self.summoner][type(self.char) in [invoc,depl]]].value = min(teamJaugeDict[self.team][[self,self.summoner][type(self.char) in [invoc,depl]]].value+((conds.value*value/target.maxHp*100)*([1,5][target.char.standAlone])),100)
				except KeyError: pass

		return popopo

	def death(self,killer = 0,trueDeath=False) -> str:
		"""
			The death method, to use when the entity dies.\n
			Parameter :\n
			.killer : The ``entity`` who have kill the entity
		"""
		nonlocal logs
		if not(trueDeath):
			for eff in self.effects:
				if eff.effects.id in [holmgangEff.id] and eff.turnLeft > 0:
					self.hp = 1
					return "{0} ne peut pas être vaincu{1} ({2})\n".format(self.name,self.accord(),eff.effects.name)
				elif eff.effects.id == undeadEff.id:
					self.hp = 1
					ballerine = add_effect(caster=self, target=self, effect=undeadEff2, start=eff.effects.name, danger=danger, skillIcon=eff.icon)
					chocolatine, latinechoco = self.heal(target=self, icon=eff.icon, statUse=None, power = round(self.maxHp*eff.effects.power/100), effName = eff.effects.name, direct=False)
					ballerine += chocolatine
					eff.decate(value=1)
					return ballerine
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
				elif eff.effects.id == "recall":
					self.hp, self.maxHp = int(self.maxHp*0.2), max(int(self.maxHp*0.95), int(self.trueMaxHp*0.2))
					return ""
		for indx, tmpId in enumerate(self.char.equippedChips):
			tmpChip = getChip(tmpId)
			if tmpChip != None:
				if tmpId == getChip("Totem de Protection").id and self.chipAddInfo[indx]:
					tmpUsrChip, self.hp = self.char.chipInventory[tmpId], 1
					tmpMsg, babie = self.heal(target=self, icon=tmpChip.emoji, statUse=PURCENTAGE, power=tmpUsrChip.power, mono = True, direct=False)
					eff1, eff2 = classes.effect("Protection","immortalityTotemShield",PURCENTAGE,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,overhealth=tmpUsrChip.power,absolutShield=True), classes.effect("Régénération","immortalityTotemHeal",PURCENTAGE,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,power=tmpUsrChip.power,turnInit=3,emoji=tmpChip.emoji)
					ballerine = groupAddEffect(caster=self, target=self, area=AREA_MONO, effect=[eff1, eff2], skillIcon=tmpChip.emoji)
					self.chipAddInfo[indx] = 0
					return tmpMsg+ballerine
				elif tmpId == getChip("Plot Armor").id and self.chipAddInfo[indx]:
					tmpUsrChip, self.hp = self.char.chipInventory[tmpId], 1
					eff1, eff2 = copy.deepcopy(holmgangEff), copy.deepcopy(dmgUp)
					eff1.power, eff2.power = 0, tmpUsrChip.power
					eff1.turnInit = eff2.turnInit = 2
					ballerine = groupAddEffect(caster=self, target=self, area=AREA_MONO, effect=[eff1, eff2], skillIcon=tmpChip.emoji)
					self.chipAddInfo[indx] = 0
					return ballerine

		for tmpEnt in dictHasBenedicton[self.team]:
			tmpEnt = entDict[tmpEnt]
			for indx, tmpId in enumerate(tmpEnt.char.equippedChips):
				tmpChip = getChip(tmpId)
				if tmpChip != None:
					if tmpId == getChip("Bénédiction").id and tmpEnt.chipAddInfo[indx]:
						self.hp = 1
						tmpMsg, babie = tmpEnt.heal(target=self, icon=tmpChip.emoji, statUse=PURCENTAGE, power=tmpEnt.char.chipInventory[tmpId].power, mono = True, direct=False)
						tmpEnt.chipAddInfo[indx] = 0
						dictHasBenedicton[self.team].remove(tmpEnt.id)
						return tmpMsg

		if self.isNpc("Aformité incarnée") and dictIsNpcVar["Luna prê."]:
			if not(killer.isNpc("Luna prê.")):
				self.hp = 1
				return ""
			else:
				add_effect(self,killer,classes.effect("Borgne","lunaBlinded",precision=-50,stat=MAGIE,turnInit=-1,unclearable=True))
				killer.refreshEffects()

		pipistrelle = f"{self.char.name} ({self.icon}) est vaincu{self.accord()} !\n"
		if self.status == STATUS_RESURECTED: pipistrelle = f"{self.char.name} ({self.icon}) est vaincu{self.accord()} (pour de bon) !\n"; self.status=STATUS_TRUE_DEATH

		if type(self.char) not in [invoc, depl] and killer != self and killer.char.says.onKill != None and random.randint(0,99)<33:
			try:
				if killer.isNpc("Luna prê.") or killer.isNpc("Luna ex."):
					msgPerElement = [None,None,None,None,None,"La lumière ne peut pas toujours avoir raison de l'ombre.","Reviens donc quand tu auras compris ce que sont les vrais Ténèbres.","L'Espace peut très bien être brisé.","Essaye donc de gagner du Temps là dessus.","Tu as tous les éléments et tu n'est même pas capable de t'en sortir ?"]
					if msgPerElement[self.char.element] != None:
						pipistrelle += "{0} : *\"{1}\"*\n".format(killer.icon,msgPerElement[self.char.element])
					else:
						pipistrelle += "{0} : *\"{1}\"*\n".format(killer.icon,killer.char.says.onKill.format(target=self.char.name,caster=killer.char.name))
				elif killer.isNpc("Ly") and self.isNpc("Zombie"):
					pipistrelle += "{0} : *\"Tu peux ramner tous tes potes si tu veux, je connais un prêtre qui est toujours prêt à me racheter de la rotten flesh\"*\n".format(killer.icon,killer.char.says.onKill.format(target=self.char.name,caster=killer.char.name))
				elif killer.isNpc("Lohica") and not(actTurn.isNpc("Lohica")):
					pipistrelle += "{0} : *\"Alors, ça t'a coupé le souffle hein ?\"*\n".format(killer.icon)
				elif killer.isNpc("Clémence Exaltée"):
					pipistrelle += "{0} : *\"{1}\"*\n".format(killer.icon,clemExKillReact[self.char.aspiration].format(target=self.char.name,caster=killer.char.name))
				elif killer.hp > 0:
					pipistrelle += "{0} : *\"{1}\"*\n".format(killer.icon,randRep(killer.char.says.onKill).format(target=self.char.name,caster=killer.char.name))
			except:
				pipistrelle += "__Error whith the onKill message__\n"
				log = format_exc()
				if len(log) > 50:
					pipistrelle += "{0}\n".format(log[-50:])
				else:
					pipistrelle += "{0}\n".format(log)

		elif self.isNpc("Lohica") and killer != self:
			pipistrelle += "{0} : *\"Ok {1}, qu'est-ce que tu dis de ça ?\"*\n".format(self.icon,killer.char.name) + add_effect(self,killer,estial)
			killer.refreshEffects()

		elif self.isNpc("Amary") and killer != self and dictIsNpcVar["Lohica"]:
			lohica = None
			for team in (0,1):
				for ent in self.tablEntTeam[team]:
					if ent.isNpc("Lohica") and ent.hp > 0:
						lohica = ent
						break

			if lohica != None:
				pipistrelle += "{0} : *\"Tu vas payer pour ça.\"*\n".format(lohica.icon) + add_effect(lohica,killer,estial,effPowerPurcent=[100,150][lohica.team != killer.team])
				killer.refreshEffects()

		try: # death reaction
			allreadyReact = False
			for reactNames, reactValues in self.char.says.specDeath.items():
				if dictIsNpcVar[reactNames]:
					for entId, ent in entDict.items():
						if ent.isNpc(reactNames) and ent.hp > 0:
							allreadyReact = True
							pipistrelle += "{0} : *\"{1}\"*\n".format(ent.icon,randRep(reactValues))

			if self.char.says.onDeath != None and not(allreadyReact) and random.randint(0,99)<33:
				try:
					pipistrelle += "{0} : *\"{1}\"*\n".format(self.icon,randRep(self.char.says.onDeath).format(target=self.char.name,caster=killer.char.name))
				except:
					pipistrelle += "__Error whith the death message__\n"
					log = format_exc()
					if len(log) > 50:
						pipistrelle += "{0}\n".format(log[-50:])
					else:
							pipistrelle += "{0}\n".format(log)
		except:
			pipistrelle += "__Error whith the death reaction message__\n"
			log = format_exc()
			if len(log) > 50:
				pipistrelle += "{0}\n".format(log[-50:])
			else:
				pipistrelle += "{0}\n".format(log)
			print_exc()

		try:				# Reactions
			allreadyReact = False
			for reactNames, reactValues in self.char.says.specReact.items():
				if dictIsNpcVar[reactNames]:
					for entId, ent in entDict.items():
						if ent.isNpc(reactNames) and ent.hp > 0:
							allreadyReact = True
							if type(reactValues) == str:
								pipistrelle += "{0} : *\"{1}\"*\n".format(ent.icon,reactValues)
							else:
								pipistrelle += "{0} : *\"{1}\"*\n".format(ent.icon,randRep(reactValues))

			if random.randint(0,99) < 20 and type(self.char) not in [invoc, depl] and not allreadyReact:
				tablAllInterract = []
				for ent in self.tablEntTeam[self.team]:
					if ent.char.says.reactAllyKilled != None and ent != self and ent.hp > 0:
						tablAllInterract.append("{0} : *\"{1}\"*\n".format(ent.icon,randRep(ent.char.says.reactAllyKilled).format(killer=killer.char.name,downed=self.char.name,target=self.char.name)))
				for ent in self.tablEntTeam[not(self.team)]:
					if ent.char.says.reactEnnemyKilled != None and ent != killer and ent.hp > 0:
						tablAllInterract.append("{0} : *\"{1}\"*\n".format(ent.icon,randRep(ent.char.says.reactEnnemyKilled).format(killer=killer.char.name,downed=self.char.name)))

				if len(tablAllInterract) >= 1:
					pipistrelle += randRep(tablAllInterract)
		except:
			pipistrelle += "__Error whith the death reaction message__\n"
			log = format_exc()
			if len(log) > 50:
				pipistrelle += "{0}\n".format(log[-50:])
			else:
				pipistrelle += "{0}\n".format(log)
			print_exc()

		allreadyexplose, dispersionDict = False, {}
		for fEffect in self.effects:
			if fEffect.effects.trigger == TRIGGER_DEATH:
				pipistrelle += fEffect.triggerDeath(killer)
			elif fEffect.effects.id == deepWound.id:
				if entDict[fEffect.caster.id].hp > 0:
					temp1, temp2 = entDict[fEffect.caster.id].heal(target=entDict[fEffect.caster.id], icon=fEffect.icon, statUse=FIXE, power=int(fEffect.value*DEEP_WOUND_RATIO/100), lifeSteal = True, direct=False, incHealJauge=False)
					pipistrelle += temp1
			elif fEffect.effects.id == estial.id and fEffect.caster.char.weapon.id == secretum.id and not(allreadyexplose):
				summationPower = 0
				for eff in self.effects:
					if eff.effects.id == estial.id and eff.turnLeft > 0:
						summationPower += eff.effects.power * secretum.effects.power / 100 * eff.turnLeft
						eff.decate(turn=99,value=99)
				self.refreshEffects()

				stat,damageBase,allReadySeen, killCount, dmgDict, beforeDmg, tempMsg, nbHit = fEffect.caster.allStats()[MAGIE]-fEffect.caster.negativeIndirect,summationPower,[], 0 , "", copy.deepcopy(fEffect.caster.stats.indirectDamageDeal), "", 0
				for a in self.cell.getEntityOnArea(area=secretum.effects.area,team=self.team,wanted=ALLIES,directTarget=False,fromCell=actTurn.cell):
					reduc = 1
					if a != self:
						reduc = max(AOEMINDAMAGE,1-self.cell.distance(a.cell)*AOEDAMAGEREDUCTION)

					damage, tempLogs = indirectDmgCalculator(fEffect.caster,self,summationPower,MAGIE,[100,danger][fEffect.caster.team==1],AREA_CIRCLE_2)
					damage = damage*reduc

					tempMsg += fEffect.caster.indirectAttack(a,value=damage,icon = secretum.emoji,name=secretum.effects.name)
					logs += tempLogs

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
					pipistrelle += groupAddEffect(killer, self, allReadySeen, fEffect.caster.char.weapon.effects.emoji[0][0], effPurcent=secretum.effects.power)
				allreadyexplose = True
			elif fEffect.effects.id == soulScealEff.id:
				eff = copy.deepcopy(fEffect.effects)
				eff.power, eff.turnInit, eff.lvl = soulScealEff.power, fEffect.turnLeft, fEffect.turnLeft
				pipistrelle += groupAddEffect(caster=fEffect.caster, target=self, area=AREA_DONUT_2, effect=eff, skillIcon=fEffect.icon)

			tmpChip = getChip("Dispersion")
			if tmpChip != None and tmpChip.id in fEffect.caster.char.equippedChips and fEffect.effects.type == TYPE_INDIRECT_DAMAGE:
				try:
					dispersionDict[fEffect.caster] += fEffect.effects.power * [1,max(1,fEffect.turnLeft)][fEffect.trigger in [TRIGGER_START_OF_TURN, TRIGGER_END_OF_TURN]] * fEffect.caster.char.chipInventory[tmpChip.id].power/100
				except KeyError:
					dispersionDict[fEffect.caster] = fEffect.effects.power * [1,max(1,fEffect.turnLeft)][fEffect.trigger in [TRIGGER_START_OF_TURN, TRIGGER_END_OF_TURN]] * fEffect.caster.char.chipInventory[tmpChip.id].power/100

			if fEffect.turnLeft > 0:
				if fEffect.trigger == TRIGGER_ON_REMOVE:
					pipistrelle += fEffect.decate(turn=99)
				else:
					fEffect.decate(turn=99)

		self.refreshEffects()
		if self.char.npcTeam == NPC_BOMB:
			tmpEff = classes.effect("Explosion",self.skills[0].id,self.skills[0].use,area=self.skills[0].area,type=TYPE_DAMAGE,trigger=TRIGGER_INSTANT,power=self.skills[0].power,emoji=self.char.icon[self.team])
			pipistrelle += groupAddEffect(caster=self, target=self, area=self, effect=tmpEff)

		if dispersionDict != {}:
			tmpChip = getChip("Dispersion")
			for ent, tPower in dispersionDict.items():
				tPower = round(max(10,tPower/3))
				tmpEff = classes.effect("Dispersion ({0})".format(tPower),"dispEff",HARMONIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN, power=tPower, emoji=tmpChip.emoji, replace=True, turnInit=3)
				pipistrelle += groupAddEffect(caster=ent, target=self, area=AREA_DONUT_2, effect=tmpEff, skillIcon=tmpChip.emoji)

		if killer.char.aspiration == SORCELER and type(self.char) not in [invoc, depl] and killer != self:
			for a in self.cell.getEntityOnArea(area=AREA_CIRCLE_1,team=self.team,wanted=ALLIES,directTarget=False,fromCell=actTurn.cell):
				reduc = 1
				if a != self:
					reduc = max(AOEMINDAMAGE,1-self.cell.distance(a.cell)*AOEDAMAGEREDUCTION)
				damage, tempLogs = indirectDmgCalculator(killer,a,max(5,killer.char.level),MAGIE,[100,danger][killer.team==1],AREA_CIRCLE_1)
				damage = damage * reduc 
				pipistrelle += killer.indirectAttack(a,value=damage,icon = aspiEmoji[SORCELER])
				logs += tempLogs

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
			if floorTanking.id in self.specialVars:
				effect = copy.deepcopy(lostSoul)
				effect.turnInit += 1
			add_effect(killer,self,effect)

			self.refreshEffects()

		elif self.status == STATUS_TRUE_DEATH and killer.isNpc("Kitsune") and type(self.char) not in [invoc,depl]:
			pipistrelle += killer.heal(killer,"",CHARISMA,60, effName = "Âme consummée",danger=100, mono = True, useActionStats = ACT_HEAL,direct=False)[0]

		if self.char.__class__ == classes.octarien and self.isNpc("Tour"):
			for ent in self.tablEntTeam[self.team]:
				for eff in ent.effects:
					if eff.effects.id == self.skills[0].effects[0].callOnTrigger.id:
						eff.decate(turn=99)
						ent.refreshEffects()
						break
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

	def attack(self,target=0,value = 0,icon = "",area=AREA_MONO,accuracy=None,use=STRENGTH,onArmor = 1,effectOnHit = [], useActionStats = ACT_DIRECT, setAoEDamage = False, lifeSteal:int = 0, erosion = 0, skillPercing = 0, execution = False, skillUsed: Union[classes.skill, classes.weapon] = None) -> str:
		"""
			The method for when a entity attack.\n
			Unlike .indirectAttack(), the targets, damages and triggered effects are all calculated in this method\n
			- Parameters :
				- target : The ``entity`` targeted by the entity
				- value : The base power of the attack.
					- If the value is at ``0``, no ``string`` is return
				- icon : The ``string`` to use as the icon of the attack. Default ``""``
				- area : The area of the attack. See ``constantes``. Default ``AREA_MONO``
				- accuracy : The base precision of the attack. If at ``None`` (Default), use the accuracy rate of the entity weapon insted
				- use : The base stat to take for the attack. See ``constantes``
				- onArmor : The multiplier of damage to deal on armors effects. Default ``1``
				- effectOnHit : Does the attack give a `effect` on the targets ? Default ``None``
		"""
		nonlocal logs
		effectOnHit = copy.deepcopy(effectOnHit)
		if effectOnHit == None:
			effectOnHit = []
		elif effectOnHit.__class__ != list:
			effectOnHit = [effectOnHit]
		if accuracy==None: # If no success is gave, use the weapon success rate
			accuracy=self.char.weapon.accuracy

		if useActionStats == None:
			useActionStats = ACT_DIRECT

		if skillUsed == None:
			skillUsed = classes.skill("No Skill","",TYPE_UNIQUE)
		sumDamage, deathCount = 0, 0

		popipo,critMsg = "",""

		if type(target) != int and value > 0: # If the target is valid
			dangerMul, dodgeMul, armorSteal, armorStealEmojis, effDealsDamage, backupDancerFlag, backupbisFlag = 1, 1, 0, "", [], None, None
			if danger != None and self.team: dangerMul = danger/100

			if type(skillUsed) == classes.skill and skillUsed.armorSteal > 0:
				armorSteal += skillUsed.armorSteal / 100
				armorStealEmojis += skillUsed.emoji

			popipo,aoeFactor,dmgUpPower,eroTxt, damageMul, isDepha, armorConvertEmoji, armorConvert, deepWoundConvert, deepWoundValue = "",1, 0+5*int(not(self.auto)),"", 1, False, [], 0, 0, 0
			if type(skillUsed) == classes.skill and skillUsed.armorConvert > 0:
				armorConvert += skillUsed.armorConvert
				armorConvertEmoji += [skillUsed.emoji]
			if erosion != 0: eroTxt += icon
			if self.char.aspiration == TETE_BRULEE:
				armorConvert, deepWoundConvert = armorConvert+10, deepWoundConvert+10
				armorConvertEmoji += [aspiEmoji[TETE_BRULEE]]
				onArmor += 0.2
			if self.char.secElement == ELEMENT_EARTH:
				armorConvert += EARTHBOOST
				armorConvertEmoji += [elemEmojis[ELEMENT_EARTH]]

			for eff in self.effects: # Does the attacker trigger eff effect
				if eff.trigger == TRIGGER_DEALS_DAMAGE and value > 0 and eff.effects.onDeclancher: effDealsDamage.append(eff)
				elif eff.effects.id == akikiSkill1Eff.id: dmgUpPower += akikiSkill1Eff.power * (1-(self.hp/self.maxHp))
				elif eff.effects.id == lbRdmBlind.id: dodgeMul -= lbRdmBlind.power/100
				elif eff.effects.id == jetLagEff.id: isDepha = True
				elif eff.effects.id in [krystalFistEff.id]:
					armorSteal += eff.effects.power / 100
					armorStealEmojis += eff.icon
				elif eff.effects.id in [ailillPassiveEff.id,physicRuneEff1.id,magicRuneEff1.id]: deepWoundConvert += eff.effects.power
			if self.char.aspiration == BERSERK and self.hp / self.maxHp <= .25: dmgUpPower += 10
			damageMul = damageMul + (dmgUpPower/100)
			damageMul = max(0.05,damageMul)

			tmpChip = getChip("Vampirisme I")
			if tmpChip != None and tmpChip.id in self.char.equippedChips: lifeSteal += self.char.chipInventory[tmpChip.id].power

			tmpChip = getChip("Dégâts directs augmentés")
			if tmpChip != None and tmpChip.id in self.char.equippedChips: dmgUpPower += self.char.chipInventory[tmpChip.id].power

			if self.hp > 0: # Does the attacker still alive ?
				critMalusCmpt, tablTarget,lifeStealMsg, aoeStealMsg, armorStolen, lifeStealEmote, tablPanhaima = 0, target.cell.getEntityOnArea(area=area,team=self.team,wanted=ENEMIES,directTarget=False,fromCell=actTurn.cell), "","", 0, [], []
				for entityInArea in tablTarget: # For eatch ennemis in the area
					if entityInArea.hp > 0: # If the entityInArea is alive
						self.stats.totalNumberShot += 1
						if entityInArea.isNpc(TGESL1.name):
							entityInArea = entDict[entityInArea.summoner.id]
						logs += "===== {0} is attacking {1} =====\n".format(self.name,entityInArea.name)
						critMsg = ""
						
						tmpChip = getChip("Empathie")
						if tmpChip.id in entityInArea.char.equippedChips and entityInArea.id == target.id and len(tablTarget) > 1: value = round(value * (100-entityInArea.char.chipInventory[tmpChip.id].power)/100)

						# Dodge / Miss
						attPre,entityInAreaAgi = self.precision, entityInArea.agility
						if area != AREA_MONO and len(tablTarget) == 1:
							accuracy += 20

						if attPre <= 0:											  # If the attacker's precision is negative
							entityInAreaAgi += abs(attPre)										# Add the negative to the entityInArea's agility
							attPre = 0
						if entityInAreaAgi <= 0:										 # Same if the entityInArea's agility is negative, add it to the attacker's precision
							attPre += abs(entityInAreaAgi)
							entityInAreaAgi = 1

						if attPre < entityInAreaAgi:									  # If the entityInArea's agility is (better ?) than the attacker's precision
							successRate = 1 - clamp((entityInAreaAgi-attPre)/100)*0.5 * dodgeMul			 # The success rate is reduced to 50% of the normal
						else:
							successRate = 1 + clamp((attPre-entityInAreaAgi)/100) * dodgeMul				 # The success rate is increased up to 200% of the normal

						# It' a hit ?
						succRate = successRate*accuracy*(1-(entityInArea.dodge/100))*10
						logs += "- Hit Rate : {0}% -> ".format(succRate/10)
						if random.randint(0,999) < succRate:
							dmgMul = 1
							tempToReturn, noneArmorMsg, lifeSavor, tablRedirect, tablArmor, critVulne, justEnig, huntMark = "", "", [], [], [], 0, None, False
							blocked, addedDeepwound = False, 0
							logs += "Hit"

							# AoE reduction factor
							if skillUsed.id != requiem.id:
								if entityInArea.cell.distance(target.cell) == 0 or setAoEDamage: aoeFactor = 1
								else: aoeFactor = 1-(min(1-AOEMINDAMAGE,min(entityInArea.cell.distance(target.cell)-int(target==self or area in [AREA_DONUT_1,AREA_DONUT_2,AREA_DONUT_3]),0)*AOEDAMAGEREDUCTION)); logs += "\n- AoEDamage : {0}%".format(aoeFactor*100)
							else:
								distance = entityInArea.cell.distance(target.cell)
								if distance == 1: aoeFactor = 2
								elif distance <= 3: aoeFactor = 1.5
								elif distance <= 9: aoeFactor = 1
								else: aoeFactor = 0.5

							if skillUsed != None and skillUsed.id == trans.id and type(entityInArea.char) in [tmpAllie,char]: aoeFactor = aoeFactor*0.65

							if self.isNpc("Iliana OvL") and self.cell.distance(entityInArea.cell) >= 3: aoeFactor = aoeFactor * 0.6

							if entityInArea.immune: damage = 0
							else:
								damage, tempLog, dmgBoostDict, resisted = dmgCalculator(self, entityInArea, value, use, useActionStats, danger, area, typeDmg = TYPE_DAMAGE, skillPercing = skillPercing)
								logs += "\n- Damage : " + str(damage) + " ("+ tempLog+")"

								damage = max(damage*aoeFactor,1)
								for entBooster, value2 in dmgBoostDict.items():
									if entBooster.id != self.id:
										if value2 > 0:
											if entBooster.char.__class__ not in [classes.invoc, classes.depl]: entDict[entBooster.id].stats.damageBoosted += round(value2*aoeFactor)
											else: entDict[entBooster.summoner.id].stats.damageBoosted += round(value2*aoeFactor)
											self.stats.underBoost += round(value2*aoeFactor)
										elif value2 < 0:
											if entBooster.char.__class__ not in [classes.invoc, classes.depl]: entDict[entBooster.id].stats.damageDodged += round(abs(value2*aoeFactor))
											else: entDict[entBooster.summoner.id].stats.damageDodged += round(abs(value2*aoeFactor))
									elif value2 > 0: self.stats.underBoost += round(value2*aoeFactor)
							
								entityInArea.stats.damageResisted += round(resisted*aoeFactor)
								
								for tmpEff in self.effects:
									if tmpEff.effects.id in [dmgUp.id, lenaExSkill5e.id, iliStans2_1.id, dmgDown.id] or (tmpEff.effects.id == charme.id and tmpEff.caster.id == entityInArea.id):
										incDmg = int(damage * tmpEff.effects.power/100 * [1,-1][tmpEff.effects.type in hostileTypes])
										damage += incDmg
										if tmpEff.caster.id != self.id:
											if tmpEff.caster.summoner != None: [tmpEff.caster.summoner.stats.damageBoosted, tmpEff.caster.summoner.stats.damageDodged][tmpEff.effects.type in hostileTypes] += abs(incDmg)
											else: [tmpEff.caster.stats.damageBoosted, tmpEff.caster.stats.damageDodged][tmpEff.effects.type in hostileTypes] += abs(incDmg)
										elif incDmg > 0: self.stats.underBoost += incDmg
									elif tmpEff.effects.id == backupdancerEff1.id: backupDancerFlag = tmpEff
									elif tmpEff.effects.id == backupdancerEff4.id and tmpEff.value > 0: backupbisFlag = tmpEff
								
								for tmpEff in entityInArea.effects:
									incDmg = 0
									if tmpEff.effects.id in [vulne.id,defenseUp.id,iliStans1_1.id] or tmpEff.effects.id in [krysWaterWeakness.id] and (type(skillUsed) == classes.skill and skillUsed.condition==[EXCLUSIVE,ELEMENT,ELEMENT_WATER]): incDmg = damage * tmpEff.effects.power/100 * [-1, 1][tmpEff.effects.type in hostileTypes]
									elif tmpEff.effects.id in [reaperEff.id,deathMark.id] and tmpEff.caster.id == self.id: incDmg = damage * REAPEREFFDMGBUFF/100
									elif tmpEff.effects.id in [charming.id,kitsuneExCharmEff.id,charmingHalf.id] and self.char.npcTeam == NPC_KITSUNE: incDmg = damage * {charming.id:KITCHARMVULNE, kitsuneExCharmEff.id:KITCHARM2VULNE,charmingHalf.id:KITCHARMVULNE//2}[tmpEff.effects.id] / 100
									elif tmpEff.trigger == TRIGGER_DAMAGE and not(tmpEff.effects.overhealth > 0 or tmpEff.effects.redirection > 0):
										temp = tmpEff.triggerDamage(value = damage, declancher=self, icon=icon, onArmor=onArmor)
										damage = temp[0]
										if len(noneArmorMsg) == 0 or (len(temp[1]) > 0 and noneArmorMsg[-1] == temp[1][0] == "\n"): temp[1] = temp[1][1:]
										if len(temp[1]) > 0 and self.icon not in noneArmorMsg and self.icon not in temp[1]: temp[1] = self.icon + temp[1]
										noneArmorMsg += temp[1]
									elif tmpEff.effects.overhealth > 0: tablArmor.append(tmpEff)
									elif tmpEff.effects.redirection > 0:
										if tmpEff.effects.id != lenaShuRedirect.id: tablRedirect.append(tmpEff)
										elif entityInArea.hp / entityInArea.maxHp <= 0.25: tablRedirect.append(tmpEff); blocked = True
									elif tmpEff.effects.id in LIFESAVOREFF: lifeSavor.append(tmpEff)
									elif tmpEff.effects.id == critWeaknessEff.id: critVulne += tmpEff.effects.power
									elif tmpEff.effects.id == elemResistanceEffects[1].id and (type(skillUsed) == classes.skill and len(skillUsed.condition)>0 and skillUsed.condition[:2]==[EXCLUSIVE,ELEMENT] and skillUsed.condition[2] in range(ELEMENT_FIRE,ELEMENT_EARTH+1)): incDmg = damage * ELEMENT_RESIST/100 * [-1,1][skillUsed.condition[2] == elemWeakness[entityInArea.char.element]] * ((100-ELEMENT_RESIST)/100)
									elif tmpEff.effects.id == justiceEnigmaEff.id: justEnig = tmpEff
									elif tmpEff.effects.id == hunterMarkEff.id and tmpEff.caster.id == self.id:
										tmpEff.turnLeft = tmpEff.effects.turnInit
										incDmgTmp = int(damage * tmpEff.effects.power/100 * [1,-1][tmpEff.effects.type in hostileTypes])
										damage += incDmgTmp
										if tmpEff.caster.id != self.id:
											if tmpEff.caster.summoner != None: [tmpEff.caster.summoner.stats.damageBoosted, tmpEff.caster.summoner.stats.damageDodged][tmpEff.effects.type in hostileTypes] += abs(incDmgTmp)
											else: [tmpEff.caster.stats.damageBoosted, tmpEff.caster.stats.damageDodged][tmpEff.effects.type in hostileTypes] += abs(incDmgTmp)
										elif incDmgTmp > 0: self.stats.underBoost += incDmgTmp
										huntMark = True
									incDmg = int(incDmg)
									if incDmg != 0:
										damage += incDmg
										if tmpEff.caster.id != self.id:
											if tmpEff.caster.summoner != None: [tmpEff.caster.summoner.stats.damageBoosted, tmpEff.caster.summoner.stats.damageDodged][tmpEff.effects.type not in hostileTypes] += abs(incDmg)
											else: [tmpEff.caster.stats.damageBoosted, tmpEff.caster.stats.damageDodged][tmpEff.effects.type not in hostileTypes] += abs(incDmg)
										elif incDmg > 0: self.stats.underBoost += incDmg
								entityInArea.refreshEffects()

								mulPowa = 0
								for indx, tmpChipId in enumerate(self.char.equippedChips):
									tmpChip = getChip(tmpChipId)
									if tmpChip != None:
										if tmpChip.name == "Achèvement" and entityInArea.hp/entityInArea.maxHp < 0.35: mulPowa += self.char.chipInventory[tmpChipId].power/100
										elif tmpChip.name == "Dissimulation" and entityInArea.id == target.id and entityInArea.id not in self.chipAddInfo[indx] and self.cell.distance(entityInArea.cell) == 1: mulPowa += self.char.chipInventory[tmpChipId].power/100; self.chipAddInfo[indx].append(entityInArea.id)
										elif tmpChip.name == "Bout-Portant" and entityInArea.id not in self.chipAddInfo[indx]: mulPowa += self.char.chipInventory[tmpChipId].power/100; self.chipAddInfo[indx].append(entityInArea.id)
								if mulPowa > 0: incDmg = damage * mulPowa ; damage += incDmg ; self.stats.damageBoosted += abs(incDmg)
								if TRAIT_GIANTESS in entityInArea.char.trait: incDmg = damage * 0.25 ; damage -= incDmg ; entityInArea.stats.damageDodged += abs(incDmg)

							if ((type(skillUsed) == classes.skill and skillUsed.group == SKILL_GROUP_HOLY and entityInArea.char.npcTeam in [NPC_UNDEAD,NPC_DEMON])) or (type(skillUsed) == classes.skill and skillUsed.group == SKILL_GROUP_DEMON and entityInArea.char.npcTeam in [NPC_HOLY,NPC_ANGEL]): dmgMul = dmgMul*((100+UNDEAD_WEAKNESS)/100)
							elif (use==MAGIE and entityInArea.char.npcTeam in [NPC_FAIRY]): dmgMul = dmgMul*(100-FAIRYMAGICRESIST)/100

							# Critical
							critRoll, critDmgMul, hasCrit, critRate = random.randint(0,99), 1, False, probCritDmg(self)
							if ((type(skillUsed) == classes.skill and skillUsed.garCrit and entityInArea.id == target.id) or (self.weaponEffect([eclataDash.id, eclataDash.id+"+",victoireShotgunEff.id]) and self.cell.distance(entityInArea.cell)<=1)) and entityInArea.id == target.id: critRate = 100
							logs += "\n- Crit Rate : {0}% -> ".format(round(critRate,2))
							if critRoll < critRate and damage > 0:
								critDmgMul += 0.35
								logs += "Success"
								if self.char.aspiration in [POIDS_PLUME, OBSERVATEUR]:critDmgMul += 0.10

								self.stats.crits, critMalusCmpt, critDmgMul, hasCrit = self.stats.crits+1, critMalusCmpt+1, critDmgMul+self.critDmgUp / 100, True

								if critRate > 100 or (skillUsed != None and skillUsed.garCrit and entityInArea.id == target.id):
									if skillUsed != None and skillUsed.garCrit and entityInArea.id == target.id: critDmgMul += max(probCritDmg(self),0)/100/2
									else: critDmgMul += critRate/100/2
								logs += " - Crit. Mul : {0}%".format(critDmgMul*100)
								critMsg = " !"

								if (skillUsed != None and skillUsed.garCrit and entityInArea.id == target.id): critMsg += "!"

							else: logs += "Failure"; critDmgMul += self.dmgUp / 100

							# Block
							logs += "\n- entityInArea Block Rate : {0}% -> ".format(entityInArea.blockRate)
							if type(skillUsed) == classes.skill and skillUsed.id == trans.id and entityInArea.isNpc("Iliana OvL","Nacialisla"): blocked = True
							if random.randint(0,99) > 100-entityInArea.blockRate or blocked: logs += "Success"; critMsg += " (Bloqué !)"; blocked = True
							else: logs += "Failure"

							secElemMul = 1
							if entityInArea.char.secElement == ELEMENT_LIGHT or (entityInArea.char.secElement == ELEMENT_SPACE and area != AREA_MONO) or (entityInArea.char.secElement == ELEMENT_TIME and area == AREA_MONO): secElemMul += 0.05
							if self.char.secElement == ELEMENT_LIGHT or (self.char.secElement == ELEMENT_SPACE and area != AREA_MONO) or (self.char.secElement == ELEMENT_TIME and area == AREA_MONO): secElemMul += 0.05
							if entityInArea.char.secElement == ELEMENT_DARKNESS: secElemMul -= 0.05
							if self.char.secElement == ELEMENT_DARKNESS: secElemMul -= 0.05

							if hasCrit: dmgMul = dmgMul*((100-critVulne)/100)

							dmgMul = round(dmgMul,2)
							logs += "\n- CasterDamageDeals : {0}% ; entityInAreaDamageTaken : {1}% ".format(round(secElemMul*critDmgMul*100*damageMul),(dmgMul*[1,1-((100-35)/100)][blocked])*100)
							effectiveDmg = round(damage*aoeFactor*secElemMul*critDmgMul)
							beforeDamageMul = copy.deepcopy(effectiveDmg)
							effectiveDmg, dephaReducedDmg = round(damage*aoeFactor*secElemMul*critDmgMul*dmgMul*(damageMul)),0
							blockDamage = [0,int(effectiveDmg*(0.35))][blocked]
							effectiveDmg = int(effectiveDmg-blockDamage)
							tmpMsg = ""
							logs += "\n- FinalDamage : "+str(effectiveDmg)

							brokenArmor, unbroken, lythoBonus = 0, "", 0.1 * int(TRAIT_LYTHOPHAGE in self.char.trait and TRAIT_ROCKED in entityInArea.char.trait)
							for tabl in [tablArmor,tablRedirect]:
								for eff in tabl:
									if effectiveDmg > 0:
										initValue = eff.value
										triggerReturn = eff.triggerDamage(value = effectiveDmg,declancher=self,icon=icon,onArmor=onArmor,armorSteal=armorSteal+lythoBonus)
										effectiveDmg = max(effectiveDmg-triggerReturn[0],0)
										if tabl == tablArmor:
											if eff.value <= 0:
												brokenArmor += initValue
											else:
												unbroken = triggerReturn[1]
										else:
											if self.icon not in tmpMsg:
												tmpMsg += f"{self.icon} {icon} → "+triggerReturn[1]
											else:
												tmpMsg += triggerReturn[1]
										if eff.effects.overhealth > 0 and eff.value > 0 and value > 0:
											armorStolen += triggerReturn[2]
								if tabl==tablArmor:
									if brokenArmor > 0:
										if self.icon not in tmpMsg: tmpMsg += "{0} {1} → {2}-{3} PAr ".format(self.icon,icon,["<:abB:934600555916050452>","<:abR:934600570633867365>"][entityInArea.team],brokenArmor)
										else: tmpMsg += "{0}-{1} PAr ".format(["<:abB:934600555916050452>","<:abR:934600570633867365>"][entityInArea.team],brokenArmor)
									if unbroken != "":
										if self.icon not in tmpMsg: tmpMsg += f"{self.icon} {icon} → "+unbroken
										else: tmpMsg += unbroken

							if entityInArea.hp/entityInArea.maxHp <= 0.35 and entityInArea.char.__class__ not in [classes.invoc, classes.depl] and dictHasSacrificialShield[entityInArea.team] != [] and effectiveDmg > 0:
								for ent in dictHasSacrificialShield[entityInArea.team]:
									if ent.hp > 0 and ent.id != entityInArea.id:
										redirect = int(effectiveDmg * ent.char.chipInventory[getChip("Bouclier Sacrificiel").id].power/100)
										effectiveDmg -= redirect

										tmpChip = getChip("Altruisme")
										if tmpChip.id in ent.char.equippedChips:
											redirect = int(redirect * (1-(ent.char.chipInventory[tmpChip.id].power/100)))
										
										self.indirectAttack(target=ent,value=redirect,icon=getChip("Bouclier Sacrificiel").emoji,ignoreImmunity=False,canCrit=False,redirected=True)
										triggerReturn = (redirect,"{0} -{1} PV".format(ent.icon,redirect))
										if self.icon not in tmpMsg:
											tmpMsg += f"{self.icon} {icon} → "+triggerReturn[1]
										else:
											tmpMsg += triggerReturn[1]

							mainTargetSkillIcon, toAddMsg = "", ""
							
							# CHIPS
							for indx, chipId in enumerate(self.char.equippedChips):
								tmpChip = getChip(chipId)
								if tmpChip != None:
									if entityInArea.id == target.id:
										if tmpChip.name == "Lame Dissimulée":
											effectiveDmg += int(self.char.chipInventory[tmpChip.id].power/100*self.char.level)
											mainTargetSkillIcon += tmpChip.emoji
										elif tmpChip.name == "Contre-Offensive" and self.chipAddInfo[indx] >= 5:
											effectiveDmg += int(self.char.chipInventory[tmpChip.id].power/100*self.char.level)
											self.chipAddInfo[indx] -= 5
											mainTargetSkillIcon += tmpChip.emoji
										elif tmpChip.name == "Toxiception":
											effectOnHit.append(toxiceptionEff)
									if tmpChip.name == "Diffraction" and area==AREA_MONO and len(self.getEntityInMelee(entityInArea))>=1 and type(skillUsed) == classes.skill and not(skillUsed.replay) and effectiveDmg > 35:
										difDmg = int(effectiveDmg * self.char.chipInventory[tmpChip.id].power/100)
										effectiveDmg -= difDmg
										difEff = classes.effect(tmpChip.name,"difEff",None,type=TYPE_INDIRECT_DAMAGE,area=AREA_DONUT_2,trigger=TRIGGER_INSTANT,power=difDmg,emoji=tmpChip.emoji)
										effectOnHit.append(difEff)
									elif tmpChip.name == "Lune de Sang": addedDeepwound += int(effectiveDmg*self.char.chipInventory[chipId].power/100)
									elif tmpChip.name == "Sourire Sadique" and random.randint(0,99) < (self.char.chipInventory[chipId].power * (1-(0.5*int(entityInArea.id != target.id or (skillUsed != None and skillUsed.repetition > 1))))) : toAddMsg += groupAddEffect(self, entityInArea, AREA_MONO, charme, tmpChip.emoji, effPurcent=50)

							for indx, chipId in enumerate(entityInArea.char.equippedChips):
								tmpChip = getChip(chipId)
								if tmpChip != None:
									if tmpChip.name == "Barrière":
										if entityInArea.chipAddInfo[indx] > 0:
											effectiveDmg = max(0,effectiveDmg-int(entityInArea.char.chipInventory[chipId].power*entityInArea.char.level/100))
											entityInArea.chipAddInfo[indx] -= 1

										if blocked:
											entityInArea.chipAddInfo[indx] += 1
									elif tmpChip.name == "Solidité" and effectiveDmg > entityInArea.maxHp * 0.25:
										effectiveDmg = max(0,effectiveDmg-int(entityInArea.char.chipInventory[chipId].power*entityInArea.char.level/100))
									elif tmpChip.name == "Présence":
										entityInArea.chipAddInfo[indx] += effectiveDmg * entityInArea.char.chipInventory[chipId].power/100
									elif tmpChip.name == "Dissimulation" and effectiveDmg >= 1:
										entityInArea.chipAddInfo[indx].append(self.id)
									elif tmpChip.name == "Contre-Offensive" and blocked:
										entityInArea.chipAddInfo[indx] = min(entityInArea.chipAddInfo[indx]+[1,5][self.char.standAlone],7)
									elif tmpChip.name == "Retour de Bâton":
										entityInArea.chipAddInfo[indx] += blockDamage * entityInArea.char.chipInventory[chipId].power/100
									elif tmpChip.name == "Sourire Mazo" and random.randint(0,99) < (entityInArea.char.chipInventory[chipId].power * (1-(0.5*int(entityInArea.id != target.id or (skillUsed != None and skillUsed.repetition > 1))))) : toAddMsg += groupAddEffect(entityInArea, self, AREA_MONO, charme, tmpChip.emoji, effPurcent=50)

							if lifeSavor != [] and entityInArea.hp - effectiveDmg <= 0:
								for eff in lifeSavor:
									if eff.effects.id not in [zelianR.id]:
										popipo += eff.triggeredIndHeal(decate=True)
									else:
										healMsg, why = eff.caster.heal(entityInArea,eff.icon,eff.effects.stat,eff.value,eff.name,mono=True,direct=False)
										popipo += healMsg
										eff.decate(value=99999999)

							popipo += tmpMsg

							if self.isNpc("Clémence pos.","Nacialisla") and entityInArea.hp - effectiveDmg <= 0 and entityInArea.hp / entityInArea.maxHp >= 0.3:
								effectiveDmg = entityInArea.hp - int(entityInArea.maxHp * (random.randint(1,5)/100))

							if blocked: entityInArea.stats.blockCount += 1; entityInArea.stats.damageBlocks += blockDamage
							if isDepha: dephaReducedDmg = int(effectiveDmg * jetLagEff.power / 100); effectiveDmg -= dephaReducedDmg
							if execution: effectiveDmg = entityInArea.maxHp
							if justEnig != None: tempDmg = int(effectiveDmg*(justEnig.effects.power/100)); effectiveDmg -= tempDmg; justEnig.value += tempDmg
							if huntMark: 
								addedDeepwound += int(effectiveDmg*0.15)
								try:
									if teamJaugeDict[self.team][self].effects.id == lycanJauge.id: teamJaugeDict[self.team][self].value = min(teamJaugeDict[self.team][self].value+5,100)
								except KeyError: pass
							self.stats.shootHited += 1
							if entityInArea != self:
								if type(self.char) not in [invoc,depl]: self.stats.damageDeal += effectiveDmg
								else: entDict[self.summoner.id].stats.damageDeal += effectiveDmg; entDict[self.summoner.id].stats.summonDmg += effectiveDmg
							else: self.stats.selfBurn += effectiveDmg

							sumDamage += effectiveDmg
							if type(entityInArea.char) in [invoc,depl]: sumDamage -= effectiveDmg / 2
							entityInArea.stats.numberAttacked += 1
							if not execution:
								if deepWoundConvert > 0 or addedDeepwound > 0:
									deepWoundValue = int(effectiveDmg*deepWoundConvert/100)+addedDeepwound
									if deepWoundValue > 0:
										add_effect(caster=self, target=entityInArea, effect=deepWound, setValue=deepWoundValue)
								entityInArea.refreshEffects()
								entityInArea.hp -= effectiveDmg
								entityInArea.stats.damageRecived += effectiveDmg

								for team in [0,1]:
									for jaugeEnt, jaugeEff in teamJaugeDict[team].items():
										for conds in jaugeEff.effects.jaugeValue.conds:
											if conds.type == INC_ENEMY_DAMAGED and jaugeEnt.team == self.team:
												jaugeEff.value = min(jaugeEff.value+((conds.value*effectiveDmg/entityInArea.maxHp*100)*([1,5][entityInArea.char.standAlone])),100)
											elif conds.type == INC_ALLY_DAMAGED and jaugeEnt.team == entityInArea.team:
												jaugeEff.value = min(jaugeEff.value+((conds.value*effectiveDmg/entityInArea.maxHp*100)*([1,5][entityInArea.char.standAlone])),100)

								try:
									if not(skillUsed.__class__ == classes.skill and skillUsed.jaugeEff != None and skillUsed.jaugeEff.id not in [bloodJauge.id, clemTmpBloodJauge.id]):
										for conds in teamJaugeDict[self.team][self].effects.jaugeValue.conds:
											if conds.type == INC_DEAL_DAMAGE: teamJaugeDict[self.team][self].value = min(teamJaugeDict[self.team][self].value+((conds.value*effectiveDmg/entityInArea.maxHp*100)*([1,5][entityInArea.char.standAlone])),100)
											elif conds.type == INC_ON_HIT: teamJaugeDict[self.team][self].value = min(round(teamJaugeDict[self.team][self].value+(conds.value*[0.3,1][entityInArea.id == target.id or (skillUsed == skill and skillUsed.replay) or (skillUsed != None and skillUsed.repetition > 1)]),2),100)
								except KeyError: pass
							else: entityInArea.hp = 0

							if erosion != 0 and effectiveDmg > 0:
								lostHp = int(effectiveDmg * erosion/100)
								self.stats.maxHpReduced += lostHp
								entityInArea.maxHp -= lostHp

							# Damage message
							if entityInArea.hp <= 0 and len(self.tablEntTeam[entityInArea.team]) == 1 and self.isNpc("Lia Ex"):
								popipo += "{0}{1} : \"*お前はもう死んでいる*\"\n{2} : \"*なに- !?*\"\n".format(["","\n"][len(popipo) > 0 and popipo[-2:-1] != "\n"],self.icon,entityInArea.icon)
							popipo += noneArmorMsg
							if not(execution):
								tmpIcon = ["",mainTargetSkillIcon][entityInArea.id == target.id]
								if effectiveDmg > 0 and tempToReturn == "":
									splited = (popipo+"\n").splitlines()
									if len(splited)> 0 and self.icon in splited[-1]: popipo += f" {entityInArea.icon} -{separeUnit(effectiveDmg)} PV{critMsg}\n"
									else: popipo += f"{self.icon} {icon}{tmpIcon} → {entityInArea.icon} -{separeUnit(effectiveDmg)} PV{critMsg}\n"
								elif not(entityInArea.immune): popipo += tempToReturn + f" {entityInArea.icon} -{separeUnit(effectiveDmg)} PV{critMsg}\n"
								else: popipo += f"{self.icon} {icon}{tmpIcon} → <:immunity:1063118365738160209> {entityInArea.icon} -0 PV\n" 
							else: popipo += "{0} {2} → <:sacrified:973313400056725545> {1}\n".format(self.icon,entityInArea.icon,icon)
							popipo += toAddMsg

							if deepWoundValue > 0: popipo = popipo[:-1]+ " +{0} {1}\n".format(deepWound.emoji[0][0],deepWoundValue)
							if erosion != 0 and effectiveDmg > 0: popipo += f"{self.icon} {eroTxt} → {entityInArea.icon} -{lostHp} PV max\n"

							if blocked and entityInArea.counterOnBlock > 0 and random.randint(0,99) < entityInArea.counterOnBlock: popipo += entityInArea.counter(self,entityInArea.counterOnBlock)

							if entityInArea.hp <= 0:
								lolipop = entityInArea.death(killer = self,trueDeath=execution)
								if (entityInArea.char.__class__ not in [classes.invoc, classes.depl]) or (entityInArea.char.__class__ in [classes.invoc, classes.depl] and len(lolipop.splitlines()) > 1): popipo += lolipop
								else: popipo = popipo[:-1] + " (<:splatted2:727586393173524570>)\n"
								deathCount += 1
								if execution: entityInArea.status, entityInArea.icon = STATUS_TRUE_DEATH, ["","<:aillilKill1:898930720528011314>","<:ailillKill2:898930734063046666>","<:ailillKill2:898930734063046666>"][entityInArea.char.species]

							elif len(tablTarget) <= 3:
								if self.char.says.onHit != None and random.randint(0,99) < 10: popipo += "*{0} : \"{1}\"*\n".format(self.icon,randRep(self.char.says.onHit).format(caster=self.name,target=entityInArea.name))
								if entityInArea.char.says.takeHit != None and random.randint(0,99) < 5: popipo += "*{0} : \"{1}\"*\n".format(entityInArea.icon,randRep(entityInArea.char.says.takeHit).format(caster=self.name,target=entityInArea.name))

							if isDepha:
								eff = copy.deepcopy(jetLagDmgEff)
								eff.power = dephaReducedDmg
								popipo += groupAddEffect(self, entityInArea, AREA_MONO, [eff], skillIcon=["<:jetLagB:984519444082610227>","<:jetLagR:984519461111472228>"][self.team])
							if effectOnHit != [] and entityInArea == target and entityInArea.hp > 0: popipo += groupAddEffect(caster=self, target=entityInArea, area=AREA_MONO, effect=effectOnHit, skillIcon=skillUsed.emoji,effPurcent=skillUsed.effPowerPurcent)

							if hasCrit:
								for jaugeEnt, jaugeEff in teamJaugeDict[self.team].items():
									for conds in jaugeEff.effects.jaugeValue.conds:
										if (conds.type == INC_ON_SELF_CRIT and jaugeEnt == self) or (conds.type == INC_ON_ALLY_CRIT and jaugeEnt.hp > 0) : 
											jaugeEff.value = min(round(jaugeEff.value+(conds.value*[0.3,1][entityInArea.id == target.id and (skillUsed != None and (type(skillUsed) == classes.skill and not(skillUsed.replay) or skillUsed.repetition <= 1))]),2),100)

							# After damage
							if entityInArea.char.aspiration in [PROTECTEUR,VIGILANT,ENCHANTEUR,MASCOTTE] and self.id not in entityInArea.aspiSlot:
								nbIt, cmpt = [1,5][self.char.standAlone], 0
								while cmpt < nbIt:
									entityInArea.aspiSlot.append(self.id)
									cmpt += 1

							elif self.char.aspiration == OBSERVATEUR and hasCrit:
								groupAddEffect(caster=self, target=self, area=AREA_MONO, effect=obseff)

							if (entityInArea.isNpc("Liu","Kitsune") and entityInArea.team == 1) and type(actTurn.char != classes.invoc):
								popipo += add_effect(entityInArea,actTurn,[charmingHalf,charming][blocked],skillIcon=entityInArea.weapon.effects.emoji[0][0])
								actTurn.refreshEffects()

							astraEarth = False
							for eff in entityInArea.effects:
								if eff.effects.id == flambe.id and use in [STRENGTH,ENDURANCE,AGILITY,PRECISION]:						 # Flambage
									eff.effects.power += flambe.power
								elif eff.effects.id == magAch.id and use == [MAGIE,CHARISMA,INTELLIGENCE,HARMONIE]:							# Magia
									eff.effects.power += magAch.power
								elif eff.effects.id in [pandaimaEff.id]:
									tablPanhaima.append(eff)
								elif eff.effects.id in [haimaEffect.id]:
									finded = False
									for sndEff in entityInArea.effects:
										if sndEff.effects.id == eff.effects.callOnTrigger.id:
											finded = True
											break

									if not(finded):
										popipo += add_effect(eff.caster,entityInArea,eff.effects.callOnTrigger,skillIcon=eff.icon)
										popipo += eff.decate(value = 1)
										entityInArea.refreshEffects()
								elif eff.effects.id in [mattSkill4Eff.id,lightLameEff.id,astralLameEff.id,timeLameEff.id]:
									popipo += eff.triggerDamage(value = damage,declancher=self,icon=icon,onArmor=onArmor)[1]
								elif eff.effects.id == anticipationEff2 and (type(skillUsed) == classes.skill and len(skillUsed.condition) > 1 and skillUsed.condition[1] == ELEMENT):
									popipo += add_effect(eff.caster,entityInArea,eff.effects.callOnTrigger)
									try:
										teamJaugeDict[entityInArea.team][entityInArea].value = min(teamJaugeDict[entityInArea.team][entityInArea].value+eff.effects.power,100)
									except KeyError:
										pass
								elif eff.effects.id in astraEarthEffList and not(astraEarth):
									popipo += eff.triggeredIndHeal()
									astraEarth = True
								elif eff.effects.trigger == TRIGGER_AFTER_DAMAGE:
									if eff.effects.thornEff:
										popipo =[popipo[:-1],popipo][popipo[-1]=="\n"] + eff.triggerThorn(target=self, decate=True)
									else:
										popipo = [popipo[:-1],popipo][popipo[-1]=="\n"]+ eff.triggerDamage(value = damage,declancher=self,icon=icon,onArmor=onArmor)[1]
								elif eff.effects.id == naciaGiantEff.id:
									if entityInArea.hp/entityInArea.maxHp <= 0.6 and entityInArea.clemBloodJauge == None:
										popipo += eff.decate(turn=20)
								elif eff.effects.id == deathMark.id and type(skillUsed) == classes.skill and skillUsed.jaugeEff != None and skillUsed.jaugeEff.id == planJauge.id and skillUsed.minJaugeValue > 1:
									tmpEff = classes.effect("Marque de la Mort","deathMarkTriggered",MISSING_HP,power=round(max(10,50*skillUsed.minJaugeValue/100)),type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,emoji=deathMark.emoji)
									popipo += groupAddEffect(self, entityInArea, AREA_MONO, tmpEff, tmpEff.emoji[0][0])
									eff.decate(turn=99)
								
								if eff.effects.trigger in [TRIGGER_HP_UNDER_70,TRIGGER_HP_UNDER_50,TRIGGER_HP_UNDER_25] and entityInArea.hp/entityInArea.maxHp <= triggerUnderHp[eff.effects.trigger]:
									if eff.effects.type == TYPE_INDIRECT_HEAL:
										popipo += eff.triggeredIndHeal(decate=True)
									elif eff.effects.type == TYPE_INDIRECT_DAMAGE:
										popipo += eff.triggeredIndDamage(target=eff.on,decate=True)

							if backupDancerFlag:
								totalShieldValue = 0
								for eff in entityInArea.effects:
									if eff.effects.overhealth > 0 and eff.value > 0: totalShieldValue += eff.value; break
								
								if totalShieldValue == 0:
									tmpValue = 1
									if type(skillUsed) in [classes.skill,classes.weapon] and skillUsed.onArmor != 1: tmpValue = skillUsed.onArmor
									tmpEff = classes.effect("Rupture Extrême", backupDancerFlag.effects.id+"1", HARMONIE, type=TYPE_INDIRECT_DAMAGE, trigger=TRIGGER_INSTANT, emoji=backupDancerFlag.icon, power=15+min(max(round((self.getOnArmorDmgValue(tmpValue)-1)*backupDancerFlag.effects.power),0),round(85*backupDancerFlag.effects.power/100)))
									popipo += groupAddEffect(caster=self, target=entityInArea, area=AREA_MONO, effect=tmpEff, skillIcon=backupDancerFlag.icon, actionStats=ACT_INDIRECT, effPurcent=[100,50][entityInArea.id != target.id])

									if backupbisFlag: popipo += groupAddEffect(caster=backupbisFlag.caster, target=entityInArea, area=AREA_MONO, effect=backupbisFlag.effects.callOnTrigger, skillIcon=backupbisFlag.icon, actionStats=ACT_INDIRECT); backupbisFlag.decate(value=1)
							
							if TRAIT_LYTHOPHAGE in self.char.trait and entityInArea.isNpc("Liu"):
								popipo += "{0} : *\"{1}\"*\n".format(entityInArea.icon,randRep(liuLythoReactTabl)) + entityInArea.counter(target=self) + formatKnockBack([entityInArea.knockback(target=self, power=1)], listEnt=[self], knockbackPower=1)

							try: 
								if teamJaugeDict[self.team][self].effects.id == lycanJauge.id and target.id == entityInArea.id and not (huntMark) and target.id != self.id:
									for ent in self.tablEntTeam[int(not(self.team))]:
										if ent.id != entityInArea.id:
											for eff in ent.effects:
												if eff.effects.id == hunterMarkEff.id: hadFound = True; eff.decate(turn=99); ent.refreshEffects(); break
									popipo += groupAddEffect(self, entityInArea, AREA_MONO, hunterMarkEff, teamJaugeDict[self.team][self].icon)
							except KeyError: pass

							try: 
								if teamJaugeDict[self.team][self].effects.id == bloodJauge.id and random.randint(0,99) <= [30,50][entityInArea.id == target.id] and target.id != self.id:
									popipo += groupAddEffect(self, entityInArea, AREA_MONO, bloodButterfly, teamJaugeDict[self.team][self].icon)
							except KeyError: pass

							try: 
								if teamJaugeDict[self.team][self].effects.id == planJauge.id and target.id == entityInArea.id and target.id != self.id and not(skillUsed.jaugeEff != None and skillUsed.jaugeEff.id == planJauge.id and skillUsed.minJaugeValue > 1):
									isEligible = True
									for eff in entityInArea.effects:
										if eff.effects.id == deathMark.id: isEligible = False; eff.leftTurn = deathMark.turnInit; break
									
									if isEligible: popipo += groupAddEffect(self, entityInArea, AREA_MONO, deathMark, teamJaugeDict[self.team][self].icon)
							except KeyError: pass
						else:
							logs += "Miss"
							popipo += f"{entityInArea.char.name} esquive l'attaque\n"

							if self.char.says.onMiss != None and random.randint(0,99) < 5: popipo += "*{0} : \"{1}\"*\n".format(self.icon,randRep(self.char.says.onMiss).format(caster=self.name,target=entityInArea.name))

							if entityInArea.char.says.dodge != None and random.randint(0,99) < 10: popipo += "*{0} : \"{1}\"*\n".format(entityInArea.icon,randRep(entityInArea.char.says.dodge).format(caster=self.name,target=entityInArea.name))

							for eff in entityInArea.effects:
								if eff.effects.id == squidRollEff.id and random.randint(0,99) < squidRollEff.power:
									popipo += groupAddEffect(caster=entityInArea, target=entityInArea, area=AREA_MONO, effect=squidRollEff.callOnTrigger, skillIcon=squidRollEff.emoji[0][0])

							entityInArea.stats.dodge += 1
							entityInArea.stats.numberAttacked += 1
							if entityInArea.char.aspiration == POIDS_PLUME:
								groupAddEffect(caster=entityInArea, target=entityInArea, area=AREA_MONO, effect=poidEff)

							if (entityInArea.weaponEffect([liaWeap, kitsuneWeap]) or entityInArea.isNpc("Lia Ex")) and type(self.char) not in [invoc,depl]:
								popipo += add_effect(entityInArea,actTurn,charming, skillIcon = entityInArea.weapon.effects.emoji[0][0])
								entityInArea.refreshEffects()

							for indx, chipId in enumerate(entityInArea.char.equippedChips):
								tmpChip = getChip(chipId)
								if tmpChip != None:
									if tmpChip.name == "Sourire Agile" and random.randint(0,99) < (entityInArea.char.chipInventory[chipId].power * (1-(0.5*int(entityInArea.id != target.id or (skillUsed != None and skillUsed.repetition > 1))))) : popipo += groupAddEffect(entityInArea, self, AREA_MONO, charme, tmpChip.emoji, effPurcent=50)

							if self.cell.distance(entityInArea.cell) <= 3 and random.randint(0,99) < entityInArea.counterOnDodge: popipo += entityInArea.counter(self,entityInArea.counterOnDodge)

						for eff in effDealsDamage:
							if eff.value > 0 and entityInArea.id == target.id:
								try:
									popipo += eff.triggerDamage(icon=eff.icon, declancher = entityInArea)
								except:
									eff.name

						logs += "\n\n"
				if len(tablTarget) > 0 and (self.isNpc("Liz","Kitsune")) and self.team == 1 and ((type(skillUsed) == classes.skill and skillUsed.id != kitsuneSkill4.id) or skillUsed == None):
					popipo += ["","\n"][popipo[-2:-1] != "\n"] + groupAddEffect(caster=self, target=target,area=tablTarget, effect=charming, skillIcon=self.weapon.effects.emoji[0][0])

				if armorStolen > 0 and sumDamage <= 0 and type(self.char) not in [classes.depl]:
					eff = stolenArmorEff
					eff.overhealth = armorStolen
					addingEffect(caster=self, target=self, area=AREA_MONO, effect=eff, skillIcon=icon)
					lifeStealMsg += " {1} +{0} PAr\n".format(armorStolen,eff.emoji[self.char.species-1][self.team])

				elif sumDamage > 0 and type(self.char) not in [classes.depl]:
					sumLifeSteal, aoeLifeStealBoost, aoeArmorConvertBoost, aoeLifeStealIcons, aoeArmorConvertIcons, aoeIcons = 0, skillUsed.aoeLifeSteal, skillUsed.aoeArmorConvert, [[],[skillUsed.emoji]][skillUsed.aoeLifeSteal>0], [[],[skillUsed.emoji]][skillUsed.aoeArmorConvert>0],[]

					for eff in self.effects:
						if eff.effects.id == convertEff.id :						 # Convertion :
							armorConvert += [int(eff.effects.power*0.35),eff.effects.power][area==AREA_MONO]
							armorConvertEmoji += [eff.icon]
						elif eff.effects.id in [vampirismeEff.id,undeadEff2.id,holmgangEff.id,clemTmpWeapEff.id]:
							sumLifeSteal += [int(eff.effects.power*0.35),eff.effects.power][area==AREA_MONO]
							lifeStealEmote += [eff.icon]
						elif eff.effects.id == bloodButterFlyPassifEff.id and target.team != self.team and random.randint(0,99)<eff.effects.power:
							popipo += groupAddEffect(caster=self, target=target, area=AREA_MONO, effect=eff.effects.callOnTrigger,skillIcon=eff.icon)
						elif eff.effects.id == aoeConvertEff.id:
							aoeArmorConvertBoost += [int(eff.effects.power*0.35),eff.effects.power][area==AREA_MONO]
							aoeArmorConvertIcons += [eff.icon]
						elif eff.effects.id == aoeVampirismeEff.id:
							aoeLifeStealBoost += [int(eff.effects.power*0.35),eff.effects.power][area==AREA_MONO]
							aoeLifeStealIcons += [eff.icon]

					if self.char.aspiration == BERSERK:
						sumLifeSteal += self.aspiSlot
						lifeStealEmote += [aspiEmoji[BERSERK]]
					if lifeSteal > 0:
						sumLifeSteal += lifeSteal
						lifeStealEmote += [icon]

					if self.isNpc("Clémence Exaltée"):
						sumLifeSteal = 50
						lifeStealEmote += [vampirismeEff.emoji[1][1]]

					if sumLifeSteal > 0:
						lythoBonus = 10 * int(TRAIT_LYTHOPHAGE in self.char.trait and TRAIT_ROCKED in entityInArea.char.trait)
						supposedHealPowa, moreHealPowa = sumDamage * ((sumLifeSteal+lythoBonus) / 100), 0
						healPowa, difHp = supposedHealPowa, self.hp
						temp, useless = self.heal(self,lifeStealEmote,None,healPowa,lifeSteal=True)
						if int(self.hp-difHp)>0:
							lifeStealMsg +=" +{0} PV".format(int(self.hp-difHp))

					if aoeLifeStealBoost > 0:
						tablTarget, tablEntTarget, supposedHealPowa = self.cell.getEntityOnArea(area=AREA_DONUT_2,team=self.team,wanted=ALLIES,directTarget=False,fromCell=actTurn.cell), [], int(sumDamage * skillUsed.aoeLifeSteal / 100)
						for ent in tablTarget:
							if ent.hp > 0 and ent.hp < ent.maxHp:
								healPowa = min(ent.maxHp - ent.hp, supposedHealPowa)
								temp, useless = self.heal(self,lifeStealEmote,None,healPowa,lifeSteal=True)
								tablEntTarget.append(ent)

						if tablEntTarget != []:
							tempMsg = ""
							for ent in tablEntTarget:
								if ent.icon not in aoeIcons:
									aoeIcons.append(ent.icon)

							if supposedHealPowa>0:
								aoeStealMsg += " +{0} PV".format(supposedHealPowa)

					if armorConvert > 0 or armorStolen > 0:
						lythoBonus = 10 * int(TRAIT_LYTHOPHAGE in self.char.trait and TRAIT_ROCKED in entityInArea.char.trait)
						eff = copy.deepcopy(convertArmor)

						eff.overhealth = toAdd = calShieldValue(self,self,sumDamage*((armorConvert+lythoBonus)/100),FIXE,tour)[0]+armorStolen
						groupAddEffect(caster=self, target=self, area=self, effect=eff)
						lifeStealMsg += " {1} +{0} PAr".format(toAdd,eff.emoji[self.char.species-1][self.team])

					if aoeArmorConvertBoost > 0:
						tablTarget, supposedArmor = self.cell.getEntityOnArea(area=AREA_DONUT_2,team=self.team,wanted=ALLIES,directTarget=False,fromCell=actTurn.cell), calShieldValue(self,self,sumDamage * (skillUsed.aoeArmorConvert / 100),FIXE,tour)[0]
						eff = copy.deepcopy(convertArmor)
						eff.overhealth = supposedArmor
						groupAddEffect(caster=self, target=self, area=tablTarget, effect=eff)
						if tablTarget != []:
							for ent in tablTarget:
								if ent.icon not in aoeIcons:
									aoeIcons.append(ent.icon)

							aoeStealMsg +=" {1} +{0} PAr".format(supposedArmor,convertArmor.emoji[0][self.team])

					if lifeStealMsg != "" or aoeStealMsg != "":
						entMsg = " "
						for entIcon in aoeIcons:
							entMsg+=entIcon

						tablAllIcons,allIconsEmojis = set(lifeStealEmote+armorConvertEmoji+aoeLifeStealIcons+aoeArmorConvertIcons), ""
						for txt in tablAllIcons:
							allIconsEmojis += txt

						popipo += "{0} {1} → ".format(self.icon, allIconsEmojis)+["",self.icon][len(lifeStealMsg)>0]+lifeStealMsg+entMsg+aoeStealMsg+"\n"

					if skillUsed != None and skillUsed.id == clemSkill7.id:
						nbDpt = nbHeal = nbBoost = 0
						effList = []
						for ent in tablTarget:
							if ent.hp > 0 and type(ent.char) not in [invoc, depl]:
								if ent.char.aspiration in dptAspi:
									nbDpt += 1
								elif ent.char.aspiration in healAspi+armorAspi:
									nbHeal += 1
								elif ent.char.aspiration in boostAspi:
									nbBoost += 1
						if nbDpt > 0:
							eff = copy.deepcopy(dmgUp)
							eff.power, eff.turnInit = 2.5*nbDpt, skillUsed.cooldown
							effList.append(eff)
						if nbHeal > 0:
							eff = copy.deepcopy(vampirismeEff)
							eff.power, eff.turnInit, eff.stat = 2.5*nbHeal, skillUsed.cooldown, None
							effList.append(eff)
						if nbBoost > 0:
							eff = classes.effect("Prise de Sang","clemBoost", stat=PURCENTAGE,magie=2.5*nbBoost, turnInit=skillUsed.cooldown, emoji='<:pacteDeSang:917096147452035102>')
							effList.append(eff)
						if len(effList) > 0:
							popipo += groupAddEffect(caster=self, target=self, area=AREA_MONO, effect=effList, skillIcon=skillUsed.emoji)

				if len(tablPanhaima)>0:
					tablEnt, entCaster = [], None
					for eff in tablPanhaima:
						if eff.value > 0:
							finded = False
							for sndEff in eff.on.effects:
								if sndEff.effects.id == eff.effects.callOnTrigger.id:
									finded = True
									break

							if not(finded):
								tablEnt.append(eff.on)
								eff.decate(value = 1)
								if entCaster == None:
									entCaster = eff.caster

					if len(tablEnt) > 0:
						popipo += groupAddEffect(caster=entCaster, target=entCaster, area=tablEnt, effect=eff.effects.callOnTrigger, skillIcon=eff.icon)

		return popipo, deathCount

	def startOfTurn(self) -> str: 
		"""
			The method to call when a entity start his turn.\n
			Reduce the duration of all their own ``fightEffects`` and return a ``string`` with the effectives changes
		"""
		toReturn = ""
		allReadySeen = []
		self.path, isCasting = None, False

		listIndEff, listIndHealEff, listIndLifeSteal, hpInit, tmpMsg = [], [], [], self.hp, ""
		for a in self.effects:
			# Any normals effects --------------------------------
			if a.trigger == TRIGGER_START_OF_TURN:
				hpTargetBefore, hpCasterBefore = self.hp, a.caster.hp
				ballerine = a.triggerStartOfTurn(danger)
				tmpMsg += ballerine

				if a.effects.type == TYPE_INDIRECT_DAMAGE and a.effects.area == AREA_MONO:
					listIndEff.append([a.caster.icon,a.icon,hpTargetBefore-self.hp])
					if a.caster.hp > hpCasterBefore: listIndLifeSteal.append([a.caster.icon,a.icon,a.caster.hp-hpCasterBefore])
				elif a.effects.type == TYPE_INDIRECT_HEAL and a.effects.area == AREA_MONO: listIndHealEff.append([a.caster.icon,a.icon,self.hp-hpTargetBefore])
				else: toReturn += ballerine

			elif a.effects.id == gwenCoupeEff.id:
				if random.randint(0,99) < 15:
					effect = intargetable
					toReturn += add_effect(self,self,effect)
			elif a.effects.id == smallBombEff.id:
				self.skills[0].power += self.skills[0].initPower
			if a.effects.replica != None:
				isCasting = True

			if a.effects.decateOnTurn:
				temp = a.decate(turn=1)
				if a.effects.trigger in [TRIGGER_ON_REMOVE,TRIGGER_ON_MOVE]:
					toReturn += temp

		toResetChip, toResetValue = ["Barrière"],[3]
		for indx, chipId in enumerate(self.char.equippedChips):
			tmpChip = getChip(chipId)
			if tmpChip != None:
				if tmpChip.name in toResetChip:
					for cmpt, toResetChipName in enumerate(toResetChip):
						if tmpChip.name == toResetChipName:
							self.chipAddInfo[indx] = toResetValue[cmpt]
							break
				elif tmpChip.name == "Convertion Vitale":
					tpar, effList = 0, []
					for eff in self.effects:
						if eff.effects.type == TYPE_ARMOR:
							effList.append(eff)
							tpar += eff.value

					if tpar > 0:
						maxHeal = min(self.maxHp-self.hp,int(tpar*self.char.chipInventory[tmpChip.id].power/100))
						if maxHeal > 0:
							for indx, eff in enumerate(effList):
								toReduce = min(maxHeal,eff.value)
								effList[indx].decate(value=toReduce)
							ballerine, babie = self.heal(target=self, icon=tmpChip.emoji, statUse=FIXE, power=maxHeal, effName = tmpChip.name, mono = True, direct=False)
							listIndHealEff.append([self.icon,tmpChip.emoji,maxHeal])
				elif tmpChip.name == "Présence" and self.chipAddInfo[indx] > 1:
					ballerine, babie = self.heal(target=self, icon=tmpChip.emoji, statUse=FIXE, power=min(self.maxHp-self.hp,int(self.chipAddInfo[indx])), effName = tmpChip.name, mono = True, direct=False)
					self.chipAddInfo[indx] -= babie
					listIndHealEff.append([self.icon,tmpChip.emoji,babie])
				elif tmpChip.name in ["Médaille de la Chauve-Souris","Haut-Perceur 5.1","Cadeau Explosif"] and (tour-1)%3==0 and self.hp > 0:
					toSmn = copy.deepcopy({"Haut-Perceur 5.1":killerWailSum,"Médaille de la Chauve-Souris":batInvoc,"Cadeau Explosif":smallBombSmn}[tmpChip.name])
					batHpBoost, batDmgBoost = copy.deepcopy(constEff), copy.deepcopy(dmgUp)
					batHpBoost.power, batHpBoost.stat, batHpBoost.turnInit, batHpBoost.silent = self.char.chipInventory[chipId].power, PURCENTAGE, -1, True
					batDmgBoost.power, batDmgBoost.turnInit, batDmgBoost.silent = self.char.chipInventory[chipId].power, -1, True
					toSmn.skills[-1] = classes.skill(tmpChip.name,tmpChip.name,TYPE_PASSIVE,effects=[batHpBoost,batDmgBoost],emoji=tmpChip.emoji)
					
					nonlocal time, tablAliveInvoc, logs
					cellToSummon = self.cell.getCellForSummon(AREA_DONUT_2,self.team,toSmn,self)
					if cellToSummon != None:
						self.tablEntTeam, tablAliveInvoc, time, tempBlabla = self.summon(toSmn,time,cellToSummon,self.tablEntTeam,tablAliveInvoc,ignoreLimite=True)
						toReturn += tempBlabla
						logs += "\n"+tempBlabla
					elif toSmn.npcTeam == NPC_BOMB:
						tmpEff = classes.effect("Explosion",toSmn.skills[0].id,toSmn.skills[0].use,area=toSmn.skills[0].area,type=TYPE_DAMAGE,trigger=TRIGGER_INSTANT,power=toSmn.skills[0].power,emoji=toSmn.icon[self.team])
						toReturn += groupAddEffect(caster=self, target=self, area=self, effect=tmpEff)
				elif tmpChip.name == "Retour de Bâton":
					for cmpt, tmpSkill in enumerate(self.skills):
						if tmpSkill.name == tmpChip.name:
							tmpSkill.power = int((self.char.level*self.char.chipInventory[chipId].power/100)+self.chipAddInfo[indx])
							tmpSkill.iaPow, tmpSkill.description = tmpSkill.cooldown/2 + tmpSkill.power, "Inflige **{0}** dégâts à l'ennemi ciblé".format(tmpSkill.power)
				elif tmpChip.name == "Pas Piégés" and (tour-1)%3==0:
					self.chipAddInfo[indx] = min(4,self.chipAddInfo[indx]+1)

		if self.hp > 0:
			indDmgCompilMsg, indHealCompilMsg, indLifeStealCompilMsg = "", "", ""
			if listIndEff != []:
				tablCast, tablIcons, compilDmg = [], [], 0
				for tabl in listIndEff: tablCast, tablIcons, compilDmg = tablCast + [tabl[0]], tablIcons + [tabl[1]], compilDmg + tabl[2]
				tablCast, tablIcons = list(set(tablCast)), list(set(tablIcons))
				castIcons, effIcons = "", ""
				for cast in tablCast: castIcons += cast
				for cast in tablIcons: effIcons += cast
				indDmgCompilMsg = "{0} {1} → {2} -{3} PV\n".format(castIcons, effIcons, self.icon, separeUnit(compilDmg))
			if listIndHealEff != []:
				tablCast, tablIcons, compilDmg = [], [], 0
				for tabl in listIndHealEff:
					tablCast, tablIcons, compilDmg = tablCast + [tabl[0]], tablIcons + [tabl[1]], compilDmg + tabl[2]
				if compilDmg > 0:
					tablCast, tablIcons = list(set(tablCast)), list(set(tablIcons))
					castIcons, effIcons = "", ""
					for cast in tablCast:
						castIcons += cast
					for cast in tablIcons:
						effIcons += cast
					indHealCompilMsg = "{0} {1} → {2} +{3} PV\n".format(castIcons, effIcons, self.icon, separeUnit(compilDmg))
			if listIndLifeSteal != []:
				tablCast, tablIcons, compilDmg = [], [], 0
				for tabl in listIndLifeSteal:
					tablCast, tablIcons, compilDmg = tablCast + [tabl[0]], tablIcons + [tabl[1]], compilDmg + tabl[2]
				if compilDmg > 0:
					tablCast, tablIcons = list(set(tablCast)), list(set(tablIcons))
					castIcons, effIcons = "", ""
					for cast in tablCast:
						castIcons += cast
					for cast in tablIcons:
						effIcons += cast
					indLifeStealCompilMsg = "{0} {1} → {0} +{3} PV\n".format(castIcons, effIcons, self.icon, separeUnit(compilDmg))

			toReturn += [indHealCompilMsg + indDmgCompilMsg, indDmgCompilMsg + indHealCompilMsg][self.hp<hpInit]+indLifeStealCompilMsg
		else:
			toReturn += tmpMsg

		allReadySeenID, unAffected, effNames, allReadySeenCharId = [], [], [], []

		for dictElem in self.ownEffect[:]:
			for on, eff in dictElem.items():
				for effOn in on.effects:
					if effOn.id == eff and not(effOn.effects.decateEndOfTurn) and not(effOn.effects.decateOnTurn and on.id != self.id):
						# Effect Decate
						if not(self.isNpc("Liz") and self.team == 1 and isCasting and effOn.effects.id in [charming.id,charmingHalf.id]):
							temp = effOn.decate(turn=1)
							if temp != "" and effOn.effects.trigger not in [TRIGGER_ON_REMOVE,TRIGGER_ON_MOVE]:
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

		if type(self.char) != classes.depl:
			for a in range(len(self.skills)):
				try:
					if self.cooldowns[a] > 0: self.cooldowns[a] -= 1
				except IndexError: print(self.name, self.cooldowns, a)

		try:
			for conds in teamJaugeDict[self.team][self].effects.jaugeValue.conds:
				if conds.type == INC_START_TURN: teamJaugeDict[self.team][self].value = min(teamJaugeDict[self.team][self].value+conds.value,100); break

		except KeyError: pass

		if self.hp > 0:
			if TRAIT_ARACHNOPHOBE in self.char.trait:
				for celly in self.cell.getSurrondings():
					if celly != None and celly.on != None and celly.on.char.npcTeam == NPC_SPIDER:
						arachnoEff = classes.effect("Arachnophobie","arachnoEff", stat=PURCENTAGE,strength=-10,magie=-10,charisma=-10,intelligence=-10,emoji='<:osaSmn21:1171873951673237537>',silentRemove=True)
						temp = groupAddEffect(caster=celly.on, target=self, area=AREA_MONO, effect=arachnoEff)
						if celly.on.team != self.team:
							if celly.on.char.__class__ == classes.invoc and celly.on.name.startswith("Myrlopé") and self.isNpc("Hélène"):
								if len(temp) > 0:
									temp = "{0} : *{1}*\n".format(self.icon,randRep(heleneReactMyrlope)) + temp
								temp += formatKnockBack([self.knockback(target=celly.on, power=1)], listEnt=[celly.on], knockbackPower=1)
								
							else:
								if len(temp) > 0:
									temp = "{0} : *{1}*\n".format(self.icon,randRep(aliceReactSpider)) + temp
								temp2 = self.attack(target=celly.on, value = 35, icon = "<:talonFracassant:1088958995030605834>", area=AREA_MONO, accuracy=100, use=STRENGTH)
								temp += temp2[0]
								if celly.on.summoner != None and celly.on.summoner.isNpc("Shehisa") and entDict[celly.on.summoner.id].hp > 0:
									temp2 = "{0} : *\"{1}\"*\n".format(celly.on.summoner.icon,randRep(shehisaReactAttackMyrlope)) + entDict[celly.on.summoner.id].counter(target=self)
									if len(temp)>0:
										temp += ["\n",""][temp[-1] == "\n" or temp2[0] == "\n"]+temp2
									else:
										temp += temp2
						if len(temp) > 0:
							if len(toReturn) > 0:
								toReturn += ["\n",""][toReturn[-1] == "\n" or temp[0] == "\n"]+temp
							else:
								toReturn += temp
			if TRAIT_ARACHNOPHILE in self.char.trait:
				for celly in self.cell.getSurrondings():
					if celly != None and celly.on != None and celly.on.char.npcTeam == NPC_SPIDER:
						arachnoEff = classes.effect("Arachnophile","arachnoEff", stat=PURCENTAGE,strength=10,magie=10,charisma=10,intelligence=10,emoji='<:osaSmn21:1171873951673237537>',silentRemove=True)
						temp = groupAddEffect(caster=self, target=self, area=AREA_MONO, effect=arachnoEff)
						if len(temp) > 0:
							if len(toReturn) > 0:
								toReturn += ["\n",""][toReturn[-1] == "\n" or temp[0] == "\n"]+temp
							else:
								toReturn += temp
			if self.char.npcTeam == NPC_DRYADE:
				tmpEff = classes.effect("Photosynthèse",constEff.id,PURCENTAGE,power=tour/2,strength=tour/2,endurance=tour/2,charisma=tour/2,agility=tour/2,precision=tour/2,intelligence=tour/2,magie=tour/2,emoji='<:lifeSeed:1028680000628596817>',silent=True)
				add_effect(caster=self, target=self, effect=tmpEff)
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

				ent = self.tablEntTeam[0][random.randint(0,len(self.tablEntTeam[0])-1)]
				if ent.hp > 0:
					toReturn += add_effect(self,ent,effect)
					ent.refreshEffects()
					
				cmpt += 1
		if self.char.aspiration == MASCOTTE:
			nbEnnemiHit = len(self.aspiSlot)
			if nbEnnemiHit > 0:
				self.aspiSlot = []
				mascDmgBuff = copy.deepcopy(dmgUp)
				mascDmgBuff.silent, mascDmgBuff.power, mascDmgBuff.emoji = True, min(MASC_MAX_BOOST, max(MASC_MIN_BOOST, self.char.level * MASC_LVL_CONVERT/100 * nbEnnemiHit)), uniqueEmoji(aspiEmoji[MASCOTTE])
				groupAddEffect(self, self, AREA_DONUT_4, mascDmgBuff)
		elif self.char.aspiration == ENCHANTEUR:
			nbEnnemiHit = len(self.aspiSlot)
			if nbEnnemiHit > 0:
				self.aspiSlot = []
				enchMagBuff = classes.effect("Enchanteur","enchMagBuff",silent=True,emoji=aspiEmoji[ENCHANTEUR],magie=self.baseStats[MAGIE]*min(0.05*nbEnnemiHit,0.3))
				add_effect(self, self, enchMagBuff)

		if self.team == 0:
			nbAliveAllies, lenTeam = 0, 0
			for ent in self.tablEntTeam[self.team]:
				if type(ent.char) in [classes.tmpAllie, classes.char]:
					if ent.hp > 0: nbAliveAllies += 1
					lenTeam += 1
			if tour >= LAST_DITCH_EFFORT_START_TURN or nbAliveAllies/lenTeam <= LAST_DITCH_EFFORT_START_ALLIE:
				turnPowa, alliesPowa = ((tour-LAST_DITCH_EFFORT_START_TURN)/(LAST_DITCH_EFFORT_MAX_TURN-LAST_DITCH_EFFORT_START_TURN))*LAST_DITCH_EFFORT_MAX_POWER*int(tour >= LAST_DITCH_EFFORT_START_TURN), (((nbAliveAllies/lenTeam)+LAST_DITCH_EFFORT_MAX_ALLIE)/(LAST_DITCH_EFFORT_START_ALLIE+LAST_DITCH_EFFORT_MAX_ALLIE))*LAST_DITCH_EFFORT_MAX_POWER*int(nbAliveAllies/lenTeam <= LAST_DITCH_EFFORT_START_ALLIE)
				lastDitchEffortEff = copy.deepcopy(dmgUp)
				lastDitchEffortEff.power, lastDitchEffortEff.silentRemove, lastDitchEffortEff.emoji = clamp(turnPowa,alliesPowa,LAST_DITCH_EFFORT_MAX_POWER), True, uniqueEmoji("<:lastDitchEffort:1216413813079937125>")
				groupAddEffect(caster=self, target=self, area=AREA_MONO, effect=lastDitchEffortEff)
		return toReturn

	def endOfTurn(self,danger) -> str:
		"""
			The method to call when eff entity end their turn\n
			Return eff ``string`` with all the correspondings actions
		"""
		toReturn,allReadySeen, deepWoundNb  = "",[], 0
		listIndEff, listIndHealEff, listIndLifeSteal, hpInit, tmpMsg = [], [], [], self.hp, ""
		for eff in self.effects:
			if eff.effects.id == deepWound.id:
				tmpEff = classes.effect(deepWound.name,deepWound.id+"1",power=int(eff.value*DEEP_WOUND_RATIO/100),trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji=deepWound.emoji,silentRemove=True,stackable=True)
				add_effect(caster=eff.caster, target=self, effect=tmpEff)

				for indx, tmpChipId in enumerate(eff.caster.char.equippedChips):
					tmpChip = getChip(tmpChipId)
					if tmpChip != None:
						if tmpChip.name == "Goût du Sang":
							eff.caster.chipAddInfo[indx] += tmpEff.power

				deepWoundNb += 1
				eff.value -= eff.value//2
		if deepWoundNb > 0:
			self.refreshEffects()

		for eff in self.effects:
			if eff.trigger == TRIGGER_END_OF_TURN:
				hpTargetBefore, hpCasterBefore = self.hp, eff.caster.hp
				ballerine = eff.triggerEndOfTurn(danger)
				tmpMsg += ballerine

				if eff.effects.type in [TYPE_INDIRECT_DAMAGE,TYPE_DAMAGE] and eff.effects.area == AREA_MONO:
					listIndEff.append([eff.caster.icon,eff.icon,hpTargetBefore-self.hp])
					if eff.caster.hp > hpCasterBefore:
						listIndLifeSteal.append([eff.caster.icon,eff.icon,eff.caster.hp-hpCasterBefore])
				elif eff.effects.type == TYPE_INDIRECT_HEAL and eff.effects.area == AREA_MONO:
					listIndHealEff.append([eff.caster.icon,eff.icon,self.hp-hpTargetBefore])
				else:
					toReturn += ballerine

			if eff.effects.id == tablWeapExp[0].id:
				try:
					if random.randint(0,99) < [20,100][optionChoice==OPTION_WEAPON]:
						for eff2 in tablWeapExp:
							if eff.name == eff2.name:
								toReturn += add_effect(self,self,eff.effects.callOnTrigger,skillIcon=eff.icon)
								break
				except:
					print_exc()

				if self.char.standAlone:
					eff.decate(value=max(eff.value,self.char.level//2))

			if eff.effects.decateEndOfTurn:
				eff.decate(turn=1)
		
		if self.hp > 0:
			indDmgCompilMsg, indHealCompilMsg, indLifeStealCompilMsg = "", "", ""
			if listIndEff != []:
				tablCast, tablIcons, compilDmg = [], [], 0
				for tabl in listIndEff:
					tablCast, tablIcons, compilDmg = tablCast + [tabl[0]], tablIcons + [tabl[1]], compilDmg + tabl[2]
				tablCast, tablIcons = list(set(tablCast)), list(set(tablIcons))
				castIcons, effIcons = "", ""
				for cast in tablCast:
					castIcons += cast
				for cast in tablIcons:
					effIcons += cast
				indDmgCompilMsg = "{0} {1} → {2} -{3} PV\n".format(castIcons, effIcons, self.icon, compilDmg)
			if listIndHealEff != []:
				tablCast, tablIcons, compilDmg = [], [], 0
				for tabl in listIndHealEff:
					tablCast, tablIcons, compilDmg = tablCast + [tabl[0]], tablIcons + [tabl[1]], compilDmg + tabl[2]
				if compilDmg > 0:
					tablCast, tablIcons = list(set(tablCast)), list(set(tablIcons))
					castIcons, effIcons = "", ""
					for cast in tablCast:
						castIcons += cast
					for cast in tablIcons:
						effIcons += cast
					indHealCompilMsg = "{0} {1} → {2} +{3} PV\n".format(castIcons, effIcons, self.icon, compilDmg)
			if listIndLifeSteal != []:
				tablCast, tablIcons, compilDmg = [], [], 0
				for tabl in listIndLifeSteal:
					tablCast, tablIcons, compilDmg = tablCast + [tabl[0]], tablIcons + [tabl[1]], compilDmg + tabl[2]
				if compilDmg > 0:
					tablCast, tablIcons = list(set(tablCast)), list(set(tablIcons))
					castIcons, effIcons = "", ""
					for cast in tablCast:
						castIcons += cast
					for cast in tablIcons:
						effIcons += cast
					indLifeStealCompilMsg = "{0} {1} → {0} +{3} PV\n".format(castIcons, effIcons, self.icon, compilDmg)

			toReturn += [indHealCompilMsg + indDmgCompilMsg, indDmgCompilMsg + indHealCompilMsg][self.hp<hpInit]+indLifeStealCompilMsg
		else:
			toReturn += tmpMsg

		for skilly in self.skills:
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
			self.aspiSlot = []

		if type(self.char) == invoc:
			self.leftTurnAlive -= 1
			if self.leftTurnAlive <= 0 and self.hp > 0:
				self.hp = 0
				toReturn += "{0} est désinvoqué{1}\n".format(self.char.name,self.accord())
				entDict[self.summoner.id].ownEffect = entDict[self.summoner.id].ownEffect+self.ownEffect

		for indx, chipId in enumerate(self.char.equippedChips):
			tmpChip = getChip(chipId)
			if tmpChip != None:
				if tmpChip.name == "Radiance Toxique" and self.chipAddInfo[indx] > 1:
					tmpEff = classes.effect(tmpChip.name,"radTox",FIXE,type=TYPE_INDIRECT_HEAL,lvl=int(self.chipAddInfo[indx]),trigger=TRIGGER_INSTANT,area=AREA_CIRCLE_2,emoji=tmpChip.emoji,lifeSteal=True)
					toReturn += groupAddEffect(self,self,AREA_MONO,tmpEff,tmpChip.emoji)
					self.chipAddInfo[indx] = 0
				elif tmpChip.name == "Transgression" and self.chipAddInfo[indx] >= self.maxHp:
					listNonSmnEnemy = []
					for tmpEnt in self.tablEntTeam[not(self.team)]:
						if tmpEnt.hp > 0 and type(tmpEnt.char) not in [classes.invoc, classes.depl]:
							listNonSmnEnemy.append(tmpEnt)

					tmpEff = copy.deepcopy(deepWound)
					tmpEff.power, tmpEff.stat = int(self.maxHp*self.char.chipInventory[chipId].power/100/max(len(listNonSmnEnemy),1)), FIXE
					toReturn += groupAddEffect(caster=self, target=self, area=listNonSmnEnemy, effect=tmpEff, skillIcon=self.char.chipInventory[chipId].emoji)
					self.chipAddInfo[indx] = 0
				elif tmpChip.name == "Aura Galvanisante":
					chipPow = round(self.char.chipInventory[chipId].power,2)
					tmpEff1 = classes.effect(tmpChip.name,tmpChip.name,PURCENTAGE,strength=chipPow,endurance=chipPow,charisma=chipPow,agility=chipPow,precision=chipPow,intelligence=chipPow,magie=chipPow,silentRemove=True)
					toReturn += groupAddEffect(caster=self, target=self, area=AREA_DONUT_2, effect=tmpEff1, skillIcon=tmpChip.emoji)
				elif tmpChip.name == "Ambivalance" and self.chipAddInfo[indx] > 1:
					tmpEff = classes.effect(tmpChip.name,tmpChip.name,type=TYPE_INDIRECT_DAMAGE,power=int(self.chipAddInfo[indx]*self.char.chipInventory[chipId].power/100),trigger=TRIGGER_INSTANT,emoji=tmpChip.emoji)
					toReturn += groupAddEffect(caster=self, target=self, area=AREA_LOWEST_HP_ENEMY, effect=tmpEff, skillIcon=tmpChip.emoji)
					self.chipAddInfo[indx] = 0
				elif tmpChip.name == "Goût du Sang" and self.chipAddInfo[indx] > 1:
					tmpEff = classes.effect(tmpChip.name,tmpChip.name,FIXE,type=TYPE_INDIRECT_HEAL,lvl=int(self.chipAddInfo[indx]*self.char.chipInventory[chipId].power/100),trigger=TRIGGER_INSTANT,emoji=tmpChip.emoji)
					ballerine, babie = self.heal(target=self, icon=tmpChip.emoji, statUse=None, power=int(self.chipAddInfo[indx]*self.char.chipInventory[chipId].power/100), mono = True, lifeSteal = True, direct=False)
					toReturn += ballerine
					self.chipAddInfo[indx] = 0
				elif tmpChip.name == "Dissimulation":
					self.chipAddInfo[indx] = []
		return toReturn

	def atRange(self):
		"""
			Return the entity in range of the main weapon
		"""
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
		if self.char.standAlone:
			temp = "{0} __{1}__ :\n({2} Pv /{3})\n".format(self.icon,self.char.name,separeUnit(self.hp),separeUnit(self.maxHp))
		else:
			temp = f"{self.icon} : "
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

			baseMsg = ""
			if len(prioEff) > 0:
				prioEff.sort(key=lambda ballerine: ballerine.effects.prio - (0.01* ballerine.turnLeft), reverse=True)
				toReturn = "{2}{0} {1}\n".format(prioEff[0].icon, prioEff[0].effects.name,temp)
				if len(self.tablEntTeam[self.team]) == 1:
					baseMsg = toReturn.replace(temp,"")
				else:
					return (toReturn, toReturn, toReturn)

			tabluLightIcon = ["🛡️","🩸","🩹","🔼","🔽","⏺️"]
			tabluLightValues = [nbArmor,nbIndDmg,nbIndHeal,nbBuff,nbDebuff,nbPassive]

			for cmpt in range(len(tabluLightValues)):
				if tabluLightValues[cmpt] > 0:
					ulightMsg += "{0} {1} ".format(tabluLightIcon[cmpt],tabluLightValues[cmpt])
			if normMsg == f"{self.icon} : ":
				normMsg = ""
			else:
				normMsg = normMsg + "\n"
			if self.char.standAlone and len(prioEff) > 0:
				normMsg = temp + baseMsg + normMsg.replace(temp,"")
				lightMsg = temp + baseMsg + lightMsg.replace(temp,"")
				ulightMsg = temp + baseMsg + ulightMsg.replace(temp,"")
			return (normMsg,lightMsg+[""," + ⏺️ {0}".format(nbPassive)][nbPassive > 0]+"\n",ulightMsg+"\n")
		else:
			if self.char.standAlone:
				return (temp,temp,temp)
			else:
				return ("","","")

	def accord(self): return ["","e"][self.char.gender == GENDER_FEMALE]

	async def getIcon(self,bot):
		if type(self.char) == char or (type(self.char) == tmpAllie and self.team == 0):
			if type(self.char) == char: self.icon = await getUserIcon(bot,self.char)
			elif type(self.char) == tmpAllie: self.icon = [self.char.splashIcon,self.char.icon][self.char.splashIcon == None]
		elif type(self.char) not in [invoc,depl]: self.icon = [self.char.splashIcon,self.char.icon][self.char.splashIcon == None]
		else: self.icon = self.char.icon[self.team]
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

	def summon(self,summon : invoc ,timeline, cell : cell, tablAliveInvoc : list, ignoreLimite=False):
		funnyTempVarName = ""
		summon = copy.deepcopy(summon)
		summon.color, tablSameSummon = self.char.color, []
		for ent in self.tablEntTeam[self.team]:
			if ent.char.__class__ == classes.invoc and ent.char.name.startswith(summon.name):
				tablSameSummon.append(ent)

		summon.name += " "+["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","X","Y","Z"][len(tablSameSummon)]
		sumEnt = entity(self.id, summon, self.team, False, summoner=self)
		ballerine = sumEnt.move(cellToMove=cell)
		self.tablEntTeam[self.team].append(sumEnt)

		timeline.insert(self,sumEnt)

		accord = ""
		if summon.gender == GENDER_FEMALE:
			accord="e"
		funnyTempVarName += f"{self.char.name} invoque un{accord} {summon.name}\n"+ballerine
		if summon.lifeTime > 0:
			tablAliveInvoc[self.team] += 1
			self.stats.nbSummon += 1

		nonlocal logs
		ballerine, babie = sumEnt.passiveInitialisation()
		funnyTempVarName += ballerine[1:]+["\n",""][len(ballerine[1:])<=0]
		logs += babie

		return self.tablEntTeam,tablAliveInvoc,timeline,funnyTempVarName

	def getElementalBonus(self,target,area : int,type : int):
		"""Return the elemental damage bonus"""
		if type not in [TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_ARMOR,TYPE_INDIRECT_DAMAGE]:

			firstDistMul, secAreaMul = 0, 0
			if (self.char.element in [ELEMENT_FIRE,ELEMENT_WATER,ELEMENT_UNIVERSALIS] and self.cell.distance(target.cell) > 2) or (self.char.element in [ELEMENT_EARTH,ELEMENT_AIR,ELEMENT_UNIVERSALIS] and self.cell.distance(target.cell) <=2):
				firstDistMul += DISTDMGBUFF/100
			if (self.char.element in [ELEMENT_FIRE,ELEMENT_AIR,ELEMENT_UNIVERSALIS,ELEMENT_SPACE] and area!=AREA_MONO) or (self.char.element in [ELEMENT_EARTH,ELEMENT_WATER,ELEMENT_UNIVERSALIS] and area==AREA_MONO):
				secAreaMul += AREADMGBUFF/100

			if self.char.element == ELEMENT_DARKNESS:
				firstDistMul += DARKDMGBUFF/100
			return 1+firstDistMul+secAreaMul

		return 1

	async def resurect(self, target, value : int, icon : str, danger=danger):
		if tour <= 20 and target.status != STATUS_TRUE_DEATH:
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
		else: return ""

	def getAggroValue(self,target):
		"""Return the aggro value agains the target. Made for be use as a key for sort lists"""
		if not(target.untargetable):
			aggro = [20,0][type(target.char)==invoc]										  # Base aggro value. Maybe some skills will influe on it later
			if target.char.weapon.id == grav.id: aggro += self.stats.survival

			for eff in target.effects:						   # Change the aggrolizBoomCast
				aggro += eff.effects.aggro

				if eff.effects.replica != None and type(target.char) not in [char,tmpAllie]: aggro += 25
				if eff.effects.id == charme.id and eff.caster.id == target.id: aggro += 12
			
			distance = self.cell.distance(target.cell)		  # Distance factor.
			aggro += 40-max(distance*10,40)					 # The closer the target, the greater the aggro will be.

			if target.char.aspiration in [BERSERK,POIDS_PLUME,ENCHANTEUR,PROTECTEUR]:	   # The tanks aspirations generate more aggro than the others
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

			aggro += target.stats.damageDeal//baseGainDmg*5			 # The more the target have deals damage, the more aggro he will generate
			aggro += target.stats.heals//baseGainHeal*5				  # The more the target have deals heals, the more aggro he will generate
			aggro += target.stats.shieldGived//baseGainShield*5			# The more the target have gave armor, the more aggro he will generate
			aggro += target.stats.damageBoosted//baseGainBoost*5			# The more the target have gave armor, the more aggro he will generate

			if self.isNpc("Luna ex."): 
				if target.char.element == ELEMENT_DARKNESS:
					aggro = aggro * 1.1
				if target.char.element == ELEMENT_LIGHT or target.char.secElement in [ELEMENT_DARKNESS,ELEMENT_LIGHT]:
					aggro = aggro * 1.05
			elif self.isNpc("Kiku") and target.status == STATUS_ALIVE:
				aggro = aggro * 1.2
			elif (self.char.npcTeam in [NPC_DRYADE,NPC_HOLY,NPC_ANGEL] and target.char.npcTeam == NPC_UNDEAD) or (target.char.npcTeam == NPC_DRYADE and self.char.npcTeam == NPC_UNDEAD):
				aggro = aggro * 1.25
			if (self.char.npcTeam == NPC_KITSUNE and target.char.npcTeam == NPC_GOLEM) or (self.char.npcTeam == NPC_DEMON and target.char.npcTeam in [NPC_HOLY,NPC_ANGEL]) or (self.char.npcTeam in [NPC_HOLY,NPC_ANGEL] and target.char.npcTeam in [NPC_UNDEAD, NPC_DEMON]):
				aggro = aggro * 1.5
			return int(aggro)
		else:
			return -111

	def heal(self,target, icon : str, statUse : Union[int,None], power : int, effName = None,danger=danger, mono = False, useActionStats = ACT_HEAL, lifeSteal = False, direct=True, incHealJauge=True):
		overheath, aff, toReturn, healPowa, critMsg, healBuffer, statUsed, deepWoundList, deepWoundReduced, bloodButterflyReducedMsg, affOverheal = 0, target.hp < target.maxHp, "", 0, "", {"total":0}, copy.deepcopy(statUse), [], 0, "", False
		if power > 0 and target.hp > 0:
			if useActionStats == None: useActionStats = ACT_HEAL
			if statUse not in [None,FIXE,PURCENTAGE,MISSING_HP]:
				if statUse == HARMONIE: statBucket = max(self.allStats())
				else: statBucket = self.allStats()[statUse]

				healPowa, elemMul = calHealPower(self,target,power, 1 ,statBucket,useActionStats,danger), 1
				if self.char.element in [ELEMENT_LIGHT,ELEMENT_UNIVERSALIS,ELEMENT_WATER]: elemMul += {ELEMENT_LIGHT:LIGHTHEALBUFF,ELEMENT_UNIVERSALIS:LIGHTHEALBUFF,ELEMENT_WATER:AREADMGBUFF}[self.char.element]/100
				elif self.char.element in [ELEMENT_TIME] and not(direct): elemMul += TIMEDMGBUFF/100

				if self.weaponEffect(elinaWeapEff.id):
					if mono: healPowa = int(healPowa * (1+(eff.power/100)))
					else: healPowa = int(healPowa * (1-((eff.power*1.5)/100)))
				
				healPowa, critRate = int(healPowa*elemMul), probCritHeal(self,target)

				if random.randint(0,99) < critRate:
					critBonus = 1.25 + self.critHealUp/100
					if critRate > 100:
						critBonus = critBonus * critRate/100
					healPowa = int(healPowa/critBonus)
					critMsg = " !"
					self.stats.critHeal += 1
				self.stats.nbHeal += 1
				healPowaInit = copy.deepcopy(healPowa)

				incurableValue, healBonus, attIncurPower, bloodButterflyFlag, fireIncur = 0, 1+(5/100*int(not(self.auto))), 0, None, 0

				for eff in target.effects:
					if eff.effects.id == incurable.id: incurableValue = max(incurableValue,eff.effects.power)
					elif eff.effects.id == undeadEff2.id: healBonus += eff.effects.power/100
					elif eff.effects.type == TYPE_INDIRECT_DAMAGE:
						if eff.caster.char.aspiration == ATTENTIF: attIncurPower += eff.effects.power
						if eff.caster.char.secElement == ELEMENT_FIRE: fireIncur += FIREINCURVALUE
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
					elif eff.effects.id == bloodButterfly.id: bloodButterflyFlag = eff
					elif eff.effects.id == deepWound.id: deepWoundList.append(eff)
				for eff in self.effects:
					if statUsed not in [HARMONIE]:
						effUsedStat = eff.effects.allStats()[statUsed]
						if effUsedStat > 0:
							diff = (statBucket-effUsedStat)/[statBucket,1][statBucket == 0]
							finded = False
							for key in healBuffer:
								if key == eff.caster:
									healBuffer[key][1] += diff
									finded = True
									break
							if not(finded): healBuffer[eff.caster] = [0,diff]

				healBonus -= (incurableValue/100 + min(attIncurPower/1000,0.3))
				healBonus = max(healBonus,0.1)

				healPowa = int(healPowa * (100-target.healResist)/100 * (1 + HEALBONUSPERLEVEL*self.level) * healBonus * (1-(min(fireIncur,30)/100)))
				if bloodButterflyFlag != None and healPowa > 0:
					reducedHeals = int(healPowa * (bloodButterflyFlag.effects.power / 100))
					entDict[bloodButterflyFlag.caster.id].stats.healReduced += reducedHeals
					bloodButterflyFlag.value += reducedHeals
					healPowa -= reducedHeals
					bloodButterflyReducedMsg = " {0} -{1}".format(bloodButterflyFlag.icon, reducedHeals)

					tmpEff = classes.effect("Vol de Soins","bloodButterflyLifeSteal",FIXE,type=TYPE_INDIRECT_HEAL,lvl=reducedHeals,turnInit=20,trigger=TRIGGER_START_OF_TURN,emoji='<:bloodButterflyHealing:1257770648277618770>',lifeSteal=True)

					addingEffect(caster=bloodButterflyFlag.caster, target=bloodButterflyFlag.caster, area=AREA_MONO, effect=tmpEff, skillIcon=tmpEff)
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
			elif statUse in [None,FIXE]:
				incurableValue, bloodButterflyFlag = 0, None
				for eff in target.effects:
					if eff.effects.id == incurable.id: incurableValue = max(incurableValue,eff.effects.power)
					elif eff.effects.id == bloodButterfly.id: bloodButterflyFlag = eff
					elif eff.effects.id == deepWound.id: deepWoundList.append(eff)
				
				healPowa = power*(100-incurableValue)/100
				overheath = max(0, healPowa - (target.maxHp-target.hp))
				healPowa = min(target.maxHp-target.hp,healPowa)

				if bloodButterflyFlag != None and healPowa > 0:
					reducedHeals = int(healPowa * (bloodButterflyFlag.effects.power / 100))
					entDict[bloodButterflyFlag.caster.id].stats.healReduced += reducedHeals
					healPowa -= reducedHeals
					tmpEff = classes.effect("Vol de Soins", "bloodButterflyLifeSteal", FIXE, type=TYPE_INDIRECT_HEAL, lvl=reducedHeals, turnInit=20, trigger=TRIGGER_START_OF_TURN, emoji='<:bloodButterflyHealing:1257770648277618770>', lifeSteal=True)
					addingEffect(caster=bloodButterflyFlag.caster, target=bloodButterflyFlag.caster, area=AREA_MONO, effect=tmpEff, skillIcon=tmpEff)

				if lifeSteal:
					healPowa = healPowa*(1-(self.healResist/100))
					healPowaInit = copy.deepcopy(healPowa)
					if type(self.char) != octarien: target.healResist += int(healPowa/target.maxHp/2.5*100)
					else: target.healResist += int(healPowa/target.maxHp/1.5*100)
				else: healPowaInit = copy.deepcopy(healPowa)
			elif statUse == MISSING_HP: healPowa = round((target.maxHp-target.hp)*power/100)
			else: healPowa = round(target.maxHp*power/100)
			healPowa = int(round(healPowa))

			if not(lifeSteal):
				if type(self.char) not in [invoc,depl]:
					self.stats.heals += healPowa
				else:
					entDict[self.summoner.id].stats.heals += healPowa
					entDict[self.summoner.id].stats.summonHeal += healPowa
			else:
				self.stats.lifeSteal += healPowa

			if len(deepWoundList)>0:
				for eff in deepWoundList:
					reduced = 0
					if eff.value > 0:
						if eff.value >= healPowa:
							reduced += healPowa
							eff.decate(value=healPowa)
							healPowa = 0
						else:
							reduced += eff.value
							healPowa -= eff.value
							eff.decate(value=eff.value+1)
						entDict[eff.caster.id].stats.healReduced += int(reduced)
					for indx, tmpChipId in enumerate(eff.caster.char.equippedChips):
						tmpChip = getChip(tmpChipId)
						if tmpChip != None:
							if tmpChip.name == "Goût du Sang":
								eff.caster.chipAddInfo[indx] += reduced
					deepWoundReduced += int(reduced)
				deepWoundReduced = int(deepWoundReduced)
				target.refreshEffects()
			target.hp += healPowa
			target.stats.healingRecived += healPowa

			toLook1, toLook2, chipMul, flagNiceSmile = [self.char.equippedChips], [self.chipAddInfo], 1, False
			if self.char.__class__ in [classes.invoc, classes.depl]: toLook1, toLook2, chipMul = [entDict[self.summoner.id].char.equippedChips], [entDict[self.summoner.id].chipAddInfo], 0.4
			for indx, tmpChipId in enumerate(toLook1[0]):
				tmpChip = getChip(tmpChipId)
				if tmpChip != None:
					try:
						if tmpChip.name == "Transgression": toLook2[0][indx] += healPowa*[1,0.5][not(mono and direct)]*chipMul
						elif tmpChip.name == "Ambivalance":
							if not(direct): toLook2[0][indx] += healPowa*0.4*chipMul
							elif not(mono): toLook2[0][indx] += healPowa*0.65*chipMul
							else: toLook2[0][indx] += healPowa*chipMul
						elif tmpChip.name == "Sourire Bienveillant" and random.randint(0,99) < self.char.chipInventory[tmpChip.id].power: flagNiceSmile = True
					except: print(self.char.chipInventory.keys()); raise

			add = ""
			if effName != None: add = " ({0})".format(effName)

			if healPowa > 0 or deepWoundReduced > 0 or bloodButterflyReducedMsg != "":
				deepWoundMsg = [""," {0} -{1}".format(deepWound.emoji[0][0],int(deepWoundReduced))][deepWoundReduced > 0]
				toReturn = f"{self.icon} {icon} → {target.icon}{deepWoundMsg}{bloodButterflyReducedMsg} +{separeUnit(healPowa)} PV{critMsg}\n"

				if healPowa > 0:
					if target.id != self.id and self.id == actTurn.id and target.char.says.getHealed != None and random.randint(0,99) < 10:
						toReturn += "*{0} : \"{1}\"*\n".format(target.icon,randRep(target.char.says.getHealed).format(caster=self.name,target=target.name))

					for team in [0,1]:
						for jaugeEnt, jaugeEff in teamJaugeDict[team].items():
							for conds in jaugeEff.effects.jaugeValue.conds:
								if conds.type == INC_ALLY_HEALED and jaugeEnt.team == self.team:
									jaugeEff.value = min(jaugeEff.value+(conds.value*healPowa/target.maxHp),100)
								elif conds.type == INC_ENEMY_HEALED and jaugeEnt.team != self.team:
									jaugeEff.value = min(jaugeEff.value+(conds.value*healPowa/target.maxHp),100)

					if incHealJauge:
						try:
							for conds in teamJaugeDict[self.team][[self,self.summoner][type(self.char) in [invoc,depl]]].effects.jaugeValue.conds:
								if conds.type == INC_DEAL_HEALING or (conds.type == INC_LIFE_STEAL and lifeSteal):
									teamJaugeDict[self.team][[self,self.summoner][type(self.char) in [invoc,depl]]].value = min(teamJaugeDict[self.team][[self,self.summoner][type(self.char) in [invoc,depl]]].value+(conds.value*(healPowa/target.maxHp*100))*(1-(0.5*int(direct))),100)
						except KeyError:
							pass

					if self.char.secElement == ELEMENT_WATER and target.id != self.id and direct and not(lifeSteal):
						subWaterEff.lvl = int(healPowa * (WATERRETURNVALUE/100))
						addingEffect(caster=self, target=self, area=self, effect=subWaterEff, skillIcon=elemEmojis[ELEMENT_WATER])
			if overheath > 0:
				tmpChip = getChip("Sur-Vie")
				tablEff, tablBool = [idoOHArmor,proOHArmor,altOHArmor,overshieldEff],[idoOHEff.id in self.specialVars,proOHEff.id in self.specialVars, altOHEff.id in self.specialVars, tmpChip != None and tmpChip.id in target.char.equippedChips]
				for cmpt in range(len(tablBool)):
					if tablBool[cmpt]:
						affOverheal = True
						tmpEff = copy.deepcopy(tablEff[cmpt])
						tmpEff.overhealth = int(overheath * ([idoOHEff.power,proOHEff.power,altOHEff.power,100,50][cmpt]/100))
						addingEffect(caster=target, target=target, area=AREA_MONO, effect=tmpEff)
						if toReturn != "": toReturn = toReturn[:-1] + " {0} +{1} PAr\n".format(tmpEff.emoji[0][target.team],tmpEff.overhealth)
						else: toReturn = "{0} {1} → {2} {4} +{3} PAr\n".format(self.icon,icon,target.icon,tmpEff.overhealth,tmpEff.emoji[0][target.team])
				aff = True

			if  self.weaponEffect([lioWeap, kitsuneWeap]) and self.team == 1 and type(target.char != classes.invoc):
				toReturn += add_effect(self, target, charming2, self.char.weapon.effects.emoji[0][0], skillIcon=self.char.weapon.effects.emoji[0][0], effPowerPurcent=[50,100][direct])
				target.refreshEffects()

			elif flagNiceSmile:
				toReturn += add_effect(self,target,enjole,getChip("Sourire Bienveillant").emoji,skillIcon=getChip("Sourire Bienveillant").emoji)
				target.refreshEffects()

			for eff in target.effects:
				if eff.effects.id == shareTabl[0].id and mono and direct:
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
		if aff: return toReturn, healPowa+[0,overheath][affOverheal]
		else: return "", healPowa+[0,overheath][affOverheal]

	def isNpc(self, *name : str) -> bool:
		"""Return if the entity is a temp's with the name given"""
		tablToSee = []
		for tmp in name:
			if type(tmp) in [list,set,tuple]:
				for tmp2 in tmp: tablToSee.append(tmp2)
			else: tablToSee.append(tmp)

		for namy in tablToSee:
			if namy.__class__ != str: namy = namy.name
			if self.char.isNpc(namy): return True
		return False

	def getCellToMove(self,cellToMove:cell=None,lastCell:cell=None):
		if cellToMove == None:
			tablOfEnt = self.cell.getEntityOnArea(area=AREA_ALL_ENEMIES-int(self.char.weapon.target==ALLIES),team=self.team,wanted=self.char.weapon.target,lineOfSight=self.char.weapon.target==ENEMIES,fromCell=actTurn.cell,ignoreInvoc = True,directTarget=True)

			if len(tablOfEnt) == 0:
				return None
			tablOfEnt.sort(key=lambda ent:self.cell.distance(ent.cell))
			cellToMove = tablOfEnt[0].cell
		surrondings = self.cell.getSurrondings()
		try:
			canMove = [surrondings[0] != None and surrondings[0].on == None, surrondings[1] != None and surrondings[1].on == None, surrondings[2] != None and surrondings[2].on == None, surrondings[3] != None and surrondings[3].on == None]
			if lastCell != None:
				for indx, val in enumerate(canMove):
					if surrondings[indx] != None and surrondings[indx].id == lastCell.id: canMove[indx] = False
		except: print("getCellToMove :" +str(surrondings)); raise
		if self.cell.x - cellToMove.x > 0 and canMove[0]: return surrondings[0]			   # If the target is forward and we can move forward
		elif self.cell.x - cellToMove.x < 0 and canMove[1]: return surrondings[1]			 # Elif the target is behind and we can move behind
		elif self.cell.y - cellToMove.y > 0 and canMove[2]: return surrondings[2]			 # Elif the target is above and we can move up
		elif self.cell.y - cellToMove.y < 0 and canMove[3]: return surrondings[3]			 # Elif the target is under and we can move down
		elif canMove[2]: return surrondings[2]												# Else, if we can move up, go up
		elif canMove[3]: return surrondings[3]												# Else, if we can move down, go down
		else: return None																	 # Else, give up

	def knockback(self, target, power:int, fromEnt=None):
		toReturn, dmg, fromEnt, toReturnStr = {}, 0, [fromEnt,self][fromEnt==None], ""
		if target.chained or TRAIT_GIANTESS in target.char.trait: return (toReturn, toReturnStr)
		axis = getDirection(target.cell,fromEnt.cell)
		
		posArea = []
		for cellule in tablAllCells:
			if axis == getDirection(cellule, target.cell) and target.cell.distance(cellule) <= power: posArea.append(cellule)

		if len(posArea) > 0: posArea.sort(key=lambda dist:target.cell.distance(dist))

		cmpt = 0
		cellToPush = target.cell
		while cmpt < len(posArea) and posArea[cmpt].on == None:
			cellToPush = posArea[cmpt]
			cmpt += 1

		initTagetCell = target.cell
		if cellToPush != target.cell:
			toReturnStr += target.move(cellToMove=cellToPush)
			for indx, chipId in enumerate(target.char.equippedChips):
				tmpChip = getChip(chipId)
				if tmpChip != None:
					if tmpChip.name == "Pas Piégés" and target.chipAddInfo[indx] > 0:
						tmpDepl = copy.deepcopy(littleTrapDepl)
						tmpDepl.skills = copy.deepcopy(tmpDepl.skills)
						tmpDepl.skills.power = target.char.chipInventory[tmpChip.id].power
						target.smnDepl(tmpDepl,initTagetCell)
						target.chipAddInfo[indx] -= 1
			try:
				for conds in teamJaugeDict[self.team][self].effects.jaugeValue.conds:
					if conds.type == INC_PER_PUSH:
						teamJaugeDict[self.team][self].value = min(teamJaugeDict[self.team][self].value+(conds.value*cellToPush.distance(initTagetCell)),100)
			except KeyError:
				pass

		liaExBuff = 1 + 0.3*int(self.isNpc("Lia Ex"))

		if cmpt < power:
			lastingPower = power-initTagetCell.distance(cellToPush)
			elemBonus = 1
			if self.char.secElement == ELEMENT_AIR:
				elemBonus += AIRPUSHDMG/100

			stat,damageBase = -100,10*lastingPower*liaExBuff*elemBonus

			for stats in self.allStats():
				if self.char.standAlone and stats == self.allStats()[ENDURANCE]:
					stat = max(stats,stat)

			badaboum = [target]
			if cmpt < len(posArea) and posArea[cmpt].on != None:
				badaboum.append(posArea[cmpt].on)
			for boom in badaboum:
				dmgBase = damageBase
				if eff in boom.effects:
					if eff.effects.id == [bonkWeakness.id]:
						dmgBase = dmgBase * eff.effects.power / 100
				damage, tempLogs = indirectDmgCalculator(self,boom,dmgBase,HARMONIE,[100,danger][self.team==1],AREA_MONO)
				try:
					toReturn[self][0].append(boom)
					toReturn[self][1].append(damage)
				except KeyError:
					toReturn[self] = [[boom],[damage],[]]
				self.indirectAttack(boom,value=damage,name="Collision")
				if lastingPower >= 3 and boom.team != self.team:
					ballerine = add_effect(caster=self,target=boom,effect=lightStun,start="Collision")
					if '🚫' not in ballerine and ballerine != "":
						toReturn[self][2].append(boom)
				try:
					for conds in teamJaugeDict[self.team][self].effects.jaugeValue.conds:
						if conds.type == INC_COLISION:
							teamJaugeDict[self.team][self].value = min(teamJaugeDict[self.team][self].value+conds.value,100)
				except KeyError:
					pass

		return (toReturn, toReturnStr)

	def jumpBack(self, power:int, fromCell:cell):
		toReturn, initCell = "", self.cell
		if self.chained:
			return toReturn

		axis = getDirection(self.cell,fromCell)
		posArea = []
		for cellule in tablAllCells:
			if axis == getDirection(cellule, self.cell) and self.cell.distance(cellule) <= power:
				posArea.append(cellule)

		if len(posArea) > 0:
			posArea.sort(key=lambda dist:self.cell.distance(dist), reverse=True)

		cmpt = 0
		cellToPush = self.cell
		while cmpt < len(posArea) and posArea[cmpt].on == None:
			cellToPush = posArea[cmpt]
			cmpt += 1

		initTagetCell = self.cell
		if cellToPush != self.cell:
			toReturn += self.move(cellToMove=cellToPush)
			try:
				for conds in teamJaugeDict[self.team][self].effects.jaugeValue.conds:
					if conds.type == INC_JUMP_BACK:
						teamJaugeDict[self.team][self].value = min(teamJaugeDict[self.team][self].value+(conds.value*cellToPush.distance(initTagetCell)),100)
			except KeyError:
				pass

		if initCell.id != self.cell.id:
			toReturn = "\n__{0} ({1})__ saute de {2} case{4} en arrière\n".format(self.char.name,self.icon,power,self.accord(),["","s"][int(power>1)])
			for eff in self.effects:
				if eff.effects.id == squidRollEff.id:
					toReturn += groupAddEffect(caster=self, target=self, area=AREA_MONO, effect=squidRollEff.callOnTrigger, skillIcon=squidRollEff.emoji[0][0])

		return toReturn

	def pull(self, target, power:int):
		toReturn = ""
		if target.chained or TRAIT_GIANTESS in target.char.trait:
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
		
		if cmpt > 0:
			toReturn = "__{0} ({1})__ est attiré{3} vers {4}\n".format(target.char.name,target.icon,power,target.accord(),self.char.name)
		initTagetCell = target.cell
		if cellToPush != target.cell:
			toReturn += target.move(cellToMove=cellToPush)

			for indx, chipId in enumerate(target.char.equippedChips):
				tmpChip = getChip(chipId)
				if tmpChip != None:
					if tmpChip.name == "Pas Piégés" and target.chipAddInfo[indx] > 0:
						tmpDepl = copy.deepcopy(littleTrapDepl)
						tmpDepl.skills = copy.deepcopy(tmpDepl.skills)
						tmpDepl.skills.power = self.char.chipInventory[tmpChip.id].power
						toReturnStr += target.smnDepl(tmpDepl,initTagetCell)
						target.chipAddInfo[indx] -= 1

		return toReturn

	def quickEvent(self, stat:int, required:int,danger:int=100, effIfFail: classes.effect = None, fromEnt=None):
		toReturn = "\n__Maneuvre Critique !__"

		required = required*0.2 + (required*0.8/50*self.char.level)
		accuracyTaux = min(1000,1000 * (self.allStats()[stat]/required))

		if random.randint(0,999) < accuracyTaux:
			toReturn += "\n{0} a réussi sa maneuvre critique !".format(self.char.name)
			return toReturn, True
		else:
			toReturn += "\n{0} a échoué sa maneuvre critique...\n".format(self.char.name)
			if effIfFail != None:
				toReturn += add_effect(fromEnt,self,effIfFail,danger=danger)
				self.refreshEffects()
				return toReturn, False

	def actionStats(self): return [self.negativeHeal, self.negativeBoost, self.negativeShield, self.negativeDirect, self.negativeIndirect]

	def smnDepl(self,depl,cell):
		if cell.depl == None:
			depl = copy.deepcopy(depl)
			deplEnt = entity(identifiant=self.id, character = depl, team=self.team, player=False, auto=True, danger=100 , summoner=self, cell=cell)
			cell.depl = deplEnt
			deplTabl.append([deplEnt,cell,cell.getArea(area=[depl.skills.area,depl.triggerArea][depl.trap],team=self.team,fromCell=cell)])
			if depl.lifeTime > 0:
				self.stats.nbSummon += 1
			if (deplEnt.skills.type in [TYPE_BOOST,TYPE_MALUS] and deplEnt.skills.effects != [None]) or (deplEnt.skills.effectAroundCaster != None and deplEnt.skills.effectAroundCaster[0] in [TYPE_BOOST,TYPE_MALUS]):
				tempEffList = []
				for eff in deplEnt.skills.effects:
					if eff != None and eff.type in [TYPE_BOOST,TYPE_MALUS]:
						effCopy = copy.deepcopy(eff)
						effCopy.turnInit = 1
						tempEffList.append(effCopy)
				if deplEnt.skills.effectAroundCaster != None and deplEnt.skills.effectAroundCaster[0] in [TYPE_BOOST,TYPE_MALUS]:
						effCopy = copy.deepcopy(deplEnt.skills.effectAroundCaster[2])
						effCopy.turnInit = 1
						tempEffList.append(effCopy)

				ballerine = groupAddEffect(caster=deplEnt, target=deplEnt, area=deplEnt.skills.area, effect=tempEffList, actionStats=deplEnt.skills.useActionStats, effPurcent = deplEnt.skills.effPowerPurcent)
				nonlocal logs
				logs += ballerine

	def counter(self,target,counterOnDodge=0):
		try: canCounter = target.id not in counterTracker[self]
		except KeyError: counterTracker[self], canCounter = [], True

		if canCounter:
			actStat, tablActStats = ACT_INDIRECT, [self.negativeHeal,self.negativeBoost,self.negativeShield,self.negativeDirect,self.negativeIndirect]
			for cmpt in range(len(tablActStats)):
				if tablActStats[cmpt] < tablActStats[actStat]:
					actStat = cmpt 

			counterDmgBuff = max(0,counterOnDodge/100)
			if self.cell.distance(target.cell) > 2: counterDmgBuff -= 0.5
			if self.isNpc("Lia Ex"): counterDmgBuff += 0.3
			if self.team == target.team: counterDmgBuff -= 0.5

			damage, tempLogs = indirectDmgCalculator(self, target, COUNTERPOWER*(1+counterDmgBuff), HARMONIE, danger, area=AREA_MONO, useActionStat=actStat)
			if not(self.isNpc("Lia Ex")): counterTracker[self].append(target.id)

			toReturn = self.indirectAttack(target,value=damage,icon = [self.char.counterEmoji,self.char.weapon.emoji][self.char.counterEmoji == None],name="Contre Attaque")
			if counterTimeEff.id in self.specialVars:
				toReturn += groupAddEffect(caster=self, target=target, area=AREA_MONO, effect=counterTimeEff.callOnTrigger, skillIcon=counterTimeEff.emoji[0][0])
			return toReturn
		else: return ""

	async def changeNpc(self,char: Union[classes.char,classes.octarien,classes.tmpAllie,classes.invoc]):
		for eff in self.effects:
			if eff.caster.id == self.id and eff.effects.turnInit == -1:
				self.effects.remove(eff)
				try:
					eff.caster.ownEffect.remove({self:eff.id})
				except:
					pass

		actOwner, actTeam = self.char.owner, self.char.team
		self.char = char
		self.skills = self.char.skills
		self.char.owner, self.char.team = actOwner, actTeam
		self.weapon = self.char.weapon
		if type(self.char) not in [invoc, depl]: self.icon = await self.getIcon(bot)
		else: self.icon = self.char.icon[team]

		if type(self.char) not in [invoc,octarien]:
			baseHP,HPparLevel = BASEHP_PLAYER, HPPERLVL_PLAYER
		elif type(self.char) == invoc:
			baseHP, HPparLevel, self.char.level = BASEHP_SUMMON, HPPERLVL_SUMMON, self.summoner.char.level
		elif not(self.char.standAlone):
			baseHP,HPparLevel = BASEHP_ENNEMI, HPPERLVL_ENNEMI
		elif type(self.char) == depl:
			baseHP,HPparLevel = 9999999,9999
		else:
			baseHP,HPparLevel = BASEHP_BOSS, HPPERLVL_BOSS

		if type(self.char) != depl: # Skill Verif
			for a in [0,1,2,3,4,5,6]:
				try:
					tmpSkill = findSkill(self.skills[a])
					if type(tmpSkill) == skill:
						if self.char.element == ELEMENT_SPACE:
							for cmpt in range(len(horoSkills)):
								if tmpSkill == horoSkills[cmpt]:
									tmpSkill = altHoroSkillsTabl[cmpt]
				except IndexError:
					self.skills.append(None)

		self.name = self.char.name
		self.aspiration = self.char.aspiration

		actHp = self.hp/self.maxHp
		self.init_stats()
		self.hp = int(self.maxHp*actHp)

		return self.passiveInitialisation()

	def summonMemoria(self, target, tablAliveInvoc: List[list], timeline):
		if type(self.char, ) == invoc: return ""
		else:
			smn, toReturn = copy.deepcopy(memoria), ""
			if target.char.team != NPC_UNDEAD:
				smn.strength, smn.endurance, smn.charisma, smn.agility, smn.precision, smn.intelligence, smn.magie, smn.percing, smn.critical = round(target.baseStats[STRENGTH]*MEMORIASTATCONVERT), round(target.baseStats[ENDURANCE]*MEMORIASTATCONVERT), round(target.baseStats[CHARISMA]*MEMORIASTATCONVERT), round(target.baseStats[AGILITY]*MEMORIASTATCONVERT), round(target.baseStats[PRECISION]*MEMORIASTATCONVERT), round(target.baseStats[INTELLIGENCE]*MEMORIASTATCONVERT), round(target.baseStats[MAGIE]*MEMORIASTATCONVERT), round(target.baseStats[PERCING]*MEMORIASTATCONVERT), round(target.baseStats[CRITICAL]*MEMORIASTATCONVERT)
				smn.aspiration, smn.element, smn.secElement, smn.says = target.char.aspiration, target.char.element, target.char.secElement, target.char.says
				smn.weapon.range, smn.skills = target.char.weapon.range, target.skills
				smn.level, smn.stars = target.char.level, target.char.stars

				for indx, tmpSkill in enumerate(target.skills):
					if type(tmpSkill) == classes.skill:
						if tmpSkill.id in [inMemoria.id, selfMemoria.id] or (tmpSkill.type == TYPE_PASSIVE and findEffect(tmpSkill.effects[0]) != None and findEffect(tmpSkill.effects[0]).type == TYPE_SUMMON): self.skills[indx] = None 


				cellToSummon = self.cell.getCellForSummon(AREA_CIRCLE_4,self.team,smn,self)
				if cellToSummon != None:
					self.tablEntTeam, tablAliveInvoc, timeline, funnyTempVarName = actTurn.summon(smn, timeline, cellToSummon,self.tablEntTeam,tablAliveInvoc,ignoreLimite=True)
					toReturn += funnyTempVarName
			return toReturn

	def tpCac(self, target, behind=False):
		if not(self.chained):
			surrond, toReturn = target.cell.getSurrondings(), ""
			for a in surrond[:]:
				if a == None or (a != None and a.on != None):
					surrond.remove(a)

			if len(surrond) > 0:
				initCell = self.cell
				surrond.sort(key=lambda celly:self.cell.distance(celly),reverse=behind)
				toReturn += "__{0}__ saute {2} de __{1}__\n".format(self.name,target.name,["devant","derrière"][behind])
				toReturn += self.move(cellToMove=surrond[0])
				try:
					for conds in teamJaugeDict[self.team][self].effects.jaugeValue.conds:
						if conds.type == INC_JUMP_PER_CASE:
							teamJaugeDict[self.team][self].value = min(teamJaugeDict[self.team][self].value+(conds.value*initCell.distance(self.cell)),100)
				except KeyError:
					pass

				for eff in self.effects:
					if eff.effects.id == squidRollEff.id:
						toReturn += groupAddEffect(caster=self, target=self, area=AREA_MONO, effect=squidRollEff.callOnTrigger, skillIcon=squidRollEff.emoji[0][0])

			else:
				toReturn += "__{0}__ saute devant de __{1}__, sans succès\n".format(self.name,target.name)
		else:
			toReturn = ""

		return toReturn

	def passiveInitialisation(self):
		if self.isNpc("Clémence"):
			isBossAgaints, listBossNames = False, []
			for ent in self.tablEntTeam[not(self.team)]:
				if ent.isNpc(tablBoss+tablRaidBoss+tablBossPlus):
					isBossAgaints = True
					break

			if not(isBossAgaints):
				self.char.splashIcon = "<:smallClemence:1236329023219437630>"
				self.icon = self.char.splashIcon
				youngClemEff1 = classes.effect("Jeunesse maudite","youngClemEff",PURCENTAGE,type=TYPE_MALUS,strength=-10,endurance=-15,magie=-10,turnInit=-1,silent=True,unclearable=True,stackable=True,emoji='<:isa:1158136337061400797>')
				youngClemEff2 = classes.effect("Jeunesse maudite","youngClemEff",PURCENTAGE,charisma=15,agility=15,dodge=10,turnInit=-1,silent=True,unclearable=True,stackable=True,emoji='<:isa:1158136337061400797>')
				youngClemEff3 = copy.deepcopy(aconstEff)
				youngClemEff3.power, youngClemEff3.turnInit, youngClemEff3.unclearable, youngClemEff3.silent, youngClemEff3.stat = 15, -1, True, True, PURCENTAGE
				groupAddEffect(caster=self, target=self, area=self, effect=[clemSmnEff,youngClemEff1,youngClemEff2,youngClemEff3])
			else: groupAddEffect(caster=self, target=self, area=self, effect=[clemSmnEff])
		elif self.isNpc("Alice"): groupAddEffect(caster=self, target=self, area=self, effect=[aliceSmnEff])

		if self.char.npcTeam == NPC_ANGEL:
			for indx, tmpSkill in enumerate(self.skills):
				if tmpSkill.__class__ == classes.skill:
					tmpSkill = copy.deepcopy(tmpSkill)
					if tmpSkill.use in range(MAGIE+1): tmpSkill.use = HARMONIE
					if tmpSkill.power > 0: tmpSkill.power = int(tmpSkill.power*ANGELPOWERMALUS)
					
					tmpSkill.effPowerPurcent = int(tmpSkill.effPowerPurcent*ANGELPOWERMALUS)
					tmpActStat = [[ACT_HEAL,self.baseStats[ACT_HEAL_FULL]],[ACT_BOOST,self.baseStats[ACT_BOOST_FULL]],[ACT_SHIELD,self.baseStats[ACT_SHIELD_FULL]],[ACT_DIRECT,self.baseStats[ACT_DIRECT_FULL]],[ACT_INDIRECT,self.baseStats[ACT_INDIRECT_FULL]]]
					tmpActStat.sort(key= lambda ballerine: ballerine[1])
					tmpSkill.useActionStats = tmpActStat[0][0]
					for indx2, tmpEff in enumerate(tmpSkill.effects):
						tmpEff = findEffect(tmpEff)
						if tmpEff != None and tmpEff.stat in range(MAGIE+1):
							tmpEff = copy.deepcopy(tmpEff)
							tmpEff.stat = HARMONIE
						tmpSkill.effects[indx2] = tmpEff

					if tmpSkill.effectAroundCaster not in [None,[]] and type(tmpSkill.effectAroundCaster[2]) == classes.effect and tmpSkill.effectAroundCaster[2].stat in range(MAGIE+1):
						tmpEff = copy.deepcopy(tmpSkill.effectAroundCaster[2])
						tmpEff.stat = HARMONIE
						tmpSkill.effectAroundCaster[2] = tmpEff
					
					if tmpSkill.effectOnSelf not in [None] and type(tmpSkill.effectOnSelf) == classes.effect and tmpSkill.effectOnSelf.stat in range(MAGIE+1):
						tmpEff = copy.deepcopy(tmpSkill.effectOnSelf)
						tmpEff.stat = HARMONIE
						tmpSkill.effectOnSelf = tmpEff

					self.skills[indx] = tmpSkill

		listEffGiven, listEffGiver, logs, toReturn = [],[], "", ""
		try:
			if self.char.elemAffinity:
				temp = add_effect(self,self,elemResistanceEffects[self.char.element],danger=danger); listEffGiven.append(elemResistanceEffects[self.char.element].emoji[self.char.species-1][self.team]); listEffGiver.append(elemEmojis[self.char.element]); logs += "{0} got the {1} effect\n".format(self.char.name,elemResistanceEffects[self.char.element].name)
		except: pass

		for indx, charSkill in enumerate(self.skills):
			if type(charSkill) == skill:
				if charSkill.jaugeEff != None:			   # If the entity have a passive
					temp = add_effect(self,self,charSkill.jaugeEff," ({0})".format(charSkill.name),danger=danger)
					if '🚫' not in temp:
						listEffGiven.append(charSkill.jaugeEff.emoji[self.char.species-1][self.team])
						if charSkill.emoji not in listEffGiver: listEffGiver.append(charSkill.emoji)
						logs += "{0} get the {1} charSkill.jaugeEff from {2}\n".format(self.char.name,charSkill.jaugeEff.name,charSkill.name)
				if charSkill.type == TYPE_PASSIVE:			   # If the entity have a passive
					for eff in charSkill.effects:
						eff = findEffect(eff)
						if eff != None:
							temp = add_effect(self,self,eff," ({0})".format(charSkill.name),danger=danger)
							if '🚫' not in temp:
								logs += "{0} got the {1} effect from {2}\n".format(self.char.name,eff.name,charSkill.name)
								if not(eff.silent):
									listEffGiven.append(eff.emoji[self.char.species-1][self.team])
									if charSkill.emoji not in listEffGiver: listEffGiver.append(charSkill.emoji)
				elif charSkill.id == divineAbne.id: self.maxHp = int(self.maxHp * (1-charSkill.power/100)); self.hp = self.maxHp
				elif charSkill.id == plumRem.id: self.char.weapon = plume2
				elif charSkill.id == lenaInkStrike.id: self.skills[indx] = lenaInkStrike_1
				elif charSkill.id == trappedField.id: self.skills[indx] = trappedFieldMockup

		for equip in [self.char.weapon]+self.char.stuff:	   # Look at the entity stuff to see if their is a passive effect
			if equip.effects != None:
				eff=findEffect(equip.effects)
				if eff != None and not(self.char.__class__ == classes.invoc and eff.type == TYPE_SUMMON):
					temp = add_effect(self,self,eff," ({0})".format(equip.name),danger=danger)
					if '🚫' not in temp:
						listEffGiven.append(eff.emoji[self.char.species-1][self.team])
						listEffGiver.append(equip.emoji)
						logs += "{0} get the {1} eff from {2}\n".format(self.char.name,eff.name,equip.name)
				else: print(equip.name,self.name,equip.effects)
		if self.char.element == ELEMENT_LIGHT:
			if self.char.standAlone:
				temp = copy.deepcopy(lightHealingPassif)
				temp.power = lightHealingPassif.power / 5
			else: temp = lightHealingPassif
			temp = add_effect(self,self,temp,danger=danger)
			listEffGiven.append(lightHealingPassif.emoji[self.char.species-1][self.team])
			listEffGiver.append(elemEmojis[self.char.element])
			logs += "{0} got the {1} effect\n".format(self.char.name,lightHealingPassif.name)
		if self.char.secElement == ELEMENT_SPACE:
			if self.char.standAlone:
				temp = copy.deepcopy(spaceShieldPassif)
				temp.power = lightHealingPassif.overhealth / 5
			else: temp = spaceShieldPassif
			temp = add_effect(self,self,temp,danger=danger)
			listEffGiven.append(spaceShieldPassif.emoji[self.char.species-1][self.team])
			listEffGiver.append(elemEmojis[self.char.element])
			logs += "{0} got the {1} effect\n".format(self.char.name,spaceShieldPassif.name)
		if self.char.npcTeam == NPC_UNDEAD:
			if self.team == 0:
				undeadPasEffv = copy.deepcopy(undeadPasEff)
				undeadPasEffv.power = 35
				add_effect(self,self,undeadPasEffv)
			else:
				add_effect(self,self,undeadPasEff)
				self.healResist += undeadPasEff.power
			self.char.rez = False

		communChipList = ["Absorbtion","Soins et armures réalisés augmentés","Dégâts universels augmentés","Convertion","Dégâts indirects reçus réduits","Dégâts reçus réduits","Cicatrisation","Châpeau de Roues","Ultime Sursaut"]
		chipEffList = ["Blocage augmenté","Esquive augmentée","Bouclier d'épines","Réflex","Précision Chirurgicale","Précision Critique","Présence","Dissimulation"]
		toSetChipName = ["Totem de Protection","Bénédiction","Plot Armor","Transgression","Overpower","Barrière","Radiance Toxique","Présence","Ambivalance","Goût du Sang","Dissimulation","Contre-Offensive","Retour de Bâton","Pas Piégés","Bout-Portant"]
		chipBaseEff = [absEff,healDoneBonus,dmgUp,convertEff,intraEff,defenseUp,cicatrisationEff,openingGambitEff,lastDitchEffortEff]
		chipBaseList, hadOne, chipNames, chipRarity = list(range(len(communChipList))), False, [], [[0,0],[1,0],[2,0],[3,0]]
		toSetValue = [1,1,1,0,1,3,0,0,0,0,[],0,0,3,[]]

		for indx, chipId in enumerate(self.char.equippedChips):
			tmpChip = getChip(chipId)
			if tmpChip != None:
				if tmpChip.name in communChipList:
					for cmpt, chipName in enumerate(communChipList):
						if tmpChip.name == chipName:
							tempEff = copy.deepcopy(chipBaseEff[cmpt])
							tempEff.power, tempEff.turnInit, tempEff.unclearable, tempEff.silent, tempEff.stat = self.char.chipInventory[chipId].power, -1, True, True, [FIXE,tempEff.stat][tempEff.stat in [FIXE,None,PURCENTAGE,MISSING_HP]]
							add_effect(caster=self, target=self, effect=tempEff)
				if tmpChip.name == "Précaution":
					tempEff = copy.deepcopy(precautionEff)
					tempEff.callOnTrigger.power = self.char.chipInventory[tmpChip.id].power
					add_effect(caster=self, target=self, effect=tempEff)
				if tmpChip.name in chipEffList:
					for cmpt, chipName in enumerate(chipEffList):
						if tmpChip.name == chipName:
							chipBaseList[cmpt] = self.char.chipInventory[chipId].power
							hadOne = True
							chipNames.append(tmpChip.name)
							chipRarity[tmpChip.rarity][1] += 1
				if tmpChip.name in toSetChipName:
					for cmpt, chipName in enumerate(toSetChipName):
						if tmpChip.name == chipName:
							self.chipAddInfo[indx] = toSetValue[cmpt]
							if chipName == "Bénédiction":
								dictHasBenedicton[self.team].append(self.id)
				if tmpChip.name == "Bouclier Sacrificiel":
					dictHasSacrificialShield[self.team].append(self)
				elif tmpChip.name == "Armure Initiale":
					initArmor = classes.effect(tmpChip.name,"initArmor",overhealth=self.maxHp*self.char.chipInventory[chipId].power/100,turnInit=5,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,replace=True,emoji=tmpChip.emoji)
					groupAddEffect(caster=self, target=self, area=self.tablEntTeam[self.team], effect=initArmor)
				elif tmpChip.name in ["Appel de la Lumière","Appel de la Nuit"]:
					for cmpt, tmpSkill in enumerate([lightCallSkill,nightCallSkill]):
						if tmpSkill.name == tmpChip.name:
							tmpSkill: skill = copy.deepcopy(tmpSkill)
							tmpSkill.effects[0].power, tmpSkill.description = round(self.char.chipInventory[chipId].power,2), tmpSkill.description.replace("%power",str(round(self.char.chipInventory[chipId].power,2)))
							self.skills, self.cooldowns = self.skills+[tmpSkill], self.cooldowns+[tmpSkill.initCooldown]
				elif tmpChip.name == "Retour de Bâton":
					tmpSkill: skill = copy.deepcopy(ilianaBonk)
					self.skills, self.cooldowns = self.skills+[tmpSkill], self.cooldowns+[tmpSkill.initCooldown]
				elif tmpChip.name == "Rentre-Dedans":
					for indx2, tmpSkill in enumerate(self.skills):
						if tmpSkill != None:
							if tmpSkill.become == None and (tmpSkill.tpCac or tmpSkill.tpBehind) and tmpSkill.power > 0:
								self.skills[indx2].power += round(self.char.chipInventory[chipId].power); self.skills[indx2].initPower += round(self.char.chipInventory[chipId].power)
							elif tmpSkill.become != None:
								for indx3, tmpBecomeSkill in enumerate(tmpSkill.become):
									if tmpBecomeSkill != None and (tmpBecomeSkill.tpCac or tmpBecomeSkill.tpBehind) and tmpBecomeSkill.power > 0:
										self.skills[indx2].become[indx3].power += round(self.char.chipInventory[chipId].power); self.skills[indx2].become[indx3].initPower += round(self.char.chipInventory[chipId].power)

		if hadOne:
			chipName = ""
			for tmpName in chipNames:
				chipName += tmpName + ", "
			chipRarity.sort(key= lambda ballerine: ballerine[1], reverse=True)
			tempEff = classes.effect(chipName[:-2],"rareChip",dodge=chipBaseList[1],block=chipBaseList[0],counterOnBlock=chipBaseList[2],counterOnDodge=chipBaseList[3], critHealUp=chipBaseList[4], critDmgUp=chipBaseList[5], aggro=(int(bool(chipBaseList[6]))*20)-(int(bool(chipBaseList[7]))*20),turnInit=-1,silent=True,unclearable=True,emoji=rarityEmojis[chipRarity[0][0]])
			add_effect(caster=self, target=self, effect=tempEff)

		self.refreshEffects()

		if listEffGiven != []:
			toReturn += "\n{0} ".format(self.icon)
			for equip in listEffGiver: toReturn += equip
			toReturn += " → "
			for equip in listEffGiven: toReturn += equip

		return toReturn, logs

	def getEntityInMelee(self,entity,lookingFor=ENEMIES): return entity.cell.getEntityOnArea(area=AREA_CIRCLE_2,team=self.team,wanted=lookingFor,directTarget=False,fromCell=self.cell)

	def triggerDepl(self):
		toReturn = "{0} __{1}__ {4}({2} __{3}__) :\n".format(self.icon,self.name,self.summoner.icon,self.summoner.name,["","se déclanche "][self.char.trap])
		self.effects, self.specialVars = [], []
		self.effects, self.specialVars = entDict[self.summoner.id].effects, entDict[self.summoner.id].specialVars
		self.recalculate()
		nonlocal logs

		if self.skills.type in [TYPE_BOOST,TYPE_ARMOR,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ,TYPE_INDIRECT_DAMAGE,TYPE_MALUS] and self.skills.effects != [None]:
			ballerine = groupAddEffect(caster=self, target=self, area=self.skills.area, effect=self.skills.effects, skillIcon=self.skills.emoji, actionStats=self.skills.useActionStats, effPurcent = self.skills.effPowerPurcent)
			toReturn += ballerine
			logs += ballerine

		elif self.skills.type == TYPE_HEAL:
			logs += "\n"
			power = self.skills.power

			if self.skills.effects != [None] and self.skills.effBeforePow:
				ballerine = groupAddEffect(caster=self, target=self, area=self.skills.area, effect=self.skills.effects, skillIcon=self.skills.emoji, actionStats=self.skills.useActionStats, effPurcent = self.skills.effPowerPurcent)
				toReturn = toReturn + ballerine
				logs += ballerine

			entHealedDict, entIcons, entHealVal = {}, "", []
			for ent in self.cell.getEntityOnArea(area=self.skills.area,team=self.team,fromCell=self.cell,wanted=ALLIES,directTarget=False):
				funnyTempVarName, healValue = self.heal(ent, self.skills.emoji, self.skills.use, self.skills.power, danger=danger, mono = self.skills.area == AREA_MONO, useActionStats = self.skills.useActionStats)
				logs += funnyTempVarName
				if healValue > 0:
					entHealedDict[ent] = healValue

			for dictKey, dictValue in entHealedDict.items():
				entIcons += dictKey.icon
				entHealVal.append(dictValue)

			lenDict = len(entHealVal)
			if lenDict > 0:
				if lenDict > 1:
					healedVal = int(sum(entHealVal)/lenDict)
				else:
					healedVal = dictValue
				toReturn += "{0} {1} → {2} +{3}{4} PV\n".format(self.icon, self.skills.emoji, entIcons, ["","≈"][lenDict>1],healedVal)

			if self.skills.effects != [None] and not(self.skills.effBeforePow):
				ballerine = groupAddEffect(caster=self, target=self, area=self.skills.area, effect=self.skills.effects, skillIcon=self.skills.emoji, actionStats=self.skills.useActionStats, effPurcent = self.skills.effPowerPurcent)
				toReturn += ballerine
				logs += ballerine

		else: # Damage
			power, elemPowBonus, cmpt = self.skills.power, 0, 0
			while cmpt < self.skills.repetition and self.skills.power > 0:
				funnyTempVarName, temp = self.attack(target=self, value=power, icon=self.skills.emoji, area=self.skills.area, accuracy=500, use=self.skills.use, onArmor=self.skills.onArmor, setAoEDamage=self.skills.setAoEDamage, erosion = self.skills.erosion, skillPercing = self.skills.percing, skillUsed = self.skills)
				toReturn += funnyTempVarName
				logs += "\n"+funnyTempVarName
				cmpt += 1
				if cmpt < self.skills.repetition:
					toReturn += "\n"

			if None not in self.skills.effects and not(self.skills.effBeforePow):
				toReturn += "\n"
				for a in self.skills.effects:
					effect = findEffect(a)
					toReturn += add_effect(self,self,effect,effPowerPurcent=self.skills.effPowerPurcent)
					logs += "\n{0} gave the {1} effect at {2} for {3} turn(s)".format(self.char.name,effect.name,self.char.name,effect.turnInit)

		if self.skills.effectAroundCaster != None:
			toReturn += "\n"
			if self.skills.effectAroundCaster[0] == TYPE_HEAL:
				entHealedDict, entIcons, entHealVal = {}, "", []
				for ent in self.cell.getEntityOnArea(area=self.skills.effectAroundCaster[1],team=self.team,fromCell=self.cell,wanted=ALLIES,directTarget=False):
					funnyTempVarName, healValue = self.heal(ent, self.skills.emoji, self.skills.use, self.skills.effectAroundCaster[2], danger=danger, mono = self.skills.effectAroundCaster[1] == AREA_MONO, useActionStats = self.skills.useActionStats)
					logs += funnyTempVarName
					if healValue > 0:
						entHealedDict[ent] = healValue

				for dictKey, dictValue in entHealedDict.items():
					entIcons += dictKey.icon
					entHealVal.append(dictValue)

				lenDict = len(entHealVal)
				if lenDict > 0:
					if lenDict > 1:
						healedVal = int(sum(entHealVal)/lenDict)
					else:
						healedVal = dictValue
					toReturn += "{0} {1} → {2} +{3}{4} PV\n".format(self.icon, self.skills.emoji, entIcons, ["","≈"][lenDict>1],healedVal)
			elif self.skills.effectAroundCaster[0] == TYPE_DAMAGE:
				funnyTempVarName, temp = self.attack(target=self,value=self.skills.effectAroundCaster[2],icon=self.skills.emoji,area=self.skills.effectAroundCaster[1],accuracy=self.skills.accuracy,use=self.skills.use,onArmor=self.skills.onArmor,useActionStats=actionStats,setAoEDamage=self.skills.setAoEDamage,lifeSteal = self.skills.lifeSteal)
				toReturn += funnyTempVarName
				logs += "\n"+funnyTempVarName
			elif type(self.skills.effectAroundCaster[2]) == classes.effect or findEffect(self.skills.effectAroundCaster[2]) != None :
				ballerine = groupAddEffect(self, self , self.skills.effectAroundCaster[1], self.skills.effectAroundCaster[2], self.skills.emoji, effPurcent=self.skills.effPowerPurcent)
				toReturn += ballerine
				logs += ballerine

		return toReturn+"\n"

	def getOnArmorDmgValue(self, skillDmgOnArmor:int=1):
		toReturn = skillDmgOnArmor*self.dmgOnArmor
		if self.char.element == ELEMENT_DARKNESS: toReturn += DARKDMGBUFF/100

		tmpChip = getChip("Démolition")
		if tmpChip != None and tmpChip.id in self.char.equippedChips: toReturn += self.char.chipInventory[tmpChip.id].power/100
		return round(toReturn,2)

	def weaponEffect(self, weapEffId: Union[str, classes.effect, classes.weapon, List[Union[str, classes.effect, classes.weapon]]]):
		if type(weapEffId) != list:
			weapEffId = list(weapEffId)
		
		for obj in weapEffId:
			if type(obj) == classes.effect: obj = obj.id
			elif type(obj) == classes.weapon:
				if obj.effects != None: obj = findEffect(obj.effects).id
				else: raise AttributeError("The weapon given has no associated effect")
			if self.char.weapon.effects != None: return findEffect(self.char.weapon.effects).id == weapEffId
		return False

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
		basePower = self.effects.power

		if effReducPurcent != None: self.effects.power = int(self.effects.power*effReducPurcent/100)
		else: effReducPurcent = 100

		self.caster:entity = caster
		self.on:entity = on
		if self.effects.type == TYPE_MALUS and self.on.char.standAlone:
			effReducPurcent = effReducPurcent//2
		if self.effects.id in [charming.id, charming2.id, charmingHalf.id, kitsuneExCharmEff.id] and self.caster.isNpc("Lia"): turnLeft += 1
		self.turnLeft = turnLeft
		if self.turnLeft == None: print("Error with {0} : None left turn".format(self.effects.name)); self.turnLeft = self.effects.turnInit
		self.trigger = trigger
		self.type = type
		self.value = value

		if effect.jaugeValue != None and effect.unclearable:
			self.value = 0
			for conds in effect.jaugeValue.conds:
				if conds.type == INC_START_FIGHT: self.value = conds.value

		self.id = id
		self.icon = self.effects.icon = icon
		self.remove = False
		self.stun:bool = effect.stun
		self.name = effect.name
		self.replicaTarget: Union[None,entity] = None

		if self.effects.type == TYPE_INDIRECT_DAMAGE and self.caster.char.secElement == ELEMENT_LIGHT:
			self.effects.lifeSteal += TIMELIFESTEAL

		tablTemp = []
		for cmpt in range(CRITICAL+1):
			tablTemp += [0]

		if self.effects.stat not in [None,FIXE,PURCENTAGE,MISSING_HP]:
			if self.effects.stat is not HARMONIE: temp = self.caster.allStats()[self.effects.stat]
			else:
				temp = -111
				for a in self.caster.allStats():
					temp = max(temp,a)

			if caster.aspiration in [BERSERK,POIDS_PLUME,TETE_BRULEE,ENCHANTEUR,VIGILANT,PROTECTEUR,MASCOTTE,ASPI_NEUTRAL]: temp += int(caster.endurance * MELEE_END_CONVERT/100)

			valueBoost, valueResis = (min(self.caster.char.level,200)/50*0.3) + (caster.valueBoost(self.on) * (temp+100-self.caster.negativeBoost)/100), caster.valueBoost(self.on) * (temp+100-self.caster.negativeShield)/100

			secElemMul = 1
			if caster.char.element in [ELEMENT_SPACE,ELEMENT_UNIVERSALIS]: secElemMul += SPACEBONUSBUFF/100

			valueBoost = valueBoost*secElemMul

			tmpChip = getChip("Spotlight")
			if tmpChip.id in caster.char.equippedChips: valueBoost = valueBoost* 1+(caster.char.chipInventory[tmpChip.id].power/100)

		else: valueBoost, valueResis = 1, 1

		if self.effects.stat not in [PURCENTAGE]:
			tablTemp[0] += self.effects.strength * valueBoost * effReducPurcent * 0.01
			tablTemp[1] += self.effects.endurance * valueBoost * effReducPurcent * 0.01
			tablTemp[2] += self.effects.charisma * valueBoost * effReducPurcent * 0.01
			tablTemp[3] += self.effects.agility * valueBoost * effReducPurcent * 0.01
			tablTemp[4] += self.effects.precision * valueBoost * effReducPurcent * 0.01
			tablTemp[5] += self.effects.intelligence * valueBoost * effReducPurcent * 0.01
			tablTemp[6] += self.effects.magie * valueBoost * effReducPurcent * 0.01
			tablTemp[7] += self.effects.resistance * valueBoost * effReducPurcent * 0.01
			tablTemp[8] += self.effects.percing * valueBoost * effReducPurcent * 0.01
			tablTemp[9] += self.effects.critical * valueBoost * effReducPurcent * 0.01

			if self.caster.char.secElement == ELEMENT_DARKNESS:
				for cmpt in range(MAGIE+1):
					tablTemp[cmpt] += round(self.on.baseStats[cmpt] * (DARKDEBUFF/100))
		else:
			malusMul = [1,-1][self.type == TYPE_MALUS]
			tablTemp[0] += abs(self.effects.strength / 100 * self.on.baseStats[0])*malusMul
			tablTemp[1] += abs(self.effects.endurance / 100 * self.on.baseStats[1])*malusMul
			tablTemp[2] += abs(self.effects.charisma / 100 * self.on.baseStats[2])*malusMul
			tablTemp[3] += abs(self.effects.agility / 100 * self.on.baseStats[3])*malusMul
			tablTemp[4] += abs(self.effects.precision / 100 * self.on.baseStats[4])*malusMul
			tablTemp[5] += abs(self.effects.intelligence / 100 * self.on.baseStats[5])*malusMul
			tablTemp[6] += abs(self.effects.magie / 100 * self.on.baseStats[6])*malusMul
			tablTemp[7] += abs(self.effects.resistance / 100 * self.on.baseStats[7])*malusMul
			tablTemp[8] += abs(self.effects.percing / 100 * self.on.baseStats[8])*malusMul
			tablTemp[9] += abs(self.effects.critical / 100 * self.on.baseStats[9])*malusMul

		for cmpt in range(CRITICAL+1): tablTemp[cmpt] = [min(tablTemp[cmpt],0),max(tablTemp[cmpt],0)][self.effects.type == TYPE_BOOST]

		self.inkResistance = [max(effect.inkResistance * valueResis,effect.inkResistance*3),min(effect.inkResistance * valueResis,effect.inkResistance*3)][effect.inkResistance>0]

		self.tablAllStats = tablTemp
		self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie,self.resistance,self.percing,self.critical = tuple(tablTemp)

		if self.effects.id in [vulne.id,dmgDown.id,dmgUp.id,defenseUp.id] and self.effects.stat not in [None,FIXE]:
			if valueBoost > 1: valueBoost = valueBoost / 2
			if self.on.char.standAlone and self.on.id != self.caster.id: self.effects.power = self.effects.power/2
			self.effects.power = self.effects.power * valueBoost
		elif self.effects.id in [vampirismeEff.id,convertEff.id,aoeConvertEff.id,aoeVampirismeEff.id] and self.effects.stat not in [None,FIXE]:
			power = self.effects.power
			if self.effects.stat == HARMONIE: maxStats = max(caster.allStats())
			else: maxStats = caster.allStats()[self.effects.stat]
			self.effects.power = power * (100+maxStats-[caster.negativeHeal,caster.negativeShield][self.effects.id==convertEff.id])/100 * (1 + caster.valueBoost(self.on,heal=self.effects.id!=convertEff.id))/2

		nonlocal logs
		try:
			if effect.stat not in [None,FIXE] and (not(tablTemp[0] == tablTemp[1] == tablTemp[2] == tablTemp[3] == tablTemp[4] == tablTemp[5] == tablTemp[6] == tablTemp[7] == tablTemp[8] == tablTemp[9] == 0) or effect.power != 0):
				logs += "\n[Effect : {0} ; Caster : {1} ; Target : {2} ;\n".format(effect.name, caster.name, self.on.name)
				if effect.power != 0 and self.effects.id not in [vulne.id,dmgDown.id,dmgUp.id,defenseUp.id]: logs += "   Puissance : {0} [BaseValue : {1} * {2}] ;".format(self.effects.power,basePower,effReducPurcent/100)
				elif effect.power != 0 and self.effects.id in [vulne.id,dmgDown.id,dmgUp.id,defenseUp.id]: logs += "   Puissance : {0} [BaseValue : {1} * {2}] ;".format(self.effects.power,basePower,valueBoost*effReducPurcent/100)

				if not(tablTemp[0] == tablTemp[1] == tablTemp[2] == tablTemp[3] == tablTemp[4] == tablTemp[5] == tablTemp[6] == tablTemp[7] == tablTemp[8] == tablTemp[9] == 0):
					tablMul = ["{0} [levelBonus]","{0} [AspiBoostBonus]","{0} [effPowerPurcent]"]
					if effect.stat != PURCENTAGE:
						try:
							temp
						except UnboundLocalError:
							temp = 0
						tempStats, tablVal, toAdd = temp+100-self.caster.negativeBoost, [min(self.caster.char.level,200)/50*0.3,caster.valueBoost(self.on),effReducPurcent/100], ""
						for cmpt in range(len(tablMul)):
							if tablVal[cmpt] != 1:
								toAdd += " * {0}".format(tablMul[cmpt].format(round(tablVal[cmpt],2)))
					else:
						tempStats, toAdd = 100, ""
					logs += "   EffBoostPower : x{0} ({1} [stats+100] /100".format(valueBoost*effReducPurcent/100,tempStats) + toAdd + ") ;"
					tempLogs, baseStats = "", effect.allStats() + [effect.resistance, effect.percing, effect.critical]
			
					for cmpt in range(CRITICAL+1):
						if tablTemp[cmpt] != 0:
							logs += " {0} : {1} [BaseValue : {2}] ;".format(allStatsNames[cmpt],round(tablTemp[cmpt],2),baseStats[cmpt])
				logs += "]\n"
		except:
			print_exc()
			pass

		if self.effects.id == sixtineCardEff.id:
			self.replicaTarget = list(range(36))
			random.shuffle(self.replicaTarget)
	
	def decate(self,turn=0,value=0) -> str:
		"""Réduit le turnLeft ou value de l'effet"""
		self.turnLeft -= turn
		self.value -= value
		temp = ""

		if ((self.turnLeft <= 0 and self.effects.turnInit > 0) or self.value <= 0) and not(self.effects.unclearable):
			self.remove = True
			if self.trigger in [TRIGGER_ON_REMOVE,TRIGGER_HP_UNDER_70,TRIGGER_HP_UNDER_50,TRIGGER_HP_UNDER_25,TRIGGER_ON_MOVE]:
				try:
					temp += self.triggerRemove()
				except: print(self.effects.name, self.caster.name); print_exc()
			elif not(self.effects.silent) and self.on.hp > 0 and self.effects.id not in (astralShield.id,timeShield.id) and self.effects.trigger != TRIGGER_INSTANT and not(self.effects.silentRemove):
				temp += f"{self.on.icon} → ~~{self.effects.name}~~\n"
			elif self.effects.id == elemShieldEff.id and self.value <= 0:
				temp += groupAddEffect(self.caster, self.on, self.effects.callOnTrigger,self.effects.area,self.icon,ACT_SHIELD)
		return temp

	def triggerDamage(self, value=0, icon="", declancher = 0, onArmor = 1, armorSteal = 0, dealsDamageOn=False) -> list:
		"""Déclanche l'effet"""
		value = round(value)
		temp2 = [value,""]

		if self.effects.overhealth > 0 and value > 0 and self.value > 0:
			shieldPAr, returnDmg, toReturnTxt = self.value, value, ""
			if not(self.effects.absolutShield):
				if declancher.char.secElement == ELEMENT_EARTH: armorSteal += EARTHBOOST/100
				onArmor = declancher.getOnArmorDmgValue(onArmor)

			else: onArmor = 1
			dmgRecived = round(value * onArmor)

			if dmgRecived >= shieldPAr:
				declancher.stats.damageOnShield += shieldPAr
				self.caster.stats.armoredDamage += shieldPAr
				self.on.stats.damageProtected += shieldPAr
				self.on.stats.damageResisted -= shieldPAr
				addedReduc = [self.on.char.level//[2,4][self.caster.char.__class__ == classes.octarien],0][self.effects.lightShield]
				tmpChip = getChip("Armure Solide")
				if tmpChip.id in self.caster.char.equippedChips:
					addedReduc += int(self.caster.char.level * self.caster.char.chipInventory[tmpChip.id].power/100)
				if preOSEff.id in self.caster.specialVars:
					addedReduc += self.caster.char.level * (preOSEff.power/100)
				elif idoOSEff.id in self.caster.specialVars or proOSEff.id in self.caster.specialVars:
					addedReduc += self.caster.char.level * (idoOSEff.power/100)

				if self.on.char.aspiration == PROTECTEUR:
					addedReduc = int(addedReduc*1.5)

				returnDmg, armorStolen = int((shieldPAr+addedReduc)/onArmor), 0
				if armorSteal > 0:
					armorStolen = int(shieldPAr*armorSteal)
				toReturnTxt = ["<:abB:934600555916050452> ","<:abR:934600570633867365> "][self.on.team] + "-" + str(shieldPAr)+" PAr "
				self.decate(value=shieldPAr)
				return (returnDmg,toReturnTxt,armorStolen)
			else:
				declancher.stats.damageOnShield += dmgRecived
				self.caster.stats.armoredDamage += dmgRecived
				self.on.stats.damageProtected += dmgRecived
				self.on.stats.damageResisted -= dmgRecived
				returnDmg = value
				toReturnTxt, armorStolen = self.icon + "-" + str(dmgRecived)+" PAr ", 0
				self.decate(value=dmgRecived)
				if armorSteal > 0:
					armorStolen = int(shieldPAr*armorSteal)
				return (returnDmg,toReturnTxt,armorStolen)
			if dmgRecived > 0:
				tmpChip = getChip("Lithophage")
				if tmpChip != None and tmpChip.id in declancher.char.equippedChips:
					tmpEff = copy.deepcopy(lythophageEff)
					tmpEff.power = declancher.char.chipInventory[tmpChip.id].power/100 * dmgRecived
					addingEffect(caster=declancher, target=declancher, area=AREA_MONO, effect=tmpEff)

		elif self.effects.redirection > 0 and value > 0:
			if self.caster.hp > 0:
				valueT = value
				redirect = int(valueT * self.effects.redirection/100)

				tmpChip = getChip("Altruisme")
				if tmpChip.id in self.caster.char.equippedChips:
					redirect = int(redirect * (1-(self.caster.char.chipInventory[tmpChip.id].power/100)))
				declancher.indirectAttack(target=self.caster,value=redirect,icon=icon,ignoreImmunity=False,name=self.effects.name,canCrit=False, redirected=True)
				return (redirect,"{0} -{1} PV".format(self.caster.icon,redirect))
			else: return (0,"")

		elif (self.type == TYPE_INDIRECT_DAMAGE or self.effects.id in [lightLameEff.id,astralLameEff.id,timeLameEff.id,mattSkill4Eff.id]) and self.value>0:
			target = [self.on,declancher][self.effects.onDeclancher]
			if self.caster.id == self.on.id and self.caster.id == declancher.id:
				target = ennemi
			temp2[1] = self.triggeredIndDamage(target)

		elif self.type == TYPE_UNIQUE:
			if self.effects.id == enchant.id :
				self.effects.magie += 5

		elif self.type == TYPE_INDIRECT_HEAL and self.on.hp > 0:
			temp2[1] = self.triggeredIndHeal()

		if self.effects.callOnTrigger != None:
			temp2[1] = ""
			if type(self.on.char) not in [invoc, depl]:
				eff = findEffect(self.effects.callOnTrigger)
				target = [self.on,declancher][declancher!=0 and eff.onDeclancher]
				temp2[1] += groupAddEffect(caster=self.caster, target=target, area=AREA_MONO, effect=eff, skillIcon=self.icon)
				self.decate(value=1)

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
			toReturn = self.triggeredIndDamage(self.on)

		elif self.type == TYPE_UNIQUE:
			if self.effects == hunter:
				add_effect(self.on,self.on,hunterBuff)
				self.on.refreshEffects()
				tempi, useless = self.on.attack(target=killer,value = self.on.char.weapon.power, icon = self.on.char.weapon.emoji, onArmor=self.on.char.weapon.onArmor)
				toReturn += tempi

		elif self.type == TYPE_DEPL and type(self.effects.callOnTrigger) == classes.depl:
			self.caster.smnDepl(self.effects.callOnTrigger,self.on.cell)
			nonlocal logs
			logs += "\n{0} is placing a {1} at {2}:{3}".format(self.caster.name,self.effects.callOnTrigger.name,self.on.cell.x,self.on.cell.y)
			toReturn += "{0} a déployé {1} __{2}__ sur la cellule {3}:{4}".format(self.caster.name,self.effects.callOnTrigger.icon[self.caster.team],self.effects.callOnTrigger.name,self.on.cell.x,self.on.cell.y)
			if self.on.cell.on != None:
				toReturn += " ({0})\n".format(self.on.cell.on.icon)
			else:
				toReturn += "\n"

		if self.effects.callOnTrigger != None and type(self.effects.callOnTrigger) in [str,classes.effect]:
			toReturn += add_effect(self.on,self.on,findEffect(self.effects.callOnTrigger))
			
		self.decate(value=1)

		return toReturn

	def triggerStartOfTurn(self,danger,decate=True) -> str:
		"""Déclanche l'effet"""
		funnyTempVarName=""
		if self.type == TYPE_INDIRECT_HEAL and self.on.hp > 0:			  # Heal Indirect
			return self.triggeredIndHeal()
		elif self.type in [TYPE_INDIRECT_DAMAGE, TYPE_DAMAGE] and self.value > 0 and ((self.effects.area==AREA_MONO and self.on.hp > 0) or self.effects.area != AREA_MONO) and self.on != None:			# Damage indirect
			funnyTempVarName = self.triggeredIndDamage(self.on,decate)

			if self.effects.id in [infection.id,epidemicEff.id,intoxEff.id]:							  # If it's the infection poisonnus effect
				if self.effects.power > 10:
					funnyTempVarName += groupAddEffect(caster=self.caster, target=self.on, area=AREA_DONUT_1, effect=self.effects, skillIcon=self.icon, effPurcent=75)
		elif self.type in [TYPE_BOOST,TYPE_MALUS] and self.on.hp > 0:					# Indirect Armor / Buff
			if self.effects.id != sixtineCardEff.id:
				if self.effects.id == toxiceptionEff.id:
					self.effects.callOnTrigger, nbEff = copy.deepcopy(self.effects.callOnTrigger), 0
					for eff in self.on.effects:
						if eff.caster.id == self.caster.id and eff.effects.type == TYPE_INDIRECT_DAMAGE:
							nbEff += 1

					self.effects.callOnTrigger.power = min(30,nbEff*self.caster.char.chipInventory[getChip("Toxiception").id].power)
					self.effects.callOnTrigger.name += " ({0}%)".format(self.effects.callOnTrigger.power)
				elif self.effects.id == clemTmpWeapEff.id:
					lowestHpAllie = self.on.cell.getEntityOnArea(AREA_LOWEST_HP_ALLIE,self.on.team,ALLIES,directTarget=False,ignoreInvoc=True,fromCell=self.on.cell)
					if len(lowestHpAllie) > 0:
						lowestHpAllie = lowestHpAllie[0]
						if lowestHpAllie != self.on and lowestHpAllie.hp < lowestHpAllie.maxHp:
							tmp, healPowa = self.on.heal(target=lowestHpAllie, icon=self.icon, statUse=None, power=self.on.hp*self.effects.power/100, effName = self.name, mono = True,direct=False)
							if healPowa > 0:
								self.on.hp -= healPowa
								return "{0} {1} → {0} -{2} PV {3} +{2} PV\n".format(self.on.icon,self.icon,healPowa,lowestHpAllie.icon)
							else: return ""
					else: return ""

				self.decate(value=1)
				return groupAddEffect(caster=self.caster, target=self.on, area=self.effects.area, effect=findEffect(self.effects.callOnTrigger),skillIcon=self.icon)
			else:
				drawedCard = self.replicaTarget.pop(0)
				drawedColor, drawedValue = drawedCard//9, drawedCard%9
				cardName, cardEmoji = "{0} {1}".format(cardValueNames[drawedValue],cardColorNames[drawedColor]), cardEmojiTabl[drawedCard]

				if drawedColor == 0:
					if drawedValue < 5 or drawedValue == 8:
						cardEff = classes.effect(cardName,cardName,MAGIE,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,power=([drawedValue+6,15][drawedValue==8])*10,emoji=cardEmoji,area=AREA_RANDOMENNEMI_1)
					else:
						cardEff = classes.effect(cardName,cardName,MAGIE,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,power={5:100,6:100,7:100}[drawedValue],emoji=cardEmoji,area={5:AREA_RANDOMENNEMI_3,6:AREA_RANDOMENNEMI_5,7:AREA_ALL_ENEMIES}[drawedValue])

				elif drawedColor == 1:
					if drawedValue < 5 or drawedValue == 8:
						triggerCardEff = classes.effect(cardName+" (effet)",cardName,INTELLIGENCE,type=TYPE_MALUS,strength=([drawedValue+6,15][drawedValue==8])*-1,magie=([drawedValue+6,15][drawedValue==8])*-1,charisma=([drawedValue+6,15][drawedValue==8]//2)*-1,intelligence=([drawedValue+6,15][drawedValue==8]//2)*-1,emoji=':clubs:',turnInit=3)
						cardEff = classes.effect(cardName,cardName,trigger=TRIGGER_END_OF_TURN,emoji=cardEmoji,area=[AREA_RANDOMENNEMI_1,AREA_RANDOMENNEMI_5][drawedValue == 8],callOnTrigger=triggerCardEff)

					else:
						valetEff, queenEff, kingEff = copy.deepcopy(vulne), copy.deepcopy(dmgDown), copy.deepcopy(deepWound)
						valetEff.power, queenEff.power, kingEff.power, kingEff.stat = 15, 15, 50, MAGIE
						valetEff.turnInit = queenEff.turnInit = kingEff.turnInit = 3
						triggerCardEff = {5:valetEff,6:queenEff,7:kingEff}[drawedValue]
						cardEff = classes.effect(cardName,cardName,trigger=TRIGGER_END_OF_TURN,emoji=cardEmoji,area=AREA_ALL_ENEMIES,callOnTrigger=triggerCardEff)

				elif drawedColor == 2:
					if drawedValue < 5 or drawedValue == 8:
						cardEff = classes.effect(cardName,cardName,MAGIE,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_HEAL,power=([drawedValue+6,10][drawedValue == 8])*10,emoji=cardEmoji,area=AREA_LOWEST_HP_ALLIE)
					elif drawedValue == 5:
						cardEff = classes.effect(cardName,cardName,MAGIE,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_HEAL,power=100,emoji=cardEmoji,area=AREA_CIRCLE_2)
					elif drawedValue == 6:
						triggerCardEff = classes.effect("Armure royale","royalarmor",PURCENTAGE,overhealth=50,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
						cardEff = classes.effect(cardName,cardName,trigger=TRIGGER_END_OF_TURN,type=TYPE_BOOST,emoji=cardEmoji,area=AREA_ALL_ALLIES,callOnTrigger=triggerCardEff)
					else:
						triggerCardEff = classes.effect("Régénération royale","royalregen",PURCENTAGE,overhealth=12.5,turnInit=3,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN)
						cardEff = classes.effect(cardName,cardName,trigger=TRIGGER_END_OF_TURN,type=TYPE_BOOST,emoji=cardEmoji,area=AREA_ALL_ALLIES,callOnTrigger=triggerCardEff)

				elif drawedColor == 3:
					if drawedValue < 5 or drawedValue == 8:
						triggerCardEff = classes.effect(cardName+" (effet)",cardName,INTELLIGENCE,strength=[drawedValue+6,15][drawedValue == 8],magie=[drawedValue+6,15][drawedValue == 8],charisma=[drawedValue+6,15][drawedValue == 8]//2,intelligence=[drawedValue+6,15][drawedValue == 8]//2,emoji=':diamonds:',turnInit=3)
						cardEff = classes.effect(cardName,cardName,trigger=TRIGGER_END_OF_TURN,emoji=cardEmoji,area=[AREA_RANDOMALLIE_1,AREA_ALL_ALLIES][drawedValue == 8],callOnTrigger=triggerCardEff)

					else:
						valetEff, queenEff, kingEff = copy.deepcopy(defenseUp), copy.deepcopy(constEff), copy.deepcopy(dmgUp)
						valetEff.power, queenEff.power, queenEff.stat, kingEff.power = 15, 10, PURCENTAGE, 15
						valetEff.turnInit = queenEff.turnInit = kingEff.turnInit = 3
						triggerCardEff = {5:valetEff,6:queenEff,7:kingEff}[drawedValue]
						cardEff = classes.effect(cardName,cardName,trigger=TRIGGER_END_OF_TURN,emoji=cardEmoji,area=AREA_ALL_ALLIES,callOnTrigger=triggerCardEff)
				
				if len(self.replicaTarget) == 0:
					self.replicaTarget = list(range(36))
					random.shuffle(self.replicaTarget)
				cardEff.turnInit, cardEff.lvl = 2, 1
				return groupAddEffect(caster=self.caster, target=self.on, area=AREA_MONO, effect=cardEff,skillIcon=self.icon)
		elif self.type == TYPE_SUMMON and type(self.effects.callOnTrigger) == classes.invoc:
			nonlocal time, tablEntTeam, tablAliveInvoc, logs
			toSummon, cmpt = findSummon(self.effects.callOnTrigger), 0
			while cmpt < self.effects.lvl:
				cellToSummon = self.on.cell.getCellForSummon(self.effects.area,self.caster.team,toSummon,self.caster)
				if cellToSummon != None:
					tablEntTeam, tablAliveInvoc, time, tempBlabla = self.caster.summon(toSummon,time,cellToSummon,tablEntTeam,tablAliveInvoc,ignoreLimite=True)
					funnyTempVarName += tempBlabla
					logs += "\n"+tempBlabla
				cmpt += 1
		return funnyTempVarName

	def triggerEndOfTurn(self,danger,decate=True) -> str:
		"""Trigger the effect"""
		temp = ""
		if self.type in [TYPE_INDIRECT_DAMAGE,TYPE_DAMAGE] and self.value > 0:							   # The only indirect damage effect for now is a insta death
			temp = self.triggeredIndDamage(self.on,decate)
		elif self.type == TYPE_UNIQUE:									  # Poids Plume effect bonus reduce
			if self.effects == poidPlumeEff:
				self.value = self.value//2

		if self.type == TYPE_INDIRECT_HEAL and self.on.hp > 0:			# End of turn healing (aka Light Aura 1)
			if self.effects.id == radianceEff.id:
				try:
					if teamJaugeDict[self.caster.team][self.caster].effects.id == healerGlare.jaugeEff.id and teamJaugeDict[self.caster.team][self.caster].value > 20:
						teamJaugeDict[self.caster.team][self.caster].value -= 20
						return self.triggeredIndHeal()
				except KeyError:
					pass
			else:
				temp = self.triggeredIndHeal()
				if self.effects.stat in [None,FIXE]:
					temp += self.decate(value=self.value+1)
		elif self.effects.callOnTrigger != None :
			temp += groupAddEffect(self.caster, self.on, self.effects.area, self.effects.callOnTrigger, self.icon, actionStats=[ACT_BOOST,ACT_SHIELD][self.effects.callOnTrigger.type == TYPE_ARMOR])
			self.decate(value=1)
		return temp

	def triggerRemove(self) -> str:
		"""Trigger the effect when it's removed\n
		For now, only unique effect activly use it, but some boost effect use it to"""
		message = ""

		if self.type == TYPE_UNIQUE:
			if self.effects.id == lostSoul.id:								   # Remove the body effect
				if self.on.status == STATUS_DEAD:
					self.on.status = STATUS_TRUE_DEATH
					message="{0} est hors combat !\n".format(self.on.char.name)
			elif self.effects.id == naciaGiantEff.id:
				message += "\n{0} : *\"Vous commencez sérieusement à me pousser à bout là.\"*\nNacialisla prend une forme giantesque !\n".format(self.on.icon)
				hptoSee = max(self.on.maxHp,self.on.trueMaxHp)
				actPurcent = max(0.6,min(self.on.hp / hptoSee,1))
				self.on.maxHp = int(hptoSee + hptoSee*(GIANTESSHPBONUS)/100)
				self.on.hp = int(self.on.maxHp*actPurcent)
				giantessEff = classes.effect("Puissance originelle","giantessNacialisla",
					strength=int(self.on.baseStats[STRENGTH]*GIANTESSSTATBONUS/100),
					endurance=int(self.on.baseStats[ENDURANCE]*GIANTESSSTATBONUS/100),
					precision=int(self.on.baseStats[PRECISION]*GIANTESSSTATBONUS/100),
					magie=int(self.on.baseStats[MAGIE]*GIANTESSSTATBONUS/100),
					resistance=20,
					dodge=-200,turnInit=-1,unclearable=True,emoji='<:naciaGiantEff:1052323849288568975>'
				)
				actStrength = self.on.strength
				self.on.clemBloodJauge = giantessEff

				self.on.char.splashIcon = '<:giantessNacia:1208132139342626846>'
				for key in naciaSplashIconPulls:
					if self.on.icon == naciaSplashIconPulls[key][0]:
						self.on.char.splashIcon = naciaSplashIconPulls[key][1]

				self.on.icon = self.on.char.splashIcon
				self.on.char.trait = self.on.char.trait + [TRAIT_GIANTESS]
				add_effect(caster=self.on, target=self.on, effect=giantessEff, danger=100)
				message += groupAddEffect(caster=self.on, target=self.on, area=AREA_MONO, effect=naciaGiantShockWave)
				nonlocal naciaFlag
				naciaFlag = True

			elif self.effects.id == justiceEnigmaEff.id:
				self.effects.power, self.effects.area, self.effects.stat = self.value, AREA_DONUT_2, None
				message += self.triggeredIndDamage(self.on,decate=False)
				self.effects.area = AREA_MONO
				message += self.triggeredIndHeal(decate=False)
		elif self.effects.id == deathMark.id and (self.value > 0 and self.turnLeft <= 0):
			message += self.triggeredIndDamage(target=self.on,decate=True)
		elif self.type in [TYPE_INDIRECT_DAMAGE,TYPE_DAMAGE]:
			message = self.triggeredIndDamage(self.on,decate=False)
		elif self.type == TYPE_INDIRECT_HEAL and self.on.hp > 0:
			if self.effects.id == zelianR.id:
				if self.value > 0:
					message += self.caster.heal(self.on, self.icon, FIXE, self.value, self.name,direct=False)[0]
			else:
				return self.triggeredIndHeal(decate=False)
		if self.effects.callOnTrigger != None and self.effects.id not in [plumRemEff.id]:							   # If the effect give another effect when removed, give that another effect
			message += groupAddEffect(self.caster, self.on, self.effects.area, self.effects.callOnTrigger, skillIcon=self.icon)
			if findEffect(self.effects.callOnTrigger).id == temNativTriggered.id:
				self.on.icon, self.on.char.icon = '<:colegue:895440308257558529>','<:colegue:895440308257558529>'

		return message

	def triggerInstant(self,danger) -> str:
		"""Déclanche l'effet"""
		funnyTempVarName, decate = "", True
		if self.effects.id == galvaniseEff.id: self.on.leftTurnAlive += self.effects.power
		elif self.effects.id == fairyRayEff.id:
			hasEstial, sumPower = False, 0
			for eff in self.on.effects:
				if eff.effects.id == estial.id:
					hasEstial = True
					sumPower = eff.effects.power * eff.value
					eff.decate(turn=99)
			if hasEstial:
				eff1 = classes.effect("Explosion Féérique","fairyBoom",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,emoji=estial.emoji[0][0],power=int(sumPower*(FAIRYRAYMONODMG/100)))
				eff2 = classes.effect("Explosion Féérique","fairyBoom2",MAGIE,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,emoji=estial.emoji[0][0],power=int(sumPower*(FAIRYRAYAOEDMG/100)),area=fairyRayEff.area)
				return groupAddEffect(caster=self.caster, target=self.on, area=AREA_MONO, effect=[eff1,eff2], skillIcon=self.effects.emoji[0][0], actionStats=ACT_INDIRECT)
			else: return groupAddEffect(caster=self.caster, target=self.on, area=AREA_MONO, effect=[estial], skillIcon=self.effects.emoji[0][0], actionStats=ACT_INDIRECT, effPurcent = FAIRYRAYPOWER)
		elif self.effects.id == playSixtineCard.id:
			for eff in self.on.effects:
				if eff.effects.id == sixtineCardEff.id:
					funnyTempVarName = eff.triggerStartOfTurn(danger)
					break
		elif self.effects.id == markInfexEff.id:
			cumulatePower = 0
			for eff in self.on.effects:
				if eff.effects.id in [infection.id,epidemicEff.id,intoxEff.id]:
					cumulatePower += eff.effects.power

			if cumulatePower > 0:
				cumulatePower = cumulatePower*self.effects.power/100
				toxiboomEff = classes.effect("Marque d'Intoxication","marqueIntoxication",MAGIE,power=cumulatePower,turnInit=3,emoji='<:megaBact:1128350289980825601>',trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE)
				funnyTempVarName += groupAddEffect(caster=self.caster, target=self.on, area=self.effects.area, effect=toxiboomEff, skillIcon=self.icon)
		elif self.effects.id == mageBanditWeapEff.id:
			tmpEff = randRep([mageBanditFireEff, mageBanditWaterEff, mageBanditAirEff, mageBanditEarthEff])
			groupAddEffect(caster=self.caster, target=self.caster, area=AREA_MONO, effect=tmpEff)
			self.caster.char.element = mageBanditElemDict[tmpEff.id]
		elif self.effects.id == tmpFeliSkill1Eff.id:
			tmpEff = randRep(tmpFeliSkill1ElementTabl)
			groupAddEffect(caster=self.caster, target=self.caster, area=AREA_MONO, effect=tmpEff)
		elif self.effects.id == burningClawEff.id:
			listIndEff, listIndHealEff, listIndLifeSteal = [], [], []
			for eff in self.on.effects:
				tempEff = None
				hpTargetBefore, hpCasterBefore = self.on.hp, eff.caster.hp
				if eff.effects.id in [bleeding.id, kliBloodyEff3.id, coroWind.id]: tempEff = classes.effect(eff.effects.name, eff.effects.id, eff.effects.stat, type=TYPE_INDIRECT_DAMAGE, power=eff.effects.power*eff.value, emoji=eff.icon, lifeSteal=eff.effects.lifeSteal, trigger=TRIGGER_INSTANT)
				elif eff.effects.id == deepWound.id: tempEff = classes.effect(eff.effects.name, eff.effects.id+"1", eff.effects.stat, type=TYPE_INDIRECT_DAMAGE, power=eff.value, emoji=eff.icon, lifeSteal=50, trigger=TRIGGER_INSTANT)
					
				if tempEff != None:
					groupAddEffect(eff.caster, self.on, AREA_MONO, tempEff, self.icon)						  
					listIndEff.append([eff.caster.icon,tempEff.emoji[0][0],hpTargetBefore-self.on.hp])
					if self.caster.hp > hpCasterBefore: listIndLifeSteal.append([eff.caster.icon,tempEff.emoji[0][0],self.caster.hp-hpCasterBefore])
					eff.decate(value=99)

			self.on.refreshEffects()

			indDmgCompilMsg, indHealCompilMsg, indLifeStealCompilMsg = "", "", ""
			if listIndEff != []:
				tablCast, tablIcons, compilDmg = [], [], 0
				for tabl in listIndEff: tablCast, tablIcons, compilDmg = tablCast + [tabl[0]], tablIcons + [tabl[1]], compilDmg + tabl[2]
				tablCast, tablIcons = list(set(tablCast)), list(set(tablIcons))
				castIcons, effIcons = "", ""
				for cast in tablCast: castIcons += cast
				for cast in tablIcons: effIcons += cast
				indDmgCompilMsg = "{0} {1} → {2} -{3} PV\n".format(castIcons, effIcons, self.on.icon, separeUnit(compilDmg))
			
			if listIndLifeSteal != []:
				tablCast, tablIcons, compilDmg = [], [], 0
				for tabl in listIndLifeSteal: tablCast, tablIcons, compilDmg = tablCast + [tabl[0]], tablIcons + [tabl[1]], compilDmg + tabl[2]
				if compilDmg > 0:
					tablCast, tablIcons = list(set(tablCast)), list(set(tablIcons))
					castIcons, effIcons = "", ""
					for cast in tablCast: castIcons += cast
					for cast in tablIcons: effIcons += cast
					indLifeStealCompilMsg = "{0} {1} → {0} +{3} PV\n".format(castIcons, effIcons, self.icon, separeUnit(compilDmg))

			print(indDmgCompilMsg + indHealCompilMsg + indLifeStealCompilMsg)
			return indDmgCompilMsg + indHealCompilMsg + indLifeStealCompilMsg

		elif self.type == TYPE_INDIRECT_HEAL and self.on.hp > 0:			  # Heal Indirect
			return self.triggeredIndHeal()

		elif self.type in [TYPE_INDIRECT_DAMAGE,TYPE_DAMAGE] and self.value > 0 and ((self.effects.area==AREA_MONO and self.on.hp > 0) or self.effects.area != AREA_MONO) and self.on != None:			# Damage indirect
			funnyTempVarName = self.triggeredIndDamage(self.on,decate)

		if self.type == TYPE_DEPL and type(self.effects.callOnTrigger) == classes.depl:
			self.caster.smnDepl(self.effects.callOnTrigger,self.on.cell)
			nonlocal logs
			logs += "\n{0} is placing a {1} at {2}:{3}".format(self.caster.name,self.effects.callOnTrigger.name,self.on.cell.x,self.on.cell.y)
			funnyTempVarName += "{0} a déployé {1} __{2}__ sur la cellule {3}:{4}".format(self.caster.name,self.effects.callOnTrigger.icon[self.caster.team],self.effects.callOnTrigger.name,self.on.cell.x,self.on.cell.y)
			if self.on.cell.on != None:
				funnyTempVarName += " ({0})\n".format(self.on.cell.on.icon)
			else:
				funnyTempVarName += "\n"

		elif self.type == TYPE_SUMMON and type(self.effects.callOnTrigger) == classes.invoc:
			toSummon, cmpt = findSummon(self.effects.callOnTrigger), 0
			nonlocal time, tablEntTeam, tablAliveInvoc
			while cmpt < self.effects.lvl:
				cellToSummon = self.on.cell.getCellForSummon(self.effects.area,self.caster.team,toSummon,self.caster)
				if cellToSummon != None:
					tablEntTeam, tablAliveInvoc, time, tempBlabla = self.caster.summon(toSummon,time,cellToSummon,tablEntTeam,tablAliveInvoc,ignoreLimite=True)
					funnyTempVarName += tempBlabla
					logs += "\n"+tempBlabla
				elif toSummon.npcTeam == NPC_BOMB:
					tmpEff = classes.effect("Explosion",toSummon.skills[0].id,toSummon.skills[0].use,area=toSummon.skills[0].area,type=TYPE_DAMAGE,trigger=TRIGGER_INSTANT,power=toSummon.skills[0].power,emoji=toSummon.skills[0].emoji)
					funnyTempVarName += groupAddEffect(caster=self.caster, target=self.on, area=self.on, effect=tmpEff)
				cmpt += 1

		if self.effects.callOnTrigger != None and type(self.effects.callOnTrigger) not in [classes.invoc, classes.depl]:
			funnyTempVarName += groupAddEffect(caster=self.caster, target=self.on, area=self.effects.area, effect=self.effects.callOnTrigger, skillIcon=self.icon)

		try: 
			for tmpConds in teamJaugeDict[self.caster.team][self.caster].effects.jaugeValue.conds:
				if tmpConds.type == INC_EFFECT_TRIGGERED:
					for tmpEff in tmpConds.add:
						if self.effects.id == tmpEff.id: teamJaugeDict[self.caster.team][self.caster].value = min(100, teamJaugeDict[self.caster.team][self.caster].value+tmpConds.value); funnyTempVarName += "{0} {1} → {0} {2} +{3}\n".format(self.caster.icon, self.icon, teamJaugeDict[self.caster.team][self.caster].icon,tmpConds.value)
		except KeyError: pass

		return funnyTempVarName

	def allStats(self):
		return self.tablAllStats

	def triggeredIndDamage(self,target,decate=True):
		toReturn, tempToReturnDmg, tempToReturnLifeSteal, tempNbDeath, hpAtStart, tempToReturn = "", "", "", 0, self.caster.hp, ""

		if self.effects.type == TYPE_INDIRECT_DAMAGE:
			if self.effects.area != AREA_MONO: tablTarget = target.cell.getEntityOnArea(area=self.effects.area,team=self.caster.team,wanted=ENEMIES,directTarget=False,fromCell=self.caster.cell)
			else: tablTarget = [target]

			nonlocal logs
			dmgDict = {}
			if self.effects.id == lizUlteff.id:
				for eff in self.on.effects:
					if eff.effects.id in [charming.id,charmingHalf.id]:
						self.effects.power += {charming.id:LIZLBPOWERGAINPERCHARM,charmingHalf.id:LIZLBPOWERGAINPERCHARM/2}[eff.effects.id]
						eff.decate(turn=99)
				self.on.refreshEffects()

			lifeStealValue, deads, deadsGender = self.effects.lifeSteal + (TIMELIFESTEAL*int(self.caster.char.secElement == ELEMENT_TIME)), [], 1

			for indx, tmpChipId in enumerate(self.caster.char.equippedChips):
				tmpChip = getChip(tmpChipId)
				if tmpChip != None and (tmpChip.name == "Vampirisme II" or (tmpChip.name == "Héritage d'Estialba" and self.effects.stat in [MAGIE,CHARISMA,INTELLIGENCE]) or (tmpChip.name == "Héritage Lesath" and self.effects.stat in [STRENGTH,AGILITY,PRECISION])):
					lifeStealValue += self.caster.char.chipInventory[tmpChipId].power

			for secTarget in tablTarget:
				if secTarget != None:
					if secTarget.isNpc(TGESL1.name): secTarget = entDict[secTarget.summoner.id]

					reduc = 1
					if secTarget != secTarget and self.effects.area not in [AREA_RANDOMENNEMI_1,AREA_RANDOMENNEMI_2,AREA_RANDOMENNEMI_3,AREA_RANDOMENNEMI_4,AREA_RANDOMENNEMI_5,AREA_ALL_ENEMIES]:
						reduc = max(AOEMINDAMAGE,1-secTarget.cell.distance(target.cell)*AOEDAMAGEREDUCTION)

					tempToReturnDmg, tempLogs = indirectDmgCalculator(self.caster, secTarget, self.effects.power*reduc, self.effects.stat, danger, area=self.effects.area)
					tempToReturn += self.caster.indirectAttack(secTarget,value=tempToReturnDmg,icon = self.icon, name=self.effects.name, canCrit=self.effects.stat!=None)

					if self.effects.id == backupdancerEff1.id+"1":
						for eff in self.caster.effects:
							if eff.effects.id == backupdancerEff1.id: eff.caster.stats.damageBoosted += int(tempToReturnDmg); break
					if secTarget.hp <= 0 and secTarget.char.__class__ not in [classes.invoc]:
						tempNbDeath += 1
						deads.append(secTarget.name)
						if secTarget.char.gender != GENDER_FEMALE:
							deadsGender = 0
					dmgDict[secTarget] = tempToReturnDmg
					logs += "\n[Indirect Damage ; Caster : {0} ; Target : {1};\n  Value : {2} ( {3} )]".format(self.name,secTarget.name,tempToReturnDmg,tempLogs)

					if lifeStealValue and self.caster.id != target.id:
						if self.caster.hp < self.caster.maxHp or getChip("Sur-Vie").id in self.caster.char.equippedChips:
							healPowa = int(tempToReturnDmg*lifeStealValue/100)
							ballerine, chocolatine = self.caster.heal(target=[self.caster,self.on][self.effects.lifeStealOnOn], icon=self.icon, statUse=None, power=healPowa, effName = self.effects.name,danger=danger, lifeSteal = True,direct=False)
							logs += ballerine
							tempToReturnLifeSteal += ballerine

						if self.caster.weaponEffect(toxicure.id):
							toxiEff = copy.deepcopy(toxicure.callOnTrigger)
							toxiEff.lvl = int(tempToReturnDmg*lifeStealValue/100*self.chqr.weapon.effects.power/100)
							addingEffect(caster=self.caster, target=self.caster, area=AREA_MONO, effect=toxiEff, skillIcon=toxicure.emoji[0][0])

					if self.caster.weaponEffect(toxicure.id):
						toxiEff = copy.deepcopy(toxicure.callOnTrigger)
						toxiEff.lvl = int(tempToReturnDmg*toxicure.power/100)
						addingEffect(caster=self.caster, target=self.caster, area=AREA_MONO, effect=toxiEff, skillIcon=toxicure.emoji[0][0])
			if (tempToReturnDmg != "") and ((len(tablTarget) >= 2 and tempNbDeath == 0) or len(tablTarget) >= 5):
				tablDmg = []
				for ent, dmg in dmgDict.items():
					find = False
					for tempDmg in tablDmg:
							tempDmg[1].append(ent)
							tempDmg[2] += dmg
							find = True
							break
					if not(find):
						tablDmg.append([dmg,[ent],dmg])
				for tempDmg in tablDmg:
					icons, moyDmg = "", round(tempDmg[2]/len(tempDmg[1]))
					for ent in tempDmg[1]:
						icons += ent.icon
					toReturn += "{0} {1} → {2} -{3}{4} PV ({5})\n".format(self.caster.icon, self.icon, icons, ["≈",""][moyDmg==tempDmg[0] or len(tempDmg[1])==1], moyDmg, self.effects.name)

				if tempNbDeath > 0:
					tempNames, lenDeads, pluriel = "", len(deads), len(deads)>1
					pluriel = pluriel>1
					for indx, name in enumerate(deads):
						tempNames += name
						if lenDeads > 1 and indx == lenDeads-2:
							tempNames += " et "
						elif lenDeads > 2 and indx < lenDeads-2:
							tempNames += ", "

					toReturn += "{0} {1} vaincu{3}{2} !\n".format(tempNames,["est","sont"][pluriel],["","s"][pluriel],["","e"][deadsGender])
			else: toReturn += tempToReturn

			if tempToReturnLifeSteal != "":
				if len(tablTarget) > 2: toReturn += "{0} {1} → {0} +{2} PV\n".format(self.caster.icon, self.icon, self.caster.hp-hpAtStart)
				else: toReturn += tempToReturnLifeSteal

			if decate: self.decate(value=1)

			if self.caster.weaponEffect([lieWeap, kitsuneWeap]) or (self.caster.isNpc("Kitsune") and type(self.on.char != classes.invoc) and ((skillToUse != None and skillToUse.id != kitsuneSkill4.id) or (skillToUse == None))):
				toReturn += groupAddEffect(caster=self.caster, target=self.on, area=tablTarget, effect=[charming,charmingHalf.id][self.caster.isNpc("Liz")], skillIcon=self.caster.char.weapon.effects.emoji[0][0])

			if self.value > 0:
				if self.effects.id == soulScealEff.id: self.effects.power = round(self.effects.power*1.15,3)
				elif self.effects.id == lieSkillEff.id: self.effects.power = round(self.effects.power*(1+(LIESKILLEFFGAIN/100)),3)
		elif self.effects.type == TYPE_DAMAGE:
			try:
				toReturn = self.caster.attack(target=self.on, value = self.effects.power, icon = self.icon, area=self.effects.area, accuracy=500,use=self.effects.stat)[0]
			except:
				toReturn = ""; print(self.effects.name); print_exc()

		if self.effects.knockback > 0:
			tablEnt, listKnockback = self.on.cell.getEntityOnArea(area=self.effects.area,team=self.caster.team,wanted=ENEMIES,directTarget=False,fromCell=self.caster.cell), []
			tablEnt.sort(key=lambda ent: self.on.cell.distance(ent.cell),reverse=True)
			for ent in tablEnt:
				listKnockback.append(self.caster.knockback(ent,self.effects.knockback,self.on))

			toReturn += "\n"+formatKnockBack(listResult=listKnockback, listEnt=tablEnt, knockbackPower=self.effects.knockback)
		return toReturn

	def triggeredIndHeal(self, decate=True):
		toReturn, tablTargets, initValue = "", self.on.cell.getEntityOnArea(area=self.effects.area,team=self.caster.team,wanted=ALLIES,directTarget=False,fromCell=self.on.cell), self.value

		if self.effects.power > 0 or self.effects.stat in [FIXE, None, PURCENTAGE, MISSING_HP] and tablTargets != []:
			tablHealed, tablRespond = [],[]
			for target in tablTargets:
				targetHp = target.hp
				funnyTempVarName, healed = self.caster.heal(target,self.icon,self.effects.stat,[self.effects.power,self.value][self.effects.stat in [None,FIXE]], self.effects.name, danger, direct=False, incHealJauge = self.effects.incHealJauge, lifeSteal=self.effects.lifeSteal)
				if healed > 0:
					tablRespond.append(funnyTempVarName)
					tablHealed.append([target,healed])
				initValue = initValue - healed

			if len(tablHealed) > 1:
				listIcon, sumHeal = "", 0
				for ent in tablHealed:
					listIcon += ent[0].icon
					sumHeal += ent[1]
				sumHeal = int(sumHeal / len(tablHealed))
				toReturn += "{0} {1} → {2} +≈{3} PV\n".format(self.caster.icon,self.icon,listIcon,sumHeal)
			elif len(tablHealed) == 1:
				toReturn += tablRespond[0]

		toRemove = [1,self.value+1][self.effects.stat in [None,FIXE]]
		if self.effects.id == "bloodButterflyLifeSteal": toRemove = min(self.value, max(0, healed))
		
		if decate: self.decate(value=toRemove)

		if self.effects.callOnTrigger != None: toReturn += groupAddEffect(caster=self.caster, target=self.on, area=self.effects.area, effect=findEffect(self.effects.callOnTrigger),skillIcon=self.icon,actionStats=ACT_HEAL)

		return toReturn

	def replaceEffect(self, effect: classes.effect):
		self.effects = copy.deepcopy(effect)
		self.name, self.turnLeft = effect.name, effect.turnInit
		self.type = effect.type
		self.value = effect.lvl
		if effect.jaugeValue != None and effect.unclearable:
			self.value = 0
			for conds in effect.jaugeValue.conds:
				if conds.type == INC_START_FIGHT: self.value = conds.value
		self.icon = effect.emoji[self.caster.char.species-1][self.caster.team]
		tablTemp = []
		for cmpt in range(CRITICAL+1):
			tablTemp += [0]

		if self.caster.char.element == ELEMENT_TIME and self.effects.type == TYPE_INDIRECT_HEAL: self.effects.power = int(self.effects.power*1.2)

		if self.effects.stat not in [None,FIXE,PURCENTAGE,MISSING_HP]:
			if self.effects.stat is not HARMONIE:
				temp = self.caster.allStats()[self.effects.stat]
			else:
				temp = -111
				for a in self.caster.allStats():
					temp = max(temp,a)

			if self.caster.aspiration in [BERSERK,POIDS_PLUME,TETE_BRULEE,ENCHANTEUR,VIGILANT,PROTECTEUR,MASCOTTE,ASPI_NEUTRAL]:
				temp += int(self.caster.endurance * MELEE_END_CONVERT/100)

			valueBoost, valueResis = min(self.caster.char.level,200)/100 + self.caster.valueBoost(self.on) * (temp+100-self.caster.negativeBoost)/100, self.caster.valueBoost(self.on) * (temp+100-self.caster.negativeShield)/100

		else: valueBoost, valueResis = 1, 1

		secElemMul = 1

		if self.caster.char.secElement in [ELEMENT_AIR, ELEMENT_UNIVERSALIS]:
			secElemMul += 0.05
		if self.on.char.secElement in [ELEMENT_AIR, ELEMENT_UNIVERSALIS]:
			secElemMul += 0.05

		if self.caster.char.element in [ELEMENT_SPACE]:
			secElemMul += 0.1
		elif self.on.char.element in [ELEMENT_SPACE] and self.caster.team == self.on.team:
			secElemMul += 0.05
		elif self.on.char.element in [ELEMENT_SPACE] and self.caster.team != self.on.team:
			secElemMul -= 0.05

		valueBoost = valueBoost*secElemMul

		if self.effects.stat not in [PURCENTAGE]:
			tablTemp[0] += self.effects.strength * valueBoost * 0.01
			tablTemp[1] += self.effects.endurance * valueBoost * 0.01
			tablTemp[2] += self.effects.charisma * valueBoost * 0.01
			tablTemp[3] += self.effects.agility * valueBoost * 0.01
			tablTemp[4] += self.effects.precision * valueBoost * 0.01
			tablTemp[5] += self.effects.intelligence * valueBoost * 0.01
			tablTemp[6] += self.effects.magie * valueBoost * 0.01
			tablTemp[7] += self.effects.resistance * valueBoost * 0.01
			tablTemp[8] += self.effects.percing * valueBoost * 0.01
			tablTemp[9] += self.effects.critical * valueBoost * 0.01
		else:
			tablTemp[0] += self.effects.strength / 100 * self.caster.baseStats[0]
			tablTemp[1] += self.effects.endurance / 100 * self.caster.baseStats[1]
			tablTemp[2] += self.effects.charisma / 100 * self.caster.baseStats[2]
			tablTemp[3] += self.effects.agility / 100 * self.caster.baseStats[3]
			tablTemp[4] += self.effects.precision / 100 * self.caster.baseStats[4]
			tablTemp[5] += self.effects.intelligence / 100 * self.caster.baseStats[5]
			tablTemp[6] += self.effects.magie / 100 * self.caster.baseStats[6]
			tablTemp[7] += self.effects.resistance / 100 * self.caster.baseStats[7]
			tablTemp[8] += self.effects.percing / 100 * self.caster.baseStats[8]
			tablTemp[9] += self.effects.critical / 100 * self.caster.baseStats[9]

		for cmpt in range(8):
			tablTemp[cmpt] = [min(tablTemp[cmpt],0),max(tablTemp[cmpt],0)][self.effects.type == TYPE_BOOST]

		self.inkResistance = min(effect.inkResistance * valueResis,effect.inkResistance*3)

		self.tablAllStats = tablTemp
		self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie,self.resistance,self.percing,self.critical = tuple(tablTemp)

	def triggerThorn(self, target, decate=True):
		if self.effects.callOnTrigger != None:
			return groupAddEffect(caster=self.caster, target=target, area=self.effects.area, effect=self.effects.callOnTrigger, skillIcon=self.icon) + self.decate(value=1)
		elif self.effects.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]:
			return self.triggeredIndDamage(target=target,decate=True)
		elif self.effects.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL]:
			return self.triggeredIndHeal(self, decate=True)

	def changeCaster(self, caster):
		if self.caster.id != caster.id:
			initName, initId = self.caster.name, self.caster.id
			try:
				self.caster.ownEffect.remove({self.on:self.id})
			except:
				print_exc()
			self.caster = caster
			self.caster.ownEffect.append({self.on:self.id})