#!/usr/bin/env python3

from PyQt5.QtWidgets import (QApplication, QPushButton, QVBoxLayout)
from PyQt5.QtCore import QFileInfo, QCoreApplication
import sys, json

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    # this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-3]))
        
from bridgehouse.editMap.transport import transportPanel


class transportTab(transportPanel.TransportPanel):

    def __init__(self):
        super().__init__()
        self.translate = QCoreApplication.translate

    def createTransportPanel(self):
        super(transportTab, self).createTransportPanel()

        if v2rayshellDebug:
            self.setLayout(self.vboxcheckBoxStreamSetting)
            self.__debugBtn = QPushButton("__debugTest", self)
            self.vboxTransportPanel.addWidget(self.__debugBtn)
            self.__debugBtn.clicked.connect(self.__debugTest)
            self.settingtransportPanelFromJSONFile(self.transportJSONFile, True)
        
        self.groupTransportPanel.setTitle(self.translate("transportTab", "Transport Setting (Global)"))
        self.groupTransportPanel.setCheckable(True)
        self.groupTransportPanel.setChecked(False)
        
        return self.groupTransportPanel
        
    def __debugTest(self):
        print(json.dumps(self.createtransportSettingJSONFile(), indent=4, sort_keys=False))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = transportTab()
    v = QVBoxLayout()
    v.addWidget(ex.createTransportPanel())
    ex.setLayout(v)
    ex.setGeometry(200, 100, 800, 768)
    ex.show()
    sys.exit(app.exec_())
