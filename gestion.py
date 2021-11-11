import os,discord,random
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

def saveCharFile(path : str, char : char):
    #try:
    saved = ""
    for a in [char.owner,char.name,char.level,char.exp,char.currencies,char.species,char.color,char.team,int(char.customColor)]:
        saved += str(a)+";"
    saved += "\n"
    for a in [char.strength,char.endurance,char.charisma,char.agility,char.precision,char.intelligence,char.magie,char.aspiration,char.gender]:
        saved += str(a)+";"
    saved += "\n"
    for a in [char.resistance,char.percing,char.critical,char.points]:
        saved += str(a)+";"
    for a in char.bonusPoints:
        saved += str(a)+";"
    saved += "\n"
    saved += (char.weapon.id) +";\n"
    for a in char.weaponInventory:
        saved += a.id+";"
    saved += "\n"
    for a in char.skills:
        try:
            saved += a.id+";"
        except:
            saved += "0;"
    saved += "\n"
    for a in char.skillInventory:
        saved += a.id+";"
    saved += "\n"
    for a in char.stuff:
        saved += a.id+";"
    saved += "\n"
    for a in char.stuffInventory:
        saved += a.id+";"
    saved += "\n"
    for a in char.otherInventory:
        saved += a.id+";"
    saved += "\n"
    for a in char.procuration:
        saved += str(a)+";"
    saved += "\n"

    saved += str(char.element) +";\n"

    for mes in char.says.tabl():
        if mes == None:
            saved += ";\n"
        else:
            saved += mes + ";\n"

    rewriteFile(path,saved)
    return True
    #except:
        #return False

def loadCharFile(path,ctx="useless") -> char:
    """The Ctx option is there because it was needed in the past. But now it's useless and I don't want the explore all the code for clean it everywhere it was used"""
    file = readSaveFiles(path)
    rep = char(owner = file[0][0])
    rep.name = file[0][1]
    rep.level = int(file[0][2])
    rep.exp = int(file[0][3])
    rep.currencies = int(file[0][4])
    rep.species = int(file[0][5])
    rep.color = int(file[0][6])
    rep.team = int(file[0][7])
    try:
        rep.customColor = bool(int(file[0][8]))
    except:
        rep.customColor = False
    
    try:
        rep.gender = int(file[1][8])
    except:
        rep.gender = int(file[1][7])
        file[1][7] = file[1][6]
        file[1][6] = 0

    rep.strength,rep.endurance,rep.charisma,rep.agility,rep.precision,rep.intelligence,rep.magie,rep.aspiration = int(file[1][0]),int(file[1][1]),int(file[1][2]),int(file[1][3]),int(file[1][4]),int(file[1][5]),int(file[1][6]),int(file[1][7])
    rep.resistance,rep.percing,rep.critical,rep.points = int(file[2][0]),int(file[2][1]),int(file[2][2]),int(file[2][3])
    try:
        temp = []
        for a in file[2][4:11]:
            temp += [int(a)]
        if len(temp) == 7:
            rep.bonusPoints = temp
        else:
            rep.bonusPoints = temp[0:6]+[0]+temp[6:]
    except:
        rep.bonusPoints = [0,0,0,0,0,0,0]
    rep.weapon = findWeapon(file[3][0])
    cmpt,temp = 0,[]
    while cmpt < len(file[4]):
        temp += [findWeapon(file[4][cmpt])]
        cmpt += 1
    rep.weaponInventory = sorted(temp,key=lambda weapon : weapon.name)

    try:
        cmpt,temp = 0,[]
        while cmpt < len(file[5]):
            if len(file[5][cmpt])>2:
                file[5][cmpt] = file[5][cmpt][-2:]
            if file[5][cmpt] != "0":
                temp += [findSkill(file[5][cmpt])]
            else:
                temp += ["0"]
            cmpt += 1
        rep.skills = temp
    except:
        rep.skills = ["0","0","0","0","0"]

    #try:
    cmpt,temp = 0,[]
    while cmpt < len(file[6]):
        if len(file[6][cmpt]) > 2:
            file[6][cmpt] = file[6][cmpt][-2:]
        temp += [findSkill(file[6][cmpt])]
        cmpt += 1
    rep.skillInventory = sorted(temp,key=lambda stuff : stuff.name)
    """except:
        rep.skillInventory = []"""

    try:
        cmpt,temp = 0,[]
        while cmpt < len(file[7]):
            if len(file[7][cmpt]) > 2:
                file[7][cmpt] = file[7][cmpt][-2:]
            temp += [findStuff(file[7][cmpt])]
            cmpt += 1
        rep.stuff = temp
    except:
        rep.stuff = [bbandeau,bshirt,bshoes]

    try:
        cmpt,temp = 0,[]
        while cmpt < len(file[8]):
            if len(file[8][cmpt]) > 2:
                file[8][cmpt] = file[8][cmpt][-2:]
            temp += [findStuff(file[8][cmpt])]
            cmpt += 1
        rep.stuffInventory = sorted(temp,key=lambda stuff : stuff.name)
    except:
        rep.stuffInventory = [bbandeau,bshirt,bshoes]

    try:
        cmpt,temp = 0,[]
        while cmpt < len(file[9]):
            if len(file[9][cmpt]) > 2:
                file[9][cmpt] = file[9][cmpt][-2:]
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

        rep.procuration = set(rep.procuration)
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

def quickLoadCharFile(path : str):
    """A quicker function for load partial char object. Very usefull for give the exp and coins where someone talk. If I had to load a entire profile everytime than Flora spam in her guild, the CPU would not like it at all"""
    file = open(path)
    fileFiles = file.readlines()

    rep,temp = [],""
    for a in fileFiles[0]:
        if a == ";":
            rep += [temp]
            temp = ""
        else:
            temp = temp + a

    if len(rep)<9:
        rep += [False]

    temp = "\n"
    for a in fileFiles[1:]:
        if a != []:
            temp += a

    rep += [temp]

    rep2 = char(owner = int(rep[0]))
    rep2.name = rep[1]
    rep2.level = int(rep[2])
    rep2.exp = int(rep[3])
    rep2.currencies = int(rep[4])
    rep2.species = int(rep[5])
    rep2.color = int(rep[6])
    rep2.team = rep[7]
    rep2.customColor = bool(int(rep[8]))
    return [rep2,rep[9]]

def quickSaveCharFile(path : str, quickUser : list):
    """For saving the partial char object loaded with quickLoadCharFile"""
    user = quickUser[0]
    rep = f"{str(user.owner)};{user.name};{str(user.level)};{str(user.exp)};{str(user.currencies)};{str(user.species)};{str(user.color)};{user.team};{int(user.customColor)};{quickUser[1]}"
    rewriteFile(path,rep)

def checkIsBotChannel(ctx : discord.Message, guild,bot : discord.Client):
    if guild.bot > 0:
        if ctx.channel == bot.get_channel(guild.bot):
            return True
        else:
            return False
    else:
        return True

def whatIsThat(advObject : Union[weapon,stuff,skill,other,str]):
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

def hex_to_rgb(value : str):
    value = value[2:]
    if len(value)<6:
        value = "00"+value
    lv = len(value)
    try:
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    except:
        return None

def convertStrtoHex(string : str):
    hex_string = string.lstrip('#')
    try:
        an_integer = int(hex_string, 16)
        return an_integer
    except:
        return None

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