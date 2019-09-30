from PyQt5.QtWidgets import QWidget, QFrame, QPushButton
from PyQt5.QtCore import Qt
from InfoVille import InfoVille
from Decrets import Decrets
from Recherche import Recherche
from ClassWidget import Cartier


class wVille(QWidget):
    "Classe servant a afficher les widget de la ville"

    def __init__(self, largeur, hauteur, viewer, parent=None):
        super(wVille, self).__init__(parent=parent)
        self.parent = parent
        self.viewer = viewer
        self.setGeometry(0, 0, largeur, hauteur)
        self.fond = QFrame(self)

        # hauteur et largeur de l'ecran, ne pas confondre avec hauteur et largeur du Widget(meme si se sont les meme)
        self.hauteur = hauteur - 200
        self.largeur = largeur - 200
        self.fond.setStyleSheet("QFrame {background-color:white}")
        self.fond.setGeometry(100, 100, self.largeur, self.hauteur)

        self.creationWidegts()
        self.creationBouton()
        self.connectionBoutons()

        self.hide()

    def creationWidegts(self):
        "Methode pour creer tous les widget (batiment, decret, ressources, recherche, armee, etc...)"

        # Widgets contenant tous les batiments de tous les cartiers(Cv, U, I, C, A, M, CM, E, CC)
        listeBat = ["Niveau du quartier", "Poste de gardes", "Prison", "Tour de guet", "Réserves", "Douves", "Puit", "Remparts intérieurs"]
        self.wCV = Cartier(self.largeur, self.hauteur, listeBat, "CV", self)
        listeBat = ["Niveau du quartier", "Bibliothèque", "Aile des sciences mécaniques", "Aile des sciences naturelles", "Aile des sciences militaires", "Tour d'astronomie"]
        self.wUnif = Cartier(self.largeur, self.hauteur, listeBat, "Unif", self)
        listeBat = ["Niveau du quartier", "Caserne", "Camps d'entrainement", "Baraquement des fantassins"]
        self.wInf = Cartier(self.largeur, self.hauteur, listeBat, "Inf", self)
        listeBat = ["Niveau du quartier", "Ecurie", "Champs de manaoeuvres", "Atelier des chars", "Ecole militaire"]
        self.wCav = Cartier(self.largeur, self.hauteur, listeBat, "Cav", self)
        listeBat = ["Niveau du quartier", "Camp de tir", "Ecurie", "Atelier"]
        self.wArt = Cartier(self.largeur, self.hauteur, listeBat, "Art", self)
        listeBat = ["Niveau du quartier", "Douves", "Pont-levis", "Chemin de ronde", "Tours", "Crénaux", "Meurtières", "Catapultes", "Balistes"]
        self.wMurs = Cartier(self.largeur, self.hauteur, listeBat, "Murs", self)
        listeBat = ["Niveau du quartier", "Marché", "Comptoir commercial", "Bâtiments des Guildes"]
        self.wMarch = Cartier(self.largeur, self.hauteur, listeBat, "March", self)
        listeBat = ["Niveau du quartier", "Entrepôt de bois", "Entrepôt de pierre", "Entrepôt de fer", "Entrepôt d'or", "Entrepôt de charbon", "Entrepôt de marbre", "Entrepôt de nourriture", "Entrepôt d'acier", "Fonderie"]
        self.wEntr = Cartier(self.largeur, self.hauteur, listeBat, "Entr", self)
        listeBat = []
        self.wCred = Cartier(self.largeur, self.hauteur, listeBat, "Cred", self)

        # Widgets autres
        self.wInfo = InfoVille(self.largeur, self.hauteur, self)
        self.wDecrets = Decrets(self.largeur, self.hauteur, self)
        self.wRecherche = Recherche(self.largeur, self.hauteur, self)

    def creationBouton(self):
        "Methode pour creer tous les boutons"

        self.bCV = QPushButton(self)
        self.bCV.setGeometry(100, self.hauteur + 50, 50, 50)
        self.bCV.setText("CV")

        self.bUnif = QPushButton(self)
        self.bUnif.setGeometry(150, self.hauteur + 50, 50, 50)
        self.bUnif.setText("U")

        self.bInf = QPushButton(self)
        self.bInf.setGeometry(200, self.hauteur + 50, 50, 50)
        self.bInf.setText("I")

        self.bCav = QPushButton(self)
        self.bCav.setGeometry(250, self.hauteur + 50, 50, 50)
        self.bCav.setText("C")

        self.bArt = QPushButton(self)
        self.bArt.setGeometry(300, self.hauteur + 50, 50, 50)
        self.bArt.setText("A")

        self.bMurs = QPushButton(self)
        self.bMurs.setGeometry(350, self.hauteur + 50, 50, 50)
        self.bMurs.setText("M")

        self.bMarch = QPushButton(self)
        self.bMarch.setGeometry(400, self.hauteur + 50, 50, 50)
        self.bMarch.setText("CM")

        self.bEntr = QPushButton(self)
        self.bEntr.setGeometry(450, self.hauteur + 50, 50, 50)
        self.bEntr.setText("E")

        self.bCred = QPushButton(self)
        self.bCred.setGeometry(500, self.hauteur + 50, 50, 50)
        self.bCred.setText("CC")

        self.bInfo = QPushButton(self)
        self.bInfo.setGeometry(100, 100, 50, 50)
        self.bInfo.setText("I")

        self.bDecret = QPushButton(self)
        self.bDecret.setGeometry(150, 100, 50, 50)
        self.bDecret.setText("D")

        self.bRecherche = QPushButton(self)
        self.bRecherche.setGeometry(200, 100, 50, 50)
        self.bRecherche.setText("R")

        self.bHeros = QPushButton(self)
        self.bHeros.setGeometry(250, 100, 50, 50)
        self.bHeros.setText("H")

        self.bArmGarn = QPushButton(self)
        self.bArmGarn.setGeometry(300, 100, 50, 50)
        self.bArmGarn.setText("AG")

    def connectionBoutons(self):
        "Methode pour connecter les boutons aux fonction"

        self.bCV.clicked.connect(self.afficheCV)
        self.bUnif.clicked.connect(self.afficheUnif)
        self.bInf.clicked.connect(self.afficheInf)
        self.bCav.clicked.connect(self.afficheCav)
        self.bArt.clicked.connect(self.afficheArt)
        self.bMurs.clicked.connect(self.afficheMurs)
        self.bMarch.clicked.connect(self.afficheMarch)
        self.bEntr.clicked.connect(self.afficheEntr)
        self.bCred.clicked.connect(self.afficheCred)

        self.bInfo.clicked.connect(self.afficheInfo)
        self.bDecret.clicked.connect(self.afficheDecret)
        self.bRecherche.clicked.connect(self.afficheRecherche)
        self.bHeros.clicked.connect(self.afficheHeros)
        self.bArmGarn.clicked.connect(self.afficheArmeeGarnison)

    def keyPressEvent(self, event):
        "Methode pour les racourcis clavier de l'interfaces"

        key = event.key()
        if key == Qt.Key_Escape:  # Permet de fermer le menus quand on clique sur esc
            self.hide()
            # Redonne ensuite le focus au widget de la ville
            self.viewer.setFocus()
        else:
            print(key)

    def mousePressEvent(self, event):
        "Methode reimplementant le mousePressEvent"

        if (event.x() > 100 and event.x() < self.largeur - 100 and event.y() > 100 and event.y() < self.hauteur - 100):  # Ne fait rien si on clique dans la zone
            return None
        self.hide()
        # Redonne ensuite le focus au viewer
        self.viewer.setFocus()

    def show(self):
        "Methode pour reimplementer le show()"

        super(wVille, self).show()
        self.afficheInfo()

    def setVille(self, ville):
        "Methode pour mettre a jour la ville dans les differents widgets"

        self.ville = ville
        # Pas de setVille pour le wInfo, deja compris dans le show()
        self.wDecrets.setVille(ville)
        self.wRecherche.setVille(ville)
        self.wCV.setVille(ville)
        self.wUnif.setVille(ville)
        self.wInf.setVille(ville)
        self.wCav.setVille(ville)
        self.wArt.setVille(ville)
        self.wMurs.setVille(ville)
        self.wMarch.setVille(ville)
        self.wEntr.setVille(ville)

    def afficheCV(self):
        "Methode pour afficher le widget du centre-ville"

        self.cacher()
        self.wCV.show()
        self.wCV.setFocus()

    def afficheUnif(self):
        "Methode pour afficher le widget de l'unif"

        self.cacher()
        self.wUnif.show()
        self.wUnif.setFocus()

    def afficheInf(self):
        "Methode pour afficher le widget de l'infenterie"

        self.cacher()
        self.wInf.show()
        self.wInf.setFocus()

    def afficheCav(self):
        "Methode pour afficher le widget de la cavalerie"

        self.cacher()
        self.wCav.show()
        self.wCav.setFocus()

    def afficheArt(self):
        "Methode pour afficher le widget de l'artillerie"

        self.cacher()
        self.wArt.show()
        self.wArt.setFocus()

    def afficheMurs(self):
        "Methode pour afficher le widget des murs"

        self.cacher()
        self.wMurs.show()
        self.wMurs.setFocus()

    def afficheMarch(self):
        "Methode pour afficher le widget du cartier marchand"

        self.cacher()
        self.wMarch.show()
        self.wMarch.setFocus()

    def afficheEntr(self):
        "Methode pour afficher le widget des entrepots"

        self.cacher()
        self.wEntr.show()
        self.wEntr.setFocus()

    def afficheCred(self):
        "Methode pour afficher le widget du cartier du credo"

        self.cacher()
        self.wCred.show()
        self.wCred.setFocus()

    def afficheInfo(self):
        "Methode pour afficher le widget avec les infos sur la ville"

        self.cacher()
        self.wInfo.show()
        self.wInfo.setFocus()

    def afficheDecret(self):
        "Methode pour afficher le widget des decrets"

        self.cacher()
        self.wDecrets.show()
        self.wDecrets.setFocus()

    def afficheRecherche(self):
        "Methode pour afficher le widget des recherches"

        self.cacher()
        self.wRecherche.show()
        self.wRecherche.setFocus()

    def afficheHeros(self):
        "Methode pour afficher le widget des heros"

        self.cacher()

    def afficheArmeeGarnison(self):
        "Methode pour afficher le widget de l'armee en garnison"

        self.cacher()

    def cacher(self):
        "Methode pour hide() tous les widgets"

        # Les cartiers
        self.wCV.hide()
        self.wUnif.hide()
        self.wInf.hide()
        self.wCav.hide()
        self.wArt.hide()
        self.wMurs.hide()
        self.wMarch.hide()
        self.wEntr.hide()
        self.wCred.hide()

        # Les autres
        self.wInfo.hide()
        self.wDecrets.hide()
        self.wRecherche.hide()
