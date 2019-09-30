class Village:
    "Classe permettant de creer un village"

    def __init__(self, nom, typeDeVillage, ressource, x, y, ville):
        self.nom = nom
        self.typeDeVillage = typeDeVillage
        self.ressource = ressource
        self.x = x
        self.y = y
        self.z = -x + -y  # coordonnees cubique (voir le site hexagonal grid)
        self.ville = ville
        self.niveau = 1
        self.constr = [-1, 0, 0]

        i = 0
        for a in ["Bois", "Pierre", "Fer", "Or", "Charbon", "Marbre", "Acier", "Nourriture", "Betail", "Chevaux"]:
            if self.ressource == a:
                break
            i += 1

        self.idRessource = i

    def cout(self):
        "Methode servant a calculer le prix pour ameliorer d'un niveau le village"

        self.ville.bdd.execute("""SELECT * FROM Village WHERE Nom == '%s' AND Niveau == %s""" % (self.typeDeVillage, self.niveau + 1))
        return self.ville.bdd.fetchall()[0]

    def construire(self):
        "Methode servant a ameliorer d'un niveau le village"

        liste = self.cout()
        if liste is None:
            return None
        i = 0
        # On regarde qu'il n'est pas deja en train de s'ameliorer
        if self.constr[0] > 0:
            return None
        # On regarde s'il a assez de ressources
        if self.ville.joueur.argent < liste[2]:
            return None
        while i < len(self.ville.ressources) - 1:
            if self.ville.ressources[i] < liste[i + 3]:
                return None
            i += 1
        # si il a assez, on lance la construction
        i = 0
        while i < len(self.ville.ressources) - 1:
            self.ville.ressources[i] -= liste[i + 3]
            i += 1
        self.ville.joueur.argent -= liste[2]
        self.constr[0] = 1
        self.constr[1] = liste[13]

    def revenus(self):
        "Methode servant a calculer les revenus du village a la fin du tour"

        self.ville.bdd.execute("""SELECT Revenus FROM VillageEffets WHERE Nom == '%s' AND Niveau == '%s'""" % (self.typeDeVillage, self.niveau))
        return self.ville.bdd.fetchall()[0][0]

    def changerVille(self, ville):
        self.ville.villages.remove(self)
        self.ville = ville
        self.ville.villages.append(self)
        print("Village change")

    def clic(self):
        "Methode s'activant lors d'un clic sur le village sur la carte"

        # self.ville.fenetre.ui.wVillage.maj()
        self.ville.fenetre.boutons.ui.wVillage.show()
        self.ville.fenetre.boutons.ui.wVillage.setFocus()
        # self.construire()  # Test  A SUPPRIMER APRES

    def debutDuTour(self):
        "Methode servant a faire les actions de debut du tour du village"

        # On ameliore le batiment s'il le faut
        if self.constr[0] > 0:
            self.constr[2] += 1
            if self.constr[2] >= self.constr[1]:
                print("Village ameliore")
                self.niveau += 1
                self.constr[0] = -1
                self.constr[1] = 0
                self.constr[2] = 0

    def finDuTour(self):
        "Methode servant a faire les actions de fin du tour du village"


class Carriere(Village):
    "Classe permettant de creer un village de type carriere"

    def __init__(self, nom, ressource, x, y, ville):
        if ressource != "Pierre" and ressource != "Marbre":
            return None
        super(Carriere, self).__init__(nom, "C", ressource, x, y, ville)

    def revenus(self):
        "Methode servant a calculer les revenus du village a la fin du tour"

        revenus = super(Carriere, self).revenus()
        # Rapporte 10x moins si c'est du marbre
        if self.ressource == "Marbre":
            return int(revenus / 10)
        return revenus


class Mine(Village):
    "Classe permettant de creer un village de type mine"

    def __init__(self, nom, ressource, x, y, ville):
        if ressource != "Fer" and ressource != "Or" and ressource != "Charbon":
            return None
        super(Carriere, self).__init__(nom, "M", ressource, x, y, ville)


