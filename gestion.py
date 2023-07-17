import os,random,sqlite3
from traceback import print_exc
from typing import Union
import interactions
from classes import *
from adv import findWeapon,findOther,findSkill,findStuff
"""
Main functions module
"""

userSettingsInterCatNames = ["start","ultimate","limiteBreak","onKill","onDeath","onResurect","blueWinAlive","blueWinDead","blueLoose","redWinAlive","redWinDead","redLoose","blockBigAttack","reactBigRaiseAllie","reactBigRaiseEnnemy","bigRaise","reactEnnemyKilled","reactAllyKilled"]

majUserSettings1 = """
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
        lastDay             STRING  DEFAULT ('0000') 
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
                                affAcc
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
                                    affAcc
                            FROM sqlitestudio_temp_table;

    DROP TABLE sqlitestudio_temp_table;

    PRAGMA foreign_keys = 1;
"""

class userTeamDbEndler:
    """A database who store some user's info like their team"""
    def __init__(self):
        self.con = sqlite3.connect(f"./data/database/aliceStats.db",timeout=10,check_same_thread=False)
        self.con.row_factory = sqlite3.Row
        self.database = "aliceStats.db"

        cursor = self.con.cursor()
        try:
            cursor.execute("SELECT teamMinLvl FROM userTeams;")
        except:
            cursor.execute("ALTER TABLE userTeams ADD teamMinLvl INTEGER DEFAULT (0)")
            print("teamMinLvl added to userTeams")
            self.con.commit()
        cursor.close()

    def updateTeam(self,team:int,members:Union[List[int],List[char]]=None):
        cursory, listToAdd, listToAdd2 = self.con.cursor(), "" , ""
        
        # Allready Exist ?
        cursory.execute("SELECT teamMember0 FROM userTeams WHERE teamId = {0};".format(team))
        result = cursory.fetchone()
        if members == None:
            cursory.execute("DELETE FROM userTeams WHERE teamId = {0};".format(team))
            self.con.commit()
            cursory.close()
            print("The team number {0} have been removed from the database".format(team))
            return 0
        if result == None:
            for a in range(len(members)):
                if type(members[a]) in [int,str]:
                    listToAdd += "{0}".format(members[a])
                elif type(members[a]) == char:
                    listToAdd += "{0}".format(members[a].owner)
                else:
                    raise Exception("Unknow type ({0})".format(type(members[a])))

                listToAdd2 += "teamMember{0}".format(a)
                if a < len(members)-1:
                    listToAdd += ","
                    listToAdd2 += ","

            cursory.execute('INSERT INTO userTeams (teamId,{2}) VALUES ({0},{1});'.format(team,listToAdd,listToAdd2))
            self.con.commit()
            cursory.close()
            print("The team number {0} have been added into the database".format(team))
        else:
            while len(members) < 8:
                members.append(None)
            cursory.execute('UPDATE userTeams SET teamMember0 = ?, teamMember1 = ?, teamMember2 = ?, teamMember3 = ?, teamMember4 = ?, teamMember5 = ?, teamMember6 = ?, teamMember7 = ? WHERE teamId = ?;',(members[0],members[1],members[2],members[3],members[4],members[5],members[6],members[7],team))
            self.con.commit()
            cursory.close()

    def getTeamMinLvl(self,team:int):
        cursory = self.con.cursor()
        cursory.execute('SELECT teamMinLvl FROM userTeams WHERE teamId = {0};'.format(team))
        rep = cursory.fetchone()
        cursory.close()
        return rep["teamMinLvl"]

    def updateTeamMinLvl(self,listUser:List[char]):
        moyLvl, cmpt = 0, 0
        for ent in listUser:
            moyLvl, cmpt = moyLvl+ent.level, cmpt+1
        moyLvl = moyLvl / cmpt
        cursory = self.con.cursor()
        cursory.execute("UPDATE userTeams SET teamMinLvl = ? WHERE teamId = ?;",(moyLvl,int(listUser[0].team)))
        self.con.commit()
        cursory.close()

    def getTeamMember(self,team:int) -> List[int]:
        cursory = self.con.cursor()
        cursory.execute('SELECT teamMember0, teamMember1, teamMember2, teamMember3, teamMember4, teamMember5, teamMember6, teamMember7 FROM userTeams WHERE teamId = {0};'.format(team))
        result = cursory.fetchone()
        cursory.close()

        if result == None:
            return None

        toReturn = []
        for a in result:
            if a not in [0,None]:
                toReturn.append(a)

        return toReturn

    def getAllTeamIds(self,withMinLvl=False) -> List[int]:
        cursory, toReturn = self.con.cursor(), []
        if withMinLvl:
            cursory.execute("SELECT teamId, teamMinLvl FROM userTeams;")
            result = cursory.fetchall()
            cursory.close()
            for a in result:
                toReturn.append([a["teamId"],a["teamMinLvl"]])
        else:
            cursory.execute("SELECT teamId FROM userTeams;")
            result = cursory.fetchall()
            cursory.close()
            for a in result:
                toReturn.append([a["teamId"]])
        return toReturn

    def doesTeamExist(self,team:int):
        cursory = self.con.cursor()
        cursory.execute("SELECT teamMember0 FROM userTeams WHERE teamId = {0};".format(team))
        result = cursory.fetchone()
        cursory.close()
        return not(result == None)

