from classes import *
from constantes import *
from advObjects.advWeapons import *
from advObjects.advSkills import *
from advObjects.advStuffs import *
from advObjects.advInvocs import *
from advObjects.advEffects import *
from advObjects.advAllies import *
from advObjects.npcSkills.npcSkills_raidBoss import *
from advObjects.npcSkills.npcSkills_boss import *

# --------------------------------------------------------- Tabl Unique Ennemis ---------------------------------------------------------
tablUniqueEnnemies = [
    octarien("Octo Bouclier",50,375,20,45,45,20,10,50,0,0,octoShieldWeap,5,'<:OctoShield:881587820530139136>',[octaStrans,blindage,octoShieldIsolation,shieldBubble,None,None,octoShieldSkill1],team=NPC_OCTARIAN,description="Un octarien qui se cache derrière un gros et lourd bouclier",number=2,aspiration=MASCOTTE),
    octarien("Octo Tireur",150,55,50,95,155,35,0,20,0,20,octoBallWeap,3,'<:octoshooter:880151608791539742>',[chargeShot,ultraShot,None,None,None,octoShotProtectSkill],team=NPC_OCTARIAN,description="Un tireur sans plus ni moins",number=3,aspiration=OBSERVATEUR),
    octarien("Octo Soigneur",30,100,250,35,15,50,50,25,0,0,octoHeal,4,"<:octohealer:880151652710092901>",[octoHealSkill1,octoHealSkill2,firstheal],team=NPC_OCTARIAN,aspiration=ALTRUISTE,description="Un octarien qui se spcésialise dans ~~passer son tour~~ soigner ses alliés",number=3),
    octarien("Rudinn",175,100,20,55,100,35,35,35,0,15,ruddinweap,6,"<a:rudinn:893246033226760232>",skill=[ultraShot],aspiration=TETE_BRULE,deadIcon='<:defeatrudeen:893246353415757824>',baseLvl=10,number=3),
    octarien("Rudinn Ranger",175,175,20,30,30,125,25,35,0,15,ruddinweap2,8,"<a:rudinnRanger:893248570742956072>",aspiration=POIDS_PLUME,deadIcon='<:defeatrudeen:893246353415757824>',skill=[octaStrans],baseLvl=10,number=3),
    octarien("Aéro-benne",200,50,50,60,150,35,20,20,0,0,flyfishweap,7,'<:flyFish:1034364608070291457>',description="Un Salmioche qui s'est passionné pour l'aviation",skill=[flyFishSkill],team=NPC_SALMON,deadIcon='<:salmonnt:894551663950573639>',aspiration=OBSERVATEUR,baseLvl=10,number=2,canMove=False),
    octarien("Mallus",25,30,20,20,25,200,200,20,0,15,malusWeapon,6,'<:mallus:895824636716130308>',skill=[malusSkill1,malusSkill2,zoneOctoInkRes,malusSkill3],aspiration=INOVATEUR,baseLvl=15,number=2),
    octarien("Kralamour",10,50,250,50,0,200,30,30,0,0,kralamWeap,5,'<:kralamour:895443866189176842>',[kralamSkill,kralamSkill2,zoneOctoInkRes,kralamSkill3, None, protectiveArmor, kralamSkill4],PREVOYANT,baseLvl=15,number=2),
    octarien("Temmie",55,100,55,50,35,30,175,30,15,15,temWeap,4,'<:temmie:894546348324552724>',[temSkill1],deadIcon='<:temmient:894545999996014663>',aspiration=TETE_BRULE,say=temSays,baseLvl=15,number=3),
    octarien("Bob",55,100,55,50,35,30,200,30,15,15,temWeap,4,'<:temmie:894546348324552724>',[temSkill1],deadIcon='<:temmient:894545999996014663>',aspiration=TETE_BRULE,say=bobSays,baseLvl=15),
    octarien("Octo Mage",50,100,30,30,30,20,250,20,10,15,octoMageWeap,5,'<:octomage:897910662758543422>',[flame,courant,rock,storm2,None,None,maitriseElementaire],MAGE,team=NPC_OCTARIAN,baseLvl=20,number=3,element=ELEMENT_UNIVERSALIS_PREMO),
    octarien("Octo Mage II",50,100,30,30,30,20,250,20,10,15,octoMageWeap,5,'<:octoMage2:907712297013751838>',[fireCircle,waterCircle,earthCircle,airCircle,None,None,maitriseElementaire],MAGE,team=NPC_OCTARIAN,baseLvl=20,number=3,element=ELEMENT_UNIVERSALIS_PREMO),
    octarien("Zombie",175,200,0,50,70,0,0,50,0,10,ironSword,6,'<:armoredZombie:899993449443491860>',[defi,zombieSkill,zombieSkill2,None,None,None,zombieUndead],BERSERK,baseLvl=20,number=2,rez=False,team=NPC_UNDEAD),
    octarien("Octo Bombardier",225,125,20,10,150,35,0,35,20,0,octobomberWeap,6,'<:octobomber:902013837123919924>',aspiration=OBSERVATEUR,baseLvl=20,number=2,team=NPC_OCTARIAN,skill=[octoTentaMissiles,octoBooyahBombCast]),
    octarien("Tentassin",175,125,20,35,30,100,20,45,15,20,tentaWeap,6,'<:octoshoter2:902013858602967052>',aspiration=OBSERVATEUR,skill=[octaStrans,ultraShot,None,None,None,octoTentasSkill],baseLvl=15,number=2),
    octarien("Octo Protecteur",0,100,50,50,30,300,20,20,0,0,octoDef,5,"<:octoProtect:883303222255706142>",[inkarmor,zoneOctoInkRes],aspiration=PREVOYANT,team=NPC_OCTARIAN,description="Un octarien qui pense que les boucliers sont la meilleure défense",baseLvl=5),
    octarien("OctoBOUM",120,-30,10,35,20,0,450,-10,0,0,octoBoumWeap,5,'<:octoboom:884810545457418271>',[explosionCast],MAGE,canMove=False,description="Un octarien qui a placé tous ses points dans ses envies pirotechniques",baseLvl=25,rez=False),
    octarien("Octaling",125,50,75,50,50,75,125,25,0,20,splattershotJR,5,'<:Octaling:866461984018137138>',baseLvl=10,description='Les Octalings ont une arme, aspiration, élément et compétences aléatoire définini au début du combat',number=3,trait=[TRAIT_ARACHNOPHOBE]),
    octarien("Octarien Volant",200,45,35,120,75,20,0,25,0,35,octoFly,4,'<:octovolant:880151493171363861>',skill=[None,None,None,ocotFlySkill1,octoFlySkill2],number=3,aspiration=OBSERVATEUR),
    octarien("Octo Soigneur Vétéran",50,50,300,35,40,35,0,25,20,0,veterHealWeap,7,'<:octoHealVet:906302110403010581>',[veterHealSkill1,veterHealSkill2,veterHealSkill3,veterHealSkill4,kralamSkill2],ALTRUISTE,baseLvl=30,number=3,team=NPC_OCTARIAN),
    octarien("Octo Moine",175,125,30,35,75,75,50,30,0,20,mainLibre,5,'<:octoMonk:907723929882337311>',[octoMonkSkill1,octoMonkSkill2,octoMonkSkill3,octoMonkSkill4,maitriseElementaire],BERSERK,baseLvl=15,number=2,element=ELEMENT_UNIVERSALIS_PREMO,team=NPC_OCTARIAN),
    octarien("Octo Scientifique",10,25,120,75,35,250,10,30,0,0,octoBoostWeap,7,"<:octoScience:915054617933541386>",[octoBoostSkill1,octoBoostSkill2,octoBoostSkill3,octoBoostSkill4,zoneOctoInkRes],INOVATEUR,trait=[TRAIT_ARACHNOPHOBE],number=2,team=NPC_OCTARIAN),
    octarien("Octo Sniper",250,30,20,100,120,20,15,15,10,20,octoSnipeWeap,7,'<:octotSniper:873118129398624287>',aspiration=OBSERVATEUR,description="Un octarien qui a passé des années à s'entrainer pour rivaliser avec une inkling qui faisait des ravages conséquents parmis les siens",baseLvl=15,skill=[antiArmorShot,sonarPaf],team=NPC_OCTARIAN),
    octarien("Liu",30,350,80,0,50,80,0,50,0,10,liuWeap,10,'<:liu:908754674449018890>',[liuSkill,liuMontBreaker,liuAoEShieldSkill,liuFurTelCast,liuEarthCircle,liuLB],PROTECTEUR,GENDER_FEMALE,"La plus sportive de sa fratterie\n\nChaque attaque à l'arme des Soeurs Kitsune applique l'état \"Charmé (Ennemi)\" qui diminue légèrement les statistiques de la cible","<:kitsuSisterDead:908756093101015100>",baseLvl=20,say=liuSays,element=ELEMENT_EARTH,elemAffinity=True,splashIcon='<:liu:1079013404804665484>',team=NPC_KITSUNE,trait=[TRAIT_ROCKED]),
    octarien("Lia",10,40,170,250,50,50,0,30,0,0,liaWeap,10,'<:lia:908754741226520656>',[liaPassive, liaWindBite, liaDash, liaLB, liaSillage, liaSkill5],POIDS_PLUME,GENDER_FEMALE,"La plus rapide et agile de sa fraterie\n\nChaque attaque à l'arme des Soeurs Kitsune applique l'état \"Charmé (Ennemi)\" qui diminue légèrement les statistiques de la cible","<:kitsuSisterDead:908756093101015100>",baseLvl=20,say=liaSays,element=ELEMENT_AIR,elemAffinity=True,splashIcon='<:lia:1079017951098847283>',team=NPC_KITSUNE,trait=[TRAIT_ARACHNOPHOBE]),
    octarien("Lio",20,70,250,75,50,35,80,35,0,0,lioWeap,10,'<:lio:908754690769043546>',[lioSkill7,lioRez,lioSkill6,lioLB,misery,lioIndirectHeal],ALTRUISTE,GENDER_FEMALE,"La plus calme et tranquille de sa fraterie\n\nChaque attaque à l'arme des Soeurs Kitsune applique l'état \"Charmé (Ennemi)\" qui diminue légèrement les statistiques de la cible","<:kitsuSisterDead:908756093101015100>",baseLvl=20,say=lioSays,element=ELEMENT_WATER,elemAffinity=True,splashIcon='<:lio:1079030249213394996>',team=NPC_KITSUNE,trait=[TRAIT_ARACHNOPHILE]),
    octarien("Liz",10,55,135,35,20,35,205,35,20,0,lieWeap,10,'<:lie:908754710121574470>',[lizBoomCast,lizQuadBoom,lieSkill,lizDotAoE,lizAoE,lizDespairFire,lizLB],MAGE,GENDER_FEMALE,"La plus impulsive de sa fraterie\n\nChaque attaque à l'arme des Soeurs Kitsune applique l'état \"Charmé (Ennemi)\" qui diminue légèrement les statistiques de la cible","<:kitsuSisterDead:908756093101015100>",baseLvl=20,say=lizSays,element=ELEMENT_FIRE,elemAffinity=True,splashIcon='<:liz:1079024673205014609>',team=NPC_KITSUNE,trait=[TRAIT_ARACHNOPHOBE]),
    octarien("Benjamin Hunter",30,100,100,30,50,250,0,35,20,0,hunterWeap,8,'<a:HunterNo:800841356502237225>',[hunterSkill1,hunterSkill2,hunterSkill3,hunterSkill4],IDOLE,GENDER_MALE,deadIcon='<:AutopsyReport:800839396151656469>',baseLvl=15),
    octarien("Octo Invocateur",135,80,45,75,75,45,135,25,0,0,octoInvocWeap,7,'<:octoSummoner:919862854683873331>',[invocCarbunR,invocCarbE,invocCarbSaphir,invocCarbObsi,invocCarbT],baseLvl=20,team=NPC_OCTARIAN),
    octarien("Citoptère Pal. Cor.",0,200,200,50,50,35,50,45,0,0,clirWeap,8,'<:cliropPal:921910882009759764>',[octaStrans,clirHeal,clirSkill2,renisurection,clirSkill1],VIGILANT,deadIcon='<:cliroOut:921912637103698010>',baseLvl=15,number=2,gender=GENDER_FEMALE),
    octarien("Octaling PomPomGirl",10,70,300,100,45,35,10,20,0,0,octaPomWeapon,7,"<:octaPomPom:921910868097257472>",[octoPomSkill1,octoPomSkill2,octoPomSkill3,octoPomSkill4,zoneOctoInkRes],IDOLE,number=2,gender=GENDER_FEMALE),
    octarien("Citoptère Inf. Cor.",0,50,275,75,100,20,20,35,0,0,clirInfWeap,6,'<:cliroInfirm:921915716435836968>',[clirInfSkill2,clirInfSkill3,renisurection,clirInfSkill1],ALTRUISTE,baseLvl = 15, deadIcon = '<:cliroOut:921912637103698010>',number=2),
    octarien("OctoSUS",200,75,0,35,50,200,0,35,20,0,octoSusWeap,5,'<:octoSus:932220811828412456>',[octoSusSkill1,octoSusSkill2],BERSERK,deadIcon='<:dead:932243831104102450>', baseLvl = 15, number=3),
    octarien("Lueur Aforme",135,150,20,20,50,25,200,50,20,0,unformLightAWeapon,10,'<:aformLight:931881464302284871>',[unformLightASkill1,unformLightASkill2,unformLightASkill3,unformLightASkill4],MASCOTTE,description="Une lueur instable qui cherche à éliminer tous les éléments autre que Lumière de ce monde. Menace pour tout être vivant",deadIcon='<:em:866459463568850954>',rez=False,element=[ELEMENT_LIGHT,ELEMENT_LIGHT],baseLvl=30,number=2,team=NPC_UNFORM),
    octarien("Ombre Aforme",100,150,20,20,50,25,235,50,20,0,unformDarknessAWeapon,10,'<:unformShadow:1059462530046636103>',[unformDarknessASkill1,unformDarknessASkill2,unformDarknessASkill3],ENCHANTEUR,description="Une ombre instable qui cherche à éliminer tous les éléments autre que Ténèbres de ce monde. Menace pour tout être vivant",deadIcon='<:em:866459463568850954>',rez=False,element=[ELEMENT_DARKNESS,ELEMENT_DARKNESS],baseLvl=30,number=2,team=NPC_UNFORM),
    octarien("Espace Aforme",80,100,20,20,100,25,250,30,20,0,unformSpaceWeap,10,'<:spaceInform:1095248758696067112>',[unformSpacePassive,unformSpaceSkill1,unformSpaceSkill2],IDOLE,description="Une distortion dimensionnelle instable qui cherche à éliminer tous les éléments autre que Astral de ce monde. Menace pour tout être vivant",deadIcon='<:em:866459463568850954>',rez=False,element=[ELEMENT_SPACE,ELEMENT_SPACE],baseLvl=30,number=2,team=NPC_UNFORM),
    octarien("Temporalité Aforme",50,80,50,50,80,25,250,30,20,0,unformTimeWeap,10,'<:timeInform:1095248719802273803>',[unformTimeSkill1,unformTimeSkill2,unformTimeSkill3],PREVOYANT,description="Une distortion temporelle instable qui cherche à éliminer tous les éléments autre que Temporel de ce monde. Menace pour tout être vivant",deadIcon='<:em:866459463568850954>',rez=False,element=[ELEMENT_TIME,ELEMENT_TIME],baseLvl=30,number=2,team=NPC_UNFORM),
    octarien("Octo Gazeur",200,70,10,50,35,200,0,35,35,0,octoGazWeap,6,'<:octogazeur:972160938104979516>',[octoGazSkill1,octoGazSkill2,octoGazSkill3],ATTENTIF,baseLvl=10,team=NPC_OCTARIAN,element=ELEMENT_DARKNESS,number=2),
    octarien("Lime Cookie",150,80,150,100,70,20,20,35,0,0,limeWeapon,8,"<a:limeCookieRun:1004092989557186570>",[limeSkill1,limeSkill2,limeSkill3,limeSkill4,limeSkill5,limeSkill6,limeSkill7],MASCOTTE,GENDER_FEMALE,deadIcon="<:limeCookieTripped:1004093087569694790>",baseLvl=5,element=[ELEMENT_SPACE,ELEMENT_AIR]),
    octarien("Imea",0,50,50,35,100,50,300,15,10,10,imeaWeap,10,"<:imea:1116364997073829998>",[imeaSkill1,imeaSkill2,imeaSkill3,imeaSkill4,imeaSkill5],MAGE,GENDER_FEMALE,"La reine de l'ancien royaume des Elfes du Nord. Aujourd'hui, elle parcourt le monde en tant que mercenaire en regrettant son royame disparu dans le Cataclysme","<:spIka:866465882540605470>",baseLvl=25,element=[ELEMENT_WATER,ELEMENT_LIGHT]),
    octarien("Gros Boulet",200,200,0,0,100,50,0,20,20,15,bigShotWeapon,7,"<:bigShot:1034364630233001994>",[bigShotSkill],OBSERVATEUR,GENDER_OTHER,"Un gros salmonoides qui bombarde les positions adverses à bonne distance","<:salmonnt:894551663950573639>",baseLvl=20,number=2,team=NPC_SALMON,canMove=False),
    octarien("Tête de Pneu",200,235,0,0,35,35,0,150,0,0,steelHeadWeap,7,"<:steelHead:1034364546573402113>",[octaStrans,steelHeadSkill1],TETE_BRULE,team=NPC_SALMON,deadIcon="<:salmonnt:894551663950573639>",description="Un gros salmonoïde à la salive explive. Sa résistance diminue fortement lorsqu'un charge son attaque",baseLvl=20,number=2),
    octarien("Sorcière",20,100,25,50,75,135,200,35,10,0,witchWeapon,7,"<:witch:1034363858262949918>",[witchSkill,strengthOfDesepearance,witchPoisonSpell,witchRageSpell,None,None,zombieUndead],SORCELER,GENDER_FEMALE,"Une sorcière ayant étudié la magie noir pour pouvoir ramener temporairement les morts à la vie","<:ghost:894550239204220958>",baseLvl=15,rez=False,number=2,team=NPC_UNDEAD,trait=[TRAIT_ARACHNOPHILE]),
    octarien("Drône Lance-Missiles",350,35,0,35,150,0,0,0,20,20,rocketWeap,7,"<:missLauncher:1051436919646588988>",[rocketSkill1,rocketSkill2],OBSERVATEUR,description="Un drône de la mafia locale",baseLvl=30,number=2),
    octarien("Prétorien Glyphique",250,270,0,20,50,10,0,30,0,0,glyphidWeap,7,"<:glyphidPretorian:1055001044909838397>",[glyphidCritWeakness,glyphidDeathCloudPassif,glyphidSkill1,glyphidSkill2],ATTENTIF,description="Une grosse créature dotté d'un squelette externe résistant",baseLvl=25,rez=False,element=[ELEMENT_EARTH,ELEMENT_DARKNESS],number=2),
    octarien("Marinier Sabreur",225,125,25,50,75,35,0,50,0,0,marSabWeap,5,"<:marSab1:1059519565693993060>",[marSabSkill1,marSabSkill2,marSabSkill3],TETE_BRULE,deadIcon="<:spIka:866465882540605470>",baseLvl=5,number=4,team=NPC_MARINE),
    octarien("Marinier Tireur",225,35,25,50,135,50,0,50,0,0,marGunWeap,5,"<:marGun1:1059519589979017337>",[marGunSkill1,marGunSkill2,marGunSkill3],OBSERVATEUR,deadIcon="<:spIka:866465882540605470>",baseLvl=5,number=3,team=NPC_MARINE),
    octarien("Protecteur Glyphique",50,150,20,50,65,225,0,40,0,0,wardenWeap,7,"<:warden:1061392165999222885>",[wardenSkill1,wardenSkill2,wardenSkill3],PREVOYANT,baseLvl=10,team=NPC_GLYPHIQUE,slowMove=True),
    octarien("Golem des Roches",75,250,0,0,100,150,0,40,0,15,earthGolemWeap,6,"<:earthGolem:1064115566790582312>",[earthGolemSkill1,earthGolemSkill2,earthGolemSkill3],PROTECTEUR,baseLvl=15,number=3,elemAffinity=True,element=[ELEMENT_EARTH,ELEMENT_EARTH],team=NPC_GOLEM,description="Un golem créé par Nacialisla pour aider la nature à reprendre ses droits",trait=[TRAIT_ROCKED]),
    octarien("Golem des Vents",0,150,0,0,75,100,250,40,0,15,airGolemWeap,6,"<:airGolem:1064115625972224090>",[windGolemSkill1,windGolemSkill2,windGolemSkill3],ENCHANTEUR,baseLvl=15,number=3,elemAffinity=True,element=[ELEMENT_AIR,ELEMENT_AIR],team=NPC_GOLEM,description="Un golem créé par Nacialisla pour aider la nature à reprendre ses droits"),
    octarien("Golem des Flammes",0,120,0,0,120,80,275,30,0,15,fireGolemWeapon,6,"<:fireGolem:1064115539166908436>",[fireGolemSkill1,fireGolemSkill2,fireGolemSkill3],MAGE,baseLvl=15,number=2,elemAffinity=True,element=[ELEMENT_FIRE,ELEMENT_FIRE],team=NPC_GOLEM,description="Un golem créé par Nacialisla pour aider la nature à reprendre ses droits"),
    octarien("Golem des Flots",0,100,0,0,120,80,295,30,0,15,waterGolemWeapon,6,"<:waterGolem:1064115595676766248>",[waterGolemSkill1,waterGolemSkill2,waterGolemSkill3],MAGE,baseLvl=15,number=2,elemAffinity=True,element=[ELEMENT_WATER,ELEMENT_WATER],team=NPC_GOLEM,description="Un golem créé par Nacialisla pour aider la nature à reprendre ses droits"),
    octarien("Bandit Surrineur",200,150,0,150,75,20,0,30,15,0,surrinWeap,5,"<:surin:1113685316319072297>",[surrinSkill1,surrinSkill2,surrinSkill3],POIDS_PLUME,description="Un bandit utilisant des surrins qui se dissimule pour prendre ses ennemis par surprise",baseLvl=10,number=3),
    octarien("Bandit Archer",200,70,0,50,200,50,0,30,15,0,bowWeap,5,"<:bow:1113685339400327198>",[bowSkill1,bowSkill2,bowSkill3],ATTENTIF,description="Un bandit utilisant un arc pour empoissonner ses cibles à distance",baseLvl=10,number=3),
    octarien("Ploufion",200,50,80,150,80,50,0,20,10,0,ploufWeap,8,"<:flopper:1034364651670097952>",[ploufSkill,ploufSkill2],OBSERVATEUR,description="Un salmonoïde qui se prend pour un dophin",baseLvl=20,number=2,team=NPC_SALMON,element=[ELEMENT_AIR,ELEMENT_WATER],canMove=False,deadIcon='<:salmonnt:894551663950573639>')

]

