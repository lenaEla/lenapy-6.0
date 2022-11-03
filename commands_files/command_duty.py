import discord
from discord_slash.context import SlashContext
from classes import *
from commands_files.command_fight import fight
from gestion import *
from advance_gestion import *
from commands_files.sussess_endler import *
from commands_files.alice_stats_endler import *
from index import *

nextButton = create_button(ButtonStyle.green,"Suivant","▶️","next")
fightButton = create_button(ButtonStyle.blue,"Combattre",getEmojiObject('<:turf:810513139740573696>'),"fight")
endButton = create_button(ButtonStyle.green,"Terminer","▶️","end")

DPT_MELEE,HEALER,BOOSTER,DPT_DIST = 0,1,2,3
aspiRoleTabl = [[BERSERK,TETE_BRULE,POIDS_PLUME,ENCHANTEUR],[ALTRUISTE,PREVOYANT,PROTECTEUR,VIGILANT],[IDOLE,INOVATEUR],[OBSERVATEUR,MAGE,SORCELER,ATTENTIF]]

async def playDuty(bot:discord.Client,msg:discord.Message,duty:duty,user:char,ctx:discord_slash.SlashContext):
    """Play a duty"""
    # Loading / Generating phase
    playerTeam:List[Union[char,tmpAllie]] = [user]
    roleList = [0,1,2,3]
    for cmpt in range(len(aspiRoleTabl)):
        if user.aspiration in aspiRoleTabl[cmpt]:
            try:
                roleList.remove(cmpt)
            except:
                pass

    for allie in duty.allies:
        if type(allie) != list:
            for cmpt in range(len(aspiRoleTabl)):
                if allie.aspiration in aspiRoleTabl[cmpt]:
                    try:
                        roleList.remove(cmpt)
                    except:
                        pass
                    playerTeam.append(allie)
        elif len(roleList) > 0:
            for ally in allie:
                for cmpt in roleList:
                    if ally.aspiration in aspiRoleTabl[cmpt]:
                        try:
                            roleList.remove(cmpt)
                        except:
                            pass
                        playerTeam.append(ally)
                        break
                if ally in playerTeam:
                    break
        else:
            playerTeam.append(allie)

    for cmpt in range(1,len(playerTeam)):
        playerTeam[cmpt].changeLevel(level=user.level,stars=user.stars,changeDict=False)

    for cmpt in range(len(duty.embedTxtList)):
        duty.embedTxtList[cmpt] = duty.embedTxtList[cmpt].format(
            userName = user.name,
            lena = tablAllAllies[0].icon, shushi = tablAllAllies[4].icon, luna = '<:luna:909047362868105227>', shihu = '<:shihu:909047672541945927>',
            alice = tablAllAllies[3].icon, sixtine = '<:sixtine:908819887059763261>', feli = '<:felicite:909048027644317706>',
            clemence = tablAllAllies[2].icon,
            shehisa = '<:shehisa:919863933320454165>', helene = tablAllAllies[6].icon, icelia = '<:icealia:909065559516250112>',
            iliana = '<:Iliana:926425844056985640>',
            gweny = tablAllAllies[1].icon, alty = '<:alty:906303048542990347>', klikli ='<:klikli:906303031837073429>', karai = '<:karail:974079383197339699>',
            lio = "<:lio:908754690769043546>", liu = "<:liu:908754674449018890>", liz = '<:lie:908754710121574470>', lia = "<:lia:908754741226520656>"
            )

    def reactCheck(m):
        return int(m.author_id) == user.owner

    embedIndex, result = 0, False
    while 1:
        embed, endButtons = discord.Embed(name = "__{0} ({1})__'".format(duty.serie,duty.numer),color=user.color,description=duty.embedTxtList[embedIndex]), []
        if duty.eventIndex[embedIndex] == None:
            endButtons = create_actionrow(nextButton)
        elif duty.eventIndex[embedIndex][0] == EVENT_CHOICE:
            endSelectOption = []
            for choice in range(1,len(duty.eventIndex[embedIndex])):
                endSelectOption.append(create_select_option(label=duty.eventIndex[embedIndex][choice][0],value=choice))
            endButtons = create_actionrow(create_select(options=endSelectOption))
        elif duty.eventIndex[embedIndex][0] == EVENT_FIGHT:
            endButtons = create_actionrow(fightButton)
        elif duty.eventIndex[embedIndex][0] == EVENT_END:
            endButtons = create_actionrow(endButton)  
        
        await msg.edit(embed=embed,components=endButtons)

        try:
            react = await wait_for_component(bot,msg,endButtons,reactCheck,3+(len(duty.embedTxtList[embedIndex])/180))
            if react.component_type == ComponentType.button:
                react = react.custom_id
            else:
                react = react.values[0]
        except TimeoutError:
            if duty.eventIndex[embedIndex] == None:
                react = nextButton["customId"]
            elif duty.eventIndex[embedIndex][0] == EVENT_CHOICE:
                react = 1
            elif duty.eventIndex[embedIndex][0] == EVENT_FIGHT:
                react = fightButton["customId"]
            elif duty.eventIndex[embedIndex][0] == EVENT_END:
                endButtons = endButton["customId"]
        
        if react == nextButton["customId"]:
            embedIndex += 1
        elif react == fightButton["customId"]:
            if duty.eventIndex[embedIndex][1] != None:
                enemyTeam = duty.eventIndex[embedIndex][1]
            else:
                enemyTeam = []
                while len(enemyTeam) < len(playerTeam):
                    alea = duty.enemies[random.randint(0,len(duty.enemies))]
                    alea.changeLevel(level=user.level)
                    enemyTeam.append(alea)
            
            try:
                fightResult = await fight(bot,playerTeam,enemyTeam,ctx,False,msg=msg)
            except:
                fightResult = None
            
            if fightResult:
                embedIndex += 1
            else:
                break
        elif react == endButton["customId"]:
            result = True
            break
        elif type(react) == int:
            embedIndex = duty.eventIndex[embedIndex][react][1]




