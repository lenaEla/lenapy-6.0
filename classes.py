"""
base classes module
Here are grouped up the bases classes of the bot, and some very basic functions
"""
import emoji,pathlib,copy,random
from constantes import *
from typing import List, Union

absPath = str(pathlib.Path(__file__).parent.resolve())

class statTabl:
    """
        A class that is use to store the entity's stats for the post fight medals and inflate their ego\n
        - Attributs :
            - damageDeal : The total amount of damage deal
            - indirectDamageDeam : The amount of damage deal with indirect attacks. Include into ``damageDeal``
            - ennemiKill : The number of entity killed by the entity. Them self include
            - allieResurected : The number of allies raised by the entity
            - shootHited : The number of shot that hit the target
            - totalNumberShot : The number of shot shoot by the entity
            - dodge : The number of attack dodges by the entity
            - numberAttacked : The number of times the entity has been attacked
            - damageRecived : The number of damage the entity has teken
            - heals : The number of HP the entity has heal. Do not count overhealth
            - crits : The number of time the entity has done a critical hit
            - survival : The number of turn the entity has stayed alive
            - damageOnShield : The number of damage the entity has done on opponent's armor
            - damageBoosted : The number of damage another entity has done with a entity's boost effect
            - damageDogded : The number of damage another entity has reduce with a entity's boost effect
            - shieldGiven : The number of Armor HP gave by the entity
            - estialba : The number of damage the entity have done with a "Estialba's poison" effect
            - bleeding : The number of damage the entity have done with a "Bleeding" effect
            - underBoost : The number of damage the entity have done with a another entity's boost effect
            - selfBurn : The number of damage the entity have done on him-self
    """
    def __init__(self):
        self.damageDeal = 0
        self.indirectDamageDeal = 0
        self.ennemiKill = 0
        self.allieResurected = 0
        self.shootHited = 0
        self.totalNumberShot = 0
        self.dodge = 0
        self.numberAttacked = 0
        self.damageRecived = 0
        self.heals = 0
        self.crits = 0
        self.survival = 0
        self.damageOnShield = 0
        self.damageBoosted = 0
        self.damageDogded = 0
        self.shieldGived = 0
        self.estialba = 0
        self.bleeding = 0
        self.underBoost = 0
        self.selfBurn = 0
        self.headnt = False
        self.friendlyfire = 0
        self.fullskip, self.turnSkipped = True, 0
        self.armoredDamage = 0
        self.damageBlocks,self.damageResisted,self.healReduced, self.healIncreased = 0, 0, 0, 0
        self.maxHpReduced, self.blockCount, self.nbHeal, self.critHeal = 0, 0, 0, 0
        self.sufferingFromSucess, self.lauthingAtTheFaceOfDeath = False, False

class option:
    """Very basic class. Only use in the "Select Option" window of manuals fights"""
    def __init__(self,name,emoji):
        self.name = name
        self.emoji = emoji

