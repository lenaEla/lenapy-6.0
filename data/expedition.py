from attr import Attribute
from adv import *

# Parameters :
# tm# : Return the name of teammate number #. The order of the teammates is randomize when starting the commande
# tm#il : Return "il" if the teamate number # is a boy or a non-binary. "elle" if it's a girl
# tm#Il : Return "Il" if the teamate number # is a boy or a non-binary. "Elle" if it's a girl
# tm#e : Return "e" if the teamate number # is a girl. "" else
# tfils : Return "elles" if all the teammates are girls. "ils" else
# tfIls : Return "Elles" if all the teammates are girls. "Ils" else
# tfe : Return "e" il all the teamates are girls. "" else
# su : Return the name of the succesfull teammate
# suil : Return "elle" if the succesfull teammate is a girl. "il" else
# sue : Return "e" if the succesfull teammate is a girl. "" else

# Event involved teamMate ========================================
SOLO_ALL:int = 0            # All teammates tries to resolve the event
SOLO_SOLO:int = 1           # Only one teammate is allowed to try
ALL_TEAM:int = 2            # The event takes all the stats of all the teammates

# Event Wanted ===================================================
STATS = 0               # The chance of winning the event depend of the stats of the teammate
ASPIRATION = 1          # If the teammate have the good aspiration, they have twice chance to succed
SKILL = 2               # If the teammate have a skill in the list, they have twice chance de succed

class expeditionEvent:
    """The class for a expedition event"""
    def __init__(self,name:str,involved:int,wantedType:int,wantedStats:Union[int,List[skill]],wantedValue:int,intro:List[str],success:List[str],failure:List[str],staminaReduceIfSuccess:int,staminaReduceIfFailure:int,lootBonus:int=1,addTemp:Union[str,None]=None):
        self.name, self._involved, self._wantedType, self._wantedStats, self._wantedValue, self.intro, self.success, self.failure, self.staminaReduceIfSuccess, self.staminaReduceIfFailure,self.lootBonus, self.addTemp = name, involved, wantedType, wantedStats, wantedValue, intro, success, failure, staminaReduceIfSuccess, staminaReduceIfFailure,lootBonus,addTemp

    @property
    def involved(self):
        """Solo_all, Solo_solo or Team_All"""
        return self._involved

    @property
    def wantedType(self):
        """Stats, Aspiration or Skill"""
        return self._wantedType

    @property
    def wantedStats(self):
        """
        If wantedType == Stats :\n
        A `int` presenting the selected stats. Can be a `list(int)`
        """
        return self._wantedStats
    
    @property
    def wantedValue(self):
        """
        If wantedType == Stats :\n
        The value expedted for a 100% at lvl 50
        """
        return self._wantedValue

class expedition:
    """The class for the expedition"""
    def __init__(self,name:str,intro:List[str],events:List[expeditionEvent],notAllowed:Union[None,List[str]]=None):
        self.name, self.intro, self.events, self.notAllowed = name, intro, events, notAllowed