# --------------------------------------------------------- Tabl All Ennemis ---------------------------------------------------------
tablAllEnnemies = []
for ennemi in tablUniqueEnnemies:
    cmpt = 0
    while cmpt < ennemi.number:
        tablAllEnnemies.append(ennemi)
        cmpt += 1

# --------------------------------------------------------- Bosses ---------------------------------------------------------

# Tabl Boss ----------------------------------------------------
tablBoss = [
    octarien("[[Spamton Neo](https://deltarune.fandom.com/wiki/Spamton)]",300,200,100,45,45,200,200,30,20,15,spamWeap,80,'<a:spamton:892749040205316138>',skill=[spamSkill1,spamSkill2,spamSkill3,spamSkill4,spamSKill5],description="NOW IT'S YOUR CHANCE TO BE A [Big shot] !",deadIcon='<:spamblocked:892750635315912746>',standAlone=True,say=spamtonSays,element=ELEMENT_DARKNESS),
    octarien("Jevil",400,185,100,60,75,120,120,10,25,15,jevilWeap,80,'<a:CHAOS:762276118224961556>',[chaos,jevilSkill1,jevilSkill2],description="I CAN DO ANYTHING !",deadIcon='<:chaosnt:892857736642064455>',standAlone=True,say=jevilSays,element=ELEMENT_DARKNESS),
    octarien("Séréna",50,200,-50,70,50,50,335,60,0,15,armilame,15,'<:serena:1113686693279711232>',[serenaCloud,serenaSkill,serenaSpe,serenaSkill2,serenaFocal,serenaSkill3,serenaSkill4],SORCELER,GENDER_FEMALE,rez=False,deadIcon='<:flowernt:894550324705120266>',say=serenaSays,team=NPC_MARINE),
    octarien("Luna ex.",500,100,80,185,75,80,50,25,35,5,lunaWeap,80,'<:luna:909047362868105227>',[lunaSpeCast,lunaSkill,lunaSkill5Base,lunaSkill2,lunaSkill4,lunaSkill6,lunaSkill7],POIDS_PLUME,GENDER_FEMALE,lunaDesc,'<:spIka:866465882540605470>',True,say=lunaBossSays,element=ELEMENT_DARKNESS),
    octarien("Tour",0,500,0,0,0,0,0,50,0,0,octoTour,12,'<:tower:905169617163538442>',[octoTourSkill],PROTECTEUR,canMove=False,rez=False,description="Une tour de siège. Tant qu'elle est en vie, tous les dégâts directs reçu par ses alliés lui sont redirigés"),
    octarien("Clémence pos.",100,150,50,100,150,150,480,30,15,-50,clemWeapon,80,'<a:clemPos:914709222116175922>',[clemSkill1,clemSkill2,clemSkill3,clemSkill4,clemSkill5,clemSkill6,clemSkill7],MAGE,GENDER_FEMALE,"Durant l'une de ses aventures, Clémence a commis l'erreur de baisser sa garde, et une entité malveillante en a profiter pour se loger dans son esprit, perturbant sa vision de la réalitée et manipulant ses émotions",standAlone=True,deadIcon='<:clemence:1088483909454536784>',say=clemPosSays,element=ELEMENT_DARKNESS,splashIcon="<:clemencePos:1088483975015698472>",team=NPC_DEMON),
    octarien("The Giant Enemy Spider",280,260,0,80,100,50,280,70,10,20,TGESWeap,80,'<:TGES:917302938785968148>',[TGESSkill1],description="En début de combat, invoque 8 __\"Patte de The Giant Enemy Spider\"__ autour de lui",standAlone=True,team=NPC_SPIDER),
    octarien("Matt",450,150,100,100,100,100,0,35,20,0,mattWeapon,80,'<:matt:922064304793059340>',[mattSkill1,mattSkill2,mattSkill3,mattSkill4],BERSERK,GENDER_MALE,"L'ultime adversaire. Dans les jeux Wii Sports en tous cas",'<:matt:922064304793059340>',True),
    octarien("Kiku",325,100,50,100,100,15,375,15,20,15,kikuWeap,80,'<:kiku:962082466368213043>',[kikuSkill1,kikuSkill2,kikuSkill3,kikuSkill4,kikuSkill5,kikuSkill6],aspiration=MAGE,gender=GENDER_FEMALE,deadIcon ='<:kiku:962082466368213043>',baseLvl=15,rez=False,element=ELEMENT_EARTH,splashArt="https://media.discordapp.net/attachments/640667220124499988/1084973959948288083/Sans_titre_46_20230313063859.png?width=507&height=676",splashIcon="<:kiku:1176581413403906200>",team=NPC_UNDEAD,standAlone=True,description="Une liche féérique soumise à son propre pouvoir"),
    octarien("Akira H.",450,100,80,50,120,100,100,30,0,10,akikiWeap,80,'<:akiraH:1007049315056881704>',[akikiSkill1,akikiSkill2_1_1,akikiSkill2_2,akikiSkill3_1_2,akikiSkill3_2_2,akikiSkill4,akikiEnrage],TETE_BRULE,GENDER_MALE,description="Bah bravo, vous avez réussi à le mettre en colère. Maintenant battez vous pour votre dignité ou fuyez pour votre vie.",deadIcon='<:spTako:866465864399323167>',standAlone=True,baseLvl=15,element=ELEMENT_DARKNESS),
    octarien("Iliana ex.",10,220,350,50,100,100,15,85,35,15,iliExWeapon,80,'<:Iliana:926425844056985640>',[iliExSkill1,iliExSkill2,iliExSkill3,iliExSkill4,iliExSKill5,iliExSkill6],VIGILANT,GENDER_FEMALE,"Voyant que vous aviez du mal à trouver un adveraire à votre taille, Iliana a décidé de se confronter à vous en utilisant 1% de sa vrai puissance",'<:oci:930481536564879370>',True,baseLvl=25,element=[ELEMENT_LIGHT,ELEMENT_LIGHT],say=iliExSay,splashIcon="<:iliEx:1053017742757855293>",team=NPC_HOLY),
    octarien("Stella",0,100,70,80,50,50,275,40,20,20,stellaWeap,15,'<:stella:1116365644263333988>',[stellaSkill5,stellaSkill1,stellaSkill2,stellaSkill3,stellaSkill4,stellaLB],IDOLE,GENDER_FEMALE,"Représentation astrale du Soleil, Stella aime pas qu'on lui fasse de l'ombre et a un léger complexe de supporiorité\nSa seule présence suffit à réchauffer l'ambiance et fait gagner quelques degrés de luminosité",'<:spIka:866465882540605470>',baseLvl=25,element=[ELEMENT_SPACE,ELEMENT_LIGHT],say=stellaSays,team=NPC_HOLY)
]

