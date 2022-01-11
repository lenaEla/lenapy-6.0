##########################################################
# Importations :
import asyncio
import discord, random, os, emoji, datetime, sys, shutil
from discord_slash.model import SlashCommandOptionType,ButtonStyle

from data.database import *
from classes import *

from adv import *
from donnes import *
from gestion import *
from advance_gestion import *

from commands_files.command_encyclopedia import *
from commands_files.command_fight import *
from commands_files.command_inventory import *
from commands_files.command_start import *
from commands_files.command_procuration import *
from commands_files.command_points import *
from commands_files.command_shop import *
from commands_files.sussess_endler import *
from commands_files.command_patchnote import *
from commands_files.command_help import *
from commands_files.command_patchnote import *
from commands_files.alice_stats_endler import *
from commands_files.command_duty import adventureDutySelect
from discord.ext import commands, tasks
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
from data.bot_tokens import lenapy, shushipy

###########################################################
# Initialisations des variables de bases :
started = False

intents = discord.Intents.all()

bot = commands.Bot(command_prefix = "l!", description= "LenaPy par LenaicU",intents=intents)
slash = SlashCommand(bot, sync_commands=True)

existDir(absPath + "/userProfile/")
existDir(absPath + "/userTeams/")
existDir(absPath + "/data/images/")
existDir(absPath + "/data/database/")
existDir(absPath + "/data/images/headgears/")
existDir(absPath + "/data/images/weapons/")
existDir(absPath + "/data/images/char_icons/")
existDir(absPath + "/data/patch/")
existDir(absPath + "/data/fightLogs/")
existDir(absPath + "/data/images/elemIcon/")
existDir(absPath + "/data/backups/")

if not(os.path.exists("./data/advScriptTxt/")):
    raise Exception("Missing folder error : advScriptTxt do not exist")
for verif in allActs:
    if not(os.path.exists("./data/advScriptTxt/"+verif[0])):
        raise Exception("Missing folder error : {0} do not exist".format(verif[0]))
    else:
        for fileVerif in verif[1:]:
            if not(os.path.exists("./data/advScriptTxt/"+verif[0]+"/"+fileVerif)):
                raise Exception("Missing file error : {0} do not exist".format(verif[0]+"/"+fileVerif))

actualyFight,actualyQuickFight = [],[]
pathUserProfile = absPath + "/userProfile/"

###########################################################
# Initialisation
allShop = weapons + skills + stuffs + others

class shopClass:
    """The class who endle the shop\n
    Maybe I should shearch how it's writed...
    """
    def __init__(self,shopList : list):
        """When inited, look for a existing shop data in the database and load it"""
        self.shopping = []
        summation = 0
        for a in shopRepatition:
            summation += a
        cmpt = 0
        while cmpt < summation:
            self.shopping.append(None)
            cmpt += 1

        if shopList != False:
            for a in range(0,len(shopList)):
                if a != None:
                    nani = whatIsThat(shopList[a])
                    try:
                        if nani == 0:
                            self.shopping[a] = findWeapon(shopList[a])
                        elif nani == 1:
                            self.shopping[a] = findSkill(shopList[a])
                        elif nani == 2:
                            self.shopping[a] = findStuff(shopList[a])
                        elif nani == 3:
                            self.shopping[a] = findOther(shopList[a])
                    except:
                        pass

    async def newShop(self):
        """Genere a new shop and upload it in the database\n
        - Returns\n
            - ``True`` if it succed
            - ``False`` else"""
        try:
            shopping = list(range(0,len(self.shopping)))

            if globalVar.fightEnabled():
                babies = datetime.datetime.now() + horaire + datetime.timedelta(hours=1)
                while babies.hour%3 != 0:
                    babies = babies + datetime.timedelta(hours=1)

                await bot.change_presence(status=discord.Status.online,activity=discord.Game(name="Prochain shop à "+babies.strftime('%Hh')))

            shopWeap,shopSkill,shopStuff,ShopOther = [],[],[],others[:]
            for a in weapons:
                if a.price > 0:
                    shopWeap.append(a)
                    if a in weapons[:3]:
                        shopWeap.append(a)
                    
            for a in skills:
                if a.price > 0:
                    shopSkill.append(a)
                    if a in skills[:5]:
                        shopWeap.append(a)
                    
            for a in stuffs:
                if a.price > 0:
                    shopStuff.append(a)
                    if a in stuffs[:5]:
                        shopWeap.append(a)
            
            temp = shopRepatition
            tablShop:List[list[Union[weapon,skill,stuff,other]]] = [shopWeap,shopSkill,shopStuff,ShopOther]
            cmp = 0
            for a in [0,1,2,3]:
                cmpt = 0
                while cmpt < temp[a]:
                    fee = random.randint(0,len(tablShop[a])-1)
                    shopping[cmp] = tablShop[a][fee]
                    tablShop[a].remove(tablShop[a][fee])
                    cmpt+=1
                    cmp+=1
                
            temp = ""
            stuffDB.addShop(shopping)
            for a in shopping:
                temp += f"\n{a.name}"

            print("\n--------------\nLe nouveau shop est :"+temp+"\n------------")
            self.shopping = shopping
            return True
        except:
            return False

async def inventoryVerif(bot,toVerif:Union[char,str]):
    if type(toVerif) == str:
        user = loadCharFile(absPath + "/userProfile/" + toVerif)
    else:
        user = toVerif
    aliceStatsDb.addUser(user)
    allReadySee,haveUltimate,modifSkill,modifStuff = [],False,0,0
    ballerine = "Une ou plusieurs compétences ont été déséquipés de votre personnage :\n"
    babie = "Un ou plusieurs équipements ont été retiré de votre inventaire :\n"

    for a in range(0,5):
        if user.skills[a] != None and user.skills[a] != "0":
            if user.skills[a] in allReadySee:
                ballerine += f"\n__{user.skills[a].name}__ (Doublon)"
                modifSkill += 1
                user.skills[a] = "0"
            else:
                allReadySee+=[user.skills[a]]

        if user.skills[a] != "0" and user.skills[a] != None:
            if not(user.skills[a].havConds(user=user)):
                ballerine += f"\n__{user.skills[a].name}__ (Conditions non respectées)"
                modifSkill += 1
                user.skills[a] = "0"

        if user.skills[a] != "0" and user.skills[a]!=None and user.skills[a].ultimate and haveUltimate:
            ballerine += f"\n__{user.skills[a].name}__ (Plus de 1 compétence ultime équipée)"
            modifSkill += 1
            user.skills[a] = "0"
        elif user.skills[a] != "0" and user.skills[a]!=None and user.skills[a].ultimate:
            haveUltimate = True

    tablInventory = [user.weaponInventory,user.skillInventory,user.stuffInventory,user.otherInventory]
    for y in tablInventory:
        allReadySee = []
        for a in y:
            if a not in allReadySee:
                allReadySee.append(a)
            else:
                babie += f"\n__{a.name}__ (Doublon)"
                modifStuff += 1
                y.remove(a)
                user.currencies += a.price

    if modifStuff > 0:
        user.weaponInventory,user.skillInventory,user.stuffInventory,user.otherInventory = tablInventory[0],tablInventory[1],tablInventory[2],tablInventory[3]
        babie += "\n\nCes objets vous ont été remboursés"

    if modifSkill+modifStuff > 0:
        saveCharFile(user=user)
        try:
            toUser = await bot.fetch_user(user.owner)
            message = ""
            if modifSkill > 0:
                message+=ballerine+"\n"
            if modifStuff > 0:
                message+=babie
            await toUser.send(embed=discord.Embed(title = "__Problème lors de la vérification automatique de l'inventaire__",color=user.color,description=message))
        except:
            pass

        print(f"Le profil de {user.name} a été mise à jour")

    temp = ""
    for equip in user.stuff:
        if not(equip.havConds(user)):
            change = getAutoStuff(equip,user)
            user.stuff[equip.type] = change

            temp += "{0} {2} -> {1} {3}\n".format(equip.emoji,change.emoji,equip.name,change.name)

    if temp != "":
        temp = "Vous ne respectez pas les conditions de niveaux d'un ou plusieurs de vos équipements\nLe(s) équipement(s) suivant a(ont) automatiquement été remplacé(s) :\n\n"+temp
        saveCharFile(user=user)
        try:
            toUser = await bot.fetch_user(user.owner)
            await toUser.send(embed=discord.Embed(title = "__Problème lors de la vérification automatique de l'inventaire__",color=user.color,description=temp))
        except:
            pass

        print(f"Le profil de {user.name} a été mise à jour")

    errorElem = False
    if user.level < 20 and user.element in [ELEMENT_SPACE,ELEMENT_TIME,ELEMENT_LIGHT,ELEMENT_DARKNESS]:
        errorElem = True
    elif user.level < 10 and user.element != ELEMENT_NEUTRAL:
        errorElem = True

    if errorElem:
        temp = ""
        user.element = ELEMENT_NEUTRAL
        if user.have(elementalCristal):
            user.currencies += elementalCristal.price
            temp = "Vous avez été crédité de {0} <:coins:862425847523704832>".format(elementalCristal)
        else:
            user.otherInventory.append(elementalCristal)
            temp = "Vous avez obtenu un {0} {1}".format(elementalCristal.emoji,elementalCristal.name)
        saveCharFile(user=user)

        try:
            toUser = await bot.fetch_user(user.owner)
            await toUser.send(embed=discord.Embed(title = "__Problème lors de la vérification automatique de l'inventaire__",color=user.color,description="Votre élément de ne respecte pas les restrictions de niveau\n\n"+temp))
        except:
            pass

    userAchivments = achivement.getSuccess(user)
    tempMissingAchivRecompMsg = ""
    for ach in userAchivments.tablAllSuccess():
        if ach.haveSucced and ach.recompense != [None] and ach.recompense not in [["qe"],["qh"]]:
            for rec in ach.recompense:
                whatty = whatIsThat(rec)
                obj = [findWeapon(rec),findSkill(rec),findStuff(rec)][whatty]

                if not(user.have(obj)):
                    if whatty == 0:
                        user.weaponInventory.append(obj)
                    elif whatty == 1:
                        user.skillInventory.append(obj)
                    elif whatty == 2:
                        user.stuffInventory.append(obj)

                    tempMissingAchivRecompMsg += "\n{0} {1} ({2})".format(obj.emoji,obj.name,ach.name)
            saveCharFile("./userProfile/{0}.prof".format(user.owner),user)

    if tempMissingAchivRecompMsg != "":
        try:
            toUser = await bot.fetch_user(user.owner)
            await toUser.send(embed=discord.Embed(title = "__Problème lors de la vérification automatique de l'inventaire__",color=user.color,description="Une ou plusieurs récompenses de succès n'ont pas été trouvées dans votre inventaire et vous ont été restituée :\n"+tempMissingAchivRecompMsg))
            print("{0} n'avait pas toutes ces récompenses de succès".format(user.name))
        except:
            pass

    if user.level > 55:
        user = loadCharFile(user=user)
        user.level, user.exp = 55,0
        user = restats(user)

        saveCharFile(user=user)

        toSend = await bot.fetch_user(user.owner)

        try:
            await toSend.send(embed=discord.Embed(title="__Problème lors de la vérification automatique de votre inventaire :__",description="Votre niveau est supérieur au niveau maximal, et à été ramené à ce dernier\nVos points bonus ont été rénitialisées\n\nPensez à faire un tour vers /prestige",color=light_blue))
        except:
            pass

