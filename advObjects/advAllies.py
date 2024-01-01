from traceback import print_exc
from classes import *
from constantes import *
from advObjects.advWeapons import *
from advObjects.advSkills import *
from advObjects.advStuffs import *
from advObjects.advInvocs import *
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

# Alliés temporaires =============================================================================
tablAllAllies = [
    tmpAllie("Lena", 1, light_blue, OBSERVATEUR, splatcharger, [amethystEarRings, lightBlueJacket, lightBlueFlats], GENDER_FEMALE, [analysedShot, mysticShot, lenaDrone1, cryoChargeBundle, doubleShot, ricochetSolo, preciseShot],"Une inkling qui en a vu des vertes et des pas murs.\nPréfère rester loin de la mêlée et abattre ses ennemis à bonne distance", [ELEMENT_WATER, ELEMENT_EARTH], icon='<:lena:909047343876288552>', bonusPoints=[STRENGTH, PRECISION, ENDURANCE], say=lenaSays,birthday=(19,1),limitBreaks=[[STRENGTH,PRECISION],5],charSettings=lenaIa ,splashIcon='<:lena:1106478667871289455>'),
    tmpAllie("Gwendoline", 2, 0xFFFF6B, PROTECTEUR, gWeap, gwenStuffTabl, GENDER_FEMALE, [royaleGardeSkill,impact,heartStone,gwenCharge,gwenPenta,justiceEnigma,gwenyQCombo],"Bien qu'elle essaye de l'éviter, cette jeune femme se retrouve toujours à devoir en venir aux mains pour se débarraser des gros lourds de la première ligne ennemie.\nIl est vrai aussi qu'elle n'est pas toute seule dans sa tête", [ELEMENT_EARTH, ELEMENT_SPACE], bonusPoints=[STRENGTH, ENDURANCE, AGILITY], icon='<:gweny:906303014665617478>', say=gwenySays, birthday=(9,9), splashIcon='<:gwendoline:1126633253047124108>'),
    tmpAllie("Clémence", 2, 0x8F001C, MAGE, rapiere, [redbutbar, corruptRedVeste, corruptRedBoots], GENDER_FEMALE, [sanguisGladio, sanguisGladio2, umbraMortis, bloodmissiles, findSkill("Éminence"), umbraMortis, sectumsempra], "Clémence est née orpheline, ses parents ayant été tués par des chasseresses d'Arthémis peut après sa naissance.\nElle fût donc élevée par des chauve-souris dans une grotte pendant une bonne partie de son enfance\nCependant, elle rencontra dans un lieu nommé la \"Ville Onirique\", une ville magique accessible via les rêves permettant aux vampires vivants comme mort de s'y retrouver, une jeune vampire majeure du nom de Ruby.\nCette dernière lui apprit les bases de la magie au fils des années, ainsi que celles des sociétés humaines que les chauve-souris pouvaient évidamment pas lui apprendre.\n\nMalgré tout, elle manquait d'amis vampire \"réels\", Ruby habitant à des centaines de kilomètres dans la réalité. Elle alla donc, par une belle soirée d'Haloween, mordre une jeune femme envers laquelle Clémence avait un bon sentiment.\nOn peut dire que sur tous les choix qu'elle a fait, ça allait être celui qui allait être le plus lourd en conséquence, dans de bons comme mauvais thermes.\n\nJe vous en passe et des meilleurs, sinon je vais casser la limite de caractères, mais en grandissant, Clémence a continué son apprentissage de la magie et a décidé de parcourir le monde pour étudier les Anciennes Runes ainsi que pour purifier les artéfacts maudits qui tourmentent les monstres pour éviter qu'ils se fassent chasser par les humains, tel ses parents biologiques", [ELEMENT_DARKNESS, ELEMENT_FIRE], icon='<:clemence:908902579554111549>', bonusPoints=[MAGIE, INTELLIGENCE], say=clemSays, deadIcon='<:AliceOut:908756108045332570>',birthday=(31,10),limitBreaks=[[MAGIE],10],charSettings=clemIa,splashIcon='<:clemence:1088483909454536784>',splashArt="https://media.discordapp.net/attachments/640667220124499988/1088478369596838048/Sans_titre_60_20230323160331.png?width=380&height=676",team=NPC_DEMON),
    tmpAllie("Alice", 1, aliceColor, IDOLE, micPink, [butterflyPendantPink, pinkChemVeste, pompomShoes], GENDER_FEMALE, [aliceDance, courage, invocBat2, roses, requiem, corGra, synastie], "Alice est la petite dernière des trois sœurs Kohishu, et la seule à être une vampire\n\nDès son plus jeune âge, elle a fortement démontré sa volontée à vouloir être le centre de l'attention, bien que ça ai frustrée sa sœur ainée. En grandissant, cette envie de reconnaissance ne s'est pas vraiment tarie, et a réussi grâce à son charme naturel à devenir rapidement une fille populaire\n\nElle décida de suivre la voie de sa mère et de devenir une chanteuse renommé, c'est ainsi qu'elle participa au concours de jeune talent de son école et réussi à se faire remarquer par une maison de disque qui recherchait de jeunes chanteurs\n\nLorsqu'elle n'est pas retenue par ses obligations, elle aime bien accompagner Félicité et Clémence dans leurs aventures, mais refuse de participer activement aux combats. À la place elle les encourages avec ses chansons légèrement magiques", [ELEMENT_SPACE, ELEMENT_WATER], icon='<:alice:908902054959939664>', bonusPoints=[CHARISMA, INTELLIGENCE], say=aliceSays, deadIcon='<:AliceOut:908756108045332570>',birthday=(14,6),limitBreaks=[[CHARISMA],10],charSettings=preDefCharSet[2][1][1][2],splashArt='https://media.discordapp.net/attachments/640667220124499988/1069699168714625034/Sans_titre_25_20230130201824.png?width=456&height=676',splashIcon='<:alice:1069700207345946715>',team=NPC_HOLY,trait=[TRAIT_ARACHNOPHOBE,TRAIT_HIGHLIGHTED]),
    tmpAllie("Shushi", 1, 0x0303D5, ENCHANTEUR, eclatanaDoto, [shushi50Hat,shushi50Dress,shushi50Shoes], GENDER_FEMALE, [squidRoll, bundleCaC, waterCircle, krakenCharge, findSkill("skx"), magicRuneStrike, findSkill("sfz")],"Une jeune fille plutôt douée en esquive plutôt espiègle", [ELEMENT_WATER, ELEMENT_SPACE], icon='<:shushi:909047653524963328>', bonusPoints=[MAGIE, ENDURANCE], say=shushiSays,birthday=(26,9),charSettings=preDefCharSet[0][1][2][2]),
    tmpAllie("Lohica", 1, purple, SORCELER, secretum, [darFlumOr, corruptPurpleVeste, corruptPurpleBoots], GENDER_FEMALE, [lohicaFocal, fairyRay, fairyLiberation, propag, heriteEstialba, lohicaBrouillad, fairyBomb],"Une fée à l'histoire bien mouvementée. Spécialisée dans les poisons", [ELEMENT_DARKNESS, ELEMENT_DARKNESS], bonusPoints=[MAGIE, INTELLIGENCE], icon='<:lohica:919863918166417448>', deadIcon='<:flowernt:894550324705120266>',team=NPC_FAIRY,birthday=(27,7),trait=[TRAIT_ARACHNOPHOBE]),
    tmpAllie("Hélène", 2, white, ALTRUISTE, heleneBrush, [butterflyEarRingsWhite, whiteChemVeste, whiteButterFlyBoots], GENDER_FEMALE, [radiance, lapSkill, renisurection, fairyGarde, reconst, revif, lifeFontain],"Une fée qui est spécialisée dans les soins héritée de sa lignée paternelle. Cependant l'influence de sa mère a pas mal joué sur son tempérament, lui donnant des envies de meurtres, parfois. Après tout, tuer ses ennemis l'empêche d'infliger des dégâts à ses alliés", [ELEMENT_WATER, ELEMENT_WATER], bonusPoints=[CHARISMA, INTELLIGENCE], splashIcon='<:helene:1183494550384291951>', icon='<:helene:906303162854543390>',charSettings=preDefCharSet[1][1][1][2], deadIcon='<:fairyOut:935335430814068786>',team=NPC_FAIRY,trait=[TRAIT_ARACHNOPHOBE]),
    tmpAllie("Félicité", 1, red, TETE_BRULE, dtsword, [celestBronzeHat, celestBronzeArmor, celestBronzeBoots], GENDER_FEMALE, [bloodyStrike, antConst, deterStrike, strengthOfWillCast, convictTet, fragmentation, absorbingStrike2], "Soeur ainée de Sixtine et Alice, Félicité est née dans un monde désolé et post apocaliptique\n\n<:lena:909047343876288552> : Mais parle pour toi !\n\nN'ayant plus aucun humain dans ce monde pas si désolé et pas si post apocaliptique, elle hérita de l'âme de Détermination de ce monde (ainsi que quelques bénédictions de dieux grecs mais c'est une autre histoire\n\nEn grandissant, ces dites bénédictions lui ont permis de développer rapidement son esprit et ses capacités, mais aussi d'attirer sur elle tous les monstres mythologiques du coin. Fort heureusement elle pu compter sur ses parents ainsi que sur sa sœur adoptive ainnée Clémence pour la protéger jusqu'au jour où elle en a eu marre de devoir laisser les autres la défendre.\nElle alla donc trouver les seuls autres personnes avec des âmes de Détermination à sa connaissance : Frisk et Chara, qui lui apprirent les bases. Sa volontée ainsi que ses bénédictions lui permirent de rapidement faire des progrès dans l'escrime, quand pour la maîtrise de la magie, c'est grâce à Hécate qu'elle le doit\n\nEn grandissant, elle a choisi une voie plus ou moins similaire à celle de Clémence, c'est à dire de chercher à purifier des artéfacts maudits agitants les monstres alentours ainsi que l'étude d'ancienne magie. Cependant, là où Féli le fait pour protéger les populations d'hommes, Clémence le fait pour protéger les monstres de ces derniers. Mais ça ne les empêche pas de faire équipe de temps en temps. Après tout le but reste le même", bonusPoints=[ENDURANCE, STRENGTH], icon='<:felicite:909048027644317706>', element=[ELEMENT_UNIVERSALIS_PREMO,ELEMENT_UNIVERSALIS_PREMO],birthday=(10,6),limitBreaks=[[STRENGTH,ENDURANCE,CHARISMA,AGILITY,PRECISION,INTELLIGENCE,MAGIE],2],say=feliSays,splashIcon="<:felicite:1116861426556997653>",trait=[TRAIT_ARACHNOPHOBE]),
    tmpAllie("Akira", 2, black, TETE_BRULE, fauc, [nemeBracelet, nemeManteau, nemeBottes], GENDER_MALE, [deathShadow, defi, absorbingStrike2, bundleLemure, theEndCast, bundleFetu, comboFaucheCroix],"Fils aîné des Fluwaraito, Akira est un jeune garçon au sang chaud qui ne renonce jamais à un affrontements. En revanche évitez de le mettre en colère.", [ELEMENT_DARKNESS,ELEMENT_EARTH], bonusPoints=[ENDURANCE, STRENGTH], icon='<:akira:909048455828238347>'),
    tmpAllie("Icealia", 2, light_blue, PREVOYANT, blueButterfly, [icealiaHat, icealiaManteau, icealiaBoots], GENDER_FEMALE, [soulagement, royalShield, pandaima, firstArmor, lightPulse, shell, elemShield],"Une ancienne garde royale du royaume des Elfes des Glaces, qui a aujourd'hui disparu avec le Cataclysme.\nArpente le monde à la dérive en tant qu'aventurière, elle a fini par s'associer à un duo de fée, bien que leurs espèces s'entendent en général assez mal", element=[ELEMENT_LIGHT, ELEMENT_LIGHT], bonusPoints=[INTELLIGENCE, ENDURANCE], icon='<:icealia:909065559516250112>'),
    tmpAllie("Powehi", 2, black, MASCOTTE, grav, [starBar, bhPull, bhBoots], GENDER_FEMALE, [blackHole, isolement, blindage, cosmicPower, inkRes2, graviton, concen], "Une manifestation cosmique d'un trou noir. Si vous vous sentez attiré par elle, c'est probablement à raison\nNe lui demandez pas de vous marchez dessus par contre, si vous voulez un conseil. Elle a beau paraître avoir un petit gabarie, ce n'est pas pour rien qu'elle évite de marcher sur le sol", element=[ELEMENT_SPACE, ELEMENT_SPACE], bonusPoints=[ENDURANCE, INTELLIGENCE], icon='<:powehi:909048473666596905>', deadIcon='<:powehiDisiped:907326521641955399>', say=powehiSays, splashIcon='<:powehi:1128584646779752498>'),
    tmpAllie("Shehisa", 1, purple, TETE_BRULE, shehisa, [redBatEarRingsred , batRedChemVeste, redBatBoots], GENDER_FEMALE, [heriteLesath, focus, smnMyrlope, bleedingPuit, hemoBomb, ShiUltimate, denoument],"Soeur d'Hélène, elle a hérité des talents d'assassins de sa mère. Cependant, l'influence de son père a pas mal joué sur sa nature, la poussant à s'interreser aux médecines expérimentales", element=[ELEMENT_FIRE,ELEMENT_FIRE], bonusPoints=[STRENGTH, INTELLIGENCE], icon='<:shehisa:919863933320454165>', splashIcon='<:shehisa:1183500980680142878>',say=shehisaSays,charSettings=lenaIa , deadIcon='<:fairyOut:935335430814068786>',team=NPC_FAIRY,trait=[TRAIT_ARACHNOPHILE]),
    tmpAllie("Ruby", 2, 0x870a24, MAGE, spaceMetRuneLong, [redbutbar, redbutterflyshirt, redButterFlyBoots], GENDER_FEMALE, [invocCarbunR, space3, magicBarrier, spaceElemUse, maitriseElementaire, magicEffGiver, rubyLight], element=[ELEMENT_SPACE, ELEMENT_EARTH], icon='<:ruby:1112519724799103037>', bonusPoints=[MAGIE, PRECISION], splashIcon='<:ruby:1108041397929517147>', say=rubySays),
    tmpAllie("Sixtine", 1, blue, INOVATEUR, miltrilPlanisphere, [sixitneBarrette, sixitnePull, sixitneBoots], icon='<:sixtine:908819887059763261>', skill=[toxicon, horoscope, newMoon, revelation, sixtineUlt, blueMoon, aff2], gender=GENDER_FEMALE, element=ELEMENT_SPACE, bonusPoints=[INTELLIGENCE, ENDURANCE], description="Soeur cadette, Sixtine est plutôt du genre à vouloir rester dans son coin sans être dérangée\n\nElle ne se démarque pas particulièrement de Félicité ou Alice, mais ça ne la dérange pas. Elle passe le plus clair de son temps libre à rêvasser, à du mal à faire le premier pas vers les autres et n'a pas vraiment l'air de s'interresser à grand chose\nMais quand elle s'interresse à un truc, elle veux souvent en connaître un maximum de chose dessus.", say=sixtineSays,birthday=(12,6),splashIcon='<:sixtine:1191385884101185626>'),
    tmpAllie("Hina", 1, purple, OBSERVATEUR, plume, [hinaAcc, hinaBody, hinaShoes], GENDER_FEMALE, [plumeCel, plumePers, pousAviaire, hinaUlt, plumRem, featherCross, trainePlume], icon='<:hina:908820821185810454>', element=[ELEMENT_AIR, ELEMENT_AIR], bonusPoints=[PRECISION, STRENGTH], description="Oiseau des îles, Hina n'a pas froid aux yeux lorsqu'il s'agit d'aventure.\nA embarquer avec la première pirate venue ça ne lui a apporté que des problèmes avec les forces maritimes.\nCependant elle manque pas mal de confiance en elle et a fait beaucoup trop d'erreur qui lui coute des amitiés.",limitBreaks=[[STRENGTH,PRECISION],7],charSettings=hinaIa),
    tmpAllie("John", 2, orange, POIDS_PLUME, airsword, [bandNoir, pullCamo, kanisand], GENDER_MALE, [airlame, airStrike, splashdown, maitriseElementaire, physEffGiver, elemArrowSkill[ELEMENT_AIR], brotherHood],description="Un Loup Garou qui a réussi à tomber amoureux de la vampire responsable des pluparts des vas et viens à l'infirmerie du village de sa meute\n\nAprès de multiple tentatives de l'approcher sans grand succès, il a réussi à changer la clémence qu'éprouvait cette dernière à son égars en affection, mais a peur d'essayer de monter dans son estime", icon='<:john:908887592756449311>', bonusPoints=[STRENGTH, AGILITY], say=johnSays, element=[ELEMENT_AIR,ELEMENT_EARTH]),
    tmpAllie("Julie", 1, red, ALTRUISTE, julieWeap, [julieHat, julieDress, julieShoes], GENDER_FEMALE, [accelerant, altOH, julieUlt, timeSp, zelian, extraMedica, shareSkill],"La principale (et unique) servante d'une des vampires les plus puissante du pays.\nElle a appris la magie curative à l'aide des nombreux grimoires dans la bibliothèque du manoire, mais il lui arrive souvent de demander de l'aide à Clémence lorsque sa maîtresse (qui ai d'ailleurs la tutrice magique de cette dernière) lui demande de récupérer des organes de monstres.\nElle se sent souvent petite, en compagnie de ces puissantes vampires\n\nDire qu'elle est légèrement inspirée serait un euphémisme. Au moins elle utilise pas de dagues", element=[ELEMENT_TIME, ELEMENT_TIME], bonusPoints=[CHARISMA, INTELLIGENCE], icon="<:julie:910185448951906325>", say=julieSays),
    tmpAllie("Krys", 2, purple, TETE_BRULE, krysWeapon, [kryscharpe, krysshirt, kryschains], GENDER_OTHER, [earthStrike, defi, krysUlt, mudlame, demolish,krystalisation,ebranlement], "\"Krys Tal (rien à voir avec la chanteuse ou les opticiens) est un cristal (nooon sans blague) ayant gagné une conscience par un procédé mystérieux.\n\nN'étant pas une forme de vie organique, il se nourrit de minéraux qui traînent par-ci par-là, et de l'armure occasionnelle en combat. Il évite habituellement la nourriture organique, mais il ne dira jamais non à un peu de pop-corn, dont il semble avoir une réserve infinie.\n\nExtrêmement sensible à l'eau, mais n'hésitera pas à ingérer le contenu de la première cannette qui traîne.\n\nAvant, il était un peu con, mais ça, c'était av-Ah on m'annonce dans l'oreillette que c'est toujours le cas, my bad.\n\nPas le plus grand fan d'Akira depuis un sombre incident dans un labo.\"", element=[ELEMENT_EARTH, ELEMENT_EARTH], icon="<:krys:916118008991215726>", deadIcon='<:krysCan:916117137339322388>', bonusPoints=[ENDURANCE, STRENGTH],limitBreaks=[[ENDURANCE],10],trait=[TRAIT_LYTHOPHAGE]),
    tmpAllie("Edelweiss", 1, 0xE0FFE7, PREVOYANT, bleuSpiritWings, [battleShieldHat, battleShieldUnif, battleShieldShoes], GENDER_FEMALE, [haimaSkill, krasis, pandaima, intelRaise, holos, kerachole, pneuma], element=[ELEMENT_EARTH, ELEMENT_WATER], icon='<:edelweiss:918451422939451412>', deadIcon="<:flowernt:894550324705120266>", bonusPoints=[INTELLIGENCE, ENDURANCE],limitBreaks=[[INTELLIGENCE],10],team=NPC_DRYADE,trait=[TRAIT_ARACHNOPHOBE]),
    tmpAllie("Iliana", 1, white, ALTRUISTE, iliSwoShield, [zenithHat, zenithArmor, zenithBoots], GENDER_FEMALE, [lightAura2, ironWillSkill, clemency, lightBigHealArea, aurore2, holiomancie, holyShieltron], "Une Neko paladine qui se bat pour faire perdurer la Lumière dans sa dimension\nRelativement timide, elle ne va pas souvent vers les inconnus, mais ça ne l'empêche pas de faire de son mieux pour les tenir en vie tout de même", [ELEMENT_LIGHT, ELEMENT_LIGHT], icon='<:Iliana:926425844056985640>', splashIcon = '<:iliana:1124750738153811998>', deadIcon='<:oci:930481536564879370>', bonusPoints=[CHARISMA, ENDURANCE], say=ilianaSaysNormal,limitBreaks=[[ENDURANCE,CHARISMA],5],team=NPC_HOLY,birthday=(4,7)),
    tmpAllie('Candy', 2, 0xa124b2, INOVATEUR, concentraceurZoom, [summonerFoulard50, summonerMenteau50, summonerShoes50], GENDER_FEMALE, [smnSpaceTurets, stimulate, lenaDrone1, killerWailUltimate, invocAutFou, invocAutQueen, invocAutTour], "Jeune ingénieur de l'Escardon Espadon Nouvelle Génération, elle s'entend très bien avec sa supérieur", icon='<:candy:933518742170771466>', bonusPoints=[MAGIE, STRENGTH]),
    tmpAllie('Ly', 1, white, ATTENTIF, triStringer, [critIndStrHat45, critIndStrBody45, critIndStrShoes45], GENDER_FEMALE, [acidRain, coroRocket, quadFleau, ultraSignal, tactician, machDeFer, lanceTox],"Une mercenaire rencontrée sur les îles\nElle préfère rester loin et innonder ses ennemis avec ses attaques de zones", [ELEMENT_FIRE, ELEMENT_FIRE], icon='<:ly:943444713212641310>', bonusPoints=[STRENGTH, PRECISION], say=lySays),
    tmpAllie('Anna', 2, black, PROTECTEUR, lunarBonk, [fullMoonHat, fullMoonArmor, fullMoonBoots], GENDER_FEMALE, [royaleGardeSkill, darkShield, ghostlyCircle, heartStone, haimaSkill, inMemoria, bigBubbler], element=[ELEMENT_EARTH, ELEMENT_EARTH], icon='<:anna:943444730430246933>', bonusPoints=[ENDURANCE, INTELLIGENCE],trait=[TRAIT_ARACHNOPHOBE]),
    tmpAllie("Elina", 1, 0x560909, ALTRUISTE, elinaWeap, [urgChirHat, urgChirDress, urgChirShoes], GENDER_FEMALE, [preciChi, cure, uberCharge, terachole, renisurection, intenseCure, reconst], element=[ELEMENT_LIGHT, ELEMENT_WATER], icon='<:elina:1113685290620571700>', bonusPoints=[CHARISMA, PRECISION],charSettings=preDefCharSet[1][1][2][2]),
    tmpAllie("Bénédicte", 1, white, MAGE, dvinSeptre, [ora50Hat, ora50Dress, ora50Shoes], GENDER_FEMALE, [genesis, comboVerMiracle, beneRedempt, benitWater, divineBenediction, divineCircle, divineAbne], element=[ELEMENT_LIGHT, ELEMENT_LIGHT], bonusPoints=[MAGIE, CHARISMA], icon='<:benedict:1116416894426173520>',description="La Soeur principale de l'une des seules églises qui a survécu à la Catastrophe\nTotalement dévouée à sa cause, les gens racomptent qu'elle est capable de réaliser des miracles et qu'elle a même réussi à obtenir une forme angélique grâce à sa foi. Elle cherche principalement à aider et redonner foi aux démunies, tout en repoussant les ennemis de son Dieu",team=NPC_HOLY),
    tmpAllie("Amary",1, 0xdb6163, IDOLE, flumWand, [pinkbutbar,pinkbutterflyshirt,pinkbutterflysandals], GENDER_FEMALE, [croissance, exploPetal, petalisation, roseeHeal, floraisonFinale, theSkill, astrodyn],"Floraaaaaaaa ?",[ELEMENT_SPACE,ELEMENT_WATER],deadIcon='<:amaryDown:979440197127262218>',icon='<:amary:979441677460713502>',bonusPoints=[CHARISMA,INTELLIGENCE],charSettings=preDefCharSet[2][1][1][2],team=NPC_DRYADE),
    tmpAllie("Chûri",1,light_blue,MAGE,phenixLeath, [on45Hat, on45Dress, on45Shoes], GENDER_FEMALE, [fairySlash, maitriseElementaire, elemRuneSkill[ELEMENT_EARTH], raisingPheonix, earthCircle, magicEffGiver, cassMont], "Ayant fini par s'ennuyer en attendant que l'infime partie d'elle même étant restée bloqué parmis les vivants réussise à la rejoindre, Chûri s'est liée d'amitié avec un phenix du nom de Hinoro au point que ce dernier concenti à fusionner temporairement leurs âmes afin d'aider la fée à atteindre son but.\nDepuis, Chûri arpente le monde sous forme translucide ressemblant fortement à son ancien corps et Hinoro apparait régulièrement à ses côtés pour lui porter assistance.",[ELEMENT_EARTH,ELEMENT_EARTH],False,"<:fairyOut:935335430814068786>","<:churi:992941366537633914>",[MAGIE,PRECISION],say=churiSays,limitBreaks=[[ENDURANCE,MAGIE,AGILITY],4],splashArt="https://media.discordapp.net/attachments/640667220124499988/1084973959948288083/Sans_titre_46_20230313063859.png?width=507&height=676",splashIcon="<:churi:1088897813678653513>",team=NPC_UNDEAD),
    tmpAllie("Lily",2,0xD9A4FD,INOVATEUR, miltrilPlanisphere, [sixitneBarrette, sixitnePull, sixitneBoots], GENDER_FEMALE, [dmonBlood, burningGround, demonLand, dmonCrit, dmonDmg, exhibitionnisme, dmonAgi], "Une succube qui se sent bien plus à l'aise dans le monde des rêves que dans la réalité.\nBonne amie de Sixtine",[ELEMENT_SPACE,ELEMENT_DARKNESS],icon="<:lily:1006442350471553076>",bonusPoints=[INTELLIGENCE,ENDURANCE],say=lilySays,charSettings=preDefCharSet[2][1][2][2],team=NPC_DEMON),
    tmpAllie("Epiphyllum",1,0xEAC6DB, PREVOYANT, epiphyllum, [butterflyEarRingsBlue,blueChemVeste,blueButterFlyBoots], GENDER_FEMALE, [forestGarde,soulagement,verseau,moonLight,inkarmor,silvArmor,sacredSoil], icon='<:epiphilium:1014094726351294484>', deadIcon = "<:flowernt:894550324705120266>", element=[ELEMENT_SPACE,ELEMENT_WATER],bonusPoints=[INTELLIGENCE,PRECISION],limitBreaks=[[INTELLIGENCE,PRECISION],7],description="Figure maternelle d'Edelweiss, Epiphyllum est une dryade calme et posée qui préfère resplandir par ses connaissances plutôt que ses aptitudes au combat",charSettings=preDefCharSet[1][1][2][2],team=NPC_DRYADE),
    tmpAllie("Astra",1,white, MASCOTTE, lunarBonk, [ninjaArmored50Hat,ninjaArmored50Dress,ninjaArmored50Shoes], GENDER_FEMALE, [blackHole, tacShield, findSkill("Divination"), moonLight, findSkill("Thèses fluidiques"), phalax, findSkill("Grâce du Poisson")], description="Une jeune fée aux origines sombres qui a rejoins le clan féérique après la Réunification Dimentionnelle.\nBien que le fait qu'elle ne veuille pas divulger son passé, elle a prouvé de nombreuses fois qu'elle était sûrment plus fidèle au clan qu'une bonne partie de ses membres. Toujours de bonne humeur, elle a le don pour rendre le sourir à n'importe qui.\n\nDe nos jours, bien que les plus septiques du clan soient toujours réticent à la laisser participer à des missions sensibles du clan, beaucoup de fées refuseraient d'y participer si Astra n'est pas de la partie, ses compétences en soins d'urgence et pour faire diversion rendent sa présence très appréciée, et beaucoup se demande même comment elle fait pour être aussi discrète malgré son accoutrement. Cependant les plus attentifs du clan commence à faire la comparaison avec une autre fée du clan, surtout que Astra a révélé avoir des pouvoirs sur le Temps",element=[ELEMENT_TIME,ELEMENT_SPACE],bonusPoints=[ENDURANCE,INTELLIGENCE],limitBreaks=[[ENDURANCE,AGILITY,INTELLIGENCE,CHARISMA],3], icon="<:astra:1051825407466426430>", deadIcon='<:fairyOut:935335430814068786>', splashIcon='<:astra:1051977465884594306>', splashArt="https://media.discordapp.net/attachments/264128214593568768/1051916946679025776/Sans_titre_12_20221212171102.png?width=460&height=675",team=NPC_FAIRY),
    tmpAllie("Céleste",2,0x1E0098, ENCHANTEUR, magicSwordnShield, [magicArmorHelmet,magicArmorBody,magicArmorBoots], GENDER_FEMALE, [ferocite, dualSupp, dualEnergyDrain, celestialChoc, spaceComet, comboConfiteor, selfMemoria],description="Une jeune avanturière dénie par Silicia pour être sa championne. N'ayant pris les armes que depuis peu, elle n'est encore pas vraiment à l'aise avec le combat",element=[ELEMENT_SPACE,ELEMENT_EARTH],deadIcon='<:oci:930481536564879370>',icon='<:celeste:1129042444479119401>',bonusPoints=[MAGIE,ENDURANCE],limitBreaks=[[ENDURANCE,MAGIE],5]),
    tmpAllie("Zénéca",1,white,SORCELER,toxicBrush,[critIndHat50, critIndBody50, critIndShoes50],GENDER_FEMALE,[propagDelPas,intox,exploMark,epidemic,gangrene,focal,infectFiole],description="Une jeune fée qui considère qu'il n'y a pas de soins à faire si il n'y a plus d'ennemi pour subir des dégâts",element=[ELEMENT_WATER,ELEMENT_TIME],deadIcon='<:fairyOut:935335430814068786>',icon='<:zeneca:1177606488496283689>',splashIcon='<:zeneca:1177605494219739176>',bonusPoints=[MAGIE,INTELLIGENCE],team=NPC_FAIRY)
]

