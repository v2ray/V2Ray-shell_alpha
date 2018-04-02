#!/usr/bin/env python3

from PyQt5.QtWidgets import (QWidget, QGroupBox, QRadioButton, QHBoxLayout, QPushButton)
from PyQt5.QtCore import QFileInfo, QCoreApplication
import sys

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    # this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-4]))

from bridgehouse.editMap.inbound import logbook


class BlackholePanel(QWidget):

    def __init__(self):
        super().__init__()
        self.blackholeJSONFile = {
                                    "response": {
                                            "type": "none"
                                            }
                                }
        self.translate = QCoreApplication.translate
        
    def createBlackholeSettingPanel(self):
        self.radioBtnBlackholeNone = QRadioButton("None", self)
        self.radioBtnBlackholeHttp = QRadioButton("Http", self)
        
        self.radioBtnBlackholeNone.setChecked(True)
        
        hboxBlackholeSetting = QHBoxLayout()
        hboxBlackholeSetting.addWidget(self.radioBtnBlackholeNone)
        hboxBlackholeSetting.addWidget(self.radioBtnBlackholeHttp)
        hboxBlackholeSetting.addStretch()
        
        self.groupBoxBlackhole = QGroupBox(self.translate("BlackholePanel", "Blackhole"), self)
        self.groupBoxBlackhole.setLayout(hboxBlackholeSetting)
        
        if (v2rayshellDebug):
            self.__debugBtn = QPushButton("__debugTest", self)
            hboxBlackholeSetting.addWidget(self.__debugBtn)
            self.__debugBtn.clicked.connect(self.__debugTest)
            self.settingblackholePanelFromJSONFile(self.blackholeJSONFile, True)
            
        return self.groupBoxBlackhole
    
    def settingblackholePanelFromJSONFile(self, blackholeJSONFile={}, openFromJSONFile=False):
        logbook.setisOpenJSONFile(openFromJSONFile)
        
        if (not blackholeJSONFile): blackholeJSONFile = {}

        try:
            blackholeJSONFile["response"]
        except KeyError as e:
            logbook.writeLog("blackhole", "KeyError", e)
            blackholeJSONFile["response"] = {}
        try:
            blackholeJSONFile["response"]["type"]
        except KeyError as e:
            logbook.writeLog("blackhole", "KeyError", e)
            blackholeJSONFile["response"]["type"] = "none"

        blackholetype = blackholeJSONFile["response"]["type"]
        if (blackholetype == "http"):
            self.radioBtnBlackholeHttp.setChecked(True)
        if (blackholetype == "none"):
            self.radioBtnBlackholeNone.setChecked(True)
  
    def createblackholeJSONFile(self):
        blackholeJSONFile = {}
        blackholeJSONFile["response"] = {}
        if (self.radioBtnBlackholeHttp.isChecked()):
            blackholeJSONFile["response"]["type"] = "http"
        if (self.radioBtnBlackholeNone.isChecked()):
            blackholeJSONFile["response"]["type"] = "none"
            
        return blackholeJSONFile
    
    def clearblackholePanel(self):
        self.radioBtnBlackholeNone.setChecked(True)
        self.radioBtnBlackholeHttp.setChecked(False)
            
    def __debugTest(self):
        import json
        print(json.dumps(self.createblackholeJSONFile(), indent=4, sort_keys=False))

          
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = BlackholePanel()
    ex.createBlackholeSettingPanel()
    ex.setGeometry(300, 300, 680, 600)
    ex.show()
    sys.exit(app.exec_())
