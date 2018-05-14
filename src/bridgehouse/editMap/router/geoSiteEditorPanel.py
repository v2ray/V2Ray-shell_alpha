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
        self.GeoSiteList = geoSite_pb2.GeoSiteList()
        self.CodeTagList = set()
        self.GeoSiteDict = {}

    def createGeoSiteEditorPanel(self):
        self.groupgeoSite = QGroupBox(self.translate("geoSiteEditorPanel", "GeoSite Editor"))

        labelCodeTag = QLabel(self.translate("geoSiteEditorPanel", "Code Tag"))
        self.comboBoxCodeTag = toolbox.MyComboBox(self)
        self.btnCodeTagNew = QPushButton(self.translate("geoSiteEditorPanel", "New Domain Sites"))
        self.lineEditCodeTag = QLineEdit()

        gridCodeTag = QGridLayout()
        gridCodeTag.addWidget(labelCodeTag, 0, 0, 1, 1)
        gridCodeTag.addWidget(self.comboBoxCodeTag, 0, 1, 1, 1)
        gridCodeTag.addWidget(self.btnCodeTagNew, 1, 0, 1, 1, Qt.AlignLeft)
        gridCodeTag.addWidget(self.lineEditCodeTag, 1, 1, 1, 1, Qt.AlignLeft)
        
        self.btntableWidgetGeoSiteOpen = QPushButton(self.translate("geoSiteEditorPanel", "Open"))
        self.btntableWidgetImport = QPushButton(self.translate("geoSiteEditorPanel", "Import..."))
        self.btntableWidgetExport = QPushButton(self.translate("geoSiteEditorPanel", "Export..."))
        self.btntableWidgetNew = QPushButton(self.translate("geoSiteEditorPanel", "New"))
        self.btntableWidgetDelete = QPushButton(self.translate("geoSiteEditorPanel", "Delete"))
        
        vboxtableBtn = QVBoxLayout()
        vboxtableBtn.addStretch()
        vboxtableBtn.addWidget(self.btntableWidgetGeoSiteOpen)
        vboxtableBtn.addSpacing(1)
        vboxtableBtn.addWidget(self.btntableWidgetImport)
        vboxtableBtn.addWidget(self.btntableWidgetExport)
        vboxtableBtn.addStretch()
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
        
        if v2rayshellDebug:
            self.__debugBtncountry_code = QPushButton("__country_code", self)
            vboxGeoSite.addWidget(self.__debugBtncountry_code)
            self.__debugBtncountry_code.clicked.connect(self.__show_country_code)
            

        return self.groupgeoSite
    
    def createGeoSiteEditorPanelSignals(self):
        self.btntableWidgetGeoSiteOpen.clicked.connect(self.ongeoSiteFileOpen)
        self.comboBoxCodeTag.previousTextChanged.connect(
            self.oncomboBoxCodeTagChanged)
        self.btnCodeTagNew.clicked.connect(self.onbtnCodeTagNew)
    
    def onbtnCodeTagNew(self):
        CodeTag = self.lineEditCodeTag.text()
        if CodeTag and CodeTag not in self.CodeTagList:
            self.comboBoxCodeTag.insertItem(0, CodeTag)
            self.comboBoxCodeTag.setCurrentIndex(0)
            self.tableViewGeoSitemodel.setRowCount(0)
            self.addNewGeoSite(CodeTag)

    def addNewGeoSite(self, CodeTag):
        self.GeoSiteDict[CodeTag] = []
        self.CodeTagList.add(CodeTag)
        self.lineEditCodeTag.clear()

    def oncomboBoxCodeTagChanged(self, oldText, newText):
        '''
        self.tableViewGeoSitemodel.setRowCount(0)
        if e in self.GeoSiteDict:
            for row, data in enumerate(self.GeoSiteDict[e]):
                self.setGeoSiteTableView(row, data)
        '''

    def ongeoSiteFileOpen(self):
        fileName = self.openGeoSiteFileDialog()
        if fileName:
            with open(fileName, "rb") as f:
                self.GeoSiteList.ParseFromString(f.read())

        codeTag = None
        for site in self.GeoSiteList.entry:
            self.CodeTagList.add(site.country_code)
            self.GeoSiteDict[site.country_code] = []
            self.resetComboBoxCodeTag()
            for data in site.domain:
                t = {}
                t["type"] = self.domainType[int(data.type)]
                t["value"] = data.value
                self.GeoSiteDict[site.country_code].append(t)
            if not codeTag:
                codeTag = site.country_code
                self.comboBoxCodeTag.setCurrentText(codeTag)
                for row, data in enumerate(site.domain):
                    t = {}
                    t["type"] = self.domainType[int(data.type)]
                    t["value"] = data.value
                    self.setGeoSiteTableView(row, t)
            else:
                continue

    def resetComboBoxCodeTag(self):
        self.comboBoxCodeTag.clear()
        self.comboBoxCodeTag.addItems(self.CodeTagList)        
        
    def setGeoSiteTableView(self, row, data):
        self.tableViewGeoSitemodel.setRowCount(row+1)
        domainValueIndex = self.tableViewGeoSitemodel.index(row, 0, QModelIndex())
        typeIndex = self.tableViewGeoSitemodel.index(row, 1, QModelIndex())
        self.tableViewGeoSitemodel.setData(domainValueIndex, data["value"])
        self.tableViewGeoSitemodel.setData(typeIndex, data["type"])

    def openGeoSiteFileDialog(self, _type=None):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(
            self,
            self.translate("geoSiteEditorPanel",  "Open Geo Data File"),
            "",
            self.translate("geoSiteEditorPanel", "Geo Data file (*.dat)"),
            options = options)
        if (filePath):
            self.geoSiteDataClear()
            return filePath
    
    def geoSiteDataClear(self):
        self.tableViewGeoSitemodel.setRowCount(0)
        self.comboBoxCodeTag.clear()
        self.GeoSiteDict.clear()
        self.GeoSiteList.Clear()
        self.CodeTagList.clear()
    
    def __show_country_code(self):
        for i in self.GeoSiteList.entry:
            print(i.country_code)

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = GeoSiteEditorPanel()
    ex.createGeoSiteEditorPanel().show()
    ex.setGeometry(300, 300, 1024, 1000)
    sys.exit(app.exec_())
