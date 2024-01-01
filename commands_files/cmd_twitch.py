
from traceback import print_exc, format_exc
from sqlite3 import Row
from constantes import *
import requests, data.bot_tokens, gestion, random, interactions, asyncio

isAllReadyStreaming = []

class stream():
	def __init__(self, title, streamer, game, thumbnail, userId, startTime=datetime.now().isoformat(), gameId=None):
		if isLenapy:
			startTime = datetime.fromisoformat(startTime.replace("Z",""))
		else:
			startTime = datetime.fromisoformat(startTime)
		self.title, self.streamer, self.game, self.thumbnail, self.userId, self.startTime, self.gameId = title, streamer, game, thumbnail, userId, startTime, gameId

def getStreamerToken():
	body = {'client_id': data.bot_tokens.twIDclient,'client_secret': data.bot_tokens.twSecret,"grant_type": 'client_credentials'}
	r = requests.post('https://id.twitch.tv/oauth2/token', body)
	keys = r.json()
	return keys['access_token']

def checkIfLive(channel):
	res = ""
	try:
		req = requests.get("https://api.twitch.tv/helix/streams?user_login=" + channel, headers={'Client-ID': data.bot_tokens.twIDclient,'Authorization': 'Bearer ' + getStreamerToken()})
		res = req.json()
		if len(res['data']) > 0: # the twitch channel is live
			return stream(res['data'][0]['title'], res['data'][0]['user_name'], res['data'][0]['game_name'], res['data'][0]['thumbnail_url'], res['data'][0]["user_id"], res['data'][0]["started_at"], res['data'][0]["game_id"])
		else:
			return False
	except:
		try:
			return "An error occured: " + format_exc() +"\n"+ res
		except:
			print("An error occured: " + format_exc())
			return "An error occured: " + format_exc()

def getStreamerAvatar(userId):
	try:
		req = requests.get("https://api.twitch.tv/helix/users?id=" + userId, headers={'Client-ID': data.bot_tokens.twIDclient,'Authorization': 'Bearer ' + getStreamerToken()})
		res = req.json()
		return res['data'][0]['profile_image_url'].format(weigth=64,length=64)
	except:
		return ""

class twitchUser():
	def __init__(self,name,login,avatar,id):
		self.name, self.login, self.avatar, self.id = name, login, avatar, id

def getStreamerUser(userlogin):
	try:
		req = requests.get("https://api.twitch.tv/helix/users?login=" + userlogin, headers={'Client-ID': data.bot_tokens.twIDclient,'Authorization': 'Bearer ' + getStreamerToken()})		
		res = req.json() 
		return twitchUser(res['data'][0]['display_name'],res['data'][0]['login'],res['data'][0]['profile_image_url'],res['data'][0]["id"])
	except Exception as e:
		return None

def getAlertEmbed(streamData:stream,streamEmb:gestion.streamEmbed) -> Embed:
	emb: interactions.Embed = interactions.Embed(title=streamEmb.embedTitle,description=streamEmb.embedDesc,color=streamEmb.embedColor)
	if streamEmb.showImage:
		tablImage = []
		for img in [streamEmb.image0,streamEmb.image1,streamEmb.image2]:
			if img != None:
				tablImage.append(img)
		
		if len(tablImage) > 1:
			img = tablImage[random.randint(0,len(tablImage)-1)]
		elif len(tablImage) == 1:
			img = tablImage[0]
		else:
			img = streamData.thumbnail.format(width=500,height=280)
		emb.set_image(url=img)
	
	try:
		gameIcon = "https://cdn.discordapp.com/emojis/1183137476571840532.webp?size=96&quality=lossless"
		if streamData.gameId!=None:
			gameIcon = requests.get("https://api.twitch.tv/helix/games?id=" + streamData.gameId, headers={'Client-ID': data.bot_tokens.twIDclient,'Authorization': 'Bearer ' + getStreamerToken()})
			gameIcon = gameIcon.json()
			if len(gameIcon["data"])>0:
				gameIcon: str = gameIcon["data"][0]["box_art_url"].format(width=256,height=256)
		emb.set_thumbnail(url=gameIcon)
	except KeyError:
		pass
	except:
		print_exc()
	emb.set_author(name=streamData.streamer,icon_url=getStreamerAvatar(streamData.userId))
	return emb

