###########################################################
# Importations :
from typing import Type
from asyncio.locks import Condition
import discord, random, gestion, os, emoji,neutral,asyncio,datetime,time,traceback,inspect

from discord.utils import _URL_REGEX

from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from commands.command_encyclopedia import *
from commands.command_fight import *
from commands.command_inventory import *
from commands.command_start import *
from commands.command_procuration import *
from commands.command_points import *
from commands.command_shop import *
from commands.sussess_endler import *
from data.database import *
from commands.command_patchnote import *
from discord.ext import commands, tasks
from discord_slash import ButtonStyle, SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice

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
existDir(absPath + "/data/images/headgears/")
existDir(absPath + "/data/images/weapons/")
existDir(absPath + "/data/images/char_icons/")
existDir(absPath + "/data/patch/")

actualyFight,actualyQuickFight = [],[]
pathUserProfile = absPath + "/userProfile/"
ctxChannel = 0
listGuildSet = os.listdir(absPath + "/guildSettings/")
guilds = list(range(0,len(listGuildSet)))

choiceExeptMsg = "missingMood.choiceExeptMsg"
errorMissingPermsMsg = "missingMood.errorMissingPermsMsg"
errorNotDigitMsg = "missingMood.errorNotDigitMsg"
errorNotInRangeMsg = "missingMood.errorNotInRangeMsg"
comfirmGuildSettingsChange = "missin.gMoodcomfirmGuildSettingsChange"
rejectGuildSettingsChange = "MissingMood.rejectGuildSettingsChange"
corruptNotice = "MissingMood.corruptNotice"
errorNotAChannel = "MissingMood.errorNotAChannel"
chooseMsg1 = "MissingMood.chooseMsg1"
chooseMsg2 = "MissingMood.chooseMsg2"
chooseMsg3 = "MissingMood.chooseMsg3"
errorUnknowMsg = "MissingMood.errorUnknowMsg"
comfirmProfileStart = "MissingMood.comfirmProfileStart"
rejectProfileStart = "MissingMood.rejectProfileStart"
startAlReadyStarted = "MissingMood.startAlReadyStarted"
currenties = "MissingMood.currenties"

###########################################################
# Mood

mood = 0

if mood == 0: # Neutral
    choiceExeptMsg = neutral.choiceExeptMsg
    errorMissingPermsMsg = neutral.errorMissingPermsMsg
    errorNotDigitMsg = neutral.errorNotDigitMsg
    errorNotInRangeMsg = neutral.errorNotInRangeMsg
    comfirmGuildSettingsChange = neutral.comfirmGuildSettingsChange
    rejectGuildSettingsChange = neutral.rejectGuildSettingsChange
    corruptNotice = neutral.corruptNotice
    errorNotAChannel = neutral.errorNotAChannel
    chooseMsg1 = neutral.chooseMsg1
    chooseMsg2 = neutral.chooseMsg2
    chooseMsg3 = neutral.chooseMsg3
    errorUnknowMsg = neutral.errorUnknowMsg
    comfirmProfileStart = neutral.comfirmProfileStart
    rejectProfileStart = neutral.rejectProfileStart
    startAlReadyStarted = neutral.startAlReadyStarted
    currenties = neutral.currenties

###########################################################
# Initialisation
allShop = weapons + skills + stuffs + others

class shopClass:
    def __init__(self,shopList : list):
        self.shopping = [None,None,None,None,None,None,None,None,None,None,None,None]
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
        ballerine = datetime.datetime.now() + datetime.timedelta(hours=3)+horaire

        await bot.change_presence(activity=discord.Game("Nouveau shop : "+ballerine.strftime('%H:%M')))
        validShop = False
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
        
        temp = [3,3,5,1]
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
            
        weaps,skils,stufs,othes = [],[],[],[]
        temp = ""
        stuffDB.addShop(shopping)
        for a in shopping:
            temp += f"\n{a.name}"

        print("\n--------------\nLe nouveau shop est :"+temp+"\n------------")
        self.shopping = shopping

bidule = stuffDB.getShop()
shopping = shopClass(bidule["ShopListe"])

@tasks.loop(hours=3)
async def skillVerif():
    for z in os.listdir(absPath + "/userProfile/"):
        user = loadCharFile(absPath + "/userProfile/" + z)
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

        tablInventory = [user.weaponInventory,user.skillInventory,user.stuffInventory]
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
            user.weaponInventory,user.skillInventory,user.stuffInventory = tablInventory[0],tablInventory[1],tablInventory[2]
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
            print(f"Les compétences de {user.name} ont été mises à jours")

@tasks.loop(hours=1)
async def fightCooldownRefresh():
    asuppr = []
    for a in actualyFight:
        now = datetime.datetime.now()
        timeD = now - a[1]
        if timeD.total_seconds() > 3600:
            asuppr.append(a)

    for a in asuppr:
        actualyFight.remove(a)

    asuppr = []
    for a in actualyQuickFight:
        now = datetime.datetime.now()
        timeD = now - a[1]
        if timeD.total_seconds() > 3600*3:
            asuppr.append(a)

    for a in asuppr:
        actualyQuickFight.remove(a)

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
    teamWinDB.resetAllFightingStatus()
    tick = datetime.datetime.now()+horaire
    if tick.hour%3==0:
        await shopping.newShop()

