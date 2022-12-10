import interactions
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from commands_files.alice_stats_endler import aliceStatsDb

aspiOp = []
for cmpt in range(len(inspi)-1):
    splited = chapter[2][cmpt+1][1].splitlines(False)
    aspiOp.append(interactions.SelectOption(label=inspi[cmpt],value=str(cmpt),emoji=getEmojiObject(aspiEmoji[cmpt]),description=splited[0]))

aspirationMenu = interactions.SelectMenu(custom_id = "aspiSelectMenu", 
    options=aspiOp,
    placeholder="Sélectionnez une aspiration pour avoir plus d'informations dessus"
    )

aspirationMenuD = interactions.SelectMenu(custom_id = "aspiSelectMenu2", 
    options=[
        interactions.SelectOption(label="Tu es pas sensé voir ça",value="0"),
        ],
    placeholder="Votre aspiration a bien été prise en compte",
    disabled=True
    )

optionIka, optionTako = [],[]
for a in range(0,len(colorChoice)):
    optionIka += [interactions.SelectOption(label=colorChoice[a],value=str(colorId[a]),emoji=getEmojiObject(EmIcon[1][a]))]
    optionTako += [interactions.SelectOption(label=colorChoice[a],value=str(colorId[a]),emoji=getEmojiObject(EmIcon[2][a]))]

async def chooseAspiration(bot : interactions.Client, msg : interactions.Message,ctx : interactions.Message,user : char):
    choosed = False
    while not(choosed):
        action = interactions.ActionRow(components=[aspirationMenu])
        await msg.remove_all_reactions()
        desc = "Le moment est venu de selectionnez l'aspiration de votre personnage.\n\nRéagissez aux emojis ci-dessus pour avoir plus d'informations sur les {0} aspirations qui sont :".format(len(inspi)-1)
        for cmpt in range(len(inspi)-1):
            desc += "\n"+aspiEmoji[cmpt]+ " "+inspi[cmpt]
        await msg.edit(embeds = interactions.Embed(title = "__Changement d'Aspiration__" + " : Aspiration",color = user.color,description = desc),components = [action])

        def check(m):
            return m.author.id == ctx.author.id and m.message.id == msg.id

        haveReaction = False
        try:
            respond = await bot.wait_for_component(components=aspirationMenu, check=check,timeout=60)
            haveReaction = True
        except:
            pass

        if haveReaction:
            action = interactions.ActionRow(components=[aspirationMenuD])
            inspiDesc = []
            for cmpt in range(1,len(chapter[2])):
                inspiDesc.append(chapter[2][cmpt][1])

            msg2 = await respond.send(embeds = interactions.Embed(title = "__Changement d'Aspiration__ {0})".format(inspi[int(respond.data.values[0])]), color = user.color, description = f"{inspiDesc[int(respond.data.values[0])]}\n\nPour choisir cette aspiration, cochez le check-ci dessous"))

            await msg2.add_reaction("◀️")
            await msg2.add_reaction("✅")
            def checkIsAuthorReact(reaction,user):
                return user == ctx.author and int(reaction.message.id) == int(msg2.id)

            try:
                respondEmoji = await bot.wait_for("reaction_add",timeout = 60,check=checkIsAuthorReact)
                if str(respondEmoji[0]) == "✅":
                    await msg2.delete()
                    return int(respond.data.values[0])
                else:
                    await msg2.delete()
            except:
                await msg2.delete()
        else:
            await msg.remove_all_reactions()
            return None

