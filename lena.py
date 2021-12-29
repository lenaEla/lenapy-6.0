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

existDir(absPath+"/guildSettings/")
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
ctxChannel = 0
listGuildSet = os.listdir(absPath + "/guildSettings/")
guilds = list(range(0,len(listGuildSet)))

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
            if teamWinDB.isFightingBool(int(team[:-5])):
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
            await chan.send(embed=discord.Embed(title="__Auto backup__",color=light_blue,description=delete_old_backups()))
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
    cmpt = 0
    lastTime = datetime.datetime.now().second
    lenGuild = len(listGuildSet)
    print("Starting guild's settings loading... 0%")
    while cmpt < lenGuild:
        try:
            guildSettings = readSaveFiles(absPath + "/guildSettings/"+listGuildSet[cmpt])
            guilds[cmpt] = server(int(listGuildSet[cmpt][0:-4]),guildSettings[0][0],int(guildSettings[0][1]),int(guildSettings[0][2]))
            guilds[cmpt].colorRole.enable, guilds[cmpt].colorRole.red, guilds[cmpt].colorRole.orange, guilds[cmpt].colorRole.yellow, guilds[cmpt].colorRole.green, guilds[cmpt].colorRole.lightBlue, guilds[cmpt].colorRole.blue, guilds[cmpt].colorRole.purple, guilds[cmpt].colorRole.pink = bool(int(guildSettings[1][0][1:])),int(guildSettings[1][1]),int(guildSettings[1][2]),int(guildSettings[1][3]),int(guildSettings[1][4]),int(guildSettings[1][5]),int(guildSettings[1][6]),int(guildSettings[1][7]),int(guildSettings[1][8])

            guild = await bot.fetch_guild(guilds[cmpt].id)
            guilds[cmpt].name = guild.name

        except:
            os.remove(absPath + "/guildSettings/"+listGuildSet[cmpt])

        now = datetime.datetime.now().second
        if now >= lastTime + 2 or (now <= 2 and now >= lastTime + 2 - 60):
            print("Loading guild's settings... {0}%".format(round((cmpt/lenGuild)*100)))
            lastTime = now

        cmpt += 1

    print("All guild's settings are loaded !\n")

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
    valid = False
    try:
        pathGuildSettings = absPath + "/guildSettings/"+str(ctx.guild.id)+".set"
        valid = True
    except:
        pass

    if valid:
        if not existFile(pathGuildSettings):
            tempGuild = server(ctx.guild.id)
            saveGuildSettings(pathGuildSettings, tempGuild)
            print(f"Création du fichier {pathGuildSettings} ({ctx.guild.name})")
            guilds.append(tempGuild) 
        
        guild = None

        for a in guilds:
            if type(a) != int:
                if ctx.guild.id == a.id:
                    guild = a

        if ((ctx.content.startswith(guild.prefixe) or ctx.content.startswith("l!")) and not(ctx.author.bot == True)):
            args = commandArgs(ctx)
            if args[0] == guild.prefixe + "settings" or args[0] == "l!settings":
                msg = await loadingEmbed(ctx)
                def checkIsAuthor(message):
                    return message.author.id == ctx.author.id
                    
                if ctx.author.guild_permissions.manage_channels == False:
                    await msg.edit(embed = errorEmbed(args[0],"Tu as pas les permissions nécéssaires pour réaliser cette commande désolée"))
                    
                else:
                    guildSettingsTemp = guild
                    choiceSettings = ["Salon des patchnotes","Salon bots"]
                    etat = -1
                    while etat > -10:
                        if etat == -1:
                            await msg.edit(embed = discord.Embed(title = args[0], description = choice(choiceSettings),color = light_blue))
                            respond = await bot.wait_for("message",timeout = 60,check = checkIsAuthor)

                            if not respond.content.isdigit():
                                await msg.edit(embed = errorEmbed(args[0],"Je m'attendais plutôt à un nombre à vrai dire"))
                            else:
                                repMsg = respond
                                respond = int(respond.content)
                                if not(respond < len(choiceSettings) and respond >= 0):
                                    await msg.edit(embed = errorEmbed(args[0],"Ta réponse ne correspond à aucune option"))
                                else:
                                    etat = respond

                                try:
                                    await repMsg.delete()
                                except:
                                    1

                        elif etat == 0:
                            if guild.patchnote == str(0):
                                await msg.edit(embed = discord.Embed(title = args[0]+" : Salons de patchnote",color = light_blue,description = f"Aucun salon est n'actuellement défini comme Salon de patchnotes pour le serveur {ctx.guild.name}\nVeuillez mentionner le salon que vous souhaitez définir comme tel"))
                            else:
                                await msg.edit(embed = discord.Embed(title = args[0]+" : Salons de patchnote",color = light_blue,description = f"Le salon de patchnote du serveur {ctx.guild.name} est : **__{bot.get_channel(guild.patchnote)}__**\nVeuillez mentionner le nouveau salon"))

                            newPatchnotes = await bot.wait_for("message",timeout = 60,check = checkIsAuthor)
                            try:
                                newPatchnotes = newPatchnotes.channel_mentions[0].id
                                guildSettingsTemp.patchnote = newPatchnotes
                                if saveGuildSettings(pathGuildSettings,guildSettingsTemp):
                                    await msg.edit(embed = discord.Embed(title = args[0] + " : Salon Patchnote",description ="Les nouveaux paramètres ont bien été sauvegardé"))
                                elif saveGuildSettings(pathGuildSettings,guild):
                                    await msg.edit(embed = discord.Embed(title = args[0] + " : Salon Patchnote",description ="Une erreur est survenue. L'opération est annulée"))
                                else:
                                    os.remove(pathGuildSettings)
                                    await msg.edit(embed = errorEmbed(args[0],"Une erreur est survenue. Une corruption a été détecté. Fichier supprimé"))
                            except:
                                    await msg.edit(embed = errorEmbed(args[0],"Tu ne m'a pas mentionné un salon"))
                            try:
                                await newPatchnotes.delete()
                            except:
                                1
                            etat = -10
                                    
                        elif etat == 1:
                            if guild.bot == str(0):
                                await msg.edit(embed = discord.Embed(title = args[0]+" : Salon des bots",color = light_blue,description = f"Lorsqu'un salon Bot est configuré, Lenapy ne réagira qu'aux commandes envoyé dans ce dit salon (à l'exeption des commandes de modération.\nDe plus, tous messages automatiques liés aux rappels ou à l'Aventure seront envoyé dans ce salon.\n\nAucun salon est n'actuellement défini comme Salon des bots pour le serveur {ctx.guild.name}\nVeuillez mentionner le salon que vous souhaitez définir comme tel"))
                            else:
                                await msg.edit(embed = discord.Embed(title = args[0]+" : Salon des bots",color = light_blue,description = f"Lorsqu'un salon Bot est configuré, Lenapy ne réagira qu'aux commandes envoyé dans ce dit salon (à l'exeption des commandes de modération.\nDe plus, tous messages automatiques liés aux rappels ou à l'Aventure seront envoyé dans ce salon.\n\nLe Salon des bots du serveur {ctx.guild.name} est : **__{bot.get_channel(guild.bot)}__**\nVeuillez mentionner le nouveau salon"))

                                newBotChannel = await bot.wait_for("message",timeout = 60,check = checkIsAuthor)
                                repMsg = newBotChannel
                                try:
                                    newBotChannel = newBotChannel.channel_mentions[0].id
                                    guildSettingsTemp.bot = newBotChannel
                                    if saveGuildSettings(pathGuildSettings,guildSettingsTemp):
                                        await msg.edit(embed = discord.Embed(title = args[0] + " : Salon Bot",description ="Les nouveaux paramètres ont bien été sauvegardé"))
                                    elif saveGuildSettings(pathGuildSettings,guild):
                                        await msg.edit(embed = discord.Embed(title = args[0] + " : Salon Bot",description ="Une erreur est survenue. L'opération est annulée"))
                                    else:
                                        os.remove(pathGuildSettings)
                                        await msg.edit(embed = errorEmbed(args[0],"Une erreur est survenue. Une corruption a été détecté. Fichier supprimé"))
                                except:
                                    await msg.edit(embed = errorEmbed(args[0],"Tu ne m'a pas mentionné un salon"))
                                try:
                                    await repMsg.delete()
                                except:
                                    1
                                etat = -10
                
                saveGuildSettings(pathGuildSettings,guild)

            elif args[0] == "l!admin" and ctx.author.id == 213027252953284609:
                #try:
                if args[1] == "clearRoles":
                    cmpt = 0
                    for a in ctx.guild.roles:
                        if a.name.startswith("lenapy_"):
                            try:
                                await a.delete()
                                cmpt+= 1
                            except:
                                None
                elif args[1] == "motherlode":
                    try:
                        mention = ctx.mentions[0]
                        pathUserProfile = absPath + "/userProfile/" + str(mention.id) + ".prof"
                        user = loadCharFile(pathUserProfile)
                        user.currencies = user.currencies + 50000
                        saveCharFile(pathUserProfile,user)
                        await ctx.add_reaction('<:goodPileOfCoins:918042081224716309>')
                    except:
                        await ctx.add_reaction('❌')
                elif args[1] == "forceRestat":
                    if args[2] == "all":
                        for a in os.listdir(absPath + "/userProfile/"):
                            pathUserProfile = absPath + "/userProfile/" + a
                            user = loadCharFile(pathUserProfile)
                            user = silentRestats(user)

                            saveCharFile(pathUserProfile,user)
                            print(f"{user.name} a bien été restat")

                    else:
                        try:
                            stated = ctx.mentions[0]
                            pathUserProfile = absPath + "/userProfile/" + str(stated.id) + ".prof"
                            user = loadCharFile(pathUserProfile)
                            user = restats(user)

                            if saveCharFile(pathUserProfile,user) :
                                await stated.send(embed = discord.Embed(title = f"{args[0]} {args[1]} {stated.name}",color = user.color,description = f"Votre profil a été restats de force par un administrateur.\n\nVous avez obtenus les statistiques correspondant à votre aspiration et votre niveau et vous avez récupéré vos {user.points} points bonus, que vous pouvez redistribuer à votre guise"))
                                print(f"{user.name} a bien été restat")
                        except:
                            pass                            
                elif args[1] == "give":
                    if args[2] == "all":
                        for a in os.listdir(absPath + "/userProfile/"):
                            try:
                                pathUserProfile = absPath + "/userProfile/" + a
                                user = loadCharFile(pathUserProfile)
                                whut = whatIsThat(args[3])

                                if whut == 0:
                                    weap = None
                                    for a in weapons:
                                        if args[3][0:2] == a.id:
                                            weap = a
                                    
                                    if weap != None:                                         
                                        trouv = False
                                        for a in user.weaponInventory:
                                            if a.id == args[3][0:2]:
                                                trouv = True

                                        if not(trouv):
                                            user.weaponInventory += [weap]

                                            saveCharFile(pathUserProfile,user)
                                            owner = await bot.fetch_user(user.owner)
                                            try:
                                                await owner.send(embed = discord.Embed(title = f"{args[0]} {args[1]} {args[2]}",color = user.color,description = f"Vous avez reçu l'object \"{weap.name}\" de la part d'un administrateur"))
                                                print(f"{user.name} a bien reçu sont object")
                                            except:
                                                pass

                                elif whut == 1:
                                    weap = None
                                    for a in skills:
                                        if args[3][0:2] == a.id:
                                            weap = a
                                    
                                    if weap != None:                                         
                                        trouv = False
                                        for a in user.skillInventory:
                                            if a.id == args[3][0:2]:
                                                trouv = True

                                        if not(trouv):
                                            user.skillInventory += [weap]

                                            saveCharFile(pathUserProfile,user)
                                            owner = await bot.fetch_user(user.owner)
                                            try:
                                                await owner.send(embed = discord.Embed(title = f"{args[0]} {args[1]} {args[2]}",color = user.color,description = f"Vous avez reçu l'object \"{weap.name}\" de la part d'un administrateur"))
                                                print(f"{user.name} a bien reçu sont object")
                                            except:
                                                pass

                                if whut == 2:
                                    weap = None
                                    for a in stuffs:
                                        if args[3][0:2] == a.id:
                                            weap = a
                                    
                                    if weap != None:                                         
                                        trouv = False
                                        for a in user.stuffInventory:
                                            if a.id == args[3][0:2]:
                                                trouv = True

                                        if not(trouv):
                                            user.stuffInventory += [weap]

                                            saveCharFile(pathUserProfile,user)
                                            owner = await bot.fetch_user(user.owner)
                                            try:
                                                await owner.send(embed = discord.Embed(title = f"{args[0]} {args[1]} {args[2]}",color = user.color,description = f"vous avez reçu l'object \"{weap.name}\" de la part d'un administrateur"))
                                                print(f"{user.name} a bien reçu sont object")
                                            except:
                                                pass

                                if whut == 3:
                                    weap = None
                                    for a in others:
                                        if args[3][0:2] == a.id:
                                            weap = a
                                    
                                    if weap != None:                                         
                                        trouv = False
                                        for a in user.otherInventory:
                                            if a.id == args[3][0:2]:
                                                trouv = True

                                        if not(trouv):
                                            user.otherInventory += [weap]

                                            saveCharFile(pathUserProfile,user)
                                            owner = await bot.fetch_user(user.owner)
                                            try:
                                                await owner.send(embed = discord.Embed(title = f"{args[0]} {args[1]} {args[2]}",color = user.color,description = f"vous avez reçu l'object \"{weap.name}\" de la part d'un administrateur"))
                                                print(f"{user.name} a bien reçu sont object")
                                            except:
                                                pass
                            except:
                                print("Une erreure est survenue")

                    else:
                        try:
                            pathUserProfile = absPath + "/userProfile/" + str(ctx.mentions[0].id) + ".prof"
                            user = loadCharFile(pathUserProfile)
                            whut = whatIsThat(args[3])

                            if whut == 0:
                                weap = None
                                for a in weapons:
                                    if args[3][0:2] == a.id:
                                        weap = a
                                
                                if weap != None:                                         
                                    trouv = False
                                    for a in user.weaponInventory:
                                        if a.id == args[3][0:2]:
                                            trouv = True

                                    if not(trouv):
                                        user.weaponInventory += [weap]

                                        saveCharFile(pathUserProfile,user)
                                        owner = await bot.fetch_user(user.owner)
                                        try:
                                            await owner.send(embed = discord.Embed(title = f"{args[0]} {args[1]} {owner.name}",color = user.color,description = f"vous avez reçu l'object \"{weap.name}\" de la part d'un administrateur"))
                                            print(f"{user.name} a bien reçu son object")
                                        except:
                                            pass

                            elif whut == 1:
                                weap = None
                                for a in skills:
                                    if args[3][0:2] == a.id:
                                        weap = a
                                
                                if weap != None:                                         
                                    trouv = False
                                    for a in user.skillInventory:
                                        if a.id == args[1][0:2]:
                                            trouv = True

                                    if not(trouv):
                                        user.skillInventory += [weap]

                                        saveCharFile(pathUserProfile,user)
                                        owner = await bot.fetch_user(user.owner)
                                        try:
                                            await owner.send(embed = discord.Embed(title = f"{args[0]} {args[1]} {args[2]}",color = user.color,description = f"vous avez reçu l'object \"{weap.name}\" de la part d'un administrateur"))
                                            print(f"{user.name} a bien reçu sont object")
                                        except:
                                            pass

                            if whut == 2:
                                weap = None
                                for a in stuffs:
                                    if args[3][0:2] == a.id:
                                        weap = a
                                
                                if weap != None:                                         
                                    trouv = False
                                    for a in user.stuffInventory:
                                        if a.id == args[3][0:2]:
                                            trouv = True

                                    if not(trouv):
                                        user.stuffInventory += [weap]

                                        saveCharFile(pathUserProfile,user)
                                        owner = await bot.fetch_user(user.owner)
                                        try:
                                            await owner.send(embed = discord.Embed(title = f"{args[0]} {args[1]} {args[2]}",color = user.color,description = f"vous avez reçu l'object \"{weap.name}\" de la part d'un administrateur"))
                                            print(f"{user.name} a bien reçu sont object")
                                        except:
                                            pass

                            if whut == 3:
                                weap = None
                                for a in others:
                                    if args[3][0:2] == a.id:
                                        weap = a
                                
                                if weap != None:                                         
                                    trouv = False
                                    for a in user.otherInventory:
                                        if a.id == args[3][0:2]:
                                            trouv = True

                                    if not(trouv):
                                        user.otherInventory += [weap]

                                        saveCharFile(pathUserProfile,user)
                                        owner = await bot.fetch_user(user.owner)
                                        try:
                                            await owner.send(embed = discord.Embed(title = f"{args[0]} {args[1]} {args[2]}",color = user.color,description = f"vous avez reçu l'object \"{weap.name}\" de la part d'un administrateur"))
                                            print(f"{user.name} a bien reçu sont object")
                                        except:
                                            pass
                        except:
                            print("Une erreure est survenue")
                elif args[1] == "forceEmoji":
                    await ctx.add_reaction('<:popcorn:695553322668785715>')
                    for a in os.listdir("./userProfile/"):
                        user = loadCharFile("./userProfile/"+a)
                        await makeCustomIcon(bot,user)
                elif args[1] == "forceShop":
                    await shopping.newShop()
                    await ctx.add_reaction('❄')

                #except:
                    #await ctx.add_reaction('<:LenaWhat:760884455727955978>')

            elif args[0] == "l!test" and ctx.author.id == 213027252953284609:
                test = loadAdvDutyFile("act0","prologue")
                user = loadCharFile("./userProfile/{0}.prof".format(ctx.author.id))

                toEmb = test.nextText()
                desc = toEmb.text.format(name=user.name)
                toBotton = "Réf. : {0}".format(toEmb.ref)

                embed = discord.Embed(title="__{0} - {1}__".format(test.act[0].upper()+test.act[1:],test.name[0].upper()+test.name[1:]),color=user.color,description=desc)
                embed.set_footer(text=toBotton)

                await ctx.channel.send(embed=embed)

            elif args[0] == "l!new_patch" and ctx.author.id == 213027252953284609:
                await new_patch(bot,ctx)
                for a in guilds:
                    try:
                        if type(a) != int:
                            ballerine = await bot.fetch_guild(a.id)
                            if ballerine != None:
                                guildSettings = readSaveFiles(absPath + "/guildSettings/"+str(ballerine.id)+".set")
                                babie = server(int(ballerine.id),guildSettings[0][0],int(guildSettings[0][1]),int(guildSettings[0][2]))
                                if babie.patchnote != 0:
                                    chan = await bot.fetch_channel(babie.patchnote)
                                    await chan.send(send_patchnote())
                                elif babie.bot != 0:
                                    chan = await bot.fetch_channel(babie.bot)
                                    await chan.send(embed=discord.Embed(title="/patchnote",color=light_blue,description="Un nouveau patchnote est disponible, vous pouvez le voir à l'aide de /patchnote\n\n*Note : Les nouvelles commandes slash peuvent mettre jusqu'à 1 heure pour apparaitre sur vos serveur*"))
                    except:
                        pass

        else:
            pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
            if os.path.exists(pathUserProfile) and len(ctx.content)>=3:
                try:
                    await addExpUser(bot,guild,pathUserProfile,ctx,3,3)
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
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    user = loadCharFile(pathUserProfile)
        
    await encylopedia(bot,ctx,destination,user)

