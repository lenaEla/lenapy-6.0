import interactions
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from commands_files.alice_stats_endler import aliceStatsDb
from advObjects.advChips import chip

aspiOp = []
for cmpt in range(len(aspiNames)-1):
	splited = chapter[2][cmpt+1][1].splitlines(False)
	desc = splited[0]
	for em in statEmojis[:ACT_INDIRECT_FULL+1]:
		desc = desc.replace(em,"")
	aspiOp.append(interactions.StringSelectOption(label=aspiNames[cmpt],value=str(cmpt),emoji=getEmojiObject(aspiEmoji[cmpt]),description=desc))

aspirationMenu = interactions.StringSelectMenu(aspiOp, custom_id = "aspiSelectMenu", placeholder="Sélectionnez une aspiration pour avoir plus d'informations dessus")
aspirationMenuD = interactions.StringSelectMenu(interactions.StringSelectOption(label="Tu es pas sensé voir ça",value="0"),custom_id = "aspiSelectMenu2",placeholder="Votre aspiration a bien été prise en compte",disabled=True)

optionIka, optionTako = [],[]
for a in range(0,len(colorChoice)):
	optionIka += [interactions.StringSelectOption(label=colorChoice[a],value=hex(colorId[a]),emoji=getEmojiObject(EmIcon[1][a]))]
	optionTako += [interactions.StringSelectOption(label=colorChoice[a],value=hex(colorId[a]),emoji=getEmojiObject(EmIcon[2][a]))]

aspiDesc = []
for cmpt in range(1,len(chapter[2])):
	aspiDesc.append(reduceEmojiNames(chapter[2][cmpt][1].replace("*", "")))

async def chooseAspirationWindow(bot: interactions.Client, ctx: InteractionContext, user: char, startAspiration: int = None):
	if startAspiration == None: startAspiration = user.aspiration

	def check(m): return m.ctx.author_id == ctx.author_id
	
	msg = None
	while 1:
		if startAspiration != -1:
			aspiMenu = copy.deepcopy(aspirationMenu)
			line0 = aspiDesc[startAspiration].splitlines()[0]
			
			for cmpt in range(len(aspiMenu.options)): aspiMenu.options[cmpt].default = cmpt == startAspiration

			msgCompList = [
				TextDisplayComponent("### __Sélectiond d'une aspiration__"),
				ActionRow(aspiMenu),
				SeparatorComponent(),
				SectionComponent(components=[TextDisplayComponent("**{}**\n{}".format(line0, aspiDesc[startAspiration].replace(line0, "")))], accessory=ThumbnailComponent(media=UnfurledMediaItem(url="https://cdn.discordapp.com/emojis/{}.webp".format(PartialEmoji.from_str(aspiEmoji[startAspiration]).id)))),
				SeparatorComponent(divider=True),
				ActionRow(returnButton, Button(style=[ButtonStyle.PRIMARY, ButtonStyle.SECONDARY][startAspiration == user.aspiration], label="{} {}".format(["Choisir", "Vous êtes déjà"][startAspiration == user.aspiration], aspiNames[startAspiration]), emoji=PartialEmoji.from_str(aspiEmoji[startAspiration]), custom_id="changeAspi", disabled=startAspiration == user.aspiration))
			]
		else:
			msgCompList = [
				TextDisplayComponent("### __Sélectiond d'une aspiration__"),
				ActionRow(aspiMenu),
				SeparatorComponent(),
				TextDisplayComponent("Aucune aspiration n'est actuellement sélectionnée\nSélectionner une aspiration via le menu déroulant ci-dessus pour avoir plus d'information dessus"),
				SeparatorComponent(divider=True),
				ActionRow(returnButton)
			]

		if msg == None: msg = await ctx.send(components=ContainerComponent(*msgCompList, accent_color=user.color))
		else: await msg.edit(components=ContainerComponent(*msgCompList, accent_color=user.color))

		try:
			react = await bot.wait_for_component(msg, timeout=180, check=check)
			react = react.ctx
		except asyncio.TimeoutError:
			await msg.delete()
			msg = None
			return user, False
		else:
			await msg.delete()
			msg = None
			
			if react.custom_id == "changeAspi":
				user.aspiration = startAspiration
				return user, True
			else: return user, False

