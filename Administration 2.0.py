#-*- coding: utf-8 -*-
from PyQt4 import QtGui

import sys
#from GUI.Exploitation_enregistreurs import Exploitation_enregistreurs
#from GUI.connexion2 import Connexion
from GUI.Main_Administration import MainWindow

if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.showMaximized()    
#    myapp.hide()
    sys.exit(app.exec_())


    



