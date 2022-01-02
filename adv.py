from classes import *
from advObjects.advWeapons import *
from advObjects.advSkills import *
from advObjects.advStuffs import *
from advObjects.advInvocs import *
from advObjects.advEffects import *
from advObjects.advEnnemies import *
from typing import Union
import copy

poidPlumeEff = effect("Poids Plume","poidCritEff",None,trigger=TRIGGER_END_OF_TURN,silent=True,lvl=0,type=TYPE_UNIQUE,unclearable=True,turnInit=-1,emoji=uniqueEmoji(aspiEmoji[POIDS_PLUME]))
obsEff = effect("Observateur","obsCritEff",None,silent=True,lvl=0,type=TYPE_UNIQUE,unclearable=True,turnInit=-1,emoji=uniqueEmoji(aspiEmoji[OBSERVATEUR]))

hourglassEffects = [hourglass1]

#Other
changeAspi = other("Changement d'aspiration","qa",description="Vous permet de changer d'aspiration",emoji='<:changeaspi:868831004545138718>')
changeAppa = other("Changement d'apparence","qb",description="Vous permet de changeer votre genre, couleur et espèce",emoji='<:changeAppa:872174182773977108>',price=500)
changeName = other("Changement de nom","qc",description="Vous permet de changer le nom de votre personnage",emoji='<:changeName:872174155485810718>',price=500)
restat = other("Rénitialisation des points bonus","qd",description="Vous permet de redistribuer vos points bonus",emoji='<:restats:872174136913461348>',price=500)
elementalCristal = other("Cristal élémentaire","qe",500,description="Ces cristaux vous permettent de changer l'élément de votre personnage dans /inventory element (lvl 10)\n\nCe cristal permet de sélectionner les éléments suivants :\n<:fire:887847475203932261> Feu\n<:water:887847459211079760> Eau\n<:air:887847440932290560> Air\n<:earth:887847425459503114> Terre",emoji="<:krysTal:888070310472073257>")
customColor = other("Couleur personnalisée","qf",500,description="Vous permet de rentrer une couleur personnalisée pour votre personnage",emoji='<:changeColor:892350738322300958>')
seeshell = other("Super Coquillage","None",500,description="Ce coquillage permet de changer son bonus iné dans /inventory bonus (lvl 25)")
blablator = other("Blablator","qg",500,description="Permet de définir des messages que votre personnages dira lors de certains événements",emoji='<:blablator:918073481562816532>')
dimentioCristal = other("Cristal dimentionel",'qh',500,'<:krysTal2:907638077307097088>',"Ces cristaux vous permettent de changer l'élément de votre personnage dans /inventory element (lvl 20)\n\nCe cristal permet de choisir les éléments suivants :\n<:light:887847410141921362> Lumière\n<:darkness:887847395067568128> Ténèbre\n<:astral:907467653147410475> Astral\n<:temporel:907467620930973707> Temporel")
token = other("Jeton de roulette","None",0,'<:jeton:917793426949435402>',"Ce jeton est à utiliser dans la Roulette\nAllez donc faire un tour à /roulette !")
mimique = other("Mimikator","qi",500,"<:mimikator:918073466077446164>","Cet emoji vous permet de changer l'apparance de votre arme ou accessoire sur votre icone de personnage.\n\nPour ce faire, appuyez juste sur le bouton correspondant lorsque vous ouvrez une page d'information d'une arme ou accessoire avec /inventory")

others = [elementalCristal,customColor,changeAspi,changeAppa,changeName,restat,blablator,dimentioCristal,mimique]

clemInnerDark = copy.deepcopy(innerdarkness)
aliceOnStage = copy.deepcopy(onstage)
aliceOnStage.say = "Hé ! Hé ! J'ai une avant première pour vous tous, vous en pensez quoi ?"
lohicaFocal = copy.deepcopy(focal)
lohicaFocal.say = "Vous commencez sérieusement à me tapez sur les nerfs..."

lenaChangeDict = createTpmChangeDict(30,0,[bigMonoLaser2],[tripleMissiles],35)
aliceChangeDict = createTpmChangeDict(1,0,[roses],[rosesMagic],50)

# Specials skills ================================================================================
# Total Kboum
totalAnnilLauch = copy.deepcopy(explosion)

totalAnnilCastEff4 = copy.deepcopy(castExplo)
totalAnnilCastEff4.replica, totalAnnilCastEff4.name = totalAnnilLauch, "Annihilation totale dans 1 tour !"
totalAnnilCastSkill4 = copy.deepcopy(explosionCast)
totalAnnilCastSkill4.effectOnSelf = totalAnnilCastEff4

totalAnnilCastEff3 = copy.deepcopy(castExplo)
totalAnnilCastEff3.replica, totalAnnilCastEff3.name = totalAnnilCastSkill4, "Annihilation totale dans 2 tours !"
totalAnnilCastSkill3 = copy.deepcopy(explosionCast)
totalAnnilCastSkill3.effectOnSelf = totalAnnilCastEff3