bidule = stuffDB.getShop()
shopping = shopClass(bidule["ShopListe"])

async def restart_program(bot : discord.Client, ctx=None):
    """If no teams are into a fight, restart the bot\n
    If a team fighting, wiat for them to finish then restart the bot"""
    if ctx != None:
        msg = await ctx.send(embed = discord.Embed(title="Redémarrage en attente...",description="Vérifications des équipes en combat..."))
    else:
        chan = await bot.fetch_channel(912137828614426707)
        msg = await chan.send(embed = discord.Embed(title="Redémarrage automatique en attente...",description="Vérifications des équipes en combat..."))
    globalVar.changeFightEnabled(False)
    await bot.change_presence(status=discord.Status.dnd,activity=discord.Game(name="attendre la fin des combats en cours pour redémarrer"))

    globalVar.getRestartMsg(int(msg.id))
    fighting = True
    firstIt = True
    while fighting:
        fighting = False
        for team in os.listdir("./userTeams/"):
            if teamWinDB.isFightingBool(int(team[:-5]))[0]:
                if firstIt:
                    teamTemp = readSaveFiles("./userTeams/"+team)[0]
                    us = await bot.fetch_user(teamTemp[0])
                    await msg.edit(embed = discord.Embed(title="Redémarrage en attente...",description="Un combat est encore en cours <a:loading:862459118912667678> ({0})".format(us.mention)))
                    firstIt = False
                fighting = True
                break
        if fighting:
            await asyncio.sleep(3)
    
    await msg.edit(embed = discord.Embed(title="Redémarrage en attente...",description="Redémarrage en cours..."))
    await bot.change_presence(status=discord.Status.idle,activity=discord.Game(name="redémarrer"))

    args = sys.argv[:]

    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]
    os.execv(sys.executable, args)

def create_backup():
    """Copy all the characters profiles files into a new directory\n
    Return a ``string`` with the path of the backup directory"""
    now = datetime.datetime.now()
    nowStr = now.strftime("%Y%m%d_%H%M")
    path = "./data/backups/"+nowStr
    try:
        os.mkdir(path)
    except:
        pass

    for charFile in os.listdir("./userProfile/"):
        shutil.copy('./userProfile/{0}'.format(charFile),path+"/"+charFile)
    
    return "Un backup a été sauvegardé à la destinaiton suivante :\n"+path

def delete_old_backups():
    """Remove backups directorys older than 3 days"""
    now = datetime.datetime.now()
    temp = ""
    for name in os.listdir("./data/backups/"):
        timeBUp = datetime.datetime.strptime(name,"%Y%m%d_%H%M")
        if now > timeBUp+datetime.timedelta(days=3):
            for files in os.listdir("./data/backups/{0}/".format(name)):
                os.remove("./data/backups/{0}/{1}".format(name,files))
            try:
                os.removedirs("./data/backups/{0}".format(name))
                temp+="./data/backups/{0} a été supprimé\n".format(name)
            except:
                temp+="./data/backups/{0} n'a pas pu être supprimé\n".format(name)
    return temp

async def remakeEmojis(ctx=None):
    if ctx != None:
        msg = await ctx.send(embed = discord.Embed(title="Remake des emojis..."))
    else:
        chan = await bot.fetch_channel(912137828614426707)
        msg = await chan.send(embed = discord.Embed(title="Remake des emojis..."))

    await bot.change_presence(status=discord.Status.idle,activity=discord.Game(name="refaire les emojis..."))
    
    async def refresh(text : str):
        await msg.edit(embed = discord.Embed(title="Remake des emojis...",description=text))

    await refresh("Suppression de la base de données...")
    try:
        customIconDB.dropCustom_iconTablDB()
    except:
        pass
    await refresh("Supression des emojis...")

    iconGuildList = []
    if not(isLenapy):
        iconGuildList = ShushyCustomIcons
    else:
        iconGuildList = LenaCustomIcons

    allEmojisNum = 0
    for a in iconGuildList:
        emojiGuild = await bot.fetch_guild(a)
        allEmojisNum += len(emojiGuild.emojis)

    cmpt = 0
    now = datetime.datetime.now().second
    lastTime = copy.deepcopy(now)
    for a in iconGuildList:
        emojiGuild = await bot.fetch_guild(a)

        for b in emojiGuild.emojis:
            try:
                print("Emoji de {0} supprimé".format(b.name))
            except:
                pass
            await b.delete()
            cmpt += 1

            if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
                await refresh("Supression des emojis ({0} %)".format(int(cmpt/allEmojisNum*100)))
                lastTime = now

    await refresh("Création des émojis...")
    allChar = os.listdir("./userProfile/")
    lenAllChar = len(allChar)
    cmpt = 0

    for num in allChar:
        user = loadCharFile("./userProfile/"+num)
        await makeCustomIcon(bot,user)
        cmpt += 1

        if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
            await refresh("Création des émojis ({0} %)".format(int(cmpt/lenAllChar*100)))
            lastTime = now

    await refresh("Fini !")
    if ctx != None:
        await ctx.channel.send("Le remake des emojis est terminées !",delete_after=10)

    ballerine = datetime.datetime.now() + horaire + datetime.timedelta(hours=1)
    while ballerine.hour%3 != 0:
        ballerine = ballerine + datetime.timedelta(hours=1)

    await bot.change_presence(status=discord.Status.online,activity=discord.Game(name="Prochain shop à "+ballerine.strftime('%Hh')))

@tasks.loop(seconds=1)
async def oneClock():
    """A simple clock who check every second if a minute have passed\n
    If it is the case, start ``minuteClock``"""
    tick = datetime.datetime.now()
    if tick.second%60 == 0 and not(minuteClock.is_running()):
        minuteClock.start()

@tasks.loop(minutes=1)
async def minuteClock():
    """
        A simple clock who check every minutes if a hour have passed\n
        If it is the case, start ``hourClock``\n
        If ``oneClock`` is running, end it
    """
    if oneClock.is_running():
        oneClock.stop()
    tick = datetime.datetime.now()
    if tick.minute%60 == 0 and not(hourClock.is_running()):
        hourClock.start()

@tasks.loop(hours=1)
async def hourClock():
    if minuteClock.is_running():
        minuteClock.stop()
    tick = datetime.datetime.now()+horaire
    if tick.hour%3==0:
        temp = False
        while not(temp):
            temp = await shopping.newShop()

    if tick.hour==0:
        for log in os.listdir("./data/fightLogs/"):
            try:
                os.remove("./data/fightLogs/"+log)
                print("{0} supprimé".format("./data/fightLogs/"+log))
            except:
                print("{0} n'a pas pu être supprimé".format("./data/fightLogs/"+log))

    if tick.hour == 4:
        chan = await bot.fetch_channel(912137828614426707)
        await chan.send(embed=discord.Embed(title="__Auto backup__",color=light_blue,description=create_backup()))
        temp = delete_old_backups()
        if temp != "":
            await chan.send(embed=discord.Embed(title="__Auto backup__",color=light_blue,description=temp))
        await remakeEmojis()
        await restart_program(bot)

    # Skill Verif
    for filename in os.listdir("./userProfile/"):
        await inventoryVerif(bot,filename)

# -------------------------------------------- ON READY --------------------------------------------
@bot.event
async def on_ready():
    print("\n---------\nThe bot is fully online ! Starting the initialisations things...\n---------\n")
    startMsg = globalVar.getRestartMsg()
    if startMsg != 0:                           # If the bot was rebooted with the admin command, change the status
        msg = await bot.fetch_channel(912137828614426707)
        msg = await msg.fetch_message(startMsg)

        await msg.edit(embed=discord.Embed(title="Redémarrage en cours...",description="Phase d'initalisation..."))
        globalVar.changeFightEnabled(True)

    # Load the guild's settings files
    if os.path.exists("./guildSettings/"):
        listGuildSet = os.listdir(absPath + "/guildSettings/")
        guilds = list(range(0,len(listGuildSet)))
        cmpt = 0
        lastTime = datetime.datetime.now().second
        lenGuild = len(listGuildSet)
        print("Starting guild's settings loading... 0%")
        while cmpt < lenGuild:
            guildSettings = readSaveFiles(absPath + "/guildSettings/"+listGuildSet[cmpt])
            guilds[cmpt] = server(int(listGuildSet[cmpt][0:-4]),guildSettings[0][0],int(guildSettings[0][1]),int(guildSettings[0][2]))
            guilds[cmpt].colorRole.enable, guilds[cmpt].colorRole.red, guilds[cmpt].colorRole.orange, guilds[cmpt].colorRole.yellow, guilds[cmpt].colorRole.green, guilds[cmpt].colorRole.lightBlue, guilds[cmpt].colorRole.blue, guilds[cmpt].colorRole.purple, guilds[cmpt].colorRole.pink = bool(int(guildSettings[1][0][1:])),int(guildSettings[1][1]),int(guildSettings[1][2]),int(guildSettings[1][3]),int(guildSettings[1][4]),int(guildSettings[1][5]),int(guildSettings[1][6]),int(guildSettings[1][7]),int(guildSettings[1][8])

            guild = await bot.fetch_guild(guilds[cmpt].id)
            guilds[cmpt].name = guild.name
            globalVar.setGuildBotChannel(guilds[cmpt].id,guilds[cmpt].bot)
            os.remove(absPath + "/guildSettings/"+listGuildSet[cmpt])

            now = datetime.datetime.now().second
            if now >= lastTime + 2 or (now <= 2 and now >= lastTime + 2 - 60):
                print("Loading guild's settings... {0}%".format(round((cmpt/lenGuild)*100)))
                lastTime = now

            cmpt += 1

        print("All guild's settings are loaded !\n")
        os.rmdir("./guildSettings/")

    # Shop reload and status change
    if bidule != False:
        ballerine = datetime.datetime.now() + horaire + datetime.timedelta(hours=1)
        while ballerine.hour%3 != 0:
            ballerine = ballerine + datetime.timedelta(hours=1)

        if not(globalVar.fightEnabled()):
            await bot.change_presence(status=discord.Status.dnd,activity=discord.Game(name="Les combats sont actuellements désactivés"))
        else:
            await bot.change_presence(status=discord.Status.online,activity=discord.Game(name="Prochain shop à "+ballerine.strftime('%Hh')))

    if not(oneClock.is_running()):
        oneClock.start()

    teamWinDB.resetAllFightingStatus()

    print("\nDownloading the emojis for the custom icons...")
    await downloadAllHeadGearPng(bot)
    await downloadAllWeapPng(bot)
    await downloadAllIconPng(bot)
    await downloadElementIcon(bot)
    print("Download complete\nVerefying the characters inventorys...")
    
    for filename in os.listdir("./userProfile/"):
        await inventoryVerif(bot,filename)

    print("\n------- End of the initialisation -------")
    if not(isLenapy):
        print(datetime.datetime.now().strftime('%H:%M'))

    if startMsg != 0:
        await msg.edit(embed=discord.Embed(title="Redémarrage en cours...",color=light_blue,description="Le bot a bien été redémarré"))
        await msg.channel.send("Le redémarrage du bot est terminé Léna",delete_after=10)
        globalVar.getRestartMsg(int(0))
        print("Redémarrage terminé")

