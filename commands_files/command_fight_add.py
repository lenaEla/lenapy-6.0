import random, copy, interactions
from interactions import *
from adv import *
from classes import *
from donnes import *
from gestion import *
from advance_gestion import *
from commands_files.achievement_handler import *
from commands_files.alice_stats_endler import *
from typing import Union, List

teamWinDB = dbHandler("teamVic.db")
AI_DPT,AI_BOOST,AI_SHIELD,AI_AVENTURE,AI_ALTRUISTE,AI_OFFERUDIT,AI_MAGE,AI_ENCHANT = 0,1,2,3,4,5,6,7
moveEmoji = ['⬅️','➡️','⬆️','⬇️']
cancelButton = interactions.ActionRow(components=[interactions.Button(type=2,style=2,label="Retour",emoji=Emoji(name="◀️"),custom_id="return")])
waitingSelect = interactions.ActionRow(components=[interactions.SelectMenu(custom_id = "waitingSelect", options=[interactions.SelectOption(label="Veuillez prendre votre mal en patience",value="wainting...",emoji=Emoji(name='🕰️'),default=True)],disabled=True)])

hiddenIcons = ['<:co:888746214999339068>','<:le:892372680777539594>','<:to:905169617163538442>','<:lo:887853918665707621>','<:co:895440308257558529>']+aspiEmoji

altDanger = [65,70,70,70,75,75,80,80,85,85,90,90]

HEALRESISTCROIS, SHIELDREDUC = 0.2, 0.2
BASEHP_PLAYER, BASEHP_ENNEMI, BASEHP_SUMMON, BASEHP_BOSS = 150, 120, 100, 600
HPPERLVL_PLAYER, HPPERLVL_ENNEMI, HPPERLVL_SUMMON, HPPERLVL_BOSS = 20, 15, 10, 132

MELEE_END_CONVERT = 35
END_NEEDED_10_INDRES, MAX_END_10_INDRES = 145, 35
END_NEEDED_10_HEAL, MAX_END_10_HEAL = 150, 20

statEmbedFieldNames = ["__Liste des effets :__","__Statistiques :__","<:em:866459463568850954>","__Jauges :__","__Déployables :__","__Équipe Bleue :__","__Équipe Rouge :__"]

tablAchivNpcName = ["Alice","Clémence","Akira","Gwendoline","Hélène","Icealia","Shehisa","Powehi","Félicité","Sixtine","Hina","Julie","Krys","Lio","Liu","Liz","Lia","Iliana","Stella","Kiku","Kitsune","Ailill","Altikia","Klironovia","Lia Ex","Iliana prê.","Anna","Belle","Clémence Exaltée","Luna ex.","Clémence pos.","Céleste","Shushi"]
tablAchivNpcCode = ["alice","clemence","akira","gwen","helene","icea","sram","powehi","feli","sixtine","hina","julie","krys","lio","liu","liz","lia","light","stella","kiku1","momKitsune","ailill2","alty","klikli","liaEx","catEx","anna","belle","clemEx","luna","clemMem","celeste","shushi"]

tablIsNpcName = []
for a in tablAllAllies + tablVarAllies + ["Liu","Lia","Liz","Lio","Ailill","Kiku","Stella","Séréna","OctoTour","Kitsune","The Giant Enemy Spider","[[Spamton Neo](https://deltarune.fandom.com/wiki/Spamton)]","Nacialisla","Luna ex.","Clémence pos."]:
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