async def chooseName(bot : interactions.Client, msg : interactions.Message, ctx: interactions.Message,user : char):
    """Selection du nom du personnage\n
    Renvoie User avec le nouveau si réussite, False sinon"""
    await msg.edit(embeds = interactions.Embed(title = "__Changement de Nom__" + " : Nom",color = light_blue,description = f"Ecrivez le nom de votre personnage :\n\nIl sera possible de modifier le nom de votre personnage en utilisant un objet spécial"))
    haveName = False
    def checkIsAuthor(message):
        return int(ctx.author.id) == int(message.author.id)
    try:
        respond = await bot.wait_for("on_message_create",timeout = 60,check = checkIsAuthor)
        user.name = respond.content
        haveName = True
    except:
        await msg.edit(embeds = errorEmbed("__Changement de Nom__","Timeout, commande annulée"))    

    if haveName:
        try:
            await respond.delete()
        except:
            pass
        return user
    else:
        return False

async def chooseColor(bot : interactions.Client, msg : interactions.Message,ctx : interactions.Message, user : char):
    ballerine = ""
    for a in range(0,len(colorChoice)):
        ballerine += f"{EmIcon[user.species][a]} - {colorChoice[a]}\n"
    babie = []
    if user.customColor:
        ballerine += "<:cutybat:884899538685530163> - Couleur personnalisé ("+hex(user.color)+")\n"
        babie = [interactions.SelectOption(label="Couleur personnalisée",value="Custom",description=hex(user.color),emoji=getEmojiObject("<:cutybat:884899538685530163>"))]

    options = [optionIka,optionTako][user.species-1] + babie
    colorMenuIka = interactions.SelectMenu(custom_id = "colorMenuIka", options=options, placeholder="Selectionnez votre couleur",)
    colorMenuTako = interactions.SelectMenu(custom_id = "colorMenuTako", options=options, placeholder="Selectionnez votre couleur",)

    if user.species == 1:
        action = interactions.ActionRow(components=[colorMenuIka])
    elif user.species == 2:
        action = interactions.ActionRow(components=[colorMenuTako])

    await msg.edit(embeds = interactions.Embed(title = "__Changement de Couleur__" + " : Couleur",color = light_blue,description = f"Sélectionnez la couleur de votre personnage :\n{ballerine}\nLa couleur sera affiché sur tous les embeds et l'icone de votre personnage."),components=[action])

    def check(m):
        return m.author.id == ctx.author.id and m.message.id == msg.id

    haveReaction = False
    try:
        respond = await bot.wait_for_component(components=action, check=check,timeout=60)
        haveReaction = True
    except:
        await msg.remove_all_reactions()

    if haveReaction == True:
        if respond.data.values[0] != "Custom":
            user.color = int(respond.data.values[0])
            user.customColor = False
        msgColor = await respond.send("Votre couleur a bien été sélectionée")
        await asyncio.sleep(2)
        await msgColor.delete()
        return user
    else:
        return False

async def changeCustomColor(bot,msg,ctx,user : char):
    def check(param):
        return param.author.id == ctx.author.id and param.channel_id == ctx.channel_id
    def checkReact(param,second):
        return second.id == ctx.author.id and param.message.id == msg.id and (str(param) in ["❌","✅"])
    while 1:
        await msg.remove_all_reactions()
        await msg.edit(embeds = interactions.Embed(title="Couleur personnalisée",description="Veillez entrer le code hexadecimal de votre nouvelle couleur :\n\nExemples :\n94d4e4\n#94d4e4",color = user.color))
        
        respond = await bot.wait_for("on_message_create",check=check,timeout=60)
        tempColor = respond.content
        color = int(respond.content,16)

        try:
            await respond.delete()
        except:
            pass

        if color == None:
            await msg.edit(embeds = errorEmbed("__Couleur personnalisée__","Le code donné n'est pas un code hexadecimal valide"))
            break

        await msg.edit(embeds = interactions.Embed(title = "Couleur personnalisée",description="Est-ce que cette couleur vous va ?",color = color))
        await msg.add_reaction("❌")
        await msg.add_reaction("✅")
        try:
            react = await bot.wait_for("reaction_add",check=checkReact,timeout=60)
        except:
            await msg.remove_all_reactions()
            break
        if str(react[0]) == "✅":
            user.color = color
            user.customColor = True
            user.colorHex = "0x"+tempColor.replace("0x","").replace("#","")
            return user

    return None

