class Joueur():
    "Classe permettant de representer un joueur, IA ou humain"

    def __init__(self, nom, type, suivant, fenetre=None):
        self.type = type  # 1 pour un humain, 0 pour une IA, -1 pour le marqueur de début de tour (celui qui joue les events generaux)
        self.nom = nom
        self.argent = 5000
        self.fenetre = fenetre
        self.listeVilles = []
        self.suivant = suivant

        self.taxe = 1  # Se modifie via l'interface generale de l'economie (peut valoir : 0.5, 0.75, 1, 1.25, 1.5)
        self.taxeRess = 20  # en %, peut prendre 5, 10, 20, 30, 40, 50 comme valeurs

        self.enVie = 1  # 1 pour un joeur en vie, 0 pour un joueur mort

    def revenusTaxes(self):
        "Methode servant a calculer les revenus dus aux taxes sur les villes"

        revenusArgent = 0
        for i in self.listeVilles:
            revenusArgent += int(i.pop * self.modifArgent())  # Le 1000 est un revenus fixe par ville
        return revenusArgent

    def revenusEchanges(self):
        "Methode servant a calculer les revenus dus aux echanges entre joueurs"

        revenus = 0

        return revenus

    def revenusAccords(self):
        "Methode servant a calculer les revenus dus aux Accords entre joueurs"

        revenus = 0

        return revenus

    def revenusAutres(self):
        "Methode servant a calculer les autres revenuss"

        revenus = len(self.listeVilles) * 1000

        return revenus

    def depArmee(self):
        "Methode servant a calculer les depenses dues aux amrees terrestres"

        depense = 0

        return depense

    def depMarine(self):
        "Methode servant a calculer les depenses dues aux armees maritimes"

        depense = 0

        return depense

    def depAccords(self):
        "Methode servant a calculer les depenses dues aux accords entre joueurs"

        depense = 0

        return depense

    def depAutres(self):
        "Methode servant a calculer les autres depenses"

        depense = 0

        return depense

    def revenus(self):
        "Methode servant à calculer les revenus de la faction entiere, de toutes ses villes et etc"

        self.argent = self.argent + self.revenusTaxes() + len(self.listeVilles) * 1000
        if self.argent < 0:  # Pour gérer la banqueroute et éviter un crash avec l'affichage d'un nombre negatif
            self.argent = 0
        # revenus en ressource des villes:
        for i in self.listeVilles:
            i.debutDuTour()

    def modifArgent(self):
        "Methode pour calculer le modificateur de revenus d'argent (en %)"

        # mettre le lien avec les events ici
        return self.taxe

    def jouer(self):
        "Methode permettant de faire joueur le joueur"

        if self.type == -1:  # le type -1 ne correspond pas a un joueur, mais a un elmt qui marque le debut d'un tour et a faire les event generaux
            self.fenetre.nbTour += 1
            self.fenetre.joueurEnCour = self.suivant
            print("tours += 1")
            self.suivant.jouer()  # /!\ ATTENTION : risque de causer des lags si les actions des IA mettent trop de temps
            return None  # attention a bien retourner None apres un .jouer() pour eviter trop d'action lors du debut du tour d'un joueur humain
        elif self.enVie == 0:  # Si le joueur est mort, on passe son tour
            self.fenetre.joueurEnCour = self.suivant
            self.suivant.jouer()  # /!\ ATTENTION : risque de causer des lags si les actions des IA mettent trop de temps
            return None  # attention a bien retourner None apres un .jouer() pour eviter trop d'action lors du debut du tour d'un joueur humain

        # events, revenus, stabilité, etc
        self.revenus()
        # Si le joueur est une IA, on fini le tour comme ceci (pas besoin d'affichage)
        if self.type == 0:
            # appeler la fonction qui fait jouer les ia ici
            self.finDuTour()
            return None
        # On affiche ce qui doit l'etre
        self.fenetre.boutons.ui.lcd.display(self.argent)

    def finDuTour(self):
        "Methode servant à faire les actions de fin du tour du joueur"

        print("Fin du tour " + str(self.fenetre.nbTour) + " pour le joueur " + self.nom)
        self.fenetre.joueurEnCour = self.suivant
        self.suivant.jouer()  # /!\ ATTENTION : risque de causer des lags si les actions des IA mettent trop de temps
