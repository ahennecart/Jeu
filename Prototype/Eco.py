from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QFrame, QPushButton, QLabel, QSlider
from PyQt5.QtCore import Qt
from ClassWidget import LCD


class Eco(QWidget):
    "Classe permettant de creer le widge de l'econnomie"

    def __init__(self, largeur, hauteur, viewer, parent=None):
        super(Eco, self).__init__(parent=parent)
        self.largeur = largeur
        self.hauteur = hauteur
        self.viewer = viewer
        self.parent = parent

        self.setGeometry(0, 0, largeur, hauteur)
        self.fond = QFrame(self)
        self.fond.setStyleSheet("QFrame {background-color:white; color:darkblue}")
        self.fond.setGeometry(0, 0, largeur, hauteur)

        # boton pour quitter vers la carte
        self.boutQuit = QPushButton(self)
        self.boutQuit.setGeometry(self.largeur - 50, 0, 50, 50)
        self.boutQuit.setText("EXIT")
        self.boutQuit.clicked.connect(self.quitter)

        # Label de titre de la fenetre   /!\ modifier la taille de la police
        self.labTitre = QLabel(self)
        self.labTitre.setGeometry(self.largeur / 2 - 100, 20, 200, 50)
        self.labTitre.setText("Revenus de la faction")
        self.labTitre.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        # label de titre de la collone des revenus
        self.labRev = QLabel(self)
        self.labRev.setGeometry(self.largeur / 4, 90, 200, 50)
        self.labRev.setText("Revenus")
        self.labRev.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.labDep = QLabel(self)
        self.labDep.setGeometry(self.largeur / 4 * 3, 90, 200, 50)
        self.labDep.setText("Dépenses")
        self.labDep.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.labTaxe = QLabel(self)
        self.labTaxe.setGeometry(30, 90 + 1 * 20 + 1 * 50, 200, 50)
        self.labTaxe.setText("Revenus des taxes")
        self.labTaxe.setAlignment(Qt.AlignVCenter)

        self.labEch = QLabel(self)
        self.labEch.setGeometry(30, 90 + 2 * 20 + 2 * 50, 200, 50)
        self.labEch.setText("Revenus des échanges commerciaux")
        self.labEch.setAlignment(Qt.AlignVCenter)

        self.labRevAccords = QLabel(self)
        self.labRevAccords.setGeometry(30, 90 + 3 * 20 + 3 * 50, 200, 50)
        self.labRevAccords.setText("Revenus des accords diplomatiques")
        self.labRevAccords.setAlignment(Qt.AlignVCenter)

        self.labRevAutre = QLabel(self)
        self.labRevAutre.setGeometry(30, 90 + 4 * 20 + 4 * 50, 200, 50)
        self.labRevAutre.setText("Autres revenus")
        self.labRevAutre.setAlignment(Qt.AlignVCenter)

        self.labArmee = QLabel(self)
        self.labArmee.setGeometry(50 + self.largeur / 2, 90 + 1 * 20 + 1 * 50, 200, 50)
        self.labArmee.setText("Dépenses dues aux armées")
        self.labArmee.setAlignment(Qt.AlignVCenter)

        self.labMarine = QLabel(self)
        self.labMarine.setGeometry(50 + self.largeur / 2, 90 + 2 * 20 + 2 * 50, 200, 50)
        self.labMarine.setText("Dépenses dues à la marine")
        self.labMarine.setAlignment(Qt.AlignVCenter)

        self.labDepAccords = QLabel(self)
        self.labDepAccords.setGeometry(50 + self.largeur / 2, 90 + 3 * 20 + 3 * 50, 200, 50)
        self.labDepAccords.setText("Dépenses dues aux accords diplomatiques")
        self.labDepAccords.setAlignment(Qt.AlignVCenter)

        self.labDepAutre = QLabel(self)
        self.labDepAutre.setGeometry(50 + self.largeur / 2, 90 + 4 * 20 + 4 * 50, 200, 50)
        self.labDepAutre.setText("Autres dépenses")
        self.labDepAutre.setAlignment(Qt.AlignVCenter)

        self.labTotalRev = QLabel(self)
        self.labTotalRev.setGeometry(30, 500, 200, 50)
        self.labTotalRev.setText("Total des revenus")
        self.labTotalRev.setAlignment(Qt.AlignVCenter)

        self.labTotalDep = QLabel(self)
        self.labTotalDep.setGeometry(50 + self.largeur / 2, 500, 200, 50)
        self.labTotalDep.setText("Total des dépenses")
        self.labTotalDep.setAlignment(Qt.AlignVCenter)

        self.revProchTour = QLabel(self)
        self.revProchTour.setGeometry(20, self.hauteur - 100, 200, 50)
        self.revProchTour.setText("Revenus au prochain tour")
        self.revProchTour.setAlignment(Qt.AlignVCenter)

        self.LCDTaxe = LCD(self.largeur / 2 - 100, 90 + 1 * 20 + 1 * 50, 100, 50, self)
        self.LCDTaxe.setStyleSheet("Color : green")

        self.LCDEch = LCD(self.largeur / 2 - 100, 90 + 2 * 20 + 2 * 50, 100, 50, self)
        self.LCDEch.setStyleSheet("Color : green")

        self.LCDRevAccords = LCD(self.largeur / 2 - 100, 90 + 3 * 20 + 3 * 50, 100, 50, self)
        self.LCDRevAccords.setStyleSheet("Color : green")

        self.LCDRevAutre = LCD(self.largeur / 2 - 100, 90 + 4 * 20 + 4 * 50, 100, 50, self)
        self.LCDRevAutre.setStyleSheet("Color : green")

        self.LCDArmee = LCD(self.largeur - 120, 90 + 1 * 50 + 1 * 20, 100, 50, self)
        self.LCDArmee.setStyleSheet("Color : red")

        self.LCDMarine = LCD(self.largeur - 120, 90 + 2 * 50 + 2 * 20, 100, 50, self)
        self.LCDMarine.setStyleSheet("Color : red")

        self.LCDDepAccords = LCD(self.largeur - 120, 90 + 3 * 50 + 3 * 20, 100, 50, self)
        self.LCDDepAccords.setStyleSheet("Color : red")

        self.LCDDepAutres = LCD(self.largeur - 120, 90 + 4 * 50 + 4 * 20, 100, 50, self)
        self.LCDDepAutres.setStyleSheet("Color : red")

        self.LCDTotalRev = LCD(self.largeur / 2 - 100, 500, 100, 50, self)
        self.LCDTotalRev.setStyleSheet("Color : green")

        self.LCDTotalDep = LCD(self.largeur - 120, 500, 100, 50, self)
        self.LCDTotalDep.setStyleSheet("Color : red")

        self.LCDRevProchTour = LCD(self.largeur / 2 - 100, self.hauteur - 100, 100, 50, self)

        self.sliderTaxe = QSlider(Qt.Horizontal, self)
        self.sliderTaxe.setGeometry(self.largeur / 2 + 50, self.hauteur - 100, self.largeur / 2 - 100, 50)
        self.sliderTaxe.setMaximum(4)
        self.sliderTaxe.setMinimum(0)

        self.sliderTaxe.valueChanged.connect(self.slider)

        self.hide()

    def show(self):
        "Methode re-implemantant show pour permettre de faire aussi une mis a jour du widget"

        self.maj()
        super(Eco, self).show()

    def maj(self):
        "Methode pour maj les LCD"

        # On met le slider a la bonne position
        self.sliderTaxe.setSliderPosition((self.parent.joueurEnCour.taxe - 0.5) * 4)
        # On maj les LCD
        self.LCDEch.display(self.parent.joueurEnCour.revenusEchanges())
        self.LCDRevAccords.display(self.parent.joueurEnCour.revenusAccords())
        self.LCDRevAutre.display(self.parent.joueurEnCour.revenusAutres())
        self.LCDArmee.display(self.parent.joueurEnCour.depArmee())
        self.LCDMarine.display(self.parent.joueurEnCour.depMarine())
        self.LCDDepAccords.display(self.parent.joueurEnCour.depAccords())
        self.LCDDepAutres.display(self.parent.joueurEnCour.depAutres())
        self.majTaxe()

    def majTaxe(self):
        "Methode pour mettre a jour uniquement les LCD qui changenet avec les taxes (utile pour ne maj que ca lors du mouvement du slider"

        self.LCDTaxe.display(self.parent.joueurEnCour.revenusTaxes())
        self.majRevFinal()

    def majRevFinal(self):
        "Methode pour calculer le revenus final et maj le LCD correspondant"

        revenus = self.LCDTaxe.value() + self.LCDRevAutre.value() + self.LCDRevAccords.value() + self.LCDEch.value()
        depenses = - self.LCDArmee.value() + self.LCDMarine.value() + self.LCDDepAccords.value() + self.LCDDepAutres.value()
        self.LCDTotalRev.display(revenus)
        self.LCDTotalDep.display(depenses)
        self.LCDRevProchTour.display(revenus - depenses)

    def quitter(self):
        "Methode pour retourner sur la carte"
        self.hide()
        self.viewer.show()
        self.viewer.setFocus()

    def slider(self, valeur):
        "Methode du slider"
        print(valeur / 4 + 0.5)
        self.parent.joueurEnCour.taxe = valeur / 4 + 0.5
        self.majTaxe()

    def keyPressEvent(self, event):
        "Methode pour les racourcis clavier de l'interfaces"

        key = event.key()
        if key == QtCore.Qt.Key_Escape:  # Permet de fermer le menus quand on clique sur esc
            self.quitter()
        else:
            print(key)