# ====================================================================================================
#                                               COMMANDS
# ====================================================================================================

# -------------------------------------------- ON MESSAGE --------------------------------------------
@bot.event
async def on_message(ctx : discord.message.Message):
    if ctx.content.startswith("l!test") and ctx.author.bot == 213027252953284609:
        user = loadCharFile("./userProfile/{0}.prof".format(ctx.author.id))
        await makeCustomIcon(bot,user)
        await ctx.add_reaction('<:littleStar:925860806602682369>')

    else:
        pathUserProfile = "./userProfile/{0}.prof".format(ctx.author.id)
        if os.path.exists(pathUserProfile) and len(ctx.content)>=3:
            try:
                await addExpUser(bot,pathUserProfile,ctx,3,3)
            except:
                print("Erreur dans la gestion du message de {0}".format(ctx.author.name))

# -------------------------------------------- ENCYCLOPEDIA --------------------------------------------
@slash.slash(name="encyclopedia",description="Vous permet de consulter l'encyclopédie", options=[
    create_option(
        name="destination", description="Que voulez vous consulter ?", required=True,option_type=3,
        choices=[
            create_choice(name="Accessoires",value="accessoires"),
            create_choice(name="Vêtements",value="vetements"),
            create_choice(name="Chaussures",value="chaussures"),
            create_choice(name="Armes",value="armes"),
            create_choice(name="Compétences",value="competences"),
            create_choice(name="Alliés Temporaires",value='tempAlies'),
            create_choice(name="Ennemis",value="ennemies"),
            create_choice(name="Boss",value="boss"),
            create_choice(name="Objets non-possédés",value="locked"),
            create_choice(name="Succès",value="achivements")
        ]
    )
])
async def comEncyclopedia(ctx,destination):
    if not(await botChannelVerif(bot,ctx)):
        return 0

    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    user = loadCharFile(pathUserProfile)
        
    await encylopedia(bot,ctx,destination,user)

