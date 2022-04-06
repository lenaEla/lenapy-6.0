import discord, sqlite3, os
from gestion import *
from advance_gestion import *

maj17="""
    PRAGMA foreign_keys = 0;

    CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                            FROM achivements;

    DROP TABLE achivements;

    CREATE TABLE achivements (
        id              INTEGER PRIMARY KEY
                                UNIQUE,
        aliceCount      INTEGER DEFAULT (0),
        aliceHave       BOOLEAN DEFAULT (0),
        clemenceCount   INTEGER DEFAULT (0),
        clemenceHave    BOOLEAN DEFAULT (0),
        akiraCount      INTEGER DEFAULT (0),
        akiraHave       BOOLEAN DEFAULT (0),
        fightCount      INTEGER DEFAULT (0),
        fightHave       BOOLEAN DEFAULT (0),
        gwenCount       INTEGER DEFAULT (0),
        gwenHave        BOOLEAN DEFAULT (0),
        quickFightCount INTEGER DEFAULT (0),
        quickFightHave  BOOLEAN DEFAULT (0),
        heleneCount     INTEGER DEFAULT (0),
        heleneHave      BOOLEAN DEFAULT (0),
        schoolCount     INTEGER DEFAULT (0),
        schoolHave      BOOLEAN DEFAULT (0),
        elementalCount  INTEGER DEFAULT (0),
        elementalHave   BOOLEAN DEFAULT (0),
        notHealButCount INTEGER DEFAULT (0),
        notHealButHave  BOOLEAN DEFAULT (0),
        greatHealCount  INTEGER DEFAULT (0),
        greatHealHave   BOOLEAN DEFAULT (0),
        greatDpsCount   INTEGER DEFAULT (0),
        greatDpsHave    BOOLEAN DEFAULT (0),
        poisonCount     INTEGER DEFAULT (0),
        poisonHave      BOOLEAN DEFAULT (0),
        iceaCount       INTEGER DEFAULT (0),
        iceaHave        BOOLEAN DEFAULT (0),
        sramCount       INTEGER DEFAULT (0),
        sramHave        BOOLEAN DEFAULT (0),
        estialbaCount   INTEGER DEFAULT (0),
        estialbaHave    BOOLEAN DEFAULT (0),
        lesathCount     INTEGER DEFAULT (0),
        lesathHave      BOOLEAN DEFAULT (0),
        powehiCount     INTEGER DEFAULT (0),
        powehiHave      BOOLEAN DEFAULT (0),
        dimentioCount   INTEGER DEFAULT (0),
        dimentioHave    BOOLEAN DEFAULT (0),
        feliCount       INTEGER DEFAULT (0),
        feliHave        BOOLEAN DEFAULT (0),
        sixtineCount    INTEGER DEFAULT (0),
        sixtineHave     BOOLEAN DEFAULT (0),
        hinaCount       INTEGER DEFAULT (0),
        hinaHave        BOOLEAN DEFAULT (0),
        lunaCount       INTEGER DEFAULT (0),
        lunaHave        BOOLEAN DEFAULT (0),
        julieCount      INTEGER DEFAULT (0),
        julieHave       BOOLEAN DEFAULT (0),
        clemMemCount    INTEGER DEFAULT (0),
        clemMemHave     BOOLEAN DEFAULT (0),
        krysCount       INTEGER DEFAULT (0),
        krysHave        BOOLEAN DEFAULT (0),
        liuHave         BOOLEAN DEFAULT (0),
        liuCount        INTEGER DEFAULT (0),
        liaHave         BOOLEAN DEFAULT (0),
        liaCount        INTEGER DEFAULT (0),
        lioHave         BOOLEAN DEFAULT (0),
        lioCount        INTEGER DEFAULT (0),
        lizHave         BOOLEAN DEFAULT (0),
        LizCount        INTEGER DEFAULT (0),
        ailillHave      BOOLEAN DEFAULT (0),
        ailillCount     INTEGER DEFAULT (0),
        lightNShadowHave      BOOLEAN DEFAULT (0),
        lightNShadowCount     INTEGER DEFAULT (0),
        fullDarkHave      BOOLEAN DEFAULT (0),
        fullDarkCount     INTEGER DEFAULT (0),
        fratereHave      BOOLEAN DEFAULT (0),
        fratereCount     INTEGER DEFAULT (0),
        lightHave     INTEGER DEFAULT (0),
        lightCount     INTEGER DEFAULT (0),
        dangerousHave     INTEGER DEFAULT (0),
        dangerousCount     INTEGER DEFAULT (0),
        looseHave     INTEGER DEFAULT (0),
        looseCount     INTEGER DEFAULT (0),
        stillHave     INTEGER DEFAULT (0),
        stillCount     INTEGER DEFAULT (0),
        dirtyHave     INTEGER DEFAULT (0),
        dirtyCount     INTEGER DEFAULT (0),
        delegationHave     INTEGER DEFAULT (0),
        delegationCount     INTEGER DEFAULT (0),
        stellaHave     INTEGER DEFAULT (0),
        stellaCount     INTEGER DEFAULT (0)
    );

    INSERT INTO achivements (
                                id,
                                aliceCount,
                                aliceHave,
                                clemenceCount,
                                clemenceHave,
                                akiraCount,
                                akiraHave,
                                fightCount,
                                fightHave,
                                gwenCount,
                                gwenHave,
                                quickFightCount,
                                quickFightHave,
                                heleneCount,
                                heleneHave,
                                schoolCount,
                                schoolHave,
                                elementalCount,
                                elementalHave,
                                notHealButCount,
                                notHealButHave,
                                greatHealCount,
                                greatHealHave,
                                greatDpsCount,
                                greatDpsHave,
                                poisonCount,
                                poisonHave,
                                iceaCount,
                                iceaHave,
                                sramCount,
                                sramHave,
                                estialbaCount,
                                estialbaHave,
                                lesathCount,
                                lesathHave,
                                powehiCount,
                                powehiHave,
                                dimentioCount,
                                dimentioHave,
                                feliCount,
                                feliHave,
                                sixtineCount,
                                sixtineHave,
                                hinaCount,
                                hinaHave,
                                lunaCount,
                                lunaHave,
                                julieCount,
                                julieHave,
                                clemMemCount,
                                clemMemHave,
                                krysCount,
                                krysHave,
                                liuHave,
                                liuCount,
                                liaHave,
                                liaCount,
                                lioHave,
                                lioCount,
                                lizHave,
                                LizCount,
                                ailillHave,
                                ailillCount,
                                lightNShadowHave,
                                lightNShadowCount,
                                fullDarkHave,
                                fullDarkCount,
                                fratereHave,
                                fratereCount,
                                lightHave,
                                lightCount,
                                dangerousHave,
                                dangerousCount,
                                looseHave,
                                looseCount,
                                stillHave,
                                stillCount,
                                dirtyHave,
                                dirtyCount,
                                delegationHave,
                                delegationCount
                            )
                            SELECT id,
                                aliceCount,
                                aliceHave,
                                clemenceCount,
                                clemenceHave,
                                akiraCount,
                                akiraHave,
                                fightCount,
                                fightHave,
                                gwenCount,
                                gwenHave,
                                quickFightCount,
                                quickFightHave,
                                heleneCount,
                                heleneHave,
                                schoolCount,
                                schoolHave,
                                elementalCount,
                                elementalHave,
                                notHealButCount,
                                notHealButHave,
                                greatHealCount,
                                greatHealHave,
                                greatDpsCount,
                                greatDpsHave,
                                poisonCount,
                                poisonHave,
                                iceaCount,
                                iceaHave,
                                sramCount,
                                sramHave,
                                estialbaCount,
                                estialbaHave,
                                lesathCount,
                                lesathHave,
                                powehiCount,
                                powehiHave,
                                dimentioCount,
                                dimentioHave,
                                feliCount,
                                feliHave,
                                sixtineCount,
                                sixtineHave,
                                hinaCount,
                                hinaHave,
                                lunaCount,
                                lunaHave,
                                julieCount,
                                julieHave,
                                clemMemCount,
                                clemMemHave,
                                krysCount,
                                krysHave,
                                liuHave,
                                liuCount,
                                liaHave,
                                liaCount,
                                lioHave,
                                lioCount,
                                lizHave,
                                LizCount,
                                ailillHave,
                                ailillCount,
                                lightNShadowHave,
                                lightNShadowCount,
                                fullDarkHave,
                                fullDarkCount,
                                fratereHave,
                                fratereCount,
                                lightHave,
                                lightCount,
                                dangerousHave,
                                dangerousCount,
                                looseHave,
                                looseCount,
                                stillHave,
                                stillCount,
                                dirtyHave,
                                dirtyCount,
                                delegationHave,
                                delegationCount
                            FROM sqlitestudio_temp_table;

    DROP TABLE sqlitestudio_temp_table;

    PRAGMA foreign_keys = 1;
"""