class userSettingsDbEndler:
    def __init__(self):
        self.con = sqlite3.connect(f"./data/database/userSettings.db",timeout=10,check_same_thread=False)
        self.con.row_factory = sqlite3.Row
        self.database = "userSettings.db"

        cursor = self.con.cursor()

        try:
            cursor.execute("SELECT affWeap FROM userSettings;")
        except:
            temp = ""
            for a in majUserSettings1:
                if a != ";":
                    temp+=a
                else:
                    cursor.execute(temp)
                    temp = ""

            cursor.execute(temp)
            cursor.execute("UPDATE userSettings SET hand = 1;")
            self.con.commit()
            print("maj1 done")

        cursor.close()
    
    def addUserToDb(self, user:char):
        toAddCat, toAddValue, blabla = [], [], user.says.tabl()
        for a in range(len(blabla)):
            if blabla[a] != None:
                toAddCat.append(userSettingsInterCatNames[a])
                toAddValue.append(blabla[a])
    
        toAddStr, tempTabl, = ["",""], [toAddCat,toAddValue]
        for a in [0,1]:
            for cmpt in range(len(tempTabl[a])):
                if a == 1:
                    toAdd = "'"
                    for b in tempTabl[a][cmpt]:
                        if b in ["'"]:
                            toAdd += "''"
                        else:
                            toAdd += b
                    toAdd += "'"
                else:
                    toAdd = tempTabl[a][cmpt]

                toAddStr[a]+=toAdd
                if cmpt < len(tempTabl[a])-1:
                    toAddStr[a]+=","

        cursory = self.con.cursor()
        cursory.execute("INSERT INTO userSettings (userId{3}{0}) VALUES ({1}{3}{2});".format(toAddStr[0],user.owner,toAddStr[1],["",","][toAddStr[0]!=""]))
        cursory.close()
        self.con.commit()
        print("{0} a été rajouté dans la base de donnée".format(user.name))

    def updateUserSettings(self,user:char):
        cursory = self.con.cursor()
        cursory.execute("SELECT * FROM userSettings WHERE userId = {0};".format(user.owner))
        result = cursory.fetchone()

        if result == None:
            cursory.close()
            self.addUserToDb(self)
            cursory = self.con.cursor()
        else:
            toAddCat, toAddValue, blabla = [], [], user.says.tabl()
            for a in range(len(blabla)):
                if blabla[a] != None:
                    toAddCat.append(userSettingsInterCatNames[a])
                    toAddValue.append(blabla[a])
            toAddStr, tempTabl = "", [toAddCat,toAddValue]
            for cmpt in range(len(tempTabl[0])):
                if result[tempTabl[0][cmpt]] != blabla[cmpt]:
                    toAdd = ""
                    for b in tempTabl[1][cmpt]:
                        if b == "'":
                            toAdd += "''"
                        else:
                            toAdd += b
                    toAdd += ""

                    tablSepcCar = ["-","*","_"]
                    for character in tablSepcCar:
                        toAdd = toAdd.replace(character,"\{0}".format(character))

                    toAddStr+= "{0}='{1}'".format(tempTabl[0][cmpt],toAdd)
                    if cmpt < len(tempTabl[0])-1:
                        toAddStr+=","

            if toAddStr != "":
                if toAddStr.endswith(","):
                    toAddStr= toAddStr[:-1]
                try:
                    cursory.execute("UPDATE userSettings SET {0} WHERE userId = {1};".format(toAddStr,user.owner))
                except:
                    print("UPDATE userSettings SET {0} WHERE userId = {1};".format(toAddStr,user.owner))
            
            textUpdateSettings = ""
            for setName, setValue in user.charSettings.items():
                if result[setName] != setValue:
                    textUpdateSettings += "{0} {1} = {2}".format(["",","][textUpdateSettings!=""],setName,setValue)
            
            if textUpdateSettings != "":
                cursory.execute("UPDATE userSettings SET {0} WHERE userId = ?;".format(textUpdateSettings),(user.owner,))

            iconSetValues = [user.handed,user.showElement,user.showAcc,user.showWeapon]
            textIconSet = ""
            for cmpt in range(len(iconSetCatNames)):
                if result[iconSetCatNames[cmpt]] != iconSetValues[cmpt]:
                    textIconSet += "{0} {1} = {2}".format(["",","][textIconSet!=""],iconSetCatNames[cmpt],iconSetValues[cmpt])            
            if textIconSet != "":
                cursory.execute("UPDATE userSettings SET ? WHERE userId = ?;",(user.owner,textIconSet,))

        cursory.close()
        self.con.commit()

    def getUserSettings(self,user: char) -> char:
        cursory = self.con.cursor()
        cursory.execute("SELECT * FROM userSettings WHERE userId = {0};".format(user.owner))
        result = cursory.fetchone()
        cursory.close()

        if result == None:
            self.addUserToDb(self)
        else:
            tablTemp = []
            for cmpt in range(len(tablSaysDictCat)):
                tablTemp.append(result[tablSaysDictCat[cmpt]])

            tempSays = says()
            user.says = tempSays.fromTabl(tablTemp)
            user.handed,user.showElement,user.showAcc,user.showWeapon = result[iconSetCatNames[0]], result[iconSetCatNames[1]], result[iconSetCatNames[2]], result[iconSetCatNames[3]]

            for charSetName in emptyCharDict:
                user.charSettings[charSetName] = result[charSetName]

        return user

