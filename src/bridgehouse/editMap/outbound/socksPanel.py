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
        labelAddress = QLabel(
            self.translate("OutboundSocksPanel", "Server Address: "), self)
        self.lineEditOutboundSocksAddress = QLineEdit()
        labelPort = QLabel(
            self.translate("OutboundSocksPanel", "Port: "), self)
        self.spinBoxOutboundSocksPort = QSpinBox()
    
        labelUserName = QLabel(
            self.translate("OutboundSocksPanel", "User: "), self)
        self.lineEditOutboundSocksUserName = QLineEdit()
        labelPassowrd = QLabel(
            self.translate("OutboundSocksPanel", "Password: "), self)
        self.lineEditOutboundSocksPassword = QLineEdit()
        self.lineEditOutboundSocksUserName.setDisabled(True)
        self.lineEditOutboundSocksPassword.setDisabled(True)
        
        labelLevel = QLabel(
            self.translate("OutboundSocksPanel", "User Level: "))
        self.spinBoxOutboundSocksuerLevel = QSpinBox()
        self.spinBoxOutboundSocksuerLevel.setRange(0, 65535)
        self.spinBoxOutboundSocksuerLevel.setValue(0)
        self.spinBoxOutboundSocksuerLevel.setDisabled(True)
        
        hboxuserLevel = QHBoxLayout()
        hboxuserLevel.addWidget(labelLevel)
        hboxuserLevel.addWidget(self.spinBoxOutboundSocksuerLevel)
        hboxuserLevel.addStretch()
        
        self.btnOutboundSocksClear = QPushButton(
            self.translate("OutboundSocksPanel", "Clear"))
        self.btnOutboundSocksChange = QPushButton(
            self.translate("OutboundSocksPanel", "Modify"))
        self.btnOutboundSocksAdd = QPushButton(
            self.translate("OutboundSocksPanel", "Add"))
        self.btnOutboundSocksDelete = QPushButton(
            self.translate("OutboundSocksPanel", "Delete"))
        
        self.spinBoxOutboundSocksPort.setRange(0, 65535)
        self.spinBoxOutboundSocksPort.setValue(1080)
        
        hboxAdress = QHBoxLayout()
        hboxAdress.addWidget(labelAddress)
        hboxAdress.addWidget(self.lineEditOutboundSocksAddress)
        hboxAdress.addWidget(labelPort)
        hboxAdress.addWidget(self.spinBoxOutboundSocksPort)
        hboxAdress.addStretch()
        
        hboxUser = QHBoxLayout()
        hboxUser.addWidget(labelUserName)
        hboxUser.addWidget(self.lineEditOutboundSocksUserName)
        hboxUser.addWidget(labelPassowrd)
        hboxUser.addWidget(self.lineEditOutboundSocksPassword)
        hboxUser.addStretch()
        
        vboxBtnUser = QVBoxLayout()
        vboxBtnUser.addStretch()
        vboxBtnUser.addWidget(self.btnOutboundSocksAdd)
        vboxBtnUser.addWidget(self.btnOutboundSocksClear)
        vboxBtnUser.addWidget(self.btnOutboundSocksChange)
        vboxBtnUser.addWidget(self.btnOutboundSocksDelete)
        
        self.treeViewoutSocksAddress = treeViewoutSocksAddress = QTreeView() 
        treeViewoutSocksAddress.setSelectionMode(QAbstractItemView.SingleSelection)
        treeViewoutSocksAddress.setSelectionBehavior(QAbstractItemView.SelectRows)
        treeViewoutSocksAddress.setUniformRowHeights(True)
        treeViewoutSocksAddress.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.treeViewoutSocksAddressMode = QStandardItemModel()
        self.treeViewoutSocksAddressMode.setHorizontalHeaderLabels(self.labeloutSocks)
        self.treeViewoutSocksAddress.setModel(self.treeViewoutSocksAddressMode)

        hboxtreeView = QHBoxLayout()
        hboxtreeView.addWidget(self.treeViewoutSocksAddress)
        hboxtreeView.addLayout(vboxBtnUser)
        
        vboxOutboundSocks = QVBoxLayout()
        vboxOutboundSocks.addLayout(hboxAdress)
        vboxOutboundSocks.addLayout(hboxUser)
        vboxOutboundSocks.addLayout(hboxuserLevel)
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
        self.btnOutboundSocksAdd.clicked.connect(self.onbtnOutboundSocksAdd)
        self.btnOutboundSocksChange.clicked.connect(self.onbtnOutboundSocksChange)
        self.btnOutboundSocksClear.clicked.connect(self.onbtnOutboundSocksClear)
        self.btnOutboundSocksDelete.clicked.connect(self.onbtnOutboundSocksDelete)
        self.treeViewoutSocksAddress.clicked.connect(self.ontreeViewoutSocksAddressClicked)

    def onbtnOutboundSocksAdd(self):
        if (not self.treeViewoutSocksAddressMode.rowCount()):
            if (not self.lineEditOutboundSocksAddress.text()): return
            self.treeViewoutSocksAddressMode.appendRow((QStandardItem(str(self.lineEditOutboundSocksAddress.text())),
                                                        QStandardItem(str(self.spinBoxOutboundSocksPort.value()))))
            self.treeViewoutSocksAddress.setCurrentIndex(self.treeViewoutSocksAddressMode.index(0, 0))
            self.btnOutboundSocksDelete.setEnabled(True)
            self.lineEditOutboundSocksUserName.setEnabled(True)
            self.lineEditOutboundSocksPassword.setEnabled(True)
            self.spinBoxOutboundSocksuerLevel.setEnabled(True)
            self.onbtnOutboundSocksClear()
            return
        
        itemSelection = self.treeViewoutSocksAddress.selectionModel()
        rowCurrent = itemSelection.selectedIndexes()[0]
        root = rowCurrent.parent().row()
        row = rowCurrent.row()
        
        rowCountAdrress = self.treeViewoutSocksAddressMode.rowCount()
        addresses = []
        for i in range(rowCountAdrress):
            addresses.append(self.treeViewoutSocksAddressMode.item(i, 0).text() + ":" + self.treeViewoutSocksAddressMode.item(i, 1).text())
        address = self.lineEditOutboundSocksAddress.text() + ":" + str(self.spinBoxOutboundSocksPort.value())
        if (root == -1):
            if (address not in addresses and self.lineEditOutboundSocksAddress.text() != ""):
                self.treeViewoutSocksAddressMode.appendRow((QStandardItem(str(self.lineEditOutboundSocksAddress.text())),
                                                            QStandardItem(str(self.spinBoxOutboundSocksPort.value()))))
                self.treeViewoutSocksAddress.setCurrentIndex(
                    self.treeViewoutSocksAddressMode.index(self.treeViewoutSocksAddressMode.rowCount() - 1, 0))
                self.lineEditOutboundSocksUserName.setEnabled(True)
                self.lineEditOutboundSocksPassword.setEnabled(True)
                self.spinBoxOutboundSocksuerLevel.setEnabled(True)
                self.onbtnOutboundSocksClear()
                
            if (not self.treeViewoutSocksAddressMode.item(row).hasChildren() and
                (self.lineEditOutboundSocksUserName.text() or self.lineEditOutboundSocksPassword.text())):
                self.treeViewoutSocksAddressMode.item(row).appendRow((QStandardItem(str(self.lineEditOutboundSocksUserName.text())),
                                                                      QStandardItem(str(self.lineEditOutboundSocksPassword.text())),
                                                                      QStandardItem(str(self.spinBoxOutboundSocksuerLevel.value()))))
                self.lineEditOutboundSocksUserName.setDisabled(True)
                self.lineEditOutboundSocksPassword.setDisabled(True)
                self.spinBoxOutboundSocksuerLevel.setDisabled(True)
                self.onbtnOutboundSocksClear()
        else:
            if (not self.lineEditOutboundSocksUserName.text() or not self.lineEditOutboundSocksPassword.text()):
                return  # an empty name or password will not be added
            self.treeViewoutSocksAddressMode.item(root).appendRow((QStandardItem(str(self.lineEditOutboundSocksUserName.text())),
                                                                   QStandardItem(str(self.lineEditOutboundSocksPassword.text())),
                                                                   QStandardItem(str(self.spinBoxOutboundSocksuerLevel.value()))))
            # the newest item always will be selected
            self.treeViewoutSocksAddress.setCurrentIndex(
                self.treeViewoutSocksAddressMode.index(
                    self.treeViewoutSocksAddressMode.item(root).rowCount() - 1, 0, rowCurrent.parent()))
            self.onbtnOutboundSocksClear()
            
    def onbtnOutboundSocksChange(self):
        if (not self.treeViewoutSocksAddressMode.rowCount()): return
            
        itemSelection = self.treeViewoutSocksAddress.selectionModel()
        rowCurrent = itemSelection.selectedIndexes()[0]
        root = rowCurrent.parent().row()
        row = rowCurrent.row()
        
        rowCountAdrress = self.treeViewoutSocksAddressMode.rowCount()
        addresses = []
        for i in range(rowCountAdrress):
            addresses.append(
                self.treeViewoutSocksAddressMode.item(i, 0).text() + ":" + self.treeViewoutSocksAddressMode.item(i, 1).text())
        address = self.lineEditOutboundSocksAddress.text() + ":" + str(self.spinBoxOutboundSocksPort.value())
                
        if (root == -1):
            if (address in addresses or not self.lineEditOutboundSocksAddress.text()):
                return
            
            users = []  # change address or port will delete child items, now save child items
            userNumber = self.treeViewoutSocksAddressMode.item(row).rowCount()
            if (self.treeViewoutSocksAddressMode.hasChildren()):
                for i in range(userNumber):
                    users.append((self.treeViewoutSocksAddressMode.item(row).child(i, 0).text(),
                                  self.treeViewoutSocksAddressMode.item(row).child(i, 1).text()))
            
            self.treeViewoutSocksAddressMode.setItem(row, 0, QStandardItem(self.lineEditOutboundSocksAddress.text()))
            self.treeViewoutSocksAddressMode.setItem(row, 1, QStandardItem(str(self.spinBoxOutboundSocksPort.value())))
            self.treeViewoutSocksAddress.setCurrentIndex(self.treeViewoutSocksAddressMode.index(row, 0))
            
            # restore child items
            if (self.treeViewoutSocksAddressMode.hasChildren()):
                for i in range(userNumber):
                    self.treeViewoutSocksAddressMode.item(row).appendRow((QStandardItem(users[i][0]),
                                                                          QStandardItem(users[i][1]),
                                                                          QStandardItem(users[i][2])))
        
        else:
            if (not self.lineEditOutboundSocksUserName.text() or not self.lineEditOutboundSocksPassword.text()):
                return
            self.treeViewoutSocksAddressMode.item(root).setChild(row, 0, QStandardItem(self.lineEditOutboundSocksUserName.text()))
            self.treeViewoutSocksAddressMode.item(root).setChild(row, 1, QStandardItem(self.lineEditOutboundSocksPassword.text()))
            self.treeViewoutSocksAddressMode.item(root).setChild(row, 2, QStandardItem(str(self.spinBoxOutboundSocksuerLevel.value())))
            self.treeViewoutSocksAddress.setCurrentIndex(self.treeViewoutSocksAddressMode.index(row, 0, rowCurrent.parent()))
            
    def onbtnOutboundSocksClear(self):
        if (self.lineEditOutboundSocksAddress.isEnabled()):
            self.lineEditOutboundSocksAddress.clear()
            self.spinBoxOutboundSocksPort.setValue(1080)
        if (self.lineEditOutboundSocksUserName.isEnabled()):
            self.lineEditOutboundSocksPassword.clear()
            self.lineEditOutboundSocksUserName.clear()
            self.spinBoxOutboundSocksuerLevel.setValue(0)
            
    def onbtnOutboundSocksDelete(self):
        if (not self.treeViewoutSocksAddressMode.rowCount()): return
        
        itemSelection = self.treeViewoutSocksAddress.selectionModel()
        rowCurrent = itemSelection.selectedIndexes()[0]
        root = rowCurrent.parent().row()
        row = rowCurrent.row()

        if (root == -1):
            self.treeViewoutSocksAddressMode.removeRow(row)
            if (not self.treeViewoutSocksAddressMode.rowCount()):
                self.lineEditOutboundSocksAddress.setEnabled(True)
                self.spinBoxOutboundSocksPort.setEnabled(True)
                self.lineEditOutboundSocksUserName.setDisabled(True)
                self.lineEditOutboundSocksPassword.setDisabled(True)
            self.onbtnOutboundSocksClear()
        else:
            self.treeViewoutSocksAddressMode.item(root).removeRow(row)
            self.onbtnOutboundSocksClear()
    
    def ontreeViewoutSocksAddressClicked(self):
        itemSelection = self.treeViewoutSocksAddress.selectionModel()
        rowCurrent = itemSelection.selectedIndexes()[0]
        root = rowCurrent.parent().row()
        row = rowCurrent.row()
        if (root == -1):
            address = self.treeViewoutSocksAddressMode.item(row, 0).text() 
            port = self.treeViewoutSocksAddressMode.item(row, 1).text()
            self.lineEditOutboundSocksAddress.setText(address)
            self.spinBoxOutboundSocksPort.setValue(int(port))
            self.lineEditOutboundSocksPassword.clear()
            self.lineEditOutboundSocksUserName.clear()
            self.lineEditOutboundSocksAddress.setEnabled(True)
            self.spinBoxOutboundSocksPort.setEnabled(True)
            if (self.treeViewoutSocksAddressMode.item(row).hasChildren()):
                self.lineEditOutboundSocksUserName.setEnabled(False)
                self.lineEditOutboundSocksPassword.setEnabled(False)
                self.spinBoxOutboundSocksuerLevel.setEnabled(False)
            else:
                self.lineEditOutboundSocksUserName.setEnabled(True)
                self.lineEditOutboundSocksPassword.setEnabled(True)
                self.spinBoxOutboundSocksuerLevel.setEnabled(True)
        else:
            address = self.treeViewoutSocksAddressMode.item(root, 0).text()
            port = self.treeViewoutSocksAddressMode.item(root, 1).text()
            user = self.treeViewoutSocksAddressMode.item(root).child(row, 0).text()
            password = self.treeViewoutSocksAddressMode.item(root).child(row, 1).text()
            level = self.treeViewoutSocksAddressMode.item(root).child(row, 2).text()
            self.lineEditOutboundSocksUserName.setText(user)
            self.lineEditOutboundSocksPassword.setText(password)
            self.lineEditOutboundSocksAddress.setText(address)
            self.spinBoxOutboundSocksPort.setValue(int(port))
            self.spinBoxOutboundSocksuerLevel.setValue(int(level))
            self.lineEditOutboundSocksAddress.setEnabled(False)
            self.spinBoxOutboundSocksPort.setEnabled(False)
            self.lineEditOutboundSocksUserName.setEnabled(True)
            self.lineEditOutboundSocksPassword.setEnabled(True)
            self.spinBoxOutboundSocksuerLevel.setEnabled(True)
            
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
            try:
                self.lineEditOutboundSocksAddress.setText(servers[0]["address"])
            except KeyError as e:
                logbook.writeLog("OutboundSocks", "KeyError", e)
                
            try:
                self.spinBoxOutboundSocksPort.setValue(int(servers[0]["port"]))
            except KeyError as e:
                logbook.writeLog("OutboundSocks", "KeyError", e)
            except (ValueError, TypeError) as e:
                logbook.writeLog("OutboundSocks", "ValueError or TypeError", e)

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
        if (not serversNumber): return self.outboundSocksJSONFile
        
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
    
    def clearoutboundSocksPanel(self):
        self.treeViewoutSocksAddressMode.setRowCount(0)
        self.lineEditOutboundSocksAddress.clear()
        self.lineEditOutboundSocksPassword.clear()
        self.lineEditOutboundSocksUserName.clear()
        self.spinBoxOutboundSocksPort.setValue(1080)
        self.spinBoxOutboundSocksuerLevel.setValue(0)
        
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