for en in tablBoss:
    en.baseLvl = 15

tablBossPlus = [unformBoss,
]
# ====================================== Raid Boss ======================================

tablRaidBoss = [
    octarien("Ailill",450,350,0,100,350,50,30,35,30,0,ailillWeap,135,'<a:Ailill:882040705814503434>',[ailillPassive,ailillSkill2,ailillSkill3,ailillSkill4,ailillSkill5,ailillSkill6,ailillSkill7],BERSERK,GENDER_FEMALE,description="Une humaine à qui la vie n'a pas vraiment souris. Du coup elle passe ses nerfs sur les autres.\nEnfin les autres plus faibles qu'elle évidamment. Si c'est le cas, il y a de bonne chance pour votre dernière vision dans ce monde soit de la voir en train de lécher votre sang sur son épée ou bien en train d'essuyer ses semelles sur votre tête",say=ailillSays,standAlone=True,deadIcon='<:aillilKill1:898930720528011314>',splashIcon='<a:ailill:1090859838717837314>'),
    octarien("Kitsune",50,435,500,125,125,350,350,25,35,0,kitsuneWeap,135,'<:kitsune:935552850686255195>',element=ELEMENT_UNIVERSALIS_PREMO,aspiration=MAGE,gender=GENDER_FEMALE,deadIcon='<:kitsuSisterDead:908756093101015100>',standAlone=True,skill=[kitsuneSkill1,kitsuneSkill2,kitsuneSkill3,kitsuneSkill4],say=kitsuneSays,team=NPC_KITSUNE),
    octarien("Nacialisla",450,400,250,100,150,200,450,35,35,10,naciaWeap,150,'<:nacialisla:985933665534103564>',[naciaEarthSkill,naciaFireSkill,naciaAirSkill,naciaWaterSkill,naciaMultiElemSkill,naciaGiant],gender=GENDER_FEMALE,standAlone=True,description="Représentation Astrale de la Terre et de la Vie, Nacialisla a pour habitude et réputation de concerver une position de neutralité dans les conflits\nDu moins c'était jusqu'à qu'elle finisse par admettre que les Humains en avait rien a faire d'elle et de ses autres créations et qu'elle décide de les élimier, même si cela va à contre-sens de tous ses principes",deadIcon="<:spIka:866465882540605470>",baseLvl=35,element=[ELEMENT_UNIVERSALIS_PREMO,ELEMENT_UNIVERSALIS_PREMO],say=naciaSay,splashIcon='<:nacialisla:1052321649346748417>'),
    octarien("Iliana OvL",50,650,200,150,200,100,700,15,20,-100,iliOvlWeapon,250,"<:Iliana:926425844056985640>",[iliOvlSkill1,iliOvlSkill2,iliOvlSkill3,iliOvlSkill4,iliOvlSkill5,iliOvlSkill6,iliOvlSkill7],gender=GENDER_FEMALE,deadIcon="<:ilianaStans:969819202032664596>",standAlone=True,baseLvl=50,element=[ELEMENT_LIGHT,ELEMENT_LIGHT],team=NPC_UNFORM,aspiration=VIGILANT,splashIcon='<:overlightIliana:1139260447703433297>',description="Le fragile équilibre élémentaire d'Iliana rompu, la Lumière en sur-abondance lui a fait perdre tout contrôle d'elle-meme",say=iliOvlSay)
]

