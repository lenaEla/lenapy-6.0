import os,discord,random,sqlite3
from typing import Union
import discord_slash
from classes import *
from adv import findWeapon,findOther,findSkill,findStuff

"""
Main functions module
"""

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

def saveGuildSettings(path : str, server : server):
    """Save the server settings in the file in Path"""
    try:
        saved = ""
        for a in [server.prefixe,server.patchnote,server.bot]:
            saved += str(a)+";"
        saved += "\n"
        for a in [int(server.colorRole.enable),server.colorRole.red,server.colorRole.orange,server.colorRole.yellow,server.colorRole.green,server.colorRole.lightBlue,server.colorRole.blue,server.colorRole.purple,server.colorRole.pink]:
            saved += str(a)+";"
        
        rewriteFile(path,saved)
        return True
    except:
        return False

def saveCharFile(path : str = None, user : char = None):
    if user == None:
        raise Exception("Attribut Error : No user gave")
    if path == None:
        path = './userProfile/{0}.prof'.format(user.owner)
    #try:
    saved = ""
    for a in [user.owner,user.name,user.level,user.exp,user.currencies,user.species,user.color,user.team,int(user.customColor),user.colorHex,user.stars]:
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

    saved += str(user.element) +";\n"

    for mes in user.says.tabl():
        if mes == None:
            saved += ";\n"
        else:
            saved += mes + ";\n"

    rewriteFile(path,saved)
    return True
    #except:
        #return False

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
        print('No stars founds')
    
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
        rep.skills = temp
    except:
        rep.skills = ["0","0","0","0","0"]

    try:                                                   # Skill Inventory
        cmpt,temp = 0,[]
        while cmpt < len(file[6]):
            temp += [findSkill(file[6][cmpt].replace("\n",""))]
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

    try:                        # Stuff inventory
        cmpt,temp = 0,[]
        while cmpt < len(file[8]):
            temp += [findStuff(file[8][cmpt].replace("/n",""))]
            cmpt += 1
        rep.stuffInventory = sorted(temp,key=lambda stuff : stuff.name)
    except:
        rep.stuffInventory = [bbandeau,bshirt,bshoes]

    try:
        cmpt,temp = 0,[]
        while cmpt < len(file[9]):

            file[9][cmpt] = file[9][cmpt].replace("\n","")
            temp += [findOther(file[9][cmpt])]
            cmpt += 1
        rep.otherInventory = temp
    except:
        rep.otherInventory = []

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
        if file[12] != "\n":
            temp = file[12][0]
            while temp.startswith("\n") or temp.startswith(" "):
                temp = temp[1:]
            if temp != "":
                rep.says.start = temp
    except:
        pass
    try:
        if file[13] != "\n":
            temp = file[13][0]
            while temp.startswith("\n") or temp.startswith(" "):
                temp = temp[1:]
            if temp != "":
                rep.says.ultimate = temp
    except:
        pass
    try:
        if file[14] != "\n":
            temp = file[14][0]
            while temp.startswith("\n") or temp.startswith(" "):
                temp = temp[1:]
            if temp != "":
                rep.says.limiteBreak = temp
    except:
        pass
    try:
        if file[15] != "\n":
            temp = file[15][0]
            while temp.startswith("\n") or temp.startswith(" "):
                temp = temp[1:]
            if temp != "":
                rep.says.onKill = temp
    except:
        pass
    try:
        if file[16] != "\n":
            temp = file[16][0]
            while temp.startswith("\n") or temp.startswith(" "):
                temp = temp[1:]
            if temp != "":
                rep.says.onDeath = temp
    except:
        pass
    try:
        if file[17] != "\n":
            temp = file[17][0]
            while temp.startswith("\n") or temp.startswith(" "):
                temp = temp[1:]
            if temp != "":
                rep.says.onResurect = temp
    except:
        pass
    try:
        if file[18] != "\n":
            temp = file[18][0]
            while temp.startswith("\n") or temp.startswith(" "):
                temp = temp[1:]
            if temp != "":
                rep.says.blueWinAlive = temp
    except:
        pass
    try:
        if file[19] != "\n":
            temp = file[19][0]
            while temp.startswith("\n") or temp.startswith(" "):
                temp = temp[1:]
            if temp != "":
                rep.says.blueWinDead = temp
    except:
        pass
    try:
        if file[20] != "\n":
            temp = file[20][0]
            while temp.startswith("\n") or temp.startswith(" "):
                temp = temp[1:]
            if temp != "":
                rep.says.blueLoose = temp
    except:
        pass
    try:
        if file[21] != "\n":
            temp = file[21][0]
            while temp.startswith("\n") or temp.startswith(" "):
                temp = temp[1:]
            if temp != "":
                rep.says.redWinAlive = temp
    except:
        pass
    try:
        if file[22] != "\n":
            temp = file[22][0]
            while temp.startswith("\n") or temp.startswith(" "):
                temp = temp[1:]
            if temp != "":
                rep.says.redWinDead = temp
    except:
        pass
    try:
        if file[23] != "\n":
            temp = file[23][0]
            while temp.startswith("\n") or temp.startswith(" "):
                temp = temp[1:]
            if temp != "":
                rep.says.redLoose = temp
    except:
        pass

    return rep

def checkIsBotChannel(ctx : discord.Message, guild,bot : discord.Client):
    if guild.bot > 0:
        if ctx.channel == bot.get_channel(guild.bot):
            return True
        else:
            return False
    else:
        return True

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

globalVar = globalVarDb()

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