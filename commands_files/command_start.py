import interactions
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from commands_files.alice_stats_endler import aliceStatsDb
from advObjects.advChips import chip

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
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".json"
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
        still, user, msg = True, char(ctx.author.id), await loadingSlashEmbed(ctx)

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
                try:
                    saveCharFile(pathUserProfile,user)
                    aliceStatsDb.addUser(user)
                    desc = "Vous avez terminé la création de votre personnage ! Rassurez-vous, vous pourrez modifier les paramètres renseignés au moyen d'objet spéciaux disponibles dans le shop.\n\nVoici quelques objets pour fêter votre recrutement :"
                    for obj in baseWeapon+baseSkills+baseStuffs:
                        desc += "\n{0}".format(obj)
                        if obj in [baseWeapon[-1],baseSkills[-1],baseStuffs[-1]]: desc += "\n"
                    desc += "\nPourquoi ne pas faire un tour vers **/inventory** pour voir ça ?"

                    await msg.edit(embeds = interactions.Embed(title = "__/start__", color= user.color, description=desc),components=[])
                except Exception as e:
                    await msg.edit(embeds = interactions.Embed(title = "__/start__", color= red, description = "Un truc c'est mal passé, l'aventure attendra"))
                    print_exc()
                    os.remove(pathUserProfile)
            else:
                still = False

        if not(still):
            await msg.edit(embeds= errorEmbed("__/start__","Commande annulée (timeout)"))
    else:
        await ctx.send(embeds=errorEmbed("__/start__","Vous avez déjà commencé l'aventure"),ephemeral=True)

