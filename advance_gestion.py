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

class cellule:
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
		self.depl = None
		self.surrondings = None
		self.besideGiant = False

	def __str__(self): return "Cell #{} at {}:{}".format(self.id, self.x, self.y)

BOARD_NORMAL = 0
BOARD_BIG = 1
BOARD_DISPLAY = 2
BOARD_SMALL = 3

def infoStuff(): pass

def infoWeapon(): pass

def infoSkill(): pass

class cellBoard:
	def __init__(self, length=BOARD_NORMAL):
		self.lenX = {BOARD_NORMAL:5, BOARD_BIG:7, BOARD_DISPLAY:5, BOARD_SMALL:3}[length]
		self.lenY = {BOARD_NORMAL:6, BOARD_BIG:5, BOARD_DISPLAY:5, BOARD_SMALL:3}[length]
		self.tablCells = []

		cellId = 0
		for x in range(self.lenX):
			self.tablCells.append([])
			for y in range(self.lenY):
				self.tablCells[x].append(cellule(x, y, cellId))
				cellId += 1

	def distance(self, cell1: cellule, cell2: cellule):
		"""Return the distance between 2 cells"""
		try:
			return int(abs(cell1.x - cell2.x)+abs(cell1.y - cell2.y))
		except AttributeError:
			raise AttributeError(cell1.__str__(), cell2.__str__())

	def getArea(self, mainCell: cellule, area=AREA_MONO, team=0, fromCell=None) -> list:
		"""
			Return a list of the cells in the area\n\n
			Parameters :\n
			area : See ``constantes``
			team : The team of the entity who's looking for the area
		"""
		rep = []
		# Circles
		
		if area==AREA_MONO: return [mainCell]
		elif area in [AREA_CIRCLE_1,AREA_CIRCLE_2,AREA_CIRCLE_3,AREA_CIRCLE_4,AREA_CIRCLE_5,AREA_CIRCLE_6,AREA_CIRCLE_7,AREA_DONUT_1,AREA_DONUT_2,AREA_DONUT_3,AREA_DONUT_4,AREA_DONUT_5,AREA_DONUT_6,AREA_DONUT_7,AREA_DIST_3,AREA_DIST_4,AREA_DIST_5,AREA_DIST_6,AREA_DIST_7,AREA_BOMB_5,AREA_BOMB_6,AREA_BOMB_7]:
			dist = area
			if area > AREA_CIRCLE_7:
				if area <= AREA_DONUT_7:
					dist -= AREA_DONUT_1-1
				elif area <= AREA_DIST_7:
					dist -= AREA_DIST_3-3
				elif area <= AREA_BOMB_7:
					dist -= AREA_BOMB_5-5

			for tmpCell in self.getSingleTabl():
				if self.distance(cell2=tmpCell, cell1=mainCell) <= dist:
					rep.append(tmpCell)

			if area > AREA_CIRCLE_7 and area <= AREA_DONUT_7: # If donut, remove the center
				rep.remove(mainCell)
			elif area > AREA_DONUT_7 and area <= AREA_DIST_7: # If dist only, remove melee
				for tmpCell in rep[:]:
					if self.distance(cell2=tmpCell, cell1=mainCell) <= 2:
						rep.remove(tmpCell)
			elif area > AREA_DIST_7 and area <= AREA_BOMB_7: # If dist only, remove melee
				for tmpCell in rep[:]:
					if self.distance(cell2=tmpCell, cell1=mainCell) <= 4:
						rep.remove(tmpCell)
		elif area in [AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES]:
			return self.getSingleTabl()
		elif area in [AREA_CONE_2,AREA_CONE_3,AREA_CONE_4,AREA_CONE_5,AREA_CONE_6,AREA_CONE_7]:
			areaTabl, coneLength, direction = [mainCell],area-(AREA_CONE_2-2), getDirection(fromCell,mainCell)
			if direction in [FROM_RIGHT,FROM_POINT]:
				for cmpt in range(coneLength+1):
					for celly in self.getSingleTabl():
						if celly not in areaTabl:
							if celly == mainCell:
								areaTabl.append(celly)
							elif celly.x == mainCell.x+(cmpt-1) and celly.x >=mainCell.x:
								if ((celly.y>mainCell.y and celly.y < mainCell.y+cmpt) or (celly.y<mainCell.y and celly.y > mainCell.y-cmpt) or (celly.y == mainCell.y)):
									areaTabl.append(celly)
			elif direction == FROM_LEFT:
				for cmpt in range(coneLength+1):
					for celly in self.getSingleTabl():
						if celly not in areaTabl:
							if celly == mainCell:
								areaTabl.append(celly)
							elif celly.x == mainCell.x-(cmpt-1) and celly.x <= mainCell.x:
								if ((celly.y>mainCell.y and celly.y < mainCell.y+cmpt) or (celly.y<mainCell.y and celly.y > mainCell.y-cmpt) or (celly.y == mainCell.y)):
									areaTabl.append(celly)
			elif direction == FROM_DOWN:
				for cmpt in range(coneLength+1):
					for celly in self.getSingleTabl():
							if celly not in areaTabl:
								if celly == mainCell:
									areaTabl.append(celly)
								elif celly.y == mainCell.y+(cmpt-1) and celly.y >= mainCell.y:
									if ((celly.x>mainCell.x and celly.x < mainCell.x+cmpt) or (celly.x<mainCell.x and celly.x > mainCell.x-cmpt) or (celly.x == mainCell.x)):
										areaTabl.append(celly)
			elif direction == FROM_UP:
				for cmpt in range(coneLength+1):
					for celly in self.getSingleTabl():
							if celly not in areaTabl:
								if celly == mainCell:
									areaTabl.append(celly)
								elif celly.y == mainCell.y-(cmpt-1) and celly.y <= mainCell.y:
									if ((celly.x>mainCell.x and celly.x < mainCell.x+cmpt) or (celly.x<mainCell.x and celly.x > mainCell.x-cmpt) or (celly.x == mainCell.x)):
										areaTabl.append(celly)
			
			return areaTabl
		elif area in [17,18,19,20,21]: # Lines
			direction = getDirection(mainCell,fromCell)
			if direction in [FROM_LEFT,FROM_POINT]:
				for cellToSee in self.getSingleTabl():
					if mainCell.y == cellToSee.y and (cellToSee.x - mainCell.x <= area-(AREA_LINE_2-1) and cellToSee.x - mainCell.x >= 0):
						rep.append(cellToSee)
			elif direction == FROM_RIGHT:
				for cellToSee in self.getSingleTabl():
					if mainCell.y == cellToSee.y and (mainCell.x - cellToSee.x <= area-(AREA_LINE_2-1) and cellToSee.x - mainCell.x <= 0):
						rep.append(cellToSee)
			elif direction == FROM_UP:
				for cellToSee in self.getSingleTabl():
					if mainCell.x == cellToSee.x and (cellToSee.y - mainCell.y <= area-(AREA_LINE_2-1) and cellToSee.y - mainCell.y >= 0):
						rep.append(cellToSee)
			elif direction == FROM_DOWN:
				for cellToSee in self.getSingleTabl():
					if mainCell.x == cellToSee.x and (mainCell.y - cellToSee.y <= area-(AREA_LINE_2-1) and cellToSee.y - mainCell.y <= 0):
						rep.append(cellToSee)
		elif area in [AREA_ARC_1,AREA_ARC_2,AREA_ARC_3]: # Arcs
			cmptx, direction = 1, getDirection(mainCell,fromCell)
			if direction in [FROM_LEFT,FROM_RIGHT]:
				while cmptx < area - 32:
					if direction == FROM_LEFT:
						cell1 = self.findCell(mainCell.x-cmptx,mainCell.y-cmptx)
						if cell1 != None:
							rep.append(cell1)
						cell2 = self.findCell(mainCell.x-cmptx,mainCell.y+cmptx)
						if cell2 != None:
							rep.append(cell2)
					else:
						cell1 = self.findCell(mainCell.x+cmptx,mainCell.y-cmptx)
						if cell1 != None:
							rep.append(cell1)
						cell2 = self.findCell(mainCell.x+cmptx,mainCell.y+cmptx)
						if cell2 != None:
							rep.append(cell2)
					cmptx+=1
			else:
				while cmptx < area - 32:
					if direction == FROM_UP:
						cell1 = self.findCell(mainCell.x-cmptx,mainCell.y-cmptx)
						if cell1 != None:
							rep.append(cell1)
						cell2 = self.findCell(mainCell.x+cmptx,mainCell.y-cmptx)
						if cell2 != None:
							rep.append(cell2)
					else:
						cell1 = self.findCell(mainCell.x-cmptx,mainCell.y+cmptx)
						if cell1 != None:
							rep.append(cell1)
						cell2 = self.findCell(mainCell.x+cmptx,mainCell.y+cmptx)
						if cell2 != None:
							rep.append(cell2)
					cmptx+=1
			rep.append(mainCell)
		elif area in [AREA_RANDOMENNEMI_1,AREA_RANDOMENNEMI_2,AREA_RANDOMENNEMI_3,AREA_RANDOMENNEMI_4,AREA_RANDOMENNEMI_5,AREA_RANDOMALLIE_1,AREA_RANDOMALLIE_2,AREA_RANDOMALLIE_3,AREA_RANDOMALLIE_4,AREA_RANDOMALLIE_5]:
			for cell in self.getSingleTabl():
				if (cell.on != None and cell.on.team != team and area <= AREA_RANDOMENNEMI_5) or (cell.on != None and cell.on.team == team and area > AREA_RANDOMENNEMI_5) and type(cell.on.char) != classes.invoc:rep.append(cell)
			nbToReturn, now = area-[AREA_RANDOMENNEMI_1,AREA_RANDOMALLIE_1][area>=AREA_RANDOMALLIE_1]+1, datetime.now()
			while len(rep) < nbToReturn-2: rep.append(rep[random.randint(0,len(rep)-1)])
			random.shuffle(rep)
			return rep[0:min(nbToReturn,len(rep))]
		elif area in [AREA_INLINE_2,AREA_INLINE_3,AREA_INLINE_4,AREA_INLINE_5]:
			for celly in self.getSingleTabl():
				if (celly.x == mainCell.x or celly.y == mainCell.y) and self.distance(cell1=mainCell, cell2=celly) <= area + 2 - AREA_INLINE_2:
					rep.append(celly)
		elif area in [AREA_LOWEST_HP_ALLIE, AREA_LOWEST_HP_ENEMY]:
			listEnt = []
			for a in self.getSingleTabl():
				if a.on != None and [a.on.team == team, a.on.team != team][area == AREA_LOWEST_HP_ENEMY] and a.on.char.__class__ not in [invoc,depl] and a.on.hp > 0:
					listEnt.append(a.on)

			if len(listEnt) > 0:
				listEnt.sort(key=lambda ballerine: ballerine.hp/ballerine.maxHp)
				return [listEnt[0].cell]
			else:
				return []
		elif area in [AREA_SUMMONS]:
			for a in self.getSingleTabl():
				if a.on != None and a.on.team == team and type(a.on.char) == classes.invoc:
					rep.append(a)
		elif area in [AREA_SUMMONER]:
			if mainCell.on != None and type(mainCell.on.char) in [depl, invoc]:
				for cell in self.getSingleTabl():
					if cell.on != None and cell.on.id == mainCell.on.summoner.id:
						return [cell]
		elif area in [AREA_BIGDONUT]:
			for a in self.getSingleTabl():
				if self.distance(cell1=mainCell, cell2=a) == 2:
					rep.append(a)
		elif area in [AREA_HIGHEST_DAMAGE_ENEMY]:
			maxDmg = [None, 0]
			for tmpCell in self.getSingleTabl():
				if tmpCell.on != None and tmpCell.on.team != team and tmpCell.on.stats.damageDeal > maxDmg[1] :
					maxDmg = [tmpCell, tmpCell.on.stats.damageDeal]
			rep = maxDmg[0]
		return rep

	def getEntityOnArea(self, mainCell: cellule, area=AREA_MONO, team=0, wanted=ALLIES, lineOfSight=False, lifeUnderPurcentage=99999, dead=False, effect=[None], ignoreInvoc = False, directTarget=True, ignoreAspiration = None, fromCell=None) -> list: 
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

		if area==AREA_MONO: return [mainCell.on]

		rep = []
		if type(effect)!=list:
			effect = [effect]

		tablArea = self.getArea(mainCell=mainCell,area=area,team=team,fromCell=fromCell)
		enties = []

		for cellule in tablArea:
			ent = None
			if cellule.on != None:														  # If there is a entity on the cell
				ent = cellule.on
			else:
				for celly in cellule.getSurrondings():
					if celly != None and celly.on != None and TRAIT_GIANTESS in celly.on.char.trait:
						if ent not in enties:
							ent = cellule.on
							break

			if ent != None:
				if directTarget:																# If we are looking for a directTarget, take into account if the entity is untargetable
					targetable = not(ent.untargetable)
				else:
					targetable = True

				if ent.hp > 0 and not(dead):
					if mainCell.on != None:
						kitsuFlag = mainCell.on.char.npcTeam in [NPC_KITSUNE,NPC_GOLEM] and ent.char.npcTeam == [NPC_KITSUNE,NPC_GOLEM][ent.char.npcTeam == NPC_KITSUNE]
					else:
						kitsuFlag = False
					allieTeamVerif = ent.team == team and wanted == ALLIES and not(kitsuFlag)
					ennemiTeamVerif = (ent.team != team and wanted == ENEMIES) or kitsuFlag
					if targetable and (allieTeamVerif or ennemiTeamVerif or (wanted == ALL) or (area == AREA_ALL_ENTITES)):
						enties.append(ent)

				elif ent.hp <= 0 and dead:
					if mainCell.on != None:
						kitsuFlag = mainCell.on.char.npcTeam in [NPC_KITSUNE,NPC_GOLEM] and ent.char.npcTeam == [NPC_KITSUNE,NPC_GOLEM][ent.char.npcTeam == NPC_KITSUNE]
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
					celly, direction = ent.cell, getDirection(mainCell,ent.cell)
					if direction == FROM_RIGHT:
						cellToFind = self.findCell(celly.x+1,celly.y)
						if cellToFind != None:
							for celly2 in self.getArea(mainCell=cellToFind, area=AREA_CONE_7,fromCell=mainCell):
								if celly2.on != None and celly.on.team != team and celly2.on in enties:
									enties.remove(celly2.on)
					elif direction == FROM_LEFT:
						cellToFind = self.findCell(celly.x-1,celly.y)
						if cellToFind != None:
							for celly2 in self.getArea(mainCell=cellToFind, area=AREA_CONE_7,fromCell=mainCell):
								if celly2.on != None and celly.on.team != team and celly2.on in enties:
									enties.remove(celly2.on)
					elif direction == FROM_DOWN:
						cellToFind = self.findCell(celly.x,celly.y+1)
						if cellToFind != None:
							for celly2 in self.getArea(mainCell=cellToFind, area=AREA_CONE_7,fromCell=mainCell):
								if celly2.on != None and celly.on.team != team and celly2.on in enties:
									enties.remove(celly2.on)
					elif direction == FROM_UP:
						cellToFind = self.findCell(celly.x,celly.y-1)
						if cellToFind != None:
							for celly2 in self.getArea(mainCell=cellToFind, area=AREA_CONE_7,fromCell=mainCell):
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
		rep.sort(key=lambda toSort: self.distance(cell1=mainCell, cell2=toSort.cell))
		for indx, ent in enumerate(rep):
			if type(ent) == None:
				try:
					rep.remove(ent)
				except:
					pass
			elif ent.isNpc(TGESL1.name):
				rep[indx] = ent.summoner
		return rep

	def getEmptyCellsInArea(self, mainCell:cellule, area=AREA_DONUT_3,team=0):
		"""Return a list of the empty cells in the area"""
		tabl = []
		cells = self.getArea(mainCell, area,team)

		for a in cells:
			if a.on == None:
				tabl.append(a)

		return tabl

	def getCellForSummon(self, mainCell:cellule, area: int, team: int, summon : invoc, summoner: "entity"):
		"""Return the best cell for summon something"""
		tabl = self.getEmptyCellsInArea(mainCell, area,team)
		rangeTabl = {RANGE_MELEE:[2,3],RANGE_DIST:[1,4],RANGE_LONG:[0,5]}[summon.weapon.range][team]

		if len(tabl)>0:
			return sorted(tabl, key = lambda ballerine: cellShort(ballerine, rangeTabl, team), reverse=True)[0]

	def getSurrondings(self, mainCell:cellule, large=False):
		if mainCell.surrondings == None or len(mainCell.surrondings) < 4:
			mainCell.surrondings = [
				self.self.findCell(mainCell.x-1,mainCell.y),
				self.self.findCell(mainCell.x+1,mainCell.y),
				self.self.findCell(mainCell.x,mainCell.y-1),
				self.self.findCell(mainCell.x,mainCell.y+1)
				]
		
		if not(large):
			return mainCell.surrondings
		else:
			return mainCell.getArea(area=AREA_CIRCLE_2)

	def findCell(self, x : int, y : int) -> cellule:
		"""Return the cell in X:Y, if it exist"""
		try: return self.tablCells[x][y]
		except: return None

	def getSingleTabl(self):
		toReturn = []
		for x in range(self.lenX):
			toReturn += self.tablCells[x]
		return toReturn

	def isCellInTabl(self, cellToLook: cellule, tablCell: List[cellule]):
		for tmp in tablCell:
			if (cellToLook.x, cellToLook.y) == (tmp.x, tmp.y): return True
		return False
	def __str__(self):
		try:
			toReturn = ""
			for x in range(self.lenX):
				for y in range(self.lenY):
					toReturn += " {} |".format(self.tablCells[x][y])
				toReturn = toReturn[:-1]+"\n"
			return toReturn
		except:
			print(toReturn)
			print(self.tablCells, "\n =================", format_exc())

