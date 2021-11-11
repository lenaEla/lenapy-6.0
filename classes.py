"""
base classes module
Here are grouped up the bases classes of the bot, and some very basic functions
"""

import emoji,pathlib,copy
from constantes import *

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
    """A class that is use to store the entity's stats for the post fight medals and inflate their ego"""
    def __init__(self):
        self.damageDeal = 0
        self.indirectDamageDeal = 0
        self.ennemiKill = 0
        self.allieResurected = 0
        self.shootHited = 1
        self.totalNumberShot = 1
        self.dodge = 1
        self.numberAttacked = 1
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

class option:
    """Very basic class. Only use in the "Select Option" window of manuals fights"""
    def __init__(self,name,emoji):
        self.name = name
        self.emoji = emoji

class weapon:
    """The main and only class for weapons"""
    def __init__(self,name : str,id : str,range,effectiveRange,power : int,sussess : int,price = 0,strength=0,endurance=0,charisma=0,agility=0,precision=0,intelligence=0,magie=0,resistance=0,percing=0,critical=0, repetition=1,emoji = None,area = AREA_MONO,effect=None,effectOnUse=None,target=ENNEMIS,type=TYPE_DAMAGE,orientation=[],needRotate = True,use=STRENGTH,damageOnArmor=1,affinity = None,message=None,negativeHeal=0,negativeDirect=0,negativeShield=0,negativeIndirect=0,negativeBoost=0,say=""):
        """rtfm"""
        self.name = name
        self.say = say
        self.id = id
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
            if self.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]:
                self.emoji='<:defDamage:885899060488339456>'
            elif self.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL]:
                self.emoji='<:defHeal:885899034563313684>'
            elif self.type in [TYPE_BOOST,TYPE_INVOC]:
                self.emoji='<:defSupp:885899082453880934>'
            elif self.type in [TYPE_ARMOR]:
                self.emoji='<:defarmor:895446300848427049>'
            elif self.type in [TYPE_MALUS]:
                self.emoji='<:defMalus:895448159675904001>'
            else:
                self.emoji='<:LenaWhat:760884455727955978>'
        else:
            self.emoji=emoji

        expectPrice = 100
        expectPrice += self.power * 4
        expectPrice += self.precision * 2
        if self.effect != None or self.effectOnUse != None:
            expectPrice += 200

        if expectPrice != price and price != 0:
            self.price = expectPrice

        if self.type == TYPE_DAMAGE and self.power != 0 and sussess != 0:
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

mainLibre = weapon("Main Libre","aa",RANGE_MELEE,AREA_CIRCLE_1,31,45,0,10,agility=10,repetition=5,emoji = emoji.fist)
splattershotJR = weapon("Liquidateur JR","af",RANGE_DIST,AREA_CIRCLE_3,34,35,0,agility=10,charisma=5,strength=5,repetition=5,emoji = emoji.splatJr)

class skill:
    """The main and only class for the skills"""
    def __init__ (self,name,id,types,price,power= 0,range = AREA_CIRCLE_5,conditionType = [],ultimate = False,secondary = False,emoji = None,effect=None,cooldown=1,area = AREA_MONO,sussess = 100,effectOnSelf=None,use=STRENGTH,damageOnArmor = 1,invocation=None,description=None,initCooldown = 1,shareCooldown = False,message=None,say="",repetition=1):
        """rtfm"""
        self.name = name
        self.repetition = repetition
        self.say = say
        self.id = id
        self.type = types
        self.power = power
        self.price = price
        self.conditionType = 0
        self.condition = conditionType
        self.ultimate = ultimate
        self.effect = effect
        self.range = range
        self.secondary = secondary
        self.cooldown = cooldown
        self.area = area
        self.sussess = sussess
        self.effectOnSelf = effectOnSelf
        self.use = use
        self.description = description
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

        if area == AREA_ALL_ALLIES or area == AREA_ALL_ENNEMIES or area == AREA_ALL_ENTITES:
            self.range = AREA_MONO

        if emoji == None:
            if self.type in [TYPE_DAMAGE,TYPE_INDIRECT_DAMAGE]:
                self.emoji='<:defDamage:885899060488339456>'
            elif self.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL]:
                self.emoji='<:defHeal:885899034563313684>'
            elif self.type in [TYPE_BOOST,TYPE_INVOC]:
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
            for stat in [strength,endurance,charisma,agility,precision,intelligence,magie,resistance,percing,critical,negativeHeal,negativeBoost,negativeDirect,negativeIndirect,negativeBoost]:
                sumStats += abs(stat)
            tempPrice = (sumStats-20)*5+100
            if effect != None:
                tempPrice += 200
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

        summation = 0
        for stat in [self.strength,self.charisma,self.agility,self.precision,self.intelligence,self.magie,self.percing,self.percing,self.critical]:
            if stat > 0:
                summation += stat
        for stat in [self.negativeHeal,self.negativeBoost,self.negativeShield,self.negativeDirect,self.negativeIndirect]:
            if stat < 0:
                summation += abs(stat)
        for stat in [self.endurance,self.resistance]:
            if stat > 0:
                summation += round(stat/2)

        cmpt = 0
        while 20 + cmpt * 10 <= summation:
            cmpt += 1
        self.minLvl = cmpt * 5

    def allStats(self):
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

    def havConds(self,user):
        return user.level >= self.minLvl

emojiMalus = [['<:ink1debuff:866828217939263548>','<:ink2debuff:866828296833466408>' ],['<:oct1debuff:866828253695705108>','<:oct2debuff:866828340470874142>'],['<:octariandebuff:866828390853247006>','<:octariandebuff:866828390853247006>']]

