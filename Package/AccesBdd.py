from sqlalchemy import *
from sqlalchemy.orm import *
#from sqlalchemy.orm import mapper
import pandas as pd
import pendulum
from sqlalchemy.ext.automap import automap_base
from PyQt4.QtGui import QMessageBox


class BDD():
    """class gerant l'ensemble de la bdd avec les engines/sessions et mapper"""
    
    def __init__(self, engine, meta, nouveau_client):
        
        Base = automap_base()
        self.engine = engine 
        
        # reflect the tables
        Base.prepare(engine, reflect=True)
        
        self.meta = meta        
        self.meta.reflect(bind= self.engine)
        
        Session = sessionmaker(bind= self.engine)
        session = Session()
        
        self.connection = self.engine.connect()
        CLIENTS = Base.classes.CLIENTS
        
        session.add(CLIENTS(CODE_CLIENT = "toto"))
        session.commit()
        
###    def creation_client(self, nouveau_client):
##        
##        table_client = Table("CLIENTS", self.meta, autoload=True)
##        mapper(nouveau_client, table_client)
##        
##        
##        self.session.save(nouveau_client)
##        self.session.flush()

class Instrument(): 
    """Class gerant la table instruments de la bdd"""
    
    def __init__(self, engine):
        
#        print("appel classe")
        
        self.engine = engine 
        self.meta = MetaData()    
        
        metadata = MetaData() 
        metadata.reflect(engine, only=['INSTRUMENTS'])
        Base = automap_base(metadata=metadata)
        
       

        
        self.connection = self.engine.connect()

        Session = sessionmaker(bind= self.engine)
        self.session = Session()

        
        Base.prepare()         

        
        self.INSTRUMENTS = Base.classes.INSTRUMENTS
        

        
        
    def parc_complet(self):
        """fonction qui retourne l'ensemble de la table instruments en pandas dataframe"""      
        Session = sessionmaker(bind= self.engine)
        session = Session()
#        print("coucou")
#        meta = MetaData()
#        table_instruments = Table("INSTRUMENTS", meta, autoload=True,  autoload_with= self.engine)
#        print(session.query(self.INSTRUMENTS).all())
        table_instrum = pd.read_sql(session.query(self.INSTRUMENTS).statement, 
                                    session.bind)      
                                    
#        print("lecture pandas")
        table_instrum = table_instrum.sort_values(by = "ID_INSTRUM")
        session.close()
        
        return table_instrum

        
        
    def update_instruments(self, list_dictionnaire):
        """permet la mise à jour des instruments"""
        Session = sessionmaker(bind= self.engine)
        session = Session()
#        print(list_dictionnaire)

        try:
            
            for ele in list_dictionnaire:
    #            print(ele)
                instrum_a_modif = session.query(self.INSTRUMENTS).get(ele["ID_INSTRUM"])
    #            print(instrum_a_modif)
                instrum_a_modif.IDENTIFICATION = ele["IDENTIFICATION"]
                instrum_a_modif.CODE = ele["CODE"]
                instrum_a_modif.DOMAINE_MESURE = ele["DOMAINE_MESURE"]
                instrum_a_modif.FAMILLE = ele["FAMILLE"]
                instrum_a_modif.DESIGNATION = ele["DESIGNATION"]
                instrum_a_modif.TYPE = ele["TYPE"]
                instrum_a_modif.DESIGNATION_LITTERALE = ele["DESIGNATION_LITTERALE"]
    #            instrum_a_modif.PARTICULARITE = ele["PARTICULARITE"]
                instrum_a_modif.CONSTRUCTEUR = ele["CONSTRUCTEUR"]
                instrum_a_modif.REFERENCE_CONSTRUCTEUR = ele["REFERENCE_CONSTRUCTEUR"]
                instrum_a_modif.SITE = ele["SITE"]
                instrum_a_modif.RESOLUTION = float(ele["RESOLUTION"])
                instrum_a_modif.AFFECTATION = ele["AFFECTATION"]
                instrum_a_modif.SOUS_AFFECTATION = ele["SOUS_AFFECTATION"]
                instrum_a_modif.LOCALISATION = ele["LOCALISATION"]
                instrum_a_modif.N_SERIE = ele["N_SERIE"]
                instrum_a_modif.N_SAP_PM = ele["N_SAP_PM"]
                instrum_a_modif.GESTIONNAIRE = ele["GESTIONNAIRE"]
                instrum_a_modif.STATUT = ele["STATUT"]
                instrum_a_modif.COMMENTAIRE = ele["COMMENTAIRE"]                
                instrum_a_modif.N_EQUIPEMENT = ele["N_EQUIPEMENT"]
                instrum_a_modif.N_PLAN = ele["N_PLAN"]
                

    #                print(ele["PERIODICITE_QUANTITE"])
                if ele["PERIODICITE_QUANTITE"] and ele["PERIODICITE_QUANTITE"] != "None" and ele["PERIODICITE_QUANTITE"] != "nan":
                    instrum_a_modif.PERIODICITE_QUANTITE = int(float(ele["PERIODICITE_QUANTITE"]))
                else:
                    instrum_a_modif.PERIODICITE_QUANTITE = None
                instrum_a_modif.PERIODICITE_UNITE = ele["PERIODICITE_UNITE"]
                instrum_a_modif.PROCEDURE = ele["PROCEDURE"]
                instrum_a_modif.PRESTATAIRE = ele["PRESTATAIRE"]
                instrum_a_modif.ETAT_UTILISATION = ele["ETAT_UTILISATION"]
                
    #                print(f""" instrum lie {ele["INSTRUMENT_LIE"]} type {type(ele["INSTRUMENT_LIE"])}""")
                if ele["INSTRUMENT_LIE"]== "False":
    #                    print("coucu")
                    instrum_a_modif.INSTRUMENT_LIE = False
                    instrum_a_modif.REF_INSTRUMENT = None
                    
                else:
                    instrum_a_modif.INSTRUMENT_LIE = True