userTeamDb = userTeamDbEndler()
userSettingsDb = userSettingsDbEndler()

def lecFile(path : str):
    "Renvoie sous forme de liste toutes les lignes d'un fichier en retirant le retour chariot\n\nParamètre : fichier (str)\n\nRetourne :\nlist"
    fich = open(path, "r")
    liste = fich.readlines()
    comp = 1
    while comp <= len(liste)-1:
        liste[comp]=liste[comp][0:-1]
        comp+=1

    fich.close()
    return liste

def empty(liste : list):
    "Teste si une liste est vide\n\nParamètre : liste (list)\n\nRetourne : bool"
    if len(liste) == 0:
        return True
    else:
        return False

def listToStr(liste : list):
    "Renvoie tout le contenue d'un list en un str, séparées par des espaces\n\nParamètre : liste (list)\n\nRetourne : str"
    temp = ""
    for a in liste:
        temp+=a+" "
    return temp

def cutStrToList(string : str, caractere : str):
    "Coupe le string à chaque itération de caractere, puis le renvoie sous forme de liste\n\nParamètres : string (str), caractere (str)\n\nRetourne : list"
    rep,temp = [],""
    for a in string:
        if a == caractere:
            rep+=[temp]
            temp = ""
        else:
            temp+=a
    rep+=[temp]
    return rep

def existDir(path : str):
    "Vérifie si le dossier au chemin String existe. Si oui, return True. Si non, créait le dossier et return False"
    if not os.path.exists(path):
        print(f"Création du dossier {path}")
        os.mkdir(path)
        return False
    else:
        return True

def rewriteFile(path : str, content : str):
    fich = open(path, "w")
    fich.write(content)
    fich.close()

def existFile(path : str):
    "Vérifie si le fichier au chemin String existe. Si oui, return True. Si non, créait le fichier et return False"
    if not os.path.exists(path):
        temp =open(path,"w")
        temp.write("0")
        temp.close()
        return False
    else: 
        return True

def commandArgs(ctx : interactions.Message):
    """A function for auto cut the ctx message content into multiples arguments.\n
    Mostly useless with slash commands now"""
    rep,temp = [],""
    for a in ctx.content:
        if a == " ":
            rep = rep + [temp]
            temp = ""
        else:
            temp = temp + a
    rep = rep + [temp] + [None]
    return rep

async def loadingEmbed(ctx : interactions.Message):
    """A function for send loading embed from a message command.\n
    Mostly useless with slash commands now"""
    return await ctx.channel.send(embeds = interactions.Embed(title = commandArgs(ctx)[0], description = emLoading))

def readSaveFiles(path : str):
    """Return a list with the saves files content, ready to be used in a Load function"""
    file = open(path,"r")
    fileContent = file.readlines()
    file.close()
    rep,temp,temp2 = [],"",[]
    for a in fileContent:
        for b in a:
            if b == ";":
                temp2 = temp2 + [temp]
                temp = ""
            else:
                temp = temp + b
        rep = rep + [temp2]
        temp2 = []
    rep = rep + [temp2]
    return rep

def saveSaveFiles(path : str, settings : list):
    """Save the settings into the file in path\n
    Return True if sussed, False if it failed"""
    try:
        saved = ""
        for a in settings:
            for b in a:
                saved += str(b)+";"
            if a != []:
                saved += "\n"
        
        rewriteFile(path,saved)
        return True
    except:
        return False

def choice(liste : list):
    """Only used in settings command"""
    msg, cmpt = "\n",0
    for a in liste:
        msg += f"\n[{cmpt}] : {a}"
        cmpt += 1

    return msg

def errorEmbed(errorType : str, msgError : str):
    """Return a error embed ready to be send"""
    rep = interactions.Embed(title = errorType, description = msgError)
    rep.set_footer(text = "Fin de la commande")
    return rep

def randRep(liste : list):
    """Hum... Where I use that...
    choose command"""
    return liste[random.randint(0,len(liste)-1)]

