##########################################################
# Importations :
import asyncio
import datetime
import os
import random
import shutil
import sys

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
from commands_files.achievement_handler import *
from commands_files.cmd_twitch import *
from commands_files.command_osamodas import *
from data.bot_tokens import lenapy, shushipy
from data.database import *
from donnes import *
from gestion import *
from datetime import datetime


###########################################################
# Initialisations des variables de bases :
started = False
slash = interactions.Client(token=[shushipy,lenapy][isLenapy],intents=Intents.ALL,send_command_tracebacks=False, disable_dm_commands=True)

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

async def test():
    usr: interactions.User = await slash.get_user(623211750832996354)
    print(usr.avatar)

###########################################################
# Initialisation
allShop = weapons + skills + stuffs + others

allieBDay, toDay = None, datetime.now(parisTimeZone)
for ally in tablAllAllies:
    if ally.birthday == (toDay.day, toDay.month):
        print("{0} bday !".format(ally.name))
        allieBDay = ally
        break

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
            haveShop = False
            while not(haveShop):
                shopping = list(range(0, len(self.shopping)))
                shopWeap, shopSkill, shopStuff, ShopOther = [], [], [], []

                for obj in listAllBuyableShop+others[:]:
                    if obj.price > 0:
                        [shopWeap, shopSkill, shopStuff, ShopOther][whatIsThat(obj)].append(obj)
                
                temp = shopRepatition
                tablShop: List[list[Union[weapon, skill, stuff, other]]] = [shopWeap, shopSkill, shopStuff, ShopOther]
                cmp = 0
                for a in [0, 1, 2, 3]:
                    cmpt = 0
                    while cmpt < temp[a]:
                        fee = random.randint(0, len(tablShop[a])-1)
                        shopping[cmp] = tablShop[a][fee]
                        tablShop[a].remove(tablShop[a][fee])
                        cmpt += 1
                        cmp += 1

                haveShop = stuffDB.addShop(shopping)
                self.shopping = shopping
            
            if globalVar.fightEnabled():
                babies = datetime.now(parisTimeZone)
                while babies.hour % 3 != 0:
                    babies = babies + timedelta(hours=1)

                if allieBDay == None:
                    await slash.change_presence(status=Status.ONLINE,activity=Activity(name="Prochain shop : "+babies.strftime('%Hh'),type=ActivityType.GAME))
                else:
                    await slash.change_presence(status=Status.ONLINE,activity=Activity(name="Anniversaire de {0} !".format(allieBDay.name),type=ActivityType.GAME))
            return True
        except:
            print_exc()
            return False

async def inventoryVerif(slash: interactions.Client, toVerif: Union[char, str]):
    if type(toVerif) == str:
        try:
            user = loadCharFile(absPath + "/userProfile/" + toVerif)
        except Exception as e:
            line = format_exc().splitlines()[-4]
            print("Couldn't load the profile {0}:\n{2}\n{1}\n===".format(toVerif,e,line))
            return 0
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

    hadChange = []
    for indx, obj in enumerate(user.stuff):
        if findStuff(obj) == None:
            user.stuff[indx] = getAutoStuff(getStuffSet(["Plugiliste Légendaire","Sniper Légendaire","Assassin de l'Ombre Nocturne","Chanteur Légendaire","Armurier Légendaire","Plugiliste Légendaire","Mage écarlate Légendaire","Soigneur Légendaire","Guerrier Mage Légendaire","Paladin Nocturne","Paladin Radieux","Mage Ultraviolet Légendaire","Barde Légendaire","Stratège Légendaire","Paladin étoilé"][user.aspiration])[indx],user)
            hadChange.append(indx)

    if hadChange != []:
        saveCharFile(user=user)
        user = loadCharFile(user=user)

        tmpMsg = ""
        for cmpt in hadChange:
            tmpMsg += str(user.stuff[cmpt]) + ", "
        tmpMsg = tmpMsg[:-2]

        try:
            toUser = slash.get_user(user.owner)
            await toUser.send(embeds=interactions.Embed(title="__Problème lors de la vérification automatique de l'inventaire__", color=user.color, description="Un ou plusieurs de vos équipements n'ont pas été retrouvé. Vous avez été équipé avec les objets suivant par conséquents :\n"+tmpMsg))
            print("Noticed the stuff changes to {0}'s owner".format(user.name))
        except Exception as e:
            print("Couldn't send the notice to {0}'s owner ({1})".format(user.name,e))
    
    tablInventory = [user.weaponInventory, user.skillInventory, user.stuffInventory, user.otherInventory]
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
        user.weaponInventory, user.skillInventory, user.stuffInventory, user.otherInventory = tablInventory[0], tablInventory[1], tablInventory[2], tablInventory[3]
        babie += "\n\nCes objets vous ont été remboursés"

    if modifSkill+modifStuff > 0:
        saveCharFile(user=user)
        try:
            toUser = await slash.get_user(user.owner)
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
            toUser = await slash.get_user(user.owner)
            await toUser.send(embeds=interactions.Embed(title="__Problème lors de la vérification automatique de l'inventaire__", color=user.color, description=temp))
        except:
            pass

        print(f"Le profil de {user.name} a été mise à jour")

    userAchivments = achivementStand.getSuccess(user)
    tempMissingAchivRecompMsg = ""
    for ach in userAchivments.tablAllSuccess():
        if ach.haveSucced and ach.recompense != [None] and ach.recompense not in [["qe"], ["qh"]]:
            for rec in ach.recompense:
                if rec not in [tripleCommunCards.id, singleRareCards.id]:
                    whatty = whatIsThat(rec)
                    obj = [findWeapon(rec), findSkill(rec), findStuff(rec), None][whatty]

                    if obj != None and not(user.have(obj)):
                        if whatty == 0:
                            user.weaponInventory.append(obj)
                        elif whatty == 1:
                            user.skillInventory.append(obj)
                        elif whatty == 2:
                            user.stuffInventory.append(obj)

                        tempMissingAchivRecompMsg += "\n{0} {1} ({2})".format(obj.emoji, obj.name, ach.name)
                    saveCharFile("./userProfile/{0}.json".format(user.owner), user)

    if tempMissingAchivRecompMsg != "":
        try:
            toUser = await slash.get_user(user.owner)
            await toUser.send(embeds=interactions.Embed(title="__Problème lors de la vérification automatique de l'inventaire__", color=user.color, description="Une ou plusieurs récompenses de succès n'ont pas été trouvées dans votre inventaire et vous ont été restituée :\n"+tempMissingAchivRecompMsg))
            print("{0} n'avait pas toutes ces récompenses de succès".format(user.name))
        except:
            pass

    if user.level > MAXLEVEL:
        user = loadCharFile(user=user)
        user.level, user.exp = MAXLEVEL, 0
        user = restats(user)

        saveCharFile(user=user)

        toSend = await slash.get_user(user.owner)

        try:
            await toSend.send(embeds=interactions.Embed(title="__Problème lors de la vérification automatique de votre inventaire :__", description="Votre niveau est supérieur au niveau maximal, et à été ramené à ce dernier\nVos points bonus ont été rénitialisées\n\nPensez à faire un tour vers /prestige", color=light_blue))
        except:
            pass

    userChipInvLen = len(user.chipInventory)
    if userChipInvLen < nbAvalibleChips:
        tempChipTabl = rangeChipList[userChipInvLen:]
        for cmpt in tempChipTabl:
            user.chipInventory[cmpt] = [0,0]
        saveCharFile(user=user)

bidule = stuffDB.getShop()
if bidule != False:
    shopping = shopClass(bidule["ShopListe"])
else:
    shopping = shopClass(False)
    print("Pas de shop !")

async def restart_program(ctx=None):
    """If no teams are into a fight, restart the bot\n
    If a team fighting, wiat for them to finish then restart the bot"""

    if ctx != None:
        msg = await ctx.send(embeds=interactions.Embed(title="Redémarrage en attente...", description="Vérifications des équipes en combat..."))
    else:
        chan = slash.get_channel(912137828614426707)
        msg = await chan.send(embeds=interactions.Embed(title="Redémarrage automatique en attente...", description="Vérifications des équipes en combat..."))
    
    globalVar.changeFightEnabled(False)
    await slash.change_presence(status=Status.DND,activity=Activity(name="Attendre la fin des combats",type=ActivityType.GAME))

    globalVar.getRestartMsg(int(msg.id))
    fighting = True
    firstIt = True
    while fighting:
        fighting = False
        for team in userTeamDb.getAllTeamIds():
            if teamWinDB.isFightingBool(team[0])[0]:
                if firstIt:
                    teamTemp = userTeamDb.getTeamMember(team[0])
                    us = slash.get_user(teamTemp[0])
                    await msg.edit(embeds=interactions.Embed(title="Redémarrage en attente...", description="Un combat est encore en cours <a:loading:862459118912667678> ({0})".format(us.mention)))
                    firstIt = False
                fighting = True
                break
        if fighting:
            await asyncio.sleep(3)

    await msg.edit(embeds=interactions.Embed(title="Redémarrage en attente...", description="Redémarrage en cours..."))
    await slash.change_presence(status=Status.IDLE,activity=Activity(name="Redémarrer...",type=ActivityType.GAME))

    args = sys.argv[:]

    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]

    os.execv(sys.executable, args)

def create_backup():
    """Copy all the characters profiles files into a new directory\n
    Return a ``string`` with the path of the backup directory"""
    now = datetime.now(parisTimeZone)
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
    now = datetime.now(parisTimeZone)
    now = now.replace(tzinfo=None)
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
        chan = await slash.get_channel(912137828614426707)
        msg = await chan.send(embeds=interactions.Embed(title="Remake des emojis..."))

    await slash.change_presence(status=Status.IDLE,activity=Activity(name="Refaire les émojis...",type=ActivityType.GAME))

    async def refresh(text: str):
        await msg.edit(embeds=interactions.Embed(title="Remake des emojis...", description=text))

    await refresh("Supression des emojis...")

    iconGuildList: List[int] = [ShushyCustomIcons,LenaCustomIcons][isLenapy]

    allEmojisNum, errorCount = 0, 0
    for a in iconGuildList:
        emojiGuild = slash.get_guild(a)
        emojiList = await emojiGuild.fetch_all_custom_emojis()
        allEmojisNum += len(emojiList)

    cmpt = 0
    for a in iconGuildList:
        emojiGuild: interactions.Guild = slash.get_guild(a)
        emojiList = await emojiGuild.fetch_all_custom_emojis()
        for b in emojiList[:]:
            try:
                await b.delete()
                print("Emoji de {0} supprimé".format(b.name))
                await asyncio.sleep(0.5)
            except:
                errorCount += 1
                print("Une erreur est survenue durant la suppression de l'emoji de {0} :\n{1}".format(b.name,format_exc(1000)))
            cmpt += 1

            if cmpt//10 == 0:
                await refresh("Supression des emojis ({0} %)".format(int(cmpt/allEmojisNum*100)))

    await refresh("Suppression de la base de données...")
    try:
        customIconDB.dropCustom_iconTablDB()
    except:
        pass

    await refresh("Création des émojis...")
    allChar = os.listdir("./userProfile/")
    lenAllChar = len(allChar)
    cmpt = 0
    for num in allChar:
        try:
            user = loadCharFile("./userProfile/"+num)
            await makeCustomIcon(slash, user)
        except:
            errorCount += 1
        cmpt += 1

        if cmpt//10==0:
            await refresh("Création des émojis ({0} %)".format(int(cmpt/lenAllChar*100)))

    await refresh("Fini !\nNombre d'erreurs : {0}".format(errorCount))
    if ctx != None:
        await ctx.channel.send("Le remake des emojis est terminées !")

    ballerine = datetime.now(parisTimeZone)
    while ballerine.hour % 3 != 0:
        ballerine = ballerine + timedelta(hours=1)

    await slash.change_presence(status=Status.ONLINE,activity=Activity(name="Prochain shop à "+ballerine.strftime('%Hh'),type=ActivityType.GAME))

async def verifEmojis(ctx=None):
    if ctx != None:
        msg = await ctx.send(embeds=interactions.Embed(title="Vérification des émojis...", description="__Progression :__ 0%"))
    else:
        chan = slash.get_channel(912137828614426707)
        msg = await chan.send(embeds=interactions.Embed(title="Vérification des émojis...", description="__Progression :__ 0%"))
    remaked, lastProgress = "", 0

    await msg.edit(embeds=interactions.Embed(title="Vérification des émojis...", description="Vérification des émojis obsoletes... (0%)"))
    cmptGuild, nbCmptGuild = 0, len([ShushyCustomIcons, LenaCustomIcons][isLenapy])
    for customIconGuildId in [ShushyCustomIcons, LenaCustomIcons][isLenapy]:
        guild, successCount, errorCount = slash.get_guild(customIconGuildId), 0, 0
        customIconList = await guild.fetch_all_custom_emojis()
        for customIcon in customIconList:
            if len(customIconDB.searchCustomIcon(customIcon)) <= 0:
                try:
                    print("\"<:{0}:{1}>\" is not in the database, trying to remove it...".format(customIcon.name,customIcon.id))
                    await customIcon.delete()
                    successCount += 1
                    print("    > Success")
                except:
                    errorCount += 1
                    excStr, excStrFin = format_exc().splitlines()[-4:], ""
                    for excStrLine in excStr:
                        excStrFin += excStrLine + "\n"
                    print("    > Fail\n{0}".format(excStrFin))
        cmptGuild += 1
        await msg.edit(embeds=interactions.Embed(title="Vérification des émojis...", description="Vérification des émojis obsoletes... ({0}%)".format((cmptGuild/nbCmptGuild)*100)))
    if successCount > 0:
        remaked += "\n{0} emojis supprimés sans problèmes".format(successCount)
    if errorCount > 0:
        remaked += "\n{0} erreurs lors de la suppression d'emojis".format(errorCount)

    listAllUsersFiles = os.listdir("./userProfile/")
    lenAllUser, progress = len(listAllUsersFiles), 0
    try:
        for path in listAllUsersFiles:
            user, haveSucced = loadCharFile("./userProfile/"+path), False
            userIcon = await getUserIcon(slash, user)
            for guildId in [ShushyCustomIcons, LenaCustomIcons][isLenapy]:
                guild = slash.get_guild(guildId)
                customIconList = await guild.fetch_all_custom_emojis()
                for tmpEmoji in customIconList:
                    if int(tmpEmoji.id) == getEmojiObject(userIcon).id:
                        haveSucced = True
                        break

                if haveSucced: break

            if not(haveSucced):
                print("{0}'s emoji not found".format(user.name))
                customIconDB.removeUserIcon(user)
                await makeCustomIcon(slash, user)
                await asyncio.sleep(0.3)
                if await getUserIcon(slash, user) not in ['<:LenaWhat:760884455727955978>', '<a:lostSilver:917783593441456198>']:
                    remaked += "Emoji de {0} refait\n".format(user.name)
                else:
                    remaked += "Erreur lors du remake de l'emoji de {0}\n".format(user.name)
            progress += 1

            if progress/lenAllUser * 100 > lastProgress + 5:
                await msg.edit(embeds=interactions.Embed(title="Vérification des émojis...", description="__Progression :__ {0}%\n".format(round(progress/lenAllUser * 100, 2))+remaked))
                lastProgress = progress/lenAllUser * 100

        await msg.edit(embeds=interactions.Embed(title="Vérification des émojis", description="Terminé\n"+remaked, color=light_blue))
    except:
        await msg.edit(embeds=interactions.Embed(title="Vérification des émojis", description="__Interrompue__\n"+format_exc(), color=red))

def newChipShop():
    tick = datetime.now(parisTimeZone)
    dailyShopJson = {"dailyBooster": 0, "chipShop": [0, 0, 0], "hasBought": [[], [[], [], []],[]]}

    if tick.weekday() == 6:
        dailyShopJson["dailyBooster"] = RARITY_LEGENDARY
        dailyShopJson["chipShop"] = [chipMythic[random.randint(0,len(chipMythic)-1)].id]
        for cmpt in range(2):
            dailyShopJson["chipShop"] += [chipLegend[random.randint(0,len(chipLegend)-1)].id]
    else:
        dailyShopJson["dailyBooster"], dailyShopJson["chipShop"] = [RARITY_COMMUN, RARITY_RARE][random.randint(0,99) > 60], []
        for cmpt in range(3):
            rarityRollProba, rarityRoll, rarity = (40,50,10,0), random.randint(0,99), RARITY_LEGENDARY
            for indx, value in enumerate(rarityRollProba):
                if rarityRoll < value:
                    tablRarityList = [chipCommun,chipRare,chipLegend,chipMythic][indx]
                    dailyShopJson["chipShop"].append(tablRarityList[random.randint(0,len(tablRarityList)-1)].id)
                    break
                else:
                    rarityRoll -= value

    with open("./data/database/dailyShop.json","w") as newFile:
        try:
            json.dump({"dailyShop":dailyShopJson}, newFile)
        except Exception as e:
            newFile.close()
            print_exc()

