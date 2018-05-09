#!/usr/bin/env python3

from PyQt5.QtWidgets import (QLabel, QWidget, QGroupBox,
                             QLineEdit, QGridLayout, QPushButton)
from PyQt5.QtCore import QFileInfo, QCoreApplication
import sys, re

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    # this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-4]))

from bridgehouse.editMap.transport import logbook


class http2Panel(QWidget):
    def __init__(self):
        super(http2Panel, self).__init__()
        self.httpJSONFile = {
                "host": ["v2ray.com"],
                "path": "/random/path"
        }
        self.translate = QCoreApplication.translate

    def createHttpSettingPanel(self):
        labelHost = QLabel(self.translate("http2Panel", "Host: "), self)
        self.lineEditHost = QLineEdit()
        
        labelPath = QLabel(self.translate("http2Panel", "Path: "), self)
        self.lineEditPath = QLineEdit()
        
        grid = QGridLayout(self)
        grid.addWidget(labelHost,0, 0)
        grid.addWidget(self.lineEditHost, 0, 1)
        grid.addWidget(labelPath, 1, 0)
        grid.addWidget(self.lineEditPath, 1, 1)
        
        self.groupBoxhttp = box = QGroupBox(self.translate("http2Panel", "http Settings "), self)
        box.setCheckable(True)
        box.setChecked(False)
        box.setLayout(grid)
        
        if (v2rayshellDebug):
            self.__debugBtn = QPushButton("__debugTest", self)
            self.__debugBtn.clicked.connect(self.__debugTest)
            grid.addWidget(self.__debugBtn, 2, 0)
            self.settingHttpPanelFromJSONFile(self.httpJSONFile, True)
        
        return box
    
    def settingHttpPanelFromJSONFile(self, httpJSONFile, openFromJSONFile=False):
        logbook.setisOpenJSONFile(openFromJSONFile)

        if (not httpJSONFile):
            self.lineEditHost.clear()
            self.lineEditPath.clear()
            self.groupBoxhttp.setChecked(False)
            del httpJSONFile
            return False
        
        try:
            httpJSONFile["host"]
        except Exception:
            httpJSONFile["host"] = []
            
        try:
            httpJSONFile["path"]
        except Exception:
            httpJSONFile["path"] = ""
            
        
        if (httpJSONFile["host"]):
            self.lineEditHost.setText(", ".join([str(x) for x in httpJSONFile["host"]]))
        
        if (httpJSONFile["path"]):
            self.lineEditPath.setText(httpJSONFile["path"])
    
    def createHttpSettingJSONFile(self):
        httpJSONFile = {}
        httpJSONFile["host"] = [x.strip() for x in re.split(r"[,;]", self.lineEditHost.text())]
        httpJSONFile["path"] = self.lineEditPath.text()
        
        return httpJSONFile
    
    def clearHttpPanel(self):
        self.lineEditHost.clear()
        self.lineEditPath.clear()
        self.groupBoxhttp.setChecked(False)

    def __debugTest(self):
        import json
        print(json.dumps(self.createHttpSettingJSONFile(), indent=4, sort_keys=False))
    
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = http2Panel()
    ex.createHttpSettingPanel()
    ex.setGeometry(300, 300, 680, 230)
    ex.show()
    sys.exit(app.exec_())
