# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
#from sqlalchemy.engine import create_engine
from PyQt4.QtCore import pyqtSlot, pyqtSignal, Qt, QRunnable, QThreadPool, QObject
from PyQt4.QtGui import QMainWindow
#from PyQt4.QtCore import QT_VERSION_STR
from .Ui_Main_Administration import Ui_MainWindow
from Package.AccesBdd import Instrument, Intervention, Client, Secteur_exploitation, Poste_tech_sap

#import traceback, sys

from GUI.connexion2 import Connexion

from Modules.Indicateurs.GUI.Indicateurs import Indicateur
from Modules.Afficheurs.GUI.afficheurs import Afficheurs

from Modules.Labo_Temp.IHM.Menu import Menu
from Modules.Labo_Temp.Package.GestionBdd import GestionBdd

from Modules.Synchronisation.GUI.Exploitation_enregistreurs import Exploitation_enregistreurs

from Modules.Caracterisation_generateurs_temperature.GUI.Main_Caracterisation import MainCaracterisation

from Modules.Consultation.GUI.Consultation_bdd import Consultation_Bdd

from Modules.Declaration_incertitudes.GUI.Main_Declaration_Incertitudes import MainDeclaration_Incertitudes

from Modules.Polynome.GUI.polynome import Polynome

from Modules.Cartographie.GUI.Main_Carto import Cartographie

from GUI.Instrument.Creation_Instruments import Creation_Instrument
from GUI.Instrument.Modification_Instrument import Modification_Instrument

from GUI.Clients.Creation_Client import Creation_Client
from GUI.Clients.Modification_Entite_Client import Modification_Entite_Client
from GUI.Clients.Modification_Site_Client import Modification_Site_Client

from Modules.Reception_expedition.GUI.Reception_Expedition import ReceptionExpedition


#from sqlalchemy.engine import create_engine
from config import Config

import pendulum
import warnings
#import numpy as np
import pandas as pd
#import json

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    
    signalMAJ_Site_Client = pyqtSignal(object)
    signalMAJ_Service_Client = pyqtSignal(object)
    signal_mise_a_dispo_client_efs = pyqtSignal(list)
    signal_mise_a_dispo_post_tech_sap_efs = pyqtSignal(list)
    signal_mise_a_dispo_poste_tech_efs = pyqtSignal(list)
    signal_nvlle_recherche = pyqtSignal(pd.DataFrame)
    
    signal_parc_a_modi = pyqtSignal(pd.DataFrame)
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        
#        cls.hide()
        #####Ouverture de Connexion 
        self.new_connexion = Connexion(self)
        self.new_connexion.signalfermeture.connect(self.demarrage)
        self.new_connexion.signalfermeture.connect(self.demarrage_bis)
        self.new_connexion.signalfermeture.connect(self.demarrage_tierce)
        self.new_connexion.signalfermeture.connect(self.demarrage_quadri)

        self.new_connexion.setWindowModality(Qt.ApplicationModal)
        self.new_connexion.show()
        
        self.threadpool = QThreadPool()

    
    @pyqtSlot(Instrument)
    def affect_class_instrument(self, cls_instrum):
        """affect class_instrum"""

        self.class_instrum = cls_instrum
    
    
    
    
    @pyqtSlot()
    def demarrage(self):
        """ fonction lancee apres la fermeture de la gui connexion"""
        self.new_connexion.close()
#        self.show()
        self.dateEdit.setDate(pendulum.now('Europe/Paris'))

        self.engine = Config.engine

        self.login = Config.login
        self.password = Config.password
        
        bdd = Config()
        self.meta = bdd.creation_metadata()
        

#        
    @pyqtSlot()
    def demarrage_bis(self):

        bdd_thread_instrum = WorkerDemarrage("instruments")
        bdd_thread_instrum.signals.signalparc.connect(self.tableView_instruments.remplir)
        bdd_thread_instrum.signals.signalparc.connect(self.combobox_colonne_parc)
        bdd_thread_instrum.signals.signalclasseinstrum.connect(self.affect_class_instrument)
        
