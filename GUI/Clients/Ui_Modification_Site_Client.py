# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Developpement Informatique\Python\Administration\GUI\Clients\Modification_Site_Client.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Modification_Site_Client(object):
    def setupUi(self, Modification_Site_Client):
        Modification_Site_Client.setObjectName(_fromUtf8("Modification_Site_Client"))
        Modification_Site_Client.resize(861, 873)
        self.centralWidget = QtGui.QWidget(Modification_Site_Client)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.tabWidget = QtGui.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.groupBox = QtGui.QGroupBox(self.tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.radioButton_modif = QtGui.QRadioButton(self.groupBox)
        self.radioButton_modif.setCheckable(True)
        self.radioButton_modif.setChecked(False)
        self.radioButton_modif.setObjectName(_fromUtf8("radioButton_modif"))
        self.horizontalLayout.addWidget(self.radioButton_modif)
        self.radioButton_creation = QtGui.QRadioButton(self.groupBox)
        self.radioButton_creation.setObjectName(_fromUtf8("radioButton_creation"))
        self.horizontalLayout.addWidget(self.radioButton_creation)
        self.verticalLayout_6.addWidget(self.groupBox)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setVerticalSpacing(16)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_12 = QtGui.QLabel(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_12)
        self.comboBox_select_Site = QtGui.QComboBox(self.tab)
        self.comboBox_select_Site.setObjectName(_fromUtf8("comboBox_select_Site"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox_select_Site)
        self.label_10 = QtGui.QLabel(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_10)
        self.comboBox_select_client = QtGui.QComboBox(self.tab)
        self.comboBox_select_client.setObjectName(_fromUtf8("comboBox_select_client"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBox_select_client)
        self.label = QtGui.QLabel(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label)
        self.lineEdit_client_nom = QtGui.QLineEdit(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_client_nom.sizePolicy().hasHeightForWidth())
        self.lineEdit_client_nom.setSizePolicy(sizePolicy)
        self.lineEdit_client_nom.setObjectName(_fromUtf8("lineEdit_client_nom"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEdit_client_nom)
        self.label_2 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEdit__client_abrev = QtGui.QLineEdit(self.tab)
        self.lineEdit__client_abrev.setObjectName(_fromUtf8("lineEdit__client_abrev"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.lineEdit__client_abrev)
        self.label_3 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_3)
        self.textEdit_client_adresse = QtGui.QTextEdit(self.tab)
        self.textEdit_client_adresse.setObjectName(_fromUtf8("textEdit_client_adresse"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.textEdit_client_adresse)
        self.label_4 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_4)
        self.lineEdit__client_code_p = QtGui.QLineEdit(self.tab)
        self.lineEdit__client_code_p.setObjectName(_fromUtf8("lineEdit__client_code_p"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.lineEdit__client_code_p)
        self.label_5 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_5)
        self.lineEdit__client_ville = QtGui.QLineEdit(self.tab)
        self.lineEdit__client_ville.setObjectName(_fromUtf8("lineEdit__client_ville"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.lineEdit__client_ville)
        self.label_6 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.LabelRole, self.label_6)
        self.lineEdit__client_tel = QtGui.QLineEdit(self.tab)
        self.lineEdit__client_tel.setObjectName(_fromUtf8("lineEdit__client_tel"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.FieldRole, self.lineEdit__client_tel)
        self.label_7 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(10, QtGui.QFormLayout.LabelRole, self.label_7)
        self.lineEdit__client_fax = QtGui.QLineEdit(self.tab)
        self.lineEdit__client_fax.setObjectName(_fromUtf8("lineEdit__client_fax"))
        self.formLayout.setWidget(10, QtGui.QFormLayout.FieldRole, self.lineEdit__client_fax)
        self.label_8 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(11, QtGui.QFormLayout.LabelRole, self.label_8)
        self.lineEdit__client_courriel = QtGui.QLineEdit(self.tab)
        self.lineEdit__client_courriel.setObjectName(_fromUtf8("lineEdit__client_courriel"))
        self.formLayout.setWidget(11, QtGui.QFormLayout.FieldRole, self.lineEdit__client_courriel)
        self.label_9 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout.setWidget(12, QtGui.QFormLayout.LabelRole, self.label_9)
        self.lineEdit__client_contact = QtGui.QLineEdit(self.tab)
        self.lineEdit__client_contact.setObjectName(_fromUtf8("lineEdit__client_contact"))
        self.formLayout.setWidget(12, QtGui.QFormLayout.FieldRole, self.lineEdit__client_contact)
        self.label_11 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.formLayout.setWidget(13, QtGui.QFormLayout.LabelRole, self.label_11)
        self.comboBox_archivage = QtGui.QComboBox(self.tab)
        self.comboBox_archivage.setObjectName(_fromUtf8("comboBox_archivage"))
        self.comboBox_archivage.addItem(_fromUtf8(""))
        self.comboBox_archivage.addItem(_fromUtf8(""))
        self.formLayout.setWidget(13, QtGui.QFormLayout.FieldRole, self.comboBox_archivage)
        self.line_2 = QtGui.QFrame(self.tab)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.formLayout.setWidget(14, QtGui.QFormLayout.LabelRole, self.line_2)
        self.checkBox_2 = QtGui.QCheckBox(self.tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.checkBox_2)
        self.comboBox_poste_tech_sap_efs = QtGui.QComboBox(self.tab)
        self.comboBox_poste_tech_sap_efs.setEnabled(False)
        self.comboBox_poste_tech_sap_efs.setEditable(True)
        self.comboBox_poste_tech_sap_efs.setObjectName(_fromUtf8("comboBox_poste_tech_sap_efs"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.comboBox_poste_tech_sap_efs)
        self.label_15 = QtGui.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_15)
        self.lineEdit_prefixe_sap = QtGui.QLineEdit(self.tab)
        self.lineEdit_prefixe_sap.setObjectName(_fromUtf8("lineEdit_prefixe_sap"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit_prefixe_sap)
        self.verticalLayout_6.addLayout(self.formLayout)
        self.line = QtGui.QFrame(self.tab)
        self.line.setEnabled(True)
        self.line.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line.setFont(font)
        self.line.setFrameShadow(QtGui.QFrame.Plain)
        self.line.setLineWidth(1)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_6.addWidget(self.line)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.pushButton_maj_site = QtGui.QPushButton(self.tab)
        self.pushButton_maj_site.setObjectName(_fromUtf8("pushButton_maj_site"))
        self.verticalLayout_3.addWidget(self.pushButton_maj_site)
        self.pushButton_ajoute_site = QtGui.QPushButton(self.tab)
        self.pushButton_ajoute_site.setObjectName(_fromUtf8("pushButton_ajoute_site"))
        self.verticalLayout_3.addWidget(self.pushButton_ajoute_site)
        self.verticalLayout_6.addLayout(self.verticalLayout_3)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_13 = QtGui.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.verticalLayout.addWidget(self.label_13)
        self.tableView_services = Tableview_donnees_fichier(self.tab_2)
        self.tableView_services.setObjectName(_fromUtf8("tableView_services"))
        self.verticalLayout.addWidget(self.tableView_services)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.formLayout_3 = QtGui.QFormLayout()
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setHorizontalSpacing(6)
        self.formLayout_3.setVerticalSpacing(16)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.label_19 = QtGui.QLabel(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_19)
        self.lineEdit_service_nom = QtGui.QLineEdit(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_service_nom.sizePolicy().hasHeightForWidth())
        self.lineEdit_service_nom.setSizePolicy(sizePolicy)
        self.lineEdit_service_nom.setObjectName(_fromUtf8("lineEdit_service_nom"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_service_nom)
        self.label_20 = QtGui.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_20)
        self.lineEdit_service_abrev = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_service_abrev.setObjectName(_fromUtf8("lineEdit_service_abrev"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit_service_abrev)
        self.label_24 = QtGui.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_24)
        self.lineEdit_service_tel = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_service_tel.setObjectName(_fromUtf8("lineEdit_service_tel"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit_service_tel)
        self.label_25 = QtGui.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_25.setFont(font)
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_25)
        self.lineEdit_service_fax = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_service_fax.setObjectName(_fromUtf8("lineEdit_service_fax"))
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEdit_service_fax)
        self.label_26 = QtGui.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_26.setFont(font)
        self.label_26.setObjectName(_fromUtf8("label_26"))
        self.formLayout_3.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_26)
        self.lineEdit_service_courriel = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_service_courriel.setObjectName(_fromUtf8("lineEdit_service_courriel"))
        self.formLayout_3.setWidget(5, QtGui.QFormLayout.FieldRole, self.lineEdit_service_courriel)
        self.label_27 = QtGui.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_27.setFont(font)
        self.label_27.setObjectName(_fromUtf8("label_27"))
        self.formLayout_3.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_27)
        self.lineEdit_service_contact = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_service_contact.setObjectName(_fromUtf8("lineEdit_service_contact"))
        self.formLayout_3.setWidget(6, QtGui.QFormLayout.FieldRole, self.lineEdit_service_contact)
        self.label_14 = QtGui.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.formLayout_3.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_14)
        self.comboBox_archivage_service = QtGui.QComboBox(self.tab_2)
        self.comboBox_archivage_service.setObjectName(_fromUtf8("comboBox_archivage_service"))
        self.comboBox_archivage_service.addItem(_fromUtf8(""))
        self.comboBox_archivage_service.addItem(_fromUtf8(""))
        self.formLayout_3.setWidget(7, QtGui.QFormLayout.FieldRole, self.comboBox_archivage_service)
        self.checkBox = QtGui.QCheckBox(self.tab_2)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.checkBox)
        self.comboBox_service_efs = QtGui.QComboBox(self.tab_2)
        self.comboBox_service_efs.setEnabled(False)
        self.comboBox_service_efs.setEditable(True)
        self.comboBox_service_efs.setObjectName(_fromUtf8("comboBox_service_efs"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox_service_efs)
        self.verticalLayout_2.addLayout(self.formLayout_3)
        self.line_3 = QtGui.QFrame(self.tab_2)
        self.line_3.setEnabled(True)
        self.line_3.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line_3.setFont(font)
        self.line_3.setFrameShadow(QtGui.QFrame.Plain)
        self.line_3.setLineWidth(1)
        self.line_3.setMidLineWidth(0)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.verticalLayout_2.addWidget(self.line_3)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.pushButton_maj_service = QtGui.QPushButton(self.tab_2)
        self.pushButton_maj_service.setObjectName(_fromUtf8("pushButton_maj_service"))
        self.verticalLayout_5.addWidget(self.pushButton_maj_service)
        self.pushButton_ajoute_service = QtGui.QPushButton(self.tab_2)
        self.pushButton_ajoute_service.setObjectName(_fromUtf8("pushButton_ajoute_service"))
        self.verticalLayout_5.addWidget(self.pushButton_ajoute_service)
        self.verticalLayout_2.addLayout(self.verticalLayout_5)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout_4.addWidget(self.tabWidget)
        Modification_Site_Client.setCentralWidget(self.centralWidget)

        self.retranslateUi(Modification_Site_Client)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Modification_Site_Client)

    def retranslateUi(self, Modification_Site_Client):
        Modification_Site_Client.setWindowTitle(_translate("Modification_Site_Client", "Modification Site Client", None))
        self.groupBox.setTitle(_translate("Modification_Site_Client", "Selection ", None))
        self.radioButton_modif.setText(_translate("Modification_Site_Client", "Modification", None))
        self.radioButton_creation.setText(_translate("Modification_Site_Client", "Creation", None))
        self.label_12.setText(_translate("Modification_Site_Client", "Choix du Site", None))
        self.label_10.setText(_translate("Modification_Site_Client", "Siege", None))
        self.label.setText(_translate("Modification_Site_Client", "Nom Complet", None))
        self.label_2.setText(_translate("Modification_Site_Client", "Abreviation", None))
        self.label_3.setText(_translate("Modification_Site_Client", "Adresse \n"
"siege social", None))
        self.label_4.setText(_translate("Modification_Site_Client", "Code Postal", None))
        self.label_5.setText(_translate("Modification_Site_Client", "Ville", None))
        self.label_6.setText(_translate("Modification_Site_Client", "N° Telephone", None))
        self.label_7.setText(_translate("Modification_Site_Client", "N° Fax", None))
        self.label_8.setText(_translate("Modification_Site_Client", "Courriel", None))
        self.label_9.setText(_translate("Modification_Site_Client", "Contact", None))
        self.label_11.setText(_translate("Modification_Site_Client", "Archivage", None))
        self.comboBox_archivage.setItemText(0, _translate("Modification_Site_Client", "Non", None))
        self.comboBox_archivage.setItemText(1, _translate("Modification_Site_Client", "Oui", None))
        self.checkBox_2.setText(_translate("Modification_Site_Client", "Site EFS", None))
        self.label_15.setText(_translate("Modification_Site_Client", "Prefixe SAP", None))
        self.pushButton_maj_site.setText(_translate("Modification_Site_Client", "Mettre à jour le site", None))
        self.pushButton_ajoute_site.setText(_translate("Modification_Site_Client", "Ajouter une site au client", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Modification_Site_Client", "Site", None))
        self.label_13.setText(_translate("Modification_Site_Client", "Recapitulatif des Services du site", None))
        self.label_19.setText(_translate("Modification_Site_Client", "Nom Complet", None))
        self.label_20.setText(_translate("Modification_Site_Client", "Abreviation", None))
        self.label_24.setText(_translate("Modification_Site_Client", "N° Telephone", None))
        self.label_25.setText(_translate("Modification_Site_Client", "N° Fax", None))
        self.label_26.setText(_translate("Modification_Site_Client", "Courriel", None))
        self.label_27.setText(_translate("Modification_Site_Client", "Contact", None))
        self.label_14.setText(_translate("Modification_Site_Client", "Archivage", None))
        self.comboBox_archivage_service.setItemText(0, _translate("Modification_Site_Client", "Non", None))
        self.comboBox_archivage_service.setItemText(1, _translate("Modification_Site_Client", "Oui", None))
        self.checkBox.setText(_translate("Modification_Site_Client", "Services EFS", None))
        self.pushButton_maj_service.setText(_translate("Modification_Site_Client", "Mettre à jour le service", None))
        self.pushButton_ajoute_service.setText(_translate("Modification_Site_Client", "Ajouter un service au site", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Modification_Site_Client", "Services", None))

from GUI.Clients.qtableview_service import Tableview_donnees_fichier
import GUI.Clients.icones_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Modification_Site_Client = QtGui.QMainWindow()
    ui = Ui_Modification_Site_Client()
    ui.setupUi(Modification_Site_Client)
    Modification_Site_Client.show()
    sys.exit(app.exec_())