def checkingStreaming(alert,bot):
	potStreamEmb, toReturn = checkIfLive(alert["streamerName"].lower()), []
	if type(potStreamEmb) == stream and alert["streamerName"] not in isAllReadyStreaming:
		isAllReadyStreaming.append(alert["streamerName"])
		if isLenapy:
			timeSteam = datetime.now() - potStreamEmb.startTime - timedelta(hours=1)
		else:
			timeSteam = datetime.now(parisTimeZone) - potStreamEmb.startTime
		timeSteam = int(timeSteam.total_seconds())
		timeHour, timeMinute, timeSeconds = timeSteam//3600, (timeSteam%3600)//60, timeSteam%3600%60
		print("Found a steam for {0}, started {1} seconds ago ({2}:{3}:{4})".format(potStreamEmb.streamer,timeSteam,timeHour,timeMinute,timeSeconds))
		if timeSteam <= 60:
			for nowStreaming in gestion.globalVar.getStreamAlertList():
				if nowStreaming["streamerName"] == alert["streamerName"].lower():
					twEmbed = gestion.globalVar.getStreamAlertEmbed(int(nowStreaming["guild"]), nowStreaming["streamerName"])
					twEmbed.guild = bot.get_guild(twEmbed.guild)
					twEmbed.notifRole = twEmbed.guild.get_role(twEmbed.notifRole)
					twEmbed.notifChannel: interactions.GuildText = twEmbed.guild.get_channel(twEmbed.notifChannel)

					def formatTwitchTxt(txt,twitchEmb:gestion.streamEmbed,stream:stream):
						return txt.format(
							notifRole = twEmbed.notifRole.mention,
							streamerName = stream.streamer,
							streamTitle = stream.title,
							gameName = stream.game,
							hyperlink = twitchEmb.hyperlink
							)

					twEmbed.notifMsg = formatTwitchTxt(twEmbed.notifMsg,twEmbed,potStreamEmb)
					twEmbed.embedTitle = formatTwitchTxt(twEmbed.embedTitle,twEmbed,potStreamEmb)
					twEmbed.embedDesc = formatTwitchTxt(twEmbed.embedDesc,twEmbed,potStreamEmb)

					toReturn.append([True,twEmbed.notifChannel,twEmbed.notifMsg, getAlertEmbed(streamData=potStreamEmb,streamEmb=twEmbed)])

	elif not(potStreamEmb) and alert["streamerName"] in isAllReadyStreaming:
		try:
			isAllReadyStreaming.remove(alert["streamerName"])
			print("{0} had finish their stream".format(alert["streamerName"]))
		except:
			print_exc()

	return toReturn

async def verifStreamingStreamers2(bot:interactions.Client, alert:Row):
	resulty = checkingStreaming(alert,bot)
	if len(resulty) > 0:
		for result in resulty:
			if result[0]:
				try:
					msg: Message = await result[1].send(content=result[2],embeds=result[3])
					print("> Send {0}'s annonce in {1} ({2})".format(alert["streamerName"],result[1].name, result[1].guild.name))
					try:
						if result[1].type == ChannelType.GUILD_NEWS:
							await msg.publish()
							print("> Publish Done")
					except:
						print_exc()
				except:
					print_exc()

async def verifStreamingStreamers(bot:interactions.Client):
	listallAlertes: List[Row] = gestion.globalVar.getStreamAlertList()
	listStreamersNames = []
	for alert in listallAlertes:
		if alert["streamerName"] not in listStreamersNames:
			asyncio.create_task(verifStreamingStreamers2(bot, alert))
			listStreamersNames.append(alert["streamerName"])
			await asyncio.sleep(0.1)


addAlertButton = interactions.Button(style=ButtonStyle.SUCCESS, label="Ajouter une alerte",emoji=PartialEmoji(name="➕"),custom_id="add")
confirmButton = interactions.Button(style=ButtonStyle.SUCCESS, label="Confirmer",emoji=PartialEmoji(name="✅"),custom_id="confirm")
rejectButton = interactions.Button(style=2, label="Refuser",emoji=PartialEmoji(name="❌"),custom_id="reject")
deleteButton = interactions.Button(style=ButtonStyle.DANGER, label="Supprimer l'alerte",emoji=PartialEmoji(name="🗑️"),custom_id="delete")
exempleButton = interactions.Button(style=ButtonStyle.SECONDARY, label="Essai dans ce salon",emoji=PartialEmoji(name="🔬"),custom_id="try")
cancelButton = interactions.Button(style=ButtonStyle.SECONDARY, label="Retour",emoji=PartialEmoji(name="◀️"),custom_id="goback")