for en in tablRaidBoss:
    if en.baseLvl == 1:
        en.baseLvl = 25

# --------------------------------------------------------- FindEnnemi ---------------------------------------------------------
def findEnnemi(name:str) -> Union[octarien,None]:
    """Return the normal ennemi or the boss with the given name\n
    Return ``None`` if not found\n
    
    /!\ Return the original and not a copy"""
    name = name.lower().replace(" ","").replace(".","")
    for a in tablUniqueEnnemies+tablBoss+tablRaidBoss+tablBossPlus:
        if a.name.lower().replace(" ","").replace(".","") == name:
            return a
    return None

def simulEnnemisStats(name:str,lvl=55):
    try:
        ent:octarien = copy.deepcopy(findEnnemi(name))
        ent.changeLevel(lvl)

        baseStats = {STRENGTH:ent.strength,ENDURANCE:ent.endurance,CHARISMA:ent.charisma,AGILITY:ent.agility,PRECISION:ent.precision,INTELLIGENCE:ent.intelligence,MAGIE:ent.magie,RESISTANCE:ent.resistance,PERCING:ent.percing,CRITICAL:ent.critical}
        toPrint = "{0} (lvl {1}) :".format(name,ent.level)
        for statName, statValue in baseStats.items():
            if statName <= CRITICAL:
                toPrint += "\n{0} : {1}".format(allStatsNames[statName],statValue)

        toPrint += "\nPVs estimés : {0}".format(round((90+ent.level*10)*((baseStats[ENDURANCE])/100+1)))

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

