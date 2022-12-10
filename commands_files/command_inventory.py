import asyncio
import interactions
from interactions import ButtonStyle

from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from commands_files.command_start import chooseAspiration,chooseColor,changeCustomColor

ENC_ACC, ENC_GEAR, ENC_SHOE, ENC_WEAP, ENC_SKILL, ENC_ALLIES, ENC_ENEMIES, ENC_BOSS, ENC_LOCKED, ENC_ACHIV = tuple(range(10))
INV_GEAR, INV_WEAPON, INV_SKILL, INV_ELEMENT, INV_OBJ = tuple(range(5))

inventoryMenu = interactions.SelectMenu(custom_id = "inventoryFirstMenu", 
    options=[
        interactions.SelectOption(label="Inventaire d'Arme",value="0",emoji=getEmojiObject('<:splattershot:866367647113543730>')),
        interactions.SelectOption(label="Inventaire de Compétences",value="1",emoji=getEmojiObject('<:splatbomb:873527088286687272>')),
        interactions.SelectOption(label="Inventaire d'Equipement",value="2",emoji=getEmojiObject('<:bshirt:867156711251771402>')),
        interactions.SelectOption(label="Inventaire d'Objets",value="3",emoji=getEmojiObject('<:changeAppa:872174182773977108>')),
        interactions.SelectOption(label="Éléments",value="4",emoji=getEmojiObject('<:krysTal:888070310472073257>'))
        ],
    placeholder="Sélectionnez l'inventaire dans lequel vous voulez aller"
        )

returnButton = interactions.Button(type=2, style=2, label="Retour", emoji=Emoji(name="◀️"), custom_id="return")

changeElemEnable = interactions.Button(type=2, style=1, label="Utiliser comme élément principal", emoji=getEmojiObject('<:krysTal:888070310472073257>'), custom_id="change")
changeElemDisabled = interactions.Button(type=2, style=1,label="Utiliser comme élément principal",emoji=getEmojiObject('<:krysTal:888070310472073257>'),custom_id="change",disabled=True)
changeElemEnable2 = interactions.Button(type=2, style=1,label="Utiliser comme élément principal",emoji=getEmojiObject('<:krysTal2:907638077307097088>'),custom_id="change")
changeElemDisabled2 = interactions.Button(type=2, style=1,label="Utiliser comme élément principal",emoji=getEmojiObject('<:krysTal2:907638077307097088>'),custom_id="change",disabled=True)

changeElemEnable3 = interactions.Button(type=2, style=1,label="Utiliser comme élément secondaire",emoji=getEmojiObject('<:krysTal:888070310472073257>'),custom_id="change2")
changeElemDisabled3 = interactions.Button(type=2, style=1,label="Utiliser comme élément secondaire",emoji=getEmojiObject('<:krysTal:888070310472073257>'),custom_id="change2",disabled=True)
changeElemEnable4 = interactions.Button(type=2, style=1,label="Utiliser comme élément secondaire",emoji=getEmojiObject('<:krysTal2:907638077307097088>'),custom_id="change2")
changeElemDisabled4 = interactions.Button(type=2, style=1,label="Utiliser comme élément secondaire",emoji=getEmojiObject('<:krysTal2:907638077307097088>'),custom_id="change2",disabled=True)

confirmButton = interactions.Button(type=2, style=ButtonStyle.SUCCESS,label="Équiper",emoji=Emoji(name="✅"),custom_id="confirm")
useMimikator = interactions.Button(type=2, style=ButtonStyle.SECONDARY,label="Utiliser votre Mimikator",emoji=getEmojiObject(mimique.emoji),custom_id="mimikator")
hideNonEquip = interactions.Button(type=2, style=ButtonStyle.PRIMARY,label="Cacher Non équip.",custom_id="hideNoneEquip",emoji=getEmojiObject('<:invisible:899788326691823656>'))
affExclu = interactions.Button(type=2, style=ButtonStyle.SUCCESS,label="Aff. Exclusivité",custom_id="affExclu",emoji=getEmojiObject(matriseElemEff.emoji[0][0]))
affNonEquip = interactions.Button(type=2, style=2,label="Aff. Non équip.",custom_id="affNoneEquip",emoji=getEmojiObject("<:noeuil:887743235131322398>"))
allType = interactions.Button(type=2, style=ButtonStyle.SECONDARY,label="Aff. Tout",custom_id="allDamages",emoji=getEmojiObject('<:targeted:912415337088159744>'))
onlyPhys = interactions.Button(type=2, style=ButtonStyle.SUCCESS,label="Aff. Phy./Corp. un.",custom_id="onlyPhys",emoji=getEmojiObject("<:berkSlash:916210295867850782>"))
onlyMag = interactions.Button(type=2, style=ButtonStyle.PRIMARY,label="Aff Mag./Psy. un.",custom_id="onlyMag",emoji=getEmojiObject('<:lizDirectSkill:917202291042435142>'))
affAcc = interactions.Button(type=2, style=ButtonStyle.SUCCESS,label="Aff. Accessoire",emoji=getEmojiObject('<:defHead:896928743967301703>'),custom_id="acc")
affBody = interactions.Button(type=2, style=ButtonStyle.SUCCESS,label="Aff. Tenue",emoji=getEmojiObject('<:defMid:896928729673109535>'),custom_id="dress")
affShoes = interactions.Button(type=2, style=ButtonStyle.PRIMARY,label="Aff. Chaussures",emoji=getEmojiObject('<:defShoes:896928709330731018>'),custom_id="flats")
affAllStuff = interactions.Button(type=2, style=2,label="Aff. Tout",emoji=getEmojiObject('<:dualMagie:899628510463803393>'),custom_id="all")

affCompMelee = interactions.Button(type=2, style=ButtonStyle.DANGER,label="Aff. Comp. Mêlée",emoji=getEmojiObject(absorbingStrike.emoji),custom_id="melee_range")
affCompDist = interactions.Button(type=2, style=ButtonStyle.DANGER,label="Aff. Comp. Distance",emoji=getEmojiObject(absorbingArrow.emoji),custom_id="dist_range")
affAllRange = interactions.Button(type=2, style=2,label="Aff toute portée",custom_id="all_range")

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

confirmChange = interactions.Button(type=2, style=ButtonStyle.SUCCESS,label="Le renouveau c'est cool",emoji=Emoji(name="✅"),custom_id="confirm")
rejectModernity = interactions.Button(type=2, style=2,label="Rejeter la modernité",emoji=Emoji(name="❌"),custom_id="nope")

returnAndConfirmActionRow = interactions.ActionRow(components=[returnButton,confirmButton])

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

def changeDefault(select : SelectMenu, value : int):
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
    elemOptions.append(interactions.SelectOption(label=elemNames[a],value=str(a),emoji=getEmojiObject(elemEmojis[a])))

elemSelect = interactions.SelectMenu(custom_id = "elementSelect", options=elemOptions,placeholder="En savoir plus ou changer d'élément")

async def mimikThat(bot : interactions.Client, ctx : ComponentContext, msg : interactions.Message, user : char, toChange : Union[weapon,stuff]):
    index = type(toChange) == stuff
    
    desc = "Votre {0} prendra l'apparance de __{1} {2}__, voulez vous continuer ?".format(["arme","accessoire"][index],toChange.emoji,toChange.name)
    await msg.edit(embeds=interactions.Embed(title="__Mimikator :__ {0} {1}".format(toChange.emoji,toChange.name),color=user.color,description=desc),components=[interactions.ActionRow(components=[returnButton,confirmButton])])

    def checkMate(m):
        return int(m.author.id) == int(ctx.author.id)

    try:
        react = await bot.wait_for_component(msg,check=checkMate,timeout=60)
    except:
        return False

    if react.custom_id == "return":
        return False
    else:
        user = loadCharFile("./userProfile/{0}.prof".format(user.owner))
        if index:
            user.apparaAcc = toChange
        else:
            user.apparaWeap = toChange

        user.otherInventory.remove(mimique)
        saveCharFile("./userProfile/{0}.prof".format(user.owner),user)

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
        emb.add_field(name="<:empty:866459463568850954>\n__Gains de statistiques :__",value=compBonus,inline=True)
    if compMalus != "":
        emb.add_field(name="<:empty:866459463568850954>\n__Pertes de statistiques :__",value=compMalus,inline=True)

    if type(see) == weapon:
        comp = ""
        tabl1 = ["Puissance","Précision","Nombre de tirs","Portée"]
        tabl2 = [see.power - toCompare.power, see.sussess - toCompare.sussess, see.repetition - toCompare.repetition, see.effectiveRange - toCompare.effectiveRange]

        for cmpt in range(len(tabl1)):
            if tabl2[cmpt] > 0:
                comp += "{0} : +**{1}**\n".format(tabl1[cmpt],tabl2[cmpt])
            else:
                comp += "{0} : {1}\n".format(tabl1[cmpt],tabl2[cmpt])

        comp += "\n"
        if see.use != toCompare.use:
            comp += "Statistique de base : ~~{0}~~ -> {1}\n".format(allStatsNames[toCompare.use],allStatsNames[see.use])

        emb.add_field(name="<:empty:866459463568850954>\n__Différences de puissance :__",value=comp,inline=False)

    # Send
    try:
        await ctx.send(embeds=emb,delete_after=30)
    except:
        await ctx.channel.send(embeds=emb,delete_after=30)