# -------------------------------------------- FIGHT --------------------------------------------
# normal fight
@slash.subcommand(base="fight",name="normal",description="Permet de lancer un combat normal")
async def normal(ctx):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    if not(globalVar.fightEnabled()):
        await ctx.send(embed=discord.Embed(title="__Combats désactivés__",description="Les combats sont actuellement désactivés pour cause de bug ou de déploiment imminant d'une mise à jour\nVeuillez vous référer au status du bot pour savoir si les combats sont désactivés ou non"),delete_after=10)
        return 0

    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    try:
        user = loadCharFile(pathUserProfile)
    except:
        await ctx.send("Vous n'avez pas commencé l'aventure",delete_after=10)
        return 0

    ballerine,temp = 0,0
    if user.team == 0:
        ballerine = user.owner
    else:
        ballerine = user.team

    timing = teamWinDB.getFightCooldown(ballerine)
    fightingStatus = teamWinDB.isFightingBool(ballerine)

    if fightingStatus[0]:
        channel = await bot.fetch_channel(fightingStatus[2])
        fightingMessage = await channel.fetch_message(fightingStatus[0])
        
        fightingRespond = "__Votre équipe affronte actuellement :__\n"
        temp = ""
        for letter in fightingStatus[1]:
            if letter==";" and len(temp) > 0:
                ennemi = findEnnemi(temp)
                if ennemi == None:
                    ennemi = findAllie(temp)
                if ennemi != None:
                    fightingRespond += "{0} {1}\n".format(ennemi.icon,ennemi.name)
                else:
                    fightingRespond += "<:blocked:897631107602841600> L'ennemi n'a pas pu être trouvé\n"
                temp = ""
            else:
                temp+=letter

        msg = await ctx.send(embed = discord.Embed(title="__/fight__",color=user.color,description=fightingRespond+"\nsur __[{0}]({1})__".format(channel.guild.name,fightingMessage.jump_url)),delete_after=15)
        return 0
    elif timing > 0:
        msg = await ctx.send(embed = errorEmbed("Cooldown","Votre équipe ne pourra faire de combats normaux que dans {0} minute{1} et {2} seconde{3}".format(timing//60,["","s"][timing//60 > 1],timing%60,["","s"][timing%60 > 1])),delete_after=10)
        return 0

    team1 = []
    if user.team != 0:
        file = readSaveFiles(absPath + "/userTeams/" + str(user.team) + ".team")
        for a in file[0]:
            team1 += [loadCharFile(absPath + "/userProfile/" + a + ".prof")]
    else:
        team1 = [user]

    # Random event
    fun = random.randint(0,99)

    if fun < 0:                 # For testing purposes
        team1.append(findAllie("Alice"))
        await fight(bot,team1,[],ctx,False)

    elif fun < 1:               # But nobody came
        teamIcon = ""
        for wonderfullIdea in team1:
            teamIcon += "{0} {1}\n".format(await getUserIcon(bot,wonderfullIdea),wonderfullIdea.name)

        temp1 = discord.Embed(title = "__Résultats du combat :__",color = black,description="__Danger :__ <a:bnc:908762423111081994>\n__Nombre de tours :__ <a:bnc:908762423111081994>\n__Durée :__ <a:bnc:908762423111081994>")
        temp1.add_field(name="<:empty:866459463568850954>\n__Vainqueurs :__",value=teamIcon,inline=True)
        temp1.add_field(name="<:empty:866459463568850954>\nPerdants :",value="[[But nobody came](https://bit.ly/3wDwyF3)]",inline=True)

        await ctx.send(embed = temp1,components=[])

    elif fun < 2:              # All OctoHeals ! Yes, it's for you H
        temp = team1
        temp.sort(key=lambda overheal: overheal.level,reverse=True)
        maxLvl = temp[0].level

        team2 = []
        lenBoucle = max(4,len(team1))
        cmpt = 0

        octoHealVet = findEnnemi("Octo Soigneur Vétéran")
        octoHeal = findEnnemi("Octo Soigneur")

        if maxLvl < octoHealVet.baseLvl:
            alea = copy.deepcopy(octoHeal)
        else:
            alea = copy.deepcopy(octoHealVet)

        alea.changeLevel(maxLvl)
        alea.charisma = alea.charisma//2

        while cmpt < lenBoucle:
            team2.append(alea)
            cmpt += 1

        await fight(bot,team1,team2,ctx,False)

    elif fun < 3:              # All Temmies
        temp = team1
        temp.sort(key=lambda overheal: overheal.level,reverse=True)
        maxLvl = temp[0].level

        team2 = []
        lenBoucle = max(4,len(team1))
        cmpt = 0

        alea = copy.deepcopy(findEnnemi("Temmie"))
        alea.changeLevel(maxLvl)
        alea.magie = alea.magie // 3

        while cmpt < lenBoucle:
            team2.append(alea)
            cmpt += 1

        await fight(bot,team1,team2,ctx,False)

    elif fun < 4:              # BOUM BOUM BOUM BOUM
        temp = team1
        temp.sort(key=lambda overheal: overheal.level,reverse=True)
        maxLvl = temp[0].level

        team2 = []
        lenBoucle = max(4,len(team1))
        cmpt = 0

        alea = copy.deepcopy(findEnnemi("OctoBOUM"))
        alea.skills, alea.weapon, alea.magie, alea.exp = [totalAnnilCastSkill0,None,None,None,None], BOUMBOUMBOUMBOUMweap, int(alea.magie * 2), 12
        alea.changeLevel(maxLvl)

        while cmpt < lenBoucle:
            team2.append(alea)
            cmpt += 1

        await fight(bot,team1,team2,ctx,False)

    elif fun < 10:             # Raid
        tablAllTeams = os.listdir("./userTeams/")
        random.shuffle(tablAllTeams)

        moyTeam = 0
        for a in team1:
            moyTeam += a.level

        moyTeam = moyTeam/len(team1)

        for tempTeamPath in tablAllTeams:
            if int(tempTeamPath.replace(".team","")) != user.team and not(teamWinDB.isFightingBool(int(tempTeamPath.replace(".team","")))[0]):
                tempTeam, moyTempTeam = [], 0
                file = readSaveFiles(absPath + "/userTeams/" + tempTeamPath)
                for a in file[0]:
                    tempUser = loadCharFile(absPath + "/userProfile/" + a + ".prof")
                    moyTempTeam += tempUser.level
                    tempTeam += [tempUser]

                moyTempTeam = moyTempTeam/max(1,len(tempTeam))
                if moyTeam <= moyTempTeam+10 and moyTeam >= moyTempTeam-10:
                    team1 += tempTeam
                    break

        temp = team1
        temp.sort(key=lambda overheal: overheal.level,reverse=True)
        maxLvl = temp[0].level
        team2 = []
        alea = copy.deepcopy(tablRaidBoss[random.randint(0,len(tablRaidBoss)-1)])

        alea.changeLevel(maxLvl)
        team2.append(alea)

        await fight(bot,team1,team2,ctx,False,bigMap=True)

    else:
        await fight(bot,team1,[],ctx,False)

# quick fight
@slash.subcommand(base="fight",name="quick",description="Vous permet de faire un combat en sautant directement à la fin")
async def comQuickFight(ctx):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    if not(globalVar.fightEnabled()):
        await ctx.send(embed=discord.Embed(title="__Combats désactivés__",description="Les combats sont actuellement désactivés pour cause de bug ou de déploiment imminant d'une mise à jour\nVeuillez vous référer au status du bot pour savoir si les combats sont désactivés ou non"),delete_after=10)
        return 0

    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    try:
        user = loadCharFile(pathUserProfile)
    except:
        await ctx.send("Vous n'avez pas commencé l'aventure",delete_after=10)
        return 0

    ballerine,temp = 0,0
    if user.team == 0:
        ballerine = user.owner
    else:
        ballerine = user.team

    timing = teamWinDB.getFightCooldown(ballerine,True)
    fightingStatus = teamWinDB.isFightingBool(ballerine)

    if fightingStatus[0]:
        channel = await bot.fetch_channel(fightingStatus[2])
        fightingMessage = await channel.fetch_message(fightingStatus[0])
        
        fightingRespond = "__Votre équipe affronte actuellement :__\n"
        temp = ""
        for letter in fightingStatus[1]:
            if letter==";" and len(temp) > 0:
                ennemi = findEnnemi(temp)
                if ennemi == None:
                    ennemi = findAllie(temp)
                if ennemi != None:
                    fightingRespond += "{0} {1}\n".format(ennemi.icon,ennemi.name)
                else:
                    fightingRespond += "<:blocked:897631107602841600> L'ennemi n'a pas pu être trouvé\n"
                temp = ""
            else:
                temp+=letter

        await ctx.send(embed = discord.Embed(title="__/fight__",color=user.color,description=fightingRespond+"\nsur __[{0}]({1})__".format(channel.guild.name,fightingMessage.jump_url)),delete_after=15)
        return 0
    elif timing > 0:
        await ctx.send(embed = errorEmbed("Cooldown","Votre équipe ne pourra faire de combats rapide que dans {0} minute{1} et {2} seconde{3}".format(timing//180,["","s"][timing//180 > 1],timing%60,["","s"][timing%60 > 1])),delete_after=10)
        return 0

    team1 = []
    if user.team != 0:
        file = readSaveFiles(absPath + "/userTeams/" + str(user.team) + ".team")
        for a in file[0]:
            team1 += [loadCharFile(absPath + "/userProfile/" + a + ".prof")]
    else:
        team1 = [user]

    fun = random.randint(0,99)

    if fun < 5:             # Raid
        tablAllTeams = os.listdir("./userTeams/")
        random.shuffle(tablAllTeams)

        moyTeam = 0
        for a in team1:
            moyTeam += a.level

        moyTeam = moyTeam/len(team1)

        for tempTeamPath in tablAllTeams:
            if int(tempTeamPath.replace(".team","")) != user.team and not(teamWinDB.isFightingBool(int(tempTeamPath.replace(".team","")))[0]):
                tempTeam, moyTempTeam = [], 0
                file = readSaveFiles(absPath + "/userTeams/" + tempTeamPath)
                for a in file[0]:
                    tempUser = loadCharFile(absPath + "/userProfile/" + a + ".prof")
                    moyTempTeam += tempUser.level
                    tempTeam += [tempUser]

                moyTempTeam = moyTempTeam/max(1,len(tempTeam))
                if moyTeam <= moyTempTeam+10 and moyTeam >= moyTempTeam-10:
                    team1 += tempTeam
                    break

        temp = team1
        temp.sort(key=lambda overheal: overheal.level,reverse=True)
        maxLvl = temp[0].level
        team2 = []
        alea = copy.deepcopy(tablRaidBoss[random.randint(0,len(tablRaidBoss)-1)])

        alea.changeLevel(maxLvl)
        team2.append(alea)

        await fight(bot,team1,team2,ctx,bigMap=True)
    else:
        await fight(bot,team1,[],ctx)

# octogone fight
@slash.subcommand(base="fight",subcommand_group="octogone",name="solo",description="Affrontez quelqu'un en 1v1 Gare Du Nord !",options=[
    create_option("versus","Affronter qui ?",6,required=True)
])
async def octogone(ctx,versus):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if not(os.path.exists(pathUserProfile)):
        await ctx.send("Comment veut-tu affronter quelqu'un si tu n'a pas de personnage ?\nVa donc faire un tour vers /start",delete_after=15)
        return 0

    if os.path.exists(absPath + "/userProfile/" + str(versus.id) + ".prof"):
        await fight(bot,[loadCharFile(pathUserProfile)],[loadCharFile(absPath + "/userProfile/" + str(versus.id) + ".prof")],ctx,auto=False,octogone=True)

    elif versus.id in [623211750832996354,769999212422234122]:
        temp = loadCharFile(pathUserProfile)
        tempi = tablAllAllies[0]
        tempi.changeLevel(temp.level)
        await fight(bot,[temp],[tempi],ctx,auto=False,octogone=True)
    
    else:
        await ctx.send("La personne que tu as désigné ne possède pas de personnage désolé",delete_after=15)

# team fight
@slash.subcommand(base="fight",subcommand_group="octogone",name="team",description="Affrontez l'équipe de quelqu'un avec la votre",options=[
    create_option("versus","Affronter qui ?",6,required=True)
])
async def teamFight(ctx,versus):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if not(os.path.exists(pathUserProfile)):
        await ctx.send("Vous ne possédez pas de personnage.\nAllez donc faire un tour vers /start",delete_after=15)
        return 0
    user = loadCharFile(pathUserProfile)
    team1 = []
    if user.team != 0:
        file = readSaveFiles(absPath + "/userTeams/" + str(user.team) + ".team")
        for a in file[0]:
            team1 += [loadCharFile(absPath + "/userProfile/" + a + ".prof")]
    else:
        team1 = [user]

    team2 = []
    pathOctogonedProfile = absPath + "/userProfile/" + str(versus.id) + ".prof"
    if not(os.path.exists(pathOctogonedProfile)) and versus.id not in [623211750832996354,769999212422234122]:
        await ctx.send("L'utilisateur désigné ne possède pas de personnage",delete_after=15)
        return 0

    if versus.id not in [623211750832996354,769999212422234122]:
        octogoned = loadCharFile(pathOctogonedProfile,ctx)
        if octogoned.team != 0:
            file = readSaveFiles(absPath + "/userTeams/" + str(octogoned.team) + ".team")
            for a in file[0]:
                team2 += [loadCharFile(absPath + "/userProfile/" + a + ".prof")]
        else:
            team2 = [octogoned]
    else:
        tablLenaTeam = ["Lena","Gwendoline","Shushi","Clémence","Alice","Félicité","Hélène","Iliana"]
        for a in tablLenaTeam:
            alea = copy.deepcopy(findAllie(a))
            alea.changeLevel(55)
            team2.append(alea)

    await fight(bot,team1,team2,ctx,False,octogone=True)

# -------------------------------------------- COOLDOWN --------------------------------------------
@slash.slash(name="cooldowns",description="Vous donne les cooldowns des commandes /fight et /quickFight pour votre équipe")
async def cooldowns(ctx):
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile)
        cd = teamWinDB.getFightCooldown(user.team)
        cd2 = teamWinDB.getFightCooldown(user.team,True)
        fcooldown,fseconds,fqcooldown,fqseconds,faccord,fqaccord,fsaccord,fqsaccord = cd//60,cd%60,cd2//60,cd2%60,"","","",""
        if fcooldown > 1:
            faccord = "s"
        if fqcooldown > 1:
            fqaccord = "s"
        if fseconds > 1:
            fsaccord = "s"
        if fqseconds > 1:
            fqsaccord = "s"

        fightingStatus = teamWinDB.isFightingBool(int(user.team))

        if fightingStatus[0]:
            channel = await bot.fetch_channel(fightingStatus[2])
            fightingMessage = await channel.fetch_message(fightingStatus[0])
            
            fightingRespond = "__Votre équipe affronte actuellement :__\n"
            temp = ""
            for letter in fightingStatus[1]:
                if letter==";" and len(temp) > 0:
                    ennemi = findEnnemi(temp)
                    if ennemi == None:
                        ennemi = findAllie(temp)
                    if ennemi != None:
                        fightingRespond += "{0} {1}\n".format(ennemi.icon,ennemi.name)
                    else:
                        fightingRespond += "<:blocked:897631107602841600> L'ennemi n'a pas pu être trouvé\n"
                    temp = ""
                else:
                    temp+=letter

            msg = await ctx.send(embed = discord.Embed(title="__/cooldowns__",color=user.color,description=fightingRespond+"\nsur __[{0}]({1})__".format(channel.guild.name,fightingMessage.jump_url)),delete_after=15)
        else:
            await ctx.send(embed= discord.Embed(title="__Cooldowns des commandes Fight l'équipe :__",description=f"__Normal__ : {fcooldown} minute{faccord} et {fseconds} seconde{fsaccord}\n__Quick__ : {fqcooldown} minute{fqaccord} et {fqseconds} seconde{fqsaccord}"),delete_after=10)

# -------------------------------------------- PATCHNOTE --------------------------------------------
@slash.slash(name="patchnote",description="Renvoie le dernier patchnote du bot")
async def patchnote(ctx):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    await send_patchnote(ctx)

# -------------------------------------------- ROLL --------------------------------------------
@slash.slash(name="roll",description="Permet de lancer un dé",options=[
    create_option(name="min",description="Minimum du jet. Par défaut, 1",option_type=4,required=False),
    create_option(name="max",description="Minimum du jet. Par défaut, 100",option_type=4,required=False),
])
async def roll(ctx,min=1,max=100):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    rollmes = rollMessage[random.randint(0,len(rollMessage)-1)]
    await ctx.send(embed= discord.Embed(title=f"🎲 roll {min} - {max}",color=light_blue,description=rollmes.format(random.randint(min,max))))

# -------------------------------------------- SHOP --------------------------------------------
@slash.slash(name="shop",description="Vous permet d'entrer dans le magasin")
async def shopSlash(ctx):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    await shop2(bot,ctx,shopping.shopping)

# -------------------------------------------- INVENTORY --------------------------------------------
@slash.slash(name="inventory",description="Vous permet de naviger dans votre inventaire",options=[
    create_option("destination","Dans quel inventaire voulez-vous aller ?",3,required=False,choices=[
        create_choice("Equipement","Equipement"),
        create_choice("Arme","Arme"),
        create_choice("Compétences","Compétences"),
        create_choice("Objets spéciaux","Objets spéciaux"),
        create_choice("Elements","Elements")
    ]),
    create_option("procuration","De qui voulez vous consulter l'inventaire ?",6,required=False),
    create_option("nom","Le nom ou l'identifiant d'un objet. Les espaces peuvent être remplacés par des _",3,required=False)
])
async def invent2(ctx,destination="Equipement",procuration=None,nom=None):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    for a in range(5):
        if ["Equipement","Arme","Compétences","Objets spéciaux","Elements"][a] == destination:
            destination = a
            break

    if procuration != None:
        user = loadCharFile(absPath + "/userProfile/" + str(procuration.id) + ".prof")
    else:
        user = loadCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof")

    if nom != None:
        nom = nom.replace("_"," ")
        nom = remove_accents(nom.lower())
        while nom.endswith(" "):
            nom = nom[0:-1]

        if whatIsThat(nom) == None:
            research = weapons[:]+skills[:]+stuffs[:]+others[:]+[token]
            lastResarch = []
            nameTempCmpt,lenName = 0, len(nom)
            while 1:
                lastResarch = research[:]
                if nameTempCmpt+1 <= lenName:
                    nameTempCmpt += 1
                else:
                    nameTempCmpt = lenName

                for a in research[:]:
                    temp = remove_accents(a.name.lower())
                    if nom[0:nameTempCmpt] not in temp:
                        research.remove(a)

                leni = len(research)
                if leni == 1:
                    nom = research[0].name
                    break
                elif leni <= 0 or nameTempCmpt == lenName:
                    desc = ""
                    options = []
                    for a in lastResarch:
                        have = ""
                        if not(user.have(a)):
                            have = "`"
                        desc += "{0} {2}{1}{2}\n".format(a.emoji,a.name,have)
                        options += [create_select_option(unhyperlink(a.name),a.name,getEmojiObject(a.emoji))]

                    if len(options) <= 25:
                        select = create_select(options,placeholder="Sélectionnez un objet :")
                    else:
                        await ctx.send(embed=discord.Embed(title="/inventory",description="L'objet spécifié n'a pas été trouvé, et le nom donné est trop vague\nVeuillez réessayer avec un paramètre Nom plus précis"),delete_after=10)
                        to = True
                        break
                    msg = await ctx.send(embed=discord.Embed(title="/inventory",color=light_blue,description="L'objet spécifié n'a pas été trouvé. Voici une liste des résultats les plus proches :\n\n"+desc),components=[create_actionrow(select)])

                    def check(m):
                        return m.author_id == ctx.author.id and m.origin_message.id == msg.id

                    try:
                        respond = await wait_for_component(bot,components=select,check=check,timeout=60)
                    except:
                        await msg.delete()
                        to = True
                        break

                    nom = respond.values[0]
                    await msg.edit(embed=discord.Embed(title="/inventory",color=light_blue,description="L'objet spécifié n'a pas été trouvé. Voici une liste des résultats les plus proches :\n\n"+desc),components=[create_actionrow(getChoisenSelect(select,respond.values[0]))])
                    break

        if nom == token.name:
            obj = token
            repEmb = infoOther(obj,user)
            try:
                await ctx.send(embed = repEmb,components=[])
            except:
                await ctx.channel.send(embed = repEmb,components=[])
            return 0

        nom = [nom,None]

    else:
        nom = [None]

    if nom != [None]:
        await inventory(bot,ctx,nom[0],procur=user.owner)
    else:
        await inventoryV2(bot,ctx,destination,user)

# -------------------------------------------- POINTS --------------------------------------------
@slash.slash(name="points",description="Vous permet de répartir vos points bonus",options=[
    create_option("procuration","De qui voulez vous consulter l'inventaire ?",6,required=False)
])
async def pts(ctx,procuration=None):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    await points(bot,ctx, ["/points",None],procuration,slashed=True)

# -------------------------------------------- TEAM --------------------------------------------
# team view
@slash.subcommand(base="team",name="view",description="Permet de voir les équipements de votre équipe ou de celle de quelqu'un d'autre",options=[
    create_option("joueur","Voir l'équipe d'un autre joueur",6,required=False)
])
async def teamView(ctx,joueur=None):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    if joueur==None:
        pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    else:
        pathUserProfile = absPath + "/userProfile/" + str(joueur.id) + ".prof"

    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile)
        pathTeam = absPath + "/userTeams/" + str(user.team) +".team"
        msg = await loadingSlashEmbed(ctx)
        if user.team == 0:
            if int(user.owner) == int(ctx.author.id):
                await msg.edit(embed = discord.Embed(title = "/team view",color = user.color,description = "Vous n'avez pas d'équipe pour le moment"))
            else:
                await msg.edit(embed = discord.Embed(title = "/team view",color = user.color,description = "{0} pas d'équipe pour le moment".format(user.name)))
        else:
            file = readSaveFiles(pathTeam)
            if len(file[0]) == 1:
                if int(user.owner) == int(ctx.author.id):
                    await msg.edit(embed = discord.Embed(title = "/team view",color = user.color,description = "Vous êtes seul dans votre équipe pour le moment"))
                else:
                    await msg.edit(embed = discord.Embed(title = "/team view",color = user.color,description = "{0} est seul dans son équipe pour le moment".format(user.name)))
            else:
                temp = ""
                for a in file[0]:
                    temp2 = loadCharFile(absPath + "/userProfile/" + a + ".prof")
                    level = str(temp2.level) + ["","<:littleStar:925860806602682369>{0}".format(temp2.stars)][temp2.stars>0]

                    ballerine = f'{aspiEmoji[temp2.aspiration]} | {elemEmojis[temp2.element]} | {temp2.weapon.emoji} | {temp2.stuff[0].emoji} {temp2.stuff[1].emoji} {temp2.stuff[2].emoji} | '
                    for b in temp2.skills:
                        if type(b)==skill:
                            ballerine+=b.emoji
                    ballerine+="\n\n"

                    icon = await getUserIcon(bot,temp2)

                    points = ""
                    if temp2.points > 0:
                        points = " *(+)*"
                    temp += f"__{icon} **{temp2.name}** ({level})__{points}\n{ballerine}"

                if int(user.owner) == int(ctx.author.id):
                    embed = discord.Embed(title = "/team view",color = user.color,description = "__Votre équipe se compose de :__\n\n"+temp)
                else:
                    embed = discord.Embed(title = "/team view",color = user.color,description = "__L'équipe de {0} se compose de :__\n\n".format(user.name)+temp)

                embed.add_field(name="<:empty:866459463568850954>\n__Résultats des derniers combats :__",value=teamWinDB.getVictoryStreakStr(user))

                await msg.edit(embed = embed)

# team add
@slash.subcommand(base="team",name="add",description="Permet de rajouter un joueur dans son équipe",options=[
    create_option("joueur","Le joueur à rajouter",6,required=True)
])
async def teamAdd(ctx,joueur):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile)

        pathTeam = absPath + "/userTeams/" + str(user.team) +".team"
        msg = await loadingSlashEmbed(ctx)

        if not(os.path.exists(pathTeam) and user.team != 0):
            rdm = str(random.randint(1,10000))
            pathTeam = absPath + "/userTeams/" + rdm +".team"
            rewriteFile(pathTeam,f"{str(user.owner)};")
            user.team = rdm
            saveCharFile(pathUserProfile,user)

        noneCap,selfAdd,temp = True,False,readSaveFiles(absPath + "/userTeams/" + str(user.team) +".team")

        if len(temp[0]) >= 8:
            noneCap = False

        if ctx.author == joueur:
            selfAdd = True

        if noneCap and not(selfAdd):
            mention = joueur
            if os.path.exists(absPath + "/userProfile/" + str(mention.id) + ".prof"):
                allReadyinTeam,allReadyInThatTeam,mate = False, False,loadCharFile(absPath + "/userProfile/" + str(mention.id) + ".prof")
                if mate.team != 0:
                    allReadyinTeam = True
                    if mate.team == user.team:
                        allReadyInThatTeam = True

                if not(allReadyinTeam):
                    await msg.edit(embed = discord.Embed(title = "/team add "+joueur.name, color = user.color, description = f"{mention.mention}, {ctx.author.mention} vous propose de rejoidre son équipe. Qu'en dites vous ?"))
                    await msg.add_reaction(emoji.check)
                    await msg.add_reaction(emoji.cross)

                    def checkisIntendedUser(reaction,user):
                        return int(user.id) == int(mention.id)

                    try:
                        reaction = await bot.wait_for("reaction_add",timeout=60,check=checkisIntendedUser)
                    except:
                        await msg.clear_reactions()
                        await msg.edit(embed = errorEmbed("/team add "+joueur.name,"La commande n'a pas pu aboutir"))

                    if str(reaction[0]) == emoji.check:
                        mate.team = user.team
                        saveCharFile(absPath + "/userProfile/" + str(mention.id) + ".prof",mate)
                        file = readSaveFiles(pathTeam)
                        file[0] += [str(mention.id)]
                        saveSaveFiles(pathTeam,file)
                        await msg.clear_reactions()
                        await msg.edit(embed = discord.Embed(title="/team add "+joueur.name,color = user.color,description = "Vous faites dorénavent parti de la même équipe"))
                
                elif allReadyInThatTeam:
                    await msg.edit(embed = errorEmbed("/team add "+joueur.name,"Ce joueur est déjà dans ton équipe"))
                elif allReadyinTeam:
                    await msg.edit(embed = errorEmbed("/team add "+joueur.name,"Ce joueur a déjà une équipe"))

            else:
                await msg.edit(embed = errorEmbed("/team add "+joueur.name,"Cet utilisateur n'a pas commencé l'aventure"))
        elif noneCap:
            await msg.edit(embed = errorEmbed("/team add "+joueur.name,"Votre équipe est déjà au complet"))
        elif selfAdd:
            await msg.edit(embed = errorEmbed("/team add "+joueur.name,"Vous voulez faire équipe avec vous-même ?"))

# team quit
@slash.subcommand(base="team",name="quit",description="Permet de quitter son équipe")
async def teamQuit(ctx):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile)
        pathTeam = absPath + "/userTeams/" + str(user.team) +".team"

    if user.team != 0:
        team = readSaveFiles(pathTeam)
        team[0].remove(str(ctx.author.id))
        user.team = 0

        saveSaveFiles(pathTeam,team)
        await ctx.send(embed = discord.Embed(title = "/team quit",color = user.color, description = "Vous avez bien quitté votre équipe"))
        saveCharFile(pathUserProfile,user)
    else:
        await ctx.send(embed = errorEmbed("/team quit","Vous n'avez aucune équipe à quitter"))

# team fact
@slash.subcommand(base="team",name="fact",description="Permet d'avoir des facts sur les membres de votre équipe")
async def teamFact(ctx):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile)
        pathTeam = absPath + "/userTeams/" + str(user.team) +".team"

    if user.team != "0":
        team = readSaveFiles(pathTeam)
        teamUser = []
        for a in team[0]:
            teamUser.append(loadCharFile(absPath + "/userProfile/" + str(a) + ".prof"))

        button = create_actionrow(create_button(ButtonStyle.grey,"Autre fact","🔄","🔄"))
        msg = None

        while 1:
            embed = await getRandomStatsEmbed(bot,teamUser,"/team fact")
            if msg == None:
                msg = await ctx.send(embed= embed,components=[button])
            else:
                await msg.edit(embed= embed,components=[button])

            try:
                await wait_for_component(bot,msg,timeout=60)
            except:
                await msg.edit(embed= embed,components=[])
                break

# -------------------------------------------- HELP --------------------------------------------
@slash.slash(name="help",description="Ouvre la page d'aide du bot")
async def helpCom(ctx):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    await helpBot(bot,ctx)

# -------------------------------------------- START --------------------------------------------
@slash.slash(name="start",description="Permet de commence l'aventure")
async def started(ctx):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    await start(bot,ctx)

# -------------------------------------------- STATS --------------------------------------------
@slash.slash(name="stats",description="Permet de voir vos statistiques ou celles d'un autre joueur",options=[
    create_option("joueur","Voir les statistiques d'un autre joueur",6,False)
])
async def statsCmd(ctx,joueur=None):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    if joueur == None:
        pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    else:
        pathUserProfile = absPath + "/userProfile/" + str(joueur.id) + ".prof"

    if os.path.exists(pathUserProfile):
        msg = await loadingSlashEmbed(ctx)
        user = loadCharFile(pathUserProfile)

        userIcon = await getUserIcon(bot,user)

        level = str(user.level)+['',"<:littleStar:925860806602682369>{0}".format(user.stars)][user.stars > 0]
        exp = [str(user.level*50-20),"MAX"][user.level == 55]
        rep = discord.Embed(title = f"__Page de statistique de {user.name} {userIcon}__",color = user.color,description = f"__Niveau :__ {level}\n__Expérience :__ {user.exp} / {exp}\n\n__Element :__ {elemEmojis[user.element]} {elemNames[user.element]}\n<:empty:866459463568850954>")

        rep.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(userIcon)["id"]))
        rep.add_field(name = "__Aspiration :__",value = aspiEmoji[user.aspiration] + " " + inspi[user.aspiration],inline = False)

        print(user.majorPoints)
        sumStatsBonus = [user.majorPoints[0],user.majorPoints[1],user.majorPoints[2],user.majorPoints[3],user.majorPoints[4],user.majorPoints[5],user.majorPoints[6],user.majorPoints[7],user.majorPoints[8],user.majorPoints[9],user.majorPoints[10],user.majorPoints[11],user.majorPoints[12],user.majorPoints[13],user.majorPoints[14]]

        for a in [user.weapon,user.stuff[0],user.stuff[1],user.stuff[2]]:
            sumStatsBonus[0] += a.strength
            sumStatsBonus[1] += a.endurance
            sumStatsBonus[2] += a.charisma
            sumStatsBonus[3] += a.agility
            sumStatsBonus[4] += a.precision
            sumStatsBonus[5] += a.intelligence
            sumStatsBonus[6] += a.magie
            sumStatsBonus[7] += a.resistance
            sumStatsBonus[8] += a.percing
            sumStatsBonus[9] += a.critical
            sumStatsBonus[10] += a.negativeHeal *-1
            sumStatsBonus[11] += a.negativeBoost *-1
            sumStatsBonus[12] += a.negativeShield *-1
            sumStatsBonus[13] += a.negativeDirect *-1
            sumStatsBonus[14] += a.negativeIndirect *-1

        for a in range(len(sumStatsBonus)):
            if sumStatsBonus[a] > 0:
                sumStatsBonus[a] = "+"+str(sumStatsBonus[a])

        rep.add_field(name = "<:empty:866459463568850954>\n__Statistiques principaux :__",value = f"Force : {user.strength} ({sumStatsBonus[0]})\nEndurance : {user.endurance} ({sumStatsBonus[1]})\nCharisme : {user.charisma} ({sumStatsBonus[2]})\nAgilité : {user.agility} ({sumStatsBonus[3]})\nPrécision : {user.precision} ({sumStatsBonus[4]})\nIntelligence : {user.intelligence} ({sumStatsBonus[5]})\nMagie : {user.magie} ({sumStatsBonus[6]})",inline= True)
        rep.add_field(name = "<:empty:866459463568850954>\n__Statistiques secondaires :__",value = f"Résistance : {user.resistance} ({sumStatsBonus[7]})\nPénétration d'Armure : {user.percing} ({sumStatsBonus[8]})\nCritique : {user.critical} ({sumStatsBonus[9]})\n\nSoins : {sumStatsBonus[10]}\nBoost et Malus : {sumStatsBonus[11]}\nArmures et Mitigation : {sumStatsBonus[12]}\nDégâts directs : {sumStatsBonus[13]}\nDégâts indirects : {sumStatsBonus[14]}\n\nLes statistiques d'actions s'ajoutent à vos statistiques quand vous réalisez l'action en question",inline = True)
        tempStuff,tempSkill = "",""
        for a in [0,1,2]:
            tempStuff += f"{ user.stuff[a].emoji} {user.stuff[a].name}\n"

        for a in [0,1,2,3,4]:
            try:
                tempSkill += f"{ user.skills[a].emoji} {user.skills[a].name}\n"
            except:
                tempSkill += f"Slot [{a+1}] : Pas de compétence équipée\n"

        rep.add_field(name = "<:empty:866459463568850954>\n__Equipement :__",value = f"__Arme :__\n{ user.weapon.emoji} {user.weapon.name}\n\n__Vêtements :__\n{tempStuff}\n__Compétences :__\n{tempSkill}",inline = False)
        await msg.edit(embed = rep)

    else:
        if joueur == None:
            await ctx.send("Tu n'a pas commencé l'aventure")
        else:
            await ctx.send("{0} n'a pas commencé l'aventure".format(joueur.name))

