#!/usr/bin/env python3

from PyQt5.QtWidgets import (QLabel, QCheckBox, QWidget, QGroupBox, QHBoxLayout, QVBoxLayout,
                             QRadioButton, QTableWidget, QPushButton, QAbstractItemView,
                             QButtonGroup, QLineEdit, QFileDialog, QTableWidgetItem,
                             QComboBox, QListView, QTextEdit, QDialog, QApplication)
from PyQt5.QtCore import QFileInfo, QCoreApplication, Qt
v2rayshellDebug = False

import sys, copy, re

if __name__ == "__main__":
    v2rayshellDebug = True
    # this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-4]))
        
from bridgehouse.editMap.transport import (
    mkcpPanel, wsPanel, tcpPanel, http2Panel, dsPanel, logbook)


class TransportSettingPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.translate = QCoreApplication.translate

        self.labelHeaderTLSSetting = (
            self.translate("TransportSettingPanel", "Usage"),
            self.translate("TransportSettingPanel", "Certificate File"),
            self.translate("TransportSettingPanel", "Key File"),
            self.translate("TransportSettingPanel", "Certificate"),
            self.translate("TransportSettingPanel", "Key"))

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
        self.radioButtonTransportDS = radioButtonDS = QRadioButton(
            self.translate("TransportSettingPanel", "ds"), self)

        radioButtonTCP.setChecked(True)

        self.groupBtnNewtwork = QButtonGroup(self)
        self.groupBtnNewtwork.addButton(radioButtonmKCP)
        self.groupBtnNewtwork.addButton(radioButtonTCP)
        self.groupBtnNewtwork.addButton(radioButtonWS)
        self.groupBtnNewtwork.addButton(radioButtonHTTP)
        self.groupBtnNewtwork.addButton(radioButtonDS)
        
        hboxNetwork = QHBoxLayout()
        hboxNetwork.addWidget(labelNetwork)
        hboxNetwork.addWidget(radioButtonTCP)
        hboxNetwork.addWidget(radioButtonmKCP)
        hboxNetwork.addWidget(radioButtonWS)
        hboxNetwork.addWidget(radioButtonHTTP)
        hboxNetwork.addWidget(radioButtonDS)
        hboxNetwork.addStretch()
        
        self.vboxNetwork = QVBoxLayout()
        self.vboxNetwork.addLayout(hboxNetwork)
        self.vboxNetwork.addWidget(self.createCertificatesSetting())
        
        self.createTransportSettingPanelSignals()
        
        return self.vboxNetwork
    
    def addTLSusageCombox(self):
        usage = ("encipherment", "verify", "issue")
        comboxUsage = QComboBox()
        comboxUsage.setView(QListView())
        comboxUsage.insertItems(0, usage)
        return comboxUsage
   
    def createCertificatesSetting(self):
        self.tableWidgetUserCertificates = tableWidgetUser = QTableWidget(self)
        tableWidgetUser.setRowCount(0)
        tableWidgetUser.setColumnCount(5)
        tableWidgetUser.setHorizontalHeaderLabels(self.labelHeaderTLSSetting)
        tableWidgetUser.setSelectionMode(QAbstractItemView.SingleSelection)
        tableWidgetUser.setSelectionBehavior(QAbstractItemView.SelectRows)

        labelServerName = QLabel(
            self.translate("TransportSettingPanel", "Server Name: "), self)
        labelalpn= QLabel(
            self.translate("TransportSettingPanel", "Alpn: "), self)
        btnNew= QPushButton(
            self.translate("TransportSettingPanel", "New"), self)
        btnDelete = QPushButton(
            self.translate("TransportSettingPanel", "Delete"), self)

        self.checkBoxCertificateAllowInsecure = QCheckBox(
            self.translate("TransportSettingPanel", "Allow Insecure"), self)
        self.lineEditCertificateServerName = QLineEdit()
        self.lineEditCertificatealpn = QLineEdit(self)
        
        self.groupBtnCertificates = QButtonGroup(self)
        self.groupBtnCertificates.addButton(btnNew)
        self.groupBtnCertificates.addButton(btnDelete)
        
        hboxServerName = QHBoxLayout()
        hboxServerName.addWidget(labelServerName)
        hboxServerName.addWidget(self.lineEditCertificateServerName)
        hboxServerName.addWidget(self.checkBoxCertificateAllowInsecure)
        hboxServerName.addStretch()
        
        hboxaphn = QHBoxLayout()
        hboxaphn.addWidget(labelalpn)
        hboxaphn.addWidget(self.lineEditCertificatealpn)
        hboxaphn.addStretch()   

        vboxCertificateFilesBtn = QVBoxLayout()
        vboxCertificateFilesBtn.addStretch()
        vboxCertificateFilesBtn.addWidget(btnNew)
        vboxCertificateFilesBtn.addWidget(btnDelete)
        
        hboxTableWidgetCertificate = QHBoxLayout()
        hboxTableWidgetCertificate.addWidget(self.tableWidgetUserCertificates)
        hboxTableWidgetCertificate.addLayout(vboxCertificateFilesBtn)
        
        vboxCertificateFiles = QVBoxLayout()
        vboxCertificateFiles.addLayout(hboxTableWidgetCertificate)
        
        vboxTLSSetting = QVBoxLayout()
        vboxTLSSetting.addLayout(hboxServerName)
        vboxTLSSetting.addLayout(hboxaphn)
        vboxTLSSetting.addLayout(vboxCertificateFiles)
        
        self.groupBoxTLSSetting = groupBoxTLSSetting = QGroupBox(
            self.translate("TransportSettingPanel", "TLS Setting: "), self)
        groupBoxTLSSetting.setCheckable(True)
        if (v2rayshellDebug):
            groupBoxTLSSetting.setChecked(True)
        else:
            groupBoxTLSSetting.setChecked(False)
            
        groupBoxTLSSetting.setLayout(vboxTLSSetting)
        groupBoxTLSSetting.setFixedHeight(groupBoxTLSSetting.height()*10)
        
        return groupBoxTLSSetting
            
    def createTransportSettingPanelSignals(self):
        self.tableWidgetUserCertificates.cellDoubleClicked.connect(self.ontableWidgetCellDoubleClicked)
        
    def ontableWidgetCellDoubleClicked(self, row, column):
        if (column == 1 or column == 2):
            # certificateFile or keyFile
            self.openCertificatesFile(row, column)
        if (column == 3 or column == 4):
            # certificate or key
            text = self.tableWidgetUserCertificates.item(row, column)
            self.openWindowTextInput(
                row, column, None if not text else text.text())
        
    def openCertificatesFile(self, row, column):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  self.translate("TransportSettingPanel", "Open Certificates File"),
                                                  "",
                                                  "All Files (*)",
                                                  options=options)

        self.tableWidgetUserCertificates.setItem(
                row, column, QTableWidgetItem("" if not fileName else fileName))
        
    def openWindowTextInput(self, row, column, text=None):
        textEdit = QTextEdit()
        btnok = QPushButton(self.translate("TransportSettingPanel", "OK"))
        btncancel = QPushButton(self.translate("TransportSettingPanel", "Cancel"))
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(btnok)
        hbox.addWidget(btncancel)
        vbox = QVBoxLayout()
        vbox.addWidget(textEdit)
        vbox.addLayout(hbox)
        
        def getTextSetTabel(d):
            self.tableWidgetUserCertificates.setItem(
                row, column, QTableWidgetItem(",".join(textEdit.toPlainText().split(",\n"))))
            d.close()

        if text:
            textEdit.setText(",\n".join(text.split(",")))
        if column == 3:
            title =  self.translate("TransportSettingPanel", "Certificate")
        if column == 4:
            title =  self.translate("TransportSettingPanel", "Key")
        dialogTextEdit = QDialog()
        dialogTextEdit.setAttribute(Qt.WA_DeleteOnClose)
        dialogTextEdit.setWindowTitle(title)
        dialogTextEdit.move(
            QApplication.desktop().screen().rect().center()-dialogTextEdit.rect().center())
        dialogTextEdit.setLayout(vbox)
        btncancel.clicked.connect(dialogTextEdit.close)
        btnok.clicked.connect(lambda: getTextSetTabel(dialogTextEdit))
        dialogTextEdit.open()
        dialogTextEdit.exec_()

    def ongroupBtnCertificatesClicked(self, e):
        rowCount = self.tableWidgetUserCertificates.rowCount()
        currentRow = self.tableWidgetUserCertificates.currentRow()
        print((currentRow, e.text()))
        if (e.text() == self.translate("TransportSettingPanel", "Delete")):
            self.tableWidgetUserCertificates.removeRow(currentRow)
        if (e.text() == self.translate("TransportSettingPanel", "New")):
            self.onbtnCertificatesaddNewRow()
    
    def onbtnCertificatesaddNewRow(self):
        row = self.tableWidgetUserCertificates.rowCount()
        if (not row):
            self.tableWidgetUserCertificates.setRowCount(row+1)
            self.tableWidgetUserCertificates.setCellWidget(row, 0, self.addTLSusageCombox())
        else:
            crtFile = self.tableWidgetUserCertificates.item(row-1, 1)
            keyFile = self.tableWidgetUserCertificates.item(row-1, 2)
            crt = self.tableWidgetUserCertificates.item(row-1, 3)
            key = self.tableWidgetUserCertificates.item(row-1, 4)
            if ((crtFile and keyFile) or (crt and key)):
                self.tableWidgetUserCertificates.setRowCount(row+1)
                self.tableWidgetUserCertificates.setCellWidget(row, 0, self.addTLSusageCombox())