charmingPandant.effects, charmingPandant.effectAroundCaster, charmingPandant.url = [charming2],[TYPE_MALUS,AREA_CIRCLE_5,charming], liaLB.url

lio = findEnnemi("Lio")
liz = findEnnemi("Liz")
liu = findEnnemi("Liu")
lia = findEnnemi('Lia')
lio.charSettings["weaponUse"], lio.charSettings["healSkillUse"] = CHARSET_WEAPON_USE_LOW, CHARSET_HEALSKILL_HIGH
lia.color, liu.color, lia.color, lio.color = green,orange,red,blue

tablKit: List[octarien] = (liz,lio,lia,liu)
for kitsune in range(len(tablKit)):
    for cmpt in range(len(tablKit[kitsune].skills)):
        if type(tablKit[kitsune].skills[cmpt]) == skill and tablKit[kitsune].skills[cmpt].condition != [EXCLUSIVE,ELEMENT,kitsune+1]:
            tempSkill = copy.deepcopy(tablKit[kitsune].skills[cmpt])
            tempSkill.condition = [EXCLUSIVE,ELEMENT,kitsune+1]
            tablKit[kitsune].skills[cmpt] = tempSkill

liuLythoReactTabl = [
    "Hé !","Back off !","Mais lache moi la grappe !"
]