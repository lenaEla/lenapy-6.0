import os,discord,random,sqlite3
from traceback import print_exc
from typing import Union
import discord_slash
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
        self.con = sqlite3.connect(f"./data/database/aliceStats.db")
        self.con.row_factory = sqlite3.Row
        self.database = "aliceStats.db"

    def updateTeam(self,team:int,members:Union[List[int],List[char]]):
        cursory, listToAdd, listToAdd2 = self.con.cursor(), "" , ""
        
        # Allready Exist ?
        cursory.execute("SELECT teamMember0 FROM userTeams WHERE teamId = {0};".format(team))
        result = cursory.fetchone()

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

    def getTeamMember(self,team:int) -> List[int]:
        cursory = self.con.cursor()
        cursory.execute('SELECT teamMember0, teamMember1, teamMember2, teamMember3, teamMember4, teamMember5, teamMember6, teamMember7 FROM userTeams WHERE teamId = {0};'.format(team))
        result = cursory.fetchone()

        if result == None:
            return None

        toReturn = []
        for a in result:
            if a not in [0,None]:
                toReturn.append(a)

        return toReturn

    def getAllTeamIds(self) -> List[int]:
        cursory, toReturn = self.con.cursor(), []
        cursory.execute("SELECT teamId FROM userTeams;")
        result = cursory.fetchall()

        for a in result:
            toReturn.append(a["teamId"])
        
        return toReturn

    def doesTeamExist(self,team:int):
        cursory = self.con.cursor()
        cursory.execute("SELECT teamMember0 FROM userTeams WHERE teamId = {0};".format(team))
        result = cursory.fetchone()
        return not(result == None)

class userSettingsDbEndler:
    def __init__(self):
        self.con = sqlite3.connect(f"./data/database/aliceStats.db")
        self.con.row_factory = sqlite3.Row
        self.database = "aliceStats.db"

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

        cursor = self.con.cursor()

    def updateUserSays(self,user:char):
        cursory = self.con.cursor()

        cursory.execute("SELECT userId FROM userSettings WHERE userId = {0};".format(user.owner))
        result = cursory.fetchone()

        if result == None:
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

            cursory.execute("INSERT INTO userSettings (userId{3}{0}) VALUES ({1}{3}{2});".format(toAddStr[0],user.owner,toAddStr[1],["",","][toAddStr[0]!=""]))
            self.con.commit()
            print("{0} a été rajouté dans la base de donnée".format(user.name))
        else:
            toAddCat, toAddValue, blabla = [], [], user.says.tabl()
            for a in range(len(blabla)):
                if blabla[a] != None:
                    toAddCat.append(userSettingsInterCatNames[a])
                    toAddValue.append(blabla[a])

            toAddStr, tempTabl = "", [toAddCat,toAddValue]
            for cmpt in range(len(tempTabl[0])):
                toAdd = ""
                for b in tempTabl[1][cmpt]:
                    if b == "'":
                        toAdd += "''"
                    else:
                        toAdd += b
                toAdd += ""

                toAddStr+= "{0}='{1}'".format(tempTabl[0][cmpt],toAdd)
                if cmpt < len(tempTabl[0])-1:
                    toAddStr+=","

            if toAddStr != "":
                cursory.execute("UPDATE userSettings SET {0} WHERE userId = {1};".format(toAddStr,user.owner))
                self.con.commit()
        cursory.close()

    def getUserSays(self,user:char):
        cursory = self.con.cursor()

        toStr = ""
        for a in range(len(userSettingsInterCatNames)):
            toStr += userSettingsInterCatNames[a]
            if a < len(userSettingsInterCatNames)-1:
                toStr+=","

        cursory.execute("SELECT {1} FROM userSettings WHERE userId = {0};".format(user.owner,toStr))
        result = cursory.fetchone()

        if result == None:
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

            cursory.execute("INSERT INTO userSettings (userId{3}{0}) VALUES ({1}{3}{2});".format(toAddStr[0],user.owner,toAddStr[1],["",","][toAddStr[0]!=""]))

            self.con.commit()
            print("{0} a été rajouté dans la base de donnée".format(user.name))
            return says()
        else:
            tablTemp = []
            for a in result:
                tablTemp.append(a)
            
            temp = says()

            return temp.fromTabl(tablTemp)

    def getUserIconSettings(self,user:char):
        cursory = self.con.cursor()

        cursory.execute("SELECT hand, affElem, affAcc, affWeap FROM userSettings WHERE userId = {0};".format(user.owner))
        result = cursory.fetchone()
        user.handed, user.showAcc, user.showElement, user.showWeapon = result["hand"], bool(result["affAcc"]), bool(result["affElem"]), bool(result["affWeap"])
        return user

    def updateUserIconSettings(self,user:char):
        cursory = self.con.cursor()

        cursory.execute("SELECT userId FROM userSettings WHERE userId = {0};".format(user.owner))
        result = cursory.fetchone()

        if result == None:
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

            cursory.execute("INSERT INTO userSettings (userId{3}{0}) VALUES ({1}{3}{2});".format(toAddStr[0],user.owner,toAddStr[1],["",","][toAddStr[0]!=""]))
            self.con.commit()
            print("{0} a été rajouté dans la base de donnée".format(user.name))

        else:
            cursory.execute("UPDATE userSettings SET hand = ?, affElem = ?, affAcc = ?, affWeap = ? WHERE userId = {0};".format(user.owner),(user.handed,user.showElement,user.showAcc,user.showWeapon))
            self.con.commit()
            cursory.close()

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

