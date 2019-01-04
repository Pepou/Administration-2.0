from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import matplotlib.dates as dates
from PyQt4.QtCore import  SIGNAL


from matplotlib.figure import Figure
#from matplotlib.widgets import Cursor
from io import BytesIO

class MplCanvas(FigureCanvas):
 
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        self.fig.canvas.mpl_connect('button_press_event', self.zoom_debut)
        self.fig.canvas.mpl_connect('button_release_event', self.zoom_fin)
        
#        zoom = pyqtSignal()
#        self.fig

    def nom_graphique(self, titre):        

        self.ax.set_title(titre)
 
    def zoom_debut(self, event):
        self.debut = dates.num2date(event.xdata)
    def zoom_fin(self, event):
        self.fin = dates.num2date(event.xdata)
        self.onclick(event)
    
    def onclick(self, event):
        if self.fin >= self.debut:
            self.emit(SIGNAL("zoom(PyQt_PyObject)"), (self.debut, self.fin))
        else:
            self.emit(SIGNAL("zoom(PyQt_PyObject)"), (self.fin, self.debut))

    
       
class matplotlibWidget(QtGui.QWidget):
 
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        
        self.vbl.addWidget(NavigationToolbar(self.canvas,self))
        self.setLayout(self.vbl)
#        toolitems = [t for t in NavigationToolbar.toolitems]
#        print("tool {}".format(toolitems))
    def sauvegarde(self):
#        print("t dedans")
        imgdata = BytesIO()
        self.canvas.fig.savefig(imgdata, format = 'png')
        imgdata.seek(0)
        return imgdata
        
    
#        toolbar = self.canvas.get_current_fig_manager().toolbar
#        if toolbar.mode!='':
#            print("You clicked on something, but toolbar is in mode {:s}.".format(toolbar.mode))
#        else:
#            print("You {0}-clicked coords ({1},{2}) (pix ({3},{4}))".format(button[event.button+1],\
#                                                                                 event.xdata,\
#                                                                                 event.ydata,\
#                                                                                 event.x,\
#                                                                                 event.y))
#        
#        
#class NavigationToolbar( NavigationToolbar2QT ):
#    
#    def onclick(self, event):
##        """Deal with click events"""
##        button = ['left','middle','right']
#        print(event)
##    def pickerToggled( self, checked ):
##        if checked:            
##            if self._active == "PAN":
##                self.pan()
##            elif self._active == "ZOOM":
##                print("coucou tu zoomes zommezen")
##                self.zoom()
##            self.set_message('Reject/use observation')
