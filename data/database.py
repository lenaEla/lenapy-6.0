import sqlite3, classes, datetime, adv, discord
from typing import List, Union

majTeamVic2 = """
    PRAGMA foreign_keys = 0;

    CREATE TABLE sqlitestudio_temp_table0 AS SELECT *
                                            FROM teamVictory;

    DROP TABLE teamVictory;

    CREATE TABLE teamVictory (
        id                     PRIMARY KEY
                            UNIQUE
                            NOT NULL,
        [1],
        [2],
        [3],
        [4],
        [5],
        [6],
        [7],
        [8],
        [9],
        [10],
        lastFight,
        lastQuickFight,
        isFighting,
        totalWin,
        totalFight,
        fightingInfo
    );

    INSERT INTO teamVictory (
                                id,
                                [1],
                                [2],
                                [3],
                                [4],
                                [5],
                                [6],
                                [7],
                                [8],
                                [9],
                                [10],
                                lastFight,
                                lastQuickFight,
                                isFighting,
                                totalWin,
                                totalFight
                            )
                            SELECT id,
                                "1",
                                "2",
                                "3",
                                "4",
                                "5",
                                "6",
                                "7",
                                "8",
                                "9",
                                "10",
                                lastFight,
                                lastQuickFight,
                                isFighting,
                                totalWin,
                                totalFight
                            FROM sqlitestudio_temp_table0;

    DROP TABLE sqlitestudio_temp_table0;

    PRAGMA foreign_keys = 1;
"""
majTeamVic1 = """
    PRAGMA foreign_keys = 0;

    CREATE TABLE sqlitestudio_temp_table0 AS SELECT *
                                            FROM teamVictory;

    DROP TABLE teamVictory;

    CREATE TABLE teamVictory (
        id                     PRIMARY KEY
                            UNIQUE
                            NOT NULL,
        [1],
        [2],
        [3],
        [4],
        [5],
        [6],
        [7],
        [8],
        [9],
        [10],
        lastFight,
        lastQuickFight,
        isFighting     BOOLEAN,
        totalWin,
        totalFight
    );

    INSERT INTO teamVictory (
                                id,
                                [1],
                                [2],
                                [3],
                                [4],
                                [5],
                                [6],
                                [7],
                                [8],
                                [9],
                                [10],
                                lastFight,
                                lastQuickFight,
                                isFighting
                            )
                            SELECT id,
                                "1",
                                "2",
                                "3",
                                "4",
                                "5",
                                "6",
                                "7",
                                "8",
                                "9",
                                "10",
                                lastFight,
                                lastQuickFight,
                                isFighting
                            FROM sqlitestudio_temp_table0;

    DROP TABLE sqlitestudio_temp_table0;

    PRAGMA foreign_keys = 1;
"""
majTeamVic3 = """
    PRAGMA foreign_keys = 0;

    CREATE TABLE sqlitestudio_temp_table0 AS SELECT *
                                            FROM teamVictory;

    DROP TABLE teamVictory;

    CREATE TABLE teamVictory (
        id                     PRIMARY KEY
                            UNIQUE
                            NOT NULL,
        [1],
        [2],
        [3],
        [4],
        [5],
        [6],
        [7],
        [8],
        [9],
        [10],
        lastFight,
        lastQuickFight,
        isFighting,
        totalWin,
        totalFight,
        fightingInfo,
        fightingChannel
    );

    INSERT INTO teamVictory (
                                id,
                                [1],
                                [2],
                                [3],
                                [4],
                                [5],
                                [6],
                                [7],
                                [8],
                                [9],
                                [10],
                                lastFight,
                                lastQuickFight,
                                isFighting,
                                totalWin,
                                totalFight,
                                fightingInfo
                            )
                            SELECT id,
                                "1",
                                "2",
                                "3",
                                "4",
                                "5",
                                "6",
                                "7",
                                "8",
                                "9",
                                "10",
                                lastFight,
                                lastQuickFight,
                                isFighting,
                                totalWin,
                                totalFight,
                                fightingInfo
                            FROM sqlitestudio_temp_table0;

    DROP TABLE sqlitestudio_temp_table0;

    PRAGMA foreign_keys = 1;
"""
majUserIcon1 = """
PRAGMA foreign_keys = 0;

CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM custom_icon;

DROP TABLE custom_icon;

CREATE TABLE custom_icon (
    owner_id    PRIMARY KEY
                UNIQUE
                NOT NULL,
    espece      DEFAULT (1),
    couleur     DEFAULT (0),
    accessoire  DEFAULT ('ha'),
    arme        DEFAULT ('af'),
    emoji       DEFAULT ('<:LenaWhat:760884455727955978>'),
    iconForm    DEFAULT (0),
    appaWeap    DEFAULT (NULL),
    appaAcc     DEFAULT (NULL)
);

INSERT INTO custom_icon (
                            owner_id,
                            espece,
                            couleur,
                            accessoire,
                            arme,
                            emoji
                        )
                        SELECT owner_id,
                               espece,
                               couleur,
                               accessoire,
                               arme,
                               emoji
                          FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;

PRAGMA foreign_keys = 1;
"""

