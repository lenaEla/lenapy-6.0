from operator import neg
from classes import *
from constantes import *

uniform = stuff("Uniforme Scolaire","hd",1,100,intelligence=5,magie=5,charisma=10,emoji='<:uniform:866830066008981534>',orientation=[None,BOOSTER],affinity=ELEMENT_WATER)
blueSnekers = stuff("Tennis Montantes Bleues","he",2,100,agility=10,endurance=5,charisma=5,emoji='<:blueHotTop:866795241721954314>')
redSnekers = stuff("Tennis Montantes Rouge","hg",2,100,strength=10,endurance=5,resistance=5,emoji='<:redHopTop:866782609464098887>')
encrifuge = stuff("Tenue Encrifugée","hh",1,350,endurance=20,resistance=15,charisma=-10,intelligence=-15,effect="ni",emoji='<:encrifuge:871878276061212762>',orientation=[TANK])
pinkFlat = stuff("Ballerines roses","hi",2,150,charisma=20,emoji='<:pinkFlat:867158156139692042>',orientation=[DISTANCE,HEALER])
blackFlat = stuff("Ballerines noires","hj",2,150,strength=5,endurance=5,charisma=10,resistance=10,agility=-10,emoji="<:blackflat:867175685768347688>",orientation=[TANK,HEALER])
batEarRings = stuff("Clous d'oreilles chauve-souris","hk",0,150,charisma=10,percing=10,emoji="<:batearrings:867159399395098634>",orientation=[DISTANCE,DPT],position=1,affinity=ELEMENT_NEUTRAL)
ironHelmet = stuff("Casque en fer","hl",0,200,endurance=10,resistance=10,emoji="<:helmet:867158650488225792>",orientation=[TANK])
determination = stuff("Détermination","hm",0,500,strength=35,endurance=20,resistance=20,negativeIndirect=50,negativeBoost=15,effect="lg",emoji='<:determination:867894180851482644>',position=2,affinity=ELEMENT_NEUTRAL)
pinkDress = stuff("Robe rose","ho",1,200,charisma=15,agility=10,strength=-5,emoji='<:pinkDress:867533070940766228>',orientation=[DISTANCE,HEALER])
oldBooks = stuff("Vieux livres","hp",0,200,intelligence=15,magie=10,agility=-15,strength=10,emoji='<:oldbooks:867533718485598208>',orientation=[DISTANCE,BOOSTER])
jeanJacket = stuff("Veste en jean","hq",1,150,5,5,5,5,emoji='<:jeanjacket:867813124697620510>',affinity=ELEMENT_NEUTRAL)
blackJeanJacket = stuff("Veste en jean noire","hr",1,150,10,10,-5,magie=-5,percing=10,emoji='<:blackjacket:867542491666579467>',orientation=[None,DPT],affinity=ELEMENT_EARTH)
whiteSneakers = stuff("Baskets Blanches","hs",2,100,agility=10,magie=10,emoji='<:whiteSneakers:867543508496023592>',orientation=[None,BOOSTER])
amethystEarRings = stuff("Boucles d'oreilles en améthyste","hw",0,200,strength=45,endurance=10,negativeDirect=-15,precision=30,percing=10,resistance=-10,negativeBoost=35,negativeHeal=35,critical=-10,emoji='<:amethystEarRings:870391874081419345>',position=1,orientation=[LONG_DIST,DPT])
anakiMask = stuff("Masque Annaki","hx",0,150,endurance=10,charisma=5,precision=10,resistance=-5,emoji='<:anakiMask:870806374009954345>',position=5)
whiteBoots = stuff("Bottines Blanches","hy",2,200,endurance=10,agility=10,resistance=5,strength=-5,emoji='<:bottinesPunkBlanche:870807353044393994>',orientation=[TANK])
mustangBoots = stuff("Bottines à lacets","hz",2,150,strength=5,agility=5,charisma=5,precision=5,emoji='<:mustangboots:870808390081851423>')
pullBrown = stuff("Pull Brun","ia",1,200,10,agility=10,resistance=5,percing=5,charisma=-10,emoji='<:pullMaron:871878275922800681>')
blackShirt = stuff("T-Shirt Noir","ib",1,50,precision=10,resistance=5,magie=5,emoji='<:tshirtNoir:871878276103159848>')
pullCamo = stuff("Pull Camouflage","ic",1,150,agility=20,resistance=10,percing=10,precision=-5,critical=-5,endurance=-10,emoji='<:pullCam:871878276090593321>',orientation=[TANK,DPT])
woodenSandals = stuff("Sandales en bois","ie",2,200,10,agility=10,resistance=5,endurance=-5,emoji="<:sandaleBois:871880746070056991>")
schoolShoes = stuff("Mocassins Scolaires","if",2,100,charisma=5,intelligence=5,magie=5,resistance=5,emoji='<:schoolShoe:871880746426593331>',orientation=[None,BOOSTER])
blackSnelers = stuff("Tennis Montantes Noires","ig",2,100,5,endurance=5,resistance=10,emoji='<:BlackHotTop:871880746422394970>',orientation=[TANK,DPT])
heartLocket = stuff("Heart Locket","ih",0,300,resistance=20,emoji='<:heartLocket:871886518753570836>',orientation=[TANK],position=2)
catEars = stuff("Oreilles de chat","ii",0,150,charisma=10,agility=10,emoji='<:catEars:871886070025957388>',orientation=[None,HEALER],affinity=ELEMENT_AIR)
batPendant = stuff("Pendantif Chauve-Souris","ij",0,200,5,5,magie=10,emoji='<:batPendant:871887272469995560>',position=2)
bikini = stuff("Tenue Provocante","ik",1,69,endurance=-15,charisma=40,resistance=-10,percing=5,emoji='<:tenueProvoquante:871889591127388201>',orientation=[LONG_DIST,HEALER])
headSG = stuff("Chapeau Squid Girl","il",0,200,strength=5,agility=10,precision=10,endurance=-5,emoji='<:headSG:874266872340680785>',orientation=[DISTANCE,DPT])
bodySG = stuff("Tunique Squid Girl","im",1,200,10,resistance=10,emoji="<:tuniqueSG:874266874299437126>",orientation=[DISTANCE,DPT])
shoeSG = stuff("Chaussures Squid Girl","in",2,200,5,agility=10,critical=5,emoji="<:shoeSG:874266873099857930>",orientation=[DISTANCE,DPT])
flum = stuff("Fleur lumineuse","io",0,150,charisma=10,effect="lz",emoji='<:flum:876079513954557952>',orientation=[None,HEALER],position=3,affinity=ELEMENT_LIGHT)
pinkShirt = stuff("Veste et jupe rose","ip",1,300,-20,charisma=25,agility=10,critical=5,emoji='<:VesteEtJupeRose:877658944045219871>',orientation=[None,HEALER])
redDress = stuff("Robe rouge et noire","iq",1,300,20,endurance=-10,percing=5,critical=5,emoji='<:gothicRednBlackDress:877665554033414217>',orientation=[DISTANCE,DPT])
pataarmor = stuff("Armure patapoulpe","ir",1,300,-10,20,-5,resistance=15,emoji='<:octoArmor:876783724237303829>',orientation=[TANK])
barrette = stuff("Barette Seiche","is",0,100,charisma=10,precision=10,emoji='<:squidBar:878718467434491934>',position=3)
squidEarRings = stuff("Boucles d'oreilles Seiche","it",0,150,charisma=15,intelligence=10,precision=-5,emoji='<:squidEarRings:878718445171126313>',orientation=[None,BOOSTER],position=1,affinity=ELEMENT_NEUTRAL)
maidDress = stuff("Robe de soubrette","iu",1,300,-10,25,20,agility=-10,resistance=15,negativeHeal=-10,negativeBoost=30,emoji='<:maidDress:878716791789080637>',orientation=[TANK,HEALER])
maidHeels = stuff("Escarpins de soubrette","iv",2,300,charisma=30,endurance=20,agility=-20,resistance=10,negativeHeal=-10,negativeShield=30,emoji='<:maidHeels:878716728346050600>',orientation=[TANK,HEALER])
maidHat = stuff("Coiffe de soubrette","iw",0,200,charisma=25,endurance=20,resistance=10,negativeHeal=-10,strength=-20,precision=-25,emoji='<:maidHat:878716744305356812>',orientation=[TANK,HEALER])
pinkRuban = stuff("Ruban Rose","ix",0,100,charisma=20,emoji='<:pinkRuban:878718698469335060>',orientation=[DISTANCE,HEALER],position=3)
pinkSneakers = stuff("Tennis Montantes Roses","iy",2,300,charisma=20,agility=10,intelligence=10,endurance=-10,precision=-10,emoji='<:PinkHotTop:877664496737472602>',orientation=[DISTANCE,HEALER])
abobination = stuff("Claquettes chaussettes","iz",2,1,1,1,-100,1,1,1,1,1,1,1,'<:claquetteChaussette:871880745998770258>')
legendaryTunic = stuff("Tunique de Légende","ja",1,300,15,10,resistance=10,precision=-10,agility=-5,emoji='<:LegendaryTunic:880008983618912277>',orientation=[TANK,DPT],affinity=ELEMENT_LIGHT)
legendaryBoots = stuff("Bottes de Légende","jb",2,300,endurance=10,resistance=10,strength=5,agility=-5,emoji='<:LegendaryBoots:880008962852917313>',orientation=[TANK,DPT])
purpleBasket = stuff("Baskets Violettes","jc",2,50,10,10,emoji='<:BasketViolette:871880746535620618>',orientation=[TANK,DPT])
camoHat = stuff("Casquette Camouflage","jd",0,50,15,precision=25,resistance=-10,magie=-10,emoji='<:camohat:878721916570058754>',orientation=[LONG_DIST,DPT])
blueFlat = stuff("Ballerines Blues","je",2,100,magie=25,resistance=-5,emoji='<:blueflat:881209954902638602>',orientation=[DISTANCE,MAGIC])
redFlat = stuff("Ballerines Rouges","jf",2,100,20,resistance=-5,percing=5,emoji='<:redflat:881209970568364173>',orientation=[DISTANCE,DPT])
redHeels = stuff("Escarpins Rouges","jg",2,150,strength=20,resistance=-10,percing=10,emoji='<:heelsRed:881339121795215410>',orientation=[DISTANCE,DPT])
whiteHeels = stuff("Escarpins Blancs","jh",2,150,charisma=15,intelligence=15,resistance=-10,emoji='<:heelsWhite:881339137410609162>',orientation=[DISTANCE,BOOSTER])
blackHeels = stuff("Escarpins Noirs","ji",2,150,10,percing=10,endurance=10,resistance=10,agility=-20,emoji='<:heelsBlack:881339167357935616>',orientation=[TANK,DPT])
heroHead = stuff("Casque Héroïque","jj",0,250,20,-10,percing=10,emoji='<:heroicheadset:881326928802496562>',orientation=[DISTANCE,DPT])
heroBody = stuff("Veste Héroïque","jk",1,250,10,10,precision=10,magie=-10,emoji='<:herojacket:881326964328255508>',orientation=[DISTANCE,DPT])
heroShoe = stuff("Baskets Héroïques","jl",2,250,strength=10,critical=5,percing=5,emoji='<:heroshoe:881326998511833098>',orientation=[DISTANCE,DPT])
intemCharpe = stuff("Echarpe Intemporelle","jm",0,250,charisma=25,negativeHeal=-35,negativeBoost=-20,negativeShield=40,resistance=-10,endurance=-10,emoji='<:intemcharpe:882006603350568960>',orientation=[None,HEALER],position=2,affinity=ELEMENT_TIME)
intemNorak = stuff("Veste Intemporelle","jn",1,250,charisma=30,negativeHeal=-30,negativeShield=30,strength=-5,percing=-5,emoji='<:intemnorak:882006589870075944>',orientation=[DISTANCE,HEALER],affinity=ELEMENT_TIME)
intemShoe = stuff("Tennis Montantes Intemporelles","jo",2,250,charisma=30,negativeHeal=-30,negativeShield=25,percing=-15,emoji='<:intemtennis:882006616961073253>',orientation=[DISTANCE,HEALER],affinity=ELEMENT_TIME)
patacasque = stuff("Casque Patapoutre","jp",0,200,resistance=10,endurance=10,orientation=[TANK,None],emoji='<:patacasque:881334720732991529>')
patabottes = stuff("Bottes Patapoutres","jq",2,200,resistance=15,endurance=5,orientation=[TANK,None],emoji='<:pataboots:881334739183730689>')
lunettesOv = stuff("Lunettes ovales","jr",0,100,strength=10,precision=10,emoji='<:lunettesovales:881965054830997534>',orientation=[None,DPT])
masqueTub = stuff("Masque et tuba","js",0,100,resistance=10,precision=10,emoji='<:masqieTubas:881965193100406785>',orientation=[TANK,None])
casqueColor = stuff("Casque coloré","jt",0,150,charisma=15,intelligence=15,agility=-5,precision=-5,emoji="<:colorheadset:881326908149727253>",orientation=[None,BOOSTER])
blingbling = stuff("Lunettes 18 karas","ju",0,100,5,5,5,5,-5,-5,5,5,emoji='<:lunettes18kara:881965006483251263>')
legendaryHat = stuff("Exelo","jw",0,300,endurance=10,resistance=5,strength=10,agility=-5,emoji='<:excelot:882727033782812702>',orientation=[TANK,DPT])
robeDrac = stuff("Robe draconique","jv",1,250,strength=-30,endurance=15,intelligence=20,resistance=15,emoji='<:robedraco:878572815807287297>',orientation=[TANK,DPT])
robeLoliBlue = stuff("Robe Lolita Bleue","jx",1,300,-10,0,10,0,0,0,40,negativeDirect=20,emoji="<:blueLolita:884212751881363467>",orientation=[DISTANCE,MAGIC])
old = stuff("Vieux porte-clefs","jy",0,200,magie=35,negativeDirect=15,emoji='<:old:885086171754012702>',affinity=ELEMENT_WATER,position=4)
batRuban = stuff("Noeud Chauve-Souris","jz",0,0,charisma=30,intelligence=30,strength=-20,negativeBoost=-30,resistance=-10,percing=-10,negativeHeal=20,endurance=-10,orientation=[LONG_DIST,HEALER],emoji='<:batRuban:887328511222763593>',position=3)
FIACNf = stuff("Robe du FIACN","ka",1,0,40,10,resistance=15,agility=-20,precision=-15,magie=-10,emoji='<:FIACNF:887328531774836736>',orientation=[TANK,DPT])
FIACNh = stuff("Gilet du FIACN","kb",1,0,40,10,resistance=15,agility=-20,precision=-15,magie=-10,emoji='<:FIACNH:887328549437059172>',orientation=[TANK,DPT])
heleneDress = stuff("Robe bleue d'Hélène","kc",1,0,charisma=25,intelligence=20,strength=-20,endurance=-15,emoji='<:heleneDress:888745359365525535>',effect='mk',affinity=ELEMENT_LIGHT,orientation=[DISTANCE,HEALER])
heleneShoe = stuff("Babies bleues d'Hélène","kd",2,0,strength=-10,charisma=25,intelligence=5,emoji='<:blueBabie:887857026477207592>',orientation=[DISTANCE,HEALER])
corset = stuff("Corset d'Ordin","ke",1,500,10,0,-5,0,25,-10,emoji="<:corsetordin:887757308157886465>",orientation=[DISTANCE,None])
ggshield = stuff("Bouclier GG","kf",0,500,endurance=20,resistance=15,agility=-15,emoji='<:emoji_8:887757446658023496>',orientation=[TANK,None],position=4)
fecaShield = stuff("Bouclier Feca","kg",0,1000,-15,15,resistance=20,emoji='<:fecashield:887757399736348722>',affinity=ELEMENT_EARTH,orientation=[TANK,None],position=4)
kanisand = stuff("Sandales Kannivore","kh",2,250,agility=20,emoji="<:sandaleskannivores:887755801161240577>",affinity=ELEMENT_AIR)
tsarine = stuff("Starine","ki",0,500,resistance=15,intelligence=10,endurance=10,precision=-15,charisma=-10,effect="mk",emoji='<:tsarine:887755891913396245>',orientation=[TANK,None])
dracBoot = stuff("Bottes Draconiques","kj",2,500,-10,20,resistance=10,intelligence=10,agility=-10,emoji='<:bottesdraco:885080377234968608>',orientation=[TANK,None])
darkMaidFlats = stuff("Ballerines de soubrette des Ténèbres","kk",2,500,25,10,agility=25,resistance=10,charisma=-20,precision=-10,magie=-20,emoji='<:linaflats:890598400624586763>',orientation=[TANK,DPT],affinity=ELEMENT_DARKNESS)
darkMaidDress = stuff("Robe de soubrette des Ténèbres","kl",1,500,25,10,agility=25,resistance=15,precision=-10,charisma=-20,magie=-25,emoji="<:linadress:890598423152185364>",orientation=[TANK,DPT],affinity=ELEMENT_DARKNESS)
darkMaidPendants = stuff("Boucles d'oreilles de soubrette des Ténèbres","km",0,500,15,20,-10,15,-10,-20,resistance=10,emoji='<:linapendant:890599104902754326>',orientation=[TANK,DPT],affinity=ELEMENT_DARKNESS,position=1)
darkbabie = stuff("Babies noires","kn",2,250,20,-20,precision=20,emoji='<:bbabies:892351703230320670>',affinity=ELEMENT_DARKNESS,orientation=[DISTANCE,DPT])
krysCorn = stuff("Serre-Tête en KrysTal","ko",0,250,endurance=15,resistance=10,agility=-5,emoji='<:krysCorn:892350678620586004>',affinity=ELEMENT_EARTH)
shihuDress = stuff("Robe de matelot noire d'encre","kp",1,750,-10,0,magie=45,negativeDirect=-15,negativeIndirect=30,emoji='<:shihudress:896916995948302336>',orientation=[DISTANCE,MAGIC])
shihuShoe = stuff("Babies noire d'encre","kq",2,750,-10,magie=35,critical=5,negativeIndirect=30,negativeDirect=-20,emoji='<:shihubabies:896914810225188895>',orientation=[DISTANCE,MAGIC])
mageDress = stuff("Coule du mage noir","kr",1,500,-20,agility=10,precision=10,magie=25,resistance=-5,emoji='<:bmage:896912954744795177>',orientation=[LONG_DIST,MAGIC])
mageShoe = stuff("Bottines de mage noir",'ks',2,500,-10,endurance=-10,magie=25,precision=15,emoji='<:bmageshoe:896913235884802090>',orientation=[LONG_DIST,MAGIC])
tankmage1 = stuff("Armure du mage de combat",'kt',1,500,-30,20,resistance=10,magie=20,emoji='<:battlemagedress:898203453824852029>',orientation=[TANK,MAGIC])
tankmage2 = stuff("Bottes du mage de combat",'ku',2,500,charisma=-20,agility=20,resistance=15,magie=15,intelligence=-10,emoji='<:battlemageboot:898203467800277032>',orientation=[TANK,MAGIC])
tankmage3 = stuff("Chapeau du mage de combat",'kv',0,500,-20,20,resistance=10,magie=10,emoji='<:battlemagehat:899698677059305482>',orientation=[TANK,MAGIC])
shihuHat = stuff("Beret de matelot noir d'encre",'kw',0,750,magie=35,negativeIndirect=35,negativeDirect=-20,emoji='<:shihuhat:898231015384944640>',orientation=[DISTANCE,MAGIC])
indeci1 = stuff("Fleur du mage indécis",'kx',0,750,strength=15,magie=15,intelligence=-5,charisma=-5,emoji='<:rmhat:898206952952332299>',position=barrette.position)
indeci2 = stuff("Veste du mage indécis",'ky',1,750,strength=15,magie=15,precision=-5,agility=-5,emoji='<:rmjakect:897631127760691240>')
indeci3 = stuff("Bottes du mage indécis",'k7',2,750,strength=15,magie=15,charisma=-5,agility=-5,emoji='<:rmboots:897631140557516840>')
hyperlink = stuff("[[Hyperlink blocked]]",'kz',2,1997,35,intelligence=30,endurance=15,charisma=-30,magie=-30,emoji='<:blocked:897631107602841600>')
heartSphapeObject = stuff("[[Heart Shaped Object](https://deltarune.fandom.com/wiki/SOUL)]","la",1,1997,20,20,-20,0,0,20,-20,20,critical=-20,emoji=determination.emoji,affinity=ELEMENT_TIME)
vigilant1 = stuff("Echarpe Temporelle","lb",0,500,intelligence=35,charisma=-15,negativeShield=-25,resistance=-10,endurance=-15,orientation=[None,BOOSTER],emoji='<:tempoCharpe:900148919248502894>',position=intemCharpe.position,affinity=ELEMENT_TIME)
vigilant2 = stuff("Veste Temporelle","lc",1,500,intelligence=35,resistance=-10,negativeBoost=5,negativeShield=-35,endurance=-15,negativeHeal=20,orientation=[None,BOOSTER],emoji='<:tempoVeste:900148936088625152>',affinity=ELEMENT_TIME)
vigilant3 = stuff("Tennis Montantes Temporelles","ld",2,500,intelligence=35,negativeShield=-25,magie=-25,negativeHeal=15,orientation=[None,BOOSTER],emoji='<:tempoBoots:900148968808402997>')
vigilant4 = stuff("Heaume du vigilant","le",0,750,strength=-10,endurance=30,intelligence=20,magie=-20,resistance=15,charisma=-15,orientation=[TANK,BOOSTER],emoji='<:prevHead:904171171300384838>')
vigilant5 = stuff("Armure du vigilant","lf",1,750,strength=-30,endurance=20,intelligence=20,magie=-15,resistance=25,orientation=[TANK,BOOSTER],emoji='<:prevArmor:904171199108628492>')
vigilant6 = stuff("Soleret du vigilant","lp",2,750,strength=-15,endurance=30,intelligence=20,magie=-15,resistance=15,charisma=-15,orientation=[TANK,BOOSTER],emoji='<:prevShoe:904171185191915590>')
lunetteDeVisee = stuff("Lunette de visée","lg",0,500,strength=25,precision=25,resistance=-10,endurance=-20,orientation=[LONG_DIST,DPT],emoji='<:emoji_47:905277620055330846>',position=fecaShield.position)
magicHeal1 = stuff("Broche du mage blanc","lh",0,500,strength=-15,charisma=30,magie=20,intelligence=-15,affinity=ELEMENT_LIGHT,position=barrette.position,emoji='<:whiteMage:912915963110916097>')
magicHeal2 = stuff("Robe du mage blanc","li",1,500,endurance=-15,charisma=35,magie=25,resistance=-10,precision=-15,affinity=ELEMENT_LIGHT,orientation=[LONG_DIST,None])
magicHeal3 = stuff("Souliers du mage blanc","lj",2,500,strength=-15,charisma=30,magie=20,intelligence=-15,affinity=ELEMENT_LIGHT)
shehisaBody = stuff("Tenue de la tiseuse","lk",1,500,strength=35,endurance=10,resistance=10,magie=-20,critical=-5,negativeDirect=10,orientation=[TANK,DPT])
shehisaBoots = stuff("Bottes de la tiseuse","ll",2,500,strength=45,resistance=5,agility=10,critical=-10,magie=-10,negativeDirect=20)
shehisaMask = stuff("Masque de la tiseuse","lo",0,500,strength=35,intelligence=10,resistance=5,agility=-10,magie=-10,emoji='<:shiMask:901850537132171334>',negativeDirect=10,position=barrette.position)
# LP alreay taken
darkFlum = stuff("Fleur ténèbreuse","lm",0,150,magie=10,effect="nt",emoji='<:darkFlum:901849622685814814>',orientation=[None,MAGIC],position=3,affinity=ELEMENT_DARKNESS)
hockey = stuff("Masque de hockey","ln",0,250,strength=30,magie=-10,charisma=-10,percing=10,emoji='<:hockeymask:881326947597164564>',orientation=[None,DPT],position=3)
laurier = stuff("Lauriers","lq",0,650,charisma=20,strength=20,magie=-10,intelligence=-10,emoji='<:laurier:887755867271888898>')
lentille = stuff("Lentilles sans corrections","lr",0,350,intelligence=20,magie=20,emoji='<:lentilles:881965103438770176>',negativeIndirect=20)
kaviboots = stuff("Bottes Kannivore","ls",2,350,strength=20,agility=25,endurance=15,resistance=15,magie=-30,intelligence=-25,emoji='<:bottinscanivore:887755841535639562>')
purpleGlass = stuff("Monture Violette","lt",0,350,magie=20,emoji='<:monturesViolettes:881965147990663188>')
legolass = stuff("Les Lego'Lasses","lu",2,350,precision=20,strength=20,endurance=-20,emoji='<:legolasse:887755747683889234>',orientation=[DISTANCE,None])
aliceDress = stuff("Robe de scène","lv",1,1,charisma=60,intelligence=30,negativeHeal=30,negativeDirect=20,negativeShield=20,emoji='<:aliceDress:902282155474964540>',orientation="Distance - Idole")
yellowpull = stuff("Pull Jaune","lw",1,1,endurance=20,charisma=40,intelligence=20,resistance=20,strength=-30,magie=-30,negativeDirect=10,negativeIndirect=10,emoji='<:yellowPull:903595209802272798>')
blackGhoticDress = stuff("Robe Gothique Noire",'lx',1,1,magie=40,resistance=-20,negativeDirect=20,negativeIndirect=-20,emoji='<:emoji_33:903616825810636830>')
aliceShoes = stuff("Chaussures de scène","ly",2,1,charisma=30,intelligence=30,endurance=5,strength=-5,negativeBoost=-20,negativeHeal=30,negativeShield=30,emoji='<:aliceShoe:904164849708331098>')
lightBlueFlats = stuff("Ballerines azurées","lz",2,1,strength=35,precision=35,negativeIndirect=70,negativeDirect=-45,agility=-25,orientation=[LONG_DIST,DPT],emoji='<:lbflats:905047434462396446>')
rangers = copy.deepcopy(lightBlueFlats)
rangers.name, rangers.id, rangers.emoji = "Rangers Octaling","ma","<:octoRangers:905048480861548544>"
lightBlueJacket = stuff("Veste Azurée","mb",1,1,strength=30,precision=30,endurance=10,negativeDirect=-45,negativeIndirect=75,agility=-20,orientation=[LONG_DIST,DPT],emoji='<:lbjacket:905047464820752404>')
encrifugeBoots = stuff("Bottes encrifugées","mc",2,350,endurance=25,resistance=15,negativeDirect=10,negativeIndirect=10,emoji='<:armoredBoots:905048503275892766>')

