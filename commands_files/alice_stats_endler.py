"""The module for the database that keeps the User's fighting stats, and their progress in the Adventure"""

import sqlite3, os, interactions
from adv import findAllie, tmpAllie, findEnnemi, tablUniqueEnnemies, tablBoss, tablRaidBoss
from gestion import *
from classes import char, statTabl
from typing import Union, List
from traceback import format_exc

# Creating the database file...
if not(os.path.exists("./data/database/aliceStats.db")):
	temp = open("./data/database/aliceStats.db","bw")
	print("Création du fichier \"aliceStats.db\"")
	temp.close()

tablAdd = ["Damage","Kill","Resu","RecivedDamage","Heal","Armor","Supp"]
aliceStatsToLook = ""
for a in tablAdd:
	aliceStatsToLook += "total"+a+", max"+a
	if a != tablAdd[-1]:
		aliceStatsToLook += ","

tablCreate = """
	CREATE TABLE userStats (
		id				 INTEGER PRIMARY KEY
								UNIQUE,
		totalDamage		INTEGER,
		maxDamage		  INTEGER,
		totalHeal		  INTEGER,
		maxHeal			INTEGER,
		totalArmor		 INTEGER,
		maxArmor		   INTEGER,
		totalRecivedDamage INTEGER,
		maxRecivedDamage   INTEGER,
		totalKill		  INTEGER,
		maxKill			INTEGER,
		totalResu		  INTEGER,
		maxResu			INTEGER
	);
	CREATE TABLE records (
		recordName STRING  PRIMARY KEY,
		owner	  INTEGER,
		value	  INTEGER
	);
"""
maj1 = """
	PRAGMA foreign_keys = 0;

	CREATE TABLE sqlitestudio_temp_table AS SELECT *
											FROM userStats;

	DROP TABLE userStats;

	CREATE TABLE userStats (
		id				 INTEGER PRIMARY KEY
								UNIQUE,
		totalDamage		INTEGER,
		maxDamage		  INTEGER,
		totalHeal		  INTEGER,
		maxHeal			INTEGER,
		totalArmor		 INTEGER,
		maxArmor		   INTEGER,
		totalRecivedDamage INTEGER,
		maxRecivedDamage   INTEGER,
		totalKill		  INTEGER,
		maxKill			INTEGER,
		totalResu		  INTEGER,
		maxResu			INTEGER,
		totalSupp		  INTEGER,
		maxSupp			INTEGER
	);

	INSERT INTO userStats (
							id,
							totalDamage,
							maxDamage,
							totalHeal,
							maxHeal,
							totalArmor,
							maxArmor,
							totalRecivedDamage,
							maxRecivedDamage,
							totalKill,
							maxKill,
							totalResu,
							maxResu
						)
						SELECT id,
								totalDamage,
								maxDamage,
								totalHeal,
								maxHeal,
								totalArmor,
								maxArmor,
								totalRecivedDamage,
								maxRecivedDamage,
								totalKill,
								maxKill,
								totalResu,
								maxResu
							FROM sqlitestudio_temp_table;

	DROP TABLE sqlitestudio_temp_table;

	PRAGMA foreign_keys = 1;
"""
maj2 = """
	PRAGMA foreign_keys = 0;

	CREATE TABLE sqlitestudio_temp_table0 AS SELECT *
											FROM userStats;

	DROP TABLE userStats;

	CREATE TABLE userStats (
		id				  INTEGER PRIMARY KEY
									UNIQUE,
		totalDamage		 INTEGER,
		maxDamage		   INTEGER,
		totalHeal		   INTEGER,
		maxHeal			 INTEGER,
		totalArmor		  INTEGER,
		maxArmor			INTEGER,
		totalRecivedDamage  INTEGER,
		maxRecivedDamage	INTEGER,
		totalKill		   INTEGER,
		maxKill			 INTEGER,
		totalResu		   INTEGER,
		maxResu			 INTEGER,
		totalSupp		   INTEGER,
		maxSupp			 INTEGER,
		dutyProgressAct,
		dutyProgressMission
	);

	INSERT INTO userStats (
							id,
							totalDamage,
							maxDamage,
							totalHeal,
							maxHeal,
							totalArmor,
							maxArmor,
							totalRecivedDamage,
							maxRecivedDamage,
							totalKill,
							maxKill,
							totalResu,
							maxResu,
							totalSupp,
							maxSupp
						)
						SELECT id,
								totalDamage,
								maxDamage,
								totalHeal,
								maxHeal,
								totalArmor,
								maxArmor,
								totalRecivedDamage,
								maxRecivedDamage,
								totalKill,
								maxKill,
								totalResu,
								maxResu,
								totalSupp,
								maxSupp
							FROM sqlitestudio_temp_table0;

	DROP TABLE sqlitestudio_temp_table0;

	PRAGMA foreign_keys = 1;
"""
maj3 = """
	PRAGMA foreign_keys = 0;

	CREATE TABLE sqlitestudio_temp_table0 AS SELECT *
											FROM userStats;

	DROP TABLE userStats;

	CREATE TABLE userStats (
		id				  INTEGER PRIMARY KEY
									UNIQUE,
		totalDamage		 INTEGER,
		maxDamage		   INTEGER,
		totalHeal		   INTEGER,
		maxHeal			 INTEGER,
		totalArmor		  INTEGER,
		maxArmor			INTEGER,
		totalRecivedDamage  INTEGER,
		maxRecivedDamage	INTEGER,
		totalKill		   INTEGER,
		maxKill			 INTEGER,
		totalResu		   INTEGER,
		maxResu			 INTEGER,
		totalSupp		   INTEGER,
		maxSupp			 INTEGER,
		dutyProgressAct,
		dutyProgressMission,
		dutyResumeRef,
		dutyGroupData,
		jetonOws
	);

	INSERT INTO userStats (
							id,
							totalDamage,
							maxDamage,
							totalHeal,
							maxHeal,
							totalArmor,
							maxArmor,
							totalRecivedDamage,
							maxRecivedDamage,
							totalKill,
							maxKill,
							totalResu,
							maxResu,
							totalSupp,
							maxSupp,
							dutyProgressAct,
							dutyProgressMission
						)
						SELECT id,
								totalDamage,
								maxDamage,
								totalHeal,
								maxHeal,
								totalArmor,
								maxArmor,
								totalRecivedDamage,
								maxRecivedDamage,
								totalKill,
								maxKill,
								totalResu,
								maxResu,
								totalSupp,
								maxSupp,
								dutyProgressAct,
								dutyProgressMission
							FROM sqlitestudio_temp_table0;

	DROP TABLE sqlitestudio_temp_table0;

	PRAGMA foreign_keys = 1;
"""
enemyStatCreate ="""
	CREATE TABLE enemyStats (
	name				PRIMARY KEY,
	NbFight			 DEFAULT (0),
	NbWin			   DEFAULT (0),
	PurcentFightWin		   DEFAULT (0),
	DPTperLevelMoy	  DEFAULT (0),
	HealPerLevelMoy	 DEFAULT (0),
	ArmorPerLevelMoy	DEFAULT (0),
	BoostPerLevelMoy	DEFAULT (0),
	KillMoy			 DEFAULT (0),
	DPTperLevel		 DEFAULT (0),
	HealPerLevel		DEFAULT (0),
	ArmorPerLevel	   DEFAULT (0),
	BoostPerLevel	   DEFAULT (0),
	Kill				DEFAULT (0),
	AllyRaise		   DEFAULT (0),
	AllyRaiseMoy		DEFAULT (0)
	);
"""

