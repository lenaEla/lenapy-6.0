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
    desc = splited[0]
    for em in statsEmojis[:ACT_INDIRECT_FULL+1]:
        desc = desc.replace(em,"")
    aspiOp.append(interactions.StringSelectOption(label=inspi[cmpt],value=str(cmpt),emoji=getEmojiObject(aspiEmoji[cmpt]),description=desc))

aspirationMenu = interactions.StringSelectMenu(aspiOp, custom_id = "aspiSelectMenu", placeholder="Sélectionnez une aspiration pour avoir plus d'informations dessus")

aspirationMenuD = interactions.StringSelectMenu(interactions.StringSelectOption(label="Tu es pas sensé voir ça",value="0"),custom_id = "aspiSelectMenu2",placeholder="Votre aspiration a bien été prise en compte",disabled=True)

optionIka, optionTako = [],[]
for a in range(0,len(colorChoice)):
    optionIka += [interactions.StringSelectOption(label=colorChoice[a],value=str(colorId[a]),emoji=getEmojiObject(EmIcon[1][a]))]
    optionTako += [interactions.StringSelectOption(label=colorChoice[a],value=str(colorId[a]),emoji=getEmojiObject(EmIcon[2][a]))]

async def chooseAspiration(bot : interactions.Client, msg : interactions.Message, ctx : interactions.SlashContext,user : char):
    choosed = False
    while not(choosed):
        action = interactions.ActionRow(aspirationMenu)
        desc = "Le moment est venu de selectionnez l'aspiration de votre personnage.\n\nRéagissez aux emojis ci-dessus pour avoir plus d'informations sur les {0} aspirations qui sont :".format(len(inspi)-1)
        for cmpt in range(len(inspi)-1):
            desc += "\n"+aspiEmoji[cmpt]+ " "+inspi[cmpt]
        await msg.edit(embeds = interactions.Embed(title = "__Changement d'Aspiration__" + " : Aspiration",color = user.color,description = desc),components = [action])

        def check(m):
            m = m.ctx
            return m.author.id == ctx.author.id

        haveReaction = False
        try:
            respond = await bot.wait_for_component(components=aspirationMenu, check=check,timeout=60)
            respond: ComponentContext = respond.ctx
            haveReaction = True
        except asyncio.TimeoutError:
            pass

        if haveReaction:
            action = interactions.ActionRow(aspirationMenuD)
            inspiDesc = []
            for cmpt in range(1,len(chapter[2])):
                inspiDesc.append(chapter[2][cmpt][1])

            msg2Components = ActionRow(
                Button(style=ButtonStyle.SECONDARY,label="Retour",emoji=getEmojiObject("◀️"),custom_id="return"),
                Button(style=ButtonStyle.SUCCESS,label="Choisir cette aspiration",emoji=getEmojiObject("✅"),custom_id="select")
            )
            msg2 = await respond.send(embeds = interactions.Embed(title = "__Changement d'Aspiration__ {0})".format(inspi[int(respond.values[0])]), color = user.color, description = f"{inspiDesc[int(respond.values[0])]}\n\nPour choisir cette aspiration, cochez le check-ci dessous"),components=msg2Components)

            def checkIsAuthorReact(reaction):
                reaction = reaction.ctx
                return reaction.author.id == ctx.author.id

            try:
                respondEmoji = await bot.wait_for_component(messages=msg2,timeout = 60,check=checkIsAuthorReact)
                respondEmoji: ComponentContext = respondEmoji.ctx
                if respondEmoji.custom_id == "select":
                    await msg2.delete()
                    return int(respond.values[0])
                else:
                    await msg2.delete()
            except asyncio.TimeoutError:
                await msg2.delete()
        else:
            return None