jeanCas = stuff("Casquette en jean","md",0,1,magie=10,negativeDirect=-10,emoji='<:CascJean:907386971276587018>')
pullPol = stuff("Pull polaire","me",1,1,endurance=20,charisma=20,negativeShield=20,emoji='<:NHChandail_neige1:907386973294047312>',orientation=[TANK,HEALER])
heartBask = stuff("Paire de baskets à coeur","mf",2,1,charisma=20,intelligence=30,negativeBoost=-30,critical=-20,negativeHeal=20,negativeDirect=20,emoji='<:NHPaire_de_baskets_c3Fur0:907386973260505109>')
mocas = stuff("Paire de mocassins","mg",2,1,strength=10,magie=10,emoji='<:NHPaire_de_mocassins1:907386974246174790>')
sandPlage = stuff("Paire de sandales de plages","mh",2,1,endurance=15,magie=15,resistance=10,strength=-10,intelligence=-10,emoji='<:NHPaire_sandalettes_de_plage1:907386973277282334>',orientation=[TANK,MAGIC])
pullHeart = stuff("Pull coeur","mi",1,1,charisma=20,intelligence=30,negativeBoost=-30,percing=-20,negativeDirect=20,negativeHeal=20,emoji='<:NHPull_c3Fur0:907386973629595729>',orientation=[None,BOOSTER])
pullJoliReve = stuff("Pull joli rêve","mj",1,1,endurance=10,agility=10,emoji='<:NHPull_joli_r3Fve1:907386973839319141>')
surveste = stuff("Surveste",'mk',1,1,precision=10,strength=10,emoji='<:NHSurveste0:907386974409732136>')
tshirMatelot = stuff("T-shirt matelot",'ml',1,1,magie=20,resistance=15,endurance=10,precision=-10,critical=-5,strength=-10,emoji='<:NHTshirt_matelot2:907386972983664661>',orientation=[TANK,MAGIC])
tshirtNoue = stuff("T-shirt noué",'mm',1,1,strength=15,resistance=10,endurance=10,magie=-15,emoji='<:NHTshirt_nou3F_devant0:907386974363615262>',orientation=[TANK,DPT])
tshirtSport = stuff("T-shirt de sport",'mn',1,1,agility=20,emoji='<:NHTshirt_sport1:907386974434893855>')
motarVeste = stuff("Veste de motard","mo",1,1,strength=25,endurance=10,resistance=10,magie=-15,agility=-10,emoji='<:NHVeste_de_motard0:907386974543945728>',orientation=[TANK,DPT])
babiesRose = stuff("Babies à ruban roses","mp",2,1,charisma=10,intelligence=10,negativeHeal=-20,negativeBoost=20,emoji='<:babieRubR:907386970966196254>',orientation=[None,HEALER])
babiesVert = stuff("Babies verts","mq",2,1,agility=15,precision=15,negativeDirect=10,emoji='<:babiesV:907386972455198750>')
carid = stuff("Casdigan","mr",1,1,endurance=10,critical=10,emoji='<:cardigan:907386965232586772>')
chemLB = stuff("Chemise azurée","ms",1,1,strength=15,precision=15,agility=-10,emoji='<:chemB:907386970668425216>')
chemV = stuff("Chemise verte","mt",1,1,strength=15,agility=15,magie=-10,emoji='<:chemCrant:907386970894893096>')
chemB = stuff("Chemise bleue","mu",1,1,magie=25,resistance=-5,emoji='<:chemFlan:907386970827788368>')
chemN = stuff("Chemise noire","mv",1,1,strength=25,endurance=20,resistance=15,agility=-20,negativeIndirect=20,emoji='<:chemN:907386972161572896>',orientation=[TANK,DPT])
chemR = stuff("Chemise rose",'mw',1,1,negativeHeal=-30,negativeDirect=10,emoji='<:chemR:907386968046985226>',orientation=[None,HEALER])

