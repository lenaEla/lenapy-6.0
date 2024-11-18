import os
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from commands_files.command_fight import teamWinDB

buttonReturn = interactions.Button(style=2, label="Retour",emoji=PartialEmoji(name="◀️"),custom_id="-1")
buttonBuy = interactions.Button(style=1, label="Acheter", emoji=getEmojiObject('<:coins:862425847523704832>'),custom_id="0")
onlyReturn = interactions.ActionRow(buttonReturn)

allBuyButton = interactions.Button(style=ButtonStyle.GRAY,label="Tout acheter",emoji=getEmojiObject('<:bought:906623435256504451>'),custom_id="buy all")
allGiveButton = interactions.Button(style=ButtonStyle.GRAY,label="Tout acheter et offrir",emoji=getEmojiObject('<:teamBought:906621631143743538>'),custom_id="buy'n'send all")

allBuyButtonButPoor = interactions.Button(style=ButtonStyle.SECONDARY,label="Vous êtes pauvre",emoji=getEmojiObject('<:bought:906623435256504451>'),custom_id="buy all",disabled=True)
allGiveButtonButPoor = interactions.Button(style=ButtonStyle.SECONDARY,label="Vous êtes pauvre, mais deluxe",emoji=getEmojiObject('<:teamBought:906621631143743538>'),custom_id="buy'n'send all",disabled=True)
allBuyButtonButAllreadyHaveM = interactions.Button(style=ButtonStyle.SECONDARY,label="Vous êtes un acheteur compulsif",emoji=getEmojiObject('<:bought:906623435256504451>'),custom_id="buy all",disabled=True)
allGiveButtonButAllreadyHaveM = interactions.Button(style=ButtonStyle.SECONDARY,label="Vous êtes un acheteur compulsif deluxe",emoji=getEmojiObject('<:teamBought:906621631143743538>'),custom_id="buy'n'send all",disabled=True)
allBuyButtonButAllreadyHaveF = interactions.Button(style=ButtonStyle.SECONDARY,label="Vous êtes une acheteuse compulsive",emoji=getEmojiObject('<:bought:906623435256504451>'),custom_id="buy all",disabled=True)
allGiveButtonButAllreadyHaveF = interactions.Button(style=ButtonStyle.SECONDARY,label="Vous êtes une acheteuse compulsive deluxe",emoji=getEmojiObject('<:teamBought:906621631143743538>'),custom_id="buy'n'send all",disabled=True)
global shopMaraine
shopMaraine = "iiiiii"

haveIcon, abigail = "<:bought:906623435256504451>", "<:abigail:1130264097271853056>"
allTeamHaveIcon = "<:teamBought:906621631143743538>"

npcIcons = {}
for npc in tablAllAllies+tablVarAllies+tablUniqueEnnemies+tablBoss+tablRaidBoss+tablBossPlus:
	npcIcons[npc.name] = [npc.icon, npc.splashIcon][npc.splashIcon != None]

npcIcons["Akia"] = '<a:akia:993550766415564831>'

def formatShop(txt:str) -> str:
	baddyTabl, randomTabl = ["","","","",""], ["","","","",""]
	if "baddy" in txt:
		for cmpt in range(0,5):
			baddyTabl[cmpt] = "<:baddy{0}:{1}>".format(cmpt,randRep([1003027064112287764,1003027102196572270,1113685316319072297,1113685339400327198]))

	if "{maraine}" in txt:
		global shopMaraine
		shopMaraine = shopMaraine + "iii"

	if "random" in txt:
		tablRandom = EmIcon[1]+EmIcon[2]
		for cmpt in (0,1,2,3,4):
			randomTabl[cmpt] = randRep(tablRandom)
			tablRandom.remove(randomTabl[cmpt])

	return txt.format(
		lena = npcIcons["Lena"],
		alice = npcIcons["Alice"],
		shushi = npcIcons["Shushi"],timeo="<:timeoB:1104517210728308746>",
		clemence = npcIcons["Clémence"], john = npcIcons["John"], sclem = '<:smallClemence:1236329023219437630>',
		luna = npcIcons["Luna"], stella = npcIcons["Stella"], celeste = npcIcons["Céleste"], abigail = abigail, oceane = "<:oceane:1243448244944638023>", glan = "<:glan:1218268667960098879>",
		feli = npcIcons["Félicité"], felicite = npcIcons["Félicité"],
		icealia = npcIcons["Icealia"], lohica=npcIcons["Lohica"],ly=npcIcons["Ly"],amary=npcIcons["Amary"],pirate='<:pirSab1:1059519845177249812>',pirate1='<:pirSab1:1059519845177249812>',pirate2='<:pirGun1:1059519820376330351>',pirate3='<:pirGun2:1059519760284528640>',
		shihu = npcIcons["Shihu"], stimeo = '<:stimeo:1089164206336647168>', itimeo = "<:itimeo:1103217741172846614>",
		shehisa = npcIcons["Shehisa"], helene = npcIcons["Hélène"], astra = npcIcons["Astra"],
		sixtine = npcIcons["Sixtine"], lily = npcIcons["Lily"], dSixtine = "<:dreamSixtine:1100793996483235851>",
		iliana = npcIcons["Iliana"], catili = '<:catIli:1006440617146060850>', childIli = "<:childIli:1089607519380443229>", miniIli = "<:miniIli:1089607564548898876>", aurora = npcIcons["Aurora"], gaurora = "<:gaurora:1103332091594281050>",
		gweny = npcIcons["Gwendoline"], alty = npcIcons["Altikia"], klikli = npcIcons["Klironovia"], karai = '<:karai:974079383197339699>',
		lio = npcIcons["Lio"], liu = npcIcons["Liu"], liz = npcIcons["Liz"], lia = npcIcons["Lia"], kitsune = npcIcons["Kitsune"], penelope = "<:penelope:1178446515459588106>", lei = '<:lei:1257691823170785372>',
		anna = npcIcons["Anna"], belle = npcIcons["Belle"],
		edelweiss = npcIcons["Edelweiss"], epiphyllum = npcIcons["Epiphyllum"],
		ruby = npcIcons["Ruby"], julie = npcIcons["Julie"],
		akia = npcIcons["Akia"],  ailill = npcIcons["Ailill"],
		nacialisla = npcIcons["Nacialisla"], silicia = "<:silicia:1045109225615003729>", powehi = npcIcons["Powehi"], aNacia = "<:airNacia:1208074166297952278>", fNacia = "<:fireNacia:1208074195888504902>", wNacia = "<:waterNacia:1208074216973410405>", eNacia = "<:earthNacia:1208074102569566209>",
		benedicte = npcIcons["Bénédicte"], amandine = npcIcons["Amandine"], candy = npcIcons["Candy"],
		kiku = npcIcons["Kiku"], churi = npcIcons["Chûri"], skeleton = "<a:smnMage:1054312154452471838>", churHin = npcIcons["Chûri-Hinoro"], anais="<:anais:1166806279042375780>",
		akira = npcIcons["Akira"], krys = npcIcons["Krys"],
		baddy1 = baddyTabl[0], baddy2 = baddyTabl[1], baddy3 = baddyTabl[2], baddy4 = baddyTabl[3], baddy5 = baddyTabl[4],
		maraine = "Mara{0}ne".format(shopMaraine), chauvesouris = "🦇", thomas = "Thomas",
		surrin = "<:surin:1113685316319072297>", bow = "<:bow:1113685339400327198>", imea = npcIcons["Imea"], isa = "<:isa:1158136337061400797>",
		soul = "<:ghostB:1119951487032901722>", jade = npcIcons["Jade"], alexandre = npcIcons["Alexandre"], zeneca = npcIcons["Zénéca"], kaleb='<:kaleb:1183176411452813433>', keuleyong = "<:keuleyong:1205465540337078292>",
		necro = "<:graveyard:1164906144339341424>", batiste = "<:batiste:1203788655240679534>", victoire = npcIcons["Victoire"],
		random1 = randomTabl[0], random2 = randomTabl[1], random3 = randomTabl[2], random4 = randomTabl[3], random5 = randomTabl[4],
		unknow="<:blocked:897631107602841600>", dzeneca=npcIcons["Phy"], krosnos = "<:kronos:1279709026015514668>", salestaly = "<:takoRed:866459004439756810>", halsta="<:ikaRed:866459224664702977>",
		elio = npcIcons["Lio"], eliu = npcIcons["Liu"], eliz = npcIcons["Liz"], elia = npcIcons["Lia Ex"])

