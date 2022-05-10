from classes import *
from constantes import *
from advObjects.advWeapons import *
from advObjects.advSkills import *
from advObjects.advStuffs import *
from advObjects.advInvocs import *
from advObjects.advEffects import *


lohicaFocal = copy.deepcopy(focal)
lohicaFocal.say = "Vous commencez sérieusement à me tapez sur les nerfs..."

lenaChangeDict = createTmpChangeDict(30, 0, [bigMonoLaser2], [tripleMissiles], 35)

amirShotLaunch = copy.deepcopy(bigLaser)
amirShotLaunch.name, amirShotLaunch.emoji, amirShotLaunch.description, amirShotLaunch.power = "Tir de l'Amiral v11.5.8", '<a:amirShot:933184039584690227>', "Candy n'a pas peur de demander à l'Amiral de l'Escadron Espadon Nouvelle Génération de tester ses nouvelles armes. Et Lena n'a jamais vraiment eu de raison de refuser", int(amirShotLaunch.power*1.11)
amirShotRepEff = effect("Cast - Tir de l'Amiral", "LenaCloneEffRep", replique=amirShotLaunch, turnInit=2,emoji=sameSpeciesEmoji('<a:amirShotB:933183135355650070>', '<a:amirShotR:933183150950088724>'),silent=True)
amirShotCast = copy.deepcopy(amirShotLaunch)
amirShotCast.effectOnSelf, amirShotCast.power = amirShotRepEff, 0

aliceLotus = createTmpChangeDict(35, 0, [onstage, courage, roses], [crimsomLotusCast, hollyGround2, fascination], 50)

