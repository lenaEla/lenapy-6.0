from gestion import existFile
from constantes import light_blue
from typing import Union
import interactions

async def new_patch(bot : interactions.Client, ctx : interactions.Message):
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

async def send_patchnote(ctx: Union[interactions.CommandContext, interactions.Channel]):
    """Permet d'envoyer le patchnote enregistré"""
    if type(ctx) == interactions.CommandContext:
        await ctx.defer()
    patchView = open("./data/patch/patch.txt","r")
    view = patchView.readlines()
    patchView.close()
    lastTxt, embedList, tempEmbDesc = "", [], ""
    for txt in view[1:]:
        if txt.startswith("__"):
            if tempEmbDesc != "":
                embedList.append(interactions.Embed(title=lastTxt,description=tempEmbDesc,color=light_blue))
            lastTxt, tempEmbDesc = txt, ""
        else:
            tempEmbDesc = tempEmbDesc + txt
        if txt == view[-1]:
            embedList.append(interactions.Embed(title=lastTxt,description=tempEmbDesc,color=light_blue))

    await ctx.send(content="```"+view[0]+"```",embeds=embedList)