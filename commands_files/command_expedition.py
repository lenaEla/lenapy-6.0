from datetime import datetime
import interactions
from gestion import *
from advance_gestion import *
from classes import char
from typing import List
from advObjects.advAllies import *

listLocations, dictLocations = ["la Forêt","l'Académie de Magie","l'Académie d'Escrime","les Ruines du Centre Commercial","les Ruines de l'Ecole","la Mine"], {}
LOC_FOREST, LOC_MAGICSCHOOL, LOC_SWORDSCHOOL, LOC_RUINEDMALL, LOC_RUINEDSCHOOL, LOC_MINE = tuple(range(len(listLocations)))
listLocationDescriptions = ["Augmente l'expérience reçue durant l'exploration","Augmente la probabilité d'obtenir des compétences psychiques","Augmente la probabilité d'obtenir des compétences physiques","Augmente la probabilité d'obtenir des équipements","Augmente la probabilité d'obtenir des cartes à jouer ou des puces","Augmente le nombre de pièces obtenues"]
for indx in range(len(listLocations)): dictLocations[indx] = listLocations[indx]
basicRoll = {"chip":5,"stuff":15,"skill":15,"tc":10,"weapon":5}

FIRSTINTER, SECONDINTER, THIRDINTER, FORTHINTER = 20, 15, 12, 10
durationCounters = [60*60,60*60*2,60*60*2,-1]

