#!/usr/bin/env python3

from PyQt5.QtWidgets import (QLabel, QCheckBox, QWidget, QGroupBox, QHBoxLayout, QVBoxLayout,
                             QRadioButton, QTableWidget, QPushButton, QAbstractItemView,
                             QButtonGroup, QLineEdit, QFileDialog, QTableWidgetItem)
from PyQt5.QtCore import QFileInfo, QCoreApplication
v2rayshellDebug = False

import sys, copy

if __name__ == "__main__":
    v2rayshellDebug = True
    # this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-4]))
        
from bridgehouse.editMap.transport import (
    mkcpPanel, wsPanel, tcpPanel, httpPanel, logbook)


class TransportSettingPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.translate = QCoreApplication.translate

        self.labelHeaderTLSSetting = (self.translate("TransportSettingPanel", "Certificate File"),
                                      self.translate("TransportSettingPanel", "Key File"))

    def createTransportSettingPanel(self):
        labelNetwork = QLabel(
            self.translate("TransportSettingPanel", "Network: "), self)
        self.radioButtonTransportTCP = radioButtonTCP = QRadioButton(
            self.translate("TransportSettingPanel", "TCP"), self)
        self.radioButtonmTransportKCP = radioButtonmKCP = QRadioButton(
            self.translate("TransportSettingPanel", "mKcp"), self)
        self.radioButtonTransportWS = radioButtonWS = QRadioButton(
            self.translate("TransportSettingPanel", "ws"), self)
        self.radioButtonTransportHTTP = radioButtonHTTP = QRadioButton(
            self.translate("TransportSettingPanel", "http"), self)

        radioButtonTCP.setChecked(True)

        self.groupBtnNewtwork = QButtonGroup(self)
        self.groupBtnNewtwork.addButton(radioButtonmKCP)
        self.groupBtnNewtwork.addButton(radioButtonTCP)
        self.groupBtnNewtwork.addButton(radioButtonWS)
        self.groupBtnNewtwork.addButton(radioButtonHTTP)
        
        hboxNetwork = QHBoxLayout()
        hboxNetwork.addWidget(labelNetwork)
        hboxNetwork.addWidget(radioButtonTCP)
        hboxNetwork.addWidget(radioButtonmKCP)
        hboxNetwork.addWidget(radioButtonWS)
        hboxNetwork.addWidget(radioButtonHTTP)
        hboxNetwork.addStretch()
        
        self.vboxNetwork = QVBoxLayout()
        self.vboxNetwork.addLayout(hboxNetwork)
        self.vboxNetwork.addWidget(self.createCertificatesSetting())
        
        self.createTransportSettingPanelSignals()
        
        return self.vboxNetwork
   
    def createCertificatesSetting(self):
        self.tableWidgetUserCertificates = tableWidgetUser = QTableWidget(self)
        tableWidgetUser.setRowCount(0)
        tableWidgetUser.setColumnCount(2)
        tableWidgetUser.adjustSize()
        tableWidgetUser.setHorizontalHeaderLabels(self.labelHeaderTLSSetting)
        tableWidgetUser.setSelectionMode(QAbstractItemView.SingleSelection)
        tableWidgetUser.setSelectionBehavior(QAbstractItemView.SelectRows)
        tableWidgetUser.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # tableWidgetUser.horizontalHeader().setStretchLastSection(True)
        
        labelCertificateFile = QLabel(
            self.translate("TransportSettingPanel", "Certificate File: "), self)
        labelServerName = QLabel(
            self.translate("TransportSettingPanel", "Server Name: "), self)
        labelKeyFile = QLabel(
            self.translate("TransportSettingPanel", "Key File: "), self)
        btnOpenCertificatesFile = QPushButton(
            self.translate("TransportSettingPanel", "&Open"), self)
        btnOpenKeyFile = QPushButton(
            self.translate("TransportSettingPanel", "O&pen"), self)
        btnClear = QPushButton(
            self.translate("TransportSettingPanel", "Clear"), self)
        btnChange = QPushButton(
            self.translate("TransportSettingPanel", "Modify"), self)
        btnAdd = QPushButton(
            self.translate("TransportSettingPanel", "Add"), self)
        btnDelete = QPushButton(
            self.translate("TransportSettingPanel", "Delete"), self)

        self.checkBoxCertificateAllowInsecure = QCheckBox(
            self.translate("TransportSettingPanel", "Allow Insecure"), self)
        self.lineEditCertificateServerName = QLineEdit()
        self.lineEditCertificateFile = QLineEdit(self)
        self.lineEditCertificateKeyFile = QLineEdit(self)
        
        self.groupBtnOpenCertificatesFile = QButtonGroup()
        self.groupBtnOpenCertificatesFile.addButton(btnOpenCertificatesFile)
        self.groupBtnOpenCertificatesFile.addButton(btnOpenKeyFile)
        
        self.groupBtnCertificates = QButtonGroup(self)
        self.groupBtnCertificates.addButton(btnClear)
        self.groupBtnCertificates.addButton(btnChange)
        self.groupBtnCertificates.addButton(btnAdd)
        self.groupBtnCertificates.addButton(btnDelete)
        
        hboxServerName = QHBoxLayout()
        hboxServerName.addWidget(labelServerName)
        hboxServerName.addWidget(self.lineEditCertificateServerName)
        hboxServerName.addWidget(self.checkBoxCertificateAllowInsecure)
        hboxServerName.addStretch()
        
        hboxCertificateFile = QHBoxLayout()
        hboxCertificateFile.addWidget(labelCertificateFile)
        hboxCertificateFile.addWidget(self.lineEditCertificateFile)
        hboxCertificateFile.addWidget(btnOpenCertificatesFile)
        
        hboxCertificateKeyFile = QHBoxLayout()
        hboxCertificateKeyFile.addWidget(labelKeyFile)
        hboxCertificateKeyFile.addWidget(self.lineEditCertificateKeyFile)
        hboxCertificateKeyFile.addWidget(btnOpenKeyFile)
        
        vboxCertificateFiles = QVBoxLayout()
        vboxCertificateFiles.addLayout(hboxCertificateFile)
        vboxCertificateFiles.addLayout(hboxCertificateKeyFile)
        
        vboxCertificateFilesBtn = QVBoxLayout()
        vboxCertificateFilesBtn.addStretch()
        vboxCertificateFilesBtn.addWidget(btnAdd)
        vboxCertificateFilesBtn.addWidget(btnClear)
        vboxCertificateFilesBtn.addWidget(btnChange)
        vboxCertificateFilesBtn.addWidget(btnDelete)
        
        hboxTableWidgetCertificate = QHBoxLayout()
        hboxTableWidgetCertificate.addWidget(self.tableWidgetUserCertificates)
        hboxTableWidgetCertificate.addLayout(vboxCertificateFilesBtn)
        
        vboxCertificateFiles.addLayout(hboxTableWidgetCertificate)
        
        vboxTLSSetting = QVBoxLayout()
        vboxTLSSetting.addLayout(hboxServerName)
        vboxTLSSetting.addLayout(vboxCertificateFiles)
        
        self.groupBoxTLSSetting = groupBoxTLSSetting = QGroupBox(
            self.translate("TransportSettingPanel", "TLS Setting: "), self)
        groupBoxTLSSetting.setCheckable(True)
        if (v2rayshellDebug):
            groupBoxTLSSetting.setChecked(True)
        else:
            groupBoxTLSSetting.setChecked(False)
            
        groupBoxTLSSetting.setLayout(vboxTLSSetting)
        
        return groupBoxTLSSetting
            
    def createTransportSettingPanelSignals(self):
        self.groupBtnOpenCertificatesFile.buttonClicked.connect(self.onbtnOpenCertificatesFile)
        self.tableWidgetUserCertificates.itemSelectionChanged.connect(self.ontableWidgetUserCeritficatesItemSelectionChanged)
        
    def onbtnOpenCertificatesFile(self, e):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  self.translate("TransportSettingPanel", "Open Certificates File"),
                                                  "",
                                                  "All Files (*)",
                                                  options=options)
        if (fileName):
            if (e.text() == self.translate("TransportSettingPanel", "&Open")):
                self.lineEditCertificateFile.setText(fileName)
            if (e.text() == self.translate("TransportSettingPanel", "O&pen")):
                self.lineEditCertificateKeyFile.setText(fileName)
        
    def ontableWidgetUserCeritficatesItemSelectionChanged(self):
        currentRow = self.tableWidgetUserCertificates.currentRow()
        certificateFile = self.tableWidgetUserCertificates.item(currentRow, 0) 
        keyFile = self.tableWidgetUserCertificates.item(currentRow, 1) 
        
        if (certificateFile):
            self.lineEditCertificateFile.setText(certificateFile.text())
        else:
            self.lineEditCertificateFile.clear()
        
        if (keyFile):
            self.lineEditCertificateKeyFile.setText(keyFile.text())
        else:
            self.lineEditCertificateKeyFile.clear()
            
    def ongroupBtnCertificatesClicked(self, e):
        rowCount = self.tableWidgetUserCertificates.rowCount()
        currentRow = self.tableWidgetUserCertificates.currentRow()
        
        def settableWidgetUserCertificates(row):
            self.tableWidgetUserCertificates.setItem(row, 0, QTableWidgetItem(self.lineEditCertificateFile.text()))
            self.tableWidgetUserCertificates.setItem(row, 1, QTableWidgetItem(self.lineEditCertificateKeyFile.text()))
            self.tableWidgetUserCertificates.resizeColumnsToContents()

        if (e.text() == self.translate("TransportSettingPanel", "Add")):
            if (not self.lineEditCertificateFile.text() or not self.lineEditCertificateKeyFile.text()): return
            self.tableWidgetUserCertificates.setRowCount(rowCount + 1)
            settableWidgetUserCertificates(rowCount)
            self.onbtnInboudPanelClear()
        if (e.text() == self.translate("TransportSettingPanel", "Modify")):
            if (not self.lineEditCertificateFile.text() or not self.lineEditCertificateKeyFile.text()): return
            settableWidgetUserCertificates(currentRow)
        if (e.text() == self.translate("TransportSettingPanel", "Delete")):
            self.tableWidgetUserCertificates.removeRow(currentRow)
            self.onbtnInboudPanelClear()
        if (e.text() == self.translate("TransportSettingPanel", "Clear")):
            self.onbtnInboudPanelClear()
           
    def onbtnInboudPanelClear(self):
        self.lineEditCertificateFile.clear()
        self.lineEditCertificateKeyFile.clear()


