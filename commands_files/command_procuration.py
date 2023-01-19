import discord, os
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from commands_files.alice_stats_endler import aliceStatsDb
from asyncio import sleep
from interactions import *

async def procuration(ctx : interactions.Message,toProcur:interactions.User):
    if os.path.exists("./userProfile/" + str(ctx.author.id) + ".prof"):
        user = loadCharFile("./userProfile/" + str(ctx.author.id) + ".prof")
        user.procuration.append(toProcur.id)
        user2 = loadCharFile("./userProfile/" + str(toProcur.id) + ".prof")
        user2.haveProcurOn	.append(user.owner)

        try:
            saveCharFile(user=user)
            saveCharFile(user=user2)
            await ctx.send(f"{toProcur.name} à bien été rajouté à la liste des personnes ayant procuration sur votre inventaire")
        except:
            await ctx.send(embeds = errorEmbed("Procuration","Une erreure est survenue"))

    else:
        await ctx.send(embeds = errorEmbed("Procuration","Vous n'avez pas commencé l'aventure"))

noneSuffisantJetonButton = interactions.Button(type=2, style=ButtonStyle.SECONDARY, label="Vous ne possédez pas de jetons", emoji=getEmojiObject('<:jeton:917793426949435402>'),disabled=True)
randomRouletteMsg = [
    "Les jeux sont fait, rien ne va plus !",
    "Tenter le diable",
    "Tentons le diable !",
    "Je sens que la chance est de mon côté !",
]