totalAnnilCastEff2 = copy.deepcopy(castExplo)
totalAnnilCastEff2.replica, totalAnnilCastEff2.name = totalAnnilCastSkill3, "Annihilation totale dans 3 tours !"
totalAnnilCastSkill2 = copy.deepcopy(explosionCast)
totalAnnilCastSkill2.effectOnSelf = totalAnnilCastEff2

totalAnnilCastEff1 = copy.deepcopy(castExplo)
totalAnnilCastEff1.replica, totalAnnilCastEff1.name = totalAnnilCastSkill2, "Annihilation totale dans 4 tours !"
totalAnnilCastSkill1 = copy.deepcopy(explosionCast)
totalAnnilCastSkill1.effectOnSelf = totalAnnilCastEff1

totalAnnilCastEff0 = copy.deepcopy(castExplo)
totalAnnilCastEff0.replica, totalAnnilCastEff0.name = totalAnnilCastSkill1, "Annihilation totale dans 5 tours !"
totalAnnilCastSkill0 = copy.deepcopy(explosionCast)
totalAnnilCastSkill0.effectOnSelf = totalAnnilCastEff0

totalAnnilLauch.name = totalAnnilCastSkill1.name = totalAnnilCastSkill2.name = totalAnnilCastSkill3.name = totalAnnilCastSkill4.name = totalAnnilCastSkill0.name = "Annihilation totale"
totalAnnilLauch.ultimate = totalAnnilCastSkill1.ultimate = totalAnnilCastSkill2.ultimate = totalAnnilCastSkill3.ultimate = totalAnnilCastSkill4.ultimate = totalAnnilCastSkill0.ultimate = totalAnnilLauch.shareCooldown = totalAnnilCastSkill1.shareCooldown = totalAnnilCastSkill2.shareCooldown = totalAnnilCastSkill3.shareCooldown = totalAnnilCastSkill4.shareCooldown = totalAnnilCastSkill0.shareCooldown = False

BOUMBOUMBOUMBOUMweap = weapon("noneWeap","BoumX4",1,AREA_CIRCLE_1,0,0,0) 


