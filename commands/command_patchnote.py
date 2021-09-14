from gestion import existFile
import discord

async def new_patch(bot : discord.Client,ctx : discord.Message):
    """Permet d'enregistrer un nouveau patchnote"""
    existFile("./data/patch/patch.txt")
    patchFile = open("./data/patch/patch.txt","w")
    patchFile.write(ctx.content[11:])
    patchFile.close()

    patchView = open("./data/patch/patch.txt","r")
    toSend = ""
    view = patchView.readlines()
    patchView.close()
    for a in view:
        toSend += a
    await ctx.channel.send("Le patch note suivant a été enregistré :")
    await ctx.channel.send(toSend)

def get_patchnote():
    """Renvoie le str contenant le patchnote"""
    patchView = open("./data/patch/patch.txt","r")
    toSend = ""
    view = patchView.readlines()
    patchView.close()
    for a in view:
        toSend += a
    return toSend
