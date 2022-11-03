from traceback import print_exc
from classes import *
from constantes import *
from advObjects.advWeapons import *
from advObjects.advSkills import *
from advObjects.advStuffs import *
from advObjects.advInvocs import *
from advObjects.advEffects import *


lohicaFocal = copy.deepcopy(focal)
lohicaFocal.say = "Vous commencez sérieusement à me tapez sur les nerfs..."

aliceCheating = copy.deepcopy(vampirisme2)
aliceCheating.name, aliceCheating.group, aliceCheating.maxHpCost, aliceCheating.hpCost = aliceCheating.name + " (Alice)", SKILL_GROUP_HOLY, 10, 0

# Alliés temporaires =============================================================================
tablAllAllies = [
    tmpAllie("Lena", 1, light_blue, OBSERVATEUR, splatcharger, [amethystEarRings, lightBlueJacket, lightBlueFlats], GENDER_FEMALE, [waterlame, mysticShot, elemArrowSkill[ELEMENT_WATER], cryoChargeBundle, doubleShot, waterShot, preciseShot],"Une inkling qui en a vu des vertes et des pas murs.\nPréfère rester loin de la mêlée et abattre ses ennemis à bonne distance", [ELEMENT_WATER, ELEMENT_NEUTRAL], icon='<:lena:909047343876288552>', bonusPoints=[STRENGTH, PRECISION], say=lenaSays,birthday=(19,1),limitBreaks=[[STRENGTH,PRECISION],5],charSettings=preDefCharSet[0][1][3][2]),
    tmpAllie("Gwendoline", 2, 0xFFFF6B, TETE_BRULE, mainLibre, [butterflyEarRingsDark, darkChemVeste, darkButterFlyBoots], GENDER_FEMALE, [defi,earthStrike,elemArrowSkill[ELEMENT_EARTH],physEffGiver,erodStrike,demolish,gwenyStrike],"Bien qu'elle essaye de l'éviter, cette jeune femme se retrouve toujours à devoir en venir aux mains pour se débarraser des gros lourds de la première ligne ennemie.\nIl est vrai aussi qu'elle n'est pas toute seule dans sa tête", [ELEMENT_EARTH, ELEMENT_DARKNESS], bonusPoints=[STRENGTH, ENDURANCE], icon='<:gweny:906303014665617478>', say=gwenySays, birthday=(9,9)),
    tmpAllie("Clémence", 2, 0x8F001C, MAGE, rapiere, [critIndHat45, critIndBody45, critIndShoes45], GENDER_FEMALE, [cwUlt, sanguisGladio2, cwFocus, magiaHeal, sanguisGladio, quadFleau], "Clémence est née orpheline, ses parents ayant été tués par des chasseresses d'Arthémis peut après sa naissance.\nElle fût donc élevée par des chauve-souris dans une grotte pendant une bonne partie de son enfance\nCependant, elle rencontra dans un lieu nommé la \"Ville Onirique\", une ville magique accessible via les rêves permettant aux vampires vivants comme mort de s'y retrouver, une jeune vampire majeure du nom de Ruby.\nCette dernière lui apprit les bases de la magie au fils des années, ainsi que celles des sociétés humaines que les chauve-souris pouvaient évidamment pas lui apprendre.\n\nMalgré tout, elle manquait d'amis vampire \"réels\", Ruby habitant à des centaines de kilomètres dans la réalité. Elle alla donc, par une belle soirée d'Haloween, mordre une jeune femme envers laquelle Clémence avait un bon sentiment.\nOn peut dire que sur tous les choix qu'elle a fait, ça allait être celui qui allait être le plus lourd en conséquence, dans de bons comme mauvais thermes.\n\nJe vous en passe et des meilleurs, sinon je vais casser la limite de caractères, mais en grandissant, Clémence a continué son apprentissage de la magie et a décidé de parcourir le monde pour étudier les Anciennes Runes ainsi que pour purifier les artéfacts maudits qui tourmentent les monstres pour éviter qu'ils se fassent chasser par les humains, tel ses parents biologiques", [ELEMENT_DARKNESS, ELEMENT_DARKNESS], icon='<:clemence:908902579554111549>', bonusPoints=[MAGIE, INTELLIGENCE], say=clemSays, deadIcon='<:AliceOut:908756108045332570>',birthday=(31,10),limitBreaks=[[MAGIE],10],charSettings=preDefCharSet[0][1][1][2]),
    tmpAllie("Alice", 1, aliceColor, IDOLE, micPink, [butterflyPendantPink, pinkChemVeste, pompomShoes], GENDER_FEMALE, [aliceDance, courage, partner, aliceCheating, onstage, corGraCast, finalFloral], "Alice est la petite dernière des trois sœurs Kohishu, et la seule à être une vampire\n\nDès son plus jeune âge, elle a fortement démontré sa volontée à vouloir être le centre de l'attention, bien que ça ai frustrée sa sœur ainée. En grandissant, cette envie de reconnaissance ne s'est pas vraiment tarie, et a réussi grâce à son charme naturel à devenir rapidement une fille populaire\n\nElle décida de suivre la voie de sa mère et de devenir une chanteuse renommé, c'est ainsi qu'elle participa au concours de jeune talent de son école et réussi à se faire remarquer par une maison de disque qui recherchait de jeunes chanteurs\n\nLorsqu'elle n'est pas retenue par ses obligations, elle aime bien accompagner Félicité et Clémence dans leurs aventures, mais refuse de participer activement aux combats. À la place elle les encourages avec ses chansons légèrement magiques", [ELEMENT_LIGHT, ELEMENT_AIR], icon='<:alice:908902054959939664>', bonusPoints=[CHARISMA, INTELLIGENCE], say=aliceSays, deadIcon='<:AliceOut:908756108045332570>',birthday=(14,6),limitBreaks=[[CHARISMA],10],charSettings=preDefCharSet[2][1][1][2]),
    tmpAllie("Shushi", 1, 0x0303D5, ENCHANTEUR, airspell, [tankmage3, tankmage2, tankmage1], GENDER_FEMALE, [storm2, ferocite, invocCarbT, lbRdmCast, supprZone, magicRuneStrike, magicEffGiver],"Jeune inkling pas très douée pour le combat, à la place elle essaye de gagner du temps pour permettre à ses alliés d'éliminer l'équipe adverse", [ELEMENT_AIR, ELEMENT_SPACE], icon='<:shushi:909047653524963328>', bonusPoints=[MAGIE, ENDURANCE], say=shushiSays,birthday=(26,9),charSettings=preDefCharSet[0][1][2][2]),
    tmpAllie("Lohica", 1, purple, SORCELER, secretum, [darFlumOr, corruptPurpleVeste, corruptPurpleBoots], GENDER_FEMALE, [lohicaFocal, poisonus, poisonusPuit, propag, lohicaUltCast, lohicaBrouillad, fairyBomb],"Une fée à l'histoire bien mouvementée. Spécialisée dans les poisons", [ELEMENT_DARKNESS, ELEMENT_WATER], bonusPoints=[MAGIE, INTELLIGENCE], icon='<:lohica:919863918166417448>', deadIcon='<:flowernt:894550324705120266>'),
    tmpAllie("Hélène", 2, white, ALTRUISTE, whiteSpiritWings, [butterflyEarRingsWhite, whiteChemVeste, whiteButterFlyBoots], GENDER_FEMALE, [megaLight3, lapSkill, renisurection, fairyGarde, sumLightButterfly, lightShot, lightHeal2],"Une fée qui estime qu'essayer de sauver la vie de ses alliés est plus efficace que si elle esseyait de terminer le combat elle-même", [ELEMENT_LIGHT, ELEMENT_FIRE], bonusPoints=[CHARISMA, INTELLIGENCE], icon='<:helene:906303162854543390>',charSettings=preDefCharSet[1][1][1][2]),
    tmpAllie("Félicité", 1, red, TETE_BRULE, dtsword, [celestBronzeHat, celestBronzeArmor, celestBronzeBoots], GENDER_FEMALE, [bloodyStrike, antConst, erodStrike, strengthOfWillCast, convictTet, fragmentation, absorbingStrike2], "Soeur ainée de Sixtine et Alice, Félicité est née dans un monde désolé et post apocaliptique\n\n<:lena:909047343876288552> : Mais parle pour toi !\n\nN'ayant plus aucun humain dans ce monde pas si désolé et pas si post apocaliptique, elle hérita de l'âme de Détermination de ce monde (ainsi que quelques bénédictions de dieux grecs mais c'est une autre histoire\n\nEn grandissant, ces dites bénédictions lui ont permis de développer rapidement son esprit et ses capacités, mais aussi d'attirer sur elle tous les monstres mythologiques du coin. Fort heureusement elle pu compter sur ses parents ainsi que sur sa sœur adoptive ainnée Clémence pour la protéger jusqu'au jour où elle en a eu marre de devoir laisser les autres la défendre.\nElle alla donc trouver les seuls autres personnes avec des âmes de Détermination à sa connaissance : Frisk et Chara, qui lui apprirent les bases. Sa volontée ainsi que ses bénédictions lui permirent de rapidement faire des progrès dans l'escrime, quand pour la maîtrise de la magie, c'est grâce à Hécate qu'elle le doit\n\nEn grandissant, elle a choisi une voie plus ou moins similaire à celle de Clémence, c'est à dire de chercher à purifier des artéfacts maudits agitants les monstres alentours ainsi que l'étude d'ancienne magie. Cependant, là où Féli le fait pour protéger les populations d'hommes, Clémence le fait pour protéger les monstres de ces derniers. Mais ça ne les empêche pas de faire équipe de temps en temps. Après tout le but reste le même", bonusPoints=[ENDURANCE, STRENGTH], icon='<:felicite:909048027644317706>', element=ELEMENT_UNIVERSALIS_PREMO,birthday=(10,6),limitBreaks=[[STRENGTH,ENDURANCE,CHARISMA,AGILITY,PRECISION,INTELLIGENCE,MAGIE],2]),
    tmpAllie("Akira", 2, black, TETE_BRULE, fauc, [nemeBracelet, nemeManteau, nemeBottes], GENDER_MALE, [deathShadow, defi, absorbingStrike2, bundleLemure, theEndCast, bundleFetu, comboFaucheCroix],"Fils aîné des Fluwaraito, Akira est un jeune garçon au sang chaud qui ne renonce jamais à un affrontements. En revanche évitez de le mettre en colère.", ELEMENT_DARKNESS, bonusPoints=[ENDURANCE, STRENGTH], icon='<:akira:909048455828238347>'),
    tmpAllie("Icealia", 2, light_blue, PREVOYANT, blueButterfly, [icealiaHat, icealiaManteau, icealiaBoots], GENDER_FEMALE, [soulagement, inkarmor, pandaima, firstArmor, lightPulse, shell, elemShield],"Une érudite qui préfère protéger ses compagnons", element=[ELEMENT_LIGHT, ELEMENT_WATER], bonusPoints=[INTELLIGENCE, ENDURANCE], icon='<:icealia:909065559516250112>'),
    tmpAllie("Powehi", 2, black, MASCOTTE, grav, [starBar, bhPull, bhBoots], GENDER_FEMALE, [blackHole, isolement, blindage, cosmicPower, inkRes2, graviton, ironHealth], "Une manifestation cosmique d'un trou noir. Si vous vous sentez attiré par elle, c'est probablement à raison\nNe lui demandez pas de vous marchez dessus par contre, si vous voulez un conseil. Elle a beau paraître avoir un petit gabarie, ce n'est pas pour rien qu'elle évite de marcher sur le sol", element=[ELEMENT_SPACE, ELEMENT_DARKNESS], bonusPoints=[ENDURANCE, INTELLIGENCE], icon='<:powehi:909048473666596905>', deadIcon='<:powehiDisiped:907326521641955399>', say=powehiSays),
    tmpAllie("Shehisa", 1, purple, TETE_BRULE, shehisa, [redBatEarRingsred , batRedChemVeste, redBatBoots], GENDER_FEMALE, [heriteLesath, focus, lacerTrap, bleedingPuit, hemoBomb, ShiUltimate, bleedingConvert],"Soeur d'Hélène, elle a elle aussi choisi de s'enroler dans la milice, mais étant trop timide pour faire face à ses adversaires, Shehisa a opté pour une stratégie un peu moins nombre qui consiste à piéger les zones et à regarder ses ennemis se vider de leur sang de loin", element=[ELEMENT_DARKNESS,ELEMENT_WATER], bonusPoints=[STRENGTH, INTELLIGENCE], icon='<:shehisa:919863933320454165>',say=shehisaSays,charSettings=preDefCharSet[0][1][3][2]),
    tmpAllie("Ruby", 2, 0x870a24, MAGE, spaceMetRuneLong, [redbutbar, redbutterflyshirt, redButterFlyBoots], GENDER_FEMALE, [invocCarbunR, space3, space2, spaceElemUse, maitriseElementaire, magicEffGiver], element=[ELEMENT_SPACE, ELEMENT_DARKNESS], icon='<:ruby:958786374759251988>', bonusPoints=[MAGIE, PRECISION]),
    tmpAllie("Sixtine", 1, blue, INOVATEUR, miltrilPlanisphere, [sixitneBarrette, sixitnePull, sixitneBoots], icon='<:sixtine:908819887059763261>', skill=[toxicon, horoscope, nostalgia, revelation, sixtineUlt, expediant, aff2], gender=GENDER_FEMALE, element=[ELEMENT_NEUTRAL, ELEMENT_AIR], bonusPoints=[INTELLIGENCE, ENDURANCE], description="Soeur cadette, Sixtine est plutôt du genre à vouloir rester dans son coin sans être dérangée\n\nElle ne se démarque pas particulièrement de Félicité ou Alice, mais ça ne la dérange pas. Elle passe le plus clair de son temps libre à rêvasser, à du mal à faire le premier pas vers les autres et n'a pas vraiment l'air de s'interresser à grand chose\nMais quand elle s'interresse à un truc, elle veux souvent en connaître un maximum de chose dessus.", say=sixtineSays,birthday=(12,6)),
    tmpAllie("Hina", 1, purple, ATTENTIF, plume, [hinaAcc, hinaBody, hinaShoes], GENDER_FEMALE, [plumeCel, plumePers, pousAviaire, hinaUlt, plumRem, trizooka, inkzooka], icon='<:hina:908820821185810454>', element=[ELEMENT_AIR, ELEMENT_SPACE], bonusPoints=[AGILITY, STRENGTH], description="Oiseau des îles, Hina n'a pas froid aux yeux lorsqu'il s'agit d'aventure.\nA embarquer avec la première pirate venue ça ne lui a apporté que des problèmes avec les forces maritimes.\nCependant elle manque pas mal de confiance en elle et a fait beaucoup trop d'erreur qui lui coute des amitiés.",limitBreaks=[[STRENGTH,PRECISION],7]),
    tmpAllie("John", 2, orange, POIDS_PLUME, airsword, [bandNoir, pullCamo, kanisand], GENDER_MALE, [airlame, airStrike, splashdown, maitriseElementaire, physEffGiver, elemArrowSkill[ELEMENT_AIR]],description="Un Loup Garou qui a réussi à tomber amoureux de la vampire responsable des pluparts des vas et viens à l'infirmerie du village de sa meute\n\nAprès de multiple tentatives de l'approcher sans grand succès, il a réussi à changer la clémence qu'éprouvait cette dernière à son égars en affection, mais a peur d'essayer de monter dans son estime", icon='<:john:908887592756449311>', bonusPoints=[STRENGTH, AGILITY], say=johnSays, element=ELEMENT_AIR),
    tmpAllie("Julie", 1, red, ALTRUISTE, julieWeap, [julieHat, julieDress, julieShoes], GENDER_FEMALE, [accelerant, altOH, julieUlt, timeSp, zelian, extraMedica, shareSkill],"La principale (et unique) servante d'une des vampires les plus puissante du pays.\nElle a appris la magie curative à l'aide des nombreux grimoires dans la bibliothèque du manoire, mais il lui arrive souvent de demander de l'aide à Clémence lorsque sa maîtresse (qui ai d'ailleurs la tutrice magique de cette dernière) lui demande de récupérer des organes de monstres.\nElle se sent souvent petite, en compagnie de ces puissantes vampires\n\nDire qu'elle est légèrement inspirée serait un euphémisme. Au moins elle utilise pas de dagues", element=[ELEMENT_TIME, ELEMENT_FIRE], bonusPoints=[CHARISMA, INTELLIGENCE], icon="<:julie:910185448951906325>", say=julieSays),
    tmpAllie("Krys", 2, purple, TETE_BRULE, krystalFist, [kryscharpe, krysshirt, kryschains], GENDER_OTHER, [earthStrike, defi, krysUlt, mudlame, demolish,krystalisation,ebranlement], "\"Krys Tal (rien à voir avec la chanteuse ou les opticiens) est un cristal (nooon sans blague) ayant gagné une conscience par un procédé mystérieux.\n\nN'étant pas une forme de vie organique, il se nourrit de minéraux qui traînent par-ci par-là, et de l'armure occasionnelle en combat. Il évite habituellement la nourriture organique, mais il ne dira jamais non à un peu de pop-corn, dont il semble avoir une réserve infinie.\n\nExtrêmement sensible à l'eau, mais n'hésitera pas à ingérer le contenu de la première cannette qui traîne.\n\nAvant, il était un peu con, mais ça, c'était av-Ah on m'annonce dans l'oreillette que c'est toujours le cas, my bad.\n\nPas le plus grand fan d'Akira depuis un sombre incident dans un labo.\"", element=[ELEMENT_EARTH, ELEMENT_EARTH], icon="<:krys:916118008991215726>", deadIcon='<:krysCan:916117137339322388>', bonusPoints=[ENDURANCE, STRENGTH],limitBreaks=[[ENDURANCE],10]),
    tmpAllie("Edelweiss", 1, 0xE0FFE7, PREVOYANT, bleuSpiritWings, [battleShieldHat, battleShieldUnif, battleShieldShoes], GENDER_FEMALE, [haimaSkill, krasis, pandaima, intelRaise, pepsis, kerachole, pneuma], element=[ELEMENT_EARTH, ELEMENT_WATER], icon='<:edelweiss:918451422939451412>', deadIcon="<:flowernt:894550324705120266>", bonusPoints=[INTELLIGENCE, ENDURANCE],limitBreaks=[[INTELLIGENCE],10]),
    tmpAllie("Iliana", 1, white, ALTRUISTE, iliSwoShield, [zenithHat, zenithArmor, zenithBoots], GENDER_FEMALE, [lightAura2, ironWillSkill, clemency, lightBigHealArea, aurore2, holiomancie, holyShieltron], "Une Neko paladine qui se bat pour faire perdurer la Lumière dans sa dimension\nRelativement timide, elle ne va pas souvent vers les inconnus, mais ça ne l'empêche pas de faire de son mieux pour les tenir en vie tout de même", [ELEMENT_LIGHT, ELEMENT_DARKNESS], icon='<:Iliana:926425844056985640>', deadIcon='<:oci:930481536564879370>', bonusPoints=[CHARISMA, ENDURANCE], say=ilianaSaysNormal,limitBreaks=[[ENDURANCE,CHARISMA],5]),
    tmpAllie('Candy', 2, 0xa124b2, INOVATEUR, concentraceurZoom, [summonerFoulard50, summonerMenteau50, summonerShoes50], GENDER_FEMALE, [invocBat, invocSeaker, bombRobot, killerWailUltimate, invocAutFou, invocAutQueen, invocAutTour], "Jeune ingénieur de l'Escardon Espadon Nouvelle Génération, elle s'entend très bien avec sa supérieur", icon='<:candy:933518742170771466>', bonusPoints=[MAGIE, STRENGTH]),
    tmpAllie('Ly', 1, white, ATTENTIF, firework, [critIndStrHat45, critIndStrBody45, critIndStrShoes45], GENDER_FEMALE, [acidRain, coroRocket, quadFleau, ultraSignal, coroShot, morsCaudiqueSkill, lanceTox],"Une mercenaire rencontrée sur les îles\nElle préfère rester loin et innonder ses ennemis avec ses attaques de zones", [ELEMENT_FIRE, ELEMENT_SPACE], icon='<:ly:943444713212641310>', bonusPoints=[STRENGTH, PRECISION], say=lySays),
    tmpAllie('Anna', 2, black, PROTECTEUR, lunarBonk, [fullMoonHat, fullMoonArmor, fullMoonBoots], GENDER_FEMALE, [royaleGardeSkill, darkShield, ghostlyCircle, heartStone, haimaSkill, intelRaise, bigBubbler], element=[ELEMENT_LIGHT, ELEMENT_WATER], icon='<:anna:943444730430246933>', bonusPoints=[ENDURANCE, INTELLIGENCE]),
    tmpAllie("Elina", 1, 0x560909, ALTRUISTE, serringue, [urgChirHat, urgChirDress, urgChirShoes], GENDER_FEMALE, [preciChi, cure, uberCharge, terachole, renisurection, asile, reconst], element=[ELEMENT_LIGHT, ELEMENT_NEUTRAL], icon='<:elina:950542889623117824>', bonusPoints=[CHARISMA, PRECISION],charSettings=preDefCharSet[1][1][2][2]),
    tmpAllie("Bénédicte", 1, white, MAGE, magicWood, [ora50Hat, ora50Dress, ora50Shoes], GENDER_FEMALE, [genesis, comboVerMiracle, redemption, benitWater, divineBenediction, divineCircle, divineAbne], element=[ELEMENT_LIGHT, ELEMENT_LIGHT], bonusPoints=[MAGIE, CHARISMA], icon='<:benedict:958786319776112690>'),
    tmpAllie("Amary",1, 0xdb6163, IDOLE, flumWand, [pinkbutbar,pinkbutterflyshirt,pinkbutterflysandals], GENDER_FEMALE, [croissance, descart, petalisation, roseeHeal, floraisonFinale, theSkill, astrodyn],"Floraaaaaaaa ?",[ELEMENT_EARTH,ELEMENT_AIR],deadIcon='<:amaryDown:979440197127262218>',icon='<:amary:979441677460713502>',bonusPoints=[CHARISMA,INTELLIGENCE],charSettings=preDefCharSet[2][1][1][2]),
    tmpAllie("Chûri",1,light_blue,MAGE,phenixLeath, [on45Hat, on45Dress, on45Shoes], GENDER_FEMALE, [fairySlash, maitriseElementaire, elemRuneSkill[ELEMENT_EARTH], raisingPheonix, earthCircle, magicEffGiver, cassMont], "Ayant fini par s'ennuyer en attendant que l'infime partie d'elle même étant restée bloqué parmis les vivants réussise à la rejoindre, Chûri s'est liée d'amitié avec un phenix du nom de Hinoro au point que ce dernier concenti à fusionner temporairement leurs âmes afin d'aider la fée à atteindre son but.\nDepuis, Chûri arpente le monde sous forme translucide ressemblant fortement à son ancien corps et Hinoro apparait régulièrement à ses côtés pour lui porter assistance.",[ELEMENT_EARTH,ELEMENT_FIRE],False,"<:fairyOut:935335430814068786>","<:churi:992941366537633914>",[MAGIE,PRECISION],say=churiSays,limitBreaks=[[ENDURANCE,MAGIE,AGILITY],4]),
    tmpAllie("Lily",2,0xD9A4FD,INOVATEUR, miltrilPlanisphere, [sixitneBarrette, sixitnePull, sixitneBoots], GENDER_FEMALE, [dmonBlood, burningGround, demonLand, demonArmor, demonArmor2, exhibitionnisme, demonConst], "Une succube qui se sent bien plus à l'aise dans le monde des rêves que dans la réalité.\nBonne amie de Sixtine",[ELEMENT_SPACE,ELEMENT_DARKNESS],icon="<:lily:1006442350471553076>",bonusPoints=[INTELLIGENCE,ENDURANCE],say=lilySays,charSettings=preDefCharSet[2][1][2][2]),
    tmpAllie("Epiphyllum",1,0xEAC6DB, PREVOYANT, epiphyllum, [butterflyEarRingsBlue,blueChemVeste,blueButterFlyBoots], GENDER_FEMALE, [forestGarde,soulagement,verseau,pandaima,inkarmor,silvArmor,sacredSoil], icon='<:epiphilium:1014094726351294484>', deadIcon = "<:flowernt:894550324705120266>", element=[ELEMENT_SPACE,ELEMENT_WATER],bonusPoints=[INTELLIGENCE,PRECISION],limitBreaks=[[INTELLIGENCE,PRECISION],7],description="Figure maternelle d'Edelweiss, Epiphyllum est une dryade calme et posée qui préfère resplandir par ses connaissances plutôt que ses aptitudes au combat",charSettings=preDefCharSet[1][1][2][2])
]

