#!/usr/bin/env python3

from PyQt5.QtWidgets import (QVBoxLayout, QWidget, QHBoxLayout, 
                             QPushButton, QTextEdit, QFileDialog,
                             QStatusBar, QGroupBox, QMessageBox, QDialog,
                             QApplication)
from PyQt5.QtCore import QFileInfo, QFile, QIODevice, QCoreApplication

import sys, json, copy, codecs

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    ### this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.path().split("/")
    sys.path.append("/".join(srcPath[:-3]))

from bridgehouse.editMap.port import treasureChest, logbook

class openV2rayJSONFile():
    """
    open a config.json file. 
    convert config.json file to v2ray-shell's format
    """
    def __init__(self, filePath = False, CaptainstreasureChest = False, disableLog = False):
        self.translate = QCoreApplication.translate
        self.JSONData = False
        if (disableLog):
            logbook.setisOpenJSONFile(False)
        else:
            logbook.setisOpenJSONFile(True)
        if (filePath):
            self.JSONData = self.openJSONData(filePath) 
 
        self.treasureChest = CaptainstreasureChest
        if (self.treasureChest == False):
            self.treasureChest = treasureChest.treasureChest()
        self.msgBox = QMessageBox()
        self.fly = QApplication.desktop().screen().rect().center()-self.msgBox.rect().center()

    def initboundJSONData(self):
        """
        save config.json file's data to class boundJSONData.
        ##########################
        boundJSONData.py
        self.__log            = {}
        self.__dns            = {}
        self.__routing        = {}
        self.__policy         = {}
        self.__inbound        = {}
        self.__outbound       = {}
        self.__inboundDetour  = {}
        self.__outboundDetour = {}
        self.__transport      = {}
        ##########################
        """
        
        JSONData = False
        if (self.JSONData):
            JSONData = copy.deepcopy(self.JSONData)
        else:
            return False
        
        try:
            JSONData["log"]
        except KeyError as e:
            logbook.writeLog("", "Parse json File Error", e)
            JSONData["log"] = {}
        
        try:
            JSONData["dns"]
        except KeyError as e:
            logbook.writeLog("", "Parse json File Error", e)
            JSONData["dns"] = {}
            
        try:
            JSONData["routing"]
        except KeyError as e:
            logbook.writeLog("", "Parse json File Error", e)
            JSONData["routing"] = {}
 
        try:
            JSONData["policy"]
        except KeyError as e:
            logbook.writeLog("", "Parse json File Error", e)
            JSONData["policy"] = {}
            JSONData["policy"]["levels"] = {}

        try:
            JSONData["inbound"]
        except KeyError as e:
            logbook.writeLog("", "Parse json File Error", e)
            JSONData["inbound"] = {}
            
        try:
            JSONData["outbound"]
        except KeyError as e:
            logbook.writeLog("", "Parse json File Error", e)
            JSONData["outbound"] = {}
        
        try:
            JSONData["inboundDetour"]
        except KeyError as e:
            logbook.writeLog("", "Parse json File Error", e)
            JSONData["inboundDetour"] = {}

        try:
            JSONData["outboundDetour"]
        except KeyError as e:
            logbook.writeLog("", "Parse json File Error", e)
            JSONData["outboundDetour"] = {}
            
        try:
            JSONData["transport"]
        except KeyError as e:
            logbook.writeLog("", "Parse json File Error", e)
            JSONData["transport"] = {}

        self.treasureChest.clear()
        self.treasureChest.setLog(JSONData["log"])
        self.treasureChest.setDns(JSONData["dns"])
        self.treasureChest.setPolicy(JSONData["policy"]["levels"])
        self.treasureChest.setRouting(JSONData["routing"])
        self.treasureChest.setInbound(JSONData["inbound"], openFromJSONFile = True)
        self.treasureChest.setOutbound(JSONData["outbound"], openFromJSONFile = True)
        self.treasureChest.setInboundDetour(None, JSONData["inboundDetour"], openFromJSONFile = True)
        self.treasureChest.setOutboundDetour(None, JSONData["outboundDetour"], openFromJSONFile = True)
        self.treasureChest.setTransport(JSONData["transport"])

        return JSONData

    def jsonDataValitor(self, JSONData):
        try:
            data = json.loads(str(JSONData))
        except ValueError as e:
            return -1, e
        return 0, data
    
    def openJSONData(self, filePath):
        self.msgBox = QMessageBox()
        self.fly = QApplication.desktop().screen().rect().center()-self.msgBox.rect().center()
        fileInfo = QFileInfo(filePath)
        fileName = fileInfo.fileName()
        openFile = QFile(filePath)
        
        openFile.open(QIODevice.ReadOnly | QIODevice.Text)
        if openFile.error() != openFile.NoError:
            self.msgBox.information(QDialog().move(self.fly), 
                               "{}".format(fileName), 
                               self.translate("openV2rayJSONFile", "Unable to open the file {}:  {}.").format(
                                   fileName, 
                                   openFile.errorString()))
            openFile = None
            return
        
        JSONData = str(openFile.readAll(), "utf-8")
        try:
            JSONData = json.loads(JSONData)
        except ValueError as e:
            self.msgBox.information(QDialog().move(self.fly), 
                               self.translate("openV2rayJSONFile", "Parse JSON Data Error"),
                               self.translate("openV2rayJSONFile", "Unable to parse {}:  error:{}.").format(fileName, e))
            openFile = None
            JSONData = None
            return
        else:
            return JSONData
        openFile.close()
        
    def saveTextdata(self, filePath, data):
        outFile = QFileInfo(filePath)
        
        fileName = outFile.fileName()
        if QFile.exists(fileName):
            QFile.remove(fileName)

        outFile = QFile(outFile.absoluteFilePath())
        
        outFile.open(QIODevice.WriteOnly | QIODevice.Text)
        if outFile.error() != outFile.NoError:
            self.msgBox.information(QDialog().move(self.fly), 
                               "{}".format(fileName), 
                               self.translate("openV2rayJSONFile", "Unable to open the file {}:  {}.").format(
                                   fileName, 
                                   outFile.errorString()))
            outFile = None
            return False
        
        outFile.write(codecs.encode(data, "utf-8"))
        
        if outFile.error() != outFile.NoError:
            self.msgBox.information(QDialog().move(self.fly), 
                               "{}".format(fileName), 
                               self.translate("openV2rayJSONFile", "Unable to save the file {}:  {}.").format(
                                   fileName, 
                                   outFile.errorString()))
            outFile = None
            return False
        
        outFile.close()

