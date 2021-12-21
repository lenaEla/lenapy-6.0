from classes import *
from constantes import *

splattershot = weapon("Liquidateur","ab",RANGE_DIST,AREA_CIRCLE_3,40,50,280,agility=10,precision=10,strength=10,repetition=3,emoji = emoji.splatShot,affinity=ELEMENT_NEUTRAL)
roller = weapon("Rouleau","ac",RANGE_MELEE,AREA_CIRCLE_1,70,70,340,strength=10,endurance=10,resistance=10,emoji = emoji.roller,needRotate=False,affinity=ELEMENT_AIR,area=AREA_CONE_2,damageOnArmor=0.8)
splatcharger = weapon("Fusil de précision anti-matériel","ad",RANGE_LONG,AREA_CIRCLE_5,83,60,482,strength=10,precision=20,emoji = '<:sniperRifle:903115499204923402>',affinity=ELEMENT_WATER)
miniBrush = weapon("Epinceau","ae",RANGE_MELEE,AREA_CIRCLE_1,31,45,224,agility=10,charisma=10,endurance=10,repetition=5,emoji='<:inkBrush:866463573580578816>',needRotate=False)
inkbrella = weapon("Para-Encre","ag",RANGE_MELEE,AREA_CIRCLE_1,41,45,price=472,endurance=5,resistance=10,repetition=3,effect='lp',emoji='<:splatbrella:866464991255199834>',needRotate=False)
blaster = weapon("Eclatblasteur","ah",RANGE_DIST,AREA_CIRCLE_3,84,50,150,agility=10,strength=10,percing=10,area=AREA_CIRCLE_1,emoji='<:blaster:866463931304378418>')
jetSkelcher = weapon("Nettoyeur XL","ai",RANGE_LONG,AREA_CIRCLE_5,31,40,200,strength=10,precision=10,percing=10,repetition=4,emoji='<:squelsher:866464376319115281>',affinity=ELEMENT_WATER)
dualies = weapon("Double Encreur","aj",RANGE_DIST,AREA_CIRCLE_3,42,35,150,strength=10,agility=20,repetition=4,emoji='<:splatDualies:866465264434806815>',needRotate=False,affinity=ELEMENT_AIR)
kcharger = weapon("Concentraceur alt.","ak",RANGE_MELEE,AREA_CIRCLE_1,38,60,200,strength=15,agility=15,repetition=3,emoji='<:kcharger:870870886939508737>',message="{0} frappe {1} avec son arme :",use=STRENGTH)
HunterRiffle = weapon("Fusil de chasseur","al",RANGE_DIST,AREA_CIRCLE_4,67,65,250,precision=15,effect="ls",emoji="<:hunterRifle:872034208095297597>",affinity=ELEMENT_NEUTRAL)
firework = weapon("Arbalette avec feu d'artifice","am",RANGE_LONG,AREA_CIRCLE_4,76,50,150,strength=10,precision=15,percing=5,emoji='<:crossbow:871746122899664976>',area=AREA_CONE_2)
plume = weapon("Plumes tranchantes","ao",RANGE_DIST,AREA_CIRCLE_4,60,50,250,precision=10,percing=5,emoji='<:plume:871893045296128030>',area=AREA_CONE_2,needRotate=False,affinity=ELEMENT_AIR,effectOnUse=incur[2])
hourglass1Weap = weapon("Sablier intemporel","ap",RANGE_DIST,AREA_CIRCLE_3,50,100,250,charisma=15,target=ALLIES,affinity=ELEMENT_TIME,type=TYPE_HEAL,emoji='<:hourglass1:872181735062908978>',use=CHARISMA)
clashBlaster = weapon("Rafa-Blasteur","aq",RANGE_MELEE,AREA_CIRCLE_2,28,40,250,endurance=10,agility=10,resistance=10,emoji='<:clashBlaster:877666681869176853>',area=AREA_CIRCLE_1,repetition=4)
dualies = weapon("Double Encreur","ar",RANGE_DIST,AREA_CIRCLE_4,34,40,150,agility=15,precision=15,repetition=4,emoji='<:splatDualies:866465264434806815>')
splatling = weapon("Badigeonneur","as",RANGE_LONG,AREA_CIRCLE_5,33,30,300,precision=10,strength=10,intelligence=10,repetition=5,emoji='<:splatling:877666764736061490>')
flexi = weapon("Flexi-Rouleau","at",RANGE_DIST,AREA_CIRCLE_3,85,70,300,strength=15,precision=10,critical=5,emoji='<:flexaRoller:877666714760925275>',needRotate=False)
squiffer = weapon("Décap' Express","au",RANGE_DIST,AREA_CIRCLE_4,78,70,300,strength=10,agility=15,precision=5,emoji='<:skiffer:877666730225328138>')
dualJetSkelcher = weapon("Nettoyeur Duo","av",RANGE_LONG,AREA_CIRCLE_5,25,50,200,strength=10,magie=10,precision=10,repetition=4,emoji='<:DualSkelcher:877666662801883237>',damageOnArmor=1.33)
butterfly = weapon("Papillon Blanc","aw",RANGE_LONG,AREA_CIRCLE_5,50,80,150,charisma=20,use=CHARISMA,intelligence=10,emoji='<:butterflyB:883627125561786428>',target=ALLIES,type=TYPE_HEAL,needRotate=False,message="{0} demande à son papillon de soigner {1} :")
mic = weapon("Micro mignon","ax",RANGE_LONG,AREA_CIRCLE_3,64,75,300,charisma=30,emoji='<:pinkMic:917838961236377690>',needRotate=False,use=CHARISMA,message="{0} pousse la chansonnette !")
spellBook = weapon("Grimoire de feu","ay",RANGE_DIST,AREA_CIRCLE_4,40,75,200,magie=20,percing=10,emoji='<:spellBook:878723144326725744>',needRotate=False,use=MAGIE,area=AREA_CIRCLE_1,affinity=ELEMENT_FIRE,message="{0} lance une boule de feu sur {1}")
legendarySword=weapon("Épée et Bouclier de Légende","az",RANGE_MELEE,AREA_CIRCLE_1,82,85,300,strength=10,endurance=10,resistance=10,emoji='<:masterSword:880008948445478962>',affinity=ELEMENT_LIGHT)
depha = weapon("Lame Dimensionnelle","ba",RANGE_MELEE,AREA_CIRCLE_1,77,90,300,strength=20,resistance=10,emoji='<:ailSword:922696057350127697>')
butterflyR = weapon("Papillon Rose","bb",RANGE_LONG,AREA_CIRCLE_5,50,80,150,charisma=20,intelligence=10,emoji='<:butterflyR:883627168406577172>',use=CHARISMA,needRotate=False,message="{0} demande à son papillon d'attaquer {1} :")
butterflyP = weapon("Papillon Violet","bc",RANGE_LONG,AREA_CIRCLE_5,32,100,250,magie=15,effectOnUse="me",needRotate=False,emoji='<:butterflyV:883627142615805962>',type=TYPE_DAMAGE,message="{0} demande à son papillon d'empoisonner {1} :",use=MAGIE)
dtsword = weapon("Épée de Détermination","bd",RANGE_MELEE,AREA_CIRCLE_1,65,85,500,strength=10,resistance=5,emoji='<:dtSword:884802145239588884>',affinity=ELEMENT_NEUTRAL,effectOnUse=incur[2])
magicSword = weapon("Épée de MagicalGirl","be",RANGE_MELEE,AREA_CIRCLE_1,80,70,200,endurance=10,charisma=10,resistance=10,emoji="<:magicSword:885241611682975744>",use=CHARISMA)
lunarBonk = weapon("Bâton Lunaire","bf",RANGE_MELEE,AREA_CIRCLE_1,65,85,250,endurance=10,intelligence=10,resistance=10,emoji="<:lunarBonk:887347614448746516>",use=MAGIE,affinity=ELEMENT_LIGHT)
rapiere = weapon("Rapière en argent","bg",RANGE_DIST,AREA_CIRCLE_3,63,60,0,magie=5,strength=5,percing=5,use=MAGIE,emoji='<:clemWeap:915358467773063208>',effectOnUse="mx")
fauc = weapon("Faux Tourmentée","bh",RANGE_MELEE,AREA_CIRCLE_2,69,75,0,strength=10,percing=5,emoji='<a:akifauxgif:887335929650507776>',affinity=ELEMENT_DARKNESS,effectOnUse=incur[2])
serringue = weapon("Serringue","bi",RANGE_DIST,AREA_CIRCLE_3,50,100,350,charisma=30,emoji='<:seringue:887402558665142343>',target=ALLIES,type=TYPE_HEAL,use=CHARISMA,affinity=ELEMENT_LIGHT,message="{0} fait une perfusion à {1}")
bigshot = weapon("[[Big shot](https://www.youtube.com/watch?v=-8p8VowCmgE)]","bj",RANGE_DIST,AREA_CIRCLE_4,63,60,1997,strength=20,percing=10,emoji='<:bigshot:892756699277037569>',message="{0} PROPOSE UN [[Big shot](https://www.youtube.com/watch?v=-8p8VowCmgE)] À {1} :",area=AREA_LINE_2)
nemefaux = weapon("Faux vangeresse","bk",RANGE_MELEE,AREA_CIRCLE_2,64,70,500,strength=15,endurance=10,resistance=5,emoji='<:avengerScythe:893227827942522951>',area=AREA_ARC_1)
waterspell = weapon("Grimoire de l'eau","bl",RANGE_LONG,AREA_CIRCLE_4,73,60,350,magie=20,precision=10,emoji='<:waterspellbook:892963508248002590>',affinity=ELEMENT_WATER,message="{0} projète un éclat de glace sur {1} :",use=MAGIE)
earthspell = weapon("Grimoire des terres","bm",RANGE_MELEE,AREA_CIRCLE_2,86,60,350,magie=10,endurance=10,resistance=10,emoji='<:earthspellbook:892963483665174578>',affinity=ELEMENT_EARTH,use=MAGIE,message="{0} fait apparaitre des pics rocheux sous {1} :")
airspell = weapon("Grimoire des vents","bn",RANGE_MELEE,AREA_CIRCLE_2,17,70,350,magie=10,resistance=10,agility=10,emoji='<:airspellbook:892963551159922718>',affinity=ELEMENT_AIR,use=MAGIE,area=AREA_ARC_1,message="{0} forme des vents violents autour de {1}",repetition=3)
airsword = weapon("Épée des vents","bo",RANGE_MELEE,AREA_CIRCLE_1,70,70,350,strength=15,agility=15,emoji='<:airsword:892963581031772170>',repetition=1,affinity=ELEMENT_AIR,area=AREA_ARC_2,use=STRENGTH,message="{0} file comme le vent !")
armilame = weapon("Épée empoisonnée","bp",RANGE_MELEE,AREA_CIRCLE_1,58,75,350,magie=10,resistance=5,emoji='<:amirlame:894643896120918107>',effectOnUse="me",use=MAGIE)
shehisa = weapon("Faux des ombres","bq",RANGE_MELEE,AREA_CIRCLE_1,74,75,350,strength=10,resistance=5,emoji='<:shefaux:896924311221305395>',effectOnUse='mx')
machinist = weapon("Canon du machiniste fantaisiste","br",RANGE_LONG,AREA_CIRCLE_4,63,60,350,strength=20,precision=10,area=AREA_LINE_2,emoji='<:mach:896924290170093580>')
ironSword = weapon("Épée en fer","bs",RANGE_MELEE,AREA_CIRCLE_1,81,60,350,endurance=20,resistance=10,emoji='<:ironSword:899994609504092171>',area=AREA_ARC_1)
darkSpellBook = weapon("Grimoire des ténèbres","bt",RANGE_DIST,AREA_CIRCLE_4,35,100,350,magie=15,effectOnUse="mw",affinity=ELEMENT_DARKNESS,use=MAGIE,emoji='<:darkspellbook:892963455773048914>')
lightSpellBook = weapon("Grimoire de la lumière","bu",RANGE_DIST,AREA_CIRCLE_4,35,100,350,charisma=10,intelligence=5,effectOnUse="mt",type=TYPE_HEAL,use=CHARISMA,target=ALLIES,emoji='<:lightspellbook:892963432222036018>',affinity=ELEMENT_LIGHT)
musical = weapon("Détubeur Musical",'bv',RANGE_LONG,AREA_CIRCLE_5,26,50,1,intelligence=30,repetition=3,use=INTELLIGENCE,emoji='<:musicalGoo:901851887291215933>')
gwenCoupe = weapon("Ciseaux de la poupée","bw",RANGE_MELEE,AREA_CIRCLE_1,10,60,price=1,repetition=5,area=AREA_CONE_2,magie=10,resistance=5,emoji='<:gwencoupecoupe:902912449261473875>',effect="ob",use=MAGIE)
inkbrella2 = weapon("Para-Encre alt.","bx",RANGE_MELEE,AREA_CIRCLE_1,32,45,price=472,endurance=5,resistance=5,intelligence=5,repetition=3,use=INTELLIGENCE,effect='ok',emoji='<:heroInkBrella:905282148917993513>',needRotate=False)
concentraceurZoom = weapon("Concentraceur Zoom","bz",RANGE_LONG,AREA_CIRCLE_6,51,60,1,strength=10,precision=10,percing=10,area=AREA_LINE_2,emoji='<:splatterscope:905283725036757002>')
klikliSword = weapon("Épée vengeresse","ca",RANGE_MELEE,AREA_CIRCLE_1,53,65,1,repetition=2,emoji='<:KlikliSword:907300288531169340>',strength=20,resistance=10)
julieWeapEff = effect("Régénération vampirique","julieWeapEff",CHARISMA,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,turnInit=3,lvl=3,power=10,stackable=True,emoji=uniqueEmoji('<:vampBall:916199488891273276>'))
julieWeap = weapon("Réceptacle vampirique","cb",RANGE_LONG,AREA_CIRCLE_6,35,100,500,charisma=15,type=TYPE_HEAL,target=ALLIES,use=CHARISMA,emoji='<:vampBall:916199488891273276>',effectOnUse=julieWeapEff)