#        bdd_thread_instrum.start() sub class qthread
        self.threadpool.start(bdd_thread_instrum)
        
    @pyqtSlot()
    def demarrage_tierce(self):
        
        bdd_thread_intervention= WorkerDemarrage("futures_receptions")
        bdd_thread_intervention.signals.signalintervention.connect(self.tableView_reception.remplir)
#        bdd_thread_intervention.start()
        self.threadpool.start(bdd_thread_intervention)
        
    
    @pyqtSlot()
    def demarrage_quadri(self):
#        print(str(self.threadpool.maxThreadCount()))
        bdd_thread_intervention = WorkerDemarrage("expeditions")
        bdd_thread_intervention.signals.signalexpeditions.connect(self.tableView_expedition.remplir)
#        bdd_thread_intervention.start()
        self.threadpool.start(bdd_thread_intervention)
        
        self.groupBox.setChecked(True)
    
    @pyqtSlot(pd.DataFrame)
    def combobox_colonne_parc(self, parc):
        #mise en place pour le tri
        self.parc = parc
        self.comboBox_nom_colonne.addItems(list(self.parc))
        self.comboBox_nom_colonne.setCurrentIndex(1)
        
        
    @pyqtSlot()
    def on_actionLaboTemp_triggered(self):
        """
        Slot documentation goes here.
        """
        db = GestionBdd('db')

        db.premiere_connexion(self.login, self.password)
        
        self.labotemp = Menu()
        self.labotemp.showMaximized()
    
    @pyqtSlot()
    def on_actionSynchronisation_enregisteurs_triggered(self):
        """
        Slot documentation goes here.
        """
        self.exploitation = Exploitation_enregistreurs(self.engine, self.meta)
        self.exploitation.show()
    
    @pyqtSlot()
    def on_actionCaracterisation_Generateurs_triggered(self):
        """
        Slot documentation goes here.
        """
        self.caracterisation = MainCaracterisation(self.engine,self.meta )
        self.caracterisation.showMaximized()
    
    @pyqtSlot()
    def on_actionAfficheurs_triggered(self):
        """
        Slot documentation goes here.
        """
        self.module_afficheur = Afficheurs(self.engine)
#        self.caracterisation_bain = Caracterisation_Bain(self.engine,self.meta )
        
#        self.connect(self.caracterisation_bain, SIGNAL("nouvellecaracterisation_bain(PyQt_PyObject)"), self.initialisation)
        self.module_afficheur.showMaximized()
    
    @pyqtSlot()
    def on_actionIndicateurs_triggered(self):
        """
        Slot documentation goes here.
        """
        bdd = Config()
        meta = bdd.creation_metadata()
        self.module_indicateur = Indicateur(Config.engine, meta)
#        self.caracterisation_bain = Caracterisation_Bain(self.engine,self.meta )
        
#        self.connect(self.caracterisation_bain, SIGNAL("nouvellecaracterisation_bain(PyQt_PyObject)"), self.initialisation)
        self.module_indicateur.showMaximized()
