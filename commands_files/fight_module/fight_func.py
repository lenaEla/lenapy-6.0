import random, copy, interactions, quickchart, aiohttp
from commands_files.fight_module.fight_class import *
from commands_files.fight_module.fight_const import *


def getPartnerValue(user : classes.char):
    if user.aspiration in [BERSERK,POIDS_PLUME,TETE_BRULEE,ENCHANTEUR]:
        return 10 + random.randint(-3,3)
    elif user.aspiration in [PROTECTEUR,ATTENTIF]:
        return 8 + random.randint(-3,3)
    elif user.aspiration in [OBSERVATEUR,VIGILANT,MAGE,SORCELER]:
        return 6 + random.randint(-3,3)
    else:
        return 4 + random.randint(-3,3)

def dmgCalculator(caster, target, basePower, use, actionStat, danger, area, typeDmg = TYPE_DAMAGE, skillPercing = 0, ignoreEff = None):
    if caster.team == 0: danger = 100

    dmg, dictContributor, baseStat, isMelee, resistedDmg = 0, {}, caster.baseStats, caster.aspiration in meleeAspi, 0
    if use == HARMONIE:
        tmpTabl = [[0,baseStat[0]],[1,baseStat[1]],[2,baseStat[2]],[3,baseStat[3]],[4,baseStat[4]],[5,baseStat[5]],[6,baseStat[6]]]
        tmpTabl.sort(key=lambda ballerine: ballerine[1], reverse=True)
        use = tmpTabl[0][0]

    if use not in [FIXE,None,MISSING_HP,PURCENTAGE]:
        statBucket, lvlBonus, elemBonus = baseStat[use]-baseStat[actionStat+ACT_HEAL_FULL], BASEDAMAGEMUL+(DMGBONUSPERLEVEL*caster.level), caster.getElementalBonus(target=target,area=area,type=typeDmg) 
        if isMelee: statBucket += int(baseStat[ENDURANCE] * MELEE_END_CONVERT/100)
        if caster.char.__class__ == classes.octarien: lvlBonus = min(lvlBonus,BASEDAMAGEMUL+(DMGBONUSPERLEVEL*MAXLEVEL))
        dmg = basePower * max(-65,statBucket)/100 *(danger/100)*lvlBonus*elemBonus

        listReducedEnt, listAddEnt = [], []
        for eff in caster.effects:
            effStats = eff.allStats()
            if effStats[use] != 0 or (isMelee and effStats[ENDURANCE] != 0):
                statBucket1 = effStats[use] + [0, int(effStats[ENDURANCE]* MELEE_END_CONVERT/100)][isMelee]
                tmpDmg = basePower * max(-65,statBucket1)/100 *(danger/100)*lvlBonus*elemBonus
                if eff.caster not in dictContributor.keys(): dictContributor[eff.caster] = tmpDmg
                else: dictContributor[eff.caster] += tmpDmg
                dmg += tmpDmg
            if eff.percing > 0:
                listAddEnt.append(eff.caster)
            elif eff.percing < 0:
                listReducedEnt.append(eff.caster)

        rawDmg = dmg
        casterPerc, targResist = getPenetration(baseStat[PERCING]+skillPercing), getResistante(target.baseStats[RESISTANCE])
        resistFactor = (between(targResist*(1-(casterPerc/100)),95,0)/100)
        rowResistedDmg = dmg*resistFactor

        for eff in target.effects:
            if eff.resistance > 0:
                listReducedEnt.append(eff.caster)
            elif eff.resistance < 0:
                listAddEnt.append(eff.caster)

        casterPerc, targResist = getPenetration(caster.percing+skillPercing), getResistante(target.resistance)
        resistFactor = between(targResist*(1-(casterPerc/100)),95,0)/100
        resistedDmg = dmg*resistFactor

        if resistedDmg > rowResistedDmg:
            lenReducedEnt = len(listReducedEnt)
            for ent in listReducedEnt:
                if ent not in dictContributor.keys():
                    dictContributor[ent] = (rowResistedDmg-resistedDmg) / lenReducedEnt
                else:
                    dictContributor[ent] += (rowResistedDmg-resistedDmg) / lenReducedEnt
        elif resistedDmg < rowResistedDmg:
            lenAddEnt = len(listAddEnt)
            for ent in listAddEnt:
                if ent not in dictContributor.keys():
                    dictContributor[ent] = (resistedDmg-rowResistedDmg) / lenAddEnt
                else:
                    dictContributor[ent] += (resistedDmg-rowResistedDmg) / lenAddEnt

        dmg = max(1,int(dmg-resistedDmg))
        logs = "> {0} [basePower] * ({1} [AtkStats] / 100) * {2} [dangerMul] * {3} [elemBonus] * {4} [lvlBonus]  * {5} [resistFactor]".format(basePower,statBucket,danger/100,elemBonus,lvlBonus,round(resistFactor,2))
        return dmg, logs, dictContributor, resistedDmg
    elif use == MISSING_HP: return int((target.maxHp-target.hp)*basePower/100), "> Missing HP", {}, 0
    elif use == PURCENTAGE: return int(target.maxHp*basePower/100), "> % max hp", {}, 0
    else: return basePower, "> Fixe", {}, 0

