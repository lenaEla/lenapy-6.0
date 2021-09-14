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

if not(os.path.exists("./data/success.db")):
    temp = open("./data/success.db","bw")
    print("Création du fichier \"success.db\"")
    temp.close()

class success:
    """Classe des succès"""
    def __init__(self,name : str,count : int,countToSucced : int,haveSucced = False,recompense = None,description = "Pas de description"):
        self.name = name
        self.count = count
        self.countToSucced = countToSucced
        self.haveSucced = haveSucced
        self.recompense = recompense
        self.description = description

        if type(recompense) != list:
            self.recompense = [recompense]

    def toDict(self):
        """Renvoie un dict contenant les informations du succès"""
        rep = {"name":self.name,"count":self.count,"countToSucced":self.countToSucced,"haveSucced":self.haveSucced,"recompense":self.recompense,"description":self.description}
        return rep

class successTabl:
    def __init__(self):
        self.alice = success("Oubliez pas qu'une rose a des épines",0,10,recompense="jz",description="Affrontez ou faites équipe avec Alice {0} fois")
        self.clemence = success("La quête de la nuit",0,10,recompense="bg",description="Affontez ou faites équipe avec Clémence {0} fois")
        self.akira = success("Seconde impression",0,10,recompense="bh",description="Affontez ou faites équipe avec Akira {0} fois")
        self.fight = success("L'ivresse du combat",0,1,recompense="ys",description="Faire {0} combat manuel")
        self.gwen = success("Une histoire de vangeance",0,10,False,["ka","kb"],"Affontez ou faites équipe avec Gwendoline {0} fois")
        self.quickFight = success("Le temps c'est de l'argent",0,10,False,None,"Lancez {0} combats rapides")
        self.helene = success("Là où mes ailes me porteront",0,10,False,"yr","Affrontez ou faites équipe avec Hélène {0} fois")

    def tablAllSuccess(self):
        """Renvoie un tableau avec tous les objets success"""
        return [self.alice,self.clemence,self.akira,self.fight,self.gwen,self.quickFight,self.helene]

    def where(self,where : str):
        if where == "alice":
            return self.alice
        elif where == "clemence":
            return self.clemence
        elif where == "akira":
            return self.akira
        elif where == "fight":
            return self.fight
        elif where == "gwen":
            return self.gwen
        elif where == "quickFight":
            return self.quickFight
        elif where == "helene":
            return self.helene

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

nbSuccess = 3

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

        # Fin des majs
        cursor.close()

    def getSuccess(self,user):
        cursor = self.con.cursor()

        # Vérification de si l'utilisateur est dans la base de donée :
        cursor.execute("SELECT * FROM achivements WHERE id = ?",(user.owner,))
        result = cursor.fetchall()

        if len(result) == 0: # L'utilisateur n'est pas dans la base de donnée
            params = (user.owner,0,False,0,False,0,False,0,False,0,False,0,False,0,False)
            cursor.execute("INSERT INTO achivements VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",params)
            self.con.commit()

            cursor.execute("SELECT * FROM achivements WHERE id = ?",(user.owner,))
            result = cursor.fetchall()

        result = result[0]
        achivTabl = successTabl()

        achivTabl.changeCount("alice",result["aliceCount"],result["aliceHave"])
        achivTabl.changeCount("clemence",result["clemenceCount"],result["clemenceHave"])
        achivTabl.changeCount("akira",result["akiraCount"],result["akiraHave"])
        achivTabl.changeCount("fight",result["fightCount"],result["fightHave"])
        achivTabl.changeCount("gwen",result["gwenCount"],result["gwenHave"])
        achivTabl.changeCount("quickFight",result["qfCount"],result["qfHave"])

        return achivTabl

    def updateSuccess(self,user,achivement):
        cursor = self.con.cursor()

        name = achivement.name
        if name == "Oubliez pas qu'une rose a des épines":
            collum1,collum2 = "aliceCount","aliceHave"
        elif name == "La quête de la nuit":
            collum1,collum2 = "clemenceCount","clemenceHave"
        elif name == "Seconde impression":
            collum1,collum2 = "akiraCount","akiraHave"
        elif name == "L'ivresse du combat":
            collum1,collum2 = "fightCount","fightHave"
        elif name == "Une histoire de vangeance":
            collum1,collum2 = "gwenCount","gwenHave" 
        elif name == "Le temps c'est de l'argent":
            collum1,collum2 = "qfCount","qfHave"
        elif name == "Là où mes ailes me porteront":
            collum1,collum2 = "heleneCount","heleneHave"
        
        cursor.execute("UPDATE achivements SET {0} = ?, {1} = ? WHERE id = ?;".format(collum1,collum2),(achivement.count,achivement.haveSucced,user.owner,))
        cursor.close()
        self.con.commit()
        
achivement = succesDb("success.db")

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