##########################################################
# Importations :
import asyncio
import discord, random, os, emoji, datetime,sys
from discord_slash.model import SlashCommandOptionType,ButtonStyle
from importlib import import_module

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

actualyFight,actualyQuickFight = [],[]
pathUserProfile = absPath + "/userProfile/"
ctxChannel = 0
listGuildSet = os.listdir(absPath + "/guildSettings/")
guilds = list(range(0,len(listGuildSet)))

###########################################################
# Initialisation
allShop = weapons + skills + stuffs + others

class shopClass:
    def __init__(self,shopList : list):
        self.shopping = [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
        if shopList != False:
            for a in range(0,len(shopList)):
                if a != None:
                    nani = whatIsThat(shopList[a])
                    if nani == 0:
                        self.shopping[a] = findWeapon(shopList[a])
                    elif nani == 1:
                        self.shopping[a] = findSkill(shopList[a])
                    elif nani == 2:
                        self.shopping[a] = findStuff(shopList[a])
                    elif nani == 3:
                        self.shopping[a] = findOther(shopList[a])
    
    async def newShop(self):
        shopping = list(range(0,len(self.shopping)))
        ballerine = datetime.datetime.now() + (datetime.timedelta(hours=3)+horaire)

        if globalVar.fightEnabled():
            await bot.change_presence(activity=discord.Game("Nouveau shop : "+ballerine.strftime('%H:%M')))

        shopWeap,shopSkill,shopStuff,ShopOther = [],[],[],others[:]
        for a in weapons:
            if a.price > 0:
                shopWeap.append(a)
                
        for a in skills:
            if a.price > 0:
                shopSkill.append(a)
                
        for a in stuffs:
            if a.price > 0:
                shopStuff.append(a)
        
        temp = [4,4,6,2]
        tablShop = [shopWeap,shopSkill,shopStuff,ShopOther]
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

async def inventoryVerif(bot):
    for z in os.listdir(absPath + "/userProfile/"):
        user = loadCharFile(absPath + "/userProfile/" + z)
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
            saveCharFile(absPath + "/userProfile/" + z,user)
            try:
                toUser = await bot.fetch_user(user.owner)
                message = ""
                if modifSkill > 0:
                    message+=ballerine+"\n"
                if modifStuff > 0:
                    message+=babie
                await toUser.send(embed=discord.Embed(title = "Problème lors de la vérification automatique de l'inventaire",color=user.color,description=message))
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
            saveCharFile(absPath + "/userProfile/" + z,user)
            try:
                toUser = await bot.fetch_user(user.owner)
                await toUser.send(embed=discord.Embed(title = "Problème lors de la vérification automatique de l'inventaire",color=user.color,description=temp))
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
            saveCharFile(absPath + "/userProfile/" + z,user)

            try:
                toUser = await bot.fetch_user(user.owner)
                await toUser.send(embed=discord.Embed(title = "Problème lors de la vérification automatique de l'inventaire",color=user.color,description="Votre élément de ne respecte pas les restrictions de niveau\n\n"+temp))
            except:
                pass

bidule = stuffDB.getShop()
shopping = shopClass(bidule["ShopListe"])

@tasks.loop(seconds=1)
async def oneClock():
    tick = datetime.datetime.now()
    if tick.second%60 == 0 and not(minuteClock.is_running()):
        minuteClock.start()

@tasks.loop(minutes=1)
async def minuteClock():
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
        await shopping.newShop()

    if tick.hour==0:
        for log in os.listdir("./data/fightLogs/"):
            try:
                os.remove("./data/fightLogs/"+log)
                print("{0} supprimé".format("./data/fightLogs/"+log))
            except:
                print("{0} n'a pas pu être supprimé".format("./data/fightLogs/"+log))

    # Skill Verif
    await inventoryVerif(bot)

@bot.event
async def on_ready():
    print("\n-----------------------------\nLe bot est en ligne. Début de la phase d'initialisation post-online !\n----------------------\n")
    globalVar = globalVarDb()
    aliceStatsDb = aliceStatsdbEndler()
    teamWinDB = dbHandler("teamVic.db")
    stuffDB = dbHandler(database="stuff.db")
    customIconDB = dbHandler(database="custom_icon.db")
    startMsg = globalVar.getRestartMsg()
    if startMsg != 0:
        msg = await bot.fetch_channel(912137828614426707)
        msg = await msg.fetch_message(startMsg)

        await msg.edit(embed=discord.Embed(title="Redémarrage en cours...",description="Phase d'initalisation..."))
        globalVar.changeFightEnabled(True)

    cmpt = 0
    lastTime = datetime.datetime.now().second
    lenGuild = len(listGuildSet)
    print("Chargement des fichiers de guilds... 0%")
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
            print("Chargement des fichiers de guilds... {0}%".format(round((cmpt/lenGuild)*100)))
            lastTime = now

        cmpt += 1

    print("Chargement des fichiers de guilds terminé !\n")
    if bidule != False:
        ballerine = bidule["Date"] + datetime.timedelta(hours=3)+horaire

        if not(globalVar.fightEnabled()):
            await bot.change_presence(status=discord.Status.dnd,activity=discord.Game(name="Les combats sont actuellements désactivés"))
        else:
            await bot.change_presence(status=discord.Status.online,activity=discord.Game(name="Nouveau shop : "+ballerine.strftime('%H:%M')))

    if not(oneClock.is_running()):
        oneClock.start()

    teamWinDB.resetAllFightingStatus()

    print("\nMise à jour des fichiers data...")
    await downloadAllHeadGearPng(bot)
    await downloadAllWeapPng(bot)
    await downloadAllIconPng(bot)
    await downloadElementIcon(bot)
    print("Mise à jour des fichiers data terminée")
    
    await inventoryVerif(bot)

    print("\n-----------------------------\nFin de l'initialisation\n-----------------------------\n")

    if startMsg != 0:
        await msg.edit(embed=discord.Embed(title="Redémarrage en cours...",color=light_blue,description="Le bot a bien été redémarré"))
        await msg.channel.send("Le redémarrage du bot est terminé Léna",delete_after=10)
        globalVar.getRestartMsg(int(0))
        print("Redémarrage terminé")

###########################################################
# Commandes
begoneTabl = []
def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """
    print("Recive restart command")
    args = sys.argv[:]

    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]
    os.execv(sys.executable, args)

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
                    mention = ctx.mentions[0]
                    pathUserProfile = absPath + "/userProfile/" + str(mention.id) + ".prof"
                    user = quickLoadCharFile(pathUserProfile)
                    user[0].currencies = user[0].currencies + 50000

                    quickSaveCharFile(pathUserProfile,user)                
                elif args[1] == "forceRestat":
                    if args[2] == "all":
                        for a in os.listdir(absPath + "/userProfile/"):
                            pathUserProfile = absPath + "/userProfile/" + a
                            user = loadCharFile(pathUserProfile,ctx)
                            user = silentRestats(user)

                            saveCharFile(pathUserProfile,user)
                            print(f"{user.name} a bien été restat")
                        
                    else:
                        try:
                            stated = ctx.mentions[0]
                            pathUserProfile = absPath + "/userProfile/" + str(stated.id) + ".prof"
                            user = loadCharFile(pathUserProfile,ctx)
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
                                user = loadCharFile(pathUserProfile,ctx)
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
                            user = loadCharFile(pathUserProfile,ctx)
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
                elif args[1] == "resetCustomEmoji":
                    msg = await loadingEmbed(ctx)

                    async def refresh(text : str):
                        await msg.edit(embed = discord.Embed(title=args[0]+ " - "+args[1],description=text))

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

                    for num in allChar:
                        user = loadCharFile("./userProfile/"+num)
                        await getUserIcon(bot,user)
                        cmpt += 1

                        if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
                            await refresh("Création des émojis ({0} %)".format(int(cmpt/lenAllChar*100)))
                            lastTime = now

                    await refresh("Fini !")
                elif args[1] == "forceShop":
                    await shopping.newShop()
                    await ctx.add_reaction('❄')

                #except:
                    #await ctx.add_reaction('<:LenaWhat:760884455727955978>')

            elif args[0] == guild.prefixe + "solde" and checkIsBotChannel(ctx,guild,bot):
                pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
                if os.path.exists(pathUserProfile):
                    user = loadCharFile(pathUserProfile,ctx)
                    await ctx.channel.send(embed = discord.Embed(title = "Porte monnaie", description = f"Ta solde actuelle est de {user.currencies} {emoji.coins}",color = user.color))
                else:
                    await ctx.channel.send("Tu n'a pas commencé l'aventure")

            elif args[0] == guild.prefixe + "invite" and checkIsBotChannel(ctx,guild,bot):
                if os.path.exists("../Kawi/"):
                    await ctx.channel.send(embed = discord.Embed(title = args[0],color = light_blue,url = 'https://canary.discord.com/api/oauth2/authorize?client_id=769999212422234122&permissions=1074097216&scope=bot%20applications.commands'))
                else:
                    await ctx.channel.send(embed = discord.Embed(title = args[0],color = light_blue,url = 'https://canary.discord.com/api/oauth2/authorize?client_id=623211750832996354&permissions=1074129984&scope=bot%20applications.commands'))

            elif args[0] == "l!test" and ctx.author.id == 213027252953284609:
                await ctx.channel.send(cafe())

            elif args[0] == guild.prefixe + "procuration" and checkIsBotChannel(ctx,guild,bot):
                await procuration(ctx)

            elif args[0] == guild.prefixe + "icon" and checkIsBotChannel(ctx,guild,bot):
                pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
                await ctx.add_reaction(emoji.loading)
                if os.path.exists(pathUserProfile):
                    user = loadCharFile(pathUserProfile,ctx)
                    await makeCustomIcon(bot,user)
                    ballerine, babie = getEmojiObject(await getUserIcon(bot,user)),None
                    iconGuildList = []
                    if os.path.exists("../Kawi/"):
                        iconGuildList = ShushyCustomIcons
                    else:
                        iconGuildList = LenaCustomIcons
                    for a in iconGuildList:
                        try:
                            guild = await bot.fetch_guild(a)
                            babie = await guild.fetch_emoji(ballerine["id"])
                        except:
                            pass

                    await ctx.clear_reaction(emoji.loading)
                    if babie != None:
                        url = babie.url
                        await ctx.channel.send(url)
                    else:
                        await ctx.channel.send(embed=errorEmbed(args[0],"L'icone de votre personnage n'a pas pu être récupéré"))
                else:
                    await ctx.channel.send(embed=errorEmbed(args[0],"Vous n'avez pas commencé l'aventure"))

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
                await addExpUser(bot,guild,pathUserProfile,ctx,3,3)

# encyclopedia ----------------------------------------
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

# FIGHT -----------------------------------------------
@slash.slash(name="fight",description="test",options=[])

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
        user = loadCharFile(pathUserProfile,ctx)
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
            if fun < 1:                # But nobody came
                teamIcon = ""
                for wonderfullIdea in team1:
                    teamIcon += "{0} {1}\n".format(await getUserIcon(bot,wonderfullIdea),wonderfullIdea.name)

                temp1 = discord.Embed(title = "__Résultats du combat :__",color = black,description="__Danger :__ <a:bnc:908762423111081994>\n__Nombre de tours :__ <a:bnc:908762423111081994>\n__Durée :__ <a:bnc:908762423111081994>")
                temp1.add_field(name="<:empty:866459463568850954>\n__Vainqueurs :__",value=teamIcon,inline=True)
                temp1.add_field(name="<:empty:866459463568850954>\nPerdants :",value="[[But nobody came](https://bit.ly/3wDwyF3)]",inline=True)

                await ctx.send(embed = temp1,components=[])
                fightAnyway = False

            elif fun < 3:              # All OctoHeals ! Yes, it's for you H
                temp = team1
                temp.sort(key=lambda overheal: overheal.level,reverse=True)
                maxLvl = temp[0].level

                team2 = []
                lenBoucle = max(4,len(team1))
                cmpt = 0

                if maxLvl < tablAllOcta[42].baseLvl:
                    alea = copy.deepcopy(tablAllOcta[6])
                else:
                    alea = copy.deepcopy(tablAllOcta[42])

                alea.changeLevel(maxLvl)

                while cmpt < lenBoucle:
                    team2.append(alea)
                    cmpt += 1

                permaIncur30 = copy.deepcopy(incur[3])
                permaIncur30.turnInit, permaIncur30.unclearable = -1, True

                await fight(bot,team1,team2,ctx,guild,False,slash=True,contexte=[[TEAM2,permaIncur30]])
                fightAnyway = False

            elif fun < 5:              # All Temmies
                temp = team1
                temp.sort(key=lambda overheal: overheal.level,reverse=True)
                maxLvl = temp[0].level

                team2 = []
                lenBoucle = max(4,len(team1))
                cmpt = 0

                alea = copy.deepcopy(findEnnemi("Temmie"))
                alea.changeLevel(maxLvl)

                while cmpt < lenBoucle:
                    team2.append(alea)
                    cmpt += 1

                permaDamageDown = effect("Malus de dégâts (20%)","damageDown",percing=-20,turnInit=-1,type=TYPE_MALUS,unclearable=True)
                permaDamageDown.turnInit, permaDamageDown.unclearable = -1, True

                await fight(bot,team1,team2,ctx,guild,False,slash=True,contexte=[[TEAM2,permaDamageDown]])
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
        user = loadCharFile(pathUserProfile,ctx)
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
            msg = await ctx.send(embed = errorEmbed("Cooldown",f"Votre équipe ne pourra faire de combats normaux que dans {timing//60} minute(s)"),delete_after=10)

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
        user = loadCharFile(pathUserProfile,ctx)
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

# cooldown ---------------------------------------------
@slash.slash(name="cooldowns",description="Vous donne les cooldowns des commandes /fight et /quickFight pour votre équipe")
async def cooldowns(ctx):
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile,ctx)
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

# Patchnote
@slash.slash(name="patchnote",description="Renvoie le dernier patchnote du bot")
async def patchnote(ctx):
    await send_patchnote(ctx)

# Roll
@slash.slash(name="roll",description="Permet de lancer un dé",options=[
    create_option(name="min",description="Minimum du jet. Par défaut, 1",option_type=4,required=False),
    create_option(name="max",description="Minimum du jet. Par défaut, 100",option_type=4,required=False),
])
async def roll(ctx,min=1,max=100):
    rollmes = rollMessage[random.randint(0,len(rollMessage)-1)]
    await ctx.send(embed= discord.Embed(title=f"🎲 roll {min} - {max}",color=light_blue,description=rollmes.format(random.randint(min,max))))

# Shop
@slash.slash(name="shop",description="Vous permet d'entrer dans le magasin")
async def shopSlash(ctx):
    await shop2(bot,ctx,shopping.shopping)

# Inventory
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
                research = weapons[:]+skills[:]+stuffs[:]+others[:]
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
            
            nom = [nom,None]

        else:
            nom = [None]
    if not(to):
        if nom != [None]:
            await inventory(bot,ctx,["/inventory"]+[procurTemp]+nom,[destination,procuration])
        else:
            await inventoryV2(bot,ctx,destination,user)

# Points
@slash.slash(name="points",description="Vous permet de répartir vos points bonus",options=[
    create_option("procuration","De qui voulez vous consulter l'inventaire ?",6,required=False)
])
async def pts(ctx,procuration=None):
    await points(bot,ctx, ["/points",None],procuration,slashed=True)

# TEAM ------------------------------------------------------------------------
@slash.slash(name="team",description="Permet de gérer son équipe",options=[])

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
        user = quickLoadCharFile(pathUserProfile)
        user = user[0]
        pathTeam = absPath + "/userTeams/" + user.team +".team"
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
        user = quickLoadCharFile(pathUserProfile)
        Qsave = user[1]
        user = user[0]
        pathTeam = absPath + "/userTeams/" + user.team +".team"
        msg = await loadingSlashEmbed(ctx)

        if not(os.path.exists(pathTeam) and user.team != "0"):
            rdm = str(random.randint(1,10000))
            pathTeam = absPath + "/userTeams/" + rdm +".team"
            rewriteFile(pathTeam,f"{str(user.owner)};")
            user.team = rdm
            quickSaveCharFile(pathUserProfile,[user,Qsave])

        noneCap,selfAdd,temp = True,False,readSaveFiles(absPath + "/userTeams/" + user.team +".team")

        if len(temp[0]) >= 8:
            noneCap = False      

        if ctx.author == joueur:
            selfAdd = True          

        if noneCap and not(selfAdd):
            mention = joueur
            if os.path.exists(absPath + "/userProfile/" + str(mention.id) + ".prof"):
                allReadyinTeam,allReadyInThatTeam,mate = False, False,quickLoadCharFile(absPath + "/userProfile/" + str(mention.id) + ".prof")
                
                if mate[0].team != "0":
                    allReadyinTeam = True
                    if mate[0].team == user.team:
                        allReadyInThatTeam = True


                if not(allReadyinTeam):
                    await msg.edit(embed = discord.Embed(title = "/team add "+joueur.name, color = user.color, description = f"{mention.mention}, {ctx.author.mention} vous propose de rejoidre son équipe. Qu'en dites vous ?"))
                    await msg.add_reaction(emoji.check)
                    await msg.add_reaction(emoji.cross)

                    def checkisIntendedUser(reaction,user):
                        return user == mention

                    try:
                        reaction = await bot.wait_for("reaction_add",timeout=60,check=checkisIntendedUser)
                        if str(reaction[0]) == emoji.check:
                            mate[0].team = user.team
                            quickSaveCharFile(absPath + "/userProfile/" + str(mention.id) + ".prof",mate)

                            file = readSaveFiles(pathTeam)
                            file[0] += [str(mention.id)]
                            saveSaveFiles(pathTeam,file)
                            await msg.clear_reactions()
                            await msg.edit(embed = discord.Embed(title="/team add "+joueur.name,color = user.color,description = "Vous faites dorénavent parti de la même équipe"))
                    except:
                        await msg.clear_reactions()
                
                elif allReadyInThatTeam:
                    await msg.edit(embed = errorEmbed("/team add "+joueur.name,"Ce joueur est déjà dans ton équipe"))
                elif allReadyinTeam:
                    await msg.edit(embed = errorEmbed("/team add "+joueur.name,"Ce joueur est déjà dans une équipe"))

            else:
                await msg.edit(embed = errorEmbed("/team add "+joueur.name,"Cet utilisateur n'a pas commencé l'aventure"))  

# team quit
@slash.subcommand(base="team",name="quit",description="Permet de quitter son équipe")
async def teamQuit(ctx):
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = quickLoadCharFile(pathUserProfile)
        Qsave = user[1]
        user = user[0]
        pathTeam = absPath + "/userTeams/" + user.team +".team"

    if user.team != "0":
        team = readSaveFiles(pathTeam)
        team[0].remove(str(ctx.author.id))
        user.team = "0"

        saveSaveFiles(pathTeam,team)
        await ctx.send(embed = discord.Embed(title = "/team quit",color = user.color, description = "Vous avez bien quitté votre équipe"))
        quickSaveCharFile(pathUserProfile,[user,Qsave])
    else:
        await ctx.send(embed = errorEmbed("/team quit","Vous n'avez aucune équipe à quitter"))

# team fact
@slash.subcommand(base="team",name="fact",description="Permet d'avoir des facts sur les membres de votre équipe")
async def teamFact(ctx):
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = quickLoadCharFile(pathUserProfile)
        Qsave = user[1]
        user = user[0]
        pathTeam = absPath + "/userTeams/" + user.team +".team"

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

# HELP ----------------------------------------------------------------
@slash.slash(name="help",description="Ouvre la page d'aide du bot")
async def helpCom(ctx):
    await helpBot(bot,ctx)

# START
@slash.slash(name="start",description="Permet de commence l'aventure")
async def started(ctx):
    await start(bot,ctx,["/start"])

# STATS
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
        user = loadCharFile(pathUserProfile,ctx)

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
        rep.add_field(name = "<:empty:866459463568850954>\n__Statistiques secondaires :__",value = f"Résistance : {user.resistance} ({sumStatsBonus[7]})\nPénétration d'Armure : {user.percing} ({sumStatsBonus[8]})\nCritique : {user.critical} ({sumStatsBonus[9]})\n\nSoins : {sumStatsBonus[10]}\nBoost et Malus : {sumStatsBonus[11]}\nArmures : {sumStatsBonus[12]}\nDégâts directs : {sumStatsBonus[13]}\nDégâts indirects : {sumStatsBonus[14]}\n\nLes statistiques d'actions s'ajoutent à vos statistiques quand vous réalisez l'action en question",inline = True)
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

# MANUEL
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

# SEE LOGS
@slash.slash(name="SeeFightLogs",description="Permet de consulter les logs des combats du jour",guild_ids=[615257372218097691])
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

# SEE STUFF
@slash.slash(name="SeeStuffRepartition",description="Permet de consulter la réportation des logs",guild_ids=[615257372218097691])
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

# CHOOSE
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

# ------------------------------- ADMIN ----------------------------------------------

@slash.subcommand(base="admin",name="enableFight",guild_ids=[912137828614426704],description="Permet d'activer les combats ou non",options=[
    create_option("valeur","Activer ou désaciver les combats", SlashCommandOptionType.BOOLEAN,False)
])
async def addEnableFight(ctx,valeur = None):
    globalVar.changeFightEnabled(valeur)
    if valeur == None:
        valeur = globalVar.fightEnabled()

    if not(valeur):
        await bot.change_presence(status=discord.Status.dnd,activity=discord.Game(name="Les combats sont actuellements désactivés"))
    else:
        bidule = stuffDB.getShop()
        ballerine = bidule["Date"] + datetime.timedelta(hours=3)+horaire
        await bot.change_presence(status=discord.Status.online,activity=discord.Game(name="Nouveau shop : "+ballerine.strftime('%H:%M')))

    await ctx.send(embed=discord.Embed(title="__Admin Enable Fight__",description="Les combats sont désormais __{0}__".format(["désactivés","activés"][int(valeur)]),color=[red,light_blue][int(valeur)]))

@slash.subcommand(base="admin",name="restartBot",guild_ids=[912137828614426704],description="Permet de redémarrer le bot lorsque tous les combats seront fini")
async def restartCommand(ctx):
    msg = await ctx.send(embed = discord.Embed(title="Redémarrage en attente...",description="Vérifications des équipes en combat..."))
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
                    await msg.edit(embed = discord.Embed(title="Redémarrage en attente...",description="Un combat est encore en cours <a:loading:862459118912667678>"))
                    firstIt = False
                fighting = True
                break
        if fighting:
            await asyncio.sleep(3)
    
    await msg.edit(embed = discord.Embed(title="Redémarrage en attente...",description="Redémarrage en cours..."))
    restart_program()

###########################################################
# Démarrage du bot
if os.path.exists("../Kawi/"):
    print("\nKawiiiiii")
    bot.run(shushipy)
else:
    print("\nIl semblerait que je sois seule cette fois. Je m'occuperais de Shushi une autre fois")
    bot.run(lenapy)