class effect:
    """The class for all skill's none instants effects and passive abilities from weapons and gears"""
    def __init__(self,name,id,stat=None,strength=0,endurance=0,charisma=0,agility=0,precision=0,intelligence=0,magie=0,resistance=0,percing=0,critical=0,emoji=None,overhealth = 0,redirection = 0,reject=None,description = "Pas de description",turnInit = 1,immunity=False,trigger=TRIGGER_PASSIVE,callOnTrigger = None,silent = False,power:int = 0,lvl = 1,type = TYPE_BOOST,ignoreImmunity = False,area=AREA_MONO,unclearable = False,stun=False,stackable=False,replique=None,translucide=False,untargetable=False,invisible=False,aggro=0,absolutShield = False, lightShield = False,onDeclancher = False,inkResistance=0,dmgUp = 0, critDmgUp = 0, healUp = 0, critHealUp = 0, block=0, jaugeValue:Union[list,None]=None, denieWeap = False):
        """rtfm"""
        self.name = name                    # Name of the effect
        if replique != None:
            self.name = name.format(replicaName=replique.name)
        self.id = id                        # The id. 2 characters
        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie,self.resistance,self.percing,self.critical= strength,endurance,charisma,agility,precision,intelligence,magie,resistance,percing,critical
        self.overhealth = overhealth        # Base shield power
        self.redirection = redirection      # Damage redirection ratio. Unuse yet
        self.block = block
        self.reject = copy.deepcopy(reject)                # A list of the rejected effects
        self.description = description.format(power,power//2)      # A (quick) description of the effect
        self.turnInit = turnInit            # How many turn does the effect stay ?
        self.stat = stat                    # Wich stat is use by the effect ?
        if (overhealth > 0 or redirection > 0) and trigger==TRIGGER_PASSIVE:
            self.trigger:int = TRIGGER_DAMAGE   # If the effect give armor, he triggers automatiquely on damage
        else:
            self.trigger:int = trigger          # When does the effect triggers ?
        self.immunity:bool = immunity            # Does the effect give a immunity ?
        self.callOnTrigger = callOnTrigger  # A list of effect given when the first one trigger
        self.silent:bool = silent                # Do the effect is showed in the fight ?
        self.power:int = power                  # The base power for heals and indirect damages
        self.lvl:int = lvl                      # How many times can the effect trigger ?
        self.type:int = type                    # The type of the effect
        self.ignoreImmunity:bool = ignoreImmunity    # Does the damage of this effect ignore immunities ?
        self.area=area                      # The area of effect of the effect
        self.unclearable:bool = unclearable      # Does the effect is unclearable ?
        self.stun:bool = stun                    # Does the effect is a stun effect ?
        self.stackable:bool = stackable          # Does the effect is stackable ?
        self.replica:Union[None,skill] = replique             # Does the effect is a replica of a skill ?
        self.translucide:bool = translucide      # Does the effect make the entity translucide ?
        self.untargetable:bool = untargetable    # Does the effect make the entity untargetable ?
        self.invisible:bool = invisible
        self.aggro:int = aggro
        self.lightShield:bool = lightShield
        self.absolutShield:bool = absolutShield
        self.onDeclancher:bool = onDeclancher
        self.inkResistance = inkResistance
        self.dmgUp, self.critDmgUp, self.healUp, self.critHealUp, self.jaugeValue, self.denieWeap = dmgUp, critDmgUp, healUp, critHealUp, jaugeValue, denieWeap

        if self.reject != None and self.id in self.reject:
            self.reject.remove(self.id)

        if emoji == None and self.replica != None:
            self.emoji = self.replica.emoji
        if emoji == None:
            if self.inkResistance > 0:
                self.emoji=[['<:inkResB:921486005008216094>','<:inkResR:921486021265354814>'],['<:inkResB:921486005008216094>','<:inkResR:921486021265354814>'],['<:inkResB:921486005008216094>','<:inkResR:921486021265354814>']]
            elif self.type in [TYPE_BOOST]:
                self.emoji=[['<:i1b:866828199156252682>','<:ink2buff:866828277171093504>'],['<:o1b:866828236724895764>','<:oct2buff:866828319528583198>'],['<:octarianbuff:866828373345959996>','<:octarianbuff:866828373345959996>']]
            elif self.type in [TYPE_MALUS]:
                self.emoji=[['<:ink1debuff:866828217939263548>','<:ink2debuff:866828296833466408>' ],['<:oct1debuff:866828253695705108>','<:oct2debuff:866828340470874142>'],['<:octariandebuff:866828390853247006>','<:octariandebuff:866828390853247006>']]
            elif self.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]:
                self.emoji=[["<:ikadamage1:895723391212978207>","<:ikadamage2:895723465389264897>"],["<:takodamage1:895723442177982516>","<:takodamage1:895723496196415508>"],[None,"<:octariandamage:895723525954998272>"]]
            elif self.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL,TYPE_INDIRECT_REZ]:
                self.emoji=[["<:ikaheal1:895722730664632321>","<:ikaheal2:895722783034732594>"],["<:takoheal1:895722755025162281>","<:takoheal2:895722806430548001>"],[None,"<:octarianheal:895722827188166698>"]]
            elif self.type in [TYPE_ARMOR]:
                self.emoji=[["<:ikashield:895723993351458877>","<:ikashield2:895724022501892217>"],["<:takoshield1:895724008350318602>","<:takoshield2:895724040348659772>"],[None,"<:octarianshield:895724055909515265>"]]
            else:
                self.emoji=[['<:lenapy:892372680777539594>','<:lenapy:892372680777539594>'],['<:lenapy:892372680777539594>','<:lenapy:892372680777539594>'],['<:lenapy:892372680777539594>','<:lenapy:892372680777539594>']]
        else:
            self.emoji=emoji


        if self.emoji[0] == "<":
            self.emoji = uniqueEmoji(emoji)

        for a in [0,1,2]:
            for b in [0,1]:
                try:
                    self.emoji[a][b]
                except:
                    raise Exception(self.name)
            
                if self.emoji[a][b] != None:
                    chocolatine = ["",""]
                    first, second, temp = False, False, ""
                    for c in self.emoji[a][b]:
                        if c == ":":
                            if not(first):
                                first = True
                            elif not(second):
                                chocolatine[0] = temp
                                temp, second = "",True
                        elif first and c != ">":
                            temp += c

                    chocolatine[1] = int(temp)
                    if self.emoji[a][b][1] == "a":
                        self.emoji[a][b] = "<a:{0}:{1}>".format(chocolatine[0][:2],chocolatine[1])
                    else:
                        self.emoji[a][b] = "<:{0}:{1}>".format(chocolatine[0][:2],chocolatine[1])

    def __str__(self) -> str:
        return self.name
    def setTurnInit(self,newTurn = 1):
        """Change the "turnInit" value. Why I need a function for that ?"""
        self.turnInit = newTurn
        return self

    def allStats(self):
        """Return a list with the mains stats of the weapon"""
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

class weapon:
    """The main and only class for weapons"""
    def __init__(self,name : str,id : str,range,effectiveRange,power : int,sussess : int,price = 0,strength=0,endurance=0,charisma=0,agility=0,precision=0,intelligence=0,magie=0,resistance=0,percing=0,critical=0, repetition=1,emoji = None,area = AREA_MONO,effect:Union[None,effect]=None,effectOnUse=None,target=ENEMIES,type=TYPE_DAMAGE,orientation=[],needRotate = True,use=STRENGTH,damageOnArmor=1,affinity = None,message=None,negativeHeal=0,negativeDirect=0,negativeShield=0,negativeIndirect=0,negativeBoost=0,say="",ignoreAutoVerif=False,taille=1):
        """rtfm"""
        self.name:str = name
        self.say:Union[str,List[str]] = say
        self.id:str = id
        try:
            self.id.isdigit
        except:
            print(self.name)
        self.range = range
        self.strength = strength
        self.endurance = endurance
        self.charisma = charisma
        self.agility = agility
        self.precision = precision
        self.intelligence = intelligence
        self.magie = magie
        self.resistance = resistance
        self.percing = percing
        self.critical = critical
        self.power = power
        self.repetition = repetition
        self.sussess = sussess
        self.price = price
        self.area = area
        self.effect = effect
        self.effectiveRange = effectiveRange
        self.effectOnUse = effectOnUse
        self.target = target
        self.type = type
        self.needRotate = needRotate
        self.use = use
        if self.range == 2 and damageOnArmor == 1:
            damageOnArmor = 1.33
        self.onArmor = damageOnArmor
        self.message = message

        self.negativeHeal = negativeHeal
        self.negativeShield = negativeShield
        self.negativeDirect = negativeDirect
        self.negativeIndirect = negativeIndirect
        self.negativeBoost = negativeBoost
        self.taille = taille

        if (self.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL]) and self.use == STRENGTH:
            self.use = CHARISMA
            print("{0} : Wrong stat taken. Taken the Charisma stat insted".format(name))

        self.affinity = affinity
        orientation += [None]
        if len(orientation) < 2:
            if orientation[0] == None:
                self.orientation = "Neutre"

        elif orientation[0] == None and orientation[1] != None:
            self.orientation = "Neutre - "+ orientation[1]
        elif orientation[0] == None:
            self.orientation = "Neutre"
        elif orientation[1] == None:
            self.orientation = orientation[0] + " - Neutre"
        else:
            self.orientation = orientation[0] + " - "+orientation[1]

        if emoji == None:
            if self.name != "noneWeap":
                if self.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]:
                    self.emoji='<:defDamage:885899060488339456>'
                elif self.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL]:
                    self.emoji='<:defHeal:885899034563313684>'
                elif self.type in [TYPE_BOOST,TYPE_SUMMON]:
                    self.emoji='<:defSupp:885899082453880934>'
                elif self.type in [TYPE_ARMOR]:
                    self.emoji='<:defarmor:895446300848427049>'
                elif self.type in [TYPE_MALUS]:
                    self.emoji='<:defMalus:895448159675904001>'
                else:
                    self.emoji='<:LenaWhat:760884455727955978>'
            else:
                self.emoji='<:noneWeap:917311409585537075>'
        else:
            self.emoji=emoji

        expectPrice = 100
        expectPrice += self.power * 4
        expectPrice += self.precision * 2
        if self.effect != None or self.effectOnUse != None:
            expectPrice += 200

        if expectPrice != price and price != 0:
            self.price = expectPrice

        if self.type == TYPE_DAMAGE and self.power != 0 and sussess != 0 and not(ignoreAutoVerif):
            expectation = 75 - 5*effectiveRange

            if self.area != AREA_MONO:
                expectation = expectation * 0.7
            if self.use != STRENGTH:
                expectation = expectation * 0.8
            if self.effect != None or self.effectOnUse != None:
                if self.id not in ["ob"]:
                    expectation = expectation * 0.8
                else:
                    expectation = expectation * 0.9
            expectation = int(expectation)

            reality = int(self.power * self.repetition * self.sussess/100)
            if reality != expectation:
                suggest = int(expectation / (self.repetition * self.sussess/100))
                if suggest != self.power:
                    print("{0} : Expected {1} finalPower, got {2}. Suggested basePower : {3}".format(self.name,expectation,reality,suggest))

    def allStats(self):
        """Return a list with the mains stats of the weapon"""
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

