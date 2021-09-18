from discord import embeds
from discord_slash.utils.manage_components import create_actionrow
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from discord_slash import ButtonStyle, SlashCommand
from discord_slash.utils.manage_components import *

import asyncio

aspirationMenu = create_select(
    options=[
        create_select_option("Berserkeur",value="0"),
        create_select_option("Observateur",value="1"),
        create_select_option("Poids Plume",value="2"),
        create_select_option("Idole",value="3"),
        create_select_option("Erudit",value="4"),
        create_select_option("Tête Brulée",value="5"),
        create_select_option("Altruiste",value="7"),
        create_select_option("Aventurier",value="8")
        ],
    placeholder="Sélectionnez une aspiration pour avoir plus d'informations dessus"
    )

aspirationMenuD = create_select(
    options=[
        create_select_option("Tu es pas sensé voir ça",value="0"),

        ],
    placeholder="Veillez répondre aux emojis sur le nouveau message",
    disabled=True
    )

optionIka, optionTako = [],[]
for a in range(0,len(colorChoice)):
    optionIka += [create_select_option(colorChoice[a],str(colorId[a]),emoji=getEmojiObject(emoji.icon[1][a]))]
    optionTako += [create_select_option(colorChoice[a],str(colorId[a]),emoji=getEmojiObject(emoji.icon[2][a]))]

async def chooseAspiration(bot : discord.client, msg : discord.message,ctx : discord.message,user : char,args: str):
    choosed = False
    while not(choosed):
        action = create_actionrow(aspirationMenu)
        await msg.clear_reactions()
        await msg.edit(embed = discord.Embed(title = args[0] + " : Aspiration",color = user.color,description = f"Le moment est venu de selectionnez l'aspiration de votre personnage.\n\nRéagissez aux emojis ci-dessus pour avoir plus d'informations sur les 8 aspirations qui sont : \n- Berserkeur\n- Observateur\n- Poids Plume\n- Idole\n- Erudit\n- Tête Brulée\n- Altruiste\n- Aventurier\n\nL'aspiration déterminera les statistiques de départ et leurs maximums de votre personnage."),components = [action])

        def check(m):
            return m.author_id == ctx.author.id and m.origin_message.id == msg.id

        haveReaction = False
        try:
            respond = await wait_for_component(bot, components=aspirationMenu, check=check,timeout=60)
            haveReaction = True
        except:
            pass

        if haveReaction:
            action = create_actionrow(aspirationMenuD)
            await msg.edit(embed = discord.Embed(title = args[0] + " : Aspiration",color = user.color,description = f"Le moment est venu de selectionnez l'aspiration de votre personnage.\n\nRéagissez aux emojis ci-dessus pour avoir plus d'informations sur les 8 aspirations qui sont : \n- Berserkeur\n- Observateur\n- Poids Plume\n- Idole\n- Erudit\n- Tête Brulée\n- Altruiste\n- Aventurier\n\nL'aspiration déterminera les statistiques de départ et leurs maximums de votre personnage."),components = [action])
            inspiDesc = [manPage8[1],manPage9[1],manPage10[1],manPage11[1],manPage12[1],manPage13[1],"Aspiration supprimée",manPage14[1],manPage15[1]]

            msg2 = await respond.send(embed = discord.Embed(title = args[0] + " : "+inspi[int(respond.values[0])],color = user.color,description = f"{inspiDesc[int(respond.values[0])]}\n\nPour choisir cette aspiration, cochez le check-ci dessous"))

            await msg2.add_reaction(emoji.backward_arrow)
            await msg2.add_reaction(emoji.check)
            def checkIsAuthorReact(reaction,user):
                return user == ctx.author and int(reaction.message.id) == int(msg2.id)

            try:
                respondEmoji = await bot.wait_for("reaction_add",timeout = 60,check=checkIsAuthorReact)
                if str(respondEmoji[0]) == emoji.check:
                    await msg2.delete()
                    return int(respond.values[0])
                else:
                    await msg2.delete()
            except:
                await msg2.delete()
                
        else:
            await msg.clear_reactions()
            return None