# -------------------------------------------- MANUEL --------------------------------------------
@slash.slash(name="manuel",description="Permet de consulter le manuel de l'Aventure",options=[
    create_option("page","Spécifiez une page à laquelle ouvrir le manuel",4,False)
])
async def manuel(ctx,page=0):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    msg,manPage,chapterInt,ini = await loadingSlashEmbed(ctx),page,0,True
    def checkReaction(reaction, user):
        return int(reaction.message.id) == int(msg.id) and int(user.id) == int(ctx.author.id) and (str(reaction) == emoji.backward_arrow or str(reaction) == emoji.forward_arrow or str(reaction) == '⏪' or str(reaction) == '⏩') 
    
    while 1:
        if manPage < lenChapter[chapterInt]:
            chapterInt-=1
        elif chapterInt != len(lenChapter)-1:
            if manPage >= lenChapter[chapterInt+1]:
                chapterInt+=1

        ballerine = discord.Embed(title = "__"+tablPage[manPage][0]+" :__",color = light_blue,description = tablPage[manPage][1]).set_footer(text=f"Page {manPage} / {len(tablPage)-1}")
        
        if len(tablPage[manPage]) == 3:
            ballerine.set_image(url=tablPage[manPage][2])

        await msg.edit(embed = ballerine)
        if ini:
            await msg.add_reaction('⏪')
            await msg.add_reaction(emoji.backward_arrow)
            await msg.add_reaction(emoji.forward_arrow)
            await msg.add_reaction('⏩')
            ini = False

        reaction = None
        try:
            reaction = await bot.wait_for("reaction_add",timeout=380,check=checkReaction)
        except:
            await msg.clear_reactions()
            break

        if reaction != None:
            if str(reaction[0]) == emoji.backward_arrow:
                if manPage == 0:
                    manPage = len(tablPage)-1
                else:
                    manPage -= 1                   

            elif str(reaction[0]) == emoji.forward_arrow:
                if manPage == len(tablPage)-1:
                    manPage = 0
                else:
                    manPage += 1

            elif str(reaction[0]) == '⏪':
                if chapterInt==0:
                    manPage = lenChapter[len(lenChapter)-1]
                else:
                    manPage = lenChapter[chapterInt]
            
            elif str(reaction[0]) == '⏩':
                if chapterInt==len(lenChapter)-1:
                    manPage = 0
                else:
                    manPage = lenChapter[chapterInt+1]

            await msg.remove_reaction(str(reaction[0]),reaction[1])

