import asyncio, interactions, string
from interactions import ButtonStyle

from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from commands_files.command_start import chooseAspiration,chooseColor,changeCustomColor

ENC_ACC, ENC_GEAR, ENC_SHOE, ENC_WEAP, ENC_SKILL, ENC_ALLIES, ENC_ENEMIES, ENC_BOSS, ENC_LOCKED, ENC_ACHIV = tuple(range(10))
INV_GEAR, INV_WEAPON, INV_SKILL, INV_OBJ, INV_ELEMENT, INV_CHIP = tuple(range(6))

inventoryMenu = interactions.StringSelectMenu([
        interactions.StringSelectOption(label="Inventaire d'Arme",value="0",emoji=getEmojiObject('<:splattershot:866367647113543730>')),
        interactions.StringSelectOption(label="Inventaire de Compétences",value="1",emoji=getEmojiObject('<:splatbomb:873527088286687272>')),
        interactions.StringSelectOption(label="Inventaire d'Equipement",value="2",emoji=getEmojiObject('<:bshirt:867156711251771402>')),
        interactions.StringSelectOption(label="Inventaire d'Objets",value="3",emoji=getEmojiObject('<:changeAppa:872174182773977108>')),
        interactions.StringSelectOption(label="Éléments",value="4",emoji=getEmojiObject('<:krysTal:888070310472073257>'))
        ],
    custom_id = "inventoryFirstMenu",
    placeholder="Sélectionnez l'inventaire dans lequel vous voulez aller"
        )

returnButton = interactions.Button(style=2, label="Retour", emoji=PartialEmoji(name="◀️"), custom_id="return")

changeElemEnable = interactions.Button(style=1, label="Utiliser comme élément principal", emoji=getEmojiObject('<:krysTal:888070310472073257>'), custom_id="change")
changeElemDisabled = interactions.Button(style=1,label="Utiliser comme élément principal",emoji=getEmojiObject('<:krysTal:888070310472073257>'),custom_id="change",disabled=True)
changeElemEnable2 = interactions.Button(style=1,label="Utiliser comme élément principal",emoji=getEmojiObject('<:krysTal2:907638077307097088>'),custom_id="change")
changeElemDisabled2 = interactions.Button(style=1,label="Utiliser comme élément principal",emoji=getEmojiObject('<:krysTal2:907638077307097088>'),custom_id="change",disabled=True)

changeElemEnable3 = interactions.Button(style=1,label="Utiliser comme élément secondaire",emoji=getEmojiObject('<:krysTal:888070310472073257>'),custom_id="change2")
changeElemDisabled3 = interactions.Button(style=1,label="Utiliser comme élément secondaire",emoji=getEmojiObject('<:krysTal:888070310472073257>'),custom_id="change2",disabled=True)
changeElemEnable4 = interactions.Button(style=1,label="Utiliser comme élément secondaire",emoji=getEmojiObject('<:krysTal2:907638077307097088>'),custom_id="change2")
changeElemDisabled4 = interactions.Button(style=1,label="Utiliser comme élément secondaire",emoji=getEmojiObject('<:krysTal2:907638077307097088>'),custom_id="change2",disabled=True)

confirmButton = interactions.Button(style=ButtonStyle.SUCCESS,label="Équiper",emoji=PartialEmoji(name="✅"),custom_id="confirm")
useMimikator = interactions.Button(style=ButtonStyle.SECONDARY,label="Utiliser votre Mimikator",emoji=getEmojiObject(mimique.emoji),custom_id="mimikator")
hideNonEquip = interactions.Button(style=ButtonStyle.PRIMARY,label="Cacher Non équipables",custom_id="hideNoneEquip",emoji=getEmojiObject('<:invisible:899788326691823656>'))
affExclu = interactions.Button(style=ButtonStyle.SUCCESS,label="Afficher Exclusivité",custom_id="affExclu",emoji=getEmojiObject(matriseElemEff.emoji[0][0]))
affNonEquip = interactions.Button(style=2,label="Afficher Non équipables",custom_id="affNoneEquip",emoji=getEmojiObject("<:noeuil:887743235131322398>"))
allType = interactions.Button(style=ButtonStyle.SECONDARY,label="Afficher Tout",custom_id="allDamages",emoji=getEmojiObject('<:targeted:912415337088159744>'))
onlyPhys = interactions.Button(style=ButtonStyle.SUCCESS,label="Physique",custom_id="onlyPhys",emoji=getEmojiObject(mainLibre.emoji))
onlyMag = interactions.Button(style=ButtonStyle.PRIMARY,label="Psychique",custom_id="onlyMag",emoji=getEmojiObject(witchWeapon.emoji))
affAcc = interactions.Button(style=ButtonStyle.SUCCESS,label="Accessoire",emoji=getEmojiObject(amethystEarRings.emoji),custom_id="acc")
affBody = interactions.Button(style=ButtonStyle.SUCCESS,label="Tenue",emoji=getEmojiObject(lightBlueJacket.emoji),custom_id="dress")
affShoes = interactions.Button(style=ButtonStyle.PRIMARY,label="Chaussures",emoji=getEmojiObject(lightBlueFlats.emoji),custom_id="flats")
affAllStuff = interactions.Button(style=2,label="Tout Type",emoji=getEmojiObject('<:dualMagie:899628510463803393>'),custom_id="all")

affCompMelee = interactions.Button(style=ButtonStyle.DANGER,label="Comptétences Mêlée",emoji=getEmojiObject(absorbingStrike.emoji),custom_id="melee_range")
affCompDist = interactions.Button(style=ButtonStyle.DANGER,label="Compétences Distance",emoji=getEmojiObject(absorbingArrow.emoji),custom_id="dist_range")
affAllRange = interactions.Button(style=2,label="Toutes portées",custom_id="all_range")

weapRangeMelee = interactions.Button(style=ButtonStyle.GRAY,label="Mêlée",emoji=getEmojiObject(roller.emoji),custom_id="range_melee")
weapRangeDist = interactions.Button(style=ButtonStyle.GRAY,label="Courte Distance",emoji=getEmojiObject(splattershot.emoji),custom_id="range_dist")
weapRangeLong = interactions.Button(style=ButtonStyle.GRAY,label="Longue Distance",emoji=getEmojiObject(concentraceurZoom.emoji),custom_id="range_long")
weapRangeAll = interactions.Button(style=ButtonStyle.GRAY,label="Toute Portée",emoji=getEmojiObject(elemEmojis[ELEMENT_UNIVERSALIS]),custom_id="range_all")

skillult, skillnonult, skillMono, skillAoe = [], [], [], []
for skilly in skills:
    if skilly.ultimate:
        skillult.append(skilly)
    else:
        skillnonult.append(skilly)
    if skilly.area == AREA_MONO:
        skillMono.append(skilly)
    else:
        skillAoe.append(skilly)

confirmChange = interactions.Button(style=ButtonStyle.SUCCESS,label="Le renouveau c'est cool",emoji=PartialEmoji(name="✅"),custom_id="confirm")
rejectModernity = interactions.Button(style=2,label="Rejeter la modernité",emoji=PartialEmoji(name="❌"),custom_id="nope")

returnAndConfirmActionRow = interactions.ActionRow(returnButton,confirmButton)

def getSortSkillValue(object : skill, wanted : int):
    if wanted in [15,17]:       # Indirect Dmg or Armor
        eff = findEffect(object.effects[0])
        if eff == None:
            eff = findEffect(object.effectOnSelf)
            if (eff == None or (eff != None and eff.type not in [TYPE_INDIRECT_DAMAGE,TYPE_ARMOR])) and object.effectAroundCaster != None:
                eff = findEffect(object.effectAroundCaster[2])
            if eff == None and object.depl != None:
                eff = findEffect(object.depl.skills.effects[0])
        if eff != None:
            if wanted == 15:
                return eff.power * object.effPowerPurcent/100
            elif wanted == 17:
                return eff.overhealth
        else:
            print("{0} n'a rien a faire dans la catégorie {1} !".format(object.name,["Dégâts indirects","Armure"][int(wanted==17)]))
            return 0
    elif wanted == 14:      # Dmg  
        objPower = max(object.power,object.maxPower) * object.repetition
        while not(object.effectOnSelf == None or (type(findEffect(object.effectOnSelf)) == effect and findEffect(object.effectOnSelf).replica == None)):
            object = findSkill(findEffect(object.effectOnSelf).replica)
            objPower += max(object.power,object.maxPower) * object.repetition
        if object.type == TYPE_DAMAGE:
            return objPower
        elif object.effectAroundCaster != None:
            return object.effectAroundCaster[2]

    elif wanted == 16:  # Heal
        if object.effects[0] == None:
            while not(object.effectOnSelf == None or findEffect(object.effectOnSelf).replica == None):
                object = findSkill(findEffect(object.effectOnSelf).replica)
            return object.power
        else:
            if object.effects[0] != None:
                return findEffect(object.effects[0]).power
            elif object.effectOnSelf != None:
                return findEffect(object.effectOnSelf).power
            elif object.effectAroundCaster != None:
                return object.effectAroundCaster[2]

    return 0

def changeDefault(select : StringSelectMenu, value : int):
    """Chance the default value from a Select Menu for the selected option"""
    value = str(value)
    temp = copy.deepcopy(select)
    for a in temp.options:
        if a.value == value:
            a.default = True
        elif a.default == True:
            a.default = False

    return temp

elemOptions = []
for a in range(0,len(elemDesc)):
    elemOptions.append(interactions.StringSelectOption(label=elemNames[a],value=str(a),emoji=getEmojiObject(elemEmojis[a])))

elemSelect = interactions.StringSelectMenu(elemOptions,custom_id = "elementSelect",placeholder="En savoir plus ou changer d'élément")

async def mimikThat(bot : interactions.Client, ctx : ComponentContext, msg : interactions.Message, user : char, toChange : Union[weapon,stuff]):
    index = type(toChange) == stuff
    
    desc = "Votre {0} prendra l'apparance de __{1} {2}__, voulez vous continuer ?".format(["arme","accessoire"][index],toChange.emoji,toChange.name)
    await msg.edit(embeds=interactions.Embed(title="__Mimikator :__ {0} {1}".format(toChange.emoji,toChange.name),color=user.color,description=desc),components=[interactions.ActionRow(returnButton,confirmButton)])

    def checkMate(m):
        m = m.ctx
        return int(m.author.id) == int(ctx.author.id)

    try:
        react = await bot.wait_for_component(msg,check=checkMate,timeout=60)
        react: ComponentContext = react.ctx
    except:
        return False

    if react.custom_id == "return":
        return False
    else:
        user = loadCharFile("./userProfile/{0}.json".format(user.owner))
        if index:
            user.apparaAcc = toChange
        else:
            user.apparaWeap = toChange

        user.otherInventory.remove(mimique)
        saveCharFile("./userProfile/{0}.json".format(user.owner),user)

        await msg.edit(embeds=interactions.Embed(title="__Mimikator :__ {0} {1}".format(toChange.emoji,toChange.name),color=user.color,description="Votre mimikator a bien été utilisé"),components=[])
        return True

