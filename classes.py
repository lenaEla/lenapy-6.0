"""
base classes module
Here are grouped up the bases classes of the bot, and some very basic functions
"""

import emoji,pathlib
from constantes import *
from PIL import Image
import io

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
    """A class that is use to store the entity's stats for the post fight medals and inflate his ego"""
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

class option:
    """Very basic class. Only use in the "Select Option" window of manuals fights"""
    def __init__(self,name,emoji):
        self.name = name
        self.emoji = emoji

class weapon:
    """The main and only class for weapons"""
    def __init__(self,name : str,id : str,range,effectiveRange,power : int,sussess : int,price : int,strength=0,endurance=0,charisma=0,agility=0,precision=0,intelligence=0,resistance=0,percing=0,critical=0, repetition=1,emoji = emoji.loading,area = AREA_MONO,effect=None,effectOnUse=None,target=ENNEMIS,type=TYPE_DAMAGE,orientation=[],needRotate = True,use=STRENGTH,damageOnArmor=1):
        """rtfm"""
        self.name = name
        self.id = id
        self.range = range
        self.strength = strength
        self.endurance = endurance
        self.charisma = charisma
        self.agility = agility
        self.precision = precision
        self.intelligence = intelligence
        self.resistance = resistance
        self.percing = percing
        self.critical = critical
        self.power = power
        self.repetition = repetition
        self.emoji = emoji
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

    def allStats(self):
        """Return a list with the mains stats of the weapon"""
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence]

mainLibre = weapon("Main Libre","aa",RANGE_MELEE,AREA_CIRCLE_1,25,45,0,10,charisma=5,agility=10,repetition=5,emoji = emoji.fist)
splattershotJR = weapon("Liquidateur JR","af",RANGE_DIST,AREA_CIRCLE_3,20,35,0,agility=10,charisma=5,strength=5,repetition=5,emoji = emoji.splatJr)

class skill:
    """The main and only class for the skills"""
    def __init__ (self,name,id,types,price,power= 0,range = AREA_CIRCLE_5,conditionType = [],ultimate = False,secondary = False,emoji = emoji.loading,effect=None,cooldown=1,area = AREA_MONO,sussess = 100,effectOnSelf=None,use=STRENGTH,damageOnArmor = 1,invocation=None,description=None,initCooldown = 1,shareCooldown = False):
        """rtfm"""
        self.name = name
        self.id = id
        self.type = types
        self.power = power
        self.price = price
        self.conditionType = 0
        self.condition = conditionType
        self.ultimate = ultimate
        self.emoji = emoji
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
                listExclu = ["weapon","aspiration"]
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

    def havConds(self,user=0):
        """Verify if the User have the conditions to equip the skill"""
        if self.condition != []:
            conds = self.condition
            if conds[0] == 0:
                if conds[1] == 0:
                    if user.weapon != findWeapon(conds[2]):
                        return False
                else:
                    if user.aspiration != conds[2]:
                        return False
            elif conds[0] == 1:
                userstats = user.allStats()
                if userstats[conds[1]] < conds[2]:
                    return False
            elif conds[0] == 2:
                if conds[1] == 0:
                    if user.weapon == findWeapon(conds[2]):
                        return False
                else:
                    for a in user.skills:
                        if a != None and a!="0":
                            if a == conds[2]:
                                return False
        return True
     
class stuff:
    """The main and only class for all the gears"""
    def __init__(self,name,id,type,price,strength=0,endurance=0,charisma=0,agility=0,precision=0,intelligence=0,resistance=0,percing=0,critical=0,emoji = emoji.loading,effect=None,orientation = [],position=0):
        """rdtm"""
        self.name = name
        self.id = id
        self.price = price
        self.type = type
        self.strength = strength
        self.endurance = endurance
        self.charisma = charisma
        self.agility = agility
        self.precision = precision
        self.intelligence = intelligence
        self.resistance = resistance
        self.percing = percing
        self.critical = critical
        self.emoji = emoji
        self.effect = effect
        self.position = position

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

    def allStats(self):
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence]

class effect:
    """The class for all skill's none instants effects and passive abilities from weapons and gears"""
    def __init__(self,name,id,stat=None,strength=0,endurance=0,charisma=0,agility=0,precision=0,intelligence=0,resistance=0,percing=0,critical=0,emoji=[['<:ink1buff:866828199156252682>','<ink2buff:866828277171093504>'],['<:oct1buff:866828236724895764>','<:oct2buff:866828319528583198>'],['<:octarianbuff:866828373345959996>','<:octariandebuff:866828390853247006>']],overhealth = 0,redirection = 0,reject=None,description = "Pas de description",turnInit = 1,onTrigger = None,immunity=False,trigger=TRIGGER_PASSIVE,callOnTrigger = None,silent = False,power = 0,lvl = 1,type = TYPE_BOOST,ignoreImmunity = False,area=AREA_MONO,unclearable = False,stun=False,stackable=False):
        """rtfm"""
        self.name = name
        self.id = id
        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.resistance,self.percing,self.critical= strength,endurance,charisma,agility,precision,intelligence,resistance,percing,critical
        self.overhealth = overhealth
        self.redirection = redirection
        self.emoji = emoji
        self.reject = reject
        self.description = description
        self.turnInit = turnInit
        self.stat = stat
        self.onTrigger = onTrigger
        self.trigger = trigger
        self.immunity = immunity
        self.callOnTrigger = callOnTrigger
        self.silent = silent
        self.power = power
        self.lvl = lvl
        self.type = type
        self.ignoreImmunity = ignoreImmunity
        self.area=area
        self.unclearable = unclearable
        self.stun = stun
        self.stackable = stackable

    def setTurnInit(self,newTurn = 1):
        """Change the "turnInit" value. Why I need a function for that ?"""
        self.turnInit = newTurn
        return self

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
        self.name = name
        self.level = level
        self.exp = 0
        self.currencies = 0
        self.species = species
        self.color = color
        self.team = 0
        self.gender = GENDER_OTHER
        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence = 0,0,0,0,0,0
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
        self.bonusPoints = [0,0,0,0,0,0]
        self.icon = None
        self.customColor = False
        self.element = ELEMENT_NEUTRAL

    def have(self,obj):
        """Verify if the character have the object Obj"""
        return obj in self.weaponInventory or obj in self.skillInventory or obj in self.stuffInventory or obj in self.otherInventory

    def allStats(self):
        """Return a list of all main stats of the character"""
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence]

class invoc:
    """The main class for summons. Similar the "char" class, but with only the fight's necessery attributs"""
    def __init__(self,name,strength,endurance,charisma,agility,precision,intelligence,resistance,percing,critical,aspiration,icon,weapon,skills=[],gender=GENDER_OTHER,description="Pas de description"):
        self.name = name
        self.level = 0
        self.team = 0
        self.gender = gender
        self.color = 0
        self.species = 1

        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.resistance,self.percing,self.critical = strength,endurance,charisma,agility,precision,intelligence,resistance,percing,critical
        self.aspiration = aspiration
        self.weapon = weapon

        self.description = description
        
        while len(skills)<5:
            skills.append("0")

        self.skills = skills
        self.icon = icon
        self.customColor = False

    def allStats(self):
        """Return a list """
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence]

def getColorId(user: char):
    """Return the color indice of the user. Only use for summons, now"""
    for b in range(0,len(colorId)):
        if user.color == colorId[b]:
            return b