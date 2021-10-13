import os, sqlite3, classes, datetime

from discord_slash.utils.manage_components import create_button

class dbHandler():
    def __init__(self, database : str):
        self.con = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database}")
        self.con.row_factory = sqlite3.Row
        self.database = database

    def create_weapon(self, weapon : classes.weapon):
        if type(weapon) == classes.weapon:
            cursor = self.con.cursor()
            params = (weapon.name,weapon.id,weapon.range,weapon.effectiveRange,weapon.power,weapon.sussess,weapon.price,weapon.strength,weapon.endurance,weapon.charisma,weapon.agility,weapon.precision,weapon.intelligence,weapon.resistance,weapon.percing,weapon.critical,weapon.repetition,weapon.emoji,weapon.area,weapon.effect,weapon.effectOnUse,weapon.target,weapon.type,weapon.orientation)
            query = "INSERT INTO weapon VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            cursor.execute(query,params)
            cursor.close()
            self.con.commit()
        else:
            print("Le paramètre donné n'est pas une arme")

    def edit_weapon(self,weapon : classes.weapon):
        if type(weapon) == classes.weapon:
            cursor = self.con.cursor()
            params = (weapon.name,weapon.range,weapon.effectiveRange,weapon.power,weapon.sussess,weapon.price,weapon.strength,weapon.endurance,weapon.charisma,weapon.agility,weapon.precision,weapon.intelligence,weapon.resistance,weapon.percing,weapon.critical,weapon.repetition,weapon.emoji,weapon.area,weapon.effect,weapon.effectOnUse,weapon.target,weapon.type,weapon.orientation,weapon.id)
            query = f"UPDATE weapon SET name = ?, range = ?,effectiveRange = ?, power = ?, sussess = ?,price = ?, strength = ?, endurance = ?, charisma = ?, agility = ?, precision = ?, intelligence = ?, resistance = ?, percing = ?, critical = ?, repetition = ?, emoji = ?, area = ?, effect = ?, effectOnUse = ?, target = ?, type = ?, orientation = ? WHERE id = ?;"
            cursor.execute(query,params)
            cursor.close()
            self.con.commit()
        else:
            print("Le paramètre donné n'est pas une arme")
       
    def create_skill(self, skill : classes.skill):
        if type(skill) == classes.skill:
            cursor = self.con.cursor()
            effectStr = ""
            for a in skill.effect:
                if a != None:
                    if type(a)!=str:
                        effectStr += a.id
                    else:
                        effectStr +=a
                    effectStr += " - "
            if effectStr =="":
                 effectStr = None
            params = (skill.name,skill.id,skill.type,skill.price,skill.power,skill.range,skill.conditionType,skill.ultimate,skill.secondary,skill.emoji,effectStr,skill.cooldown,skill.area,skill.sussess)
            query = "INSERT INTO skill VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            cursor.execute(query,params)
            cursor.close()
            self.con.commit()
        else:
            print("Le paramètre donné n'est pas une compétence")

    def edit_skill(self,skill : classes.skill):
        if type(skill) == classes.skill:
            cursor = self.con.cursor()
            effectStr = ""
            for a in skill.effect:
                if a != None:
                    if type(a)!=str:
                        effectStr += a.id
                    else:
                        effectStr +=a
                    effectStr += " - "
            if effectStr =="":
                 effectStr = None
            params = (skill.name,skill.type,skill.price,skill.power,skill.range,skill.conditionType,skill.ultimate,skill.secondary,skill.emoji,effectStr,skill.cooldown,skill.area,skill.sussess,skill.id)
            query = "UPDATE skill SET name = ?,type = ?, price = ?, power = ?, range = ?, conditionType = ?, ultimate = ?, secondary = ?, emoji = ?, effect = ?, cooldown = ?, area = ?, sussess = ? WHERE id = ?;"
            cursor.execute(query,params)
            cursor.close()
            self.con.commit()
        else:
            print("Le paramètre donné n'est pas une compétence")

    def create_gear(self, gear : classes.stuff):
        if type(gear) == classes.stuff:
            cursor = self.con.cursor()
            params = (gear.name,gear.id,gear.type,gear.strength,gear.endurance,gear.charisma,gear.agility,gear.precision,gear.intelligence,gear.resistance,gear.percing,gear.critical,gear.emoji,gear.effect,gear.orientation)
            query = "INSERT INTO gear VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            cursor.execute(query,params)
            cursor.close()
            self.con.commit()
        else:
            print("Le paramètre donné n'est pas un équipement")

    def edit_gear(self, gear : classes.stuff):
        if type(gear) == classes.stuff:
            cursor = self.con.cursor()
            params = (gear.name,gear.type,gear.strength,gear.endurance,gear.charisma,gear.agility,gear.precision,gear.intelligence,gear.resistance,gear.percing,gear.critical,gear.emoji,gear.effect,gear.orientation,gear.id)
            query = "UPDATE gear SET name = ?, type = ?, strength = ?, endurance = ?, charisma = ?, agility = ?, precision = ?, intelligence = ?, resistance = ?, percing = ?, critical = ?, emoji = ?, effect = ?,orientation = ? WHERE id = ?;"
            cursor.execute(query,params)
            cursor.close()
            self.con.commit()
        else:
            print("Le paramètre donné n'est pas un équipement")

    def getAllHeadGear(self):
        cursor = self.con.cursor()
        query = "SELECT emoji FROM gear WHERE type = 0;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        for a in range(0,len(result)):
            result[a] = result[a]["emoji"]
        return result

    def getAllWeap(self):
        cursor = self.con.cursor()
        query = "SELECT emoji FROM weapon"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        for a in range(0,len(result)):
            result[a] = result[a]["emoji"]
        return result

    def addHeadGearImageFiles(self,headgearId,headgearFile):
        cursor = self.con.cursor()
        params = (headgearId,headgearFile)
        query = "INSERT INTO head_has_png VALUES (?,?);"
        try:
            cursor.execute(query,params)
        except:
            curso.execute("UPDATE head_has_png SET fichier = ? WHERE accessoire = ?",(headgearFile,headgearId))
        cursor.close()
        self.con.commit()

    def addWeapImageFiles(self,weapId,weapFile):
        cursor = self.con.cursor()
        params = (weapId,weapFile)
        query = "INSERT INTO weap_has_png VALUES (?,?);"
        try:
            cursor.execute(query,params)
        except:
            curso.execute("UPDATE weap_has_png SET file = ? WHERE weapon = ?",(weapFile,weapId))
        cursor.close()
        self.con.commit()

    def addIconFiles(self,species,color,file):
        cursor = self.con.cursor()
        params = (species,color,file)
        query = "INSERT INTO color_icon VALUES (?,?,?);"
        cursor.execute(query,params)
        cursor.close()
        self.con.commit()

    def getIdFromEmoji(self,emoji,where):
        cursor = self.con.cursor()
        query = f"SELECT id FROM {where} WHERE emoji = ?;"
        cursor.execute(query,(emoji,))
        result = cursor.fetchall()
        cursor.close()
        return result[0]["id"]

    def haveCustomIcon(self,user):
        cursor = self.con.cursor()
        query = f"SELECT owner_id FROM custom_icon WHERE owner_id = ?;"
        cursor.execute(query,(user.owner,))
        result = cursor.fetchall()
        cursor.close()
        return len(result) > 0

    def editCustomIcon(self,user,emoji):
        cursor = self.con.cursor()
        if self.haveCustomIcon(user):
            params = (user.species, user.color, user.stuff[0].id, user.weapon.id, str(emoji), user.owner)
            query = "UPDATE custom_icon SET espece = ?, couleur = ?, accessoire = ?, arme = ?, emoji = ? WHERE owner_id = ?;"
            cursor.execute(query,params)
            cursor.close()
            self.con.commit()
        else:
            params = (user.owner,user.species, user.color, user.stuff[0].id, user.weapon.id, str(emoji))
            query = "INSERT INTO custom_icon VALUES (?,?,?,?,?,?)"
            cursor.execute(query,params)
            cursor.close()
            self.con.commit()

    def getColorFile(self,user):
        cursor = self.con.cursor()
        query = f"SELECT file FROM color_icon WHERE species = {user.species} AND color = {classes.getColorId(user)};"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result[0]["file"]

    def getWeaponFile(self,user):
        cursor = self.con.cursor()
        query = f"SELECT file FROM weap_has_png WHERE weapon = '{user.weapon.id}';"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result[0]["file"]

    def getAccFile(self,user):
        cursor = self.con.cursor()
        query = f"SELECT fichier FROM head_has_png WHERE accessoire = '{user.stuff[0].id}';"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        if len(result) == 0:
            return "defHead.png"
        return result[0]["fichier"]

    def getCustomIcon(self,user):
        cursor = self.con.cursor()
        query = f"SELECT emoji FROM custom_icon WHERE owner_id = ?;"
        cursor.execute(query,(user.owner,))
        result = cursor.fetchall()
        cursor.close()
        return result[0]["emoji"]

    def isDifferent(self,user):
        query = f"SELECT * FROM custom_icon WHERE owner_id = ?;"
        cursor = self.con.cursor()
        cursor.execute(query,(user.owner,))
        result = cursor.fetchall()
        cursor.close()
        if len(result)>0:
            return not(result[0]["espece"] == user.species and result[0]["accessoire"]==user.stuff[0].id and result[0]["arme"]==user.weapon.id and result[0]["couleur"]==user.color)
        else:
            return True

    def getVictoryStreak(self,user):
        team = user.team
        if user.team == 0:
            team = user.owner
        cursor = self.con.cursor()
        query = f"SELECT * FROM teamVictory WHERE id = ?;"
        cursor.execute(query,(team,))
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
            query = "INSERT INTO teamVictory VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
            params = (team,True,False,True,False,True,False,True,False,True,False,datetime.datetime.min.strftime("%m/%d/%Y, %H:%M:%S"),datetime.datetime.min.strftime("%m/%d/%Y, %H:%M:%S"),False,)
            cursor.execute(query,params)
            cursor.close()
            self.con.commit()
            return 5

        cursor.close()

    def addResultToStreak(self,user,resultat : bool):
        team = user.team
        if team == 0:
            team = user.owner
        cursor = self.con.cursor()
        query = f"SELECT * FROM teamVictory WHERE id = ?;"
        cursor.execute(query,(team,))
        result = cursor.fetchall()[0]

        params = (resultat, result["1"], result["2"], result["3"], result["4"], result["5"], result["6"], result["7"], result["8"], result["9"], team,)
        query = "UPDATE teamVictory SET '1'=?, '2'=?, '3'=?, '4'=?, '5'=?, '6'=?, '7'=?, '8'=?, '9'=?, '10'=? WHERE id = ?;"
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
        cursor.execute("SELECT isFighting FROM teamVictory where id = ?;",(team,))
        result = cursor.fetchall()
        if len(result)>0:
            result = result[0]["isFighting"]
            cursor.close()
            if result == None:
                result = False
            return result
        else:
            return False
    def changeFighting(self,team : int,value=bool):
        cursor = self.con.cursor()
        cursor.execute("UPDATE teamVictory SET isFighting = ? WHERE id = ?",(value,team,))
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

    def refreshFightCooldown(self,team : int,quickFight = False):
        cursor = self.con.cursor()
        now = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
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
