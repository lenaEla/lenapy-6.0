##########################################################
# Importations :
import asyncio
import datetime
import os
import random
import shutil
import sys

from discord.ext import tasks
from interactions import *

from adv import *
from advance_gestion import *
from classes import *
from commands_files.alice_stats_endler import *
from commands_files.command_encyclopedia import *
from commands_files.command_expedition import *
from commands_files.command_fight import *
from commands_files.command_help import *
from commands_files.command_inventory import *
from commands_files.command_patchnote import *
from commands_files.command_points import *
from commands_files.command_procuration import *
from commands_files.command_shop import *
from commands_files.command_start import *
from commands_files.sussess_endler import *
from commands_files.cmd_twitch import *
from data.bot_tokens import lenapy, shushipy
from data.database import *
from donnes import *
from gestion import *
from datetime import datetime

###########################################################
# Initialisations des variables de bases :
started = False
slash = setup(interactions.Client(token=[shushipy,lenapy][isLenapy],intents=interactions.Intents(Intents.ALL)))

existDir(absPath + "/userProfile/")
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

actualyFight, actualyQuickFight = [], []
pathUserProfile = absPath + "/userProfile/"

###########################################################
# Initialisation
allShop = weapons + skills + stuffs + others

class shopClass:
    """The class who endle the shop\n
    Maybe I should shearch how it's writed...
    """

    def __init__(self, shopList: list = []):
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
            for a in range(0, len(shopList)):
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
            shopping = list(range(0, len(self.shopping)))

            if globalVar.fightEnabled():
                babies = datetime.now() + horaire + timedelta(hours=1)
                while babies.hour % 3 != 0:
                    babies = babies + timedelta(hours=1)

                await slash.change_presence(ClientPresence(status=StatusType.ONLINE,activities=[PresenceActivity(name="Prochain shop à "+babies.strftime('%Hh'),type=PresenceActivityType.GAME)]))

            shopWeap, shopSkill, shopStuff, ShopOther = [], [], [], others[:]
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
            tablShop: List[list[Union[weapon, skill, stuff, other]]] = [
                shopWeap, shopSkill, shopStuff, ShopOther]
            cmp = 0
            for a in [0, 1, 2, 3]:
                cmpt = 0
                while cmpt < temp[a]:
                    fee = random.randint(0, len(tablShop[a])-1)
                    shopping[cmp] = tablShop[a][fee]
                    tablShop[a].remove(tablShop[a][fee])
                    cmpt += 1
                    cmp += 1

            temp = ""
            stuffDB.addShop(shopping)
            for a in shopping:
                temp += f"\n{a.name}"

            print("\n--------------\nLe nouveau shop est :"+temp+"\n------------")
            self.shopping = shopping
            return True
        except:
            return False

async def inventoryVerif(slash, toVerif: Union[char, str]):
    if type(toVerif) == str:
        user = loadCharFile(absPath + "/userProfile/" + toVerif)
    else:
        user = toVerif
    aliceStatsDb.addUser(user)
    allReadySee, haveUltimate, modifSkill, modifStuff = [], False, 0, 0
    ballerine = "Une ou plusieurs compétences ont été déséquipés de votre personnage :\n"
    babie = "Un ou plusieurs équipements ont été retiré de votre inventaire :\n"

    for a in range(0, 7):
        if type(user.skills[a]) == skill:
            if user.skills[a] in allReadySee:
                ballerine += f"\n__{user.skills[a].name}__ (Doublon)"
                modifSkill += 1
                user.skills[a] = "0"
            else:
                allReadySee += [user.skills[a]]

            if user.skills[a] != "0" and not(user.skills[a].havConds(user=user)):
                ballerine += f"\n__{user.skills[a].name}__ (Conditions non respectées)"
                modifSkill += 1
                user.skills[a] = "0"

            if user.skills[a] != "0" and user.skills[a].ultimate and haveUltimate:
                ballerine += f"\n__{user.skills[a].name}__ (Plus de 1 compétence ultime équipée)"
                modifSkill += 1
                user.skills[a] = "0"
            elif user.skills[a] != "0" and user.skills[a].ultimate:
                haveUltimate = True

            if user.skills[a] != "0" and lvlToUnlockSkill[a] > user.level:
                ballerine += f"\n__{user.skills[a].name}__ (Emplacement non débloqué)"
                modifSkill += 1
                user.skills[a] = "0"

    tablInventory = [user.weaponInventory, user.skillInventory,
                     user.stuffInventory, user.otherInventory]
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
        user.weaponInventory, user.skillInventory, user.stuffInventory, user.otherInventory = tablInventory[
            0], tablInventory[1], tablInventory[2], tablInventory[3]
        babie += "\n\nCes objets vous ont été remboursés"

    if modifSkill+modifStuff > 0:
        saveCharFile(user=user)
        try:
            toUser = await get(slash,interactions.User,object_id=user.owner)
            message = ""
            if modifSkill > 0:
                message += ballerine+"\n"
            if modifStuff > 0:
                message += babie
            await toUser.send(embeds=interactions.Embed(title="__Problème lors de la vérification automatique de l'inventaire__", color=user.color, description=message))
        except:
            pass

        print(f"Le profil de {user.name} a été mise à jour")

    temp = ""

    for equip in user.stuff:
        if equip == None:
            for a in (0, 1, 2):
                if user.stuff[a] == None:
                    user.stuff[a] = [bbandeau, bshirt, bshoes][a]
                    temp += "<:LenaWhat:760884455727955978> __Objet non trouvé__ -> {0} {1}\n".format(
                        [bbandeau, bshirt, bshoes][a].emoji, [bbandeau, bshirt, bshoes][a].name)
        elif not(equip.havConds(user)):
            change = getAutoStuff(equip, user)
            user.stuff[equip.type] = change

            temp += "{0} {2} -> {1} {3}\n".format(
                equip.emoji, change.emoji, equip.name, change.name)

    if temp != "":
        temp = "Vous ne respectez pas les conditions de niveaux d'un ou plusieurs de vos équipements\nLe(s) équipement(s) suivant a(ont) automatiquement été remplacé(s) :\n\n"+temp
        saveCharFile(user=user)
        try:
            toUser = await get(slash,interactions.User,object_id=user.owner)
            await toUser.send(embeds=interactions.Embed(title="__Problème lors de la vérification automatique de l'inventaire__", color=user.color, description=temp))
        except:
            pass

        print(f"Le profil de {user.name} a été mise à jour")

    userAchivments = achivement.getSuccess(user)
    tempMissingAchivRecompMsg = ""
    for ach in userAchivments.tablAllSuccess():
        if ach.haveSucced and ach.recompense != [None] and ach.recompense not in [["qe"], ["qh"]]:
            for rec in ach.recompense:
                whatty = whatIsThat(rec)
                obj = [findWeapon(rec), findSkill(rec), findStuff(rec)][whatty]

                if not(user.have(obj)):
                    if whatty == 0:
                        user.weaponInventory.append(obj)
                    elif whatty == 1:
                        user.skillInventory.append(obj)
                    elif whatty == 2:
                        user.stuffInventory.append(obj)

                    tempMissingAchivRecompMsg += "\n{0} {1} ({2})".format(
                        obj.emoji, obj.name, ach.name)
            saveCharFile("./userProfile/{0}.prof".format(user.owner), user)

    if tempMissingAchivRecompMsg != "":
        try:
            toUser = await get(slash,interactions.User,object_id=user.owner)
            await toUser.send(embeds=interactions.Embed(title="__Problème lors de la vérification automatique de l'inventaire__", color=user.color, description="Une ou plusieurs récompenses de succès n'ont pas été trouvées dans votre inventaire et vous ont été restituée :\n"+tempMissingAchivRecompMsg))
            print("{0} n'avait pas toutes ces récompenses de succès".format(user.name))
        except:
            pass

    if user.level > 55:
        user = loadCharFile(user=user)
        user.level, user.exp = 55, 0
        user = restats(user)

        saveCharFile(user=user)

        toSend = await get(slash,interactions.User,object_id=user.owner)

        try:
            await toSend.send(embeds=interactions.Embed(title="__Problème lors de la vérification automatique de votre inventaire :__", description="Votre niveau est supérieur au niveau maximal, et à été ramené à ce dernier\nVos points bonus ont été rénitialisées\n\nPensez à faire un tour vers /prestige", color=light_blue))
        except:
            pass

bidule = stuffDB.getShop()
if bidule != False:
    shopping = shopClass(bidule["ShopListe"])
else:
    shopping = shopClass(False)
    shopping.newShop()

async def restart_program(bot: interactions.Client, ctx=None):
    """If no teams are into a fight, restart the bot\n
    If a team fighting, wiat for them to finish then restart the bot"""
    if ctx != None:
        msg = await ctx.send(embeds=interactions.Embed(title="Redémarrage en attente...", description="Vérifications des équipes en combat..."))
    else:
        chan = await get(slash,interactions.Channel,object_id=912137828614426707)
        msg = await chan.send(embeds=interactions.Embed(title="Redémarrage automatique en attente...", description="Vérifications des équipes en combat..."))
    globalVar.changeFightEnabled(False)
    await slash.change_presence(status=ClientPresence(status=StatusType.DND,activities=[PresenceActivity(name="Attendre la fin des combats",type=PresenceActivityType.GAME)]))

    globalVar.getRestartMsg(int(msg.id))
    fighting = True
    firstIt = True
    while fighting:
        fighting = False
        for team in userTeamDb.getAllTeamIds():
            if teamWinDB.isFightingBool(team)[0]:
                if firstIt:
                    teamTemp = userTeamDb.getTeamMember(team)
                    us = await get(slash,interactions.User,object_id=teamTemp[0])
                    await msg.edit(embeds=interactions.Embed(title="Redémarrage en attente...", description="Un combat est encore en cours <a:loading:862459118912667678> ({0})".format(us.mention)))
                    firstIt = False
                fighting = True
                break
        if fighting:
            await asyncio.sleep(3)

    await msg.edit(embeds=interactions.Embed(title="Redémarrage en attente...", description="Redémarrage en cours..."))
    await slash.change_presence(ClientPresence(status=StatusType.IDLE,activities=[PresenceActivity(name="Redémarrer...",type=PresenceActivityType.GAME)]))

    args = sys.argv[:]

    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]
    os.execv(sys.executable, args)

def create_backup():
    """Copy all the characters profiles files into a new directory\n
    Return a ``string`` with the path of the backup directory"""
    now = datetime.now()
    nowStr = now.strftime("%Y%m%d_%H%M")
    path = "./data/backups/"+nowStr 
    try:
        os.mkdir(path)
    except:
        pass

    for charFile in os.listdir("./userProfile/"):
        shutil.copy('./userProfile/{0}'.format(charFile), path+"/"+charFile)

    return "Un backup a été sauvegardé à la destinaiton suivante :\n"+path

def delete_old_backups():
    """Remove backups directorys older than 3 days"""
    now = datetime.now()
    temp = ""
    for name in os.listdir("./data/backups/"):
        timeBUp = datetime.strptime(name, "%Y%m%d_%H%M")
        if now > timeBUp+timedelta(days=3):
            for files in os.listdir("./data/backups/{0}/".format(name)):
                os.remove("./data/backups/{0}/{1}".format(name, files))
            try:
                os.removedirs("./data/backups/{0}".format(name))
                temp += "./data/backups/{0} a été supprimé\n".format(name)
            except:
                temp += "./data/backups/{0} n'a pas pu être supprimé\n".format(
                    name)
    return temp

async def remakeEmojis(ctx=None):
    if ctx != None:
        msg = await ctx.send(embeds=interactions.Embed(title="Remake des emojis..."))
    else:
        chan = await get(slash,interactions.Channel,object_id=912137828614426707)
        msg = await chan.send(embeds=interactions.Embed(title="Remake des emojis..."))

    await slash.change_presence(ClientPresence(status=StatusType.IDLE,activities=[PresenceActivity(name="Refaire les émojis...",type=PresenceActivityType.GAME)]))

    async def refresh(text: str):
        await msg.edit(embeds=interactions.Embed(title="Remake des emojis...", description=text))

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
        emojiGuild = await get(slash,interactions.Guild,a)
        allEmojisNum += len(emojiGuild.emojis)

    cmpt = 0
    now = datetime.now().second
    lastTime = copy.deepcopy(now)
    for a in iconGuildList:
        emojiGuild = await get(slash,interactions.Guild,a)

        for b in emojiGuild.emojis:
            try:
                print("Emoji de {0} supprimé".format(b.name))
            except:
                pass
            await b.delete()
            await asyncio.sleep(0.5)
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
        await makeCustomIcon(slash, user)
        cmpt += 1

        if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
            await refresh("Création des émojis ({0} %)".format(int(cmpt/lenAllChar*100)))
            lastTime = now

    await refresh("Fini !")
    if ctx != None:
        await ctx.channel.send("Le remake des emojis est terminées !")

    ballerine = datetime.now() + horaire + timedelta(hours=1)
    while ballerine.hour % 3 != 0:
        ballerine = ballerine + timedelta(hours=1)

    await slash.change_presence(ClientPresence(status=StatusType.ONLINE,activities=[PresenceActivity(name="Prochain shop à "+ballerine.strftime('%Hh'),type=PresenceActivityType.GAME)]))