# Alliés temporaires =============================================================================
tablAllAllies = [
    tmpAllie("Lena",1,light_blue,OBSERVATEUR,splatcharger,[amethystEarRings,lightBlueJacket,lightBlueFlats],GENDER_FEMALE,[waterlame,bigMonoLaser2,trans,shot,invocCarbSaphir],"Une inkling qui en a vu des vertes et des pas murs.\nPréfère rester loin de la mêlée et abattre ses ennemis à bonne distance",ELEMENT_WATER,icon='<:lena:909047343876288552>',bonusPoints=[STRENGTH,PRECISION],say=lenaSays,changeDict=lenaChangeDict),
    tmpAllie("Gwendoline",2,yellow,POIDS_PLUME,roller,[anakiMask,FIACNf,blackFlat],GENDER_FEMALE,[defi,splashdown,balayette,airStrike,airlame],"Bien qu'elle essaye de l'éviter, cette jeune femme se retrouve toujours à devoir en venir aux mains pour se débarraser des gros lourds de la première ligne ennemie.\nIl est vrai aussi qu'elle n'est pas toute seule dans sa tête",ELEMENT_AIR,bonusPoints=[STRENGTH,ENDURANCE],icon='<:gweny:906303014665617478>'),
    tmpAllie("Clémence",2,red,MAGE,rapiere,[clemEarRings,clemVeste,clemBoots],GENDER_FEMALE,[propag,focal,focus,poisonus,bleedingTrap],"Clémence est née orpheline, ses parents ayant été tués par des chasseresses d'Arthémis peut après sa naissance.\nElle fût donc élevée par des chauve-souris dans une grotte pendant une bonne partie de son enfance\nCependant, elle rencontra dans un lieu nommé la \"Ville Onirique\", une ville magique accessible via les rêves permettant aux vampires vivants comme mort de s'y retrouver, une jeune vampire majeure du nom de Ruby.\nCette dernière lui apprit les bases de la magie au fils des années, ainsi que celles des sociétés humaines que les chauve-souris pouvaient évidamment pas lui apprendre.\n\nMalgré tout, elle manquait d'amis vampire \"réels\", Ruby habitant à des centaines de kilomètres dans la réalité. Elle alla donc, par une belle soirée d'Haloween, mordre une jeune femme envers laquelle Clémence avait un bon sentiment.\nOn peut dire que sur tous les choix qu'elle a fait, ça allait être celui qui allait être le plus lourd en conséquence, dans de bons comme mauvais thermes.\n\nJe vous en passe et des meilleurs, sinon je vais casser la limite de caractères, mais en grandissant, Clémence a continué son apprentissage de la magie et a décidé de parcourir le monde pour étudier les Anciennes Runes ainsi que pour purifier les artéfacts maudits qui tourmentent les monstres pour éviter qu'ils se fassent chasser par les humains, tel ses parents biologiques",ELEMENT_DARKNESS,icon='<:clemence:908902579554111549>',bonusPoints=[MAGIE,STRENGTH],say=clemSays,deadIcon='<:AliceOut:908756108045332570>'),
    tmpAllie("Alice",1,aliceColor,IDOLE,mic,[batRuban,aliceDress,aliceShoes],GENDER_FEMALE,[invocBat2,vampirisme,renisurection,roses,aliceOnStage],"Alice est la petite dernière des trois sœurs Kohishu, et la seule à être une vampire\n\nDès son plus jeune âge, elle a fortement démontré sa volontée à vouloir être le centre de l'attention, bien que ça ai frustrée sa sœur ainée. En grandissant, cette envie de reconnaissance ne s'est pas vraiment tarie, et a réussi grâce à son charme naturel à devenir rapidement une fille populaire\n\nElle décida de suivre la voie de sa mère et de devenir une chanteuse renommé, c'est ainsi qu'elle participa au concours de jeune talent de son école et réussi à se faire remarquer par une maison de disque qui recherchait de jeunes chanteurs\n\nLorsqu'elle n'est pas retenue par ses obligations, elle aime bien accompagner Félicité et Clémence dans leurs aventures, mais refuse de participer activement aux combats. À la place elle les encourages avec ses chansons légèrement magiques",ELEMENT_LIGHT,icon='<:alice:908902054959939664>',bonusPoints=[CHARISMA,INTELLIGENCE],say=aliceSays,deadIcon='<:AliceOut:908756108045332570>',changeDict=aliceChangeDict),
    tmpAllie("Shushi",1,blue,ENCHANTEUR,airspell,[tankmage3,tankmage2,tankmage1],GENDER_FEMALE,[ferocite,invocCarbT,storm2,storm,suppr],"Jeune inkling pas très douée pour le combat, à la place elle essaye de gagner du temps pour permettre à ses alliés d'éliminer l'équipe adverse",ELEMENT_AIR,icon='<:shushi:909047653524963328>',bonusPoints=[MAGIE,ENDURANCE],say=shushiSays),
    tmpAllie("Lohica",1,purple,MAGE,butterflyP,[old,robeLoliBlue,blueFlat],GENDER_FEMALE,[lohicaFocal,poisonus,heriteEstialba,poisonusPuit,propag],"Une fée à l'histoire bien mouvementée. Spécialisée dans les poisons",ELEMENT_DARKNESS,bonusPoints=[MAGIE,STRENGTH],icon='<:lohica:919863918166417448>',deadIcon='<:flowernt:894550324705120266>'),
    tmpAllie("Hélène",2,white,ALTRUISTE,serringue,[barrette,heleneDress,heleneShoe],GENDER_FEMALE,[cure,lapSkill,renisurection,eting,lightBigHealArea],"Une fée qui estime qu'essayer de sauver la vie de ses alliés est plus efficace que si elle esseyait de terminer le combat elle-même",ELEMENT_LIGHT,bonusPoints=[CHARISMA,INTELLIGENCE],icon='<:helene:906303162854543390>'),
    tmpAllie("Félicité",1,red,BERSERK,dtsword,[celestBronzeHat,celestBronzeArmor,celestBronzeBoots],GENDER_FEMALE,[defi,uppercut,strengthOfWillCast,highkick,bloodyStrike],"Soeur ainée de Sixtine et Alice, Félicité est née dans un monde désolé et post apocaliptique\n\n<:lena:909047343876288552> : Mais parle pour toi !\n\nN'ayant plus aucun humain dans ce monde pas si désolé et pas si post apocaliptique, elle hérita de l'âme de Détermination de ce monde (ainsi que quelques bénédictions de dieux grecs mais c'est une autre histoire\n\nEn grandissant, ces dites bénédictions lui ont permis de développer rapidement son esprit et ses capacités, mais aussi d'attirer sur elle tous les monstres mythologiques du coin. Fort heureusement elle pu compter sur ses parents ainsi que sur sa sœur adoptive ainnée Clémence pour la protéger jusqu'au jour où elle en a eu marre de devoir laisser les autres la défendre.\nElle alla donc trouver les seuls autres personnes avec des âmes de Détermination à sa connaissance : Frisk et Chara, qui lui apprirent les bases. Sa volontée ainsi que ses bénédictions lui permirent de rapidement faire des progrès dans l'escrime, quand pour la maîtrise de la magie, c'est grâce à Hécate qu'elle le doit\n\nEn grandissant, elle a choisi une voie plus ou moins similaire à celle de Clémence, c'est à dire de chercher à purifier des artéfacts maudits agitants les monstres alentours ainsi que l'étude d'ancienne magie. Cependant, là où Féli le fait pour protéger les populations d'hommes, Clémence le fait pour protéger les monstres de ces derniers. Mais ça ne les empêche pas de faire équipe de temps en temps. Après tout le but reste le même",bonusPoints=[ENDURANCE,STRENGTH],icon='<:felicite:909048027644317706>'),
    tmpAllie("Akira",2,black,TETE_BRULE,fauc,[anakiMask,heartSphapeObject,hyperlink],GENDER_MALE,[defi,bleedingPuit,highkick,bleedingDague,demolish],"Flora si tu as une description je veux bien",ELEMENT_DARKNESS,bonusPoints=[ENDURANCE,STRENGTH],icon='<:akira:909048455828238347>'),
    tmpAllie("Icealia",2,light_blue,PREVOYANT,blueButterfly,[icealiaHat,icealiaManteau,icealiaBoots],GENDER_FEMALE,[soulagement,inkarmor,kralamSkill,convert,onde],"Une érudite qui préfère protéger ses compagnons",element=ELEMENT_LIGHT,bonusPoints=[INTELLIGENCE,ENDURANCE],icon='<:icealia:909065559516250112>'),
    tmpAllie("Powehi",2,black,PROTECTEUR,inkbrella2,[starBar,bhPull,bhBoots],GENDER_FEMALE,[blackHole,trans,blindage,cosmicPower,inkRes2],"Une manifestation cosmique d'un trou noir. Si vous vous sentez attiré par elle, c'est probablement à raison\nNe lui demandez pas de vous marchez dessus par contre, si vous voulez un conseil. Elle a beau paraître avoir un petit gabarie, ce n'est pas pour rien qu'elle évite de marcher sur le sol",element=ELEMENT_SPACE,bonusPoints=[ENDURANCE,INTELLIGENCE],icon='<:powehi:909048473666596905>',deadIcon = '<:powehiDisiped:907326521641955399>',say=powehiSays),
    tmpAllie("Shehisa",1,purple,TETE_BRULE,shehisa,[shehisaMask,shehisaBody,shehisaBoots],GENDER_FEMALE,[propag,bleedingDague,bleedingPuit,bleedingTrap,heriteLesath],"Soeur d'Hélène, elle a cependant préférer suivre un chemin beaucoup moins altruiste",element=ELEMENT_NEUTRAL,bonusPoints=[STRENGTH,ENDURANCE],icon='<:shehisa:919863933320454165>'),
    tmpAllie("Rasalhague",1,light_blue,MAGE,spellBook,[lentille,chemB,mocas],GENDER_MALE,[space1,space2,space3,spaceSp],element=ELEMENT_SPACE,icon='<:rasalhague:907689992745271376>',bonusPoints=[MAGIE]),
    tmpAllie("Sixtine",1,blue,IDOLE,lightSpellBook,[blueNoeud,pullHeart,heartBask],icon='<:sixtine:908819887059763261>',skill=[bpotion,affaiblissement,nostalgia,provo,sixtineUlt],gender=GENDER_FEMALE,element=ELEMENT_NEUTRAL,bonusPoints=[INTELLIGENCE,ENDURANCE],description="Soeur cadette, Sixtine est plutôt du genre à vouloir rester dans son coin sans être dérangée\n\nElle ne se démarque pas particulièrement de Félicité ou Alice, mais ça ne la dérange pas. Elle passe le plus clair de son temps libre à rêvasser, à du mal à faire le premier pas vers les autres et n'a pas vraiment l'air de s'interresser à grand chose\nMais quand elle s'interresse à un truc, elle veux souvent en connaître un maximum de chose dessus.",say=sixtineSays),
    tmpAllie("Hina",1,purple,OBSERVATEUR,plume,[hinaAcc,hinaBody,hinaShoes],GENDER_FEMALE,[multishot,multiMissiles,hinaUlt,airlame,preciseShot],icon='<:hina:908820821185810454>',element=ELEMENT_AIR,bonusPoints=[AGILITY,STRENGTH]),
    tmpAllie("John",2,orange,POIDS_PLUME,airsword,[bandNoir,pullCamo,kanisand],GENDER_MALE,[airlame,airStrike,airlame],description="Un Loup Garou qui a réussi à tomber amoureux de la vampire responsable des pluparts des vas et viens à l'infirmerie du village de sa meute\n\nAprès de multiple tentatives de l'approcher sans grand succès, il a réussi à changer la clémence qu'éprouvait cette dernière à son égars en affection, mais a peur d'essayer de monter dans son estime",icon='<:john:908887592756449311>',bonusPoints=[STRENGTH,AGILITY],say=johnSays),
    tmpAllie("Julie",1,red,ALTRUISTE,julieWeap,[julieHat,julieDress,julieShoes],GENDER_FEMALE,[altOH,infraMedica,julieUlt,timeSp,trans],"La principale (et unique) servante d'une des vampires les plus puissante du pays.\nElle a appris la magie curative à l'aide des nombreux grimoires dans la bibliothèque du manoire, mais il lui arrive souvent de demander de l'aide à Clémence lorsque sa maîtresse (qui ai d'ailleurs la tutrice magique de cette dernière) lui demande de récupérer des organes de monstres.\nElle se sent souvent petite, en compagnie de ces puissantes vampires\n\nDire qu'elle est légèrement inspirée serait un euphémisme. Au moins elle utilise pas de dagues",element=ELEMENT_TIME,bonusPoints=[CHARISMA,INTELLIGENCE],icon="<:julie:910185448951906325>",say=julieSays),
    tmpAllie("Krys",2,purple,TETE_BRULE,krystalFist,[kryscharpe,krysshirt,kryschains],GENDER_OTHER,[defi,krysUlt,earthStrike,mudlame,demolish],"\"Krys Tal (rien à voir avec la chanteuse ou les opticiens) est un cristal (nooon sans blague) ayant gagné une conscience par un procédé mystérieux.\n\nN'étant pas une forme de vie organique, il se nourrit de minéraux qui traînent par-ci par-là, et de l'armure occasionnelle en combat. Il évite habituellement la nourriture organique, mais il ne dira jamais non à un peu de pop-corn, dont il semble avoir une réserve infinie.\n\nExtrêmement sensible à l'eau, mais n'hésitera pas à ingérer le contenu de la première cannette qui traîne.\n\nAvant, il était un peu con, mais ça, c'était av-Ah on m'annonce dans l'oreillette que c'est toujours le cas, my bad.\n\nPas le plus grand fan d'Akira depuis un sombre incident dans un labo.\"",element=ELEMENT_EARTH,icon="<:krys:916118008991215726>",deadIcon='<:krysCan:916117137339322388>',bonusPoints=[ENDURANCE,STRENGTH]),
    tmpAllie("Edelweiss",1,white,PREVOYANT,eternalInkScience,[battleShieldHat,battleShieldUnif,battleShieldShoes],GENDER_FEMALE,[preOS,soulagement,haimaSkill,intelRaise,inkRes],element=ELEMENT_EARTH,icon='<:edelweiss:918451422939451412>',deadIcon="<:flowernt:894550324705120266>",bonusPoints=[INTELLIGENCE,ENDURANCE]),
    tmpAllie("Iliana",1,white,ALTRUISTE,magicSword,[zenithHat,zenithArmor,zenithBoots],GENDER_FEMALE,[ironWillSkill,lightAura2,clemency,lightBigHealArea,invocFee],"Une Neko paladine qui se bat pour faire perdurer la Lumière dans sa dimension\nRelativement timide, elle ne va pas souvent vers les inconnus, mais ça ne l'empêche pas de faire de son mieux pour les tenir en vie tout de même",ELEMENT_LIGHT,icon='<:Iliana:926425844056985640>',bonusPoints=[CHARISMA,ENDURANCE])
]