def cellShort(tmpCell, rangeTabl, team):
	value = 0
	if tmpCell.x == rangeTabl:
		value += 100
	if tmpCell.x == rangeTabl + [1,-1][team]:
		value += 50
	
	value += abs(2-tmpCell.y)*10
	return value

def infoOther(other: other, user: char):
	weap = other
	repEmb = interactions.Embed(title=weap.name, color=user.color, description=f"Icone : { weap. emoji}")
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

def addExpUser(path: Union[str,char],  exp=3, coins=0):
	if type(path) == str: user = loadCharFile(path)
	else: user = path

	if user.level < MAXLEVEL: user.exp = user.exp + exp
	else: user.exp = 0
	user.currencies = user.currencies + coins

	upLvl = (user.level-1)*50+30

	while user.exp >= upLvl and user.level < MAXLEVEL:
		user.points = user.points + BONUSPOINTPERLEVEL
		if (user.level+1) // 10 == 0: user.points = user.points + 5
		temp, up, stats = user.allStats(), [0, 0, 0, 0, 0, 0, 0], user.allStats()
		for a in range(0, len(stats)):
			stats[a], temp[a] = round(aspiStats[user.aspiration][a]*0.1+aspiStats[user.aspiration][a]*0.9*user.level/50+user.bonusPoints[a]), round(aspiStats[user.aspiration][a]*0.1+aspiStats[user.aspiration][a]*0.9*(user.level+1)/50+user.bonusPoints[a])
			up[a] = temp[a]-stats[a]

		user.strength, user.endurance, user.charisma, user.agility, user.precision, user.intelligence, user.magie = temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6]

		user.exp, user.level = user.exp - upLvl, user.level+1
		upLvl = (user.level-1)*50+30

		if user.level % 5 == 0 and user.autoStuff and user.level <= MAXLEVEL: user.stuff = [getAutoStuff([user.stuff[0], findStuff(user.aimedStuff[0])][user.aimedStuff[0]!=None],user,recommandedStuffStat[user.aspiration]), getAutoStuff([user.stuff[1], findStuff(user.aimedStuff[1])][user.aimedStuff[1]!=None],user,recommandedStuffStat[user.aspiration]), getAutoStuff([user.stuff[2], findStuff(user.aimedStuff[2])][user.aimedStuff[2]!=None],user,recommandedStuffStat[user.aspiration])]
		if user.autoPoint:
			while user.points > 0:
				for recStat in recommandedStat[user.aspiration]:
					if user.bonusPoints[recStat] < MAXBONUSPERSTAT and user.points > 0: user.bonusPoints[recStat], user.points = user.bonusPoints[recStat]+1, user.points-1

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
	user.stuff[0], user.weapon, user.apparaAcc = findStuff(user.stuff[0]), findWeapon(user.weapon), findStuff(user.apparaAcc)

	if user.apparaAcc == None:
		if os.path.exists("./data/images/headgears/{0}.png".format(getEmojiObject(user.stuff[0].emoji).name)): accessoire, pos = PIL.Image.open("./data/images/headgears/{0}.png".format(getEmojiObject(user.stuff[0].emoji).name)), user.stuff[0].position
		else: accessoire  = PIL.Image.new("RGBA", [0,0], (0, 0, 0, 0))

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
					accessoire.size[1])],		  # 0
			[(round(accessoire.size[0]*0.8), round(accessoire.size[1]*0.8))],	# 1
			[(round(accessoire.size[0]*1.2), round(accessoire.size[1]*0.7))],	# 2
			[(round(accessoire.size[0]*0.8), round(accessoire.size[1]*0.8))],	# 3
			# 4
			[None],
			[(round(accessoire.size[0]*1.2), round(accessoire.size[1]*0.7))],	# 5
			[None, (round(accessoire.size[0]*1.3),
					accessoire.size[1])]		   # 6
		],
		[   # IconForm 1
			[None, (round(accessoire.size[0]*1.3), accessoire.size[1])],	# 0
			[(round(accessoire.size[0]*0.7), round(accessoire.size[1]*0.7))],	# 1
			[(round(accessoire.size[0]*1.2), round(accessoire.size[1]*0.7))],	# 2
			[(round(accessoire.size[0]*0.8), round(accessoire.size[1]*0.8))],	# 3
			[None],	# 4
			[(round(accessoire.size[0]*1.2), round(accessoire.size[1]*0.7))],	# 5
			[None, (round(accessoire.size[0]*1.3), accessoire.size[1])]	 # 6
		],
		[   # IconForm 2
			[(round(accessoire.size[0]*0.7), round(accessoire.size[1]*0.6))],	# 0
			[(round(accessoire.size[0]*0.35), round(accessoire.size[1]*0.35))],	# 1
			[(round(accessoire.size[0]*0.4), round(accessoire.size[1]*0.3))],	# 2
			[(round(accessoire.size[0]*0.5), round(accessoire.size[1]*0.5))],	# 3
			[None],	# 4
			[(round(accessoire.size[0]*0.6), round(accessoire.size[1]*0.4))],	# 5
			[(round(accessoire.size[0]*0.7), round(accessoire.size[1]*0.6))]	 # 6
		],
		[   # IconForm 3
			[(round(accessoire.size[0]*0.7), round(accessoire.size[1]*0.6))],	# 0
			[(round(accessoire.size[0]*0.35), round(accessoire.size[1]*0.35))],	# 1
			[(round(accessoire.size[0]*0.4), round(accessoire.size[1]*0.3))],	# 2
			[(round(accessoire.size[0]*0.5), round(accessoire.size[1]*0.5))],	# 3
			[None],	# 4
			[(round(accessoire.size[0]*0.6), round(accessoire.size[1]*0.4))],	# 5
			[(round(accessoire.size[0]*0.7), round(accessoire.size[1]*0.6))]	 # 6
		],
		[   # IconForm 4
			[None, (round(accessoire.size[0]*1.3),
					accessoire.size[1])],		  # 0
			[(round(accessoire.size[0]*0.8), round(accessoire.size[1]*0.8))],	# 1
			[(round(accessoire.size[0]*1.2), round(accessoire.size[1]*0.7))],	# 2
			[(round(accessoire.size[0]*0.8), round(accessoire.size[1]*0.8))],	# 3
			# 4
			[None],
			[(round(accessoire.size[0]*1.2), round(accessoire.size[1]*0.7))],	# 5
			[None, (round(accessoire.size[0]*1.3),
					accessoire.size[1])]		   # 6
		],
		[   # IconForm 5
			[(round(accessoire.size[0]*1), round(accessoire.size[1]*0.8)),
			 (round(accessoire.size[0]*1.3), accessoire.size[1])],		  # 0
			[(round(accessoire.size[0]*0.7), round(accessoire.size[1]*0.7))],	# 1
			[(round(accessoire.size[0]*1.1), round(accessoire.size[1]*0.6))],	# 2
			[(round(accessoire.size[0]*0.8), round(accessoire.size[1]*0.8))],	# 3
			# 4
			[None],
			[(round(accessoire.size[0]*1.0), round(accessoire.size[1]*0.7))],	# 5
			[None, (round(accessoire.size[0]*1.3),
					accessoire.size[1])]		   # 6
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
			 ],							   # 0
			[(0, round(background.size[1]/2)-5),
			 (3, round(background.size[1]/2)-5)],				  # 1
			[(round(background.size[0]/2-accessoire.size[0]/2),
			  round(background.size[1]/2+20))],	# 2
			[(round(background.size[0]*0.25-accessoire.size[0]/2+8), 13),
			 (round(background.size[0]*0.25-accessoire.size[0]/2+3), 7)],	# 3
			[(round(background.size[0]*0.20-accessoire.size[0]/2), 75)
			 ],							 # 4
			[(round(background.size[0]/2-accessoire.size[0]/2),
			  round(background.size[1]/2+10))],	# 5
			[(round(background.size[0]/2-accessoire.size[0]/2), -10)
			 ]								# 6
		],
		[   # IconForm 1
			[(round(background.size[0]/2-accessoire.size[0]/2), -10)
			 ],							   # 0
			[(5, round(background.size[1]*0.1)),
			 (3, round(background.size[1]*0.1))],				  # 1
			[(round(background.size[0]/2-accessoire.size[0]/2),
			  round(background.size[1]/2+20))],	# 2
			[(round(background.size[0]*0.25-accessoire.size[0]/2+8), 13),
			 (round(background.size[0]*0.25-accessoire.size[0]/2+3), 7)],	# 3
			[(round(background.size[0]*0.20-accessoire.size[0]/2), 75)
			 ],							 # 4
			[(round(background.size[0]/2-accessoire.size[0]/2),
			  round(background.size[1]/2+10))],	# 5
			[(round(background.size[0]/2-accessoire.size[0]/2), -10)
			 ]								# 6
		],
		[   # IconForm 2
			[(round(background.size[0]/2-accessoire.size[0]/2), 0)
			 ],									 # 0
			[(round(background.size[0]*0.25), 21)
			 ],								  # 1
			[(round(background.size[0]/2-accessoire.size[0]/2),
			  round(background.size[1]/2+2))],	  # 2
			[(round(background.size[0]*0.25), 15)
			 ],								  # 3
			[(round(background.size[0]*0.20-accessoire.size[0]/2), 75)
			 ],								 # 4
			[(round(background.size[0]/2-accessoire.size[0]/2),
			  round(background.size[1]/2-18))],	 # 5
			[(round(background.size[0]/2-accessoire.size[0]/2), 0)
			 ]									  # 6
		],
		[   # IconForm 3
			[(round(background.size[0]/2-accessoire.size[0]/2), 0)
			 ],									 # 0
			[(round(background.size[0]*0.25), 21)
			 ],								  # 1
			[(round(background.size[0]/2-accessoire.size[0]/2),
			  round(background.size[1]/2+2))],	  # 2
			[(round(background.size[0]*0.25), 15)
			 ],								  # 3
			[(round(background.size[0]*0.20-accessoire.size[0]/2), 75)
			 ],								 # 4
			[(round(background.size[0]/2-accessoire.size[0]/2),
			  round(background.size[1]/2-18))],	 # 5
			[(round(background.size[0]/2-accessoire.size[0]/2), 0)
			 ]									  # 6
		],
		[   # IconForm 4
			[(round(background.size[0]/2-accessoire.size[0]/2), -10)
			 ],							   # 0
			[(0, round(background.size[1]/2)-5),
			 (3, round(background.size[1]/2)-5)],				  # 1
			[(round(background.size[0]/2-accessoire.size[0]/2),
			  round(background.size[1]/2+20))],	# 2
			[(round(background.size[0]*0.25-accessoire.size[0]/2+8), 13),
			 (round(background.size[0]*0.25-accessoire.size[0]/2+3), 7)],	# 3
			[(round(background.size[0]*0.20-accessoire.size[0]/2), 75)
			 ],							 # 4
			[(round(background.size[0]/2-accessoire.size[0]/2),
			  round(background.size[1]/2+10))],	# 5
			[(round(background.size[0]/2-accessoire.size[0]/2), -10)
			 ]								# 6
		],
		[   # IconForm 5
			[(round(background.size[0]/2-accessoire.size[0]/2), 0)
			 ],							   # 0
			[(0, round(background.size[1]/2)-5),
			 (3, round(background.size[1]/2)-5)],				  # 1
			[(round(background.size[0]/2-accessoire.size[0]/2),
			  round(background.size[1]/2+20))],	# 2
			[(round(background.size[0]*0.25-accessoire.size[0]/2+8), 13),
			 (round(background.size[0]*0.25-accessoire.size[0]/2+3), 7)],	# 3
			[(round(background.size[0]*0.20-accessoire.size[0]/2), 75)
			 ],							 # 4
			[(round(background.size[0]/2-accessoire.size[0]/2),
			  round(background.size[1]/2+10))],	# 5
			[(round(background.size[0]/2-accessoire.size[0]/2), 0)
			 ]								# 6
		]
	]

	if pos == 6 and user.showAcc:								 # Behind
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

	if user.customColor == None: colorToUse = hex(user.color).replace("0x", "#")
	else:
		colorToUse = user.colorHex
		if colorToUse in ["None", None]:
			if user.color != black: colorToUse = hex(user.color).replace("0x", "#")
			else: colorToUse = "#000000"
		else:
			user.colorHex.replace("0x", "#")
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
		if pos == 3:										  # Barettes
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
	emb.add_field(name="<:em:866459463568850954>\n{} __{}__".format(invoc.icon[0],invoc.name), value=reduceEmojiNames(f"__Aspiration :__ {aspiEmoji[invoc.aspiration]} {aspiNames[invoc.aspiration]}\n__Elément :__ {elemEmojis[invoc.element]} {elemNames[invoc.element]}\n__Description :__\n{invoc.description}"), inline=False)
	stats, rep = invoc.allStats()+[invoc.resistance, invoc.percing, invoc.critical], ""

	for a in range(0, len(stats)):
		if type(stats[a]) == list:
			if stats[a][0] in [PURCENTAGE,HARMONIE]:
				rep += "\n__{0} {1} :__ {2}%".format(statEmojis[a],allStatsNames[a],highlight(round(stats[a][1]*100)))
				if stats[a][0] == HARMONIE:
					rep += " (Harmonie)"
		else:
			rep += "\n__{0} {1} :__ {2}".format(statEmojis[a],allStatsNames[a],highlight(stats[a]))

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
	var, teamName, listTraitStr = "", "", ""
	if allie.variant:
		for tmpAllie in tablAllAllies:
			if allie.name in tmpAllie.variantTabl.keys(): var += "Cet{0} allié{1} est une variante de {2} {3} ({4}% d'apparition)\n".format(["","te"][allie.gender == GENDER_FEMALE],["","e"][allie.gender == GENDER_FEMALE], tmpAllie.icon,tmpAllie.name,tmpAllie.variantTabl[allie.name]); break
		if var == "":
			var = "Cet{0} allié{1} n'apparait que lors d'évenements spéciaux\n".format(["","te"][allie.gender == GENDER_FEMALE],["","e"][allie.gender == GENDER_FEMALE])
	for key, value in allie.variantTabl.items(): tmpAllie = findAlly(key); var += "Cet{0} allié{1} peut être remplacé{1} par {2} {3} ({4}%) en combat\n".format(["","te"][allie.gender == GENDER_FEMALE],["","e"][allie.gender == GENDER_FEMALE],tmpAllie.icon,tmpAllie.name,value)
	if var != "": var += "\n"
	if allie.npcTeam != None: teamName = "__Affinité :__ {0}{1}\n".format(npcTeamEmojis[allie.npcTeam]+[""," "][npcTeamEmojis[allie.npcTeam]!=""], npcTeamNames[allie.npcTeam])

	for tmp in allie.trait:
		if tmp in traitAccord.keys() and allie.gender == 1:
			listTraitStr += "- {0} {1}\n".format(traitNames[tmp][0], traitAccord[tmp])
		else:
			listTraitStr += "- {0} {1}\n".format(traitNames[tmp][0], traitNames[tmp][1])

	if listTraitStr != "":
		listTraitStr = "\n__Traits :__\n"+listTraitStr

	rep = f"{var}__Aspiration :__ {aspiNames[allie.aspiration]}\n__Element :__ {elemEmojis[allie.element]} {elemNames[allie.element]} ({elemEmojis[allie.secElement]} {elemNames[allie.secElement]})\n{teamName}{listTraitStr}__Description :__\n{allie.description}"
	allMaxStats, accStats, dressStats, flatsStats, statsWeapon = allie.allStats(), allie.stuff[0].allStats(), allie.stuff[1].allStats(), allie.stuff[2].allStats(), allie.weapon.allStats()
	stats = ""
	for a in range(0, len(allMaxStats)): allyStat = int((allMaxStats[a]+accStats[a]+dressStats[a]+flatsStats[a]+statsWeapon[a]) * ((100+allie.limitBreaks[a])/100)); stats += f"{statEmojis[a]} __{nameStats[a]}.__ : {allyStat}\n"

	stats2 = ""
	accStats = [allie.stuff[0].resistance,allie.stuff[0].percing, allie.stuff[0].critical]
	dressStats = [allie.stuff[1].resistance,allie.stuff[1].percing, allie.stuff[1].critical]
	flatsStats = [allie.stuff[2].resistance,allie.stuff[2].percing, allie.stuff[2].critical]
	weaponStats = [allie.weapon.resistance,allie.weapon.percing, allie.weapon.critical]
	statsPlusName = nameStats2
	for num in range(3):
		summation = accStats[num] + dressStats[num] + flatsStats[num] + weaponStats[num]
		stats2 += f"{statEmojis[num+RESISTANCE]} __{statsPlusName[num]}__ : {summation}\n"

	accStats = [allie.stuff[0].negativeHeal, allie.stuff[0].negativeBoost,allie.stuff[0].negativeShield, allie.stuff[0].negativeDirect, allie.stuff[0].negativeIndirect]
	dressStats = [allie.stuff[1].negativeHeal, allie.stuff[1].negativeBoost,allie.stuff[1].negativeShield, allie.stuff[1].negativeDirect, allie.stuff[1].negativeIndirect]
	flatsStats = [allie.stuff[2].negativeHeal, allie.stuff[2].negativeBoost,allie.stuff[2].negativeShield, allie.stuff[2].negativeDirect, allie.stuff[2].negativeIndirect]
	statsPlusName = ["Soins", "Bonus/Malus","Armure", "Dégâts directs", "Dégâts indirect"]
	stats2 += "\n"
	for num in range(5):
		summation = accStats[num]*-1 + dressStats[num]*-1 + flatsStats[num]*-1; stats2 += f"{statEmojis[num+ACT_HEAL_FULL]} __{statsPlusName[num]}__ : {summation}\n"

	tmpField = f"{allie.weapon.emoji} {allie.weapon.name}\n"
	for a in allie.skills:
		if type(a) == skill: tmpField += f"\n{a.emoji} {a.name}"
	
	emb = interactions.Embed(title="__Allié temporaire : "+allie.name+"__", color=allie.color, description= reduceEmojiNames(rep)+"\n<:em:866459463568850954>")
	
	emb.add_field(name="__**Arme et compétences** :__", value=reduceEmojiNames(tmpField),inline=True)
	tmpField = ""
	for a in allie.equippedChips:
		tmpChip = getChip(a)
		if tmpChip != None: tmpField += "{}{}{}\n".format(tmpChip.emoji,[""," "][tmpChip.emoji != ""],tmpChip.name)

	if tmpField != "": emb.add_field(name=["<:em:866459463568850954>\n",""][allie.splashArt==None]+"__**Puces** :__", value=reduceEmojiNames(tmpField),inline=allie.splashArt == None)
	emb.add_field(name="<:em:866459463568850954>\n__**Equipement :**__",value=reduceEmojiNames(f"__Accessoire__ : {allie.stuff[0].emoji} {allie.stuff[0].name}\n__Vêtements__ : {allie.stuff[1].emoji} {allie.stuff[1].name}\n__Chaussures__ : {allie.stuff[2].emoji} {allie.stuff[2].name}\n<:em:866459463568850954>"),inline=False)

	emb.add_field(name="__**Statistiques au niveau {0} :**__".format(allie.level), value=reduceEmojiNames(stats),inline=True)
	emb.add_field(name=["<:em:866459463568850954>\n",""][allie.splashArt==None]+"__**Statistiques secondaires :**__", value=reduceEmojiNames(stats2),inline=allie.splashArt == None)
	emb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.{1}".format(getEmojiObject(allie.icon).id, ["png","gif"][allie.icon[1] == "a"]))

	if allie.splashArt != None: emb.set_image(url=allie.splashArt)

	if allie.changeDict != None:
		for altBuild in allie.changeDict:
			fieldValue = ""
			if altBuild.aspiration != None: fieldValue += "{0}|".format(aspiEmoji[altBuild.aspiration])
			else: fieldValue += "{0}|".format(aspiEmoji[allie.aspiration])
			if altBuild.weapon != None: fieldValue += "{0}|".format(altBuild.weapon.emoji)
			else: fieldValue += "{0}|".format(allie.weapon.emoji)
			if altBuild.stuff != None:
				if altBuild.proba > 0: stuffToSee = [getAutoStuff(altBuild.stuff[0], allie), getAutoStuff(altBuild.stuff[1], allie), getAutoStuff(altBuild.stuff[2], allie)]
				else: stuffToSee = altBuild.stuff
			else: stuffToSee = allie.stuff
			for stuffy in stuffToSee: fieldValue += stuffy.emoji
			fieldValue += "|"
			if altBuild.skills != None: listActSkills = altBuild.skills
			else: listActSkills = allie.skills
			
			for skilly in listActSkills:
				if type(skilly) == skill: fieldValue += skilly.emoji
			tmpName = "Build alternatif"
			if altBuild.buildName != None: tmpName = altBuild.buildName
			emb.add_field(name="<:em:866459463568850954>\n__{1} ({0}%) :__".format(altBuild.proba, tmpName), value=reduceEmojiNames(fieldValue), inline=False)

	if allie.elemAffinity:
		emb = infoEffect(elemResistanceEffects[allie.element],allie,emb)

	return emb

