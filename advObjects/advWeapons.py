from classes import *
from constantes import *
from advObjects.advSkills import tablElemEff, coroWind, plumRemEff, estial, bleeding, krysUlt, bloodButterfly
from advObjects.advStuffs import shieltron

splattershot = weapon("Liquidateur","ab",RANGE_DIST,AREA_CIRCLE_3,40,50,280,agility=10,precision=20,strength=20,repetition=3,emoji = '<:splattershot:866367647113543730>',affinity=ELEMENT_NEUTRAL)
roller = weapon("Rouleau","ac",RANGE_MELEE,AREA_CIRCLE_1,64,70,340,strength=25,endurance=15,resistance=10,emoji = '<:splatroller:866367775722831934>',needRotate=False,affinity=ELEMENT_AIR,area=AREA_CONE_2,damageOnArmor=0.8)
splatcharger = weapon("Fusil de précision anti-matériel","ad",RANGE_LONG,AREA_CIRCLE_5,83,60,482,strength=20,precision=30,emoji = '<:sniperRifle:903115499204923402>',affinity=ELEMENT_WATER)
miniBrush = weapon("Epinceau","ae",RANGE_MELEE,AREA_CIRCLE_1,28,45,224,agility=20,strength=20,endurance=10,repetition=3,emoji='<:inkBrush:866463573580578816>',needRotate=False)
inkbrella = weapon("Para-Encre","ag",RANGE_MELEE,AREA_CIRCLE_1,38,45,price=472,endurance=15,resistance=10,strength=5,repetition=3,effects='lp',emoji='<:splatbrella:866464991255199834>',needRotate=False)
blaster = weapon("Eclatblasteur","ah",RANGE_DIST,AREA_CIRCLE_3,84,50,150,agility=15,strength=20,precision=15,area=AREA_CIRCLE_1,emoji='<:blaster:866463931304378418>')
jetSkelcher = weapon("Nettoyeur XL","ai",RANGE_LONG,AREA_CIRCLE_5,31,40,200,strength=25,precision=20,percing=5,repetition=3,emoji='<:squelsher:866464376319115281>',affinity=ELEMENT_WATER)
dualies = weapon("Double Encreur","aj",RANGE_DIST,AREA_CIRCLE_3,42,35,150,strength=20,agility=20,precision=10,repetition=3,emoji='<:splatDualies:866465264434806815>',needRotate=False,affinity=ELEMENT_AIR)
kcharger = weapon("Concentraceur alt.","ak",RANGE_MELEE,AREA_CIRCLE_1,36,60,200,strength=30,agility=15,critical=5,repetition=3,emoji='<:kcharger:870870886939508737>',message="{0} frappe {1} avec son arme :",use=STRENGTH)
HunterRiffle = weapon("Fusil de chasseur","al",RANGE_DIST,AREA_CIRCLE_4,61,65,250,precision=20,strength=10,effects="ls",emoji="<:hunterRifle:872034208095297597>",affinity=ELEMENT_NEUTRAL)
firework = weapon("Arbalette avec feu d'artifice","am",RANGE_LONG,AREA_CIRCLE_4,56,50,150,strength=30,precision=15,percing=5,emoji='<:crossbow:871746122899664976>',area=AREA_CONE_2)
plume = weapon("Plumes tranchantes","ao",RANGE_DIST,AREA_CIRCLE_4,60,50,250,taille=0,precision=15,strength=10,percing=5,emoji='<:plume:871893045296128030>',area=AREA_CONE_2,needRotate=False,affinity=ELEMENT_AIR,effectOnUse=incur[2])
hourglass1Weap = weapon("Sablier intemporel","ap",RANGE_DIST,AREA_CIRCLE_3,50,100,250,charisma=25,taille=0,intelligence=25,target=ALLIES,affinity=ELEMENT_TIME,type=TYPE_HEAL,emoji='<:hourglass1:872181735062908978>',use=CHARISMA,needRotate=False)
clashBlaster = weapon("Rafa-Blasteur","aq",RANGE_MELEE,AREA_CIRCLE_2,28,40,250,endurance=10,agility=10,resistance=10,strength=10,precision=10,emoji='<:clashBlaster:877666681869176853>',area=AREA_CIRCLE_1,repetition=3)
splatling = weapon("Badigeonneur","as",RANGE_LONG,AREA_CIRCLE_5,33,30,300,precision=15,strength=35,intelligence=10,agility=-10,repetition=3,emoji='<:splatling:877666764736061490>')
flexi = weapon("Flexi-Rouleau","at",RANGE_DIST,AREA_CIRCLE_3,85,70,300,strength=15,precision=10,critical=5,endurance=10,resistance=10,emoji='<:flexaRoller:877666714760925275>',needRotate=False)
squiffer = weapon("Décap' Express","au",RANGE_DIST,AREA_CIRCLE_4,78,70,300,strength=15,agility=15,precision=10,percing=10,emoji='<:skiffer:877666730225328138>')
dualJetSkelcher = weapon("Nettoyeur Duo","av",RANGE_LONG,AREA_CIRCLE_5,25,50,200,strength=15,magie=15,precision=20,repetition=3,emoji='<:DualSkelcher:877666662801883237>',damageOnArmor=1.33)
butterfly = weapon("Papillon Blanc","aw",RANGE_LONG,AREA_CIRCLE_5,35,80,150,taille=0,charisma=35,use=CHARISMA,intelligence=15,emoji='<:butterflyB:883627125561786428>',target=ALLIES,type=TYPE_HEAL,needRotate=False,message="{0} demande à son papillon de soigner {1} :")
spellBook = weapon("Grimoire de feu","ay",RANGE_DIST,AREA_CIRCLE_4,50,75,200,magie=40,taille=0,percing=10,emoji='<:spellBook:878723144326725744>',needRotate=False,use=MAGIE,area=AREA_CIRCLE_1,affinity=ELEMENT_FIRE,message="{0} lance une boule de feu sur {1}")
legendarySword=weapon("Épée et Bouclier de Légende","az",RANGE_MELEE,AREA_CIRCLE_1,61,85,300,strength=15,resistance=5,endurance=10,emoji='<:masterSword:880008948445478962>',affinity=ELEMENT_LIGHT,effects=shieltron)
depha = weapon("Lame Dimensionnelle","ba",RANGE_MELEE,AREA_CIRCLE_1,72,90,300,strength=50,emoji='<:ailSword:922696057350127697>')
butterflyR = weapon("Papillon Rose","bb",RANGE_LONG,AREA_CIRCLE_5,62,80,150,taille=0,charisma=30,intelligence=20,emoji='<:butterflyR:883627168406577172>',use=CHARISMA,needRotate=False,message="{0} demande à son papillon d'attaquer {1} :")
butterflyP = weapon("Papillon Violet","bc",RANGE_LONG,AREA_CIRCLE_5,28,100,250,taille=0,area=AREA_CIRCLE_1,magie=30,effectOnUse=estial.id,needRotate=False,emoji='<:butterflyV:883627142615805962>',type=TYPE_DAMAGE,message="{0} demande à son papillon d'empoisonner {1} :",use=MAGIE)
dtsword = weapon("Épée de Détermination","bd",RANGE_MELEE,AREA_CIRCLE_1,61,85,500,strength=15,resistance=10,critical=5,emoji='<:dtSword:884802145239588884>',affinity=ELEMENT_NEUTRAL,effects="lg")
magicSword = weapon("Épée de MagicalGirl","be",RANGE_MELEE,AREA_CIRCLE_1,92,70,200,endurance=10,charisma=30,resistance=10,emoji="<:magicSword:885241611682975744>",use=CHARISMA)
lunarBonk = weapon("Bâton Lunaire","bf",RANGE_MELEE,AREA_CIRCLE_1,76,85,250,endurance=20,intelligence=20,resistance=10,emoji="<:lunarBonk:887347614448746516>",use=INTELLIGENCE,affinity=ELEMENT_LIGHT)
rapiere = weapon("Rapière en argent","bg",RANGE_DIST,AREA_CIRCLE_3,80,60,0,magie=10,intelligence=10,percing=5,endurance=5,use=MAGIE,emoji='<:clemWeap:915358467773063208>',effectOnUse=bloodButterfly)
fauc = weapon("Faux Tourmentée","bh",RANGE_MELEE,AREA_CIRCLE_2,69,75,0,strength=25,percing=5,emoji='<a:akifauxgif:887335929650507776>',affinity=ELEMENT_DARKNESS,effectOnUse=incur[2])
serringue = weapon("Serringue","bi",RANGE_DIST,AREA_CIRCLE_3,35,100,350,charisma=30,precision=20,emoji='<:seringue:887402558665142343>',target=ALLIES,type=TYPE_HEAL,use=CHARISMA,affinity=ELEMENT_LIGHT,message="{0} fait une perfusion à {1}")
bigshot = weapon("[[Big shot](https://www.youtube.com/watch?v=-8p8VowCmgE)]","bj",RANGE_DIST,AREA_CIRCLE_4,63,60,1997,strength=20,percing=10,magie=20,emoji='<:bigshot:892756699277037569>',message="{0} PROPOSE UN [[Big shot](https://www.youtube.com/watch?v=-8p8VowCmgE)] À {1} :",area=AREA_LINE_2)
nemefaux = weapon("Faux vangeresse","bk",RANGE_MELEE,AREA_CIRCLE_2,64,70,500,strength=25,endurance=15,resistance=10,emoji='<:avengerScythe:893227827942522951>',area=AREA_ARC_1)
waterspell = weapon("Grimoire de l'eau","bl",RANGE_LONG,AREA_CIRCLE_4,91,60,350,magie=30,precision=20,taille=0,emoji='<:waterspellbook:892963508248002590>',affinity=ELEMENT_WATER,message="{0} projète un éclat de glace sur {1} :",use=MAGIE)
earthspell = weapon("Grimoire des terres","bm",RANGE_MELEE,AREA_CIRCLE_2,81,80,350,magie=25,endurance=15,taille=0,resistance=10,emoji='<:earthspellbook:892963483665174578>',affinity=ELEMENT_EARTH,use=MAGIE,message="{0} fait apparaitre des pics rocheux sous {1} :")
airspell = weapon("Grimoire des vents","bn",RANGE_MELEE,AREA_CIRCLE_2,21,70,350,magie=25,resistance=10,taille=0,agility=15,emoji='<:airspellbook:892963551159922718>',affinity=ELEMENT_AIR,use=MAGIE,area=AREA_ARC_1,message="{0} forme des vents violents autour de {1}",repetition=3)
airsword = weapon("Épée des vents","bo",RANGE_MELEE,AREA_CIRCLE_1,64,70,350,strength=30,agility=20,emoji='<:airsword:892963581031772170>',repetition=1,affinity=ELEMENT_AIR,area=AREA_ARC_2,use=STRENGTH,message="{0} file comme le vent !")
armilame = weapon("Épée empoisonnée","bp",RANGE_MELEE,AREA_CIRCLE_1,69,75,350,magie=20,resistance=10,emoji='<:amirlame:894643896120918107>',effectOnUse=estial.id,use=MAGIE)
shehisa = weapon("Faux des ombres","bq",RANGE_MELEE,AREA_CIRCLE_1,69,75,350,strength=20,resistance=10,emoji='<:shefaux:896924311221305395>',effectOnUse='mx')
machinist = weapon("Canon du machiniste fantaisiste","br",RANGE_LONG,AREA_CIRCLE_4,63,60,350,strength=30,precision=20,area=AREA_LINE_2,emoji='<:mach:896924290170093580>')
ironSword = weapon("Épée en fer","bs",RANGE_MELEE,AREA_CIRCLE_1,75,60,350,endurance=20,resistance=10,strength=20,emoji='<:ironSword:899994609504092171>',area=AREA_ARC_1)
darkSpellBook = weapon("Grimoire des ténèbres","bt",RANGE_DIST,AREA_CIRCLE_4,44,100,350,magie=30,taille=0,effectOnUse="mw",affinity=ELEMENT_DARKNESS,use=MAGIE,emoji='<:darkspellbook:892963455773048914>')
lightSpellBook = weapon("Grimoire de la lumière","bu",RANGE_DIST,AREA_CIRCLE_4,20,100,350,charisma=15,intelligence=15,effectOnUse="mt",type=TYPE_HEAL,use=CHARISMA,target=ALLIES,taille=0,emoji='<:lightspellbook:892963432222036018>',affinity=ELEMENT_LIGHT)
musical = weapon("Détubeur Musical",'bv',RANGE_LONG,AREA_CIRCLE_5,33,50,1,intelligence=30,precision=20,repetition=3,use=INTELLIGENCE,emoji='<:musicalGoo:901851887291215933>')
gwenCoupe = weapon("Ciseaux de la poupée","bw",RANGE_MELEE,AREA_CIRCLE_1,12,60,price=1,repetition=3,area=AREA_CONE_2,magie=20,resistance=10,emoji='<:gwencoupecoupe:902912449261473875>',effects="ob",use=MAGIE)
inkbrella2 = weapon("Para-Encre alt.","bx",RANGE_MELEE,AREA_CIRCLE_1,38,45,price=472,endurance=10,resistance=10,intelligence=10,repetition=3,use=INTELLIGENCE,effects='ok',emoji='<:heroInkBrella:905282148917993513>',needRotate=False)
concentraceurZoom = weapon("Concentraceur Zoom","bz",RANGE_LONG,AREA_CIRCLE_6,51,60,1,strength=25,precision=15,percing=10,area=AREA_LINE_2,emoji='<:splatterscope:905283725036757002>')
klikliSword = weapon("Épée vengeresse","ca",RANGE_MELEE,AREA_CIRCLE_1,50,65,1,repetition=2,emoji='<:KlikliSword:907300288531169340>',strength=30,resistance=10,endurance=10)
julieWeapEff = effect("Régénération vampirique","julieWeapEff", stat=CHARISMA,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_START_OF_TURN,turnInit=3,lvl=3,power=10,stackable=True,emoji=uniqueEmoji('<:vampBall:916199488891273276>'))
julieWeap = weapon("Réceptacle vampirique","cb",RANGE_LONG,AREA_CIRCLE_6,20,100,500,charisma=20,precision=10,type=TYPE_HEAL,target=ALLIES,taille=0,use=CHARISMA,emoji='<:vampBall:916199488891273276>',effectOnUse=julieWeapEff)

