#!/usr/bin/env python3

from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QSpinBox,
                             QHBoxLayout, QVBoxLayout, QCheckBox,
                             QTableWidget, QAbstractItemView, QPushButton,
                             QGroupBox, QTableWidgetItem)
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


class InboundSocksPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.inboundSocksJSONFile = {
                                        "auth": "noauth",
                                        "accounts": [
                                                {
                                                "user": "my-username",
                                                "pass": "my-password"
                                                }
                                            ],
                                        "udp": False,
                                        "ip": "127.0.0.1",
                                        "timeout": 300,
                                        "userLevel": 0
                                    }
        self.translate = QCoreApplication.translate
        self.labelUserSocksPanel = (self.translate("InboundSocksPanel", "User"),
                          self.translate("InboundSocksPanel", "Password"))
        
    def createSocksSettingPanel(self):
        labelIP = QLabel(
            self.translate("InboundSocksPanel", "Local IP Address: "), self)
        self.lineEditInboundSocksIP = QLineEdit()
        labelTimeout = QLabel(
            self.translate("InboundSocksPanel", "Timeout: "), self)
        self.spinBoxInboundSocksTimeout = QSpinBox()
        self.checkBoxInboundSocksUDP = QCheckBox(
            self.translate("InboundSocksPanel", "Enable the UDP protocol"), self)
        self.btnInboundSocksUserAdd = QPushButton(
            self.translate("InboundSocksPanel", "Add"), self)
        self.btnInboundSocksChange = QPushButton(
            self.translate("InboundSocksPanel", "Modify"), self)
        self.btnInboundSocksPanelClear = QPushButton(
            self.translate("InboundSocksPanel", "Clear"), self)
        self.btnInboundSocksUserDelete = QPushButton(
            self.translate("InboundSocksPanel", "Delete"), self)
        labelUserName = QLabel(
            self.translate("InboundSocksPanel", "User: "), self)
        self.lineEditInboundSocksUserName = QLineEdit()
        labelPassowrd = QLabel(
            self.translate("InboundSocksPanel", "Password: "), self)
        self.lineEditInboundSocksPassword = QLineEdit()
        self.tableWidgetInboundSocksUser = QTableWidget(self)
        
        self.spinBoxInboundSocksTimeout.setRange(0, 999)
        self.spinBoxInboundSocksTimeout.setValue(300)
        self.lineEditInboundSocksIP.setText("127.0.0.1")
        self.checkBoxInboundSocksUDP.setChecked(False)
        
        labeluserLevel = QLabel(
            self.translate("InboundSocksPanel", "User Level: "))
        self.spinBoxInboundSocksuserLevel = QSpinBox()
        self.spinBoxInboundSocksuserLevel.setRange(0, 65535)
        self.spinBoxInboundSocksuserLevel.setValue(0)
        
        hboxuserLevel = QHBoxLayout()
        hboxuserLevel.addWidget(labeluserLevel)
        hboxuserLevel.addWidget(self.spinBoxInboundSocksuserLevel)
        hboxuserLevel.addStretch()
        
        hboxIP = QHBoxLayout()
        hboxTimeout = QHBoxLayout()
        vboxSocksSetting = QVBoxLayout()
        vboxBtnSocksUser = QVBoxLayout()
        
        hboxIP.addWidget(labelIP)
        hboxIP.addWidget(self.lineEditInboundSocksIP)
        hboxIP.addStretch(1)
        
        hboxTimeout.addWidget(labelTimeout)
        hboxTimeout.addWidget(self.spinBoxInboundSocksTimeout)
        hboxTimeout.addStretch()
        
        hboxUser = QHBoxLayout()
        hboxUser.addWidget(labelUserName)
        hboxUser.addWidget(self.lineEditInboundSocksUserName)
        hboxUser.addWidget(labelPassowrd)
        hboxUser.addWidget(self.lineEditInboundSocksPassword)
        hboxUser.addStretch()
        
        vboxBtnSocksUser.addStretch()
        vboxBtnSocksUser.addWidget(self.btnInboundSocksUserAdd)
        vboxBtnSocksUser.addWidget(self.btnInboundSocksPanelClear)
        vboxBtnSocksUser.addWidget(self.btnInboundSocksChange)
        vboxBtnSocksUser.addWidget(self.btnInboundSocksUserDelete)
        
        vboxSocksSetting.addLayout(hboxIP)
        vboxSocksSetting.addLayout(hboxTimeout)
        vboxSocksSetting.addLayout(hboxuserLevel)
        vboxSocksSetting.addWidget(self.checkBoxInboundSocksUDP)
        
        self.tableWidgetInboundSocksUser.setColumnCount(2)
        self.tableWidgetInboundSocksUser.adjustSize()
        self.tableWidgetInboundSocksUser.setHorizontalHeaderLabels(self.labelUserSocksPanel)
        self.tableWidgetInboundSocksUser.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidgetInboundSocksUser.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidgetInboundSocksUser.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidgetInboundSocksUser.horizontalHeader().setStretchLastSection(True)
        
        self.groupBoxAuth = groupBoxAuth = QGroupBox(
            self.translate("InboundSocksPanel", "Requires Authentication: "), self)
        groupBoxAuth.setCheckable(True)
        groupBoxAuth.setChecked(False)

        hboxInboundSocksAuthTableWidget = QHBoxLayout()
        hboxInboundSocksAuthTableWidget.addWidget(self.tableWidgetInboundSocksUser)
        hboxInboundSocksAuthTableWidget.addLayout(vboxBtnSocksUser)
        
        vboxInboundSocksAuth = QVBoxLayout()
        vboxInboundSocksAuth.addLayout(hboxUser)
        vboxInboundSocksAuth.addLayout(hboxInboundSocksAuthTableWidget)
        
        groupBoxAuth.setLayout(vboxInboundSocksAuth)
        
        vboxInboundSocksPanel = QVBoxLayout()
        vboxInboundSocksPanel.addLayout(vboxSocksSetting)
        vboxInboundSocksPanel.addWidget(groupBoxAuth)
        
        self.createInboundSocksPanelSignals()
        
        if (v2rayshellDebug):
            self.__debugBtn = QPushButton("__debugTest", self)
            vboxInboundSocksPanel.addWidget(self.__debugBtn)
            self.__debugBtn.clicked.connect(self.__debugTest)
            self.settingInboundSocksPanelFromJSONFile(self.inboundSocksJSONFile, True)
            self.setLayout(vboxInboundSocksPanel)
            return
        
        groupSocksPanel = QGroupBox(
            self.translate("InboundSocksPanel", "Socks"), self)
        groupSocksPanel.setLayout(vboxInboundSocksPanel)

        return groupSocksPanel

    def createInboundSocksPanelSignals(self):
        self.tableWidgetInboundSocksUser.itemSelectionChanged.connect(
            self.ontableWidgetInboundSocksUserSelectionChanged)
        self.btnInboundSocksPanelClear.clicked.connect(self.onbtnInboundSocksPanelClear)
        self.btnInboundSocksUserAdd.clicked.connect(self.onbtnInboundSocksUserAdd)
        self.btnInboundSocksUserDelete.clicked.connect(self.onbtnInboundSocksUserDelete)
        self.btnInboundSocksChange.clicked.connect(self.onbtnInboundSocksChange)
        
    def onbtnInboundSocksChange(self):
        row = self.tableWidgetInboundSocksUser.currentRow()
        self.tableWidgetInboundSocksUser.setItem(
            row, 0, QTableWidgetItem(self.lineEditInboundSocksUserName.text()))
        self.tableWidgetInboundSocksUser.setItem(
            row, 1, QTableWidgetItem(self.lineEditInboundSocksPassword.text()))
        
    def onbtnInboundSocksUserDelete(self):
        self.onbtnInboundSocksPanelClear()
        row = self.tableWidgetInboundSocksUser.currentRow()
        self.tableWidgetInboundSocksUser.removeRow(row)
        
    def onbtnInboundSocksUserAdd(self):
        if (not self.lineEditInboundSocksPassword.text() or not self.lineEditInboundSocksUserName.text()): return
        row = self.tableWidgetInboundSocksUser.rowCount()
        self.tableWidgetInboundSocksUser.setRowCount(row + 1)
        self.tableWidgetInboundSocksUser.setItem(
            row, 0, QTableWidgetItem(self.lineEditInboundSocksUserName.text()))
        self.tableWidgetInboundSocksUser.setItem(
            row, 1, QTableWidgetItem(self.lineEditInboundSocksPassword.text()))
        self.tableWidgetInboundSocksUser.resizeColumnsToContents()
        self.onbtnInboundSocksPanelClear()
        
    def onbtnInboundSocksPanelClear(self):
        self.lineEditInboundSocksUserName.clear()
        self.lineEditInboundSocksPassword.clear()
        
    def ontableWidgetInboundSocksUserSelectionChanged(self):
        self.onbtnInboundSocksPanelClear()
        row = self.tableWidgetInboundSocksUser.currentRow()
        user = self.tableWidgetInboundSocksUser.item(row, 0)
        password = self.tableWidgetInboundSocksUser.item(row, 1)
        
        if (user):
            self.lineEditInboundSocksUserName.setText(user.text())
        else:
            self.lineEditInboundSocksUserName.clear()
        if (password):
            self.lineEditInboundSocksPassword.setText(password.text())
        else:
            self.lineEditInboundSocksPassword.clear()

    def settingInboundSocksPanelFromJSONFile(self, inboundSocksJSONFile={}, openFromJSONFile=False):
        logbook.setisOpenJSONFile(openFromJSONFile)
        self.tableWidgetInboundSocksUser.setRowCount(0)
        accountsNumber = 0; accounts = True
        
        if (not inboundSocksJSONFile): inboundSocksJSONFile = {}

        try:
            inboundSocksJSONFile["auth"]
        except KeyError as e:
            logbook.writeLog("InboundSocks", "KeyError", e)
            inboundSocksJSONFile["auth"] = "noauth"
        
        try:
            inboundSocksJSONFile["udp"]
        except KeyError as e:
            logbook.writeLog("InboundSocks", "KeyError", e)
            inboundSocksJSONFile["udp"] = False

        try:
            inboundSocksJSONFile["ip"]
        except KeyError as e:
            logbook.writeLog("InboundSocks", "KeyError", e)
            inboundSocksJSONFile["ip"] = "127.0.0.1"
    
        try:
            inboundSocksJSONFile["timeout"]
        except KeyError as e:
            logbook.writeLog("InboundSocks", "KeyError", e)
            inboundSocksJSONFile["timeout"] = 300
        try:
            inboundSocksJSONFile["accounts"]
        except KeyError as e:
            logbook.writeLog("InboundSocks", "KeyError", e)
            inboundSocksJSONFile["accounts"] = []
            accounts = False
            
        try:
            inboundSocksJSONFile["userLevel"]
        except KeyError as e:
            logbook.writeLog("InboundSocks", "KeyError", e)
            inboundSocksJSONFile["userLevel"] = 0
        
        self.lineEditInboundSocksIP.setText(str(inboundSocksJSONFile["ip"]))
        self.checkBoxInboundSocksUDP.setChecked(bool(inboundSocksJSONFile["udp"]))
        
        try:
            self.spinBoxInboundSocksTimeout.setValue(int(inboundSocksJSONFile["timeout"]))
        except (TypeError, ValueError) as e:
            logbook.writeLog("InboundSocks", "ValueError or TypeError", e)
            self.spinBoxInboundSocksTimeout.setValue(300)
            
        try:
            self.spinBoxInboundSocksuserLevel.setValue(int(inboundSocksJSONFile["userLevel"]))
        except (TypeError, ValueError) as e:
            logbook.writeLog("InboundSocks", "ValueError or TypeError", e)
            self.spinBoxInboundSocksuserLevel.setValue(0)
            
        try:
            self.treasureChest.addLevel(self.spinBoxInboundSocksuserLevel.value())
        except Exception:
            pass

        if (accounts):
            if (inboundSocksJSONFile["auth"] == "password"):
                self.groupBoxAuth.setChecked(True)
            accountsNumber = len(inboundSocksJSONFile["accounts"])
            accounts = inboundSocksJSONFile["accounts"]
            if (accountsNumber):
                self.tableWidgetInboundSocksUser.setRowCount(accountsNumber)
                try:
                    for i in range(0, accountsNumber):
                        self.tableWidgetInboundSocksUser.setItem(i, 0, QTableWidgetItem(str(accounts[i]["user"])))
                        self.tableWidgetInboundSocksUser.setItem(i, 1, QTableWidgetItem(str(accounts[i]["pass"])))
                        self.tableWidgetInboundSocksUser.resizeColumnsToContents()
                except KeyError as e:
                    logbook.writeLog("InboundSocks", "KeyError", e)
        
    def createInboundSocksJSONFile(self):
        inboundSocksJSONFile = {}

        if (self.groupBoxAuth.isChecked()):
            inboundSocksJSONFile["auth"] = "password"
            accountsNumber = self.tableWidgetInboundSocksUser.rowCount()
            if (accountsNumber):
                accounts = []
                for i in range(0, accountsNumber):
                    account = {}
                    user = self.tableWidgetInboundSocksUser.item(i, 0)
                    password = self.tableWidgetInboundSocksUser.item(i, 1)
                    if (user and password):
                        account["user"] = user.text()
                        account["pass"] = password.text()
                        accounts.append(copy.deepcopy(account))
                inboundSocksJSONFile["accounts"] = copy.deepcopy(accounts)
        else:
            inboundSocksJSONFile["auth"] = "noauth"
        
        inboundSocksJSONFile["udp"] = self.checkBoxInboundSocksUDP.isChecked()
        inboundSocksJSONFile["ip"] = self.lineEditInboundSocksIP.text()
        inboundSocksJSONFile["timeout"] = self.spinBoxInboundSocksTimeout.value()
        inboundSocksJSONFile["userLevel"] = self.spinBoxInboundSocksuserLevel.value()
        
        try:
            self.treasureChest.addLevel(self.spinBoxInboundSocksuserLevel.value())
        except Exception:
            pass

        return inboundSocksJSONFile
    
    def clearinboundsocksPanel(self):
        self.tableWidgetInboundSocksUser.setRowCount(0)
        self.lineEditInboundSocksIP.clear()
        self.lineEditInboundSocksPassword.clear()
        self.lineEditInboundSocksUserName.clear()
        self.checkBoxInboundSocksUDP.setChecked(False)
        self.groupBoxAuth.setChecked(False)
        self.spinBoxInboundSocksTimeout.setValue(300)
        self.spinBoxInboundSocksuserLevel.setValue(0)
                    
    def __debugTest(self):
        import json
        print(json.dumps(self.createInboundSocksJSONFile(), indent=4, sort_keys=False))


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = InboundSocksPanel()
    ex.createSocksSettingPanel()
    ex.setGeometry(300, 300, 480, 450)
    ex.show()
    sys.exit(app.exec_())
