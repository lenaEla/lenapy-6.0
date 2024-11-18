import copy
from interactions import *
from adv import *
from constantes import *
from gestion import getEmojiObject, whatIsThat
from advance_gestion import infoStuff,infoWeapon,infoSkill,getUserIcon,infoAllie,infoEnnemi
from commands_files.achievement_handler import *
from commands_files.command_inventory import *

ENC_ACC, ENC_GEAR, ENC_SHOE, ENC_WEAP, ENC_SKILL, ENC_ALLIES, ENC_ENEMIES, ENC_BOSS, ENC_LOCKED, ENC_ACHIV = tuple(range(10))

async def encylopedia(bot : interactions.Client, ctx : interactions.SlashContext, destination : int, user : char):
    """The main function for the encyclopedia command"""

    def check(m):
        m = m.ctx
        return m.author.id == ctx.author.id and m.message.id == msg.id

    msg = None
    stuffed = [[],[],[]]
    for a in [0,1,2]:
        for b in stuffs:
            if b.type == a:
                stuffed[a].append(b.emoji)

    # Randomly select emojis for the "Destionation" select Menu
    value = copy.deepcopy(destination)
    opValues,destination,fullValue=["accessoires","vetements","chaussures","armes","competences","tempAlies","ennemies","boss","locked","achivements"],0,["Accessoires","Vêtements","Chaussures","Armes","Compétences","Alliés","Ennemis","Boss","Objets non-possédés","Succès"]
    valueIcon = [stuffed[0][random.randint(0,len(stuffed[0])-1)],stuffed[1][random.randint(0,len(stuffed[1])-1)],stuffed[2][random.randint(0,len(stuffed[2])-1)],weapons[random.randint(0,len(weapons)-1)].emoji,skills[random.randint(0,len(skills)-1)].emoji,tablAllAllies[random.randint(0,len(tablAllAllies)-1)].icon,tablAllEnnemies[random.randint(0,len(tablAllEnnemies)-1)].icon,tablBoss[random.randint(0,len(tablBoss)-1)].icon,'<:splatted2:727586393173524570>','<:ls1:868838101752098837>']
    tri = 0
    for a in range(0,len(opValues)):
        if value == opValues[a]:
            destination=a
            break

    needRemake = True
    userIcon = await getUserIcon(bot,user)

    # Start the command
    while 1:
        destOptions = []
        for a in range(0,len(opValues)):
            destOptions+=[interactions.StringSelectOption(label=fullValue[a],value=opValues[a],emoji=getEmojiObject(valueIcon[a]),default=opValues[a]==opValues[destination])]

        destSelect = interactions.ActionRow(interactions.StringSelectMenu(destOptions,custom_id = "destoptions"))

        # The options for the filter menu. Change with the selected destination
        options = [
            interactions.StringSelectOption(label="Ordre Alphabétique ↓",value="0",emoji=PartialEmoji(name='🇦'),default=0==tri),
            interactions.StringSelectOption(label="Ordre Alphabétique ↑",value="1",emoji=PartialEmoji(name='🇿'),default=1==tri)
        ]

        if destination in [ENC_ACC, ENC_GEAR, ENC_SHOE, ENC_WEAP, ENC_SKILL]:
            options += [
            interactions.StringSelectOption(label="Possédé",value="2",emoji=PartialEmoji(name='🔓'),default=2==tri),
            interactions.StringSelectOption(label="Non possédé",value="3",emoji=PartialEmoji(name='🔒'),default=3==tri)
            ]
        
        if destination in [ENC_ACC, ENC_GEAR, ENC_SHOE, ENC_WEAP]:
            options+=[
                interactions.StringSelectOption(label="Force",value="4",emoji=getEmojiObject(statsEmojis[0]),default=4==tri),
                interactions.StringSelectOption(label="Endurance",value="5",emoji=getEmojiObject(statsEmojis[1]),default=5==tri),
                interactions.StringSelectOption(label="Charisme",value='6',emoji=getEmojiObject(statsEmojis[2]),default=6==tri),
                interactions.StringSelectOption(label="Agilité",value="7",emoji=getEmojiObject(statsEmojis[3]),default=7==tri),
                interactions.StringSelectOption(label="Précision",value="8",emoji=getEmojiObject(statsEmojis[4]),default=8==tri),
                interactions.StringSelectOption(label="Intelligence",value="9",emoji=getEmojiObject(statsEmojis[5]),default=9==tri),
                interactions.StringSelectOption(label="Magie",value="10",emoji=getEmojiObject(statsEmojis[6]),default=10==tri),
                interactions.StringSelectOption(label="Résistance",value="11",emoji=getEmojiObject(statsEmojis[7]),default=11==tri),
                interactions.StringSelectOption(label="Pénétration",value="12",emoji=getEmojiObject(statsEmojis[8]),default=12==tri),
                interactions.StringSelectOption(label="Critique",value="13",emoji=getEmojiObject(statsEmojis[9]),default=13==tri)]

        elif destination == ENC_SKILL:
            options += [
                interactions.StringSelectOption(label="Dégâts",value="14",emoji=getEmojiObject(statsEmojis[ACT_DIRECT_FULL]),default=tri==14),
                interactions.StringSelectOption(label="Dégâts indirects",value="15",emoji=getEmojiObject(statsEmojis[ACT_INDIRECT_FULL]),default=tri==15),
                interactions.StringSelectOption(label="Soins",value="16",emoji=getEmojiObject(statsEmojis[ACT_HEAL_FULL]),default=tri==16),
                interactions.StringSelectOption(label="Armure",value="17",emoji=getEmojiObject(statsEmojis[ACT_SHIELD_FULL]),default=tri==17),
                interactions.StringSelectOption(label="Boost",value='18',emoji=getEmojiObject(statsEmojis[ACT_BOOST_FULL]),default=tri==18),
                interactions.StringSelectOption(label="Malus",value="19",emoji=getEmojiObject(statsEmojis[ACT_BOOST_FULL]),default=tri==19),
                interactions.StringSelectOption(label="Invocation",value="20",emoji=getEmojiObject("<:sprink1:887747751339757599>"),default=tri==20),
                interactions.StringSelectOption(label="Passif",value="21",emoji=getEmojiObject("<:stratageme:937370395605086229>"),default=tri==21)
            ]

        elif destination in [ENC_ALLIES, ENC_ENEMIES, ENC_BOSS]:
            options += [
                interactions.StringSelectOption(label="DPT - Mêlée",value="21",emoji=getEmojiObject('<:sworddance:894544710952173609>'),default=tri==21),
                interactions.StringSelectOption(label="DPT - Distance",value="22",emoji=getEmojiObject('<:preciseShot:916561817969500191>'),default=tri==22),
                interactions.StringSelectOption(label="Supports",value="23",emoji=getEmojiObject('<:alice:893463608716062760>'),default=tri==23),
                interactions.StringSelectOption(label="Soigneur / Armuriers",value="24",emoji=getEmojiObject('<:absorb:971788658782928918>'),default=tri==24),
            ]
        elif destination in [ENC_ACHIV]:
            options += [
            interactions.StringSelectOption(label="Terminés",value="14",emoji=PartialEmoji(name='🔓'),default=13==tri),
            interactions.StringSelectOption(label="Non terminés",value="15",emoji=PartialEmoji(name='🔒'),default=14==tri)
            ]

        sortOptions = interactions.StringSelectMenu(options,custom_id = "sortMenue=")
    
        if needRemake:                          # The "TablToSee" generation
            tablToSee = []
            if destination in [0,1,2]:
                for a in stuffs:
                    if a.type == destination:
                        tablToSee.append(a)
            elif destination == 3:
                tablToSee = weapons[:]
            elif destination == 4:
                tablToSee = skills[:]
                if tri >= 14:
                    typeTabl = [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE,[TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_RESURECTION,TYPE_INDIRECT_REZ],TYPE_ARMOR,TYPE_BOOST,TYPE_MALUS,TYPE_SUMMON,TYPE_PASSIVE]
                    see = typeTabl[tri-14]
                    if type(see) != list:
                        for ski in tablToSee[:]:
                            if not(ski.type == see or (ski.effects != [None] and findEffect(ski.effects[0]).type == see) or (ski.effectAroundCaster != None and ski.effectAroundCaster[0] == see) or (ski.effectOnSelf != None and findEffect(ski.effectOnSelf).type == see)):
                                tablToSee.remove(ski)
                    else:
                        for ski in tablToSee[:]:
                            if not(ski.type in see or (ski.effects != [None] and findEffect(ski.effects[0]).type in see) or (ski.effectAroundCaster != None and ski.effectAroundCaster[0] in see) or (ski.effectOnSelf != None and findEffect(ski.effectOnSelf).type in see)):
                                tablToSee.remove(ski)

                if tri in [14,16]:
                    tablToSee.sort(key=lambda ballerine:getSortSkillValue(ballerine,tri),reverse=True)
                elif tri in [15]:
                    tablToSee.sort(key=lambda ballerine:getSortSkillValue(ballerine,tri),reverse=True)
                elif tri in [17]:
                    tablToSee.sort(key=lambda ballerine:getSortSkillValue(ballerine,tri),reverse=True)
            elif destination == 5:
                for a in tablAllAllies+tablVarAllies:
                    if a not in tablToSee:
                        tablToSee.append(a)
            elif destination == 6:
                tablToSee = tablUniqueEnnemies[:]
            elif destination == 7:
                for a in tablBoss+tablRaidBoss+tablBossPlus:
                    trouv=False
                    for b in tablToSee:
                        if a.name == b.name:
                            trouv=True
                            break
                    if not(trouv):
                        tablToSee.append(a)

            elif destination == 8:
                tablToSee = weapons[:]+stuffs[:]+skills[:]
                for a in tablToSee[:]:
                    if user.have(a):
                        tablToSee.remove(a)

            elif destination==9:
                pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".json"
                user = loadCharFile(pathUserProfile)
                tablToSee = achivementStand.getSuccess(user)
                tablToSee = tablToSee.tablAllSuccess()

            if destination in [0,1,2,3,9]:
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
                elif tri in [14,15]:
                    tablToSee.sort(key=lambda ballerine:ballerine.haveSucced, reverse=not(tri-14))
                else:
                    tablToSee.sort(key=lambda ballerine:ballerine.name, reverse=tri)
            elif destination in [5,6,7] and tri >= 21:
                for ent in tablToSee[:]:
                    if tri == 21 and ent.aspiration not in [BERSERK,POIDS_PLUME,TETE_BRULEE,ENCHANTEUR]:
                        tablToSee.remove(ent)
                    elif tri == 22 and ent.aspiration not in [OBSERVATEUR,ATTENTIF,MAGE,SORCELER]:
                        tablToSee.remove(ent)
                    elif tri == 23 and ent.aspiration not in [IDOLE,INOVATEUR]:
                        tablToSee.remove(ent)
                    elif tri == 24 and ent.aspiration not in [PROTECTEUR,ALTRUISTE,VIGILANT,PREVOYANT]:
                        tablToSee.remove(ent)
                tablToSee.sort(key=lambda ballerine:ballerine.name)
            else:
                tablToSee.sort(key=lambda ballerine:ballerine.name,reverse=tri==1)
            
            if tri == 1:
                tablToSee.sort(key=lambda name: name.name, reverse=True)
            lenTabl = len(tablToSee)
            maxPage=lenTabl//10
            page=0
            needRemake = False

        # Base description for the selected destination
        if destination in [ENC_ACC, ENC_GEAR, ENC_SHOE, ENC_WEAP, ENC_SKILL, ENC_LOCKED]:                          # Stuffs, Weapons and Skills
            desc = f"{userIcon} : Vous possédez déjà cet objet\n<:coinsn_t:885921771071627304> : Cet ebjet ne peut pas être obtenu dans le Magasin ou en butin"
        elif destination == ENC_ALLIES:                                    # Alliés Temps
            desc = "Les alliés temporaires rejoignent automatiquement un combat pour remplir les équipes n'ayant pas assez de membres"
        elif destination == ENC_ENEMIES:                                    # Ennemis
            desc = "Les ennemis sont là pour vous opposer une petite résistance tout de même"
        elif destination == ENC_BOSS:                                    # Boss's
            desc = "Chaque combat a une chance sur trois de voir un Boss parmis les ennemis"
        elif destination == ENC_ACHIV:                                    # Sussess
            desc = "Liste des succès :"

        firstOptions = []
        if page != 0:
            firstOptions+=[interactions.StringSelectOption(label="Page précédente",value="return",emoji=PartialEmoji(name="◀️"))]

        if lenTabl != 0: # Génération des pages
            if destination <= ENC_SKILL or destination == ENC_LOCKED:
                if page != maxPage:
                    maxi = (page+1)*10
                else:
                    maxi = lenTabl
                
                mess, tempFirstOptions = getInvMenu(tablToSee[(page)*10:maxi])
                firstOptions = firstOptions + tempFirstOptions

            elif destination != ENC_ACHIV:
                mess = ""
                if page != maxPage:
                    maxi = (page+1)*10
                else:
                    maxi = lenTabl
                for a in tablToSee[(page)*10:maxi]:
                    mess += "{0}{1} __{2}__\n{3} {4}. | {5} |".format(a.icon,["",a.splashIcon][a.splashIcon!=None],a.name,aspiEmoji[a.aspiration],inspi[a.aspiration][0:3],a.weapon.emoji)
                    firstOptions+=[interactions.StringSelectOption(label=unhyperlink(a.name),value=a.name,emoji=getEmojiObject([a.icon,a.splashIcon][a.splashIcon!=None]))]

                    for b in a.skills:
                        if type(b) == skill:
                            mess += f" {b.emoji}"

                    mess+="\n\n"
            else:
                mess = ""
                if page != maxPage:
                    maxi = (page+1)*10
                else:
                    maxi = lenTabl
                for a in tablToSee[(page)*10:maxi]:
                    succed = ""
                    if a.haveSucced:
                        succed = "~~"
                    emo = ""
                    if a.emoji != None:
                        emo = a.emoji + " "
                    mess += f"**__{succed}{emo}{a.name}{succed}__**"

                    if a.haveSucced:
                        mess += f" ({userIcon})"

                    mess += f"\n*{a.description.format(a.countToSucced)}*\nProgression : **{min(a.count,a.countToSucced)}**/{a.countToSucced}"

                    recompense = ""
                    if a.recompense != [None]:
                        for rep in a.recompense:
                            what = whatIsThat(rep)
                            if what == 0:
                                que = findWeapon(rep)
                            elif what == 1:
                                que = findSkill(rep)
                            elif what == 2:
                                que = findStuff(rep)
                            elif what == 3:
                                que = findOther(rep)

                            recompense += que.emoji + " "

                    if recompense != "":
                        mess += "\nRécompense : "+recompense

                    mess+="\n\n"

            mess = reduceEmojiNames(mess)
            if len(mess) > 4056: # Mess abrégé
                mess = unemoji(mess)

        else:
            mess = "Il n'y a rien à afficher dans cette catégorie"

        if page < maxPage:
            firstOptions+=[interactions.StringSelectOption(label="Page suivante",value="next",emoji=PartialEmoji(name="▶️"))]

        if len(firstOptions) > 0:
            firstSelect = interactions.StringSelectMenu(firstOptions,custom_id = "seeEquipPage",placeholder="Changez de page ou voir la page de l'équipement")
        else:
            firstSelect = interactions.StringSelectMenu(interactions.StringSelectOption(label="None",value="None"),custom_id = "NothingToShow",placeholder="Cette catégorie n'a rien à afficher",disabled=True)

        emb = interactions.Embed(title="Encyclopédie",description=desc+"\n\n__Page **{0}** / {1} :__\n".format(page+1,maxPage+1)+mess,color=user.color)

        if msg == None:     # Send the message for the first loop
            try:
                msg = await ctx.send(embeds=emb,components=[destSelect,interactions.ActionRow(sortOptions),interactions.ActionRow(firstSelect)])
            except:
                msg = await ctx.channel.send(embeds=emb,components=[destSelect,interactions.ActionRow(sortOptions),interactions.ActionRow(firstSelect)])

        else:
            await msg.edit(embeds=emb,components=[destSelect,interactions.ActionRow(sortOptions),interactions.ActionRow(firstSelect)])

        try:
            respond = await bot.wait_for_component(msg,check=check,timeout=180)
            respond: ComponentContext = respond.ctx
        except:
            await msg.edit(embeds=emb,components=[])
            break

        if respond.values[0].isdigit():
            respond = int(respond.values[0])

            if respond in [0,1]:
                needRemake = True
            else:
                if destination in [0,1,2,3]:
                    tablToSee.sort(key=lambda ballerine: ballerine.name)
                    if respond in [2,3]: tablToSee.sort(key=lambda ballerine:user.have(ballerine), reverse=not(respond-2))
                    elif respond == 4: tablToSee.sort(key=lambda ballerine:ballerine.strength + max(ballerine.negativeDirect *-1,ballerine.negativeIndirect *-1), reverse=True)
                    elif respond == 5: tablToSee.sort(key=lambda ballerine:ballerine.endurance, reverse=True)
                    elif respond == 6: tablToSee.sort(key=lambda ballerine:ballerine.charisma + max(ballerine.negativeHeal *-1,ballerine.negativeBoost *-1), reverse=True)
                    elif respond == 7: tablToSee.sort(key=lambda ballerine:ballerine.agility, reverse=True)
                    elif respond == 8: tablToSee.sort(key=lambda ballerine:ballerine.precision, reverse=True)
                    elif respond == 9: tablToSee.sort(key=lambda ballerine:ballerine.intelligence + max(ballerine.negativeShield *-1,ballerine.negativeBoost *-1), reverse=True)
                    elif respond == 10: tablToSee.sort(key=lambda ballerine:ballerine.magie + max(ballerine.negativeDirect *-1,ballerine.negativeIndirect *-1), reverse=True)
                    elif respond == 11: tablToSee.sort(key=lambda ballerine:ballerine.resistance, reverse=True)
                    elif respond == 12: tablToSee.sort(key=lambda ballerine:ballerine.percing, reverse=True)
                    elif respond == 13: tablToSee.sort(key=lambda ballerine:ballerine.critical, reverse=True)
                    elif respond in [14,15]: tablToSee.sort(key=lambda ballerine:ballerine.haveSucced, reverse=not(respond-14))
                else: needRemake = True
            tri=respond

        else:
            inter: ComponentContext = respond
            respond = respond.values[0]

            if respond == "return": page -= 1
            elif respond == "next": page += 1

            elif respond in opValues:
                for a in range(0,len(opValues)):
                    if opValues[a] == respond:destination = a; needRemake = True; break
            elif destination in [0,1,2]: await inter.defer(); await inter.send(embeds=infoStuff(findStuff(respond),user,ctx))
            elif destination == 3: await inter.defer(); await inter.send(embeds=infoWeapon(findWeapon(respond),user,ctx))
            elif destination == 4: await inter.defer(); await inter.send(embeds=infoSkill(findSkill(respond),user,ctx))
            elif destination == ENC_ALLIES:
                await inter.defer()
                lvl, tempMachin, addLvl = MAXLEVEL, None, 0
                procurData = None
                for procurName, procurStuff in procurTempStuff.items():
                    if respond == procurName:
                        addLvl = procurStuff[0]
                        procurData = procurStuff
                        break
                altBuildNb = -1
                while 1:
                    lvlAdded = lvl + addLvl
                    ally = copy.deepcopy(findAllie(respond))

                    if altBuildNb != -1:
                        tempBuild = ally.changeDict[altBuildNb]
                        initBuildProb = 100
                        for chDict in ally.changeDict: initBuildProb = initBuildProb - chDict.proba
                        ally.changeDict[altBuildNb] = tempAltBuild(proba=initBuildProb,aspiration=ally.aspiration,weap=ally.weapon,stuffs=ally.stuff,skills=ally.skills,elements=[ally.element,ally.secElement],bonusPoints=ally.bonusPoints,buildName="Build Original",buildIcon=ally.icon)
                        
                        if tempBuild.aspiration != None: ally.aspiration = tempBuild.aspiration
                        if tempBuild.weapon != None: ally.weapon = tempBuild.weapon
                        if tempBuild.stuff != None: ally.stuff = tempBuild.stuff
                        if tempBuild.skills != None: ally.skills = tempBuild.skills
                        if tempBuild.elements != None: ally.element, ally.secElement = tempBuild.elements[0], tempBuild.elements[1]
                        if tempBuild.bonusPoints != None: ally.bonusPoints = tempBuild.bonusPoints
                        if tempBuild.icon != None: ally.icon = tempBuild.icon
                        if tempBuild.splashIcon != None: ally.splashIcon = tempBuild.splashIcon
                        if tempBuild.chips != None: ally.equippedChips = tempBuild.chips[0]
                    ally.changeLevel(lvl,changeDict=False)

                    if procurData == None and (altBuildNb == -1 or (altBuildNb != -1 and tempBuild.proba > 0)): ally.stuff = [getAutoStuff(ally.stuff[0],ally),getAutoStuff(ally.stuff[1],ally),getAutoStuff(ally.stuff[2],ally)]
                    elif procurData != None: ally.stuff = [stuff(procurData[1][0],procurData[1][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*lvlAdded),int(procurData[4][1][0]*procurData[4][1][1]*lvlAdded),int(procurData[4][2][0]*procurData[4][2][1]*lvlAdded),int(procurData[4][3][0]*procurData[4][3][1]*lvlAdded),int(procurData[4][4][0]*procurData[4][4][1]*lvlAdded),int(procurData[4][5][0]*procurData[4][5][1]*lvlAdded),int(procurData[4][6][0]*procurData[4][6][1]*lvlAdded),int(procurData[4][7][0]*procurData[4][7][1]*lvlAdded),int(procurData[4][8][0]*procurData[4][8][1]*lvlAdded),int(procurData[4][9][0]*procurData[4][9][1]*lvlAdded),emoji=procurData[1][2]),stuff(procurData[2][0],procurData[2][1],1,0,int(procurData[4][0][0]*procurData[4][0][1]*lvlAdded),int(procurData[4][1][0]*procurData[4][1][1]*lvlAdded),int(procurData[4][2][0]*procurData[4][2][1]*lvlAdded),int(procurData[4][3][0]*procurData[4][3][1]*lvlAdded),int(procurData[4][4][0]*procurData[4][4][1]*lvlAdded),int(procurData[4][5][0]*procurData[4][5][1]*lvlAdded),int(procurData[4][6][0]*procurData[4][6][1]*lvlAdded),int(procurData[4][7][0]*procurData[4][7][1]*lvlAdded),int(procurData[4][8][0]*procurData[4][8][1]*lvlAdded),int(procurData[4][9][0]*procurData[4][9][1]*lvlAdded),emoji=procurData[2][2]),stuff(procurData[3][0],procurData[3][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*lvlAdded),int(procurData[4][1][0]*procurData[4][1][1]*lvlAdded),int(procurData[4][2][0]*procurData[4][2][1]*lvlAdded),int(procurData[4][3][0]*procurData[4][3][1]*lvlAdded),int(procurData[4][4][0]*procurData[4][4][1]*lvlAdded),int(procurData[4][5][0]*procurData[4][5][1]*lvlAdded),int(procurData[4][6][0]*procurData[4][6][1]*lvlAdded),int(procurData[4][7][0]*procurData[4][7][1]*lvlAdded),int(procurData[4][8][0]*procurData[4][8][1]*lvlAdded),int(procurData[4][9][0]*procurData[4][9][1]*lvlAdded),emoji=procurData[3][2])]
                    options, cmpt = [], 0
                    for stuffy in [ally.weapon]+ally.skills:
                        if type(stuffy) in [skill,weapon]: options.append(interactions.StringSelectOption(label=stuffy.name,value=str(cmpt),emoji=getEmojiObject(stuffy.emoji)))
                        cmpt+=1
                    returnButton = interactions.ActionRow(interactions.Button(style=1 ,label="Retour",custom_id="return"))
                    select = interactions.ActionRow(interactions.StringSelectMenu(options,custom_id = "seeMoreInfoMenue",placeholder="Voir plus d'informations sur les équipements"))
                    lvlSelectOption = []
                    for a in range(1,MAXLEVEL//10+1): lvlSelectOption.append(interactions.StringSelectOption(label="Niveau {0}".format(10*a),value="lvl_{0}".format(10*a+addLvl),default=lvl==10*a))
                    lvlSelect = interactions.ActionRow(interactions.StringSelectMenu(lvlSelectOption,custom_id = "selectLvlMenu",placeholder="Choisir un niveau"))
                    emb = infoAllie(ally)

                    if ally.changeDict != None:
                        optionChDict, cmpt = [], 0
                        for chDict in ally.changeDict:
                            tmpName, tmpIcon = "Build Alternatif {0}".format(cmpt+1), getEmojiObject(aspiEmoji[ally.aspiration])
                            if chDict.buildName != None: tmpName = chDict.buildName
                            if chDict.buildIcon != None: tmpIcon = getEmojiObject(chDict.buildIcon)
                            optionChDict.append(StringSelectOption(label=tmpName,value="altBuild_{0}".format(cmpt),emoji=tmpIcon))
                            cmpt += 1

                        chDictSelect = [ActionRow(StringSelectMenu(optionChDict,custom_id="chDictSelect",placeholder="Voir un build alternatif"))]
                    else: chDictSelect = []
                    if tempMachin == None:
                        try: tempMachin = await inter.send(embeds=emb,components=[returnButton, select, lvlSelect]+chDictSelect)
                        except Exception as e: print_exc(); raise e
                    else: await tempMachin.edit(embeds=emb,components=[returnButton,select,lvlSelect]+chDictSelect)
                    try: resp2 = await bot.wait_for_component(messages=tempMachin,timeout=60); resp2: ComponentContext = resp2.ctx
                    except: await tempMachin.edit(embeds=emb,components=[]); break
                    try:
                        if resp2.component_type == ComponentType.BUTTON: await tempMachin.delete(); break
                        elif resp2.values[0].startswith("lvl_"): lvl = int(resp2.values[0][4:])
                        elif resp2.values[0].startswith("altBuild_"): altBuildNb = int(resp2.values[0].replace("altBuild_",""))
                        else:
                            await resp2.defer()
                            tablStuff = [ally.weapon]+ally.skills
                            obj = tablStuff[int(resp2.values[0])]
                            if type(obj) == weapon: await resp2.send(embeds=infoWeapon(obj,user,ctx))
                            elif type(obj) == skill: await resp2.send(embeds=infoSkill(obj,user,ctx))
                            elif type(obj) == stuff: await resp2.send(embeds=infoStuff(obj,user,ctx))
                    except Exception as e:
                        print_exc(); await resp2.send("Une erreur est survenue lors de l'affichage de l'objet :\n{0}".format(e))

            elif destination in [6,7]:
                await inter.defer()
                options = []
                ennemi = findEnnemi(respond)
                cmpt = 0
                for stuffy in [ennemi.weapon]+ennemi.skills:
                    if type(stuffy) in [skill,weapon]:
                        options.append(interactions.StringSelectOption(label=stuffy.name,value=str(cmpt),emoji=getEmojiObject(stuffy.emoji)))
                    cmpt+=1

                returnButton = interactions.Button(style=1,label="Retour",custom_id="return")
                select = interactions.StringSelectMenu(options,custom_id = "seeMoreInfoMenue",placeholder="Voir plus d'informations sur les équipements")

                tempMachin = await inter.send(embeds=infoEnnemi(ennemi),components=[interactions.ActionRow(returnButton),interactions.ActionRow(select)])

                while 1:
                    try:
                        resp2 = await bot.wait_for_component(messages=tempMachin,timeout=60)
                        resp2: ComponentContext = resp2.ctx
                    except:
                        await tempMachin.edit(embeds=infoEnnemi(ennemi),components=[])
                        break
                    try:
                        resp3 = int(resp2.values[0])
                        tablStuff = [ennemi.weapon]+ennemi.skills
                        if type(tablStuff[resp3]) == weapon:
                            await resp2.send(embeds=infoWeapon(tablStuff[resp3],user,ctx))
                        elif type(tablStuff[resp3]) == skill:
                            await resp2.send(embeds=infoSkill(tablStuff[resp3],user,ctx))
                        else:
                            await resp2.send(embeds=infoStuff(tablStuff[resp3],user,ctx))
                    except:
                        await tempMachin.delete()
                        print_exc()
                        break

            elif destination == 8:
                await inter.defer()
                what = whatIsThat(respond)
                if what == 0:
                    await inter.send(embeds=infoWeapon(findWeapon(respond),user,ctx))
                elif what == 1:
                    await inter.send(embeds=infoSkill(findSkill(respond),user,ctx))
                elif what == 2:
                    await inter.send(embeds=infoStuff(findStuff(respond),user,ctx))
