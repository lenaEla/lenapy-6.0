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
        id                 INTEGER PRIMARY KEY
                                UNIQUE,
        totalDamage        INTEGER,
        maxDamage          INTEGER,
        totalHeal          INTEGER,
        maxHeal            INTEGER,
        totalArmor         INTEGER,
        maxArmor           INTEGER,
        totalRecivedDamage INTEGER,
        maxRecivedDamage   INTEGER,
        totalKill          INTEGER,
        maxKill            INTEGER,
        totalResu          INTEGER,
        maxResu            INTEGER
    );
    CREATE TABLE records (
        recordName STRING  PRIMARY KEY,
        owner      INTEGER,
        value      INTEGER
    );
"""
maj1 = """
    PRAGMA foreign_keys = 0;

    CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                            FROM userStats;

    DROP TABLE userStats;

    CREATE TABLE userStats (
        id                 INTEGER PRIMARY KEY
                                UNIQUE,
        totalDamage        INTEGER,
        maxDamage          INTEGER,
        totalHeal          INTEGER,
        maxHeal            INTEGER,
        totalArmor         INTEGER,
        maxArmor           INTEGER,
        totalRecivedDamage INTEGER,
        maxRecivedDamage   INTEGER,
        totalKill          INTEGER,
        maxKill            INTEGER,
        totalResu          INTEGER,
        maxResu            INTEGER,
        totalSupp          INTEGER,
        maxSupp            INTEGER
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
        id                  INTEGER PRIMARY KEY
                                    UNIQUE,
        totalDamage         INTEGER,
        maxDamage           INTEGER,
        totalHeal           INTEGER,
        maxHeal             INTEGER,
        totalArmor          INTEGER,
        maxArmor            INTEGER,
        totalRecivedDamage  INTEGER,
        maxRecivedDamage    INTEGER,
        totalKill           INTEGER,
        maxKill             INTEGER,
        totalResu           INTEGER,
        maxResu             INTEGER,
        totalSupp           INTEGER,
        maxSupp             INTEGER,
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
        id                  INTEGER PRIMARY KEY
                                    UNIQUE,
        totalDamage         INTEGER,
        maxDamage           INTEGER,
        totalHeal           INTEGER,
        maxHeal             INTEGER,
        totalArmor          INTEGER,
        maxArmor            INTEGER,
        totalRecivedDamage  INTEGER,
        maxRecivedDamage    INTEGER,
        totalKill           INTEGER,
        maxKill             INTEGER,
        totalResu           INTEGER,
        maxResu             INTEGER,
        totalSupp           INTEGER,
        maxSupp             INTEGER,
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
    Name                PRIMARY KEY,
    NbFight             DEFAULT (0),
    NbWin               DEFAULT (0),
    PurcentFightWin           DEFAULT (0),
    DPTperLevelMoy      DEFAULT (0),
    HealPerLevelMoy     DEFAULT (0),
    ArmorPerLevelMoy    DEFAULT (0),
    BoostPerLevelMoy    DEFAULT (0),
    KillMoy             DEFAULT (0),
    DPTperLevel         DEFAULT (0),
    HealPerLevel        DEFAULT (0),
    ArmorPerLevel       DEFAULT (0),
    BoostPerLevel       DEFAULT (0),
    Kill                DEFAULT (0),
    AllyRaise           DEFAULT (0),
    AllyRaiseMoy        DEFAULT (0)
    );
