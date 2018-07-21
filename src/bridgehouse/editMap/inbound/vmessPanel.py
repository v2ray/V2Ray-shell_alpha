#!/usr/bin/env python3

from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QSpinBox,
                             QHBoxLayout, QVBoxLayout, QListView,
                             QTableWidget, QAbstractItemView, QPushButton,
                             QGroupBox, QComboBox, QTableWidgetItem,
                             QCheckBox, QTableView)
from PyQt5.QtCore import QFileInfo, QCoreApplication, Qt
from PyQt5.Qt import QStandardItemModel, QModelIndex
from _operator import index

listMethod = "aes-128-cfb", "aes-128-gcm", "chacha20-poly1305", "auto", "none"
import sys, uuid, copy

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    # this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-4]))

from bridgehouse.editMap.inbound import logbook
from bridgehouse.editMap.toolbox import toolbox


class InboundVmessPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.inboundVmessJSONFile = {
                                    "clients": [
                                        {
                                            "id": "27848739-7e62-4138-9fd3-098a63964b6b",
                                            "level": 10,
                                            "alterId": 30,
                                            "email": "love@v2ray.com"
                                            }
                                                ],
                                     "default": {
                                         "level": 10,
                                         "alterId": 30
                                         },
                                     "detour": {
                                         "to": "tag_to_detour"
                                         },
                                     "disableInsecureEncryption": False
                                     }
        self.translate = QCoreApplication.translate
        
        self.labelUserVmessPanel = (
            self.translate("InboundVmessPanel", "Email"),
            self.translate("InboundVmessPanel", "Level"),
            self.translate("InboundVmessPanel", "AlterID"),
            self.translate("InboundVmessPanel", "UUID"))
        
    def createVmessSettingPanel(self):
        labelDetourTo = QLabel(
            self.translate("InboundVmessPanel", "Detour To InboundDetour: "), self)
        self.comboBoxInVmessInboundTags = QComboBox()
        self.checkBoxdisableInsecureEncryption = QCheckBox(
            self.translate("InboundVmessPanel", "Disable Insecure Encryption"), self)
        self.checkBoxdisableInsecureEncryption.setChecked(False)

        self.btnInVmessNew = QPushButton(
            self.translate("InboundVmessPanel", "New"), self)
        self.btnInVmessDelete = QPushButton(
            self.translate("InboundVmessPanel", "Delete"), self)

        self.comboBoxInVmessInboundTags.setView(QListView())
        # self.comboBoxInVmessInboundTags.setStyleSheet("QComboBox {min-width: 128px; }" "QComboBox QAbstractItemView::item {min-width: 128px; }")
        
        hboxDetourTo = QHBoxLayout()
        hboxDetourTo.addWidget(labelDetourTo)
        hboxDetourTo.addWidget(self.comboBoxInVmessInboundTags)
        # hboxDetourTo.addStretch()

        vboxInVmessBtn = QVBoxLayout()
        vboxInVmessBtn.addWidget(QLabel())
        vboxInVmessBtn.addWidget(QLabel())
        vboxInVmessBtn.addWidget(QLabel())
        vboxInVmessBtn.addWidget(QLabel())
        vboxInVmessBtn.addWidget(self.btnInVmessNew)
        vboxInVmessBtn.addWidget(self.btnInVmessDelete)

        UUIDdelegate = toolbox.UUIDLineEditDelegate(
            self.translate("InboundVmessPanel", "Gerate UUID"))

        self.model = QStandardItemModel(0, 4)
        self.tableViewInVmessUser = tableViewUser = QTableView(self)
        tableViewUser.setModel(self.model)
        self.model.setHorizontalHeaderLabels(self.labelUserVmessPanel)
        tableViewUser.setSelectionMode(QAbstractItemView.SingleSelection)
        tableViewUser.setSelectionBehavior(QAbstractItemView.SelectRows)

        tableViewUser.setItemDelegateForColumn(3, UUIDdelegate)
        hboxtableViewUser = QHBoxLayout()
        hboxtableViewUser.addWidget(tableViewUser)
        hboxtableViewUser.addLayout(vboxInVmessBtn)
        
        vboxSetting = QVBoxLayout()
        vboxSetting.addLayout(hboxtableViewUser)
        
        self.groupBoxClientsSetting = groupBoxClientsSetting = QGroupBox(
            self.translate("InboundVmessPanel", "Clients: "), self)
        groupBoxClientsSetting.setLayout(vboxSetting)
        groupBoxClientsSetting.setCheckable(True)
        groupBoxClientsSetting.setChecked(True)
        
        vboxVmessPanel = QVBoxLayout()
        vboxVmessPanel.addLayout(hboxDetourTo)
        vboxVmessPanel.addWidget(self.checkBoxdisableInsecureEncryption)
        vboxVmessPanel.addWidget(self.createVmessDefaultSettingPanel())
        vboxVmessPanel.addWidget(groupBoxClientsSetting)

        self.createInboundVmessPanelSignals()

        if (v2rayshellDebug):
            self.__debugBtn = QPushButton("__debugTest", self)
            vboxVmessPanel.addWidget(self.__debugBtn)
            self.__debugBtn.clicked.connect(self.__debugTest)
            self.settingInboundVmessPanelFromJSONFile(self.inboundVmessJSONFile, True)

        groupBoxVmessPanel = QGroupBox(
            self.translate("InboundVmessPanel", "Vmess"), self)
        groupBoxVmessPanel.setLayout(vboxVmessPanel)

        return groupBoxVmessPanel
    
    def createVmessDefaultSettingPanel(self):
        labelDefaultLevel = QLabel(
            self.translate("InboundVmessPanel", "Level: "), self)
        self.spinBoxDefaultLevel = QSpinBox()
        labelAlterID = QLabel(
            self.translate("InboundVmessPanel", "AlterID: "), self)
        self.spinBoxDefaultAlterID = QSpinBox()
            
        self.spinBoxDefaultLevel.setRange(0, 100)
        self.spinBoxDefaultLevel.setValue(10)
        self.spinBoxDefaultAlterID.setRange(0, 65535)
        self.spinBoxDefaultAlterID.setValue(30)
        
        self.groupBoxDefault = groupBoxDefault = QGroupBox(
            self.translate("InboundVmessPanel", "Default: "), self)
        hboxDefault = QHBoxLayout()
        hboxDefault.addWidget(labelDefaultLevel)
        hboxDefault.addWidget(self.spinBoxDefaultLevel)
        hboxDefault.addWidget(labelAlterID)
        hboxDefault.addWidget(self.spinBoxDefaultAlterID)
        hboxDefault.addStretch()
        groupBoxDefault.setCheckable(True)
        groupBoxDefault.setChecked(False)
        groupBoxDefault.setLayout(hboxDefault)

        return groupBoxDefault
    
    def createInboundVmessPanelSignals(self):
        self.btnInVmessDelete.clicked.connect(self.onbtnInVmessDelete)
        self.btnInVmessNew.clicked.connect(self.onbtnInVmessNew)
        
    def onbtnInVmessNew(self):
        row = self.model.rowCount()
        if not row:
            self.model.setRowCount(row+1)
            self.setRowData(row)
        else:
            if (self.model.index(row-1, 3, QModelIndex()).data()):
                self.model.setRowCount(row+1)
                self.setRowData(row)

    def setRowData(self, row, email=None, level=None, alterID=None, vmessUUID=None):
        indexEmail = self.model.index(row, 0, QModelIndex())
        indexLevel = self.model.index(row, 1, QModelIndex())
        indexAlterID = self.model.index(row, 2, QModelIndex())
        indexUUID = self.model.index(row, 3, QModelIndex())
        
        self.model.setData(indexEmail, "" if not email else email)
        self.model.setData(indexLevel, 0 if not level else level)
        self.model.setData(indexAlterID, 0 if not alterID else alterID)
        self.model.setData(indexUUID, 0 if not vmessUUID else vmessUUID)
        try:
            if level: self.treasureChest.addLevel(int(level))
            if email: self.treasureChest.addEmail(str(email))
        except Exception: pass

    def onbtnInVmessDelete(self):
        row = self.tableViewInVmessUser.selectedIndexes()
        if row:
            self.model.removeRow(row[0].row())
 
    def settingInboundVmessPanelFromJSONFile(self, inboundVmessJSONFile=None, openFromJSONFile=False):
        logbook.setisOpenJSONFile(openFromJSONFile)
        detour = True; defaultLevelAlterID = True; client = True
        
        if (not inboundVmessJSONFile): inboundVmessJSONFile = {}

        try:
            inboundVmessJSONFile["detour"]
            inboundVmessJSONFile["detour"]["to"]
        except KeyError as e:
            logbook.writeLog("InboundVmess", "KeyError", e)
            inboundVmessJSONFile["detour"] = {}
            inboundVmessJSONFile["detour"]["to"] = ""
            detour = False
            
        try:
            inboundVmessJSONFile["disableInsecureEncryption"]
        except KeyError as e:
            logbook.writeLog("InboundVmess", "KeyError", e)
            inboundVmessJSONFile["disableInsecureEncryption"] = False
            
        try:
            inboundVmessJSONFile["default"]
        except KeyError as e:
            logbook.writeLog("InboundVmess", "KeyError", e)
            inboundVmessJSONFile["default"] = {}
            inboundVmessJSONFile["default"]["level"] = 10
            inboundVmessJSONFile["default"]["alterId"] = 30
            defaultLevelAlterID = False

        def settingdefaultLevelAlterID(level=10, alterid=30, default=True):
            self.spinBoxDefaultLevel.setValue(level)
            self.spinBoxDefaultAlterID.setValue(alterid)
            self.groupBoxDefault.setChecked(default)
            try: self.treasureChest.addLevel(self.spinBoxDefaultLevel.value())
            except Exception: pass
            
        try:
            inboundVmessJSONFile["clients"]
        except KeyError as e:
            logbook.writeLog("InboundVmess", "KeyError", e)
            inboundVmessJSONFile["clients"] = []
            client = False
            
        if (inboundVmessJSONFile["disableInsecureEncryption"]):
            self.checkBoxdisableInsecureEncryption.setChecked(True)    

        if (detour):
            self.comboBoxInVmessInboundTags.insertItem(self.comboBoxInVmessInboundTags.currentIndex(),
                                                        str(inboundVmessJSONFile["detour"]["to"]))
            self.comboBoxInVmessInboundTags.setCurrentText(str(inboundVmessJSONFile["detour"]["to"]))
                
        if (defaultLevelAlterID):
            try:
                settingdefaultLevelAlterID(int(inboundVmessJSONFile["default"]["level"]),
                                           int(inboundVmessJSONFile["default"]["alterId"]),
                                           True)
            except KeyError as e:
                logbook.writeLog("InboundVmess Default Level and AlterID", "KeyError", e)
                settingdefaultLevelAlterID()
            except (TypeError, ValueError) as e:
                logbook.writeLog("InboundVmess Default Level and AlterID", "ValueError or TypeError", e)
                settingdefaultLevelAlterID()
        elif (not defaultLevelAlterID):
            settingdefaultLevelAlterID(default=False)
            
        if (client):
            self.groupBoxClientsSetting.setChecked(True)
            clientsNumber = len(inboundVmessJSONFile["clients"])
            clients = inboundVmessJSONFile["clients"]
            if (clientsNumber):
                for r, i in enumerate(clients):
                    self.model.setRowCount(r+1)
                    self.setRowData(r, i["email"], i["level"], i["alterId"], i["id"])
                    try:
                        self.treasureChest.addLevel(int(i["level"]))
                        self.treasureChest.addLevel(int(i["email"]))
                    except Exception: pass
                    
            else:
                self.groupBoxClientsSetting.setChecked(False)
        else:
            self.groupBoxClientsSetting.setChecked(False)
    
    def createInboundVmessJSONFile(self):
        inboundVmessJSONFile = {}
        inboundVmessJSONFile["clients"] = []
        inboundVmessJSONFile["default"] = {}
        inboundVmessJSONFile["detour"] = {}
            
        clientsNumber = self.model.rowCount()
        if (clientsNumber and self.groupBoxClientsSetting.isChecked()):
            clients = []
            for i in range(0, clientsNumber):
                client = {}
                indexEmail = self.model.index(i, 0, QModelIndex())
                indexLevel = self.model.index(i, 1, QModelIndex())
                indexalterID = self.model.index(i, 2, QModelIndex())
                indexUUID= self.model.index(i, 3, QModelIndex())
                client["email"] = indexEmail.data()
                client["level"] = indexLevel.data()
                client["alterId"] = indexalterID.data()
                client["id"] = indexUUID.data()
                clients.append(copy.deepcopy(client))    
            inboundVmessJSONFile["clients"] = copy.deepcopy(clients)
        else:
            inboundVmessJSONFile["clients"] = []
            
        if (self.groupBoxDefault.isChecked()):
            inboundVmessJSONFile["default"]["level"] = self.spinBoxDefaultLevel.value()
            inboundVmessJSONFile["default"]["alterId"] = self.spinBoxDefaultAlterID.value()
            try:
                self.treasureChest.addLevel(self.spinBoxDefaultLevel.value())
            except Exception:
                pass
        else:
            del inboundVmessJSONFile["default"]
            
        InboundTags = self.comboBoxInVmessInboundTags.currentText()
        if (InboundTags):
            inboundVmessJSONFile["detour"]["to"] = InboundTags
        else:
            del inboundVmessJSONFile["detour"]
        
        if (self.checkBoxdisableInsecureEncryption.isChecked()):
            inboundVmessJSONFile["disableInsecureEncryption"] = True
        else:
            inboundVmessJSONFile["disableInsecureEncryption"] = False
            
        return inboundVmessJSONFile
    
    def clearinboundVmessPanel(self):
        self.model.setRowCount(0)
        self.groupBoxClientsSetting.setChecked(False)
        self.groupBoxDefault.setChecked(False)
        self.spinBoxDefaultAlterID.setValue(30)
        self.spinBoxDefaultLevel.setValue(10)
        self.comboBoxInVmessInboundTags.setCurrentIndex(0)
        self.checkBoxdisableInsecureEncryption.setChecked(False)
        
    def __debugTest(self):
        import json
        print(json.dumps(self.createInboundVmessJSONFile(), indent=4, sort_keys=False))

        
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = InboundVmessPanel()
    ex.createVmessSettingPanel()
    ex.setGeometry(200, 100, 800, 768)
    ex.show()
    sys.exit(app.exec_())