# Shushi alt spells
shushiSkill1 = skill("Frappe lumineuse","shushiSkill1",TYPE_DAMAGE,0,150,cooldown=3,use=MAGIE,emoji='<a:ShushiLF:900088862871781427>')
shushiSkill3Eff = effect("Jeu de lumière","diff",redirection=35,trigger=TRIGGER_DAMAGE,description="Un habile jeu de lumière permet de vous cacher de vos ennemis")
shushiSkill3 = skill("Diffraction","shushiSkill2",TYPE_ARMOR,0,0,AREA_CIRCLE_6,effect=shushiSkill3Eff,cooldown=5,initCooldown=2,use=None,emoji='<a:diffraction:916260345054658590>')
shushiSkill4Eff = effect("Assimilation","assimil",MAGIE,resistance=10,overhealth=150,description="Grâce à Shihu, vous avez réussi à utiliser les Ténèbres environant à votre avantage",emoji=uniqueEmoji("<:tarmor:909134091604090880>"),type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE)
shushiSkill4 = skill("Assimilation","shushiSkill4",TYPE_ARMOR,0,cooldown=3,effect=shushiSkill4Eff,say='On peut y awiver !',use=MAGIE,emoji='<:assimilation:916260679944634368>')
shushiWeapEff = effect("Lueur Ténébreuse","darkLight",MAGIE,resistance=5,overhealth=50,type=TYPE_ARMOR,emoji=uniqueEmoji('<:dualMagie:899628510463803393>'))
shushiWeap = weapon("Magie trancendante","dualMagie",RANGE_LONG,AREA_DONUT_5,35,100,0,strength=-20,endurance=10,charisma=20,intelligence=20,magie=55,type=TYPE_HEAL,target=ALLIES,use=MAGIE,effectOnUse=shushiWeapEff,affinity=ELEMENT_LIGHT,emoji='<:dualMagie:899628510463803393>')
shushiHat = stuff("Barrête de la cohabitation","dualHat",0,0,strength=-20,endurance=15,charisma=20,agility=10,precision=10,intelligence=20,magie=45,affinity=ELEMENT_LIGHT,emoji='<:coaBar:911659734812229662>')
shushiDress = stuff("Robe de la cohabitation","dualDress",1,0,strength=-10,endurance=35,charisma=20,agility=0,precision=10,intelligence=10,magie=60,resistance=20,affinity=ELEMENT_LIGHT,emoji='<:coaDress:911659797076660294>')
shushiBoots = stuff("Bottines de la cohabitation","dualBoost",2,0,strength=-10,endurance=15,charisma=0,agility=20,precision=10,magie=45,intelligence=10,affinity=ELEMENT_LIGHT,emoji='<:coaBoots:911659778995007528>')
shushiSkill5 = skill("Lumière éternelle","LumEt",TYPE_RESURECTION,0,100,emoji='<:renisurection:873723658315644938>',cooldown=3,description="Permet de ressuciter un allié",use=MAGIE,range=AREA_DONUT_7)
shushiArmorSkillEff = effect("Armure Harmonique","shushiArmor",MAGIE,overhealth=200,turnInit=3,type=TYPE_ARMOR,trigger=TRIGGER_DAMAGE,emoji=uniqueEmoji("<a:transArmorB:900037831257358378>"))
shushiArmorSkill = skill("Armure Harmonique","shushiArmorSkill",TYPE_ARMOR,0,effect=shushiArmorSkillEff,range=AREA_MONO,area=AREA_CIRCLE_5,cooldown=7,use=MAGIE,emoji='<a:transArmorB:900037831257358378>')