async def startFunc(bot: interactions.Client, ctx: Union[InteractionContext, Message, SlashContext], lock=[0, 0, 0], user: char = None):
	if type(ctx) != Message and not(ctx.responded): msg = await ctx.send(components=waitingEmbed)
	else: msg = ctx
	
	isNewChar = False
	if user == None:
		if not(os.path.exists("./userProfile/{}.json".format(ctx.author_id))):
			user = char(owner=int(ctx.author_id))
			isNewChar = True
		else: await msg.edit(components=TextDisplayComponent("Vous avez déjà un personnage"))

	aspiMenu, aspiMenuVal, haveChange = copy.deepcopy(aspirationMenu), user.aspiration, False

	def check(m): return int(m.ctx.author_id) == int(ctx.author_id)

	while 1:
		mainEmbComp = [
			TextDisplayComponent("### __Création de personnage__")
		]

		if isNewChar:
			mainEmbComp[0].content += "\n-# Tous les paramètres ci-dessous pourront être modifiés par la suite à l'aide d'objets spéciaux"
			mainEmbComp.append(SeparatorComponent(divider=True, spacing=SeparatorSpacingSize.LARGE))

		moduleList = []
		if not(lock[0]):
			moduleList += [[
				SectionComponent(
					components=[TextDisplayComponent("__Nom du personnage :__ {}".format([user.name, "`Pas de nom`".format(changeName)][user.name == ""]))], 
					accessory=Button(style=[ButtonStyle.SECONDARY, ButtonStyle.PRIMARY][user.name == ""], label="Modifier", custom_id="name", emoji=PartialEmoji.from_str("<:writingPopout:1374491977667707042>")))
			]]

		if not(lock[1]):
			colorOp, haveColor = copy.deepcopy([optionIka, optionTako][user.species == 1]), False
			if user.color in colorId:
				for indx in range(len(colorOp)):
					colorOp[indx].default = hex(user.color) == colorOp[indx].value
					if hex(user.color) == colorOp[indx].value: haveColor = True

			if not(isNewChar): customColorOp = StringSelectOption(label="Couleur Personnalisée", emoji=PartialEmoji.from_str(await getUserIcon(bot, char)), value='custom', default=not(haveColor))
			else: customColorOp = StringSelectOption(label="Couleur Personnalisée", emoji=PartialEmoji.from_str(customColor.emoji), value='custom', default=not(haveColor))

			colorOp.insert(0, customColorOp)
			
			moduleList += [[
				TextDisplayComponent("__Forme d'icone et couleur :__".format(changeAppa)),
				ActionRow(Button(style=[ButtonStyle.SECONDARY, ButtonStyle.PRIMARY][user.species == 0], label="Calamar",emoji=getEmojiObject('<:ikaLBlue:1362015691049533450>'), custom_id="inkling", disabled=user.species == 0), Button(style=[ButtonStyle.SECONDARY, ButtonStyle.PRIMARY][user.species == 1],label="Poulpe",emoji=getEmojiObject('<:takoLBlue:866459095875190804>'),custom_id="octaling", disabled = user.species == 1 or lock[1])),
				ActionRow(StringSelectMenu(colorOp, placeholder="Choissez une couleur de base", disabled=lock[1], custom_id="colorPicker")),
				TextDisplayComponent("Votre personnage doit-il être genré au féminin ?\n-# Ce paramètre n'a aucune inscidence sur les mécaniques de jeux"),
				ActionRow(Button(style=[ButtonStyle.SECONDARY, ButtonStyle.PRIMARY][user.gender != 1], label="Non", custom_id="genderMale", disabled=user.gender != 1), Button(style=[ButtonStyle.SECONDARY, ButtonStyle.PRIMARY][user.gender == 1],label="Oui",custom_id="genderFemale", disabled = user.gender == 1)),
			]]

		if not(lock[2]):
			for cmpt in range(len(aspiMenu.options)):
				aspiMenu.options[cmpt].default = cmpt == aspiMenuVal
				
			moduleList += [[
				TextDisplayComponent("__Aspiration :__"),
				ActionRow(aspiMenu)
			]]

		for indx, val in enumerate(moduleList):
			mainEmbComp += val
			mainEmbComp.append(SeparatorComponent(divider=True, spacing=SeparatorSpacingSize.LARGE))

		errorTabl = [user.name == "", user.name != "" and (len(user.name) < 2 or len(user.name) >= 16), user.aspiration == -1]
		errorMsg = ["Vous devez entrer un nom pour votre personnage", "Le nom de votre personnage doit être compris entre 2 et 16 charactères", "Vous devez choisir une aspiration pour votre personnage"]

		if sum(errorTabl) > 0:
			tmp = ""
			for indx, val in enumerate(errorTabl):
				if val: tmp += "- {}\n".format(errorMsg[indx])

			mainEmbComp.append(TextDisplayComponent(tmp))

		tmpConfirmButton = Button(style=ButtonStyle.SECONDARY, label="Terminer", emoji=getEmojiObject("✅"), custom_id="finish", disabled=True)
		if haveChange and sum(errorTabl) == 0:
			if isNewChar : tmpConfirmButton.style=ButtonStyle.SUCCESS
			else: tmpConfirmButton.style=ButtonStyle.PRIMARY
			tmpConfirmButton.disabled = False

		await msg.edit(components=ContainerComponent(*mainEmbComp, ActionRow(returnButton, tmpConfirmButton), accent_color=user.color))

		try: 
			react = await bot.wait_for_component(messages=msg, check=check, timeout=300)
			react = react.ctx
		except:
			try: await msg.delete()
			except: pass
			return 0
		else:
			match react.custom_id:
				case aspiMenu.custom_id:
					aspiMenuVal = int(react.values[0])
					await lockMsg(msg)

					user, tmpChange = await chooseAspirationWindow(bot=bot, ctx=react, user=user, startAspiration=aspiMenuVal)
					
					if tmpChange: haveChange = True
				case "name":
					await lockMsg(msg, 60)
					nameModal = await react.send_modal(Modal(InputText(label="Nom de votre personnage", style=TextStyles.SHORT, value=[user.name, None][user.name == ""], min_length=3, max_length=15, custom_id="name"), title="Nom du personnage"))
					try:
						modalReact = await bot.wait_for_modal(nameModal, react.author_id, 60)
					except TimeoutError: continue
					else:
						if user.name == modalReact.responses['name']:
							await modalReact.send(components=ContainerComponent(TextDisplayComponent("Le nom de votre persoonage est identique au nom actuel")), ephemeral=True)
						else:
							user.name = modalReact.responses['name']
							await modalReact.send(components=ContainerComponent(TextDisplayComponent("Le nom de votre persoonage a été modifié"), accent_color=user.color), ephemeral=True)
							haveChange = True
				case "inkling":
					user.species = 0
					haveChange = True
				case "octaling":
					user.species = 1
					haveChange = True
				case returnButton.custom_id:
					try: await msg.delete()
					except: pass
					return 0
				case "colorPicker":
					if react.values[0] == "custom":
						await lockMsg(msg, time=60)
						colorModal = await react.send_modal(Modal(InputText(label="Code hexadécimal", style=TextStyles.SHORT, value=hex(user.color).replace("0x", "#"), custom_id="Code hexadécimal"), title="Sélection de couleur"))
						try: modalResp = await bot.wait_for_modal(colorModal, react.author_id, 60)
						except TimeoutError: continue
						else:
							try:
								user.color = int(modalResp.responses["Code hexadécimal"].replace("#", "0x"), 16)
								haveChange = True
								await modalResp.send(components=ContainerComponent(TextDisplayComponent("Votre couleur personnalisée a été appliquée"), accent_color=user.color), ephemeral=True)
							except Exception as e:
								await modalResp.send(components=ContainerComponent(TextDisplayComponent("Une erreur est survenue :\n{}".format(format_exc()))), ephemeral=True)
					else:
						user.color = int(react.values[0], 16)
						haveChange = True
				case "finish":
					user = restats(user)

					if not(os.path.exists("./userProfile/{0}.json".format(user.owner))):
						temp = open("./userProfile/{0}.json".format(user.owner),"w")
						temp.write("0")
						temp.close()

					try:
						saveCharFile(user=user)
						aliceStatsDb.addUser(user)
						desc = "Vous avez terminé la création de votre personnage ! Rassurez-vous, vous pourrez modifier les paramètres renseignés au moyen d'objet spéciaux disponibles dans le shop.\n\nVoici quelques objets pour fêter votre recrutement :"
						for obj in baseWeapon+baseSkills+baseStuffs:
							desc += "\n{0}".format(obj)
							if obj in [baseWeapon[-1],baseSkills[-1],baseStuffs[-1]]: desc += "\n"
						desc += "\nPourquoi ne pas faire un tour vers **/inventory** pour voir ça ?"

						await msg.edit(components=ContainerComponent(TextDisplayComponent(desc), accent_color=user.color))
					except Exception as e:
						await msg.edit(components=ContainerComponent(
							TextDisplayComponent("Une erreur est survenue"), SeparatorComponent(divider=True), TextDisplayComponent(format_exc())))
						print_exc()
						os.remove("./userProfile/{0}.json".format(user.owner))

					break
				case "genderMale":
					user.gender = 2
					haveChange = True
				case "genderFemale":
					user.gender = 1
					haveChange = True
				case _:
					print(react.custom_id)