def indirectDmgCalculator(caster, target, basePower, use, danger, area, useActionStat = ACT_INDIRECT):
    damage, logs = basePower, "FIXE"
    if use not in [None,FIXE,PURCENTAGE,MISSING_HP]:
        if use != HARMONIE: stat = caster.allStats()[use]-[caster.negativeHeal, caster.negativeShield, caster.negativeBoost, caster.negativeDirect, caster.negativeIndirect][useActionStat]
        else: stat = max(caster.allStats())-min(caster.negativeHeal, caster.negativeShield, caster.negativeBoost, caster.negativeDirect, caster.negativeIndirect)
        if caster.aspiration in [BERSERK,POIDS_PLUME,TETE_BRULEE,ENCHANTEUR,VIGILANT,PROTECTEUR,MASCOTTE,ASPI_NEUTRAL]: stat += int(caster.endurance * MELEE_END_CONVERT/100)

        effMultiplier, dmgMul, elementMul = 100 + 5*int(not(caster.auto)), 1, 1
        if caster.char.element in [ELEMENT_DARKNESS,ELEMENT_TIME,ELEMENT_UNIVERSALIS,ELEMENT_FIRE,ELEMENT_AIR]:
            elementMul += {ELEMENT_DARKNESS:DARKDMGBUFF*2,ELEMENT_TIME:TIMEDMGBUFF,ELEMENT_UNIVERSALIS:DARKDMGBUFF*2,ELEMENT_FIRE:AREADMGBUFF,ELEMENT_AIR:AREADMGBUFF}[caster.char.element]/100
        for eff in caster.effects:
            if eff.effects.id == dmgUp.id:
                effMultiplier += eff.effects.power
        for eff in target.effects:
            if eff.effects.id in [vulne.id]:
                dmgMul = dmgMul*((100+eff.effects.power)/100)
            elif eff.effects.id == defenseUp.id:
                dmgMul = dmgMul*((100-eff.effects.power)/100)
            elif eff.effects.inkResistance != 0:
                dmgMul = dmgMul*((100-eff.effects.inkResistance)/100)

        tmpChip = getChip("Dégâts indirects augmentés")
        if tmpChip != None and tmpChip.id in caster.char.equippedChips:
            dmgMul += caster.char.chipInventory[tmpChip.id].power/100
        effMultiplier -= min((target.endurance/END_NEEDED_10_INDRES*10),MAX_END_10_INDRES)

        if target.char.aspiration == MASCOTTE:
            effMultiplier -= 10

        effMultiplier = max(effMultiplier, 5)
        effMultiplier = min(effMultiplier, 200)

        if (use==MAGIE and target.char.npcTeam in [NPC_FAIRY]):
            effMultiplier += FAIRYMAGICRESIST

        effMultiplier = effMultiplier * elementMul

        dangerMul = [100, danger][caster.team == 1]
        lvlBonus = (1+(DMGBONUSPERLEVEL*caster.level))
        if lvlBonus > 2.5 and type(caster.char) not in [char,tmpAllie]:
            lvlBonus = 2.5
        damage = basePower * (1+(stat/100)) * (1-(min(95,target.resistance*(1-caster.percing/100))/100)) * lvlBonus * effMultiplier/100 * dmgMul * dangerMul/100
        logs = "{0} [basePower] * (1 + ( {1} [stats] / 100)) * {2} [targetResistance] * {3} [lvlBonus] * {4} [indDamMul] * {5} [dangerMul]".format(basePower,stat,round(1-(min(95,target.resistance*(1-caster.percing/100))/100),2),lvlBonus,effMultiplier/100,dangerMul/100)
    elif use in [PURCENTAGE]:
        damage = int(target.maxHp*basePower/100)
    elif use in [MISSING_HP]:
        damage = int((target.maxHp-target.hp)*basePower/100)
        try:
            if target.char.standAlone:
                damage = min(int(target.maxHp)*0.05,damage)
        except:
            pass
    return damage, logs

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
    toReturn, cmpt = actTurn.quickEffectIcons()+["Trans. : ",""][LBBars[actTurn.team][0]<=0], 0
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