# -------------------------------------------- FIGHT --------------------------------------------
# normal fight
@slash.subcommand(base="fight",name="normal",description="Permet de lancer un combat normal")
async def normal(ctx):
    if not(globalVar.fightEnabled()):
        await ctx.send(embed=discord.Embed(title="__Combats désactivés__",description="Les combats sont actuellement désactivés pour cause de bug ou de déploiment imminant d'une mise à jour\nVeuillez vous référer au status du bot pour savoir si les combats sont désactivés ou non"),delete_after=10)
    else:
        try:
            pathGuildSettings = absPath + "/guildSettings/"+str(ctx.guild.id)+".set"
            valid = True
        except:
            pass
        
        if valid:
            if not existFile(pathGuildSettings):
                tempGuild = server(ctx.guild.id)
                saveGuildSettings(pathGuildSettings, tempGuild)
                print(f"Création du fichier {pathGuildSettings} ({ctx.guild.name})")
                guilds.append(tempGuild) 
            
            guild = None

            for a in guilds:
                if type(a) != int:
                    if ctx.guild.id == a.id:
                        guild = a

        pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
        user = loadCharFile(pathUserProfile)
        ballerine,temp = 0,0
        if user.team == 0:
            ballerine = user.owner
        else:
            ballerine = user.team

        cooldownOk = True
        timing = teamWinDB.getFightCooldown(ballerine)
        if timing > 0:
            cooldownOk = False

        if cooldownOk and not(teamWinDB.isFightingBool(ballerine)):
            team1 = []
            if user.team != 0:
                file = readSaveFiles(absPath + "/userTeams/" + str(user.team) + ".team")
                for a in file[0]:
                    team1 += [loadCharFile(absPath + "/userProfile/" + a + ".prof")]
            else:
                team1 = [user]

            # Random event
            fun = random.randint(0,99)

            fightAnyway = True

            if False:        # Test
                temp = team1
                temp.sort(key=lambda overheal: overheal.level,reverse=True)
                maxLvl = temp[0].level

                team2 = []
                lenBoucle = 10
                cmpt = 0

                octoShield = findEnnemi("Octo Bouclier")
                alea = copy.deepcopy(findEnnemi("Octo Bouclier"))

                alea.changeLevel(maxLvl)

                while cmpt < lenBoucle:
                    team2.append(alea)
                    cmpt += 1

                await fight(bot,team1,team2,ctx,guild,False,slash=True)
                fightAnyway = False

            elif fun < 1:                # But nobody came
                teamIcon = ""
                for wonderfullIdea in team1:
                    teamIcon += "{0} {1}\n".format(await getUserIcon(bot,wonderfullIdea),wonderfullIdea.name)

                temp1 = discord.Embed(title = "__Résultats du combat :__",color = black,description="__Danger :__ <a:bnc:908762423111081994>\n__Nombre de tours :__ <a:bnc:908762423111081994>\n__Durée :__ <a:bnc:908762423111081994>")
                temp1.add_field(name="<:empty:866459463568850954>\n__Vainqueurs :__",value=teamIcon,inline=True)
                temp1.add_field(name="<:empty:866459463568850954>\nPerdants :",value="[[But nobody came](https://bit.ly/3wDwyF3)]",inline=True)

                await ctx.send(embed = temp1,components=[])
                fightAnyway = False

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

                await fight(bot,team1,team2,ctx,guild,False,slash=True)
                fightAnyway = False

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

                await fight(bot,team1,team2,ctx,guild,False,slash=True)
                fightAnyway = False

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

                await fight(bot,team1,team2,ctx,guild,False,slash=True)
                fightAnyway = False

            if fightAnyway:
                await fight(bot,team1,[],ctx,guild,False,slash=True)

        elif teamWinDB.isFightingBool(ballerine):
            msg = await ctx.send(embed = errorEmbed("Woopsy","Vous êtes déjà en train de vous battre"),delete_after=10)
        else:
            msg = await ctx.send(embed = errorEmbed("Cooldown",f"Votre équipe ne pourra faire de combats normaux que dans {timing//60} minute(s)"),delete_after=10)