async def verifEmojis(ctx=None):
    if ctx != None:
        msg = await ctx.send(embeds=interactions.Embed(title="Vérification des émojis...", description="__Progression :__ 0%"))
    else:
        chan = await get(slash,interactions.Channel,912137828614426707)
        msg = await chan.send(embeds=interactions.Embed(title="Vérification des émojis...", description="__Progression :__ 0%"))
    remaked, lastProgress = "", 0
    listAllUsersFiles = os.listdir("./userProfile/")
    lenAllUser, progress = len(listAllUsersFiles), 0
    try:
        for path in listAllUsersFiles:
            user, haveSucced = loadCharFile("./userProfile/"+path), False
            userIcon = await getUserIcon(slash, user)
            haveSucced = False
            for guildId in [ShushyCustomIcons, LenaCustomIcons][isLenapy]:
                guild = await get(slash,interactions.Guild,guildId)
                try:
                    await get(slash, interactions.Emoji, parent_id=int(guild.id), object_id=getEmojiObject(userIcon).id)
                    haveSucced = True
                    break
                except:
                    pass
            if not(haveSucced):
                customIconDB.removeUserIcon(user)
                await makeCustomIcon(slash, user)
                if await getUserIcon(slash, user) not in ['<:LenaWhat:760884455727955978>', '<a:lostSilver:917783593441456198>']:
                    remaked += "Emoji de {0} refait\n".format(user.name)
                else:
                    remaked += "Erreur lors du remake de l'emoji de {0}\n".format(
                        user.name)
            progress += 1

            if progress/lenAllUser * 100 > lastProgress + 5:
                await msg.edit(embeds=interactions.Embed(title="Vérification des émojis...", description="__Progression :__ {0}%\n".format(round(progress/lenAllUser * 100, 2))+remaked))
                lastProgress = progress/lenAllUser * 100

        await msg.edit(embeds=interactions.Embed(title="Vérification des émojis", description="__Progression :__ Terminé\n"+remaked, color=light_blue))
    except:
        await msg.edit(embeds=interactions.Embed(title="Vérification des émojis", description="__Interrompue__\n"+format_exc(), color=red))

@tasks.loop(seconds=1)
async def oneClock():
    """A simple clock who check every second if a minute have passed\n
    If it is the case, start ``minuteClock``"""
    tick = datetime.now()
    if tick.second % 60 == 0 and not(minuteClock.is_running()):
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
    tick = datetime.now()
    if tick.minute % 60 == 0 and not(hourClock.is_running()):
        hourClock.start()