blueButterFlyEff = effect("Bouclier du papillon bleu","blueButterflyShield",INTELLIGENCE,overhealth=35,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,lightShield=True,description="Armure Légère\nLes armures légères absorbent pas de dégâts supplémentaire en disparaissant")
blueButterfly = weapon("Papillon bleu","cf",RANGE_DIST,price=500,effectiveRange=AREA_CIRCLE_4,needRotate=False,effectOnUse=blueButterFlyEff,use=INTELLIGENCE,target=ALLIES,type=TYPE_HEAL,power=0,emoji='<:bluebutterfly:910586341614567425>',sussess=100,intelligence=15)
butterflyRed = weapon("Papillon Rouge","cg",RANGE_LONG,AREA_CIRCLE_5,50,80,150,magie=20,precision=10,emoji='<:redbuterfly:912441401508233226>',use=MAGIE,needRotate=False,message="{0} demande à son papillon d'attaquer {1} :")

luth = weapon("Luth",'ch',RANGE_DIST,AREA_CIRCLE_4,62,70,1,intelligence=15,charisma=15,use=INTELLIGENCE,emoji='<:luth:911647678037905458>')
krystalFist = weapon("Poings cristalins","ci",RANGE_MELEE,AREA_CIRCLE_1,38,60,price=1,repetition=3,strength=5,resistance=15,endurance=10,emoji='<:krystalopoings:916120173130448948>')

