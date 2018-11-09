# -*- coding: utf-8 -*-

"""
Module implementing Creation_Instrument.
"""

from PyQt4.QtCore import pyqtSlot, Qt, pyqtSignal, QRunnable, QObject, QThreadPool, QMutex
from PyQt4.QtGui import QDialog, QFileDialog, QTableWidgetItem, QStandardItem, QStandardItemModel, QMessageBox
#import unicodedata
from config import Config
from Package.AccesBdd import Instrument, Client, Secteur_exploitation, Poste_tech_sap

from .Ui_Creation_Instruments import Ui_Creation_Instrument
import pandas as pd

class Creation_Instrument(QDialog, Ui_Creation_Instrument):
    """
    Class documentation goes here.
    """
    
    signal_Creation_ok = pyqtSignal()
    
    def __init__(self, engine, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
#        self.engine = engine
        self.threadpool = QThreadPool()
        
        #recuperation des tables
        
        bdd_thread_instrum = WorkerDemarrageParc()
        bdd_thread_instrum.signals.signalparc.connect(self.remplissage_combobox_instrums_non_liees)
        bdd_thread_instrum.signals.signaldomaine_mesure.connect(self.comboBox_domaine_mes.addItems)
        bdd_thread_instrum.signals.signaldomaine_designation.connect(self.comboBox_designation.addItems)
        bdd_thread_instrum.signals.signaldomaine_type.connect(self.comboBox_type.addItems)
        bdd_thread_instrum.signals.signaldomaine_commentaire.connect(self.comboBox_commentaire.addItems)
        bdd_thread_instrum.signals.signaldomaine_designation_lit.connect(self.comboBox_designation_litt.addItems)
        bdd_thread_instrum.signals.signaldomaine_constructeur.connect(self.comboBox_constructeur.addItems)
        bdd_thread_instrum.signals.signaldomaine_ref_constructeur.connect(self.comboBox_ref_constructeur.addItems)
        
        bdd_thread_instrum.signals.signalclassinstrum.connect(self.mise_dispo_instrument)
        
        self.threadpool.start(bdd_thread_instrum)
        
#        self.class_instrument = Instrument(engine)
#        parc = self.class_instrument.parc_complet()
        bdd_thread_secteur_poste_tech = WorkerDemarrageSecteurPosteTech()
        bdd_thread_secteur_poste_tech.signals.signaltable_secteur.connect(self.mise_dispo_table_secteur)
        bdd_thread_secteur_poste_tech.signals.signaltable_poste_tech_sap.connect(self.mise_dispo_poste_tech)
        
        self.threadpool.start(bdd_thread_secteur_poste_tech)
        
        
        bdd_thread_clients = WorkerDemarrageClients()                
        bdd_thread_clients.signals.signaltableclients.connect(self.mise_dispo_clients)
        bdd_thread_clients.signals.signalensemble_entites_clients.connect(self.ensemble_clients)
        bdd_thread_clients.signals.signalclients.connect(self.comboBox_client.addItems)
        
        
        self.threadpool.start(bdd_thread_clients)
        
#        self.classe_clients = Client(engine)
#        self.clients = self.classe_clients.ensemble_entites_clients()
        

#        clients_tries = self.clients.sort_values(by = "ID_ENT_CLIENT")       
#        self.comboBox_client.addItems(clients_tries["ABREVIATION"].tolist())

        
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
    @pyqtSlot(Instrument)
    def mise_dispo_instrument(self, classinstrum):        
        self.class_instrument = classinstrum
    
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
        
#        print(self.classe_clients.ensemble_sites_clients())
        
        
#        self.comboBox_affectation.clear()
#        abreviation_siege = self.comboBox_client.currentText()
#        id_siege = int(self.clients[self.clients.ABREVIATION == abreviation_siege].ID_ENT_CLIENT.values[0])
##            print(f"id_siege {id_siege}")
#        sites_clients = self.classe_clients.ensemble_sites_clients()
#        sites_clients_tries = sites_clients[sites_clients.ID_ENT_CLIENT == id_siege].sort_values(by = "ID_CLIENTS") 
#
#        self.comboBox_affectation.addItems(sites_clients_tries["CODE_CLIENT"].tolist())
        
        
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
        
    

    
    
    def keyPressEvent(self, event):
        pass
#        print(f"coucou {event}")
#    def closeEvent(self, event):
#        print("coucou je me casse")
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        nbr_ligne = self.tableWidget.rowCount()-1
        nbr_colonne =self.tableWidget.columnCount()
#        print(f"nbr ligne {nbr_ligne}")
        list_dictionnaire = []
        list_non_enregistree = []
        
        for num_ligne in range(nbr_ligne, -1, -1):
#            print(f"boucle {num_ligne}")
            
            #test valeurs None sur CODE,DOMAINE de mesure,Designation:
            try:
                code = self.tableWidget.item(num_ligne,10).text()
                domaine_mesure= self.tableWidget.item(num_ligne,5).text()
                designation = self.tableWidget.item(num_ligne,7).text()
                
                if code!= "None" and domaine_mesure != "None" and designation !="None":
                    dict_ligne = {}
                    for num_colonne in range(nbr_colonne):
    
                        if self.tableWidget.item(num_ligne,num_colonne):
                            if self.tableWidget.horizontalHeaderItem(num_colonne).text() == "RESOLUTION":
                                dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = float(self.tableWidget.item(num_ligne,num_colonne).text())
                            elif self.tableWidget.horizontalHeaderItem(num_colonne).text() == "REF_INSTRUMENT":
                                try:
                                    dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = int(self.tableWidget.item(num_ligne,num_colonne).text())
                                except:
                                    dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = None
                            elif self.tableWidget.horizontalHeaderItem(num_colonne).text() == "INSTRUMENT_LIE":
                                try:
                                    dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = True
                                except:
                                    dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = False
                                
                            else:
                                dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = self.tableWidget.item(num_ligne,num_colonne).text()
                            
    
                        else:
                            dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = None
                    list_dictionnaire.append(dict_ligne)
                    
                    self.tableWidget.removeRow(num_ligne)
                
                else:
                    dict_ligne = {}
                    for num_colonne in range(nbr_colonne):
    
                        if self.tableWidget.item(num_ligne,num_colonne):
                            if self.tableWidget.horizontalHeaderItem(num_colonne).text() == "RESOLUTION":
                                dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = float(self.tableWidget.item(num_ligne,num_colonne).text())
                            elif self.tableWidget.horizontalHeaderItem(num_colonne).text() == "REF_INSTRUMENT":
                                try:
                                    dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = int(self.tableWidget.item(num_ligne,num_colonne).text())
                                except:
                                    dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = None                        
                            else:
                                dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = self.tableWidget.item(num_ligne,num_colonne).text()
                        
                        else:
                            dict_ligne[self.tableWidget.horizontalHeaderItem(num_colonne).text()] = None
                    list_non_enregistree.append(dict_ligne)
                    
            except :                
                pass
                QMessageBox.critical(self, 
                    self.trUtf8("Client"), 
                    self.trUtf8("La mise a jour n'a pu etre realisée"))
        
        
        if len(list_dictionnaire) == 1:
           self.class_instrument.creation_instrum_unique(list_dictionnaire[0])        
        
        elif len(list_dictionnaire) > 1:
            self.class_instrument.creation_instrums_multi(list_dictionnaire)
        

                
        if self.tableWidget.rowCount()== 0 :
            self.close()
            self.signal_Creation_ok.emit()
        
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        """
        Slot documentation goes here.
        """
        self.close()
    
    @pyqtSlot()
    def on_pushButton_open_file_clicked(self):
        """
        Slot documentation goes here.
        """
        colonne_table_instru = ["IDENTIFICATION", "RESOLUTION","N_SERIE","CONSTRUCTEUR", "REFERENCE_CONSTRUCTEUR",
                                "DOMAINE_MESURE", "FAMILLE", "DESIGNATION", "TYPE", 
                                "DESIGNATION_LITTERALE","CODE", "SITE", "AFFECTATION", "SOUS_AFFECTATION", 
                                "LOCALISATION",  "N_SAP_PM", "COMMENTAIRE", "ETAT_UTILISATION", "INSTRUMENT_LIE", "REF_INSTRUMENT", 
                                "N_EQUIPEMENT"]

        fichier = QFileDialog.getOpenFileNames(self, "Choisir le fichier de donnees")#, "y:/1.METROLOGIE/1EBRO-1 FD5/")
        
        if fichier:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)

            

            if self.comboBox_type_fichier.currentText()== "Optimu":
                self.df = pd.read_excel(fichier[0], 0, 0)
                
                colonnes = {"Code":"CODE", "Identification":"IDENTIFICATION", "Désignation":"DESIGNATION", 
                            "Type":"TYPE", "Désignation littérale":"DESIGNATION_LITTERALE",
                            "État d'utilisation": "ETAT_UTILISATION", "Site":"SITE", 
                            "Affectation":"AFFECTATION", "Sous-affectation":"SOUS_AFFECTATION", 
                            "Constructeur":"CONSTRUCTEUR", "Référence constructeur":"REFERENCE_CONSTRUCTEUR", 
                            "N° de série":"N_SERIE"} 

                self.df.rename(columns = colonnes, inplace = True)
