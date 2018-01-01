#!/usr/bin/env python3

from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox, QSpinBox,
                             QCheckBox, QGridLayout, QVBoxLayout,
                             QGroupBox, QPushButton, QHBoxLayout)
from PyQt5.QtCore import QFileInfo, QCoreApplication

import sys

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    ### this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.path().split("/")
    sys.path.append("/".join(srcPath[:-3]))

from bridgehouse.editMap.inbound import logbook

class InboundShadowsocksPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.inboundShadowsocksJSONFile = {
                                    "email": "",
                                    "method": "",
                                    "password": "",
                                    "udp": False,
                                    "level": 1,
                                    "ota": True
                                    }
        self.listMethodShadowsocksPanel = "aes-256-cfb", "aes-128-cfb", "chacha20", "chacha20-ietf", "aes-256-gcm", "aes-128-gcm", "chacha20-poly1305"
        self.translate = QCoreApplication.translate

    def createShadowsocksSettingPanel(self):
        labelEmail = QLabel(
            self.translate("InboundShadowsocksPanel", "Email: "), self)
        self.lineEditInboundShadowsocksEmail = QLineEdit()
        labelMethod = QLabel(
            self.translate("InboundShadowsocksPanel", "Method: "), self)
        self.comboBoxInboundShadowsocksMethod = QComboBox()
        labelPassowrd = QLabel(
            self.translate("InboundShadowsocksPanel", "Password: "), self)
        self.lineEditInboundShadowsocksPassowrd = QLineEdit()
        self.checkBoxInboundShadowsocksUDP = QCheckBox(
            self.translate("InboundShadowsocksPanel", "open UDP forwarding"), self)
        labelLevel = QLabel(
            self.translate("InboundShadowsocksPanel", "User Level: "), self)
        self.spinBoxInboundShadowsocksLevel = QSpinBox()
        self.checkBoxInboundShadowsocksOTA = QCheckBox(
            self.translate("InboundShadowsocksPanel", "One Time Auth (OTA)"), self)
        
        self.comboBoxInboundShadowsocksMethod.addItems(self.listMethodShadowsocksPanel)
        self.checkBoxInboundShadowsocksUDP.setChecked(False)
        self.spinBoxInboundShadowsocksLevel.setRange(0, 65535)
        self.spinBoxInboundShadowsocksLevel.setValue(0)

        gridBoxInboundShadowsocks = QGridLayout(self)
        gridBoxInboundShadowsocks.addWidget(labelEmail, 0, 0)
        gridBoxInboundShadowsocks.addWidget(self.lineEditInboundShadowsocksEmail, 0, 1)
        gridBoxInboundShadowsocks.addWidget(labelMethod, 1, 0)
        gridBoxInboundShadowsocks.addWidget(self.comboBoxInboundShadowsocksMethod, 1, 1)
        gridBoxInboundShadowsocks.addWidget(labelPassowrd, 2, 0)
        gridBoxInboundShadowsocks.addWidget(self.lineEditInboundShadowsocksPassowrd, 2, 1)
        gridBoxInboundShadowsocks.addWidget(labelLevel, 3, 0)
        
        hboxLevel = QHBoxLayout()
        hboxLevel.addWidget(self.spinBoxInboundShadowsocksLevel)
        hboxLevel.addStretch()
        gridBoxInboundShadowsocks.addLayout(hboxLevel, 3, 1)
        
        gridBoxInboundShadowsocks.addWidget(self.checkBoxInboundShadowsocksUDP, 4, 0)
        gridBoxInboundShadowsocks.addWidget(self.checkBoxInboundShadowsocksOTA, 5, 0)
        
        if (v2rayshellDebug):
            self.__debugBtn = QPushButton("__debugTest", self)
            gridBoxInboundShadowsocks.addWidget(self.__debugBtn, 6, 0)
            self.__debugBtn.clicked.connect(self.__debugTest)
            self.settingInboundShadowsocksPanelFromJSONFile(self.inboundShadowsocksJSONFile, True)

        groupBoxInboundShadowsocks = QGroupBox(
            self.translate("InboundShadowsocksPanel", "Shadowsocks"), self)
        groupBoxInboundShadowsocks.setLayout(gridBoxInboundShadowsocks)
        
        self.createShadowsocksPanelSignals()
        
        return groupBoxInboundShadowsocks
    
    def createShadowsocksPanelSignals(self):
        pass
    
    def settingInboundShadowsocksPanelFromJSONFile(self, inboundShadowsocksJSONFile = {}, openFromJSONFile = False):
        logbook.setisOpenJSONFile(openFromJSONFile)
        
        if (inboundShadowsocksJSONFile == None): inboundShadowsocksJSONFile = {}

        try:
            inboundShadowsocksJSONFile["email"]
        except KeyError as e:
            logbook.writeLog("InboundShadowsocks", "KeyError", e)
            inboundShadowsocksJSONFile["email"] = ""
        try:
            inboundShadowsocksJSONFile["method"]
        except KeyError as e:
            logbook.writeLog("InboundShadowsocks", "KeyError", e)
            inboundShadowsocksJSONFile["method"] = ""
            
        try:
            inboundShadowsocksJSONFile["password"]
        except KeyError as e:
            logbook.writeLog("InboundShadowsocks", "KeyError", e)
            inboundShadowsocksJSONFile["password"] = ""
            
        try:
            inboundShadowsocksJSONFile["udp"]
        except KeyError as e:
            logbook.writeLog("InboundShadowsocks", "KeyError", e)
            inboundShadowsocksJSONFile["udp"] = False
        
        try:
            inboundShadowsocksJSONFile["level"]
        except KeyError as e:
            logbook.writeLog("InboundShadowsocks", "KeyError", e)
            inboundShadowsocksJSONFile["level"] = 1

        try:
            inboundShadowsocksJSONFile["ota"]
        except KeyError as e:
            logbook.writeLog("InboundShadowsocks", "KeyError", e)
            inboundShadowsocksJSONFile["ota"] = True

        self.lineEditInboundShadowsocksEmail.setText(str(inboundShadowsocksJSONFile["email"]))
        self.comboBoxInboundShadowsocksMethod.setCurrentText(str(inboundShadowsocksJSONFile["method"]))
        self.lineEditInboundShadowsocksPassowrd.setText(str(inboundShadowsocksJSONFile["password"]))
        self.checkBoxInboundShadowsocksUDP.setChecked(bool(inboundShadowsocksJSONFile["udp"]))
        self.checkBoxInboundShadowsocksOTA.setChecked(bool(inboundShadowsocksJSONFile["ota"]))
        
        try:
            self.spinBoxInboundShadowsocksLevel.setValue(int(inboundShadowsocksJSONFile["level"]))
        except (TypeError, ValueError) as e:
            logbook.writeLog("InboundShadowsocks", "KeyError", e)
            self.spinBoxInboundShadowsocksLevel.setValue(1)
            
        try:
            self.treasureChest.addLevel(self.spinBoxInboundShadowsocksLevel.value())
            self.treasureChest.addEmail(self.lineEditInboundShadowsocksEmail.text())
        except Exception:
            pass
        
    def createInboundShadowsocksJSONFile(self):
        inboundShadowsocksJSONFile= {}
        inboundShadowsocksJSONFile["email"]    = self.lineEditInboundShadowsocksEmail.text()
        inboundShadowsocksJSONFile["method"]   = self.comboBoxInboundShadowsocksMethod.currentText()
        inboundShadowsocksJSONFile["password"] = self.lineEditInboundShadowsocksPassowrd.text()
        inboundShadowsocksJSONFile["udp"]      = self.checkBoxInboundShadowsocksUDP.isChecked()
        inboundShadowsocksJSONFile["level"]    = self.spinBoxInboundShadowsocksLevel.value()
        inboundShadowsocksJSONFile["ota"]      = self.checkBoxInboundShadowsocksOTA.isChecked()
        
        try:
            self.treasureChest.addLevel(self.spinBoxInboundShadowsocksLevel.value())
            self.treasureChest.addEmail(self.lineEditInboundShadowsocksEmail.text())
        except Exception:
            pass
        
        return inboundShadowsocksJSONFile
    
    def clearinboundShadowsocksPanel(self):
        self.lineEditInboundShadowsocksEmail.clear()
        self.comboBoxInboundShadowsocksMethod.setCurrentIndex(0)
        self.lineEditInboundShadowsocksPassowrd.clear()
        self.checkBoxInboundShadowsocksUDP.setChecked(False)
        self.checkBoxInboundShadowsocksOTA.setChecked(False)
        self.spinBoxInboundShadowsocksLevel.setValue(0)
        
    def __debugTest(self):
        import json
        print(json.dumps(self.createInboundShadowsocksJSONFile(), indent=4, sort_keys = False))
        
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = InboundShadowsocksPanel()
    v = QVBoxLayout()
    v.addWidget(ex.createShadowsocksSettingPanel())
    ex.setLayout(v)
    ex.setGeometry(300, 300, 680, 260)
    ex.show()
    sys.exit(app.exec_())
