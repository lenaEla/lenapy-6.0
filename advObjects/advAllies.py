from traceback import print_exc
from classes import *
from constantes import *
from advObjects.advWeapons import *
from advObjects.advSkills import *
from advObjects.advStuffs import *
from advObjects.advSummons import *
from advObjects.advEffects import *
from advObjects.npcSkills.npcSkillsAllies import *

lohicaFocal = copy.deepcopy(focal)
lohicaFocal.say = "Vous commencez sérieusement à me tapez sur les nerfs..."

aliceCheating = copy.deepcopy(vampirisme2)
aliceCheating.name, aliceCheating.group, aliceCheating.maxHpCost, aliceCheating.hpCost = aliceCheating.name + " (Alice)", SKILL_GROUP_HOLY, 10, 0

rubySays = says(
    start="Vous savez, c'est pas vraiment dans mes habitudes de participer moi-même aux combats. Prenez donc ça comme une exception",
    ultimate="Félicitation, vous avez tenus jusqu'à là, donc je suppose qu'on peut commencer à vraiment s'y mettre, vous en pensez quoi ?",
    limiteBreak="Et bah dites-donc, vous êtes du genre tenace, n'est-ce pas ?",
    onKill="J'espérais quand même un peu plus de résistance",
    onResurect="C'est terriblement gênant...",
    blueWinAlive="Déjà fini ? J'en espérais pas trop, mais je suis tout de même décue",
    redWinAlive="Et bien et bien... Il semblerais que vous ayez quelques bases à reprendre, non ?",
    reactAllyKilled="Ah. Je vois que je vais devoir m'impliquer un peu plus que prévu, apparament",
    reactAllyLb="Et bien, qu'elle démonstration",
    reactEnemyLb="Hum. Pas si mal",
    onHit="Il semblerais qu'il va en falloir plus pour te faire plier, n'est-il pas ?",
    specDeath={"Julie":"MADAME !"},specReact={"Clémence":"Il semblerait que vous n'avez plus les mêmes réflexes, dame Ruby"},specKill={"Clémence":"L'élève a dépassé le maître"}
)

listSetName = {}
def getStuffSet(name:str):
    rep = [None,None,None]
    if name not in listSetName.keys():
        for stuffMaxLevel in listMaxLevelStuff:
            if stuffMaxLevel.name.split(" +")[0].endswith(name.split(" +")[0]):
                rep[stuffMaxLevel.type], haveAll = stuffMaxLevel, True
                for tempStuff in rep:
                    if tempStuff == None: haveAll = False; break
                if haveAll: listSetName[name] = rep; return rep
    else: return listSetName[name]
    print("Couldn't find the stuffs with the name : {0}".format(name))
    return rep