def probCritDmg(ent) -> int:
    return (ent.agility/(AGI_REQUIERD_FOR_30_CRIT/50*max(15,ent.level)))*30 + (ent.precision/(PRE_REQUIERD_FOR_30_CRIT/50*max(15,ent.level)))*30 + ent.critical

def probCritHeal(ent,target) -> int:
    return (ent.precision/((PRE_REQUIERD_FOR_30_CRIT-50)/50*max(15,ent.level)))*30 + (target.endurance/(END_REQUIERD_FOR_30_CRIT/50*max(15,ent.level)))*30 + ent.critical

def calHealPower(ent,target,power,secElemMul,statUse,useActionStats,danger):
    if ent.team == 0: danger = 100
    vigilBonus = [1,1.1][target.char.aspiration == VIGILANT]

    if ent.aspiration in [BERSERK,POIDS_PLUME,TETE_BRULEE,ENCHANTEUR,VIGILANT,PROTECTEUR,MASCOTTE,ASPI_NEUTRAL]: statUse += int(ent.endurance * MELEE_END_CONVERT/100)

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

    if type(ent.char) in [char,tmpAllie]: descri += f" | {ent.char.stuff[0].emoji} {ent.char.stuff[1].emoji} {ent.char.stuff[2].emoji}"

    skillTmp = ""
    for a in ent.char.skills:
        if type(a) == skill:

            skillTmp += "{0} ".format(a.emoji)
    if skillTmp != "":
        skillTmp = " | "+skillTmp

    chipTmp = ""
    for tmpChipId in ent.char.equippedChips:
        tmpChip = getChip(tmpChipId)
        if tmpChip != None:
            chipTmp += tmpChip.emoji + " "
    if chipTmp != "":
        chipTmp = "|\n "+chipTmp

    descri+=skillTmp+chipTmp
    statsEm = interactions.Embed(title = "__Statistiques de {0} {1}__".format(userIcon,unhyperlink(ent.name)),color=ent.char.color,description=descri)

    precisePurcent,dodgePurcent,critPurcent = "-","-","-"
    if stats.totalNumberShot > 0:
        precisePurcent = str(round(stats.shootHited/stats.totalNumberShot*100)) +"%"
        critPurcent = str(round(stats.crits/stats.totalNumberShot*100)) +"%"
    if stats.numberAttacked > 0:
        dodgePurcent = str(round(stats.dodge/stats.numberAttacked*100)) +"%"

    statsCatNames = ["__Statistiques offensives <:sg:968479144293855252> :__","<:em:866459463568850954>\n__Statistiques défensives <:re:989529323063107605> :__","<:em:866459463568850954>\n__Statistiques de soutiens <:fF:956715234842791937>  :__","<:em:866459463568850954>\n__Autres :__"]

    pvRestant = "{0} / {2} ({1}%)".format(highlight(separeUnit(max(ent.hp,0))),round(max(ent.hp,0)/ent.maxHp*100,2),separeUnit(ent.maxHp))
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
            "Soins effectués":int(ent.stats.heals),
            "> - Vol de vie":ent.stats.lifeSteal,
            "Armures données":ent.stats.shieldGived,
            "> - Soins / Armures (Invoc./Depl.)":ent.stats.summonHeal,
            "> - Dégâts protégés":ent.stats.armoredDamage,
            "Points Supports":ent.stats.damageBoosted+ent.stats.damageDodged,
            "> - Dégâts augmentés":int(ent.stats.damageBoosted),
            "> - Dégâts réduits":ent.stats.damageDodged,
            "> - Soins augmentés":ent.stats.healIncreased,
            "> - Soins réduits":ent.stats.healReduced,
            "> - Points Supports (Invocation)":ent.stats.summonBoost,
            "> - Dégâts redirigés": ent.stats.redirectedDamage,
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