# -------------------------------------------- SEE LOGS --------------------------------------------
@slash.subcommand(base="see",name="FightLogs",description="Permet de consulter les logs des combats du jour",guild_ids=[615257372218097691])
async def seeLogs(ctx):
    listLogs = os.listdir("./data/fightLogs/")
    listLogs.sort(key=lambda name: name[-8:])

    page = 0
    maxPage = len(listLogs) // 24
    msg = None
    while 1:
        desc = "__Page **{0}** / {1} :__\n".format(page+1,maxPage+1)
        option = []
        maxi = min(len(listLogs),(page+1)*24)
        for log in listLogs[page*24:maxi]:
            desc += "> - {0}\n".format(log)
            option.append(create_select_option(log,log))

        embed = discord.Embed(title="__Logs des combats du jour__",color=light_blue,description=desc)

        if len(option) > 0:
            select = create_select(option)
        else:
            select = create_select([create_select_option("disabled","0")],placeholder="Il n'y a aucun logs à afficher",disabled=True)

        if page != 0:
            previousBoutton = create_button(ButtonStyle(2),"Page précédente",emoji.backward_arrow,"back")
        else:
            previousBoutton = create_button(ButtonStyle(2),"Page précédente",emoji.backward_arrow,"back",disabled=True)
        if page != maxPage:
            nextBoutton = create_button(ButtonStyle(2),"Page suivante",emoji.forward_arrow,"forward")
        else:
            nextBoutton = create_button(ButtonStyle(2),"Page suivante",emoji.forward_arrow,"forward",disabled=True)

        buttons = create_actionrow(previousBoutton,nextBoutton)

        if msg == None:
            try:
                msg = await ctx.send(embed=embed,components=[create_actionrow(select),buttons])
            except:
                msg = await ctx.channel.send(embed=embed,components=[create_actionrow(select),buttons])
        else:
            await msg.edit(embed=embed,components=[create_actionrow(select),buttons])

        try:
            respond = await wait_for_component(bot,msg,timeout=180)
        except:
            break
        
        try:
            resp = respond.values[0]
        except:
            resp = respond.custom_id
        if resp not in ["back","forward"]:
            opened = open("./data/fightLogs/{0}".format(resp),"rb")
            try:
                await respond.send("Voici les logs du combat :",file=discord.File(fp=opened))
            except:
                await ctx.channel.send("Voici les logs du combat :",file=discord.File(fp=opened))
            opened.close()
        elif resp == "back":
            page -= 1
        elif resp == "forward":
            page += 1

