import discord, os
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from commands_files.alice_stats_endler import aliceStatsdbEndler, aliceStatsDb
from asyncio import sleep

async def procuration(ctx : discord.message,toProcur:discord.User):
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"

    if os.path.exists(pathUserProfile):
        user = loadCharFile(pathUserProfile)
        user.procuration.append(toProcur.id)

        if saveCharFile(pathUserProfile,user):
            await ctx.send(f"{toProcur.name} à bien été rajouté à la liste des personnes ayant procuration sur votre inventaire")
        else:
            await ctx.send(embed = errorEmbed("Procuration","Une erreure est survenue"))

    else:
            await ctx.send(embed = errorEmbed("Procuration","Vous n'avez pas commencé l'aventure"))

noneSuffisantJetonButton = create_button(ButtonStyle.gray,"Vous ne possédez pas de jetons",getEmojiObject('<:jeton:917793426949435402>'),disabled=True)
randomRouletteMsg = [
    "Les jeux sont fait, rien ne va plus !",
    "Tenter le diable",
    "Tentons le diable !",
    "Je sens que la chance est de mon côté !",
]

async def roulette(bot: discord.Client, ctx: discord.message, user: char):
    userJetonsCount = aliceStatsDb.getUserJetons(user)
    baseDesc = """
    La roulette est un moyen supplémentaire d'obtenir des équipements ou de l'argent.
    Après chaque combat, si le lanceur n'a pas réussi à obtenir quelque chose après une victoire, il a une probabilité d'obtenir un __<:jeton:917793426949435402> Jeton de Roulette__, nécessaire pour pouvoir lancer celle dernière.
    
    Les objets obtenables dans la roulette sont les mêmes que ceux disponibles dans le magasin et en butin. Leurs probabilités d'appararition dépend du pourcentage d'objet obtenu :
    <:coins:862425847523704832>, <:blocked:897631107602841600>, <:blocked:897631107602841600>, <:blocked:897631107602841600>, <:blocked:897631107602841600> : < 25%
    <:coins:862425847523704832>, <:coins:862425847523704832>, <:blocked:897631107602841600>, <:blocked:897631107602841600>, <:blocked:897631107602841600> : 25% -> 50%
    <:coins:862425847523704832>, <:coins:862425847523704832>, <:coins:862425847523704832>, <:blocked:897631107602841600>, <:blocked:897631107602841600> : 50% -> 75%
    <:coins:862425847523704832>, <:coins:862425847523704832>, <:coins:862425847523704832>, <:coins:862425847523704832>, <:blocked:897631107602841600> : 75% -> 100%
    <:coins:862425847523704832>, <:coins:862425847523704832>, <:coins:862425847523704832>, <:coins:862425847523704832>, <:coins:862425847523704832> : 100%
    
    Il n'est pas possible d'obtenir des objets déjà aquis dans la roulette. La quantité de pièces obtenue est égale au prix d'un équipement obtenable.
    
    Vous possédez **{0} __<:jeton:917793426949435402> Jeton de Roulette__**
    """.format(userJetonsCount)

    embed = discord.Embed(title="__Roulette :__",color=light_blue,description=baseDesc)
    if userJetonsCount == 0:
        await ctx.send(embed=embed,components=[create_actionrow(noneSuffisantJetonButton)])
        return 0

    button = create_button(ButtonStyle.blue,randomRouletteMsg[random.randint(0,len(randomRouletteMsg)-1)],getEmojiObject('<:jeton:917793426949435402>'),"go")

    msg = await ctx.send(embed=embed,components=[create_actionrow(button)])

    def check(m):
        print(int(m.author_id) == int(ctx.author_id))
        return int(m.author_id) == int(ctx.author_id)

    try:
        await wait_for_component(bot,msg,check=check,timeout=60)
    except:
        await msg.edit(embed=embed,components=[])
        return 0

    aliceStatsDb.updateJetonsCount(user,-1)
    gettenShop = userShopPurcent(user)
    if gettenShop == 100:
        toGet = [False,False,False,False,False]
    elif gettenShop < 100:
        toGet = [False,False,False,False,True]
    elif gettenShop < 75:
        toGet = [False,False,False,True,True]
    elif gettenShop < 50:
        toGet = [False,False,True,True,True]
    elif gettenShop < 25:
        toGet = [False,True,True,True,True]

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
        listPossibleEmojis.append('<:empty:866459463568850954>')
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
    await msg.edit(embed=discord.Embed(title="__Roulette :__",color=light_blue,description=possibleGainList+"\n\n"+"__Découvrez ce que vous avez gagné :__\n"+hidden),components=[])
    await sleep(60)
    await msg.edit(embed=discord.Embed(title="__Roulette :__",color=light_blue,description=possibleGainList+"\n\n"+"__Découvrez ce que vous avez gagné :__\n"+hidden.replace("||","")),components=[])