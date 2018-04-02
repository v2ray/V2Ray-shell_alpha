#!/usr/bin/env python3

from PyQt5.QtWidgets import (QLabel, QSpinBox, QComboBox, QCheckBox, QWidget,
                             QGridLayout, QGroupBox, QPushButton)
from PyQt5.QtCore import QFileInfo, QCoreApplication

v2rayshellDebug = False
import sys

if __name__ == "__main__":
    v2rayshellDebug = True
    # this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-4]))

from bridgehouse.editMap.transport import logbook


class mKcpPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.mKcpJSONFile = {
                            "mtu": 1355,
                            "tti": 50,
                            "uplinkCapacity": 5,
                            "downlinkCapacity": 20,
                            "congestion": False,
                            "readBufferSize": 2,
                            "writeBufferSize": 2,
                            "header": {
                                "type": "none"
                                }
                             }
        self.translate = QCoreApplication.translate
        self.headerTypes = ("none", "srtp", "uTP", "wechat-video")
                    
    def createmKcpSettingPanel(self):       
        labelMTU = QLabel(
            self.translate("mKcpPanel", "MTU: "), self)
        self.spinBoxmKcpMTU = QSpinBox()
        labelTTI = QLabel(
            self.translate("mKcpPanel", "TTI: "), self)
        self.spinBoxmKcpTTI = QSpinBox()
        labelUplinkCapacity = QLabel(
            self.translate("mKcpPanel", "Uplink Capacity: "), self)
        self.spinBoxUpCapacity = QSpinBox()
        labelDownlinckCapacity = QLabel(
            self.translate("mKcpPanel", "Downlink Capacity: "), self)
        self.spinBoxDownCapacity = QSpinBox()
        labelReadBufferSize = QLabel(
            self.translate("mKcpPanel", "Read Buffer Size: "), self)
        self.spinBoxRdBufferSize = QSpinBox()
        labelWriteBufferSize = QLabel(
            self.translate("mKcpPanel", "Write Buffer Size: "), self)
        self.spinBoxWrBufferSize = QSpinBox()
        self.checkBoxCongestion = QCheckBox(
            self.translate("mKcpPanel", "Congestion"), self)
        labelHeaderType = QLabel(
            self.translate("mKcpPanel", "Header Type: "), self)
        self.comboBoxHeader = QComboBox()
        
        self.spinBoxmKcpMTU.setRange(576, 1460)
        self.spinBoxmKcpMTU.setValue(1335)
        self.spinBoxmKcpTTI.setRange(10, 100)
        self.spinBoxmKcpTTI.setValue(50)
        self.spinBoxUpCapacity.setRange(0, 9212500)  # Francesco Poletti 73.7 Tb/s
        self.spinBoxUpCapacity.setValue(5)
        self.spinBoxDownCapacity.setRange(0, 9212500)
        self.spinBoxDownCapacity.setValue(20)
        self.spinBoxRdBufferSize.setRange(0, 230584301)  # 2.30584301 * 10^12 (2^64 bit)
        self.spinBoxRdBufferSize.setValue(2)
        self.spinBoxWrBufferSize.setRange(0, 230584301)
        self.spinBoxWrBufferSize.setValue(2)
        self.comboBoxHeader.addItems(self.headerTypes)

        gridBoxmKCP = QGridLayout(self)
        gridBoxmKCP.addWidget(labelMTU, 0, 0)
        gridBoxmKCP.addWidget(self.spinBoxmKcpMTU, 0, 1)
        gridBoxmKCP.addWidget(labelTTI, 0, 2)
        gridBoxmKCP.addWidget(self.spinBoxmKcpTTI, 0, 3)
        
        gridBoxmKCP.addWidget(labelUplinkCapacity, 1, 0)
        gridBoxmKCP.addWidget(self.spinBoxUpCapacity, 1, 1)
        gridBoxmKCP.addWidget(labelDownlinckCapacity, 1, 2)
        gridBoxmKCP.addWidget(self.spinBoxDownCapacity, 1, 3)
        
        gridBoxmKCP.addWidget(labelReadBufferSize, 2, 0)
        gridBoxmKCP.addWidget(self.spinBoxRdBufferSize, 2, 1)
        gridBoxmKCP.addWidget(labelWriteBufferSize, 2, 2)
        gridBoxmKCP.addWidget(self.spinBoxWrBufferSize, 2, 3)
        gridBoxmKCP.addWidget(self.checkBoxCongestion, 3, 0)
        gridBoxmKCP.addWidget(labelHeaderType, 4, 0)
        gridBoxmKCP.addWidget(self.comboBoxHeader, 4, 1)
        
        self.groupBoxmKCPSetting = groupBoxmKCPSetting = QGroupBox(
            self.translate("mKcpPanel", "mKcp Setting"), self)
        groupBoxmKCPSetting.setCheckable(True)
        groupBoxmKCPSetting.setChecked(False)
        groupBoxmKCPSetting.adjustSize()
        groupBoxmKCPSetting.setLayout(gridBoxmKCP)
        
        if (v2rayshellDebug):
            self.__debugBtn = QPushButton("__debugTest", self)
            gridBoxmKCP.addWidget(self.__debugBtn, 5, 0)
            self.__debugBtn.clicked.connect(self.__debugTest)
            self.settingmKcpPanelFromJSONFile(self.mKcpJSONFile, True)

        return groupBoxmKCPSetting
    
    def settingmKcpPanelFromJSONFile(self, mKcpJSONFile, openFromJSONFile=False):
        logbook.setisOpenJSONFile(openFromJSONFile)
        
        if (not mKcpJSONFile): 
            mKcpJSONFile = {}
            self.groupBoxmKCPSetting.setChecked(False)
            return False

        try:
            mKcpJSONFile["mtu"]
        except KeyError as e:
            logbook.writeLog("mKcp", "KeyError", e)
            mKcpJSONFile["mtu"] = 1355

        try:
            mKcpJSONFile["tti"]
        except KeyError as e:
            logbook.writeLog("mKcp", "KeyError", e)
            mKcpJSONFile["tti"] = 50
        
        try:
            mKcpJSONFile["uplinkCapacity"]
        except KeyError as e:
            logbook.writeLog("mKcp", "KeyError", e)
            mKcpJSONFile["uplinkCapacity"] = 5
        
        try:
            mKcpJSONFile["downlinkCapacity"]
        except KeyError as e:
            logbook.writeLog("mKcp", "KeyError", e)
            mKcpJSONFile["downlinkCapacity"] = 20
            
        try:
            mKcpJSONFile["congestion"]
        except KeyError as e:
            logbook.writeLog("mKcp", "KeyError", e)
            mKcpJSONFile["congestion"] = False
        
        try:
            mKcpJSONFile["readBufferSize"]
        except KeyError as e:
            logbook.writeLog("mKcp", "KeyError", e)
            mKcpJSONFile["readBufferSize"] = 2
        
        try:
            mKcpJSONFile["writeBufferSize"]
        except KeyError as e:
            logbook.writeLog("mKcp", "KeyError", e)
            mKcpJSONFile["writeBufferSize"] = 2
        
        try:
            mKcpJSONFile["header"]
        except KeyError as e:
            logbook.writeLog("mKcp", "KeyError", e)
            mKcpJSONFile["header"] = {}
        
        try:
            mKcpJSONFile["header"]["type"]
        except KeyError as e:
            logbook.writeLog("mKcp", "KeyError", e)
            mKcpJSONFile["header"]["type"] = "none"
            
        try:
            self.spinBoxmKcpMTU.setValue(int(mKcpJSONFile["mtu"]))
        except ValueError as e:
            logbook.writeLog("mKcp", "ValueError", e)
            mKcpJSONFile["mtu"] = 1355
        
        try:
            self.spinBoxmKcpTTI.setValue(int(mKcpJSONFile["tti"]))
        except ValueError as e:
            logbook.writeLog("mKcp", "ValueError", e)
            mKcpJSONFile["tti"] = 50
        
        try:
            self.spinBoxUpCapacity.setValue(int(mKcpJSONFile["uplinkCapacity"]))
        except ValueError as e:
            logbook.writeLog("mKcp", "ValueError", e)
            mKcpJSONFile["uplinkCapacity"] = 5
        
        try:
            self.spinBoxDownCapacity.setValue(int(mKcpJSONFile["downlinkCapacity"]))
        except ValueError as e:
            logbook.writeLog("mKcp", "ValueError", e)
            mKcpJSONFile["downlinkCapacity"] = 20
        
        try:
            self.checkBoxCongestion.setChecked(mKcpJSONFile["congestion"])
        except ValueError as e:
            logbook.writeLog("mKcp", "ValueError", e)
            mKcpJSONFile["congestion"] = False
        
        try:
            self.spinBoxRdBufferSize.setValue(int(mKcpJSONFile["readBufferSize"]))
        except ValueError as e:
            logbook.writeLog("mKcp", "ValueError", e)
            mKcpJSONFile["readBufferSize"] = 2
        
        try:
            self.spinBoxWrBufferSize.setValue(int(mKcpJSONFile["writeBufferSize"]))
        except ValueError as e:
            logbook.writeLog("mKcp", "ValueError", e)
            mKcpJSONFile["writeBufferSize"] = 2

        try:
            self.comboBoxHeader.setCurrentText(mKcpJSONFile["header"]["type"])
        except ValueError as e:
            logbook.writeLog("mKcp", "ValueError", e)
        except TypeError as e:
            logbook.writeLog("mKcp", "TypeError", e)
        except:
            logbook.writeLog("mKcp", "unkonw Error")
        
    def createmKcpSettingJSONFile(self):
        mKcpJSONFile = {}
        
        mKcpJSONFile["mtu"] = self.spinBoxmKcpMTU.value()
        mKcpJSONFile["tti"] = self.spinBoxmKcpTTI.value()
        mKcpJSONFile["uplinkCapacity"] = self.spinBoxUpCapacity.value()
        mKcpJSONFile["downlinkCapacity"] = self.spinBoxDownCapacity.value()
        mKcpJSONFile["congestion"] = self.checkBoxCongestion.isChecked()
        mKcpJSONFile["readBufferSize"] = self.spinBoxRdBufferSize.value()
        mKcpJSONFile["writeBufferSize"] = self.spinBoxWrBufferSize.value()
        mKcpJSONFile["header"] = {}
        mKcpJSONFile["header"]["type"] = self.comboBoxHeader.currentText()
            
        return mKcpJSONFile
    
    def clearmkcpPanel(self):
        self.groupBoxmKCPSetting.setChecked(False)
        self.spinBoxmKcpMTU.setValue(1355)
        self.spinBoxmKcpTTI.setValue(50)
        self.spinBoxUpCapacity.setValue(5)
        self.spinBoxDownCapacity.setValue(20)
        self.checkBoxCongestion.setChecked(False)
        self.spinBoxRdBufferSize.setValue(2)
        self.spinBoxWrBufferSize.setValue(2)
        self.comboBoxHeader.setCurrentIndex(0)
    
    def __debugTest(self):
        import json
        print(json.dumps(self.createmKcpSettingJSONFile(), indent=4, sort_keys=False))

        
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = mKcpPanel()
    ex.createmKcpSettingPanel()
    ex.setGeometry(300, 300, 680, 230)
    ex.show()
    sys.exit(app.exec_())