def dmgCalculator(caster, target, basePower, use, actionStat, danger, area, typeDmg = TYPE_DAMAGE, skillPercing = 0, ignoreEff = None):
    if caster.team == 0:
        danger = 100

    if use == HARMONIE:
        maxi, stats = -100, caster.allStats()
        for cmpt in range(0,7):
            if stats[cmpt] > maxi:
                maxi, use = stats[cmpt], cmpt 
    if use not in [FIXE,None]:
        enemyPercing, tarResi = caster.percing+skillPercing, target.resistance
        if ignoreEff != None:
            enemyPercing = getPenetration(caster.rawPercing-ignoreEff.percing)+skillPercing
            tarResi =  getResistante(target.rawResist-ignoreEff.resistance)
        resistFactor = (1-(min(95,tarResi*(1-(enemyPercing)/100))/100))
        lvlBonus = (1+(DMGBONUSPERLEVEL*caster.level))
        if lvlBonus > 2.5 and type(caster.char) not in [char,tmpAllie]:
            lvlBonus = 2.5
        elemBonus = caster.getElementalBonus(target=target,area=area,type=typeDmg)

        stat = caster.allStats()[use]
        if caster.aspiration in [BERSERK,POIDS_PLUME,TETE_BRULE,ENCHANTEUR,VIGILANT,PROTECTEUR,MASCOTTE,ASPI_NEUTRAL]:
            stat += int(caster.endurance * MELEE_END_CONVERT/100)

        if ignoreEff != None:
            stat = stat - ignoreEff.allStats()[use]

        dmg = round(basePower * (max(-65,stat+100-caster.actionStats()[actionStat]))/100 *(danger/100)*elemBonus*lvlBonus)
        if ignoreEff == None:
            target.stats.damageResisted += dmg - (dmg*resistFactor)

        logs = "> {0} [basePower] * ({1} [AtkStats] / 100) * {2} [dangerMul] * {3} [elemBonus] * {4} [lvlBonus]  * {5} [resistFactor]".format(
            basePower,caster.allStats()[use]+100-caster.actionStats()[actionStat],danger/100,elemBonus,lvlBonus,round(resistFactor,2))
        return max(1,round(dmg*resistFactor)), logs
    else:
        return basePower, "> Fixe"

def indirectDmgCalculator(caster, target, basePower, use, danger, area, useActionStat = ACT_INDIRECT):
    damage, logs = basePower, "FIXE"
    if use not in [None,FIXE,PURCENTAGE]:
        if use != HARMONIE:
            stat = caster.allStats()[use]-[caster.negativeHeal, caster.negativeShield, caster.negativeBoost, caster.negativeDirect, caster.negativeIndirect][useActionStat]
        else:
            stat = max(caster.allStats())

        if caster.aspiration in [BERSERK,POIDS_PLUME,TETE_BRULE,ENCHANTEUR,VIGILANT,PROTECTEUR,MASCOTTE,ASPI_NEUTRAL]:
            stat += int(caster.endurance * MELEE_END_CONVERT/100)

        effMultiplier = 100 + 5*int(not(caster.auto))
        for eff in caster.effects:
            if eff.effects.id == dmgUp.id:
                effMultiplier += eff.effects.power
            elif eff.effects.id in [dmgDown.id,indDealReducTmp.id]:
                effMultiplier -= eff.effects.power
        for eff in target.effects:
            if eff.effects.id in [vulne.id,kikuRaiseEff.id]:
                effMultiplier += eff.effects.power
            elif eff.effects.id == defenseUp.id:
                effMultiplier -= eff.effects.power
            elif eff.effects.inkResistance != 0:
                effMultiplier -= eff.effects.inkResistance

        effMultiplier -= min((target.endurance/END_NEEDED_10_INDRES*10),MAX_END_10_INDRES)

        if target.char.aspiration == MASCOTTE:
            effMultiplier -= 10

        effMultiplier = max(effMultiplier, 5)
        effMultiplier = min(effMultiplier, 200)

        if (use==MAGIE and target.char.npcTeam in [NPC_FAIRY]):
            effMultiplier += FAIRYMAGICRESIST

        dangerMul = [100, danger][caster.team == 1]
        lvlBonus = (1+(DMGBONUSPERLEVEL*caster.level))
        if lvlBonus > 2.5 and type(caster.char) not in [char,tmpAllie]:
            lvlBonus = 2.5
        damage = basePower * (1+(stat/100)) * (1-(min(95,target.resistance*(1-caster.percing/100))/100)) * lvlBonus * effMultiplier/100 * dangerMul/100
        logs = "{0} [basePower] * (1 + ( {1} [stats] / 100)) * {2} [targetResistance] * {3} [lvlBonus] * {4} [indDamMul] * {5} [dangerMul]".format(basePower,stat,round(1-(min(95,target.resistance*(1-caster.percing/100))/100),2),lvlBonus,effMultiplier/100,dangerMul/100)
    elif use in [PURCENTAGE]:
        damage = int(target.maxHp*basePower/100)
    return damage, logs