async def elements(bot : interactions.Client, ctx : interactions.Message, msg : interactions.Message, user : classes.char):
    """Function to call for inventory elements.\n
    Edit de Msg for display the actual element of the user and a short description.\n
    Can also change the element if th user have a Elemental Cristal."""

    def check(m):
        return m.author.id == ctx.author.id and m.message.id == msg.id

    def checkSecond(m):
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

            await msg.edit(embeds = elemEmbed,components=[interactions.ActionRow(components=[elemSelect])])

            try:
                respond = await bot.wait_for_component(msg,check=check,timeout=60)
            except:
                await msg.edit(embeds = elemEmbed,components=[])
                break

            resp = int(respond.data.values[0])
            respEmb = interactions.Embed(title = "__Élément : {0}__".format(elemNames[resp]),description = elemDesc[resp]+"\n\n__Passif principal :__\n"+elemMainPassifDesc[resp]+"\n\n__Passif secondaire__\n"+elemSecPassifDesc[resp],color=user.color)

            if resp not in [ELEMENT_LIGHT,ELEMENT_DARKNESS,ELEMENT_SPACE,ELEMENT_TIME]:
                if user.have(elementalCristal) and user.level >= 10:
                    actionrow = interactions.ActionRow(components=[returnButton,changeElemEnable])
                else:
                    respEmb.set_footer(text="Vous ne possédez pas de cristaux élémentaires ou n'avez pas le niveau requis")
                    actionrow = interactions.ActionRow(components=[returnButton,changeElemDisabled])
            else:
                if user.have(dimentioCristal) and user.level >= 20:
                    actionrow = interactions.ActionRow(components=[returnButton,changeElemEnable2])
                else:
                    respEmb.set_footer(text="Vous ne possédez pas de cristaux dimentionnels ou n'avez pas le niveau requis")
                    actionrow = interactions.ActionRow(components=[returnButton,changeElemDisabled2])

            if user.level < 30:
                secElemButton = []
            else:
                if resp in [ELEMENT_LIGHT,ELEMENT_DARKNESS,ELEMENT_SPACE,ELEMENT_TIME]:
                    if user.have(dimentioCristal):
                        secElemButton = [interactions.ActionRow(components=[changeElemEnable4])]
                    else:
                        secElemButton = [interactions.ActionRow(components=[changeElemDisabled4])]
                else:
                    if user.have(elementalCristal):
                        secElemButton = [interactions.ActionRow(components=[changeElemEnable3])]
                    else:
                        secElemButton = [interactions.ActionRow(components=[changeElemDisabled3])]

            try:
                secondMsg = await respond.send(embeds = respEmb,components=[actionrow]+secElemButton)
            except:
                secondMsg = await ctx.channel.send(embeds = respEmb,components=[actionrow]+secElemButton)

            try:
                respond = await bot.wait_for_component(secondMsg,check=checkSecond,timeout=60)
            except:
                await secondMsg.delete()
                await msg.edit(embeds = elemEmbed,components=[])
                break

            if respond.custom_id == "change":
                user.element = resp
                if resp not in [ELEMENT_LIGHT,ELEMENT_DARKNESS,ELEMENT_SPACE,ELEMENT_TIME]:
                    user.otherInventory.remove(elementalCristal)
                else:
                    user.otherInventory.remove(dimentioCristal)
                saveCharFile(absPath+"/userProfile/"+str(user.owner)+".prof",user)
                await secondMsg.edit(embeds = interactions.Embed(title="__Élément : {0}__".format(elemNames[resp]),description="Votre élément principal a bien été modifié",color=user.color),components=[],delete_after=3)

            elif respond.custom_id == "change2":
                user.secElement = resp
                if resp not in [ELEMENT_LIGHT,ELEMENT_DARKNESS,ELEMENT_SPACE,ELEMENT_TIME]:
                    user.otherInventory.remove(elementalCristal)
                else:
                    user.otherInventory.remove(dimentioCristal)
                saveCharFile(absPath+"/userProfile/"+str(user.owner)+".prof",user)
                await secondMsg.edit(embeds = interactions.Embed(title="__Élément : {0}__".format(elemNames[resp]),description="Votre élément secondaire a bien été modifié",color=user.color),components=[],delete_after=3)

            else:
                await secondMsg.delete()

async def blablaEdit(bot : interactions.Client, ctx : interactions.Message, msg : interactions.Message, user : classes.char):
    pathUserProfile = absPath + "/userProfile/" + str(user.owner) + ".prof"

    def check(m):
        return m.author.id == ctx.author.id and m.message.id == msg.id

    def checkMsg(message):
        return int(message.author.id) == int(ctx.author.id) and int(message.channel_id) == int(msg.channel_id)

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
            option.append(interactions.SelectOption(label=tablCat[count],value=str(count),description=desc))

        select = interactions.SelectMenu(custom_id = "selectAEvenement", options=option,placeholder="Sélectionnez un événement")

        emb = interactions.Embed(title="__/inventory says__",color=user.color,description="Vous pouvez enregistrer des messages que votre personnage dira lors de certain événements durant le combat\n\nCertains messages n'apparaitrons pas sistématiquement\n\nVous pouvez modifier autant de message que vous voulez, mais lors que le bot détectera une trop longue inactivité, votre Blablator sera consommé")
        await msg.edit(embeds=emb,components=[interactions.ActionRow(components=[select])])

        try:
            respond = await bot.wait_for_component(messages=msg,check=check,timeout=180)
        except:
            break

        select = interactions.SelectMenu(custom_id = "selectAEvenement", options=option,placeholder="Sélectionnez un événement",disabled=True)
        await msg.edit(embeds=emb,components=[interactions.ActionRow(components=[select])])
        repValue = int(respond.data.values[0])

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
            newMessage = await bot.wait_for("on_message_create",check=checkMsg,timeout=180)
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
        await reply.edit(embeds=interactions.Embed(title = "/inventory says - {0}".format(tablCat[repValue]),color=user.color,description="Le message suivant a bien été enregistré pour cet événement :\n{0} : *\"{1}\"*".format(await getUserIcon(bot,user),new)),delete_after=10)

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
            if type(obj) in [skill,stuff] and not(obj.havConds(user)):
                canEquip = "`"
            elif obj in [user.weapon]+user.skills+user.stuff:
                hasEquiped = " 💼"
            desc = [None,"Cet object est déjà équipé"][obj in [user.weapon]+user.skills+user.stuff]
        else:
            desc = None
        returnText += f"\n{obj.emoji}{hasEquiped} __{canEquip}{obj.name}{canEquip}__\n{obj.getSummary()}\n"

        returnSelectOptions += [interactions.SelectOption(label=unhyperlink(obj.name),value=obj.id,emoji=getEmojiObject(obj.emoji),description=desc)]

    return (returnText, returnSelectOptions)

