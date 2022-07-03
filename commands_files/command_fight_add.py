import discord, random, os, emoji, asyncio, datetime, copy
from discord_slash.context import SlashContext
from discord_slash.utils.manage_components import create_actionrow, create_select, create_select_option, create_button
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from commands_files.sussess_endler import *
from commands_files.alice_stats_endler import *
from traceback import format_exc
from typing import Union, List
from sys import maxsize
from socket import error as SocketError
import errno

teamWinDB = dbHandler("teamVic.db")
AI_DPT,AI_BOOST,AI_SHIELD,AI_AVENTURE,AI_ALTRUISTE,AI_OFFERUDIT,AI_MAGE,AI_ENCHANT = 0,1,2,3,4,5,6,7
moveEmoji = ['⬅️','➡️','⬆️','⬇️']
cancelButton = create_actionrow(create_button(ButtonStyle.grey,"Retour",'◀️',custom_id="return"))
waitingSelect = create_actionrow(create_select([create_select_option("Veuillez prendre votre mal en patience","wainting...",'🕰️',default=True)],disabled=True))

altDanger = [65,70,70,70,75,75,75,80,85,90,95,100]

tablIsNpcName = []
for a in tablAllAllies + tablVarAllies + ["Liu","Lia","Liz","Lio","Ailill","Kiku","Stella","Séréna","OctoTour","Kitsune","The Giant Enemy Spider","[[Spamton Neo](https://deltarune.fandom.com/wiki/Spamton)]"]:
    if type(a) != str:
        tablIsNpcName.append(a.name)
    else:
        tablIsNpcName.append(a)

temp = []
for a in tablIsNpcName:
    temp.append((a,False))

primitiveDictIsNpcVar = dict(temp)

def getPartnerValue(user : classes.char):
    if user.aspiration in [BERSERK,POIDS_PLUME,TETE_BRULE,ENCHANTEUR]:
        return 10 + random.randint(-3,3)
    elif user.aspiration in [PROTECTEUR,ATTENTIF]:
        return 8 + random.randint(-3,3)
    elif user.aspiration in [OBSERVATEUR,VIGILANT,MAGE,SORCELER]:
        return 6 + random.randint(-3,3)
    else:
        return 4 + random.randint(-3,3)

def dmgCalculator(caster, target, basePower, use, actionStat, danger, area, typeDmg = TYPE_DAMAGE, skillPercing = 0):
    if use == HARMONIE:
        maxi, stats = -100, caster.allStats()
        for cmpt in range(0,7):
            if stats[cmpt] > maxi:
                maxi, use = stats[cmpt], cmpt 
    if use not in [FIXE,None]:
        dmgBonusMelee = int(caster.aspiration in [BERSERK,POIDS_PLUME,TETE_BRULE,ENCHANTEUR] and caster.char.weapon.range == RANGE_MELEE) * caster.endurance/150*0.15 +1
        enemyPercing = [caster.percing+skillPercing, max(caster.percing+skillPercing,15)][target.isNpc("Clémence Exaltée") or target.isNpc("Luna prê.")]
        resistFactor = (1-(min(95,target.resistance*(1-(caster.percing+skillPercing)/100))/100))
        lvlBonus = (1+(DMGBONUSPERLEVEL*caster.level))
        if lvlBonus > 2.5 and type(caster.char) not in [char,tmpAllie]:
            lvlBonus = 2.5
        dmg = round(basePower * (max(-65,caster.allStats()[use]+100-caster.actionStats()[actionStat]))/100 *(danger/100)*caster.getElementalBonus(target=target,area=area,type=typeDmg)*lvlBonus*dmgBonusMelee)
        target.stats.damageResisted += dmg - (dmg*resistFactor)
        return max(1,round(dmg*resistFactor))
    else:
        return basePower