eternalInkEff = effect("Encre Éternelle","eternalInk",turnInit=-1,unclearable=True,description="Au début du combat, converti l'intégralité de vos statistiques d'Actions positives dans la statistique utilisée par votre arme principale (Ratio de 70%)",emoji=uniqueEmoji('<:inkEter:918083455731007499>'))
eternalInkSword = weapon("Épée de l'Encre Éternelle","cj",RANGE_MELEE,AREA_CIRCLE_1,74,75,1,strength=15,effect=eternalInkEff,emoji='<:inkEtSword:918071301913079808>',needRotate=False)
eternalInkStick = weapon("Dague de l'Encre Éternelle","ck",RANGE_MELEE,AREA_CIRCLE_1,58,75,1,agility=15,effect=eternalInkEff,use=AGILITY,emoji='<:inkEtDague:918083344250568734>',needRotate=False)
eternalInkShield = weapon("Bouclier de l'Encre Éternelle","cl",RANGE_MELEE,AREA_CIRCLE_1,58,75,1,endurance=15,effect=eternalInkEff,use=ENDURANCE,emoji='<:inkEtShield:918083377712734251>',needRotate=False)
eternalInkStaff = weapon("Baguette de l'Encre Éternelle","cm",RANGE_DIST,AREA_CIRCLE_4,46,75,1,magie=15,effect=eternalInkEff,use=MAGIE,emoji='<:inkEtStick:918083398956900392>',needRotate=False)
eternalInkWind = weapon("Éventail de l'Encre Éternelle","cn",RANGE_DIST,AREA_CIRCLE_4,46,75,1,charisma=15,effect=eternalInkEff,use=CHARISMA,emoji='<:inkEtFan:918083360545443870>',needRotate=False)
eternalInkScience = weapon("Gant de l'Encre Éternelle","co",RANGE_DIST,AREA_CIRCLE_4,46,75,1,intelligence=15,effect=eternalInkEff,use=INTELLIGENCE,emoji='<:inkEtGlove:918083419081170954>',needRotate=False)
eternalInkBow = weapon("Arc de l'Encre Éternelle","cp",RANGE_LONG,AREA_CIRCLE_6,37,75,1,precision=15,effect=eternalInkEff,use=PRECISION,emoji='<:inkEtBow:918083434860146710>',needRotate=False)