class timeline:
    """Classe de la timeline"""
    def __init__(self):
        self.timeline = []
        self.initTimeline = []
        self.begin = None
        entDict = {}

    def init(self,tablEntTeam : list,entDict):
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
        entDict = entDict

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

    def endOfTurn(self,tablEntTeam,tablAliveInvoc,entDict):
        timelineTempo = self.timeline
        actTurn = timelineTempo[0]

        timelineTempo.remove(actTurn)
        timelineTempo.append(actTurn)

        for ent in self.timeline[:]:
            if ent.hp <= 0 and type(ent.char) == invoc:
                inv = ent
                timelineTempo.remove(inv)
                inv.cell.on = None
                tablEntTeam[inv.team].remove(inv)
                tablAliveInvoc[inv.team] -= 1

        self.timeline = timelineTempo
        return tablEntTeam, tablAliveInvoc, entDict

    def insert(self,entBefore,entToInsert):
        found = False
        for cmpt in range(len(self.timeline)):
            if entBefore.id == self.timeline[cmpt].id and type(self.timeline[cmpt].char) not in [invoc, depl]:
                whereToInsert = cmpt+1
                break
        
        if not(found):
            whereToInsert = 1
        
        self.timeline.insert(whereToInsert,entToInsert)

def map(tablAllCells,bigMap,showArea:List[cell]=[],fromEnt=None,wanted=None,numberEmoji=None,fullArea=[],deplTabl=[]):
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
        if a.on != None and (numberEmoji == None or (len(numberEmoji)>0 and type(numberEmoji[0] != cell))):
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
        elif numberEmoji != None and a in numberEmoji:
            for cmpt in range(len(numberEmoji)):
                if a == numberEmoji[cmpt]:
                    temp = listNumberEmoji[cmpt]
                    break
        elif a.depl != None:
            temp = a.depl.char.icon[a.depl.team]
        else:
            for deplEnt in deplTabl:
                if a in deplEnt[2]:
                    temp = deplEnt[0].char.cellIcon[deplEnt[0].team]
                    break
        lines[a.y][a.x]=temp
    temp = ""
    for a in lines:
        for b in [0,1,2,3,4]:
            temp += f"{a[b]}|"
        temp += f"{a[b+1]}\n"
    return temp