async def chooseName(bot : discord.client, msg : discord.message, ctx: discord.message, args : list,user : char):
    """Selection du nom du personnage\n
    Renvoie User avec le nouveau si réussite, False sinon"""
    await msg.edit(embed = discord.Embed(title = args[0] + " : Nom",color = light_blue,description = f"Ecrivez le nom de votre personnage :\n\nVous ne pourrez pas modifier le nom de votre personnage par la suite"))
    haveName = False
    def checkIsAuthor(message):
        return ctx.author == message.author
    try:
        respond = await bot.wait_for("message",timeout = 60,check = checkIsAuthor)
        user.name = respond.content
        haveName = True
    except:
        await msg.edit(embed = errorEmbed(args[0],"Timeout, commande annulée"))    

    if haveName:
        try:
            await respond.delete()
        except:
            print("Il me manque la permission de supprimer des messages")
        return user
    else:
        return False

async def chooseColor(bot : discord.client, msg : discord.message,ctx : discord.message, user : char, args: str):
    ballerine = ""
    for a in range(0,len(colorChoice)):
        ballerine += f"{emoji.icon[user.species][a]} - {colorChoice[a]}\n"
    babie = []
    if user.customColor:
        ballerine += ["<:empty_squid:882766450308284417>","<:empty_octo:882766485754351698>"][user.species]+" - Couleur personnalisé ("+hex(user.color)+")\n"
        babie = [create_select_option("Couleur personnalisée","Custom",description=hex(user.color),emoji=getEmojiObject(["<:empty_squid:882766450308284417>","<:empty_octo:882766485754351698>"][user.species]))]

    options = [optionIka,optionTako][user.species-1] + babie
    colorMenuIka = create_select(
        options=options,
        placeholder="Selectionnez votre couleur",
        )
    colorMenuTako = create_select(
        options=options,
        placeholder="Selectionnez votre couleur",
        )

    if user.species == 1:
        action = create_actionrow(colorMenuIka)
    elif user.species == 2:
        action = create_actionrow(colorMenuTako)

    await msg.edit(embed = discord.Embed(title = args[0] + " : Couleur",color = light_blue,description = f"Sélectionnez la couleur de votre personnage :\n{ballerine}\nLa couleur sera affiché sur tous les embeds et l'icone de votre personnage."),components=[action])

    def check(m):
        return m.author_id == ctx.author.id and m.origin_message.id == msg.id

    haveReaction = False
    try:
        respond = await wait_for_component(bot, components=action, check=check,timeout=60)
        haveReaction = True
    except:
        await msg.clear_reactions()

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

async def changeCustomColor(bot,msg,ctx,user,args):
    def check(param):
        return param.author.id == ctx.author.id and param.channel.id == ctx.channel.id
    def checkReact(param,second):
        return second.id == ctx.author.id and param.message.id == msg.id and (str(param) in [emoji.cross,emoji.check])
    while 1:
        await msg.clear_reactions()
        await msg.edit(embed = discord.Embed(title="Couleur personnalisée",description="Veillez entrer le code hexadecimal de votre nouvelle couleur :\n\nExemples :\n94d4e4\n#94d4e4",color = user.color))
        
        respond = await bot.wait_for("message",check=check,timeout=60)
        color = convertStrtoHex(respond.content)

        try:
            await respond.delete()
        except:
            pass

        if color == None:
            await msg.edit(embed = errorEmbed(args[0],"Le code donné n'est pas un code hexadecimal valide"))
            break

        await msg.edit(embed = discord.Embed(title = "Couleur personnalisée",description="Est-ce que cette couleur vous va ?",color = color))
        await msg.add_reaction(emoji.cross)
        await msg.add_reaction(emoji.check)
        try:
            react = await bot.wait_for("reaction_add",check=checkReact,timeout=60)
        except:
            await msg.clear_reactions()
            break
        if str(react[0]) == emoji.check:
            user.color = color
            user.customColor = True
            return user

    return None   