#                    print(f""" {ele["REF_INSTRUMENT"]} et type {type(ele["REF_INSTRUMENT"])}""")
                
                    if ele["REF_INSTRUMENT"] and ele["REF_INSTRUMENT"]!= "None" and ele["REF_INSTRUMENT"] != "nan":
                        try:
                            id_instrum_lie = session.query(self.INSTRUMENTS.ID_INSTRUM).filter(self.INSTRUMENTS.IDENTIFICATION == ele["REF_INSTRUMENT"]).first()[0]
#                            print(id_instrum_lie)
                            instrum_a_modif.REF_INSTRUMENT = int(float(id_instrum_lie))
                        except:
                            try:
#                                print("premeir bloc")
                                id_instrum_lie = int(float(ele["REF_INSTRUMENT"]))
                                instrum_a_modif.INSTRUMENT_LIE = True
                                instrum_a_modif.REF_INSTRUMENT = id_instrum_lie
#                                print(id_instrum_lie)
                            except:                            
                                instrum_a_modif.INSTRUMENT_LIE = False
                                instrum_a_modif.REF_INSTRUMENT = None
                    else:
                        instrum_a_modif.INSTRUMENT_LIE = False
                        instrum_a_modif.REF_INSTRUMENT = None
                            
                session.flush()                
            session.commit()

        except Exception as e:
            print(e)
            session.rollback()
#                yield None
        finally:
            session.close()
#            print("erreur lors de la modification")
            
    
    def creation_instrum_unique(self, new_instrum):
        """fct qui insert un nouvelle in instrumen
        new_instrum = dict{key = nom column:value,...."""
        
        Session = sessionmaker(bind= self.engine)
        session = Session()
        meta = MetaData()
        trans = self.connection.begin()
        table_instruments = table_instruments = Table("INSTRUMENTS", meta, autoload=True,  autoload_with= self.engine)
        i = table_instruments.insert()
        
        query = session.query(self.INSTRUMENTS.IDENTIFICATION).all()
        query_list = [x[0] for x in query]
        if new_instrum["IDENTIFICATION"] not in query_list:
            try:
                self.connection.execute(i, new_instrum)
                trans.commit()
            except Exception as e:            
                trans.rollback()
                print(f"une erreur s'est produite lors de la creation de l'instrument: {new_instrum} \n erreur : {e}")
            finally:
                self.session.close()
        else:
            print(f"l'instrument est deja connu")
            self.session.close()
        
    def creation_instrums_multi(self, list_new_intrum):
        """fct qui insert un nouvelle in instrumen
        list_new_instrum = lict(dict{key = nom column:value,....}dict2.....]"""
        
        Session = sessionmaker(bind= self.engine)
        session = Session()
        
        meta = MetaData()  
        trans = self.connection.begin()
        table_instruments = Table("INSTRUMENTS", meta, autoload=True,  autoload_with= self.engine)
        i = table_instruments.insert()
        
        
        
        query = session.query(self.INSTRUMENTS.IDENTIFICATION).all()
        query_list = [x[0] for x in query]
