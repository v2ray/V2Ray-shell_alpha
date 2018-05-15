#!/usr/bin/env python3

from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QHBoxLayout, QGroupBox, QPushButton, 
                             QAbstractItemView, QVBoxLayout,
                             QGridLayout, QFileDialog, QTableView, QDialog,
                             QApplication, QComboBox, QCheckBox, QToolTip)
from PyQt5.QtCore import QFileInfo, QCoreApplication, Qt, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QCursor

import sys, copy


v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    # this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-4]))

from bridgehouse.editMap.toolbox import toolbox
from bridgehouse.editMap.router import geoSite_pb2, readgfwlist

class GeoSiteEditorPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.translate = QCoreApplication.translate
        self.labelGeoSiteTabel = (
            self.translate("geoSiteEditorPanel", "Domain"),
            self.translate("geoSiteEditorPanel", "Type"))
        self.domainType = ["Plain", "Regex", "Domain"]
        self.GeoSiteList = geoSite_pb2.GeoSiteList()
        self.CodeTagList = set()
        self.GeoSiteDict = dict()
        self.DomainType = (geoSite_pb2.Domain.Plain,
                           geoSite_pb2.Domain.Regex,
                           geoSite_pb2.Domain.Domain)

    def createGeoSiteEditorPanel(self):
        self.groupgeoSite = QGroupBox(self.translate("geoSiteEditorPanel", "GeoSite Editor"))

        labelCodeTag = QLabel(self.translate("geoSiteEditorPanel", "Code Tag"))
        self.btnCodeTagDelete = QPushButton(self.translate("geoSiteEditorPanel", "Delete Code Tag"))
        self.comboBoxCodeTag = toolbox.MyComboBox(self)
        self.btnCodeTagNew = QPushButton(self.translate("geoSiteEditorPanel", "New Code Tag"))
        self.lineEditCodeTag = QLineEdit()
        
        hboxCodeTag = QHBoxLayout()
        hboxCodeTag.addWidget(self.comboBoxCodeTag)
        hboxCodeTag.addWidget(self.btnCodeTagDelete)

        gridCodeTag = QGridLayout()
        gridCodeTag.addWidget(labelCodeTag, 0, 0, 1, 1)
        gridCodeTag.addLayout(hboxCodeTag, 0, 1, 1, 1)
        gridCodeTag.addWidget(self.btnCodeTagNew, 1, 0, 1, 1, Qt.AlignLeft)
        gridCodeTag.addWidget(self.lineEditCodeTag, 1, 1, 1, 2, Qt.AlignLeft)
        
        self.btnTableViewGeoSiteOpen = QPushButton(self.translate("geoSiteEditorPanel", "Open"))
        self.btnTableViewImport = QPushButton(self.translate("geoSiteEditorPanel", "Import..."))
        self.btnTableViewExport = QPushButton(self.translate("geoSiteEditorPanel", "Export..."))
        self.btnTableViewNew = QPushButton(self.translate("geoSiteEditorPanel", "New"))
        self.btnTableViewDelete = QPushButton(self.translate("geoSiteEditorPanel", "Delete"))
        self.btnTableViewImport.setEnabled(False)
        
        vboxtableBtn = QVBoxLayout()
        vboxtableBtn.addStretch()
        vboxtableBtn.addWidget(self.btnTableViewGeoSiteOpen)
        vboxtableBtn.addSpacing(1)
        vboxtableBtn.addWidget(self.btnTableViewImport)
        vboxtableBtn.addWidget(self.btnTableViewExport)
        vboxtableBtn.addStretch()
        vboxtableBtn.addWidget(self.btnTableViewNew)
        vboxtableBtn.addWidget(self.btnTableViewDelete)
        
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
            hdebugBox = QHBoxLayout()
            self.__debugBtncountry_code = QPushButton("__country_code", self)
            self.__debugBtnGeoSiteDict = QPushButton("__GeoSiteDict", self)
            hdebugBox.addWidget(self.__debugBtncountry_code)
            hdebugBox.addWidget(self.__debugBtnGeoSiteDict)
            vboxGeoSite.addLayout(hdebugBox)
            self.__debugBtncountry_code.clicked.connect(self.__show_country_code)
            self.__debugBtnGeoSiteDict.clicked.connect(self.__show_GeoSiteDict)

        return self.groupgeoSite
    
    def createGeoSiteEditorPanelSignals(self):
        self.btnTableViewGeoSiteOpen.clicked.connect(self.ongeoSiteFileOpen)
        self.comboBoxCodeTag.previousTextChanged.connect(self.oncomboBoxCodeTagChanged)
        self.btnCodeTagNew.clicked.connect(self.onbtnCodeTagNew)
        self.btnTableViewNew.clicked.connect(self.onbtnTableViewNew)
        self.btnTableViewDelete.clicked.connect(self.onbtnTableViewDelete)
        self.btnTableViewExport.clicked.connect(self.onbtnTableViewExport)
        self.btnTableViewImport.clicked.connect(self.importCustomizedListPanel)
        self.btnCodeTagDelete.clicked.connect(self.onbtnCodeTagDelete)
        
    def onbtnCodeTagDelete(self):
        tagIndex = self.comboBoxCodeTag.currentIndex()
        CodeTag = self.comboBoxCodeTag.currentText()
        if tagIndex != -1:
            self.comboBoxCodeTag.removeItem(tagIndex)
            del self.GeoSiteDict[CodeTag]
            self.CodeTagList.remove(CodeTag)

    def onbtnTableViewExport(self):
        self.rebackupTabelDataToGeoSiteDict(self.comboBoxCodeTag.currentText())
        self.addDatatoGeoSiteList()

        fileName = self.saveGeoSiteFileDialog()
        if fileName:
            with open(fileName, "wb") as f:
                f.write(self.GeoSiteList.SerializeToString())

    def addDatatoGeoSiteList(self):
        self.GeoSiteList.Clear()
        j = 0
        entry = list()
        for i, k in self.GeoSiteDict.items():
            entry.append(self.GeoSiteList.entry.add())
            entry[j].country_code = i
            for c in k:
                domain = entry[j].domain.add()
                domain.type = self.DomainType[self.domainType.index(c["type"])]
                domain.value = c["value"]
            j += 1
        
    def onbtnTableViewDelete(self):
        if not self.tableViewGeoSitemodel.rowCount():
            return
        currentRow = self.tableViewIGeoSite.currentIndex()
        self.tableViewGeoSitemodel.removeRow(currentRow.row())
    
    def onbtnTableViewNew(self):
        row = self.tableViewGeoSitemodel.rowCount()
        if not row:
            self.tableViewGeoSitemodel.setRowCount(row+1)
        else:
            typeIndex = self.tableViewGeoSitemodel.index(row-1, 0)
            valueIndex = self.tableViewGeoSitemodel.index(row-1, 1)
            if typeIndex.data() and valueIndex.data():
                self.tableViewGeoSitemodel.setRowCount(row+1)

    def onbtnCodeTagNew(self):
        CodeTag = self.lineEditCodeTag.text()
        if not self.comboBoxCodeTag.count():
            self.addNewGeoSite(CodeTag)
            self.comboBoxCodeTag.addItem(CodeTag)
            return
        
        if CodeTag and CodeTag not in self.CodeTagList:
            self.addNewGeoSite(CodeTag)
            self.comboBoxCodeTag.addItem(CodeTag)
            self.comboBoxCodeTag.setCurrentText(CodeTag)
            self.tableViewGeoSitemodel.setRowCount(0)

    def addNewGeoSite(self, CodeTag):
        self.GeoSiteDict[CodeTag] = list()
        self.CodeTagList.add(CodeTag)
        self.lineEditCodeTag.clear()

    def oncomboBoxCodeTagChanged(self, oldText, newText):
        self.rebackupTabelDataToGeoSiteDict(CodeTag = oldText)
        self.tableViewGeoSitemodel.setRowCount(0)
        if newText:
            data = self.GeoSiteDict[newText]
            for row, data in enumerate(data):
                self.setGeoSiteTableView(row, data)
        self.btnTableViewImport.setEnabled(True)
        
    def rebackupTabelDataToGeoSiteDict(self, CodeTag=None):
        if not CodeTag:
            CodeTag = self.comboBoxCodeTag.currentText()

        self.GeoSiteDict[CodeTag] = list()
        for i in range(self.tableViewGeoSitemodel.rowCount()):
            valueIndex = self.tableViewGeoSitemodel.index(i, 0)
            typeIndex = self.tableViewGeoSitemodel.index(i, 1)
            t = {}
            t["type"] = typeIndex.data()
            t["value"] = valueIndex.data()
            self.GeoSiteDict[CodeTag].append(t)

    def ongeoSiteFileOpen(self):
        fileName = self.openGeoSiteFileDialog()
        if fileName:
            with open(fileName, "rb") as f:
                self.GeoSiteList.ParseFromString(f.read())
        try:
            entry = self.GeoSiteList.entry
        except:
            # TODO
            # open a file type is wrong.
            pass
        for d in entry:
            self.GeoSiteDict[d.country_code] = list()
            self.CodeTagList.add(d.country_code)
            for k in d.domain:
                t = dict()
                t['type'] = self.domainType[int(k.type)]
                t['value'] = k.value
                self.GeoSiteDict[d.country_code].append(t)
                del t
        self.initTabelView()

    def initTabelView(self):
        if self.GeoSiteDict:
            codeTag = None
            self.tableViewGeoSitemodel.setRowCount(0)
            for i, k in self.GeoSiteDict.items():
                
                codeTag = i
                for row, data in enumerate(k):
                    self.setGeoSiteTableView(row, data)
                break
            self.resetComboBoxCodeTag()
            self.comboBoxCodeTag.setCurrentText(codeTag)

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
        title = self.translate("geoSiteEditorPanel",  "Open Geo Data File")
        fliter = self.translate("geoSiteEditorPanel", """Geo Data file (*.dat);;All file (*)""")
        if _type:
            title = self.translate("geoSiteEditorPanel",  "Import Customized List File")
            fliter = self.translate("geoSiteEditorPanel", """All file (*)""")

        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, title, "", fliter, options = options)

        if (filePath):
            if not _type:
                self.geoSiteDataClear()
            return filePath
        
    def saveGeoSiteFileDialog(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getSaveFileName(
            self,
            self.translate("geoSiteEditorPanel",  "Export Geo Data File"),
            "",
            self.translate("geoSiteEditorPanel", """Geo Data file (*.dat);;All file (*)"""),
            options = options)
        if (filePath):
            return filePath
        
    def importCustomizedListPanel(self):
        labelTypes = QLabel(self.translate("geoSiteEditorPanel", "Types: "))
        comboboxTypes = QComboBox()
        comboboxTypes.addItems(self.domainType)
        labelCodeTag = QLabel(self.translate("geoSiteEditorPanel", "Code Tag Name: "))
        
        # TODO
        # user can name code tag here
        # if code tag is not in self.CodeTagList, that create a new 
        lineEditCodeTag = QLineEdit()
        lineEditCodeTag.setReadOnly(True)
        if self.comboBoxCodeTag.currentText():
            lineEditCodeTag.setText(self.comboBoxCodeTag.currentText())

        def setcomboboxTypes(e):
            if e:
                comboboxTypes.setCurrentText("Regex")
            else:
                comboboxTypes.setCurrentText("Plain")
        checkBoxGFWList = QCheckBox(self.translate("geoSiteEditorPanel", "gfwlist.txt"))
        btnOpen = QPushButton(self.translate("geoSiteEditorPanel", "Open"))
        btnCancel = QPushButton(self.translate("geoSiteEditorPanel", "Cancel"))

        grid = QGridLayout()
        hboxBtn = QHBoxLayout()
        vboxPanel = QVBoxLayout()

        hboxBtn.addStretch()
        hboxBtn.addWidget(btnOpen)
        hboxBtn.addWidget(btnCancel)
        grid.addWidget(labelTypes, 0, 0)
        grid.addWidget(comboboxTypes, 0, 1)
        grid.addWidget(labelCodeTag, 1, 0)
        grid.addWidget(lineEditCodeTag, 1, 1)
        grid.addWidget(checkBoxGFWList, 2, 0)
        vboxPanel.addLayout(grid)
        vboxPanel.addLayout(hboxBtn)

        self.customizedListPanel = customizedListPanel = QDialog()
        customizedListPanel.setAttribute(Qt.WA_DeleteOnClose)
        customizedListPanel.setWindowTitle(
            self.translate("geoSiteEditorPanel", "Import Customized List"))
        customizedListPanel.move(
            QApplication.desktop().screen().rect().center()-customizedListPanel.rect().center())
        customizedListPanel.setLayout(vboxPanel)
        btnCancel.clicked.connect(customizedListPanel.close)
        btnOpen.clicked.connect(
            lambda: self.onbtnimport(
                btnOpen,
                lineEditCodeTag.text(),
                checkBoxGFWList.isChecked(),
                comboboxTypes.currentText()))
        checkBoxGFWList.clicked.connect(setcomboboxTypes)

        customizedListPanel.open()
        customizedListPanel.exec_()

    def onbtnimport(self, btn, codeTag, gfwlist, comboboxtype):
        if not codeTag or codeTag not in self.CodeTagList:
            # this tip will never reach here
            QToolTip.showText(QCursor.pos(),
                                  self.translate(
                                      "geoSiteEditorPanel",
                                      "You should name a code tag before import file."),
                                  btn)
            return
        fileName = self.openGeoSiteFileDialog(_type=True)
        if fileName:
            geosite = self.initComstomizedFileList(fileName, gfwlist)
            if geosite:
                self.setComstomizedListToTabel(geosite, comboboxtype)
                self.customizedListPanel.close()

    def initComstomizedFileList(self, path, gfwlist=False):
        geosite = list()
        openFile = None
        if gfwlist:
            geosite = copy.deepcopy(readgfwlist.openGWFLIST(path))
        else:
            with open(path, "r") as f:
                openFile = f.read()
        if openFile:
            for i in openFile.split("\n"):
                geosite.append(i)

        return geosite
    
    def setComstomizedListToTabel(self, geosite, _type="Plain"):
        for i in geosite:
            self.setGeoSiteTableView(
                self.tableViewGeoSitemodel.rowCount(),
                dict(value=i, type=_type))

    def geoSiteDataClear(self):
        self.tableViewGeoSitemodel.setRowCount(0)
        self.comboBoxCodeTag.clear()
        self.GeoSiteDict.clear()
        self.GeoSiteList.Clear()
        self.CodeTagList.clear()
    
    def __show_country_code(self):
        print(self.GeoSiteList.entry)
            
    def __show_GeoSiteDict(self):
        print(self.GeoSiteDict)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GeoSiteEditorPanel()
    vbox = QVBoxLayout()
    vbox.addWidget(ex.createGeoSiteEditorPanel())
    ex.setLayout(vbox)
    ex.setGeometry(300, 150, 1024, 800)
    ex.show()
    sys.exit(app.exec_())
