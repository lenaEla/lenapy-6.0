import discord, os, asyncio

from discord_slash.utils.manage_components import *
from discord_slash import ButtonStyle

from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from emoji import backward_arrow

from commands.command_start import chooseAspiration,chooseColor,chooseName,changeCustomColor

inventoryMenu = create_select(
    options=[
        create_select_option("Inventaire d'Arme",value="0",emoji=getEmojiObject('<:splattershot:866367647113543730>')),
        create_select_option("Inventaire de Compétences",value="1",emoji=getEmojiObject('<:splatbomb:873527088286687272>')),
        create_select_option("Inventaire d'Equipement",value="2",emoji=getEmojiObject('<:bshirt:867156711251771402>')),
        create_select_option("Inventaire d'Objets",value="3",emoji=getEmojiObject('<:changeAppa:872174182773977108>')),
        create_select_option("Éléments",value="4",emoji=getEmojiObject('<:krisTal:888070310472073257>'))
        ],
    placeholder="Sélectionnez l'inventaire dans lequel vous voulez aller"
        )

retunrButton = create_button(2,"Retour",backward_arrow,"return")
changeElemEnable = create_button(1,"Changer d'élément",getEmojiObject('<:krisTal:888070310472073257>'),"change")
changeElemDisabled = create_button(1,"Changer d'élément",getEmojiObject('<:krisTal:888070310472073257>'),"change",disabled=True)

elemOptions = []
for a in range(0,len(elemDesc)):
    elemOptions.append(create_select_option(elemNames[a],str(a),getEmojiObject(elemEmojis[a])))

elemSelect = create_select(elemOptions,placeholder="En savoir plus ou changer d'élément")

async def elements(bot : discord.client, ctx : discord.message, msg : discord.message, user : classes.char):
    """Function to call for inventory elements.\n
    Edit de Msg for display the actual element of the user and a short description.\n
    Can also change the element if th user have a Elemental Cristal."""

    def check(m):
        return m.author_id == ctx.author.id and m.origin_message.id == msg.id

    def checkSecond(m):
        return m.author_id == ctx.author.id and m.origin_message.id == secondMsg.id

    if user.level < 10: # The user doesn't have the level
        elemEmbed = discord.Embed(title="__Éléments__",color=user.color,description="Les éléments renforcent la spécialisation d'un personnage en augmentant les dégâts qu'il fait suivant certaines conditions définie par l'élément choisi\nLes équipements peuvent également avoir des éléments. Avoir des équipements du même élément que soit accroie un peu leurs statistiques\n")
        elemEmbed.add_field(name="__Contenu verouillé :__",value="Les éléments se débloquent à partir du nieau 10")
        await msg.edit(embed=elemEmbed,components=[])

    else:
        while 1:
            elemEmbed = discord.Embed(title="__Éléments__",color=user.color,description="Les éléments renforcent la spécialisation d'un personnage en augmentant les dégâts qu'il fait suivant certaines conditions définie par l'élément choisi\nLes équipements peuvent également avoir des éléments. Avoir des équipements du même élément que soit accroie un peu leurs statistiques\n")
            elemEmbed.add_field(name="__Votre élément actuel est l'élément **{0}** ({1}) :__".format(elemNames[user.element],elemEmojis[user.element]),value=elemDesc[user.element])
            await msg.edit(embed = elemEmbed,components=[create_actionrow(elemSelect)])

            try:
                respond = await wait_for_component(bot,msg,check=check,timeout=60)
            except:
                await msg.edit(embed = elemEmbed,components=[])
                break

            resp = int(respond.values[0])
            respEmb = discord.Embed(title = "__Élément : {0}__".format(elemNames[resp]),description = elemDesc[resp],color=user.color)
            if user.have(elementalCristal) and user.level >= 10:
                actionrow = create_actionrow(retunrButton,changeElemEnable)
            else:
                respEmb.set_footer(text="Vous ne possédez pas de cristaux élémentaire ou n'avez pas le niveau requis")
                actionrow = create_actionrow(retunrButton,changeElemDisabled)

            secondMsg = await respond.send(embed = respEmb,components=[actionrow])

            try:
                respond = await wait_for_component(bot,secondMsg,check=checkSecond,timeout=60)
            except:
                await secondMsg.delete()
                await msg.edit(embed = elemEmbed,components=[])
                break

            if respond.custom_id == "change":
                user.element = resp
                user.otherInventory.remove(elementalCristal)
                saveCharFile(absPath+"/userProfile/"+str(user.owner)+".prof",user)
                await secondMsg.edit(embed = discord.Embed(title="__Élément : {0}__".format(elemNames[resp]),description="Votre élément a bien été modifié",color=user.color),components=[])
                await asyncio.sleep(5)
                await secondMsg.delete()
            else:
                await secondMsg.delete()


