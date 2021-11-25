import discord, os
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *

async def procuration(ctx : discord.message):
    pathUserProfile = absPath + "/userProfile/" + str(ctx.author.id) + ".prof"

    if os.path.exists(pathUserProfile):
        if ctx.mentions != []:
            user = loadCharFile(pathUserProfile)
            user.procuration += [ctx.mentions[0].id]

            if saveCharFile(pathUserProfile,user):
                await ctx.channel.send(f"{ctx.mentions[0].name} à bien été rajouté à la liste des personnes ayant procuration sur votre inventaire")
            else:
                await ctx.channel.send(embed = errorEmbed("Procuration","Une erreure est survenue"))
        else:
            await ctx.channel.send(embed = errorEmbed("Procuration","Vous devez mentionner quelqu'un"))
    else:
            await ctx.channel.send(embed = errorEmbed("Procuration","Vous n'avez pas commencé l'aventure"))