"""

maj4 = """PRAGMA foreign_keys = 0;

    CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                            FROM userStats;

    DROP TABLE userStats;

    CREATE TABLE userStats (
        id                 INTEGER PRIMARY KEY
                                UNIQUE,
        totalDamage        INTEGER,
        maxDamage          INTEGER,
        totalHeal          INTEGER,
        maxHeal            INTEGER,
        totalArmor         INTEGER,
        maxArmor           INTEGER,
        totalRecivedDamage INTEGER,
        maxRecivedDamage   INTEGER,
        totalKill          INTEGER,
        maxKill            INTEGER,
        totalResu          INTEGER,
        maxResu            INTEGER,
        totalSupp          INTEGER,
        maxSupp            INTEGER,
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
        teamId            INTEGER PRIMARY KEY
                                NOT NULL
                                UNIQUE,
        teamMember0       INTEGER DEFAULT 0,
        teamMember1       INTEGER DEFAULT 0,
        teamMember2       INTEGER DEFAULT 0,
        teamMember3       INTEGER DEFAULT 0,
        teamMember4       INTEGER DEFAULT 0,
        teamMember5       INTEGER DEFAULT 0,
        teamMember6       INTEGER DEFAULT 0,
        teamMember7       INTEGER DEFAULT 0,
        teamLeader        INTEGER,
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
        teamId            INTEGER PRIMARY KEY
                                NOT NULL
                                UNIQUE,
        teamMember0       INTEGER DEFAULT 0,
        teamMember1       INTEGER DEFAULT 0,
        teamMember2       INTEGER DEFAULT 0,
        teamMember3       INTEGER DEFAULT 0,
        teamMember4       INTEGER DEFAULT 0,
        teamMember5       INTEGER DEFAULT 0,
        teamMember6       INTEGER DEFAULT 0,
        teamMember7       INTEGER DEFAULT 0,
        teamLeader        INTEGER,
        settingsAllyIcon  INTEGER DEFAULT (0),
        settingsEnemyIcon INTEGER DEFAULT (0),
        teamName          STRING,
        teamCaptain       INTEGER,
        teamCapLenaExp    INTEGER DEFAULT ( 0),
        teamCapClemenceExp    INTEGER DEFAULT ( 0),
        teamCapHeleneExp    INTEGER DEFAULT ( 0),
        teamCapShehisaExp    INTEGER DEFAULT ( 0),
        teamCapLiuExp    INTEGER DEFAULT ( 0),
        teamCapEdelweissExp    INTEGER DEFAULT ( 0),
        teamCapElinaExp    INTEGER DEFAULT ( 0),
        teamCapIcealiaExp    INTEGER DEFAULT ( 0)
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
        userId              INTEGER PRIMARY KEY
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
        hand                INTEGER DEFAULT 1,
        affElem             BOOLEAN DEFAULT 1,
        affAcc              BOOLEAN DEFAULT 1,
        affWeap             BOOLEAN DEFAULT (1),
        lastDay             STRING  DEFAULT ('0000'),
        weaponUse           INTEGER DEFAULT (1),
        dmgSkillUse           INTEGER DEFAULT (1),
        healSkillUse           INTEGER DEFAULT (1),
        armorSkillUse           INTEGER DEFAULT (1),
        buffSkillUse           INTEGER DEFAULT (1),
        debuffSkillUse           INTEGER DEFAULT (1),
        summonSkillUse           INTEGER DEFAULT (1),
        offTarget           INTEGER DEFAULT (0),
        healTarget           INTEGER DEFAULT (0),
        armorTarget           INTEGER DEFAULT (0),
        buffTarget           INTEGER DEFAULT (0),
        raiseTarget         INTERGER DEFAULT (0)
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

        try: cursor.execute("SELECT * FROM enemyStats;")
        except:
            temp = ""
            for a in enemyStatCreate:
                if a != ";":
                    temp+=a
                else:
                    cursor.execute(temp)
                    temp = ""

            self.con.commit()
            print("enemyStat crée")

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
            
        try: cursor.execute("SELECT explorationStr FROM userTeams;")
        except: cursor.execute("ALTER TABLE userTeams ADD explorationStr STRING DEFAULT \"None\";"); print("explorationStr added")
        try: cursor.execute("SELECT lastExploDate FROM userTeams;")
        except: cursor.execute("ALTER TABLE userTeams ADD lastExploDate STRING DEFAULT \"None\";"); print("lastExploDate added")
        cursor.close()

    def addUser(self,user : char):
        """Add a user in the database\n
        - Parameter\n
            - .user : The ``char`` to add into the database"""
        cursory = self.con.cursor()
        cursory.execute("SELECT * FROM userStats WHERE id = {0}".format(user.owner))
        result = cursory.fetchall()

        if len(result) == 0:
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
        result = cursor.fetchall()[0]
        cursor.execute("SELECT * FROM records")
        records = cursor.fetchall()
        listUpdated = []

        tablStats = [stats.damageDeal,stats.ennemiKill,stats.allieResurected,stats.damageRecived,stats.heals,stats.shieldGived,stats.damageDodged+stats.damageBoosted]

        for num in range(len(tablAdd)):
            listUpdated.append(result["total{0}".format(tablAdd[num])]+tablStats[num])
            listUpdated.append(max(result["max{0}".format(tablAdd[num])],tablStats[num]))

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
        result = cursor.fetchall()

        if len(result) == 0:
            self.addUser(user)
            cursor.execute("SELECT {0} FROM userStats WHERE id = ?".format,(user.owner,))
            result = cursor.fetchall()

        result = result[0]

        if wanted == "all":
            return result
        else:
            return result[wanted]

    def getRecord(self,wanted : str):
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM records")
        result = cursor.fetchall()

        for a in result:
            if a["recordName"] == wanted:
                return a

    def getAdventureProgress(self,user : char):
        cursor = self.con.cursor()
        cursor.execute("SELECT dutyProgressAct, dutyProgressMission FROM userStats WHERE id = ?",(int(user.owner),))
        result = cursor.fetchall()

        if len(result) == 0:
            self.addUser(char)
            cursor.execute("SELECT dutyProgressAct, dutyProgressMission FROM userStats WHERE id = ?",(int(user.owner),))
            result = cursor.fetchall()

        return result[0]["dutyProgressAct"], result[0]["dutyProgressMission"]

    def getUserJetons(self, user : char):
        cursor = self.con.cursor()
        cursor.execute("SELECT jetonOws FROM userStats WHERE id = ?",(user.owner,))
        result = cursor.fetchall()

        if len(result) == 0:
            self.addUser(char)
            cursor.execute("SELECT jetonOws FROM userStats WHERE id = ?",(user.owner,))
            result = cursor.fetchall()

        return result[0]["jetonOws"]

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

    def addEnemyStats(self, enemy: Union[octarien,tmpAllie], tablStats: statTabl, winner:bool):
        cursor = self.con.cursor()
        nameEnemy = enemy.name.replace(" ","")
        cursor.execute("SELECT * FROM enemyStats WHERE Name = ?",(nameEnemy,))
        result = cursor.fetchall()

        if len(result)==0:
            cursor.execute("INSERT INTO enemyStats (Name) VALUES (?)",(nameEnemy,))
            self.con.commit()
            cursor.execute("SELECT * FROM enemyStats WHERE Name = ?",(nameEnemy,))
            result = cursor.fetchall()

        result = result[0]

        dictModifValues = {
            "NbFight" :result["NbFight"]+1,
            "NbWin":result["NbWin"]+int(winner),
            "PurcentFightWin":round((result["NbWin"]+int(winner))/(result["NbFight"]+1),2),
            "DPTperLevel":int(result["DPTperLevel"]+round(tablStats.damageDeal/enemy.level,1)),
            "DPTperLevelMoy":round((result["DPTperLevel"]+round(tablStats.damageDeal/enemy.level,1)) / (result["NbFight"]+1),1),
            "HealPerLevel":result["HealPerLevel"]+round(tablStats.heals/enemy.level,1),
            "HealPerLevelMoy":round((result["HealPerLevel"]+round(tablStats.heals/enemy.level,1)) / (result["NbFight"]+1),1),
            "ArmorPerLevel":result["ArmorPerLevel"]+round(tablStats.shieldGived/enemy.level,1),
            "ArmorPerLevelMoy":round((result["ArmorPerLevel"]+round(tablStats.shieldGived/enemy.level,1)) / (result["NbFight"]+1),1),
            "BoostPerLevel":result["BoostPerLevel"]+round((tablStats.damageBoosted+tablStats.damageDodged)/enemy.level,1),
            "BoostPerLevelMoy":round((result["BoostPerLevel"]+round((tablStats.damageBoosted+tablStats.damageDodged)/enemy.level,1)) / (result["NbFight"]+1),1),
            "Kill":result["Kill"]+tablStats.ennemiKill,
            "KillMoy":round((result["Kill"]+tablStats.ennemiKill)/(result["NbFight"]+1),1),
            "AllyRaise":result["AllyRaise"]+tablStats.allieResurected,
            "AllyRaiseMoy":round((result["AllyRaise"]+tablStats.allieResurected)/(result["NbFight"]+1),1),
        }

        varExect = ""
        for name, value in dictModifValues.items():
            varExect += "{0} = {1}".format(name,value)
            if name != "AllyRaiseMoy": varExect += ", "

        cursor.execute("UPDATE enemyStats SET {0} WHERE Name = ?".format(varExect),(nameEnemy,))
        self.con.commit()

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
        try: cursor.execute("SELECT explorationStr, lastExploDate FROM userTeams WHERE teamId = ?",(team,)); result = cursor.fetchall()
        except: print_exc(); return False, -1, 0
        else: 
            tmpStr = result[0]["explorationStr"]; tmpStr = tmpStr.split(";")
            try: tmpStr2 = datetime.fromisoformat(result[0]["lastExploDate"])
            except: tmpStr2 = None
            if tmpStr[0] not in ["None",""]: return datetime.fromisoformat(tmpStr[0]), int(tmpStr[1]), tmpStr2
            else: return False, -1, None

aliceStatsDb = aliceStatsdbEndler()