# Alliés temporaires =============================================================================
tablAllAllies = [
    tmpAllie("Lena", 1, light_blue, OBSERVATEUR, splatcharger, [amethystEarRings, lightBlueJacket, lightBlueFlats], GENDER_FEMALE, [waterlame, amirShotCast, trans, matriceEmpli, doubleShot, constance2, preciseShot],"Une inkling qui en a vu des vertes et des pas murs.\nPréfère rester loin de la mêlée et abattre ses ennemis à bonne distance", [ELEMENT_WATER, ELEMENT_TIME], icon='<:lena:909047343876288552>', bonusPoints=[STRENGTH, PRECISION], say=lenaSays,birthday=(19,1)),
    tmpAllie("Gwendoline", 2, yellow, PROTECTEUR, roller, [newMoonHat, newMoonArmor, newMoonBoots], GENDER_FEMALE, [airStrike, royaleGardeSkill, shieldAura, darkShield, bolide, impact, heartStone],"Bien qu'elle essaye de l'éviter, cette jeune femme se retrouve toujours à devoir en venir aux mains pour se débarraser des gros lourds de la première ligne ennemie.\nIl est vrai aussi qu'elle n'est pas toute seule dans sa tête", [ELEMENT_AIR, ELEMENT_DARKNESS], bonusPoints=[STRENGTH, ENDURANCE], icon='<:gweny:906303014665617478>', say=gwenySays, birthday=(9,9)),
    tmpAllie("Clémence", 2, red, MAGE, rapiere, [critIndHat45, critIndBody45, critIndShoes45], GENDER_FEMALE, [cwUlt, sanguisGladio2, cwFocus, magiaHeal, sanguisGladio, gigaFoudre], "Clémence est née orpheline, ses parents ayant été tués par des chasseresses d'Arthémis peut après sa naissance.\nElle fût donc élevée par des chauve-souris dans une grotte pendant une bonne partie de son enfance\nCependant, elle rencontra dans un lieu nommé la \"Ville Onirique\", une ville magique accessible via les rêves permettant aux vampires vivants comme mort de s'y retrouver, une jeune vampire majeure du nom de Ruby.\nCette dernière lui apprit les bases de la magie au fils des années, ainsi que celles des sociétés humaines que les chauve-souris pouvaient évidamment pas lui apprendre.\n\nMalgré tout, elle manquait d'amis vampire \"réels\", Ruby habitant à des centaines de kilomètres dans la réalité. Elle alla donc, par une belle soirée d'Haloween, mordre une jeune femme envers laquelle Clémence avait un bon sentiment.\nOn peut dire que sur tous les choix qu'elle a fait, ça allait être celui qui allait être le plus lourd en conséquence, dans de bons comme mauvais thermes.\n\nJe vous en passe et des meilleurs, sinon je vais casser la limite de caractères, mais en grandissant, Clémence a continué son apprentissage de la magie et a décidé de parcourir le monde pour étudier les Anciennes Runes ainsi que pour purifier les artéfacts maudits qui tourmentent les monstres pour éviter qu'ils se fassent chasser par les humains, tel ses parents biologiques", [ELEMENT_DARKNESS, ELEMENT_DARKNESS], icon='<:clemence:908902579554111549>', bonusPoints=[MAGIE, INTELLIGENCE], say=clemSays, deadIcon='<:AliceOut:908756108045332570>',birthday=(31,10)),
    tmpAllie("Alice", 1, aliceColor, IDOLE, astroGlobe, [butterflyPendantPink, pinkChemVeste, pompomShoes], GENDER_FEMALE, [aliceDance, courage, partner, trans, onstage, corGraCast, finalFloral], "Alice est la petite dernière des trois sœurs Kohishu, et la seule à être une vampire\n\nDès son plus jeune âge, elle a fortement démontré sa volontée à vouloir être le centre de l'attention, bien que ça ai frustrée sa sœur ainée. En grandissant, cette envie de reconnaissance ne s'est pas vraiment tarie, et a réussi grâce à son charme naturel à devenir rapidement une fille populaire\n\nElle décida de suivre la voie de sa mère et de devenir une chanteuse renommé, c'est ainsi qu'elle participa au concours de jeune talent de son école et réussi à se faire remarquer par une maison de disque qui recherchait de jeunes chanteurs\n\nLorsqu'elle n'est pas retenue par ses obligations, elle aime bien accompagner Félicité et Clémence dans leurs aventures, mais refuse de participer activement aux combats. À la place elle les encourages avec ses chansons légèrement magiques", [ELEMENT_LIGHT, ELEMENT_AIR], icon='<:alice:908902054959939664>', bonusPoints=[CHARISMA, INTELLIGENCE], say=aliceSays, deadIcon='<:AliceOut:908756108045332570>', changeDict=aliceLotus,birthday=(14,6)),
    tmpAllie("Shushi", 1, blue, ENCHANTEUR, airspell, [tankmage3, tankmage2, tankmage1], GENDER_FEMALE, [storm2, ferocite, invocCarbT, storm, supprZone, magicRuneStrike, magicEffGiver],"Jeune inkling pas très douée pour le combat, à la place elle essaye de gagner du temps pour permettre à ses alliés d'éliminer l'équipe adverse", [ELEMENT_AIR, ELEMENT_SPACE], icon='<:shushi:909047653524963328>', bonusPoints=[MAGIE, ENDURANCE], say=shushiSays,birthday=(26,9)),
    tmpAllie("Lohica", 1, purple, SORCELER, secretum, [darFlumOr, corruptPurpleVeste, corruptPurpleBoots], GENDER_FEMALE, [lohicaFocal, poisonus, poisonusPuit, propag, lohicaUltCast, fairyFligth],"Une fée à l'histoire bien mouvementée. Spécialisée dans les poisons", [ELEMENT_DARKNESS, ELEMENT_WATER], bonusPoints=[MAGIE, INTELLIGENCE], icon='<:lohica:919863918166417448>', deadIcon='<:flowernt:894550324705120266>'),
    tmpAllie("Hélène", 2, white, ALTRUISTE, whiteSpiritWings, [butterflyEarRingsWhite, whiteChemVeste, whiteButterFlyBoots], GENDER_FEMALE, [cure, lapSkill, renisurection, benediction, lifePulseCast, cure2Bundle, tintabule],"Une fée qui estime qu'essayer de sauver la vie de ses alliés est plus efficace que si elle esseyait de terminer le combat elle-même", [ELEMENT_LIGHT, ELEMENT_FIRE], bonusPoints=[CHARISMA, INTELLIGENCE], icon='<:helene:906303162854543390>'),
    tmpAllie("Félicité", 1, red, TETE_BRULE, dtsword, [celestBronzeHat, celestBronzeArmor, celestBronzeBoots], GENDER_FEMALE, [bloodyStrike, defi, erodStrike, strengthOfWillCast, highkick, fragmentation, absorbingStrike2], "Soeur ainée de Sixtine et Alice, Félicité est née dans un monde désolé et post apocaliptique\n\n<:lena:909047343876288552> : Mais parle pour toi !\n\nN'ayant plus aucun humain dans ce monde pas si désolé et pas si post apocaliptique, elle hérita de l'âme de Détermination de ce monde (ainsi que quelques bénédictions de dieux grecs mais c'est une autre histoire\n\nEn grandissant, ces dites bénédictions lui ont permis de développer rapidement son esprit et ses capacités, mais aussi d'attirer sur elle tous les monstres mythologiques du coin. Fort heureusement elle pu compter sur ses parents ainsi que sur sa sœur adoptive ainnée Clémence pour la protéger jusqu'au jour où elle en a eu marre de devoir laisser les autres la défendre.\nElle alla donc trouver les seuls autres personnes avec des âmes de Détermination à sa connaissance : Frisk et Chara, qui lui apprirent les bases. Sa volontée ainsi que ses bénédictions lui permirent de rapidement faire des progrès dans l'escrime, quand pour la maîtrise de la magie, c'est grâce à Hécate qu'elle le doit\n\nEn grandissant, elle a choisi une voie plus ou moins similaire à celle de Clémence, c'est à dire de chercher à purifier des artéfacts maudits agitants les monstres alentours ainsi que l'étude d'ancienne magie. Cependant, là où Féli le fait pour protéger les populations d'hommes, Clémence le fait pour protéger les monstres de ces derniers. Mais ça ne les empêche pas de faire équipe de temps en temps. Après tout le but reste le même", bonusPoints=[ENDURANCE, STRENGTH], icon='<:felicite:909048027644317706>', element=ELEMENT_UNIVERSALIS_PREMO,birthday=(10,6)),
    tmpAllie("Akira", 2, black, TETE_BRULE, fauc, [nemeBracelet, nemeManteau, nemeBottes], GENDER_MALE, [deathShadow, defi, absorbingStrike2, absorbingStrike, theEndCast, toMelee, comboFaucheCroix],"Fils aîné des Fluwaraito, Akira est un jeune garçon au sang chaud qui ne renonce jamais à un affrontements. En revanche évitez de le mettre en colère.", ELEMENT_DARKNESS, bonusPoints=[ENDURANCE, STRENGTH], icon='<:akira:909048455828238347>'),
    tmpAllie("Icealia", 2, light_blue, PREVOYANT, blueButterfly, [icealiaHat, icealiaManteau, icealiaBoots], GENDER_FEMALE, [soulagement, inkarmor, kralamSkill, convert, onde, shell, elemShield],"Une érudite qui préfère protéger ses compagnons", element=[ELEMENT_LIGHT, ELEMENT_WATER], bonusPoints=[INTELLIGENCE, ENDURANCE], icon='<:icealia:909065559516250112>'),
    tmpAllie("Powehi", 2, black, PROTECTEUR, grav, [starBar, bhPull, bhBoots], GENDER_FEMALE, [blackHole, trans, blindage, cosmicPower, inkRes2, darkShield, ironHealth], "Une manifestation cosmique d'un trou noir. Si vous vous sentez attiré par elle, c'est probablement à raison\nNe lui demandez pas de vous marchez dessus par contre, si vous voulez un conseil. Elle a beau paraître avoir un petit gabarie, ce n'est pas pour rien qu'elle évite de marcher sur le sol", element=[ELEMENT_SPACE, ELEMENT_DARKNESS], bonusPoints=[ENDURANCE, INTELLIGENCE], icon='<:powehi:909048473666596905>', deadIcon='<:powehiDisiped:907326521641955399>', say=powehiSays),
    tmpAllie("Shehisa", 1, purple, TETE_BRULE, shehisa, [redBatEarRingsred , batRedChemVeste, redBatBoots], GENDER_FEMALE, [heriteLesath, focus, dissimulation, bleedingPuit, bleedingTrap, ShiUltimate, bleedingConvert],"Soeur d'Hélène, elle a elle aussi choisi de s'enroler dans la milice, mais étant trop timide pour faire face à ses adversaires, Shehisa a opté pour une stratégie un peu moins nombre qui consiste à piéger les zones et à regarder ses ennemis se vider de leur sang de loin", element=[ELEMENT_DARKNESS,ELEMENT_WATER], bonusPoints=[STRENGTH, INTELLIGENCE], icon='<:shehisa:919863933320454165>',say=shehisaSays),
    tmpAllie("Ruby", 2, 0x870a24, MAGE, spaceMetRuneLong, [redbutbar, redbutterflyshirt, redButterFlyBoots], GENDER_FEMALE, [invocCarbunR, space3, space2, spaceElemUse, maitriseElementaire, magicEffGiver], element=[ELEMENT_SPACE, ELEMENT_DARKNESS], icon='<:ruby:958786374759251988>', bonusPoints=[MAGIE, PRECISION]),
    tmpAllie("Sixtine", 1, blue, INOVATEUR, miltrilPlanisphere, [sixitneBarrette, sixitnePull, sixitneBoots], icon='<:sixtine:908819887059763261>', skill=[divination, horoscope, nostalgia, revelation, sixtineUlt, expediant, aff2], gender=GENDER_FEMALE, element=[ELEMENT_NEUTRAL, ELEMENT_AIR], bonusPoints=[INTELLIGENCE, ENDURANCE], description="Soeur cadette, Sixtine est plutôt du genre à vouloir rester dans son coin sans être dérangée\n\nElle ne se démarque pas particulièrement de Félicité ou Alice, mais ça ne la dérange pas. Elle passe le plus clair de son temps libre à rêvasser, à du mal à faire le premier pas vers les autres et n'a pas vraiment l'air de s'interresser à grand chose\nMais quand elle s'interresse à un truc, elle veux souvent en connaître un maximum de chose dessus.", say=sixtineSays,birthday=(12,6)),
    tmpAllie("Hina", 1, purple, ATTENTIF, plume, [hinaAcc, hinaBody, hinaShoes], GENDER_FEMALE, [multishot, multiMissiles, hinaUlt, airlame, preciseShot, physEffGiver], icon='<:hina:908820821185810454>', element=[ELEMENT_AIR, ELEMENT_SPACE], bonusPoints=[AGILITY, STRENGTH], description="Oiseau des îles, Hina n'a pas froid aux yeux lorsqu'il s'agit d'aventure.\nA embarquer avec la première pirate venue ça ne lui a apporté que des problèmes avec les forces maritimes.\nCependant elle manque pas mal de confiance en elle et a fait beaucoup trop d'erreur qui lui coute des amitiés."),
    tmpAllie("John", 2, orange, POIDS_PLUME, airsword, [bandNoir, pullCamo, kanisand], GENDER_MALE, [airlame, airStrike, splashdown, maitriseElementaire, physEffGiver],description="Un Loup Garou qui a réussi à tomber amoureux de la vampire responsable des pluparts des vas et viens à l'infirmerie du village de sa meute\n\nAprès de multiple tentatives de l'approcher sans grand succès, il a réussi à changer la clémence qu'éprouvait cette dernière à son égars en affection, mais a peur d'essayer de monter dans son estime", icon='<:john:908887592756449311>', bonusPoints=[STRENGTH, AGILITY], say=johnSays, element=ELEMENT_AIR),
    tmpAllie("Julie", 1, red, ALTRUISTE, julieWeap, [julieHat, julieDress, julieShoes], GENDER_FEMALE, [infraMedica, altOH, julieUlt, timeSp, zelian, extraMedica, shareSkill],"La principale (et unique) servante d'une des vampires les plus puissante du pays.\nElle a appris la magie curative à l'aide des nombreux grimoires dans la bibliothèque du manoire, mais il lui arrive souvent de demander de l'aide à Clémence lorsque sa maîtresse (qui ai d'ailleurs la tutrice magique de cette dernière) lui demande de récupérer des organes de monstres.\nElle se sent souvent petite, en compagnie de ces puissantes vampires\n\nDire qu'elle est légèrement inspirée serait un euphémisme. Au moins elle utilise pas de dagues", element=[ELEMENT_TIME, ELEMENT_FIRE], bonusPoints=[CHARISMA, INTELLIGENCE], icon="<:julie:910185448951906325>", say=julieSays),
    tmpAllie("Krys", 2, purple, TETE_BRULE, krystalFist, [kryscharpe, krysshirt, kryschains], GENDER_OTHER, [earthStrike, defi, krysUlt, mudlame, demolish,krystalisation], "\"Krys Tal (rien à voir avec la chanteuse ou les opticiens) est un cristal (nooon sans blague) ayant gagné une conscience par un procédé mystérieux.\n\nN'étant pas une forme de vie organique, il se nourrit de minéraux qui traînent par-ci par-là, et de l'armure occasionnelle en combat. Il évite habituellement la nourriture organique, mais il ne dira jamais non à un peu de pop-corn, dont il semble avoir une réserve infinie.\n\nExtrêmement sensible à l'eau, mais n'hésitera pas à ingérer le contenu de la première cannette qui traîne.\n\nAvant, il était un peu con, mais ça, c'était av-Ah on m'annonce dans l'oreillette que c'est toujours le cas, my bad.\n\nPas le plus grand fan d'Akira depuis un sombre incident dans un labo.\"", element=[ELEMENT_EARTH, ELEMENT_EARTH], icon="<:krys:916118008991215726>", deadIcon='<:krysCan:916117137339322388>', bonusPoints=[ENDURANCE, STRENGTH]),
    tmpAllie("Edelweiss", 1, white, PREVOYANT, bleuSpiritWings, [battleShieldHat, battleShieldUnif, battleShieldShoes], GENDER_FEMALE, [haimaSkill, preOS, soulagement, intelRaise, pepsis, invocSeraf, pneuma], element=[ELEMENT_EARTH, ELEMENT_WATER], icon='<:edelweiss:918451422939451412>', deadIcon="<:flowernt:894550324705120266>", bonusPoints=[INTELLIGENCE, ENDURANCE]),
    tmpAllie("Iliana", 1, white, ALTRUISTE, infLightSword, [zenithHat, zenithArmor, zenithBoots], GENDER_FEMALE, [lightAura2, ironWillSkill, clemency, lightBigHealArea, aurore2, holiomancie, holyShieltron], "Une Neko paladine qui se bat pour faire perdurer la Lumière dans sa dimension\nRelativement timide, elle ne va pas souvent vers les inconnus, mais ça ne l'empêche pas de faire de son mieux pour les tenir en vie tout de même", [ELEMENT_LIGHT, ELEMENT_DARKNESS], icon='<:Iliana:926425844056985640>', deadIcon='<:oci:930481536564879370>', bonusPoints=[CHARISMA, ENDURANCE], say=ilianaSaysNormal),
    tmpAllie('Candy', 2, 0xa124b2, INOVATEUR, concentraceurZoom, [summonerFoulard50, summonerMenteau50, summonerShoes50], GENDER_FEMALE, [invocBat, invocSeaker, bombRobot, killerWailUltimate, invocFee,invocCarbunR, invocCarbObsi], "Jeune ingénieur de l'Escardon Espadon Nouvelle Génération, elle s'entend très bien avec sa supérieur", icon='<:candy:933518742170771466>', bonusPoints=[MAGIE, STRENGTH]),
    tmpAllie('Ly', 1, white, ATTENTIF, firework, [critIndStrHat45, critIndStrBody45, critIndStrShoes45], GENDER_FEMALE, [booyahBombCast, morsTempSkill, multishot, splatbomb, machDeFer, morsCaudiqueSkill, lanceTox],"Une mercenaire rencontrée sur les îles\nElle préfère rester loin et innonder ses ennemis avec ses attaques de zones", [ELEMENT_FIRE, ELEMENT_SPACE], icon='<:ly:943444713212641310>', bonusPoints=[STRENGTH, PRECISION], say=lySays),
    tmpAllie('Anna', 2, black, PROTECTEUR, lunarBonk, [fullMoonHat, fullMoonArmor, fullMoonBoots], GENDER_FEMALE, [royaleGardeSkill, darkShield, isolement,heartStone, haimaSkill, intelRaise], element=[ELEMENT_LIGHT, ELEMENT_WATER], icon='<:anna:943444730430246933>', bonusPoints=[ENDURANCE, INTELLIGENCE]),
    tmpAllie("Elina", 1, 0x560909, ALTRUISTE, serringue, [urgChirHat, urgChirDress, urgChirShoes], GENDER_FEMALE, [preciChi, cure, adrenaline, firstheal, cure2Bundle], element=[ELEMENT_LIGHT, ELEMENT_NEUTRAL], icon='<:elina:950542889623117824>', bonusPoints=[CHARISMA, PRECISION]),
    tmpAllie("Bénédicte", 1, white, MAGE, magicWood, [mysticHat, mysticBody, mysticBoots], GENDER_FEMALE, [genesis, comboVerMiracle, redemption, benitWater, divineSave], element=[ELEMENT_LIGHT, ELEMENT_LIGHT], bonusPoints=[MAGIE, CHARISMA], icon='<:benedict:958786319776112690>')
]