async def shop2(bot : interactions.Client, ctx : interactions.Message,shopping : list):
	pathUserProfile, overloadShopMsg = absPath + "/userProfile/" + str(ctx.author.id) + ".json", None
	if not(os.path.exists(pathUserProfile)):
		await ctx.send(embeds = errorEmbed("shop","Vous n'avez pas commencé l'aventure"),ephemeral=True)

	user = loadCharFile(pathUserProfile)
	randRoll = random.randint(0,99)
	dateNow = datetime.now(parisTimeZone).replace(tzinfo=None)
	years = dateNow.year

	if randRoll < 10: shopTotalRandom = shopRandomMsg[:]
	elif randRoll < 25: shopTotalRandom = singingShopMsg[:]
	elif randRoll < 75: shopTotalRandom = shopMonthlyMsg[dateNow.month-1][:]
	else: shopTotalRandom = shopLastMonthlyMsg[dateNow.month-1][:]

	if dateNow > datetime.strptime("23/12/{0}".format(years),"%d/%m/%Y") and dateNow < datetime.strptime("4/1/{0}".format(years+1),"%d/%m/%Y"): shopTotalRandom += shopEventEndYears 

	for shopDict in shopEventOneDay:
		if shopDict["date"] == [dateNow.day,dateNow.month]: shopTotalRandom = shopDict["tabl"]; break

	tmp = shopTotalRandom[random.randint(0,len(shopTotalRandom)-1)]
	if type(tmp) == list: tmp = tmp[1]
	shopRdMsg = formatShop(tmp)
	
	initMsg = None

	if user.team != 0: teamList = userTeamDb.getTeamMember(user.team)
	else: teamList = [user.owner]

	buttonGift = interactions.Button(style=3, label="Offrir",emoji=PartialEmoji(name='🎁'),custom_id="1",disabled=len(teamList) == 1)
	buttonAllGift = interactions.Button(style=3, label="Offrir à tous",emoji=getEmojiObject('<:teamBought:906621631143743538>'),custom_id="2",disabled=len(teamList) == 1)

	allButtons = interactions.ActionRow(buttonReturn,buttonBuy,buttonGift,buttonAllGift)
	buttonsWithoutBuy = interactions.ActionRow(buttonReturn,buttonGift,buttonAllGift)

	abigailTalkingFile, isSunday = open(os.getcwd() + '/data/database/shopMsg.json',encoding="utf8"), datetime.now(parisTimeZone).weekday()==6
	abigailTalking, reduction = json.load(abigailTalkingFile)["abiShopMsg"], [1,0.7][isSunday]

	while 1:
		# Loading the user's team
		if len(teamList) > 1:
			teamMember = []
			for a in teamList:
				if a != int(ctx.author.id): teamMember += [loadCharFile(absPath + "/userProfile/" + str(a) + ".json")]

		reducMsg = ["","Réduction de 30% active !\n"][isSunday]
		shopEmb = interactions.Embed(title = "__Shop__",color = user.color, description = "Le magasin est commun à tous les serveurs et est actualisé toutes les 3 heures"+f"\n\nVous disposez actuellement de {user.currencies} <:coins:862425847523704832>.\nVous êtes en possession de **{round(userShopPurcent(user),2)}**% du magasin.\n{reducMsg}\n{shopRdMsg}")

		shopWeap,shopSkill,shopStuff,shopOther = [],[],[],[]
		for a in shopping:
			if type(a) == weapon: shopWeap.append(a)
			elif type(a) == skill: shopSkill.append(a)
			elif type(a) == stuff: shopStuff.append(a)
			else : shopOther.append(a)

		shopped, shopMsg, options = shopWeap+shopSkill+shopStuff+shopOther, ["__**Armes :**__","__**Compétences :**__","__**Equipement :**__","**__Autre :__**"], []
		listNotHave,listNotAllTeamHave,totalCost,totalTeamCost = [],[],0,0

		shopField = ["","","",""]
		for a in [0,1,2,3]:
			for b in [shopWeap,shopSkill,shopStuff,shopOther][a]:
				if b != None:
					price = int(b.price*reduction)
					shopField[a] += f"\n{b.emoji} {b.name} ({price} <:coins:862425847523704832>)"
					desc, desc2, icon = ["Arme","Compétence","Equipement","Autre"][a], "", ""

					if user.have(b): icon, desc2 = " ("+haveIcon+")", " - Possédé"
					else: listNotHave.append(b); totalCost += price

					if len(teamList) > 1:
						allTeamHave = True
						for c in teamMember:
							if not(c.have(b)):
								allTeamHave = False
								totalTeamCost += price

						if allTeamHave:
							icon = " ("+allTeamHaveIcon+")"
							desc2 = " - Toute votre équipe possède cet objet"
						else:
							listNotAllTeamHave.append(b)

					shopField[a] += icon
					options += [interactions.StringSelectOption(label=unhyperlink(b.name),value=b.id,emoji=getEmojiObject(b.emoji),description=desc+desc2)]

			shopField[a] = reduceEmojiNames(shopField[a])
			if len(shopField[a]) <= 1024:
				shopEmb.add_field(name="<:em:866459463568850954>\n"+shopMsg[a],value=shopField[a],inline=False)
			else:
				shopField[a] = ""
				for b in [shopWeap,shopSkill,shopStuff,shopOther][a]:
					if b != None:
						tempName, temp = "",""
						for letter in unhyperlink(b.name+" "):
							if letter == " ":
								if len(temp) > 4:
									tempName += " {0}.".format(temp[:3])
								else:
									tempName += " {0}".format(temp[:4])
								temp = ""
							else:
								temp += letter
						price = int(b.price*reduction)
						shopField[a] += f"\n{b.emoji}{tempName} : {price} pièces"
						icon = ""
						if user.have(b):
							icon = " (☑️)"

						if len(teamList) > 1:
							allTeamHave = True
							for c in teamMember:
								if not(c.have(b)):
									allTeamHave = False
									break

							if allTeamHave:
								icon = " (✅)"

						shopField[a] += icon

				if shopField[a] == "":
					shopField[a] = "???"

				shopEmb.add_field(name="<:em:866459463568850954>\n"+shopMsg[a],value=shopField[a],inline=False)
	   
		tmpValue, notFight, cd, cd2, fightingStatus = "","", teamWinDB.getFightCooldown(user.team,timestamp=True), teamWinDB.getFightCooldown(user.team, True, timestamp=True), teamWinDB.isFightingBool(int(user.team))
		if not(globalVar.fightEnabled()):
			notFight = "**<:noneWeap:917311409585537075> __Les combats sont actuellement désactivées !__**\n\n"
		else:
			tmpValue = "__Normal__ :\n"
			if fightingStatus[0]:
				tmpValue += "__Votre équipe affronte actuellement :__\n"
				tablEnnemis = fightingStatus[1].split(";")[:-1]
				for enemyName in tablEnnemis:
					ennemi = findEnnemi(enemyName)
					if ennemi == None: ennemi = findAllie(enemyName)
					if ennemi != None: tmpValue += "{0} {1}\n".format(ennemi.icon, ennemi.name)
					else: tmpValue += "<:blocked:897631107602841600> L'ennemi n'a pas pu être trouvé\n"
			elif user.team in allReadyInWait.keys():
				tmpStr = allReadyInWait[user.team].split(":")
				tmpChannel = await bot.fetch_channel(int(tmpStr[1]))
				tmpMsg = tmpChannel.get_message(int(tmpStr[0]))
				tmpValue += "Votre équipe est en file d'attente ({0}) ({1})\n".format(tmpMsg.jump_url,cd)
			else: tmpValue += cd+"\n"

			tmpValue += "__Rapide__ :\n"
			if user.team in allReadyInWaitQuick.keys():
				tmpStr = allReadyInWaitQuick[user.team].split(":")
				tmpChannel = await bot.fetch_channel(int(tmpStr[1]))
				tmpMsg = tmpChannel.get_message(int(tmpStr[0]))
				tmpValue += "Votre équipe est en file d'attente ({0}) ({1})\n".format(tmpMsg.jump_url,cd2)
			else: tmpValue += cd2

		shopEmb.add_field(name="<:em:866459463568850954>\n__Temps de rechargements :__",value=notFight+tmpValue)

		select = interactions.StringSelectMenu(options,custom_id = "seeMoreInfos",placeholder="Un article vous interesse ?")

		if totalCost == 0:
			temp1 = [allBuyButtonButAllreadyHaveM,allBuyButtonButAllreadyHaveF,allBuyButtonButAllreadyHaveM][user.gender]
		else:
			temp1 = copy.deepcopy(allBuyButton)
			temp1.label += " ({0})".format(totalCost)
			if user.currencies < totalCost:
				temp1.disabled, temp1.style = True, ButtonStyle.GRAY

		actrow2 = ActionRow(temp1)
		if len(teamList)>1:
			if totalTeamCost == 0:
				actrow2.add_component([allGiveButtonButAllreadyHaveM,allGiveButtonButAllreadyHaveF,allGiveButtonButAllreadyHaveM][user.gender])
			else:
				tempComp = copy.deepcopy(allGiveButton)
				tempComp.label += " ({0})".format(totalTeamCost)
				if user.currencies < totalTeamCost:
					tempComp.disabled, tempComp.style = True, ButtonStyle.GRAY
				actrow2.add_component(tempComp)

		if initMsg != None:
			await initMsg.edit(embeds = shopEmb,components=[interactions.ActionRow(select),actrow2])
		else:
			try:
				initMsg = await ctx.send(embeds = shopEmb,components=[interactions.ActionRow(select),actrow2])
			except:
				tempShopEmb, shopEmb.description, shopEmb.title, shopEmb.fields[0].name = interactions.Embed(title=shopEmb.title, description=shopEmb.description, color=shopEmb.color), "", "", "__Armes :__"
				overloadShopMsg = await ctx.send(embeds=tempShopEmb)
				initMsg = await ctx.channel.send(embeds = shopEmb,components=[interactions.ActionRow(select),actrow2])

		def check(m):
			m = m.ctx
			return int(m.author.id) == int(ctx.author.id)

		try:
			respond = await bot.wait_for_component(messages=initMsg,check=check,timeout=60)
			respond: ComponentContext = respond.ctx
			await respond.defer()
		except asyncio.TimeoutError :
			timeoutEmbed = interactions.Embed(title="__Shop__",color=user.color,description=shopRdMsg)
			await initMsg.edit(embeds = timeoutEmbed,components=[])
			if overloadShopMsg != None:
				await overloadShopMsg.delete()
			return 0
		except Exception as e:
			await initMsg.edit(embeds=Embed(title="Une erreur est survenue",description=format_exc(limit=4000)))

		if respond.component_type == 2:
			if respond.custom_id =="buy all":
				tempMsg = await respond.send(embeds=interactions.Embed(title="__/shop__",color=user.color,description=abigail + " : " + abigailTalking["buyAll"][random.randint(0,len(abigailTalking["buyAll"])-1)]))
				user = loadCharFile(user.owner)
				tempTabl = []
				for obj in listNotHave:
					if not(user.have(obj)) and user.currencies >= int(obj.price*reduction):
						[user.weaponInventory,user.skillInventory,user.stuffInventory,user.otherInventory][whatIsThat(obj)].append(obj)
						user.currencies -= int(obj.price*reduction)
						tempTabl += [[obj.emoji,obj.name]]
				saveCharFile("./userProfile/{0}.json".format(user.owner),user)
				temp = ""
				for a in tempTabl:
					temp += "{0} {1}\n".format(a[0],a[1])
				await tempMsg.edit(embeds=interactions.Embed(title="__/shop__",color=user.color, description=abigail + " : " + abigailTalking["buyAllEnd"][random.randint(0,len(abigailTalking["buyAllEnd"])-1)]+"\n"+temp))

			elif respond.custom_id == "buy'n'send all":
				tempMsg = await respond.send(embeds=interactions.Embed(title="__/shop__",color=user.color,description=abigail + " : " + abigailTalking["buyAllAndSend"][random.randint(0,len(abigailTalking["buyAllAndSend"])-1)]))
				user = loadCharFile("./userProfile/{0}.json".format(user.owner))
				tempTabl1,tempTabl2,tempTabl3 = [],[],[]
				for teamUser in teamMember:
					gifted = loadCharFile("./userProfile/{0}.json".format(teamUser.owner))
					for obj in listNotAllTeamHave:
						if not(gifted.have(obj)) and user.currencies >= int(obj.price*reduction):
							[gifted.weaponInventory,gifted.skillInventory,gifted.stuffInventory,gifted.otherInventory][whatIsThat(obj)].append(obj)
							user.currencies -= int(obj.price*reduction)

							if obj.name not in tempTabl1:
								tempTabl1.append(obj.name)
								tempTabl2.append(1)
								tempTabl3.append(obj.emoji)
							else:
								for cmpt in range(len(tempTabl1)):
									if tempTabl1[cmpt] == obj.name:
										tempTabl2[cmpt] += 1

					saveCharFile("./userProfile/{0}.json".format(gifted.owner),gifted)

				for obj in listNotAllTeamHave:
					if not(user.have(obj)) and user.currencies >= int(obj.price*reduction):
						[user.weaponInventory,user.skillInventory,user.stuffInventory,user.otherInventory][whatIsThat(obj)].append(obj)
						user.currencies -= int(obj.price*reduction)

				temp = ""
				for cmpt in range(len(tempTabl1)):
					temp += "{0} {1} *x{2}*\n".format(tempTabl3[cmpt],tempTabl1[cmpt],tempTabl2[cmpt])

				saveCharFile("./userProfile/{0}.json".format(user.owner),user)
				await tempMsg.edit(embeds=interactions.Embed(title="__/shop__",color=user.color, description=abigail +" : "+ abigailTalking["buyAllAndSendEnd"][random.randint(0,len(abigailTalking["buyAllAndSendEnd"])-1)]+"\n"+temp))

		else:
			await initMsg.edit(embeds = shopEmb,components=[interactions.ActionRow(getChoisenSelect(select,respond.values[0]))])
			rep = None
			for a in range(0,len(shopped)):
				if shopped[a].id == respond.values[0]:
					rep = a
					break

			try:
				msg = await respond.send(embeds = interactions.Embed(title="shop",description="Recherche de l'objet dans les rayons..."))
			except:
				msg = await initMsg.channel.send(embeds = interactions.Embed(title="shop",description="Recherche de l'objet dans les rayons..."))

			try:
				if rep == None:					 # Object not found
					await msg.edit(embeds=interactions.Embed(title="Error in shop command",description="Unfound object"))
				else:
					typ, obj = whatIsThat(shopped[rep]), shopped[rep]
					if typ == 0:
						repEmb = infoWeapon(obj,user,ctx)
					elif typ == 1:
						repEmb = infoSkill(shopped[rep],user,ctx)
					elif typ == 2:
						repEmb = infoStuff(obj,user,ctx)
					elif typ == 3:
						repEmb = infoOther(obj,user)

					if user.currencies < int(obj.price*reduction):
						repEmb.set_footer(text = "Vous n'avez pas suffisament de pièces")
						await msg.edit(embeds = repEmb,components=[onlyReturn])
					else:
						if user.have(obj):
							repEmb.set_footer(text = "Vous possédez déjà cet objet")
							await msg.edit(embeds = repEmb,components=[buttonsWithoutBuy])
						else:
							repEmb.set_footer(text = "Cliquez sur le bouton \"Acheter\" pour acheter cet objet")
							await msg.edit(embeds = repEmb,components=[allButtons])

						try:
							rep = await bot.wait_for_component(messages=msg,check=check,timeout=60)
							rep: ComponentContext = rep.ctx
						except:
							await msg.delete()
							rep = None

						if rep != None:
							if rep.custom_id == "0":				# Buy for them self
								try:
									if typ == 0:
										user.weaponInventory.append(obj)
									elif typ == 1:
										user.skillInventory.append(obj)
									elif typ == 2:
										user.stuffInventory.append(obj)
									elif typ == 3:
										user.otherInventory.append(obj)
									user.currencies = user.currencies - int(obj.price*reduction)
									saveCharFile(pathUserProfile,user)
									await msg.edit(embeds = interactions.Embed(title="shop"+ " - " +obj.name,color = user.color,description = f"Votre achat a bien été effectué ! Faites \"/inventory nom:{obj.id}\" pour l'équiper"),components=[])
								except:
									await msg.edit(embeds = errorEmbed("shop","Une erreur s'est produite"))

							elif rep.custom_id == "1":			  # Gift to annother teamMate
								options = []
								for a in teamMember:
									if not(a.have(obj)) and a.owner != user.owner:
										options += [interactions.StringSelectOption(label=a.name,value=str(a.owner),emoji=getEmojiObject(await getUserIcon(bot,a)))]

								if options == [] :
									select = interactions.StringSelectMenu([interactions.StringSelectOption(label="Vous n'avez pas à voir ça",value="Nani")],placeholder="Toute votre équipe a déjà cet objet",disabled=True,custom_id = "ohYouWantToSeeThis")
								else:
									select = interactions.StringSelectMenu(options,custom_id = "mudamudamudamudamuda",placeholder="À qui voulez vous offrir cet objet ?")
								await msg.edit(embeds= repEmb, components=[interactions.ActionRow(buttonReturn),interactions.ActionRow(select)])

								respond = None
								try:
									respond = await bot.wait_for_component(messages=msg,timeout = 60)
									respond: ComponentContext = respond.ctx
								except:
									await msg.delete()
								if respond != None:
									try:
										for teamMate in teamMember:
											if teamMate.owner == respond.values[0]:
												try:
													try:
														temp = await respond.send("Envoie du cadeau...")
													except:
														temp = await initMsg.channel.send("Envoie du cadeau...")
													if typ == 0:
														teamMate.weaponInventory.append(obj)
													elif typ == 1:
														teamMate.skillInventory.append(obj)
													elif typ == 2:
														teamMate.stuffInventory.append(obj)
													elif typ == 3:
														teamMate.otherInventory.append(obj)
													user.currencies = user.currencies - int(obj.price*reduction)
													saveCharFile(absPath + "/userProfile/" + str(teamMate.owner) + ".json",teamMate)
													saveCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".json",user)
													await temp.delete()
													await msg.edit(embeds = interactions.Embed(title="shop",color = user.color,description = f"Votre cadeau a bien été envoyé !"),components = [interactions.ActionRow(getChoisenSelect(select,respond.values[0]))])
												except:
													await msg.edit(embeds = errorEmbed("shop","Une erreur s'est produite"))
												break
									except:
										await msg.delete()

							elif rep.custom_id == "2":
								tablTeamToGift, msgTeamToGift = [],"Voulez vous offrir __{0}__ aux coéquipiers suivants ?\n".format(obj.name)

								for a in teamMember:
									if obj not in a.otherInventory:
										tablTeamToGift.append(a)
										msgTeamToGift += "{0} {1}\n".format(await getUserIcon(bot,a), a.name)

								msgTeamToGift += "\nPrix total : {0} <:coins:862425847523704832>".format(int(obj.price*reduction) * len(tablTeamToGift))

								if user.currencies >= int(obj.price*reduction) * len(tablTeamToGift):
									buttonConfirm = interactions.Button(style=1,label="Rendez moi pauvre !",emoji=getEmojiObject('<:coins:862425847523704832>'),custom_id="buy")
								else:
									buttonConfirm = interactions.Button(style=1,label="Rendez moi pauvre !",emoji=getEmojiObject('<:coins:862425847523704832>'),custom_id="buy",disabled=True)

								await msg.edit(embeds = interactions.Embed(title="__/shop {0}__".format(obj.name),color=user.color,description=msgTeamToGift),components=[interactions.ActionRow(buttonReturn,buttonConfirm)])

								try:
									respond = await bot.wait_for_component(messages=msg,timeout = 60,check=check)
									respond: ComponentContext = respond.ctx
								except:
									break

								if respond.custom_id == "buy":
									await msg.edit(embeds = interactions.Embed(title="__/shop {0}__".format(obj.name),color = user.color,description = f"Envoie de vos cadeaux... <a:loading:862459118912667678>"),components = [])
									for a in tablTeamToGift:
										if int(a.owner) != int(user.owner):
											if typ == 0:
												a.weaponInventory.append(obj)
											elif typ == 1:
												a.skillInventory.append(obj)
											elif typ == 2:
												a.stuffInventory.append(obj)
											elif typ == 3:
												a.otherInventory.append(obj)
											user.currencies = user.currencies - int(obj.price*reduction)
											saveCharFile(absPath + "/userProfile/" + str(a.owner) + ".json",a)
											saveCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".json",user)

										else:
											user.otherInventory += [obj]
											user.currencies = user.currencies - int(obj.price*reduction)
											saveCharFile(absPath + "/userProfile/" + str(ctx.author.id) + ".json",user)
									await msg.edit(embeds = interactions.Embed(title="shop",color = user.color,description = f"Vos cadeaux ont bien été envoyés !"),components = [])
								else:
									await msg.delete()

							elif rep.custom_id == "-1":
								await msg.delete()
			except:
				await msg.edit(embeds=interactions.Embed(title="Uncatch error in shop command",description=format_exc()),components=[])