#        print(query)
        list_a_passer = [inst for inst in list_new_intrum if inst["IDENTIFICATION"] not in query_list]
#        print(list_a_passer)
        
        if list_a_passer:
            try:
                self.connection.execute(i, list_a_passer)
                trans.commit()
                self.session.close()
            except Exception as e:            
                trans.rollback()
                print(f"une erreur s'est produite lors de la creation des instruments: {list_a_passer} \n erreur : {e}")
            finally:
                self.session.close()
        else:
            self.session.close()

class Secteur_exploitation():
    """class tapant sur la table SET_EXPLOIT_SAP"""    
    
    def __init__(self, engine):
             
        Base = automap_base()
        self.engine = engine     
        self.meta = MetaData()
        self.connection = self.engine.connect()
        
        Base.prepare(engine, reflect=True)        
        
        self.SEC_EXPLOIT = Base.classes.SECT_EXPLOIT_SAP

        
    def return_nom_secteur(self, num_secteur_exploit):
        Session = sessionmaker(bind= self.engine)
        session = Session()
#        try:
        try:
                a = session.query(self.SEC_EXPLOIT).filter(self.SEC_EXPLOIT.SEX == num_secteur_exploit).first()
                yield a.RESPONSABLE
        except Exception as e:
            print(e)
            session.rollback()
#                yield None
        finally:
            session.close()
#        except :
#            pass
    def return_colonne_responsable(self):
        """renvoie la colonne responsable ou les nom des services sont en fct des secteurs d'exploit"""
        Session = sessionmaker(bind= self.engine)
        session = Session()       
        
        try:
            colonne_responsable = session.query(self.SEC_EXPLOIT.RESPONSABLE).all() #list de tupple
            
            #mise en list
            list_retourne = []
            for ele in colonne_responsable:
                list_retourne.append(ele[0])

            return list_retourne
        
        except Exception as e:
            print(e)
            session.rollback()

        finally:
            session.close()
        
class Poste_tech_sap():
    """class tapant sur la table SET_EXPLOIT_SAP"""
    
    
    def __init__(self, engine):        
        
        Base = automap_base()
        self.engine = engine     
        self.meta = MetaData()
        self.connection = self.engine.connect()
        
        Base.prepare(engine, reflect=True)        
        
        self.POSTES_TECH_SAP = Base.classes.POSTES_TECH_SAP
    
    def return_prefixe_colonne_poste_tech(self):
        """renvoie la colonne responsable ou les nom des services sont en fct des secteurs d'exploit"""
        Session = sessionmaker(bind= self.engine)
        session = Session()       
        
        try:
            colonne = session.query(self.POSTES_TECH_SAP).all() #list de tupple
        
        #mise en list
            list_retourne = []
            for ele in colonne:
    
                mise_en_list = ele.POSTE_TECHNIQUE.split("-")
    
                if len(mise_en_list) == 3:
                    
                    prefixe_sap = str( "-".join(mise_en_list))
                    list_retourne.append((mise_en_list[2], ele.DESIGNATION, prefixe_sap))
    
    #        print(list_retourne)
            return list_retourne
        
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()
            
            
    def recherche_designation_by_post_tech(self, post_tech):
        """permet la recherche d'une designation de poste tech par sa reference exemple SAP 23-4401-NTS"""
        Session = sessionmaker(bind= self.engine)
        session = Session()       
        
        try:
            nom = session.query(self.POSTES_TECH_SAP).filter(self.POSTES_TECH_SAP.POSTE_TECHNIQUE == post_tech).first()
    #        for ele in nom:
    #            print(ele)
    #        print(nom.DESIGNATION)
            yield nom.DESIGNATION
            
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()
#    
#    def recherche_code_client_by_post_tech(self, post_tech):
#        
#        Session = sessionmaker(bind= self.engine)
#        session = Session()       
#        
#        try:
#            nom = session.query(self.POSTES_TECH_SAP).filter(self.POSTES_TECH_SAP.POSTE_TECHNIQUE == post_tech).first()
#    #        for ele in nom:
#    #            print(ele)
#            print(nom.DESIGNATION)
#            yield nom.DESIGNATION
#            
#        except:
#            session.rollback()
#        finally:
#            session.close()