coiffeInfirmR = stuff("Coiffe d'infirmier rose","mx",0, price=1, negativeHeal=-20, emoji='<:coiffeInfirmR:907386964888653824>', orientation=[None,HEALER])
coiffeInfirmB = stuff("Coiffe d'infirmier bleu","my",0, price=1, negativeShield=-20, emoji='<:coiffeInfirmB:907386964288868373>', orientation=[None,BOOSTER])

blueNoeud = stuff("Noeud bleu",'mz',0,1,intelligence=30,negativeHeal=30,negativeShield=-20,emoji='<:noeudB:907386968013418497>',orientation=[None,BOOSTER],position=barrette.position)
whiteNoeud = stuff("Noeud blanc",'na',0,1,charisma=30,negativeHeal=-20,negativeBoost=5,negativeShield=25,emoji='<:noeudBl:907386972505522178>',orientation=[None,HEALER],position=barrette.position)
giletShirt = stuff("Gilet avec T-shirt",'nb',1,1,endurance=10,resistance=10,magie=10,negativeIndirect=10,emoji='<:giletTshirt:907386967472365618>',orientation=[TANK,MAGIC])
LBBerer = stuff("Bêret azuré",'nc',0,1,precision=20,negativeDirect=-20,negativeIndirect=20,emoji='<:beretBleu:907386673166426187>')
starBoots = stuff("Cuissardes nébuleuse","nd",2,1,endurance=30,resistance=20,magie=35,intelligence=5,negativeDirect=30,negativeIndirect=30,precision=-10,emoji='<:startBoots:907799882776076318>',orientation=[TANK,MAGIC])
starPull = stuff("Pull nébuleuse","ne",1,1,endurance=30,resistance=20,magie=35,negativeHeal=25,negativeShield=15,negativeBoost=15,strength=-10,emoji='<:starsPull:907778034738811000>',orientation=[TANK,MAGIC])
starBar = stuff("Barette étoilée","nf",0,1,endurance=10,resistance=10,magie=30,precision=20,critical=5,intelligence=10,negativeHeal=30,negativeShield=35,emoji='<:startBar:907779307630391307>',orientation=[None,MAGIC],position=barrette.position)
starDress = stuff("Robe nébuleuse","ng",1,1,endurance=10,resistance=10,magie=35,negativeDirect=-35,strength=-40,negativeBoost=30,emoji='<:starDress:907799795228352544>',orientation=[None,MAGIC])
starFlats = stuff("Ballerines nébuleuses","nh",2,1,endurance=10,resistance=5,magie=20,negativeIndirect=-35,negativeDirect=-18,negativeHeal=35,negativeShield=33,emoji='<:startFlats:907778001897414766>',orientation=[None,MAGIC])
celestBronzeHat = stuff("Casque en bronze céleste","ni",0,1,emoji='<:feliHelmet:912418068649611314>',strength=35,endurance=30,resistance=15,negativeDirect=-15,precision=-25,negativeHeal=25,magie=-25,orientation=[TANK,DPT])
celestBronzeArmor = stuff("Armure en bronze céleste",'nj',1,1,emoji='<:feliArmor:912418017181302824>',strength=25,endurance=30,resistance=25,negativeDirect=-20,agility=-30,negativeIndirect=20,negativeBoost=30,orientation=[TANK,DPT])
celestBronzeBoots = stuff("Bottes en bronze céleste",'nk',2,1,emoji='<:feliBoots:912418033878859796>',strength=35,endurance=30,resistance=15,negativeDirect=-15,precision=-25,negativeHeal=25,magie=-25,orientation=[TANK,DPT])
armyBoots = stuff("Bottes de l'EEv3",'nl',2,1,strength=40,endurance=10,precision=25,negativeDirect=-15,negativeIndirect=30,charisma=-15,intelligence=-25,orientation=[LONG_DIST,DPT],emoji='<:eev3Boots:911647517152796753>')
armyArmor = stuff("Uniforme de l'EEv3",'nm',1,1,strength=35,endurance=15,precision=25,negativeDirect=-15,negativeIndirect=30,charisma=-15,intelligence=-25,orientation=[LONG_DIST,DPT],emoji='<:eev3Uniform:911647498324549663>')
hinaAcc = stuff("Protège-Bras aviaire","nn",0,1,emoji='<:hinaAcc:908454872515502091>',position=fecaShield.position,strength=30,endurance=10,precision=30,agility=15,percing=5,negativeDirect=-5,critical=-10,negativeBoost=30,negativeHeal=15,negativeShield=15,negativeIndirect=5)
hinaBody = stuff("Tenue aviaire","no",1,1,emoji='<:hinaBody:908454912009060432>',strength=30,endurance=10,precision=20,agility=15,percing=5,negativeDirect=-15,negativeIndirect=35,negativeHeal=20,negativeShield=20)
hinaShoes = stuff("Ballerines aviaires","np",2,1,emoji='<:HinaFlats:908454891255631882>',strength=20,endurance=10,precision=30,agility=25,percing=5,negativeDirect=-5,negativeBoost=30,negativeHeal=20,negativeShield=20,negativeIndirect=5)
pinkChemVeste = stuff("Veste et robe papillon rose","nq",1,1,emoji='<:djpR:908553229539868674>',negativeBoost=-40,endurance=10,charisma=20,intelligence=20,negativeHeal=35,negativeShield=35,orientation=[DISTANCE,BOOSTER])
whiteChemVeste = stuff("Veste et robe papillon blanc","nr",1,1,emoji='<:djpB:908553258497355876>',effect="mk",negativeHeal=-40,endurance=10,charisma=20,intelligence=20,negativeBoost=40,negativeShield=40,orientation=[DISTANCE,HEALER])
blueCharpe = stuff("Écharpe bleue","ns",0,1,emoji='<:bluecharpe:908549607133421578>',negativeShield=-30,intelligence=30,endurance=10,charisma=20,negativeDirect=20,negativeIndirect=20,magie=-10,strength=-10,precision=-10,orientation=[DISTANCE,BOOSTER],position=intemCharpe.position)
bandNoir = stuff("Bandana Noir","nt",0,1,emoji='<:nbn:908554373796343908>',strength=25,agility=25,endurance=20,resistance=10,negativeDirect=-10,precision=-10,magie=-25,critical=-10,negativeIndirect=25)
blueVC = stuff("Veste et chemise bleus","nu",1,1,emoji='<:bsj:908551535796035644>',intelligence=30,negativeShield=-30,endurance=10,charisma=20,negativeHeal=20,negativeIndirect=30,resistance=-10,percing=-10)
bhBoots = stuff("Bottes gravité","nv",2,1,emoji='<:bhBoots:908489324750860309>',endurance=40,resistance=25,negativeIndirect=35,agility=20,precision=-5,negativeDirect=5,negativeBoost=10,negativeHeal=10)
bhPull = stuff("Pull gravité","nw",1,1,emoji='<:bhPull:908489339925856266>',endurance=50,resistance=25,precision=10,negativeHeal=25,negativeShield=25,agility=-15)