maj4 = """PRAGMA foreign_keys = 0;

	CREATE TABLE sqlitestudio_temp_table AS SELECT *
											FROM userStats;

	DROP TABLE userStats;

	CREATE TABLE userStats (
		id				 INTEGER PRIMARY KEY
								UNIQUE,
		totalDamage		INTEGER,
		maxDamage		  INTEGER,
		totalHeal		  INTEGER,
		maxHeal			INTEGER,
		totalArmor		 INTEGER,
		maxArmor		   INTEGER,
		totalRecivedDamage INTEGER,
		maxRecivedDamage   INTEGER,
		totalKill		  INTEGER,
		maxKill			INTEGER,
		totalResu		  INTEGER,
		maxResu			INTEGER,
		totalSupp		  INTEGER,
		maxSupp			INTEGER,
		jetonOws
	);

	INSERT INTO userStats (
							id,
							totalDamage,
							maxDamage,
							totalHeal,
							maxHeal,
							totalArmor,
							maxArmor,
							totalRecivedDamage,
							maxRecivedDamage,
							totalKill,
							maxKill,
							totalResu,
							maxResu,
							totalSupp,
							maxSupp,
							jetonOws
						)
						SELECT id,
								totalDamage,
								maxDamage,
								totalHeal,
								maxHeal,
								totalArmor,
								maxArmor,
								totalRecivedDamage,
								maxRecivedDamage,
								totalKill,
								maxKill,
								totalResu,
								maxResu,
								totalSupp,
								maxSupp,
								jetonOws
							FROM sqlitestudio_temp_table;

	DROP TABLE sqlitestudio_temp_table;

	PRAGMA foreign_keys = 1;
"""
majTeamDb = """
	PRAGMA foreign_keys = 0;

	CREATE TABLE sqlitestudio_temp_table AS SELECT *
											FROM userTeams;

	DROP TABLE userTeams;

	CREATE TABLE userTeams (
		teamId			INTEGER PRIMARY KEY
								NOT NULL
								UNIQUE,
		teamMember0	   INTEGER DEFAULT 0,
		teamMember1	   INTEGER DEFAULT 0,
		teamMember2	   INTEGER DEFAULT 0,
		teamMember3	   INTEGER DEFAULT 0,
		teamMember4	   INTEGER DEFAULT 0,
		teamMember5	   INTEGER DEFAULT 0,
		teamMember6	   INTEGER DEFAULT 0,
		teamMember7	   INTEGER DEFAULT 0,
		teamLeader		INTEGER,
		settingsAllyIcon  INTEGER DEFAULT (0),
		settingsEnemyIcon INTEGER DEFAULT (0) 
	);

	INSERT INTO userTeams (
							teamId,
							teamMember0,
							teamMember1,
							teamMember2,
							teamMember3,
							teamMember4,
							teamMember5,
							teamMember6,
							teamMember7
						)
						SELECT teamId,
								teamMember0,
								teamMember1,
								teamMember2,
								teamMember3,
								teamMember4,
								teamMember5,
								teamMember6,
								teamMember7
							FROM sqlitestudio_temp_table;

	DROP TABLE sqlitestudio_temp_table;

	PRAGMA foreign_keys = 1;
"""

majTeamDb2 = """
	PRAGMA foreign_keys = 0;

	CREATE TABLE sqlitestudio_temp_table AS SELECT *
											FROM userTeams;

	DROP TABLE userTeams;

	CREATE TABLE userTeams (
		teamId			INTEGER PRIMARY KEY
								NOT NULL
								UNIQUE,
		teamMember0	   INTEGER DEFAULT 0,
		teamMember1	   INTEGER DEFAULT 0,
		teamMember2	   INTEGER DEFAULT 0,
		teamMember3	   INTEGER DEFAULT 0,
		teamMember4	   INTEGER DEFAULT 0,
		teamMember5	   INTEGER DEFAULT 0,
		teamMember6	   INTEGER DEFAULT 0,
		teamMember7	   INTEGER DEFAULT 0,
		teamLeader		INTEGER,
		settingsAllyIcon  INTEGER DEFAULT (0),
		settingsEnemyIcon INTEGER DEFAULT (0),
		teamName		  STRING,
		teamCaptain	   INTEGER,
		teamCapLenaExp	INTEGER DEFAULT ( 0),
		teamCapClemenceExp	INTEGER DEFAULT ( 0),
		teamCapHeleneExp	INTEGER DEFAULT ( 0),
		teamCapShehisaExp	INTEGER DEFAULT ( 0),
		teamCapLiuExp	INTEGER DEFAULT ( 0),
		teamCapEdelweissExp	INTEGER DEFAULT ( 0),
		teamCapElinaExp	INTEGER DEFAULT ( 0),
		teamCapIcealiaExp	INTEGER DEFAULT ( 0)
	);

	INSERT INTO userTeams (
							teamId,
							teamMember0,
							teamMember1,
							teamMember2,
							teamMember3,
							teamMember4,
							teamMember5,
							teamMember6,
							teamMember7,
							teamLeader,
							settingsAllyIcon,
							settingsEnemyIcon
						)
						SELECT teamId,
								teamMember0,
								teamMember1,
								teamMember2,
								teamMember3,
								teamMember4,
								teamMember5,
								teamMember6,
								teamMember7,
								teamLeader,
								settingsAllyIcon,
								settingsEnemyIcon
							FROM sqlitestudio_temp_table;

	DROP TABLE sqlitestudio_temp_table;

	PRAGMA foreign_keys = 1;

	"""

