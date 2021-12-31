"""
base classes module
Here are grouped up the bases classes of the bot, and some very basic functions
"""

import emoji,pathlib,copy,random
from constantes import *
from typing import List, Union

absPath = str(pathlib.Path(__file__).parent.resolve())

class autoColor:
    """A class for the "autocolor" command of the bot.
    Maybe I should delete it all, no body will ever use it, me included"""
    def __init__(self,enable,redId = 0,orangeId = 0,yellowId = 0,greenId = 0,lightBlueId = 0,blueId = 0,purpleId = 0,pinkId = 0,whiteId = 0,blackId = 0):
        self.enable = enable
        self.red = redId
        self.orange = orangeId
        self.yellow = yellowId
        self.green = greenId
        self.lightBlue = lightBlueId
        self.blue = blueId
        self.purple = purpleId
        self.pink = pinkId
        self.white = whiteId
        self.black = blackId

class server:
    """A class that is use to store the guild's settings"""
    def __init__(self,id,prefixe="l!",patchnote = 0,bot = 0):
        self.id = id
        self.prefixe = prefixe
        self.patchnote = patchnote
        self.bot = bot
        self.name = ""
        self.colorRole = autoColor(0)

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

class option:
    """Very basic class. Only use in the "Select Option" window of manuals fights"""
    def __init__(self,name,emoji):
        self.name = name
        self.emoji = emoji