async def compare(bot : interactions.Client, ctx : ComponentContext, user : char, see : Union[weapon,stuff]):
    if type(see) == stuff:
        toCompare = user.stuff[see.type]
    elif type(see) == weapon:
        toCompare = user.weapon

    emb = interactions.Embed(title="__Comparaison : {0} {2} -> {3} {1}__".format(toCompare.name,see.name,toCompare.emoji,see.emoji),color=user.color)
    compBonus = ""
    compMalus = ""
    allStaty = allStatsNames
    allStatsCompare = toCompare.allStats() + [toCompare.resistance,toCompare.percing,toCompare.critical,toCompare.negativeHeal*-1,toCompare.negativeBoost*-1,toCompare.negativeShield*-1,toCompare.negativeDirect*-1,toCompare.negativeIndirect*-1]
    allStatsSee = see.allStats() + [see.resistance,see.percing,see.critical,see.negativeHeal*-1,see.negativeBoost*-1,see.negativeShield*-1,see.negativeDirect*-1,see.negativeIndirect*-1]

    for cmpt in range(len(allStatsSee)):
        diff = allStatsSee[cmpt] - allStatsCompare[cmpt]
        if diff > 0:
            compBonus += "{2} {0} : **+{1}**\n".format(allStaty[cmpt],diff,statsEmojis[cmpt])
        elif diff < 0:
            compMalus += "{2}{0} : {1}\n".format(allStaty[cmpt],diff,statsEmojis[cmpt])

    if compBonus != "":
        emb.add_field(name="<:em:866459463568850954>\n__Gains de statistiques :__",value=compBonus,inline=True)
    if compMalus != "":
        emb.add_field(name="<:em:866459463568850954>\n__Pertes de statistiques :__",value=compMalus,inline=True)

    if type(see) == weapon:
        comp = ""
        tabl1 = ["Puissance","Précision","Nombre de tirs","Portée"]
        tabl2 = [see.power - toCompare.power, see.accuracy - toCompare.accuracy, see.repetition - toCompare.repetition, see.effectiveRange - toCompare.effectiveRange]

        for cmpt in range(len(tabl1)):
            if tabl2[cmpt] > 0:
                comp += "{0} : +**{1}**\n".format(tabl1[cmpt],tabl2[cmpt])
            else:
                comp += "{0} : {1}\n".format(tabl1[cmpt],tabl2[cmpt])

        comp += "\n"
        if see.use != toCompare.use:
            comp += "Statistique de base : ~~{0}~~ -> {1}\n".format(allStatsNames[toCompare.use],allStatsNames[see.use])

        emb.add_field(name="<:em:866459463568850954>\n__Différences de puissance :__",value=comp,inline=False)

    # Send
    try:
        await ctx.send(embeds=emb,ephemeral=True)
    except:
        await ctx.channel.send(embeds=emb)

async def elements(bot : interactions.Client, ctx : interactions.Message, msg : interactions.Message, user : classes.char):
    """Function to call for inventory elements.\n
    Edit de Msg for display the actual element of the user and a short description.\n
    Can also change the element if th user have a Elemental Cristal."""

    def check(m):
        m = m.ctx
        return m.author.id == ctx.author.id and m.message.id == msg.id

    def checkSecond(m):
        m = m.ctx
        return m.author.id == ctx.author.id and m.message.id == secondMsg.id

    if user.level < 10: # The user doesn't have the level
        elemEmbed = interactions.Embed(title="__Éléments__",color=user.color,description="Les éléments renforcent la spécialisation d'un personnage en augmentant les dégâts qu'il fait suivant certaines conditions définie par l'élément choisi\nLes équipements peuvent également avoir des éléments. Avoir des équipements du même élément que soit accroie un peu leurs statistiques\n")
        elemEmbed.add_field(name="__Contenu verouillé :__",value="Les éléments se débloquent à partir du nieau 10")
        await msg.edit(embeds=elemEmbed,components=[])

    else:
        while 1:
            elemEmbed = interactions.Embed(title="__Éléments__",color=user.color,description="Les éléments renforcent la spécialisation d'un personnage en augmentant les dégâts qu'il fait suivant certaines conditions définie par l'élément choisi\nLes équipements peuvent également avoir des éléments. Avoir des équipements du même élément que soit accroie un peu leurs statistiques\n")
            elemEmbed.add_field(name="<:em:866459463568850954>\n__Votre élément principal actuel est l'élément **{0}** ({1}) :__".format(elemNames[user.element],elemEmojis[user.element]),value=elemDesc[user.element]+"\n\n**__Passif principal :__\n"+elemMainPassifDesc[user.element]+"**", inline=False)
            if user.level >= 30:
                elemEmbed.add_field(name="<:em:866459463568850954>\n__Votre élément secondaire actuel est l'élément **{0}** ({1}) :__".format(elemNames[user.secElement],elemEmojis[user.secElement]),value=elemDesc[user.secElement]+"\n\n**__Passif secondaire :__\n"+elemSecPassifDesc[user.secElement]+"**", inline=False)
            else:
                elemEmbed.add_field(name="<:em:866459463568850954>\n__Votre élément secondaire actuel est l'élément **{0}** ({1}) :__".format(elemNames[user.secElement],elemEmojis[user.secElement]),value="Vous pourrez changer d'élément secondaire une fois le __niveau 30__ atteint", inline=False)

            await msg.edit(embeds = elemEmbed,components=[interactions.ActionRow(elemSelect)])

            try:
                respond = await bot.wait_for_component(msg,check=check,timeout=60)
                respond: ComponentContext = respond.ctx
            except asyncio.TimeoutError:
                await msg.edit(embeds = elemEmbed,components=[])
                break
            except:
                await msg.channel.send(format_exc())
                break

            resp = int(respond.values[0])
            respEmb = interactions.Embed(title = "__Élément : {0}__".format(elemNames[resp]),description = elemDesc[resp]+"\n\n__Passif principal :__\n"+elemMainPassifDesc[resp]+"\n\n__Passif secondaire__\n"+elemSecPassifDesc[resp],color=user.color)

            if resp not in [ELEMENT_LIGHT,ELEMENT_DARKNESS,ELEMENT_SPACE,ELEMENT_TIME]:
                if user.have(elementalCristal) and user.level >= 10:
                    actionrow = interactions.ActionRow(returnButton,changeElemEnable)
                else:
                    respEmb.set_footer(text="Vous ne possédez pas de cristaux élémentaires ou n'avez pas le niveau requis")
                    actionrow = interactions.ActionRow(returnButton,changeElemDisabled)
            else:
                if user.have(dimentioCristal) and user.level >= 20:
                    actionrow = interactions.ActionRow(returnButton,changeElemEnable2)
                else:
                    respEmb.set_footer(text="Vous ne possédez pas de cristaux dimentionnels ou n'avez pas le niveau requis")
                    actionrow = interactions.ActionRow(returnButton,changeElemDisabled2)

            if user.level < 30:
                secElemButton = []
            else:
                if resp in [ELEMENT_LIGHT,ELEMENT_DARKNESS,ELEMENT_SPACE,ELEMENT_TIME]:
                    if user.have(dimentioCristal):
                        secElemButton = [interactions.ActionRow(changeElemEnable4)]
                    else:
                        secElemButton = [interactions.ActionRow(changeElemDisabled4)]
                else:
                    if user.have(elementalCristal):
                        secElemButton = [interactions.ActionRow(changeElemEnable3)]
                    else:
                        secElemButton = [interactions.ActionRow(changeElemDisabled3)]

            try:
                secondMsg = await respond.send(embeds = respEmb,components=[actionrow]+secElemButton)
            except:
                secondMsg = await ctx.channel.send(embeds = respEmb,components=[actionrow]+secElemButton)

            try:
                respond = await bot.wait_for_component(secondMsg,check=checkSecond,timeout=60)
                respond: ComponentContext = respond.ctx
            except asyncio.TimeoutError:
                await secondMsg.delete()
                await msg.edit(embeds = elemEmbed,components=[])
                break
            except:
                await secondMsg.delete()
                await msg.channel.send(format_exc())
                break

            if respond.custom_id == "change":
                user.element = resp
                if resp not in [ELEMENT_LIGHT,ELEMENT_DARKNESS,ELEMENT_SPACE,ELEMENT_TIME]:
                    user.otherInventory.remove(elementalCristal)
                else:
                    user.otherInventory.remove(dimentioCristal)
                saveCharFile(absPath+"/userProfile/"+str(user.owner)+".json",user)
                await secondMsg.edit(embeds = interactions.Embed(title="__Élément : {0}__".format(elemNames[resp]),description="Votre élément principal a bien été modifié",color=user.color),components=[])

            elif respond.custom_id == "change2":
                user.secElement = resp
                if resp not in [ELEMENT_LIGHT,ELEMENT_DARKNESS,ELEMENT_SPACE,ELEMENT_TIME]:
                    user.otherInventory.remove(elementalCristal)
                else:
                    user.otherInventory.remove(dimentioCristal)
                saveCharFile(absPath+"/userProfile/"+str(user.owner)+".json",user)
                await secondMsg.edit(embeds = interactions.Embed(title="__Élément : {0}__".format(elemNames[resp]),description="Votre élément secondaire a bien été modifié",color=user.color),components=[])

            else:
                await secondMsg.delete()

async def blablaEdit(bot : interactions.Client, ctx : interactions.Message, msg : interactions.Message, user : classes.char):
    pathUserProfile = absPath + "/userProfile/" + str(user.owner) + ".json"

    def check(m):
        m = m.ctx
        return m.author.id == ctx.author.id and m.message.id == msg.id

    def checkMsg(message):
        message = message.message
        return int(message.author.id) == int(ctx.author.id) and int(message.channel.id) == int(msg.channel.id)

    while 1:
        user = loadCharFile(pathUserProfile)
        tablSays = user.says.tabl()
        option = []
        for count in range(len(tablCat)):
            desc = "Aucun message enregistré"
            if tablSays[count] != None:
                if len(tablSays[count]) <= 98:
                    desc = "\"{0}\"".format(tablSays[count])
                else:
                    desc = "\"{0}(...)\"".format(tablSays[count][:93])
            option.append(interactions.StringSelectOption(label=tablCat[count],value=str(count),description=desc))

        select = interactions.StringSelectMenu(option, custom_id = "selectAEvenement",placeholder="Sélectionnez un événement")

        emb = interactions.Embed(title="__/inventory says__",color=user.color,description="Vous pouvez enregistrer des messages que votre personnage dira lors de certain événements durant le combat\n\nCertains messages n'apparaitrons pas sistématiquement\n\nVous pouvez modifier autant de message que vous voulez, mais lors que le bot détectera une trop longue inactivité, votre Blablator sera consommé")
        await msg.edit(embeds=emb,components=[interactions.ActionRow(select)])

        try:
            respond = await bot.wait_for_component(messages=msg,check=check,timeout=180)
            respond: ComponentContext = respond.ctx
        except:
            break

        select = interactions.StringSelectMenu(option, custom_id = "selectAEvenement",placeholder="Sélectionnez un événement",disabled=True)
        await msg.edit(embeds=emb,components=[interactions.ActionRow(select)])
        repValue = int(respond.values[0])

        if tablSays[repValue] == None:
            desc = "Vous n'avez pas encore enregistré de message pour cet événement"
        else:
            desc = "Le message suivant est enregistré pour cet évémenement :\n\"{0}\"".format(tablSays[repValue])

        desc += "\n\nVeuillez renseigner le nouveau message :"
        if repValue in [1,2,12]:
            desc += "\n\n__Vous pouvez utiliser les balises suivantes pour cette catégorie :__\n{target} : Nom de la cible\n{caster} : Nom du lanceur\n{skill} : Nom de la compétence"
        elif repValue in [3]:
            desc += "\n\n__Vous pouvez utiliser les balises suivantes pour cette catégorie :__\n{target} : Nom de la cible éliminée\n{caster} : Nom du tueur"
        elif repValue in [4,5]:
            desc += "\n\n__Vous pouvez utiliser les balises suivantes pour cette catégorie :__\n{target} : Nom du tueur, réanimateur\n{caster} : Nom de la personne éliminée, réanimée"
        elif repValue in [15]:
            desc += "\n\n__Vous pouvez utiliser les balises suivantes pour cette catégorie :__\n{skill} : Nom de la compétence"
        elif repValue in [16,17]:
            desc += "\n\n__Vous pouvez utiliser les balises suivantes pour cette catégorie :__\n{killer} : Nom du tueur\n{downed} : Nom de la personne éliminée"
        elif repValue in [13,14]:
            desc += "\n\n__Vous pouvez utiliser les balises suivantes pour cette catégorie :__\n{caster} : Nom du réanimateur\n{skill} : Compétence utilisée"

        embed2 = interactions.Embed(title = "__/inventory says - {0}__".format(tablCat[repValue]),color=user.color,description=desc)
        reply = await respond.send(embeds = embed2)

        try:
            newMessage = await bot.wait_for("on_message_create",checks=checkMsg,timeout=180)
            newMessage: Message = newMessage.message

        except:
            break

        new = newMessage.content
        while new.startswith(" "):
            new = new[1:]
        while new.endswith(" "):
            new = new[:-2]
        tablSays[repValue] = new
        temp = says()
        user.says = temp.fromTabl(tablSays)
        saveCharFile(pathUserProfile,user)
        try:
            await newMessage.delete()
        except:
            print("J'ai pas pu effacer le message :|")
        await reply.edit(embeds=interactions.Embed(title = "/inventory says - {0}".format(tablCat[repValue]),color=user.color,description="Le message suivant a bien été enregistré pour cet événement :\n{0} : *\"{1}\"*".format(await getUserIcon(bot,user),new)))

    try:
        user.otherInventory.remove(blablator)
        saveCharFile(pathUserProfile,user)
    except:
        pass

    try:
        await reply.delete()
    except:
        pass

    await msg.edit(embeds=interactions.Embed(title="/inventory say",color=user.color,description="Votre Blablator a été consommé"))

