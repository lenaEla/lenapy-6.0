import os,random,sqlite3,json, asyncio
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
            if user.says == None:
                blabla = says().tabl()
            else:
                blabla = user.says.tabl()
            toAddCat, toAddValue = [], []
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
                    textIconSet += ", {0} = {1}".format(iconSetCatNames[cmpt],int(iconSetValues[cmpt]))
            if textIconSet != "":
                textIconSet = textIconSet[2:]
                print("UPDATE userSettings SET {0} WHERE userId = {1};".format(textIconSet,user.owner))
                cursory.execute("UPDATE userSettings SET {0} WHERE userId = ?;".format(textIconSet),(user.owner,))

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
    """Return a random value from the list"""
    if type(liste) != list:
        liste = [liste]

    if len(liste) == 1:
        return liste[0]
    else:
        return liste[random.randint(0,len(liste)-1)]

def saveCharFile(path : str = None, user : char = None):
    if user == None:
        raise Exception("No Character referenced")

    userSettingsDb.updateUserSettings(user)
    convertProfFileIntoJson(character=user)

def loadCharFile(path : str = None, user:char = None, id:int=None) -> char:
    """
        Return a ``char`` object loaded from the file at ``path``
    """
    toRead = ""

    if path.__class__ == str:
        toRead = path
    elif user != None or path.__class__ == char:
        if path != None:
            user = path
        toRead = "./userProfile/{0}.json".format(user.owner)
    elif id != None or path.__class__ == int:
        if path != None:
            id = path
        toRead = "./userProfile/{0}.json".format(id)
    else:
        raise Exception("No path or character referenced")

    jsonFile = open(toRead)
    loadedDict, tmpDict = json.load(jsonFile), {}

    try:
        for k, v in loadedDict["chipInventory"].items():
            try:
                tmpDict[int(k)] = v
            except:
                tmpDict[int(k)] = (0,0)
        loadedDict["chipInventory"] = tmpDict
    except KeyError:
        loadedDict["equippedChips"], loadedDict["chipInventory"] = [None,None,None,None,None], copy.deepcopy(initChipInv)

    rep = char(0,fromDict=loadedDict)
    rep = userSettingsDb.getUserSettings(rep)

    rep.weapon, rep.apparaAcc, rep.apparaWeap = findWeapon(rep.weapon), findStuff(rep.apparaAcc), findWeapon(rep.apparaWeap)
    for indx, weapId in enumerate(rep.weaponInventory):
        temp = findWeapon(weapId)
        if temp != None:
            rep.weaponInventory[indx] = temp

    for indx, skillId in enumerate(rep.skillInventory):
        temp, toRemove = findSkill(skillId), []
        if temp != None:
            rep.skillInventory[indx] = temp
        else:
            toRemove.append(skillId)
    
        for obj in toRemove:
            rep.skillInventory.remove(obj)

    for indx, skillId in enumerate(rep.skills):
        temp = findSkill(skillId)
        if temp != None:
            rep.skills[indx] = temp

    for indx, stuffId in enumerate(rep.stuffInventory):
        temp, toRemove = findStuff(stuffId), []
        if temp != None:
            rep.stuffInventory[indx] = temp
        else:
            toRemove.append(stuffId)

        for obj in toRemove:
            rep.stuffInventory.remove(obj)

    for indx, stuffId in enumerate(rep.stuff):
        temp = findStuff(stuffId)
        if temp != None:
            rep.stuff[indx] = temp

    for indx, objId in enumerate(rep.otherInventory):
        temp = findOther(objId)
        if temp != None:
            rep.otherInventory[indx] = temp

    return rep

def whatIsThat(advObject : Union[weapon,stuff,skill,other,str]):
    """``0`` : Weapon
        ``1`` : Skill
        ``2`` : Stuff
        ``3`` : Other
    """
    if type(advObject) == weapon or findWeapon(advObject) != None:
        return 0
    elif type(advObject) == skill or findSkill(advObject) != None:
        return 1
    elif type(advObject) == stuff or findStuff(advObject) != None:
        return 2
    elif type(advObject) == other or findOther(advObject) != None:
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
    if type(emoji) == interactions.CustomEmoji:
        return emoji
    try:
        temp = getEmojiInfo(emoji)
        return PartialEmoji(name=temp[0],id=int(temp[1]))
    except ValueError:
        return PartialEmoji(name=emoji)

