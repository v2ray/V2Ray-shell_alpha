#!/usr/bin/env python3

from PyQt5.QtWidgets import (QTableWidget, QLabel, QLineEdit, QSpinBox, QComboBox,
                             QCheckBox, QWidget, QGroupBox, QGridLayout, QPushButton,
                             QHBoxLayout, QVBoxLayout, QAbstractItemView,
                             QTableWidgetItem)
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


class OutboundShadowsocksPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.outboundShadowsocksJSONFile = {
                                            "servers": [
                                                   {
                                                    "email": "love@v2ray.com",
                                                    "address": "127.0.0.1",
                                                    "port": 495,
                                                    "method": "aes-256-cfb",
                                                    "password": "password",
                                                    "ota": True,
                                                    "level": 0
                                                }
                                            ]
                                        }
        self.translate = QCoreApplication.translate
        self.listMethodShadowsocksPanel = "aes-256-cfb", "aes-128-cfb", "chacha20", "chacha20-ietf", "aes-256-gcm", "aes-128-gcm", "chacha20-poly1305"
        self.labelHeaderShadowsocksPanel = (self.translate("OutboundShadowsocksPanel", "Adress"),
                            self.translate("OutboundShadowsocksPanel", "Port"),
                            self.translate("OutboundShadowsocksPanel", "Method"),
                            self.translate("OutboundShadowsocksPanel", "Password"),
                            self.translate("OutboundShadowsocksPanel", "Email"),
                            self.translate("OutboundShadowsocksPanel", "User Level"),
                            self.translate("OutboundShadowsocksPanel", "OTA"))

    def createShadowsocksTableWidget(self):
        self.tableWidgetOutShadowsocks = tableWidget = QTableWidget(self)
        tableWidget.setRowCount(0)
        tableWidget.setColumnCount(7)
        tableWidget.setHorizontalHeaderLabels(self.labelHeaderShadowsocksPanel)
        tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tableWidget.horizontalHeader().setStretchLastSection(True)
        
        self.btnOutShadowsocksClear = QPushButton(
            self.translate("OutboundShadowsocksPanel", "Clear"), self)
        self.btnOutShadowsocksChange = QPushButton(
            self.translate("OutboundShadowsocksPanel", "Modify"), self)
        self.btnOutShadowsocksAddUser = QPushButton(
            self.translate("OutboundShadowsocksPanel", "Add"), self)
        self.btnOutShadowsocksDelete = QPushButton(
            self.translate("OutboundShadowsocksPanel", "Delete"), self)

        vboxBtn = QVBoxLayout()
        vboxBtn.addStretch()
        vboxBtn.addWidget(self.btnOutShadowsocksAddUser)
        vboxBtn.addWidget(self.btnOutShadowsocksClear)
        vboxBtn.addWidget(self.btnOutShadowsocksChange)
        vboxBtn.addWidget(self.btnOutShadowsocksDelete)
        
        hboxTableWidgetUser = QHBoxLayout()
        hboxTableWidgetUser.addWidget(tableWidget)
        hboxTableWidgetUser.addLayout(vboxBtn)
        
        return hboxTableWidgetUser
        
    def createShadowsocksSettingPanel(self):
        labelEmail = QLabel(
            self.translate("OutboundShadowsocksPanel", "Email: "), self)
        self.lineEditOutShadowsocksEmail = QLineEdit()
        labelAddress = QLabel(
            self.translate("OutboundShadowsocksPanel", "Server Address: "), self)
        self.lineEditOutShadowsocksAddress = QLineEdit()        
        labelPort = QLabel(
            self.translate("OutboundShadowsocksPanel", "Port: "), self)
        self.spinBoxOutShadowsocksPort = QSpinBox()
        labelMethod = QLabel(
            self.translate("OutboundShadowsocksPanel", "Method: "), self)
        labelPassword = QLabel(
            self.translate("OutboundShadowsocksPanel", "Password: "), self)
        self.lineEditOutShadowsocksPassword = QLineEdit()
        self.comboBoxOutShadowsocksMethod = QComboBox()
        self.checkBoxOutShadowsocksOTA = QCheckBox(
            self.translate("OutboundShadowsocksPanel", "One Time Auth (OTA)"), self)
        
        labeluserLevel = QLabel(
            self.translate("OutboundShadowsocksPanel", "User Level: "))
        self.spinBoxOutShadowsocksuserLevel = QSpinBox()
        self.spinBoxOutShadowsocksuserLevel.setRange(0, 65535)
        self.spinBoxOutShadowsocksuserLevel.setValue(0)
        
        hboxspinboxuserLevel = QHBoxLayout()
        hboxspinboxuserLevel.addWidget(self.spinBoxOutShadowsocksuserLevel)
        hboxspinboxuserLevel.addStretch()
        
        self.spinBoxOutShadowsocksPort.setRange(0, 65535)
        self.spinBoxOutShadowsocksPort.setValue(495)
        self.comboBoxOutShadowsocksMethod.addItems(self.listMethodShadowsocksPanel)
        
        gridLayout = QGridLayout()
        gridLayout.addWidget(labelEmail, 0, 0)
        gridLayout.addWidget(self.lineEditOutShadowsocksEmail, 0, 1)
        gridLayout.addWidget(labelAddress, 1, 0)
        gridLayout.addWidget(self.lineEditOutShadowsocksAddress, 1, 1)
        gridLayout.addWidget(labelPort, 1, 2)
        gridLayout.addWidget(self.spinBoxOutShadowsocksPort, 1, 3)
        gridLayout.addWidget(labelMethod, 2, 0)
        gridLayout.addWidget(self.comboBoxOutShadowsocksMethod, 2, 1)
        gridLayout.addWidget(labelPassword, 3, 0)
        gridLayout.addWidget(self.lineEditOutShadowsocksPassword, 3, 1)
        gridLayout.addWidget(labeluserLevel, 4, 0)
        gridLayout.addLayout(hboxspinboxuserLevel, 4, 1)
        gridLayout.addWidget(self.checkBoxOutShadowsocksOTA, 5, 0)
        
        vboxShadowsocksSettingPanel = QVBoxLayout()
        vboxShadowsocksSettingPanel.addLayout(gridLayout)
        vboxShadowsocksSettingPanel.addLayout(self.createShadowsocksTableWidget()) 
        
        groupBoxShadowsocksSetting = QGroupBox(
            self.translate("OutboundShadowsocksPanel", "Shadowsocks"), self)
        groupBoxShadowsocksSetting.setLayout(vboxShadowsocksSettingPanel)

        if (v2rayshellDebug):
            self.__btnDebug = QPushButton("__DebugTest", self)
            vboxShadowsocksSettingPanel.addWidget(self.__btnDebug)
            self.__btnDebug.clicked.connect(self.__DebugTest)
            self.settingOutboundShadowsocksPanelFromJSONFile(self.outboundShadowsocksJSONFile, True)

        self.createOutShadowsocksSignales()

        return groupBoxShadowsocksSetting

    def createOutShadowsocksSignales(self):
        self.tableWidgetOutShadowsocks.itemSelectionChanged.connect(self.ontablewWidgetOutShadowsocksItemChanged)
        self.tableWidgetOutShadowsocks.clicked.connect(self.ontablewWidgetOutShadowsocksItemChanged)
        self.btnOutShadowsocksClear.clicked.connect(self.onbtnOutShadowsocksClear)
        self.btnOutShadowsocksAddUser.clicked.connect(self.onbtnOutShadowsocksAddUser)
        self.btnOutShadowsocksChange.clicked.connect(self.onbtnOutShadowsocksChange)
        self.btnOutShadowsocksDelete.clicked.connect(self.onbtnOutShadowsocksDelete)
        
    def onbtnOutShadowsocksClear(self):
        self.lineEditOutShadowsocksAddress.clear()
        self.lineEditOutShadowsocksEmail.clear()
        self.lineEditOutShadowsocksPassword.clear()
        self.spinBoxOutShadowsocksPort.setValue(495)
        self.checkBoxOutShadowsocksOTA.setChecked(False)
        
    def onbtnOutShadowsocksAddUser(self):
        if (not self.lineEditOutShadowsocksAddress.text() or 
            not self.lineEditOutShadowsocksEmail.text() or
            not self.lineEditOutShadowsocksPassword.text()): return
            
        row = self.tableWidgetOutShadowsocks.rowCount()
        self.tableWidgetOutShadowsocks.setRowCount(row + 1)
        check = QCheckBox(self)
        check.setChecked(self.checkBoxOutShadowsocksOTA.isChecked())
        
        self.tableWidgetOutShadowsocks.setItem(
            row, 0, QTableWidgetItem(self.lineEditOutShadowsocksAddress.text()))
        self.tableWidgetOutShadowsocks.setItem(
            row, 1, QTableWidgetItem(self.spinBoxOutShadowsocksPort.text()))
        self.tableWidgetOutShadowsocks.setItem(
            row, 2, QTableWidgetItem(self.comboBoxOutShadowsocksMethod.currentText()))
        self.tableWidgetOutShadowsocks.setItem(
            row, 3, QTableWidgetItem(self.lineEditOutShadowsocksPassword.text()))
        self.tableWidgetOutShadowsocks.setItem(
            row, 4, QTableWidgetItem(self.lineEditOutShadowsocksEmail.text()))
        self.tableWidgetOutShadowsocks.setItem(
            row, 5, QTableWidgetItem(str(self.spinBoxOutShadowsocksuserLevel.value())))
        self.tableWidgetOutShadowsocks.setCellWidget(row, 6, check)
        self.tableWidgetOutShadowsocks.resizeColumnsToContents()
        
        self.onbtnOutShadowsocksClear()
    
    def onbtnOutShadowsocksChange(self):
        row = self.tableWidgetOutShadowsocks.currentRow()
        if (not row or not self.tableWidgetOutShadowsocks.selectedItems()): return
        
        check = QCheckBox(self)
        check.setChecked(self.checkBoxOutShadowsocksOTA.isChecked())
        
        self.tableWidgetOutShadowsocks.setItem(
            row, 0, QTableWidgetItem(self.lineEditOutShadowsocksAddress.text()))
        self.tableWidgetOutShadowsocks.setItem(
            row, 1, QTableWidgetItem(self.spinBoxOutShadowsocksPort.text()))
        self.tableWidgetOutShadowsocks.setItem(
            row, 2, QTableWidgetItem(self.comboBoxOutShadowsocksMethod.currentText()))
        self.tableWidgetOutShadowsocks.setItem(
            row, 3, QTableWidgetItem(self.lineEditOutShadowsocksPassword.text()))
        self.tableWidgetOutShadowsocks.setItem(
            row, 4, QTableWidgetItem(self.lineEditOutShadowsocksEmail.text()))
        self.tableWidgetOutShadowsocks.setItem(
            row, 5, QTableWidgetItem(str(self.spinBoxOutShadowsocksuserLevel.value())))
        self.tableWidgetOutShadowsocks.setCellWidget(row, 6, check)
        self.tableWidgetOutShadowsocks.resizeColumnsToContents()
    
    def onbtnOutShadowsocksDelete(self):
        self.onbtnOutShadowsocksClear()
        self.tableWidgetOutShadowsocks.removeRow(self.tableWidgetOutShadowsocks.currentRow())
        
    def ontablewWidgetOutShadowsocksItemChanged(self):
        if (not self.tableWidgetOutShadowsocks.selectedItems()): return
        row = self.tableWidgetOutShadowsocks.currentRow()
        address = self.tableWidgetOutShadowsocks.item(row, 0)
        port = self.tableWidgetOutShadowsocks.item(row, 1)
        method = self.tableWidgetOutShadowsocks.item(row, 2)
        password = self.tableWidgetOutShadowsocks.item(row, 3)
        email = self.tableWidgetOutShadowsocks.item(row, 4)
        level = self.tableWidgetOutShadowsocks.item(row, 5)
        ota = self.tableWidgetOutShadowsocks.cellWidget(row, 6)
        
        if (address):
            self.lineEditOutShadowsocksAddress.setText(address.text())
        else:
            self.lineEditOutShadowsocksAddress.clear()
        
        if (port):
            self.spinBoxOutShadowsocksPort.setValue(int(port.text()))
        else:
            self.spinBoxOutShadowsocksPort.setValue(8338)
        
        if (method):
            self.comboBoxOutShadowsocksMethod.setCurrentText(method.text())
        else:
            pass
        
        if (password):
            self.lineEditOutShadowsocksPassword.setText(password.text())
        else:
            self.lineEditOutShadowsocksPassword.clear()
        
        if (email):
            self.lineEditOutShadowsocksEmail.setText(email.text())
        else:
            self.lineEditOutShadowsocksEmail.clear()
            
        if (level):
            self.spinBoxOutShadowsocksuserLevel.setValue(int(level.text()))
        else:
            self.spinBoxOutShadowsocksuserLevel.clear()

        if (ota):
            self.checkBoxOutShadowsocksOTA.setChecked(ota.isChecked())
        else:
            self.checkBoxOutShadowsocksOTA.setChecked(False)
    
    def settingOutboundShadowsocksPanelFromJSONFile(self, outboundShadowsocksJSONFile={}, openFromJSONFile=False):
        logbook.setisOpenJSONFile(openFromJSONFile)
        self.tableWidgetOutShadowsocks.setRowCount(0)
        
        if (not outboundShadowsocksJSONFile): outboundShadowsocksJSONFile = {}

        try:
            outboundShadowsocksJSONFile["servers"]
        except KeyError as e:
            logbook.writeLog("OutboundShadowsocks", "KeyError", e)
            outboundShadowsocksJSONFile["servers"] = []

        serverNumber = len(outboundShadowsocksJSONFile["servers"])
        servers = outboundShadowsocksJSONFile["servers"]
        
        if (serverNumber):
            self.tableWidgetOutShadowsocks.setRowCount(serverNumber)
            try:
                for i in range(serverNumber):
                    self.tableWidgetOutShadowsocks.setItem(
                        i, 0, QTableWidgetItem(str(servers[i]["address"])))
                    self.tableWidgetOutShadowsocks.setItem(
                        i, 1, QTableWidgetItem(str(servers[i]["port"])))
                    self.tableWidgetOutShadowsocks.setItem(
                        i, 2, QTableWidgetItem(str(servers[i]["method"])))
                    self.tableWidgetOutShadowsocks.setItem(
                        i, 3, QTableWidgetItem(str(servers[i]["password"])))
                    self.tableWidgetOutShadowsocks.setItem(
                        i, 4, QTableWidgetItem(str(servers[i]["email"])))
                    try:
                        self.tableWidgetOutShadowsocks.setItem(
                            i, 5, QTableWidgetItem(str(servers[i]["level"])))
                    except Exception:
                        self.tableWidgetOutShadowsocks.setItem(
                            i, 5, QTableWidgetItem("0"))
                        
                    try:self.treasureChest.addLevel(servers[i]["level"])
                    except Exception:pass
                    try:self.treasureChest.addEmail(servers[i]["email"])
                    except Exception:pass

                    checkota = QCheckBox()
                    checkota.setChecked(bool(servers[i]["ota"]))
                    self.tableWidgetOutShadowsocks.setCellWidget(i, 6, checkota)
                    self.tableWidgetOutShadowsocks.resizeColumnsToContents()

            except KeyError as e:logbook.writeLog("OutboundShadowsocks", "KeyError", e)
            except:logbook.writeLog("OutboundShadowsocks set servers", "unkown", e)
    
    def createOutboundShadowsocksJSONFile(self):
        serversNumber = self.tableWidgetOutShadowsocks.rowCount()
        outboundShadowsocksJSONFile = {}
        outboundShadowsocksJSONFile["servers"] = []  # clean default setting
        for i in range(serversNumber):
            servers = {}
            server = self.tableWidgetOutShadowsocks.item(i, 0)
            port = self.tableWidgetOutShadowsocks.item(i, 1)
            method = self.tableWidgetOutShadowsocks.item(i, 2)
            password = self.tableWidgetOutShadowsocks.item(i, 3)
            email = self.tableWidgetOutShadowsocks.item(i, 4)       
            level = self.tableWidgetOutShadowsocks.item(i, 5)
            ota = self.tableWidgetOutShadowsocks.cellWidget(i, 6)
            
            if (server and port and method and password and email and ota and level):
                servers["email"] = email.text()
                servers["address"] = server.text()
                servers["port"] = int(port.text())
                servers["method"] = method.text()
                servers["password"] = password.text()
                try:servers["level"] = int(level.text())
                except Exception: servers["level"] = 0

                if (ota.isChecked()): servers["ota"] = True
                else:servers["ota"] = False

                try:self.treasureChest.addLevel(level.text())
                except Exception:pass
                try:self.treasureChest.addEmail(email.text())
                except Exception:pass

            outboundShadowsocksJSONFile["servers"].append(copy.deepcopy(servers))

        return outboundShadowsocksJSONFile
    
    def clearoutboundShadowsocksPanel(self):
        self.tableWidgetOutShadowsocks.setRowCount(0)
        self.checkBoxOutShadowsocksOTA.setChecked(False)
        self.lineEditOutShadowsocksAddress.clear()
        self.lineEditOutShadowsocksEmail.clear()
        self.lineEditOutShadowsocksPassword.clear()
        self.comboBoxOutShadowsocksMethod.setCurrentIndex(0)
        self.spinBoxOutShadowsocksPort.setValue(495)
        self.spinBoxOutShadowsocksuserLevel.setValue(0)
       
    def __DebugTest(self):
        import json
        print(json.dumps(self.createOutboundShadowsocksJSONFile(), indent=4, sort_keys=False))


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = OutboundShadowsocksPanel()
    ex.createShadowsocksSettingPanel()
    ex.setGeometry(300, 300, 680, 500)
    ex.show()
    sys.exit(app.exec_())