listExpedition:List[expedition] = [
    expedition(
        name="Temple en ruines",
        intro=[
            "Après plusieurs dizaines de minutes à marcher vers le soleil levant, **{tm1}** et ses coéquipiers finirent par tomber sur un vieux temple en ruine. La végétation avait sacrément reprit ses droits, les lianes et la mousse ayant recouvert la quasi totalité du bâtiment.\nAprès quelques minutes de délibération, l'équipe décida de que ce serait là qu'elle ferait son expédition et s'engouffra dans les ruines.",
            "Alors qu'ils se demandaient dans quelle direction aller, **{tm4}** informa de reste de l'équipe qu'{tm4il} avait entendu parler d'une rumeur à propos d'un vieu temple en ruine dans les environs de l'auberge où ils séjournaient.\nLa perspective d'une aventure dans un lieu abandonné depuis des siècles envahis par des miriades d'insectes et araignés n'avait pas trop l'air d'enchanter **{tm2}**, mais {tm2il} pris sur {tm2il}-même et le choix fût fait.\n\nTrouver le temple fût plus simple que ce qu'{tfils} avaient éspérés, mais ce n'était pas pour leur déplaire. L'éditfice était caché au fond d'une forêt profonde et {tfils} avaient du pas mal crapahuter pour y arriver, mais maintenant {tfils} étaient là. Après une grande inspiration collective, {tfils} s'engoufrère à l'intérieur des Ruines.",
            "Pendant que **{tm8}** et son équipe explorait une sombre forêt, **{tm5}** se mit à se plaindre qu'{tm5il} commençait sérieusement à avoir envie d'aller au petit coin. L'équipe s'arrêta donc pour faire une pause déjeunée et **{tm5}** prit un peu de distance pour aller faire son affaire pendant que le reste de ses coéquipiers s'occupait de sortir les sandwitchs.\n\nCes derniers eurent cependant la désagrable surprise de l'entendre crier et lorsque **{tm7}** vint voir ce qui se passait, {tm7il} vit que **{tm5}** était passé au travers d'un sol grandement friable et était tombé dans une sorte de couloir. Après avoir appelé le reste de l'équipe, {tfils} désidère d'explorer les ruines qui s'ouvraient à eux..."
        ],
        events=[
            expeditionEvent(
                "Mécanisme endurant",
                SOLO_ALL,STATS,ENDURANCE,350,
                ["Peu de temps après être entré{tfe} dans l'édifice, {tfils} se retrouvèrent fasse à une impasse. Dans le mur se trouvait une sorte de levier, et **{tm1}** esseya de tirer dessus et se rendit compte qu'il opposait une forte résistance. D'autant plus, une sorte de son de mécanisme se fit entendre lorsqu'{tm1il} essaya.\n\n{tm1Il} en conclu qu'il fallait réussir à tirer sur le levier suffisament longtemps pour ouvrir le chemin.","Après plusieurs tours et détours dans ce dédale, {tfils} se retrouvèrent fasse à une impasse. Cependant, **{tm3}** découvrit qu'une pierre du mur semblait pouvoir bouger et tenta d'appuyer dessus.\nLa pierre semblait vouloir retourner d'elle même dans sa position d'origine, mais plus {tm3il} la maintenait poussée, plus les pierres autour semblaient bouger. L'équipe en déduit qu'elle fallait réussir à pousser la pierre suffisament longtemps pour ouvrir le chemin"],
                ["Après plusieurs tentatives, ce fût au final __**{su}**__ qui arrivea à activer le mécanisme suffisament longtemps. Avec plusieurs cliquetis, le mur s'ouvrit, leur révélant un nouveau passage."],
                ["Malgré leurs efforts, personne ne réussi cependant à actionner le mécanisme suffisament longtemps. {tfIls} désidèrent que ça ne servait à rien de s'acharner et rebroussèrent chemin pour essayer de trouver un autre chemin."],
                5,12
            ),
            expeditionEvent(
                "Un bon sens de l'observation",
                SOLO_ALL,STATS,PRECISION,350,
                ["L'équipe marcha un moment dans les ruines. Le lieu était un vrai dédale, et **{tm7}** était passioné{tm7e} par les anciennes gravures qui s'étandait à perte de vue"],
                ["Au bout d'un moment cependant, __**{su}**__ remarqua que l'un des murs ne semblait pas aussi normal que les autre et lorsqu'{suil} en approcha la main, {suil} découvrit qu'il s'agissait en réalité d'une illusion d'optique causé par le manque d'éclairage et qu'il s'agissait en réalité du mur d'un couloir adjacent\n\nAprès avoir porté sa découverte au reste de l'équipe, cette dernière décida de s'y avanturer."],
                ["Cela semblait cependant bien moins interresser **{tm2}**."],
                0,2
            ),
            expeditionEvent("Un combat d'envergure",ALL_TEAM,STATS,[STRENGTH,ENDURANCE,MAGIE,INTELLIGENCE],5000,
                [
                    "En explorant les ruines, l'équipe fini par se retrouver dans une grande salle où {tfils} eurent la surprise de trouver **Alice** qui était assise devant un mur.\nElle semblait avoir l'air abscente, ne les ayant même pas entendu lorsqu'{tfils} la rejoignirent et sursauta quand **{tm7}** lui toucha l'épaule.\n\n{alice} : \"Oh c'est vous... ... Hum... c'est surment pas le moment ou le lieu pour mais hum... j'aurais besoin d'un coup de main...\nPour... certaines raisons, je me suis aventurée dans ces ruines et je me suis faites attaquée par des araignées... Hum... pas des araignées particulières hein... juste... des araignées... normales... et hum... j'ai perdu un de mes rubans qu'elles ont emportées dans leur nid...\"\n\nElle pointa de la tête un petit trou dans le mur.\n\n{alice} : \"Vous... pouvez allez me le récupérer s'il vous plait... j'y tiens beaucoup, à celui-la...\"\n\n**{tm4}** lui fit remarquer qu'{tfils} étaient un peu grand pour rentrer dans le trou\n\n{alice} : \"Oh heu... c'est pas vraiment un problème ça... Je... je peux changer la taille des gens... Je... je pourrais y aller moi-même mais... araignées...\"\n\nL'équipe accepta de l'aider à récupérer son ruban. Alice se releva doucement, prit une inspiration puis ouvrit la main. Plusieurs boules lumineuses sortirèrent se sa paume et allèrent se loger dans la poitrine des membres de l'équipes.\nLorsqu'{tfils} ouvrirent les yeux, {tfils} constatèrent qu'{tfils} ne mesurait qu'une dizaine de centimètres. Alice les prit doucement dans ses mains, leur souhaita bonne chance et les amena à hauteur du trou."
                ],
                [
                    "Après un combat acharné contre des dizaines arachnés, l'équipe réussi à s'en sortir vainqueuse. {tfIls} souflèrent un bon coup puis se mirent à chercher le ruban. Il ne fut pas vraiment compliqué à trouver, car plusieurs cristaux taillés en forme de coeurs ou de chauve-souris reflétant la lumière étaient fixés à ses extrémités. {tfIls} trouvèrent également d'autres objets interressant.\n\nLors qu'{tfils} allèrent à l'extrémité du nid, Alice sourit lorsqu'{tfils} rendirent son ruban qu'elle rattacha dans ses cheveux avant de les faire redescendre sur le plancher des vaches et leur rendre leur taille normale\n\n{alice} : \"Merci, j'aurais surment dû faire une croix dessus si vous étiez pas passé dans le coins ^^' ... Ils n'y avait pas tant d'araignés que ça '-' ? Une c'est déjà trop... Mais bref qu'est-ce que vous faites ici en faite ? Vous êtes en expédition pour l'Escadron ? Vous permettez que vous accompagne ^^ ? J'ai plus rien à faire ici et puis... si jamais il y a d'autres araignées... Hum... N'y pensons pas ^^'\""
                ],
                [
                    "Malgré tous leurs effors, l'équipe ne parvint pas à défaire les multitudes de vagues d'araignés, et dû battre en retraite. Alice était déçu mais elle fit de son mieux pour pas le montrer, elle qui ne pouvait pas faire grand chose en premiers lieux.\nElle les fit descendre du mur et leur rendit leur taille normal, puis décida de les accompagner, puisque ça restera toujours plus utilse que de rester plantée devant un mur à ne rien faire"
                ],
                15,25,3,"Alice"
                )
        ],
        notAllowed=["Alice"]
    )
]