def getHealAggro(caster,target, skillToUse : Union[skill,weapon],armor=False):
    if type(target.char) == invoc or target.hp <= 0 or target.hp >= target.maxHp:
        return -999
    else:
        prio = (1-(target.hp/target.maxHp))*100
        prio = prio * (1.2 - (0.1*target.char.weapon.range))                # If the entity is a melee, he is more important
        if not(target.auto):
            prio = prio * 1.1                                           # If the entity is a active player, he is a little more important, for reduce the use of the spoon

        if (skillToUse.type == TYPE_HEAL and (type(skillToUse) == classes.skill and skillToUse.cooldown >= 7) and target.hp/target.maxHp >= 0.7) or (skillToUse.type == TYPE_INDIRECT_HEAL and target.hp/target.maxHp <= 0.35):
            prio = prio * 0.7                                           # If the skill is a big direct heal and the entity is not low Hp or if the skill is a HoT and the entity is low Hp

        if not(armor):
            prio = prio * (1-(target.healResist/2/100))                             # If the entity have a big healing resist, he is less important

        incurValue, healAggroBonus = 0, 100
        for eff in target.effects:
            if eff.effects.id == incurable.id:
                incurValue = max(eff.effects.power,incurValue)
            elif eff.effects.id == undeadEff2.id:
                healAggroBonus += undeadEff2.power

            if eff.effects.name.startswith("⚠️ Cible - ") and armor:
                prio += 35
        prio = prio * (1-(incurValue/2/100)) * (healAggroBonus/100)                              # Same with the healing reduce effects

        if (not(armor) and (caster.char.charSettings["healTarget"] == CHARSET_HEALTARGET_DPT and target.char.aspiration in dptAspi) or (caster.char.charSettings["healTarget"] == CHARSET_HEALTARGET_BUFF and target.char.aspiration in boostAspi) or (caster.char.charSettings["healTarget"] == CHARSET_HEALTARGET_HEAL and target.char.aspiration in healAspi+armorAspi) or caster.char.charSettings["healTarget"] == CHARSET_HEALTARGET_MELEE and len(target.cell.getEntityOnArea(area=AREA_CIRCLE_2,team=caster.team,wanted=ENEMIES,directTarget=False,fromCell=target.cell)) >= 2) or (armor and (caster.char.charSettings["armorTarget"] == CHARSET_ARMORTARGET_DPT and target.char.aspiration in dptAspi) or (caster.char.charSettings["armorTarget"] == CHARSET_ARMORTARGET_BUFF and target.char.aspiration in boostAspi) or (caster.char.charSettings["armorTarget"] == CHARSET_ARMORTARGET_HEAL and target.char.aspiration in armorAspi+healAspi) or caster.char.charSettings["armorTarget"] == CHARSET_ARMORTARGET_MELEE and len(target.cell.getEntityOnArea(area=AREA_CIRCLE_2,team=caster.team,wanted=ENEMIES,directTarget=False,fromCell=target.cell)) >= 2):
            prio = prio * 1.35

        if (caster.char.npcTeam == NPC_KITSUNE and target.char.npcTeam == NPC_GOLEM) or (caster.char.npcTeam == NPC_DEMON and target.char.npcTeam == NPC_HOLY) or (caster.char.npcTeam == NPC_HOLY and target.char.npcTeam in [NPC_UNDEAD, NPC_DEMON]):
            prio = prio * 0.6
        return prio

def getHealTarget(caster,tablTeam : list, skillToUse : skill, armor=False):
    if len(tablTeam) == 1:
        return tablTeam[0]
    elif len(tablTeam) < 1:
        raise AttributeError("tablTeam is empty")
    
    temp = tablTeam
    temp.sort(key=lambda funnyTempVarName:getHealAggro(caster,funnyTempVarName,skillToUse, armor),reverse=True)
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
    for eff in actTurn.effects:
        if eff.effects.id == dmgUp.id:
            dmgUpCount += eff.effects.power
        elif eff.effects.id == dmgDown.id:
            dmgUpCount -= eff.effects.power
        elif eff.effects.id == defenseUp.id:
            defenseUpCount += eff.effects.power
        elif eff.effects.id == vulne.id:
            defenseUpCount -= eff.effects.power
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

AGI_REQUIERD_FOR_30_CRIT = 180
PRE_REQUIERD_FOR_30_CRIT = 180

def probCritDmg(ent) -> int:
    return (ent.agility/(AGI_REQUIERD_FOR_30_CRIT/50*max(15,ent.level)))*30 + (ent.precision/(PRE_REQUIERD_FOR_30_CRIT/50*max(15,ent.level)))*30 + ent.critical

END_REQUIERD_FOR_30_CRIT = 350
def probCritHeal(ent,target) -> int:
    return (ent.precision/(PRE_REQUIERD_FOR_30_CRIT/50*max(15,ent.level)))*30 + (target.endurance/(END_REQUIERD_FOR_30_CRIT/50*max(15,ent.level)))*30 + ent.critical

def calHealPower(ent,target,power,secElemMul,statUse,useActionStats,danger):
    if ent.team == 0:
        danger = 100
    vigilBonus = [1,1.1][target.char.aspiration == VIGILANT]

    if ent.aspiration in [BERSERK,POIDS_PLUME,TETE_BRULE,ENCHANTEUR,VIGILANT,PROTECTEUR,MASCOTTE,ASPI_NEUTRAL]:
        statUse += int(ent.endurance * MELEE_END_CONVERT/100)

    END_NEEDED_10_HEAL, MAX_END_10_HEAL
    endHealReciveBonus = min((target.endurance/END_NEEDED_10_HEAL*10),MAX_END_10_HEAL)
    return round(power * secElemMul * (1+(max(-65,statUse-(ent.actionStats()[useActionStats])))/100)*(1+endHealReciveBonus/100)*ent.valueBoost(target = target,heal=True)*ent.getElementalBonus(target,area = AREA_MONO,type = TYPE_HEAL) * danger/100 * vigilBonus)

