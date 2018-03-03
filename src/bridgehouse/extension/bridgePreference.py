#!/usr/bin/env python3

from PyQt5.QtWidgets import (QDialog, QApplication, QPushButton, QGridLayout,
                             QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, 
                             QFileDialog, QGroupBox, QRadioButton, QSpinBox,
                             QComboBox, QCheckBox, QToolTip)
from PyQt5.QtCore import (QSize, QFileInfo, Qt, QCoreApplication,
                          QProcess, QIODevice, QProcessEnvironment,
                          qDebug, QDir, QFile)
from PyQt5.QtGui import QCursor

import sys
import codecs

CRONTAB = True
try:
    import crontab
except ImportError:
    CRONTAB = None

is_win = sys.platform.startswith('win')

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    ### this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-3]))
    
class startUp():
    def __init__(self, striptName=False, enableStartup=False):
        self.enableStartup = enableStartup
        self.timesForTrySetcrontab = False
        self.striptName = sys.argv[0]
        if striptName:
            self.striptName = striptName

        self.scriptAbsoluteFilePath = QFileInfo(self.striptName).absoluteFilePath()

        self.QProcessCreateStartUp = QProcess()
        self.QProcessCreateStartUp.setProcessChannelMode(QProcess.MergedChannels)
        self.QProcessCreateStartUp.setProcessEnvironment(
            QProcessEnvironment.systemEnvironment())

        self.QProcessCreateStartUp.readyRead.connect(self.parseOut)
        
        self.crontab = crontab.CronTab(user=True)
        self.commentorTaskName = "V2Ray-shell"

    def getWorkPath(self):
        if (not is_win):
            if (self.scriptAbsoluteFilePath.endswith(".pyw") or self.scriptAbsoluteFilePath.endswith(".py")):
                return "python3 {}".format(self.scriptAbsoluteFilePath)
            else:
                return self.scriptAbsoluteFilePath
        else:
            if (self.scriptAbsoluteFilePath.endswith(".exe")):
                return self.scriptAbsoluteFilePath
            else:
                return """/tr "pythonw '{}'" """.format(self.scriptAbsoluteFilePath)

    def setStartUp(self, enable=False):
        if (not isinstance(enable, bool)):
            enable = False

        if (not is_win):
            if not enable:
                self.crontab.remove_all(comment=self.commentorTaskName)
                self.crontab.write_to_user()
                return True

            hasjob = False
            for i in self.crontab.find_comment(self.commentorTaskName):
                if str(i).endswith(self.commentorTaskName):
                    hasjob = True
            if not hasjob:
                job = self.crontab.new(command=self.getWorkPath())
                job.set_comment(self.commentorTaskName)
                job.every_reboot()
                job.enable(enable)
                self.crontab.write_to_user()
                return True
            else:
                return False
        else:
            # windows
            pass
    
    def createVBScript(self):
        pass

    def parseOut(self):

        pass
            
