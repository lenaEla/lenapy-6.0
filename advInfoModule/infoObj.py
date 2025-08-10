from constantes import *
from classes import *
from adv import findSkill, findStuff, findWeapon, findEffect
from advance_gestion import *

def infoEff2(eff: Union[str, effect], txt: str = "{}", powerPurcent=100, compList: list = None, rangeInt: str= None) -> list:
	eff = findEffect(eff)
	if eff == None: return [TextDisplayComponent("L'effet n'est pas été trouvé")]
	else:
		if compList == None: compList = []

		if eff.callOnTrigger != None:
			eff2 = findEffect(eff.callOnTrigger)
			if eff2 != None and eff.trigger in [TRIGGER_INSTANT, TRIGGER_ON_REMOVE]:
				if eff.trigger == TRIGGER_ON_REMOVE: toAdd = "après {} tours ".format(eff2.turnInit)
				else: toAdd = ""

				tmpEff = copy.deepcopy(eff2)
				if tmpEff.area == AREA_MONO: tmpEff.area = eff.area
				
				if eff2.type == TYPE_DAMAGE: return infoEff2(eff=tmpEff, txt="Inflige une attaque supplémentaire {} la cible {}".format(["à", "autour de"][eff2.area != AREA_MONO], toAdd))
				elif eff2.type in [TYPE_BOOST, TYPE_MALUS, TYPE_INDIRECT_HEAL, TYPE_INDIRECT_DAMAGE]: return infoEff2(eff=tmpEff, txt=["Inflige", "Octroi"][eff2.type in friendlyTypes] + " {}" + " {} la cible {}".format(["à", "autour de"][eff2.area != AREA_MONO], toAdd))
				elif eff2.type == TYPE_HEAL: return infoEff2(eff=tmpEff, txt="Soigne les alliés {} la cible {}".format(["sur ", "autour de"][eff2.area != AREA_MONO], toAdd))
		bonusStr, malusStr = "", ""

		typeEmoji = ""
		if eff.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_RESURECTION]: typeEmoji = statEmojis[ACT_HEAL_FULL]
		elif eff.type in [TYPE_INDIRECT_DAMAGE]: typeEmoji = statEmojis[ACT_INDIRECT_FULL]
		elif eff.type in [TYPE_ARMOR]: typeEmoji = statEmojis[ACT_SHIELD_FULL]
		elif eff.type in [TYPE_BOOST,TYPE_MALUS]: typeEmoji = statEmojis[ACT_BOOST_FULL]
		elif eff.type in [TYPE_SUMMON,TYPE_DEPL]: typeEmoji = "<:Icn_Sprinkler:1080807633432350801>"
		elif eff.type in [TYPE_DAMAGE]: typeEmoji = statEmojis[ACT_DIRECT_FULL]

		effTmp = "__Type :__ {1} {0}\n".format(allTypeNames[eff.type],typeEmoji)

		if rangeInt != None: effTmp += "__Portée :__ {} *{}*\n".format(areaEmojis[rangeInt], areaNames[rangeInt])
		if eff.power > 0 or eff.overhealth > 0: 
			powa = max(eff.power, eff.overhealth)*([powerPurcent,100][eff.stat in [PURCENTAGE,FIXE,None,MISSING_HP]]/100)
			if not(eff.stat in [PURCENTAGE, FIXE, None, MISSING_HP, HARMONIE]): effTmp += "__Puissance :__ {} **{}** (*{} {}*)".format(statEmojis[eff.stat], int(powa), areaEmojis[eff.area], areaNames[eff.area])
			elif eff.stat == PURCENTAGE: effTmp += "__Puissance :__ **{}% PV Max** (*{} {}*)".format(int(powa), areaEmojis[eff.area], areaNames[eff.area])
			elif eff.stat == MISSING_HP: effTmp += "__Puissance :__ **{}% PV manquants** (*{} {}*)".format(int(powa), areaEmojis[eff.area], areaNames[eff.area])
			elif eff.stat == HARMONIE: effTmp += "__Puissance :__ **{}** (Harmonie) (*{} {}*)".format(int(powa), areaEmojis[eff.area], areaNames[eff.area])
			else: effTmp += "__Puissance :__ **{}** (Fixe) (*{} {}*)".format( int(powa), areaEmojis[eff.area], areaNames[eff.area])

		else: effTmp += "__Statistique :__ **{} {}**".format(extraStatEmojis[eff.stat], extraallStatNames[eff.stat])

		if eff.turnInit == -1: effTmp += "\n__Durée :__ Infinie\n"
		elif eff.trigger!=TRIGGER_INSTANT: effTmp += "\n__Durée :__ {0} tour{1}\n".format(eff.turnInit,["","s"][eff.turnInit>1])
		else: effTmp += "\n"

		addTxt = ""
		if eff.trigger != TRIGGER_PASSIVE: addTxt += "Cet effet se déclanche {0}".format(triggersTxt[eff.trigger])
		if eff.stackable: addTxt += "Cet effet est **cumulable**"
		if eff.callOnTrigger != None and findEffect(eff.callOnTrigger) != None:
			effCalled = findEffect(eff.callOnTrigger)
			addTxt += "\nEn se déclanchant, cet effet {0} {1}".format(["octroie","inflige"][effCalled.type in hostileTypes],effCalled)

		if eff.lvl not in [1,99] and eff.trigger not in [TRIGGER_PASSIVE] and eff.type not in [TYPE_PASSIVE,TYPE_BOOST,TYPE_MALUS,TYPE_ARMOR] and eff.lvl != eff.turnInit: addTxt += "\nCet effet peut se déclancher au maximum **{0} fois**".format(eff.lvl)
		stats = eff.allStats()+[eff.resistance, eff.percing, eff.critical, eff.overhealth, eff.aggro, eff.inkResistance, eff.block, eff.dodge, eff.critDmgUp, eff.critHealUp, eff.dmgUp, eff.healUp, eff.counterOnBlock, eff.counterOnDodge]
		names = nameStats+nameStats2 + ["Puissance de l'Armure", "Agression", "Résistance aux dégâts indirects","Blocage","Prob. Esquive", "Dégâts Critiques","Soins Critiques", "Dégâts non critiques","Soins non critiques","Prob. Contre lors d'un blocage","Prob. Contre lors d'une esquive"]

		if eff.redirection > 0: addTxt += "\nCet effet redirige **{0}**% des **dégâts direct** reçu par le porteur vers le lanceur de l'effet en tant que **dégâts indirects**".format(eff.redirection)
		if eff.immunity: addTxt += "\nCet effet rend le porteur **invulnérable aux dégâts**"
		if eff.armorDmgBonus > 0: addTxt += "\nCet effet augmente les dégâts du porteur sur les armures de **{0}%**".format(int(eff.armorDmgBonus*100))
		if eff.superBreak: 
			if eff.type == TYPE_BOOST: addTxt += "\nCet effet permet d'infliger aux ennemis attaqués des dégâts de <:allOut:1254213677134118993> **Rupture Extrême**"
			else: addTxt += "\nCet effet permet d'infliger au porteur des dégâts de <:completCombustion:1254213769131986976> **Rupture Extrême**"

		if addTxt != "": effTmp += "\n"+addTxt
		if eff.description != "Pas de description":
			if eff.stat not in [FIXE,None,PURCENTAGE]: statEm = " ({})".format(statEmojis[eff.stat])
			else: statEm = ""
			effTmp += "\n\n{1}__Description :__\n{0}\n".format(eff.description.format(str([round(eff.power*(powerPurcent/100),1),eff.power][type(eff.power)==int])+statEm, str(int(eff.power*powerPurcent/100)//2)+statEm),["","\n"][effTmp[-1] == "\n"])
		for a in range(len(stats)):
			if stats[a] > 0: bonusStr += "{2} __{0}__ : +{1}\n".format(names[a],int(stats[a]*powerPurcent/100),[statEmojis[a],""][a>CRITICAL])
			elif stats[a] < 0: malusStr += "{2} __{0}__ : {1}\n".format(names[a],int(stats[a]*powerPurcent/100),[statEmojis[a],""][a>CRITICAL])

		if bonusStr != "": effTmp += ["\n",""][effTmp[-1]=="\n"]+"\n**__Bonus de statistiques :__**{0}\n".format([""," *({0}%)*".format(powerPurcent)][powerPurcent!=100]) + bonusStr
		if malusStr != "": effTmp += ["\n",""][effTmp[-1]=="\n"]+"\n**__Malus de statistiques :__**{0}\n".format([""," *({0}%)*".format(powerPurcent)][powerPurcent!=100]) + malusStr

		if eff.inkResistance > 0 and eff.stat != None: effTmp += "\nLa résistance aux dégâts indirects ne peux pas dépasser 3 fois sa valeur de base"
		if eff.block > 0: effTmp += "\n__Blocage :__\nUne attaque bloquée réduit de **35%** les dégâts reçus"
		if eff.counterOnDodge > 0: effTmp += "\n__Contre Attaque :__\n- Puissance : **{0}**, Harmonie".format(COUNTERPOWER)
		if eff.reject != None:
			effTmp += "\n{0}__Cet effet n'est pas compatible avec les effets :__\n".format(["","\n"][effTmp[-1]!="\n"])
			for a in eff.reject:
				rejected = findEffect(a)
				effTmp += f"{rejected.emoji[0][0]} {rejected.name}\n"

		while effTmp.endswith("\n"): effTmp = effTmp[:-1]

		while "\n\n\n" in effTmp: effTmp = effTmp.replace("\n\n\n", "\n\n")
		compList.append(TextDisplayComponent("**{} :**\n> {}".format(txt.format(eff), effTmp.replace("\n", "\n> "))))
		return compList

def getMultiPow(itm: skill, statDict = {}, key:skill = None):
	itm = findSkill(itm)
	if itm == None: return "The skill could not have been found"
	if itm.effectOnSelf != None:
		eff = findEffect(itm.effectOnSelf)
		if eff.replica != None:
			if key == None:
				try: statDict[itm].append(itm)
				except KeyError: statDict[itm] = [itm]
			else:
				try: statDict[key].append(itm)
				except: print("{} :\n{}".format(itm, format_exc()))
			return getMultiPow(eff.replica, statDict, itm)
		else: statDict[itm] = [itm]
	else:
		statDict[itm] = [itm]
	toReturn = ""

	for mainSkill, subSkillList in statDict.items():
		for tmpSkill in subSkillList:
			toReturn += "- {2} : {0} **{1}** ({3} {4} )\n> *Tour{5} de rechargement{5} : {6}*\n".format(statEmojis[tmpSkill.use], tmpSkill.power, str(tmpSkill).replace("__", ""), rangeAreaEmojis[tmpSkill.range], areaEmojis[tmpSkill.area], ["", "s"][tmpSkill.cooldown > 1], tmpSkill.cooldown)
		toReturn = toReturn[:-1] +"\n"
	return toReturn

legendButton = Button(style=ButtonStyle.SECONDARY, label="Détail des attributs", emoji=PartialEmoji(name="⬇️"), custom_id="legendeButton")
areaButton = Button(style=ButtonStyle.SECONDARY, label="Détail des zones d'effets", emoji=PartialEmoji(name="⬇️"), custom_id="areaButton")
jaugeButton = Button(style=ButtonStyle.SECONDARY, custom_id="jaugeButton", label="tmp")
effButton = Button(style=ButtonStyle.SECONDARY, label="Détail des effets", emoji=PartialEmoji(name="⬇️"), custom_id="effButton")

def getTablFromVisuArea(area:int, wanted:int, fromDir:int):
	mainTabl, tmp, indx = [[]], "", 0
	value = visuArea(area=area, wanted=wanted, fromDir=fromDir)

	for c in value:
		if c == "|":
			mainTabl[indx].append(tmp)
			tmp = ""
		elif c == "\n":
			mainTabl[indx].append(tmp)
			tmp = ""
			mainTabl.append([])
			indx += 1
		else:
			tmp += c
	
	return mainTabl

def colorTablVisuArea(value: List[List[List[int]]], tablInit: List[cellule], color:int):
	colorIndx = color // 2 + 1
	
	for tmpCell in tablInit:
		value[tmpCell.x][tmpCell.y][colorIndx] = color%2 + 1

	return value

def getStrFromCellList(value: List[List[List[int]]]):
	toReturn = ""
	for a in range(len(value)):
		for b in range(len(value[a])):
			key = '{}{}{}{}'.format(value[a][b][0], value[a][b][1], value[a][b][2], value[a][b][3])
			toReturn += "{}|".format([targetEmojis[key], key][targetEmojis[key] == "MISSING"])
		toReturn = toReturn[:-1]+"\n"
	return toReturn

def skillVisuArea(itm: Union[str, skill]):
	if type(itm) == str:
		itm2 = findSkill(itm)
		if itm2 == None: itm = findWeapon(itm)
		else: itm = itm2
	if itm == None:
		return ContainerComponent(TextDisplayComponent("Le skill n'a pas été trouvé"), accent_color=red)

	boardSize = BOARD_NORMAL
	if itm.range in [AREA_MONO, AREA_CIRCLE_1] and itm.area in [AREA_MONO, AREA_CIRCLE_1]:
		boardSize = BOARD_SMALL
	elif itm.range in [AREA_MONO, AREA_CIRCLE_1, AREA_CIRCLE_2, AREA_CIRCLE_3]:
		boardSize = BOARD_DISPLAY

	board, toReturn, containerComp, isHostile = cellBoard(boardSize), [], [], int(itm.type in hostileTypes)
	for x in range(board.lenX):
		toReturn.append([])
		for y in range(board.lenY):
			toReturn[x].append([0, 0, 0, 0])

	else: mainCell: cellule = board.findCell(*{BOARD_NORMAL:(2, 1), BOARD_SMALL:(1,[0, 1][itm.range == AREA_MONO]), BOARD_DISPLAY:(2,1)}[boardSize])
	
	toReturn[mainCell.x][mainCell.y][0] = 1

	mainRange = board.getArea(mainCell=mainCell, area=itm.range, team=0, fromCell=mainCell)
	toReturn = colorTablVisuArea(toReturn, mainRange, isHostile)

	if itm.range != AREA_MONO:
		targetCell: cellule = board.findCell(*{BOARD_NORMAL:(2, 4), BOARD_SMALL:(1,1), BOARD_DISPLAY:(2,3)}[boardSize])
		toReturn[targetCell.x][targetCell.y][0] = 2 + int(isHostile)
	else: targetCell = mainCell

	targetArea = board.getArea(mainCell=targetCell, area=itm.area, team=0, fromCell=mainCell)
	toReturn = colorTablVisuArea(toReturn, targetArea, 2+isHostile)

	areaMsg = "{0} {1} *{2}*\n{3} {4} *{5}*".format(targetEmojis["0{}00".format(1+ int(isHostile))],  rangeAreaEmojis[itm.range], areaNames[itm.range], targetEmojis["00{}0".format(1+ int(isHostile))], areaEmojis[itm.area], areaNames[itm.area])
	biggestArea, effType, effName, effArea = [], -1, "", -1
	for eff in itm.effects:
		eff = findEffect(eff)
		if eff != None:
			tmpArea = board.getArea(mainCell=targetCell, area=eff.area, team=0, fromCell=mainCell)
			if len(tmpArea) > len(biggestArea): biggestArea, effType, effName, effArea = tmpArea, int(eff.type in hostileTypes), eff.__str__(), eff.area

	if len(biggestArea) > 1:
		toReturn = colorTablVisuArea(toReturn, biggestArea, 4+effType)
		areaMsg += "\n-# {} {} : {} *{}*".format(targetEmojis["000"+str(effType+1)], effName.replace("__", "*"), areaEmojis[effArea], areaNames[effArea])

	if itm.effectAroundCaster != None:
		toReturn = colorTablVisuArea(toReturn, board.getArea(mainCell=mainCell, area=itm.effectAroundCaster[1], team=0, fromCell=mainCell), 4+int(itm.effectAroundCaster[0] in hostileTypes))

		try:
			if type(itm.effectAroundCaster[2]) == int:
				areaMsg += "\n-# {} {}{}*{}* : {} *{}*".format(targetEmojis["000"+str(int(itm.effectAroundCaster[2].type in hostileTypes)+1)], typeEmojis[itm.effectAroundCaster[0]], statEmojis[itm.use], itm.effectAroundCaster[2], areaEmojis[itm.effectAroundCaster[1]], areaNames[itm.effectAroundCaster[1]])
			else:
				areaMsg += "\n-# {} {} : {} *{}*".format(targetEmojis["000"+str(int(itm.effectAroundCaster[2].type in hostileTypes)+1)], itm.effectAroundCaster[2].replace("__", "*"), areaEmojis[itm.effectAroundCaster[1]], areaNames[itm.effectAroundCaster[1]])
		except:
			print_exc()
			print(itm.name, itm.effectAroundCaster)
	return TextDisplayComponent(reduceEmojiNames("### {0} : Détail des zones d'effets\n\n{1}\n{2}".format(
			itm, getStrFromCellList(toReturn), areaMsg 
		))
	)

def weaponVisuArea(itm: Union[str, weapon]):
	itm = findWeapon(itm)
	if itm == None:
		return ContainerComponent(TextDisplayComponent("Le skill n'a pas été trouvé"), accent_color=red)

	boardSize = BOARD_NORMAL

	board, toReturn, containerComp, isHostile = cellBoard(boardSize), [], [], int(itm.target == ENEMIES)
	for x in range(board.lenX):
		toReturn.append([])
		for y in range(board.lenY):
			toReturn[x].append([0, 0, 0, 0])

	else: mainCell: cellule = board.findCell(2, 1)
	
	toReturn[mainCell.x][mainCell.y][0] = 1

	mainRange = board.getArea(mainCell=mainCell, area=itm.effectiveRange, team=0, fromCell=mainCell)
	toReturn = colorTablVisuArea(toReturn, mainRange, isHostile)

	if itm.effectiveRange != AREA_MONO:
		targetCell: cellule = board.findCell(2, 4)
		toReturn[targetCell.x][targetCell.y][0] = 2 + isHostile
	else: targetCell = mainCell

	targetArea = board.getArea(mainCell=targetCell, area=itm.area, team=0, fromCell=mainCell)
	toReturn = colorTablVisuArea(toReturn, targetArea, 2+isHostile)

	areaMsg = "{0} {1} *{2}*\n{3} {4} *{5}*".format(targetEmojis["0{}00".format(1+ int(isHostile))], rangeAreaEmojis[itm.effectiveRange], areaNames[itm.effectiveRange], targetEmojis["00{}0".format(1+ int(isHostile))], areaEmojis[itm.area], areaNames[itm.area])
	biggestArea, effType, effName, effArea = [], -1, "", -1
	
	if itm.effectOnUse != None:
		tmpArea = board.getArea(mainCell=targetCell, area=eff.area, team=0, fromCell=mainCell)
		if len(tmpArea) > len(biggestArea): biggestArea, effType, effName, effArea = tmpArea, int(eff.type in hostileTypes), eff.__str__(), eff.area
	
	if len(biggestArea) > 1:
		toReturn = colorTablVisuArea(toReturn, biggestArea, 4+effType)
		areaMsg += "\n-# {} {} : {} *{}*".format(targetEmojis["000"+str(effType+1)], effName.replace("__", "*"), areaEmojis[effArea], areaNames[effArea])

	return TextDisplayComponent(reduceEmojiNames("### __Portée et zone d'effet :__\n\n{1}\n{2}".format(itm, getStrFromCellList(toReturn), areaMsg))
	)

legend_visuArea = TextDisplayComponent("-# {} : Lanceur, {} : Cible alliée, {} : Cible ennemie\n-# {} / {} : Cellule à portée\n-# {} / {} : Cellule dans l'aire d'effet principale\n-# {} / {} : Cellule dans l'aire d'effet secondaire".format(
	targetEmojis["1000"], targetEmojis["2000"], targetEmojis["3000"], targetEmojis["0100"], targetEmojis["0200"], targetEmojis["0010"], targetEmojis["0020"], targetEmojis["0001"], targetEmojis["0002"]
))

lenLegendVisuArea = len(legend_visuArea.content)

def infoSkill2(itm: Union[str, skill], subTabl = []):
	itm = findSkill(itm)
	if itm == None: return [TextDisplayComponent("La compétence n'a pas été retrouvée")]

	if itm.become != None and len(itm.become) > 3:
		txt = "Cette compétence regroupe les compétences suivantes :\n\n"
		for tmpSkill in itm.become:
			if len(itm.become) < 10: txt += "- {} :\n{}\n\n".format(tmpSkill, tmpSkill.getSummary())
			else: txt += "\- {} :\n{}\n".format(tmpSkill, tmpSkill.getSummary().splitlines()[0])

		return [TextDisplayComponent("### {}\n{}".format(itm, txt))]
	else:
		if itm.effectOnSelf != None:
			eff = findEffect(itm.effectOnSelf)
			if eff != None and eff.replica != None:
				subTabl.append(itm)
				return infoSkill2(eff.replica, subTabl=subTabl)

	desc = ""
	if itm.become != None:
		desc += "Cette compétence regroupe les compétences suivantes :\n"
		listConds = []
		for indx, tmpSkill in enumerate(itm.become):
			desc += "{}".format(tmpSkill)
			if indx < len(itm.become)-2: desc += ", "
			elif indx == len(itm.become)-2: desc += " et "
		desc += "\n\n"

	# Type
	typeEmoji = ""
	if itm.type in [TYPE_DAMAGE]: typeEmoji = statEmojis[ACT_DIRECT_FULL]
	elif itm.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_RESURECTION]: typeEmoji = statEmojis[ACT_HEAL_FULL]
	elif itm.type in [TYPE_INDIRECT_DAMAGE]: typeEmoji = statEmojis[ACT_INDIRECT_FULL]
	elif itm.type in [TYPE_ARMOR]: typeEmoji = statEmojis[ACT_SHIELD_FULL]
	elif itm.type in [TYPE_BOOST,TYPE_MALUS]: typeEmoji = statEmojis[ACT_BOOST_FULL]
	elif itm.type in [TYPE_SUMMON,TYPE_DEPL]: typeEmoji = "<:sprink1:887747751339757599>"

	desc += "__Type :__ {} {}\n".format(typeEmoji, allTypeNames[itm.type])
	lenCast, lenChannel, lenChain = 0, 0, 0
	for tmpSkill in subTabl:
		if tmpSkill.power == 0 and tmpSkill.effects == [None]: lenCast += 1
		elif tmpSkill.replay: lenChain += 1
		else: lenChannel += 1

	if lenCast > 0: desc += "Cette compétence requière {} tour{} de chargement\n".format(lenCast+1, ["", "s"][lenCast > 1])
	if lenChain > 0: desc += "Cette compétence permet d'enchainer plusieurs compétences durant le même tour\n"
	if lenChannel > 0: desc += "Cette compétence s'utilise en continue durant {} tour{}\n".format(lenChannel+1, ["", "s"][lenChain > 1])

	desc += "\n__Description :__\n*{}*".format(itm.description)
	powerComp = ""

	if itm.become == None and itm.power > 0:
		if subTabl == []: powerComp += "__Puissance :__ **{1}**{2} {0} (Précision : *{3}*%) ({4} {5} )\n> *Tour{6} de rechargement{6} : {7}*".format(extraStatEmojis[itm.use], itm.power, ["", " x{}".format(itm.repetition)][itm.repetition > 1], itm.accuracy, rangeAreaEmojis[itm.range], areaEmojis[itm.area], ["", "s"][itm.cooldown > 1], itm.cooldown)
		else:
			tmp, totalPow, areaEm = "", {}, ""
			for tmpSkill in subTabl+[itm]:
				try: totalPow[tmpSkill.use] += tmpSkill.power * tmpSkill.repetition
				except KeyError: totalPow[tmpSkill.use] = tmpSkill.power * tmpSkill.repetition

				if tmpSkill.areaEmoji not in areaEm: areaEm += tmpSkill.areaEmoji

				tmp += "\n- {0} : {1} **{2}**{3}{4} ({5} {6})".format(tmpSkill, statEmojis[tmpSkill.use], tmpSkill.power, ["", " x{}".format(tmpSkill.repetition)][tmpSkill.repetition > 1], ["", " (Précision : *{}*%)".format(tmpSkill.accuracy)][tmpSkill.power > 0], rangeAreaEmojis[tmpSkill.range], areaEmojis[tmpSkill.area])

			powerComp += "__Puissance :__ Total : "
			for key, obj in totalPow.items():
				powerComp += "**{1}** {0} + ".format(statEmojis[key], obj)
			powerComp = powerComp[:-3]
			if lenCast+lenChannel > 0: powerComp += " / {} tours".format(lenCast+lenChannel+1)
			powerComp += " ({})".format(areaEm) + tmp + "\n> *Tour{0} de rechargement{0} : {1}*".format(["", "s"][itm.cooldown > 1], itm.cooldown)
	elif itm.become != None:
		powerComp += "\n__Puissances :__\n"
		for tmpSkill in itm.become:
			powerComp += getMultiPow(itm=tmpSkill, statDict = {})
	else:
		powerComp = "__Portée et zone d'effet__ :\n{0} *{1}*, {2} *{3}*\n> Tour{4} de rechargement{4} : {5}".format(rangeAreaEmojis[itm.range], areaNames[itm.range], areaEmojis[itm.area], areaNames[itm.area], ["", "s"][itm.cooldown > 1], itm.cooldown)
	
	testCompListLight = [
		SectionComponent(components=[TextDisplayComponent("### {}\n{}".format(itm, desc))], accessory=ThumbnailComponent(media=UnfurledMediaItem(url="https://cdn.discordapp.com/emojis/{}.{}".format(PartialEmoji.from_str(itm.emoji).id, ["webp", "gif"][itm.emoji[2] == "a"])))),
		SeparatorComponent(),
		SectionComponent(components=[TextDisplayComponent(powerComp)], accessory=areaButton)
	]

	testCompListFull = copy.deepcopy(testCompListLight)

	dictSpecialEffects = {}
	if itm.become == None and subTabl == []: listSkills = [itm]
	elif itm.become == None and subTabl != []: listSkills = subTabl + [itm]
	else:
		listSkills = []
		for tmpItm in itm.become:
			if tmpItm.effectOnSelf == None: listSkills.append(tmpItm)
			while tmpItm.effectOnSelf != None:
				listSkills.append(tmpItm)
				eff = findEffect(tmpItm.effectOnSelf)
				if eff != None and eff.replica != None:
					tmpSkill = findSkill(eff.replica)
					if tmpSkill != None: tmpItm = tmpSkill
				else:
					break

	jaugeStatMsg, tablEff = "", []
	for tmpSkill in listSkills:
		suppStatsLight, suppStatsFull = "", ""
		listConds = [tmpSkill.damageOnArmor != 1, tmpSkill.replay, tmpSkill.maxHpCost > 0, tmpSkill.hpCost > 0, tmpSkill.ultimate, tmpSkill.execution, tmpSkill.group != 0, tmpSkill.setAoEDamage, tmpSkill.lifeSteal > 0, tmpSkill.aoeLifeSteal > 0, tmpSkill.armorConvert > 0, tmpSkill.aoeArmorConvert > 0, tmpSkill.tpCac, tmpSkill.tpBehind, tmpSkill.percing > 0, tmpSkill.knockback > 0 and tmpSkill.become == None, tmpSkill.pull > 0 and tmpSkill.become == None, tmpSkill.garCrit, tmpSkill.sharedDamage, tmpSkill.sharedTB, tmpSkill.erosion > 0]
		listToAddEmoji = [
			["<:matriceArmor2R:1241381762291073024>", "<:matriceArmor2B:1241381818901725305>"][tmpSkill.damageOnArmor > 1],
			"<:qqLuna:932318030380302386>",
			"<:dvin:1004737746377654383>",
			"<:dmon:1004737763771433130>",
			"<:littleStar:925860806602682369>",
			"<:sacrified:973313400056725545>",
			["","<:dvin:1004737746377654383>","<:dmon:1004737763771433130>"][tmpSkill.group],
			"<:dislocation:1052697663402950667>",
			"<:vampire:900312789686571018>",
			"<:aoeLifeSteal:1100770895846457376>",
			"<:converted:902527031663788032>",
			"<:aoeConvert:1100770918340497519>",
			"<:iliLightSpeed:1046384202792308797>",
			"<:liaCounter:998001563379437568>",
			statEmojis[PERCING],
			"<:piedVolt:1034208868068233348>",
			"<:retPercu:1034210776703062057>",
			"<:critB:925763298346033193>",
			"<:akiStack:1007050822338748466>",
			"<:akiTankStack:1007050856748818464>",
			"<:emoji_4:1028695463651717200>"
		]
		listToAdd = [
			"Inflige **{}%** dégats contre l'armure".format(tmpSkill.damageOnArmor * 100),
			"Permet de **rejouer son tour**",
			"Réduit de **{0}%** les PV Max".format(tmpSkill.maxHpCost),
			"Réduit de **{0}%** les PV actuels".format(tmpSkill.hpCost),
			"Compétence Ultime",
			"Exécution",
			"Compétence {0}".format(skillGroupNames[tmpSkill.group][0].upper()+skillGroupNames[tmpSkill.group][1:]),
			"Ignore la réduction de Dégâts de zone",
			"Vous soigne de **{0}%** des dégâts infligés".format(tmpSkill.lifeSteal),
			"Soigne les alliés alentours de **{0}%** des dégâts infligés".format(tmpSkill.aoeLifeSteal),
			"Vous octroie une armure équivalent à **{0}%** des dégâts infligés".format(tmpSkill.armorConvert),
			"Octroie une armure équivalent à **{0}%** des dégâts infligés aux alliés proches".format(tmpSkill.aoeArmorConvert),
			"Permet de sauter **devant** de la cible",
			"Permet de sauter **derrière** de la cible",
			"Ignore **{0}%** de la Résistance de la cible".format(tmpSkill.percing),
			"Pousse les cibles de **{0} case{1}**".format(tmpSkill.knockback,["","s"][tmpSkill.knockback > 1]),
			"Vous fait reculer de **{0} case{1}**".format(tmpSkill.jumpBack,["","s"][tmpSkill.jumpBack > 1]),
			"Inflige forcément un coup critique",
			"La puissance de cette compétence est divisée par le nombre de cible",
			"La puissance de cette compétence est divisée par le nombre de cible ayant une aspiration de mêlée",
			"Réduit les PV max de la cible de **{0}%** des dégâts infligés".format(tmpSkill.erosion)
		]
		listSmallAtributs = [
			["Dégâts réduits sur l'armure", "Dégâts accrus sur l'armure"][tmpSkill.damageOnArmor > 100],
			"Permet de rejouer son tour",
			"Réduit les PV Max du lanceur",
			"Réduit les PV du lanceur",
			"Compétence Ultime",
			"Exécution",
			"Compétence {0}".format(skillGroupNames[tmpSkill.group][0].upper()+skillGroupNames[tmpSkill.group][1:]),
			"Ignore la réduction de Dégâts de zone",
			"Vol de vie",
			"Vol de vie en zone",
			"Convertion d'armure",
			"Convertion d'armure en zone",
			"Saute devant de la cible",
			"Saute derrière de la cible",
			"Ignore une partie de la Résistance de la cible".format(tmpSkill.percing),
			"Pousse les cibles",
			"Vous fait reculer",
			"Inflige forcément un coup critique",
			"Puissance divisée par le nombre de cible",
			"Puissance divisée par le nombre de cible ayant une aspiration de mêlée",
			"Réduit les PVs max de la cible"
		]

		for indx, value in enumerate(listConds):
			if value:
				suppStatsFull += "- {} {}\n".format(listToAddEmoji[indx], listToAdd[indx])
				suppStatsLight += "\n> -# {} {}".format(listToAddEmoji[indx], listSmallAtributs[indx])

		dictSpecialEffects[tmpSkill] = [suppStatsFull, suppStatsLight]
		if tmpSkill.jaugeEff != None:
			if jaugeStatMsg == "":
				jaugeStatMsg = "\n**Consommation de {} :**\n".format(tmpSkill.jaugeEff)
			if tmpSkill.minJaugeValue == tmpSkill.maxJaugeValue or tmpSkill.maxJaugeValue <= 0: 
				jaugeStatMsg += "{}{} : **{}** point{}\n".format(["", "- "][len(listSkills) > 1], tmpSkill, tmpSkill.minJaugeValue, ["", "s"][tmpSkill.minJaugeValue > 1])
			else:
				jaugeStatMsg += "{}{} : **{}** → **{}** point{}\n".format(["", "- "][len(listSkills) > 1], tmpSkill, tmpSkill.minJaugeValue, tmpSkill.maxJaugeValue, ["", "s"][tmpSkill.minJaugeValue > 1])

		if tmpSkill.rejectJaugeVal != None:
			if jaugeStatMsg == "":
				jaugeStatMsg = "\n**Consommation de {} :**\n".format(tmpSkill.rejectJaugeVal[0])
			jaugeStatMsg += "- {} n'est utilisable uniquement si la {} est inférieure à {} points\n".format(tmpSkill, tmpSkill.rejectJaugeVal[0], tmpSkill.rejectJaugeVal[1])

		for eff in tmpSkill.effects:
			eff = findEffect(eff)
			if eff != None:
				skillName = ["", "{} ".format(tmpSkill)][len(listSkills) > 1]
				subMsg = [["Octroi", "Inflige"][eff.type in hostileTypes], ["octroi", "inflige"][eff.type in hostileTypes]][len(listSkills) > 1]
				
				if not(eff.type in hostileTypes or (eff.type in friendlyTypes and tmpSkill.area == AREA_MONO)): targetAccord = ["aux", "s"]
				else: targetAccord = ["à la", ""]

				tmpTxt = "{}{} l'effet".format(skillName, subMsg) + " {} " + "{} cible{}".format(targetAccord[0], targetAccord[1])

				tablEff.append(
					[
						tmpTxt.format(eff)+"\n",
						infoEff2(eff=eff, txt=tmpTxt, powerPurcent=tmpSkill.effPowerPurcent, compList = None)
					]
				)
		if tmpSkill.effectOnSelf != None:
			eff = findEffect(tmpSkill.effectOnSelf)
			if eff != None and not(eff.silent):
				skillName = ["", "{} ".format(tmpSkill)][len(listSkills) > 1]
				subMsg = [["Octroi", "Inflige"][eff.type in hostileTypes], ["octroi", "inflige"][eff.type in hostileTypes]][len(listSkills) > 1]
				
				if not(eff.type in hostileTypes or (eff.type in friendlyTypes and tmpSkill.area == AREA_MONO)): targetAccord = ["aux", "s"]
				else: targetAccord = ["à la", ""]

				tmpTxt = "{}{} l'effet".format(skillName, subMsg) + " {} " + "au lanceur".format(targetAccord[0], targetAccord[1])

				tablEff.append(
					[
						tmpTxt.format(eff)+"\n",
						infoEff2(eff=eff, txt=tmpTxt, powerPurcent=tmpSkill.selfEffPurcent, compList = None)
					]
				)

		if tmpSkill.effectAroundCaster != None:
			if type(tmpSkill.effectAroundCaster[2]) == effect:
				eff = findEffect(tmpSkill.effectAroundCaster[2])
				if eff != None and not(eff.silent):
					skillName = ["", "{} ".format(tmpSkill)][len(listSkills) > 1]
					subMsg = [["Octroi", "Inflige"][eff.type in hostileTypes], ["octroi", "inflige"][eff.type in hostileTypes]][len(listSkills) > 1]
					
					if not(eff.type in hostileTypes or (eff.type in friendlyTypes and tmpSkill.area == AREA_MONO)): targetAccord = ["aux", "s"]
					else: targetAccord = ["à la", ""]

					tmpTxt = "{}{} l'effet".format(skillName, subMsg) + " {} " + "dans un {} *{}* autour du lanceur".format(areaEmojis[tmpSkill.effectAroundCaster[1]], areaNames[tmpSkill.effectAroundCaster[1]])
					tmpTxt2 = "{}{} l'effet".format(skillName, subMsg) + " {} " + " autour du lanceur"
					tablEff.append(
						[
							tmpTxt.format(eff)+"\n",
							infoEff2(eff=eff, txt=tmpTxt2, powerPurcent=tmpSkill.selfEffPurcent, compList = None, rangeInt=tmpSkill.effectAroundCaster[1])
						]
					)

		# Combo
	if itm.become != None:
		comboDict = {}
		for tmpSkill in itm.become:
			if tmpSkill.effectOnSelf != None:
				eff = findEffect(tmpSkill.effectOnSelf)
				for tmpItm in itm.become:
					if tmpItm != tmpSkill and tmpItm.needEffect != None:
						for tmpEff in tmpItm.needEffect:
							tmpEff = findEffect(tmpEff)
							if eff.id == tmpEff.id:
								if len(comboDict.keys()) == 0:
									comboDict[tmpSkill] = [tmpItm]
								else:
									for tabl in comboDict:
										if tmpSkill in comboDict[tabl]:
											comboDict[tabl].append(tmpItm)
										elif tmpSkill not in comboDict.keys():
											comboDict[tmpSkill] = [tmpItm]

		if len(comboDict.keys()) > 0:
			tmpValue, tmpValueLight = "", ""
			for mainSkill, skillList in comboDict.items():
				tmpValue += "{}".format(mainSkill).replace("__", "*")
				tmpValueLight += mainSkill.name
				for tmpItm in skillList:
					tmpValue += " → {}".format(tmpItm).replace("__", "*")
					tmpValueLight += " → {}".format(tmpItm.name)
				tmpValue += "\n"

			testCompListFull += [
				SeparatorComponent(), TextDisplayComponent("**Combo :**\n"+tmpValue)
			]
			testCompListLight += [
				SeparatorComponent(), TextDisplayComponent("**Combo : ** "+tmpValueLight)
			]


	tmpStr, tmpList = "", []
	for tmp in tablEff:
		tmpStr += tmp[0]
		tmpList += tmp[1]

	if tmpStr != "":
		testCompListLight += [
			SeparatorComponent(),
			SectionComponent(components=[TextDisplayComponent("**Liste des effets :**\n"+tmpStr)], accessory=effButton)
		]
	if tmpList != []:
		testCompListFull += [SeparatorComponent()]+tmpList

	haveSpecialEffects = False
	if len(dictSpecialEffects.keys()) <= 1:
		haveSpecialEffects = True
		if len(dictSpecialEffects[itm][0]) > 0:
			testCompListFull += [
				SeparatorComponent(),
				TextDisplayComponent("**__Attributs__ :**\n"+dictSpecialEffects[itm][0])
			]
		if len(dictSpecialEffects[itm][1]) > 0:
			testCompListLight += [
				SeparatorComponent(),
				SectionComponent(components=[TextDisplayComponent("**__Attributs__ :**\n"+dictSpecialEffects[itm][0])], accessory=legendButton)
			]
	else:
		haveSpecialEffects = True
		shortList = ""
		for tmpSkill, tablValue in dictSpecialEffects.items():
			if len(tablValue[1]) > 0:
				shortList += "- {} : {}\n".format(tmpSkill, tablValue[1])

		if shortList != "":
			tmpTabl = [SeparatorComponent(), SectionComponent(components=[TextDisplayComponent("**Attributs :**\n"+shortList)], accessory=legendButton)]
			testCompListFull += tmpTabl
			testCompListLight += tmpTabl

	if jaugeStatMsg != "":
		tmpButton = copy.deepcopy(jaugeButton)
		tmpButton.label, tmpButton.emoji = itm.jaugeEff.name, PartialEmoji.from_str(itm.jaugeEff.emoji[0][0])

		tmpTabl = [
			SeparatorComponent(),
			SectionComponent(components=[TextDisplayComponent(jaugeStatMsg)], accessory=tmpButton)
		]
		
		testCompListLight += tmpTabl
		testCompListFull += tmpTabl

	if itm.url != None:
		testCompListFull.append(MediaGalleryComponent([MediaGalleryItem(UnfurledMediaItem(url=itm.url))]))
	if lenContainer(ContainerComponent(*testCompListFull)) > 4000: return testCompListLight
	else: return testCompListFull

def getItmVisuArea(itm: Union[skill, weapon]):
	if type(itm) == str:
		itm2 = findSkill(itm)
		if itm2 == None:
			itm = findWeapon(itm)
		else:
			itm = itm2

	if itm == None: raise AttributeError("Given itm is not a skill or a weapon")

	tablToSee, tablToReturn = [], []
	
	if type(itm) == skill:
		if itm.become == None: tablToSee = [itm]
		else: tablToSee = itm.become
	else: tablToSee = [itm]

	for tmpItm in tablToSee:
		tmp = None
		if type(tmpItm) == skill: tmp = skillVisuArea(tmpItm)
		if type(tmpItm) == weapon: tmp = weaponVisuArea(tmpItm)

		finded = False
		for tmpStr in tablToReturn:
			if tmpStr.content.splitlines()[1:] == tmp.content.splitlines()[1:]:
				tmp2 = "\n".join(tmpStr.content.splitlines()[1:])
				tmpStr.content = tmpStr.content[:4] + tmpItm.__str__() + ", " + tmpStr.content.splitlines()[0][4:] + "\n" + tmp2
				finded = True

		if not(finded):
			tablToReturn.append(tmp)
	
	tablFinal = []
	for tmp in tablToReturn:
		tmp.content = reduceEmojiNames(tmp.content)
		tablFinal += [tmp, SeparatorComponent(divider=True)]
	
	return tablFinal[:-1]

def infoWeapon2(itm: Union[str, weapon]) -> list:
	itm = findWeapon(itm)
	if itm == None: return [TextDisplayComponent("La compétence n'a pas été retrouvée")]

	mainTitle = "### {}".format(itm)

	typeEmoji = ""
	if itm.type in [TYPE_DAMAGE]: typeEmoji = statEmojis[ACT_DIRECT_FULL]
	elif itm.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_RESURECTION]: typeEmoji = statEmojis[ACT_HEAL_FULL]
	elif itm.type in [TYPE_INDIRECT_DAMAGE]: typeEmoji = statEmojis[ACT_INDIRECT_FULL]
	elif itm.type in [TYPE_ARMOR]: typeEmoji = statEmojis[ACT_SHIELD_FULL]
	elif itm.type in [TYPE_BOOST,TYPE_MALUS]: typeEmoji = statEmojis[ACT_BOOST_FULL]
	elif itm.type in [TYPE_SUMMON,TYPE_DEPL]: typeEmoji = "<:sprink1:887747751339757599>"

	mainDesc = "__Type :__ {} {}\n".format(typeEmoji, allTypeNames[itm.type])
	mainDesc += "__Puissance :__ {} {} ({}%) {}".format(statEmojis[itm.use], itm.power, itm.accuracy, ["", " x{}".format(itm.repetition)][itm.repetition])

	stats = ""
	for indx, stat in enumerate(itm.allStats()):
		if stat != 0: stats += "{} {} +{}\n".format(statEmojis[indx], allStatNames[  indx], stat)

	toReturnCompList = [
		SectionComponent(components=[TextDisplayComponent(mainTitle), TextDisplayComponent(mainDesc)], accessory=ThumbnailComponent(media=UnfurledMediaItem(url="https://cdn.discordapp.com/emojis/{}.webp".format(PartialEmoji.from_str(itm.emoji).id)))),
		TextDisplayComponent("**__Bonus de statistiques :__**\n"+stats),
		SeparatorComponent()
	] + getItmVisuArea(itm)

	if itm.effects != None:
		toReturnCompList += [SeparatorComponent()] + infoEff2(eff=itm.effects, txt = "Octroi le passif \"{}\" lorsque cette arme est equipée", powerPurcent=100)
	if itm.effectOnUse != None:
		toReturnCompList += [SeparatorComponent()] + infoEff2(eff=itm.effects, txt = "{}".format(["Octroi", "Inflige"][int(itm.target == ENEMIES)]) +"le passif \"{}\" à la cible lors de l'utilisation", powerPurcent=100)

	return toReturnCompList

def infoStuff2(itm = Union[str, stuff], user: char = None) -> list:
	itm = findStuff(itm)

	if itm == None: return [TextDisplayComponent("L'équiment n'a pas été retrouvée")]
	mainTitle = "### {}".format(itm)

	mainDesc = "__Type__ : {}\n__Orientation :__ {}\n__Niveau :__ {}+".format({0: "Accessoire", 1: "Vêtement", 2: "Chaussures"}[itm.type], itm.orientation, itm.minLvl)

	if user != None and not(user.stuff[itm.type].id == itm.id):
		statsStr, sumDif = "", 0
		equippedItm = user.stuff[itm.type]
		equippedStats = equippedItm.getAllStats()

		for indx, tmpStat in enumerate(itm.getAllStats()):
			tmp = "{0} *{1}* {2}{3}".format(statEmojis[indx], allStatNames[indx], ["", "+"][tmpStat >= 0], tmpStat)

			statDif = tmpStat - equippedStats[indx]

			if indx in recommandedStuffStat[user.aspiration] and statDif != 0:
				if statDif > 0:
					tmp = STAT_UP_EM + " **"+tmp+" (+{})**\n".format(statDif)
					sumDif += statDif
				else: 
					tmp = "-# " + STAT_DOWN_EM + " " + tmp + " ({})\n".format(statDif)
					sumDif += statDif
			else:
				tmp = ["-# ", "**"][tmpStat > 0] + STAT_NEUTRAL_EM + " " + tmp + " ({}{})".format(["", "+"][statDif > 0], statDif) + ["", "**"][tmpStat > 0] + "\n"


			if not(tmpStat == 0 and statDif == 0):
				statsStr += tmp
				sumDif += statDif
			if indx in [CRITICAL, MAGIE] and statsStr[-2:] != "\n\n": statsStr += "\n"

		if sumDif != 0: statsStr += "\n{} {} de statistiques importantes : **{}**".format([STAT_DOWN_EM, STAT_UP_EM][sumDif > 0], ["Pertes", "Gains"][sumDif > 0], abs(sumDif))

		statComponent = TextDisplayComponent("**__Statistiques :__**\n"+statsStr)
	else:
		statStrPlus, statStrMinus = "", ""
		for indx, tmpStat in enumerate(itm.getAllStats()):
			if tmpStat > 0: statStrPlus += "- {} *{}* **+{}**\n".format(statEmojis[indx], allStatNames[indx], tmpStat)
			elif tmpStat < 0: statStrMinus += "-# - {} *{}* {}\n".format(statEmojis[indx], allStatNames[indx], tmpStat)

		statComponent = TextDisplayComponent("**__Statistiques :__**\n"+statStrPlus +"\n"+statStrMinus)

	toReturnCompList = [
		SectionComponent(components=[TextDisplayComponent(mainTitle), TextDisplayComponent(mainDesc)], accessory=(ThumbnailComponent(media=UnfurledMediaItem(url="https://cdn.discordapp.com/emojis/{}.webp".format(PartialEmoji.from_str(itm.emoji).id))))),
		SeparatorComponent(),
		statComponent
	]

	if itm.effects != None:
		toReturnCompList += [SeparatorComponent()] + infoEff2(eff=itm.effects, txt = "Octroi le passif \"{}\" lorsque cet équipement est equipée", powerPurcent=100)

	return toReturnCompList 

def infoJaugeEff(itm = skill):
	temp2 = "\nCette compétence octroie et utilise **{}**. La valeur de cette jauge augmente dans les conditions suivantes :\n".format(itm.jaugeEff)
	jaugeVal: jaugeValue = itm.jaugeEff.jaugeValue
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

	if itm.jaugeEff.id == lycanJauge.id: temp2 += "\nDe plus, lorsque vous attaquez un ennemi, lui inflige {0} (vous pouvez placez qu'un seul effet {0} à la fois)\n> {1}\n".format(hunterMarkEff, hunterMarkEff.description)
	elif itm.jaugeEff.id == bloodJauge.id: temp2 += "\nDe plus, lorsque vous attaquez un ennemi, 30% de chance de lui infliger {0}\n> {1}\n".format(bloodButterfly, bloodButterfly.description)
	elif itm.jaugeEff.id == planJauge.id: temp2 += "\nDe plus, lorsque vous attaquez un ennemi, lui inflige {0} si il n'en était pas sous l'emprise. Si l'effet était déjà présent utlisant une compétence qui consomme cette jauge, {0} est consommé pour infliger une attaque supplémentaire en fonction des PVs manquant de la cible et de la quantité minimale de jauge consommée par la compétence".format(deathMark)

	return TextDisplayComponent(temp2)