class effect:
    """The class for all skill's none instants effects and passive abilities from weapons and gears"""
    def __init__(self,name,id,stat=None,strength=0,endurance=0,charisma=0,agility=0,precision=0,intelligence=0,magie=0,resistance=0,percing=0,critical=0,emoji=None,overhealth = 0,redirection = 0,reject=None,description = "Pas de description",turnInit = 1,immunity=False,trigger=TRIGGER_PASSIVE,callOnTrigger = None,silent = False,power:int = 0,lvl = 1,type = TYPE_BOOST,ignoreImmunity = False,area=AREA_MONO,unclearable = False,stun=False,stackable=False,replique=None,translucide=False,untargetable=False,invisible=False,aggro=0,absolutShield = False, lightShield = False,onDeclancher = False,inkResistance=0):
        """rtfm"""
        self.name = name                    # Name of the effect
        self.id = id                        # The id. 2 characters
        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie,self.resistance,self.percing,self.critical= strength,endurance,charisma,agility,precision,intelligence,magie,resistance,percing,critical
        self.overhealth = overhealth        # Base shield power
        self.redirection = redirection      # Damage redirection ratio. Unuse yet
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

        if self.reject != None and self.id in self.reject:
            self.reject.remove(self.id)

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
            self.emoji = [[emoji,emoji],[emoji,emoji],[emoji,emoji]]

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
    def __init__(self,name : str,id : str,range,effectiveRange,power : int,sussess : int,price = 0,strength=0,endurance=0,charisma=0,agility=0,precision=0,intelligence=0,magie=0,resistance=0,percing=0,critical=0, repetition=1,emoji = None,area = AREA_MONO,effect:Union[None,effect]=None,effectOnUse=None,target=ENNEMIS,type=TYPE_DAMAGE,orientation=[],needRotate = True,use=STRENGTH,damageOnArmor=1,affinity = None,message=None,negativeHeal=0,negativeDirect=0,negativeShield=0,negativeIndirect=0,negativeBoost=0,say="",ignoreAutoVerif=False):
        """rtfm"""
        self.name:str = name
        self.say:str = say
        self.id:str = id
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
        self.say = ""
        if self.range == 2 and damageOnArmor == 1:
            damageOnArmor = 1.33
        self.onArmor = damageOnArmor
        self.message = message

        self.negativeHeal = negativeHeal
        self.negativeShield = negativeShield
        self.negativeDirect = negativeDirect
        self.negativeIndirect = negativeIndirect
        self.negativeBoost = negativeBoost

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
    def __init__ (self,name : str, id : str, types : int ,price : int, power= 0,range = AREA_CIRCLE_5,conditionType = [],ultimate = False,secondary = False,emoji = None,effect=None,cooldown=1,area = AREA_MONO,sussess = 100,effectOnSelf=None,use=STRENGTH,damageOnArmor = 1,invocation=None,description=None,initCooldown = 1,shareCooldown = False,message=None,say="",repetition=1,knockback=0,effPowerPurcent=100,become:Union[list,None]=None):
        """rtfm"""
        self.name = name                                # Name of the skill
        self.repetition = repetition                    # The number of hits it does
        self.say = say                                  # Does the attacker say something when the skill is used ?
        self.id = id                                    # The id of the skill.  Idealy, unique
        self.type = types                               # The type of the skill. See constante.types
        
        if power != AUTO_POWER:
            self.power = power                              # Power of the skill. Use for damage and healing skills
        else:
            power = 25 + 25*cooldown
            if area != AREA_MONO:
                power = power * 0.7
            if use == MAGIE:
                power = power * 1.2
            self.power = int(power)

        self.knockback = knockback
        self.effPowerPurcent = effPowerPurcent
        self.become = become

        if range == AREA_MONO and area != AREA_MONO and types == TYPE_DAMAGE:
            self.power = int(power * (1+AOEDAMAGEREDUCTION))

        self.price = price                              # Price. 0 if the skill can't be drop or bought
        self.conditionType = 0
        self.condition = conditionType
        self.ultimate = ultimate
        self.effect = effect
        self.range = range
        self.secondary = secondary                      # Not used.
        self.cooldown = cooldown
        self.area = area
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
            self.description = description.format(power,power//2)
        else:
            self.description = None
            
        self.initCooldown = initCooldown
        self.shareCooldown = shareCooldown
        if use==STRENGTH:
            if types in [TYPE_ARMOR]:
                self.use = INTELLIGENCE
            elif types in [TYPE_HEAL,TYPE_INDIRECT_HEAL]:
                self.use = CHARISMA

        self.onArmor = damageOnArmor
        self.invocation = invocation
        self.message = message

        if types==TYPE_PASSIVE:
            self.area=AREA_MONO
            self.range=AREA_MONO
            self.initCooldown=99
            if self.effectOnSelf == None:
                self.effectOnSelf = effect
                self.effect=None
                print("{0} : EffectOnSelf not found ! Taken the effect in Effect field insted !".format(name))

        if type(self.effect)!=list:
            self.effect = [self.effect]

        if conditionType != []:
            listTypeCond = ["exclusive","statMin","reject"]
            cmpt = 0
            for a in listTypeCond:
                if conditionType[0] == a:
                    self.condition[0] = cmpt
                cmpt+=1

            if self.condition[0] == 0:
                listExclu = ["weapon","aspiration","element"]
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
            elif self.type in [TYPE_RESURECTION,TYPE_INDIRECT_REZ]:
                self.emoji='<:renisurection:873723658315644938>'
            else:
                self.emoji='<:LenaWhat:760884455727955978>'
        else:
            self.emoji=emoji

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

            elif conds[0] == 1: 
                userstats = user.allStats()
                if userstats[conds[1]] < conds[2]:
                    return False
        return user.level >= 5

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
                if orientation == [LONG_DIST,DPT,None]:
                    self.orientation = LONG_DIST + " - Obs, T.Bru"
                elif orientation == [TANK,DPT,None]:
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
        self.owner = owner
        self.name = str(name)
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
        self.majorPointsCount = 0
        self.weapon = splattershotJR
        self.weaponInventory = [splattershotJR,mainLibre]
        self.skills = ["0","0","0","0","0"]
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
        self.deadIcon = None
        self.says = says()
        self.apparaWeap = None
        self.apparaAcc = None
        self.colorHex = None

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
    def __init__(self,name,strength,endurance,charisma,agility,precision,intelligence,magie,resistance,percing,critical,aspiration,icon,weapon,skill=[],gender=GENDER_OTHER,description="Pas de description",element=ELEMENT_NEUTRAL):
        self.name = name
        self.level = 0
        self.team = 0
        self.gender = gender
        self.color = 0
        self.species = 1
        self.stars = 0

        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.resistance,self.percing,self.critical,self.magie = strength,endurance,charisma,agility,precision,intelligence,resistance,percing,critical,magie
        self.aspiration = aspiration
        self.weapon = weapon
        self.majorPoints = [0,0,0,0,0,0,0]+[0,0,0]+[0,0,0,0,0]

        self.description = description
        
        while len(skill)<5:
            skill.append("0")

        self.skills = skill
        self.icon = icon
        self.customColor = False
        self.element = element
        self.says = says()
        
    def allStats(self):
        """Return a list """
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]
    
    def isNpc(self,name : str):
        return False

