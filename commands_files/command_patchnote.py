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
    await ctx.channel.send("Le patch note suivant a été enregistré :")
    for a in view:
        if len(toSend+a) <= 2000:
            toSend += a
        else: # If the message is to long, send it
            await ctx.channel.send(toSend)
            toSend = a
    
    await ctx.channel.send(toSend)

async def send_patchnote(ctx):
    """Permet d'envoyer le patchnote enregistré"""
    patchView = open("./data/patch/patch.txt","r")
    toSend = ""
    view = patchView.readlines()
    patchView.close()
    msg = 0
    for a in view:
        if len(toSend+a) <= 2000: 
            toSend += a
        else: # If the message is to long, send it
            if msg == 0:
                msg = await ctx.send(toSend)
            else:
                await msg.channel.send(toSend)
            toSend = a

    if msg == 0:
        msg = await ctx.send(toSend)
    else:
        await msg.channel.send(toSend)