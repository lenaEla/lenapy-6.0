from gestion import getEmojiObject
import interactions
from constantes import light_blue
from advance_gestion import timeoutSelect

normalFightDesc = """Permet de lancer un combat normal.

Les combats normaux ont un cooldown de 1 heure, syncronisé pour toute l'équipe.
Au début du combat vous sera demandé si vous êtes présent ou non. Les utilisateurs n'ayant pas répondu au bout d'un certain temps seront controlé par le bot.

Si une équipe est composé de moins de 4 joueurs, des alliés temporaires contrôlés par le bot seront rajouté à l'équipe pour le combat.

Les combats raportent de l'expérience (en fonction des ennemis vaincus) et des pièces (en fonction du nombre de tours qu'à duré le combat).
En cas de victoire, chaque joueur a 20% de chance d'obtenir un équipement qu'il ne possédait pas déjà."""

quickFightDesc = """Permet de lancer un combat rapide.

Les combats rapides ont un cooldown de 3 heures, syncronisé pour toute l'équipe.
Si une équipe est composé de moins de 4 joueurs, des alliés temporaires contrôlés par le bot seront rajouté à l'équipe pour le combat.

Les combats rapident sautent tout le combat pour n'afficher directement que l'écran des résultats. Par conséquent, il y est impossible de contrôler son personnage.

Les combats raportent de l'expérience (en fonction des ennemis vaincus) et des pièces (en fonction du nombre de tours qu'à duré le combat).
En cas de victoire, chaque joueur a 20% de chance d'obtenir un équipement qu'il ne possédait pas déjà."""

allCommands = [
    #{"name":"","short":"","long":"","catégorie":""},
    {"name":"settings","short":"Permet de définir des paramètres pour le serveur","long":"⚠ Cette commande nécessite que l'utilisateur ai la permission de gérer les salons.\n\nPermet d'initialiser le menu des paramètres du serveur.\nDe là, vous pourrez définir le salon Patchnote ou le salon Bot","catégorie":"utilitaire"},
    {"name":"choose","short":"Renvoie un choix aléatoire parmis une liste donnée","long":"Permet de choisir aléatoirement parmit plusieurs options données.\n\nl!choose *Option 1*| *Option 2* | *...* | *Option n*","catégorie":"utilitaire"},
    {"name":"invite","short":"Obtenez le lien d'invitation du bot","long":"Renvoie un lien d'invitation pour inviter Lenapy sur un serveur.\n\n⚠ Vous devez avoir la permission de gérer le serveur en question","catégorie":"utilitaire"},
    {"name":"start","short":"Permet de commencer l'aventure","long":"Si vous n'avez pas commencé l'aventure, permet d'initialiser le menu de départ\nVous sera demandé de choisir l'espèce, le nom, la couleur et l'aspiration de votre personnage.\n\n- La couleur sera affiché sur tous les embeds en rapport avec votre personnage. \n- L'aspiration détermine les statistiques de base de votre personnage et leur augmentation","catégorie":"aventure"},
    {"name":"stats","short":"Permet de voir ses stats","long":"Vous permet de voir les statistiques de votre personnage, ainsi que votre équipement.","catégorie":"aventure"},
    {"name":"solde","short":"Permet de voir votre nombre de pièces","long":"Vous permet de voir la solde actuelle de votre personnage.","catégorie":"aventure"},
    {"name":"inventory","short":"Permet de voir son inventaire","long":"Vous permet de voir les armes et compétences dans votre inventaire, ou de changer votre élément.\n\nVous pouvez entrer le nom ou l'identifiant de l'équipement/compétence en question pour pouvoir accéder directement à sa page d'information.\n\n__Procuration__ : Si une personne vous as donné procuration sur son inventaire via la commande du même nom, vous pourrez ouvrir son inventaire comme si c'était lui réalisait la commande.\n\nSi vous la possédez, vous permettra de l'équiper.","catégorie":"aventure"},
    {"name":"points","short":"Permet de répartir ses points bonus","long":"Vous permet de répartir vos points bonus obtenu grace aux montées de niveau\n\n__Procuration__ : Si une personne vous as donné procuration sur son inventaire via la commande du même nom, vous pourrez utiliser cette commande comme si c'était lui qui la réalisait.","catégorie":"aventure"},
    {"name":"shop","short":"Ouvre le magasin","long":"Vous permet de dépenser vos pièces pour acheter Armes, Compétences ou Equipement.\nIndique aussi les cooldowns des commandes /fight et /quickfight","catégorie":"aventure"},
    {"name":"team view","short":"Permet de voir son équipe","long":"Permet d'afficher les joueurs de votre équipe ainsi que leurs équipements","catégorie":"aventure"},
    {"name":"team up","short":"Permet d'ajouter quelqu'un dans votre équipe","long":"Permet d'ajouter le joueur mentionné dans votre équipe, si ce dernier n'en a pas","catégorie":"aventure"},
    {"name":"team quit","short":"Permet de quitter son équipe","long":"Permet de quitter son équipe","catégorie":"aventure"},
    {"name":"fight normal","short":"Permet de lancer un combat normal","long":normalFightDesc,"catégorie":"aventure"},
    {"name":"fight quick","short":"Permet de lancer un combat rapide","long":quickFightDesc,"catégorie":"aventure"},
    {"name":"fight octogone","short":"Permet de lancer un combat PvP 1v1","long":"Permet d'affronter un autre joueur. Les combats PvP ne donnent pas d'exp ni de pièces","catégorie":"aventure"},
    {"name":"fight team","short":"Permet de lancer un combat PvP en équipe","long":"Permet d'affronter l'équipe d'un autre joueur. Les combats PvP ne donnent pas d'exp ni de pièces","catégorie":"aventure"},
    {"name":"roll","short":"Permet de lancer un dé","long":"Permet de lancer un dé.\nLe minimum et le maximum peuvent être personnalisé","catégorie":"utilitaire"},
    {"name":"procuration","short":"Permet de donner procuration sur son inventaire","long":"Permet à un autre utilisateur d'avoir accès à votre inventaire pour équiper des trucs à votre place","catégorie":"aventure"},
    {"name":"encyclopedia","short":"Permet de consulter l'encyclopédie","long":"Permet de consulter l'encyclopédie de Bot, qui ressence toutes les armes, équipements, compétenes, alliés temporaires, ennemis, boss et succès du bot","catégorie":"aventure"},
    {"name":"patchnote","short":"Permet d'afficher le dernier patchnote","long":"Permet d'afficher le dernier patchnote","catégorie":"utilitaire"},
]

