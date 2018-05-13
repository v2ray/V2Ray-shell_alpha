#!/usr/bin/env python3

from PyQt5.QtWidgets import (QWidget, QTextEdit, QVBoxLayout, QApplication, 
                             QGroupBox, QLineEdit, QPushButton, QHBoxLayout, QLabel)
from PyQt5.QtCore import QFileInfo, QCoreApplication
import sys, json, copy, re

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    # this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-3]))

from bridgehouse.editMap.port import treasureChest


class apiTAB(QWidget):
    def __init__(self, CaptainstreasureChest=False):
        super(apiTAB, self).__init__()
        self.apiJSONFILE = {
                            "tag": "api",
                            "services": [
                                "HandlerService",
                                "LoggerService"
                                ]
                            }
        
        self.translate = QCoreApplication.translate
        if (CaptainstreasureChest):
            self.treasureChest = CaptainstreasureChest
        else:
            self.treasureChest = treasureChest.treasureChest()
        
    def createapiTAB(self):
        self.groupBoxAPI = QGroupBox("API")
        self.groupBoxAPI.setCheckable(True)
        self.groupBoxAPI.setChecked(False)
        
        labelAPI = QLabel(self.translate("apiTAB","API's Tag: "))
        self.lineEditTagName = QLineEdit("api")
        hboxApi = QHBoxLayout()
        hboxApi.addWidget(labelAPI)
        hboxApi.addWidget(self.lineEditTagName)
        hboxApi.addStretch()
        
        hboxServices = QHBoxLayout()
        labelServices = QLabel(self.translate("apiTAB", "Services: "))
        self.lineEditServices = QLineEdit("HandlerService, LoggerService, StatsService")
        hboxServices.addWidget(labelServices)
        hboxServices.addWidget(self.lineEditServices)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hboxApi)
        vbox.addLayout(hboxServices)
        vbox.addStretch()
        
        self.groupBoxAPI.setLayout(vbox)
        self.lineEditTagName.editingFinished.connect(
            lambda:self.treasureChest.setApitag([x.strip() for x in re.split(r"[,;]", self.lineEditTagName.text())]))
        
        if v2rayshellDebug:
            self.__debugBtn = QPushButton("__debugTest", self)
            vbox.addWidget(self.__debugBtn)
            self.__debugBtn.clicked.connect(self.__debugTest)
        
        return self.groupBoxAPI
    
    def settingAPITabFromJSONFile(self, apiJSONFile):
        if not apiJSONFile:
            apiJSONFile = {}
            self.groupBoxAPI.setChecked(False)
        else:
            self.groupBoxAPI.setChecked(True)

        try:
            apiJSONFile['tag']
        except Exception:
            apiJSONFile['tag'] = 'api'
            
        try:
            apiJSONFile["services"]
        except Exception:
            apiJSONFile["services"] = "HandlerService, LoggerService, StatsService"

        self.lineEditServices.clear()
        self.lineEditTagName.clear()
        self.lineEditTagName.setText(apiJSONFile['tag'])
        try:
            if isinstance(apiJSONFile["services"], list):
                self.lineEditServices.setText(", ".join(apiJSONFile["services"]))
            else:
                self.lineEditServices.setText(apiJSONFile["services"])
        except Exception:
            pass

    def createApiJSONFile(self):
        if self.groupBoxAPI:
            api = {}
            api["tag"] = self.lineEditTagName.text()
            api["services"] = [x.strip() for x in re.split(r"[,;]", self.lineEditServices.text())]
            return api
        return None
    
    def __debugTest(self):
        print(json.dumps(self.createApiJSONFile(), indent=4, sort_keys=False))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = apiTAB()
    v = QVBoxLayout()
    v.addWidget(ex.createapiTAB())
    ex.setLayout(v)
    ex.setGeometry(200, 100, 400, 300)
    ex.show()
    sys.exit(app.exec_())