class Intervention():
    """classe gerant la table intervention"""
    
    def __init__(self, engine):
        
        self.engine = engine 
        self.meta = MetaData()        
        self.meta.reflect(bind=self.engine)
        
        metadata = MetaData() 
        metadata.reflect(engine, only=['INSTRUMENTS', 'INTERVENTIONS', 
                                        'CARTO_ADMINISTRATION', 'AFFICHEUR_CONTROLE_ADMINISTRATIF',
                                        'AFFICHEUR_CONTROLE_ADMINISTRATIF', 'ETALONNAGE_TEMP_ADMINISTRATION'])
        Base = automap_base(metadata=metadata)

        
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        
#        self.connection = self.engine.connect()
        self.table_intervention = Table("INTERVENTIONS", self.meta, autoload=True)
        
#        Base = automap_base()
        Base.prepare()   
        
        self.INSTRUMENTS = Base.classes.INSTRUMENTS
        self.INTERVENTIONS = Base.classes.INTERVENTIONS
        self.ADMIN_CARTO = Base.classes.CARTO_ADMINISTRATION
        self.AFFICHEURS_ADMIN = Base.classes.AFFICHEUR_CONTROLE_ADMINISTRATIF
        self.ETAL_TEMP = Base.classes.ETALONNAGE_TEMP_ADMINISTRATION
        
    
    def future_reception(self):
        try:
            Session = sessionmaker(bind= self.engine)
            session = Session()
            date_du_jour = pendulum.now('Europe/Paris')
    #        print(date_du_jour)
            
            a = session.query(self.table_intervention).filter(
                            self.table_intervention.c.INTERVENTION == "Réception", 
                            self.table_intervention.c.DATE_PROCHAINE_INTERVENTION >= date_du_jour )\
                            .order_by(self.table_intervention.c.DATE_INTERVENTION.desc())\
                            .limit(100)
            
            receptions = pd.read_sql(a.statement, 
                                        self.session.bind)   
            
            
#            self.session.close()
            return receptions
        
        except Exception as e:
            print(e)
            self.session.rollback()
#            yield None
        finally:
            self.session.close()
    
    def gestion_onglet_expedition(self):
        """ fct qui va trier les differents tables pour afficher tout ce qui a ete expedier"""

#        date_annee_precedente = pendulum.now().subtract(years=1)
        
        colonnes = ["Date", "Date realisation","Instrument", "N°Inventaire", "N°Equipement", "N°Plan", "N° Rapport"]
        result = self.session.query(self.INTERVENTIONS.DATE_INTERVENTION,
                                        self.ADMIN_CARTO.DATE_REALISATION, 
                                       self.INTERVENTIONS.IDENTIFICATION,
                                       self.INSTRUMENTS.N_SAP_PM,
                                       self.INSTRUMENTS.N_EQUIPEMENT, 
                                       self.INSTRUMENTS.N_PLAN,
                                       self.ADMIN_CARTO.NUM_RAPPORT)\
                                       .filter(and_(func.lower(self.INTERVENTIONS.INTERVENTION)== func.lower("Expédition"),
                                                    self.INTERVENTIONS.DATE_INTERVENTION >= pendulum.now().subtract(days=15), 
                                                    self.ADMIN_CARTO.DATE_REALISATION >= pendulum.now().subtract(months=1), 
                                                    self.ADMIN_CARTO.DATE_REALISATION<=self.INTERVENTIONS.DATE_INTERVENTION ))\
                                       .join(self.ADMIN_CARTO, self.ADMIN_CARTO.IDENT_ENCEINTE == self.INTERVENTIONS.IDENTIFICATION)\
                                       .join((self.INSTRUMENTS, self.ADMIN_CARTO.IDENT_ENCEINTE == self.INSTRUMENTS.IDENTIFICATION))\
                                       .order_by(self.INTERVENTIONS.IDENTIFICATION)\
                                       .distinct(self.INTERVENTIONS.IDENTIFICATION)\
                                       .order_by(self.INTERVENTIONS.DATE_INTERVENTION.desc())\
                                       
#                                    .all()   
#                                       .limit(100)
#                                       .all()
        
        cartos = pd.read_sql(result.statement, self.session.bind)
        cartos.columns = colonnes