class dbHandler():
    def __init__(self, database : str):
        self.con = sqlite3.connect(f"./data/database/{database}")
        self.con.row_factory = sqlite3.Row
        self.database = database

        if database=="teamVic.db":
            cursor = self.con.cursor()

            # MajTeamVic1
        
            try:
                cursor.execute("SELECT totalWin FROM teamVictory;")
            except:
                temp = ""
                for a in majTeamVic1:
                    if a != ";":
                        temp+=a
                    else:
                        cursor.execute(temp)
                        temp = ""

                cursor.execute("UPDATE teamVictory SET totalWin = ?, totalFight = ?;",(0,0))
                self.con.commit()
                print("majTeamVic1 réalisée")

            try:
                cursor.execute("SELECT fightingInfo FROM teamVictory;")
            except:
                temp = ""
                for a in majTeamVic2:
                    if a != ";":
                        temp+=a
                    else:
                        cursor.execute(temp)
                        temp = ""

                cursor.execute("UPDATE teamVictory SET fightingInfo = ?;",(';',))
                self.con.commit()
                print("majTeamVic2 réalisée")                
        
            try:
                cursor.execute("SELECT fightingChannel FROM teamVictory;")
            except:
                temp = ""
                for a in majTeamVic3:
                    if a != ";":
                        temp+=a
                    else:
                        cursor.execute(temp)
                        temp = ""

                cursor.execute("UPDATE teamVictory SET fightingChannel = ?;",(0,))
                self.con.commit()
                print("majTeamVic3 réalisée")                

        elif database=="custom_icon.db":
            cursor = self.con.cursor()
            try:
                cursor.execute("SELECT iconForm FROM custom_icon;")
            except:
                temp = ""
                for a in majUserIcon1:
                    if a != ";":
                        temp+=a
                    else:
                        cursor.execute(temp)
                        temp = ""

                self.con.commit()
                print("majUserIcon1 réalisée")

    def addIconFiles(self,species:int,color:int,file):
        cursor = self.con.cursor()
        params = (species,color,file)
        query = "INSERT INTO color_icon VALUES (?,?,?);"
        try:
            cursor.execute(query,params)
        except:
            pass
        cursor.close()
        self.con.commit()

    def getIdFromEmoji(self,emoji,where):
        for obj in adv.stuffs + adv.weapons:
            if obj.emoji == emoji:
                return obj.id

    def haveCustomIcon(self,user):
        cursor = self.con.cursor()
        query = f"SELECT owner_id FROM custom_icon WHERE owner_id = ?;"
        cursor.execute(query,(user.owner,))
        result = cursor.fetchall()
        cursor.close()
        return len(result) > 0

    def editCustomIcon(self,user:classes.char,emoji:discord.Emoji):
        cursor = self.con.cursor()
        if user.apparaAcc != None:
            blbl1 = user.apparaAcc.id
        else:
            blbl1 = None
        if user.apparaWeap != None:
            blbl2 = user.apparaWeap.id
        else:
            blbl2 = None
        if self.haveCustomIcon(user):
            params = (user.species, user.color, user.stuff[0].id, user.weapon.id, str(emoji), blbl2, blbl1, user.iconForm, user.owner)
            query = "UPDATE custom_icon SET espece = ?, couleur = ?, accessoire = ?, arme = ?, emoji = ?, appaWeap = ?, appaAcc = ?, iconForm = ? WHERE owner_id = ?;"
            cursor.execute(query,params)
            cursor.close()
            self.con.commit()
        else:
            params = (user.owner,user.species, user.color, user.stuff[0].id, user.weapon.id, str(emoji), blbl2, blbl1, user.iconForm)
            query = "INSERT INTO custom_icon VALUES (?,?,?,?,?,?,?,?,?)"
            cursor.execute(query,params)
            cursor.close()
            self.con.commit()

    def getCustomIcon(self,user):
        cursor = self.con.cursor()
        query = f"SELECT emoji FROM custom_icon WHERE owner_id = ?;"
        cursor.execute(query,(user.owner,))
        result = cursor.fetchall()
        cursor.close()
        try:
            return result[0]["emoji"]
        except:
            return '<:LenaWhat:760884455727955978>'

    def isDifferent(self,user:classes.char):
        query = f"SELECT * FROM custom_icon WHERE owner_id = ?;"
        cursor = self.con.cursor()
        cursor.execute(query,(user.owner,))
        result = cursor.fetchone()
        cursor.close()
        if result != None:
            return not(result["espece"] == user.species and result["couleur"]==user.color and ((user.apparaAcc==None and result["accessoire"]==user.stuff[0].id) or (user.apparaAcc!=None and user.apparaAcc.id == result["appaAcc"])) and ((user.apparaWeap == None and result["arme"]==user.weapon.id) or (user.apparaWeap!=None and user.apparaWeap.id == result["appaWeap"])) and result["couleur"]==user.color and user.iconForm == result["iconForm"])
        else:
            return True

    def getVictoryStreak(self,user):
        team = user.team
        if user.team == 0:
            team = user.owner
        cursor = self.con.cursor()
        query = f"SELECT * FROM teamVictory WHERE id = ?;"
        cursor.execute(query,(int(team),))
        result = cursor.fetchall()

        if len(result) > 0:
            result = result[0]
            win = 0
            tabl = [result["1"],result["2"],result["3"],result["4"],result["5"],result["6"],result["7"],result["8"],result["9"],result["10"]]
            for a in tabl:
                if a:
                    win += 1
            return win

        else:
            query = "INSERT INTO teamVictory VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,';',0);"
            params = (int(team),True,False,True,False,True,False,True,False,True,False,datetime.datetime.min.strftime("%m/%d/%Y, %H:%M:%S"),datetime.datetime.min.strftime("%m/%d/%Y, %H:%M:%S"),False,0,0)
            cursor.execute(query,params)
            cursor.close()
            self.con.commit()
            return 5

        cursor.close()

    def getVictoryStreakStr(self,user):
        team = user.team
        if user.team == 0:
            team = user.owner
        cursor = self.con.cursor()
        query = f"SELECT * FROM teamVictory WHERE id = ?;"
        cursor.execute(query,(int(team),))
        result = cursor.fetchall()

        if len(result) > 0:
            result = result[0]
            win = ""
            tabl = [result["1"],result["2"],result["3"],result["4"],result["5"],result["6"],result["7"],result["8"],result["9"],result["10"]]
            cmpt = 0
            winCmpt = 0
            while cmpt < 10:
                if tabl[cmpt]:
                    win += "🟢"
                    winCmpt += 1
                else:
                    win += "🔴"

                if cmpt != 9:
                    win += ","

                cmpt += 1
            win += "\n__Taux de victoire des derniers combats :__ {0}%".format(int(winCmpt/10*100))
            try:
                win += "\n__Taux de victoire total :__ {0}%".format(round(result["totalWin"]/result["totalFight"]*100,1))
            except:
                pass
            return win

        else:
            query = "INSERT INTO teamVictory VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
            params = (int(team),True,False,True,False,True,False,True,False,True,False,datetime.datetime.min.strftime("%m/%d/%Y, %H:%M:%S"),datetime.datetime.min.strftime("%m/%d/%Y, %H:%M:%S"),False,0,0)
            cursor.execute(query,params)
            cursor.close()
            self.con.commit()
            return "🟢,🔴,🟢,🔴,🟢,🔴,🟢,🔴,🟢,🔴"

        cursor.close()

    def addResultToStreak(self,user,resultat : bool):
        team = user.team
        if team == 0:
            team = user.owner
        cursor = self.con.cursor()
        query = f"SELECT * FROM teamVictory WHERE id = ?;"
        cursor.execute(query,(int(team),))
        result = cursor.fetchall()
        if len(result) > 0:
            result = result[0]
        else:
            query = "INSERT INTO teamVictory VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
            params = (int(team),True,False,True,False,True,False,True,False,True,False,datetime.datetime.min.strftime("%m/%d/%Y, %H:%M:%S"),datetime.datetime.min.strftime("%m/%d/%Y, %H:%M:%S"),False,0,0)
            cursor.execute(query,params)
            cursor.close()
            self.con.commit()
            query = f"SELECT * FROM teamVictory WHERE id = ?;"
            cursor.execute(query,(team,))
            result = cursor.fetchall()[0]

        nbWin = result["totalWin"]
        nbWin += int(resultat)

        params = (resultat, result["1"], result["2"], result["3"], result["4"], result["5"], result["6"], result["7"], result["8"], result["9"], nbWin, result["totalFight"]+1, team,)
        query = "UPDATE teamVictory SET '1'=?, '2'=?, '3'=?, '4'=?, '5'=?, '6'=?, '7'=?, '8'=?, '9'=?, '10'=?, totalWin = ?, totalFight=? WHERE id = ?;"
        cursor.execute(query,params)
        self.con.commit()
        cursor.close()

    def addShop(self,shop : list):
        cursor = self.con.cursor()
        cursor.execute("DELETE FROM shop;")
        self.con.commit()
        cmpt = 1
        for a in shop:
            last = datetime.datetime.now()
            last = last.strftime("%m/%d/%Y, %H:%M:%S")
            cursor.execute(f"INSERT INTO shop VALUES ('{a.id}','{last}',{cmpt});")
            cmpt += 1
            self.con.commit()

        cursor.close()
    def remarkeCustomDB(self):
        cursor = self.con.cursor()
        cursor.execute("CREATE TABLE color_icon (\n    species,\n    color,\n    file     UNIQUE\n);")
        cursor.execute("CREATE TABLE custom_icon (\n    owner_id    PRIMARY KEY\n                UNIQUE\n                NOT NULL,\n    espece,\n    couleur,\n    accessoire,\n    arme,\n    emoji       UNIQUE\n);")
        cursor.execute("CREATE TABLE head_has_png (\n    accessoire  PRIMARY KEY\n                UNIQUE\n                NOT NULL,\n    fichier     UNIQUE\n);")
        cursor.execute("CREATE TABLE weap_has_png (\n    weapon  PRIMARY KEY\n            UNIQUE,\n    file\n);")
        self.con.commit()
        cursor.close()
    def dropCustomDB(self):
        cursor = self.con.cursor()
        cursor.execute("DROP TABLE color_icon;")
        cursor.execute("DROP TABLE custom_icon;")
        cursor.execute("DROP TABLE head_has_png;")
        cursor.execute("DROP TABLE weap_has_png;")
        self.con.commit()
        cursor.close()
    def getShop(self):
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM shop;")
        result = cursor.fetchall()

        if len(result)>0:
            rep = {'ShopListe':[],'Date':None}
            click = result[0]["last"]
            rep["Date"] = datetime.datetime.strptime(click,"%m/%d/%Y, %H:%M:%S")
            for a in result:
                rep["ShopListe"] += [a["id"]]
            return rep
        else:
            return False

    def isFightingBool(self,team : int):
        cursor = self.con.cursor()
        cursor.execute("SELECT isFighting, fightingInfo, fightingChannel FROM teamVictory WHERE id = ?;",(team,))
        result = cursor.fetchall()
        if len(result)>0:
            result = result[0]
            cursor.close()
            return result["isFighting"], result["fightingInfo"], result["fightingChannel"]
        else:
            return 0,";",0

    def changeFighting(self,team : int,value:int, channel:int = 0, ennemis:List[Union[classes.char,classes.tmpAllie,classes.octarien]] = []):
        cursor = self.con.cursor()
        ennemiNames = ""
        for a in ennemis:
            ennemiNames += "{0};".format(a.name)

        if ennemiNames == "":
            ennemiNames = ";"
        
        if value == 0:
            channel = 0
        cursor.execute("UPDATE teamVictory SET isFighting = ?, fightingInfo = ?, fightingChannel = ? WHERE id = ?",(value,ennemiNames,channel,team,))
        self.con.commit()
        cursor.close()

    def getFightCooldown(self,team : int,quickFight = False):
        cursor = self.con.cursor()
        quickFight = int(quickFight)
        tabl = ["lastFight","lastQuickFight"]
        if quickFight:
            cursor.execute("SELECT lastQuickFight FROM teamVictory WHERE id = ?;",(team,))
        else:
            cursor.execute("SELECT lastFight FROM teamVictory WHERE id = ?;",(team,))
        result = cursor.fetchall()
        if len(result)>0:
            if quickFight:
                result = result[0]["lastQuickFight"]
            else:
                result = result[0]["lastFight"]
            try:
                result = datetime.datetime.strptime(result,"%m/%d/%Y, %H:%M:%S")
            except:
                return 0
            delta = result + datetime.timedelta(hours=1+2*quickFight)
            now = datetime.datetime.now()
            ballerine = delta - now
            return max(0,int(ballerine.total_seconds()))
        else:
            return 0

    def refreshFightCooldown(self,team : int,quickFight = False, fromTime : Union[None,datetime.datetime] = None):
        cursor = self.con.cursor()
        if fromTime == None:
            now = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        else:
            now = fromTime.strftime("%m/%d/%Y, %H:%M:%S")
        if quickFight:
            cursor.execute("UPDATE teamVictory SET lastQuickFight = ? WHERE id = ?;",(now,team,))
        else:
            cursor.execute("UPDATE teamVictory SET lastFight = ? WHERE id = ?;",(now,team,))
        self.con.commit()
        cursor.close()

    def resetAllFightingStatus(self):
        cursor = self.con.cursor()
        cursor.execute("UPDATE teamVictory SET isFighting = ?;",(False,))
        self.con.commit()
        cursor.close

    def dropCustom_iconTablDB(self):
        cursor = self.con.cursor()
        cursor.execute("DROP TABLE custom_icon;")
        self.con.commit()
        cursor.execute("""CREATE TABLE custom_icon(                owner_id    PRIMARY KEY                UNIQUE                NOT NULL,                espece      DEFAULT(1),                couleur     DEFAULT(0),                accessoire  DEFAULT('ha'),                arme        DEFAULT('af'),                emoji       DEFAULT('<:LenaWhat:760884455727955978>'),                iconForm    DEFAULT(0),                appaWeap    DEFAULT(NULL),                appaAcc     DEFAULT(NULL)            );""")
        self.con.commit()
        cursor.close()

    def removeUserIcon(self,user:classes.char):
        cursor = self.con.cursor()
        cursor.execute("DELETE FROM custom_icon WHERE owner_id = {0};".format(user.owner))
        self.con.commit()
        cursor.close()