blueButterFlyEff = effect("Bouclier du papillon bleu","blueButterflyShield", stat=INTELLIGENCE,overhealth=35,trigger=TRIGGER_DAMAGE,type=TYPE_ARMOR,lightShield=True,description="Armure Légère\nLes armures légères absorbent pas de dégâts supplémentaire en disparaissant")
blueButterfly = weapon("Papillon Bleu","cf",RANGE_DIST,price=500,taille=0,effectiveRange=AREA_CIRCLE_4,needRotate=False,effectOnUse=blueButterFlyEff,use=INTELLIGENCE,target=ALLIES,type=TYPE_HEAL,power=0,emoji='<:bluebutterfly:910586341614567425>',accuracy=100,intelligence=30)
butterflyRed = weapon("Papillon Rouge","cg",RANGE_LONG,AREA_CIRCLE_5,62,80,150,magie=30,precision=15,critical=5,taille=0,emoji='<:redbuterfly:912441401508233226>',use=MAGIE,needRotate=False,message="{0} demande à son papillon d'attaquer {1} :")

luth = weapon("Luth",'ch',RANGE_DIST,AREA_CIRCLE_4,78,70,1,intelligence=35,charisma=15,use=INTELLIGENCE,emoji='<:luth:911647678037905458>')
krystalFistEff = effect("Vol d'Armure","armorSteal",power=20,turnInit=-1,unclearable=True,emoji=krysUlt.emoji,description="Vous octroi **{0}%** de vol d'armure durant tout le combat")
krystalFist = weapon("Poings cristalins","ci",RANGE_MELEE,AREA_CIRCLE_1,28,60,price=1,repetition=3,strength=30,resistance=10,endurance=10,intelligence=-20,emoji='<:krystalopoings:916120173130448948>',effects=krystalFistEff)

