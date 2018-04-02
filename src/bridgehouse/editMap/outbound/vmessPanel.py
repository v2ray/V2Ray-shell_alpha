#!/usr/bin/env python3

from PyQt5.QtWidgets import (QLabel, QLineEdit, QSpinBox, QComboBox,
                             QWidget, QGroupBox, QPushButton,
                             QHBoxLayout, QVBoxLayout, QAbstractItemView, QTreeView)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QFileInfo, QCoreApplication

import sys, uuid, copy

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    # this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-4]))

from bridgehouse.editMap.inbound import logbook

    
class OutboundVmessSettingPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.outboundVmessJSONFile = {
                                        "vnext": [
                                            {
                                                "address": "127.0.0.1",
                                                "port": 443,
                                                "users": [
                                                    {
                                                        "id": "27848739-7e62-4138-9fd3-098a63964b6b",
                                                        "alterId": 10,
                                                        "security": "aes-128-cfb",
                                                        "level": 0
                                                    }
                                                ]
                                             }
                                        ]
                                      }
        self.translate = QCoreApplication.translate
        self.labeloutVmess = (self.translate("OutboundVmessSettingPanel", "Address/AlterID"),
                              self.translate("OutboundVmessSettingPanel", "Port/Method"),
                              self.translate("OutboundVmessSettingPanel", "UUID"),
                              self.translate("OutboundVmessSettingPanel", "Level"))
        
        self.listMethodoutVmess = "auto", "aes-128-cfb", "aes-128-gcm", "chacha20-poly1305", "none"

    def createOutboundVmessPanel(self):
        labelAddress = QLabel(
            self.translate("OutboundVmessSettingPanel", "Server Address: "), self)
        self.lineEditOutboundVmessAddress = QLineEdit()
        labelPort = QLabel(
            self.translate("OutboundVmessSettingPanel", "Port: "), self)
        self.spinBoxOutboundVmessPort = QSpinBox()
        self.spinBoxOutboundVmessPort.setRange(0, 65535)
        self.spinBoxOutboundVmessPort.setValue(443)
        
        labelUIID = QLabel(
            self.translate("OutboundVmessSettingPanel", "UUID: "), self)
        self.lineEditOutboundVmessUUID = QLineEdit()
        self.btnoutVmessGerateUUID = QPushButton(
            self.translate("OutboundVmessSettingPanel", "Gerate UUID"), self)
        labelAlterID = QLabel(
            self.translate("OutboundVmessSettingPanel", "AlterID: "), self)
        self.spinBoxOutboundVmessAlterID = QSpinBox()
        self.comboBoxOutboundVmessMethod = QComboBox()
        self.spinBoxOutboundVmessAlterID.setRange(0, 65535)
        self.lineEditOutboundVmessUUID.setInputMask("HHHHHHHH-HHHH-HHHH-HHHH-HHHHHHHHHHHH;_")
        self.comboBoxOutboundVmessMethod.addItems(self.listMethodoutVmess)
        
        labelLevel = QLabel(
            self.translate("OutboundVmessSettingPanel", "User Level: "))
        self.spinBoxOutboundVmessuserLevel = QSpinBox()
        self.spinBoxOutboundVmessuserLevel.setRange(0, 65535)
        self.spinBoxOutboundVmessuserLevel.setValue(0)
        
        hboxuserLevel = QHBoxLayout()
        hboxuserLevel.addWidget(labelLevel)
        hboxuserLevel.addWidget(self.spinBoxOutboundVmessuserLevel)
        
        hboxAddress = QHBoxLayout()
        hboxAddress.addWidget(labelAddress)
        hboxAddress.addWidget(self.lineEditOutboundVmessAddress)
        hboxAddress.addWidget(labelPort)
        hboxAddress.addWidget(self.spinBoxOutboundVmessPort)
        hboxAddress.addStretch()
        
        self.groupBoxOutBoundVmessAddress = QGroupBox("", self)
        self.groupBoxOutBoundVmessAddress.setLayout(hboxAddress)
        
        hboxID = QHBoxLayout()
        hboxID.addWidget(labelUIID)
        hboxID.addWidget(self.lineEditOutboundVmessUUID)
        hboxID.addWidget(self.btnoutVmessGerateUUID)
        
        hboxAlterID = QHBoxLayout()
        hboxAlterID.addLayout(hboxuserLevel)
        hboxAlterID.addWidget(labelAlterID)
        hboxAlterID.addWidget(self.spinBoxOutboundVmessAlterID)
        hboxAlterID.addWidget(self.comboBoxOutboundVmessMethod)
        hboxAlterID.addStretch()
        
        self.treeViewOutboundVmessAddress = treeViewOutboundVmessAddress = QTreeView()
        treeViewOutboundVmessAddress.setSelectionMode(QAbstractItemView.SingleSelection)
        treeViewOutboundVmessAddress.setSelectionBehavior(QAbstractItemView.SelectRows)
        treeViewOutboundVmessAddress.setUniformRowHeights(True)
        treeViewOutboundVmessAddress.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.treeViewOutboundVmessAddressMode = QStandardItemModel()
        self.treeViewOutboundVmessAddressMode.setHorizontalHeaderLabels(self.labeloutVmess)
        treeViewOutboundVmessAddress.setModel(self.treeViewOutboundVmessAddressMode)
        
        self.btnoutVmessClear = QPushButton(
            self.translate("OutboundVmessSettingPanel", "Clear"))
        self.btnoutVmessChange = QPushButton(
            self.translate("OutboundVmessSettingPanel", "Modify"))
        self.btnoutVmessAdd = QPushButton(
            self.translate("OutboundVmessSettingPanel", "Add"))
        self.btnoutVmessDelete = QPushButton(
            self.translate("OutboundVmessSettingPanel", "Delete"))

        vboxBtn = QVBoxLayout()
        vboxBtn.addStretch()
        vboxBtn.addWidget(self.btnoutVmessAdd)
        vboxBtn.addWidget(self.btnoutVmessClear)
        vboxBtn.addWidget(self.btnoutVmessChange)
        vboxBtn.addWidget(self.btnoutVmessDelete)

        vboxID = QVBoxLayout()
        vboxID.addLayout(hboxID)
        vboxID.addLayout(hboxAlterID)
        
        self.groupBoxOutBoundVmessID = QGroupBox("", self)
        self.groupBoxOutBoundVmessID.setLayout(vboxID)
        self.groupBoxOutBoundVmessID.setEnabled(False)
        
        hboxTreeView = QHBoxLayout()
        hboxTreeView.addWidget(treeViewOutboundVmessAddress)
        hboxTreeView.addLayout(vboxBtn)
        
        vboxOutBoundVmessUser = QVBoxLayout()
        vboxOutBoundVmessUser.addWidget(self.groupBoxOutBoundVmessAddress)
        vboxOutBoundVmessUser.addWidget(self.groupBoxOutBoundVmessID)
        vboxOutBoundVmessUser.addLayout(hboxTreeView)
        
        self.groupBoxOutboundVmessUser = QGroupBox("", self)
        self.groupBoxOutboundVmessUser.setLayout(vboxOutBoundVmessUser)
        
        self.createOutboundVmessPanelSignals()

        if(v2rayshellDebug):
            self.__btnDebug = QPushButton("__DebugTest", self)
            self.__btnDebug.clicked.connect(self.__DebugTest)
            vboxOutBoundVmessUser.addWidget(self.__btnDebug)
            self.setLayout(vboxOutBoundVmessUser)
            self.settingOutboundVmessPanelFromJSONFile(self.outboundVmessJSONFile, True)
            return
            
        return self.groupBoxOutboundVmessUser
    
    def createOutboundVmessPanelSignals(self):
        self.btnoutVmessGerateUUID.clicked.connect(self.onbtnoutVmessGerateUUID)
        self.treeViewOutboundVmessAddress.clicked.connect(self.ontreeViewOutboundVmessAddress)
        self.btnoutVmessClear.clicked.connect(self.onbtnoutVmessClear)
        self.btnoutVmessAdd.clicked.connect(self.onbtnoutVmessAdd)
        self.btnoutVmessDelete.clicked.connect(self.onbtnoutVmessDelete)
        self.btnoutVmessChange.clicked.connect(self.onbtnoutVmessChange)
        
    def onbtnoutVmessGerateUUID(self):
        self.lineEditOutboundVmessUUID.setText(self.createUUID())
        
    def onbtnoutVmessClear(self):
        if (self.groupBoxOutBoundVmessAddress.isEnabled()):
            self.outVmessClearAddress()
        if (self.groupBoxOutBoundVmessID.isEnabled()):
            self.outVmessClearID()
            
    def outVmessClearID(self):
        self.lineEditOutboundVmessUUID.clear()
        self.spinBoxOutboundVmessAlterID.setValue(10)
        self.comboBoxOutboundVmessMethod.setCurrentText("aes-128-cfb")
        self.spinBoxOutboundVmessuserLevel.setValue(0)
        
    def outVmessClearAddress(self):
        self.lineEditOutboundVmessAddress.clear()
        self.spinBoxOutboundVmessPort.setValue(443)
    
    def ontreeViewOutboundVmessAddress(self):
        itemSelection = self.treeViewOutboundVmessAddress.selectionModel()
        rowCurrent = itemSelection.selectedIndexes()[0]
        root = rowCurrent.parent().row()
        row = rowCurrent.row()
        
        if (root == -1):
            self.groupBoxOutBoundVmessAddress.setEnabled(True)
            address = self.treeViewOutboundVmessAddressMode.item(row, 0).text() 
            port = self.treeViewOutboundVmessAddressMode.item(row, 1).text()
            self.lineEditOutboundVmessAddress.setText(address)
            self.spinBoxOutboundVmessPort.setValue(int(port))
            self.outVmessClearID()
            if (self.treeViewOutboundVmessAddressMode.item(row).hasChildren()):
                self.groupBoxOutBoundVmessID.setEnabled(False)
            else:
                self.groupBoxOutBoundVmessID.setEnabled(True)
        else:
            self.groupBoxOutBoundVmessID.setEnabled(True)
            self.groupBoxOutBoundVmessAddress.setEnabled(False)
            
            address = self.treeViewOutboundVmessAddressMode.item(root, 0).text()
            port = self.treeViewOutboundVmessAddressMode.item(root, 1).text()
            uuidString = self.treeViewOutboundVmessAddressMode.item(root).child(row, 2).text()
            alterId = self.treeViewOutboundVmessAddressMode.item(root).child(row, 0).text()
            security = self.treeViewOutboundVmessAddressMode.item(root).child(row, 1).text()
            level = self.treeViewOutboundVmessAddressMode.item(root).child(row, 3).text()
            self.lineEditOutboundVmessAddress.setText(address)
            self.spinBoxOutboundVmessPort.setValue(int(port))
            self.lineEditOutboundVmessUUID.setText(uuidString)
            self.spinBoxOutboundVmessAlterID.setValue(int(alterId))
            self.comboBoxOutboundVmessMethod.setCurrentText(security)
            self.spinBoxOutboundVmessuserLevel.setValue(int(level))

    def onbtnoutVmessChange(self):
        if (not self.treeViewOutboundVmessAddressMode.rowCount()): return
        
        itemSelection = self.treeViewOutboundVmessAddress.selectionModel()
        rowCurrent = itemSelection.selectedIndexes()[0]
        root = rowCurrent.parent().row()
        row = rowCurrent.row()
        
        rowCountAddress = self.treeViewOutboundVmessAddressMode.rowCount()
        addresses = []
        for i in range(rowCountAddress):
            # make sure no Duplicate address
            addresses.append(
                self.treeViewOutboundVmessAddressMode.item(i, 0).text() + ":" + self.treeViewOutboundVmessAddressMode.item(i, 1).text())
        address = self.lineEditOutboundVmessAddress.text() + ":" + str(self.spinBoxOutboundVmessPort.value())

        if (root == -1):
            if ((address in addresses) or (self.lineEditOutboundVmessAddress.text() == "")):
                return
            
            users = []
            usersNumber = self.treeViewOutboundVmessAddressMode.item(row).rowCount()
            if (self.treeViewOutboundVmessAddressMode.hasChildren()):  # or use usersNumber > 0  but hasChildren() more clearer
                for i in range(usersNumber):
                    alterID = self.treeViewOutboundVmessAddressMode.item(row).child(i, 0).text()
                    security = self.treeViewOutboundVmessAddressMode.item(row).child(i, 1).text()
                    uuidString = self.treeViewOutboundVmessAddressMode.item(row).child(i, 2).text()
                    level = self.treeViewOutboundVmessAddressMode.item(row).child(i, 3).text()
                    users.append((alterID, security, uuidString, level))
            
            self.treeViewOutboundVmessAddressMode.setItem(
                row, 0, QStandardItem(str(self.lineEditOutboundVmessAddress.text())))
            self.treeViewOutboundVmessAddressMode.setItem(
                row, 1, QStandardItem(str(self.spinBoxOutboundVmessPort.value())))
            self.treeViewOutboundVmessAddress.setCurrentIndex(
                self.treeViewOutboundVmessAddressMode.index(row, 0))
            
            if (self.treeViewOutboundVmessAddressMode.hasChildren()):
                for i in range(usersNumber):
                    alterID = QStandardItem(str(users[i][0])) 
                    security = QStandardItem(str(users[i][1]))
                    uuidString = QStandardItem(str(users[i][2]))
                    level = QStandardItem(str(users[i][3]))
                    self.treeViewOutboundVmessAddressMode.item(row).appendRow((alterID, security, uuidString, level))
        else:
            if (self.lineEditOutboundVmessUUID.text() == "----"): return
            alterID = QStandardItem(str(self.spinBoxOutboundVmessAlterID.value()))
            security = QStandardItem(str(self.comboBoxOutboundVmessMethod.currentText()))
            uuidString = QStandardItem(str(self.lineEditOutboundVmessUUID.text()))
            level = QStandardItem(str(self.spinBoxOutboundVmessuserLevel.value()))
            self.treeViewOutboundVmessAddressMode.item(root).setChild(row, 0, alterID)
            self.treeViewOutboundVmessAddressMode.item(root).setChild(row, 1, security)
            self.treeViewOutboundVmessAddressMode.item(root).setChild(row, 2, uuidString)
            self.treeViewOutboundVmessAddressMode.item(root).setChild(row, 3, level)
            self.treeViewOutboundVmessAddress.setCurrentIndex(
                self.treeViewOutboundVmessAddressMode.index(row, 0, rowCurrent.parent()))

    def onbtnoutVmessAdd(self):
        if (not self.treeViewOutboundVmessAddressMode.rowCount()):
            if (not self.lineEditOutboundVmessAddress.text()): return
            self.treeViewOutboundVmessAddressMode.appendRow((QStandardItem(str(self.lineEditOutboundVmessAddress.text())),
                                                             QStandardItem(str(self.spinBoxOutboundVmessPort.value()))))
            self.treeViewOutboundVmessAddress.setCurrentIndex(
                self.treeViewOutboundVmessAddressMode.index(0, 0))
            self.btnoutVmessDelete.setEnabled(True)
            self.groupBoxOutBoundVmessID.setEnabled(True)
            self.onbtnoutVmessClear()
            return
        
        itemSelection = self.treeViewOutboundVmessAddress.selectionModel()
        rowCurrent = itemSelection.selectedIndexes()[0]
        root = rowCurrent.parent().row()
        row = rowCurrent.row()
        
        rowCountAddress = self.treeViewOutboundVmessAddressMode.rowCount()
        addresses = []
        for i in range(rowCountAddress):
            # make sure no Duplicate address
            addresses.append(self.treeViewOutboundVmessAddressMode.item(i, 0).text() + ":" + self.treeViewOutboundVmessAddressMode.item(i, 1).text())
        address = self.lineEditOutboundVmessAddress.text() + ":" + str(self.spinBoxOutboundVmessPort.value())
        
        if (root == -1):  # user clicked address
            if (address not in addresses and self.lineEditOutboundVmessAddress.text() != ""):
                self.treeViewOutboundVmessAddressMode.appendRow((QStandardItem(str(self.lineEditOutboundVmessAddress.text())),
                                                             QStandardItem(str(self.spinBoxOutboundVmessPort.value()))))
                self.treeViewOutboundVmessAddress.setCurrentIndex(
                    self.treeViewOutboundVmessAddressMode.index(
                        self.treeViewOutboundVmessAddressMode.rowCount() - 1, 0))
                self.groupBoxOutBoundVmessID.setEnabled(True)
                self.onbtnoutVmessClear()
                     
            if (not self.treeViewOutboundVmessAddressMode.item(row).hasChildren() and
                (self.lineEditOutboundVmessUUID.text() != "----")):
                alterID = QStandardItem(str(self.spinBoxOutboundVmessAlterID.value()))
                security = QStandardItem(str(self.comboBoxOutboundVmessMethod.currentText()))
                uuidString = QStandardItem(str(self.lineEditOutboundVmessUUID.text()))
                level = QStandardItem(str(self.spinBoxOutboundVmessuserLevel.value()))
                self.treeViewOutboundVmessAddressMode.item(row).appendRow((alterID, security, uuidString, level))                                              
                self.onbtnoutVmessClear()
        else:
            if (self.lineEditOutboundVmessUUID.text() == "----"): return  # an empty UUID not allow
            alterID = QStandardItem(str(self.spinBoxOutboundVmessAlterID.value()))
            security = QStandardItem(str(self.comboBoxOutboundVmessMethod.currentText()))
            uuidString = QStandardItem(str(self.lineEditOutboundVmessUUID.text()))
            level = QStandardItem(str(self.spinBoxOutboundVmessuserLevel.value()))
            self.treeViewOutboundVmessAddressMode.item(root).appendRow((alterID, security, uuidString, level))
            
            # the newest item always will be selected
            self.treeViewOutboundVmessAddress.setCurrentIndex(
                self.treeViewOutboundVmessAddressMode.index(
                    self.treeViewOutboundVmessAddressMode.item(root).rowCount() - 1, 0, rowCurrent.parent()))    
            self.onbtnoutVmessClear()
            
    def onbtnoutVmessDelete(self):
        if (not self.treeViewOutboundVmessAddressMode.rowCount()): return
        
        itemSelection = self.treeViewOutboundVmessAddress.selectionModel()
        rowCurrent = itemSelection.selectedIndexes()[0]
        root = rowCurrent.parent().row()
        row = rowCurrent.row()
        
        if (root == -1):
            self.treeViewOutboundVmessAddressMode.removeRow(row)
            if (not self.treeViewOutboundVmessAddressMode.rowCount()):
                self.onbtnoutVmessClear()
                self.groupBoxOutBoundVmessAddress.setEnabled(True)
                self.groupBoxOutBoundVmessID.setDisabled(True)
            self.onbtnoutVmessClear()
        else:
            self.treeViewOutboundVmessAddressMode.item(root).removeRow(row)
            self.onbtnoutVmessClear()
          
    def settingOutboundVmessPanelFromJSONFile(self, outboundVmessJSONFile=None, openFromJSONFile=False):
        logbook.setisOpenJSONFile(openFromJSONFile)
        self.treeViewOutboundVmessAddressMode.setRowCount(0)
        
        if (not outboundVmessJSONFile): outboundVmessJSONFile = {}

        try:
            outboundVmessJSONFile["vnext"]
        except KeyError as e:
            logbook.writeLog("OutboundVmess", "KeyError", e)
            outboundVmessJSONFile["vnext"] = []
            
        addressNumber = len(outboundVmessJSONFile["vnext"])
        
        if (addressNumber):
            addresses = outboundVmessJSONFile["vnext"]
            try:
                self.lineEditOutboundVmessAddress.setText(str(addresses[0]["address"]))
            except KeyError as e:
                logbook.writeLog("OutboundVmess", "KeyError", e)
            except ValueError as e:
                logbook.writeLog("OutboundVmess", "KeyError", e)
                
            try:
                self.spinBoxOutboundVmessPort.setValue(int(addresses[0]["port"]))
            except KeyError as e:
                logbook.writeLog("OutboundVmess", "KeyError", e)
            except (TypeError, ValueError) as e:
                logbook.writeLog("OutboundVmess", "ValueError or TypeError", e)
            
            for i in range(addressNumber):
                try:
                    users = addresses[i]["users"]
                    usersNumber = len(users)
                    serverAddress = QStandardItem(addresses[i]["address"])
                    serverPort = QStandardItem(str(addresses[i]["port"]))
                    if (usersNumber):
                        for j in range(usersNumber):
                            try:
                                uuidString = QStandardItem(str(users[j]["id"]))
                            except Exception: uuidString = QStandardItem("")
                            try:
                                alterId = QStandardItem(str(users[j]["alterId"]))
                            except Exception: alterId = QStandardItem("")
                            try:
                                security = QStandardItem(str(users[j]["security"]))
                            except Exception: security = QStandardItem("")
                            try:
                                level = QStandardItem(str(users[j]["level"]))
                            except Exception: level = QStandardItem("0")
                            try:
                                self.treasureChest.addLevel(users[j]["level"])
                            except Exception:pass
                            serverAddress.appendRow((alterId, security, uuidString, level))                        
                    self.treeViewOutboundVmessAddressMode.appendRow((serverAddress, serverPort))
                except KeyError as e:
                    logbook.writeLog("OutboundVmess", "KeyError", e)
                except:
                    logbook.writeLog("OutboundVmess", "unkonw")
        
        if (self.treeViewOutboundVmessAddressMode.rowCount() > 0):
            self.treeViewOutboundVmessAddress.setCurrentIndex(self.treeViewOutboundVmessAddressMode.index(0, 0))

    def createOutboundVmessJSONFile(self):
        outboundVmessJSONFile = {}
        outboundVmessJSONFile["vnext"] = []
        serversNumber = self.treeViewOutboundVmessAddressMode.rowCount()
        if (not serversNumber): return self.outboundVmessJSONFile
        
        for i in range(serversNumber):
            server = {}
            user = {}
            server["address"] = self.treeViewOutboundVmessAddressMode.item(i, 0).text()
            server["port"] = int(self.treeViewOutboundVmessAddressMode.item(i, 1).text())
            server["users"] = []
            if (self.treeViewOutboundVmessAddressMode.hasChildren()):
                usersNumber = self.treeViewOutboundVmessAddressMode.item(i).rowCount()
                for j in range(usersNumber):
                    user["id"] = self.treeViewOutboundVmessAddressMode.item(i).child(j, 2).text()
                    user["alterId"] = int(self.treeViewOutboundVmessAddressMode.item(i).child(j, 0).text())
                    user["security"] = self.treeViewOutboundVmessAddressMode.item(i).child(j, 1).text()
                    user["level"] = int(self.treeViewOutboundVmessAddressMode.item(i).child(j, 3).text())
                    try:
                        self.treasureChest.addLevel(user["level"])
                    except Exception:
                        pass
                    server["users"].append(copy.deepcopy(user))
            else:
                server["users"] = []
            outboundVmessJSONFile["vnext"].append(copy.deepcopy(server))
        
        return outboundVmessJSONFile

    def clearoutboundVmessPanel(self):
        self.treeViewOutboundVmessAddressMode.setRowCount(0)
        self.lineEditOutboundVmessAddress.clear()
        self.lineEditOutboundVmessUUID.clear()
        self.comboBoxOutboundVmessMethod.setCurrentIndex(0)
        self.spinBoxOutboundVmessAlterID.setValue(10)
        self.spinBoxOutboundVmessPort.setValue(443)
        self.spinBoxOutboundVmessuserLevel.setValue(0)
                     
    def createUUID(self):
        return str(uuid.uuid4())
    
    def validateUUID4(self, uuidString):
        try:
            uuid.UUID(uuidString, version=4)
        except ValueError:
            return False
        return True
        
    def __DebugTest(self):
        import json
        print(json.dumps(self.createOutboundVmessJSONFile(), indent=4, sort_keys=False))

    
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = OutboundVmessSettingPanel()
    ex.createOutboundVmessPanel()
    ex.setGeometry(300, 300, 580, 580)
    ex.show()
    sys.exit(app.exec_())