@Task.create(OrTrigger(TimeTrigger(hour=0,utc=False),TimeTrigger(hour=3,utc=False),TimeTrigger(hour=6,utc=False),TimeTrigger(hour=9,utc=False),TimeTrigger(hour=12,utc=False),TimeTrigger(hour=15,utc=False),TimeTrigger(hour=18,utc=False),TimeTrigger(hour=21,utc=False)))
async def hourClock():
    tick, temp = datetime.now(parisTimeZone), False
    while not(temp):
        temp = await shopping.newShop()
    if allieBDay == None:
        tick = tick + timedelta(hours=3)
        await slash.change_presence(status=Status.ONLINE,activity=Activity(name="Prochain shop : "+tick.strftime('%Hh'),type=ActivityType.GAME))
    else:
        await slash.change_presence(status=Status.ONLINE,activity=Activity(name="Anniversaire de {0} !".format(allieBDay.name),type=ActivityType.GAME))

    # Skill Verif
    tick = datetime.now(parisTimeZone)
    #print("===============================\n[{0}:{1}:{2}] Starting a inventory verification...".format(tick.hour,tick.minute,tick.second))
    lenProf, cmpt, triggered = len(os.listdir("./userProfile/")), 1, {0:False,25:False,50:False,75:False}
    for filename in os.listdir("./userProfile/"):
        await inventoryVerif(slash, filename)
        cmpt += 1

        for trigerredItem, triggeredValue in triggered.items():
            if cmpt/lenProf > trigerredItem/100 and not(triggeredValue):
                triggered[trigerredItem], tick = True, datetime.now(parisTimeZone)
                #print("[{1}:{2}:{3}] {0}%...".format(trigerredItem,tick.hour,tick.minute,tick.second))
    #print("[{0}:{1}:{2}] Inventory verification done !".format(tick.hour,tick.minute,tick.second))