# Shushi alt spells
shushiSkill1 = skill("Frappe lumineuse", "shushiSkill1", TYPE_DAMAGE, 0,150, cooldown=3, use=MAGIE, emoji='<a:ShushiLF:900088862871781427>')
shushiSkill3Eff = effect("Jeu de lumière", "diff", redirection=35, trigger=TRIGGER_DAMAGE,description="Un habile jeu de lumière permet de vous cacher de vos ennemis")
shushiSkill3 = skill("Diffraction", "shushiSkill2", TYPE_ARMOR, 0, 0, AREA_CIRCLE_6, effect=shushiSkill3Eff,cooldown=5, initCooldown=2, use=None, emoji='<a:diffraction:916260345054658590>')
shushiSkill4Eff = effect("Assimilation", "assimil", MAGIE, resistance=10, overhealth=150, description="Grâce à Shihu, vous avez réussi à utiliser les Ténèbres environant à votre avantage",emoji=uniqueEmoji("<:tarmor:909134091604090880>"), type=TYPE_ARMOR, trigger=TRIGGER_DAMAGE)
shushiSkill4 = skill("Assimilation", "shushiSkill4", TYPE_ARMOR, 0, cooldown=3, effect=shushiSkill4Eff,say='On peut y awiver !', use=MAGIE, emoji='<:assimilation:916260679944634368>')
shushiWeapEff = effect("Lueur Ténébreuse", "darkLight", MAGIE, resistance=5, overhealth=50,type=TYPE_ARMOR, emoji=uniqueEmoji('<:dualMagie:899628510463803393>'))
shushiWeap = weapon("Magie trancendante", "dualMagie", RANGE_LONG, AREA_DONUT_5, 35, 100, 0, strength=-20, endurance=10, charisma=20, intelligence=20,magie=55, type=TYPE_HEAL, target=ALLIES, use=MAGIE, effectOnUse=shushiWeapEff, affinity=ELEMENT_LIGHT, emoji='<:dualMagie:899628510463803393>')
shushiHat = stuff("Barrête de la cohabitation", "dualHat", 0, 0, strength=-20, endurance=15, charisma=20, agility=10,precision=10, intelligence=20, magie=45, affinity=ELEMENT_LIGHT, emoji='<:coaBar:911659734812229662>')
shushiDress = stuff("Robe de la cohabitation", "dualDress", 1, 0, strength=-10, endurance=35, charisma=20, agility=0,precision=10, intelligence=10, magie=60, resistance=20, affinity=ELEMENT_LIGHT, emoji='<:coaDress:911659797076660294>')
shushiBoots = stuff("Bottines de la cohabitation", "dualBoost", 2, 0, strength=-10, endurance=15, charisma=0, agility=20,precision=10, magie=45, intelligence=10, affinity=ELEMENT_LIGHT, emoji='<:coaBoots:911659778995007528>')
shushiSkill5 = skill("Lumière éternelle", "LumEt", TYPE_RESURECTION, 0, 100, emoji='<:renisurection:873723658315644938>',cooldown=3, description="Permet de ressuciter un allié", use=MAGIE, range=AREA_DONUT_7)
shushiArmorSkillEff = effect("Armure Harmonique", "shushiArmor", MAGIE, overhealth=200, turnInit=3,type=TYPE_ARMOR, trigger=TRIGGER_DAMAGE, emoji=uniqueEmoji("<a:transArmorB:900037831257358378>"))
shushiArmorSkill = skill("Armure Harmonique", "shushiArmorSkill", TYPE_ARMOR, 0, effect=shushiArmorSkillEff,range=AREA_MONO, area=AREA_CIRCLE_5, cooldown=7, use=MAGIE, emoji='<a:transArmorB:900037831257358378>')