churInoSkills = [galvanisation, maitriseElementaire, elemRuneSkill[ELEMENT_FIRE], raisingPheonix, fireCircle, magicEffGiver, cycloneEcarlate]

# Tabl var allies =============================================================================
tablVarAllies = [
    tmpAllie("Luna", 1, black, POIDS_PLUME, infDarkSword, [lunaPandan, lunaDress, lunaBoots], GENDER_FEMALE, [meditate, brotherHood, soupledown, highkick, renforPhys, bundleRixeEva],"Là où se trouve la Lumière se trouvent les Ténèbres", [ELEMENT_DARKNESS, ELEMENT_AIR], variant=True, icon='<:luna:909047362868105227>', bonusPoints=[STRENGTH, ENDURANCE], say=lunaSays),
    tmpAllie("Altikia", 2, 0xDFFF92, VIGILANT, aWeap, altyStuffTabl, GENDER_FEMALE, [ironWillSkill, altyCover, altyPenta, healingSacrifice, convictionVigilante, altyStrike, altyQCombo],"Une personnalité de Gwen qui préfère se concentrer sur ses alliés", [ELEMENT_WATER, ELEMENT_LIGHT], variant=True, bonusPoints=[ENDURANCE, CHARISMA], icon='<:alty:1112517632671875152>', say=altySays, splashIcon='<:altikia:1126732994732884049>'),
    tmpAllie("Klironovia", 2, 0xF49206, BERSERK, kWeap, [butterflyEarRingsDark, darkChemVeste, darkButterFlyBoots], GENDER_FEMALE, [intuitionFoug, klikliQCombo, kStrike, kliBloody, klikliStrike, pentastrike, bloodPact],"Une personnalité de Gwen bien plus violente que les deux autres", [ELEMENT_AIR, ELEMENT_TIME], variant=True, bonusPoints=[STRENGTH, AGILITY], icon='<:klikli:906303031837073429>', say=klikliSays, splashIcon ='<:klironovia:1126632922510786690>'),
    tmpAllie("Shihu", 1, 0x00002D, MAGE, darkMetRuneMid, [shihuHat, shihuDress, shihuShoe], GENDER_FEMALE, [dark2, dark3, darkFlamme, darkBoomCast, quickCast, darkIce, dualCast],"\"Eye veut zuste un pi d'attenchions...\" - Shushi", [ELEMENT_DARKNESS, ELEMENT_FIRE], variant=True, icon='<:shihu:909047672541945927>', bonusPoints=[MAGIE, STRENGTH], say=shihuSays,trait=[TRAIT_ARACHNOPHOBE]),
    tmpAllie("Clémence Exaltée", 2, 0x8F001C, ENCHANTEUR, clemExWeapon, [miniStuff, miniStuff, miniStuff], GENDER_FEMALE, [clemExSkill2, clemExSkill3, clemExSkill4, clemExSkill5, clemExSkill6, clemExBloodDemon], "WIP, revenez plus tard", [ELEMENT_DARKNESS, ELEMENT_LIGHT], icon='<:clemence:908902579554111549>', bonusPoints=[MAGIE, STRENGTH], say=clemExSay, deadIcon='<:AliceOut:908756108045332570>',variant=True,splashIcon="<:clemenceEx:1088484359872450600>",splashArt="https://media.discordapp.net/attachments/640667220124499988/1088478369596838048/Sans_titre_60_20230323160331.png?width=380&height=676",team=NPC_DEMON),
    tmpAllie('Iliana prê.', 1, white, VIGILANT, iliWeap, [miniStuffHead, miniStuffDress, miniStuffFlats], GENDER_FEMALE, [iliPreSkill5, iliPreSkill4, iliPreSkill6, iliPreSkill1, iliPreSkill2, iliPreSkill3, iliPreSkill7], element=[ELEMENT_LIGHT, ELEMENT_LIGHT], deadIcon='<:oci:930481536564879370>', icon='<:Iliana:926425844056985640>', bonusPoints=[CHARISMA, ENDURANCE], description="Face à une menace dimensionnelle sans précédents, Iliana a décider de réveiller ses pouvoirs de Prêtresse de la Lumière pour faire équipe avec celle des Ténèbres",say=ilianaPreSays,variant=True,splashIcon='<:iliPre:1053017768443785236>', team=NPC_HOLY),
    tmpAllie('Belle', 2, 0x1f0004, ENCHANTEUR, magicSwordnShield, [magicArmorHelmet, magicArmorBody, magicArmorBoots], GENDER_FEMALE, [ferocite, spectralCircle, darkAmb, spectralFurie, magicRuneStrike, strengthOfDesepearance, undead], element=[ELEMENT_DARKNESS, ELEMENT_NEUTRAL], variant=True, icon='<:belle:943444751288528957>', bonusPoints=[ENDURANCE, MAGIE],team=NPC_UNDEAD,trait=[TRAIT_ARACHNOPHOBE]),
    tmpAllie("Luna prê.", 1, black, POIDS_PLUME, lunaWeap, [LunaPreStuffHead, LunaPreStuffDress, LunaPreStuffFlats], GENDER_FEMALE, [lunaSpeCast,lunaDarkChoc,lunaPreSkill5_3,lunaPreSkill3,lunaPreSkill2,lunaSkill6,lunaPreUltimawashi], element=[ELEMENT_DARKNESS, ELEMENT_DARKNESS], icon='<:luna:909047362868105227>', bonusPoints=[STRENGTH, AGILITY], say=lunaPreSays,variant=True, description = "Face à une menace temporelle sans précédents, Luna a décidé de réveiller ses pouvoirs de Prêtresse des Ténèbres pour faire équipe avec celle de la Lumière"),
    tmpAllie("Chûri-Hinoro", 1,orange, ENCHANTEUR, phenixLeath, [on45Hat, on45Dress, on45Shoes], GENDER_FEMALE, churInoSkills, description="En utilisant la compétence \"Envolée du Phenix\", Chûri devient Chûri-Hinoro, modifiant son élément et ses compétences", element=[ELEMENT_FIRE,ELEMENT_EARTH],deadIcon="<:fairyOut:935335430814068786>",icon='<:churHi:994045813175111811>',bonusPoints=[MAGIE,PRECISION],say=churiSays,variant=True,splashIcon="<:churiHinoro:1088897850219450448>",splashArt="https://media.discordapp.net/attachments/640667220124499988/1084973960191549470/Sans_titre_49_20230313235816.png?width=490&height=676",team=NPC_FAIRY),
    tmpAllie("Lia Ex",2,0xBBFFCB,POIDS_PLUME,liaExWeap,[greenbutbar,greenbutterflyshirt,greenbutterflysandals],GENDER_FEMALE,[liaExSkill1,liaExSkill2,liaExSkill3,liaExSkill4,liaExUlt_1,liaExSkill6,liaExSkill7],description="Suite à l'émergeance d'une nouvelle menage, afin de protéger ses frères et soeurs et comme épreuve de sa mère, Lia a du mettre son masque de démon renard et se jeter corps et âme contre leur ennemi d'ombre",element=[ELEMENT_AIR,ELEMENT_AIR],deadIcon="<:kitsuSisterDead:908756093101015100>",icon="<:liaEx:1012669139711696928>",bonusPoints=[MAGIE,AGILITY],limitBreaks=[[MAGIE,AGILITY,ENDURANCE],5],elemAffinity=True,splashIcon='<:liaEx:1079115890437656598>'),
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

# Balancing
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

shehisaReactAttackMyrlope = [
    "Hé !",
    "Myrlopé !",
    "Pas si vite.",
    "J'te permet pas !",
    "Fiche lui la paix !",
    "Arrête ça !"
]
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
    tempAltBuilds(35,stuffs=[batRuban, aliceDress, aliceShoes], skills=[aliceDance, courage, charmingPandant, holyVoice, onstage, corGra, inconsCollect],splashIcon='<:alice:1183197636153577482>'),
    tempAltBuilds(20,POIDS_PLUME,aliceFan,[dans50Hat,dans50Dress,dans50Shoes],[finalTech,swordDance,aliceFanDanse,fanRevol,danseStarFall,tangoEnd,fanVirBundle],[ELEMENT_SPACE,ELEMENT_SPACE],[AGILITY,CHARISMA]),
    tempAltBuilds(20,stuffs=[bardIntHat50, bardIntDress50, bardIntShoes50],skills=[mageBalad, martialPean, vanderManuet, apexArrow, heroicFantasy, blastArrow, courage],splashIcon='<:alice:1183197636153577482>',bonusPoints=[STRENGTH,CHARISMA],aspiration=OBSERVATEUR)
    ]
