# -*- coding: utf-8 -*-

"""
Module implementing Modification_Instrument.
"""
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QThreadPool, QRunnable, QObject, QMutex
    
from PyQt4.QtGui import QDialog, QTableWidgetItem, QStandardItem, QStandardItemModel
#import unicodedata

from Package.AccesBdd import Instrument, Client, Secteur_exploitation, Poste_tech_sap

import pandas as pd

from .Ui_Modification_Instruments import Ui_Modification_Instrument

from config import Config


class Modification_Instrument(QDialog, Ui_Modification_Instrument):
    """
    Class documentation goes here.
    """

    
    signal_modification_ok = pyqtSignal()    
    closeApp = pyqtSignal()    
    
    
    def __init__(self, mainwindow, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
        self.mainwindow = mainwindow
#        print(self.mainwindow.parc)
        self.demarage()
        
    def demarage(self):

        #signaux vers la mainwindows
        self.mainwindow.signal_nvlle_recherche.connect(self.nvlle_recherche) 
        
#        self.fct_remplissage(self.mainwindow)
#        
        self.mainwindow.signal_parc_a_modi.connect(self.fonction_remplissage_tableau_instrums_a_modif)

        self.threadpool = QThreadPool()
        
        #recuperation des tables
        
#        thread_parc_a_modif = WorkerDemarragefctremplissage(self.mainwindow, self.fct_remplissage)
#        thread_parc_a_modif.signals.signalparcmodf.connect(self.fonction_remplissage_tableau_instrums_a_modif)
#        self.threadpool.start(thread_parc_a_modif)
        
        bdd_thread_instrum = WorkerDemarrageParc()
        bdd_thread_instrum.signals.signalparc.connect(self.remplissage_combobox_instrums_non_liees)
        bdd_thread_instrum.signals.signaldomaine_mesure.connect(self.comboBox_domaine_mes.addItems)
        bdd_thread_instrum.signals.signaldomaine_designation.connect(self.comboBox_designation.addItems)
        bdd_thread_instrum.signals.signaldomaine_type.connect(self.comboBox_type.addItems)
        bdd_thread_instrum.signals.signaldomaine_commentaire.connect(self.comboBox_commentaire.addItems)
        bdd_thread_instrum.signals.signaldomaine_designation_lit.connect(self.comboBox_designation_litt.addItems)
        bdd_thread_instrum.signals.signaldomaine_constructeur.connect(self.comboBox_constructeur.addItems)
        bdd_thread_instrum.signals.signaldomaine_ref_constructeur.connect(self.comboBox_ref_constructeur.addItems)
        bdd_thread_instrum.signals.signalclasseinstrum.connect(self.affect_class_instrument)
        
        self.threadpool.start(bdd_thread_instrum)
        

        bdd_thread_secteur_poste_tech = WorkerDemarrageSecteurPosteTech()
        bdd_thread_secteur_poste_tech.signals.signaltable_secteur.connect(self.mise_dispo_table_secteur)
        bdd_thread_secteur_poste_tech.signals.signaltable_poste_tech_sap.connect(self.mise_dispo_poste_tech)
        
        self.threadpool.start(bdd_thread_secteur_poste_tech)
        
        
        bdd_thread_clients = WorkerDemarrageClients()                
        bdd_thread_clients.signals.signaltableclients.connect(self.mise_dispo_clients)
        bdd_thread_clients.signals.signalensemble_entites_clients.connect(self.ensemble_clients)
        bdd_thread_clients.signals.signalclients.connect(self.comboBox_client.addItems)
                
        self.threadpool.start(bdd_thread_clients)
        

        
        self.dict_famille = {"AR":"ANEMOMETRE", "AT":"AGITATEUR LABO", "AU":"AUTOCLAVE", "BA":"BALANCE / SYST PESEE", 
                    "BE":"MESURE DE PRESSION", "BM":"BAINS-MARIE", "CF":"CHAMBRE FROIDE", "CH":"MESURE DU TEMPS", 
                    "CN":"CONSERVAT. PLAQUETTE", "CO":"ENCEINTE T°C NEGATIV", "CP":"CENTRI GRDE CAPACITE", 
                    "CT":"CENTRI MOY CAPACITE", "DE":"DECONGELATEURS", "DI":"DISTRIBUTEUR", 
                    "EE":"EQPT ELECTRIQUE", "FG":"FOUR ET BAIN ETALON", "FO":"FOUR", 
                    "HY":"HYGROMETRES", "IN":"ETUVES - INCUBATEURS", 
                    "MC":"REFRIGERAT. DOMESTIQ", "MY":"MATERIEL CRYOGENIQUE", "PG":"POIDS ETALON", 
                    "PI":"PIPETTES", "RT":"ENCEINTE T°C POSITIV", "TH":"THERMOCYCLEUR", 
                    "TM":"MESURE POLYVAL (T°C)", "TN":"TENSIOMETRE", "TO":"TRAITEMENT DE L'EAU", 
                    "TR":"TABLE REFRIGEREE", "TY":"TACHYMETRES", "UC":"ULTRA-CENTRIFUGEUSE"}
        
        list_famille = [self.dict_famille[x] for x in self.dict_famille]
        list_famille.sort()
        self.comboBox_famille.addItems(list_famille)
        
#        self.resize(100,100)
#        self.setWindowFlags(self.windowFlags() |
#                              Qt.WindowSystemMenuHint |
#                              Qt.WindowMinMaxButtonsHint)

#        self.setFixedSize(self.size()) 
        
    def fct_remplissage(self, mainwindows):
        """fct qui va voir sur le tableview du mainwindows"""
        model = mainwindows.tableView_instruments.model()
        id = []
#        print("ca commence")
        for row in range(model.rowCount()):
#            for column in range(model.columnCount()):
            index = model.index(row, 0)
            id.append(int(model.data(index)))
#        print("c'est fini")
        instrument = mainwindows.parc.loc[mainwindows.parc["ID_INSTRUM"].isin(id)]
        return instrument
    
    
        
    def closeEvent(self, evnt):
        """reimplement la fermeture"""    
        self.closeApp.emit()
        

    @pyqtSlot(Instrument)
    def affect_class_instrument(self, cls_instrum):
        mutex = QMutex()
        mutex.lock()
        self.class_instrument = cls_instrum
        mutex.unlock()
    
    def fonction_remplissage_tableau_instrums_a_modif(self, dataframe_instruments):

#        self.tableWidget.setRowCount(0)
        
        self.tableWidget.setColumnCount(dataframe_instruments.shape[1])
        self.tableWidget.setRowCount(dataframe_instruments.shape[0])
#        colonne_name = list(dataframe_instruments.columns)
#        print(colonne_name)
        
#        for j in range(dataframe_instruments.shape[1]):
#            self.tableWidget.setHorizontalHeaderItem(j, QTableWidgetItem(colonne_name[j]))
#            for i in range(dataframe_instruments.shape[0]):                
#                self.tableWidget.setItem(i,j,QTableWidgetItem(str(dataframe_instruments.iloc[i, j])))
#                
#                i += 1
#            j +=1
        
        numero_colonne = 0
        for nom_colonne in list(dataframe_instruments):
#                print(numero_colonne)
#            self.tableWidget.insertColumn(numero_colonne)
            self.tableWidget.setHorizontalHeaderItem(numero_colonne, QTableWidgetItem(nom_colonne))
            numero_ligne=0
            for ele in dataframe_instruments[nom_colonne]:
#                print(ele)
#                print(f"num ligne {numero_ligne} , numero colonne {numero_colonne}")
                if numero_colonne == 0:
#                    self.tableWidget.insertRow(numero_ligne)
                    self.tableWidget.setItem(numero_ligne, numero_colonne, QTableWidgetItem(str(ele)))
                
                else:
                    self.tableWidget.setItem(numero_ligne, numero_colonne, QTableWidgetItem(str(ele)))
                numero_ligne+= 1
            numero_colonne += 1

        
    @pyqtSlot(Secteur_exploitation)
    def mise_dispo_table_secteur(self, table_secteur):        
        self.table_secteur = table_secteur
    
    @pyqtSlot(Poste_tech_sap)
    def mise_dispo_poste_tech(self, poste_tech):        
        self.table_poste_tech_sap = poste_tech
    
    @pyqtSlot(Client)
    def mise_dispo_clients(self, client):        
        mutex = QMutex()
        mutex.lock()
        self.classe_clients = client
        
        mutex.unlock()
        
        
    @pyqtSlot(pd.DataFrame)
    def ensemble_clients(self, ensemble_client):        
        mutex = QMutex()
        mutex.lock()
        self.clients = ensemble_client
        mutex.unlock()
    
    @pyqtSlot(pd.DataFrame)
    def remplissage_combobox_instrums_non_liees(self, parc):
        """fct qui recupere le signal et rempli le combobox"""
        
        instrums_non_lies = parc[(parc["ETAT_UTILISATION"] != True)]
#        print(instrums_non_lies)
        
        self.comboBox_instrument.installEventFilter(self)
        model = QStandardItemModel()

        for i,word in enumerate(instrums_non_lies["IDENTIFICATION"]):
            item = QStandardItem(word)
            model.setItem(i, 0, item)

        self.comboBox_instrument.setModel(model)
        self.comboBox_instrument.setModelColumn(0)
    
    
    @pyqtSlot(pd.DataFrame)
    def nvlle_recherche(self, instrums_tries):
        """fct qui est appeléé qd on recherche dans la fenetre principale"""
#        print(instrums_tries)
        self.fonction_remplissage_tableau_instrums_a_modif(instrums_tries)
        
        
    def keyPressEvent(self, event):
        pass

    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        nbr_ligne = self.tableWidget.rowCount()
        nbr_colonne =self.tableWidget.columnCount()
        
        list_dictionnaire = []
        list_non_enregistree = []
        
        for num_ligne in range(nbr_ligne, -1, -1):
            
            #test valeurs None sur CODE,DOMAINE de mesure,Designation:
            try:
                code = self.tableWidget.item(num_ligne,2).text()
                domaine_mesure= self.tableWidget.item(num_ligne,3).text()
                designation = self.tableWidget.item(num_ligne,5).text()
                
                if code!= "None" and domaine_mesure != "None" and designation !="None":
                    dict_ligne = {}
                    for num_colonne in range(nbr_colonne):
    
                        if self.tableWidget.item(num_ligne,num_colonne):
                            dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = self.tableWidget.item(num_ligne,num_colonne).text()
                        else:
                            dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = None
                    list_dictionnaire.append(dict_ligne)
                    
                    self.tableWidget.removeRow(num_ligne)
                
                else:
                    dict_ligne = {}
                    for num_colonne in range(nbr_colonne):
    
                        if self.tableWidget.item(num_ligne,num_colonne):
                            dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = self.tableWidget.item(num_ligne,num_colonne).text()
                        else:
                            dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = None
                    list_non_enregistree.append(dict_ligne)
                    
            except :                
                pass
#                QMessageBox.critical(self, 
#                    self.trUtf8("Client"), 
#                    self.trUtf8("La mise a jour n'a pu etre realisée"))
        

        self.class_instrument.update_instruments(list_dictionnaire)        #####p

                
        if self.tableWidget.rowCount()== 0 :
            self.signal_modification_ok.emit()
            self.tableWidget.setRowCount(0)
#            self.close()
            
        
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        self.close()
    
    

    @pyqtSlot()
    def on_pushButton_maj_clicked(self):
        """
        Slot documentation goes here.
        """

        dict_questionnaire = {"CODE": self.comboBox_affectation.currentText(),
                            "AFFECTATION":self.comboBox_localisation.currentText(),
                            "DOMAINE_MESURE": self.comboBox_domaine_mes.currentText(),
                            "FAMILLE": self.comboBox_famille.currentText(), 
                            "DESIGNATION":self.comboBox_designation.currentText(),
                            "TYPE": self.comboBox_type.currentText(),
                            "DESIGNATION_LITTERALE":self.comboBox_designation_litt.currentText(), 
                            "CONSTRUCTEUR":self.comboBox_constructeur.currentText(), 
                            "REFERENCE_CONSTRUCTEUR": self.comboBox_ref_constructeur.currentText(), 
                            "N_SERIE": self.lineEdit_n_serie.text(),
                            "RESOLUTION": self.lineEdit_resolution.text(), 
                            "ETAT_UTILISATION":self.comboBox_etat_util.currentText(), 
                            "REF_INSTRUMENT": self.comboBox_instrument.currentText(), 
                            "COMMENTAIRE": self.comboBox_commentaire.currentText()}

        list_n_ligne = list(set([item.row() for item in self.tableWidget.selectedIndexes()]))
        list_n_ligne.sort()
        
        list_n_colonne = list(set([item.column() for item in self.tableWidget.selectedIndexes()]))
        list_n_colonne.sort()

        for ligne in list_n_ligne:
            for colonne in list_n_colonne:
#                print(f"n° colonne {colonne}")
                try:
                    nom_colonne = self.tableWidget.horizontalHeaderItem(colonne).text()
#                    print(f"nom colone {nom_colonne}")
                    if nom_colonne == "REF_INSTRUMENT":
#                        print("test0")
                        if self.checkBox_lier.isChecked():
                            value = dict_questionnaire[nom_colonne]
                            self.tableWidget.setItem(ligne, colonne, QTableWidgetItem(str(value)))
                            self.tableWidget.setItem(ligne, (colonne-1), QTableWidgetItem(str(True)))
                        else:
                            self.tableWidget.setItem(ligne, colonne, QTableWidgetItem(str("")))
                            self.tableWidget.setItem(ligne, (colonne-1), QTableWidgetItem(str(False)))
                    
                    elif nom_colonne == "CODE":
                        
                        ###faire boucle pour trouver l'adresse de la colonne "SITE" pas toujour en 11
                        value = dict_questionnaire[nom_colonne]
#                        print(value)
                        self.tableWidget.setItem(ligne, colonne, QTableWidgetItem(str(value)))                        
                        sites_clients = self.classe_clients.ensemble_sites_clients()
                        nom_site = sites_clients[sites_clients.CODE_CLIENT == value].VILLE.values[0]
                        self.tableWidget.setItem(ligne, 10, QTableWidgetItem(str(nom_site)))
                    else:                            
                        value = dict_questionnaire[nom_colonne]
    #                    print(f"value {value}")
                        self.tableWidget.setItem(ligne, colonne, QTableWidgetItem(str(value)))
                except KeyError:
                    pass
#        print(list_n_ligne)
    
    @pyqtSlot()
    def on_checkBox_lier_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.checkBox_lier.isChecked():
            self.comboBox_instrument.setEnabled(True)
            
        else:
            self.comboBox_instrument.setEnabled(False)
    
    @pyqtSlot(int)
    def on_comboBox_client_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        """
        try:
            #gestion des sites
            self.comboBox_affectation.clear()
            abreviation_siege = self.comboBox_client.currentText()
            id_siege = int(self.clients[self.clients.ABREVIATION == abreviation_siege].ID_ENT_CLIENT.values[0])
#            print(f"id_siege {id_siege}")
            sites_clients = self.classe_clients.ensemble_sites_clients()
            sites_clients_tries = sites_clients[sites_clients.ID_ENT_CLIENT == id_siege].sort_values(by = "ID_CLIENTS") 
 
            self.comboBox_affectation.addItems(sites_clients_tries["CODE_CLIENT"].tolist())
        
            #gestion des services
            
        
        except IndexError:
            pass
    
    @pyqtSlot(int)
    def on_comboBox_affectation_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        """
        try:
            self.comboBox_localisation.clear()
            site_client = self.comboBox_affectation.currentText()
#            print(site_client)
            sites_clients = self.classe_clients.ensemble_sites_clients() 
#            print(sites_clients[sites_clients.CODE_CLIENT == site_client])
            id_site = int(sites_clients[sites_clients.CODE_CLIENT == site_client].ID_CLIENTS.values[0])
#            print(f"id site {id_site}")
            services_client = self.classe_clients.ensemble_service_client()
            services_tries = services_client[services_client.ID_CLIENT == id_site].sort_values(by = "ID_SERVICE")
            
#            print(services_tries)
            
            self.comboBox_localisation.addItems(services_tries["ABREVIATION"].tolist())
        
        except IndexError:
            
#            id_site = int(sites_clients[sites_clients.CODE_CLIENT == site_client].ID_CLIENTS.values[0])
#            print(f"id site {id_site}")
            pass

class WorkerDemarrageParc(QRunnable):
    
    def __init__(self, parent= None):
        super(WorkerDemarrageParc, self).__init__()    
        
        self.signals = WorkerSignals()
        
        
    def run(self):
        
        class_instrument = Instrument(Config.engine)
        self.signals.signalclasseinstrum.emit(class_instrument)
#        parc = class_instrument.parc_complet()  
        parc = class_instrument.parc_complet()
#        print(self.parc)
        self.signals.signalparc.emit(parc)
        

        """remplissage combobox domaine mesure"""
        
        domaine_mesure = list(set([x.upper() for x in parc["DOMAINE_MESURE"].tolist() if x]))
        domaine_mesure.sort()
        self.signals.signaldomaine_mesure.emit(domaine_mesure)


        """remplissage combobox domaine mesure"""
        
        designation = list(set([x.upper() for x in parc["DESIGNATION"].tolist() if x]))
        designation.sort()
        self.signals.signaldomaine_designation.emit(designation)

        """remplissage combobox domaine mesure"""
        
        type = list(set([x.upper() for x in parc["TYPE"].tolist() if x]))
        type.sort()
        self.signals.signaldomaine_type.emit(type)
        
        """remplissage combobox commentaire"""
        commentaire = list(set([x.upper() for x in parc["COMMENTAIRE"].tolist() if x]))
        commentaire.sort()
        commentaire.insert(0, "")
        self.signals.signaldomaine_commentaire.emit(commentaire)
        
        """remplissage combobox designation_lit"""
        designation_lit = list(filter(None.__ne__, list(set(parc["DESIGNATION_LITTERALE"].tolist()))))
        designation_lit.sort()
        self.signals.signaldomaine_designation_lit.emit(designation_lit)
#        self.comboBox_designation_litt.addItems(designation_lit)
        
        """remplissage combobox constructeur"""
        constructeur = list(set([x.upper() for x in parc["CONSTRUCTEUR"].tolist() if x]))
        constructeur.sort()
        self.signals.signaldomaine_constructeur.emit(constructeur)
#        self.comboBox_constructeur.addItems(constructeur)
        
        """remplissage combobox ref_constructeur"""
#        ref_constructeur = list(set(parc["REFERENCE_CONSTRUCTEUR"].tolist()))
        ref_constructeur = list(filter(None.__ne__, list(set(parc["REFERENCE_CONSTRUCTEUR"].tolist()))))
        ref_constructeur.sort()
        self.signals.signaldomaine_ref_constructeur.emit(ref_constructeur)
        
#        self.comboBox_ref_constructeur.addItems(ref_constructeur)
        

#class WorkerDemarragefctremplissage(QRunnable):
#    
#    def __init__(self, mainwindow, fct , parent= None):
#        super(WorkerDemarragefctremplissage, self).__init__()    
#        
#        self.signals = WorkerSignals()
#        self.fct = fct
#        self.mainwindow = mainwindow
#    
#    def run(self):
#        
#        parc = self.fct(self.mainwindow)
#        self.signals.signalparcmodf.emit(parc)





class WorkerDemarrageSecteurPosteTech(QRunnable):
    
    def __init__(self, parent= None):
        super(WorkerDemarrageSecteurPosteTech, self).__init__()    
        
        self.signals = WorkerSignals()
        
    def run(self):
        
        table_secteur = Secteur_exploitation(Config.engine)
        self.signals.signaltable_secteur.emit(table_secteur)
        
        table_poste_tech_sap = Poste_tech_sap(Config.engine)
        self.signals.signaltable_poste_tech_sap.emit(table_poste_tech_sap)
        
class WorkerDemarrageClients(QRunnable):
    
    def __init__(self, parent= None):
        super(WorkerDemarrageClients, self).__init__()    
        
        self.signals = WorkerSignals()
        
    def run(self):
        classe_clients = Client(Config.engine)
        self.signals.signaltableclients.emit(classe_clients)
        clients = classe_clients.ensemble_entites_clients()
#        print(f"type {type(clients)}")
        self.signals.signalensemble_entites_clients.emit(clients)
        clients_tries = clients.sort_values(by = "ID_ENT_CLIENT") 
        
          
        self.signals.signalclients.emit(clients_tries["ABREVIATION"].tolist())
        
        
class WorkerSignals(QObject):
    '''
        Gestion des signaux

    '''
    signalparc = pyqtSignal(pd.DataFrame)
    signaldomaine_mesure= pyqtSignal(list)
    signaldomaine_designation = pyqtSignal(list)
    signaldomaine_type = pyqtSignal(list)
    signaldomaine_commentaire = pyqtSignal(list)
    signaldomaine_designation_lit = pyqtSignal(list)
    signaldomaine_constructeur = pyqtSignal(list)
    signaldomaine_ref_constructeur = pyqtSignal(list)
    
    signaltable_secteur = pyqtSignal(Secteur_exploitation)
    signaltable_poste_tech_sap = pyqtSignal(Poste_tech_sap)
    
    signaltableclients = pyqtSignal(Client)
    signalensemble_entites_clients = pyqtSignal(pd.DataFrame)
    signalclients = pyqtSignal(list)
    
    signalintervention = pyqtSignal(pd.DataFrame)
    signalexpeditions = pyqtSignal(pd.DataFrame)
    
    
    signalclasseinstrum = pyqtSignal(Instrument)
        
    signalparcmodf = pyqtSignal(pd.DataFrame)
        
        
        
        