def indirectDmgCalculator(caster, target, basePower, use, danger, area):
    damage = ""
    dmgBonusMelee = int(caster.aspiration in [BERSERK,POIDS_PLUME,TETE_BRULE,ENCHANTEUR] and caster.char.weapon.range == RANGE_MELEE) * caster.endurance/150*0.1 +1
    if use != None:
        if use != HARMONIE:
            stat = caster.allStats()[use]-caster.negativeIndirect
        else:
            stat = max(caster.allStats())

        effMultiplier = 100 + 5*int(not(caster.auto))
        for eff in caster.effect:
            if eff.effect.id == dmgUp.id:
                effMultiplier += eff.effect.power
            elif eff.effect.id in [dmgDown.id,indDealReducTmp.id]:
                effMultiplier -= eff.effect.power
        for eff in target.effect:
            if eff.effect.id in [vulne.id,kikuRaiseEff.id]:
                effMultiplier += eff.effect.power
            elif eff.effect.id == defenseUp.id:
                effMultiplier -= eff.effect.power
            elif eff.effect.inkResistance != 0:
                effMultiplier -= eff.effect.inkResistance
            
        effMultiplier = max(effMultiplier, 5)
        effMultiplier = min(effMultiplier, 200)

        selfElem = caster.getElementalBonus(target,area,TYPE_INDIRECT_DAMAGE)
        dangerMul = [100, danger][caster.team == 1]
        lvlBonus = (1+(DMGBONUSPERLEVEL*caster.level))
        if lvlBonus > 2.5 and type(caster.char) not in [char,tmpAllie]:
            lvlBonus = 2.5
        damage = basePower * (1+(stat/100)) *  (1-(min(95,target.resistance*(1-caster.percing/100))/100)) * selfElem * lvlBonus * effMultiplier/100 * dangerMul/100 * dmgBonusMelee

    return damage

class timeline:
    """Classe de la timeline"""
    def __init__(self):
        self.timeline = []
        self.initTimeline = []
        self.begin = None

    def init(self,tablEntTeam : list):
        timeline = []

        for tabl in (0,1):
            tablPrio, tablNorm, tablLast = [],[],[]

            for ent in tablEntTeam[tabl]:
                suppSkillsCount,healSkillsCount = 0,0
                for skil in ent.char.skills:
                    if type(skil) == skill:
                        if skil.type in [TYPE_BOOST,TYPE_MALUS] or skil.id in [invocBat2.id]:
                            suppSkillsCount += 1
                        elif skil.type in [TYPE_ARMOR,TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_RESURECTION] or skil.id in [idoOSEff.id,proOSEff.id,preOSEff.id,invocSeraf.id,idoOHEff.id,proOHEff.id,altOHEff.id,lightAura.id,lightAura2.id,invocFee.id,lapSkill.id]:
                            healSkillsCount += 1

                if (suppSkillsCount >= 3 and random.randint(0,99)<50) or (ent.char.weapon.range == RANGE_MELEE and random.randint(0,99)<33) or not(ent.auto):
                    tablPrio.append(ent)
                elif healSkillsCount >= 3 and random.randint(0,99)<50:
                    tablLast.append(ent)
                else:
                    tablNorm.append(ent)

            tabltabl = [tablPrio,tablNorm,tablLast]
            for cmpt in (0,1,2):
                random.shuffle(tabltabl[cmpt])

            tablEntTeam[tabl] = tabltabl[0]+tabltabl[1]+tabltabl[2]
        for a in range(max(len(tablEntTeam[0]),len(tablEntTeam[1]))):
            try:
                timeline+=[tablEntTeam[0][a]]
            except:
                pass
            try:
                timeline+=[tablEntTeam[1][a]]
            except:
                pass

        self.timeline = timeline
        self.initTimeline = copy.copy(timeline)
        self.begin = self.initTimeline[0]

        return self, tablEntTeam

    def getActTurn(self):
        return self.timeline[0]

    def icons(self):
        temp = ""
        for a in self.timeline:
            if a == self.initTimeline[-1]:
                temp += f"{a.icon} <|- "
            else:
                temp += f"{a.icon} <- "
        return temp

    def endOfTurn(self,tablEntTeam,tablAliveInvoc):
        timelineTempo = self.timeline
        actTurn = timelineTempo[0]

        timelineTempo.remove(actTurn)
        timelineTempo.append(actTurn)

        for ent in self.timeline[:]:
            if ent.hp <= 0 and type(ent.char) == invoc:
                inv = ent
                timelineTempo.remove(inv)
                inv.cell.on = None
                for ent2 in tablEntTeam[inv.team]:
                    if ent2.id == inv.summoner.id:
                        smn = ent2
                        smn.stats.damageDeal += inv.stats.damageDeal
                        smn.stats.indirectDamageDeal += inv.stats.indirectDamageDeal
                        smn.stats.ennemiKill += inv.stats.ennemiKill
                        smn.stats.damageRecived += inv.stats.damageRecived
                        smn.stats.heals += inv.stats.heals
                        smn.stats.damageOnShield += inv.stats.damageOnShield
                        smn.stats.shieldGived += inv.stats.shieldGived

                        for dictElem in inv.ownEffect:
                            for on, effID in dictElem.items():
                                for effOn in on.effect:
                                    if effOn.id == effID:
                                        effOn.caster = smn
                                        effOn.effect.power = int(effOn.effect.power * 0.7)
                                        break

                                on.refreshEffects()

                        smn.ownEffect += inv.ownEffect
                        break

                tablEntTeam[inv.team].remove(inv)
                tablAliveInvoc[inv.team] -= 1

        self.timeline = timelineTempo
        return tablEntTeam, tablAliveInvoc

