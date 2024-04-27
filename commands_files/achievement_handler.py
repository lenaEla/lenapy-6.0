import sqlite3, os
from gestion import *
from advance_gestion import *
from advObjects.advSkills import *
from advObjects.advAllies import findAllie
from adv import *

if not(os.path.exists("./data/database/success.db")):
    temp = open("./data/database/success.db","bw")
    print("Création du fichier \"success.db\"")
    temp.close()

class achivement:
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

class achiveTabl:
    def __init__(self):
        self.alice = achivement("Oubliez pas qu'une rose a des épines",10,"alice",recompense="jz",description="Affrontez ou faites équipe avec Alice {0} fois",emoji=findAllie("Alice").icon)
        self.clemence = achivement("La quête de la nuit",10,"clemence",recompense="bg",description="Affrontez ou faites équipe avec Clémence {0} fois",emoji=findAllie("Clémence").icon)
        self.akira = achivement("Seconde impression",10,"akira",recompense="bh",description="Affrontez ou faites équipe avec Akira {0} fois",emoji=findAllie("Akira").icon)
        self.fight = achivement("L'ivresse du combat",1,"fight",recompense="ys",description="Faire {0} combat manuel",emoji='<:splattershotJR:866367630465433611>')
        self.gwen = achivement("Une histoire de vangeance",3,"gwen",["ka","kb",gwenyStrike.id],"Affrontez ou faites équipe avec Gwendoline {0} fois",emoji=findAllie("Gwendoline").icon)
        self.quickFight = achivement("Le temps c'est de l'argent",10,"quickFight",None,"Lancez {0} combats rapides",'<:hourglass1:872181651801772052>')
        self.helene = achivement("Là où mes ailes me porteront",10,"helene","yr","Affrontez ou faites équipe avec Hélène {0} fois",findAllie("Hélène").icon)
        self.school = achivement("Je ne veux pas d'écolière pour défendre nos terres",30,"school",None,"Combattre {0} fois !",'<:splattershot:866367647113543730>')
        self.elemental = achivement("Elémentaire mon cher Watson",1,"elemental","qe","Combattre {0} fois en étant niveau 10 ou plus",'<:neutral:887847377917050930>')
        self.notHealBut = achivement("Situation désespérée Mesure désespérée",500,"notHealBut",None,"Sans être Altruiste, Idole ou Erudit, soignez un total de {0} PV",'<:bandage:873542442484396073>')
        self.greatHeal = achivement("Soigneur de compétiton",5000,"greatHeal",["kc","kd"],"Soignez un total de {0} PV",'<:seringue:887402558665142343>')
        self.greatDps = achivement("La meilleure défense c'est l'attaque",5000,"greatDps",None,"Infligez un total de {0} dégâts directs",'<:splatcharger:866367658752213024>')
        self.poison = achivement("Notre pire ennemi, c'est nous même",5000,"poison",None,"Infligez un total de {0} dégâts indirects",'<:butterflyV:883627142615805962>')
        self.icealia = achivement("Prévoir l'imprévisible",10,"icea","vn","Faite équipe ou affrontez {0} fois Icealia",findAllie("Icealia").icon)
        self.shehisa = achivement("Pas vue, pas prise",10,"sram","vq","Faite équipe ou affrontez {0} fois Shehisa",findAllie("Shehisa").icon)
        self.heriteEstialba = achivement("Savoir utiliser ses atouts",25000,"estialba",description="Infligez {0} dégâts indirects à l'aide de l'effet \"__<:est:884223390804766740> Poison d'Estialba__\"",emoji=findAllie("Lohica").icon)
        self.heriteLesath = achivement("Il faut que ça sorte",25000,"lesath",description="Infligez {0} dégâts indirects à l'aide de l'effet \"__<:bleeding:1133258052225745048> Hémorragie__\"",emoji="<:ombralStrike:900083085708771349>")
        self.powehi = achivement("La fin de tout, et renouvellement",10,"powehi","uj","Affrontez ou faites équipe avec Powehi {0} fois",findAllie("Powehi").icon)
        self.dimentio = achivement("Le secret de l'imperceptible",1,"dimentio","qh","Combattre {0} fois en étant niveau 20 ou plus","<:krysTal2:907638077307097088>")
        self.feli = achivement("Ne jamais abandonner",10,"feli","tl","Affrontez ou faites équipe avec Félicité {0} fois",findAllie("Félicité").icon)
        self.sixtine = achivement("Tomber dans les bras de Morphée",10,"sixtine","tk","Affrontez ou faites équipe avec Sixtine {0} fois",findAllie("Sixtine").icon)
        self.hina = achivement("Voler à la recousse",10,"hina","tj","Affrontez ou faites équipe avec Hina {0} fois","<:hina:908820821185810454>")
        self.luna = achivement("La prêtresse obsitnée",3,"luna",description="Vainquez {0} le boss \"Luna\"",emoji="<:luna:909047362868105227>",recompense=["oq","or","os","ot","ou","ov"])
        self.julie = achivement("Être dans les temps",10,"julie","ti","Affrontez ou faites équipe avec Julie {0} fois","<:julie:910185448951906325>")
        self.memClem = achivement("La Chauve-Souris Archaniste et la Rose",3,"clemMem","sv","Combattez Clémence Possédée {0} fois","<a:clemPos:914709222116175922>")
        self.krys = achivement("Cris \"Staline\" !",10,"krys","st","Affrontez ou faites équipe avec Krys {0} fois","<:krys:916118008991215726>")
        self.liu = achivement("Tochi no ai",10,"liu",description="Combattez Liu {0} fois",emoji='<:earthKitsune:917670882586017792>',recompense='zzc')
        self.lia = achivement("Kaze no ai",10,"lia",description="Combattez Lia {0} fois",emoji='<:airKitsune:917670912646602823>',recompense='zzb')
        self.lio = achivement("Mizu no ai",10,"lio",description="Combattez Lio {0} fois",emoji='<:waterKitsune:917670866626707516>',recompense='zza')
        self.liz = achivement("Hi no ai",10,"liz",description="Combattez Liz {0} fois",emoji='<:fireKitsune:917670925904785408>',recompense='zyz')
        self.head = achivement("À en perdre la tête",1,"ailill",description="???",emoji='<:blocked:897631107602841600>')
        self.lightNShadow = achivement("L'Ombre et la Lumière",1,"lightNShadow",description="Affrontez ou faites équipe avec simultanément Iliana et Luna (ou Shihu)",emoji="<:Iliana:926425844056985640><:luna:909047362868105227>")
        self.fullDarkness = achivement("Ténèbres Éternels",5,"fullDark",description="Affrontez ou faites équipe Luna ou Shihu {0} fois",emoji='<:luna:909047362868105227><:shihu:909047672541945927>',recompense="cw")
        self.fraticide = achivement("Feu allié",1,"fratere",description="???",emoji='<a:meeting2:760186427119501312><a:meeting1:760186398401232916>')
        self.fullLight = achivement("Lumière Éternelle",25,"light",description="Faite équipe ou combattez Iliana {0} fois",emoji='<:Iliana:926425844056985640>',recompense='cx')
        self.dangerousFight = achivement("Jeu dangereux",1,"dangerous",description="Gagner un combat en ayant 80% de résistance soins ou plus",emoji='<:healnt:903595333949464607>')
        self.loosing = achivement("Toucher le fond",1,"loose",description="Perdre un combat avec le plus faible taux de danger possible")
        self.still = achivement("You win by doing absolutly nothing",1,"still",description="Gagner un combat en passant tous vos tours",recompense='hga')
        self.dirty = achivement("Main propre",5,"dirty",description="Gagner {0} combats en étant dans les 3 meilleurs DPT sans infliger de dégâts directs")
        self.delegation = achivement("Laisser le sale boulot aux autres",1,"delegation",description="Terminer un combat en atant meilleur DPT mais en ayant réalisé aucune élimination")
        self.stella = achivement("Puissance solaire",10,"stella","srb",description="Affrontez Stella {0} fois",emoji=findEnnemi("Stella").icon)
        self.momKitsune = achivement("La passion originelle",3,"momKitsune","sph",description="Affrontez Kitsune {0} fois",emoji=findEnnemi("Kitsune").icon)
        self.kiku1 = achivement("Aux portes de la mort",5,"kiku1","spg",description="Affrontez Kiku {0} fois",emoji=findEnnemi("Kiku").icon)
        self.kiku2 = achivement("Rire au visage de la mort",1,"kiku2",description="Être en vie en commençant son 16e tour tout en ayant l'effet \"Mors Vita Est\" de Kiku",emoji=findEnnemi("Kiku").icon)
        self.suffering = achivement("Suffering form success",1,"suffering",description="Remplir l'une des conditions suivantes :\n- Être ciblé par la compétence Carapace à épines\n- Être vaincu pour son propre effet de dégâts indirect",emoji=blueShell.emoji)
        self.ailill2 = achivement("Un résultat sanglant",3,"ailill2",bloodBath2.id,"Affrontez Ailill {0} fois",emoji='<a:Ailill:882040705814503434>')
        self.alty = achivement("Laisser la vedette aux autres",3,"alty",altyCover.id,"Affrontez ou faites équipe avec Altikia {0} fois","<:alty:1112517632671875152>")
        self.klikli = achivement("Ne pas laissez les autres imposer leur volonté",3,"klikli",klikliStrike.id,"Affrontez ou faites équipe avec Klironovia {0} fois","<:klikli:906303031837073429>")
        self.liaEx = achivement("Filer comme le vent",3,"liaEx",Hauringusutomusodo.id,"Rencontrer {0} fois le combat de Lia Ex",'<:liaEx:1079115890437656598>')
        self.ilianaEx = achivement("Qui continue de briller dans le Noir",3,"catEx",eternalLight,"Rencontrer {0} fois le combat de Iliana Prê.","<:iliPre:1053017768443785236>")
        self.clemEx = achivement("Sang pitié",3,"clemEx",komoriHerit.id,description="Rencontrer {0} fois le combat de Clémence Ex",emoji=tablVarAllies[4].splashIcon)
        self.anna = achivement("Moitié perdue",7,"anna",inMemoria.id,"Affrontez ou faites équipe avec Anna {0} fois",emoji="<:anna:943444730430246933>")
        self.belle = achivement("Moitié brisée",3,"belle",description="Affrontez ou faites équipe avec Belle {0} fois",emoji="<:belle:943444751288528957>")
        self.masterDamage = achivement("Quête de la puissance",500,"masterDamage",description="Infligez l'équivalent de **{0} fois** vos PV Max en dégâts",emoji='<a:dmgBuffB:954429227657224272>',recompense=[renforPhys.id,dualCast.id])
        self.masterTank = achivement("Quête de la résistance",500,"masterTank",description="Recevoir l'équivalent de **{0} fois** vos PV Max de dégâts",emoji='<a:defBuffB:954537632543682620>')
        self.marineDealer = achivement("Do what you want 'cause a pirate is free",50,"marineDealer",[fairyLiberation.id,exploPetal.id],description="Vaincre **{0} ennemis** ayant une affinité avec les **Marines**",emoji='<:pirSan2:1059519736347631696>')
        self.celeste = achivement("Le début d'une aventure céleste",10,"celeste",selfMemoria.id,"Affrontez ou faites équipe avec Céleste {0} fois",emoji=findAllie("Céleste").icon)
        self.shushi = achivement("Filer telle une anguille",10,"shushi",squidRoll.id,"Affrontez ou faites équipe avec Shushi {0} fois",emoji=findAllie("Shushi").icon)
        self.convicStar1 = achivement("Conviction des étoiles 1",1,"convicStar1",description="Soyez témoins de la compétence \"Conviction de Silicia\" lors de **{0}** combats",emoji="<:silicia:1045109225615003729>",recompense=[tripleCommunCards.id])
        self.convicStar2 = achivement("Conviction des étoiles 2",5,"convicStar2",description="Soyez témoins de la compétence \"Conviction de Silicia\" lors de **{0}** combats",emoji="<:silicia:1045109225615003729>",recompense=[tripleCommunCards.id,dailyCardBooster1.id])
        self.convicStar3 = achivement("Conviction des étoiles 3",20,"convicStar3",description="Soyez témoins de la compétence \"Conviction de Silicia\" lors de **{0}** combats",emoji="<:silicia:1045109225615003729>",recompense=[tripleCommunCards.id,singleRareCards.id,dailyCardBooster2.id])

    def tablAllSuccess(self)->List[achivement]:
        """Renvoie un tableau avec tous les objets success"""
        toReturn = []
        for a, b in self.__dict__.items():
            toReturn.append(b)
        return toReturn

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

    async def addCount(self,ctx,user,where : str,add = 1, sendEmbed = False):
        where, hadSucced = self.where(where), False
        where.count += add

        if where.count >= where.countToSucced and not(where.haveSucced):
            desti = "Vous avez "
            if int(user.owner) != int(ctx.author.id) :
                desti = user.name + " a "
            emb = interactions.Embed(title=where.name,color=user.color,description=desti+"terminé le succès {0} !".format(where.name))

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
                            print("L'équipement {0} n'a pas été trouvée".format(a))
                        elif user.have(recompense):
                            print("{0} possède déjà {1}".format(user.name,recompense.name))
                        else:
                            user.stuffInventory.append(recompense)
                            recompenseMsg += "{0} {1}\n".format(recompense.emoji,recompense.name)
                    elif what == 3:
                        recompense = findOther(a)
                        if recompense == None:
                            print("L'équipement {0} n'a pas été trouvée".format(a))
                        elif recompense.id in [tripleCommunCards.id,singleRareCards.id]:
                            pass
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
                emb.add_field(name=desti + "obtenu l{1}objet{0} suivant{0} :".format(pluriel,pluriel2),value=recompenseMsg)

            if sendEmbed:
                await ctx.channel.send(embeds=emb)
            where.haveSucced = True
            saveCharFile(user=user)
            hadSucced = True

        achivementStand.updateSuccess(user,where)
        return user, hadSucced