julieHat = stuff("Coiffe de la soubrette écarlate","nx",0,1,endurance=5,charisma=40,negativeHeal=-30,negativeBoost=-20,negativeShield=25,strength=-30,magie=-20,emoji='<:julieHat:910192954671505428>')
julieDress = stuff("Robe de la soubrette écarlate","nz",1,1,endurance=5,charisma=30,negativeHeal=-30,resistance=10,negativeBoost=-20,negativeShield=35,negativeDirect=20,negativeIndirect=20,emoji='<:julieDress:910192981959655424>')
julieShoes = stuff("Escarpins de la soubrette écarlate","oa",2,1,endurance=5,charisma=40,negativeHeal=-30,negativeBoost=-20,negativeShield=25,agility=-30,precision=-20,emoji='<:julieShoes:910192936652800031>')

obsiHelmet = stuff("Casque en obsidienne","ob",0,1,endurance=70,resistance=25,agility=20,negativeDirect=20,negativeBoost=15,negativeShield=20,negativeHeal=20,negativeIndirect=20,emoji='<:obsiHelmet:910569288937635900>')
obsiBody = stuff("Armure en obsidienne","oc",1,1,endurance=70,resistance=35,agility=10,negativeDirect=20,negativeBoost=20,negativeShield=15,negativeHeal=20,negativeIndirect=20,emoji='<:obsiBody:910569302615277630>')
obsiBoots = stuff("Bottes en obsidienne","od",2,1,endurance=70,resistance=25,agility=20,negativeDirect=20,negativeBoost=20,negativeShield=20,negativeHeal=15,negativeIndirect=20,emoji='<:obsiBoots:910569317165318174>')

