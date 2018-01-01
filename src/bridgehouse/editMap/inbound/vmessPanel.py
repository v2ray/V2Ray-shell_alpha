#!/usr/bin/env python3

from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QSpinBox,
                             QHBoxLayout, QVBoxLayout, QListView, 
                             QTableWidget, QAbstractItemView, QPushButton, 
                             QGroupBox, QComboBox, QTableWidgetItem)
from PyQt5.QtCore import QFileInfo, QCoreApplication

listMethod = "aes-128-cfb", "aes-128-gcm", "chacha20-poly1305", "auto", "none"
import sys, uuid, copy

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    ### this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.path().split("/")
    sys.path.append("/".join(srcPath[:-3]))

from bridgehouse.editMap.inbound import logbook

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
                                         }
                                     }
        self.translate = QCoreApplication.translate
        
        self.labelUserVmessPanel = (
            self.translate("InboundVmessPanel", "Email"), 
            self.translate("InboundVmessPanel", "Level"), 
            self.translate("InboundVmessPanel", "AlterID"),
            self.translate("InboundVmessPanel", "UUID"))
        
    def createVmessSettingPanel(self):
        labelDetourTo = QLabel(
            self.translate("InboundVmessPanel", "Detour To outboundDetour: "), self)
        self.comboBoxInVmessOutboundTags = QComboBox()
        labelEmail    = QLabel(
            self.translate("InboundVmessPanel", "Email: "), self)
        self.lineEditInVmessMail   = QLineEdit()
        labelUIID     = QLabel(
            self.translate("InboundVmessPanel", "UUID: "), self)
        self.lineEditInVmessUUID   = QLineEdit()
        labelAlterID  = QLabel(
            self.translate("InboundVmessPanel", "AlterID: "), self)
        labelLevel    = QLabel(
            self.translate("InboundVmessPanel", "Level: "), self)
        self.btnInVmessGenerate    = QPushButton(
            self.translate("InboundVmessPanel", "Generate UUID"), self)
        self.btnInVmessChange      = QPushButton(
            self.translate("InboundVmessPanel", "Modify"), self)
        self.btnInVmessClear       = QPushButton(
            self.translate("InboundVmessPanel", "Clear"), self)
        self.btnInVmessAdd         = QPushButton(
            self.translate("InboundVmessPanel", "Add"), self)
        self.btnInVmessDelete      = QPushButton(
            self.translate("InboundVmessPanel", "Delete"), self)
        self.spinBoxInVmessLevel   = QSpinBox()
        self.spinBoxInVmessAlterID = QSpinBox()
        
        self.spinBoxInVmessAlterID.setRange(0, 65535)
        self.spinBoxInVmessLevel.setRange(0, 65535)
        self.spinBoxInVmessLevel.setValue(10)
        self.spinBoxInVmessAlterID.setValue(30)
        self.lineEditInVmessUUID.setInputMask("HHHHHHHH-HHHH-HHHH-HHHH-HHHHHHHHHHHH; ")
        self.comboBoxInVmessOutboundTags.setView(QListView())
        #self.comboBoxInVmessOutboundTags.setStyleSheet("QComboBox {min-width: 128px; }" "QComboBox QAbstractItemView::item {min-width: 128px; }")
        
        hboxDetourTo = QHBoxLayout()
        hboxDetourTo.addWidget(labelDetourTo)
        hboxDetourTo.addWidget(self.comboBoxInVmessOutboundTags)
        #hboxDetourTo.addStretch()
        
        hboxID = QHBoxLayout()
        hboxID.addWidget(labelUIID)
        hboxID.addWidget(self.lineEditInVmessUUID)
        hboxID.addWidget(self.btnInVmessGenerate)
        
        hboxLevel = QHBoxLayout()
        hboxLevel.addWidget(labelLevel)
        hboxLevel.addWidget(self.spinBoxInVmessLevel)
        hboxLevel.addWidget(labelAlterID)
        hboxLevel.addWidget(self.spinBoxInVmessAlterID)
        hboxLevel.addStretch()
        
        hboxEmail = QHBoxLayout()
        hboxEmail.addWidget(labelEmail)
        hboxEmail.addWidget(self.lineEditInVmessMail)
        
        vboxInVmessBtn = QVBoxLayout()
        vboxInVmessBtn.addStretch()
        vboxInVmessBtn.addWidget(self.btnInVmessAdd)
        vboxInVmessBtn.addWidget(self.btnInVmessClear)
        vboxInVmessBtn.addWidget(self.btnInVmessChange)
        vboxInVmessBtn.addWidget(self.btnInVmessDelete)
        
        vboxSetting = QVBoxLayout()
        vboxSetting.addLayout(hboxID)
        vboxSetting.addLayout(hboxLevel)
        vboxSetting.addLayout(hboxEmail)
        
        self.tableWidgetInVmessUser = tableWidgetUser = QTableWidget(self)
        tableWidgetUser.setRowCount(0)
        tableWidgetUser.setColumnCount(4)
        tableWidgetUser.setHorizontalHeaderLabels(self.labelUserVmessPanel)
        tableWidgetUser.setSelectionMode(QAbstractItemView.SingleSelection)
        tableWidgetUser.setSelectionBehavior(QAbstractItemView.SelectRows)
        tableWidgetUser.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tableWidgetUser.horizontalHeader().setStretchLastSection(True)

        hboxTableWidgetUser = QHBoxLayout()
        hboxTableWidgetUser.addWidget(tableWidgetUser)
        hboxTableWidgetUser.addLayout(vboxInVmessBtn)
        
        vboxSetting.addLayout(hboxTableWidgetUser)
        
        self.groupBoxClientsSetting = groupBoxClientsSetting = QGroupBox(
            self.translate("InboundVmessPanel", "Clients: "), self)
        groupBoxClientsSetting.setLayout(vboxSetting)
        groupBoxClientsSetting.setCheckable(True)
        groupBoxClientsSetting.setChecked(True)
        
        vboxVmessPanel = QVBoxLayout()
        vboxVmessPanel.addLayout(hboxDetourTo)
        vboxVmessPanel.addWidget(self.createVmessDefaultSettingPanel())
        vboxVmessPanel.addWidget(groupBoxClientsSetting)
        
        if (v2rayshellDebug):
            self.__debugBtn = QPushButton("__debugTest", self)
            vboxVmessPanel.addWidget(self.__debugBtn)
            self.__debugBtn.clicked.connect(self.__debugTest)
            self.settingInboundVmessPanelFromJSONFile(self.inboundVmessJSONFile, True)
       
        groupBoxVmessPanel = QGroupBox(
            self.translate("InboundVmessPanel", "Vmess"), self)
        groupBoxVmessPanel.setLayout(vboxVmessPanel)

        self.createVmessPanelSignals()

        return groupBoxVmessPanel
    
    def createVmessDefaultSettingPanel(self):
        labelDefaultLevel          = QLabel(
            self.translate("InboundVmessPanel", "Level: "), self)
        self.spinBoxDefaultLevel   = QSpinBox()
        labelAlterID               = QLabel(
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
    
    def createVmessPanelSignals(self):
        self.btnInVmessClear.clicked.connect(self.onbtnInVmessClear)
        self.btnInVmessGenerate.clicked.connect(self.onbtnInVmessGenerate)
        self.btnInVmessAdd.clicked.connect(self.onbtnInVmessAdd)
        self.tableWidgetInVmessUser.itemSelectionChanged.connect(
            self.ontableWidgetInVmessUserSelectionChanged)
        self.btnInVmessDelete.clicked.connect(self.onbtnInVmessDelete)
        self.btnInVmessChange.clicked.connect(self.onbtnInVmessChange)
        
    def onbtnInVmessChange(self):
        row = self.tableWidgetInVmessUser.currentRow()
        self.tableWidgetInVmessUser.setItem(
            row, 0, QTableWidgetItem(self.lineEditInVmessMail.text()))
        self.tableWidgetInVmessUser.setItem(
            row, 3, QTableWidgetItem(self.lineEditInVmessUUID.text()))
        self.tableWidgetInVmessUser.setItem(
            row, 2, QTableWidgetItem(self.spinBoxInVmessAlterID.text()))
        self.tableWidgetInVmessUser.setItem(
            row, 1, QTableWidgetItem(self.spinBoxInVmessLevel.text()))
        self.tableWidgetInVmessUser.resizeColumnsToContents()
        
    def onbtnInVmessDelete(self):
        self.onbtnInVmessClear()
        self.tableWidgetInVmessUser.removeRow(self.tableWidgetInVmessUser.currentRow())

    def ontableWidgetInVmessUserSelectionChanged(self):
        row     = self.tableWidgetInVmessUser.currentRow()
        mail    = self.tableWidgetInVmessUser.item(row, 0)
        level   = self.tableWidgetInVmessUser.item(row, 1)
        alterID = self.tableWidgetInVmessUser.item(row, 2)
        uuid    = self.tableWidgetInVmessUser.item(row, 3)
        
        if (uuid):
            self.lineEditInVmessUUID.setText(uuid.text())
        else:
            self.lineEditInVmessUUID.clear()
            
        if (mail):
            self.lineEditInVmessMail.setText(mail.text())
        else:
            self.lineEditInVmessMail.clear()
        
        if (level):
            try: self.spinBoxInVmessLevel.setValue(int(level.text()))
            except Exception: pass
        else:
            self.spinBoxInVmessLevel.setValue(10)
        
        if (alterID):
            try:self.spinBoxInVmessAlterID.setValue(int(alterID.text()))
            except Exception: pass
        else:
            self.spinBoxInVmessAlterID.setValue(30)
        
    def onbtnInVmessAdd(self):
        boolUUID = self.validateUUID4("".join(self.lineEditInVmessUUID.text().split("-")))
        if (self.lineEditInVmessMail.text() == "" or (boolUUID == False)): return
        
        row = self.tableWidgetInVmessUser.rowCount()
        self.tableWidgetInVmessUser.setRowCount(row+1)  ### DO NOT use ++row, row maybe is ZERO
        self.tableWidgetInVmessUser.setItem(
            row, 3, QTableWidgetItem(self.lineEditInVmessUUID.text()))
        self.tableWidgetInVmessUser.setItem(
            row, 2, QTableWidgetItem(self.spinBoxInVmessAlterID.text()))
        self.tableWidgetInVmessUser.setItem(
            row, 1, QTableWidgetItem(self.spinBoxInVmessLevel.text()))
        self.tableWidgetInVmessUser.setItem(
            row, 0, QTableWidgetItem(self.lineEditInVmessMail.text()))
        self.tableWidgetInVmessUser.resizeColumnsToContents()
        self.onbtnInVmessClear()
        
    def onbtnInVmessGenerate(self):
        self.lineEditInVmessUUID.setText(self.createUUID())
        
    def onbtnInVmessClear(self):
        self.lineEditInVmessUUID.clear()
        self.spinBoxInVmessAlterID.setValue(30)
        self.spinBoxInVmessLevel.setValue(10)
        self.lineEditInVmessMail.clear()

    def settingInboundVmessPanelFromJSONFile(self, inboundVmessJSONFile = {}, openFromJSONFile = False):
        logbook.setisOpenJSONFile(openFromJSONFile)
        self.tableWidgetInVmessUser.setRowCount(0)
        detour = True; defaultLevelAlterID = True; client = True
        
        if (inboundVmessJSONFile == None): inboundVmessJSONFile ={}

        try:
            inboundVmessJSONFile["detour"]
            inboundVmessJSONFile["detour"]["to"]
        except KeyError as e:
            logbook.writeLog("InboundVmess", "KeyError", e)
            inboundVmessJSONFile["detour"] = {}
            inboundVmessJSONFile["detour"]["to"] = ""
            detour = False
            
        try:
            inboundVmessJSONFile["default"]
        except KeyError as e:
            logbook.writeLog("InboundVmess", "KeyError", e)
            inboundVmessJSONFile["default"] = {}
            inboundVmessJSONFile["default"]["level"] = 10
            inboundVmessJSONFile["default"]["alterId"] = 30
            defaultLevelAlterID = False

        def settingdefaultLevelAlterID(level = 10, alterid = 30, default = True):
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

        if (detour):
            self.comboBoxInVmessOutboundTags.insertItem(self.comboBoxInVmessOutboundTags.currentIndex(), 
                                                        str(inboundVmessJSONFile["detour"]["to"]))
            self.comboBoxInVmessOutboundTags.setCurrentText(str(inboundVmessJSONFile["detour"]["to"]))
                
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
        elif (defaultLevelAlterID == False):
            settingdefaultLevelAlterID(default = False)
            
        if (client):
            self.groupBoxClientsSetting.setChecked(True)
            clientsNumber = len(inboundVmessJSONFile["clients"])
            clients       = inboundVmessJSONFile["clients"]
            if (clientsNumber > 0):
                self.tableWidgetInVmessUser.setRowCount(clientsNumber)
                for i in range(clientsNumber):
                    try:
                        email = QTableWidgetItem(str(clients[i]["email"]))
                    except Exception: email = QTableWidgetItem("")
                    try:
                        level = QTableWidgetItem(str(clients[i]["level"]))
                    except Exception: level = QTableWidgetItem("")
                    try:
                        alterID = QTableWidgetItem(str(clients[i]["alterId"]))
                    except Exception: alterID = QTableWidgetItem("")
                    try:
                        uuidStr = QTableWidgetItem(str(clients[i]["id"]))
                    except Exception: uuidStr = QTableWidgetItem("")
                    
                    self.tableWidgetInVmessUser.setItem(i, 0, email)           
                    self.tableWidgetInVmessUser.setItem(i, 1, level)
                    self.tableWidgetInVmessUser.setItem(i, 2, alterID)
                    self.tableWidgetInVmessUser.setItem(i, 3, uuidStr)
                    self.tableWidgetInVmessUser.resizeColumnsToContents()

                    try:self.treasureChest.addLevel(clients[i]["level"])
                    except Exception: pass
                    try: self.treasureChest.addEmail(clients[i]["email"])
                    except Exception: pass
            else:
                self.groupBoxClientsSetting.setChecked(False)
        else:
            self.groupBoxClientsSetting.setChecked(False)
    
    def createInboundVmessJSONFile(self):
        inboundVmessJSONFile = {}
        inboundVmessJSONFile["clients"] = []
        inboundVmessJSONFile["default"] = {}
        inboundVmessJSONFile["detour"]  = {}
            
        clientsNumber = self.tableWidgetInVmessUser.rowCount()
        if (clientsNumber > 0 and self.groupBoxClientsSetting.isChecked()):
            clients = []
            for i in range(0, clientsNumber):
                client     = {}
                email   = self.tableWidgetInVmessUser.item(i, 0)
                level   = self.tableWidgetInVmessUser.item(i, 1)
                alterId = self.tableWidgetInVmessUser.item(i, 2)
                uuid      = self.tableWidgetInVmessUser.item(i, 3)
                if (email and level and alterId and uuid):
                    client["id"]      = uuid.text()
                    client["level"]   = int(level.text())
                    client["alterId"] = int(alterId.text())
                    client["email"]   = email.text()
                    try:
                        self.treasureChest.addLevel(client["level"])
                        self.treasureChest.addEmail(client["email"])
                    except Exception:
                        pass
                clients.append(copy.deepcopy(client))    
            inboundVmessJSONFile["clients"] = copy.deepcopy(clients)
        else:
            inboundVmessJSONFile["clients"] = []
            
        if (self.groupBoxDefault.isChecked()):
            inboundVmessJSONFile["default"]["level"]   = self.spinBoxDefaultLevel.value()
            inboundVmessJSONFile["default"]["alterId"] = self.spinBoxDefaultAlterID.value()
            try:
                self.treasureChest.addLevel(self.spinBoxDefaultLevel.value())
            except Exception:
                pass
        else:
            del inboundVmessJSONFile["default"]
            
        OutboundTags = self.comboBoxInVmessOutboundTags.currentText()
        if (OutboundTags != ""):
            inboundVmessJSONFile["detour"]["to"] = OutboundTags
        else:
            del inboundVmessJSONFile["detour"]
            
        return inboundVmessJSONFile
    
    def clearinboundVmessPanel(self):
        self.tableWidgetInVmessUser.setRowCount(0)
        self.groupBoxClientsSetting.setChecked(False)
        self.groupBoxDefault.setChecked(False)
        self.spinBoxDefaultAlterID.setValue(30)
        self.spinBoxDefaultLevel.setValue(10)
        self.spinBoxInVmessAlterID.setValue(30)
        self.spinBoxInVmessLevel.setValue(10)
        self.comboBoxInVmessOutboundTags.setCurrentIndex(0)
        self.lineEditInVmessMail.clear()
        self.lineEditInVmessUUID.clear()
        
    def createUUID(self):
        return str(uuid.uuid4())
    
    def validateUUID4(self, uuidString):
        try:
            uuid.UUID(uuidString, version = 4)
        except ValueError:
            return False
        return True

    def __debugTest(self):
        import json
        print(json.dumps(self.createInboundVmessJSONFile(), indent = 4, sort_keys = False))
        
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = InboundVmessPanel()
    ex.createVmessSettingPanel()
    ex.setGeometry(200, 100, 800, 768)
    ex.show()
    sys.exit(app.exec_())