mainLibre = weapon("Main Libre","aa",RANGE_MELEE,AREA_CIRCLE_1,31,45,0,strength=15,agility=15,repetition=5,emoji = emoji.fist)
splattershotJR = weapon("Liquidateur JR","af",RANGE_DIST,AREA_CIRCLE_3,34,35,0,agility=10,charisma=10,strength=10,repetition=5,emoji = emoji.splatJr)

class skill:
    """The main and only class for the skills"""
    def __init__ (self,name : str, id : str, types : int ,price : int = 0, power= 0,range = AREA_CIRCLE_5,conditionType = [],ultimate = False,group = 0,emoji = None,effect=None,cooldown=1,area = AREA_MONO,sussess = 100,effectOnSelf=None,use=STRENGTH,damageOnArmor = 1,invocation=None,description=None,initCooldown = 1,shareCooldown = False,message=None,say="",repetition=1,knockback=0,effPowerPurcent=100,become:Union[list,None]=None,replay:bool=False,maxHpCost=0,hpCost=0,tpCac = False,jumpBack=0,useActionStats = None,setAoEDamage=False,url=None,areaOnSelf=False, lifeSteal = 0, effectAroundCaster = None,needEffect=None,rejectEffect=None,erosion=0,percing=None,execution=False,selfEffPurcent=100,effBeforePow=False,jaugeEff=None,pull=0):
        """rtfm"""
        if type(effect)!=list:
            effect = [effect]
        self.name = name                                # Name of the skill

        self.repetition = repetition                    # The number of hits it does
        self.say:Union[str,List[str]] = say                                  # Does the attacker say something when the skill is used ?
        self.id = id                                    # The id of the skill.  Idealy, unique
        self.type = types                               # The type of the skill. See constante.types
        self.replay = replay
        self.tpCac:bool = tpCac
        self.execution = execution
        self.jumpBack:int = jumpBack
        self.setAoEDamage:bool = setAoEDamage
        self.areaOnSelf = areaOnSelf
        self.lifeSteal:int = lifeSteal
        self.erosion, self.pull = erosion, pull
        self.effBeforePow, self.jaugeEff =effBeforePow, jaugeEff
        self.effectAroundCaster: Union[None,List[int]] = effectAroundCaster
        if needEffect == None or type(needEffect) == list:
            self.needEffect=needEffect
        else:
            self.needEffect=[needEffect]

        if rejectEffect == None or type(rejectEffect) == list:
            self.rejectEffect=rejectEffect
        else:
            self.rejectEffect=[rejectEffect]

        if effectAroundCaster != None:
            if effectAroundCaster[0] not in allTypes:
                raise Exception("EffectAroudCaster[0] not a type")
            elif effectAroundCaster[0] not in allArea:
                raise Exception("EffectAroudCaster[1] not a area")

        self.power = power  # Power of the skill. Use for damage and healing skills


        self.knockback:int = knockback
        self.effPowerPurcent:int = effPowerPurcent
        self.become:List = become
        self.url:str = url
        self.selfEffPurcent = selfEffPurcent

        if percing == None:
            self.percing = 0
        else:
            self.percing = percing + 20*int(ultimate)

        self.price = price                              # Price. 0 if the skill can't be drop or bought
        self.conditionType = 0
        self.condition = conditionType
        self.ultimate = ultimate
        self.effect = effect
        self.range = range
        self.group = group                      # Not used.
        self.cooldown = cooldown
        self.area = area
        self.maxHpCost, self.hpCost = maxHpCost, hpCost
        if sussess != 100 or types != TYPE_DAMAGE:
            self.sussess = sussess
        else:
            if area==AREA_MONO:
                self.sussess = 120
            else:
                self.sussess = 80

        self.effectOnSelf = effectOnSelf
        self.use = use
        if description != None:
            if "{0}" in description:
                print(name)
            if self.effect != [None] and type(self.effect[0]) != str:
                self.description = description.format(effIcon = self.effect[0].emoji[0][0],effName=self.effect[0].name,power=power,power2=power//2,length=self.effect[0].turnInit,armor=self.effect[0].overhealth)
            else:
                self.description = description.format(power=power,power2=power//2)
        else:
            self.description = None

        self.initCooldown = initCooldown
        self.shareCooldown = shareCooldown

        if use==STRENGTH:
            if types in [TYPE_ARMOR]:
                self.use = INTELLIGENCE
            elif types in [TYPE_HEAL,TYPE_INDIRECT_HEAL]:
                self.use = CHARISMA
            elif power == 0 and self.effect != [None] and type(self.effect[0]) != str:
                self.use = self.effect[0].stat
            elif power == 0 and self.effectOnSelf != None and type(self.effectOnSelf) != str:
                self.use = self.effectOnSelf.stat

        self.onArmor = damageOnArmor
        self.invocation = invocation
        self.message = message

        self.useActionStats = useActionStats

        if types==TYPE_PASSIVE:
            self.area=AREA_MONO
            self.range=AREA_MONO
            self.initCooldown=99
            if self.effectOnSelf == None:
                self.effectOnSelf = effect
                self.effect=None

        if conditionType != []:
            listTypeCond = ["exclusive","statMin","reject"]
            cmpt = 0
            for a in listTypeCond:
                if conditionType[0] == a:
                    self.condition[0] = cmpt
                cmpt+=1

            if self.condition[0] == 0:
                listExclu = ["weapon","aspiration","element","secElem"]
                cmpt = 0
                for a in listExclu:
                    if conditionType[1] == a:
                        self.condition[1] = cmpt
                    cmpt += 1
                
                self.condition[2] = conditionType[2]

            elif self.condition[0] == 1:
                listStats,cmpt = ["strength","endurance","charisma","agility","precision","intelligence"],0
                for a in listStats:
                    if conditionType[1] == a:
                        self.condition[1] = cmpt
                    cmpt += 1

                self.condition[2] = int(conditionType[2])

            elif self.condition[0] == 2:
                listReject = ["weapon","skill"]
                cmpt = 0
                for a in listReject:
                    if conditionType[1] == a:
                        self.condition[1] = cmpt
                    cmpt += 1
                
                self.condition[2] = conditionType[2]

        if area in [AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES]:
            self.range = AREA_MONO

        if emoji == None:
            if self.type in [TYPE_DAMAGE]:
                if area == AREA_MONO:
                    if use in [STRENGTH,PRECISION,AGILITY]:
                        if cooldown >= 7 or ultimate:
                            self.emoji='<:dUPM:943279319994728539>'
                        else:
                            self.emoji='<:dM:943275508492292138>'
                    else:
                        if cooldown >= 7 or ultimate:
                            self.emoji='<:dUMM:943279280002060309>'
                        else:
                            self.emoji='<:dD:885899060488339456>'
                else:
                    if use in [STRENGTH,PRECISION,AGILITY]:
                        if cooldown >= 7 or ultimate:
                            self.emoji='<:dUZ:943279239573143612>'
                        else:
                            self.emoji='<:dZ:943275494802079804>'
                    else:
                        if cooldown >= 7 or ultimate:
                            self.emoji='<:dUMZ:943279254991409232>'
                        else:
                            self.emoji="<:dZ:943266058024943656>"
            elif self.type in [TYPE_INDIRECT_DAMAGE]:
                self.emoji = '<:defIndi:943266043558768640>'
            elif self.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL]:
                if area == AREA_MONO:
                    if cooldown >= 7 or ultimate:
                        self.emoji='<:defUltHeal:943279333869486110>'
                    else:
                        self.emoji='<:defHeal:885899034563313684>'
                else:
                    self.emoji="<:defHealZone:943266024155922433>"
            elif self.type in [TYPE_BOOST,TYPE_SUMMON]:
                self.emoji='<:defSupp:885899082453880934>'
            elif self.type in [TYPE_ARMOR]:
                self.emoji='<:defarmor:895446300848427049>'
            elif self.type in [TYPE_MALUS]:
                self.emoji='<:defMalus:895448159675904001>'
            elif self.type in [TYPE_RESURECTION,TYPE_INDIRECT_REZ]:
                self.emoji='<:renisurection:873723658315644938>'
            else:
                self.emoji='<:LenaWhat:760884455727955978>'
        else:
            self.emoji=emoji

        if self.use == STRENGTH and self.type in [TYPE_INDIRECT_DAMAGE,TYPE_INDIRECT_HEAL,TYPE_BOOST,TYPE_MALUS] and (self.effect[0] != None and type(self.effect[0]) != str) :
            self.use = self.effect[0].stat

    def havConds(self,user):
        """Verify if the User have the conditions to equip the skill"""
        if self.condition != []:
            conds = self.condition
            if conds[0] == 0: # Reject
                if conds[1] == 1: # Conds Aspi
                    if user.aspiration != conds[2]:
                        return False
                elif conds[1] == 2: #Conds Elem
                    if user.element != conds[2]:
                        return False
                elif conds[1] == 3: #Conds Elem
                    if user.secElement != conds[2]:
                        return False

            elif conds[0] == 1: 
                userstats = user.allStats()
                if userstats[conds[1]] < conds[2]:
                    return False

        elif self.group != 0:
            for skilly in user.skills:
                if type(skilly) == skill and skilly.group not in [0,self.group]:
                    return False

        return not(user.level < 10 and self.ultimate)

class stuff:
    """The main and only class for all the gears"""
    def __init__(self,name,id,types,price,strength=0,endurance=0,charisma=0,agility=0,precision=0,intelligence=0,magie=0,resistance=0,percing=0,critical=0,emoji = None,effect=None,orientation = [],position=0,affinity = None,negativeShield=0,negativeHeal=0,negativeDirect=0,negativeIndirect=0,negativeBoost=0):
        """rdtm"""
        self.name = name
        self.id = id
        self.price = price
        self.type = types
        self.strength = strength
        self.endurance = endurance
        self.charisma = charisma
        self.agility = agility
        self.precision = precision
        self.intelligence = intelligence
        self.magie = magie
        self.resistance = resistance
        self.percing = percing
        self.critical = critical
        self.emoji = emoji
        self.position = position

        self.negativeHeal = negativeHeal
        self.negativeShield = negativeShield
        self.negativeDirect = negativeDirect
        self.negativeIndirect = negativeIndirect
        self.negativeBoost = negativeBoost

        if price != 0:
            sumStats = 0
            for stat in [strength,endurance,charisma,agility,precision,intelligence,magie,resistance,percing,critical,negativeHeal*-1,negativeBoost*-1,negativeShield*-1,negativeDirect*-1,negativeIndirect*-1]:
                sumStats += max(0,stat)
            tempPrice = int((sumStats-20)*7.5)+100
            if effect != None:
                tempPrice += 100
            self.price = tempPrice

        if emoji == None:
            if self.type == 0:
                self.emoji='<:defHead:896928743967301703>'
                self.position = 4
            elif self.type == 1:
                self.emoji='<:defMid:896928729673109535>'
            elif self.type == 2:
                self.emoji='<:defShoes:896928709330731018>'

        self.effect = effect
        self.affinity = affinity

        if type(orientation) != list:
            self.orientation = orientation
        else:
            orientation += [None]
            if len(orientation) < 2:
                if orientation[0] == None:
                    self.orientation = "Neutre"

            elif orientation[0] == None and orientation[1] != None:
                self.orientation = "Neutre - "+ orientation[1]
            elif orientation[0] == None:
                self.orientation = "Neutre"
            elif orientation[1] == None:
                self.orientation = orientation[0] + " - Neutre"
            else:
                if orientation == [LONG_DIST,DPT_PHYS,None]:
                    self.orientation = LONG_DIST + " - Obs, T.Bru"
                elif orientation == [TANK,DPT_PHYS,None]:
                    self.orientation = TANK + " - Bers, P.Plu"
                else:
                    self.orientation = orientation[0] + " - "+orientation[1]

        cmpt = 0
        summation = 0
        for stat in [strength,endurance,charisma,agility,precision,intelligence,magie,resistance,percing,critical,negativeHeal*-1,negativeBoost*-1,negativeShield*-1,negativeDirect*-1,negativeIndirect*-1]:
            if stat > 0:
                summation += stat

        if effect != None:
            summation += 15

        while 20 + cmpt * 10 < summation:
            cmpt += 1
        self.minLvl = cmpt * 5

    def allStats(self):
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

    def havConds(self,user):
        return user.level >= self.minLvl

emojiMalus = [['<:ink1debuff:866828217939263548>','<:ink2debuff:866828296833466408>' ],['<:oct1debuff:866828253695705108>','<:oct2debuff:866828340470874142>'],['<:octariandebuff:866828390853247006>','<:octariandebuff:866828390853247006>']]

class other:
    """The class for all the "specials objets" categorie"""
    def __init__(self,name,id,price=1000,emoji=emoji.loading,description="Léna est féniant"):
        self.name = name
        self.id = id
        self.price = price
        self.emoji = emoji
        self.description = description

bbandeau = stuff("Bandeau du débutant","ha",0,0,resistance=5,endurance=5,strength=5,intelligence=5,emoji="<:bhead:867156694629744691>")
bshirt = stuff("Tee-shirt du débutant","hb",1,0,resistance=5,strength=5,agility=5,precision=5,emoji="<:bshirt:867156711251771402>")
bshoes = stuff("Chaussures du débutant","hc",2,0,agility=5,endurance=5,charisma=10,emoji="<:bshoes:867156725945073694>")

class char:
    """
        The most important class. Store the data of a character\n
        Attributs :\n
        .owner : The owner id of the character
        .name : The name of the character
        .level : The level of the character
        .exp : The exp of the character for the current level
        .currencies : The amount of coins the character owns
        .species : The species of the character. ``1`` for Inkling, ``2`` for Octaling
        .color : The color of the character
        .team : The character's team ID
        .gender : The gender of the character. Only use for according messages
        .strength -> .critical : The main stats of the characters
            -> A character do not have Action Stats by them self, for now
        .aspiration : A ``int`` who represent the character aspiration
        .points : The number of bonus points the character can attribuate
        .weapon : The ``weapon`` used by the character
        .weaponInventory : The ``list`` of ``weapon`` objects own by the character
        .skills : A ``list`` of the equiped ``skill`` objects by the character
    """
    def __init__(self,owner,name = "",level = 1,species=0,color=red):
        self.owner:int = owner
        self.name:str = str(name)
        self.level = int(level)
        self.stars = 0
        self.exp = 0
        self.currencies = 0
        self.species = species
        self.color = color
        self.team = 0
        self.gender = GENDER_OTHER
        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie = 0,0,0,0,0,0,0
        self.resistance,self.percing,self.critical = 0,0,0
        self.aspiration = -1
        self.points = 0
        self.canMove = True
        self.majorPointsCount = 0
        self.weapon = splattershotJR
        self.weaponInventory = [splattershotJR,mainLibre]
        self.skills = ["0","0","0","0","0","0","0"]
        self.skillInventory = []
        self.stuff = [bbandeau,bshirt,bshoes]
        self.stuffInventory = [bbandeau,bshirt,bshoes]
        self.otherInventory = []
        self.procuration = []
        self.bonusPoints = [0,0,0,0,0,0,0]
        self.majorPoints = [0,0,0,0,0,0,0]+[0,0,0]+[0,0,0,0,0]
        self.icon = None
        self.customColor = False
        self.element = ELEMENT_NEUTRAL
        self.secElement = ELEMENT_NEUTRAL
        self.deadIcon = None
        self.says = says()
        self.autoPoint = False
        self.apparaWeap:weapon = None
        self.apparaAcc:stuff = None
        self.colorHex = None
        self.iconForm = 0
        self.showElement = True
        self.showWeapon = True
        self.showAcc = True
        self.handed = 1
        self.autoStuff = False
        self.haveProcurOn = []

    def have(self,obj):
        """Verify if the character have the object Obj"""
        return obj in self.weaponInventory or obj in self.skillInventory or obj in self.stuffInventory or obj in self.otherInventory

    def isNpc(self,name : str):
        return False

    def allStats(self):
        """Return a list of all main stats of the character"""
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

class invoc:
    """The main class for summons. Similar the "char" class, but with only the fight's necessery attributs"""
    def __init__(self,name,strength,endurance,charisma,agility,precision,intelligence,magie,resistance,percing,critical,aspiration,icon,weapon,skill=[],gender=GENDER_OTHER,description="Pas de description",element=ELEMENT_NEUTRAL,canMove=True):
        self.name = name
        self.level = 0
        self.team = 0
        self.gender = gender
        self.color = 0
        self.species = 1
        self.stars = 0
        self.canMove = canMove

        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.resistance,self.percing,self.critical,self.magie = strength,endurance,charisma,agility,precision,intelligence,resistance,percing,critical,magie
        self.aspiration = aspiration
        self.weapon = weapon
        self.majorPoints = [0,0,0,0,0,0,0]+[0,0,0]+[0,0,0,0,0]

        self.description = description
        
        while len(skill)<7:
            skill.append("0")

        self.skills = skill
        self.icon = icon
        self.customColor = False
        if type(element) != list:
            element = [element,ELEMENT_NEUTRAL]
        self.element = element[0]
        self.secElement = element[1]
        self.says = says()
        
    def allStats(self):
        """Return a list """
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]
    
    def isNpc(self,name : str):
        return False

