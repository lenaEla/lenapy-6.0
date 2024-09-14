import asyncio, os
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from typing import List

async def pointsCmd(bot: interactions.Client, ctx: interactions.SlashContext, procuration: interactions.Member = None, stat=None, points=None):
    mainUser, msg, babie = loadCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".json"), None, None
    if procuration != None:
        mainUser = loadCharFile(id=int(procuration.id))

    state = 0
    if stat != None and points == None:
        state = 1
    elif stat == None and points != None:
        await ctx.send("Vous devez spécifier une statistique si vous spécifiez un nombre de points",ephemeral=True)
        return 0
    elif stat != None and points != None:
        state = 2

    listUserProcure = [mainUser]
    for a in mainUser.haveProcurOn:
        listUserProcure.append(loadCharFile("./userProfile/{0}.json".format(a)))
    
    def userSortValue(user):
        if user.owner == mainUser.owner: return 2
        elif user.team == mainUser.team and user.team != 0: return 1
        else: return 0

    listUserProcure.sort(key=lambda ballerine: userSortValue(ballerine),reverse=True)

    if len(listUserProcure) > 24:
        listUserProcure = listUserProcure[:24]

    pathUserProfile = "./userProfile/{0}.json".format(int(mainUser.owner))

    if int(mainUser.owner) != int(ctx.author.id):
        if ctx.author.id not in mainUser.procuration:
            await ctx.send("{0} ne vous a pas donné procuration sur son inventaire".format(mainUser.name),ephemeral = True)
            return 0

    await ctx.defer()
    while 1:
        user = loadCharFile(pathUserProfile)
        if state == 0:
            if len(listUserProcure) > 0:
                procurOptions = []
                for a in listUserProcure:
                    procurOptions.append(interactions.StringSelectOption(label=a.name,value="user_{0}".format(a.owner),emoji=getEmojiObject(await getUserIcon(bot,a)),default=a.owner == user.owner,description=["{0} point{1} bonus restants".format(a.points,["","s"][a.points>1]),None][a.points==0]))
                procurSelect = [interactions.ActionRow(interactions.StringSelectMenu(procurOptions,custom_id = "procurSelect"))]
            else:
                procurSelect = []
            temp = user.allStats

            msgTemp = "\n"
            for a in range(0,len(nameStats)):
                dif = user.bonusPoints[a]
                msgTemp += "{4} __{0} :__ {1} *(+{2})*{3}\n".format(nameStats[a],temp[a]-dif,dif,[""," (+{0} <:littleStar:925860806602682369>)".format(user.majorPoints[a])][user.majorPoints[a]>0],statsEmojis[a])

            if user.stars > 0:
                msgTemp += "\n"
                for cmpt in range(RESISTANCE,CRITICAL+6):
                    msgTemp += "{3} __{0} :__ {1}{2}\n".format((nameStats2+["Soins","Boost","Armure","Direct","Indirect"])[cmpt-RESISTANCE],user.majorPoints[cmpt],[""," (<:littleStar:925860806602682369>)"][user.majorPoints[cmpt]>0],statsEmojis[cmpt])

            selectCatOptions = []
            for cmpt in range(MAGIE+1):
                selectCatOptions.append(interactions.StringSelectOption(label=nameStats[cmpt],value=str(cmpt),emoji=getEmojiObject(statsEmojis[cmpt])))

            select = interactions.StringSelectMenu(selectCatOptions,custom_id = "selectACat",
                placeholder=["Utiliser vos points bonus","Vous n'avez pas de points bonus à répartir"][user.points == 0],
                disabled=user.points == 0
            )

            selectCatOptions = []
            for cmpt in range(ACT_INDIRECT_FULL+1):
                selectCatOptions.append(interactions.StringSelectOption(label=allStatsNames[cmpt] + " (Majeur)",value=str(cmpt),emoji=getEmojiObject(statsEmojis[cmpt])))

            select2 = interactions.StringSelectMenu(selectCatOptions,custom_id = "selectACatMaj",
                placeholder=["Utiliser vos points majeurs","Vous n'avez pas de points majeurs à répartir"][user.majorPointsCount == 0],
                disabled=user.majorPointsCount == 0
            )
            emb = interactions.Embed(title = "__Stats__ :",color = user.color,description = f"Vous avez {user.points} points et {user.majorPointsCount} points majeurs à répartir.\nQuand quelle catégorie voulez vous les rajouter ?\n{msgTemp}\n(Vous ne pouvez placer que {MAXBONUSPERSTAT} points bonus par catégorie)")
            emb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(await getUserIcon(bot,user)).id))
            if msg == None:
                msg = await ctx.send(embeds = emb,components=procurSelect+[[interactions.ActionRow(select),interactions.ActionRow(select2)],[interactions.ActionRow(select)]][user.stars == 0])
            else:
                await msg.edit(embeds = emb,components=procurSelect+[[interactions.ActionRow(select),interactions.ActionRow(select2)],[interactions.ActionRow(select)]][user.stars == 0])

            try:
                respond = await bot.wait_for_component(msg,timeout=60,check=check)
                respond: ComponentContext = respond.ctx
            except:
                await msg.edit(embeds = emb,components=[])
                return 0

            ballerine = respond

            if ballerine.values[0].startswith('user_'):
                pathUserProfile = "./userProfile/{0}.json".format(respond.values[0].replace("user_",""))
            else:
                respond = int(ballerine.values[0])
                temp = user.allStats

                if ballerine.custom_id == "selectACat":
                    stat, state = respond, 1
                elif ballerine.custom_id == "selectACatMaj":
                    stat, state = respond, 3

        if state == 1:
            userStats = user.allStats
            trueStat = userStats[stat]-user.bonusPoints[stat]
            dif = user.bonusPoints[stat]
            def checkIsAuthor(message: interactions.Message):
                message: interactions.Message = message.message
                return int(message.channel.id) == int(ctx.channel.id) and int(message.author.id) == int(ctx.author.id)

            resp = None
            if babie == None:
                babie = await ballerine.send(embeds = interactions.Embed(title = f"__/stats__ : {nameStats[stat]}", color = user.color, description = f"__{nameStats[stat]} :__ {trueStat} *+{dif}*\n\nCombien de points voulez vous rajouter ?\nPour rappel, vous avez {user.points} points bonus à votre disposition."))
            else:
                await babie.edit(embeds = interactions.Embed(title = f"__/stats__ : {nameStats[stat]}", color = user.color, description = f"__{nameStats[stat]} :__ {trueStat} *+{dif}*\n\nCombien de points voulez vous rajouter ?\nPour rappel, vous avez {user.points} points bonus à votre disposition."))
            try:
                resp: interactions.Message = await bot.wait_for("on_message_create",timeout=60,checks=checkIsAuthor)
                resp: Message = resp.message
            except asyncio.TimeoutError:
                await babie.delete()
                babie, state = None, 0

            if resp != None:
                if not resp.content.isdigit():
                    await msg.edit("La réponse donnée n'est pas un nombre")
                else:
                    points, state = int(resp.content), 2

        if state == 2:
            userStats = user.allStats
            if points <= user.points and points >= 0 and user.bonusPoints[stat] <= MAXBONUSPERSTAT and user.bonusPoints[stat]+points <= MAXBONUSPERSTAT:
                userStats[stat] = userStats[stat]+points
                user.points -= points
                user.strength, user.endurance, user.charisma, user.agility, user.precision, user.intelligence, user.magie = userStats[0],userStats[1],userStats[2],userStats[3],userStats[4],userStats[5],userStats[6]
                user.bonusPoints[stat] += points
                saveCharFile(pathUserProfile,user)

                toRespondEmb = interactions.Embed(title = f"__stats__ : {nameStats[stat]}", color = user.color, description = "Vos points ont bien été attribué !\n\n{0} : {1} +{2} */{3}*".format(allStatsNames[stat],userStats[stat]-user.bonusPoints[stat],user.bonusPoints[stat],MAXBONUSPERSTAT))
                if not(ctx.responded):
                    await ctx.send(embeds = toRespondEmb)
                else:
                    if babie != None:
                        await babie.edit(embeds = toRespondEmb)
                    else:
                        await ctx.channel.send(embeds = toRespondEmb)
                if msg == None: return 1
                else: state = 0
            else:
                state = 0
                errorMsg = ""
                if points > user.points: errorMsg += "- Vous n'avez pas assez de points à attribuer (Vous avez {0} point{1})\n".format(user.points, ["","s"][user.points > 1])
                if user.bonusPoints[stat] >= MAXBONUSPERSTAT: errorMsg += "- Vous avez déjà attribué le maximum de points bonus dans cette catégorie\n"
                if user.bonusPoints[stat]+points >= MAXBONUSPERSTAT: errorMsg += "- Le nombre de points spécifié dépasse la limite maximum de points bonus dans une seule catégorie (Vous ne pouvez placer plus que {0} point{1} dans cette statistique)\n".format(MAXBONUSPERSTAT-user.bonusPoints[stat],["","s"][MAXBONUSPERSTAT-user.bonusPoints[stat]])

                if not(ctx.responded):
                    await ctx.send(embeds= interactions.Embed(title="__/stats__ :",color=red,description="Vos points n'ont pas été attribués :\n"+errorMsg))
                    if msg == None: return 0
                else:
                    if babie != None:
                        await babie.edit(embeds= interactions.Embed(title="__/stats__ :",color=red,description="Vos points n'ont pas été attribués :\n"+errorMsg))
                    else:
                        await ctx.channel.send(embeds= interactions.Embed(title="__/stats__ :",color=red,description="Vos points n'ont pas été attribués :\n"+errorMsg))

        if state == 3:
            dif = user.majorPoints[stat]
            if dif == 0:
                def check1(message):
                    message = message.ctx
                    return message.author.id == ctx.author.id

                conf = interactions.Button(style=ButtonStyle.SUCCESS,label="Utiliser votre point majeur",emoji=PartialEmoji(name='✅'),custom_id='✅')
                tmpEmb = interactions.Embed(title="__/points__ : {0}".format(allStatsNames[stat]),color=user.color,description="Voulez vous attribuer un point majeur en {0} pour obtenir __{1}__ points de statistiques ?".format(allStatsNames[stat],[10,MAJORBONUS][stat not in [RESISTANCE,PERCING,CRITICAL]]))
                
                if babie == None:
                    babie = await ballerine.send(embeds=tmpEmb,components=[interactions.ActionRow(conf)])
                else:
                    await babie.edit(embeds=tmpEmb,components=[interactions.ActionRow(conf)])
                try:
                    confirmAct = await bot.wait_for_component(babie,check=check1,timeout=60)
                    confirmAct = confirmAct.ctx
                except:
                    await babie.delete()
                    babie, state = None, 0

                if confirmAct.component.custom_id == '✅':
                    user.majorPoints[stat] += [10,MAJORBONUS][stat not in [RESISTANCE,PERCING,CRITICAL]]
                    user.majorPointsCount -= 1
                    saveCharFile(user=user)

                    toRespondEmb = interactions.Embed(title = f"__stats__ : {allStatsNames[stat]}", color = user.color, description = "Vos points ont bien été attribué !\n\n{0} : {1} +**{2}**/{3}".format(allStatsNames[stat],0,user.majorPoints[stat],[10,MAJORBONUS][stat not in [RESISTANCE,PERCING,CRITICAL]]))
                    if not(ctx.responded):
                        await ctx.send(embeds = toRespondEmb)
                    else:
                        if babie != None: await babie.edit(embeds = toRespondEmb,components=[])
                        else: await msg.reply(embeds = toRespondEmb)
                    state = 0
                else:
                    await babie.delete()
                    babie, state = None, 0

            else:
                state = 0
                errorMsg = ""
                if 1 > user.majorPointsCount:
                    errorMsg += "- Vous n'avez pas assez de points à attribuer (Vous avez {0} point{1})\n".format(user.majorPointsCount, ["","s"][user.majorPointsCount > 1])
                if 1 <= 0:
                    errorMsg += "- Vous le nombre de points à attribuer doit être supérieur à 0\n"
                if user.majorPoints[stat] > 0:
                    errorMsg += "- Vous avez déjà attribué le maximum de points bonus dans cette catégorie\n"

                if not(ctx.responded):
                    await ctx.send(embeds= interactions.Embed(title="__/stats__ :",color=red,description="Vos points n'ont pas été attribués :\n"+errorMsg))
                    return 0
                else:
                    if babie != None:
                        await babie.edit(embeds= interactions.Embed(title="__/stats__ :",color=red,description="Vos points n'ont pas été attribués :\n"+errorMsg))
                    else:
                        await msg.reply(embeds= interactions.Embed(title="__/stats__ :",color=red,description="Vos points n'ont pas été attribués :\n"+errorMsg))