async def inventory(bot : interactions.Client, ctx : interactions.Message, identifiant : str, delete=False, procur=None):
    """Old function for the user's inventory. Still called when we go a id"""
    oldMsg = None
    if procur != None:
        pathUserProfile = "./userProfile/" + str(procur) + ".prof"
    else:
        pathUserProfile = "./userProfile/" + str(ctx.author.id) + ".prof"

    def checkIsAuthorReact(reaction,user):
        return int(user.id) == int(ctx.author.id) and int(reaction.message.id) == int(oldMsg.id)

    user = loadCharFile(pathUserProfile)
    if user.owner != ctx.author.id:
        if ctx.author.id not in user.procuration:
            try:
                await ctx.send(embeds = errorEmbed("__/inventory__",f"{user.name} ne vous a pas donné procuration sur son inventaire"),delete_after=10)
            except:
                await ctx.channel.send(embeds = errorEmbed("__/inventory__",f"{user.name} ne vous a pas donné procuration sur son inventaire"),delete_after=10)
            return 0

    if oldMsg == None:
        try:
            oldMsg = await ctx.send(embeds = interactions.Embed(title = "/inventory", description = emLoading))
        except:
            oldMsg = await ctx.channel.send(embeds = interactions.Embed(title = "/inventory", description = emLoading))
    inv = whatIsThat(identifiant)
    if inv != None:
        if inv == 0:                # Weapon
            weap = findWeapon(identifiant)
            emb = infoWeapon(weap,user,ctx)
            
            trouv = False
            for a in user.weaponInventory:
                if a.id == identifiant or a.name.lower() == identifiant.lower():
                    trouv = True

            if not(trouv):
                emb.set_footer(text = "Vous ne possédez pas cette arme")
                if delete:
                    await oldMsg.edit(embeds = emb,components=[],delete_after=60)
                else:
                    await oldMsg.edit(embeds = emb,components=[])
            elif weap == user.weapon:
                emb.set_footer(text = "Vous utilisez déjà cette arme")
                if delete:
                    await oldMsg.edit(embeds = emb,components=[])
                else:
                    await oldMsg.edit(embeds = emb,components=[])
            else:
                emb.set_footer(text = "Cliquez sur l'icone de l'arme pour l'équiper")
                compareButton = interactions.Button(type=2, style=2,label="Comparer",emoji=getEmojiObject(user.weapon.emoji),custom_id="compare")
                if user.have(mimique):
                    toAdd = [interactions.ActionRow(components=[useMimikator])]
                else:
                    toAdd = []
                await oldMsg.edit(embeds = emb,components=[returnAndConfirmActionRow,interactions.ActionRow(components=[compareButton])]+toAdd)

                def check(m):
                    return m.author.id == ctx.author.id and m.message.id == oldMsg.id

                while 1:
                    try:
                        rep = await bot.wait_for_component(timeout=60,check=check,messages=oldMsg)
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
                        if saveCharFile(pathUserProfile,user):
                            await oldMsg.edit(embeds = interactions.Embed(title = "__/inventory__",color = user.color,description = "Votre nouvelle équipement a bien été équipée"),components=[interactions.ActionRow(components=[interactions.SelectMenu(custom_id = "validStuff", options=[interactions.SelectOption(label=unhyperlink(weap.name),value="bidule",emoji=getEmojiObject(weap.emoji),default=True)],disabled=True)])],delete_after=5)
                        else:
                            await oldMsg.edit(embeds = errorEmbed("Erreur","Une erreur est survenue. La modification a pas été enregistrée"))
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

        elif inv == 1:              # Skills
            invSkill = findSkill(identifiant)
            emb = infoSkill(invSkill,user,ctx)

            ballerine=True
            if invSkill.group != 0:
                for skilly in user.skills:
                    if type(skilly) == skill and skilly.group not in [0,invSkill.group]:
                        ballerine = False
                        break

            if invSkill not in user.skillInventory:
                emb.set_footer(text = "Vous ne possédez pas cette compétence")
                if delete:
                    await oldMsg.edit(embeds = emb,components=[],delete_after=60)
                else:
                    await oldMsg.edit(embeds = emb,components=[])
            elif invSkill in user.skills:
                emb.set_footer(text = "Vous avez déjà équipé cette compétence. Voulez vous la déséquiper ?")
                await oldMsg.edit(embeds = emb,components=[returnAndConfirmActionRow])

                def check(m):
                    return m.author.id == ctx.author.id and m.message.id == oldMsg.id

                try:
                    rep = await bot.wait_for_component(timeout=60,check=check,messages=oldMsg)
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
                    await oldMsg.edit(embeds = interactions.Embed(title="Inventory",color=user.color,description="Votre compétence a bien été déséquipée"),delete_after=5,components=[])
                else:
                    if delete:
                        await oldMsg.delete()
                    else:
                        await oldMsg.edit(embeds = emb,components=[])
                    return 0
            elif not(ballerine):
                emb.set_footer(text = "Vous utilisez déjà une compétence du groupe opposé")
                if delete:
                    await oldMsg.edit(embeds = emb,components=[],delete_after=60)
                else:
                    await oldMsg.edit(embeds = emb,components=[])
            elif not(invSkill.havConds(user=user)):
                emb.set_footer(text = "Vous ne respectez pas les conditions de cette compétence")
                if delete:
                    await oldMsg.edit(embeds = emb,components=[],delete_after=60)
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
                    if user.level >= lvlToUnlockSkill[slotNb]:
                        skillWithLevel.append(slotNb)

                for comp in skillWithLevel:
                    if type(user.skills[comp]) == skill:
                        ultimatum = ""
                        if user.skills[comp].ultimate:
                            ultimatum = "Capacité ultime - "
                        if not(hasUltimate) or (hasUltimate and user.skills[comp].ultimate and invSkill.ultimate):
                            options += [interactions.SelectOption(label=user.skills[comp].name, value=user.skills[comp].id, emoji=getEmojiObject(user.skills[comp].emoji))]
                    elif not(hasUltimate):
                        options += [interactions.SelectOption(label=f"Slot de compétence vide",value=str(comp+1),emoji=Emoji(name=EmCount[comp+1]))]

                select = interactions.SelectMenu(custom_id = "skillPlaceSelect", options=options,placeholder="Sélectionnez un emplacement")

                emb.set_footer(text = "Cliquez sur l'icone d'emplacement pour équiper")
                await oldMsg.edit(embeds = emb,components=[interactions.ActionRow(components=[returnButton]),interactions.ActionRow(components=[select])])
                def check(m):
                    return m.author.id == ctx.author.id and m.message.id == oldMsg.id
                react = None
                try:
                    react = await bot.wait_for_component(messages=oldMsg,timeout=60,check=check)
                except:
                    if delete :
                        await oldMsg.delete()
                    else:
                        await oldMsg.edit(embeds = emb,components=[])

                if react != None:
                    try:
                        await oldMsg.edit(embeds = emb,components=[interactions.ActionRow(components=[getChoisenSelect(select,react.data.values[0])])])

                        for a in [0,1,2,3,4,5,6]:
                            ballerine,babie = False,react.data.values[0] == str(a+1)
                            if type(user.skills[a]) == skill:
                                ballerine = react.data.values[0] == user.skills[a].id

                            if babie or ballerine:
                                try:
                                    user.skills[a] = invSkill
                                    saveCharFile(pathUserProfile,user)
                                    await oldMsg.edit(embeds = interactions.Embed(title = "__/inventory__",color = user.color,description="Vous avez bien équipé votre compétence !",components=[interactions.ActionRow(components=[interactions.SelectMenu(custom_id = "validSelect", options=[interactions.SelectOption(label=unhyperlink(invSkill.name),value="bidule",emoji=getEmojiObject(invSkill.emoji),default=True)],disabled=True)])]),delete_after=5)
                                except:
                                    await oldMsg.edit(embeds = errorEmbed("__/inventory__","Une erreur est survenue",components=[]))
                                break
                    except:
                        await oldMsg.delete()

        elif inv == 2:              # Stuff
            invStuff = findStuff(identifiant)
            emb = infoStuff(invStuff,user,ctx)

            trouv = False
            for a in user.stuffInventory:
                if a.id == identifiant or a.name.lower() == identifiant.lower():
                    trouv = True

            if not(trouv):
                emb.set_footer(text = "Vous ne possédez pas cet équipement")
                if delete:
                    await oldMsg.edit(embeds = emb,components=[],delete_after=60)
                else:
                    await oldMsg.edit(embeds = emb,components=[])

            elif invStuff == user.stuff[invStuff.type]:
                emb.set_footer(text = "Vous portez déjà cet équipement")
                if delete:
                    await oldMsg.edit(embeds = emb,components=[],delete_after=60)
                else:
                    await oldMsg.edit(embeds = emb,components=[])
                
            elif invStuff.minLvl > user.level:
                emb.set_footer(text = "Cet équipement donne trop de statistiques pour votre niveau")
                if delete:
                    await oldMsg.edit(embeds = emb,components=[],delete_after=60)
                else:
                    await oldMsg.edit(embeds = emb,components=[])

            else:
                emb.set_footer(text = "Cliquez sur l'icone de l'équipement pour l'équiper")
                compareButton = interactions.Button(type=2, style=2,label="Comparer",emoji=getEmojiObject(user.stuff[invStuff.type].emoji),custom_id="compare")
                if user.have(mimique) and invStuff.type == 0:
                    toAdd = [interactions.ActionRow(components=[useMimikator])]
                else:
                    toAdd = []
                await oldMsg.edit(embeds = emb,components=[returnAndConfirmActionRow,interactions.ActionRow(components=[compareButton])]+toAdd)

                def check(m):
                    return m.author.id == ctx.author.id and m.message.id == oldMsg.id

                while 1:
                    try:
                        rep = await bot.wait_for_component(timeout=60,check=check,messages=oldMsg)
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

                    if rep.custom_id == "confirm":
                        user.stuff[invStuff.type] = invStuff
                        if saveCharFile(pathUserProfile,user):
                            await oldMsg.edit(embeds = interactions.Embed(title = "__/inventory__",color = user.color,description = "Votre nouvelle équipement a bien été équipée"),components=[interactions.ActionRow(components=[interactions.SelectMenu(custom_id = "Idontrememberwhatthisissupposedtobe", options=[interactions.SelectOption(label=unhyperlink(invStuff.name),value="bidule",emoji=getEmojiObject(invStuff.emoji),default=True)],disabled=True)])],delete_after=5)
                        else:
                            await oldMsg.edit(embeds = errorEmbed("Erreur","Une erreur est survenue. La modification a pas été enregistrée"))
                        break
                    elif rep.custom_id == "compare":
                        await compare(bot,rep,user,invStuff)
                    elif rep.custom_id == "return":
                        if delete :
                            await oldMsg.delete()
                        else:
                            await oldMsg.edit(embeds = emb,components=[])
                        break
                    elif rep.custom_id == "mimikator":
                        var = await mimikThat(bot,ctx,oldMsg,user,invStuff)
                        break

        elif inv == 3:              # Other
            obj = findOther(identifiant)
            emb = infoOther(obj,user)

            if obj == autoPoint:
                emb.add_field(name ='<:empty:866459463568850954>\n__Status de votre {0} :__'.format(obj.name),value=["Activé","Désactivé"][not(user.autoPoint)],inline=False)
                emb.add_field(name ='<:empty:866459463568850954>\n__Statistiques recommandées pour votre aspiration :__',value="{0}\n{1}".format(nameStats[recommandedStat[user.aspiration][0]],nameStats[recommandedStat[user.aspiration][1]]),inline=False)

            if obj == autoStuff:
                emb.add_field(name ='<:empty:866459463568850954>\n__Status de votre {0} :__'.format(obj.name),value=["Activé","Désactivé"][not(user.autoStuff)],inline=False)
                emb.add_field(name ='<:empty:866459463568850954>\n__Statistiques recommandées pour votre aspiration :__',value="{0}\n{1}\n{2}".format(allStatsNames[recommandedStuffStat[user.aspiration][0]],allStatsNames[recommandedStuffStat[user.aspiration][1]],allStatsNames[recommandedStuffStat[user.aspiration][2]]),inline=False)

            trouv = False
            for a in user.otherInventory:
                if a.id == identifiant or a.name.lower() == identifiant.lower():
                    trouv = True

            if not(trouv):
                emb.set_footer(text = "Vous ne possédez pas cet objet")
                await oldMsg.edit(embeds = emb,components=[])

            else:
                if obj != elementalCristal:
                    emb.set_footer(text = "Cliquez sur l'icone de l'objet l'utiliser")
                else:
                    emb.set_footer(text = "Cet objet s'utilise avec /inventory destination: Élément")

                await oldMsg.edit(embeds = emb,components=[])
                if obj not in [elementalCristal,dimentioCristal,mimique]:
                    await oldMsg.add_reaction(obj.emoji)

                def checkisReaction(reaction, user):
                    return int(user.id) == int(ctx.author.id) and str(reaction.emoji) ==  obj.emoji

                try:
                    await bot.wait_for("reaction_add",timeout=60,check=checkisReaction)
                    await oldMsg.remove_all_reactions()
                except asyncio.TimeoutError:
                    await oldMsg.remove_all_reactions()
                    return 0

                if obj==changeAspi:
                    try:
                        user.aspiration = await chooseAspiration(bot,oldMsg,ctx,user)
                        if user.aspiration != None:
                            user = restats(user)

                            user.otherInventory.remove(changeAspi)
                            if saveCharFile(pathUserProfile,user):
                                
                                await oldMsg.edit(embeds = interactions.Embed(title = "__/inventory__",color = user.color,description = "Votre nouvelle aspiration a bien été prise en compte et vous avez récupéré vos points bonus"))
                            else:
                                await oldMsg.edit(embeds = errorEmbed("__/inventory__","Une erreure est survenue\n"))
                                print_exc()
                    except:
                        await oldMsg.edit(embeds = errorEmbed("__/inventory__","Une erreure est survenue"))
                        print_exc()
                elif obj==changeAppa:
                    
                    await oldMsg.edit(embeds = interactions.Embed(title = "__/inventory__" + " : Espèce",color = light_blue,description = f"Sélectionnez l'espèce de votre personnage :\n\n<:ikaLBlue:866459302319226910> Inkling\n<:takoLBlue:866459095875190804> Octaling\n\nL'espèce n'a aucune influence sur les statistiques du personnage."))
                    await oldMsg.add_reaction('<:ikaLBlue:866459302319226910>')
                    await oldMsg.add_reaction('<:takoLBlue:866459095875190804>')

                    def checkIsAuthorReact1(reaction,user):
                        return int(user.id) == int(ctx.author.id) and int(reaction.message.id) == int(oldMsg.id) and (str(reaction)=='<:ikaLBlue:866459302319226910>' or str(reaction) == '<:takoLBlue:866459095875190804>')

                    respond = await bot.wait_for("reaction_add",timeout = 60,check = checkIsAuthorReact1)

                    if str(respond[0]) == '<:ikaLBlue:866459302319226910>':
                        user.species = 1
                    else:
                        user.species = 2
                    
                    await oldMsg.remove_all_reactions()
                    await oldMsg.edit(embeds = interactions.Embed(title = "__/inventory__" + " : Genre",color = light_blue,description = f"Renseignez (ou non) le genre personnage :\nLe genre du personnage n'a aucune incidences sur ses statistiques\n"))
                    await oldMsg.add_reaction('♂️')
                    await oldMsg.add_reaction('♀️')
                    await oldMsg.add_reaction("▶️")

                    def checkIsAuthorReact(reaction,user):
                        return int(user.id) == int(ctx.author.id) and int(reaction.message.id) == int(oldMsg.id) and (str(reaction)=='♀️' or str(reaction) == '♂️' or str(reaction) =="▶️")

                    respond = await bot.wait_for("reaction_add",timeout = 60,check = checkIsAuthorReact)
                    testouille,titouille = [GENDER_MALE,GENDER_FEMALE,GENDER_OTHER],['♂️','♀️',"▶️"]
                    for a in range(0,len(titouille)):
                        if str(respond[0]) == titouille[a]:
                            user.gender = testouille[a]

                    user = await chooseColor(bot,oldMsg,ctx,user)

                    if user != False:
                        user.otherInventory.remove(changeAppa)
                        saveCharFile(pathUserProfile,user)
                        
                        await oldMsg.edit(embeds = interactions.Embed(title="Changement d'apparence",color = user.color,description="Votre changement a bien été pris en compte !"),components = [])
                elif obj==changeName: 
                    
                    await oldMsg.edit(embeds = interactions.Embed(title = "__/inventory__" + " : Nom",color = light_blue,description = f"Ecrivez le nom de votre personnage :\n\nVous ne pourrez pas modifier le nom de votre personnage par la suite"))
                    timeout = False
                    def checkIsAuthor(message):
                        return int(ctx.author.id) == int(message.author.id)
                    try:
                        respond = await bot.wait_for("on_message_create",timeout = 60,check = checkIsAuthor)
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
                        
                        await oldMsg.edit(embeds = interactions.Embed(title="Changement de nom",color = user.color,description="Votre changement a bien été pris en compte !",components=[]))
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
                        
                        await oldMsg.edit(embeds = interactions.Embed(title="Couleur personnalisée",description="Votre couleur a bien été enregistrée\n\nCelle-ci sera appliquée à votre icone lors de sa prochaine modification",color=user.color))
                elif obj==blablator:
                    await blablaEdit(bot,ctx,oldMsg,user)
                elif obj in changeIconForm:
                    for cmpt in range(len(changeIconForm)):
                        if changeIconForm[cmpt] == obj:
                            if user.iconForm != cmpt:
                                user.iconForm = cmpt
                                user.otherInventory.remove(obj)
                                saveCharFile(user=user)
                                await oldMsg.edit(embeds=interactions.Embed(title="__/inventory__",color=user.color,description="Votre {0} a bien été utilisé".format(obj.name)).set_image(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(await getUserIcon(bot,user)).id)))
                            else:
                                await oldMsg.edit(embeds=interactions.Embed(title="__/inventory__",color=user.color,description="Vous utilisez déjà cette forme d'icon"))
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
                await oldMsg.remove_all_reactions()