class VillageCotier(Village):
    "Classe permettant de creer un village de type VC"

    def __init__(self, nom, ressource, x, y, ville):
        if ressource != "Nourriture":
            return None
        super(VillageCotier, self).__init__(self, nom, "VC", ressource, x, y, ville)


class VillageBucheron(Village):
    "Classe permettant de creer un village de type VB"

    def __init__(self, nom, ressource, x, y, ville):
        if ressource != "Bois":
            return None
        super(VillageBucheron, self).__init__(self, nom, "VB", ressource, x, y, ville)


class Ferme(Village):
    "Classe permettant de creer un village de type F"

    def __init__(self, nom, ressource, x, y, ville):
        if ressource != "Nourriture":
            return None
        super(Ferme, self).__init__(self, nom, "F", ressource, x, y, ville)


class ElevageBetail(Village):
    "Classe permettant de creer un village de type EB"

    def __init__(self, nom, ressource, x, y, ville):
        if ressource != "Betail":
            return None
        super(ElevageBetail, self).__init__(self, nom, "EB", ressource, x, y, ville)
        self.nbBetail = 0  # On commence avec 0 betail, il faudra en acheter puis les faire se reproduire
        self.limite = [100, 300, 700]

    def modifBetail(self):
        "Methode pour calculer la modification du nombre de betail (en %)"

        return 10  # modification de 10% en plus par tour (sans les event)

    def debutDuTour(self):
        "Methode servant a faire les actions de debut du tour du village"

        # Si trop peu de betail que pour qu'il y aie une augmentation
        if int(self.nbBetail * (self.modifBetail + 100) / 100) == 0 and self.nbBetail > 1:
            self.nbBetail += 1

        self.nbBetail = int(self.nbBetail * (self.modifBetail() + 100) / 100)  # La pop augmente
        # Si elle augmente trop, ca ne depasse quand meme pas la limite
        if self.nbBetail > self.limite[self.niveau - 1]:
            self.nbBetail = self.limite[self.niveau - 1]
        # Le betail consomme de la nourriture (1 par betail)
        self.ville.ressources[7] -= self.nbChevaux * 1
        # On fait un debut de tour normal apres
        super(ElevageBetail, self).debutDuTour()

    def revenus(self):
        "Methode servant a calculer le revenus du village (0 ici, car le nombre de betails augmente mais ne rapporte rien)"

        return 0


class ElevageChevaux(Village):
    "Classe permettant de creer un village de type EC"

    def __init__(self, nom, ressource, x, y, ville):
        if ressource != "Chevaux":
            return None
        super(ElevageChevaux, self).__init__(self, nom, "EC", ressource, x, y, ville)
        self.nbChevaux = 0  # On commence avec 0 chevaux, il faudra en acheter puis les faire se reproduire
        self.limite = [50, 150, 400]

    def modifChevaux(self):
        "Methode pour calculer la modification du nombre de chevaux (en %)"

        return 5  # modification de 5% en plus par tour (sans les event)

    def debutDuTour(self):
        "Methode servant a faire les actions de debut du tour du village"

        # Si trop peu de chevaux que pour qu'il y aie une augmentation
        if int(self.nbChevaux * (self.modifChevaux + 100) / 100) == 0 and self.nbChevaux > 1:
            self.nbChevaux += 1

        self.nbChevaux = int(self.nbChevaux * (self.modifChevaux() + 100) / 100)  # La pop augmente
        # Si elle augmente trop, ca ne depasse quand meme pas la limite
        if self.nbChevaux > self.limite[self.niveau - 1]:
            self.nbChevaux = self.limite[self.niveau - 1]
        # Les chevaux consomme de la nourriture (2 par cheval)
        self.ville.ressources[7] -= self.nbChevaux * 2
        # On fait un debut de tour normal apres
        super(ElevageChevaux, self).debutDuTour()

    def revenus(self):
        "Methode servant a calculer le revenus du village (0 ici, car le nombre dechevaux augmente mais ne rapporte rien)"

        return 0