incurable = effect("Incurable","incur",type=TYPE_MALUS,power=100,description="Diminue les soins reçus par la cible de **(puissance)**%.\n\nL'effet Incurable n'est pas cumulable\nSi un autre effet Incurable moins puissant est rajouté sur la cible, celui-ci est ignoré\nSi un autre effet Incurable plus puissant est rajouté, celui-ci remplace celui déjà présent",emoji=[['<:healnt:903595333949464607>','<:healnt:903595333949464607>'],['<:healnt:903595333949464607>','<:healnt:903595333949464607>'],['<:healnt:903595333949464607>','<:healnt:903595333949464607>']])

incur = []
for num in range(0,10):
    incurTemp = copy.deepcopy(incurable)
    incurTemp.power = 10*num
    incurTemp.name = "Incurable ({0})".format(10*num)
    incurTemp.description="Diminue les soins reçus par la cible de **{0}**%.\n\nEffet Remplaçable : Les effets remplaçables sont remplassés si le même effet avec une meilleure puissance est donné".format(10*num)
    incur.append(incurTemp)

vulne = effect("Dégâts subis augmentés","vulne",power=100,emoji=sameSpeciesEmoji("<a:defDebuffB:954544469649285232>","<a:defDebuffR:954544494110441563>"),type=TYPE_MALUS,stackable=True)
defenseUp = effect("Dégâts subis réduits","defenseUp",stackable=True,emoji=sameSpeciesEmoji('<a:defBuffB:954537632543682620>','<a:defBuffR:954538558541148190>'),description="Réduit les dégâts reçus d'une valeur égalant la puissance de l'effet")
dmgUp = effect("Dégâts infligés augmentés","dmgUp",stackable=True,emoji=sameSpeciesEmoji('<a:dmgBuffB:954429227657224272>','<a:dmgBuffR:954429157079654460>'),description="Augmente les dégâts infligés d'une valeur égalant la puissance de l'effet")