# Alliés temporaires =============================================================================
tablAllAllies = [
    tmpAllie("Lena", 1, light_blue, OBSERVATEUR, splatcharger, getStuffSet("Sniper Légendaire"), GENDER_FEMALE, [analysedShot, lenaInkStrike, lenaDrone1, cryoChargeBundle, doubleShot, ricochetSolo, preciseShot], [ELEMENT_WATER], icon='<:lena:909047343876288552>', bonusPoints=[STRENGTH, PRECISION, ENDURANCE], say=lenaSays,birthday=(19,1),charSettings=lenaIa ,splashIcon='<:lena:1106478667871289455>',equippedChips=[getChip("Diffraction","Force augmentée I","Overpower","Démolition","Dégâts directs augmentés")],variantTabl={"Luna":25}),
    tmpAllie("Gwendoline", 2, 0xFFFF6B, PROTECTEUR, gWeap, getStuffSet("Paladin Nocturne"), GENDER_FEMALE, [royaleGardeSkill,impact,heartStone,gwenCharge,gwenPenta,justiceEnigma,gwenyQCombo],element= [ELEMENT_EARTH, ELEMENT_SPACE], bonusPoints=[STRENGTH, ENDURANCE, AGILITY], icon='<:gweny:906303014665617478>', say=gwenySays, birthday=(9,9), splashIcon='<:gwendoline:1126633253047124108>',variantTabl={"Klironovia":30,"Altikia":30}, equippedChips=[getChip("Bouclier d'épines","Barrière","Blocage augmenté","Contre-Offensive","Bout-Portant")]),
    tmpAllie("Clémence", 2, 0x8F001C, MAGE, rapiere, getStuffSet("Mage écarlate Légendaire"), GENDER_FEMALE, [sanguisGladio, sanguisGladio2, bloodmissiles, findSkill("Blood Cross"), umbraMortis, sectumsempra], element= [ELEMENT_DARKNESS, ELEMENT_FIRE], icon='<:clemence:908902579554111549>', bonusPoints=[MAGIE, PRECISION], say=clemSays, deadIcon='<:AliceOut:908756108045332570>',birthday=(31,10),charSettings=clemIa,splashIcon='<:clemence:1088483909454536784>',splashArt="https://media.discordapp.net/attachments/1200064382063869984/1236355329449656400/Sans_titre_138_20240504164537.png",team=NPC_DEMON,equippedChips=[getChip("Vampirisme I","Overpower","Magie augmentée I","Lune de Sang","Goût du Sang")], variantTabl={"Liz":15}),
    tmpAllie("Alice", 1, aliceColor, IDOLE, micPink, getStuffSet("Chanteur Légendaire"), GENDER_FEMALE, [aliceDance, courage, invocBat2, roses, requiem, corGra, synastie], element= [ELEMENT_SPACE, ELEMENT_WATER], icon='<:alice:908902054959939664>', bonusPoints=[CHARISMA, INTELLIGENCE], say=aliceSays, deadIcon='<:AliceOut:908756108045332570>',birthday=(14,6),charSettings=preDefCharSet[2][1][1][2],splashArt='https://media.discordapp.net/attachments/640667220124499988/1069699168714625034/Sans_titre_25_20230130201824.png?width=456&height=676',splashIcon='<:alice:1069700207345946715>',team=NPC_HOLY,trait=[TRAIT_ARACHNOPHOBE,TRAIT_HIGHLIGHTED],equippedChips=[getChip("Médaille de la Chauve-Souris","Spotlight","Charisme augmenté I","Symbiose","Maître Invocateur")],variantTabl={"Jade":15}),
    tmpAllie("Shushi", 1, 0x0303D5, ENCHANTEUR, eclatanaDoto, getStuffSet("Assassin Mage Légendaire"), GENDER_FEMALE, [squidRoll, bundleCaC, waterCircle, krakenCharge, findSkill("skx"), magicRuneStrike, findSkill("sfz")], element= [ELEMENT_WATER, ELEMENT_SPACE], icon='<:shushi:909047653524963328>', bonusPoints=[MAGIE, ENDURANCE], say=shushiSays,birthday=(26,9),charSettings=preDefCharSet[0][1][2][2], splashIcon = "<:shushi:1243488103880986676>", equippedChips=[getChip("Agilité augmentée I","Esquive augmentée","Réflex","Précision augmentée I","Camalataque")], variantTabl={"Shihu":25}),
    tmpAllie("Lohica", 1, purple, SORCELER, secretum, getStuffSet("Mage Ultraviolet Légendaire"), GENDER_FEMALE, [lohicaFocal, fairyRay, fairyLiberation, propag, lohicaBrouillad, fairyBomb], element= [ELEMENT_DARKNESS, ELEMENT_DARKNESS], bonusPoints=[MAGIE, INTELLIGENCE], icon='<:lohica:919863918166417448>', deadIcon='<:flowernt:894550324705120266>',team=NPC_FAIRY,birthday=(27,7),trait=[TRAIT_ARACHNOPHOBE], equippedChips=[getChip("Héritage d'Estialba","Toxiception","Magie augmentée I","Intelligence augmentée I","Dégâts indirects augmentés")]),
    tmpAllie("Hélène", 2, white, ALTRUISTE, heleneBrush, getStuffSet("Soigneur Légendaire"), GENDER_FEMALE, [radiance, lapSkill, renisurection, fairyGarde, reconst, revif, lifeFontain], element= [ELEMENT_WATER, ELEMENT_WATER], bonusPoints=[CHARISMA, INTELLIGENCE], splashIcon='<:helene:1183494550384291951>', icon='<:helene:906303162854543390>',charSettings=preDefCharSet[1][1][1][2], deadIcon='<:fairyOut:935335430814068786>',team=NPC_FAIRY,trait=[TRAIT_ARACHNOPHOBE], equippedChips=[getChip("Transgression","Soins augmentés I","Soins et armures réalisés augmentés","Charisme augmenté II","Sur-Vie"), getChip("Ambivalance","Charisme augmenté I","Soins et armures réalisés augmentés","Soins augmentés I","Convertion Vitale")],say=heleneSays, birthday=(25,5), variantTabl={"Lio":15}),
    tmpAllie("Félicité", 1, red, TETE_BRULEE, dtsword, getStuffSet("Plugiliste Légendaire"), GENDER_FEMALE, [bloodyStrike, antConst, deterStrike, strengthOfWillCast, convictTet, fragmentation, absorbingStrike2], bonusPoints=[ENDURANCE, STRENGTH], icon='<:felicite:909048027644317706>', element=[ELEMENT_UNIVERSALIS,ELEMENT_UNIVERSALIS],birthday=(10,6),say=feliSays,splashIcon="<:felicite:1116861426556997653>",trait=[TRAIT_ARACHNOPHOBE],equippedChips=[getChip("Sur-Vie","Force augmentée I","Convertion","Démolition","Vampirisme I")],variantTabl={"Lia":15}),
    tmpAllie("Akira", 2, black, TETE_BRULEE, fauc, getStuffSet("Plugiliste Légendaire"), GENDER_MALE, [deathShadow, defi, absorbingStrike2, bundleLemure, theEndCast, bundleFetu, comboFaucheCroix], element=[ELEMENT_DARKNESS,ELEMENT_EARTH], bonusPoints=[ENDURANCE, STRENGTH], icon='<:akira:909048455828238347>', equippedChips=[getChip("Incurable","Friable","Achèvement","Lune de Sang","Démolition")]),
    tmpAllie("Icealia", 2, light_blue, PREVOYANT, blueButterfly, getStuffSet("Armurier Légendaire"), GENDER_FEMALE, [soulagementBundle, royalShield, haimaBundle, firstArmor, lightPulse, matriceShield, elemShield], element=[ELEMENT_LIGHT, ELEMENT_LIGHT], bonusPoints=[INTELLIGENCE, ENDURANCE], icon='<:icealia:1308103151643136020>', equippedChips=[getChip("Un pour tous","Armure Initiale","Armures augmenté I",'Intelligence augmentée I',"Soins et armures réalisés augmentés")]),
    tmpAllie("Powehi", 2, black, MASCOTTE, grav, getStuffSet("Paladin étoilé"), GENDER_FEMALE, [blackHole, isolement, blindage, cosmicPower, inkRes2, ironHealth, concen], element=[ELEMENT_SPACE, ELEMENT_SPACE], bonusPoints=[ENDURANCE, INTELLIGENCE], icon='<:powehi:909048473666596905>', deadIcon='<:powehiDisiped:907326521641955399>', say=powehiSays, splashIcon='<:powehi:1128584646779752498>',equippedChips=[getChip("Bouclier Sacrificiel","Absorbtion","Altruisme","Empathie","Présence")]),
    tmpAllie("Shehisa", 1, purple, POIDS_PLUME, shehisa, getStuffSet("Assassin de l'Ombre Nocturne"), GENDER_FEMALE, [bleedingStrikeBundle, trappedField, UmbralTravel, bundleSurpriseJump, bombThrow, assasinate, smnMyrlope], element=[ELEMENT_WATER, ELEMENT_FIRE], bonusPoints=[STRENGTH, AGILITY, PRECISION], icon='<:shehisa:919863933320454165>', splashIcon='<:shehisa:1183500980680142878>',say=shehisaSays, charSettings=lenaIa , deadIcon='<:fairyOut:935335430814068786>',team=NPC_FAIRY,trait=[TRAIT_ARACHNOPHILE],equippedChips=[getChip("Achèvement","Cadeau Explosif","Pas Piégés","Dissimulation","Réflex")]),
    tmpAllie("Ruby", 2, 0x870a24, MAGE, butterflyRed, getStuffSet("Mage écarlate Légendaire"), GENDER_FEMALE, [invocCarbunR, spaceMagicCombo, magicBarrier, rubyArcane, maitriseElementaire, magicEffGiver, rubyLight], element=[ELEMENT_UNIVERSALIS, ELEMENT_UNIVERSALIS], icon='<:ruby:1112519724799103037>', bonusPoints=[MAGIE, PRECISION], splashIcon='<:ruby:1108041397929517147>', say=rubySays, equippedChips=[getChip("Magie augmentée I","Magie augmentée II","Pénétration","Vampirisme I","Lune de Sang")]),
    tmpAllie("Sixtine", 1, blue, INOVATEUR, miltrilPlanisphere, getStuffSet("Barde Légendaire"), icon='<:sixtine:908819887059763261>', skill=[toxicon, horoscope, debuffMoonBundle, revelation, backupdancer, buffMoonBundle, aff2], gender=GENDER_FEMALE, element=ELEMENT_SPACE, bonusPoints=[INTELLIGENCE, ENDURANCE], say=sixtineSays,birthday=(12,6),splashIcon='<:sixtine:1191385884101185626>',equippedChips=[getChip("Boosts augmenté I","Intelligence augmentée I","Aura Galvanisante","Spotlight","Bénédiction")],variantTabl={"Lei":15}),
    tmpAllie("Hina", 1, purple, OBSERVATEUR, plume, getStuffSet("Sniper Légendaire"), GENDER_FEMALE, [plumeCel, plumePers, pousAviaire, hinaUlt, plumRem, featherCross, trainePlume], icon='<:hina:908820821185810454>', element=[ELEMENT_AIR, ELEMENT_AIR], bonusPoints=[PRECISION, STRENGTH],charSettings=hinaIa),
    tmpAllie("John", 2, orange, POIDS_PLUME, airsword, getStuffSet("Assassin de l'Ombre Nocturne"), GENDER_MALE, [airlame, airStrike, physEffGiver, klikliQCombo, lycantStrike, burningClaw, brotherHood], icon='<:john:908887592756449311>', bonusPoints=[STRENGTH, AGILITY], say=johnSays, element=[ELEMENT_AIR,ELEMENT_EARTH]),
    tmpAllie("Julie", 1, red, ALTRUISTE, julieWeap, getStuffSet("Soigneur Légendaire"), GENDER_FEMALE, [accelerant, altOH, julieUlt, timeSp, zelian, extraMedica, shareSkill],element=[ELEMENT_TIME, ELEMENT_TIME], bonusPoints=[CHARISMA, INTELLIGENCE], icon="<:julie:910185448951906325>", say=julieSays),
    tmpAllie("Krys", 2, purple, TETE_BRULEE, krysWeapon, getStuffSet("Plugiliste Légendaire"), GENDER_OTHER, [earthStrike, fizzbang, krysUlt, mudlame, krystalisation, ebranlement], element=[ELEMENT_EARTH, ELEMENT_EARTH], icon="<:krys:916118008991215726>", deadIcon='<:krysCan:916117137339322388>', bonusPoints=[ENDURANCE, STRENGTH],trait=[TRAIT_LYTHOPHAGE], equippedChips=[getChip("Force augmentée I","Endurance augmenté I","Dégâts indirects reçus réduits","Dégâts reçus réduits","Lithophage")], variantTabl={"Alexandre":20, "Liu":15}),
    tmpAllie("Edelweiss", 1, 0xE0FFE7, PREVOYANT, bleuSpiritWings, getStuffSet("Armurier Légendaire"), GENDER_FEMALE, [haimaBundle, krasis, dosisBundle, intelRaise, holos, kerachole, pneuma], element=[ELEMENT_EARTH, ELEMENT_WATER], icon='<:edelweiss:918451422939451412>', deadIcon="<:flowernt:894550324705120266>", bonusPoints=[INTELLIGENCE, ENDURANCE],team=NPC_DRYADE,trait=[TRAIT_ARACHNOPHOBE], equippedChips=[getChip("Intelligence augmentée I","Directs augmentée I","Armures augmenté I","Armure Solide","Un pour tous")],splashIcon='<:edelweiss:1237117806462505040>'),
    tmpAllie("Iliana", 1, white, ALTRUISTE, iliSwoShield, getStuffSet("Paladin Radieux"), GENDER_FEMALE, [lightAura2, ironWillSkill, clemency, lightBigHealArea, aurore2, holiomancie, holyShieltron], element= [ELEMENT_LIGHT, ELEMENT_LIGHT], icon='<:Iliana:926425844056985640>', splashIcon = '<:iliana:1124750738153811998>', deadIcon='<:oci:930481536564879370>', bonusPoints=[CHARISMA, ENDURANCE], say=ilianaSaysNormal,team=NPC_HOLY,birthday=(4,7),trait=[TRAIT_CATGIRL],equippedChips=[getChip("Contre-Offensive","Retour de Bâton","Constitution II","Blocage augmenté","Soins et armures réalisés augmentés")]),
    tmpAllie('Candy', 2, 0xa124b2, INOVATEUR, concentraceurZoom, getStuffSet("Sniper Légendaire"), GENDER_FEMALE, [smnSpaceTurets, stimulate, lenaDrone1, killerWailUltimate, invocAutFou, invocAutQueen, invocAutTour], icon='<:candy:933518742170771466>', bonusPoints=[MAGIE, STRENGTH], equippedChips=[getChip("Maître Invocateur","Force augmentée I","Force augmentée II","Constitution I","Haut-Perceur 5.1")]),
    tmpAllie('Ly', 1, white, ATTENTIF, triStringer, getStuffSet("Stratège Légendaire"), GENDER_FEMALE, [acidRain, coroRocket, quadFleau, ultraSignal, tactician, machDeFer, lanceTox], element=[ELEMENT_FIRE, ELEMENT_FIRE], icon='<:ly:943444713212641310>', bonusPoints=[STRENGTH, PRECISION], say=lySays, equippedChips=[getChip("Totem de Protection","Indirects augmentée I","Incurable","Dispersion","Châpeau de Roues")],splashIcon='<:ly:1243526418546032732>'),
    tmpAllie('Anna', 2, black, PROTECTEUR, lunarBonk, getStuffSet("Paladin Nocturne"), GENDER_FEMALE, [royaleGardeSkill, darkShield, ghostlyCircle, heartStone, haimaBundle, inMemoria, bigBubbler], element=[ELEMENT_EARTH, ELEMENT_EARTH], icon='<:anna:943444730430246933>', bonusPoints=[ENDURANCE, INTELLIGENCE],trait=[TRAIT_ARACHNOPHOBE],variantTabl={"Belle":50}),
    tmpAllie("Elina", 1, 0x560909, ALTRUISTE, elinaWeap, getStuffSet("Soigneur Légendaire"), GENDER_FEMALE, [nanoHeal, cure, uberCharge, terachole, renisurection, intenseCure, reconst], element=[ELEMENT_LIGHT, ELEMENT_WATER], icon='<:elina:1113685290620571700>', bonusPoints=[CHARISMA, PRECISION],charSettings=preDefCharSet[1][1][2][2], equippedChips=[getChip("Soins et armures réalisés augmentés","Charisme augmenté I","Précision augmentée I","Précision Chirurgicale","Critique universel")],splashArt='https://media.discordapp.net/attachments/769956170081107978/1241309849212420156/Sans_titre_142_20240518102622.png?',splashIcon='<:elina:1241309730245443635>'),
    tmpAllie("Bénédicte", 1, white, MAGE, dvinSeptre, getStuffSet("Mage écarlate Légendaire"), GENDER_FEMALE, [genesis, comboVerMiracle, beneRedempt, benitWater, divineBenediction, divineCircle, divineAbne], element=[ELEMENT_LIGHT, ELEMENT_LIGHT], bonusPoints=[MAGIE, CHARISMA], icon='<:benedict:1116416894426173520>',team=NPC_ANGEL, equippedChips=[getChip("Crucifix","Magie augmentée I","Appel de la Lumière","Précision Critique","Châpeau de Roues")],variantTabl={"Victoire":25},splashIcon='<:benedict:1235273144030335067>',splashArt="https://media.discordapp.net/attachments/769956170081107978/1235272647189987338/Sans_titre_138_20240501185137.png"),
    tmpAllie("Chûri",1,light_blue,MAGE,phenixLeath, getStuffSet("Guerrier Mage Légendaire"), GENDER_FEMALE, [fairySlash, maitriseElementaire, elemRuneSkill[ELEMENT_EARTH], raisingPheonix, earthCircle, magicEffGiver, cassMont],deadIcon="<:fairyOut:935335430814068786>",icon="<:churi:992941366537633914>",bonusPoints=[MAGIE,PRECISION],element=[ELEMENT_EARTH,ELEMENT_EARTH],say=churiSays,splashArt="https://media.discordapp.net/attachments/640667220124499988/1084973959948288083/Sans_titre_46_20230313063859.png?width=507&height=676",splashIcon="<:churi:1088897813678653513>",team=NPC_UNDEAD),
    tmpAllie("Lily",2,0xD9A4FD,INOVATEUR, miltrilPlanisphere, getStuffSet("Barde Légendaire"), GENDER_FEMALE, [dmonBlood, burningGround, demonLand, dmonCrit, dmonDmg, aeraCharm, dmonAgi], element=[ELEMENT_SPACE,ELEMENT_DARKNESS],icon="<:lily:1006442350471553076>",bonusPoints=[INTELLIGENCE,ENDURANCE],say=lilySays,team=NPC_DEMON,equippedChips=[getChip("Démaniaque","Précaution","Spotlight","Convertion Vitale","Cicatrisation")],splashIcon='<:lily:1226588449809633321>',charSettings=createCharSettingsDict(weaponUse=CHARSET_WEAPON_USE_LOW,dmgSkillUse=CHARSET_DMGSKILL_HIGH,buffSkillUse=CHARSET_BOOSTSKILL_HIGH,debuffSkillUse=CHARSET_DEBUFFSKILL_HIGH),splashArt="https://media.discordapp.net/attachments/264128214593568768/1226575068042236015/Sans_titre_142_20240407185040.png"),
    tmpAllie("Epiphyllum",1,0xEAC6DB, PREVOYANT, epiphyllum, getStuffSet("Barde Légendaire"), GENDER_FEMALE, [invocSeraf, soulagementBundle, reconfortBundle, moonLight, seraphism, silvArmor, sacredSoil], icon='<:epiphilium:1014094726351294484>', deadIcon = "<:flowernt:894550324705120266>", element=[ELEMENT_SPACE,ELEMENT_WATER],bonusPoints=[INTELLIGENCE,PRECISION],charSettings=preDefCharSet[1][1][2][2],team=NPC_DRYADE),
    tmpAllie("Astra",1,white, MASCOTTE, lunarBonk, getStuffSet("Paladin étoilé"), GENDER_FEMALE, [blackHole, tacShield, findSkill("Divination"), moonLight, findSkill("Thèses fluidiques"), phalax, findSkill("Grâce du Poisson")],element=[ELEMENT_TIME,ELEMENT_SPACE],bonusPoints=[ENDURANCE,INTELLIGENCE], icon="<:astra:1051825407466426430>", deadIcon='<:fairyOut:935335430814068786>', splashIcon='<:astra:1051977465884594306>', splashArt="https://media.discordapp.net/attachments/264128214593568768/1051916946679025776/Sans_titre_12_20221212171102.png?width=460&height=675",team=NPC_FAIRY),
    tmpAllie("Céleste",2,0x1E0098, ENCHANTEUR, magicSwordnShield, getStuffSet("Guerrier Mage Légendaire"), GENDER_FEMALE, [ferocite, dualSupp, dualEnergyDrain, celestialChoc, smnAnais, comboConfiteor, selfMemoria], element=[ELEMENT_SPACE,ELEMENT_EARTH],deadIcon='<:oci:930481536564879370>',icon='<:celeste:1129042444479119401>',bonusPoints=[MAGIE,ENDURANCE],trait=[TRAIT_CATGIRL]),
    tmpAllie("Zénéca",1,white,SORCELER,toxicBrush, getStuffSet("Mage Ultraviolet Légendaire"),GENDER_FEMALE,[propagDelPas,exploMark,epidemic,gangrene,toxiOvercharge,markInfex,intaveneuse],element=[ELEMENT_WATER,ELEMENT_TIME],deadIcon='<:fairyOut:935335430814068786>',icon='<:zeneca:1177606488496283689>',splashIcon='<:zeneca:1177605494219739176>',bonusPoints=[MAGIE,INTELLIGENCE],team=NPC_FAIRY, equippedChips=[getChip("Radiance Toxique","Héritage d'Estialba","Vampirisme II","Magie augmentée I","Toxiception")],say=zenecaSays),
    tmpAllie("Amandine",1,0xb8f3a7,POIDS_PLUME,splattershot, getStuffSet("Plugiliste Légendaire"),GENDER_FEMALE,[burst,splatbomb,inkzooka,trizooka,triSlashdown,fizzbang,bento],element=[ELEMENT_WATER,ELEMENT_SPACE],icon='<:amandine:1191883886309949501>',bonusPoints=[STRENGTH,PRECISION],say=amandineSays,charSettings=preDefCharSet[0][1][1][2]),
    tmpAllie("Amary",1, 0xdb6163, IDOLE, flumWand, getStuffSet("Chanteur Légendaire"), GENDER_FEMALE, [croissance, exploPetal, petalisation, roseeHeal, floraisonFinale, theSkill, astrodyn] ,"Floraaaaaaaa ?",[ELEMENT_SPACE,ELEMENT_WATER],deadIcon='<:amaryDown:979440197127262218>',icon='<:amary:979441677460713502>',bonusPoints=[CHARISMA,INTELLIGENCE],charSettings=preDefCharSet[2][1][1][2],team=NPC_DRYADE)
    
]