# Alice Ex. skills
clemBloodJauge = effect("Jauge de sang","clemBloodJauge",turnInit=-1,unclearable=True,emoji=uniqueEmoji('<:clemBJ:914710384299106345>'),lvl=100,description="Clémence possédée tourne autour de sa Jauge de Sang\n\nElle débute le combat avec une jauge à **100** Points de sang, son maximum.\nChacunes de ses compétences ont un coût en Points de Sang, qui sont retiré à la jauge à la fin de leur utilisation\n\nSi la jauge de sang tombe à **0 point**, Clémence est étourdie pendant 2 tours durant lesquels sa résistance est diminuée\nLa jauge de sang récupère **1 point** de sang à chaque fois que Clémence inflige 50 points de dégâts, et **100 points** une fois que Clémence n'est plus étourdie\n\nLa quantité de points de sang dans la jauge de sang est constamant visible\nClémence possède 10% de vol de vie")

aliceBloodJauge = copy.deepcopy(clemBloodJauge)
aliceBloodJauge.emoji = uniqueEmoji("<:aliceBJ:914798086667264010>")
aliceBloodJauge.description = "Alice exaltée tourne autour de sa Jauge de Sang\n\nElle débute le combat avec une jauge à **100** Points de sang, son maximum.\nChacunes de ses compétences ont un coût en Points de Sang, qui sont retiré à la jauge à la fin de leur utilisation\n\nSi la jauge de sang tombe à **0 point**, Alice est étourdie pendant 2 tours durant lesquels sa résistance est diminuée\nLa jauge de sang récupère **1 point** de sang à chaque fois que Alice soigne 50 points de vie, et **100 points** une fois qu'Alice n'est plus étourdie\n\nLa quantité de points de sang dans la jauge de sang est constamant visible"

aliceExHeadruban = stuff("Ruban vampirique", "aliceExHead", 0, 0, charisma=40, negativeHeal=-50, endurance=55, emoji=batRuban.emoji)
aliceExDress = stuff("Robe vampirique", "aliceExDress", 1, 0, endurance=10, resistance=15, charisma=45, negativeHeal=-25, emoji=aliceDress.emoji)
aliceExShoes = stuff("Ballerines vampiriques", "aliceExShoes", 2, 0, agility=25, charisma=45, negativeHeal=-35, endurance=5, emoji=aliceShoes.emoji)

