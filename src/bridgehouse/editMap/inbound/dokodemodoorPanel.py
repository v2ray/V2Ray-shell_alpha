#!/usr/bin/env python3

from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QSpinBox,
                             QCheckBox, QGroupBox, QHBoxLayout, QVBoxLayout, 
                             QToolTip, QPushButton)
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QFileInfo, QCoreApplication
import sys, re, platform

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    ### this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-4]))

from bridgehouse.editMap.inbound import logbook

class DokodemodoorPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.dokodemodoorJSONFile = {
                                    "address": "",
                                    "port": 443,
                                    "network": "",
                                    "timeout": 300,
                                    "followRedirect": False,
                                    "userLevel": 0
                                    }
        self.translate = QCoreApplication.translate

    def createDokodemodoorSettingPanel(self):
        labelAddress = QLabel(
            self.translate("DokodemodoorPanel", "Address: "), self)
        self.lineEditDokodemodoorAddress = QLineEdit()
        labelPort = QLabel(
            self.translate("DokodemodoorPanel", "Port: "), self)
        self.spinBoxDokodemodoorPort = QSpinBox()
        labelNetwork = QLabel(
            self.translate("DokodemodoorPanel", "Network: "), self)
        self.checkBoxDokodemodoorTCP = QCheckBox("TCP", self)
        self.checkBoxDokodemodoorUDP = QCheckBox("UDP", self)
        labelTimeout = QLabel(
            self.translate("DokodemodoorPanel", "Timeout: "), self)
        self.spinBoxDokodemodoorTimeout = QSpinBox()
        self.checkBoxDokodemodoorFollowRedirect = QCheckBox(
            self.translate("DokodemodoorPanel", "Follow Redirect"), self)
        
        labeluserLevel = QLabel(
            self.translate("DokodemodoorPanel", "User Level: "))
        self.spinBoxDokodemodooruserLevel = QSpinBox()
        self.spinBoxDokodemodooruserLevel.setRange(0, 65535)
        self.spinBoxDokodemodooruserLevel.setValue(0)
        
        hboxuserLevel = QHBoxLayout()
        hboxuserLevel.addWidget(labeluserLevel)
        hboxuserLevel.addWidget(self.spinBoxDokodemodooruserLevel)
        hboxuserLevel.addStretch()
        
        self.spinBoxDokodemodoorPort.setRange(0, 65535)
        self.spinBoxDokodemodoorTimeout.setRange(0, 999)
        self.spinBoxDokodemodoorTimeout.setValue(300)
        self.spinBoxDokodemodoorPort.setValue(443)
        self.checkBoxDokodemodoorFollowRedirect.setChecked(False)
        
        hboxAdress = QHBoxLayout()
        hboxAdress.addWidget(labelAddress)
        hboxAdress.addWidget(self.lineEditDokodemodoorAddress)
        hboxAdress.addWidget(labelPort)
        hboxAdress.addWidget(self.spinBoxDokodemodoorPort)
        hboxAdress.addStretch()
        
        hboxNetwork = QHBoxLayout()
        hboxNetwork.addWidget(labelNetwork)
        hboxNetwork.addWidget(self.checkBoxDokodemodoorTCP)
        hboxNetwork.addWidget(self.checkBoxDokodemodoorUDP)
        hboxNetwork.addStretch()
        
        hboxTimeout = QHBoxLayout()
        hboxTimeout.addWidget(labelTimeout)
        hboxTimeout.addWidget(self.spinBoxDokodemodoorTimeout)
        hboxTimeout.addWidget(self.checkBoxDokodemodoorFollowRedirect)
        hboxTimeout.addStretch()
        
        groupBoxDokodemodoor = QGroupBox(
            self.translate("DokodemodoorPanel", "Dokodemo-door"), self)
        vboxDokodemodoor = QVBoxLayout()
        vboxDokodemodoor.addLayout(hboxAdress)
        vboxDokodemodoor.addLayout(hboxTimeout)
        vboxDokodemodoor.addLayout(hboxNetwork)
        vboxDokodemodoor.addLayout(hboxuserLevel)
        
        groupBoxDokodemodoor.setLayout(vboxDokodemodoor)
        
        if (v2rayshellDebug):
            self.__debugBtn = QPushButton("__debugTest", self)
            self.__debugBtn.clicked.connect(self.__debugTest)
            vboxDokodemodoor.addWidget(self.__debugBtn)
            self.settingdokodemodoorPanelFromJSONFile(self.dokodemodoorJSONFile, True)

        self.createDokodemodoorSignals()
        return groupBoxDokodemodoor
        
    def createDokodemodoorSignals(self):
        self.checkBoxDokodemodoorFollowRedirect.clicked.connect(self.oncheckBoxDokodemodoorFollowRedirect)
    
    def oncheckBoxDokodemodoorFollowRedirect(self):
        if (platform.system() == "Linux"):
            self.checkBoxDokodemodoorFollowRedirect.setCheckable(True)
        else:
            QToolTip.showText(QCursor.pos(),
                              self.translate("DokodemodoorPanel", "Only suport Linux System."), 
                              self.checkBoxDokodemodoorFollowRedirect)

    def settingdokodemodoorPanelFromJSONFile(self, dokodemodoorJSONFile = {}, openFromJSONFile = False):
        logbook.setisOpenJSONFile(openFromJSONFile)
        
        if (dokodemodoorJSONFile == None): dokodemodoorJSONFile = {}

        try:
            dokodemodoorJSONFile["address"]
        except KeyError as e:
            logbook.writeLog("dokodemodoor", "KeyError", e)
            dokodemodoorJSONFile["address"] = ""
            
        try:
            dokodemodoorJSONFile["port"]
        except KeyError as e:
            logbook.writeLog("dokodemodoor", "KeyError", e)
            dokodemodoorJSONFile["port"] = 443

        try:
            dokodemodoorJSONFile["network"]
        except KeyError as e:
            logbook.writeLog("dokodemodoor", "KeyError", e)
            dokodemodoorJSONFile["network"] = ""
            
        try:
            dokodemodoorJSONFile["timeout"]
        except KeyError as e:
            logbook.writeLog("dokodemodoor", "KeyError", e)
            dokodemodoorJSONFile["timeout"] = 300

        try:
            dokodemodoorJSONFile["followRedirect"]
        except KeyError as e:
            logbook.writeLog("dokodemodoor", "KeyError", e)
            dokodemodoorJSONFile["followRedirect"] = False
        
        try:
            dokodemodoorJSONFile["userLevel"]
        except KeyError as e:
            logbook.writeLog("dokodemodoor", "KeyError", e)
            dokodemodoorJSONFile["userLevel"] = 0


        self.lineEditDokodemodoorAddress.setText(str(dokodemodoorJSONFile["address"]))
        try:
            self.spinBoxDokodemodoorPort.setValue(int(dokodemodoorJSONFile["port"]))
        except (ValueError, TypeError) as e:
            logbook.writeLog("dokodemodoor", "ValueError or TypeError", e)
            self.spinBoxDokodemodoorPort.setValue(443)
        
        try:
            self.spinBoxDokodemodoorTimeout.setValue(int(dokodemodoorJSONFile["timeout"]))
        except (ValueError, TypeError) as e:
            logbook.writeLog("dokodemodoor", "ValueError or TypeError", e)
            self.spinBoxDokodemodoorTimeout.setValue(300)
        self.checkBoxDokodemodoorFollowRedirect.setChecked(bool(dokodemodoorJSONFile["followRedirect"]))
        
        try:
            self.spinBoxDokodemodooruserLevel.setValue(int(dokodemodoorJSONFile["userLevel"]))
        except (ValueError, TypeError) as e:
            logbook.writeLog("dokodemodoor", "ValueError or TypeError", e)
            self.spinBoxDokodemodooruserLevel.setValue(0)
            
        try:
            self.treasureChest.addLevel(self.spinBoxDokodemodooruserLevel.value())
        except Exception:pass
        
        udp = re.search("udp", dokodemodoorJSONFile["network"].lower())
        tcp = re.search("tcp", dokodemodoorJSONFile["network"].lower())
        if (bool(tcp)):self.checkBoxDokodemodoorTCP.setChecked(True)
        if (bool(udp)):self.checkBoxDokodemodoorUDP.setChecked(True)
            
    def createDokodemodorrJSONFile(self):
        dokodemodoorJSONFile = {}
        tcp = self.checkBoxDokodemodoorTCP.isChecked()
        udp = self.checkBoxDokodemodoorUDP.isChecked()
        port = ""   ### defaut
        if (tcp):
            port = "tcp"
        if (udp):
            port = "udp"
        if (tcp and udp):
            port = "tcp,udp"
        dokodemodoorJSONFile["address"]        = self.lineEditDokodemodoorAddress.text()
        dokodemodoorJSONFile["port"]           = self.spinBoxDokodemodoorPort.value()
        dokodemodoorJSONFile["network"]        = port
        dokodemodoorJSONFile["timeout"]        = self.spinBoxDokodemodoorTimeout.value()
        dokodemodoorJSONFile["followRedirect"] = self.checkBoxDokodemodoorFollowRedirect.isChecked()
        dokodemodoorJSONFile["userLevel"]      = self.spinBoxDokodemodooruserLevel.value()
        
        try:
            self.treasureChest.addLevel(self.spinBoxDokodemodooruserLevel.value())
        except Exception:
            pass
        return dokodemodoorJSONFile
    
    def cleardokodemodoorPanel(self):
        self.lineEditDokodemodoorAddress.clear()
        self.spinBoxDokodemodoorPort.setValue(443)
        self.spinBoxDokodemodoorTimeout.setValue(300)
        self.checkBoxDokodemodoorFollowRedirect.setChecked(False)
        self.spinBoxDokodemodooruserLevel.setValue(0)
        self.checkBoxDokodemodoorTCP.setChecked(False)
        self.checkBoxDokodemodoorUDP.setChecked(False)
    
    def __debugTest(self):
        import json
        print(json.dumps(self.createDokodemodorrJSONFile(), indent=4, sort_keys = False))

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = DokodemodoorPanel()
    ex.createDokodemodoorSettingPanel()
    ex.setGeometry(300, 300, 680, 230)
    ex.show()
    sys.exit(app.exec_())