def getInvMenu(tablToSee: List[Union[skill,stuff,weapon]], user: char = None):
    returnText, returnSelectOptions = "", []
    for obj in tablToSee:
        canEquip, hasEquiped = "", ""

        if user != None:
            if type(obj) in [skill,stuff] and not(obj.havConds(user)): canEquip = "`"
            elif obj in [user.weapon]+user.skills+user.stuff: hasEquiped = " 💼"
            desc = [None,"Cet object est déjà équipé"][obj in [user.weapon]+user.skills+user.stuff]
        else: desc = None
        returnText += f"\n{obj.emoji}{hasEquiped} __{canEquip}{obj.name}{canEquip}__\n{obj.getSummary()}\n"

        returnSelectOptions += [interactions.StringSelectOption(label=unhyperlink(obj.name),value=obj.id,emoji=getEmojiObject(obj.emoji),description=desc)]

    return (returnText, returnSelectOptions)

async def inventory(bot : interactions.Client, ctx : interactions.Message, identifiant : str, delete=False, procur=None):
    """Old function for the user's inventory. Still called when we go a id"""
    oldMsg = None
    if procur != None: pathUserProfile = "./userProfile/" + str(procur) + ".json"
    else: pathUserProfile = "./userProfile/" + str(ctx.author.id) + ".json"

    def checkIsAuthorReact(reaction,user):
        return int(user.id) == int(ctx.author.id) and int(reaction.message.id) == int(oldMsg.id)

    user = loadCharFile(pathUserProfile)
    if user.owner != ctx.author.id:
        if ctx.author.id not in user.procuration:
            try:
                await ctx.send(embeds = errorEmbed("__/inventory__",f"{user.name} ne vous a pas donné procuration sur son inventaire"))
            except:
                await ctx.channel.send(embeds = errorEmbed("__/inventory__",f"{user.name} ne vous a pas donné procuration sur son inventaire"))
            return 0

    if oldMsg == None:
        tmpEmb = interactions.Embed(title = "/inventory", description = emLoading)
        try: oldMsg = await ctx.send(embeds = tmpEmb)
        except: oldMsg = await ctx.channel.send(embeds = tmpEmb)

    inv = whatIsThat(identifiant)
    if inv != None:
        match inv:
            case 0:                # Weapon
                weap = findWeapon(identifiant)
                emb = infoWeapon(weap,user,ctx)

                componentList = [interactions.ActionRow(returnButton)]
                if not(user.have(weap)):
                    emb.footer.text +=" - Vous ne possédez pas cette arme"
                else:
                    if weap == user.weapon:
                        emb.footer.text += " - Vous utilisez déjà cette arme"
                    else:
                        emb.footer.text += " - Cliquez sur l'icone de l'arme pour l'équiper"
                        componentList[0].add_component(confirmButton)
                        componentList.append(interactions.ActionRow(interactions.Button(style=2,label="Comparer",emoji=getEmojiObject(user.weapon.emoji),custom_id="compare")))

                    if user.have(mimique) and (user.apparaWeap != None and user.apparaWeap.id != weap.id):
                        componentList[-1].add_component(useMimikator)

                await oldMsg.edit(embeds=emb, components=componentList)

                def check(m):
                    m = m.ctx
                    return m.author.id == ctx.author.id and m.message.id == oldMsg.id

                while 1:
                    try:
                        rep = await bot.wait_for_component(timeout=60,check=check,messages=oldMsg)
                        rep: ComponentContext = rep.ctx
                    except:
                        try:
                            if delete :
                                await oldMsg.delete()
                            else:
                                await oldMsg.edit(embeds = emb,components=[])
                        except:
                            pass
                        break

                    if rep.custom_id == "confirm":
                        user.weapon = weap
                        try:
                            saveCharFile(pathUserProfile,user)
                            await rep.respond(embeds = interactions.Embed(title = "__/inventory__",color = user.color,description="Vous avez bien équipé votre arme !"),ephemeral=True)
                            await oldMsg.delete()
                        except:
                            await react.respond(embeds = errorEmbed("__/inventory__","<:aliceBoude:1179656601083322470> Une erreur est survenue"))
                            await oldMsg.delete()
                        break
                    elif rep.custom_id == "compare":
                        await compare(bot,rep,user,weap)
                    elif rep.custom_id == "return":
                        if delete :
                            await oldMsg.delete()
                        else:
                            await oldMsg.edit(embeds = emb,components=[])
                        break
                    elif rep.custom_id == "mimikator":
                        var = await mimikThat(bot,ctx,oldMsg,user,weap)
                        break
            case 1:              # Skills
                invSkill = findSkill(identifiant)
                emb = infoSkill(invSkill,user,ctx)
                if type(emb) != list:
                    emb = [emb]

                ballerine=True
                if invSkill.group != 0:
                    for skilly in user.skills:
                        if type(skilly) == skill and skilly.group not in [0,invSkill.group]:
                            ballerine = False
                            break

                if invSkill not in user.skillInventory:
                    emb[-1].footer.text += " - Vous ne possédez pas cette compétence"
                    if delete:
                        await oldMsg.edit(embeds = emb,components=[])
                    else:
                        await oldMsg.edit(embeds = emb,components=[])
                elif invSkill in user.skills:
                    emb[-1].footer.text += "- Vous avez déjà équipé cette compétence. Voulez vous la déséquiper ?"
                    alReadyHaveButton = returnAndConfirmActionRow
                    alReadyHaveButton.components[0].label, alReadyHaveButton.components[0].style = "Déséquiper", ButtonStyle.GRAY
                    await oldMsg.edit(embeds = emb,components=[alReadyHaveButton])

                    def check(m):
                        m = m.ctx
                        return m.author.id == ctx.author.id

                    try:
                        rep = await bot.wait_for_component(timeout=60,check=check,messages=oldMsg)
                        rep: ComponentContext = rep.ctx
                    except:
                        if delete:
                            await oldMsg.delete()
                        else:
                            await oldMsg.edit(embeds = emb,components=[])
                        return 0

                    if rep.custom_id == "confirm":
                        for a in range(0,7):
                            if user.skills[a] == invSkill:
                                user.skills[a] = "0"
                                break

                        saveCharFile(pathUserProfile,user)
                        await rep.respond(embeds = interactions.Embed(title="Inventory",color=user.color,description="Votre compétence a bien été déséquipée"),ephemeral=True)
                        await oldMsg.delete()
                    else:
                        if delete:
                            await oldMsg.delete()
                        else:
                            await oldMsg.edit(embeds = emb,components=[])
                        return 0
                elif not(ballerine):
                    emb[-1].footer.text += " - Vous utilisez déjà une compétence du groupe opposé"
                    if delete:
                        await oldMsg.edit(embeds = emb,components=[])
                    else:
                        await oldMsg.edit(embeds = emb,components=[])
                elif not(invSkill.havConds(user=user)):
                    emb[-1].footer.text += "- Vous ne respectez pas les conditions de cette compétence"
                    if delete:
                        await oldMsg.edit(embeds = emb,components=[])
                    else:
                        await oldMsg.edit(embeds = emb,components=[])
                else:
                    hasUltimate=False
                    for a in [0,1,2,3,4,5,6]:
                        if type(user.skills[a]) == skill:
                            if user.skills[a].ultimate and invSkill.ultimate:
                                hasUltimate=True
                                break
                    options = []
            
                    if user.level < 5:
                        addPerLevel = []
                    elif user.level < 15:
                        addPerLevel = [3]
                    elif user.level < 25:
                        addPerLevel = [3,4]
                    elif user.level < 35:
                        addPerLevel = [3,4,5]
                    else:
                        addPerLevel = [3,4,5,6]

                    skillWithLevel = []
                    for slotNb in range(len(lvlToUnlockSkill)):
                        if user.level >= lvlToUnlockSkill[slotNb] or user.stars >= 1:skillWithLevel.append(slotNb)

                    for comp in skillWithLevel:
                        if type(user.skills[comp]) == skill:
                            ultimatum = ""
                            if user.skills[comp].ultimate: ultimatum = "Compétence ultime - "
                            if not(hasUltimate) or (hasUltimate and user.skills[comp].ultimate and invSkill.ultimate): options += [interactions.StringSelectOption(label=user.skills[comp].name, value=user.skills[comp].id, emoji=getEmojiObject(user.skills[comp].emoji))]
                        elif not(hasUltimate): options += [interactions.StringSelectOption(label=f"Slot de compétence vide",value=str(comp+1),emoji=PartialEmoji(name=EmCount[comp+1]))]

                    select = interactions.StringSelectMenu(options,custom_id = "skillPlaceSelect",placeholder="Sélectionnez un emplacement")

                    emb[-1].footer.text += " - Cliquez sur l'icone d'emplacement pour équiper"
                    await oldMsg.edit(embeds = emb,components=[interactions.ActionRow(returnButton),interactions.ActionRow(select)])
                    def check(m):
                        m = m.ctx
                        return m.author.id == ctx.author.id
                    react = None
                    try:
                        react = await bot.wait_for_component(messages=oldMsg,timeout=60,check=check)
                        react: ComponentContext = react.ctx
                    except:
                        if delete :
                            await oldMsg.delete()
                        else:
                            await oldMsg.edit(embeds = emb,components=[])

                    if react != None:
                        try:
                            await oldMsg.edit(embeds = emb,components=[interactions.ActionRow(getChoisenSelect(select,react.values[0]))])

                            for cmpt in [0,1,2,3,4,5,6]:
                                ballerine,babie = False,react.values[0] == str(cmpt+1)
                                if type(user.skills[cmpt]) == skill:
                                    ballerine = react.values[0] == user.skills[cmpt].id
                                if babie or ballerine:
                                    try:
                                        user.skills[cmpt] = invSkill
                                        saveCharFile(pathUserProfile,user)
                                        await react.respond(embeds = interactions.Embed(title = "__/inventory__",color = user.color,description="Vous avez bien équipé votre compétence !"),ephemeral=True)
                                        await oldMsg.delete()
                                    except:
                                        await react.respond(embeds = errorEmbed("__/inventory__","<:aliceBoude:1179656601083322470> Une erreur est survenue"),ephemeral=True)
                                        await oldMsg.delete()
                                    break
                        except:
                            print_exc()
                            await oldMsg.delete()
            case 2:              # Stuff
                invStuff = findStuff(identifiant)
                emb = infoStuff(invStuff,user,ctx)

                componentList = [interactions.ActionRow(returnButton)]

                if not(user.have(invStuff)): emb.footer.text +=  " - Vous ne possédez pas cet équipement"
                else:
                    if (invStuff == user.stuff[invStuff.type]) or (invStuff.minLvl > user.level):
                        if invStuff == user.stuff[invStuff.type]: emb.footer.text += " - Vous portez déjà cet équipement"
                        else: 
                            emb.footer.text += " - Cet équipement donne trop de statistiques pour votre niveau"
                            if user.aimedStuff[invStuff.type] != None and user.aimedStuff[invStuff.type] != invStuff.id: componentList[-1].add_component(interactions.Button(style=2,label="Changer Equipement Visé",emoji=getEmojiObject(findStuff(user.aimedStuff[invStuff.type]).emoji),custom_id="aimed"))

                    else:
                        emb.footer.text += " - Cliquez sur l'icone de l'équipement pour l'équiper"
                        componentList[0].add_component(confirmButton)
                        componentList.append(interactions.ActionRow(interactions.Button(style=2,label="Comparer",emoji=getEmojiObject(user.stuff[invStuff.type].emoji),custom_id="compare")))
                        if user.aimedStuff[invStuff.type] != None and user.aimedStuff[invStuff.type] != invStuff.id: componentList[-1].add_component(interactions.Button(style=2,label="Changer Equipement Visé",emoji=getEmojiObject(findStuff(user.aimedStuff[invStuff.type]).emoji),custom_id="aimed"))


                    if user.have(mimique) and invStuff.type == 0 and (user.apparaAcc != None and user.apparaAcc.id != invStuff.id): componentList[-1].add_component(useMimikator)
                await oldMsg.edit(embeds=emb, components=componentList)

                def check(m):
                    m = m.ctx
                    return m.author.id == ctx.author.id and m.message.id == oldMsg.id

                while 1:
                    try:
                        rep = await bot.wait_for_component(timeout=60,check=check,messages=oldMsg)
                        rep: ComponentContext = rep.ctx
                    except:
                        if delete :
                            try:
                                await oldMsg.delete()
                            except:
                                pass

                        else:
                            try:
                                await oldMsg.edit(embeds = emb,components=[])
                            except:
                                pass
                        break

                    match rep.custom_id:
                        case "confirm":
                            user.stuff[invStuff.type] = invStuff
                            try:
                                saveCharFile(pathUserProfile,user)
                                await rep.respond(embeds = interactions.Embed(title = "__/inventory__",color = user.color,description = "Votre nouvel équipement a bien été équipée"),ephemeral=True)
                                await oldMsg.delete()
                            except:
                                await rep.respond(embeds = errorEmbed("Erreur","Une erreur est survenue. La modification a pas été enregistrée"),ephemeral=True)
                                await oldMsg.delete()
                            break
                        case "compare":
                            await compare(bot,rep,user,invStuff)
                        case "return":
                            if delete :
                                await oldMsg.delete()
                            else:
                                await oldMsg.edit(embeds = emb,components=[])
                            break
                        case "mimikator":
                            var = await mimikThat(bot,ctx,oldMsg,user,invStuff)
                            break
                        case "aimed":
                            user.aimedStuff[invStuff.type] = invStuff.id
                            try:
                                saveCharFile(pathUserProfile,user)
                                await rep.respond(embeds = interactions.Embed(title = "__/inventory__",color = user.color,description = "Cet équipement a été défini comme équipement visé"),ephemeral=True)
                                await oldMsg.delete()
                            except:
                                await rep.respond(embeds = errorEmbed("Erreur","Une erreur est survenue. La modification a pas été enregistrée"),ephemeral=True)
                                await oldMsg.delete()
                            break
            case 3:              # Other
                obj = findOther(identifiant)
                emb = infoOther(obj,user)

                if obj == autoPoint:
                    emb.add_field(name ='<:em:866459463568850954>\n__Status de votre {0} :__'.format(obj.name),value=["Activé","Désactivé"][not(user.autoPoint)],inline=False)
                    emb.add_field(name ='<:em:866459463568850954>\n__Statistiques recommandées pour votre aspiration :__',value="{0}\n{1}".format(nameStats[recommandedStat[user.aspiration][0]],nameStats[recommandedStat[user.aspiration][1]]),inline=False)

                if obj == autoStuff:
                    emb.add_field(name ='<:em:866459463568850954>\n__Status de votre {0} :__'.format(obj.name),value=["Activé","Désactivé"][not(user.autoStuff)],inline=False)
                    emb.add_field(name ='<:em:866459463568850954>\n__Statistiques recommandées pour votre aspiration :__',value="{0}\n{1}\n{2}".format(allStatsNames[recommandedStuffStat[user.aspiration][0]],allStatsNames[recommandedStuffStat[user.aspiration][1]],allStatsNames[recommandedStuffStat[user.aspiration][2]]),inline=False)

                trouv = False
                for a in user.otherInventory:
                    if a.id == identifiant or a.name.lower() == identifiant.lower():
                        trouv = True

                if not(trouv):
                    emb.set_footer(text = "Vous ne possédez pas cet objet")
                    await oldMsg.edit(embeds = emb,components=[])

                else:
                    if obj == elementalCristal:
                        emb.set_footer(text = "Cet objet s'utilise avec /inventory destination: Élément")

                    if obj not in [elementalCristal,dimentioCristal,mimique,dailyCardBooster1,dailyCardBooster2]:
                        oldMsgCompo = ActionRow(
                            Button(style=ButtonStyle.SECONDARY,label="Retour",emoji=getEmojiObject("◀️"),custom_id="Return"),
                            Button(style=ButtonStyle.SUCCESS,label="Utiliser l'objet",emoji=getEmojiObject(obj.emoji),custom_id="use")
                        )
                    else:
                        oldMsgCompo = []

                    await oldMsg.edit(embeds = emb,components=oldMsgCompo)
                    def checkisReaction(reaction:ComponentContext):
                        reaction = reaction.ctx
                        return reaction.author.id == ctx.author.id
                    try:
                        reaction:ComponentContext = await bot.wait_for_component(messages=oldMsg,timeout=60,check=checkisReaction)
                        reaction: ComponentContext = reaction.ctx
                    except asyncio.TimeoutError:
                        return 0

                    if reaction.custom_id == "use":
                        if obj==changeAspi:
                            try:
                                user.aspiration = await chooseAspiration(bot,oldMsg,ctx,user)
                                if user.aspiration != None:
                                    user = restats(user)

                                    user.otherInventory.remove(changeAspi)
                                    try:
                                        saveCharFile(pathUserProfile,user)
                                        await oldMsg.edit(embeds = interactions.Embed(title = "__/inventory__",color = user.color,description = "Votre nouvelle aspiration a bien été prise en compte et vous avez récupéré vos points bonus"))
                                    except:
                                        await oldMsg.edit(embeds = errorEmbed("__/inventory__","Une erreure est survenue\n"))
                                        print_exc()
                            except:
                                await oldMsg.edit(embeds = errorEmbed("__/inventory__","Une erreure est survenue"))
                                print_exc()
                        elif obj==changeAppa:
                            still = True
                            if still: #Espèce
                                msgComponents = ActionRow(
                                    Button(style=ButtonStyle.PRIMARY,label="Inkling",emoji=getEmojiObject('<:ikaLBlue:866459302319226910>'),custom_id="inkling"),
                                    Button(style=ButtonStyle.PRIMARY,label="Octaling",emoji=getEmojiObject('<:takoLBlue:866459095875190804>'),custom_id="octaling")
                                )
                                await oldMsg.edit(embeds = interactions.Embed(title = "__/start__" + " : Espèce",color = light_blue,description = f"Sélectionnez l'espèce de votre personnage :\n\n<:ikaLBlue:866459302319226910> Inkling\n<:takoLBlue:866459095875190804> Octaling\n\nL'espèce n'a aucune influence sur les statistiques du personnage, et il vous sera possible de modifier la forme de votre personnage avec des objets spéciaux"),components=[msgComponents])

                                def checkIsAuthorReact1(reaction):
                                    reaction = reaction.ctx
                                    return reaction.author.id == ctx.author.id

                                try:
                                    respond = await bot.wait_for_component(messages=oldMsg ,timeout = 60, check = checkIsAuthorReact1)
                                    respond: ComponentContext = respond.ctx
                                    if respond.custom_id == 'inkling':
                                        user.species = 1
                                    else:
                                        user.species = 2
                                except asyncio.TimeoutError :
                                    print_exc()
                                    await oldMsg.edit(embeds = interactions.Embed(title = "Commande annulée (Timeout)"),components=MISSING)
                                    still = False
                            if still: #Genre
                                components = interactions.ActionRow(
                                    interactions.Button(style=ButtonStyle.PRIMARY,label="Masculin",emoji=getEmojiObject('♂️'),custom_id="male"),
                                    interactions.Button(style=ButtonStyle.PRIMARY,label="Féminin",emoji=getEmojiObject('♀️'),custom_id="female"),
                                    interactions.Button(style=ButtonStyle.PRIMARY,label="Autre / Passer",emoji=getEmojiObject("▶️"),custom_id="other")
                                )
                                await oldMsg.edit(embeds = interactions.Embed(title = "__/start__" + " : Genre",color = light_blue,description = f"Renseignez (ou non) le genre personnage :\nLe genre du personnage n'a aucune incidences sur ses statistiques et ne sert qu'à des fins orthographiques"),components=components)
                        
                                def checkIsAuthorReact(reaction:interactions.ComponentContext):
                                    reaction = reaction.ctx
                                    return reaction.author.id == ctx.author.id

                                try:
                                    respond = await bot.wait_for_component(timeout=60,check=checkIsAuthorReact,messages=oldMsg)
                                    respond: ComponentContext = respond.ctx
                                    testouille,titouille = [GENDER_MALE,GENDER_FEMALE,GENDER_OTHER],["male","female","other"]
                                    for a in range(0,len(titouille)):
                                        if str(respond.custom_id) == titouille[a]:
                                            user.gender = testouille[a]
                                except asyncio.TimeoutError:
                                    still = False
                                    await oldMsg.edit(embeds=interactions.Embed(title="Commande annulée (timeout"))
                            if still:
                                user = await chooseColor(bot,oldMsg,ctx,user)

                                if user != False:
                                    user.otherInventory.remove(changeAppa)
                                    saveCharFile(pathUserProfile,user)

                                    await oldMsg.edit(embeds = interactions.Embed(title="Changement d'apparence",color = user.color,description="Votre changement a bien été pris en compte !"),components = [])
                        elif obj==changeName:
                            await oldMsg.edit(embeds = interactions.Embed(title = "__/inventory__" + " : Nom",color = light_blue,description = f"Ecrivez le nom de votre personnage :\n\nVous ne pourrez pas modifier le nom de votre personnage par la suite"),components=[])
                            timeout = False
                            def checkIsAuthor(message):
                                message = message.message
                                return int(ctx.author.id) == int(message.author.id)
                            try:
                                respond = await bot.wait_for("on_message_create",timeout = 60,checks = checkIsAuthor)
                                respond: Message = respond.message
                            except:
                                timeout = True

                            if not(timeout):
                                user.name = respond.content
                                user.otherInventory.remove(changeName)

                                try:
                                    await respond.delete()
                                except:
                                    pass

                                saveCharFile(pathUserProfile,user)

                                await oldMsg.edit(embeds = interactions.Embed(title="Changement de nom",color = user.color,description="Votre changement a bien été pris en compte !"),components=[])
                            else:
                                await oldMsg.add_reaction('🕛')
                        elif obj==restat:
                            restats(user)
                            user.otherInventory.remove(restat)

                            saveCharFile(pathUserProfile,user)
                            
                            await oldMsg.edit(embeds = interactions.Embed(title="Rénitialisation des points bonus",color = user.color,description=f"Votre changement a bien été pris en compte !\nVous avez {user.points} à distribuer avec la commande \"points\""))
                        elif obj==customColor:
                            user = await changeCustomColor(bot,oldMsg,ctx,user)
                            if user != None:
                                user.otherInventory.remove(customColor)
                                saveCharFile(pathUserProfile,user)
                                
                                await oldMsg.edit(embeds = interactions.Embed(title="Couleur personnalisée",description="Votre couleur a bien été enregistrée\n\nCelle-ci sera appliquée à votre icone lors de sa prochaine modification",color=user.color),components=[])
                        elif obj==blablator:
                            await blablaEdit(bot,ctx,oldMsg,user)
                        elif obj in changeIconForm:
                            for cmpt in range(len(changeIconForm)):
                                if changeIconForm[cmpt] == obj:
                                    if user.iconForm != cmpt:
                                        user.iconForm = cmpt
                                        user.otherInventory.remove(obj)
                                        saveCharFile(user=user)
                                        await oldMsg.edit(embeds=interactions.Embed(title="__/inventory__",color=user.color,description="Votre {0} a bien été utilisé".format(obj.name)).set_image(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(await getUserIcon(bot,user)).id)),components=[])
                                    else: await oldMsg.edit(embeds=interactions.Embed(title="__/inventory__",color=user.color,description="Vous utilisez déjà cette forme d'icon"))
                                    break
                        elif obj==autoPoint:
                            if user.autoPoint:
                                user.autoPoint = False
                                user.otherInventory.remove(obj)
                                saveCharFile(user=user)
                                await oldMsg.edit(embeds=interactions.Embed(title="__Pai'rte de Nheur'o'Nes :__",color=user.color,description="Votre Pai'rte de Nheur'o'Nes a été désactivé"))
                            elif user.stars > 0:
                                user.autoPoint = True
                                user.otherInventory.remove(obj)
                                saveCharFile(user=user)
                                await oldMsg.edit(embeds=interactions.Embed(title="__Pai'rte de Nheur'o'Nes :__",color=user.color,description="Votre Pai'rte de Nheur'o'Nes a bien été activé.\n\n__Vos futurs points bonus seront attribués aux statistiques suivantes :__\n{0}\n{1}".format(nameStats[recommandedStat[user.aspiration][0]],nameStats[recommandedStat[user.aspiration][1]])))
                            else:
                                await oldMsg.edit(embeds=interactions.Embed(title="__Pai'rte de Nheur'o'Nes :__",color=user.color,description="Vous n'avez pas le niveau requis pour utiliser cet objet"))
                        elif obj==autoStuff:
                            if user.autoStuff:
                                user.autoStuff = False
                                user.otherInventory.remove(obj)
                                saveCharFile(user=user)
                                await oldMsg.edit(embeds=interactions.Embed(title="__Garde-robe de la Fée Niante :__",color=user.color,description="Votre Garde-robe de la Fée Niante a été désactivé"))
                            elif user.stars > 0:
                                user.autoStuff = True
                                user.otherInventory.remove(obj)
                                saveCharFile(user=user)
                                await oldMsg.edit(embeds=interactions.Embed(title="__Garde-robe de la Fée Niante :__",color=user.color,description="Votre Garde-robe de la Fée Niante a bien été activé.\n\n__Vos futurs équipements seront sélectionnés selon les statistiques suivantes :__\n{0}\n{1}\n{2}".format(allStatsNames[recommandedStuffStat[user.aspiration][0]],allStatsNames[recommandedStuffStat[user.aspiration][1]],allStatsNames[recommandedStuffStat[user.aspiration][2]])))
                            else:
                                await oldMsg.edit(embeds=interactions.Embed(title="_Garde-robe de la Fée Niante :__",color=user.color,description="Vous n'avez pas le niveau requis pour utiliser cet objet"))
                    else:
                        await oldMsg.delete()

    else: await ctx.edit(embed=Embed("Inventory",description="L'objet cherché n'a pas été trouvé"))

