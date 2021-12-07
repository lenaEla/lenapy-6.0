import discord
from discord_slash.context import SlashContext
from classes import *
from gestion import *
from advance_gestion import *
from commands_files.sussess_endler import *
from commands_files.alice_stats_endler import *

async def adventureDutySelect(bot : discord.client,ctx : SlashContext, user : char): 
    """
        Function for the menu for selecting the duty\n
        Parameters :\n
        .bot : The bot's ``discord.client``
        .ctx : The contexte of the command
        .user : The ``char`` of the user\n
        Returns :\n
        .If sucessful :
            .actName, dutyName, msg
        .Else:
            .``None``, ``None``, ``None``
    """
    userProgressAct, userProgressDuty = aliceStatsDb.getAdventureProgress(user)
    tablAllreadyFinishedAct = []
    status,next = True,0

    if userProgressAct == None:
        next = True

    for cmpt in range(len(allActs)):
        if status:
            tablAllreadyFinishedAct.append(True)
        else:
            tablAllreadyFinishedAct.append(False)

        if next:
            status = False
            next = False

        if allActs[cmpt][0] == userProgressAct and userProgressDuty != None:
            status = False

        elif allActs[cmpt][0] == userProgressAct:
            next = True

    desc = "__Veillez sélectionner un act :__\n\n"

    actSelectOptions = []

    for cmpt in range(len(allActs)):
        if tablAllreadyFinishedAct[cmpt]:
            desc += "[Act {0}] - {1}\n".format(cmpt,allActs[cmpt][0])
            actSelectOptions.append(create_select_option(allActs[cmpt][0],allActs[cmpt][0]))
        else:
            desc += "`[Act {0}] - ".format(cmpt)
            for letter in allActs[cmpt][0]:
                desc += "?"
            desc += "`\n"

    embed = discord.Embed(title="__Aventure : Sélection de l'Act__",color=user.color,description=desc)
    mainMenu = await ctx.send(embed=embed,components=[create_actionrow(create_select(actSelectOptions,placeholder="Veillez sélectionner un act"))])

    def check(m):
        return m.author_id == ctx.author_id

    try:
        react = await wait_for_component(bot,mainMenu,check=check,timeout=60)
    except:
        await mainMenu.delete()
        return None, None, None

    embed = discord.Embed(title="__Aventure : Sélection de l'Act__",color=user.color,description=desc)
    await mainMenu.edit(embed=embed,components=[create_actionrow(getChoisenSelect(create_select(actSelectOptions,placeholder="Veillez sélectionner un act"),react.values[0]))])

    toReact = react
    react = react.values[0]

    selectedAct = None
    for cmpt in range(len(allActs)):
        if allActs[cmpt][0] == react:
            selectedAct = cmpt
            break

    if selectedAct == None:
        raise Exception("The selected act hasn't been found")

    desc = "__Veillez sélectionner une mission :__\n\n"

    if userProgressAct == None:
        userProgressAct = allActs[0][0]
    if userProgressDuty == None:
        userProgressDuty = allActs[selectedAct][1]

    unlock,actUnlock = True,react==userProgressAct
    dutySelectOptions = []
    for cmpt in range(1,len(allActs[selectedAct])):
        if unlock or not(actUnlock) :
            desc += "[{0}] - {1}\n".format(cmpt,allActs[selectedAct][cmpt][0].upper()+allActs[selectedAct][cmpt][1:-4].lower())
            dutySelectOptions.append(create_select_option(allActs[selectedAct][cmpt][0].upper()+allActs[selectedAct][cmpt][1:-4].lower(),allActs[selectedAct][cmpt][:-4]))
        else:
            desc += "`[{0}] - ".format(cmpt)
            for letter in allActs[selectedAct][cmpt]:
                desc += "?"
            desc += "`\n"

        if actUnlock and allActs[selectedAct][cmpt] == userProgressDuty:
            unlock = False

    missionSelect = create_select(dutySelectOptions,placeholder="Veillez sélectionner une mission")
    selectMenu = await toReact.send(embed=discord.Embed(title="__Sélection de la mission - {0}__".format(react),color=user.color,description=desc),components=[create_actionrow(missionSelect)])
    actSelected = react
    try:
        react = await wait_for_component(bot,selectMenu,check=check,timeout=60)
    except:
        await mainMenu.delete()
        return None, None, None

    await selectMenu.delete()
    react = react.values[0]

    return actSelected, react, mainMenu