#        cartos.drop_duplicates("N° Rapport",  inplace=True)
#        cartos.stack().unique()
#        print(cartos)
#        print( cartos["N° Rapport"].unique())
        result = self.session.query(self.INTERVENTIONS.DATE_INTERVENTION,
                                        self.AFFICHEURS_ADMIN.DATE_CONTROLE,         
                                        self.INTERVENTIONS.IDENTIFICATION,
                                        self.INSTRUMENTS.N_SAP_PM, 
                                        self.INSTRUMENTS.N_EQUIPEMENT, 
                                        self.INSTRUMENTS.N_PLAN,
                                        self.AFFICHEURS_ADMIN.NUM_DOC)\
                                        .filter(and_(func.lower(self.INTERVENTIONS.INTERVENTION)== func.lower("Expédition"),
                                                    self.INTERVENTIONS.DATE_INTERVENTION >= pendulum.now().subtract(days=15), 
                                                    self.AFFICHEURS_ADMIN.DATE_CONTROLE >= pendulum.now().subtract(months=1), 
                                                    self.AFFICHEURS_ADMIN.DATE_CONTROLE<=self.INTERVENTIONS.DATE_INTERVENTION ))\
                                        .join(self.INSTRUMENTS,  self.INTERVENTIONS.IDENTIFICATION == self.INSTRUMENTS.IDENTIFICATION)\
                                        .join(self.AFFICHEURS_ADMIN, self.AFFICHEURS_ADMIN.IDENTIFICATION == self.INSTRUMENTS.ID_INSTRUM)\
                                        .order_by(self.INTERVENTIONS.IDENTIFICATION)\
                                        .distinct(self.INTERVENTIONS.IDENTIFICATION)\
                                        .order_by(self.INTERVENTIONS.DATE_INTERVENTION.desc())
#                                        .join(self.AFFICHEURS_ADMIN.IDENTIFICATION, self.AFFICHEURS_ADMIN.IDENTIFICATION == self.INSTRUMENTS.ID_INSTRUM)\
#                                        
#                                                    
#                                        .join((self.INSTRUMENTS, self.AFFICHEURS_ADMIN.IDENTIFICATION == self.INSTRUMENTS.ID_INSTRUM))\
#                                        .order_by(self.INTERVENTIONS.DATE_INTERVENTION.desc())
#                                        .join(self.INSTRUMENTS,  self.INTERVENTIONS.IDENTIFICATION == self.INSTRUMENTS.IDENTIFICATION)\
#                                       .limit(100)
###                                       .all()
##                                       INSTRUMENTS
##                                       #, self.INTERVENTIONS.IDENTIFICATION == self.AFFICHEURS_ADMIN.IDENTIFICATION )\
##        
###        print(afficheurs.all)
        afficheurs = pd.read_sql(result.statement, self.session.bind)
        afficheurs.columns = colonnes
#        afficheurs.drop_duplicates("N° Rapport",  inplace=True)
        
#        print(afficheurs)
##        
##        
        result = self.session.query(self.INTERVENTIONS.DATE_INTERVENTION,
                                        self.ETAL_TEMP.DATE_ETAL, 
                                       self.INTERVENTIONS.IDENTIFICATION,
                                       self.INSTRUMENTS.N_SAP_PM,
                                       self.INSTRUMENTS.N_EQUIPEMENT, 
                                       self.INSTRUMENTS.N_PLAN,
                                       self.ETAL_TEMP.NUM_DOCUMENT
                                       )\
                                        .filter(and_(func.lower(self.INTERVENTIONS.INTERVENTION)== func.lower("Expédition"),
                                                    self.INTERVENTIONS.DATE_INTERVENTION >= pendulum.now().subtract(days=15), 
                                                    self.ETAL_TEMP.DATE_ETAL <= self.INTERVENTIONS.DATE_INTERVENTION, 
                                                    self.ETAL_TEMP.DATE_ETAL >= pendulum.now().subtract(months=1)))\
                                        .join(self.ETAL_TEMP,  self.INTERVENTIONS.IDENTIFICATION == self.ETAL_TEMP.IDENTIFICATION_INSTRUM)\
                                        .join((self.INSTRUMENTS, self.ETAL_TEMP.IDENTIFICATION_INSTRUM == self.INSTRUMENTS.IDENTIFICATION))\
                                        .order_by(self.INTERVENTIONS.IDENTIFICATION)\
                                        .distinct(self.INTERVENTIONS.IDENTIFICATION)\
                                        .order_by(self.INTERVENTIONS.DATE_INTERVENTION.desc())
##                                       .limit(10)
##
###                                       
##
        temperatures = pd.read_sql(result.statement, self.session.bind)
        temperatures.columns = colonnes
#        
##        print(temperatures)
#
        expeditions = pd.concat([cartos, afficheurs, temperatures])

        
        return expeditions
        
class Client():
    """class qui permert de gerer les clients :
    un client:
    un siege social
    peut avoir des sites et les sites peuvent avoir des services"""
    
    def __init__(self,engine):
        
        Base = automap_base()
        self.engine = engine     
