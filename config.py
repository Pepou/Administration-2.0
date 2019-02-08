from sqlalchemy.engine import create_engine
from sqlalchemy import *
from sqlalchemy.orm import *
#from sqlalchemy import exc

class Config():
    """class permettant de configurer/retourner certaines valeurs notamment ce qui concerne la BDD:
    -Configuration BDD
    -Engine
    -base reflect..."""
    
    __adress_bdd = "10.42.1.74"
    __port_bdd= "5434"
    __name_bdd= "Labo_Metro_Prod"#"Labo_Metro_Prod"#"test_modif"#"Labo_Metro_Prod" #
    __site= "LMS"
    engine=""
    login=""
    password=""
    ### si on modifie une varibale avant le init c'est propagé a toutes les instances de la classe
    def __init__(self):
        
        pass
#        self.login=login
#        self.password = password
        
    def modif_engine(cls,login, password ):
#        print(self.adress_bdd)
#        try:
        Config.engine = create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(login, password, Config.__adress_bdd, Config.__port_bdd, Config.__name_bdd)) 
        Config.login = login
        Config.password = password
#        print(Config.engine)
    
    modif_engine = classmethod(modif_engine)

    def creation_metadata(self):
        """"""
        meta = MetaData()
        return meta
    def create_new_engine(self):
        engine = create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(Config.login, Config.password, Config.__adress_bdd, Config.__port_bdd, Config.__name_bdd))
        return engine
#    def engine
        
        