def saveCharFile(path : str = None, user : char = None):
    if user.owner.__class__ != int:
        user.owner = int(user.owner)
    try:
        if user == None:
            raise Exception("Attribut Error : No user gave")
        if path == None:
            path = './userProfile/{0}.prof'.format(user.owner)
        #try:
        saved = ""
        for a in [user.owner,user.name,user.level,user.exp,user.currencies,user.species,user.color,user.team,int(user.customColor),user.colorHex,user.stars,user.iconForm,user.secElement]:
            saved += str(a)+";"
        saved += "\n"
        for a in [user.strength,user.endurance,user.charisma,user.agility,user.precision,user.intelligence,user.magie,user.aspiration,user.gender]:
            saved += str(a)+";"
        saved += "\n"
        for a in [user.resistance,user.percing,user.critical,user.points]:
            saved += str(a)+";"
        for a in user.bonusPoints+user.majorPoints+[user.majorPointsCount]:
            saved += str(a)+";"
        saved += "\n"
        saved += user.weapon.id +";\n"
        for a in user.weaponInventory:
            saved += a.id+";"
        saved += "\n"
        for a in user.skills:
            try:
                saved += a.id+";"
            except:
                saved += "0;"
        saved += "\n"
        for a in user.skillInventory:
            saved += a.id+";"
        saved += "\n"
        for a in user.stuff:
            saved += a.id+";"
        for a in [user.apparaWeap,user.apparaAcc]:
            if a != None:
                saved += a.id+";"
            else:
                saved += "0;"
        saved += "\n"
        for a in user.stuffInventory:
            saved += a.id+";"
        saved += "\n"
        for a in user.otherInventory:
            saved += a.id+";"
        saved += "\n"
        for a in user.procuration:
            if int(a) != user.owner:
                saved += str(a)+";"
        saved += "\n"

        saved += str(user.element) +";"+str(int(user.autoPoint))+";"+str(int(user.autoStuff))+";\n"

        for a in user.haveProcurOn:
            saved += str(a) + ";"
        saved += "\n"

        for a in user.limitBreaks:
            saved += str(a) + ";"
        saved += "\n"

        userSettingsDb.updateUserSettings(user)
        rewriteFile(path,saved)
        return True
    except:
        raise