findAllie("Hélène").changeDict = [
    tempAltBuilds(20,SORCELER,butterflyP,[critIndHat45,critIndBody45,critIndShoes45],[infectFiole,epidemic,intox,funDraw,propaUltLaunch,infDraw,quadFleau],[ELEMENT_DARKNESS,ELEMENT_LIGHT],[MAGIE,INTELLIGENCE]),
    tempAltBuilds(35,weap=whiteSpiritWings,skills=[propagPas,lightHeal2,lightShot,lapSkill,invocFee,sumLightButterfly,shareMark],elements=[ELEMENT_LIGHT,ELEMENT_WATER])
    ]
findAllie("Amary").changeDict = [tempAltBuilds(50,ALTRUISTE,stuffs=findAllie("Hélène").stuff,skills=[mend,lifeSeed,lillyTransform,cure,roseeHeal,renisurection,asile],elements=[ELEMENT_LIGHT,ELEMENT_WATER],bonusPoints=[CHARISMA,PRECISION])]
findAllie("Shehisa").changeDict = [
    tempAltBuilds(25,stuffs=[ninEnt50Hat,ninEnt50Mid,ninEnt50Shoes],skills=[dissimulation,physTraqnard,UmbralTravel,bundleFetu,carnage,assasinate,smnMyrlope],elements=[ELEMENT_DARKNESS,ELEMENT_DARKNESS],bonusPoints=[STRENGTH,AGILITY]),
    tempAltBuilds(25,aspiration=POIDS_PLUME,stuffs=[ninEnt50Hat,ninEnt50Mid,ninEnt50Shoes],skills=[dissimulation,dreamInADream,smnMyrlope,trickAttack,assasinate,redrum,florChaot],elements=[ELEMENT_DARKNESS,ELEMENT_LIGHT],bonusPoints=[STRENGTH,AGILITY]),
    tempAltBuilds(25,aspiration=TETE_BRULE,stuffs=[ninEnt50Hat,ninEnt50Mid,ninEnt50Shoes],skills=[trickAttack,seitonTenchu,deathPercing,smnMyrlope,echecEtMat,ripping,weakPoint],elements=[ELEMENT_DARKNESS,ELEMENT_LIGHT],bonusPoints=[STRENGTH,AGILITY])
]
findAllie("Julie").changeDict = [
    tempAltBuilds(20,SORCELER,magicWood,stuffs=findAllie("Lohica").stuff,skills=[dephaIncant,ice2,lizSKillSus,clock,hourglass,magAchSkill,fairyTraqnard],elements=[ELEMENT_TIME,ELEMENT_DARKNESS],bonusPoints=[MAGIE,INTELLIGENCE]),
    tempAltBuilds(35,skills=[rajeunissement,healingTimebomb,inconsCollect,julieUlt,extraMedica,extraEting,vampirisme2]),
    tempAltBuilds(20,ENCHANTEUR,eclatanaDoto,stuffs=[magicArmorHelmet,magicArmorBody,magicArmorBoots],skills=[periodStrike,descynNeg,elemRuneSkill[ELEMENT_TIME],time3,canceling,spectralFurie])
    ]