affult = interactions.Button(style=ButtonStyle.SUCCESS,label="Afficher tout type",emoji=getEmojiObject(splatbomb.emoji),custom_id="aff_ult")
hideult = interactions.Button(style=ButtonStyle.PRIMARY,label="Cacher Ultimes",emoji=getEmojiObject(burst.emoji),custom_id="hide_ult")
affonlyult = interactions.Button(style=2,label="Afficher Uniquement Ultimes",emoji=getEmojiObject(splashdown.emoji),custom_id="affonly_ult")
tablShowUltButton = [affult,hideult,affonlyult]
affmono = interactions.Button(style=ButtonStyle.SUCCESS,label="Afficher Compétences monocibles",emoji=getEmojiObject(fragmentation.emoji),custom_id="mono_area")
affaoe = interactions.Button(style=ButtonStyle.PRIMARY,label="Afficher Compétences Zone",emoji=getEmojiObject(multishot.emoji),custom_id="aoe_area")
affallarea = interactions.Button(style=2,label="Afficher toutes zones",emoji=getEmojiObject(coroShot.emoji),custom_id="all_area")
tablSkillArea = [affmono,affaoe,affallarea]
tablRangeSkill = [affAllRange,affCompMelee,affCompDist]
affReplaySkills2 = interactions.Button(style=ButtonStyle.BLUE,label="Afficher Compétences Rapides",emoji=getEmojiObject(suppuration.emoji),custom_id="replayAff")
affReplaySkills = interactions.Button(style=ButtonStyle.BLUE,label="Aff. Uniq. Compétences Rapides",emoji=getEmojiObject(lunaQuickFightEff.emoji[0][0]),custom_id="replayAffUn")
hideReplaySkills = interactions.Button(style=ButtonStyle.GREY,label="Cacher  Compétences Rapides",emoji=getEmojiObject(onstageeff.emoji[0][0]),custom_id="replayHide")
tablReplaySkills = [affReplaySkills2,affReplaySkills,hideReplaySkills]
affBundleSkills2 = interactions.Button(style=ButtonStyle.BLUE,label="Afficher Compétences Multiples",emoji=getEmojiObject(heatedCleanShot.emoji),custom_id="bundleAff")
affBundleSkills = interactions.Button(style=ButtonStyle.BLUE,label="Aff. Uniq. Compétences Multiples",emoji=getEmojiObject(confiteor.emoji),custom_id="bundleAffUn")
hideBundleSkills = interactions.Button(style=ButtonStyle.GREY,label="Cacher Compétences Multiples",emoji=getEmojiObject(infuEther.emoji),custom_id="bundleyHide")
tablBundleSkills = [affBundleSkills2,affBundleSkills,hideBundleSkills]