def loadCharFile(path : str = None, user:char = None) -> char:
    """
        Return a ``char`` object loaded from the file at ``path``
    """
    try:
        if path != None:
            file = readSaveFiles(path)
        elif user != None:
            file = readSaveFiles("./userProfile/{0}.prof".format(user.owner))
        else:
            raise Exception("Argument error : No path or user given")
    except:
        print_exc()
        return None
    rep = char(owner = int(file[0][0]))                     # Owner
    rep.name = file[0][1]                                   # Name
    rep.level = int(file[0][2])                             # Level
    rep.exp = int(file[0][3])                               # Exp
    rep.currencies = int(file[0][4])                        # Currencies
    rep.species = int(file[0][5])                           # Species
    rep.color = int(file[0][6])                             # Color
    rep.team = int(file[0][7])                              # Team id
    rep.customColor = bool(int(file[0][8]))                 # Custom color
    rep.gender = int(file[1][8])
    rep.colorHex = file[0][9]
    rep.stars = int(file[0][10])
    rep.iconForm = int(file[0][11])
    rep.secElement = int(file[0][12])

    # Stats
    rep.strength,rep.endurance,rep.charisma,rep.agility,rep.precision,rep.intelligence,rep.magie,rep.aspiration = int(file[1][0]),int(file[1][1]),int(file[1][2]),int(file[1][3]),int(file[1][4]),int(file[1][5]),int(file[1][6]),int(file[1][7])
    rep.resistance,rep.percing,rep.critical,rep.points = int(file[2][0]),int(file[2][1]),int(file[2][2]),int(file[2][3])

    rep.majorPointsCount = int(file[2][-1])

    try:                                                    # Bonus points
        temp = []
        for a in file[2][4:11]:
            temp += [int(a)]
        rep.bonusPoints = temp
    except:
        rep.bonusPoints = [0,0,0,0,0,0,0]

    try:
        temp = []
        for a in file[2][11:-1]:
            temp += [int(a)]
        while len(temp) < 15:
            temp.append(0)
        rep.majorPoints = temp
    except:
        rep.majorPoints = [0,0,0,0,0,0,0]+[0,0,0]+[0,0,0,0,0]
        print("No major point")

    rep.weapon = findWeapon(file[3][0])                     # Weapon
    cmpt,temp = 0,[]
    while cmpt < len(file[4]):                              # Weapon Inventort
        temp += [findWeapon(file[4][cmpt])]
        cmpt += 1
    for weap in baseWeapon:
        if weap not in temp:
            temp.append(weap)
    rep.weaponInventory = sorted(temp,key=lambda weapon : weapon.name)
    try:                                                    # Equiped Skills
        cmpt,temp = 0,[]
        while cmpt < len(file[5]):
            if file[5][cmpt] != "0":
                temp += [findSkill(file[5][cmpt].replace("\n",""))]
            else:
                temp += ["0"]
            cmpt += 1
        while cmpt < 7:
            temp += ["0"]
            cmpt += 1
        rep.skills = temp
    except:
        rep.skills = ["0","0","0","0","0","0","0"]

    try:                                                   # Skill Inventory
        cmpt,temp = 0,[]
        while cmpt < len(file[6]):
            tempFind = findSkill(file[6][cmpt].replace("\n",""))
            if tempFind != None:
                temp += [tempFind]
            cmpt += 1
        for ski in baseSkills:
            if ski not in temp:
                temp.append(ski)
        rep.skillInventory = sorted(temp,key=lambda stuff : stuff.name)
    except:
        rep.skillInventory = []

    try:                        #Eqquiped Stuff
        cmpt,temp = 0,[]
        while cmpt < 3:
            temp += [findStuff(file[7][cmpt].replace("/n",""))]
            cmpt += 1
        rep.stuff = temp
    except:
        rep.stuff= [bbandeau,bshirt,bshoes]

    try:
        if file[7][3] != "0":
            rep.apparaWeap = findWeapon(file[7][3])
        else:
            rep.apparaWeap = None
    except:
        rep.apparaWeap = None
    try:
        if file[7][4] != "0":
            rep.apparaAcc = findStuff(file[7][4])
        else:
            rep.apparaAcc = None
    except:
        rep.apparaAcc = None

    # Stuff inventory
    cmpt,temp = 0,[]
    while cmpt < len(file[8]):
        tempFind = findStuff(file[8][cmpt].replace("/n",""))
        if tempFind != None:
            temp += [tempFind]
        cmpt += 1
    for stuffy in baseStuffs:
        if stuffy not in temp:
            temp.append(stuffy)
    rep.stuffInventory = sorted(temp,key=lambda stuff : stuff.name)

    cmpt,temp = 0,[]
    while cmpt < len(file[9]):
        file[9][cmpt] = file[9][cmpt].replace("\n","")
        otherTemp = findOther(file[9][cmpt])
        if type(otherTemp) != None:
            temp.append(otherTemp)
        else:
            print(file[9][cmpt])
        cmpt += 1
    rep.otherInventory = temp

    try:
        rep.procuration = [int(rep.owner)]
        for a in file[10]:
            rep.procuration += [int(a)]
    except:
        rep.procuration = [int(rep.owner)]

    try:
        rep.element = int(file[11][0])
    except:
        rep.element = ELEMENT_NEUTRAL
    
    try:
        rep.autoPoint = bool(int(file[11][1]))
    except:
        rep.autoPoint = False
    try:
        rep.autoStuff = bool(int(file[11][2]))
    except:
        rep.autoStuff = False

    try:
        for temp in file[12]:
            rep.haveProcurOn.append(int(temp))
    except:
        rep.haveProcurOn = []

    try:
        rep.limitBreaks = []
        for temp in file[13]:
            rep.limitBreaks.append(int(temp))
        if len(rep.limitBreaks) != 7:
            rep.limitBreaks = [0,0,0,0,0,0,0]
    except:
        rep.limitBreaks = [0,0,0,0,0,0,0]

    rep = userSettingsDb.getUserSettings(rep)
    return rep

def whatIsThat(advObject : Union[weapon,stuff,skill,other,str]):
    """``0`` : Weapon
        ``1`` : Skill
        ``2`` : Stuff
        ``3`` : Other
    """
    if findWeapon(advObject) != None:
        return 0
    elif findSkill(advObject) != None:
        return 1
    elif findStuff(advObject) != None:
        return 2
    elif findOther(advObject) != None:
        return 3
    else:
        return None

def getEmojiInfo(emoji : str):
    """Renvoie un tableau avec le nom de l'emoji et son identifiant"""
    rep = ["",""]
    first, second, temp = False, False, ""
    for a in emoji:
        if a == ":":
            if not(first):
                first = True
            elif not(second):
                rep[0] = temp
                temp, second = "",True
        elif first and a != ">":
            temp += a

    rep[1] = int(temp)
    return rep

def getEmojiObject(emoji : str):
    if type(emoji) == interactions.Emoji:
        return emoji
    try:
        temp = getEmojiInfo(emoji)
        return Emoji(name=temp[0],id=int(temp[1]))
    except ValueError:
        return Emoji(name=emoji)

async def loadingSlashEmbed(ctx : interactions.CommandContext):
    """Send a loading embed from a slash command"""
    return await ctx.send(embeds = interactions.Embed(title = "slash_command", description = emLoading))

def unhyperlink(text : str):
    """Return the text of Text without the hyperlink"""
    if text[0] == "[":
        temp = ""
        for a in text[1:]:
            if a != "]":
                temp += a
            else:
                temp.upper()
                return temp+"]"
    else:
        return text

def unemoji(text : str):
    """Retire les emojis du str donné"""
    rep = ""
    onEmoji,started = False, False
    for char in text:
        if char == "<":
            onEmoji = True
        elif char == ">":
            onEmoji = False
        elif char == ":" and onEmoji and not(started):
            temp = ""
            started = True
        elif char == ":" and onEmoji and started:
            rep += temp
            started = False
        elif onEmoji and started:
            temp += char
        elif not(onEmoji) and (char not in ["<",">"]):
            rep += char
    return rep