async def start(bot : discord.client, ctx : discord.message, guild : server, args : list):
    """Commande de création de personnage"""
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"

    if not os.path.exists(pathUserProfile):
        def checkIsAuthor(message):
            return ctx.author == message.author

        still = True
        user = char(ctx.author.id)
        msg = await loadingEmbed(ctx)

        user = await chooseName(bot,msg,ctx,args,user)

        if user == False:
            still = False
        
        if still: #Espèce
            await msg.edit(embed = discord.Embed(title = args[0] + " : Espèce",color = light_blue,description = f"Sélectionnez l'espèce de votre personnage :\n\n<:ikaLBlue:866459302319226910> Inkling\n<:takoLBlue:866459095875190804> Octaling\n\nL'espèce n'a aucune influence sur les statistiques du personnage."))
            await msg.add_reaction('<:ikaLBlue:866459302319226910>')
            await msg.add_reaction('<:takoLBlue:866459095875190804>')

            def checkIsAuthorReact1(reaction,user):
                return user == ctx.author and reaction.message == msg and (str(reaction)=='<:ikaLBlue:866459302319226910>' or str(reaction) == '<:takoLBlue:866459095875190804>')

            respond = await bot.wait_for("reaction_add",timeout = 60,check = checkIsAuthorReact1)

            if str(respond[0]) == '<:ikaLBlue:866459302319226910>':
                user.species = 1
            else:
                user.species = 2
        
        if still: #Genre
            await msg.clear_reactions()
            await msg.edit(embed = discord.Embed(title = args[0] + " : Genre",color = light_blue,description = f"Renseignez (ou non) le genre personnage :\nLe genre du personnage n'a aucune incidences sur ses statistiques\n"))
            await msg.add_reaction('♂️')
            await msg.add_reaction('♀️')
            await msg.add_reaction(emoji.forward_arrow)
            def checkIsAuthorReact(reaction,user):
                return user == ctx.author and reaction.message == msg and (str(reaction)=='♀️' or str(reaction) == '♂️' or str(reaction) == emoji.forward_arrow)

            respond = await bot.wait_for("reaction_add",timeout = 60,check = checkIsAuthorReact)
            testouille,titouille = [GENDER_MALE,GENDER_FEMALE,GENDER_OTHER],['♂️','♀️',emoji.forward_arrow]
            for a in range(0,len(titouille)):
                if str(respond[0]) == titouille[a]:
                    user.gender = testouille[a]

        if still: #Couleur
            await msg.clear_reactions()
            user = await chooseColor(bot,msg,ctx,user,args)

            if user == False:
                still=False

        if still: #Aspiration
            user.aspiration = await chooseAspiration(bot,msg,ctx,user,args)
            if user.aspiration != None:
                user = restats(user)

                existFile(pathUserProfile)
                await msg.clear_reactions()
                if saveCharFile(pathUserProfile,user):
                    await msg.delete()
                    await ctx.channel.send(embed = discord.Embed(title = args[0], color= user.color, description = f"Tout a bien été enregistré !\nN'hésite pas à utiliser la commande {guild.prefixe}help pour connaître les commandes de l'Aventure\nOu bien juste lire le manuel avec {guild.prefixe}manuel"))
                else:
                    await msg.delete()
                    await ctx.channel.send(embed = discord.Embed(title = args[0], color= red, description = rejectProfileStart))
                    os.remove(pathUserProfile)
            else:
                still = False

        if not(still):
            await msg.edit(embed= errorEmbed(args[0],"Commande annulée (timeout)"))
    else:
        await ctx.channel.send(embed=errorEmbed(args[0],"Vous avez déjà commencé l'aventure"))