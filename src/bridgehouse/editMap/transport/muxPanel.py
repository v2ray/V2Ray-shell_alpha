#!/usr/bin/env python3

from PyQt5.QtWidgets import (QLabel, QWidget, QGroupBox, QHBoxLayout, QSpinBox, QPushButton)
from PyQt5.QtCore import QFileInfo, QCoreApplication
import sys

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    ### this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-4]))

from bridgehouse.editMap.transport import logbook

class muxPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.muxJSONFile = {
                            "enabled": False,
                            "concurrency": 8
                            }
        self.translate = QCoreApplication.translate
        
        self.groupBoxmuxSetting = QGroupBox(
            self.translate("muxPanel", "Mux Setting"), self)
        self.hboxConcurrency = QHBoxLayout()

    def createmuxSettingPanel(self):
        labelConcurrency = QLabel(
            self.translate("muxPanel", "Concurrency: "), self)
        self.spinBoxConcurrency = QSpinBox()
        self.spinBoxConcurrency.setRange(1, 1024)
        self.spinBoxConcurrency.setValue(8)
        
        hboxConcurrency = self.hboxConcurrency
        hboxConcurrency.addWidget(labelConcurrency)
        hboxConcurrency.addWidget(self.spinBoxConcurrency)
        hboxConcurrency.addStretch()
        
        self.groupBoxmuxSetting.setCheckable(True)
        self.groupBoxmuxSetting.setLayout(hboxConcurrency)
        
        if (v2rayshellDebug):
            from PyQt5.QtWidgets import QVBoxLayout
            self.__debugBtn = QPushButton("__debugTest", self)
            v = QVBoxLayout()
            v.addWidget(self.groupBoxmuxSetting)
            v.addWidget(self.__debugBtn)
            self.__debugBtn.clicked.connect(self.__debugTest)
            self.settingmuxPanelFromJSONFile(self.muxJSONFile, True)
            self.setLayout(v)
            return
        
        return self.groupBoxmuxSetting
    
    def settingmuxPanelFromJSONFile(self, muxJSONFile, openFromJSONFile = False):
        logbook.setisOpenJSONFile(openFromJSONFile)
        
        if (muxJSONFile == None): 
            muxJSONFile = {}
            self.groupBoxmuxSetting.setChecked(False)
            return
        
        try:
            muxJSONFile["enabled"]
        except KeyError as e:
            logbook.writeLog("mux", "KeyError", e)
            muxJSONFile["enabled"] = False
        
        try:
            muxJSONFile["concurrency"]
        except KeyError as e:
            logbook.writeLog("mux", "KeyError", e)
            muxJSONFile["concurrency"] = 8
        
        try:
            self.spinBoxConcurrency.setValue(int(muxJSONFile["concurrency"]))
        except ValueError as e:
            logbook.writeLog("mux", "ValueError", e)
            muxJSONFile["concurrency"] = 8

        self.groupBoxmuxSetting.setChecked(bool(muxJSONFile["enabled"]))

    def createmuxSettingJSONFile(self):
        muxJSONFile = {}
        muxJSONFile["enabled"]     = self.groupBoxmuxSetting.isChecked()
        muxJSONFile["concurrency"] = self.spinBoxConcurrency.value()
        
        return muxJSONFile
    
    def clearmuxPanel(self):
        self.groupBoxmuxSetting.setChecked(False)
        self.spinBoxConcurrency.setValue(8)
    
    def __debugTest(self):
        import json
        print(json.dumps(self.createmuxSettingJSONFile(), indent=4, sort_keys = False))

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = muxPanel()
    ex.createmuxSettingPanel()
    ex.setGeometry(300, 300, 680, 230)
    ex.show()
    sys.exit(app.exec_())