class TransportPanel(TransportSettingPanel,
                     mkcpPanel.mKcpPanel,
                     wsPanel.wsPanel,
                     tcpPanel.TcpPanel):

    def __init__(self):
        super().__init__()
        self.transportJSONFile = {
                        "network": "tcp",
                        "security": "none",
                        "tlsSettings": {
                            "serverName": "v2ray.com",
                            "allowInsecure": True,
                            "certificates": [
                                {
                                    "certificateFile": "/path/to/certificate.crt",
                                    "keyFile": "/path/to/key.key"
                                    }
                                             ]
                                        },
                        "tcpSettings": {},
                        "kcpSettings": {},
                        "wsSettings": {},
                        "httpSettings": {}
                        }
        self.translate = QCoreApplication.translate
    
    def createTransportPanel(self):
        TransportSettingPanel = self.createTransportSettingPanel()
        self.mkcp = mkcpPanel.mKcpPanel()
        self.tcp = tcpPanel.TcpPanel()
        self.ws = wsPanel.wsPanel()
        self.http = httpPanel.httpPanel()
        self.mkcpPanel = self.mkcp.createmKcpSettingPanel()
        self.tcpPanel = self.tcp.createTCPSettingPanel()
        self.wsPanel = self.ws.createwsSettingPanel()
        self.httpPanel = self.http.createHttpSettingPanel()
        self.mkcpPanel.hide()
        self.wsPanel.hide()
        self.httpPanel.hide()
        
        vboxTransportProtocols = QVBoxLayout()
        vboxTransportProtocols.addWidget(self.mkcpPanel)
        vboxTransportProtocols.addWidget(self.tcpPanel)
        vboxTransportProtocols.addWidget(self.wsPanel)
        vboxTransportProtocols.addWidget(self.httpPanel)
        vboxTransportProtocols.addStretch()
        
        self.checkBoxTransportSetting = QCheckBox(
            self.translate("TcpPanel", "Transport Setting"), self)
        self.checkBoxTransportSetting.setCheckable(True)
        self.checkBoxTransportSetting.setChecked(False)
        
        self.vboxcheckBoxStreamSetting = QVBoxLayout()
        self.vboxcheckBoxStreamSetting.addWidget(self.checkBoxTransportSetting)
        
        self.vboxTransportPanel = QVBoxLayout()
        self.vboxTransportPanel.addLayout(TransportSettingPanel)
        self.vboxTransportPanel.addLayout(vboxTransportProtocols)
        
        self.groupTransportPanel = QGroupBox("", self)
        self.groupTransportPanel.hide()
        self.groupTransportPanel.setLayout(self.vboxTransportPanel)
        self.vboxcheckBoxStreamSetting.addWidget(self.groupTransportPanel)
        
        if (v2rayshellDebug):
            self.__debugBtn = QPushButton("__debugTest", self)
            self.vboxcheckBoxStreamSetting.addWidget(self.__debugBtn)
            self.__debugBtn.clicked.connect(self.__debugTest)
            self.settingtransportPanelFromJSONFile(self.transportJSONFile, True)
            self.groupTransportPanel.show()
        
        self.createTransportPanelSignals()

        return self.vboxcheckBoxStreamSetting
        
    def createTransportPanelSignals(self):
        self.groupBtnNewtwork.buttonClicked.connect(self.ongroupBtnNetwork)
        self.checkBoxTransportSetting.clicked.connect(self.onHideAndShowStreamStettingPanle)
        self.groupBtnCertificates.buttonClicked.connect(self.ongroupBtnCertificatesClicked)
        
    def ongroupBtnNetwork(self, e):

        def showNetwork(btn=e):
            self.tcpPanel.hide()
            self.wsPanel.hide()
            self.mkcpPanel.hide()
            self.httpPanel.hide()
            if (btn == self.translate("TransportSettingPanel", "mKcp")):
                self.mkcpPanel.show()
            elif (btn == self.translate("TransportSettingPanel", "ws")):
                self.wsPanel.show()
            elif (btn == self.translate("TransportSettingPanel", "TCP")):
                self.tcpPanel.show()
            elif (btn == self.translate("TransportSettingPanel", "http")):
                self.httpPanel.show()

        showNetwork(e.text())

    def onHideAndShowStreamStettingPanle(self, e):
        if (e):
            self.groupTransportPanel.show()
        else :
            self.groupTransportPanel.hide()

    def settingtransportPanelFromJSONFile(self, transportJSONFile=None, openFromJSONFile=False):
        logbook.setisOpenJSONFile(openFromJSONFile)
        certificatesFilesNumber = 0

        if (not transportJSONFile ): 
            transportJSONFile = {}
            self.checkBoxTransportSetting.setChecked(False)
            return False
        
        try:
            transportJSONFile["network"]
        except KeyError as e:
            logbook.writeLog("transport", "KeyError", e)
            transportJSONFile["network"] = "tcp"
        
        try:
            transportJSONFile["security"]
        except KeyError as e:
            logbook.writeLog("transport", "KeyError", e)
            transportJSONFile["security"] = "none"
        
        try:
            transportJSONFile["tlsSettings"]
        except KeyError as e:
            logbook.writeLog("transport", "KeyError", e)
            transportJSONFile["tlsSettings"] = None
        
        try:
            transportJSONFile["tcpSettings"]
        except KeyError as e:
            logbook.writeLog("transport", "KeyError", e)
            transportJSONFile["tcpSettings"] = None
        
        try:
            transportJSONFile["kcpSettings"]
        except KeyError as e:
            logbook.writeLog("transport", "KeyError", e)
            transportJSONFile["kcpSettings"] = None
        
        try:
            transportJSONFile["wsSettings"]
        except KeyError as e:
            logbook.writeLog("transport", "KeyError", e)
            transportJSONFile["wsSettings"] = None
            
        try:
            transportJSONFile["httpSettings"]
        except KeyError as e:
            logbook.writeLog("transport", "KeyError", e)
            transportJSONFile["httpSettings"] = None
        
        
        def hideSettingsandDisableRadioButton():
            self.tcpPanel.hide()
            self.wsPanel.hide()
            self.mkcpPanel.hide()
            self.httpPanel.hide()
            self.ws.groupBoxwsSetting.setChecked(False)
            self.mkcp.groupBoxmKCPSetting.setChecked(False)
            self.tcp.groupBoxTCPSetting.setChecked(False)
            self.http.groupBoxhttp.setChecked(False)

        def setTransport(protocol=transportJSONFile["network"]):
            if (protocol == "tcp"):
                hideSettingsandDisableRadioButton()
                self.radioButtonTransportTCP.setChecked(True)
                self.tcpPanel.show()
                if (transportJSONFile["tcpSettings"]):
                    self.tcp.settingtcpPanelFromJSONFile(
                        copy.deepcopy(transportJSONFile["tcpSettings"]), openFromJSONFile)
                    self.tcp.groupBoxTCPSetting.setChecked(True)
            
            elif (protocol == "kcp"):
                hideSettingsandDisableRadioButton()
                self.radioButtonmTransportKCP.setChecked(True)
                self.mkcpPanel.show()
                if (transportJSONFile["kcpSettings"]):
                    self.mkcp.settingmKcpPanelFromJSONFile(
                        copy.deepcopy(transportJSONFile["kcpSettings"]), openFromJSONFile)
                    self.mkcp.groupBoxmKCPSetting.setChecked(True)

            elif (protocol == "ws"):
                hideSettingsandDisableRadioButton()
                self.radioButtonTransportWS.setChecked(True)
                self.wsPanel.show()
                if (transportJSONFile["wsSettings"]):
                    self.ws.settingwsPanelFromJSONFile(
                        copy.deepcopy(transportJSONFile["wsSettings"]), openFromJSONFile)
                    self.ws.groupBoxwsSetting.setChecked(True)
                    
            elif (protocol == "http"):
                hideSettingsandDisableRadioButton()
                self.radioButtonTransportHTTP.setChecked(True)
                self.httpPanel.show()
                if (transportJSONFile["httpSettings"]):
                    self.http.groupBoxhttp.setChecked(True)
                    self.http.settingHttpPanelFromJSONFile(
                        copy.deepcopy(transportJSONFile["httpSettings"]), openFromJSONFile)
        
        setTransport()
        
        def cleartlsSettings():
            self.groupBoxTLSSetting.setChecked(False)
            self.checkBoxCertificateAllowInsecure.setChecked(False)
            self.tableWidgetUserCertificates.setRowCount(0)
            self.lineEditCertificateServerName.clear()
            
        if (transportJSONFile["security"] == "tls"):
            self.groupBoxTLSSetting.setChecked(True)
            if (not transportJSONFile["tlsSettings"]):
                cleartlsSettings()
                certificatesFilesNumber = 0
            else:
                try:
                    certificatesFilesNumber = len(transportJSONFile["tlsSettings"]["certificates"])
                except KeyError as e:
                    logbook.writeLog("transport", "KeyError", e)
                try:
                    certificateFiles = transportJSONFile["tlsSettings"]["certificates"]
                except KeyError as e:
                    logbook.writeLog("transport", "KeyError", e)
                except:
                    logbook.writeLog("transport tlsSettings certificates", "unkonw")
                try:
                    self.lineEditCertificateServerName.setText(
                        str(transportJSONFile["tlsSettings"]["serverName"]))
                except KeyError as e:
                    logbook.writeLog("transport", "KeyError", e)
                try:
                    self.checkBoxCertificateAllowInsecure.setChecked(
                        bool(transportJSONFile["tlsSettings"]["allowInsecure"]))
                except KeyError as e:
                    logbook.writeLog("transport", "KeyError", e)
        else:
            cleartlsSettings()
            certificatesFilesNumber = 0
            
        if (certificatesFilesNumber):
            self.tableWidgetUserCertificates.setRowCount(certificatesFilesNumber)
            try:
                for i in range(certificatesFilesNumber):
                    self.tableWidgetUserCertificates.setItem(
                        i, 0, QTableWidgetItem(str(certificateFiles[i]["certificateFile"])))
                    self.tableWidgetUserCertificates.setItem(
                        i, 1, QTableWidgetItem(str(certificateFiles[i]["keyFile"])))
                    self.tableWidgetUserCertificates.resizeColumnsToContents()
            except KeyError as e:
                logbook.writeLog("transport", "KeyError", e)
        else:
            self.tableWidgetUserCertificates.setRowCount(0)

    def createtransportSettingJSONFile(self):
        transportJSONFile = {}
        if (self.radioButtonmTransportKCP.isChecked()):
            transportJSONFile["network"] = "kcp"
        if (self.radioButtonTransportTCP.isChecked()):
            transportJSONFile["network"] = "tcp"
        if (self.radioButtonTransportWS.isChecked()):
            transportJSONFile["network"] = "ws"
        if (self.radioButtonTransportHTTP.isChecked()):
            transportJSONFile["network"] = "http"
        
        if (self.groupBoxTLSSetting.isChecked()):
            transportJSONFile["security"] = "tls"
            transportJSONFile["tlsSettings"] = {}
            if self.checkBoxCertificateAllowInsecure.isChecked():
                transportJSONFile["tlsSettings"]["allowInsecure"] = True
            if self.lineEditCertificateServerName.text():
                transportJSONFile["tlsSettings"]["serverName"] = copy.deepcopy(self.lineEditCertificateServerName.text())
            certificatesFilesNumber = self.tableWidgetUserCertificates.rowCount()
            files = []
            if (certificatesFilesNumber > 0):
                for i in range(0, certificatesFilesNumber):
                    fileName = {}
                    certificateFile = self.tableWidgetUserCertificates.item(i, 0)
                    keyFile = self.tableWidgetUserCertificates.item(i, 1)
                    if (certificateFile and keyFile):
                        fileName["certificateFile"] = certificateFile.text()
                        fileName["keyFile"] = keyFile.text()
                        files.append(copy.deepcopy(fileName))
                transportJSONFile["tlsSettings"]["certificates"] = copy.deepcopy(files)
            else:
                del files; certificatesFilesNumber
        else:
            transportJSONFile["security"] = "none"

        if (self.radioButtonmTransportKCP.isChecked() and self.mkcp.groupBoxmKCPSetting.isChecked()):
            transportJSONFile["kcpSettings"] = copy.deepcopy(self.mkcp.createmKcpSettingJSONFile())

        if (self.radioButtonTransportTCP.isChecked() and self.tcp.groupBoxTCPSetting.isChecked()):
            transportJSONFile["tcpSettings"] = copy.deepcopy(self.tcp.createtcpSettingJSONFile())

        if (self.radioButtonTransportWS.isChecked() and self.ws.groupBoxwsSetting.isChecked()):
            transportJSONFile["wsSettings"] = copy.deepcopy(self.ws.createwsSettingJSONFile())

        if (self.radioButtonTransportHTTP.isChecked() and self.http.groupBoxhttp.isChecked()):
            transportJSONFile["httpSettings"] = copy.deepcopy(self.http.createHttpSettingJSONFile())
        
        return transportJSONFile
    
    def clearTransportPanel(self):
        # set to Default
        self.checkBoxTransportSetting.setChecked(False)
        self.tableWidgetUserCertificates.setRowCount(0)
        self.groupBoxTLSSetting.setChecked(False)
        self.lineEditCertificateFile.clear()
        self.lineEditCertificateKeyFile.clear()
        self.lineEditCertificateServerName.clear()
        self.checkBoxCertificateAllowInsecure.setChecked(False)
        self.radioButtonTransportTCP.setChecked(True)
        self.radioButtonmTransportKCP.setChecked(False)
        self.radioButtonTransportWS.setChecked(False)
        self.radioButtonTransportHTTP.setChecked(False)
        self.tcpPanel.show()
        self.groupTransportPanel.hide()
        self.mkcp.clearmkcpPanel()
        self.ws.clearwsPanel()
        self.tcp.cleartcpPanel()
        #self.http.clearHttpPanel()  # a bug need fix

    def __debugTest(self):
        import json
        print(json.dumps(self.createtransportSettingJSONFile(), indent=4, sort_keys=False))


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = TransportPanel()
    ex.setLayout(ex.createTransportPanel())
    ex.setGeometry(300, 300, 680, 620)
    ex.show()
    sys.exit(app.exec_())