def separeUnit(number : Union[str,int]):
    """Return a string with a space for seperate the units"""
    number = str(number)
    temp = ""
    cmpt = -1
    numCmpt = -1
    while cmpt >= len(number)*-1:
        numCmpt += 1
        if numCmpt%3 == 0:
            temp = " "+temp
        temp = number[cmpt]+temp
        cmpt -= 1
    return temp[:-1]

gbvdb0 = """
    CREATE TABLE globalVar (
        name  STRING PRIMARY KEY
                    UNIQUE,
        value
);"""

gbvdb1 = """
    CREATE TABLE guildSettings (
        guildid  PRIMARY KEY
                    UNIQUE,
        botChannel  DEFAULT(0)
);"""

def completlyRemoveEmoji(text:str):
    toReturn,started,justExited = '',False,False
    for letter in text:
        if letter == '<' and not started:
            started = True
        elif letter == '>' and started:
            started,justExited = False, True
        elif not(started) and not(justExited and letter==" "):
            toReturn += letter

        if justExited and letter not in ['>',' ']:
            justExited = False
    return toReturn

gbdmaj = """CREATE TABLE guildStreamSettings (
    guild        INTEGER NOT NULL,
    streamerName STRING  NOT NULL,
    notifRole    INTEGER,
    notifMsg     STRING  DEFAULT [notifRole : streamerName viens de commencer un stream !],
    embedTitle   STRING  DEFAULT streamTitle,
    embedDesc    STRING  DEFAULT [gameName\nhyperlink],
    embedColor   STRING,
    notifChannel INTEGER,
    hyperlinkTxt STRING  DEFAULT [Ça se passe ici !],
    showImage    BOOLEAN DEFAULT (TRUE),
    image0       STRING,
    image1       STRING,
    image2       STRING
);
"""

listToChange = ["notifRole","streamerName","gameName","hyperlink","streamTitle","streamTitle"]
class streamEmbed():
    def __init__(self, guild, notifRole=None, notifChannel=None, streamerName="alice_kohishu", notifMsg="Hey notifRole ! **streamerName** viens de commencer un live !", embedTitle="streamTitle", embedDesc="Viens donc le voir jouer à gameName hyperlink", embedColor=light_blue, hyperlinkTxt="ici", showImage=True, image0=None, image1=None, image2=None):
        self.guild, self.notifRole, self.notifChannel, self.streamerName, self.embedTitle, self.embedDesc, self.showImage, self.image0, self.image1, self.image2 = guild, notifRole, notifChannel, streamerName, embedTitle, embedDesc, showImage, image0, image1, image2
        self.notifMsg = [notifMsg,"streamerName viens de commencer un stream !"][self.notifRole == None and notifMsg == "notifRole : streamerName viens de commencer un stream !"]
        if embedColor != None:
            if type(embedColor) != int:
                self.embedColor = int(embedColor,16)
            else:
                self.embedColor = embedColor
        else:
            self.embedColor = light_blue
        self.hyperlinkTxt = hyperlinkTxt
        self.hyperlink = "[{1}](https://www.twitch.tv/{0})".format(streamerName.lower(),hyperlinkTxt)

        listToChange = ["notifRole","streamerName","gameName","hyperlink","streamTitle"]
        for cmpt in range(len(listToChange)):
            self.notifMsg = self.notifMsg.replace(listToChange[cmpt],"{"+listToChange[cmpt]+"}")
            self.embedDesc = self.embedDesc.replace(listToChange[cmpt],"{"+listToChange[cmpt]+"}")
            self.embedTitle = self.embedTitle.replace(listToChange[cmpt],"{"+listToChange[cmpt]+"}")