@Task.create(TimeTrigger(hour=4,utc=False))
async def forthHourClock():
    chan, tick = slash.get_channel(912137828614426707), datetime.now(parisTimeZone)
    if tick.day == 19:
        await chan.send(embeds=interactions.Embed(title="__Reset des records__", color=light_blue, description=aliceStatsDb.resetRecords()))
    for log in os.listdir("./data/fightLogs/"):
        try:
            os.remove("./data/fightLogs/"+log)
            print("{0} supprimé".format("./data/fightLogs/"+log))
        except:
            print("{0} n'a pas pu être supprimé".format(            "./data/fightLogs/"+log))
    await chan.send(embeds=interactions.Embed(title="__Suppression des logs__", color=light_blue, description="Les logs de combats ont été supprimés"))
    await chan.send(embeds=interactions.Embed(title="__Auto backup__", color=light_blue, description=create_backup()))
    temp = delete_old_backups()
    if temp != "":
        await chan.send(embeds=interactions.Embed(title="__Auto backup__", color=light_blue, description=temp))
    await verifEmojis()

    for userPath in os.listdir("./userProfile/"):
        user = loadCharFile('./userProfile/{0}'.format(userPath))
        aliceStatsDb.updateJetonsCount(user, max(0,9-(userShopPurcent(user)//10)))

    newChipShop()
    print("Got the restart program signal !")
    await restart_program()

@Task.create(IntervalTrigger(seconds=10))
async def twitchAlertLoop():
    backgroundTast = set()
    stremVerifTast = asyncio.create_task(verifStreamingStreamers(slash))
    backgroundTast.add(stremVerifTast)
    stremVerifTast.add_done_callback(backgroundTast.discard)

# -------------------------------------------- ON READY --------------------------------------------
@listen()
async def on_startup():
    print("\n---------\nThe bot is online ! Starting the initialisations things...\n---------\n")
    startMsg = globalVar.getRestartMsg()
    try:
        if startMsg != 0:                           # If the bot was rebooted with the admin command, change the status
            guildChan = await slash.fetch_channel('912137828614426707')
            msg = await guildChan.fetch_message(startMsg)
            await msg.edit(embeds=interactions.Embed(title="Redémarrage en cours...", description="Phase d'initalisation..."))
            globalVar.changeFightEnabled(True)
    except:
        print_exc()
        globalVar.changeFightEnabled(True)

    # Shop reload and status change

    if bidule != False:
        ballerine = datetime.now(parisTimeZone)
        while ballerine.hour % 3 != 0:
            ballerine = ballerine + timedelta(hours=1)

        if not(globalVar.fightEnabled()):
            await slash.change_presence(status=Status.DND,activitiy=Activity(name="Les combats sont désactivés",type=ActivityType.GAME))
        elif allieBDay == None:
            await slash.change_presence(status=Status.ONLINE,activity=Activity(name="Prochain shop : "+ballerine.strftime('%Hh'),type=ActivityType.GAME))
        else:
            await slash.change_presence(status=Status.ONLINE,activity=Activity(name="Anniversaire de {0} !".format(allieBDay.name),type=ActivityType.GAME))

    if isLenapy or 0:
        forthHourClock.start()
        hourClock.start()
        twitchAlertLoop.start()

    teamWinDB.resetAllFightingStatus()
    print("Downloading the emojis for the custom icons...")
    try:
        await downloadAllHeadGearPng(slash)
    except Exception as e:
        print("A error occured during the download of the head gears icons :\n{0}".format(e))
    try:
        await downloadAllWeapPng(slash)
    except Exception as e:
        print("A error occured during the download of the head gears icons :\n{0}".format(e))
    try:
        await downloadAllIconPng(slash)
    except Exception as e:
        print("A error occured during the download of the head gears icons :\n{0}".format(e))
    try:
        await downloadElementIcon(slash)
    except Exception as e:

        print("A error occured during the download of the head gears icons :\n{0}".format(e))
    print("Download done")

    print("\nSkill cost verif...")
    tempTablSkills:List[skill] = skills[:]
    tempSuc:List[achivement] = achiveTabl().tablAllSuccess()
    for achivment in tempSuc:
        if achivment.recompense != None:
            for recompense in achivment.recompense:
                skilly = findSkill(recompense)
                if skilly != None:
                    try:
                        for skilly2 in tempTablSkills:
                            if skilly2.id == skilly.id:
                                tempTablSkills.remove(skilly2)
                                break
                    except:
                        pass

    listConflictingSkills = []
    for skilly in tempTablSkills:
        if skilly.price == 0:
            listConflictingSkills.append(skilly)

    if len(listConflictingSkills) > 0:
        for skilly in listConflictingSkills:
            print("La compétence {0} coûte 0 !".format(skilly.name))


    print("Vérification des inventaires...")
    for filename in os.listdir("./userProfile/"):
        await inventoryVerif(slash, filename)
    print("> Vérification terminée")

    print("\n------- End of the initialisation -------")
    print(datetime.now(parisTimeZone).strftime('[%H:%M:%S]'))

    try:
        if startMsg != 0:
            await msg.edit(embeds=interactions.Embed(title="Redémarrage en cours...", color=light_blue, description="Le bot a bien été redémarré"))
            await msg.reply("✅ Le redémarrage du bot est terminé Léna")
            globalVar.getRestartMsg(int(0))
            print("Redémarrage terminé")
    except:
        globalVar.getRestartMsg(int(0))

    if isLenapy:
        try:
            majChan:interactions.models.discord.channel.TYPE_MESSAGEABLE_CHANNEL = slash.get_channel(1052669726674915398)
            try:
                lastMsg:List[interactions.Message] = await majChan.fetch_messages(1)
                lastMsg:interactions.Message = majChan.get_message(lastMsg[0])
                patchNoteOpened = open("./data/patch/patch.txt")
                patchVer = patchNoteOpened.readline()
                if not(patchVer in lastMsg.content):
                    await send_patchnote(majChan)
                    print("Sending patchnote {0}".format(patchVer))
            except:
                raise
        except Exception as e:
            if not "50001" in e.__str__():
                print_exc()

# ====================================================================================================
#                                               COMMANDS
# ====================================================================================================
if isLenapy:
    adminServ = [912137828614426704]
else:
    adminServ = [927195778013859902]

# -------------------------------------------- ENCYCLOPEDIA --------------------------------------------
@slash_command(name="encyclopedia", description="Vous permet de consulter l'encyclopédie", options=[
    SlashCommandOption(
        name="destination", description="Que voulez vous consulter ?", required=False, type=3,
        choices=[
            interactions.SlashCommandChoice(name="Accessoires", value="accessoires"),
            interactions.SlashCommandChoice(name="Vêtements", value="vetements"),
            interactions.SlashCommandChoice(name="Chaussures", value="chaussures"),
            interactions.SlashCommandChoice(name="Armes", value="armes"),
            interactions.SlashCommandChoice(name="Compétences", value="competences"),
            interactions.SlashCommandChoice(name="Alliés Temporaires", value='tempAlies'),
            interactions.SlashCommandChoice(name="Ennemis", value="ennemies"),
            interactions.SlashCommandChoice(name="Boss", value="boss"),
            interactions.SlashCommandChoice(name="Objets non-possédés", value="locked"),
            interactions.SlashCommandChoice(name="Succès", value="achivements")
        ]
    )
])

async def comEncyclopedia(ctx: SlashContext, destination = None):
    if not(await botChannelVerif(slash, ctx)):
        await ctx.send("Je ne suis pas autorisée à donner suite aux commandes dans ce salon",ephemeral=True)

    await ctx.defer()

    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".json"
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
toTestTemp, toTestChangeDict = None, None

# normal fight
baseFight = SlashCommand(name="fight",description="Permet de lancer un combat",auto_defer=AutoDefer(enabled=True,time_until_defer=0))
baseOcto = SlashCommand(name="octogone",description="Permet de lancer un combat contre un autre joueur",auto_defer=AutoDefer(enabled=True,time_until_defer=0.5))

addNotif, removeNotif = Button(style=ButtonStyle.GRAY,label="Me notifier à la fin du combat",emoji=getEmojiObject('🔔'),custom_id="notif"), Button(style=ButtonStyle.GRAY,label="Supprimer la notification",emoji=getEmojiObject('🔕'),custom_id="notif")

@baseFight.subcommand(sub_cmd_name="normal",sub_cmd_description="Permet de lancer un combat normal",options=[SlashCommandOption(name="notify",type=OptionType.BOOLEAN,description="Vous notifie à la fin du combat",required=False)])
async def normal(ctx:SlashContext, notify=False):
    msg, fightResult = None, None
    if not(await botChannelVerif(slash, ctx)):
        return 0
    if not(globalVar.fightEnabled()):
        await ctx.send(embeds=interactions.Embed(title="__Combats désactivés__", description="Les combats sont actuellement désactivés pour cause de bug ou de déploiment imminant d'une mise à jour\nVeuillez vous référer au status du bot pour savoir si les combats sont désactivés ou non"),ephemeral=True)
        return 0

    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".json"
    try: user = loadCharFile(pathUserProfile)
    except:
        try: await ctx.send("Vous n'avez pas commencé l'aventure")
        except: await ctx.channel.send("Vous n'avez pas commencé l'aventure")
        return 0

    ballerine, temp = 0, 0
    if user.team == 0: user = newTeam(user)

    ballerine = user.team
    timing, fightDate, today = teamWinDB.getFightCooldown(ballerine), teamWinDB.getFightCooldown(ballerine, returnDate=True), datetime.now(parisTimeZone)
    initTiming = timing

    if timing > 0:
        if timing > 60*60:
            ts = teamWinDB.getFightCooldown(ballerine,timestamp=True)
            try:
                msg = await ctx.send(embeds=errorEmbed("Cooldown", "Votre équipe ne pourra faire de combats normaux que {0}".format(ts)),ephemeral=True)
            except:
                msg = await ctx.channel.send(embeds=errorEmbed("Cooldown", "Votre équipe ne pourra faire de combats normaux que {0}".format(ts)))
                await asyncio.sleep(3)
                await msg.delete()
            return 0
        elif ballerine not in allreadyinWait:
            allreadyinWait.append(ballerine)
            ts = teamWinDB.getFightCooldown(ballerine,timestamp=True)

            def notifyCheck(interact):
                interact = interact.ctx
                return interact.author_id == ctx.author_id

            while 1:
                notifButton = [ActionRow([addNotif, removeNotif][notify])]
                if timing > 0:
                    try:
                        if msg == None:
                            try: msg = await ctx.send(embeds=await getRandomStatsEmbed(slash, [user], text="Votre combat a été mis en liste d'attente ({0})".format(ts)), components=notifButton)
                            except: msg = await ctx.channel.send(embeds=await getRandomStatsEmbed(slash, [user], text="Votre combat a été mis en liste d'attente ({0})".format(ts)), components=notifButton)
                        else: await msg.edit(embeds=await getRandomStatsEmbed(slash, [user], text="Votre combat a été mis en liste d'attente ({0})".format(ts)), components=notifButton)
                    except: pass

                    timeout = max(10,min(initTiming//10,timing))
                    try:
                        react = await slash.wait_for_component(messages=msg,components=notifButton[0].components,timeout=timeout,check=notifyCheck)
                        react: ComponentContext = react.ctx

                        notify = not(notify)
                        notifButton = [ActionRow([addNotif, removeNotif][notify])]
                        await react.send(content=["🔔 Vous serez notifié à la fin du combat","🔕 La notification a été annulée"][not(notify)], ephemeral=True)
                        timing = teamWinDB.getFightCooldown(ballerine)
                    except asyncio.TimeoutError: timing -= timeout
                else:
                    try:
                        if msg == None: msg = await ctx.send(embeds=await getRandomStatsEmbed(slash, [user], text="Combat en cour de génération..."))
                        else: await msg.edit(embeds=await getRandomStatsEmbed(slash, [user], text="Combat en cour de génération..."),components=[])
                    except: pass
                    break
        else:
            try:
                msg = await ctx.send(embeds=errorEmbed("Cooldown", "Votre équipe est déjà en file d'attente"),ephemeral=True)
            except:
                msg = await ctx.channel.send(embeds=errorEmbed("Cooldown", "Votre équipe est déjà en file d'attente"),ephemeral=True)
                await asyncio.sleep(3)
                await msg.delete()
            return 0

    if (fightDate.year,fightDate.month,fightDate.day) != (today.year,today.month,today.day) and isLenapy and (fightDate.year,fightDate.month,fightDate.day) != (2001,1,19):
        try:
            await ctx.defer()
        except:
            pass
        user = loadCharFile(int(ctx.member.id))
        nbBooster = 1 + int(user.have(dailyCardBooster1)) + int(user.have(dailyCardBooster2))
        user, fieldValue = openBooster(user=user, boosters=[RARITY_COMMUN]*nbBooster, infield=False)
        saveCharFile(user=user)

        await ctx.respond(embeds=Embed(title="__Premier combat du jour !__",description="Vous avez obtenus {1} {0} Booster{2} de Puces Commun !".format(rarityEmojis[RARITY_COMMUN],["zéro ?","un","deux","trois"][nbBooster],["","s"][nbBooster>1])+"\n\n"+fieldValue,color=user.color))

    try: allreadyinWait.remove(ballerine)
    except: pass

    fightingStatus = teamWinDB.isFightingBool(ballerine)
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

        if msg == None:
            await ctx.send(embeds=interactions.Embed(title="__/fight__", color=user.color, description=fightingRespond),ephemeral=True)
        else:
            await msg.edit(embeds=interactions.Embed(title="__/fight__", color=user.color, description=fightingRespond))
        return 0

    team1 = []
    if user.team != 0: 
        for a in userTeamDb.getTeamMember(user.team): team1 += [loadCharFile("./userProfile/{0}.json".format(a))]
    else: team1 = [user]

    teamSettings = aliceStatsDb.getTeamSettings(team1[0])
    procurFight = []

    if not(isLenapy) and toTestTemp != None:
        ent = findAllie(toTestTemp)
        global toTestChangeDict
        if toTestChangeDict == -1: toTestChangeDict = False
        elif type(toTestChangeDict) == int: ent = getAllieFromBuild(ent,ent.changeDict[toTestChangeDict]); toTestChangeDict = False
        ent.changeLevel(MAXLEVEL,stars=5,changeDict=toTestChangeDict,changeStuff=toTestChangeDict)
        ent.owner, ent.team = user.owner, user.team
        team1 = [ent]

    # Random event
    if msg == None:
        try: msg = await ctx.send(embeds=await getRandomStatsEmbed(slash,team1,text="__Combat en cours de génération...__"))
        except: msg = await ctx.channel.send(embeds=await getRandomStatsEmbed(slash,team1,text="__Combat en cours de génération...__"))
    fun, teamLvl, starLvl = random.randint(0, 99), 0, 0
    for ent in team1: teamLvl = max(ent.level,teamLvl); starLvl = max(ent.stars,starLvl)

    userTeamDb.updateTeamMinLvl(team1)
    spFightPrc, raidFightPrc = [(SPSPECIALFIGHTPURCENT, SPRAIDPURCENT),(SPECIALFIGHTPURCENT, RAIDPURCENT)][isLenapy]
    fightCtx = fightContext()

    if fun < spFightPrc:              # Specials fights
        team2, initTeam, procurFight = [], team1, []
        team1 = []

        tablPreDefTeam = ["All One Ennemis","Kitsunes","Helping Kitsune","academicTeam","ClemClem","Luna","Iliana","Lia","Lena","Nacialisla","Lohica Pirate fight","full bandito"]
        rdmRoll = random.randint(0,len(tablPreDefTeam))
        print("Special Fight : {}".format(tablPreDefTeam[rdmRoll]))

        match rdmRoll:
            case 0: # One for all
                team1, cmpt = initTeam, 0
                tablAllvOne = [["Octo Soigneur","Octo Soigneur Vétéran"][teamLvl>=35],"Temmie","OctoBOUM","Aéro-benne"]
                alea = copy.deepcopy(findEnnemi(randRep(tablAllvOne)))
                alea.changeLevel(teamLvl)
                while cmpt < 8: team2.append(alea); cmpt += 1
            case 1: # Kitsu
                team1 = initTeam
                team1, team2 = initTeam [copy.deepcopy(findEnnemi("Lia")),copy.deepcopy(findEnnemi("Liu")),copy.deepcopy(findEnnemi("Liz")),copy.deepcopy(findEnnemi("Lio"))]
                team2[0].agility, team2[1].endurance, team2[2].magie, team2[3].charisma = int(team2[0].agility * 1), int(team2[1].endurance * 1), int(team2[2].magie * 1.35), int(team2[3].charisma * 1)
                team2[0].exp = team2[1].exp = team2[2].exp = team2[3].exp = 20
                kitsuneAbs = copy.deepcopy(constEff)
                kitsuneAbs.power, kitsuneAbs.turnInit, kitsuneAbs.unclearable, kitsuneAbs.stat = 50, -1, True, PURCENTAGE
                fightCtx.giveEffToTeam2 = [kitsuneAbs]
                for cmpt in range(len(team2)): team2[cmpt].changeLevel(teamLvl)
            case 2: # Allied Kitsu
                team1 = initTeam
                kitsuneTabl = [findEnnemi("Lia"),findEnnemi("Liu"),findEnnemi("Liz"),findEnnemi("Lio")]
                kitsuneStuffIcon = [
                    [rubButGreen.emoji,greenChemVeste.emoji,greenbutterflysandals.emoji],
                    [BatEarRingsorange.emoji,orangeBatshirt.emoji,orangeBatBoots.emoji],
                    [foulard.emoji,chemAndJupeRed.emoji,redHeels.emoji],
                    [butterflyPendantDarkBlue.emoji,chemRubButDBlue.emoji,balRubButDBlue.emoji]
                ]
                randomNumber = random.randint(0,len(kitsuneTabl))
                for randomNumber in range(len(kitsuneTabl)):
                    toAdd = getAllieFromEnemy(kitsuneTabl[randomNumber],teamLvl,kitsuneStuffIcon,color=[green,orange,red,blue][randomNumber])
                    toAdd.changeLevel(level=teamLvl,stars=user.stars)
                    team1.append(toAdd)
                fightCtx.removeEnemy, fightCtx.nbAllies, fightCtx.procur = ["Lia","Liu","Liz","Lio"], 12
                del kitsuneTabl, kitsuneStuffIcon
            case 3: # Academic Team
                team1 = []
                templist = ["Zénéca","Victoire","Alexandre","Jade"]
                for tempName in templist:
                    ent = findAllie(tempName)
                    ent.changeLevel(random.randint(0,8)+80,stars=5)
                    team1.append(ent)
                    procurFight.append(ent)
                ratio1 = 8/len(team1)
                for ent in team1:
                    for cmpt in range(len(ent.stuff)):
                        stuffy = copy.deepcopy(ent.stuff[cmpt])
                        stuffy.strength = int(stuffy.strength * ratio1)
                        stuffy.endurance = int(stuffy.endurance * max(1,ratio1/3))
                        stuffy.charisma = int(stuffy.charisma * max(1,ratio1/2))
                        stuffy.agility = int(stuffy.agility * max(1,ratio1/3))
                        stuffy.precision = int(stuffy.precision * max(1,ratio1/3))
                        stuffy.intelligence = int(stuffy.intelligence * max(1,ratio1/2))
                        stuffy.magie = int(stuffy.magie * ratio1)

                        ent.stuff[cmpt] = stuffy

                    for indx, tmpSkill in enumerate(ent.skills):
                        if tmpSkill.__class__ == classes.skill:
                            tmpSkill = copy.deepcopy(tmpSkill)
                            tmpSkill.use = HARMONIE
                            for indx2, tmpEff in enumerate(tmpSkill.effects):
                                tmpEff = findEffect(tmpEff)
                                if tmpEff != None and tmpEff.stat in range(MAGIE+1):
                                    tmpEff = copy.deepcopy(tmpEff)
                                    tmpEff.stat = HARMONIE
                                tmpSkill.effects[indx2] = tmpEff

                            if tmpSkill.effectAroundCaster not in [None,[]] and type(tmpSkill.effectAroundCaster[2]) == classes.effect and tmpSkill.effectAroundCaster[2].stat in range(MAGIE+1):
                                tmpEff = copy.deepcopy(tmpSkill.effectAroundCaster[2])
                                tmpEff.stat = HARMONIE
                                tmpSkill.effectAroundCaster[2] = tmpEff
                            
                            if tmpSkill.effectOnSelf not in [None] and type(tmpSkill.effectOnSelf) == classes.effect and tmpSkill.effectOnSelf.stat in range(MAGIE+1):
                                tmpEff = copy.deepcopy(tmpSkill.effectOnSelf)
                                tmpEff.stat = HARMONIE
                                tmpSkill.effectOnSelf = tmpEff

                            ent.skills[indx] = tmpSkill

                procurFight = team1

                if random.randint(0,99) > 20:
                    tempTeamEff, tempTeamEff2, tempTeamEff3, tempTeamEff4 = copy.deepcopy(constEff), copy.deepcopy(dmgUp), copy.deepcopy(defenseUp), copy.deepcopy(healDoneBonus)
                    tempTeamEff.stat = PURCENTAGE
                    tempTeamEff.turnInit = tempTeamEff2.turnInit = tempTeamEff3.turnInit = tempTeamEff4.turnInit = -1
                    tempTeamEff.unclearable = tempTeamEff2.unclearable = tempTeamEff3.unclearable = tempTeamEff4.unclearable = tempTeamEff.silent = tempTeamEff2.silent = tempTeamEff3.silent = tempTeamEff4.silent = True
                    tempTeamEff.power = tempTeamEff2.power = tempTeamEff3.power = 50
                    tempTeamEff4.power = 35

                    fightCtx.allowTemp, fightCtx.nbAllies, fightCtx.giveEffToTeam1, fightCtx.nbEnnemis, fightCtx.allowBoss = False, len(team1), [tempTeamEff, tempTeamEff2, tempTeamEff3, tempTeamEff4], 8, False
                else:
                    ent = findEnnemi("Phy")
                    ent.changeLevel(random.randint(0,8)+80)
                    team2 = [ent]
                    tempTeamEff = copy.deepcopy(constEff)
                    tempTeamEff.power, tempTeamEff.stat, tempTeamEff.turnInit, tempTeamEff.unclearable = 500, PURCENTAGE, -1, True
                    tempTeamEff2 = effect("Bonus de magie","magicBoost",PURCENTAGE,turnInit=-1,silent=True,unclearable=True,magie=300,emoji=statsEmojis[MAGIE])

                    tempUndyingEff = effect("Recall","recall",turnInit=-1,silent=True,unclearable=True,emoji="")
                    fightCtx.allowTemp, fightCtx.nbAllies, fightCtx.nbEnnemis, fightCtx.allowBoss, fightCtx.giveEffToTeam2, fightCtx.giveEffToTeam1 = False, len(team1), 1, False, [tempTeamEff,tempTeamEff2], [tempUndyingEff]
            case 4: # Clemence Ex
                ent = copy.deepcopy(findAllie("Clémence Exaltée"))
                ent.changeLevel(teamLvl+500+random.randint(0, 100),stars=starLvl,changeStuff=False)
                stuffRatio = (ent.level-200)*12/(ent.stuff[0].minLvl*3)

                for cmpt, tmpStuff in enumerate(ent.stuff): ent.stuff[cmpt].strength = int(tmpStuff.strength*stuffRatio); ent.stuff[cmpt].endurance = int(tmpStuff.endurance*(stuffRatio/2)); ent.stuff[cmpt].magie = int(tmpStuff.magie*stuffRatio)

                ent.chipInventory[getChip("Sur-Vie").id].power, ent.chipInventory[getChip("Démolition").id].power, ent.chipInventory[getChip("Dégâts reçus réduits").id].power = 50, 100, 65
            
                team1.append(ent)
                procurFight.append(ent)
                fightCtx.reduceEnemyLevel, fightCtx.allowTemp, fightCtx.nbEnnemis = 200, False, 12
                procurFight = team1
            case 5: # Luna
                ent, procurData = copy.deepcopy(findAllie("Luna prê.")), procurTempStuff["Luna prê."]
                ent.changeLevel(teamLvl+random.randint(0, 50),stars=starLvl)

                ent.stuff = [stuff(procurData[1][0],procurData[1][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[1][2]),stuff(procurData[2][0],procurData[2][1],1,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[2][2]),stuff(procurData[3][0],procurData[3][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[3][2])]

                team1.append(ent)
                procurFight.append(ent)
                fightCtx.reduceEnemyLevel, fightCtx.allowTemp = 150, False

                if random.randint(0, 99) < 50:               # Eclipse Eternelle
                    ent2, procurData = copy.deepcopy(findAllie('Iliana prê.')), procurTempStuff["Iliana prê."]
                    ent2.skills[0] = ent2.skills[0].become[0]
                    ent2.changeLevel(team1[0].level,stars=starLvl)

                    ent2.stuff = [stuff(procurData[1][0],procurData[1][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent2.level),int(procurData[4][1][0]*procurData[4][1][1]*ent2.level),int(procurData[4][2][0]*procurData[4][2][1]*ent2.level),int(procurData[4][3][0]*procurData[4][3][1]*ent2.level),int(procurData[4][4][0]*procurData[4][4][1]*ent2.level),int(procurData[4][5][0]*procurData[4][5][1]*ent2.level),int(procurData[4][6][0]*procurData[4][6][1]*ent2.level),int(procurData[4][7][0]*procurData[4][7][1]*ent2.level),int(procurData[4][8][0]*procurData[4][8][1]*ent2.level),int(procurData[4][9][0]*procurData[4][9][1]*ent2.level),emoji=procurData[1][2]),stuff(procurData[2][0],procurData[2][1],1,0,int(procurData[4][0][0]*procurData[4][0][1]*ent2.level),int(procurData[4][1][0]*procurData[4][1][1]*ent2.level),int(procurData[4][2][0]*procurData[4][2][1]*ent2.level),int(procurData[4][3][0]*procurData[4][3][1]*ent2.level),int(procurData[4][4][0]*procurData[4][4][1]*ent2.level),int(procurData[4][5][0]*procurData[4][5][1]*ent2.level),int(procurData[4][6][0]*procurData[4][6][1]*ent2.level),int(procurData[4][7][0]*procurData[4][7][1]*ent2.level),int(procurData[4][8][0]*procurData[4][8][1]*ent2.level),int(procurData[4][9][0]*procurData[4][9][1]*ent2.level),emoji=procurData[2][2]),stuff(procurData[3][0],procurData[3][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent2.level),int(procurData[4][1][0]*procurData[4][1][1]*ent2.level),int(procurData[4][2][0]*procurData[4][2][1]*ent2.level),int(procurData[4][3][0]*procurData[4][3][1]*ent2.level),int(procurData[4][4][0]*procurData[4][4][1]*ent2.level),int(procurData[4][5][0]*procurData[4][5][1]*ent2.level),int(procurData[4][6][0]*procurData[4][6][1]*ent2.level),int(procurData[4][7][0]*procurData[4][7][1]*ent2.level),int(procurData[4][8][0]*procurData[4][8][1]*ent2.level),int(procurData[4][9][0]*procurData[4][9][1]*ent2.level),emoji=procurData[3][2])]
                    
                    team1.append(ent2)
                    procurFight.append(ent2)

                    boss = copy.deepcopy(unformBoss)
                    boss.changeLevel(team1[0].level + random.randint(300, 350))
                    team2, listDangerous, cmpt = [boss], [findEnnemi('Lueur Aforme'), findEnnemi('Lueur Aforme'), findEnnemi('Espace Aforme'), findEnnemi('Temporalité Aforme')], 1
                    while cmpt < 8: temp = copy.deepcopy(listDangerous[random.randint(0, len(listDangerous)-1)]); temp.changeLevel(level + random.randint(200, 300)); team2.append(temp); cmpt += 1
                else:
                    lunaDmgRes = copy.deepcopy(defenseUp)
                    lunaDmgRes.power, lunaDmgRes.turnInit, lunaDmgRes.unclearable = 50, -1, True
                    lunaLifeSteal = copy.deepcopy(vampirismeEff)
                    lunaLifeSteal.power, lunaLifeSteal.turnInit, lunaLifeSteal.unclearable = 30, -1, True
                    fightCtx.giveEffToTeam1=[lunaDmgRes,lunaLifeSteal]
                procurFight = team1
            case 6: # Ilianya
                ent, procurData = copy.deepcopy(findAllie("Iliana prê.")), procurTempStuff["Iliana prê."]
                ent.skills[0] = ent.skills[0].become[1]
                ent.changeLevel(teamLvl+random.randint(0, 50),stars=starLvl)

                ent.says = says(start="Désolée pour vous, mais j'ai grand besoin de taper sur quelque chose.",blueWinAlive="`Soupire` Bon Iliana calme toi, tu as suffisament tapé de trucs comme ça. Tout va- Oh ils sont tous aux portes de la mort")
                ent.stuff = [stuff(procurData[1][0],procurData[1][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[1][2]),stuff(procurData[2][0],procurData[2][1],1,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[2][2]),stuff(procurData[3][0],procurData[3][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[3][2])]

                team1.append(ent)
                procurFight.append(ent)
                fightCtx.reduceEnemyLevel, fightCtx.allowTemp, fightCtx.nbEnnemis = 100, False, 12

                if random.randint(0,100)<35:
                    team1[0].says=says(start="Encore et toujours...",ultimate="Voilà pour vous, de quoi bien vous exprimer ma façon de penser.",blueWinAlive="Pourquoi Luna a dit qu'elle ne ferait que me gêner c'était simple pourtant...",onKill='Retourne donc d\'où tu viens.')

                    team1[0].skills[0].effects[0].power = team1[0].skills[0].effects[0].power * 2
                    team2, listDangerous, cmpt = [], [findEnnemi('Lueur Aforme'), findEnnemi('Lueur Aforme'), findEnnemi('Espace Aforme'), findEnnemi('Temporalité Aforme')], 0
                    while cmpt < 12: temp = copy.deepcopy(listDangerous[random.randint(0, len(listDangerous)-1)]); temp.changeLevel(team1[0].level); team2.append(temp); cmpt += 1

                    tempEff = copy.deepcopy(dmgUp)
                    tempEff.power, tempEff.turnInit, tempEff.unclearable = 50, -1, True
                    fightCtx.giveEffToTeam2 = [tempEff]
                procurFight = team1
            case 7: # Lia Ex
                ent,procurData = copy.deepcopy(findAllie("Lia Ex")), procurTempStuff["Lia Ex"]
                ent.changeLevel(teamLvl+random.randint(0, 50),stars=starLvl)
                ent.stuff, ent.charSettings = [stuff(procurData[1][0],procurData[1][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[1][2]),stuff(procurData[2][0],procurData[2][1],1,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[2][2]),stuff(procurData[3][0],procurData[3][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[3][2])], createCharSettingsDict(dmgSkillUse=CHARSET_DMGSKILL_HIGH,healSkillUse=CHARSET_HEALSKILL_LOW,armorSkillUse=CHARSET_ARMORSKILL_LOW)

                team1.append(ent)
                procurFight.append(ent)

                tmpEff = copy.deepcopy(dmgUp)
                tmpEff.power, tmpEff.turnInit = 35, -1
                fightCtx.reduceEnemyLevel, fightCtx.removeEnemy, fightCtx.allowTemp, fightCtx.nbEnnemis, fightCtx.giveEffToTeam1 = 50, ["Lia","Liz","Lio","Liu"], False, 8, [tmpEff]
                procurFight = team1
            case 8: # Main Cast Team
                templist = ["Lena","Shushi","Sixtine","Gwendoline"]
                for tempName in templist: ally = findAllie(tempName); ent = getAllieFromBuild(ally,ally.changeDict[-1]); ent.changeLevel(teamLvl,stars=5,changeDict=False,changeStuff=False); team1.append(ent); procurFight.append(ent)

                ratio1, ratio2 = round(6/len(team1),2), round(teamLvl/65,2)
                for ent in team1: 
                    for cmpt in range(len(ent.stuff)): stuffy = copy.deepcopy(ent.stuff[cmpt]); stuffy.strength = int(stuffy.strength * ratio1 * ratio2); stuffy.endurance = int(stuffy.endurance * max(1,ratio1/4) * ratio2); stuffy.charisma = int(stuffy.charisma * max(1,ratio1/3) * ratio2); stuffy.agility = int(stuffy.agility * max(1,ratio1/4) * ratio2); stuffy.precision = int(stuffy.precision * max(1,ratio1/4) * ratio2); stuffy.intelligence = int(stuffy.intelligence * max(1,ratio1/3) * ratio2); stuffy.magie = int(stuffy.magie * ratio1 * ratio2); ent.stuff[cmpt] = stuffy

                tempTeamEff = copy.deepcopy(constEff)
                tempTeamEff.stat, tempTeamEff.turnInit, tempTeamEff.unclearable, tempTeamEff.power = PURCENTAGE, -1, True, (ratio1-1)*100

                fightCtx.allowTemp, fightCtx.nbEnnemis, fightCtx.nbAllies, fightCtx.giveEffToTeam1, fightCtx.allowBoss = False, 8, len(team1), [tempTeamEff], False
                procurFight = team1
            case 9: # Nacialisla
                toAdd = getAllieFromEnemy(findEnnemi("Nacialisla"),teamLvl,[roseGreen.emoji[0][0],tshirtNoue.emoji,mageShoe.emoji],0x422d0e)

                toAdd.stuff[0].strength = toAdd.stuff[1].strength = toAdd.stuff[2].strength = toAdd.stuff[0].strength*1.5
                toAdd.stuff[0].endurance = toAdd.stuff[1].endurance = toAdd.stuff[2].endurance = toAdd.stuff[0].endurance*2
                toAdd.stuff[0].magie = toAdd.stuff[1].magie = toAdd.stuff[2].magie = toAdd.stuff[0].magie*1.5
                toAdd.weapon = copy.deepcopy(toAdd.weapon)
                toAdd.weapon.range = RANGE_MELEE

                naciaStuffEff1, naciaStuffEff2 = copy.deepcopy(constEff), copy.deepcopy(dmgUp)
                naciaStuffEff1.power, naciaStuffEff1.stat, naciaStuffEff1.turnInit, naciaStuffEff1.unclearable, naciaStuffEff2.power, naciaStuffEff2.turnInit, naciaStuffEff2.unclearable = round((BASEHP_BOSS+(HPPERLVL_BOSS*teamLvl/2))/(BASEHP_PLAYER+(HPPERLVL_PLAYER*teamLvl))*100), PURCENTAGE, -1, True, 15, -1, True
                toAdd.stuff[0].effects, toAdd.stuff[1].effects = naciaStuffEff1, naciaStuffEff2

                team1.append(toAdd)
                procurFight.append(toAdd)
                fightCtx.nbEnnemis, fightCtx.allowBoss, fightCtx.allowTemp, fightCtx.removeEnemy = 16, False, False, ["Golem des Roches","Golem des Vents","Golem des Flots","Golem des Flammes"]
                procurFight = team1
            case 10: # Lohica Pirate Fight
                team1 = [copy.deepcopy(findAllie("Lohica")),copy.deepcopy(findAllie("Amary"))]
                fightCtx.setDanger = True
                procurFight = team1
                if random.randint(0,99) < 35: team1 = team1 + [copy.deepcopy(findAllie("Hélène")),copy.deepcopy(findAllie("Shehisa")),copy.deepcopy(findAllie("Astra")),getAllieFromBuild(findAllie("Icealia"),findAllie("Icealia").changeDict[1])]

                for cmpt in range(len(team1)): team1[cmpt].changeLevel(45+random.randint(0,10),False,starLvl,False); procurFight.append(team1[cmpt])

                sabr, pist = getAllieFromEnemy(findEnnemi("Marinier Sabreur"),35,color=0xE572FE), getAllieFromEnemy(findEnnemi("Marinier Tireur"),35,color=0xE572FE)
                while len(team1) < 8:team1.append([sabr,pist][random.randint(0,1)])

                if random.randint(0,99) < 20: ent = findEnnemi("Séréna"); ent.changeLevel(50); team2.append(ent)

                while len(team2) < 10: ent = copy.deepcopy(findEnnemi(["Marinier Sabreur","Marinier Tireur"][random.randint(0,1)])); ent.changeLevel(35); team2.append(ent)
            case 11: # Shehisa Icealia
                team1 = [getAllieFromBuild(findAllie("Icealia"),findAllie("Icealia").changeDict[1]),getAllieFromBuild(findAllie("Shehisa"),findAllie("Shehisa").changeDict[1]),getAllieFromEnemy("Imea",50,color=light_blue)]
                procurFight = team1
                for cmpt in range(len(team1)): team1[cmpt].changeLevel(45+random.randint(0,10),False,starLvl,False); procurFight.append(team1[cmpt])

                icealiaLifeBoost, icealiaDmgBoost = copy.deepcopy(constEff), copy.deepcopy(dmgUp)
                icealiaLifeBoost.turnInit, icealiaLifeBoost.stat, icealiaLifeBoost.power, icealiaLifeBoost.unclearable, icealiaLifeBoost.aggro = -1, PURCENTAGE, 50, True, 100
                icealiaDmgBoost.turnInit, icealiaDmgBoost.unclearable, icealiaDmgBoost.power = -1, True, 100
                team1[0].stuff[0].effects, team1[0].stuff[1].effects = icealiaLifeBoost, icealiaDmgBoost

                shehisaDmgBoost = copy.deepcopy(dmgUp)
                shehisaDmgBoost.unclearable, shehisaDmgBoost.turnInit, shehisaDmgBoost.power = True, -1, 35
                shehisaHealBuff = effect("Précautions","shehisaHealBuff",PURCENTAGE,power=10,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji=gpotion.emoji,turnInit=-1)
                team1[1].stuff[0], team1[1].stuff[1] = copy.deepcopy(team1[1].stuff[0]), copy.deepcopy(team1[1].stuff[1])
                team1[1].stuff[0].effects, team1[1].stuff[1].effects = shehisaDmgBoost, shehisaHealBuff

                while len(team2) < 8:ent = copy.deepcopy(findEnnemi(["Bandit Surrineur","Bandit Archer"][random.randint(0,1)])); ent.changeLevel(30); team2.append(ent)

        await fight(slash, team1, team2, ctx, False, contexte=fightCtx, msg=msg, teamSettings=teamSettings, notify=notify, procurFight=set(procurFight))
    elif fun < spFightPrc+raidFightPrc and teamLvl >= 10:             # Raid
        try:
            tablAllTeams, allReadySeen = userTeamDb.getAllTeamIds(True), []
            random.shuffle(tablAllTeams)

            moyTeam = 0
            for a in team1: moyTeam += a.level; allReadySeen.append(a.owner)
            moyTeam = moyTeam/len(team1)
            for tempTeamId in tablAllTeams:
                try:
                    tempTeam, moyTempTeam = [], tempTeamId[1]
                    if moyTeam <= moyTempTeam+10 and moyTeam >= moyTempTeam-10 and tempTeamId[0] != user.team:
                        for a in userTeamDb.getTeamMember(tempTeamId[0]):
                            if a not in allReadySeen: tempUser = loadCharFile("./userProfile/{0}.json".format(a)); tempTeam += [tempUser]
                        team1 += tempTeam
                        break
                except Exception as e: print(e)

            del tablAllTeams, allReadySeen
            team1.sort(key=lambda overheal: overheal.level, reverse=True)
            maxLvl, team2 = team1[0].level, []
            
            if teamLvl >= findEnnemi(RAIDHIGHLIGHT).baseLvl and random.randint(0,99) <= RAIDHIGHLIGHTPURCENT: alea = copy.deepcopy(findEnnemi(RAIDHIGHLIGHT))
            else:
                tablBoss = []
                for boss in range(len(tablRaidBoss)):
                    if tablRaidBoss[boss].baseLvl <= teamLvl: tablBoss.append(tablRaidBoss[boss])
                alea = copy.deepcopy(tablBoss[random.randint(0, len(tablBoss)-1)])

            alea.changeLevel(maxLvl)
            team2.append(alea)

            fightCtx.nbAllies=16
            fightResult: Message =  await fight(slash, team1, team2, ctx, False, bigMap=True, msg=msg, teamSettings=teamSettings, contexte=fightCtx, notify=notify)
        except: await msg.edit(embeds=interactions.Embed(title="__Unknow error during fight__", description=format_exc())); teamWinDB.changeFighting(team1[0].team, value=False, channel=0)
    else: await fight(slash, team1, [], ctx, False, msg=msg, teamSettings=teamSettings, notify=notify)

# quick fight
@baseFight.subcommand(sub_cmd_name="quick", sub_cmd_description="Vous permet de faire un combat en sautant directement à la fin")
async def comQuickFight(ctx,notify=False):
    msg, fightResult = None, None
    if not(await botChannelVerif(slash, ctx)):
        return 0
    if not(globalVar.fightEnabled()) and int(ctx.author.id) != 213027252953284609:
        await ctx.send(embeds=interactions.Embed(title="__Combats désactivés__", description="Les combats sont actuellement désactivés pour cause de bug ou de déploiment imminant d'une mise à jour\nVeuillez vous référer au status du bot pour savoir si les combats sont désactivés ou non"),ephemeral=True)
        return 0

    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".json"
    try: user = loadCharFile(pathUserProfile)
    except:
        try: msg = await ctx.send("Vous n'avez pas commencé l'aventure",ephemeral=True)
        except: msg = await ctx.channel.send("Vous n'avez pas commencé l'aventure"); await asyncio.sleep(3); await msg.delete(); return 0

    if user.team == 0: user = newTeam(user)
    ballerine = user.team

    timing = teamWinDB.getFightCooldown(ballerine, True)
    initTiming = copy.deepcopy(timing)
    if timing > 0:
        ts = teamWinDB.getFightCooldown(ballerine, True,timestamp=True)
        if timing > 60*180:
            try:
                msg = await ctx.send(embeds=errorEmbed("Cooldown", "Votre équipe ne pourra faire de combats rapides que {0}".format(ts)),ephemeral=True)
            except:
                msg = await ctx.channel.send(embeds=errorEmbed("Cooldown", "Votre équipe ne pourra faire de combats rapides que {0}".format(ts)))
                await asyncio.sleep(3)
                await msg.delete()
            return 0
        elif ballerine not in allreadyinWaitQuick:
            allreadyinWaitQuick.append(ballerine)
            def notifyCheck(interact):
                interact = interact.ctx
                return interact.author_id == ctx.author_id

            while 1:
                notifButton = [ActionRow([addNotif, removeNotif][notify])]
                if timing > 0:
                    try:
                        if msg == None:
                            try: msg = await ctx.send(embeds=await getRandomStatsEmbed(slash, [user], text="Votre combat a été mis en liste d'attente ({0})".format(ts)), components=notifButton)
                            except: msg = await ctx.channel.send(embeds=await getRandomStatsEmbed(slash, [user], text="Votre combat a été mis en liste d'attente ({0})".format(ts)), components=notifButton)
                        else: await msg.edit(embeds=await getRandomStatsEmbed(slash, [user], text="Votre combat a été mis en liste d'attente ({0})".format(ts)), components=notifButton)
                    except: pass

                    timeout = max(10,min(initTiming//10,timing))
                    try:
                        react = await slash.wait_for_component(messages=msg,components=notifButton[0].components,timeout=timeout,check=notifyCheck)
                        react: ComponentContext = react.ctx

                        notify = not(notify)
                        notifButton = [ActionRow([addNotif, removeNotif][notify])]
                        await react.send(content=["🔔 Vous serez notifié à la fin du combat","🔕 La notification a été annulée"][not(notify)],ephemeral=True)
                        timing = teamWinDB.getFightCooldown(ballerine, True)
                    except asyncio.TimeoutError: timing -= timeout
                else: break
        else:
            try: msg = await ctx.send(embeds=errorEmbed("Cooldown", "Votre équipe est déjà en file d'attente"),ephemeral=True)
            except:
                msg = await ctx.channel.send(embeds=errorEmbed("Cooldown", "Votre équipe est déjà en file d'attente"))
                await asyncio.sleep(3)
                await msg.delete()
            return 0

    try: allreadyinWaitQuick.remove(ballerine)
    except: pass

    team1 = []
    if user.team != 0:
        for a in userTeamDb.getTeamMember(user.team):
            team1 += [loadCharFile("./userProfile/{0}.json".format(a))]
    else:
        team1 = [user]
    teamSettings = aliceStatsDb.getTeamSettings(team1[0])

    if msg == None:
        try:
            msg = await ctx.send(embeds=await getRandomStatsEmbed(slash,team1,text="__Combat rapide en cours de génération...__"))
        except:
            msg = await ctx.channel.send(embeds=await getRandomStatsEmbed(slash,team1,text="__Combat rapide en cours de génération...__"))

    if not(isLenapy) and toTestTemp != None:
        ent = copy.deepcopy(findAllie(toTestTemp))
        global toTestChangeDict
        if toTestChangeDict == -1:
            toTestChangeDict = False
        elif type(toTestChangeDict) == int:
            ent = getAllieFromBuild(ent,ent.changeDict[toTestChangeDict])
            toTestChangeDict = False
        ent.changeLevel(MAXLEVEL,stars=5,changeDict=toTestChangeDict, changeStuff=toTestChangeDict)
        ent.owner, ent.team = user.owner, user.team
        team1 = [ent]

    fun, teamLvl = random.randint(0, 99), 0
    for ent in team1:
        teamLvl = max(ent.level,teamLvl)

    if fun < RAIDPURCENT and teamLvl >= 25:             # Raid
        await msg.edit(embeds=interactions.Embed(title="__Combat de raid__", color=light_blue, description="Les équipes sont en cours de génération..."))
        try:
            tablAllTeams, allReadySeen = userTeamDb.getAllTeamIds(True), []
            random.shuffle(tablAllTeams)

            moyTeam = 0
            for a in team1:
                moyTeam += a.level
                allReadySeen.append(a.owner)

            moyTeam = moyTeam/len(team1)

            for tempTeamId in tablAllTeams:
                try:
                    tempTeam, moyTempTeam = [], tempTeamId[1]
                    if moyTeam <= moyTempTeam+10 and moyTeam >= moyTempTeam-10 and tempTeamId[0] != user.team:
                        for a in userTeamDb.getTeamMember(tempTeamId[0]):
                            if a not in allReadySeen:
                                tempUser = loadCharFile("./userProfile/{0}.json".format(a))
                                tempTeam += [tempUser]

                        team1 += tempTeam
                        break
                except Exception as e:
                    print(e)

            del tablAllTeams, allReadySeen
            team1.sort(key=lambda overheal: overheal.level, reverse=True)
            maxLvl = team1[0].level
            team2 = []
            
            if teamLvl >= findEnnemi(RAIDHIGHLIGHT).baseLvl and random.randint(0,99) <= RAIDHIGHLIGHTPURCENT:
                alea = copy.deepcopy(findEnnemi(RAIDHIGHLIGHT))
            else:
                tablBoss = []
                for boss in range(len(tablRaidBoss)):
                    if tablRaidBoss[boss].baseLvl <= teamLvl:
                        tablBoss.append(tablRaidBoss[boss])

                alea = copy.deepcopy(tablBoss[random.randint(0, len(tablBoss)-1)])

            alea.changeLevel(maxLvl)
            team2.append(alea)

            fightResult = await fight(slash, team1, team2, ctx, True, bigMap=True, msg=msg, teamSettings=teamSettings, contexte=fightContext(nbAllies=16))
        except:
            await msg.edit(embeds=interactions.Embed(title="__Unknow error during fight__", description=format_exc()))
            teamWinDB.changeFighting(team1[0].team, value=False, channel=0)
    else:
        fightResult = await fight(slash, team1, [], ctx, msg= msg, teamSettings = teamSettings, waitEnd=False, notify=notify)

"""testing 0 : Lena, testing 1 : Liu"""

# test fights
@slash_command(name="fight_test", description="Permet de réaliser 10 combats rapides de suite", scopes=adminServ, options=[SlashCommandOption("testing",OptionType.INTEGER,required=False,description="rtfm"),SlashCommandOption(name="number",type=OptionType.INTEGER,description="Nb of fights",required=False)])
async def comTestFight(ctx,testing=False, number=10):
    try:
        user = loadCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".json")
        team1 = []
        if user.team != 0:
            for a in userTeamDb.getTeamMember(user.team):
                team1 += [loadCharFile("./userProfile/{0}.json".format(a))]
        else:
            team1 = [user]

        if not(isLenapy) and 1:
            if testing == 0:
                ent = copy.deepcopy(findAllie("Lena"))
                ent.changeLevel(MAXLEVEL,stars=5)
                ent.owner, ent.team = user.owner, user.team
                team1 = [ent]
            elif testing == 1:
                ent = getAllieFromEnemy(findEnnemi("Liu"),MAXLEVEL,[BatEarRingsorange.emoji,orangeBatshirt.emoji,orangeBatBoots.emoji],color=orange)
                ent.changeLevel(MAXLEVEL,stars=user.stars)
                ent.owner, ent.team = user.owner, user.team
                team1 = [ent]
            elif testing == 2:
                ent = copy.deepcopy(findAllie("Amandine"))
                ent.changeLevel(MAXLEVEL,stars=5)
                ent.owner, ent.team = user.owner, user.team
                team1 = [ent]
            elif testing == 3:
                ent = copy.deepcopy(findAllie("Céleste"))
                ent.changeLevel(MAXLEVEL,stars=5)
                ent.owner, ent.team = user.owner, user.team
                team1 = [ent]
        teamSettings = aliceStatsDb.getTeamSettings(team1[0])
        teamLvl, cmpt = 0, 0
        for ent in team1:
            teamLvl = max(ent.level,teamLvl)

        while cmpt < number:
            team3 = team1[:]
            fun, team2, bigMap, fightCtx = random.randint(0, 99), [], False, fightContext()
            if fun < RAIDPURCENT//3 and teamLvl >= 25:             # Raid
                alea, bigMap = copy.deepcopy(tablRaidBoss[random.randint(0, len(tablRaidBoss)-1)]), True

                if alea.name != RAIDHIGHLIGHT and random.randint(0,99) < RAIDHIGHLIGHTPURCENT:
                    alea = copy.deepcopy(findEnnemi(RAIDHIGHLIGHT))
                    if alea == None:
                        raise AttributeError("L'ennemi {0} n'a pas été trouvé".format(RAIDHIGHLIGHT))

                alea.changeLevel(teamLvl)
                team2.append(alea)
                fightCtx.nbAllies = 16 

            await fight(slash, team3, team2, ctx, teamSettings = teamSettings, testFight=True, waitEnd=False, auto=True, contexte=fightCtx, bigMap = bigMap)
            cmpt += 1
        await ctx.send("Tous les combats ont été effectués ✅")
    except:
        await ctx.send(embeds=Embed(title="<:aliceBoude:1179656601083322470> __Une erreur est survenue :__",description=format_exc(4000)))

# octogone fight
@baseOcto.subcommand(sub_cmd_name="solo", sub_cmd_description="Affrontez quelqu'un en 1v1 Gare Du Nord !")
@slash_option(name="versus", description="Affronter qui ?", opt_type=6, required=True)
async def octogone(ctx, versus):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".json"
    if not(os.path.exists(pathUserProfile)):
        await ctx.send("Comment veut-tu affronter quelqu'un si tu n'a pas de personnage ?\nVa donc faire un tour vers /start",ephemeral=True)
        return 0

    if os.path.exists(absPath + "/userProfile/" + str(int(versus.id)) + ".json"):
        await ctx.defer()
        await fight(slash, [loadCharFile(pathUserProfile)], [loadCharFile(absPath + "/userProfile/" + str(int(versus.id)) + ".json")], ctx, auto=False, octogone=True)

    elif int(versus.id) in [623211750832996354, 769999212422234122]:
        await ctx.defer()
        temp = loadCharFile(pathUserProfile)
        tempi = tablAllAllies[0]
        tempi.changeLevel(50)
        await fight(slash, [temp], [tempi], ctx, auto=False, octogone=True)

    else:
        await ctx.send("La personne que tu as désigné ne possède pas de personnage, désolée",ephemeral=True)

# team fight
@baseOcto.subcommand(sub_cmd_name="team", sub_cmd_description="Affrontez l'équipe de quelqu'un avec la votre")
@slash_option(name="versus", description="Affronter qui ?", opt_type=6, required=True)
async def teamFight(ctx, versus):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".json"
    if not(os.path.exists(pathUserProfile)):
        await ctx.send("Vous ne possédez pas de personnage.\nAllez donc faire un tour vers /start",ephemeral=True)
        return 0

    team2 = []
    pathOctogonedProfile = absPath + "/userProfile/" + str(int(versus.id)) + ".json"
    if not(os.path.exists(pathOctogonedProfile)) and int(versus.id) not in [623211750832996354, 769999212422234122]:
        await ctx.send("L'utilisateur désigné ne possède pas de personnage",ephemeral=True)
        return 0

    await ctx.defer()
    user = loadCharFile(pathUserProfile)
    team1 = []
    if user.team != 0:
        for a in userTeamDb.getTeamMember(user.team):
            team1 += [loadCharFile("./userProfile/{0}.json".format(a))]
    else:
        team1 = [user]
    if int(versus.id) not in [623211750832996354, 769999212422234122]:
        octogoned = loadCharFile(pathOctogonedProfile)
        if octogoned.team != 0:
            for a in userTeamDb.getTeamMember(octogoned.team):
                team2 += [loadCharFile("./userProfile/{0}.json".format(a))]
        else:
            team2 = [octogoned]
    else:
        tablLenaTeam = ["Lena", "Gwendoline", "Shushi", "Clémence", "Alice", "Félicité", "Iliana"]
        for a in tablLenaTeam:
            alea = copy.deepcopy(findAllie(a))
            alea.changeLevel(MAXLEVEL,stars=5)
            team2.append(alea)

    await fight(slash, team1, team2, ctx, False, octogone=True)

# -------------------------------------------- COOLDOWN --------------------------------------------
@slash_command(name="cooldowns", description="Vous donne les cooldowns des commandes /fight et /quickFight pour votre équipe")
async def cooldowns(ctx):
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".json"
    if os.path.exists(pathUserProfile):
        try:
            await ctx.defer(ephemeral=True)
        except:
            pass
        user = loadCharFile(pathUserProfile)
        involvedTeam, involvedEmoji = [[user.team,user.owner][user.team==0]], [await getUserIcon(slash,user)]

        for procur in user.haveProcurOn:
            usr = loadCharFile("./userProfile/{0}.json".format(procur))
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
            cd = teamWinDB.getFightCooldown(team,timestamp=True)
            cd2 = teamWinDB.getFightCooldown(team, True, timestamp=True)
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
                            fightingRespond += "{0} {1}\n".format(ennemi.icon, ennemi.name)
                        else:
                            fightingRespond += "<:blocked:897631107602841600> L'ennemi n'a pas pu être trouvé\n"
                        temp = ""
                    else:
                        temp += letter

                toReply.add_field(name="__Cooldowns__",value=involvedEmoji[cmpt]+"\n"+notFight+fightingRespond)
            else:
                toReply.add_field(name="__Cooldowns__",value=involvedEmoji[cmpt]+"\n"+notFight+f"__Normal__ : {cd}\n__Quick__ : {cd2}")
            
        try:
            await ctx.send(embeds = toReply,ephemeral=True)
        except:
            await ctx.send("Une erreur est survenue :\n"+format_exc(1900))

# -------------------------------------------- PATCHNOTE --------------------------------------------
@slash_command(name="patchnote", description="Renvoie le dernier patchnote du bot")
async def patchnote(ctx):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    try:
        await ctx.defer()
    except:
        pass
    await send_patchnote(ctx)

# -------------------------------------------- ROLL --------------------------------------------
@slash_command(name="roll", description="Permet de lancer un dé", options=[
    SlashCommandOption(name="min", description="Minimum du jet. Par défaut, 1",type=4, required=False),
    SlashCommandOption(name="max", description="Minimum du jet. Par défaut, 100",type=4, required=False),
])
async def roll(ctx, min=1, max=100):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    rollmes = rollMessage[random.randint(0, len(rollMessage)-1)]
    await ctx.send(embeds=interactions.Embed(title=f"🎲 roll {min} - {max}", color=light_blue, description=rollmes.format(random.randint(min, max))))

# -------------------------------------------- SHOP --------------------------------------------
@slash_command(name="shop", description="Vous permet d'entrer dans le magasin")
async def shopSlash(ctx):
    if not(await botChannelVerif(slash, ctx)): return 0
    try: await ctx.defer()
    except: pass
    await shop2(slash, ctx, shopping.shopping)


chipShopBase = SlashCommand(name="chip")
@chipShopBase.subcommand(sub_cmd_name="shop", sub_cmd_description="Permet d'entrer dans le magasin de puces")
async def chipShopCmd(ctx):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    await chipShop(slash, ctx)

@chipShopBase.subcommand(sub_cmd_name="inventory", sub_cmd_description="Permet d'ouvrir l'inventaire de puce")
async def chipInvCmd(ctx):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    if not(os.path.exists("./userProfile/{0}.json".format(int(ctx.author_id)))):
        await ctx.send("Vous n'avez pas encore de personnage. Commencez par **/start** pour en créer un !",ephemeral=True)
    else:
        user = loadCharFile(id=int(ctx.author_id))
        await chipInventory(slash,ctx,user)

# -------------------------------------------- INVENTORY --------------------------------------------
@slash_command(name="inventory", description="Vous permet de naviger dans votre inventaire", options=[
    SlashCommandOption(name="destination", description="Dans quel inventaire voulez-vous aller ?", type=3, required=False, choices=[
        interactions.SlashCommandChoice(name="Equipement", value="0"),
        interactions.SlashCommandChoice(name="Arme", value="1"),
        interactions.SlashCommandChoice(name="Compétences", value="2"),
        interactions.SlashCommandChoice(name="Objets spéciaux", value="3"),
        interactions.SlashCommandChoice(name="Elements", value="4"),
        interactions.SlashCommandChoice(name="Puces", value="5")
    ]),
    SlashCommandOption(name="procuration", description="De qui voulez vous consulter l'inventaire ?", type=6, required=False),
    SlashCommandOption(name="item", type=3, required=False, description="Quel est le nom de votre object ?")
])
async def invent2(ctx, destination=0, procuration=None, item=None):
    try:
        if not(await botChannelVerif(slash, ctx)):
            return 0
        try:
            await ctx.defer()
        except:
            pass

        try:
            user = loadCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".json")
            if procuration != None:
                if int(procuration.id) in user.haveProcurOn:
                    user = loadCharFile(absPath + "/userProfile/" + str(procuration.id) + ".json")
                else:
                    msg = await ctx.send(embed=Embed("__Inventory :__",description="Vous n'avez pas procuration sur ce personnage"))
                    await asyncio.sleep(15)
                    await msg.delete()
                    return 0
        except:
            msg = await ctx.send(embed=Embed("__Inventory :__",description="Vous ou bien l'utilisateur ciblé n'avez pas de personnage\nLa commande /start permet d'en créer un"))
            await asyncio.sleep(15)
            await msg.delete()
            return 0

        if item != None:
            item = item.replace("_", " ")
            item = remove_accents(item.lower())
            while item.endswith(" "):
                item = item[0:-1]

            research = weapons[:]+skills[:]+stuffs[:]+others[:]+[token,trans]
            lastResarch = []
            nameTempCmpt, lenName, findId = 0, len(item), False
            for obj in research:
                if item == obj.id:
                    item, findId = obj.id, True
                    break

            if not(findId):
                lookingFor = []
                for tempItem in research:
                    if item in remove_accents(tempItem.name.lower()):
                        lookingFor.append(tempItem)

                if len(lookingFor) == 1:
                    item = lookingFor[0].id
                elif len(lookingFor) > 1:
                    tablOption, desc, dictItems = [], "", {}
                    for tempItem in lookingFor:
                        tablOption.append(interactions.StringSelectOption(label=unhyperlink(tempItem.name), value=tempItem.id, emoji=getEmojiObject(tempItem.emoji)))
                        dictItems[tempItem.id] = tempItem
                        desc += "{0}\n".format(tempItem)

                    if len(tablOption) > 24:
                        tablOption.sort(key=lambda ballerine: dictItems[ballerine.value].minLvl >= user.level-5 and dictItems[ballerine.value].minLvl <= user.level+5, reverse=True)
                        tablOption = tablOption[:24]

                    selectOption = ActionRow(StringSelectMenu(tablOption,placeholder="Sélectionnez un object",custom_id="selectOption"))
                    msg = await ctx.send(embeds=Embed(title="__Inventory :__",description="Plusieurs objets au nom proche de celui recherché ont été trouvé :\n\n"+desc),components=[selectOption])

                    def check(m):
                        m = m.ctx
                        return int(m.message.id) == int(msg.id) and int(m.author.id) == int(ctx.author.id)

                    try:
                        rep = await slash.wait_for_component(messages=[msg], components=[selectOption], check=check, timeout=60)
                        rep: interactions.ComponentContext = rep.ctx

                        item = rep.values[0]
                        for opt in tablOption:
                            if opt.value == item:
                                opt.default=True
                        selectOption = ActionRow(StringSelectMenu(tablOption,custom_id="selectOption",disabled=True))
                        await msg.edit(embeds=Embed(title="__Inventory :__",description="Plusieurs objets au nom proche de celui recherché ont été trouvé :\n\n"+desc),components=[selectOption])
                        ctx = rep
                    except asyncio.TimeoutError:
                        await msg.edit(embeds=Embed(title="__Inventory :__",description="Plusieurs object au nom proche de celui recherché ont été trouvé :\n\n"+desc),components=[])
                        return 0
                else:
                    while 1:
                        lastResarch = research[:]
                        if nameTempCmpt+1 <= lenName:
                            nameTempCmpt += 1
                        else:
                            nameTempCmpt = lenName

                        for a in research[:]:
                            temp = remove_accents(a.name.lower())
                            if item[0:nameTempCmpt] not in temp:
                                research.remove(a)

                        leni = len(research)
                        if leni == 1:
                            item = research[0].name
                            break
                        elif leni <= 0 or nameTempCmpt == lenName:
                            desc = ""
                            options = []
                            for a in lastResarch:
                                have = ""
                                if not(user.have(a)):
                                    have = "`"
                                desc += "{0} {2}{1}{2}\n".format(a.emoji, a.name, have)
                                options += [interactions.StringSelectOption(label=unhyperlink(a.name), value=a.name, emoji=getEmojiObject(a.emoji))]

                            if len(options) > 24:
                                def getNameSortValue(obj):
                                    cmpt = 0
                                    for letter in item:
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
                                    options += [interactions.StringSelectOption(unhyperlink(a.name), a.name, getEmojiObject(a.emoji))]
                            select = interactions.StringSelectMenu(options,custom_id = "invSherchMenu", placeholder="Sélectionnez un objet")
                            msg = await ctx.send(embeds=interactions.Embed(title="/inventory", color=light_blue, description="L'objet spécifié n'a pas été trouvé. Voici une liste des résultats les plus proches :\n\n"+desc), components=[interactions.ActionRow(select)])

                            def check(m):
                                m = m.ctx
                                return int(m.author.id) == int(ctx.author.id) and int(m.message.id) == int(msg.id)

                            try:
                                respond = await slash.wait_for_component(components=select, check=check, timeout=60)
                                respond = respond.ctx
                            except asyncio.TimeoutError:
                                await msg.edit(embeds=interactions.Embed(title="/inventory", color=light_blue, description="Liste des résultats correspondant à la recherche\n\n"+desc), components=[])
                                return 0

                            item = respond.values[0]
                            await msg.edit(embeds=interactions.Embed(title="/inventory", color=light_blue, description="L'objet spécifié n'a pas été trouvé. Voici une liste des résultats les plus proches :\n\n"+desc), components=[interactions.ActionRow(getChoisenSelect(select, respond.values[0]))])
                            break

            if item == token.name:
                obj = token
                repEmb = infoOther(obj, user)
                try:
                    await ctx.send(embeds=repEmb, components=[])
                except:
                    await ctx.channel.send(embeds=repEmb, components=[])
                return 0
            elif item in [trans.name,"lb"]:
                transField = "La **Transcendance** est une compétence commune à tous les joueurs et alliés temporaires débloquée et équipée automatiquement dès le début.\nLorsqu'utilisée, cette compétence deviens l'une des compétences listée si dessous en fonction du itembre de **jauges transcendiques** remplie ainsi que de l'aspiration du lanceur.\nLe itembre de jauges transcendiques disponibles dans un combat dépend de divers critères. Chaques critères remplie rajoute une barre pour l'équipe en question :\n> - L'équipe comporte au moins 8 membres\n> - L'équipe comporte au moins 16 membres\n> - L'équipe adverse contient au moins 1 boss\n> - L'équipe adverse est composée d'un boss AllvOne\n> - L'équipe adverse est composée d'alliés temporaires ou de joueurs\n\nLorsqu'utilisée, toutes les **jauges transcendiques** de l'équipe sont remises à 0, même si elles n'étaient pas toutes remplies."
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

        if item != None:
            await inventory(slash, ctx, item, procur=user.owner)
        else:
            await inventoryV2(slash, ctx, int(destination), user)
    except:
        await ctx.send(embed=Embed(title="<:aliceBoude:1179656601083322470> __Une erreur est survenue :__",description=format_exc(4000)))
# -------------------------------------------- POINTS --------------------------------------------
choicesTabl = []
for cmpt in range(MAGIE+1):
    choicesTabl.append(SlashCommandChoice(name=allStatsNames[cmpt],value=cmpt))

@slash_command(name="points", description="Vous permet de répartir vos points bonus", options=[
    SlashCommandOption(name="procuration", description="De qui voulez vous consulter les points bonus ?", type=6, required=False),
    SlashCommandOption(name="stat",description="Dans quelle statistique voulez-vous attribuer vos points bonus", type=OptionType.INTEGER, choices=choicesTabl, required=False),
    SlashCommandOption(name="points",description="Combien de points voulez-vous attribuer ?", type=OptionType.INTEGER, required=False, min_value=1, max_value=MAXBONUSPERSTAT)
])
async def pts(ctx, procuration=None,stat=None,points=None):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    await pointsCmd(slash, ctx, procuration, stat, points)

# -------------------------------------------- TEAM --------------------------------------------
detailPlus = interactions.Button(style=ButtonStyle.PRIMARY, label="Aff. détaillé", emoji=PartialEmoji(name="➕"), custom_id="detail")
detailMinus = interactions.Button(style=ButtonStyle.PRIMARY, label="Aff. simplifié", emoji=PartialEmoji(name="➖"), custom_id=detailPlus.custom_id)

baseTeam = SlashCommand(name="team",description="Permet de gérer votre équipe")

# team view
teamViewButtonList = [
    Button(style=ButtonStyle.GRAY,label="Afficher compétences",emoji=getEmojiObject(splatbomb.emoji),custom_id="aff_1"),
    Button(style=ButtonStyle.GRAY,label="Afficher équipement",emoji=getEmojiObject(uniform.emoji),custom_id="aff_2"),
    Button(style=ButtonStyle.GRAY,label="Afficher statistiques",emoji=getEmojiObject(statsEmojis[ENDURANCE]),custom_id="aff_3"),
    Button(style=ButtonStyle.GRAY,label="Affichage réduit",emoji=PartialEmoji(name="➖"),custom_id="aff_0")
]

@baseTeam.subcommand(sub_cmd_name="view", sub_cmd_description="Permet de voir les équipements de votre équipe ou de celle de quelqu'un d'autre", options=[
    SlashCommandOption(name="joueur", description="Voir l'équipe d'un autre joueur", type=6, required=False),
    SlashCommandOption(name="affichage",type=OptionType.INTEGER,description="Utiliser un affichage particulié",required=False,choices=[
        SlashCommandChoice("Réduit",0),
        SlashCommandChoice("Compétences",1),
        SlashCommandChoice("Equipements",2),
        SlashCommandChoice("Statistiques",3)
    ])
])
async def teamView(ctx, joueur=None,affichage=0):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    if joueur == None:
        joueur = ctx.author
    pathUserProfile = absPath + "/userProfile/" + str(joueur.id) + ".json"

    if os.path.exists(pathUserProfile):
        await ctx.defer()
        user, msg = loadCharFile(pathUserProfile), None
        if user.team == 0:
            user = newTeam(user)
            teamMates = [user]
        else:
            teamMates = []
            for usr in userTeamDb.getTeamMember(user.team):
                teamMates.append(loadCharFile(path="./userProfile/{0}.json".format(usr)))

        def checky(m):
            m = m.ctx
            return m.author.id == ctx.author.id

        while 1:
            temp = ""
            if affichage == 0:
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
                    emb.add_field(name="<:em:866459463568850954>\n__Résultats des derniers combats :__",value=teamWinDB.getVictoryStreakStr(user))

            else:
                emb = await getFullTeamEmbed(slash, teamMates, user, affichage-1)

            if msg != None:
                await msg.edit(embeds=emb, components=[interactions.ActionRow(teamViewButtonList[affichage])])
            else:
                msg = await ctx.send(embeds=emb, components=[interactions.ActionRow(teamViewButtonList[affichage])])

            try:
                react = await slash.wait_for_component(msg, check=checky, timeout=60)
                react: ComponentContext= react.ctx
            except:
                await msg.edit(embeds=emb, components=[])
                break

            if react.custom_id.startswith("aff"):
                affichage = (affichage+1)%4

# team add
@baseTeam.subcommand(sub_cmd_name="add", sub_cmd_description="Permet de rajouter un joueur dans son équipe", options=[
    SlashCommandOption(name="joueur", description="Le joueur à rajouter", type=6, required=True)
])
async def teamAdd(ctx: SlashContext, joueur:Member):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".json"
    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile)
        await ctx.defer()
        msg = None

        if user.team == 0:
            user = newTeam(user)

        selfTeam = userTeamDb.getTeamMember(user.team)

        if ctx.author.id == joueur.id:
            await ctx.send(embeds=errorEmbed("/team add "+joueur.name, "Vous voulez faire équipe avec vous-même ?"))
        elif not(len(selfTeam) >= 8) and not(ctx.author.id == joueur.id):
            mention = joueur
            if os.path.exists(absPath + "/userProfile/" + str(mention.id) + ".json"):
                mate =loadCharFile(absPath + "/userProfile/" + str(mention.id) + ".json")
                if mate.team != 0:
                    if mate.team == user.team:
                        await ctx.send(embeds=errorEmbed("/team add "+mate.name, "Ce joueur est déjà dans ton équipe"))
                        return 0
                    elif len(userTeamDb.getTeamMember(mate.team))>1:
                        await ctx.send(embeds=errorEmbed("/team add "+mate.name, "Ce joueur a déjà une équipe"))
                        return 0

                msg = await ctx.send(content=mention.mention,
                                     embeds=interactions.Embed(title="/team add "+mate.name, color=user.color, description="{0}, {1} vous propose de rejoidre son équipe. Qu'en dites vous ?".format(mention.mention,ctx.author.mention)),
                                     components=[
                                         ActionRow(
                                                Button(label="Accepter",style=ButtonStyle.GREEN,emoji=PartialEmoji(name="✅"),custom_id="✅"),
                                                Button(label="Refuser",style=ButtonStyle.GREY,emoji=PartialEmoji(name="❌"),custom_id="❌")
                                            )
                                        ])

                def checkisIntendedUser(component):
                    component: ComponentContext = component.ctx
                    return int(component.author_id) == int(mention.id)

                try:
                    react = await slash.wait_for_component(messages=msg, timeout=60, check=checkisIntendedUser)
                    react: ComponentContext= react.ctx
                except:
                    await msg.edit(embeds=errorEmbed("/team add "+mate.name, "La commande n'a pas pu aboutir"))
                    return 0

                if react.custom_id == "✅":
                    mate.team = user.team
                    saveCharFile(absPath + "/userProfile/" +str(mention.id) + ".json", mate)
                    team = userTeamDb.getTeamMember(user.team)
                    team.append(mention.id)
                    userTeamDb.updateTeam(user.team, team)
                    await msg.edit(embeds=interactions.Embed(title="/team add "+user.name, color=user.color, description="Vous faites dorénavent parti de la même équipe"),components=[])
                else:
                    await msg.edit(embeds=interactions.Embed(title="/team add "+user.name, color=red, description="Vous avez refusé l'invitation"),components=[])


            else:
                await ctx.send(embeds=errorEmbed("/team add "+user.name, "Cet utilisateur n'a pas commencé l'aventure"))
        else:
            await ctx.send(embeds=errorEmbed("/team add "+user.name, "Votre équipe est déjà au complet"))

# team quit
@baseTeam.subcommand(sub_cmd_name="leave", sub_cmd_description="Permet de quitter son équipe")
async def teamQuit(ctx: SlashContext):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".json"
    if os.path.exists(pathUserProfile):
        await ctx.defer()
        user = loadCharFile(pathUserProfile)
    team = userTeamDb.getTeamMember(user.team)
    if len(team) > 1:
        msg = await ctx.send(embeds=interactions.Embed(title="/team quit", color=user.color, description="Voulez vous vraiment quitter votre équipe ?"),components=[ActionRow(Button(label="Quitter l'équipe",style=ButtonStyle.RED,emoji=PartialEmoji(name="✅"),custom_id="✅"),Button(label="Abandonner",style=ButtonStyle.GREY,emoji=PartialEmoji(name="❌"),custom_id="❌"))])
        
        def check(r):
            r = r.ctx
            return r.author_id == ctx.author_id
        
        try:
            react = await slash.wait_for_component(messages=msg,check=check,timeout=60)
            react: ComponentContext= react.ctx
        except asyncio.TimeoutError:
            await msg.delete()
            return 0
        
        if react.custom_id == "✅":
            team.remove(ctx.author.id)
            userTeamDb.updateTeam(user.team, team)
            user = newTeam(user)
            saveCharFile(pathUserProfile, user)
            await msg.edit(embeds=interactions.Embed(title="/team quit", color=user.color, description="Vous avez bien quitté votre équipe"),components=[])
        else:
            await msg.delete()
    else:
        await ctx.send(embeds=errorEmbed("/team quit", "Vous n'avez aucune équipe à quitter"))

# team fact
@baseTeam.subcommand(sub_cmd_name="facts", sub_cmd_description="Permet d'avoir des facts sur les membres de votre équipe")
async def teamFact(ctx):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".json"
    if os.path.exists(pathUserProfile):
        await ctx.defer()
        user = loadCharFile(pathUserProfile)
    else:
        await ctx.send("Vous n'avez pas de personnage",ephemeral=True)

    teamUser = []

    if user.team != 0:
        for a in userTeamDb.getTeamMember(user.team):
            teamUser.append(loadCharFile(absPath + "/userProfile/" + str(a) + ".json"))

    else:
        teamUser.append(user)

    button = interactions.ActionRow(interactions.Button(style=2, label="Autre fact", emoji=PartialEmoji(name="🔄"), custom_id="🔄"))
    msg = None

    while 1:
        emb = await getRandomStatsEmbed(slash, teamUser, "/team facts", fullStats=True)
        if msg == None:
            msg = await ctx.send(embeds=emb, components=[button])
        else:
            await msg.edit(embeds=emb, components=[button])

        try:
            await slash.wait_for_component(msg, timeout=60)
        except:
            await msg.edit(embeds=emb, components=[])
            break

@slash_command(name="tips",description="Vous donne un conseil ou une précision sur les mécaniques de combat")
async def tipsCommand(ctx):
    button = interactions.ActionRow(interactions.Button(style=2, label="Autre fact", emoji=PartialEmoji(name="🔄", custom_id="🔄")))
    msg = None

    while 1:
        emb = await getRandomStatsEmbed(slash, [], "/tips", fullTips=True)
        if msg == None:
            msg = await ctx.send(embeds=emb, components=[button])
        else:
            await msg.edit(embeds=emb, components=[button])

        try:
            await slash.wait_for_component(msg, timeout=60)
        except:
            await msg.edit(embeds=emb, components=[])
            break

# -------------------------------------------- HELP --------------------------------------------
@slash_command(name="help", description="Ouvre la page d'aide du bot")
async def helpCom(ctx):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    await helpBot(slash, ctx)

# -------------------------------------------- START --------------------------------------------
@slash_command(name="start", description="Permet de commence l'aventure")
async def started(ctx):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    await start(slash, ctx)

# -------------------------------------------- CHARACTER --------------------------------------------
baseChar = SlashCommand(name="character")

@baseChar.subcommand(sub_cmd_name="info", sub_cmd_description="Permet de voir votre page de personnage ou celle d'un autre joueur", options=[SlashCommandOption(name="joueur", description="Voir les statistiques d'un autre joueur", type=6, required=False)])
async def statsCmd(ctx, joueur=None):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    if joueur == None:
        pathUserProfile = absPath + "/userProfile/" + \
            str(ctx.author.id) + ".json"
    else:
        pathUserProfile = absPath + "/userProfile/" + str(joueur.id) + ".json"

    if os.path.exists(pathUserProfile):
        msg = await loadingSlashEmbed(ctx)
        user = loadCharFile(pathUserProfile)

        userIcon = await getUserIcon(slash, user)

        level = str(
            user.level)+['', "<:littleStar:925860806602682369>{0}".format(user.stars)][user.stars > 0]
        exp = [str(user.level*50-20), "MAX"][user.level == MAXLEVEL]
        rep = interactions.Embed(title=f"__Page de statistique de {user.name} {userIcon}__", color=user.color,description=f"__Niveau :__ {level}\n__Expérience :__ {user.exp} / {exp}\n\n__Element :__ {elemEmojis[user.element]} {elemNames[user.element]} ({elemEmojis[user.secElement]} {elemNames[user.secElement]})\n__Aspiration :__ {aspiEmoji[user.aspiration]} {inspi[user.aspiration]}")

        rep.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(userIcon).id))
        sumStatsBonus = [user.majorPoints[0], user.majorPoints[1], user.majorPoints[2], user.majorPoints[3], user.majorPoints[4], user.majorPoints[5], user.majorPoints[6], user.majorPoints[7], user.majorPoints[8], user.majorPoints[9], user.majorPoints[10], user.majorPoints[11], user.majorPoints[12], user.majorPoints[13], user.majorPoints[14]]

        for a in [user.weapon]+user.stuff:
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
        rep.add_field(name="<:em:866459463568850954>\n__Stats. principaux :__",value=value, inline=False)
        value = ""
        for cmpt in range(RESISTANCE,CRITICAL+1):
            value += "\n{0} __{1}__ : {2}".format(statsEmojis[cmpt],allStatsNames[cmpt],allStatsUser[cmpt]+sumStatsBonus[cmpt])
            if cmpt == RESISTANCE:
                value += "\n> Réduction de dégâts : {0}%".format(round(getResistante(allStatsUser[RESISTANCE]+sumStatsBonus[RESISTANCE])))
            elif cmpt == PERCING: 
                value += "\n> Réduction de dégâts ignoré : {0}%".format(round(getPenetration(allStatsUser[PERCING]+sumStatsBonus[PERCING])))
            getPenetration
        rep.add_field(name="<:em:866459463568850954>\n__Stats. secondaires :__",value=value, inline=True)
        value = ""
        for cmpt in range(ACT_HEAL_FULL,ACT_INDIRECT_FULL+1):
            value += "\n{0} __{1}__ : {2}".format(statsEmojis[cmpt],allStatsNames[cmpt],allStatsUser[cmpt]+sumStatsBonus[cmpt])
        rep.add_field(name="<:em:866459463568850954>\n__Stats. d'actions :__",value=value, inline=True)
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

        rep.add_field(name="<:em:866459463568850954>",value='**__Objets équipés :__**',inline=False)
        rep.add_field(name="__Arme et équipements :__",value=user.weapon.emoji+" "+user.weapon.name+"\n\n"+tempStuff, inline=True)
        rep.add_field(name="__Compétences :__",value=tempSkill, inline=True)

        tempMsg = ""
        for tmpChip in user.equippedChips:
            tempMsg += str(getChip(tmpChip))+"\n"
        if tempMsg != "":
            rep.add_field(name="__Puces :__",value=tempMsg,inline=True)

        await msg.edit(embeds=rep)

    else:
        if joueur == None:
            await ctx.send("Tu n'a pas commencé l'aventure")
        else:
            await ctx.send("{0} n'a pas commencé l'aventure".format(joueur.name))

@baseChar.subcommand(sub_cmd_name="settings", sub_cmd_description="Permet de modifier les paramètres de son icone de personnage", options=[SlashCommandOption(name="joueur", description="Voir les statistiques d'un autre joueur", type=6, required=False)])
async def char_settings(ctx, joueur=None):
    user = loadCharFile("./userProfile/{0}.json".format(ctx.author.id))
    if joueur != None:
        procurUser = loadCharFile("./userProfile/{0}.json".format(int(joueur.id)))
        if joueur.id in user.haveProcurOn:
            user = loadCharFile("./userProfile/{0}.json".format(int(joueur.id)))
        else:
            await ctx.send("Vous n'avez pas procuration sur ce personnage",ephemeral=True)
            return 0
    await userSettings(slash, user, ctx)

# -------------------------------------------- MANUEL --------------------------------------------
@slash_command(name="manuel", description="Permet de consulter le manuel de l'Aventure", options=[
    SlashCommandOption(name="page", description="Spécifiez une page à laquelle ouvrir le manuel", type=4, required=False)
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
            reaction = await slash.wait_for_component("reaction_add", timeout=380, check=checkReaction)
        except:
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
baseSee = SlashCommand(name="see",scopes=adminServ)
@baseSee.subcommand(sub_cmd_name="fightlogs", sub_cmd_description="Permet de consulter les logs des combats du jour")
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
            option.append(interactions.StringSelectOption(log, log))

        emb = interactions.Embed(
            title="__Logs des combats du jour__", color=light_blue, description=desc)

        if len(option) > 0:
            select = interactions.StringSelectMenu(custom_id = "seeFightLogs", options =option)
        else:
            select = interactions.StringSelectMenu(custom_id = "seeFightLogs", options= [interactions.StringSelectOption(label="disabled", value="0")], placeholder="Il n'y a aucun logs à afficher", disabled=True)

        if page != 0:
            previousBoutton = interactions.Button(style=ButtonStyle(2), label="Page précédente", emoji=PartialEmoji(name="◀️"), custom_id="back")
        else:
            previousBoutton = interactions.Button(style=ButtonStyle(2), label="Page précédente", emoji=PartialEmoji(name="◀️"), custom_id="back", disabled=True)
        if page != maxPage:
            nextBoutton = interactions.Button(style=ButtonStyle(2), label="Page suivante", emoji=PartialEmoji(name="▶️"), custom_id="forward")
        else:
            nextBoutton = interactions.Button(style=ButtonStyle(2), label="Page suivante", emoji=PartialEmoji(name="▶️"), custom_id="forward", disabled=True)

        buttons = interactions.ActionRow(previousBoutton, nextBoutton)

        if msg == None:
            try:
                msg = await ctx.send(embeds=emb, components=[interactions.ActionRow(select), buttons])
            except:
                msg = await ctx.channel.send(embeds=emb, components=[interactions.ActionRow(select), buttons])
        else:
            await msg.edit(embeds=emb, components=[interactions.ActionRow(select), buttons])

        try:
            respond = await slash.wait_for_component(msg, timeout=180)
        except:
            break

        try:
            resp = respond.values[0]
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
@baseSee.subcommand(sub_cmd_name="stuffrepartition", sub_cmd_description="Permet de consulter la réportation des logs")
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
    ssrTypeChoice.append(SlashCommandChoice(name=allTypeNames[cmpt],value=cmpt))
ssrAspiChoice = []
for cmpt in range(MASCOTTE+1):
    ssrAspiChoice.append(SlashCommandChoice(name=inspi[cmpt],value=cmpt))
ssrElemChoice = []
for cmpt in range(ELEMENT_TIME+1):
    ssrElemChoice.append(SlashCommandChoice(name=elemNames[cmpt],value=cmpt))
ssrUseChoice = []
for cmpt in range(MAGIE+1):
    ssrUseChoice.append(SlashCommandChoice(name=nameStats[cmpt],value=cmpt))

@baseSee.subcommand(sub_cmd_name="skill_repartition",options=[
    SlashCommandOption(type=OptionType.INTEGER,name="skilltype",choices=ssrTypeChoice,description="Le type de compétence à voir"),
    SlashCommandOption(type=OptionType.INTEGER,name="aspiration",choices=ssrAspiChoice,description="Afficher les compétences exclusives à une aspiration",required=False),
    SlashCommandOption(type=OptionType.INTEGER,name="element",choices=ssrElemChoice,description="Afficher les compétences exclusives à un élément",required=False),
    SlashCommandOption(type=OptionType.INTEGER,name="use",choices=ssrUseChoice,description="Afficher uniquement les compétences utilisant une statistique",required=False),
    SlashCommandOption(type=OptionType.INTEGER,name="skillrange",choices=[SlashCommandChoice(name="Mêlée",value=0),SlashCommandChoice(name="Distance",value=1)],description="Afficher uniquement les compétences avec une portée spécifique",required=False)
    ])
async def seeSkillRepartition(ctx: interactions.SlashContext, skilltype: int, aspiration: Union[int, None] = None, element: Union[int, None] = None, use: Union[int,None] = None, skillrange: Union[int, None] = None):
    try:
        await ctx.defer()
    except:
        ctx = await ctx.channel.send(embeds=Embed(title="__skill_repartition__",description="Chargement..."))
    try:
        await seeSkillsRep(ctx, skilltype, aspiration, element, use, skillRange)
    except Exception as e:
        await ctx.send(content=e.__str__())

# -------------------------------------------- CHOOSE --------------------------------------------
@slash_command(name="choose", description="Renvoie une élément aléatoire de la liste donnée", options=[
    SlashCommandOption(name="choix1", description="Le premier élément de la liste",type=interactions.OptionType.STRING, required=True),
    SlashCommandOption(name="choix2", description="Le second élément de la liste",type=interactions.OptionType.STRING, required=True),
    SlashCommandOption(name="choix3", description="Un potentiel troisième de la liste",type=interactions.OptionType.STRING, required=False),
    SlashCommandOption(name="choix4", description="Un potentiel quatrième de la liste",type=interactions.OptionType.STRING, required=False),
    SlashCommandOption(name="choix5", description="Un potentiel cinquième de la liste",type=interactions.OptionType.STRING, required=False)
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
baseAdmin = SlashCommand(name="admin",scopes=adminServ, description="Permet d'utiliser les commandes administrateurs")

@baseAdmin.subcommand(sub_cmd_name="enable_fight", sub_cmd_description="Permet d'activer les combats ou non", options=[
    SlashCommandOption(name="valeur", description="Activer ou désaciver les combats", type=OptionType.BOOLEAN, required=False)
])
async def addEnableFight(ctx, valeur=None):
    globalVar.changeFightEnabled(valeur)
    if valeur == None:
        valeur = globalVar.fightEnabled()

    if not(valeur):
        await slash.change_presence(status=Status.DND,activity=Activity(name="Les combats sont désactivés",type=ActivityType.GAME))
    else:
        ballerine = datetime.now(parisTimeZone)
        while ballerine.hour % 3 != 0:
            ballerine = ballerine + timedelta(hours=1)

        await slash.change_presence(status=Status.ONLINE,activity=Activity(name="Prochain shop à "+ballerine.strftime('%Hh'),type=ActivityType.GAME))

    await ctx.send(embeds=interactions.Embed(title="__Admin Enable Fight__", description="Les combats sont désormais __{0}__".format(["désactivés", "activés"][int(valeur)]), color=[red, light_blue][int(valeur)]))

@baseAdmin.subcommand(sub_cmd_name="restart_bot", sub_cmd_description="Permet de redémarrer le bot lorsque tous les combats seront fini")
async def restartCommand(ctx):
    print("Got the restart program signal !")
    await restart_program(ctx)

@baseAdmin.subcommand(sub_cmd_name="backup_new", sub_cmd_description="Permet de réaliser un backup des profiles de personnages")
async def adminBackup(ctx):
    temp = create_backup()
    try:
        await ctx.send(embeds=interactions.Embed(title="__Admin : Backups__", color=light_blue, description=temp))
    except:
        await ctx.channel.send(embeds=interactions.Embed(title="__Admin : Backups__", color=light_blue, description=temp))

@baseAdmin.subcommand(sub_cmd_name="force_new_shop", sub_cmd_description="Refait le shop")
async def forceShop(ctx):
    try:
        await shopping.newShop()
        await ctx.send("Succès")
    except:
        await ctx.send("Echec")

@baseAdmin.subcommand(sub_cmd_name="force_chip_shop")
async def forceChipShop(ctx):
    await ctx.defer()
    try:
        newChipShop()
        await ctx.send("Succès")
    except:
        await ctx.send("Une erreur est survenue :\n"+format_exc())

@baseAdmin.subcommand(sub_cmd_name="reset_records")
async def resetRecord(ctx):
    await ctx.send(embeds=interactions.Embed(title="__Reset des records__", color=light_blue, description=aliceStatsDb.resetRecords()))

@baseAdmin.subcommand(sub_cmd_name="give_achivements",options=[SlashCommandOption(type=OptionType.STRING,name="id",required=True,description="Id de l'utilisateur")])
async def giveAchivments(ctx:interactions.SlashContext,id:int):
    await ctx.defer()
    user = loadCharFile(path="./userProfile/{0}.json".format(id))
    userAchiv, nbModif, nbError = achivementStand.getSuccess(user), 0, 0
    for achiv in userAchiv.tablAllSuccess():
        if achiv.name not in ["Filer comme le vent","Qui continue de briller dans le Noir"] and not(achiv.haveSucced):
            try:
                achiv.count, achiv.haveSucced = achiv.countToSucced, True
                achivementStand.updateSuccess(user,achiv)
                nbModif += 1
            except:
                nbError += 1
                print_exc()
    await ctx.send("Succès Modif : {0}\nEchecs : {1}".format(nbModif,nbError))

# ------------- emoji
groupComEmoji = SlashCommand(name="emoji",description="Commandes en rapport avec les emojis")

@groupComEmoji.subcommand(sub_cmd_name="reset_all", sub_cmd_description="Lance une rénitialisation des emojis")
async def resetCustomEmoji(ctx):
    msg = await ctx.send(embeds=interactions.Embed(title="Rénitialisation des emojis..."))
    await slash.change_presence(status=Status.IDLE,activity=Activity(name="Refaire les émojis...",type=ActivityType.GAME))

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
        emojiGuild = slash.get_guild(a)
        emojiList = await emojiGuild.fetch_all_custom_emojis()
        allEmojisNum += len(emojiList)

    cmpt = 0
    now = datetime.now(parisTimeZone).second
    lastTime = copy.deepcopy(now)
    for a in iconGuildList:
        emojiGuild = slash.get_guild(a)
        emojiList = await emojiGuild.fetch_all_custom_emojis()
        for b in emojiList:
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
    await downloadAllIconPng(slash)
    await downloadElementIcon(slash)

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

    ballerine = datetime.now(parisTimeZone)
    while ballerine.hour % 3 != 0:
        ballerine = ballerine + timedelta(hours=1)

    await slash.change_presence(status=Status.ONLINE,activity=Activity(name="Prochain shop à "+ballerine.strftime('%Hh'),type=ActivityType.GAME))

@groupComEmoji.subcommand(sub_cmd_name="remake_all", sub_cmd_description="Supprime puis refait tous les emojis de personnage")
async def remakeCustomEmoji(ctx):
    await remakeEmojis(ctx)

subStat = baseAdmin.group(name="stat",description="Permet de gérer les stats des utilisateurs")
@subStat.subcommand(sub_cmd_name="silent_restat_all", sub_cmd_description="silentRestat all users")
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

@subStat.subcommand(sub_cmd_name="restat_all",sub_cmd_description="Permet de restat tout le monde")
async def restatForEveryone(ctx):
    msg = await ctx.send(embeds=interactions.Embed(title="__/admin stat RestallAll__", color=light_blue, description="Restats en cours..."))
    try:
        for fileName in os.listdir("./userProfile/"):
            user = loadCharFile("./userProfile/"+fileName)
            user = restats(user)
            saveCharFile(user=user)
        await msg.edit(embeds=interactions.Embed(title="__/admin stat silentRestallAll__", color=light_blue, description="Tous les utilisateurs ont été restats 👍"))
    except:
        await msg.edit(embeds=interactions.Embed(title="__/admin stat silentRestallAll__", description="Une erreur est survenue :\n"+format_exc()))

# -------------------------------------------- KIKIMETER --------------------------------------------
if isLenapy:
    tabl = [912137828614426704, 405331357112205326]
else:
    tabl = adminServ

@slash_command(name="kikimeter", description="Allow to see players, allies and ennemies stats", scopes=tabl, options=[
    SlashCommandOption(type=OptionType.BOOLEAN,name="last",description="Show last mounth stats",required=False)
])
async def kikimeter(ctx,last=False):
    await kikimerFunction(bot=slash,ctx=ctx,period=last)

@slash_command(name='osamodas',description="Donne une liste des invocations capturables par un Osamodas (Wakfu)",scopes=tabl,options=[
    SlashCommandOption(name="niveau",type=OptionType.INTEGER,description="Le niveau maximal (arrondi à la tranche suppérieure) à afficher",required=False,min_value=1,max_value=WAKFUMAXLEVEL),
    SlashCommandOption(name="type",type=OptionType.INTEGER,description="Le type d'invocation à afficher",required=False,choices=[
        SlashCommandChoice(name="Tous",value=SMN_TYPE_ALL),
        SlashCommandChoice(name="Dégâts",value=TYPE_DAMAGE),
        SlashCommandChoice(name="Soins",value=TYPE_HEAL),
        SlashCommandChoice(name="Tank",value=TYPE_ARMOR),
        SlashCommandChoice(name="Support",value=TYPE_BOOST)
    ])
])
async def osamodasCmd(ctx,niveau=WAKFUMAXLEVEL,type=SMN_TYPE_ALL):
    try:
        await ctx.defer()
    except:
        ctx = await ctx.channel.send(embeds=interactions.Embed(title="__Osamodas Summons__",description="Chargement..."))

    niveau = 20+(15*((niveau//15)))
    await osaSmnCommand(ctx,slash,level=niveau,type=type)

# -------------------------------------------- PROCURATION --------------------------------------------
@slash_command(name="procuration", description="Permet de donner à un autre utilisateur procuration sur votre inventaire", options=[SlashCommandOption(name="utilisateur", description="L'utilisateur qui pourra modifier vos objets équipés", type=6, required=True)])
async def procurCmd(ctx, utilisateur):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    await procuration(ctx, utilisateur)

# -------------------------------------------- ICON --------------------------------------------
@slash_command(name="icon", description="Renvoie l'icone de votre personnage", options=[SlashCommandOption(name="utilisateur", description="Voir l'icone d'un autre utilisateur", type=6, required=False)])
async def iconCommand(ctx, utilisateur=None):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    try:
        if utilisateur == None:
            user = loadCharFile("./userProfile/{0}.json".format(ctx.author.id))
        else:
            user = loadCharFile(
                "./userProfile/{0}.json".format(utilisateur.id))
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
@slash_command(name="roulette", description="Permet d'utiliser un Jeton de roulette pour obtenir un objet ou des pièces",options=[SlashCommandOption(name="procuration", type=6, required=False)])
async def rouletteSlash(ctx, procuration=None):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    try:
        user = loadCharFile("./userProfile/{0}.json".format(ctx.author.id))
    except:
        await ctx.send(embeds=interactions.Embed(title="__Commande de l'Aventure :__", description="Vous devez avoir commencé l'aventure pour utiliser cette commande.\n\nFaites donc un tour vers /start"),ephemeral=True)
        return 0
    
    if procuration != None:
        if int(procuration.id) in user.haveProcurOn:
            try:
                user = loadCharFile("./userProfile/{0}.json".format(int(procuration.id)))
            except:
                await ctx.send(embeds=Embed(title="Une erreur est survenue",description="Cet utilisateur n'a pas de personnage"),ephemeral=True)
                return 0
        else:
            await ctx.send(embeds=Embed(title="Une erreur est survenue",description="Vous n'avez pas procuration sur le personnage de cet utilisateur"),ephemeral=True)
            return 0

    await roulette(slash, ctx, user)

# -------------------------------------------- SEE ENEMY REPARTITION -------------------------------
@baseSee.subcommand(sub_cmd_name="enemy_repartition", sub_cmd_description="Permet de voir la répartition des ennemis")
async def seeEnnemyRep(ctx):
    # 0 : Dmg; 1 : Heal/Armor; 2 : Buff/Debuff
    octoRolesNPos = [[[], [], []], [[], [], []], [[], [], []]]
    dicidants = []

    for octa in tablUniqueEnnemies:
        if octa.aspiration in [BERSERK, POIDS_PLUME, MAGE, ENCHANTEUR, OBSERVATEUR, TETE_BRULEE, ATTENTIF, SORCELER]:
            roleId = 0
        elif octa.aspiration in [ALTRUISTE, PREVOYANT, VIGILANT, PROTECTEUR]:
            roleId = 1
        elif octa.aspiration in [IDOLE, INOVATEUR, MASCOTTE]:
            roleId = 2
        else:
            dicidants.append(octa)
            roleId = -1

        if roleId != -1:
            octoRolesNPos[roleId][octa.weapon.range].append(octa)

    for cmpt in (0, 1, 2):
        emb = interactions.Embed(title="__Ennemi répartion : {0}__".format(["DPT_PHYS", "Healer/Shilder", "Support"][cmpt]), color=light_blue)
        for cmptBis in range(len(octoRolesNPos[cmpt])):
            desc = ""
            for name in octoRolesNPos[cmpt][cmptBis]:
                desc += "{0} {1}\n".format(name.icon, name.name)
            if len(desc) > 0:
                emb.add_field(name=["__Mêlée :__", "__Distance :__","__Backline :__"][cmptBis], value=desc, inline=True)
            else:
                emb.add_field(name=["__Mêlée :__", "__Distance :__", "__Backline :__"][cmptBis], value="`-`", inline=True)

        if cmpt == 0:
            await ctx.send(embeds=emb)
        else:
            await ctx.channel.send(embeds=emb)

    desc = ''
    for name in dicidants:
        desc += "{0} {1}\n".format(name.icon, name.name)
    emb = interactions.Embed(title="__Hors catégorie :__".format(["DPT_PHYS", "Healer/Shilder", "Support"][cmpt]), color=light_blue, description=desc)

    await ctx.channel.send(embeds=emb)

@baseSee.subcommand(sub_cmd_name="enemy",sub_cmd_description="Permet d'afficher la page d'info d'un ennemi",options=[SlashCommandOption(type=OptionType.STRING,name="name",description="Le nom de l'ennemi",required=True)])
async def seeEnemy(ctx:SlashContext,name:str):
    await ctx.defer()
    badGuy = findEnnemi(name)
    emptyUser = char(owner=int(ctx.author.id))
    if badGuy != None:
        listOption = []
        for skilly in badGuy.skills:
            if type(skilly) == skill:
                listOption.append(StringSelectOption(label=skilly.name,value=skilly.id,emoji=getEmojiObject(skilly.emoji)))
        
        select = StringSelectMenu(listOption,custom_id="seeEnemySkill",placeholder="Voir une compétence en détail")
        emb = infoEnnemi(badGuy)
        msg = await ctx.send(embeds=emb,components=[select])

        while 1:
            try:
                rep = await slash.wait_for_component(components=select,messages=msg,timeout=180)
                rep: ComponentContext = rep.ctx
            except asyncio.TimeoutError:
                await msg.edit(embeds=emb,components=[])
                break

            await rep.defer()
            for skilly in badGuy.skills:
                if type(skilly) == skill and skilly.id == rep.values[0]:
                    await rep.send(embeds=infoSkill(skill=skilly,ctx=rep,user=emptyUser))

    else:
        await ctx.send(content="L'ennemi \"{0}\" n'a pas été trouvé".format(name))

# ------------------------------------------- PRESTIGE ---------------------------------------------
@slash_command(name="prestige", description="Permet de revenir au niveau 1, avec quelques bonus en primes")
async def prestigeCmd(ctx):
    if not(await botChannelVerif(slash, ctx)):
        return 0
    try:
        user = loadCharFile("./userProfile/{0}.json".format(ctx.author.id))
    except:
        await ctx.send("Vous n'avez même pas encore commencé l'aventure et vous voulez déjà prestige ?",ephemeral=True)
        return 0

    if user.level < MAXLEVEL:
        await ctx.send("Vous devez être niveau {0} pour pouvoir utiliser cette commande".format(MAXLEVEL),ephemeral=True)
        return 0

    emb = interactions.Embed(title="__Prestige__", color=light_blue,description="En prestigeant votre personnage, vous retournerez au niveau 1<:littleStar:925860806602682369>{0}.\n\nVous conserverez votre inventaire d'objet des de compétences et obtiendrez un __Point Majeur__.\nVous pourrez l'utiliser pour augmenter une de vos statistiques principales de 30 points supplémentaires, ou augmenter vos statistiques secondaires de 10 points".format(user.stars+1))
    comfirm = interactions.Button(style=ButtonStyle.SUCCESS, label="Prestige votre personnage", emoji='✅', custom_id='✅')

    msg = await ctx.send(embeds=emb, components=[interactions.ActionRow(comfirm)])

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
@slash_command(name="set_bot_channel", description="Permet de définir un salon comme salon bot", options=[SlashCommandOption(name="salon", description="Le salon dans lequel les utilisateurs pourront utiliser les commandes", type=7, required=True)])
async def setChannel(ctx: interactions.SlashContext, salon: interactions.BaseChannel):
    if not(ctx.author.guild_permissions.manage_channels):
        await ctx.send(embeds=interactions.Embed(title="__/set_bot_channel__", color=red, description="Tu as besoin des permissions de gérer les salons textuels pour utiliser cette commande, désolée"),ephemeral=True)
        return 0
    if type(salon) != interactions.BaseChannel:
        await ctx.send(embeds=interactions.Embed(title="__/set_bot_channel__", color=red, description="Seul un salon textuel peut être rajouté comme salon bot, désolée"),ephemeral=True)
        return 0

    globalVar.setGuildBotChannel(int                                                    (ctx.guild_id), salon.id)
    await ctx.send(embeds=interactions.Embed(title="__/set_bot_channel__", color=light_blue, description="Le salon {0} a bien été enregistré comme salon bot\nChaque serveur ne peut avoir qu'un seul salon bot, réutiliser la commande remplacera l'ancien".format(salon.mention)))

# ------------------------------------------- VERIF ------------------------------------------------
groupComVerif = baseAdmin.group(name="verif",description="Commandes qui vérifient des trucs")

@groupComVerif.subcommand(sub_cmd_name="user", sub_cmd_description="Permet de voir toutes les informations d'un personnage",options=[SlashCommandOption(name="identifiant", description="L'identifiant de l'utilisateur", type=OptionType.STRING, required=True)])
async def verifuser(ctx, identifiant):
    user = loadCharFile("./userProfile/{0}.json".format(identifiant))
    await ctx.send(embeds=await seeAllInfo(slash, user))

@groupComVerif.subcommand(sub_cmd_name="team")
async def verifTeams(ctx):
    toSend, allReadySeen, msg, userTeam = "", [], None, []

    def getUserMainTeam(user: char):
        for look in userTeam:
            if look[0] == user.owner:
                return int(look[1])

    for team in userTeamDb.getAllTeamIds():
        temp = ""
        if len(userTeamDb.getTeamMember(team)) == 0:
            userTeamDb.updateTeam(team)
            toSend += "\nL'équipe **{0}** a été supprimée\n".format(team)
            print("Equipe {0} supprimée".format(team))
        if team != 0:
            temp = "__Team **{0}** :__".format(team)
            teamMembers = userTeamDb.getTeamMember(team)

            tmpTeamMembers = teamMembers[:]
            for ids in teamMembers:
                user = loadCharFile(path="./userProfile/{0}.json".format(ids))
                if user.owner in allReadySeen:
                    warn = "~~"
                    if getUserMainTeam(user) != team:
                        try:
                            tmpTeamMembers.remove(user.owner)
                        except:
                            print_exc()
                else:
                    warn = ""
                    allReadySeen.append(user.owner)
                    userTeam.append([user.owner, team])

                if user.team != team and team != 0:
                    user.team = team
                    saveCharFile(user=user)
                    redacted = " 📎"
                else:
                    redacted = ""

                temp += "\n{2}{0} {1}{2}{3}".format(await getUserIcon(slash, user), user.name, warn, redacted)

            if len(tmpTeamMembers) > 0:
                userTeamDb.updateTeam(team, tmpTeamMembers)
            else:
                userTeamDb.updateTeam(team)
        elif team == 0:
            tmpTeamMembers = userTeamDb.getTeamMember(team)
            teamId = random.randint(1,maxsize)
            for cmpt in range(len(tmpTeamMembers)):
                user: char = loadCharFile(path="./userProfile/{0}.json".format(tmpTeamMembers[cmpt]))
                user.team = teamId
                saveCharFile(user=user)
                tmpTeamMembers[cmpt] = user
                allReadySeen.append(user.owner)

            userTeamDb.updateTeam(teamId, tmpTeamMembers)
            userTeamDb.updateTeam(team)
            toSend += "\nL'équipe **0** ({1} {2}) a été redéfinie en équipe **{0}**".format(teamId,await getUserIcon(slash,tmpTeamMembers[0]),tmpTeamMembers[0].name)

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

@groupComVerif.subcommand(sub_cmd_name="emoji")
async def emojiVerficition(ctx):
    await ctx.defer()
    await verifEmojis(ctx)

listMonth, thatMonth = ["Janvier","Février","Mars","Avril",'Mai',"Juin","Juillet","Aout","Septembre","Octobre","Novembre","Decembre"], dateNow.month-1
listOptions = []
for cmpt in range(len(listMonth)):
    listOptions.append(SlashCommandChoice(name=listMonth[cmpt],value=str(cmpt)))

@groupComVerif.subcommand(sub_cmd_name="shop_msg",options=[SlashCommandOption(type=OptionType.STRING,name="mois",description="Voir les messages de quel mois",choices=listOptions)])
async def shopMsgVerif(ctx:interactions.SlashContext,mois:Union[str,None]=None):
    await ctx.defer()
    if mois == None:
        mois = thatMonth
    elif type(mois) != int:
        mois = int(mois)
    for msg in shopMonthlyMsg[mois]:
        msgShop = formatShop(msg)
        lenMsgShop = len(msgShop)
        await ctx.channel.send(embeds=interactions.Embed(description=msgShop,color=[light_blue,red][lenMsgShop>4000],footer=EmbedFooter(text="{0}/4096".format(lenMsgShop))))
        await asyncio.sleep(0.3)
    await ctx.send("Tous les messages ont été envoyés")

@groupComVerif.subcommand(sub_cmd_name="empty_emoji_slots")
async def verifEmptyEmojiSlots(ctx:interactions.SlashContext):
    await ctx.defer()
    guildList:List[interactions.Guild] = slash.guilds
    dictEmptyGuilds = {}
    for temp in guildList:
        if temp.name.startswith("Lenapy"):
            emojiList = await temp.fetch_all_custom_emojis()
            lenEmoji = len(emojiList)
            if lenEmoji < 50:
                dictEmptyGuilds[temp.name] = 50-lenEmoji
    
    toReturn = ""
    for servName, emojiDiff in dictEmptyGuilds.items():
        toReturn += "{0} : **{1}** emplacement{2} disponible{2}\n".format(servName,emojiDiff,["","s"] [emojiDiff>1])
    await ctx.send(content=toReturn)

@groupComVerif.subcommand(sub_cmd_name="default_skill_icons")
async def verifDefaultSkillIcons(ctx):
    await ctx.defer()
    listSkills, msg = [], None
    for tmpSkill in skills:
        if tmpSkill.emoji in ["<:dUPM:943279319994728539>","<:dM:943275508492292138>","<:dUMM:943279280002060309>","<:dD:885899060488339456>","<:dUZ:943279239573143612>","<:dZ:943275494802079804>","<:dUMZ:943279254991409232>","<:dZ:943266058024943656>","<:defIndi:943266043558768640>","<:defUltHeal:943279333869486110>","<:defHeal:885899034563313684>","<:defHealZone:943266024155922433>","<:defSupp:885899082453880934>","<:defarmor:895446300848427049>","<:defMalus:895448159675904001>","<:renisurection:873723658315644938>"]:
            listSkills.append(reduceEmojiNames(str(tmpSkill)))
    
    tmp = ""
    for tmpStr in listSkills:
        if len(tmp+tmpStr) > EMBED_MAX_DESC_LENGTH:
            if msg == None:
                await ctx.send(embeds=Embed(description=tmp))
            else:
                await ctx.channel.send(embeds=Embed(description=tmp))
            tmp = tmpStr+"\n"
        else:
            tmp += tmpStr+"\n"

    if len(tmp) > 0:
        if msg == None:
            await ctx.send(embeds=Embed(description=tmp))
        else:
            await ctx.channel.send(embeds=Embed(description=tmp))
    else:
        await ctx.send("Toutes les compétences ont des emojis")



# ------------------------------------------ CHAR SETTINGS ----------------------------------------

# ------------------------------------------ STREAM ----------------------------------------
twitchAlert = SlashCommand(name="twitch",auto_defer=AutoDefer(enabled=True,time_until_defer=0))
@twitchAlert.subcommand(sub_cmd_name="alert",sub_cmd_description="Permet de gérer les alertes streams")
async def lenaTwitchAlerte(ctx):
    await streamSettingsFunction(slash,ctx.guild,ctx)

@slash_command(name="test", scopes=adminServ)
async def expeditionTest(ctx):
    user, chan = loadCharFile("./userProfile/{0}.json".format(ctx.author.id)), ctx.channel
    listEmbed = await generateExpeditionReport(slash, [user], user, datetime.now(parisTimeZone), ctx)
    for a in listEmbed:
        await chan.send(embeds=a)

@slash_command(name="test2", scopes=adminServ)
async def boosterTest(ctx):
    await chipShop(slash, ctx)

@slash_command(name="area_test",scopes=adminServ)
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

conflictingGuildsLenapy = [866363139931242506,866829835211636756]

@groupComVerif.subcommand(sub_cmd_name="guild",sub_cmd_description="Donne la liste des serveurs sur lequel le bot ne peut pas créer de commandes slash")
async def adminVerifGuild(ctx:interactions.SlashContext):
    try:
        await ctx.defer()
        listNonPerms = ""
        for serv in conflictingGuildsLenapy:
            try:
                serv: interactions.Guild = slash.get_guild(serv)
                owner: interactions.User = await slash.get_user(serv.owner_id)
                listNonPerms += "\n{0} ({1})".format(serv.name,owner.mention)
            except Exception as e:
                print(e)

        await ctx.send(embeds=interactions.Embed(title="__Liste des serveurs sur lesquel le bot ne peut pas créer de commandes__",description=listNonPerms,color=light_blue))
    except:
        await ctx.send(format_exc(limite=2000))

@baseAdmin.subcommand(sub_cmd_name="test_tread")
async def testTread(ctx: interactions.SlashContext):
    msg: interactions.Message = await ctx.send(embeds=interactions.Embed(title="Test"))
    treadChan: interactions.BaseChannel = await msg.create_thread("Test Message",invitable=False)
    await treadChan.add_member(ctx.author)
    await asyncio.sleep(3)
    await treadChan.delete()

###########################################################
# Démarrage du bot
if __name__ == "__main__":
    print(["\nKawiiiiii","\nIl semblerait que je sois seule cette fois. Je m'occuperais de Shushi une autre fois"][isLenapy])
    try:
        slash.start()
    except Exception as e:
        print("La connexion a écouché :")
        print(e)