# quick fight
@slash.subcommand(base="fight",name="quick",description="Vous permet de faire un combat en sautant directement à la fin")
async def comQuickFight(ctx):
    if not(globalVar.fightEnabled()):
        await ctx.send(embed=discord.Embed(title="__Combats désactivés__",description="Les combats sont actuellement désactivés pour cause de bug ou de déploiment imminant d'une mise à jour\nVeuillez vous référer au status du bot pour savoir si les combats sont désactivés ou non"),delete_after=10)
    else:
        try:
            pathGuildSettings = absPath + "/guildSettings/"+str(ctx.guild.id)+".set"
            valid = True
        except:
            valid = False
        
        if valid:
            if not existFile(pathGuildSettings):
                tempGuild = server(ctx.guild.id)
                saveGuildSettings(pathGuildSettings, tempGuild)
                print(f"Création du fichier {pathGuildSettings} ({ctx.guild.name})")
                guilds.append(tempGuild) 
            
            guild = None

            for a in guilds:
                if type(a) != int:
                    if ctx.guild.id == a.id:
                        guild = a

        pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
        user = loadCharFile(pathUserProfile)
        ballerine,trouv,temp = 0,False,0
        if user.team == 0:
            ballerine = user.owner
        else:
            ballerine = user.team

        cooldownOk = True
        timing = teamWinDB.getFightCooldown(ballerine,True)
        if timing > 0 :
            cooldownOk = False

        if cooldownOk and not(teamWinDB.isFightingBool(ballerine)):
            team1 = []
            if user.team != 0:
                file = readSaveFiles(absPath + "/userTeams/" + str(user.team) + ".team")
                for a in file[0]:
                    team1 += [loadCharFile(absPath + "/userProfile/" + a + ".prof")]
            else:
                team1 = [user]

            fun = random.randint(0,99)

            fightAnyway = True
            if fun < -1:           # Testing purposes
                await ctx.channel.send(embed=await getRandomStatsEmbed(bot,team1))

            if fightAnyway:
                await fight(bot,team1,[],ctx,guild,slash=True)

        elif teamWinDB.isFightingBool(ballerine):
            msg = await ctx.send(embed = errorEmbed("Woopsy","Vous êtes déjà en train de vous battre"),delete_after=10)
        else:
            msg = await ctx.send(embed = errorEmbed("Cooldown",f"Votre équipe ne pourra faire de combats rapides que dans {timing//60} minute(s)"),delete_after=10)