churInoSkills = [galvanisation, fizzbang, elemRuneSkill[ELEMENT_FIRE], raisingPheonix, fireCircle, magicEffGiver, cycloneEcarlate]

# Tabl var allies =============================================================================
tablVarAllies = [
    tmpAllie("Luna", 1, black, POIDS_PLUME, infDarkSword, getStuffSet("Assassin de l'Ombre Nocturne"), GENDER_FEMALE, [meditate, brotherHood, soupledown, highkick, renforPhys, bundleRixeEva, fizzbang],"Là où se trouve la Lumière se trouvent les Ténèbres", [ELEMENT_DARKNESS, ELEMENT_AIR], variant=True, icon='<:luna:909047362868105227>', bonusPoints=[STRENGTH, ENDURANCE], say=lunaSays, splashIcon='<:luna:1242920285577936896>'),
    tmpAllie("Altikia", 2, 0xDFFF92, VIGILANT, aWeap, getStuffSet("Paladin Radieux"), GENDER_FEMALE, [ironWillSkill, altyCover, altyPenta, healingSacrifice, convictionVigilante, altyStrike, altyQCombo],"Une personnalité de Gwen qui préfère se concentrer sur ses alliés", [ELEMENT_WATER, ELEMENT_LIGHT], variant=True, bonusPoints=[ENDURANCE, CHARISMA], icon='<:alty:1112517632671875152>', say=altySays, splashIcon='<:altikia:1126732994732884049>'),
    tmpAllie("Klironovia", 2, 0xF49206, BERSERK, kWeap, getStuffSet("Plugiliste Légendaire"), GENDER_FEMALE, [intuitionFoug, klikliQCombo, kStrike, kliBloody, klikliStrike, pentastrike, retourneImpactant],"Une personnalité de Gwen bien plus violente que les deux autres", [ELEMENT_AIR, ELEMENT_TIME], variant=True, bonusPoints=[STRENGTH, AGILITY], icon='<:klikli:906303031837073429>', say=klikliSays, splashIcon ='<:klironovia:1126632922510786690>',equippedChips=[getChip("Plot Armor","Blocage augmenté","Force augmentée I","Contre-Offensive","Bouclier d'épines")]),
    tmpAllie("Shihu", 1, 0x00002D, MAGE, darkMetRuneMid, getStuffSet("Mage écarlate Légendaire"), GENDER_FEMALE, [darknessMagicCombo, darkFlamme, darkBoomCast, quickCast, darkIce, dualCast],"\"Eye veut zuste un pi d'attenchions...\" - Shushi", [ELEMENT_DARKNESS, ELEMENT_FIRE], variant=True, icon='<:shihu:1243488051804639232>', bonusPoints=[MAGIE, STRENGTH], say=shihuSays,trait=[TRAIT_ARACHNOPHOBE]),
    tmpAllie("Clémence Exaltée", 2, 0x8F001C, ENCHANTEUR, clemExWeapon, [clemExStuff1, clemExStuff2, clemExStuff3], GENDER_FEMALE, [clemExSkill2, clemExSkill3, clemExSkill4, clemExSkill5, clemExSkill6, clemExBloodDemon, clemExBloodMissiles], "WIP, revenez plus tard", [ELEMENT_DARKNESS, ELEMENT_LIGHT], icon='<:clemence:908902579554111549>', bonusPoints=[MAGIE, STRENGTH], say=clemExSay, deadIcon='<:AliceOut:908756108045332570>',variant=True,splashIcon="<:clemenceEx:1088484359872450600>",splashArt="https://media.discordapp.net/attachments/640667220124499988/1088478369596838048/Sans_titre_60_20230323160331.png",team=NPC_DEMON, equippedChips=[getChip("Sur-Vie","Démolition","Dégâts reçus réduits","Lune de Sang","Goût du Sang")]),
    tmpAllie('Iliana prê.', 1, white, VIGILANT, iliWeap, [miniStuffHead, miniStuffDress, miniStuffFlats], GENDER_FEMALE, [iliPreSkill5, iliPreSkill4, iliPreSkill6, iliPreSkill1, iliPreSkill2, iliPreSkill3, iliPreSkill7], element=[ELEMENT_LIGHT, ELEMENT_LIGHT], deadIcon='<:oci:930481536564879370>', icon='<:Iliana:926425844056985640>', bonusPoints=[CHARISMA, ENDURANCE], description="Face à une menace dimensionnelle sans précédents, Iliana a décider de réveiller ses pouvoirs de Prêtresse de la Lumière pour faire équipe avec celle des Ténèbres",say=ilianaPreSays,variant=True,splashIcon='<:iliPre:1053017768443785236>', team=NPC_HOLY, trait=[TRAIT_CATGIRL] ,equippedChips=[getChip("Contre-Offensive","Retour de Bâton","Constitution II","Blocage augmenté","Soins et armures réalisés augmentés")]),
    tmpAllie('Belle', 2, 0x1f0004, ENCHANTEUR, magicSwordnShield, getStuffSet("Guerrier Mage Légendaire"), GENDER_FEMALE, [ferocite, spectralCircle, darkAmb, spectralFurie, magicRuneStrike, fizzbang, inMemoria], element=[ELEMENT_DARKNESS, ELEMENT_NEUTRAL], variant=True, icon='<:belle:943444751288528957>', bonusPoints=[ENDURANCE, MAGIE],team=NPC_UNDEAD,trait=[TRAIT_ARACHNOPHOBE]),
    tmpAllie("Luna prê.", 1, black, POIDS_PLUME, lunaWeap, [LunaPreStuffHead, LunaPreStuffDress, LunaPreStuffFlats], GENDER_FEMALE, [lunaDarkChoc,lunaPreSkill5_3,lunaPreSkill3,lunaPreSkill2,lunaSkill6,lunaPreUltimawashi], element=[ELEMENT_DARKNESS, ELEMENT_DARKNESS], icon='<:luna:909047362868105227>', bonusPoints=[STRENGTH, AGILITY], say=lunaPreSays,variant=True, description = "Face à une menace temporelle sans précédents, Luna a décidé de réveiller ses pouvoirs de Prêtresse des Ténèbres pour faire équipe avec celle de la Lumière", splashIcon='<:luna:1242920285577936896>'),
    tmpAllie("Chûri-Hinoro", 1, orange, ENCHANTEUR, phenixLeath, getStuffSet("Guerrier Mage Légendaire"), GENDER_FEMALE, churInoSkills, description="En utilisant la compétence \"Envolée du Phenix\", Chûri devient Chûri-Hinoro, modifiant son élément et ses compétences", element=[ELEMENT_FIRE,ELEMENT_EARTH],deadIcon="<:fairyOut:935335430814068786>",icon='<:churHi:994045813175111811>',bonusPoints=[MAGIE,PRECISION],say=churiSays,variant=True,splashIcon="<:churiHinoro:1088897850219450448>",splashArt="https://media.discordapp.net/attachments/640667220124499988/1084973960191549470/Sans_titre_49_20230313235816.png?width=490&height=676",team=NPC_FAIRY),
    tmpAllie("Lia Ex",2,0xBBFFCB,POIDS_PLUME, liaExWeap,[greenbutbar,greenbutterflyshirt,greenbutterflysandals],GENDER_FEMALE,[liaExSkill1,liaExSkill2,liaExSkill3,liaExSkill4,liaExUlt_1,liaExSkill6,liaExSkill7],description="Suite à l'émergeance d'une nouvelle menage, afin de protéger ses frères et soeurs et comme épreuve de sa mère, Lia a du mettre son masque de démon renard et se jeter corps et âme contre leur ennemi d'ombre",element=[ELEMENT_AIR,ELEMENT_AIR],deadIcon="<:kitsuSisterDead:908756093101015100>",icon="<:liaEx:1012669139711696928>",bonusPoints=[MAGIE,AGILITY],elemAffinity=True,splashIcon='<:liaEx:1079115890437656598>'),
    tmpAllie("Aurora",1,white, MAGE, dvinWand,getStuffSet("Mage écarlate Légendaire"), GENDER_FEMALE, [lightPillar], variant=True, icon="<:aurora:1100791091483136133>",element=[ELEMENT_LIGHT,ELEMENT_LIGHT]),
    tmpAllie("Victoire",1,white, MASCOTTE, enchantedShotgun,getStuffSet("Guerrier Mage Légendaire"),GENDER_FEMALE, [seraphStrike, miracle, comboVerMiracle, victoireTeleportBehindYou, angelStrike, fizzbang, bundleCaC], variant=True, icon="<:victoire:1203788632163360858>", element=[ELEMENT_LIGHT, ELEMENT_LIGHT], splashIcon="<:victoire:1235273325018746901>", team=NPC_ANGEL, bonusPoints=[MAGIE,CHARISMA,ENDURANCE], equippedChips=[getChip("Magie augmentée I","Crucifix","Rentre-Dedans","Agilité augmentée I","Bout-Portant")], charSettings=createCharSettingsDict(weaponUse=CHARSET_WEAPON_USE_LOW,dmgSkillUse=CHARSET_DMGSKILL_HIGH,buffSkillUse=CHARSET_BOOSTSKILL_HIGH),say=victoireSays, splashArt="https://media.discordapp.net/attachments/769956170081107978/1233106715373998151/Sans_titre_138_20240425192526.png"),
    tmpAllie("Alexandre",1,0x498877, BERSERK, bigHammer, getStuffSet("Plugiliste Légendaire"),GENDER_MALE, [seisme, fisure, earthUlt2, krystalisation, rockStomp, rockSpike, rockBlast], variant=True, icon="<:alexandre:1178570945368162405>", element=[ELEMENT_EARTH], bonusPoints=[STRENGTH,ENDURANCE,PRECISION], equippedChips=[getChip("Force augmentée I","Endurance augmenté I","Démolition","Blocage augmenté","Totem de Protection")], charSettings=createCharSettingsDict(weaponUse=CHARSET_WEAPON_USE_LOW,dmgSkillUse=CHARSET_DMGSKILL_HIGH,buffSkillUse=CHARSET_BOOSTSKILL_HIGH),say=alexandreSays),
    tmpAllie("Jade",1,0x87E990, IDOLE,flumWand, getStuffSet('Chanteur Légendaire'), GENDER_FEMALE, [astrodyn, echo, corGra, aurore, aliceDance, descart, thinkSkill], variant=True, icon="<:jade:1178453233442754701>", element=[ELEMENT_WATER], bonusPoints=[CHARISMA], equippedChips=[getChip("Charisme augmenté I","Spotlight","Aura Galvanisante")], charSettings=createCharSettingsDict(weaponUse=CHARSET_WEAPON_USE_LOW,buffSkillUse=CHARSET_BOOSTSKILL_HIGH),say=jadeSays),
    tmpAllie("Lia",2, 0xDAF7A6, POIDS_PLUME, airsword, getStuffSet("Assassin de l'Ombre Nocturne"), GENDER_FEMALE, [higanbana, hissatsu, ikishoten, senbonzakura, florChaot, Hauringusutomusodo], variant=True, icon="<:lia:1079017951098847283>", element=[ELEMENT_AIR, ELEMENT_AIR], bonusPoints=[AGILITY, STRENGTH, PRECISION], equippedChips=[getChip("Sourire Agile","Charisme augmenté I","Agilité augmentée I","Esquive augmentée","Réflex")], team=NPC_KITSUNE),
    tmpAllie("Lei",2, red, INOVATEUR, spellBook, getStuffSet("Barde Légendaire"), GENDER_FEMALE, [cuteFlame, objectOfObsession, contrainte, toxicon, nostalgia, nova, dosisBundle], variant=True, icon="<:lei:1257691823170785372>", element=[ELEMENT_FIRE,ELEMENT_FIRE], bonusPoints=[INTELLIGENCE, CHARISMA, MAGIE], equippedChips=[getChip("Intelligence augmentée I","Précision augmentée I","Esquive augmentée","Sourire Sadique","Spotlight")], team=NPC_KITSUNE),
    tmpAllie("Liz",2, red, MAGE, spellBook, getStuffSet("Mage écarlate Légendaire"), GENDER_FEMALE, [fireMagicCombo, pyroSparkle, pyroCalcinate, pyroBlast, fireCircle, infinitFire], variant=True, icon="<:liz:1079024673205014609>", element=[ELEMENT_FIRE, ELEMENT_FIRE], bonusPoints=[MAGIE, PRECISION, CHARISMA], equippedChips=[getChip("Magie augmentée I",'Dégâts universels augmentés',"Dégâts directs augmentés","Aura Galvanisante","Sourire Sadique")], team=NPC_KITSUNE),
    tmpAllie("Liu",2, orange, TETE_BRULEE, bigHammer, getStuffSet("Plugiliste Légendaire"), GENDER_FEMALE, [findSkill("Combo Frappes Rocheuses"), seisme, fisure, elipseTerrestre, hearthFrac, findSkill("Conviction du Tête Brulée"), findSkill("Défi")], variant=True, icon="<:liu:1079013404804665484>", element=[ELEMENT_EARTH, ELEMENT_EARTH], bonusPoints=[STRENGTH, ENDURANCE, CHARISMA], equippedChips=[getChip("Sourire Mazo","Dégâts reçus réduits","Blocage augmenté","Présence","Constitution I")], team=NPC_KITSUNE),
    tmpAllie("Lio",2, blue, ALTRUISTE, flumWand, getStuffSet("Soigneur Légendaire"), GENDER_FEMALE, [revif, bundleOffr, cure2Bundle, revitalisation, guardianAngel, altOH, asile], variant=True, icon="<:lio:1079030249213394996>", element=[ELEMENT_WATER, ELEMENT_WATER], equippedChips=[getChip("Charisme augmenté I","Soins augmentés I","Soins et armures réalisés augmentés","Sourire Bienveillant","Transgression")], team=NPC_KITSUNE, bonusPoints=[CHARISMA, PRECISION])
    ]