findAllie("Gwendoline").changeDict = [
    tempAltBuilds(30,POIDS_PLUME,mainLibre,stuffs=[butterflyEarRingsDark, darkChemVeste, darkButterFlyBoots],skills=[elipseTerrestre,piedVolt,retourneImpactant,demolish,earthStrike,hearthFrac,ebranlement]),
    tempAltBuilds(30,POIDS_PLUME,mainLibre,stuffs=[butterflyEarRingsDark, darkChemVeste, darkButterFlyBoots],skills=[defi,earthStrike,justiceEnigma,physEffGiver,erodStrike,demolish,gwenyStrike])
]
findAllie("Klironovia").changeDict = [
    tempAltBuilds(50,weap=mainLibre,skills=[fracas,piedVolt,revolutionFracas,plongeFracas,pentastrike,uppercut,balayette])
]
findAllie("Lily").changeDict = [
    tempAltBuilds(30,PREVOYANT,epiphyllum,stuffs=findAllie("Epiphyllum").stuff,skills=[demonArmor,demonArmor2,dmonReconstitution,dmonReconstitution2,demonConst,inkarmor,firstArmor],bonusPoints=[INTELLIGENCE,PRECISION]),
    tempAltBuilds(30,INOVATEUR,luth,skills=[unHolly,exhibitionnisme,corruptusArea,infirm,toxicon,findSkill("Blocage Démoniaque"),findSkill("DistribuCool")])
]
findAllie("Sixtine").changeDict = [
    tempAltBuilds(30,stuffs=[bardMagHat50, bardMagDress50, bardMagShoes50],skills=[stigmate,dissonance,vibrSon,enhardissement,sernade,manafication,descart],bonusPoints=[MAGIE,CHARISMA],aspiration=MAGE,icon="<:dreamSixtine:1100793996483235851>"),
    tempAltBuilds(20,aspiration=ENCHANTEUR,weap=dSixtineWeap,stuffs=[on45Hat,on45Dress,on45Shoes],skills=[ferocite,spaceCrush,spacePulse,hexadecaComb,findSkill("Percée du Capricorne"),findSkill("Frappe Runique")],elements=[ELEMENT_SPACE,ELEMENT_DARKNESS],bonusPoints=[MAGIE,ENDURANCE],icon='<:dreamSixtine:1100793996483235851>')
    ]