#                print(self.df)
                colonne_a_supp = [x for x in list(self.df) if x not in colonne_table_instru]
                self.df.drop(colonne_a_supp, inplace=True, axis=1)
#                print(self.df)
#                self.df.
            
            
            
            else:#cas de SAP                
                ###formules de conversion pandas                
                def nom_famille(abreviation):
                    try:
                        return self.dict_famille[abreviation]
                    except:
                        pass  
                        
                def secteur(num):
                    try:
                        value = self.table_secteur.return_nom_secteur(int(num))
                        return next(value)
                    except:
                        return None
                        pass
                
                def recherche_client(localisation):
#                    print(localisation)
                    if len(localisation.split("-")) >= 3:
                        poste_tech = str(localisation.split("-")[0]) + "-" + str(localisation.split("-")[1]) + "-" + str(localisation.split("-")[2])
#                        print(poste_tech)
                        site = self.table_poste_tech_sap.recherche_designation_by_post_tech(poste_tech)
                        try:
                            return next(site)
                        except:
                            return None
                        site.close()
                    else:
                        pass
                
                def recherche_code_client(localisation):
                    if len(localisation.split("-")) >= 3:
                        poste_tech = str(localisation.split("-")[0]) + "-" + str(localisation.split("-")[1]) + "-" + str(localisation.split("-")[2])
                        code_client = self.classe_clients.recherche_code_client_by_post_tech(poste_tech)
                        try:
                            return next(code_client)
                        except:
                            return None

                    else:
                        pass
                
                ######
                
                colonnes = {"N° inventaire":"IDENTIFICATION", "Dom.activité":"CODE", "Type d'objet":"FAMILLE", 
                            "Désignation":"DESIGNATION_LITTERALE", "Fournisseur":"CONSTRUCTEUR",
                            "Désignat. type": "REFERENCE_CONSTRUCTEUR", "Poste technique":"LOCALISATION", 
                            "Désignation.1":"SOUS_AFFECTATION", "N° série fabr.":"N_SERIE", 
                            "Statut util.":"ETAT_UTILISATION", "Equipement":"N_EQUIPEMENT"}            
            

                self.df = pd.read_excel(fichier[0], 0, 0)
                self.df.rename(columns = colonnes, inplace = True)
                
                self.df["N_SAP_PM"]=self.df["IDENTIFICATION"]

                self.df["FAMILLE"]= self.df["FAMILLE"].apply(lambda nom : nom_famille(nom))
                
                self.df["AFFECTATION"]= self.df["Sect.d'exploit."].apply(lambda num : secteur(num))
                self.df["SITE"] = self.df["LOCALISATION"].apply(lambda loca : recherche_client(str(loca)))
                self.df["CODE"] = self.df["LOCALISATION"].apply(lambda loca : recherche_code_client(str(loca)))
                
            try :
                self.df["RESOLUTION"]     
            except KeyError:
                self.df["RESOLUTION"] = 0.1
            try :
                self.df["DOMAINE_MESURE"]     
            except KeyError:
                self.df["DOMAINE_MESURE"] = None
                
            try :
                self.df["DESIGNATION"]     
            except KeyError:
                self.df["DESIGNATION"] = None
            
            self.df.dropna(axis=0, how='any', subset = ["IDENTIFICATION"], inplace = True)

            numero_colonne = 0
            for colonne in colonne_table_instru:
#                print(numero_colonne)
                self.tableWidget.insertColumn(numero_colonne)
                self.tableWidget.setHorizontalHeaderItem(numero_colonne, QTableWidgetItem(colonne))
                
                try:
                    numero_ligne = 0                    
                    for ele in self.df[colonne]:                        
                        if numero_colonne == 0:
                            self.tableWidget.insertRow(numero_ligne)
                        if colonne in ["CODE", "DOMAINE_MESURE", "FAMILLE", "DESIGNATION", "DESIGNATION_LITTERALE", "CONSTRUCTEUR", "REFERENCE_CONSTRUCTEUR"]:
                            self.tableWidget.setItem(numero_ligne, numero_colonne, QTableWidgetItem(str(ele).upper()))
                        else:
                            self.tableWidget.setItem(numero_ligne, numero_colonne, QTableWidgetItem(str(ele)))
                        
                        if( not ele or ele == "None") and (colonne == "CODE" or colonne == "DOMAINE_MESURE" or colonne == "DESIGNATION"):
                            self.tableWidget.item(numero_ligne, numero_colonne).setBackground(Qt.darkYellow)
                        
                        numero_ligne += 1
                    numero_colonne += 1
                except KeyError:
                    
                    numero_colonne += 1
                    
                
                
    @pyqtSlot()
    def on_pushButton_plus_clicked(self):
        """
        Slot documentation goes here.
        """
        nbr_ligne = self.tableWidget.rowCount()
