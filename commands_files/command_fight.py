from commands_files.fight_module.fight_func import *
from socket import error as SocketError
import errno

async def fight(bot : interactions.Client , team1 : list, team2 : list, ctx : interactions.SlashContext, auto:bool = True,contexte:fightContext=fightContext(),octogone:bool=False,bigMap:bool=False, procurFight = [], msg=None, testFight = False, waitEnd = True, notify=False):
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
		now, mainUser, skillToUse, naciaFlag, threadChan, alliedTreaded, entId, selectWindowMsg, hadLb4 = datetime.now(parisTimeZone), loadCharFile("./userProfile/{0}.json".format(ctx.author.id)), None, False, None, [], 0, None, False
		teamJaugeDict, teamHealReistMul, teamArmorReducer, deplTabl, logsName, entDict, allieBDay = [{},{}], [1,1], [1,1], [], ctx.author.tag.replace("/","_"), {}, ""
	
		if mainUser == None: mainUser = loadCharFile(id=int(ctx.author_id))

		# Base vars declalation
		listImplicadTeams, tablAllieTemp, footerText, playOfTheGame, logs, haveError, errorNb, optionChoice = [mainUser.team], copy.deepcopy(tablAllAllies), "", [1500,None,None,""], "[{0}]\n".format(now.strftime("%H:%M:%S, %d/%m/%Y")),False, 0, None
		# dictIsNpcVar creation
		dictIsNpcVar, dictHasBenedicton = copy.deepcopy(primitiveDictIsNpcVar), [[],[]]

		print("[{0}:{1}:{2}] {3} a lancé un combat".format(now.hour,now.minute,now.second,logsName))
		cmpt, tablAllCells, tour, danger, tablAliveInvoc, longTurn, longTurnNumber, standAlone = 0, [], 0, 100, [0,0], False, [], False

		for a in [0,1,2,3,4,5]:			 # Creating the board
			for b in [[0,1,2,3,4],[0,1,2,3,4,5,6]][bigMap]:
				tablAllCells += [cell(a,b,cmpt,tablAllCells)]
				cmpt += 1

		addEffect, tablEntTeam, ressurected, listGuildMembers, dictHasSacrificialShield = [],[],[[],[]], ctx.guild.members, [[],[]]

		def getMember(userId:Union[int,str,Snowflake]) -> Member:
			userId = int(userId)
			for member in listGuildMembers:
				if int(member.id) == userId: return member
			return None

		def add_effect(caster: entity, target: entity, effect: classes.effect, start: str = "", ignoreEndurance=False, danger=danger, setReplica : Union[None,entity] = None, effPowerPurcent=100, useActionStats = ACT_SHIELD, skillIcon="", setValue=None):
			"""Méthode qui rajoute l'effet Effet à l'entity Target lancé par Caster dans la liste d'attente des effets"""
			if type(target) == entity and not(type(target.char) == depl) and type(effect) == classes.effect:
				valid,id,popipo, friableValue = False,0,"", 0
				valid = True
				turn = caster.stats.survival
				if effect.id == elemEff.id:
					effect = tablElemEff[target.char.element]
				elif effect.id == lightStun.id and (target.char.standAlone or target.name in ENEMYIGNORELIGHTSTUN):
					return "🚫 {0} est immunisé{1} aux étourdissements\n".format(target.name,target.accord())
				elif effect.id in [deathMark.id]:
					for eff in target.effects:
						if eff.effects.id == effect.id and eff.caster.id == caster.id:
							eff.effects.power = eff.effects.power + effect.power // 2
							return "{0} {1} → {2}{4} Puissance +{3}\n".format(caster.icon,skillIcon,eff.icon,effect.power // 2,target.icon)
						elif eff.effects.id == reaperEff.id and eff.caster.id == caster.id:
							eff.effects.power = eff.effects.power // 2
							ballerine, babies = eff.caster.heal(target=caster, icon=eff.icon, statUse=PURCENTAGE, power=eff.effects.power, effName = eff.name, danger=danger, mono = True, useActionStats = ACT_HEAL, lifeSteal = False,direct=False)
							eff.decate(turn=99)
							popipo += ballerine
							break
				elif effect.id in [reaperEff.id]:
					for eff in target.effects:
						if eff.id == deathMark.id and eff.caster.id == caster.id:
							eff.decate(turn=99)
							popipo += ballerine
							break
						elif eff.id == reaperEff.id and eff.caster.id == caster.id:
							return f"{caster.icon} {effect.emoji[caster.char.species-1][caster.team]} → 🚫{eff.emoji[caster.char.species-1][caster.team]} {target.icon}\n"
				elif effect.id == neutralCard.id:
					effect = copy.deepcopy(cardAspi[ent.char.aspiration])
					effect.turnInit = effect.turnInit
				elif effect.id == deepWound.id:
					value, tmpLog, boostedValue, resistedValue = dmgCalculator(caster=caster, target=target, basePower=(effect.power*effPowerPurcent/100), use=effect.stat, actionStat=ACT_DIRECT, danger=danger, area=AREA_MONO)
					finded, valueToAdd, castMul, targetMul = False, [value,setValue][setValue!=None], 1, 1
					if type(valueToAdd) != int:
						if type(valueToAdd) in [list,tuple]:
							valueToAdd = int(valueToAdd[0])
						else:
							valueToAdd = int(valueToAdd)
						for eff in target.effects:
							if eff.effects.id in [vulne.id]:
								targetMul = targetMul * ((100+eff.effects.power)/100)
							elif eff.effects.id in [charming.id,kitsuneExCharmEff.id,charmingHalf.id] and caster.char.npcTeam == NPC_KITSUNE:
								targetMul = targetMul * ((100+{charming.id:KITCHARMVULNE, kitsuneExCharmEff.id:KITCHARM2VULNE,charmingHalf.id:KITCHARMVULNE//2}[eff.effects.id])/100)
							elif eff.effects.id in [defenseUp.id,iliStans1_1.id]:
								targetMul = targetMul * ((100-eff.effects.power)/100)

						for eff in caster.effects:
							if eff.effects.id == dmgDown.id:
								castMul -= eff.effects.power/100
							elif eff.effects.id in [dmgUp.id,lenaExSkill5e.id,iliStans2_1.id]:
								castMul += eff.effects.power/100
							elif eff.effects.id == akikiSkill1Eff.id: castMul += akikiSkill1Eff.power * (1-(eff.caster.hp/eff.caster.maxHp))/100

						valueToAdd = int(valueToAdd * castMul * targetMul)

					damageOnArmors = 0
					for eff in target.effects:
						if eff.effects.id == effect.id and eff.caster.id == caster.id:
							for eff2 in target.effects:
								if valueToAdd > 0 and eff.effects.overhealth > 0 and eff.value > 0:
									effValue = eff.value
									returnDmg = eff.triggerDamage(value=valueToAdd, icon=effect.emoji[0][0], declancher = caster)
									damageOnArmors = effValue - eff.value
									valueToAdd -= returnDmg[0]
							if valueToAdd > 0:
								eff.value += valueToAdd
								finded, armorMsg = True, ["","{0} -{1} PAr ".format(["<:abB:934600555916050452>","<:abR:934600570633867365>"][target.team],damageOnArmors)][damageOnArmors>0]
								return "{0} {1} → {5} {4}{2} +{3}\n".format(caster.icon,skillIcon,eff.icon,int(valueToAdd),armorMsg,target.icon)
							elif damageOnArmors > 0:
								finded, armorMsg = True, ["","{0} -{1} PAr ".format(["<:abB:934600555916050452>","<:abR:934600570633867365>"][target.team],damageOnArmors)][damageOnArmors>0]
								return "{0} {1}{3} → {2}\n".format(caster.icon,skillIcon,armorMsg,effect.emoji[0][0])

					if not(finded):
						setValue = valueToAdd
				elif effect.id in naciaElemEffIds:
					for eff in target.effects:
						if eff.effects.id in naciaElemEffIds:
							eff.replaceEffect(effect)
							break
					target.char.splashIcon = naciaSplashIconPulls[effect.id][naciaFlag]
					target.icon = target.char.splashIcon
				elif effect.id == lavenderShield.id:
					potShieldValue, critMsg = calShieldValue(caster,target,(effect.overhealth*effPowerPurcent/100),effect.stat,turn,dangerVal=danger,actStat=useActionStats)
					for eff in target.effects:
						if eff.effects.id == lavenderShield.id:
							ballerine, babies = caster.heal(target, icon=effect.emoji[0][0], statUse=None, power=[eff.value,potShieldValue][eff.value >= potShieldValue], effName = effect.name, danger=danger, direct=True)

							if eff.value < potShieldValue:
								if ballerine == "":
									ballerine = "{0} {1} → {2} {3} +{4} PAr\n".format(caster.icon,skillIcon,target.icon,eff.icon,potShieldValue-eff.value)
								else:
									ballerine = ballerine[:-1]+" {0} +{1} PAr\n".format(eff.icon,potShieldValue-eff.value)
								eff.decate(value=babies+1)
								addEffect.append(fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,TYPE_ARMOR,eff.icon,potShieldValue))
								target.refreshEffects()

							return ballerine

				# Does the effect can be applied ?
				if not(effect.stackable) or effect.reject != None or effect.replace:
					if effect.replace:
						initEff = findEffect(effect)
						if initEff == None: print("Could not find the {0} effect !".format(effect.name))
						else:
							for eff in target.effects:
								if eff.effects.id == initEff.id:
									if effect.overhealth > 0:
										potShieldValue, critMsg = calShieldValue(caster,target,(effect.overhealth*effPowerPurcent/100),effect.stat,turn,dangerVal=danger,actStat=useActionStats)
										initShieldValue = eff.value

										maxValue = potShieldValue + (initShieldValue * (effect.stackable and eff.caster.id == caster.id))
										match eff.id:
											case overshieldEff.id:
												maxValue = round(target.maxHp * (target.char.chipInventory[getChip("Sur-Vie").id].power)/100)
											case convertArmor.id:
												maxValue = round(target.maxHp * 50 / 100)

										potShieldValue = min(potShieldValue,maxValue)

										if potShieldValue > initShieldValue:
											eff.value, eff.leftTurn, difArmor = potShieldValue, effect.turnInit, potShieldValue - initShieldValue
											if eff.caster.id != caster.id: eff.changeCaster(caster)
											return f"{caster.icon} {skillIcon} → {target.icon} {eff.icon} +{difArmor} PAr\n"
										elif not(effect.stackable): return ""
									else:
										if effect.power > eff.effects.power:
											if eff.caster.id != caster.id: eff.changeCaster(caster)
											eff.effects.power, eff.effects.leftTurn, eff.effects.value = max(eff.effects.power, effect.power), effect.turnInit, effect.lvl
											power = ["", " ({0}%)".format(effPowerPurcent)][effPowerPurcent!=100]
											return f"{caster.icon} {skillIcon} → {target.icon} +{eff.icon} __{effect.name}__{power}\n"
										elif caster.id == eff.caster.id:
											eff.effects.leftTurn, eff.effects.value = effect.turnInit, effect.lvl
											power = ["", " ({0}%)".format(effPowerPurcent)][effPowerPurcent!=100]
											return f"{caster.icon} {skillIcon} → {target.icon} +{eff.icon} __{effect.name}__{power}\n"
										else: return f"{caster.icon} {eff.icon} → 🚫{eff.icon} {target.icon}\n"
									valid = False
									break

					if valid and not(effect.stackable):
						for a in target.effects:
							if a.effects.id == effect.id:		  # The effect insn't stackable
								if not(effect.silent):										# It's not Healn't
									popipo = f"{caster.icon} {effect.emoji[caster.char.species-1][caster.team]} → 🚫{a.effects.emoji[caster.char.species-1][caster.team]} {target.icon}\n"
								valid = False

					if valid and effect.reject != None:										   # The effect reject other effects
						for a in effect.reject:
							for b in target.effects:
								if a == b.effects.id:
									popipo = f"{caster.icon} {effect.emoji[caster.char.species-1][caster.team]} → 🚫{findEffect(a).emoji[caster.char.species-1][caster.team]} {target.icon}\n"
									valid = False
									break
							if not(valid):
								break

				if valid:
					valid = False
					id = random.randint(0,maxsize)

					icon = effect.emoji[caster.char.species-1][caster.team]
					if effect.id == darkFlumPoi.id: effect = darkFlumPoi; effect.power = int(caster.char.level * 0.2)
					elif effect.id == constEff.id:
						actPVPurcent = target.hp / target.maxHp
						if effect.stat in [None,FIXE]:
							boostHp = effect.power
						elif effect.stat == PURCENTAGE:
							boostHp = int(target.maxHp*(effect.power/100))
						else:
							if useActionStats == None:
								useActionStats = ACT_BOOST
							boostHp = effect.power * (100+(caster.allStats()[effect.stat]+[caster.negativeHeal,caster.negativeBoost,caster.negativeShield,caster.negativeDirect,caster.negativeIndirect][useActionStats]))/100

						target.maxHp = int(target.maxHp + boostHp)
						target.hp = int(target.maxHp * actPVPurcent)
						toAppend = fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,effect.type,icon,boostHp,effPowerPurcent)
						if not(effect.turnInit < 0 and effect.unclearable):
							addEffect.append(toAppend)
							target.refreshEffects()

						if not(effect.silent):
							return f"{caster.icon} {skillIcon} → {target.icon} +{icon} __{effect.name}__ ({int(boostHp)})\n"
						else:
							return ""
					elif effect.id == aconstEff.id:
						actPVPurcent = target.hp / target.maxHp
						if effect.stat in [None,FIXE]:
							boostHp = effect.power
						elif effect.stat == PURCENTAGE:
							boostHp = int(target.maxHp*(effect.power/100))
						else:
							if useActionStats == None:
								useActionStats = ACT_BOOST
							boostHp = int(effect.power * (100+(caster.allStats()[effect.stat]+[caster.negativeHeal,caster.negativeBoost,caster.negativeShield,caster.negativeDirect,caster.negativeIndirect][useActionStats]))/100)

						nonlocal logs
						logs += "\ntarget%Hp : {0}; maxHpMalus : {1}; targetHp : {2}; targetEnd : {3}\n".format(actPVPurcent,boostHp,int(target.maxHp * actPVPurcent),target.maxHp - boostHp)
						target.maxHp = target.maxHp - boostHp
						target.hp = int(target.maxHp * actPVPurcent)
						toAppend = fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,effect.type,icon,boostHp,effPowerPurcent)
						addEffect.append(toAppend)
						target.refreshEffects()

						if not(effect.silent):
							return f"{caster.icon} {skillIcon} → {target.icon} +{icon} __{effect.name}__ (-{int(boostHp)})\n"
						else:
							return ""
					elif effect.id == charming.id and caster.isNpc("Lia Ex"): effect = kitsuneExCharmEff
					if effect.overhealth > 0:									   # Armor Effect
						shieldPower = (effect.overhealth*effPowerPurcent/100)
						if effect.id == chaosArmor.id:
							shieldPower = random.randint(10,50)
						value, critMsg = calShieldValue(caster,target,shieldPower,effect.stat,turn,dangerVal=danger,actStat=useActionStats)

						maxValue = value
						match effect.id:
							case overshieldEff.id:
								maxValue = round(target.maxHp * (target.char.chipInventory[getChip("Sur-Vie").id].power)/100)
							case convertArmor.id:
								maxValue = round(target.maxHp * 50 / 100)

						value = min(value,maxValue)

						if value>0:
							if type(caster.char) not in [invoc,depl]:
								caster.stats.shieldGived += value
							else:
								entDict[caster.summoner.id].stats.shieldGived += value
								entDict[caster.summoner.id].stats.summonHeal += value

							toAppend = fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,TYPE_ARMOR,icon,value)
							if setReplica != None:
								toAppend.replicaTarget = setReplica

							addEffect.append(toAppend)

							if not(effect.silent):
								popipo = f"{caster.icon} {skillIcon} → {target.icon} {icon} +{separeUnit(value)} PAr{critMsg}\n"

					else:														   # Any other effect
						if effPowerPurcent == 100: effPowerPurcent = None

						toAppend: fightEffect = fightEffect(id,effect,caster,target,effect.turnInit,effect.trigger,effect.type,icon,effect.lvl,effPowerPurcent)
						if setValue != None: toAppend.value = setValue
						if effect.id == undeadEff2.id: toAppend.effects.power = int(target.maxHp * 0.3)
						if effect.trigger != TRIGGER_INSTANT and not(effect.trigger in [TRIGGER_HP_UNDER_70,TRIGGER_HP_UNDER_50,TRIGGER_HP_UNDER_25] and target.hp/target.maxHp <= triggerUnderHp[effect.trigger]):
							if setReplica != None:
								toAppend.replicaTarget = setReplica

							addEffect.append(toAppend)

							if effect.id == "clemBloodJauge":
								caster.clemBloodJauge = toAppend

							if not(effect.silent):
								power = ["", " ({0}%)".format(effPowerPurcent)][effPowerPurcent!=None]
								popipo = f"{caster.icon} {skillIcon} → {target.icon} +{icon} __{effect.name}__{power}\n"
								if effect.id == deepWound.id:
									for eff in target.effects:
										if toAppend.value > 0 and eff.effects.overhealth > 0 and eff.value > 0:
											effValue = eff.value
											returnDmg = eff.triggerDamage(value=toAppend.value, icon=effect.emoji[0][0], declancher = caster)
											damageOnArmors = effValue - eff.value
											toAppend.value -= returnDmg[0]
									armorMsg = ["","{0} -{1} PAr ".format(["<:abB:934600555916050452>","<:abR:934600570633867365>"][target.team],damageOnArmors)][damageOnArmors>0]
									if toAppend.value > 0:
										power = " ({0})".format(toAppend.value)
										popipo = f"{caster.icon} {skillIcon} → {target.icon}{armorMsg} +{icon} __{effect.name}__{power}\n"
									else:
										return f"{caster.icon} {skillIcon}{toAppend.icon} → {target.icon}{armorMsg}\n"

							if effect.id == lightStun.id and type(target.char) in [tmpAllie,char]:
								toAppend = fightEffect(id+1,imuneLightStun,caster,target,imuneLightStun.turnInit,imuneLightStun.trigger,imuneLightStun.type,imuneLightStun.emoji[caster.char.species-1][caster.team],imuneLightStun.lvl,effPowerPurcent)
								addEffect.append(toAppend)
							target.refreshEffects()

							if effect.id in effToSpecialVars:
								target.specialVars.append(effect.id)

							if effect.id in [estial.id,bleeding.id]:							   # If is the Estialba effect
								effLookingFor = {estial.id:heriteEstialbaEff,bleeding.id:heriteLesathEff}[effect.id]
								for eff in caster.effects:
									if eff.effects.id == effLookingFor.id:
										effect = effLookingFor.callOnTrigger
										icon = effect.emoji[caster.char.species-1][caster.team]
										addEffect.append(fightEffect(1,effect,caster,target,effect.turnInit,effect.trigger,effect.type,icon,effect.lvl))

										popipo += f"{caster.icon} {heriteEstialba.emoji} → {target.icon} +{icon} __{effect.name}__\n"
										target.refreshEffects()

							elif effect.id == bloodPactEff.id:
								caster.aspiSlot = bloodPactEff.power
							elif effect.id == partnerIn.id:
								tempTabl = tablEntTeam[caster.team]
								tempTabl.sort(key=lambda chocolatine: getPartnerValue(chocolatine.char),reverse=True)

								if tempTabl[0] == caster:
									tempTabl.remove(caster)

								if len(tempTabl) > 0:
									effect, icon = partnerOut, partnerOut.emoji[0][0]
									addEffect.append(fightEffect(id,effect,caster,tempTabl[0],effect.turnInit,effect.trigger,effect.type,icon,effect.lvl))
									tempTabl[0].refreshEffects()
									toAppend.replicaTarget = tempTabl[0]

						else: popipo = toAppend.triggerInstant(danger)

				if target.hp > 0 or effect.trigger == TRIGGER_INSTANT: return popipo
				else: return ''
			else:
				return ""

		def groupAddEffect(caster:entity, target:entity, area:Union[int,List[entity]], effect:List[classes.effect], skillIcon="", actionStats=ACT_BOOST,effPurcent=100):
			tablName, tablEff, tablIcon, toReturn, tablPurcent, toReturnTmp = [], [], [], "", [], ""
			if type(effect) != list:
				effect = [effect]

			for c in effect:
				eff = findEffect(c)
				if eff != None:
					if type(area) == int:
						tablToSee = target.cell.getEntityOnArea(area=area,team=caster.team,wanted=[ENEMIES,ALLIES][eff.type in friendlyTypes],directTarget=False,fromCell=caster.cell)
					elif type(area) == list:
						tablToSee = area
					else:
						tablToSee = [area]
					for ent in tablToSee:
						if ent != None:
							eff2 = eff
							if eff.id == neutralCard.id:
								eff2 = copy.deepcopy(cardAspi[ent.char.aspiration])
								eff2.turnInit = eff2.turnInit
							elif eff.id == charming.id and caster.isNpc("Kitsune","Lia Ex","Lio Ex"): eff2 = kitsuneExCharmEff
							ballerine = add_effect(caster,ent,eff2,useActionStats=actionStats,skillIcon=skillIcon,effPowerPurcent=effPurcent)
							if '🚫' not in ballerine and ballerine != "":
								if eff2.type == TYPE_ARMOR or eff2.trigger in [TRIGGER_INSTANT,TRIGGER_HP_UNDER_70,TRIGGER_HP_UNDER_50,TRIGGER_HP_UNDER_25] or eff2.id == deepWound.id:
									toReturnTmp += ballerine
								else:
									if eff2.name not in tablEff:
										tablEff.append(eff2.name)
										tablIcon.append(eff2.emoji[caster.char.species-1][caster.team])
										tablName.append(ent.icon)
										tablPurcent.append(eff2.stat in [FIXE,None,PURCENTAGE,MISSING_HP])
									else:
										for cmpt in range(len(tablEff)):
											if tablEff[cmpt] == eff2.name:
												tablName[cmpt]+=ent.icon
												break
								ent.refreshEffects()

			if tablEff != []:
				temp = ""
				if effPurcent != 100 and effPurcent != None: temp = " ({0}%)".format(int(effPurcent))
				for cmpt in range(len(tablEff)): toReturn += "{1} {2} → {3} +{0} __{4}__{5}\n".format(tablIcon[cmpt],caster.icon,skillIcon,tablName[cmpt],tablEff[cmpt],[temp,""][tablPurcent[cmpt]])

			return toReturn+toReturnTmp

		def addingEffect(caster:entity, target:entity, area:Union[int,List[entity]], effect:List[classes.effect], skillIcon="", actionStats=ACT_BOOST,effPurcent=100):
			toReturn = ""
			if type(effect) != list: effect = [effect]

			for c in effect:
				eff:classes.effect = findEffect(c)
				if eff != None:
					if type(area) == int: tablToSee = target.cell.getEntityOnArea(area=area,team=caster.team,wanted=[ENEMIES,ALLIES][eff.type in friendlyTypes],directTarget=False,fromCell=caster.cell)
					elif type(area) == list: tablToSee = area
					else: tablToSee = [area]
					
					for ent in tablToSee:
						if ent != None:
							finded=False
							for eff2 in ent.effects:
								if eff2.effects.id == eff.id:
									valueToAdd, initValue, initPower = [eff2.effects.power, [eff.lvl,eff.overhealth][eff.overhealth>0]][eff2.type == TYPE_ARMOR or eff2.effects.stat in [None,FIXE]], eff2.value, eff2.effects.power
									
									if eff2.type == TYPE_ARMOR or eff2.effects.stat in [None,FIXE]: eff2.value += valueToAdd
									else: eff2.effects.power += valueToAdd
																		
									finded, toReturn = True, toReturn+"{0} {1} → {2} +{3}{4}\n".format(caster.icon,skillIcon,eff.emoji[caster.char.species-1][caster.team],valueToAdd,[""," PAr"][eff.overhealth>0])
									break
							if not(finded): toReturn += groupAddEffect(caster=caster, target=ent, area=[ent], effect=eff, skillIcon=skillIcon, effPurcent=effPurcent)

			return toReturn

		# =============================================== Pre fight things ================================================

		logs += "Fight triggered by {0}\n".format(logsName)
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

		# Temp Anniversary Add
		if not(octogone) and procurFight == []:
			today = (now.day,now.month)
			for tmp in tablAllAllies:
				if today == tmp.birthday:
					ent = copy.deepcopy(tmp)
					ent.changeLevel(team1[0].level, stars=team1[0].stars)
					team1.append(ent)
					allieBDay = ent.name
					break

		tempAlliesTabl, addedAllies = [], 0
		if len(team1) < contexte.nbAllies and not(octogone) and procurFight == []: # Remplisage de la team1
			tempAlliesTabl = tablAllieTemp[:]
			lvlMax = 0
			for a in team1: lvlMax = max(lvlMax,a.level)
			for ally in tablAllieTemp[:]:
				if ally.name == allieBDay:
					try: tempAlliesTabl.remove(ally)
					except: pass
				elif ally.changeDict != None:
					for tempDict in ally.changeDict:
						roll = random.randint(0,99)
						if roll < tempDict.proba:
							tempAlliesTabl.append(getAllieFromBuild(ally, tempDict))
							try: tablAllieTemp.remove(ally)
							except: pass
							break
						else: roll-=tempDict.proba

			vacantRole = ["DPT1","DPT2","DPT3","DPT4","Healer","Booster"]
			for perso in team1:
				if perso.aspiration in [BERSERK,TETE_BRULEE,OBSERVATEUR,POIDS_PLUME,ENCHANTEUR,MAGE]:
					for dptVac in ["DPT1","DPT2","DPT3","DPT4"]:
						if dptVac in vacantRole:
							vacantRole.remove(dptVac)
							break
				elif perso.aspiration in [IDOLE,INOVATEUR,MASCOTTE] and ("Booster" in vacantRole):
					vacantRole.remove("Booster")
				elif perso.aspiration in [PREVOYANT,ALTRUISTE,VIGILANT,PROTECTEUR] and ("Healer" in vacantRole):
					vacantRole.remove("Healer")

			while len(team1) < contexte.nbAllies:
				tablToSee = []
				if len(vacantRole) <= 0: tablToSee = tablAllieTemp
				else:
					for role in vacantRole:
						if role in ["DPT1","DPT2","DPT3","DPT4"]:
							for allie in tablAllieTemp:
								if allie.aspiration in [BERSERK,TETE_BRULEE,OBSERVATEUR,POIDS_PLUME,ENCHANTEUR,MAGE]: tablToSee.append(allie)
						elif role == "Healer":
							for allie in tablAllieTemp:
								if allie.aspiration in [PREVOYANT,ALTRUISTE,VIGILANT,PROTECTEUR]: tablToSee.append(allie)
						elif role == "Booster":
							for allie in tablAllieTemp:
								if allie.aspiration in [IDOLE,INOVATEUR,MASCOTTE]: tablToSee.append(allie)

				temp = random.randint(0,len(tablToSee)-1)
				alea = tablToSee[temp]
				for ally in tablAllieTemp[:]:
					if alea.name == ally.name:
						try: tablAllieTemp.remove(ally)
						except: print_exc()

				for key, value in alea.variantTabl.items():
					randVal = random.randint(0,99)
					if randVal < value: alea = copy.deepcopy(findAllie(key)); break
					else: randVal - value

				if alea.aspiration in [BERSERK,TETE_BRULEE,OBSERVATEUR,POIDS_PLUME,ENCHANTEUR,MAGE]:
					for dptVac in ["DPT1","DPT2","DPT3","DPT4"]:
						try: vacantRole.remove(dptVac); break
						except: pass
				elif alea.aspiration in [IDOLE,INOVATEUR,MASCOTTE]:
					try: vacantRole.remove("Booster")
					except: pass
				elif alea.aspiration in [PREVOYANT,ALTRUISTE,VIGILANT,PROTECTEUR]:
					try: vacantRole.remove("Healer")
					except: pass

				for cmpt in tablIsNpcName:
					if alea.isNpc(cmpt): dictIsNpcVar[f"{cmpt}"] = True; break

				alea.changeLevel(lvlMax,stars=starLevel,changeDict=False)
				alea.stuff = [getAutoStuff(alea.stuff[0],alea),getAutoStuff(alea.stuff[1],alea),getAutoStuff(alea.stuff[2],alea)]
				if alea.level < 10: alea.element = ELEMENT_NEUTRAL
				elif alea.level < 20 and alea.element in [ELEMENT_SPACE,ELEMENT_TIME,ELEMENT_LIGHT,ELEMENT_DARKNESS]: alea.element = ELEMENT_NEUTRAL

				team1 += [alea]
				addedAllies += 1

				logs += "{0} have been added into team1 ({1}, {2}, {3})\n".format(alea.name,alea.stuff[0].name,alea.stuff[1].name,alea.stuff[2].name)

		team1.sort(key=lambda star: star.level, reverse = True)

		if team2 == []: # Génération de la team 2
			lvlMax = team1[0].level - contexte.reduceEnemyLevel
			winStreak = teamWinDB.getVictoryStreak(team1[0])

			if random.randint(0,99) < 85 or not(contexte.allowTemp) or addedAllies > 3 or lvlMax < 15: # Vs normal team
				danger = dangerLevel[winStreak] + (starLevel * DANGERUPPERSTAR)

				tablOctaTemp:List[octarien] = copy.deepcopy(tablAllEnnemies)
				if len(contexte.removeEnemy)>0:
					for enmy in tablOctaTemp[:]:
						if enmy.name in contexte.removeEnemy:
							tablOctaTemp.remove(enmy)

				standAlone = False

				tablTeamOctaPos = [0,0,1,1,2,2]+[random.randint(0,2),random.randint(0,2)]
				tablTeamOctaComp = [4,2,2]

				random.shuffle(tablTeamOctaPos)
				if len(team2) < contexte.nbEnnemis and lvlMax >= 15:
					if random.randint(0,99) < BOSSPURCENT and contexte.allowBoss:			   # Boss ?
						temp = random.randint(0,len(tablBoss)-1)
						alea = copy.deepcopy(tablBoss[temp])
						while team1[0].isNpc("Clémence Exaltée") and alea.isNpc("Clémence pos."):
							temp = random.randint(0,len(tablBoss)-1)
							alea = copy.deepcopy(tablBoss[temp])

						if random.randint(0,99) < HIGHLIGHTPURCENT:
							alea = copy.deepcopy(findEnnemi(HIGHLIGHTBOSS))

						standAlone = alea.standAlone

						alea.changeLevel(lvlMax)
						team2.append(alea)
						logs += "{0} have been added into team2\n".format(alea.name)

				for octa in tablOctaTemp[:]:
					if octa.baseLvl > lvlMax:
						tablOctaTemp.remove(octa)

				octoRolesNPos = [[[],[],[]],[[],[],[]],[[],[],[]]] # 0 : Dmg; 1 : Heal/Armor; 2 : Buff/Debuff

				for octa in tablOctaTemp:
					if octa.aspiration in [BERSERK, POIDS_PLUME, MAGE, ENCHANTEUR, OBSERVATEUR, TETE_BRULEE,SORCELER,ATTENTIF]:
						roleId = 0
					elif octa.aspiration in [ALTRUISTE, PREVOYANT]:
						roleId = 1
					elif octa.aspiration in [IDOLE,INOVATEUR, PROTECTEUR, VIGILANT,MASCOTTE]:
						roleId = 2
					else:
						roleId = random.randint(0,2)

					octoRolesNPos[roleId][octa.weapon.range].append(octa)

				for octa in team2:
					if octa.aspiration in [BERSERK, POIDS_PLUME, MAGE, ENCHANTEUR, OBSERVATEUR, TETE_BRULEE]:
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

				if lvlMax > 20 and procurFight == []:
					while len(team2) < contexte.nbEnnemis and not(standAlone):
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
					while len(team2) < contexte.nbEnnemis and not(standAlone) and len(tablOctaTemp)>0:
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

				del tablOctaTemp
			else: # Vs ally team
				team1.sort(key=lambda funnyTempVarName: funnyTempVarName.level,reverse=True)
				danger, lvlMax = altDanger[winStreak], min(team1[0].level,MAXLEVEL)
				
				tablTeamAlliePos = [0,0,1,1,2,2]+[random.randint(0,2),random.randint(0,2)]
				tablTeamAllieComp = [4,2,2]

				random.shuffle(tablTeamAlliePos)
				allieRolesNPos = [[[],[],[]],[[],[],[]],[[],[],[]]] # 0 : Dmg; 1 : Heal/Armor; 2 : Buff/Debuff

				for allie in tablAllieTemp:
					if allie.aspiration in [BERSERK, POIDS_PLUME, MAGE, ENCHANTEUR, OBSERVATEUR, TETE_BRULEE, SORCELER, ATTENTIF]:
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
						if tablTeamAllieComp[tempCmpt] > 0 and len(allieRolesNPos[tempCmpt][tablTeamAlliePos[0]]) > 0: break

					for secondCmpt in range(len(tablTeamAlliePos)):
						if len(allieRolesNPos[tempCmpt][tablTeamAlliePos[secondCmpt]]) > 0: break

					alea = None
					if len(allieRolesNPos[tempCmpt][tablTeamAlliePos[secondCmpt]]) > 1: alea = randRep(allieRolesNPos[tempCmpt][tablTeamAlliePos[secondCmpt]])
					else:
						try: alea = allieRolesNPos[tempCmpt][tablTeamAlliePos[secondCmpt]][0]
						except: pass

					if alea != None:
						allieRolesNPos[tempCmpt][tablTeamAlliePos[secondCmpt]].remove(alea)
						tablTeamAlliePos.remove(tablTeamAlliePos[secondCmpt])
						tablTeamAllieComp[tempCmpt] -= 1
					else:
						logs += "Hum... Something gone wrong... So hum... emergency procedure\n"
						alea = randRep(tablAllieTemp)

					try: tablAllieTemp.remove(alea)
					except:
						rdmAspi, tablTempAspi = random.randint(0,ASPI_NEUTRAL-1), []
						for ally in tempAlliesTabl:
							if ally.aspiration == rdmAspi: tablTempAspi.append(ally)
						alea = tmpAllie("Akia",2,white,rdmAspi,akiaPreWeapon[rdmAspi],akiaStuffPreDef[rdmAspi],GENDER_FEMALE,randRep(tablTempAspi).skills,deadIcon="<:em:866459463568850954>",icon="<a:akia:993550766415564831>",bonusPoints=recommandedStat[rdmAspi],say=says(start="Je suppose que je vais me dévouer, sinon tout va encre cracher\"\n<:lena:909047343876288552> :\"Merci Akia"))

					for key, value in alea.variantTabl.items():
						randVal = random.randint(0,99)
						if randVal < value: alea = copy.deepcopy(findAllie(key)); break
						else: randVal - value
					
					alea.changeLevel(lvlMax,stars=starLevel)
					alea.stuff = [getAutoStuff(alea.stuff[0],alea), getAutoStuff(alea.stuff[1],alea), getAutoStuff(alea.stuff[2],alea)]

					team2.append(alea)
					logs += "{0} have been added into team2\n".format(alea.name)

				del allieRolesNPos
			for enemy in team2:
				for cmpt in tablIsNpcName:
					if enemy.isNpc(cmpt): dictIsNpcVar[f"{cmpt}"] = True; break

		elif bigMap:
			for enemy in team2:
				for cmpt in tablIsNpcName:
					if enemy.isNpc(cmpt): dictIsNpcVar[f"{cmpt}"] = True; break
			danger = 100 + round(5*starLevel/2,2)

		if not(octogone):
			for ent in team2:
				bossToReplaceName = dictAllyToReplace.keys()
				if ent.__class__ in [tmpAllie, octarien] and ent.name in bossToReplaceName:
					for ent2 in team1:
						if ent2.__class__ in [tmpAllie, octarien] and ent2.name in dictAllyToReplace[ent.name]: ent2.name, ent2.icon, ent2.splashIcon, ent2.says, ent2.deadIcon = "Akia", "<a:akia:993550766415564831>", None, akiaSays, "<:spTako:866465864399323167>"

		if contexte.setDanger or octogone: danger = 100
		elif type(team2[0]) != classes.tmpAllie: winStreak = teamWinDB.getVictoryStreak(team1[0]); danger = dangerLevel[winStreak] + (starLevel * (DANGERUPPERSTAR + max(0,(0.5*starLevel-1))))

		# Updating the Danger and Team Fighting status

		tablTeam, tablEntTeam = [team1,team2],[[],[]]
		readyMsg, nbHealer, nbShielder = None, [0,0], [0,0]

		for teamNum in [0,1]:				 # Entities generations and stats calculations
			for initChar in tablTeam[teamNum]:
				ent = entity(entId, initChar, teamNum, auto=not(type(initChar) == char and not(auto)), danger=danger, tablEntTeam=tablEntTeam)
				entId += 1
				entDict[ent.id] = ent
				tablEntTeam[teamNum].append(ent)
				ent.recalculate()
				await ent.getIcon(bot=bot)
				nbHealer[teamNum], nbShielder[teamNum] = nbHealer[teamNum]+ int(ent.char.aspiration in [VIGILANT,ALTRUISTE]), nbShielder[teamNum]+ int(ent.char.aspiration in [PROTECTEUR,PREVOYANT])

			if nbHealer[teamNum] > (1+int(bigMap)): teamHealReistMul[teamNum] = teamHealReistMul[teamNum] +((nbHealer[teamNum]-1) * HEALRESISTCROIS / (1+int(bigMap))); teamArmorReducer[teamNum] = teamArmorReducer[teamNum] - ((nbShielder[teamNum]-1) * SHIELDREDUC / (1+int(bigMap)))

		def checkHpComponent(inter):
			inter: ComponentContext = inter.ctx
			return int(inter.message.id) == int(msg.id)
		if not(auto):				   # Send the first embed for the inital "Vs" message and start generating the message
			if not(octogone):
				for team in listImplicadTeams:
					try: teamWinDB.changeFighting(team,msg.id,int(ctx.channel_id),team2)
					except: pass

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
							if cmpt != len(allStats) - 1: tempMsg += ", "
						logs += tempMsg

		# Placement phase -----------------------------------------------------
		logs += "\n=========\nInitial placements phase\n=========\n\n"
		tablLineTeamGround, placementlines, allAuto, maxPerLine = [[0,1,2],[3,4,5]], [[[],[],[]],[[],[],[]]], True, [5,7][bigMap]

		for actTeam in [0,1]:			   # Sort the entities and place them
			logs += "len(team1) : {0}; len(team2) : {1}\n".format(len(team1),len(team2))
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

						nbMeleeEnt = len(tablEntOnLine[lineVal])
						if nbMeleeEnt > 0:
							for pos in range(nbMeleeEnt):
								tablEntOnLine[lineVal][pos].move(y=tablSetPos[nbMeleeEnt][pos],x=xLinePos)
								logs += "{0} moved from {1}:{2} to {3}:{4}\n".format(tablEntOnLine[lineVal][pos].char.name,0,0,xLinePos,tablSetPos[nbMeleeEnt][pos])

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

						random.shuffle(emptyCells[0])
						random.shuffle(emptyCells[1])

						for ent in unplaced:
							if len(emptyCells[ent.team]) > 0:
								rdmCell = emptyCells[ent.team].pop()
								ent.move(cellToMove=rdmCell)
								logs += "{0} has been randomly placed at {1}:{2}\n".format(ent.char.name,rdmCell.x,rdmCell.y)
							else:
								print("{0} have no cell to be placed !".format(ent.name))
								for celly in tablAllCells:
									if celly.on == None and celly.x == [3,2][ent.team]:
										emptyCells[ent.team].append(celly)
								if len(emptyCells[ent.team]):
									random.shuffle(emptyCells[ent.team])
									rdmCell = emptyCells[ent.team].pop()
									ent.move(cellToMove=rdmCell)
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

					try:
						for cmpt in range(len(tablEntOnLine[lineVal])):
							if len(prePos[lineVal]) > 1:
								rand = random.randint(0,len(prePos[lineVal])-1)
							else:
								rand = 0
							ruby = prePos[lineVal][rand]
							prePos[lineVal].remove(ruby)
							tablEntOnLine[lineVal][cmpt].move(y=ruby[1],x=ruby[0])
							logs += "{0} has been place at {1}:{2}\n".format(tablEntOnLine[lineVal][0].char.name,ruby[0],ruby[1])
					except IndexError:
						listCells = []
						for celly in tablAllCells:
							if celly.x < 3 and celly.on == None: listCells.append(celly)
						rdmCell = randRep(listCells)
						tablEntOnLine[lineVal][cmpt].move(cellToMove=rdmCell)
						logs += "{0} has been place at {1}:{2} (emergency placement)\n".format(tablEntOnLine[lineVal][0].char.name,rdmCell.x,rdmCell.y)


				lineVal += 1

		if not(auto):					   # Edit the Vs embed for his message
			initTeamEmbed = interactions.Embed(title = "__Ce combat oppose :__",color = light_blue, description=reduceEmojiNames("{0}\n\n__Carte__ :\n{1}".format(versus,map(tablAllCells,bigMap))))
			initTeamEmbed.add_field(name = "__Taux de danger :__",value=str(danger),inline=False)
			if footerText != "":
				initTeamEmbed.set_footer(text=footerText,icon_url=ctx.author.avatar_url)

		if not(auto):					   # User there ?
			allReady = False
			already, awaited, awaitedChar = [],[],[]
			dateLimite = datetime.now(parisTimeZone) + timedelta(seconds=15)
			addNotif, removeNotif = Button(style=ButtonStyle.GRAY,label="Me notifier à la fin du combat",emoji=getEmojiObject('🔔'),custom_id="notif"), Button(style=ButtonStyle.GRAY,label="Supprimer la notification",emoji=getEmojiObject('🔕'),custom_id="notif")

			if procurFight == []:
				for teamNum in tablEntTeam: # Génération du tableau des utilisateurs devant confirmer leur présence
					for ent in teamNum:
						if ent.auto == False and ent.char.owner > 100:
							owner = None
							try: 
								owner = bot.get_member(ent.char.owner, ctx.guild_id)
								if owner != None: awaitedChar.append(ent); awaited.append(owner)
								else: ent.auto = True
							except: ent.auto = True
						else:
							ent.auto = True

				readyButton = Button(style=ButtonStyle.SUCCESS,label="Rejoindre le combat",emoji=PartialEmoji(name="✅"),custom_id="readyButton")
				while not(allReady): # Demande aux utilisateurs de confirmer leur présence
					readyEm = interactions.Embed(title = "__Combat manuel__",color=light_blue)
					readyEm.set_footer(text="Les utilisateurs n'ayant pas réagis dans les 15 prochaines secondes seront considérés comme combattant automatiques")
					tmpNotifButton = [addNotif, removeNotif][notify]
					tablMentions = ["", ""]
					for cmpt in [0,1]: 
						for tmpMember in [awaited, already][cmpt]: tablMentions[cmpt] += tmpMember.mention + ", "
						if tablMentions[cmpt] != "": readyEm.add_field(name = ["En attente de :","Prêts :"][cmpt], value = tablMentions[cmpt][:-1])

					await msg.edit(embeds = [initTeamEmbed,readyEm], components=[ActionRow(readyButton,tmpNotifButton)])

					def checkIsIntendedUser(reaction:ComponentContext):
						reaction: ComponentContext = reaction.ctx
						for awaitedUsers in awaited: 
							if int(reaction.author.id) == int(awaitedUsers.id): return True

					try:
						timeLimite = (dateLimite - datetime.now(parisTimeZone)).total_seconds()
						react:ComponentContext = await bot.wait_for_component(messages=msg,components=[readyButton,tmpNotifButton],check=checkIsIntendedUser,timeout=timeLimite)
						react:ComponentContext = react.ctx
					except asyncio.TimeoutError: break
					else:
						if react.custom_id == tmpNotifButton.custom_id: notify = not(notify); await react.send(content=["🔔 Vous serez notifié à la fin du combat","🔕 La notification a été annulée"][not(notify)], ephemeral=True)
						else:
							awaited.remove(react.author)
							already.append(react.author)
							allAuto = False

							try:
								for team in (0,1):
									for ent in tablEntTeam[team]:
										if int(ent.char.owner) == int(react.author.id):
											if threadChan == None:
												threadChan: interactions.BaseChannel = await msg.create_thread(name = "Fight : {0}".format(ctx.author.tag))
												selectWindowMsg = await threadChan.send(embeds=await getRandomStatsEmbed(bot,team1,"Fenêtre de sélection de l'action"))
												await threadChan.add_member(react.author)
												await threadChan.send("__Description de personnage :__",embeds=ent.char.getSkillsDescription())
											else:
												thMembers: List[ThreadMember] = await threadChan.get_members()
												finded = False
												for member in thMembers:
													if member.id == react.id: finded = True; break

												if not(finded): await threadChan.add_member(react.author)
												await threadChan.send("__Description de personnage :__",embeds=ent.char.getSkillsDescription())
											await react.send("✅ Vous avez rejoint le combat avec votre personnage\n{0}".format(selectWindowMsg.jump_url),ephemeral=True)
							except: print_exc()

							if awaited == []: allReady = True

			else:
				listProc = []
				for ent in tablEntTeam[0]:
					for proc in procurFight:
						if ent.name == proc.name: ent.char.owner == 0; listProc.append(ent)
				while 1:
					readyEm = interactions.Embed(title = "__Combat manuel__",color=light_blue)
					readyEm.set_footer(text="Vous avez 15 secondes pour sélectionner votre personnage")
					tmpNotifButton = [addNotif, removeNotif][notify]
					fieldValue, procSelectOptions = "", []

					for ent in listProc:
						if ent.char.owner == 0:
							fieldValue += "{0} {1} : *En attente...*\n".format(ent.icon,ent.name)
							procSelectOptions.append(StringSelectOption(label=ent.name,value=ent.name,description="En attente...",emoji=getEmojiObject(ent.icon)))
						else:
							entOwner: Member = getMember(ent.char.owner)
							if entOwner == None:
								fieldValue += "{0} {1} : [Utilisateur non trouvé]\n".format(ent.icon,ent.name)
								procSelectOptions.append(StringSelectOption(label=ent.name,value=ent.name,description="Utilisateur non trouvé",emoji=getEmojiObject(ent.icon)))
							else:
								fieldValue += "{0} {1} : {2}\n".format(ent.icon,ent.name, entOwner.mention)
								procSelectOptions.append(StringSelectOption(label=ent.name,value=ent.name,description=entOwner.tag,emoji=getEmojiObject(ent.icon)))
					
					procSelect = StringSelectMenu(procSelectOptions,custom_id="tempProcurSelect",placeholder="Choisissez un Allié Temporaire à jouer")
					readyEm.add_field("__Allié Temporaires :__",fieldValue)
					await msg.edit(embeds = [initTeamEmbed,readyEm], components=[ActionRow(procSelect),ActionRow(tmpNotifButton)])

					try:
						timeLimite = (dateLimite - datetime.now(parisTimeZone)).total_seconds()
						react = await bot.wait_for_component(messages=msg,components=[procSelect,tmpNotifButton],timeout=timeLimite)
						react: ComponentContext = react.ctx
					except asyncio.TimeoutError: break
					else:
						if react.custom_id == tmpNotifButton.custom_id: notify = not(notify); await react.send(content=["🔔 Vous serez notifié à la fin du combat","🔕 La notification a été annulée"][not(notify)], ephemeral=True)
						else:
							for ent in tablEntTeam[0]:
								if react.values[0] == ent.name:
									allAuto = False
									if ent.char.owner == 0:
										ent.char.owner = int(react.author.id)
										ent.auto = False
										for ent2 in tablEntTeam[0]:
											if ent2 != ent and ent2.char.owner == int(react.author.id):
												ent2.char.owner = 0
												ent2.auto = True
										await react.send("✅ Vous avez rejoins le combat avec {0}".format(ent.name),ephemeral=True)
										try:
											charDescList = []
											if ent.isNpc("Gwendoline") and ent.char.weapon.id == gwenyWeap.id:
												tempKlikli, tempAlty = findAllie("Klironovia"), findAllie("Altikia")
												charList = [ent.char,getAllieFromBuild(tempKlikli,tempKlikli.changeDict[-1]),getAllieFromBuild(tempAlty,tempAlty.changeDict[-1])]
												for gwenPersonality in charList:
													charDescList.append(gwenPersonality.getSkillsDescription())

											if ent.name not in alliedTreaded:
												if threadChan == None:
													threadChan: interactions.BaseChannel = await msg.create_thread(name = "Fight : {0}".format(ctx.author.tag))
													selectWindowMsg = await threadChan.send(embeds=await getRandomStatsEmbed(bot,team1,"Fenêtre de sélection de l'action"))
													await threadChan.add_member(react.author)
													for inx, emb in enumerate(charDescList):
														await threadChan.send(["__Description de personnage :__",""][inx>0],embeds=emb)
												else:
													thMembers: List[ThreadMember] = await threadChan.get_members()
													finded = False
													for member in thMembers:
														if member.id == react.id:
															finded = True
															break

													if not(finded):
														await threadChan.add_member(react.author)
													for inx, emb in enumerate(charDescList):
														await threadChan.send(["__Description de personnage :__",""][inx>0],embeds=emb)
												alliedTreaded.append(ent.name)
										except: pass

									else:
										entOwner: Member = getMember(ent.char.owner)
										if entOwner.id == react.author.id:
											await react.send("❌ Vous avez déjà choisi ce personnage",ephemeral=True)
										elif react.author.id == ctx.author.id and react.author.id != entOwner.id:
											ent.char.owner = int(react.author.id)
											ent.auto = False
											for ent2 in tablEntTeam[0]:
												if ent2 != ent and ent2.char.owner == 0:
													ent2.char.owner = int(entOwner.id)
													await react.send("✅ Vous avez rejoins le combat avec {0}".format(ent.name),ephemeral=True)
													try:
														if ent.name not in alliedTreaded:
															if threadChan == None:
																threadChan: interactions.BaseChannel = await msg.create_thread(name = "Fight : {0}".format(ctx.author.tag))
																selectWindowMsg = await threadChan.send(embeds=await getRandomStatsEmbed(bot,team1,"Fenêtre de sélection de l'action"))
																await threadChan.add_member(react.author)
																await threadChan.send("__Description de personnage :__",embeds=ent.char.getSkillsDescription())
															else:
																thMembers: List[ThreadMember] = await threadChan.get_members()
																finded = False
																for member in thMembers:
																	if member.id == react.id:
																		finded = True
																		break

																if not(finded):
																	await threadChan.add_member(react.author)
																await threadChan.send("__Description de personnage :__",embeds=ent.char.getSkillsDescription())
															alliedTreaded.append(ent.name)
													except:
														print_exc()
													break
										elif entOwner.id == ctx.author.id:
											await react.send("❌ Ce personnage a déjà été choisi par l'initiateur de la commande",ephemeral=True)
										else:
											ownerChar, reactChar, initChar = loadCharFile(path="./userProfile/{0}.txt".format(int(entOwner.id))),loadCharFile(path="./userProfile/{0}.txt".format(int(react.id))),loadCharFile(path="./userProfile/{0}.txt".format(int(ctx.author.id)))
											if reactChar.team == initChar.team and ownerChar.team != initChar.team:
												ent.char.owner = int(react.author.id)
												ent.auto = False
												for ent2 in tablEntTeam[0]:
													if ent2 != ent and ent2.char.owner == 0:
														ent2.char.owner = int(entOwner.id)
														await react.send("✅ Vous avez rejoins le combat avec {0}".format(ent.name),ephemeral=True)
														try:
															if ent.name not in alliedTreaded:
																if threadChan == None:
																	threadChan: interactions.BaseChannel = await msg.create_thread(name = "Fight : {0}".format(ctx.author.tag))
																	selectWindowMsg = await threadChan.send(embeds=await getRandomStatsEmbed(bot,team1,"Fenêtre de sélection de l'action"))
																	await threadChan.add_member(react.author)
																	await threadChan.send("__Description de personnage :__",embeds=ent.char.getSkillsDescription())
																else:
																	thMembers: List[ThreadMember] = await threadChan.get_members()
																	finded = False
																	for member in thMembers:
																		if member.id == react.id:
																			finded = True
																			break

																	if not(finded):
																		await threadChan.add_member(react.author)
																	await threadChan.send("__Description de personnage :__",embeds=ent.char.getSkillsDescription())
																alliedTreaded.append(ent.name)
														except:
															print_exc()
														break
											elif reactChar.team != initChar.team and ownerChar.team == initChar.team:
												await react.send("❌ Ce personnage a déjà été choisi par un membre de l'équipe de l'initiateur de la commande",ephemeral=True)
											else:
												await react.send("❌ Vous n'avez pas pu choisir ce personnage",ephemeral=True)

			temp, awaitNum, temp2 = "", len(awaited), ""
			if awaitNum == 1: temp = awaited[0].mention
			elif awaitNum == 2: temp = f"{awaited[0].mention} et {awaited[1].mention} "
			elif awaitNum != 0:
				for a in range(0,awaitNum-2): temp += f"{awaited[a].mention}, "
				temp += f"{awaited[a+1].mention} et {awaited[a+2].mention} "
			else: temp = "-"

			if awaitNum != 0: temp2 = f"\n\n{temp} seront considérés comme combattants automatiques"
			statingEmb = interactions.Embed(title = "Initialisation",color = light_blue,description = f"Le combat va commencer {emLoading}{temp2}")

			if threadChan != None and selectWindowMsg != None: await threadChan.send(content=selectWindowMsg.jump_url)

			await msg.edit(embeds = [initTeamEmbed,statingEmb], components=[])

			for z in awaitedChar:
				for b in awaited:
					if b.id == int(z.char.owner): z.auto = True; break

		# Timeline's initialisation -----------------------------------------
		tempTurnMsg = "__Début du combat :__"
		time = timeline()
		time, tablEntTeam = time.init(tablEntTeam, entDict)

		logs += "\n=========\nStuffs passives effects phase\n=========\n\n"
		for team in [0,1]:								  # Says Start
			for ent in tablEntTeam[team]:
				if ent.char.says.start != None and random.randint(0,99)<33:
					if ent.isNpc("Alice"):						  # Alice specials interractions
						if dictIsNpcVar["Hélène"]:									# Helene in the fight
							tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"__Arf, pourquoi je dois faire équipe avec elle déjà (＃￣0￣) ?__")
							if dictIsNpcVar["Clémence"]:
								if random.randint(0,99) < 50:
									tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:clemence:908902579554111549>',"__S'il te plait Alice, commence pas... Elle fait même pas le même taff que toi.__")
									if dictIsNpcVar["Lena"]:
										tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:lena:909047343876288552>',"Je sais que c'est tentant de se parler avec des ultra-sons quand on a votre ouïe, mais si vous pôuviez plutôt vous concentrer sur le combat ce sera cool")
								else:
									tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:clemence:908902579554111549>',"Je l'ai entendue celle là !")
					
						elif dictIsNpcVar["Félicité"] and dictIsNpcVar["Sixtine"] and dictIsNpcVar["Clémence"]:		 # All sisters in the fight
							tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"Allez ! Un p'tit combat en famille !")

						elif dictIsNpcVar["Félicité"] or dictIsNpcVar["Sixtine"]:						 # A sister in the fight (except Clémence)
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

					elif ent.isNpc("Clémence"):					 # Clémence specials interractions
						if dictIsNpcVar["Alice"] or dictIsNpcVar["Félicité"] or dictIsNpcVar["Sixtine"]:		  # With her sisters
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
								tempTurnMsg += "\n<:ruby:1112519724799103037> : *\"`Ricane` Tu as peur que je pense que tu as régréssé ?\"*"
							elif randy < 66:
								tempTurnMsg += "\n<:ruby:1112519724799103037> : *\"Tu sais bien que je suis toujours interresée par tes progrès\"*"
							elif dictIsNpcVar["John"]:
								tempTurnMsg += "\n<:ruby:1112519724799103037> : *\"Je suis plutôt là pour surveiller un certain loup garou aujourd'hui\"*"
								if random.randint(0,99) < 60:
									tempTurnMsg += "\n<:john:908887592756449311> : *`Ne se sens pas vraiment à l'aise avec les auras des deux puissantes vampires cotes à cotes`*"
						else:
							tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,ent.char.says.start)

					elif ent.isNpc("Shushi"):					   # Shushi specials interractions
						if dictIsNpcVar["Lena"]:
							tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,"Allez Miman ! Ti va touz les défonzer !")
							if random.randint(0,99) < 50:
								if random.randint(0,99) < 50:
									tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:lena:909047343876288552>',"Voyons Shushi, c'est quoi ce language ?")
								else:
									tempTurnMsg += "\n{0} : *\"{1}\"*".format('<:lena:909047343876288552>',"`Ricane`")

						else:
							tempTurnMsg += "\n{0} : *\"{1}\"*".format(ent.icon,ent.char.says.start)

					elif ent.isNpc("Shihu"):						# Shihu specials interractions
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

		if tempTurnMsg != "__Début du combat :__": tempTurnMsg += "\n"

		nbLB, LBBars = [8,8], [[0,0],[0,0]]
		# Passives skills and stuffs effects ---------------------------------
		for team in [0,1]:
			teamHasLb = False
			for ent in tablEntTeam[team]:
				if ent.char.__class__ not in [classes.invoc]:
					ballerine, babie = ent.passiveInitialisation()
					tempTurnMsg += ballerine
					logs += babie
					for bosses in tablBoss+tablRaidBoss:
						if ent.isNpc(bosses): LBBars[0][0] += 1
					if ent.char.standAlone: LBBars[0][0] += 1
					ent.stats.hpPerTurn[tour], ent.stats.dmgPerTurn[tour], ent.stats.healPerTurn[tour], ent.stats.armorPerTurn[tour], ent.stats.suppPerTurn[tour] = max(ent.hp,0), 0, 0, 0, 0
			if type(tablEntTeam[team][0].char) in [tmpAllie,char]: LBBars[team][0] = int(len(tablEntTeam[team])>=8)+int(len(tablEntTeam[team])>=16)+int(type(tablEntTeam[not(team)][0].char) in [tmpAllie,char])
			elif teamHasLb: LBBars[team][0] = 1

		for cmpt, tablEff in enumerate([contexte.giveEffToTeam1,contexte.giveEffToTeam2]):
			if len(tablEff) > 0:
				lenPy = entity(0,copy.deepcopy(findAllie("Lena")),cmpt,False,True)
				groupAddEffect(lenPy, tablEntTeam[cmpt][0], tablEntTeam[cmpt], tablEff)

		for team in [0,1]:
			for ent in tablEntTeam[team]:
				try:
					for conds in teamJaugeDict[team][ent].effects.jaugeValue.conds:
						if conds.type == INC_START_FIGHT:
							teamJaugeDict[team][ent].value = min(teamJaugeDict[team][ent].value+conds.value,100)
				except KeyError:
					pass

		if tablEntTeam[1][0].isNpc("The Giant Enemy Spider"):		   # Giant Enemy Spider's legs summoning
			surrondingsCells = [findCell(tablEntTeam[1][0].cell.x-1,tablEntTeam[1][0].cell.y-1,tablAllCells),findCell(tablEntTeam[1][0].cell.x-1,tablEntTeam[1][0].cell.y,tablAllCells),findCell(tablEntTeam[1][0].cell.x-1,tablEntTeam[1][0].cell.y+1,tablAllCells),findCell(tablEntTeam[1][0].cell.x,tablEntTeam[1][0].cell.y-1,tablAllCells),findCell(tablEntTeam[1][0].cell.x,tablEntTeam[1][0].cell.y+1,tablAllCells),findCell(tablEntTeam[1][0].cell.x+1,tablEntTeam[1][0].cell.y-1,tablAllCells),findCell(tablEntTeam[1][0].cell.x+1,tablEntTeam[1][0].cell.y,tablAllCells),findCell(tablEntTeam[1][0].cell.x+1,tablEntTeam[1][0].cell.y+1,tablAllCells)]
			tablTemp = [TGESL1,TGESL2]
			for cmpt in range(8):
				if surrondingsCells[cmpt].on == None:
					toSummon = copy.deepcopy(tablTemp[cmpt//4])
					tablEntTeam, tablAliveInvoc, time, funnyTempVarName = tablEntTeam[1][0].summon(toSummon,time,surrondingsCells[cmpt],tablEntTeam,tablAliveInvoc,ignoreLimite=True)
					logs += "\n"+funnyTempVarName

		elif tablEntTeam[1][0].isNpc("Jevil"):						  # Jevil Confusiong effect
			for teamCmpt in [0,1]:
				for ent in tablEntTeam[teamCmpt]:
					add_effect(tablEntTeam[1][0],ent,jevilEff)
					ent.refreshEffects()

		if dictIsNpcVar["Lena"] and (dictIsNpcVar["Shushi"] or dictIsNpcVar["Shihu"]):
			lenaEnt = None
			targetEnt = None
			for team in [0,1]:
				for ent in tablEntTeam[team]:
					if ent.isNpc("Lena"):
						lenaEnt = ent
					elif ent.isNpc('Shushi',"Shihu"):
						targetEnt = ent
					if lenaEnt != None and targetEnt != None: break
				if lenaEnt != None and targetEnt != None: break
		
			if lenaEnt != None and targetEnt != None and lenaEnt.team == targetEnt.team:
				add_effect(lenaEnt,targetEnt,lenaShuRedirect)

		for team in [0,1]:												 # Raise skills verifications
			for ent in tablEntTeam[team]:
				for skilly in ent.skills + ent.effects:
					if type(skilly)==skill:
						if skilly.type in [TYPE_INDIRECT_REZ,TYPE_RESURECTION] or (skilly.effectAroundCaster != None and skilly.effectAroundCaster[0] == TYPE_RESURECTION):
							for ent2 in tablEntTeam[team]:
								ent2.ressurectable = True
							break

				for eff in ent.effects:
					if eff.effects.jaugeValue != None :
						teamJaugeDict[team][ent] = eff
						break

		if not(auto):							   # Send the turn 0 msg
			if tempTurnMsg == "__Début du combat :__":
				tempTurnMsg += "\n -"
			emby = interactions.Embed(title=f"__Tour {tour}__",description= reduceEmojiNames(tempTurnMsg),color = light_blue)
			if footerText != "":
				emby.set_footer(text=footerText,icon_url=ctx.author.avatar_url)
			embInfo = interactions.Embed(title = "__Combat (D.{0})__".format(danger), color = mainUser.color, description=reduceEmojiNames("__Carte__ :\n{0}\n__Timeline__ :\n{1}".format(map(tablAllCells,bigMap,deplTabl=deplTabl),time.icons())))
			await msg.edit(embeds = [embInfo,emby])
			await asyncio.sleep(2+(min(len(tempTurnMsg),2000)/2000*3))

		fight, ennemi, counterTracker = True, tablEntTeam[1][0], {}
		if isLenapy and not(octogone):
			teamWinDB.refreshFightCooldown(mainUser.team,auto,fromTime=now)
		# Effective Fight Start --------------------------------------------------------------------------
		tempTurnMsg = ""
		try:
			while fight:
				everyoneDead, skillUrl = [True,True], None
				actTurn: entity = time.getActTurn()
				nextNotAuto,lastNotAuto = 0,0

				everyoneStillThere = False
				for ent in time.timeline : # Looking for the next not auto player
					if not(ent.auto):
						everyoneStillThere = True
						if ent.hp > 0: nextNotAuto = ent; break

				if not(everyoneStillThere): allAuto = True

				if nextNotAuto != actTurn and not(auto) and not(allAuto):
					if lastNotAuto != nextNotAuto: choiceEmbDesc = nextNotAuto.quickEffectIcons(); await selectWindowMsg.edit(embeds=interactions.Embed(title = "Fenêtre de selection de l'action", color=nextNotAuto.char.color,description = f"En attente du tour de {nextNotAuto.char.name} {emLoading}\n{choiceEmbDesc}")); lastNotAuto = nextNotAuto
					elif nextNotAuto == 0: await selectWindowMsg.edit(embeds=interactions.Embed(title = "Fenêtre de selection de l'action", color=light_blue,description = f"Il n'y a plus de combattants manuels en vie")); lastNotAuto = nextNotAuto

				if allAuto and selectWindowMsg != None and threadChan != None:
					selectWindowMsg = None
					try: threadChan = await threadChan.delete()
					except: print_exc()

				if actTurn.hp > 0 and not(type(actTurn.char) in [classes.invoc]): tempTurnMsg = f"__Début du tour de {actTurn.char.name} :__\n"

				actTurnCell = actTurn.cell

				# New table turn ----------------------------
				if actTurn == time.begin:
					funnyTempVarName, counterTracker = "", {}
					tour += 1
					logs += "\n\n=========\nTurn {0}\n=========".format(tour)

					for team in [0,1]:
						for ent in tablEntTeam[team]:
							if ent.hp > 0:
								ent.stats.survival += 1
								if ent.cell != None:
									if ent.cell.on != ent and ent.cell.on == None: ent.cell.on = ent; print("{0} n'était pas sur sa cellule, apparament".format(ent.char.name))
								else: raise Exception("{0} n'est pas sur une cellule !!".format(ent.char.name))

						if LBBars[team][0] > 0: LBBars[team][1] = min(LBBars[team][1]+(1+2*int(naciaFlag)),LBBars[team][0]*3)

					if tour >= 21:
						funnyTempVarName += f"\n__Mort subite !__\nTous les combattants perdent **{SUDDENDEATHDMG*(tour-20)}%** de leurs PV maximums\n"
						for a in [0,1]:
							for b in tablEntTeam[a]:
								if b.hp > 0:
									if b.char.standAlone: lose = int(b.maxHp*((SUDDENDEATHDMG/1000)*(tour-20)))
									else: lose = int(b.maxHp*((SUDDENDEATHDMG/100)*(tour-20)))
									funnyTempVarName += "{0} : -{1} PV\n".format(b.icon,lose)
									b.hp -= lose
									b.stats.selfBurn += lose
									if b.hp <= 0: funnyTempVarName += b.death(killer=b,trueDeath=True)
									for skil in range(len(b.skills)):
										if type(b.skills[skil]) == skill and b.skills[skil].type in [TYPE_RESURECTION,TYPE_INDIRECT_REZ]: b.cooldowns[skil] = 99

						if not(auto):
							if len(funnyTempVarName) > 4096:
								funnyTempVarName = unemoji(funnyTempVarName)
								if len(funnyTempVarName) > 4096: funnyTempVarName = "OVERLOAD"
							await msg.edit(embeds = [embInfo,interactions.Embed(title=f"__Tour {tour}__",description=funnyTempVarName)],components=[infoSelect])
							await asyncio.sleep(1.8+(min(len(funnyTempVarName),2000)/2000*3))

						logs += funnyTempVarName

					tempMsg = ""
					for entDepl in deplTabl[:]:
						entDepl[0].startOfTurn()
						if entDepl[0].leftTurnAlive > 0 and entDepl[0].char.lifeTime > 0:
							if not(entDepl[0].char.trap): tempMsg += entDepl[0].triggerDepl()
							elif entDepl[0].char.trap and entDepl[0].leftTurnAlive == 1: entDepl[0].skills.power, entDepl[0].skills.effPowerPurcent = entDepl[0].skills.power/2, entDepl[0].skills.effPowerPurcent/2
							entDepl[0].leftTurnAlive = entDepl[0].leftTurnAlive -1

						if entDepl[0].leftTurnAlive <= 0 and len(entDepl[0].ownEffect) == 0:
							try:
								deplTabl.remove(entDepl)
							except:
								print_exc()

					if not(auto) and tempMsg != "":
						tempMsg = reduceEmojiNames(tempMsg)
						emby = interactions.Embed(title=f"__Tour {tour}__",description=tempMsg,color = actTurn.char.color)
						tried, cmpt = 0, 0
						while getEmbedLength(embInfo)+getEmbedLength(emby) > 5500:
							if tried == 0:
								finded = False
								for field in embInfo.fields:
									if cmpt < len(statEmbedFieldNames) and statEmbedFieldNames[cmpt] in field.name:
										field.value, finded, cmpt = "[...]", True, cmpt + 1
								if cmpt == len(statEmbedFieldNames)-1 or not(finded):
									tried += 1
							elif tried == 1:
								emby.description = emby.description[5500-(getEmbedLength(embInfo)+getEmbedLength(emby)):]
								if len(emby.description) > 4050:
									emby.description = emby.description[len(emby.description)-4050]
								tried += 1
							else:
								emby.description = "OVERLOAD"
								break

						await msg.edit(embeds = [embInfo,emby],components=[infoSelect])
						await asyncio.sleep(1+(min(len(tempMsg),2000)/2000*3))

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
						for team in [0,1]:			 # Result msg character showoff
							for ent in tablEntTeam[team]:
								if type(ent.char) not in [invoc,depl]:
									pvTabls[team] = [pvTabls[team][0]+max(0,ent.hp),pvTabls[team][1]+max(0,ent.maxHp)]
									raised = ""
									if ent.status == STATUS_RESURECTED and ent.raiser != None:
										raised = " ({1}{0})".format(ent.raiser,['<:rezB:907289785620631603>','<:rezR:907289804188819526>'][ent.team])
									elif ent.status == STATUS_TRUE_DEATH and ent.raiser != None:
										raised = " ({0})".format(['<:diedTwiceB:907289950301601843>','<:diedTwiceR:907289935663485029>'][ent.team])

									addText = ent.getMedals(listClassement)
									if addText != "":
										addText = " "+addText
									resultMsg = reduceEmojiNames("{0} {1}{2}\n".format(ent.icon,ent.char.name,addText))
									
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

						resultEmbed = interactions.Embed(title = "__Combat rapide en cours <a:loading:862459118912667678> :__",color = mainUser.color,description="Vous pouvez toujours lancer des combats normaux durant ce chargement\n__Tour {0}__".format(tour))

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

								if len(temp2)>0 and temp2[-2:-1] != "\n":
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
								resultEmbed.add_field(name="\n__Equipe 3 :__",value=tablEntTeam[1][0],inline=True)

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

				# Generating the first part of the main message -
				if not(auto):
					embInfo = interactions.Embed(title = "__Combat Normal (D.{0})__".format(danger),color = mainUser.color,description="__Carte__ :\n{0}".format(map(tablAllCells,bigMap,deplTabl=deplTabl)))
					tempFieldValue = time.icons()+"\n<:em:866459463568850954>"
					if len(tempFieldValue) > EMBED_FIELD_VALUE_LENGTH:
						tempFieldValue = ""
						for cmpt in range(min(len(time.timeline),5)):
							tempFieldValue += "{0} ← ".format(time.timeline[cmpt].icon)
						if len(time.timeline) > 5:
							tempFieldValue += " [...]"

					embInfo.add_field(name="<:em:866459463568850954>\n__Timeline__",value=tempFieldValue)
					if footerText != "": embInfo.set_footer(text=footerText,icon_url=ctx.author.avatar_url)

				# Start of the turn ---------------------------------------------------------------------------------
				wasAlive = actTurn.hp > 0
				temp,atRange = "",actTurn.atRange()
				nbTargetAtRange = len(atRange)
				if wasAlive:
					logs += "\n\nTurn {0} - {1}:".format(tour,actTurn.char.name)

				funnyTempVarName = actTurn.startOfTurn()
				tempTurnMsg += reduceEmojiNames(funnyTempVarName)
				logs += "\n"+funnyTempVarName
				deathCount = bigRaiseCount = 0

				# Main messages statistics generation ---------------------------------------------------------------
				if not(auto) and (wasAlive or actTurn.hp > 0):
					infoOp,temp = [], ""
					for a in [0,1]:	 # Generating the Hp's select menu
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
								infoOp += [interactions.StringSelectOption(label=unhyperlink(b.char.name),value=str(b.id),emoji=getEmojiObject(b.icon),description=f"{separeUnit(max(0,b.hp))} PV{armorTxt} ({max(0,round(b.hp/b.maxHp*100))}%{armorPurcent}), R.S. : {b.healResist}%{raised}")]
					infoSelect =  interactions.ActionRow(interactions.StringSelectMenu(infoOp,custom_id = "seeFightersPv", placeholder="Voir les PVs des combattants"))

					temp2 = actTurn.allStats()+[actTurn.resistance,actTurn.percing]
					critRate = round(probCritDmg(actTurn),1)
					temp2 += [critRate]
					for a in range(CRITICAL+1):			   # Generating the stats field of the main message
						if a == 7:
							temp += f"\n\n__Réduction de dégâts__ : {temp2[a]}%"
						elif a == 8:
							temp += f"\n__Taux pénétration d'armure__ : {temp2[a]}%"
						elif a == 9:
							temp += f"\n__Taux de coup critique__ : {min(temp2[a],80)}%"
						else:
							temp += f"\n__{allStatsNames[a]}__ : {temp2[a]}"

					level = str(actTurn.char.level) + ["","<:littleStar:925860806602682369>{0}".format(actTurn.char.stars)][actTurn.char.stars>0]
					embInfo.add_field(name = f"__{actTurn.icon} {unhyperlink(actTurn.char.name)}__ (Niveau {level})",value=f"PV : {max(0,actTurn.hp)} / {actTurn.maxHp}",inline = False)
					embInfo.add_field(name = statEmbedFieldNames[0],value=actTurn.effectIcons(),inline = True)
					embInfo.add_field(name = statEmbedFieldNames[1],value = temp,inline = True)
					embInfo.add_field(name = "<:em:866459463568850954>",value='**__Liste des effets :__**',inline=False)
					adds, deplMsg = "", ""

					for team in [0,1]:								  # Generating the effects fields of the main message
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
							teamView = reduceEmojiNames(teamView)
							if len(teamView2[0]) <= (1024-len(teamView)):
								teamView += teamView2[0]
							elif len(teamView2[1]) <= (1024-len(teamView)):
								teamView += teamView2[1]
							elif len(teamView2[2]) <= (1024-len(teamView)):
								teamView += teamView2[2]
							else:
								teamView = "Overload"

						embInfo.add_field(name=[statEmbedFieldNames[-2],statEmbedFieldNames[-1]][team],value=reduceEmojiNames(teamView),inline=True)

					if teamJaugeDict != [{},{}]:
						for team in [0,1]:
							jaugeField = ""
							for jaugeEnt, jaugeEff in teamJaugeDict[team].items():
								if jaugeEnt.hp > 0:
									jaugeField += "{0} : {1} ".format(jaugeEnt.icon,jaugeEff.icon)
									nbFieldEm, cmpt = len(jaugeEff.effects.jaugeValue.emoji[0]), 0
									nbPointPerField = 100/nbFieldEm
									while cmpt * nbPointPerField < jaugeEff.value: cmpt += 1
									if jaugeEff.value - nbPointPerField * (cmpt-1) < (nbPointPerField * cmpt/2) and cmpt > 0: cmpt -= 1

									jaugeField += jaugeEff.effects.jaugeValue.emoji[jaugeEff.value > 25][0]+jaugeEff.effects.jaugeValue.emoji[jaugeEff.value>=65][1]+jaugeEff.effects.jaugeValue.emoji[jaugeEff.value>=90][2]
									jaugeField += " **{0}**\n".format(round(jaugeEff.value,2))
									jaugeField = reduceEmojiNames(jaugeField)
							
							if len(jaugeField) > EMBED_FIELD_VALUE_LENGTH:
								jaugeField = ""
								for jaugeEnt, jaugeEff in teamJaugeDict[team].items():
									if jaugeEnt.hp > 0:
										jaugeField += "{0} : {1} ".format(jaugeEnt.icon,jaugeEff.name)
										jaugeField += " **{0}**\n".format(round(jaugeEff.value,2))

								jaugeField = reduceEmojiNames(jaugeField)
						
							if jaugeField:
								embInfo.add_field(name="__Jauges :__",value=jaugeField,inline=False)

					for deplEnt in deplTabl:
						if deplEnt[0].leftTurnAlive > 0 and deplEnt[0].name != lenaInkStrike_depl1.name:
							on = ""
							if deplEnt[1].on != None:
								on = " ({0})".format(deplEnt[1].on.icon)
							deplMsg += reduceEmojiNames("{0}{1} {2}:{3}{4}\n".format(deplEnt[0].summoner.icon, deplEnt[0].icon, deplEnt[1].x, deplEnt[1].y, on))

					if len(deplMsg) > 1000:
						deplMsg = ""
						for deplEnt in deplTabl:
							if deplEnt[0].leftTurnAlive > 0:
								deplMsg += reduceEmojiNames("{0} {1} {2}:{3}\n".format(deplEnt[0].summoner.icon, deplEnt[0].name, deplEnt[1].x, deplEnt[1].y, on))
						deplMsg += reduceEmojiNames("{0}{1} {2}:{3}{4}\n".format(deplEnt[0].summoner.icon, deplEnt[0].icon, deplEnt[1].x, deplEnt[1].y, on))
					if deplMsg != "":
						embInfo.add_field(name="__Déployables :__",value=deplMsg,inline=embInfo.fields[-1].name=="__Jauges :__")

					if nextNotAuto == actTurn:
						await msg.edit(embeds = [embInfo,interactions.Embed(title=f"__Tour {tour}__",description=reduceEmojiNames(tempTurnMsg),color = actTurn.char.color)],components=[infoSelect])

				# Turn actions --------------------------------------------------------------------------------------
				statsTurnDict = {}
				for team in [0,1]:
					for ent in tablEntTeam[team]:
						if type(ent.char) not in [classes.invoc, classes.depl]:
							entPAR = 0
							for eff in ent.effects:
								if eff.effects.overhealth > 0:
									entPAR += eff.value
							statsTurnDict[ent.id] = {
								"hp":ent.hp,
								"par":entPAR,
								"damage":ent.stats.damageDeal,
								"kill":ent.stats.ennemiKill,
								"heal":ent.stats.heals,
								"raise":ent.stats.allieResurected,
								"armoredDamage":ent.stats.armoredDamage,
							}

				if actTurn.hp > 0:
					cmpt,iteration,replay,allyRea = 0,actTurn.char.weapon.repetition,False,actTurn.stats.allieResurected
					unsuccess = True

					# ========== Playing the turn ==============
					if not(actTurn.stun):				   # The entity isn't stun, so he can play his turn
						allReadyMove, hadReplayed = False, False
						while 1:
							nowStartOfTurn = datetime.now(parisTimeZone)
							atRange, nbTargetAtRange = actTurn.atRange(), len(actTurn.atRange())
							onReplica = False
							for eff in actTurn.effects:
								if eff.effects.replica != None:
									onReplica = eff
									eff.decate(turn=1)
									actTurn.refreshEffects()
									break

							canMove,cellx,celly = [True,True,True,True],actTurn.cell.x,actTurn.cell.y
							surrondings = actTurn.cell.getSurrondings()
							for a in range(0,len(surrondings)):
								if surrondings[a] != None:
									if surrondings[a].on != None and surrondings[a].on.status != STATUS_TRUE_DEATH:
										canMove[a] = False
								else:
									canMove[a] = False

							# The entity isn't already casting something
							if onReplica == False:
								if not(actTurn.auto) :					  # Manual Fighter - Action select window
									haveOption,unsuccess, waitingSelect, haveIterate, lbSkill = False,False, interactions.ActionRow(interactions.StringSelectMenu([interactions.StringSelectOption(label="Veillez patienter...",value="PILLON!",emoji=PartialEmoji(name='🕑'),default=True)],custom_id = "anotherWaitingSelect",disabled=True)), False, None
									def check(m):
										m = m.ctx
										return int(m.author.id) == int(actTurn.char.owner) and m.message.id == selectWindowMsg.id

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
										choiceMsgTemp,tempTabl,tablCooldown,canBeUsed = getPrelimManWindow(actTurn, LBBars, tablEntTeam)+"\n\n__Options disponibles :__",[actTurn.char.weapon],[0]+actTurn.cooldowns,[]

										cmpt, tried = 0, 0
										while getEmbedLength(embInfo)+getEmbedLength(emby) > 5900:
											if tried == 0:
												finded = False
												for field in embInfo.fields:
													if cmpt < len(statEmbedFieldNames) and statEmbedFieldNames[cmpt] in field.name:
														field.value, finded, cmpt = "[...]", True, cmpt + 1
												if cmpt == len(statEmbedFieldNames)-1 or not(finded):
													tried += 1
											elif tried == 1:
												emby.description = emby.description[5500-(getEmbedLength(embInfo)+getEmbedLength(emby)):]
												if len(emby.description) > 4000:
													emby.description = emby.description[len(emby.description)-4000:]
												tried += 1
											else:
												emby.description = "OVERLOAD"
												break

										# Generating the main menu of the window
										for indx, skillToSee in enumerate(actTurn.skills):
											if not(actTurn.silent) and type(skillToSee) == classes.skill and actTurn.cooldowns[indx] <= 0:								   # If the option is skillToSee valid option and the cooldown is down
												tablToSee = []
												if skillToSee.become != None:
													tablToSee, tablEffId = [], []
													for eff in actTurn.effects:
														tablEffId.append(eff.effects.id)

													for skilly in skillToSee.become:
														ifEligible = True
														if skilly.jaugeEff != None:
															try: ifEligible = teamJaugeDict[actTurn.team][actTurn].effects.id == skilly.jaugeEff.id and teamJaugeDict[actTurn.team][actTurn].value >= skilly.minJaugeValue
															except KeyError: pass

														if ifEligible:
															if skilly.needEffect != None:
																for eff in skilly.needEffect:
																	eff = findEffect(eff)
																	if eff.id not in tablEffId:
																		ifEligible = False
																		break

															if ifEligible and skilly.rejectEffect != None:
																for eff in skilly.rejectEffect:
																	if eff.id in tablEffId:
																		ifEligible = False
																		break

															if ifEligible:
																tablToSee.append(skilly)
												else:
													tablToSee = [skillToSee]

												for tempOption in tablToSee:
													if type(tempOption) == weapon and len(actTurn.atRange()) > 0 and actTurn.char.weapon.id not in cannotUseMainWeapon:				  # Aff. the number of targets if the option is skillToSee Weapon
														canBeUsed += [tempOption]
														choiceMsgTemp += f"\n{tempOption.emoji} {tempOption.name} (Cibles à portée : {str(nbTargetAtRange)})\n"
													elif type(tempOption) != weapon:
														if type(tempOption) == classes.skill:
															line = tempOption.type in [TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE,TYPE_DAMAGE]
															target = [ALLIES,ENEMIES][line]
															if len(actTurn.cell.getEntityOnArea(area=tempOption.range,team=actTurn.team,wanted=target,lineOfSight=line,dead=tempOption.type == TYPE_RESURECTION,fromCell=actTurn.cell)) > 0:
																choiceMsgTemp += f"\n\n{tempOption.emoji} __{tempOption.name} :__\n"
																choiceMsgTemp += tempOption.getSummary() +"\n"
																canBeUsed += [tempOption]

										if len(actTurn.cell.getEntityOnArea(area=AREA_CIRCLE_1,team=actTurn.team,wanted=ALLIES,fromCell=actTurn.cell)) > 1:
											tempOption = copy.deepcopy(friendlyPush)
											tempOption.emoji = ["<:movePlz:928756987532029972>","<a:sparta:928795602328903721>"][random.randint(0,1)]
											line = tempOption.type in hostileTypes
											target = [ALLIES,ENEMIES][line]
											if len(actTurn.cell.getEntityOnArea(area=tempOption.range,team=actTurn.team,wanted=target,lineOfSight=line,fromCell=actTurn.cell)) > 0:
												choiceMsgTemp += f"\n\n{tempOption.emoji} __{tempOption.name} :__\n" + [tempOption.getSummary(),tempOption.description][tempOption.description!=None] + "\n"
												canBeUsed += [tempOption]

										if LBBars[actTurn.team][1]>=3:
											line = lbSkill.type in [TYPE_INDIRECT_DAMAGE,TYPE_MALUS,TYPE_DAMAGE,TYPE_DAMAGE]
											target = [ALLIES,ENEMIES][line]
											if len(actTurn.cell.getEntityOnArea(area=lbSkill.range,team=actTurn.team,wanted=target,lineOfSight=line,dead=lbSkill.type == TYPE_RESURECTION,fromCell=actTurn.cell)) > 0:
												choiceMsgTemp += f"\n{lbSkill.emoji} __{lbSkill.name} :__\n"
												choiceMsgTemp += "> {0}\n".format(lbSkill.description.replace("\n","\n> "))
												canBeUsed += [lbSkill]

										choiceMsgTemp += "\n"
										if canMove[0] or canMove[1] or canMove[2] or canMove[3]:						   # If the ent. can move, add the Move option
											canBeUsed += [option("Déplacement",'👟')]
											choiceMsgTemp += "👟 Déplacement\n"

										canBeUsed += [option("Passer",'🚫')]											   # Adding the Pass option, for the dark Sasuke who think that actualy playing the game is to much for them
										choiceMsgTemp += "🚫 Passer"

										mainOptions,cmpt = [],0
										for a in canBeUsed:					 # Generating the select menu
											mainOptions += [interactions.StringSelectOption(label=unhyperlink(a.name),value=str(cmpt),emoji=getEmojiObject(a.emoji))]
											
											cmpt += 1

										mainSelect = interactions.StringSelectMenu(mainOptions,custom_id = "selectAOption",placeholder = "Séléctionnez une option :")
										emby = interactions.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color)
										if footerText != "":
											emby.set_footer(text=footerText,icon_url=ctx.author.avatar_url)

										if haveIterate:						 # Time limite stuff
											await selectWindowMsg.edit(embeds=interactions.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = reduceEmojiNames(choiceMsgTemp)),components=[infoSelect,waitingSelect])
											await asyncio.sleep(3)

										await selectWindowMsg.edit(embeds=interactions.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = reduceEmojiNames(choiceMsgTemp)),components=[infoSelect,interactions.ActionRow(mainSelect)])
										haveIterate = True

										validoption = False
										def checkMainOption(m):
											m = m.ctx
											return int(m.author.id) == int(actTurn.char.owner)
										while not(validoption):
											try:
												try:
													react = await bot.wait_for_component(messages=selectWindowMsg,check=checkMainOption,timeout = 30)
													react: ComponentContext = react.ctx
												except asyncio.TimeoutError:
													unsuccess = True
													break
											except asyncio.TimeoutError:
												unsuccess = True
												break

											mainSelect.disabled = True
											react = canBeUsed[int(react.values[0])]
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
												weapOptions += [interactions.StringSelectOption(label=listNumberEmoji[a] + " "+unhyperlink(atRange[a].char.name),value=str(a),emoji=getEmojiObject(atRange[a].icon),description=desc)]

											weapOptions += [interactions.StringSelectOption(label="Retour",value=str(a+1),emoji=PartialEmoji(name='◀️'))]
											weapSelect = interactions.StringSelectMenu(weapOptions,custom_id = "weapSelect",placeholder="Sélectionnez une cible :")
											mainSelect = ActionRow(mainSelect)
											mainSelectEmbed = interactions.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = reduceEmojiNames(choiceMsgTemp))

											if len(weapOptions) == 2:
												weapSelect = interactions.ActionRow(
													interactions.Button(style=ButtonStyle.SUCCESS, label=weapOptions[0].label, emoji=weapOptions[0].emoji, custom_id=weapOptions[0].value),
													interactions.Button(style=ButtonStyle.SECONDARY, label=weapOptions[1].label, emoji=weapOptions[1].emoji, custom_id=weapOptions[1].value)
													)
												
												await selectWindowMsg.edit(embeds=mainSelectEmbed,components=[mainSelect,weapSelect])

											elif choiceMsgTemp != "":
												choiceMsgTemp = reduceEmojiNames(choiceMsgTemp)
												await selectWindowMsg.edit(embeds=mainSelectEmbed,components=[mainSelect,waitingSelect])
												await asyncio.sleep(3)
												await selectWindowMsg.edit(embeds=mainSelectEmbed,components=[mainSelect,ActionRow(weapSelect)])

											try:
												react = await bot.wait_for_component(messages=selectWindowMsg,check=check,timeout=timeLimite)
												react: ComponentContext = react.ctx
											except:
												unsuccess = True
												break

											if len(weapOptions) > 2:
												selectedOptionSelect = [getChoisenSelect(weapSelect,react.values[0])]
											else:
												selectedOptionSelect = None

											optionChoice = OPTION_WEAPON
											if react.component_type == ComponentType.STRING_SELECT:
												value = int(react.values[0])
											else:
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
													if skillToUse.type == TYPE_DEPL:
														tablCells.sort(key=lambda ballerine: len(ballerine.getEntityOnArea(area=react.depl.skills.area,team=actTurn.team,wanted=[ALLIES,ENEMIES][react.depl.skills.type in hostileTypes], ignoreInvoc = True, directTarget=False, fromCell= ballerine))+0.5-(ballerine.distance(actTurn.cell)*0.1),reverse=True)
														targetAtRangeSkill = tablCells[:min(len(tablCells),5)]
													else:
														targetAtRangeSkill = [actTurn.cell.getCellForSummon(area=skillToUse.range, team=actTurn.team, summon=findSummon(skillToUse.invocation), summoner=actTurn)]
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

											skillOptions, choiceMsgTemp = [], reduceEmojiNames("__Carte :__\n{0}\n\n__Combattants à portée :__\n".format(map(tablAllCells,bigMap,viArea,fromEnt=actTurn,wanted=[ENEMIES,ALLIES][skillToUse.type in funnyTempVarName],numberEmoji=targetAtRangeSkill,fullArea=altViArea)))

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
													skillOptions += [interactions.StringSelectOption(label=listNumberEmoji[a] + " "+unhyperlink(targetAtRangeSkill[a].char.name),value=str(a),emoji=getEmojiObject(targetAtRangeSkill[a].icon),description=desc)]
												
												if react.area in [AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES] or react.range == AREA_MONO:
													skillOptions = [interactions.StringSelectOption(label="Valider",value='✅',emoji=PartialEmoji(name='✅'))]

											elif skillToUse.type == TYPE_SUMMON:
												choiceMsgTemp =f"Voulez vous invoquer {skillToUse.invocation} ?"
												skillOptions = [interactions.StringSelectOption(label="Valider",value='✅',emoji=PartialEmoji(name='✅'))]
												a = 0

											else:
												nbTargetAtRangeSkill = len(targetAtRangeSkill)

												for a in range(nbTargetAtRangeSkill):
													choiceMsgTemp += f"{listNumberEmoji[a]} - {targetAtRangeSkill[a].x}:{targetAtRangeSkill[a].y}\n"
													desc = f"{targetAtRangeSkill[a].x} - {targetAtRangeSkill[a].y}"
													desc += f", Zone : {len(targetAtRangeSkill[a].getEntityOnArea(area=react.depl.skills.area,team=actTurn.team,wanted=[ALLIES,ENEMIES][react.depl.skills.type in hostileTypes],directTarget=False,fromCell=actTurn.cell))}"
													skillOptions += [interactions.StringSelectOption(label=str(targetAtRangeSkill[a].x) + ":" + str(targetAtRangeSkill[a].y),value=str(a),emoji=PartialEmoji(name=listNumberEmoji[a]),description=desc)]
												
												if react.area in [AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES] or react.range == AREA_MONO:
													skillOptions = [interactions.StringSelectOption(label="Valider",value='✅',emoji=PartialEmoji(name='✅'))]

											skillOptions += [interactions.StringSelectOption(label="Retour",value=str(a+1),emoji=PartialEmoji(name='\u25C0'))]
											skillSelect = interactions.StringSelectMenu(skillOptions,custom_id = "skillOptions")
											mainSelect = ActionRow(mainSelect)

											if len(skillOptions) == 2:
												skillSelect = None
												for a in skillOptions:
													if skillSelect == None:
														skillSelect = ActionRow(interactions.Button(style=[ButtonStyle.SUCCESS,interactions.ButtonStyle.SECONDARY][a.label == "Retour"],label=a.label, emoji=a.emoji, custom_id=a.label))
													else:
														skillSelect.add_component(interactions.Button(style=[ButtonStyle.SUCCESS,interactions.ButtonStyle.SECONDARY][a.label == "Retour"],label=a.label, emoji=a.emoji, custom_id=a.label))

												await selectWindowMsg.edit(embeds=interactions.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp),components=[mainSelect,skillSelect])

											elif choiceMsgTemp != "":
												await selectWindowMsg.edit(embeds=interactions.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp),components=[mainSelect,waitingSelect])
												await asyncio.sleep(3)
												await selectWindowMsg.edit(embeds=interactions.Embed(title = f"Choix de l'option - {react.name}",color = actTurn.char.color,description = choiceMsgTemp),components=[mainSelect]+[interactions.ActionRow(skillSelect)])

											try:
												react = await bot.wait_for_component(messages=selectWindowMsg,timeout = 30,check=check)
												react: ComponentContext = react.ctx
											except:
												unsuccess = True
												break

											if len(skillOptions) > 2:
												selectedOptionSelect = [getChoisenSelect(skillSelect,react.values[0])]
											else:
												selectedOptionSelect = None

											if react.component_type == ComponentType.BUTTON and react.custom_id == 'Valider':
												ennemi = actTurn
												optionChoice = OPTION_SKILL
												haveOption = True
												break
											elif react.component_type == ComponentType.BUTTON and react.custom_id != 'Retour':
												ennemi = targetAtRangeSkill[0]
												optionChoice = OPTION_SKILL
												haveOption = True
												break
											elif react.component_type == ComponentType.STRING_SELECT and int(react.values[0]) < len(targetAtRangeSkill):
												ennemi = targetAtRangeSkill[int(react.values[0])]
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
														movingOption[cmpt] = interactions.Button(style=2, label="Aller sur {0}:{1}".format(surrondings[cmpt].x,surrondings[cmpt].y),emoji=getEmojiObject(moveEmoji[cmpt]),custom_id=moveEmoji[cmpt],disabled=not(canMove[cmpt]))
													else:
														movingOption[cmpt] = interactions.Button(style=2,label="Aller en dehors du monde",emoji=getEmojiObject(moveEmoji[cmpt]),custom_id=moveEmoji[cmpt],disabled=True)

												allMouvementOptions = interactions.ActionRow(movingOption[0],movingOption[1],movingOption[2],movingOption[3])
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
																mapLike += '<:em:866459463568850954>'

														if cmpt != 2:
															mapLike += "|"
													mapLike += "\n"

												mapLike = reduceEmojiNames(mapLike)
												await selectWindowMsg.edit(embeds=interactions.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = "Dans quelle direction voulez vous aller ?\n\n"+mapLike),components=[infoSelect,cancelButton,allMouvementOptions])

												choiceToMove = None
												while choiceToMove == None:
													try:
														choiceMove = await bot.wait_for_component(messages=selectWindowMsg,timeout=30,check=check)
														choiceMove : ComponentContext = choiceMove.ctx
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
									await selectWindowMsg.edit(embeds=interactions.Embed(title = f"Choix de l'option - {actTurn.icon} {actTurn.char.name}",color = actTurn.char.color,description = "Tour en cours "+emLoading),components=[])

								if not(actTurn.auto) and unsuccess:
									if actTurn.missedLastTurn == False:
										actTurn.missedLastTurn = True

									else:
										actTurn.auto = True
										nowStartOfTurn = datetime.now(parisTimeZone)

								elif not(actTurn.auto) and not(unsuccess):
									actTurn.missedLastTurn = False

								if unsuccess or type(ennemi)==int: # AI's stuffs
									team2maxHp, team2Hp, team1maxHp, team1Hp, optionChoisen = 1, 0, 1, 0, False
									for ent in tablEntTeam[int(not(actTurn.team))]:
										if ent.hp > 0 and type(ent.char) not in [invoc]:
											team2maxHp, team2Hp = team2maxHp+ent.maxHp, team2Hp+ent.hp

									for ent in tablEntTeam[actTurn.team]:
										if ent.hp > 0 and type(ent.char) not in [invoc]:
											team1maxHp, team1Hp = team1maxHp+ent.maxHp, team1Hp+ent.hp

									teamMatesHpRatio = team1Hp / team1maxHp
									ennemiesdying, alliesdying = team2Hp / team2maxHp <= 0.3, teamMatesHpRatio <= 0.4

									# Définition du type d'IA :
									choisenIA = actTurn.IA

									if actTurn.char.aspiration in [IDOLE, INOVATEUR, PREVOYANT, VIGILANT, MASCOTTE] and len(tablEntTeam[actTurn.team])>5 and teamMatesHpRatio > 0.3:
										allyDPTAlive = 0
										for ent in tablEntTeam[actTurn.team]:
											if ent.char.aspiration in [BERSERK,OBSERVATEUR,POIDS_PLUME,TETE_BRULEE,MAGE,ENCHANTEUR,ATTENTIF,SORCELER] and ent.hp > 0:
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
												if eff.effects.id == estial.id:
													poisonCount += 1

										if poisonCount >= 8:
											optionChoice = OPTION_SKILL
											skillToUse: classes.skill = serenaSpe
											ennemi = actTurn
											optionChoisen = True

									elif actTurn.char.aspiration in [IDOLE, INOVATEUR, VIGILANT, PROTECTEUR, MASCOTTE] and not(allReadyMove) and len(tablEntTeam[actTurn.team]) > 5 and teamMatesHpRatio > 0.3:
										nbAllies = len(actTurn.cell.getEntityOnArea(area=AREA_DONUT_3,team=actTurn.team,wanted=ALLIES,lineOfSight=False,lifeUnderPurcentage=99999,dead=False,effect=[None],ignoreInvoc = True, directTarget=False,ignoreAspiration = None,fromCell=actTurn.cell))
										nbAliveAllies = 0
										for ent in tablEntTeam[actTurn.team]:
											if type(ent.char) not in [invoc, depl] and ent.hp > 0:
												nbAliveAllies += 1
										if nbAllies < nbAliveAllies/2:
											potCell = actTurn.getCellToMove(cellToMove=findCell(2, [2,3][bigMap], tablAllCells),lastCell=actTurnCell)
											if potCell != None:
												optionChoice,choiceToMove,optionChoisen = OPTION_MOVE, potCell, True

									if not(optionChoisen):
										probaAtkWeap = [0,0,0,0,0,0,0,0]
										probaHealWeap = [0,0,0,0,0,0,0,0]
										probaReaSkill = [100,220,200,100,200,100,100,100]
										probaIndirectReaSkill = [30,150,100,30,150,80,30,30]
										probaAtkSkill = [100,65,70,50,50,100,100,100]
										probaIndirectAtkSkill = [50,40,40,30,40,120,100,100]
										probaHealSkill = [50,100,70,30,130,50,30,30]
										probaBoost = [50,130,50,30,70,50,30,50]
										probaMalus = [50,40,100,30,50,50,50,50]
										probaArmor = [50,100,150,30,70,50,50,35]
										probaInvoc = [80,80,80,80,80,80,80,80]
										probaDepl = [70,70,70,70,70,70,70,70]

										if actTurn.isNpc("Shehisa"):
											probaInvoc[choisenIA] = 200
										elif actTurn.isNpc("Lena") and actTurn.skills[0].id == lenaExSkill1.id:
											probaBoost[choisenIA] = 500

										tablSetProb = [[probaAtkWeap,probaHealWeap],[probaAtkSkill,probaIndirectAtkSkill],[probaHealSkill,probaReaSkill,probaIndirectReaSkill],[probaArmor],[probaBoost],[probaMalus],[probaInvoc,probaDepl]]
										tablCharSet = [actTurn.char.charSettings["weaponUse"],actTurn.char.charSettings["dmgSkillUse"],actTurn.char.charSettings["healSkillUse"],actTurn.char.charSettings["armorSkillUse"],actTurn.char.charSettings["buffSkillUse"],actTurn.char.charSettings["debuffSkillUse"],actTurn.char.charSettings["summonSkillUse"],]

										for cmpt1 in range(len(tablCharSet)):
											for cmpt2 in range(len(tablSetProb[cmpt1])): tablSetProb[cmpt1][cmpt2][choisenIA] = int(tablSetProb[cmpt1][cmpt2][choisenIA] * [0.5,1,1.5][tablCharSet[cmpt1]])

										# There is a ennemi casting ?
										ennemiCast, targetCast = False, None
										for ent in tablEntTeam[int(not(actTurn.team))]:
											for eff in ent.effects:
												if eff.effects.replica != None:
													skillFinded = findSkill(eff.effects.replica)
													if (skillFinded.effectOnSelf == None and skillFinded.type in [TYPE_DAMAGE]) or (skillFinded.effectOnSelf != None and findEffect(skillFinded.effectOnSelf).replica == None) and skillFinded.area != AREA_MONO:
														ennemiCast, targetCast = True, eff.replicaTarget

										if ennemiCast:logs += "\nA ennemi is casting !"; probaArmor[actTurn.IA] = int(probaArmor[choisenIA]*(2+int(targetCast==actTurn)))
										if alliesdying and not(ennemiesdying):probaHealSkill[choisenIA] = int(probaHealSkill[choisenIA] * 1.25)
										if actTurn.isNpc("Luna ex.") and len(atRange) > 0: probaAtkSkill[actTurn.IA] = probaAtkSkill[actTurn.IA] * 2
										elif actTurn.isNpc("Lio"):
											downedAllies = 0
											for ent in tablEntTeam[actTurn.team]:
												if ent.hp <= 0: downedAllies += 1
											probaAtkSkill[choisenIA] = probaAtkSkill[choisenIA] * (1 + downedAllies/7)

										# Do we have a big buff ? If yes, maybe we should consider using skills if we can't attack
										bigbuffy, dmgUpValue = actTurn.allStats()[actTurn.char.weapon.use] >= actTurn.baseStats[actTurn.char.weapon.use] * 1.1, 0
										if not(bigbuffy):
											for a in actTurn.effects:
												if a.effects.id in [dmgUp.id, lenaExSkill5e.id]: dmgUpValue += a.effects.power
													
										bigbuffy = dmgUpValue >= max(5,actTurn.level / 5)

										qCast = False
										healSkill,atkSkill,reaSkill,indirectReaSkill,indirectAtkSkill,boostSkill,malusSkill,armorSkill,invocSkill,deplSkills = [],[],[],[],[],[],[],[],[],[]

										if not(actTurn.silent):
											for indx, skillToSee in enumerate(actTurn.skills): # Catégorisation des sorts
												skillToSee:classes.skill = copy.deepcopy(skillToSee)
												tablToLook = []

												if actTurn.cooldowns[indx] == 0 and type(skillToSee) == classes.skill and skillToSee.id not in ["lb", quickCast.id]:
													if skillToSee.become == None:
														if not(skillToSee.replay and hadReplayed) and not(skillToSee.id == selfMemoria.id and actTurn.isNpc(memoria.name)): tablToLook = [skillToSee]
													else:
														tablToLook, tablEffId = [], []
														for eff in actTurn.effects: tablEffId.append(eff.effects.id)

														for skillToSee2 in skillToSee.become:
															fullValid = not(skillToSee2.replay and hadReplayed)
															if fullValid and skillToSee2.needEffect != None:
																for bidule in skillToSee2.needEffect:
																	if bidule.id not in tablEffId:
																		fullValid = False
																		break
																	elif skillToSee2.effectFinisher:
																		for eff in actTurn.effects:
																			if bidule.id == eff.effects.id and eff.effects.turnInit > 0 and eff.turnLeft == 1:
																				atRange = actTurn.cell.getEntityOnArea(area=skillToSee2.range,fromCell=actTurn.cell,team=actTurn.team,wanted=ENEMIES)
																				if len(atRange) > 0:
																					atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
																					ennemi = atRange[0]
																					optionChoice = OPTION_SKILL
																					skillToUse: classes.skill = skillToSee2
																					optionChoisen = True
																					break

																		if not(optionChoisen):
																			fullValid = False
																			break
															if fullValid and skillToSee2.rejectEffect != None:
																for bidule in skillToSee2.rejectEffect:
																	if bidule.id in tablEffId: fullValid = False ; break
															if skillToSee2.id in [clemTmpSkill3.id,clemTmpSkill1.id,clemTmpSkill2.id,clemTmpSkill4.id,clemTmpSkill5.id] and skillToSee2.jaugeEff == None and fullValid:
																for eff in actTurn.effects:
																	if eff.effects.id == clemTmpBloodJauge.id and eff.value >= 35: fullValid = False; break
															if fullValid and skillToSee2.rejectJaugeVal != None:
																try: fullValid = teamJaugeDict[actTurn.team][actTurn].effects.id == skillToSee2.rejectJaugeVal[0].id and teamJaugeDict[actTurn.team][actTurn].value < skillToSee2.rejectJaugeVal[1]
																except KeyError: fullValid = False
															if fullValid: tablToLook.append(skillToSee2)

													cpTablToLook = tablToLook[:]
													for tmpSkill in cpTablToLook:
														jaugeConds = tmpSkill.jaugeEff != None
														if jaugeConds:
															try: jaugeConds = teamJaugeDict[actTurn.team][actTurn].effects.id == tmpSkill.jaugeEff.id and teamJaugeDict[actTurn.team][actTurn].value >= tmpSkill.minJaugeValue
															except KeyError: jaugeConds = tmpSkill.minJaugeValue == 0

															if not(jaugeConds):
																try: tablToLook.remove(tmpSkill)
																except: pass

													for skillToSee in tablToLook:
														skillToSee: classes.skill = skillToSee
														raisable, jaugeValue = actTurn.cell.getEntityOnArea(area=[skillToSee.range,skillToSee.area][skillToSee.range == AREA_MONO],fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,dead=True), 0
														if skillToSee.jaugeEff != None:
															try: 
																if teamJaugeDict[actTurn.team][actTurn].effects.id == skillToSee.jaugeEff.id: jaugeValue = teamJaugeDict[actTurn.team][actTurn].value
															except KeyError: pass

														if skillToSee.type in friendlyTypes+hostileTypes:
															if skillToSee.range == AREA_MONO: tablAtRangeTargets, posTarget = [actTurn], actTurn
															else:
																tablAtRangeTargets = actTurn.cell.getEntityOnArea(area=skillToSee.range,team=actTurn.team,wanted=[ENEMIES,ALLIES][skillToSee.type in friendlyTypes],effect=skillToSee.effects,fromCell=actTurn.cell,directTarget=skillToSee.type in hostileTypes,lifeUnderPurcentage=[[75,90][skillToSee.hpCost > 0],99999][skillToSee.type in hostileTypes],dead=skillToSee.type == TYPE_RESURECTION)
																if skillToSee.type in hostileTypes: tablAtRangeTargets.sort(key=lambda ballerine: actTurn.getAggroValue(ballerine),reverse=True)
																elif skillToSee.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_ARMOR]: tablAtRangeTargets.sort(key=lambda ballerine: getHealAggro(actTurn,ballerine,skillToSee,armor=skillToSee.type == TYPE_ARMOR),reverse=True)
																elif skillToSee.type in [TYPE_BOOST]: tablAtRangeTargets.sort(key=lambda ballerine: getBuffAggro(actTurn,ballerine,findEffect(skillToSee.effects[0])),reverse=True)

																if len(tablAtRangeTargets) > 0: posTarget = tablAtRangeTargets[0]
																else: posTarget = None

															if posTarget != None:
																nbDeadAllies = 0
																if skillToSee.area == AREA_MONO: tablHotEnemiesInArea = [posTarget]
																else:
																	tablHotEnemiesInArea = posTarget.cell.getEntityOnArea(area=skillToSee.area,team=actTurn.team,wanted=[ENEMIES,ALLIES][skillToSee.type in friendlyTypes],effect=skillToSee.effects,fromCell=actTurn.cell,directTarget=False,lifeUnderPurcentage=[99,99999][skillToSee.type in hostileTypes],dead=skillToSee.type == TYPE_RESURECTION)
																	if skillToSee.id == inMemoria.id:
																		for ent in tablEntTeam[actTurn.team]:
																			if ent.hp < 0 and type(ent.char) not in [invoc,depl] or ent.isNpc("Anna","Iliana"): nbDeadAllies += 1
																	elif skillToSee.id in [lizLB.id,plumRem.id,fairyLiberation.id]:
																		nbEff = 0
																		for ent in tablHotEnemiesInArea:
																			for eff in ent.effects:
																				if eff.effects.id in {lizLB.id:[charming.id,charmingHalf.id],plumRem.id:[plumRemEff.id],fairyLiberation.id:[estial.id]}[skillToSee.id]:
																					nbEff += [1,0.5][eff.effects.id==charmingHalf.id]
																		skillToSee.iaPow = {lizLB.id:lizLB.effects[0],plumRem.id:plumRemEff,fairyLiberation.id:fairyLiberation.effects[0]}[skillToSee.id].iaPow*nbEff
																		if skillToSee.iaPow > 0:
																			skillToSee.iaPow += (skillToSee.cooldown*5)+(skillToSee.ultimate * 15)
																nbHotTargetsInArea = len(tablHotEnemiesInArea) + [0,nbDeadAllies][nbDeadAllies>1]

																if nbHotTargetsInArea >= skillToSee.minTargetRequired:
																	if nbHotTargetsInArea == 1 and skillToSee.area!=AREA_MONO: iaPow = skillToSee.iaPow * 0.50
																	else: iaPow = skillToSee.iaPow * nbHotTargetsInArea
																	if skillToSee.jaugeEff != None:
																		try:
																			if teamJaugeDict[actTurn.team][actTurn].effects.id == skillToSee.jaugeEff.id and teamJaugeDict[actTurn.team][actTurn].value >= 85: iaPow = iaPow + 150
																			elif teamJaugeDict[actTurn.team][actTurn].effects.id == skillToSee.jaugeEff.id and teamJaugeDict[actTurn.team][actTurn].value >= 35: iaPow = iaPow + 50
																		except: pass
																	if skillToSee.needEffect != None: iaPow = iaPow * 2
																	if skillToSee.id in importantSkills: iaPow = iaPow*3

																	maxCmpt, cmpt = iaPow//10, 1

																	if skillToSee.id in [intox.id,epidemic.id,infectFiole.id]:
																		tablCacTarget = posTarget.cell.getEntityOnArea(area=AREA_DONUT_1,team=actTurn.team,wanted=ENEMIES,effect=skillToSee.effects,ignoreInvoc = False,directTarget=False,fromCell=actTurn.cell)
																		iaPow = iaPow * (0.5+(0.5*len(tablCacTarget)))

																	if skillToSee.type == TYPE_DAMAGE:
																		while cmpt <= maxCmpt:
																			atkSkill.append(skillToSee)
																			cmpt += 1
																	elif skillToSee.type == TYPE_INDIRECT_DAMAGE:
																		while cmpt <= maxCmpt:
																			indirectAtkSkill.append(skillToSee)
																			cmpt += 1
																	elif skillToSee.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL]:
																		if skillToSee.range == AREA_MONO and skillToSee.area != skillToSee.range:
																			cmptNeedingAllies, maxHpMin, maxHpMinDict = 0, 50, {0:90,1:90,2:90,3:90,4:80,5:70,6:60,7:50}
																			try:
																				maxHpMin = maxHpMinDict[skillToSee.cooldown]
																			except KeyError:
																				pass

																			for ent in tablHotEnemiesInArea:
																				if ent.hp/ent.maxHp <= maxHpMin:
																					cmptNeedingAllies += 1

																			if cmptNeedingAllies < len(tablHotEnemiesInArea)*0.4:
																				maxCmpt = maxCmpt / 3
																		while cmpt <= maxCmpt:
																			healSkill.append(skillToSee)
																			cmpt += 1
																	elif skillToSee.type == TYPE_ARMOR:
																		while cmpt <= maxCmpt:
																			armorSkill.append(skillToSee)
																			cmpt += 1
																	elif skillToSee.type == TYPE_BOOST:
																		while cmpt <= maxCmpt:
																			boostSkill.append(skillToSee)
																			cmpt += 1
																		for effy in skillToSee.effects+[skillToSee.effectOnSelf]:
																			eff = findEffect(effy)
																			if type(eff) == classes.effect:
																				if eff.id in [defenseUp.id,justiceEnigmaEff.id]:
																					cmpt = 1
																					while cmpt <= maxCmpt:
																						armorSkill.append(skillToSee)
																						cmpt += 1
																					break
																					probaArmor[choisenIA] = int(probaArmor[choisenIA] * 1.2)
																				elif eff.id in [partage.id,healDoneBonus.id,absEff.id]:
																					cmpt = 1
																					while cmpt <= maxCmpt:
																						healSkill.append(skillToSee)
																						cmpt += 1
																					break
																					probaHealSkill[choisenIA] = int(probaHealSkill[choisenIA] * 1.2)
																		if skillToSee.range == skillToSee.area == AREA_MONO: probaBoost[choisenIA] = probaBoost[choisenIA]*(1.25+(0.25*int(skillToSee.ultimate)))
																	elif skillToSee.type == TYPE_MALUS:
																		while cmpt <= maxCmpt:
																			malusSkill.append(skillToSee)
																			cmpt += 1
																	elif skillToSee.type == TYPE_RESURECTION:
																		while cmpt <= maxCmpt:
																			reaSkill.append(skillToSee)
																			cmpt += 1

														else:
															if skillToSee.range == AREA_MONO:									 # If the skill is launch on self
																if skillToSee.type == TYPE_SUMMON and len(actTurn.cell.getEmptyCellsInArea(area=skillToSee.range,team=actTurn.team,fromCell=actTurn.cell))>0 and not(qCast): # Invocation
																	temp = actTurn.cell.getEmptyCellsInArea(area=skillToSee.range,team=actTurn.team)
																	for b in temp[:]:
																		if [b.x > 2, b.x < 3][actTurn.team] :
																			temp.remove(b)

																	if len(temp) > 0:
																		invocSkill.append(skillToSee)
																elif skillToSee.type == TYPE_DEPL and len(actTurn.cell.getEntityOnArea(area=skillToSee.depl.skills.area,team=actTurn.team,wanted=[ALLIES,ENEMIES][skillToSee.depl.skills.type in hostileTypes],ignoreInvoc = True, directTarget=False ,fromCell=actTurn.cell)) > 1:
																	deplSkills.append(skillToSee)

																elif skillToSee.id in ["ul",abnegation.id] and not(qCast): 
																	sumHp,sumMaxHp = 0,0
																	for b in tablEntTeam[actTurn.team]:
																		sumHp += max(0,b.hp)
																		sumMaxHp += b.maxHp
																	if sumHp / sumMaxHp <= 0.6:
																		healSkill.append(skillToSee)
																		healSkill.append(skillToSee)
																		for num in range(len(probaHealSkill)):
																			probaHealSkill[num] = probaHealSkill[num] *1.2
																	if sumHp / sumMaxHp <= 0.4:
																		healSkill.append(skillToSee)
																		healSkill.append(skillToSee)
																		for num in range(len(probaHealSkill)):
																			probaHealSkill[num] = probaHealSkill[num] *1.5

															else: # The skill is cast on others
																if skillToSee.type == TYPE_UNIQUE and not(qCast):
																	for b in [chaos]: # Boost
																		if b == skillToSee:
																			boostSkill.append(b)
																elif skillToSee.type == TYPE_SUMMON and actTurn.cell.getCellForSummon(area=skillToSee.range, team=actTurn.team, summon= findSummon(skillToSee.invocation), summoner=actTurn) != None and not(qCast):
																	invocSkill.append(skillToSee)
																	if skillToSee.ultimate:
																		probaInvoc[choisenIA] = probaInvoc[choisenIA]*2
																		invocSkill.append(skillToSee)
																		invocSkill.append(skillToSee)
																elif skillToSee.type == TYPE_DEPL:
																	deplSkills.append(skillToSee)

										if not(optionChoisen):
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

													nbToAdd = 0
													if lbSkill.area == AREA_MONO:
														ennemiNb = 0
														for ent in tablEntTeam[not(actTurn.team)]:
															if type(ent.char) not in [invoc, depl] and ent.hp > 0:
																ennemiNb += 1
														if ennemiNb <= 2:
															nbToAdd += 5
													elif len(ennemiTabl) > 0 and (not dictIsNpcVar["The Giant Enemy Spider"] and not dictIsNpcVar["[[Spamton Neo](https://deltarune.fandom.com/wiki/Spamton)]"]):
														if len(ennemiTabl[0].cell.getEntityOnArea(area=lbSkill.area,team=actTurn.team,wanted=ENEMIES,fromCell=actTurn.cell,ignoreInvoc = True)) >= [2,3][lbSkill.area==lb1AoE.area]:
															nbToAdd += 10
													elif dictIsNpcVar["The Giant Enemy Spider"] or dictIsNpcVar["[[Spamton Neo](https://deltarune.fandom.com/wiki/Spamton)]"]:
														nbToAdd += 5
														if lbSkill.area==lb1AoE.area:
															nbToAdd += 5

													cmpt, maxCmpt = 0, ((lbSkill.iaPow//10)+1)*nbToAdd
													while cmpt < maxCmpt:
														atkSkill.append(lbSkill)
														cmpt += 1

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

											probTabl, analyse = [probaReaSkill,probaIndirectReaSkill,probaAtkSkill,probaIndirectAtkSkill,probaHealSkill,probaBoost,probaMalus,probaArmor,probaDepl], [reaSkill,indirectReaSkill,atkSkill,indirectAtkSkill,healSkill,boostSkill,malusSkill,armorSkill,deplSkills]
											for cmpt in range(len(probTabl)):
												if len(analyse[cmpt]) == 0:
													probTabl[cmpt][choisenIA] = 0
												if actTurn.isNpc("Akira H.") and cmpt == 3:
													logs += "\n" + str(analyse[cmpt])

											if len(invocSkill) == 0:
												probaInvoc[choisenIA] = 0

											totalProba = probaAtkWeap[choisenIA]+probaHealWeap[choisenIA]+probaInvoc[choisenIA]

											for cmpt in range(len(probTabl)):
												totalProba += probTabl[cmpt][choisenIA]

											nbIte, optionChoice = 0, OPTION_WEAPON
											atRange = actTurn.atRange()
											nbTargetAtRange = len(atRange)

											if not(actTurn.char.weapon.priority == WEAPON_PRIORITY_NONE or (actTurn.char.weapon.id in cannotUseMainWeapon and len(actTurn.atRange()) > 0) and not(actTurn.char.slowMove and allReadyMove)):
												if actTurn.char.weapon.target == ENEMIES:
													if nbTargetAtRange > 0:
														atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
														optionChoice, ennemi = OPTION_WEAPON,atRange[0]

													else:
														optionChoice,choiceToMove = OPTION_MOVE, actTurn.getCellToMove(lastCell=actTurnCell)
														if choiceToMove == None:
															optionChoice=OPTION_SKIP

												else:
													if nbTargetAtRange > 0:
														optionChoice,ennemi = OPTION_WEAPON,getHealTarget(actTurn,atRange,actTurn.char.weapon)
													else:
														optionChoice,choiceToMove = OPTION_MOVE, actTurn.getCellToMove(lastCell=actTurnCell)
														if choiceToMove == None:
															optionChoice=OPTION_SKIP
											else:
												optionChoice,choiceToMove = OPTION_MOVE, actTurn.getCellToMove(lastCell=actTurnCell)
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
														for indx, skillToSee in enumerate(actTurn.skills):
															if type(skillToSee) == classes.skill and actTurn.cooldowns[indx] == 0 and type(ennemi) == entity and (skillToSee.tpCac or skillToSee.tpBehind) and skillToSee.type in hostileTypes:
																atRange2 = actTurn.cell.getEntityOnArea(area=skillToSee.range,fromCell=actTurn.cell,team=actTurn.team,wanted=ENEMIES,lineOfSight=True)
																if len(atRange2)>0:
																	try:
																		atRange2.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
																		skillToUse: classes.skill = copy.deepcopy(skillToSee)
																		optionChoice, ennemi, compromis = OPTION_SKILL, atRange2[0], True
																	except:
																		print_exc()
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
													randomSkill: classes.skill = randRep(invocSkill)

													optionChoice = OPTION_SKILL
													skillToUse: classes.skill = randomSkill
													optionChoisen = True
												elif not(optionChoisen):
													probaRoll -= probaInvoc[choisenIA]

												if probaRoll <= probaReaSkill[choisenIA] and probaReaSkill[choisenIA] > 0 and not(optionChoisen): # Résurection
													logs += "\nSelected option : Resurection Skill"
													skillToUse: classes.skill = randRep(reaSkill)
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
																skillToUse: classes.skill = indirectReaSkill[random.randint(0,len(reaSkill)-1)]
															else:
																skillToUse: classes.skill = indirectReaSkill[0]
															ennemi = a
															optionChoisen = True
															break

													optionChoisen = True
												elif not(optionChoisen):
													probaRoll -= probTabl[1][choisenIA]

												if probaRoll <= probTabl[2][choisenIA] and probTabl[2][choisenIA] > 0 and not(optionChoisen): # Sort de dégâts
													logs += "\nSelected option : Damage skill"
													randomSkill: classes.skill = randRep(atkSkill)

													if randomSkill.range != AREA_MONO:
														atRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,fromCell=actTurn.cell,team=actTurn.team,wanted=ENEMIES,lineOfSight = True,effect=randomSkill.effects,ignoreInvoc = (randomSkill.effectOnSelf == None or (randomSkill.effectOnSelf != None and findEffect(randomSkill.effectOnSelf).replica != None)))
														atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)

														if len(atRange) > 0:
															optionChoice = OPTION_SKILL
															skillToUse: classes.skill = randomSkill
															ennemi = atRange[0]

													else:
														optionChoice = OPTION_SKILL
														skillToUse: classes.skill = randomSkill
														ennemi = actTurn

													optionChoisen=True
												elif not(optionChoisen):
													probaRoll -= probTabl[2][choisenIA]

												if probaRoll <= probTabl[3][choisenIA] and probTabl[3][choisenIA] > 0 and not(optionChoisen): # Dégâts indirects
													logs += "\nSelected option : Indirect damage skill"
													if len(indirectAtkSkill) >= 1:
														randomSkill: classes.skill = randRep(indirectAtkSkill)
														atRange = actTurn.cell.getEntityOnArea(area=[randomSkill.range,randomSkill.area][randomSkill.range == AREA_MONO],team=actTurn.team,fromCell=actTurn.cell,wanted=ENEMIES,lineOfSight=randomSkill.range != AREA_MONO)
														if len(atRange) <= 0:
															logs += "\nNo target at range finded w/ {0}, retrying...".format(randomSkill.name)
															indirectAtkSkill.remove(randomSkill)
														else:
															if randomSkill.range != AREA_MONO:
																atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)
																optionChoice, skillToUse, ennemi = OPTION_SKILL, randomSkill, atRange[0]
															else:
																optionChoice, skillToUse, ennemi = OPTION_SKILL, randomSkill, actTurn
															optionChoisen=True
													else:
														logs += "\n"+str(indirectAtkSkill)
														probTabl[3][choisenIA] = 0
												elif not(optionChoisen):
													probaRoll -= probTabl[3][choisenIA]

												if probaRoll <= probTabl[4][choisenIA] and probTabl[4][choisenIA] > 0 and not(optionChoisen): # Heal
													logs += "\nSelected option : Healing skill"
													randomSkill: classes.skill = randRep(healSkill)

													if randomSkill.range != AREA_MONO:
														if randomSkill.id != vampirisme.id:
															tablAtRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,fromCell=actTurn.cell,wanted=ALLIES,lifeUnderPurcentage=90,effect=randomSkill.effects)
														else:
															tablAtRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,fromCell=actTurn.cell,wanted=ALLIES,lifeUnderPurcentage=90,effect=randomSkill.effects,ignoreAspiration=[ALTRUISTE,PROTECTEUR,PREVOYANT,IDOLE])
												
														if len(tablAtRange) > 0:
															optionChoice = OPTION_SKILL
															skillToUse: classes.skill = randomSkill
															ennemi = getHealTarget(actTurn,tablAtRange,skillToUse)

													else:
														if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,wanted=ALLIES,fromCell=actTurn.cell,effect=randomSkill.effects,directTarget=False)) > 0 or (randomSkill == trans and actTurn.char.aspiration in [ALTRUISTE,IDOLE]):
															optionChoice = OPTION_SKILL
															skillToUse: classes.skill = randomSkill
															ennemi = actTurn
													
													optionChoisen = True
												elif not(optionChoisen):
													probaRoll -= probTabl[4][choisenIA]

												if probaRoll <= probTabl[5][choisenIA] and probTabl[5][choisenIA] > 0 and not(optionChoisen): # Boost
													logs += "\nSelected option : Buff skill"
													randomSkill: classes.skill = randRep(boostSkill)

													if randomSkill.range != AREA_MONO: # Targeted Boost Spell
														atRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,effect=randomSkill.effects,ignoreInvoc = True)
														atRange.sort(key=lambda ballerine:getBuffAggro(actTurn,ballerine,findEffect(randomSkill.effects[0])))
														optionChoice = OPTION_SKILL
														skillToUse: classes.skill = randomSkill
														try:
															ennemi = atRange[0]
														except:
															ennemi = actTurn

													else:
														if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,effect=randomSkill.effects,directTarget=False)) > 0:
															optionChoice = OPTION_SKILL
															skillToUse: classes.skill = randomSkill
															ennemi = actTurn

													optionChoisen = True
												elif not(optionChoisen):
													probaRoll -= probTabl[5][choisenIA]

												if probaRoll <= probTabl[6][choisenIA] and probTabl[6][choisenIA] > 0 and not(optionChoisen): # Malus
													logs += "\nSelected option : Debuff skill"
													randomSkill: classes.skill = randRep(malusSkill[0])

													if randomSkill.range != AREA_MONO:
														atRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,fromCell=actTurn.cell,team=actTurn.team,wanted=ENEMIES,lineOfSight = True,effect=randomSkill.effects,ignoreInvoc = (randomSkill.effectOnSelf == None or (randomSkill.effectOnSelf != None and findEffect(randomSkill.effectOnSelf).replica != None)))
														atRange.sort(key=lambda ent:actTurn.getAggroValue(ent),reverse=True)

														optionChoice = OPTION_SKILL
														skillToUse: classes.skill = randomSkill
														try:
															ennemi = atRange[0]
														except:
															logs += "\nError : No valid target find"
															optionChoice = OPTION_SKIP

													else:
														if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,fromCell=actTurn.cell,wanted=ENEMIES,effect=randomSkill.effects,directTarget=False)) > 0:
															optionChoice = OPTION_SKILL
															skillToUse: classes.skill = randomSkill
															ennemi = actTurn

													optionChoisen=True
												elif not(optionChoisen):
													probaRoll -= probTabl[6][choisenIA]

												if probaRoll <= probTabl[7][choisenIA] and probTabl[7][choisenIA] > 0 and not(optionChoisen): # Armure
													logs += "\nSelected option : Armor skill"
													randomSkill: classes.skill = randRep(armorSkill)

													if randomSkill.range != AREA_MONO:
														if randomSkill.id != convert.id:
															tablAtRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,effect=randomSkill.effects)
														else:
															tablAtRange = actTurn.cell.getEntityOnArea(area=randomSkill.range,team=actTurn.team,wanted=ALLIES,fromCell=actTurn.cell,effect=randomSkill.effects,ignoreAspiration=[ALTRUISTE,PREVOYANT,PROTECTEUR,IDOLE])

														optionChoice = OPTION_SKILL
														skillToUse: classes.skill = randomSkill
														ennemi = getHealTarget(actTurn,tablAtRange,skillToUse,True)

													else:
														if len(actTurn.cell.getEntityOnArea(area=randomSkill.area,team=actTurn.team,fromCell=actTurn.cell,wanted=ALLIES,effect=randomSkill.effects,directTarget=False)) > 0:
															optionChoice = OPTION_SKILL
															skillToUse: classes.skill = randomSkill
															ennemi = actTurn
													
													optionChoisen = True
												elif not(optionChoisen):
													probaRoll -= probTabl[7][choisenIA]

												if probaRoll <= probaDepl[choisenIA] and probaDepl[choisenIA] > 0 and not(optionChoisen): # Déployable
													logs += "\nSelected option : Depl skill"
													randomSkill: classes.skill = randRep(deplSkills)

													optionChoice = OPTION_SKILL
													skillToUse: classes.skill = randomSkill
													optionChoisen = True

													if randomSkill.range == AREA_MONO:
														ennemi = actTurn.cell
													else:
														tablCells = actTurn.cell.getArea(area=randomSkill.range,team=actTurn.team,fromCell=actTurn.cell)
														for celly in tablCells[:]:
															if celly.depl != None:
																tablCells.remove(celly)
														tablCells.sort(key=lambda ballerine: len(ballerine.getEntityOnArea(area=randomSkill.depl.skills.area,team=actTurn.team,wanted=[ALLIES,ENEMIES][randomSkill.depl.skills.type in hostileTypes], ignoreInvoc = True, directTarget=False, fromCell= ballerine))+0.5*int(ballerine.on != None and ballerine.on.team == [actTurn.team, not(actTurn.team)][randomSkill.depl.skills.type in hostileTypes]),reverse=True)
														ennemi = tablCells[0]

												elif not(optionChoisen):
													probaRoll -= probaDepl[choisenIA]

												if probaRoll == -1 and probaAtkWeap[choisenIA] == probaHealWeap[choisenIA] == 0 and actTurn.char.weapon.emoji != '<:noneWeap:917311409585537075>' and not(optionChoisen):	 # Can't use anything
													logs += "\nNo target at range. Trying to move"
													optionChoice,choiceToMove = OPTION_MOVE, actTurn.getCellToMove(lastCell=actTurnCell)
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
								if skilly.id != lenaInkStrike_2.id :
									if onReplica.replicaTarget == None:
										if skilly.range == AREA_MONO:
											onReplica.replicaTarget = actTurn
										else:
											tablAtRangeTargets = actTurn.cell.getEntityOnArea(area=skilly.range,team=actTurn.team,wanted=[ENEMIES,ALLIES][skilly.type in friendlyTypes],effect=skilly.effects,fromCell=actTurn.cell,directTarget=skilly.type in hostileTypes,lifeUnderPurcentage=[90,99999][skilly.type in hostileTypes],dead=skilly.type == TYPE_RESURECTION)
											if len(tablAtRangeTargets) > 0:
												if skilly.type in hostileTypes:
													tablAtRangeTargets.sort(key=lambda ballerine: actTurn.getAggroValue(ballerine),reverse=True)
												elif skilly.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_ARMOR]:
													tablAtRangeTargets.sort(key=lambda ballerine: getHealAggro(actTurn,ballerine,actSkill,armor=actSkill.type == TYPE_ARMOR),reverse=True)
												elif skilly.type in [TYPE_BOOST]:
													tablAtRangeTargets.sort(key=lambda ballerine: getBuffAggro(actTurn,ballerine,findEffect(actSkill.effects[0])),reverse=True)
												onReplica.replicaTarget = tablAtRangeTargets[0]
											else:
												onReplica.replicaTarget = actTurn

									if onReplica.replicaTarget.hp > 0:
										optionChoice = OPTION_SKILL
										skillToUse: classes.skill = skilly
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
											skillToUse: classes.skill = skilly
											ennemi = atRange[0]
										else:
											optionChoice = OPTION_SKIP

								else:
									optionChoice = OPTION_SKILL
									skillToUse: classes.skill = skilly
									ennemi = actTurn
							lunaUsedQuickFight, lunaQFEff = "", None

							if not(actTurn.char.canMove) and optionChoice == OPTION_MOVE:
								optionChoice = OPTION_SKIP

							if optionChoice == OPTION_WEAPON: #Option : Weapon
								for eff in actTurn.effects:
									if eff.effects.id == lunaQuickFightEff.id:
										lunaQFEff = eff
										break

								if actTurn.char.weapon.say != "":
									tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,randRep(actTurn.char.weapon.say))
								if actTurn.char.weapon.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]: # Agressive Weapon
									logs += "\n{0} is attacking {1} with their weapon\n".format(actTurn.char.name,ennemi.char.name)
									cmpt = 0
									while cmpt < iteration:
										isAlive = ennemi.hp > 0
										if not(isAlive) :
											break
										if cmpt == 0:
											if actTurn.char.weapon.message == None:
												tempTurnMsg += f"\n__{actTurn.char.name} attaque {ennemi.char.name} :__\n"
											else:
												tempTurnMsg += "\n__"+actTurn.char.weapon.message.format(actTurn.char.name,ennemi.char.name)+"__\n"
										else:
											tempTurnMsg += "\n"
										power = actTurn.char.weapon.power

										if actTurn.weaponEffect([eclataDash.id, eclataDash.id+"+"]) and actTurn.cell.distance(ennemi.cell) > 1:
											tempTurnMsg += actTurn.tpCac(ennemi)
											if actTurnweaponEffect(eclataDash.id+"+") and not(hadReplayed): replay = True

										funnyTempVarName, deathCount = actTurn.attack(target=ennemi,value=power,icon=actTurn.char.weapon.emoji,area=actTurn.char.weapon.area,use=actTurn.char.weapon.use,onArmor=actTurn.char.weapon.onArmor,skillUsed=actTurn.char.weapon,effectOnHit=actTurn.char.weapon.effectOnUse)
										logs+= funnyTempVarName
										tempTurnMsg += funnyTempVarName
										cmpt += 1

									if actTurn.char.weapon.power > 0:
										for eff in actTurn.effects:
											if eff.effects.id in [propagEff.id,propagDelEff.id]:
												try:
													if teamJaugeDict[eff.caster.team][eff.caster].effects.id == healerGlare.jaugeEff.id and teamJaugeDict[eff.caster.team][eff.caster].value > 35:
														teamJaugeDict[eff.caster.team][eff.caster].value -= 35
														ballerine = groupAddEffect(caster=actTurn, target=ennemi, area=ennemi, effect=eff.effects.callOnTrigger,skillIcon=eff.icon)
														tempTurnMsg += ballerine
														logs += ballerine
												except KeyError:
													pass
											elif eff.effects.id in [convictionVigilantEff.id,convicProEff.id,convictEnchtEff.id,convictTetEff.id]:
												ballerine = eff.triggerStartOfTurn(danger,decate=True)
												logs += ballerine
												tempTurnMsg += ballerine

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
										funnyTempVarName = add_effect(actTurn,ennemi,findEffect(actTurn.char.weapon.effectOnUse),danger=danger,skillIcon=actTurn.char.weapon.emoji)
										
										logs+= funnyTempVarName
										tempTurnMsg += funnyTempVarName

										ennemi.refreshEffects()

								for eff in actTurn.effects:
									if eff.trigger == TRIGGER_WEAPON_USE:
										funnyTempVarName = eff.triggerStartOfTurn(danger)
										tempTurnMsg += funnyTempVarName
										logs += funnyTempVarName
									elif eff.effects.id == toxicureEff.id:
										tempMsg = actTurn.heal(ennemi, icon=eff.icon, statUse=None, power=eff.value, effName=eff.effects.name, danger=danger, mono=True, direct=False)
										tempTurnMsg, logs = tempTurnMsg+tempMsg[0], logs+tempMsg[0]
										eff.decate(value=eff.value+1)

								if actTurn.isNpc("Iliana prê."):
									funnyTempVarName, useless = actTurn.heal(actTurn, actTurn.skills[0].effects[0].emoji[0][0], actTurn.skills[0].effects[0].stat, actTurn.skills[0].effects[0].power*1.25, danger=danger, mono = True, useActionStats = ACT_HEAL, direct=False)
									tempTurnMsg += funnyTempVarName
									logs += funnyTempVarName

								try:
									actTurn.stats.actionUsed[tour].append(actTurn.char.weapon.name)
								except KeyError:
									actTurn.stats.actionUsed[tour] = [actTurn.char.weapon.name]
							elif optionChoice == OPTION_MOVE: #Option : Déplacement
								logs += "\n{0} is moving".format(actTurn.char.name)
								temp = actTurn.cell

								tmpMsg = actTurn.move(cellToMove=choiceToMove)
								tempTurnMsg+= "\n"+actTurn.char.name+" se déplace" + ["\n",""][type(actTurn.char) == classes.invoc and len(tmpMsg) == 0]
								logs += "\n{0} have been moved from {1}:{2} to {3}:{4}".format(actTurn.char.name,temp.x,temp.y,choiceToMove.x,choiceToMove.y)
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
									if eff.effects.id in [quickCastEff.id,clemExBloodDemonEff.id]:
										qCast = True
									elif eff.effects.id == lunaQuickFightEff.id:
										lunaQFEff = eff
									elif skillToUse.id in useElemEffId+elemArrowId+elemRuneId and eff.effects.id in [tablElemEff[actTurn.char.element].id,tablElemEff[ELEMENT_UNIVERSALIS].id]:
										eff.decate(turn=99)
										useEffElem += 1
										needRefresh = True
									elif eff.effects.id in [nightCalEff.id, lightCalEff.id]:
										if skillToUse.group == [SKILL_GROUP_DEMON, SKILL_GROUP_HOLY][eff.effects.id == lightCalEff.id]:
											skillToUse.power, skillToUse.maxPower = skillToUse.power*(100+eff.effects.power)/100, skillToUse.maxPower*(100+eff.effects.power)/100
											if skillToUse.effPowerPurcent == None:
												skillToUse.effPowerPurcent = 100
											skillToUse.effPowerPurcent = int(skillToUse.effPowerPurcent*(100+eff.effects.power)/100)

								if needRefresh: actTurn.refreshEffects()

								if skillToUse.id in useElemEffId+elemArrowId+elemRuneId:
									skillToUse: classes.skill = copy.deepcopy(skillToUse)
									skillToUse.name = skillToUse.name + " +{0}".format(useEffElem)

								if qCast and skillToUse.effectOnSelf != None and findEffect(skillToUse.effectOnSelf).replica != None:
									skillToUse: classes.skill = copy.deepcopy(findSkill(findEffect(skillToUse.effectOnSelf).replica))

								if skillToUse.effectOnSelf != None and findEffect(skillToUse.effectOnSelf).replica != None and actTurn.auto:
									for indx, tmpSkill in enumerate(actTurn.skills):
										if type(tmpSkill) == skill and actTurn.cooldowns[indx] == 0 and tmpSkill.id == quickCast.id:
											lastSkillToUse = skillToUse
											skillToUse: classes.skill = copy.deepcopy(tmpSkill)
											skillToUse.effects[0].replica = findSkill(findEffect(lastSkillToUse.effectOnSelf).replica)
											ennemi = actTurn
											break

								if skillToUse.needEffect != None and skillToUse.consumeNeededEffects and not skillToUse.effectFinisher:
									for needed in skillToUse.needEffect:
										for eff in actTurn.effects:
											if needed.id == eff.effects.id and needed.id not in [iliTmpSkill1_renfort.id]: eff.decate(turn=99); break
									actTurn.refreshEffects()

								try: logs += "\n\n{0} is using {1} on {2}\n".format(actTurn.char.name,skillToUse.name,ennemi.char.name)
								except: logs += "\n\nError on writing into the logs"
								if skillToUse.say != "": tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,randRep(skillToUse.say))

								# Say Ultimate
								if actTurn.char.says.ultimate != None and skillToUse.ultimate and not(skillToUse.effectOnSelf != None and findEffect(skillToUse.effectOnSelf).replica != None and skillToUse.power == 0 and skillToUse.effects == [None]) and skillToUse.affSkillMsg:
									try: tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,randRep(actTurn.char.says.ultimate).format(target=ennemi.char.name,caster=actTurn.char.name,skill=skillToUse.name))
									except: tempTurnMsg += "\n__Error with the ultimate message.__ See logs for more informations"; logs += "\n"+format_exc()

								if (skillToUse.ultimate and not(skillToUse.effectOnSelf != None and findEffect(skillToUse.effectOnSelf).replica != None and skillToUse.power == 0 and skillToUse.effects == [None])):
									tmpChip = getChip("Overpower")
									for indx, tmpChipId in enumerate(actTurn.char.equippedChips):
										if tmpChipId == tmpChip.id and actTurn.chipAddInfo[indx]:
											skillToUse.power, skillToUse.effPowerPurcent, skillToUse.hpCost, actTurn.chipAddInfo[indx], skillToUse.emoji = skillToUse.power*(1+(actTurn.char.chipInventory[tmpChipId].power/100)), int(skillToUse.effPowerPurcent*(1+(actTurn.char.chipInventory[tmpChipId].power/100))), skillToUse.hpCost+50, 0, skillToUse.emoji+tmpChip.emoji
											skillToUse.maxPower = skillToUse.maxPower*(1+(actTurn.char.chipInventory[tmpChipId].power/100))
								if skillToUse.ultimate and actTurn.char.aspiration == MAGE: mageMagBuff = classes.effect("Mage","magMagBuff",magie=actTurn.baseStats[MAGIE]*0.2,turnInit=3,emoji=aspiEmoji[MAGE],silent=True); add_effect(actTurn, actTurn, mageMagBuff)

								# Say Limite Break
								if actTurn.char.says.limiteBreak != None and skillToUse.id == trans.id:
									try: tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,actTurn.char.says.limiteBreak.format(target=ennemi.char.name,caster=actTurn.char.name,skill=skillToUse.name))
									except: tempTurnMsg += "\n__Error with the Limite Break message.__ See logs for more informations";  logs += "\n"+format_exc()

								# Skill base message
								if skillToUse.affSkillMsg : tempTurnMsg += f"\n__{actTurn.char.name} utilise {skillToUse.name} :__\n"
								else: tempTurnMsg += "\n"

								if skillToUse.id in arcaneSkillsId:
									for eff in actTurn.effects:
										if eff.effects.id == rubyArcaneEff.id: skillToUse.power = skillToUse.power * (100+eff.effects.power)/100; eff.decate(value=1)
										elif eff.effects.id == quartzArcaneEff.id: skillToUse.cooldown -= eff.effects.power; eff.decate(value=1)
										elif eff.effects.id in [obsiArcaneEff.id, saphirArcEff.id]: skillToUse.effects.append(eff.effects.callOnTrigger); eff.decate(value=1)
										elif eff.effects.id in [amethysArcaneEff.id, topazArcEff.id, emeraudeArcEff.id]: skillToUse.effectAroundCaster = [TYPE_BOOST,AREA_MONO,eff.effects.callOnTrigger]; eff.decate(value=1)
								# Set the cooldown
								for cmpt, tmpSkill in enumerate(actTurn.skills):
									if type(tmpSkill) == skill:
										if skillToUse.id == tmpSkill.id:
											actTurn.cooldowns[cmpt] = skillToUse.cooldown
										if skillToUse.id == "lb":
											LBBars[actTurn.team][1] = 0
											if tmpSkill.ultimate and actTurn.cooldowns[cmpt] < 2: actTurn.cooldowns[cmpt] = 2

								# Share cooldown
								if skillToUse.shareCooldown:
									for ent in tablEntTeam[actTurn.team]:
											for indx, tmpSkill in enumerate(ent.skills):
												if type(tmpSkill) == skill and tmpSkill.id == skillToUse.id: ent.cooldowns[indx] = skillToUse.cooldown

								if skillToUse.effectOnSelf != None and skillToUse.effBeforePow:
									effect = findEffect(skillToUse.effectOnSelf)
									tempTurnMsg = [tempTurnMsg[:-1],tempTurnMsg][skillToUse.type != TYPE_HEAL] + add_effect(actTurn,actTurn,effect,effPowerPurcent=skillToUse.effPowerPurcent,skillIcon = skillToUse.emoji)
									logs += "\n{0} gave the {1} effect at {2} for {3} turn(s)".format(actTurn.char.name,effect.name,ennemi.char.name,effect.turnInit)

								if skillToUse.effects != [None] and skillToUse.effBeforePow:
									ballerine = groupAddEffect(caster=actTurn, target=ennemi, area=[skillToUse.area,AREA_MONO][skillToUse.type == TYPE_DAMAGE], effect=skillToUse.effects, skillIcon=skillToUse.emoji, actionStats=skillToUse.useActionStats, effPurcent=skillToUse.effPowerPurcent)
									tempTurnMsg = tempTurnMsg + ballerine
									logs += ballerine

								# tpCac
								if (skillToUse.tpCac or skillToUse.tpBehind) and type(ennemi) == entity:
									if actTurn.cell.distance(ennemi.cell) > 1:
										tempTurnMsg += actTurn.tpCac(ennemi,behind=skillToUse.tpBehind)
										if skillToUse.areaOnSelf:
											ennemi = actTurn

									for indx, tmpChipId in enumerate(actTurn.char.equippedChips):
										tmpChip = getChip(tmpChipId)
										if tmpChip != None:
											if tmpChip.name == "Camalataque":
												tmpEff = classes.effect(tmpChip.name,"squidAttack",HARMONIE,power=int(actTurn.char.level*actTurn.char.chipInventory[tmpChip.id].power/100),area=AREA_DONUT_1,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,emoji=tmpChip.emoji)
												tempTurnMsg += groupAddEffect(caster=actTurn, target=actTurn, area=AREA_MONO, effect=tmpEff, skillIcon=tmpChip.emoji)
											elif tmpChip.name == "Pas Piégés" and actTurn.chipAddInfo[indx] > 0:
												tmpEff = copy.deepcopy(littleTrapEff)
												tmpEff.power = actTurn.char.chipInventory[tmpChip.id].power
												tempTurnMsg += groupAddEffect(caster=actTurn, target=ennemi, area=AREA_MONO, effect=tmpEff, skillIcon=tmpChip.emoji)
												actTurn.chipAddInfo[indx] -= 1

								jaugeConsumed = 0
								if skillToUse.jaugeEff != None:
									try:
										if teamJaugeDict[actTurn.team][actTurn].effects.id == skillToUse.jaugeEff.id:
											jaugeMinValue, jaugeMaxValue = skillToUse.minJaugeValue, max(skillToUse.maxJaugeValue,skillToUse.minJaugeValue)
											jaugeConsumed = [teamJaugeDict[actTurn.team][actTurn].value,jaugeMaxValue][jaugeMaxValue<teamJaugeDict[actTurn.team][actTurn].value]
											teamJaugeDict[actTurn.team][actTurn].value -= jaugeConsumed
											jaugeRatio, lastEffPower, lastPower = jaugeConsumed / jaugeMaxValue, skillToUse.effPowerPurcent, skillToUse.power
											if skillToUse.id == tripleChoc.id:
												tc1, tc2, tc1c, tc2c = copy.deepcopy(tripleChoc_1), copy.deepcopy(tripleChoc_2), copy.deepcopy(tripleChoc_1_c), copy.deepcopy(tripleChoc_2_c)
												skillToUse.power, tc1.power, tc2.power, tc1c.replica, tc2c.replica = skillToUse.power+((skillToUse.maxPower-skillToUse.power)*jaugeRatio), tc1.power+((tc1.maxPower-tc1.power)*jaugeRatio), tc2.power+((tc2.maxPower-tc2.power)*jaugeRatio), tc1, tc2
												tc1.maxPower, tc2.maxPower, skillToUse.effectOnSelf, tc1.effectOnSelf = tc1.power, tc2.power, tc1c, tc2c
											elif skillToUse.maxJaugeValue != skillToUse.minJaugeValue and skillToUse.maxJaugeValue != 0:
												skillToUse.maxPower = skillToUse.maxPower * (skillToUse.power/skillToUse.initPower)
												skillToUse.power += (skillToUse.maxPower-skillToUse.power)*jaugeRatio

											if teamJaugeDict[actTurn.team][actTurn].effects.id == focusJauge.id:
												for ent in tablEntTeam[not(actTurn.team)]:
													for eff in ent.effects:
														if eff.effects.id == cribArrowEff.id and eff.caster.id == actTurn.id:
															eff.effects.power = int(cribArrow.effects[0].power * (1+(jaugeConsumed-cribArrow.minJaugeValue)/(100-cribArrow.minJaugeValue)))
															print(eff.effects.power)
															tempTurnMsg += eff.triggerStartOfTurn(danger,decate=True)

											skillToUse.effPowerPurcent = round((skillToUse.effPowerPurcent/2) + (skillToUse.effPowerPurcent/2*jaugeRatio))
									except KeyError: logs += "\n{0} hasn't any jauge eff"

								if skillToUse.id == plumRem.id:
									tablEntInArea = ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENEMIES,ignoreInvoc = True, directTarget=False,fromCell=actTurn.cell)
									for ent in tablEntInArea:
										nbPlume = 0
										for eff in ent.effects:
											if eff.effects.id == plumRemEff.id:
												nbPlume+=1
												eff.decate(value=99)
										if nbPlume == 0:
											tempTurnMsg += "Cela n'affecte pas {0}\n".format(ent.name)
										else:
											deepTemp = groupAddEffect(caster=actTurn, target=ent, area=AREA_MONO, effect=plumRemEff.callOnTrigger, skillIcon=skillToUse.emoji)
											temp, temp2 = actTurn.attack(target=ent, value = int(plumRemEff.power*nbPlume*1.35), icon = skillToUse.emoji, area=plumRemEff.area, accuracy=200)
											logs +="\n"+deepTemp+temp
											tempTurnMsg += ["\n",""][ent.id == tablEntInArea[0].id]+deepTemp+temp

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

								elif skillToUse.id in [triSlashdown.id,shushiSkill122.id]:
									funnyTempVarName, temp = actTurn.attack(target=ennemi,value=skillToUse.power,icon=skillToUse.emoji,area=skillToUse.area,accuracy=skillToUse.accuracy,use=skillToUse.use,onArmor=skillToUse.onArmor,useActionStats=actionStats,setAoEDamage=skillToUse.setAoEDamage,lifeSteal = skillToUse.lifeSteal,erosion = skillToUse.erosion,skillPercing = skillToUse.percing,execution=skillToUse.execution,skillUsed=skillToUse,)
									tempTurnMsg = [tempTurnMsg,tempTurnMsg[:-1]][skillToUse.area==AREA_MONO and cmpt>0 and len(funnyTempVarName.splitlines())==1] + funnyTempVarName

									for celly in [findCell(x=actTurn.cell.x + [1,-1][actTurn.team],y = actTurn.cell.y + 1,tablAllCells=tablAllCells),findCell(x=actTurn.cell.x + [1,-1][actTurn.team],y = actTurn.cell.y - 1,tablAllCells=tablAllCells)]:
										if celly != None:
											if celly.on == None:
												tablEntTeam, tablAliveInvoc, time, funnyTempVarName = actTurn.summon(inkFist, time, celly, tablAliveInvoc, ignoreLimite=True)

											funnyTempVarName, temp = actTurn.attack(target=celly.on,value=skillToUse.power,icon=inkFist.icon[actTurn.team],area=skillToUse.area,use=skillToUse.use,onArmor=skillToUse.onArmor,useActionStats=actionStats,setAoEDamage=skillToUse.setAoEDamage,lifeSteal = skillToUse.lifeSteal,erosion = skillToUse.erosion,skillPercing = skillToUse.percing,execution=skillToUse.execution,skillUsed=skillToUse)
											tempTurnMsg += "\n"+ funnyTempVarName

											if celly.on.char.__class__ == classes.invoc and celly.on.char.name.startswith("Poings d'Encre"):
												celly.on.endOfTurn(danger)

								elif skillToUse.id == gwenyExChangeSkill.id:
									ally: classes.tmpAllie = findAllie(skillToUse.name.split(" - ")[-1])
									ally = getAllieFromBuild(ally,ally.changeDict[-1])
									ally.changeLevel(level=actTurn.char.level, changeDict=False, stars=actTurn.char.stars, changeStuff=False)

									ballerine, babie = await actTurn.changeNpc(char=ally)
									tempTurnMsg += ballerine[1:]+"\n"
									logs += babie

								elif skillToUse.id == lenaInkStrike_1.id:
									spreadRange = len(ennemi.getEntityOnArea(area=lenaInkStrike_1.depl.skills.area, team=actTurn.team, wanted=ENEMIES, directTarget=False, fromCell=actTurn.cell)) > 3
									tablToLookCells = [[(0,-1),(1,0),(0,1),(-1,0)],[(0,-2),(2,0),(0,2),(-2,0),(0,0)]][spreadRange]
									for cellPos in tablToLookCells:
										tmpCell = findCell(ennemi.x+cellPos[0],ennemi.y+cellPos[1],tablAllCells)
										if tmpCell == None and spreadRange:
											tmpCell = findCell(ennemi.x+(cellPos[0]/2),ennemi.y+(cellPos[1]/2),tablAllCells)

										if tmpCell != None:
											actTurn.smnDepl(lenaInkStrike_depl1,tmpCell)
											if tmpCell.on != None:
												iconMsg = " ({0})".format(tmpCell.on.icon)
											else:
												iconMsg = ""
											tempTurnMsg += "{0} cible la cellule {1}:{2}{3}\n".format(actTurn.name,tmpCell.x,tmpCell.y,iconMsg)
									tempTurnMsg += "\n"

								elif skillToUse.id == lenaInkStrike_2.id:
									skillToUse.emoji, toReturn = ["<:lenaInkstrikeB:1226240176305733632>","<:lenaInkstrikeR:1226240195259797504>"][actTurn.team], ""
									for entDepl in deplTabl:
										if entDepl[0].name == lenaInkStrike_depl1.name and entDepl[0].summoner.id == actTurn.id and entDepl[0].leftTurnAlive > 0 and entDepl[1] != None:
											if entDepl[1].on == None:
												tablEntTeam, tablAliveInvoc, time, funnyTempVarName = actTurn.summon(inkFist, time, entDepl[1], tablAliveInvoc, ignoreLimite=True)
											toTarget = entDepl[1].on

											ballerine, temp = actTurn.attack(target=toTarget,value=skillToUse.power,icon=skillToUse.emoji,area=skillToUse.area,accuracy=skillToUse.accuracy,use=skillToUse.use,onArmor=skillToUse.onArmor,useActionStats=actionStats,setAoEDamage=skillToUse.setAoEDamage,lifeSteal = skillToUse.lifeSteal,erosion = skillToUse.erosion,skillPercing = skillToUse.percing,skillUsed=skillToUse)
											if len(ballerine) > 0:
												toReturn += ballerine+"\n"
												logs += "\n"+ballerine
												deathCount += temp

											if entDepl[1].on.char.__class__ == classes.invoc and entDepl[1].on.char.name.startswith("Poings d'Encre"):
												entDepl[1].on.endOfTurn(danger)

											entDepl[1].depl = None
											entDepl[1], entDepl[2] = None, []

									if len(toReturn) == 0:
										tempTurnMsg += "Mais rien ne se passe\n"
									else:
										tempTurnMsg += toReturn[:-1]

								elif skillToUse.id == trappedFieldMockup.id:
									surfaceArea = ennemi.getArea(area=trappedFieldMockup.depl.skills.area,team=actTurn.team,fromCell=actTurn.cell)
									for tmpCell in surfaceArea[:]:
										if tmpCell.depl != None:
											surfaceArea.remove(tmpCell)

									for cmpt in range(3):
										tmpCell = randRep(surfaceArea)
										actTurn.smnDepl(trappedFieldTrueDepl,tmpCell)
										if tmpCell.on != None:
											iconMsg = " ({0})".format(tmpCell.on.icon)
										else:
											iconMsg = ""
										tempTurnMsg += "{0} place une {4} {5} sur la cellule {1}:{2}{3}\n".format(actTurn.name,tmpCell.x,tmpCell.y,iconMsg,trappedFieldTrueDepl.icon[0], trappedFieldTrueDepl.name)
										surfaceArea.remove(tmpCell)
								
								# ======================== Any other skill ========================
								else:
									actionStats = skillToUse.useActionStats
									if skillToUse.id == trans.id:
										actionStats, entActStats = 0, actTurn.actionStats()
										for cmpt in (0,1,2,3,4):
											if entActStats[cmpt] > entActStats[actionStats]:
												skillToUse.useActionStats = cmpt
										actTurn.stats.nbLB += 1

									if skillToUse.type in [TYPE_BOOST,TYPE_ARMOR,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ] and skillToUse.effects != [None]:
										if skillToUse.id == bolide.id:
											tempTurnMsg += "{0} {1} → {0} -{2} PV\n".format(actTurn.icon,skillToUse.emoji,actTurn.hp -1)
											actTurn.stats.selfBurn += actTurn.hp -1
											actTurn.hp = 1
										elif skillToUse.id == gwenySkill3.id:
											nbHpConsummed = actTurn.hp//2
											instantDmgEff, ratio = classes.effect(skillToUse.name,"sacrInstEff",power=nbHpConsummed,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,emoji=skillToUse.emoji), 1-(nbHpConsummed/(actTurn.maxHp//2))
											tempTurnMsg += groupAddEffect(actTurn, actTurn, AREA_MONO,instantDmgEff,skillToUse.emoji)
											skillToUse.effPowerPurcent = int((100*ratio)+((1-ratio)*500))

										if TRAIT_HIGHLIGHTED in actTurn.char.trait and skillToUse.ultimate:
											skillToUse.effPowerPurcent += 10

										affectedEntities = ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES,effect=skillToUse.effects, directTarget=False,fromCell=actTurn.cell)
										ballerine = groupAddEffect(caster=actTurn, target=ennemi, area=affectedEntities, effect=skillToUse.effects, skillIcon=skillToUse.emoji, actionStats=skillToUse.useActionStats, effPurcent = skillToUse.effPowerPurcent)
										tempTurnMsg += ballerine
										logs += ballerine

										for indx, tmpChipId in enumerate(actTurn.char.equippedChips):
											tmpChip = getChip(tmpChipId)
											if tmpChip != None:
												if tmpChip.name == "Un pour tous" and skillToUse.type == TYPE_ARMOR:
													tmpEff = classes.effect("Résistance augmentée","resiUp",PURCENTAGE,resistance=round(actTurn.char.chipInventory[tmpChip.id].power*[1,0.6][skillToUse.area!=AREA_MONO]),emoji='<:resisUp:1170999443861020742>')
													tempTurnMsg += groupAddEffect(caster=actTurn, target=ennemi, area=affectedEntities, effect=tmpEff, skillIcon=tmpChip.emoji)
												elif tmpChip.name == "Symbiose" and skillToUse.type == TYPE_BOOST and skillToUse.range == AREA_MONO:
													tablSecEnt = []
													for ent in tablEntTeam[actTurn.team]:
														if ent.hp > 0 and ent.char.__class__ == classes.invoc and ent.summoner.id == actTurn.id:
															secEntInAreaTabl = ent.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES,effect=skillToUse.effects, directTarget=False, fromCell=ent.cell)
															for tmpEnt in secEntInAreaTabl[:]:
																if tmpEnt not in affectedEntities and tmpEnt not in tablSecEnt:
																	tablSecEnt.append(tmpEnt)
													if len(tablSecEnt) > 0:
														powerPourcent = round([100,skillToUse.effPowerPurcent][skillToUse.effPowerPurcent != None] * (actTurn.char.chipInventory[tmpChipId].power)/100)
														tempTurnMsg += groupAddEffect(caster=actTurn, target=ennemi, area=tablSecEnt, effect=skillToUse.effects, skillIcon=tmpChip.emoji, actionStats=skillToUse.useActionStats, effPurcent = powerPourcent)

										if skillToUse.type == TYPE_BOOST and skillToUse.range == AREA_MONO:
											if partnerIn.id in actTurn.specialVars:
												for eff in actTurn.effects:
													if eff.effects.id == partnerIn.id:
														partnerEnt = eff.replicaTarget

												if partnerEnt.hp > 0:
													initArea = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ALLIES,directTarget=False)
													secondArea = partnerEnt.cell.getEntityOnArea(area=skillToUse.area,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,directTarget=False)

													for ent in secondArea[:]:
														if ent in initArea or ent == actTurn:
															secondArea.remove(ent)

													if len(secondArea) > 0:
														effPower = [skillToUse.effPowerPurcent,100][skillToUse.effPowerPurcent == None]
														ballerine = groupAddEffect(caster=actTurn, target=partnerEnt, area=secondArea, effect=skillToUse.effects, skillIcon=partner.emoji, actionStats=skillToUse.useActionStats, effPurcent = [effPower * partnerIn.power * 0.01,effPower][findEffect(skillToUse.effects[0]).id == tangoEndEff.id])
														tempTurnMsg += ballerine
														logs += ballerine

									elif skillToUse.type in [TYPE_INDIRECT_DAMAGE,TYPE_MALUS]:
										if skillToUse.id not in [serenaSpe.id,fairyLiberation.id]:
											ballerine = groupAddEffect(caster=actTurn, target=ennemi, area=skillToUse.area, effect=skillToUse.effects, skillIcon=skillToUse.emoji, actionStats=skillToUse.useActionStats, effPurcent = skillToUse.effPowerPurcent)
											tempTurnMsg += ballerine
											logs += ballerine

											if skillToUse.id == []:
												pass

											for eff in actTurn.effects:
												if eff.effects.id in [propagEff.id,propagDelEff] and ennemi.team != actTurn.team:
													try:
														if teamJaugeDict[actTurn.team][actTurn].effects.id == healerGlare.jaugeEff.id and teamJaugeDict[actTurn.team][actTurn].value > 35:
															teamJaugeDict[actTurn.team][actTurn].value -= 35
															ballerine = groupAddEffect(caster=actTurn, target=ennemi, area=ennemi, effect=eff.effects.callOnTrigger,skillIcon=eff.icon)
															tempTurnMsg += ballerine
															logs += ballerine
													except KeyError:
														pass
										elif skillToUse.id == serenaSpe.id:
											for ent in tablEntTeam[int(not(actTurn.team))]:
												if ent.hp > 0:
													sumPower = 0
													for eff in ent.effects:
														if eff.effects.id == estial.id:
															sumPower += int(eff.effects.power*eff.turnLeft*(skillToUse.power/100))
															eff.decate(value=100)

													if sumPower > 0:
														ent.refreshEffects()
														sumPower += estial.power * estial.turnInit * (skillToUse.power/100)
														temp = actTurn.indirectAttack(target=ent,value=indirectDmgCalculator(actTurn, ent, sumPower, skillToUse.use, danger, skillToUse.area),icon=skillToUse.emoji)
													else:
														temp = "Cela a aucun effet sur __{0}__\n".format(ent.name)
													tempTurnMsg += temp
													logs += temp
										elif skillToUse.id == fairyLiberation.id:
											tablEntEnnemis = ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENEMIES,directTarget=False,fromCell=actTurn.cell)
											for ent in tablEntEnnemis:
												effExplo, sumPow = copy.deepcopy(liberationEff), 0
												for eff in ent.effects:
													if eff.effects.id == estial.id:
														sumPow += eff.effects.power * eff.value * (effExplo.power/100)
														eff.decate(turn=99)
												effExplo.power = sumPow
												if effExplo.power > 0:
													if effExplo.power < 10:
														effExplo.callOnTrigger = None
													ballerine = groupAddEffect(caster=actTurn, target=ent, area=AREA_MONO, effect=effExplo, skillIcon=skillToUse.emoji)
													tempTurnMsg += ballerine
													logs += ballerine

										if skillToUse.id == cwUlt.id:
											skillToUse.maxPower = skillToUse.maxPower * (skillToUse.power/skillToUse.initPower)
											mul = skillToUse.power+(skillToUse.maxPower-skillToUse.power)/(jaugeConsumed/[skillToUse.maxJaugeValue,skillToUse.minJaugeValue][skillToUse.maxJaugeValue==0])

											skillToUse.power = mul
											for eff in ennemi.effects:
												if eff.effects.type == TYPE_INDIRECT_DAMAGE:
													if eff.effects.id == coroWind.id:
														skillToUse.power += mul * eff.turnLeft/eff.effects.turnInit
													else:
														skillToUse.power += mul * eff.turnLeft/eff.effects.turnInit * 1.35
														eff.decate(turn=99)

											if skillToUse.power > 0:
												ballerine = actTurn.indirectAttack(ennemi,value=indirectDmgCalculator(actTurn, ennemi, skillToUse.power, skillToUse.use, danger, area=skillToUse.area),icon = skillToUse.emoji)
												tempTurnMsg += ballerine
												logs += ballerine
												ennemi.refreshEffects()
										elif skillToUse.id == propag.id:
											listTarget = []
											sumPower = 0
											for eff in ennemi.effects:
												if eff.effects.id in [estial.id] and eff.value > 0:
													sumPower += eff.effects.power * ([propag.power,propag.power//2][int(eff.caster==actTurn)])/100
											affectedEnemies = ennemi.cell.getEntityOnArea(area=AREA_DONUT_2,team=actTurn.team,wanted=ENEMIES, directTarget=False, fromCell=actTurn.cell)
											if len(affectedEnemies) >= 1:
												temp = groupAddEffect(caster=actTurn, target=ennemi, area=affectedEnemies, effect=estial, skillIcon=skillToUse.emoji, actionStats=ACT_BOOST,effPurcent=int((sumPower/estial.power)*100))
												tempTurnMsg += temp
												logs += temp
											else:
												effTemp = classes.effect("Vulnérabilité Indirecte","indiVulnePropag",MAGIE,inkResistance=-10,turnInit=3,type=TYPE_MALUS)
												temp = groupAddEffect(caster=actTurn, target=ennemi, area=AREA_MONO, effect=effTemp, skillIcon=skillToUse.emoji, actionStats=ACT_BOOST)
												tempTurnMsg += temp
												logs += temp

										tmpChip = getChip("Toxiception")
										if tmpChip.id in actTurn.char.equippedChips and ennemi.id != actTurn.id:
											tempTurnMsg += groupAddEffect(actTurn,ennemi,AREA_MONO,toxiceptionEff,tmpChip.emoji)

									elif skillToUse.type == TYPE_HEAL:
										logs += "\n"
										if skillToUse.id == healingSacrifice.id:
											skillToUse: classes.skill = copy.deepcopy(skillToUse)
											pvConsumed = actTurn.hp - 1
											actTurn.hp = 1
											tempTurnMsg += "{0} {1} → {0} -{2} PV\n\n".format(actTurn.icon,skillToUse.emoji,pvConsumed)
											skillToUse.use, skillToUse.power, skillToUse.effPowerPurcent = None, round(pvConsumed*skillToUse.power/100), int(100*pvConsumed/actTurn.maxHp)

										if ennemi.hp > 0 or skillToUse.area != AREA_MONO:
											elemPowBonus = 0
											if skillToUse.condition[:2] == [0,2]:
												for eff in actTurn.effects:
													if eff.effects.id in [tablElemEff[skillToUse.condition[2]],tablElemEff[ELEMENT_UNIVERSALIS]]:
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

											skillToUse.power = skillToUse.power * (1+(LIGHTHEALBUFF/100*actTurn.char.element == ELEMENT_LIGHT))
											skillToUse.power, actionStats = skillToUse.power * (1+elemPowBonus * 0.05), ACT_HEAL

											if skillToUse.id == dissi.id:
												nbSummon = 0
												for ent in tablEntTeam[actTurn.team]:
													if type(ent.char) == invoc and ent.id == actTurn.id:
														nbSummon += 1
														tempTurnMsg += "{0} est désinvoqué\n".format(ent.char.name)
														ent.hp = 0
												skillToUse.power += skillToUse.power*nbSummon

											elif skillToUse.id == trans.id:
												actionStats, entActStats = 0, actTurn.actionStats()
												for cmpt in (0,1,2,3,4):
													if entActStats[cmpt] > entActStats[actionStats]:
														actionStats = cmpt
											else:
												actionStats = ACT_HEAL

											if skillToUse.id == uberCharge.id:
												if jaugeConsumed >= 100:
													skillToUse.effects[0] = uberImune
												else:
													skillToUse.effects[0] = copy.deepcopy(defenseUp)
													skillToUse.effects[0].power = 5 + (70/100*jaugeConsumed)

											for ent in ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,fromCell=actTurn.cell,wanted=ALLIES,directTarget=False):
												funnyTempVarName, useless = actTurn.heal(ent, skillToUse.emoji, skillToUse.use, skillToUse.power, danger=danger, mono = skillToUse.area == AREA_MONO, useActionStats = skillToUse.useActionStats, incHealJauge=(skillToUse.jaugeEff == None) or (skillToUse.jaugeEff != None and skillToUse.jaugeEff.id == uberJauge.id))
												tempTurnMsg += funnyTempVarName
												logs += funnyTempVarName

											if skillToUse.effects != [None] and not(skillToUse.effBeforePow):
												ballerine = groupAddEffect(caster=actTurn, target=ennemi, area=skillToUse.area, effect=skillToUse.effects, skillIcon=skillToUse.emoji, actionStats=skillToUse.useActionStats, effPurcent = skillToUse.effPowerPurcent)
												tempTurnMsg += ballerine
												logs += ballerine

									elif skillToUse.type == TYPE_SUMMON:
										toSummon, cmpt, limit = findSummon(skillToUse.invocation), 0, skillToUse.nbSummon
										if skillToUse.id == selfMemoria.id:
											tempTurnMsg += actTurn.summonMemoria(actTurn, tablAliveInvoc, time)
										else:
											while cmpt < limit:
												cellToSummon = actTurn.cell.getCellForSummon(skillToUse.range,actTurn.team,toSummon,actTurn)
												if cellToSummon != None:
													tablEntTeam, tablAliveInvoc, time, funnyTempVarName = actTurn.summon(toSummon, time, cellToSummon, tablAliveInvoc, ignoreLimite=True)
													tempTurnMsg += funnyTempVarName
													logs += "\n"+funnyTempVarName
												cmpt += 1

									elif skillToUse.type == TYPE_RESURECTION:
										stat, resTabl = skillToUse.use, []
										if stat not in [PURCENTAGE,None,FIXE,MISSING_HP]:
											tempActStatsTabl = [[ACT_HEAL,actTurn.negativeHeal],[ACT_BOOST,actTurn.negativeBoost],[ACT_SHIELD,actTurn.negativeShield]]
											tempActStatsTabl.sort(key=lambda ballerine:ballerine[1])

										for target in ennemi.cell.getEntityOnArea(area=skillToUse.area,fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,dead=True,directTarget=False,ignoreInvoc=True):
											if stat not in [PURCENTAGE,None,FIXE,MISSING_HP]:
												if stat == HARMONIE: statUsed = max(actTurn.allStats())
												else: statUsed = actTurn.allStats()[skillToUse.use]
												healPowa = min(target.maxHp, calHealPower(actTurn,target,skillToUse.power, 1, statUsed,tempActStatsTabl[0][0],danger))
											elif stat == PURCENTAGE:
												healPowa = round(target.maxHP * skillToUse.power/100)
											elif stat == MISSING_HP:
												healPowa = round((target.maxHp-target.hp)*skillToUse.power/100)
											elif stat == None:
												healPowa = skillToUse.power

											funnyTempVarName = await actTurn.resurect(target,healPowa,skillToUse.emoji,danger=danger)
											tempTurnMsg += funnyTempVarName
											logs += funnyTempVarName
											resTabl.append(target)

										if skillToUse.id == inMemoria.id:
											for ent in tablEntTeam[actTurn.team]:
												if ent.hp < 0 and type(ent.char) not in [invoc,depl] :
													tempTurnMsg += actTurn.summonMemoria(ent, tablAliveInvoc, time)
												elif ent.isNpc("Anna"):
													belle = copy.deepcopy(findAllie("Belle"))
													belle.changeLevel(ent.char.level,False,ent.char.stars)
													belle = entity(ent.id, belle, ent.team, False, auto=True, danger=[100,danger][ent.team > 0])
													tempTurnMsg += actTurn.summonMemoria(belle, tablAliveInvoc, time)
												elif ent.isNpc("Iliana"):
													belle = copy.deepcopy(findAllie("Aurora"))
													belle.changeLevel(ent.char.level,False,ent.char.stars)
													belle = entity(ent.id, belle, ent.team, False, auto=True, danger=[100,danger][ent.team > 0])
													tempTurnMsg += actTurn.summonMemoria(belle, tablAliveInvoc, time)

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

										if skillToUse.id == snowFall.id and ennemi.on == None:
											tempTurnMsg += "{0} saute sur la cellule {1}:{2}\n".format(actTurn.name,ennemi.x,ennemi.y)+actTurn.move(cellToMove=ennemi)

									elif type(ennemi) == entity: # Damage
										elemPowBonus, elemEffGet = 0, 0
										skillToUse.maxPower = skillToUse.maxPower * (skillToUse.power/skillToUse.initPower)

										if skillToUse.condition[:2] == [0,2]:
											for eff in actTurn.effects:
												if eff.effects.id in [tablElemEff[skillToUse.condition[2]],tablElemEff[ELEMENT_UNIVERSALIS]]:
													elemPowBonus += eff.effects.power
													elemEffGet += 1
										if elemPowBonus > 0:
											skillToUse.power = skillToUse.power * (1+(elemPowBonus/100))

										if skillToUse.id == lowBlow.id and (ennemi.char.standAlone or ennemi.name in ENEMYIGNORELIGHTSTUN):
											skillToUse.power += skillToUse.maxPower - skillToUse.power
										elif skillToUse.id == memClemCastSkill.id:
											effect = classes.effect("Bouclier vampirique","clemMemSkillShield",overhealth=(actTurn.hp-1)//2,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji('<:clemMemento2:902222663806775428>'),absolutShield=True)
											tempTurnMsg += "{0} : - {1} PV\n".format(actTurn.icon,actTurn.hp-1)
											actTurn.hp = 1
											actTurn.maxHp, actTurn.healResist = actTurn.maxHp//2,actTurn.healResist//2
											tempTurnMsg += add_effect(actTurn,actTurn,effect,ignoreEndurance=True)
											defIncur50 = incur[5]
											defIncur50.turnInit, defIncur50.unclearable = -1,True
											tempTurnMsg += add_effect(actTurn,actTurn,defIncur50)
										elif skillToUse.id == theEnd.id:
											for eff in ennemi.effects:
												if eff.effects.id == reaperEff.id:
													skillToUse.power = int(skillToUse.power*1.2)
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
											skillToUse.power = skillToUse.power * (bleedingNumber+1)
										elif skillToUse.id == kikuSkill2.id and ennemi.status == STATUS_ALIVE:
											skillToUse.power = int(skillToUse.power*2)
										elif skillToUse.id in elemArrowId+elemRuneId:
											skillToUse.power += INCREASEPOWERPURCENTBYELEMEFF * useEffElem
										elif skillToUse.id in [klikliStrike.id,gwenyStrike.id]:
											hpConsumed = actTurn.hp - 1
											actTurn.stats.selfBurn += hpConsumed
											actTurn.hp = 1
											tempTurnMsg += "Les PVs de {0} sont réduits à 1 !\n".format(actTurn.name)
											skillToUse.power += (skillToUse.maxPower - skillToUse.power) * (hpConsumed/actTurn.maxHp)
										elif skillToUse.id == liaExUlt_1.id:
											effect = classes.effect("Kaze no yoroi","liaExUltShield",overhealth=int(actTurn.maxHp * (1-10*elemEffGet)),type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,turnInit=2)
											tempTurnMsg += add_effect(actTurn,actTurn,effect,ignoreEndurance=True)
											actTurn.refreshEffects()
										elif skillToUse.id in [liaExUlt_2.id,liaExUlt_3.id]:
											skillToUse.power = int(skillToUse.power  * (1+10*elemEffGet))
										elif skillToUse.id in [liaExUlt_4.id]:
											skillToUse.power = int(skillToUse.power  * (1+15*elemEffGet))
										elif skillToUse.id == deterStrike.id:
											maxCon, cons = actTurn.maxHp, 0
											for eff in actTurn.effects:
												if eff.effects.type == TYPE_ARMOR:
													if (cons + eff.value) > maxCon:
														eaten = maxCon - cons
													else:
														eaten = eff.value
													eff.decate(value=eaten)
													cons += eaten
											if cons > 0:
												tempTurnMsg += "{0} consomme {1} PAr !\n".format(actTurn.name,cons)
											skillToUse.effects = [classes.effect("Frappe Déterminée","deterStrikeEff",type=TYPE_INDIRECT_DAMAGE,power=cons,trigger=TRIGGER_INSTANT,emoji=skillToUse.emoji)]
										elif skillToUse.id == soulTwin.id:
											skillToUse: classes.skill = copy.deepcopy(skillToUse)
											effPower = 0
											for eff in ennemi.effects:
												if eff.effects.id == soulScealEff.id and eff.caster.id == actTurn.id:
													effPower = eff.effects.power * soulTwinEff.power/soulScealEff.power
													break
											if effPower > 0:
												skillToUse.effects[0].power = effPower
											else:
												skillToUse.effects = [None]
										elif skillToUse.id == soulWave.id:
											skillToUse: classes.skill = copy.deepcopy(skillToUse)
											effPower = 0
											for eff in ennemi.effects:
												if eff.effects.id == soulScealEff.id and eff.caster.id == actTurn.id:
													effPower = eff.effects.power * skillToUse.effPowerPurcent/100
													break
											if effPower > 0:
												soulWaveEff2 = copy.deepcopy(soulWaveEff)
												soulWaveEff2.power, soulWaveEff2.turnInit, soulWaveEff2.lvl = round(effPower,2), eff.turnLeft, eff.value
												eff = classes.effect(skillToUse.name,skillToUse.id,area=AREA_DONUT_2,emoji=skillToUse.emoji,callOnTrigger=soulWaveEff2,type=TYPE_MALUS,trigger=TRIGGER_INSTANT)
												skillToUse.effects = [eff]
											else:
												skillToUse.effects = [None]
										elif skillToUse.id == echec.id:
											for eff in ennemi.effects:
												if eff.effects.id == deathMark.id and eff.caster.id == actTurn.id:
													skillToUse = copy.deepcopy(mat)
										elif skillToUse.id == funDraw.id:
											for eff in ennemi.effects:
												if eff.effects.id == deathMark.id:
													eff.effects.power = round(eff.effects.power * 1.35)
										elif skillToUse.id == kliSkill3.id:
											nbHpConsummed = actTurn.hp//2
											instantDmgEff, ratio = classes.effect(skillToUse.name,"sacrInstEff",power=nbHpConsummed,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,emoji=skillToUse.emoji), 1-(nbHpConsummed/(actTurn.maxHp//2))
											tempTurnMsg += groupAddEffect(actTurn, actTurn, AREA_MONO,instantDmgEff,skillToUse.emoji)
											skillToUse.power = int((skillToUse.power*ratio)+((1-ratio)*skillToUse.maxPower))
											skillToUse.effects[0].power = int(skillToUse.effects[0].power*(1+(skillToUse.power/skillToUse.maxPower)))
										elif skillToUse.id == dicetiny.id:
											randomRolls = sorted([random.randint(1,6), random.randint(1,6), random.randint(1,6)])
											rollsSum = sum(randomRolls)
											skillToUse.power = skillToUse.initPower + ((skillToUse.maxPower-skillToUse.initPower)/15*(rollsSum-3))
											tempTurnMsg += "{0} {1} tire 3 dés : 🎲{2}, 🎲{3}, 🎲{4}\n".format(skillToUse.emoji, actTurn.name, randomRolls[0], randomRolls[1], randomRolls[2])

											if randomRolls[0] == randomRolls[1] or randomRolls[1] == randomRolls[2] or randomRolls[2] == randomRolls[0]: skillToUse.power = skillToUse.power*1.2
											elif randomRolls[2] == randomRolls[1]+1 == randomRolls[0]+2: skillToUse.power = skillToUse.power*1.1
											elif randomRolls[0] == randomRolls[1] == randomRolls[2]: skillToUse.power = skillToUse.power*1.5

											oddNumber, threeMultiple, sixCount = 0, 0, 0
											for tmp in randomRolls:
												if tmp%2 == 0: oddNumber += 1
												if tmp%3 == 0: threeMultiple += 1
												if tmp == 6: sixCount += 1
											
											if sixCount > 0: skillToUse.garCrit = True
											if sixCount > 1: skillToUse.power = skillToUse.power*(1+(0.05*(sixCount-1)))
											if threeMultiple > 0: skillToUse.percing = 1+(0.05*threeMultiple)
											if oddNumber > 0: skillToUse.effects = [classes.effect("ExploDés","explodice",HARMONIE,type=TYPE_DAMAGE,power=int(skillToUse.power * 0.2 * oddNumber),trigger=TRIGGER_INSTANT,area=AREA_DONUT_1,emoji='<:blueShockWave:1231542914950365277>')]

										if skillToUse.sharedDamage or skillToUse.sharedTB:
											nbEnnemis = len(ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENEMIES,directTarget=False,fromCell=ennemi.cell,ignoreAspiration = [None,[OBSERVATEUR,ATTENTIF,SORCELER,MAGE,ALTRUISTE,IDOLE,INOVATEUR,PREVOYANT,MASCOTTE]][skillToUse.sharedTB]))
											skillToUse.power = skillToUse.power // clamp(nbEnnemis,1,10)

										actionStats = skillToUse.useActionStats
										if actTurn.char.secElement == ELEMENT_LIGHT and (
												(skillToUse.effectAroundCaster != None and skillToUse.effectAroundCaster[0] in [TYPE_HEAL,TYPE_INDIRECT_HEAL]) or
												(skillToUse.effectOnSelf != None and skillToUse.effectOnSelf.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL]) or
												(skillToUse.lifeSteal > 0 or skillToUse.aoeLifeSteal > 0) or
												(skillToUse.effectAroundCaster != None and skillToUse.effectAroundCaster[0] in [TYPE_ARMOR]) or
												(skillToUse.effectOnSelf != None and skillToUse.effectOnSelf.type in [TYPE_ARMOR]) or
												(skillToUse.armorConvert > 0 or skillToUse.aoeArmorConvert > 0)
											):
												skillToUse.power = skillToUse.power * (1+(LIGHTDMGBUFF/100))

										cmpt = 0
										while cmpt < skillToUse.repetition and skillToUse.power > 0:
											funnyTempVarName, temp = actTurn.attack(
												target=ennemi,
												value=skillToUse.power,
												icon=skillToUse.emoji,
												area=skillToUse.area,
												accuracy=skillToUse.accuracy,
												use=skillToUse.use,
												onArmor=skillToUse.onArmor,
												useActionStats=actionStats,
												setAoEDamage=skillToUse.setAoEDamage,
												lifeSteal = skillToUse.lifeSteal,
												erosion = skillToUse.erosion,
												skillPercing = skillToUse.percing,
												execution=skillToUse.execution,
												skillUsed=skillToUse,
												effectOnHit=[None,skillToUse.effects][skillToUse.repetition>1])
											tempTurnMsg = tempTurnMsg + funnyTempVarName
											logs += "\n"+funnyTempVarName
											deathCount += temp
											cmpt += 1
											if cmpt < skillToUse.repetition:
												tempTurnMsg += "\n"

										if None not in skillToUse.effects and not(skillToUse.effBeforePow) and skillToUse.repetition <= 1:
											for a in skillToUse.effects:
												eff = findEffect(a)
												tempTurnMsg += add_effect(actTurn,ennemi,eff,effPowerPurcent=skillToUse.effPowerPurcent, skillIcon=skillToUse.emoji)
												logs += "\n{0} gave the {1} effect at {2} for {3} turn(s)".format(actTurn.char.name,eff.name,ennemi.char.name,eff.turnInit)

										if actTurn.isNpc("Ailill") and skillToUse.id == "headnt":
											ennemi.stats.headnt = True
										elif actTurn.isNpc("Iliana prê."):
											funnyTempVarName, useless = actTurn.heal(actTurn, actTurn.skills[0].effects[0].emoji[0][0], actTurn.skills[0].effects[0].stat, actTurn.skills[0].effects[0].power*1.25, danger=danger, mono = True, useActionStats = ACT_HEAL,direct=False)
											tempTurnMsg += funnyTempVarName
											logs += funnyTempVarName

										if skillToUse.area == AREA_MONO:
											communChipList = ["Incurable","Friable"]
											chipBaseEff = [incurable,armorGetMalus]
											for indx, chipName in enumerate(communChipList):
												tmpChip = getChip(chipName)
												if tmpChip != None and tmpChip.id in actTurn.char.equippedChips:
													tempEff = copy.deepcopy(chipBaseEff[indx])
													tempEff.power, tempEff.turnInit = actTurn.char.chipInventory[tmpChip.id].power, 1
													tempTurnMsg += groupAddEffect(caster=actTurn, target=ennemi, area=AREA_MONO, effect=tempEff)

										if skillToUse.execution:
											ennemi.status = STATUS_TRUE_DEATH

										if skillToUse.id == gemmes.id:
											for ent in tablEntTeam[actTurn.team]:
												if type(ent.char) == invoc and ent.char.name.startswith("Carbuncle"):
													skillToUse.power = [65,50][ent.char.element in [ELEMENT_AIR,ELEMENT_FIRE,ELEMENT_SPACE,ELEMENT_LIGHT]]
													area = [AREA_MONO,AREA_CIRCLE_1][ent.char.element in [ELEMENT_AIR,ELEMENT_FIRE,ELEMENT_SPACE,ELEMENT_LIGHT]]
													funnyTempVarName, temp = ent.attack(
														target=ennemi,
														value=power,
														icon=skillToUse.emoji,
														area=area,
														accuracy=skillToUse.accuracy,
														use=HARMONIE,
														onArmor=skillToUse.onArmor,
														useActionStats=actionStats,
														setAoEDamage = skillToUse.setAoEDamage,
														lifeSteal = skillToUse.lifeSteal,
														erosion = skillToUse.erosion,
														skillPercing = skillToUse.percing,
														execution=skillToUse.execution,
														skillUsed=skillToUse)
													tempTurnMsg += funnyTempVarName
													logs += "\n"+funnyTempVarName
													deathCount += temp
										elif skillToUse.id == burningClaw.id:
											for eff in ennemi.effects:
												if eff.effects.id == bloodButterfly.id:
													tmp1, tmp2 = eff.caster.attack(target=ennemi, value = 30, icon = eff.icon, area=AREA_MONO, accuracy=300, use=MAGIE, useActionStats = ACT_DIRECT, lifeSteal = 50)
													
													tempTurnMsg += tmp1
										for eff in actTurn.effects:
											if eff.effects.id in [propagEff.id,propagDelEff] and ennemi.team != actTurn.team:
												try:
													if teamJaugeDict[actTurn.team][actTurn].effects.id == healerGlare.jaugeEff.id and teamJaugeDict[actTurn.team][actTurn].value > 35:
														teamJaugeDict[actTurn.team][actTurn].value -= 35
														ballerine = groupAddEffect(caster=actTurn, target=ennemi, area=ennemi, effect=eff.effects.callOnTrigger,skillIcon=eff.icon)
														tempTurnMsg += ballerine
														logs += ballerine
												except KeyError:
													pass
											elif eff.effects.id in [convictionVigilantEff.id,convicProEff.id,convictEnchtEff.id,convictTetEff.id] and not(skillToUse.replay):
												ballerine = eff.triggerStartOfTurn(danger,decate=True)
												logs += ballerine
												tempTurnMsg += ballerine
								# =================================================================
								# Knockback
								if skillToUse.knockback > 0:
									tablEnt, listKnockback = ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=[ENEMIES,ALLIES][skillToUse.id == friendlyPush.id],directTarget=False,fromCell=actTurn.cell), []
									tablEnt.sort(key=lambda ent: actTurn.cell.distance(ent.cell),reverse=True)
									for ent in tablEnt: listKnockback.append(actTurn.knockback(ent,skillToUse.knockback))

									ballerine = formatKnockBack(listResult=listKnockback, listEnt=tablEnt, knockbackPower=skillToUse.knockback)

									tempTurnMsg += ballerine
									logs += ballerine

								if skillToUse.pull > 0:
									tablEnt = ennemi.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENEMIES,directTarget=False,fromCell=actTurn.cell)
									tablEnt.sort(key=lambda ent: actTurn.cell.distance(ent.cell))
									tablPulled, toReturn = [], ""
									for ent in tablEnt:
										temp = actTurn.pull(ent,skillToUse.pull)
										if len(temp) > 0:
											if len(temp.splitlines())<=1:
												tablPulled.append(ent)
											else:
												toReturn += temp
										
										logs += temp

									if len(tablPulled) > 0:
										tmpList, lenPulled = "", len(tablPulled)-1
										for indx, ent in enumerate(tablPulled):
											tmpList += "{0}".format(ent.name)
											if indx == lenPulled-1:
												tmpList += " et "
											elif indx < lenPulled-1:
												tmpList += ", "
										tempTurnMsg += "\n"+tmpList+ " {0} attiré{1} vers {2}\n".format(["est","sont"][lenPulled>0],["","s"][lenPulled>0],actTurn.name)
									tempTurnMsg += toReturn

									tmpChip = getChip("Camalataque")
									if tmpChip.id in actTurn.char.equippedChips:
										tmpEff = classes.effect(tmpChip.name,"squidAttack",HARMONIE,power=int(actTurn.char.level*actTurn.char.chipInventory[tmpChip.id].power/100),area=AREA_DONUT_1,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_INSTANT,emoji=tmpChip.emoji)
										tempTurnMsg += groupAddEffect(caster=actTurn, target=actTurn, area=AREA_MONO, effect=tmpEff, skillIcon=tmpChip.emoji)

								# JumpBack
								if skillToUse.jumpBack > 0:
									tempCell = actTurn.cell
									temp = actTurn.jumpBack(skillToUse.jumpBack,ennemi.cell)
									tempTurnMsg += temp
									logs += temp
									if tempCell.id != actTurn.cell.id and squidRollEff.id in actTurn.specialVars:
										tempTurnMsg += groupAddEffect(caster=actTurn, target=actTurn, area=AREA_MONO, effect=squidRollEff.callOnTrigger, skillIcon=squidRollEff.emoji[0][0])

									for indx, tmpChipId in enumerate(actTurn.char.equippedChips):
										tmpChip = getChip(tmpChipId)
										if tmpChip != None:
											if tmpChip.name == "Pas Piégés" and actTurn.chipAddInfo[indx] > 0:
												tmpEff = copy.deepcopy(littleTrapEff)
												tmpEff.power = actTurn.char.chipInventory[tmpChip.id].power
												tempTurnMsg += groupAddEffect(caster=actTurn, target=ennemi, area=AREA_MONO, effect=tmpEff, skillIcon=tmpChip.emoji)
												actTurn.chipAddInfo[indx] -= 1

								# Does the skill give a effect on the caster ?
								if skillToUse.effectAroundCaster != None:
									if skillToUse.effectAroundCaster[0] == TYPE_HEAL:
										tablHealed, tablRespond = [],[]
										for target in actTurn.cell.getEntityOnArea(area=skillToUse.effectAroundCaster[1],fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,directTarget=False):
											if target.hp/target.maxHp<1:
												targetHp = target.hp
												funnyTempVarName, useless = actTurn.heal(target,skillToUse.emoji,skillToUse.use,skillToUse.effectAroundCaster[2],skillToUse.name,danger)
												tablRespond.append(funnyTempVarName)
												tablHealed.append([target,target.hp - targetHp])

										if len(tablHealed) > 1:
											listIcon, sumHeal = "", 0
											for ent in tablHealed:
												listIcon += ent[0].icon
												sumHeal += ent[1]
											sumHeal = int(sumHeal / len(tablHealed))
											tempTurnMsg += "{0} {1} → {2} +≈{3} PV\n".format(actTurn.icon,skillToUse.emoji,listIcon,sumHeal)
										elif len(tablHealed) == 1:
											tempTurnMsg += tablRespond[0]
									elif skillToUse.effectAroundCaster[0] == TYPE_DAMAGE:
										funnyTempVarName, temp = actTurn.attack(target=actTurn,value=skillToUse.effectAroundCaster[2],icon=skillToUse.emoji,area=skillToUse.effectAroundCaster[1],accuracy=skillToUse.accuracy,use=skillToUse.use,onArmor=skillToUse.onArmor,useActionStats=actionStats,setAoEDamage=skillToUse.setAoEDamage,lifeSteal = skillToUse.lifeSteal)
										tempTurnMsg += ["","\n"][tempTurnMsg[-1]!="\n" and len(funnyTempVarName)>0]+"\n"+funnyTempVarName
										logs += "\n"+funnyTempVarName
									elif type(skillToUse.effectAroundCaster[2]) == classes.effect:
										if skillToUse.id != requiem.id:
											ballerine = groupAddEffect(actTurn, actTurn, skillToUse.effectAroundCaster[1], skillToUse.effectAroundCaster[2], skillToUse.emoji, effPurcent=[skillToUse.effPowerPurcent,liaLB.effPowerPurcent/5][skillToUse.id == trans.id and actTurn.isNpc("Lia")])
											if len(ballerine)>0:
												tempTurnMsg = [tempTurnMsg+ballerine,tempTurnMsg[:-1]+ballerine][tempTurnMsg[-1]+ballerine[0]=="\n\n"]
												logs += ballerine
										else:
											ballerine = actTurn.cell.getEntityOnArea(area=skillToUse.effectAroundCaster[1],team=actTurn.team,wanted=ENEMIES,effect=[skillToUse.effectAroundCaster[2]],directTarget=False,fromCell=actTurn.cell)
											if len(ballerine)>0:
												babies = [[],[],[],[]]
												for ent in ballerine:
													distance = actTurn.cell.distance(ent.cell)
													if distance == 1:
														babies[0].append(ent)
													elif distance <= 3:
														babies[1].append(ent)
													elif distance <= 9:
														babies[2].append(ent)
													else:
														babies[3].append(ent)
												for cmpt in (0,1,2,3):
													if len(babies[cmpt])>0:
														ballerine = groupAddEffect(caster=actTurn, target=actTurn, area=babies[cmpt], effect=skillToUse.effectAroundCaster[2], skillIcon=skillToUse.emoji, actionStats=ACT_BOOST,effPurcent=[200,150,100,50][cmpt])
														tempTurnMsg = [tempTurnMsg+ballerine,tempTurnMsg[:-1]+ballerine][tempTurnMsg[-1]+ballerine[0]=="\n\n"]
														logs += ballerine

									elif skillToUse.effectAroundCaster[0] == TYPE_RESURECTION:
										stat = skillToUse.use
										for a in actTurn.cell.getEntityOnArea(area=skillToUse.effectAroundCaster[1],fromCell=actTurn.cell,team=actTurn.team,wanted=ALLIES,dead=True,directTarget=False):
											if stat != HARMONIE:
												statUse = actTurn.allStats()[stat]
											else:
												statUse = max(actTurn.allStats())


											tempActStatsTabl = [[ACT_HEAL,actTurn.negativeHeal],[ACT_BOOST,actTurn.negativeBoost],[ACT_SHIELD,actTurn.negativeShield]]
											tempActStatsTabl.sort(key=lambda ballerine:ballerine[1])
											healPowa = calHealPower(actTurn, a, skillToUse.effectAroundCaster[2] ,1, statUse, tempActStatsTabl[0][0],danger)

											funnyTempVarName = await actTurn.resurect(a,healPowa,skillToUse.emoji,danger=danger)
											tempTurnMsg += ["","\n"][tempTurnMsg[-1] != "\n" and len(funnyTempVarName)>0]+funnyTempVarName
											logs += funnyTempVarName
											bigRaiseCount += 1

								# Lb4
								if skillToUse.id == trans.id and skillToUse.name == lb4.name:
									lb4HealEff = classes.effect("Soins Transcendique","lb4HealEff",HARMONIE,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_INSTANT,emoji=lb4.emoji,power=200,area=AREA_ALL_ALLIES)
									lb4DmgBuff = copy.deepcopy(dmgUp)
									lb4DmgBuff.power, lb4DmgBuff.turnInit = 15,3
									lb4DefBuff = copy.deepcopy(defenseUp)
									lb4DefBuff.power, lb4DefBuff.turnInit = 15,3
									lb4DmgBuff1, lb4DefBuff1 = classes.effect("Dégâts Transcendique","lb4dmgBuff",type=TYPE_BOOST,trigger=TRIGGER_INSTANT,emoji=lb4.emoji,callOnTrigger=lb4DmgBuff,area=AREA_ALL_ALLIES), classes.effect("Résistance Transcendique","lb4defBuff",type=TYPE_BOOST,trigger=TRIGGER_INSTANT,emoji=lb4.emoji,callOnTrigger=lb4DefBuff,area=AREA_ALL_ALLIES)
									ballerine = groupAddEffect(actTurn, actTurn , AREA_MONO, [lb4HealEff,lb4DmgBuff1,lb4DefBuff1], skillToUse.emoji)
									tempTurnMsg += ballerine
									logs += ballerine
									hadLb4 = True

								if skillToUse.effectOnSelf != None and not(skillToUse.effBeforePow):
									eff = findEffect(skillToUse.effectOnSelf)
									if eff != None and eff.id not in [incKaikaku.id]:
										if eff.replica != None:
											tempTurnMsg += ["\n",""][eff.silent]+add_effect(actTurn,actTurn,eff,setReplica=ennemi)
											if ennemi != actTurn and not(skillToUse.replay) and type(ennemi) != cell:
												eff2 = classes.effect("⚠️ Cible - {0}".format(eff.replica.name),"targeted{0}".format(eff.replica.id),effPrio=1,silent=True,turnInit=eff.turnInit-1,emoji=eff.replica.emoji)
												add_effect(actTurn,ennemi,eff2)
												ennemi.refreshEffects()
										else:
											tempTurnMsg += ["\n",""][eff.silent]+add_effect(actTurn,actTurn,eff,skillIcon = skillToUse.emoji,effPowerPurcent=skillToUse.selfEffPurcent)
											actTurn.refreshEffects()
									else:
										for eff in ennemi.effects:
											if eff.effects.id == deathMark.id and eff.caster.id == actTurn.id:
												tempTurnMsg += eff.triggerRemove()
												eff.decate(value=99)
												ennemi.refreshEffects()
												break

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
											ballerine, why = actTurn.attack(ennemi,int(skillToUse.power*0.15),skillToUse.emoji,AREA_MONO,skillToUse.accuracy,use=MAGIE,skillPercing=skillToUse.percing)
											logs += ballerine
											tempTurnMsg += ballerine
											cmpt += 1
									elif skillToUse.id == useElemEffId[3]:
										ballerine, why = actTurn.attack(actTurn,int(skillToUse.power*0.2*useEffElem),skillToUse.emoji,AREA_DONUT_2,skillToUse.accuracy,use=MAGIE,skillPercing=skillToUse.percing)
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

											ballerine, why = actTurn.attack(target,int(skillToUse.power*0.30),skillToUse.emoji,AREA_CIRCLE_1,skillToUse.accuracy,use=MAGIE,skillPercing=skillToUse.percing)
											logs += ballerine
											tempTurnMsg += "\n"+ballerine
											if target.hp <= 0:
												tablTargets.remove(target)
											cmpt += 1

								# Max Hp cost
								if skillToUse.maxHpCost > 0:
									reduceMaxHp = skillToUse.maxHpCost
									if skillToUse.group == SKILL_GROUP_HOLY:
										if actTurn.weapon.effects != None and findEffect(actTurn.weapon.effects).id == ascendance.id:
											reduceMaxHp = skillToUse.maxHpCost * (100-findEffect(actTurn.weapon.effects).power)/100
										
										tmpChip = getChip("Crucifix")
										if tmpChip.id in actTurn.char.equippedChips:
											reduceMaxHp = reduceMaxHp * (1-(actTurn.char.chipInventory[tmpChip.id].power/100))

									diff = actTurn.maxHp - int(actTurn.maxHp * (1-(reduceMaxHp/100)))
									actTurn.maxHp = int(actTurn.maxHp * (1-(skillToUse.maxHpCost/100)))
									diff2 = min(0,actTurn.maxHp-actTurn.hp)
									actTurn.hp = min(actTurn.hp,actTurn.maxHp)
									tempTurnMsg += "\n{2} → {0} -{1} PV max\n".format(actTurn.icon,diff,skillToUse.emoji)
									actTurn.stats.selfBurn += abs(diff2)

								# Act HpCost
								reduceHp = skillToUse.hpCost
								if skillToUse.hpCost > 0:
									if skillToUse.group == SKILL_GROUP_DEMON:
										tmpChip = getChip("Démaniaque")
										if tmpChip.id in actTurn.char.equippedChips:
											reduceHp = reduceHp * (1-(actTurn.char.chipInventory[tmpChip.id].power/100))
									diff = actTurn.hp - int(actTurn.hp * (1-(reduceHp/100)))
									actTurn.hp = max(1,actTurn.hp-diff)
									tempTurnMsg += "\n{2} → {0} -{1} PV\n".format(actTurn.icon,diff,skillToUse.emoji)
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

								if skillToUse.id == liaExUlt_4.id:
									elemNm = 0
									for eff in actTurn.effects:
										if eff.effects.id in [tablElemEff[skillToUse.condition[2]],tablElemEff[ELEMENT_UNIVERSALIS]]:
											elemNm += 1
											eff.decate(turn=99)

									funnyTempVarName, useless = actTurn.heal(actTurn, skillToUse.emoji, None, int(actTurn.maxHp * (0.05*elemNm)),danger=danger, mono = True, useActionStats = skillToUse.useActionStats)
									tempTurnMsg += funnyTempVarName
									logs += funnyTempVarName
									actTurn.refreshEffects()

								if skillToUse.needEffect != None and skillToUse.consumeNeededEffects and skillToUse.effectFinisher:
									for needed in skillToUse.needEffect:
										for eff in actTurn.effects:
											if needed.id == eff.effects.id and needed.id not in [iliTmpSkill1_renfort.id]: eff.decate(turn=99); break
									actTurn.refreshEffects()

								if skillToUse.id == ilianaBonk.id:
									for indx, chipId in enumerate(actTurn.char.equippedChips):
										tmpChip = getChip(chipId)
										if tmpChip != None and tmpChip.name == skillToUse.name:
											actTurn.chipAddInfo[indx] = 0

								# ============================= Interactions =============================
								if skillToUse.ultimate and skillToUse.effects != [None] and skillToUse.type == TYPE_BOOST:			   # Alice
									for team in [0,1]:
										for ent in tablEntTeam[team]:
											if TRAIT_HIGHLIGHTED in ent.char.trait and ent.hp > 0:
												murcialago = ent.counter(target=actTurn)
												tempTurnMsg += murcialago

								if skillToUse.effectOnSelf != None and findEffect(skillToUse.effectOnSelf).replica != None and skillToUse.power == 0 and skillToUse.effects == [None]:
									tempTurnMsg += "{0} charge la compétence __{1}__\n".format(actTurn.name,skillToUse.name)

								elif skillToUse.id in tablRosesSkillsId and skillToUse.effectOnSelf == None: # Final Floral On Self
									for skilly in actTurn.skills:
										if type(skilly) == classes.skill and skilly.id == finalFloral.id:
											roseCount = 0
											for eff in actTurn.effects:
												if eff.effects.id in tablRosesId:
													roseCount += 1

											if roseCount < 3:
												if skillToUse.id in [onStage.id,floraisonFinale.id]:
													roseToAdd = rosePink
												elif skillToUse.id in [crimsomLotus.id]:
													roseToAdd = roseYellow
												elif skillToUse.id in [corGra.id,petalisation.id]:
													roseToAdd = roseDarkBlu
												elif skillToUse.id in [aliceDance.id,danceFas.id]:
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
								
								elif skillToUse.id in [plumeCel.id,hinaUlt.id,plumePers.id,pousAviaire.id,trainePlume.id,featherCross.id]:
									for skilly in actTurn.skills:
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
									for eff in actTurn.effects:
										if eff.effects.id == tablElemEff[ELEMENT_EARTH].id:
											eff.replaceEffect(tablElemEff[ELEMENT_FIRE])
									ally = copy.deepcopy(findAllie("Chûri-Hinoro"))
									ally.changeLevel(level=team1[0].level,stars=team1[0].stars)
									await actTurn.changeNpc(ally)
									tempTurnMsg += "{0}\n{1} __{2}__ prend sa forme de Demi-Phenix !\n".format(["\n",""][tempTurnMsg[-1] == "\n"], actTurn.icon, actTurn.name)
									logs += "\nChuri is ready to burn everything !\n"

								if actTurn.dualCast != None and skillToUse.type in hostileTypes and not(skillToUse.replay):
									target = ennemi
									if ennemi.id == actTurn.id:
										tempTablTarget = actTurn.cell.getEntityOnArea(area=skillToUse.area,team=actTurn.team,wanted=ENEMIES, directTarget=False, fromCell=actTurn.cell)
										if len(tempTablTarget) > 0:
											tempTablTarget.sort(key=lambda ballerine: actTurn.getAggroValue(ballerine),reverse=True)
											target = tempTablTarget[0]
									ballerine, babie = actTurn.attack(target=target,value = actTurn.dualCast.effects.power,icon =actTurn.dualCast.icon,area=actTurn.dualCast.effects.area,accuracy=300,use=actTurn.dualCast.effects.stat)
									actTurn.dualCast.decate(value=1)
									actTurn.refreshEffects()
									tempTurnMsg += "\n"+ballerine
									logs += ballerine
									deathCount += babie
								else:
									for cmpt in range(len(horoSkills)):
										if skillToUse.id == horoSkills[cmpt].id:
											for ent in tablEntTeam[actTurn.team]:
												for skilly in ent.skills:
													if type(skilly) == classes.skill and skilly.id == horoscope.id:
														allreadyhave = False
														for eff in ent.effects:
															if eff.effects.id == horoscopeEff[cmpt][0].id:
																allreadyhave = True
																break
														if not(allreadyhave):
															tempMsg = groupAddEffect(caster=actTurn, target=ent, area=[ent], effect=[horoscopeEff[cmpt][0]], skillIcon=skillToUse.emoji)
															tempMsg += groupAddEffect(caster=actTurn, target=actTurn, area=[actTurn], effect=[elemEff], skillIcon=skillToUse.emoji)
															logs += tempMsg
															tempTurnMsg += tempMsg
																
								try:				# Big raise
									if actTurn.stats.allieResurected - allyRea >= 3:
										if actTurn.char.says.bigRaise != None:
											tempTurnMsg += "\n{0} : *\"{1}\"*".format(actTurn.icon,actTurn.char.says.bigRaise.format(skill=skillToUse.name))
										tablReact = []
										for team in [0,1]:
											for ent in tablEntTeam[team]:
												if ent.hp > 0 and ent != actTurn and [ent.char.says.reactBigRaiseEnnemy,ent.char.says.reactBigRaiseAllie][ent.team == actTurn.team] != None and (ent not in ressurected[ent.team]):
													
													tablReact.append([ent.icon,randRep([ent.char.says.reactBigRaiseEnnemy,ent.char.says.reactBigRaiseAllie][ent.team == actTurn.team])])

										if len(tablReact) != 0:
											if len(tablReact) == 1:
												rand = 0
											else:
												rand = random.randint(0,len(tablReact)-1)
											tempTurnMsg += "\n{0} : *\"{1}\"*".format(tablReact[rand][0],tablReact[rand][1].format(caster=actTurn.char.name,skill=skillToUse.name))
								except:
									tempTurnMsg += "\n__Error with the BigRaisesReaction.__ See logs for more informations"
									logs += "\n"+format_exc()

								try:				# LB React
									if skillToUse.id == trans.id:
										tablReact = []
										for team in [0,1]:
											for ent in tablEntTeam[team]:
												if ent.hp > 0 and ent != actTurn and [ent.char.says.reactEnemyLb ,ent.char.says.reactAllyLb][ent.team == actTurn.team] != None:
													tablReact.append([ent.icon,randRep([ent.char.says.reactEnemyLb ,ent.char.says.reactAllyLb][ent.team == actTurn.team])])

										if len(tablReact) != 0:
											tablReact = randRep(tablReact)
											tempTurnMsg += "\n{0} : *\"{1}\"*".format(tablReact[0],tablReact[1].format(caster=actTurn.char.name,skill=skillToUse.name))
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

								try:
									actTurn.stats.actionUsed[tour].append(skillToUse.name)
								except KeyError:
									actTurn.stats.actionUsed[tour] = [skillToUse.name]

								if skillToUse.url != None: skillUrl = skillToUse.url
							if actTurn.stats.fullskip and optionChoice != OPTION_SKIP:
								actTurn.stats.fullskip = False

							if lunaQFEff != None and not(replay or (optionChoice == OPTION_MOVE and not(allReadyMove))):
								replay = True
								lunaUsedQuickFight += "\n"+lunaQFEff.decate(1)
								actTurn.refreshEffects()

							timeNow = (datetime.now(parisTimeZone) - nowStartOfTurn)/timedelta(microseconds=1000)
							logs += "Turn duration : {0} ms{1}\n ----------".format(timeNow,[" (Manual fighter)",""][int(actTurn.auto)])
							if timeNow > 500 and actTurn.auto:
								longTurn = True
								longTurnNumber.append({"turn":tour,"ent":actTurn.char.name,"duration":timeNow})
							if not(replay or (optionChoice == OPTION_MOVE and not(allReadyMove) and not(TRAIT_GIANTESS in actTurn.char.trait))):
								if actTurn.isNpc("Epiphyllum"):
									for ent in tablEntTeam[actTurn.team]:
										if ent.hp <= 0 and ent.status == STATUS_DEAD and ent.char.npcTeam == NPC_DRYADE:
											ballerine = await actTurn.resurect(ent,int(ent.maxHp*0.35),lifeSeed.emoji,danger)
											logs += ballerine
											tempTurnMsg += ballerine
								break
							else:
								replay, isCasting = False, False
								if optionChoice != OPTION_MOVE:
									hadReplayed = True
									for eff in actTurn.effects:
										if eff.effects.replica != None:
											isCasting = True
											break

								tempTurnMsg += lunaUsedQuickFight
								if optionChoice == OPTION_MOVE and not(allReadyMove) and not(TRAIT_GIANTESS in actTurn.char.trait):
									allReadyMove = True
									logs += "\n"

								if not(auto) and not(actTurn.auto):   # Sending the Turn message
									if len(tempTurnMsg) > 4000:
										tempTurnMsg = "Overload <:iliSip:1119011945157230692>"
									emby = interactions.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color)
									if skillUrl != None:
										emby.set_image(url=skillUrl)

									tried, cmpt, lenEmbeds = 0, 0, getEmbedLength(embInfo)+getEmbedLength(emby)
									while lenEmbeds > 5500:
										if tried == 0:
											finded = False
											for field in embInfo.fields:
												if cmpt < len(statEmbedFieldNames) and statEmbedFieldNames[cmpt] in field.name:
													field.value, finded, cmpt = "[...]", True, cmpt+1
													break
											if not(finded):
												tried += 1
										elif tried == 1:
											embInfo.description = "[...]"
											tried += 1
										elif tried == 2:
											emby.description = emby.description[lenEmbeds-5500:]
											if len(emby.description) > 4050:
												emby.description = emby.description[len(emby.description)-4050:]
											tried += 1
										elif tried == 3:
											tempTurnMsg = "__Tour de {0} :__".format(actTurn.name)
											if type(skillToUse) == classes.skill:
												tempTurnMsg = "\n__{0} utilise {1} {2} :__".format(actTurn.name, skillToUse.emoji, skillToUse.name)
											for team in [0,1]:
												for ent in tablEntTeam[team]:
													if type(ent.char) not in [classes.invoc, classes.depl]:
														entPAR = 0
														for eff in ent.effects:
															if eff.effects.overhealth > 0:
																entPAR += eff.value
														tempMsg = ""
														if statsTurnDict[ent.id]["par"] != entPAR:
															tempMsg += " {0}{1} PAr".format(["","+"][entPAR>statsTurnDict[ent.id]["par"]],entPAR-statsTurnDict[ent.id]["par"])
														if statsTurnDict[ent.id]["hp"] != ent.hp:
															tempMsg += " {0}{1} PV".format(["","+"][ent.hp>statsTurnDict[ent.id]["hp"]],ent.hp-statsTurnDict[ent.id]["hp"])
														if ent.hp <= 0:
															tempMsg += " (�)"
														if tempMsg != "":
															tempMsg = "\n{0} →".format(ent.icon)+tempMsg
														tempTurnMsg += tempMsg
											tempTurnMsg = reduceEmojiNames(tempTurnMsg)
											tried += 1
										else:
											emby.description = "OVERLOAD"
											break
										lenEmbeds = getEmbedLength(embInfo)+getEmbedLength(emby)
									nbTry = 0
									while 1:
										try:
											await msg.edit(embeds = [embInfo,emby],components=[infoSelect])
											break
										except aiohttp.ClientOSError:
											if nbTry < 5:
												await asyncio.sleep(1)
												nbTry += 1
												errorNb += 1
												logs += "\nConnexion error... retrying..."
											else:
												logs += "\nConnexion lost"
												raise

										await asyncio.sleep(1)

								for team in [0,1]:					  # Does a team is dead ?
									for ent in tablEntTeam[team]:
										if ent.hp > 0 and type(ent.char) not in [invoc, depl]:
											everyoneDead[team] = False
											break

								if everyoneDead[0] or everyoneDead[1]:  # If Yes, ending the fight
									fight = False
									break
					# ==========================================
					# Else, the entity is stun
					else:								   # The entity is, in fact, stun
						temp = f"\n{actTurn.char.name} est étourdi{actTurn.accord()} !\n"
						tempTurnMsg += temp
						logs += "{0} is stun\n".format(actTurn.name)
						optionChoice = OPTION_SKIP

					funnyTempVarName, ressurected = ["\n__Fin du tour__\n",""][type(actTurn.char) == classes.invoc]+actTurn.endOfTurn(danger), [[],[]]
					logs += funnyTempVarName

					tmpMsg = tempTurnMsg.splitlines()
					while tmpMsg[-1] == "":
						tmpMsg.pop()
					tempTurnMsg += funnyTempVarName

				if wasAlive and type(time.timeline[1].char) not in [classes.invoc]:
					tempTurnMsg = reduceEmojiNames(tempTurnMsg)
					if len(tempTurnMsg) > EMBED_MAX_DESC_LENGTH :
						tempTurnMsg = "__Tour de {0} :__".format(actTurn.name)
						if type(skillToUse) == classes.skill: tempTurnMsg = "\n__{0} utilise {1} {2} :__\n".format(actTurn.name, skillToUse.emoji, skillToUse.name)
						for team in [0,1]:
							for ent in tablEntTeam[team]:
								if type(ent.char) not in [classes.invoc, classes.depl]:
									entPAR = 0
									for eff in ent.effects:
										if eff.effects.overhealth > 0: entPAR += eff.value
									tempMsg = ""
									if statsTurnDict[ent.id]["par"] != entPAR: tempMsg += " {0}{1} PAr".format(["","+"][entPAR>statsTurnDict[ent.id]["par"]],entPAR-statsTurnDict[ent.id]["par"])
									if statsTurnDict[ent.id]["hp"] != ent.hp: tempMsg += " {0}{1} PV".format(["","+"][ent.hp>statsTurnDict[ent.id]["hp"]],ent.hp-statsTurnDict[ent.id]["hp"])
									if tempMsg != "": tempMsg = "\n{0} →".format(ent.icon)+tempMsg
									tempTurnMsg += tempMsg
						tempTurnMsg = reduceEmojiNames(tempTurnMsg)

					if not(auto):   # Sending the Turn message
						emby = interactions.Embed(title=f"__Tour {tour}__",description=tempTurnMsg,color = actTurn.char.color)
						if skillUrl != None: emby.set_image(url=skillUrl)

						tried, cmpt, lenEmbeds = 0, 0, getEmbedLength(embInfo)+getEmbedLength(emby)
						while lenEmbeds > 6000:
							if tried == 0:
								finded = False
								for field in embInfo.fields:
									if cmpt < len(statEmbedFieldNames) and statEmbedFieldNames[cmpt] in field.name:
										field.value, finded, cmpt = "[...]", True, cmpt+1
										break
								if not(finded):
									tried += 1
							elif tried == 1: embInfo.description = "[...]"; tried += 1
							elif tried == 2:
								emby.description = emby.description[lenEmbeds-EMBED_MAX_DESC_LENGTH:]
								if len(emby.description) > EMBED_MAX_DESC_LENGTH:emby.description = emby.description[len(emby.description)-EMBED_MAX_DESC_LENGTH:]
								tried += 1
							elif tried == 3:
								tempTurnMsg = "__Tour de {0} :__".format(actTurn.name)
								if type(skillToUse) == classes.skill:
									tempTurnMsg = "\n__{0} utilise {1} {2} :__".format(actTurn.name, skillToUse.emoji, skillToUse.name)
								for team in [0,1]:
									for ent in tablEntTeam[team]:
										if type(ent.char) not in [classes.invoc, classes.depl]:
											entPAR = 0
											for eff in ent.effects:
												if eff.effects.overhealth > 0:
													entPAR += eff.value
											tempMsg = ""
											if statsTurnDict[ent.id]["par"] != entPAR:
												tempMsg += " {0}{1} PAr".format(["","+"][entPAR>statsTurnDict[ent.id]["par"]],entPAR-statsTurnDict[ent.id]["par"])
											if statsTurnDict[ent.id]["hp"] != ent.hp:
												tempMsg += " {0}{1} PV".format(["","+"][ent.hp>statsTurnDict[ent.id]["hp"]],ent.hp-statsTurnDict[ent.id]["hp"])
											if ent.hp <= 0:
												tempMsg += " (�)"
											if tempMsg != "":
												tempMsg = "\n{0} →".format(ent.icon)+tempMsg
											tempTurnMsg += tempMsg
								tempTurnMsg = reduceEmojiNames(tempTurnMsg)
								tried += 1
							else: emby.description = "OVERLOAD"; break
							lenEmbeds = getEmbedLength(embInfo)+getEmbedLength(emby)

						nbTry = 0
						for cmpt in [0,1]:
							if len([embInfo,emby][cmpt].description) > 4096:
								[embInfo,emby][cmpt].description = "Overload mother fucker\nlen([embInfo,emby][cmpt].description) : {0}/4096".format(len([embInfo,emby][cmpt].description))
						while 1:
							try: await msg.edit(embeds = [embInfo,emby],components=[infoSelect]); break
							except SocketError as e:
								if e.errno not in [errno.ECONNRESET,503] or '503: Service Unavailable' not in e.__str__(): raise
								else:
									if nbTry < 5:
										await asyncio.sleep(1)
										nbTry += 1
										errorNb += 1
										logs += "\nConnexion error... retrying..."
									else: logs += "\nConnexion lost"; raise

						asyncSleepTimer = 1.8-([0,0.3][int(bigMap or not(allAuto) or (len(team2)>8 and actTurn.team))])+(min(len(tempTurnMsg),2250)/2250*5)+(1*int(skillUrl != None))

						# Sending turn msg
						reactHpSelect = None
						try: reactHpSelect = await bot.wait_for_component(messages=msg,components=infoSelect.components,check=checkHpComponent,timeout=asyncSleepTimer); reactHpSelect: ComponentContext = reactHpSelect.ctx
						except asyncio.TimeoutError: pass
						except asyncio.CancelledError: pass
						except:
							errorTxt = format_exc()
							if len(errorTxt) > EMBED_MAX_DESC_LENGTH: errorTxt = errorTxt[len(errorTxt)-EMBED_MAX_DESC_LENGTH:]
							try:
								if reactHpSelect != None: await reactHpSelect.send(embeds=Embed(title="<:aliceBoude:1179656601083322470> __Une erreur est survenue lors de l'envoie du message :__",description=errorTxt),ephemeral=True)
								else: await ctx.send(embeds=Embed(title="<:aliceBoude:1179656601083322470> __Une erreur est survenue lors de l'envoie du message :__",description=errorTxt),ephemeral=True)
							except: print_exc()
						else:
							await reactHpSelect.defer(ephemeral=True)

							tempEmbInfoChar, tempEmbInfoCharStatsTxt = entDict[int(reactHpSelect.values[0])], ""
							addMsg = ""
							for indx, tmpSkill in enumerate(tempEmbInfoChar.skills):
								if type(tmpSkill) == classes.skill: addMsg += "{0}{1}\n".format(str(tmpSkill).replace("__",""), [""," ({0})".format(tempEmbInfoChar.cooldowns[indx])][tempEmbInfoChar.cooldowns[indx]>0 and tmpSkill.initCooldown < 20])
								else: addMsg += " \-\n"
							addChipMsg = ""
							for indx, tmpChip in enumerate(tempEmbInfoChar.char.equippedChips):
								tmpChip = getChip(tmpChip)
								if tmpChip != None:
									toAff, chipVal = "", tempEmbInfoChar.chipAddInfo[indx]
									if chipVal != None and chipVal.__class__ != list: toAff = [int(chipVal),round(chipVal,2)][math.modf(chipVal)[0]>0]
									addChipMsg += "{0}{1}\n".format(tmpChip,[""," ({0})".format(toAff)][chipVal != None])
								elif tempEmbInfoChar.char.__class__ in [classes.char, classes.tmpAllie]:addChipMsg += ' \-\n'

							embInfoTemp = Embed(title="__{0}__ (Tour {1})".format(unhyperlink(tempEmbInfoChar.name), tour), description="__PVs :__ **{0}** / {1}".format(separeUnit(max(0,tempEmbInfoChar.hp)),separeUnit(tempEmbInfoChar.maxHp)),color=tempEmbInfoChar.char.color)
							embInfoTemp.add_field(name="<:em:866459463568850954>\n__Temps de rechargements__",value=reduceEmojiNames(addMsg),inline=True)
							if addChipMsg != "": embInfoTemp.add_field(name="<:em:866459463568850954>\n__Puces__",value=reduceEmojiNames(addChipMsg),inline=True)

							infoCharDmgUp, infoCharDefenseUp, infoCharArmor, effSumTxt, antConstVal = 0, 1, 0, "", 0
							for eff in tempEmbInfoChar.effects:
								if eff.effects.id in [dmgUp.id,dmgDown.id,lenaExSkill5e.id]: infoCharDmgUp += round((eff.effects.power * [1,-1][eff.effects.id == dmgDown.id]),1)
								elif eff.effects.id in [vulne.id,defenseUp.id]: infoCharDefenseUp = infoCharDefenseUp * (100 + (eff.effects.power * [1,-1][eff.effects.id == vulne.id]))/100
								elif eff.effects.overhealth > 0: infoCharArmor += eff.value
								elif eff.effects.id in [aconstEff.id, constEff.id]: antConstVal += (eff.value * [1,-1][eff.effects.id == aconstEff.id])
							infoCharDefenseUp = round((infoCharDefenseUp-1)*100,2)
							for cmpt in range(3):
								if [infoCharDmgUp, infoCharDefenseUp, infoCharArmor][cmpt] != 0: [infoCharDmgUp, infoCharDefenseUp, infoCharArmor][cmpt] = round([infoCharDmgUp, infoCharDefenseUp, infoCharArmor][cmpt],2); effSumTxt += "*{0} {1}{2}{3}* ".format([[dmgDown.emoji[0][1],dmgUp.emoji[0][0]][infoCharDmgUp>0],[vulne.emoji[0][1],defenseUp.emoji[0][0]][infoCharDefenseUp>0],["<a:transArmorB:900037831257358378>","<a:transArmorR:900037817449717800>"][tempEmbInfoChar.team]][cmpt],["-","+"][[infoCharDmgUp, infoCharDefenseUp, infoCharArmor][cmpt] >=0],abs([infoCharDmgUp, infoCharDefenseUp, infoCharArmor][cmpt]),["%"," PAr"][cmpt==2])
							constMsg = ["\n"," ({0} {1}{2})\n".format([aconstEff.emoji[0][0],constEff.emoji[0][0]][antConstVal>=0],["-","+"][antConstVal>=0],abs(antConstVal))][antConstVal != 0]
							embInfoTemp.description += constMsg + effSumTxt + ["","\n"][len(effSumTxt)>0] + "\n__**Liste des effets :**__\n" + tempEmbInfoChar.effectIcons()

							tempEmbInfoCharStats = tempEmbInfoChar.allStats()+[tempEmbInfoChar.resistance,tempEmbInfoChar.percing,round(probCritDmg(tempEmbInfoChar),1)]
							for statId in range(CRITICAL+1):
								if statId == RESISTANCE: tempEmbInfoCharStatsTxt += f"\n\n__Réduction de dégâts__ : {tempEmbInfoCharStats[statId]}%"
								elif statId == PERCING: tempEmbInfoCharStatsTxt += f"\n__Taux pénétration d'armure__ : {tempEmbInfoCharStats[statId]}%"
								elif statId == CRITICAL: tempEmbInfoCharStatsTxt += f"\n__Taux de coup critique__ : {min(tempEmbInfoCharStats[statId],80)}%"
								else:
									tempEmbInfoCharStatsTxt += f"\n{statsEmojis[statId]} __{allStatsNames[statId]}__ : **{tempEmbInfoCharStats[statId]}**"
									if tempEmbInfoChar.baseStats[statId] != tempEmbInfoCharStats[statId]: statDif = tempEmbInfoCharStats[statId]-tempEmbInfoChar.baseStats[statId]; tempEmbInfoCharStatsTxt += " *({2} {0} {1})*".format(["-","+"][statDif>0],abs(statDif),tempEmbInfoChar.baseStats[statId])

							embInfoTemp.description += "\n__**Statistiques :**__" + tempEmbInfoCharStatsTxt
							embInfoTemp.description = reduceEmojiNames(embInfoTemp.description)
							embInfoTemp.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.{1}?size=96&quality=lossless".format(getEmojiObject(tempEmbInfoChar.icon).id,["png","gif"][tempEmbInfoChar.icon[:3]=="<a:"]))
							await reactHpSelect.send(embeds=embInfoTemp)
					else: await asyncio.sleep(0.01)

					# POTG
					potgValue, tempPotgValue = (None,0), 0
					for team in (0,1):
						for ent in tablEntTeam[team]:
							try:
								potgDamages = (ent.stats.damageDeal-statsTurnDict[ent.id]["damage"])*0.7
								potgHeals = (ent.stats.heals-statsTurnDict[ent.id]["heal"])*0.6
								potgKills = (ent.stats.ennemiKill-statsTurnDict[ent.id]["kill"])*ent.char.level*10
								potgRaises = (ent.stats.allieResurected-statsTurnDict[ent.id]["raise"])*ent.char.level*15 
								potgArmor = (ent.stats.armoredDamage-statsTurnDict[ent.id]["armoredDamage"])*0.7
								tempPotgValue = potgDamages + potgHeals + potgKills + potgRaises + potgArmor + 200*int(optionChoice==OPTION_SKILL and skillToUse.ultimate) - (1000*int(type(actTurn.char)==octarien))
							except KeyError: pass
							if tempPotgValue > potgValue[1]: potgValue = (ent,tempPotgValue)
					if potgValue[1] > playOfTheGame[0]:
						embAllStats, embMsg = potgValue[0].allStats(), "{0} __{1}__ :".format(potgValue[0].icon,potgValue[0].name)
						statValue, statDif = None, None
						if optionChoice == OPTION_SKILL:
							if skillToUse.use == HARMONIE:
								maxValue, maxStats = 0, 0
								for cmpt in range(MAGIE+1):
									if embAllStats[cmpt] > maxValue: maxValue, maxStats = embAllStats[cmpt], cmpt
								statValue, statDif = maxStats, potgValue[0].allStats()[maxStats] - potgValue[0].baseStats[maxStats]
							elif skillToUse.use not in [None,FIXE,PURCENTAGE,MISSING_HP] and skillToUse.use < MAGIE+1: statValue, statDif = skillToUse.use, potgValue[0].allStats()[skillToUse.use] - potgValue[0].baseStats[skillToUse.use]
						elif optionChoice == OPTION_WEAPON: statValue, statDif = potgValue[0].char.weapon.use, potgValue[0].allStats()[potgValue[0].char.weapon.use] - potgValue[0].baseStats[potgValue[0].char.weapon.use]

						if statValue != None and statDif not in [None,0]: embMsg += " {0} {3} ({2}{1})".format(statsEmojis[statValue], statDif, ["","+"][statDif>0], potgValue[0].baseStats[statValue])
						dmgValue, effEmojis = 0, {}
						for eff in potgValue[0].effects:
							if eff.effects.id == dmgUp.id: dmgValue += eff.effects.power
							elif eff.effects.id == dmgDown.id: dmgValue -= eff.effects.power
							try: effEmojis[eff.icon] = effEmojis[eff.icon]+1
							except KeyError: effEmojis[eff.icon] = 1
						
						if dmgValue != 0: embMsg += " {0} {2}{1}%".format([dmgDown.emoji[0][1],dmgUp.emoji[0][0]][dmgValue>0],round(dmgValue),["","+"][dmgValue>0])
						ballerine:str = "\n"
						for em, value in effEmojis.items(): ballerine += "{0}{1}".format(em,["","({0})".format(value)][value>1])
						embMsg += ballerine

						potgEmb2 = Embed(description=embMsg,color=potgValue[0].char.color)
						if skillUrl != None: potgEmb = interactions.Embed(title=f"__Action du combat\nTour {tour}__",description=tempTurnMsg,color = potgValue[0].char.color); potgEmb.set_image(url=skillUrl); playOfTheGame = [potgValue[1],potgValue[0],potgEmb,potgEmb2]
						else: playOfTheGame = [potgValue[1],potgValue[0],interactions.Embed(title=f"__Action du combat\nTour {tour}__",description=tempTurnMsg,color = potgValue[0].char.color),potgEmb2]

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

					if time.timeline[1].hp <= 0: tempTurnMsg = ""
				# =========================================

				# End of the turn - timeline stuff ------------------------------------------------------------------
				actTurn.stats.hpPerTurn[tour], actTurn.stats.dmgPerTurn[tour], actTurn.stats.healPerTurn[tour], actTurn.stats.armorPerTurn[tour], actTurn.stats.suppPerTurn[tour] = max(actTurn.hp,0), actTurn.stats.damageDeal, actTurn.stats.heals+actTurn.stats.lifeSteal, actTurn.stats.shieldGived, actTurn.stats.damageBoosted+actTurn.stats.damageDodged+actTurn.stats.healReduced+actTurn.stats.healIncreased
				tablEntTeam,tablAliveInvoc,entDict = time.endOfTurn(tablEntTeam,tablAliveInvoc,entDict)

				for team in [0,1]:					  # Does a team is dead ?
					for ent in tablEntTeam[team]:
						if ent.hp > 0 and type(ent.char) not in [invoc, depl]:
							everyoneDead[team] = False
							break

				if everyoneDead[0] or everyoneDead[1]:  # If Yes, ending the fight
					fight = False

			# End of the fight ============================
			logs += "\n\n================= End of the fight ================="
		except Exception as e:
			print("> Une erreur est survenue sur le combat de {0} :".format(logsName))
			formExc = format_exc()
			print('>',formExc.splitlines()[-1],"\n> "+e.__str__())
			for team in listImplicadTeams:
				teamWinDB.changeFighting(team,0)
			if isLenapy and not(octogone):
				teamWinDB.refreshFightCooldown(mainUser.team,auto,fromTime=0)
			logs += "\n"+format_exc()

			desc = format_exc(limit=3000)
			desc = desc.replace("^","")
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

			logsButton = interactions.Button(style=2, label="Voir les logs", emoji=PartialEmoji(name="📄"),custom_id="📄")
			logsActRow = interactions.ActionRow(logsButton)

			try:
				msg = await ctx.send(content="{0} : Une erreur est survenue".format(ctx.author.mention),embeds=interactions.Embed(title=["Descriptif de l'erreur","Une erreur de communication prolongée est survenue"]["aiohttp.client_exceptions.ClientOSError" in logs],description=desc))
			except:
				msg = await ctx.channel.send(embeds=interactions.Embed(title=["Une erreur est survenue durant le combat","Une erreur de communication prolongée est survenue"]["aiohttp.client_exceptions.ClientOSError: [Errno 104] Connection reset by peer" in logs],description=desc))

			date = datetime.now(parisTimeZone)
			date = date.strftime("%H%M")
			fileName="ERROR_{0}_{1}.txt".format(logsName,date)
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
			opened.close()

			try:
				if threadChan != None:
					await threadChan.delete()
			except:
				pass

			haveError = True
			await msg.edit(content="{0} : Une erreur est survenue".format(ctx.author.mention),embeds=interactions.Embed(title=["Descriptif de l'erreur","Une erreur de communication prolongée est survenue"]["aiohttp.client_exceptions.ClientOSError: [Errno 104] Connection reset by peer" in logs],description=desc),components=[logsActRow])
			
			try:
				interact = await bot.wait_for_component(msg,timeout=[0,180][waitEnd])
				interact: ComponentContext = interact.ctx
			except asyncio.TimeoutError:
				await msg.edit(content="{0} : Une erreur est survenue".format(ctx.author.mention),embeds=interactions.Embed(title=["Descriptif de l'erreur","Une erreur de communication prolongée est survenue"]["aiohttp.client_exceptions.ClientOSError: [Errno 104] Connection reset by peer" in logs],description=desc), components=[])
				return msg

			if interact.custom_id == "📄":
				try:
					opened = open("./data/fightLogs/{0}".format(fileName),"rb")
					await ctx.channel.send("`Logs, {0} à {1}:{2}`".format(logsName,date[0:2],date[-2:]),files =interactions.File(file=opened, file_name=fileName))
					opened.close()
				except:
					try:
						await interact.send("Une erreur est survenue lors de l'affichage des logs :\n"+format_exc(1000),ephemeral=True)
					except:
						await interact.channel.send("Une erreur est survenue lors de l'affichage des logs :\n"+format_exc(1000),ephemeral=True)

		# ===============================================================================================
		#									   Post Fight Things
		# ===============================================================================================
		if not(haveError):
			nowTemp = datetime.now(parisTimeZone)
			print("[{0}:{1}:{2}] {3} a terminé son combat".format(nowTemp.hour,nowTemp.minute,nowTemp.second,logsName))
			startMsg, lootButtons, looted, dropedCards = globalVar.getRestartMsg() == 0 and waitEnd, [], [], {}

			if not(everyoneDead[1] and everyoneDead[0]): winners, nullMatch = int(not(everyoneDead[1])), False
			else: winners, nullMatch = 1, True

			if (octogone and team2[0].isNpc('Lena') and len(team2) == 1 and not(winners)):
				logs += mauvaisePerdante
				for team in listImplicadTeams:
					teamWinDB.changeFighting(team,0)
				logs += "\n"+format_exc()
				date = datetime.now(parisTimeZone)
				date = date.strftime("%H_%M")
				fileName ="{0}_{1}.txt".format(logsName,date)
				fich = open("./data/{0}".format(fileName),"w",encoding='utf-8')
				if not(isLenapy):
					try:
						fich.write(unemoji(logs))
					except:
						print_exc()

				else:
					fich.write(unemoji(logs))
				fich.close()
				opened = open("./data/{0}".format(fileName),"rb")

				try: msg: interactions.Message = await ctx.send("Une erreur est survenue durant le combat",files =interactions.File(file=opened))
				except: msg: interactions.Message = await ctx.channel.send("Une erreur est survenue durant le combat",files =interactions.File(file=opened))

				opened.close()
				os.remove("./data/{0}_{1}.txt".format(logsName,date))
				haveError = True

			else:			   # None Special fights, EXP, Gold and loot
				for z in (0,1):
					for a in tablEntTeam[z]:
						if type(a.char) == invoc: a.hp = 0

				tablEntTeam,tablAliveInvoc,entDict = time.endOfTurn(tablEntTeam,tablAliveInvoc,entDict)
				temp = tablEntTeam[0][:]+tablEntTeam[1][:]

				dptClass = sorted(temp,key=lambda student: student.stats.damageDeal,reverse=True)
				for a in dptClass[:]:
					if a.stats.damageDeal < 1: dptClass.remove(a)
				healClass = sorted(temp,key=lambda student: student.stats.heals,reverse=True)
				for a in healClass[:]:
					if a.stats.heals < 1: healClass.remove(a)
				shieldClass = sorted(temp,key=lambda student: student.stats.armoredDamage,reverse=True)
				for a in shieldClass[:]:
					if a.stats.shieldGived < 1: shieldClass.remove(a)
				suppClass = sorted(temp,key=lambda student: student.stats.damageBoosted + student.stats.damageDodged,reverse=True)
				for a in suppClass[:]:
					if a.stats.damageBoosted + a.stats.damageDodged < 1: suppClass.remove(a)

				listClassement = [dptClass,healClass,shieldClass,suppClass]

				tablSays = []
				temp = ["",""]
				endResultRep, teamWon, nbTeamMates, truePlayer = {}, {}, {}, 0
				for ent in tablEntTeam[0]:
					if type(ent.char) == char and ent.char.team == mainUser.team: truePlayer += 1
				for a in [0,1]:			 # Result msg character showoff
					for b in tablEntTeam[a]:
						raised, actIcon, icon = "", b.icon, await b.getIcon(bot)
						if b.status == STATUS_RESURECTED and b.raiser != None:
							raised = " ({1}{0})".format(b.raiser,['<:rezB:907289785620631603>','<:rezR:907289804188819526>'][b.team])
						elif b.status == STATUS_TRUE_DEATH and b.raiser != None:
							raised = " ({0})".format(['<:diedTwiceB:907289950301601843>','<:diedTwiceR:907289935663485029>'][b.team])

						addText = b.getMedals(listClassement)
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

						if b.char.standAlone:
							if a == 1 and winners and b.char.says.redWinAlive != None and b.hp > 0:
								for cmpt in (0,1,2,3,4,5): tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redWinAlive)]

							elif a == 1 and not(winners) and b.char.says.redLoose != None:
								for cmpt in (0,1,2,3): tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redLoose)]
						else:
							if a == 0 and not(winners) and b.char.says.blueWinAlive != None and b.hp > 0:
								for cmpt in (0,1): tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.blueWinAlive)]
							elif a == 0 and not(winners) and b.char.says.blueWinDead != None and b.hp <= 0: tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.blueWinDead)]
							elif a == 0 and winners and b.char.says.blueLoose != None: tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.blueLoose)]
							elif a == 1 and winners and b.char.says.redWinAlive != None and b.hp > 0:
								for cmpt in (0,1): tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redWinAlive)]
							elif a == 1 and winners and b.char.says.redWinDead != None and b.hp <= 0: tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redWinDead)]
							elif a == 1 and not(winners) and b.char.says.redLoose != None: tablSays += ["{0} : *\"{1}\"*".format(icon,b.char.says.redLoose)]

				say = ""
				if len(tablSays) > 0: say = "\n\n{0}".format(randRep(tablSays))
		
				duree = datetime.now(parisTimeZone)
				nowTemp = duree - now
				nowTemp = str(nowTemp.seconds//60) + ":" + str(nowTemp.seconds%60)

				if not(octogone):	   # Add the "next fight" field
					nextFigth = now + timedelta(hours=1+(2*auto))
					timecode = interactions.client.utils.timestamp_converter(nextFigth)
					timecode.format(TimestampStyles.RelativeTime)
					nextFightMsg = "\n__Prochain combat {0}__ : {1}".format(["normal","rapide"][auto],timecode.format(TimestampStyles.RelativeTime))
				else: nextFightMsg = ""

				if not(nullMatch): color = [[0x2996E5,0x00107D][danger<100],red][winners]
				else: color = 0x818181

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
						
						if len(temp2)>0 and temp2[-2:-1] != "\n":
							temp += temp2
						endResultRep[indexTeam] = temp

				for indexTeam in endResultRep:
					if teamWon[indexTeam]:
						resultEmbed.add_field(name="<:em:866459463568850954>\n__Vainqueurs :__",value=endResultRep[indexTeam],inline=True)
				for indexTeam in endResultRep:
					if not(teamWon[indexTeam]):
						resultEmbed.add_field(name="<:em:866459463568850954>\nPerdants :",value=endResultRep[indexTeam],inline=True)
				if footerText != "": resultEmbed.set_footer(text=footerText,icon_url=ctx.author.avatar_url)

				if longTurn: resultEmbed.set_footer(text="{0} tour{1} anormalement long{1} {2} été détecté{1} durant le combat. Un rapport va être envoyé".format(len(longTurnNumber),["",'s'][int(len(longTurnNumber) > 1)],["a","ont"][int(len(longTurnNumber) > 1)]))

				endOfFightStats = copy.deepcopy(tablEntTeam)
				for team in (0,1):
					for ent in endOfFightStats[team]:
						tempStr = str(ent.stats.__dict__).replace("'","")
						logs += "\n\n===== {0} [{2}] =====\n{1}".format(ent.name,tempStr,team)

				if procurFight != []:
					team1 = []
					for a in userTeamDb.getTeamMember(mainUser.team): team1 += [loadCharFile(absPath + "/userProfile/{0}.json".format(a))]

					tablEntTeam[0], cmpt = [], 0
					for user in team1: tablEntTeam[0].append(entity(cmpt,user,0,danger=danger,dictInteraction=dictIsNpcVar)); cmpt+=1

				# Gain rolls and defenitions -------------------------------------------------
				if not(octogone):
					gainExp, gainCoins, allOcta, gainMsg, listLvlUp = tour,tour*20,True,"", []
					# Base Exp Calculation
					for ent in tablEntTeam[1]:
						if type(ent.char) == octarien:
							if ent.hp <= 0:
								gainExp += ent.char.exp
								if ent.char.npcTeam == NPC_SALMON:
									gainCoins += 9
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
						if type(ent.char) == char:
							ent.char = loadCharFile(user=ent.char)
							veryLate = 1 + (int(maxLevel-ent.char.level > 10 and winners) * 0.5)
							if ent.char.level < MAXLEVEL:
								baseGain = gainExp+(ent.medals[0]*3)+(ent.medals[1]*2)+(ent.medals[2]*1)+int((maxLevel-ent.char.level)/2)
							else:
								baseGain = 0

							prestigeXpBoost = 1.5
							if ent.char.stars > 0:
								prestigeXpBoost = max(1+(XPBOOSTVALUE - (XPBOOSTVALUE / PRESTIGEXPBOOST * ent.char.level)) / 100, 1)

							effectiveExpGain = int(baseGain*(1+0.02*(min(10,maxLevel-ent.char.level)))*veryLate* prestigeXpBoost * (1+(maxLevlDiff <= 5 * 0.2)+(ent.auto*0.1)) // [1,2][winners or nullMatch or ent.char.team != mainUser.team])
							temp = (ent.char.level, ent.char.stars)

							ent.char = addExpUser(ent.char,exp=effectiveExpGain,coins=gainCoins)

							if (ent.char.level, ent.char.stars) != temp:
								listLvlUp.append("{0} : Niv. {1}{2} → Niv. {3}{4}\n".format(await ent.getIcon(bot),temp[0],["","<:littleStar:925860806602682369>{0}".format(temp[1])][temp[1]>0],ent.char.level,["","<:littleStar:925860806602682369>{0}".format(ent.char.stars)][ent.char.stars>0]))

							if effectiveExpGain > 0:
								gainMsg += "\n{0} → <:exp:926106339799887892> +{1}".format(await getUserIcon(bot,ent.char),effectiveExpGain)

							if baseGain != effectiveExpGain:
								logs += "\n{0} got ent {1}% exp boost (total : +{2} exp)".format(ent.char.name,int((effectiveExpGain/baseGain-1)*100),effectiveExpGain)

							userShop = userShopPurcent(ent.char)
							stuffRoll, skillRoll = constStuffDrop[userShop//10*10], constSkillDrop[userShop//10*10]
							if allOcta and ent.char.team == mainUser.team:			 # Loots
								if not(winners):
									if random.randint(0,99) < 30:
										probRarity, initRoll, rarity = (60,30,9,1), random.randint(0,99), RARITY_MYTHICAL
										for rarityRoll, proba in enumerate(probRarity):
											if initRoll < proba:
												usrIcon = await getUserIcon(bot,ent.char)
												gainMsg += ["\n{0} → ".format(usrIcon),", "][usrIcon in gainMsg]+"{0} {1}".format(rarityEmojis[rarityRoll],"Booster de puces "+["commun","rare","légendaire","mythique"][rarityRoll])
												dropedCards[ent.char] = [rarityRoll]
												break
											else:
												initRoll -= proba

									elif mainUser.owner == ent.char.owner and random.randint(0,99) < (20-(10*int(userShop>80))-(10*int(userShop>95))):
										aliceStatsDb.updateJetonsCount(mainUser,1)
										logs += "\n{0} ent obtenu un jeton de roulette".format(mainUser.name)
										usrIcon = await getUserIcon(bot,ent.char)
										if usrIcon in gainMsg:
											gainMsg += f", <:jtn:917793426949435402> Jeton de roulette"
										else:
											gainMsg += "\n{0} → <:jtn:917793426949435402> Jeton de roulette".format(usrIcon)
									
									if random.randint(0,99) < stuffRoll:				   # Drop Stuff
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
											
											if ent.char.owner == mainUser.owner:
												lootButtons.append(interactions.Button(style=ButtonStyle.SECONDARY,label=rand.name,emoji=getEmojiObject(rand.emoji),custom_id="loot_stuff_{0}".format(rand.id)))
												looted.append(rand)

										elif len(drop) == 0:
											gainTabl = [5,35,50,69,11,100,150,666,111,13,1,256,128,64,32]

											for comp in ent.skills+ent.char.stuff:							 # Dans toutes les compétences du personnage + ses équipementd
												if type(comp) == skill and comp.name == "Truc pas catho":	   # Si On sais quoi est équipé
													gainTabl = [69]											 # Tu peux gagner que 69 pièces
													break
												elif type(comp) == stuff and comp.name == "Tenue Provocante":   # Sinon, si On sait quoi 2 est équipé
													gainTabl = [69]											 # Tu peux gagner que 69 pièces aussi
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
												if ent.char.owner == mainUser.owner:
													lootButtons.append(interactions.Button(style=ButtonStyle.SECONDARY,label=rand.name,emoji=getEmojiObject(rand.emoji),custom_id="loot_skill_{0}".format(rand.id)))
													looted.append(rand)

										elif len(drop) == 0:
											gainTabl = [5,35,50,69,11,100,150,666,111,13,1,256,128,64,32]

											for comp in ent.skills+ent.char.stuff:							 # Dans toutes les compétences du personnage + ses équipements
												if type(comp) == skill and comp.name == "Truc pas catho":	   # Si On sais quoi est équipé
													gainTabl = [69]											 # Tu peux gagner que 69 pièces
													break
												elif type(comp) == stuff and comp.name == "Tenue Provocante":   # Sinon, si On sait quoi 2 est équipé
													gainTabl = [69]											 # Tu peux gagner que 69 pièces aussi
													break

											gain = gainTabl[random.randint(0,len(gainTabl)-1)]
											logs += " {0} pièces".format(gain)
											ent.char.currencies += gain
											saveCharFile(user=ent.char)
											if await getUserIcon(bot,ent.char) in gainMsg:
												gainMsg += f", {gain} <:coins:862425847523704832>"
											else:
												gainMsg += "\n{0} → {1} <:coins:862425847523704832>".format(await getUserIcon(bot,ent.char),gain)

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

											for comp in ent.skills+ent.char.stuff:							 # Dans toutes les compétences du personnage + ses équipementd
												if type(comp) == skill and comp.name == "Truc pas catho":	   # Si On sais quoi est équipé
													gainTabl = [69]											 # Tu peux gagner que 69 pièces
													break
												elif type(comp) == stuff and comp.name == "Tenue Provocante":   # Sinon, si On sait quoi 2 est équipé
													gainTabl = [69]											 # Tu peux gagner que 69 pièces aussi
													break

											gain = gainTabl[random.randint(0,len(gainTabl)-1)]
											logs += " {0} pièces".format(gain)
											ent.char.currencies += gain
											saveCharFile(user=ent.char)
											if await getUserIcon(bot,ent.char) in gainMsg:
												gainMsg += f", {gain} <:coins:862425847523704832>"
											else:
												gainMsg += "\n{0} → {1} <:coins:862425847523704832>".format(await getUserIcon(bot,ent.char),gain)

					for team in [0,1]:
						for ent in endOfFightStats[team]:
							if type(ent.char) != char:
								tmpChar = copy.deepcopy(ent.char)
								if type(tmpChar) == classes.tmpAllie: tmpChar.name += ["_B", "_R"][ent.team]
								aliceStatsDb.addEnemyStats(enemy=tmpChar, tablStats=ent.stats, winner=winners==ent.team)
							else: aliceStatsDb.addStats(user=ent.char,stats=ent.stats)

					gainMsg = reduceEmojiNames(gainMsg)
					if len(gainMsg)>EMBED_FIELD_VALUE_LENGTH:
						gainMsg = gainMsg.replace("<:ex:926106339799887892>","XP")
					if len(gainMsg)>EMBED_FIELD_VALUE_LENGTH:
						gainMsg = completlyRemoveEmoji(gainMsg)
					resultEmbed.add_field(name="<:em:866459463568850954>\n__Gains de l'équipe joueur :__",value = gainMsg,inline=False)

					if listLvlUp != []:
						temp = ""
						for a in listLvlUp:
							temp+=a
						tmpEmb = interactions.Embed(title="__Montée de niveau__",color=light_blue)
						tmpEmb.add_field(name="Le{0} personnage{0} suivant{0} {1} monté de niveau !".format(["","s"][len(listLvlUp)>1],["a","ont"][len(listLvlUp)>1]), value=reduceEmojiNames(temp))
						try:
							await ctx.respond(embeds=tmpEmb)
						except:
							await ctx.channel.send(embeds=tmpEmb)

				if errorNb > 0: resultEmbed.add_field(name="<:em:866459463568850954>\nDebugg :",value="{0} erreurs de connexions ont survenu durant ce combat",inline=False)

			if not(haveError):
				try:
					try:
						if threadChan != None: await threadChan.delete()
					except: pass
					if startMsg: await msg.edit(embeds = resultEmbed,components=[interactions.ActionRow(interactions.Button(style=2, label="Chargement...", emoji=getEmojiObject('<a:loading:862459118912667678>'), custom_id="📄",disabled=True))])
					else: await msg.edit(embeds = resultEmbed,components=[])
				except:
					if startMsg: await ctx.channel.send(embeds = resultEmbed,components=[interactions.ActionRow(interactions.Button(style=2, label="Chargement...", emoji=getEmojiObject('<a:loading:862459118912667678>'), custom_id="📄",disabled=True))])
					else: await ctx.channel.send(embeds = resultEmbed,components=[])
				if not(octogone):
					for team in listImplicadTeams: teamWinDB.changeFighting(team,0)
			# ------------ Succès -------------- #
			if not(octogone):
				dictHadSucced, marineDealer, errorList, achivTabl = {}, 0, "", achiveTabl()

				def addSuccedtoDict(ent:entity,code:str):
					try: dictHadSucced[code].append(ent)
					except KeyError: dictHadSucced[code] = [ent]

				for ent in tablEntTeam[1]:
					if ent.char.npcTeam == NPC_MARINE and ent.hp < 0: marineDealer += 1
				for team in [0,1]:
					for ent in tablEntTeam[team]:
						if type(ent.char) == char and ent.char.team == mainUser.team:
							achivements = achivementStand.getSuccess(ent.char)
							for cmpt in range(len(tablAchivNpcName)):
								if dictIsNpcVar["{0}".format(tablAchivNpcName[cmpt])]: # Temp or enemy presence accuracys
									ent.char, succed = await achivements.addCount(ctx,ent.char,tablAchivNpcCode[cmpt])
									if succed: addSuccedtoDict(ent, tablAchivNpcCode[cmpt])

							achivmentsCodes = ["greatHeal","greatDps","poison","estialba","lesath",achivements.masterTank.code,achivements.masterDamage.code,achivements.marineDealer.code,"school"] 
							achivmentsStat = [ent.stats.heals,ent.stats.damageDeal-ent.stats.indirectDamageDeal,ent.stats.indirectDamageDeal,int(ent.stats.estialba),int(ent.stats.bleeding),ent.stats.damageRecived/ent.maxHp,ent.stats.damageDeal/ent.maxHp,marineDealer,1]
							achivConds = {"elemental":ent.char.level,"dangerous":not(winners) and ent.healResist >= 80 and ent.hp > 0,"still":not(winners) and ent.stats.fullskip,"loose":winners and danger == (dangerLevel[0] + (starLevel * DANGERUPPERSTAR)),"ailill":ent.stats.headnt,"suffering":ent.stats.sufferingFromSucess,"kiku2":ent.stats.lauthingAtTheFaceOfDeath,"fratere":ent.stats.friendlyfire,"quickFight":auto and int(ctx.author.id) == int(ent.char.owner),"dimentio":ent.char.level >= 20,"dirty":ent in dptClass[:3] and ent.stats.indirectDamageDeal == ent.stats.damageDeal,"delegation":ent == dptClass[0] and ent.stats.ennemiKill == 0,achivements.convicStar1.code:hadLb4,achivements.convicStar2.code:hadLb4,achivements.convicStar3.code:hadLb4,"fullDark":dictIsNpcVar["Luna"] or dictIsNpcVar["Shihu"],"lightNShadow":dictIsNpcVar["Iliana"] and (dictIsNpcVar["Luna"] or dictIsNpcVar["Shihu"]),"fight":type(ent.char) == char and ent.char.team == mainUser.team}
							for indx, achivCode in enumerate(achivmentsCodes):
								try:
									ent.char, succed = await achivements.addCount(ctx,ent.char,achivCode,achivmentsStat[indx])
									if succed: addSuccedtoDict(ent,achivCode)
								except Exception as e: errorList += "{0} : {1}:{2} ({3})\n".format(ent.name,achivCode,indx,e)

							for key, valid in achivConds.items():
								if valid:
									try:
										ent.char, succed = await achivements.addCount(ctx,ent.char,key)
										if succed: 
											addSuccedtoDict(ent,key)
											tablReward = []
											for reward in achivTabl.where(key).recompense:
												if reward == tripleCommunCards.id: tablReward += [0]*3
												elif reward == singleRareCards.id: tablReward += [1]

											if ent.char in dropedCards.keys(): dropedCards[ent.char] += tablReward
											else: dropedCards[ent.char] = tablReward
									except Exception as e: errorList += "{0} : {1} ({2})\n".format(ent.name,achivCode,e)

				for achivKey, achivValue in dictHadSucced.items():
					achiv, desc, lenAchivValue = achivTabl.where(achivKey), "", len(achivValue)
					if lenAchivValue == 1: desc = "__{0}__ a terminé le succès __{1}__ !".format(achivValue[0],achiv.name)
					else:
						for cmpt in range(lenAchivValue):
							desc += "__{0}__".format(achivValue[cmpt])
							if cmpt == lenAchivValue-2: desc += " et "
							elif cmpt < lenAchivValue-2: desc += ", "
						desc += " ont terminé le succes __{0}__ !".format(achiv.name)
					listRecompense = ""
					if achiv.recompense not in [None,[],[None]]:
						listRecompense = "\n\n__Récompense{0} :__\n".format(["","s"][len(achiv.recompense)>1])
						for objId in achiv.recompense:
							try:
								objType = whatIsThat(objId)
								match objType:
									case 0: objId = findWeapon(objId)
									case 1: objId = findSkill(objId)
									case 2: objId = findStuff(objId)
									case 3: objId = findOther(objId)
								if type(objId) != str: 
									listRecompense += "{0} {1}\n".format(objId.emoji, objId.name)
									if type(objId) not in [other]: listRecompense += objId.getSummary()+"\n"
								else: listRecompense += "?? \"{0}\"\n".format(objId)
							except Exception as e: listRecompense += "?? \"{0}\"\n> {1}\n".format(objId,e)
					await ctx.channel.send(embeds=Embed(title="{0} __{1}__".format(["",str(achiv.emoji)+" "][achiv.emoji != None], achiv.name),description=desc+listRecompense,color=mainUser.color))

				if errorList != "": await ctx.channel.send(embed=Embed(title="Some achivements had encounter a error :",description=errorList,color=red))

			timeout = False
			date, actuTeam, actuEntity, started, prec = datetime.now(parisTimeZone),0,0,False,None
			date, logsName, listFields = date.strftime("%H%M"), logsName.replace("/","_"), []

			if dropedCards != {}:
				for character in dropedCards:
					usr = loadCharFile(character.owner)
					usr, tempMsg = openBooster(user=usr, boosters = dropedCards[character])
					saveCharFile(user=usr)
					tmpField = EmbedField(name="{0} __{1}__".format(await getUserIcon(bot,usr),usr.name),value=tempMsg)
					if len(dropedCards[character]) == 1: tmpField.name += " (Booster {})".format(["Commun","Rare","Légendaire","Mythique"][dropedCards[character][0]])
					
					if usr.owner == int(ctx.author_id): 
						try: await msg.reply(embeds=Embed(title="__Booster de puces :__\n",color=usr.color,fields=[tmpField]))
						except: tmpField.name = ["","<:em:866459463568850954>\n"][len(listFields)>0]+tmpField.name; listFields.append(tmpField)
					else: tmpField.name = ["","<:em:866459463568850954>\n"][len(listFields)>0]+tmpField.name; listFields.append(tmpField)

			try:
				fich = open("./data/fightLogs/{0}_{1}.txt".format(logsName,date),"w",encoding='utf-8')
				try: fich.write(unemoji(logs))
				except: print_exc()
				fich.close()
			except: print_exc()

			if not(octogone): teamWinDB.addResultToStreak(mainUser,not(everyoneDead[0]))
			if isLenapy and not(octogone): teamWinDB.refreshFightCooldown(mainUser.team,auto,fromTime=now)

			if longTurn:
				for team in listImplicadTeams: teamWinDB.changeFighting(team,0)
				logs += "\n"+format_exc()
				date = datetime.now(parisTimeZone).strftime("%H%M")
				fileName = "{0}_{1}.txt".format(logsName,date)
				fich = open("./data/fightLogs/{0}".format(fileName),"w",encoding='utf-8')
				try: fich.write(unemoji(logs))
				except: print_exc()
				fich.close()

			logsPotgActionRow: interactions.ActionRow = interactions.ActionRow(interactions.Button(style=2, label="Voir les logs", emoji=PartialEmoji(name="📄"),custom_id="📄"))
			potg:List[ActionRow] = []
			potgMsg, potgIcon, precId = None, None, None

			if playOfTheGame[1] != None:
				try: potgIcon = await playOfTheGame[1].getIcon(bot); logsPotgActionRow.add_component(interactions.Button(style=2, label="Action du combat", emoji=getEmojiObject(potgIcon),custom_id="potg"))
				except: pass

			if lootButtons != []:
				lootActRow = []
				for but in lootButtons:
					if lootActRow == []: lootActRow = [interactions.ActionRow(but)]
					else: lootActRow[0].add_component(but)
			else: lootActRow = []

			if len(listFields) > 0:
				tmpButton = interactions.Button(label="Voir Puces",style=ButtonStyle.GRAY,custom_id="showChip")
				if lootActRow == []:
					lootActRow = [interactions.ActionRow(tmpButton)]
				else:
					lootActRow[0].add_component(tmpButton)

			showedGraph = False
			if notify:
				try: await ctx.send(content="{0}, votre combat est terminé".format(ctx.author.mention),ephemeral=True)
				except: 
					try:await ctx.author.user.send(content="Votre combat {2} est terminé ({1})".format(ctx.author.mention, msg.jump_url, ["normal","rapide"][auto]),ephemeral=True)
					except: ctx.channel.send(content="{0}, votre combat est terminé ({1})".format(ctx.author.mention, msg.jump_url))

			while startMsg: # Tableau des statistiques
				options = []
				for team in [0,1]:
					for num in range(len(endOfFightStats[team])):
						ent = endOfFightStats[team][num]
						options.append(interactions.StringSelectOption(label=ent.name,value="{0}:{1}".format(team,num),emoji=getEmojiObject(await ent.getIcon(bot)),default=started and team == actuTeam and num == actuEntity))

				select = interactions.StringSelectMenu(options,custom_id = "seeFighterStats", placeholder="Voir les statistiques d'un combattant")

				await msg.edit(embeds = resultEmbed, components=[interactions.ActionRow(select),logsPotgActionRow]+lootActRow)

				precTabl = [[],[prec]][prec != None]
				try: interact = await bot.wait_for_component(messages=[msg]+precTabl,timeout=[0,180][waitEnd]); interact: ComponentContext = interact.ctx
				except asyncio.TimeoutError:
					await msg.edit(embeds = resultEmbed, components=[])
					if prec != None: await prec.delete()
					break
				except asyncio.exceptions.CancelledError:
					resultEmbed.set_footer(text="Btw, got cancelled <:aliceBoude:1179656601083322470>")
					await msg.edit(embeds = resultEmbed, components=[])
					if prec != None: await prec.delete()
					break
					

				if interact.component_type == ComponentType.BUTTON:
					match interact.custom_id:
						case "📄":
							try:
								await interact.defer()
							except:
								pass
							try:
								fileName = "{0}_{1}.txt".format(logsName,date)
								opened = open("./data/fightLogs/{0}".format(fileName),"rb")
								await interact.send("`Logs, {0} à {1}:{2}`".format(logsName,date[0:2],date[-2:]),files=interactions.File(file=opened, file_name=fileName))
								opened.close()
							except:
								try:
									await interact.send("Une erreur est survenue lors de l'affichage des logs :\n"+format_exc(1000),ephemeral=True)
								except:
									await interact.channel.send("Une erreur est survenue lors de l'affichage des logs :\n"+format_exc(1000),ephemeral=True)
						case getHpButton.custom_id:
							await interact.defer(ephemeral=True)
							try:
								highestHp, labelList, dataList, highestTurn, dmgList, healList, armorList, suppList, showedGraph = 0, [], [], 0, [], [], [], [], True
								for key, value in actu.stats.hpPerTurn.items():
									highestTurn = key

									highestHp = max(highestHp, value, actu.stats.dmgPerTurn[key], actu.stats.healPerTurn[key], actu.stats.armorPerTurn[key], actu.stats.suppPerTurn[key])
									skillUsedNames = ""
									try:
										for skillName in actu.stats.actionUsed[key]:
											if len(skillName) > 10:
												tempSkillName = ""
												for txt in skillName.split(" "):
													if len(txt) == 2:
														pass
													elif len(txt) > 5:
														tempSkillName += txt[:4]+". "
													else:
														tempSkillName += txt+" "
												skillUsedNames += tempSkillName+"\n"
											else:
												skillUsedNames += skillName+"\n"
									except KeyError:
										skillUsedNames = "-"

									labelList.append("T{0}".format(key)+"\n"+skillUsedNames)
									dataList.append(value)
									dmgList.append(actu.stats.dmgPerTurn[key])
									healList.append(actu.stats.healPerTurn[key])
									armorList.append(actu.stats.armorPerTurn[key])
									suppList.append(actu.stats.suppPerTurn[key])

								color = hex(actu.char.color).replace("0x", "#")
								if color == "None":
									color = hex(light_blue).replace("0x", "#")
								if int(color[1:3],16)>200 and int(color[3:5],16)>200 and int(color[5:],16)>200:
									color = "#191919"
								qc = quickchart.QuickChart()
								qc.width, qc.height, qc.device_pixel_ratio = 350+(highestTurn*70), 700, 1.5
								qc.config = {"type": "line","data": {"labels": labelList,"datasets": [
									{"label": "Dégâts","data":dmgList,"borderColor":"rgb(235, 55, 55)","backgroundColor":"rgba(235, 100, 100, 0.2)","fill":actu.char.aspiration in [BERSERK,TETE_BRULEE,POIDS_PLUME,ENCHANTEUR,OBSERVATEUR,ATTENTIF,SORCELER,MAGE]},
									{"label": "Soins","data":healList,"borderColor":"rgb(200, 200, 55)","backgroundColor":"rgba(230, 230, 100, 0.2)","fill":actu.char.aspiration in [ALTRUISTE,VIGILANT]},
									{"label": "Armure","data":armorList,"borderColor":"rgb(100, 200, 55)","backgroundColor":"rgba(100, 230, 100, 0.2)","fill":actu.char.aspiration in [PREVOYANT,PROTECTEUR]},
									{"label": "Supp","data":suppList,"borderColor":"rgb(200, 55, 200)","backgroundColor":"rgba(230, 100, 230, 0.2)","fill":actu.char.aspiration in [IDOLE,INOVATEUR,MASCOTTE]},

									]},
									"options":{
										"title":{"display": True, "text":"Graphiques de {0}".format(actu.name),"fontSize":40},
										"scales":{"xAxes":[{"ticks":{"fontStyle":"bold"},"scaleLabel":{"display":True,"labelString":"Tours","fontSize":40}}]},
										
									}}


								qc2 = quickchart.QuickChart()
								qc2.width, qc2.height, qc2.device_pixel_ratio = 350+(highestTurn*70), 700, 1.5
								qc2.config = {"type": "line","data": {"labels": labelList,"datasets": [
									{"label": "PVs","data": dataList,"borderColor":color,"backgroundColor":color+"50"}
									]},
									"options":{
											"title":{"display": True, "text":"Graphiques de {0} (PVs)".format(actu.name),"fontSize":40},
											"scales":{"xAxes":[{"ticks":{"fontStyle":"bold"},"scaleLabel":{"display":True,"labelString":"Tours","fontSize":40}}]},
										}}
								await interact.send(content="[Graphiques]({0}) [de]({3}) {1} {2}".format(qc.get_short_url(),actu.icon,actu.name,qc2.get_short_url()))
							except:
								await interact.send(embeds=Embed(title="Une erreure est survenue",description=format_exc()))
						case "potg":
							playOfTheGame[2].set_footer(icon_url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(potgIcon).id),text="Action du combat")
							try:
								try:
									potgMsg = await interact.send(embeds = [playOfTheGame[3],playOfTheGame[2]])
								except:
									potgMsg = await interact.channel.send(embeds = [playOfTheGame[3],playOfTheGame[2]])
							except:
								try:
									potgMsg = await interact.send(embeds = [playOfTheGame[2]])
								except:
									potgMsg = await interact.channel.send(embeds = [playOfTheGame[2]])
							logsPotgActionRow.components[1].disabled = True
						case "showChip":
							while len(listFields) > 0 :
								nbFields = min(6,len(listFields))
								try:
									await interact.send(embeds=Embed(title="__Booster de puces :__",color=[light_blue,usr.color][len(listFields) == 1],fields=listFields[:nbFields]))
								except:
									nbFields = min(4,len(listFields))
									await interact.send(embeds=Embed(title="__Booster de puces :__",color=[light_blue,usr.color][len(listFields) == 1],fields=listFields[:nbFields]))
								listFields = listFields[nbFields:]

							for tmpComp in lootActRow:
								if tmpComp.custom_id == interact.custom_id:
									tmpComp.disabled = True
									break
						case _:
							try:
								await interact.defer()
								obj, lootEmb = None, None
								for truc in looted:
									if interact.custom_id.endswith(truc.id):
										obj = truc
										for cmpt in range(len(lootActRow[0].components)):
											if lootActRow[0].components[cmpt].custom_id == interact.custom_id:
												lootActRow[0].components[cmpt].disabled = True
												break
										break
								if obj != None:
									if type(obj) == classes.weapon:
										lootEmb = infoWeapon(weap=obj, user=mainUser, ctx=ctx)
									elif type(obj) == classes.stuff:
										lootEmb = infoStuff(stuff=obj, user=mainUser, ctx=ctx)
									elif type(obj) == classes.skill:
										lootEmb = infoSkill(skill=obj, user=mainUser, ctx=ctx)

									if lootEmb != None:
										try:
											await interact.send(embeds=lootEmb)
										except:
											await interact.channel.send(embeds=lootEmb)
									else:
										await interact.send(content="L'objet recherché n'a pas été trouvé",ephemeral=True)
								else:
									await interact.send(content="L'objet recherché n'a pas été trouvé",ephemeral=True)
							except:
								pass

				else:
					if prec == None:
						await interact.defer()
					else:
						try:
							showedGraph = precId == actu.id
							precId = actu.id
						except:
							print_exc()
					inter = interact.values[0]
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
						await prec.edit(embeds = await getResultScreen(bot,actu),components=[ActionRow([getHpButton,getHpButtonD][actu.id == precId or showedGraph])])
					else:
						try:
							prec = await interact.send(embeds = await getResultScreen(bot,actu),components=[ActionRow(getHpButton)])
						except:
							prec = await interact.channel.send(embeds = await getResultScreen(bot,actu),components=[ActionRow(getHpButton)])
					started = True
			return msg
	except:
		emby = interactions.Embed(title="__Uncatch error raised__",description=format_exc(limit=3000).replace("*",""))
		try:
			if footerText != "": emby.set_footer(text=footerText,icon_url=ctx.author.avatar_url)
		except: pass
		if msg == None: msg = await ctx.channel.send(embeds=emby,components=[])
		else: await msg.edit(embeds=emby,components=[])
		try:
			if threadChan != None: await threadChan.delete()
		except: pass

		teamWinDB.changeFighting(mainUser.team,0)
		return msg