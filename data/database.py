import sqlite3, classes, adv, interactions
from typing import List, Union
from datetime import datetime, timedelta
from constantes import *
from traceback import print_exc

class dbHandler():
    def __init__(self, database : str):
        self.con = sqlite3.connect(f"./data/database/{database}",timeout=10)
        self.con.row_factory = sqlite3.Row
        self.database = database

    def addTeam(self,team):
        try:
            cursor, defIso = self.con.cursor(), defaultDate.isoformat()
            cursor.execute("INSERT INTO teamVictory VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,';',0);",(team,True,False,True,False,True,False,True,False,True,False,defIso,defIso,False,0,0,))
            cursor.close()
            self.con.commit()
        except: print_exc()

    def getAllTeamIds(self):
        try:
            cursor = self.con.cursor()
            cursor.execute("SELECT id FROM teamVictory")
            result = cursor.fetchall()
            cursor.close()

            toReturn = []
            for tmp in result: toReturn.append(int(tmp["id"]))
            return toReturn
        except: print_exc(); raise
        
    def delTeam(self,team):
        try:
            cursor = self.con.cursor()
            cursor.execute("DELETE FROM teamVictory WHERE id = {0};".format(team))
            self.con.commit()
            cursor.close()
            return True
        except: print_exc(); return False

    def addIconFiles(self,species:int,color:int,file):
        cursor = self.con.cursor()
        params = (species,color,file)
        query = "INSERT INTO color_icon VALUES (?,?,?);"
        try: cursor.execute(query,params)
        except: pass
        cursor.close()
        self.con.commit()

    def getIdFromEmoji(self,emoji,where):
        for obj in adv.stuffs + adv.weapons:
            if obj.emoji == emoji: return obj.id

    def haveCustomIcon(self,user):
        cursor = self.con.cursor()
        cursor.execute("SELECT owner_id FROM custom_icon WHERE owner_id = ?;",(user.owner,))
        result = cursor.fetchall()
        cursor.close()
        return len(result) > 0

    def editCustomIcon(self,user:classes.char,emoji:interactions.CustomEmoji):
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
            if user.stuff[0].__class__ != str:
                user.stuff[0] = user.stuff[0].id
            if user.weapon.__class__ != str:
                user.weapon = user.weapon.id
            
            params = (user.species, user.color, user.stuff[0], user.weapon, str(emoji), blbl2, blbl1, user.iconForm, user.owner,)
            query = "UPDATE custom_icon SET espece = ?, couleur = ?, accessoire = ?, arme = ?, emoji = ?, appaWeap = ?, appaAcc = ?, iconForm = ? WHERE owner_id = ?;"
            cursor.execute(query,params)
            cursor.close()
            self.con.commit()
        else:
            params = (user.owner,user.species, user.color, user.stuff[0].id, user.weapon.id, str(emoji), blbl2, blbl1, user.iconForm,)
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
            formVerif = [result["iconForm"],0][result["iconForm"] == None]
            try:
                return not(result["espece"] == user.species and ((user.apparaAcc==None and result["accessoire"]==user.stuff[0].id) or (user.apparaAcc!=None and user.apparaAcc.id == result["appaAcc"])) and ((user.apparaWeap == None and result["arme"]==user.weapon.id) or (user.apparaWeap!=None and user.apparaWeap.id == result["appaWeap"])) and result["couleur"]==user.color and user.iconForm == formVerif)
            except:
                return False
        else:
            return True

    def getVictoryStreak(self, user, returnStr=False):
        team = user.team
        if user.team == 0: team = user.owner
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM teamVictory WHERE id = ?;",(team,))
        result = cursor.fetchall()
        
        cursor.close()

        if len(result) > 0:
            result, winNb, winStr = result[0], 0, ""
            tabl = [result["1"],result["2"],result["3"],result["4"],result["5"],result["6"],result["7"],result["8"],result["9"],result["10"]]
            for indx, tmpResult in enumerate(tabl):
                if tmpResult: winNb += 1; winStr += "🟢"
                else: winStr += "🔴"

                if indx != 9: winStr += ","
            
            if not(returnStr): return winNb
            else:
                winStr += "\n__Taux de victoire des derniers combats :__ {0}%".format(int(winNb/10*100))
                try: winStr += "\n__Taux de victoire total :__ {0}%".format(round(result["totalWin"]/result["totalFight"]*100,1))
                except: pass
                return winStr

        else:
            self.addTeam(team)
            if not(returnStr): return 5
            else: return "🟢,🔴,🟢,🔴,🟢,🔴,🟢,🔴,🟢,🔴"

    def addResultToStreak(self,user,resultat : bool):
        team = user.team
        if team == 0: team = user.owner
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM teamVictory WHERE id = ?;",(team,))
        result = cursor.fetchall()
        if len(result) > 0: result = result[0]
        else:
            self.addTeam(team)
            cursor.execute("SELECT * FROM teamVictory WHERE id = ?;",(team,))
            result = cursor.fetchall()[0]

        nbWin = result["totalWin"]
        nbWin += int(resultat)

        cursor.execute("UPDATE teamVictory SET '1'=?, '2'=?, '3'=?, '4'=?, '5'=?, '6'=?, '7'=?, '8'=?, '9'=?, '10'=?, totalWin = ?, totalFight=? WHERE id = ?;",(resultat, result["1"], result["2"], result["3"], result["4"], result["5"], result["6"], result["7"], result["8"], result["9"], nbWin, result["totalFight"]+1, team,))
        self.con.commit()
        cursor.close()

    def addShop(self,shop : list[Union[classes.weapon,classes.stuff,classes.skill,classes.other]]):
        try:
            cursor = self.con.cursor()
            cursor.execute("DELETE FROM shop;")
            self.con.commit()
            cmpt = 1
            for a in shop:
                last = datetime.now(parisTimeZone)
                last = last.strftime("%m/%d/%Y, %H:%M:%S")
                cursor.execute(f"INSERT INTO shop VALUES ('{a.id}','{last}',{cmpt});")
                cmpt += 1
                self.con.commit()

            cursor.close()
            return True
        except:
            return False
    
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
            rep["Date"] = datetime.strptime(click,"%m/%d/%Y, %H:%M:%S")
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
        value = int(value)
        channel = int(value)
        for a in ennemis: ennemiNames += "{0};".format(a.name)

        if ennemiNames == "": ennemiNames = ";"
        
        if value == 0: channel = 0
        cursor.execute("UPDATE teamVictory SET isFighting = ?, fightingInfo = ?, fightingChannel = ? WHERE id = ?",(value,ennemiNames,channel,team,))
        self.con.commit()
        cursor.close()

    def getFightCooldown(self,team : int ,quickFight = False ,timestamp=False ,returnDate=False):
        cursor = self.con.cursor()
        quickFight = int(quickFight)
        tabl = ["lastFight","lastQuickFight"]
        if quickFight: cursor.execute("SELECT lastQuickFight FROM teamVictory WHERE id = ?;",(team,))
        else: cursor.execute("SELECT lastFight FROM teamVictory WHERE id = ?;",(team,))
        result = cursor.fetchall()
        cursor.close()
        if len(result)>0:
            if quickFight: result = result[0]["lastQuickFight"]
            else: result = result[0]["lastFight"]
            try:
                result = datetime.fromisoformat(result)
                if result.tzinfo == None: result = result.replace(tzinfo=parisTimeZone)
            except ValueError: result = defaultDate
            except: print_exc(); print("Error endled"); result = defaultDate

            if returnDate: return result

            delta = result + timedelta(hours=1+(2*int(quickFight)))
            if not(timestamp):
                try: now = datetime.now(parisTimeZone); ballerine = delta - now
                except: print_exc(); print("Error endled"); return 999
                return max(0,int(ballerine.total_seconds()))
            else:
                timy = delta
                if delta.year == delta.month == delta.day == 1: delta = defaultDate; delta = delta.isoformat()
                else: delta = timy.isoformat()
                return ["✅ ","❌ "][(timy-datetime.now(parisTimeZone)).total_seconds()>0] + Timestamp.fromisoformat(delta).format(interactions.models.discord.timestamp.TimestampStyles.RelativeTime)
        else:
            self.addTeam(team)
            if returnDate: return defaultDate
            else: return (defaultDate-datetime.now(parisTimeZone)).total_seconds()

    def refreshFightCooldown(self,team : int,quickFight = False, fromTime : Union[None,datetime,int] = None):
        cursor = self.con.cursor()
        if fromTime == None: now = datetime.now(parisTimeZone).isoformat()
        elif fromTime == 0: now = defaultDate.isoformat()
        else: now = fromTime.isoformat()
        if quickFight: cursor.execute("UPDATE teamVictory SET lastQuickFight = ? WHERE id = ?;",(now,team,))
        else: cursor.execute("UPDATE teamVictory SET lastFight = ? WHERE id = ?;",(now,team,))
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

    def searchCustomIcon(self,emoji:Union[str,interactions.CustomEmoji]):
        if type(emoji) != str:
            emoji = '<:{0}:{1}>'.format(emoji.name,emoji.id)
        cursor = self.con.cursor()
        cursor.execute("SELECT owner_id FROM custom_icon WHERE emoji = '{0}';".format(emoji))
        cursorReturn, toReturn = cursor.fetchall(), []
        cursor.close()

        for respond in cursorReturn:
            toReturn.append(respond["owner_id"])
        return toReturn