#        print(nbr_ligne)
        self.tableWidget.insertRow(nbr_ligne)
        colonne_table_instru = ["IDENTIFICATION", "RESOLUTION","N_SERIE","CONSTRUCTEUR", "REFERENCE_CONSTRUCTEUR",
                                "DOMAINE_MESURE", "FAMILLE", "DESIGNATION", "TYPE", 
                                "DESIGNATION_LITTERALE","CODE", "SITE", "AFFECTATION", "SOUS_AFFECTATION", 
                                "LOCALISATION",  "N_SAP_PM", "COMMENTAIRE", "ETAT_UTILISATION", "INSTRUMENT_LIE", "REF_INSTRUMENT"]
        
        if nbr_ligne == 0:
            num_colonne = 0
            for nom_colonne in colonne_table_instru:
                self.tableWidget.insertColumn(num_colonne)
                self.tableWidget.setHorizontalHeaderLabels (list(colonne_table_instru))
                num_colonne += 1
    
    
        #remplissage:
        
        dict_questionnaire = {"CODE": self.comboBox_affectation.currentText(),
                            "AFFECTATION":self.comboBox_localisation.currentText(),
                            "DOMAINE_MESURE": self.comboBox_domaine_mes.currentText().upper(),
                            "FAMILLE": self.comboBox_famille.currentText().upper(), 
                            "DESIGNATION":self.comboBox_designation.currentText().upper(),
                            "TYPE": self.comboBox_type.currentText().upper(),
                            "DESIGNATION_LITTERALE":self.comboBox_designation_litt.currentText(), 
                            "CONSTRUCTEUR":self.comboBox_constructeur.currentText().upper(), 
                            "REFERENCE_CONSTRUCTEUR": self.comboBox_ref_constructeur.currentText().upper(), 
                            "N_SERIE": self.lineEdit_n_serie.text(),
                            "RESOLUTION": self.lineEdit_resolution.text(), 
                            "ETAT_UTILISATION":self.comboBox_etat_util.currentText(), 
                            "REF_INSTRUMENT": self.comboBox_instrument.currentText(), 
                            "COMMENTAIRE": self.comboBox_commentaire.currentText()}
        

        

        
        for colonne in range(self.tableWidget.columnCount()):