churInoSkills = [galvanisation, maitriseElementaire, elemRuneSkill[ELEMENT_FIRE], raisingPheonix, fireCircle, magicEffGiver, cycloneEcarlate]

# Shushi alt spells
shushiSkill1 = skill("Frappe lumineuse", "shushiSkill1", TYPE_DAMAGE, 0,150, cooldown=3, use=MAGIE, emoji='<a:ShushiLF:900088862871781427>')
shushiSkill3Eff = effect("Jeu de lumière", "diff", redirection=35, trigger=TRIGGER_DAMAGE,description="Un habile jeu de lumière permet de vous cacher de vos ennemis")
shushiSkill3 = skill("Diffraction", "shushiSkill2", TYPE_ARMOR, 0, 0, AREA_CIRCLE_6, effects=shushiSkill3Eff,cooldown=5, initCooldown=2, use=None, emoji='<a:diffraction:916260345054658590>')
shushiSkill4Eff = effect("Assimilation", "assimil", MAGIE, resistance=10, overhealth=150, description="Grâce à Shihu, vous avez réussi à utiliser les Ténèbres environant à votre avantage",emoji=uniqueEmoji("<:tarmor:909134091604090880>"), type=TYPE_ARMOR, trigger=TRIGGER_DAMAGE)
shushiSkill4 = skill("Assimilation", "shushiSkill4", TYPE_ARMOR, 0, cooldown=3, effects=shushiSkill4Eff,say='On peut y awiver !', use=MAGIE, emoji='<:assimilation:916260679944634368>')
shushiWeapEff = effect("Lueur Ténébreuse", "darkLight", MAGIE, resistance=5, overhealth=50,type=TYPE_ARMOR, emoji=uniqueEmoji('<:dualMagie:899628510463803393>'))
shushiWeap = weapon("Magie trancendante", "dualMagie", RANGE_LONG, AREA_DONUT_5, 35, 100, 0, strength=-20, endurance=10, charisma=20, intelligence=20,magie=55, type=TYPE_HEAL, target=ALLIES, use=MAGIE, effectOnUse=shushiWeapEff, affinity=ELEMENT_LIGHT, emoji='<:dualMagie:899628510463803393>')
shushiHat = stuff("Barrête de la cohabitation", "dualHat", 0, 0, strength=-20, endurance=15, charisma=20, agility=10,precision=10, intelligence=20, magie=45, affinity=ELEMENT_LIGHT, emoji='<:coaBar:911659734812229662>')
shushiDress = stuff("Robe de la cohabitation", "dualDress", 1, 0, strength=-10, endurance=35, charisma=20, agility=0,precision=10, intelligence=10, magie=60, resistance=20, affinity=ELEMENT_LIGHT, emoji='<:coaDress:911659797076660294>')
shushiBoots = stuff("Bottines de la cohabitation", "dualBoost", 2, 0, strength=-10, endurance=15, charisma=0, agility=20,precision=10, magie=45, intelligence=10, affinity=ELEMENT_LIGHT, emoji='<:coaBoots:911659778995007528>')
shushiSkill5 = skill("Lumière éternelle", "LumEt", TYPE_RESURECTION, 0, 100, emoji='<:renisurection:873723658315644938>',cooldown=3, description="Permet de ressuciter un allié", use=MAGIE, range=AREA_DONUT_7)
shushiArmorSkillEff = effect("Armure Harmonique", "shushiArmor", MAGIE, overhealth=200, turnInit=3,type=TYPE_ARMOR, trigger=TRIGGER_DAMAGE, emoji=uniqueEmoji("<a:transArmorB:900037831257358378>"))
shushiArmorSkill = skill("Armure Harmonique", "shushiArmorSkill", TYPE_ARMOR, 0, effects=shushiArmorSkillEff,range=AREA_MONO, area=AREA_CIRCLE_5, cooldown=7, use=MAGIE, emoji='<a:transArmorB:900037831257358378>')