async def chooseName(bot : interactions.Client, msg : interactions.Message, ctx: interactions.Message,user : char):
    """Selection du nom du personnage\n
    Renvoie User avec le nouveau si réussite, False sinon"""
    await msg.edit(embeds = interactions.Embed(title = "__Changement de Nom__" + " : Nom",color = light_blue,description = f"Ecrivez le nom de votre personnage :\n\nIl sera possible de modifier le nom de votre personnage en utilisant un objet spécial"))
    haveName = False
    def checkIsAuthor(message):
        return int(ctx.author.id) == int(message.message.author.id)
    try:
        respond = await bot.wait_for("on_message_create",timeout = 60,checks = checkIsAuthor)
        respond: Message = respond.message
        user.name = respond.content
        haveName = True
    except:
        print_exc()
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
        babie = [interactions.StringSelectOption(label="Couleur personnalisée",value="Custom",description=hex(user.color),emoji=getEmojiObject("<:cutybat:884899538685530163>"))]

    options = [optionIka,optionTako][user.species-1] + babie
    colorMenuIka = interactions.StringSelectMenu(options,custom_id = "colorMenuIka", placeholder="Selectionnez votre couleur",)
    colorMenuTako = interactions.StringSelectMenu(options,custom_id = "colorMenuTako", placeholder="Selectionnez votre couleur",)
    action = interactions.ActionRow([colorMenuIka,colorMenuTako][user.species-1])

    await msg.edit(embeds = interactions.Embed(title = "__Changement de Couleur__" + " : Couleur",color = light_blue,description = f"Sélectionnez la couleur de votre personnage :\n{ballerine}\nLa couleur sera affiché sur tous les embeds et l'icone de votre personnage."),components=[action])

    def check(m):
        m = m.ctx
        return m.author.id == ctx.author.id and m.message.id == msg.id

    haveReaction = False
    try:
        respond = await bot.wait_for_component(components=action, check=check,timeout=60)
        respond: ComponentContext = respond.ctx
        haveReaction = True
    except:
        await msg.clear_all_reactions()

    if haveReaction == True:
        if respond.values[0] != "Custom":
            user.color = int(respond.values[0])
            user.customColor = False
        msgColor = await respond.send("Votre couleur a bien été sélectionée")
        await asyncio.sleep(2)
        await msgColor.delete()
        return user
    else:
        return False

async def changeCustomColor(bot: Client, msg: Message, ctx : SlashContext, user : char):
    def check(param: Message):
        param = param.message
        return param.author.id == ctx.author.id and param.channel.id == ctx.channel_id

    def checkReact(param: ComponentContext):
        param = param.ctx
        return param.author.id == ctx.author.id

    while 1:
        await msg.edit(embeds = interactions.Embed(title="Couleur personnalisée",description="Veillez entrer le code hexadecimal de votre nouvelle couleur :\n\nExemples :\n94d4e4\n#94d4e4",color = user.color),components=[])
        
        respond = await bot.wait_for("on_message_create",checks=check,timeout=60)
        respond: Message = respond.message
        tempColor = respond.content
        color = int(respond.content,16)

        try:
            await respond.delete()
        except:
            pass

        if color == None:
            await msg.edit(embeds = errorEmbed("__Couleur personnalisée__","Le code donné n'est pas un code hexadecimal valide"))
            break

        msgComponents = ActionRow(
            Button(style=ButtonStyle.SECONDARY,label="Retour",emoji=getEmojiObject("❌"),custom_id="Return"),
            Button(style=ButtonStyle.SUCCESS,label="Valider",emoji=getEmojiObject("✅"),custom_id="Success")
        )

        await msg.edit(embeds = interactions.Embed(title = "Couleur personnalisée",description="Est-ce que cette couleur vous va ?",color = color),components=msgComponents)
        
        try:
            react = await bot.wait_for_component(components=msgComponents,messages=msg,check=checkReact,timeout=60)
            react: ComponentContext = react.ctx
        except asyncio.TimeoutError:
            await msg.edit(embeds = interactions.Embed(title = "Commande annulée (timeout)",color = color),components=[])
            break
        except:
            await msg.edit(embeds = interactions.Embed(title = "Une erreur est survenue\n",description=format_exc(),color = color),components=[])
            print_exc()
            break
        if react.custom_id == "Success":
            user.color = color
            user.customColor = True
            user.colorHex = "0x"+tempColor.replace("0x","").replace("#","")
            return user

    return None