async def explorationReturn(bot: interactions.Client, team: List[char], duration:int, location:int):
	maxCmpt, fieldList, successfulRoll = 0, [], 0

	for indx, durLimit in enumerate(durationCounters):
		if durLimit == -1 and duration > 0: maxCmpt += duration // (FORTHINTER*60)
		elif duration > 0:
			tmp = min(durLimit,duration)
			maxCmpt += tmp // ([FIRSTINTER, SECONDINTER, THIRDINTER][indx] * 60)
			duration -= tmp

	maxCmpt = int(min(maxCmpt, 200))

	for tmpChar in team:
		tmpChar, charStamina, listLoot, cmpt, basicCopy, basicKeys, successfulRoll, lootTabl = loadCharFile(user=tmpChar), 100, {"exp":0, "gold":0, "tc":0, "loot":"", "chip":""}, 0, copy.deepcopy(basicRoll), basicRoll.keys(), 0, {"stuff":[], "skill": [], "weapon": []}
		match location:
			case 3: basicCopy["stuff"] += 10
			case 4: basicCopy["tc"] += 5
		while cmpt < maxCmpt:
			cmpt += 1
			if random.randint(0,99) < charStamina:
				charStamina, totalRollRange, rollValue, finded, successfulRoll = charStamina-5, 0, random.randint(0,99), False, successfulRoll+1
				for tmpKey in basicCopy: totalRollRange += basicCopy[tmpKey]
				for tmpKey in basicKeys:
					if rollValue < basicCopy[tmpKey]:
						match tmpKey:
							case "chip":
								chipRarity, rdmRoll, rarity = [[50,35,14,1],[40,39,20,1]][location == 4], random.randint(0,99), RARITY_MYTHICAL
								for rar in range(4):
									if rdmRoll < chipRarity[rar]: rarity = rar; break
									else: rdmRoll -= chipRarity[rar]

								rolledChip = randRep([chipCommun,chipRare,chipLegend,chipMythic][rarity])
								toAddChip = max(int(nbChipsForLvlUp[tmpChar.chipInventory[rolledChip.id].lvl-rarityMinLvl[tmpChar.chipInventory[rolledChip.id].rarity]]*0.05),[5,3,1,1][rolledChip.rarity])
								tmp, tmpChar = tmpChar.chipInventory[rolledChip.id].addProgress(toAddChip,tmpChar)
								listLoot["chip"] += "{0}*{1}* x**{2}**\n".format(rolledChip.emoji+[""," "][rolledChip.emoji != ""],rolledChip.name,toAddChip)
							case "stuff":
								if lootTabl["stuff"] == []:
									lootTabl["stuff"] = stuffs[:]
									for tmpStuff in stuffs:
										if (tmpChar.have(tmpStuff) and random.randint(0,9) < 9) or tmpStuff.price == 0: lootTabl["stuff"].remove(tmpStuff)
								pulledStuff: stuff = randRep(lootTabl["stuff"])
								if tmpChar.have(pulledStuff): listLoot["exp"] += 25
								else: tmpChar.stuffInventory.append(pulledStuff); listLoot["loot"] += "{0}\n".format(pulledStuff)
							case "weapon":
								if lootTabl["weapon"] == []:
									lootTabl["weapon"] = weapons[:]
									for tmpWeapon in weapons:
										if (tmpChar.have(tmpWeapon) and random.randint(0,9) < 9) or tmpWeapon.price == 0: lootTabl["weapon"].remove(tmpWeapon)
								pulledStuff: weapon = randRep(lootTabl["weapon"])
								if tmpChar.have(pulledStuff): listLoot["exp"] += 25
								else: tmpChar.weaponInventory.append(pulledStuff); listLoot["loot"] += "{0}\n".format(pulledStuff)
							case "skill":
								if lootTabl["skill"] == []:
									lootTabl["skill"] = skills[:]
									for tmpSkill in skills:
										if (tmpChar.have(tmpSkill) and random.randint(0,9) < 9) or tmpSkill.price == 0: lootTabl["skill"].remove(tmpSkill)
									for tmpSkill in lootTabl["skill"][:]:
										if (tmpSkill.use in [STRENGTH,AGILITY,PRECISION,ENDURANCE] and location == LOC_SWORDSCHOOL) or (tmpSkill.use in [CHARISMA,INTELLIGENCE,MAGIE] and location == LOC_MAGICSCHOOL): lootTabl["skill"].append(tmpSkill)
								pulledStuff: skill = randRep(lootTabl["skill"])
								if tmpChar.have(pulledStuff): listLoot["exp"] += 25
								else: tmpChar.skillInventory.append(pulledStuff); listLoot["loot"] += "{0}\n".format(pulledStuff)
							case "tc": listLoot["tc"] += random.randint(5,10)
						finded = True
						break
					else: rollValue -= basicCopy[tmpKey]
				if not(finded): listLoot[["exp","gold"][random.randint(0,99)<50]] += random.randint(25,50)
				if charStamina <= 0: break
		if location == LOC_FOREST: listLoot["exp"] = int(listLoot["exp"]*1.25)
		elif location == LOC_MINE: listLoot["gold"] = int(listLoot["gold"]*1.25)
		tmpChar = addExpUser(tmpChar,exp=listLoot["exp"],coins=listLoot["gold"])
		saveCharFile(user=tmpChar)

		fieldList.append(EmbedField(name=reduceEmojiNames("{0} __{1}__ ({2} / {3}) :".format(await getUserIcon(bot, tmpChar), tmpChar.name, successfulRoll, min(maxCmpt,20))),value=reduceEmojiNames("{1} {0}, {3} {2}, {5} {4}\n{6}{8}{7}".format("<:exp:926106339799887892>",listLoot["exp"],"<:coins:862425847523704832>",listLoot["gold"],"<:tc:1218274555081261116>",listLoot["tc"],listLoot["loot"].replace("_",""),listLoot["chip"].replace("*",""),["","\n"][listLoot["chip"] != "" and listLoot["loot"] != ""]))))

	return fieldList

async def explorationEndEmb(exploStartTime: datetime, location:int, user:char, bot:interactions.Client):
	dateDelta = (datetime.now(parisTimeZone) - exploStartTime).total_seconds()
	tmpTeam = []
	if user.team != 0:
		for a in userTeamDb.getTeamMember(user.team): tmpTeam += [loadCharFile("./userProfile/{0}.json".format(a))]
	else: tmpTeam = [user]

	rdmLocation, nbH, nbM = location, dateDelta//60//60, dateDelta//60%60
	if rdmLocation == -1: rdmLocation = random.randint(0,len(listLocations)-1)
	aliceStatsDb.setExplorationStr(user.team)
	return Embed(title="__Votre équipe est revenue d'exploration__",description="Votre équipe est revenue d'exploration. Elle est allé dans **{0}** durant **{1}h{2}**. Voici la liste de leurs trouvailles :".format(listLocations[rdmLocation], int(nbH), int(nbM)),color=tmpTeam[0].color, fields=await explorationReturn(bot=bot, team=tmpTeam, duration=dateDelta, location=rdmLocation))