# Alice Ex. skills
clemBloodJauge = effect("Jauge de sang","clemBloodJauge",turnInit=-1,unclearable=True,emoji=uniqueEmoji('<:vampire:900312789686571018>'),lvl=100,description="Clémence possédée tourne autour de sa Jauge de Sang\n\nElle débute le combat avec une jauge à **100** Points de sang, son maximum.\nChacunes de ses compétences ont un coût en Points de Sang, qui sont retiré à la jauge à la fin de leur utilisation\n\nSi la jauge de sang tombe à **0 point**, Clémence est étourdie pendant 2 tours durant lesquels sa résistance est diminuée\nLa jauge de sang récupère **1 point** de sang à chaque fois que Clémence inflige 50 points de dégâts, et **100 points** une fois que Clémence n'est plus étourdie\n\nLa quantité de points de sang dans la jauge de sang est constamant visible\nClémence possède 10% de vol de vie",jaugeValue=[["<:BJLeftEmpty:900473865459875911>","<:BJMidEmpty:900473889539366994>","<:BJRightEmpty:900473909856587847>"],["<:BJLeftFull:900473987564441651>","<:BJMidFull:900474021781569604>","<:BJRightFull:900474036042215515>"]])

aliceBloodJauge = copy.deepcopy(clemBloodJauge)
aliceBloodJauge.emoji = uniqueEmoji("<:vampire:900312789686571018>")
aliceBloodJauge.description = "Alice exaltée tourne autour de sa Jauge de Sang\n\nElle débute le combat avec une jauge à **100** Points de sang, son maximum.\nChacunes de ses compétences ont un coût en Points de Sang, qui sont retiré à la jauge à la fin de leur utilisation\n\nSi la jauge de sang tombe à **0 point**, Alice est étourdie pendant 2 tours durant lesquels sa résistance est diminuée\nLa jauge de sang récupère **1 point** de sang à chaque fois que Alice soigne 50 points de vie, et **100 points** une fois qu'Alice n'est plus étourdie\n\nLa quantité de points de sang dans la jauge de sang est constamant visible"
aliceBloodJauge.jaugeValue = [["<:BJLeftEmpty:900473865459875911>","<:BJMidEmpty:900473889539366994>","<:BJRightEmpty:900473909856587847>"],["<:aliceBJLeftFull:914780954336305192>","<:aliceBJMidFull:914780988134019073>","<:aliceBJRightFull:914781018559492106>"]]

aliceExHeadruban = stuff("Ruban vampirique", "aliceExHead", 0, 0, charisma=40, negativeHeal=-50, endurance=55, emoji=batRuban.emoji)
aliceExDress = stuff("Robe vampirique", "aliceExDress", 1, 0, endurance=10, resistance=15, charisma=45, negativeHeal=-25, emoji=aliceDress.emoji)
aliceExShoes = stuff("Ballerines vampiriques", "aliceExShoes", 2, 0, agility=25, charisma=45, negativeHeal=-35, endurance=5, emoji=aliceShoes.emoji)

aliceExWeapEff = effect("Bénédiction vampirique", "aliceExWeapEff", CHARISMA, emoji=uniqueEmoji("<:vampire:900312789686571018>"), power=15, type=TYPE_INDIRECT_HEAL, trigger=TRIGGER_AFTER_DAMAGE, description="Cet effect confère **{0}%** de Vol de Vie au porteur.\nLe pourcentage de convertion est augmenté par les statistiques du lanceur")
aliceExWeap = weapon("Rosa receptaculum", "aliceExWeap", RANGE_DIST, AREA_CIRCLE_5, 35, 100, 0, use=CHARISMA, charisma=35, resistance=10, type=TYPE_HEAL, target=ALLIES, effectOnUse=aliceExWeapEff, effects=aliceBloodJauge, emoji='<:vampBall:916199488891273276>', say=["Je vais essayer de vous faire tenir le plus longtemps possible...", "Je sais que tu en as encore en réserve, c'est pas vraiment le moemenent de lacher !", "On tiens le bon bou, continuons comme ça !", "Mhf..."])
aliceSkill1Eff = effect("Régénération vampirique", "aliceRegenEff", CHARISMA, power=20, emoji=uniqueEmoji("<a:aliceSkill1:914787461949960202>"), type=TYPE_INDIRECT_HEAL,turnInit=3, lvl=3, area=AREA_CIRCLE_2, description="Au début du tour du porteur, lui et ses alliés proches recoivent des soins", trigger=TRIGGER_START_OF_TURN)
aliceSkill1 = skill("Rénégération", "aliceSkill1", TYPE_INDIRECT_HEAL, 0,0, emoji="<a:aliceSkill1:914787461949960202>", effects=aliceSkill1Eff, cooldown=3)
aliceSkill2Eff = effect("Galvanision vampirique", "aliceBoostEff", CHARISMA, strength=20,magie=20, percing=3, emoji=uniqueEmoji('<a:aliceSkill2:914791502931197962>'))
aliceSkill2 = skill("Galvanisation", "aliceSkill2", TYPE_BOOST, 0, range=AREA_DONUT_6, area=AREA_CIRCLE_2, effects=aliceSkill2Eff, cooldown=3, emoji='<a:aliceSkill2:914791502931197962>', say=["Allez-s'y !", "On ne lâche rien !", "Il va falloir essayer un peu plus fort que ça..."])
aliceDirectDmg = skill("Flos luminosus", "aliceSkill3", TYPE_DAMAGE, 0, 130, emoji='<a:aliceSkill3:914794172215623690>', cooldown=3,use=CHARISMA, say=["C'est pour ton bien Clémence !", "Sit invehitur Rosa Lucis !", "Tuum, Rosa Lucis !"])
aliceIndirectDmgEff = effect("Provecta Fluos Luminosus","aliceDot",CHARISMA,power=int(150/5),turnInit=5,lvl=5,description="Inflige des dégâts indirects en début de tours",type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_START_OF_TURN,emoji='<a:aliceSkill3:914794172215623690>')
aliceDotEff2 = copy.deepcopy(dmgDown)
aliceDotEff2.power, aliceDotEff2.stat, aliceDotEff2.turnInit = 3, CHARISMA, 3
aliceIndirectDmg = skill("Provecta Fluos Luminosus","aliceSkill3",TYPE_INDIRECT_DAMAGE,effects=[aliceIndirectDmgEff,aliceDotEff2],cooldown=5)
aliceSkill3 = skill("Sorts offensifs","aliceSkill3",TYPE_DAMAGE,become=[aliceDirectDmg,aliceIndirectDmg],cooldown=3,description="Inflige des dégâts directs ou bien inflige un effet de dégâts sur la durée tout en réduisant légèrement les dégâts de la cible")
aliceSkill4 = skill("Pleine lune", "aliceSkill4", TYPE_HEAL, 0, 80, AREA_MONO, area=AREA_CIRCLE_3, use=CHARISMA, cooldown=3,emoji='<a:aliceSkill4:914796355925458984>', say=["On lache rien !", "Je donnerais tout, même si je dois y passer !", "Courage !", "Sanet nos lux plenae lunae !"])
aliceRez = skill("Vampirization", "aliceRez", TYPE_RESURECTION, 0, 300, range=AREA_CIRCLE_7, emoji="<a:memAlice2:908424319900745768>", use=CHARISMA,description="Si plus de la moitié de l'équipe est morte, la zone d'effet de la compétence deviens un cercle de 7 cases autour de Alice, mais consomme l'intégralité de sa jauge de sang", say=["C'est trop tôt pour laisser tomber !", "On a encore besoin de toi !"])
aliceRez2 = skill("Salutaris meridiem", "aliceRez+", TYPE_RESURECTION, 0, 300, range=AREA_MONO, area=AREA_CIRCLE_7,emoji="<a:memAlice2:908424319900745768>", use=CHARISMA, say="Angeli, audi me et adiuva nos, sustulite... MEMENTO VOCIS ANGELI !")
aliceSongEff2 = effect("Chant de la gloire","aliceSongEff2",CHARISMA,strength=10,endurance=10,charisma=10,agility=10,precision=10,intelligence=10,magie=10,description="Augmente toutes les statisitiques principales du porteur",emoji='<:aliceSongSkill:977011751075868682>')
aliceSongEff1 = effect("Chant de la gloire","aliceSongEff1",callOnTrigger=aliceSongEff2,area=AREA_DONUT_7,trigger=TRIGGER_END_OF_TURN,emoji='<a:aliceSongEff:977011977358544927>',turnInit=3,description="Augmente les statistiques des alliés à la fin du tour")
aliceSong1 = skill("Chant de la gloire","aliceSkill5",TYPE_BOOST,effects=aliceSongEff1,range=AREA_MONO,emoji='<:aliceSongSkill:977011751075868682>',cooldown=5,description="Se met à entonner le Chant de la Gloire, augmentant les statistiques principales des alliés autour de vous à la fin de votre tour pendant 3 tours (celui-ci inclut)",message='Alice entonne le Chant de la Gloire')
aliceSong2Eff1, aliceSong2Eff2 = copy.deepcopy(healDoneBonus), effect("Chant de la vie","aliceSong2Eff2",CHARISMA,power=15,area=AREA_CIRCLE_7,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_HEAL,turnInit=3,lvl=3,emoji=aliceSkill1.emoji)
aliceSong2Eff1.turnInit, aliceSong2Eff1.power = 3, 20
aliceSong2 = skill("Chant de la Vie","aliceSkill5",TYPE_INDIRECT_HEAL,range=AREA_MONO,effects=[aliceSong2Eff1,aliceSong2Eff2],cooldown=3)
aliceSkill5 = skill("Répertoire","aliceSkill5",TYPE_BOOST,become=[aliceSong1,aliceSong2],use=CHARISMA,cooldown=3,description="Permet d'entonner un chant pendant 3 tours\n{0} __{1} :__ Augmente toutes les statistiques principales des alliés alentours\n{2} __{3} :__ Soigne les alliés alentours tout en augmentant les soins réalisés par Alice".format(aliceSong1.emoji,aliceSong1.name,aliceSong2.emoji,aliceSong2.name))
aliceCoda1Eff = effect("Coda régénérant","aliceCoda1Eff",CHARISMA,power=30,area=AREA_CIRCLE_1,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_HEAL)
aliceCoda2Eff, aliceCoda3Eff = copy.deepcopy(defenseUp), copy.deepcopy(dmgUp)
aliceCoda2Eff.stat = aliceCoda3Eff.stat = CHARISMA
aliceCoda2Eff.power, aliceCoda3Eff.power = 7, 10
aliceCoda2Eff.turnInit = aliceCoda3Eff.turnInit = 3
aliceCoda4Eff = effect("Coda galvanisant","aliceCoda4Eff",CHARISMA,strength=15,magie=15,turnInit=3)
aliceCoda1 = skill("Coda régénérant","aliceSkill6",TYPE_INDIRECT_HEAL,cooldown=3,effects=aliceCoda1Eff)
aliceCoda2 = skill("Coda offensif","aliceSkill6",TYPE_BOOST,cooldown=3,effects=aliceCoda2Eff,area=AREA_CIRCLE_1)
aliceCoda3 = skill("Coda défensif","aliceSkill6",TYPE_BOOST,cooldown=3,effects=aliceCoda3Eff,area=AREA_CIRCLE_1)
aliceCoda4 = skill("Coda galvanisant","aliceSkill6",TYPE_BOOST,cooldown=3,effects=aliceCoda4Eff,area=AREA_CIRCLE_1)
aliceSkill6 = skill("Coda Musicaux","aliceSkill6",TYPE_BOOST,cooldown=3,become=[aliceCoda1,aliceCoda2,aliceCoda3,aliceCoda4],description="Octroi un Coda à un allié")