vulneTabl = []
for num in range(0,10):
    vulneTemp = copy.deepcopy(vulne)
    vulneTemp.power = 10*num
    vulneTemp.name += " ({0})".format(10*num)
    vulneTemp.description="Augmente les dégâts subis par le porteur de **{0}%**".format(10*num)
    vulneTabl.append(vulneTemp)

dmgDown = effect("Dégâts infligés réduits","dmgDown",power=100,emoji=sameSpeciesEmoji("<a:dmgDebuffB:954431054654087228>","<a:dmgDebuffR:954430950668914748>"),type=TYPE_MALUS,stackable=True)
partage = effect("Partage","share",type=TYPE_MALUS,power=100,turnInit=-1,description="",stackable=True,emoji=[["<:sharaB:931239879852032001>","<:shareR:931239900018278470>"],["<:sharaB:931239879852032001>","<:shareR:931239900018278470>"],["<:sharaB:931239879852032001>","<:shareR:931239900018278470>"]],area=AREA_DONUT_2)

shareTabl = []
for num in range(0,10):
    shareTemp = copy.deepcopy(partage)
    shareTemp.power = 10*num
    shareTemp.name = "Partage ({0})".format(10*num)
    shareTemp.description="En revecant des soins monocibles, les alliés dans la zone d'effet en reçoivent **{0}**% bonus.\n\nSi plusieurs effets Partages sont présent sur la même cible, uniquement le plus puissant sont pris en compte".format(10*num)
    shareTabl.append(shareTemp)