# octogone fight
@slash.subcommand(base="fight",name="octogone",description="Affrontez quelqu'un en 1v1 Gare Du Nord !",options=[
    create_option("versus","Affronter qui ?",6,required=True)
])
async def octogone(ctx,versus):
    try:
        pathGuildSettings = absPath + "/guildSettings/"+str(ctx.guild.id)+".set"
        valid = True
    except:
        pass
    
    if valid:
        if not existFile(pathGuildSettings):
            tempGuild = server(ctx.guild.id)
            saveGuildSettings(pathGuildSettings, tempGuild)
            print(f"Création du fichier {pathGuildSettings} ({ctx.guild.name})")
            guilds.append(tempGuild) 
        
        guild = None

        for a in guilds:
            if type(a) != int:
                if ctx.guild.id == a.id:
                    guild = a

    pathUserProfile,ballerine = absPath + "/userProfile/" + str(ctx.author.id) + ".prof",""
    if os.path.exists(pathUserProfile):
        if not(checkIsBotChannel(ctx,guild,bot)) and ctx.author.id == 213027252953284609:
            ballerine = "Tu va te calmer Léna, tu es pas dans le bon salon pour octogone quelqu'un"
            if not(os.path.exists(absPath + "/userProfile/" + versus.id + ".prof")):
                ballerine += f"\nEn plus {versus.name} n'a même pas commencé l'aventure"
        elif checkIsBotChannel(ctx,guild,bot) and ctx.author.id == 213027252953284609 and not(os.path.exists(absPath + "/userProfile/" + str(versus.id) + ".prof")) and not((versus.id in [623211750832996354,769999212422234122])):
            ballerine = f'{versus.name} n\'a pas commencé l\'aventure Léna'

        elif checkIsBotChannel(ctx,guild,bot) and os.path.exists(absPath + "/userProfile/" + str(versus.id) + ".prof"):
            await fight(bot,[loadCharFile(pathUserProfile)],[loadCharFile(absPath + "/userProfile/" + str(versus.id) + ".prof")],ctx,guild,auto=False,octogone=True,slash=True)

        elif checkIsBotChannel(ctx,guild,bot) and (versus.id in [623211750832996354,769999212422234122]):
            temp = loadCharFile(pathUserProfile)
            tempi = tablAllAllies[0]
            tempi.changeLevel(temp.level)
            await fight(bot,[temp],[tempi],ctx,guild,auto=False,octogone=True,slash=True)

        elif checkIsBotChannel(ctx,guild,bot):
            await ctx.send(f"{versus.name} n'a pas commencé l'aventure",delete_after=5)
        else:
            await ctx.send("ok",delete_after=5)

        if ballerine != "":
            await ctx.send(ballerine,delete_after=5)