def formatKnockBack(listResult:List[dict], listEnt:List, knockbackPower: int) -> str:
    allDict, listStuns, returnMsg = {}, {}, ""
    tmpList, tmpStr = [], ""
    for tmpResult in listResult:
        tmpList.append(tmpResult[0])
        tmpStr += tmpResult[1]
    
    listResult = tmpList
    
    for resultDict in listResult:
        for ent, damage in resultDict.items():
            try:
                allDict[ent][0], allDict[ent][1] = allDict[ent][0]+damage[0], allDict[ent][1]+damage[1]
                listStuns[ent] = listStuns[ent]+damage[2]
            except KeyError:
                allDict[ent] = [damage[0],damage[1]]
                listStuns[ent] = damage[2]

    for ent in listEnt:
        returnMsg += "__{0}__".format(ent.name)
        if len(listEnt) > 2:
            if ent not in listEnt[-2:]:
                returnMsg += ", "
            elif ent == listEnt[-2]:
                returnMsg += " et "
        elif ent.id != listEnt[-1].id:
            returnMsg += " et "

    returnMsg += " {0} repoussé{1} de {2} case{3}".format(["est","sont"][len(listEnt)>1],["","s"][len(listEnt)>1],knockbackPower,["","s"][knockbackPower>1])

    for ent, values in allDict.items():
        returnMsg += "\n{0} → ".format(ent.icon)
        for ent2 in values[0]:
            if ent2.icon not in returnMsg:
                returnMsg += ent2.icon
        sumation = 0
        for damage in values[1]:
            sumation += damage
        returnMsg += " -≈ {0} PV".format(round(sumation/len(values[1])))
        try:
            if (len(listStuns[ent])) > 0:
                returnMsg += "\n{0} → ".format(ent.icon)
                for ent2 in listStuns[ent]:
                    returnMsg += ent2.icon
                returnMsg += " + {0} __{1}__".format(lightStun.emoji[0][ent.team],lightStun.name)
        except KeyError:
            pass

    return returnMsg + "\n"

def calShieldValue(caster,target,shieldPower,stat,turn,dangerVal=100,actStat=ACT_SHIELD):
    elemMul = 1
    if caster.char.element in [ELEMENT_LIGHT,ELEMENT_EARTH,ELEMENT_UNIVERSALIS]:
        elemMul += {ELEMENT_LIGHT:LIGHTHEALBUFF,ELEMENT_EARTH:AREADMGBUFF,ELEMENT_UNIVERSALIS:LIGHTHEALBUFF}[caster.char.element]/100

    value, critMsg = shieldPower * elemMul, ""

    friablility = max(1-(turn / 30),0.1)                   # Reduct over time
    if actStat == None:
        actStat = ACT_SHIELD

    dangerBoost = [1,dangerVal/100][caster.team]

    if stat not in [None,FIXE,PURCENTAGE,MISSING_HP]:   # Classical armor effect
        if stat == HARMONIE:
            maxi = -100
            for randomVar in caster.allStats():
                maxi = max(maxi,randomVar)
            stati = maxi
        else:
            stati = caster.allStats()[stat]

        if caster.aspiration in [BERSERK,POIDS_PLUME,TETE_BRULEE,ENCHANTEUR,VIGILANT,PROTECTEUR,MASCOTTE,ASPI_NEUTRAL]:
            stati += int(caster.endurance * MELEE_END_CONVERT/100)
        value = round(value * caster.valueBoost(target=target,armor=True) * (1+(stati-caster.actionStats()[actStat])/100) * (1+min(target.endurance/END_NEEDED_10_HEAL*10,MAX_END_10_HEAL)/100) * dangerBoost * (1 - (ARMORMALUSATLVL0/100) + (ARMORLBONUSPERLEVEL*caster.level)))

        critRate = probCritHeal(caster,target)
        if random.randint(0,99) < critRate:
            critBonus = 1.25 + caster.critHealUp/100
            if critRate > 100:
                critBonus = critBonus * critRate/100
            value = int(value*critBonus)
            caster.stats.critHeal += 1
            critMsg += " !"
        caster.stats.nbHeal += 1
    elif stat == PURCENTAGE:
        value = round(target.maxHp*shieldPower/100)
    elif stat == MISSING_HP:
        value = round((target.maxHp-target.hp)*shieldPower/100)
    else:                                                           # Fixe armor effect
        value = round(shieldPower)

    armorGetMul = 1
    for eff in caster.effects:
        if eff.effects.id == healDoneBonus.id:
            armorGetMul = armorGetMul * ((100+eff.effects.power)/100)
    for eff in target.effects:
        if eff.effects.id == absEff.id:
            armorGetMul = armorGetMul * ((100+eff.effects.power)/100)
        elif eff.effects.id == armorGetMalus.id:
            armorGetMul = armorGetMul * (1-(eff.effects.power/100))

    value = int(value*armorGetMul*friablility)

    return (value,critMsg)
