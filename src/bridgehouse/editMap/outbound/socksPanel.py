#!/usr/bin/env python3

from PyQt5.QtWidgets import (QLabel, QLineEdit, QSpinBox,
                             QWidget, QGroupBox, QPushButton,
                             QHBoxLayout, QVBoxLayout, QAbstractItemView,
                             QTreeView)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QFileInfo, QCoreApplication

import sys, copy


v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    # this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-4]))

from bridgehouse.editMap.inbound import logbook


class OutboundSocksPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.outboundSocksJSONFile = {
                                        "servers": [{
                                            "address": "127.0.0.1",
                                            "port": 1080,
                                            "users": [{
                                                    "user": "test user",
                                                    "pass": "test pass",
                                                    "level": 0
                                                }]
                                            }]
                                      }
        self.translate = QCoreApplication.translate

        self.labeloutSocks = (self.translate("OutboundSocksPanel", "Address"),
                              self.translate("OutboundSocksPanel", "Port"),
                              self.translate("OutboundSocksPanel", "Level"))
    
    def createOutboundSocksSettingPanel(self):
        self.btnOutboundSocksNewUser= QPushButton(
            self.translate("OutboundSocksPanel", "New User"))
        self.btnOutboundSocksNewServer= QPushButton(
            self.translate("OutboundSocksPanel", "New Server"))
        self.btnOutboundSocksDelete = QPushButton(
            self.translate("OutboundSocksPanel", "Delete"))
        
        vboxBtnUser = QVBoxLayout()
        vboxBtnUser.addWidget(QLabel())
        vboxBtnUser.addWidget(QLabel())
        vboxBtnUser.addWidget(QLabel())
        vboxBtnUser.addWidget(QLabel())
        vboxBtnUser.addWidget(self.btnOutboundSocksNewUser)
        vboxBtnUser.addWidget(self.btnOutboundSocksNewServer)
        vboxBtnUser.addWidget(self.btnOutboundSocksDelete)
        
        self.treeViewoutSocksAddress = treeViewoutSocksAddress = QTreeView() 
        treeViewoutSocksAddress.setSelectionMode(QAbstractItemView.SingleSelection)
        treeViewoutSocksAddress.setSelectionBehavior(QAbstractItemView.SelectRows)
        treeViewoutSocksAddress.setUniformRowHeights(True)
        
        self.treeViewoutSocksAddressMode = QStandardItemModel()
        self.treeViewoutSocksAddressMode.setHorizontalHeaderLabels(self.labeloutSocks)
        self.treeViewoutSocksAddress.setModel(self.treeViewoutSocksAddressMode)

        hboxtreeView = QHBoxLayout()
        hboxtreeView.addWidget(self.treeViewoutSocksAddress)
        hboxtreeView.addLayout(vboxBtnUser)
        
        vboxOutboundSocks = QVBoxLayout()
        vboxOutboundSocks.addLayout(hboxtreeView)

        groupBoxOutboundSocksPanel = QGroupBox(
            self.translate("OutboundSocksPanel", "Socks"), self)
        groupBoxOutboundSocksPanel.setLayout(vboxOutboundSocks)
        
        if (v2rayshellDebug):
            self.__btnDebug = QPushButton("__DebugTest", self)
            vboxOutboundSocks.addWidget(self.__btnDebug)
            self.__btnDebug.clicked.connect(self.__DebugTest)
            self.settingOutboundSocksPanelFromJSONFile(self.outboundSocksJSONFile, True)
        
        self.createOutboundSocksPanelSignals()

        return groupBoxOutboundSocksPanel
    
    def createOutboundSocksPanelSignals(self):
        self.btnOutboundSocksDelete.clicked.connect(self.onbtnOutboundSocksDelete)
        self.btnOutboundSocksNewUser.clicked.connect(self.onbtnOutboundSocksNewUser)
        self.btnOutboundSocksNewServer.clicked.connect(self.onbtnOutboundSocksNewServer)
        
    def onbtnOutboundSocksNewUser(self):
        rowCount = self.treeViewoutSocksAddressMode.rowCount()
        if not rowCount:
            self.newRowOutSocks(rowCount)
            self.treeViewoutSocksAddress.setCurrentIndex(self.treeViewoutSocksAddressMode.index(rowCount, 0))
            return
    
        itemSelection = self.treeViewoutSocksAddress.selectionModel()
        rowCurrent = itemSelection.selectedIndexes()[0]
        root = rowCurrent.parent().row()
        row = rowCurrent.row()
        if root == -1:
            self.treeViewoutSocksAddressMode.item(row).appendRow((
                QStandardItem("user_name"),
                QStandardItem("********"),
                QStandardItem("0")))
            self.treeViewoutSocksAddress.expand(self.treeViewoutSocksAddressMode.index(row, 0))
        else:
            self.treeViewoutSocksAddressMode.item(root).appendRow((
                QStandardItem("user_name"),
                QStandardItem("********"),
                QStandardItem("0")))
        
    def onbtnOutboundSocksNewServer(self):
        row = self.treeViewoutSocksAddressMode.rowCount()
        if not row:
            self.newRowOutSocks(row)
            self.treeViewoutSocksAddress.setCurrentIndex(self.treeViewoutSocksAddressMode.index(row, 0))
        else:
            r = self.treeViewoutSocksAddressMode.item(row-1)
            if r.hasChildren():
                self.newRowOutSocks(row)

    def newRowOutSocks(self, row):
        self.treeViewoutSocksAddressMode.setRowCount(row+1)
        address = self.treeViewoutSocksAddressMode.index(row, 0)
        port = self.treeViewoutSocksAddressMode.index(row, 1)
        self.treeViewoutSocksAddressMode.setData(address, "127.0.0.1")
        self.treeViewoutSocksAddressMode.setData(port, "1080")

    def onbtnOutboundSocksDelete(self):
        if (not self.treeViewoutSocksAddressMode.rowCount()): return
        
        itemSelection = self.treeViewoutSocksAddress.selectionModel()
        rowCurrent = itemSelection.selectedIndexes()[0]
        root = rowCurrent.parent().row()
        row = rowCurrent.row()
        if root == -1:
            self.treeViewoutSocksAddressMode.removeRow(row)
        else:
            self.treeViewoutSocksAddressMode.item(root).removeRow(row)
            
    def settingOutboundSocksPanelFromJSONFile(self, outboundSocksJSONFile={}, openFromJSONFile=True):
        logbook.setisOpenJSONFile(openFromJSONFile)
        self.treeViewoutSocksAddressMode.setRowCount(0)
        
        if (not outboundSocksJSONFile): outboundSocksJSONFile = {}

        try:
            outboundSocksJSONFile["servers"]
        except KeyError as e:
            logbook.writeLog("OutboundSocks", "KeyError", e)
            outboundSocksJSONFile["servers"] = []
        
        servers = outboundSocksJSONFile["servers"]
        serversNumber = len(servers)
        
        # just show the first server detail in TabelWidget
        if (serversNumber):

            for i in range(serversNumber):
                try:
                    usersNumber = len(servers[i]["users"])
                except KeyError as e:
                    logbook.writeLog("OutboundSocks", "KeyError", e)
                    usersNumber = 0
                try:
                    users = servers[i]["users"]
                except KeyError as e:
                    logbook.writeLog("OutboundSocks", "KeyError", e)
                try:
                    serverAddress = QStandardItem(str(servers[i]["address"]))
                except KeyError as e:
                    logbook.writeLog("OutboundSocks", "KeyError", e)
                    
                try:
                    serverPort = QStandardItem(str(servers[i]["port"]))
                except KeyError as e:
                    logbook.writeLog("OutboundSocks", "KeyError", e)
                    
                for j in range(usersNumber):
                    try:
                        user = QStandardItem(str(users[j]["user"]))
                        password = QStandardItem(str(users[j]["pass"]))
                        try:
                            level = QStandardItem(str(users[j]["level"]))
                        except Exception:
                            level = QStandardItem("0")
                        
                        try:    
                            self.treasureChest.addLevel(users[j]["level"])
                        except Exception:
                            pass
                        serverAddress.appendRow((user, password, level))
                    except KeyError as e:
                        logbook.writeLog("OutboundSocks set user", "KeyError", e)
                    except TypeError as e:
                        logbook.writeLog("OutboundSocks set user", "TypeError", e)
                    except ValueError as e:
                        logbook.writeLog("OutboundSocks set user", "ValueError", e)
                    except:
                        logbook.writeLog("OutboundSocks set user", "unkonw")
                self.treeViewoutSocksAddressMode.appendRow((serverAddress, serverPort))
        # make a sure add items success
        if (self.treeViewoutSocksAddressMode.rowCount()):
            # if there no any selectItem, "Add, Modify, Delete" button's slot will crash
            self.treeViewoutSocksAddress.setCurrentIndex(self.treeViewoutSocksAddressMode.index(0, 0))
        
    def createOutboundSocksJSONFile(self):
        outboundSocksJSONFile = {}
        outboundSocksJSONFile["servers"] = []
        serversNumber = self.treeViewoutSocksAddressMode.rowCount()
        if (not serversNumber): return
        print(serversNumber)
        for i in range(serversNumber):
            server = {}
            user = {}
            server["address"] = self.treeViewoutSocksAddressMode.item(i, 0).text()
            server["port"] = int(self.treeViewoutSocksAddressMode.item(i, 1).text())
            server["users"] = []
            if (self.treeViewoutSocksAddressMode.hasChildren()):
                usersNumber = self.treeViewoutSocksAddressMode.item(i).rowCount()
                for j in range(usersNumber):
                    user["user"] = self.treeViewoutSocksAddressMode.item(i).child(j, 0).text()
                    user["pass"] = self.treeViewoutSocksAddressMode.item(i).child(j, 1).text()
                    user["level"] = int(self.treeViewoutSocksAddressMode.item(i).child(j, 2).text())
                    try:
                        self.treasureChest.addLevel(user["level"])
                    except Exception:
                        pass
                    server["users"].append(copy.deepcopy(user))
            else:
                server["users"] = []
            outboundSocksJSONFile["servers"].append(copy.deepcopy(server))

        return outboundSocksJSONFile
    
    def clearSocksPanel(self):
        self.treeViewoutSocksAddressMode.setRowCount(0)
        
    def __DebugTest(self):
        import json
        print(json.dumps(self.createOutboundSocksJSONFile(), indent=4, sort_keys=False))

        
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = OutboundSocksPanel()
    ex.createOutboundSocksSettingPanel()
    ex.setGeometry(300, 300, 800, 350)
    ex.show()
    sys.exit(app.exec_())