findAllie("Icealia").changeDict = [
    tempAltBuilds(40,PROTECTEUR,icealiaShield,stuffs=[royalGardHelmet,royalGardPlate,royalGardBoots],skills=[royaleGardeSkill,snowFall,findSkill("Onde"),findSkill("Aura Armurière"),findSkill("Orbe défensif"),royalShield,findSkill("Inconscient collectif")],bonusPoints=[ENDURANCE,INTELLIGENCE],elements=[ELEMENT_LIGHT,ELEMENT_WATER]),
    tempAltBuilds(25,MASCOTTE,constShield,stuffs=[findStuff("Casque en obsidienne"),findStuff("Armure en obsidienne"),findStuff("Bottes en obsidienne")],skills=[royaleGardeSkill,bastion,orage,magma,findSkill("Teliki Anakatéfthynsi"),findSkill("Coeur de Lumière"),findSkill("Inconscient collectif")],bonusPoints=[ENDURANCE,INTELLIGENCE],elements=[ELEMENT_LIGHT,ELEMENT_WATER])
    ]
findAllie("Bénédicte").changeDict = [
    tempAltBuilds(20,IDOLE,dvinWand,skills=[findSkill("Terre Sacrée Étendue"),findSkill("Guide Divin"),findSkill("Equilibre de la Balance"),findSkill("Astrodynamie"),findSkill("Lotus Pourpre"),findSkill("Manafication"),findSkill("Eruption Solaire")],bonusPoints=[CHARISMA,MAGIE],elements=[ELEMENT_SPACE,ELEMENT_DARKNESS]),
    tempAltBuilds(20,ALTRUISTE,dvinWand,stuffs=findAllie("Elina").stuff,skills=[findSkill("Constitution Divine"),findSkill("Bénédiction Avancée"),findSkill("Purification"),findSkill("Extra Medica"),findSkill("Pulsation Vitale"),findSkill("Offrande de misère")],elements=[ELEMENT_LIGHT,ELEMENT_FIRE]),
    tempAltBuilds(20,MASCOTTE,sacredSword,stuffs=[meleeOra50Hat,meleeOra50Dress,meleeOra50Shoes],skills=[findSkill("Volontée de Fer"),findSkill("Frappe Séraphique"),findSkill("Miracle"),findSkill("Invincible"),findSkill('Rivière Céleste'),findSkill('ssj'),findSkill('Bénidiction de la Vièrge')],elements=[ELEMENT_SPACE,ELEMENT_FIRE],bonusPoints=[ENDURANCE,CHARISMA])
]
findAllie("Lena").changeDict = [
    tempAltBuilds(25,OBSERVATEUR,splatcharger,skills=[findSkill("Flèche Gelante"),findSkill("Flèche Givrante"),findSkill("Flèche de glace"),findSkill("Aqua ferrum"),findSkill("Tir Parfait"),rapidFire,findSkill("Constance Critique")],splashIcon='<:lena:1177723779548446842>'),
    tempAltBuilds(10,ATTENTIF,triStringer,stuffs=[findStuff("Boucles d'oreilles de la chauve-souris écarlate"),findStuff("Veste et robe de la chauve-souris écarlate"),findStuff("Bottes de la chauve-souris écarlate")],skills=[inkStrike,findSkill("Mâchoire de Fer"),findSkill("Morsure de la Tempette"),findSkill("Morsure Caudique"),findSkill("Multi-Missiles"),findSkill("Tir Explosif"),findSkill("Flambage")],splashIcon='<:lena:1177723779548446842>'),
    tempAltBuilds(35,OBSERVATEUR,splatcharger,skills=[comboHeatedCleanShot,leadShot,dismantle,exploShot,dechargeGausseSolo,findSkill("Tir Parfait"),sagArrow])
]
findAllie("Ly").changeDict = [
    tempAltBuilds(20,OBSERVATEUR,stuffs=findAllie("Lena").stuff,skills=[findSkill("Tir Feu"),findSkill("Pyro-Hypercharge"),findSkill("Flèche d'Immolation"),findSkill("Barrage"),findSkill("Flèche Explosive"),findSkill("Flèche emflammée"),tactician],elements=[ELEMENT_FIRE,ELEMENT_SPACE]),
    tempAltBuilds(30,skills=[lanceTox,lanceTox2,lanceTox3,machDeFer,morsTempSkill,morsCaudiqueSkill,ultraSignal])
]
findAllie("Astra").changeDict = [
    tempAltBuilds(50,VIGILANT,constShield,stuffs=findAllie("Iliana").stuff,skills=[ironWillSkill,astraRegenPhase,astraIncurStrike,astraRegenEarth,findSkill("Medicamentum"),extraEting,propagPas],bonusPoints=[CHARISMA,ENDURANCE])
]
findAllie("Ruby").changeDict = [
    tempAltBuilds(10,weap=fireMetRuneLong,skills=[findSkill("Pyrotechnie"),pyroSparkle,findSkill("Flammes infernales"),findSkill("Flamme"),pyroBlast,findSkill("Brasier"),magicBarrier],elements=[ELEMENT_FIRE,ELEMENT_SPACE]),
    tempAltBuilds(10,weap=waterMetRuneLong,skills=[findSkill("Torrant"),bouncingWater,findSkill("Geyser"),findSkill("Courant"),waterBlast,findSkill("Pluie Glacée"),magicBarrier],elements=[ELEMENT_WATER,ELEMENT_SPACE]),
    tempAltBuilds(10,aspiration=ENCHANTEUR,stuffs=findAllie("Belle").stuff,weap=airMetRuneMel,skills=[findSkill("Tornade"),windBlast,findSkill("Sillage"),findSkill("Tempête"),windCutter,findSkill("Tempête Jupiterrienne"),magicBarrier],elements=[ELEMENT_AIR,ELEMENT_SPACE],bonusPoints=[ENDURANCE,MAGIE]),
    tempAltBuilds(10,aspiration=ENCHANTEUR,stuffs=findAllie("Belle").stuff,weap=earthMetRuneMel,skills=[findSkill("Montagne"),rockStomp,findSkill("Casse-Montagne"),findSkill("Rocher"),rockBlast,findSkill("Déchirure Tectonique"),magicBarrier],elements=[ELEMENT_AIR,ELEMENT_SPACE],bonusPoints=[ENDURANCE,MAGIE])
]
findAllie("Clémence").changeDict = [
    tempAltBuilds(25,aspiration=SORCELER,stuffs=[critIndHat45, critIndBody45, critIndShoes45],skills=[findSkill("Méga Pénombre"),findSkill("Giga Pénombre"),findSkill("Giga Obscurité"),findSkill("Méga Obscurité"),findSkill("Umbra ferrum"),findSkill("Âbime"),findSkill("Giga Foudre")]),
    tempAltBuilds(20,aspiration=MAGE,skills=[sanguisGladio,sanguisGladio2,bloodDemonBundle,findSkill("Umbra Mortis"),findSkill("Ultima Sanguis Pluviae"),magicRune,findSkill("Anticipation")],weap=findWeapon("Baguette en argent"))
]

