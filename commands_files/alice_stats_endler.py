import discord, sqlite3, os
from gestion import *
from classes import char, statTabl
from typing import Union

if not(os.path.exists("./data/database/aliceStats.db")):
    temp = open("./data/database/aliceStats.db","bw")
    print("Création du fichier \"aliceStats.db\"")
    temp.close()

tablAdd = ["Damage","Kill","Resu","RecivedDamage","Heal","Armor"]

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
            cursor.close()

    def addUser(self,user : char):
        cursory = self.con.cursor()
        cursory.execute("SELECT * FROM userStats WHERE id = ?",(int(user.owner),))
        result = cursory.fetchall()

        if len(result) == 0:
            cursory.execute("INSERT INTO userStats VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",(int(user.owner),0,0,0,0,0,0,0,0,0,0,0,0,))
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

        tablStats = [stats.damageDeal,stats.ennemiKill,stats.allieResurected,stats.damageRecived,stats.heals,stats.shieldGived]

        for num in range(len(tablAdd)):
            listUpdated.append(result["total{0}".format(tablAdd[num])]+tablStats[num])
            listUpdated.append(max(result["max{0}".format(tablAdd[num])],tablStats[num]))

            if tablStats[num] > records[num]["value"]:
                cursor.execute("UPDATE records SET owner = ?, value = ? WHERE recordName = ?;",(int(user.owner),tablStats[num],"max{0}".format(tablAdd[num])))
                self.con.commit()
                cursor.execute("SELECT * FROM records")
                records = cursor.fetchall()

        cursor.execute("UPDATE userStats SET totalDamage = ?, maxDamage = ?, totalKill = ?, maxKill = ?, totalResu = ?, maxResu = ?, totalRecivedDamage = ?, maxRecivedDamage = ?, totalHeal = ?, maxHeal = ?, totalArmor = ?, maxArmor = ? WHERE id = ?;",(listUpdated[0],listUpdated[1],listUpdated[2],listUpdated[3],listUpdated[4],listUpdated[5],listUpdated[6],listUpdated[7],listUpdated[8],listUpdated[9],listUpdated[10],listUpdated[11],int(user.owner)))
        self.con.commit()
        cursor.close()

    def getUserStats(self, user : char, wanted : str) -> Union[dict,int]:
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM userStats WHERE id = ?",(int(user.owner),))
        result = cursor.fetchall()[0]

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

aliceStatsDb = aliceStatsdbEndler()