magicArmorHelmet = stuff("Casque magicochromatique de l'EEv3","oe",0,1,endurance=45,magie=35,resistance=20,negativeDirect=-20,strength=-40,intelligence=-30,charisma=-30)
magicArmorBody = stuff("Armure magicochromatique de l'EEv3","of",1,1,endurance=45,magie=25,resistance=25,negativeDirect=-20,strength=-35,intelligence=-30,charisma=-30)
magicArmorBoots = stuff("Bottes magicochromatique de l'EEv3","og",2,1,endurance=45,magie=35,resistance=20,negativeDirect=-20,strength=-40,intelligence=-30,charisma=-30)

mysticHat = stuff("Coiffe mystique","oh",0,1,emoji='<:magHat:912405415067783228>',magie=60,endurance=10,negativeDirect=-25,strength=-10,negativeIndirect=-25,negativeBoost=30,negativeHeal=30,negativeShield=30)
mysticBody = stuff("Tunique mystique","oi",1,1,magie=50,emoji='<:magTunic:912405342888013874>',endurance=15,negativeDirect=-20,negativeIndirect=-20,strength=-10,resistance=15,negativeBoost=30,negativeHeal=30,negativeShield=30)
mysticBoots = stuff("Bottes mystiques","oj",2,1,magie=60,emoji='<:magBoots:912405359128346694>',endurance=10,negativeDirect=-25,negativeIndirect=-25,strength=-10,negativeBoost=30,negativeHeal=30,negativeShield=30)

