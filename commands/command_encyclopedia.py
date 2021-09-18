import discord,emoji,copy
from discord_slash.utils.manage_components import create_actionrow, create_select_option, create_select, wait_for_component
from adv import *
from constantes import *
from gestion import getEmojiObject, whatIsThat
from advance_gestion import infoStuff,infoWeapon,infoSkill,getUserIcon,infoAllie,infoEffect,infoEnnemi
from commands.sussess_endler import *


def changeDefault(select,value : int):
    value = str(value)
    temp = copy.deepcopy(select)
    for a in temp["options"]:
        if a["value"] == value:
            a["default"] = True
        elif a["default"] == True:
            a["default"] = False

    return temp

async def encylopedia(bot,ctx,destination,user):
    def check(m):
        return m.author_id == ctx.author.id and m.origin_message.id == msg.id
    
    msg = None
    stuffed = [[],[],[]]
    for a in [0,1,2]:
        for b in stuffs:
            if b.type == a:
                stuffed[a].append(b.emoji)


    opValues,value,fullValue=["accessoires","vetements","chaussures","armes","competences","tempAlies","ennemies","boss","locked","achivements"],0,["Accessoires","Vêtements","Chaussures","Armes","Compétences","Alliés","Ennemis","Boss","Objets non-possédés","Succès"]
    valueIcon = [stuffed[0][random.randint(0,len(stuffed[0])-1)],stuffed[1][random.randint(0,len(stuffed[1])-1)],stuffed[2][random.randint(0,len(stuffed[2])-1)],weapons[random.randint(0,len(weapons)-1)].emoji,skills[random.randint(0,len(skills)-1)].emoji,tablAllAllies[random.randint(0,len(tablAllAllies)-1)].icon,tablAllOcta[random.randint(0,len(tablAllOcta)-1)].icon,tablBoss[random.randint(0,len(tablBoss)-1)].icon,'<:splatted2:727586393173524570>','<:ls1:868838101752098837>']
    tri = 0
    for a in range(0,len(opValues)):
        if destination == opValues[a]:
            value=a
            break

    needRemake = True
    reverse=False
    userIcon = await getUserIcon(bot,user)
    while 1:
        destOptions = []
        for a in range(0,len(opValues)):
            destOptions+=[create_select_option(fullValue[a],opValues[a],getEmojiObject(valueIcon[a]),default=opValues[a]==opValues[value])]

        destSelect = create_actionrow(create_select(destOptions))        

        options = [
            create_select_option("Ordre Alphabétique ↓","0",'🇦',default=0==tri or(tri > 3 and value > 3 and value != 9)),
            create_select_option("Ordre Alphabétique ↑","1",'🇿',default=1==tri)
        ]

        if value in [0,1,2,3,4]:
            options += [
            create_select_option("Possédé","2",'🔓',default=2==tri),
            create_select_option("Non possédé","3",'🔒',default=3==tri)
            ]
        
        if value in [0,1,2,3]:
            options+=[
                create_select_option("Force","4",'💪',default=4==tri),
                create_select_option("Endurance","5",'🏃',default=5==tri),
                create_select_option("Charisme",'6','💃',default=6==tri),
                create_select_option("Agilité","7",'🤸',default=7==tri),
                create_select_option("Précision","8",'🏹',default=8==tri),
                create_select_option("Intelligence","9",'🎓',default=9==tri),
                create_select_option("Résistance","10",'🛡️',default=10==tri),
                create_select_option("Pénétration","11",'🗡️',default=11==tri),
                create_select_option("Critique","12",'🎲',default=12==tri)]

        if value in [9]:
            options += [
            create_select_option("Terminés","13",'🔓',default=13==tri),
            create_select_option("Non terminés","14",'🔒',default=14==tri)
            ]

        sortOptions = create_select(options)
    
        if needRemake:
            tablToSee = []
            if value in [0,1,2]:
                for a in stuffs:
                    if a.type == value:
                        tablToSee.append(a)
            elif value == 3:
                tablToSee = weapons[:]
            elif value == 4:
                tablToSee = skills[:]
            elif value == 5:
                for a in tablAllAllies:
                    if a not in tablToSee:
                        tablToSee.append(a)
            elif value == 6:
                for a in tablAllOcta:
                    trouv=False
                    for b in tablToSee:
                        if a.name == b.name:
                            trouv=True
                            break
                    if not(trouv):
                        tablToSee.append(a)
            elif value == 7:
                for a in tablBoss:
                    trouv=False
                    for b in tablToSee:
                        if a.name == b.name:
                            trouv=True
                            break
                    if not(trouv):
                        tablToSee.append(a)

            elif value == 8:
                tablToSee = weapons[:]+stuffs[:]+skills[:]
                for a in tablToSee[:]:
                    if user.have(a):
                        tablToSee.remove(a)

            elif value==9:
                pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"
                user = loadCharFile(pathUserProfile)
                tablToSee = achivement.getSuccess(user)
                tablToSee = tablToSee.tablAllSuccess()

            tablToSee.sort(key=lambda stuff:stuff.name,reverse=reverse)
            lenTabl = len(tablToSee)
            maxPage=(lenTabl-1)//5
            page=0
            needRemake = False

        if value in [0,1,2,3,4,8]:
            desc = f"{userIcon} : Vous possédez déjà cet objet\n<:coinsn_t:885921771071627304> : Cet ebjet ne peut pas être obtenu dans le Magasin ou en butin"
        elif value == 5:
            desc = "Les alliés temporaires rejoignent automatiquement un combat pour remplir les équipes en dessous de 4 membres"
        elif value == 6:
            desc = "Les ennemis sont là pour vous opposer une petite résistance tout de même"
        elif value == 7:
            desc = "Chaque combat a une chance sur trois de voir un Boss parmis les ennemis"
        elif value == 9:
            desc = "Liste des succès :"

        embed = discord.Embed(title="Encyclopédie",description=desc,color=user.color)
        firstOptions = []
        if page != 0:
            firstOptions+=[create_select_option("Page précédente","return",emoji.backward_arrow)]
        
        if value < 5 or value == 8:
            for z in [0,1]:
                if page+z <= maxPage:
                    mess=""
                    if page+z != maxPage:
                        maxi = (page+1+z)*5
                    else:
                        maxi = lenTabl
                    for a in tablToSee[(page+z)*5:maxi]:
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
                        if value in [0,1,2,8] and type(a) == stuff:
                            mess +="*"+a.orientation+"*\n"
                        elif value in [3,4,8] and type(a) != stuff:
                            ballerine = tablTypeStr[a.type]+" "
                            if a.use != None and a.use != HARMONIE:
                                sandale = nameStats[a.use]
                            elif a.use == None:
                                sandale = "Fixe"
                            elif a.use == HARMONIE:
                                sandale = "Harmonie"

                            if value == 3:
                                babie = ["Mêlée","Distance","Longue Distance"][a.range]+" - "
                            else:
                                babie=''
                            mess += f"*{babie}{ballerine} - {sandale}*\n"

                        # Statistiques
                        temp = ""
                        if value in [0,1,2,3,8]:
                            if type(a) != skill:
                                stats,abre = [a.strength,a.endurance,a.charisma,a.agility,a.precision,a.intelligence,a.resistance,a.percing,a.critical],["For","End","Cha","Agi","Pre","Int","Rés","Pén","Cri"]
                                for b in range(0,len(stats)):
                                    if stats[b] != 0:
                                        form = ""
                                        if b == tri-4:
                                            form = "**"
                                        temp+=f"{form}{abre[b]}: {stats[b]}{form}, "
                                if a.affinity != None:
                                    nim = elemNames[a.affinity]
                                    if len(nim) > 3:
                                        nim = nim[0:3]+"."
                                    temp += " Elem. : "+nim
                    
                        # Création de l'option
                        mess += temp+"\n"
                        firstOptions += [create_select_option(a.name,a.id,getEmojiObject(a.emoji))]
                    embed = embed.add_field(name="<:empty:866459463568850954>\n__"+fullValue[value] + f" - Page {page+z+1} sur {maxPage+1}__",value=mess,inline=False)
        
        elif value != 9:
            for z in [0,1]:
                if page+z <= maxPage:
                    mess = ""
                    if page+z != maxPage:
                        maxi = (page+1+z)*5
                    else:
                        maxi = lenTabl
                    for a in tablToSee[(page+z)*5:maxi]:
                        if type(a) == octarien:
                            mess += f"{a.icon} __{a.name}__\n{inspi[a.aspiration]} | {a.weapon.emoji} |"
                            firstOptions+=[create_select_option(a.name,a.name,getEmojiObject(a.icon))]
                        else:
                            mess += f"{emoji.icon[a.species][getColorId(a)]} __{a.name}__\n{inspi[a.aspiration]} | {a.weapon.emoji} |"
                            firstOptions+=[create_select_option(a.name,a.name,getEmojiObject(emoji.icon[a.species][getColorId(a)]))]

                        for b in a.skills:
                            if type(b) == skill:
                                mess += f" {b.emoji}"

                        mess+="\n\n"
                    embed = embed.add_field(name="<:empty:866459463568850954>\n__"+fullValue[value] + f" - Page {page+z+1} sur {maxPage+1}__",value=mess,inline=False)
        
        else:
            for z in [0,1]:
                if page+z <= maxPage:
                    mess = ""
                    if page+z != maxPage:
                        maxi = (page+1+z)*5
                    else:
                        maxi = lenTabl
                    for a in tablToSee[(page+z)*5:maxi]:
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
                    embed = embed.add_field(name="<:empty:866459463568850954>\n__"+fullValue[value] + f" - Page {page+z+1} sur {maxPage+1}__",value=mess,inline=False)

        if page+1 < maxPage:
            firstOptions+=[create_select_option("Page suivante","next",emoji.forward_arrow)]
        
        firstSelect = create_select(options=firstOptions,placeholder="Changez de page ou voir la page de l'équipement")

        if msg == None:
            msg = await ctx.send(embed=embed,components=[destSelect,create_actionrow(sortOptions),create_actionrow(firstSelect)])

        else:
            await msg.edit(embed=embed,components=[destSelect,create_actionrow(sortOptions),create_actionrow(firstSelect)])


        try:
            respond = await wait_for_component(bot,msg,check=check,timeout=180)
        except:
            await msg.edit(embed=embed,components=[])
            break
    
        if respond.values[0].isdigit():
            respond = int(respond.values[0])
            sortOptions = changeDefault(sortOptions,respond)

            if respond in [0,1]:
                needRemake,reverse=True,respond
            else:
                tablToSee.sort(key=lambda ballerine: ballerine.name)
                if respond in [2,3]:
                    tablToSee.sort(key=lambda ballerine:user.have(ballerine), reverse=not(respond-2))
                elif respond == 4:
                    tablToSee.sort(key=lambda ballerine:ballerine.strength, reverse=True)
                elif respond == 5:
                    tablToSee.sort(key=lambda ballerine:ballerine.endurance, reverse=True)
                elif respond == 6:
                    tablToSee.sort(key=lambda ballerine:ballerine.charisma, reverse=True)
                elif respond == 7:
                    tablToSee.sort(key=lambda ballerine:ballerine.agility, reverse=True)
                elif respond == 8:
                    tablToSee.sort(key=lambda ballerine:ballerine.precision, reverse=True)
                elif respond == 9:
                    tablToSee.sort(key=lambda ballerine:ballerine.intelligence, reverse=True)
                elif respond == 10:
                    tablToSee.sort(key=lambda ballerine:ballerine.resistance, reverse=True)
                elif respond == 11:
                    tablToSee.sort(key=lambda ballerine:ballerine.percing, reverse=True)
                elif respond == 12:
                    tablToSee.sort(key=lambda ballerine:ballerine.critical, reverse=True)
                elif respond in [13,14]:
                    tablToSee.sort(key=lambda ballerine:ballerine.haveSucced, reverse=not(respond-13))
            tri=respond

        else:
            inter = respond
            respond = respond.values[0]

            if respond == "return":
                page -= 2
            elif respond == "next":
                page += 2

            elif respond in opValues:
                for a in range(0,len(opValues)):
                    if opValues[a] == respond:
                        value = a
                        needRemake = True
                        break
            elif value in [0,1,2]:
                await inter.send(embed=infoStuff(findStuff(respond),user,ctx))
            elif value == 3:
                await inter.send(embed=infoWeapon(findWeapon(respond),user,ctx))
            elif value == 4:
                await inter.send(embed=infoSkill(findSkill(respond),user,ctx))
            elif value == 5:
                await inter.send(embed=infoAllie(findAllie(respond)))
            elif value in [6,7]:
                await inter.send(embed=infoEnnemi(findEnnemi(respond)))
            elif value == 8:
                what = whatIsThat(respond)
                if what == 0:
                    await inter.send(embed=infoWeapon(findStuff(respond),user,ctx))
                elif what == 1:
                    await inter.send(embed=infoSkill(findSkill(respond),user,ctx))
                elif what == 2:
                    await inter.send(embed=infoStuff(findStuff(respond),user,ctx))