# FindAllies
def findAllie(name: str) -> tmpAllie:
    for a in tablAllAllies+tablVarAllies:
        if a.name == name:
            return a
    return None

clemExKillReact = [
    "Celui qui t'as dit que frapper comme un bourrin suffirait s'est moqué de toi",
    "Observe donc ça {target}.",
    "Oups, tu aurais mieux fait de chercher à ne pas te faire souffler par ce sort là",
    "J't'ai suffisament vu comme ça {target}.",
    "Tiens donc, tu avais pas prévu ça manifestement",
    "Et si tu écoutais les autres la prochaine fois ?",
    "Ça c'est la vrai magie.",
    "À trop vouloir aider les autres ont fini par se perdre de vu, {target}.",
    "Garde tes enchantements de bas étages pour quelqu'un d'autre, tu veux ?",
    "Ça se dit protecteur mais ça sait même pas se protéger soi-même.",
    "Tu as manqué de vigilance il semblerais",
    "Tu appellelais ça des sorts {target} ? *Ça* c'était un vrai sort",
    "Oh, est-ce que j'ai mis un stop à tes projets ?",
    "J'espère que tu en as pris de la graine.",
    "Quel piètre mascotte tu fais..."
    "C'est tout {target} ?"
]

findAllie("Iliana prê.").standAlone = findAllie("Lia Ex").standAlone = findAllie("Clémence Exaltée").standAlone = findAllie("Luna prê.").standAlone = True
# Balancing