async def functionVerifUnusedEmoji(bot: interactions.Client, ctx: interactions.SlashContext):
    msg = await ctx.send(embeds=loadingEmbed("Obtention de la liste des émojis..."))

    async def modifMsg(text:str):
        await msg.edit(embeds=loadingEmbed(text))

    listException: List[str] = ["<:timeoB:1104517210728308746>","<:smallClemence:1236329023219437630>","<:oceane:1218268649564143707>","<:glan:1218268667960098879>","<:pirSab1:1059519845177249812>","<:pirGun1:1059519820376330351>","<:pirGun2:1059519760284528640>","<:stimeo:1089164206336647168>","<:itimeo:1103217741172846614>","<:stimeo:1089164206336647168>","<:itimeo:1103217741172846614>","<:dreamSixtine:1100793996483235851>","<:catIli:1006440617146060850>","<:childIli:1089607519380443229>","<:miniIli:1089607564548898876>","<:gaurora:1103332091594281050>","<:penelope:1178446515459588106>", "<:lei:1257691823170785372>","<:silicia:1045109225615003729>", "<:airNacia:1208074166297952278>", "<:fireNacia:1208074195888504902>", "<:waterNacia:1208074216973410405>", "<:earthNacia:1208074102569566209>","<:anais:1166806279042375780>","<:isa:1158136337061400797>","<:batiste:1203788655240679534>","<:kaleb:1183176411452813433>","<:keuleyong:1205465540337078292>"]
    listEmojisId: List[int] = []
    for tmpStr in listException: listEmojisId.append(int(getEmojiObject(tmpStr).id))
    
    listAll: List[Union[classes.skill,classes.weapon,classes.stuff,classes.tmpAllie,classes.octarien]] = skills+stuffs+weapons+tablAllAllies+tablVarAllies+tablUniqueEnnemies+tablBoss+tablRaidBoss+tablBossPlus+chipList+invocTabl
    tablRawestSkill = []
    tablSkills: List[Union[classes.skill,classes.weapon,classes.stuff]] = []
    for tmpObject in listAll:
        match type(tmpObject):
            case classes.skill: tablRawestSkill.append(tmpObject)
            case classes.weapon: tablSkills.append(tmpObject)
            case classes.stuff: tablSkills.append(tmpObject)
            case classes.tmpAllie:
                listEmojisId.append(int(getEmojiObject(tmpObject.icon).id))
                tablSkills.append(tmpObject.weapon)
                tablRawestSkill = tablRawestSkill + tmpObject.skills
                if tmpObject.splashIcon != None: listEmojisId.append(int(getEmojiObject(tmpObject.splashIcon).id))
                if tmpObject.changeDict != None:
                    for tmpDict in tmpObject.changeDict:
                        if tmpDict.skills != None: tablRawestSkill = tablRawestSkill + tmpDict.skills
                        if tmpDict.icon != None: listEmojisId.append(int(getEmojiObject(tmpDict.icon).id))
                        if tmpDict.splashIcon != None: listEmojisId.append(int(getEmojiObject(tmpDict.splashIcon).id))
            case classes.octarien:
                listEmojisId.append(int(getEmojiObject(tmpObject.icon).id))
                tablRawestSkill = tablRawestSkill + tmpObject.skills
                tablSkills.append(tmpObject.weapon)
                if tmpObject.splashIcon != None: listEmojisId.append(int(getEmojiObject(tmpObject.splashIcon).id))
            case classes.invoc:
                listEmojisId.append(int(getEmojiObject(tmpObject.icon[0]).id)); listEmojisId.append(int(getEmojiObject(tmpObject.icon[1]).id))
                tablRawestSkill = tablRawestSkill + tmpObject.skills
                tablSkills.append(tmpObject.weapon)
            case _:
                if type(tmpObject) == chip: tablSkills.append(tmpObject)

    tablRawerSkill = []
    for tmpObject in tablRawestSkill:
        if type(tmpObject) == classes.skill:
            if tmpObject.become == None: tablRawerSkill.append(tmpObject)
            else: tablRawerSkill = tablRawerSkill + tmpObject.become + [tmpObject]
        elif tmpObject == None: pass
    
    for tmpObject in tablRawerSkill:
        if type(tmpObject) == classes.skill:
            tablSkills.append(tmpObject)

            while tmpObject != None and tmpObject.effectOnSelf != None: 
                tmpEff = findEffect(tmpObject.effectOnSelf)
                if tmpEff != None and tmpEff.replica != None: 
                    tmpObject = findSkill(tmpEff.replica)
                    tablSkills.append(tmpObject)
                else: break

    tablSkills = set(tablSkills)
    for tmpObject in tablSkills:
        if type(tmpObject) in [classes.weapon, classes.stuff]:
            listEmojisId.append(int(getEmojiObject(tmpObject.emoji).id))
            if tmpObject.effects != None: 
                tmpEff = findEffect(tmpObject.effects)
                if tmpEff != None:
                    for tmpEm in set(tmpEff.emoji[0]+tmpEff.emoji[1]+tmpEff.emoji[2]): 
                        if tmpEm != None: listEmojisId.append(int(getEmojiObject(tmpEm).id))
            if type(tmpObject) == classes.weapon and tmpObject.effectOnUse != None: 
                tmpEff = findEffect(tmpObject.effectOnUse)
                if tmpEff != None:
                    for tmpEm in set(tmpEff.emoji[0]+tmpEff.emoji[1]+tmpEff.emoji[2]): 
                        if tmpEm != None: listEmojisId.append(int(getEmojiObject(tmpEm).id))
        elif type(tmpObject) == chip:
            if tmpObject.emoji != "" : listEmojisId.append(int(getEmojiObject(tmpObject.emoji).id))
        elif type(tmpObject) == classes.skill:
            tmp = getEmojiObject(tmpObject.emoji).id
            if tmp != None: listEmojisId.append(int(tmp))
            else: print(tmpObject.name)
            
            tablEffToSee: List[classes.effect] = []
            if tmpObject.effects != None: tablEffToSee = tablEffToSee+tmpObject.effects
            if tmpObject.effectAroundCaster != None and type(tmpObject.effectAroundCaster[2]) == classes.effect: tablEffToSee.append(tmpObject.effectAroundCaster[2])
            if tmpObject.effectOnSelf != None: tablEffToSee.append(tmpObject.effectOnSelf)
            if tmpObject.jaugeEff != None: tablEffToSee.append(tmpObject.jaugeEff)

            for tmpEff in flatList(tablEffToSee):
                tmpEff2 = findEffect(tmpEff)
                if tmpEff2 != None:
                    for tmpEm in set(tmpEff2.emoji[0]+tmpEff2.emoji[1]+tmpEff2.emoji[2]):
                        if tmpEm != None:
                            tmp = getEmojiObject(tmpEm).id
                            if tmp != None: listEmojisId.append(int(tmp))
                            else: print(tmpEm)

                    if tmpEff2.jaugeValue != None:
                        for tmpEm in tmpEff2.jaugeValue.emoji[0]+tmpEff2.jaugeValue.emoji[1]:
                            if tmpEm != None: listEmojisId.append(int(getEmojiObject(tmpEm).id))
                    while tmpEff2 != None and tmpEff2.callOnTrigger != None:
                        for tmpEm in set(tmpEff2.emoji[0]+tmpEff2.emoji[1]+tmpEff2.emoji[2]):
                            if tmpEm != None:
                                tmp = getEmojiObject(tmpEm).id
                                if tmp != None: listEmojisId.append(int(tmp))
                        tmpEff2 = findEffect(tmpEff2.callOnTrigger)
                elif tmpEff != None : print(tmpObject.name, type(tmpEff))
  
    listEmojisId = list(set(listEmojisId))
    await modifMsg("Vérification des emojis non utlisés... (0%) {1}\nNombre d'émojis utilisés : {0}".format(len(listEmojisId), "\."*100))
    guildList: List[interactions.Guild] = bot.guilds
    dictUnusedGuilds, listExcludedGuilds, cmpt, cmpt2, lenGuildList = {}, LenaCustomIcons+ShushyCustomIcons+[1171852774217093120,1137363859410264065,1013740566602846248,932941135276560455,894528703185424425,810212019608485918,916120008948600872,1044487484786094120,887846876114739261], 0, 1, len(guildList)
    for temp in guildList:
        if temp.name.startswith("Lenapy") and int(temp.id) not in listExcludedGuilds:
            emojiList = await temp.fetch_all_custom_emojis()
            for tmpEmoji in emojiList:
                if int(tmpEmoji.id) not in listEmojisId:
                    if temp in dictUnusedGuilds.keys(): dictUnusedGuilds[temp].append(tmpEmoji)
                    else: dictUnusedGuilds[temp] = [tmpEmoji]
        cmpt += 1
        if cmpt > lenGuildList//10*cmpt2:
            cmpt2, purcent, tmp = cmpt2+1, round(cmpt/lenGuildList*100,2), ""
            tmp = "\|"*int(purcent)
            while len(tmp) < 200: tmp+="\."
            await modifMsg("Vérification des emojis non utlisés... ({1}%) {2}\nNombre d'émojis utilisés : {0}".format(len(listEmojisId),purcent,tmp))

    totalLenUnused, listField = 0, []
    for tmpGuild, emojiList in dictUnusedGuilds.items():
        tempValue = ""
        for tmpEmoji in emojiList: totalLenUnused += 1; tempValue += "<:{0}:{1}> {0}\n".format(tmpEmoji.name,tmpEmoji.id)
        try: listField.append(EmbedField(name=tmpGuild.name + " ({0})".format(tmpGuild.id),value=reduceEmojiNames(tempValue),inline=True))
        except: print(tmpGuild.name,tmpGuild.id,"\n",tempValue,"=================")

    tmpFieldList, first = [], True
    for tmpField in listField:
        if len(tmpFieldList) >= 9:
            emb = Embed(title="__Vérification des émojis non utilisés__",color=light_blue,description="Nombre d'émojis utlisés : {0}\nNombre d'émojis non utilisés : {1}".format(len(listEmojisId),totalLenUnused),fields=tmpFieldList)
            if first: await msg.edit(embeds=emb); first = False
            else: await msg.channel.send(embeds=emb)
            tmpFieldList = [tmpField]
        else: tmpFieldList.append(tmpField)