whiteButterFlyBoots = stuff("Bottes du papillon blanc","ok",2,1,charisma=30,negativeHeal=-30,endurance=10,intelligence=20,negativeShield=20,negativeBoost=30,negativeDirect=20,emoji='<:whiteButterflyBoots:911245758081138758>')
pinkButterFlyBoots = stuff("Bottes du papillon rose","ol",2,1,charisma=30,negativeBoost=-30,endurance=10,intelligence=20,negativeShield=20,negativeHeal=30,negativeDirect=20,emoji='<:pinkButterflyBoots:911245683124752445>')
purpleButterFlyBoots = stuff("Bottes du papillon violet","om",2,1,magie=30,negativeIndirect=-30,endurance=10,intelligence=20,negativeShield=20,negativeHeal=30,negativeDirect=20,emoji='<:purpleButterflyBoots:911245717715161098>')
purpleChemVeste = stuff("Veste et robe papillon violet","on",1,1,emoji='<:purpleButterflyDress:910582874263146496>',negativeIndirect=-40,endurance=10,magie=40,negativeDirect=70)
blueButterFlyBoots = stuff("Bottes du papillon bleu","oo",2,1,intelligence=30,negativeShield=-30,endurance=10,charisma=20,negativeHeal=20,negativeBoost=30,negativeDirect=20,emoji='<:blueButterflyBoots:911245699377676308>')
blueChemVeste = stuff("Veste et robe papillon bleu","op",1,1,emoji='<:blueButterflyDress:910582894253182976>',negativeShield=-40,endurance=10,charisma=20,intelligence=20,negativeHeal=35,negativeBoost=35)