class editV2rayJSONFile(QWidget):
    """
    This class for debug or edit json file
    """
    def __init__(self, CaptainstreasureChest = False):
        super().__init__()
        
        self._windowTitle = "Edit JSON File"
        
        self.treasureChest = CaptainstreasureChest
        if (CaptainstreasureChest == False):
            self.treasureChest = treasureChest.treasureChest()

        self.createPanel()
        
    def createPanel(self):
        self.setWindowTitle(self._windowTitle)
        self.btnOpen = QPushButton("Open", self)
        self.btnSave = QPushButton("Save", self)
        self.statusBar = QStatusBar(self)
        self.textEditor = QTextEdit(self)
        self.textEditor.setFontPointSize(13)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.statusBar)
        #hbox.addStretch()
        hbox.addWidget(self.btnOpen)
        hbox.addWidget(self.btnSave)

        vbox = QVBoxLayout()
        vbox.addWidget(self.textEditor)
        vbox.addLayout(hbox)
        
        self.groupboxEdtorV2rayJSONFile = QGroupBox("", self)
        self.groupboxEdtorV2rayJSONFile.setLayout(vbox)
        
        self.createSignals()
        
        return self.groupboxEdtorV2rayJSONFile
    
    def createSignals(self):
        self.btnOpen.clicked.connect(self.onbtnOpen)
        self.btnSave.clicked.connect(self.onbtnSave)
        self.textEditor.textChanged.connect(self.ontextEditorChanged)
    
    def ontextEditorChanged(self):
        title = copy.deepcopy(self._windowTitle)
        self.setWindowTitle(title + "*")
    
    def onbtnOpen(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self,
                                                  "Open V2ray config.json File",
                                                  "",
                                                  """
                                                  V2ray conf.json (config.json);;
                                                  json file (*.json);;
                                                  v2ray-shell file(*.v2rayshell);;
                                                  All Files (*)
                                                  """,
                                                  options = options)
        if (filePath):
            JSONData = {}
            v2rayshell = filePath.split(".")[-1:][0]
            if (v2rayshell == "v2rayshell"):
                self.textEditor.clear()
                JSONData = openV2rayJSONFile.openJSONData(filePath)
                JSONData = json.loads(JSONData)
                JSONData = json.dumps(JSONData, indent = 4, sort_keys = False)
                self.textEditor.setText(JSONData)
                return
            else:
                JSONData = openV2rayJSONFile(filePath, self.treasureChest)
                JSONData = json.dumps(JSONData.initboundJSONData(), indent = 4, sort_keys = False)
                self.textEditor.clear()
                self.textEditor.setText(JSONData)
                self._windowTitle = "{}".format(filePath)
                self.setWindowTitle(self._windowTitle)
        
    def onbtnSave(self):
        text = self.textEditor.toPlainText()
        if (text == ""): 
            self.statusBar.showMessage("There have nothing to svae...") 
            return
        JSONData = openV2rayJSONFile().jsonDataValitor(copy.deepcopy(text))
        if (JSONData[0] == -1):
            logbook.writeLog("", "Parse json File Error", JSONData[1])
            self.statusBar.showMessage(JSONData[1])
            return
        else:
            JSONData = copy.deepcopy(json.dumps(JSONData[1], indent = 4, sort_keys = False))
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Save V2ray config.json file",
                                                  "",
                                                  """
                                                  json file (*.json);;
                                                  All file (*)
                                                  """,
                                                  options = options)
        if (fileName and JSONData != ""):
            openV2rayJSONFile().saveTextdata(filePath = fileName, 
                                             data     = JSONData)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = editV2rayJSONFile()
    ex.groupboxEdtorV2rayJSONFile.setFixedSize(1000, 750)
    ex.setGeometry(300, 100, 1024, 768)
    ex.show()
    sys.exit(app.exec_())