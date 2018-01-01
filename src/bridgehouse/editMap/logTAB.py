#!/usr/bin/env python3

from PyQt5.QtWidgets import (QLabel,  QWidget, QHBoxLayout, QVBoxLayout, 
                             QPushButton, QButtonGroup, QLineEdit, 
                             QFileDialog, QComboBox, QGroupBox)
from PyQt5.QtCore import QDate, QTime, qWarning, QFileInfo, QCoreApplication

import sys, json
v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    ### this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.path().split("/")
    sys.path.append("/".join(srcPath[:2]))

class logBook():
    """
    Check the status of the v2ray before departure
    """
    def __init__(self, openFromJSONFile = False):
        ### only record the debug message when use open conf.json file
        self.openFile = openFromJSONFile

    def setisOpenJSONFile(self, openFromJSONFile):
        self.openFile = openFromJSONFile
        
    def getTime(self):
        return QDate.currentDate().toString()+" "+QTime.currentTime().toString("HH:mm:ss")
    
    def writeLog(self, cabin, situation, log = "unkonw"):
        if (self.openFile):
            if (situation == "KeyError"):
                qWarning("Date: {} ---> {} Panel analysis of JSON file error. can not find the key {}, use default value.".format(self.getTime(), cabin, log))
            elif (situation == "ValueError or TypeError" or 
                  situation == "ValueError" or 
                  situation == "TypeError"):
                qWarning("Date: {} ---> {} Panel analysis of JSON file error. can not use this value {}, use default value.".format(self.getTime(), cabin, log))
            else:
                qWarning("Date: {} ---> {} Panel analysis of JSON file error. have a error:--> {} <--".format(self.getTime(), cabin, log))

class logTab(QWidget):
    def __init__(self):
        super().__init__()
        self.logJSONFile = {
                            "access": "",
                            "error": "",
                            "loglevel": "warning"
                        }
        self.translate = QCoreApplication.translate
    
    def createLogTab(self):
        labelAccess = QLabel(
            self.translate("logTab", "Access File: "))
        labelError  = QLabel(
            self.translate("logTab", "Error  File:  "))
        self.lineEditAccess = QLineEdit()
        self.lineEditError  = QLineEdit()
        
        btnSaveAccess = QPushButton(
            self.translate("logTab", "&Save"), self)
        btnSaveError  = QPushButton(
            self.translate("logTab", "S&ave"), self)
        
        labelLogLevel = QLabel(self.translate("logTab", "Log Level: "), self)
        self.comboxLogLevel = QComboBox()
        self.comboxLogLevel.addItems(("warning", "debug", "info", "error" ,"none"))
        
        self.buttonGroupSave = QButtonGroup()
        self.buttonGroupSave.addButton(btnSaveAccess)
        self.buttonGroupSave.addButton(btnSaveError)
        
        hboxAccess = QHBoxLayout()
        hboxAccess.addWidget(labelAccess)
        hboxAccess.addWidget(self.lineEditAccess)
        hboxAccess.addWidget(btnSaveAccess)
        
        hboxError = QHBoxLayout()
        hboxError.addWidget(labelError)
        hboxError.addWidget(self.lineEditError)
        hboxError.addWidget(btnSaveError)
        
        hboxLogLevel = QHBoxLayout()
        hboxLogLevel.addWidget(labelLogLevel)
        hboxLogLevel.addWidget(self.comboxLogLevel)
        hboxLogLevel.addStretch()
        
        vboxLogPanel = QVBoxLayout()
        vboxLogPanel.addLayout(hboxAccess)
        vboxLogPanel.addLayout(hboxError)
        vboxLogPanel.addLayout(hboxLogLevel)
        vboxLogPanel.addStretch()
    
        self.setLayout(vboxLogPanel)
        
        groupBoxLogTAB = QGroupBox("", self)
        groupBoxLogTAB.setLayout(vboxLogPanel)
        
        self.createLogTabSignals()
        
        if (v2rayshellDebug):
            self.__debugBtn = QPushButton("__debugTest", self)
            vboxLogPanel.addWidget(self.__debugBtn)
            self.__debugBtn.clicked.connect(self.__debugTest)
            self.settingLogTabFromJSONFile(self.logJSONFile, True)
        
        return groupBoxLogTAB
    
    def createLogTabSignals(self):
        self.buttonGroupSave.buttonClicked.connect(self.onbuttonGroupSave)
        
    def onbuttonGroupSave(self, e):
        options = QFileDialog.Options()
        if (e.text() == self.translate("logTab", "&Save")):
                fileName, _ = QFileDialog.getSaveFileName(self,
                                                  self.translate("logTab", "Save V2ray Access log file"),
                                                  "_access",
                                                  "Log Files (*.log)",
                                                  options = options)
                self.lineEditAccess.setText(fileName)
                
        if (e.text() == self.translate("logTab", "S&ave")):
                fileName, _ = QFileDialog.getSaveFileName(self,
                                                  self.translate("logTab", "Save V2ray Error log file"),
                                                  "_error",
                                                  "Log Files (*.log)",
                                                  options = options)
                self.lineEditError.setText(fileName)
    
    def settingLogTabFromJSONFile(self, logJSONFile = {}, openFromJSONFile = False):
        logTagslog = logBook(openFromJSONFile)
        
        if (logJSONFile == None): logJSONFile = {}

        try:
            logJSONFile["access"]
        except KeyError as e:
            logTagslog.writeLog("LogTAB", "KeyError", e)
            logJSONFile["access"] = ""

        try:
            logJSONFile["error"]
        except KeyError as e:
            logTagslog.writeLog("LogTAB", "KeyError", e)
            logJSONFile["error"] = ""
                
        try:
            logJSONFile["loglevel"]
        except KeyError as e:
            logTagslog.writeLog("LogTAB", "KeyError", e)
            logJSONFile["loglevel"] = "warning"
            
        self.lineEditAccess.setText(str(logJSONFile["access"]))
        self.lineEditError.setText(str(logJSONFile["error"]))
        try:
            self.comboxLogLevel.setCurrentText(str(logJSONFile["loglevel"]))
        except (ValueError, TypeError) as e:
            logTagslog.writeLog("LogTAB", "ValueError or TypeError", e)

    def createLogJSONFile(self):
        logJSONFile = {}
        logJSONFile["access"]   = self.lineEditAccess.text()
        logJSONFile["error"]    = self.lineEditError.text()
        logJSONFile["loglevel"] = self.comboxLogLevel.currentText()
        
        return logJSONFile
    
    def __debugTest(self):
        print(json.dumps(self.createLogJSONFile(), indent = 4, sort_keys = False))
        
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = logTab()
    ex.createLogTab()
    ex.setGeometry(200, 100, 380, 180)
    ex.show()
    sys.exit(app.exec_())