async def start(bot : interactions.Client, ctx : interactions.Message):
    """Commande de création de personnage"""
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"

    if not os.path.exists(pathUserProfile):

        still = True
        user = char(ctx.author.id)
        msg = await loadingSlashEmbed(ctx)

        user = await chooseName(bot,msg,ctx,user)

        if user == False:
            still = False
        
        if still: #Espèce
            await msg.edit(embeds = interactions.Embed(title = "__/start__" + " : Espèce",color = light_blue,description = f"Sélectionnez l'espèce de votre personnage :\n\n<:ikaLBlue:866459302319226910> Inkling\n<:takoLBlue:866459095875190804> Octaling\n\nL'espèce n'a aucune influence sur les statistiques du personnage."))
            await msg.add_reaction('<:ikaLBlue:866459302319226910>')
            await msg.add_reaction('<:takoLBlue:866459095875190804>')

            def checkIsAuthorReact1(reaction,user):
                return int(user.id) == int(ctx.author.id) and int(reaction.message.id) == int(msg.id) and (str(reaction)=='<:ikaLBlue:866459302319226910>' or str(reaction) == '<:takoLBlue:866459095875190804>')

            respond = await bot.wait_for("reaction_add",timeout = 60,check = checkIsAuthorReact1)

            if str(respond[0]) == '<:ikaLBlue:866459302319226910>':
                user.species = 1
            else:
                user.species = 2
        
        if still: #Genre
            await msg.remove_all_reactions()
            await msg.edit(embeds = interactions.Embed(title = "__/start__" + " : Genre",color = light_blue,description = f"Renseignez (ou non) le genre personnage :\nLe genre du personnage n'a aucune incidences sur ses statistiques\n"))
            await msg.add_reaction('♂️')
            await msg.add_reaction('♀️')
            await msg.add_reaction("▶️")
            def checkIsAuthorReact(reaction,user):
                return int(user.id) == int(ctx.author.id) and int(reaction.message.id) == int(msg.id) and (str(reaction)=='♀️' or str(reaction) == '♂️' or str(reaction) =="▶️")

            respond = await bot.wait_for("reaction_add",timeout = 60,check = checkIsAuthorReact)
            testouille,titouille = [GENDER_MALE,GENDER_FEMALE,GENDER_OTHER],['♂️','♀️',"▶️"]
            for a in range(0,len(titouille)):
                if str(respond[0]) == titouille[a]:
                    user.gender = testouille[a]

        if still: #Couleur
            await msg.remove_all_reactions()
            user = await chooseColor(bot,msg,ctx,user)

            if user == False:
                still=False

        if still: #Aspiration
            user.aspiration = await chooseAspiration(bot,msg,ctx,user)
            if user.aspiration != None:
                user = restats(user)

                existFile(pathUserProfile)
                await msg.remove_all_reactions()
                if saveCharFile(pathUserProfile,user):
                    await msg.delete()
                    aliceStatsDb.addUser(user)
                    await ctx.channel.send(embeds = interactions.Embed(title = "__/start__", color= user.color, description = f"Tout a bien été enregistré !\nN'hésite pas à utiliser la commande /help pour connaître les commandes de l'Aventure\nOu bien juste lire le manuel avec /manuel"))
                else:
                    await msg.delete()
                    await ctx.channel.send(embeds = interactions.Embed(title = "__/start__", color= red, description = "Un truc c'est mal passé, l'aventure attendra"))
                    os.remove(pathUserProfile)
            else:
                still = False

        if not(still):
            await msg.edit(embeds= errorEmbed("__/start__","Commande annulée (timeout)"))
    else:
        await ctx.channel.send(embeds=errorEmbed("__/start__","Vous avez déjà commencé l'aventure"))