async def start(bot : interactions.Client, ctx : interactions.SlashContext):
    """Commande de création de personnage"""
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    isEmpty = False
    try:
        isEmpty = open(pathUserProfile)
        isEmptyLines = isEmpty.readlines()
        if len(isEmptyLines)<=1:
            isEmpty.close()
            isEmpty = True
        else:
            isEmpty.close()
            isEmpty = False
    except:
        try:
            isEmpty.close()
        except:
            pass
        isEmpty = False

    if not os.path.exists(pathUserProfile) or isEmpty:
        still = True
        user = char(ctx.author.id)
        msg = await loadingSlashEmbed(ctx)

        user = await chooseName(bot,msg,ctx,user)

        if user == False:
            still = False

        if still: #Espèce
            msgComponents = ActionRow(
                Button(style=ButtonStyle.PRIMARY,label="Inkling",emoji=getEmojiObject('<:ikaLBlue:866459302319226910>'),custom_id="inkling"),
                Button(style=ButtonStyle.PRIMARY,label="Octaling",emoji=getEmojiObject('<:takoLBlue:866459095875190804>'),custom_id="octaling")
            )
            await msg.edit(embeds = interactions.Embed(title = "__/start__" + " : Espèce",color = light_blue,description = f"Sélectionnez l'espèce de votre personnage :\n\n<:ikaLBlue:866459302319226910> Inkling\n<:takoLBlue:866459095875190804> Octaling\n\nL'espèce n'a aucune influence sur les statistiques du personnage, et il vous sera possible de modifier la forme de votre personnage avec des objets spéciaux"),components=[msgComponents])

            def checkIsAuthorReact1(reaction):
                reaction = reaction.ctx
                return reaction.author.id == ctx.author.id

            try:
                respond = await bot.wait_for_component(messages=msg ,timeout = 60, check = checkIsAuthorReact1)
                respond: ComponentContext = respond.ctx
                if respond.custom_id == 'inkling':
                    user.species = 1
                else:
                    user.species = 2
            except asyncio.TimeoutError :
                print_exc()
                await msg.edit(embeds = interactions.Embed(title = "Commande annulée (Timeout)"),components=MISSING)
                still = False

        if still: #Genre
            components = interactions.ActionRow(
                interactions.Button(style=ButtonStyle.PRIMARY,label="Masculin",emoji=getEmojiObject('♂️'),custom_id="male"),
                interactions.Button(style=ButtonStyle.PRIMARY,label="Féminin",emoji=getEmojiObject('♀️'),custom_id="female"),
                interactions.Button(style=ButtonStyle.PRIMARY,label="Autre / Passer",emoji=getEmojiObject("▶️"),custom_id="other")
            )
            await msg.edit(embeds = interactions.Embed(title = "__/start__" + " : Genre",color = light_blue,description = f"Renseignez (ou non) le genre personnage :\nLe genre du personnage n'a aucune incidences sur ses statistiques et ne sert qu'à des fins orthographiques"),components=components)
    
            def checkIsAuthorReact(reaction:interactions.ComponentContext):
                reaction = reaction.ctx
                return reaction.author.id == ctx.author.id

            try:
                respond = await bot.wait_for_component(timeout=60,check=checkIsAuthorReact,messages=msg)
                respond: ComponentContext = respond.ctx
                testouille,titouille = [GENDER_MALE,GENDER_FEMALE,GENDER_OTHER],["male","female","other"]
                for a in range(0,len(titouille)):
                    if str(respond.custom_id) == titouille[a]:
                        user.gender = testouille[a]
            except asyncio.TimeoutError:
                still = False
                await msg.edit(embeds=interactions.Embed(title="Commande annulée (timeout"))

        if still: #Couleur
            user = await chooseColor(bot,msg,ctx,user)

            if user == False:
                still=False

        if still: #Aspiration
            user.aspiration = await chooseAspiration(bot,msg,ctx,user)
            if user.aspiration != None:
                user = restats(user)

                existFile(pathUserProfile)
                if saveCharFile(pathUserProfile,user):
                    aliceStatsDb.addUser(user)
                    desc = "Vous avez terminé la création de votre personnage ! Rassurez-vous, vous pourrez modifier les paramètres renseignés au moyen d'objet spéciaux disponibles dans le shop.\n\nVoici quelques objets pour fêter votre recrutement :"
                    for obj in baseWeapon+baseSkills+baseStuffs:
                        desc += "\n{0} {1}".format(obj.emoji,obj.name)
                        if obj in [baseWeapon[-1],baseSkills[-1],baseStuffs[-1]]:
                            desc += "\n"
                    desc += "\nPourquoi ne pas faire un tour vers **/inventory** pour voir ça ?"

                    await msg.edit(embeds = interactions.Embed(title = "__/start__", color= user.color, description=desc),components=[])
                else:
                    await msg.edit(embeds = interactions.Embed(title = "__/start__", color= red, description = "Un truc c'est mal passé, l'aventure attendra"))
                    os.remove(pathUserProfile)
            else:
                still = False

        if not(still):
            await msg.edit(embeds= errorEmbed("__/start__","Commande annulée (timeout)"))
    else:
        await ctx.send(embeds=errorEmbed("__/start__","Vous avez déjà commencé l'aventure"),ephemeral=True)
