from asyncio.tasks import wait_for
import discord, os

from discord.ext import commands, tasks
from discord_slash.utils.manage_components import *
from discord_slash import ButtonStyle, SlashCommand

from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *

from commands.command_fight import teamWinDB

buttonReturn = create_actionrow(create_button(2,"Retour",emoji='◀️',custom_id="-1"))
buttonBuy = create_actionrow(create_button(1,"Acheter",getEmojiObject('<:coins:862425847523704832>'),custom_id="0"))
buttonGift = create_actionrow(create_button(3,"Offrir",emoji='🎁',custom_id="1"))

async def shop2(bot : discord.Client, ctx : discord.message, guild : server, args : list,shopping : list):
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile,ctx)
        msg = await loadingEmbed(ctx)
        shopEmb = discord.Embed(title = args[0] +" - Céphalochic",color = user.color, description = "Le magasin est commun à tous les serveurs et est actualisé toutes les 3 heures"+f"\n\nVous disposez actuellement de {user.currencies} {emoji.coins}.\nVous êtes en possession de **{round(userShopPurcent(user),2)}**% du magasin.\n\n*{shopRandomMsg[random.randint(0,len(shopRandomMsg)-1)]}*\n<:empty:866459463568850954>")

        shopWeap,shopSkill,shopStuff,shopOther = [],[],[],[]
        for a in shopping:
            if type(a)==weapon:
                shopWeap.append(a)
            elif type(a)==skill:
                shopSkill.append(a)
            elif type(a)==stuff:
                shopStuff.append(a)
            else:
                shopOther.append(a)

        shopped = shopWeap+shopSkill+shopStuff+shopOther
        shopMsg = ["__**Armes :**__","__**Compétences :**__","__**Equipement :**__","**__Objets :__**"]

        shopField = ["","","",""]
        for a in [0,1,2,3]:
            for b in [shopWeap,shopSkill,shopStuff,shopOther][a]:
                if b != None:
                    shopField[a] += "\n"+b.emoji+ " "
                    shopField[a] += f"{b.name} ({b.price} {emoji.coins})"
            shopEmb.add_field(name=shopMsg[a],value=shopField[a]+"\n<:empty:866459463568850954>",inline=False)

        initMsg = msg

        fcooldown,fqcooldown,faccord,fqaccord = teamWinDB.getFightCooldown(user.team)//60,teamWinDB.getFightCooldown(user.team,True)//60,"",""
        if fcooldown > 1:
            faccord = "s"
        if fqcooldown > 1:
            fqaccord = "s"
        shopEmb.add_field(name=f"__Cooldowns de l'équipe :__",value=f"__Fight__ : {fcooldown} minute{faccord}\n__QuickFight__ : {fqcooldown} minute{fqaccord}",inline=False)

        if userShopPurcent(user) >= 100 and not(user.have(trans)):
            fullEmb = discord.Embed(title="Vous avez obtenu l'intégralité du magasin",description="Vous recevez la compétence suivante en récompense :\n<:limiteBreak:886657642553032824> Transcendance (identifiant : yt)",color=user.color)
            user.skillInventory.append(trans)
            saveCharFile(pathUserProfile,user)
            await ctx.channel.send(embed=fullEmb)

        while 1:
            options = []
            for a in shopped:
                desc,escarpin ="",whatIsThat(a)
                
                if escarpin == 0:
                    desc = "Arme"
                elif escarpin == 1:
                    desc = "Compétence"
                elif escarpin == 2:
                    if a.type == 0:
                        desc = "Accessoire"
                    elif a.type == 1:
                        desc = "Tenue"
                    elif a.type == 2:
                        desc = "Chaussures"
                elif escarpin == 3:
                    desc = "Autre"

                if user.have(a):
                    desc += " - Vous avez déjà cet objet"

                options += [create_select_option(a.name,a.id,getEmojiObject(a.emoji),desc)]
            select = create_select(
                options=options,
                placeholder="Choisissez un article pour avoir plus d'informations dessus"
                )
            
            await initMsg.edit(embed = shopEmb,components=[create_actionrow(select)])
            reacTabl = []

            def check(m):
                return m.author_id == ctx.author.id and m.origin_message.id == msg.id

            def check2(m):
                return m.author_id == ctx.author.id and m.origin_message.id == initMsg.id

            try:
                respond = await wait_for_component(bot,components=select,check=check2,timeout=60)
                await initMsg.edit(embed = shopEmb,components=[create_actionrow(getChoisenSelect(select,respond.values[0]))])
            except:
                await initMsg.edit(embed = shopEmb,components=[timeoutSelect])
                break

            rep = None
            for a in range(0,len(shopped)):
                if shopped[a].id == respond.values[0]:
                    rep = a
                    break

            msg = await respond.send(embed = discord.Embed(title=args[0],description="Recherche de l'objet dans les rayons..."))
            if rep != None:
                typ = whatIsThat(shopped[rep])

                if typ == 0:
                    arm = shopped[rep]
                    repEmb = infoWeapon(arm,user,ctx)

                    if user.have(arm):
                        repEmb.set_footer(text = "Vous possédez déjà cette arme")
                        await msg.edit(embed = repEmb,components=[buttonReturn,buttonGift])
                    elif user.currencies < arm.price:
                        repEmb.set_footer(text = "Vous n'avez pas suffisament de pièces")
                        await msg.edit(embed = repEmb,components=[buttonReturn])
                    else:
                        repEmb.set_footer(text = "Cliquez sur le bouton \"Acheter\" pour acheter cet objet !")
                        await msg.edit(embed = repEmb,components=[buttonReturn,buttonBuy,buttonGift])

                    rep = await wait_for_component(bot,components=[buttonReturn,buttonBuy,buttonGift],check=check,timeout=60)

                    if rep.custom_id == "0":
                        try:
                            user.weaponInventory += [arm]
                            user.currencies = user.currencies - arm.price
                            saveCharFile(pathUserProfile,user)
                            await msg.edit(embed = discord.Embed(title=args[0]+ " - " +arm.name,color = user.color,description = f"Votre achat a bien été effectué ! Faites \"{guild.prefixe}inventory {arm.id}\" pour l'équiper"),components=[])
                        except:
                            await msg.edit(embed = errorEmbed(args[0],"Une erreur s'est produite"))

                    elif rep.custom_id == "1":
                        team = readSaveFiles(absPath + "/userTeams/" + str(user.team) +".team")[0]
                        teamMember = []
                        for a in team:
                            teamMember += [loadCharFile(absPath + "/userProfile/" + str(a) + ".prof")]

                        options = []
                        for a in teamMember:
                            if arm not in a.weaponInventory:
                                options += [create_select_option(a.name,a.owner,getEmojiObject(await getUserIcon(bot,a)))]

                        if options == [] :
                            select = create_select([create_select_option("Vous n'avez pas à voir ça","Nani")],placeholder="Toute votre équipe a déjà cet objet",disabled=True)
                        else:
                            select = create_select(options,placeholder="À qui voulez vous offrir cet objet ?")
                        await msg.edit(embed= repEmb, components=[])
                        await msg.edit(embed= repEmb, components=[buttonReturn,create_actionrow(select)])

                        respond = await wait_for_component(bot,components=[buttonReturn,select],timeout = 60)
                        try:
                            for a in teamMember:
                                if a.owner == respond.values[0]:
                                    try:
                                        temp = await respond.send("Envoie du cadeau...")
                                        a.weaponInventory += [arm]
                                        user.currencies = user.currencies - arm.price
                                        saveCharFile(absPath + "/userProfile/" + str(a.owner) + ".prof",a)
                                        await temp.delete()
                                        await msg.edit(embed = discord.Embed(title=args[0],color = user.color,description = f"Votre cadeau a bien été envoyé !"),components = [create_actionrow(getChoisenSelect(select,respond.values[0]))])
                                    except:
                                        await msg.edit(embed = errorEmbed(args[0],"Une erreur s'est produite"))
                                    break
                        except:
                            await msg.delete()

                    elif rep.custom_id == "-1":
                        await msg.delete()

                elif typ == 1:
                    arm = shopped[rep]
                    repEmb = infoSkill(shopped[rep],user,ctx)
                    if user.have(arm):
                        repEmb.set_footer(text = "Vous possédez déjà cette compétence")
                        await msg.edit(embed = repEmb,components=[buttonReturn,buttonGift])
                    elif user.currencies < arm.price:
                        repEmb.set_footer(text = "Vous n'avez pas suffisament de pièces")
                        await msg.edit(embed = repEmb,components=[buttonReturn])
                    else:
                        repEmb.set_footer(text = "Cliquez sur le bouton \"Acheter\" pour acheter cet objet !")
                        await msg.edit(embed = repEmb,components=[buttonReturn,buttonBuy,buttonGift])

                    rep = await wait_for_component(bot,components=[buttonReturn,buttonBuy,buttonGift],check=check,timeout=60)

                    if rep.custom_id == "0":
                        try:
                            user.skillInventory += [arm]
                            user.currencies = user.currencies - arm.price
                            saveCharFile(pathUserProfile,user)
                            await msg.edit(embed = discord.Embed(title=args[0]+ " - " +arm.name,color = user.color,description = f"Votre achat a bien été effectué ! Faites \"{guild.prefixe}inventory {arm.id}\" pour l'équiper"),components=[])
                        except:
                            await msg.edit(embed = errorEmbed(args[0],"Une erreur s'est produite"))
                    elif rep.custom_id == "1":
                        team = readSaveFiles(absPath + "/userTeams/" + str(user.team) +".team")[0]
                        teamMember = []
                        for a in team:
                            teamMember += [loadCharFile(absPath + "/userProfile/" + str(a) + ".prof")]

                        options = []
                        for a in teamMember:
                            if arm not in a.skillInventory:
                                options += [create_select_option(a.name,a.owner,getEmojiObject(await getUserIcon(bot,a)))]

                        if options == [] :
                            select = create_select([create_select_option("Vous n'avez pas à voir ça","Nani")],placeholder="Toute votre équipe a déjà cet objet",disabled=True)
                        else:
                            select = create_select(options,placeholder="À qui voulez vous offrir cet objet ?")
                        await msg.edit(embed= repEmb, components=[])
                        await msg.edit(embed= repEmb, components=[buttonReturn,create_actionrow(select)])

                        respond = await wait_for_component(bot,components=[buttonReturn,select],timeout = 60)
                        try:
                            for a in teamMember:
                                if a.owner == respond.values[0]:
                                    try:
                                        temp = await respond.send("Envoie du cadeau...")
                                        a.skillInventory += [arm]
                                        user.currencies = user.currencies - arm.price
                                        saveCharFile(absPath + "/userProfile/" + str(a.owner) + ".prof",a)
                                        await msg.clear_reactions() 
                                        await temp.delete()
                                        await msg.edit(embed = discord.Embed(title=args[0],color = user.color,description = f"Votre cadeau a bien été envoyé !"),components = [create_actionrow(getChoisenSelect(select,respond.values[0]))])
                                    except:
                                        await msg.edit(embed = errorEmbed(args[0],"Une erreur s'est produite"))
                                    break
                        except:
                            await msg.delete()
                    elif rep.custom_id == "-1":
                        await msg.delete()

                elif typ == 2:
                    arm = shopped[rep]
                    repEmb = infoStuff(arm,user,ctx)
                    if user.have(arm):
                        repEmb.set_footer(text = "Vous possédez déjà cet objet")
                        await msg.edit(embed = repEmb,components=[buttonReturn,buttonGift])
                    elif user.currencies < arm.price:
                        repEmb.set_footer(text = "Vous n'avez pas suffisament de pièces")
                        await msg.edit(embed = repEmb,components=[buttonReturn])
                    else:
                        repEmb.set_footer(text = "Cliquez sur le bouton \"Acheter\" pour acheter cet objet !")
                        await msg.edit(embed = repEmb,components=[buttonReturn,buttonBuy,buttonGift])

                    rep = await wait_for_component(bot,components=[buttonReturn,buttonBuy,buttonGift],check=check,timeout=60)

                    if rep.custom_id == "0":
                        try:
                            user.stuffInventory += [arm]
                            user.currencies = user.currencies - arm.price
                            saveCharFile(pathUserProfile,user)
                            await msg.edit(embed = discord.Embed(title=args[0]+ " - " +arm.name,color = user.color,description = f"Votre achat a bien été effectué ! Faites \"{guild.prefixe}inventory {arm.id}\" pour l'équiper"),components=[])
                        except:
                            await msg.edit(embed = errorEmbed(args[0],"Une erreur s'est produite"))

                    elif rep.custom_id == "1":
                        team = readSaveFiles(absPath + "/userTeams/" + str(user.team) +".team")[0]
                        teamMember = []
                        for a in team:
                            teamMember += [loadCharFile(absPath + "/userProfile/" + str(a) + ".prof")]

                        options = []
                        for a in teamMember:
                            if arm not in a.stuffInventory:
                                options += [create_select_option(a.name,a.owner,getEmojiObject(await getUserIcon(bot,a)))]

                        if options == [] :
                            select = create_select([create_select_option("Vous n'avez pas à voir ça","Nani")],placeholder="Toute votre équipe a déjà cet objet",disabled=True)
                        else:
                            select = create_select(options,placeholder="À qui voulez vous offrir cet objet ?")
                        await msg.edit(embed= repEmb, components=[])
                        await msg.edit(embed= repEmb, components=[buttonReturn,create_actionrow(select)])

                        respond = await wait_for_component(bot,components=[buttonReturn,select],timeout = 60)
                        try:
                            for a in teamMember:
                                if a.owner == respond.values[0]:
                                    try:
                                        temp = await respond.send("Envoie du cadeau...")
                                        a.stuffInventory += [arm]
                                        user.currencies = user.currencies - arm.price
                                        saveCharFile(absPath + "/userProfile/" + str(a.owner) + ".prof",a)
                                        await msg.clear_reactions() 
                                        await temp.delete()
                                        await msg.edit(embed = discord.Embed(title=args[0],color = user.color,description = f"Votre cadeau a bien été envoyé !"),components = [create_actionrow(getChoisenSelect(select,respond.values[0]))])
                                    except:
                                        await msg.edit(embed = errorEmbed(args[0],"Une erreur s'est produite"))
                                    break
                        except:
                            await msg.delete()

                    elif rep.custom_id == "-1":
                        await msg.delete()

                elif typ == 3:
                    arm = shopped[rep]
                    repEmb = infoOther(arm,user)
                    if user.have(arm):
                        repEmb.set_footer(text = "Vous possédez déjà cette arme")
                        await msg.edit(embed = repEmb,components=[buttonReturn,buttonGift])
                    elif user.currencies < arm.price:
                        repEmb.set_footer(text = "Vous n'avez pas suffisament de pièces")
                        await msg.edit(embed = repEmb,components=[buttonReturn])
                    else:
                        repEmb.set_footer(text = "Cliquez sur le bouton \"Acheter\" pour acheter cet objet !")
                        await msg.edit(embed = repEmb,components=[buttonReturn,buttonBuy,buttonGift])

                    rep = await wait_for_component(bot,components=[buttonReturn,buttonBuy,buttonGift],check=check,timeout=60)

                    if rep.custom_id == "0":
                        try:
                            user.otherInventory += [arm]
                            user.currencies = user.currencies - arm.price
                            saveCharFile(pathUserProfile,user)
                            await msg.edit(embed = discord.Embed(title=args[0]+ " - " +arm.name,color = user.color,description = f"Votre achat a bien été effectué ! Faites \"{guild.prefixe}inventory {arm.id}\" pour l'équiper"),components=[])
                        except:
                            await msg.edit(embed = errorEmbed(args[0],"Une erreur s'est produite"))

                    elif rep.custom_id == "1":
                        team = readSaveFiles(absPath + "/userTeams/" + str(user.team) +".team")[0]
                        teamMember = []
                        for a in team:
                            teamMember += [loadCharFile(absPath + "/userProfile/" + str(a) + ".prof")]

                        options = []
                        for a in teamMember:
                            if arm not in a.otherInventory:
                                options += [create_select_option(a.name,a.owner,getEmojiObject(await getUserIcon(bot,a)))]

                        if options == [] :
                            select = create_select([create_select_option("Vous n'avez pas à voir ça","Nani")],placeholder="Toute votre équipe a déjà cet objet",disabled=True)
                        else:
                            select = create_select(options,placeholder="À qui voulez vous offrir cet objet ?")
                        await msg.edit(embed= repEmb, components=[])
                        await msg.edit(embed= repEmb, components=[buttonReturn,create_actionrow(select)])

                        respond = await wait_for_component(bot,components=[buttonReturn,select],timeout = 60)
                        try:
                            for a in teamMember:
                                if a.owner == respond.values[0]:
                                    try:
                                        temp = await respond.send("Envoie du cadeau...")
                                        a.otherInventory += [arm]
                                        user.currencies = user.currencies - arm.price
                                        saveCharFile(absPath + "/userProfile/" + str(a.owner) + ".prof",a)
                                        await msg.clear_reactions() 
                                        await temp.delete()
                                        await msg.edit(embed = discord.Embed(title=args[0],color = user.color,description = f"Votre cadeau a bien été envoyé !"),components = [create_actionrow(getChoisenSelect(select,respond.values[0]))])
                                    except:
                                        await msg.edit(embed = errorEmbed(args[0],"Une erreur s'est produite"))
                                    break
                        except:
                            await msg.delete()
                    
                    elif rep.custom_id == "-1":
                        await msg.delete()

    else:
        await ctx.channel.send(embed = errorEmbed(args[0],"Vous n'avez pas commencé l'aventure"))