@tasks.loop(hours=1)
async def hourClock():
    if minuteClock.is_running():
        minuteClock.stop()
    tick = datetime.now()+horaire
    if tick.hour % 3 == 0:
        temp = False
        while not(temp):
            temp = await shopping.newShop()

    elif tick.hour == 4:
        chan = await get(slash,interactions.Channel,912137828614426707)
        if tick.day == 19:
            chan = await get(slash,interactions.Channel,912137828614426707)
            await chan.send(embeds=interactions.Embed(title="__Reset des records__", color=light_blue, description=aliceStatsDb.resetRecords()))
        for log in os.listdir("./data/fightLogs/"):
            try:
                os.remove("./data/fightLogs/"+log)
                print("{0} supprimé".format("./data/fightLogs/"+log))
            except:
                print("{0} n'a pas pu être supprimé".format(
                    "./data/fightLogs/"+log))
        await chan.send(embeds=interactions.Embed(title="__Suppression des logs__", color=light_blue, description="Les logs de combats ont été supprimés"))
        await chan.send(embeds=interactions.Embed(title="__Auto backup__", color=light_blue, description=create_backup()))
        temp = delete_old_backups()
        if temp != "":
            await chan.send(embeds=interactions.Embed(title="__Auto backup__", color=light_blue, description=temp))
        await verifEmojis()

        for userPath in os.listdir("./userProfile/"):
            user = loadCharFile('./userProfile/{0}'.format(userPath))
            aliceStatsDb.updateJetonsCount(user, max(0,9-(userShopPurcent(user)//10)))
        await restart_program(bot)

    # Skill Verif
    for filename in os.listdir("./userProfile/"):
        await inventoryVerif(slash, filename)

@tasks.loop(seconds=5)
async def twitchAlertLoop():
    await verifStreamingStreamers(bot)

# -------------------------------------------- ON READY --------------------------------------------
@slash.event
async def on_ready():
    print("\n---------\nThe bot is fully online ! Starting the initialisations things...\n---------\n")
    startMsg = globalVar.getRestartMsg()
    try:
        if startMsg != 0:                           # If the bot was rebooted with the admin command, change the status
            msg = await get(slash, interactions.Message, parent_id=912137828614426707, object_id=startMsg)
            await msg.edit(embeds=interactions.Embed(title="Redémarrage en cours...", description="Phase d'initalisation..."))
            globalVar.changeFightEnabled(True)
    except:
        globalVar.changeFightEnabled(True)

    # Shop reload and status change
    if bidule != False:
        ballerine = datetime.now() + horaire + timedelta(hours=1)
        while ballerine.hour % 3 != 0:
            ballerine = ballerine + timedelta(hours=1)

        if not(globalVar.fightEnabled()):
            await slash.change_presence(ClientPresence(status=StatusType.DND,activities=[PresenceActivity(name="Les combats sont désactivés",type=PresenceActivityType.GAME)]))
        else:
            await slash.change_presence(ClientPresence(status=StatusType.ONLINE,activities=[PresenceActivity(name="Prochain shop à "+ballerine.strftime('%Hh'),type=PresenceActivityType.GAME)]))

    if not(oneClock.is_running()):
        oneClock.start()

    teamWinDB.resetAllFightingStatus()
    if not(twitchAlertLoop.is_running()):
        twitchAlertLoop.start()

    print("\nDownloading the emojis for the custom icons...")
    await downloadAllHeadGearPng(slash)
    await downloadAllWeapPng(slash)
    await downloadAllIconPng(slash)
    await downloadElementIcon(slash)

    print("\n------- End of the initialisation -------")
    if not(isLenapy):
        print(datetime.now().strftime('%H:%M'))

    try:
        if startMsg != 0:
            await msg.edit(embeds=interactions.Embed(title="Redémarrage en cours...", color=light_blue, description="Le bot a bien été redémarré"))
            await msg.channel.send("Le redémarrage du bot est terminé Léna")
            globalVar.getRestartMsg(int(0))
            print("Redémarrage terminé")
    except:
        globalVar.getRestartMsg(int(0))

# ====================================================================================================
#                                               COMMANDS
# ====================================================================================================
if isLenapy:
    adminServ = [912137828614426704]
else:
    adminServ = [927195778013859902]

# -------------------------------------------- ON MESSAGE --------------------------------------------
@slash.event
async def on_message(ctx: interactions.Message):
    pathUserProfile = "./userProfile/{0}.prof".format(ctx.author.id)
    if os.path.exists(pathUserProfile) and len(ctx.content) >= 3:
        try:
            await addExpUser(slash, pathUserProfile, ctx, 3, 3)
        except:
            print("Erreur dans la gestion du message de {0}".format(
                ctx.author.name))
            print_exc()

# -------------------------------------------- ENCYCLOPEDIA --------------------------------------------
@slash.command(name="encyclopedia", description="Vous permet de consulter l'encyclopédie", options=[
    interactions.Option(
        name="destination", description="Que voulez vous consulter ?", required=False, type=3,
        choices=[
            interactions.Choice(name="Accessoires", value="accessoires"),
            interactions.Choice(name="Vêtements", value="vetements"),
            interactions.Choice(name="Chaussures", value="chaussures"),
            interactions.Choice(name="Armes", value="armes"),
            interactions.Choice(name="Compétences", value="competences"),
            interactions.Choice(name="Alliés Temporaires", value='tempAlies'),
            interactions.Choice(name="Ennemis", value="ennemies"),
            interactions.Choice(name="Boss", value="boss"),
            interactions.Choice(name="Objets non-possédés", value="locked"),
            interactions.Choice(name="Succès", value="achivements")
        ]
    )
])

async def comEncyclopedia(ctx: CommandContext, destination = None):
    if not(await botChannelVerif(slash, ctx)):
        await ctx.send("Je ne suis pas autorisée à donner suite aux commandes dans ce salon",ephemeral=True)

    await ctx.defer()

    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    user = loadCharFile(pathUserProfile)

    if user == None:
        await ctx.send("Vous devez avoir un personnage pour utiliser cette commande.\nVous pouvez en créer un a l'aide de la command /start")

    try:
        if destination == None:
            destination = "locked"
        await encylopedia(slash, ctx, destination, user)
    except Exception as e:
        print_exc()
        await ctx.send("Une erreur est survenue :\n{0}".format(e))

# -------------------------------------------- FIGHT --------------------------------------------
allreadyinWait, allreadyinWaitQuick = [], []
# normal fight
@slash.command(name="fight_normal", description="Permet de lancer un combat normal")
async def normal(ctx):
    msg = None
    if not(await botChannelVerif(slash, ctx)):
        return 0
    if not(globalVar.fightEnabled()):
        await ctx.send(embeds=interactions.Embed(title="__Combats désactivés__", description="Les combats sont actuellement désactivés pour cause de bug ou de déploiment imminant d'une mise à jour\nVeuillez vous référer au status du bot pour savoir si les combats sont désactivés ou non"),ephemeral=True)
        return 0

    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    try:
        user = loadCharFile(pathUserProfile)
    except:
        await ctx.send("Vous n'avez pas commencé l'aventure",ephemeral=True)
        return 0

    ballerine, temp = 0, 0
    if user.team == 0:
        ballerine = user.owner
    else:
        ballerine = user.team

    timing = teamWinDB.getFightCooldown(ballerine)

    if timing > 0:
        if timing > 60*10:
            await ctx.send(embeds=errorEmbed("Cooldown", "Votre équipe ne pourra faire de combats normaux que dans {0} minute{1} et {2} seconde{3}".format(timing//60, ["", "s"][timing//60 > 1], timing % 60, ["", "s"][timing % 60 > 1])),ephemeral=True)
            return 0
        elif ballerine not in allreadyinWait:
            allreadyinWait.append(ballerine)
            while 1:
                timing = teamWinDB.getFightCooldown(ballerine)
                if timing > 0:
                    try:
                        if msg == None:
                            try:
                                msg = await ctx.send(embeds=await getRandomStatsEmbed(slash, [user], text="Votre combat a été mis en liste d'attente (Reste {0}{1}:{2}{3})".format(["","0"][timing//60<10], timing//60, ["","0"][timing%60<10], timing % 60)))
                            except:
                                msg = await ctx.channel.send(embeds=await getRandomStatsEmbed(slash, [user], text="Votre combat a été mis en liste d'attente (Reste {0}{1}:{2}{3})".format(["","0"][timing//60<10], timing//60, ["","0"][timing%60<10], timing % 60)))
                        else:
                            await msg.edit(embeds=await getRandomStatsEmbed(slash, [user], text="Votre combat a été mis en liste d'attente (Reste {0}{1}:{2}{3})".format(["","0"][timing//60<10], timing//60, ["","0"][timing%60<10], timing % 60)))
                    except:
                        pass
                    await asyncio.sleep(10)
                else:
                    try:
                        if msg == None:
                            msg = await ctx.send(embeds=await getRandomStatsEmbed(slash, [user], text="Combat en cour de génération..."))
                        else:
                            await msg.edit(embeds=await getRandomStatsEmbed(slash, [user], text="Combat en cour de génération..."))
                    except:
                        pass
                    break
        else:
            await ctx.send(embeds=errorEmbed("Cooldown", "Votre équipe est déjà en file d'attente"),ephemeral=True)
            return 0

    try:
        allreadyinWait.remove(ballerine)
    except:
        pass
    fightingStatus = teamWinDB.isFightingBool(ballerine)
    if fightingStatus[0]:
        channel = await get(slash,interactions.Channel,object_id=fightingStatus[2],parent_id=ctx.guild_id)
        fightingMessage = await get(slash, interactions.Message, object_id=fightingStatus[0],parent_id=channel.id)

        fightingRespond = "__Votre équipe affronte actuellement :__\n"
        temp = ""
        for letter in fightingStatus[1]:
            if letter == ";" and len(temp) > 0:
                ennemi = findEnnemi(temp)
                if ennemi == None:
                    ennemi = findAllie(temp)
                if ennemi != None:
                    fightingRespond += "{0} {1}\n".format(
                        ennemi.icon, ennemi.name)
                else:
                    fightingRespond += "<:blocked:897631107602841600> L'ennemi n'a pas pu être trouvé\n"
                temp = ""
            else:
                temp += letter

        if msg == None:
            await ctx.send(embeds=interactions.Embed(title="__/fight__", color=user.color, description=fightingRespond),ephemeral=True)
        else:
            await msg.edit(embeds=interactions.Embed(title="__/fight__", color=user.color, description=fightingRespond))
        return 0

    team1 = []
    if user.team != 0:
        for a in userTeamDb.getTeamMember(user.team):
            team1 += [loadCharFile("./userProfile/{0}.prof".format(a))]
    else:
        team1 = [user]

    teamSettings = aliceStatsDb.getTeamSettings(team1[0])

    # Random event
    if msg == None:
        try:
            msg = await ctx.send(embeds=await getRandomStatsEmbed(slash,team1,text="__Combat en cours de génération...__"))
        except:
            msg = await ctx.channel.send(embeds=await getRandomStatsEmbed(slash,team1,text="__Combat en cours de génération...__"))
    fun, teamLvl, starLvl = random.randint(0, 99), 0, 0
    for ent in team1:
        teamLvl = max(ent.level,teamLvl)
        starLvl = max(ent.stars,starLvl)

    if fun < 0:                # For testing purposes
        temp = copy.deepcopy(findAllie("Lena"))
        temp.changeLevel(50)
        await fight(slash, [temp], [], ctx, False, procurFight=True, msg=msg)

    elif fun < 10:              # All OctoHeals ! Yes, it's for you H
        temp = team1
        temp.sort(key=lambda overheal: overheal.level, reverse=True)
        maxLvl = temp[0].level

        tablPreDefTeam = ["OctoHeal","Temmie","OctoBooms","Kitsunes","Aéro-Bennes"]
        roll = random.randint(0,len(tablPreDefTeam)-1)
        fightCtx = fightContext()
        #roll = 3
        
        if roll == 0:
            team2, lenBoucle, cmpt = [],8,0
            octoHealVet = findEnnemi("Octo Soigneur Vétéran")
            octoHeal = findEnnemi("Octo Soigneur")

            if maxLvl < octoHealVet.baseLvl:
                alea = copy.deepcopy(octoHeal)
            else:
                alea = copy.deepcopy(octoHealVet)

            alea.changeLevel(maxLvl)
            while cmpt < lenBoucle:
                team2.append(alea)
                cmpt += 1
        elif roll == 1:
            team2, lenBoucle, cmpt = [],8,1

            alea = copy.deepcopy(findEnnemi("Bob"))
            alea.changeLevel(maxLvl)
            alea.magie = alea.magie // 2
            team2.append(alea)
            
            alea = copy.deepcopy(findEnnemi("Temmie"))
            alea.changeLevel(maxLvl)

            while cmpt < lenBoucle:
                team2.append(alea)
                cmpt += 1
        elif roll == 2:
            team2, lenBoucle, cmpt = [],8,1
            alea = copy.deepcopy(findEnnemi("OctoBOUM"))
            alea.changeLevel(maxLvl)
            alea.skills, alea.weapon, alea.magie, alea.exp = [totalAnnilCast, None, None, None, None, None, None], BOUMBOUMBOUMBOUMweap, int(alea.magie * 2), 12

            while cmpt < lenBoucle:
                team2.append(alea)
                cmpt += 1
        elif roll == 3:
            team2 = [copy.deepcopy(findEnnemi("Lia")),copy.deepcopy(findEnnemi("Liu")),copy.deepcopy(findEnnemi("Liz")),copy.deepcopy(findEnnemi("Lio"))]
            for cmpt in range(len(team2)):
                team2[cmpt].changeLevel(maxLvl)

            kitFightConstEff = copy.deepcopy(constEff)
            kitFightConstEff.power, kitFightConstEff.stat, kitFightConstEff.turnInit, kitFightConstEff.unclearable = 25, PURCENTAGE, -1, True
            kitFightDmgUp = copy.deepcopy(dmgUp)
            kitFightDmgUp.power, kitFightDmgUp.turnInit, kitFightDmgUp.unclearable = 25, -1, True
            kitFightHealUp = copy.deepcopy(healDoneBonus)
            kitFightHealUp.power, kitFightHealUp.turnInit, kitFightHealUp.unclearable = 25, -1, True

            fightCtx.giveEffToTeam2 = [kitFightDmgUp, kitFightHealUp, kitFightConstEff]
        elif roll == 4:
            team2, lenBoucle, cmpt = [],8,1

            alea = copy.deepcopy(findEnnemi("Aéro-benne"))
            alea.changeLevel(maxLvl)

            while cmpt < lenBoucle:
                team2.append(alea)
                cmpt += 1
        
        await fight(slash, team1, team2, ctx, False, contexte=fightCtx, msg=msg, teamSettings=teamSettings)

    elif fun < 20 and teamLvl >= 25:             # Raid
        try:
            tablAllTeams, allReadySeen = userTeamDb.getAllTeamIds(), []
            if user.team not in ["0",0]:
                tablAllTeams.remove(user.team)
            random.shuffle(tablAllTeams)

            moyTeam = 0
            for a in team1:
                moyTeam += a.level
                allReadySeen.append(a.owner)

            moyTeam = moyTeam/len(team1)

            for tempTeamId in tablAllTeams:
                tempTeam, moyTempTeam = [], 0
                for a in userTeamDb.getTeamMember(tempTeamId):
                    if a not in allReadySeen:
                        tempUser = loadCharFile(
                            "./userProfile/{0}.prof".format(a))
                        moyTempTeam += tempUser.level
                        tempTeam += [tempUser]

                moyTempTeam = moyTempTeam/max(1, len(tempTeam))
                if moyTeam <= moyTempTeam+10 and moyTeam >= moyTempTeam-10:
                    team1 += tempTeam
                    break

            temp = team1
            temp.sort(key=lambda overheal: overheal.level, reverse=True)
            maxLvl = temp[0].level
            team2 = []
            alea = copy.deepcopy(tablRaidBoss[random.randint(0, len(tablRaidBoss)-1)])

            alea.changeLevel(maxLvl)
            team2.append(alea)

            await fight(slash, team1, team2, ctx, False, bigMap=True, msg=msg, teamSettings=teamSettings)
        except:
            await msg.edit(embeds=interactions.Embed(title="__Unknow error during fight__", description=format_exc()))
            teamWinDB.changeFighting(team1[0].team, value=False, channel=0)

    elif fun < 30:              # Procu Fight
        level = team1[0].level
        team1, team2, randomRoll = [], [], random.randint(0, 99)
        if randomRoll < 35: # ClemClem
            procurData = procurTempStuff["Clémence Exaltée"]
            ent = copy.deepcopy(findAllie("Clémence Exaltée"))
            level += random.randint(0, 100)
            ent.changeLevel(level,stars=starLvl)
            ent.stuff = [
                stuff(procurData[1][0],procurData[1][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[1][2]),
                stuff(procurData[2][0],procurData[2][1],1,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[2][2]),
                stuff(procurData[3][0],procurData[3][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[3][2])
            ]

            team1.append(ent)

        elif randomRoll < 65:  # Luna
            ent = copy.deepcopy(findAllie("Luna prê."))
            procurData = procurTempStuff["Luna prê."]
            level += random.randint(0, 50)
            ent.changeLevel(level,stars=starLvl)

            ent.stuff = [
                stuff(procurData[1][0],procurData[1][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[1][2]),
                stuff(procurData[2][0],procurData[2][1],1,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[2][2]),
                stuff(procurData[3][0],procurData[3][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[3][2])
            ]

            team1.append(ent)

            if random.randint(0, 99) < 50:               # Eclipse Eternelle
                ent2 = copy.deepcopy(findAllie('Iliana prê.'))
                procurData = procurTempStuff["Iliana prê."]
                ent2.changeLevel(level,stars=starLvl)

                ent2.stuff = [
                    stuff(procurData[1][0],procurData[1][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent2.level),int(procurData[4][1][0]*procurData[4][1][1]*ent2.level),int(procurData[4][2][0]*procurData[4][2][1]*ent2.level),int(procurData[4][3][0]*procurData[4][3][1]*ent2.level),int(procurData[4][4][0]*procurData[4][4][1]*ent2.level),int(procurData[4][5][0]*procurData[4][5][1]*ent2.level),int(procurData[4][6][0]*procurData[4][6][1]*ent2.level),int(procurData[4][7][0]*procurData[4][7][1]*ent2.level),int(procurData[4][8][0]*procurData[4][8][1]*ent2.level),int(procurData[4][9][0]*procurData[4][9][1]*ent2.level),emoji=procurData[1][2]),
                    stuff(procurData[2][0],procurData[2][1],1,0,int(procurData[4][0][0]*procurData[4][0][1]*ent2.level),int(procurData[4][1][0]*procurData[4][1][1]*ent2.level),int(procurData[4][2][0]*procurData[4][2][1]*ent2.level),int(procurData[4][3][0]*procurData[4][3][1]*ent2.level),int(procurData[4][4][0]*procurData[4][4][1]*ent2.level),int(procurData[4][5][0]*procurData[4][5][1]*ent2.level),int(procurData[4][6][0]*procurData[4][6][1]*ent2.level),int(procurData[4][7][0]*procurData[4][7][1]*ent2.level),int(procurData[4][8][0]*procurData[4][8][1]*ent2.level),int(procurData[4][9][0]*procurData[4][9][1]*ent2.level),emoji=procurData[2][2]),
                    stuff(procurData[3][0],procurData[3][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent2.level),int(procurData[4][1][0]*procurData[4][1][1]*ent2.level),int(procurData[4][2][0]*procurData[4][2][1]*ent2.level),int(procurData[4][3][0]*procurData[4][3][1]*ent2.level),int(procurData[4][4][0]*procurData[4][4][1]*ent2.level),int(procurData[4][5][0]*procurData[4][5][1]*ent2.level),int(procurData[4][6][0]*procurData[4][6][1]*ent2.level),int(procurData[4][7][0]*procurData[4][7][1]*ent2.level),int(procurData[4][8][0]*procurData[4][8][1]*ent2.level),int(procurData[4][9][0]*procurData[4][9][1]*ent2.level),emoji=procurData[3][2])
                ]
                
                team1.append(ent2)

                if user.aspiration in [ALTRUISTE, IDOLE, INOVATEUR, PREVOYANT, VIGILANT, PROTECTEUR]:
                    team1 = [ent2, ent]

                boss = copy.deepcopy(unformBoss)
                boss.changeLevel(level + random.randint(300, 350))
                team2, listDangerous, cmpt = [boss], [findEnnemi('Lueur informe A'), findEnnemi('Ombre informe A'), findEnnemi('Ombre informe B')], 1
                while cmpt < 8:
                    temp = copy.deepcopy(listDangerous[random.randint(0, len(listDangerous)-1)])
                    temp.changeLevel(level + random.randint(200, 300))
                    team2.append(temp)
                    cmpt += 1

        else:
            procurData = procurTempStuff["Lia Ex"]
            ent = copy.deepcopy(findAllie("Lia Ex"))
            level += random.randint(0, 50)
            ent.changeLevel(level,stars=starLvl)
            ent.stuff = [
                stuff(procurData[1][0],procurData[1][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[1][2]),
                stuff(procurData[2][0],procurData[2][1],1,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[2][2]),
                stuff(procurData[3][0],procurData[3][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[3][2])
            ]

            team1.append(ent)

        try:
            await fight(slash, team1, team2, ctx, False, procurFight=True, msg=msg, teamSettings=teamSettings)
        except:
            if msg == None:
                await ctx.send(embeds=interactions.Embed(title="__Unknow error during fight__", description=format_exc()))
            else:
                await msg.edit(embeds=interactions.Embed(title="__Unknow error during fight__", description=format_exc()))
            teamWinDB.changeFighting(team1[0].team, value=False, channel=0)

    else:
        await fight(slash, team1, [], ctx, False, msg=msg, teamSettings=teamSettings)

# quick fight
@slash.command(name="fight_quick", description="Vous permet de faire un combat en sautant directement à la fin")
async def comQuickFight(ctx):
    msg = None
    if not(await botChannelVerif(slash, ctx)):
        return 0
    if not(globalVar.fightEnabled()) and int(ctx.author.id) != 213027252953284609:
        await ctx.send(embeds=interactions.Embed(title="__Combats désactivés__", description="Les combats sont actuellement désactivés pour cause de bug ou de déploiment imminant d'une mise à jour\nVeuillez vous référer au status du bot pour savoir si les combats sont désactivés ou non"),ephemeral=True)
        return 0

    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    try:
        user = loadCharFile(pathUserProfile)
    except:
        await ctx.send("Vous n'avez pas commencé l'aventure",ephemeral=True)
        return 0

    ballerine, temp = 0, 0
    if user.team == 0:
        ballerine = user.owner
    else:
        ballerine = user.team

    timing = teamWinDB.getFightCooldown(ballerine, True)
    if timing > 0:
        if timing > 60*10:
            await ctx.send(embeds=errorEmbed("Cooldown", "Votre équipe ne pourra faire de combats rapides que dans {0} minute{1} et {2} seconde{3}".format(timing//60, ["", "s"][timing//60 > 1], timing % 60, ["", "s"][timing % 60 > 1])),ephemeral=True)
            return 0
        elif ballerine not in allreadyinWaitQuick:
            allreadyinWaitQuick.append(ballerine)
            while 1:
                timing = teamWinDB.getFightCooldown(ballerine, True)
                if timing > 0:
                    try:
                        if msg == None:
                            try:
                                msg = await ctx.send(embeds=await getRandomStatsEmbed(slash, [user], text="Votre combat a été mis en liste d'attente (Reste {0}{1}:{2}{3})".format(["","0"][timing//60<10], timing//60, ["","0"][timing%60<10], timing % 60)))
                            except:
                                msg = await ctx.channel.send(embeds=await getRandomStatsEmbed(slash, [user], text="Votre combat a été mis en liste d'attente (Reste {0}{1}:{2}{3})".format(["","0"][timing//60<10], timing//60, ["","0"][timing%60<10], timing % 60)))

                        else:
                            await msg.edit(embeds=await getRandomStatsEmbed(slash, [user], text="Votre combat a été mis en liste d'attente (Reste {0}{1}:{2}{3})".format(["","0"][timing//60<10], timing//60, ["","0"][timing%60<10], timing % 60)))
                    except:
                        pass
                    await asyncio.sleep(10)
                else:
                    try:
                        if msg == None:
                            msg = await ctx.send(embeds=await getRandomStatsEmbed(slash, [user], text="Combat en cour de génération..."))
                        else:
                            await msg.edit(embeds=await getRandomStatsEmbed(slash, [user], text="Combat en cour de génération..."))

                    except:
                        pass
                    break
        else:
            await ctx.send(embeds=errorEmbed("Cooldown", "Votre équipe est déjà en file d'attente"))
            return 0

    try:
        allreadyinWaitQuick.remove(ballerine)
    except:
        pass
    team1 = []
    if user.team != 0:
        for a in userTeamDb.getTeamMember(user.team):
            team1 += [loadCharFile("./userProfile/{0}.prof".format(a))]
    else:
        team1 = [user]

    teamSettings = aliceStatsDb.getTeamSettings(team1[0])

    if msg == None:
        try:
            msg = await ctx.send(embeds=await getRandomStatsEmbed(slash,team1,text="__Combat rapide en cours de génération...__"))
        except:
            msg = await ctx.channel.send(embeds=await getRandomStatsEmbed(slash,team1,text="__Combat rapide en cours de génération...__"))

    fun, teamLvl = random.randint(0, 99), 0
    for ent in team1:
        teamLvl = max(ent.level,teamLvl)

    if fun < 5 and teamLvl >= 25:             # Raid
        await msg.edit(embeds=interactions.Embed(title="__Combat de raid__", color=light_blue, description="Les équipes sont en cours de génération..."))
        try:
            tablAllTeams, allReadySeen = userTeamDb.getAllTeamIds(), []
            try:
                tablAllTeams.remove(user.team)
            except:
                pass
            random.shuffle(tablAllTeams)

            moyTeam = 0
            for a in team1:
                moyTeam += a.level
                allReadySeen.append(a.owner)

            moyTeam = moyTeam/len(team1)

            for tempTeamId in tablAllTeams:
                tempTeam, moyTempTeam = [], 0
                for a in userTeamDb.getTeamMember(tempTeamId):
                    if a not in allReadySeen:
                        tempUser = loadCharFile(
                            "./userProfile/{0}.prof".format(a))
                        moyTempTeam += tempUser.level
                        tempTeam += [tempUser]

                moyTempTeam = moyTempTeam/max(1, len(tempTeam))
                if moyTeam <= moyTempTeam+10 and moyTeam >= moyTempTeam-10:
                    team1 += tempTeam
                    break

            temp = team1
            temp.sort(key=lambda overheal: overheal.level, reverse=True)
            maxLvl = temp[0].level
            team2 = []
            alea = copy.deepcopy(tablRaidBoss[random.randint(0, len(tablRaidBoss)-1)])
            #alea = copy.deepcopy(findEnnemi("Nacialisla"))

            alea.changeLevel(maxLvl)
            team2.append(alea)

            await fight(slash, team1, team2, ctx, True, bigMap=True, msg=msg, teamSettings=teamSettings)
        except:
            await msg.edit(embeds=interactions.Embed(title="__Unknow error during fight__", description=format_exc()))
            teamWinDB.changeFighting(team1[0].team, value=False, channel=0)
    else:
        await fight(slash, team1, [], ctx, msg= msg, teamSettings = teamSettings)

# test fights
@slash.command(name="fight_test", description="Permet de réaliser 10 combats rapides de suite", scope=adminServ)
async def comTestFight(ctx):
    await ctx.defer()
    try:
        user = loadCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof")

        team1 = []
        if user.team != 0:
            for a in userTeamDb.getTeamMember(user.team):
                team1 += [loadCharFile("./userProfile/{0}.prof".format(a))]
        else:
            team1 = [user]

        teamSettings = aliceStatsDb.getTeamSettings(team1[0])
        teamLvl, cmpt = 0, 0
        for ent in team1:
            teamLvl = max(ent.level,teamLvl)

        while cmpt < 10:
            fun = random.randint(0, 99)
            if fun < 5 and teamLvl >= 25:             # Raid
                try:
                    team3 = copy.deepcopy(team1)
                    tablAllTeams, allReadySeen = userTeamDb.getAllTeamIds(), []
                    try:
                        tablAllTeams.remove(user.team)
                    except:
                        pass
                    random.shuffle(tablAllTeams)

                    moyTeam = 0
                    for a in team3:
                        moyTeam += a.level
                        allReadySeen.append(a.owner)

                    moyTeam = moyTeam/len(team3)

                    for tempTeamId in tablAllTeams:
                        tempTeam, moyTempTeam = [], 0
                        for a in userTeamDb.getTeamMember(tempTeamId):
                            if a not in allReadySeen:
                                tempUser = loadCharFile(
                                    "./userProfile/{0}.prof".format(a))
                                moyTempTeam += tempUser.level
                                tempTeam += [tempUser]

                        moyTempTeam = moyTempTeam/max(1, len(tempTeam))
                        if moyTeam <= moyTempTeam+10 and moyTeam >= moyTempTeam-10:
                            team3 += tempTeam
                            break

                    temp = team3
                    temp.sort(key=lambda overheal: overheal.level, reverse=True)
                    maxLvl = temp[0].level
                    team2 = []
                    alea = copy.deepcopy(tablRaidBoss[random.randint(0, len(tablRaidBoss)-1)])
                    #alea = copy.deepcopy(findEnnemi("Nacialisla"))

                    alea.changeLevel(maxLvl)
                    team2.append(alea)

                    await fight(slash, team3, team2, ctx, True, bigMap=True, teamSettings=teamSettings, testFight=True, waitEnd=False)
                except:
                    teamWinDB.changeFighting(team1[0].team, value=False, channel=0)
            else:
                await fight(slash, team1, [], ctx, teamSettings = teamSettings, testFight=True, waitEnd=False)
            cmpt += 1
        await ctx.send("Tous les combats ont été effectués ✅")
    except:
        await ctx.send("Une erreur est survenue :\n"+format_exc(1900))

# octogone fight
@slash.command(name="octogone_solo", description="Affrontez quelqu'un en 1v1 Gare Du Nord !", options=[
    interactions.Option(name="versus", description="Affronter qui ?", type=6, required=True)
])
async def octogone(ctx, versus):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if not(os.path.exists(pathUserProfile)):
        await ctx.send("Comment veut-tu affronter quelqu'un si tu n'a pas de personnage ?\nVa donc faire un tour vers /start",ephemeral=True)
        return 0

    if os.path.exists(absPath + "/userProfile/" + str(versus.id) + ".prof"):
        await fight(slash, [loadCharFile(pathUserProfile)], [loadCharFile(absPath + "/userProfile/" + str(versus.id) + ".prof")], ctx, auto=False, octogone=True)

    elif versus.id in [623211750832996354, 769999212422234122]:
        temp = loadCharFile(pathUserProfile)
        tempi = tablAllAllies[0]
        tempi.changeLevel(50)
        await fight(slash, [temp], [tempi], ctx, auto=False, octogone=True)

    else:
        await ctx.send("La personne que tu as désigné ne possède pas de personnage désolé",ephemeral=True)

# team fight
@slash.command(name="octogone_team", description="Affrontez l'équipe de quelqu'un avec la votre", options=[
    interactions.Option(name="versus", description="Affronter qui ?", type=6, required=True)
])
async def teamFight(ctx, versus):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if not(os.path.exists(pathUserProfile)):
        await ctx.send("Vous ne possédez pas de personnage.\nAllez donc faire un tour vers /start",ephemeral=True)
        return 0
    user = loadCharFile(pathUserProfile)
    team1 = []
    if user.team != 0:
        for a in userTeamDb.getTeamMember(user.team):
            team1 += [loadCharFile("./userProfile/{0}.prof".format(a))]
    else:
        team1 = [user]

    team2 = []
    pathOctogonedProfile = absPath + "/userProfile/" + str(versus.id) + ".prof"
    if not(os.path.exists(pathOctogonedProfile)) and versus.id not in [623211750832996354, 769999212422234122]:
        await ctx.send("L'utilisateur désigné ne possède pas de personnage",ephemeral=True)
        return 0

    if versus.id not in [623211750832996354, 769999212422234122]:
        octogoned = loadCharFile(pathOctogonedProfile, ctx)
        if octogoned.team != 0:
            for a in userTeamDb.getTeamMember(user.team):
                team2 += [loadCharFile("./userProfile/{0}.prof".format(a))]
        else:
            team2 = [octogoned]
    else:
        tablLenaTeam = ["Lena", "Gwendoline", "Shushi",
                        "Clémence", "Alice", "Félicité", "Hélène", "Iliana"]
        for a in tablLenaTeam:
            alea = copy.deepcopy(findAllie(a))
            alea.changeLevel(55)
            team2.append(alea)

    await fight(slash, team1, team2, ctx, False, octogone=True)

# -------------------------------------------- COOLDOWN --------------------------------------------
@slash.command(name="cooldowns", description="Vous donne les cooldowns des commandes /fight et /quickFight pour votre équipe")
async def cooldowns(ctx):
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile)
        involvedTeam, involvedEmoji = [[user.team,user.owner][user.team==0]], [await getUserIcon(slash,user)]

        for procur in user.haveProcurOn:
            usr = loadCharFile("./userProfile/{0}.prof".format(procur))
            if usr.team not in involvedTeam or usr.team == 0:
                involvedTeam.append([usr.team,user.owner][usr.team==0])
                involvedEmoji.append(await getUserIcon(slash,usr))
            else:
                for cmpt in range(len(involvedTeam)):
                    if involvedTeam[cmpt] == usr.team:
                        involvedEmoji[cmpt]+=await getUserIcon(slash,usr)
        
        color = user.color
        if not(globalVar.fightEnabled()):
            color = red
        toReply = interactions.Embed(title="__Cooldowns des commandes Fight__", color=color)

        for cmpt in range(len(involvedTeam)):
            team = involvedTeam[cmpt]
            cd = teamWinDB.getFightCooldown(team)
            cd2 = teamWinDB.getFightCooldown(team, True)
            fcooldown, fseconds, fqcooldown, fqseconds, faccord, fqaccord, fsaccord, fqsaccord = cd//60, cd % 60, cd2//60, cd2 % 60, "", "", "", ""
            if fcooldown > 1:
                faccord = "s"
            if fqcooldown > 1:
                fqaccord = "s"
            if fseconds > 1:
                fsaccord = "s"
            if fqseconds > 1:
                fqsaccord = "s"

            fightingStatus = teamWinDB.isFightingBool(int(team))
            if not(globalVar.fightEnabled()):
                notFight = "**<:noneWeap:917311409585537075> __Les combats sont actuellement désactivées !__**\n\n"
                color = red
            else:
                notFight = ""
                color = user.color

            if fightingStatus[0]:
                fightingRespond = "__Votre équipe affronte actuellement :__\n"
                temp = ""
                for letter in fightingStatus[1]:
                    if letter == ";" and len(temp) > 0:
                        ennemi = findEnnemi(temp)
                        if ennemi == None:
                            ennemi = findAllie(temp)
                        if ennemi != None:
                            fightingRespond += "{0} {1}\n".format(
                                ennemi.icon, ennemi.name)
                        else:
                            fightingRespond += "<:blocked:897631107602841600> L'ennemi n'a pas pu être trouvé\n"
                        temp = ""
                    else:
                        temp += letter

                toReply.add_field(name="__Cooldowns__",value=involvedEmoji[cmpt]+"\n"+notFight+fightingRespond)
            else:
                toReply.add_field(name="__Cooldowns__",value=involvedEmoji[cmpt]+"\n"+notFight+f"__Normal__ : {fcooldown} minute{faccord} et {fseconds} seconde{fsaccord}\n__Quick__ : {fqcooldown} minute{fqaccord} et {fqseconds} seconde{fqsaccord}")
            
        try:
            await ctx.send(embeds = toReply,ephemeral=True)
        except:
            await ctx.send("Une erreur est survenue :\n"+format_exc(1900))

# -------------------------------------------- PATCHNOTE --------------------------------------------
@slash.command(name="patchnote", description="Renvoie le dernier patchnote du bot")
async def patchnote(ctx):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    await send_patchnote(ctx)

# -------------------------------------------- ROLL --------------------------------------------
@slash.command(name="roll", description="Permet de lancer un dé", options=[
    interactions.Option(name="min", description="Minimum du jet. Par défaut, 1",type=4, required=False),
    interactions.Option(name="max", description="Minimum du jet. Par défaut, 100",type=4, required=False),
])
async def roll(ctx, min=1, max=100):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    rollmes = rollMessage[random.randint(0, len(rollMessage)-1)]
    await ctx.send(embeds=interactions.Embed(title=f"🎲 roll {min} - {max}", color=light_blue, description=rollmes.format(random.randint(min, max))))

# -------------------------------------------- SHOP --------------------------------------------
@slash.command(name="shop", description="Vous permet d'entrer dans le magasin")
async def shopSlash(ctx):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    await shop2(slash, ctx, shopping.shopping)

# -------------------------------------------- INVENTORY --------------------------------------------
@slash.command(name="inventory", description="Vous permet de naviger dans votre inventaire", options=[
    interactions.Option(name="destination", description="Dans quel inventaire voulez-vous aller ?", type=3, required=False, choices=[
        interactions.Choice(name="Equipement", value="Equipement"),
        interactions.Choice(name="Arme", value="Arme"),
        interactions.Choice(name="Compétences", value="Compétences"),
        interactions.Choice(name="Objets spéciaux", value="Objets spéciaux"),
        interactions.Choice(name="Elements", value="Elements")
    ]),
    interactions.Option(name="procuration", description="De qui voulez vous consulter l'inventaire ?", type=6, required=False),
    interactions.Option(name="nom", description="Le nom ou l'identifiant d'un objet. Les espaces peuvent être remplacés par des _", type=3, required=False)
])
async def invent2(ctx, destination="Equipement", procuration=None, nom=None):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    for a in range(5):
        if ["Equipement", "Arme", "Compétences", "Objets spéciaux", "Elements"][a] == destination:
            destination = a
            break

    if procuration != None:
        user = loadCharFile(absPath + "/userProfile/" + str(procuration.id) + ".prof")
    else:
        user = loadCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof")

    if nom != None:
        nom = nom.replace("_", " ")
        nom = remove_accents(nom.lower())
        while nom.endswith(" "):
            nom = nom[0:-1]

        research = weapons[:]+skills[:]+stuffs[:]+others[:]+[token,trans]
        lastResarch = []
        nameTempCmpt, lenName, findId = 0, len(nom), False

        for obj in research:
            if nom == obj.id or remove_accents(obj.name.lower()) == nom:
                nom, findId = obj.id, True
                break

        if not(findId):
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
                        desc += "{0} {2}{1}{2}\n".format(a.emoji, a.name, have)
                        options += [interactions.SelectOption(label=unhyperlink(a.name), value=a.name, emoji=getEmojiObject(a.emoji))]

                    if len(options) > 24:
                        def getNameSortValue(obj):
                            cmpt = 0
                            for letter in nom:
                                if letter in obj.name:
                                    cmpt+=1
                            return cmpt
                        
                        lastResarch.sort(key=lambda obj:getNameSortValue(obj))
                        lastResarch = lastResarch[:24]
                        options, desc = [], ""
                        for a in lastResarch:
                            have = ""
                            if not(user.have(a)):
                                have = "`"
                            desc += "{0} {2}{1}{2}\n".format(a.emoji, a.name, have)
                            options += [interactions.SelectOption(unhyperlink(a.name), a.name, getEmojiObject(a.emoji))]

                    select = interactions.SelectMenu(custom_id = "invSherchMenu", options=options, placeholder="Sélectionnez un objet :")
                    msg = await ctx.send(embeds=interactions.Embed(title="/inventory", color=light_blue, description="L'objet spécifié n'a pas été trouvé. Voici une liste des résultats les plus proches :\n\n"+desc), components=[interactions.ActionRow(components=[select])])

                    def check(m):
                        return m.author.id == ctx.author.id and m.message.id == msg.id

                    try:
                        respond = await slash.wait_for_component(components=select, check=check, timeout=60)
                    except:
                        await msg.edit(embeds=interactions.Embed(title="/inventory", color=light_blue, description="Liste des résultats correspondant à la recherche\n\n"+desc), components=[])
                        return 0
                        break

                    nom = respond.data.values[0]
                    await msg.edit(embeds=interactions.Embed(title="/inventory", color=light_blue, description="L'objet spécifié n'a pas été trouvé. Voici une liste des résultats les plus proches :\n\n"+desc), components=[interactions.ActionRow(components=[getChoisenSelect(select, respond.data.values[0])])])
                    break

        if nom == token.name:
            obj = token
            repEmb = infoOther(obj, user)
            try:
                await ctx.send(embeds=repEmb, components=[])
            except:
                await ctx.channel.send(embeds=repEmb, components=[])
            return 0
        elif nom in [trans.name,"lb"]:
            transField = "La **Transcendance** est une compétence commune à tous les joueurs et alliés temporaires débloquée et équipée automatiquement dès le début.\nLorsqu'utilisée, cette compétence deviens l'une des compétences listée si dessous en fonction du nombre de **jauges transcendiques** remplie ainsi que de l'aspiration du lanceur.\nLe nombre de jauges transcendiques disponibles dans un combat dépend de divers critères. Chaques critères remplie rajoute une barre pour l'équipe en question :\n> - L'équipe comporte au moins 8 membres\n> - L'équipe comporte au moins 16 membres\n> - L'équipe adverse contient au moins 1 boss\n> - L'équipe adverse est composée d'un boss AllvOne\n> - L'équipe adverse est composée d'alliés temporaires ou de joueurs\n\nLorsqu'utilisée, toutes les **jauges transcendiques** de l'équipe sont remises à 0, même si elles n'étaient pas toutes remplies."
            emby = interactions.Embed(title="__Transcendance :__",color=light_blue,description=transField)
            await ctx.send(embeds=emby)

            transNames, cmpt, tably = ["__Transcendances niveau 1__ <:lbFull:983450379205378088>","__Transcendances niveau 2__ <:lbFull:983450379205378088><:lbFull:983450379205378088>","__Transcendances niveau 3__ <:lbFull:983450379205378088><:lbFull:983450379205378088><:lbFull:983450379205378088>","__Transcendances niveau 4__ <:lbFull:983450379205378088><:lbFull:983450379205378088><:lbFull:983450379205378088><:lbFull:983450379205378088>"], 0, [lb1MinTabl,lb2MinTabl,lb3Tabl,[lb4]]
            
            while cmpt < 4:
                transField = ""
                for skilly in tably[cmpt]:
                    usedBy = ""
                    if cmpt != 3:
                        for cmpt2 in range(len(inspi)):
                            if [lb1Tabl,lb2Tabl,lb3Tabl][cmpt][cmpt2] == skilly:
                                usedBy += aspiEmoji[cmpt2]
                    else:
                        for cmpt2 in range(len(inspi)):
                            usedBy += aspiEmoji[cmpt2]
                    transField += "{0} __{1} :__ ({3})\n> {2}\n\n".format(skilly.emoji,skilly.name,skilly.description.replace("\n","\n> "),usedBy)
                emby = interactions.Embed(title=transNames[cmpt],color=light_blue,description=transField)
                emby.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(trans.emoji).id))

                await ctx.channel.send(embeds=emby)
                cmpt += 1
            return 1

        nom = [nom, None]

    else:
        nom = [None]

    if nom != [None]:
        await inventory(slash, ctx, nom[0], procur=user.owner)
    else:
        await inventoryV2(slash, ctx, destination, user)

# -------------------------------------------- POINTS --------------------------------------------
@slash.command(name="points", description="Vous permet de répartir vos points bonus", options=[
    interactions.Option(name="procuration", description="De qui voulez vous consulter les points bonus ?", type=6, required=False)
])
async def pts(ctx, procuration=None):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    await points(slash, ctx, ["/points", None], procuration, slashed=True)

# -------------------------------------------- TEAM --------------------------------------------
detailPlus = interactions.Button(type=2, style=ButtonStyle.PRIMARY, label="Aff. détaillé", emoji=Emoji(name="➕"), custom_id="detail")
detailMinus = interactions.Button(type=2, style=ButtonStyle.PRIMARY, label="Aff. simplifié", emoji=Emoji(name="➖"), custom_id=detailPlus.custom_id)

# team view
@slash.command(name="team_view", description="Permet de voir les équipements de votre équipe ou de celle de quelqu'un d'autre", options=[
    interactions.Option(name="joueur", description="Voir l'équipe d'un autre joueur", type=6, required=False)
])
async def teamView(ctx, joueur=None):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    if joueur == None:
        joueur = ctx.author
    pathUserProfile = absPath + "/userProfile/" + str(joueur.id) + ".prof"

    if os.path.exists(pathUserProfile):
        user, extended = loadCharFile(pathUserProfile), False
        msg = await loadingSlashEmbed(ctx)
        if user.team == 0:
            teamMates = [user]
        else:
            teamMates = []
            for usr in userTeamDb.getTeamMember(user.team):
                teamMates.append(loadCharFile(
                    path="./userProfile/{0}.prof".format(usr)))

        def checky(m):
            return m.author.id == ctx.author.id

        while 1:
            temp = ""
            if not(extended):
                for usr in teamMates:
                    level = str(usr.level) + ["", "<:ls:925860806602682369>{0}".format(usr.stars)][usr.stars > 0]
                    ballerine = f'{aspiEmoji[usr.aspiration]}|{usr.weapon.emoji}|{usr.stuff[0].emoji}{usr.stuff[1].emoji}{usr.stuff[2].emoji}|'
                    for cmpt in range(len(usr.skills)):
                        if type(usr.skills[cmpt]) == skill:
                            ballerine += usr.skills[cmpt].emoji
                        elif usr.level >= lvlToUnlockSkill[cmpt]:
                            ballerine += "<:noSkill:978458473018830858>"
                        else:
                            ballerine += "🔒"
                    ballerine += "\n\n"

                    icon = await getUserIcon(slash, usr)
                    points = ""
                    if usr.points > 0:
                        points = " *(+)*"
                    temp += f"__{icon} **{usr.name}** ({level})__{points}\n{ballerine}"
                if int(user.owner) == int(ctx.author.id):
                    emb = interactions.Embed(title="/team view", color=user.color,description="__Votre équipe se compose de :__\n\n"+temp)
                else:
                    emb = interactions.Embed(title="/team view", color=user.color,description="__L'équipe de {0} se compose de :__\n\n".format(user.name)+temp)

                if user.team != 0:
                    emb.add_field(name="<:empty:866459463568850954>\n__Résultats des derniers combats :__",value=teamWinDB.getVictoryStreakStr(user))

            else:
                embeds = await getFullteamEmbed(slash, teamMates, user)

            await msg.edit(embeds=emb, components=[interactions.ActionRow(components=[detailPlus, detailMinus][extended])])

            try:
                react = await slash.wait_for_component(msg, check=checky, timeout=60)
            except:

                await msg.edit(embeds=emb, components=[])
                break

            if react.custom_id == detailPlus["custom_id"]:
                extended = not(extended)

# team add
@slash.command(name="team_add", description="Permet de rajouter un joueur dans son équipe", options=[
    interactions.Option(name="joueur", description="Le joueur à rajouter", type=6, required=True)
])
async def teamAdd(ctx, joueur):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile)

        msg = await loadingSlashEmbed(ctx)

        if user.team == 0:
            rdm = str(random.randint(1, 999999999))
            while rdm in userTeamDb.getAllTeamIds():
                rdm = str(random.randint(1, 999999999))
            userTeamDb.updateTeam(rdm, [user])
            user.team = rdm
            saveCharFile(pathUserProfile, user)

        noneCap, selfAdd, temp = True, False, userTeamDb.getTeamMember(
            user.team)

        if len(temp) >= 8:
            noneCap = False

        if ctx.author == joueur:
            selfAdd = True

        if noneCap and not(selfAdd):
            mention = joueur
            if os.path.exists(absPath + "/userProfile/" + str(mention.id) + ".prof"):
                allReadyinTeam, allReadyInThatTeam, mate = False, False, loadCharFile(
                    absPath + "/userProfile/" + str(mention.id) + ".prof")
                if mate.team != 0:
                    allReadyinTeam = True
                    if mate.team == user.team:
                        allReadyInThatTeam = True

                if not(allReadyinTeam):
                    await msg.edit(embeds=interactions.Embed(title="/team add "+joueur.name, color=user.color, description=f"{mention.mention}, {ctx.author.mention} vous propose de rejoidre son équipe. Qu'en dites vous ?"))
                    await msg.add_reaction("✅")
                    await msg.add_reaction("❌")

                    def checkisIntendedUser(reaction, user):
                        return int(user.id) == int(mention.id)

                    try:
                        reaction = await slash.wait_for("reaction_add", timeout=60, check=checkisIntendedUser)
                    except:
                        await msg.remove_all_reactions()
                        await msg.edit(embeds=errorEmbed("/team add "+joueur.name, "La commande n'a pas pu aboutir"))

                    if str(reaction[0]) == "✅":
                        mate.team = user.team
                        saveCharFile(absPath + "/userProfile/" +
                                     str(mention.id) + ".prof", mate)
                        team = userTeamDb.getTeamMember(user.team)
                        team.append(mention.id)
                        userTeamDb.updateTeam(user.team, team)
                        await msg.remove_all_reactions()
                        await msg.edit(embeds=interactions.Embed(title="/team add "+joueur.name, color=user.color, description="Vous faites dorénavent parti de la même équipe"))

                elif allReadyInThatTeam:
                    await msg.edit(embeds=errorEmbed("/team add "+joueur.name, "Ce joueur est déjà dans ton équipe"))
                elif allReadyinTeam:
                    await msg.edit(embeds=errorEmbed("/team add "+joueur.name, "Ce joueur a déjà une équipe"))

            else:
                await msg.edit(embeds=errorEmbed("/team add "+joueur.name, "Cet utilisateur n'a pas commencé l'aventure"))
        elif selfAdd:
            await msg.edit(embeds=errorEmbed("/team add "+joueur.name, "Vous voulez faire équipe avec vous-même ?"))
        else:
            await msg.edit(embeds=errorEmbed("/team add "+joueur.name, "Votre équipe est déjà au complet"))

# team quit
@slash.command(name="team_quit", description="Permet de quitter son équipe")
async def teamQuit(ctx):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile)

    if user.team != 0:
        team = userTeamDb.getTeamMember(user.team)
        team.remove(ctx.author.id)
        user.team = 0

        userTeamDb.updateTeam(user.team, team)
        await ctx.send(embeds=interactions.Embed(title="/team quit", color=user.color, description="Vous avez bien quitté votre équipe"))
        saveCharFile(pathUserProfile, user)
    else:
        await ctx.send(embeds=errorEmbed("/team quit", "Vous n'avez aucune équipe à quitter"))

# team fact
@slash.command(name="team_fact", description="Permet d'avoir des facts sur les membres de votre équipe")
async def teamFact(ctx):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile)

    teamUser = []

    if user.team != 0:
        for a in userTeamDb.getTeamMember(user.team):
            teamUser.append(loadCharFile(
                absPath + "/userProfile/" + str(a) + ".prof"))

    else:
        teamUser.append(user)

    button = interactions.ActionRow(components=[interactions.Button(type=2, style=2, label="Autre fact", emoji=Emoji(name="🔄"), custom_id="🔄")])
    msg = None

    while 1:
        emb = await getRandomStatsEmbed(slash, teamUser, "/team fact")
        if msg == None:
            msg = await ctx.send(embeds=emb, components=[button])
        else:
            await msg.edit(embeds=emb, components=[button])

        try:
            await slash.wait_for_component(msg, timeout=60)
        except:
            await msg.edit(embeds=emb, components=[])
            break

# team settings
"""@slash.command(name_localizations="team", name="settings", description="Permet de modifier des paramètres d'équipes")
async def teamSetFunction(ctx):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile)
    team, msg = userTeamDb.getTeamMember(user.team), None
    teamSet = aliceStatsDb.getTeamSettings(user)

    if teamSet["teamLeader"] == None:
        buttons = interactions.ActionRow(components=[interactions.Button(type=2, style=ButtonStyle.SUCCESS,"Devenir Chef d'équipe","✅","becomeTeamLead"),interactions.Button(type=2, style=ButtonStyle.SECONDARY,"Passer son tour","❌","pass"))
        msg = await ctx.send(embeds=interactions.Embed(title="__Paramètres d'équipe__",color=user.color,description="Votre équipe ne possède pas encore de chef d'équipe.\nVoulez vous, {0} {1}, vous auto-proclamer comme chef d'équipe ?".format(await getUserIcon(slash,user),user.name)),components=[buttons])
        def check(m):
            return m.author.id == ctx.author.id
        
        try:
            rep = await slash.wait_for_component(msg,buttons,check,30)
            rep = rep.custom_id
        except:
            rep = "pass"
        
        if rep == "becomeTeamLead":
            teamSet["teamLeader"] = user.owner
            if aliceStatsDb.updateTeamSettings(user,teamSet):
                await msg.edit(embeds=interactions.Embed(title="__Paramètres d'équipe__",description="Vous êtes désormais le chef de votre équipe",color=user.color),components=[])
                await asyncio.sleep(3)
    
    leader = None
    for ent in team:
        if ent == teamSet["teamLeader"]:
            leader = loadCharFile(absPath + "/userProfile/" + str(ent) + ".prof")
            break
    repEmb = interactions.Embed(title="__Equipe {0}__".format(teamSet["teamName"]),color=user.color)
    baseInfo = "__ID. :__ {0}\n__Chef :__ {1}{2}\n__Capitaine :__ ".format(leader.team,await getUserIcon(slash,leader),leader.name)
    if teamSet["teamCaptain"] != None:
        baseInfo += "{0} {1}".format(capSkills[teamSet["teamCaptain"]]["icon"],capSkills[teamSet["teamCaptain"]]["name"])
        tablCapExp = [teamSet["teamCapLenaExp"],teamSet["teamCapClemenceExp"],teamSet["teamCapHeleneExp"],teamSet["teamCapShehisaExp"],teamSet["teamCapLiuExp"],teamSet["teamCapEdelweissExp"],teamSet["teamCapElinaExp"],teamSet["teamCapIcealiaExp"]]
        lvl = int(tablCapExp[teamSet["teamCaptain"]]>=CAP_EXP_LVL2) + int(tablCapExp[teamSet["teamCaptain"]]>=CAP_EXP_LVL3)
        baseInfo += "\n> {0}".format(capSkills[teamSet["teamCaptain"]]["desc"].format(capSkills[teamSet["teamCaptain"]]["lvlValue1"][lvl],capSkills[teamSet["teamCaptain"]]["lvlValue2"][lvl]).replace("\n","\n> "))
        baseInfo += "\n__Expérience du capitaine :__ {0}/{1}".format(["MAX",tablCapExp[teamSet["teamCaptain"]]][tablCapExp[teamSet["teamCaptain"]] < CAP_EXP_LVL2],[CAP_EXP_LVL2,CAP_EXP_LVL3,CAP_EXP_LVL3][lvl])
    else:
        baseInfo += "-\n__Expériance du capitaine :__ -"

    repEmb.add_field(name="__Résumé :__",value=baseInfo)

    if msg == None:
        msg = await ctx.send(embeds=repEmb)
    else:
        await msg.edit(embeds=repEmb)
"""
# -------------------------------------------- HELP --------------------------------------------
@slash.command(name="help", description="Ouvre la page d'aide du bot")
async def helpCom(ctx):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    await helpBot(slash, ctx)

# -------------------------------------------- START --------------------------------------------
@slash.command(name="start", description="Permet de commence l'aventure")
async def started(ctx):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    await start(slash, ctx)

# -------------------------------------------- STATS --------------------------------------------
@slash.command(name="stats", description="Permet de voir vos statistiques ou celles d'un autre joueur", options=[interactions.Option(name="joueur", description="Voir les statistiques d'un autre joueur", type=6, required=False)])
async def statsCmd(ctx, joueur=None):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    if joueur == None:
        pathUserProfile = absPath + "/userProfile/" + \
            str(ctx.author.id) + ".prof"
    else:
        pathUserProfile = absPath + "/userProfile/" + str(joueur.id) + ".prof"

    if os.path.exists(pathUserProfile):
        msg = await loadingSlashEmbed(ctx)
        user = loadCharFile(pathUserProfile)

        userIcon = await getUserIcon(slash, user)

        level = str(
            user.level)+['', "<:littleStar:925860806602682369>{0}".format(user.stars)][user.stars > 0]
        exp = [str(user.level*50-20), "MAX"][user.level == 55]
        rep = interactions.Embed(title=f"__Page de statistique de {user.name} {userIcon}__", color=user.color,description=f"__Niveau :__ {level}\n__Expérience :__ {user.exp} / {exp}\n\n__Element :__ {elemEmojis[user.element]} {elemNames[user.element]} ({elemEmojis[user.secElement]} {elemNames[user.secElement]})\n__Aspiration :__ {aspiEmoji[user.aspiration]} {inspi[user.aspiration]}")

        rep.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(userIcon).id))
        sumStatsBonus = [user.majorPoints[0], user.majorPoints[1], user.majorPoints[2], user.majorPoints[3], user.majorPoints[4], user.majorPoints[5], user.majorPoints[6], user.majorPoints[7], user.majorPoints[8], user.majorPoints[9], user.majorPoints[10], user.majorPoints[11], user.majorPoints[12], user.majorPoints[13], user.majorPoints[14]]

        for a in [user.weapon, user.stuff[0], user.stuff[1], user.stuff[2]]:
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
            sumStatsBonus[10] += a.negativeHeal * -1
            sumStatsBonus[11] += a.negativeBoost * -1
            sumStatsBonus[12] += a.negativeShield * -1
            sumStatsBonus[13] += a.negativeDirect * -1
            sumStatsBonus[14] += a.negativeIndirect * -1

        estimPV = separeUnit(round((130+user.level*15)*(int((user.endurance+sumStatsBonus[ENDURANCE]*(1+user.limitBreaks[ENDURANCE]/100)))/100+1)))
        value = "\n__PVs :__ {0}".format(estimPV)
        allStatsUser = user.allStats()+[user.resistance,user.percing,user.critical,user.majorPoints[ACT_BOOST_FULL],user.majorPoints[ACT_HEAL_FULL],user.majorPoints[ACT_SHIELD_FULL],user.majorPoints[ACT_DIRECT_FULL],user.majorPoints[ACT_INDIRECT_FULL]]
        for cmpt in range(0,MAGIE+1):
            userStats = int((allStatsUser[cmpt]+sumStatsBonus[cmpt]) * (1+user.limitBreaks[cmpt]/100))
            value += "\n{0} __{1}__ : {2}".format(statsEmojis[cmpt],allStatsNames[cmpt],userStats)
        rep.add_field(name="<:empty:866459463568850954>\n__Stats. principaux :__",value=value, inline=False)
        value = ""
        for cmpt in range(RESISTANCE,CRITICAL+1):
            value += "\n{0} __{1}__ : {2}".format(statsEmojis[cmpt],allStatsNames[cmpt],allStatsUser[cmpt]+sumStatsBonus[cmpt])
        rep.add_field(name="<:empty:866459463568850954>\n__Stats. secondaires :__",value=value, inline=True)
        value = ""
        for cmpt in range(ACT_HEAL_FULL,ACT_INDIRECT_FULL+1):
            value += "\n{0} __{1}__ : {2}".format(statsEmojis[cmpt],allStatsNames[cmpt],allStatsUser[cmpt]+sumStatsBonus[cmpt])
        rep.add_field(name="<:empty:866459463568850954>\n__Stats. d'actions :__",value=value, inline=True)
        tempStuff, tempSkill = "", ""
        
        for a in [0, 1, 2]:
            tempStuff += f"{user.stuff[a].emoji} {user.stuff[a].name}\n"

        for a in [0, 1, 2, 3, 4, 5, 6]:
            try:
                tempSkill += f"{user.skills[a].emoji} {user.skills[a].name}\n"
            except:
                if user.level >= lvlToUnlockSkill[a]:
                    tempSkill += " -\n"
                else:
                    tempSkill += " 🔒\n"

        rep.add_field(name="<:empty:866459463568850954>",value='**__Objets équipés :__**',inline=False)
        rep.add_field(name="__Arme et équipements :__",value=user.weapon.emoji+" "+user.weapon.name+"\n\n"+tempStuff, inline=True)
        rep.add_field(name="__Compétences :__",value=tempSkill, inline=True)

        await msg.edit(embeds=rep)

    else:
        if joueur == None:
            await ctx.send("Tu n'a pas commencé l'aventure")
        else:
            await ctx.send("{0} n'a pas commencé l'aventure".format(joueur.name))

# -------------------------------------------- MANUEL --------------------------------------------
@slash.command(name="manuel", description="Permet de consulter le manuel de l'Aventure", options=[
    interactions.Option(name="page", description="Spécifiez une page à laquelle ouvrir le manuel", type=4, required=False)
])
async def manuel(ctx, page=0):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    msg, manPage, chapterInt, ini = await loadingSlashEmbed(ctx), page, 0, True

    def checkReaction(reaction, user):
        return int(reaction.message.id) == int(msg.id) and int(user.id) == int(ctx.author.id) and (str(reaction) == "◀️" or str(reaction) =="▶️" or str(reaction) == '⏪' or str(reaction) == '⏩')

    while 1:
        if manPage < lenChapter[chapterInt]:
            chapterInt -= 1
        elif chapterInt != len(lenChapter)-1:
            if manPage >= lenChapter[chapterInt+1]:
                chapterInt += 1

        ballerine = interactions.Embed(title="__"+tablPage[manPage][0]+" :__", color=light_blue,
                                  description=tablPage[manPage][1]).set_footer(text=f"Page {manPage} / {len(tablPage)-1}")

        if len(tablPage[manPage]) == 3:
            ballerine.set_image(url=tablPage[manPage][2])

        await msg.edit(embeds=ballerine)
        if ini:
            await msg.add_reaction('⏪')
            await msg.add_reaction("◀️")
            await msg.add_reaction("▶️")
            await msg.add_reaction('⏩')
            ini = False

        reaction = None
        try:
            reaction = await slash.wait_for("reaction_add", timeout=380, check=checkReaction)
        except:
            await msg.remove_all_reactions()
            break

        if reaction != None:
            if str(reaction[0]) == "◀️":
                if manPage == 0:
                    manPage = len(tablPage)-1
                else:
                    manPage -= 1

            elif str(reaction[0]) =="▶️":
                if manPage == len(tablPage)-1:
                    manPage = 0
                else:
                    manPage += 1

            elif str(reaction[0]) == '⏪':
                if chapterInt == 0:
                    manPage = lenChapter[len(lenChapter)-1]
                else:
                    manPage = lenChapter[chapterInt]

            elif str(reaction[0]) == '⏩':
                if chapterInt == len(lenChapter)-1:
                    manPage = 0
                else:
                    manPage = lenChapter[chapterInt+1]

            await msg.remove_reaction(str(reaction[0]), reaction[1])

# -------------------------------------------- SEE LOGS --------------------------------------------
@slash.command(name="see_fightlogs", description="Permet de consulter les logs des combats du jour", scope=[615257372218097691])
async def seeLogs(ctx):
    listLogs = os.listdir("./data/fightLogs/")
    listLogs.sort(key=lambda name: name[-8:])

    page = 0
    maxPage = len(listLogs) // 24
    msg = None
    while 1:
        desc = "__Page **{0}** / {1} :__\n".format(page+1, maxPage+1)
        option = []
        maxi = min(len(listLogs), (page+1)*24)
        for log in listLogs[page*24:maxi]:
            desc += "> - {0}\n".format(log)
            option.append(interactions.SelectOption(log, log))

        emb = interactions.Embed(
            title="__Logs des combats du jour__", color=light_blue, description=desc)

        if len(option) > 0:
            select = interactions.SelectMenu(custom_id = "seeFightLogs", options =option)
        else:
            select = interactions.SelectMenu(custom_id = "seeFightLogs", options= [interactions.SelectOption(label="disabled", value="0")], placeholder="Il n'y a aucun logs à afficher", disabled=True)

        if page != 0:
            previousBoutton = interactions.Button(type=2, style=ButtonStyle(2), label="Page précédente", emoji=Emoji(name="◀️"), custom_id="back")
        else:
            previousBoutton = interactions.Button(type=2, style=ButtonStyle(2), label="Page précédente", emoji=Emoji(name="◀️"), custom_id="back", disabled=True)
        if page != maxPage:
            nextBoutton = interactions.Button(type=2, style=ButtonStyle(2), label="Page suivante", emoji=Emoji(name="▶️"), custom_id="forward")
        else:
            nextBoutton = interactions.Button(type=2, style=ButtonStyle(2), label="Page suivante", emoji=Emoji(name="▶️"), custom_id="forward", disabled=True)

        buttons = interactions.ActionRow(components=[previousBoutton, nextBoutton])

        if msg == None:
            try:
                msg = await ctx.send(embeds=emb, components=[interactions.ActionRow(components=[select]), buttons])
            except:
                msg = await ctx.channel.send(embeds=emb, components=[interactions.ActionRow(components=[select]), buttons])
        else:
            await msg.edit(embeds=emb, components=[interactions.ActionRow(components=[select]), buttons])

        try:
            respond = await slash.wait_for_component(msg, timeout=180)
        except:
            break

        try:
            resp = respond.data.values[0]
        except:
            resp = respond.custom_id
        if resp not in ["back", "forward"]:
            opened = open("./data/fightLogs/{0}".format(resp), "rb")
            try:
                await respond.send("Voici les logs du combat :", file=interactions.File(filename=resp,fp=opened))
            except:
                await ctx.channel.send("Voici les logs du combat :", file=interactions.File(filename=resp,fp=opened))
            opened.close()
        elif resp == "back":
            page -= 1
        elif resp == "forward":
            page += 1

# -------------------------------------------- SEE STUFF --------------------------------------------
@slash.command(name="see_stuffrepartition", description="Permet de consulter la réportation des logs", scope=[615257372218097691])
async def seeStuffRepartition(ctx):
    rep = "=============================================="
    temp = copy.deepcopy(stuffs)
    temp.sort(key=lambda ballerine: ballerine.minLvl)
    allreadySeenLvl = []
    for a in temp:
        if a.minLvl not in allreadySeenLvl:
            allreadySeenLvl.append(a.minLvl)
            rep += "\n__Stuff de niveau {0} :__\n\n".format(a.minLvl)
        rep += "{0} {1}\n".format(a.emoji, a.name)

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

ssrTypeChoice = []
for cmpt in range(TYPE_DEPL+1):
    ssrTypeChoice.append(Choice(name=tablTypeStr[cmpt],value=cmpt))
ssrAspiChoice = []
for cmpt in range(MASCOTTE+1):
    ssrAspiChoice.append(Choice(name=inspi[cmpt],value=cmpt))
ssrElemChoice = []
for cmpt in range(ELEMENT_TIME+1):
    ssrElemChoice.append(Choice(name=elemNames[cmpt],value=cmpt))
ssrUseChoice = []
for cmpt in range(MAGIE+1):
    ssrUseChoice.append(Choice(name=nameStats[cmpt],value=cmpt))

@slash.command(name="see_skill_repartition",scope=adminServ,options=[
    Option(type=OptionType.INTEGER,name="skilltype",required=True,choices=ssrTypeChoice,description="Le type de compétence à voir"),
    Option(type=OptionType.INTEGER,name="aspiration",choices=ssrAspiChoice,description="Afficher les compétences exclusives à une aspiration"),
    Option(type=OptionType.INTEGER,name="element",choices=ssrElemChoice,description="Afficher les compétences exclusives à un élément"),
    Option(type=OptionType.INTEGER,name="use",choices=ssrUseChoice,description="Afficher uniquement les compétences utilisant une statistique"),
    Option(type=OptionType.INTEGER,name="skillrange",choices=[Choice(name="Mêlée",value=0),Choice(name="Distance",value=1)],description="Afficher uniquement les compétences avec une portée spécifique")
])
async def seeSkillRepartition(ctx: interactions.CommandContext, skilltype: int, aspiration: Union[int, None] = None, element: Union[int, None] = None, use: Union[int,None] = None, skillrange: Union[int, None] = None):
    await ctx.defer()
    try:
        await seeSkillsRep(ctx, skilltype, aspiration, element, use, skillRange)
    except Exception as e:
        await ctx.send(content=e.__str__())

# -------------------------------------------- CHOOSE --------------------------------------------
@slash.command(name="choose", description="Renvoie une élément aléatoire de la liste donnée", options=[
    interactions.Option(name="choix1", description="Le premier élément de la liste",type=interactions.OptionType.STRING, required=True),
    interactions.Option(name="choix2", description="Le second élément de la liste",type=interactions.OptionType.STRING, required=True),
    interactions.Option(name="choix3", description="Un potentiel troisième de la liste",type=interactions.OptionType.STRING, required=False),
    interactions.Option(name="choix4", description="Un potentiel quatrième de la liste",type=interactions.OptionType.STRING, required=False),
    interactions.Option(name="choix5", description="Un potentiel cinquième de la liste",type=interactions.OptionType.STRING, required=False)
])
async def chooseCmd(ctx, choix1, choix2, choix3=None, choix4=None, choix5=None):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    tempTabl = [choix1, choix2]
    for a in [choix3, choix4, choix5]:
        if a != None:
            tempTabl.append(a)

    selected = tempTabl[random.randint(0, len(tempTabl)-1)]
    while selected.endswith(" "):
        selected = selected[:-1]
    while selected.startswith(" "):
        selected = selected[1:]
    await ctx.send(embeds=interactions.Embed(title="/choose", color=light_blue, description="{0} :\n__{1}__".format(randChooseMsg[random.randint(0, len(randChooseMsg)-1)], selected)))

# -------------------------------------------- ADMIN --------------------------------------------
@slash.command(name="admin_enable_fight", scope=adminServ, description="Permet d'activer les combats ou non", options=[
    interactions.Option(name="valeur", description="Activer ou désaciver les combats", type=OptionType.BOOLEAN, required=False)
])
async def addEnableFight(ctx, valeur=None):
    globalVar.changeFightEnabled(valeur)
    if valeur == None:
        valeur = globalVar.fightEnabled()

    if not(valeur):
        await slash.change_presence(ClientPresence(status=StatusType.DND,activities=[PresenceActivity(name="Les combats sont désactivés",type=PresenceActivityType.GAME)]))
    else:
        ballerine = datetime.now() + horaire + timedelta(hours=1)
        while ballerine.hour % 3 != 0:
            ballerine = ballerine + timedelta(hours=1)

        await slash.change_presence(ClientPresence(status=StatusType.ONLINE,activities=[PresenceActivity(name="Prochain shop à "+ballerine.strftime('%Hh'),type=PresenceActivityType.GAME)]))

    await ctx.send(embeds=interactions.Embed(title="__Admin Enable Fight__", description="Les combats sont désormais __{0}__".format(["désactivés", "activés"][int(valeur)]), color=[red, light_blue][int(valeur)]))


@slash.command(name="admin_restart_bot", scope=adminServ, description="Permet de redémarrer le bot lorsque tous les combats seront fini")
async def restartCommand(ctx):
    await restart_program(slash, ctx)

@slash.command(name="admin_emoji_reset_all", scope=adminServ, description="Lance une rénitialisation des emojis")
async def resetCustomEmoji(ctx):
    msg = await ctx.send(embeds=interactions.Embed(title="Rénitialisation des emojis..."))
    await slash.change_presence(ClientPresence(status=StatusType.IDLE,activities=[PresenceActivity(name="Refaire les émojis...",type=PresenceActivityType.GAME)]))

    async def refresh(text: str):
        await msg.edit(embeds=interactions.Embed(title="Rénitialisation des emojis...", description=text))

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
        emojiGuild = await get(slash,interactions.Guild,a)
        allEmojisNum += len(emojiGuild.emojis)

    cmpt = 0
    now = datetime.now().second
    lastTime = copy.deepcopy(now)
    for a in iconGuildList:
        emojiGuild = await get(slash,interactions.Guild,a)

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
    base = open("./data/database/custom_icon.db", "w")
    base.close()
    customIconDB.remarkeCustomDB()
    await downloadAllHeadGearPng(slash, msg, lastTime)
    await downloadAllWeapPng(slash, msg, lastTime)
    await refresh("Téléchargements des icones de bases...")
    await downloadAllIconPng(bot)
    await downloadElementIcon(bot)

    allChar = os.listdir("./userProfile/")
    lenAllChar = len(allChar)
    cmpt = 0

    await refresh("Création des émojis...")
    for num in allChar:
        user = loadCharFile("./userProfile/"+num)
        await getUserIcon(slash, user)
        cmpt += 1

        if now >= lastTime + 3 or (now <= 3 and now >= lastTime + 3 - 60):
            await refresh("Création des émojis ({0} %)".format(int(cmpt/lenAllChar*100)))
            lastTime = now

    await refresh("Fini !")
    await ctx.channel.send("La rénitialisation des emojis est terminées !")

    ballerine = datetime.now() + horaire + timedelta(hours=1)
    while ballerine.hour % 3 != 0:
        ballerine = ballerine + timedelta(hours=1)

    await slash.change_presence(ClientPresence(status=StatusType.ONLINE,activities=[PresenceActivity(name="Prochain shop à "+ballerine.strftime('%Hh'),type=PresenceActivityType.GAME)]))

@slash.command(name="admin_emoji_remake_all", scope=adminServ, description="Supprime puis refait tous les emojis de personnage")
async def remakeCustomEmoji(ctx):
    await remakeEmojis(ctx)

@slash.command(name="admin_backup_new", description="Permet de réaliser un backup des profiles de personnages", scope=adminServ)
async def adminBackup(ctx):
    temp = create_backup()
    try:
        await ctx.send(embeds=interactions.Embed(title="__Admin : Backups__", color=light_blue, description=temp))
    except:
        await ctx.channel.send(embeds=interactions.Embed(title="__Admin : Backups__", color=light_blue, description=temp))

@slash.command(name="admin_stat_silent_restat_all", description="silentRestat all users", scope=adminServ)
async def silentRestatForEveryone(ctx):
    msg = await ctx.send(embeds=interactions.Embed(title="__/admin stat silentRestallAll__", color=light_blue, description="Restats en cours..."))
    try:
        for fileName in os.listdir("./userProfile/"):
            user = loadCharFile("./userProfile/"+fileName)
            user = silentRestats(user)
            saveCharFile(user=user)
        await msg.edit(embeds=interactions.Embed(title="__/admin stat silentRestallAll__", color=light_blue, description="Tous les utilisateurs ont été restats 👍"))
    except:
        await msg.edit(embeds=interactions.Embed(title="__/admin stat silentRestallAll__", description="Une erreur est survenue :\n"+format_exc()))

@slash.command(name="admin_force_new_shop", description="silentRestat all users", scope=adminServ)
async def forceShop(ctx):
    try:
        await shopping.newShop()
        await ctx.send("Succès")
    except:
        await ctx.send("Echec")

@slash.command(name="admin_reset_records", scope=adminServ)
async def resetRecord(ctx):
    await ctx.send(embeds=interactions.Embed(title="__Reset des records__", color=light_blue, description=aliceStatsDb.resetRecords()))

# -------------------------------------------- KIKIMETER --------------------------------------------
if isLenapy:
    tabl = [912137828614426704, 405331357112205326]
else:
    tabl = adminServ

@slash.command(name="kikimeter", description="Permet de voir le top 5 de chaques catégories", scope=tabl, options=[interactions.Option(name="what", description="Que regarder", type=3, required=True, choices=[interactions.Choice(name="total", value="total"), interactions.Choice(name="max", value="max")])])
async def kikimeterCmd(ctx, what):
    listAllChars = []
    for text in os.listdir("./userProfile/"):
        listAllChars.append(loadCharFile("./userProfile/" + text))

    for cmpt in range(len(listAllChars)):
        temp = aliceStatsDb.getUserStats(listAllChars[cmpt], "all")
        listAllChars[cmpt] = {"char": listAllChars[cmpt], "{what}Damage".format(what=what): temp["{what}Damage".format(what=what)], "{what}Kill".format(what=what): temp["{what}Kill".format(what=what)], "{what}Resu".format(what=what): temp["{what}Resu".format(what=what)], "{what}RecivedDamage".format(
            what=what): temp["{what}RecivedDamage".format(what=what)], "{what}Heal".format(what=what): temp["{what}Heal".format(what=what)], "{what}Armor".format(what=what): temp["{what}Armor".format(what=what)], "{what}Supp".format(what=what): temp["{what}Supp".format(what=what)]}

    emb = interactions.Embed(
        title="__Kikimeter__", description="=========================================================")
    for cat in ["{what}Damage".format(what=what), "{what}Kill".format(what=what), "{what}Resu".format(what=what), "{what}RecivedDamage".format(what=what), "{what}Heal".format(what=what), "{what}Armor".format(what=what), "{what}Supp".format(what=what)]:
        listAllChars.sort(
            key=lambda character: character["{0}".format(cat)], reverse=True)
        desc = ""

        for cmpt in range(min(5, len(listAllChars)-1)):
            if listAllChars[cmpt]["{0}".format(cat)] > 0:
                desc += "{0} - {1} {2} ({3})\n".format(cmpt+1, await getUserIcon(slash, listAllChars[cmpt]["char"]), listAllChars[cmpt]["char"].name, separeUnit(int(listAllChars[cmpt]["{0}".format(cat)])))

        if desc != "":
            emb.add_field(
                name="<:empty:866459463568850954>\n__{0}__".format(cat), value=desc)
    try:
        await ctx.send(embeds=emb)
    except:
        await ctx.channel.send(embeds=emb)

# -------------------------------------------- PROCURATION --------------------------------------------
@slash.command(name="procuration", description="Permet de donner à un autre utilisateur procuration sur votre inventaire", options=[interactions.Option(name="utilisateur", description="L'utilisateur qui pourra modifier vos objets équipés", type=6, required=True)])
async def procurCmd(ctx, utilisateur):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    await procuration(ctx, utilisateur)

# -------------------------------------------- ICON --------------------------------------------
@slash.command(name="icon", description="Renvoie l'icone de votre personnage", options=[interactions.Option(name="utilisateur", description="Voir l'icone d'un autre utilisateur", type=6, required=False)])
async def iconCommand(ctx, utilisateur=None):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    try:
        if utilisateur == None:
            user = loadCharFile("./userProfile/{0}.prof".format(ctx.author.id))
        else:
            user = loadCharFile(
                "./userProfile/{0}.prof".format(utilisateur.id))
    except:
        if utilisateur == None:
            await ctx.send("Vous devez avoir commencé l'Aventure pour utiliser cette commande\nFaites donc un tour du côté de /start !",ephemeral=True)
        else:
            await ctx.send("La personne mentionnée n'a pas commencé l'aventure",ephemeral=True)
        return 0

    emb = interactions.Embed(title="__Icone de personnage__", color=user.color)
    emb.set_image(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(await getUserIcon(slash, user)).id))

    await ctx.send(embeds=emb)

# -------------------------------------------- ADVENTURE ---------------------------------------------

# -------------------------------------------- ROULETTE --------------------------------------------
@slash.command(name="roulette", description="Permet d'utiliser un Jeton de roulette pour obtenir un objet ou des pièces")
async def rouletteSlash(ctx):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    try:
        user = loadCharFile("./userProfile/{0}.prof".format(ctx.author.id))
    except:
        await ctx.send(embeds=interactions.Embed(title="__Commande de l'Aventure :__", description="Vous devez avoir commencé l'aventure pour utiliser cette commande.\n\nFaites donc un tour vers /start"),ephemeral=True)
        return 0

    await roulette(slash, ctx, user)

# -------------------------------------------- SEE ENEMY REPARTITION -------------------------------
@slash.command(name="see_enemy_repartition", scope=[615257372218097691], description="Permet de voir la répartition des ennemis")
async def seeEnnemyRep(ctx):
    # 0 : Dmg; 1 : Heal/Armor; 2 : Buff/Debuff
    octoRolesNPos = [[[], [], []], [[], [], []], [[], [], []]]
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

    for cmpt in (0, 1, 2):
        emb = interactions.Embed(title="__Ennemi répartion : {0}__".format(
            ["DPT_PHYS", "Healer/Shilder", "Support"][cmpt]), color=light_blue)
        for cmptBis in range(len(octoRolesNPos[cmpt])):
            desc = ""
            for name in octoRolesNPos[cmpt][cmptBis]:
                desc += "{0} {1}\n".format(name.icon, name.name)
            if len(desc) > 0:
                emb.add_field(name=["__Mêlée :__", "__Distance :__",
                                "__Backline :__"][cmptBis], value=desc, inline=True)
            else:
                emb.add_field(name=["__Mêlée :__", "__Distance :__",
                                "__Backline :__"][cmptBis], value="`-`", inline=True)

        if cmpt == 0:
            await ctx.send(embeds=emb)
        else:
            await ctx.channel.send(embeds=emb)

    desc = ''
    for name in dicidants:
        desc += "{0} {1}\n".format(name.icon, name.name)
    emb = interactions.Embed(title="__Hors catégorie :__".format(
        ["DPT_PHYS", "Healer/Shilder", "Support"][cmpt]), color=light_blue, description=desc)

    await ctx.channel.send(embeds=emb)

@slash.command(name="see_enemy",description="Permet d'afficher la page d'info d'un ennemi",scope=adminServ,options=[Option(type=OptionType.STRING,name="name",description="Le nom de l'ennemi",focused=True,required=True)])
async def seeEnemy(ctx:CommandContext,name:str):
    await ctx.defer()
    badGuy = findEnnemi(name)
    emptyUser = char(owner=int(ctx.author.id))
    if badGuy != None:
        listOption = []
        for skilly in badGuy.skills:
            if type(skilly) == skill:
                listOption.append(SelectOption(label=skilly.name,value=skilly.id,emoji=getEmojiObject(skilly.emoji)))
        
        select = SelectMenu(custom_id="seeEnemySkill",options=listOption,placeholder="Voir une compétence en détail")
        emb = infoEnnemi(badGuy)
        msg = await ctx.send(embeds=emb,components=[select])

        while 1:
            try:
                rep: ComponentContext = await slash.wait_for_component(components=select,messages=msg,timeout=180)
            except asyncio.TimeoutError:
                await msg.edit(embeds=emb,components=[])
                break

            await rep.defer()
            for skilly in badGuy.skills:
                if type(skilly) == skill and skilly.id == rep.data.values[0]:
                    await rep.send(embeds=infoSkill(skill=skilly,ctx=rep,user=emptyUser))

    else:
        await ctx.send(content="L'ennemi \"{0}\" n'a pas été trouvé".format(name))

# ------------------------------------------- PRESTIGE ---------------------------------------------
@slash.command(name="prestige", description="Permet de revenir au niveau 1, avec quelques bonus en primes")
async def prestigeCmd(ctx):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    try:
        user = loadCharFile("./userProfile/{0}.prof".format(ctx.author.id))
    except:
        await ctx.send("Vous n'avez même pas encore commencé l'aventure et vous voulez déjà prestige ?",ephemeral=True)
        return 0

    if user.level < 55:
        await ctx.send("Vous devez être niveau 55 pour pouvoir utiliser cette commande",ephemeral=True)
        return 0

    emb = interactions.Embed(title="__Prestige__", color=light_blue,description="En prestigeant votre personnage, vous retournerez au niveau 1<:littleStar:925860806602682369>{0}.\n\nVous conserverez votre inventaire d'objet des de compétences et obtiendrez un __Point Majeur__.\nVous pourrez l'utiliser pour augmenter une de vos statistiques principales de 30 points supplémentaires, ou augmenter vos statistiques secondaires de 10 points".format(user.stars+1))
    comfirm = interactions.Button(type=2, style=ButtonStyle.SUCCESS, label="Prestige votre personnage", emoji=Emoji(name='✅'), custom_id='✅')

    msg = await ctx.send(embeds=emb, components=[interactions.ActionRow(components=[comfirm])])

    def check(m):
        return int(m.author.id) == int(ctx.author.id)

    try:
        await slash.wait_for_component(msg, check=check, timeout=30)
    except:
        await msg.edit(embeds=emb, components=[])
        return 0

    user = loadCharFile(user=user)
    user.level, user.exp, user.stars = 1, 0, user.stars+1
    user = restats(user)

    saveCharFile(user=user)
    await makeCustomIcon(slash, user)
    await inventoryVerif(slash, user)
    await msg.edit(embeds=interactions.Embed(title="__Prestige__", color=light_blue, description="Vous avez bien prestige votre personnage"), components=[])

# ------------------------------------------- SET_BOT_CHANNEL --------------------------------------
@slash.command(name="set_bot_channel", description="Permet de définir un salon comme salon bot", options=[interactions.Option(name="salon", description="Le salon dans lequel les utilisateurs pourront utiliser les commandes", type=7, required=True)])
async def setChannel(ctx: interactions.CommandContext, salon: interactions.Channel):
    if not(ctx.author.guild_permissions.manage_channels):
        await ctx.send(embeds=interactions.Embed(title="__/set_bot_channel__", color=red, description="Tu as besoin des permissions de gérer les salons textuels pour utiliser cette commande, désolée"),ephemeral=True)
        return 0
    if type(salon) != interactions.Channel:
        await ctx.send(embeds=interactions.Embed(title="__/set_bot_channel__", color=red, description="Seul un salon textuel peut être rajouté comme salon bot, désolée"),ephemeral=True)
        return 0

    globalVar.setGuildBotChannel(ctx.guild_id, salon.id)
    await ctx.send(embeds=interactions.Embed(title="__/set_bot_channel__", color=light_blue, description="Le salon {0} a bien été enregistré comme salon bot\nChaque serveur ne peut avoir qu'un seul salon bot, réutiliser la commande remplacera l'ancien".format(salon.mention)))

# ------------------------------------------- VERIF ------------------------------------------------
@slash.command(name="verif_user", description="Permet de voir toutes les informations d'un personnage", scope=adminServ, options=[interactions.Option(name="identifiant", description="L'identifiant de l'utilisateur", type=OptionType.STRING, required=True)])
async def verifuser(ctx, identifiant):
    user = loadCharFile("./userProfile/{0}.prof".format(identifiant))
    await ctx.send(embeds=await seeAllInfo(slash, user))

@slash.command(name="verif_team", scope=adminServ)
async def verifTeams(ctx):
    toSend, allReadySeen, msg, userTeam = "", [], None, []

    def getUserMainTeam(user: char):
        for look in userTeam:
            if look[0] == user.owner:
                return int(look[1])

    for team in userTeamDb.getAllTeamIds():
        temp = "__Team **{0}** :__".format(team)
        teamMembers = userTeamDb.getTeamMember(team)

        tmpTeamMembers = teamMembers[:]
        for ids in teamMembers:
            user = loadCharFile(path="./userProfile/{0}.prof".format(ids))
            if user.owner in allReadySeen:
                warn = "~~"
                if getUserMainTeam(user) != team:
                    tmpTeamMembers.remove(str(user.owner))
            else:
                warn = ""
                allReadySeen.append(user.owner)
                userTeam.append([user.owner, team])

            if user.team != team:
                user.team = team
                saveCharFile(user=user)
                redacted = " 📎"
            else:
                redacted = ""

            temp += "\n{2}{0} {1}{2}{3}".format(await getUserIcon(slash, user), user.name, warn, redacted)

        if len(tmpTeamMembers) > 0:
            userTeamDb.updateTeam(team, tmpTeamMembers)

        temp += "\n"
        if len(toSend+temp) > 4000:
            if msg == None:
                try:
                    msg = await ctx.send(embeds=interactions.Embed(title="__Team Vérification__", color=light_blue, description=toSend))
                except:
                    msg = await ctx.channel.send(embeds=interactions.Embed(title="__Team Vérification__", color=light_blue, description=toSend))
            else:
                await ctx.channel.send(embeds=interactions.Embed(title="__Team Vérification__", color=light_blue, description=toSend))
            toSend = temp
            temp = ""
        else:
            toSend = toSend + temp + "\n"

    if toSend != "":
        if msg == None:
            try:
                msg = await ctx.send(embeds=interactions.Embed(title="__Team Vérification__", color=light_blue, description=toSend))
            except:
                msg = await ctx.channel.send(embeds=interactions.Embed(title="__Team Vérification__", color=light_blue, description=toSend))
        else:
            await ctx.channel.send(embeds=interactions.Embed(title="__Team Vérification__", color=light_blue, description=toSend))

@slash.command(name="verif_emoji", scope=adminServ)
async def emojiVerficition(ctx):
    msg, remaked, lastProgress = await ctx.send(embeds=interactions.Embed(title="Vérification des émojis...", description="__Progression :__ 0%")), "", 0
    listAllUsersFiles = os.listdir("./userProfile/")
    lenAllUser, progress = len(listAllUsersFiles), 0
    try:
        for path in listAllUsersFiles:
            user, haveSucced = loadCharFile("./userProfile/"+path), False
            userIcon = await getUserIcon(slash, user)
            haveSucced = False
            for guildId in [ShushyCustomIcons, LenaCustomIcons][isLenapy]:
                guild = await get(slash,interactions.Guild,guildId)
                try:
                    await get(slash, interactions.Emoji, parent_id=int(guild.id), object_id=getEmojiObject(userIcon).id)
                    haveSucced = True
                    break
                except:
                    pass
            if not(haveSucced):
                customIconDB.removeUserIcon(user)
                await makeCustomIcon(slash, user)
                if await getUserIcon(slash, user) not in ['<:LenaWhat:760884455727955978>', '<a:lostSilver:917783593441456198>']:
                    remaked += "Emoji de {0} refait\n".format(user.name)
                else:
                    remaked += "Erreur lors du remake de l'emoji de {0}\n".format(
                        user.name)
            progress += 1

            if progress/lenAllUser * 100 > lastProgress + 5:
                await msg.edit(embeds=interactions.Embed(title="Vérification des émojis...", description="__Progression :__ {0}%\n".format(round(progress/lenAllUser * 100, 2))+remaked))
                lastProgress = progress/lenAllUser * 100

        await msg.edit(embeds=interactions.Embed(title="Vérification des émojis", description="__Progression :__ Terminé\n"+remaked, color=light_blue))
    except:
        await msg.edit(embeds=interactions.Embed(title="Vérification des émojis", description="__Interrompue__\n"+format_exc(), color=red))

# ------------------------------------------ CHAR SETTINGS ----------------------------------------
@slash.command(name="char_settings", description="Permet de modifier les paramètres de son icone de personnage")
async def char_settings(ctx):
    user = loadCharFile("./userProfile/{0}.prof".format(ctx.author.id))
    await userSettings(slash, user, ctx)

# ======================= Limit Breaks ================================
@slash.command(name="limitbreaks",description="Permet de briser les limites de votre personnage",options=[interactions.Option(name="procuration", description="Permet d'utiliser la commande avec un autre personnage", type=6, required=False)])
async def limitBreak(ctx,procuration:interactions.Member=None):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    try:
        user = loadCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof")
    except:
        await ctx.send("Vous n'avez pas encore de personnage.\nVous pouvez vous en créer un à l'aide de la commande /start",ephemeral=True)
        return 0

    if procuration != None:
        if procuration.id not in user.haveProcurOn:
            await ctx.send("{0} ne vous a pas donné procuration sur son personnage".format(procuration.nick),ephemeral=True)
            return 0
        else:
            user = loadCharFile(absPath + "/userProfile/" + str(procuration.id) + ".prof")

    if user.level < 40 and user.stars <= 0:
        hasSkillUpdated, lvl = True, user.level - 5
        nbExpectedSkills, nbSkills = 0, 0
        for cmpt in range(len(lvlToUnlockSkill)):
            if lvl >= lvlToUnlockSkill[cmpt]:
                nbExpectedSkills += 1

        for skilly in user.skills:
            if type(skilly) == skill:
                nbSkills += 1
        
        hasSkillUpdated = nbSkills >= nbExpectedSkills
        hasUpdatedStuff = True
        for stuffy in user.stuff:
            if stuffy.minLvl < user.level-10:
                hasUpdatedStuff = False
                break

        hasBonusPointsUpdated, updateBonus = user.points < 5, ""

        if not(hasBonusPointsUpdated and hasSkillUpdated and hasUpdatedStuff):
            updateBonus += "__Bonus de personnage à jour :__\nComplétez les conditions suivantes pour obtenir un bonus de 5% dans toutes vos satistiques principales :\n"
            updateBonus += "{0} {1}Avoir moins de **5 points bonus** non attribués{1}\n".format(["❌","✅"][hasBonusPointsUpdated],["","~~"][hasBonusPointsUpdated])
            updateBonus += "{0} {1}Avoir moins des équipements à votre niveau ou maximum **10 niveaux** en dessous du votre{1}\n".format(["❌","✅"][hasUpdatedStuff],["","~~"][hasUpdatedStuff])
            updateBonus += "{0} {1}Avoir **aucun** d'emplacement de compétences vides, à l'exeption du dernière emplacement sur il a été débloqué réçament{1}\n".format(["❌","✅"][hasSkillUpdated],["","~~"][hasSkillUpdated])

        await ctx.send("Vous ne pourrez briser vos limites qu'à partir du Niveau 40\n\n"+updateBonus,ephemeral=True)
        return 0
    await breakTheLimits(slash, ctx, user)

# ------------------------------------------ STREAM ----------------------------------------
@slash.command(name="twitch_alerts",description="Permet de gérer les alertes streams")
async def lenaTwitchAlerte(ctx):
    await streamSettingsFunction(slash,ctx.guild,ctx)

@slash.command(name="test", scope=adminServ)
async def expeditionTest(ctx):
    user, chan = loadCharFile(
        "./userProfile/{0}.prof".format(ctx.author.id)), ctx.channel
    listEmbed = await generateExpeditionReport(slash, [user], user, datetime.now(), ctx)
    for a in listEmbed:
        await chan.send(embeds=a)

@slash.command(name="area_test",scope=adminServ)
async def areaTest(ctx):
    first = True
    for area in [AREA_BOMB_5,AREA_BOMB_6,AREA_BOMB_7,]:
        emb = interactions.Embed(title=areaNames[area],color=light_blue)
        if area not in notOrientedAreas:
            for cmpt in (0,1,2,3):
                emb.add_field(name=["__From Left__","__From Right__","__From Up__","__From Down__"][cmpt],value=visuArea(area,ENEMIES,False,cmpt),inline=False)
            if first:
                await ctx.send(embeds=emb)
                first = False
            else:
                await ctx.channel.send(embeds=emb)
        else:
            emb.add_field(name=areaNames[area],value=visuArea(area,ENEMIES,True),inline=False)
            if first:
                await ctx.send(embeds=emb)
                first = False
            else:
                await ctx.channel.send(embeds=emb)
            
###########################################################
# Démarrage du bot
print(["\nKawiiiiii","\nIl semblerait que je sois seule cette fois. Je m'occuperais de Shushi une autre fois"][isLenapy])
try:
    slash.start()
except Exception as e:
    print("La connexion a écouché :")
    print(e)