async def inventoryV2(bot : interactions.Client,ctx : interactions.CommandContext ,destination : int ,user : classes.char):
    """New function for the user's inventory. Heavely copied from encyclopedia"""
    if destination == INV_ELEMENT:
        msg = await ctx.send(embeds = interactions.Embed(title=randomWaitingMsg[random.randint(0,len(randomWaitingMsg)-1)]))
        await elements(bot,ctx,msg,user)
    else:
        def check(m):
            return m.author.id == ctx.author.id and m.message.id == msg.id

        msg = None
        opValues=["equipement","armes","competences","autre"]
        tri = 0
        needRemake, hideUlt, affMono, stuffMenuStatus, rangeSkill = True, 0, 0, 0, 0

        affult = interactions.Button(type=2, style=ButtonStyle.SUCCESS,label="Aff. tout type",emoji=getEmojiObject(skillult[random.randint(0,len(skillult)-1)].emoji),custom_id="aff_ult")
        hideult = interactions.Button(type=2, style=ButtonStyle.PRIMARY,label="Cacher Ultimes",emoji=getEmojiObject(skillnonult[random.randint(0,len(skillnonult)-1)].emoji),custom_id="hide_ult")
        affonlyult = interactions.Button(type=2, style=2,label="Aff. seulement Ult.",emoji=getEmojiObject(skillult[random.randint(0,len(skillult)-1)].emoji),custom_id="affonly_ult")
        tablShowUltButton = [affult,hideult,affonlyult]
        affmono = interactions.Button(type=2, style=ButtonStyle.SUCCESS,label="Aff. comp. monocibles",emoji=getEmojiObject(skillMono[random.randint(0,len(skillMono)-1)].emoji),custom_id="mono_area")
        affaoe = interactions.Button(type=2, style=ButtonStyle.PRIMARY,label="Aff. comp. Zone",emoji=getEmojiObject(skillAoe[random.randint(0,len(skillAoe)-1)].emoji),custom_id="aoe_area")
        affallarea = interactions.Button(type=2, style=2,label="Aff. toutes zones",emoji=getEmojiObject(skills[random.randint(0,len(skills)-1)].emoji),custom_id="all_area")
        tablSkillArea = [affmono,affaoe,affallarea]
        tablRangeSkill = [affAllRange,affCompMelee,affCompDist]

        listUserProcure = [user]
        for a in user.haveProcurOn:
            listUserProcure.append(loadCharFile("./userProfile/{0}.prof".format(a)))
        
        mainUser = loadCharFile("./userProfile/{0}.prof".format(ctx.author.id))
        def userSortValue(user):
            if user.owner == mainUser.owner:
                return 2
            elif user.team == mainUser.team and user.team != 0:
                return 1
            else:
                return 0
        listUserProcure.sort(key=lambda ballerine: userSortValue(ballerine),reverse=True)

        if len(listUserProcure) > 24:
            listUserProcure = listUserProcure[:24]

        affAll,stuffAff,statsToAff,stuffToAff = 0,False,0,0
        while 1:
            if len(listUserProcure) > 0:
                procurOptions = []
                for a in listUserProcure:
                    ilevel = (a.stuff[0].minLvl + a.stuff[1].minLvl + a.stuff[2].minLvl)//3
                    procurOptions.append(interactions.SelectOption(label=a.name,value="user_{0}".format(a.owner),emoji=getEmojiObject(await getUserIcon(bot,a)),default=a.owner == user.owner,description="Niveau {0}, Niv. Equip. {1}".format(a.level, ilevel)))
                procurSelect = [interactions.ActionRow(components=[interactions.SelectMenu(custom_id = "procurSelect", options=procurOptions)])]
            else:
                procurSelect = []

            catSelect = interactions.SelectMenu(custom_id = "catOptionSelect", 
                options=[
                    interactions.SelectOption(label="Equipements",value="cat_0",emoji=getEmojiObject('<:uniform:866830066008981534>'),default=destination==0),
                    interactions.SelectOption(label="Armes",value="cat_1",emoji=getEmojiObject('<:kcharger:870870886939508737>'),default=destination==1),
                    interactions.SelectOption(label="Compétences",value="cat_2",emoji=getEmojiObject('<:stingray:899243721378390036>'),default=destination==2)
                ],
                placeholder="Changer de catégorie d'objets"
            )
            user = loadCharFile(absPath + "/userProfile/" + str(user.owner) + ".prof")
            for a in range(len(listUserProcure)):
                if listUserProcure[a].owner == user.owner:
                    listUserProcure[a] = user
                    break

            userIconThub = getEmojiObject(await getUserIcon(bot,user)).id
            options = [
                interactions.SelectOption(label="Ordre Alphabétique ↓",value="0",emoji=Emoji(name='🇦'),default=0==tri or(tri > 3 and destination > 3 and destination != 9)),
                interactions.SelectOption(label="Ordre Alphabétique ↑",value="1",emoji=Emoji(name='🇿'),default=1==tri)
            ]

            if destination in [INV_GEAR, INV_WEAPON]:
                if not(stuffMenuStatus):
                    for cmpt in range(4,ACT_INDIRECT_FULL+5):
                        options.append(interactions.SelectOption(label=allStatsNames[cmpt-4],value=str(cmpt),emoji=getEmojiObject(statsEmojis[cmpt-4]),default=cmpt==tri))
                    options.append(interactions.SelectOption(label="Autre cat.",value="autCat_1",emoji=Emoji(name="➡️")))
                else:
                    options +=[
                                interactions.SelectOption(label="Cat. classiques",value="autCat_0",emoji=Emoji(name="⬅️")),
                                interactions.SelectOption(label="For. - Pré.",value="22",emoji=getEmojiObject('<:lightBlue:933728207453163590>'),default=22==tri),
                                interactions.SelectOption(label="For. - Agi.",value="23",emoji=getEmojiObject('<:green:933734508317003846>'),default=23==tri),
                                interactions.SelectOption(label="Endur. - For.",value="24",emoji=getEmojiObject('<:black:933728357152096277>'),default=24==tri),
                                interactions.SelectOption(label="Endur. - Mag.",value="25",emoji=getEmojiObject('<:orangeBatEarRing:938496708554416168>'),default=25==tri),
                                interactions.SelectOption(label="Endur. - Soins / Char.",value="26",emoji=getEmojiObject('<:apGreenBatEar:938496729718849546>'),default=26==tri),
                                interactions.SelectOption(label="Endur. - Intel. / Arm.",value="27",emoji=getEmojiObject('<:darkblue:933728323455045672>'),default=27==tri),
                                interactions.SelectOption(label="Char. - Soins",value="28",emoji=getEmojiObject('<:white:933785500257513472>'),default=28==tri),
                                interactions.SelectOption(label="Char. - Boost",value="29",emoji=getEmojiObject('<:pink:933728188754980904>'),default=29==tri),
                                interactions.SelectOption(label="Intel. - Arm.",value="30",emoji=getEmojiObject('<:blue:933728247995305994>'),default=30==tri),
                                interactions.SelectOption(label="Intel. - Boost",value="31",emoji=getEmojiObject('<:yellowBatER:937740799150555148>'),default=31==tri),
                                interactions.SelectOption(label="Mag. - Préc.",value="32",emoji=getEmojiObject('<:red:933728281289715782> '),default=32==tri),
                            ]

            elif destination == INV_SKILL:
                options+=[
                    interactions.SelectOption(label="Dégâts",value="14",emoji=getEmojiObject('<:meteor:904164411990749194>'),default=14==tri),
                    interactions.SelectOption(label="Dégâts indirects",value="15",emoji=getEmojiObject('<:tentamissile:884757344397951026>'),default=15==tri),
                    interactions.SelectOption(label="Soins",value="16",emoji=getEmojiObject('<:AdL:873548073769533470>'),default=16==tri),
                    interactions.SelectOption(label="Armure",value="17",emoji=getEmojiObject('<:orbeDef:873725544427053076>'),default=17==tri),
                    interactions.SelectOption(label="Boost",value='18',emoji=getEmojiObject('<:bpotion:867165268911849522>'),default=18==tri),
                    interactions.SelectOption(label="Malus",value="19",emoji=getEmojiObject('<:nostalgia:867162802783649802>'),default=19==tri),
                    interactions.SelectOption(label="Invocation",value="20",emoji=getEmojiObject('<:sprink1:887747751339757599>'),default=20==tri),
                    interactions.SelectOption(label="Passif",value="21",emoji=getEmojiObject('<:IdoOH:909278546172719184>'),default=21==20)
                ]

            sortOptions = interactions.SelectMenu(custom_id = "sortOptionsSelect", options=options,placeholder=["Trier par statistique","Afficher une catégorie en particulier"][destination == 2])

            if needRemake:
                tablToSee = []
                if destination == 0:
                    tablToSee = user.stuffInventory
                    if not(stuffAff) or stuffToAff > 0:
                        for a in tablToSee[:]:
                            if not(stuffAff) and not(a.havConds(user)):
                                tablToSee.remove(a)
                            elif stuffToAff > 0 and a.type != stuffToAff-1:
                                tablToSee.remove(a)

                elif destination == 1:
                    tablToSee = user.weaponInventory
                elif destination == 2:
                    tablToSee = user.skillInventory
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
                            if not(a.havConds(user)):
                                tablToSee.remove(a)
                    elif affAll == 1:
                        for a in tablToSee[:]:
                            if not(a.havConds(user)) or a.condition == []:
                                tablToSee.remove(a)

                    if statsToAff > 0:
                        for skilly in tablToSee[:]:
                            if skilly.use not in [[STRENGTH,AGILITY,PRECISION],[MAGIE,CHARISMA,INTELLIGENCE]][statsToAff-1]:
                                tablToSee.remove(skilly)
                    if hideUlt == 1:
                        for skilly in tablToSee[:]:
                            if skilly.ultimate:
                                tablToSee.remove(skilly)
                    elif hideUlt == 2:
                        for skilly in tablToSee[:]:
                            if not skilly.ultimate:
                                tablToSee.remove(skilly)
                    if rangeSkill == 1:
                        for skilly in tablToSee[:]:
                            if skilly.ultimate or skilly.range not in areaMelee+areaMixte:
                                tablToSee.remove(skilly)
                    elif rangeSkill == 2:
                        for skilly in tablToSee[:]:
                            if skilly.ultimate or skilly.range not in areaDist+areaMixte:
                                tablToSee.remove(skilly)
                    if affMono == 1:
                        for skilly in tablToSee[:]:
                            if skilly.area != AREA_MONO:
                                tablToSee.remove(skilly)
                    elif affMono == 2:
                        for skilly in tablToSee[:]:
                            if skilly.area == AREA_MONO:
                                tablToSee.remove(skilly)

                    if tri in [14,16]:
                        tablToSee.sort(key=lambda ballerine:getSortSkillValue(ballerine,tri),reverse=True)
                    elif tri in [15]:
                        tablToSee.sort(key=lambda ballerine:getSortSkillValue(ballerine,tri),reverse=True)
                    elif tri in [17]:
                        tablToSee.sort(key=lambda ballerine:getSortSkillValue(ballerine,tri),reverse=True)

                elif destination == 3:
                    tablToSee = user.otherInventory

                if destination in [0,1]:
                    tablToSee.sort(key=lambda ballerine:ballerine.name, reverse=tri)
                    if tri in [2,3]:
                        tablToSee.sort(key=lambda ballerine:user.have(ballerine), reverse=not(tri-2))
                    elif tri == 4:
                        tablToSee.sort(key=lambda ballerine:ballerine.strength + max(ballerine.negativeDirect *-1,ballerine.negativeIndirect *-1), reverse=True)
                    elif tri == 5:
                        tablToSee.sort(key=lambda ballerine:ballerine.endurance, reverse=True)
                    elif tri == 6:
                        tablToSee.sort(key=lambda ballerine:ballerine.charisma + max(ballerine.negativeHeal *-1,ballerine.negativeBoost *-1), reverse=True)
                    elif tri == 7:
                        tablToSee.sort(key=lambda ballerine:ballerine.agility, reverse=True)
                    elif tri == 8:
                        tablToSee.sort(key=lambda ballerine:ballerine.precision, reverse=True)
                    elif tri == 9:
                        tablToSee.sort(key=lambda ballerine:ballerine.intelligence + max(ballerine.negativeShield *-1,ballerine.negativeBoost *-1), reverse=True)
                    elif tri == 10:
                        tablToSee.sort(key=lambda ballerine:ballerine.magie + max(ballerine.negativeDirect *-1,ballerine.negativeIndirect *-1), reverse=True)
                    elif tri == 11:
                        tablToSee.sort(key=lambda ballerine:ballerine.resistance, reverse=True)
                    elif tri == 12:
                        tablToSee.sort(key=lambda ballerine:ballerine.percing, reverse=True)
                    elif tri == 13:
                        tablToSee.sort(key=lambda ballerine:ballerine.critical, reverse=True)
                    elif tri == 14:
                        tablToSee.sort(key=lambda ballerine:-ballerine.negativeHeal + ballerine.charisma, reverse=True)
                    elif tri == 15:
                        tablToSee.sort(key=lambda ballerine:-ballerine.negativeBoost + max(ballerine.charisma,ballerine.intelligence), reverse=True)
                    elif tri == 16:
                        tablToSee.sort(key=lambda ballerine:-ballerine.negativeShield + ballerine.intelligence, reverse=True)
                    elif tri == 17:
                        tablToSee.sort(key=lambda ballerine:-ballerine.negativeDirect + max(ballerine.magie,ballerine.strength), reverse=True)
                    elif tri == 18:
                        tablToSee.sort(key=lambda ballerine:-ballerine.negativeIndirect + max(ballerine.magie,ballerine.strength), reverse=True)
                    elif tri == 22:
                        tablToSee.sort(key=lambda ballerine:ballerine.strength + ballerine.precision + min(ballerine.negativeDirect,ballerine.negativeIndirect)*-1, reverse=True)
                    elif tri == 23:
                        tablToSee.sort(key=lambda ballerine:ballerine.strength + ballerine.agility + min(ballerine.negativeDirect,ballerine.negativeIndirect)*-1, reverse=True)
                    elif tri == 24:
                        tablToSee.sort(key=lambda ballerine:ballerine.strength + ballerine.endurance + min(ballerine.negativeDirect,ballerine.negativeIndirect)*-1, reverse=True)
                    elif tri == 25:
                        tablToSee.sort(key=lambda ballerine:ballerine.endurance + ballerine.magie + min(ballerine.negativeDirect,ballerine.negativeIndirect)*-1, reverse=True)
                    elif tri == 26:
                        tablToSee.sort(key=lambda ballerine:ballerine.charisma + ballerine.endurance + ballerine.negativeHeal*-1, reverse=True)
                    elif tri == 27:
                        tablToSee.sort(key=lambda ballerine:ballerine.intelligence + ballerine.endurance + ballerine.negativeShield*-1, reverse=True)
                    elif tri == 28:
                        tablToSee.sort(key=lambda ballerine:ballerine.charisma + ballerine.negativeHeal*-1, reverse=True)
                    elif tri == 29:
                        tablToSee.sort(key=lambda ballerine:ballerine.charisma + ballerine.negativeBoost*-1, reverse=True)
                    elif tri == 30:
                        tablToSee.sort(key=lambda ballerine:ballerine.intelligence + ballerine.negativeShield*-1, reverse=True)
                    elif tri == 31:
                        tablToSee.sort(key=lambda ballerine:ballerine.intelligence + ballerine.negativeBoost*-1, reverse=True)
                    elif tri == 32:
                        tablToSee.sort(key=lambda ballerine:ballerine.magie + ballerine.precision + min(ballerine.negativeDirect,ballerine.negativeIndirect)*-1, reverse=True)
                elif destination != 2:
                    tablToSee.sort(key=lambda ballerine:ballerine.name,reverse=tri==1)

                lenTabl = len(tablToSee)
                maxPage=lenTabl//15 - int(lenTabl%15 == 0)
                page=0
                needRemake = False

            if destination == INV_GEAR:      # Equipement
                desc = "**__Équipement équipé :__\n{0} {1}\n{2} {3}\n{4} {5}**".format(user.stuff[0].emoji,user.stuff[0].name,user.stuff[1].emoji,user.stuff[1].name,user.stuff[2].emoji,user.stuff[2].name)
            elif destination == INV_WEAPON:    # Arme
                desc = "**__Arme équipée :__\n{0} {1}**".format(user.weapon.emoji,user.weapon.name)
            elif destination == INV_SKILL:    # Compétences
                desc = "**__Compétences équipées :__"
                for tip in range(len(user.skills)):
                    if type(user.skills[tip]) == skill:
                        desc += "\n{0} {1}".format(user.skills[tip].emoji,user.skills[tip].name)
                    else:
                        if user.level >= lvlToUnlockSkill[tip]:
                            desc += "\n -"
                        else:
                            desc += "\n 🔒"
                desc += "**"
            else:
                desc = "Les objets spéciaux permettent de modifier votre personnage"

            firstOptions = []

            if page > 0:
                firstOptions.append(interactions.SelectOption(label="Page précédente",value="goto{0}".format(page-1),emoji=Emoji(name="◀️")))
            if lenTabl != 0: # Génération des pages
                mess=""
                if page != maxPage:
                    maxi = (page+1)*10
                else:
                    maxi = lenTabl

                mess, tempFirstOptions = getInvMenu(tablToSee[(page)*10:maxi],user)
                firstOptions = firstOptions + tempFirstOptions

                mess = reducedEmojiNames(mess)

                if len(mess) > 4056: # Mess abrégé
                    mess = unemoji(mess)

            else:
                mess = "Il n'y a rien à afficher dans cette catégorie"

            if page < maxPage:
                firstOptions.append(interactions.SelectOption(label="Page suivante",value="goto{0}".format(page+1),emoji=Emoji(name="▶️")))

            emb = interactions.Embed(title="__/inventory__",description=desc+"\n\n__Page **{0}** / {1} :__\n".format(page+1,maxPage+1)+mess,color=user.color)
            emb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(userIconThub))

            if destination in [INV_WEAPON, INV_SKILL]:
                temp1 = [hideNonEquip,affExclu,affNonEquip][affAll-1]
                if statsToAff == 0:
                    temp2 = onlyPhys
                elif statsToAff == 1:
                    temp2 = onlyMag
                else:
                    temp2 = allType

                if destination == 1:
                    ultimateTemp = [interactions.ActionRow(components=[temp1,temp2])]
                else:
                    temp3 = tablShowUltButton[(hideUlt+1)%3]
                    temp4 = tablSkillArea[affMono]
                    temp5 = tablRangeSkill[(rangeSkill+1)%3]
                    ultimateTemp = [interactions.ActionRow(components=[temp1,temp2,temp3,temp4,temp5])]

            elif destination == INV_GEAR:
                temp1 = [hideNonEquip,affNonEquip,affExclu][affAll]
                temp2 = [affAcc,affBody,affShoes,affAllStuff][stuffToAff%4]
                ultimateTemp = [interactions.ActionRow(components=[temp1,temp2])]
            else:
                ultimateTemp = []

            if len(firstOptions) > 0:
                firstSelect = interactions.SelectMenu(custom_id = "firstSelect", options=firstOptions,placeholder="Voir la page de l'équipement")
            else:
                firstSelect = interactions.SelectMenu(custom_id = "firstSelect", options=[interactions.SelectOption(label="None",value="None")],placeholder="Cette catégorie n'a rien à afficher",disabled=True)

            if msg == None:
                try:
                    msg = await ctx.send(embeds=emb,components=procurSelect+[interactions.ActionRow(components=[catSelect]),interactions.ActionRow(components=[sortOptions]),interactions.ActionRow(components=[firstSelect])]+ultimateTemp)
                except:
                    msg = await ctx.channel.send(embeds=emb,components=procurSelect+[interactions.ActionRow(components=[catSelect]),interactions.ActionRow(components=[sortOptions]),interactions.ActionRow(components=[firstSelect])]+ultimateTemp)
            else:
                try:
                    await msg.edit(embeds=emb,components=procurSelect+[interactions.ActionRow(components=[catSelect]),interactions.ActionRow(components=[sortOptions]),interactions.ActionRow(components=[firstSelect])]+ultimateTemp)
                except:
                    await msg.edit(embeds=emb,components=procurSelect+[interactions.ActionRow(components=[catSelect]),interactions.ActionRow(components=[sortOptions]),interactions.ActionRow(components=[firstSelect])]+ultimateTemp)

            try:
                respond: ComponentContext = await bot.wait_for_component(msg,check=check,timeout=180)
            except:
                emb = interactions.Embed(title="__/inventory__",color=user.color)
                emb.add_field(name="__Arme :__",value="{0} {1}".format(user.weapon.emoji,user.weapon.name))
                emb.add_field(name="__Equipement :__",value="{0} {1}\n{2} {3}\n{4} {5}".format(user.stuff[0].emoji,user.stuff[0].name,user.stuff[1].emoji,user.stuff[1].name,user.stuff[2].emoji,user.stuff[2].name))
                temp = ""

                for nb in range(len(user.skills)):
                    if type(user.skills[nb])==skill:
                        temp += "{0} {1}\n".format(user.skills[nb].emoji,user.skills[nb].name)
                    else:
                        if user.level >= lvlToUnlockSkill[nb]:
                            temp += " -\n"
                        else:
                            temp += " 🔒\n"

                emb.add_field(name="__Compétences :__",value=temp)
                emb.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(userIconThub))
                await msg.edit(embeds = emb, components = [])
                return 0

            if respond.data.component_type == 2:
                respond.data.values = [respond.custom_id]

            if respond.data.values[0].isdigit():
                respond = int(respond.data.values[0])
                sortOptions = changeDefault(sortOptions,respond)

                if respond in [0,1] or respond >= 14:
                    needRemake=True
                else:
                    tablToSee.sort(key=lambda ballerine: ballerine.name)
                    if respond == 4:
                        tablToSee.sort(key=lambda ballerine:ballerine.strength + max(ballerine.negativeDirect *-1,ballerine.negativeIndirect *-1), reverse=True)
                    elif respond == 5:
                        tablToSee.sort(key=lambda ballerine:ballerine.endurance, reverse=True)
                    elif respond == 6:
                        tablToSee.sort(key=lambda ballerine:ballerine.charisma + max(ballerine.negativeHeal *-1,ballerine.negativeBoost *-1), reverse=True)
                    elif respond == 7:
                        tablToSee.sort(key=lambda ballerine:ballerine.agility, reverse=True)
                    elif respond == 8:
                        tablToSee.sort(key=lambda ballerine:ballerine.precision, reverse=True)
                    elif respond == 9:
                        tablToSee.sort(key=lambda ballerine:ballerine.intelligence + max(ballerine.negativeShield *-1,ballerine.negativeBoost *-1), reverse=True)
                    elif respond == 10:
                        tablToSee.sort(key=lambda ballerine:ballerine.magie + max(ballerine.negativeDirect *-1,ballerine.negativeIndirect *-1), reverse=True)
                    elif respond == 11:
                        tablToSee.sort(key=lambda ballerine:ballerine.resistance, reverse=True)
                    elif respond == 12:
                        tablToSee.sort(key=lambda ballerine:ballerine.percing, reverse=True)
                    elif respond == 13:
                        tablToSee.sort(key=lambda ballerine:ballerine.critical, reverse=True)

                tri=respond

            elif respond.data.values[0].startswith("cat_"):
                destination = int(respond.data.values[0].replace("cat_",""))
                needRemake, tri, affAll, stuffAff, statsToAff, stuffToAff = True, 0, 0, False, 0, 0

            elif respond.data.values[0].startswith("goto"):
                page = int(respond.data.values[0].replace("goto",""))

            elif respond.data.values[0].startswith("user_"):
                user = loadCharFile("./userProfile/{0}.prof".format(respond.data.values[0].replace("user_","")))
                needRemake, tri, affAll, stuffAff, statsToAff, stuffToAff = True, 0, 0, False, 0, 0

            elif respond.data.values[0] in ["hideNoneEquip","affNoneEquip","affExclu"]:
                for cmpt in range(3):
                    if respond.data.values[0] == ["hideNoneEquip","affExclu","affNoneEquip"][cmpt]:
                        affAll = cmpt
                        break
                stuffAff = not(stuffAff)
                needRemake = True
            elif respond.data.values[0] in ["allDamages","onlyPhys","onlyMag","acc","dress","flats","all"]:
                if destination == 2:
                    statsToAff = (statsToAff+1)%3
                elif destination == 0:
                    stuffToAff = (stuffToAff+1)%4
                needRemake = True
            elif respond.data.values[0].endswith("_ult"):
                hideUlt = (hideUlt+1)%3
                needRemake = True
            elif respond.data.values[0].endswith("_range"):
                rangeSkill = (rangeSkill+1)%3
                needRemake = True
            elif respond.data.values[0].endswith("_area"):
                affMono = (affMono+1)%3
                needRemake = True
            elif respond.data.values[0].startswith("autCat_"):
                stuffMenuStatus, needRemake = int(respond.data.values[0][-1]), True
                tri = [0,22][stuffMenuStatus]
            else:
                inter = respond
                respond = respond.data.values[0]

                if respond in opValues:
                    for a in range(0,len(opValues)):
                        if opValues[a] == respond:
                            destination = a
                            needRemake = True
                            break

                else:
                    await msg.edit(embeds=emb,components=[interactions.ActionRow(components=[interactions.SelectMenu(custom_id = "dunno", options=[interactions.SelectOption(label="None",value="None")],placeholder="Une autre action est en cours",disabled=True)])])
                    if ctx.author.id != user.owner:
                        await inventory(bot,inter,respond,delete=True,procur=user.owner)
                    else:
                        await inventory(bot,inter,respond,delete=True)