class effect:
    """The class for all skill's none instants effects and passive abilities from weapons and gears"""
    def __init__(self,name,id,stat=None,strength=0,endurance=0,charisma=0,agility=0,precision=0,intelligence=0,magie=0,resistance=0,percing=0,critical=0,emoji=None,overhealth = 0,redirection = 0,reject=None,description = "Pas de description",turnInit = 1,onTrigger = None,immunity=False,trigger=TRIGGER_PASSIVE,callOnTrigger = None,silent = False,power = 0,lvl = 1,type = TYPE_BOOST,ignoreImmunity = False,area=AREA_MONO,unclearable = False,stun=False,stackable=False,replique=None,translucide=False,untargetable=False,invisible=False,aggro=0):
        """rtfm"""
        self.name = name                    # Name of the effect
        self.id = id                        # The id. 2 characters
        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie,self.resistance,self.percing,self.critical= strength,endurance,charisma,agility,precision,intelligence,magie,resistance,percing,critical
        self.overhealth = overhealth        # Base shield power
        self.redirection = redirection      # Damage redirection ratio. Unuse yet
        self.reject = reject                # A list of the rejected effects
        self.description = description.format(power)      # A (quick) description of the effect
        self.turnInit = turnInit            # How many turn does the effect stay ?
        self.stat = stat                    # Wich stat is use by the effect ?
        self.onTrigger = onTrigger          # Unused
        if (overhealth > 0 or redirection > 0) and trigger==TRIGGER_PASSIVE:
            self.trigger = TRIGGER_DAMAGE   # If the effect give armor, he triggers automatiquely on damage
        else:
            self.trigger = trigger          # When does the effect triggers ?
        self.immunity = immunity            # Does the effect give a immunity ?
        self.callOnTrigger = callOnTrigger  # A list of effect given when the first one trigger
        self.silent = silent                # Do the effect is showed in the fight ?
        self.power = power                  # The base power for heals and indirect damages
        self.lvl = lvl                      # How many times can the effect trigger ?
        self.type = type                    # The type of the effect
        self.ignoreImmunity = ignoreImmunity    # Does the damage of this effect ignore immunities ?
        self.area=area                      # The area of effect of the effect
        self.unclearable = unclearable      # Does the effect is unclearable ?
        self.stun = stun                    # Does the effect is a stun effect ?
        self.stackable = stackable          # Does the effect is stackable ?
        self.replica = replique             # Does the effect is a replica of a skill ?
        self.replicaTarget = None           # The Target of the replica
        self.translucide = translucide      # Does the effect make the entity translucide ?
        self.untargetable = untargetable    # Does the effect make the entity untargetable ?
        self.invisible = invisible
        self.aggro = aggro

        if emoji == None:
            if self.type in [TYPE_BOOST]:
                self.emoji=[['<:ink1buff:866828199156252682>','<:ink2buff:866828277171093504>'],['<:oct1buff:866828236724895764>','<:oct2buff:866828319528583198>'],['<:octarianbuff:866828373345959996>','<:octarianbuff:866828373345959996>']]
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

    def setTurnInit(self,newTurn = 1):
        """Change the "turnInit" value. Why I need a function for that ?"""
        self.turnInit = newTurn
        return self

    def allStats(self):
        """Return a list with the mains stats of the weapon"""
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

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
    """The most important class. Store the data of a character"""
    def __init__(self,owner,name = "",level = 1,species=0,color=red):
        """rtfm. realy."""
        self.owner = owner
        self.name = str(name)
        self.level = int(level)
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
        self.weapon = splattershotJR
        self.weaponInventory = [splattershotJR,mainLibre]
        self.skills = ["0","0","0","0","0"]
        self.skillInventory = []
        self.stuff = [bbandeau,bshirt,bshoes]
        self.stuffInventory = [bbandeau,bshirt,bshoes]
        self.otherInventory = []
        self.procuration = []
        self.bonusPoints = [0,0,0,0,0,0,0]
        self.icon = None
        self.customColor = False
        self.element = ELEMENT_NEUTRAL
        self.deadIcon = None
        self.says = says()

    def have(self,obj):
        """Verify if the character have the object Obj"""
        return obj in self.weaponInventory or obj in self.skillInventory or obj in self.stuffInventory or obj in self.otherInventory

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

        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.resistance,self.percing,self.critical,self.magie = strength,endurance,charisma,agility,precision,intelligence,resistance,percing,critical,magie
        self.aspiration = aspiration
        self.weapon = weapon

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

def getColorId(user: char):
    """Return the color indice of the user. Only use for summons, now"""
    for b in range(0,len(colorId)):
        if user.color == colorId[b]:
            return b

incurable = effect("Incurable","incur",power=100,description="Diminue les soins reçus par la cible de **(puissance)**%.\n\nL'effet Incurable n'est pas cumulable\nSi un autre effet Incurable moins puissant est rajouté sur la cible, celui-ci est ignoré\nSi un autre effet Incurable plus puissant est rajouté, celui-ci remplace celui déjà présent",emoji=[['<:healnt:903595333949464607>','<:healnt:903595333949464607>'],['<:healnt:903595333949464607>','<:healnt:903595333949464607>'],['<:healnt:903595333949464607>','<:healnt:903595333949464607>']])

incur = []
for num in range(0,10):
    incurTemp = copy.deepcopy(incurable)
    incurTemp.power = 10*num
    incurTemp.name = "Incurable ({0})".format(10*num)
    incurTemp.description="Diminue les soins reçus par la cible de **{0}**%.\n\nL'effet Incurable n'est pas cumulable\nSi un autre effet Incurable moins puissant ou égal est rajouté sur la cible, celui-ci est ignoré\nSi un autre effet Incurable plus puissant est rajouté, celui-ci remplace celui déjà présent".format(10*num)
    incur.append(incurTemp)