def map(tablAllCells,bigMap,showArea:List[cell]=[],fromEnt=None,wanted=None,numberEmoji=None,fullArea=[]):
    """Renvoie un str contenant la carte du combat"""
    line1,line2,line3,line4,line5 = [None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None]
    lines = [line1,line2,line3,line4,line5]

    if bigMap:
        line6, line7 = [None,None,None,None,None,None],[None,None,None,None,None,None]
        lines.append(line6)
        lines.append(line7)

    for a in tablAllCells:
        if isLenapy or True:
            if a in fullArea and not(a in showArea):
                temp = '<:unseenTargeted:978458473018830858>'
            else:
                temp = ['<:em:866459463568850954>',['<:tb:873118129214083102>','<:tr:873118129130192947>'][wanted==ENEMIES]][a in showArea]
        else:
            temp = f'{str(a.x)}:{str(a.y)}'                         # Show cells ID
        if a.on != None:
            if a.on.status == STATUS_DEAD:
                temp = ['<:ls:868838101752098837>','<:ls:868838465180151838>'][a.on.team]
            elif a.on.status != STATUS_TRUE_DEATH:
                if a.on.invisible:                              # If the entity is invisible, don't show it. Logic
                    temp = '<:em:866459463568850954>'
                elif a not in showArea or (wanted==ALLIES and a.on.team != fromEnt.team) or (wanted==ENEMIES and a.on.team == fromEnt.team):
                    if a not in showArea and a in fullArea:
                        temp = '<:unsee:899788326691823656>'
                    else:
                        temp = [a.on.icon,'❇️'][a.on==fromEnt]
                elif a != fromEnt.cell:
                    temp = '<:unsee:899788326691823656>'
                    for cmpt in range(len(numberEmoji)):
                        if a.on == numberEmoji[cmpt]:
                            temp = listNumberEmoji[cmpt]
                            break
                else:
                    temp = '<:ikaWhiteTargeted1:873118129021157377>'
            else:
                a.on = None
        lines[a.y][a.x]=temp
    temp = ""
    for a in lines:
        for b in [0,1,2,3,4]:
            temp += f"{a[b]}|"
        temp += f"{a[b+1]}\n"
    return temp

def getHealAggro(on, skillToUse : Union[skill,weapon]):
    if on.hp <= 0 or on.hp >= on.maxHp:
        return 0
    elif type(on.char) == invoc:
        return -111
    else:
        prio = (1-on.hp/on.maxHp)*100

        prio = prio * (1.2 - (0.1*on.char.weapon.range))                # If the entity is a melee, he is more important
        if not(on.auto):
            prio = prio * 1.1                                           # If the entity is a active player, he is a little more important, for reduce the use of the spoon

        if (skillToUse.type == TYPE_HEAL and skillToUse.power >= 75 and on.maxHp - on.hp < on.char.level * 3) or (skillToUse.type == TYPE_INDIRECT_HEAL and on.hp/on.maxHp <= 0.35):
            prio = prio * 0.7                                           # If the skill is a big direct heal and the entity is not low Hp or if the skill is a HoT and the entity is low Hp
                                                                            # The entity is less important
        
        prio = prio * (1-(on.healResist/2/100))                             # If the entity have a big healing resist, he is less important

        incurValue, healAggroBonus = 0, 100
        for eff in on.effect:
            if eff.effect.id == incurable.id:
                incurValue = max(eff.effect.power,incurValue)
            elif eff.effect.id == undeadEff2.id:
                healAggroBonus += undeadEff2.power

        prio = prio * (1-(incurValue/2/100)) * (healAggroBonus/100)                              # Same with the healing reduce effects
        return prio

