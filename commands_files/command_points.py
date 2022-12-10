import asyncio, os
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from typing import List

async def points(bot : interactions.Client, ctx : interactions.CommandContext, args : List[str], procuration = None, slashed = True):
    mainUser = loadCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".prof")
    listUserProcure = [mainUser]
    for a in mainUser.haveProcurOn:
        listUserProcure.append(loadCharFile("./userProfile/{0}.prof".format(a)))

    mainUser2 = loadCharFile("./userProfile/{0}.prof".format(ctx.author.id))
    def userSortValue(user):
        if user.owner == mainUser2.owner:
            return 2
        elif user.team == mainUser2.team and user.team != 0:
            return 1
        else:
            return 0
    listUserProcure.sort(key=lambda ballerine: userSortValue(ballerine),reverse=True)

    if len(listUserProcure) > 24:
        listUserProcure = listUserProcure[:24]

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

    msg = None
    await ctx.defer()

    def check(m):
        return m.author.id == ctx.author.id

    while 1:
        user = loadCharFile(pathUserProfile)
        if len(listUserProcure) > 0:
            procurOptions = []
            for a in listUserProcure:
                procurOptions.append(interactions.SelectOption(label=a.name,value="user_{0}".format(a.owner),emoji=getEmojiObject(await getUserIcon(bot,a)),default=a.owner == user.owner,description=["{0} point{1} bonus restants".format(a.points,["","s"][a.points>1]),None][a.points==0]))
            procurSelect = [interactions.ActionRow(components=[interactions.SelectMenu(custom_id = "procurSelect", options=procurOptions)])]
        else:
            procurSelect = []
        temp = user.allStats()

        msgTemp = "\n"
        for a in range(0,len(nameStats)):
            dif = user.bonusPoints[a]
            msgTemp += "{4} __{0} :__ {1} *(+{2})*{3}\n".format(nameStats[a],temp[a]-dif,dif+user.majorPoints[a],[""," (<:littleStar:925860806602682369>)"][user.majorPoints[a]>0],statsEmojis[a])

        if user.stars > 0:
            msgTemp += "\n"
            for cmpt in range(RESISTANCE,CRITICAL+6):
                msgTemp += "{3} __{0} :__ {1}{2}\n".format((nameStats2+["Soins","Boost","Armure","Direct","Indirect"])[cmpt-RESISTANCE],user.majorPoints[cmpt],[""," (<:littleStar:925860806602682369>)"][user.majorPoints[cmpt]>0],statsEmojis[cmpt])

        selectCatOptions = []
        for cmpt in range(MAGIE+1):
            selectCatOptions.append(interactions.SelectOption(label=nameStats[cmpt],value=str(cmpt),emoji=getEmojiObject(statsEmojis[cmpt])))

        select = interactions.SelectMenu(custom_id = "selectACat", 
            options=selectCatOptions,
            placeholder=["Utiliser vos points bonus","Vous n'avez pas de points bonus à répartir"][user.points == 0],
            disabled=user.points == 0
        )

        selectCatOptions = []
        for cmpt in range(ACT_INDIRECT_FULL+1):
            selectCatOptions.append(interactions.SelectOption(label=allStatsNames[cmpt] + " (Majeur)",value=str(cmpt),emoji=getEmojiObject(statsEmojis[cmpt])))

        select2 = interactions.SelectMenu(custom_id = "selectACatMaj", 
            options=selectCatOptions,
            placeholder=["Utiliser vos points majeurs","Vous n'avez pas de points majeurs à répartir"][user.majorPointsCount == 0],
            disabled=user.majorPointsCount == 0
        )
        emb = interactions.Embed(title = args[0],color = user.color,description = f"Vous avez {user.points} points et {user.majorPointsCount} points majeurs à répartir.\nQuand quelle catégorie voulez vous les rajouter ?\n{msgTemp}\n(Vous ne pouvez placer que 30 points bonus par catégorie)")
        emb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(await getUserIcon(bot,user)).id))
        if msg == None:
            msg = await ctx.send(embeds = emb,components=procurSelect+[[interactions.ActionRow(components=[select]),interactions.ActionRow(components=[select2])],[interactions.ActionRow(components=[select])]][user.stars == 0])
        else:
            await msg.edit(embeds = emb,components=procurSelect+[[interactions.ActionRow(components=[select]),interactions.ActionRow(components=[select2])],[interactions.ActionRow(components=[select])]][user.stars == 0])

        try:
            respond = await bot.wait_for_component(msg,timeout=30,check=check)
        except:
            await msg.edit(embeds = emb,components=[])
            return 0

        ballerine = respond

        if ballerine.data.values[0].startswith('user_'):
            pathUserProfile = "./userProfile/{0}.prof".format(respond.data.values[0].replace("user_",""))
        else:
            respond = int(ballerine.data.values[0])
            temp = user.allStats()

            if ballerine.data.custom_id == "selectACat":
                stat = temp[respond]
                trueStat = stat-user.bonusPoints[respond]
                dif = user.bonusPoints[respond]
                if dif < 30:
                    def checkIsAuthor(message: interactions.Message):
                        return int(message.channel_id) == int(ctx.channel_id) and int(message.author.id) == int(ctx.author.id)

                    babie, resp = await ballerine.send(embeds = interactions.Embed(title = f"__/stats__ : {nameStats[respond]}", color = user.color, description = f"__{nameStats[respond]} :__ {trueStat} *+{dif}*\n\nCombien de points voulez vous rajouter ?\nPour rappel, vous avez {user.points} points bonus à votre disposition.")), None
                    try:
                        resp: interactions.Message = await bot.wait_for("on_message_create",timeout=60,check=checkIsAuthor)
                        resp = await get(bot, interactions.Message, object_id=int(resp.id), parent_id=int(resp.channel_id))
                    except asyncio.TimeoutError:
                        await babie.delete()

                    if resp != None:
                        repMsg = resp
                        print("Chocolatine :",resp.content,"\n")
                        if not resp.content.isdigit():
                            await msg.edit(embeds = errorEmbed(args[0],"La réponse donnée n'est pas un nombre"))
                        else:
                            resp = int(resp.content)
                            if resp <= user.points and resp >= 0 and user.bonusPoints[respond]+resp <= 30:
                                temp[respond] = temp[respond]+resp
                                user.points -= resp
                                user.strength, user.endurance, user.charisma, user.agility, user.precision, user.intelligence, user.magie = temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6]
                                user.bonusPoints[respond] += resp
                                await babie.edit(embeds = interactions.Embed(title = f"__/stats__ : {nameStats[respond]}", color = user.color, description = "Vos points ont bien été attribué !"),components=[])
                                saveCharFile(pathUserProfile,user)

                            else:
                                await babie.edit(embeds = errorEmbed(args[0],"Tu as donné un nombre non valide"))

                        try:
                            await repMsg.delete()
                        except:
                            pass

                        await asyncio.sleep(2)
                        await babie.delete()

                else:
                    await msg.edit(embeds = interactions.Embed(title = f"__/stats__ : {nameStats[respond]}", color = user.color, description = "Vous avez déjà attribué le maximum de points bonus possibles dans cette catégorie"))

            else:
                respond = respond-7
                dif = user.majorPoints[respond]
                if dif == 0:
                    def check1(message):
                        return message.author.id == int(ctx.author.id)

                    conf = interactions.Button(type=2, style=ButtonStyle.SUCCESS,label="Utiliser votre point majeur",emoji=Emoji(name='✅'),custom_id='✅')
                    await msg.edit(embeds=interactions.Embed(title="__/points__ : {0}".format((nameStats+nameStats2+["Soins","Boost","Armure","Direct","Indirect"])[respond]),color=user.color,description="Voulez vous attribuer un point majeur en {0} pour obtenir __{1}__ points de statistiques ?".format((nameStats+nameStats2+["Soins","Boost","Armure","Direct","Indirect"])[respond],[10,35][respond not in [RESISTANCE,PERCING,CRITICAL]])),components=[interactions.ActionRow(components=[conf])])
                    try:
                        await bot.wait_for_component(msg,check=check1,timeout=30)
                    except:
                        await msg.edit(embeds = interactions.Embed(title = "__/points__ : {0}".format((nameStats+nameStats2+["Soins","Boost","Armure","Direct","Indirect"])[respond]),color = user.color,description = f"Vous avez {user.points} points à répartir.\nQuand quelle catégorie voulez vous les rajouter ?\n{msgTemp}\n(Vous ne pouvez placer que 30 points bonus par catégorie)"),components=[])
                        return 0
                    
                    user.majorPoints[respond] += [10,35][respond not in [RESISTANCE,PERCING,CRITICAL]]
                    user.majorPointsCount -= 1
                    saveCharFile(user=user)
                else:
                    await msg.edit(embeds=interactions.Embed(title="__/points__ : {0}".format((nameStats+nameStats2+["Soins","Boost","Armure","Direct","Indirect"])[respond]),color=user.color,description="Vous avez déjà attribué un point majeur dans cette catégorie"),components=[])
                    await asyncio.sleep(2)
            for cmpt in range(len(listUserProcure)):
                if listUserProcure[cmpt].owner == user.owner:
                    listUserProcure[cmpt] = user
