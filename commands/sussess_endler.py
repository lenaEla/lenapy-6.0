import discord, sqlite3, os
from gestion import *
from advance_gestion import *

createTabl = """
CREATE TABLE achivements (
    id            INTEGER PRIMARY KEY
                          UNIQUE,
    aliceCount    INTEGER,
    aliceHave     BOOLEAN,
    clemenceCount INTEGER,
    clemenceHave  INTEGER,
    akiraCount    INTEGER,
    akiraHave     BOOLEAN
);"""
maj1 = """
    PRAGMA foreign_keys = 0;
    CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                            FROM achivements;
    DROP TABLE achivements;
    CREATE TABLE achivements (
        id            INTEGER PRIMARY KEY
                            UNIQUE,
        aliceCount    INTEGER,
        aliceHave     BOOLEAN,
        clemenceCount INTEGER,
        clemenceHave  INTEGER,
        akiraCount    INTEGER,
        akiraHave     BOOLEAN,
        fightCount    INTEGER,
        fightHave     BOOLEAN
    );
    INSERT INTO achivements (
                                id,
                                aliceCount,
                                aliceHave,
                                clemenceCount,
                                clemenceHave,
                                akiraCount,
                                akiraHave
                            )
                            SELECT id,
                                aliceCount,
                                aliceHave,
                                clemenceCount,
                                clemenceHave,
                                akiraCount,
                                akiraHave
                            FROM sqlitestudio_temp_table;
    DROP TABLE sqlitestudio_temp_table;
    PRAGMA foreign_keys = 1;
"""
maj2 = """PRAGMA foreign_keys = 0;
    CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                            FROM achivements;
    DROP TABLE achivements;
    CREATE TABLE achivements (
        id            INTEGER PRIMARY KEY
                            UNIQUE,
        aliceCount    INTEGER,
        aliceHave     BOOLEAN,
        clemenceCount INTEGER,
        clemenceHave  INTEGER,
        akiraCount    INTEGER,
        akiraHave     BOOLEAN,
        fightCount    INTEGER,
        fightHave     BOOLEAN,
        gwenCount     INTEGER,
        gwenHave      BOOLEAN,
        qfCount       INTEGER,
        qfHave        BOOLEAN
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
                                fightHave
                            )
                            SELECT id,
                                aliceCount,
                                aliceHave,
                                clemenceCount,
                                clemenceHave,
                                akiraCount,
                                akiraHave,
                                fightCount,
                                fightHave
                            FROM sqlitestudio_temp_table;
    DROP TABLE sqlitestudio_temp_table;
    PRAGMA foreign_keys = 1;
"""
maj3 = """
    PRAGMA foreign_keys = 0;
    CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                            FROM achivements;
    DROP TABLE achivements;
    CREATE TABLE achivements (
        id            INTEGER PRIMARY KEY
                            UNIQUE,
        aliceCount    INTEGER,
        aliceHave     BOOLEAN,
        clemenceCount INTEGER,
        clemenceHave  INTEGER,
        akiraCount    INTEGER,
        akiraHave     BOOLEAN,
        fightCount    INTEGER,
        fightHave     BOOLEAN,
        gwenCount     INTEGER,
        gwenHave      BOOLEAN,
        qfCount       INTEGER,
        qfHave        BOOLEAN,
        heleneCount   INTEGER,
        heleneHave    BOOLEAN
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
                                qfCount,
                                qfHave
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
                                qfCount,
                                qfHave
                            FROM sqlitestudio_temp_table;
    DROP TABLE sqlitestudio_temp_table;
    PRAGMA foreign_keys = 1;
"""
maj4="""
    PRAGMA foreign_keys = 0;
    CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                            FROM achivements;
    DROP TABLE achivements;
    CREATE TABLE achivements (
        id            INTEGER PRIMARY KEY
                            UNIQUE,
        aliceCount    INTEGER,
        aliceHave     BOOLEAN,
        clemenceCount INTEGER,
        clemenceHave  INTEGER,
        akiraCount    INTEGER,
        akiraHave     BOOLEAN,
        fightCount    INTEGER,
        fightHave     BOOLEAN,
        gwenCount     INTEGER,
        gwenHave      BOOLEAN,
        qfCount       INTEGER,
        qfHave        BOOLEAN,
        heleneCount   INTEGER,
        heleneHave    BOOLEAN,
        schoolCount   INTEGER,
        schoolHave    BOOLEAN
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
                                qfCount,
                                qfHave,
                                heleneCount,
                                heleneHave
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
                                qfCount,
                                qfHave,
                                heleneCount,
                                heleneHave
                            FROM sqlitestudio_temp_table;
    DROP TABLE sqlitestudio_temp_table;
    PRAGMA foreign_keys = 1;
"""
maj5="""
    PRAGMA foreign_keys = 0;
    CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                            FROM achivements;
    DROP TABLE achivements;
    CREATE TABLE achivements (
        id              INTEGER PRIMARY KEY
                                UNIQUE,
        aliceCount      INTEGER,
        aliceHave       BOOLEAN,
        clemenceCount   INTEGER,
        clemenceHave    INTEGER,
        akiraCount      INTEGER,
        akiraHave       BOOLEAN,
        fightCount      INTEGER,
        fightHave       BOOLEAN,
        gwenCount       INTEGER,
        gwenHave        BOOLEAN,
        quickFightCount INTEGER,
        quickFightHave  BOOLEAN,
        heleneCount     INTEGER,
        heleneHave      BOOLEAN,
        schoolCount     INTEGER,
        schoolHave      BOOLEAN
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
                                schoolHave
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
                                qfCount,
                                qfHave,
                                heleneCount,
                                heleneHave,
                                schoolCount,
                                schoolHave
                            FROM sqlitestudio_temp_table;
    DROP TABLE sqlitestudio_temp_table;
    PRAGMA foreign_keys = 1;
"""
maj6="""
    PRAGMA foreign_keys = 0;
    CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                            FROM achivements;
    DROP TABLE achivements;
    CREATE TABLE achivements (
        id              INTEGER PRIMARY KEY
                                UNIQUE,
        aliceCount      INTEGER,
        aliceHave       BOOLEAN,
        clemenceCount   INTEGER,
        clemenceHave    INTEGER,
        akiraCount      INTEGER,
        akiraHave       BOOLEAN,
        fightCount      INTEGER,
        fightHave       BOOLEAN,
        gwenCount       INTEGER,
        gwenHave        BOOLEAN,
        quickFightCount INTEGER,
        quickFightHave  BOOLEAN,
        heleneCount     INTEGER,
        heleneHave      BOOLEAN,
        schoolCount     INTEGER,
        schoolHave      BOOLEAN,
        elementalCount  INTEGER,
        elementalHave,
        notHealButCount,
        notHealButHave,
        greatHealCount,
        greatHealHave,
        greatDpsCount,
        greatDpsHave,
        poisonCount,
        poisonHave
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
                                schoolHave
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
                                schoolHave
                            FROM sqlitestudio_temp_table;
    DROP TABLE sqlitestudio_temp_table;
    PRAGMA foreign_keys = 1;
"""