shihuDarkBoom1 = copy.deepcopy(explosion)
shihuDarkBoom2 = copy.deepcopy(explosionCast)
shihuDarkBoomEff = copy.deepcopy(castExplo)
shihuDarkBoom1.emoji= '<a:darkExplosion:899451335269822475>'
shihuDarkBoom1.id = "ShihuDarkBoomLaunch"
shihuDarkBoom1.say = "Za va fire Boum Boum !"
shihuDarkBoom1.name, shihuDarkBoom1.repetition, shihuDarkBoom1.power = "Explosion Noire",2,int(explosion.power * 0.45)

shihuDarkBoomEff.replica = shihuDarkBoom1
shihuDarkBoomEff.id = "ShihuDarkBoomEff"
shihuDarkBoom2.effectOnSelf, shihuDarkBoom2.name,shihuDarkBoom2.emoji = shihuDarkBoomEff,"Explosion Noire",'<a:darkExplosion:899451335269822475>'
shihuDarkBoom2.id = "ShihuDarkBoom"

aliceBloodJauge = copy.deepcopy(clemBloodJauge)
aliceBloodJauge.emoji = uniqueEmoji("<:aliceBJ:914798086667264010>")
aliceBloodJauge.description = "Alice exaltée tourne autour de sa Jauge de Sang\n\nElle débute le combat avec une jauge à **100** Points de sang, son maximum.\nChacunes de ses compétences ont un coût en Points de Sang, qui sont retiré à la jauge à la fin de leur utilisation\n\nSi la jauge de sang tombe à **0 point**, Alice est étourdie pendant 2 tours durant lesquels sa résistance est diminuée\nLa jauge de sang récupère **1 point** de sang à chaque fois que Alice soigne 50 points de vie, et **100 points** une fois qu'Alice n'est plus étourdie\n\nLa quantité de points de sang dans la jauge de sang est constamant visible"

