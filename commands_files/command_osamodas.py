from advance_gestion import *

SMN_TYPE_ALL = -1
listButtons = [
    interactions.Button(style=ButtonStyle.GRAY,label="Retour rapide",emoji=getEmojiObject('⏮'),custom_id="freturn"),
    interactions.Button(style=ButtonStyle.GRAY,label="Retour",emoji=getEmojiObject('◀'),custom_id="return"),
    interactions.Button(style=ButtonStyle.GRAY,label="Suivant",emoji=getEmojiObject('▶'),custom_id="forward"),
    interactions.Button(style=ButtonStyle.GRAY,label="Avance rapide",emoji=getEmojiObject('⏭'),custom_id="fforward")
    ]

listOptions: List[StringSelectOption] = []
cmpt = 0
while 20+(15*cmpt) <= WAKFUMAXLEVEL:
    listOptions.append(StringSelectOption(label="{0}".format(20+(15*cmpt)),value=str(20+(15*cmpt))))
    cmpt += 1

lenListOptions = len(listOptions)

listTypeOptions = [
    StringSelectOption(label="Tous types",value=str(SMN_TYPE_ALL),description="Afficher toutes les invocations",emoji=getEmojiObject('<:catNeutral:956600537174929419>')),
    StringSelectOption(label="Dégâts",value=str(TYPE_DAMAGE),description="Afficher les invocations offensives",emoji=statsEmojis[ACT_DIRECT_FULL]),
    StringSelectOption(label="Soins",value=str(TYPE_HEAL),description="Afficher les invocations soigneuses",emoji=statsEmojis[ACT_HEAL_FULL]),
    StringSelectOption(label="Tank",value=str(TYPE_ARMOR),description="Afficher les invocations défensives",emoji=statsEmojis[ACT_SHIELD_FULL]),
    StringSelectOption(label="Support",value=str(TYPE_BOOST),description="Afficher les invocations de supports",emoji=statsEmojis[ACT_BOOST_FULL])
]

class osaSkill:
    def __init__(self,name:str,element,type,description:str):
        self.name = name
        try:
            self.element:int = {"Feu":ELEMENT_FIRE,"Eau":ELEMENT_WATER,"Air":ELEMENT_AIR,"Terre":ELEMENT_EARTH,"Neutre":ELEMENT_NEUTRAL}[element]
            self.type:int = {"Support":TYPE_BOOST,"Soins":TYPE_HEAL,"Armure":TYPE_ARMOR,"Dmg":TYPE_DAMAGE,}[type]
        except KeyError:
            print(self.name)
        self.description = description

class osaSmnClass:
    def __init__(self,name:str,level:int,type:int,area:str,skills:List[osaSkill],imageUlr:str,encyclopediaUlr:str,emoji='<:LenaWhat:760884455727955978>'):
        try:
            self.name, self.level, self.type, self.area, self.skills, self.imageUrl, self.encyclopediaUrl, self.emoji = name,level, {"Support":TYPE_BOOST,"Soins":TYPE_HEAL,"Armure":TYPE_ARMOR,"Dmg":TYPE_DAMAGE,"Tank":TYPE_ARMOR}[type] ,area,skills,imageUlr,encyclopediaUlr,emoji
        except Exception as e:
            print(name,e)

wappin = osaSmnClass("Wapin",1,"Support","Rii",[
    osaSkill("Wapinade","Terre","Dmg","Inflige des dégâts"),
    osaSkill("Wapinerie","Neutre","Support","Se téléporte sur la case ciblée"),
    osaSkill("Super Wapin","Air","Dmg","Inflige des dégâts et repousse la cible")],
    "https://static.ankama.com/wakfu/portal/game/monster/200/117402504.w133h.png","https://www.wakfu.com/fr/mmorpg/encyclopedie/monstres/5525-wapin","<:ffshrug:895280749366878258>"
)

osaSmnTypesEmojis = {TYPE_DAMAGE:statsEmojis[ACT_DIRECT_FULL],TYPE_HEAL:statsEmojis[ACT_HEAL_FULL],TYPE_ARMOR:statsEmojis[ACT_SHIELD_FULL],TYPE_BOOST:statsEmojis[ACT_BOOST_FULL]}