findAllie("Powehi").changeDict = [tempAltBuilds(35,aspiration=ENCHANTEUR,stuffs=findAllie("Belle").stuff,skills=[findSkill("Trou Noir"),vibrSon,findSkill("Constellation"),findSkill("Trou noir Avancé"),gravPulse,findSkill("Combo Confiteor"),findSkill("Conviction de l'Enchanteur")])]
findAllie("Luna").changeDict = [tempAltBuilds(50,skills=[findSkill("Foulée Légère"),findSkill("Danse du Phénix"),findSkill("Pied Voltige"),expultion,findSkill("Triple Choc"),findSkill("Frappe Convertissante"),findSkill("Envolée féérique")])]
findAllie("Lohica").changeDict = [tempAltBuilds(50, skills=[findSkill("Focalisation"),findSkill("Intraveineuse"),findSkill("Propagation"),fairyRay,findSkill("Propagation Avancée"),exploMark,findSkill("Héritage - Estialba")],weap=butterflyP)]
findAllie("Chûri").changeDict = [tempAltBuilds(50, aspiration=ENCHANTEUR, skills=[galvanisation,fireCircle,inMemoria,darkSweetHeat,phenixRevive,summonHinoro,pyro],elements=[ELEMENT_FIRE,ELEMENT_FIRE])]
findAllie("Iliana").changeDict = [
    tempAltBuilds(50,skills=[ironWillSkill,holyShieltron,convictionVigilante,altyQCombo,inspiration,lightAura,iliLightCombo])
]
lenaShuRedirect = effect("Protection Maternelle","materProtect",redirection=100,unclearable=True,turnInit=-1,emoji='<:analyse:1003645750225412257>')