#        self.meta = MetaData()
        self.connection = self.engine.connect()
        
        metadata = MetaData() 
        metadata.reflect(engine, only=['ENTITE_CLIENT', 'CLIENTS', 
                                        'SERVICES_CLIENT'])
        Base = automap_base(metadata=metadata)
        
        Base.prepare()
        
        
        self.ENT_CLIENT = Base.classes.ENTITE_CLIENT
        self.CLIENTS = Base.classes.CLIENTS
        self.SERVICE = Base.classes.SERVICES_CLIENT
        
        
    def ensemble_entites_clients(self):
        """recupere la table entite_client et la met dans une dataframe pandas"""
#        meta = MetaData()
        Session = sessionmaker(bind= self.engine)
        session = Session()
        try:
            #chargement de la table complete:
            table = session.query(self.ENT_CLIENT)
            
            #mise sous pandas:
            table_entite_client = pd.read_sql(table.statement, session.bind)      
            
    
    #        session.close()
            return table_entite_client
        
        except Exception as e:
            print(e)
            session.rollback()
#            yield None
        finally:
            session.close()
    
    def ensemble_sites_clients(self):
        """recupere la table clients qui correspond aux sites des clients et la met dans une dataframe pandas"""
#        meta = MetaData()
        Session = sessionmaker(bind= self.engine)
        session = Session()
        
        try:
            #chargement de la table complete:
            table = session.query(self.CLIENTS)
            
            #mise sous pandas:
            table_site_client = pd.read_sql(table.statement, session.bind)

            return table_site_client
        
        except Exception as e:
            print(e)
            session.rollback()
#            yield None
        finally:
            session.close()
            
            
    def ensemble_service_client(self):
        """recupere la table services du client  et la met dans une dataframe pandas"""
#        meta = MetaData()
        Session = sessionmaker(bind= self.engine)
        session = Session()
        try:
            #chargement de la table complete:
            table = session.query(self.SERVICE)
            
            #mise sous pandas:
            table_services_client = pd.read_sql(table.statement, session.bind)
        
#        session.close()
            return table_services_client       
        except Exception as e:
            print(e)
            session.rollback()
#            yield None
        finally:
            session.close()   
        
    def mise_a_jour_ent_client(self, donnees_en_dic):
#        meta = MetaData()
        try:
            Session = sessionmaker(bind= self.engine)
            session = Session()
    
            id = int(donnees_en_dic.pop("ID"))
    
            session.query(self.ENT_CLIENT).filter(self.ENT_CLIENT.ID_ENT_CLIENT == id).update(donnees_en_dic)
            session.commit()
#            session.close()
        
        except Exception as e:
            print(e)
            session.rollback()
#            session.close()
        
        finally:
            session.close()
            
    def mise_a_jour_site_client(self, donnees_en_dic):
#        meta = MetaData()
        Session = sessionmaker(bind= self.engine)
        session = Session()
#        print(donnees_en_dic)
        
        try:
            id = int(donnees_en_dic.pop("ID_CLIENTS"))
    
            session.query(self.CLIENTS).filter(self.CLIENTS.ID_CLIENTS == id).update(donnees_en_dic)
            session.commit()
#            session.close()
                
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, 
                    self.trUtf8("Client"), 
                    self.trUtf8("La mise a jour n'a pu etre realisée. Erreur {e}"))
        finally:
            session.close()
        
    def ajout_site(self, donnees_en_dic):        
        try:
            Session = sessionmaker(bind= self.engine)
            session = Session()
            
            new_site = self.CLIENTS(CODE_CLIENT = donnees_en_dic["CODE_CLIENT"], 
                                        SOCIETE = donnees_en_dic["SOCIETE"], 
                                        ADRESSE = donnees_en_dic["ADRESSE"], 
                                        VILLE = donnees_en_dic["VILLE"], 
                                        CODE_POSTAL = donnees_en_dic["CODE_POSTAL"], 
                                        TELEPHONE = donnees_en_dic["TELEPHONE"], 
                                        FAX = donnees_en_dic["FAX"],
                                        ID_ENT_CLIENT = donnees_en_dic["ID_ENT_CLIENT"],
                                        COURRIEL = donnees_en_dic["COURRIEL"],
                                        CONTACT = donnees_en_dic["CONTACT"], 
                                        ARCHIVAGE = donnees_en_dic["ARCHIVAGE"], 
                                        PREFIXE_POSTE_TECH_SAP = donnees_en_dic["PREFIXE_POSTE_TECH_SAP"])
            session.add(new_site)
            session.commit()
            
        except Exception as e:
            print("une erreur s'est produite lors de l'ajout d'un site. Erreur {e}")
            session.rollback()