#        self.module_indicateur.resize(100,100)
    
    @pyqtSlot()
    def on_actionCreation_triggered(self):
        """
        CREATION D INSTRUMENTS
        """
        
        self.instrument = Creation_Instrument(self.engine)
        self.instrument.signal_Creation_ok.connect(self.mise_a_jour_parc)
        self.instrument.showMaximized()
    
    
    
    @pyqtSlot()
    def on_actionModification_triggered(self):
        """
        Modification instrument
        """
        def suppression():
            """fct qui supprime l'objet self.modif_instrument"""
            del self.modif_instrument

        def recup_parc_a_modif(): 
            """fct qui recupere le aprc à modif et l'envoi dans un signal
            dans la modul modif"""
                 
            model = self.tableView_instruments.model()
            id = []
            for row in range(model.rowCount()):
    #            for column in range(model.columnCount()):
                index = model.index(row, 0)
                id.append(int(model.data(index)))
    
            instrument = self.parc.loc[self.parc["ID_INSTRUM"].isin(id)]
            return instrument

        self.modif_instrument = Modification_Instrument(self)
        self.modif_instrument.signal_modification_ok.connect(self.mise_a_jour_parc)
        self.modif_instrument.closeApp.connect(suppression)
        self.modif_instrument.showMaximized()
        
        ####♥on recupere les instruments à modifier et on envoie à la gui via signal

        instrument = recup_parc_a_modif()
        self.signal_parc_a_modi.emit(instrument)

        
    @pyqtSlot()
    def on_actionRecherche_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionCreation_2_triggered(self):
        """
        Slot Gere la creation et l'enregistrement d'un nouveau client
        """

        def table_sect_exploit_sap_bdd():
            """fct recoit le signal de demande secteur exploit de la gui client et
            renvoie la liste en emettant un signal a la gui"""            
            class_table = Secteur_exploitation(self.engine)
            colonne_complete = class_table.return_colonne_responsable()            
            self.signal_mise_a_dispo_client_efs.emit(colonne_complete)        
        
        def sauvegarde_new_client(client):
            """fct qui sauvegarde le nouveau client"""      
            new_client = Client(self.engine)
            new_client.ajouter_client(client)
            
        def mise_dispo_prefix_post_tech():
            """fct recoit le signal de demande poste tech de la gui client et
            renvoie la liste en emettant un signal a la gui""" 
        
        
        def table_postes_tech_sap():
            class_table = Poste_tech_sap(self.engine)
            colonne_complete = class_table.return_prefixe_colonne_poste_tech()            
            self.signal_mise_a_dispo_poste_tech_efs.emit(colonne_complete) 
        
        
        
        self.new_client = Creation_Client(self)
        
        self.new_client.signalNewclient.connect(sauvegarde_new_client)
        self.new_client.signalBesoinservices_efs.connect(table_sect_exploit_sap_bdd)
        
        self.new_client.signalBesoinpostetech_efs.connect(table_postes_tech_sap)

        self.new_client.show()
        
        
        
    
    
    @pyqtSlot()    
    def on_actionReception_Expedition_triggered(self):
        self.reception_expedition = ReceptionExpedition(self.engine)
        self.reception_expedition.showMaximized()
        
    
    @pyqtSlot()
    def on_actionModification_2_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionRecherche_2_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionCreer_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionModifier_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionAffecter_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionModifier_2_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionRechercher_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionPolynome_triggered(self):
        """
        Slot documentation goes here.
        """
        self.polynome = Polynome(self.engine, self.meta)
        self.polynome.showMaximized()
    
    @pyqtSlot()
    def on_actionConsultation_triggered(self):
        """
        Slot documentation goes here.
        """
        self.consultation_bdd = Consultation_Bdd(self.engine, self.meta)
        self.consultation_bdd.showMaximized()
    
    @pyqtSlot()
    def on_actionDeclaration_incertitudes_triggered(self):
        """
        Slot documentation goes here.
        """
        self.declaration_u = MainDeclaration_Incertitudes(self.engine,self.meta )
        self.declaration_u.showMaximized()
    
    @pyqtSlot()
    def on_actionEntite_Client_triggered(self):
        """
        Slot documentation goes here.
        """
        ensemble_client_modif = Client(self.engine)
        table_entite_client = ensemble_client_modif.ensemble_entites_clients()
        
        self.modif_entite_client = Modification_Entite_Client(table_entite_client)
        
        self.modif_entite_client.signalModif_Entite_Client.connect(self.modification_entite_client)

        self.modif_entite_client.show()
    
    def modification_entite_client(self, client):
        
        client_modif = Client(self.engine)
        client_modif.mise_a_jour_ent_client(client)
    
    @pyqtSlot()
    def on_actionSite_Client_triggered(self):
        """
        Gestion de la gui modification client
        """
        def table_postes_tech_sap():
            class_table = Poste_tech_sap(self.engine)
            colonne_complete = class_table.return_prefixe_colonne_poste_tech()            
            self.signal_mise_a_dispo_poste_tech_efs.emit(colonne_complete)
           
        def table_sect_exploit_sap_bdd():
            """fct recoit le signal de demande secteur exploit de la gui client et
            renvoie la liste en emettant un signal a la gui"""            
            class_table = Secteur_exploitation(self.engine)
            colonne_complete = class_table.return_colonne_responsable()            
            self.signal_mise_a_dispo_client_efs.emit(colonne_complete)
        
        def modification_service_client(service_dic):        
            service_modif = Client(self.engine)
            service_modif.mise_a_jour_service_client(service_dic)
            
            table_services_client = service_modif.ensemble_service_client()
            self.signalMAJ_Service_Client.emit(table_services_client)
        
        def ajout_service_client(service_dic ):
            service_new = Client(self.engine)
            service_new.ajout_service(service_dic)            
            table_services_client = service_new.ensemble_service_client()
            
            self.signalMAJ_Service_Client.emit(table_services_client)
           
        def modification_site_client(site):
        
            site_modif = Client(self.engine)
            site_modif.mise_a_jour_site_client(site)
    
            table_site_client = site_modif.ensemble_sites_clients()
    
            self.signalMAJ_Site_Client.emit(table_site_client)
            self.mise_a_jour_parc()
    
        def ajout_site_client(site):
        
            site_new = Client(self.engine)
            site_new.ajout_site(site)
    
            table_site_client = site_new.ensemble_sites_clients()
    
            self.signalMAJ_Site_Client.emit(table_site_client)
            
            self.mise_a_jour_parc()
        
        
        
        ensemble_sites_modif = Client(self.engine)
        table_entite_client = ensemble_sites_modif.ensemble_entites_clients()
        table_site_client = ensemble_sites_modif.ensemble_sites_clients()
        table_services_client = ensemble_sites_modif.ensemble_service_client()
        
        
        self.modif_site_client = Modification_Site_Client(self, table_entite_client, table_site_client, table_services_client )
        
        #connection des signaux
    
        self.modif_site_client.signalModif_Site_Client.connect(modification_site_client)        
        self.modif_site_client.signalAjout_Site_Client.connect(ajout_site_client)
        
        self.modif_site_client.signalModif_Service_Client.connect(modification_service_client)
        self.modif_site_client.signalAjout_Service_Client.connect(ajout_service_client)
        
        
        self.modif_site_client.signalBesoinservices_efs.connect(table_sect_exploit_sap_bdd)
        
        self.modif_site_client.signalBesoinpostetech_efs.connect(table_postes_tech_sap)
        

        self.modif_site_client.show()
    
    

    @pyqtSlot(str)
    def on_lineEdit_valeur_textChanged(self, p0):
        """
        Gestion du tri
        """
        warnings.filterwarnings("error")
        
        text = p0