def getBuffAggro(caster,target,effect:classes.effect):
    if type(effect) != classes.effect or (caster == target and effect.turnInit < 2):
        return 0
    toReturn, targetStats, maxEffStats, effStats = 0, target.allStats(), [], effect.allStats()
    for cmpt in range(len(effStats)):
        maxEffStats.append([cmpt,effStats[cmpt]])

    if effect.block > 0 or effect.inkResistance > 0:
        maxEffStats[ENDURANCE][1] += 10
    if effect.dodge > 0 or effect.counterOnDodge > 0:
        maxEffStats[ENDURANCE][1] += 5
        maxEffStats[AGILITY][1] += 5
    if effect.id == dmgUp.id:
        maxEffStats[STRENGTH][1] += 5
        maxEffStats[MAGIE][1] += 5
    if effect.id == healDoneBonus.id:
        maxEffStats[CHARISMA][1] += 1

    maxEffStats.sort(key=lambda ballerine: ballerine[1], reverse=True)
    BASESTATVALUE = 300
    toReturn = targetStats[maxEffStats[0][0]]/BASESTATVALUE

    BASEDPTVALUE = 10000
    if caster.char.charSettings["buffTarget"] == CHARSET_BUFFTARGET_HIGHDPT and target.char.aspiration in dptAspi:
        toReturn = toReturn * (1+(target.stats.damageDeal/BASEDPTVALUE))
    elif caster.char.charSettings["buffTarget"] == CHARSET_BUFFTARGET_LOWDPT and target.char.aspiration in dptAspi:
        toReturn = toReturn * (1+(BASEDPTVALUE-target.stats.damageDeal/BASEDPTVALUE))
    elif caster.char.charSettings["buffTarget"] == CHARSET_BUFFTARGET_HASULT and target.char.aspiration in dptAspi:
        bigSkillMul = 1
        for cmpt in range(len(target.char.skills)):
            if type(target.char.skills[cmpt]) == skill and target.cooldowns[cmpt] == 0 and (target.char.skills[cmpt].cooldown >= 7 or target.char.skills[cmpt].ultimate):
                bigSkillMul += 0.25
        toReturn = toReturn * bigSkillMul

    return toReturn 

def getRaiseAggro(caster,target):
    if not(target.auto):
        return 10
    if caster.char.charSettings["raiseTarget"] == CHARSET_RAISETARGET_DEFAULT or (caster.char.charSettings["raiseTarget"] == CHARSET_RAISETARGET_DMG and target.char.aspiration in dptAspi) or caster.char.charSettings["raiseTarget"] == CHARSET_RAISETARGET_BUFF and target.char.aspiration in boostAspi or caster.char.charSettings["raiseTarget"] == CHARSET_RAISETARGET_HEAL and target.char.aspiration in healAspi+armorAspi:
        return 1

    return 0