# -------------------------------------------- SEE STUFF --------------------------------------------
@slash.subcommand(base="see",name="StuffRepartition",description="Permet de consulter la réportation des logs",guild_ids=[615257372218097691])
async def seeStuffRepartition(ctx):
    rep = "=============================================="
    temp = copy.deepcopy(stuffs)
    temp.sort(key=lambda ballerine: ballerine.minLvl)
    allreadySeenLvl = []
    for a in temp:
        if a.minLvl not in allreadySeenLvl:
            allreadySeenLvl.append(a.minLvl)
            rep += "\n__Stuff de niveau {0} :__\n\n".format(a.minLvl)
        rep += "{0} {1}\n".format(a.emoji,a.name)

    temp = ""
    temp2 = ""
    for a in rep:
        if a == "\n":
            if len(temp2+temp) > 2000:
                await ctx.channel.send(temp2)
                temp2 = ""
                temp = ""
            else:
                temp2 += temp+a
                temp = ""
        else:
            temp += a
    await ctx.channel.send(temp2)

# -------------------------------------------- CHOOSE --------------------------------------------
@slash.slash(name="Choose",description="Renvoie une élément aléatoire de la liste donnée",options=[
    create_option("choix1",description="Le premier élément de la liste",option_type=discord_slash.SlashCommandOptionType.STRING,required=True),
    create_option("choix2",description="Le second élément de la liste",option_type=discord_slash.SlashCommandOptionType.STRING,required=True),
    create_option("choix3",description="Un potentiel troisième de la liste",option_type=discord_slash.SlashCommandOptionType.STRING,required=False),
    create_option("choix4",description="Un potentiel quatrième de la liste",option_type=discord_slash.SlashCommandOptionType.STRING,required=False),
    create_option("choix5",description="Un potentiel cinquième de la liste",option_type=discord_slash.SlashCommandOptionType.STRING,required=False)
])
async def chooseCmd(ctx,choix1,choix2,choix3=None,choix4=None,choix5=None):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    tempTabl = [choix1,choix2]
    for a in [choix3,choix4,choix5]:
        if a != None:
            tempTabl.append(a)

    selected = tempTabl[random.randint(0,len(tempTabl)-1)]
    while selected.endswith(" "):
        selected = selected[:-1]
    while selected.startswith(" "):
        selected = selected[1:]
    await ctx.send(embed=discord.Embed(title="/choose",color=light_blue,description="{0} :\n__{1}__".format(randChooseMsg[random.randint(0,len(randChooseMsg)-1)],selected)))

# -------------------------------------------- ADMIN --------------------------------------------
if isLenapy:
    adminServ = [912137828614426704]
else:
    adminServ = [927195778013859902]

@slash.subcommand(base="admin",name="enable_Fight",guild_ids=adminServ,description="Permet d'activer les combats ou non",options=[
    create_option("valeur","Activer ou désaciver les combats", SlashCommandOptionType.BOOLEAN,False)
])
async def addEnableFight(ctx,valeur = None):
    globalVar.changeFightEnabled(valeur)
    if valeur == None:
        valeur = globalVar.fightEnabled()

    if not(valeur):
        await bot.change_presence(status=discord.Status.dnd,activity=discord.Game(name="Les combats sont actuellements désactivés"))
    else:
        ballerine = datetime.datetime.now() + horaire + datetime.timedelta(hours=1)
        while ballerine.hour%3 != 0:
            ballerine = ballerine + datetime.timedelta(hours=1)

        await bot.change_presence(status=discord.Status.online,activity=discord.Game(name="Prochain shop à "+ballerine.strftime('%Hh')))

    await ctx.send(embed=discord.Embed(title="__Admin Enable Fight__",description="Les combats sont désormais __{0}__".format(["désactivés","activés"][int(valeur)]),color=[red,light_blue][int(valeur)]))

@slash.subcommand(base="admin",name="restart_Bot",guild_ids=adminServ,description="Permet de redémarrer le bot lorsque tous les combats seront fini")
async def restartCommand(ctx):
    await restart_program(bot,ctx)

@slash.subcommand(base="admin",subcommand_group="emoji",name="reset_all",guild_ids=adminServ,description="Lance une rénitialisation des emojis")
async def resetCustomEmoji(ctx):
    msg = await ctx.send(embed = discord.Embed(title="Rénitialisation des emojis..."))
    await bot.change_presence(status=discord.Status.idle,activity=discord.Game(name="rénitialiser les emojis..."))
    
    async def refresh(text : str):
        await msg.edit(embed = discord.Embed(title="Rénitialisation des emojis...",description=text))

    await refresh("Suppression des dossiers images...")
    path = "./data/images"
    for a in os.listdir(path):
        for b in os.listdir(path+"/"+a):
            os.remove(path+"/"+a+"/"+b)
            print(f"{path}/{a}/{b} supprimé")
        os.rmdir(path+"/"+a)
        print(f"{path}/{a} supprimé")

    os.rmdir("./data/images")
    print(f"{path} supprimé")
    await refresh("Suppression de la base de données")
    try:
        customIconDB.dropCustomDB()
    except:
        pass
    await refresh("Supression des emojis")
    iconGuildList = []
    if os.path.exists("../Kawi/"):
        iconGuildList = ShushyCustomIcons
    else:
        iconGuildList = LenaCustomIcons

    allEmojisNum = 0
    for a in iconGuildList:
        emojiGuild = await bot.fetch_guild(a)
        allEmojisNum += len(emojiGuild.emojis)

    cmpt = 0
    now = datetime.datetime.now().second
    lastTime = copy.deepcopy(now)
    for a in iconGuildList:
        emojiGuild = await bot.fetch_guild(a)

        for b in emojiGuild.emojis:
            try:
                print("Emoji {0} supprimé".format(b.name))
            except:
                pass
            await b.delete()
            cmpt += 1

            if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
                await refresh("Supression des emojis ({0} %)".format(int(cmpt/allEmojisNum*100)))
                lastTime = now

    await refresh("Création des dossiers...")
    existDir(absPath + "/data/images/")
    existDir(absPath + "/data/images/headgears/")
    existDir(absPath + "/data/images/weapons/")
    existDir(absPath + "/data/images/char_icons/")
    existDir(absPath + "/data/images/elemIcon/")
    await refresh("Création de la base de donnée")
    base = open("./data/database/custom_icon.db","w")
    base.close()
    customIconDB.remarkeCustomDB()
    await downloadAllHeadGearPng(bot,msg,lastTime)
    await downloadAllWeapPng(bot,msg,lastTime)
    await refresh("Téléchargements des icones de bases...")
    await downloadAllIconPng(bot)
    await downloadElementIcon(bot)

    allChar = os.listdir("./userProfile/")
    lenAllChar = len(allChar)
    cmpt = 0

    await refresh("Création des émojis...")
    for num in allChar:
        user = loadCharFile("./userProfile/"+num)
        await getUserIcon(bot,user)
        cmpt += 1

        if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
            await refresh("Création des émojis ({0} %)".format(int(cmpt/lenAllChar*100)))
            lastTime = now

    await refresh("Fini !")
    await ctx.channel.send("La rénitialisation des emojis est terminées !",delete_after=10)

    ballerine = datetime.datetime.now() + horaire + datetime.timedelta(hours=1)
    while ballerine.hour%3 != 0:
        ballerine = ballerine + datetime.timedelta(hours=1)

    await bot.change_presence(status=discord.Status.online,activity=discord.Game(name="Prochain shop à "+ballerine.strftime('%Hh')))

@slash.subcommand(base="admin",subcommand_group="emoji",name="remake_all",guild_ids=adminServ,description="Supprime puis refait tous les emojis de personnage")
async def remakeCustomEmoji(ctx):
    await remakeEmojis(ctx)

@slash.subcommand(base="admin",subcommand_group="backup",name="new",description="Permet de réaliser un backup des profiles de personnages",guild_ids=adminServ)
async def adminBackup(ctx):
    temp = create_backup()
    try:
        await ctx.send(embed=discord.Embed(title="__Admin : Backups__",color=light_blue,description=temp))
    except:
        await ctx.channel.send(embed=discord.Embed(title="__Admin : Backups__",color=light_blue,description=temp))

if isLenapy:
    tabl=[912137828614426704,405331357112205326]
else:
    tabl=adminServ

# -------------------------------------------- KIKIMETER --------------------------------------------
@slash.slash(name="Kikimeter",description="Permet de voir le top 5 de chaques catégories",guild_ids=tabl,options=[create_option(name="what",description="Que regarder",option_type=str,required=True,choices=[create_choice("total","total"),create_choice("max","max")])])
async def kikimeterCmd(ctx,what):
    listAllChars = []
    for text in os.listdir("./userProfile/"):
        listAllChars.append(loadCharFile("./userProfile/" + text))

    for cmpt in range(len(listAllChars)):
        temp = aliceStatsDb.getUserStats(listAllChars[cmpt],"all")
        listAllChars[cmpt] = {"char":listAllChars[cmpt],"{what}Damage".format(what=what):temp["{what}Damage".format(what=what)],"{what}Kill".format(what=what):temp["{what}Kill".format(what=what)],"{what}Resu".format(what=what):temp["{what}Resu".format(what=what)],"{what}RecivedDamage".format(what=what):temp["{what}RecivedDamage".format(what=what)],"{what}Heal".format(what=what):temp["{what}Heal".format(what=what)],"{what}Armor".format(what=what):temp["{what}Armor".format(what=what)],"{what}Supp".format(what=what):temp["{what}Supp".format(what=what)]}
    
    embed = discord.Embed(title="__Kikimeter__",description="=========================================================")
    for cat in ["{what}Damage".format(what=what),"{what}Kill".format(what=what),"{what}Resu".format(what=what),"{what}RecivedDamage".format(what=what),"{what}Heal".format(what=what),"{what}Armor".format(what=what),"{what}Supp".format(what=what)]:
        listAllChars.sort(key=lambda character: character["{0}".format(cat)],reverse=True)
        desc = ""

        for cmpt in range(min(5,len(listAllChars)-1)):
            if listAllChars[cmpt]["{0}".format(cat)] > 0:
                desc += "{0} - {1} {2} ({3})\n".format(cmpt+1,await getUserIcon(bot,listAllChars[cmpt]["char"]),listAllChars[cmpt]["char"].name,separeUnit(int(listAllChars[cmpt]["{0}".format(cat)])))

        if desc != "":
            embed.add_field(name="<:empty:866459463568850954>\n__{0}__".format(cat),value=desc)
    try:
        await ctx.send(embed = embed)
    except:
        await ctx.channel.send(embed = embed)

# -------------------------------------------- PROCURATION --------------------------------------------
@slash.slash(name="procuration",description="Permet de donner à un autre utilisateur procuration sur votre inventaire",options=[create_option("utilisateur","L'utilisateur qui pourra modifier vos objets équipés",6,True)])
async def procurCmd(ctx,utilisateur):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    await procuration(ctx,utilisateur)

