import os,discord,random
from classes import *
from adv import findWeapon,findEffect,findOther,findSkill,findStuff

"""
Main functions module
"""

def lecFile(fichier):
    "Renvoie sous forme de liste toutes les lignes d'un fichier en retirant le retour chariot\n\nParamètre : fichier (str)\n\nRetourne :\nlist"
    fich = open(fichier, "r")
    liste = fich.readlines()
    comp = 1
    while comp <= len(liste)-1:
        liste[comp]=liste[comp][0:-1]
        comp+=1

    fich.close()
    return liste

def empty(liste):
    "Teste si une liste est vide\n\nParamètre : liste (list)\n\nRetourne : bool"
    if len(liste) == 0:
        return True
    else:
        return False

def listToStr(liste):
    "Renvoie tout le contenue d'un list en un str, séparées par des espaces\n\nParamètre : liste (list)\n\nRetourne : str"
    temp = ""
    for a in liste:
        temp+=a+" "
    return temp

def cutStrToList(string,caractere):
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

def existDir(string):
    "Vérifie si le dossier au chemin String existe. Si oui, return True. Si non, créait le dossier et return False"
    if not os.path.exists(string):
        print(f"Création du dossier {string}")
        os.mkdir(string)
        return False
    else:
        return True

def rewriteFile(string,content):
    fich = open(string, "w")
    fich.write(content)
    fich.close()

def existFile(string):
    "Vérifie si le fichier au chemin String existe. Si oui, return True. Si non, créait le fichier et return False"
    if not os.path.exists(string):
        temp =open(string,"w")
        temp.write("0")
        temp.close()
        return False
    else: 
        return True

def commandArgs(ctx):
    rep,temp = [],""
    for a in ctx.content:
        if a == " ":
            rep = rep + [temp]
            temp = ""
        else:
            temp = temp + a
    rep = rep + [temp] + [None]
    return rep

async def loadingEmbed(ctx):
    return await ctx.channel.send(embed = discord.Embed(title = commandArgs(ctx)[0], description = emoji.loading))

def readSaveFiles(path):
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

def saveSaveFiles(path,settings):
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

def choice(liste):
    """Lol I don't use it anymore"""
    msg, cmpt = "\n",0
    for a in liste:
        msg += f"\n[{cmpt}] : {a}"
        cmpt += 1

    return msg

def errorEmbed(errorType, msgError):
    """Return a error embed ready to be send"""
    rep = discord.Embed(title = errorType, description = msgError)
    rep.set_footer(text = "Fin de la commande")
    return rep

def randRep(liste):
    """Hum... Where I use that..."""
    return liste[random.randint(0,len(liste)-1)]

def saveGuildSettings(path,server):
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

def saveCharFile(path,char):
    try:
        saved = ""
        for a in [char.owner,char.name,char.level,char.exp,char.currencies,char.species,char.color,char.team,int(char.customColor)]:
            saved += str(a)+";"
        saved += "\n"
        for a in [char.strength,char.endurance,char.charisma,char.agility,char.precision,char.intelligence,char.aspiration,char.gender]:
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

        rewriteFile(path,saved)
        return True
    except:
        return False

def loadCharFile(path,ctx="useless"):
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
        rep.gender = int(file[1][7])
    except:
        rep.gender = GENDER_OTHER
    rep.strength,rep.endurance,rep.charisma,rep.agility,rep.precision,rep.intelligence,rep.aspiration = int(file[1][0]),int(file[1][1]),int(file[1][2]),int(file[1][3]),int(file[1][4]),int(file[1][5]),int(file[1][6])
    rep.resistance,rep.percing,rep.critical,rep.points = int(file[2][0]),int(file[2][1]),int(file[2][2]),int(file[2][3])
    try:
        temp = []
        for a in file[2][4:10]:
            temp += [int(a)]
        if len(temp) == 6:
            rep.bonusPoints = temp
        else:
            print(file[2][4:10])
    except:
        rep.bonusPoints = [0,0,0,0,0,0]
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

    try:
        cmpt,temp = 0,[]
        while cmpt < len(file[6]):
            if len(file[6][cmpt]) > 2:
                file[6][cmpt] = file[6][cmpt][-2:]
            temp += [findSkill(file[6][cmpt])]
            cmpt += 1
        rep.skillInventory = sorted(temp,key=lambda stuff : stuff.name)
    except:
        rep.skillInventory = []

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
        for a in file[10]:
            rep.procuration += [int(a)]
    except:
        rep.procuration = []
    try:
        rep.element = int(file[11][0])
    except:
        rep.element = ELEMENT_NEUTRAL

    return rep

def quickLoadCharFile(path):
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

def quickSaveCharFile(path,quickUser):
    """For saving the partial char object loaded with quickLoadCharFile"""
    user = quickUser[0]
    rep = f"{str(user.owner)};{user.name};{str(user.level)};{str(user.exp)};{str(user.currencies)};{str(user.species)};{str(user.color)};{user.team};{int(user.customColor)};{quickUser[1]}"
    rewriteFile(path,rep)

def checkIsBotChannel(ctx,guild,bot):
    if guild.bot > 0:
        if ctx.channel == bot.get_channel(guild.bot):
            return True
        else:
            return False
    else:
        return True

def whatIsThat(advObject):
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

def hex_to_rgb(value):
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

async def loadingSlashEmbed(ctx):
    return await ctx.send(embed = discord.Embed(title = "slash_command", description = emoji.loading))
