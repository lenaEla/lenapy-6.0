from datetime import datetime
import interactions
from gestion import saveCharFile, whatIsThat
from advance_gestion import addExpUser, getAutoStuff, getUserIcon
from data.expedition import *
from classes import char
from typing import Union, List
from advObjects.advAllies import *

aliceIcon = findAllie("Alice").icon

def formatingExpeditionText(text: str, team: List[char], allWomens: bool, sucessfull: Union[char, None] = None):
    if sucessfull == None:
        sucessfull = team[0]
    return text.format(
        tm1=team[0].name,
        tm1e=["", "e"][team[0].gender == GENDER_FEMALE],
        tm1il=["il", "elle"][team[0].gender == GENDER_FEMALE],
        tm1Il=["Il", "Elle"][team[0].gender == GENDER_FEMALE],
        tm2=team[1].name,
        tm2e=["", "e"][team[1].gender == GENDER_FEMALE],
        tm2il=["il", "elle"][team[1].gender == GENDER_FEMALE],
        tm2Il=["Il", "Elle"][team[1].gender == GENDER_FEMALE],
        tm3=team[2].name,
        tm3e=["", "e"][team[2].gender == GENDER_FEMALE],
        tm3il=["il", "elle"][team[2].gender == GENDER_FEMALE],
        tm3Il=["Il", "Elle"][team[2].gender == GENDER_FEMALE],
        tm4=team[3].name,
        tm4e=["", "e"][team[3].gender == GENDER_FEMALE],
        tm4il=["il", "elle"][team[3].gender == GENDER_FEMALE],
        tm4Il=["Il", "Elle"][team[3].gender == GENDER_FEMALE],
        tm5=team[4].name,
        tm5e=["", "e"][team[4].gender == GENDER_FEMALE],
        tm5il=["il", "elle"][team[4].gender == GENDER_FEMALE],
        tm5Il=["Il", "Elle"][team[4].gender == GENDER_FEMALE],
        tm6=team[5].name,
        tm6e=["", "e"][team[5].gender == GENDER_FEMALE],
        tm6il=["il", "elle"][team[5].gender == GENDER_FEMALE],
        tm6Il=["Il", "Elle"][team[5].gender == GENDER_FEMALE],
        tm7=team[6].name,
        tm7e=["", "e"][team[6].gender == GENDER_FEMALE],
        tm7il=["il", "elle"][team[6].gender == GENDER_FEMALE],
        tm7Il=["Il", "Elle"][team[6].gender == GENDER_FEMALE],
        tm8=team[7].name,
        tm8e=["", "e"][team[7].gender == GENDER_FEMALE],
        tm8il=["il", "elle"][team[7].gender == GENDER_FEMALE],
        tm8Il=["Il", "Elle"][team[7].gender == GENDER_FEMALE],
        tfe=["", "e"][allWomens],
        tfils=["ils", "elles"][allWomens],
        tfIls=["Ils", "Elles"][allWomens],
        su=sucessfull.name,
        sue=["", "e"][sucessfull.gender == GENDER_FEMALE],
        suil=["il", "elle"][sucessfull.gender == GENDER_FEMALE],
        suIl=["Il", "Elle"][sucessfull.gender == GENDER_FEMALE],
        alice=aliceIcon
    )