helpUtils, helpAdventure = [],[]

for a in allCommands:
    if a["catégorie"] == "utilitaire":
        helpUtils.append(a)
    elif a["catégorie"] == "aventure":
        helpAdventure.append(a)
    else:
        print("{0} n'a pas de catégorie valide ({1})".format(a["name"],a["catégorie"]))

nameCat,tablCat = ["Utilitaire","Aventure"],[helpUtils,helpAdventure]

categorieSelect = interactions.SelectMenu(custom_id = "catSelect", 
    options=[
        interactions.SelectOption(label="Utilitaire",value="0",description="Retrouvez toutes les commandes utilitaires du bot"),
        interactions.SelectOption(label="Aventure",value="1",description="Retrouvez toutes les commandes en lien avec l'Aventure du bot"),
    ], 
    placeholder="Séléctionnez une catégorie"
)

firstEmbedDesc = """__Page d'aide de **Lenapy**__
Lenapy est un bot discord de style rpg développé par LenaicU#4888 durant son temps libre, codé en Python.

LenaicU ne prétend pas posséder tous les icones et visuels utilisés par le bot.
Si certains posent problème, vous pouvez faire une réclammation via MP.

Vous vous trouvez actuellement sur la page d'acceuil de la commande /help.
Pour obtenir plus d'informations sur les commandes du bot, veillez entrer une catégorie dans le menu déroulant ci-dessous
"""

buttons = interactions.ActionRow(components=[
    interactions.Button(type=2, style=5, label="GitHub", emoji=getEmojiObject('<:github:892369658429190166>'),url='https://github.com/lenaEla/lenapy-2.0'),
    interactions.Button(type=2, style=5, value="Inviter le bot", emoji=getEmojiObject('<:lenapy:892372680777539594>'),url='https://discord.com/api/oauth2/authorize?client_id=623211750832996354&permissions=328565386304&scope=bot%20applications.commands')
])

async def helpBot(bot,ctx):
    msg = await ctx.send(embeds=interactions.Embed(title="__/help__",color=light_blue,description=firstEmbedDesc),components=[interactions.ActionRow(components=[categorieSelect]),buttons])

    def check(m):
        return m.author.id == ctx.author.id and m.message.id == msg.id

    try:
        respond = await bot.wait_for_component(components=categorieSelect,check=check,timeout=60)
        continu = True
    except:
        await msg.delete()
        continu = False

    if continu:
        tablToSee,value = [], int(respond.data.values[0])
        for a in range(0,len(tablCat)):
            if value == a:
                tablToSee = sorted(tablCat[a],key= lambda com: com["name"])
                break

        leni = len(tablToSee)
        page,maxPage = 0,leni//10
        if leni%10 == 0:
            maxPage -= 1
        
        while 1:
            commandInfoOptions = []
            if page > 0:
                commandInfoOptions.append(interactions.SelectOption(label="Page précédente",value="0",description="Retournez à la page précédente"))
            maxi,desc = (page+1)*10,"__Page **{0}** / {1}__\n".format(page+1,maxPage+1)
            if maxi > leni:
                maxi = leni
            for a in tablToSee[page*10:maxi]:
                desc += f'\n__/{a["name"]}__\n*{a["short"]}*\n'
                commandInfoOptions.append(interactions.SelectOption(label=a["name"],value=a["name"],description=a["short"]))

            
            if page < maxPage:
                commandInfoOptions.append(interactions.SelectOption(label="Page suivante",value="1",description="Allez à la page suivante"))
            commandInfoSelect = interactions.SelectMenu(custom_id = "commandInfoSelect", options=commandInfoOptions,placeholder="Sélectionnez une commande pour avoir plus d'informations")
            await msg.edit(embeds = interactions.Embed(title="__/help {0}__".format(nameCat[value]),color=light_blue,description=desc),components=[interactions.ActionRow(components=[commandInfoSelect])])
            
            try:
                respond = await bot.wait_for_component(components=commandInfoSelect,check=check,timeout=60)
            except:
                await msg.edit(embeds = interactions.Embed(title="__/help {0}__".format(nameCat[value]),color=light_blue,description=desc),components=[timeoutSelect])
                break

            value2 = respond.data.values[0]
            if value2 == "0":
                page -= 1
            elif value2 == "1":
                page += 1
            else:
                wanted = None
                for a in tablToSee:
                    if a["name"] == value2:
                            wanted=a
                            break

                if wanted != None:
                    await respond.send(embeds=interactions.Embed(title="__/help {0}__".format(wanted["name"]),color=light_blue,description=wanted["long"]))
                else:
                    await respond.send("La commande n'a pas pu être retrouvée :/")