#        print(p0)
        signe = self.comboBox_signe.currentText()
        nom_colonne = self.comboBox_nom_colonne.currentText()
        
        if text:
            if signe == "=":
                try:
#                    
                    tri = self.parc.loc[(self.parc[nom_colonne] == text)| 
                                        (self.parc[nom_colonne] == text.upper()) |
                                        (self.parc[nom_colonne] == text.capitalize())]
                    self.tableView_instruments.remplir(tri)

                except :
                    try:
                        tri = self.parc[self.parc[nom_colonne].astype(str) == text] #☺gestion des colonnes numeriques
                        self.tableView_instruments.remplir(tri)
                    except:
                        pass

            elif signe == "Contient":
#                try:
                    tri = self.parc[(self.parc[nom_colonne].astype(str).str.contains(text))|
                    (self.parc[nom_colonne].astype(str).str.contains(text.upper()))|
                    (self.parc[nom_colonne].astype(str).str.contains(text.capitalize()))]
                    
                    self.tableView_instruments.remplir(tri)
                    
#                except:                    
#                    pass
            
            elif signe == "<":
                try:
                    tri = self.parc[self.parc[nom_colonne] < float(text)]
                    self.tableView_instruments.remplir(tri)
                    
                except:
                    pass
                    
            elif signe == ">":
                try:
                    tri = self.parc[self.parc[nom_colonne] > float(text)]
                    print(id(tri))
                    self.tableView_instruments.remplir(tri)
#                    print(tri)
                except:
                   pass
        else:
            self.tableView_instruments.remplir(self.parc)
#            if tri:
#                self.tableView_instruments.remplir(tri)
        try:
#            if self.modif_instrument:
            self.signal_nvlle_recherche.emit(tri)