def simulAdapTempStats(name:str):
    try:
        procurData = procurTempStuff[name]
        ent = copy.deepcopy(findAllie(name))
        ent.changeLevel(MAXLEVEL)
        ent.stuff = [
            stuff(procurData[1][0],procurData[1][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[1][2]),
            stuff(procurData[2][0],procurData[2][1],1,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[2][2]),
            stuff(procurData[3][0],procurData[3][1],0,0,int(procurData[4][0][0]*procurData[4][0][1]*ent.level),int(procurData[4][1][0]*procurData[4][1][1]*ent.level),int(procurData[4][2][0]*procurData[4][2][1]*ent.level),int(procurData[4][3][0]*procurData[4][3][1]*ent.level),int(procurData[4][4][0]*procurData[4][4][1]*ent.level),int(procurData[4][5][0]*procurData[4][5][1]*ent.level),int(procurData[4][6][0]*procurData[4][6][1]*ent.level),int(procurData[4][7][0]*procurData[4][7][1]*ent.level),int(procurData[4][8][0]*procurData[4][8][1]*ent.level),int(procurData[4][9][0]*procurData[4][9][1]*ent.level),emoji=procurData[3][2])
        ]

        baseStats = {STRENGTH:ent.strength,ENDURANCE:ent.endurance,CHARISMA:ent.charisma,AGILITY:ent.agility,PRECISION:ent.precision,INTELLIGENCE:ent.intelligence,MAGIE:ent.magie,RESISTANCE:ent.resistance,PERCING:ent.percing,CRITICAL:ent.critical}
        for obj in [ent.weapon,ent.stuff[0],ent.stuff[1],ent.stuff[2]]:
            valueElem = 1
            if obj.affinity == ent.element :
                valueElem = 1.1
            
            baseStats[0] += int(obj.strength*valueElem)
            baseStats[1] += int(obj.endurance*valueElem)
            baseStats[2] += int(obj.charisma*valueElem)
            baseStats[3] += int(obj.agility*valueElem)
            baseStats[4] += int(obj.precision*valueElem)
            baseStats[5] += int(obj.intelligence*valueElem)
            baseStats[6] += int(obj.magie*valueElem)
            baseStats[7] += int(obj.resistance*valueElem)
            baseStats[8] += int(obj.percing*valueElem)
            baseStats[9] += int(obj.critical*valueElem)

        toPrint = "{0} (lvl {1}) :".format(name,ent.level)
        for statName, statValue in baseStats.items():
            if statName <= CRITICAL:
                toPrint += "\n{0} : {1}".format(allStatsNames[statName],statValue)

        toPrint += "\nPVs estimés : {0}".format(round((130+ent.level*15)*((baseStats[ENDURANCE])/100+1)))

        tempRes = 0
        tRes = tempRes+baseStats[RESISTANCE]
        t1 = max(0,tRes - 100)
        t2 = min(max(0,tRes - 40),60)
        t3 = min(tRes,40)

        tempRes = int(t3 + t2//3 + t1//5)
        toPrint += "\nRésistance estimée : {0}".format(tempRes)
        print(toPrint)
    except:
        print_exc()

PROBLENAMSG = 15

lenaReactTmpDeath = {
    "Clémence":"Hé bah alors Clémence ? Fatiguée aujourd'hui ?\"\n<:clemence:908902579554111549> : \"Oh la ferme toi.",
    "Alice":"`Soupir`Je t'ai déjà dit d'essayer de ne pas trop te de perdre de vue en combat Alice",
    "Ly":"Faute d'inatention ?",
    "Amary":"Petite fleur partie trop tôt",
    "Edelweiss":"Elle devrait plus se concentrer sur elle même plutôt que supporter pour les autres..."
}

#simulAdapTempStats("Iliana prê.")

if datetime.now(parisTimeZone).month == 9:
    for cmpt in range(len(tablAllAllies)):
        if tablAllAllies[cmpt].isNpc("Félicité"):
            tablVarAllies.append(tablAllAllies[cmpt])
            tablAllAllies.remove(tablAllAllies[cmpt])
            break

iliLightCombo = copy.deepcopy(lightPillar)
iliLightCombo.become[0].use = iliLightCombo.become[1].use = iliLightCombo.become[2].use = iliLightCombo.use = CHARISMA

shehisaReactAttackMyrlope = ["Hé !","Myrlopé !","Pas si vite.","J'te permet pas !","Fiche lui la paix !","Arrête ça !"]
aliceReactSpider = [
    "!!??",
    "!?",
    "Huh !",
    "Que !?",
    "Hii !"
]
heleneReactMyrlope = [
    "Mmmmg...",
    "Est-ce que tu... Pourrais aller voir ailleurs s'il te plaît ?",
    "Tss...",
    "Zou.",
    "`Soupire`"
]

findAllie("Alice").changeDict = [
    tempAltBuild(35, skills=[aliceDance, courage, charmingPandant, holyVoice, onStage, corGra, inconsCollect],splashIcon='<:alice:1183197636153577482>',chips=[getChip("Spotlight","Aura Galvanisante","Charisme augmenté I","Charisme augmenté II","Sur-Vie")],buildName="En scène !", buildIcon = onStage.emoji),
    tempAltBuild(20, POIDS_PLUME, aliceFan, getStuffSet("Assassin de l'Ombre Nocturne"), [finalTech,swordDance,aliceFanDanse,fanRevol,danseStarFall,tangoEnd,fanVirBundle],[ELEMENT_SPACE,ELEMENT_SPACE],[AGILITY,CHARISMA], buildName="Danse des éventails", buildIcon="<:celestianFans:1003313557242388622>"),
    tempAltBuild(20, stuffs= getStuffSet("Tireur Charismatique") ,skills=[mageBalad, martialPean, vanderManuet, apexArrow, heroicFantasy, blastArrow, courage],splashIcon='<:alice:1183197636153577482>',bonusPoints=[STRENGTH,CHARISMA],aspiration=OBSERVATEUR, buildName="Barde", buildIcon="<:voixDivine:1085991767834370108>"),
    tempAltBuild(0, IDOLE, stuffs=aliceExStuff, skills=[aliceSongBundle,aliceSkill2,aliceSkill3], weap=aliceExWeap, elements=[ELEMENT_SPACE,ELEMENT_LIGHT], chips=[getChip("Spotlight","Médaille de la Chauve-Souris")])
    ]
findAllie("Hélène").changeDict = [
    tempAltBuild(20,SORCELER,butterflyP,getStuffSet("Mage Ultraviolet Légendaire"),[infectFiole,epidemic,intox,funDraw,propaUltLaunch,infDraw,quadFleau],[ELEMENT_DARKNESS,ELEMENT_LIGHT],[MAGIE,INTELLIGENCE]),
    tempAltBuild(35,weap=whiteSpiritWings,skills=[propagPas,lightHeal2,lightShot,lapSkill,invocFee,sumLightButterfly,shareMark],elements=[ELEMENT_LIGHT,ELEMENT_WATER])
    ]
findAllie("Amary").changeDict = [
    tempAltBuild(25,ALTRUISTE,stuffs=getStuffSet("Soigneur Légendaire"),skills=[mend,lifeSeed,lillyTransform,healingField,roseeHeal,renisurection,asile],elements=[ELEMENT_LIGHT,ELEMENT_WATER],bonusPoints=[CHARISMA,PRECISION]),
    tempAltBuild(25,ALTRUISTE,stuffs=getStuffSet("Soigneur Légendaire"),skills=[bundleOffr,tetragramme,renisurection,asile,healingField,misery,temperance],elements=[ELEMENT_LIGHT,ELEMENT_WATER],bonusPoints=[CHARISMA,PRECISION])]
findAllie("Shehisa").changeDict = [
    tempAltBuild(20,ATTENTIF,stuffs=getStuffSet("Stratège Légendaire"), skills=[focus, smnMyrlope, bleedingPuit, hemoBomb, ShiUltimate, denoument, trappedField], elements=[ELEMENT_DARKNESS,ELEMENT_DARKNESS],bonusPoints=[STRENGTH, INTELLIGENCE, AGILITY], chips=[getChip("Force augmentée I","Esquive augmentée","Achèvement","Héritage Lesath","Dissimulation")]),
    tempAltBuild(20,skills=[ombralStrike,dreamInADream,smnMyrlope,trickAttack,assasinate,redrum,bundleSurpriseJump]),
    tempAltBuild(20,skills=[trickAttack, seitonTenchu, deathPercing, smnMyrlope, echecEtMat, ripping, weakPoint]),
    tempAltBuild(20,aspiration=POIDS_PLUME,skills=[deathSentenceBundle,bleedingStrikeBundle,traumatismeBundle,smnMyrlope,UmbralTravel])
]
findAllie("Julie").changeDict = [
    tempAltBuild(20,SORCELER,magicWood,stuffs=findAllie("Lohica").stuff,skills=[dephaIncant,ice2,lizSKillSus,clock,hourglass,magAchSkill,fairyTraqnard],elements=[ELEMENT_TIME,ELEMENT_DARKNESS],bonusPoints=[MAGIE,INTELLIGENCE]),
    tempAltBuild(30,skills=[rajeunissement,healingTimebomb,inconsCollect,julieUlt,extraMedica,extraEting,vampirisme2]),
    tempAltBuild(25,POIDS_PLUME,eclatanaDoto,stuffs=getStuffSet("Assassin Mage Légendaire"),skills=[periodStrike,descynNeg,quartzArcane,timeMagicCombo,timeRip,counterTime],chips=[getChip("Magie augmentée I","Esquive augmentée","Réflex","Barrière","Agilité augmentée I")],bonusPoints=[MAGIE,AGILITY,ENDURANCE])
    ]
findAllie("Gwendoline").changeDict = [
    tempAltBuild(30,POIDS_PLUME,mainLibre,stuffs=getStuffSet("Assassin de l'Ombre Nocturne"),skills=[elipseTerrestre,piedVolt,earthStrike,hearthFrac,ebranlement,retourneImpactant]),
    tempAltBuild(30,POIDS_PLUME,mainLibre,stuffs=getStuffSet("Assassin de l'Ombre Nocturne"),skills=[defi,earthStrike,justiceEnigma,physEffGiver,erodStrike,gwenyStrike]),
    tempAltBuild(0,PROTECTEUR,gwenyWeap,stuffs=gwenyExStuff,skills=gwenyExSkillList)
]
findAllie("Klironovia").changeDict = [
    tempAltBuild(50,weap=mainLibre,stuffs=getStuffSet("Assassin de l'Ombre Nocturne"),skills=[fracas,piedVolt,revolutionFracas,plongeFracas,pentastrike,uppercut,retourneImpactant]),
    tempAltBuild(0,BERSERK,kliWeap,stuffs=klikliExStuff,skills=klikliExSkillList)
]
findAllie("Altikia").changeDict = [
    tempAltBuild(0,VIGILANT,altyWeap,stuffs=altyExStuff,skills=altyExSkillList)
]
findAllie("Lily").changeDict = [
    tempAltBuild(20,PREVOYANT,epiphyllum,stuffs=findAllie("Epiphyllum").stuff,skills=[demonArmor,demonArmor2,dmonReconstitution,dmonReconstitution2,demonConst,inkarmor,firstArmor],bonusPoints=[INTELLIGENCE,PRECISION]),
    tempAltBuild(20,INOVATEUR,luth,skills=[prettySmile,aeraCharm,corruptusArea,infirm,toxicon,findSkill("Blocage Démoniaque"),findSkill("DistribuCool")]),
    tempAltBuild(20,MAGE,magicWood,stuffs=getStuffSet("Mage écarlate Légendaire"),skills=[demonSpell1,demonMissile,comboVerBrasier,sterialSoil,magicMissile,dualEnergyDrain,daemoniumTerraeMotus],bonusPoints=[MAGIE,PRECISION,ENDURANCE],chips=[getChip("Aura Galvanisante","Démaniaque","Démolition","Absorbtion","Magie augmentée I")]),
    tempAltBuild(20, aspiration=MASCOTTE, weap=magicSword, stuffs=getStuffSet("Paladin étoilé"), skills=[aeraCharm, charmingPandant, prettySmile, trouble, rivCel, entraide, transfert], chips=[getChip("Sourire Mazo","Démaniaque","Soins augmentés I","Sourire Bienveillant","Charisme augmenté I")])
    ]

findAllie("Sixtine").changeDict = [
    tempAltBuild(30, stuffs=getStuffSet('Sage'), skills=[stigmate,dissonance,vibrSon,enhardissement,sernade,manafication,descart], bonusPoints=[MAGIE,CHARISMA], aspiration=MAGE,icon="<:dreamSixtine:1100793996483235851>",buildName="Barde Onirique", buildIcon='<:sixtineSkill2:1205624341488865290>'),
    tempAltBuild(20, aspiration=ENCHANTEUR,weap=dSixtineWeap,stuffs=getStuffSet("Assassin Mage Légendaire"),skills=[ferocite,spaceCrush,spacePulse,hexadecaComb,findSkill("Percée du Capricorne"),findSkill("Frappe Runique")],elements=[ELEMENT_SPACE,ELEMENT_DARKNESS],bonusPoints=[MAGIE,ENDURANCE],icon='<:dreamSixtine:1100793996483235851>', buildName = "Escrimeuse Onirique", buildIcon="<:dreamSixtine:1100793996483235851>"),
    tempAltBuild(0, weap=sixtineWeap, aspiration=INOVATEUR,stuffs=[sixtineStuff1,sixtineStuff2,sixtineStuff3],skills=[sixtineSkill1,sixtineSkill2,sixtineSkill3,sixtineSkill4,sixtineSkill5 ],elements=[ELEMENT_SPACE,ELEMENT_LIGHT],bonusPoints=[INTELLIGENCE,MAGIE])
    ]
findAllie("Icealia").changeDict = [
    tempAltBuild(40,PROTECTEUR,icealiaShield,stuffs=getStuffSet("Paladin Nocturne"),skills=[royaleGardeSkill,snowFall,findSkill("Onde"),findSkill("Aura Armurière"),findSkill("Orbe défensif"),royalShield,findSkill("Inconscient collectif")],bonusPoints=[ENDURANCE,INTELLIGENCE],elements=[ELEMENT_LIGHT,ELEMENT_WATER]),
    tempAltBuild(25,MASCOTTE,constShield,stuffs=getStuffSet("Guerrier Mage Légendaire"),skills=[royaleGardeSkill,bastion,orage,magma,findSkill("Teliki Anakatéfthynsi"),findSkill("Coeur de Lumière"),findSkill("Inconscient collectif")],bonusPoints=[ENDURANCE,INTELLIGENCE],elements=[ELEMENT_LIGHT,ELEMENT_WATER])
    ]
findAllie("Bénédicte").changeDict = [
    tempAltBuild(20,IDOLE,dvinWand,skills=[findSkill("Terre Sacrée Étendue"),findSkill("Guide Divin"),findSkill("Equilibre de la Balance"),findSkill("Astrodynamie"),findSkill("Lotus Pourpre"),findSkill("Manafication"),findSkill("Eruption Solaire")],bonusPoints=[CHARISMA,MAGIE],elements=[ELEMENT_SPACE,ELEMENT_DARKNESS]),
    tempAltBuild(20,ALTRUISTE,dvinWand,stuffs=findAllie("Elina").stuff,skills=[findSkill("Constitution Divine"),findSkill("Bénédiction Avancée"),findSkill("Purification"),findSkill("Extra Medica"),findSkill("Pulsation Vitale"),findSkill("Offrande de Misère")],elements=[ELEMENT_LIGHT,ELEMENT_FIRE]),
    tempAltBuild(20,MASCOTTE,sacredSword,stuffs=getStuffSet("Paladin étoilé"),skills=[findSkill("Volontée de Fer"),findSkill("Frappe Séraphique"),findSkill("Miracle"),findSkill("Invincible"),findSkill('Rivière Céleste'),findSkill('ssj'),findSkill('Bénidiction de la Vièrge')],elements=[ELEMENT_SPACE,ELEMENT_FIRE],bonusPoints=[CHARISMA,MAGIE,ENDURANCE])
]
findAllie("Lena").changeDict = [
    tempAltBuild(30,OBSERVATEUR,splatcharger,skills=[findSkill("Flèche Gelante"),findSkill("Flèche Givrante"),findSkill("Flèche de glace"),findSkill("Aqua ferrum"),findSkill("Tir Parfait"),rapidFire,findSkill("Tir Critique")],splashIcon='<:lena:1177723779548446842>'),
    tempAltBuild(30,OBSERVATEUR,splatcharger,skills=[comboHeatedCleanShot,leadShot,dismantle,exploShot,dechargeGausseSolo,findSkill("Tir Parfait"),sagArrow]),
    tempAltBuild(0,weap=lenaExWeapon,stuffs=[lenaExStuff1,lenaExStuff2,lenaExStuff3], skills=[lenaExSkill1,lenaExSkill2,lenaExSkill3,lenaExSkill4,lenaExSkill5,lenaExSkill6],buildName="Main Crew Fight", buildIcon="<:lenaRailgun:1209368562750201886>")
]
findAllie("Ly").changeDict = [
    tempAltBuild(20,OBSERVATEUR,stuffs=getStuffSet("Sniper Légendaire"), skills=[findSkill("Tir Feu"),findSkill("Pyro-Hypercharge"),findSkill("Flèche d'Immolation"),findSkill("Barrage"),findSkill("Flèche Explosive"),findSkill("Flèche emflammée"),tactician],elements=[ELEMENT_FIRE,ELEMENT_SPACE]),
    tempAltBuild(30,skills=[lanceTox,lanceTox2,lanceTox3,machDeFer,morsTempSkill,morsCaudiqueSkill,ultraSignal]),
    tempAltBuild(20,OBSERVATEUR,stuffs=getStuffSet("Sniper Légendaire"), skills=[cribArrow, rapidFire, rayoArrow, destrucArrow, holyShot, quickShot, cherchArrow], chips=[getChip("Force augmentée I","Dégâts universels augmentés","Friable","Diffraction","Démolition")])
]
findAllie("Astra").changeDict = [
    tempAltBuild(50,VIGILANT,constShield,stuffs=findAllie("Iliana").stuff,skills=[ironWillSkill,astraRegenPhase,astraIncurStrike,astraRegenEarth,findSkill("Medicamentum"),extraEting,propagPas],bonusPoints=[CHARISMA,ENDURANCE])
]
findAllie("Ruby").changeDict = [
    tempAltBuild(int(100/12),weap=fireMetRuneLong,skills=[fireMagicCombo,pyroSparkle,findSkill("Flammes infernales"),pyroBlast,findSkill("Brasier"),magicBarrier],elements=[ELEMENT_FIRE,ELEMENT_SPACE]),
    tempAltBuild(int(100/12),weap=waterMetRuneLong,skills=[waterMagicCombo,bouncingWater,findSkill("Geyser"),waterBlast,findSkill("Pluie Glacée"),magicBarrier],elements=[ELEMENT_WATER,ELEMENT_SPACE]),
    tempAltBuild(int(100/12),aspiration=ENCHANTEUR,stuffs=getStuffSet("Assassin Mage Légendaire"),weap=airMetRuneMel,skills=[airMagicCombo,windBlast,findSkill("Sillage"),windCutter,findSkill("Tempête Jupiterrienne"),magicBarrier],elements=[ELEMENT_AIR,ELEMENT_SPACE],bonusPoints=[AGILITY,MAGIE,PRECISION], chips=[getChip("Magie augmentée I","Agilité augmentée I","Esquive augmentée","Vampirisme I","Réflex")]),
    tempAltBuild(int(100/12),aspiration=ENCHANTEUR,stuffs=getStuffSet("Assassin Mage Légendaire"),weap=earthMetRuneMel,skills=[earthMagicCombo,rockStomp,findSkill("Casse-Montagne"),rockBlast,findSkill("Déchirure Tectonique"),magicBarrier],elements=[ELEMENT_EARTH,ELEMENT_SPACE],bonusPoints=[AGILITY,MAGIE,PRECISION], chips=[getChip("Magie augmentée I","Agilité augmentée I","Esquive augmentée","Vampirisme I","Réflex")]),
    tempAltBuild(int(100/12),weap=darkMetRuneLong,skills=[darknessMagicCombo,darkThunder,darkFlamme,innerdarkness,darkElemUse,magicBarrier],elements=[ELEMENT_DARKNESS,ELEMENT_SPACE]),
    tempAltBuild(int(100/12),weap=lightMetRuneLong,skills=[lightMagicCombo,lightPillar,eternalLight,dualSupp,demonMissile,magicMissile,magicBarrier],elements=[ELEMENT_LIGHT,ELEMENT_SPACE]),
    tempAltBuild(int(100/12),aspiration=ENCHANTEUR,stuffs=getStuffSet("Assassin Mage Légendaire"),weap=timeMetRuneMid,skills=[timeMagicCombo,accelerant,descynNeg,counterTime,timeRip,timeBomb,magicBarrier],elements=[ELEMENT_TIME,ELEMENT_SPACE],bonusPoints=[AGILITY,MAGIE,PRECISION], chips=[getChip("Magie augmentée I","Agilité augmentée I","Esquive augmentée","Vampirisme II","Réflex")]),
]
findAllie("Clémence").changeDict = [
    tempAltBuild(50,aspiration=MAGE,skills=[sanguisGladio,sanguisGladio2,bloodDemonBundle,findSkill("Umbra Mortis"),findSkill("Ultima Sanguis Pluviae"),magicRune,findSkill("Anticipation")],weap=findWeapon("Baguette en argent")),
    tempAltBuild(0,aspiration=MAGE,weap=clemTmpWeap,stuffs=clemTmpStuff,skills=[clemTmpSkill3,clemTmpSkill1,clemTmpSkill2,clemTmpSkill4,clemTmpSkill5],chips=[getChip("Goût du Sang","Lune de Sang","Magie augmentée II","Sur-Vie","Convertion Vitale")])
]
findAllie("Powehi").changeDict = [tempAltBuild(35, aspiration=ENCHANTEUR,stuffs=getStuffSet("Guerrier Mage Légendaire"),skills=[findSkill("Trou Noir"),vibrSon,spaceMagicCombo,findSkill("Trou noir Avancé"),gravPulse,findSkill("Combo Confiteor"),findSkill("Conviction de l'Enchanteur")])]
findAllie("Luna").changeDict = [tempAltBuild(50, skills=[findSkill("Foulée Légère"),findSkill("Danse du Phénix"),findSkill("Pied Voltige"),expultion,findSkill("Triple Impact"),findSkill("Frappe Convertissante"),findSkill("Envolée féérique")])]
findAllie("Lohica").changeDict = [tempAltBuild(50, skills=[findSkill("Focalisation"),findSkill("Intraveineuse"),findSkill("Propagation"),fairyRay,findSkill("Propagation Avancée"),exploMark],weap=butterflyP)]
findAllie("Chûri").changeDict = [tempAltBuild(50, aspiration=ENCHANTEUR, skills=[galvanisation,fireCircle,inMemoria,darkSweetHeat,phenixRevive,summonHinoro,fireMagicCombo],elements=[ELEMENT_FIRE,ELEMENT_FIRE])]
findAllie("Iliana").changeDict = [
    tempAltBuild(50,skills=[ironWillSkill,holyShieltron,convictionVigilante,altyQCombo,inspiration,lightAura,iliLightCombo]),
    tempAltBuild(0,weap=iliTmpWeap,stuffs=iliTmpStuff,skills=[iliTmpSkill1,iliTmpSkill2,iliTmpSkill3,iliTmpSkill4,iliTmpSkill5,iliTmpSkill6],chips=[getChip("Blocage augmenté","Constitution II","Bouclier d'épines","Barrière","Bouclier Sacrificiel")])
]
findAllie("Céleste").changeDict = [tempAltBuild(35,aspiration=BERSERK,stuffs=getStuffSet("Plugiliste Légendaire"),skills=[defi,drkCombo,meditate,fireflyUlt,chiStrike,bloodPact,physicRune])]
lenaShuRedirect = effect("Protection Maternelle","materProtect",redirection=100,unclearable=True,turnInit=-1,emoji='<:analyse:1003645750225412257>')
findAllie("Shushi").changeDict = [tempAltBuild(0,weap=shushiWeapon,stuffs=[shushiStuff1,shushiStuff2,shushiStuff3],skills=[shushiSkill1,shushiSkill2,shushiSkill3],chips=[getChip("Dégâts indirects reçus réduits","Esquive augmentée","Totem de Protection","Barrière","Présence")])]
findAllie("Félicité").changeDict = [
    tempAltBuild(10,skills=[firePhysCombo,ironStormBundle,trancheCombo,hissatsu,higanbana,fragmentation,strengthOfWillCast], buildName=elemNames[1], buildIcon = elemEmojis[1]),
    tempAltBuild(10,skills=[waterPhysCombo,ironStormBundle,trancheCombo,meditate,brotherHood,fragmentation,strengthOfWillCast], buildName=elemNames[2], buildIcon = elemEmojis[2]),
    tempAltBuild(10,skills=[airPhysCombo,ironStormBundle,trancheCombo,hissatsu,higanbana,fragmentation,strengthOfWillCast], buildName=elemNames[3], buildIcon = elemEmojis[3]),
    tempAltBuild(10,skills=[earthPhysCombo,ironStormBundle,trancheCombo,meditate,brotherHood,fragmentation,strengthOfWillCast], buildName=elemNames[4], buildIcon = elemEmojis[4]),
    tempAltBuild(10,skills=[lightPhysCombo,ironStormBundle,trancheCombo,hissatsu,higanbana,fragmentation,strengthOfWillCast], buildName=elemNames[5], buildIcon = elemEmojis[5]),
    tempAltBuild(10,skills=[darknessPhysCombo,ironStormBundle,trancheCombo,meditate,brotherHood,fragmentation,strengthOfWillCast], buildName=elemNames[6], buildIcon = elemEmojis[6]),
    tempAltBuild(10,skills=[spacePhysCombo,ironStormBundle,trancheCombo,meditate,brotherHood,fragmentation,strengthOfWillCast], buildName=elemNames[7], buildIcon = elemEmojis[7]),
    tempAltBuild(10,skills=[timePhysCombo,ironStormBundle,drkCombo,trancheCombo,higanbana,fragmentation,ikishoten], buildName=elemNames[8], buildIcon = elemEmojis[8]),
    tempAltBuild(0,weap=tmpFeliWeap,skills=[tmpFeliSkill1,tmpFeliSkill2,tmpFeliSkill3], buildName="Main Crew Procur", buildIcon = "<:felicite:1116861426556997653>")
]
findAllie("Elina").changeDict = [tempAltBuild(40,stuffs=getStuffSet('Infirmier Prévoyant'),skills=[adrenaline,pepsis,matriceShield,onde,armaturaMetrica,lightElemUse,vaccin], bonusPoints=[INTELLIGENCE, PRECISION], chips=[getChip("Précision augmentée I","Critique universel","Intelligence augmentée I",'Soins et armures réalisés augmentés',"Précision Chirurgicale")],buildName="Hybride Armure",buildIcon = adrenaline.emoji)]