if not(isLenapy):
	print("Shop message verification...")
	tablShopMsg = shopRandomMsg+shopEventEndYears
	for temp in shopEventOneDay: tablShopMsg = tablShopMsg + temp["tabl"]
	for temp in shopMonthlyMsg: tablShopMsg = tablShopMsg+temp

	for shopmsg in tablShopMsg:
		try:
			if type(shopmsg) == list: formatShop(shopmsg[1])
			else: formatShop(shopmsg)
		except: print("Error with the following shop message :\n{0}".format(shopmsg)); print_exc()
	print("Shop message verification done")

async def seeSkillsRep(ctx : interactions.SlashContext, skillType:int, aspiration:int = None, element:int = None, use: int=None, skillRange : int = None):
	tablToSee: List[skill] = skillsCat[skillType][:]
	firstMsgSend = False

	for skillToSee in tablToSee[:]:
		if (element != None and skillToSee.condition != [EXCLUSIVE,ELEMENT,element]) or (aspiration != None and skillToSee.condition != [EXCLUSIVE,ASPIRATION,aspiration]) or (use != None and skillToSee.use != use):
			try:
				tablToSee.remove(skillToSee)
			except:
				pass

	tablsCd: List[List[skill]] = [[],[],[]]
	for skilly in tablToSee:
		if (use == None or skilly.use == use):
			if skilly.cooldown <= 3:
				tablsCd[0].append(skilly)
			elif skilly.cooldown <= 5:
				tablsCd[1].append(skilly)
			else:
				tablsCd[2].append(skilly)

	tablLens, lenTot = [0,len(tablsCd[0]),len(tablsCd[1])+len(tablsCd[0])], len(tablsCd[0])+len(tablsCd[1])+len(tablsCd[2])

	if len(tablsCd[0]) + len(tablsCd[1]) + len(tablsCd[2]) > 0:
		for cmpt in range(3):
			tablsCd[cmpt].sort(key=lambda ballerine : ballerine.iaPow, reverse=True)
			desc = ""
			for cmpt2 in range(len(tablsCd[cmpt])):
				desc += "{0} {2}{1}{2}".format(tablsCd[cmpt][cmpt2].emoji, tablsCd[cmpt][cmpt2].name, ["","~~"][tablsCd[cmpt][cmpt2] in listUseSkills])
				toAdd = ""
				if len(tablsCd[cmpt][cmpt2].condition) > 0:
					if tablsCd[cmpt][cmpt2].condition[1] == ASPIRATION:
						toAdd += aspiEmoji[tablsCd[cmpt][cmpt2].condition[2]]
					elif tablsCd[cmpt][cmpt2].condition[1] == ELEMENT:
						toAdd += elemEmojis[tablsCd[cmpt][cmpt2].condition[2]]
				if tablsCd[cmpt][cmpt2].ultimate :
					toAdd += "<:littleStar:925860806602682369>"
				if tablsCd[cmpt][cmpt2].group == SKILL_GROUP_DEMON:
					toAdd += "<:dmon:1004737763771433130>"
				elif tablsCd[cmpt][cmpt2].group == SKILL_GROUP_HOLY:
					toAdd += "<:dvin:1004737746377654383>"
				if toAdd != "":
					desc += " - {0}".format(toAdd)
				desc += "\n"
				if len(desc) > 4000 or tablsCd[cmpt][cmpt2] == tablsCd[cmpt][-1]:
					if not(firstMsgSend):
						if ctx.__class__ == interactions.Message:
							await ctx.edit(embeds=interactions.Embed(title="__Cooldown {0}__".format(["faible","moyen","élevé"][cmpt]),description=desc,color=light_blue,footer=EmbedFooter(text="{0}/{1}".format(tablLens[cmpt]+cmpt2+1,lenTot))))
						else:
							await ctx.send(embeds=interactions.Embed(title="__Cooldown {0}__".format(["faible","moyen","élevé"][cmpt]),description=desc,color=light_blue,footer=EmbedFooter(text="{0}/{1}".format(tablLens[cmpt]+cmpt2+1,lenTot))))
						firstMsgSend = True
					else:
						await ctx.channel.send(embeds=interactions.Embed(title="__Cooldown {0}__".format(["faible","moyen","élevé"][cmpt]),description=desc,color=light_blue,footer=EmbedFooter(text="{0}/{1}".format(tablLens[cmpt]+cmpt2+1,lenTot))))
					desc = ""
	else:
		
		await ctx.send(embeds=interactions.Embed(title="__Aucune correspondance__",description="-",color=light_blue))