def getHealTarget(tablTeam : list, skillToUse : skill):
    if len(tablTeam) == 1:
        return tablTeam[0]
    elif len(tablTeam) < 1:
        raise AttributeError("tablTeam is empty")
    
    temp = tablTeam
    temp.sort(key=lambda funnyTempVarName:getHealAggro(funnyTempVarName,skillToUse),reverse=True)
    return temp[0]

def getPrelimManWindow(actTurn, LBBars: List[List[int]], tablEntTeam : List):
    toReturn, cmpt = actTurn.quickEffectIcons()+"Trans. : ", 0
    while cmpt < LBBars[actTurn.team][0]:
        if LBBars[actTurn.team][1]//3 > cmpt:
            toReturn += "<:lbF:983450379205378088>"
        elif LBBars[actTurn.team][1]%3 >= 0 and LBBars[actTurn.team][1] >= LBBars[actTurn.team][0]*3:
            toReturn += ["<:lb0:983450435404849202>","<:lb1:983450416010371183>","<:lb2:983450398645977218>"][LBBars[actTurn.team][1]%3]
        else:
            toReturn += "<:lb0:983450435404849202>"
        cmpt += 1
    baseStat, actStat, difStatMsg, difMsg = actTurn.baseStats, actTurn.allStats(), [], ""
    baseStat = [baseStat[0],baseStat[1],baseStat[2],baseStat[3],baseStat[4],baseStat[5],baseStat[6]]
    for cmpt in (0,1,2,3,4,5,6):
        if baseStat[cmpt] != actStat[cmpt]:
            difStatMsg.append("__{0}.__ {1}{2}".format(nameStats[cmpt][:3],["","+"][actStat[cmpt]-baseStat[cmpt]>0],actStat[cmpt]-baseStat[cmpt]))
    lenDif = len(difStatMsg)
    if lenDif == 1:
        difMsg = "\n{0}".format(difStatMsg[0])
    elif lenDif > 1:
        difMsg = "\n"
        for cmpt in range(lenDif):
            difMsg += "{0}".format(difStatMsg[cmpt])
            if cmpt < lenDif - 1:
                difMsg += ", "

    toReturn += difMsg
    dmgUpCount, defenseUpCount, buffMsg = 0, 0, ""
    for eff in actTurn.effect:
        if eff.effect.id == dmgUp.id:
            dmgUpCount += eff.effect.power
        elif eff.effect.id == dmgDown.id:
            dmgUpCount -= eff.effect.power
        elif eff.effect.id == defenseUp.id:
            defenseUpCount += eff.effect.power
        elif eff.effect.id == vulne.id:
            defenseUpCount -= eff.effect.power
    if dmgUpCount != 0:
        buffMsg += "\n{0} {1}{2}%".format(["<a:dmgDown:954430950668914748>","<a:dmgUp:954429227657224272>"][dmgUpCount>0],["","+"][dmgUpCount>0],round(dmgUpCount,2))
    if defenseUpCount != 0:
        if buffMsg != "":
            buffMsg += ", "
        else:
            buffMsg += "\n"
        buffMsg += "{0} {1}{2}%".format(["<a:defdown:954544494110441563>","<a:defup:954537632543682620>"][defenseUpCount>0],["","+"][defenseUpCount>0],round(defenseUpCount,2))

    allieUnHealthy, allieRea, allieDead, allieAlive = 0, 0, 0, 0
    for ent in tablEntTeam[actTurn.team]:
        if ent != actTurn and type(ent.char) != invoc:
            if ent.hp > 0 and ent.hp/ent.maxHp <= 0.5:
                allieUnHealthy += 1
            elif ent.hp <= 0 and ent.status == STATUS_DEAD:
                allieRea += 1
            elif ent.hp <= 0:
                allieDead += 1
            else:
                allieAlive += 1
    
    alliesEmoji = ["<:ha:866459302319226910>","<:inh:881587796287057951>","<:ls1:868838101752098837>","<:d2B:907289950301601843>"]
    for cmpt in [0,1,2,3]:
        if [allieAlive,allieUnHealthy,allieRea,allieDead][cmpt] > 0:
            if buffMsg != "":
                buffMsg += ", "
            else:
                buffMsg += "\n"
            buffMsg += "{0}x{1}".format(alliesEmoji[cmpt],[allieAlive,allieUnHealthy,allieRea,allieDead][cmpt])
    toReturn += buffMsg
    return toReturn