async def functionVerifUnusedEmoji(bot: interactions.Client, ctx: interactions.SlashContext):
	msg = await ctx.send(embeds=loadingEmbed("Obtention de la liste des émojis..."))

	async def modifMsg(text:str):
		await msg.edit(embeds=loadingEmbed(text))

	listException: List[str] = ["<:timeoB:1104517210728308746>","<:smallClemence:1236329023219437630>","<:oceane:1218268649564143707>","<:glan:1218268667960098879>","<:pirSab1:1059519845177249812>","<:pirGun1:1059519820376330351>","<:pirGun2:1059519760284528640>","<:stimeo:1089164206336647168>","<:itimeo:1103217741172846614>","<:stimeo:1089164206336647168>","<:itimeo:1103217741172846614>","<:dreamSixtine:1100793996483235851>","<:catIli:1006440617146060850>","<:childIli:1089607519380443229>","<:miniIli:1089607564548898876>","<:gaurora:1103332091594281050>","<:penelope:1178446515459588106>", "<:lei:1257691823170785372>","<:silicia:1045109225615003729>", "<:airNacia:1208074166297952278>", "<:fireNacia:1208074195888504902>", "<:waterNacia:1208074216973410405>", "<:earthNacia:1208074102569566209>","<:anais:1311811363009462313>","<:isa:1158136337061400797>","<:batiste:1203788655240679534>","<:kaleb:1183176411452813433>","<:keuleyong:1205465540337078292>"]
	listEmojisId: List[int] = []
	for tmpStr in listException: listEmojisId.append(int(getEmojiObject(tmpStr).id))
	
	listAll: List[Union[classes.skill,classes.weapon,classes.stuff,classes.tmpAllie,classes.octarien]] = skills+stuffs+weapons+tablAllAllies+tablVarAllies+tablUniqueEnnemies+tablBoss+tablRaidBoss+tablBossPlus+chipList+invocTabl
	tablRawestSkill = []
	tablSkills: List[Union[classes.skill,classes.weapon,classes.stuff]] = []
	for tmpObject in listAll:
		match type(tmpObject):
			case classes.skill: tablRawestSkill.append(tmpObject)
			case classes.weapon: tablSkills.append(tmpObject)
			case classes.stuff: tablSkills.append(tmpObject)
			case classes.tmpAllie:
				listEmojisId.append(int(getEmojiObject(tmpObject.icon).id))
				tablSkills.append(tmpObject.weapon)
				tablRawestSkill = tablRawestSkill + tmpObject.skills
				if tmpObject.changeDict != None:
					for tmpDict in tmpObject.changeDict:
						if tmpDict.skills != None: tablRawestSkill = tablRawestSkill + tmpDict.skills
						if tmpDict.icon != None: listEmojisId.append(int(getEmojiObject(tmpDict.icon).id))
			case classes.octarien:
				listEmojisId.append(int(getEmojiObject(tmpObject.icon).id))
				tablRawestSkill = tablRawestSkill + tmpObject.skills
				tablSkills.append(tmpObject.weapon)
			case classes.invoc:
				listEmojisId.append(int(getEmojiObject(tmpObject.icon[0]).id)); listEmojisId.append(int(getEmojiObject(tmpObject.icon[1]).id))
				tablRawestSkill = tablRawestSkill + tmpObject.skills
				tablSkills.append(tmpObject.weapon)
			case _:
				if type(tmpObject) == chip: tablSkills.append(tmpObject)

	tablRawerSkill = []
	for tmpObject in tablRawestSkill:
		if type(tmpObject) == classes.skill:
			if tmpObject.become == None: tablRawerSkill.append(tmpObject)
			else: tablRawerSkill = tablRawerSkill + tmpObject.become + [tmpObject]
		elif tmpObject == None: pass
	
	for tmpObject in tablRawerSkill:
		if type(tmpObject) == classes.skill:
			tablSkills.append(tmpObject)

			while tmpObject != None and tmpObject.effectOnSelf != None: 
				tmpEff = findEffect(tmpObject.effectOnSelf)
				if tmpEff != None and tmpEff.replica != None: 
					tmpObject = findSkill(tmpEff.replica)
					tablSkills.append(tmpObject)
				else: break

	tablSkills = set(tablSkills)
	for tmpObject in tablSkills:
		if type(tmpObject) in [classes.weapon, classes.stuff]:
			listEmojisId.append(int(getEmojiObject(tmpObject.emoji).id))
			if tmpObject.effects != None: 
				tmpEff = findEffect(tmpObject.effects)
				if tmpEff != None:
					for tmpEm in set(tmpEff.emoji[0]+tmpEff.emoji[1]+tmpEff.emoji[2]): 
						if tmpEm != None: listEmojisId.append(int(getEmojiObject(tmpEm).id))
			if type(tmpObject) == classes.weapon and tmpObject.effectOnUse != None: 
				tmpEff = findEffect(tmpObject.effectOnUse)
				if tmpEff != None:
					for tmpEm in set(tmpEff.emoji[0]+tmpEff.emoji[1]+tmpEff.emoji[2]): 
						if tmpEm != None: listEmojisId.append(int(getEmojiObject(tmpEm).id))
		elif type(tmpObject) == chip:
			if tmpObject.emoji != "" : listEmojisId.append(int(getEmojiObject(tmpObject.emoji).id))
		elif type(tmpObject) == classes.skill:
			tmp = getEmojiObject(tmpObject.emoji).id
			if tmp != None: listEmojisId.append(int(tmp))
			else: print(tmpObject.name)
			
			tablEffToSee: List[classes.effect] = []
			if tmpObject.effects != None: tablEffToSee = tablEffToSee+tmpObject.effects
			if tmpObject.effectAroundCaster != None and type(tmpObject.effectAroundCaster[2]) == classes.effect: tablEffToSee.append(tmpObject.effectAroundCaster[2])
			if tmpObject.effectOnSelf != None: tablEffToSee.append(tmpObject.effectOnSelf)
			if tmpObject.jaugeEff != None: tablEffToSee.append(tmpObject.jaugeEff)

			for tmpEff in flatList(tablEffToSee):
				tmpEff2 = findEffect(tmpEff)
				if tmpEff2 != None:
					for tmpEm in set(tmpEff2.emoji[0]+tmpEff2.emoji[1]+tmpEff2.emoji[2]):
						if tmpEm != None:
							tmp = getEmojiObject(tmpEm).id
							if tmp != None: listEmojisId.append(int(tmp))
							else: print(tmpEm)

					if tmpEff2.jaugeValue != None:
						for tmpEm in tmpEff2.jaugeValue.emoji[0]+tmpEff2.jaugeValue.emoji[1]:
							if tmpEm != None: listEmojisId.append(int(getEmojiObject(tmpEm).id))
					while tmpEff2 != None and tmpEff2.callOnTrigger != None:
						for tmpEm in set(tmpEff2.emoji[0]+tmpEff2.emoji[1]+tmpEff2.emoji[2]):
							if tmpEm != None:
								tmp = getEmojiObject(tmpEm).id
								if tmp != None: listEmojisId.append(int(tmp))
						tmpEff2 = findEffect(tmpEff2.callOnTrigger)
				elif tmpEff != None : print(tmpObject.name, type(tmpEff))
  
	listEmojisId = list(set(listEmojisId))
	await modifMsg("Vérification des emojis non utlisés... (0%) {1}\nNombre d'émojis utilisés : {0}".format(len(listEmojisId), "\."*100))
	guildList: List[interactions.Guild] = bot.guilds
	dictUnusedGuilds, listExcludedGuilds, cmpt, cmpt2, lenGuildList = {}, LenaCustomIcons+ShushyCustomIcons+[1171852774217093120,1137363859410264065,1013740566602846248,932941135276560455,894528703185424425,810212019608485918,916120008948600872,1044487484786094120,887846876114739261], 0, 1, len(guildList)
	for temp in guildList:
		if temp.name.startswith("Lenapy") and int(temp.id) not in listExcludedGuilds:
			emojiList = await temp.fetch_all_custom_emojis()
			for tmpEmoji in emojiList:
				if int(tmpEmoji.id) not in listEmojisId:
					if temp in dictUnusedGuilds.keys(): dictUnusedGuilds[temp].append(tmpEmoji)
					else: dictUnusedGuilds[temp] = [tmpEmoji]
		cmpt += 1
		if cmpt > lenGuildList//10*cmpt2:
			cmpt2, purcent, tmp = cmpt2+1, round(cmpt/lenGuildList*100,2), ""
			tmp = "\|"*int(purcent)
			while len(tmp) < 200: tmp+="\."
			await modifMsg("Vérification des emojis non utlisés... ({1}%) {2}\nNombre d'émojis utilisés : {0}".format(len(listEmojisId),purcent,tmp))

	totalLenUnused, listField = 0, []
	for tmpGuild, emojiList in dictUnusedGuilds.items():
		tempValue = ""
		for tmpEmoji in emojiList: totalLenUnused += 1; tempValue += "<:{0}:{1}> {0}\n".format(tmpEmoji.name,tmpEmoji.id)
		try: listField.append(EmbedField(name=tmpGuild.name + " ({0})".format(tmpGuild.id),value=reduceEmojiNames(tempValue),inline=True))
		except: print(tmpGuild.name,tmpGuild.id,"\n",tempValue,"=================")

	tmpFieldList, first = [], True
	for tmpField in listField:
		if len(tmpFieldList) >= 9:
			emb = Embed(title="__Vérification des émojis non utilisés__",color=light_blue,description="Nombre d'émojis utlisés : {0}\nNombre d'émojis non utilisés : {1}".format(len(listEmojisId),totalLenUnused),fields=tmpFieldList)
			if first: await msg.edit(embeds=emb); first = False
			else: await msg.channel.send(embeds=emb)
			tmpFieldList = [tmpField]
		else: tmpFieldList.append(tmpField)
