from interactions import *
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from commands_files.achievement_handler import *
from commands_files.alice_stats_endler import *
from typing import Union, List

HIGHLIGHTBOSS, HIGHLIGHTPURCENT, BOSSPURCENT = "Phy", 25, 25
RAIDPURCENT, RAIDHIGHLIGHTPURCENT, RAIDHIGHLIGHT = 5, 0, "Nacialisla"

teamWinDB = dbHandler("teamVic.db")
AI_DPT,AI_BOOST,AI_SHIELD,AI_AVENTURE,AI_ALTRUISTE,AI_OFFERUDIT,AI_MAGE,AI_ENCHANT = 0,1,2,3,4,5,6,7
moveEmoji = ['⬅️','➡️','⬆️','⬇️']
cancelButton = interactions.ActionRow(interactions.Button(style=2,label="Retour",emoji=PartialEmoji(name="◀️"),custom_id="return"))
waitingSelect = interactions.ActionRow(interactions.StringSelectMenu(interactions.StringSelectOption(label="Veuillez prendre votre mal en patience",value="wainting...",emoji=PartialEmoji(name='🕰️'),default=True),custom_id = "waitingSelect",disabled=True))

hiddenIcons = ['<:co:888746214999339068>','<:le:892372680777539594>','<:to:905169617163538442>','<:lo:887853918665707621>','<:co:895440308257558529>']+aspiEmoji

altDanger = [65,70,70,70,75,75,80,80,85,90,100,100]
dangerLevel = [70,75,80,80,90,90,90,100,110,120,135]
HEALRESISTCROIS, SHIELDREDUC = 0.2, 0.2
BASEHP_PLAYER, BASEHP_ENNEMI, BASEHP_SUMMON, BASEHP_BOSS = 200, 150, 100, 650
HPPERLVL_PLAYER, HPPERLVL_ENNEMI, HPPERLVL_SUMMON, HPPERLVL_BOSS = 30, 20, 20, 160

MELEE_END_CONVERT = 35
END_NEEDED_10_INDRES, MAX_END_10_INDRES = 130, 35
END_NEEDED_10_HEAL, MAX_END_10_HEAL = 150, 20

statEmbedFieldNames = ["__Liste des effets :__","__Statistiques :__","<:em:866459463568850954>","__Jauges :__","__Déployables :__","__Équipe Bleue :__","__Équipe Rouge :__"]

tablAchivNpcName = ["Alice","Clémence","Akira","Gwendoline","Hélène","Icealia","Shehisa","Powehi","Félicité","Sixtine","Hina","Julie","Krys","Lio","Liu","Liz","Lia","Iliana","Stella","Kiku","Kitsune","Ailill","Altikia","Klironovia","Lia Ex","Iliana prê.","Anna","Belle","Clémence Exaltée","Luna ex.","Clémence pos.","Céleste","Shushi"]
tablAchivNpcCode = ["alice","clemence","akira","gwen","helene","icea","sram","powehi","feli","sixtine","hina","julie","krys","lio","liu","liz","lia","light","stella","kiku1","momKitsune","ailill2","alty","klikli","liaEx","catEx","anna","belle","clemEx","luna","clemMem","celeste","shushi"]

LIFESAVOREFF = [deterEff1.id,zelianR.id,healingTimeBombEff.id,lifeSeedEff.id]


dictAllyToReplace = {
    "Clémence pos.":["Clémence"],
    "Luna ex.":["Luna","Lena"],
    "Kiku":["Ly","Chûri","Céleste"],
    "Akira H.":["Akira"],
    "Iliana ex.":["Iliana"],
    "Iliana OvL":["Iliana"]
}

tablIsNpcName = []
for a in tablAllAllies + tablVarAllies + ["Liu","Lia","Liz","Lio","Ailill","Kiku","Stella","Séréna","OctoTour","Kitsune","The Giant Enemy Spider","[[Spamton Neo](https://deltarune.fandom.com/wiki/Spamton)]","Nacialisla","Luna ex.","Clémence pos."]:
    if type(a) != str: tablIsNpcName.append(a.name)
    else: tablIsNpcName.append(a)

temp = []
for a in tablIsNpcName: temp.append((a,False))
primitiveDictIsNpcVar = dict(temp)

effToSpecialVars = [altOHEff.id,proOHEff.id,idoOHEff.id,idoOSEff.id,proOSEff.id,preOSEff.id,heriteEstialbaEff.id,heriteLesathEff.id,floorTanking.id,foulleeEff.id,exploHealMarkEff.id,squidRollEff.id,partnerIn.id,counterTimeEff.id]

AGI_REQUIERD_FOR_30_CRIT = 180
PRE_REQUIERD_FOR_30_CRIT = 180
END_REQUIERD_FOR_30_CRIT = 350

getHpButton = Button(style=ButtonStyle.GRAY,label="Graphiques",emoji=getEmojiObject("<:ConfusedStonks:782072496693706794>"),custom_id="hpChart")
getHpButtonD = copy.deepcopy(getHpButton)
getHpButtonD.disabled=True

LAST_DITCH_EFFORT_MAX_POWER = 40
LAST_DITCH_EFFORT_START_TURN, LAST_DITCH_EFFORT_MAX_TURN = 15, 20
LAST_DITCH_EFFORT_START_ALLIE, LAST_DITCH_EFFORT_MAX_ALLIE = 0.5, 0.2

effListShowPower = [vulne.id,dmgUp.id,dmgDown.id,defenseUp.id,akikiSkill1Eff.id,incurable.id,armorGetMalus.id,healDoneBonus.id,absEff.id]