async def osaSmnCommand(ctx: Union[interactions.ComponentContext, interactions.Message],bot:interactions.Client,level=WAKFUMAXLEVEL,type=SMN_TYPE_ALL):
    osaSmnDictList, osaSmnList = getOsamodasJson(), []
    for osaSmnDict in osaSmnDictList:
        try:
            emojiStr = osaSmnDict["emojiStr"]
        except KeyError:
            emojiStr = '<:LenaWhat:760884455727955978>'

        osaSmnList.append(osaSmnClass(osaSmnDict["name"],osaSmnDict["level"],osaSmnDict["type"],osaSmnDict["area"],[
            osaSkill(osaSmnDict["skills"][0]["name"],osaSmnDict["skills"][0]["element"],osaSmnDict["skills"][0]["type"],osaSmnDict["skills"][0]["description"]),
            osaSkill(osaSmnDict["skills"][1]["name"],osaSmnDict["skills"][1]["element"],osaSmnDict["skills"][1]["type"],osaSmnDict["skills"][1]["description"]),
            osaSkill(osaSmnDict["skills"][2]["name"],osaSmnDict["skills"][2]["element"],osaSmnDict["skills"][2]["type"],osaSmnDict["skills"][2]["description"])],
            osaSmnDict["imageUrl"],osaSmnDict["encyclopediaUrl"],emojiStr
            ))

    osaSmnListCopy: List[osaSmnClass] = osaSmnList[:]
    
    listMul, msg = 0, None
    while 1:
        for smn in osaSmnListCopy[:]:
            if smn.level > level:
                try:
                    osaSmnListCopy.remove(smn)
                except:
                    pass
            if type != SMN_TYPE_ALL:
                if smn.type != type:
                    try:
                        osaSmnListCopy.remove(smn)
                    except:
                        pass
        
        osaSmnListCopy.sort(key=lambda ballerine: ballerine.level, reverse=True)
        lenOsaSmnListCopy = len(osaSmnListCopy)
        if lenOsaSmnListCopy <= 0:
            osaSmnListCopy, lenOsaSmnListCopy = [wappin], 1

        listVal, description = (5*listMul,min((5*(listMul+1)),lenOsaSmnListCopy)), ""
        for osaSmn in osaSmnListCopy[listVal[0]:listVal[1]]:
            description += ["","\n\n"][description != ""] + "{0} **__[{1}]({17})__** ({2}) __(lv. {15})__ :\n*{16}*\n- {3}{4} __{5}__ : {6}\n- {7}{8} __{9}__ : {10}\n- {11}{12} __{13}__ : {14}".format(
                osaSmn.emoji, osaSmn.name, osaSmnTypesEmojis[osaSmn.type], 
                    osaSmnTypesEmojis[osaSmn.skills[0].type], elemEmojis[osaSmn.skills[0].element], osaSmn.skills[0].name, osaSmn.skills[0].description.format(osaSmn.name),
                    osaSmnTypesEmojis[osaSmn.skills[1].type], elemEmojis[osaSmn.skills[1].element], osaSmn.skills[1].name, osaSmn.skills[1].description.format(osaSmn.name),
                    osaSmnTypesEmojis[osaSmn.skills[2].type], elemEmojis[osaSmn.skills[2].element], osaSmn.skills[2].name, osaSmn.skills[2].description.format(osaSmn.name), osaSmn.level, osaSmn.area, osaSmn.encyclopediaUrl
            )
        
        listButtonsSub, listTypeOptionsSub, listOptionsSub = listButtons[:], listTypeOptions[:], listOptions[:]
        listButtonsSub[0].disabled, listButtonsSub[1].disabled, listButtonsSub[2].disabled, listButtonsSub[3].disabled = listMul <= 0, listMul <= 0, 5*(listMul+1) >= lenOsaSmnListCopy, 5*(listMul+1) >= lenOsaSmnListCopy
        listButtonsAct = ActionRow(listButtonsSub[0],listButtonsSub[1],listButtonsSub[2],listButtonsSub[3])
        
        for cmpt in range(1,len(listOptionsSub)):
            listOptionsSub[cmpt].default = int(level) <= int(listOptionsSub[cmpt].value) and int(level) > int(listOptionsSub[cmpt-1].value)
        levelSelectMenu = ActionRow(StringSelectMenu(listOptionsSub,placeholder="Changer le niveau maximum",custom_id="lvlSelect"))
        
        for cmpt in range(len(listTypeOptionsSub)):
            listTypeOptionsSub[cmpt].default = str(type) == listTypeOptionsSub[cmpt].value
        typeSelectMenu = ActionRow(StringSelectMenu(listTypeOptionsSub,placeholder="Changer le type d'invocation affiché",custom_id="typeSelect"))

        description = reduceEmojiNames(description)
        returnEmbed = interactions.Embed(title="__Osamodas Summons__", description=description,color=light_blue,footer=EmbedFooter(text="Page {0}/{1} - {2}".format(listMul+1,((lenOsaSmnListCopy-1)//5)+1,{SMN_TYPE_ALL:"Tous",TYPE_DAMAGE:"Offensifs",TYPE_ARMOR:"Défensifs",TYPE_HEAL:"Soigneur",TYPE_BOOST:"Support"}[type])))
        if ctx.__class__ == interactions.ComponentContext and msg == None:
            msg: Message = await ctx.send(embeds=returnEmbed, components=[listButtonsAct,levelSelectMenu,typeSelectMenu])
        else:
            msg: Message = await ctx.edit(embeds=returnEmbed, components=[listButtonsAct,levelSelectMenu,typeSelectMenu ])

        def check(comp):
            comp:ComponentContext = comp.ctx
            return int(comp.message_id) == int(msg.id)
        try:
            respond = await bot.wait_for_component(check=check,components=[listButtonsAct,levelSelectMenu,typeSelectMenu ],timeout=300)
            respond:ComponentContext = respond.ctx
        except asyncio.TimeoutError:
            await msg.edit(embeds=returnEmbed, components=[])
            return 1

        if respond.component_type == ComponentType.BUTTON:
            if respond.custom_id == listButtonsSub[0].custom_id:
                listMul = 0
            elif respond.custom_id == listButtonsSub[1].custom_id:
                listMul = max(listMul-1,0)
            elif respond.custom_id == listButtonsSub[2].custom_id:
                listMul = min(listMul+1,(lenOsaSmnListCopy-1)//5)
            else:
                listMul = (lenOsaSmnListCopy-1)//5
        else:
            if respond.custom_id == levelSelectMenu.components[0].custom_id:
                level, listMul = int(respond.values[0]), 0
            elif respond.custom_id == typeSelectMenu.components[0].custom_id:
                type, listMul = int(respond.values[0]), 0
            osaSmnListCopy: List[osaSmnClass] = osaSmnList[:]