@bot.event
async def on_ready():
    print("\n-----------------------------\nLe bot est en ligne. Début de la phase d'initialisation post-online !\n----------------------\n")
    cmpt = 0
    while cmpt < len(listGuildSet):
        if listGuildSet[cmpt] != "index.set":
            try:
                guildSettings = readSaveFiles(absPath + "/guildSettings/"+listGuildSet[cmpt])
                guilds[cmpt] = server(int(listGuildSet[cmpt][0:-4]),guildSettings[0][0],int(guildSettings[0][1]),int(guildSettings[0][2]))
                guilds[cmpt].colorRole.enable, guilds[cmpt].colorRole.red, guilds[cmpt].colorRole.orange, guilds[cmpt].colorRole.yellow, guilds[cmpt].colorRole.green, guilds[cmpt].colorRole.lightBlue, guilds[cmpt].colorRole.blue, guilds[cmpt].colorRole.purple, guilds[cmpt].colorRole.pink = bool(int(guildSettings[1][0][1:])),int(guildSettings[1][1]),int(guildSettings[1][2]),int(guildSettings[1][3]),int(guildSettings[1][4]),int(guildSettings[1][5]),int(guildSettings[1][6]),int(guildSettings[1][7]),int(guildSettings[1][8])

                guild = await bot.fetch_guild(guilds[cmpt].id)
                guilds[cmpt].name = guild.name

                print(f"Le fichier du serveur {guilds[cmpt].name} a été chargé")
            except:
                print(f"Erreur dans le chargement du fichier {listGuildSet[cmpt]}")
                os.remove(absPath + "/guildSettings/"+listGuildSet[cmpt])

        cmpt += 1

    if bidule != False:
        ballerine = bidule["Date"] + datetime.timedelta(hours=3)
        if not(os.path.exists("../Kawi")):
            ballerine = bidule["Date"] + datetime.timedelta(hours=5)

        await bot.change_presence(activity=discord.Game("Nouveau shop : "+ballerine.strftime('%H:%M')))

        if not(oneClock.is_running()):
            oneClock.start()

    if not(fightCooldownRefresh.is_running()):
        fightCooldownRefresh.start()
    if not(skillVerif.is_running()):
        skillVerif.start()

    teamWinDB.resetAllFightingStatus()

    await asyncio.sleep(1)
    print("\nMise à jour des fichiers data...")
    await downloadAllHeadGearPng(bot)
    await downloadAllWeapPng(bot)
    await downloadAllIconPng(bot)
    print("Mise à jour des fichiers data terminée")
    
    started = True
    print("\n-----------------------------\nFin de l'initialisation\n-----------------------------\n")

@bot.event
async def on_error(error1,error2):
    if error2.author.id != 769999212422234122 and error2.author.id != 623211750832996354:
        if "TimeoutError" not in traceback.format_exc():
            if error2.author.guild.name != "dual T Squad":
                babie = datetime.datetime.now()
                ballerine = discord.Embed(title = error1,color=red,description="Une erreur est survenue\nUn rapport d'erreur a été envoyé")
                errorChannel = await bot.fetch_channel(error2.channel.id)
                await errorChannel.send(embed = ballerine)

                ballerine = discord.Embed(title = error1,color=red,description="Une erreur est survenue")
                ballerine.add_field(name="__Serveur :__",value=f"**{error2.author.guild.name}**\n{error2.channel.name}")
                ballerine.add_field(name="__Heure :__",value=babie.strftime("%m/%d/%Y, %H:%M:%S"))
                ballerine.add_field(name="__Message :__",value=error2.content + "\n(" + error2.author.name+")",inline=False)
                if len(traceback.format_exc()) > 1024:
                    ballerine.add_field(name="__Erreur :__",value="(...)\n"+traceback.format_exc()[-1000:],inline=False)
                else:
                    ballerine.add_field(name="__Erreur :__",value=traceback.format_exc(),inline=False)

                errorChannel = await bot.fetch_channel(808394788126064680)
                await errorChannel.send(embed = ballerine)
            else:
                await error2.add_reaction('<:LenaWhat:760884455727955978>')
        else:
            await error2.add_reaction('🕛')

###########################################################
# Commandes
begoneTabl = []