userSettingsDbUptade = """
	PRAGMA foreign_keys = 0;

	CREATE TABLE sqlitestudio_temp_table AS SELECT *
											FROM userSettings;

	DROP TABLE userSettings;

	CREATE TABLE userSettings (
		userId			  INTEGER PRIMARY KEY
									NOT NULL
									UNIQUE,
		start,
		ultimate,
		limiteBreak,
		onKill,
		onDeath,
		onResurect,
		blueWinAlive,
		blueWinDead,
		blueLoose,
		redWinAlive,
		redWinDead,
		redLoose,
		blockBigAttack,
		reactBigRaiseAllie,
		reactBigRaiseEnnemy,
		bigRaise,
		reactEnnemyKilled,
		reactAllyKilled,
		hand				INTEGER DEFAULT 1,
		affElem			 BOOLEAN DEFAULT 1,
		affAcc			  BOOLEAN DEFAULT 1,
		affWeap			 BOOLEAN DEFAULT (1),
		lastDay			 STRING  DEFAULT ('0000'),
		weaponUse		   INTEGER DEFAULT (1),
		dmgSkillUse		   INTEGER DEFAULT (1),
		healSkillUse		   INTEGER DEFAULT (1),
		armorSkillUse		   INTEGER DEFAULT (1),
		buffSkillUse		   INTEGER DEFAULT (1),
		debuffSkillUse		   INTEGER DEFAULT (1),
		summonSkillUse		   INTEGER DEFAULT (1),
		offTarget		   INTEGER DEFAULT (0),
		healTarget		   INTEGER DEFAULT (0),
		armorTarget		   INTEGER DEFAULT (0),
		buffTarget		   INTEGER DEFAULT (0),
		raiseTarget		 INTERGER DEFAULT (0)
	);

	INSERT INTO userSettings (
								userId,
								start,
								ultimate,
								limiteBreak,
								onKill,
								onDeath,
								onResurect,
								blueWinAlive,
								blueWinDead,
								blueLoose,
								redWinAlive,
								redWinDead,
								redLoose,
								blockBigAttack,
								reactBigRaiseAllie,
								reactBigRaiseEnnemy,
								bigRaise,
								reactEnnemyKilled,
								reactAllyKilled,
								hand,
								affElem,
								affAcc,
								affWeap,
								lastDay
							)
							SELECT userId,
									start,
									ultimate,
									limiteBreak,
									onKill,
									onDeath,
									onResurect,
									blueWinAlive,
									blueWinDead,
									blueLoose,
									redWinAlive,
									redWinDead,
									redLoose,
									blockBigAttack,
									reactBigRaiseAllie,
									reactBigRaiseEnnemy,
									bigRaise,
									reactEnnemyKilled,
									reactAllyKilled,
									hand,
									affElem,
									affAcc,
									affWeap,
									lastDay
							FROM sqlitestudio_temp_table;

	DROP TABLE sqlitestudio_temp_table;

	PRAGMA foreign_keys = 1;"""

class statTablClass():
	def __init__(self, from_dict:dict = None):
		if from_dict == None:
			self.nbFight = "nbFight"
			self.nbWin = "nbWin"
			self.nbWinSuddenDeath = "nbWinSuddenDeath"
			self.nbLooseSuddenDeath = "nbLooseSuddenDeath"
			self.percentWin = "percentWin"
			self.averageDPT = "averageDPT"
			self.averageHeal = "averageHeal"
			self.averageShield = "averageShield"
			self.averageBoost = "averageBoost"
			self.averageKillCount = "averageKillCount"
			self.averageRaiseCount = "averageRaiseCount"
			self.averageAliveTurn = "averageAliveTurn"
			self.averageLifeSteal = "averageLifeSteal"
			self.averageBlockedDamage = "averageBlockedDamage"
			self.survivalCount = "survivalCount"
			self.averageTakenDamage = "averageTakenDamage"
			self.reducedHeal = "reducedHeal"
			self.averageRedirectedDamage = "averageRedirectedDamage"
			self.buildId = 0
			self.aspiration = 0
		else:
			self.nbFight = from_dict["nbFight"]
			self.nbWin = from_dict["nbWin"]
			self.nbWinSuddenDeath = from_dict["nbWinSuddenDeath"]
			self.nbLooseSuddenDeath = from_dict["nbLooseSuddenDeath"]
			self.percentWin = from_dict["percentWin"]
			self.averageDPT = from_dict["averageDPT"]
			self.averageHeal = from_dict["averageHeal"]
			self.averageShield = from_dict["averageShield"]
			self.averageBoost = from_dict["averageBoost"]
			self.averageKillCount = from_dict["averageKillCount"]
			self.averageRaiseCount = from_dict["averageRaiseCount"]
			self.averageAliveTurn = from_dict["averageAliveTurn"]
			self.averageLifeSteal = from_dict["averageLifeSteal"]
			self.averageBlockedDamage = from_dict["averageBlockedDamage"]
			self.survivalCount = from_dict["survivalCount"]
			self.averageTakenDamage = from_dict["averageTakenDamage"]
			self.averageRedirectedDamage = from_dict["averageRedirectedDamage"]
			self.reducedHeal = from_dict["reducedHeal"]
			self.buildId = from_dict["buildId"]
			self.aspiration = from_dict["aspiration"]

	def __str__(self):
		splited = self.nbWin.split["_"]
		return "statTabl.{0}.{1}".format(splited[1], splited[2])

