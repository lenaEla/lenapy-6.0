import asyncio
import discord, os

from discord_slash.utils.manage_components import *
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from typing import List

async def points(bot : discord.client, ctx : discord.message, args : List[str], procuration = None, slashed = False):
    listUserProcure = []
    mainUser = loadCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof")
    if mainUser.team != 0:
        file = readSaveFiles("./userTeams/{0}.team".format(mainUser.team))
        for a in file[0]:
            temp = loadCharFile("./userProfile/" + a + ".prof")
            if ctx.author_id in temp.procuration:
                listUserProcure.append(temp)

    if procuration == None:
        pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    else:
        pathUserProfile = absPath + "/userProfile/" + str(procuration.id) + ".prof"
    
    if not(os.path.exists(pathUserProfile)):
        await ctx.send("Vous n'avez pas commencé l'aventure",delete_after=15)
        return 0

    user = loadCharFile(pathUserProfile)

    if int(user.owner) != int(ctx.author.id):
        if ctx.author.id not in user.procuration:
            await ctx.send("{0} ne vous a pas donné procuration sur son inventaire".format(user.name),delete_after=15)
            return 0

    if slashed :
        msg = await loadingSlashEmbed(ctx)
    else:
        msg = await loadingEmbed(ctx)

    def check(m):
        return m.author_id == ctx.author.id

    while 1:
        user = loadCharFile(pathUserProfile)
        if len(listUserProcure) > 0:
            procurOptions = []
            for a in listUserProcure:
                procurOptions.append(create_select_option(a.name,"user_{0}".format(a.owner),getEmojiObject(await getUserIcon(bot,a)),default=a.owner == user.owner,description=["{0} point{1} bonus restants".format(a.points,["","s"][a.points>1]),None][a.points==0]))
            procurSelect = [create_actionrow(create_select(procurOptions))]
        else:
            procurSelect = []
        temp = user.allStats()

        msgTemp = "\n"
        for a in range(0,len(nameStats)):
            dif = user.bonusPoints[a]
            msgTemp += "__{0} :__ {1} *(+{2})*{3}\n".format(nameStats[a],temp[a]-dif,dif+user.majorPoints[a],[""," (<:littleStar:925860806602682369>)"][user.majorPoints[a]>0])

        if user.stars > 0:
            msgTemp += "\n"
            for cmpt in range(RESISTANCE,CRITICAL+6):
                msgTemp += "__{0} :__ {1}{2}\n".format((nameStats2+["Soins","Boost","Armure","Direct","Indirect"])[cmpt-RESISTANCE],user.majorPoints[cmpt],[""," (<:littleStar:925860806602682369>)"][user.majorPoints[cmpt]>0])


        if user.stars:
            pass

        select = create_select(
            options=[
                create_select_option("Force","0"),
                create_select_option("Endurance","1"),
                create_select_option("Charisme","2"),
                create_select_option("Agilité","3"),
                create_select_option("Précision","4"),
                create_select_option("Intelligence","5"),
                create_select_option("Magie","6")
            ],
            placeholder=["Utiliser vos points bonus","Vous n'avez pas de points bonus à répartir"][user.points == 0],
            disabled=user.points == 0
        )
        select2 = create_select(
            options=[
                create_select_option("Force","7"),
                create_select_option("Endurance","8"),
                create_select_option("Charisme","9"),
                create_select_option("Agilité","10"),
                create_select_option("Précision","11"),
                create_select_option("Intelligence","12"),
                create_select_option("Magie","13"),
                create_select_option("Résistance","14"),
                create_select_option("Pénétration","15"),
                create_select_option("Critique",'16'),
                create_select_option("Soins",'17'),
                create_select_option("Boost",'18'),
                create_select_option("Armures",'19'),
                create_select_option("Direct","20"),
                create_select_option("Indirect","21")
            ],
            placeholder=["Utiliser vos points majeurs","Vous n'avez pas de points majeurs à répartir"][user.majorPointsCount == 0],
            disabled=user.majorPointsCount == 0
        )
        await msg.edit(embed = discord.Embed(title = args[0],color = user.color,description = f"Vous avez {user.points} points et {user.majorPointsCount} points majeurs à répartir.\nQuand quelle catégorie voulez vous les rajouter ?\n{msgTemp}\n(Vous ne pouvez placer que 30 points bonus par catégorie)").set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(await getUserIcon(bot,user))["id"])),components=procurSelect+[[create_actionrow(select),create_actionrow(select2)],[create_actionrow(select)]][user.stars == 0])
        
        try:
            respond = await wait_for_component(bot,msg,timeout=30,check=check)
        except:
            await msg.edit(embed = discord.Embed(title = args[0],color = user.color,description = msgTemp).set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(await getUserIcon(bot,user))["id"])),components=[])
            return 0

        ballerine = respond

        if ballerine.values[0].startswith('user_'):
            pathUserProfile = "./userProfile/{0}.prof".format(respond.values[0].replace("user_",""))
        else:
            respond = int(ballerine.values[0])
            temp = user.allStats()

            if respond <= 6:
                stat = temp[respond]
                trueStat = stat-user.bonusPoints[respond]
                dif = user.bonusPoints[respond]
                if dif < 30:
                    def checkIsAuthor(message):
                        return int(message.channel.id) == int(babie.channel.id) and int(message.author.id) == int(ctx.author.id)

                    babie = await ballerine.send(embed = discord.Embed(title = f"__/stats__ : {nameStats[respond]}", color = user.color, description = f"__{nameStats[respond]} :__ {trueStat} *+{dif}*\n\nCombien de points voulez vous rajouter ?\nPour rappel, vous avez {user.points} points bonus à votre disposition."))
                    resp = await bot.wait_for("message",timeout=60,check=checkIsAuthor)
                    repMsg = resp
                    if not resp.content.isdigit():
                        await msg.edit(embed = errorEmbed(args[0],"La réponse donnée n'est pas un nombre"))
                    else:
                        resp = int(resp.content)
                        if resp <= user.points and resp >= 0 and user.bonusPoints[respond]+resp <= 30:
                            temp[respond] = temp[respond]+resp
                            user.points -= resp
                            user.strength, user.endurance, user.charisma, user.agility, user.precision, user.intelligence, user.magie = temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6]
                            user.bonusPoints[respond] += resp
                            await babie.edit(embed = discord.Embed(title = f"__/stats__ : {nameStats[respond]}", color = user.color, description = "Vos points ont bien été attribué !"),components=[])
                            saveCharFile(pathUserProfile,user)

                        else:
                            await babie.edit(embed = errorEmbed(args[0],"Tu as donné un nombre non valide"))

                    try:
                        await repMsg.delete()
                    except:
                        pass

                    await asyncio.sleep(2)
                    await babie.delete()
                
                else:
                    await msg.edit(embed = discord.Embed(title = f"__/stats__ : {nameStats[respond]}", color = user.color, description = "Vous avez déjà attribué le maximum de points bonus possibles dans cette catégorie"))

            else:
                respond = respond-7
                dif = user.majorPoints[respond]
                if dif == 0:
                    def check1(message):
                        return message.author_id == int(ctx.author.id)

                    conf = create_button(ButtonStyle.green,"Utiliser votre point majeur",'✅','✅')
                    await msg.edit(embed=discord.Embed(title="__/points__ : {0}".format((nameStats+nameStats2+["Soins","Boost","Armure","Direct","Indirect"])[respond]),color=user.color,description="Voulez vous attribuer un point majeur en {0} pour obtenir __{1}__ points de statistiques ?".format((nameStats+nameStats2+["Soins","Boost","Armure","Direct","Indirect"])[respond],[10,35][respond not in [RESISTANCE,PERCING,CRITICAL]])),components=[create_actionrow(conf)])
                    try:
                        await wait_for_component(bot,msg,check=check1,timeout=30)
                    except:
                        await msg.edit(embed = discord.Embed(title = "__/points__ : {0}".format((nameStats+nameStats2+["Soins","Boost","Armure","Direct","Indirect"])[respond]),color = user.color,description = f"Vous avez {user.points} points à répartir.\nQuand quelle catégorie voulez vous les rajouter ?\n{msgTemp}\n(Vous ne pouvez placer que 30 points bonus par catégorie)"),components=[])
                        return 0
                    
                    user.majorPoints[respond] += [10,35][respond not in [RESISTANCE,PERCING,CRITICAL]]
                    user.majorPointsCount -= 1
                    saveCharFile(user=user)
                else:
                    await msg.edit(embed=discord.Embed(title="__/points__ : {0}".format((nameStats+nameStats2+["Soins","Boost","Armure","Direct","Indirect"])[respond]),color=user.color,description="Vous avez déjà attribué un point majeur dans cette catégorie"),components=[])
                    await asyncio.sleep(2)
            for cmpt in range(len(listUserProcure)):
                if listUserProcure[cmpt].owner == user.owner:
                    listUserProcure[cmpt] = user