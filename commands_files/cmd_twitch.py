from asyncio import selector_events
from shutil import ExecError
from traceback import print_exc
import discord, requests, data.bot_tokens, gestion, random
from discord_slash.utils.manage_components import create_actionrow, create_select, create_select_option, create_button, ButtonStyle
from discord_slash.context import SlashContext
from discord_slash.utils.manage_components import *
from constantes import light_blue, red, green
import asyncio

isAllReadyStreaming = []

class stream():
    def __init__(self, title, streamer, game, thumbnail, userId):
        self.title, self.streamer, self.game, self.thumbnail, self.userId = title, streamer, game, thumbnail, userId

def getStreamerToken():
    body = {'client_id': data.bot_tokens.twIDclient,'client_secret': data.bot_tokens.twSecret,"grant_type": 'client_credentials'}
    r = requests.post('https://id.twitch.tv/oauth2/token', body)
    keys = r.json()
    return keys['access_token']

def checkIfLive(channel):
    try:
        req = requests.get("https://api.twitch.tv/helix/streams?user_login=" + channel, headers={'Client-ID': data.bot_tokens.twIDclient,'Authorization': 'Bearer ' + getStreamerToken()})        
        res = req.json() 
        if len(res['data']) > 0: # the twitch channel is live
            data2 = res['data'][0]
            title = data2['title']
            streamer = data2['user_name']
            game = data2['game_name']
            thumbnail_url = data2['thumbnail_url']
            streamerId = data2["user_id"]
            return stream(title, streamer, game, thumbnail_url, streamerId)
        else:
            return False
    except Exception as e:
        return "An error occured: " + str(e)

def getStreamerAvatar(userId):
    try:
        req = requests.get("https://api.twitch.tv/helix/users?id=" + userId, headers={'Client-ID': data.bot_tokens.twIDclient,'Authorization': 'Bearer ' + getStreamerToken()})        
        res = req.json() 
        return res['data'][0]['profile_image_url']
    except Exception as e:
        return "An error occured: " + str(e)

class twitchUser():
	def __init__(self,name,login,avatar):
		self.name, self.login, self.avatar = name, login, avatar

def getStreamerUser(userlogin):
    try:
        req = requests.get("https://api.twitch.tv/helix/users?login=" + userlogin, headers={'Client-ID': data.bot_tokens.twIDclient,'Authorization': 'Bearer ' + getStreamerToken()})        
        res = req.json() 
        return twitchUser(res['data'][0]['display_name'],res['data'][0]['login'],res['data'][0]['profile_image_url'])
    except Exception as e:
        print(e)
        return None

async def verifStreamingStreamers(bot:discord.Client):
    listallAlertes = gestion.globalVar.getStreamAlertList()
    for alert in listallAlertes:
        potStreamEmb = checkIfLive(alert["streamerName"].lower())
        if type(potStreamEmb) == stream and alert["streamerName"] not in isAllReadyStreaming:
            isAllReadyStreaming.append(alert["streamerName"])
            for nowStreaming in listallAlertes:
                if nowStreaming["streamerName"] == alert["streamerName"].lower():
                    twEmbed = gestion.globalVar.getStreamAlertEmbed(nowStreaming["guild"], nowStreaming["streamerName"])
                    twEmbed.guild = await bot.fetch_guild(twEmbed.guild)
                    roles, channels = await twEmbed.guild.fetch_roles(), await twEmbed.guild.fetch_channels()
                    for roly in roles:
                        if roly.id == twEmbed.notifRole:
                            twEmbed.notifRole = roly
                            break
                    for channy in channels:
                        if channy.id == twEmbed.notifChannel:
                            twEmbed.notifChannel = channy
                            break

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

                    emb = discord.Embed(title=twEmbed.embedTitle,description=twEmbed.embedDesc,color=twEmbed.embedColor)
                    if twEmbed.showImage:
                        tablImage = []
                        for img in [twEmbed.image0,twEmbed.image1,twEmbed.image2]:
                            if img != None:
                                tablImage.append(img)
                        
                        if len(tablImage) > 1:
                            img = tablImage[random.randint(0,len(tablImage)-1)]
                        elif len(tablImage) == 1:
                            img = tablImage[0]
                        else:
                            img = potStreamEmb.thumbnail.format(width=500,height=280)
                        emb.set_image(url=img)
                    emb.set_thumbnail(url=getStreamerAvatar(potStreamEmb.userId))
                    emb.set_footer(icon_url=getStreamerAvatar(potStreamEmb.userId),text=potStreamEmb.streamer)

                    try:
                        await twEmbed.notifChannel.send(content=twEmbed.notifMsg,embed=emb)
                    except:
                        print_exc()
        elif not(potStreamEmb) and alert["streamerName"] in isAllReadyStreaming:
            try:
                isAllReadyStreaming.remove(alert["streamerName"])
            except:
                print_exc()