healDoneBonus = effect("Soins réalisés augmentés","healBonus",description="Augmente les soins réalisés par le lanceur d'une valeur équivalante à la puissance de cet effet",emoji='<:temperance:982349348992081960>')

intargetable = effect("Inciblable","untargetable",untargetable=True,emoji=uniqueEmoji('<:untargetable:899610264998125589>'),description="Cet entité deviens inciblable directement",turnInit=2)

textBaliseAtReplace = ["Ã©","Ã","à§"]
textBaliseToReplace = ["é","à","ç"]

if len(textBaliseAtReplace) != len(textBaliseToReplace):
    raise Exception("len(textBaliseAtReplace) != len(textBaliseToReplace)")

class dutyText:
    """The class of a duty text, for generating the embed\n"""
    def __init__(self,ref : str, text : str):
        self.ref = ref
        
        for cmpt in range(len(textBaliseAtReplace)):
            text = text.replace(textBaliseAtReplace[cmpt],textBaliseToReplace[cmpt])
        
        self.text = text

        if len(self.text) > 4026:
            raise Exception("Text ref {0} is to big ({1} / 4026)".format(self.ref,len(self.text)))

class duty:
    """The class of a loaded duty"""
    def __init__(self,act: str,name : str, dutyTextList : List[dutyText]):
        """
            .name : The name of the duty\n
            .dutyTextList : A ``list`` of ``dutyText`` objects
        """
        self.act = act
        self.name = name
        self.dutyTextList = dutyTextList
        self.cmpt = -1
        self.team = []

    def __str__(self):
        return self.name

    def nextText(self):
        """Increment the inter cumpter and return the corresponding ``dutyText``"""
        self.cmpt += 1
        print(self.cmpt)
        if self.cmpt > len(self.dutyTextList)-1:
            raise Exception("Duty {0} error : dutyTextList index above the len of the list".format(self))
        return self.dutyTextList[self.cmpt]

    def prevText(self):
        """Decrement the inter cumpter and return the corresponding ``dutyText``"""
        self.cmpt -= 1
        if self.cmpt < 0:
            raise Exception("Duty {0} error : dutyTextList index under 0".format(self))
        return self.dutyTextList[self.cmpt]

    def actText(self):
        """Return the actual ``dutyText``"""
        return self.dutyTextList[self.cmpt]

    def addTeam(self,team : list):
        self.team = team