class globalVarDb:
    """
        The class for the database who keep the global variables
    """
    def __init__(self):
        if not(os.path.exists("./data/database/globalCooldown.db")):
            temp = open("./data/database/globalCooldown.db","bw")
            print("Création du fichier \"globalCooldown.db\"")
            temp.close()

        self.con = sqlite3.connect(f"./data/database/globalCooldown.db")
        self.con.row_factory = sqlite3.Row
        self.database = "globalCooldown.db"

        cursor = self.con.cursor()
        try:
            cursor.execute("SELECT * FROM globalVar;")
        except:
            temp = ""
            for a in gbvdb0:
                if a != ";":
                    temp+=a
                else:
                    cursor.execute(temp)
                    temp = ""

            cursor.execute("INSERT INTO globalVar VALUES (?,?)",("fightEnabled",True))

            self.con.commit()
            print("Table globalVar crée")
        
        try:
            cursor.execute("SELECT * FROM guildSettings;")
        except:
            temp = ""
            for a in gbvdb1:
                if a != ";":
                    temp+=a
                else:
                    cursor.execute(temp)
                    temp = ""

            self.con.commit()
            print("Table guildSettings crée")
        
        try:
            cursor.execute("SELECT * FROM guildStreamSettings;")
        except:
            temp = ""
            for a in gbdmaj:
                if a != ";":
                    temp+=a
                else:
                    cursor.execute(temp)
                    temp = ""

            self.con.commit()
            print("Table guildStreamSettings crée")
        
        cursor.close()

    def fightEnabled(self) -> bool:
        """Return if the fights are enabled"""
        cursor = self.con.cursor()
        cursor.execute("SELECT value FROM globalVar WHERE name='fightEnabled'")
        return bool(cursor.fetchone()["value"])

    def changeFightEnabled(self, to:bool = None):
        """Change the status of the "fightEnabled" global variable\n
            - Parameter :\n
                .to : The status to set. If ``None``, just reverse it"""
        act = self.fightEnabled()

        if to == None:
            changeTo = not(act)
        else:
            changeTo = to

        cursor = self.con.cursor()
        cursor.execute("UPDATE globalVar SET value = ? WHERE name='fightEnabled';",(changeTo,))
        self.con.commit()
        cursor.close()

    def getRestartMsg(self,set=None):
        """Return the id of a precedent message\n
        - Parameters :\n
            .set : Set the global variable with the id given. If ``None``, return the value of the global variable"""
        cursor = self.con.cursor()
        cursor.execute("SELECT value FROM globalVar WHERE name=?",("restartID",))
        result = cursor.fetchall()

        if len(result) == 0:
            cursor.execute("INSERT INTO globalVar VALUES (?,?)",("restartID",0,))
            self.con.commit()

        if set == None:
            cursor.close()
            if len(result)==0:
                return 0
            else:
                return int(result[0]["value"])
        else:
            cursor.execute("UPDATE globalVar SET value = ? WHERE name = ?",(int(set),"restartID",))
            self.con.commit()
            cursor.close()
            return 0

    def setGuildBotChannel(self,guild_id:int,channel_id:int):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT guildid FROM guildSettings WHERE guildid = {guild_id};")
        result = cursor.fetchall()

        if len(result) == 0:
            cursor.execute(f"INSERT INTO guildSettings VALUES ({guild_id}, {channel_id});")
        else:
            cursor.execute(f"UPDATE guildSettings SET botChannel = {channel_id} WHERE guildid = {guild_id};")
        self.con.commit()
        cursor.close()

    def getGuildBotChannel(self,guild_id:int):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT botChannel FROM guildSettings WHERE guildid = {guild_id};")
        result = cursor.fetchall()

        if len(result) == 0:
            cursor.execute(f"INSERT INTO guildSettings (guildid) VALUES ({guild_id});")
            self.con.commit()
            cursor.close()
            return 0
        else:
            cursor.close()
            return result[0]["botChannel"]

    def getStreamAlertList(self):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT guild, streamerName FROM guildStreamSettings;")
        result = cursor.fetchall()
        cursor.close()
        return result

    def getStreamAlertEmbed(self, guild, streamerName):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT * FROM guildStreamSettings WHERE guild = ? AND streamerName = ?;",(guild, streamerName,))
        result = cursor.fetchone()
        cursor.close()

        return streamEmbed(result["guild"],result["notifRole"],result["notifChannel"],result["streamerName"],result["notifMsg"],result["embedTitle"],result["embedDesc"],result["embedColor"],result["hyperlinkTxt"],result["showImage"],result["image0"],result["image1"],result["image2"])

    def getStreamAlterPerGuild(self, guild):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT * FROM guildStreamSettings WHERE guild = ?;",(guild,))
        result = cursor.fetchall()
        cursor.close()
        toReturn = []
        for rep in result:
            toReturn.append(streamEmbed(rep["guild"],rep["notifRole"],rep["notifChannel"],rep["streamerName"],rep["notifMsg"],rep["embedTitle"],rep["embedDesc"],rep["embedColor"],rep["hyperlinkTxt"],rep["showImage"],rep["image0"],rep["image1"],rep["image2"]))

        return toReturn

    def updateStreamEmbed(self,streamEmbed:streamEmbed):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT * FROM guildStreamSettings WHERE guild = ? AND streamerName = ?;",(streamEmbed.guild, streamEmbed.streamerName,))
        result = cursor.fetchall()

        listToChange = ["notifRole","streamerName","gameName","hyperlink","streamTitle"]
        for cmpt in range(len(listToChange)):
            streamEmbed.notifMsg = streamEmbed.notifMsg.replace("{"+listToChange[cmpt]+"}",listToChange[cmpt])
            streamEmbed.embedDesc = streamEmbed.embedDesc.replace("{"+listToChange[cmpt]+"}",listToChange[cmpt])
            streamEmbed.embedTitle = streamEmbed.embedTitle.replace("{"+listToChange[cmpt]+"}",listToChange[cmpt])


        if len(result) <= 0:
            cursor.execute("INSERT INTO guildStreamSettings VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);",(streamEmbed.guild,streamEmbed.streamerName,streamEmbed.notifRole,streamEmbed.notifMsg,streamEmbed.embedTitle,streamEmbed.embedDesc,str(streamEmbed.embedColor),streamEmbed.notifChannel,streamEmbed.hyperlinkTxt,streamEmbed.showImage,streamEmbed.image0,streamEmbed.image1,streamEmbed.image2,))
            cursor.close()
            self.con.commit()
        else:
            cursor.execute("UPDATE guildStreamSettings SET notifRole=?, notifMsg=?, embedTitle=?, embedDesc=?, embedColor=?, notifChannel=?, hyperlinkTxt=?, showImage=?, image0=?, image1=?, image2=? WHERE guild = ? AND streamerName = ?",(streamEmbed.notifRole,streamEmbed.notifMsg,streamEmbed.embedTitle,streamEmbed.embedDesc,str(streamEmbed.embedColor),streamEmbed.notifChannel,streamEmbed.hyperlinkTxt,streamEmbed.showImage,streamEmbed.image0,streamEmbed.image1,streamEmbed.image2,streamEmbed.guild,streamEmbed.streamerName,))
            cursor.close()
            self.con.commit()

    def removeAlert(self,guild_id,streamer_login):
        cursor = self.con.cursor()
        cursor.execute("DELETE FROM guildStreamSettings WHERE guild = ? AND streamerName = ?;",(guild_id,streamer_login))
        cursor.close()
        self.con.commit()