tablSelectEmbed = [
	["Messsage de noctification","Le message qui s'affiche lors d'une alerte.\nLes mentions de rôles ne fonctionnent dans ce message"],
	["Titre de l'embed","Le titre de l'embed."],
	["Description de l'embed","Le message qui s'affichera en dessous du titre\nLes liens hypertextes ne fonctionnent que dans cette description"],
	["Couleur de l'embed","La couleur de l'embed"],
	["Texte du lien hypertexte","Le texte du lien. Cliquer dessus enveras les utilisateurs vers la chaîne de l'alerte"],
	["Image 1","Une image pouvant être affichée dans l'alerte.\nSi aucune image est paramétrée, la miniature du stream est utilisée à la place\nSi plusieurs images sont paramétrées, une sera sélectionnée au hasard"],
	["Image 2","Voir Image 1"],
	["Image 3","Voir Image 1"],
	["Afficher l'image ?","Permet d'afficher ou non l'une des images paramétrées ou la miniature du stream sur l'alerte"]
]

async def streamSettingsFunction(bot:interactions.Client,guild:interactions.Guild,ctx:interactions.SlashContext):
	user, msg = ctx.author, None
	userPerms = ctx.channel.permissions_for(user)

	if not(userPerms.MANAGE_CHANNELS):
		await ctx.send(content="Cette commande ne peut être utilisée uniquement par des membres pouvant gérer les salons de ce serveur",ephemeral=True)
		return 0

	await ctx.defer()
	while 1:
		desc, listOption = "", []
		guildAlerteList = gestion.globalVar.getStreamAlterPerGuild(guild.id)

		if len(guildAlerteList) == 0:
			desc = "Aucune alerte est paramétré pour ce serveur"
		else:
			if msg == None:
				msg = await ctx.send(embeds=Embed("Chargement des alertes..."))
			else:
				await msg.edit(embeds=Embed("Chargement des alertes..."),components=[])
			roles, channels = guild.roles, guild.channels
			desc = "__Liste des alertes :__"
			for alerte in guildAlerteList:
				chan, role = None, None
				user = getStreamerUser(alerte.streamerName)

				for roly in roles:
					if roly.id == alerte.notifRole:
						role = roly
						break
				for channy in channels:
					if channy.id == alerte.notifChannel:
						chan = channy
						break
				
				if user != None:
					userName = user.name
					userLogin = user.login
				else:
					userName = userLogin = "???"
				if role != None:
					role = role.mention
				else:
					role = "???"
				if chan != None:
					chan = chan.mention
				else:
					chan = "???"
				desc += "\n{0} ({1}) | {2} | {3}".format(userName,userLogin,chan,role)
				listOption.append(interactions.StringSelectOption(label=userName,value=userLogin))
			
		emb = interactions.Embed(title="__Alertes Twitch ({0})__".format(guild.name),color=light_blue,description=desc)
		
		comp = []
		if len(guildAlerteList) < 10:
			comp = comp + [interactions.ActionRow(addAlertButton)]

		if len(listOption) > 0:
			comp = comp + [interactions.ActionRow(interactions.StringSelectMenu(listOption,custom_id = "listAlert",placeholder="Modifier / Supprimer une alerte"))]
		
		if msg == None:
			try:
				msg = await ctx.send(embeds=emb,components=comp)
			except:
				msg = await ctx.channel.send(embeds=emb,components=comp)
		else:
			await msg.edit(embeds=emb,components=comp)

		def check(m):
			m = m.ctx
			return m.author.id == ctx.author.id

		try:
			rep = await bot.wait_for_component(msg,check=check,timeout=360)
			rep: ComponentContext = rep.ctx
			await rep.defer()
		except asyncio.TimeoutError:
			await msg.edit(embeds=emb,components=[])
			return 0

		if rep.component_type == 2:
			await msg.edit(embeds=emb,components=[])
			newAlert, paramMsg = gestion.streamEmbed(guild.id), None

			def check2(m):
				m = m.message
				return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

			while 1:
				paramEmb = interactions.Embed(title="__Nouvelle alerte__",color=light_blue,description="Veuillez renseigner le nom d'utilisateur ou le liens vers la chaîne twitch à cibler.\n\n__Exemples :__\nalicekohisu\nhttps://www.twitch.tv/alicekohisu")
				if paramMsg == None:
					paramMsg = await rep.send(embeds=paramEmb)
				else:
					await paramMsg.edit(embeds=paramEmb,components=[])

				try:
					paramRep = await bot.wait_for("on_message_create",checks=check2,timeout=360)
					paramRep: Message = paramRep.message
				except asyncio.TimeoutError:
					await paramMsg.delete()
					return 1

				await paramRep.add_reaction(gestion.getEmojiObject(emLoading))
				twUser = getStreamerUser(paramRep.content.replace("https://www.twitch.tv/",""))
				if twUser != None:
					if "https://www.twitch.tv/" not in paramRep.content:
						await paramRep.add_reaction(gestion.getEmojiObject(emLoading))
						paramEmb = interactions.Embed(title="__Nouvelle alerte__",color=light_blue,description="Cette chaîne est-elle bien votre chaîne ciblée ?\n{0} ({1})".format(twUser.name,twUser.login))
						paramEmb.set_thumbnail(url=twUser.avatar)
						await paramRep.remove_reaction(gestion.getEmojiObject(emLoading))
						confirmMsg = await paramRep.channel.send(embeds=paramEmb,components=[interactions.ActionRow(confirmButton,rejectButton)])
						try:
							confirmRep = await bot.wait_for_component(confirmMsg,check=check,timeout=60)
							confirmRep: ComponentContext = confirmRep.ctx
						except asyncio.TimeoutError:
							await paramMsg.delete()
							return 1
					
						if confirmRep.custom_id == confirmButton.custom_id:
							newAlert.streamerName = paramRep.content.replace("https://www.twitch.tv/","")
							await confirmMsg.edit(content=" ✅Cette alerte portera sur la chaîne de {0}".format(twUser.name),components=[],embeds=[])
							await asyncio.sleep(3)
							await confirmMsg.delete()
							try:
								await paramRep.delete()
							except:
								pass
							break
					else:
						newAlert.streamerName = paramRep.content.replace("https://www.twitch.tv/","")
						await paramRep.remove_reaction(gestion.getEmojiObject(emLoading))
						tempMsg = await paramRep.channel.send(content="✅ Cette alerte portera sur la chaîne de {0}".format(twUser.name),components=[])
						await asyncio.sleep(3)
						await tempMsg.delete()
						try:
							await paramRep.delete()
						except:
							pass
						break

				else:
					await paramRep.add_reaction(emoji=PartialEmoji(name="❌"))
					await paramRep.channel.send(content="❌ Aucune chaîne n'a été trouvée.\nVérifiez bien que vous entrez le nom d'utilisateur et non le nom de chaîne (les nom d'utilisateurs sont toujours en minuscules) ou envoyez directement le lien de votre chaîne ciblée")

			while 1:
				paramEmb = interactions.Embed(title="__Nouvelle alerte__",color=light_blue,description="__Chaîne :__ {0}\n\nVeuillez mentionner le role qui sera notifié lors qu'une alerte sera envoyé.".format(twUser.name))
				await paramMsg.edit(embeds=paramEmb,components=[])
				try:
					paramRep = await bot.wait_for("on_message_create",checks=check2,timeout=60)
					paramRep: Message = paramRep.message
				except asyncio.TimeoutError:
					await paramMsg.delete()
					return 1

				listRoleMentions = paramRep._mention_roles
				if listRoleMentions!=None:
					newAlert.notifRole = ctx.guild.get_role(listRoleMentions[0])

					tempMsg = await paramRep.channel.send(content="✅ Le role **{0}** sera désormais notifié lors des alertes".format(newAlert.notifRole.name),components=[])
					await asyncio.sleep(3)
					await tempMsg.delete()
					try:
						await paramRep.delete()
					except:
						pass
					break
				else:
					await paramRep.remove_reaction(gestion.getEmojiObject(emLoading))
					await paramRep.add_reaction(PartialEmoji(name="❌"))
					await paramRep.channel.send(content="❌ Vous n'avez mentionné aucun rôle",delete_after=3)

			while 1:
				paramEmb = interactions.Embed(title="__Nouvelle alerte__",color=light_blue,description="__Chaîne :__ {0}\n__Rôle :__ {1}\n\nVeuillez mentionner le salon où seront envoyés les alertes.".format(twUser.name,newAlert.notifRole.mention))
				await paramMsg.edit(embeds=paramEmb,components=[])
				try:
					paramRep = await bot.wait_for("on_message_create",checks=check2,timeout=60)
					paramRep: Message = paramRep.message
				except asyncio.TimeoutError:
					await paramMsg.delete()
					return 1

				listChannelMentions = paramRep.mention_channels
				if len(listChannelMentions) > 0:
					newAlert.notifChannel: TYPE_MESSAGEABLE_CHANNEL = listChannelMentions[0]

					tempMsg = await paramRep.channel.send(content="✅ Les futures alertes seront envoyées dans le salon **{0}**".format(newAlert.notifChannel.name),components=[])
					await asyncio.sleep(3)
					await tempMsg.delete()
					try:
						await paramRep.delete()
					except:
						pass
					break
				else:
					await paramRep.remove_reaction(gestion.getEmojiObject(emLoading))
					await paramRep.add_reaction(PartialEmoji(name="❌"))
					await paramRep.channel.send(content="❌ Vous n'avez mentionné aucun salon",delete_after=3)

			try:
				gestion.globalVar.updateStreamEmbed(newAlert)
				await paramMsg.edit(embeds=interactions.Embed(title="__Nouvelle alerte enregistrée__",color=green,description="✅ Votre nouvelle alerte a été enregistrée avec succès"),components=[])
			except Exception as e :
				print_exc()
				await paramMsg.edit(embeds=interactions.Embed(title="__Erreur lors de l'enregistrement de l'alerte__",color=red,description="Une erreur est survenue lors de l'enregistrement de l'alerte :\n{0}".format(e)),components=[])

		else:
			try:
				newMsg = await rep.send(content="Chargement des paramètres de l'alerte <a:loading:862459118912667678>...",components=[])
			except:
				newMsg = await rep.channel.send(content="Chargement des paramètres de l'alerte <a:loading:862459118912667678>...",components=[])
			user = getStreamerUser(rep.values[0])
			while 1:
				selectAlert = gestion.globalVar.getStreamAlertEmbed(guild.id,rep.values[0])
				tablSettings = [selectAlert.notifMsg,selectAlert.embedTitle,selectAlert.embedDesc, selectAlert.embedColor, selectAlert.hyperlinkTxt, [selectAlert.image0,"-"][selectAlert.image0 == None], [selectAlert.image1,"-"][selectAlert.image1 == None], [selectAlert.image2,"-"][selectAlert.image2 == None]]
				tablSettings2 = [bool(selectAlert.showImage)]
				allTabl = tablSettings+tablSettings2
				desc, tablOption = "__Paramètres de l'alerte :__\n",[]
				for cmpt in range(len(allTabl)):
					desc += "\n__**{0}** :__\n{1}\n*> {2}*".format(tablSelectEmbed[cmpt][0],allTabl[cmpt],tablSelectEmbed[cmpt][1].replace("\n","\n> "))
					tablOption.append(interactions.StringSelectOption(label=tablSelectEmbed[cmpt][0],value=str(cmpt),description=tablSelectEmbed[cmpt][1].splitlines()[0]))

				mainEmb = interactions.Embed(title="__Alerte de stream ({0} - {1})__".format(guild.name,user.name),color=light_blue,description=desc)
				mainEmb.set_thumbnail(url=user.avatar)

				comp = [
						interactions.ActionRow(interactions.StringSelectMenu(tablOption,custom_id = "selectSomethingToModify",placeholder="Sélectionnez une catégorie à modifier")),
						interactions.ActionRow(exempleButton,deleteButton)
					]
				
				await newMsg.edit(content="",embeds=mainEmb,components=comp)
				try:
					customRep = await bot.wait_for_component(messages=newMsg,components=comp,check=check,timeout=180)
					customRep: ComponentContext = customRep.ctx
					await customRep.defer()
				except asyncio.TimeoutError:
					await newMsg.delete()
					return 1
					
				if customRep.component_type == 2:
					if customRep.custom_id == exempleButton.custom_id:
						try:
							tempMsg = await customRep.send(content="Génération de la fausse alerte <a:loading:862459118912667678>...",components=[])
						except:
							tempMsg = await customRep.channel.send(content="Génération de la fausse alerte <a:loading:862459118912667678>...",components=[])
						for roly in guild.roles:
							if roly.id == selectAlert.notifRole:
								selectAlert.notifRole = roly
								break

						selectAlert.notifChannel = ctx.channel

						def formatTwitchTxt(txt,twitchEmb:gestion.streamEmbed,stream:stream):
							return txt.format(
								notifRole = "["+selectAlert.notifRole.name+"]",
								streamerName = stream.streamer,
								streamTitle = stream.title,
								gameName = stream.game,
								hyperlink = twitchEmb.hyperlink
								)

						fakeStream = stream("Lenapy Title",user.name,"Lenapy Game","https://cdn.discordapp.com/attachments/927195778517184534/1155148054693953556/Sans_titre_120_20230923162521.png?width={width}&height={height}",user.id)
						selectAlert.notifMsg = formatTwitchTxt(selectAlert.notifMsg,selectAlert,fakeStream)
						selectAlert.embedTitle = formatTwitchTxt(selectAlert.embedTitle,selectAlert,fakeStream)
						selectAlert.embedDesc = formatTwitchTxt(selectAlert.embedDesc,selectAlert,fakeStream)

						emb = getAlertEmbed(streamData=fakeStream,streamEmb=selectAlert)
						try:
							await tempMsg.edit(content=selectAlert.notifMsg,embeds=getAlertEmbed(streamData=fakeStream,streamEmb=selectAlert))
						except Exception as e:
							await tempMsg.edit(content="Une erreur est survenue durant le test : {0}".format(e))
							print(emb.author.icon_url)
					elif customRep.custom_id == deleteButton.custom_id:
						comp = [interactions.ActionRow(cancelButton,deleteButton)]
						try:
							deleteMsg = await customRep.send(content="",embeds=interactions.Embed(title="__Supprimer cette alerte ?__",color=red,description="Si vous voudrez la réactiver il faudra tout recommencer !"),components=comp)
						except:
							deleteMsg = await customRep.channel.send(content="",embeds=interactions.Embed(title="__Supprimer cette alerte ?__",color=red,description="Si vous voudrez la réactiver il faudra tout recommencer !"),components=comp)

						try:
							deleteRep = await bot.wait_for_component(deleteMsg,comp,check,60)
							deleteRep: ComponentContext = deleteRep.ctx
						except asyncio.TimeoutError:
							await newMsg.delete()
							await deleteMsg.delete()
							return 1

						if deleteRep.custom_id == deleteButton.custom_id:
							try:
								gestion.globalVar.removeAlert(guild.id,selectAlert.streamerName)
								tempMsg = await deleteRep.send("🗑️ L'alerte à bien été supprimée")
								await asyncio.sleep(3)
								await tempMsg.delete()
								await deleteMsg.delete()
								await newMsg.delete()
								break
							except Exception as e:
								tempMsg = await deleteRep.send("❌ Une erreur est survenue durant la procédure :\n{0}".format(e))
								await asyncio.sleep(3)
								await tempMsg.delete()
								await deleteMsg.delete()
								await newMsg.delete()
								break
				else:
					def check2(m):
						m = m.message
						return m.author.id == int(ctx.author.id) and m.channel.id == ctx.channel.id
					customRep.values[0] = int(customRep.values[0])
					if customRep.values[0] in [0,1,2,4]:
						desc = ["Veillez écrire le nouveau message.\nVous pouvez rajouter des balises de formatage pour dynamiser un peu votre annonce !\n\n__{streamerName}__ : Nom du streamer\n__{streamTitle}__ : Titre du stream\n__{gameName}__ : Nom du jeu\n__{hyperlink}__ : Lien vers le stream\n> Ne fonctionne que dans la description de l'embed\n__{notifRole}__ : Mentionne le role\n> Ne fonctionne que dans le message d'annonce\n\nEntrez \"Retour\" pour annuler","Veuillez entrer le nouveau texte du lien.\n\nEntrez \"Retour\" pour annuler"][customRep.values[0] == 4]
						editMsg = await customRep.send(embeds=interactions.Embed(title="__Personnalisation de l'alerte__",color=light_blue,description=desc))
						
						try:
							editRep = await bot.wait_for("on_message_create",checks=check2,timeout=60)
							editRep: Message = editRep.message
							await editRep.add_reaction(gestion.getEmojiObject(emLoading))
						except asyncio.TimeoutError:
							await newMsg.delete()
							await editMsg.delete()
							return 1

						if editRep.content == "Retour":
							await editMsg.delete()
							try:
								await editRep.delete()
							except:
								pass
						else:
							if customRep.values[0] == 0:
								selectAlert.notifMsg = editRep.content
							elif customRep.values[0] == 1:
								selectAlert.embedTitle = editRep.content 
							elif customRep.values[0] == 2:
								selectAlert.embedDesc = editRep.content
							elif customRep.values[0] == 4:
								selectAlert.hyperlinkTxt = editRep.content

							gestion.globalVar.updateStreamEmbed(selectAlert)
							try:
								await editRep.clear_all_reactions()
							except:
								pass
							await editRep.reply(ephemeral=True,content="✅ Votre modification a bien été prise en compte",delete_after=3)
							try:
								await editRep.delete()
							except:
								pass
							await editMsg.delete()
					elif customRep.values[0] == 3:
						colorMsg = await customRep.send(embeds = interactions.Embed(title="__Couleur de l'embed__",description="Veillez entrer le code hexadecimal de votre nouvelle couleur :\n\nExemples :\n94d4e4\n#94d4e4",color = light_blue))
						while 1:
							try:
								respond = await bot.wait_for("on_message_create",checks=check2,timeout=60)
								respond: Message = respond.message
							except asyncio.TimeoutError:
								await newMsg.delete()
								await colorMsg.delete()
								return 1

							if respond.content == "Retour":
								await colorMsg.delete()
								try:
									await respond.delete()
								except:
									pass
								break
							else:
								tempColor = respond.content
								color = int(respond.content,16)

								if color == None:
									await respond.add_reaction(PartialEmoji(name='❌'))
									await colorMsg.channel.send(content="Le code donné n'est pas un code hexadecimal valide")
								else:
									break
						if not(respond.content == "Retour"):
							comp = [interactions.ActionRow(confirmButton,rejectButton)]
							await colorMsg.edit(embeds = interactions.Embed(title = "Couleur personnalisée",description="Est-ce que cette couleur vous va ?",color = color),components=comp)
							try:
								react = await bot.wait_for_component(colorMsg,comp,check,timeout=60)
								react: ComponentContext = react.ctx
							except asyncio.TimeoutError:
								await newMsg.delete()
								await colorMsg.delete()
								return 1

							if react.custom_id == confirmButton.custom_id:
								selectAlert.color = color
								gestion.globalVar.updateStreamEmbed(selectAlert)
								await colorMsg.delete()
					elif customRep.values[0] in [5,6,7]:
						desc = "Veillez entrer l'URL de votre image\nEntrez \"None\" pour supprimer l'image actuelle.\nEntrez \"Retour\" pour annuler\nNote : Une image peut ne pas s'afficher si l'url ne correspond pas à une image"
						editMsg = await customRep.send(embeds=interactions.Embed(title="__Personnalisation de l'alerte__",color=light_blue,description=desc))

						try:
							editRep = await bot.wait_for("on_message_create",checks=check2,timeout=60)
							editRep: Message = editRep.message
							await editRep.add_reaction(emoji=gestion.getEmojiObject(emLoading))
						except asyncio.TimeoutError:
							await newMsg.delete()
							await editMsg.delete()
							return 1

						if editRep.content == "Retour":
							await editMsg.delete()
							try:
								await editRep.delete()
							except:
								pass
						else:
							if editRep.content == "None":
								editRep.content = None
							
							if customRep.values[0] == 5:
								selectAlert.image0 = editRep.content
							elif customRep.values[0] == 6:
								selectAlert.image1 = editRep.content 
							else:
								selectAlert.image2 = editRep.content

							gestion.globalVar.updateStreamEmbed(selectAlert)
							try:
								await editRep.clear_all_reactions()
							except:
								pass
							await editRep.add_reaction(PartialEmoji(name='✅'))
							await editMsg.delete()
					else:
						comp = [interactions.ActionRow(interactions.StringSelectMenu([interactions.StringSelectOption(label="Afficher",value="1"),interactions.StringSelectOption(label="Cacher",value="0")],custom_id = "listOptionsiGuess"))]
						editMsg = await customRep.send(embeds=interactions.Embed(title="__Personnalisation de l'alerte__",color=light_blue,description="Voulez-vous afficher ou cacher les images ?"),components=comp)
						try:
							editRep = await bot.wait_for_component(editMsg,comp,check,60)
							editRep: ComponentContext = editRep.ctx
						except asyncio.TimeoutError:
							await newMsg.delete()
							await editMsg.delete()
							return 1

						selectAlert.showImage = bool(int(editRep.values[0]))
						gestion.globalVar.updateStreamEmbed(selectAlert)
						await editMsg.delete()