aliceExHeadruban = stuff("Ruban vampirique","aliceExHead",0,0,charisma=40,negativeHeal=-50,endurance=55,emoji=batRuban.emoji)
aliceExDress = stuff("Robe vampirique","aliceExDress",1,0,endurance=10,resistance=15,charisma=45,negativeHeal=-25,emoji=aliceDress.emoji)
aliceExShoes = stuff("Ballerines vampiriques","aliceExShoes",2,0,agility=25,charisma=45,negativeHeal=-35,endurance=5,emoji=aliceShoes.emoji)

aliceExWeapEff = effect("Bénédiction vampirique","aliceExWeapEff",CHARISMA,emoji=uniqueEmoji("<:vampire:900312789686571018>"),power=15,type=TYPE_INDIRECT_HEAL,trigger=TRIGGER_AFTER_DAMAGE,description="Cet effect confère **{0}%** de Vol de Vie au porteur.\nLe pourcentage de convertion est augmenté par les statistiques du lanceur")
aliceExWeap = weapon("Rosa receptaculum","aliceExWeap",RANGE_DIST,AREA_CIRCLE_5,25,100,0,use=CHARISMA,charisma=35,resistance=10,type=TYPE_HEAL,target=ALLIES,effectOnUse=aliceExWeapEff,effect=aliceBloodJauge,emoji='<:vampBall:916199488891273276>')
aliceSkill1Eff = effect("Régénération vampirique","aliceRegenEff",CHARISMA,power=15,emoji=uniqueEmoji("<a:aliceSkill1:914787461949960202>"),type=TYPE_INDIRECT_HEAL,turnInit=3,lvl=3,area=AREA_CIRCLE_2,description="Au début du tour du porteur, lui et ses alliés proches recoivent des soins",trigger=TRIGGER_START_OF_TURN)
aliceSkill1 = skill("Sort - Rénégération","aliceSkill1",TYPE_INDIRECT_HEAL,0,0,emoji="<a:aliceSkill1:914787461949960202>",effect=aliceSkill1Eff,cooldown=3)
aliceSkill2Eff = effect("Galvanision vampirique","aliceBoostEff",CHARISMA,strength=12,magie=12,percing=3,emoji=uniqueEmoji('<a:aliceSkill2:914791502931197962>'))
aliceSkill2 = skill("Sort - Galvanisation","aliceSkill2",TYPE_BOOST,0,range=AREA_MONO,area=AREA_DONUT_3,effect=aliceSkill2Eff,cooldown=2,emoji='<a:aliceSkill2:914791502931197962>')
aliceSkill3 = skill("Rune - Flos luminosus","aliceSkill3",TYPE_DAMAGE,0,130,emoji='<a:aliceSkill3:914794172215623690>',cooldown=2,use=CHARISMA)
aliceSkill4 = skill("Rune - Pleine lune","aliceSkill4",TYPE_HEAL,0,120,AREA_MONO,area=AREA_CIRCLE_3,use=CHARISMA,cooldown=3,emoji='<a:aliceSkill4:914796355925458984>')
aliceRez = skill("Memento - Voie de l'Ange II","aliceRez",TYPE_RESURECTION,0,350,range=AREA_CIRCLE_7,emoji="<a:memAlice2:908424319900745768>",use=CHARISMA,description="Si plus de la moitié de l'équipe est morte, la zone d'effet de la compétence deviens un cercle de 7 cases autour de Alice, mais consomme l'intégralité de sa jauge de sang")
aliceRez2 = skill("Memento - Voie de l'Ange III","aliceRez+",TYPE_RESURECTION,0,350,range=AREA_MONO,area=AREA_CIRCLE_7,emoji="<a:memAlice2:908424319900745768>",use=CHARISMA)