if not(os.path.exists("./data/success.db")):
    temp = open("./data/success.db","bw")
    print("Création du fichier \"success.db\"")
    temp.close()

class success:
    """Classe des succès"""
    def __init__(self,name : str,countToSucced : int,code: str,recompense = None,description = "Pas de description",emoji=None):
        self.name = name
        self.count = 0
        self.code = code
        self.countToSucced = countToSucced
        self.haveSucced = False
        self.recompense = recompense
        self.description = description
        self.emoji = emoji

        if type(recompense) != list:
            self.recompense = [recompense]

    def toDict(self):
        """Renvoie un dict contenant les informations du succès"""
        rep = {"name":self.name,"count":self.count,"countToSucced":self.countToSucced,"haveSucced":self.haveSucced,"recompense":self.recompense,"description":self.description,"code":self.code}
        return rep

class successTabl:
    def __init__(self):
        self.alice = success("Oubliez pas qu'une rose a des épines",10,"alice",recompense="jz",description="Affrontez ou faites équipe avec Alice {0} fois",emoji='<:ikaPink:866459344173137930>')
        self.clemence = success("La quête de la nuit",10,"clemence",recompense="bg",description="Affontez ou faites équipe avec Clémence {0} fois",emoji='<:takoRed:866459004439756810>')
        self.akira = success("Seconde impression",10,"akira",recompense="bh",description="Affontez ou faites équipe avec Akira {0} fois",emoji='<:takoBlack:871151069193969714>')
        self.fight = success("L'ivresse du combat",1,"fight",recompense="ys",description="Faire {0} combat manuel",emoji='<:splattershotJR:866367630465433611>')
        self.gwen = success("Une histoire de vangeance",10,"gwen",["ka","kb"],"Affontez ou faites équipe avec Gwendoline {0} fois",emoji='<:takoYellow:866459052132532275>')
        self.quickFight = success("Le temps c'est de l'argent",10,"quickFight",None,"Lancez {0} combats rapides",'<:hourglass1:872181651801772052>')
        self.helene = success("Là où mes ailes me porteront",10,"helene","yr","Affrontez ou faites équipe avec Hélène {0} fois",'<:takoWhite:871149576965455933>')
        self.school = success("Je ne veux pas d'écolière pour défendre nos terres",30,"school",None,"Mi Miman tu es habiyée en écolière... Combatti {0} fois !",'<:splattershot:866367647113543730>')
        self.elemental = success("Elémentaire mon cher Watson",1,"elemental","qe","Combattre {0} fois en étant niveau 10 ou plus",'<:neutral:887847377917050930>')
        self.notHealBut = success("Situation désespérée Mesure désespérée",500,"notHealBut",None,"Sans être Altruiste, Idole ou Erudit, soignez un total de {0} PV",'<:bandage:873542442484396073>')
        self.greatHeal = success("Soigneur de compétiton",5000,"greatHeal",["kc","kd"],"Soignez un total de {0} PV",'<:seringue:887402558665142343>')
        self.greatDps = success("La meilleure défense c'est l'attaque",5000,"greatDps",None,"Infligez un total de {0} dégâts directs",'<:splatcharger:866367658752213024>')
        self.poison = success("Notre pire ennemi, c'est nous même",5000,"poison",None,"Infligez un total de {0} dégâts indirects",'<:butterflyV:883627142615805962>')

    def tablAllSuccess(self):
        """Renvoie un tableau avec tous les objets success"""
        return [self.alice,self.clemence,self.akira,self.fight,self.gwen,self.quickFight,self.helene,self.school,self.elemental,self.notHealBut,self.greatHeal,self.greatDps,self.poison]

    def where(self,where : str):
        alls = self.tablAllSuccess()
        for a in range(0,len(alls)):
            if where == alls[a].code:
                return alls[a]

    def changeCount(self,where : str,count,haveSucced):
        where = self.where(where)
        where.count = count
        where.haveSucced = haveSucced

    async def addCount(self,ctx,user,where : str,add = 1):
        where = self.where(where)
        where.count += add

        if where.count >= where.countToSucced and not(where.haveSucced):
            desti = "Vous avez "
            if user.owner != int(ctx.author.id) :
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
                            recompenseMsg += "{0} {1}".format(recompense.emoji,recompense.name)
                    elif what == 1:
                        recompense = findSkill(a)
                        if recompense == None:
                            print("La compétence {0} n'a pas été trouvée".format(a))
                        elif user.have(recompense):
                            print("{0} possède déjà {1}".format(user.name,recompense.name))
                        else:
                            user.skillInventory.append(recompense)
                            recompenseMsg += "{0} {1}".format(recompense.emoji,recompense.name)
                    elif what == 2:
                        recompense = findStuff(a)
                        if recompense == None:
                            print("L'aéquipement {0} n'a pas été trouvée".format(a))
                        elif user.have(recompense):
                            print("{0} possède déjà {1}".format(user.name,recompense.name))
                        else:
                            user.stuffInventory.append(recompense)
                            recompenseMsg += "{0} {1}".format(recompense.emoji,recompense.name)
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
        self.con = sqlite3.connect(f"./data/{database}")
        self.con.row_factory = sqlite3.Row
        self.database = database

        cursor = self.con.cursor()

        # Création de la table
        try:
            cursor.execute("SELECT * FROM achivements;")
        except:
            cursor.execute(createTabl)
            self.con.commit()
            print("Table achivements créé")

        # Maj Ivresse du combat
        try:
            cursor.execute("SELECT fightCount FROM achivements;")
        except:
            temp = ""
            for a in maj1:
                if a != ";":
                    temp+=a
                else:
                    cursor.execute(temp)
                    temp = ""

            cursor.execute("UPDATE achivements SET fightCount = ?, fightHave = ?;",(0,False))
            self.con.commit()
            print("maj1 réalisée")

        # Maj Gwen
        try:
            cursor.execute("SELECT gwenCount FROM achivements;")
        except:
            temp = ""
            for a in maj2:
                if a != ";":
                    temp+=a
                else:
                    cursor.execute(temp)
                    temp = ""

            cursor.execute("UPDATE achivements SET gwenCount = ?, gwenHave = ?, qfCount = ?, qfHave = ?;",(0,False,0,False,))
            self.con.commit()
            print("maj2 réalisée")
    
        # Maj Hélène
        try:
            cursor.execute("SELECT heleneCount FROM achivements;")
        except:
            temp = ""
            for a in maj3:
                if a != ";":
                    temp+=a
                else:
                    cursor.execute(temp)
                    temp = ""

            cursor.execute("UPDATE achivements SET heleneCount = ?, heleneHave = ?;",(0,False))
            self.con.commit()
            print("maj3 réalisée")

        # Maj school
        try:
            cursor.execute("SELECT schoolCount FROM achivements;")
        except:
            temp = ""
            for a in maj4:
                if a != ";":
                    temp+=a
                else:
                    cursor.execute(temp)
                    temp = ""

            cursor.execute("UPDATE achivements SET schoolCount = ?, schoolHave = ?;",(0,False))
            self.con.commit()
            print("maj4 réalisée")

        # Maj quickFightCount
        try:
            cursor.execute("SELECT quickFightCount FROM achivements;")
        except:
            temp = ""
            for a in maj5:
                if a != ";":
                    temp+=a
                else:
                    cursor.execute(temp)
                    temp = ""
            self.con.commit()
            print("maj5 réalisée")

        # Maj elemental
        try:
            cursor.execute("SELECT elementalCount FROM achivements;")
        except:
            temp = ""
            for a in maj6:
                if a != ";":
                    temp+=a
                else:
                    cursor.execute(temp)
                    temp = ""

            cursor.execute("UPDATE achivements SET elementalCount = ?, elementalHave = ?, notHealButCount = ?, notHealButHave = ?, greatHealCount = ?, greatHealHave = ?, greatDpsCount = ?, greatDpsHave = ?, poisonCount = ?, poisonHave = ?;",(0,False,0,False,0,False,0,False,0,False))
            self.con.commit()
            print("maj6 réalisée")

        # Fin des majs
        cursor.close()

    def getSuccess(self,user):
        cursor = self.con.cursor()

        # Vérification de si l'utilisateur est dans la base de donée :
        cursor.execute("SELECT * FROM achivements WHERE id = ?",(user.owner,))
        result = cursor.fetchall()

        if len(result) == 0: # L'utilisateur n'est pas dans la base de donnée
            params = (user.owner,0,False,0,False,0,False,0,False,0,False,0,False,0,False,0,False,0,False,0,False,0,False,0,False,0,False)
            cursor.execute("INSERT INTO achivements VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",params)
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
        cursor.execute("UPDATE achivements SET {0}Count = ?, {0}Have = ? WHERE id = ?;".format(achivement.code),(achivement.count,achivement.haveSucced,user.owner,))
        cursor.close()
        self.con.commit()
        
achivement = succesDb("success.db")