if not(os.path.exists("./data/database/success.db")):
    temp = open("./data/database/success.db","bw")
    print("Création du fichier \"success.db\"")
    temp.close()

class success:
    """Classe des succès"""
    def __init__(self,name : str,countToSucced : int,code: str,recompense = None,description = "Pas de description",emoji=None):
        self.name:str = name
        self.count:int = 0
        self.code:str = code
        self.countToSucced:int = countToSucced
        self.haveSucced:bool = False
        self.recompense:Union[None,List[str]] = recompense
        self.description:str = description
        self.emoji:str = emoji

        if type(recompense) != list:
            self.recompense = [recompense]

    def toDict(self):
        """Renvoie un dict contenant les informations du succès"""
        rep = {"name":self.name,"count":self.count,"countToSucced":self.countToSucced,"haveSucced":self.haveSucced,"recompense":self.recompense,"description":self.description,"code":self.code}
        return rep

class successTabl:
    def __init__(self):
        self.alice = success("Oubliez pas qu'une rose a des épines",10,"alice",recompense="jz",description="Affrontez ou faites équipe avec Alice {0} fois",emoji='<:alice:908902054959939664>')
        self.clemence = success("La quête de la nuit",10,"clemence",recompense="bg",description="Affrontez ou faites équipe avec Clémence {0} fois",emoji='<:clemence:908902579554111549>')
        self.akira = success("Seconde impression",10,"akira",recompense="bh",description="Affrontez ou faites équipe avec Akira {0} fois",emoji='<:akira:909048455828238347>')
        self.fight = success("L'ivresse du combat",1,"fight",recompense="ys",description="Faire {0} combat manuel",emoji='<:splattershotJR:866367630465433611>')
        self.gwen = success("Une histoire de vangeance",10,"gwen",["ka","kb"],"Affrontez ou faites équipe avec Gwen {0} fois",emoji='<:takoYellow:866459052132532275>')
        self.quickFight = success("Le temps c'est de l'argent",10,"quickFight",None,"Lancez {0} combats rapides",'<:hourglass1:872181651801772052>')
        self.helene = success("Là où mes ailes me porteront",10,"helene","yr","Affrontez ou faites équipe avec Hélène {0} fois",'<:takoWhite:871149576965455933>')
        self.school = success("Je ne veux pas d'écolière pour défendre nos terres",30,"school",None,"Mi Miman tu es habiyée en écolière... Combatti {0} fois !",'<:splattershot:866367647113543730>')
        self.elemental = success("Elémentaire mon cher Watson",1,"elemental","qe","Combattre {0} fois en étant niveau 10 ou plus",'<:neutral:887847377917050930>')
        self.notHealBut = success("Situation désespérée Mesure désespérée",500,"notHealBut",None,"Sans être Altruiste, Idole ou Erudit, soignez un total de {0} PV",'<:bandage:873542442484396073>')
        self.greatHeal = success("Soigneur de compétiton",5000,"greatHeal",["kc","kd"],"Soignez un total de {0} PV",'<:seringue:887402558665142343>')
        self.greatDps = success("La meilleure défense c'est l'attaque",5000,"greatDps",None,"Infligez un total de {0} dégâts directs",'<:splatcharger:866367658752213024>')
        self.poison = success("Notre pire ennemi, c'est nous même",5000,"poison",None,"Infligez un total de {0} dégâts indirects",'<:butterflyV:883627142615805962>')
        self.icealia = success("Prévoir l'imprévisible",10,"icea","vn","Faite équipe ou affrontez {0} fois Icealia",'<:takoLBlue:866459095875190804>')
        self.shehisa = success("Pas vue, pas prise",10,"sram","vq","Faite équipe ou affrontez {0} fois Shehisa",'<:ikaPurple:866459331254550558>')
        self.heriteEstialba = success("Savoir utiliser ses atouts",25000,"estialba",'vk',"Infligez {0} dégâts indirects à l'aide de l'effet \"__<:est:884223390804766740> Poison d'Estialba__\"","<:lohica:919863918166417448>")
        self.heriteLesath = success("Il faut que ça sorte",25000,"lesath",'vj',"Infligez {0} dégâts indirects à l'aide de l'effet \"__<:ble:887743186095730708> Hémorragie__\"","<:dissimulation:900083085708771349>")
        self.powehi = success("La fin de tout, et renouvellement",10,"powehi","uj","Affrontez ou faites équipe avec Powehi {0} fois","<:powehi:909048473666596905>")
        self.dimentio = success("Le secret de l'imperceptible",1,"dimentio","qh","Combattre {0} fois en étant niveau 20 ou plus","<:krysTal2:907638077307097088>")
        self.feli = success("Ne jamais abandonner",10,"feli","tl","Affrontez ou faites équipe avec Félicité {0} fois","<:felicite:909048027644317706>")
        self.sixtine = success("Tomber dans les bras de Morphée",10,"sixtine","tk","Affrontez ou faites équipe avec Sixtine {0} fois","<:sixtine:908819887059763261>")
        self.hina = success("Voler à la recousse",10,"hina","tj","Affrontez ou faites équipe avec Hina {0} fois","<:hina:908820821185810454>")
        self.luna = success("La prêtresse obsitnée",3,"luna",description="Vainquez {0} le boss \"Luna\"",emoji="<:luna:909047362868105227>",recompense=["oq","or","os","ot","ou","ov"])
        self.julie = success("Être dans les temps",10,"julie","ti","Affrontez ou faites équipe avec Julie {0} fois","<:julie:910185448951906325>")
        self.memClem = success("La Chauve-Souris Archaniste et la Rose",3,"clemMem","sv","Combattez Clémence Possédée {0} fois","<a:clemPos:914709222116175922><a:aliceExalte:914782398451953685>")
        self.krys = success("Cris \"Staline\" !",10,"krys","st","Affrontez ou faites équipe avec Krys {0} fois","<:krys:916118008991215726>")
        self.liu = success("Tochi no ai",10,"liu",description="Combattez Liu {0} fois",emoji='<:earthKitsune:917670882586017792>',recompense='zzc')
        self.lia = success("Kaze no ai",10,"lia",description="Combattez Lia {0} fois",emoji='<:airKitsune:917670912646602823>',recompense='zzb')
        self.lio = success("Mizu no ai",10,"lio",description="Combattez Lio {0} fois",emoji='<:waterKitsune:917670866626707516>',recompense='zza')
        self.liz = success("Hi no ai",10,"liz",description="Combattez Liz {0} fois",emoji='<:fireKitsune:917670925904785408>',recompense='zyz')
        self.head = success("À en perdre la tête",1,"ailill",description="???",emoji='<:blocked:897631107602841600>')
        self.lightNShadow = success("L'Ombre et la Lumière",1,"lightNShadow",description="Affrontez ou faites équipe avec simultanément Iliana et Luna (ou Shihu)",emoji="<:Iliana:926425844056985640><:luna:909047362868105227>")
        self.fullDarkness = success("Ténèbres Éternels",5,"fullDark",description="Affrontez ou faites équipe Luna ou Shihu {0} fois",emoji='<:luna:909047362868105227><:shihu:909047672541945927>',recompense="cw")
        self.fraticide = success("Feu allié",1,"fratere",description="???",emoji='<a:meeting2:760186427119501312><a:meeting1:760186398401232916>')
        self.fullLight = success("Lumière Éternelle",25,"light",description="Faite équipe ou combattez Iliana {0} fois",emoji='<:Iliana:926425844056985640>',recompense='cx')
        self.dangerousFight = success("Jeu dangereux",1,"dangerous",description="Gagner un combat en ayant 80% de résistance soins ou plus",emoji='<:healnt:903595333949464607>')
        self.loosing = success("Toucher le fond",1,"loose",description="Perdre un combat avec le plus faible taux de danger possible")
        self.still = success("You win by doing absolutly nothing",1,"still",description="Gagner un combat en passant tous vos tours",recompense='hga')
        self.dirty = success("Main propre",5,"dirty",description="Gagner {0} combats en étant dans les 3 meilleurs DPT sans infliger de dégâts directs")
        self.delegation = success("Laisser le sale boulot aux autres",1,"delegation",description="Terminer un combat en atant meilleur DPT mais en ayant réalisé aucune élimination")
        self.stella = success("Puissance solaire",10,"stella","srb",description="Affronter Stella {0} fois")

    def tablAllSuccess(self):
        """Renvoie un tableau avec tous les objets success"""
        return [self.alice,self.clemence,self.akira,self.fight,self.gwen,self.quickFight,self.helene,self.school,self.elemental,self.notHealBut,self.greatHeal,self.greatDps,self.poison,self.icealia,self.shehisa,self.heriteEstialba,self.heriteLesath,self.powehi,self.dimentio,self.feli,self.sixtine,self.hina,self.luna,self.julie,self.memClem,self.krys,self.liz,self.lio,self.lia,self.liu,self.head,self.lightNShadow,self.fullDarkness,self.fraticide,self.fullLight,self.dangerousFight,self.loosing,self.still,self.dirty,self.delegation,self.stella]

    def where(self,where : str):
        alls = self.tablAllSuccess()
        for a in range(0,len(alls)):
            if where == alls[a].code:
                return alls[a]

        raise AttributeError("\"{0}\" not found".format(where))

    def changeCount(self,where : str,count,haveSucced):
        where = self.where(where)
        where.count = count
        where.haveSucced = haveSucced

    async def addCount(self,ctx,user,where : str,add = 1):
        where = self.where(where)
        where.count += add

        if where.count >= where.countToSucced and not(where.haveSucced):
            desti = "Vous avez "
            if int(user.owner) != int(ctx.author.id) :
                desti = user.name + " a "
            embed = discord.Embed(title=where.name,color=user.color,description=desti+"terminé le succès {0} !".format(where.name))

            recompenseMsg = ""
            if where.recompense != [None]:
                for a in where.recompense:
                    what = whatIsThat(a)
                    if what == 0:
                        recompense = findWeapon(a)
                        if recompense == None:
                            print("L'arme {0} n'a pas été trouvée".format(a))
                        elif user.have(recompense):
                            print("{0} possède déjà {1}".format(user.name,recompense.name))
                        else:
                            user.weaponInventory.append(recompense)
                            recompenseMsg += "{0} {1}\n".format(recompense.emoji,recompense.name)
                    elif what == 1:
                        recompense = findSkill(a)
                        if recompense == None:
                            print("La compétence {0} n'a pas été trouvée".format(a))
                        elif user.have(recompense):
                            print("{0} possède déjà {1}".format(user.name,recompense.name))
                        else:
                            user.skillInventory.append(recompense)
                            recompenseMsg += "{0} {1}\n".format(recompense.emoji,recompense.name)
                    elif what == 2:
                        recompense = findStuff(a)
                        if recompense == None:
                            print("L'aéquipement {0} n'a pas été trouvée".format(a))
                        elif user.have(recompense):
                            print("{0} possède déjà {1}".format(user.name,recompense.name))
                        else:
                            user.stuffInventory.append(recompense)
                            recompenseMsg += "{0} {1}\n".format(recompense.emoji,recompense.name)
                    elif what == 3:
                        recompense = findOther(a)
                        if recompense == None:
                            print("L'équipement {0} n'a pas été trouvée".format(a))
                        elif user.have(recompense):
                            print("{0} possède déjà {1}".format(user.name,recompense.name))
                            user.currencies += recompense.price
                            recompenseMsg += "{0} <:coins:862425847523704832>\n".format(recompense.price)
                        else:
                            user.otherInventory.append(recompense)
                            recompenseMsg += "{0} {1}\n".format(recompense.emoji,recompense.name)

            if recompenseMsg != "":
                pluriel = ""
                pluriel2 = "'"
                if len(where.recompense) > 1:
                    pluriel = "s"
                    pluriel2 = "es "
                embed.add_field(name=desti + "obtenu l{1}objet{0} suivant{0} :".format(pluriel,pluriel2),value=recompenseMsg)

            await ctx.channel.send(embed=embed)
            where.haveSucced = True

        achivement.updateSuccess(user,where)
        return user

