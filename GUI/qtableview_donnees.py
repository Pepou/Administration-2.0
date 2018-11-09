from PyQt4.QtCore import  Qt, QAbstractTableModel#, QVariant
from PyQt4.QtGui import  QTableView 
#import sys
#import pandas as pd
class Tableview_donnees_fichier(QTableView):
    
    def __init__(self, parent=None):
        super(Tableview_donnees_fichier, self).__init__(parent)
        
        

        self.setAlternatingRowColors(True)
#        self.setStyleSheet("alternate-background-color: lightGray;background-color: white;")

        
    def keyPressEvent(self, event):
        """gestion du copier coller dans le tableau homogeneite"""
       
        items_tableView = self.selectedIndexes()

        clavier = event.key()

        if items_tableView !=None:
            if clavier == 67 :
                self.copySelection()
#            else:
#                return 

    def remplir(self, donnees):
        """fct pour remplir le tableview attention les donnees sont des dataframes pandas"""

        
        self.donnees = donnees
        model = PandasModel(self.donnees) 
        self.setModel(model)
#        self.setEditTriggers(QAbstractItemView::NoEditTriggers)
#        self.resizeColumnsToContents()    
    
    def copySelection(self):
        """Fonction qui copie les donnees presente dans tablewidget """
        selection = self.selectedIndexes()

        if selection:              
            rows = list(set(index.row() for index in selection))
            columns = list(set(index.column() for index in selection))            
            data_export = self.donnees.iloc[rows, columns]            
            data_export.to_clipboard(excel =True)


class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data
#        self.headerDate = [x for x in data.columns]
    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
#        print("coucou {}".format((self._data.iloc[index.row(), index.column()])))
        
        if index.isValid():
            if role == Qt.DisplayRole:
                
                return str(self._data.iloc[index.row(), index.column()])
        
        return None

    def headerData(self, col, orientation, role):
#        print(col)
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:

            return str(self._data.columns[col])
        return None
        
#    def setData(self, index, value, role= Qt.EditRole):
#        if index.isValid():
#            if role == Qt.EditRole:
#                print(value)
#                row = index.row()
#                column = index.column()
#                self._data.iloc[row, column] = value
#                return True
##        print(self._data)
#        return False
#        
#        
#    def flags(self, index):
#        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        
#    def setHeaderDate(self):