eternalInkWeapons = [eternalInkSword,eternalInkStick,eternalInkShield,eternalInkStaff,eternalInkWind,eternalInkScience,eternalInkBow]
eternalInkWeaponIds = [eternalInkSword.id,eternalInkStick.id,eternalInkShield.id,eternalInkStaff.id,eternalInkWind.id,eternalInkScience.id,eternalInkBow.id]
etInkBases = ["<:BaseinkEtSword:918071336994230302>","<:BaseinkEtDague:918169899170426960>","<:BaseinkEtShield:918169963624292392>","<:BaseinkEtStick:918170006649458741>","<:BaseinkEtFan:918170045111226438>","<:BaseinkEtGlove:918170092678815744>","<:BaseinkEtBow:918170130041671720>"]
etInkLines = ["<:LineinkEtSword:918071323618607144>","<:LineinkEtDague:918169920951418890>","<:LineinkEtShield:918169983152975893>","<:LineinkEtStick:918170024370380841>","<:LineinkEtFan:918170074400055317>","<:LineinkEtGlove:918170114984124426>","<:LineinkEtBow:918170144499466300>"]

purpleSecretEff = effect("Secretum purpureum prædictas","purpleSecrets",turnInit=-1,emoji=uniqueEmoji('<:plsLetMeSleep:919713870858317875>'),area=AREA_DONUT_2,description="Lorsqu'un adversaire meurt, s'il portait au moins 1 effet __Poison d'Estialba__ venant de votre part, une explosion **indirecte magique** dont la puissance dépend de celles de vos effets __Poison d'Estialba__ et de leur durée restante sur le porteur se produit\nTous les ennemis dans la zone d'effet reçoive un effet __Poison d'Estialba__ ayant une puissance équivalente à {0}% de celle de l'effet de base\n\n__Vous empèche d'utiliser votre arme principale !__",reject=['np',"ns","pacteDeSang","pacteD'âme"],power=25)
secretum = weapon("Secretum purpureum prædictas","cq",RANGE_DIST,AREA_CIRCLE_3,30,100,750,emoji='<:plsLetMeSleep:919713870858317875>',magie=10,resistance=5,effect=purpleSecretEff,use=MAGIE,affinity=ELEMENT_DARKNESS,ignoreAutoVerif=True)

# Weapon
weapons = [secretum,
    eternalInkSword,eternalInkStick,eternalInkShield,eternalInkStaff,eternalInkWind,eternalInkScience,eternalInkBow,
    julieWeap,blueButterfly,butterflyRed,luth,krystalFist,musical,gwenCoupe,inkbrella2,concentraceurZoom,klikliSword,darkSpellBook,lightSpellBook,ironSword,machinist,shehisa,armilame,airsword,waterspell,earthspell,airspell,nemefaux,bigshot,serringue,fauc,rapiere,lunarBonk,magicSword,dtsword,butterflyP,butterflyR,depha,legendarySword,spellBook,mic,butterfly,dualJetSkelcher,squiffer,flexi,splatling,dualies,clashBlaster,hourglass1Weap,plume,mainLibre,splattershotJR,splattershot,roller,splatcharger,miniBrush,inkbrella,blaster,jetSkelcher,kcharger,HunterRiffle,firework
]