# Clem Ex.
clemBleeding = copy.deepcopy(bleeding)
clemBleeding.power, clemBleeding.stat, clemBleeding.name = 50, MAGIE, "Sanguisugae"
clemExSkill1 = skill("Exponentia Catenae", "clemExSkill1", TYPE_DAMAGE, 0, power=100, effectOnSelf=quickCastEff, replay=True, use=MAGIE,description="Inflige des dégâts, puis vous permet de rejouer votre tour en ignorant un tour de chargement de la prochaine compétence utilisée", cooldown=4, initCooldown=3, emoji=quickCast.emoji, lifeSteal=35, say=["Vous me faite tous perdre mon temps...","Vous n'êtes qu'un contre-temps."])
clemExSkill21Lauch = skill("Sanguinis Explosio", "clemExSkill2Launch", TYPE_DAMAGE, 0,sussess=150,ultimate=True, emoji='<:clemBoom:978377130750644224>', initCooldown=2, power=750,area=AREA_CIRCLE_2, use=MAGIE, cooldown=6, description="Déclanche une explosion infligeant de lourds dégâts dans une large zone\nTemps de rechargement partagé avec <:clemRay:978376646262403144> __Sanguinis Ray__ \n__Puissance :__ {power}", say=["Voyons faire si quelqu'un résistera à ça.","J'espère que vous avez une bonne assurance vie.","J'espère que vous avez eu la bonne idée de rédiger votre testamant avant de venir me faire chier"])
clemExSkill21CastEff = effect("Cast - Sanguinis Explosio", "clemExSkill2CastEff",replique=clemExSkill21Lauch, silent=True, turnInit=2)
clemExSkill22Lauch = skill("Sanguinis Ray",clemExSkill21Lauch.id,TYPE_DAMAGE,sussess=250,power=1250,ultimate=True,emoji='<:clemRay:978376646262403144>',area=AREA_INLINE_5,initCooldown=clemExSkill21Lauch.initCooldown,cooldown=clemExSkill21Lauch.cooldown,use=MAGIE,description="Tir un grand rayon d'énergie à vos points caridaux, infligeant d'extrèmes dégâts à tous les ennemis alignés\nNe peux pas être esquivé et ignore **35%** de la résistance ennemie\nTemps de rechargement partégé avec <:clemBoom:978377130750644224> __Sanguinis Explosio__\n__Puissance :__ {power}",percing=35,say=["J'espère que vous avez une bonne assurance vie !","Faisons un peu le ménage, voulez-vous ?","Je vais mettre une croix sur vos projets d'avenirs."])
clemExSkill22Cast = effect("Cast - {0}".format(clemExSkill22Lauch.name),"clemRayonSanguinCastEff",silent=True,turnInit=2,replique=clemExSkill22Lauch)
clemExSkill22 = copy.deepcopy(clemExSkill22Lauch)
clemExSkill22.power, clemExSkill22.effectOnSelf = 0, clemExSkill22Cast
clemExSkill21 = copy.deepcopy(clemExSkill21Lauch)
clemExSkill21.power, clemExSkill21.effectOnSelf = 0, clemExSkill21CastEff
clemExSkill2 = skill('Sanguis Bang',clemExSkill21.id,TYPE_DAMAGE,cooldown=clemExSkill21.cooldown,ultimate=True,use=MAGIE,become=[clemExSkill21,clemExSkill22],area=AREA_CIRCLE_2,emoji='<:clemCast:978376938286641172>')
clemExSkill31 = skill("Sanguis Hastis", "clemExSkill3", TYPE_DAMAGE, 0, sussess=125, power=250, range=AREA_DIST_7, use=MAGIE,area=AREA_CIRCLE_1, cooldown=3, emoji='<:clemExSkill:1015209835001815091>', description="Inflige de lourd dégâts à l'ennemi éloignés ciblé et ses alliés alentours\nTemps de rechargement partagé avec __Hastae Noctis__\n__Puissance :__ {power}",say=["C'est pas parceque vous êtes loin que vous aurez plus de chances de survie","Vous comptiez pas rester là bas à regarder vos camarades se faire écraser, si ?","J'ose espérer que vous ne pensiez pas que je vous avais oublié ?"])
clemExSkill32 = skill("Hastae Noctis", "clemExSkill3", TYPE_DAMAGE, 0,sussess=250, power=350,use=MAGIE, cooldown=3, emoji='<:clemExSkill:1015209812407111770>', description="Inflige de lourd dégâts monocibles et vous soigne d'une partie des dégâts infligés\nTemps de rechargement partagé avec __Sanguis Hastis__\n__Puissance :__ {power}",lifeSteal=35,say=["Tu penses que tu va pouvoir tenir combien de temps comme ça ?","Tu t'es pris pour qui ?"])
clemExSkill3 = skill("Sanguis Hastis/Hastae Noctis","clemExSkill3",TYPE_DAMAGE,become=[clemExSkill31,clemExSkill32],cooldown=clemExSkill32.cooldown,use=MAGIE, emoji='<:clemExSkill:1015209835001815091>')
clemExSkill5 = skill("Saturi Cum Sanguine", "clemExSkill5", TYPE_DAMAGE, 0 ,sussess=150, power=250, emoji='<:clemExSkill:1015209760062189628>', range=AREA_MONO,area=AREA_CIRCLE_2, use=MAGIE, cooldown=5, description="Inflige de lourd aux ennemis alentours",say=["C'est bien, vous me faites le plaisir de venir mourir de vous-même","Vous n'êtes pas les premiers et vous serez clairement pas les derniers."])
clemExSkill6 = skill("Sanguis Pluvia", "clemExSkill6", TYPE_DAMAGE, emoji='<:clemExSkill:1015209784800198728>', power=50,sussess=200, range=AREA_MONO, area=AREA_ALL_ENEMIES, initCooldown=2, use=MAGIE,cooldown=5, setAoEDamage=True, replay=True, description="Inflige des dégâts à tous les ennemis en volant une partie des dégâts infligés, tout en leur infligeant un effet de dégâts indirects sur la durée",lifeSteal=35,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_ALL_ENEMIES,clemBleeding],say=["Vous suffirez à peine à combler ma soif pour 3 minutes...","J'utilise trop de sang pour vous..."])
clemExSkill7Eff = copy.deepcopy(dmgUp)
clemExSkill7Eff.power, clemExSkill7Eff.turnInit = 35, 3
clemExSkill7 = skill("Sanguis Exaltus", "clemExSkill7", TYPE_BOOST, range=AREA_MONO, emoji='<a:dmgBuffB:954429227657224272>', effects=clemExSkill7Eff, cooldown=7,description="Augmente vos dégâts de **{0}%** pendant {1} tours et vous permet de rejouer votre tour".format(clemExSkill7Eff.power, clemExSkill7Eff.turnInit),replay=True,say=["Si vous y tenez tant, je vais vous faire l'honneur d'y mettre un peu du miens","`Soupir` Pas question de perdre trop de temps sur des cloportes de votre espèce.","Je doute que n'importe lequel d'entre vous pouvais déjà résister plus de 3 secondes, mais vous avez de la chance j'ai pas envie que ça dure aussi longtemps"])

CLEMCOMB6POWER, CLEMCOMB5POWER, CLEMCOMB4POWER, CLEMCOMB3POWER, CLEMCOMB2POWER, CLEMCOMB1POWER = 750,100,400,350,300,100

clemExSkill41 = skill("Résolution Sanglante","clemExSkill4",TYPE_DAMAGE,power=CLEMCOMB6POWER,sussess=200,cooldown=5,range=AREA_INLINE_5,emoji='<:resolution:978398280943804436>',area=AREA_LINE_5,description="Effectue une succession d'attaque contre un ennemi. Le dernier coup du combo inflige des dégâts en ligne\n__Puissance totale :__ **{0}**".format(CLEMCOMB6POWER+CLEMCOMB5POWER+CLEMCOMB4POWER+CLEMCOMB3POWER+CLEMCOMB2POWER+CLEMCOMB1POWER),use=MAGIE,say="Prêt pour le final ?")
clemExSkill41Cast = effect("Résolution préparée","clemExSkill41Cast",silent=True,replique=clemExSkill41)
clemExSkill42 = skill("Déplacement Sanglant","clemExSkill4",TYPE_DAMAGE,sussess=200,power=CLEMCOMB5POWER,jumpBack=1,effectOnSelf=clemExSkill41Cast,emoji='<:dep:932765889017839636>',range=AREA_CIRCLE_1,replay=True,use=MAGIE,tpCac=True)
clemExSkill42Cast = effect("Déplacement préparé","clemExSkill42Cast",silent=True,replique=clemExSkill42)
clemExSkill43 = skill("Redoublement Sanglant","clemExSkill4",TYPE_DAMAGE,sussess=200,power=CLEMCOMB4POWER,effectOnSelf=clemExSkill42Cast,emoji='<:combo3:978398179999514624>',range=AREA_CIRCLE_1,replay=True,use=MAGIE,tpCac=True)
clemExSkill43Cast = effect("Redoublement préparé","clemExSkill43Cast",silent=True,replique=clemExSkill43)
clemExSkill44 = skill("Zwerchhau Sanglant","clemExSkill4",TYPE_DAMAGE,sussess=200,power=CLEMCOMB3POWER,effectOnSelf=clemExSkill43Cast,emoji='<:combo2:978398160454045738>',range=AREA_CIRCLE_1,replay=True,use=MAGIE,tpCac=True)
clemExSkill44Cast = effect("Zwerchhau préparé","clemExSkill44Cast",silent=True,replique=clemExSkill44)
clemExSkill45 = skill("Riposte Sanglante","clemExSkill4",TYPE_DAMAGE,sussess=200,power=CLEMCOMB2POWER,effectOnSelf=clemExSkill44Cast,emoji='<:combo1:978398142967992330>',range=AREA_CIRCLE_1,replay=True,use=MAGIE,tpCac=True)
clemExSkill45Cast = effect("Riposte préparée","clemExSkill45Cast",silent=True,replique=clemExSkill45)
clemExSkill4 = skill("Corps à Corps Sanglant","clemExSkill4",TYPE_DAMAGE,sussess=200,power=CLEMCOMB1POWER,effectOnSelf=clemExSkill45Cast,replay=True,range=AREA_INLINE_5,emoji='<:cac:932765903102291999>',tpCac=True,description="Effectue une succession d'attaque contre un ennemi. Le dernier coup du combo inflige des dégâts en ligne\n__Puissance totale :__ **{0}**".format(CLEMCOMB6POWER+CLEMCOMB5POWER+CLEMCOMB4POWER+CLEMCOMB3POWER+CLEMCOMB2POWER+CLEMCOMB1POWER),use=MAGIE)

