#!/usr/bin/env python3

from PyQt5.QtWidgets import (QWidget, QGroupBox, QApplication,
                             QHBoxLayout, QVBoxLayout, QTextEdit,
                             QLabel, QComboBox, QPushButton)
from PyQt5.QtCore import QFileInfo, QCoreApplication
import sys, json

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    ### this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.path().split("/")
    sys.path.append("/".join(srcPath[:-3]))
        
from bridgehouse.editMap.transport import logbook

class TcpPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.tcpJSONFile = {
                            "header": {
                                "type": "none"
                                }
                            }
        self.translate = QCoreApplication.translate
        self.httpHeader = "none", "http"
        
    def createTCPSettingPanel(self):
        labelHttpHeaderType = QLabel(
            self.translate("TcpPanel", "Http type: "), self)
        self.comboxHttpHeaderType = QComboBox(self)
        self.btnHttpHeaderTypeClear = QPushButton(
            self.translate("TcpPanel", "Clear"), self)
        self.textHttpHeaderType = QTextEdit()
    
        
        self.comboxHttpHeaderType.addItems(self.httpHeader)
        self.btnHttpHeaderTypeClear.hide()       
        self.textHttpHeaderType.hide()
        self.textHttpHeaderType.adjustSize()
        
        hboxhttpHeader = QHBoxLayout()
        hboxhttpHeader.addWidget(labelHttpHeaderType)
        hboxhttpHeader.addWidget(self.comboxHttpHeaderType)
        hboxhttpHeader.addWidget(self.btnHttpHeaderTypeClear)
        hboxhttpHeader.addStretch()
        
        vboxTCPSetting = QVBoxLayout()
        vboxTCPSetting.addLayout(hboxhttpHeader)
        vboxTCPSetting.addWidget(self.textHttpHeaderType)
        
        self.groupBoxTCPSetting = groupBoxTCPSetting = QGroupBox(
            self.translate("TcpPanel", "TCP Settings"), self)
        groupBoxTCPSetting.setCheckable(True)
        groupBoxTCPSetting.setChecked(False)
        groupBoxTCPSetting.adjustSize()
        groupBoxTCPSetting.setLayout(vboxTCPSetting)
        
        self.createTCPSettingPanelSignles()

        if(v2rayshellDebug):
            self.__debugBtn = QPushButton("__debugTest", self)
            v = QVBoxLayout()
            v.addWidget(groupBoxTCPSetting)
            v.addWidget(self.__debugBtn)
            v.addStretch()
            self.setLayout(v)
            self.__debugBtn.clicked.connect(self.__debugTest)
            self.settingtcpPanelFromJSONFile(self.tcpJSONFile, True)
            return
        
        return groupBoxTCPSetting
    
    def createTCPSettingPanelSignles(self):
        self.comboxHttpHeaderType.currentTextChanged.connect(self.oncomboxHttpHeaderType)
        self.btnHttpHeaderTypeClear.clicked.connect(self.onbtnHttpHeaderTypeClear)
        
    def onbtnHttpHeaderTypeClear(self):
        self.textHttpHeaderType.clear()
        
    def oncomboxHttpHeaderType(self, e):
        if (e == "none"):
            self.textHttpHeaderType.hide()
            self.btnHttpHeaderTypeClear.hide()
            
        if (e == "http"):
            self.btnHttpHeaderTypeClear.show()
            self.textHttpHeaderType.show()
            
    def jsonDataValitor(self, jsonData):
        try:
            data = json.loads(str(jsonData))
        except ValueError as e:
            return -1, e
        return 0, data
    
    def settingtcpPanelFromJSONFile(self, tcpJSONFile, openFromJSONFile = False):
        logbook.setisOpenJSONFile(openFromJSONFile)  
        
        if (tcpJSONFile == None): 
            tcpJSONFile = {}
            self.groupBoxTCPSetting.setChecked(False)
            self.textHttpHeaderType.clear()
            self.comboxHttpHeaderType.setCurrentText("none")
            return 
        
        try:
            tcpJSONFile["header"]
        except KeyError as e:
            logbook.writeLog("transport TCP", "KeyError", e)
            tcpJSONFile["header"] = {}
            
        try:
            tcpJSONFile["header"]["type"]
        except KeyError as e:
            logbook.writeLog("transport TCP", "KeyError", e)
            tcpJSONFile["header"]["type"] = "none"

        if (tcpJSONFile["header"]["type"] == "http"):
            self.textHttpHeaderType.setText(
                json.dumps(tcpJSONFile["header"], indent = 4, sort_keys = False))
            self.comboxHttpHeaderType.setCurrentText("http")
        elif (tcpJSONFile["header"]["type"] == "none"):
            self.textHttpHeaderType.clear()
        else:
            ### TODO pop a error message
            pass
        
    def createtcpSettingJSONFile(self):
        tcpJSONFile = {}
        tcpJSONFile["header"] = {}
        
        if (self.comboxHttpHeaderType.currentText() == "http"):
            header = self.textHttpHeaderType.toPlainText()
            checkjsonfile = self.jsonDataValitor(header)
            if (checkjsonfile[0] == -1):
                tcpJSONFile["header"]["type"] = "none"
                return tcpJSONFile
            
            if (checkjsonfile[0] == 0):
                header = checkjsonfile[1]
                http = False
                try:
                    ### use input text maybe no value type
                    http = (header["type"] == "http")
                except KeyError:
                    ### TODO pop a error message
                    pass
                except:
                    ### TODO pop a error message
                    pass
                
                if(http):
                    tcpJSONFile["header"] = header
                else:
                    tcpJSONFile["header"]["type"] = "none"
        else:
            tcpJSONFile["header"]["type"] = "none"
            
        return tcpJSONFile
    
    def cleartcpPanel(self):
        self.groupBoxTCPSetting.setChecked(False)
        self.comboxHttpHeaderType.setCurrentIndex(0)
        self.textHttpHeaderType.clear()
    
    def __debugTest(self):
        print(json.dumps(self.createtcpSettingJSONFile(), indent=4, sort_keys = False))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TcpPanel()
    ex.createTCPSettingPanel()
    ex.setGeometry(300, 300, 680, 620)
    ex.show()
    sys.exit(app.exec_())