incurable = effect("Incurable","incur",power=100,description="Diminue les soins reçus par la cible de **(puissance)**%.\n\nL'effet Incurable n'est pas cumulable\nSi un autre effet Incurable moins puissant est rajouté sur la cible, celui-ci est ignoré\nSi un autre effet Incurable plus puissant est rajouté, celui-ci remplace celui déjà présent",emoji=[['<:healnt:903595333949464607>','<:healnt:903595333949464607>'],['<:healnt:903595333949464607>','<:healnt:903595333949464607>'],['<:healnt:903595333949464607>','<:healnt:903595333949464607>']])

incur = []
for num in range(0,10):
    incurTemp = copy.deepcopy(incurable)
    incurTemp.power = 10*num
    incurTemp.name = "Incurable ({0})".format(10*num)
    incurTemp.description="Diminue les soins reçus par la cible de **{0}**%.\n\nEffet Remplaçable : Les effets remplaçables sont remplassés si le même effet avec une meilleure puissance est donné".format(10*num)
    incur.append(incurTemp)

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
            skill:List[Union[skill,str,None]] =["0","0","0","0","0"],
            aspiration:int=INVOCATEUR,
            gender:int=GENDER_OTHER,
            description:str="",
            deadIcon:Union[str,None]=None,
            oneVAll:bool = False,
            say:says=says(),
            baseLvl:int = 1,
            rez:bool=True,
            element:int = ELEMENT_NEUTRAL,
            number:int = 1
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
        self.species = 3
        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie = maxStrength,maxEndurance,maxCharisma,maxAgility,maxPrecision,maxIntelligence,maxMagie
        self.resistance,self.percing,self.critical = resistance,percing,critical
        self.aspiration = aspiration
        self.weapon = weapon
        self.number = number
        self.skills = skill
        self.stars = 0
        while len(self.skills) < 5:
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
        self.element = element
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
        stats = copy.deepcopy(self.allStats())
        for a in range(0,len(stats)):
            stats[a] = round(stats[a]*0.1+stats[a]*0.9*self.level/50)

        if level > 50:
            tempStats = copy.deepcopy(self.allStats())
            for a in range(0,len(tempStats)):
                stats[a] = tempStats[a] + (stats[a]-tempStats[a])//3

        if self.level < 25:
            self.skills[4] = "0"
        if self.level < 20:
            self.skills[3] = "0"
        if self.level < 15:
            self.skills[2] = "0"
        if self.level < 10:
            self.skills[1] = "0"

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
        element:int=ELEMENT_NEUTRAL,
        variant:bool = False,
        deadIcon: Union[None,str]=None,
        icon: Union[None,str] = None,
        bonusPoints:List[int] = [None,None],
        say:says=says(),
        changeDict:Union[None,dict] = None,
        unlock:Union[bool,None,str]=False
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
        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie = 0,0,0,0,0,0,0
        self.resistance,self.percing,self.critical = 0,0,0
        self.aspiration = aspiration
        self.weapon = weapon
        self.stars = 0
        self.skills = ["0","0","0","0","0"]
        self.majorPoints = [0,0,0,0,0,0,0]+[0,0,0]+[0,0,0,0,0]
        for a in range(0,len(skill)):
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
        self.element = element
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

    def changeLevel(self,level=1):
        self.level = level
        stats = self.allStats()
        allMax = [maxStrength,maxEndur,maxChar,maxAgi,maxPreci,maxIntel,maxMagie]
        for a in range(0,len(stats)):
            stats[a] = round(allMax[a][self.aspiration]*0.1+allMax[a][self.aspiration]*0.9*self.level/50)

        bPoints = level
        for a in self.bonusPoints:
            if a != None:
                distribute = min(30,bPoints)
                bPoints -= distribute
                stats[a] += distribute

        if self.changeDict != None:
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

        if self.level < 25:
            self.skills[4] = "0"
        if self.level < 20:
            self.skills[3] = "0"
        if self.level < 15:
            self.skills[2] = "0"
        if self.level < 10:
            self.skills[1] = "0"

        if self.level < 10:
            self.element = ELEMENT_NEUTRAL
        elif self.level < 20 and self.element in [ELEMENT_SPACE,ELEMENT_DARKNESS,ELEMENT_LIGHT,ELEMENT_LIGHT]:
            self.element = random.randint(0,3)

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