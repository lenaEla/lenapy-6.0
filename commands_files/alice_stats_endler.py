import sqlite3, os
from gestion import *
from classes import char, statTabl
from typing import Union

if not(os.path.exists("./data/database/aliceStats.db")):
    temp = open("./data/database/aliceStats.db","bw")
    print("Création du fichier \"aliceStats.db\"")
    temp.close()

tablAdd = ["Damage","Kill","Resu","RecivedDamage","Heal","Armor","Supp"]

tablCreate = """
    CREATE TABLE userStats (
        id                 INTEGER PRIMARY KEY
                                UNIQUE,
        totalDamage        INTEGER,
        maxDamage          INTEGER,
        totalHeal          INTEGER,
        maxHeal            INTEGER,
        totalArmor         INTEGER,
        maxArmor          INTEGER,
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
class aliceStatsdbEndler:
    def __init__(self):
            self.con = sqlite3.connect(f"./data/database/aliceStats.db")
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

            try:
                cursor.execute("SELECT totalSupp FROM userStats;")
            except:
                temp = ""
                for a in maj1:
                    if a != ";":
                        temp+=a
                    else:
                        cursor.execute(temp)
                        temp = ""

                cursor.execute(temp)
                cursor.execute("UPDATE userStats SET totalSupp = ?, maxSupp = ?;",(0,0))
                #cursor.execute("INSERT INTO records VALUES (?,?,?)",("maxSupp",0,0,))
                self.con.commit()
                print("maj1 réalisée")

            try:
                cursor.execute("SELECT dutyProgressAct FROM userStats;")
            except:
                temp = ""
                for a in maj2:
                    if a != ";":
                        temp+=a
                    else:
                        cursor.execute(temp)
                        temp = ""

                cursor.execute("UPDATE userStats SET dutyProgressAct = ?, dutyProgressMission = ?;",(None,None))
                self.con.commit()
                print("maj2 réalisée")

            cursor.close()

    def addUser(self,user : char):
        cursory = self.con.cursor()
        cursory.execute("SELECT * FROM userStats WHERE id = ?",(int(user.owner),))
        result = cursory.fetchall()

        if len(result) == 0:
            cursory.execute("INSERT INTO userStats VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(int(user.owner),0,0,0,0,0,0,0,0,0,0,0,0,0,0,None,None))
            self.con.commit()
            print("Le personnage {0} a été rajouté à la base de donnée".format(user.name))
        cursory.close()

    def addStats(self, user : char, stats : statTabl):
        cursor = self.con.cursor()
        self.addUser(user)

        cursor.execute("SELECT * FROM userStats WHERE id = ?",(int(user.owner),))
        result = cursor.fetchall()[0]
        cursor.execute("SELECT * FROM records")
        records = cursor.fetchall()
        listUpdated = []

        tablStats = [stats.damageDeal,stats.ennemiKill,stats.allieResurected,stats.damageRecived,stats.heals,stats.shieldGived,stats.damageDogded+stats.damageBoosted]

        for num in range(len(tablAdd)):
            listUpdated.append(result["total{0}".format(tablAdd[num])]+tablStats[num])
            listUpdated.append(max(result["max{0}".format(tablAdd[num])],tablStats[num]))

            if tablStats[num] > records[num]["value"]:
                cursor.execute("UPDATE records SET owner = ?, value = ? WHERE recordName = ?;",(int(user.owner),tablStats[num],"max{0}".format(tablAdd[num])))
                self.con.commit()
                cursor.execute("SELECT * FROM records")
                records = cursor.fetchall()

        cursor.execute("UPDATE userStats SET totalDamage = ?, maxDamage = ?, totalKill = ?, maxKill = ?, totalResu = ?, maxResu = ?, totalRecivedDamage = ?, maxRecivedDamage = ?, totalHeal = ?, maxHeal = ?, totalArmor = ?, maxArmor = ?, totalSupp = ?, maxSupp = ? WHERE id = ?;",(listUpdated[0],listUpdated[1],listUpdated[2],listUpdated[3],listUpdated[4],listUpdated[5],listUpdated[6],listUpdated[7],listUpdated[8],listUpdated[9],listUpdated[10],listUpdated[11],listUpdated[12],listUpdated[13],int(user.owner)))
        self.con.commit()
        cursor.close()

    def getUserStats(self, user : char, wanted : str) -> Union[dict,int]:
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM userStats WHERE id = ?",(int(user.owner),))
        result = cursor.fetchall()

        if len(result) == 0:
            self.addUser(char)
            cursor.execute("SELECT * FROM userStats WHERE id = ?",(int(user.owner),))
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

aliceStatsDb = aliceStatsdbEndler()