@bot.event
async def on_message(ctx):
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
                    await msg.edit(embed = errorEmbed(args[0],errorMissingPermsMsg))
                    
                else:
                    guildSettingsTemp = guild
                    choiceSettings = ["Préfixe","Salon des patchnotes","Salon bots","Couleur automatique"]
                    etat = -1
                    while etat > -10:
                        if etat == -1:
                            await msg.edit(embed = discord.Embed(title = args[0], description = choice(choiceSettings),color = light_blue))
                            respond = await bot.wait_for("message",timeout = 60,check = checkIsAuthor)

                            if not respond.content.isdigit():
                                await msg.edit(embed = errorEmbed(args[0],errorNotDigitMsg))
                            else:
                                repMsg = respond
                                respond = int(respond.content)
                                if not(respond < len(choiceSettings) and respond >= 0):
                                    await msg.edit(embed = errorEmbed(args[0],errorNotInRangeMsg))
                                else:
                                    etat = respond

                                try:
                                    await repMsg.delete()
                                except:
                                    1

                        if etat == 0:
                            await msg.edit(embed = discord.Embed(title = args[0]+" préfixe",color = light_blue,description = f"Le préfixe actuel du serveur est : **__{guild.prefixe}__**\nPar quoi voulez vous le remplacer ?\n\nVous pourrez toujours utiliser le préfixe par défaut (l!) pour la commande settings"))
                            newPrefixe = await bot.wait_for("message",timeout = 60,check = checkIsAuthor)
                            guildSettingsTemp.prefixe = newPrefixe.content
                            if saveGuildSettings(pathGuildSettings,guildSettingsTemp):
                                guild, guilds[guildscmpt] = guildSettingsTemp, guild
                                await msg.edit(comfirmGuildSettingsChange)
                            elif saveGuildSettings(pathGuildSettings,guild):
                                await msg.edit(rejectGuildSettingsChange)
                            else:
                                os.remove(pathGuildSettings)
                                await msg.edit(embed = errorEmbed(args[0],corruptNotice))

                            try:
                                await newPrefixe.delete()
                            except:
                                1
                            etat = -10

                        elif etat == 1:
                            if guild.patchnote == str(0):
                                await msg.edit(embed = discord.Embed(title = args[0]+" : Salons de patchnote",color = light_blue,description = f"Aucun salon est n'actuellement défini comme Salon de patchnotes pour le serveur {ctx.guild.name}\nVeuillez mentionner le salon que vous souhaitez définir comme tel"))
                            else:
                                await msg.edit(embed = discord.Embed(title = args[0]+" : Salons de patchnote",color = light_blue,description = f"Le salon de patchnote du serveur {ctx.guild.name} est : **__{bot.get_channel(guild.patchnote)}__**\nVeuillez mentionner le nouveau salon"))

                            newPatchnotes = await bot.wait_for("message",timeout = 60,check = checkIsAuthor)
                            try:
                                newPatchnotes = newPatchnotes.channel_mentions[0].id
                                guildSettingsTemp.patchnote = newPatchnotes
                                if saveGuildSettings(pathGuildSettings,guildSettingsTemp):
                                    await msg.edit(embed = discord.Embed(title = args[0] + " : Salon Patchnote",description =comfirmGuildSettingsChange))
                                elif saveGuildSettings(pathGuildSettings,guild):
                                    await msg.edit(embed = discord.Embed(title = args[0] + " : Salon Patchnote",description =rejectGuildSettingsChange))
                                else:
                                    os.remove(pathGuildSettings)
                                    await msg.edit(embed = errorEmbed(args[0],corruptNotice))
                            except:
                                    await msg.edit(embed = errorEmbed(args[0],errorNotAChannel))
                            try:
                                await newPatchnotes.delete()
                            except:
                                1
                            etat = -10
                                    
                        elif etat == 2:
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
                                        await msg.edit(embed = discord.Embed(title = args[0] + " : Salon Bot",description =comfirmGuildSettingsChange))
                                    elif saveGuildSettings(pathGuildSettings,guild):
                                        await msg.edit(embed = discord.Embed(title = args[0] + " : Salon Bot",description =rejectGuildSettingsChange))
                                    else:
                                        os.remove(pathGuildSettings)
                                        await msg.edit(embed = errorEmbed(args[0],corruptNotice))
                                except:
                                    await msg.edit(embed = errorEmbed(args[0],errorNotAChannel))
                                try:
                                    await repMsg.delete()
                                except:
                                    1
                                etat = -10

                        elif etat == 3:
                            choiceColorRole = ["Désactiver","Activer","Retour"]
                            await msg.edit(embed = discord.Embed(title = args[0]+" : Couleur automatique",color = light_blue,description = f"Lorsque cette option est activée, le bot attribura aux utilisateurs un role Couleur en fonction de la couleur qu'ils auront choisi dans l'Aventure\n\nLors de l'activation, de nouveaux roles seront crées. Par la suite, vous pourrez modifier leur nom ou leur couleur.\nSi il s'agit d'une seconde activation, le bot va recréer que les roles manqaunts.\n\nLors de la désactivation, le bot supprimera les rôles créés.\n\nActuellement, cette option est réglée sur __{(guild.colorRole.enable)}__{choice(choiceColorRole)}"))

                            respond = await bot.wait_for("message",timeout = 60,check = checkIsAuthor)
                            if not respond.content.isdigit():
                                msg.edit(embed = errorEmbed(args[0],errorNotDigitMsg))
                            else:
                                repMsg = respond
                                respond = int(respond.content)
                                if respond > len(choiceSettings) and respond < 0:
                                    await msg.edit(embed = errorEmbed(args[0],errorNotInRangeMsg))
                                elif not(commands.bot_has_guild_permissions(manage_roles = False)):
                                    await msg.edit(embed= errorEmbed(args[0],"Je n'ai pas la permission de gérer les rôles"))
                                elif respond == 1:
                                    await msg.edit(embed = discord.Embed(title = commandArgs(ctx)[0], description = emoji.loading))
                                    discGuild = bot.get_guild(guild.id)
                                    tablId,cmpt = [guild.colorRole.red,guild.colorRole.orange,guild.colorRole.yellow,guild.colorRole.green,guild.colorRole.lightBlue,guild.colorRole.blue,guild.colorRole.purple,guild.colorRole.pink,guild.colorRole.white,guild.colorRole.black],0
                                    for a in range(len(tablId)):
                                        if discGuild.get_role(tablId[a]) == None:
                                            try:
                                                newRole = await discGuild.create_role(name = f"lenapy_{colorChoice[a]}",colour = discord.Colour(colorId[a]))
                                                print(f"Le rôle {newRole.name} a été créé sur le serveur {discGuild.name} (Id : {newRole.id})")
                                                tablId[a] = newRole.id
                                                cmpt += 1
                                            except:
                                                print(f"Echec de création de role sur le serveur {discGuild.name}")
                                        
                                        guild.colorRole.enable, guild.colorRole.red, guild.colorRole.orange, guild.colorRole.yellow,guild.colorRole.green,guild.colorRole.lightBlue,guild.colorRole.blue,guild.colorRole.purple,guild.colorRole.pink = 1,tablId[0],tablId[1],tablId[2],tablId[3],tablId[4],tablId[5],tablId[6],tablId[7]
                                    await msg.edit(embed = discord.Embed(title = args[0] + " : Couleur Automatique",color = light_blue,description = f"{cmpt} nouveau(x) role(s) ont été crées"))
                                    etat = -10

                                elif respond == 0:
                                    discGuild, cmpt = bot.get_guild(guild.id), 0
                                    await msg.edit(embed = discord.Embed(title="Chargement",description="Suppression des roles couleurs"))
                                    for a in discGuild.roles:
                                        for b in [guild.colorRole.red, guild.colorRole.orange, guild.colorRole.yellow,guild.colorRole.green,guild.colorRole.lightBlue,guild.colorRole.blue,guild.colorRole.purple,guild.colorRole.pink,guild.colorRole.white,guild.colorRole.black]:
                                            if a.id == b:
                                                try:
                                                    await a.delete()
                                                    print(f"Le role {a.name} a été supprimé")
                                                    cmpt += 1
                                                except:
                                                    print(f"Le role {a.name} n'a pas pu être supprimé.")
                                    await msg.edit(embed = discord.Embed(title = args[0] + " : Couleur Automatique", color = light_blue, description = f"{cmpt} roles ont été supprimés"))
                                    guild.colorRole.enable = 0
                                    etat = -10

                                elif respond == 2:
                                    etat = -1

                                try:
                                    await repMsg.delete()
                                except:
                                    1
                
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
                            try:
                                pathUserProfile = absPath + "/userProfile/" + a
                                user = loadCharFile(pathUserProfile,ctx)
                                user = restats(user)

                                saveCharFile(pathUserProfile,user)
                                owner = await bot.fetch_user(user.owner)
                                await owner.send(embed = discord.Embed(title = f"{args[0]} {args[1]} {args[2]}",color = user.color,description = f"Votre profil a été restats de force par un administrateur.\n\nVous avez obtenus les statistiques correspondant à votre aspiration et votre niveau et vous avez récupéré vos {user.points} points bonus, que vous pouvez redistribuer à votre guise"))
                                print(f"{user.name} a bien été restat")
                            except:
                                pass

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
                    customIconDB.dropCustomDB()
                    await refresh("Supression des emojis")
                    iconGuildList = []
                    if os.path.exists("../Kawi/"):
                        iconGuildList = ShushyCustomIcons
                    else:
                        iconGuildList = LenaCustomIcons

                    for a in iconGuildList:
                        emojiGuild = await bot.fetch_guild(a)

                        for b in emojiGuild.emojis:
                            await b.delete()

                    await refresh("Création des dossiers...")
                    existDir(absPath + "/data/images/")
                    existDir(absPath + "/data/images/headgears/")
                    existDir(absPath + "/data/images/weapons/")
                    existDir(absPath + "/data/images/char_icons/")
                    await refresh("Création de la base de donnée")
                    base = open("./data/custom_icon.db","w")
                    base.close()
                    customIconDB.remarkeCustomDB()
                    await refresh("Téléchargements des icones d'accessoires...")
                    await downloadAllHeadGearPng(bot)
                    await refresh("Téléchargements des icones d'armes...")
                    await downloadAllWeapPng(bot)
                    await refresh("Téléchargements des icones de bases...")
                    await downloadAllIconPng(bot)
                    await refresh("Fini !")
                elif args[1] == "forceShop":
                    await shopping.newShop()
                    await ctx.add_reaction('❄')

                await ctx.add_reaction(emoji.cat)

                #except:
                    #await ctx.add_reaction('<:LenaWhat:760884455727955978>')

            elif args[0] == guild.prefixe + "choose" and checkIsBotChannel(ctx,guild,bot):
                choBet = []
                temp = ""
                for a in range(1,len(args)-1):
                    for b in args[a]:
                        if b != "|":
                            temp += b
                        else:
                            choBet += [temp]
                            temp = ""
                    temp += " "
                choBet += [temp]

                rep = discord.Embed(title = "**l!choose**",color = light_blue,description = (randRep([chooseMsg1,chooseMsg2,chooseMsg3])+"__"+random.choice(choBet)+"__\n"))
                await ctx.channel.send(embed = rep)

            elif args[0] == guild.prefixe + "start" and checkIsBotChannel(ctx,guild,bot):
                await start(bot,ctx,guild,args)

            elif args[0] == guild.prefixe + "solde" and checkIsBotChannel(ctx,guild,bot):
                pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
                if os.path.exists(pathUserProfile):
                    user = loadCharFile(pathUserProfile,ctx)
                    await ctx.channel.send(embed = discord.Embed(title = "Porte monnaie", description = f"{currenties} {user.currencies} {emoji.coins}",color = user.color))
                else:
                    await ctx.channel.send("Tu n'a pas commencé l'aventure")

            elif args[0] == guild.prefixe + "stats" and checkIsBotChannel(ctx,guild,bot):
                if ctx.mentions == [] and args[1] == None:
                    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
                else:
                    try:
                        pathUserProfile = absPath + "/userProfile/" + str(ctx.mentions[0].id) + ".prof"
                    except:
                        pathUserProfile = absPath + "/userProfile/" + args[1][3:-1] + ".prof"

                if os.path.exists(pathUserProfile):
                    msg = await loadingEmbed(ctx)
                    user = loadCharFile(pathUserProfile,ctx)

                    if os.path.exists("../Kawi/"):
                        iconGuildList = ShushyCustomIcons
                    else:
                        iconGuildList = LenaCustomIcons

                    url_em = None
                    for icGuild in iconGuildList:
                        icGuild = await bot.fetch_guild(icGuild)
                        try:
                            url_em = await icGuild.fetch_emoji(getEmojiObject(await getUserIcon(bot,user))["id"])
                        except:
                            pass

                    if url_em != None:
                        url_em = str(url_em.url)

                    rep = discord.Embed(title = f"__Page de statistique de {user.name}__",color = user.color,description = f"__Niveau :__ {user.level}\n__Expérience :__ {user.exp} / {user.level*50-20}")
                    print(url_em)
                    rep.set_thumbnail(url=url_em)
                    rep.add_field(name = "__Aspiration :__",value = inspi[user.aspiration],inline = False)

                    sumStatsBonus = [0,0,0,0,0,0,0,0,0]

                    for a in [user.weapon,user.stuff[0],user.stuff[1],user.stuff[2]]:
                        sumStatsBonus[0] += a.strength
                        sumStatsBonus[1] += a.endurance
                        sumStatsBonus[2] += a.charisma
                        sumStatsBonus[3] += a.agility
                        sumStatsBonus[4] += a.precision
                        sumStatsBonus[5] += a.intelligence
                        sumStatsBonus[6] += a.resistance
                        sumStatsBonus[7] += a.percing
                        sumStatsBonus[8] += a.critical

                    for a in range(len(sumStatsBonus)):
                        if sumStatsBonus[a] > 0:
                            sumStatsBonus[a] = "+"+str(sumStatsBonus[a])

                    rep.add_field(name = "__Statistiques principaux :__",value = f"Force : {user.strength} ({sumStatsBonus[0]})\nEndurance : {user.endurance} ({sumStatsBonus[1]})\nCharisme : {user.charisma} ({sumStatsBonus[2]})\nAgilité : {user.agility} ({sumStatsBonus[3]})\nPrécision : {user.precision} ({sumStatsBonus[4]})\nIntelligence : {user.intelligence} ({sumStatsBonus[5]})",inline= True)
                    rep.add_field(name = "__Statistiques secondaires :__",value = f"Résistance : {user.resistance} ({sumStatsBonus[6]})\nPénétration d'Armure : {user.percing} ({sumStatsBonus[7]})\nCritique : {user.critical} ({sumStatsBonus[8]})",inline = True)
                    rep.set_thumbnail(url = 'https://cdn.discordapp.com/emojis/866459463568850954.png?v=1')
                    tempStuff,tempSkill = "",""
                    for a in [0,1,2]:
                        tempStuff += f"{ user.stuff[a].emoji} {user.stuff[a].name}\n"

                    for a in [0,1,2,3,4]:
                        try:
                            tempSkill += f"{ user.skills[a].emoji} {user.skills[a].name}\n"
                        except:
                            tempSkill += f"Slot [{a+1}] : Pas de compétence équipée\n"

                    rep.add_field(name = "__Equipement :__",value = f"__Arme :__\n{ user.weapon.emoji} {user.weapon.name}\n\n__Vêtements :__\n{tempStuff}\n__Compétences :__\n{tempSkill}",inline = False)
                    await msg.edit(embed = rep)

                else:
                    await ctx.channel.send("Tu n'a pas commencé l'aventure")

            elif args[0] == guild.prefixe + "inventory" and checkIsBotChannel(ctx,guild,bot):
                await inventory(bot,ctx,args)

            elif args[0] == guild.prefixe + "points" and checkIsBotChannel(ctx,guild,bot):
                await points(bot,ctx,args)

            elif args[0] == guild.prefixe + "invite" and checkIsBotChannel(ctx,guild,bot):
                if os.path.exists("../Kawi/"):
                    await ctx.channel.send(embed = discord.Embed(title = args[0],color = light_blue,url = 'https://canary.discord.com/api/oauth2/authorize?client_id=769999212422234122&permissions=1074097216&scope=bot%20applications.commands'))
                else:
                    await ctx.channel.send(embed = discord.Embed(title = args[0],color = light_blue,url = 'https://canary.discord.com/api/oauth2/authorize?client_id=623211750832996354&permissions=1074129984&scope=bot%20applications.commands'))

            elif args[0] == guild.prefixe + "help" and checkIsBotChannel(ctx,guild,bot):
                msg,etat = await loadingEmbed(ctx), 0
                def checkIsAuthor(message):
                    return message.channel.id == ctx.channel.id and message.author.id == ctx.author.id

                while etat >=0:
                    if etat == 0:
                        choiceMain = ["Modération","Utilitaire","Aventure"]
                        await msg.edit(embed= discord.Embed(title = args[0],color = 0x94d4e4, description = "Voici les principales catégories de commandes :"+choice(choiceMain)))
                        respond = await bot.wait_for("message",timeout=60,check=checkIsAuthor)

                        if not respond.content.isdigit():
                                await msg.edit(embed = errorEmbed(args[0],errorNotDigitMsg))
                                etat = -1
                        else:
                            repMsg = respond
                            respond = int(respond.content)
                            if respond < len(choiceMain) and respond >= 0:
                                etat = respond+1
                            else:
                                await msg.edit(embed = errorEmbed(args[0],errorNotInRangeMsg))
                                etat = -1

                            try:
                                await repMsg.delete()
                            except:
                                1
                            
                    else:
                        choiceMain = [""]+choiceMain
                        choiceMod = ["settings","Retour"]
                        choiceUt = ["choose","invite","Retour"]
                        choiceAdv = ["start","stats","solde","inventory","points","shop","team","fight","quickFight","octogone","teamFight","procuration","Retour"]

                        tablChoice = ["",choiceMod,choiceUt,choiceAdv]
                        tablCat = ["","Voici les commandes de modération :","Voici les commandes utilitaires :","Voici les commandes de l'Aventure"]
                        await msg.edit(embed= discord.Embed(title = args[0]+" : "+choiceMain[etat],color = light_blue, description = tablCat[etat]+choice(tablChoice[etat])))
                        respond = await bot.wait_for("message",timeout=60,check=checkIsAuthor)

                        if not respond.content.isdigit():
                                await msg.edit(embed = errorEmbed(args[0],errorNotDigitMsg))
                        else:
                            repMsg = respond
                            respond = int(respond.content)
                            if not(respond < len(tablChoice[etat]) and respond >= 0):
                                await msg.edit(embed = errorEmbed(args[0],errorNotInRangeMsg))
                                etat = -1
                            else:
                                tablDes = ["",tablDescMod,tablDescUt,tablDescAdv]
                                if respond == len(tablDes[etat]):
                                    etat = 0
                                    try:
                                        await repMsg.delete()
                                    except:
                                        1
                                else:
                                    try:
                                        await repMsg.delete()
                                    except:
                                        1

                                    await msg.edit(embed = discord.Embed(title = args[0]+ " : "+tablChoice[etat][respond],color = light_blue,description = tablDes[etat][respond]))
                                    etat = -1
  
            elif args[0] == guild.prefixe + "team" and checkIsBotChannel(ctx,guild,bot):
                pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"

                if os.path.exists(pathUserProfile):
                    user = quickLoadCharFile(pathUserProfile)
                    Qsave = user[1]
                    user = user[0]
                    pathTeam = absPath + "/userTeams/" + user.team +".team"
                    if args[1] == None:
                        msg = await loadingEmbed(ctx)
                        if user.team == "0":
                            await msg.edit(embed = discord.Embed(title = args[0],color = user.color,description = "Vous n'avez pas d'équipe pour le moment"))
                        else:
                            file = readSaveFiles(pathTeam)
                            if len(file[0]) == 1:
                                await msg.edit(embed = discord.Embed(title = args[0],color = user.color,description = "Vous êtes seul dans votre équipe pour le moment"))
                            else:
                                temp = ""
                                for a in file[0]:
                                    temp2 = loadCharFile(absPath + "/userProfile/" + a + ".prof")
                                    temp3 = "L'utilisateur n'a pas parlé depuis la mise en ligne du bot"

                                    temp3 = await bot.fetch_user(int(a))
                                    temp3 = temp3.name

                                    ballerine = f'{inspi[temp2.aspiration][0:3]}. | {elemEmojis[temp2.element]} | {temp2.weapon.emoji} | {temp2.stuff[0].emoji} {temp2.stuff[1].emoji} {temp2.stuff[2].emoji} | '
                                    for b in temp2.skills:
                                        if type(b)==skill:
                                            ballerine+=b.emoji
                                    ballerine+="\n\n"

                                    icon = await getUserIcon(bot,temp2)
                                    temp += f"__{icon} **{temp2.name}** ({temp3})__\n{ballerine}"
                                await msg.edit(embed = discord.Embed(title = args[0],color = user.color,description = "__Votre équipe se compose de :__\n\n"+temp))

                    if args[1] == "up":
                        msg = await loadingEmbed(ctx)
                        if not(os.path.exists(pathTeam) and user.team != "0"):
                            rdm = str(random.randint(1,10000))
                            pathTeam = absPath + "/userTeams/" + rdm +".team"
                            rewriteFile(pathTeam,f"{str(user.owner)};")
                            user.team = rdm
                            quickSaveCharFile(pathUserProfile,[user,Qsave])

                        noneCap,selfAdd,temp = True,False,readSaveFiles(absPath + "/userTeams/" + user.team +".team")
                        
                        if len(temp[0]) >= 8:
                            noneCap = False      

                        if ctx.author == ctx.mentions[0]:
                            selfAdd = True          

                        if noneCap and not(selfAdd):
                            mention = ctx.mentions[0]
                            if os.path.exists(absPath + "/userProfile/" + str(mention.id) + ".prof"):
                                allReadyinTeam,allReadyInThatTeam,mate = False, False,quickLoadCharFile(absPath + "/userProfile/" + str(mention.id) + ".prof")
                                
                                if mate[0].team != "0":
                                    allReadyinTeam = True
                                    if mate[0].team == user.team:
                                        allReadyInThatTeam = True


                                if not(allReadyinTeam):
                                    await msg.edit(embed = discord.Embed(title = args[0]+ " "+args[1], color = user.color, description = f"{mention.mention}, {ctx.author.mention} vous propose de rejoidre son équipe. Qu'en dites vous ?"))
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
                                            await msg.edit(embed = discord.Embed(title=args[0]+ " "+args[1],color = user.color,description = "Vous faites dorénavent parti de la même équipe"))
                                    except:
                                        await msg.clear_reactions()
                                
                                elif allReadyInThatTeam:
                                    await msg.edit(embed = errorEmbed(args[0]+ " "+args[1],"Ce joueur est déjà dans ton équipe"))
                                elif allReadyinTeam:
                                    await msg.edit(embed = errorEmbed(args[0]+ " "+args[1],"Ce joueur est déjà dans une équipe"))

                            else:
                                await msg.edit(embed = errorEmbed(args[0]+ " "+args[1],"Cet utilisateur n'a pas commencé l'aventure"))  
                        
                        elif selfAdd:
                            await msg.edit(embed = errorEmbed(args[0]+ " "+args[1],"Tu veux te rajouter toi-même dans ta propre équipe ?"))
                        elif not(noneCap):
                            await msg.edit(embed = errorEmbed(args[0]+ " "+args[1],"Votre équipe a déjà atteint son nombre maximal de membre"))

                    elif args[1] == "quit":
                        if user.team != "0":
                            team = readSaveFiles(pathTeam)
                            team[0].remove(str(ctx.author.id))
                            user.team = "0"

                            saveSaveFiles(pathTeam,team)
                            await ctx.channel.send(embed = discord.Embed(title = args[0]+ " "+args[1],color = user.color, description = "Vous avez bien quitté votre équipe"))

                        else:
                            await ctx.channel.send(embed = errorEmbed(args[0]+ " "+args[1],"Vous n'avez aucune équipe à quitter"))
                    quickSaveCharFile(pathUserProfile,[user,Qsave])

            elif args[0] == guild.prefixe + "shop" and checkIsBotChannel(ctx,guild,bot):
                await shop2(bot,ctx,shopping.shopping)

            elif args[0] == guild.prefixe + "fight" and checkIsBotChannel(ctx,guild,bot):
                pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
                user = loadCharFile(pathUserProfile,ctx)
                ballerine,trouv,temp = 0,False,0
                if user.team == 0:
                    ballerine = user.owner
                else:
                    ballerine = user.team

                cooldownOk = True
                timing = teamWinDB.getFightCooldown(ballerine)
                if timing > 0:
                    cooldownOk = False

                if cooldownOk and not(teamWinDB.isFightingBool(ballerine)):
                    teamWinDB.changeFighting(ballerine,True)
                    team1 = []
                    if user.team != 0:
                        file = readSaveFiles(absPath + "/userTeams/" + str(user.team) + ".team")
                        for a in file[0]:
                            team1 += [loadCharFile(absPath + "/userProfile/" + a + ".prof")]
                    else:
                        team1 = [user]

                    await fight(bot,team1,[],ctx,guild,False)

                elif teamWinDB.isFightingBool(ballerine):
                    await ctx.channel.send(embed = errorEmbed(args[0],"Vous êtes déjà en train de vous battre"))
                else:
                    await ctx.channel.send(embed = errorEmbed("Cooldown",f"Votre équipe ne pourra faire de combats normaux que dans {timing//60} minute(s)"))

            elif args[0] == guild.prefixe + "quickFight" and checkIsBotChannel(ctx,guild,bot):
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

                    await fight(bot,team1,[],ctx,guild)

                elif teamWinDB.isFightingBool(ballerine):
                    await ctx.channel.send(embed = errorEmbed(args[0],"Vous êtes déjà en train de vous battre"))
                else:
                    await ctx.channel.send(embed = errorEmbed("Cooldown",f"Votre équipe ne pourra faire de combats normaux que dans {timing//60} minute(s)"))

            elif args[0] == guild.prefixe + "octogone":
                pathUserProfile,ballerine = absPath + "/userProfile/" + str(ctx.author.id) + ".prof",""
                if os.path.exists(pathUserProfile):
                    if not(checkIsBotChannel(ctx,guild,bot)) and ctx.author.id == 213027252953284609:
                        ballerine = "Tu va te calmer Léna, tu es pas dans le bon salon pour octogone quelqu'un"
                        if not(os.path.exists(absPath + "/userProfile/" + ctx.mentions[0].id + ".prof")):
                            ballerine += f"\nEn plus {ctx.mentions[0].name} n'a même pas commencé l'aventure"
                    elif checkIsBotChannel(ctx,guild,bot) and ctx.author.id == 213027252953284609 and not(os.path.exists(absPath + "/userProfile/" + str(ctx.mentions[0].id) + ".prof")) and not((ctx.mentions[0].id in [623211750832996354,769999212422234122])):
                        ballerine = f'{ctx.mentions[0].name} n\'a pas commencé l\'aventure Léna'

                    elif checkIsBotChannel(ctx,guild,bot) and os.path.exists(absPath + "/userProfile/" + str(ctx.mentions[0].id) + ".prof"):
                        await fight(bot,[loadCharFile(pathUserProfile)],[loadCharFile(absPath + "/userProfile/" + str(ctx.mentions[0].id) + ".prof")],ctx,guild,auto=False,octogone=True)

                    elif checkIsBotChannel(ctx,guild,bot) and (ctx.mentions[0].id in [623211750832996354,769999212422234122]):
                        temp = loadCharFile(pathUserProfile)
                        tempi = tablAllAllies[0]
                        tempi.changeLevel(temp.level)
                        await fight(bot,[temp],[tempi],ctx,guild,auto=False,octogone=True)

                    elif checkIsBotChannel(ctx,guild,bot):
                        await ctx.channel.send(f"{ctx.mentions[0].name} n'a pas commencé l'aventure")
                    else:
                        await ctx.channel.send("ok")

                    if ballerine != "":
                        await ctx.channel.send(ballerine)

            elif args[0] == guild.prefixe + "manuel" and checkIsBotChannel(ctx,guild,bot):
                msg,manPage,chapterInt = await loadingEmbed(ctx),0,0
                if args[1] != None and args[1].isdigit():
                    manPage = int(args[1])
                def checkReaction(reaction, user):
                    return reaction.message == msg and user == ctx.author and (str(reaction) == emoji.backward_arrow or str(reaction) == emoji.forward_arrow or str(reaction) == '⏪' or str(reaction) == '⏩') 
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
                    await msg.add_reaction('⏪')
                    await msg.add_reaction(emoji.backward_arrow)
                    await msg.add_reaction(emoji.forward_arrow)
                    await msg.add_reaction('⏩')

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
                                print(chapterInt,lenChapter[len(lenChapter)-1])
                                manPage = lenChapter[len(lenChapter)-1]
                            else:
                                manPage = lenChapter[chapterInt]
                        
                        elif str(reaction[0]) == '⏩':
                            print(chapterInt,len(lenChapter)-1)
                            if chapterInt==len(lenChapter)-1:
                                manPage = 0
                            else:
                                print(lenChapter[chapterInt+1])
                                manPage = lenChapter[chapterInt+1]


                        await msg.remove_reaction(str(reaction[0]),reaction[1])

            elif args[0] == "l!test" and ctx.author.id == 213027252953284609:
                pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
                if os.path.exists(pathUserProfile):
                    user = loadCharFile(pathUserProfile,ctx)
                    userAchiv = achivement.getSuccess(user)
                    for a in userAchiv.tablAllSuccess():
                        a = a.toDict()
                        print(a["name"],a["count"])
     
            elif args[0] == guild.prefixe + "teamFight" and checkIsBotChannel(ctx,guild,bot):
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
                    pathOctogonedProfile = absPath + "/userProfile/" + str(ctx.mentions[0].id) + ".prof"
                    if os.path.exists(pathOctogonedProfile):
                        octogoned = loadCharFile(pathOctogonedProfile,ctx)
                        if octogoned.team != 0:
                            file = readSaveFiles(absPath + "/userTeams/" + str(octogoned.team) + ".team")
                            for a in file[0]:
                                team2 += [loadCharFile(absPath + "/userProfile/" + a + ".prof")]
                        else:
                            team2 = [octogoned]

                        await fight(bot,team1,team2,ctx,guild,False,octogone=True)
                    else:
                        await ctx.channel.send("L'utilisateur mentioné n'a pas commencé l'aventure")
                else:
                    await ctx.channel.send("Tu n'as pas commencé l'aventure")
        
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
                    if type(a) != int:
                        ballerine = await bot.fetch_guild(a.id)
                        if ballerine != None:
                            guildSettings = readSaveFiles(absPath + "/guildSettings/"+str(ballerine.id)+".set")
                            babie = server(int(ballerine.id),guildSettings[0][0],int(guildSettings[0][1]),int(guildSettings[0][2]))
                            if babie.patchnote != 0:
                                chan = await bot.fetch_channel(babie.patchnote)
                                await chan.send(get_patchnote())
                            elif babie.bot != 0:
                                chan = await bot.fetch_channel(babie.bot)
                                await chan.send(embed=discord.Embed(title="/patchnote",color=light_blue,description="Un nouveau patchnote est disponible, vous pouvez le voir à l'aide de /patchnote\n\n*Note : Les nouvelles commandes slash peuvent mettre jusqu'à 1 heure pour apparaitre sur vos serveur*"))

        else:
            pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
            if os.path.exists(pathUserProfile) and len(ctx.content)>=3:
                #try:
                await addExpUser(bot,guild,pathUserProfile,ctx,3,len(set(ctx.content)))
                """except:
                    print(f"Une erreur est survenue sur le message de {ctx.author.name}")"""