def commandArgs(ctx : discord.Message):
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

async def loadingEmbed(ctx : discord.Message):
    """A function for send loading embed from a message command.\n
    Mostly useless with slash commands now"""
    return await ctx.channel.send(embed = discord.Embed(title = commandArgs(ctx)[0], description = emoji.loading))

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
    rep = discord.Embed(title = errorType, description = msgError)
    rep.set_footer(text = "Fin de la commande")
    return rep

def randRep(liste : list):
    """Hum... Where I use that...
    choose command"""
    return liste[random.randint(0,len(liste)-1)]

def saveCharFile(path : str = None, user : char = None):
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

    userSettingsDb.updateUserSays(user)
    userSettingsDb.updateUserIconSettings(user)
    rewriteFile(path,saved)
    return True

def loadCharFile(path : str = None, user:char = None) -> char:
    """
        Return a ``char`` object loaded from the file at ``path``
    """
    if path != None:
        file = readSaveFiles(path)
    elif user != None:
        file = readSaveFiles("./userProfile/{0}.prof".format(user.owner))
    else:
        raise Exception("Argument error : No path or user given")
    rep = char(owner = int(file[0][0]))                     # Owner
    rep.name = file[0][1]                                   # Name
    rep.level = int(file[0][2])                             # Level
    rep.exp = int(file[0][3])                               # Exp
    rep.currencies = int(file[0][4])                        # Currencies
    rep.species = int(file[0][5])                           # Species
    rep.color = int(file[0][6])                             # Color
    rep.team = int(file[0][7])                              # Team id
    try:                                                    # Custom color
        rep.customColor = bool(int(file[0][8]))
    except:
        rep.customColor = False
    try:                                                    # Gender I guess ?
        rep.gender = int(file[1][8])
    except:
        rep.gender = int(file[1][7])
        file[1][7] = file[1][6]
        file[1][6] = 0
    try:
        rep.colorHex = file[0][9]
    except:
        rep.colorHex = "None"

    try:
        rep.stars = int(file[0][10])
    except:
        rep.stars = 0
    try:
        rep.iconForm = int(file[0][11])
    except:
        rep.iconForm = 0
    try:
        rep.secElement = int(file[0][12])
    except:
        rep.secElement = ELEMENT_NEUTRAL
    
    # Stats
    rep.strength,rep.endurance,rep.charisma,rep.agility,rep.precision,rep.intelligence,rep.magie,rep.aspiration = int(file[1][0]),int(file[1][1]),int(file[1][2]),int(file[1][3]),int(file[1][4]),int(file[1][5]),int(file[1][6]),int(file[1][7])
    rep.resistance,rep.percing,rep.critical,rep.points = int(file[2][0]),int(file[2][1]),int(file[2][2]),int(file[2][3])

    try:
        rep.majorPointsCount = int(file[2][-1])
    except:
        rep.majorPointsCount = 0
        print("No major point count")

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
        rep.skillInventory = sorted(temp,key=lambda stuff : stuff.name)
    except:
        rep.skillInventory = []

    try:                        # Equiped Stuff
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
    rep.stuffInventory = sorted(temp,key=lambda stuff : stuff.name)

    cmpt,temp = 0,[]
    while cmpt < len(file[9]):

        file[9][cmpt] = file[9][cmpt].replace("\n","")
        temp += [findOther(file[9][cmpt])]
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

    rep.says = userSettingsDb.getUserSays(rep)
    rep = userSettingsDb.getUserIconSettings(rep)

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
    temp = getEmojiInfo(emoji)
    return {"name":temp[0],"id":temp[1]}