async def inventory(bot : discord.client, ctx : discord.message, args : list,slashed = None):
    """Commande d'inventaire d'un personnage"""
    
    def checkIsAuthor(message):
        return message.author.id == ctx.author.id and message.channel.id == ctx.channe.id

    if slashed != None:
        ctx.mentions = slashed[1]

    if ctx.mentions == []:
        pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
    else:
        pathUserProfile = absPath + "/userProfile/" + str(ctx.mentions[0].id) + ".prof"

    def checkIsAuthorReact(reaction,user):
        return user == ctx.author and int(reaction.message.id) == int(msg.id)

    def check(m):
        return m.author_id == ctx.author.id and m.origin_message.id == msgOrigine.id

    if os.path.exists(pathUserProfile):
        state = 0
        user = loadCharFile(pathUserProfile,ctx)
        okForCommand = True
        if ctx.mentions != []:
            if ctx.author.id not in user.procuration:
                okForCommand = False
            else:
                args.remove(args[1])

        if okForCommand:
            if args[1] == None:
                if slashed == None:
                    actionrow = create_actionrow(inventoryMenu)
                    embed = discord.Embed(title = args[0],color=user.color,description="Dans quel inventaire voulez vous aller ?")
                    msgOrigine = await ctx.channel.send(embed=embed,components=[actionrow])

                    on = True
                    try:
                        menuSelect = await wait_for_component(bot, components=inventoryMenu, timeout = 60,check=check)
                        actionrow = create_actionrow(getChoisenSelect(inventoryMenu,menuSelect.values[0]))
                        state = int(menuSelect.values[0])
                    except:
                        actionrow = timeoutSelect
                        on = False

                    await msgOrigine.edit(embed=embed,components=[actionrow])
                
                else:
                    menuSelect = ctx
                    state = slashed[0]
                    on = True
                
                if on:
                    msg = await menuSelect.send(embed = discord.Embed(title = "/inventory", description = emoji.loading))
                    page=0
                    while 1:
                        if state == 0:
                            rep = discord.Embed(title = f"__Inventaire de {user.name} - Armes__ :",color = user.color,description = "Pour avoir plus d'information sur une arme ou l'équiper, réalisez la commande \"inventory (id)\"")
                            rep.add_field(name = "__Arme équipée :__",value = f"{user.weapon.emoji} {user.weapon.name}",inline = False)

                            temp = ""

                            maxPage=len(user.weaponInventory)//10
                            if len(user.weaponInventory)%10 == 0:
                                maxPage -= 1
                            listOfWeapon = []
                            for a in range(0,10):
                                try:
                                    listOfWeapon += [user.weaponInventory[page*10+a]]
                                except:
                                    pass

                            for a in listOfWeapon:
                                temp += f"{ a.emoji} {a.name} ({a.id})\n"

                            temp += f"\nPage **{page+1}** sur {maxPage+1}"
                            
                            rep.add_field(name = "__Inventaire d'armes :__",value = temp,inline = False)

                            await msg.clear_reactions()

                            if page != 0:
                                previousBoutton = create_button(ButtonStyle(2),"Page précédente",emoji.backward_arrow,"back")
                            else:
                                previousBoutton = create_button(ButtonStyle(2),"Page précédente",emoji.backward_arrow,"back",disabled=True)
                            if page != maxPage:
                                nextBoutton = create_button(ButtonStyle(2),"Page suivante",emoji.forward_arrow,"forward")
                            else:
                                nextBoutton = create_button(ButtonStyle(2),"Page suivante",emoji.forward_arrow,"forward",disabled=True)

                            options=[]
                            for a in listOfWeapon:
                                options += [create_select_option(a.name,a.id,getEmojiObject(a.emoji))]

                            select=create_select(
                                options=options,
                                placeholder="Sélectionnez un objet pour avoir plus d'informations dessus"
                                )

                            actionSelect = create_actionrow(select)
                            actionPrevious = create_actionrow(previousBoutton)
                            actionNext = create_actionrow(nextBoutton)
                            actionTabl = [actionPrevious,actionNext,actionSelect]

                            await msg.edit(embed = rep,components=actionTabl)
                            def check(m):
                                return m.author_id == ctx.author.id and m.origin_message.id == msg.id

                            respond = await wait_for_component(bot, components=actionTabl, check=check)

                            try:
                                if respond.custom_id == "back":
                                    page -= 1
                                    temp = await respond.send("Page changée !")
                                    await temp.delete()
                                elif respond.custom_id == "forward":
                                    page += 1
                                    temp = await respond.send("Page changée !")
                                    await temp.delete()
                            except:
                                pass

                            try:
                                args[1] = respond.values[0]
                                args += [None]
                                await msg.delete()
                                await msgOrigine.delete()
                                break
                            except:
                                pass

                            if args[1] != None:
                                break

                        elif state == 1:
                            rep = discord.Embed(title = f"__Inventaire de {user.name} - Compétences__ :",color = user.color,description = "Pour avoir plus d'information sur une compétence ou l'équiper, réalisez la commande \"inventory (id)\"")
                            temp = ""
                            for a in range(0,len(user.skills)):
                                if user.skills[a] != None and user.skills[a] != "0":
                                    temp+=f"[{a+1}] : {user.skills[a].emoji} {user.skills[a].name}\n"
                                else:
                                    temp+=f"[{a+1}] : Emplacement vide\n"
                            
                            rep.add_field(name = "__Compétences équipées :__",value = temp ,inline = False)

                            temp = ""
                            maxPage=len(user.skillInventory)//10
                            if len(user.skillInventory)%10 == 0:
                                maxPage	-= 1
                            listOfSkills = []
                            for a in range(0,10):
                                try:
                                    listOfSkills += [user.skillInventory[page*10+a]]
                                except:
                                    pass

                            for a in listOfSkills:
                                temp += f"{ a.emoji} {a.name} ({a.id})\n"

                            temp += f"\nPage **{page+1}** sur {maxPage+1}"
                            
                            rep.add_field(name = "__Inventaire de compétences :__",value = temp,inline = False)

                            await msg.clear_reactions()
                            if page != 0:
                                previousBoutton = create_button(ButtonStyle(2),"Page précédente",emoji.backward_arrow,"back")
                            else:
                                previousBoutton = create_button(ButtonStyle(2),"Page précédente",emoji.backward_arrow,"back",disabled=True)
                            if page != maxPage:
                                nextBoutton = create_button(ButtonStyle(2),"Page suivante",emoji.forward_arrow,"forward")
                            else:
                                nextBoutton = create_button(ButtonStyle(2),"Page suivante",emoji.forward_arrow,"forward",disabled=True)

                            options=[]
                            for a in listOfSkills:
                                options += [create_select_option(a.name,a.id,getEmojiObject(a.emoji))]

                            select=create_select(
                                options=options,
                                placeholder="Sélectionnez un objet pour avoir plus d'informations dessus"
                                )

                            if len(select["options"]) <= 0:
                                select=create_select([create_select_option("Bah alors on viens de commencer ?","Waw !")],placeholder="Vous n'avez pas de compétences",disabled = True)

                            actionSelect = create_actionrow(select)
                            actionButtons = create_actionrow(previousBoutton,nextBoutton)
                            actionTabl = [actionButtons,actionSelect]

                            await msg.edit(embed = rep,components=actionTabl)
                            def check(m):
                                return m.author_id == ctx.author.id and m.origin_message.id == msg.id

                            respond = await wait_for_component(bot, components=actionTabl, check=check)
                            try:
                                if respond.custom_id == "back":
                                    page -= 1
                                    temp = await respond.send("Page changée !")
                                    await temp.delete()
                                elif respond.custom_id == "forward":
                                    page += 1
                                    temp = await respond.send("Page changée !")
                                    await temp.delete()
                            except:
                                pass

                            try:
                                args[1] = respond.values[0]
                                args += [None]
                                await msg.delete()
                                await msgOrigine.delete()
                                break
                            except:
                                pass

                            if args[1] != None:
                                break
                            
                        elif state == 2:
                            rep = discord.Embed(title = f"__Inventaire de {user.name} - Equipement__ :",color = user.color,description = "Pour avoir plus d'information sur un équipement ou l'équiper, réalisez la commande \"inventory (id)\"")
                            temp,temp2 = "",["Accessoire","Corps","Chaussures"]
                            for a in range(0,len(user.stuff)):
                                if user.stuff[a] != "0":
                                    temp+=f"{temp2[a]} : {user.stuff[a].emoji} {user.stuff[a].name}\n"
                            rep.add_field(name = "__Equipement porté :__",value = temp,inline = False)

                            temp = ""
                            maxPage=len(user.stuffInventory)//10
                            if len(user.stuffInventory)%10 == 0:
                                maxPage -= 1
                            listOfStuffs = []
                            for a in range(0,10):
                                try:
                                    listOfStuffs += [user.stuffInventory[page*10+a]]
                                except:
                                    pass

                            for a in listOfStuffs:
                                temp += f"{ a.emoji} {a.name} ({a.id})\n"

                            temp += f"\nPage **{page+1}** sur {maxPage+1}"
                            
                            rep.add_field(name = "__Inventaire d'équipements :__",value = temp,inline = False)

                            await msg.clear_reactions()
                            if page != 0:
                                previousBoutton = create_button(ButtonStyle(2),"Page précédente",emoji.backward_arrow,"back")
                            else:
                                previousBoutton = create_button(ButtonStyle(2),"Page précédente",emoji.backward_arrow,"back",disabled=True)
                            if page != maxPage:
                                nextBoutton = create_button(ButtonStyle(2),"Page suivante",emoji.forward_arrow,"forward")
                            else:
                                nextBoutton = create_button(ButtonStyle(2),"Page suivante",emoji.forward_arrow,"forward",disabled=True)

                            options=[]
                            for a in listOfStuffs:
                                options += [create_select_option(a.name,a.id,getEmojiObject(a.emoji),a.orientation)]

                            select=create_select(
                                options=options,
                                placeholder="Sélectionnez un objet pour avoir plus d'informations dessus"
                                )

                            actionSelect = create_actionrow(select)
                            actionPrevious = create_actionrow(previousBoutton)
                            actionNext = create_actionrow(nextBoutton)
                            actionTabl = [actionPrevious,actionNext,actionSelect]

                            await msg.edit(embed = rep,components=actionTabl)
                            def check(m):
                                return m.author_id == ctx.author.id and m.origin_message.id == msg.id

                            respond = await wait_for_component(bot, components=actionTabl, check=check)
                            try:
                                if respond.custom_id == "back":
                                    page -= 1
                                    temp = await respond.send("Page changée !")
                                    await temp.delete()
                                elif respond.custom_id == "forward":
                                    page += 1
                                    temp = await respond.send("Page changée !")
                                    await temp.delete()
                            except:
                                pass

                            try:
                                args[1] = respond.values[0]
                                args += [None]
                                await msg.delete()
                                await msgOrigine.delete()
                                break
                            except:
                                pass

                            if args[1] != None:
                                break

                        elif state == 3:
                            rep = discord.Embed(title = f"__Inventaire de {user.name} - Objet__ :",color = user.color,description = "Pour avoir plus d'information sur un objet, réalisez la commande \"inventory (id)\"")
                            temp = ""
                            for a in user.otherInventory:
                                    temp += f"{a.emoji} {a.name} ({a.id})\n"
                            
                            if temp == "":
                                temp = "Votre inventaire est vide"

                            rep.add_field(name = "__Inventaire d'objets :__",value = temp,inline = False)
                            await msg.edit(embed=rep)
                            break

                        elif state == 4:
                            await elements(bot,ctx,msg,user)

            if len(args) > 3:
                for a in range(2,len(args)):
                    if args[a] != None:
                        args[1] += " "+args[a]
            
            if args[1] != None:
                inv = whatIsThat(args[1])
                if inv != None:
                    msg = await loadingEmbed(ctx)
                    if inv == 0:
                        weap = findWeapon(args[1])
                        
                        repEmb = infoWeapon(weap,user,ctx)
                        
                        trouv = False
                        for a in user.weaponInventory:
                            if a.id == args[1][0:2] or a.name.lower() == args[1].lower():
                                trouv = True

                        if not(trouv):
                            repEmb.set_footer(text = "Vous ne possédez pas cette arme")
                            await msg.edit(embed = repEmb)
                        elif weap == user.weapon:
                            repEmb.set_footer(text = "Vous utilisez déjà cette arme")
                            await msg.edit(embed = repEmb)

                        else:
                            repEmb.set_footer(text = "Cliquez sur l'icone de l'arme pour l'équiper")
                            await msg.edit(embed = repEmb)
                            await msg.add_reaction(weap.emoji)

                            def checkisReaction(reaction, user):
                                return user == ctx.author and str(reaction.emoji) ==  weap.emoji

                            await bot.wait_for("reaction_add",timeout=60,check=checkisReaction)
                            user.weapon = weap
                            if saveCharFile(pathUserProfile,user):
                                await msg.clear_reactions()
                                await msg.edit(embed = discord.Embed(title = args[0],color = user.color,description = "Votre nouvelle arme a bien été équipée"))
                            else:
                                await msg.edit(embed = errorEmbed("Erreur","Une erreur est survenue. La modification a pas été enregistrée"))

                    elif inv == 1:
                        weap = findSkill(args[1])

                        emb = infoSkill(weap,user,ctx)

                        trouv = False
                        for a in user.skillInventory:
                            if a == weap:
                                trouv = True
                                break
                        
                        ballerine=False
                        for a in user.skills:
                            if a != '0' and a != None:
                                if a == weap:
                                    ballerine = True
                                    break

                        if not(trouv):
                            emb.set_footer(text = "Vous ne possédez pas cette compétence")
                            await msg.edit(embed = emb)

                        elif ballerine:
                            emb.set_footer(text = "Vous avez déjà équipé cette compétence. Voulez vous la déséquiper ?")
                            await msg.edit(embed = emb)
                            await msg.add_reaction(emoji.check)
                            def checkisReaction(reaction, user):
                                return user == ctx.author and reaction.message == msg

                            react = None
                            try:
                                react = await bot.wait_for("reaction_add",timeout=60,check=checkisReaction)
                            except:
                                await msg.clear_reactions()

                            if react != None:
                                if str(react[0]) == emoji.check:
                                    for a in range(0,5):
                                        if user.skills[a] == weap:
                                            user.skills[a] = "0"
                                            break

                                    saveCharFile(pathUserProfile,user)
                                    await msg.edit(embed = discord.Embed(title="Inventory",color=user.color,description="Votre compétence a bien été déséquipée"))

                        elif not(weap.havConds(user=user)):
                            emb.set_footer(text = "Vous ne respectez pas les conditions de cette compétence")
                            await msg.edit(embed = emb)

                        else:
                            hasUltimate=False
                            for a in [0,1,2,3,4]:
                                if type(user.skills[a]) == skill:
                                    if user.skills[a].ultimate and weap.ultimate:
                                        hasUltimate=True
                                        break

                            options = []
                            for a in [0,1,2,3,4]:
                                if type(user.skills[a]) == skill:
                                    ultimatum = ""
                                    if user.skills[a].ultimate:
                                        ultimatum = "Capacité ultime - "
                                    if hasUltimate and user.skills[a].ultimate and weap.ultimate:
                                        options += [create_select_option(user.skills[a].name,user.skills[a].id,getEmojiObject(user.skills[a].emoji),ultimatum+tablTypeStr[user.skills[a].type])]
                                    elif not(hasUltimate):
                                        options += [create_select_option(user.skills[a].name,user.skills[a].id,getEmojiObject(user.skills[a].emoji),ultimatum+tablTypeStr[user.skills[a].type])]
                                elif not(hasUltimate):
                                    options += [create_select_option(f"Slot de compétence vide",str(a+1),emoji.count[a+1])]

                            select = create_select(options,placeholder="Sélectionnez un emplacement")

                            emb.set_footer(text = "Cliquez sur l'icone d'emplacement pour équiper")

                            await msg.edit(embed = emb,components=[create_actionrow(select)])
                            def check(m):
                                return m.author_id == ctx.author.id and m.origin_message.id == msg.id

                            react = None
                            try:
                                react = await wait_for_component(bot,messages=msg,timeout=60,check=check)
                            except:
                                await msg.edit(embed = emb,components=[timeoutSelect])

                            if react != None:
                                await msg.edit(embed = emb,components=[create_actionrow(getChoisenSelect(select,react.values[0]))])
                                pondu = await react.send("Changement de compétence en cours...")
                            
                                for a in [0,1,2,3,4]:
                                    ballerine,babie = False,False
                                    if user.skills[a] != "0" and user.skills[a] != None:
                                        ballerine = react.values[0] == user.skills[a].id
                                    else:
                                        babie = int(react.values[0]) == a+1
                                    if babie or ballerine:
                                        try:
                                            user.skills[a] = weap
                                            saveCharFile(pathUserProfile,user)
                                            await pondu.delete()
                                            await msg.edit(embed = discord.Embed(title = args[0],color = user.color,description="Vous avez bien équipé votre compétence !",components=[]))
                                        except:
                                            await msg.edit(embed = errorEmbed(args[0],"Une erreur est survenue",components=[]))
                                        break
                        
                    elif inv == 2:
                        weap = findStuff(args[1])

                        emb = infoStuff(weap,user,ctx)

                        trouv = False
                        for a in user.stuffInventory:
                            if a.id == args[1][0:2] or a.name.lower() == args[1].lower():
                                trouv = True

                        if not(trouv):
                            emb.set_footer(text = "Vous ne possédez pas cet équipement")
                            await msg.edit(embed = emb)

                        elif weap == user.stuff[weap.type]:
                            emb.set_footer(text = "Vous portez cet équipement")
                            await msg.edit(embed = emb)

                        else:
                            emb.set_footer(text = "Cliquez sur l'icone de l'équipement pour l'équiper")
                            await msg.edit(embed = emb)
                            await msg.add_reaction(weap.emoji)

                            def checkisReaction(reaction, user):
                                return user == ctx.author and str(reaction.emoji) ==  weap.emoji

                            await bot.wait_for("reaction_add",timeout=60,check=checkisReaction)
                            user.stuff[weap.type] = weap
                            if saveCharFile(pathUserProfile,user):
                                await msg.clear_reactions()
                                await msg.edit(embed = discord.Embed(title = args[0],color = user.color,description = "Votre nouvel équipement a bien été équipée"))
                            else:
                                await msg.edit(embed = errorEmbed("Erreur","Une erreur est survenue. La modification a pas été enregistrée"))
                    
                    elif inv == 3:
                        obj = findOther(args[1])
                        repEmb = infoOther(obj,user)
                        trouv = False
                        for a in user.otherInventory:
                            if a.id == args[1][0:2] or a.name.lower() == args[1].lower():
                                trouv = True

                        if not(trouv):
                            repEmb.set_footer(text = "Vous ne possédez pas cet objet")
                            await msg.edit(embed = repEmb)

                        else:
                            repEmb.set_footer(text = "Cliquez sur l'icone de l'objet l'utiliser")
                            await msg.edit(embed = repEmb)
                            await msg.add_reaction( obj.emoji)

                            def checkisReaction(reaction, user):
                                return user == ctx.author and str(reaction.emoji) ==  obj.emoji

                            await bot.wait_for("reaction_add",timeout=60,check=checkisReaction)

                            if obj==changeAspi:
                                try:
                                    user.aspiration = await chooseAspiration(bot,msg,ctx,user,args)
                                    if user.aspiration != False:
                                        user = restats(user)

                                        user.otherInventory.remove(changeAspi)
                                        if saveCharFile(pathUserProfile,user):
                                            await msg.clear_reactions()
                                            await msg.edit(embed = discord.Embed(title = args[0],color = user.color,description = "Votre nouvelle aspiration a bien été prise en compte et vous avez récupéré vos points bonus"))
                                        else:
                                            await msg.clear_reactions()
                                            await msg.edit(embed = errorEmbed(args[0],"Une erreure est survenue"))
                                except:
                                    await msg.clear_reactions()
                                    await msg.edit(embed = errorEmbed(args[0],"Une erreure est survenue"))
                            elif obj==changeAppa:
                                await msg.clear_reactions()
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

                                await msg.clear_reactions()

                                user = await chooseColor(bot,msg,ctx,user,args)

                                if user != False:
                                    user.otherInventory.remove(changeAppa)
                                    saveCharFile(pathUserProfile,user)
                                    await msg.clear_reactions()
                                    await msg.edit(embed = discord.Embed(title="Changement d'apparence",color = user.color,description="Votre changement a bien été pris en compte !"),components = [])

                            elif obj==changeName: 
                                await msg.clear_reactions()
                                await msg.edit(embed = discord.Embed(title = args[0] + " : Nom",color = light_blue,description = f"Ecrivez le nom de votre personnage :\n\nVous ne pourrez pas modifier le nom de votre personnage par la suite"))
                                timeout = False
                                
                                try:
                                    respond = await bot.wait_for("message",timeout = 60,check = checkIsAuthorReact)
                                except:
                                    timeout = True

                                if not(timeout):    
                                    user.name = respond.content
                                    user.otherInventory.remove(changeName)

                                    try:
                                        await respond.delete()
                                    except:
                                        print("Il me manque la permission de supprimer des messages")

                                    saveCharFile(pathUserProfile,user)
                                    await msg.clear_reactions()
                                    await msg.edit(embed = discord.Embed(title="Changement de nom",color = user.color,description="Votre changement a bien été pris en compte !"))
                                else:
                                    await msg.add_reaction('🕛')
                
                            elif obj==restat:
                                await msg.clear_reactions()
                                restats(user)
                                user.otherInventory.remove(restat)

                                saveCharFile(pathUserProfile,user)
                                await msg.clear_reactions()
                                await msg.edit(embed = discord.Embed(title="Rénitialisation des points bonus",color = user.color,description=f"Votre changement a bien été pris en compte !\nVous avez {user.points} à distribuer avec la commande \"points\""))

                            elif obj==customColor:
                                user = await changeCustomColor(bot,msg,ctx,user,args)
                                if user != None:
                                    user.otherInventory.remove(customColor)
                                    saveCharFile(pathUserProfile,user)
                                    await msg.clear_reactions()
                                    await msg.edit(embed = discord.Embed(title="Couleur personnalisée",description="Votre couleur a bien été enregistrée\n\nCelle-ci sera appliquée à votre icone lors de sa prochaine modification",color=user.color))
                else:
                    await ctx.channel.send(embed = errorEmbed(args[0],"Rien de trouvé, désolé"))
        else:
            await ctx.channel.send(embed = errorEmbed(args[0],f"{ctx.mentions[0].name} ne vous a pas donné procuration sur son inventaire"))