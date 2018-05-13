#!/usr/bin/env python3

from PyQt5.QtWidgets import (QWidget, QLabel, QComboBox,
                             QHBoxLayout, QGroupBox, QPushButton, 
                             QAbstractItemView, QVBoxLayout, QLineEdit,
                             QGridLayout, QFileDialog, QTableView)
from PyQt5.QtCore import QFileInfo, QCoreApplication, Qt, QModelIndex

import sys
from PyQt5.QtGui import QStandardItemModel


v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    # this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-4]))

from bridgehouse.editMap.toolbox import toolbox
from bridgehouse.editMap.router import geoSite_pb2
    
class GeoSiteEditorPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.translate = QCoreApplication.translate
        self.labelGeoSiteTabel = (
            self.translate("geoSiteEditorPanel", "Domain"),
            self.translate("geoSiteEditorPanel", "Type"))
        self.domainType = ("Plain", "Regex", "Domain")
        self.geoSiteList = geoSite_pb2.GeoSiteList()
        self.CodeTagList = set()
        
    def createGeoSiteEditorPanel(self):
        self.groupgeoSite = QGroupBox(self.translate("geoSiteEditorPanel", "GeoSite Editor"))

        labelCodeTag = QLabel(self.translate("geoSiteEditorPanel", "Code Tag"))
        self.comboBoxCodeTag = QComboBox()
        self.btnCodeTagNew = QPushButton(self.translate("geoSiteEditorPanel", "New Domain Sites"))
        self.lineEditCodeTag = QLineEdit()

        gridCodeTag = QGridLayout()
        gridCodeTag.addWidget(labelCodeTag, 0, 0, 1, 1)
        gridCodeTag.addWidget(self.comboBoxCodeTag, 0, 1, 1, 1)
        gridCodeTag.addWidget(self.btnCodeTagNew, 1, 0, 1, 1, Qt.AlignLeft)
        gridCodeTag.addWidget(self.lineEditCodeTag, 1, 1, 1, 1, Qt.AlignLeft)
        
        self.btntableWidgetGeoSiteOpen = QPushButton(self.translate("geoSiteEditorPanel", "Open"))
        self.btntableWidgetNew = QPushButton(self.translate("geoSiteEditorPanel", "New"))
        self.btntableWidgetDelete = QPushButton(self.translate("geoSiteEditorPanel", "Delete"))
        
        vboxtableBtn = QVBoxLayout()
        vboxtableBtn.addStretch()
        vboxtableBtn.addWidget(self.btntableWidgetGeoSiteOpen)
        vboxtableBtn.addWidget(self.btntableWidgetNew)
        vboxtableBtn.addWidget(self.btntableWidgetDelete)
        
        self.tableViewGeoSitemodel = QStandardItemModel(0, 2)
        self.tableViewIGeoSite = tableViewGeoSite = QTableView(self)
        tableViewGeoSite.setModel(self.tableViewGeoSitemodel)
        self.tableViewGeoSitemodel.setHorizontalHeaderLabels(self.labelGeoSiteTabel)
        tableViewGeoSite.setSelectionMode(QAbstractItemView.SingleSelection)
        tableViewGeoSite.setSelectionBehavior(QAbstractItemView.SelectRows)

        tableViewGeoSite.setItemDelegateForColumn(1, toolbox.ComboBoxDelegate(self.domainType))

        hboxTabelView = QHBoxLayout()
        hboxTabelView.addWidget(self.tableViewIGeoSite)
        hboxTabelView.addLayout(vboxtableBtn)
        
        vboxGeoSite = QVBoxLayout()
        vboxGeoSite.addLayout(gridCodeTag)
        vboxGeoSite.addLayout(hboxTabelView)
        
        self.groupgeoSite.setLayout(vboxGeoSite)

        self.createGeoSiteEditorPanelSignals()

        return self.groupgeoSite
    
    def createGeoSiteEditorPanelSignals(self):
        self.btntableWidgetGeoSiteOpen.clicked.connect(self.ongeoSiteFileOpen)
        self.comboBoxCodeTag.currentIndexChanged.connect(self.oncomboBoxCodeTagChanged)
        self.btnCodeTagNew.clicked.connect(self.onbtnCodeTagNew)
    
    def onbtnCodeTagNew(self):
        CodeTag = self.lineEditCodeTag.text()
        if CodeTag and CodeTag not in self.CodeTagList:
            self.comboBoxCodeTag.insertItem(0, CodeTag)
            self.comboBoxCodeTag.setCurrentIndex(0)
            self.tableViewGeoSitemodel.setRowCount(0)
            
    def oncomboBoxCodeTagChanged(self, e):
        pass
    
    

    def ongeoSiteFileOpen(self):
        fileName = self.openGeoSiteFileDialog()
        if fileName:
            with open(fileName, "rb") as f:
                self.geoSiteList.ParseFromString(f.read())
        
        self.settingGeoSiteTableWidget()

    def settingGeoSiteTableWidget(self):
        for site in self.geoSiteList.entry:
            self.CodeTagList.add(site.country_code)
        
        if self.CodeTagList:
            self.comboBoxCodeTag.addItems(self.CodeTagList)
            for row, data in enumerate(self.geoSiteList.entry[0].domain):
                self.setGeoSiteTableView(row, data)
                
    def setGeoSiteTableView(self, row, data):
        self.tableViewGeoSitemodel.setRowCount(row+1)
        domainValueIndex = self.tableViewGeoSitemodel.index(row, 0, QModelIndex())
        typeIndex = self.tableViewGeoSitemodel.index(row, 1, QModelIndex())
        self.tableViewGeoSitemodel.setData(domainValueIndex, str(data.value))
        self.tableViewGeoSitemodel.setData(typeIndex, self.domainType[int(data.type)])

    def openGeoSiteFileDialog(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(
            self,
            self.translate("geoSiteEditorPanel",  "Open Geo Data File"),
            "",
            self.translate("geoSiteEditorPanel", "Geo Data file (*.dat)"),
            options = options)
        if (filePath):
            return filePath

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = GeoSiteEditorPanel()
    ex.createGeoSiteEditorPanel().show()
    ex.setGeometry(300, 300, 1024, 1000)
    sys.exit(app.exec_())