async def roulette(bot: interactions.Client, ctx: interactions.Message, user: char):
    userJetonsCount = aliceStatsDb.getUserJetons(user)
    baseDesc = """\nLa roulette est un moyen supplémentaire d'obtenir des équipements ou de l'argent.\nAprès chaque combat, si le lanceur n'a pas réussi à obtenir quelque chose après une victoire, il a une probabilité d'obtenir un __<:jeton:917793426949435402> Jeton de Roulette__, nécessaire pour pouvoir lancer celle dernière.\n\nLes objets obtenables dans la roulette sont les mêmes que ceux disponibles dans le magasin et en butin. Leurs probabilités d'appararition dépend du pourcentage d'objet obtenu :\n<:coins:862425847523704832>, <:blocked:897631107602841600>, <:blocked:897631107602841600>, <:blocked:897631107602841600>, <:blocked:897631107602841600> : < 25%\n<:coins:862425847523704832>, <:coins:862425847523704832>, <:blocked:897631107602841600>, <:blocked:897631107602841600>, <:blocked:897631107602841600> : 25% -> 50%\n<:coins:862425847523704832>, <:coins:862425847523704832>, <:coins:862425847523704832>, <:blocked:897631107602841600>, <:blocked:897631107602841600> : 50% -> 75%\n<:coins:862425847523704832>, <:coins:862425847523704832>, <:coins:862425847523704832>, <:coins:862425847523704832>, <:blocked:897631107602841600> : 75% -> 100%\n<:coins:862425847523704832>, <:coins:862425847523704832>, <:coins:862425847523704832>, <:coins:862425847523704832>, <:coins:862425847523704832> : 100%\n\nIl n'est pas possible d'obtenir des objets déjà aquis dans la roulette. La quantité de pièces obtenue est égale au prix d'un équipement obtenable.\n\nVous possédez **{0} __<:jeton:917793426949435402> Jeton de Roulette__**""".format(userJetonsCount)

    emb = interactions.Embed(title="__Roulette :__",color=light_blue,description=baseDesc)
    if userJetonsCount == 0:
        await ctx.send(embeds=emb,components=[interactions.ActionRow(components=[noneSuffisantJetonButton])])
        return 0

    if userJetonsCount >= 3:
        allButon = [interactions.ActionRow(components=[interactions.Button(type=2, style=ButtonStyle.SECONDARY,label="Utiliser tous vos jetons",emoji=getEmojiObject('<:jeton:917793426949435402>'),custom_id="all")])]
    else:
        allButon = []

    button = interactions.Button(type=2, style=ButtonStyle.PRIMARY,label=randomRouletteMsg[random.randint(0,len(randomRouletteMsg)-1)],emoji=getEmojiObject('<:jeton:917793426949435402>'),custom_id="go")

    msg = await ctx.send(embeds=emb,components=[interactions.ActionRow(components=[button])]+allButon)

    def check(m):
        return int(m.author.id) == int(ctx.author.id)

    try:
        react = await bot.wait_for_component(msg,check=check,timeout=60)
    except:
        await msg.edit(embeds=emb,components=[])
        return 0

    if react.custom_id == "go":
        aliceStatsDb.updateJetonsCount(user,-1)
        gettenShop = userShopPurcent(user)
        if gettenShop < 25:
            toGet = [False,True,True,True,True]
        elif gettenShop < 50:
            toGet = [False,False,True,True,True]
        elif gettenShop < 75:
            toGet = [False,False,False,True,True]
        elif gettenShop < 100:
            toGet = [False,False,False,False,True]
        else:
            toGet = [False,False,False,False,False]
        noneAllreadyGet = []
        for b in listAllBuyableShop:
            if not(user.have(obj=b)):
                noneAllreadyGet.append(b)
                if type(b) == stuff and b.minLvl//5 == user.level//5:
                    noneAllreadyGet.append(b)
                    noneAllreadyGet.append(b)

        coinsList=['<:mehPileOfCoins:918042096076722197>','<:goodPileOfCoins:918042081224716309>','<:multiplesCoins:918042117899681792>','<a:rotativeYPositiveCoin:917927342918221865>','<a:rotatingPositiveXCoin:917927242888269864>']
        bigRolly = []
        for a in toGet:
            if a:
                bigRolly.append(noneAllreadyGet[random.randint(0,len(noneAllreadyGet)-1)])
            else:
                bigRolly.append(listAllBuyableShop[random.randint(0,len(listAllBuyableShop)-1)].price)

        possibleGainList = "__Liste des possibles gains :__"
        for a in range(len(bigRolly)):
            if type(bigRolly[a]) == int:
                possibleGainList += "\n{1} : {0} <:coins:862425847523704832>".format(bigRolly[a],coinsList[a])
            else:
                possibleGainList += "\n{0} : {1}".format(bigRolly[a].emoji,bigRolly[a].name)

        gain = random.randint(0,4)

        listPossibleEmojis=["<a:giveup:902383022354079814>",'<a:CHAOS:762276118224961556>','<a:spamton:892749040205316138>','<:ConfusedStonks:782072496693706794>','<a:menacing:917007335220711434>','<a:PhoenixMarteauPiqueur:800831991389749249>','<:descartes:885240392860188672>']
        for cmpt in range(len(listPossibleEmojis)):
            listPossibleEmojis.append('<:em:866459463568850954>')
        if random.randint(0,99) == 66:
            listPossibleEmojis.append('<a:lostSilver:917783593441456198>')

        hidden = "\n"

        whereToHide = random.randint(0,8)
        for cmpt in (0,1,2,3,4,5,6,7,8):
            if cmpt == whereToHide:
                if type(bigRolly[gain]) == int:
                    hidden += "||{0}||".format(coinsList[gain])
                else:
                    hidden += "||{0}||".format(bigRolly[gain].emoji)
            else:
                hidden += "||{0}||".format(listPossibleEmojis[random.randint(0,len(listPossibleEmojis)-1)])
            if cmpt in [2,5]:
                hidden += "\n"

        user = loadCharFile("./userProfile/{0}.prof".format(user.owner))
        if type(bigRolly[gain]) == weapon:
            user.weaponInventory += [bigRolly[gain]]
        elif type(bigRolly[gain]) == skill:
            user.skillInventory += [bigRolly[gain]]
        elif type(bigRolly[gain]) == stuff:
            user.stuffInventory += [bigRolly[gain]]
        else:
            user.currencies += bigRolly[gain]

        saveCharFile("./userProfile/{0}.prof".format(user.owner),user)

        hidden += "\n\nVotre gain a été ajouté à votre inventaire"
        await msg.edit(embeds=interactions.Embed(title="__Roulette :__",color=light_blue,description=possibleGainList+"\n\n"+"__Découvrez ce que vous avez gagné :__\n"+hidden),components=[])
        await sleep(60)
        await msg.edit(embeds=interactions.Embed(title="__Roulette :__",color=light_blue,description=possibleGainList+"\n\n"+"__Découvrez ce que vous avez gagné :__\n"+hidden.replace("||","")),components=[])
    else:
        await msg.edit(embeds= await getRandomStatsEmbed(bot,[user],text="Utilisation de tous vos jetons... (Reste encore {0} jetons)".format(aliceStatsDb.getUserJetons(user))),components=[])
        now = datetime.now()
        allGains, coinGain = [], 0
        while aliceStatsDb.getUserJetons(user) > 0:
            if datetime.now() > now + timedelta(seconds=3):
                await msg.edit(embeds= await getRandomStatsEmbed(bot,[user],text="Utilisation de tous vos jetons... (Reste encore {0} jetons)".format(aliceStatsDb.getUserJetons(user))),components=[])
                now = datetime.now()
            user = loadCharFile("./userProfile/{0}.prof".format(user.owner))
            aliceStatsDb.updateJetonsCount(user,-1)
            gettenShop = userShopPurcent(user)
            if gettenShop < 25:
                toGet = [False,True,True,True,True]
            elif gettenShop < 50:
                toGet = [False,False,True,True,True]
            elif gettenShop < 75:
                toGet = [False,False,False,True,True]
            elif gettenShop < 100:
                toGet = [False,False,False,False,True]
            else:
                toGet = [False,False,False,False,False]

            noneAllreadyGet = []
            for b in listAllBuyableShop:
                if not(user.have(obj=b)):
                    noneAllreadyGet.append(b)
                    if type(b) == stuff and b.minLvl//5 == user.level//5:
                        noneAllreadyGet.append(b)
                        noneAllreadyGet.append(b)

            bigRolly = []
            for a in toGet:
                if a:
                    bigRolly.append(noneAllreadyGet[random.randint(0,len(noneAllreadyGet)-1)])
                else:
                    bigRolly.append(listAllBuyableShop[random.randint(0,len(listAllBuyableShop)-1)].price)
            gain = random.randint(0,4)
            user = loadCharFile("./userProfile/{0}.prof".format(user.owner))
            if type(bigRolly[gain]) == weapon:
                user.weaponInventory += [bigRolly[gain]]
            elif type(bigRolly[gain]) == skill:
                user.skillInventory += [bigRolly[gain]]
            elif type(bigRolly[gain]) == stuff:
                user.stuffInventory += [bigRolly[gain]]
            else:
                user.currencies += bigRolly[gain]

            if type(bigRolly[gain]) == int:
                coinGain += bigRolly[gain]
            else:
                allGains.append(bigRolly[gain])

            saveCharFile("./userProfile/{0}.prof".format(user.owner),user)

        toSend = "\n{0} <:coins:862425847523704832>".format(coinGain)
        for a in allGains:
            toSend += "\n{1} {0}".format(a.name,a.emoji)

        if len(toSend) > 4000:
            toSend = "\n{0} pièces".format(coinGain)
            for b in allGains:
                tempName, temp = "",""
                for letter in unhyperlink(b.name+" "):
                    if letter == " ":
                        if len(temp) > 4:
                            tempName += " {0}.".format(temp[:3])
                        else:
                            tempName += " {0}".format(temp[:4])
                        temp = ""
                    else:
                        temp += letter
                tempName += temp

                toSend += "\n {0}".format(tempName)

        await msg.edit(embeds=interactions.Embed(title="__Roulette :__",color=light_blue,description="__Vous avez obtenus :__"+toSend),components=[])

