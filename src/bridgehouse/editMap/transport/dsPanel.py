#!/usr/bin/env python3

from PyQt5.QtWidgets import (QLabel, QWidget, QGroupBox,
                             QLineEdit, QHBoxLayout, QVBoxLayout,
                             QPushButton)
from PyQt5.QtCore import QFileInfo, QCoreApplication
import sys

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    # this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-4]))
    
class domainSocketPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.domainSocketJSONFile = {
                            "path": "/path/to/ds/file"
                        }
        self.translate = QCoreApplication.translate

    def createdsSettingPanel(self):
        labelPath = QLabel(self.translate("domainSocketPanel", 'Path:'), self)
        self.lineEditPath = QLineEdit(self)
        
        vbox = QVBoxLayout()
        vbox.addWidget(labelPath)
        vbox.addWidget(self.lineEditPath)
        
        self.groupBoxdsSetting = groupBoxdsSetting = QGroupBox(
            self.translate("domainSocketPanel", "Domain Socket Setting"), self)
        groupBoxdsSetting.setCheckable(True)
        groupBoxdsSetting.setChecked(False)
        groupBoxdsSetting.setLayout(vbox)
        
        if (v2rayshellDebug):
            self.__debugBtn = QPushButton("__debugTest", self)
            self.__debugBtn.clicked.connect(self.__debugTest)
            vbox.addWidget(self.__debugBtn)

        return groupBoxdsSetting
        
    def settingdsPanelFromJSONFile(self, dsJSONFile, openFromJSONFile=False):
        
        if not dsJSONFile:
            dsJSONFile = {}
            self.cleardsPanel()
        
        try:
            dsJSONFile['path']
        except KeyError:
            dsJSONFile['path'] = ''
            
        self.lineEditPath.setText(str(dsJSONFile['path']))
    
    def createdsSettingJSONFile(self):
        dsJSONFile = {}
        dsJSONFile['path'] = self.lineEditPath.text()
        
        return dsJSONFile
    
    def cleardsPanel(self):
        self.groupBoxdsSetting.setChecked(False)
        self.lineEditPath.clear()
    
    def __debugTest(self):
        import json
        print(json.dumps(self.createdsSettingJSONFile(), indent=4, sort_keys=False))

    
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = domainSocketPanel()
    ex.createdsSettingPanel()
    ex.setGeometry(300, 300, 680, 230)
    ex.show()
    sys.exit(app.exec_())