tablVarAllies = [ 
    tmpAllie("Luna",1,black,POIDS_PLUME,kcharger,[lunaPandan,lunaDress,lunaBoots],GENDER_FEMALE,[defi,splatbomb,invocCarbObsi,soupledown,highkick],"Là où se trouve la Lumière se trouvent les Ténèbres",ELEMENT_DARKNESS,variant=True,icon='<:luna:909047362868105227>',bonusPoints=[STRENGTH,ENDURANCE],say=lunaSays),
    tmpAllie("Altikia",2,yellow,PROTECTEUR,inkbrella,[crepuHat,crepuArmor,crepuBoots],GENDER_FEMALE,[ironWillSkill,lightAura2,inkarmor,renisurection,concen],"Une personnalité de Gwen qui préfère se concentrer sur ses alliés",ELEMENT_LIGHT,variant=True,bonusPoints=[ENDURANCE,CHARISMA],icon='<:alty:906303048542990347>'),
    tmpAllie("Klironovia",2,yellow,BERSERK,klikliSword,[darkMaidPendants,FIACNf,blackFlat],GENDER_FEMALE,[defi,demolish,bloodyStrike,trans,highkick],"Une personnalité de Gwen bien plus violente que les deux autres",ELEMENT_EARTH,variant=True,bonusPoints=[STRENGTH,AGILITY],icon='<:klikli:906303031837073429>'),
    tmpAllie("Shihu",1,black,MAGE,darkSpellBook,[shihuHat,shihuDress,shihuShoe],GENDER_FEMALE,[dark2,dark3,shihuDarkBoom2,suppr],"\"Eye veut zuste un pi d'attenchions...\" - Shushi",ELEMENT_DARKNESS,variant=True,icon='<:shihu:909047672541945927>',bonusPoints=[MAGIE,STRENGTH],say=shihuSays),
    tmpAllie("Shushi Cohabitée",1,blue,PREVOYANT,shushiWeap,[shushiHat,shushiDress,shushiBoots],GENDER_FEMALE,[shushiSkill1,shushiArmorSkill,shushiSkill3,shushiSkill4,shushiSkill5],"S'étant comprise l'une et l'autre, Shushi et Shihu ont décidé de se liguer contre la mère de cette dernière.\nCette allié temporaire n'apparait que contre le boss \"Luna\"",ELEMENT_LIGHT,True,icon='<:shushiCoa:915488591654842368>',bonusPoints=[MAGIE,AGILITY]),
    tmpAllie("Alice Exaltée",1,aliceColor,IDOLE,aliceExWeap,[aliceExHeadruban,aliceExDress,aliceExShoes],GENDER_FEMALE,[aliceSkill1,aliceSkill2,aliceSkill3,aliceSkill4,aliceRez],"Voyant qu'elle n'arriverai pas à ramener sa sœur à la raison, Alice a décider d'aller contre ses principes et de révéler toute sa puissance vampirique pour tenter de redresser la balance.\nN'apparait que contre Clémence possédée",element=ELEMENT_LIGHT,variant=True,deadIcon="<:AliceOut:908756108045332570>",icon="<a:aliceExalte:914782398451953685>",bonusPoints=[CHARISMA,ENDURANCE],say=aliceExSays)
]

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

def findSkill(skillId) -> skill:
    """Renvoie une compétence Skill, si trouvé"""
    typi = type(skillId)
    if typi == skill:
        return skillId

    elif type(skillId) != str or skillId == "0":
        return None
    else:
        if skillId.startswith("\n"):
            skillId = id.replace("\n","")
        for a in skills:
            if a.id == skillId or a.name.lower() == skillId.lower():
                return a

        #print("ID non trouvée : ",skillId)
        return None

def findStuff(stuffId) -> stuff:
    """Renvoie un équipement Stuff, si trouvé"""
    typi = type(stuffId)
    if typi == stuff:
        return stuffId

    elif type(stuffId) != str:
        return None
    else:
        rep,id = None,stuffId
        if stuffId.startswith("\n"):
            id = id.replace("\n","")
        for a in stuffs:
            if a.id == id or a.name.lower() == id.lower():
                rep = a
                break

        return rep

def findEffect(effectId) -> effect:
    if type(effectId) == effect:
        return effectId
    elif type(effectId) != str:
        
        return None
    else:
        rep,id = None,effectId
        for a in effects:
            if a.id == id or a.name.lower() == id.lower():
                rep = a
                break
    
        return rep