async def seeAllInfo(bot:interactions.Client, user:char)-> interactions.Embed:
    desc = ""
    try:            # User owner
        owner = await get(bot, interactions.User, object_id=user.owner)
        desc += "__Compte associé :__ {0}\n".format(owner.mention)
    except:
        desc += "`Le compte associé n'a pas pu être récupéré`\n"

    desc += "__Nom :__ {0}, __Niveau :__ {1}<:littleStar:925860806602682369>{2}, __Exp :__ {3}, __Argent :__ {4}\n".format(user.name,user.level,user.stars,user.exp,user.currencies)
    desc += "__Espèce :__ {0}, __Couleur :__ {1}, __Hexa :__ {2}, __Forme d'icone :__ {3}\n".format(['<:ikaLBlue:866459302319226910>','<:takoLBlue:866459095875190804>'][user.species-1],user.color,user.colorHex,['<:spIka:866465882540605470>','<:komoriOut:930798849969246208>','<:birdOut:930906560811646996>','<:outSkeleton:930910463951249479>'][user.iconForm])
    emb = interactions.Embed(title="Page de {0}".format(user.name),color=user.color,description=desc)
    emb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(await getUserIcon(bot,user)).id))

    tablSays = user.says.tabl()
    tempSays = ""

    for cmpt in range(len(tablSays)):
        tempReplace = {"Réaction":"Réac.","Victoire":"Vic.","Défaite":"Déf.","réanimation":"réa.","élimination":"élim."}
        tempCatCmpp, tempo = tablCat[cmpt], tablSays[cmpt]
        for a in tempReplace:
            tempCatCmpp = tempCatCmpp.replace(a,tempReplace[a])

        if tempo == None:
            tempo = "-"
        elif len(tempo) > 30:
            tempo = tempo[:30]+"(...)"

        tempSays += "{0} : {1}\n".format(tempCatCmpp,tempo)
    
    emb.add_field(name="__Blablator :__",value=tempSays)
    return emb