async def generateExpeditionReport(bot: interactions.Client, team: List[char], mainUser: char, starting: datetime, ctx):
    listEmbed: List[interactions.Embed] = []
    selectedExpedition, title, now, loot = copy.deepcopy(
        listExpedition[0]), "__Expédition__", datetime.now(parisTimeZone), 25
    title = "__Expedition : {0}__".format(selectedExpedition.name)
    #hoursSpend = (now - starting).total_seconds()//3600
    hoursSpend = 3

    moy = 0
    for user in team:
        moy += user.level

    moy, succed = int(moy/len(team)), 0

    # Filling the team
    if len(team) < 8:
        tablAllies = copy.deepcopy(tablAllAllies)
        if selectedExpedition.notAllowed != None:
            print(selectedExpedition.notAllowed)
            for a in tablAllies[:]:
                if a.name in selectedExpedition.notAllowed:
                    tablAllies.remove(a)

        while len(team) < 8:
            alea = tablAllAllies[random.randint(0, len(tablAllAllies)-1)]
            tablAllAllies.remove(alea)
            alea.changeLevel(moy)
            alea.stuff = [getAutoStuff(alea.stuff[0], alea), getAutoStuff(
                alea.stuff[1], alea), getAutoStuff(alea.stuff[2], alea)]
            team.append(alea)

    random.shuffle(team)

    allWomens = True
    for user in team:
        if user.gender != GENDER_FEMALE:
            allWomens = False
            break

    dictStamina = []
    for user in team:
        dictStamina.append([user, random.randint(90, 100)])
    dictStamina = dict(dictStamina)

    if len(selectedExpedition.intro) == 1:
        desc = selectedExpedition.intro[0]
    else:
        desc = selectedExpedition.intro[random.randint(
            0, len(selectedExpedition.intro)-1)]

    listEmbed.append(interactions.Embed(title=title, color=mainUser.color,description=formatingExpeditionText(desc, team, allWomens)))

    for nbEvent in range(hoursSpend):
        if len(selectedExpedition.events) > 1:
            event = selectedExpedition.events[random.randint(
                0, len(selectedExpedition.events)-1)]
        else:
            event = selectedExpedition.events[0]
        selectedExpedition.events.remove(event)
        wanted, desc = event.wantedStats, "__{0}__ :\n\n".format(event.name)
        if len(event.intro) > 1:
            desc += formatingExpeditionText(event.intro[random.randint(
                0, len(event.intro)-1)], team, allWomens) + "\n\n"
        else:
            desc += formatingExpeditionText(
                event.intro[0], team, allWomens) + "\n\n"

        listTeamMatesToSee = []
        if event.involved == SOLO_ALL:
            listTeamMatesToSee = team
        elif event.involved == SOLO_SOLO:
            listTeamMatesToSee = [team[event.wantedValue[0]]]
        elif event.involved == ALL_TEAM:
            tempChar = char(11, "Temp", level=moy)

            tablStats = tempChar.allStats()
            if type(wanted) == int:
                wanted = [wanted]

            for a in wanted:
                for user in team:
                    tablStats[a] += user.allStats()[a]

            tempChar.strength, tempChar.endurance, tempChar.charisma, tempChar.agility, tempChar.precision, tempChar.intelligence, tempChar.magie = tuple(
                tablStats)
            listTeamMatesToSee = [tempChar]

        if event.wantedType == STATS:
            haveSucced = False
            toSuccedReal = event.wantedValue * 0.2 + \
                (event.wantedValue * 0.8 * moy/50)

            for user in listTeamMatesToSee:
                if type(wanted) == int:
                    wanted = [wanted]

                sumStats = 0
                if user.owner != 11:
                    stamValue = dictStamina[user] / 100
                else:
                    sumSam = 0
                    for a in dictStamina:
                        sumSam += dictStamina[a]
                    stamValue = sumSam / 8 / 100

                for a in wanted:
                    sumStats += int(user.allStats()[a] * stamValue)

                successRate = sumStats / toSuccedReal * 1000
                if successRate > random.randint(0, 999):
                    haveSucced, succed = True, succed + 1
                    if len(event.success) > 1:
                        desc += formatingExpeditionText(event.success[random.randint(
                            0, len(event.success)-1)], team, allWomens, user)
                    else:
                        desc += formatingExpeditionText(
                            event.success[0], team, allWomens, user)

                    if user.owner != 11:
                        dictStamina[user] -= event.staminaReduceIfSuccess
                    else:
                        for a in dictStamina:
                            dictStamina[a] -= event.staminaReduceIfSuccess

                    loot += 5 * event.lootBonus

                    break
                else:
                    if user.owner != 11:
                        dictStamina[user] -= event.staminaReduceIfFailure
                    else:
                        for a in dictStamina:
                            dictStamina[a] -= event.staminaReduceIfFailure

            if not(haveSucced):
                if len(event.failure) > 1:
                    desc += formatingExpeditionText(event.failure[random.randint(
                        0, len(event.failure)-1)], team, allWomens, user)
                else:
                    desc += formatingExpeditionText(
                        event.failure[0], team, allWomens, user)

        if event.addTemp != None:
            alea = copy.deepcopy(findAllie(event.addTemp))
            if alea == None:
                print(event.addTemp, findAllie("Alice"))
            else:
                alea.changeLevel(moy)
                alea.stuff = [getAutoStuff(alea.stuff[0], alea), getAutoStuff(
                    alea.stuff[1], alea), getAutoStuff(alea.stuff[2], alea)]
                team.append(alea)
                dictStamina[alea] = random.randint(75,95)
                desc += "\n\n**__{0}__** rejoint l'équipe !".format(alea.name)
                if allWomens and alea.gender != GENDER_FEMALE:
                    allWomens = False

        listEmbed.append(interactions.Embed(title=title, color=[0x9FFFBC, 0xFF9FB2][not(haveSucced)], description=formatingExpeditionText(desc, team, allWomens)))

    recExp, recCoins = 40 * hoursSpend, 50 * hoursSpend
    desc, listLvlUp = "__Résultats :__\n__Expérience__ <:exp:926106339799887892> : +{0}, __Pièces__ <:coins:862425847523704832> : +{1}\n".format(
        recExp, recCoins), []
    for user in team:
        if type(user) == char:
            gainMsg, useIcon, userlevel = "", await getUserIcon(bot, user), [user.level, user.stars]
            user = await addExpUser(bot, "./userProfile/{0}.prof".format(user.owner), ctx, exp=recExp, coins=recCoins, send=False)
            for a in range(0, hoursSpend):
                if random.randint(0, 99) < loot:
                    drop = listAllBuyableShop[:]
                    temp = drop[:]

                    for b in drop:
                        if user.have(obj=b) or (type(b) == stuff and b.minLvl > user.level + 5):
                            temp.remove(b)
                        elif (type(b) == stuff and b.minLvl <= user.level + 5) or (type(b) == skill and b.havConds(user)):
                            temp.append(b)
                            temp.append(b)

                    if len(temp) > 0:
                        rvn = random.randint(0, 9)
                        if rvn < 5:
                            rand = temp[random.randint(0, len(temp)-1)]
                            newTemp = whatIsThat(rand)

                            if newTemp == 0:
                                user.weaponInventory += [rand]
                            elif newTemp == 1:
                                user.skillInventory += [rand]
                            elif newTemp == 2:
                                user.stuffInventory += [rand]

                            saveCharFile(user=user)
                            if useIcon in gainMsg:
                                gainMsg += f"{rand.emoji}"
                            else:
                                gainMsg += "\n{0} → {1}".format(
                                    useIcon, rand.emoji)
                        elif rvn < 7:
                            rdmExpGain = random.randint(20, 50)
                            user = await addExpUser(bot, "./userProfile/{0}.prof".format(user.owner), ctx, rdmExpGain, send=False)
                            if useIcon in gainMsg:
                                gainMsg += f"<:exp:926106339799887892>{rdmExpGain}"
                            else:
                                gainMsg += "\n{0} → <:exp:926106339799887892>{1}".format(useIcon, rdmExpGain)
                        else:
                            rdmCoinsGain = random.randint(50, 150)
                            user = await addExpUser(bot, "./userProfile/{0}.prof".format(user.owner), ctx, exp=0, coins=rdmCoinsGain, send=False)
                            if useIcon in gainMsg:
                                gainMsg += f"<:coins:862425847523704832>{rdmCoinsGain}"
                            else:
                                gainMsg += "\n{0} → <:coins:862425847523704832>{1}".format(
                                    useIcon, rdmCoinsGain)
            desc += gainMsg

            if user.level != userlevel[0]:
                listLvlUp.append("{0} : Niv. {1}{2} → Niv. {3}{4}\n".format(useIcon, userlevel[0], ["", "<:littleStar:925860806602682369>{0}".format(
                    userlevel[1])][userlevel[1] > 0], user.level, ["", "<:littleStar:925860806602682369>{0}".format(user.stars)][user.stars > 0]))

    if listLvlUp != []:
        temp = ""
        for a in listLvlUp:
            temp += a
        desc += "\n\n__Montée de niveau :__\nLe{0} personnage{0} suivant{0} {1} monté de niveau !\n".format(["", "s"][len(listLvlUp) > 1], ["a", "ont"][len(listLvlUp) > 1])+temp

    listEmbed.append(interactions.Embed(title=title, color=mainUser.color, description=desc))
    return listEmbed
