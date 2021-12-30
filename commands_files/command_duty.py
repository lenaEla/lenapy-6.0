import discord
from discord_slash.context import SlashContext
from classes import *
from gestion import *
from advance_gestion import *
from commands_files.sussess_endler import *
from commands_files.alice_stats_endler import *

nextButton = create_button(ButtonStyle.blue,"Suivant","▶️","next")
pauseButton = create_button(ButtonStyle.grey,"Faire une pause","⏸️","pause")
enableFavTeam = create_button(ButtonStyle.secondary,"Utiliser l'équipe favorite","<:littleStar:925860806602682369>","fav")
disabledFavTeam = create_button(ButtonStyle.secondary,"Vous n'avez pas d'équipe favorite","<:littleStar:925860806602682369>","fav",disabled=True)
errorFavTeam = create_button(ButtonStyle.red,"Erreur lord du chargement de l'équipe favorite","<:littleStar:925860806602682369>","fav",disabled=True)
classicButtons = [create_actionrow(pauseButton,nextButton)]

async def adventureDutySelect(bot : discord.client, ctx : SlashContext, user : char): 
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

async def dutyTextAff(message : discord.Message, text : dutyText, user : char, duty : duty):
    """Generate the embed for a ``dutyText`` and edit the ``message`` given in parameters\n
    Return the ``len`` of the embed's description"""
    desc = text.text.format(
        charName=user.name,
        Lena="<:lena:909047343876288552>")

    embed = discord.Embed(title="__{0} : {1}__".format(duty.act,duty.name),color=user.color,description=desc)

    await message.edit(embed=embed,components=classicButtons)
    return len(desc)

async def pauseDuty(message : discord.Message, duty : duty, dutyText : dutyText, user : char):
    """Generate the pause data and update it into the database"""
    pauseData = duty.act + "|" + duty.name + "|" + dutyText.ref + "|"

    teamTemp, cmpt = ["-","-","-","-","-"],0
    for temp in duty.team:
        teamTemp[cmpt] = temp.name
        cmpt += 1

    for temp in teamTemp:
        pauseData+=temp+"|"

    aliceStatsDb.updatePauseData(user,pauseData)

    message.edit(embed = discord.Embed(title="__{0} : {1}__".format(duty.act,duty.name),color=user.color,description="Votre mission a été mise en pause\n\nVous pouvez la reprendre quand vous voulez avec /adventure duty resume"),components=[])
    return 0

def partySelect(duty : duty):
    listMeleeDPT,listDistDPT,listHealer,listShielder,listBoost,listOther = [],[],[],[],[],[]

    for tempAllie in tablAllAllies:
        if tempAllie.isUnlock(duty):
            if tempAllie.aspiration in [BERSERK,POIDS_PLUME,ENCHANTEUR,TETE_BRULE]:
                listMeleeDPT.append(tempAllie)
            elif tempAllie.aspiration in [OBSERVATEUR,MAGE,TETE_BRULE]:
                listDistDPT.append(tempAllie)
            elif tempAllie.aspiration == ALTRUISTE:
                listHealer.append(tempAllie)
            elif tempAllie.aspiration == PREVOYANT:
                listShielder.append(tempAllie)
            elif tempAllie.aspiration in [IDOLE,PROTECTEUR]:
                listBoost.append(tempAllie)
            else:
                listOther.append(tempAllie)

    for a in [listMeleeDPT,listDistDPT,listHealer,listShielder,listBoost,listOther]:
        temp = []
        for b in a:
            temp.append(b.name)

        print(temp)


async def mainDuty(bot: discord.Client, message : discord.Message, ctx : SlashContext, user: char, duty: duty, resumed : Union[None,dict] = None):
    if resumed != None:
        while duty.actText().ref != resumed["ref"]:
            duty.cmpt += 1
            if duty.cmpt >= len(duty.dutyTextList):
                print("DutyError : The duty's resume point havn't been found")
                await message.edit(embed=discord.Embed(title="__{0} : {1}__",color=red,description="Une erreur est survenue :\nLe point de reprise n'a pas pu être retrouvé"))
                return 0

        tempDutyTeam = []
        for temp in resumed["team"]:
            temporaly = findAllie(temp)
            if temporaly == None:
                print("DutyError : A duty's team member hav'nt been found")
                await message.edit(embed=discord.Embed(title="__{0} : {1}__",color=red,description="Une erreur est survenue :\nUn allié n'a pas pu être retrouvé"))
                return 0
            else:
                tempDutyTeam.append(temporaly)

        duty.team = tempDutyTeam

    else:
        favTeam = aliceStatsDb.getTeamFavData(user)
        if favTeam == False:
            favTeamButton = errorFavTeam
        elif favTeam == None:
            favTeamButton = disabledFavTeam
        else:
            favTeamButton = enableFavTeam