# team fight
@slash.subcommand(base="fight",name="team",description="Affrontez l'équipe de quelqu'un avec la votre",options=[
    create_option("versus","Affronter qui ?",6,required=True)
])
async def teamFight(ctx,versus):
    try:
        pathGuildSettings = absPath + "/guildSettings/"+str(ctx.guild.id)+".set"
        valid = True
    except:
        pass
    
    if valid:
        if not existFile(pathGuildSettings):
            tempGuild = server(ctx.guild.id)
            saveGuildSettings(pathGuildSettings, tempGuild)
            print(f"Création du fichier {pathGuildSettings} ({ctx.guild.name})")
            guilds.append(tempGuild) 
        
        guild = None

        for a in guilds:
            if type(a) != int:
                if ctx.guild.id == a.id:
                    guild = a

    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile)
        ballerine,trouv,temp = 0,False,0
        if user.team == 0:
            ballerine = user.owner
        else:
            ballerine = user.team

        team1 = []
        if user.team != 0:
            file = readSaveFiles(absPath + "/userTeams/" + str(user.team) + ".team")
            for a in file[0]:
                team1 += [loadCharFile(absPath + "/userProfile/" + a + ".prof")]
        else:
            team1 = [user]


        team2 = []
        pathOctogonedProfile = absPath + "/userProfile/" + str(versus.id) + ".prof"
        if os.path.exists(pathOctogonedProfile):
            octogoned = loadCharFile(pathOctogonedProfile,ctx)
            if octogoned.team != 0:
                file = readSaveFiles(absPath + "/userTeams/" + str(octogoned.team) + ".team")
                for a in file[0]:
                    team2 += [loadCharFile(absPath + "/userProfile/" + a + ".prof")]
            else:
                team2 = [octogoned]

            await fight(bot,team1,team2,ctx,guild,False,octogone=True,slash=True)
        else:
            await ctx.send("L'utilisateur mentioné n'a pas commencé l'aventure",delete_after=5)
    else:
        await ctx.send("Tu n'as pas commencé l'aventure",delete_after=5)

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
        if not(teamWinDB.isFightingBool(int(user.team))):
            await ctx.send(embed= discord.Embed(title="__Cooldowns des commandes Fight l'équipe :__",description=f"__Normal__ : {fcooldown} minute{faccord} et {fseconds} seconde{fsaccord}\n__Quick__ : {fqcooldown} minute{fqaccord} et {fqseconds} seconde{fqsaccord}"),delete_after=10)
        else:
            await ctx.send(embed= discord.Embed(title="__Cooldowns des commandes Fight l'équipe :__",description=f"__Normal__ : En combat <:turf:810513139740573696>\n__Quick__ : {fqcooldown} minute{fqaccord} et {fqseconds} seconde{fqsaccord}"),delete_after=10)