lunaPandan = stuff("Obsidienne en pendantif","oq",0,0,strength=40,agility=40,endurance=20,resistance=15,charisma=-30,negativeIndirect=40,negativeHeal=25,emoji='<:obsiPendan:911086215409848341>',position=batPendant.position)
lunaDress = stuff("Robe et veste noire","or",1,0,strength=35,agility=35,endurance=25,resistance=20,intelligence=-30,negativeBoost=40,negativeIndirect=25,emoji='<:blackDress:911086257831039016>')
lunaBoots = stuff("Cuissardes noires","os",2,0,strength=40,agility=40,endurance=20,resistance=15,magie=-30,negativeHeal=40,negativeBoost=25,emoji='<:blackBoots:911086872900546560>')

coalHat = stuff("Barrête de la cohabitation rep.","ot",0,0,magie=50,negativeDirect=-50,endurance=10,resistance=10,negativeIndirect=100,emoji='<:coaBar:911659734812229662>',position=barrette.position)
coalDress = stuff("Robe de la cohabitation rep.","ou",1,0,magie=45,negativeDirect=-45,endurance=15,resistance=15,negativeIndirect=100,emoji='<:coaDress:911659797076660294>')
coalBoots = stuff("Bottines de la cohabitation rep.","ov",2,0,magie=50,negativeDirect=-50,endurance=10,resistance=10,negativeIndirect=100,emoji="<:coaBoots:911659778995007528>")

