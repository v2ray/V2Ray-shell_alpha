#!/usr/bin/env python3

from PyQt5.QtWidgets import (QTableWidget, QLabel, QLineEdit, QSpinBox, QComboBox,
                             QCheckBox, QWidget, QGroupBox, QGridLayout, QPushButton,
                             QHBoxLayout, QVBoxLayout, QAbstractItemView,
                             QTableWidgetItem)
from PyQt5.QtCore import QFileInfo, QCoreApplication
import sys, copy
from PyQt5.Qt import QStandardItem

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
                                                    "method": "chacha20-poly1305",
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

    def createShadowsocksSettingPanel(self):
        self.tableWidgetOutShadowsocks = tableWidget = QTableWidget(self)
        tableWidget.setRowCount(0)
        tableWidget.setColumnCount(7)
        tableWidget.setHorizontalHeaderLabels(self.labelHeaderShadowsocksPanel)
        tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.btnOutShadowsocksNew= QPushButton(
            self.translate("OutboundShadowsocksPanel", "New"), self)
        self.btnOutShadowsocksDelete = QPushButton(
            self.translate("OutboundShadowsocksPanel", "Delete"), self)

        vboxBtn = QVBoxLayout()
        vboxBtn.addStretch()
        vboxBtn.addWidget(self.btnOutShadowsocksNew)
        vboxBtn.addWidget(self.btnOutShadowsocksDelete)
        
        hboxTableWidgetUser = QHBoxLayout()
        hboxTableWidgetUser.addWidget(tableWidget)
        hboxTableWidgetUser.addLayout(vboxBtn)

        vboxShadowsocksSettingPanel = QVBoxLayout()
        vboxShadowsocksSettingPanel.addLayout(hboxTableWidgetUser) 
        
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
        self.btnOutShadowsocksDelete.clicked.connect(self.onbtnOutShadowsocksDelete)
        self.btnOutShadowsocksNew.clicked.connect(self.onbtnOutShadowsocksNew)
    
    def tableWidgetNewRowItem(
            self, row, address=None, port=None, method=None, password=None, email=None, level=None, ota=False):
        spinBoxPort = QSpinBox()
        spinBoxLevel = QSpinBox()
        checkBoxOTA = QCheckBox()
        comboBoxMethod = QComboBox()
        comboBoxMethod.addItems(self.listMethodShadowsocksPanel)
        spinBoxPort.setMinimum(0)
        spinBoxPort.setMaximum(65535)
        
        spinBoxLevel.setMinimum(0)
        spinBoxLevel.setMaximum(65535)
        spinBoxLevel.setValue(0)
        checkBoxOTA.setCheckable(True)
        checkBoxOTA.setChecked(ota)
        if port:
            spinBoxPort.setValue(int(port))
        if level:
            spinBoxLevel.setValue(int(level))
        if method:
            comboBoxMethod.setCurrentText(method)
        self.tableWidgetOutShadowsocks.setItem(row, 0, QTableWidgetItem("" if not address else address))
        self.tableWidgetOutShadowsocks.setCellWidget(row, 1, spinBoxPort)
        self.tableWidgetOutShadowsocks.setCellWidget(row, 2, comboBoxMethod)
        self.tableWidgetOutShadowsocks.setItem(row, 3, QTableWidgetItem("" if not password else password))
        self.tableWidgetOutShadowsocks.setItem(row, 4, QTableWidgetItem("" if not email else email))
        self.tableWidgetOutShadowsocks.setCellWidget(row, 5, spinBoxLevel)
        self.tableWidgetOutShadowsocks.setCellWidget(row, 6, checkBoxOTA)

    def onbtnOutShadowsocksNew(self):
        row = self.tableWidgetOutShadowsocks.rowCount()
        if (not row):
            self.tableWidgetOutShadowsocks.setRowCount(row+1)
            self.tableWidgetNewRowItem(row)
        else:
            password = self.tableWidgetOutShadowsocks.item(row-1, 3)
            address = self.tableWidgetOutShadowsocks.item(row-1, 0)
            if (address and address.text() and password and password.text()):
                self.tableWidgetOutShadowsocks.setRowCount(row+1)
                self.tableWidgetNewRowItem(row)
    
    def onbtnOutShadowsocksDelete(self):
        self.tableWidgetOutShadowsocks.removeRow(self.tableWidgetOutShadowsocks.currentRow())

    def settingOutboundShadowsocksPanelFromJSONFile(self, outboundShadowsocksJSONFile=None, openFromJSONFile=False):
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
                    self.tableWidgetOutShadowsocks.setRowCount(i+1)
                    address = servers[i]["address"]
                    port = servers[i]["port"]
                    method = servers[i]["method"]
                    password = servers[i]["password"]
                    email = servers[i]["email"]
                    level = servers[i]["level"]
                    ota = servers[i]["ota"]
                    if method == "chacha20-ietf-poly1305":
                        method = "chacha20-poly1305"
                    self.tableWidgetNewRowItem(i, address, int(port), method, password, email, int(level), ota)
            except KeyError as e:
                logbook.writeLog("OutboundShadowsocks", "KeyError", e)
    
    def createOutboundShadowsocksJSONFile(self):
        serversNumber = self.tableWidgetOutShadowsocks.rowCount()
        outboundShadowsocksJSONFile = {}
        outboundShadowsocksJSONFile["servers"] = []  # clean default setting
        for i in range(serversNumber):
            servers = {}
            address = self.tableWidgetOutShadowsocks.item(i, 0)
            password = self.tableWidgetOutShadowsocks.item(i, 3)
            if not address.text() and not password.text():
                continue
            port = self.tableWidgetOutShadowsocks.cellWidget(i, 1)
            method = self.tableWidgetOutShadowsocks.cellWidget(i, 2)
            
            email = self.tableWidgetOutShadowsocks.item(i, 4)       
            level = self.tableWidgetOutShadowsocks.cellWidget(i, 5)
            ota = self.tableWidgetOutShadowsocks.cellWidget(i, 6)
            servers["email"] = email.text()
            servers["address"] = address.text()
            servers["port"] = int(port.value())
            servers["method"] = method.currentText()
            servers["password"] = password.text()
            servers["level"] = int(level.value())
            servers["ota"] = ota.isChecked()

            try:self.treasureChest.addLevel(level.value())
            except Exception:pass
            try:self.treasureChest.addEmail(email.text())
            except Exception:pass
            outboundShadowsocksJSONFile["servers"].append(copy.deepcopy(servers))

        return outboundShadowsocksJSONFile

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