async def testShopMsgFunction(ctx: interactions.SlashContext):
	listEmbed: List[interactions.Embed] = []
	dateNow, started = datetime.now(parisTimeZone), False
	print(dateNow.month)
	for cmpt in range(len(shopMonthlyMsg[dateNow.month-1])):
		if not(started):
			await ctx.send(embeds=[interactions.Embed(title=str(cmpt),description=formatShop(shopMonthlyMsg[dateNow.month-1][cmpt]))])
			started = True
		else:
			await ctx.channel.send(embeds=[interactions.Embed(title=str(cmpt),description=formatShop(shopMonthlyMsg[dateNow.month-1][cmpt]))])

tcBoosterCost, tcCardCost = (60,80,120,160), (30,50,70,100)
cnBoosterCost, cnCardCost = (1000,2000,3000,5000), (500,750,1350,2500)

async def chipShop(bot: interactions.Client, ctx: interactions.SlashContext):
	if not(os.path.exists("./userProfile/{0}.json".format(int(ctx.author_id)))):
		await ctx.send(content="Vous n'avez pas encore de personnage. Commencez d'abord avec la commande **/start** !",ephemeral=True)
		return 0

	await ctx.defer()

	try:
		user, msg, secMsg, secButtons, hasSelected = loadCharFile(int(ctx.author_id)), None, None, None, None
		chipShopMsgFile = open("./data/database/shopMsg.json","r",encoding="utf8")
		chipShopMsg = json.load(chipShopMsgFile)["chipShopMsg"]
		chipShopMsgFile.close()
		chipShopMsg = chipShopMsg[["oceaneSingle","oceaneSingle","glanSingle","glanSingle","oceaneGlanDuo"][random.randint(0,4)]]
		shopDesc = chipShopMsg["shopDsc"][random.randint(0,len(chipShopMsg["shopDsc"])-1)]
		
		jsonFile = open("./data/database/dailyShop.json")
		chipShopContent = json.load(jsonFile)["dailyShop"]

		makeOfferOptions = []
		for tmpChipId in user.equippedChips:
			tmpChip = getChip(tmpChipId)
			if tmpChip != None:
				makeOfferOptions.append(StringSelectOption(label=tmpChip.name,value="offer_"+str(tmpChipId),emoji=[None,getEmojiObject(tmpChip.emoji)][tmpChip.emoji != ""],description="Niveau {0} - {1}/{2} - {3} TC".format(user.chipInventory[tmpChipId].lvl, user.chipInventory[tmpChipId].progress, nbChipsForLvlUp[user.chipInventory[tmpChipId].lvl-rarityMinLvl[user.chipInventory[tmpChipId].rarity]], int(tcCardCost[user.chipInventory[tmpChipId].rarity]*1.5))))

		isOffer = False
		while 1:
			mainEmbed, totalCardCost, totalCoinCost, shopOptionList = Embed(title="__Chip Shop__",description=reduceEmojiNames("Vous possédez {0} <:tc:1218274555081261116> et {1} <:coins:862425847523704832>\n\n".format(separeUnit(user.tc), separeUnit(user.currencies))+formatShop(shopDesc)+"\n<:empty:866459463568850954>"),color=user.color), 0, 0, []
			packName, packPriceCards, packPriceCoins = "Booster de puces "+["commun","rare","légendaire","mythique"][chipShopContent["dailyBooster"]], tcBoosterCost[chipShopContent["dailyBooster"]], cnBoosterCost[chipShopContent["dailyBooster"]]
			mainEmbed.add_field(name="__Booster du jour :__",value="{0} {1} {2}".format(rarityEmojis[chipShopContent["dailyBooster"]],packName,["({0} <:tc:1218274555081261116> / {1} <:coins:862425847523704832>)".format(packPriceCards,packPriceCoins),"({0})".format(haveIcon)][user.owner in chipShopContent["hasBought"][0]]))

			if user.owner not in chipShopContent["hasBought"][0]:
				totalCardCost, totalCoinCost = totalCardCost+packPriceCards, totalCoinCost+packPriceCoins
				shopOptionList.append(StringSelectOption(label=packName,value="booster_{0}".format(chipShopContent["dailyBooster"]),emoji=getEmojiObject(rarityEmojis[chipShopContent["dailyBooster"]])))

			secFieldValue, chipsInShop, tmpChipNb = "", getChip(chipShopContent["chipShop"]), {}
			for cmpt, tmpChip in enumerate(chipsInShop):
				cardCardCost, cardCoinCost = tcCardCost[tmpChip.rarity],cnCardCost[tmpChip.rarity]
				tmpChipNb[cmpt] = max([10,5,3,1][tmpChip.rarity], int(nbChipsForLvlUp[user.chipInventory[tmpChip.id].lvl-rarityMinLvl[user.chipInventory[tmpChip.id].rarity]]*0.1))
				secFieldValue += "{0} {1}*{2}* x**{4}** {3}\n".format(rarityEmojis[tmpChip.rarity],tmpChip.emoji+[""," "][tmpChip.emoji != ""],tmpChip.name,["({0} <:tc:1218274555081261116> / {1} <:coins:862425847523704832>)".format(cardCardCost, cardCoinCost),"({0})".format(haveIcon)][user.owner in chipShopContent["hasBought"][1][cmpt]],tmpChipNb[cmpt])
				if user.owner not in chipShopContent["hasBought"][1][cmpt]:
					totalCardCost, totalCoinCost = totalCardCost+cardCardCost, totalCoinCost+cardCoinCost
					shopOptionList.append(StringSelectOption(label=tmpChip.name,value="chip_{0}".format(cmpt),emoji=[getEmojiObject(tmpChip.emoji),None][tmpChip.emoji == ""]))

			mainEmbed.add_field(name="__Puces du jour :__",value=secFieldValue)

			if len(shopOptionList) > 0:actRowSelect = ActionRow(StringSelectMenu(shopOptionList,placeholder="Tu veux voir quelque chose de plus près ?"))
			else: actRowSelect = ActionRow(StringSelectMenu(StringSelectOption(label='Vous avez déjà acheté toutes les offres',default=True,value="shopn't"),disabled=True,placeholder="Tu veux voir quelque chose de plus près ?"))

			actRowSelfAllBuy = ActionRow(
				Button(style=ButtonStyle.GRAY,label='{0} '.format(separeUnit(totalCardCost)) + chipShopMsg["buyCardButton"][random.randint(0,len(chipShopMsg["buyCardButton"])-1)],emoji=getEmojiObject('<:tc:1218274555081261116>'),custom_id='buyAllSoloCards', disabled=totalCardCost > user.tc or totalCardCost <= 0),
				Button(style=ButtonStyle.GRAY,label='{0} '.format(separeUnit(totalCoinCost))+ chipShopMsg["buyCoinButton"][random.randint(0,len(chipShopMsg["buyCoinButton"])-1)],emoji=getEmojiObject('<:coins:862425847523704832>'),custom_id='buyAllSoloCoins', disabled=totalCoinCost > user.currencies or totalCoinCost <= 0)
			)

			disablepString = False
			if user.owner in chipShopContent["hasBought"][2]: makeOfferOptions, disablepString = [StringSelectOption(label="Vous avez déjà fait une offre pour aujourd'hui",value="disabled",default=True)], True
			elif len(makeOfferOptions) == 0: makeOfferOptions, disablepString = [StringSelectOption(label="Vous devez avoir une puce équipée pour faire une offre",value="disabled",default=True)], True

			makeOfferSelect = ActionRow(StringSelectMenu(makeOfferOptions,placeholder="Faire une offre",disabled = disablepString,custom_id = "makeOffer"))

			for inx, field in enumerate(mainEmbed.fields): mainEmbed.fields[inx].value = reduceEmojiNames(field.value)

			if ctx.responded: await msg.edit(embeds=mainEmbed, components=[actRowSelect,makeOfferSelect,actRowSelfAllBuy])
			else: msg = await ctx.respond(embeds=mainEmbed, components=[actRowSelect,makeOfferSelect,actRowSelfAllBuy])

			def check(m):
				m = m.ctx
				return m.author_id == ctx.author_id

			try:
				respond = await bot.wait_for_component(messages=[msg]+[[],[secMsg]][secMsg!=None],components=[actRowSelect,makeOfferSelect,actRowSelfAllBuy]+[[],[secButtons]][secButtons != None],check=check,timeout=60)
				respond: ComponentContext = respond.ctx
				await respond.defer()
			except asyncio.TimeoutError:
				await msg.edit(embeds=mainEmbed, components=[])
				break
			
			if len(shopOptionList) == 0:
				actRowSelfAllBuy.components[0].disabled = actRowSelfAllBuy.components[1].disabled = actRowSelect.components[0].disabled = True
			await msg.edit(embeds=mainEmbed, components=[actRowSelect,actRowSelfAllBuy])

			if respond.component_type == ComponentType.STRING_SELECT:
				hasSelected, tcCost, coinCost = respond.values[0], 0, 0
				isOffer = hasSelected.startswith("offer_")
				if hasSelected.startswith("booster_"):
					boosterRarity = int(hasSelected.replace("booster_",""))
					embDesc = reduceEmojiNames("Vous octroie une dizaine de puce. Les puces {2} Communes et {3} Rares ont **30%** de chance d'être doublé (**9%** qu'une puce {2} Commune soit triplé)\n\nProbabilité par tirage :\n{2} : {4}%, {3} : {5}%, {6} : {7}%, {8} : {9}%".format(
						rarityEmojis[boosterRarity], ["commun","rare","légendaire","mythique"][boosterRarity], rarityEmojis[0], rarityEmojis[1], probaRarityTabl[boosterRarity][0]/10, probaRarityTabl[boosterRarity][1]/10, rarityEmojis[2], probaRarityTabl[boosterRarity][2]/10, rarityEmojis[3], probaRarityTabl[boosterRarity][3]/10
					))
					tcCost, coinCost = tcBoosterCost[chipShopContent["dailyBooster"]], cnBoosterCost[chipShopContent["dailyBooster"]]
					secEmbed = Embed(title="{0} __Booster de puces {1} :__".format(rarityEmojis[boosterRarity], ["commun","rare","légendaire","mythique"][boosterRarity]),color=user.color,description=embDesc)

					secButtons = ActionRow(
						Button(style=ButtonStyle.GRAY,label='{0} '.format(separeUnit(tcCost)) + chipShopMsg["buyCardButton"][random.randint(0,len(chipShopMsg["buyCardButton"])-1)],emoji=getEmojiObject('<:tc:1218274555081261116>'),custom_id='buyCards', disabled=tcCost > user.tc),
						Button(style=ButtonStyle.GRAY,label='{0} '.format(separeUnit(coinCost))+ chipShopMsg["buyCoinButton"][random.randint(0,len(chipShopMsg["buyCoinButton"])-1)],emoji=getEmojiObject('<:coins:862425847523704832>'),custom_id='buyCoins', disabled=coinCost > user.currencies)
					)
				elif hasSelected.startswith("offer_"):
					tmpChip = getChip(int(hasSelected.replace("offer_","")))
					chipOwned = user.chipInventory[tmpChip.id]
					embDesc = tmpChip.description.replace("%power","({0} → {1})".format(tmpChip.minValue, tmpChip.maxValue)).replace("%lvlPower","{0} → {1}".format(int(tmpChip.minValue/100*user.level), int(tmpChip.maxValue/100*user.level))) + "\n\n" + ["*Vous ne possédez pas encore cette puce*","*Niveau actuel : **{0}** (**{1}**/{2})*".format(chipOwned.lvl,chipOwned.progress,nbChipsForLvlUp[chipOwned.lvl-rarityMinLvl[chipOwned.rarity]])][chipOwned.lvl>rarityMinLvl[chipOwned.rarity]]
					secEmbed = Embed(title="{0} {1}__{2} :__".format(rarityEmojis[tmpChip.rarity],tmpChip.emoji+['',' '][tmpChip.emoji != ""], tmpChip.name),description=embDesc,color=user.color)

					tcCost = int(tcCardCost[tmpChip.rarity]*1.5)

					secButtons = ActionRow(
						Button(style=ButtonStyle.GRAY,label='{0} '.format(separeUnit(tcCost)) + chipShopMsg["buyCardButton"][random.randint(0,len(chipShopMsg["buyCardButton"])-1)],emoji=getEmojiObject('<:tc:1218274555081261116>'),custom_id='buyCards', disabled=tcCost > user.tc),
						)

				else:
					selectedChipId = chipsInShop[int(hasSelected.replace("chip_",""))].id
					selectedChip, chipOwned = chipList[selectedChipId], user.chipInventory[selectedChipId]
					embDesc = selectedChip.description.replace("%power","({0} → {1})".format(selectedChip.minValue, selectedChip.maxValue)).replace("%lvlPower","{0} → {1}".format(int(selectedChip.minValue/100*user.level), int(selectedChip.maxValue/100*user.level))) + "\n\n" + ["*Vous ne possédez pas encore cette puce*","*Niveau actuel : **{0}** (**{1}**/{2})*".format(chipOwned.lvl,chipOwned.progress,nbChipsForLvlUp[chipOwned.lvl-rarityMinLvl[chipOwned.rarity]])][chipOwned.lvl>rarityMinLvl[chipOwned.rarity]]
					secEmbed = Embed(title="{0} {1}__{2} :__".format(rarityEmojis[selectedChip.rarity],selectedChip.emoji+['',' '][selectedChip.emoji != ""], selectedChip.name),description=embDesc,color=user.color)

					tcCost, coinCost = tcCardCost[tmpChip.rarity],cnCardCost[tmpChip.rarity]

					secButtons = ActionRow(
						Button(style=ButtonStyle.GRAY,label='{0} '.format(separeUnit(tcCost)) + chipShopMsg["buyCardButton"][random.randint(0,len(chipShopMsg["buyCardButton"])-1)],emoji=getEmojiObject('<:tc:1218274555081261116>'),custom_id='buyCards', disabled=tcCost > user.tc),
						Button(style=ButtonStyle.GRAY,label='{0} '.format(separeUnit(coinCost))+ chipShopMsg["buyCoinButton"][random.randint(0,len(chipShopMsg["buyCoinButton"])-1)],emoji=getEmojiObject('<:coins:862425847523704832>'),custom_id='buyCoins', disabled=coinCost > user.currencies)
					)

				if secMsg == None:
					secMsg = await respond.respond(embeds=secEmbed,components=[secButtons])
				else:
					await secMsg.edit(embeds=secEmbed,components=[secButtons])

			elif respond.component_type == ComponentType.BUTTON and respond.component.custom_id in ["buyAllSoloCards","buyAllSoloCoins"]:
				tmpDesc = ""
				if user.owner not in chipShopContent["hasBought"][0] and [user.tc, user.currencies][respond.component.custom_id == "buyAllSoloCoins"] >= [tcBoosterCost,cnBoosterCost][respond.component.custom_id == "buyAllSoloCoins"][chipShopContent["dailyBooster"]]:
					user, tmpDesc = openBooster(user=user, boosters = [chipShopContent["dailyBooster"]], infield = False)
					if respond.component.custom_id == "buyAllSoloCoins":
						user.currencies -= cnBoosterCost[chipShopContent["dailyBooster"]]
					else:
						user.tc -= tcBoosterCost[chipShopContent["dailyBooster"]]

					chipShopContent["hasBought"][0].append(user.owner)
				
				temp = ""
				for indx, tmpChip in enumerate(chipsInShop):
					if user.owner not in chipShopContent["hasBought"][1][indx] and [user.tc, user.currencies][respond.component.custom_id == "buyAllSoloCoins"] > [tcCardCost,cnCardCost][respond.component.custom_id == "buyAllSoloCoins"][tmpChip.rarity]:
						hadLvlUp = False
						user.chipInventory[tmpChip.id].progress += tmpChipNb[indx]
						if respond.component.custom_id == "buyAllSoloCoins":
							user.currencies -= cnCardCost[tmpChip.rarity]
						else:
							user.tc -= tcCardCost[tmpChip.rarity]

						chipShopContent["hasBought"][1][indx].append(user.owner)
						while user.chipInventory[tmpChip.id].progress > nbChipsForLvlUp[user.chipInventory[tmpChip.id].lvl-rarityMinLvl[tmpChip.rarity]]:
							user.chipInventory[tmpChip.id].lvl += 1
							user.chipInventory[tmpChip.id].progress -= user.chipInventory[tmpChip.id].lvl-rarityMinLvl[tmpChip.rarity]
							hadLvlUp = True
						
						temp += "{4} {0}*{1}* x**{2}** *{3}*\n".format(tmpChip.emoji+[""," "][tmpChip.emoji != ""],tmpChip.name,[10,5,3,1][tmpChip.rarity],["({0}/{1})".format(user.chipInventory[tmpChip.id].progress,nbChipsForLvlUp[user.chipInventory[tmpChip.id].lvl-rarityMinLvl[tmpChip.rarity]]),"(↑)"][hadLvlUp],rarityEmojis[tmpChip.rarity])
				
				saveCharFile(user=user)
				jsonFile = open("./data/database/dailyShop.json","w")
				json.dump({"dailyShop":chipShopContent},jsonFile)
				jsonFile.close()
				await respond.respond(embed=Embed(title="/chip shop",color=user.color,description=reduceEmojiNames(formatShop(chipShopMsg["buyed"][random.randint(0,len(chipShopMsg["buyed"])-1)])+"\n\n"+tmpDesc+["","\n"][tmpDesc != ""]+temp)))
				user = loadCharFile(user=user)
			elif respond.component_type == ComponentType.BUTTON and respond.component.custom_id in ["buyCards","buyCoins"]:
				if hasSelected.startswith("booster_"):
					user, tmpDesc = openBooster(user=user, boosters = [chipShopContent["dailyBooster"]], infield = False)
					if respond.component.custom_id == "buyCoins":
						user.currencies -= coinCost
					else:
						user.tc -= tcCost
					chipShopContent["hasBought"][0].append(user.owner)
					
					saveCharFile(user=user)
					jsonFile = open("./data/database/dailyShop.json","w")
					json.dump({"dailyShop":chipShopContent},jsonFile)
					jsonFile.close()
					await respond.respond(embed=Embed(title="/chip shop",color=user.color,description=reduceEmojiNames(formatShop(chipShopMsg["buyed"][random.randint(0,len(chipShopMsg["buyed"])-1)])+"\n\n"+tmpDesc+["","\n"][tmpDesc != ""])))
					user = loadCharFile(user=user)
				else:
					if isOffer:
						indx = int(hasSelected.replace("offer_",""))
						tmpChip, toAppend = getChip(indx), [chipShopContent["hasBought"][2]] 
						tmpChipNb[indx] = max([10,5,3,1][tmpChip.rarity], int(nbChipsForLvlUp[user.chipInventory[tmpChip.id].lvl-rarityMinLvl[user.chipInventory[tmpChip.id].rarity]]*0.1))
					else:
						indx = int(hasSelected.replace("chip_",""))
						tmpChip, toAppend = chipsInShop[indx], [chipShopContent["hasBought"][1][indx]]
					hadLvlUp = False
					temp, user = user.chipInventory[tmpChip.id].addProgress(tmpChipNb[indx],user)

					if respond.component.custom_id == "buyCoins": user.currencies -= coinCost
					else: user.tc -= tcCost

					toAppend[0].append(user.owner)
					temp = "{4} {0}*{1}* x**{2}** *{3}*\n".format(tmpChip.emoji+[""," "][tmpChip.emoji != ""],tmpChip.name,tmpChipNb[indx],["({0}/{1})".format(user.chipInventory[tmpChip.id].progress,nbChipsForLvlUp[user.chipInventory[tmpChip.id].lvl-rarityMinLvl[tmpChip.rarity]]),"(↑)"][hadLvlUp],rarityEmojis[tmpChip.rarity])
			
					saveCharFile(user=user)
					jsonFile = open("./data/database/dailyShop.json","w")
					json.dump({"dailyShop":chipShopContent},jsonFile)
					jsonFile.close()
					await respond.respond(embed=Embed(title="/chip shop",color=user.color,description=reduceEmojiNames(formatShop(chipShopMsg["buyed"][random.randint(0,len(chipShopMsg["buyed"])-1)])+"\n\n"+temp)))
					user = loadCharFile(user=user)
				try:
					await secMsg.delete()
					secMsg = None
				except:
					pass
	except:
		try:
			await secMsg.delete()
			secMsg = None
		except:
			pass

		try:
			await respond.delete()
		except:
			pass

		try:
			await msg.suppress_embeds()
		except:
			pass
		if msg != None:
			await msg.edit(content="A unexpected error occured :\n"+format_exc(limit=4000).replace("_","\"").replace("*","\*").replace("^","\^"),components=[],embeds=[])
		else:
			await ctx.send(content="A unexpected error occured :\n"+format_exc(limit=4000).replace("_","\"").replace("*","\*").replace("^","\^"),components=[],embeds=[])