#                print(f"n° colonne {colonne}")
            try:
                nom_colonne = self.tableWidget.horizontalHeaderItem(colonne).text()
                value = dict_questionnaire[nom_colonne]
#                print(value)
#                self.tableWidget.setItem(0, colonne, QTableWidgetItem(str(value)))

                
#                    print(f"nom colone {nom_colonne}")
                if nom_colonne == "REF_INSTRUMENT":
#                        print("test0")
                    if self.checkBox_lier.isChecked():
                        value = dict_questionnaire[nom_colonne]
                        self.tableWidget.setItem(nbr_ligne, colonne, QTableWidgetItem(str(value)))
                        self.tableWidget.setItem(0, (colonne-1), QTableWidgetItem(str(True)))
                    else:
                        self.tableWidget.setItem(nbr_ligne, colonne, QTableWidgetItem(str("")))
                        self.tableWidget.setItem(nbr_ligne, (colonne-1), QTableWidgetItem(str(False)))
                
                elif nom_colonne == "CODE":
                    value = dict_questionnaire[nom_colonne]
#                        print(value)
                    self.tableWidget.setItem(nbr_ligne, colonne, QTableWidgetItem(str(value)))                        
                    sites_clients = self.classe_clients.ensemble_sites_clients()
                    nom_site = sites_clients[sites_clients.CODE_CLIENT == value].VILLE.values[0]
                    
                    self.tableWidget.setItem(nbr_ligne, 11, QTableWidgetItem(str(nom_site)))
                else:                            
                    value = dict_questionnaire[nom_colonne]
#                    print(f"value {value}")
                    self.tableWidget.setItem(nbr_ligne, colonne, QTableWidgetItem(str(value)))
                
                
    
    
            except:
                pass
            
    
    @pyqtSlot()
    def on_pushButton_moins_clicked(self):
        """
        Slot documentation goes here.
        """
        lignes = self.tableWidget.selectedIndexes()         
        
        list_n_lignes = list(set([item.row() for item in lignes]))
        list_n_lignes.sort()
#        print(list_n_lignes)
        
        for ele in reversed(list_n_lignes):
            self.tableWidget.removeRow(ele)
        
        
#    @pyqtSlot()
#    def on_groupBox_fichier_clicked(self):
#        """
#        Slot documentation goes here.
#        """
#        if self.groupBox_fichier.isChecked():
#            self.groupBox_manuel.setChecked(False)
#        else:
#            self.groupBox_manuel.setChecked(True)
    
    @pyqtSlot()
    def on_groupBox_manuel_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.groupBox_manuel.isChecked():
            self.groupBox_fichier.setChecked(False)
        else:
            self.groupBox_fichier.setChecked(True)
    
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
                        value = dict_questionnaire[nom_colonne]
#                        print(value)
                        self.tableWidget.setItem(ligne, colonne, QTableWidgetItem(str(value)))                        
                        sites_clients = self.classe_clients.ensemble_sites_clients()
                        nom_site = sites_clients[sites_clients.CODE_CLIENT == value].VILLE.values[0]
                        self.tableWidget.setItem(ligne, 11, QTableWidgetItem(str(nom_site)))
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
#        print(index)
#        if index !=0:
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
#        except AttributeError:
#            pass
#    
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
        parc = class_instrument.parc_complet()        
        
        self.signals.signalparc.emit(parc)
        self.signals.signalclassinstrum.emit(class_instrument)
        

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
        print(f"type {type(clients)}")
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
        
    signalclassinstrum = pyqtSignal(Instrument)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