def infoEnnemi(ennemi: octarien):
	teamName, listTraitStr = "", ""
	if ennemi.npcTeam != None:
		teamName = "__Affinité :__ {0}{1}\n".format(npcTeamEmojis[ennemi.npcTeam]+[""," "][npcTeamEmojis[ennemi.npcTeam]!=""], npcTeamNames[ennemi.npcTeam])
	
	for tmp in ennemi.trait:
		if tmp in traitAccord.keys() and ennemi.gender == 1:
			listTraitStr += "- {0} {1}\n".format(traitNames[tmp][0], traitAccord[tmp])
		else:
			listTraitStr += "- {0} {1}\n".format(traitNames[tmp][0], traitNames[tmp][1])

	if listTraitStr != "":
		listTraitStr = "\n__Traits :__\n"+listTraitStr

	rep = f"__Aspiration :__ {aspiNames[ennemi.aspiration]}\n__Niveau Minimum :__ {ennemi.baseLvl}\n__Element :__ {elemEmojis[ennemi.element]} {elemNames[ennemi.element]}\n{teamName}{listTraitStr}\n__Description :__\n{ennemi.description}\n\n__**Statistiques au niveau 50 :**__\n"
	allMaxStats, accStats, dressStats, flatsStats, weapStats = ennemi.allStats(), ennemi.stuff[0].allStats(), ennemi.stuff[1].allStats(), ennemi.stuff[2].allStats(), ennemi.weapon.allStats()
	for a in range(0, len(allMaxStats)):
		enStat = allMaxStats[a]+ accStats[a] + dressStats[a]+flatsStats[a]+weapStats[a]
		rep += f"\n{statEmojis[a]} __{nameStats[a]}__ : {enStat}"

	rep += f"\n\n__**Arme et compétences** :__\n{ennemi.weapon.emoji} __{ennemi.weapon.name}__\n{ennemi.weapon.getSummary()}\n"
	for skilly in ennemi.skills:
		if type(skilly) == skill:
			rep += "{3}{0} __{1}__\n{2}\n".format(skilly.emoji,skilly.name,skilly.getSummary(),["\n",""][rep[-2:] == "\n\n"])

	emb = interactions.Embed(title="__Ennemi : "+ennemi.name +"__", color=ennemi.color, description=rep)
	emb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.{1}".format(getEmojiObject(ennemi.icon).id,["png","gif"][ennemi.icon[1] == "a"]))
	if ennemi.splashArt != None:
		emb.set_image(url=ennemi.splashArt)
	if ennemi.elemAffinity:
		emb = infoEffect(elemResistanceEffects[ennemi.element],ennemi,emb)

	return emb