#            session.close()
        
        finally:
            session.close()
    
    def mise_a_jour_service_client(self, donnees_en_dic):
#        meta = MetaData()
        try:
            Session = sessionmaker(bind= self.engine)
            session = Session()
    
            id = int(donnees_en_dic.pop("ID_SERVICE"))
#            print(f"id pour la base {id}")

            session.query(self.SERVICE).filter(self.SERVICE.ID_SERVICE == id).update(donnees_en_dic)
            session.commit()

        except Exception as e:
            print("une erreur s'est produite lors de la mise à jour du service.\n erreur {e}")
            session.rollback()
        
        finally:
            session.close()
            
            

    def ajout_service(self, donnees_en_dic):
        
        try:
            Session = sessionmaker(bind= self.engine)
            session = Session()
            
            new_service = self.SERVICE(ID_CLIENT = donnees_en_dic["ID_CLIENT"],
                                        ID_ENTITE_CLIENT = donnees_en_dic["ID_ENTITE_CLIENT"],
                                        NOM = donnees_en_dic["NOM"], 
                                        ABREVIATION = donnees_en_dic["ABREVIATION"], 
                                        TELEPHONE = donnees_en_dic["TELEPHONE"], 
                                        FAX = donnees_en_dic["FAX"], 
                                        COURRIEL = donnees_en_dic["COURRIEL"], 
                                        CONTACT = donnees_en_dic["CONTACT"], 
                                        ARCHIVAGE = donnees_en_dic["ARCHIVAGE"])
            session.add(new_service)
            session.commit()
            
        except Exception as e:
            print("une erreur s'est produite lors de l'ajout d'un service.\n Erreur {e}")
            session.rollback()
#            session.close()
        
        finally:
            session.close()
    
    def ajouter_client(self, dict_attribu):    
        """fct qui gere l'ajout dans la bdd d'un client avec un siege social des sites et des services"""
        try:
            Session = sessionmaker(bind= self.engine)
            session = Session()
            
            #gestion Siege social client
            new_client = self.ENT_CLIENT(NOM = dict_attribu["nom_complet"], 
                                        ABREVIATION = dict_attribu["abreviation"] , 
                                        ADRESSE = dict_attribu["adresse"], 
                                        CODE_POSTAL=dict_attribu["code_postal"], 
                                        VILLE=dict_attribu["ville"], 
                                        TELEPHONE=dict_attribu["telephone"], 
                                        FAX=dict_attribu["fax"], 
                                        COURRIEL=dict_attribu["courriel"], 
                                        CONTACT=dict_attribu["contact"], 
                                        ARCHIVAGE = False)
            
    
            session.add(new_client)
            session.flush()
            
            #gestion sites client
            if dict_attribu["sites"]:
                for site in  dict_attribu["sites"]:
                    object_service = []
                    new_site = self.CLIENTS(CODE_CLIENT = site["abreviation"], 
                                        SOCIETE = site["nom_complet"], 
                                        ADRESSE = site["adresse"], 
                                        VILLE = site["ville"], 
                                        CODE_POSTAL = site["code_postal"], 
                                        TELEPHONE = site["tel"], 
                                        FAX = site["fax"],
                                        ID_ENT_CLIENT = new_client.ID_ENT_CLIENT,
                                        COURRIEL = site["courriel"],
                                        CONTACT = site["contact"],
                                        PREFIXE_POSTE_TECH_SAP = site["prefixe_sap"], 
                                        ARCHIVAGE = False)
                
                    session.add(new_site)
                    session.flush()
                    for service in site["services"]:
                        new_service = self.SERVICE(ID_CLIENT = new_site.ID_CLIENTS,
                                                    ID_ENTITE_CLIENT = new_client.ID_ENT_CLIENT,
                                                    NOM = service["nom_complet"], 
                                                    ABREVIATION = service["abreviation"], 
                                                    TELEPHONE = service["tel"], 
                                                    FAX = service["fax"], 
                                                    COURRIEL = service["courriel"], 
                                                    CONTACT = service["contact"], 
                                                    ARCHIVAGE = False)
                        
                        object_service.append(new_service)
                    
                    session.add_all(object_service)
            else:
                new_site = self.CLIENTS(CODE_CLIENT = dict_attribu["abreviation"], 
                                        SOCIETE = dict_attribu["nom_complet"], 
                                        ADRESSE = dict_attribu["adresse"], 
                                        VILLE = dict_attribu["ville"], 
                                        CODE_POSTAL = dict_attribu["code_postal"], 
                                        TELEPHONE = dict_attribu["telephone"], 
                                        FAX = dict_attribu["fax"],
                                        ID_ENT_CLIENT = new_client.ID_ENT_CLIENT,
                                        COURRIEL = dict_attribu["courriel"],
                                        CONTACT = dict_attribu["contact"])
                
                session.add(new_site)
                session.flush()
            
            session.commit()