# -------------------------------------------- PATCHNOTE --------------------------------------------
@slash.slash(name="patchnote",description="Renvoie le dernier patchnote du bot")
async def patchnote(ctx):
    await send_patchnote(ctx)

# -------------------------------------------- ROLL --------------------------------------------
@slash.slash(name="roll",description="Permet de lancer un dé",options=[
    create_option(name="min",description="Minimum du jet. Par défaut, 1",option_type=4,required=False),
    create_option(name="max",description="Minimum du jet. Par défaut, 100",option_type=4,required=False),
])
async def roll(ctx,min=1,max=100):
    rollmes = rollMessage[random.randint(0,len(rollMessage)-1)]
    await ctx.send(embed= discord.Embed(title=f"🎲 roll {min} - {max}",color=light_blue,description=rollmes.format(random.randint(min,max))))

# -------------------------------------------- SHOP --------------------------------------------
@slash.slash(name="shop",description="Vous permet d'entrer dans le magasin")
async def shopSlash(ctx):
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
async def invent2(ctx,destination=None,procuration=None,nom=None):
    to = False
    if destination == None and nom==None:
        await ctx.send(embed=discord.Embed(title="/inventory",description="Les champs \"destination\" et \"nom\" ne peuvent pas être tous les deux vides"),delete_after=15)
        to = True
    else:
        for a in range(5):
            if ["Equipement","Arme","Compétences","Objets spéciaux","Elements"][a] == destination:
                destination = a
                break

        if procuration != None:
            user = loadCharFile(absPath + "/userProfile/" + str(procuration.id) + ".prof")
            procurTemp = procuration.mention
        else:
            user = loadCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof")
            procurTemp = None

        if nom != None:
            nom = nom.replace("_"," ")
            nom = nom.lower()
            while nom.endswith(" "):
                nom = nom[0:-1]

            if whatIsThat(nom) == None:
                research = weapons[:]+skills[:]+stuffs[:]+others[:]+[token]
                lastResarch = []
                nameTempCmpt,lenName = 0, len(nom)
                while 1:
                    lastResarch = research[:]
                    if nameTempCmpt+2 <= lenName:
                        nameTempCmpt += 2
                    else:
                        nameTempCmpt = lenName

                    for a in research[:]:
                        temp = a.name.lower()
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
    if not(to):
        if nom != [None]:
            await inventory(bot,ctx,["/inventory"]+[procurTemp]+nom,[destination,procuration])
        else:
            await inventoryV2(bot,ctx,destination,user)