async def loadingSlashEmbed(ctx : discord_slash.SlashContext):
    """Send a loading embed from a slash command"""
    return await ctx.send(embed = discord.Embed(title = "slash_command", description = emoji.loading))

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

globalVar = globalVarDb()

async def botChannelVerif(bot:discord.Client,ctx:discord_slash.SlashContext):
    if globalVar.getGuildBotChannel(ctx.guild_id) in [0,ctx.channel_id]:
        return True
    
    else:
        chan = await bot.fetch_channel(globalVar.getGuildBotChannel(ctx.guild_id))
        try:
            await ctx.send(embed=discord.Embed(title="__Paramètres__",color=light_blue,description="Désolée, mais on m'a demandé de répondre aux commandes que dans {0}".format(chan.mention)),delete_after=5)
        except:
            try:
                await ctx.channel.send(embed=discord.Embed(title="__Paramètres__",color=light_blue,description="Désolée, mais on m'a demandé de répondre aux commandes que dans {0}".format(chan.mention)),delete_after=5)
            except:
                pass
        return False

def loadAdvDutyFile(actName : str, dutyName : str) -> duty:
    """Load the texts for Duty of the main adventure\n
    Parameters :\n
    .actName : The name of the main act of the duty\n
    .dutyName : The name of the duty"""

    dutyTextList = []
    file = open("./data/advScriptTxt/{0}/{1}.txt".format(actName,dutyName.replace(".txt","")))
    text, ref = "",""
    fileContent = file.readlines()
    for line in fileContent:
        baliseOpend, tempBalise, endOfText, endOfTextFlag = False,"","",False
        for car in line:
            if car == "[":
                baliseOpend = True
                tempBalise = "["
            elif car == "]":
                baliseOpend = False
                tempBalise += "]"

                if tempBalise.startswith("[ref:"):
                    ref = tempBalise[5:-1]
                else:
                    text += tempBalise

                tempBalise = ""

            elif car == "=" and not(endOfTextFlag):
                endOfTextFlag = True
                endOfText += car

            elif car == "=" and endOfTextFlag:
                endOfText += car
                if len(endOfText) >= 5:
                    dutyTextList.append(dutyText(ref,text))
                    ref,text,baliseOpend, tempBalise, endOfText, endOfTextFlag = "","",False,"","",False

            elif car != "=" and endOfTextFlag:
                endOfTextFlag = False
                text += endOfText + car
                endOfText = ""

            elif baliseOpend:
                tempBalise += car

            else:
                text += car

    dut = duty(actName,dutyName,dutyTextList)
    file.close()
    return dut

def highlight(string : str):
    if string not in [0,"-","0"]:
        return "**{0}**".format(string)
    else:
        return string
