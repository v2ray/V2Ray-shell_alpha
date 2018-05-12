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
from bridgehouse.editMap.toolbox import toolbox
    
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
        self.treeViewOutboundVmessAddress = treeViewOutboundVmessAddress = QTreeView()
        treeViewOutboundVmessAddress.setSelectionMode(QAbstractItemView.SingleSelection)
        treeViewOutboundVmessAddress.setSelectionBehavior(QAbstractItemView.SelectRows)
        treeViewOutboundVmessAddress.setUniformRowHeights(True)
        
        self.treeViewOutboundVmessAddressMode = QStandardItemModel()
        self.treeViewOutboundVmessAddressMode.setHorizontalHeaderLabels(self.labeloutVmess)
        treeViewOutboundVmessAddress.setModel(self.treeViewOutboundVmessAddressMode)
        
        treeViewOutboundVmessAddress.setItemDelegateForColumn(1, toolbox.ComboBoxDelegate(self.listMethodoutVmess))
        
        self.btnoutVmessNewUser = QPushButton(
            self.translate("OutboundVmessSettingPanel", "New User"))
        self.btnoutVmessNewServer= QPushButton(
            self.translate("OutboundVmessSettingPanel", "New Sever"))
        self.btnoutVmessDelete = QPushButton(
            self.translate("OutboundVmessSettingPanel", "Delete"))

        vboxBtn = QVBoxLayout()
        vboxBtn.addWidget(QLabel())
        vboxBtn.addWidget(QLabel())
        vboxBtn.addWidget(QLabel())
        vboxBtn.addWidget(QLabel())
        vboxBtn.addWidget(self.btnoutVmessNewUser)
        vboxBtn.addWidget(self.btnoutVmessNewServer)
        vboxBtn.addWidget(self.btnoutVmessDelete)
        
        hboxTreeView = QHBoxLayout()
        hboxTreeView.addWidget(treeViewOutboundVmessAddress)
        hboxTreeView.addLayout(vboxBtn)
        
        vboxOutBoundVmessUser = QVBoxLayout()
        vboxOutBoundVmessUser.addLayout(hboxTreeView)
        
        groupBoxOutboundVmessUser = QGroupBox("", self)
        groupBoxOutboundVmessUser.setLayout(vboxOutBoundVmessUser)
        
        self.createOutboundVmessPanelSignals()

        if(v2rayshellDebug):
            self.__btnDebug = QPushButton("__DebugTest", self)
            self.__btnDebug.clicked.connect(self.__DebugTest)
            vboxOutBoundVmessUser.addWidget(self.__btnDebug)
            self.setLayout(vboxOutBoundVmessUser)
            self.settingOutboundVmessPanelFromJSONFile(self.outboundVmessJSONFile, True)
            return
            
        return groupBoxOutboundVmessUser
    
    def createOutboundVmessPanelSignals(self):
        self.btnoutVmessDelete.clicked.connect(self.onbtnoutVmessDelete)
        self.btnoutVmessNewServer.clicked.connect(self.onbtnoutVmessNewServer)
        self.btnoutVmessNewUser.clicked.connect(self.onbtnoutVmessNewUser)
            
    def onbtnoutVmessDelete(self):
        if (not self.treeViewOutboundVmessAddressMode.rowCount()): return

        itemSelection = self.treeViewOutboundVmessAddress.selectionModel()
        rowCurrent = itemSelection.selectedIndexes()[0]
        root = rowCurrent.parent().row()
        row = rowCurrent.row()

        if (root == -1):
            self.treeViewOutboundVmessAddressMode.removeRow(row)
        else:
            self.treeViewOutboundVmessAddressMode.item(root).removeRow(row)
    
    def onbtnoutVmessNewUser(self):
        rowCount = self.treeViewOutboundVmessAddressMode.rowCount()
        if not rowCount:
            self.newRowOutVmess(rowCount)
            self.treeViewOutboundVmessAddress.setCurrentIndex(
                self.treeViewOutboundVmessAddressMode.index(rowCount, 0))
            return
    
        itemSelection = self.treeViewOutboundVmessAddress.selectionModel()
        rowCurrent = itemSelection.selectedIndexes()[0]
        root = rowCurrent.parent().row()
        row = rowCurrent.row()
        if root == -1:
            self.treeViewOutboundVmessAddressMode.item(row).appendRow((
                QStandardItem("10"),
                QStandardItem("aes-128-cfb"),
                QStandardItem(self.createUUID()),
                QStandardItem("0")))
            self.treeViewOutboundVmessAddress.expand(self.treeViewOutboundVmessAddressMode.index(row, 0))
        else:
            self.treeViewOutboundVmessAddressMode.item(root).appendRow((
                QStandardItem("10"),
                QStandardItem("aes-128-cfb"),
                QStandardItem(self.createUUID()),
                QStandardItem("0")))
    
    def onbtnoutVmessNewServer(self):
        row = self.treeViewOutboundVmessAddressMode.rowCount()
        if not row:
            self.newRowOutVmess(row)
            self.treeViewOutboundVmessAddress.setCurrentIndex(
                self.treeViewOutboundVmessAddressMode.index(row, 0))
        else:
            r = self.treeViewOutboundVmessAddressMode.item(row-1)
            if r.hasChildren():
                self.newRowOutVmess(row)

    def newRowOutVmess(self, row):
        self.treeViewOutboundVmessAddressMode.setRowCount(row+1)
        address = self.treeViewOutboundVmessAddressMode.index(row, 0)
        port = self.treeViewOutboundVmessAddressMode.index(row, 1)
        self.treeViewOutboundVmessAddressMode.setData(address, "127.0.0.1")
        self.treeViewOutboundVmessAddressMode.setData(port, "443")

    def settingOutboundVmessPanelFromJSONFile(self, outboundVmessJSONFile=None, openFromJSONFile=False):
        logbook.setisOpenJSONFile(openFromJSONFile)
        self.treeViewOutboundVmessAddressMode.setRowCount(0)
        
        if (not outboundVmessJSONFile):
            outboundVmessJSONFile = {}

        try:
            outboundVmessJSONFile["vnext"]
        except KeyError as e:
            logbook.writeLog("OutboundVmess", "KeyError", e)
            outboundVmessJSONFile["vnext"] = []
            
        addressNumber = len(outboundVmessJSONFile["vnext"])
        
        if (addressNumber):
            addresses = outboundVmessJSONFile["vnext"]
            
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
        if (not serversNumber): return
        
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
                     
    def createUUID(self):
        return str(uuid.uuid4())
    
    def validateUUID4(self, uuidString):
        try:
            uuid.UUID(uuidString, version=4)
        except ValueError:
            return False
        return True

    def clearOutVmessPanel(self):
        self.treeViewOutboundVmessAddressMode.setRowCount(0)

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