# encyclopedia
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

# encyclopedia-test
@slash.slash(name="encyclopedia_test",guild_ids = [615257372218097691],description="Vous permet de consulter l'encyclopédie", options=[
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

# fight
@slash.slash(name="fight",description="Vous permet de faire un combat normal")
async def comFight(ctx):
    try:
        pathGuildSettings = absPath + "/guildSettings/"+str(ctx.guild.id)+".set"
    except:
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
                break

    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    user = loadCharFile(pathUserProfile,ctx)
    ballerine,trouv,temp = 0,False,0
    if user.team == 0:
        ballerine = user.owner
    else:
        ballerine = user.team

    cooldownOk = True
    timing = teamWinDB.getFightCooldown(ballerine)
    if timing > 0:
        cooldownOk = False

    if cooldownOk and not(teamWinDB.isFightingBool(ballerine)):
        teamWinDB.changeFighting(ballerine,True)
        team1 = []
        if user.team != 0:
            file = readSaveFiles(absPath + "/userTeams/" + str(user.team) + ".team")
            for a in file[0]:
                team1 += [loadCharFile(absPath + "/userProfile/" + a + ".prof")]
        else:
            team1 = [user]

        await fight(bot,team1,[],ctx,guild,False,slash=True)

    elif teamWinDB.isFightingBool(ballerine):
        msg = await ctx.send(embed = errorEmbed(args[0],"Vous êtes déjà en train de vous battre"))
        await asyncio.sleep(10)
        await msg.delete()
    else:
        msg = await ctx.send(embed = errorEmbed("Cooldown",f"Votre équipe ne pourra faire de combats normaux que dans {timing//60} minute(s)"))
        await asyncio.sleep(10)
        await msg.delete()

# quickFight
@slash.slash(name="quickFight",description="Vous permet de faire un combat en sautant directement à la fin")
async def comQuickFight(ctx):
    try:
        pathGuildSettings = absPath + "/guildSettings/"+str(ctx.guild.id)+".set"
    except:
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
                break
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

        await fight(bot,team1,[],ctx,guild,slash=True)

    elif teamWinDB.isFightingBool(ballerine):
        msg = await ctx.send(embed = errorEmbed(args[0],"Vous êtes déjà en train de vous battre"))
        await asyncio.sleep(10)
        await msg.delete()
    else:
        msg = await ctx.send(embed = errorEmbed("Cooldown",f"Votre équipe ne pourra faire de combats normaux que dans {timing//60} minute(s)"))
        await asyncio.sleep(10)
        await msg.delete()

# cooldown
@slash.slash(name="cooldowns",description="Vous donne les cooldowns des commandes /fight et /quickFight pour votre équipe")
async def cooldowns(ctx):
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile,ctx)
        fcooldown,fseconds,fqcooldown,fqseconds,faccord,fqaccord,fsaccord,fqsaccord = teamWinDB.getFightCooldown(user.team)//60,teamWinDB.getFightCooldown(user.team)%60,teamWinDB.getFightCooldown(user.team,True)//60,teamWinDB.getFightCooldown(user.team,True)%60,"","","",""
        if fcooldown > 1:
            faccord = "s"
        if fqcooldown > 1:
            fqaccord = "s"
        if fseconds > 1:
            fsaccord = "s"
        if fqseconds > 1:
            fqsaccord = "s"
        msg = await ctx.send(embed = discord.Embed(title=f"__Cooldowns de l'équipe :__",description=f"__Fight__ : {fcooldown} minute{faccord} et {fseconds} seconde{fsaccord}\n__QuickFight__ : {fqcooldown} minute{fqaccord} et {fqseconds} seconde{fqsaccord}",color=user.color))
        await asyncio.sleep(10)
        await msg.delete()

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

###########################################################
# Démarrage du bot
if os.path.exists("../Kawi/"):
    print("Kawiiiiii")
    bot.run("=)")
else:
    print("Il semblerait que je sois seule cette fois. Je m'occuperais de Shushi une autre fois")
    bot.run("=]")