octoEmpty1 = stuff("placeolder","ht",0,0)
octoEmpty2 = stuff("placeolder","hu",0,0)
octoEmpty3 = stuff("placeolder","hv",0,0)

class octarien:
    """The class for the ennemis
    \nBased on a ``char`` object"""
    def __init__(
            self,
            name:str,
            maxStrength:int,
            maxEndurance:int,
            maxCharisma:int,
            maxAgility:int,
            maxPrecision:int,
            maxIntelligence:int,
            maxMagie:int,
            resistance:int,
            percing:int,
            critical:int,
            weapon:weapon,
            exp:int,
            icon:str,
            skill:List[Union[skill,str,None]] =["0","0","0","0","0","0","0"],
            aspiration:int=ASPI_NEUTRAL,
            gender:int=GENDER_OTHER,
            description:str="",
            deadIcon:Union[str,None]=None,
            oneVAll:bool = False,
            say:says=says(),
            baseLvl:int = 1,
            rez:bool=True,
            element:List[int] = [ELEMENT_NEUTRAL,ELEMENT_NEUTRAL],
            number:int = 1,
            canMove=True
        ):
        """
            .name : The name of the ennemy
            .maxStrength -> .maxMagie : The amount of stat in their respective category that the ennemy will have at level 50
            .resistance -> .critical : The amount of stat in their respective category that the ennemy will have. Unlike the main stats, do not change depending of the level
            .weapon : The ``weapon`` use by the ennemy
            .exp : The amount of experience the ennemy will give if they are down
            .icon : The emoji string of the ennemy, used has his icon
            .skill : A list of ``skill`` objects, used by the ennemy
            .aspiration : The aspiration of the ennemy
            .gender : The gender of the ennmy. Only use for according messages
            .description : The description of the ennemy
            .deadIcon : the emoji string to use when the ennemy is down
            .oneVAll : Does the ennemy is a "All v One" boss ?
            .say : A ``says`` object, for some specials interractions
            .baseLvl : The minimum amount of level required for battleling againts the ennemy
            .rez : Does the ennemy can be raise ?
            .element : The element of the ennemy
            .number : The number of times the ennemy appairse in the ennemy list
        """
        self.name = name
        self.owner = self.team = 0
        self.species = 3
        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie = maxStrength,maxEndurance,maxCharisma,maxAgility,maxPrecision,maxIntelligence,maxMagie
        self.resistance,self.percing,self.critical = resistance,percing,critical
        self.aspiration = aspiration
        self.weapon = weapon
        self.number = number
        self.skills = skill
        self.stars = 0
        self.team = -2
        self.canMove = canMove
        while len(self.skills) < 7:
            self.skills+=["0"]

        self.skillsInventory = []
        self.majorPoints = [0,0,0,0,0,0,0]+[0,0,0]+[0,0,0,0,0]
        self.color = red
        self.level = 1
        self.stuff = [octoEmpty1,octoEmpty2,octoEmpty3]
        self.exp = exp
        self.icon = icon
        self.gender = gender
        self.description = description

        if type(element) != list:
            element = [element,ELEMENT_NEUTRAL]

        self.element = element[0]
        self.secElement = element[1]
        self.deadIcon = deadIcon
        self.oneVAll = oneVAll
        self.says = say
        self.baseLvl = baseLvl
        self.rez = rez
        self.bonusPoints = [0,0,0,0,0,0,0]

    def allStats(self):
        """Return a ``list`` with the mains stats of the ennemi\n
        Those stats are the Lvl 50 stats"""
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

    def changeLevel(self,level=1):
        """Change the level of the ennmy and adjust his stats and skills in consequence\n
        It's very recommanded to do than on a copy of the ennemy"""
        self.level = level
        stats, cmpt = copy.deepcopy(self.allStats()),0
        for a in lvlToUnlockSkill:
            if self.level >= a:
                cmpt += 1

        skillCountMul = 0.65 + (0.35*(cmpt/7))

        for a in range(0,len(stats)):
            stats[a] = round(stats[a]*0.1+stats[a]*0.9*self.level/50*skillCountMul)

        for cmpt in range(len(lvlToUnlockSkill)):
            if self.level < lvlToUnlockSkill[cmpt]:
                self.skills[cmpt] = "0"

        if self.level < 10:
            self.element = ELEMENT_NEUTRAL
        elif self.level < 20 and self.element in [ELEMENT_SPACE,ELEMENT_DARKNESS,ELEMENT_LIGHT,ELEMENT_LIGHT]:
            self.element = random.randint(0,3)

        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie = stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],stats[6]

    def isNpc(self,name : str):
        """Return if the given name is egal to the ennemy name"""
        return self.name == name

    def __str__(self) -> str:
        return self.name

