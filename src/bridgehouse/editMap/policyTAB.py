#!/usr/bin/env python3

from PyQt5.QtWidgets import (QWidget, QGroupBox,
                             QVBoxLayout, QApplication, QLabel, QComboBox,
                             QHBoxLayout, QSpinBox, QGridLayout, QPushButton)
from PyQt5.QtCore import QFileInfo, Qt, QCoreApplication
import sys, copy

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    ### this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-3]))

from bridgehouse.editMap.port import treasureChest

class policyTab(QWidget):
    def __init__(self, CaptainstreasureChest = False):
        super().__init__()
        self.policyJSONFile = {
                                "levels": {
                                    "0": {
                                        "handshake": 4,
                                        "connIdle": 300,
                                        "uplinkOnly": 5,
                                        "downlinkOnly": 30
                                        }
                                    }
                               }
        
        self.template = {
                   "handshake": 4,
                   "connIdle": 300,
                   "uplinkOnly": 5,
                   "downlinkOnly": 30
                }
        self.translate = QCoreApplication.translate
        if (CaptainstreasureChest):
            self.treasureChest = CaptainstreasureChest
        else:
            self.treasureChest = treasureChest.treasureChest()  ### a empty treasure chest
        self.__groupPolicyTitle = self.translate("policyTab", "Policy Setting")
        self.levels = {}
        
    def createPolicyTab(self):
        labelLevels = QLabel(self.translate("policyTab", "Levels: "))
        self.comboBoxLevels = QComboBox()
        
        hboxLevels = QHBoxLayout()
        hboxLevels.addWidget(labelLevels)
        hboxLevels.addWidget(self.comboBoxLevels)
        hboxLevels.addStretch()
        
        labelhandshake      = QLabel(
            self.translate("policyTab", "Handshake: "))
        labelconnIdle       = QLabel(
            self.translate("policyTab", "ConnIdle: "))
        labeluplinkOnly     = QLabel(
            self.translate("policyTab", "UplinkOnly: "))
        labeldownlinkOnly   = QLabel(
            self.translate("policyTab", "DownlinkOnly: "))
        self.spinboxhandshake    = QSpinBox()
        self.spinboxuplinkOnly   = QSpinBox()
        self.spinboxconnIdle     = QSpinBox()
        self.spinboxdownlinkOnly = QSpinBox()
        self.spinboxhandshake.setRange(0, 20)
        self.spinboxhandshake.setValue(4)
        self.spinboxconnIdle.setRange(0, 1500)
        self.spinboxconnIdle.setValue(300)
        self.spinboxuplinkOnly.setRange(0, 25)
        self.spinboxuplinkOnly.setValue(5)
        self.spinboxdownlinkOnly.setRange(0, 150)
        self.spinboxdownlinkOnly.setValue(30)
        
        hboxhandshake = QHBoxLayout()
        hboxhandshake.addWidget(self.spinboxhandshake)
        hboxhandshake.addStretch()
        
        self.buttonPolicyApply   = QPushButton(
            self.translate("policyTab", "Apply"), self)
        self.buttonPolicyDefault = QPushButton(
            self.translate("policyTab", "Default"), self)
        hboxButton = QHBoxLayout()
        hboxButton.addStretch()
        hboxButton.addWidget(self.buttonPolicyApply)
        hboxButton.addWidget(self.buttonPolicyDefault)
            
        gridBoxLevel = QGridLayout()
        gridBoxLevel.addWidget(labelhandshake, 0, 0, 1, 1, Qt.AlignLeft)
        gridBoxLevel.addLayout(hboxhandshake, 0, 1, 1, 1, Qt.AlignLeft)
        gridBoxLevel.addWidget(labelconnIdle, 1, 0, 1, 1, Qt.AlignLeft)
        gridBoxLevel.addWidget(self.spinboxconnIdle, 1, 1, 1, 1, Qt.AlignLeft)
        gridBoxLevel.addWidget(labeluplinkOnly, 2, 0, 1, 1, Qt.AlignLeft)
        gridBoxLevel.addWidget(self.spinboxuplinkOnly, 2, 1, 1, 1, Qt.AlignLeft)
        gridBoxLevel.addWidget(labeldownlinkOnly, 3, 0, 1, 1, Qt.AlignLeft)
        gridBoxLevel.addWidget(self.spinboxdownlinkOnly, 3, 1, 1, 1, Qt.AlignLeft)
        gridBoxLevel.addLayout(hboxButton, 4, 2, 1, 2, Qt.AlignLeft)
        
        vboxLevels = QVBoxLayout()
        vboxLevels.addLayout(hboxLevels)
        vboxLevels.addLayout(gridBoxLevel)
        vboxLevels.addStretch()
        
        self.groupBoxPolicy = QGroupBox(self.__groupPolicyTitle, self)
        self.groupBoxPolicy.setLayout(vboxLevels)
        
        self.createPolcyTabSignals()

        if v2rayshellDebug:
            levels = ("0","1","2","3","4","5","6")
            self.comboBoxLevels.addItems(levels)
            self.__debugBtn = QPushButton("__debugTest", self)
            self.__debugBtn.clicked.connect(self.__debugTest)
            vboxLevels.addWidget(self.__debugBtn)
            return self.groupBoxPolicy

        return self.groupBoxPolicy
        
    def createPolcyTabSignals(self):
        self.treasureChest.updateList.updateLevelandEmail.connect(self.onupdatecomboBoxLevels)
        self.comboBoxLevels.activated[str].connect(self.settingLevelsSpinbox)
        self.buttonPolicyApply.clicked.connect(self.onbuttonPolicyApply)
        self.buttonPolicyDefault.clicked.connect(self.settingLevelsSpinboxDefault)
        self.spinboxconnIdle.valueChanged.connect(self.changegroupBoxPolicyTitle)
        self.spinboxdownlinkOnly.valueChanged.connect(self.changegroupBoxPolicyTitle)
        self.spinboxhandshake.valueChanged.connect(self.changegroupBoxPolicyTitle)
        self.spinboxuplinkOnly.valueChanged.connect(self.changegroupBoxPolicyTitle)
        
    def settingLevelsSpinbox(self, level):
        if level in self.levels.keys():
            self.spinboxhandshake.setValue(self.levels[level]["handshake"])
            self.spinboxconnIdle.setValue(self.levels[level]["connIdle"])
            self.spinboxdownlinkOnly.setValue(self.levels[level]["downlinkOnly"])
            self.spinboxuplinkOnly.setValue(self.levels[level]["uplinkOnly"])
            self.groupBoxPolicy.setTitle("{}".format(self.__groupPolicyTitle))
        else:
            self.settingLevelsSpinboxDefault()
            
    def onbuttonPolicyApply(self):
        currentLevel = self.comboBoxLevels.currentText()
        if currentLevel not in self.levels: self.levels[currentLevel] = {}
        self.levels[currentLevel]["handshake"]    = self.spinboxhandshake.value()
        self.levels[currentLevel]["connIdle"]     = self.spinboxconnIdle.value()
        self.levels[currentLevel]["downlinkOnly"] = self.spinboxdownlinkOnly.value()
        self.levels[currentLevel]["uplinkOnly"]   = self.spinboxuplinkOnly.value()
        self.groupBoxPolicy.setTitle("{}".format(self.__groupPolicyTitle))

    def settingLevelsSpinboxDefault(self):
        self.spinboxhandshake.setValue(self.template["handshake"])
        self.spinboxconnIdle.setValue(self.template["connIdle"])
        self.spinboxdownlinkOnly.setValue(self.template["downlinkOnly"])
        self.spinboxuplinkOnly.setValue(self.template["uplinkOnly"])
        self.onbuttonPolicyApply()

    def changegroupBoxPolicyTitle(self):
        self.groupBoxPolicy.setTitle("{}{}".format(self.__groupPolicyTitle, "*"))
    
    def onupdatecomboBoxLevels(self):
        self.comboBoxLevels.clear()
        allLevels = copy.deepcopy(self.treasureChest.getLevels())

        if allLevels:
            ### add new Levels
            for i in allLevels:  
                if i not in self.levels.keys():
                    self.levels[i] = copy.deepcopy(self.template)
            
            ### delete obsolete Levels
            for i in self.levels.keys():
                if i not in allLevels:
                    del self.levels[i]
                    continue
                self.comboBoxLevels.addItem(i)

    def settingPolicyTabFromJSONFile(self, policyJSONFile):
        self.levels.clear()
        self.comboBoxLevels.clear()

        if (policyJSONFile == None): policyJSONFile = {}
        
        for i,v in policyJSONFile.items():
            try:
                int(i)
            except Exception:
                continue
            
            try:
                v["handshake"]
            except Exception:
                v["handshake"] = 4
            
            try:
                v["connIdle"]
            except Exception:
                v["connIdle"] = 300
            
            try:
                v["uplinkOnly"]
            except Exception:
                v["uplinkOnly"] = 5
                
            try:
                v["downlinkOnly"]
            except Exception:
                v["downlinkOnly"] = 30
                
            try:
                self.levels[str(i)] = copy.deepcopy(v)
            except Exception:
                pass
            self.comboBoxLevels.addItem(str(i))
            
        if len(self.levels) > 0:
            for i in self.levels.items():
                try:
                    self.settingLevelsSpinbox(i[0])
                except Exception:
                    pass
                break

    def createPolicyJSONFile(self):
        return self.levels
    
    def __debugTest(self):
        import json
        print(json.dumps(self.createPolicyJSONFile(), indent = 4, sort_keys = False))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = policyTab()
    vbox = QVBoxLayout()
    vbox.addWidget(ex.createPolicyTab())
    ex.setLayout(vbox)
    ex.setGeometry(200, 100, 250, 200)
    ex.show()
    sys.exit(app.exec_())