# -------------------------------------------- POINTS --------------------------------------------
@slash.slash(name="points",description="Vous permet de répartir vos points bonus",options=[
    create_option("procuration","De qui voulez vous consulter l'inventaire ?",6,required=False)
])
async def pts(ctx,procuration=None):
    await points(bot,ctx, ["/points",None],procuration,slashed=True)

# -------------------------------------------- TEAM --------------------------------------------
# team view
@slash.subcommand(base="team",name="view",description="Permet de voir les équipements de votre équipe ou de celle de quelqu'un d'autre",options=[
    create_option("joueur","Voir l'équipe d'un autre joueur",6,required=False)
])
async def teamView(ctx,joueur=None):
    if joueur==None:
        pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    else:
        pathUserProfile = absPath + "/userProfile/" + str(joueur.id) + ".prof"

    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile)
        pathTeam = absPath + "/userTeams/" + str(user.team) +".team"
        msg = await loadingSlashEmbed(ctx)
        if user.team == "0":
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
                    temp3 = None

                    temp3 = await bot.fetch_user(int(a))
                    temp3 = temp3.name

                    ballerine = f'{aspiEmoji[temp2.aspiration]} | {elemEmojis[temp2.element]} | {temp2.weapon.emoji} | {temp2.stuff[0].emoji} {temp2.stuff[1].emoji} {temp2.stuff[2].emoji} | '
                    for b in temp2.skills:
                        if type(b)==skill:
                            ballerine+=b.emoji
                    ballerine+="\n\n"

                    icon = await getUserIcon(bot,temp2)

                    points = ""
                    if temp2.points > 0:
                        points = " *(+)*"
                    temp += f"__{icon} **{temp2.name}** ({temp3})__{points}\n{ballerine}"

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
    await helpBot(bot,ctx)

# -------------------------------------------- START --------------------------------------------
@slash.slash(name="start",description="Permet de commence l'aventure")
async def started(ctx):
    await start(bot,ctx,["/start"])

# -------------------------------------------- STATS --------------------------------------------
@slash.slash(name="stats",description="Permet de voir vos statistiques ou celles d'un autre joueur",options=[
    create_option("joueur","Voir les statistiques d'un autre joueur",6,False)
])
async def stats(ctx,joueur=None):
    if joueur == None:
        pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    else:
        pathUserProfile = absPath + "/userProfile/" + str(joueur.id) + ".prof"

    if os.path.exists(pathUserProfile):
        msg = await loadingSlashEmbed(ctx)
        user = loadCharFile(pathUserProfile)

        userIcon = await getUserIcon(bot,user)

        rep = discord.Embed(title = f"__Page de statistique de {user.name} {userIcon}__",color = user.color,description = f"__Niveau :__ {user.level}\n__Expérience :__ {user.exp} / {user.level*50-20}\n\n__Element :__ {elemEmojis[user.element]} {elemNames[user.element]}\n<:empty:866459463568850954>")

        rep.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(userIcon)["id"]))
        rep.add_field(name = "__Aspiration :__",value = aspiEmoji[user.aspiration] + " " + inspi[user.aspiration],inline = False)

        sumStatsBonus = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

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