aliceExWeapEff = effect("Bénédiction vampirique", "aliceExWeapEff", CHARISMA, emoji=uniqueEmoji("<:vampire:900312789686571018>"), power=20, type=TYPE_INDIRECT_HEAL, trigger=TRIGGER_AFTER_DAMAGE, description="Cet effect confère **{0}%** de Vol de Vie au porteur.\nLe pourcentage de convertion est augmenté par les statistiques du lanceur")
aliceExWeap = weapon("Rosa receptaculum", "aliceExWeap", RANGE_DIST, AREA_CIRCLE_5, 50, 100, 0, use=CHARISMA, charisma=35, resistance=10, type=TYPE_HEAL, target=ALLIES, effectOnUse=aliceExWeapEff, effect=aliceBloodJauge, emoji='<:vampBall:916199488891273276>', say=["Je vais essayer de vous faire tenir le plus longtemps possible...", "Je sais que tu en as encore en réserve, c'est pas vraiment le moemenent de lacher !", "On tiens le bon bou, continuons comme ça !", "Mhf..."])
aliceSkill1Eff = effect("Régénération vampirique", "aliceRegenEff", CHARISMA, power=15, emoji=uniqueEmoji("<a:aliceSkill1:914787461949960202>"), type=TYPE_INDIRECT_HEAL,turnInit=3, lvl=3, area=AREA_CIRCLE_2, description="Au début du tour du porteur, lui et ses alliés proches recoivent des soins", trigger=TRIGGER_START_OF_TURN)
aliceSkill1 = skill("Sort - Rénégération", "aliceSkill1", TYPE_INDIRECT_HEAL, 0,0, emoji="<a:aliceSkill1:914787461949960202>", effect=aliceSkill1Eff, cooldown=3)
aliceSkill2Eff = effect("Galvanision vampirique", "aliceBoostEff", CHARISMA, strength=12,magie=12, percing=3, emoji=uniqueEmoji('<a:aliceSkill2:914791502931197962>'))
aliceSkill2 = skill("Sort - Galvanisation", "aliceSkill2", TYPE_BOOST, 0, range=AREA_MONO, area=AREA_DONUT_3, effect=aliceSkill2Eff, cooldown=2, emoji='<a:aliceSkill2:914791502931197962>', say=["Allez-s'y !", "Ce truc qui la possède n'a pas l'air d'avoir compris un quart de toutes les possibilités qui s'offraient à lui... Profitez-en !", "Il va falloir essayer un peu plus fort que ça..."])
aliceSkill3 = skill("Rune - Flos luminosus", "aliceSkill3", TYPE_DAMAGE, 0, 130, emoji='<a:aliceSkill3:914794172215623690>', cooldown=2,use=CHARISMA, say=["Tu va la laisser tranquille oui !?", "Sit invehitur Rosa Lucis !", "Tuum, Rosa Lucis !", "Paenitet..."])
aliceSkill4 = skill("Rune - Pleine lune", "aliceSkill4", TYPE_HEAL, 0, 120, AREA_MONO, area=AREA_CIRCLE_3, use=CHARISMA, cooldown=3,emoji='<a:aliceSkill4:914796355925458984>', say=["On lache rien !", "Je donnerais tout, même si je dois y passer !", "Courage !", "Sanet nos lux plenae lunae !"])
aliceRez = skill("Vampirization", "aliceRez", TYPE_RESURECTION, 0, 350, range=AREA_CIRCLE_7, emoji="<a:memAlice2:908424319900745768>", use=CHARISMA,description="Si plus de la moitié de l'équipe est morte, la zone d'effet de la compétence deviens un cercle de 7 cases autour de Alice, mais consomme l'intégralité de sa jauge de sang", say=["C'est trop tôt pour laisser tomber !", "On a encore besoin de toi !"])
aliceRez2 = skill("Salutaris meridiem", "aliceRez+", TYPE_RESURECTION, 0, 350, range=AREA_MONO, area=AREA_CIRCLE_7,emoji="<a:memAlice2:908424319900745768>", use=CHARISMA, say="Angeli, audi me et adiuva nos, sustulite... MEMENTO VOCIS ANGELI !")

# Clem Ex.
clemBleeding = copy.deepcopy(bleeding)
clemBleeding.power, clemBleeding.stat, clemBleeding.name = 50, MAGIE, "Sanguisugae"
clemExSkill1 = skill("Exponentia Catenae", "clemExSkill1", TYPE_DAMAGE, 0, power=100, effectOnSelf=quickCastEff, replay=True, use=MAGIE,description="Inflige des dégâts, puis vous permet de rejouer votre tour en ignorant un tour de chargement de la prochaine compétence utilisée", cooldown=4, initCooldown=2, emoji=quickCast.emoji, lifeSteal=35)
clemExSkill21Lauch = skill("Sanguinis Explosio", "clemExSkill2Launch", TYPE_DAMAGE, 0, initCooldown=2, power=750,area=AREA_CIRCLE_2, use=MAGIE, cooldown=6, description="Déclanche une explosion infligeant de lourds dégâts dans une large zone")
clemExSkill21CastEff = effect("Cast - Sanguinis Explosio", "clemExSkill2CastEff",replique=clemExSkill21Lauch, silent=True, turnInit=2)
clemExSkill22Lauch = skill("Sanguinis Ray",clemExSkill21Lauch.id,TYPE_DAMAGE,power=1250,range=AREA_MONO,area=AREA_INLINE_5,sussess=250,initCooldown=clemExSkill21Lauch.initCooldown,cooldown=clemExSkill21Lauch.cooldown,setAoEDamge=True,use=MAGIE,description="Tir un grand rayon d'énergie à vos points caridaux, infligeant d'extrèmes dégâts à tous les ennemis alignés\nNe peux pas être esquivé et ignore **35%** de la résistance ennemie",percing=35)
clemExSkill22Cast = effect("Cast - {0}".format(clemExSkill22Lauch.name),"clemRayonSanguinCastEff",silent=True,turnInit=2,replique=clemExSkill22Lauch)
clemExSkill22 = copy.deepcopy(clemExSkill22Lauch)
clemExSkill22.power, clemExSkill22.effectOnSelf = 0, clemExSkill22Cast
clemExSkill21 = copy.deepcopy(clemExSkill21Lauch)
clemExSkill21.power, clemExSkill21.effectOnSelf = 0, clemExSkill21CastEff
clemExSkill2 = skill('Sanguis Bang',clemExSkill21.id,TYPE_DAMAGE,cooldown=clemExSkill21.cooldown,use=MAGIE,become=[clemExSkill21,clemExSkill22],area=AREA_CIRCLE_2)
clemExSkill3 = skill("Sanguis Hastis", "clemExSkill3", TYPE_DAMAGE, 0, power=250, range=AREA_DIST_7, use=MAGIE,area=AREA_CIRCLE_1, cooldown=3, description="Inflige de lourd dégâts à l'ennemi éloignés ciblé et ses alliés alentours")
clemExSkill4 = skill("Hastae Noctis", "clemExSkill4", TYPE_DAMAGE, 0, power=300,use=MAGIE, cooldown=2, description="Inflige de lourd dégâts monocibles et vous soigne d'une partie des dégâts infligés",lifeSteal=35)
clemExSkill5 = skill("Saturi Cum Sanguine", "clemExSkill5", TYPE_DAMAGE, 0, power=250, range=AREA_MONO,area=AREA_CIRCLE_2, use=MAGIE, cooldown=5, description="Inflige de lourd aux ennemis alentours")
clemExSkill6 = skill("Sanguis Pluvia", "clemExSkill6", TYPE_DAMAGE, power=50, range=AREA_MONO, area=AREA_ALL_ENEMIES, initCooldown=2, use=MAGIE,cooldown=5, setAoEDamge=True, replay=True, description="Inflige des dégâts à tous les ennemis en volant une partie des dégâts infligés, tout en leur infligeant un effet de dégâts indirects sur la durée",lifeSteal=35,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_ALL_ENEMIES,clemBleeding])
clemExSkill7Eff = copy.deepcopy(dmgUp)
clemExSkill7Eff.power, clemExSkill7Eff.turnInit = 35, 3
clemExSkill7 = skill("Sanguis Exaltus", "clemExSkill7", TYPE_BOOST, range=AREA_MONO, emoji='<a:dmgBuffB:954429227657224272>', effect=clemExSkill7Eff, cooldown=7,description="Augmente vos dégâts de **{0}%** pendant {1} tours et vous permet de rejouer votre tour".format(clemExSkill7Eff.power, clemExSkill7Eff.turnInit),replay=True)