redButterFlyBoots = stuff("Bottes du papillon rouge","ow",2,1,magie=30,negativeDirect=-30,endurance=10,intelligence=20,negativeShield=20,negativeHeal=30,negativeIndirect=20,emoji='<:redButterflyBoots:911245739093524480>')
redChemVeste = stuff("Veste et robe papillon rouge","ox",1,1,emoji='<:redButterflyDress:911245794617724968>',negativeDirect=-40,endurance=10,magie=40,negativeIndirect=70)

newMoonHat = stuff("Coiffe de la nouvelle lune","oy",0,1,endurance=20,intelligence=30,resistance=20,negativeShield=-20,negativeHeal=30,precision=-10,strength=-30,emoji='<:newMoonHead:912914075581808690>')
newMoonArmor = stuff("Armure de la nouvelle lune","oz",1,1,endurance=30,intelligence=25,resistance=20,negativeShield=-15,negativeHeal=30,agility=-10,magie=-30,emoji='<:newMoonArmor:912914097509630042>')
newMoonBoots = stuff("Bottes de la nouvelle lune","pa",2,1,endurance=20,intelligence=30,resistance=20,negativeShield=-20,negativeHeal=30,charisma=-10,negativeBoost=30,emoji='<:newMoonBoots:912914114463019069>')

fullMoonHat = stuff("Coiffe de la pleine lune","pb",0,1,endurance=30,intelligence=40,resistance=20,negativeShield=-25,negativeHeal=35,precision=-30,strength=-30,emoji='<:fullMoonHead:912914171925000202>')
fullMoonArmor = stuff("Armure de la pleine lune","pc",1,1,endurance=40,intelligence=30,resistance=30,negativeShield=-20,negativeHeal=35,agility=-30,magie=-35,emoji='<:fullMoonArmor:912914156842278913>')
fullMoonBoots = stuff("Bottes de la pleine lune","pd",2,1,endurance=30,intelligence=40,resistance=20,negativeShield=-25,negativeHeal=35,charisma=-30,negativeBoost=30,emoji='<:fullMoonBoots:912914130623680543>')

bunnyEars = stuff("Serre tête oreilles de lapin","pe",0,1,charisma=40,negativeBoost=-30,intelligence=30,precision=10,endurance=-20,resistance=-10,negativeShield=30,magie=-30,emoji='<:bunnyHeadset:912846454098374691>')
bunnyBody = stuff("Juste-au-corps de lapin","pf",1,1,charisma=40,negativeBoost=-30,intelligence=30,precision=10,strength=-20,magie=-10,negativeIndirect=30,negativeHeal=30,emoji='<:bunnyBody:912846432485142600>')
bunnyShoes = stuff("Sandales à talons de lapin","pg",2,1,charisma=40,negativeBoost=-30,intelligence=30,precision=10,agility=-20,resistance=-10,negativeDirect=30,strength=-30,emoji='<:bunnyHeels:912846592321671209>')

crepuHat = stuff("Coiffe du crépuscule","ph",0,1,endurance=20,charisma=30,resistance=20,negativeHeal=-20,negativeShield=30,precision=-10,strength=-30,emoji='<:crepHead:913170593636048996>')
crepuArmor = stuff("Armure du crépuscule","pi",1,1,endurance=30,charisma=25,resistance=20,negativeHeal=-15,negativeShield=30,agility=-10,magie=-30,emoji='<:crepArmor:913170610367119410>')
crepuBoots = stuff("Bottes du crépuscule","pj",2,1,endurance=20,charisma=30,resistance=20,negativeHeal=-20,negativeShield=30,intelligence=-10,negativeBoost=30,emoji='<:crepBoots:913170562988273674>')

zenithHat = stuff("Coiffe du zénith","pk",0,1,endurance=30,charisma=40,resistance=20,negativeHeal=-25,negativeShield=35,precision=-30,strength=-30,emoji='<:zenithHead:913170464581484554>')
zenithArmor = stuff("Armure du zénith","pl",1,1,endurance=40,charisma=30,resistance=30,negativeHeal=-20,negativeShield=35,agility=-30,magie=-35,emoji='<:zenithArmor:913170492452646922>')
zenithBoots = stuff("Bottes du zénith","pm",2,1,endurance=30,charisma=40,resistance=20,negativeHeal=-25,negativeShield=35,intelligence=-30,negativeBoost=30,emoji='<:zenithBoots:913170512564334623>')

bardHat = stuff("Chapeau du barde","po",0,1,intelligence=40,negativeBoost=-40,negativeShield=-20,charisma=10,negativeHeal=30,negativeDirect=30,negativeIndirect=30)
bardBody = stuff("Vêtements du barde","pp",1,1,intelligence=40,negativeBoost=-40,resistance=20,endurance=10,strength=-30,magie=-30,agility=-15,precision=-15)
bardShoes = stuff("Chaussures du barde","pq",2,1,intelligence=40,negativeBoost=-40,charisma=20,negativeShield=-10,negativeHeal=30,agility=-30,precision=-30)

floorTanking = effect("Maître tankeur de sol","dragoonIsDead",unclearable=True,turnInit=-1,description='Augmente de 1 tour la durée de l\'effet "Âme en peine" sur soi (Non cumulable !)')

dragoonHelmet = stuff("Heaume du tankeur de sol","pr",0,1,strength=35,agility=25,endurance=10,resistance=10,percing=10,magie=-30,charisma=-20,negativeHeal=15,negativeShield=15,effect=floorTanking,emoji='<:floorTankHelmet:914608772247347200>')
dragoonArmor = stuff("Armure du tankeur de sol","ps",1,1,strength=25,agility=25,endurance=20,resistance=15,percing=5,magie=-30,intelligence=-20,negativeHeal=15,negativeShield=15,effect=floorTanking,emoji='<:floorTankArmor:914608787187441665>')
dragoonBoots = stuff("Solerets du tankeur de sol","pt",2,1,strength=25,agility=35,endurance=10,resistance=10,percing=10,magie=-30,charisma=-20,negativeHeal=15,negativeShield=15,effect=floorTanking,emoji='<:floorTankBoots:914608812663652353>')

whiteLily = stuff("Broche du lys blanc","pu",0,1,charisma=25,negativeHeal=-40,effect=flum.effect,emoji='<:whiteLily:914608227545673758>',strength=-30,magie=-25)
bloodLily = stuff("Broche du lys de sang","pv",0,1,magie=25,negativeDirect=-40,effect=darkFlum.effect,emoji='<:bloodLily:914608243354001429>',charisma=-30,intelligence=-25)