async def getResultScreen(bot,ent) -> interactions.Embed:
    stats = ent.stats
    userIcon = await ent.getIcon(bot)
    descri = f"{ent.char.weapon.emoji}"

    if type(ent.char) in [char,tmpAllie]:
        descri += f" | {ent.char.stuff[0].emoji} {ent.char.stuff[1].emoji} {ent.char.stuff[2].emoji}"

    skillTmp = ""
    for a in ent.char.skills:
        if type(a) == skill:
            if skillTmp == "":
                skillTmp = " |"
            skillTmp += " {0}".format(a.emoji)

    descri+=skillTmp
    statsEm = interactions.Embed(title = "__Statistiques de {0} {1}__".format(userIcon,unhyperlink(ent.name)),color=ent.char.color,description=descri)

    precisePurcent,dodgePurcent,critPurcent = "-","-","-"
    if stats.totalNumberShot > 0:
        precisePurcent = str(round(stats.shootHited/stats.totalNumberShot*100)) +"%"
        critPurcent = str(round(stats.crits/stats.totalNumberShot*100)) +"%"
    if stats.numberAttacked > 0:
        dodgePurcent = str(round(stats.dodge/stats.numberAttacked*100)) +"%"

    statsCatNames = ["__Statistiques offensives <:sg:968479144293855252> :__","<:em:866459463568850954>\n__Statistiques défensives <:re:989529323063107605> :__","<:em:866459463568850954>\n__Statistiques de soutiens <:fF:956715234842791937>  :__","<:em:866459463568850954>\n__Autres :__"]

    pvRestant = "{0} ({1}%)".format(highlight(separeUnit(max(ent.hp,0))),round(max(ent.hp,0)/ent.maxHp*100,2))
    allStatsTabl = [
        {
            "Dégâts totaux infligés":ent.stats.damageDeal,
            "> - Dégâts indirects":ent.stats.indirectDamageDeal,
            "> - Dégâts sous boost":ent.stats.underBoost,
            "> - Dégâts sur armure":int(ent.stats.damageOnShield),
            "> - Dégâts (Invoc./Depl.)":ent.stats.summonDmg,
            "Coups de grâce":ent.stats.ennemiKill,
            "Précision":precisePurcent,
            "Coups critiques":critPurcent
        },
        {
            "Tours survécus":ent.stats.survival,
            "Dégâts reçus":ent.stats.damageRecived,
            "> - Dégâts réduits sur soi":int(ent.stats.damageResisted),
            "> - Dégâts sur armure reçus":ent.stats.damageProtected,
            "> - Dégâts bloqués":ent.stats.damageBlocks,
            "> - Soins reçus":ent.stats.healingRecived,
            "Taux d'esquive":dodgePurcent,
            "Taux de blocage":"{0}%".format(round(ent.stats.blockCount/max(ent.stats.numberAttacked,1)*100))
        },
        {
            "{0} réamimés".format(["Combattants","Alliés"][not(ent.isNpc("Kiku"))]):ent.stats.allieResurected,
            "Soins effectués":ent.stats.heals,
            "> - Vol de vie":ent.stats.lifeSteal,
            "Armures données":ent.stats.shieldGived,
            "> - Soins / Armures (Invoc./Depl.)":ent.stats.summonHeal,
            "> - Dégâts protégés":ent.stats.armoredDamage,
            "Points Supports":ent.stats.damageBoosted+ent.stats.damageDodged,
            "> - Dégâts augmentés":ent.stats.damageBoosted,
            "> - Dégâts réduits":ent.stats.damageDodged,
            "> - Soins augmentés":ent.stats.healIncreased,
            "> - Soins réduits":ent.stats.healReduced,
            "> - Points Supports (Invocation)":ent.stats.summonBoost,
            "Taux Critique (soins et armure)":"{0}%".format(round(ent.stats.critHeal/max(ent.stats.nbHeal,1)*100))
        },
        {
            "Tours passés":ent.stats.turnSkipped,
            "Dégâts sur soi-même":ent.stats.selfBurn,
            "PV restants":pvRestant,
            "Invocation / Déployables invoqués":ent.stats.nbSummon
        }
    ]

    for cmpt in range(len(statsCatNames)):
        try:
            catDict = allStatsTabl[cmpt]
            tempDesc = ""
            for catName, catValue in catDict.items():
                if not(catName.startswith("> -")):
                    tempDesc += "__{0}__ : {1}\n".format(catName,[highlight(separeUnit(catValue)),catValue][type(catValue)==str])
                elif catValue > 0:
                    tempDesc += "{0} : {1}\n".format(catName,highlight(separeUnit(catValue)))
            statsEm.add_field(name=statsCatNames[cmpt],value=tempDesc,inline=False)
        except:
            print_exc()
    statsEm.set_thumbnail(url="https://cdn.discordapp.com/emojis/{0}.png".format(getEmojiObject(userIcon).id))
    return statsEm

class cellPath:
    def __init__(self,startCell,toTarget,tabl):
        self.cell = startCell
        self.target = toTarget
        self.path = tabl
        self.allReadyCheck = []
        self.movingAway = 0