class tmpAllie:
    """The class for the allies\n
    Based on a ``char`` object"""
    def __init__(self,
        name:str,
        species:int,
        color:int,
        aspiration:int,
        weapon:weapon,
        stuff:List[stuff],
        gender:int,
        skill:List[skill]=[],
        description:str="Pas de description",
        element:List[int]=[ELEMENT_NEUTRAL,ELEMENT_NEUTRAL],
        variant:bool = False,
        deadIcon: Union[None,str]=None,
        icon: Union[None,str] = None,
        bonusPoints:List[int] = [None,None],
        say:says=says(),
        changeDict:Union[None,dict] = None,
        unlock:Union[bool,None,str]=False,
        birthday:Union[None,tuple]=None,
        ):
        """
            The class for a ally, based on the ``char`` class\n

            - Parameters :\n
                .name : The name of the ally
                .species : The species of the ally. ``1`` for Inkling, ``2`` for Octoling
                .color : A ``int`` that represent the color of the ally
                .aspiration : The aspiration of the ally
                .weapon : The ``weapon`` use by the ally
                .stuff : A ``list`` of three ``stuff`` use by the ally
                .gender : The gender of the ally. Used for accordings messages only
                .skill : A ``list`` of ``skill`` use by the ally
                .description : The descrition of the ally. Try to be brief
                .element : The element of the ally
                .variant : Does the ally is a variant of another ally ?
                .deadIcon : The emoji string to use when the ally is down
                .icon : The emoji string to use for the ally icon. If ``None``, use one of the default icon insteed
                .bonusPoints : The ``list`` of stats to prioritise for reparting the bonus points
                .say : A ``says`` object for special interractions
                .changeDict : A ``dict`` who define if the ally must take another build sometimes
                .unlock : When the ally is unlock for the Adventure. 
                    -> ``False`` : Not unlocable
                    -> ``None`` : Base ally allready unlocked
                    -> ``ActName - DutyName`` : The duty after the ally will be unlock
        """

        self.name = name
        self.species = species
        self.owner = self.team = 0
        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie = 0,0,0,0,0,0,0
        self.resistance,self.percing,self.critical = 0,0,0
        self.aspiration = aspiration
        self.weapon = weapon
        self.stars = 0
        self.team = -1
        self.birthday = birthday
        self.canMove = True
        self.skills = ["0","0","0","0","0","0","0"]
        self.majorPoints = [0,0,0,0,0,0,0]+[0,0,0]+[0,0,0,0,0]
        for a in range(len(skill)):
            self.skills[a] = skill[a]
        self.skillsInventory = []
        self.color = color
        self.level = 1
        self.stuff = stuff
        self.gender = gender
        if icon == None:
            raise Exception("No icon given")
        else:
            self.icon = icon
        self.description=description
        if type(element) != list:
            element = [element,ELEMENT_NEUTRAL]
        self.element = element[0]
        self.secElement = element[1]
        self.variant = variant
        self.deadIcon = deadIcon
        self.bonusPoints = bonusPoints
        self.says = say
        if changeDict == None or type(changeDict) == list:
            self.changeDict = changeDict
        else:
            self.changeDict = [changeDict]

        self.unlock = unlock

    def __str__(self):
        return self.name

    def changeLevel(self,level=1,changeDict=True):
        for procurName, procurStuff in procurTempStuff.items():
            if self.name == procurName:
                level += procurStuff[0]
                break

        self.level = level
        stats = self.allStats()

        for a in range(0,len(stats)):
            stats[a] = round(aspiStats[self.aspiration][a]*0.1+aspiStats[self.aspiration][a]*0.9*self.level/50)

        bPoints = level
        for a in self.bonusPoints:
            if a != None:
                distribute = min(30,bPoints)
                bPoints -= distribute
                stats[a] += distribute

        if self.changeDict != None and changeDict==True:
            haveChanged = False
            for changeDictCell in self.changeDict:
                roll = random.randint(0,99)
                if changeDictCell["level"] <= level and roll < changeDictCell["proba"] and not(haveChanged):
                    if changeDictCell["changeWhat"] == 0:               # Change Skills
                        for num in range(len(changeDictCell["change"])):
                            for skillNum in range(len(self.skills)):
                                if self.skills[skillNum].id == changeDictCell["change"][num].id:
                                    self.skills[skillNum] = changeDictCell["to"][num]
                                    break
                        haveChanged = True

        for cmpt in range(len(lvlToUnlockSkill)):
            if self.level < lvlToUnlockSkill[cmpt]:
                self.skills[cmpt] = "0"

        if self.level < 10:
            self.element = ELEMENT_NEUTRAL
        elif self.level < 20 and self.element in [ELEMENT_SPACE,ELEMENT_DARKNESS,ELEMENT_LIGHT,ELEMENT_LIGHT]:
            self.element = random.randint(0,3)

        if self.level < 30:
            self.secElement = ELEMENT_NEUTRAL

        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie = stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],stats[6]

    def allStats(self):
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

    def isNpc(self,name : str):
        return self.name == name

    def isUnlock(self, duty:duty):
        """Return if the Tmp can be use in the ``duty``"""
        if self.unlock == None:
            return True
        elif self.unlock == False:
            return False
        
        for mainTemp in allActs:
            for temp in mainTemp[1:]:
                if mainTemp[0]+"|"+temp == self.unlock:
                    return False
                elif mainTemp[0]+"|"+temp == duty.act+"|"+duty.name:
                    return True

        return None

silenceEff = effect("InCapacité","silenceEff",description="Empèche l'utilisation de compétence durant la durée de l'effet",type=TYPE_MALUS,emoji='<:silenced:975746154270691358>')
absEff = effect("Absorbtion","absEff",description="Augmente les soins reçus par le porteur d'un pourcentage équivalant à la puissance de cet effet",emoji='<:absorb:971788658782928918>',stackable=True)
chained = effect("Enchaîné","chained",emoji='<:chained:982710848487317575>',description="Empêche tous déplacements de la cible, que ce soit par elle-même que part une compétence",type=TYPE_MALUS)
upgradedLifeSteal = effect("Augmentation du plafond de vol de vie","lifeSteal+",power=100,turnInit=-1,silent=True,unclearable=True,description="Augmente de **{0}%** le plafond de vol de vie")

ailillUpLifeSteal, clemPosUpLifeSteal, clemExUpLifeSteal = copy.deepcopy(upgradedLifeSteal), copy.deepcopy(upgradedLifeSteal), copy.deepcopy(upgradedLifeSteal)
ailillUpLifeSteal.power, clemPosUpLifeSteal.power, clemExUpLifeSteal.power = 20,50,10000
upLifeStealNames, upLifeStealEff = ["Clémence Exaltée","Clémence pos.","Ailill"], [clemExUpLifeSteal,clemPosUpLifeSteal,ailillUpLifeSteal]