async def userSettings(bot:interactions.Client, user:char, ctx:interactions.CommandContext):
    msg, state = None, 0
    while 1:
        user = loadCharFile(user=user)
        userIcon = await getUserIcon(bot,user)

        if state == 0:
            typeIA = "Personnalisée"
            for presetIA1 in preDefCharSet:
                if user.aspiration in presetIA1[0]:
                    for presetIA2 in presetIA1[1]:
                        if user.charSettings == presetIA2[2]:
                            typeIA = presetIA2[0]
                            break
            emb = interactions.Embed(title="__Paramètres de personnage :__",color=user.color,description="__**Type d'IA** :__ {0}".format(typeIA))
            temp = ""
            for cmpt in range(len(charsetCatNamesUse)):
                temp += "__{0} :__ {1}\n".format(charsetCatNamesUse[cmpt],skillProbTxt[user.charSettings[charsetUseNames[cmpt]]])
            emb.add_field(name="__Utilisations des moyens :__",value=temp,inline=False)
            temp = ""
            for cmpt in range(len(charsetCatNamesTarget)):
                temp += "__{0} :__ {1}\n".format(charsetCatNamesTarget[cmpt],charsetTargetOptions[cmpt][user.charSettings[charsetTargetsNames[cmpt]]])
            emb.add_field(name="<:em:866459463568850954>\n__Cibles Priviligiés :__",value=temp,inline=False)

            temp, iconSet, iconSetNames, iconSetOption = "", [user.handed,user.showElement,user.showWeapon,user.showAcc], ["Main dominante","Elément","Arme","Accessoire"], [["Gauche","Droite"],["Masqué","Affiché"],["Masquée","Affichée"],["Masqué","Affiché"]]
            for cmpt in range(len(iconSet)):
                temp += "__{0} :__ {1}\n".format(iconSetNames[cmpt],iconSetOption[cmpt][iconSet[cmpt]])
            emb.add_field(name="<:em:866459463568850954>\n__Paramètres d'icon :__",value=temp,inline=False)
            emb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(userIcon).id))

            changeIAOptions = interactions.ActionRow(components=[interactions.SelectMenu(custom_id = "changeIaSelect", options=[
                interactions.SelectOption(label="Modifier l'IA",value="changeIA",description="Permet de sélectionner une IA prédéfinie ou de changer ses paramètres d'IA"),
                interactions.SelectOption(label="Modifier l'Icone",value="changeIcon",description="Permet de modifier certains paramètres de votre icon")
                ],placeholder="Modifier des paramètres")])
            if msg == None:
                try:
                    msg = await ctx.send(embeds=emb, components=[changeIAOptions])
                except:
                    msg = await ctx.channel.send(embeds=emb, components=[changeIAOptions])
            else:
                await msg.edit(embeds=emb, components=[changeIAOptions])       
            
            def check(m):
                return m.author.id == ctx.author.id
            rep = None
            try:
                rep = await bot.wait_for_component(msg,changeIAOptions,check,60)
            except asyncio.TimeoutError:
                await msg.edit(embeds=emb, components=[])
                return 1

            rep = rep.data.values[0]

            if rep == "changeIcon":
                state = 1
            elif rep == "changeIA":
                temp = ""
                selectIAOptions = []
                for roleIA in preDefCharSet:
                    if user.aspiration in roleIA[0]:
                        for cmpt in range(len(roleIA[1])):
                            presetIA = roleIA[1][cmpt]
                            temp += "__**{0}**__\n> - {1}\n\n".format(presetIA[0],presetIA[1].replace("\n","\n> -"))
                            selectIAOptions.append(interactions.SelectOption(presetIA[0],str(cmpt)))
                        break
                
                selectIAOptions.append(interactions.SelectOption(label="Personnaliser",value="-1"))
                selectIAOptions.append(interactions.SelectOption(label="Retour",value="-2"))
                emb = interactions.Embed(title="__Paramètres de Personnage__",color=user.color,description="__Paramètres Prédéfinies :__\n"+temp)
                selectIA = interactions.ActionRow(components=[interactions.SelectMenu(custom_id = "selectIASelect", options=selectIAOptions,placeholder="Choisir une IA Préféfinie pour personnaliser la sienne")])

                await msg.edit(embeds=emb,components=[selectIA])

                try:
                    rep = await bot.wait_for_component(msg,selectIA,check,timeout=60)
                except asyncio.TimeoutError:
                    await msg.edit(embeds=emb,components=[])             
                
                rep = int(rep.data.values[0])
                if rep >= 0:
                    for roleIA in preDefCharSet:
                        if user.aspiration in roleIA[0]:
                            print(roleIA[1][rep][0])
                            user.charSettings = roleIA[1][rep][2]
                            saveCharFile(user=user)
                            break
                elif rep == -2:
                    pass
                elif rep == -1:
                    while 1:
                        emb = interactions.Embed(title="__Paramètres de personnage :__",color=user.color,description="__**Type d'IA** :__ {0}".format(typeIA))
                        temp = ""
                        for cmpt in range(len(charsetCatNamesUse)):
                            temp += "__{0} :__ {1}\n".format(charsetCatNamesUse[cmpt],skillProbTxt[user.charSettings[charsetUseNames[cmpt]]])
                        emb.add_field(name="__Utilisations des moyens :__",value=temp,inline=False)
                        temp = ""
                        for cmpt in range(len(charsetCatNamesTarget)):
                            temp += "__{0} :__ {1}\n".format(charsetCatNamesTarget[cmpt],charsetTargetOptions[cmpt][user.charSettings[charsetTargetsNames[cmpt]]])
                        emb.add_field(name="<:em:866459463568850954>\n__Cibles Priviligiés :__",value=temp,inline=False)
                        emb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(userIcon).id))
                        selectIAOptions = []
                        for cmpt in range(len(charsetCatNamesUse)):
                            selectIAOptions.append(interactions.SelectOption(label="Utilisation "+charsetCatNamesUse[cmpt],value=str(cmpt),description=skillProbTxt[user.charSettings[charsetUseNames[cmpt]]]))
                        for cmpt in range(len(charsetCatNamesTarget)):
                            selectIAOptions.append(interactions.SelectOption(label="Cible "+charsetCatNamesTarget[cmpt],value=str(cmpt+len(charsetCatNamesUse)),description=charsetTargetOptions[cmpt][user.charSettings[charsetTargetsNames[cmpt]]]))

                        selectIAOptions.append(interactions.SelectOption(label="Retour",value = str(-1)))
                        selectIA = interactions.ActionRow(components=[interactions.SelectMenu(custom_id = "selectIASelectMenu", options=selectIAOptions,placeholder="Choisissez une catégorie à modifier")])
                        await msg.edit(embeds=emb,components=[selectIA])

                        try:
                            rep3 = await bot.wait_for_component(msg,selectIA,check,60)
                        except asyncio.TimeoutError:
                            await msg.edit(embeds=emb,components=[])
                            rep = -2
                            break

                        rep3 = int(rep3.data.values[0])
                        if rep3 == -1:
                            break
                        elif rep3 < len(charsetCatNamesUse):
                            desc = "__Utilisation **{0}**__ :\n> - {1}\n> - {2}\n> - {3}".format(charsetCatNamesUse[rep3],skillProbTxt[0],skillProbTxt[1],skillProbTxt[2])
                            selectIAOptions = []
                            for cmpt in range(len(skillProbTxt)):
                                selectIAOptions.append(interactions.SelectOption(skillProbTxt[cmpt],str(cmpt)))
                            
                            selectIA = interactions.ActionRow(components=[interactions.SelectMenu(custom_id = "selectIATheThird", options=selectIAOptions,placeholder="Choissez un paramètre")])
                            await msg.edit(embeds=interactions.Embed(title="__Paramètres de personnage__",description=desc,color=user.color),components=[selectIA])

                            try:
                                rep2 = await bot.wait_for_component(msg,selectIA,check,60)
                            except asyncio.TimeoutError:
                                await msg.edit(embeds=emb,components=[])
                                break

                            user.charSettings[charsetUseNames[rep3]] = int(rep2.data.values[0])
                            saveCharFile(user=user)
                        else:
                            rep3 -= len(charsetCatNamesUse)
                            desc = "__Cible **{0}**__ :".format(charsetCatNamesTarget[rep3])
                            selectIAOptions = []
                            for cmpt in range(len(charsetTargetOptions[rep3])):
                                selectIAOptions.append(interactions.SelectOption(charsetTargetOptions[rep3][cmpt],str(cmpt)))
                                desc += "\n> - {0}".format(charsetTargetOptions[rep3][cmpt])
                            
                            selectIA = interactions.ActionRow(components=[interactions.SelectMenu(custom_id = "anotherSelectIA", options=selectIAOptions,placeholder="Choissez un paramètre")])
                            await msg.edit(embeds=interactions.Embed(title="__Paramètres de personnage__",description=desc,color=user.color),components=[selectIA])

                            try:
                                rep2 = await bot.wait_for_component(msg,selectIA,check,60)
                            except asyncio.TimeoutError:
                                await msg.edit(embeds=emb,components=[])
                                break

                            user.charSettings[charsetTargetsNames[rep3]] = int(rep2.data.values[0])
                            saveCharFile(user=user)

        elif state == 1:
            desc = "__Main dominante :__ {0}\n__Aff. élément :__ {1}\n__Aff. arme :__ {2}\n__Aff. accessoire :__ {3}".format(["Gauche","Droite"][user.handed],["Non","Oui"][user.showElement],["Non","Oui"][user.showWeapon],["Non","Oui"][user.showAcc])

            boutonHand = interactions.Button(type=2, style=2, label=["Main droite","Main gauche"][user.handed],custom_id="hand")
            boutonElem = interactions.Button(type=2, style=[ButtonStyle.PRIMARY,2][user.showElement],label=["Afficher l'élément","Cacher l'élément"][user.showElement],custom_id="elem")
            boutonArme = interactions.Button(type=2, style=[ButtonStyle.PRIMARY,2][user.showWeapon],label=["Afficher l'arme","Cacher l'arme"][user.showWeapon],custom_id="weap")
            boutonAcc = interactions.Button(type=2, style=[ButtonStyle.PRIMARY,2][user.showAcc],label=["Afficher l'accessoire","Cacher l'accessoire"][user.showAcc],custom_id="acc")
            boutonReturn = interactions.Button(type=2, style=2,label="Retour",custom_id="back")
            actionRow = [interactions.ActionRow(components=[boutonHand,boutonElem,boutonArme,boutonAcc,boutonReturn])]

            emb = interactions.Embed(title="__User Settings__",description=desc,color=user.color).set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(userIcon).id))
            await msg.edit(embeds=emb,components=actionRow)

            def check(m):
                return int(m.author.id) == int(ctx.author.id)

            try:
                react = await bot.wait_for_component(messages=msg,check=check,timeout=30)
            except:
                await msg.edit(embeds=emb,components=[])
                return 0

            if react.custom_id != "back":
                await msg.edit(embeds=interactions.Embed(title="__User Settings__",description=desc,color=user.color).set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(userIcon).id)),components=[interactions.ActionRow(components=[interactions.Button(type=2, style=2,label="Chargment...",emoji=getEmojiObject('<a:loading:862459118912667678>'),value="loading",disabled=True)])])
                tablTemp, tablTempId = [user.handed,user.showElement,user.showWeapon,user.showAcc], ["hand","elem","weap","acc"]
                for cmpt in range(4):
                    if react.custom_id == tablTempId[cmpt]:
                        tablTemp[cmpt] = [not(tablTemp[cmpt]),int(not(bool(tablTemp[cmpt])))][cmpt == 0]

                user.handed,user.showElement,user.showWeapon,user.showAcc = tablTemp[0],tablTemp[1],tablTemp[2],tablTemp[3]

                saveCharFile(user=user)
                await makeCustomIcon(bot,user)
            else:
                state = 0