clemExSay = says(
    start="Très bien, vous l'avez cherché.",
    ultimate="Voyons voir comment vous en sortirez face à ça !",
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
iliPreSkill1 = skill("Champ lumineux", 'iliSkill1', TYPE_INDIRECT_DAMAGE, effect=iliPrePoi, range=AREA_MONO, area=AREA_CIRCLE_3, use=CHARISMA, cooldown=4, effectAroundCaster=[TYPE_ARMOR, AREA_MONO, iliPreArmor], description='Donne un effet de dégâts indirects aux ennemis alentours et vous procure une armure')
iliPreRegen = effect("Régénération de Lumière", "ilianaRegen", CHARISMA, power=50, trigger=TRIGGER_START_OF_TURN, type=TYPE_INDIRECT_HEAL,emoji='<a:ilianaRegen:969825374093578260>', turnInit=5, stackable=True, description="Soigne le porteur de l'effet au début de son tour")
iliPreSkill2Heal = skill('Rénération', "iliSkill2", TYPE_HEAL, power=200, range=AREA_CIRCLE_7, effect=iliPreRegen,cooldown=3, description="Soigne l'allié ciblé et lui procure un effet de régénération sur la durée", use=CHARISMA,emoji='<a:ilianaRegen:969825374093578260>')
iliPreSkill2Shield = skill("Armure de lumière","iliSkill2", TYPE_ARMOR, effect=iliPreArmor,cooldown=iliPreSkill2Heal.cooldown,range=iliPreSkill2Heal.range,description="Procure une grosse armure à l'allié ciblé",effPowerPurcent=1.2)
iliPreSkill2 = skill("Pouvoir de la lumière","iliSkill2",TYPE_HEAL,cooldown=3,become=[iliPreSkill2Heal,iliPreSkill2Shield])
iliPreSkill3 = skill("Tourbillon de Lumière", "iliSkill3", TYPE_DAMAGE, power=150, range=AREA_MONO,area=AREA_CIRCLE_2, use=CHARISMA, description="Inflige des dégâts aux ennemis alentours")
iliPreDmgReduc = copy.deepcopy(defenseUp)
iliPreDmgReduc.power = 80
iliPreSkill4 = skill("Lumière Eternelle", "lb", TYPE_ARMOR, emoji=trans.emoji, use=None, range=AREA_MONO, area=AREA_ALL_ALLIES,ultimate=True, effect=[iliPreDmgReduc, iliPreRegen], cooldown=7, description='Réduit les dégâts subis par tous les allié de 80%')
iliStans = effect("Conviction de la Lumière", "ilianaStans", charisma=30, resistance=20,aggro=100, turnInit=-1, unclearable=True, emoji='<:ilianaStans:969819202032664596>')
iliPreSkill5 = skill("Conviction de la Lumière", "ilianaSkill5",TYPE_PASSIVE, effectOnSelf=iliStans, emoji='<:ilianaStans:969819202032664596>')
iliPreSkill6 = skill("Vitesse Lumière", "iliSkill6", TYPE_DAMAGE, power=50, range=AREA_INLINE_4, replay=True, cooldown=2, tpCac=True,use=CHARISMA, description='Vous téléporte au corps à corps de l\'ennemi ciblé et vous permet de rejouer votre tour')
iliPreSkill7Dmg = skill("Rayon de Lumière", "iliSkill7", TYPE_DAMAGE, power=150, range=AREA_CIRCLE_1, area=AREA_LINE_6, cooldown=4, use=CHARISMA,effectOnSelf= iliPreArmor, description="Inflige des dégâts sur une ligne droite puis vous procure une armure")
iliPreSkill7RedirectEff = effect("Diffraction","iliRedirect",redirection=100)
iliPreSkill7Redirect = skill('Diffraction',"iliPreSkill7",TYPE_BOOST,effect=iliPreSkill7RedirectEff,range=AREA_DONUT_7,effectOnSelf=iliPreRegen,cooldown=iliPreSkill7Dmg.cooldown)
iliPreSkill7 = skill("Jeu de lumière",'iliPreSkill7',TYPE_DAMAGE,become=[iliPreSkill7Dmg,iliPreSkill7Redirect],cooldown=4)
iliWeapEff = effect("Conviction de la Lumière", "iliWeapRegenEff", CHARISMA, power=15,turnInit=-1, unclearable=True, type=TYPE_INDIRECT_HEAL, trigger=TRIGGER_START_OF_TURN, emoji='<a:ilianaRegen:969825374093578260>')
iliWeap = weapon("Epée et Bouclier de la Lumière", "iliWeap", RANGE_MELEE, AREA_CIRCLE_1, 50, 75, charisma=30, endurance=20,resistance=15, effect=iliWeapEff, area=AREA_CIRCLE_1, ignoreAutoVerif=True, emoji=infLightSword.emoji, use=CHARISMA)

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
lunaSkill4_1 = skill("Convertion rapprochée",'lunaSkill4',TYPE_INDIRECT_DAMAGE,0,range=AREA_MONO,area=AREA_CIRCLE_2,effect=lunaSkill4EffAlt,cooldown=3,emoji=lunaSkill4Eff.emoji[0][0],say=['Vous tenez tant à voir les Ténèbres de plus près ? Voilà pour vous !','Votre Lumière ne vous protègera pas éternellement.'],description="Donne un effet de dégâts indirect monocible aux ennemis proches")
lunaSkill4_2 = skill("Convertion externe",'lunaSkill4',TYPE_INDIRECT_DAMAGE,0,range=AREA_MONO,area=AREA_DIST_7,effect=lunaSkill4Eff,cooldown=3,emoji=lunaSkill4Eff.emoji[0][0],say=["C'est pas parceque vous restez loin que vous serez épargné !","Votre Lumière sucombera à mes Ténèbres."],description="Inflige un effet de dégâts indirect en zone aux ennemis éloignés")

lunaSkill4 = skill("Convertion","lunaSkill4",TYPE_INDIRECT_DAMAGE,0,range=AREA_CIRCLE_7,use=STRENGTH,say="Votre Lumière ne vous protègera pas éternellement !",emoji=lunaSkill4Eff.emoji[0][0],become=[lunaSkill4_1,lunaSkill4_2])
lunaSkill5_1 = skill("Reverse roundhouse-kick","lunaSkill5",TYPE_DAMAGE,0,100,AREA_CIRCLE_1,area=AREA_ARC_1,emoji='<:luna4inOne:919260128698589184>',damageOnArmor=2,description='Inflige des dégâts en zone à un ennemi au corps à corps')
lunaSkill5_2 = skill("Side-kick fouetté","lunaSkill5",TYPE_DAMAGE,0,135,AREA_CIRCLE_1,emoji='<:luna4inOne:919260128698589184>',say="Hmf !",damageOnArmor=3,description='Inflige des dégâts à une cible unique au corps à corps\nDégâts triplé sur de l\'armure')
lunaSkill5_3_eff = effect("Destabilisé","lunaSkill5_3Eff",type=TYPE_MALUS,emoji="<:stun:882597448898474024>",stun=True)
lunaSkill5_3 = skill("Sweeping into Backflip","lunaSkill5",TYPE_DAMAGE,0,80,AREA_CIRCLE_1,repetition=2,effect=lunaSkill5_3_eff,knockback=1,emoji='<:luna4inOne:919260128698589184>',say="C'est que tu es colant toi !",description='Inflige des dégâts, étourdit pendant un tour et repousse un ennemi au corps à corps')
lunaSkill5_4 = skill("Double High roundhouse-kick into Side-kick","lunaSkill5",TYPE_DAMAGE,0,40,AREA_CIRCLE_1,repetition=3,knockback=3,emoji='<:luna4inOne:919260128698589184>',say="Hé vous derrière ! Cadeau !",damageOnArmor=2,description='Inflige des dégats et repousse de 3 cases un ennemi au corps à corps')
lunaSkill6 = skill("Vitesse ombrale","lunaSkill6",TYPE_DAMAGE,0,50,AREA_INLINE_4,emoji='<:lunaDash:932286143884566528>',cooldown=2,replay=True,tpCac=True,sussess=200,description='Se téléporte au corps à corps d\'un ennemi et vous permet de rejouer votre tour')
lunaSkill7 = skill("Ultimawashi","lunaSkill7",TYPE_DAMAGE,0,150,AREA_CIRCLE_1,cooldown=3,knockback=10,sussess=200,emoji='<:ultimawashi:932378739327787078>',description="Inflige de lourd dégâts et repousse violament un ennemi au corps à corps")
lunaQuickFightEff = effect('Enchaînement',"lunaQuickFight",emoji=uniqueEmoji('<:qqLuna:932318030380302386>'))
lunaSkill5Base = skill("Corps à corps","lunaSkill5",TYPE_DAMAGE,0,0,AREA_CIRCLE_1,description="Cette compétence peut avoir 4 effets différents, sélectionné de manière aléatoire",emoji='<:luna4inOne:919260128698589184>',become=[lunaSkill5_1,lunaSkill5_2,lunaSkill5_3,lunaSkill5_4])

lunaPreSkill5_1 = copy.deepcopy(lunaSkill5_4)
lunaPreSkill5_1.cooldown, lunaPreSkill5_1.description = 2, "Effectue plusieurs attaques sur un adversaire\n__Puissance estimée :__ **{0}**".format(int(lunaPreSkill5_1.power*lunaPreSkill5_1.repetition)+int(lunaSkill5_2.power*lunaSkill5_2.repetition)+int(lunaSkill5_1.power*lunaSkill5_1.repetition))
lunaPreSkill5_1_cast = effect("Enchainement 4","ench4",silent=True,replique=lunaPreSkill5_1)
lunaPreSkill5_2 = copy.deepcopy(lunaSkill5_2)
lunaPreSkill5_2.effectOnSelf, lunaPreSkill5_2.replay = lunaPreSkill5_1_cast, True
lunaPreSkill5_2_cast = effect("Enchaînement 3","ench3",silent=True,replique=lunaPreSkill5_2)
lunaPreSkill5_3 = copy.deepcopy(lunaSkill5_1)
lunaPreSkill5_3.effectOnSelf, lunaPreSkill5_3.replay, lunaPreSkill5_3.description, lunaPreSkill5_3.name = lunaPreSkill5_2_cast, True, "Effectue plusieurs attaques sur un adversaire\n__Puissance estimée :__ **{0}**".format(int(lunaPreSkill5_1.power*lunaPreSkill5_1.repetition)+int(lunaPreSkill5_2.power*lunaPreSkill5_2.repetition)+int(lunaPreSkill5_3.power*lunaPreSkill5_3.repetition)), "Combo Corps à Corps"
lunaPreSkill2_eff = effect("Ténèbres d'Obsidienne","lunaPreIndirect",STRENGTH,power=80,emoji='<:lunaIndi:932447879786823730>',turnInit=3,lvl=3,trigger=TRIGGER_START_OF_TURN,type=TYPE_INDIRECT_DAMAGE)
lunaPreSkill2 = skill("Obsidienne Ténébreuse","lunaPreSkill2",TYPE_INDIRECT_DAMAGE,emoji=lunaPandan.emoji,effect=lunaPreSkill2_eff,effectAroundCaster=[TYPE_INDIRECT_DAMAGE,AREA_INLINE_4,lunaPreSkill2_eff],range=AREA_MONO,area=AREA_CIRCLE_4,cooldown=4,description="Inflige un effet de dégâts indirects aux ennemis alentours. Les adversaires allignés subissent une deuxième fois l'effet")
lunaPreSkill3 = skill("Frappe d'Obsidienne","lunaPreSkill3",TYPE_DAMAGE,emoji=lunaSkill2.emoji,power=int(lunaSkill2.power*lunaSkill2.repetition*1.25),cooldown=lunaSkill2.cooldown,description="Inflige de lourd dégâts à un ennemi.\n__Puissance :__ **{power}**")
lunaDarkChoc = copy.deepcopy(lunaSkill)
lunaDarkChoc.power, lunaDarkChoc.lifeSteal, lunaDarkChoc.cooldown, lunaDarkChoc.description, lunaDarkChoc.name = 200, 15, 5, "Vous téléporte au corps à corps de l'ennemi ciblé et lui porte une attaque infligeant des dégâts de zone tout en vous restituant un pourcentage des dégâts infligés.\n__Puissance :__ **200**", "Choc d'Obsidienne"
lunaPreUltimawashi = copy.deepcopy(lunaSkill7)
lunaPreUltimawashi.area, lunaPreUltimawashi.name, lunaPreUltimawashi.description = AREA_CIRCLE_1, "Piqué Ténébreux", "Inflige des dégâts à l'ennemi ciblé ainsi qu'aux adversaires alentours, puis repousse violament ce premier.\n__Puissance :__ **{0}**".format(lunaPreUltimawashi.power)

# Tabl var allies =============================================================================
tablVarAllies = [
    tmpAllie("Luna", 1, black, POIDS_PLUME, infDarkSword, [lunaPandan, lunaDress, lunaBoots], GENDER_FEMALE, [defi, splatbomb, ironStormBundle, soupledown, highkick, calestJump, foullee],"Là où se trouve la Lumière se trouvent les Ténèbres", [ELEMENT_DARKNESS, ELEMENT_LIGHT], variant=True, icon='<:luna:909047362868105227>', bonusPoints=[STRENGTH, ENDURANCE], say=lunaSays),
    tmpAllie("Altikia", 2, yellow, VIGILANT, fleau, [zenithHat, zenithArmor, zenithBoots], GENDER_FEMALE, [ironWillSkill, holyShieltron, lightBigHealArea, renisurection, concen, clemency, regenVigil],"Une personnalité de Gwen qui préfère se concentrer sur ses alliés", [ELEMENT_LIGHT, ELEMENT_FIRE], variant=True, bonusPoints=[ENDURANCE, CHARISMA], icon='<:alty:906303048542990347>', say=altySays),
    tmpAllie("Klironovia", 2, yellow, BERSERK, klikliSword, [darkbutbar, darkChemVeste, darkButterFlyBoots], GENDER_FEMALE, [demolish, trans, bloodyStrike, absorbingStrike2, highkick, holmgang, bloodPact],"Une personnalité de Gwen bien plus violente que les deux autres", [ELEMENT_EARTH, ELEMENT_TIME], variant=True, bonusPoints=[STRENGTH, AGILITY], icon='<:klikli:906303031837073429>', say=klikliSays),
    tmpAllie("Shihu", 1, black, MAGE, darkMetRuneMid, [shihuHat, shihuDress, shihuShoe], GENDER_FEMALE, [dark2, dark3, suppr, darkBoomCast, quickCast, mageSkill, maitriseElementaire],"\"Eye veut zuste un pi d'attenchions...\" - Shushi", [ELEMENT_DARKNESS, ELEMENT_SPACE], variant=True, icon='<:shihu:909047672541945927>', bonusPoints=[MAGIE, STRENGTH], say=shihuSays),
    tmpAllie("Shushi Cohabitée", 1, blue, PREVOYANT, shushiWeap, [shushiHat, shushiDress, shushiBoots], GENDER_FEMALE, [shushiSkill1, shushiArmorSkill, shushiSkill3, shushiSkill4, shushiSkill5],"S'étant comprise l'une et l'autre, Shushi et Shihu ont décidé de se liguer contre la mère de cette dernière.\nCette allié temporaire n'apparait que contre le boss \"Luna\"", [ELEMENT_LIGHT, ELEMENT_DARKNESS], True, icon='<:shushiCoa:915488591654842368>', bonusPoints=[MAGIE, AGILITY]),
    tmpAllie("Alice Exaltée", 1, aliceColor, ALTRUISTE, aliceExWeap, [aliceExHeadruban, aliceExDress, aliceExShoes], GENDER_FEMALE, [aliceRez, aliceSkill1, aliceSkill2, aliceSkill3, aliceSkill4], "Voyant qu'elle n'arriverai pas à ramener sa sœur à la raison, Alice a décider d'aller contre ses principes et de révéler toute sa puissance vampirique pour tenter de redresser la balance.\nN'apparait que contre Clémence possédée", element=[ELEMENT_LIGHT, ELEMENT_FIRE], variant=True, deadIcon="<:AliceOut:908756108045332570>", icon="<a:aliceExalte:914782398451953685>", bonusPoints=[CHARISMA, ENDURANCE], say=aliceExSays),
    tmpAllie("Clémence Exaltée", 2, red, MAGE, clemExWeapon, [miniStuff, miniStuff, miniStuff], GENDER_FEMALE, [clemExSkill1, clemExSkill2, clemExSkill3, clemExSkill4, clemExSkill5, clemExSkill6, clemExSkill7], "WIP, revenez plus tard", [ELEMENT_DARKNESS, ELEMENT_LIGHT], icon='<:clemence:908902579554111549>', bonusPoints=[MAGIE, STRENGTH], say=clemExSay, deadIcon='<:AliceOut:908756108045332570>',variant=True),
    tmpAllie('Iliana prê.', 1, white, VIGILANT, iliWeap, [miniStuffHead, miniStuffDress, miniStuffFlats], GENDER_FEMALE, [iliPreSkill4, iliPreSkill5, iliPreSkill6, iliPreSkill1, iliPreSkill2, iliPreSkill3, iliPreSkill7], element=[ELEMENT_LIGHT, ELEMENT_LIGHT], deadIcon='<:oci:930481536564879370>', icon='<:Iliana:926425844056985640>', bonusPoints=[CHARISMA, ENDURANCE], description="Face à une menace dimensionnelle sans précédents, Iliana a décider de réveiller ses pouvoirs de Prêtresse de la Lumière pour faire équipe avec celle des Ténèbres",say=ilianaPreSays,variant=True),
    tmpAllie('Belle', 2, 0x1f0004, ENCHANTEUR, magicSwordnShield, [magicArmorHelmet, magicArmorBody, magicArmorBoots], GENDER_FEMALE, [ferocite, dark3, dark2, innerdarkness, magicRuneStrike, strengthOfDesepearance, undead], element=[ELEMENT_DARKNESS, ELEMENT_NEUTRAL], variant=True, icon='<:belle:943444751288528957>', bonusPoints=[ENDURANCE, MAGIE]),
    tmpAllie("Luna prê.", 1, black, POIDS_PLUME, lunaWeap, [LunaPreStuffHead, LunaPreStuffDress, LunaPreStuffFlats], GENDER_FEMALE, [lunaSpeCast,lunaDarkChoc,lunaPreSkill5_3,lunaPreSkill3,lunaPreSkill2,lunaSkill6,lunaPreUltimawashi], element=[ELEMENT_DARKNESS, ELEMENT_DARKNESS], icon='<:luna:909047362868105227>', bonusPoints=[STRENGTH, AGILITY], say=lunaPreSays,variant=True, description = "Face à une menace temporelle sans précédents, Luna a décidé de réveiller ses pouvoirs de Prêtresse des Ténèbres pour faire équipe avec celle de la Lumière")
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
areaDmgReductionTmp = effect("Dégâts de zone réduits","areaDmgReductionTmp",power=20,turnInit=-1,unclearable=True,type=TYPE_MALUS,description="Les dégâts infligés par les compétences à zone d'effet sont réduits de **20%** sur les cibles secondaires")
healReductionTmp = effect("Soins effectués réduits","healReductionTmp",power=15,turnInit=-1,unclearable=True,type=TYPE_MALUS,description="La puissance des soins effectués est réduite de **15%**")
armorReductionTmp = effect("Armure donnée réduite","armorReductionTmp",power=15,turnInit=-1,unclearable=True,description="Réduit la puissance des armures données de **15%**",type=TYPE_MALUS)
monoDmgReductionTmp = effect("Dégâts monocibles réduits","monoDmgReductionTmp",power=15,turnInit=-1,unclearable=True,description="Réduit les dégâts monocibles infligés de **15%**",type=TYPE_MALUS)
healReciveReductionTmp = effect("Soins reçus diminués","healReciveReductionTmp",power=10,turnInit=-1,unclearable=True,description="Réduit les soins reçus de **10%**",type=TYPE_MALUS)

tmpBalancingDict = {
    "Ly":areaDmgReductionTmp,
    "Lena":areaDmgReductionTmp,
    "Iliana":healReductionTmp,
    "Hélène":healReductionTmp,
    "Julie":healReductionTmp,
    "Edelweiss":armorReductionTmp,
    "Icealia":armorReductionTmp,
    "Ruby":areaDmgReductionTmp,
    "Altikia":healReductionTmp,
    "Bénédicte":areaDmgReductionTmp,
    "Gwendoline":healReciveReductionTmp,
    "Hina":areaDmgReductionTmp,
    "Powehi":armorReductionTmp,
}