async def breakTheLimits(bot : interactions.Client, ctx : interactions.CommandContext, user : classes.char, msg : interactions.Message = None):
    if msg == None:
        try:
            msg = await ctx.send(embeds = await getRandomStatsEmbed(bot, [user], text="Chargement..."))
        except:
            msg = await ctx.channel.send(embeds = await getRandomStatsEmbed(bot, [user], text="Chargement..."))

    started = False

    while 1:
        if not(started):
            actBonus, valeurAjoute = "", 0
            if user.limitBreaks == [0,0,0,0,0,0,0]:
                actBonus = "`Pas de bonus`"
            else:
                valeur, nbBuff = 0, 0
                for cmpt in range(len(user.limitBreaks)):
                    if user.limitBreaks[cmpt] > 0:
                        actBonus += statsEmojis[cmpt]
                        nbBuff += 1
                        valeur = max(valeur, user.limitBreaks[cmpt])
                actBonus += " +{0}%".format(valeur)

                valeurAjoute = 30 * valeur * nbBuff

            hasSkillUpdated, lvl = True, user.level - 5
            nbExpectedSkills, nbSkills = 0, 0
            for cmpt in range(len(lvlToUnlockSkill)):
                if lvl >= lvlToUnlockSkill[cmpt]:
                    nbExpectedSkills += 1

            for skilly in user.skills:
                if type(skilly) == skill:
                    nbSkills += 1
            
            hasSkillUpdated = nbSkills >= nbExpectedSkills
            hasUpdatedStuff = True
            for stuffy in user.stuff:
                if stuffy.minLvl < user.level-10:
                    hasUpdatedStuff = False
                    break

            hasBonusPointsUpdated, updateBonus = user.points < 5, "\n\n"

            if not(hasBonusPointsUpdated and hasSkillUpdated and hasUpdatedStuff):
                updateBonus += "__Bonus de personnage à jour :__\nComplétez les conditions suivantes pour obtenir un bonus de 5% dans toutes vos satistiques principales :\n"
                updateBonus += "{0} {1}Avoir moins de **5 points bonus** non attribués{1}\n".format(["❌","✅"][hasBonusPointsUpdated],["","~~"][hasBonusPointsUpdated])
                updateBonus += "{0} {1}Avoir moins des équipements à votre niveau ou maximum **10 niveaux** en dessous du votre{1}\n".format(["❌","✅"][hasUpdatedStuff],["","~~"][hasUpdatedStuff])
                updateBonus += "{0} {1}Avoir **aucun** d'emplacement de compétences vides, à l'exeption du dernière emplacement sur il a été débloqué réçament{1}\n".format(["❌","✅"][hasSkillUpdated],["","~~"][hasSkillUpdated])

            else:
                updateBonus += "__Bonus de personnage à jour :__\n<:str:1012308654780850267>,<:sta:1012308718140002374>,<:cha:1012308755121188905>,<:agi:1012308798494482482><:pre:1012308901498208286><:int:1012308834661961748><:mag:1012308871525699604> +5%\n"           
            
            repEmb = interactions.Embed(title="__Dépassement de ses limites :__", color=user.color, description = "__En début de combats, votre personnage verra ses statistiques suivantes augmenter :__\n{0}{1}\n- Vous pouvez obtenir un nouveau set de bonus en déboursant quelques pièces, mais libre à vous de choisir si vous voulez l'utiliser ou passer.\n- En utilisant un nouveau set de bonus, l'ancien est perdu.\n- Plus votre set de bonus utilisé est puissant, plus la quantité de pièces devant être débourssée est élevée".format(actBonus,updateBonus))

            payButton = interactions.ActionRow(components=[interactions.Button(type=2, style=ButtonStyle.PRIMARY,label="Nouveau Set ({0})".format(100+valeurAjoute),emoji=getEmojiObject("<:coins:862425847523704832>"),custom_id="buy",disabled=user.currencies<100+valeurAjoute)])
            await msg.edit(embeds=repEmb,components=[payButton])

            def check(m):
                return int(m.author.id) == int(ctx.author.id)

            try:
                respond = await bot.wait_for_component(msg,payButton,check=check,timeout=60)
            except asyncio.exceptions.TimeoutError:
                await msg.edit(embeds=interactions.Embed(title="__Dépassement de ses limites :__", color=user.color, description = "En début de combats, votre personnage verra ses statistiques suivantes augmenter :\n{0}".format(actBonus)),components=[])
                return 0

        started = True
        user = loadCharFile(user=user)
        if user.currencies <= 100+valeurAjoute:
            await msg.edit(embeds=interactions.Embed(title="__Dépassement de ses limites :__", color=red, description = "Une erreur est survenue :\nVous n'avez pas les fonds nécessaires"))
            return 0

        user.currencies -= 100+valeurAjoute
        saveCharFile(user=user)
        rolledBonus = tablBreakingTheLimits[random.randint(0,len(tablBreakingTheLimits)-1)]

        rolledPower = random.randint(tablRangeLB[len(rolledBonus)-1][0],tablRangeLB[len(rolledBonus)-1][-1])

        bonusTxt = ""
        for cmpt in range(len(rolledBonus)):
            bonusTxt += statsEmojis[rolledBonus[cmpt]] + allStatsNames[rolledBonus[cmpt]] + "\n"
        bonusTxt += "+{0}%".format(rolledPower)

        repEmb = interactions.Embed(title="__Dépassement de ses limites :__", color = user.color, description = "__Votre bonus actuel est :__\n{0}\n\n__Vous venez de tirer :__\n{1}\n\nSouhaitez vous concerver ce nouveau set de bonus ?".format(actBonus, bonusTxt))

        repayButton = interactions.ActionRow(components=[interactions.Button(type=2, style=ButtonStyle.PRIMARY,label="Passer et retirer ({0})".format(100+valeurAjoute),emoji=getEmojiObject("<:coins:862425847523704832>"),custom_id="buy",disabled=user.currencies<100+valeurAjoute)])
        buttons = interactions.ActionRow(components=[confirmChange,rejectModernity])
        await msg.edit(embeds=repEmb,components=[buttons,repayButton])
        try:
            respond = await bot.wait_for_component(msg,[payButton,buttons],check=check,timeout=60)
        except asyncio.exceptions.TimeoutError:
            await msg.edit(embeds=interactions.Embed(title="__Dépassement de ses limites :__", color=user.color, description = "En début de combats, votre personnage verra ses statistiques suivantes augmenter :\n{0}".format(actBonus)),components=[])
            return 0

        if respond.custom_id == "nope":
            started = False
        elif respond.custom_id == "buy":
            pass
        else:
            for cmpt in range(0,MAGIE+1):
                if cmpt in rolledBonus:
                    user.limitBreaks[cmpt] = rolledPower
                else:
                    user.limitBreaks[cmpt] = 0
            
            saveCharFile(user=user)
            started = False

