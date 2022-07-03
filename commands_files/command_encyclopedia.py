import discord,emoji,copy
from discord_slash.utils.manage_components import create_actionrow, create_select_option, create_select, wait_for_component
from adv import *
from constantes import *
from gestion import getEmojiObject, whatIsThat
from advance_gestion import infoStuff,infoWeapon,infoSkill,getUserIcon,infoAllie,infoEnnemi
from commands_files.sussess_endler import *
from commands_files.command_inventory import getSortSkillValue

async def encylopedia(bot : discord.Client, ctx : discord_slash.SlashContext, destination : int, user : char):
    """The main function for the encyclopedia command"""

    def check(m):
        return m.author_id == ctx.author.id and m.origin_message.id == msg.id

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
            destOptions+=[create_select_option(fullValue[a],opValues[a],getEmojiObject(valueIcon[a]),default=opValues[a]==opValues[destination])]

        destSelect = create_actionrow(create_select(destOptions))

        # The options for the filter menu. Change with the selected destination
        options = [
            create_select_option("Ordre Alphabétique ↓","0",'🇦',default=0==tri),
            create_select_option("Ordre Alphabétique ↑","1",'🇿',default=1==tri)
        ]

        if destination in [0,1,2,3,4]:
            options += [
            create_select_option("Possédé","2",'🔓',default=2==tri),
            create_select_option("Non possédé","3",'🔒',default=3==tri)
            ]
        
        if destination in [0,1,2,3]:
            options+=[
                create_select_option("Force","4",'💪',default=4==tri),
                create_select_option("Endurance","5",'🏃',default=5==tri),
                create_select_option("Charisme",'6','💃',default=6==tri),
                create_select_option("Agilité","7",'🤸',default=7==tri),
                create_select_option("Précision","8",'🏹',default=8==tri),
                create_select_option("Intelligence","9",'🎓',default=9==tri),
                create_select_option("Magie","10",'🧙',default=10==tri),
                create_select_option("Résistance","11",'🛡️',default=11==tri),
                create_select_option("Pénétration","12",'🗡️',default=12==tri),
                create_select_option("Critique","13",'🎲',default=13==tri)]

        elif destination == 4:
            options += [
                create_select_option("Dégâts","14",getEmojiObject('<:meteor:904164411990749194>'),default=tri==14),
                create_select_option("Dégâts indirects","15",getEmojiObject('<:tentamissile:884757344397951026>'),default=tri==15),
                create_select_option("Soins","16",getEmojiObject('<:AdL:873548073769533470>'),default=tri==16),
                create_select_option("Armure","17",getEmojiObject('<:orbeDef:873725544427053076>'),default=tri==17),
                create_select_option("Boost",'18',getEmojiObject('<:bpotion:867165268911849522>'),default=tri==18),
                create_select_option("Malus","19",getEmojiObject('<:nostalgia:867162802783649802>'),default=tri==19),
                create_select_option("Invocation","20",getEmojiObject('<:sprink1:887747751339757599>'),default=tri==20),
                create_select_option("Passif","21",getEmojiObject('<:IdoOH:909278546172719184>'),default=tri==21)
            ]

        elif destination in [5,6,7]:
            options += [
                create_select_option("DPT - Mêlée","21",getEmojiObject('<:sworddance:894544710952173609>'),default=tri==21),
                create_select_option("DPT - Distance","22",getEmojiObject('<:preciseShot:916561817969500191>'),default=tri==22),
                create_select_option("Supports","23",getEmojiObject('<:alice:893463608716062760>'),default=tri==23),
                create_select_option("Soigneur / Armuriers","24",getEmojiObject('<:absorb:971788658782928918>'),default=tri==24),
            ]
        elif destination in [9]:
            options += [
            create_select_option("Terminés","14",'🔓',default=13==tri),
            create_select_option("Non terminés","15",'🔒',default=14==tri)
            ]

        sortOptions = create_select(options)
    
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
                            if not(ski.type == see or (ski.effect != [None] and findEffect(ski.effect[0]).type == see) or (ski.effectAroundCaster != None and ski.effectAroundCaster[0] == see) or (ski.effectOnSelf != None and findEffect(ski.effectOnSelf).type == see)):
                                tablToSee.remove(ski)
                    else:
                        for ski in tablToSee[:]:
                            if not(ski.type in see or (ski.effect != [None] and findEffect(ski.effect[0]).type in see) or (ski.effectAroundCaster != None and ski.effectAroundCaster[0] in see) or (ski.effectOnSelf != None and findEffect(ski.effectOnSelf).type in see)):
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
                pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
                user = loadCharFile(pathUserProfile)
                tablToSee = achivement.getSuccess(user)
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
                    if tri == 21 and ent.aspiration not in [BERSERK,POIDS_PLUME,TETE_BRULE,ENCHANTEUR]:
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
        if destination in [0,1,2,3,4,8]:                          # Stuffs, Weapons and Skills
            desc = f"{userIcon} : Vous possédez déjà cet objet\n<:coinsn_t:885921771071627304> : Cet ebjet ne peut pas être obtenu dans le Magasin ou en butin"
        elif destination == 5:                                    # Alliés Temps
            desc = "Les alliés temporaires rejoignent automatiquement un combat pour remplir les équipes en dessous de 4 membres"
        elif destination == 6:                                    # Ennemis
            desc = "Les ennemis sont là pour vous opposer une petite résistance tout de même"
        elif destination == 7:                                    # Boss's
            desc = "Chaque combat a une chance sur trois de voir un Boss parmis les ennemis"
        elif destination == 9:                                    # Sussess
            desc = "Liste des succès :"

        firstOptions = []
        if page != 0:
            firstOptions+=[create_select_option("Page précédente","return",emoji.backward_arrow)]

        if lenTabl != 0: # Génération des pages
            if destination < 5 or destination == 8:
                mess=""
                if page != maxPage:
                    maxi = (page+1)*10
                else:
                    maxi = lenTabl
                for a in tablToSee[(page)*10:maxi]:
                    # Nom, posession
                    mess += f"\n{a.emoji} **__{a.name}__** "
                    temp=""
                    if user.have(a):
                        temp += userIcon
                    if temp!="":
                        temp = "("+temp+")"

                    lock = ""
                    if a not in listAllBuyableShop:
                        lock = "(<:coinsn_t:885921771071627304>)"
                    mess += temp+lock+"\n"

                    # Première info utile
                    if destination in [0,1,2,8] and type(a) == stuff:
                        affinity = ""
                        if type(a) == stuff and a.affinity != None:
                            affinity = elemEmojis[a.affinity]
                        elif type(a) == skill and a.condition != []:
                            if a.condition[:2] == [0, 2]:
                                affinity = elemEmojis[a.condition[2]]
                            elif a.condition[:2] == [0, 1]:
                                affinity = aspiEmoji[a.condition[2]]
                        if affinity != "":
                            affinity = " - "+affinity
                        mess +="*"+a.orientation+affinity+"*\n"
                    elif destination in [3,4,8] and type(a) != stuff:
                        ballerine = tablTypeStr[a.type]+" "
                        if a.use != None and a.use != HARMONIE:
                            sandale = nameStats[a.use]
                        elif a.use == None:
                            sandale = "Fixe"
                        elif a.use == HARMONIE:
                            sandale = "Harmonie"

                        if destination == 3:
                            babie = ["Mêlée","Distance","Longue Distance"][a.range]+" - "
                        else:
                            babie=''

                        affinity = ""
                        if type(a) == stuff and a.affinity != None:
                            affinity = elemEmojis[a.affinity]
                        elif type(a) == skill and a.condition != []:
                            if a.condition[:2] == [0, 2]:
                                affinity = elemEmojis[a.condition[2]]
                            elif a.condition[:2] == [0, 1]:
                                affinity = aspiEmoji[a.condition[2]]
                            elif a.condition[:2] == [0, 3]:
                                affinity = secElemEmojis[a.condition[2]]
                        if affinity != "":
                            affinity = " - "+affinity
                        mess += f"*{babie}{ballerine} - {sandale}{affinity}*\n"

                    # Statistiques
                    temp = ""
                    if destination in [0,1,2,3,8]:
                        if type(a) != skill:
                            stats,abre = [a.strength,a.endurance,a.charisma,a.agility,a.precision,a.intelligence,a.magie,a.resistance,a.percing,a.critical,a.negativeHeal*-1,a.negativeBoost*-1,a.negativeShield*-1,a.negativeDirect*-1,a.negativeIndirect*-1],["For","End","Cha","Agi","Pre","Int","Mag","Rés","Pén","Cri","Soi","Boo","Arm","Dir","Ind"]
                            for b in range(0,len(stats)):
                                if stats[b] != 0:
                                    form = ""
                                    if b == tri-4:
                                        form = "**"
                                    if tri in [4,10] and b in [13,14]:
                                        if (b == 13 and (stats[13] > stats[14] or stats[13] == stats[14])) or (b == 14 and (stats[14] > stats[13] or stats[13] == stats[14])):
                                            form = "**"
                                    elif tri == 6 and b in [10,11]:
                                        if (b == 10 and (stats[10] > stats[11] or stats[10] == stats[11])) or (b == 11 and (stats[11] > stats[10] or stats[11] == stats[10])):
                                            form = "**"
                                    elif tri == 9 and b in [12,11]:
                                        if (b == 12 and (stats[12] > stats[11] or stats[12] == stats[11])) or (b == 11 and (stats[11] > stats[12] or stats[11] == stats[12])):
                                            form = "**"

                                    temp+=f"{form}{abre[b]}: {stats[b]}{form}, "
                            if a.affinity != None:
                                nim = elemNames[a.affinity]
                                if len(nim) > 3:
                                    nim = nim[0:3]+"."
                                temp += " Elem. : "+nim

                            if a.effect != None:
                                temp += " *{0}*".format(findEffect(a.effect).name)

                    # Création de l'option
                    mess += temp+"\n"
                    firstOptions += [create_select_option(unhyperlink(a.name),a.id,getEmojiObject(a.emoji))]
            elif destination != 9:
                mess = ""
                if page != maxPage:
                    maxi = (page+1)*10
                else:
                    maxi = lenTabl
                for a in tablToSee[(page)*10:maxi]:
                    if type(a) == octarien:
                        mess += f"{a.icon} __{a.name}__\n{aspiEmoji[a.aspiration]} {inspi[a.aspiration][0:3]}. | {a.weapon.emoji} |"
                        firstOptions+=[create_select_option(unhyperlink(a.name),a.name,getEmojiObject(a.icon))]
                    else:
                        variantVar = ""
                        if a.variant:
                            variantVar = " (🔀)"
                        mess += f"{a.icon} __{a.name}__{variantVar}\n{aspiEmoji[a.aspiration]} {inspi[a.aspiration][0:3]} | {a.weapon.emoji} |"
                        firstOptions+=[create_select_option(unhyperlink(a.name),a.name,getEmojiObject(a.icon))]

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

            if len(mess) > 4056: # Mess abrégé
                mess = unemoji(mess)

        else:
            mess = "Il n'y a rien à afficher dans cette catégorie"

        if page < maxPage:
            firstOptions+=[create_select_option("Page suivante","next",emoji.forward_arrow)]

        if len(firstOptions) > 0:
            firstSelect = create_select(options=firstOptions,placeholder="Changez de page ou voir la page de l'équipement")
        else:
            firstSelect = create_select(options=[create_select_option("None","None")],placeholder="Cette catégorie n'a rien à afficher",disabled=True)

        embed = discord.Embed(title="Encyclopédie",description=desc+"\n\n__Page **{0}** / {1} :__\n\n".format(page+1,maxPage+1)+mess,color=user.color)

        if msg == None:     # Send the message for the first loop
            try:
                msg = await ctx.send(embed=embed,components=[destSelect,create_actionrow(sortOptions),create_actionrow(firstSelect)])
            except:
                msg = await ctx.channel.send(embed=embed,components=[destSelect,create_actionrow(sortOptions),create_actionrow(firstSelect)])

        else:
            await msg.edit(embed=embed,components=[destSelect,create_actionrow(sortOptions),create_actionrow(firstSelect)])

        try:
            respond = await wait_for_component(bot,msg,check=check,timeout=180)
        except:
            await msg.edit(embed=embed,components=[])
            break
    
        if respond.values[0].isdigit():
            respond = int(respond.values[0])

            if respond in [0,1]:
                needRemake = True
            else:
                if destination in [0,1,2,3]:
                    tablToSee.sort(key=lambda ballerine: ballerine.name)
                    if respond in [2,3]:
                        tablToSee.sort(key=lambda ballerine:user.have(ballerine), reverse=not(respond-2))
                    elif respond == 4:
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
                    elif respond in [14,15]:
                        tablToSee.sort(key=lambda ballerine:ballerine.haveSucced, reverse=not(respond-14))
                else:
                    needRemake = True
            tri=respond

        else:
            inter = respond
            respond = respond.values[0]

            if respond == "return":
                page -= 1
            elif respond == "next":
                page += 1

            elif respond in opValues:
                for a in range(0,len(opValues)):
                    if opValues[a] == respond:
                        destination = a
                        needRemake = True
                        break
            elif destination in [0,1,2]:
                await inter.send(embed=infoStuff(findStuff(respond),user,ctx))
            elif destination == 3:
                await inter.send(embed=infoWeapon(findWeapon(respond),user,ctx))
            elif destination == 4:
                await inter.send(embed=infoSkill(findSkill(respond),user,ctx))
            elif destination == 5:
                lvl, tempMachin, addLvl = 50, None, 0
                procurData = None
                for procurName, procurStuff in procurTempStuff.items():
                    if respond == procurName:
                        addLvl = procurStuff[0]
                        procurData = procurStuff
                        break
                while 1:
                    lvlAdded = lvl + addLvl
                    ally = copy.deepcopy(findAllie(respond))
                    ally.changeLevel(lvl,changeDict=False)
                    
                    if procurData == None:
                        ally.stuff = [getAutoStuff(ally.stuff[0],ally),getAutoStuff(ally.stuff[1],ally),getAutoStuff(ally.stuff[2],ally)]
                    else:
                        ally.stuff = [
                            stuff(procurData[1][0],procurData[1][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*lvlAdded),int(procurData[4][1][0]*procurData[4][1][1]*lvlAdded),int(procurData[4][2][0]*procurData[4][2][1]*lvlAdded),int(procurData[4][3][0]*procurData[4][3][1]*lvlAdded),int(procurData[4][4][0]*procurData[4][4][1]*lvlAdded),int(procurData[4][5][0]*procurData[4][5][1]*lvlAdded),int(procurData[4][6][0]*procurData[4][6][1]*lvlAdded),int(procurData[4][7][0]*procurData[4][7][1]*lvlAdded),int(procurData[4][8][0]*procurData[4][8][1]*lvlAdded),int(procurData[4][9][0]*procurData[4][9][1]*lvlAdded),emoji=procurData[1][2]),
                            stuff(procurData[2][0],procurData[2][1],1,0,int(procurData[4][0][0]*procurData[4][0][1]*lvlAdded),int(procurData[4][1][0]*procurData[4][1][1]*lvlAdded),int(procurData[4][2][0]*procurData[4][2][1]*lvlAdded),int(procurData[4][3][0]*procurData[4][3][1]*lvlAdded),int(procurData[4][4][0]*procurData[4][4][1]*lvlAdded),int(procurData[4][5][0]*procurData[4][5][1]*lvlAdded),int(procurData[4][6][0]*procurData[4][6][1]*lvlAdded),int(procurData[4][7][0]*procurData[4][7][1]*lvlAdded),int(procurData[4][8][0]*procurData[4][8][1]*lvlAdded),int(procurData[4][9][0]*procurData[4][9][1]*lvlAdded),emoji=procurData[2][2]),
                            stuff(procurData[3][0],procurData[3][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*lvlAdded),int(procurData[4][1][0]*procurData[4][1][1]*lvlAdded),int(procurData[4][2][0]*procurData[4][2][1]*lvlAdded),int(procurData[4][3][0]*procurData[4][3][1]*lvlAdded),int(procurData[4][4][0]*procurData[4][4][1]*lvlAdded),int(procurData[4][5][0]*procurData[4][5][1]*lvlAdded),int(procurData[4][6][0]*procurData[4][6][1]*lvlAdded),int(procurData[4][7][0]*procurData[4][7][1]*lvlAdded),int(procurData[4][8][0]*procurData[4][8][1]*lvlAdded),int(procurData[4][9][0]*procurData[4][9][1]*lvlAdded),emoji=procurData[3][2])
                        ]
                    options, cmpt = [], 0
                    for stuffy in [ally.weapon]+ally.skills+ally.stuff:
                        if type(stuffy) in [skill,weapon,stuff]:
                            options.append(create_select_option(stuffy.name,str(cmpt),getEmojiObject(stuffy.emoji)))
                        cmpt+=1
                    returnButton = create_button(1,"Retour",custom_id="return")
                    select = create_select(options,placeholder="Voir plus d'informations sur les équipements")
                    lvlSelectOption = []
                    for a in range(1,12):
                        lvlSelectOption.append(create_select_option("Niveau {0}".format(5*a),"lvl_{0}".format(5*a+addLvl),default=lvl==5*a))
                    lvlSelect = create_actionrow(create_select(options=lvlSelectOption,placeholder="Choisir un niveau"))
                    embed = infoAllie(ally)
                    if tempMachin == None:
                        tempMachin = await inter.send(embed=embed,components=[create_actionrow(returnButton),create_actionrow(select),lvlSelect])
                    else:
                        await tempMachin.edit(embed=embed,components=[create_actionrow(returnButton),create_actionrow(select),lvlSelect])
                    try:
                        resp2 = await wait_for_component(bot,messages=tempMachin,timeout=60)
                    except:
                        await tempMachin.edit(embed=embed,components=[])
                        break
                    try:
                        if not(resp2.values[0].startswith("lvl_")):
                            resp3 = int(resp2.values[0])
                            tablStuff = [ally.weapon]+ally.skills+ally.stuff
                            whatty = whatIsThat(tablStuff[resp3])
                            if whatty == 0:
                                await resp2.send(embed=infoWeapon(tablStuff[resp3],user,ctx),delete_after=60)
                            elif whatty == 1:
                                await resp2.send(embed=infoSkill(tablStuff[resp3],user,ctx),delete_after=60)
                            elif whatty == 2:
                                await resp2.send(embed=infoStuff(tablStuff[resp3],user,ctx),delete_after=60)
                        else:
                            lvl = int(resp2.values[0][4:])
                    except:
                        print_exc()
                        await tempMachin.delete()
                        break

            elif destination in [6,7]:
                options = []
                ennemi = findEnnemi(respond)
                cmpt = 0
                for stuffy in [ennemi.weapon]+ennemi.skills:
                    if type(stuffy) in [skill,weapon]:
                        options.append(create_select_option(stuffy.name,str(cmpt),getEmojiObject(stuffy.emoji)))
                    cmpt+=1

                returnButton = create_button(1,"Retour",custom_id="return")
                select = create_select(options,placeholder="Voir plus d'informations sur les équipements")

                tempMachin = await inter.send(embed=infoEnnemi(ennemi),components=[create_actionrow(returnButton),create_actionrow(select)])

                while 1:
                    try:
                        resp2 = await wait_for_component(bot,messages=tempMachin,timeout=60)
                    except:
                        await tempMachin.edit(embed=infoEnnemi(ennemi),components=[])
                        break
                    try:
                        resp3 = int(resp2.values[0])
                        tablStuff = [ennemi.weapon]+ennemi.skills
                        if type(tablStuff[resp3]) == weapon:
                            await resp2.send(embed=infoWeapon(tablStuff[resp3],user,ctx),delete_after=60)
                        elif type(tablStuff[resp3]) == skill:
                            await resp2.send(embed=infoSkill(tablStuff[resp3],user,ctx),delete_after=60)
                        else:
                            await resp2.send(embed=infoStuff(tablStuff[resp3],user,ctx),delete_after=60)
                    except:
                        print_exc()
                        await tempMachin.delete()
                        break

            elif destination == 8:
                what = whatIsThat(respond)
                if what == 0:
                    await inter.send(embed=infoWeapon(findWeapon(respond),user,ctx))
                elif what == 1:
                    await inter.send(embed=infoSkill(findSkill(respond),user,ctx))
                elif what == 2:
                    await inter.send(embed=infoStuff(findStuff(respond),user,ctx))