class TransportPanel(TransportSettingPanel,
                     mkcpPanel.mKcpPanel,
                     wsPanel.wsPanel,
                     tcpPanel.TcpPanel,
                     http2Panel.http2Panel,
                     dsPanel.domainSocketPanel):

    def __init__(self):
        super().__init__()
        self.transportJSONFile = {
                        "network": "tcp",
                        "security": "tls",
                        "tlsSettings": {
                            "serverName": "v2ray.com",
                            "allowInsecure": True,
                            "alpn": ["http/1.1"],
                            "certificates": [
                                {
                                    "usage": "encipherment",
                                    "certificateFile": "/path/to/certificate.crt",
                                    "keyFile": "/path/to/key.key",
                                    "certificate": [
                                              "-----BEGIN CERTIFICATE-----",
                                              "MIICwDCCAaigAwIBAgIRAO16JMdESAuHidFYJAR/7kAwDQYJKoZIhvcNAQELBQAw",
                                              "ADAeFw0xODA0MTAxMzU1MTdaFw0xODA0MTAxNTU1MTdaMAAwggEiMA0GCSqGSIb3",
                                              "DQEBAQUAA4IBDwAwggEKAoIBAQCs2PX0fFSCjOemmdm9UbOvcLctF94Ox4BpSfJ+",
                                              "3lJHwZbvnOFuo56WhQJWrclKoImp/c9veL1J4Bbtam3sW3APkZVEK9UxRQ57HQuw",
                                              "OzhV0FD20/0YELou85TwnkTw5l9GVCXT02NG+pGlYsFrxesUHpojdl8tIcn113M5",
                                              "pypgDPVmPeeORRf7nseMC6GhvXYM4txJPyenohwegl8DZ6OE5FkSVR5wFQtAhbON",
                                              "OAkIVVmw002K2J6pitPuJGOka9PxcCVWhko/W+JCGapcC7O74palwBUuXE1iH+Jp",
                                              "noPjGp4qE2ognW3WH/sgQ+rvo20eXb9Um1steaYY8xlxgBsXAgMBAAGjNTAzMA4G",
                                              "A1UdDwEB/wQEAwIFoDATBgNVHSUEDDAKBggrBgEFBQcDATAMBgNVHRMBAf8EAjAA",
                                              "MA0GCSqGSIb3DQEBCwUAA4IBAQBUd9sGKYemzwPnxtw/vzkV8Q32NILEMlPVqeJU",
                                              "7UxVgIODBV6A1b3tOUoktuhmgSSaQxjhYbFAVTD+LUglMUCxNbj56luBRlLLQWo+",
                                              "9BUhC/ow393tLmqKcB59qNcwbZER6XT5POYwcaKM75QVqhCJVHJNb1zSEE7Co7iO",
                                              "6wIan3lFyjBfYlBEz5vyRWQNIwKfdh5cK1yAu13xGENwmtlSTHiwbjBLXfk+0A/8",
                                              "r/2s+sCYUkGZHhj8xY7bJ1zg0FRalP5LrqY+r6BckT1QPDIQKYy615j1LpOtwZe/",
                                              "d4q7MD/dkzRDsch7t2cIjM/PYeMuzh87admSyL6hdtK0Nm/Q",
                                              "-----END CERTIFICATE-----"
                                            ],
                                    "key": [
                                              "-----BEGIN RSA PRIVATE KEY-----",
                                              "MIIEowIBAAKCAQEArNj19HxUgoznppnZvVGzr3C3LRfeDseAaUnyft5SR8GW75zh",
                                              "bqOeloUCVq3JSqCJqf3Pb3i9SeAW7Wpt7FtwD5GVRCvVMUUOex0LsDs4VdBQ9tP9",
                                              "GBC6LvOU8J5E8OZfRlQl09NjRvqRpWLBa8XrFB6aI3ZfLSHJ9ddzOacqYAz1Zj3n",
                                              "jkUX+57HjAuhob12DOLcST8np6IcHoJfA2ejhORZElUecBULQIWzjTgJCFVZsNNN",
                                              "itieqYrT7iRjpGvT8XAlVoZKP1viQhmqXAuzu+KWpcAVLlxNYh/iaZ6D4xqeKhNq",
                                              "IJ1t1h/7IEPq76NtHl2/VJtbLXmmGPMZcYAbFwIDAQABAoIBAFCgG4phfGIxK9Uw",
                                              "qrp+o9xQLYGhQnmOYb27OpwnRCYojSlT+mvLcqwvevnHsr9WxyA+PkZ3AYS2PLue",
                                              "C4xW0pzQgdn8wENtPOX8lHkuBocw1rNsCwDwvIguIuliSjI8o3CAy+xVDFgNhWap",
                                              "/CMzfQYziB7GlnrM6hH838iiy0dlv4I/HKk+3/YlSYQEvnFokTf7HxbDDmznkJTM",
                                              "aPKZ5qbnV+4AcQfcLYJ8QE0ViJ8dVZ7RLwIf7+SG0b0bqloti4+oQXqGtiESUwEW",
                                              "/Wzi7oyCbFJoPsFWp1P5+wD7jAGpAd9lPIwPahdr1wl6VwIx9W0XYjoZn71AEaw4",
                                              "bK4xUXECgYEA3g2o9WqyrhYSax3pGEdvV2qN0VQhw7Xe+jyy98CELOO2DNbB9QNJ",
                                              "8cSSU/PjkxQlgbOJc8DEprdMldN5xI/srlsbQWCj72wXxXnVnh991bI2clwt7oYi",
                                              "pcGZwzCrJyFL+QaZmYzLxkxYl1tCiiuqLm+EkjxCWKTX/kKEFb6rtnMCgYEAx0WR",
                                              "L8Uue3lXxhXRdBS5QRTBNklkSxtU+2yyXRpvFa7Qam+GghJs5RKfJ9lTvjfM/PxG",
                                              "3vhuBliWQOKQbm1ZGLbgGBM505EOP7DikUmH/kzKxIeRo4l64mioKdDwK/4CZtS7",
                                              "az0Lq3eS6bq11qL4mEdE6Gn/Y+sqB83GHZYju80CgYABFm4KbbBcW+1RKv9WSBtK",
                                              "gVIagV/89moWLa/uuLmtApyEqZSfn5mAHqdc0+f8c2/Pl9KHh50u99zfKv8AsHfH",
                                              "TtjuVAvZg10GcZdTQ/I41ruficYL0gpfZ3haVWWxNl+J47di4iapXPxeGWtVA+u8",
                                              "eH1cvgDRMFWCgE7nUFzE8wKBgGndUomfZtdgGrp4ouLZk6W4ogD2MpsYNSixkXyW",
                                              "64cIbV7uSvZVVZbJMtaXxb6bpIKOgBQ6xTEH5SMpenPAEgJoPVts816rhHdfwK5Q",
                                              "8zetklegckYAZtFbqmM0xjOI6bu5rqwFLWr1xo33jF0wDYPQ8RHMJkruB1FIB8V2",
                                              "GxvNAoGBAM4g2z8NTPMqX+8IBGkGgqmcYuRQxd3cs7LOSEjF9hPy1it2ZFe/yUKq",
                                              "ePa2E8osffK5LBkFzhyQb0WrGC9ijM9E6rv10gyuNjlwXdFJcdqVamxwPUBtxRJR",
                                              "cYTY2HRkJXDdtT0Bkc3josE6UUDvwMpO0CfAETQPto1tjNEDhQhT",
                                              "-----END RSA PRIVATE KEY-----"
                                            ]
                                }
                            ]
                        },
                        "tcpSettings": {},
                        "kcpSettings": {},
                        "wsSettings": {},
                        "httpSettings": {},
                        "dsSettings": {}
                        }
        self.translate = QCoreApplication.translate

    def createTransportPanel(self):
        TransportSettingPanel = self.createTransportSettingPanel()
        self.mkcp = mkcpPanel.mKcpPanel()
        self.tcp = tcpPanel.TcpPanel()
        self.ws = wsPanel.wsPanel()
        self.http2 = http2Panel.http2Panel()
        self.ds = dsPanel.domainSocketPanel()
        self.mkcpPanel = self.mkcp.createmKcpSettingPanel()
        self.tcpPanel = self.tcp.createTCPSettingPanel()
        self.wsPanel = self.ws.createwsSettingPanel()
        self.http2Panel = self.http2.createHttpSettingPanel()
        self.dsPanel = self.ds.createdsSettingPanel()
        self.mkcpPanel.hide()
        self.wsPanel.hide()
        self.http2Panel.hide()
        self.dsPanel.hide()
        
        vboxTransportProtocols = QVBoxLayout()
        vboxTransportProtocols.addWidget(self.mkcpPanel)
        vboxTransportProtocols.addWidget(self.tcpPanel)
        vboxTransportProtocols.addWidget(self.wsPanel)
        vboxTransportProtocols.addWidget(self.http2Panel)
        vboxTransportProtocols.addWidget(self.dsPanel)
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
        btn = e.text()
        self.tcpPanel.hide()
        self.wsPanel.hide()
        self.mkcpPanel.hide()
        self.http2Panel.hide()
        self.dsPanel.hide()
        if (btn == self.translate("TransportSettingPanel", "mKcp")):
            self.mkcpPanel.show()
        elif (btn == self.translate("TransportSettingPanel", "ws")):
            self.wsPanel.show()
        elif (btn == self.translate("TransportSettingPanel", "TCP")):
            self.tcpPanel.show()
        elif (btn == self.translate("TransportSettingPanel", "http")):
            self.http2Panel.show()
        elif (btn == self.translate("TransportSettingPanel", "ds")):
            self.dsPanel.show()


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
            
        try:
            transportJSONFile["dsSettings"]
        except KeyError as e:
            logbook.writeLog("transport", "KeyError", e)
            transportJSONFile["dsSettings"] = None
        
        
        def hideSettingsandDisableRadioButton():
            self.tcpPanel.hide()
            self.wsPanel.hide()
            self.mkcpPanel.hide()
            self.http2Panel.hide()
            self.dsPanel.hide()
            self.ws.groupBoxwsSetting.setChecked(False)
            self.mkcp.groupBoxmKCPSetting.setChecked(False)
            self.tcp.groupBoxTCPSetting.setChecked(False)
            self.http2.groupBoxhttp.setChecked(False)
            self.ds.groupBoxdsSetting.setChecked(False)

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
                self.http2Panel.show()
                if (transportJSONFile["httpSettings"]):
                    self.http2.groupBoxhttp.setChecked(True)
                    self.http2.settingHttpPanelFromJSONFile(
                        copy.deepcopy(transportJSONFile["httpSettings"]), openFromJSONFile)
            
            elif (protocol == "ds"):
                hideSettingsandDisableRadioButton()
                self.radioButtonTransportDS.setChecked(True)
                self.dsPanel.show()
                if (transportJSONFile["httpSettings"]):
                    self.ds.groupBoxdsSetting.setChecked(True)
                    self.ds.settingdsPanelFromJSONFile(
                        copy.deepcopy(transportJSONFile["dsSettings"]), openFromJSONFile)
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
                try:
                    self.lineEditCertificatealpn.setText(", ".join([str(x) for x in transportJSONFile["tlsSettings"]["alpn"]]))
                except KeyError as e:
                    logbook.writeLog("transport", "KeyError", e)
        else:
            cleartlsSettings()
            certificatesFilesNumber = 0
            
        if (certificatesFilesNumber):
            try:
                for i in range(certificatesFilesNumber):
                    self.onbtnCertificatesaddNewRow()
                    combox = self.tableWidgetUserCertificates.cellWidget(i, 0)
                    try:
                        combox.setCurrentText(str(certificateFiles[i]["useage"]))
                    except Exception: pass
                    self.tableWidgetUserCertificates.setItem(
                        i, 1, QTableWidgetItem(str(certificateFiles[i]["certificateFile"])))
                    self.tableWidgetUserCertificates.setItem(
                        i, 2, QTableWidgetItem(str(certificateFiles[i]["keyFile"])))
                    self.tableWidgetUserCertificates.setItem(
                        i, 3, QTableWidgetItem(",".join(certificateFiles[i]["certificate"])))
                    self.tableWidgetUserCertificates.setItem(
                        i, 4, QTableWidgetItem(",".join(certificateFiles[i]["key"])))
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
        if (self.radioButtonTransportDS.isChecked()):
            transportJSONFile["network"] = "ds"    
        
        
        if (self.groupBoxTLSSetting.isChecked()):
            transportJSONFile["security"] = "tls"
            transportJSONFile["tlsSettings"] = {}
            if self.checkBoxCertificateAllowInsecure.isChecked():
                transportJSONFile["tlsSettings"]["allowInsecure"] = True
            if self.lineEditCertificateServerName.text():
                transportJSONFile["tlsSettings"]["serverName"] = copy.deepcopy(
                    self.lineEditCertificateServerName.text())
            if self.lineEditCertificatealpn.text():
                transportJSONFile["tlsSettings"]["alpn"] = copy.deepcopy(
                    [x.strip() for x in re.split(r"[,;]", self.lineEditCertificatealpn.text())])
            certificatesFilesNumber = self.tableWidgetUserCertificates.rowCount()
            files = []
            if (certificatesFilesNumber > 0):
                for i in range(0, certificatesFilesNumber):
                    fileName = {}
                    useage = self.tableWidgetUserCertificates.cellWidget(i, 0)
                    certificateFile = self.tableWidgetUserCertificates.item(i, 1)
                    keyFile = self.tableWidgetUserCertificates.item(i, 2)
                    certificate = self.tableWidgetUserCertificates.item(i, 3)
                    key = self.tableWidgetUserCertificates.item(i, 4)
                    fileName["useage"] = useage.currentText()
                    if (certificateFile and keyFile):
                        fileName["certificateFile"] = certificateFile.text()
                        fileName["keyFile"] = keyFile.text()
                    if (certificate and key):
                        fileName["certificate"] = [x for x in certificate.text().split(",")]
                        fileName["key"] = [x for x in key.text().split(",")]
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

        if (self.radioButtonTransportHTTP.isChecked() and self.http2.groupBoxhttp.isChecked()):
            transportJSONFile["httpSettings"] = copy.deepcopy(self.http2.createHttpSettingJSONFile())
        
        if (self.radioButtonTransportDS.isChecked() and self.ds.groupBoxdsSetting.isChecked()):
            transportJSONFile["dsSettings"] = copy.deepcopy(self.ds.createdsSettingJSONFile())
        return transportJSONFile
    
    def clearTransportPanel(self):
        # set to Default
        self.checkBoxTransportSetting.setChecked(False)
        self.tableWidgetUserCertificates.setRowCount(0)
        self.groupBoxTLSSetting.setChecked(False)
        self.lineEditCertificateServerName.clear()
        self.lineEditCertificatealpn.clear()
        self.checkBoxCertificateAllowInsecure.setChecked(False)
        self.radioButtonTransportTCP.setChecked(True)
        self.radioButtonmTransportKCP.setChecked(False)
        self.radioButtonTransportWS.setChecked(False)
        self.radioButtonTransportHTTP.setChecked(False)
        self.radioButtonTransportDS.setChecked(False)
        self.tcpPanel.show()
        self.groupTransportPanel.hide()
        self.mkcp.clearmkcpPanel()
        self.ws.clearwsPanel()
        self.tcp.cleartcpPanel()
        self.http2.clearHttpPanel()
        self.ds.cleardsPanel()

    def __debugTest(self):
        import json
        print(json.dumps(self.createtransportSettingJSONFile(), indent=4, sort_keys=False))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TransportPanel()
    ex.setLayout(ex.createTransportPanel())
    ex.setGeometry(300, 300, 680, 620)
    ex.show()
    sys.exit(app.exec_())