clemExSay = says(
    start="Pff, vous tenez tant que ça à être au milieu de ma route ?",
    onKill="Tss, même pas le temps de faire une pause pour manger...",
    blueWinAlive="Quel résultat surprenant"
)

clemExWeapon = copy.deepcopy(rapiere)
clemExWeapon.power, clemExWeapon.range, clemExWeapon.effectOnUse, clemExWeapon.name = 200, RANGE_MELEE, clemBleeding, "Flos Argenteus"
miniStuff = stuff("Rune adaptative", 'clemRune', 0, 0, endurance=50, charisma=0, agility=50//2,precision=int(50*0.3), intelligence=50//10, magie=50*2, resistance=min(50//5, 35), emoji=clemEarRings.emoji)

# Iliana prêtresse
miniStuffHead = stuff("Casque de la neko de la lueur ultime", 'ilianaPreHead', 0, 0, endurance=int(50*1.35), agility=int(50*0.3), precision=int(50*0.3), charisma=50, magie=50, resistance=min(50//5, 50), percing=10, emoji=zenithHat.emoji)
miniStuffDress = stuff("Armure de la neko de la lueur ultime", 'ilianaPreArmor', 1, 0, endurance=int(50*1.85), agility=int(50*0.3), precision=int(50*0.5), charisma=50, magie=50, percing=15, resistance=min(50//5, 50), emoji=zenithArmor.emoji)
miniStuffFlats = stuff("Sorolets de la neko de la lueur ultime", 'ilianaPreBoots', 2, 0, endurance=int(50*1.35), agility=int(50*0.3), precision=int(50*0.3), charisma=50, magie=50, resistance=min(50//5, 50), percing=10, emoji=zenithBoots.emoji)

iliPreArmor = effect("Armure de Lumière", "ilianaShield", CHARISMA, overhealth=135, type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE, turnInit=5, stackable=True, emoji='<a:transArmorB:900037831257358378>')
iliPrePoi = effect("Lumière Absolue", "ilianaIndirect", CHARISMA, power=50,type=TYPE_INDIRECT_DAMAGE, trigger=TRIGGER_START_OF_TURN, turnInit=3, lvl=5)
iliPreSkill1 = skill("Champ lumineux", 'iliSkill1', TYPE_INDIRECT_DAMAGE, effects=iliPrePoi, range=AREA_MONO, area=AREA_CIRCLE_3, use=CHARISMA, cooldown=4, effectAroundCaster=[TYPE_ARMOR, AREA_MONO, iliPreArmor], description='Donne un effet de dégâts indirects aux ennemis alentours et vous procure une armure')
iliPreRegen = effect("Régénération de Lumière", "ilianaRegen", CHARISMA, power=50, trigger=TRIGGER_START_OF_TURN, type=TYPE_INDIRECT_HEAL,emoji='<a:ilianaRegen:969825374093578260>', turnInit=5, stackable=True, description="Soigne le porteur de l'effet au début de son tour")
iliPreSkill2Heal = skill('Rénération', "iliSkill2", TYPE_HEAL, power=200, range=AREA_CIRCLE_7, effects=iliPreRegen,cooldown=3, description="Soigne l'allié ciblé et lui procure un effet de régénération sur la durée", use=CHARISMA,emoji='<a:ilianaRegen:969825374093578260>')
iliPreSkill2Shield = skill("Armure de lumière","iliSkill2", TYPE_ARMOR, effects=iliPreArmor,cooldown=iliPreSkill2Heal.cooldown,range=iliPreSkill2Heal.range,description="Procure une grosse armure à l'allié ciblé",effPowerPurcent=1.2)
iliPreSkill2 = skill("Pouvoir de la lumière","iliSkill2",TYPE_HEAL,cooldown=3,become=[iliPreSkill2Heal,iliPreSkill2Shield])
iliPreSkill3 = skill("Tourbillon de Lumière", "iliSkill3", TYPE_DAMAGE, power=150, range=AREA_MONO,area=AREA_CIRCLE_2, use=CHARISMA, description="Inflige des dégâts aux ennemis alentours")
iliPreDmgReduc = copy.deepcopy(defenseUp)
iliPreDmgReduc.power = 80
iliPreSkill4 = skill("Lumière Eternelle", "lb", TYPE_ARMOR, emoji=trans.emoji, use=None, range=AREA_MONO, area=AREA_ALL_ALLIES,ultimate=True, effects=[iliPreDmgReduc, iliPreRegen], cooldown=7, description='Réduit les dégâts subis par tous les allié de 80%')
iliStans = effect("Conviction de la Lumière", "ilianaStans", charisma=30, resistance=20,aggro=100, turnInit=-1, unclearable=True, emoji='<:ilianaStans:969819202032664596>')
iliPreSkill5 = skill("Conviction de la Lumière", "ilianaSkill5",TYPE_PASSIVE, effectOnSelf=iliStans, emoji='<:ilianaStans:969819202032664596>')
iliPreSkill6 = skill("Vitesse Lumière", "iliSkill6", TYPE_DAMAGE, power=50, range=AREA_INLINE_4, replay=True, cooldown=2, tpCac=True,use=CHARISMA, description='Vous téléporte au corps à corps de l\'ennemi ciblé et vous permet de rejouer votre tour')
iliPreSkill7Dmg = skill("Rayon de Lumière", "iliSkill7", TYPE_DAMAGE, power=150, range=AREA_CIRCLE_1, area=AREA_LINE_6, cooldown=4, use=CHARISMA,effectOnSelf= iliPreArmor, description="Inflige des dégâts sur une ligne droite puis vous procure une armure")
iliPreSkill7RedirectEff = effect("Diffraction","iliRedirect",redirection=100)
iliPreSkill7Redirect = skill('Diffraction',"iliPreSkill7",TYPE_BOOST,effects=iliPreSkill7RedirectEff,range=AREA_DONUT_7,effectOnSelf=iliPreRegen,cooldown=iliPreSkill7Dmg.cooldown)
iliPreSkill7 = skill("Jeu de lumière",'iliPreSkill7',TYPE_DAMAGE,become=[iliPreSkill7Dmg,iliPreSkill7Redirect],cooldown=4)
iliWeapEff = effect("Conviction de la Lumière", "iliWeapRegenEff", CHARISMA, power=15,turnInit=-1, unclearable=True, type=TYPE_INDIRECT_HEAL, trigger=TRIGGER_START_OF_TURN, emoji='<a:ilianaRegen:969825374093578260>')
iliWeap = weapon("Epée et Bouclier de la Lumière", "iliWeap", RANGE_MELEE, AREA_CIRCLE_1, 50, 75, charisma=30, endurance=20,resistance=15, effects=iliWeapEff, area=AREA_CIRCLE_1, ignoreAutoVerif=True, emoji=infLightSword.emoji, use=CHARISMA)

LunaPreStuffHead = stuff("Boucle d'oreille ombrale", 'lunaDarkPendant', 0, 0, endurance=int(50*0.3), agility=50,precision=int(50*0.3), strength=int(50*2.2), resistance=min(50//5, 30), percing=10, emoji=darkMaidPendants.emoji)
LunaPreStuffDress = stuff("Robe de soubrette ombrale ombrale", 'lunaDarkMaidDress', 0, 0, endurance=int(50*0.7), agility=50, precision=int(50*0.5), strength=int(50*3), percing=15, resistance=min(50//5, 40), emoji=darkMaidDress.emoji)
LunaPreStuffFlats = stuff("Ballerines ombrales", 'lunaDarkFlats', 0, 0, endurance=int(50*0.3), agility=int(50*1.3), precision=int(50*0.3), strength=int(50*2.2), resistance=min(50//5, 30), percing=10, emoji=darkMaidFlats.emoji)

lunaWeap = weapon("Épee de l'ombre éternelle","aaa",RANGE_LONG,AREA_CIRCLE_1,35,40,strength=20,agility=20,precision=20,repetition=5,emoji='<:lunaWeap:915358834543968348>',damageOnArmor=1.2,ignoreAutoVerif=True)
lunaInfiniteDarknessStun = effect("Lumière Éternelle","ilianaInfiniteLigthEff",None,type=TYPE_MALUS,stun=True,silent=True,emoji=uniqueEmoji("<:iliEff:929705167853604895>"))

lunaVulne = effect("Vulnérabilité ombrale","lunaVulné",STRENGTH,resistance=-3,turnInit=-1,emoji=vulneEmoji,type=TYPE_MALUS,stackable=True)

lunaSpe = skill("Ténèbres Éternels","InfDarkLaunch",TYPE_DAMAGE,0,235,range=AREA_CIRCLE_7,area=AREA_CIRCLE_7,emoji='<:lunaSecDamage:929705185016692786>',say=["Laissez moi vous montrer un avant goût des Ténèbres Éternels !","Arrête de toujours d'interposer comme ça !","Même toi ne peut pas contrer mes Ténèbres éternellement !","Raah cette lueur ! Cette insuportable lueur !"],description="Inflige des dégâts extrèmes après un tour de chargement",cooldown=99,initCooldown=5,ultimate=True,damageOnArmor=1.2)
lunaInfiniteDarknessShield = effect("Ténèbres Éternels","lunaInfiniteDarknessShield",STRENGTH,agility=-500,overhealth=350,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,replique=lunaSpe,turnInit=99,absolutShield=True,emoji=uniqueEmoji('<:lunaEff:929700784537477150>'))
lunaRepEffect = effect("Cast - Ténèbres Éternels","darkerYetDarker3",replique=lunaSpe,turnInit=2,silent=True,emoji=uniqueEmoji("<a:lu:916575004492169226>"))
lunaSpeCast = skill("Ténèbres Éternels","lunaInfDarkCast",TYPE_DAMAGE,0,0,emoji='<:lunaSecDamage:929705185016692786>',range=AREA_CIRCLE_7,area=AREA_CIRCLE_7,effectOnSelf=lunaRepEffect,say="Ok ça suffit ! Voyons voir comment vous tiendrez face à ça...",message="Luna concentre les Ténèbres environants...",cooldown=lunaSpe.cooldown,initCooldown=lunaSpe.initCooldown,ultimate=lunaSpe.ultimate)
lunaSkill = copy.deepcopy(soupledown)
lunaSkill.power, lunaSkill.onArmor, lunaSkill.cooldown = 180, 1.3, 4
lunaSkill2 = skill("Frappes des Ténèbres","lunaSkill2",TYPE_DAMAGE,0,150,AREA_CIRCLE_2,repetition=3,cooldown=5,initCooldown=2,damageOnArmor=1.3,emoji='<:lunaTb:932444874073063434>',say=["Je pense pas que tu va pouvoir prendre celui-ci sans broncher.","Tu as des healers non ? Donnons leur un peu de boulot !"],description="Inflige de lourd dégâts à une cible unique")
lunaSkill4Eff = copy.deepcopy(innerdarknessEff)
lunaSkill4Eff.stat,lunaSkill4Eff.power , lunaSkill4Eff.id, lunaSkill4Eff.emoji = STRENGTH, 40, "lunaSkill4Eff", uniqueEmoji('<:lunaIndi:932447879786823730>')
lunaSkill4EffAlt = copy.deepcopy(lunaSkill4Eff)
lunaSkill4EffAlt.power, lunaSkill4EffAlt.area, lunaSkill4EffAlt.id = 75 , AREA_MONO, "lunaSkill4Eff2"
lunaSkill4_1 = skill("Convertion rapprochée",'lunaSkill4',TYPE_INDIRECT_DAMAGE,0,range=AREA_MONO,area=AREA_CIRCLE_2,effects=lunaSkill4EffAlt,cooldown=3,emoji=lunaSkill4Eff.emoji[0][0],say=['Vous tenez tant à voir les Ténèbres de plus près ? Voilà pour vous !','Votre Lumière ne vous protègera pas éternellement.'],description="Donne un effet de dégâts indirect monocible aux ennemis proches")
lunaSkill4_2 = skill("Convertion externe",'lunaSkill4',TYPE_INDIRECT_DAMAGE,0,range=AREA_MONO,area=AREA_DIST_7,effects=lunaSkill4Eff,cooldown=3,emoji=lunaSkill4Eff.emoji[0][0],say=["C'est pas parceque vous restez loin que vous serez épargné !","Votre Lumière sucombera à mes Ténèbres."],description="Inflige un effet de dégâts indirect en zone aux ennemis éloignés")

lunaSkill4 = skill("Convertion","lunaSkill4",TYPE_INDIRECT_DAMAGE,0,range=AREA_CIRCLE_7,use=STRENGTH,say="Votre Lumière ne vous protègera pas éternellement !",emoji=lunaSkill4Eff.emoji[0][0],become=[lunaSkill4_1,lunaSkill4_2])
lunaSkill5_1 = skill("Reverse roundhouse-kick","lunaSkill5",TYPE_DAMAGE,0,100,AREA_CIRCLE_1,area=AREA_ARC_1,emoji='<:luna4inOne:919260128698589184>',damageOnArmor=2,description='Inflige des dégâts en zone à un ennemi au corps à corps')
lunaSkill5_2 = skill("Side-kick fouetté","lunaSkill5",TYPE_DAMAGE,0,135,AREA_CIRCLE_1,emoji='<:luna4inOne:919260128698589184>',say="Hmf !",damageOnArmor=3,description='Inflige des dégâts à une cible unique au corps à corps\nDégâts triplé sur de l\'armure')
lunaSkill5_3_eff = effect("Destabilisé","lunaSkill5_3Eff",type=TYPE_MALUS,emoji="<:stun:882597448898474024>",stun=True)
lunaSkill5_3 = skill("Sweeping into Backflip","lunaSkill5",TYPE_DAMAGE,0,80,AREA_CIRCLE_1,repetition=2,effects=lunaSkill5_3_eff,knockback=1,emoji='<:luna4inOne:919260128698589184>',say="C'est que tu es colant toi !",description='Inflige des dégâts, étourdit pendant un tour et repousse un ennemi au corps à corps')
lunaSkill5_4 = skill("Double High roundhouse-kick into Side-kick","lunaSkill5",TYPE_DAMAGE,0,40,AREA_CIRCLE_1,repetition=3,knockback=3,emoji='<:luna4inOne:919260128698589184>',say="Hé vous derrière ! Cadeau !",damageOnArmor=2,description='Inflige des dégats et repousse de 3 cases un ennemi au corps à corps')
lunaSkill6 = skill("Vitesse ombrale","lunaSkill6",TYPE_DAMAGE,0,50,AREA_INLINE_4,emoji='<:lunaDash:932286143884566528>',cooldown=2,replay=True,tpCac=True,sussess=200,description='Se téléporte au corps à corps d\'un ennemi et vous permet de rejouer votre tour')
lunaSkill7 = skill("Ultimawashi","lunaSkill7",TYPE_DAMAGE,0,150,AREA_CIRCLE_1,cooldown=3,knockback=10,sussess=200,emoji='<:ultimawashi:932378739327787078>',description="Inflige de lourd dégâts et repousse violament un ennemi au corps à corps")
lunaQuickFightEff = effect('Accélération',"lunaQuickFight",emoji=uniqueEmoji('<:qqLuna:932318030380302386>'),description="Permet au porteur de rejouer son tou une fois")
lunaSkill5Base = skill("Corps à corps","lunaSkill5",TYPE_DAMAGE,0,0,AREA_CIRCLE_1,description="Cette compétence peut avoir 4 effets différents, sélectionné de manière aléatoire",emoji='<:luna4inOne:919260128698589184>',become=[lunaSkill5_1,lunaSkill5_2,lunaSkill5_3,lunaSkill5_4])


accelerant.effects= [lunaQuickFightEff]

lunaPreSkill5_1 = copy.deepcopy(lunaSkill5_4)
lunaPreSkill5_1.cooldown, lunaPreSkill5_1.description, lunaPreSkill5_1.power = 2, "Effectue plusieurs attaques sur un adversaire\n__Puissance estimée :__ **{0}**".format(int(lunaPreSkill5_1.power*lunaPreSkill5_1.repetition)+int(lunaSkill5_2.power*lunaSkill5_2.repetition)+int(lunaSkill5_1.power*lunaSkill5_1.repetition)), int(lunaPreSkill5_1.power*1.3)
lunaPreSkill5_1_cast = effect("Enchainement 4","ench4",silent=True,replique=lunaPreSkill5_1)
lunaPreSkill5_2 = copy.deepcopy(lunaSkill5_2)
lunaPreSkill5_2.effectOnSelf, lunaPreSkill5_2.replay, lunaPreSkill5_2.power = lunaPreSkill5_1_cast, True, int(lunaPreSkill5_2.power*1.3)
lunaPreSkill5_2_cast = effect("Enchaînement 3","ench3",silent=True,replique=lunaPreSkill5_2)
lunaPreSkill5_3 = copy.deepcopy(lunaSkill5_1)
lunaPreSkill5_3.effectOnSelf, lunaPreSkill5_3.replay, lunaPreSkill5_3.description, lunaPreSkill5_3.name, lunaPreSkill5_3.power = lunaPreSkill5_2_cast, True, "Effectue plusieurs attaques sur un adversaire\n__Puissance estimée :__ **461**", "Combo Corps à Corps", int(lunaPreSkill5_3.power*1.3)
lunaPreSkill2_eff = effect("Ténèbres d'Obsidienne","lunaPreIndirect",STRENGTH,power=80,emoji='<:lunaIndi:932447879786823730>',turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE)
lunaPreSkill2 = skill("Obsidienne Ténébreuse","lunaPreSkill2",TYPE_INDIRECT_DAMAGE,emoji=lunaPandan.emoji,effects=lunaPreSkill2_eff,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_INLINE_4,lunaPreSkill2_eff],range=AREA_MONO,area=AREA_CIRCLE_4,cooldown=4,description="Inflige un effet de dégâts indirects aux ennemis alentours. Les adversaires allignés subissent une deuxième fois l'effet",replay=True)
lunaPreSkill3 = skill("Frappe d'Obsidienne","lunaPreSkill3",TYPE_DAMAGE,emoji=lunaSkill2.emoji,power=int(lunaSkill2.power*lunaSkill2.repetition*1.25),cooldown=lunaSkill2.cooldown,description="Inflige de lourd dégâts à un ennemi.\n__Puissance :__ **{power}**")
lunaDarkChoc = copy.deepcopy(lunaSkill)
lunaDarkChoc.power, lunaDarkChoc.lifeSteal, lunaDarkChoc.cooldown, lunaDarkChoc.description, lunaDarkChoc.name = 200, 15, 5, "Vous téléporte au corps à corps de l'ennemi ciblé et lui porte une attaque infligeant des dégâts de zone tout en vous restituant un pourcentage des dégâts infligés.\n__Puissance :__ **200**", "Choc d'Obsidienne"
lunaPreUltimawashi = copy.deepcopy(lunaSkill7)
lunaPreUltimawashi.area, lunaPreUltimawashi.name, lunaPreUltimawashi.description = AREA_CIRCLE_1, "Piqué Ténébreux", "Inflige des dégâts à l'ennemi ciblé ainsi qu'aux adversaires alentours, puis repousse violament ce premier.\n__Puissance :__ **{0}**".format(lunaPreUltimawashi.power)

liaExWeapEff = effect("Kazama","liaExWeapEff",turnInit=-1,unclearable=True,dodge=13,counterOnDodge=75,power=80,description="Octroi à Lia 75% de chances d'effectuer une **contre-attaque** en esquivant un assaut adverse\nLui octroi également {0}% de chance d'obtenir l'effet {1} __{2}__ en effectuant une compétence {3} __{4}__".format(50,tablElemEff[ELEMENT_AIR].emoji[0][0],tablElemEff[ELEMENT_AIR].name,elemEmojis[ELEMENT_AIR],elemNames[ELEMENT_AIR]),emoji='<:liaWeap:908859908034793552>')
liaExWeap = weapon("Akashi","noneweap",RANGE_MELEE,AREA_CIRCLE_1,power=25,sussess=90,magie=20,agility=20,resistance=10,area=AREA_ARC_1,emoji=liaKatana.emoji,ignoreAutoVerif=True,use=MAGIE,effects=liaExWeapEff)
liaExDotOnTarget = effect("U~indobaito","liaExDotOnTarget",MAGIE,power=80,turnInit=8,lvl=8,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji='<:airKitsune:917670912646602823>')
liaExSkill1_3_ready = effect("Harikenburedo préparé","liaSkill1_3_ready",turnInit=5,emoji='<:liaSki1_3:1012765729554178138>')
liaExSkill1_3 = skill("Harikenburedo","liaExSkill1",TYPE_DAMAGE,power=90,use=MAGIE,emoji='<:liaSki1_3:1012765729554178138>',range=AREA_CIRCLE_1,area=AREA_LINE_2,effects=liaExDotOnTarget,sussess=120,description="Dernier coup du combo Lame des vents\nInflige des dégâts aux ennemis ciblé et inflige {0} __{1}__ à la cible principale, lui infligeant des dégâts continues pendant {2} tours".format(liaExDotOnTarget.emoji[0][0],liaExDotOnTarget.name,liaExDotOnTarget.turnInit),needEffect=[liaExSkill1_3_ready],condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR])
liaExSkill1_2_ready = effect("Sutomubureido préparé","liaSkill1_2_ready",turnInit=5,emoji='<:liaSki1_2:1012761707858382929>')
liaExDotOnSelf = effect("Taifu no me","liaExDotOnSelf",MAGIE,power=60,area=AREA_CIRCLE_3,turnInit=8,lvl=8,type=TYPE_INDIRECT_DAMAGE,trigger=TRIGGER_END_OF_TURN,emoji='<:windBite:961185646993637476>')
liaExSkill1_2 = skill("Sutomubureido","liaExSkill1",TYPE_DAMAGE,use=MAGIE,emoji='<:liaSki1_2:1012761707858382929>',power=80,sussess=120,range=AREA_MONO,area=AREA_CIRCLE_3,effectOnSelf=liaExSkill1_3_ready,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_MONO,liaExDotOnSelf],needEffect=[liaExSkill1_2_ready],condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],description="Second coup du combo Lame des vents\nInflige des dégâts aux ennemis autour de vous et vous octroi {0} __{1}__, infligeant des dégâts aux ennemis autour de vous lorsque vous terminez votre tour pendant {2} tours".format(liaExDotOnSelf.emoji[0][0],liaExDotOnSelf.name,liaExDotOnSelf.turnInit))
liaExSkill1_1_eff = copy.deepcopy(dmgUp)
liaExSkill1_1_eff.power, liaExSkill1_1_eff.turnInit = 15, 8
liaExSkill1_1 = skill("Kaze no ha","liaExSkill1",TYPE_DAMAGE,use=MAGIE,power=75,emoji='<:liaSki1_1:1012761673427333120>',effectOnSelf=liaExSkill1_2_ready,effectAroundCaster=[TYPE_BOOST,AREA_MONO,liaExSkill1_1_eff],rejectEffect=[liaExSkill1_2_ready,liaExSkill1_3_ready],condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],range=AREA_CIRCLE_1,description="Premier coup du combo Lame des vents\nInflige des dégâts à l'ennemi ciblé et augmente vos dégâts infligés de 15% pendant 8 tours")
liaExSkill1 = skill("Combo Lame des vents","liaExSkill1",TYPE_DAMAGE,use=MAGIE,emoji='<:liaSki1_3:1012765729554178138>',become=[liaExSkill1_1,liaExSkill1_2,liaExSkill1_3],description="Permet d'effectuer le combo Lame des Vents.\n\n{0} __{1}__ augmente les dégâts infligés,\n{2} __{3}__ vous octroi un effet de dégâts indirects infligeant des dégâts autour de vous en fin de tour\n{4} __{5}__ inflige un effet de dégâts indirect à la cible, lui infligeant des dégâtts lorsqu'il débute son tour".format(liaExSkill1_1.emoji,liaExSkill1_1.name,liaExSkill1_2.emoji,liaExSkill1_2.name,liaExSkill1_3.emoji,liaExSkill1_3.name))
liaExSkill2_2_ready = effect("Shapuchajido préparé","liaExSkill2_2_ready",turnInit=5,emoji='<:liaCounter:998001563379437568>')
liaExSkill2_2 = skill("Shapuchajido","liaExSkill2",TYPE_DAMAGE,power=35,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],range=AREA_CIRCLE_4,tpCac=True,replay=True,use=AGILITY,emoji='<:liaCounter:998001563379437568>',needEffect=[liaExSkill2_2_ready],description="Charge l'ennemi ciblé, lui inflige des dégâts et vous permet de rejouer votre tour")
liaExSkill2_1_deney = effect("Terukikku impossible","liaExSkill2_1_deney",turnInit=4,silent=True,emoji='<:liaSkill:922291249002709062>')
liaExSkill2_1 = skill("Terukikku","liaExSkill2",TYPE_DAMAGE,power=100,range=AREA_CIRCLE_4,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],area=AREA_CONE_2,tpCac=True,knockback=3,description="Charge l'ennmi ciblé, lui inflige des dégâts et le repousse de 3 cases\nVous octroi également la possibilité d'utiliser {0} __{1}__ une fois durant les {2} prochains tours".format(liaExSkill2_2.emoji,liaExSkill2_2.name,liaExSkill2_2.needEffect[0].turnInit),effectOnSelf=liaExSkill2_2.needEffect[0],effectAroundCaster=[TYPE_MALUS,AREA_MONO,liaExSkill2_1_deney],rejectEffect=[liaExSkill2_1_deney],emoji='<:liaSkill:922291249002709062>')
liaExSkill2 = skill("Terukikku +","liaExSkill2",TYPE_DAMAGE,power=liaExSkill2_1.power,use=AGILITY,emoji=liaExSkill2_1.emoji,become=[liaExSkill2_1,liaExSkill2_2],description="Inflige des dégâts agilité à l'ennemi ciblé.\n\n{0} __{1}__ permet de rejouer son tour\n{2} __{3}__ ne peut pas être utilisé pendant 4 tours après utilisation".format(liaExSkill2_2.emoji, liaExSkill2_2.name, liaExSkill2_1.emoji, liaExSkill2_1.name))
liaExSkill3_eff = effect("Hariken no me","liaExSkill3_eff",MAGIE,area=AREA_DIST_5,trigger=TRIGGER_END_OF_TURN,type=TYPE_INDIRECT_DAMAGE,emoji=liaExDotOnSelf.emoji[0][0],power=135,lvl=5,turnInit=5)
liaExSkill3 = skill("Hariken","liaExSkill3",TYPE_DAMAGE,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],power=100,range=AREA_MONO,area=AREA_CIRCLE_2,cooldown=5,use=MAGIE,effectOnSelf=liaExSkill3_eff,emoji=liaExSkill3_eff.emoji[0][0],description="Inflige et repousse les ennemis en mêlée et vous octroi un effet infligeant des dégâts aux ennemis éloignés à la fin de votre tour pendant 3 tour",knockback=2)
liaExSkill4_3 = skill("Keifu","liaExSkill4",TYPE_DAMAGE,power=100,effectAroundCaster=[TYPE_HEAL,AREA_MONO,150],use=MAGIE,cooldown=5,description="Inflige des dégâts aux ennemis alliégné avec vous et vous soigne",area=AREA_INLINE_5,range=AREA_MONO,emoji="<:waterKitsune:917670866626707516>")
liaExSkill4_2_eff = effect("Asuama","liaExSkill4_2_eff",MAGIE,overhealth=100,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji='<:liaWindArmor:1013901987303149630>')
liaExSkill4_2 = skill("Sunaarashi","liaExSkill4",use=MAGIE,types=TYPE_DAMAGE,power=125,range=AREA_MONO,area=AREA_CIRCLE_2,effectOnSelf=liaExSkill4_2_eff,cooldown=liaExSkill4_3.cooldown, emoji="<:earthKitsune:917670882586017792>", description="Inflige des dégâts aux ennemis en mêlée et vous octroi une armure pendnant 3 tours")
liaExSkill4_1_dot = effect("Moeta","liaExSkill4_1_dot",MAGIE,power=35,turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE)
liaExSkill4_1 = skill("Sabaku no kaze","liaExSkill4",TYPE_DAMAGE,area=AREA_ALL_ENEMIES,use=MAGIE,range=AREA_MONO,power=25,description="Inflige des dégâts à tous les ennemis et leur inflige un effet de dégâts indirect pendant 3 tours",effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_ALL_ENEMIES,liaExSkill4_1_dot],cooldown=liaExSkill4_3.cooldown,emoji='<:fireKitsune:917670925904785408>')
liaExSkill4 = skill("Kyodai no kyoka","liaExSkill4",TYPE_DAMAGE,use=MAGIE,initCooldown=2,power=max(liaExSkill4_3.power,liaExSkill4_2.power,liaExSkill4_1.power+liaExSkill4_1_dot.power*liaExSkill4_1_dot.turnInit),become=[liaExSkill4_1,liaExSkill4_2,liaExSkill4_3],emoji='<:kitsuWeap:935553775500947486>',description="Permet d'utiliser les éléments des soeurs de Lia pour déclancher une attaque suivant leur élément.\n\n{0} __{1}__ vous soigne en plus d'infliger des dégâts\n{2} __{3}__ vous octroi une armure en plus d'infliger des dégâts".format(liaExSkill4_3.emoji,liaExSkill4_3.name,liaExSkill4_2.emoji,liaExSkill4_2.name))
liaExUlt_4 = skill("Kaze no bakuhatsu","liaExUlt_4",TYPE_DAMAGE,power=110,cooldown=7,ultimate=True,area=AREA_CIRCLE_1,range=AREA_CIRCLE_3,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],emoji='<:liaSkiUlt3:1013889062962217021>',description="Au premier tour, inflige des dégâts aux ennemis en mêlée et les repoussent.\nAu second tour, inflige à deux reprises des dégâts dans une zone en arc de cercle centrée sur l'ennemi ciblé, repoussant les ennemis touchés et vous téléportant au corps à corps de la cible à chaque reprise, puis inflige des dégâts en cercle autour de l'ennemi ciblé\n\nChaque effet {0} __{1}__ possédé au premier tour vous octroi une armure équivalante à **5%** de vos PV Max\nChaque effet {0} __{1}__ possédé augmente les puissances des attaques en arc de cercle du second tour de **10%**\nChaque effet {0} __{1}__ possédé augmente la puissance de l'attaque de zone de **15%** et les consommes pour vous soigner de **5%** de vos PV max".format(tablElemEff[ELEMENT_AIR].emoji[0][0],tablElemEff[ELEMENT_AIR].name),sussess=200,use=MAGIE)
liaExUlt_4_cast = effect("Enchainement - {replicaName}","liaExUlt_4_c",replique=liaExUlt_4,silent=True)
liaExUlt_3 = skill("Gyakufu no suraisu","liaExUlt_3",TYPE_DAMAGE,power=70,area=AREA_ARC_3,tpCac=True,knockback=1,range=liaExUlt_4.range,condition=liaExUlt_4.condition,description=liaExUlt_4.description,cooldown=liaExUlt_4.cooldown,replay=True,effectOnSelf=liaExUlt_4_cast,emoji='<:liaSkiUlt2:1013889034600329246>',use=MAGIE)
liaExUlt_3_cast = effect("Enchainement - {replicaName}","liaExUlt_3_c",replique=liaExUlt_3,silent=True)
liaExUlt_2 = skill("Kaze no suraisu","liaExUlt_2",TYPE_DAMAGE,power=70,area=AREA_ARC_3,tpCac=True,knockback=1,range=liaExUlt_4.range,condition=liaExUlt_4.condition,description=liaExUlt_4.description,cooldown=liaExUlt_4.cooldown,replay=True,effectOnSelf=liaExUlt_3_cast,emoji='<:liaSkiUlt1:1013889002731995246>',use=MAGIE)
liaExUlt_2_cast = effect("Cast - {replicaName}","liaExult_2_c",turnInit=2,silent=True,replique=liaExUlt_2)
liaExUlt_1 = skill("Ririsu","liaExUlt",TYPE_DAMAGE,power=25,range=AREA_CIRCLE_3,ultimate=True,area=AREA_CIRCLE_2,areaOnSelf=True,cooldown=liaExUlt_4.cooldown,effectOnSelf=liaExUlt_2_cast,emoji='<:liaSkiUlt0:1013889091831599178>',description=liaExUlt_4.description,condition=liaExUlt_4.condition,knockback=3,use=MAGIE)
liaExSkill6 = skill("Déployable - Tatsumaki","liaExSkill6",TYPE_DEPL,emoji='<:liaDepl:1013912739728592896>',use=MAGIE,range=AREA_CIRCLE_2,cooldown=7,depl=liaTornade,description="Invoque une tornade sur la cellule ciblée, infligeant des dégâts à chaque début de table aux ennemis à portée",condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR])
liaExSkill7_eff = effect("Kaze no shinkiro","liaExSkill7_e",emoji='<:liaSki6:1013891089662488596>',dodge=100,counterOnDodge=100)
liaExSkill7 = skill("Kaze no shinkiro","liaExSkill7",TYPE_ARMOR,effects=liaExSkill7_eff,cooldown=5,condition=[EXCLUSIVE,ELEMENT,ELEMENT_AIR],use=None,range=AREA_MONO,emoji='<:liaSki6:1013891089662488596>',description="Augmente votre probabilité d'esquive et de contre-attaque de **100%** jusqu'à votre prochain tour")

liaExSkill4_3.description += "\nPartage le même temps de rechargement que {0} __{1}__ et {2} __{3}__".format(liaExSkill4_2.emoji,liaExSkill4_2.name,liaExSkill4_1.emoji,liaExSkill4_1.name)
liaExSkill4_2.description += "\nPartage le même temps de rechargement que {0} __{1}__ et {2} __{3}__".format(liaExSkill4_3.emoji,liaExSkill4_3.name,liaExSkill4_1.emoji,liaExSkill4_1.name)
liaExSkill4_1.description += "\nPartage le même temps de rechargement que {0} __{1}__ et {2} __{3}__".format(liaExSkill4_2.emoji,liaExSkill4_2.name,liaExSkill4_3.emoji,liaExSkill4_3.name)

# Tabl var allies =============================================================================
tablVarAllies = [
    tmpAllie("Luna", 1, black, POIDS_PLUME, infDarkSword, [lunaPandan, lunaDress, lunaBoots], GENDER_FEMALE, [defi, splatbomb, ironStormBundle, soupledown, highkick, calestJump, foullee],"Là où se trouve la Lumière se trouvent les Ténèbres", [ELEMENT_DARKNESS, ELEMENT_LIGHT], variant=True, icon='<:luna:909047362868105227>', bonusPoints=[STRENGTH, ENDURANCE], say=lunaSays),
    tmpAllie("Altikia", 2, 0xDFFF92, VIGILANT, fleau, [zenithHat, zenithArmor, zenithBoots], GENDER_FEMALE, [ironWillSkill, altyCover, lightBigHealArea, renisurection, concen, clemency, regenVigil],"Une personnalité de Gwen qui préfère se concentrer sur ses alliés", [ELEMENT_LIGHT, ELEMENT_FIRE], variant=True, bonusPoints=[ENDURANCE, CHARISMA], icon='<:alty:906303048542990347>', say=altySays),
    tmpAllie("Klironovia", 2, 0xF49206, BERSERK, klikliSword, [butterflyEarRingsDark, darkChemVeste, darkButterFlyBoots], GENDER_FEMALE, [demolish, bloodBath, bloodyStrike, absorbingStrike2, klikliStrike, legStrike, bloodPact],"Une personnalité de Gwen bien plus violente que les deux autres", [ELEMENT_EARTH, ELEMENT_TIME], variant=True, bonusPoints=[STRENGTH, AGILITY], icon='<:klikli:906303031837073429>', say=klikliSays),
    tmpAllie("Shihu", 1, 0x00002D, MAGE, darkMetRuneMid, [shihuHat, shihuDress, shihuShoe], GENDER_FEMALE, [dark2, dark3, findSkill("Extra Obscurité"), darkBoomCast, quickCast, findSkill("Extra Pénombre"), maitriseElementaire],"\"Eye veut zuste un pi d'attenchions...\" - Shushi", [ELEMENT_DARKNESS, ELEMENT_SPACE], variant=True, icon='<:shihu:909047672541945927>', bonusPoints=[MAGIE, STRENGTH], say=shihuSays),
    tmpAllie("Shushi Cohabitée", 1, 0x0303D5, PREVOYANT, shushiWeap, [shushiHat, shushiDress, shushiBoots], GENDER_FEMALE, [shushiSkill1, shushiArmorSkill, shushiSkill3, shushiSkill4, shushiSkill5],"S'étant comprise l'une et l'autre, Shushi et Shihu ont décidé de se liguer contre la mère de cette dernière.\nCette allié temporaire n'apparait que contre le boss \"Luna\"", [ELEMENT_LIGHT, ELEMENT_DARKNESS], True, icon='<:shushiCoa:915488591654842368>', bonusPoints=[MAGIE, AGILITY]),
    tmpAllie("Alice Exaltée", 1, aliceColor, ALTRUISTE, aliceExWeap, [aliceExHeadruban, aliceExDress, aliceExShoes], GENDER_FEMALE, [aliceRez, aliceSkill1, aliceSkill2, aliceSkill3, aliceSkill4, aliceSkill5, aliceSkill6], "Voyant qu'elle n'arriverai pas à ramener sa sœur à la raison, Alice a décider d'aller contre ses principes et de révéler toute sa puissance vampirique pour tenter de redresser la balance.\nN'apparait que contre Clémence possédée", element=[ELEMENT_LIGHT, ELEMENT_FIRE], variant=True, deadIcon="<:AliceOut:908756108045332570>", icon="<a:aliceExalte:914782398451953685>", bonusPoints=[CHARISMA, ENDURANCE], say=aliceExSays),
    tmpAllie("Clémence Exaltée", 2, 0x8F001C, MAGE, clemExWeapon, [miniStuff, miniStuff, miniStuff], GENDER_FEMALE, [clemExSkill1, clemExSkill2, clemExSkill3, clemExSkill4, clemExSkill5, clemExSkill6, clemExSkill7], "WIP, revenez plus tard", [ELEMENT_DARKNESS, ELEMENT_LIGHT], icon='<:clemence:908902579554111549>', bonusPoints=[MAGIE, STRENGTH], say=clemExSay, deadIcon='<:AliceOut:908756108045332570>',variant=True),
    tmpAllie('Iliana prê.', 1, white, VIGILANT, iliWeap, [miniStuffHead, miniStuffDress, miniStuffFlats], GENDER_FEMALE, [iliPreSkill4, iliPreSkill5, iliPreSkill6, iliPreSkill1, iliPreSkill2, iliPreSkill3, iliPreSkill7], element=[ELEMENT_LIGHT, ELEMENT_LIGHT], deadIcon='<:oci:930481536564879370>', icon='<:Iliana:926425844056985640>', bonusPoints=[CHARISMA, ENDURANCE], description="Face à une menace dimensionnelle sans précédents, Iliana a décider de réveiller ses pouvoirs de Prêtresse de la Lumière pour faire équipe avec celle des Ténèbres",say=ilianaPreSays,variant=True),
    tmpAllie('Belle', 2, 0x1f0004, ENCHANTEUR, magicSwordnShield, [magicArmorHelmet, magicArmorBody, magicArmorBoots], GENDER_FEMALE, [ferocite, spectralCircle, darkAmb, spectralFurie, magicRuneStrike, strengthOfDesepearance, undead], element=[ELEMENT_DARKNESS, ELEMENT_NEUTRAL], variant=True, icon='<:belle:943444751288528957>', bonusPoints=[ENDURANCE, MAGIE]),
    tmpAllie("Luna prê.", 1, black, POIDS_PLUME, lunaWeap, [LunaPreStuffHead, LunaPreStuffDress, LunaPreStuffFlats], GENDER_FEMALE, [lunaSpeCast,lunaDarkChoc,lunaPreSkill5_3,lunaPreSkill3,lunaPreSkill2,lunaSkill6,lunaPreUltimawashi], element=[ELEMENT_DARKNESS, ELEMENT_DARKNESS], icon='<:luna:909047362868105227>', bonusPoints=[STRENGTH, AGILITY], say=lunaPreSays,variant=True, description = "Face à une menace temporelle sans précédents, Luna a décidé de réveiller ses pouvoirs de Prêtresse des Ténèbres pour faire équipe avec celle de la Lumière"),
    tmpAllie("Chûri-Hinoro", 1,orange, MAGE, phenixLeath, [on45Hat, on45Dress, on45Shoes], GENDER_FEMALE, churInoSkills, description="En utilisant la compétence \"Envolée du Phenix\", Chûri devient Chûri-Hinoro, modifiant son élément et ses compétences", element=[ELEMENT_FIRE,ELEMENT_EARTH],deadIcon="<:fairyOut:935335430814068786>",icon='<:churHi:994045813175111811>',bonusPoints=[MAGIE,PRECISION],say=churiSays,variant=True),
    tmpAllie("Lia Ex",2,0xBBFFCB,POIDS_PLUME,liaExWeap,[greenbutbar,greenbutterflyshirt,greenbutterflysandals],GENDER_FEMALE,[liaExSkill1,liaExSkill2,liaExSkill3,liaExSkill4,liaExUlt_1,liaExSkill6,liaExSkill7],description="Suite à l'émergeance d'une nouvelle menage, afin de protéger ses frères et soeurs et comme épreuve de sa mère, Lia a du mettre son masque de démon renard et se jeter corps et âme contre leur ennemi d'ombre",element=[ELEMENT_AIR,ELEMENT_AIR],deadIcon="<:kitsuSisterDead:908756093101015100>",icon="<:liaEx:1012669139711696928>",bonusPoints=[MAGIE,AGILITY],limitBreaks=[[MAGIE,AGILITY,ENDURANCE],5]),
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
    "C'est tout {target} ?"
]

# Balancing
areaDmgReductionTmp = effect("Dégâts de zone réduits","areaDmgReductionTmp",emoji='<:aoeDown:979953519350149130>',power=15,turnInit=-1,unclearable=True,type=TYPE_MALUS,description="Les dégâts infligés par les compétences à zone d'effet sont réduits de **{0}%** sur les cibles secondaires")
healReductionTmp = effect("Soins effectués réduits","healReductionTmp",emoji='<:healDown:979953539918987315>',power=10,turnInit=-1,unclearable=True,type=TYPE_MALUS,description="La puissance des soins effectués est réduite de **{0}%**")
armorReductionTmp = effect("Armure donnée réduite","armorReductionTmp",emoji='<:armorDown:979953578556948531>',power=10,turnInit=-1,unclearable=True,description="Réduit la puissance des armures données de **{0}%**",type=TYPE_MALUS)
monoDmgReductionTmp = effect("Dégâts monocibles réduits","monoDmgReductionTmp",emoji='<:monoDown:979953496218533918>',power=10,turnInit=-1,unclearable=True,description="Réduit les dégâts monocibles infligés de **{0}%**",type=TYPE_MALUS)
healReciveReductionTmp = effect("Soins reçus diminués","healReciveReductionTmp",emoji="<:recivedHealDown:979953560689197117>",power=10,turnInit=-1,unclearable=True,description="Réduit les soins reçus de **{0}%**",type=TYPE_MALUS)
indDealReducTmp = effect("Dégâts indirects infligés réduits","indirectDealReducTmp",emoji="<:lenapy:979953598807031918> ",power=10,turnInit=-1,unclearable=True,description="Réduit les dégâts indirects infligés de **{0}%**",type=TYPE_MALUS)

specLohiReduc = copy.deepcopy(indDealReducTmp)
specLohiReduc.power = 20
specBeneReduc = copy.deepcopy(monoDmgReductionTmp)
specBeneReduc.power = 20
tmpBalancingDict = {
    "Ly":indDealReducTmp,
    "Iliana":healReductionTmp,
    "Hélène":healReductionTmp,
    "Julie":healReductionTmp,
    "Edelweiss":armorReductionTmp,
    "Icealia":armorReductionTmp,
    "Ruby":areaDmgReductionTmp,
    "Altikia":healReductionTmp,
    "Bénédicte":specBeneReduc,
    "Gwendoline":healReciveReductionTmp,
    "Hina":areaDmgReductionTmp,
    "Powehi":healReciveReductionTmp,
    "Lohica":specLohiReduc,
    "Shehisa":indDealReducTmp,
    "Elina":healReductionTmp,
}

def simulAdapTempStats(name:str):
    try:
        procurData = procurTempStuff[name]
        ent = copy.deepcopy(findAllie(name))
        ent.changeLevel(55)
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

lohicaReactHinaDeath = [
    "Tss, encore par terre toi ?",
    "Un jour il va falloir que tu apprenne à voler de tes propres ailes tu sais ?",
    "À trop vouloir toucher le ciel on fini par se brûler les ailes."
]

PROBLENAMSG = 15
lenaNotKillMsg = ["Mais tu va creuver oui ?","Tu prendras pas toutes te les prendre sans broncher."]
lenaMissMsg = ["T'en fais pas je te raterais pas la prochaine fois.","Pas la peine de prendre la grosse tête, je te raterais pas la prochaine fois.","Juste un coup de chance."]
lenaReactTmpDeath = {
    "Clémence":"Hé bah alors Clémence ? Fatiguée aujourd'hui ?\"\n<:clemence:908902579554111549> : \"Oh la ferme toi.",
    "Alice":"`Soupir`Je t'ai déjà dit d'essayer de ne pas trop te de perdre de vue en combat Alice",
    "Ly":"Faute d'inatention ?",
    "Amary":"Petite fleur partie trop tôt",
    "Edelweiss":"Elle devrait plus se concentrer sur elle même plutôt que supporter pour les autres..."

}

#simulAdapTempStats("Clémence Exaltée")

if datetime.now().month == 9:
    for cmpt in range(len(tablAllAllies)):
        if tablAllAllies[cmpt].isNpc("Félicité"):
            tablVarAllies.append(tablAllAllies[cmpt])
            tablAllAllies.remove(tablAllAllies[cmpt])
            break

findAllie("Alice").changeDict = [tempAltBuilds(33,POIDS_PLUME,aliceFan,[dans50Hat,dans50Dress,dans50Shoes],[finalTech,swordDance,aliceFanDanse,comboFanCelest,danseStarFall,tangoEnd,partner],[ELEMENT_SPACE,ELEMENT_LIGHT],[AGILITY,CHARISMA])]
findAllie("Hélène").changeDict = [tempAltBuilds(33,SORCELER,butterflyP,[critIndHat45,critIndBody45,critIndShoes45],[infectFiole,epidemic,intox,expoHeal,propaUltLaunch,propag,quadFleau],[ELEMENT_DARKNESS,ELEMENT_LIGHT],[MAGIE,INTELLIGENCE])]
findAllie("Amary").changeDict = [tempAltBuilds(30,ALTRUISTE,stuffs=findAllie("Hélène").stuff,skills=[mend,lifeSeed,lillyTransform,cure,roseeHeal,renisurection,asile],elements=[ELEMENT_LIGHT,ELEMENT_WATER],bonusPoints=[CHARISMA,PRECISION])]
findAllie("Shehisa").changeDict = [tempAltBuilds(40,stuffs=findAllie("Luna").stuff,skills=[dissimulation,physTraqnard,UmbralTravel,bundleFetu,carnage,assasinate,antConst],elements=[ELEMENT_DARKNESS,ELEMENT_DARKNESS],bonusPoints=[STRENGTH,AGILITY])]
findAllie("Julie").changeDict = [tempAltBuilds(45,SORCELER,magicWood,stuffs=findAllie("Lohica").stuff,skills=[dephaIncant,ice2,lizSKillSus,clock,hourglass,magAchSkill,fairyTraqnard],elements=[ELEMENT_TIME,ELEMENT_DARKNESS],bonusPoints=[MAGIE,INTELLIGENCE])]
findAllie("Gwendoline").changeDict =[tempAltBuilds(55,POIDS_PLUME,mainLibre,skills=[elipseTerrestre,piedVolt,retourneImpactant,demolish,legStrike,hearthFrac,ebranlement])]

lenaShuRedirect = effect("Protection Maternelle","materProtect",redirection=100,unclearable=True,turnInit=-1,emoji='<:analyse:1003645750225412257>')
