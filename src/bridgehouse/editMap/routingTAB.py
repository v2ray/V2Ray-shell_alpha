#!/usr/bin/env python3

from PyQt5.QtWidgets import (QWidget, QTextEdit,
                             QVBoxLayout, QApplication)
from PyQt5.QtCore import QFileInfo, QCoreApplication
import sys, json, copy

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    ### this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-3]))

class routingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.routingJSONFile = {
                                "strategy": "rules",
                                "settings": {
                                    "domainStrategy": "IPIfNonMatch",
                                    "rules": [
                                        {
                                        "type": "field",
                                        "port": "1-52",
                                        "outboundTag": "direct"
                                        },
                                        {
                                        "type": "field",
                                        "port": "54-79",
                                        "outboundTag": "direct"
                                        },
                                        {
                                        "type": "field",
                                        "port": "81-442",
                                        "outboundTag": "direct"
                                        },
                                        {
                                        "type": "field",
                                        "port": "444-65535",
                                        "outboundTag": "direct"
                                        },
                                        {
                                        "type": "chinasites",
                                        "outboundTag": "direct"
                                        },
                                        {
                                          "type": "field",
                                          "ip": [
                                            "0.0.0.0/8",
                                            "10.0.0.0/8",
                                            "100.64.0.0/10",
                                            "127.0.0.0/8",
                                            "169.254.0.0/16",
                                            "172.16.0.0/12",
                                            "192.0.0.0/24",
                                            "192.0.2.0/24",
                                            "192.168.0.0/16",
                                            "198.18.0.0/15",
                                            "198.51.100.0/24",
                                            "203.0.113.0/24",
                                            "::1/128",
                                            "fc00::/7",
                                            "fe80::/10"
                                          ],
                                          "outboundTag": "direct"
                                        },
                                        {
                                          "type": "chinaip",
                                          "outboundTag": "direct"
                                        }
                                      ]
                                    }
                                }
        self.translate = QCoreApplication.translate
    
    def createRoutingTab(self):
        self.textEditRoutingJSONFile = QTextEdit()
        self.textEditRoutingJSONFile.setReadOnly(True)
        
        self.textEditRoutingJSONFile.setPlainText(
            json.dumps(self.routingJSONFile, indent = 4, sort_keys = False))

        return self.textEditRoutingJSONFile
    
    def settingRoutingTABFromJSONFile(self, routingJSONFile = {}, openFromJSONFile = False):
        
        if (routingJSONFile == None): routingJSONFile = self.routingJSONFile
        
        if (openFromJSONFile and routingJSONFile != {} or routingJSONFile != None):
            self.textEditRoutingJSONFile.clear()
            try:
                self.textEditRoutingJSONFile.setText(
                    json.dumps(routingJSONFile, indent = 4, sort_keys = False))
            except Exception:
                pass
        elif (openFromJSONFile == False):
            ### use default settings
            self.textEditRoutingJSONFile.setText(
                json.dumps(self.routingJSONFile, indent = 4, sort_keys = False))
    
    def createRoutingJSONFile(self):
        try:
            routingJSONFile = copy.deepcopy(
                json.loads(self.textEditRoutingJSONFile.toPlainText()))
        except Exception:
            routingJSONFile = {}
        
        return routingJSONFile

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = routingTab()
    v = QVBoxLayout()
    v.addWidget(ex.createRoutingTab())
    ex.setLayout(v)
    ex.setGeometry(200, 100, 800, 768)
    ex.show()
    sys.exit(app.exec_())