addAlertButton = create_button(ButtonStyle.green,"Ajouter une alerte","➕","add")
confirmButton = create_button(ButtonStyle.green,"Confirmer","✅","confirm")
rejectButton = create_button(ButtonStyle.grey,"Refuser","❌","reject")
deleteButton = create_button(ButtonStyle.red,"Supprimer l'alerte","🗑️","delete")
exempleButton = create_button(ButtonStyle.gray,"Essai (dans ce salon)","🔬","try")
cancelButton = create_button(ButtonStyle.gray,"Retour","◀️","goback")

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

async def streamSettingsFunction(bot:discord.Client,guild:discord.Guild,ctx:SlashContext):
	user, msg = ctx.author, None
	userPerms = ctx.channel.permissions_for(user)

	if not(userPerms.manage_channels):
		await ctx.send(content="Cette commande ne peut être utilisée uniquement par des membres pouvant gérer les salons de ce serveur",hidden=True)
		return 0

	while 1:
		desc, listOption = "", []
		guildAlerteList = gestion.globalVar.getStreamAlterPerGuild(guild.id)

		if len(guildAlerteList) == 0:
			desc = "Aucune alerte est paramétré pour ce serveur"
		else:
			if msg == None:
				try:
					msg = await ctx.send(content="Chargement des alertes...")
				except:
					msg = await ctx.channel.send(content="Chargement des alertes...")
			else:
				await msg.edit(content="Chargement des alertes...",components=[])
			roles, channels = await guild.fetch_roles(), await guild.fetch_channels()
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
				listOption.append(create_select_option(userName,userLogin))
			
		emb = discord.Embed(title="__Alertes Twitch ({0})__".format(guild.name),color=light_blue,description=desc)
		
		comp = []
		if len(guildAlerteList) < 10:
			comp = comp + [create_actionrow(addAlertButton)]

		if len(listOption) > 0:
			comp = comp + [create_actionrow(create_select(listOption,placeholder="Modifier / Supprimer une alerte"))]
		
		if msg == None:
			try:
				msg = await ctx.send(embed=emb,components=comp)
			except:
				msg = await ctx.channel.send(embed=emb,components=comp)
		else:
			await msg.edit(content="",embed=emb,components=comp)

		def check(m):
			return m.author_id == ctx.author_id

		try:
			rep = await wait_for_component(bot,msg,check=check,timeout=360)
		except asyncio.TimeoutError:
			await msg.edit(content="",embed=emb,components=[])
			return 1

		if rep.component_type == ComponentType.button:
			await msg.edit(content="",embed=emb,components=[])
			newAlert, paramMsg = gestion.streamEmbed(guild.id), None

			def check2(m):
				return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

			while 1:
				paramEmb = discord.Embed(title="__Nouvelle alerte__",color=light_blue,description="Veuillez renseigner le nom d'utilisateur ou le liens vers la chaîne twitch à cibler.\n\n__Exemples :__\naliceko\nhttps://www.twitch.tv/aliceko")
				if paramMsg == None:
					paramMsg = await rep.send(embed=paramEmb)
				else:
					await paramMsg.edit(embed=paramEmb,components=[])

				try:
					paramRep = await bot.wait_for(event='message',check=check2,timeout=360)
				except asyncio.TimeoutError:
					await paramMsg.delete()
					return 1

				twUser = getStreamerUser(paramRep.content.replace("https://www.twitch.tv/",""))
				if twUser != None:
					print(paramRep.content,"https://www.twitch.tv/","https://www.twitch.tv/" not in paramRep.content)
					if "https://www.twitch.tv/" not in paramRep.content:
						paramEmb = discord.Embed(title="__Nouvelle alerte__",color=light_blue,description="Cette chaîne est-elle bien votre chaîne ciblée ?\n{0} ({1})".format(twUser.name,twUser.login))
						paramEmb.set_thumbnail(url=twUser.avatar)

						confirmMsg = await paramRep.channel.send(embed=paramEmb,components=[create_actionrow(confirmButton,rejectButton)])
						try:
							confirmRep = await wait_for_component(bot,confirmMsg,check=check,timeout=60)
						except asyncio.TimeoutError:
							await paramMsg.delete()
							return 1
					
						if confirmRep.custom_id == confirmButton["custom_id"]:
							newAlert.streamerName = paramRep.content.replace("https://www.twitch.tv/","")
							await confirmMsg.edit(content=" ✅Cette alerte portera sur la chaîne de {0}".format(twUser.name),components=[])
							await asyncio.sleep(3)
							await confirmMsg.delete()
							try:
								await paramRep.delete()
							except:
								pass
							break
					else:
						newAlert.streamerName = paramRep.content.replace("https://www.twitch.tv/","")
						tempMsg = await paramRep.channel.send(content="✅ Cette alerte portera sur la chaîne de {0}".format(twUser.name),components=[])
						await asyncio.sleep(3)
						await tempMsg.delete()
						try:
							await paramRep.delete()
						except:
							pass
						break

				else:
					await paramRep.add_reaction("❌")
					await paramRep.channel.send(content="❌ Aucune chaîne n'a été trouvée.\nVérifiez bien que vous entrez le nom d'utilisateur et non le nom de chaîne (les nom d'utilisateurs sont toujours en minuscules) ou envoyez directement le lien de votre chaîne ciblée",delete_after=5)

			while 1:
				paramEmb = discord.Embed(title="__Nouvelle alerte__",color=light_blue,description="__Chaîne :__ {0}\n\nVeuillez mentionner le role qui sera notifié lors qu'une alerte sera envoyé.".format(twUser.name))
				await paramMsg.edit(embed=paramEmb,components=[])
				try:
					paramRep = await bot.wait_for(event='message',check=check2,timeout=60)
				except asyncio.TimeoutError:
					await paramMsg.delete()
					return 1

				listChannelMentions = paramRep.role_mentions
				if len(listChannelMentions) > 0:
					newRole = listChannelMentions[0]
					newAlert.notifRole = newRole.id

					tempMsg = await paramRep.channel.send(content="✅ Le role **{0}** sera désormais notifié lors des alertes".format(newRole.name),components=[])
					await asyncio.sleep(3)
					await tempMsg.delete()
					try:
						await paramRep.delete()
					except:
						pass
					break
				else:
					await paramRep.add_reaction("❌")
					await paramRep.channel.send(content="❌ Vous n'avez mentionné aucun rôle",delete_after=5)

			while 1:
				paramEmb = discord.Embed(title="__Nouvelle alerte__",color=light_blue,description="__Chaîne :__ {0}\n__Rôle :__ {1}\n\nVeuillez mentionner le salon où seront envoyés les alertes.".format(twUser.name,newRole.mention))
				await paramMsg.edit(embed=paramEmb,components=[])
				try:
					paramRep = await bot.wait_for(event='message',check=check2,timeout=60)
				except asyncio.TimeoutError:
					await paramMsg.delete()
					return 1

				listChannelMentions = paramRep.channel_mentions
				if len(listChannelMentions) > 0:
					newChannel = listChannelMentions[0]
					newAlert.notifChannel = newChannel.id

					tempMsg = await paramRep.channel.send(content="✅ Les futures alertes seront envoyées dans le salon {0}".format(newChannel.mention),components=[])
					await asyncio.sleep(3)
					await tempMsg.delete()
					try:
						await paramRep.delete()
					except:
						pass
					break
				else:
					await paramRep.add_reaction("❌")
					await paramRep.channel.send(content="❌ Vous n'avez mentionné aucun salon",delete_after=5)

			try:
				gestion.globalVar.updateStreamEmbed(newAlert)
				await paramMsg.edit(embed=discord.Embed(title="__Nouvelle alerte enregistrée__",color=green,description="✅ Votre nouvelle alerte a été enregistrée avec succès.\nVous pouvez dorénavant la personnaliser depuis la liste des alertes du serveur.\n\n__Streamer :__ {0} ({1})\n__Salon :__ {2}\n__Rôle notifié :__ {3}".format(twUser.name,twUser.login,newChannel.mention,newRole.mention),components=[],delete_after=10))
			except Exception as e :
				await paramMsg.edit(embed=discord.Embed(title="__Erreur lors de l'enregistrement de l'alerte__",color=red,description="Une erreur est survenue lors de l'enregistrement de l'alerte :\n{0}".format(e),components=[],delete_after=10))

		else:
			newMsg = await rep.send(content="Chargement des paramètres de l'alerte <a:loading:862459118912667678>...",components=[])
			user = getStreamerUser(rep.values[0])
			while 1:
				selectAlert = gestion.globalVar.getStreamAlertEmbed(guild.id,rep.values[0])
				tablSettings = [selectAlert.notifMsg,selectAlert.embedTitle,selectAlert.embedDesc, selectAlert.embedColor, selectAlert.hyperlinkTxt, [selectAlert.image0,"-"][selectAlert.image0 == None], [selectAlert.image1,"-"][selectAlert.image1 == None], [selectAlert.image2,"-"][selectAlert.image2 == None]]
				tablSettings2 = [bool(selectAlert.showImage)]
				allTabl = tablSettings+tablSettings2
				desc, tablOption = "__Paramètres de l'alerte :__\n",[]
				for cmpt in range(len(allTabl)):
					desc += "\n__**{0}** :__\n{1}\n*> {2}*".format(tablSelectEmbed[cmpt][0],allTabl[cmpt],tablSelectEmbed[cmpt][1].replace("\n","\n> "))
					tablOption.append(create_select_option(tablSelectEmbed[cmpt][0],str(cmpt),description=tablSelectEmbed[cmpt][1].splitlines()[0]))

				mainEmb = discord.Embed(title="__Alerte de stream ({0} - {1})__".format(guild.name,user.name),color=light_blue,description=desc)
				mainEmb.set_thumbnail(url=user.avatar)

				comp = [
						create_actionrow(create_select(tablOption,placeholder="Sélectionnez une catégorie à modifier")),
						create_actionrow(exempleButton,deleteButton)
					]
				
				await newMsg.edit(content="",embed=mainEmb,components=comp)
				try:
					customRep = await wait_for_component(bot,newMsg,comp,check,180)
				except asyncio.TimeoutError:
					await newMsg.delete()
					return 1
					
				if customRep.component_type == ComponentType.button:
					if customRep.custom_id == exempleButton["custom_id"]:
						tempMsg = await customRep.send(content="Génération de la fausse alerte <a:loading:862459118912667678>...",components=[])
						roles = await guild.fetch_roles()
						for roly in roles:
							if roly.id == selectAlert.notifRole:
								selectAlert.notifRole = roly
								break

						selectAlert.notifChannel = ctx.channel

						def formatTwitchTxt(txt,twitchEmb:gestion.streamEmbed,stream:stream):
							return txt.format(
								notifRole = selectAlert.notifRole.mention,
								streamerName = stream.streamer,
								streamTitle = stream.title,
								gameName = stream.game,
								hyperlink = twitchEmb.hyperlink
								)

						fakeStream = stream("Lenapy Title",user.name,"Lenapy Game","https://media.discordapp.net/attachments/685104853596241964/1028436862030839889/Sans_titre_195_20221009003940.png?width={width}&height={height}",user.login)
						selectAlert.notifMsg = formatTwitchTxt(selectAlert.notifMsg,selectAlert,fakeStream)
						selectAlert.embedTitle = formatTwitchTxt(selectAlert.embedTitle,selectAlert,fakeStream)
						selectAlert.embedDesc = formatTwitchTxt(selectAlert.embedDesc,selectAlert,fakeStream)

						emb = discord.Embed(title=selectAlert.embedTitle,description=selectAlert.embedDesc,color=selectAlert.embedColor)
						if selectAlert.showImage:
							tablImage = []
							for img in [selectAlert.image0,selectAlert.image1,selectAlert.image2]:
								if img != None:
									tablImage.append(img)
							
							if len(tablImage) > 1:
								img = tablImage[random.randint(0,len(tablImage)-1)]
							elif len(tablImage) == 1:
								img = tablImage[0]
							else:
								img = fakeStream.thumbnail.format(width=500,height=280)
							emb.set_image(url=img)
						emb.set_thumbnail(url=user.avatar)
						emb.set_footer(icon_url=user.avatar,text=fakeStream.streamer)

						try:
							await tempMsg.edit(content=selectAlert.notifMsg,embed=emb)
						except Exception as e:
							await tempMsg.edit(content="Une erreur est survenue durant le test : {0}".format(e))
					elif customRep.custom_id == deleteButton["custom_id"]:
						comp = [create_actionrow(cancelButton,deleteButton)]
						deleteMsg = await customRep.send(content="",embed=discord.Embed(title="__Supprimer cette alerte ?__",color=red,description="Si vous voudrez la réactiver il faudra tout recommencer !"),components=comp)
						try:
							deleteRep = await wait_for_component(bot,deleteMsg,comp,check,60)
						except asyncio.TimeoutError:
							await newMsg.delete()
							await deleteMsg.delete()
							return 1

						if deleteRep.custom_id == deleteButton["custom_id"]:
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
						return m.author.id == int(ctx.author_id) and m.channel.id == ctx.channel.id
					customRep.values[0] = int(customRep.values[0])
					if customRep.values[0] in [0,1,2,4]:
						desc = ["Veillez écrire le nouveau message.\nVous pouvez rajouter des balises de formatage pour dynamiser un peu votre annonce !\n\n__{streamerName}__ : Nom du streamer\n__{streamTitle}__ : Titre du stream\n__{gameName}__ : Nom du jeu\n__{hyperlink}__ : Lien vers le stream\n> Ne fonctionne que dans la description de l'embed\n__{notifRole}__ : Mentionne le role\n> Ne fonctionne que dans le message d'annonce\n\nEntrez \"Retour\" pour annuler","Veuillez entrer le nouveau texte du lien.\n\nEntrez \"Retour\" pour annuler"][customRep.values[0] == 4]
						editMsg = await customRep.send(embed=discord.Embed(title="__Personnalisation de l'alerte__",color=light_blue,description=desc))
						
						try:
							editRep = await bot.wait_for(event='message',check=check2,timeout=60)
							await editRep.add_reaction('<a:loading:862459118912667678>')
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
							elif customRep.values[0] == 4:
								selectAlert.hyperlinkTxt = editRep.content

							gestion.globalVar.updateStreamEmbed(selectAlert)
							try:
								await editRep.clear_reactions()
							except:
								pass
							await editRep.add_reaction('✅')
							await editMsg.delete()
					elif customRep.values[0] == 3:
						colorMsg = await customRep.send(embed = discord.Embed(title="__Couleur de l'embed__",description="Veillez entrer le code hexadecimal de votre nouvelle couleur :\n\nExemples :\n94d4e4\n#94d4e4",color = light_blue))
						while 1:
							try:
								respond = await bot.wait_for("message",check=check2,timeout=60)
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
									await respond.add_reaction('❌')
									await colorMsg.channel.send(content="Le code donné n'est pas un code hexadecimal valide",delete_after=5)
								else:
									break
						if not(respond.content == "Retour"):
							comp = [create_actionrow(confirmButton,rejectButton)]
							await colorMsg.edit(embed = discord.Embed(title = "Couleur personnalisée",description="Est-ce que cette couleur vous va ?",color = color),components=comp)
							try:
								react = await wait_for_component(bot,colorMsg,comp,check,timeout=60)
							except asyncio.TimeoutError:
								await newMsg.delete()
								await colorMsg.delete()
								return 1

							if react.custom_id == confirmButton["custom_id"]:
								selectAlert.color = color
								gestion.globalVar.updateStreamEmbed(selectAlert)
								await colorMsg.delete()
					elif customRep.values[0] in [5,6,7]:
						desc = "Veillez entrer l'URL de votre image\nEntrez \"None\" pour supprimer l'image actuelle.\nEntrez \"Retour\" pour annuler\nNote : Une image peut ne pas s'afficher si l'url ne correspond pas à une image"
						editMsg = await customRep.send(embed=discord.Embed(title="__Personnalisation de l'alerte__",color=light_blue,description=desc))

						try:
							editRep = await bot.wait_for(event='message',check=check2,timeout=60)
							await editRep.add_reaction('<a:loading:862459118912667678>')
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
								await editRep.clear_reactions()
							except:
								pass
							await editRep.add_reaction('✅')
							await editMsg.delete()
					else:
						comp = [create_actionrow(create_select([create_select_option("Afficher","1"),create_select_option("Cacher","0")]))]
						editMsg = await customRep.send(embed=discord.Embed(title="__Personnalisation de l'alerte__",color=light_blue,description="Voulez-vous afficher ou cacher les images ?"),components=comp)
						try:
							editRep = await wait_for_component(bot,editMsg,comp,check,60)
						except asyncio.TimeoutError:
							await newMsg.delete()
							await editMsg.delete()
							return 1

						selectAlert.showImage = bool(int(editRep.values[0]))
						gestion.globalVar.updateStreamEmbed(selectAlert)
						await editMsg.delete()