# -------------------------------------------- ICON --------------------------------------------
@slash.slash(name="icon",description="Renvoie l'icone de votre personnage",options=[create_option("utilisateur","Voir l'icone d'un autre utilisateur",6,False)])
async def iconCommand(ctx,utilisateur=None):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    try:
        if utilisateur == None:
            user = loadCharFile("./userProfile/{0}.prof".format(ctx.author_id))
        else:
            user = loadCharFile("./userProfile/{0}.prof".format(utilisateur.id))
    except:
        if utilisateur == None:
            await ctx.send("Vous devez avoir commencé l'Aventure pour utiliser cette commande\nFaites donc un tour du côté de /start !",delete_after=15)
        else:
            await ctx.send("La personne mentionnée n'a pas commencé l'aventure",delete_after=15)
        return 0

    embed = discord.Embed(title="__Icone de personnage__",color=user.color)
    embed.set_image(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(await getUserIcon(bot,user))["id"]))

    await ctx.send(embed=embed)

# -------------------------------------------- ADVENTURE ---------------------------------------------
@slash.subcommand(base="adventure",subcommand_group="duty",name="select",description="Permet de commencer une nouvelle mission",base_description="Commandes de l'Aventure",guild_ids=[615257372218097691])
async def dutyStart(ctx):
    still = True
    try:
        user = loadCharFile("./userProfile/{0}.prof".format(ctx.author.id))
    except:
        still = False
        await ctx.send(embed=discord.Embed(title="__Commande de l'Aventure :__",description="Vous devez avoir commencé l'aventure pour utiliser cette commande.\n\nFaites donc un tour vers /start"),delete_after=15)
    
    if still:
        actName, dutyName, msg = await adventureDutySelect(bot,ctx,user)
        await msg.edit(embed = discord.Embed(title="__Mission sélectionnée__",color=light_blue,description="Vous avez sélectioné la mission \"{0} - {1}\"".format(actName,dutyName[0].upper()+dutyName[1:].lower())),components=[])

# -------------------------------------------- ROULETTE --------------------------------------------
@slash.slash(name="roulette",description="Permet d'utiliser un Jeton de roulette pour obtenir un objet ou des pièces")
async def rouletteSlash(ctx):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    try:
        user = loadCharFile("./userProfile/{0}.prof".format(ctx.author_id))
    except:
        await ctx.send(embed=discord.Embed(title="__Commande de l'Aventure :__",description="Vous devez avoir commencé l'aventure pour utiliser cette commande.\n\nFaites donc un tour vers /start"),delete_after=15)
        return 0

    await roulette(bot, ctx, user)

# -------------------------------------------- SEE ENEMY REPARTITION -------------------------------
@slash.subcommand(base="see",name="enemyRepartition",guild_ids=[615257372218097691],description="Permet de voir la répartition des ennemis")
async def seeEnnemyRep(ctx):
    octoRolesNPos = [[[],[],[]],[[],[],[]],[[],[],[]]] # 0 : Dmg; 1 : Heal/Armor; 2 : Buff/Debuff
    dicidants = []

    for octa in tablUniqueEnnemies:
        if octa.aspiration in [BERSERK, POIDS_PLUME, MAGE, ENCHANTEUR, OBSERVATEUR, TETE_BRULE]:
            roleId = 0
        elif octa.aspiration in [ALTRUISTE, PREVOYANT]:
            roleId = 1
        elif octa.aspiration in [IDOLE, PROTECTEUR]:
            roleId = 2
        else:
            dicidants.append(octa)
            roleId = -1

        if roleId != -1:
            octoRolesNPos[roleId][octa.weapon.range].append(octa)

    for cmpt in (0,1,2):
        embed = discord.Embed(title="__Ennemi répartion : {0}__".format(["DPT_PHYS","Healer/Shilder","Support"][cmpt]),color=light_blue)
        for cmptBis in range(len(octoRolesNPos[cmpt])):
            desc = ""
            for name in octoRolesNPos[cmpt][cmptBis]:
                desc += "{0} {1}\n".format(name.icon,name.name)
            if len(desc) > 0:
                embed.add_field(name=["__Mêlée :__","__Distance :__","__Backline :__"][cmptBis],value=desc,inline=True)
            else:
                embed.add_field(name=["__Mêlée :__","__Distance :__","__Backline :__"][cmptBis],value="`-`",inline=True)


        if cmpt == 0:
            await ctx.send(embed = embed)
        else:
            await ctx.channel.send(embed = embed)

    desc = ''
    for name in dicidants:
        desc += "{0} {1}\n".format(name.icon,name.name)
    embed = discord.Embed(title="__Hors catégorie :__".format(["DPT_PHYS","Healer/Shilder","Support"][cmpt]),color=light_blue,description=desc)

    await ctx.channel.send(embed = embed)

# ------------------------------------------- PRESTIGE ---------------------------------------------
@slash.slash(name="prestige",description="Permet de revenir au niveau 1, avec quelques bonus en primes")
async def prestigeCmd(ctx):
    if not(await botChannelVerif(bot,ctx)):
        return 0
    try:
        user = loadCharFile("./userProfile/{0}.prof".format(ctx.author.id))
    except:
        await ctx.send("Vous n'avez même pas encore commencé l'aventure et vous voulez déjà prestige ?",delete_after=15)
        return 0

    if user.level < 55:
        await ctx.send("Vous devez être niveau 55 pour pouvoir utiliser cette commande",delete_after=15)
        return 0

    embed = discord.Embed(title="__Prestige__",color=light_blue,description="En prestigeant votre personnage, vous retournerez au niveau 1<:littleStar:925860806602682369>{0}.\n\nVous conserverez votre inventaire d'objet des de compétences et obtiendrez un __Point Majeur__.\nVous pourrez l'utiliser pour augmenter une de vos statistiques principales de 30 points supplémentaires, ou augmenter vos statistiques secondaires de 10 points".format(user.stars+1))
    comfirm = create_button(ButtonStyle.green,"Prestige votre personnage",'✅','✅')

    msg = await ctx.send(embed=embed,components=[create_actionrow(comfirm)])

    def check(m):
        return int(m.author_id) == int(ctx.author.id)

    try:
        await wait_for_component(bot,msg,check=check,timeout=30)
    except:
        await msg.edit(embed=embed,components=[])
        return 0

    user = loadCharFile(user=user)
    user.level, user.exp, user.stars = 1,0,user.stars+1
    user = restats(user)

    saveCharFile(user=user)
    await inventoryVerif(bot,user)
    await msg.edit(embed = discord.Embed(title="__Prestige__",color=light_blue,description="Vous avez bien prestige votre personnage"),components=[])    

# ------------------------------------------- SET_BOT_CHANNEL --------------------------------------
@slash.slash(name="set_bot_channel",description="Permet de définir un salon comme salon bot",options=[create_option("salon","Le salon dans lequel les utilisateurs pourront utiliser les commandes",7,True)])
async def setChannel(ctx:discord_slash.SlashContext, salon:discord.TextChannel):
    if not(ctx.author.guild_permissions.manage_channels):
        await ctx.send(embed = discord.Embed(title="__/set_bot_channel__",color=red,description="Tu as besoin des permissions de gérer les salons textuels pour utiliser cette commande, désolée"),delete_after=10)
        return 0
    if type(salon) != discord.TextChannel:
        await ctx.send(embed = discord.Embed(title="__/set_bot_channel__",color=red,description="Seul un salon textuel peut être rajouté comme salon bot, désolée"),delete_after=10)
        return 0

    globalVar.setGuildBotChannel(ctx.guild_id,salon.id)
    await ctx.send(embed = discord.Embed(title="__/set_bot_channel__",color=light_blue,description="Le salon {0} a bien été enregistré comme salon bot\nChaque serveur ne peut avoir qu'un seul salon bot, réutiliser la commande remplacera l'ancien".format(salon.mention)))


@slash.slash(name="verif_team",guild_ids=adminServ)
async def verifTeams(ctx):
    toSend, allReadySeenn, msg, userTeam = "", [], None, []

    def getUserMainTeam(user:char):
        for look in userTeam:
            if look[0] == user.owner:
                return int(look[1])

    for team in os.listdir("./userTeams/"):
        temp = "__Team **{0}** :__".format(team.replace(".team",""))
        teamMembers = readSaveFiles("./userTeams/"+team)[0]
        if len(teamMembers) == 0:
            os.remove("./userTeams/"+team)
            temp += "\n`Equipe vide. Fichier supprimé`"
        else:
            tmpTeamMembers = teamMembers[:]
            for ids in teamMembers:
                user = loadCharFile(path="./userProfile/{0}.prof".format(ids))
                if user.owner in allReadySeen:
                    warn = "~~"
                    if getUserMainTeam(user) != int(team.replace(".team","")):
                        tmpTeamMembers.remove(str(user.owner))
                else:
                    warn = ""
                    allReadySeen.append(user.owner)
                    userTeam.append([user.owner,int(team.replace(".team",""))])

                if int(user.team) != int(team.replace(".team","")):
                    user.team = int(team.replace(".team",""))
                    saveCharFile(user=user)
                    redacted = " 📎"
                else:
                    redacted = ""

                temp += "\n{2}{0} {1}{2}{3}".format(await getUserIcon(bot, user), user.name, warn, redacted)


            if len(tmpTeamMembers) > 0:
                saveSaveFiles("./userTeams/"+team,[tmpTeamMembers])
            else:
                os.remove("./userTeams/"+team)
                temp += "\n`Equipe vide. Fichier supprimé`"


        temp+="\n"
        if len(toSend+temp) > 4000:
            if msg == None:
                msg = await ctx.send(embed=discord.Embed(title="__Team Vérification__",color=light_blue,description=toSend))
            else:
                await ctx.channel.send(embed=discord.Embed(title="__Team Vérification__",color=light_blue,description=toSend))
            toSend = temp
            temp = ""
        else:
            toSend = toSend + temp + "\n"

    if toSend != "":
        if msg == None:
            msg = await ctx.send(embed=discord.Embed(title="__Team Vérification__",color=light_blue,description=toSend))
        else:
            await ctx.channel.send(embed=discord.Embed(title="__Team Vérification__",color=light_blue,description=toSend))

###########################################################
# Démarrage du bot
if not(isLenapy):
    print("\nKawiiiiii")
    try:
        bot.run(shushipy)
    except:
        print("La connexion a écouché")
else:
    print("\nIl semblerait que je sois seule cette fois. Je m'occuperais de Shushi une autre fois")
    bot.run(lenapy)