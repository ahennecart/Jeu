import Villages


class Ville():
    "Classe permettant de creer une Ville"

    def __init__(self, nom, x, y, pop, ressources, joueur, bdd, fenetre):
        self.nom = nom
        self.x = x
        self.y = y
        self.z = -x + -y  # coordonnees cubique (voir le site hexagonal grid)
        self.pop = pop  # Represente le nombre d'habitant dans la ville  POULATION DE BASE = 500 NORMALEMENT
        self.ressources = ressources  # Tableau comprenant toutes les resources selon : [Bois, Pierre, Fer, Or, Charbon, Marbre, Acier, Nourriture, Betail, Chevaux]
        self.joueur = joueur
        self.bdd = bdd
        self.fenetre = fenetre

        self.villages = []

        self.typeCentre = None  # Type de centre-ville (0, 1 ou 2 pour Militaire, economique ou politique)

        # Tableaux contenant la liste des niveau des batiments de chaque quartiers, l'emplacament correspond a un batiment, l'emplacement 0 correspond au quartier
        # Les tableaux sont dans l'ordre d'affichage
        self.batCV = [1, 0, 0, 0, 0, 0, 0, 0]
        self.batUnif = [1, 0, 0, 0, 0, 0]
        self.batInf = [1, 0, 0, 0]
        self.batCav = [1, 0, 0, 0, 0]
        self.batArt = [1, 0, 0, 0]
        self.batMurs = [1, 0, 0, 0, 0, 0, 0, 0, 0]
        self.batMarch = [1, 0, 0, 0]
        self.batEntr = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.batCred = [1, 0, 0, 0, 0, 0, 0, 0, 0]

        # Liste des construction en cours pour chaque quartier, [numBat, tour necessaires, tours faits]
        self.constrCV = [-1, 0, 0]
        self.constrUnif = [-1, 0, 0]
        self.constrInf = [-1, 0, 0]
        self.constrCav = [-1, 0, 0]
        self.constrArt = [-1, 0, 0]
        self.constrMurs = [-1, 0, 0]
        self.constrMarch = [-1, 0, 0]
        self.constrEntr = [-1, 0, 0]
        self.constrCred = [-1, 0, 0]

        self.niveauVille = 1  # Le niveau depend de la population et permet de construire une amélioration de quartier

        self.tauxCrime = 0  # Le taux de crime dans la ville (max : 100)
        self.stabilite = 50  # La stabilite de la ville (min : 0, max : 100)
        self.famine = False  # Variable pour savoir si c'est la famine

        self.joueur.listeVilles.append(self)

    def construire(self, quartier, numBat, parent, condition):
        "Methode servant a construire un batiment"

        print("construction de : " + str(numBat))
        # On regarde si le batiment peut ere ameliore
        if not condition:
            return None
        liste = self.cout(quartier, numBat)
        # On regarde si le joueur a assez de ressource et d'argent:
        if self.joueur.argent < liste[3]:
            return None
        i = 0
        while i < len(self.ressources) - 1:
            if self.ressources[i] < liste[i + 4]:
                return None
            i += 1
        # si il a assez, on lance la construction et on retire les ressources
        i = 0
        while i < len(self.ressources) - 1:
            self.ressources[i] -= liste[i + 4]
            i += 1
        self.joueur.argent -= liste[3]
        self.fenetre.boutons.ui.lcd.display(self.joueur.argent)
        constr = self.quelleListeDeConstr(quartier)
        constr[0] = numBat
        constr[1] = liste[15]

    def cout(self, quartier, numBat):
        "Methode retournant le cout d'un batiment sous forme de la liste qui se trouve dans la bdd (il y a donc tout)"

        niveau = self.quelQuartier(quartier)[numBat] + 1
        self.bdd.execute("""SELECT * FROM Ville WHERE Quartier == "%s" AND Batiment == %s AND Niveau == %s """ % (quartier, numBat, niveau))
        cout = self.bdd.fetchall()
        if cout == []:  # MODIFIER ICI
            return None
        return cout[0]

    def quelQuartier(self, quart):
        "Methode servant a retourner le quartier que l'on veut"

        if quart == "CV":
            return self.batCV
        elif quart == "Unif":
            return self.batUnif
        elif quart == "Inf":
            return self.batInf
        elif quart == "Cav":
            return self.batCav
        elif quart == "Art":
            return self.batArt
        elif quart == "Murs":
            return self.batMurs
        elif quart == "March":
            return self.batMarch
        elif quart == "Entr":
            return self.batEntr
        elif quart == "Credo":
            return self.batCred
        else:
            print("Erreur 1")

    def quelleListeDeConstr(self, quart):
        "Methode servant a retourner la liste de construction que l'on veut"

        if quart == "CV":
            return self.constrCV
        elif quart == "Unif":
            return self.constrUnif
        elif quart == "Inf":
            return self.constrInf
        elif quart == "Cav":
            return self.constrCav
        elif quart == "Art":
            return self.constrArt
        elif quart == "Murs":
            return self.constrMurs
        elif quart == "March":
            return self.constrMarch
        elif quart == "Entr":
            return self.constrEntr
        elif quart == "Credo":
            return self.constrCred
        else:
            print("Erreur 2")

    def addVillage(self, nom, typeVillage, ressource, x, y):
        "Methode pour ajouter un village a la liste de ceux posseder par la ville"

        if typeVillage == "C":
            village = Villages.Carriere(nom, ressource, x, y, self)
        elif typeVillage == "M":
            village = Villages.Mine(nom, ressource, x, y, self)
        elif typeVillage == "":
            village = Villages.Village(nom, ressource, x, y, self)
        if village is None:
            return None
        self.fenetre.viewer.addVillage(x, y, village)
        self.villages.append(village)

    def clic(self):
        "Methode s'activant lors d'un clic sur la ville sur la carte"

        self.fenetre.boutons.ui.setVille(self)
        self.fenetre.boutons.ui.wVilles.show()
        self.fenetre.boutons.ui.wVilles.setFocus()

    def revenus(self):
        "Methode servant a calculer et appliquer les revenus"

        for i in self.villages:
            revenus = i.revenus()
            self.ressources[i.idRessource] = int(self.ressources[i.idRessource] + revenus * (self.modifRess(i.ressource) + 100) / 100)

    def modifPop(self):
        "Methode pour calculer le modificateur de population (en %)"

        return 5

    def modifRess(self, ress):
        "Methode pour calculer le modificateur d'une ressource (en %)"

        return 0  # etat normal, les villages produisent ce qui est dans la bdd

    def variationStabilite(self):
        "Methode pour appliquer les modification de la stabilite en fin de tour"

        NV = self.calculNvVie()
        G = self.calculAttachGouv()
        N = self.calculNourr()
        TC1 = self.calculTauxCroy()
        TC2 = self.calculTauxCrime()

        self.stabilite = self.stabilite + int((10 * NV + 2 * G + 2 * N + TC1 + TC2) / 10)
        if self.stabilite > 100:
            self.stabilite = 100
        elif self.stabilite < 0:
            self.stabilite = 0

    def calculNvVie(self):
        "Methode pour calculer le niveau de vie dans la ville"

        # Faire une fonction pour calculer le nv de vie du aux bat
        # Faire une fonction pour calculer le nv de vie du aux tech

        return 0

    def calculAttachGouv(self):
        "Methode pour calculer les variations de stabilite dues a l'attachement au gouvernement dans la ville"

        # clacul en fonction des taxes :
        if self.joueur.taxes == 0.5:
            T = 5
        elif self.joueur.taxes == 0.75:
            T = 2
        elif self.joueur.taxes == 1:
            T = -1
        elif self.joueur.taxes == 1.25:
            T = -5
        elif self.joueur.taxes == 1.5:
            T = -10

        return 0

    def calculNourr(self):
        "Methode pour calculer les variations de stabilite dues a la nourriture"

        # si il y a famine
        if self.famine is True:
            R = -70
        # si on peut tenir encore 5 tours :
        elif self.ressources[7] > self.pop * 5:
            R = 5
        # si rique de famine :
        elif self.ressources[7] > 0:
            R = -5
        # si manque de bouffe mais pas de famine
        else:
            R = -20

        return 0

    def calculTauxCroy(self):
        "Methode pour calculer les variations de stabilite dues au taux de croyance"

        return 0

    def calculTauxCrime(self):
        "Methode pour calculer et appliquer les variations de stabilite dues au taux de crime"

        # variation du taux de crime
        # A ajouter : armee, chef police, event, general
        # Le taux de crime augmente naturellement :
        self.tauxCrime += 1
        if self.tauxCrime > 100:
            self.tauxCrime = 100
        # Si stabilité trop basse, le taux de crime augmente :
        if self.stabilite < 30:
            self.tauxCrime = (30 - self.stabilite)

        # on doit return self.tauxCrime normalement
        return 0

    def debutDuTour(self):
        "Methode servant a faire les actions de debut du tour"

        # On calcul les revenus
        self.revenus()
        # On fait les actions des villages
        for i in self.villages:
            i.debutDuTour()
        # On construit les batiments en cours
        for i in ("CV", "Unif", "Inf", "Cav", "Art", "Murs", "March", "Entr", "Credo"):
            constrCart = self.quelleListeDeConstr(i)
            if constrCart[0] >= 0:
                constrCart[2] += 1
                if constrCart[2] >= constrCart[1]:
                    self.quelQuartier(i)[constrCart[0]] += 1
                    constrCart[0] = -1
                    constrCart[1] = 0
                    constrCart[2] = 0
        # on modifie la pop
        self.pop = int(self.pop * (self.modifPop() + 100) / 100)
        # On change le niveau de la ville
        if self.pop < 500:
            self.niveauVille = 0
        elif self.pop < 1500:
            self.niveauVille = 1
        elif self.pop < 10000:
            self.niveauVille = 2
        else:  # >= 10000
            self.niveauVille = 3

        # la population consomme de la nourriture:
        self.ressources[7] -= self.pop
        if self.ressources[7] < 0:
            self.ressources[7] = 0

        # gerer la supopulation, la famine, etc

    def finDutour(self):
        "Methode servant a faire les actions de fin du tour"

        self.variationStabilite()