@slash.subcommand(base="admin",name="enable_Fight",guild_ids=[912137828614426704],description="Permet d'activer les combats ou non",options=[
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

@slash.subcommand(base="admin",name="restart_Bot",guild_ids=[912137828614426704],description="Permet de redémarrer le bot lorsque tous les combats seront fini")
async def restartCommand(ctx):
    await restart_program(bot,ctx)

@slash.subcommand(base="admin",subcommand_group="emoji",name="reset_all",guild_ids=[912137828614426704],description="Lance une rénitialisation des emojis")
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
    base = open("./data/custom_icon.db","w")
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

@slash.subcommand(base="admin",subcommand_group="emoji",name="remake_all",guild_ids=[912137828614426704],description="Supprime puis refait tous les emojis de personnage")
async def remakeCustomEmoji(ctx):
    msg = await ctx.send(embed = discord.Embed(title="Remake des emojis..."))
    await bot.change_presence(status=discord.Status.idle,activity=discord.Game(name="refaire les emojis..."))
    
    async def refresh(text : str):
        await msg.edit(embed = discord.Embed(title="Remake des emojis...",description=text))

    await refresh("Suppression de la base de données")
    try:
        customIconDB.dropCustom_iconTablDB
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

    allChar = os.listdir("./userProfile/")
    lenAllChar = len(allChar)
    cmpt = 0

    for num in allChar:
        user = loadCharFile("./userProfile/"+num)
        await getUserIcon(bot,user)
        cmpt += 1

        if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
            await refresh("Création des émojis ({0} %)".format(int(cmpt/lenAllChar*100)))
            lastTime = now

    await refresh("Fini !")
    await ctx.channel.send("Le remake des emojis est terminées !",delete_after=10)

    ballerine = datetime.datetime.now() + horaire + datetime.timedelta(hours=1)
    while ballerine.hour%3 != 0:
        ballerine = ballerine + datetime.timedelta(hours=1)

    await bot.change_presence(status=discord.Status.online,activity=discord.Game(name="Prochain shop à "+ballerine.strftime('%Hh')))

@slash.subcommand(base="admin",subcommand_group="backup",name="new",description="Permet de réaliser un backup des profiles de personnages",guild_ids=[912137828614426704])
async def adminBackup(ctx):
    temp = create_backup()
    try:
        await ctx.send(embed=discord.Embed(title="__Admin : Backups__",color=light_blue,description=temp))
    except:
        await ctx.channel.send(embed=discord.Embed(title="__Admin : Backups__",color=light_blue,description=temp))

if isLenapy:
    tabl=[912137828614426704,405331357112205326]
else:
    tabl=[912137828614426704]

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
    await procuration(ctx,utilisateur)

# -------------------------------------------- ICON --------------------------------------------
@slash.slash(name="icon",description="Renvoie l'icone de votre personnage")
async def iconCommand(ctx):
    try:
        user = loadCharFile("./userProfile/{0}.prof".format(ctx.author_id))
    except:
        await ctx.send("Vous devez avoir commencé l'Aventure pour utiliser cette commande\nFaites donc un tour du côté de /start !",delete_after=15)
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

    tablNames = [[[],[],[]],[[],[],[]],[[],[],[]]]
    for cmpt in (0,1,2):
        embed = discord.Embed(title="__Ennemi répartion : {0}__".format(["DPT","Healer/Shilder","Support"][cmpt]),color=light_blue)
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
    embed = discord.Embed(title="__Hors catégorie :__".format(["DPT","Healer/Shilder","Support"][cmpt]),color=light_blue,description=desc)

    await ctx.channel.send(embed = embed)

# -------------------------------------------- SEE SKILL RECOMMENDED POWER
@slash.subcommand(base="see",name="skillRecommandedPower",guild_ids=[615257372218097691],description="Permet de voir la répartition des ennemis")
async def seeSkillRecommandedPower(ctx):
    temp,debut = "",False
    for cmpt in range(len(skills)):
        castTime = 0
        tempSkill = skills[cmpt]
        if tempSkill.type == TYPE_DAMAGE:
            while not(tempSkill.effectOnSelf == None or (tempSkill.effectOnSelf != None and findEffect(tempSkill.effectOnSelf).replica == None)):
                tempSkill = findSkill(findEffect(tempSkill.effectOnSelf).replica)
                castTime += 1

            power = 25 + 25 * tempSkill.cooldown + 50 * castTime + 55 * tempSkill.ultimate

            if tempSkill.effectOnSelf != None and findEffect(tempSkill.effectOnSelf).stun:
                power += (findEffect(tempSkill.effectOnSelf).turnInit -1) * 15


            if tempSkill.area != AREA_MONO:
                power = power * 0.7
            if tempSkill.use == MAGIE:
                power = power * 1.2

            if tempSkill.effect[0] != None or tempSkill.effectOnSelf != None:
                power = power * 0.7
            
            if tempSkill.onArmor != 1:
                power = power * (1 - min(0.5,(tempSkill.onArmor-1)/2))

            power = int(power / tempSkill.repetition)

            if power != tempSkill.power:
                temp += "{0} __{1}__ : {2} (rec : {3})\n".format(tempSkill.emoji,tempSkill.name,tempSkill.power,power)
        if ((cmpt+1)%20 == 0 or cmpt == len(skills)-1) and temp != "":
            if not(debut):
                await ctx.send(embed=discord.Embed(title="Recommaned power",color=light_blue,description=temp))
                debut = True
            else:
                await ctx.channel.send(embed=discord.Embed(title="Recommaned power",color=light_blue,description=temp))
            temp = ""

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