class bridgepreferencesPanel(QDialog):
    def __init__(self, bridgetreasureChest = False):
        super().__init__()

        self.__preferencesJSONFile = {
    				                "v2ray-core": "x.xx",
    				                "v2ray-coreFilePath": "v2ray",
                                    "connection":{
                                        "enable": True,
                                        "connect": "switch", ### reconnect/switch
                                        "interval": 60,      ### seconds
                                        "timeout" : 3,
                                        "trytimes": 3
                                    }
                                }
        self.bridgetreasureChest = bridgetreasureChest
        if not bridgetreasureChest:
            from bridgehouse.extension import bridgetreasureChest
            self.bridgetreasureChest = bridgetreasureChest.bridgetreasureChest()
        self.translate = QCoreApplication.translate
        self.AllLanguage = self.bridgetreasureChest.getAllLanguage()
        self.starup = startUp()
        
    def createpreferencesPanel(self):
        self.labelV2raycoreVersion   = QLabel(
            self.translate("bridgepreferencesPanel", "v2ray core version is: "))
        self.labelv2raycorecurrentVersion = QLabel() 
        self.labelV2raycoreFilePath  = QLabel(
            self.translate("bridgepreferencesPanel","v2ray core File Path: "))
        self.lineEditFilePath        = QLineEdit()
        self.buttonOpenV2raycoreFile = QPushButton(
            self.translate("bridgepreferencesPanel", "Open"))
        
        self.buttonpreferenceApply   = QPushButton(
            self.translate("bridgepreferencesPanel", "Apply and Close"))
        self.buttonpreferenceCancel  = QPushButton(
            self.translate("bridgepreferencesPanel", "Cancel"))
        hboxbutton = QHBoxLayout()
        hboxbutton.addStretch()
        hboxbutton.addWidget(self.buttonpreferenceApply)
        hboxbutton.addWidget(self.buttonpreferenceCancel)
        
        gridBox = QGridLayout()
        gridBox.addWidget(self.labelV2raycoreVersion, 0, 0, 1, 1)
        gridBox.addWidget(self.labelv2raycorecurrentVersion, 0, 1, 1, 1)
        gridBox.addWidget(self.labelV2raycoreFilePath, 1, 0, 1, 1)
        gridBox.addWidget(self.lineEditFilePath, 2, 0, 1, 5)
        gridBox.addWidget(self.buttonOpenV2raycoreFile, 2, 5, 1, 1)
        
        self.grouBoxConnection = QGroupBox(
            self.translate("bridgepreferencesPanel", "Configure Connection settings."), self)
        self.grouBoxConnection.setCheckable(True)
        self.grouBoxConnection.setChecked(False)
        
        self.radioButtonSwitch = QRadioButton(
            self.translate("bridgepreferencesPanel", "Switch to the next server"))
        self.radioButtonSwitch.setChecked(True)
        self.radioButtonReconnect = QRadioButton(
            self.translate("bridgepreferencesPanel", "Reconnect the server"))
        hboxRadioButton = QHBoxLayout()
        hboxRadioButton.addWidget(self.radioButtonSwitch)
        hboxRadioButton.addWidget(self.radioButtonReconnect)
        hboxRadioButton.addStretch()
        
        labelInterval = QLabel(
            self.translate("bridgepreferencesPanel", "Check the Interval: "))
        self.spinBoxInterval = QSpinBox()
        self.spinBoxInterval.setRange(60, 360)
        self.spinBoxInterval.setValue(60)
        labelMinandMaxInterval = QLabel(
            self.translate("bridgepreferencesPanel", "Interval time value is 60 to 360"))

        labelCheckProxyTimeout = QLabel(
            self.translate("bridgepreferencesPanel", "Check Proxy Timeout: "))
        self.spinBoxCheckProxyTimeout = QSpinBox()
        self.spinBoxCheckProxyTimeout.setRange(0, 15)
        self.spinBoxCheckProxyTimeout.setValue(3)
        labelCheckProxyTimeoutWarning = QLabel(
            self.translate("bridgepreferencesPanel", "Set 0 to disable timeout."))
    
        labeltrytimes = QLabel(
            self.translate("bridgepreferencesPanel", "Try Times: "))
        self.spinboxTrytimes = QSpinBox()
        self.spinboxTrytimes.setRange(0, 12)
        self.spinboxTrytimes.setValue(3)
        labelMaxtrytimes = QLabel(
            self.translate(
                "bridgepreferencesPanel",
                "0 means immediately connect, \nthe maximum value of try times is 12"))
        
        gridBoxConnection = QGridLayout()
        gridBoxConnection.addWidget(labelInterval, 0, 0, Qt.AlignLeft)
        gridBoxConnection.addWidget(self.spinBoxInterval, 0, 1, Qt.AlignLeft)
        gridBoxConnection.addWidget(labelMinandMaxInterval, 0, 2, Qt.AlignLeft)
        gridBoxConnection.addWidget(labelCheckProxyTimeout, 1, 0, Qt.AlignLeft)
        gridBoxConnection.addWidget(self.spinBoxCheckProxyTimeout, 1, 1, Qt.AlignLeft)
        gridBoxConnection.addWidget(labelCheckProxyTimeoutWarning, 1, 2, Qt.AlignLeft)
        gridBoxConnection.addWidget(labeltrytimes, 2, 0, Qt.AlignLeft)
        gridBoxConnection.addWidget(self.spinboxTrytimes, 2, 1, Qt.AlignLeft)
        gridBoxConnection.addWidget(labelMaxtrytimes, 2, 2, Qt.AlignLeft)

        hboxConnection = QHBoxLayout()
        hboxConnection.addLayout(gridBoxConnection)
        hboxConnection.addStretch()
        
        vboxConnection = QVBoxLayout()
        vboxConnection.addLayout(hboxRadioButton)
        vboxConnection.addLayout(hboxConnection)

        self.grouBoxConnection.setLayout(vboxConnection)
        
        labelLanguageSetting = QLabel(
            self.translate("bridgepreferencesPanel", "Language: "))
        self.comboBoxLanguage = QComboBox()
        hboxLanguage = QHBoxLayout()
        hboxLanguage.addWidget(labelLanguageSetting)
        hboxLanguage.addWidget(self.comboBoxLanguage)
        hboxLanguage.addStretch()
        
        self.comboxStarup = QCheckBox(
            self.translate("bridgepreferencesPanel", "Starting Script Automatically on System Boot"))
        self.comboxStarup.setChecked(False)
        self.comboxStarup.setVisible(False)
        if not CRONTAB and not is_win:
            self.comboxStarup.setCheckable(False)
            self.comboxStarup.clicked.connect(lambda: QToolTip.showText(
                QCursor.pos(), self.translate(
                    "bridgepreferencesPanel",
                    "Please install python package crontab (pip3 install python-crontab)"),
                self.comboxStarup))

        vboxpreferences = QVBoxLayout()
        vboxpreferences.addLayout(gridBox)
        vboxpreferences.addWidget(self.grouBoxConnection)
        vboxpreferences.addLayout(hboxLanguage)
        vboxpreferences.addWidget(self.comboxStarup)
        vboxpreferences.addStretch()
        vboxpreferences.addLayout(hboxbutton)
        
        self.setLayout(vboxpreferences)
        self.setWindowTitle(
            self.translate("bridgepreferencesPanel", "Preferences"))
        self.resize(QSize(680, 320))
        
        self.createpreferencePanelSignals()
        
        self.settingv2rayshellpreferencesPanel()
        
        if v2rayshellDebug:
            self.comboxStarup.setVisible(True)
            self.starupTest = startUp()
            hbox = QHBoxLayout()
            self.__testBtn = QPushButton("__testBtn")
            hbox.addWidget(self.__testBtn)
            vboxpreferences.addLayout(hbox)
            self.__testBtn.clicked.connect(lambda: self.starupTest.setStartUp(True))
        
    def createpreferencePanelSignals(self):
        self.buttonpreferenceCancel.clicked.connect(self.onbuttonpreferenceCancel)
        self.buttonOpenV2raycoreFile.clicked.connect(self.onbuttonOpenV2raycoreFile)
        self.buttonpreferenceApply.clicked.connect(self.onbuttonpreferenceApply)
        self.comboxStarup.clicked.connect(self.onsetStartUp)
        
    def onsetStartUp(self):
        if (self.comboxStarup.isChecked()):
            self.starup.setStartUp(True)
        else:
            self.starup.setStartUp(False)

    def onbuttonpreferenceApply(self):
        filePath = self.lineEditFilePath.text()
        if filePath != "":
            self.bridgetreasureChest.setV2raycoreFilePath(filePath)
        
        connection = {}
        if self.grouBoxConnection.isChecked():
            connection["enable"] = True
        else:
            connection["enable"] = False
        
        if self.radioButtonReconnect.isChecked():
            connection["connect"] = "reconnect"
        elif self.radioButtonSwitch.isChecked():
            connection["connect"] = "switch"
            
        connection["interval"] = self.spinBoxInterval.value()
        connection["timeout"]  = self.spinBoxCheckProxyTimeout.value()
        connection["trytimes"] = self.spinboxTrytimes.value()
        
        self.bridgetreasureChest.setLanguage(self.comboBoxLanguage.currentText())
        self.bridgetreasureChest.setConnection(connection)
        self.bridgetreasureChest.save.emit()
        self.close()
        
    def onbuttonOpenV2raycoreFile(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self,
                                                      self.translate("bridgepreferencesPanel", "Open V2ray execute File"),
                                                      "",
                                                      "All File (*)",
                                                      options = options)
        if (filePath):
            self.lineEditFilePath.setText(filePath)
    
    def onbuttonpreferenceCancel(self):
        self.close()
    
    def settingv2rayshellpreferencesPanel(self):
        version      = self.bridgetreasureChest.getV2raycoreVersion()
        filePath     = self.bridgetreasureChest.getV2raycoreFilePath()
        allLanguages = self.bridgetreasureChest.getAllLanguage()
        language     = self.bridgetreasureChest.getLanguage()
        
        if version:
            self.labelv2raycorecurrentVersion.setText(version)
        if filePath:
            self.lineEditFilePath.setText(filePath)
        if allLanguages:
            self.comboBoxLanguage.clear()
            allLangs = []
            for i in allLanguages.keys():
                allLangs.append(i)
            self.comboBoxLanguage.addItems(allLangs)
            if language in allLangs:
                self.comboBoxLanguage.setCurrentText(language)
            else:
                self.comboBoxLanguage.setCurrentText("en_US")
        else:
            self.comboBoxLanguage.setCurrentText("en_US")
        
        connection = self.bridgetreasureChest.getConnection()
        if connection:
            try:
                connection["enable"]
            except Exception:
                connection["enable"] = False
    
            self.grouBoxConnection.setChecked(connection["enable"])
            
            try:
                connection["connect"]
            except Exception:
                connection["connect"] = "switch"
            
            if connection["connect"] == "switch":
                self.radioButtonSwitch.setChecked(True)
                self.radioButtonSwitch.setChecked(False)
            elif connection["connect"] == "reconnect":
                self.radioButtonReconnect.setChecked(True)
                self.radioButtonSwitch.setChecked(False)
                
            try:
                connection["interval"]
            except Exception:
                connection["interval"] = 10
            
            try:
                self.spinBoxInterval.setValue(connection["interval"])
            except Exception:
                self.spinBoxInterval.setValue(10)
                
            try:
                self.spinBoxCheckProxyTimeout.setValue(connection["timeout"])
            except Exception:
                self.spinBoxCheckProxyTimeout.setValue(3)
                
            try:
                self.spinboxTrytimes.setValue(connection["trytimes"])
            except Exception:
                self.spinboxTrytimes.setValue(3)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = bridgepreferencesPanel()
    ex.createpreferencesPanel()
    ex.show()
    sys.exit(app.exec_())