#            session.close()
        except Execption as e:
            print(e)
            session.rollback()
#            session.close()
        
        finally:
            session.close()
        

    def modif_entite(self, dict_attribu):
        """fct modifi la table entite client"""
        
        
        Session = sessionmaker(bind= self.engine)
        session = Session()
        try:
        #gestion Siege social client
            client = self.ENT_CLIENT(NOM = dict_attribu["nom_complet"], 
                                        ABREVIATION = dict_attribu["abreviation"] , 
                                        ADRESSE = dict_attribu["adresse"], 
                                        CODE_POSTAL=dict_attribu["code_postal"], 
                                        VILLE=dict_attribu["ville"], 
                                        TELEPHONE=dict_attribu["telephone"], 
                                        FAX=dict_attribu["fax"], 
                                        COURRIEL=dict_attribu["courriel"], 
                                        CONTACT=dict_attribu["contact"])
            
            
            
            session.query(self.ENT_CLIENT).filter_by(id=123).update({"name": u"Bob Marley"})
        
        
        
        
        except Exception as e:
            print(e)
            session.rollback()
#            yield None
        finally:
            session.close()
        


    def recherche_code_client_by_post_tech(self, post_tech):

        Session = sessionmaker(bind= self.engine)
        session = Session()     
        
        try:
            code = session.query(self.CLIENTS.CODE_CLIENT).filter(self.CLIENTS.PREFIXE_POSTE_TECH_SAP == post_tech).first()
#            print(f"requete passéee {code}")
#            print(code[0])
    #        for ele in nom:
    #            print(ele.CODE_CLIENT)
            if code:
    #            print(nom.CODE_CLIENT)
                yield code[0]
        
        except Exception as e:
            print(e) 
            session.rollback()
        finally:
            session.close()









class Prestation():
    """class permettant de rapatrier l'ensemble des prestations en fct du domaine"""

def __init__(self,engine, domaine):
        
#        Base = automap_base()
        self.engine = engine     
#        self.meta = MetaData()
        self.connection = engine.connect()
        self.DBSession = sessionmaker(bind=engine)
        
        metadata = MetaData() 
        metadata.reflect(engine, only=['ETALONNAGE_TEMP_ADMINISTRATION', 'ETALONNAGE_RESULTAT', 
                                        'CONFORMITE_TEMP_RESULTAT'])
        self.Base = automap_base(metadata=metadata)
        
        self.Base.prepare()
        
def prestation_temperature(self, nom_instrum):
    """recupere les prestations effectuees sur un instrum"""
    
    
    Session = sessionmaker(bind= self.engine)
    session = Session()
    
    ETAL_TEMP = self.Base.classes.ETALONNAGE_TEMP_ADMINISTRATION
    ETAL_RESULT = self.Base.classes.ETALONNAGE_RESULTAT
    
    result = session.query(ETAL_TEMP.IDENTIFICATION_INSTRUM, 
                            ETAL_TEMP.DATE_ETAL, 
                            ETAL_TEMP.NUM_DOCUMENT, 
                            ETAL_TEMP.ANNULE_NUM_DOC, 
                            ETAL_TEMP.NBR_PT_ETALONNAGE, 
                            ETAL_TEMP.NOM_PROC, 
                            ETAL_TEMP.ETAT_RECEPTION,
                            ETAL_RESULT.MOYENNE_ETAL_C, 
                            ETAL_RESULT.MOYENNE_INSTRUM,
                            ETAL_RESULT.MOYENNE_CORRECTION, 
                            ETAL_RESULT.U)\
                            .join(ETAL_RESULT, ETAL_TEMP == ETAL_RESULT.ID_ETALONNAGE)\
                            .filter(ETAL_TEMP.IDENTIFICATION_INSTRUM == nom_instrum)\
                            .all()
    
    
    
#        self.ENT_CLIENT = Base.classes.ENTITE_CLIENT
#        self.CLIENTS = Base.classes.CLIENTS
#        self.SERVICE = Base.classes.SERVICES_CLIENT