async def chipInventory(bot: interactions.Client, ctx: Union[interactions.SlashContext, interactions.Message], user: classes.char):
    rarityFilter, toSeePage, msg, secMsg, actRowtoEquipSelect = RARITY_MYTHICAL+1, 0, [None,ctx][type(ctx) == interactions.Message], None, None
    rarityfilterSelectOptions = [
        StringSelectOption(label="Rararté Commune",value="rarity_0",emoji=getEmojiObject(rarityEmojis[0])),
        StringSelectOption(label="Rararté Rare",value="rarity_1",emoji=getEmojiObject(rarityEmojis[1])),
        StringSelectOption(label="Rararté Légendaire",value="rarity_2",emoji=getEmojiObject(rarityEmojis[2])),
        StringSelectOption(label="Rararté Mythique",value="rarity_3",emoji=getEmojiObject(rarityEmojis[3])),
        StringSelectOption(label="Puces Possédées",value="rarity_4",emoji=getEmojiObject('<:univ:1137367685995438100>')),
        StringSelectOption(label="Puces Non-Possédées",value="rarity_5",emoji=getEmojiObject('🔒'))
    ]
    changePageButtons = [
        Button(style=ButtonStyle.GRAY,label="Première page",emoji=getEmojiObject('⏮'),custom_id="firstPage"),
        Button(style=ButtonStyle.GRAY,label="Page précédente",emoji=getEmojiObject('◀️'),custom_id="previousPage"),
        Button(style=ButtonStyle.GRAY,label="Page suivante",emoji=getEmojiObject('▶'),custom_id="nextPage"),
        Button(style=ButtonStyle.GRAY,label="Dernière page",emoji=getEmojiObject('⏭'),custom_id="lastPage")
    ]

    try:
        while 1:
            for indx in range(len(rarityfilterSelectOptions)):
                rarityfilterSelectOptions[indx].default = indx == rarityFilter
            
            actRowRarity = ActionRow(StringSelectMenu(rarityfilterSelectOptions,custom_id="raritySelect"))
            equippedChipInventoryEmbed, tempDesc, toEquipSelectOption = Embed(title="Puces équipées",color=user.color), "", []
            for cmpt, tmpChipId in enumerate(user.equippedChips):
                if tmpChipId != None:
                    tmpChip: userChip = user.chipInventory[tmpChipId]
                    tempDesc += " - {0} {1}__{2}__ - Niveau {3}\n> {4}\n".format(rarityEmojis[tmpChip.rarity],tmpChip.emoji+[""," "][tmpChip.emoji != ""], tmpChip.name, tmpChip.lvl, tmpChip.formatDescription().replace("> ","  - ").replace("\n","\n > "))
                    toEquipSelectOption.append(StringSelectOption(label=tmpChip.name,value="slot_{0}".format(cmpt),emoji=[getEmojiObject(tmpChip.emoji),None][tmpChip.emoji==""],description=["Commun","Rare","Légendaire","Mythique"][tmpChip.rarity]))
                else:
                    tempDesc += " \- \n"
                    toEquipSelectOption.append(StringSelectOption(label="Emplacement vide",emoji=getEmojiObject(listNumberEmoji[cmpt+1]),value="slot_{0}".format(cmpt)))

            equippedChipInventoryEmbed.description = tempDesc
            equippedChipInventoryEmbed.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.webp?size=96&quality=lossless".format(getEmojiInfo(await getUserIcon(bot,user))[1]))
            listOptionSelectChip = []
            ownedCommunChips, ownedRareChips, ownedLegendaryChips, ownedMythicalChips, unownedCommunChips, unownedRareChips, unownedLegendaryChips, unownedMythicalChips = [], [], [], [],[], [], [], []
            for tmpChipId, tmpChip in user.chipInventory.items():
                [[ownedCommunChips, ownedRareChips, ownedLegendaryChips, ownedMythicalChips],[unownedCommunChips, unownedRareChips, unownedLegendaryChips, unownedMythicalChips]][tmpChip.lvl <= rarityMinLvl[tmpChip.rarity]][tmpChip.rarity].append(tmpChip)

            tablAllTablChips = [ownedCommunChips, ownedRareChips, ownedLegendaryChips, ownedMythicalChips, unownedCommunChips, unownedRareChips, unownedLegendaryChips, unownedMythicalChips]
            for cmpt in range(len(tablAllTablChips)):
                tablAllTablChips[cmpt] = tablAllTablChips[cmpt].sort(key= lambda ballerine : ballerine.lvl*50+(26-string.ascii_lowercase.index(remove_accents(ballerine.name[0].lower()))),reverse=True)

            tablToSeeFull = [ownedCommunChips+unownedCommunChips, ownedRareChips+unownedRareChips, ownedLegendaryChips+unownedLegendaryChips, ownedMythicalChips+unownedMythicalChips, ownedCommunChips+ownedRareChips+ownedLegendaryChips+ownedMythicalChips,unownedCommunChips+unownedRareChips+unownedLegendaryChips+unownedMythicalChips][rarityFilter]
            tablToSee, chipInvEmbedDesc, chipInvEmbed = tablToSeeFull[toSeePage*10:min((toSeePage+1)*10,len(tablToSeeFull)-1)], "", Embed(title="Inventaire de puces",color=user.color)
            for tmpChip in tablToSee:
                chipInvEmbedDesc += " - {0} {1}__{5}{2}{5}__ - Niveau {5}{3}{5}{6}\n> {5}{4}{5}\n\n".format(rarityEmojis[tmpChip.rarity],tmpChip.emoji+[""," "][tmpChip.emoji != ""], tmpChip.name, tmpChip.lvl, tmpChip.formatDescription().replace("> ","  - ").replace("\n","\n > "),["","`"][tmpChip.lvl <= rarityMinLvl[tmpChip.rarity]],[""," (**{0}**/{1})".format(tmpChip.progress,nbChipsForLvlUp[tmpChip.lvl-rarityMinLvl[tmpChip.rarity]])][tmpChip.lvl > rarityMinLvl[tmpChip.rarity]])
                if tmpChip.lvl > rarityMinLvl[tmpChip.rarity]:
                    listOptionSelectChip.append(StringSelectOption(label=tmpChip.name,emoji=[getEmojiObject(tmpChip.emoji),None][tmpChip.emoji==""],value=tmpChip.id,description=["Commun","Rare","Légendaire","Mythique"][tmpChip.rarity]))
            
            chipInvEmbed.description, chipInvEmbed.footer = chipInvEmbedDesc, EmbedFooter(text="Page {0}/{1}".format(toSeePage+1 ,len(tablToSeeFull)//10 + int(len(tablToSeeFull)%10 > 0) -1+ 1))
            if len(listOptionSelectChip) > 0:
                actrowSelecChip = ActionRow(StringSelectMenu(listOptionSelectChip,placeholder="Voir une puce en particulier",custom_id="selecChip"))
            else:
                actrowSelecChip = ActionRow(StringSelectMenu(StringSelectOption(label="Vous ne possédez pas de puce de cette rareté",value="valuen't",default=True),disabled=True,placeholder="Voir une puce en particulier",custom_id="selecChip"))

            changePageButtons[0].disabled = changePageButtons[1].disabled = toSeePage <= 0
            changePageButtons[2].disabled = changePageButtons[3].disabled = toSeePage >= len(tablToSeeFull)//10 + int(len(tablToSeeFull)%10 > 0) -1

            actRowSailingButtons = ActionRow(changePageButtons[0],changePageButtons[1],changePageButtons[2],changePageButtons[3])

            if msg == None:
                msg = await ctx.send(embeds=[equippedChipInventoryEmbed,chipInvEmbed], components=[actRowSailingButtons,actrowSelecChip,actRowRarity])
            else:
                await msg.edit(embeds=[equippedChipInventoryEmbed,chipInvEmbed], components=[actRowSailingButtons,actrowSelecChip,actRowRarity])

            def check(m):
                m = m.ctx
                return m.author_id == ctx.author_id
            
            try:
                respond = await bot.wait_for_component(messages=[msg]+[[],[secMsg]][secMsg != None], components=[actRowSailingButtons,actrowSelecChip,actRowRarity]+[[],[actRowtoEquipSelect]][secMsg != None], timeout=300, check=check)
                respond: ComponentContext = respond.ctx
            except asyncio.TimeoutError:
                try:
                    await secMsg.delete()
                except:
                    pass

                await msg.edit(embeds=[equippedChipInventoryEmbed,chipInvEmbed], components=[])
                return 1

            if respond.component_type == ComponentType.STRING_SELECT and respond.component.custom_id == actrowSelecChip.components[0].custom_id:
                selectedChip: userChip = user.chipInventory[int(respond.values[0])]
                secEmbed = Embed(title="{0} __{1}__ - Niveau {2} (**{3}**/{4})".format(selectedChip.emoji+[" ",""][selectedChip.emoji == ""],selectedChip.name,selectedChip.lvl,selectedChip.progress,nbChipsForLvlUp[selectedChip.lvl-rarityMinLvl[selectedChip.rarity]]),color=user.color,description=selectedChip.formatDescription())

                if selectedChip.emoji != '':
                    secEmbed.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.webp?size=96&quality=lossless".format(getEmojiInfo(selectedChip.emoji)[1]))

                if selectedChip.id in user.equippedChips:
                    toEquipSelectOption = [StringSelectOption(label="Déséquiper",value="unequip",emoji=getEmojiObject('❌'))]
                elif selectedChip.rarity == RARITY_MYTHICAL:
                    otherMythical = False
                    for opt in toEquipSelectOption:
                        if opt.description == "Mythique":
                            otherMythical = True
                            break

                    if otherMythical:
                        for opt in toEquipSelectOption[:]:
                            if opt.description != "Mythique":
                                toEquipSelectOption.remove(opt)

                actRowtoEquipSelect = ActionRow(StringSelectMenu(toEquipSelectOption,placeholder=["Equiper la puce","Cette puce est actuellement désactivée"][selectedChip.name in disabled],custom_id="equipChip",disabled=selectedChip.name in disabled))

                if secMsg == None:
                    secMsg = await respond.respond(embeds=secEmbed, components=[actRowtoEquipSelect])
                else:
                    await secMsg.edit(embeds=secEmbed, components=[actRowtoEquipSelect])
            elif respond.component_type == ComponentType.STRING_SELECT and respond.component.custom_id == "equipChip":
                if respond.values[0] == "unequip":
                    for indx, chipId in enumerate(user.equippedChips):
                        if chipId == selectedChip.id:
                            user.equippedChips[indx] = None
                            await respond.respond("✅ Votre puce a bien été déséquipée",ephemeral=True)
                            break

                else:
                    user.equippedChips[int(respond.values[0].replace("slot_",""))] = selectedChip.id
                    await respond.respond("✅ Votre puce a bien été équipée",ephemeral=True)
                
                try:
                    await secMsg.delete()
                    secMsg = None
                except:
                    pass
                saveCharFile(user=user)
                user = loadCharFile(user=user)
            elif respond.component_type == ComponentType.STRING_SELECT and respond.component.custom_id == actRowRarity.components[0].custom_id:
                rarityFilter = int(respond.values[0].replace("rarity_",""))
                toSeePage = 0
            elif respond.component_type == ComponentType.BUTTON:
                toSeePage = {changePageButtons[0].custom_id:0, changePageButtons[1].custom_id:toSeePage-1, changePageButtons[2].custom_id:toSeePage+1, changePageButtons[3].custom_id:len(tablToSeeFull)//10 + int(len(tablToSeeFull)%10 > 0) -1}[respond.component.custom_id]
    except Exception as e:
        print_exc()
        try:
            await secMsg.delete()
        except:
            pass

        if msg != None:
            await msg.suppress_embeds()
            await msg.edit(content="A unexpected error occured :\n"+str(e),components=[])
        else:
            await ctx.send("A unexpected error occured :\n"+str(e))

async def inventoryV2(bot : interactions.Client, ctx : interactions.SlashContext, destination : int ,user : classes.char):
    """New function for the user's inventory. Heavely copied from encyclopedia"""
    if destination == INV_ELEMENT: msg = await ctx.send(embeds = interactions.Embed(title=randomWaitingMsg[random.randint(0,len(randomWaitingMsg)-1)])) ; await elements(bot,ctx,msg,user)
    elif destination == INV_CHIP: await chipInventory(bot, ctx, user)
    else:
        def check(m):
            m = m.ctx
            return m.author.id == ctx.author.id and m.message.id == msg.id

        msg = None
        opValues=["equipement","armes","competences","autre"]
        tri = 0
        needRemake, hideUlt, affMono, stuffMenuStatus, rangeSkill, showMaxLevel = True, 0, 0, 0, 0, 0

        listUserProcure = [user]
        for a in user.haveProcurOn:
            listUserProcure.append(loadCharFile("./userProfile/{0}.json".format(a)))

        mainUser = loadCharFile("./userProfile/{0}.json".format(ctx.author.id))
        def userSortValue(user):
            if user.owner == mainUser.owner:
                return 2
            elif user.team == mainUser.team and user.team != 0:
                return 1
            else:
                return 0
        listUserProcure.sort(key=lambda ballerine: userSortValue(ballerine),reverse=True)

        if len(listUserProcure) > 24: listUserProcure = listUserProcure[:24]

        affAll,stuffAff, statsToAff, stuffToAff, affReplay, affBundle, weaponRange = 0,False,0,0,0,0,0
        while 1:
            try:
                if len(listUserProcure) > 1:
                    procurOptions = []
                    for a in listUserProcure:
                        ilevel = (a.stuff[0].minLvl + a.stuff[1].minLvl + a.stuff[2].minLvl)//3
                        procurOptions.append(interactions.StringSelectOption(label=a.name,value="user_{0}".format(a.owner),emoji=getEmojiObject(await getUserIcon(bot,a)),description="Niveau {0}, Niv. Equip. {1}".format(a.level, ilevel)))
                    procurSelect = [interactions.ActionRow(interactions.StringSelectMenu(procurOptions,custom_id = "procurSelect",placeholder="Changer de personnage"))]
                else: procurSelect = []

                catSelect = interactions.StringSelectMenu([
                        interactions.StringSelectOption(label="Equipements",value="cat_0",emoji=getEmojiObject('<:uniform:866830066008981534>'),default=destination==0),
                        interactions.StringSelectOption(label="Armes",value="cat_1",emoji=getEmojiObject('<:kcharger:870870886939508737>'),default=destination==1),
                        interactions.StringSelectOption(label="Compétences",value="cat_2",emoji=getEmojiObject('<:stingray:899243721378390036>'),default=destination==2),
                        interactions.StringSelectOption(label="Objets",value="cat_3",emoji=getEmojiObject('<:changeAppa:872174182773977108>'),default=destination==3)
                    ],custom_id = "catOptionSelect",
                    placeholder="Changer de catégorie d'objets"
                )
                user = loadCharFile(absPath + "/userProfile/" + str(user.owner) + ".json")
                for a in range(len(listUserProcure)):
                    if listUserProcure[a].owner == user.owner:
                        listUserProcure[a] = user
                        break

                userIconThub = getEmojiObject(await getUserIcon(bot,user)).id
                options = [
                    interactions.StringSelectOption(label="Ordre Alphabétique ↓",value="0",emoji=PartialEmoji(name='🇦'),default=0==tri or(tri > 3 and destination > 3 and destination != 9)),
                    interactions.StringSelectOption(label="Ordre Alphabétique ↑",value="1",emoji=PartialEmoji(name='🇿'),default=1==tri)
                ]

                if destination in [INV_GEAR, INV_WEAPON]:
                    if not(stuffMenuStatus):
                        for cmpt in range(4,ACT_INDIRECT_FULL+5):
                            options.append(interactions.StringSelectOption(label=allStatsNames[cmpt-4],value=str(cmpt),emoji=getEmojiObject(statsEmojis[cmpt-4]),default=cmpt==tri))
                        options.append(interactions.StringSelectOption(label="Autre cat.",value="autCat_1",emoji=PartialEmoji(name="➡️")))
                    else:
                        options +=[
                                    interactions.StringSelectOption(label="Cat. classiques",value="autCat_0",emoji=PartialEmoji(name="⬅️")),
                                    interactions.StringSelectOption(label="For. - Pré.",value="22",emoji=getEmojiObject('<:lightBlue:933728207453163590>'),default=22==tri),
                                    interactions.StringSelectOption(label="For. - Agi.",value="23",emoji=getEmojiObject('<:green:933734508317003846>'),default=23==tri),
                                    interactions.StringSelectOption(label="Endur. - For.",value="24",emoji=getEmojiObject('<:black:933728357152096277>'),default=24==tri),
                                    interactions.StringSelectOption(label="Endur. - Mag.",value="25",emoji=getEmojiObject('<:orangeBatEarRing:938496708554416168>'),default=25==tri),
                                    interactions.StringSelectOption(label="Endur. - Soins / Char.",value="26",emoji=getEmojiObject('<:apGreenBatEar:938496729718849546>'),default=26==tri),
                                    interactions.StringSelectOption(label="Endur. - Intel. / Arm.",value="27",emoji=getEmojiObject('<:darkblue:933728323455045672>'),default=27==tri),
                                    interactions.StringSelectOption(label="Char. - Soins",value="28",emoji=getEmojiObject('<:white:933785500257513472>'),default=28==tri),
                                    interactions.StringSelectOption(label="Char. - Boost",value="29",emoji=getEmojiObject('<:pink:933728188754980904>'),default=29==tri),
                                    interactions.StringSelectOption(label="Intel. - Arm.",value="30",emoji=getEmojiObject('<:blue:933728247995305994>'),default=30==tri),
                                    interactions.StringSelectOption(label="Intel. - Boost",value="31",emoji=getEmojiObject('<:yellowBatER:937740799150555148>'),default=31==tri),
                                    interactions.StringSelectOption(label="Mag. - Préc.",value="32",emoji=getEmojiObject('<:red:933728281289715782> '),default=32==tri),
                                ]

                elif destination == INV_SKILL:options+=[interactions.StringSelectOption(label="Dégâts",value="14",emoji=getEmojiObject('<:meteor:904164411990749194>'),default=14==tri), interactions.StringSelectOption(label="Dégâts indirects",value="15",emoji=getEmojiObject('<:tentamissile:884757344397951026>'),default=15==tri), interactions.StringSelectOption(label="Soins",value="16",emoji=getEmojiObject('<:AdL:873548073769533470>'),default=16==tri), interactions.StringSelectOption(label="Armure",value="17",emoji=getEmojiObject('<:orbeDef:873725544427053076>'),default=17==tri), interactions.StringSelectOption(label="Boost",value='18',emoji=getEmojiObject('<:bpotion:867165268911849522>'),default=18==tri), interactions.StringSelectOption(label="Malus",value="19",emoji=getEmojiObject('<:nostalgia:867162802783649802>'),default=19==tri), interactions.StringSelectOption(label="Invocation",value="20",emoji=getEmojiObject('<:sprink1:887747751339757599>'),default=20==tri), interactions.StringSelectOption(label="Passif",value="21",emoji=getEmojiObject('<:IdoOH:909278546172719184>'),default=21==20)]

                sortOptions = interactions.StringSelectMenu(options,custom_id = "sortOptionsSelect",placeholder=["Trier par statistique","Afficher une catégorie en particulier"][destination == 2])
                if len(sortOptions.options) <= 1: sortOptions.options, sortOptions.disabled = [interactions.StringSelectOption(label="Aucune Option Disponible",value="None",emoji=PartialEmoji(name='❌'),default=True)], True

                if needRemake:
                    tablToSee = []
                    match destination:
                        case 0:
                            tablToSee, toRemove = user.stuffInventory, []
                            for indx, obj in enumerate(tablToSee):
                                tmpObj = findStuff(obj)
                                if tmpObj != None: tablToSee[indx] = tmpObj
                                else: toRemove.append(obj)

                            for obj in toRemove: tablToSee.remove(obj)

                            if not(stuffAff) or stuffToAff > 0 or showMaxLevel:
                                for a in tablToSee[:]:
                                    if (a !=None and not(stuffAff) and not(a.havConds(user))) or (stuffToAff > 0 and a.type != stuffToAff-1) or (showMaxLevel and (a.minLvl//10 < user.level//10 or a.minLvl//10 > user.level//10)): tablToSee.remove(a)
                        case 1:
                            tablToSee, toRemove = user.weaponInventory, []
                            for indx, obj in enumerate(tablToSee):
                                tmpObj = findWeapon(obj)
                                if tmpObj != None: tablToSee[indx] = tmpObj
                                else: toRemove.append(obj)

                                if weaponRange and tmpObj.range != weaponRange-1:
                                    toRemove.append(obj)
                            for obj in toRemove: tablToSee.remove(obj)
                        case 2:
                            tablToSee, toRemove = user.skillInventory, []
                            for indx, obj in enumerate(tablToSee):
                                tmpObj = findSkill(obj)
                                if tmpObj != None:
                                    tablToSee[indx] = tmpObj
                                else:
                                    toRemove.append(obj)

                            for obj in toRemove:
                                tablToSee.remove(obj)

                            if tri >= 14:
                                typeTabl = [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE,[TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_RESURECTION,TYPE_INDIRECT_REZ],TYPE_ARMOR,TYPE_BOOST,TYPE_MALUS,TYPE_SUMMON,TYPE_PASSIVE]
                                see = typeTabl[tri-14]
                                if type(see) != list:
                                    for ski in tablToSee[:]:
                                        if type(ski) != None:
                                            if (see != TYPE_BOOST and not(ski.type == see or (ski.effects != [None] and findEffect(ski.effects[0]).type == see) or (ski.effectAroundCaster != None and ski.effectAroundCaster[0] == see) or (ski.effectOnSelf != None and findEffect(ski.effectOnSelf).type == see) or (ski.depl != None and ski.depl.skills.type == see))) or (see == TYPE_BOOST and ski.type != TYPE_BOOST) or (see == TYPE_BOOST and ski.depl != None and ski.depl.skills.type != see):
                                                tablToSee.remove(ski)

                                else:
                                    for ski in tablToSee[:]:
                                        if not(ski.type in see or (ski.effects != [None] and findEffect(ski.effects[0]).type in see) or (ski.effectAroundCaster != None and ski.effectAroundCaster[0] in see) or (ski.effectOnSelf != None and findEffect(ski.effectOnSelf).type in see)):
                                            tablToSee.remove(ski)

                            if affAll==0:
                                for a in tablToSee[:]:
                                    if not(a.havConds(user)): tablToSee.remove(a)
                            elif affAll == 1:
                                for a in tablToSee[:]:
                                    if not(a.havConds(user)) or a.condition == []: tablToSee.remove(a)

                            if statsToAff > 0:
                                for skilly in tablToSee[:]:
                                    if skilly.use not in [[STRENGTH,AGILITY,PRECISION],[MAGIE,CHARISMA,INTELLIGENCE]][statsToAff-1]: tablToSee.remove(skilly)
                            if hideUlt == 1:
                                for skilly in tablToSee[:]:
                                    if skilly.ultimate: tablToSee.remove(skilly)
                            elif hideUlt == 2:
                                for skilly in tablToSee[:]:
                                    if not skilly.ultimate: tablToSee.remove(skilly)
                            if rangeSkill == 1:
                                for skilly in tablToSee[:]:
                                    if skilly.ultimate or skilly.range not in areaMelee+areaMixte: tablToSee.remove(skilly)
                            elif rangeSkill == 2:
                                for skilly in tablToSee[:]:
                                    if skilly.ultimate or skilly.range not in areaDist+areaMixte: tablToSee.remove(skilly)
                            if affMono == 1:
                                for skilly in tablToSee[:]:
                                    if skilly.area != AREA_MONO: tablToSee.remove(skilly)
                            elif affMono == 2:
                                for skilly in tablToSee[:]:
                                    if skilly.area == AREA_MONO:
                                        isValid = False
                                        if skilly.effects != None:
                                            for eff in skilly.effects:
                                                eff = findEffect(eff)
                                                if eff != None and eff.type == skilly.type and eff.area in [AREA_DONUT_1,AREA_DONUT_2,AREA_DONUT_3,AREA_DONUT_4,AREA_DONUT_5]: isValid = True; break

                                        if not(isValid): tablToSee.remove(skilly)

                            if affReplay > 0:
                                for skilly in tablToSee[:]:
                                    if [not(skilly.replay),skilly.replay][affReplay-1]: tablToSee.remove(skilly)
                            if affBundle > 0:
                                for skilly in tablToSee[:]:
                                    if [type(skilly.become) != list,type(skilly.become) == list][affBundle-1]: tablToSee.remove(skilly)

                            if tri in [14,16]:
                                tablToSee.sort(key=lambda ballerine:getSortSkillValue(ballerine,tri),reverse=True)
                            elif tri in [15]:
                                tablToSee.sort(key=lambda ballerine:getSortSkillValue(ballerine,tri),reverse=True)
                            elif tri in [17]:
                                tablToSee.sort(key=lambda ballerine:getSortSkillValue(ballerine,tri),reverse=True)
                        case 3:
                            tablToSee, toRemove = user.otherInventory, []
                            for indx, obj in enumerate(tablToSee):
                                tmpObj = findOther(obj)
                                if tmpObj != None:
                                    tablToSee[indx] = tmpObj
                                
                                else:
                                    toRemove.append(obj)
                            
                            for obj in toRemove:
                                tablToSee.remove(obj)

                    if destination in [0,1]:
                        tablToSee.sort(key=lambda ballerine:ballerine.name, reverse=tri)
                        match tri:
                            case num if 2 <= num <= 3: tablToSee.sort(key=lambda ballerine:user.have(ballerine), reverse=not(tri-2))
                            case 4: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.strength), reverse=True)
                            case 5: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.endurance), reverse=True)
                            case 6: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.charisma), reverse=True)
                            case 7: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.agility), reverse=True)
                            case 8: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.precision), reverse=True)
                            case 9: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.intelligence), reverse=True)
                            case 10: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.magie), reverse=True)
                            case 11: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.resistance), reverse=True)
                            case 12: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.percing), reverse=True)
                            case 13: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.critical), reverse=True)
                            case 14: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,-ballerine.negativeHeal), reverse=True)
                            case 15: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,-ballerine.negativeBoost), reverse=True)
                            case 16: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,-ballerine.negativeShield), reverse=True)
                            case 17: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,-ballerine.negativeDirect), reverse=True)
                            case 18: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,-ballerine.negativeIndirect), reverse=True)
                            case 22: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.strength + ballerine.precision + min(ballerine.negativeDirect,ballerine.negativeIndirect)*-1), reverse=True)
                            case 23: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.strength + ballerine.agility + min(ballerine.negativeDirect,ballerine.negativeIndirect)*-1), reverse=True)
                            case 24: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.strength + ballerine.endurance + min(ballerine.negativeDirect,ballerine.negativeIndirect)*-1), reverse=True)
                            case 25: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.endurance + ballerine.magie + min(ballerine.negativeDirect,ballerine.negativeIndirect)*-1), reverse=True)
                            case 26: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.charisma + ballerine.endurance + ballerine.negativeHeal*-1), reverse=True)
                            case 27: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.intelligence + ballerine.endurance + ballerine.negativeShield*-1), reverse=True)
                            case 28: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.charisma + ballerine.negativeHeal*-1), reverse=True)
                            case 29: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.charisma + ballerine.negativeBoost*-1), reverse=True)
                            case 30: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.intelligence + ballerine.negativeShield*-1), reverse=True)
                            case 31: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.intelligence + ballerine.negativeBoost*-1), reverse=True)
                            case 32: tablToSee.sort(key=lambda ballerine:(ballerine.minLvl,ballerine.magie + ballerine.precision + min(ballerine.negativeDirect,ballerine.negativeIndirect)*-1), reverse=True)

                    elif destination != 2: tablToSee.sort(key=lambda ballerine:ballerine.name,reverse=tri==1)

                    lenTabl = len(tablToSee)
                    maxPage, page, needRemake = lenTabl//15 - int(lenTabl%15 == 0), 0, False

                if destination == INV_GEAR: 
                    temp = ["","",""]
                    for indx, tmpId in enumerate(user.aimedStuff):
                        user.aimedStuff[indx] = findStuff(tmpId)
                        if user.aimedStuff[indx] != None: temp[indx] = " ({0})".format(user.aimedStuff[indx])
                    desc = "**__Équipement équipé :__\n{0}{3}\n{1}{4}\n{2}{5}**".format(user.stuff[0],user.stuff[1],user.stuff[2],temp[0],temp[1],temp[2])
                elif destination == INV_WEAPON: desc = "**__Arme équipée :__\n{0} {1}**".format(user.weapon.emoji,user.weapon.name)
                elif destination == INV_SKILL:    # Compétences
                    desc = "**__Compétences équipées :__"
                    for tip in range(len(user.skills)):
                        if type(user.skills[tip]) == skill: desc += "\n{0} {1}".format(user.skills[tip].emoji,user.skills[tip].name)
                        else: desc += ["\n 🔒","\n -"][user.level >= lvlToUnlockSkill[tip] or user.stars >= 1]
                    desc += "**"
                else: desc = "Les objets spéciaux permettent de modifier votre personnage"

                firstOptions = []

                if page > 0: firstOptions.append(interactions.StringSelectOption(label="Page précédente",value="goto{0}".format(page-1),emoji=PartialEmoji(name="◀️")))
                if lenTabl != 0: # Génération des pages
                    maxi = [(page+1)*10,lenTabl][page == maxPage]

                    mess, tempFirstOptions = getInvMenu(tablToSee[(page)*10:maxi],user)
                    firstOptions = firstOptions + tempFirstOptions

                    mess = reduceEmojiNames(mess)
                    if len(mess) > 4056: mess = unemoji(mess)
                    if len(mess) > 4056:
                        mess = "Objets sur cette page :"
                        for tmpObject in tablToSee[(page)*10:maxi]: mess += "- {0}\n".format(tmpObject)
                else: mess = "Il n'y a rien à afficher dans cette catégorie"

                if page < maxPage: firstOptions.append(interactions.StringSelectOption(label="Page suivante",value="goto{0}".format(page+1),emoji=PartialEmoji(name="▶️")))

                mainEmb = interactions.Embed(title="__/inventory__",description=desc,color=user.color)
                mainEmb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(userIconThub))
                emb = interactions.Embed(description="__Page **{0}** / {1} :__\n".format(page+1,maxPage+1)+mess,color=user.color)

                tempSelectOptions, listButtons, tmpBottom = [], [], []
                tmpTablEquip, tmpTablStat = [hideNonEquip,affExclu,affNonEquip], [onlyPhys,onlyMag,allType]
                tmpTablEquip.remove([hideNonEquip,affExclu,affNonEquip][affAll-1]); tmpTablStat.remove([onlyPhys,onlyMag,allType][(statsToAff+2)%3])
                
                if destination == INV_WEAPON:
                    listRangeButtons = [weapRangeAll,weapRangeMelee,weapRangeDist,weapRangeLong]
                    listRangeButtons.remove(listRangeButtons[weaponRange])
                    listButtons += tmpTablStat + listRangeButtons
                    tmpBottom += [["Physique","Psychique",""][(statsToAff+2)%3],["Toute portée","Mêlée","Distance","Longue Distance"][weaponRange]]

                elif destination == INV_SKILL:
                    tmpShowUlt, tmpSkillArea, tmpRangSkill, tmpReplay, tmpBundle = copy.deepcopy(tablShowUltButton), copy.deepcopy(tablSkillArea), copy.deepcopy(tablRangeSkill), copy.deepcopy(tablReplaySkills), copy.deepcopy(tablBundleSkills)
                    tmpShowUlt.remove(tablShowUltButton[hideUlt%3]); tmpSkillArea.remove(tablSkillArea[affMono-1]); tmpRangSkill.remove(tablRangeSkill[rangeSkill%3]); tmpReplay.remove(tablReplaySkills[affReplay%3]); tmpBundle.remove(tablBundleSkills[affBundle%3])
                    listButtons += tmpTablEquip+tmpTablStat+tmpShowUlt+tmpSkillArea+tmpRangSkill+tmpReplay+tmpBundle
                    tmpBottom += [
                        ["Equipable","Exclusivité","Non Equipable"][affAll],
                        ["Physique","Psychique",""][(statsToAff+2)%3],
                        ["Ultime","Non Ultime",""][hideUlt],
                        ["Monocible","Zone",""][affMono-1],
                        ["","Mêlée","Distance"][rangeSkill%3],
                        ["","Rapide","Non Rapide"][affReplay%3],
                        ["","Multiple","Unique"][affBundle%3]
                    ]

                elif destination == INV_GEAR:
                    tmpTabl = [affAcc,affBody,affShoes,affAllStuff]
                    tmpTabl.remove(tmpTabl[(stuffToAff+3)%4])
                    listButtons += tmpTabl+[Button(style=ButtonStyle.BLUE,label=["Afficher Niveaux Proches","Afficher Tous Niveaux"][showMaxLevel],custom_id="showMaxLevel")]
                    tmpBottom += [["Accessoires","Tenues","Chaussures",""][(stuffToAff+3)%4],["Tous niveaux","Niveaux proches"][showMaxLevel]]

                if len(firstOptions) > 0: firstSelect = interactions.StringSelectMenu(firstOptions,custom_id = "firstSelect",placeholder="Voir la page de l'équipement")
                else: firstSelect = interactions.StringSelectMenu(interactions.StringSelectOption(label="Cette catégorie n'a rien à afficher",value="None",emoji=PartialEmoji(name="❌"),default=True),custom_id = "firstSelect",placeholder="Cette catégorie n'a rien à afficher",disabled=True)

                for tempButton in listButtons: tempSelectOptions.append(interactions.StringSelectOption(label=tempButton.label,value=tempButton.custom_id,emoji=tempButton.emoji))

                if len(tempSelectOptions) < 1: ultimateTemp = [interactions.ActionRow(interactions.StringSelectMenu([interactions.StringSelectOption(label="Aucune Option Disponible",value="None",emoji=PartialEmoji(name='❌'),default=True)],disabled=True,custom_id="invSelectStat"))]
                else: ultimateTemp = [interactions.ActionRow(interactions.StringSelectMenu(tempSelectOptions,custom_id="invSelectStat",placeholder="Paramètres de tri",min_values=1,max_values=len(tempSelectOptions)))]

                tmpList = []
                for txt in tmpBottom:
                    if txt != "": tmpList.append(txt)

                bottom = " - ".join(tmpList)
                emb.set_footer(text=bottom)

                if msg == None:
                    try: msg = await ctx.send(embeds=[mainEmb,emb],components=procurSelect+[interactions.ActionRow(catSelect),interactions.ActionRow(sortOptions)]+ultimateTemp+[interactions.ActionRow(firstSelect)])
                    except:
                        try: msg = await ctx.channel.send(embeds=[mainEmb,emb],components=procurSelect+[interactions.ActionRow(catSelect),interactions.ActionRow(sortOptions)]+ultimateTemp+[interactions.ActionRow(firstSelect)])
                        except:
                            errorTxt = format_exc()
                            if len(errorTxt) > 1000:
                                errorTxt = errorTxt[len(errorTxt)-1000:]
                            await ctx.send(embeds=Embed(title="<:aliceBoude:1179656601083322470> Une erreur est survenue",description=errorTxt))
                            return 0
                else:
                    try: await msg.edit(embeds=[mainEmb,emb],components=procurSelect+[interactions.ActionRow(catSelect),interactions.ActionRow(sortOptions)]+ultimateTemp+[interactions.ActionRow(firstSelect)])
                    except:
                        formatedExc = format_exc()
                        if len(formatedExc) > EMBED_MAX_DESC_LENGTH: formatedExc.slipt("\n\n")[-1]
                        await msg.edit(embeds=[interactions.Embed(title="<:aliceBoude:1179656601083322470> Une erreur est survenue",description=formatedExc),interactions.Embed(title="Variable",description="FirstSelect = {0}".format(firstSelect.__dict__.__str__().replace("<StringSelectOption","\n<StringSelectOption")))],components=[])
                        return 0
                try: respond: ComponentContext = await bot.wait_for_component(msg,check=check,timeout=180);  respond: ComponentContext = respond.ctx
                except:
                    emb = interactions.Embed(title="__/inventory__",color=user.color)
                    emb.add_field(name="__Arme :__",value="{0} {1}".format(user.weapon.emoji,user.weapon.name))
                    emb.add_field(name="__Equipement :__",value="{0} {1}\n{2} {3}\n{4} {5}".format(user.stuff[0].emoji,user.stuff[0].name,user.stuff[1].emoji,user.stuff[1].name,user.stuff[2].emoji,user.stuff[2].name))
                    temp = ""

                    for nb in range(len(user.skills)):
                        if type(user.skills[nb])==skill:
                            temp += "{0} {1}\n".format(user.skills[nb].emoji,user.skills[nb].name)
                        else:
                            if user.level >= lvlToUnlockSkill[nb] or user.stars >= 1: temp += " -\n"
                            else: temp += " 🔒\n"

                    emb.add_field(name="__Compétences :__",value=temp)
                    emb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(userIconThub))
                    await msg.edit(embeds = emb, components = [])
                    return 0

                if respond.component_type == ComponentType.BUTTON: respond.values = [respond.custom_id]

                for value in respond.values:
                    if value.isdigit(): respond = int(value); sortOptions, needRemake, tri = changeDefault(sortOptions,respond), True, respond
                    elif value.startswith("cat_"):
                        if not(destination in [0,1] and tri <= 18): tri = 0
                        destination, needRemake, affAll, stuffAff, statsToAff, stuffToAff, showMaxLevel = int(value.replace("cat_","")), True, 0, False, 0, 0, 0
                    elif value.startswith("goto"): page = int(value.replace("goto",""))
                    elif value.startswith("user_"): user, needRemake, tri, affAll, stuffAff, statsToAff, stuffToAff = loadCharFile("./userProfile/{0}.json".format(value.replace("user_",""))), True, 0, 0, False, 0, 0
                    elif respond.custom_id in ["invSelectStat","sortOptionsSelect"]:
                        needRemake = True
                        for value in respond.values:
                            if value in ["hideNoneEquip","affNoneEquip","affExclu"]: affAll, stuffAff = {"hideNoneEquip":0,"affExclu":1,"affNoneEquip":2}[value], not(stuffAff)
                            elif value in ["allDamages","onlyPhys","onlyMag"]: statsToAff = {"allDamages":0,"onlyPhys":1,"onlyMag":2}[value]
                            elif value in ["acc","dress","flats","all"] : stuffToAff = {"acc":1,"dress":2,"flats":3,"all":0}[value]
                            elif value.endswith("_ult"): hideUlt = {"aff_ult":0,"hide_ult":1,"affonly_ult":2}[value]
                            elif value.endswith("_range"): rangeSkill = {"all_range":0,"melee_range":1,"dist_range":2}[value]
                            elif value.endswith("_area"): affMono = {"all_area":0,"mono_area":1,"aoe_area":2}[value]
                            elif value.startswith("autCat_"): stuffMenuStatus = int(value[-1]); tri = [0,22][stuffMenuStatus]
                            elif value.startswith("replay"): affReplay = {"replayAff":0,"replayAffUn":1,"replayHide":2}[value]
                            elif value.startswith("bundle"): affBundle = {"bundleAff":0,"bundleAffUn":1,"bundleyHide":2}[value]
                            elif value == "showMaxLevel": showMaxLevel = int(not(showMaxLevel))
                            elif value.startswith("range_"): weaponRange = {"range_all":0,"range_melee":1,"range_dist":2,"range_long":3}[value]
                    else:
                        if value in opValues:
                            for a in range(0,len(opValues)):
                                if opValues[a] == value: destination, needRemake = a, True; break

                        else:
                            await msg.edit(embeds=emb,components=[interactions.ActionRow(interactions.StringSelectMenu(interactions.StringSelectOption(label="None",value="None"),custom_id = "dunno",placeholder="Une autre action est en cours",disabled=True))])
                            if ctx.author.id != user.owner: await inventory(bot,respond,value,delete=True,procur=user.owner)
                            else: await inventory(bot,respond,value,delete=True)
            except:
                errorForm = format_exc()
                if len(errorForm) > EMBED_MAX_DESC_LENGTH:errorForm = errorForm[len(errorForm)-EMBED_MAX_DESC_LENGTH:]
                await ctx.send(embeds=Embed(title="<:aliceBoude:1179656601083322470> Une erreur est survenue",description=errorForm))
                return 0