#            mise_en_thread = WorkerSignalParcModif(self, tri)
#            self.threadpool.start(mise_en_thread)
            
        except (UnboundLocalError, AttributeError):
            pass
            
    
    @pyqtSlot(str)
    def on_lineEdit_recherche_instrum_prest_textChanged(self, p0):
        print(p0)
    
    @pyqtSlot(int)
    def on_comboBox_signe_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        """
        text = self.lineEdit_valeur.text()
        self.on_lineEdit_valeur_textChanged(text)
    
    @pyqtSlot(int)
    def on_comboBox_nom_colonne_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        """
        text = self.lineEdit_valeur.text()
        self.on_lineEdit_valeur_textChanged(text)

    
    def mise_a_jour_parc(self):
#        print("coucou")
        self.parc = self.class_instrum.parc_complet()  #####amettre en place
        self.tableView_instruments.remplir(self.parc)
        
        self.on_groupBox_clicked()
    
    @pyqtSlot()
    def on_groupBox_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.groupBox.isChecked():
            text = self.lineEdit_valeur.text()
            self.on_lineEdit_valeur_textChanged(text)
            
        else:
            self.on_lineEdit_valeur_textChanged("")
#        raise NotImplementedError
    
    @pyqtSlot()
    def on_actionCartographie_triggered(self):
        """
        Slot documentation goes here.
        """
        self.carto = Cartographie(self.engine)#Exploitation_Centrales(self.engine)
        self.carto.showMaximized()
        
        

class WorkerDemarrage(QRunnable):
    """class permettant de realiser l'ensemble des appels dans la bdd 
    et d'etre integree dans des trhead via qrunnable et qthreadpoll
    
    exemple en subclassant qthread:
    class WorkerDemarrage(QThread):
    lass permettant de realiser l'ensemble des appels dans la bdd 
    et d'etre integree dans des trhead via qrunnable et qthreadpoll
    
    #    def __init__(self, type, parent= None):
#        super(WorkerDemarrage, self).__init__(parent)
    
    """
    
 
    def __init__(self, type, parent= None):
        super(WorkerDemarrage, self).__init__()
        self.type = type
#        a=Config()
#        engine_bis = a.create_new_engine()
#        print(Config.engine)

        
        self.signals = WorkerSignals()
    
    def parc_instrument(self):
        """fct qui va retourner le parc"""
#        print("parc")
        class_instrum = Instrument(Config.engine)
        self.signals.signalclasseinstrum.emit(class_instrum)
        parc = class_instrum.parc_complet()
#        print(parc)
        self.signals.signalparc.emit(parc)
    
    def futures_reception(self):
        """fct qui va chercher les futures receptions """
#        print("futur rrec")
        class_intervention = Intervention(Config.engine)
        interventions = class_intervention.future_reception() 
        self.signals.signalintervention.emit(interventions)
    
    def expeditions(self):
        class_intervention = Intervention(Config.engine)
        expeditions = class_intervention.gestion_onglet_expedition()
#        print(expeditions)
        self.signals.signalexpeditions.emit(expeditions)
        
        
    @pyqtSlot()
    def run(self):
        if self.type == "instruments":
            self.parc_instrument()
        
        elif self.type == "futures_receptions":
            self.futures_reception()
            
        elif self.type == "expeditions":
            self.expeditions()
        


class WorkerSignalParcModif(QRunnable):
    """mise en thread signal quil y a eu une recher pour la gui modif instruments
    
    """
    
 
    def __init__(self, mainwindow,tri, parent= None):
        super(WorkerSignalParcModif, self).__init__()

        self.mainwindow = mainwindow
        self.tri = tri
        self.signals = WorkerSignals()
    
    def run(self):
        
        self.mainwindow.signal_nvlle_recherche.emit(self.tri)
        




class WorkerSignals(QObject):
    '''
        Gestion des signaux

    '''
    signalparc = pyqtSignal(pd.DataFrame)
    signalintervention = pyqtSignal(pd.DataFrame)
    signalexpeditions = pyqtSignal(pd.DataFrame)
    signalclasseinstrum = pyqtSignal(Instrument)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