class aliceStatsdbEndler:
	"""This database keeps the user's fighting stats and their progress in the main adventure"""
	def __init__(self):
		"""Update the database, if needed"""
		self.con = sqlite3.connect(f"./data/database/aliceStats.db",timeout=10,check_same_thread=False)
		self.con.row_factory = sqlite3.Row
		self.database = "aliceStats.db"

		cursor = self.con.cursor()

		# Création de la table
		try:
			cursor.execute("SELECT * FROM userStats;")
		except:
			temp = ""
			for a in tablCreate:
				if a != ";":
					temp+=a
				else:
					cursor.execute(temp)
					temp = ""

			for name in tablAdd:
				cursor.execute("INSERT INTO records VALUES (?,?,?)",("max{0}".format(name),0,0,))

			self.con.commit()
			print("Table userStats et records créé")

		try: cursor.execute("SELECT totalSupp FROM userStats;")
		except:
			temp = ""
			for a in majTeamDb:
				if a != ";":
					temp+=a
				else:
					cursor.execute(temp)
					temp = ""

			cursor.execute(temp)
			self.con.commit()
			print("UserTeams updated")

		try:
			cursor.execute("SELECT dutyProgressAct FROM userStats;")
			temp = ""
			for a in maj4:
				if a != ";":
					temp+=a
				else:
					cursor.execute(temp)
					temp = ""

			self.con.commit()
			print("maj4 done")
		except:
			pass

		try: cursor.execute("SELECT teamLeader FROM userTeams;")
		except:
			temp = ""
			for a in majTeamDb:
				if a != ";":
					temp+=a
				else:
					cursor.execute(temp)
					temp = ""

			cursor.execute(temp)
			self.con.commit()
			print("majTeam1 done")

		try: cursor.execute("SELECT teamName FROM userTeams;")
		except:
			temp = ""
			for a in majTeamDb2:
				if a != ";":
					temp+=a
				else:
					cursor.execute(temp)
					temp = ""

			cursor.execute(temp)
			self.con.commit()
			print("majTeam2 done")

		try: cursor.execute("SELECT weaponUse FROM userSettings;")
		except:
			temp = ""
			for a in userSettingsDbUptade:
				if a != ";": temp+=a
				else: cursor.execute(temp); temp = ""

			cursor.execute(temp)
			self.con.commit()
			print("user Settings updated")

		try:
			cursor.execute("SELECT * FROM enemyStats;")
		except:
			try:
				cursor.execute("DROP TABLE enemyStats;")
				print("enemyStats dropped")
			except: pass
			cursor.execute("CREATE TABLE enemyStats (name STRING, npcType INTEGER DEFAULT 0, buildId INTEGER DEFAULT 0, aspiration INT DEFAULT 0)")
			print("enemyStats created")
			self.con.commit()
		
		changeCounter = 0
		tmpStatTabl = statTablClass()
		tmpStatTabl = tmpStatTabl.__dict__
		for key, value in tmpStatTabl.items():
			try:
				cursor.execute("SELECT {0} FROM enemyStats;".format(value))
			except:
				if "purcent" not in value:
					cursor.execute("ALTER TABLE enemyStats ADD {0} INT DEFAULT 0;".format(value))
				else:
					cursor.execute("ALTER TABLE enemyStats ADD {0} FLOAT DEFAULT 0;".format(value))
				print("{0} added".format(value))
				changeCounter += 1

		if changeCounter > 0:
			print("> Some change in the stats tabl have been noticed, reseting the table...")
			cursor.execute("DELETE FROM enemyStats;")

		try: cursor.execute("SELECT explorationStr FROM userTeams;")
		except: cursor.execute("ALTER TABLE userTeams ADD explorationStr STRING DEFAULT \"None\";"); print("explorationStr added")
		try: cursor.execute("SELECT lastExploDate FROM userTeams;")
		except: cursor.execute("ALTER TABLE userTeams ADD lastExploDate STRING DEFAULT \"None\";"); print("lastExploDate added")
		self.con.commit()
		cursor.close()

	def addUser(self,user : char):
		"""Add a user in the database\n
		- Parameter\n
			- .user : The ``char`` to add into the database"""
		cursory = self.con.cursor()
		cursory.execute("SELECT * FROM userStats WHERE id = {0}".format(user.owner))
		result_data = cursory.fetchall()

		if len(result_data) == 0:
			cursory.execute("INSERT INTO userStats VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(user.owner,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0))
			self.con.commit()
			print("Le personnage {0} a été rajouté à la base de donnée".format(user.name))
		cursory.close()

	def addStats(self, user : char, stats : statTabl):
		"""
			Update the ``user``'s stats into the database\n
			- Parameters :
				- user : The ``char`` to update the stats
				- stats : The ``statTabl`` from witch the bot will increase the stats of the user
		"""
		cursor = self.con.cursor()
		self.addUser(user)

		cursor.execute("SELECT * FROM userStats WHERE id = ?",(int(user.owner),))
		result_data = cursor.fetchall()[0]
		cursor.execute("SELECT * FROM records")
		records = cursor.fetchall()
		listUpdated = []

		tablStats = [stats.damageDeal,stats.ennemiKill,stats.allieResurected,stats.damageRecived,stats.heals,stats.shieldGived,stats.damageDodged+stats.damageBoosted]

		for num in range(len(tablAdd)):
			listUpdated.append(result_data["total{0}".format(tablAdd[num])]+tablStats[num])
			listUpdated.append(max(result_data["max{0}".format(tablAdd[num])],tablStats[num]))

			try:
				if tablStats[num] > records[num]["value"]:
					cursor.execute("UPDATE records SET owner = ?, value = ? WHERE recordName = ?;",(int(user.owner),tablStats[num],"max{0}".format(tablAdd[num])))
					self.con.commit()
					cursor.execute("SELECT * FROM records")
					records = cursor.fetchall()
			except IndexError:
				pass

		cursor.execute("UPDATE userStats SET totalDamage = ?, maxDamage = ?, totalKill = ?, maxKill = ?, totalResu = ?, maxResu = ?, totalRecivedDamage = ?, maxRecivedDamage = ?, totalHeal = ?, maxHeal = ?, totalArmor = ?, maxArmor = ?, totalSupp = ?, maxSupp = ? WHERE id = ?;",(listUpdated[0],listUpdated[1],listUpdated[2],listUpdated[3],listUpdated[4],listUpdated[5],listUpdated[6],listUpdated[7],listUpdated[8],listUpdated[9],listUpdated[10],listUpdated[11],listUpdated[12],listUpdated[13],int(user.owner)))
		self.con.commit()
		cursor.close()

	def getUserStats(self, user : char, wanted : str) -> Union[dict,int]:
		cursor = self.con.cursor()
		temp = ""
		for a in tablAdd:
			temp += "total"+a+", max"+a
			if a != tablAdd[-1]:
				temp += ","
		cursor.execute("SELECT {0} FROM userStats WHERE id = ?".format(aliceStatsToLook),(user.owner,))
		result_data = cursor.fetchall()

		if len(result_data) == 0:
			self.addUser(user)
			cursor.execute("SELECT {0} FROM userStats WHERE id = ?".format,(user.owner,))
			result_data = cursor.fetchall()

		result_data = result_data[0]

		if wanted == "all":
			return result_data
		else:
			return result_data[wanted]

	def getRecord(self,wanted : str):
		cursor = self.con.cursor()
		cursor.execute("SELECT * FROM records")
		result_data = cursor.fetchall()

		for a in result_data:
			if a["recordName"] == wanted:
				return a

	def getAdventureProgress(self,user : char):
		cursor = self.con.cursor()
		cursor.execute("SELECT dutyProgressAct, dutyProgressMission FROM userStats WHERE id = ?",(int(user.owner),))
		result_data = cursor.fetchall()

		if len(result_data) == 0:
			self.addUser(char)
			cursor.execute("SELECT dutyProgressAct, dutyProgressMission FROM userStats WHERE id = ?",(int(user.owner),))
			result_data = cursor.fetchall()

		return result_data[0]["dutyProgressAct"], result_data[0]["dutyProgressMission"]

	def getUserJetons(self, user : char):
		cursor = self.con.cursor()
		cursor.execute("SELECT jetonOws FROM userStats WHERE id = ?",(user.owner,))
		result_data = cursor.fetchall()

		if len(result_data) == 0:
			self.addUser(char)
			cursor.execute("SELECT jetonOws FROM userStats WHERE id = ?",(user.owner,))
			result_data = cursor.fetchall()

		return result_data[0]["jetonOws"]

	def updateJetonsCount(self,user:char,count:int):
		actJeton = self.getUserJetons(user)

		actJeton = int(actJeton+count)
		cursor = self.con.cursor()
		cursor.execute("UPDATE userStats SET jetonOws = ? WHERE id = ?",(actJeton,int(user.owner),))
		self.con.commit()
		cursor.close()

	def updatePauseData(self, user: char, text: Union[str,None]):
		cursor = self.con.cursor()
		if text != None:
			cursor.execute("UPDATE userStats SET dutyResumeRef = '{0}' WHERE id = {1};".format(text,user.owner))
		else:
			cursor.execute("UPDATE userStats SET dutyResumeRef = ? WHERE id = {0};".format(text,user.owner),(None,))
		self.con.commit()

	def getPauseData(self, user: char):
		cursor = self.con.cursor()
		cursor.execute("SELECT dutyResumeRef FROM userStats WHERE id = {0};".format(user.owner))
		return cursor.fetchall[0]["dutyResumeRef"]

	def updateTeamFavData(self, user: char, tabl:List[tmpAllie]):
		text = ""
		for cmpt in range(len(tabl)):
			text += tabl[cmpt].name+"|"
	
		cursor = self.con.cursor()
		if text != None:
			cursor.execute("UPDATE userStats SET dutyGroupData = '{0}' WHERE id = {1};".format(text,user.owner))
		else:
			cursor.execute("UPDATE userStats SET dutyGroupData = ? WHERE id = {0};".format(text,user.owner),(None,))
		self.con.commit()

	def getTeamFavData(self, user: char) -> Union[List[tmpAllie],None,bool]:
		cursor = self.con.cursor()
		cursor.execute("SELECT dutyGroupData FROM userStats WHERE id = {0};".format(user.owner))
		tabl = cursor.fetchall[0]["dutyGroupData"]
		if tabl == None:
			temp, tempTabl = "", []
			for letter in tabl[:]:
				if letter == "|":
					tempTabl.append(temp)
					temp = ""
				else:
					temp += letter
				
			tabl = tempTabl
			for cmpt in range(len(tabl)):
				temp = findAllie(tabl[cmpt])
				if temp != None:
					tabl[cmpt] = temp
				else:
					return False
			
			return tabl
		else:
			return None

	def addEnemyStats(self, enemy: Union[octarien,tmpAllie], tablStats: statTabl, winner:bool, isAlive:bool, overTime=False):
		if [findEnnemi(enemy.name), findAllie(enemy.name)][type(enemy) == tmpAllie] != None:
			if enemy.name == "Chûri-Hinoro": enemy = copy.deepcopy(findAllie("Chûri"))

			cursor = self.con.cursor()
			nameEnemy = enemy.name.replace(" ","")
			npcType = int(type(enemy) == tmpAllie)
			cursor.execute("SELECT * FROM enemyStats WHERE name = ? AND npcType = ? AND buildId = ?",(nameEnemy, npcType, enemy.buildId,))
			result_data = cursor.fetchall()

			if len(result_data) == 0:
				if type(enemy) == octarien:
					cursor.execute("INSERT INTO enemyStats (name, npcType, buildId, aspiration) VALUES (?, ?, ?, ?)",(nameEnemy, npcType, enemy.buildId, enemy.aspiration,))
					self.con.commit()
					cursor.execute("SELECT * FROM enemyStats WHERE name = ? AND npcType = ? AND buildId = ?",(nameEnemy, npcType, enemy.buildId,))
					print("{0} (BuildId = {1}) have been added into the database".format(enemy.name, enemy.buildId))
					result_data = cursor.fetchall()
				else:
					print("{0} build {1} cannot be added into the database (special fight)".format(enemy.name, enemy.buildId))
					cursor.close()
					return 0

			result_data = result_data[0]
			tmpStatClass = statTablClass()

			try:
				nbFight = result_data[tmpStatClass.nbFight] + 1
				dictModifValues = {
					tmpStatClass.nbFight: nbFight,
					tmpStatClass.nbWin: result_data[tmpStatClass.nbWin] + int(winner),
					tmpStatClass.nbWinSuddenDeath: result_data[tmpStatClass.nbWinSuddenDeath] + int(winner and overTime),
					tmpStatClass.nbLooseSuddenDeath: result_data[tmpStatClass.nbLooseSuddenDeath] + int(not(winner) and overTime),
					tmpStatClass.averageDPT: int(result_data[tmpStatClass.averageDPT] + (tablStats.damageDeal / enemy.level)),
					tmpStatClass.averageHeal: int(result_data[tmpStatClass.averageHeal] + (tablStats.heals / enemy.level)),
					tmpStatClass.averageShield: int(result_data[tmpStatClass.averageShield] + (tablStats.shieldGived / enemy.level)),
					tmpStatClass.averageBoost: int(result_data[tmpStatClass.averageBoost] + (tablStats.damageBoosted + tablStats.damageDodged) / enemy.level),
					tmpStatClass.averageKillCount: int(result_data[tmpStatClass.averageKillCount] + (tablStats.ennemiKill / enemy.level)),
					tmpStatClass.averageRaiseCount: int(result_data[tmpStatClass.averageRaiseCount] + (tablStats.allieResurected / enemy.level)),
					tmpStatClass.averageAliveTurn: int(result_data[tmpStatClass.averageAliveTurn] + (tablStats.survival / enemy.level)),
					tmpStatClass.averageLifeSteal: int(result_data[tmpStatClass.averageLifeSteal] + (tablStats.lifeSteal / enemy.level)),
					tmpStatClass.averageBlockedDamage: int(result_data[tmpStatClass.averageBlockedDamage] + (tablStats.damageBlocks / enemy.level)),
					tmpStatClass.survivalCount: result_data[tmpStatClass.survivalCount] + int(isAlive),
					tmpStatClass.averageTakenDamage: int(result_data[tmpStatClass.averageTakenDamage] + (tablStats.damageRecived / enemy.level)),
					tmpStatClass.reducedHeal: int(result_data[tmpStatClass.reducedHeal] + (tablStats.healReduced/ enemy.level)),
					tmpStatClass.averageRedirectedDamage: int(result_data[tmpStatClass.averageRedirectedDamage] + (tablStats.redirectedDamage / enemy.level))
				}
			except IndexError:
				print_exc()
				print(tmpStatClass.nbFight)
				raise

			varExect = ""
			for name, value in dictModifValues.items():
				varExect += "{0} = {1}".format(name,value)
				if name != tmpStatClass.averageRedirectedDamage: varExect += ", "

			cursor.execute("UPDATE enemyStats SET {0} WHERE name = ? AND npcType = ? AND buildId = ?".format(varExect),(nameEnemy, npcType, enemy.buildId))
			self.con.commit()
			cursor.close()
		else:
			print("> Could not process {0}".format(enemy.name))

	def resetRecords(self):
		cursory = self.con.cursor()
		try:
			try:
				cursory.execute("DROP TABLE lastMouthUsers")
				self.con.commit()
			except:
				print_exc()
			
			cursory.execute("CREATE TABLE lastMouthUsers AS SELECT * FROM userStats")

			cursory.execute("UPDATE records SET owner = 0, value = 0;")
			temp = ""
			for a in tablAdd:
				temp += "max{0} = 0".format(a)
				if a != tablAdd[-1]:
					temp += ", "
			cursory.execute("UPDATE userStats SET {0};".format(temp))
			self.con.commit()

			try:
				cursory.execute("DROP TABLE lastMouthEnemy")
				self.con.commit()
			except:
				print_exc()
			
			cursory.execute("CREATE TABLE lastMouthEnemy AS SELECT * FROM enemyStats")
			self.con.commit()

			try:
				cursory.execute("DROP TABLE enemyStats")
				self.con.commit()
			except:
				print_exc()

			temp = ""
			for a in enemyStatCreate:
				if a != ";":
					temp+=a
				else:
					cursory.execute(temp)
					temp = ""
			self.con.commit()

			cursory.close()
			return "Opération réussie"

		except:
			cursory.close()
			return format_exc()

	def updateTeamSettings(self,team:Union[int,str,char],teamSettings:dict):
		cursor = self.con.cursor()
		try:
			if type(team) == char: teamToSee = int(team.team)
			else: teamToSee = int(team)
			
			for setName, setValue in teamSettings.items(): cursor.execute("UPDATE userTeams SET {0} = ? WHERE teamId = ?;".format(setName),(setValue,teamToSee))
			
			self.con.commit()
			cursor.close()
			return True
		except:
			cursor.close()
			print_exc()
			return False

	def setExplorationStr(self, team:int, location:int=-1, departure:Union[datetime,bool]=False):
		if type(departure) == datetime: tmpStr = departure.isoformat()+";"+str(location)
		else: tmpStr = "None;-1"
		cursor = self.con.cursor()
		try: cursor.execute("UPDATE userTeams SET explorationStr = ? WHERE teamId = ?;",(tmpStr,team,)); self.con.commit()
		except: print_exc()

		if tmpStr == "None;-1":
			try: cursor.execute("UPDATE userTeams SET lastExploDate = ? WHERE teamId = ?;",(str(datetime.now(parisTimeZone).isoformat),team,)); self.con.commit()
			except: print_exc()
		cursor.close()

	def getExplorationStr(self, team:int):
		cursor = self.con.cursor()
		try: cursor.execute("SELECT explorationStr, lastExploDate FROM userTeams WHERE teamId = ?",(team,)); result_data = cursor.fetchall()
		except: print_exc(); return False, -1, 0
		else: 
			tmpStr = result_data[0]["explorationStr"]; tmpStr = tmpStr.split(";")
			try: tmpStr2 = datetime.fromisoformat(result_data[0]["lastExploDate"])
			except: tmpStr2 = None
			if tmpStr[0] not in ["None",""]: return datetime.fromisoformat(tmpStr[0]), int(tmpStr[1]), tmpStr2
			else: return False, -1, None

aliceStatsDb = aliceStatsdbEndler()

absAverageDmgPerLevel, absAverageHealPerLevel, absAverageShieldPerLevel, absAverageBoostPerLevel, absAverageDmgRecived, absAverageAntiHeal = [[1,1,1,1,1], [1,1,1,1,1]], [[1,1,1,1,1], [1,1,1,1,1]], [[1,1,1,1,1], [1,1,1,1,1]], [[1,1,1,1,1], [1,1,1,1,1]], [[1,1,1,1,1], [1,1,1,1,1]], [[1,1,1,1,1], [1,1,1,1,1]]
averageCatDict = {BERSERK: 0, OBSERVATEUR:0, POIDS_PLUME:0, IDOLE:3, PREVOYANT:3, TETE_BRULEE:0, MAGE:0, ALTRUISTE:1, ENCHANTEUR:0, PROTECTEUR:2, VIGILANT:1, SORCELER:0, INOVATEUR:3, ATTENTIF:0, MASCOTTE:3, ASPI_NEUTRAL:4}

def calculateAverageStats():
	print("Calculating average stats...")
	try:
		initTime = datetime.now()
		global absAverageDmgPerLevel, absAverageHealPerLevel, absAverageShieldPerLevel, absAverageBoostPerLevel, absAverageDmgRecived, absAverageAntiHeal
		cmpt = 0
		while cmpt < 2:
			cursor = aliceStatsDb.con.cursor()
			cursor.execute("SELECT * FROM enemyStats WHERE npcType = ?;", (cmpt,))
			resultData = cursor.fetchall()
			cursor.close()
			ultimateCounter = [0,0,0,0,0]
			totalDmg, totalHeal, totalShield, totalBoost, totalTaken, totalAntiHeal = [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]
			for rowData in resultData:
				tmpData = statTablClass()
				totalDmg[averageCatDict[rowData["aspiration"]]] += rowData[tmpData.averageDPT]
				totalHeal[averageCatDict[rowData["aspiration"]]] += rowData[tmpData.averageHeal]
				totalShield[averageCatDict[rowData["aspiration"]]] += rowData[tmpData.averageShield]
				totalBoost[averageCatDict[rowData["aspiration"]]] += rowData[tmpData.averageBoost]
				totalTaken[averageCatDict[rowData["aspiration"]]] += rowData[tmpData.averageTakenDamage]
				totalAntiHeal[averageCatDict[rowData["aspiration"]]] += rowData[tmpData.reducedHeal]
				ultimateCounter[averageCatDict[rowData["aspiration"]]] += rowData[tmpData.nbFight]

			for indx in range(5):
				if ultimateCounter[indx] > 0:
					absAverageDmgPerLevel[cmpt][indx] = round(totalDmg[indx] / ultimateCounter[indx])
					absAverageHealPerLevel[cmpt][indx] = round(totalHeal[indx] / ultimateCounter[indx])
					absAverageShieldPerLevel[cmpt][indx] = round(totalShield[indx] / ultimateCounter[indx])
					absAverageBoostPerLevel[cmpt][indx] = round(totalBoost[indx] / ultimateCounter[indx])
					absAverageDmgRecived[cmpt][indx] = round(totalTaken[indx] / ultimateCounter[indx]) 
					absAverageAntiHeal[cmpt][indx] = round(totalAntiHeal[indx] / ultimateCounter[indx])
			print("> Average calculations for {0} done".format(["enemies", "allies"][cmpt]))
			cmpt += 1
		timenow = datetime.now() - initTime
		print("> All done ({0} ms)".format(separeUnit(int(timenow.total_seconds()*1000))))
	except Exception as e:
		print("/!\ An error as occured : {0} /!\ ".format(e))

calculateAverageStats()

listAllCat = ["DPT", "Heal", 'Shield', 'Boost', None, 'Taken', 'survivalCount', None, 'LifeSteal', 'Redirected', 'reduced heal']

def getNpcStats(npcType:int, npcName: str = None):
	dataResultDict, npcAllData, bigStew = {}, [], []
	tmpCursor = aliceStatsDb.con.cursor()
	try:
		if npcName == None:
			tmpCursor.execute("SELECT * FROM enemyStats WHERE npcType = ?;",(npcType,))
		else:
			tmpCursor.execute("SELECT * FROM enemyStats WHERE name = ? AND npcType = ?;",(npcName, npcType))
			
		npcAllData = tmpCursor.fetchall()
	except:
		print_exc()

	tmpCursor.close()

	for singleData in npcAllData:
		tmpStatData = statTablClass().__dict__
		for key, value in tmpStatData.items():
			tmpStatData[key] = singleData[value]
		tmpStatData["buildId"] = singleData["buildId"]
		tmpStatData["aspiration"] = singleData["aspiration"]
		if singleData["name"] in dataResultDict.keys():
			if singleData["buildId"] in dataResultDict[singleData["name"]].keys():
				dataResultDict[singleData["name"]][singleData["buildId"]].append(statTablClass(tmpStatData))
			else:
				dataResultDict[singleData["name"]][singleData["buildId"]] = [statTablClass(tmpStatData)]
		else:
			dataResultDict[singleData["name"]] = {singleData["buildId"]: [statTablClass(tmpStatData)]}

	for entityName in dataResultDict:
		entityDict = dataResultDict[entityName]
		entity: Union[octarien, tmpAllie] = [findEnnemi(entityName), findAllie(entityName)][npcType]
		if entity == None:
			continue
		for buildId in entityDict:
			buildDictList = entityDict[buildId]
			buildName, buildIcon, buildAspiration = "Default Build", entity.icon, entity.aspiration
			if buildId != 0:
				tmpBuild: tempAltBuild = entity.changeDict[buildId-1]
				if tmpBuild == None: continue
				if tmpBuild.buildName != None:
					buildName = tmpBuild.buildName
				else:
					buildName = "Alternative Build #{0}".format(buildId)
				if tmpBuild.buildIcon != None:
					buildIcon = tmpBuild.buildIcon
				elif tmpBuild.aspiration != None:
					buildIcon = aspiEmoji[tmpBuild.aspiration]
				else:
					buildIcon = aspiEmoji[entity.aspiration]
				if tmpBuild.aspiration != None:
					buildAspiration = tmpBuild.aspiration
			tmpDict = {"name": buildName, "icon": buildIcon, "aspiration": buildAspiration, "ownerName": entity.name, "ownerIcon": entity.icon, "nbWin": 0, "nbFight": 0 ,"nbWinSuddenDeath": 0, "nbLooseSuddenDeath": 0, "buildId":buildId}
			total = {}
			for val in listAllCat:
				if val != None:
					tmpDict[val] = 0
					total[val] = 0

			for singleData in buildDictList:
				if singleData.nbFight > 0:
					total["DPT"] += singleData.averageDPT
					total["Heal"] += singleData.averageHeal
					total["Shield"] += singleData.averageShield
					total["Boost"] += singleData.averageBoost
					total["LifeSteal"] +=singleData.averageLifeSteal
					total["Taken"] += singleData.averageTakenDamage
					total["Redirected"] += singleData.averageRedirectedDamage
					total["reduced heal"] += singleData.reducedHeal

					tmpDict["nbWin"] += singleData.nbWin
					tmpDict["nbWinSuddenDeath"] += singleData.nbWinSuddenDeath
					tmpDict["nbLooseSuddenDeath"] += singleData.nbLooseSuddenDeath
					tmpDict["nbFight"] += singleData.nbFight
					tmpDict["survivalCount"] += singleData.survivalCount

			if tmpDict["nbFight"] > 0:
				tmpDict["DPT"] = round(total["DPT"] / tmpDict["nbFight"] , 2)
				tmpDict["Heal"] = round(total["Heal"] / tmpDict["nbFight"] , 2)
				tmpDict["Shield"] = round(total["Shield"] / tmpDict["nbFight"] , 2)
				tmpDict["Boost"] = round(total["Boost"] / tmpDict["nbFight"] , 2)
				tmpDict["LifeSteal"] = round(total["LifeSteal"] / tmpDict["nbFight"] , 2)
				tmpDict["Taken"] = round(total["Taken"] / tmpDict["nbFight"] , 2)
				tmpDict["Redirected"] = round(total["Redirected"] / tmpDict["nbFight"] , 2)
				tmpDict["reduced heal"] = round(total["reduced heal"] / tmpDict["nbFight"] , 2)
			bigStew.append(tmpDict)
	return bigStew

def getGeneralStat(dictStats: List[dict], entity: Union[octarien, tmpAllie], entityType:int):
	totalWinCount, totalFightCount, winDuringSuddenDeath = 0, 0, 0

	for tmpKey in dictStats:
		totalFightCount, totalWinCount, winDuringSuddenDeath = totalFightCount + tmpKey["nbFight"], totalWinCount + tmpKey["nbWin"], winDuringSuddenDeath + tmpKey["nbWinSuddenDeath"]
	description = "__Total Win Percent :__ {0}% *({2} / {1})*".format(round(totalWinCount / totalFightCount * 100, 2), totalFightCount, totalWinCount)
	description += "\n__Victoires durant Mort Subites :__ {0} *({1} / {2})*".format(round(winDuringSuddenDeath / totalWinCount * 100, 2), winDuringSuddenDeath, totalWinCount)

	listText = ["dmg", "heal", "armor", "boost", None, "dmg recived", "Survival rate", None, "life steal", "damage redirected", "anti-heal"]
	listEmojis = ["<:berkSlash:916210295867850782>", "<:AltyRegen:994748551932428319>", "<:matriceArmor2B:1241381818901725305>", "<:dmncrit:1045691517307719701>", None, "<:matruceArmor1R:1241381785254756514>", "<:concentration:1138879338805211156>", None, "<:vampire:900312789686571018>", "<:cover:1061384419212005417>", "<:deepWound:1188192336652546079>"]
	listAverageTabl = [absAverageDmgPerLevel[entityType], absAverageHealPerLevel[entityType], absAverageShieldPerLevel[entityType], absAverageBoostPerLevel[entityType], None, absAverageDmgRecived[entityType], None, None, None, None, absAverageAntiHeal[entityType]]

	toReturn = Embed(title="__Statistiques :__ {0} (Résumé)".format(entity.name), color=entity.color, description=description)
	toReturn.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.webp".format(int(PartialEmoji.from_str(entity.icon).id)))

	dictStats.sort(key=lambda item: round(item["nbWin"] / max(item["nbFight"], 1) * 100, 2) - item["nbFight"] * 0.0001, reverse=True)
	for tmpDict in dictStats:
		if tmpDict["nbFight"] > 0:
			fieldValue = ""
			for indx, txt in enumerate(listText):
				if txt != None:
					if tmpDict[listAllCat[indx]] > 0:
						if txt not in ["Survival rate"]:
							fieldValue += "> - {3} __{0}{1}:__ {2}\n".format(txt[0].upper(), txt[1:], separeUnit(round(tmpDict[listAllCat[indx]])), listEmojis[indx])
							if listAverageTabl[indx] != None and tmpDict[listAllCat[indx]] > 1 and listAverageTabl[indx][averageCatDict[tmpDict["aspiration"]]] != 0:
								averageRatio = round((tmpDict[listAllCat[indx]] / listAverageTabl[indx][averageCatDict[tmpDict["aspiration"]]] * 100) - 100, 2)
								fieldValue += ">   - Average : {0} *({1}{2}%)*\n".format(listAverageTabl[indx][averageCatDict[tmpDict["aspiration"]]], ["+",""][averageRatio <= 0], averageRatio)
						else:
							fieldValue += "> - {2} __{0} :__ {1}%\n".format(txt, round(tmpDict["survivalCount"] / tmpDict["nbFight"] * 100, 2), listEmojis[indx])
				else:
					fieldValue += "\n"

			toReturn.add_field(name=reduceEmojiNames("<:empty:866459463568850954>\n{1} __{0} :__".format(tmpDict["name"], tmpDict["icon"])), value=reduceEmojiNames("__Victory Rate :__ {0}% *({1} / {2}))*\n".format(round(tmpDict["nbWin"] / tmpDict["nbFight"] * 100, 2), tmpDict["nbWin"], tmpDict["nbFight"])+fieldValue), inline=len(dictStats) >= 3)
	toReturn.set_footer(text="All values ​​are expressed divided by the level of the npc during their fights")

	lenField = len(toReturn.fields)
	if lenField >= 3:
		for indx in range(lenField):
			if (indx == 0 or indx == lenField -1):
				toReturn.fields[indx].inline = False

	if toReturn.__len__() > EMBED_TOTAL_MAX:
		if lenField > 4:
			for indx, value in enumerate(toReturn.fields):
				if indx >= 2 and indx <= lenField - 2:
					toReturn.fields.remove(value)

			toReturn.fields.insert(2, EmbedField(name="<:empty:866459463568850954>\nDue the character limits, some build had to be hided from this list...", value="-# Only the top 2 and bottom 2 builds are showed", inline=False))
	return toReturn

async def npcStatsFunction(ctx: interactions.SlashContext, npcName:str, npcType:int):
	await defer(ctx)

	if npcType == None:
		npcType = 1

	entity = [findEnnemi(npcName), findAllie(npcName)][npcType]
	if entity != None:
		dictData = getNpcStats(npcType=npcType, npcName=npcName)
		await respond(ctx, embeds=getGeneralStat(dictStats=dictData, entity=entity, entityType=npcType))
	else:
		await respond(ctx, content="Npc not found")

async def npcRankingFunction(ctx:interactions.SlashContext, npcType: int):
	await defer(ctx)
	bigStew = getNpcStats(npcType = npcType)
	topWinRatio = sorted(bigStew, key=lambda item: round((item["nbWin"] + [item["nbWinSuddenDeath"] * -1, item["nbLooseSuddenDeath"]][npcType]) / max(1,item["nbFight"]) * 100, 2) + item["nbFight"] * 0.0000001, reverse=True)
	top, worst = "__Top Win Ratio :__\n", "__Worst Win Ratio :__\n"
	for indx in range(10):
		try:
			tmpBuild = topWinRatio[indx]
			top += "- {0} __{1} :__\n> - {2} {3} : {4}% *({5} / {6})*\n".format(
				tmpBuild["ownerIcon"], tmpBuild["ownerName"], tmpBuild["icon"], tmpBuild["name"], round(tmpBuild["nbWin"] / max(1,tmpBuild["nbFight"]) * 100, 2), tmpBuild["nbWin"], tmpBuild["nbFight"])
		except IndexError:
			pass
		try:
			tmpBuild = topWinRatio[-(indx+1)]
			worst += "- {0} __{1} :__\n> - {2} {3} : {4}% *({5} / {6})*\n".format(
				tmpBuild["ownerIcon"], tmpBuild["ownerName"], tmpBuild["icon"], tmpBuild["name"], round(tmpBuild["nbWin"] / max(1,tmpBuild["nbFight"]) * 100, 2), tmpBuild["nbWin"], tmpBuild["nbFight"])
		except IndexError:
			pass

	toReturn = Embed(title="__npc ranking__", description=top + "\n" + worst, color=light_blue)
	await respond(ctx, embeds=toReturn)

def npcGetLowestBuild():
	"""Return an `tmpAlly` object with the lowest fight count"""
	stew = getNpcStats(npcType=1)
	stew.sort(key=lambda data: data["nbFight"])

	while stew[0]["ownerName"] == "Akia":
		stew.pop(0)
	entity = findAllie(stew[0]["ownerName"])

	print("> Current lowest count build : {0} ({1}), {2}".format(entity.name, ["Default", "Alt Build #{0}".format(stew[0]["buildId"] -1)][stew[0]["buildId"] > 0], stew[0]["nbFight"]))
	if stew[0]["buildId"] == 0:
		return entity
	else:
		try:
			tmp = getAllieFromBuild(entity, entity.changeDict[stew[0]["buildId"]-1])
		except:
			print(entity.name, entity.changeDict, stew[0]["buildId"]-1)
			raise Exception("Index Out Of Range : {0} {1} {2}".format(entity.name, entity.changeDict, stew[0]["buildId"]-1))
		return tmp