class succesDb:
    def __init__(self, database : str):
        self.con = sqlite3.connect(f"./data/database/{database}",check_same_thread=False)
        self.con.row_factory = sqlite3.Row
        self.database, tabl = database, achiveTabl()

        cursor, tabl = self.con.cursor(), tabl.tablAllSuccess()

        try:
            cursor.execute("SELECT * from achivements;")
        except:
            cursor.execute("CREATE TABLE achivements (id INTEGER PRIMARY KEY)")
            print("Tabl Achivment créée")
            self.con.commit()

        for achiv in tabl:
            try:
                cursor.execute("SELECT {0}Have FROM achivements;".format(achiv.code))
            except:
                cursor.execute("ALTER TABLE achivements ADD {0}Count INTEGER DEFAULT (0)".format(achiv.code))
                cursor.execute("ALTER TABLE achivements ADD {0}Have BOOLEAN DEFAULT (0)".format(achiv.code))
                cursor.execute("UPDATE achivements SET {0}Count = 0, {0}Have = 0;".format(achiv.code))
                print("Achivement {0} ajouté à la base de donné".format(achiv.name))
                self.con.commit()

        # Fin des majs
        cursor.close()

    def getSuccess(self,user)->achiveTabl:
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
        cursor.close()
        achivTabl = achiveTabl()

        for a in achivTabl.tablAllSuccess():
            b,c = "{0}Count".format(a.code),"{0}Have".format(a.code)
            achivTabl.changeCount(a.code,result[b],result[c])

        return achivTabl

    def updateSuccess(self,user,achivement):
        cursor = self.con.cursor()
        cursor.execute("UPDATE achivements SET {0}Count = ?, {0}Have = ? WHERE id = ?;".format(achivement.code),(achivement.count,achivement.haveSucced,int(user.owner),))
        cursor.close()
        self.con.commit()

achivementStand = succesDb("success.db")