class succesDb:
    def __init__(self, database : str):
        self.con = sqlite3.connect(f"./data/database/{database}")
        self.con.row_factory = sqlite3.Row
        self.database = database

        cursor = self.con.cursor()

        try:
            cursor.execute("SELECT stellaCount FROM achivements;")
        except:
            temp = ""
            for a in maj17:
                if a != ";":
                    temp+=a
                else:
                    cursor.execute(temp)
                    temp = ""

            self.con.commit()
            print("maj17 réalisée")

        # Fin des majs
        cursor.close()

    def getSuccess(self,user):
        cursor = self.con.cursor()

        # Vérification de si l'utilisateur est dans la base de donée :
        cursor.execute("SELECT * FROM achivements WHERE id = ?",(int(user.owner),))
        result = cursor.fetchall()

        if len(result) == 0: # L'utilisateur n'est pas dans la base de donnée
            cursor.execute("INSERT INTO achivements (id) VALUES (?)",(user.owner,))
            self.con.commit()

            cursor.execute("SELECT * FROM achivements WHERE id = ?",(user.owner,))
            result = cursor.fetchall()

        result = result[0]
        achivTabl = successTabl()

        for a in achivTabl.tablAllSuccess():
            b,c = "{0}Count".format(a.code),"{0}Have".format(a.code)
            achivTabl.changeCount(a.code,result[b],result[c])

        return achivTabl

    def updateSuccess(self,user,achivement):
        cursor = self.con.cursor()
        cursor.execute("UPDATE achivements SET {0}Count = ?, {0}Have = ? WHERE id = ?;".format(achivement.code),(achivement.count,achivement.haveSucced,int(user.owner),))
        cursor.close()
        self.con.commit()

achivement = succesDb("success.db")