globalVar = globalVarDb()

async def botChannelVerif(bot:interactions.Client,ctx:interactions.CommandContext):
    if globalVar.getGuildBotChannel(ctx.guild_id) in [0,ctx.channel_id]:
        return True

    else:
        chan = await get(bot, interactions.Channel, parent_id=int(ctx.guild_id), object_id=globalVar.getGuildBotChannel(ctx.guild_id))
        try:
            await ctx.send(embeds=interactions.Embed(title="__Paramètres__",color=light_blue,description="Je regrète mais on m'a demandé de répondre aux commandes que dans {0}".format(chan.mention)),ephemeral=True)
        except:
            pass
        return False

def highlight(string : str):
    if string not in [0,"-","0"]:
        return "**{0}**".format(string)
    else:
        return string

def getRandomTeamName() -> str:
    rdmFirst = teamFirstName[random.randint(0,len(teamFirstName)-1)]
    return rdmFirst[0] + " " + teamSecondName[random.randint(0,len(teamSecondName)-1)][rdmFirst[1]]

OBJECTIVE_WIN = 0
class fightContext():
    def __init__(self,giveEffToTeam1:list=[],giveEffToTeam2:list=[],objective=OBJECTIVE_WIN,nbEnnemis=8,nbAllies=8):
        self.giveEffToTeam1 = giveEffToTeam1
        self.giveEffToTeam2 = giveEffToTeam2
        self.objective = objective
        self.allowBoss = True
        self.allowTemp = True
        self.removeEnemy = []
        self.reduceEnemyLevel = 0
        self.nbEnnemis = nbEnnemis
        self.nbAllies = nbAllies
        self.setDanger = False

def getEmbedLength(emb = interactions.Embed):
    if type(emb) == interactions.Embed:
        toReturn = len(emb.title) + len(emb.description)
        try:
            for field in emb.fields:
                toReturn = toReturn + len(field.name) + len(field.value)
        except:
            pass
        return toReturn
    else:
        return 0

INCREASED_RESIST, NORMAL_RESIST, REDUCED_1_RESIST, REDUCED_2_RESIST = 15, 30, 50, 70

def getResistante(resist:int):
    baseResist, resist = min(resist,10)*INCREASED_RESIST/10, resist - min(resist,10)
    if resist > 0:
        baseResist += resist
    if baseResist > NORMAL_RESIST:
        baseResist = NORMAL_RESIST + (baseResist-NORMAL_RESIST)*0.65
    if baseResist > REDUCED_1_RESIST:
        baseResist = REDUCED_1_RESIST + (baseResist-REDUCED_1_RESIST)*0.45
    if baseResist > REDUCED_2_RESIST:
        baseResist = REDUCED_2_RESIST + (baseResist-REDUCED_2_RESIST)*0.15

    return baseResist

INCREASED_PENE, NORMAL_PENE, REDUCED_1_PENE, REDUCED_2_PENE= 10, 15, 25, 35
def getPenetration(pene:int):
    baseResist, pene = min(pene,5)*INCREASED_PENE/5, pene - min(pene,5)
    if pene > 0:
        baseResist += pene
    if baseResist > NORMAL_PENE:
        baseResist = NORMAL_PENE + (baseResist-NORMAL_PENE)*0.5
    if baseResist > REDUCED_1_PENE:
        baseResist = REDUCED_1_PENE + (baseResist-REDUCED_1_PENE)*0.3
    if baseResist > REDUCED_2_PENE:
        baseResist = REDUCED_2_PENE + (baseResist-REDUCED_2_PENE)*0.1

    return baseResist