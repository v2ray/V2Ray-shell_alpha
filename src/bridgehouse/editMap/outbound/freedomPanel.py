#!/usr/bin/env python3

from PyQt5.QtWidgets import (QGroupBox, QLabel, QRadioButton,
                             QLineEdit, QWidget, QSpinBox, QGridLayout, 
                             QHBoxLayout, QPushButton)
from PyQt5.QtCore import QFileInfo, QCoreApplication
import sys

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    ### this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-4]))

from bridgehouse.editMap.inbound import logbook

class FreedomPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.freedomJSONFile = {
                                "domainStrategy": "AsIs",
                                "timeout": 0,
                                "redirect": "",
                                "userLevel": 0
                                }
        self.translate = QCoreApplication.translate

    def createFreedomSettingPanel(self):
        labelDomainStrategy = QLabel(self.translate("FreedomPanel", "Domain Strategy: "), self)
        self.radioBtnFreedomAsIs = QRadioButton(self.translate("FreedomPanel", "AsIs"), self)
        self.radioBtnFreedomUseIP = QRadioButton(self.translate("FreedomPanel", "UseIP"), self)
        labelTimeout = QLabel(self.translate("FreedomPanel", "Timeout: "), self)
        self.spinBoxFreedomTime = QSpinBox(self)
        labelRedirect = QLabel(self.translate("FreedomPanel", "Redirect Address: "), self)
        self.lineEditFreedomRedirect = QLineEdit(self)
        
        labeluserLevel = QLabel(
            self.translate("FreedomPanel", "User Level: "))
        self.spinBoxFreedomsuserLevel = QSpinBox()
        self.spinBoxFreedomsuserLevel.setRange(0, 65535)
        self.spinBoxFreedomsuserLevel.setValue(0)
        hboxuserLevel = QHBoxLayout()
        hboxuserLevel.addWidget(labeluserLevel)
        hboxuserLevel.addWidget(self.spinBoxFreedomsuserLevel)
        hboxuserLevel.addStretch()

        self.radioBtnFreedomAsIs.setChecked(True)
        self.spinBoxFreedomTime.setRange(0, 999)
        
        groupBoxFreedom = QGroupBox(self.translate("FreedomPanel", "Freedom"), self)
        
        hboxRdBtn = QHBoxLayout()
        hboxRdBtn.addWidget(labelDomainStrategy)
        hboxRdBtn.addWidget(self.radioBtnFreedomAsIs)
        hboxRdBtn.addWidget(self.radioBtnFreedomUseIP)
        hboxRdBtn.addStretch()
        
        hboxTimeout = QHBoxLayout()
        hboxRedirct = QHBoxLayout()
        hboxTimeout.addWidget(labelTimeout)
        hboxTimeout.addWidget(self.spinBoxFreedomTime)
        hboxTimeout.addStretch()
        
        hboxRedirct.addWidget(labelRedirect)
        hboxRedirct.addWidget(self.lineEditFreedomRedirect)
        hboxRedirct.addStretch()
        
        gridLayoutFreedom = QGridLayout()
        gridLayoutFreedom.addLayout(hboxRdBtn, 0, 0)
        gridLayoutFreedom.addLayout(hboxRedirct, 1, 0)
        gridLayoutFreedom.addLayout(hboxTimeout, 2, 0)
        gridLayoutFreedom.addLayout(hboxuserLevel, 3, 0)
        
        groupBoxFreedom.setLayout(gridLayoutFreedom)
        
        if (v2rayshellDebug):
            self.__debugBtn = QPushButton("__debugTest", self)
            gridLayoutFreedom.addWidget(self.__debugBtn, 4, 0)
            self.__debugBtn.clicked.connect(self.__debugTest)
        
        self.settingfreedomPanelFromJSONFile(self.freedomJSONFile, True)
        
        return groupBoxFreedom
    
    def settingfreedomPanelFromJSONFile(self, freedomJSONFile = {}, openFromJSONFile = False):
        logbook.setisOpenJSONFile(openFromJSONFile)
        
        if (freedomJSONFile == None): freedomJSONFile = {}

        try:
            freedomJSONFile["domainStrategy"]
        except KeyError as e:
            logbook.writeLog("freedom", "KeyError", e)
            freedomJSONFile["domainStrategy"] = "AsIs"
        
        try:
            freedomJSONFile["timeout"]
        except KeyError as e:
            logbook.writeLog("freedom", "KeyError", e)
            freedomJSONFile["timeout"] = 0
        
        try:
            freedomJSONFile["redirect"]
        except KeyError as e:
            logbook.writeLog("freedom", "KeyError", e)
            freedomJSONFile["redirect"] = ""
            
        try:
            freedomJSONFile["userLevel"]
        except KeyError as e:
            logbook.writeLog("freedom", "KeyError", e)
            freedomJSONFile["userLevel"] = 0

        domainStrategy = freedomJSONFile["domainStrategy"]
        
        if (domainStrategy == "AsIs"):
                self.radioBtnFreedomAsIs.setChecked(True)
        if (domainStrategy == "UseIP"):
                self.radioBtnFreedomUseIP.setChecked(True)
        
        self.lineEditFreedomRedirect.setText(str(freedomJSONFile["redirect"]))
        
        try:
            self.spinBoxFreedomTime.setValue(int(freedomJSONFile["timeout"]))
        except (TypeError, ValueError) as e:
            logbook.writeLog("freedom", "ValueError or TypeError", e)
            self.spinBoxFreedomTime.setValue(0)
            
        try:
            self.spinBoxFreedomsuserLevel.setValue(int(freedomJSONFile["userLevel"]))
        except (TypeError, ValueError) as e:
            logbook.writeLog("freedom", "ValueError or TypeError", e)
            self.spinBoxFreedomsuserLevel.setValue(0)
            
        try:
            self.treasureChest.addLevel(int(freedomJSONFile["userLevel"]))
        except Exception:
            pass

    def createFreedomJSONFile(self):
        freedomJSONFile = {}
        if (self.radioBtnFreedomAsIs.isChecked()):
            freedomJSONFile["domainStrategy"] = "AsIs"
        if (self.radioBtnFreedomUseIP.isChecked()):
            freedomJSONFile["domainStrategy"] = "UseIP"
        freedomJSONFile["timeout"]   = int(self.spinBoxFreedomTime.value())
        freedomJSONFile["redirect"]  = self.lineEditFreedomRedirect.text()
        freedomJSONFile["userLevel"] = int(self.spinBoxFreedomsuserLevel.value())

        return freedomJSONFile
    
    def clearfreedomPanel(self):
        self.radioBtnFreedomAsIs.setChecked(True)
        self.radioBtnFreedomUseIP.setChecked(False)
        self.lineEditFreedomRedirect.clear()
        self.spinBoxFreedomsuserLevel.setValue(0)
        self.spinBoxFreedomTime.setValue(0)

    def __debugTest(self):
        import json
        print(json.dumps(self.createFreedomJSONFile(), indent = 4, sort_keys = False))
    
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = FreedomPanel()
    ex.createFreedomSettingPanel()
    ex.setGeometry(300, 350, 380, 160)
    ex.show()
    sys.exit(app.exec_())