eternalInkEff = effect("Encre Éternelle","eternalInk",turnInit=-1,unclearable=True,description="Au début du combat, converti l'intégralité de vos statistiques d'Actions positives dans la statistique utilisée par votre arme principale (Ratio de 70%)",emoji=uniqueEmoji('<:inkEter:918083455731007499>'))
eternalInkSword = weapon("Épée de l'Encre Éternelle","cj",RANGE_MELEE,AREA_CIRCLE_1,69,75,1,strength=30,effects=eternalInkEff,emoji='<:inkEtSword:918071301913079808>',needRotate=False)
eternalInkStick = weapon("Dague de l'Encre Éternelle","ck",RANGE_MELEE,AREA_CIRCLE_1,69,75,1,agility=30,effects=eternalInkEff,taille=0,use=AGILITY,emoji='<:inkEtDague:918083344250568734>',needRotate=False)
eternalInkShield = weapon("Bouclier de l'Encre Éternelle","cl",RANGE_MELEE,AREA_CIRCLE_1,69,75,1,endurance=30,effects=eternalInkEff,taille=0,use=ENDURANCE,emoji='<:inkEtShield:918083377712734251>',needRotate=False)
eternalInkStaff = weapon("Baguette de l'Encre Éternelle","cm",RANGE_DIST,AREA_CIRCLE_4,58,75,1,magie=30,effects=eternalInkEff,use=MAGIE,emoji='<:inkEtStick:918083398956900392>',needRotate=False)
eternalInkWind = weapon("Éventail de l'Encre Éternelle","cn",RANGE_DIST,AREA_CIRCLE_4,58,75,1,charisma=30,effects=eternalInkEff,taille=0,use=CHARISMA,emoji='<:inkEtFan:918083360545443870>',needRotate=False)
eternalInkScience = weapon("Gant de l'Encre Éternelle","co",RANGE_DIST,AREA_CIRCLE_4,58,75,1,intelligence=30,effects=eternalInkEff,taille=0,use=INTELLIGENCE,emoji='<:inkEtGlove:918083419081170954>',needRotate=False)
eternalInkBow = weapon("Arc de l'Encre Éternelle","cp",RANGE_LONG,AREA_CIRCLE_6,48,75,1,precision=30,effects=eternalInkEff,use=PRECISION,emoji='<:inkEtBow:918083434860146710>',needRotate=False)
eternalInkWeapons = [eternalInkSword,eternalInkStick,eternalInkShield,eternalInkStaff,eternalInkWind,eternalInkScience,eternalInkBow]
eternalInkWeaponIds = [eternalInkSword.id,eternalInkStick.id,eternalInkShield.id,eternalInkStaff.id,eternalInkWind.id,eternalInkScience.id,eternalInkBow.id]
etInkBases = ["<:BaseinkEtSword:918071336994230302>","<:BaseinkEtDague:918169899170426960>","<:BaseinkEtShield:918169963624292392>","<:BaseinkEtStick:918170006649458741>","<:BaseinkEtFan:918170045111226438>","<:BaseinkEtGlove:918170092678815744>","<:BaseinkEtBow:918170130041671720>"]
etInkLines = ["<:LineinkEtSword:918071323618607144>","<:LineinkEtDague:918169920951418890>","<:LineinkEtShield:918169983152975893>","<:LineinkEtStick:918170024370380841>","<:LineinkEtFan:918170074400055317>","<:LineinkEtGlove:918170114984124426>","<:LineinkEtBow:918170144499466300>"]
purpleSecretEff = effect("Sec. pur. prædi.","purpleSecrets",turnInit=-1,emoji=uniqueEmoji('<:sdf:919713870858317875>'),area=AREA_DONUT_2,description="Lorsqu'un adversaire meurt, s'il portait au moins 1 effet __Poison d'Estialba__ venant de votre part, une explosion **indirecte magique** dont la puissance dépend de celles de vos effets __Poison d'Estialba__ et de leur durée restante sur le porteur se produit\nTous les ennemis dans la zone d'effet reçoive un effet __Poison d'Estialba__ ayant une puissance équivalente à {0}% de celle de l'effet de base",reject=['np',"ns","pacteDeSang","pacteD'âme"],power=25)
secretum = weapon("Secretum purpureum prædictas","cq",RANGE_DIST,AREA_CIRCLE_3,60,80,750,emoji='<:sdf:919713870858317875>',magie=20,intelligence=10,effects=purpleSecretEff,use=MAGIE,affinity=ELEMENT_DARKNESS,effectOnUse=estial.id,effPowerPurcent=50,priority=WEAPON_PRIORITY_LOW)
critBonusEff = effect("Bonus critique","scopeCritBonus",turnInit=-1,unclearable=True,emoji=sameSpeciesEmoji('<:critB:925763298346033193>','<:critR:925763310383677490>'),critDmgUp=5,description="Augmente les dégâts de coup critique de 5%")
ElitherScope = weapon("Extraceur Zoom +","cr",RANGE_LONG,AREA_CIRCLE_7,49,65,1,precision=30,effects=critBonusEff,emoji='<:elitherScope:925762142202921040>')
gravEff = effect("Gravitation","grav",turnInit=-1,unclearable=True,description="Augmente progressivement votre agression au fur et à mesure du combat mais __empêche l'utilisation de votre arme principale__",emoji='<a:ble:925774688641228810>')
grav = weapon("Gravité","cs",RANGE_MELEE,AREA_CIRCLE_1,69,75,1,endurance=20,taille=0,resistance=10,effects=gravEff,emoji='<:bl:925774629711282196>',use=ENDURANCE)
darkbluebutterfly = weapon("Papillon Bleu Marine",'ct',RANGE_MELEE,AREA_CIRCLE_2,86,75,1,magie=20,endurance=20,taille=0,resistance=10,use=MAGIE,needRotate=False,emoji='<:dbb:926954332593725511>')
kardia = effect("Kardia","kardia",type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_WEAPON_USE,power=35,turnInit=-1,unclearable=True,description="Lorsque vous attaquez avec votre arme principale, soigne l'allié le plus blessé avec une puissance de **15**\nAugmente la probabilité d'utiliser son arme principale de **50%** en mode automatique",emoji='<:kar:929860644461740133>',stat=CHARISMA,area=AREA_LOWEST_HP_ALLIE)
whiteSpiritWings = weapon("Ailes de l'esprit blanc","cu",RANGE_DIST,AREA_CIRCLE_4,46,75,1,taille=0,charisma=20,precision=10,effects=kardia,use=CHARISMA,needRotate=False,emoji='<:wws:929847728077406279>',ignoreAutoVerif=True,priority=WEAPON_PRIORITY_HIGH)
diag = effect('Diagnostique',"diagEuk", stat=INTELLIGENCE,overhealth=35,emoji=sameSpeciesEmoji("<:ekb:929866306554056725>" ,"<:ekr:929866324153360394>"),type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
eukrasia = effect("Eukrasia","eukrasia",type=TYPE_BOOST,trigger=TRIGGER_WEAPON_USE,turnInit=-1,unclearable=True,description="Lorsque vous attaquez avec votre arme principale, donne l'effet __Diagnostique__ à l'allié le plus blssée\nAugmente la probabilité d'utiliser son arme principale de **50%** en mode automatique",emoji='<:ekr:929860664497942558>',stat=INTELLIGENCE,callOnTrigger=diag,area=AREA_LOWEST_HP_ALLIE)
bleuSpiritWings = weapon("Ailes de l'esprit bleu","cv",RANGE_DIST,AREA_CIRCLE_4,46,75,1,intelligence=20,precision=10,effects=eukrasia,use=INTELLIGENCE,needRotate=False,emoji='<:bws:929847711941935214>',ignoreAutoVerif=True,priority=WEAPON_PRIORITY_HIGH)

neutralCard = effect("Carte Astrale","astralCard",stat=CHARISMA,description="Cette carte devient une des cartes astrale, appropriée à l'aspiration du receveur, lorsqu'elle est octroyée",emoji=uniqueEmoji('<:deck:932400761176981605>'),turnInit=2)
cardsDeck = effect("Deck de cartes","astro", stat=CHARISMA,emoji=uniqueEmoji('<:deck:932400761176981605>'),turnInit=-1,unclearable=True,description="À chaque début de tour, désigne aléatoirement un allié et lui octroi un effet boostant ses statistiques en fonction de son aspiration",callOnTrigger=neutralCard,trigger=TRIGGER_START_OF_TURN,area=AREA_RANDOMALLIE_1)
cardBer = effect("La balance berserk",'BerCard', stat=CHARISMA,strength=5,resistance=3,emoji='<:balance:932399888422043739>',turnInit=2)
cardPlume = effect("La balance agile",'PoiCard', stat=CHARISMA,strength=5,agility=5,emoji='<:balance:932399888422043739>',turnInit=2)
cardObs = effect("La flèche précise",'ObsCard', stat=CHARISMA,strength=5,precision=5,emoji='<:fleche:932399905807433738>',turnInit=2)
cardTet = effect("La flèche bornée",'TetCard', stat=CHARISMA,strength=5,magie=5,emoji='<:fleche:932399905807433738>',turnInit=2)
cardMag = effect("La tour magique",'MagCard', stat=CHARISMA,magie=5,precision=5,emoji='<:tour:932399958936657921>',turnInit=2)
cardEnch = effect("La tour enchantée",'EncCard', stat=CHARISMA,magie=5,resistance=3,emoji='<:tour:932399958936657921>',turnInit=2)
cardAlt = effect("Le tronc revifiant",'AltCard', stat=CHARISMA,charisma=7,emoji='<:tronc:932399933724700763>',turnInit=2)
cardPre = effect("Le tronc résistant",'PreCard', stat=CHARISMA,intelligence=7,emoji='<:tronc:932399933724700763>',turnInit=2)
cardIdo = effect("L'aiguilère attentionée",'IdoCard', stat=CHARISMA,charisma=5,intelligence=5,emoji='<:aiguilere:932399946659921990>',turnInit=2)
cardPro = effect("L'aiguilère ponctuelle",'ProCard', stat=CHARISMA,resistance=3,intelligence=5,emoji='<:aiguilere:932399946659921990>',turnInit=2)
cardSorc = effect("La tour intemporelle",'SorCard', stat=CHARISMA,magie=5,intelligence=5,emoji='<:tour:932399958936657921>',turnInit=2)
cardVig = effect('Le tronc solide',"vigiCard", stat=CHARISMA,charisma=5,resistance=3,emoji='<:tronc:932399933724700763>',turnInit=2)
cardInv = effect("L'épieu versatil",'InvCard', stat=CHARISMA,charisma=2,intelligence=2,strength=2,magie=2,emoji='<:epieu:932399920873357382>',turnInit=2)
cardAtt = effect("La flèche empoisonnée",'ObsCard', stat=CHARISMA,strength=5,intelligence=5,emoji='<:fleche:932399905807433738>',turnInit=2)
cardMas = effect("L'épieu versatil",'MasCard', stat=CHARISMA,charisma=5,endurance=5,emoji='<:epieu:932399920873357382>',turnInit=2)
cardAspi = [cardBer,cardObs,cardPlume,cardIdo,cardPre,cardTet,cardMag,cardAlt,cardEnch,cardPro,cardVig,cardSorc,cardIdo,cardAtt,cardMas,cardInv]

astroGlobe = weapon("Globe céleste",'cy',RANGE_LONG,AREA_CIRCLE_5,50,80,1,charisma=15,intelligence=15,priority=WEAPON_PRIORITY_LOW,effects=cardsDeck,use=CHARISMA,emoji='<:globe:932399865110093884>')

infDarkSword = weapon("Épée de l'Ombre Éternelle","cw",RANGE_MELEE,AREA_CIRCLE_1,power=61,accuracy=85,strength=10,agility=20,effects=shareTabl[2],use=AGILITY,emoji='<:lunaWeap:915358834543968348>')
infLightSword = weapon("Épée de la Lueur Éternelle","cx",RANGE_MELEE,AREA_CIRCLE_1,power=61,accuracy=85,resistance=10,charisma=20,effects=shareTabl[2],use=CHARISMA,emoji='<:lumSword:926874664175816735>')
magicWood = weapon("Baguette en argent",'dc',RANGE_LONG,AREA_CIRCLE_5,66,75,1,taille=0,magie=35,precision=15,use=MAGIE,emoji='<:magicWand:934585282907488307>')
magicMass = weapon("Masse argentée",'cz',RANGE_DIST,AREA_CIRCLE_3,75,80,1,magie=30,endurance=20,use=MAGIE,emoji='<:magicMasse:934585301463072778>')
magicSwordnShield = weapon("Bouclier Runique",'da',RANGE_MELEE,AREA_CIRCLE_1,74,70,1,magie=15,resistance=10,endurance=5,use=MAGIE,emoji='<:magicShield:934585318508736532>',needRotate=False,effects=shieltron)
keyblade = weapon("Keyblade",'db',RANGE_MELEE,AREA_CIRCLE_2,81,80,1,agility=10,strength=10,endurance=10,charisma=10,intelligence=10,emoji='<:kb:934497052723929108>',ignoreAutoVerif=True)
fleauHealEff = effect('Cicatrisation','altiWeapHealEff', stat=CHARISMA,stackable=True,power=15,turnInit=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL,description="Soigne légèrement en début de tour",emoji=sameSpeciesEmoji('<:flB:934615447263916103>','<:flR:934615460157198346>'))
fleauPassifEffect = effect('Bénidiction de la Compréhension','altiWeapPassifEff',callOnTrigger=fleauHealEff,turnInit=-1,unclearable=True,area=AREA_CIRCLE_2,emoji='<:flE:934615479732043776>',description="Lorsque vous attaquez avec votre arme, donne l'effet __Cicatrisation__ à tous vos alliés dans la zone d'effet\n\nAugmente de 50% la probabililté d'utiliser son arme principale en mode automatique",trigger=TRIGGER_WEAPON_USE)
fleau = weapon('Fléau de la Compréhension',"de",RANGE_MELEE,AREA_CIRCLE_2,72,50,1,charisma=10,resistance=10,endurance=10,priority=WEAPON_PRIORITY_HIGH,use=CHARISMA,effects=fleauPassifEffect,emoji='<:fleau:934615644622704641>',area=AREA_ARC_1)

micPinkBoostEff = effect("Chanson rose",'micPinkBoostEff', stat=CHARISMA,strength=3,magie=3,emoji='<:pinkMic:917838961236377690>')
micPinkBoost = effect("Vocalises roses",'micPinkBoost', stat=CHARISMA,turnInit=-1,unclearable=True,trigger=TRIGGER_WEAPON_USE,description="En attaquant avec votre arme principale, donne l'effet __Chanson rose__ aux alliés dans la zone d'effet",area=AREA_DONUT_2,callOnTrigger=micPinkBoostEff,emoji='<:pinkMic:917838961236377690>')
micPink = weapon("Micro rose","ax",RANGE_LONG,AREA_CIRCLE_5,53,75,300,charisma=20,precision=10,emoji='<:pinkMic:917838961236377690>',needRotate=False,use=CHARISMA,message="{0} pousse la chansonnette !",taille=0,effects=micPinkBoost)
micRedBoostEff = effect("Chanson rouge",'micRedBoostEff', stat=CHARISMA,strength=5,emoji='<:redMic:936781924620451850>')
micRedBoost = effect("Vocalises rouges",'micRedBoost', stat=CHARISMA,turnInit=-1,trigger=TRIGGER_WEAPON_USE,unclearable=True,description="En attaquant avec votre arme principale, donne l'effet __Chanson rouge__ aux alliés dans la zone d'effet",area=AREA_DONUT_2,callOnTrigger=micRedBoostEff,emoji='<:redMic:936781924620451850>')
micRed = weapon("Micro rouge","df",RANGE_LONG,AREA_CIRCLE_5,53,75,300,charisma=20,precision=10,emoji='<:redMic:936781924620451850>',needRotate=False,use=CHARISMA,message="{0} pousse la chansonnette !",taille=0,effects=micRedBoost)
micPurpleBoostEff = effect("Chanson violette",'micPurpleBoostEff', stat=CHARISMA,magie=5,emoji='<:purpleMic:936781868127354900>')
micPurpleBoost = effect("Vocalises violettes",'micPurpleBoost', stat=CHARISMA,turnInit=-1,trigger=TRIGGER_WEAPON_USE,unclearable=True,description="En attaquant avec votre arme principale, donne l'effet __Chanson violette__ aux alliés dans la zone d'effet",area=AREA_DONUT_2,callOnTrigger=micPurpleBoostEff,emoji='<:purpleMic:936781868127354900>')
micPurple = weapon("Micro violet","dg",RANGE_LONG,AREA_CIRCLE_5,53,75,300,charisma=20,precision=10,emoji='<:purpleMic:936781868127354900>',needRotate=False,use=CHARISMA,message="{0} pousse la chansonnette !",taille=0,effects=micRedBoost)
explosher = weapon('Détoneur','dh',RANGE_LONG,AREA_CIRCLE_4,54,70,1,strength=35,precision=15,area=AREA_CIRCLE_1,emoji='<:explosher:936781519475855390>')
explosher2 = weapon('Détoneur Modifié','di',RANGE_LONG,AREA_CIRCLE_4,25,70,1,charisma=35,precision=15,area=AREA_CIRCLE_1,use=CHARISMA,type=TYPE_HEAL,target=ALLIES,emoji='<:healExplo:936784243424645160>')
trislosher = weapon("Dépoteur",'dj',RANGE_MELEE,AREA_CIRCLE_1,37,60,1,strength=15,endurance=15,agility=15,resistance=5,emoji='<:trislosher:936782121450741800>',area=AREA_CONE_2,repetition=2)

miltrilPlanisftEffBuff = copy.deepcopy(dmgUp)
miltrilPlanisftEffBuff.power, miltrilPlanisftEffBuff.stat, miltrilPlanisftEffBuff.turnInit = 3.5, INTELLIGENCE, 2
miltrilPlanisftEff = effect("Deck de cartes II","mitrilPlanisphereEff", stat=INTELLIGENCE,turnInit=-1,unclearable=True,emoji='<:deck:932400761176981605>',description="À chaque début de tour, augmente les dégâts infligés d'un allié",callOnTrigger=miltrilPlanisftEffBuff,trigger=TRIGGER_START_OF_TURN,area=AREA_RANDOMALLIE_1)
miltrilPlanisphere = weapon("Planisphère en mithril", 'dk', RANGE_LONG, AREA_CIRCLE_5, 35, 80, 1, area=AREA_CIRCLE_1, charisma=15, intelligence=15, effects=miltrilPlanisftEff, use=INTELLIGENCE, emoji='<:planisMitrill:938379244856291388>',priority=WEAPON_PRIORITY_LOW)

weapExpElemNames, tablWeapExp, weapExpElemEmojis = ["des flammes","des torrants","des tempettes","des roches","de la lueur","de l'ombre","dimensionnelle","temporelle"], [], ["<:fire:957763345681875015>","<:water:957763434030710824>","<:air:957763387566219265>","<:earth:957763463395049514>","<:light:957763573877211146>","<:darkness:957763497272414228>","<:space:957763551060189245>","<:time:957763517300240394>"]
for cmpt in range(8):
    tablWeapExp.append(effect("Maitrisse {0}".format(weapExpElemNames[cmpt]),"weaponElemMet",turnInit=-1,unclearable=True,description="Vous octroie **20%** de chance d'obtenir l'effet {0} __{1}__ en fin de tour.\nCette probabilité passe à **100%** si la dernière action réalisée pendant votre tour est une attaque à l'arme".format(tablElemEff[cmpt+1].emoji[0][0],tablElemEff[cmpt+1].name),emoji=weapExpElemEmojis[cmpt],callOnTrigger=tablElemEff[cmpt+1]))

fireMetRuneLong = weapon("Rune allongée des flammes","dl",RANGE_LONG,AREA_CIRCLE_6,41,60,1,magie=20,percing=10,area=AREA_CIRCLE_1,effects=tablWeapExp[0],use=MAGIE,emoji='<:fireLong:957759716484849754>',affinity=ELEMENT_FIRE,taille=0,priority=WEAPON_PRIORITY_HIGH)
fireMetRuneMel = weapon("Rune de proximité des flammes","dm",RANGE_MELEE,AREA_CIRCLE_2,60,60,1,magie=20,resistance=10,area=AREA_CIRCLE_1,effects=tablWeapExp[0],use=MAGIE,emoji='<:fireMele:957759749716336640>',affinity=ELEMENT_FIRE,taille=0,priority=WEAPON_PRIORITY_HIGH)
waterMetRuneLong = weapon("Rune allongée des courants","dn",RANGE_LONG,AREA_CIRCLE_6,60,60,1,magie=20,percing=10,effects=tablWeapExp[1],use=MAGIE,emoji='<:aqualong:957759791697125447>',affinity=ELEMENT_WATER,taille=0,priority=WEAPON_PRIORITY_HIGH)
waterMetRuneMel = weapon("Rune de proximité des courants","do",RANGE_MELEE,AREA_CIRCLE_2,86,60,1,magie=20,resistance=10,effects=tablWeapExp[1],use=MAGIE,emoji='<:aquaMel:957759818393870336>',affinity=ELEMENT_WATER,taille=0,priority=WEAPON_PRIORITY_HIGH)
airMetRuneMid = weapon("Rune étendue des vents","dp",RANGE_DIST,AREA_CIRCLE_4,50,60,1,magie=20,critical=10,area=AREA_CIRCLE_1,effects=tablWeapExp[2],use=MAGIE,emoji='<:airMid:957759962799562752>',affinity=ELEMENT_AIR,taille=0,priority=WEAPON_PRIORITY_HIGH)
airMetRuneMel = weapon("Rune de proximité des vents","dq",RANGE_MELEE,AREA_CIRCLE_2,60,60,1,magie=20,resistance=10,area=AREA_CIRCLE_1,effects=tablWeapExp[2],use=MAGIE,emoji='<:airMel:957759933359751239>',affinity=ELEMENT_AIR,taille=0,priority=WEAPON_PRIORITY_HIGH)
earthMetRuneMid = weapon("Rune étendue des sédiments","dr",RANGE_LONG,AREA_CIRCLE_4,73,60,1,magie=20,critical=10,effects=tablWeapExp[3],use=MAGIE,emoji='<:earthMid:957762288998305814>',affinity=ELEMENT_EARTH,taille=0,priority=WEAPON_PRIORITY_HIGH)
earthMetRuneMel = weapon("Rune de proximité des sédiments","ds",RANGE_MELEE,AREA_CIRCLE_2,86,60,1,magie=20,resistance=10,effects=tablWeapExp[3],use=MAGIE,emoji='<:earthMel:957759999227097118>',affinity=ELEMENT_EARTH,taille=0,priority=WEAPON_PRIORITY_HIGH)

lightMetRuneMid = weapon("Rune étendue des lueurs","dt",RANGE_DIST,AREA_CIRCLE_4,50,60,1,magie=20,percing=10,area=AREA_CIRCLE_1,effects=tablWeapExp[4],use=MAGIE,emoji='<:lightMid:957762377561014292>',affinity=ELEMENT_LIGHT,taille=0,priority=WEAPON_PRIORITY_HIGH)
lightMetRuneLong = weapon("Rune allongée des lueurs","du",RANGE_LONG,AREA_CIRCLE_6,41,60,1,magie=20,critical=10,area=AREA_CIRCLE_1,effects=tablWeapExp[4],use=MAGIE,emoji='<:lightLong:957762401963474994>',affinity=ELEMENT_LIGHT,taille=0,priority=WEAPON_PRIORITY_HIGH)
darkMetRuneMid = weapon("Rune étendue des ombres","dv",RANGE_DIST,AREA_CIRCLE_4,73,60,1,magie=20,critical=10,effects=tablWeapExp[5],use=MAGIE,emoji='<:darkMid:957762321709662339>',affinity=ELEMENT_DARKNESS,taille=0,priority=WEAPON_PRIORITY_HIGH)
darkMetRuneLong = weapon("Rune allongée des ombres","dw",RANGE_LONG,AREA_CIRCLE_6,60,60,1,magie=20,percing=10,effects=tablWeapExp[5],use=MAGIE,emoji='<:darkMel:957762348876169257>',affinity=ELEMENT_DARKNESS,taille=0,priority=WEAPON_PRIORITY_HIGH)
spaceMetRuneMid = weapon("Rune de proximité dimensionnelle","dx",RANGE_MELEE,AREA_CIRCLE_2,60,60,1,magie=20,resistance=10,area=AREA_CIRCLE_1,effects=tablWeapExp[6],use=MAGIE,emoji='<:spaceMel:957762429289369662>',affinity=ELEMENT_SPACE,taille=0,priority=WEAPON_PRIORITY_HIGH)
spaceMetRuneLong = weapon("Rune allongée dimensionnelle","dy",RANGE_LONG,AREA_CIRCLE_6,41,60,1,magie=20,percing=10,area=AREA_CIRCLE_1,effects=tablWeapExp[6],use=MAGIE,emoji='<:spaceLong:957762451515011112>',affinity=ELEMENT_SPACE,taille=0,priority=WEAPON_PRIORITY_HIGH)
timeMetRuneMid = weapon("Rune étendue temporelle","dz",RANGE_DIST,AREA_CIRCLE_4,73,60,1,magie=20,critical=10,effects=tablWeapExp[7],use=MAGIE,emoji='<:timeMid:957762503629226064>',affinity=ELEMENT_TIME,taille=0,priority=WEAPON_PRIORITY_HIGH)
timeMetRuneLong = weapon("Rune allongée temporelle","ea",RANGE_LONG,AREA_CIRCLE_6,60,60,1,magie=20,percing=10,effects=tablWeapExp[7],use=MAGIE,emoji='<:timeLong:957762475351244810>',affinity=ELEMENT_TIME,taille=0,priority=WEAPON_PRIORITY_HIGH)

iliSwoShield = weapon("Epée et Bouclier de la Lumière","eb",RANGE_MELEE,AREA_CIRCLE_1,69,75,1,resistance=10,charisma=20,effects=shieltron,use=CHARISMA,emoji='<:iliShield:975785889512976434>',affinity=ELEMENT_LIGHT)
flumShield = weapon("Epée et Bouclier de la Fleur Lumineuse","ec",RANGE_MELEE,AREA_CIRCLE_1,69,75,1,charisma=10,endurance=10,resistance=10,effects="lz",use=CHARISMA,affinity=ELEMENT_LIGHT,emoji='<:flumShield:964467183952465921>')
flumWand = weapon("Canne de la Fleur Lumineuse","ed",RANGE_LONG,AREA_CIRCLE_5,35,100,1,type=TYPE_HEAL,target=ALLIES,charisma=30,effects="lz",use=CHARISMA,affinity=ELEMENT_LIGHT,emoji='<:flumWand:964465128399568917>')
dflumShield = weapon("Epée et Bouclier de la Fleur Ténèbreuse","ef",RANGE_MELEE,AREA_CIRCLE_1,69,75,1,magie=20,resistance=10,effects="nt",use=MAGIE,affinity=ELEMENT_DARKNESS,emoji='<:darkShield:964467248486047765>')
dflumWand = weapon("Canne de la Fleur Ténèbreuse","eg",RANGE_LONG,AREA_CIRCLE_5,44,90,1,magie=25,precision=5,effects="nt",use=MAGIE,affinity=ELEMENT_DARKNESS,emoji='<:darkWand:964465066860761088>')
constShield = weapon("Bouclier Constitutionnel",'eh',RANGE_MELEE,AREA_CIRCLE_1,57,90,1,endurance=20,resistance=10,use=ENDURANCE,emoji='<:constShield:964463485968859137>',effects="mk")
aliceFan = weapon("Eventail","ei",RANGE_MELEE,AREA_CIRCLE_2,56,80,1,strength=20,charisma=20,endurance=10,area=AREA_ARC_1,emoji='<:aliceFan:986989072318861363>')
dSixtineWeap = weapon("Rapière Onirique","ej",RANGE_MELEE,AREA_CIRCLE_1,power=64,accuracy=70,price=1,area=AREA_LINE_2,magie=35,agility=10,resistance=5,emoji='<:dsixtRap:987009911097540710>',use=MAGIE)
phenixLeath = weapon("Plumes de Phénix","ek",RANGE_DIST,AREA_CIRCLE_4,46,65,1,magie=15,endurance=5,precision=10,effects=dtsword.effects,emoji='<:phenpl:992946043161411694>',area=AREA_CONE_2,use=MAGIE)
plume2 = copy.deepcopy(plume)
plume2.effectOnUse = plumRemEff
liaKatanaEff = effect("Akashi","liaKatanaEff",None,turnInit=-1,unclearable=True,emoji='<:liaCounter:998001563379437568>',counterOnDodge=15,description="Vous octroi **15%** de chance d'effectuer une **contre-attaque** en esquivant une attaque d'un adversaire se trouvant à 3 cases ou moins de vous",reject=["windDanceEff"])
liaKatana = weapon("Akashi","el",RANGE_MELEE,AREA_CIRCLE_1,34,50,repetition=3,effects=liaKatanaEff,agility=20,endurance=10,use=AGILITY,emoji='<:liaKat:998001500267749448>',price=1)
epiEff = effect("Armure","epiphyllumArmor", stat=INTELLIGENCE,overhealth=20,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
epiphyllum = weapon("Epiphyllum","em",RANGE_LONG,AREA_CIRCLE_5,power=15,type=TYPE_HEAL,effectOnUse=epiEff,area=AREA_CIRCLE_1,target=ALLIES,taille=0,emoji='<:flower:1014636465239629918>',accuracy=100,price=250,use=INTELLIGENCE,intelligence=30)
ascendance = effect("Ascendance","ascendance",unclearable=True,turnInit=-1,power=35,block=shieltron.block,description="Réduit les pertes de PV dues à l'utilisation des compétences Divines de **{0}%** et augmente votre taux de blocage",emoji='<:ascendance:1051510131105464370>')
sacredSword = weapon("Epée et Bouclier sacrés","en",RANGE_MELEE,AREA_CIRCLE_1,86,60,1,use=MAGIE,magie=20,resistance=10,effects=ascendance,emoji='<:sacredSword:1051510648359628811>')
triStringerEff = effect("Flèches exlosives","triStringerEff", stat=STRENGTH,power=35,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,description="Inflige des dégâts au porteur et vos ennemis alentours à la fin de son tour",area=AREA_CIRCLE_1)
triStringer = weapon("Tri-sperceur","eo",RANGE_LONG,AREA_CIRCLE_5,45,70,1,strength=10,intelligence=5,precision=5,percing=10,effectOnUse=triStringerEff,emoji='<:triStringer:1058334338065903669>')
kWeapEff = effect("Représailles","kWeapEff",block=15,counterOnBlock=20,turnInit=-1,description="Augmente votre probabilité de blocade ainsi que celle d'effectuer une contre attaque lors d'un blocage",emoji='<:represailles:1101242340523397191>')
kWeap = weapon("Pistolame Vangeresse",getAutoId("ep"),RANGE_MELEE,AREA_CIRCLE_1,64,75,1,strength=20,endurance=10,effects=kWeapEff,emoji='<:kGunblade:1100679173980291082>')
gWeap = weapon("Pistolame Justicière",getAutoId(kWeap.id),RANGE_MELEE,AREA_CIRCLE_1,64,75,1,intelligence=20,endurance=10,effects=eukrasia,emoji='<:gGunblade:1100679196436594759>',use=INTELLIGENCE)
aWeap = weapon("Pistolame Compatissante",getAutoId(gWeap.id),RANGE_MELEE,AREA_CIRCLE_1,64,75,1,charisma=20,endurance=10,effects=kardia,emoji='<:aGunblade:1100679222453862473>',use=CHARISMA)

dvinWandEff = effect("Ascendance","ascendance",unclearable=True,turnInit=-1,power=15,description="Réduit les pertes de PV dues à l'utilisation des compétences Divines de **{0}%**",emoji='<:ascendance:1051510131105464370>')
dvinWand = weapon("Canne Divine",getAutoId(aWeap.id),RANGE_LONG,AREA_CIRCLE_4,50,100,price=1,effects=dvinWandEff,type=TYPE_HEAL,charisma=30,emoji='<:dvinWand:1104505507978432583>',use=CHARISMA)
dvinSeptre = weapon("Sceptre Divin",getAutoId(dvinWand.id),RANGE_LONG,AREA_CIRCLE_4,37,85,price=1,effects=dvinWandEff,magie=25,precision=5,emoji='<:dvinSeptre:1104505536092840026>',use=MAGIE)
eclataDash = effect("Eclatadash","eclatadash", stat=PURCENTAGE,turnInit=-1,agility=5,unclearable=True,emoji='<:splatana:1129775771410505819>',dodge=5,description="Si vous attaquez votre cible avec votre arme sans être à son corps à corps, vous sautez devant de la cible. De plus, vos attaques à l'arme au corps à corps de la cible sont forcément critique\nAugmente aussi de **5%** votre probabilité d'esquive et votre agilité")
eclatana = weapon("Eclatana",getAutoId(dvinSeptre.id),RANGE_MELEE,AREA_CIRCLE_3,64,75,1,strength=20,agility=10,emoji='<:splatana:1129775771410505819>',effects=eclataDash,priority=WEAPON_PRIORITY_LOW)
eclatanaDoto = weapon("Eclatana Chic",getAutoId(eclatana.id),RANGE_MELEE,AREA_CIRCLE_3,64,75,1,magie=20,agility=10,emoji='<:splatanaDeco:1129775782798049360>',effects=eclataDash,use=MAGIE,priority=WEAPON_PRIORITY_LOW)
icealiaShieldEff = copy.deepcopy(defenseUp)
icealiaShieldEff.power, icealiaShieldEff.unclearable, icealiaShieldEff.turnInit, icealiaShieldEff.block = 5, -1, True, 20
icealiaShield = weapon("Bouclier Royal",getAutoId(eclatanaDoto.id),RANGE_MELEE,AREA_CIRCLE_1,60,80,1,use=INTELLIGENCE,endurance=20,resistance=10,effects=icealiaShieldEff,taille=0,priority=WEAPON_PRIORITY_LOWEST,emoji='<:royalInsing:1163510202713247904>')
heleneBrushEff = effect("Intégrité","heleneBrushEff", stat=CHARISMA,type=TYPE_INDIRECT_HEAL,turnInit=5,stackable=True,trigger=TRIGGER_HP_UNDER_25,power=35,emoji=sameSpeciesEmoji("<:integriteB:1131483104222126133>","<:integriteR:1131483136526663810>"),description="Soigne le porteur si ses PV tombent en dessous de **25%** de ses PV Max")
heleneBrush = weapon("Pinceau Magique",getAutoId(icealiaShield.id),RANGE_DIST,AREA_CIRCLE_4,35,100,1,use=CHARISMA,charisma=20,precision=10,effectOnUse=heleneBrushEff,type=TYPE_HEAL,target=ALLIES,emoji='<:heleneBrush:1131483975743971379>',taille=0)
elinaWeapEff = effect("Soins Intensifs","elinaWeapEff",power=20,turnInit=-1,unclearable=True,emoji='<:elinaWeapEff:1168213257031520326>',description="Augmente de **20%** les soins directs monocibles effectués mais diminue de **35%** les soins directs de zone")
elinaWeap = weapon("Seringue d'urgence",getAutoId(heleneBrush),RANGE_LONG,AREA_CIRCLE_5,40,100,1,type=TYPE_HEAL,use=CHARISMA,target=ALLIES,effects=elinaWeapEff,charisma=10,precision=20,emoji='<:elinaWeap:1168214196324925552>')
toxicureEff = effect("Toxicure","toxicureEff",type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_ON_REMOVE,emoji='<:toxiheart:1177648816774717482>',turnInit=1,lvl=1,area=AREA_LOWEST_HP_ALLIE)
toxicure = effect("Toxicure","toxicure",power=25,turnInit=-1,unclearable=True,silent=True,emoji="<:toxiCure:1177648759727980665>",callOnTrigger=toxicureEff,description="Lorsque vous infligez des dégâts ou vol de vie indirects, **{0}%** des dégâts ou des PVs restorés sont stockés. Au début de chaque tour, l'allié le plus blessé reçoit des soins équivalents à la quantité de dégâts ou PVs stoqués")
toxicBrush = weapon("Pinceau ToxiCo",getAutoId(elinaWeap),RANGE_DIST,AREA_CIRCLE_3,35,100,500,magie=20,intelligence=10,effects=toxicure,emoji='<:zenecaBrush:1177650683260969090>',use=MAGIE,type=TYPE_HEAL,target=ALLIES,priority=WEAPON_PRIORITY_NONE)

victoireShotgunEff = effect("Fusil à Pompe","victoireShotgunEff",turnInit=-1,unclearable=True,description="Vos attaques à l'arme au corps à corps infligent forcément un coup critique",emoji='<:shotgun:1227635614686380052>')
shotgun = weapon("Fusil à Pompe",getAutoId(toxicBrush),RANGE_MELEE,AREA_CIRCLE_2,75,60,1,strength=10,damageOnArmor=1.35,precision=10,endurance=10,effects=victoireShotgunEff,emoji='<:shotgun:1227635614686380052>')
enchantedShotgunEff = copy.deepcopy(victoireShotgunEff)
enchantedShotgunEff.name, enchantedShotgunEff.emoji = "Fusil à Pompe Enchanté", uniqueEmoji("<:enchantedShotgun:1227635638136864890>")
enchantedShotgun = weapon("Fusil à Pompe Enchanté",getAutoId(shotgun),RANGE_MELEE,AREA_CIRCLE_2,75,60,1,strength=10,damageOnArmor=1.35,precision=10,endurance=10,effects=enchantedShotgunEff,use=MAGIE,emoji='<:enchantedShotgun:1227635638136864890>')
ailillPassiveEff = effect("Acharnement","aillilPassiv",power=15,emoji=deepWound.emoji,turnInit=-1,unclearable=True,callOnTrigger=deepWound,description="Lors de vos attaques directs, **15%** des dégâts infligés sont également infligés en tant que Blessure Profonde")
chainsaw = weapon("Tronçonneuse",getAutoId(enchantedShotgun),RANGE_MELEE,AREA_CIRCLE_1,80,75,1,strength=15,precision=10,endurance=5,effects=ailillPassiveEff,emoji='<:chainsaw:1189299410794979479>')

# Weapon
weapons = [chainsaw,shotgun,enchantedShotgun,toxicBrush,elinaWeap,heleneBrush,icealiaShield,eclatana,eclatanaDoto,dvinWand,dvinSeptre,gWeap,aWeap,kWeap,triStringer,dSixtineWeap,phenixLeath,liaKatana,epiphyllum,sacredSword,
    iliSwoShield,flumShield,flumWand,dflumShield,dflumWand,constShield,aliceFan,
    fireMetRuneLong,fireMetRuneMel,waterMetRuneLong,waterMetRuneMel,airMetRuneMid,airMetRuneMel,earthMetRuneMid,earthMetRuneMel,lightMetRuneMid,lightMetRuneLong,darkMetRuneMid,darkMetRuneLong,spaceMetRuneMid,spaceMetRuneLong,timeMetRuneLong,timeMetRuneMid,
    magicWood,magicMass,magicSwordnShield,keyblade,fleau,micPurple,micRed,explosher,explosher2,trislosher,miltrilPlanisphere,
    secretum,ElitherScope,grav,darkbluebutterfly,bleuSpiritWings,whiteSpiritWings,infDarkSword,infLightSword,astroGlobe,
    eternalInkSword,eternalInkStick,eternalInkShield,eternalInkStaff,eternalInkWind,eternalInkScience,eternalInkBow,
    julieWeap,blueButterfly,butterflyRed,luth,krystalFist,musical,gwenCoupe,inkbrella2,concentraceurZoom,klikliSword,darkSpellBook,lightSpellBook,ironSword,machinist,shehisa,armilame,airsword,waterspell,earthspell,airspell,nemefaux,bigshot,serringue,fauc,rapiere,lunarBonk,magicSword,dtsword,butterflyP,butterflyR,depha,legendarySword,spellBook,micPink,butterfly,dualJetSkelcher,squiffer,flexi,splatling,dualies,clashBlaster,hourglass1Weap,plume,splattershot,roller,splatcharger,miniBrush,inkbrella,blaster,jetSkelcher,kcharger,HunterRiffle,firework
]+baseWeapon

# Can't use weapon
cannotUseMainWeapon = []

# Find Weapon
def findWeapon(WeaponId) -> weapon:
    typi = type(WeaponId)
    if typi == weapon:
        return WeaponId

    elif type(WeaponId) != str:
        return None
    else:
        rep,id = None,WeaponId

        if WeaponId.startswith("\n"):
            id = id.replace("\n","")
        for a in weapons:
            if a.id == id or a.name.lower() == id.lower():
                rep = a
                break
        return rep

akiaPreWeapon = [klikliSword,splatcharger,dualies,micPink,bleuSpiritWings,clashBlaster,magicWood,explosher2,magicSwordnShield,inkbrella2,constShield,dflumWand,luth,HunterRiffle]