async def loadingSlashEmbed(ctx : interactions.SlashContext):
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
        if letter == '<' and not(started):
            started = True
        elif letter == '>' and started:
            started = False
        elif not(started):
            toReturn += letter
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
        self.guild, self.notifRole, self.notifChannel, self.streamerName, self.embedTitle, self.embedDesc, self.showImage, self.image0, self.image1, self.image2 = int(guild), notifRole, notifChannel, streamerName, embedTitle, embedDesc, showImage, image0, image1, image2
        if self.notifRole != None:
            self.notifRole = int(self.notifRole)
        if self.notifChannel != None:
            self.notifChannel = int(self.notifChannel)
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
        cursor, guild = self.con.cursor(), int(guild)
        cursor.execute(f"SELECT * FROM guildStreamSettings WHERE guild = ? AND streamerName = ?;",(guild, streamerName,))
        result = cursor.fetchone()
        cursor.close()

        return streamEmbed(result["guild"],result["notifRole"],result["notifChannel"],result["streamerName"],result["notifMsg"],result["embedTitle"],result["embedDesc"],result["embedColor"],result["hyperlinkTxt"],result["showImage"],result["image0"],result["image1"],result["image2"])

    def getStreamAlterPerGuild(self, guild):
        cursor, guild = self.con.cursor(), int(guild)
        cursor.execute(f"SELECT * FROM guildStreamSettings WHERE guild = ?;",(guild,))
        result = cursor.fetchall()
        cursor.close()
        toReturn = []
        for rep in result:
            toReturn.append(streamEmbed(rep["guild"],rep["notifRole"],rep["notifChannel"],rep["streamerName"],rep["notifMsg"],rep["embedTitle"],rep["embedDesc"],rep["embedColor"],rep["hyperlinkTxt"],rep["showImage"],rep["image0"],rep["image1"],rep["image2"]))

        return toReturn

    def updateStreamEmbed(self,streamEmbed:streamEmbed):
        cursor = self.con.cursor()
        if type(streamEmbed.notifChannel) != int:
            streamEmbed.notifChannel = int(streamEmbed.notifChannel.id)
        if type(streamEmbed.notifRole) != int:
            streamEmbed.notifRole = int(streamEmbed.notifRole.id)
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

async def botChannelVerif(bot:interactions.Client,ctx:interactions.SlashContext):
    if globalVar.getGuildBotChannel(ctx.guild_id) in [0,ctx.channel_id]:
        return True

    else:
        chan = await bot.get_channel(globalVar.getGuildBotChannel(ctx.guild_id))
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

def getMinusPurcent(nb:int):
    return (100-nb)/100

def getPlusPurcent(nb:int):
    return (100+nb)/100

def getOsamodasJson() -> List[dict]:
    jsonFile = json.load(open("./data/database/osamodas.json"))
    return jsonFile["smnList"]

def getNextLetter(letter:str=""):
    if letter == "":
        return "A"
    else:
        tablAlpha = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","X","Y","Z"]
        for cmpt in range(len(tablAlpha)):
            if tablAlpha[cmpt] == letter:
                return tablAlpha[cmpt+1]
        return ""

def convertProfFileIntoJson(character:char):
    existedBefore = os.path.exists("./userProfile/{0}.json".format(character.owner))
    tablInventory = [character.weaponInventory,character.skills,character.skillInventory,character.stuff,character.stuffInventory,character.otherInventory,[character.weapon],[character.apparaAcc],[character.apparaWeap]]
    for indx1, tabl in enumerate(tablInventory):
        for indx2, obj in enumerate(tabl):
            if obj != None:
                if obj.__class__ != str:
                    tablInventory[indx1][indx2] = obj.id
                else:
                    tablInventory[indx1][indx2] = obj

    character.weapon,character.apparaAcc,character.apparaWeap = (tablInventory[-3][0],tablInventory[-2][0],tablInventory[-1][0])

    tempDict = {}
    for tmpChipId, tmpChip in character.chipInventory.items():
        if type(tmpChip) == userChip:
            tempDict[tmpChipId] = [tmpChip.lvl, tmpChip.progress]
        else:
            tempDict[tmpChipId] = tmpChip
    character.chipInventory = tempDict
    charDict = character.__dict__
    charDict["says"] = None
    with open("./userProfile/{0}.json".format(character.owner),"w") as newFile:
        try:
            json.dump(charDict, newFile)
        except Exception as e:
            newFile.close()
            if not(existedBefore):
                os.remove("./userProfile/{0}.json".format(character.owner))
            print_exc()
            return e
    if os.path.exists("./userProfile/{0}.prof".format(character.owner)):
        os.remove("./userProfile/{0}.prof".format(character.owner))