def getAutoStuff(object: stuff, user: Union[char, tmpAllie], tablStats = None):
	if user.level//5 == object.minLvl//5 or (object.minLvl == MAXLEVEL//10*10 and user.level >= MAXLEVEL) and (type(user) == char and user.have(object)): return object
	else:
		if tablStats == None:
			tablAllStats = object.allStats()+[object.resistance, object.percing, object.critical]+[object.negativeHeal*-1, object.negativeBoost*-1, object.negativeShield*-1, object.negativeDirect*-1, object.negativeIndirect*-1]

			for comp in user.skills:
				if type(comp) == skill and comp.use not in [None, HARMONIE]: tablAllStats[comp.use] += 1
			dictList = []
			for cmpt in range(len(tablAllStats)): dictList.append({"Stats": cmpt, "Value": tablAllStats[cmpt]})

			dictList.sort(key=lambda ballerine: ballerine["Value"], reverse=True)
			dictList = dictList[0:3]

			statsMaxPlace = []
			for a in dictList:
				if a["Value"] > 0: statsMaxPlace.append(a["Stats"])
		
		else:
			statsMaxPlace = tablStats

		if type(user) == char: 
			tablToSee = []
			for tmpStuff in user.stuffInventory:
				tmpStuff = findStuff(tmpStuff)
				tablToSee.append(tmpStuff)
		elif type(user) == tmpAllie: tablToSee = stuffs[:]

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
			if (stuffy.minLvl > user.level or stuffy.type != object.type or getSortValue(stuffy) <= 0) and (object.minLvl//5 >= stuffy.minLvl//5):tablToSee.remove(stuffy)
			elif (stuffy.minLvl > user.level or stuffy.type != object.type or getSortValue(stuffy) <= 0) and (object.minLvl//5 <= stuffy.minLvl//5): tablToSee.remove(stuffy)

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
		title, desc = "<:alice:1069700207345946715> :", "\""
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
		emb.add_field(name="<:lena:1106478667871289455> :",value="\""+lenaTipsMsgTabl[random.randint(0, len(lenaTipsMsgTabl)-1)]+"\"")
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
				entDesc += "\n{0} __{1}__ : {2}".format(statEmojis[cmpt],allStatsNames[cmpt],userStats)

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
	rdm, teamIds = random.randint(1, 999999999), userTeamDb.getAllTeamIds() + dbHandler("teamVic.db").getAllTeamIds()
	for indx, value in enumerate(teamIds[:]):
		if type(value) == list:
			for val2 in value:
				teamIds.append(val2)
		teamIds.remove(value)
	teamIds = set(teamIds)
	while rdm in teamIds: rdm = random.randint(1, 999999999)

	rdm = str(rdm)
	userTeamDb.updateTeam(rdm, [user])
	user.team = rdm
	saveCharFile(user=user)
	return user

catSelect = interactions.ActionRow(interactions.StringSelectMenu([StringSelectOption(label="Players",value="0",description="Show players"),StringSelectOption(label="Allies (équipe bleue)",value="1",description="Show allies"),StringSelectOption(label="Allies (équipe rouge)",value="6",description="Show allies"),StringSelectOption(label="Ennemis",value="2",description="Show ennemis"),StringSelectOption(label="Small Bosses",value="3",description="Show small bosses"),StringSelectOption(label="Stands Alones",value="4",description="Show stands alones bosses"),StringSelectOption(label="Raids",value="5",description="Show raids bosses")],custom_id="catSelect",placeholder="Sort by entity category"))
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
				if not(period): cursory.execute("SELECT * FROM enemyStats")
				else: cursory.execute("SELECT * FROM lastMouthEnemy")
				tempTablResultDict = cursory.fetchall()
				cursory.close()

				for indx, value in enumerate(tempTablResultDict):
					try:
						if destination in [1,6]:
							tempEnt = findAlly(value["name"].replace("_B","").replace("_R",""))
							if tempEnt != None and (destination==1 and value["name"].endswith("_B")) or (destination==6 and value["name"].endswith("_R")): tablResultDict.append([tempEnt,value])
						else:
							tempEnt = findEnnemi(value["name"])
							if tempEnt != None:
								match destination:
									case 2:
										for ent in tablUniqueEnnemies:
											if tempEnt.name == ent.name: tablResultDict.append([tempEnt,value]); break
									case 3:
										for ent in tablBoss:
											if tempEnt.name == ent.name and not(ent.standAlone): tablResultDict.append([tempEnt,value]); break
									case 4:
										for ent in tablBoss:
											if tempEnt.name == ent.name and ent.standAlone: tablResultDict.append([tempEnt,value]); break
									case 5:
										for ent in tablRaidBoss:
											if tempEnt.name == ent.name: tablResultDict.append([tempEnt,value]);break
						
					except: pass
		
		except:
			print_exc()

		if len(tablResultDict) == 0:
			if msg == None: msg = await ctx.send(embeds=interactions.Embed(title="============== Kikimeter ==============",description="No result found"),components=[catSelect])
			else: await msg.edit(embeds=interactions.Embed(title="============== Kikimeter ==============",description="No result found"),components=[catSelect])

			try: respond: interactions.ComponentContext = await bot.wait_for_component(messages=msg,components=[catSelect,sortSelect,buttonsActRow],timeout=60); respond = respond.ctx
			except asyncio.TimeoutError: await msg.edit(embeds=interactions.Embed(title="============== Kikimeter ==============",description="No result found"),components=[]); return 0

			if respond.custom_id == catSelect.components[0].custom_id: destination, sortValue, page = int(respond.values[0]), 0, 0
		else:
			selectSortOptions, cmpt, itemList = [], 0, tablResultDict[0][1].keys()
			itemList = itemList[1:]

			for ballerine in itemList: selectSortOptions.append(interactions.StringSelectOption(label=ballerine,value=str(cmpt))); cmpt += 1
			sortSelect = interactions.ActionRow(interactions.StringSelectMenu(selectSortOptions,custom_id='selectMenu',placeholder="Sort by stat category"))
			tablResultDict.sort(key=lambda ballerine: ballerine[1][itemList[sortValue]],reverse=True)
			description = ""
			for cmpt in range(10*page,min((page+1)*10,len(tablResultDict))):
				if type(tablResultDict[cmpt][0]) == char: icon = await getUserIcon(bot,tablResultDict[cmpt][0])
				else: icon = tablResultDict[cmpt][0].icon
				
				description += "\n{0}. {1} {4}		[{2}] : {3}".format(cmpt,icon,itemList[sortValue],tablResultDict[cmpt][1][itemList[sortValue]],tablResultDict[cmpt][0].name)

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
				try: drawnedChip[pulledChip.id][1] += 1
				except KeyError: drawnedChip[pulledChip.id] = [pulledChip,1]
				chipsPulls+=1

		for cmpt in range(10-chipsPulls):
			randRoll, rarity = random.randint(0,999), RARITY_MYTHICAL
			for rar in range(4):
				if randRoll < probaRarity[rar]: rarity = rar; break
				else: randRoll -= probaRarity[rar]

			listChipPull = [chipCommun,chipRare,chipLegend,chipMythic][rarity][:]
			pulledChip =  listChipPull[random.randint(0,len(listChipPull)-1)]

			nbDrawnedChips, neededChips = 1, nbChipsForLvlUp[user.chipInventory[pulledChip.id].lvl-rarityMinLvl[pulledChip.rarity]]
			if neededChips > 20: tmp = int(neededChips*0.05); nbDrawnedChips += random.randint(0,max(tmp,1))

			try: drawnedChip[pulledChip.id][1] += nbDrawnedChips
			except KeyError: drawnedChip[pulledChip.id] = [user.chipInventory[pulledChip.id],nbDrawnedChips]

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
		for cmpt, toReplace in enumerate(tablToRemplace): toReturn = toReturn.replace(tablToRemove[cmpt],toReplace)
		if len(toReturn) > charLimit:
			tablToRemove = []
			for chipid in drawnedChip:
				if drawnedChip[chipid][0].emoji != "": tablToRemove.append(reduceEmojiNames(drawnedChip[chipid][0].emoji))
			for toReplace in tablToRemove: toReturn = toReturn.replace(toReplace,"")
		if len(toReturn) > charLimit:
			toReturn, nbRarity = "Overload <:iliSip:1119011945157230692>\n", [0,0,0,0]
			for chipid in drawnedChip: nbRarity[drawnedChip[chipid][0].rarity]+=drawnedChip[chipid][1]
			for indx, nbCards in enumerate(nbRarity): toReturn += "{0} x{1}, ".format(rarityEmojis[indx],nbCards)

	return user, toReturn

async def lockMsg(msg:Message, time:int = None):
	compList = copy.deepcopy(msg.components)

	def checkComponent(comp):
		if comp.type in [1, 17]:
			for indx in range(len(comp.components)):
				checkComponent(comp.components[indx])
		elif comp.type in [2, 3, 5, 6, 7, 8]:
			comp.disabled = True
		elif comp.type == 9:
			try: comp.accessory.disabled = True
			except: pass

	for indx in range(len(compList)):
		checkComponent(compList[indx])

	if time != None:
		compList.append(SeparatorComponent(divider=True))
		compList.append(TextDisplayComponent("🔒 Ce message est vérouillé pendant {} secondes (Formulaire envoyé)".format(time)))

	await msg.edit(components=compList)

waitingEmbed = ContainerComponent(
	TextDisplayComponent("Chargement en cours <a:anaisLoading:1319052792006053928>..."),
	accent_color=0x9683ec
)