"""
base classes module
Here are grouped up the bases classes of the bot, and some very basic functions
"""
import pathlib,copy,random,interactions
from constantes import *
from typing import List, Union, Dict

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
            - damageBoosted : The number of damage another entity has done with a entity's boost effects
            - damageDodged : The number of damage another entity has reduce with a entity's boost effects
            - shieldGiven : The number of Armor HP gave by the entity
            - estialba : The number of damage the entity have done with a "Estialba's poison" effects
            - bleeding : The number of damage the entity have done with a "Bleeding" effects
            - underBoost : The number of damage the entity have done with a another entity's boost effects
            - selfBurn : The number of damage the entity have done on him-self
    """
    def __init__(self):
        self.damageDeal, self.indirectDamageDeal = 0, 0
        self.damageRecived = 0
        self.ennemiKill = 0
        self.allieResurected = 0
        self.shootHited = 0
        self.totalNumberShot = 0
        self.dodge = 0
        self.numberAttacked = 0
        self.heals, self.lifeSteal, self.shieldGived = 0, 0, 0
        self.crits = 0
        self.survival = 0
        self.damageOnShield, self.damageBoosted, self.damageDodged, self.underBoost = 0, 0, 0, 0
        self.summonBoost = 0
        self.estialba = 0
        self.bleeding = 0
        self.selfBurn = 0
        self.headnt = False
        self.friendlyfire = 0
        self.fullskip, self.turnSkipped = True, 0
        self.armoredDamage = 0
        self.damageBlocks,self.damageResisted,self.healReduced, self.healIncreased = 0, 0, 0, 0
        self.maxHpReduced, self.blockCount, self.nbHeal, self.critHeal = 0, 0, 0, 0
        self.sufferingFromSucess, self.lauthingAtTheFaceOfDeath = False, False
        self.nbLB, self.nbSummon = 0, 0
        self.summonDmg, self.summonHeal = 0, 0
        self.damageProtected = 0
        self.lbDamage = 0
        self.healingRecived = 0
        self.hpPerTurn, self.dmgPerTurn, self.healPerTurn, self.armorPerTurn, self.suppPerTurn, self.actionUsed = {}, {}, {}, {}, {}, {}

    def __str__(self):
        return self.__dict__.__str__().replace("{","{\n").replace(",",",\n")

class option:
    """Very basic class. Only use in the "Select Option" window of manuals fights"""
    def __init__(self,name,emoji):
        self.name = name
        self.emoji = emoji

INC_START_FIGHT, INC_START_TURN, INC_KILL, INC_ENEMY_KILLED, INC_ALLY_KILLED, INC_DEAL_DAMAGE, INC_ENEMY_DAMAGED, INC_ALLY_DAMAGED, INC_DEAL_HEALING, INC_ENEMY_HEALED, INC_ALLY_HEALED, INC_USE_SKILL, INC_EFFECT_TRIGGERED, INC_ON_SELF_CRIT, INC_ON_ALLY_CRIT, INC_USE_ELEMENT_SKILL, INC_USE_GROUP_SKILL, INC_JUMP_PER_CASE, INC_PER_PUSH, INC_COLISION, INC_JUMP_BACK, INC_LIFE_STEAL = tuple(range(22))

incCondsStr = ["Au début du combat","En début de tour","Lorsque vous éliminez un adversaire","Lorsqu'un ennemi est éliminé","Lorsqu'un allié est éliminé","Lorsque vous infligez des dégâts par pourcentage de PV retiré à la cible","Par pourcentage de vie perdue par un ennemi","Par pourcentage de vie perdue par un allié","Par pourcentage de PV soigné par rapport aux PV Max de la cible","Par pourcentage de vie soignée d'un ennemi","Par pourcentage de vie soignée d'un allié","Lors de l'utilisation de certaines compétences","Lors du déclanchement de certains effets","Lorsque vous réalisez un coup critique","Lors d'un coup critique allié","En utilisant des compétences de l'élément suivant","En utilisant des compétences du groupe suivant","Par cases parcourue lors d'une téléportation au corps à crops d'un combattant","Par cases parcourues par un combattant que vous avez repoussé","En infligeant des dégâts de colisions","Par cases parcourues lors d'un saut en arrière","Par pourcentage de vie soigné avec du Vol de Vie"]

class jaugeConds:
    """A sub class for any jauge effects. Define conditions"""
    def __init__(self,type:int,value:int,add:Union[None,List]=None):
        self.type = type
        self.value = value
        self.add = add

class jaugeValue:
    """A stucturing class for any jauge effects. Define conditions"""
    def __init__(self,emoji:List[str],conds:List[jaugeConds]):
        self.emoji = emoji
        self.conds = conds

defaultVarsEffInit: Dict[str, Union[None,int,str]] = {"strength":0, "endurance":0, "charisma":0, "agility":0, "precision":0, "intelligence":0, "magie":0, "resistance":0, "percing":0, "critical":0, "emoji":None, "overhealth":0, "redirection":0, "reject":None, "description":"Pas de description", "turnInit":1, "immunity":False, "trigger":TRIGGER_PASSIVE, "callOnTrigger":None, "silent":False, "power":0, "lvl":None, "type":TYPE_BOOST, "ignoreImmunity":False, "area":AREA_MONO, "unclearable":False, "stun":False, "stackable":False, "replique":None, "translucide":False, "untargetable":False, "invisible":False, "aggro":0, "absolutShield": False, "lightShield": False, "onDeclancher": False, "inkResistance":0, "dmgUp": 0, "critDmgUp": 0, "healUp": 0, "critHealUp": 0, "block":0, "jaugeValue":None, "denieWeap": False, "lifeSteal":0,"lifeStealOnOn": False,"counterOnDodge":0,"dodge": 0,"replace":False,"effPrio": 0,"counterOnBlock":0,"iaPow": 0,"armorDmgBonus": 0,"incHealJauge": True,"thornEff": False,"afterchocEff": False,"silentRemove": False}
defaultKeysEff = list(defaultVarsEffInit.keys())

class effect:
    """The class for all skill's none instants effects and passive abilities from weapons and gears"""
    def __init__(self,name,id,stat=None,**kwargs):
        defaultVars = copy.deepcopy(defaultVarsEffInit)
        for key in kwargs:
            defaultVars[key] = kwargs[key]
            if key not in defaultKeysEff:
                raise ValueError("{0} : Key {1} not matching".format(name,key))

        #emoji=None,overhealth = 0,redirection = 0,reject=None,description = "Pas de description",turnInit = 1,immunity=False,trigger=TRIGGER_PASSIVE,callOnTrigger = None,silent = False,power:int = 0,lvl = None,type = TYPE_BOOST,ignoreImmunity = False,area=AREA_MONO,unclearable = False,stun=False,stackable=False,replique=None,translucide=False,untargetable=False,invisible=False,aggro=0,absolutShield = False, lightShield = False,onDeclancher = False,inkResistance=0,dmgUp = 0, critDmgUp = 0, healUp = 0, critHealUp = 0, block=0, jaugeValue:Union[jaugeValue,None]=None, denieWeap = False, lifeSteal=0, lifeStealOnOn = False, counterOnDodge=0, dodge = 0,replace=False, effPrio = 0, counterOnBlock=0, iaPow = 0, armorDmgBonus = 0, incHealJauge = True, thornEff = False, afterchocEff = False, silentRemove = False

        self.name, self.id = name, id                    # Name of the effects
        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie,self.resistance,self.percing,self.critical= defaultVars["strength"],defaultVars["endurance"],defaultVars["charisma"],defaultVars["agility"],defaultVars["precision"],defaultVars["intelligence"],defaultVars["magie"],defaultVars["resistance"],defaultVars["percing"],defaultVars["critical"]
        self.overhealth = defaultVars["overhealth"]        # Base shield power
        self.redirection = defaultVars["redirection"]      # Damage redirection ratio. Unuse yet
        self.block = defaultVars["block"]
        self.reject = copy.deepcopy(defaultVars["reject"])                # A list of the rejected effects
        self.description = defaultVars["description"]      # A (quick) description of the effects
        self.turnInit = defaultVars["turnInit"]            # How many turn does the effects stay ?
        self.stat = stat                    # Wich stat is use by the effects ?
        
        self.trigger:int = defaultVars["trigger"]          # When does the effects triggers ?
        if (self.overhealth > 0 or self.redirection > 0) and self.trigger==TRIGGER_PASSIVE:
            self.trigger:int = TRIGGER_DAMAGE   # If the effects give armor, he triggers automatiquely on damage
        self.immunity:bool = defaultVars["immunity"]            # Does the effects give a immunity ?
        self.callOnTrigger = defaultVars["callOnTrigger"]  # A list of effects given when the first one trigger
        self.silent:bool = defaultVars["silent"]                # Do the effects is showed in the fight ?
        self.power:int = defaultVars["power"]                  # The base power for heals and indirect damages
        self.lifeSteal, self.lifeStealOnOn = defaultVars["lifeSteal"], defaultVars["lifeStealOnOn"]
        self.type:int = defaultVars["type"]                    # The type of the effects
        self.ignoreImmunity:bool = defaultVars["ignoreImmunity"]    # Does the damage of this effects ignore immunities ?
        self.area= defaultVars["area"]                      # The area of effects of the effects
        self.unclearable:bool = defaultVars["unclearable"]      # Does the effects is unclearable ?
        self.stun:bool = defaultVars["stun"]                    # Does the effects is a stun effects ?
        self.stackable:bool = defaultVars["stackable"]          # Does the effects is stackable ?
        self.replica:Union[None,skill] = defaultVars["replique"]             # Does the effects is a replica of a skill ?
        if self.replica != None:
            self.name = name.format(replicaName=self.replica.name)
        self.translucide:bool = defaultVars["translucide"]      # Does the effects make the entity translucide ?
        self.untargetable:bool = defaultVars["untargetable"]    # Does the effects make the entity untargetable ?
        self.invisible:bool = defaultVars["invisible"]
        self.aggro:int = defaultVars["aggro"]
        self.lightShield:bool = defaultVars["lightShield"]
        self.absolutShield:bool = defaultVars["absolutShield"]
        self.onDeclancher:bool = defaultVars["onDeclancher"]
        self.inkResistance = defaultVars["inkResistance"]
        self.replace = defaultVars["replace"]
        self.dmgUp, self.critDmgUp, self.healUp, self.critHealUp, self.jaugeValue, self.denieWeap = defaultVars["dmgUp"], defaultVars["critDmgUp"], defaultVars["healUp"], defaultVars["critHealUp"], defaultVars["jaugeValue"], defaultVars["denieWeap"]
        self.counterOnDodge, self.dodge, self.counterOnBlock = defaultVars["counterOnDodge"], defaultVars["dodge"], defaultVars["counterOnBlock"]
        self.prio, self.armorDmgBonus, self.icon = defaultVars["effPrio"], defaultVars["armorDmgBonus"], ""
        self.incHealJauge = defaultVars["incHealJauge"]
        self.thornEff, self.afterchocEff, self.iaPow, self.emoji = defaultVars["thornEff"], defaultVars["afterchocEff"], defaultVars["iaPow"], defaultVars["emoji"]

        self.lvl:int = defaultVars["lvl"]                      # How many times can the effects trigger ?
        if self.lvl == None:
            self.lvl = [[[self.turnInit,99][self.turnInit==-1],0][self.jaugeValue != None],1][self.trigger==TRIGGER_ON_REMOVE]

        if self.iaPow == 0:          # Auto generate IA power if none is given
            iaPow = 0
            if self.callOnTrigger == None:
                tstats = 0
                for staty in [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.magie,self.resistance,self.percing,self.critical]:
                    iaPow += staty * [1,5][self.stat not in [None,FIXE,PURCENTAGE]]
                    tstats += staty
                iaPow += self.overhealth
                iaPow += ((abs((self.inkResistance+self.overhealth)*[1,3][self.stat not in [None,FIXE,PURCENTAGE]]) + abs(self.aggro) + self.block + self.counterOnDodge + self.critDmgUp + self.critHealUp + self.dmgUp + self.healUp + self.redirection) // 3)
                iaPow += self.power * self.lvl

                if self.power > 0 and tstats == 0 and self.stat not in [None,FIXE,PURCENTAGE] and self.type in [TYPE_BOOST,TYPE_MALUS]:
                    iaPow += self.power * 5

                try:
                    iaPow += self.callOnTrigger.iaPow
                except:
                    pass
                try:
                    iaPow += self.callOnTrigger.skills.iaPow * self.callOnTrigger.lifeTime
                except:
                    pass
            elif self.callOnTrigger.__class__ not in [str,None]:
                try:
                    iaPow = self.callOnTrigger.iaPow
                except Exception as e:
                    print(self.name,e)
                    pass

            self.iaPow = iaPow
        self.silentRemove = defaultVars["silentRemove"]

        if self.replica != None and self.prio == 0:
            self.prio = 2
        elif self.immunity or self.translucide or self.invisible or self.untargetable:
            self.prio = 1.5

        if self.reject != None and self.id in self.reject:
            self.reject.remove(self.id)

        if self.emoji == None and self.replica != None:
            self.emoji = uniqueEmoji(self.replica.emoji)
        elif self.emoji == None:
            if self.immunity:
                self.emoji = '<:immunity:1063118365738160209>'
            elif self.inkResistance > 0:
                self.emoji=sameSpeciesEmoji('<:inkResB:1143285391009529896>','<:inkResR:1143285464770543636>')
            elif self.inkResistance < 0:
                self.emoji=sameSpeciesEmoji('<:indVulnB:1143285431077707828>','<:indVulnR:1143285490510999584>')
            elif self.stat == PURCENTAGE and self.resistance < 0:
                self.emoji=uniqueEmoji(statsEmojis[PERCING])
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

        if self.emoji.__class__ == str:
            self.emoji = uniqueEmoji(self.emoji)

    def __str__(self) -> str:
        return "{0} __{1}__".format(self.emoji[0][0], self.name)

    def setTurnInit(self,newTurn = 1):
        """Change the "turnInit" value. Why I need a function for that ?"""
        self.turnInit = newTurn
        return self

    def allStats(self):
        """Return a list with the mains stats of the effect"""
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

# Basic effects :
incurable = effect("Incurable","incur",type=TYPE_MALUS,power=100,replace=True,description="Diminue les soins reçus par la cible de **{0}**%.\nSeul l'effet Incurable le plus puissant est pris en compte",emoji=sameSpeciesEmoji('<:incurB:1143285329391001762>','<:incurR:1143285244477317233>'),stackable=True)
armorPackEff = effect("Armure","armorPack", stat = INTELLIGENCE,overhealth=35,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
vulne = effect("Dégâts subis augmentés","vulne",power=100,emoji=sameSpeciesEmoji("<a:defDebuffB:954544469649285232>","<a:defDebuffR:954544494110441563>"),type=TYPE_MALUS,stackable=True,description="Augmente les dégâts reçus de **{0}%**")
defenseUp = effect("Dégâts subis réduits","defenseUp",stackable=True,emoji=sameSpeciesEmoji('<a:defBuffB:954537632543682620>','<a:defBuffR:954538558541148190>'),description="Réduit les dégâts reçus de **{0}%**")
dmgUp = effect("Dégâts infligés augmentés","dmgUp",stackable=True,emoji=sameSpeciesEmoji('<a:dmgBuffB:954429227657224272>','<a:dmgBuffR:954429157079654460>'),description="Augmente les dégâts infligés de **{0}%**")
dmgDown = effect("Dégâts infligés réduits","dmgDown",power=100,emoji=sameSpeciesEmoji("<a:dmgDebuffB:954431054654087228>","<a:dmgDebuffR:954430950668914748>"),type=TYPE_MALUS,stackable=True,description="Réduit les dégâts infligés de **{0}%**")
partage = effect("Partage","share",power=100,turnInit=-1,stackable=True,emoji=sameSpeciesEmoji("<:sharaB:931239879852032001>","<:shareR:931239900018278470>"),area=AREA_DONUT_2,description="Lorsque le porteur reçoit des soins monocibles, cet effet soigne ses alliés proche de l'équivalent de **{0}%** des soins reçus par le porteur")
partage.iaPow = 35
healDoneBonus = effect("Soins réalisés augmentés","healBonus",description="Augmente les soins réalisés par le lanceur de **{0}%**",emoji='<:largesse:1086390291055005736>')
intargetable = effect("Inciblable","untargetable",untargetable=True,emoji=uniqueEmoji('<:untargetable:899610264998125589>'),description="Cet entité deviens inciblable directement",turnInit=2)
silenceEff = effect("InCapacité","silenceEff",description="Empèche l'utilisation de compétence durant la durée de l'effet",type=TYPE_MALUS,emoji='<:silenced:975746154270691358>',effPrio = 1)
absEff = effect("Absorbtion","absEff",description="Augmente les soins reçus par le porteur de **{0}%**",emoji=sameSpeciesEmoji('<:absB:1143285351608221838>','<:absR:1143285293240291368>'),stackable=True)
chained = effect("Enchaîné","chained",emoji='<:chained:982710848487317575>',description="Empêche tous déplacements de la cible, que ce soit par elle-même que part une compétence",type=TYPE_MALUS,dodge=-35,effPrio = 1)
upgradedLifeSteal = effect("Augmentation du plafond de vol de vie","lifeSteal+",power=100,turnInit=-1,silent=True,unclearable=True,description="Augmente de **POWER%** le plafond de vol de vie",emoji=sameSpeciesEmoji("<:lifeStealUpB:1058795614755885066>","<:lifeStealUpR:1058795585873911850>"))
imuneLightStun = effect("Immunité à l'étourdissement","imuneLightStun",description="Le porteur ne peut plus être étourdi.\nCertains effects étourdissants ignorent cette immunitée",emoji='<:antiStun:1005128649613262968>',turnInit=5)
lightStun = effect("Etourdissement","lightStun",stun=True,type=TYPE_MALUS,description="Le porteur de l'effet est étourdi.\n\nSans effet sur les boss Stand Alone, les boss de Raid ainsi que certains ennemis.\nInfligé à un joueur ou un allié temporaire, ce dernier bénéficie par la suite d'une immunité aux étourdissements durant **{0} tours**.".format(imuneLightStun.turnInit),emoji='<:stun:1005128631888117852>',reject=[imuneLightStun.id],effPrio=3)

ENEMYIGNORELIGHTSTUN = ["OctoBOUM","Liu","Prétorien Glyphique"]

ailillUpLifeSteal, clemPosUpLifeSteal, clemExUpLifeSteal = copy.deepcopy(upgradedLifeSteal), copy.deepcopy(upgradedLifeSteal), copy.deepcopy(upgradedLifeSteal)
ailillUpLifeSteal.power, clemPosUpLifeSteal.power, clemExUpLifeSteal.power = 50,50,10000
upLifeStealNames, upLifeStealEff = ["Clémence Exaltée","Clémence pos.","Ailill"], [clemExUpLifeSteal,clemPosUpLifeSteal,ailillUpLifeSteal]

for eff in upLifeStealEff:
    eff.description = eff.description.replace("POWER",str(eff.power))

upLifeStealEff[0].description = upLifeStealEff[0].description + "\n\nDe plus, une partie des soins réalisés par vol de vie lorsque les PVs sont au maximum sont converties en armure"

constEff = effect("Constitution","constEff",description="Augmente les PVs maximums de la cible.\nLe pourcentage de PV actuels est concervé lors de la pose de l'effet mais aucun PV est perdu lorsque l'effet est retiré, sauf si le nombre de PV exède les PV maximums",emoji=sameSpeciesEmoji('<:constB:1028695344059518986>','<:constR:1028695415966679132>'))
aconstEff = effect("Anti-constitution","aconstEff",description="Réduit les PVs maximums de la cible\nLe pourcentage de PV actuels est concervé lors de la pose de l'effet mais aucun PV est perdu lorsque l'effet est retiré, sauf si le nombre de PV exède les PV maximums",emoji=sameSpeciesEmoji('<:ConB:1028695381447557210>','<:ConR:1028695463651717200>'))
armorGetMalus = effect("Friable","armorRecivedDown",type=TYPE_MALUS,description="Réduit de **{0}%** l'armure reçu par le porteur",stackable=True,emoji=sameSpeciesEmoji("<:abB:934600555916050452>","<:abR:934600570633867365>"))

incur = []
for num in range(0,10):
    incurTemp = copy.deepcopy(incurable)
    incurTemp.power = 10*num
    incurTemp.name = "Incurable ({0})".format(10*num)
    incur.append(incurTemp)

vulneTabl = []
for num in range(0,10):
    vulneTemp = copy.deepcopy(vulne)
    vulneTemp.power = 10*num
    vulneTemp.name += " ({0})".format(10*num)
    vulneTemp.description="Augmente les dégâts subis par le porteur de **{0}%**"
    vulneTabl.append(vulneTemp)

shareTabl = []
for num in range(0,10):
    shareTemp = copy.deepcopy(partage)
    shareTemp.power = 10*num
    shareTemp.name = "Partage ({0})".format(10*num)
    shareTabl.append(shareTemp)


WEAPON_PRIORITY_LOW, WEAPON_PRIORITY_DEFAULT, WEAPON_PRIORITY_HIGH, WEAPON_PRIORITY_LOWEST = -1,0,1,-2

class defaultObj():
    def getSummary(self):
        """Return a strin gwith basic infos on the weapon"""
        if self.__class__==weapon:
            toReturn = ""
            iconMsg = statsEmojis[[ACT_DIRECT_FULL,ACT_HEAL_FULL][self.type==TYPE_HEAL]]
            toReturn += "{0} {1}{2} ({6}) <:targeted:912415337088159744> {5}% | {3} {4}\n".format(iconMsg,self.power,[" x{0}".format(self.repetition),""][self.repetition <= 1],rangeAreaEmojis[self.effectiveRange],areaEmojis[self.area],self.accuracy,statsEmojis[self.use])
            stats = [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie,self.resistance,self.percing,self.critical,self.negativeHeal*-1,self.negativeBoost*-1,self.negativeShield*-1,self.negativeDirect*-1,self.negativeIndirect*-1]
            for cmpt in range(0,len(stats)):
                if stats[cmpt] != 0:
                    toReturn += "{0}{1}{2}, ".format(statsEmojis[cmpt],["","+"][stats[cmpt]>0],stats[cmpt])
            if len(toReturn)> 0 and toReturn[-1] == ", ":
                toReturn = toReturn[:-1]
            if self.affinity != None:
                toReturn += elemEmojis[self.affinity]
            toAdd = ""

            if type(self.effects) == effect:
                    toAdd += "__Passif__ : {0} {1}".format(self.effects.emoji[0][0],self.effects.name)
            if type(self.effectOnUse) == effect:
                    toAdd += "{0}__Effet sur la cible__ : {1} {2}".format(["","\n"][toAdd != ""],self.effectOnUse.emoji[0][0],self.effectOnUse.name)
            
            if toAdd != "":
                toReturn += "\n" + toAdd

            return toReturn
        elif self.__class__==skill:
            """Return a sting with basic infos"""
            toReturn, tpower, tcasttime, treplay, actSkill = "", 0, 0, 1, self
            if actSkill.become == None:
                while type(actSkill.effectOnSelf) == effect and type(actSkill.effectOnSelf.replica) == skill:
                    if actSkill.replay:
                        treplay += 1
                    else:
                        tcasttime += 1
                    tpower += actSkill.power
                    actSkill = actSkill.effectOnSelf.replica
                if actSkill == self:
                    tpower = self.power
                else:
                    tpower += actSkill.power
            else:
                moyPow = 0
                for skilly in actSkill.become:
                    actSkill2 = skilly
                    while type(actSkill2.effectOnSelf) == effect and type(actSkill2.effectOnSelf.replica) == skill:
                        moyPow += actSkill.power
                        actSkill2 = actSkill2.effectOnSelf.replica
                    if actSkill2 == actSkill:
                        moyPow += actSkill.power
                    else:
                        moyPow += actSkill2.power
                tpower = int(moyPow)/len(actSkill.become)

            if actSkill.type in [TYPE_DAMAGE,TYPE_HEAL]:
                iconMsg = [statsEmojis[[ACT_DIRECT_FULL,ACT_HEAL_FULL][actSkill.type==TYPE_HEAL]], "{0} 🕑 - {1}".format(tcasttime, statsEmojis[[ACT_DIRECT_FULL,ACT_HEAL_FULL][actSkill.type==TYPE_HEAL]])][tcasttime>0]
                if actSkill == self:
                    toReturn += "{0} {1}{2}".format(iconMsg,actSkill.power,[" x{0}".format(actSkill.repetition),""][actSkill.repetition <= 1])
                else:
                    toReturn += "{0} {1}{2}{3}".format(iconMsg,tpower,[" x{0}".format(actSkill.repetition),""][actSkill.repetition <= 1],["","/{0}".format(treplay)][treplay>1])
            elif actSkill.type in [TYPE_INDIRECT_DAMAGE,TYPE_INDIRECT_HEAL]:
                iconMsg = [statsEmojis[[ACT_INDIRECT_FULL,ACT_HEAL_FULL][actSkill.type==TYPE_INDIRECT_HEAL]], "{0} 🕑 - {1}".format(tcasttime, statsEmojis[[ACT_INDIRECT_FULL,ACT_HEAL_FULL][actSkill.type==TYPE_INDIRECT_HEAL]])][tcasttime>0]
                if type(actSkill.effects[0]) == effect:
                    if actSkill == self:
                        toReturn += "{0} {1}/{2}".format(iconMsg,int(actSkill.effects[0].power*actSkill.effects[0].lvl*actSkill.effPowerPurcent/100),actSkill.effects[0].lvl)
                    else:
                        toReturn += "{0} {1}/{2}".format(iconMsg,int(actSkill.effects[0].power*actSkill.effects[0].lvl*actSkill.effPowerPurcent/100),actSkill.effects[0].lvl,["","/{0}".format(treplay)][treplay>1])
                else:
                    toReturn += "{0} ?/?".format(iconMsg)
            elif actSkill.type in [TYPE_BOOST,TYPE_MALUS]:
                toReturn += [statsEmojis[ACT_BOOST_FULL], "{0} 🕑 - {1}".format(tcasttime, statsEmojis[ACT_BOOST_FULL])][tcasttime>0]
            elif actSkill.type == TYPE_ARMOR:
                toReturn += [statsEmojis[ACT_SHIELD_FULL], "{0} 🕑 - {1}".format(tcasttime, statsEmojis[ACT_SHIELD_FULL])][tcasttime>0]
            elif actSkill.type in [TYPE_SUMMON,TYPE_DEPL]:
                toReturn += "<:sprink1:887747751339757599>"
            elif actSkill.type == TYPE_RESURECTION:
                toReturn += '<:renisurection:873723658315644938>'
            else:
                toReturn += "<:i1b:866828199156252682>"

            if self.type == TYPE_PASSIVE:
                toReturn = "*Passif*"
            toAdd = ""
            if actSkill.use != None and actSkill.use <= MAGIE:
                toAdd += statsEmojis[actSkill.use]
            if actSkill.useActionStats != None:
                toAdd += statsEmojis[actSkill.useActionStats+CRITICAL+1]
            if toAdd != "":
                toReturn += " ({0})".format(toAdd)

            if actSkill.condition != []:
                tabl = [None,aspiEmoji,elemEmojis][actSkill.condition[1]]
                toReturn += " | {0}".format(tabl[actSkill.condition[2]])
            
            effarea = ""
            if actSkill.type in [TYPE_INDIRECT_DAMAGE,TYPE_INDIRECT_HEAL] and type(actSkill.effects[0]) == effect:
                effarea = " ({0})".format(areaEmojis[actSkill.effects[0].area])

            if not(self.type == TYPE_PASSIVE):
                toReturn += " | {0} {1}{4} | 🕓 {2}{3}{4}".format(rangeAreaEmojis[actSkill.range],areaEmojis[actSkill.area],actSkill.cooldown,[""," ⭐"][actSkill.ultimate],effarea,[""," ✨"][actSkill.replay])

            if actSkill.description not in [None,'']:
                lines = actSkill.description.splitlines()
                toReturn += "\n> " + lines[0]
                if len(lines)>1:
                    toReturn += "\n> (...)"

            return toReturn
        elif self.__class__==stuff:
            """Return a string with the basics gear info"""
            stats, temp = [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie,self.resistance,self.percing,self.critical,self.negativeHeal*-1,self.negativeBoost*-1,self.negativeShield*-1,self.negativeDirect*-1,self.negativeIndirect*-1], ""
            for cmpt in range(0,len(stats)):
                if stats[cmpt] != 0:
                    temp += "{0}{1}{2}, ".format(statsEmojis[cmpt],["","+"][stats[cmpt]>0],stats[cmpt])
            if len(temp)> 0 and temp[-1] == ",":
                temp = temp[:-1]
            if self.affinity != None:
                temp += elemEmojis[self.affinity]

            if self.orientation not in [None,""]:
                temp += "\n{0}".format(self.orientation)

            if type(self.effects) == effect:
                temp += "\n{1} {0}".format(self.effects.name, self.effects.emoji[0][0])
            return temp
        elif self.__class__ ==other:
            return "> "+self.description.splitlines()[0]
        else:
            return "Une erreur est survenue : {0}".format(self.__class__.__str__)

class weapon(defaultObj):
    """The main and only class for weapons"""
    def __init__(self,name : str,id : str,range,effectiveRange,power : int,accuracy : int,price = 0,strength=0,endurance=0,charisma=0,agility=0,precision=0,intelligence=0,magie=0,resistance=0,percing=0,critical=0, repetition=1,emoji = None,area = AREA_MONO,effects:Union[None,effect]=None,effectOnUse=None,target=ENEMIES,type=TYPE_DAMAGE,orientation=[],needRotate = True,use=STRENGTH,damageOnArmor=1,affinity = None,message=None,negativeHeal=0,negativeDirect=0,negativeShield=0,negativeIndirect=0,negativeBoost=0,say="",ignoreAutoVerif=False,taille=1,effPowerPurcent=100,priority=WEAPON_PRIORITY_DEFAULT):
        """rtfm"""
        self.name:str = name
        self.say:Union[str,List[str]] = say
        self.id:str = id
        self.priority = priority
        try:
            self.id.isdigit()
        except:
            print("Invalid id : "+self.name)
        self.range = range
        self.strength, self.endurance, self.charisma, self.agility, self.precision, self.intelligence, self.magie = strength, endurance, charisma, agility, precision, intelligence, magie
        self.resistance, self.percing, self.critical = resistance, percing, critical
        self.ignoreAutoVerif = ignoreAutoVerif
        self.minLvl = 1
        self.aoeLifeSteal:int = 0
        self.aoeArmorConvert:int = 0
        self.garCrit:bool = False

        self.power = power
        self.repetition = repetition
        self.accuracy = accuracy
        self.price = price
        self.area = area
        self.effects = effects
        self.effectiveRange = effectiveRange
        self.effectOnUse, self.effPowerPurcent = effectOnUse, effPowerPurcent

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

        # Do I use it anymore ?
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

        # Price generation
        expectPrice = 100
        expectPrice += self.power * 4
        expectPrice += self.precision * 2
        if self.effects != None or self.effectOnUse != None:
            expectPrice += 200

        if expectPrice != price and price != 0:
            self.price = expectPrice

    def allStats(self):
        """Return a list with the mains stats of the weapon"""
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

mainLibre = weapon("Main Libre","aa",RANGE_MELEE,AREA_CIRCLE_1,44,45,0,strength=20,agility=15,endurance=10,resistance=5,repetition=3,emoji = '<:fist:866368882784337941>')
splattershotJR = weapon("Liquidateur JR","af",RANGE_DIST,AREA_CIRCLE_3,47,35,0,agility=20,charisma=10,strength=20,repetition=3,emoji = '<:splattershotJR:866367630465433611>')
novaShotter = weapon("Lanceur Spacial",getAutoId("eo"),RANGE_LONG,AREA_CIRCLE_5,33,40,0,precision=20,strength=20,intelligence=10,repetition=3,emoji='<:novaShotter:1064172067576090715>')

baseWeapon = [mainLibre, splattershotJR,novaShotter]

skillVarInit = {
    "condition":[], "ultimate":False, "group":0, "emoji":None, "effects":None, "cooldown":1,"area" : AREA_MONO,"accuracy" : 100,"effectOnSelf":None,"use":STRENGTH,"damageOnArmor" : 1,"invocation":None,"description":None,"initCooldown" : 1,"shareCooldown" : False,"message":None,"say":"","repetition":1,"knockback":0,"effPowerPurcent":100,"become":None,"replay":False,"maxHpCost":0,"hpCost":0,"tpCac" : False,"jumpBack":0,"useActionStats" : None,"setAoEDamage":False,"url":None,"areaOnSelf":False, "lifeSteal" : 0, "effectAroundCaster" : None,"needEffect":None,"rejectEffect":None,"erosion":0,"percing":0,"execution":False,"selfEffPurcent":100,"effBeforePow":False,"jaugeEff":None,"pull":0,"maxPower":0,"minJaugeValue" : 0, "maxJaugeValue" : 0, "minTargetRequired" : 1, "quickDesc" : "", "depl":None, "armorConvert":0, "nbSummon" : 1, "firstSumIgnoreLimit":False, "garCrit" : False, "tpBehind" : False, "affSkillMsg" : True, "aoeLifeSteal":0, "aoeArmorConvert" : 0,"armorSteal":0
}
skillVarKeyInit = list(skillVarInit.keys())

class skill(defaultObj):
    """The main and only class for the skills"""
    def __init__ (self,name : str, id : str, types : int ,price : int = 0, power:int= 0, range=AREA_CIRCLE_5, **kwargs):
        """rtfm"""
        defaultVars = copy.deepcopy(skillVarInit)
        for key in kwargs:
            defaultVars[key] = kwargs[key]
            if key not in skillVarKeyInit:
                raise ValueError("{0} : Key {1} not matching".format(name,key))

        self.effects: List[Union[None,effect]] = defaultVars["effects"]
        if type(self.effects)!=list:
            self.effects = [self.effects]
        self.name:str = name                                # Name of the skill
        self.repetition:int = defaultVars["repetition"]                    # The number of hits it does
        self.say:Union[str,List[str]] = defaultVars["say"]                                  # Does the attacker say something when the skill is used ?
        self.id:str = id                                    # The id of the skill.  Idealy, unique
        self.type:int = types                               # The type of the skill. See constante.types
        self.replay:bool = defaultVars["replay"]
        self.tpCac:bool = defaultVars["tpCac"]
        self.tpBehind:bool = defaultVars["tpBehind"]
        self.execution:bool = defaultVars["execution"]
        self.jumpBack:int = defaultVars["jumpBack"]
        self.setAoEDamage:bool = defaultVars["setAoEDamage"]
        self.garCrit = defaultVars["garCrit"]
        self.areaOnSelf:bool = defaultVars["areaOnSelf"]
        self.lifeSteal, self.aoeLifeSteal = defaultVars["lifeSteal"], defaultVars["aoeLifeSteal"]
        self.armorConvert, self.aoeArmorConvert = defaultVars["armorConvert"], defaultVars["aoeArmorConvert"]
        self.erosion, self.pull = defaultVars["erosion"], defaultVars["pull"]
        self.effBeforePow, self.jaugeEff, self.minJaugeValue, self.maxJaugeValue = defaultVars["effBeforePow"], defaultVars["jaugeEff"], defaultVars["minJaugeValue"], [defaultVars["maxJaugeValue"],defaultVars["minJaugeValue"]][defaultVars["minJaugeValue"]>= 0 and defaultVars["maxJaugeValue"] == 0]
        self.effectAroundCaster: Union[None,List[int]] = defaultVars["effectAroundCaster"]
        self.depl = defaultVars["depl"]
        self.nbSummon = defaultVars["nbSummon"]
        self.armorSteal:int = defaultVars["armorSteal"]
        if self.depl != None:
            self.depl.skills.emoji = defaultVars["emoji"]
        self.needEffect: Union[None,List[effect]]=defaultVars["needEffect"]
        if self.needEffect != None and type(self.needEffect) != list:
            self.needEffect = [self.needEffect]
        self.rejectEffect= defaultVars["rejectEffect"]
        if self.rejectEffect != None and type(self.rejectEffect) != list:
            self.rejectEffect=[self.rejectEffect]

        if self.effectAroundCaster != None:
            if self.effectAroundCaster[0] not in allTypes:
                raise Exception("EffectAroudCaster[0] not a type")
            elif self.effectAroundCaster[0] not in allArea:
                raise Exception("EffectAroudCaster[1] not a area")

        self.power = power  # Power of the skill. Use for damage and healing skills
        self.maxPower = defaultVars["maxPower"]
        if self.maxPower == 0 and self.minJaugeValue == self.maxJaugeValue and self.minJaugeValue != 0:
            self.maxPower = power

        self.knockback:int = defaultVars["knockback"]
        self.effPowerPurcent:int = defaultVars["effPowerPurcent"]
        self.become:List = defaultVars["become"]
        self.url:str = defaultVars["url"]
        self.selfEffPurcent = defaultVars["selfEffPurcent"]
        self.ultimate = defaultVars["ultimate"]
        self.percing = defaultVars["percing"] + [0,20][self.ultimate and self.type == TYPE_DAMAGE]

        self.price = price                              # Price. 0 if the skill can't be drop or bought
        self.condition = defaultVars["condition"]
        
        self.range = range
        self.group = defaultVars["group"]
        self.cooldown = defaultVars["cooldown"]
        self.affSkillMsg = defaultVars["affSkillMsg"]
        if self.become != None:
            minCd, maxCd,sumPowa,minJaVa,maxJaVa = 99, 0, 0, 100,0
            for skilly in self.become:
                if skilly.cooldown < minCd:
                    minCd = skilly.cooldown
                elif skilly.cooldown > maxCd:
                    maxCd = skilly.cooldown
                if skilly.jaugeEff != None:
                    minJaVa = min(skilly.minJaugeValue,minJaVa)
                    maxJaVa = max(skilly.maxJaugeValue,maxJaVa)
                sumPowa += skilly.iaPow
            self.cooldown = minCd
            if self.power <= 0:
                self.power = int(sumPowa/len(self.become))
            if self.jaugeEff != None:
                self.minJaugeValue = minJaugeValue = minJaVa
                self.maxJaugeValue = maxJaugeValue = maxJaVa
            cmpt = 0
            while cmpt < len(self.become):
                if self.become[cmpt].cooldown != maxCd:
                    self.become[cmpt].iaPow += min(maxCd-self.become[cmpt].cooldown,10) * 5
                cmpt+=1

        self.area = defaultVars["area"]
        self.maxHpCost, self.hpCost = defaultVars["maxHpCost"], defaultVars["hpCost"]
        self.minTargetRequired = defaultVars["minTargetRequired"]
        self.accuracy = defaultVars["accuracy"]
        if self.accuracy == 100 and types == TYPE_DAMAGE:
            self.accuracy = [80,120][self.area==AREA_MONO]

        self.effectOnSelf = defaultVars["effectOnSelf"]
        self.use = defaultVars["use"]
        self.description = defaultVars["description"]
        if self.description != None:
            if self.effects != [None] and type(self.effects[0]) != str:
                self.description = self.description.format(effIcon = self.effects[0].emoji[0][0],effName=self.effects[0].name,power=power,power2=power//2,length=self.effects[0].turnInit,armor=self.effects[0].overhealth)
            elif self.effectOnSelf != None and type(self.effectOnSelf) != str:
                self.description = self.description.format(effIcon = self.effectOnSelf.emoji[0][0],effName=self.effectOnSelf.name,power=power,power2=power//2,length=self.effectOnSelf.turnInit,armor=self.effectOnSelf.overhealth)
            else:
                try:
                    self.description = self.description.format(power=power,power2=power//2)
                except:
                    self.description = "Error with the formatage of the description"
                    print("Error with the formatage of the description of the skill : "+self.name)
        self.quickDesc = defaultVars["quickDesc"]
        self.initCooldown = defaultVars["initCooldown"]
        self.shareCooldown = defaultVars["shareCooldown"]

        if self.use==STRENGTH:
            if types in [TYPE_ARMOR]:
                self.use = INTELLIGENCE
            elif types in [TYPE_HEAL,TYPE_INDIRECT_HEAL]:
                self.use = CHARISMA
            elif power == 0 and self.effects != [None] and type(self.effects[0]) != str:
                self.use = self.effects[0].stat
            elif power == 0 and self.effectOnSelf != None and type(self.effectOnSelf) != str:
                self.use = self.effectOnSelf.stat
            elif self.become !=None:
                dictUse = [[STRENGTH,0],[ENDURANCE,0],[CHARISMA,0],[AGILITY,0],[PRECISION,0],[INTELLIGENCE,0],[MAGIE,0]]
                for skilly in self.become:
                    if type(skilly.use) == int and skilly.use <= MAGIE:
                        dictUse[skilly.use][1] += 1
                dictUse.sort(key=lambda ballerine: ballerine[1],reverse=True)
                self.use = dictUse[0][0]

        self.onArmor = defaultVars["damageOnArmor"]
        self.invocation = defaultVars["invocation"]
        self.useActionStats = defaultVars["useActionStats"]

        if types==TYPE_PASSIVE:
            self.area=AREA_MONO
            self.range=AREA_MONO
            self.initCooldown=99
            if self.effectOnSelf != None:
                if self.effects == [None]:
                    self.effects = [self.effectOnSelf]
                else:
                    self.effects.append(self.effectOnSelf)
                self.effectOnSelf = None

        if self.area in [AREA_ALL_ALLIES,AREA_ALL_ENEMIES,AREA_ALL_ENTITES]:
            self.range = AREA_MONO

        self.emoji = defaultVars["emoji"]
        if self.emoji == None:
            if self.type in [TYPE_DAMAGE]:
                if self.area == AREA_MONO:
                    if self.use in [STRENGTH,PRECISION,AGILITY]:
                        if self.cooldown >= 7 or self.ultimate:
                            self.emoji='<:dUPM:943279319994728539>'
                        else:
                            self.emoji='<:dM:943275508492292138>'
                    else:
                        if self.cooldown >= 7 or self.ultimate:
                            self.emoji='<:dUMM:943279280002060309>'
                        else:
                            self.emoji='<:dD:885899060488339456>'
                else:
                    if self.use in [STRENGTH,PRECISION,AGILITY]:
                        if self.cooldown >= 7 or self.ultimate:
                            self.emoji='<:dUZ:943279239573143612>'
                        else:
                            self.emoji='<:dZ:943275494802079804>'
                    else:
                        if self.cooldown >= 7 or self.ultimate:
                            self.emoji='<:dUMZ:943279254991409232>'
                        else:
                            self.emoji="<:dZ:943266058024943656>"
            elif self.type in [TYPE_INDIRECT_DAMAGE]:
                self.emoji = '<:defIndi:943266043558768640>'
            elif self.type in [TYPE_HEAL,TYPE_INDIRECT_HEAL]:
                if self.area == AREA_MONO:
                    if self.cooldown >= 7 or self.ultimate:
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
            elif self.type in [TYPE_PASSIVE]:
                self.emoji = self.effects[0].emoji[0][0]
            else:
                self.emoji=''

        if self.use == STRENGTH and self.type in [TYPE_INDIRECT_DAMAGE,TYPE_INDIRECT_HEAL,TYPE_BOOST,TYPE_MALUS] and (self.effects[0] != None and type(self.effects[0]) != str) :
            self.use = self.effects[0].stat

        if self.jaugeEff != None and self.minJaugeValue == self.maxJaugeValue == 0:
            self.minJaugeValue = self.maxJaugeValue = 1
            self.maxPower = self.power

        iaPow = 0
        if self.type in [TYPE_DAMAGE,TYPE_HEAL,TYPE_RESURECTION]:
            cmpt, skillToSee, iaPow = 1, self, int(min([self.power,(self.maxPower-self.power)+self.power][self.maxPower > 0 and self.maxPower != self.power],350)*(min(self.accuracy,150)/100))
            if self.garCrit or self.setAoEDamage:
                iaPow = iaPow *1.3
            skillToSee = self
            while (skillToSee.effectOnSelf != None and skillToSee.effectOnSelf.replica != None):
                skillToSee = skillToSee.effectOnSelf.replica
                try:
                    iaPow += skillToSee.power
                    cmpt += 1
                except:
                    break
            iaPow = iaPow//cmpt 
        elif self.type in [TYPE_SUMMON, TYPE_DEPL]:
            try:
                iaPow += self.invocation.iaPow
            except:
                iaPow += 100
        effToSee:List[effect] = self.effects[:]*self.repetition
        if self.effectOnSelf != None:
            effToSee.append(self.effectOnSelf)
        if self.effectAroundCaster != None and type(self.effectAroundCaster[2]) == effect:
            effToSee.append(self.effectAroundCaster[2])
        elif self.effectAroundCaster != None and type(self.effectAroundCaster[2]) == int:
            iaPow += min(self.effectAroundCaster[2] * 0.7,150)

        for eff in effToSee:
            if type(eff) == effect:
                if eff.id in [vulne.id,defenseUp.id,dmgDown.id,dmgUp.id,healDoneBonus.id,absEff.id,incurable.id,armorGetMalus.id]:
                    iaPow += eff.power * [2.5,5][eff.stat not in [None,FIXE,PURCENTAGE]]
                else:
                    iaPow += eff.iaPow

        iaPow += (min(self.cooldown,10) * 5) + (self.ultimate * 15)
        if self.replay:
            iaPow += 100
        for movingValue in [self.knockback, self.jumpBack, self.pull]:
            iaPow += 10*movingValue
        if self.tpCac or self.tpBehind:
            iaPow += 20

        if self.knockback >= 3:
            iaPow += 20
        if self.depl != None:
            iaPow += self.depl.skills.iaPow * self.depl.lifeTime
        self.iaPow = int(iaPow)

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

firstheal = skill("Premiers Secours","zj",TYPE_HEAL,price=10,power=35,emoji="<:bandage:873542442484396073>",description="Une compétence de soin peu puissance mais utilisable sans temps de rechargement",use=CHARISMA)
armorPack = skill("Armure Portative",getAutoId("sfv",True),TYPE_ARMOR,price=10,effects=armorPackEff,emoji='<:armorPack:1063490980759748789>',description="Une compétence d'armure peu puissance mais utilisable sans temps de rechargement")

baseSkills = [firstheal,armorPack]

class stuff(defaultObj):
    """The main and only class for all the gears"""
    def __init__(self,name,id,types,price,strength=0,endurance=0,charisma=0,agility=0,precision=0,intelligence=0,magie=0,resistance=0,percing=0,critical=0,emoji = None,effects=None, orientation = [],position=0,affinity = None,negativeShield=0,negativeHeal=0,negativeDirect=0,negativeIndirect=0,negativeBoost=0):
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
            if effects != None:
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

        self.effects = effects
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

        if effects != None:
            summation += 15

        while 20 + cmpt * 10 < summation:
            cmpt += 1
        self.minLvl = cmpt * 5

    def allStats(self):
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

    def havConds(self,user):
        return user.level >= self.minLvl

emojiMalus = [['<:ink1debuff:866828217939263548>','<:ink2debuff:866828296833466408>' ],['<:oct1debuff:866828253695705108>','<:oct2debuff:866828340470874142>'],['<:octariandebuff:866828390853247006>','<:octariandebuff:866828390853247006>']]

class other(defaultObj):
    """The class for all the "specials objets" categorie"""
    def __init__(self,name,id,price=1000,emoji=emLoading,description="Léna est féniant"):
        self.name = name
        self.id = id
        self.price = price
        self.emoji = emoji
        self.description = description

bbandeau = stuff("Bandeau du débutant","ha",0,0,resistance=5,endurance=5,strength=5,intelligence=5,emoji="<:bhead:867156694629744691>")
bshirt = stuff("Tee-shirt du débutant","hb",1,0,resistance=5,strength=5,agility=5,precision=5,emoji="<:bshirt:867156711251771402>")
bshoes = stuff("Chaussures du débutant","hc",2,0,agility=5,endurance=5,charisma=10,emoji="<:bshoes:867156725945073694>")
tunRed = stuff("Tunique Rouge",getAutoId("hsi"),1,0,10,5,resistance=5,emoji='<:tunRed:1063480503015055480>',orientation="Dégâts physiques")
tunViolet = stuff("Tunique Violette",getAutoId(tunRed.id),1,0,magie=10,endurance=5,resistance=5,emoji='<:tunPurple:1063480574989324332>',orientation="Dégâts magiques")
tunPink = stuff("Tunique Rose",getAutoId(tunViolet.id),1,0,charisma=10,endurance=5,resistance=5,emoji='<:tunPink:1063480528273154079>',orientation="Soins / Boosts")
tunLBLue = stuff("Tunique Bleu Claire",getAutoId(tunPink.id),1,0,precision=10,endurance=5,resistance=5,emoji='<:tunLightBlue:1063480548393222207>',orientation="Précision")
tunGreen = stuff("Tunique Verte",getAutoId(tunLBLue.id),1,0,agility=10,endurance=5,resistance=5,emoji='<:tunGreen:1063480629880164414>',orientation="Agilité")
tunBleu = stuff("Tunique Bleu",getAutoId(tunGreen.id),1,0,intelligence=10,endurance=5,resistance=5,emoji='<:tunBlue:1063480603615428668>',orientation="Intelligence")

baseStuffs = [
    bbandeau,
    bshirt,tunRed,tunPink,tunLBLue,tunGreen,tunBleu,tunViolet,
    bshoes,
]

class defaultChar:
    def getSkillsDescription(self) -> List[interactions.Embed]:
        toReturn = []
        desc = ""
        if self.elemAffinity:
            desc += "{0} __{1}__ :\n{2}\n".format(elemResistanceEffects[self.element].emoji[0][0],elemResistanceEffects[self.element].name,elemResistanceEffects[self.element].description)
        for cmpt in range(len(upLifeStealNames)):
            if self.name == upLifeStealNames[cmpt]:
                desc += "{0} __{1}__ :\n{2}\n".format(upLifeStealEff[cmpt].emoji[0][0],upLifeStealEff[cmpt].name,upLifeStealEff[cmpt].description)

        for skilly in self.skills:
            if type(skilly) == skill:
                if skilly.become == None:
                    if skilly.description != None:
                        desc += "\n{0} __{1}__ :\n{2}\n".format(skilly.emoji,skilly.name,skilly.description)
                    else:
                        desc += "\n{0} __{1}__ :\n{2}\n".format(skilly.emoji,skilly.name,skilly.getSummary())
                else:
                    desc += "\n{0} __{1}__ :\n*Les compétences suivantes ont un temps de rechargement partégé*".format(skilly.emoji,skilly.name)
                    for ski in skilly.become:
                        if ski.description != None:
                            desc += "\n> {0} __{1}__ :\n> {2}\n".format(ski.emoji, ski.name, ski.description.replace("\n","\n> "))
                        else:
                            desc += "\n> {0} __{1}__ :\n> {2}\n".format(ski.emoji, ski.name, ski.getSummary())
        desc = reduceEmojiNames(desc)
        nbEmbed = 0
        while len(desc) > 0:
            if len(desc) > 4000:
                tempDesc = desc.splitlines()
                tempDesc = desc.replace(tempDesc[-1],"")
                toReturn.append(interactions.Embed(title=["__{0}__".format(self.name),""][nbEmbed>0],color=self.color, description=tempDesc))
                desc = desc.replace(tempDesc,"")
                nbEmbed += 1
            else:
                toReturn.append(interactions.Embed(title=["__{0}__".format(self.name),""][nbEmbed>0],color=self.color, description=desc))
                desc = ""
                nbEmbed += 1
        return toReturn

    def __str__(self) -> str:
        return self.name

    def allStats(self):
        """Return a ``list`` with the mains stats of the ennemi\n
        Those stats are the Lvl 50 stats"""
        return [self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie]

class char(defaultChar):
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
        self.points = 5
        self.canMove = True
        self.majorPointsCount = 0
        self.elemAffinity = False
        self.weapon = splattershotJR
        self.weaponInventory = baseWeapon
        self.skills = ["0","0","0","0","0","0","0"]
        self.skillInventory = baseSkills
        self.stuff = [bbandeau,bshirt,bshoes]
        self.stuffInventory = baseStuffs
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
        self.limitBreaks = [0,0,0,0,0,0,0]
        self.charSettings = createCharSettingsDict()
        self.npcTeam = None
        self.trait, self.counterEmoji, self.slowMove = [], None, False

    def have(self,obj):
        """Verify if the character have the object Obj"""
        for weap in self.weaponInventory:
            if weap.id == obj.id:
                return True
        for skilly in self.skillInventory:
            if skilly.id == obj.id:
                return True
        for stuffy in self.stuffInventory:
            if stuffy.id == obj.id:
                return True
        try:
            for othy in self.otherInventory:
                if othy.id == obj.id:
                    return True
        except:
            print(self.otherInventory)
        return False

    def isNpc(self,name : str):
        return False

class invoc(defaultChar):
    """The main class for summons. Similar the "char" class, but with only the fight's necessery attributs"""
    def __init__(self,name,strength,endurance,charisma,agility,precision,intelligence,magie,resistance,percing,critical,aspiration,icon,weapon,skills=[],gender=GENDER_OTHER,description="Pas de description",element=ELEMENT_NEUTRAL,canMove=True,team:int=None,lifeTime=3,trait=[],slowMove=False):
        self.name = name
        self.level = 0
        self.team = 0
        self.gender = gender
        self.color = 0
        self.species = 1
        self.stars = 0
        self.canMove = canMove
        self.limitBreaks, self.points = [0,0,0,0,0,0,0], 0

        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.resistance,self.percing,self.critical,self.magie = strength,endurance,charisma,agility,precision,intelligence,resistance,percing,critical,magie
        self.aspiration = aspiration
        self.weapon = weapon
        self.majorPoints = [0,0,0,0,0,0,0]+[0,0,0]+[0,0,0,0,0]
        self.npcTeam = team

        self.description = description
        self.trait, self.counterEmoji = trait, None

        while len(skills)<7:
            skills.append("0")

        self.skills = skills
        self.icon = icon
        self.customColor = False
        if type(element) != list:
            element = [element,ELEMENT_NEUTRAL]
        self.element = element[0]
        if self.element != ELEMENT_NEUTRAL:
            for cmpt in range(len(self.skills)):
                if type(self.skills[cmpt]) == skill:
                    self.skills[cmpt].condition = [EXCLUSIVE,ELEMENT,self.element]

        self.secElement = element[1]
        self.says = says()
        self.charSettings = createCharSettingsDict()
        self.lifeTime = lifeTime
        sumIaPow = self.weapon.power * (self.weapon.accuracy/100)
        for skillVerif in self.skills:
            if type(skillVerif) == skill:
                sumIaPow += skillVerif.iaPow
        self.iaPow = sumIaPow
        self.slowMove = slowMove

    def isNpc(self,name : str):
        return False

textBaliseAtReplace = ["Ã©","Ã","à§"]
textBaliseToReplace = ["é","à","Ç"]

if len(textBaliseAtReplace) != len(textBaliseToReplace):
    raise Exception("len(textBaliseAtReplace) != len(textBaliseToReplace)")

octoEmpty1 = stuff("placeolder","ht",0,0)
octoEmpty2 = stuff("placeolder","hu",0,0)
octoEmpty3 = stuff("placeolder","hv",0,0)

class octarien(defaultChar):
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
            standAlone:bool = False,
            say:says=says(),
            baseLvl:int = 1,
            rez:bool=True,
            element:List[int] = [ELEMENT_NEUTRAL,ELEMENT_NEUTRAL],
            number:int = 1,
            canMove=True,
            splashArt = None,
            splashIcon = None, elemAffinity = False, team:int=None, trait=[], slowMove = False
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
            .standAlone : Does the ennemy is a "All v One" boss ?
            .say : A ``says`` object, for some specials interractions
            .baseLvl : The minimum amount of level required for battleling againts the ennemy
            .rez : Does the ennemy can be raise ?
            .element : The element of the ennemy
            .number : The number of times the ennemy appairse in the ennemy list
        """
        self.name = name
        self.owner = 0
        self.elemAffinity = elemAffinity
        if team in [NPC_KITSUNE,NPC_GOLEM]:
            self.elemAffinity = True
        else:
            self.elemAffinity = elemAffinity
        self.species = 3
        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie = maxStrength,maxEndurance,maxCharisma,maxAgility,maxPrecision,maxIntelligence,maxMagie
        self.resistance,self.percing,self.critical, self.points = resistance,percing,critical, 0
        self.aspiration = aspiration
        self.weapon = weapon
        self.number = number
        self.skills = skill
        self.stars = 0
        self.team = -2
        self.trait = trait
        self.canMove = canMove
        self.limitBreaks = [0,0,0,0,0,0,0]
        while len(self.skills) < 7:
            self.skills+=["0"]

        self.skillsInventory = []
        self.majorPoints = [0,0,0,0,0,0,0]+[0,0,0]+[0,0,0,0,0]
        self.color = red
        self.level = 1
        self.stuff = [octoEmpty1,octoEmpty2,octoEmpty3]
        self.npcTeam = team
        self.exp = exp
        self.icon = icon
        self.gender = gender
        self.description = description
        self.counterEmoji = None

        if type(element) != list:
            element = [element,ELEMENT_NEUTRAL]

        self.element = element[0]
        self.secElement = element[1]
        self.deadIcon = deadIcon
        self.standAlone = standAlone
        self.says = say
        self.baseLvl = baseLvl
        self.rez = rez
        self.bonusPoints = [0,0,0,0,0,0,0]
        self.charSettings = createCharSettingsDict()
        cmpt = 0
        for skilly in skill:
            if type(skilly) == skill:
                cmpt += 1

        self.baseSkillNb = cmpt
        self.splashArt, self.splashIcon = splashArt, splashIcon
        self.slowMove = slowMove

    def changeLevel(self,level=1):
        """Change the level of the ennmy and adjust his stats and skills in consequence\n
        It's very recommanded to do than on a copy of the ennemy"""
        self.level = level
        stats, cmpt = copy.deepcopy(self.allStats()),0
        for a in lvlToUnlockSkill:
            if self.level >= a:
                cmpt += 1

        skillCountMul = 0.65 + (0.35*(cmpt/7))

        if self.name == "Marinier Sabreur" and random.randint(0,99) < 50:
            self.icon, self.deadIcon = "<:marSab2:1059519678944382976>", "<:spTako:866465864399323167>"
        elif self.name == "Marinier Tireur" and random.randint(0,99) < 50:
            self.icon, self.deadIcon = "<:marGun2:1059519645201223700>", "<:spTako:866465864399323167>"


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
        self.stuff[0].minLvl = self.stuff[1].minLvl = self.stuff[2].minLvl = level

    def isNpc(self,name : str):
        """Return if the given name is egal to the ennemy name"""
        return self.name == name

class tempAltBuilds():
    def __init__(self,proba:int=30,aspiration:int=None,weap:weapon=None,stuffs:List[stuff]=None,skills:List[skill]=None,elements:Union[int,List[int]]=None,bonusPoints:List[int]=None,icon=None,splashIcon=None):
        self.proba = proba
        self.aspiration = aspiration
        self.weapon = weap
        self.stuff = stuffs
        self.skills =skills
        if elements != None:
            if type(elements) == list:
                self.elements = elements
            else:
                self.elements = [elements,ELEMENT_NEUTRAL]
        else:
            self.elements = None
        self.bonusPoints = bonusPoints
        self.icon, self.splashIcon = icon, splashIcon

class tmpAllie(defaultChar):
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
        changeDict:Union[None,List[tempAltBuilds]] = None,
        unlock:Union[bool,None,str]=False,
        birthday:Union[None,tuple]=None,
        limitBreaks:list=None,
        splashArt=None,
        splashIcon = None,
        charSettings = None, elemAffinity=False,team:int=None,trait=[]
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
        self.majorPoints, self.points = [0,0,0,0,0,0,0]+[0,0,0]+[0,0,0,0,0], 0
        for a in range(len(skill)):
            self.skills[a] = skill[a]
        self.skillsInventory = []
        self.color = color
        self.level = 1
        self.stuff = stuff
        if team in [NPC_KITSUNE,NPC_GOLEM]:
            self.elemAffinity = True
        else:
            self.elemAffinity = elemAffinity
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
        self.npcTeam = team
        if limitBreaks == None:
            self.limitBreaks = [0,0,0,0,0,0,0]
        else:
            self.limitBreaks = [0,0,0,0,0,0,0]
            for cmpt in limitBreaks[0]:
                self.limitBreaks[cmpt] = limitBreaks[1]

        self.splashArt, self.splashIcon = splashArt, splashIcon
        self.trait = trait
        self.counterEmoji = None
        self.slowMove = False
        
        if charSettings == None:
            self.charSettings = createCharSettingsDict()
        else:
            if type(charSettings) != dict:
                print("Error with {0} charSettings : {1}".format(self.name,charSettings))
            self.charSettings = charSettings

    def changeLevel(self,level=1,changeDict=True,stars=0,changeStuff=True):
        for procurName, procurStuff in procurTempStuff.items():
            if self.name == procurName:
                level += procurStuff[0]
                break

        self.level = level
        self.stars = stars
        stats = self.allStats()

        if self.changeDict != None and changeDict:
            roll = random.randint(0,99)
            tprob = 0
            for altBuild in self.changeDict:
                tprob += altBuild.proba
            if roll < tprob:
                for altBuild in self.changeDict:
                    if roll < altBuild.proba:
                        if altBuild.weapon != None:
                            self.weapon = altBuild.weapon
                        if altBuild.aspiration != None:
                            self.aspiration = altBuild.aspiration
                        if altBuild.stuff != None:
                            self.stuff = altBuild.stuff
                        if altBuild.skills != None:
                            self.skills = altBuild.skills
                            while len(self.skills) < 7:
                                self.skills.append(None)
                        if altBuild.elements != None:
                            self.element = altBuild.elements[0]
                            self.secElement = altBuild.elements[1]
                        if altBuild.bonusPoints != None:
                            self.bonusPoints = altBuild.bonusPoints
                        if altBuild.icon != None:
                            self.icon = altBuild.icon
                        if altBuild.splashIcon != None:
                            self.splashIcon = altBuild.splashIcon
                        break
                    else:
                        roll = roll - altBuild.proba
        for a in range(0,len(stats)):
            stats[a] = round(aspiStats[self.aspiration][a]*0.1+aspiStats[self.aspiration][a]*0.9*self.level/50)

        bPoints = level
        for a in self.bonusPoints:
            if a != None:
                distribute = min(MAXBONUSPERSTAT,bPoints)
                bPoints -= distribute
                stats[a] += distribute

        for cmpt in range(len(lvlToUnlockSkill)):
            if self.level < lvlToUnlockSkill[cmpt]:
                self.skills[cmpt] = "0"

        if self.level < 10:
            self.element = ELEMENT_NEUTRAL
        elif self.level < 20 and self.element in [ELEMENT_SPACE,ELEMENT_DARKNESS,ELEMENT_LIGHT,ELEMENT_LIGHT]:
            self.element = random.randint(0,3)

        if self.level < 30:
            self.secElement = ELEMENT_NEUTRAL

        if stars > 0:
            for cmpt in range(min(stars,len(recommandedMajorPoints[self.aspiration]))):
                self.majorPoints[recommandedMajorPoints[self.aspiration][cmpt]] = [MAJORBONUS,10][recommandedMajorPoints[self.aspiration][cmpt] in [RESISTANCE,PERCING,CRITICAL]] * [1,-1][recommandedMajorPoints[self.aspiration][cmpt] >= ACT_HEAL_FULL]
        self.strength,self.endurance,self.charisma,self.agility,self.precision,self.intelligence,self.magie = stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],stats[6]

    def isNpc(self,name : str):
        return self.name == name

def getAllieFromBuild(ally:tmpAllie, build:tempAltBuilds):
    """Generate a new Ally from one of their alt builds"""
    ally = copy.deepcopy(ally)
    if build.aspiration != None:
        ally.aspiration = build.aspiration
    if build.elements != None:
        ally.elements = build.elements
    if build.skills != None:
        ally.skills = build.skills
    if build.stuff != None:
        ally.stuff = build.stuff
    if build.weapon != None:
        ally.weapon = build.weapon
    if build.bonusPoints != None:
        ally.bonusPoints = build.bonusPoints
    if build.splashIcon != None:
        ally.splashIcon = build.splashIcon
    if build.icon != None:
        ally.icon = build.icon
    if build.splashIcon != None:
        ally.splashIcon = build.splashIcon
    return ally

class duty():
    def __init__(self,serie:str,number:int,eventDict:dict={}):
        self.serie, self.numer, self.txtPath = serie, number, "./data/advScriptTxt/{0}/{1}.txt".format(serie.replace(" ","_"),number)
        self.eventDict, self.enemies, self.allies, self.embedTxtList = eventDict, [], [], []
        self.trait = []

    def load(self):
        """Load the duty with their text box"""
        loadedFile = open(self.txtPath)
        tempTxt, loadedRowTxt = "", loadedFile.readlines() + "====="
        for line in loadedRowTxt:
            if "=====" in line:
                self.embedTxtList.append(tempTxt)
                tempTxt = ""
            else:
                tempTxt += line

        while len(self.eventIndex) < len(self.embedTxtList):
            self.eventIndex.append(None)

class depl(defaultChar):
    def __init__(self,name:str,skills:skill,icon:List[str],cellIcon:List[str]=None,description:str="",lifeTime=3):
        if cellIcon == None:
            if skills.type in friendlyTypes:
                cellIcon = ["<:avalancheB:1115997614589104219>","<:avalanceR:1115997637821337761>"]
            elif skills.type in hostilesTypes:
                cellIcon = ["<:fecaloB:1115997532909228052>","<:fecaloR:1115997559308165211>"]
            else:
                cellIcon = ["<:Targeted1:873118129214083102>","<:Targeted2:873118129130192947>"]
        if type(icon) == str:
            icon = [icon,icon]
        self.name = name
        self.skills = skills
        self.skills.accuracy = 350
        self.icon = icon
        self.cellIcon = cellIcon
        self.description = description + "\n\nCe déployable utlise la statistique de {1} __{0}__ et a une durée de vie de __{2}__ tours".format(allStatsNames[skills.use],statsEmojis[skills.use],lifeTime)
        self.lifeTime = lifeTime
        self.weapon = weapon("None weap","noneWeap",RANGE_DIST,AREA_CIRCLE_3,0,0)
        self.says = says()
        self.gender = GENDER_OTHER
        self.npcTeam = None
        sumIaPow = 0
        if type(self.skills) == skill:
            sumIaPow += self.skills.iaPow
        self.iaPow = sumIaPow
        self.trait, self.counterEmoji = [], None

    def isNpc(self,name):
        return False

stolenArmorEff = effect("Vol d'Armure","armorStolenEff",overhealth=1,turnInit=3,stackable=True,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,lightShield=True,emoji=sameSpeciesEmoji('<:lightArmorB:1177978814329004162>','<:lightArmorR:1177978836940496957>'))
lightHealingPassif = effect("Soins lumières","lightHealingPassif", stat=MISSING_HP,power=LIGHTHEALBUFF,turnInit=-1,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,unclearable=True,emoji=elemEmojis[ELEMENT_LIGHT])
spaceShield = effect("Armure dimentionnelle","spaceShield", stat=MISSING_HP,stackable=True,turnInit=1,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,overhealth=SPACESHIELD,emoji=stolenArmorEff.emoji,lightShield=True,silentRemove=True)
spaceShieldPassif = effect("Cycle Dimentionnel","spaceShield2",turnInit=-1,unclearable=True,callOnTrigger=spaceShield,trigger=TRIGGER_START_OF_TURN,emoji=elemEmojis[ELEMENT_SPACE])

ELEMENT_FIRE, ELEMENT_WATER, ELEMENT_AIR, ELEMENT_EARTH
elemResistanceEffects, elemStrength, elemWeakness = [None], [None,ELEMENT_AIR,ELEMENT_FIRE,ELEMENT_EARTH,ELEMENT_WATER], [None,ELEMENT_WATER,ELEMENT_EARTH,ELEMENT_FIRE,ELEMENT_AIR]

subWaterEff = effect("Sub Water","subWaterEff", stat=FIXE,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_HEAL,emoji=elemEmojis[ELEMENT_WATER],incHealJauge=False,turnInit=2,silentRemove=True)

DEEP_WOUND_RATIO = 50
deepWound = effect("Blessure Profonde","deepWound",turnInit=20,stackable=True,emoji='<:deepWound:1188192336652546079>',type=TYPE_MALUS,description="Cet effet absorbe les soins reçus par l'adversaire. La puissance de cet effet suit les mêmes règles que les dégâts directs. Si de l'armure est présente sur la cible lors de la pose de l'effet, des dégâts sont infligés à l'armure à la place. Si cet effet est présent lorsque la cible termine son tour, elle reçoit des dégâts indirects équivalent à **{0}%** de la valeur de l'effet".format(DEEP_WOUND_RATIO))

ELEMENT_RESIST = 20
for cmpt in range(1,ELEMENT_EARTH+1):
    elemResistanceEffects.append(
        effect("Affinité : {0}".format(elemNames[cmpt]), "elemAffinity", turnInit=-1, unclearable=True, emoji=["","<:fireResist:1064110332869611561>","<:waterResist:1064110363584503848>","<:airResist:1064110303836639273>","<:earthResist:1064110388288950302>"][cmpt], description="Réduit de **{0}%** les dégâts subis venant de compétences {1} __{2}__ mais augmente d'autant les dégâts subis de compétences {3} __{4}__".format(ELEMENT_RESIST, elemEmojis[elemStrength[cmpt]], elemNames[elemStrength[cmpt]], elemEmojis[elemWeakness[cmpt]], elemNames[elemWeakness[cmpt]]))
        )

TRAIT_ARACHNOPHOBE, TRAIT_ARACHNOPHILE, TRAIT_HIGHLIGHTED, TRAIT_LYTHOPHAGE, TRAIT_ROCKED = 0,1,2,3,4

clemIa = createCharSettingsDict(
    weaponUse=CHARSET_WEAPON_USE_LOW,
    dmgSkillUse=CHARSET_DMGSKILL_HIGH,
    healSkillUse=CHARSET_HEALSKILL_HIGH,
    offTarget=CHARSET_OFFTARGET_HEAL
)
lenaIa = createCharSettingsDict(
    weaponUse=CHARSET_WEAPON_USE_LOW,
    dmgSkillUse=CHARSET_DMGSKILL_HIGH,
    summonSkillUse=CHARSET_SUMMONSKILL_HIGH
)
hinaIa = createCharSettingsDict(
    weaponUse=CHARSET_WEAPON_USE_LOW,
    dmgSkillUse=CHARSET_DMGSKILL_HIGH
)