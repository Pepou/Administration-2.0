# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QMainWindow


from GUI.Ui_connexion2 import Ui_MainWindow

from config import Config

class Connexion(QMainWindow, Ui_MainWindow):
    """
    Class pour la saisie du login et mot de passe et connexion a la bdd
    elle modifie la class config ou l'engin sqlachemy est.
    """
    
    signalfermeture = pyqtSignal()
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        #connection
        self.password.returnPressed.connect(self.buttonBox_2.accepted)
        

        
    @pyqtSlot()
    def on_buttonBox_2_accepted(self):
        """
        Connexion à la base
        """
        # acces à la BDD
#        try:
#        self.close()
        login = self.login.text()
        password = self.password.text()
        
        Config.modif_engine(login,password)
        
        self.signalfermeture.emit() 

        
        
        
#        self.admin = MainWindow(engine, self.meta, login, password)
#
#        
#        self.admin.showMaximized()
#        self.close()   
        
#        return login, password
#        except exc.SQLAlchemyError:
#            QMessageBox.information(self, 
#                ("Erreur connexion "), 
#                ("Erreur sur le login et/ou mot de passe")) 
#            self.show()
#        

    
    @pyqtSlot()
    def on_buttonBox_2_rejected(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.close()
    
