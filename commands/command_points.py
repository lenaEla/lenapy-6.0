import discord,discord_slash, os

from discord_slash.utils.manage_components import *
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *

async def points(bot : discord.client, ctx : discord.message, args : [str]):
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile,ctx)
        msg = await loadingEmbed(ctx)
        if user.points > 0:
            def check(m):
                return m.author_id == ctx.author.id and int(m.origin_message.id) == int(msg.id)

            choiceStat = ["Force","Endurance","Charisme","Agilité","Précision","Intelligence"]
            tabl = [maxStrength,maxEndur,maxChar,maxAgi,maxPreci,maxIntel]
            temp = user.allStats()

            msgTemp = "\n"
            for a in range(0,len(choiceStat)):
                trueStat = round(tabl[a][user.aspiration]*0.1+tabl[a][user.aspiration]*0.9*50/user.level)
                dif = user.bonusPoints[a]
                msgTemp += f"{choiceStat[a]} : {str(temp[a])} *(+{str(dif)})*\n"

            select = create_select(
                options=[
                    create_select_option("Force","0"),
                    create_select_option("Endurance","1"),
                    create_select_option("Charisme","2"),
                    create_select_option("Agilité","3"),
                    create_select_option("Précision","4"),
                    create_select_option("Intelligence","5")
                ],
                placeholder="Dans quelle catégorie voulez-vous rajouter vos points ?"
            )

            await msg.edit(embed = discord.Embed(title = args[0],color = user.color,description = f"Vous avez {user.points} points à répartir.\nQuand quelle catégorie voulez vous les rajouter ?\n{msgTemp}\n(Vous ne pouvez placer que 30 points bonus par catégorie)"),components=[create_actionrow(select)])
            
            try:
                respond = await wait_for_component(bot,components=select,timeout=10,check=check)
            except:
                await msg.edit(embed = discord.Embed(title = args[0],color = user.color,description = f"Vous avez {user.points} points à répartir.\nQuand quelle catégorie voulez vous les rajouter ?\n{msgTemp}\n(Vous ne pouvez placer que 30 points bonus par catégorie)"),components=[timeoutSelect])
                return 0

            ballerine = respond
            respond = int(ballerine.values[0])
            temp = user.allStats()
            tabl = [maxStrength,maxEndur,maxChar,maxAgi,maxPreci,maxIntel]

            stat = temp[respond]
            trueStat = stat-user.bonusPoints[respond]
            dif = user.bonusPoints[respond]
            if dif < 30:
                def checkIsAuthor(message):
                    return int(message.channel.id) == int(babie.channel.id) and int(message.author.id) == int(ctx.author.id)

                babie = await ballerine.send(embed = discord.Embed(title = f"{args[0]} : {choiceStat[respond]}", color = user.color, description = f"__{choiceStat[respond]} :__ {trueStat} *+{dif}*\n\nCombien de points voulez vous rajouter ?\nPour rappel, vous avez {user.points} points bonus à votre disposition."))
                resp = await bot.wait_for("message",timeout=60,check=checkIsAuthor)
                repMsg = resp
                if not resp.content.isdigit():
                    await msg.edit(embed = errorEmbed(args[0],"La réponse donnée n'est pas un nombre"))
                else:
                    resp = int(resp.content)
                    if resp <= user.points and resp >= 0 and user.bonusPoints[respond]+resp <= 30:
                        temp[respond] = temp[respond]+resp
                        user.points -= resp
                        user.strength, user.endurance, user.charisma, user.agility, user.precision, user.intelligence = temp[0],temp[1],temp[2],temp[3],temp[4],temp[5]
                        user.bonusPoints[respond] += resp
                        await msg.edit(embed = discord.Embed(title = f"{args[0]} : {choiceStat[respond]}", color = user.color, description = "Vos points ont bien été attribué !"),components=[])
                        saveCharFile(pathUserProfile,user)

                    else:
                        await msg.edit(embed = errorEmbed(args[0],"Tu as donné un nombre non valide"))

                try:
                    await repMsg.delete()
                except:
                    pass

                await babie.delete()

            else:
                await msg.edit(embed = discord.Embed(title = f"{args[0]} : {choiceStat[respond]}", color = user.color, description = "Vous avez déjà attribué le maximum de points bonus possibles dans cette catégorie"))

        else:
            await msg.edit(embed = errorEmbed(args[0],"Tu n'as pas de points à répartir"))
