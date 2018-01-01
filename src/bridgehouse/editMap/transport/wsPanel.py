#!/usr/bin/env python3

from PyQt5.QtWidgets import (QLabel, QWidget, QGroupBox, 
                             QLineEdit, QHBoxLayout, QVBoxLayout, 
                             QPushButton)
from PyQt5.QtCore import QFileInfo, QCoreApplication
import sys

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    ### this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.path().split("/")
    sys.path.append("/".join(srcPath[:-3]))

from bridgehouse.editMap.transport import logbook

class wsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.wsJSONFile = {
                            "path": "",
                            "headers": {
                                "Host": "v2ray.com"
                            }
                        }
        self.translate = QCoreApplication.translate

    def createwsSettingPanel(self):
        labelPath = QLabel(self.translate("wsPanel", "Path: "), self)
        self.lineEditwebsocksPath = QLineEdit()
        labelHost = QLabel(self.translate("wsPanel", "Host: "), self)
        self.lineEditwebsocksHost = QLineEdit()
        
        hboxPath = QHBoxLayout()
        hboxPath.addWidget(labelPath)
        hboxPath.addWidget(self.lineEditwebsocksPath)
        
        hboxHost = QHBoxLayout()
        hboxHost.addWidget(labelHost)
        hboxHost.addWidget(self.lineEditwebsocksHost)
        
        vboxwsSetting = QVBoxLayout()
        vboxwsSetting.addLayout(hboxPath)
        vboxwsSetting.addLayout(hboxHost)
        
        self.groupBoxwsSetting = groupBoxwsSetting = QGroupBox(
            self.translate("wsPanel", "WebSocket Setting"), self)
        groupBoxwsSetting.setCheckable(True)
        groupBoxwsSetting.setChecked(False)
        groupBoxwsSetting.adjustSize()
        groupBoxwsSetting.setLayout(vboxwsSetting)
        
        if (v2rayshellDebug):
            self.__debugBtn = QPushButton("__debugTest", self)
            self.__debugBtn.clicked.connect(self.__debugTest)
            vboxwsSetting.addWidget(self.__debugBtn)
            self.settingwsPanelFromJSONFile(self.wsJSONFile, True)
            
        return groupBoxwsSetting
    
    def settingwsPanelFromJSONFile(self, wsJSONFile, openFromJSONFile = False):
        logbook.setisOpenJSONFile(openFromJSONFile)

        if (wsJSONFile == None): 
            wsJSONFile = {}
            self.groupBoxwsSetting.setChecked(False)
            self.lineEditwebsocksHost.clear()
            self.lineEditwebsocksPath.clear()
            return False
        try:
            wsJSONFile["path"]
        except KeyError as e:
            logbook.writeLog("transport ws", "KeyError", e)
            wsJSONFile["path"] = ""
            
        try:
            wsJSONFile["headers"]
        except KeyError as e:
            logbook.writeLog("transport ws", "KeyError", e)
            wsJSONFile["headers"] = {}
            
        try:
            wsJSONFile["headers"]["Host"]
        except KeyError as e:
            logbook.writeLog("transport ws", "KeyError", e)
            wsJSONFile["headers"]["Host"] = ""

        self.lineEditwebsocksPath.setText(str(wsJSONFile["path"]))
        self.lineEditwebsocksHost.setText(str(wsJSONFile["headers"]["Host"]))

    def createwsSettingJSONFile(self):
        wsJSONFile = {}
        wsJSONFile["headers"] = {}
        wsJSONFile["headers"]["Host"] = self.lineEditwebsocksHost.text()
        wsJSONFile["path"] = self.lineEditwebsocksPath.text()
        
        return wsJSONFile
    
    def clearwsPanel(self):
        self.lineEditwebsocksHost.clear()
        self.lineEditwebsocksPath.clear()
        self.groupBoxwsSetting.setChecked(False)
    
    def __debugTest(self):
        import json
        print(json.dumps(self.createwsSettingJSONFile(), indent=4, sort_keys = False))

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = wsPanel()
    ex.createwsSettingPanel()
    ex.setGeometry(300, 300, 680, 230)
    ex.show()
    sys.exit(app.exec_())