def findOther(otherId : Union[str,other]) -> Union[other,None]:
    if type(otherId) == other:
        return otherId
    else:
        otherId = otherId.replace("\n","")
        for a in others:
            if a.id == otherId or a.name.lower() == otherId.lower():
                if otherId == "qj":
                    print("finded !")
                return a
    print("{0} not finded".format(otherId))
    return None

def findInvoc(name) -> invoc:
    for a in invocTabl:
        if a.name == name:
            return a

    return None

def findAllie(name) -> tmpAllie:
    for a in tablAllAllies+tablVarAllies:
        if a.name == name:
            return a
    return None

if not(isLenapy):
    print("\nVérification de l'équilibrage des stuffs...")
    allstats = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for a in stuffs:
        if a.effect == None or (a.effect != None and findEffect(a.effect).id != summonerMalus.id):
            ballerine = a.allStats()+[a.resistance,a.percing,a.critical]
            babie = [a.negativeHeal,a.negativeBoost,a.negativeShield,a.negativeDirect,a.negativeIndirect]
            sumation = 0
            for b in range(0,len(ballerine)):
                sumation += ballerine[b]
                allstats[b] += ballerine[b]

            for b in babie:
                sumation -= b

            if sumation != 20 and a.effect == None and a.name != "Claquettes chaussettes":
                print("{0} n'a pas le bon cumul de stats : {1}".format(a.name,sumation))

            elif sumation != 10 and a.effect != None:
                print("{0} n'a pas le bon cumul de stats : {1}".format(a.name,sumation))

    temp = "\nDistribution des statistiques :\n"
    total = 0
    for a in allstats:
        total += a

    for a in range(0,len(allStatsNames)):
        temp += "{0} : {1}% ({2})\n".format(allStatsNames[a],round(allstats[a]/total*100,2),allstats[a])
    #print(temp)

    lvlTabl = [{"level":0,"nombre":0}]
    for equip in stuffs:
        find = False
        for temp in lvlTabl:
            if temp["level"] == equip.minLvl:
                temp["nombre"]+=1
                find = True
                break

        if not(find):
            lvlTabl.append({"level":equip.minLvl,"nombre":1})

    lenStuff = len(stuffs)
    lvlTabl.sort(key=lambda ballerine: ballerine["level"])

    for temp in lvlTabl:
        pass
        #print("Objets de niveau {0} : {1} ({2})%, statsAttendues : {3}".format(temp["level"],temp["nombre"],round(temp["nombre"]/lenStuff*100,2),20 + (temp["level"] * 2)))

    tabl = copy.deepcopy(tablAllAllies)
    tablTank = []
    tablMid = []
    tablBack = []

    for allie in tabl:
        [tablTank,tablMid,tablBack][allie.weapon.range].append(allie)

    print("")
    for num in range(3):
        pass
        #print("Nombre de Temp's en {0} : {1}".format(["mêlée","distance","backline"][num],len([tablTank,tablMid,tablBack][num])))

    tabl = copy.deepcopy(tablAllEnnemies)
    alReadySeen = []
    tablTank = []
    tablMid = []
    tablBack = []

    for ennemi in tabl:
        if ennemi.name not in alReadySeen:
            [tablTank,tablMid,tablBack][ennemi.weapon.range].append(ennemi)
            alReadySeen.append(ennemi.name)
            stat = ennemi.allStats()+[ennemi.resistance,ennemi.percing,ennemi.critical]
            summ = 0
            for a in stat:
                summ += a

            awaited = int((230+110*3)*0.9)
            if summ < awaited*0.9 or summ > awaited*1.1:
                print("{0} n'a pas le bon cumul de stats : {1} ({2})".format(ennemi.name,summ,awaited))

    print("")
    for num in range(3):
        #print("Nombre d'ennemis en {0} : {1}".format(["mêlée","distance","backline"][num],len([tablTank,tablMid,tablBack][num])))
        pass

    for weap in weapons:
        summation = 0
        for stats in weap.allStats()+[weap.resistance,weap.percing,weap.critical]:
            if stats < 0:
                print("{0} : Stat négative détectée !".format(weap.name))
            else:
                summation += stats

        toVerif = 30
        if weap.effect != None or weap.effectOnUse != None:
            toVerif = 15

        if int(summation) != int(toVerif):
            print("{0} : Cumule de stats non égal à {1} ({2} / {1})".format(weap.name,toVerif,summation))
    print("\nVérification de l'équilibrage des stuffs terminée")

listAllBuyableShop = []
for a in weapons+skills+stuffs:
    if a.price > 0:
        listAllBuyableShop.append(a)

def userShopPurcent(user : char):
    totalShop = len(listAllBuyableShop)
    tablToSee = listAllBuyableShop[:]
    for a in listAllBuyableShop:
        if user.have(a):
            tablToSee.remove(a)

    return 100-(len(tablToSee)/totalShop*100)

allReadySeen = []
for obj in stuffs+weapons+skills+others:
    if obj.id not in allReadySeen:
        allReadySeen.append(obj.id)
    else:
        what = ""
        for whaty in stuffs+weapons+skills+others:
            if whaty.id == obj.id:
                what += whaty.name + ", "
        raise Exception("Identifiant doublon : {1}".format(obj.name,what))